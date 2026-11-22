#!/usr/bin/env python3
"""Calcola il ricavo netto e il margine di un acquisto per canale di rivendita.

Esempi:
  margine.py --canali
  margine.py --acquisto 40 --vendita 300 --tutti
  margine.py --acquisto 40 --vendita 300 --canale cardmarket --spedizione 6 --extra 25
  margine.py --vendita 300 --canale ebay_privato --margine-voluto 0.4

Convenzioni:
  --vendita      prezzo dell'oggetto pagato dall'acquirente (o aggiudicazione in asta,
                 o offerta del commerciante per il canale "antiquario").
  --spedizione   costo di spedizione/imballo/assicurazione che resta a tuo carico.
  --extra        altri costi: grading, perizia, restauro, trasporto, viaggio.
  Le commissioni sono calcolate sul solo --vendita (eBay le calcola sul totale pagato,
  spedizione compresa: se la fai pagare all'acquirente aggiungila a --vendita).
"""
import argparse
import sys

DATA_VERIFICA = "2026-11-22"

# pct: lista di scaglioni (soglia_superiore_o_None, percentuale) applicati a quote.
# fisso: euro per ordine. iva: True se alle commissioni si aggiunge l'IVA al 22%.
CANALI = {
    "ebay_privato": dict(
        pct=[(None, 0.0)], fisso=0.0, iva=False,
        nota="eBay.it venditore privato residente in Italia: 0% dal 1/9/2026 (verificato)."),
    "ebay_pro_collezionismo": dict(
        pct=[(990, 0.11), (None, 0.02)], extra_pct=0.0035, fisso=0.35, iva=True,
        nota="eBay.it professionale, arte/antiquariato/collezionismo/giocattoli: 11% fino a 990 € + 2% oltre, +0,35% e 0,35 €; IVA sulle commissioni (verificato)."),
    "ebay_pro_carte": dict(
        pct=[(990, 0.065), (None, 0.02)], extra_pct=0.0035, fisso=0.35, iva=True,
        nota="eBay.it professionale, carte collezionabili: 6,5% fino a 990 € + 2% oltre (verificato)."),
    "cardmarket": dict(
        pct=[(None, 0.05)], fisso=0.0, iva=False,
        nota="Cardmarket, carte singole, privato: 5% (verificato). Il sigillato può differire."),
    "vinted": dict(
        pct=[(None, 0.0)], fisso=0.0, iva=False,
        nota="Vinted: nessuna commissione per il venditore (paga l'acquirente). Da ricontrollare."),
    "subito": dict(
        pct=[(None, 0.0)], fisso=0.0, iva=False,
        nota="Subito.it privato: nessuna commissione per il venditore. Da ricontrollare."),
    "catawiki": dict(
        pct=[(None, 0.125)], fisso=0.0, iva=True,
        nota="Catawiki: 12,5% + una quota fissa, IVA esclusa (verificato); la quota fissa non è inclusa: aggiungila con --fisso."),
    "chrono24": dict(
        pct=[(None, 0.0695)], fisso=0.0, iva=False,
        nota="Chrono24, venditore privato: 6,95% (verificato)."),
    "discogs": dict(
        pct=[(None, 0.09)], fisso=0.0, iva=False,
        nota="Discogs: 9% (verificato; anche sulla spedizione, con tetto per ordine) + commissione di pagamento non inclusa."),
    "reverb": dict(
        pct=[(None, 0.0819)], fisso=0.49, iva=False,
        nota="Reverb: 5% di vendita (verificato) + circa 3,19% + 0,49 di pagamento (indicativo)."),
    "vestiaire": dict(
        pct=[(None, 0.20)], fisso=0.0, iva=False,
        nota="Vestiaire Collective: 17% + 3% di pagamento per articoli 75–15.000 € (verificato)."),
    "delcampe": dict(
        pct=[(None, 0.055)], fisso=0.15, iva=False,
        nota="Delcampe: circa 5,5% + piccola quota per oggetto (indicativo, da ricontrollare)."),
    "tarisio": dict(
        pct=[(None, 0.20)], fisso=0.0, iva=False,
        nota="Tarisio (violini e archi): 20% sull'aggiudicazione fino a circa 9.000 € (verificato)."),
    "emovieposter": dict(
        pct=[(None, 0.28)], fisso=0.0, iva=False,
        nota="eMoviePoster: il venditore incassa circa il 72% di quanto paga l'acquirente (verificato); --vendita = prezzo pagato."),
    "stockx": dict(
        pct=[(None, 0.12)], fisso=0.0, iva=False,
        nota="StockX: 9–7% secondo il livello + 3% di pagamento, minimo circa 5 € (verificato); solo nuovo."),
    "casa_aste": dict(
        pct=[(None, 0.17)], fisso=0.0, iva=True,
        nota="Casa d'aste: tipicamente 10–25% sull'aggiudicazione + costi foto/assicurazione; qui 15% + 2%. Usa i valori del mandato reale con --commissione."),
    "antiquario": dict(
        pct=[(None, 0.0)], fisso=0.0, iva=False,
        nota="Vendita diretta a un commerciante: nessuna commissione, ma --vendita deve essere la sua offerta (in genere 30–50% del prezzo al pubblico)."),
}


