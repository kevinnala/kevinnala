#!/usr/bin/env python3
"""Perizie dopo ogni giro dello scanner: prepara i candidati, poi invia le schede su Telegram
e le ricorda (memoria/periziati.jsonl) così il giro dopo non le ripropone.

  perizie.py prepara [--n 30] [--scelti]
                                     # --scelti: prima gli annunci scelti nelle griglie di esplora.py
                                     # (risultati/esplora/scelti.txt), poi completa fino a N con i primi
                                     # NON ancora periziati dell'ultimo report dello scanner per parole;
                                     # scarica le foto e fa un provino per annuncio; scrive
                                     # risultati/perizie/da_periziare.json e stampa le lezioni dagli esiti
  perizie.py modello                 # stampa un esempio del file perizie.json da compilare
  perizie.py invia <perizie.json> [--prova]
                                     # controlla il file, numera le perizie (#N), le manda su Telegram
                                     # (COMPRA/TRATTA/VERIFICA con scheda completa, LASCIA in una riga)
                                     # e le aggiunge alla memoria

Formato di perizie.json: lista di oggetti, uno per annuncio di da_periziare.json (vedi `modello`).
La perizia la scrive Claude guardando foto e testo con la skill caccia-affari: lo script non stima nulla.
"""
import html
import json
import os
import re
import sys
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import memoria  # noqa: E402

RIS = os.path.normpath(os.path.join(QUI, "..", "risultati"))
DIR = os.path.join(RIS, "perizie")
F_CANDIDATI = os.path.join(DIR, "da_periziare.json")
VERDETTI = ["COMPRA", "TRATTA", "VERIFICA PRIMA", "LASCIA"]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

MODELLO = [{
    "id": "669304052",
    "verdetto": "TRATTA",
    "nome": "11 tazzine da caffè Richard Ginori 'Pittoria di Doccia'",
    "cosa": "Tazzine con piattino di decori diversi, marchio a cartiglio dorato; produzione seconda metà '900.",
    "fiducia": "certo sul marchio, epoca da confermare",
    "errore_venditore": "prezzo simbolico di 1 €, chiede offerte",
    "valore": [90, 130, 180],
    "comparabili": "Etsy 2 tazze 50 € (chiesto); eBay set tazza 80 € (chiesto)",
    "dove": "eBay privato o Vinted a coppie → netto ~130 €; lotto Catawiki → netto ~110 €",
    "verifiche": "foto del marchio sotto ogni pezzo; niente sbeccature",
    "rischi": "",
    "offerta": 40,
    "massimo": 60,
}]


def ultimo_report():
    import glob
    reports = sorted(glob.glob(os.path.join(RIS, "report-*.json")))
    if not reports:
        sys.exit("Nessun report: lancia prima lo scanner.")
    with open(reports[-1], encoding="utf-8") as fh:
        return json.load(fh), reports[-1]


