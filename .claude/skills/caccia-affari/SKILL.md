---
name: caccia-affari
description: Trova oggetti vintage, antichi e da collezione venduti sotto il loro valore (su Subito, eBay, Vinted, Wallapop, Marketplace, mercatini, aste), li identifica e attribuisce come farebbe un perito, stima il valore sui prezzi di vendita reali e indica dove rivenderli per il massimo ricavo netto. Usala quando l'utente vuole cercare affari da rivendere, valutare un annuncio o una foto ("quanto vale?", "è originale?", "di che epoca è?"), capire a chi vendere un oggetto (carte Pokémon, dipinti dell'800, bronzi, argenti, ceramiche, vetri di Murano, design, orologi, giocattoli, vinili...), o calcolare il margine di un acquisto.
---

# Caccia agli affari: vintage, antiquariato e collezionismo

L'affare nasce quasi sempre da un **venditore che non sa cosa vende**: lo descrive
male, lo data male, lo mette nella categoria sbagliata o lo prezza come "roba della
nonna". Il lavoro di questa skill è vedere quello che il venditore non ha visto, e
dimostrarlo con prove, non con l'entusiasmo.

**Criterio unico: il valore di rivendita.** Si cercano oggetti di qualunque epoca e di
qualunque manifattura, italiana o internazionale, purché si possano rivendere con un margine
reale (mercato dimostrabile, oggetto riconoscibile, margine che regge: vedi
`references/categorie/epoche-e-stili.md#Il criterio`). Si cerca ovunque; la zona conta
**solo per il ritiro a mano**: gli oggetti non spedibili devono essere nelle province di
ritiro (oggi Campania, Latina e Frosinone).

Consegna sempre una **scheda affare** (formato al passo 7) e mai una promessa:
ogni attribuzione ha un grado di fiducia e ogni prezzo viene da vendite reali.

## Passo 0, sempre: instrada sulla categoria (prima di leggere qualunque file)

```bash
python3 .claude/skills/caccia-affari/scripts/categoria.py "<titolo e descrizione dell'annuncio>"
```

Lo script riconosce la categoria (55, con sinonimi in 4 lingue ed errori di battitura) e
stampa la scheda essenziale: verifiche chiave, foto da chiedere, rischi, dove vendere, e
**le sole righe dei file da leggere** (`file:inizio-fine`), più i manuali e i dati da
interrogare. `--estratto` stampa direttamente il testo di quelle sezioni.

Regole di economia (meno token, meno errori):

- **Leggi solo le righe indicate** dallo script (Read con offset e limit). Non aprire le
  altre guide, la mappa qui sotto serve solo se lo script non basta.
- **Una categoria per oggetto.** Se lo script ne dà due, usa la prima e prendi dalla
  seconda solo ciò che manca. Non ricominciare il ragionamento da capo.
- **Lotti misti**: elenca gli oggetti visibili e rilancia lo script su ognuno di quelli
  promettenti. Ignora il resto.
- **Nessuna categoria riconosciuta**: non indovinare. Stabilisci materiale e funzione
  dell'oggetto e rilancia lo script con quelle parole; se ancora niente, usa
  `references/nuova-categoria.md`.
- **Triage prima della perizia**: per ogni annuncio bastano 2–3 righe (cos'è, valore
  plausibile, sì/no). Approfondisci solo se il valore plausibile è almeno il doppio del
  prezzo chiesto.
- **Ricerche con limite**: al massimo 3 comparabili venduti per oggetto e una ricerca nei
  manuali per nome; se mancano dati, scrivi "da verificare" e passa oltre invece di
  continuare a cercare.
- **Le verifiche chiave dello script sono la checklist**: seguile in ordine e fermati alla
  prima che fa cadere l'affare (es. "è una stampa", "è zama", "è una riedizione").

## Le categorie sono esempi, non limiti

Questa skill vale per **qualunque** oggetto con un mercato di collezionisti o di
appassionati: monete, francobolli, militaria, penne, macchine fotografiche, strumenti
musicali, hi-fi, computer retro, arte orientale, tappeti, icone, moda e borse di lusso,
sneakers, vini e distillati, automobilia, minerali, manifesti, memorabilia sportiva e
tutto il resto. Non fermarti alle categorie con una guida: se l'oggetto non è coperto,
mappa il suo ecosistema con `references/nuova-categoria.md`.

E non fermarti alle piattaforme generaliste (eBay, Catawiki, Subito, Vinted): per
comprare e per rivendere cerca sempre anche i **canali specializzati** della categoria
(case d'asta di settore, commercianti che comprano, marketplace di nicchia, forum,
cataloghi di prezzi, servizi di perizia). Sono in `references/canali-specializzati/`.