def commissione(canale, vendita, pct_override=None, fisso_override=None):
    c = CANALI[canale]
    if pct_override is not None:
        variabile = vendita * pct_override
    else:
        variabile, base = 0.0, 0.0
        for soglia, pct in c["pct"]:
            tetto = vendita if soglia is None else min(vendita, soglia)
            if tetto > base:
                variabile += (tetto - base) * pct
                base = tetto
        variabile += vendita * c.get("extra_pct", 0.0)
    fisso = c["fisso"] if fisso_override is None else fisso_override
    totale = variabile + (fisso if vendita > 0 else 0.0)
    if c["iva"]:
        totale *= 1.22
    return round(totale, 2)


def calcola(canale, acquisto, vendita, spedizione, extra, pct=None, fisso=None):
    comm = commissione(canale, vendita, pct, fisso)
    incasso = vendita - comm - spedizione - extra
    utile = incasso - acquisto
    roi = utile / acquisto if acquisto > 0 else None
    return dict(canale=canale, commissione=comm, incasso=round(incasso, 2),
                utile=round(utile, 2), roi=roi)


def eur(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--acquisto", type=float, default=0.0, help="prezzo pagato per l'oggetto (€)")
    p.add_argument("--vendita", type=float, help="prezzo di vendita atteso (€)")
    p.add_argument("--canale", choices=sorted(CANALI), default="ebay_privato")
    p.add_argument("--tutti", action="store_true", help="confronta tutti i canali")
    p.add_argument("--spedizione", type=float, default=0.0, help="costi di spedizione a tuo carico (€)")
    p.add_argument("--extra", type=float, default=0.0, help="grading, perizia, restauro, viaggi (€)")
    p.add_argument("--commissione", type=float, help="percentuale reale da usare, es. 0.15 (sostituisce la tabella)")
    p.add_argument("--fisso", type=float, help="quota fissa reale per ordine (€)")
    p.add_argument("--margine-voluto", type=float,
                   help="utile voluto come frazione del costo, es. 0.4: calcola il prezzo massimo da pagare")
    p.add_argument("--minimo", type=float, default=0.0, help="utile minimo voluto in euro (con --margine-voluto)")
    p.add_argument("--canali", action="store_true", help="elenca canali e commissioni")
    a = p.parse_args(argv)

    if a.canali:
        print(f"Commissioni (data di verifica {DATA_VERIFICA}):")
        for nome in sorted(CANALI):
            print(f"  {nome:24} {CANALI[nome]['nota']}")
        return 0
    if a.vendita is None:
        p.error("serve --vendita (oppure --canali)")

    # "antiquario" resta fuori dal confronto: il suo prezzo non è il prezzo di mercato.
    canali = [c for c in sorted(CANALI) if c != "antiquario"] if a.tutti else [a.canale]

    if a.margine_voluto is not None:
        print(f"Prezzo massimo da pagare per vendere a {eur(a.vendita)} "
              f"con utile ≥ {a.margine_voluto:.0%} del costo e ≥ {eur(a.minimo)}:")
        for c in canali:
            incasso = calcola(c, 0, a.vendita, a.spedizione, a.extra, a.commissione, a.fisso)["incasso"]
            massimo = min(incasso / (1 + a.margine_voluto), incasso - a.minimo)
            print(f"  {c:24} incasso netto {eur(incasso):>12}  →  paga al massimo {eur(max(massimo, 0)):>12}")
        return 0

    righe = [calcola(c, a.acquisto, a.vendita, a.spedizione, a.extra, a.commissione, a.fisso) for c in canali]
    righe.sort(key=lambda r: r["utile"], reverse=True)
    print(f"Acquisto {eur(a.acquisto)} · vendita {eur(a.vendita)} · spedizione {eur(a.spedizione)} · extra {eur(a.extra)}")
    print(f"{'canale':24} {'commissioni':>12} {'incasso':>12} {'utile':>12} {'utile/costo':>12}")
    for r in righe:
        roi = "—" if r["roi"] is None else f"{r['roi']:.0%}"
        print(f"{r['canale']:24} {eur(r['commissione']):>12} {eur(r['incasso']):>12} {eur(r['utile']):>12} {roi:>12}")
    print(f"\nCommissioni verificate il {DATA_VERIFICA}; vedi --canali per le note. "
          "Per un commerciante usa --canale antiquario con la sua offerta reale come --vendita.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
