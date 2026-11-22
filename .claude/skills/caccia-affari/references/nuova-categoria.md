# Una categoria che non conosci: come mapparla da zero

Le categorie descritte nella skill sono esempi, non un elenco chiuso. Quasi ogni oggetto
ha una comunità di collezionisti, e ogni comunità ha lo stesso "ecosistema": chi compra,
dove si vende, dove si discute, dove si leggono i prezzi, chi certifica. Prima di valutare
un oggetto di una categoria nuova, ricostruisci questo ecosistema con ricerche sul web.

## I sette pezzi dell'ecosistema

| Pezzo | Cosa ti dà | Come trovarlo (ricerche tipo) |
|---|---|---|
| 1. **Case d'asta specializzate** | i prezzi più alti per i pezzi migliori, risultati pubblici | `asta <categoria>`, `<categoria> auction house`, `vente aux enchères <categoria>`, `Auktion <Kategorie>`; aggregatori Invaluable, LiveAuctioneers, Lot-tissimo, Drouot, Interenchères, NumisBids e simili |
| 2. **Commercianti che comprano** | liquidità immediata, il "pavimento" del prezzo | `compriamo <categoria>`, `vendi la tua collezione di <categoria>`, `acquisto <categoria> pagamento immediato`; associazioni di categoria (spesso hanno elenchi di soci affidabili) |
| 3. **Marketplace di nicchia** | pubblico appassionato, prezzi di mercato | `<categoria> marketplace`, il nome inglese della categoria + "buy sell"; spesso le sezioni "mercatino" dei forum |
| 4. **Forum e comunità** | identificazione, varianti, falsi noti, stime informali | `forum <categoria>`, gruppi Facebook, subreddit (`r/<categoria>`), Discord dei collezionisti |
| 5. **Cataloghi e banche dati di prezzi** | identificazione della variante e prezzi di vendita | `catalogo <categoria>`, `price guide <category>`, `<category> sold prices database`, database di numeri di serie |
| 6. **Perizia, grading, autenticazione** | credibilità e premio di prezzo | `perizia <categoria>`, `grading <category>`, `authentication <category>`, periti iscritti alla Camera di Commercio |
| 7. **Leggi e limiti** | cosa non si può comprare, vendere o esportare | `<categoria> commercio legge`, CITES, beni culturali, armi, alcol, farmaci, fossili |

## Procedura

1. **Nomina l'oggetto in più lingue**: italiano, inglese, francese, tedesco (e giapponese
   o cinese se pertinente). I nomi tecnici esatti moltiplicano i risultati
   (es. "candeliere" → "bougeoir", "Kerzenleuchter", "candlestick").
2. **Trova la comunità**: un forum o un gruppo attivo è la scorciatoia migliore per
   capire cosa conta (varianti, numeri di serie, falsi noti).
3. **Trova i venduti**: almeno 3 vendite concluse comparabili, meglio da fonti diverse
   (asta specializzata + marketplace di nicchia + eBay venduti).
4. **Trova chi compra subito**: un commerciante o una buylist dà il prezzo minimo
   realizzabile in pochi giorni. Se l'acquisto costa meno di questo, il rischio è basso.
5. **Confronta i canali sul netto** con `scripts/margine.py` (usa `--commissione` e
   `--fisso` per canali non presenti nella tabella).
6. **Annota** il nuovo ecosistema in `manuali/appunti-categorie.md`, così la prossima
   volta è già pronto.

## Regola d'oro

Per ogni categoria esistono tre prezzi diversi: quello del **commerciante che compra**
(basso, immediato), quello del **marketplace di appassionati** (medio, settimane), quello
dell'**asta specializzata** (alto per i pezzi top, mesi, commissioni). L'affare è comprare
sotto il primo; il guadagno massimo è vendere al secondo o al terzo.