def scarica_foto(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/jpeg,image/*"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as fh:
            fh.write(r.read())
        return True
    except Exception:  # noqa: BLE001
        return False


def provino(files, dest, larghezza=420):
    """Unisce le foto di un annuncio in un'unica immagine (una lettura invece di tante)."""
    try:
        from PIL import Image
    except ImportError:
        return False
    ims = []
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            ims.append(im.resize((larghezza, max(1, int(larghezza * im.height / im.width)))))
        except Exception:  # noqa: BLE001
            continue
    if not ims:
        return False
    tela = Image.new("RGB", (larghezza * len(ims), max(i.height for i in ims)), "white")
    for k, im in enumerate(ims):
        tela.paste(im, (larghezza * k, 0))
    tela.save(dest, quality=80)
    return True


def da_esplora():
    """Annunci scelti da Claude nelle griglie di esplora.py (risultati/esplora/scelti.txt)."""
    f_cand = os.path.join(RIS, "esplora", "candidati.json")
    f_scelti = os.path.join(RIS, "esplora", "scelti.txt")
    if not (os.path.exists(f_cand) and os.path.exists(f_scelti)):
        return []
    with open(f_cand, encoding="utf-8") as fh:
        cand = json.load(fh)
    per_k = {str(a["k"]): a for a in cand}
    per_id = {a["id"]: a for a in cand}
    with open(f_scelti, encoding="utf-8") as fh:
        voci = re.findall(r"[#\w-]+", fh.read())
    out = []
    for v in voci:
        a = per_k.get(v.lstrip("#")) or per_id.get(v)
        if a and a not in out:
            out.append(a)
    return out


def prepara(n, max_foto=4, con_scelti=False):
    gia = memoria.ids_periziati()
    scelti = [a for a in da_esplora() if a["id"] not in gia] if con_scelti else []
    try:
        annunci, nome = ultimo_report()
    except SystemExit:
        annunci, nome = [], "nessun report dello scanner per parole"
    presi = {a["id"] for a in scelti}
    scelti += [a for a in annunci if a["id"] not in gia and a["id"] not in presi][: max(0, n - len(scelti))]
    os.makedirs(DIR, exist_ok=True)
    out = []
    for a in scelti:
        cartella = os.path.join(DIR, a["id"])
        os.makedirs(cartella, exist_ok=True)
        files = []
        for k, u in enumerate((a.get("foto") or [])[:max_foto], 1):
            f = os.path.join(cartella, f"{k}.jpg")
            if os.path.exists(f) or scarica_foto(u, f):
                files.append(f)
        prov = os.path.join(DIR, f"provino-{a['id']}.jpg")
        out.append({
            "id": a["id"], "titolo": a["titolo"], "prezzo": a.get("prezzo"), "url": a["url"],
            "fonte": a.get("fonte") or "Subito", "luogo": f"{a.get('comune') or ''} ({a.get('provincia') or ''})".strip(),
            "spedizione": a.get("spedizione"), "categoria": a.get("categoria"), "punti": a.get("punti"),
            "condizione": a.get("condizione"), "data": a.get("data"), "testo": (a.get("testo") or "")[:1500],
            "origine": "griglie" if a.get("k") else "parole",
            "extra": {k: a[k] for k in ("termine", "tribunale", "prezzo_con_oneri") if a.get(k)},
            "provino": prov if provino(files, prov) else None, "n_foto_scaricate": len(files),
        })
    with open(F_CANDIDATI, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"Report: {os.path.basename(nome)} · già periziati esclusi: {len(gia)} · candidati: {len(out)} "
          f"(dalle griglie: {sum(c['origine'] == 'griglie' for c in out)})")
    print(f"Candidati: {F_CANDIDATI}")
    for i, c in enumerate(out, 1):
        print(f"{i:2}. [{c['id']}] {c['prezzo']} € · {c['titolo'][:60]} · {c['categoria']} · provino: {c['provino'] or 'nessuna foto'}")
    print()
    print(memoria.lezioni())
    if len(out) < n:
        print(f"\nAttenzione: solo {len(out)} candidati nuovi (chiesti {n}). Abbassa punti_minimi_report o rilancia lo scanner.")


def controlla(perizie, candidati):
    per_id = {c["id"]: c for c in candidati}
    errori = []
    for p in perizie:
        if p.get("id") not in per_id:
            errori.append(f"id {p.get('id')} non è tra i candidati")
            continue
        if p.get("verdetto") not in VERDETTI:
            errori.append(f"{p['id']}: verdetto deve essere uno di {VERDETTI}")
        v = p.get("valore")
        if not (isinstance(v, list) and len(v) == 3 and all(isinstance(x, (int, float)) for x in v)):
            errori.append(f"{p['id']}: valore deve essere [prudente, probabile, ottimista]")
        if p.get("verdetto") != "LASCIA":
            for campo in ("cosa", "dove", "verifiche", "offerta"):
                if not p.get(campo):
                    errori.append(f"{p['id']}: manca '{campo}'")
        # completa con i dati dell'annuncio
        c = per_id.get(p.get("id"), {})
        for k in ("titolo", "prezzo", "url", "fonte", "luogo", "spedizione", "categoria", "extra"):
            p.setdefault(k, c.get(k))
    return errori


def eur(x):
    return "n.d." if x in (None, "") else f"{x:.0f} €" if isinstance(x, (int, float)) else str(x)


def e(testo):
    return html.escape(str(testo), quote=False)


def scheda(p):
    sped = "📦" if p.get("spedizione") else "🤝 solo ritiro"
    asta = (p.get("fonte") or "").startswith("Asta")
    if asta:
        sped = "🏛️ ritiro o spedizione da chiedere all'IVG"
    v = p["valore"]
    margine = ""
    if isinstance(p.get("offerta"), (int, float)):
        margine = f" · margine atteso ~{v[1] - p['offerta']:+.0f} €"
    righe = [
        f"<b>#{p['n']} · {e(p['verdetto'])} · {e(p.get('nome') or p['titolo'])}</b>",
        f"💶 Chiesto {eur(p.get('prezzo'))} · {e(p.get('fonte') or '')} · {e(p.get('luogo') or '')} {sped}",
        *([f"⏰ Asta: termine {e(p['extra'].get('termine', '?'))} · Tribunale di {e(p['extra'].get('tribunale', '?'))}"
           f" · base con oneri {eur(p['extra'].get('prezzo_con_oneri'))}"] if asta and p.get("extra") else []),
        f"🔍 {e(p.get('cosa', ''))}",
        f"🎓 Fiducia: {e(p.get('fiducia', 'n.d.'))}",
    ]
    if p.get("errore_venditore"):
        righe.append(f"🙈 Il venditore: {e(p['errore_venditore'])}")
    righe.append(f"💰 Valore: prudente {eur(v[0])} · probabile {eur(v[1])} · ottimista {eur(v[2])}")
    if p.get("comparabili"):
        righe.append(f"📊 {e(p['comparabili'])}")
    righe.append(f"🏪 Dove vendere: {e(p.get('dove', ''))}")
    righe.append(f"✅ Prima di pagare: {e(p.get('verifiche', ''))}")
    if p.get("rischi"):
        righe.append(f"⚠️ {e(p['rischi'])}")
    righe.append(f"🎯 Offri {eur(p.get('offerta'))} (massimo {eur(p.get('massimo'))}){margine}")
    righe.append(f"<a href=\"{html.escape(p['url'])}\">Apri annuncio</a>")
    return "\n".join(righe)


def riga_lascia(p):
    motivo = p.get("motivo") or p.get("cosa") or ""
    return (f"#{p['n']} <a href=\"{html.escape(p['url'])}\">{e((p.get('nome') or p['titolo'])[:55])}</a> · "
            f"{eur(p.get('prezzo'))} → vale {eur(p['valore'][0])}-{eur(p['valore'][2])}. {e(motivo[:140])}")


def componi(perizie, max_car=3900):
    buone = [p for p in perizie if p["verdetto"] != "LASCIA"]
    lascia = [p for p in perizie if p["verdetto"] == "LASCIA"]
    ordine = {v: i for i, v in enumerate(VERDETTI)}
    def costo(p):
        for k in ("offerta", "prezzo"):
            if isinstance(p.get(k), (int, float)):
                return p[k]
        return 0
    buone.sort(key=lambda p: (ordine[p["verdetto"]], -((p["valore"][1] or 0) - costo(p))))
    intest = (f"🧾 <b>PERIZIE · {memoria.oggi()}</b>\n{len(perizie)} annunci periziati: "
              f"{sum(p['verdetto'] == 'COMPRA' for p in perizie)} COMPRA · {sum(p['verdetto'] == 'TRATTA' for p in perizie)} TRATTA · "
              f"{sum(p['verdetto'] == 'VERIFICA PRIMA' for p in perizie)} VERIFICA · {len(lascia)} LASCIA\n"
              "Per dirmi com'è andata: /preso #N prezzo · /venduto #N prezzo canale · /scartato #N motivo · /aiuto")
    pezzi = [intest] + [scheda(p) for p in buone]
    if lascia:
        pezzi.append("<b>LASCIA</b> (prezzo già giusto o niente mercato)\n" + "\n".join(riga_lascia(p) for p in lascia))
    messaggi, cur = [], ""
    for pz in pezzi:
        for blocco in ([pz] if len(pz) <= max_car else [pz[i:i + max_car] for i in range(0, len(pz), max_car)]):
            if cur and len(cur) + len(blocco) + 2 > max_car:
                messaggi.append(cur)
                cur = ""
            cur = f"{cur}\n\n{blocco}" if cur else blocco
    if cur:
        messaggi.append(cur)
    return messaggi


def invia(percorso, prova=False):
    with open(percorso, encoding="utf-8") as fh:
        perizie = json.load(fh)
    with open(F_CANDIDATI, encoding="utf-8") as fh:
        candidati = json.load(fh)
    errori = controlla(perizie, candidati)
    if errori:
        sys.exit("Perizie da correggere:\n- " + "\n- ".join(errori))
    gia = memoria.ids_periziati()
    perizie = [p for p in perizie if p["id"] not in gia]
    if not perizie:
        sys.exit("Tutte queste perizie sono già state mandate.")
    if prova:
        s = memoria.stato()
        for k, p in enumerate(perizie, 1):
            p["n"] = s["ultimo_numero"] + k
        print("\n\n----- messaggio -----\n".join(componi(perizie)))
        return
    import notifica_telegram as tg
    chat_id = tg.chat_id()
    s = memoria.stato()
    for k, p in enumerate(perizie, 1):
        p["n"] = s["ultimo_numero"] + k  # numeri provvisori per il messaggio, confermati da registra_perizie
    testi = componi(perizie)
    for t in testi:
        r = tg.api("sendMessage", chat_id=chat_id, text=t, parse_mode="HTML", disable_web_page_preview="true")
        if not r.get("ok"):
            sys.exit(f"Telegram ha rifiutato il messaggio: {r}")
    memoria.registra_perizie(perizie)
    print(f"Inviate {len(perizie)} perizie in {len(testi)} messaggi; memoria aggiornata ({memoria.F_PERIZIATI}).")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "prepara":
        prepara(int(argv[argv.index("--n") + 1]) if "--n" in argv else 30, con_scelti="--scelti" in argv)
    elif argv[0] == "modello":
        print(json.dumps(MODELLO, ensure_ascii=False, indent=1))
    elif argv[0] == "invia":
        invia(argv[1], "--prova" in argv)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
