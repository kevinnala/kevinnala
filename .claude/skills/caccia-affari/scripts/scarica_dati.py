#!/usr/bin/env python3
"""Costruisce in dati/ indici compatti di produttori e artisti da open data museali
(licenza CC0) pubblicati su GitHub:

  - Metropolitan Museum of Art (github.com/metmuseum/openaccess): ~480.000 oggetti.
    Il CSV (circa 340 MB) viene letto in streaming e NON salvato: si tiene solo un
    indice di chi ha fatto gli oggetti (artisti, manifatture, fonderie, argentieri...).
  - MoMA (github.com/MuseumofModernArt/collection): artisti e designer del '900.
  - Tate (github.com/tategallery/collection): artisti della collezione Tate.

Uso: python3 scarica_dati.py [--solo met|moma|tate]
"""
import collections
import csv
import io
import json
import os
import sys
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(QUI, "..", "dati")
UA = {"User-Agent": "caccia-affari-dati/1.0 (uso personale)"}
MET = "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv"
MOMA = "https://media.githubusercontent.com/media/MuseumofModernArt/collection/main/Artists.json"
TATE = "https://raw.githubusercontent.com/tategallery/collection/master/artist_data.csv"

csv.field_size_limit(10**8)


def apri(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600)


def pulisci(s):
    return " ".join((s or "").replace("\t", " ").split())


def top(counter, n=3):
    return "; ".join(k for k, _ in counter.most_common(n) if k)


def met():
    stat = {}
    with apri(MET) as r:
        lettore = csv.DictReader(io.TextIOWrapper(r, encoding="utf-8-sig", newline=""))
        for riga in lettore:
            nomi = (riga.get("Artist Display Name") or "").split("|")
            if not any(n.strip() for n in nomi):
                continue
            campi = {k: (riga.get(k) or "").split("|") for k in (
                "Artist Role", "Artist Display Bio", "Artist Nationality",
                "Artist Begin Date", "Artist End Date", "Artist ULAN URL")}
            for i, nome in enumerate(nomi):
                nome = pulisci(nome)
                if not nome:
                    continue
                s = stat.get(nome)
                if s is None:
                    s = stat[nome] = dict(
                        bio="", naz="", nascita="", morte="", ulan="",
                        ruoli=collections.Counter(), reparti=collections.Counter(),
                        oggetti=collections.Counter(), materiali=collections.Counter(),
                        luoghi=collections.Counter(), n=0, da=None, a=None)

                def campo(k):
                    v = campi[k]
                    return pulisci(v[i] if i < len(v) else "")

                for chiave, k in (("bio", "Artist Display Bio"), ("naz", "Artist Nationality"),
                                  ("nascita", "Artist Begin Date"), ("morte", "Artist End Date"),
                                  ("ulan", "Artist ULAN URL")):
                    if not s[chiave]:
                        s[chiave] = campo(k)
                s["ruoli"][campo("Artist Role")] += 1
                s["reparti"][pulisci(riga.get("Department"))] += 1
                s["oggetti"][pulisci(riga.get("Object Name"))] += 1
                s["materiali"][pulisci(riga.get("Medium"))[:60]] += 1
                s["luoghi"][pulisci(riga.get("City") or riga.get("Country") or riga.get("Culture"))] += 1
                s["n"] += 1
                for k, f in (("da", min), ("a", max)):
                    try:
                        v = int(riga.get("Object Begin Date" if k == "da" else "Object End Date") or "")
                        s[k] = v if s[k] is None else f(s[k], v)
                    except ValueError:
                        pass
    os.makedirs(DEST, exist_ok=True)
    out = os.path.join(DEST, "produttori-met.tsv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["nome", "bio", "nazionalita", "nascita_inizio", "morte_fine", "ruoli",
                    "n_oggetti", "date_oggetti", "tipi_oggetto", "materiali", "luoghi",
                    "reparti_met", "ulan"])
        for nome in sorted(stat, key=lambda x: x.lower()):
            s = stat[nome]
            date = f"{s['da']}–{s['a']}" if s["da"] is not None else ""
            w.writerow([nome, s["bio"], s["naz"], s["nascita"], s["morte"], top(s["ruoli"]),
                        s["n"], date, top(s["oggetti"]), top(s["materiali"]), top(s["luoghi"]),
                        top(s["reparti"], 2), s["ulan"]])
    print(f"Met: {len(stat)} produttori/artisti → {out}")


def moma():
    with apri(MOMA) as r:
        dati = json.load(r)
    out = os.path.join(DEST, "artisti-moma.tsv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["nome", "bio", "nazionalita", "nascita", "morte", "ulan", "wikidata"])
        for a in sorted(dati, key=lambda x: (x.get("DisplayName") or "").lower()):
            w.writerow([pulisci(a.get("DisplayName")), pulisci(a.get("ArtistBio")),
                        pulisci(a.get("Nationality")), a.get("BeginDate") or "",
                        a.get("EndDate") or "", a.get("ULAN") or "", a.get("Wiki QID") or ""])
    print(f"MoMA: {len(dati)} artisti e designer → {out}")


def tate():
    with apri(TATE) as r:
        righe = list(csv.DictReader(io.TextIOWrapper(r, encoding="utf-8-sig", newline="")))
    out = os.path.join(DEST, "artisti-tate.tsv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["nome", "date", "nascita", "morte", "luogo_nascita", "luogo_morte"])
        for a in righe:
            w.writerow([pulisci(a.get("name")), pulisci(a.get("dates")), a.get("yearOfBirth") or "",
                        a.get("yearOfDeath") or "", pulisci(a.get("placeOfBirth")),
                        pulisci(a.get("placeOfDeath"))])
    print(f"Tate: {len(righe)} artisti → {out}")


if __name__ == "__main__":
    os.makedirs(DEST, exist_ok=True)
    scelta = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
    for nome, f in (("moma", moma), ("tate", tate), ("met", met)):
        if scelta in (None, nome):
            f()
