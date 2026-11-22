#!/usr/bin/env python3
"""Scarica da archive.org il testo completo (OCR) di manuali di dominio pubblico
e lo salva in manuali/testi/ come file .txt ricercabili.

Uso:  python3 scarica_manuali.py            # scarica quelli mancanti
      python3 scarica_manuali.py --tutti    # riscarica tutto
      python3 scarica_manuali.py --elenco   # mostra il catalogo

Serve accesso di rete ad archive.org. Le immagini (marchi, punzoni, tavole) non sono
nel testo: per vederle apri il PDF al link indicato in testa a ogni file.
"""
import html
import os
import re
import sys
import time
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(QUI, "..", "manuali", "testi")

# (file, identificativo archive.org, titolo, autore, anno, categoria, diritti)
CATALOGO = [
    ("ceramica-chaffers-marks-and-monograms-1908", "marksmonogram00chaf",
     "Marks and Monograms on European and Oriental Pottery and Porcelain (12a ed.)",
     "William Chaffers (1811-1892), rev. Frederick Litchfield (1850-1930)", 1908, "ceramica",
     "dominio pubblico (autori morti da oltre 70 anni, pubblicato prima del 1930)"),
    ("ceramica-de-mauri-amatore-maioliche-porcellane-1899", "lamatoredimaiol00demgoog",
     "L'amatore di maioliche e porcellane (Manuali Hoepli)",
     "Luigi De Mauri (pseud. di Ernesto Sarasino)", 1899, "ceramica",
     "dominio pubblico (pubblicato nel 1899)"),
    ("ceramica-corona-la-ceramica-1879", "laceramicabiogra00coro",
     "La ceramica: biografie e note storiche", "Giuseppe Corona", 1879, "ceramica",
     "dominio pubblico (pubblicato nel 1879)"),
    ("ceramica-litchfield-pottery-and-porcelain-1900", "potteryporcelai00litc",
     "Pottery and Porcelain: a Guide to Collectors", "Frederick Litchfield (1850-1930)", 1900,
     "ceramica", "dominio pubblico"),
    ("arte-orientale-hobson-chinese-pottery-vol1-1915", "chinesepotterypo01hobs",
     "Chinese Pottery and Porcelain, vol. 1", "R. L. Hobson (1872-1941)", 1915, "arte orientale",
     "dominio pubblico (autore morto nel 1941)"),
    ("arte-orientale-hobson-chinese-pottery-vol2-1915", "chinesepotterypo02hobs",
     "Chinese Pottery and Porcelain, vol. 2 (con i marchi di regno)", "R. L. Hobson (1872-1941)",
     1915, "arte orientale", "dominio pubblico (autore morto nel 1941)"),
    ("argento-jackson-english-goldsmiths-1905", "cu31924030681757",
     "English Goldsmiths and their Marks", "Charles James Jackson (1849-1923)", 1905, "argento",
     "dominio pubblico"),
    ("argento-rosenberg-goldschmiede-merkzeichen-1922", "dergoldschmiede00rosegoog",
     "Der Goldschmiede Merkzeichen (punzoni europei, anche italiani)",
     "Marc Rosenberg (1852-1930)", 1922, "argento", "dominio pubblico"),
    ("metalli-masse-chats-on-old-pewter-1911", "chatsonoldpewter00mass",
     "Chats on Old Pewter", "H. J. L. J. Massé (1860-1936)", 1911, "metalli", "dominio pubblico"),
    ("metalli-burgess-chats-on-old-copper-and-brass-1914", "chatsonoldcopper00burg",
     "Chats on Old Copper and Brass", "Fred. W. Burgess (1855-1945)", 1914, "metalli",
     "dominio pubblico (autore morto nel 1945)"),
    ("vetro-dillon-glass-1907", "glass00dill", "Glass", "Edward Dillon (m. 1914)", 1907, "vetro",
     "dominio pubblico"),
    ("orologi-britten-old-clocks-and-watches-1911", "oldclockswatches00brit_0",
     "Old Clocks and Watches and their Makers (3a ed., con elenco di orologiai)",
     "F. J. Britten (1843-1913)", 1911, "orologi", "dominio pubblico"),
    ("mobili-litchfield-history-of-furniture-1903", "illustratedhisto00litcrich",
     "Illustrated History of Furniture", "Frederick Litchfield (1850-1930)", 1903, "mobili",
     "dominio pubblico"),
    ("tappeti-mumford-oriental-rugs-1915", "orientalrugsmum00mumf",
     "Oriental Rugs", "John Kimberly Mumford (1863-1926)", 1915, "tappeti", "dominio pubblico"),
    ("dipinti-de-gubernatis-dizionario-artisti-italiani-viventi-1889", "dizionariodeglia00degu",
     "Dizionario degli artisti italiani viventi: pittori, scultori e architetti",
     "Angelo De Gubernatis (1840-1913)", 1889, "dipinti",
     "dominio pubblico (gli artisti dell'Ottocento italiano attivi nel 1889)"),
    ("numismatica-ambrosoli-manuale-numismatica-1891", "numismatica00ambrgoog",
     "Numismatica (Manuali Hoepli)", "Solone Ambrosoli (1851-1906)", 1891, "numismatica",
     "dominio pubblico"),
    ("numismatica-ambrosoli-atlante-numismatico-italiano-1906", "atlantenumismat00goog",
     "Atlante numismatico italiano: monete moderne (Manuali Hoepli)", "Solone Ambrosoli (1851-1906)",
     1906, "numismatica", "dominio pubblico"),
    ("numismatica-ambrosoli-vocabolarietto-7-lingue-1897", "vocabolariettope1897ambr",
     "Vocabolarietto pei numismatici in 7 lingue", "Solone Ambrosoli (1851-1906)", 1897,
     "numismatica", "dominio pubblico"),
    ("numismatica-gnecchi-monete-romane-1896", "moneteromaneman00gnecgoog",
     "Monete romane: manuale elementare (Manuali Hoepli)", "Francesco Gnecchi (1847-1919)", 1896,
     "numismatica", "dominio pubblico"),
    ("armi-gelli-guida-raccoglitore-armi-antiche-1900", "gelli-guida-raccoglitore-amatore-armi",
     "Guida del raccoglitore e dell'amatore di armi antiche (Manuali Hoepli)",
     "Jacopo Gelli (1858-1935)", 1900, "armi e militaria", "dominio pubblico",
     "GelliGuidaRaccoglitoreAmatoreArmi"),
    ("stili-melani-distinguere-stili-legni-metalli-1919", "lartedidistingue00mela",
     "L'arte di distinguere gli stili: legni e metalli (mobili, ferri, bronzi...) (Manuali Hoepli)",
     "Alfredo Melani (1859-1928)", 1919, "stili ed epoche", "dominio pubblico"),
    ("stili-melani-distinguere-stili-architettura-decorativa-1918", "lartedidistingue00mela_0",
     "L'arte di distinguere gli stili: architettura, scultura applicata, arte decorativa (Manuali Hoepli)",
     "Alfredo Melani (1859-1928)", 1918, "stili ed epoche", "dominio pubblico"),
    ("stili-melani-manuale-arte-decorativa-1907", "manualedartedeco00mela",
     "Manuale d'arte decorativa antica e moderna", "Alfredo Melani (1859-1928)", 1907,
     "stili ed epoche", "dominio pubblico"),
    ("stili-meyer-handbook-of-ornament-1900", "handbookoforname1900meye",
     "Handbook of Ornament (3.000 ornamenti di tutte le epoche)", "Franz Sales Meyer (1849-1927)", 1900,
     "stili ed epoche", "dominio pubblico"),
    ("oggetti-de-mauri-amatore-oggetti-arte-curiosita-1922", "lamatoredioggett00dema",
     "L'amatore di oggetti d'arte e di curiosità (Manuali Hoepli)",
     "Luigi De Mauri (pseud. di Ernesto Sarasino)", 1922, "oggetti d'arte di ogni epoca",
     "dominio pubblico"),
    ("gioielli-davenport-jewellery-1905", "jewellery00davegoog", "Jewellery",
     "Cyril Davenport (1848-1941)", 1905, "gioielli", "dominio pubblico (autore morto nel 1941)"),
    ("tribale-guillaume-munro-primitive-negro-sculpture-1926", "primitivenegros00guil",
     "Primitive Negro Sculpture (stili e zone della scultura africana, vecchie collezioni)",
     "Paul Guillaume (1891-1934) e Thomas Munro (1897-1974)", 1926, "arte africana",
     "dominio pubblico negli USA (pubblicato a New York nel 1926); il coautore Munro è morto "
     "nel 1974, quindi fuori dagli USA può essere ancora protetto: solo uso personale"),
    ("nativi-matthews-navajo-weavers-1884", "navajoweavers00matt",
     "Navajo Weavers (3rd Annual Report of the Bureau of Ethnology)",
     "Washington Matthews (1843-1905)", 1884, "nativi americani",
     "dominio pubblico (pubblicazione del governo USA, autore morto nel 1905)"),
    ("nativi-james-indian-blankets-1914", "indianblanketsth00jameuoft",
     "Indian Blankets and their Makers (coperte Navajo, Pueblo, Chimayó; falsi e imitazioni)",
     "George Wharton James (1858-1923)", 1914, "nativi americani", "dominio pubblico"),
    ("nativi-mason-aboriginal-american-basketry-1904", "aboriginalbasket00masorich",
     "Aboriginal American Basketry: Studies in a Textile Art Without Machinery",
     "Otis Tufton Mason (1838-1908)", 1904, "nativi americani",
     "dominio pubblico (pubblicazione del governo USA, autore morto nel 1908)"),
    ("nativi-fewkes-hopi-katcinas-1903", "hopikatcinasdraw00fewk",
     "Hopi Katcinas Drawn by Native Artists (21st Annual Report of the Bureau of American Ethnology)",
     "Jesse Walter Fewkes (1850-1930)", 1903, "nativi americani",
     "dominio pubblico (pubblicazione del governo USA, autore morto nel 1930)"),
    ("ceramica-barber-marks-of-american-potters-1904", "marksamericanpo00barbgoog",
     "Marks of American Potters (Rookwood, Grueby, Van Briggle, Newcomb e centinaia di altri)",
     "Edwin Atlee Barber (1851-1916)", 1904, "ceramica", "dominio pubblico"),
    ("mobili-stickley-catalogue-craftsman-furniture-1910", "catalogueofcr00stic",
     "Catalogue of Craftsman Furniture made by Gustav Stickley (numeri di modello, marchi)",
     "Gustav Stickley (1858-1942)", 1910, "mobili", "dominio pubblico (pubblicato nel 1910 negli USA)"),
    ("scultura-de-kay-barye-life-and-works-1889", "baryelifeworksof00deka",
     "Barye: Life and Works of Antoine Louis Barye (con elenco dei bronzi)",
     "Charles De Kay (1848-1935)", 1889, "scultura e bronzi",
     "dominio pubblico (autore morto nel 1935)"),
]
# Un ottavo campo facoltativo indica il nome del file su archive.org quando non
# coincide con l'identificativo.

