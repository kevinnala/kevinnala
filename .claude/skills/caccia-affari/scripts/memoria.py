#!/usr/bin/env python3
"""Memoria permanente della caccia agli affari (salvata nel repository, non in risultati/).

  memoria/visti.txt        id degli annunci già passati dallo scanner (uno per riga)
  memoria/periziati.jsonl  una riga per ogni perizia mandata su Telegram (con numero #N)
  memoria/esiti.jsonl      cosa l'utente ha comprato, venduto o scartato (dai messaggi Telegram)
  memoria/stato.json       contatore delle perizie e offset dei messaggi Telegram
  memoria/coda.jsonl       annunci interessanti non ancora periziati, da periziare a blocchi su richiesta

Uso da riga di comando:
  memoria.py lezioni     # cosa insegnano gli esiti: categorie che rendono, stime troppo alte o basse
  memoria.py bilancio    # elenco acquisti e vendite con utile
  memoria.py coda        # quanti annunci aspettano la perizia (coda da vedere a blocchi)
"""
import datetime as dt
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.normpath(os.path.join(QUI, "..", "memoria"))
F_VISTI = os.path.join(MEM, "visti.txt")
F_PERIZIATI = os.path.join(MEM, "periziati.jsonl")
F_ESITI = os.path.join(MEM, "esiti.jsonl")
F_STATO = os.path.join(MEM, "stato.json")
F_CODA = os.path.join(MEM, "coda.jsonl")
GIORNI_CODA = 21  # gli annunci più vecchi escono dalla coda (probabilmente venduti)
CAMPI_CODA = ("id", "titolo", "testo", "prezzo", "url", "fonte", "comune", "provincia", "locale", "spedizione",
              "categoria", "punti", "motivi", "foto", "n_foto", "condizione", "data", "termine", "tribunale",
              "prezzo_con_oneri", "k")


def _jsonl(percorso):
    if not os.path.exists(percorso):
        return []
    with open(percorso, encoding="utf-8") as fh:
        return [json.loads(r) for r in fh if r.strip()]


def _aggiungi(percorso, righe):
    os.makedirs(MEM, exist_ok=True)
    with open(percorso, "a", encoding="utf-8") as fh:
        for r in righe:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def oggi():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


# --- annunci visti -------------------------------------------------------------
def visti():
    if not os.path.exists(F_VISTI):
        return set()
    with open(F_VISTI, encoding="utf-8") as fh:
        return {r.strip() for r in fh if r.strip()}


def aggiungi_visti(ids):
    gia = visti()
    nuovi = sorted(set(ids) - gia)
    if nuovi:
        os.makedirs(MEM, exist_ok=True)
        with open(F_VISTI, "a", encoding="utf-8") as fh:
            fh.write("".join(i + "\n" for i in nuovi))
    return len(nuovi)


# --- stato ---------------------------------------------------------------------
def stato():
    if os.path.exists(F_STATO):
        with open(F_STATO, encoding="utf-8") as fh:
            return json.load(fh)
    return {"ultimo_numero": 0, "telegram_offset": 0}


def salva_stato(s):
    os.makedirs(MEM, exist_ok=True)
    with open(F_STATO, "w", encoding="utf-8") as fh:
        json.dump(s, fh, ensure_ascii=False, indent=1)


# --- perizie -------------------------------------------------------------------
def periziati():
    return _jsonl(F_PERIZIATI)


def ids_periziati():
    return {p["id"] for p in periziati()}


def registra_perizie(perizie):
    """Assegna a ogni perizia un numero progressivo stabile (#N) e la salva."""
    s = stato()
    for p in perizie:
        s["ultimo_numero"] += 1
        p["n"] = s["ultimo_numero"]
        p.setdefault("data", oggi())
    _aggiungi(F_PERIZIATI, perizie)
    salva_stato(s)
    return perizie


def trova_perizia(rif):
    """rif = numero (#12 o 12), id dell'annuncio o link."""
    rif = str(rif).strip().lstrip("#")
    for p in reversed(periziati()):
        if rif.isdigit() and p.get("n") == int(rif):
            return p
        if rif == p["id"] or (p.get("url") and p["url"] in rif):
            return p
        codice = p["id"].split(":")[-1].split("-")[-1]
        if len(codice) >= 6 and codice in rif:
            return p
    return None


# --- coda: annunci interessanti non ancora periziati, da vedere a blocchi -------
PRIORITA = {"scelti": 0, "parole": 1, "griglie": 2}


def coda():
    """Coda senza i già periziati e senza gli annunci troppo vecchi, in ordine di priorità."""
    gia = ids_periziati()
    limite = (dt.datetime.now() - dt.timedelta(days=GIORNI_CODA)).strftime("%Y-%m-%d")
    per_id = {}
    for a in _jsonl(F_CODA):
        if a["id"] in gia or (a.get("aggiunto") or "") < limite:
            continue
        vecchio = per_id.get(a["id"])
        if not vecchio or PRIORITA.get(a["origine"], 9) < PRIORITA.get(vecchio["origine"], 9):
            per_id[a["id"]] = a
    return sorted(per_id.values(), key=lambda a: (PRIORITA.get(a["origine"], 9), -(a.get("punti") or 0),
                                                   a.get("prezzo") or 0))


def aggiungi_coda(annunci, origine):
    """origine: 'scelti' (scelti a occhio nelle griglie), 'parole' (scanner per parole), 'griglie'."""
    gia = ids_periziati()
    righe = []
    for a in annunci:
        if a["id"] in gia:
            continue
        r = {k: a.get(k) for k in CAMPI_CODA if a.get(k) not in (None, "", [])}
        r["testo"] = (r.get("testo") or "")[:500]
        r["origine"], r["aggiunto"] = origine, oggi()
        righe.append(r)
    _aggiungi(F_CODA, righe)
    return len(righe)


