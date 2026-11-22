#!/usr/bin/env python3
"""Scanner di Subito.it: cerca annunci nelle zone configurate con le parole dei
venditori inconsapevoli, salta quelli già visti, li smista per categoria con
categoria.py, assegna un punteggio di "possibile affare" e scrive un report.

Uso:
  scanner.py                      # tutte le zone e tutte le ricerche
  scanner.py --max 10             # solo le prime 10 ricerche (prova veloce)
  scanner.py --anche-visti        # rimetti nel report anche gli annunci già visti
  scanner.py --config altro.json  # altra configurazione
  scanner.py --telegram           # alla fine manda la lista su Telegram (vedi notifica_telegram.py);
                                  # di norma non serve: dopo lo scanner si mandano le perizie (perizie.py)
  scanner.py --da-archivio        # rifà il report dagli annunci già salvati (dopo aver cambiato i segnali)

Configurazione: scanner_config.json (zone, ricerche, segnali). Archivio: risultati/annunci.sqlite
(locale) + memoria/visti.txt e memoria/periziati.jsonl (nel repository: valgono anche nelle sessioni nuove).
Report: risultati/report-AAAA-MM-GG-HHMM.md (i migliori in cima).

Il punteggio NON è una stima di valore: ordina gli annunci da guardare per primi.
La perizia vera la fa Claude con la skill, sui primi della lista.
"""
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.parse

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, ".."))
sys.path.insert(0, QUI)
import categoria as router  # noqa: E402
import fonti_extra  # noqa: E402
import memoria  # noqa: E402

OUT = os.path.join(RADICE, "risultati")


def carica_config(percorso):
    with open(percorso, encoding="utf-8") as fh:
        return json.load(fh)


def costruisci_richieste(cfg, massimo=None):
    ric = []
    for q in cfg["ricerche"]:
        for z in cfg["zone"]:
            url = z["url"].format(q=urllib.parse.quote_plus(q))
            ric.append({"url": url, "zona": z["nome"], "query": q})
    if massimo:
        ric = ric[: massimo * len(cfg["zone"])]
    # ricerche per manifattura/marchio: solo nelle zone con "marchi": true (di norma tutta Italia)
    marchi = cfg.get("ricerche_marchi", [])
    if massimo:
        marchi = marchi[:massimo]
    for q in marchi:
        for z in cfg["zone"]:
            if z.get("marchi"):
                ric.append({"url": z["url"].format(q=urllib.parse.quote_plus(q)), "zona": z["nome"], "query": q})
    return ric


def scarica(richieste):
    proc = subprocess.run(["node", os.path.join(QUI, "subito_fetch.js")], input=json.dumps(richieste),
                          capture_output=True, text=True, timeout=60 * 60)
    sys.stderr.write(proc.stderr)
    annunci = {}
    for riga in proc.stdout.splitlines():
        try:
            a = json.loads(riga)
        except json.JSONDecodeError:
            continue
        if a["id"] in annunci:
            annunci[a["id"]]["query"] += ", " + a["query"]
        else:
            annunci[a["id"]] = a
    return list(annunci.values())


def norm(s):
    return router.norm(s or "")


