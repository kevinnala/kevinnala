# Dati aperti (CC0)

Indici compatti ricavati da open data di musei pubblicati su GitHub, in licenza CC0
(liberamente riutilizzabili). Si ricostruiscono con `../scripts/scarica_dati.py`.
La valutazione delle fonti è in `../references/librerie-github.md`.

| File | Fonte | Righe | A cosa serve |
|---|---|---|---|
| `produttori-met.tsv` | Metropolitan Museum (metmuseum/openaccess) | ~62.000 | chi ha fatto un oggetto: **manifatture, fonderie, argentieri, ebanisti, vetrerie, artisti**. Per ognuno: date di attività, nazionalità, ruolo (fonditore, manifattura, decoratore...), quanti oggetti ha la Met, intervallo di date degli oggetti, tipi di oggetto, materiali, luoghi |
| `artisti-moma.tsv` | MoMA (MuseumofModernArt/collection) | ~16.000 | **designer e artisti del Novecento**, con date, nazionalità, ULAN e Wikidata |
| `artisti-tate.tsv` | Tate (tategallery/collection) | ~3.500 | artisti, con luoghi e date di nascita e morte |

## Esempi di ricerca

```bash
cd .claude/skills/caccia-affari/dati
grep -i "barbedienne" produttori-met.tsv     # fonderia: date di attività, ruolo, oggetti
grep -i "ginori\|doccia" produttori-met.tsv  # manifattura di porcellana
grep -i "christofle" produttori-met.tsv      # argentiere
grep -i "sottsass" artisti-moma.tsv          # designer
```

## Come usarli nella perizia

- **Coerenza delle date**: se un oggetto "firmato X" sembra del 1820 ma X ha lavorato dal
  1870, è un'incoerenza (oggetto più tardo, firma aggiunta o falso).
- **Che cosa faceva davvero**: se la Met ha di un produttore solo statuette in bronzo, un
  "vaso in ceramica firmato X" merita più sospetto.
- **Nome esatto**: la colonna `nome` dà la grafia corretta da usare nelle ricerche e negli
  annunci (es. "Barbedienne Foundry", "Susse Frères").
- **Valore**: questi dati non contengono prezzi. La presenza nella collezione di un grande
  museo indica però che il produttore è riconosciuto, il che di solito sostiene il prezzo.