def pulisci_coda():
    """Riscrive la coda tenendo solo ciò che serve (da chiamare ogni tanto)."""
    tenuti = coda()
    os.makedirs(MEM, exist_ok=True)
    with open(F_CODA, "w", encoding="utf-8") as fh:
        for a in tenuti:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")
    return len(tenuti)


# --- esiti ---------------------------------------------------------------------
def esiti():
    return _jsonl(F_ESITI)


def registra_esito(e):
    e.setdefault("data", oggi())
    _aggiungi(F_ESITI, [e])


def _per_numero():
    """Ricostruisce, per ogni perizia, acquisto e vendita dichiarati dall'utente."""
    per = {p["n"]: {"perizia": p} for p in periziati()}
    note = []
    for e in esiti():
        n = e.get("n")
        if n is None or n not in per:
            note.append(e)
            continue
        per[n].setdefault("eventi", []).append(e)
        if e["tipo"] == "preso":
            per[n]["preso"] = e.get("prezzo")
        elif e["tipo"] == "venduto":
            per[n]["venduto"] = e.get("prezzo")
            per[n]["canale"] = e.get("canale")
        elif e["tipo"] in ("scartato", "perso"):
            per[n]["scartato"] = e.get("testo") or e["tipo"]
    return per, note


def lezioni(testo=True):
    """Statistiche per categoria + bonus di punteggio da dare allo scanner."""
    per, note = _per_numero()
    cat = {}
    for n, r in per.items():
        p = r["perizia"]
        c = cat.setdefault(p.get("categoria") or "?", {"periziati": 0, "presi": 0, "venduti": 0, "utile": 0.0,
                                                         "rapporti": [], "canali": {}, "scartati": 0})
        c["periziati"] += 1
        if r.get("preso") is not None:
            c["presi"] += 1
        if r.get("scartato"):
            c["scartati"] += 1
        if r.get("venduto") is not None:
            c["venduti"] += 1
            utile = r["venduto"] - (r.get("preso") or 0)
            c["utile"] += utile
            stima = (p.get("valore") or [None, None, None])[1]
            if stima:
                c["rapporti"].append(r["venduto"] / stima)
            if r.get("canale"):
                c["canali"][r["canale"]] = c["canali"].get(r["canale"], 0) + utile
    bonus = {}
    for nome, c in cat.items():
        if c["venduti"]:
            bonus[nome] = 2 if c["utile"] > 0 else -2
        elif c["presi"]:
            bonus[nome] = 1
    if not testo:
        return {"categorie": cat, "bonus": bonus, "note": note}
    righe = []
    for nome, c in sorted(cat.items(), key=lambda x: -x[1]["utile"]):
        if not (c["presi"] or c["venduti"] or c["scartati"]):
            continue
        r = f"- {nome}: periziati {c['periziati']}, presi {c['presi']}, venduti {c['venduti']}, utile {c['utile']:.0f} €"
        if c["rapporti"]:
            media = sum(c["rapporti"]) / len(c["rapporti"])
            r += f", venduto/stima probabile = {media:.2f}" + (" (stime troppo alte: abbassale)" if media < 0.85 else
                                                                 " (stime prudenti: puoi alzarle)" if media > 1.2 else "")
        if c["canali"]:
            r += ", canale migliore: " + max(c["canali"], key=c["canali"].get)
        righe.append(r)
    if not righe and not note:
        return "Nessun esito ancora: l'utente non ha segnalato acquisti o vendite."
    out = ["Lezioni dagli esiti dell'utente:"] + (righe or ["- nessun acquisto o vendita collegati a una perizia"])
    if bonus:
        out.append("Bonus di punteggio nello scanner: " + ", ".join(f"{k} {v:+d}" for k, v in bonus.items()))
    if note:
        out.append("Note libere dell'utente (leggile prima di periziare):")
        out += [f"- [{e['data']}] {e.get('testo', '')}" + (f"  (in risposta a: «{e['risposta_a'][:120]}»)" if e.get("risposta_a") else "")
                for e in note[-20:]]
    return "\n".join(out)


def bilancio():
    per, _ = _per_numero()
    righe, tot_spesa, tot_incasso = [], 0.0, 0.0
    for n, r in sorted(per.items()):
        if r.get("preso") is None and r.get("venduto") is None:
            continue
        p = r["perizia"]
        spesa, incasso = r.get("preso") or 0, r.get("venduto")
        tot_spesa += spesa
        stato_r = f"venduto {incasso:.0f} € ({r.get('canale') or '?'}) → utile {incasso - spesa:+.0f} €" if incasso is not None \
            else "in magazzino"
        if incasso is not None:
            tot_incasso += incasso
        righe.append(f"#{n} {p['titolo'][:45]} · preso {spesa:.0f} € · {stato_r}")
    if not righe:
        return "Nessun acquisto registrato."
    venduti_spesa = sum((r.get("preso") or 0) for r in per.values() if r.get("venduto") is not None)
    righe.append(f"Totale: speso {tot_spesa:.0f} €, incassato {tot_incasso:.0f} €, "
                 f"utile sui venduti {tot_incasso - venduti_spesa:+.0f} €")
    return "\n".join(righe)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "lezioni"
    if cmd == "coda":
        c = coda()
        print(f"In coda: {len(c)} annunci (scelti {sum(a['origine'] == 'scelti' for a in c)}, "
              f"per parole {sum(a['origine'] == 'parole' for a in c)}, dalle griglie {sum(a['origine'] == 'griglie' for a in c)})")
    else:
        print(bilancio() if cmd == "bilancio" else lezioni())
