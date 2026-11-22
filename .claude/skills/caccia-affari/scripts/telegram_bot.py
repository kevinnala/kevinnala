#!/usr/bin/env python3
"""Legge i messaggi che l'utente ha scritto al bot e li registra in memoria/esiti.jsonl.

Non è un server sempre acceso: i messaggi restano in coda su Telegram (fino a 24 ore) e
vengono letti a ogni giro (prima dello scanner e prima delle perizie). Il bot risponde
confermando cosa ha capito.

  telegram_bot.py              # legge i messaggi nuovi, li registra e risponde
  telegram_bot.py --prova      # mostra cosa registrerebbe, senza salvare né rispondere

Comandi che l'utente può scrivere (il numero #N è quello delle perizie):
  /preso #12 40                → ho comprato la perizia #12 a 40 €
  /venduto #12 130 ebay        → l'ho venduta a 130 € su eBay
  /scartato #12 era una stampa → non l'ho presa (o la perizia era sbagliata) e perché
  /perso #12                   → l'ha comprata qualcun altro
  /nota testo libero           → un'osservazione da ricordare (es. "le tazzine Ginori si vendono male")
  /altri 30                    → al prossimo giro altre 30 perizie dalla coda (annunci non ancora periziati)
  /coda                        → quanti annunci aspettano la perizia
  /bilancio                    → riepilogo di acquisti, vendite e utile
  /lezioni                     → cosa ho imparato dagli esiti
  /aiuto                       → questo elenco
Si accettano anche il link dell'annuncio al posto di #N e le parole senza "/" (preso, venduto...).
Un messaggio senza comando viene salvato come nota.
"""
import html
import os
import re
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import memoria  # noqa: E402
import notifica_telegram as tg  # noqa: E402

AIUTO = """<b>Come dirmi com'è andata</b>
/preso #12 40 → hai comprato la perizia #12 a 40 €
/venduto #12 130 ebay → venduta a 130 € su eBay
/scartato #12 era una stampa → non presa, e perché
/perso #12 → l'ha presa qualcun altro
/nota testo → un'osservazione da ricordare
/altri 30 → al prossimo giro altre 30 perizie dalla coda
/coda → quanti annunci aspettano la perizia
/bilancio → acquisti, vendite e utile
/lezioni → cosa ho imparato
Puoi usare il link dell'annuncio al posto di #12. Leggo i messaggi a ogni giro dello scanner."""

COMANDI = ("preso", "comprato", "venduto", "scartato", "perso", "nota", "bilancio", "lezioni", "aiuto", "start", "help",
           "altri", "coda")
NUM = re.compile(r"(\d+(?:[.,]\d+)?)")


def prezzo(testo):
    m = NUM.search(testo.replace("€", " "))
    return float(m.group(1).replace(",", ".")) if m else None


def interpreta(testo):
    """Ritorna (esito da registrare o None, risposta)."""
    t = testo.strip()
    parole = t.split(maxsplit=1)
    cmd = parole[0].lstrip("/").split("@")[0].lower() if parole else ""
    resto = parole[1] if len(parole) > 1 else ""
    if cmd not in COMANDI:
        return {"tipo": "nota", "testo": t}, "📝 Nota salvata: la leggerò prima delle prossime perizie."
    if cmd in ("aiuto", "help", "start"):
        return None, AIUTO
    if cmd == "bilancio":
        return None, html.escape(memoria.bilancio())
    if cmd == "lezioni":
        return None, html.escape(memoria.lezioni())
    if cmd == "coda":
        return None, f"📥 In coda ci sono {len(memoria.coda())} annunci non ancora periziati. Scrivi /altri 30 per riceverne un blocco."
    if cmd == "altri":
        n = int(prezzo(resto) or 30)
        return {"tipo": "altri", "quanti": n}, (f"📥 Ok: al prossimo giro ti mando altre {n} perizie dalla coda "
                                               f"(in attesa: {len(memoria.coda())}).")
    if cmd == "nota":
        return {"tipo": "nota", "testo": resto}, "📝 Nota salvata."
    tipo = "preso" if cmd == "comprato" else cmd
    # riferimento: #N, link o id; il resto è prezzo, canale o motivo
    rif = None
    m = re.search(r"#(\d+)", resto) or re.search(r"(https?://\S+)", resto)
    if m:
        rif = m.group(1)
        resto_dopo = (resto[:m.start()] + resto[m.end():]).strip()
    else:
        pezzi = resto.split(maxsplit=1)
        rif = pezzi[0] if pezzi else None
        resto_dopo = pezzi[1] if len(pezzi) > 1 else ""
    p = memoria.trova_perizia(rif) if rif else None
    if not p:
        return ({"tipo": "nota", "testo": t},
                f"⚠️ Non trovo la perizia «{html.escape(rif or '')}». Ho salvato il messaggio come nota; "
                "usa il numero #N che trovi nelle perizie.")
    e = {"tipo": tipo, "n": p["n"], "id": p["id"], "testo": resto_dopo}
    nome = html.escape(p.get("nome") or p["titolo"])[:60]
    if tipo in ("preso", "venduto"):
        e["prezzo"] = prezzo(resto_dopo)
        if e["prezzo"] is None:
            return None, f"⚠️ Manca il prezzo. Esempio: /{tipo} #{p['n']} 40"
    if tipo == "venduto":
        canale = NUM.sub("", resto_dopo.replace("€", "")).strip(" ,.-")
        e["canale"] = canale.lower() or None
        preso = next((x.get("prezzo") for x in reversed(memoria.esiti()) if x.get("n") == p["n"] and x["tipo"] == "preso"), None)
        utile = f" · utile {e['prezzo'] - preso:+.0f} €" if preso is not None else " (non mi hai detto a quanto l'hai preso: /preso)"
        stima = p.get("valore", [None, None, None])[1]
        conf = f" · la mia stima probabile era {stima:.0f} €" if stima else ""
        return e, f"💰 Registrato: #{p['n']} {nome} venduto a {e['prezzo']:.0f} €{utile}{conf}."
    if tipo == "preso":
        return e, f"🛒 Registrato: #{p['n']} {nome} preso a {e['prezzo']:.0f} €. Quando lo vendi scrivi /venduto #{p['n']} prezzo canale."
    return e, f"👌 Registrato: #{p['n']} {nome} → {tipo}" + (f" ({html.escape(resto_dopo)})" if resto_dopo else "") + "."


def main(argv):
    prova = "--prova" in argv
    s = memoria.stato()
    cid = str(tg.chat_id())
    r = tg.api("getUpdates", offset=s.get("telegram_offset", 0), timeout=0)
    letti = 0
    for u in r.get("result", []):
        s["telegram_offset"] = u["update_id"] + 1
        msg = u.get("message") or u.get("edited_message") or {}
        if str(msg.get("chat", {}).get("id")) != cid or not msg.get("text"):
            continue  # solo i messaggi dell'utente configurato
        esito, risposta = interpreta(msg["text"])
        letti += 1
        print(f"«{msg['text']}» → {esito} ")
        if prova:
            continue
        if esito and esito["tipo"] == "altri":
            s["blocchi_richiesti"] = s.get("blocchi_richiesti", 0) + esito["quanti"]
        elif esito:
            esito["messaggio"] = msg["text"]
            memoria.registra_esito(esito)
        tg.api("sendMessage", chat_id=cid, text=risposta, parse_mode="HTML", disable_web_page_preview="true",
               reply_to_message_id=msg["message_id"])
    if not prova:
        memoria.salva_stato(s)
    print(f"Messaggi letti: {letti}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
