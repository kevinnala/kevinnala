# Repository GitHub utili: valutazione di attendibilità

Verifica fatta il 22/11/2026 con la ricerca di GitHub e la lettura dei file pubblici.

**Criteri**:
- chi lo mantiene (istituzione o organizzazione vs singola persona);
- stelle e fork (popolarità: un indizio, non una prova);
- data dell'ultimo aggiornamento e se è archiviato;
- licenza (senza licenza il codice non si può riusare legalmente);
- issue aperte;
- per il codice, lettura di README e dipendenze.

**Giudizio**: **Alta** = fonte istituzionale o progetto maturo e attivo; **Media** =
utile ma con limiti; **Bassa** = poco usato, nuovo, senza licenza o non verificabile.

Regola: **i dati CC0/MIT di fonti affidabili li carichiamo; il codice di terzi non lo
eseguiamo senza averlo letto**, e per Subito scriviamo il nostro strumento (vedi sotto).

## A. Caricati nel progetto (cartella `dati/`)

| Repository | Cosa contiene | ★ / ultimo agg. | Licenza | Attendibilità | Uso |
|---|---|---|---|---|---|
| **metmuseum/openaccess** | ~480.000 oggetti del Metropolitan Museum con autore/manifattura, date, materiali, provenienza | 1.470 / 16-11-2026 | CC0 | **Alta**: pubblicato dal museo, aggiornato ogni settimana | indice `dati/produttori-met.tsv` (62.000 nomi): fonderie, manifatture, argentieri, ebanisti, artisti, con date di attività e tipi di oggetti |
| **MuseumofModernArt/collection** | artisti e designer della collezione MoMA | 1.571 / 17-11-2026 | CC0 | **Alta**: pubblicato dal museo, attivo | `dati/artisti-moma.tsv` (16.000 nomi): designer e artisti del '900, con identificativi ULAN e Wikidata |
| **tategallery/collection** | artisti della collezione Tate | 527 / 02-11-2021 | CC0 | **Media-alta**: fonte ufficiale ma ferma al 2021 | `dati/artisti-tate.tsv` (3.500 nomi), con luoghi di nascita e morte |

Si ricostruiscono con `scripts/scarica_dati.py`.

## B. Dati di carte collezionabili (non caricati: si usano via rete quando servono)

| Repository | Cosa contiene | ★ / ultimo agg. | Licenza | Attendibilità | Note |
|---|---|---|---|---|---|
| **tcgdex/cards-database** | database Pokémon TCG in più lingue, **italiano compreso** | 1.207 / 19-11-2026 | MIT | **Alta** | il più adatto a noi (nomi italiani); 177 issue aperte, normali per un progetto così grande |
| **PokemonTCG/pokemon-tcg-data** | dati della Pokémon TCG API (set, carte, rarità, varianti) | 887 / 08-11-2026 | non dichiarata | **Alta come dati, ma senza licenza** | si consulta (es. `raw.githubusercontent.com/PokemonTCG/pokemon-tcg-data/master/sets/en.json`), non lo copiamo |
| **mtgjson/mtgjson** | tutti i dati di Magic: the Gathering | 484 / 21-11-2026 | MIT | **Alta**: lo standard della comunità | la vecchia versione mtgjson3 è archiviata, non usarla |
| **DawnbrandBots/yaml-yugi** | database Yu-Gi-Oh! (TCG e OCG giapponese) | 47 / 22-11-2026 | AGPL-3.0 | **Media**: attivo ma piccolo | licenza AGPL: va bene per consultare |

## C. Librerie per prezzi e cataloghi (da usare nello scanner, previa lettura del codice)