def punteggio(a, cat, cfg, bonus=None):
    """Ritorna (punti, motivi). Più alto = da guardare prima.
    bonus: {categoria: punti} imparati dagli esiti dell'utente (memoria.lezioni)."""
    s = cfg["segnali"]
    testo = f" {norm(a['titolo'])} {norm(a['testo'])} "
    punti, motivi = 0, []
    if a.get("categoria_subito") in s.get("categorie_subito_escluse", []):
        return -99, [f"categoria Subito esclusa: {a['categoria_subito']}"]
    vere = [x for x in cat if x[1]["id"] != "lotto-misto"]
    if vere:
        forza = vere[0][0]
        punti += 1 + min(forza, 4)
        motivi.append(f"categoria: {vere[0][1]['id']} (forza {forza})")
        b = (bonus or {}).get(vere[0][1]["id"])
        if b:
            punti += b
            motivi.append(f"esiti passati {b:+d}")
    elif cat:
        motivi.append("lotto misto")
    else:
        return -99, ["nessuna categoria da collezione"]
    trovati_valore = [w for w in s.get("valore", []) if f" {norm(w)} " in testo]
    if trovati_valore:
        punti += min(len(trovati_valore), 3)
        motivi.append("valore: " + ", ".join(trovati_valore[:4]))
    if a["azienda"]:
        punti -= 2
        motivi.append("venditore professionale")
    else:
        punti += 1
    for parola in s["inconsapevole"]:
        if f" {norm(parola)} " in testo:
            punti += 2
            motivi.append(f"\"{parola}\"")
    for parola in s["negativi"]:
        if f" {norm(parola)} " in testo:
            punti -= 3
            motivi.append(f"neg: \"{parola}\"")
    lung = len(a["testo"] or "")
    if lung < 120:
        punti += 1
        motivi.append("descrizione scarna")
    if a["n_foto"] <= 2:
        punti += 1
        motivi.append("poche foto")
    p = a["prezzo"]
    if p is None or p == 0:
        motivi.append("prezzo non indicato")
    elif p <= s["prezzo_basso"]:
        punti += 1
        motivi.append(f"prezzo basso ({p} €)")
    try:
        ore = (dt.datetime.now() - dt.datetime.fromisoformat(a["data"])).total_seconds() / 3600
        if ore <= 24:
            punti += 1
            motivi.append("pubblicato nelle ultime 24 ore")
        elif ore > 24 * s.get("giorni_vecchio", 120):
            punti -= 1
            motivi.append(f"annuncio vecchio ({int(ore // 24)} giorni)")
    except ValueError:
        pass
    return punti, motivi


def apri_db():
    os.makedirs(OUT, exist_ok=True)
    db = sqlite3.connect(os.path.join(OUT, "annunci.sqlite"))
    db.execute("""CREATE TABLE IF NOT EXISTS annunci (id TEXT PRIMARY KEY, visto_il TEXT, titolo TEXT,
                  prezzo REAL, url TEXT, comune TEXT, provincia TEXT, categoria TEXT, punti INTEGER, json TEXT)""")
    return db