UA = {"User-Agent": "caccia-affari-manuali/1.0 (uso personale)"}


def scarica(ident, base=None):
    url = f"https://archive.org/stream/{ident}/{base or ident}_djvu.txt"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        pagina = r.read().decode("utf-8", "replace")
    m = re.search(r"<pre[^>]*>(.*?)</pre>", pagina, re.S)
    if not m:
        raise RuntimeError("testo OCR non trovato")
    return html.unescape(m.group(1)).strip()


def main():
    if "--elenco" in sys.argv:
        for f, ident, tit, aut, anno, cat, *_ in CATALOGO:
            print(f"{cat:16} {anno}  {tit} — {aut}  [{ident}]")
        return 0
    os.makedirs(DEST, exist_ok=True)
    errori = 0
    for f, ident, tit, aut, anno, cat, dir_, *base in CATALOGO:
        percorso = os.path.join(DEST, f + ".txt")
        if os.path.exists(percorso) and "--tutti" not in sys.argv:
            print("già presente:", f)
            continue
        try:
            testo = scarica(ident, base[0] if base else None)
        except Exception as e:  # noqa: BLE001
            print("ERRORE", f, e)
            errori += 1
            continue
        testa = (f"Titolo: {tit}\nAutore: {aut}\nAnno: {anno}\nCategoria: {cat}\n"
                 f"Diritti: {dir_}\nFonte: https://archive.org/details/{ident}\n"
                 f"PDF con le immagini: https://archive.org/download/{ident}\n"
                 "Nota: testo OCR automatico; marchi e tavole sono immagini, guardali nel PDF.\n"
                 + "=" * 78 + "\n\n")
        with open(percorso, "w", encoding="utf-8") as fh:
            fh.write(testa + testo + "\n")
        print(f"ok  {f}  ({len(testo) // 1000} mila caratteri)")
        time.sleep(2)
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