## Mappa dei riferimenti

Da usare solo se lo script del passo 0 non basta:

| Serve | File |
|---|---|
| Come si fa una perizia (metodo generale, valido per tutto) | `references/metodo-perizia.md` |
| Dove cercare e quali parole usano i venditori inconsapevoli | `references/dove-cercare.md` |
| A chi rivendere, commissioni, prezzi venduti | `references/dove-rivendere.md` |
| Leggi, esportazione, avorio, archeologia, fisco | `references/legale-fiscale.md` |
| Carte collezionabili (Pokémon, Magic, Yu-Gi-Oh, sport) | `references/categorie/carte-collezionabili.md` |
| Dipinti, disegni, stampe (in particolare l'Ottocento) | `references/categorie/dipinti-stampe.md` |
| Bronzi, argenti, peltro, ottone, candelieri, oggetti in metallo | `references/categorie/metalli-bronzi-argenti.md` |
| Porcellane, maioliche, vetri (Murano, Gallé, Daum) | `references/categorie/ceramiche-vetri.md` |
| Design e modernariato del Novecento | `references/categorie/design-modernariato.md` |
| Orologi, giocattoli, videogiochi, LEGO, vinili, fumetti, libri, monete, francobolli | `references/categorie/altre-categorie.md` |
| Il criterio del valore di rivendita; manifatture e marchi che fanno prezzo (Italia e mondo); riconoscere le epoche dagli stili; esempi di specialità regionali (presepe, corallo e cammei, Vietri, arte sacra, fotografie d'epoca); piccoli oggetti di pregio | `references/categorie/epoche-e-stili.md` |
| Arte africana e oceanica, nativi nordamericani (Navajo, argento e turchese, Pueblo, kachina, inuit), argento di Taxco, antiquariato e design USA (Tiffany Studios, art pottery, Stickley, Eames, Zippo, insegne); cosa è vietato | `references/categorie/arte-africana-americana.md` |
| Scultori e bronzi firmati (animalier, viennesi, Déco, fonderie, riproduzioni napoletane, scultori italiani e multipli) e soprammobili di designer e manifatture italiane e internazionali | `references/categorie/scultori-designer.md` |
| Canali specializzati per categoria (aste di settore, chi compra, nicchie, forum, prezzi, perizie) | `references/canali-specializzati/` (indice nel `README.md`) |
| Categoria non coperta: come mapparne l'ecosistema | `references/nuova-categoria.md` |
| Manuali e banche dati da consultare | `references/manuali-consigliati.md` |
| Biblioteca di 34 manuali storici in testo completo (stili ed epoche, oggetti d'arte e curiosità, marchi di ceramiche, punzoni d'argento, gioielli, orologiai, pittori dell'Ottocento, numismatica, armi, tappeti, vetro, mobili, arte tribale e nativa americana, ceramica americana, Arts and Crafts, bronzi animalier) | `manuali/INDICE.md` e `manuali/testi/` |
| Indici aperti di produttori e artisti (Met 62.000 nomi, MoMA 16.000, Tate 3.500): date di attività, ruolo, tipi di oggetto | `dati/` (guida in `dati/README.md`) |
| Repository GitHub utili e loro attendibilità (dati di carte, API di prezzi, scanner) | `references/librerie-github.md` |
| Manuali in PDF dell'utente (se presenti) | `manuali/` |

Quando devi leggere un marchio, un punzone, una firma o il nome di una manifattura o di un
artigiano, **cerca prima nei manuali** (`grep -n -i -C3 "<nome>" manuali/testi/*.txt`;
l'indice dice quale libro usare), poi negli indici di `dati/` (`grep -i "<nome>"
dati/*.tsv`: date di attività e tipi di oggetto per verificare la coerenza) e poi in rete. Sono libri storici: affidabili per marchi,
date e biografie, non per i prezzi. Cita il libro e la pagina quando lo usi.

## Scanner automatico (Subito, Wallapop, Vinted)

```bash
python3 .claude/skills/caccia-affari/scripts/scanner.py            # giro completo (~25 min)
python3 .claude/skills/caccia-affari/scripts/scanner.py --max 5    # prova veloce
python3 .claude/skills/caccia-affari/scripts/scanner.py --da-archivio  # ricalcola dopo aver cambiato i segnali
python3 .claude/skills/caccia-affari/scripts/foto.py <url> --max-foto 3  # testo e foto di un annuncio
```

Fonti (attivabili in `fonti` di `scanner_config.json`): **Subito** (tutta Italia + zone di
ritiro), **Wallapop** (Italia e Spagna, interfaccia di ricerca pubblica), **Vinted** (pagina
pubblica di ricerca, sempre con spedizione). eBay rifiuta i browser automatici: servirebbe
la sua API ufficiale. Con `--telegram` alla fine manda la lista dei migliori su Telegram
(`scripts/notifica_telegram.py`, istruzioni in testa al file).

Cerca in tutta Italia e nelle zone di ritiro; tiene gli annunci con spedizione da ovunque e
quelli **solo a mano** soltanto nelle province di ritiro (`province_ritiro` in
`scripts/scanner_config.json`: oggi Campania, Latina, Frosinone). Salta gli annunci già
visti, li smista con `categoria.py`, li ordina per probabilità di affare e scrive
`risultati/report-*.md` (📦 spedibile, 🤝 solo ritiro). Il punteggio ordina, non stima:
la perizia si fa sui primi della lista con le foto (`foto.py`).

### Giro completo: OGNI volta che si lancia lo scanner (regola dell'utente)

L'utente vuole a ogni giro **le perizie di almeno 30 annunci nuovi su Telegram**, non solo
la lista. Non ripropone mai un annuncio già periziato e impara da ciò che l'utente compra e
vende. Passi, in quest'ordine, senza saltarne:

```bash
S=.claude/skills/caccia-affari/scripts
python3 $S/telegram_bot.py                 # 1. legge i messaggi dell'utente (preso/venduto/note) e risponde
python3 $S/scanner.py                      # 2a. scanner per parole (salta visti e periziati; bonus dagli esiti)
python3 $S/esplora.py                      # 2b. scanner GENERALE: tutto il nuovo per categoria + aste giudiziarie
#    3. Claude GUARDA TUTTE le griglie risultati/esplora/griglia-*.jpg (Read, una per volta) come un
#       rigattiere: cerca ciò che il titolo non dice (firma, marchio, materiale, epoca, forma da designer,
#       arte tribale vera, bronzo, argento, vetro d'autore...). Scrive i numeri scelti (#k) in
#       risultati/esplora/scelti.txt — di solito 10-25 su 400; nel dubbio includi.
python3 $S/perizie.py prepara --n 30 --scelti   # 4. scelti dalle griglie + i migliori per parole fino a 30,
#                                                    provini delle foto + LEZIONI dagli esiti
#    5. Claude guarda ogni provino (Read) e il testo, e scrive risultati/perizie/perizie.json
#       (formato: `perizie.py modello`), applicando la skill e le lezioni stampate al passo 4
python3 $S/perizie.py invia .claude/skills/caccia-affari/risultati/perizie/perizie.json   # 6. Telegram + memoria
#    7. commit e push di .claude/skills/caccia-affari/memoria/ (senza push la memoria si perde)
```

- **Coda a blocchi** (`memoria/coda.jsonl`): tutto ciò che è interessante ma non periziato nel
  giro (resto del report per parole e candidati delle griglie) resta in coda per 21 giorni.
  L'utente chiede altri blocchi con `/altri 30` su Telegram (o in chat): `perizie.py prepara`
  ne aggiunge automaticamente tanti quanti richiesti, scelti prima, poi per parole, poi griglie.
  `memoria.py coda` dice quanti ne aspettano. Se l'utente chiede un blocco in chat senza giro:
  `perizie.py prepara --n 30` (prende dalla coda) e poi i passi 5-7.
- **Budget e margine** dell'utente: `esplora.budget` (500 €) e `esplora.margine_minimo_netto`
  (50 €) in `scanner_config.json`. COMPRA/TRATTA solo se il netto atteso supera il margine minimo.
- **Scanner generale** (`esplora.py`): Subito per categoria (collezionismo, arredamento, libri e
  musica solo con segnali d'epoca), Wallapop per categoria (solo Italia), aste giudiziarie di
  Fallcoaste (oggetti d'arte e preziosi: lotti dei tribunali, descritti in fretta). Tiene solo
  privati sotto budget e premia i segnali del venditore inconsapevole (titolo vago, parole da
  cantina/eredità, poche foto, descrizione scarna); penalizza chi nomina già il marchio. Per le
  aste: scadenza, tribunale e "prezzo base con oneri" sono nella scheda; il ritiro o la
  spedizione si chiedono all'IVG prima di offrire.
- **Siti che rifiutano i programmi automatici** (Asteannunci, Mercatinousato, Facebook): non si
  aggirano i blocchi. Facebook Marketplace solo dal browser dell'utente, se collega il suo computer.

- **Perizia per ogni annuncio** (30): verdetto COMPRA / TRATTA / VERIFICA PRIMA / LASCIA,
  valore `[prudente, probabile, ottimista]`; per i non-LASCIA anche cosa è, fiducia, dove
  vendere con netto, verifiche prima di pagare, offerta e massimo. Per i LASCIA basta una
  riga di motivo. Triage onesto: se il giro è debole, dillo (molti LASCIA vanno bene).
- **Lezioni** (`memoria.py lezioni`): se per una categoria il rapporto venduto/stima è sotto
  0,85 abbassa le stime, sopra 1,2 alzale; usa il canale che ha reso di più; leggi le note
  libere dell'utente prima di periziare.
- **Foto**: Vinted (images1.vinted.net) e Wallapop (cdn.wallapop.com) possono essere bloccati
  dalla rete dell'ambiente: in quel caso perizia dal testo, verdetto al massimo VERIFICA PRIMA.
- **Memoria** (`memoria/`, nel repository): `visti.txt` (annunci già passati),
  `periziati.jsonl` (perizie con numero stabile #N), `esiti.jsonl` (messaggi dell'utente),
  `stato.json` (contatore e offset Telegram). `risultati/` invece è locale e si perde.
- **Comandi Telegram dell'utente** (letti al passo 1; il bot non è sempre acceso):
  `/preso #N prezzo`, `/venduto #N prezzo canale`, `/scartato #N motivo`, `/perso #N`,
  `/nota testo`, `/bilancio`, `/lezioni`, `/aiuto`. Un testo libero diventa una nota.

## 1. Capire la richiesta

Tre modalità; riconosci quale e chiedi in un solo messaggio ciò che manca:

- **Caccia**: "trovami affari". Servono categoria (o "qualsiasi"), budget massimo
  per pezzo, zona (ritiro a mano o spedizione), margine minimo voluto (default:
  almeno il 40% netto o 100 € netti, il maggiore dei due).
- **Valutazione**: l'utente porta un annuncio, un link o delle foto. Vai al passo 3.
- **Rivendita**: l'utente ha già l'oggetto e chiede a chi venderlo. Passo 3 per
  confermare cos'è, poi passo 5.

## 2. Cercare (modalità caccia)

Segui `references/dove-cercare.md`. In breve:

- Subito.it e altri siti bloccano fetch e curl (403 / protezione anti-bot): usa un
  browser vero (Playwright, già presente nell'ambiente cloud; oppure il browser
  dell'utente se collegato). Rispetta i siti: poche pagine, ritmo umano, niente
  raccolta massiva.
- Cerca **dove il venditore sbaglia**, non dove il collezionista cerca: parole
  generiche ("quadro antico", "soprammobile vecchio", "svuoto cantina", "lotto
  carte"), errori di battitura (`pokemn`, `cristofle`, `venini` scritto male),
  categorie sbagliate, foto pessime, annunci appena pubblicati.
- Non solo i siti generalisti: anche i **mercatini dei forum** specializzati, i
  marketplace di nicchia, i lotti invenduti o mal descritti delle piccole aste di
  settore (elenchi per categoria in `references/canali-specializzati/`).
- Per ogni annuncio promettente salva: link, prezzo, data, foto, testo, zona.
- Scarta presto: un candidato vale l'approfondimento solo se il valore plausibile
  è almeno il doppio del prezzo chiesto.

## 3. Identificare e attribuire

Applica `references/metodo-perizia.md` e poi il file della categoria. L'ordine è
sempre lo stesso, e non si salta:

1. **Che cos'è**: funzione, materiale, tecnica di costruzione.
2. **Quando**: indizi di epoca che il venditore non può falsificare facilmente
   (viti, chiodi, tela, carta, stampa, segni di usura).
3. **Chi**: marchi, firme, punzoni, etichette; solo dopo lo stile.
4. **Coerenza**: tutto deve raccontare la stessa storia. Una firma "antica" su un
   oggetto costruito con viti moderne è un falso o un'aggiunta.
5. **Condizione**: restauri, mancanze, parti sostituite.

Correggi il venditore quando sbaglia l'epoca: "portacandele impressionista" non
esiste come categoria; l'impressionismo è pittura. Un candeliere di quegli anni è
Napoleone III / Secondo Impero, eclettismo o (dopo il 1890) Art Nouveau / Liberty.
Usa il termine giusto: è anche quello che userà chi compra.

Dai sempre un **grado di fiducia** con la convenzione delle case d'asta
(vedi `metodo-perizia.md`): *certo*, *attribuito a*, *cerchia / bottega di*,
*scuola di*, *maniera di*, *non determinabile dalle foto*. Se dalle foto non si
può decidere, dillo e **elenca le foto o le verifiche che servono** (retro,
punzoni in macro, firma con luce radente, base, peso, luce UV, ecc.).

## 4. Stimare il valore

- Usa **solo prezzi di vendita conclusi** (eBay "oggetti venduti", risultati d'asta,
  Cardmarket venduti, PriceCharting, archivi d'asta), mai i prezzi chiesti.
- Minimo 3 comparabili dello stesso autore/modello/variante e condizione simile;
  annota fonte, data, prezzo.
- Nei risultati d'asta distingui **aggiudicazione** (martello) e **prezzo con diritti**
  d'asta (+20–30%): non confrontare mele con pere.
- Correggi per condizione, completezza (scatola, documenti), provenienza e mercato
  (un pittore napoletano vale di più a Napoli; un manga raro in Giappone).
- Restituisci una **forchetta** (prudente, probabile, ottimista), non un numero solo.

## 5. Scegliere dove rivendere

Segui `references/dove-rivendere.md` e il file della categoria in
`references/canali-specializzati/`. Metti sempre a confronto almeno un canale
generalista e almeno uno specializzato (asta di settore, commerciante che compra,
marketplace di nicchia). Per ogni oggetto confronta 2–3 canali sul
**ricavo netto** (prezzo atteso − commissioni − spedizione/assicurazione − costi di
perizia, grading o restauro), tenendo conto di tempi e rischio.

Calcola i numeri con lo script (Python 3, nessuna dipendenza):

```bash
python3 .claude/skills/caccia-affari/scripts/margine.py --acquisto 40 --vendita 300 --tutti
python3 .claude/skills/caccia-affari/scripts/margine.py --acquisto 40 --vendita 300 --canale cardmarket --spedizione 6 --extra 25
python3 .claude/skills/caccia-affari/scripts/margine.py --vendita 300 --canale ebay_privato --margine-voluto 0.4   # prezzo massimo da offrire
python3 .claude/skills/caccia-affari/scripts/margine.py --canali   # elenco canali e commissioni
```

Le commissioni nello script hanno una data di verifica: se è vecchia di più di
qualche mese, ricontrolla sul sito della piattaforma e aggiornale.

## 6. Rischi e legalità

Prima di consigliare un acquisto controlla `references/legale-fiscale.md`, in
particolare: reperti archeologici (mai), avorio e specie protette, opere con più di
70 anni da vendere all'estero (serve l'attestato di libera circolazione), e
compravendita abituale (diventa attività commerciale). Segnala i segnali di truffa
dell'annuncio (prezzo troppo basso per un oggetto famoso, pagamento fuori
piattaforma, foto prese dal web, fretta).

## 7. Scheda affare (output)

Per ogni oggetto:

```
## <Nome corretto dell'oggetto> — <verdetto: COMPRA / TRATTA / VERIFICA PRIMA / LASCIA>
Annuncio: <link> · chiesto <prezzo> · <zona> · pubblicato <data>
Cos'è davvero: <identificazione, epoca, autore/manifattura>
Fiducia: <certo / attribuito a / … / non determinabile> — perché: <prove viste>
Cosa ha sbagliato il venditore: <categoria, epoca, nome, foto…>
Valore: prudente <€> · probabile <€> · ottimista <€>
  Comparabili: <fonte, data, prezzo> ×3+
Dove rivendere: <canale migliore> → netto <€> (margine <€>, <%>) ; alternativa <canale> → netto <€>
Da verificare prima di pagare: <foto/domande da fare al venditore>
Rischi: <falsi tipici, condizioni, legali>
Offerta consigliata: <€> (massimo <€>)
```

Per la caccia, metti in cima una tabella riassuntiva ordinata per margine netto
atteso × fiducia, e scarta in fondo, con una riga di motivo, ciò che non regge.

## Regole

- Mai spacciare un'ipotesi per certezza. Nel dubbio, "maniera di" e prezzo prudente.
- Mai consigliare di mentire al venditore o all'acquirente sull'attribuzione. Si
  compra bene sapendo di più, non ingannando.
- Per oggetti sopra ~2.000 € di valore stimato, consiglia una perizia (archivio
  d'artista, perito iscritto alla Camera di Commercio / CTU del tribunale,
  dipartimento della casa d'asta, servizio di grading) prima di vendere.
- Prezzi e commissioni cambiano: scrivi sempre la data dei comparabili.
