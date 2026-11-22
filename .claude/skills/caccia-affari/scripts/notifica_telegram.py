#!/usr/bin/env python3
"""Manda su Telegram la lista dei migliori annunci dell'ultimo report dello scanner.

Configurazione (una volta sola):
  1. Su Telegram scrivi a @BotFather, comando /newbot, scegli un nome: ottieni il TOKEN del bot.
  2. Scrivi /start al tuo nuovo bot (serve perché il bot possa scriverti).
  3. Metti il token nelle impostazioni dell'ambiente come variabile TELEGRAM_BOT_TOKEN
     (mai in chat, mai nel repository).
  4. Lancia: notifica_telegram.py --chat-id   → stampa il tuo chat id; mettilo in
     scanner_config.json → "telegram": {"chat_id": "..."} oppure nella variabile TELEGRAM_CHAT_ID.

Uso:
  notifica_telegram.py              # manda i migliori dell'ultimo report
  notifica_telegram.py --prova      # mostra il messaggio senza mandarlo
  notifica_telegram.py --chat-id    # trova il tuo chat id
"""
import glob
import html
import json
import os
import sys
import urllib.parse
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
RIS = os.path.join(QUI, "..", "risultati")


def api(metodo, **params):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        sys.exit("Manca la variabile TELEGRAM_BOT_TOKEN (impostala nelle impostazioni dell'ambiente).")
    dati = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/{metodo}", data=dati, timeout=30) as r:
        return json.load(r)


def messaggi(annunci, intestazione, massimo_car=3900):
    blocchi, cur = [], intestazione
    for i, a in enumerate(annunci, 1):
        prezzo = f"{a['prezzo']:.0f} €" if a.get("prezzo") else "prezzo n.d."
        dove = a.get("comune") or ""
        if a.get("provincia"):
            dove = f"{dove} ({a['provincia']})".strip()
        sped = "📦" if a.get("spedizione") else "🤝 solo ritiro"
        riga = (f"\n\n<b>{i}. {html.escape(a['titolo'][:80])}</b>\n"
                f"{prezzo} · {html.escape(a.get('fonte', 'Subito'))} · {html.escape(dove)} {sped}\n"
                f"{html.escape(a.get('categoria') or '')} · punti {a['punti']}\n"
                f"<a href=\"{html.escape(a['url'])}\">Apri annuncio</a>")
        if len(cur) + len(riga) > massimo_car:
            blocchi.append(cur)
            cur = ""
        cur += riga
    blocchi.append(cur)
    return blocchi


def main(argv):
    cfg = json.load(open(os.path.join(QUI, "scanner_config.json"), encoding="utf-8"))
    tg = cfg.get("telegram", {})
    if "--chat-id" in argv:
        r = api("getUpdates")
        chat = {(u.get("message") or {}).get("chat", {}).get("id"): (u.get("message") or {}).get("chat", {}).get("first_name")
                for u in r.get("result", [])}
        print(chat or "Nessun messaggio: scrivi /start al bot e riprova.")
        return 0
    reports = sorted(glob.glob(os.path.join(RIS, "report-*.json")))
    if not reports:
        sys.exit("Nessun report: lancia prima lo scanner.")
    annunci = json.load(open(reports[-1], encoding="utf-8"))
    soglia, quanti = tg.get("punti_minimi", 9), tg.get("massimo_annunci", 15)
    scelti = [a for a in annunci if a["punti"] >= soglia][:quanti]
    nome = os.path.basename(reports[-1]).replace("report-", "").replace(".json", "")
    if not scelti:
        testo = [f"🔎 Scanner {nome}: nessuna novità sopra la soglia ({soglia} punti)."]
    else:
        testo = messaggi(scelti, f"🔎 <b>Scanner {nome}</b>: {len(scelti)} annunci da guardare "
                                 f"(il punteggio ordina, non stima il valore)")
    if "--prova" in argv:
        print("\n\n----- messaggio -----\n".join(testo))
        return 0
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or tg.get("chat_id")
    if not chat_id:
        sys.exit("Manca il chat id: lancia notifica_telegram.py --chat-id")
    for t in testo:
        r = api("sendMessage", chat_id=chat_id, text=t, parse_mode="HTML", disable_web_page_preview="true")
        if not r.get("ok"):
            sys.exit(f"Telegram ha rifiutato il messaggio: {r}")
    print(f"Inviati {len(testo)} messaggi con {len(scelti)} annunci.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
