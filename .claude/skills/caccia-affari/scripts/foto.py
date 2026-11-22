#!/usr/bin/env python3
"""Scarica testo completo e foto di annunci Subito per la valutazione.

Uso: foto.py <url-annuncio> [<url-annuncio> ...] [--max-foto 6]

Per ogni annuncio crea risultati/foto/<id>/ con scheda.json e 1.jpg, 2.jpg, ...
Le foto si guardano poi con lo strumento di lettura immagini (Read).
"""
import json
import os
import subprocess
import sys
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, "..", "risultati", "foto")


def converti_in_jpeg(percorso):
    """Alcune foto arrivano in AVIF anche se si chiede JPEG: convertile, se Pillow lo permette."""
    with open(percorso, "rb") as fh:
        testa = fh.read(12)
    if testa[4:8] != b"ftyp":
        return
    try:
        from PIL import Image
        with Image.open(percorso) as im:
            im.convert("RGB").save(percorso, "JPEG", quality=90)
    except Exception as e:  # noqa: BLE001
        print("  foto in formato AVIF non convertita:", percorso, e)


def main(argv):
    massimo = int(argv[argv.index("--max-foto") + 1]) if "--max-foto" in argv else 6
    urls = [a for a in argv if a.startswith("http")]
    if not urls:
        print(__doc__)
        return 2
    proc = subprocess.run(["node", os.path.join(QUI, "subito_annuncio.js"), *urls],
                          capture_output=True, text=True, timeout=600)
    for riga in proc.stdout.splitlines():
        a = json.loads(riga)
        if a.get("errore") or not a.get("id"):
            print("ERRORE", a.get("url"), a.get("errore", "annuncio non trovato (rimosso?)"))
            continue
        cartella = os.path.join(OUT, a["id"])
        os.makedirs(cartella, exist_ok=True)
        salvate = []
        for i, u in enumerate(a["foto"][:massimo], 1):
            dest = os.path.join(cartella, f"{i}.jpg")
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Accept": "image/jpeg,image/*;q=0.5"})
                with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as fh:
                    fh.write(r.read())
                converti_in_jpeg(dest)
                salvate.append(dest)
            except Exception as e:  # noqa: BLE001
                print("  foto non scaricata:", u, e)
        a["foto_locali"] = salvate
        with open(os.path.join(cartella, "scheda.json"), "w", encoding="utf-8") as fh:
            json.dump(a, fh, ensure_ascii=False, indent=1)
        print(f"{a['id']}: {a['titolo']} — {len(salvate)}/{len(a['foto'])} foto in {os.path.normpath(cartella)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
