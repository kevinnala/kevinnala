#!/usr/bin/env python3
"""Instradatore: dal testo di un annuncio (titolo, descrizione) alla categoria giusta,
con la scheda essenziale e SOLO le righe dei file da leggere.

Uso:
  categoria.py "candeliere bronzo dorato firmato"     # scheda breve
  categoria.py --estratto "vecchie carte pokemon"     # anche il testo delle sezioni
  categoria.py --json "lotto 45 giri"                 # per lo scanner
  echo "testo" | categoria.py -                       # da stdin
  categoria.py --elenco                               # tutte le categorie

Nessuna dipendenza. Funziona con sinonimi in italiano, inglese, francese, tedesco ed
errori di battitura con lettere doppie (es. "vennini", "rollex").
"""
import glob
import json
import os
import re
import sys
import unicodedata

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, ".."))
REF = os.path.join(RADICE, "references")
CATALOGO = os.path.join(REF, "categorie.json")
TESTI = os.path.join(RADICE, "manuali", "testi")


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def dedup(s):
    return re.sub(r"(.)\1+", r"\1", s)


def punteggio(testo, cat):
    t1, t2 = f" {norm(testo)} ", None
    t2 = f" {dedup(t1.strip())} "
    trovate, viste = [], set()
    for p in cat["parole"]:
        n = norm(p)
        if not n or dedup(n) in viste:
            continue
        if f" {n} " in t1 or f" {dedup(n)} " in t2:
            trovate.append(p)
            viste.add(dedup(n))
    peso = sum(1 + n.count(" ") for n in map(norm, trovate)) * cat.get("peso", 1)
    return peso, trovate


def sezione(rif):
    """'file#titolo' -> (percorso relativo, riga inizio, riga fine) 1-based."""
    file, _, titolo = rif.partition("#")
    percorso = os.path.join(REF, file)
    with open(percorso, encoding="utf-8") as fh:
        righe = fh.read().split("\n")
    if not titolo:
        return file, 1, len(righe), righe
    t = norm(titolo)
    for i, r in enumerate(righe):
        m = re.match(r"^(#+)\s+(.*)", r)
        if m and norm(m.group(2)).startswith(t):
            livello = len(m.group(1))
            fine = len(righe)
            for j in range(i + 1, len(righe)):
                m2 = re.match(r"^(#+)\s", righe[j])
                if m2 and len(m2.group(1)) <= livello:
                    fine = j
                    break
            while fine > i + 1 and not righe[fine - 1].strip():
                fine -= 1
            return file, i + 1, fine, righe
    raise KeyError(f"sezione non trovata: {rif}")


def classifica(testo, dati):
    ris = []
    for c in dati["categorie"]:
        p, trovate = punteggio(testo, c)
        if p:
            ris.append((p, c, trovate))
    ris.sort(key=lambda x: -x[0])
    if not ris:
        return []
    migliore = ris[0][0]
    # tieni la seconda solo se è vicina (oggetti a cavallo: orologio in bronzo, icona in argento)
    return [r for r in ris[:2] if r[0] >= max(1, migliore * 0.6)]


def scheda(p, c, trovate, estratto=False):
    out = [f"## {c['nome']}  [{c['id']}]  (parole riconosciute: {', '.join(trovate)}; punteggio {p})"]
    out.append("Verifiche chiave:")
    out += [f"  - {v}" for v in c["verifiche"]]
    out.append("Foto da chiedere: " + "; ".join(c["foto"]))
    if c.get("rischi"):
        out.append("Rischi: " + "; ".join(c["rischi"]))
    out.append("Dove vendere: " + c["vendi"])
    out.append("Leggi SOLO queste righe (references/):")
    testi = []
    for rif in c["leggi"]:
        file, a, b, righe = sezione(rif)
        out.append(f"  - {file}:{a}-{b}  ({b - a + 1} righe)")
        if estratto:
            testi.append("\n".join(righe[a - 1:b]))
    man = []
    for pref in c.get("manuali", []):
        man += sorted(os.path.basename(f) for f in glob.glob(os.path.join(TESTI, pref + "*.txt")))
    if man:
        out.append("Manuali (cerca con grep -n -i -C3 \"<nome>\" manuali/testi/<file>): " + ", ".join(man))
    if c.get("dati") == "produttori-met":
        out.append("Dati: grep -i \"<produttore>\" dati/produttori-met.tsv  (date di attività, ruolo, oggetti)")
    elif c.get("dati") == "artisti":
        out.append("Dati: grep -i \"<nome>\" dati/produttori-met.tsv dati/artisti-moma.tsv dati/artisti-tate.tsv")
    if estratto:
        out.append("\n--- estratto ---\n" + "\n\n".join(testi))
    return "\n".join(out)


def main(argv):
    with open(CATALOGO, encoding="utf-8") as fh:
        dati = json.load(fh)
    if "--elenco" in argv:
        for c in dati["categorie"]:
            print(f"{c['id']:22} {c['nome']}")
        return 0
    estratto = "--estratto" in argv
    come_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    testo = sys.stdin.read() if args == ["-"] else " ".join(args)
    if not testo.strip():
        print(__doc__)
        return 2
    ris = classifica(testo, dati)
    if come_json:
        print(json.dumps([{"id": c["id"], "nome": c["nome"], "punteggio": p, "parole": t}
                          for p, c, t in ris], ensure_ascii=False))
        return 0
    if not ris:
        print("Categoria non riconosciuta. Non tirare a indovinare: chiedi o deduci cos'è "
              "l'oggetto (materiale, funzione), poi usa references/nuova-categoria.md.")
        return 1
    print("\n\n".join(scheda(p, c, t, estratto) for p, c, t in ris))
    if len(ris) > 1:
        print("\n(Due categorie plausibili: l'oggetto può stare a cavallo; usa la prima, "
              "aggiungi della seconda solo ciò che serve.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