| Repository | A cosa serve | ★ / ultimo agg. | Licenza | Attendibilità | Note |
|---|---|---|---|---|---|
| **joalla/discogs_client** | client Python per l'API di Discogs (stampe, prezzi, venduti) | 424 / 29-09-2026 | non standard (ereditata dal client ufficiale) | **Alta**: continuazione del client ufficiale, ormai archiviato | serve un token Discogs gratuito |
| **andli/pymkm** | client Python per l'API di Cardmarket | 58 / 13-02-2026 | MIT | **Media**: maturo ma poco attivo | richiede credenziali API Cardmarket: verificare se sono concesse ai privati |
| markfoster314/Pricecharting-Scraper | estrae i prezzi da PriceCharting senza API | 34 / 28-10-2026 | MIT | **Bassa**: scraping, probabilmente contrario ai termini del sito | meglio l'API ufficiale a pagamento o la consultazione manuale |
| SDK per Numista (namachieli, wells01440...) | client per l'API del catalogo Numista | 0–5 / 2022–2025 | MIT | **Bassa**: piccoli e poco seguiti | meglio chiamare direttamente l'API ufficiale di Numista (chiave gratuita) |
| Smithsonian/OpenAccess | open data dello Smithsonian | 443 / 2021 | CC0 | **Bassa come repository**: archiviato, i dati sono stati spostati altrove | non usarlo |

## D. Scanner di annunci (Subito, Vinted, Wallapop)

| Repository | Cosa fa | ★ / ultimo agg. | Licenza | Attendibilità | Note |
|---|---|---|---|---|---|
| **morrolinux/subito-it-searcher** | cerca su Subito a intervalli e notifica su Telegram | 162 / 01-12-2025 | **nessuna** | **Media**: il più usato e longevo (dal 2019), ma 18 issue aperte | usa `requests` + BeautifulSoup: Subito oggi blocca le richieste non da browser, quindi probabilmente non funziona più così com'è; senza licenza non si può riusare il codice |
| **Giglium/vinted_scraper** | libreria Python per cercare su Vinted | 110 / 16-11-2026 | MIT | **Media-alta**: attivo, poche issue | candidato per la parte Vinted dello scanner |
| jasp-nerd/vinted-bot | avvisi di nuovi annunci Vinted (Telegram, email, ntfy) | 16 / 21-11-2026 | MIT | **Media-bassa** | da leggere prima dell'uso |
| mxyp/subot | controlla Subito, Vinted e Wallapop e notifica | 5 / 21-11-2026 | MIT | **Bassa**: creato ad agosto 2026, README non trovato | non usare |
| gianemi2/subito.it-bot, Kianda/subitoo, alebrandi/Subito.it-API | bot e API non ufficiali per Subito | 5–9 / 2022–2026 | varie | **Bassa** | piccoli o fermi |

## E. Skill e server MCP per Subito (trovati nella prima ricerca)

| Repository | Cosa fa | ★ / ultimo agg. | Licenza | Attendibilità | Note |
|---|---|---|---|---|---|
| filippolmt/skills (`subito-research`) | skill per cercare su Subito e giudicare i prezzi | 1 / 22-11-2026 | MIT | **Bassa come popolarità, buona come contenuto** (letta: approccio corretto con browser vero) | ne abbiamo ripreso l'approccio |
| remorses/subito-cli | CLI di ricerca su Subito tramite il Chrome dell'utente | 2 / 08-08-2026 | nessuna | **Bassa** | richiede un'estensione nel browser |
| monossido/mcp-server-subito | server MCP per cercare su Subito | 0 / 06-11-2026 | AGPL-3.0 | **Bassa** | nessun utente visibile |

## Cosa non esiste (o non è affidabile)

- **Banche dati aperte di punzoni d'argento o di marchi di porcellana**: nessun repository
  serio. Usare i manuali in `manuali/testi/` (Jackson, Rosenberg, Chaffers) e gli indici in `dati/`.
- **Marchi di regno cinesi**: nessun dataset affidabile; usare Hobson vol. 2 e gotheborg.com.
- **Storici dei prezzi d'asta aperti**: non esistono gratis e affidabili; i prezzi restano
  da cercare caso per caso (eBay venduti, archivi d'asta, Cardmarket, PriceCharting, Discogs).

## Raccomandazione per lo scanner di Subito

Nessun progetto per Subito è insieme affidabile, mantenuto e con licenza. Conviene scrivere
il nostro scanner con Playwright (già installato nell'ambiente), con poche richieste e a
ritmo umano, leggendo i dati che Subito incorpora nella pagina (`__NEXT_DATA__`). Per Vinted
si può valutare `Giglium/vinted_scraper` (MIT) dopo averne letto il codice.