def main(argv):
    cfg_path = os.path.join(QUI, "scanner_config.json")
    if "--config" in argv:
        cfg_path = argv[argv.index("--config") + 1]
    massimo = int(argv[argv.index("--max") + 1]) if "--max" in argv else None
    cfg = carica_config(cfg_path)
    dati = json.load(open(router.CATALOGO, encoding="utf-8"))
    richieste = costruisci_richieste(cfg, massimo)
    db = apri_db()
    if "--da-archivio" in argv:
        # ricalcola il report dagli annunci già salvati, senza scaricare
        annunci = [json.loads(j) for (j,) in db.execute("SELECT json FROM annunci")]
        db.execute("DELETE FROM annunci")
    else:
        fonti = cfg.get("fonti", {"subito": True})
        annunci = []
        if fonti.get("subito", True):
            sys.stderr.write(f"Subito: {len(richieste)} pagine da scaricare (ritmo prudente)...\n")
            annunci += scarica(richieste)
        q_extra = cfg["ricerche"] + cfg.get("ricerche_marchi", [])
        if massimo:
            q_extra = q_extra[:massimo]
        if fonti.get("wallapop"):
            annunci += fonti_extra.wallapop(q_extra, cfg.get("wallapop", {}), set(cfg.get("province_ritiro_nomi", [])),
                                            set(cfg.get("regioni_ritiro", [])))
        if fonti.get("vinted"):
            annunci += fonti_extra.vinted(q_extra, cfg.get("vinted", {}))
    unici = {}
    for a in annunci:  # lo stesso annuncio può uscire da più ricerche o fonti
        unici.setdefault(a["id"], a)
    annunci = list(unici.values())
    # già visti: archivio locale + memoria nel repository (sopravvive alle sessioni) + già periziati
    in_archivio = {r[0] for r in db.execute("SELECT id FROM annunci")}
    # già visti: archivio locale + memoria nel repository (vale anche nelle sessioni nuove) + già periziati.
    # Con --da-archivio l'archivio è appena stato svuotato e visti.txt li conterrebbe tutti: si escludono solo i periziati.
    visti = in_archivio | memoria.ids_periziati()
    if "--da-archivio" not in argv:
        visti |= memoria.visti()
    bonus = memoria.lezioni(testo=False)["bonus"]
    adesso = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    nuovi, righe = 0, []
    ritiro = set(cfg.get("province_ritiro", []))
    no_sped = [norm(x) for x in cfg.get("segnali", {}).get("solo_ritiro", [])]
    scartati_distanza = 0
    for a in annunci:
        testo_n = f" {norm(a['titolo'])} {norm(a['testo'])} "
        if any(f" {x} " in testo_n for x in no_sped) or (" ritiro " in testo_n and " sped" not in testo_n):
            a["spedizione"] = False  # il venditore scrive che non spedisce, o parla solo di ritiro
        locale = a.get("locale", a.get("provincia") in ritiro)
        if a.get("riservato"):
            continue  # già riservato a un altro acquirente
        if ritiro and not a.get("spedizione") and not locale:
            scartati_distanza += 1  # solo ritiro a mano, ma troppo lontano
            continue
        cat = router.classifica(f"{a['titolo']} {a['testo']}", dati)
        punti, motivi = punteggio(a, cat, cfg, bonus)
        a["categoria"] = cat[0][1]["id"] if cat else ""
        a["punti"], a["motivi"] = punti, motivi
        if a["id"] not in in_archivio:
            db.execute("INSERT INTO annunci VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (a["id"], adesso, a["titolo"], a["prezzo"], a["url"], a["comune"], a["provincia"],
                        a["categoria"], punti, json.dumps(a, ensure_ascii=False)))
        if a["id"] not in visti:
            nuovi += 1
            righe.append(a)
        elif "--anche-visti" in argv:
            righe.append(a)
    db.commit()
    memoria.aggiungi_visti([a["id"] for a in annunci])
    righe.sort(key=lambda x: (-x["punti"], x["prezzo"] or 0))
    soglia = cfg["segnali"]["punti_minimi_report"]
    da_guardare = [a for a in righe if a["punti"] >= soglia][: cfg["segnali"].get("max_report", 50)]
    nome = os.path.join(OUT, "report-" + dt.datetime.now().strftime("%Y-%m-%d-%H%M") + ".md")
    with open(nome, "w", encoding="utf-8") as fh:
        fh.write(f"# Scanner Subito — {adesso}\n\n")
        fh.write(f"Zone: {', '.join(z['nome'] for z in cfg['zone'])} · pagine: {len(richieste)} · "
                 f"annunci letti: {len(annunci)} · scartati perché solo ritiro e lontani: {scartati_distanza} · nuovi: {nuovi} · da guardare (punti ≥ {soglia}): {len(da_guardare)}\n\n")
        fh.write("Il punteggio ordina cosa guardare prima; non è una stima di valore.\n\n")
        fh.write("| # | Punti | Prezzo | Titolo | Luogo | Categoria | Perché |\n|---|---|---|---|---|---|---|\n")
        for i, a in enumerate(da_guardare, 1):
            prezzo = f"{a['prezzo']:.0f} €" if a["prezzo"] else "—"
            titolo = a["titolo"].replace("|", "/")[:70]
            fh.write(f"| {i} | {a['punti']} | {prezzo} | [{titolo}]({a['url']}) | {a.get('fonte', 'Subito')} · {a['comune']} ({a['provincia']}){' 📦' if a.get('spedizione') else ' 🤝'} | "
                     f"{a['categoria'] or '?'} | {'; '.join(a['motivi'])[:160]} |\n")
    with open(nome.replace(".md", ".json"), "w", encoding="utf-8") as fh:
        json.dump(da_guardare, fh, ensure_ascii=False, indent=1)
    if "--telegram" in argv:
        subprocess.run([sys.executable, os.path.join(QUI, "notifica_telegram.py")])
    print(f"Report: {nome}\nAnnunci letti {len(annunci)}, nuovi {nuovi}, da guardare {len(da_guardare)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
