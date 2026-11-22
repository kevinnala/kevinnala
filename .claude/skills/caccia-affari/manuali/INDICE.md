# Biblioteca dei manuali (dominio pubblico)

In `testi/` ci sono 26 manuali classici per collezionisti in testo completo, scaricati
da archive.org con `scripts/scarica_manuali.py`. Sono tutti di **dominio pubblico**
(pubblicati prima del 1930 e/o con autori morti da oltre 70 anni). In testa a ogni file:
titolo, autore, anno, diritti, link alla scheda e al PDF.

## Avvertenze: come usarli bene

- **Sono libri di 100–150 anni fa.** Ottimi per marchi, punzoni, manifatture, biografie
  di artisti e artigiani, tecniche e storia. **Inutili per i prezzi** (vecchi di un secolo)
  e talvolta superati nelle attribuzioni: incrocia sempre con fonti recenti.
- **I marchi disegnati sono immagini**: nel testo trovi nomi, luoghi, date e descrizioni
  dei marchi, non il disegno. Per vedere il marchio apri il PDF al link in testa al file
  e vai alla pagina indicata.
- **Il testo è un OCR automatico**: ci sono errori di lettura (lettere scambiate,
  parole spezzate dall'a capo). Cerca con parole parziali e varianti.
- I falsi esistevano già allora: molti di questi libri descrivono anche le imitazioni
  ottocentesche (Samson, falsi Sèvres e Meissen). Leggi quei passi.

## Come cercare

```bash
cd .claude/skills/caccia-affari/manuali/testi
grep -il "ginori" *.txt                       # quali libri ne parlano
grep -n -i -C3 "ginori" ceramica-*.txt | less # i passi, con 3 righe di contesto
grep -n -i "capodimonte" ceramica-de-mauri*   # un libro solo
grep -n -i "fattori" dipinti-de-gubernatis*   # un pittore dell'Ottocento
```

Claude fa lo stesso con lo strumento di ricerca: prima i nomi (manifattura, autore,
città), poi le parole del marchio ("ancora", "corona", "spade incrociate", "stella").

## Quale libro per cosa

| Serve | File (in `testi/`) | Lingua |
|---|---|---|
| Marchi di **porcellane e maioliche europee e orientali** (oltre 3.500 marchi, con storia delle manifatture) | `ceramica-chaffers-marks-and-monograms-1908` | inglese |
| **Maioliche e porcellane italiane**: manifatture, marchi, storia, falsi (Manuale Hoepli) | `ceramica-de-mauri-amatore-maioliche-porcellane-1899` | italiano |
| Biografie di ceramisti e note sulle fabbriche italiane | `ceramica-corona-la-ceramica-1879` | italiano |
| Guida generale per collezionisti di ceramica, con marchi | `ceramica-litchfield-pottery-and-porcelain-1900` | inglese |
| **Porcellane cinesi**: periodi, tipi, decori; il vol. 2 ha i **marchi di regno** e i marchi apocrifi | `arte-orientale-hobson-chinese-pottery-vol1-1915`, `...-vol2-1915` | inglese |
| **Punzoni inglesi, scozzesi e irlandesi**: lettere dell'anno, città, oltre 11.000 marchi di argentieri | `argento-jackson-english-goldsmiths-1905` | inglese |
| **Punzoni europei** (Germania, Francia, Italia, ecc.) su oggetti antichi in oro e argento | `argento-rosenberg-goldschmiede-merkzeichen-1922` | tedesco |
| **Peltro**: marchi, tipi, falsi | `metalli-masse-chats-on-old-pewter-1911` | inglese |
| **Rame e ottone**: candelieri, oggetti domestici, come datarli | `metalli-burgess-chats-on-old-copper-and-brass-1914` | inglese |
| **Vetro** antico, Venezia e Murano compresi | `vetro-dillon-glass-1907` | inglese |
| **Orologi** e pendole: storia, meccanismi e un grande **elenco di orologiai** con date | `orologi-britten-old-clocks-and-watches-1911` | inglese |
| **Mobili**: stili, epoche, falsi | `mobili-litchfield-history-of-furniture-1903` | inglese |
| **Tappeti orientali**: tipi, provenienze, nodi, colori | `tappeti-mumford-oriental-rugs-1915` | inglese |
| **Pittori, scultori e architetti italiani dell'Ottocento** (attivi nel 1889): luoghi, opere, mostre | `dipinti-de-gubernatis-dizionario-artisti-italiani-viventi-1889` | italiano |
| **Numismatica** generale (Manuale Hoepli) | `numismatica-ambrosoli-manuale-numismatica-1891` | italiano |
| Monete italiane moderne (zecche, sovrani) | `numismatica-ambrosoli-atlante-numismatico-italiano-1906` | italiano |
| Termini numismatici in 7 lingue (per leggere cataloghi esteri) | `numismatica-ambrosoli-vocabolarietto-7-lingue-1897` | più lingue |
| **Monete romane** (Manuale Hoepli) | `numismatica-gnecchi-monete-romane-1896` | italiano |
| **Armi antiche**: tipi, epoche, armaioli, marchi (Manuale Hoepli) | `armi-gelli-guida-raccoglitore-armi-antiche-1900` | italiano |
| **Riconoscere gli stili e le epoche** di mobili, ferri, bronzi e altri metalli (Manuale Hoepli) | `stili-melani-distinguere-stili-legni-metalli-1919` | italiano |
| Riconoscere gli stili: architettura, scultura applicata, arti decorative (Manuale Hoepli) | `stili-melani-distinguere-stili-architettura-decorativa-1918` | italiano |
| Arte decorativa antica e moderna: ornati, materiali, tecniche per epoca | `stili-melani-manuale-arte-decorativa-1907` | italiano |
| **3.000 ornamenti di tutte le epoche** (per datare un decoro) | `stili-meyer-handbook-of-ornament-1900` | inglese |
| **Oggetti d'arte e di curiosità di ogni epoca**: cammei, tabacchiere, ventagli, avori, presepe, smalti, orologi, vetri... (Manuale Hoepli) | `oggetti-de-mauri-amatore-oggetti-arte-curiosita-1922` | italiano |
| **Gioielli** antichi: tipi, epoche, tecniche, pietre | `gioielli-davenport-jewellery-1905` | inglese |

## Cosa non c'è (e perché)

- **Manuali moderni** (Miller's, Kovels', Comanducci recente, Tardy, Bulgari, Kjellberg,
  Sassone, Gigante): protetti da diritto d'autore. Si comprano, oppure si consultano in
  biblioteca. Se li hai in PDF, mettili in questa cartella (`manuali/`, non in `testi/`).
- **Carte collezionabili, design, videogiochi, sneakers**: sono mercati recenti, senza
  manuali storici. Le fonti sono online (vedi `../references/canali-specializzati/`).
- **Leggi e regolamenti** (Codice dei beni culturali, metalli preziosi, CITES): i testi
  ufficiali sono su normattiva.it e eur-lex.europa.eu; la sintesi pratica è in
  `../references/legale-fiscale.md`.

## Altre biblioteche gratuite da consultare (uso personale)

- **MetPublications** del Metropolitan Museum (metmuseum.org): centinaia di cataloghi
  esauriti scaricabili gratis: porcellane, argenti, armi, orologi, arte asiatica, mobili.
- **Getty Publications Virtual Library** (getty.edu): libri gratuiti di arte e restauro.
- **Gallica** (gallica.bnf.fr) e **Internet Archive** (archive.org): moltissimi cataloghi
  d'asta storici e repertori francesi, tedeschi e italiani.
- **Biblioteca digitale dell'ICCD** e **Catalogo generale dei beni culturali**
  (catalogo.beniculturali.it): schede di opere italiane con foto e datazioni, utili come
  confronto.

I libri di MetPublications e Getty sono gratuiti ma protetti da diritto d'autore:
scaricali per uso personale, non ripubblicarli.

## Aggiungere altri libri

Aggiungi una riga a `CATALOGO` in `scripts/scarica_manuali.py` (identificativo
archive.org, titolo, autore, anno, categoria, diritti) e rilancia lo script. Controlla
prima che il libro sia di dominio pubblico: pubblicato prima del 1930 e con autore morto
da più di 70 anni.
