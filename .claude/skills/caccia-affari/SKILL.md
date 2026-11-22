---
name: caccia-affari
description: Trova oggetti vintage, antichi e da collezione venduti sotto il loro valore (su Subito, eBay, Vinted, Wallapop, Marketplace, mercatini, aste), li identifica e attribuisce come farebbe un perito, stima il valore sui prezzi di vendita reali e indica dove rivenderli per il massimo ricavo netto. Usala quando l'utente vuole cercare affari da rivendere, valutare un annuncio o una foto ("quanto vale?", "è originale?", "di che epoca è?"), capire a chi vendere un oggetto (carte Pokémon, dipinti dell'800, bronzi, argenti, ceramiche, vetri di Murano, design, orologi, giocattoli, vinili...), o calcolare il margine di un acquisto.
---

# Caccia agli affari: vintage, antiquariato e collezionismo

L'affare nasce quasi sempre da un **venditore che non sa cosa vende**: lo descrive
male, lo data male, lo mette nella categoria sbagliata o lo prezza come "roba della
nonna". Il lavoro di questa skill è vedere quello che il venditore non ha visto, e
dimostrarlo con prove, non con l'entusiasmo.

Consegna sempre una **scheda affare** (formato al passo 7) e mai una promessa:
ogni attribuzione ha un grado di fiducia e ogni prezzo viene da vendite reali.

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

Leggi solo ciò che serve al caso:

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
| Canali specializzati per categoria (aste di settore, chi compra, nicchie, forum, prezzi, perizie) | `references/canali-specializzati/` (indice nel `README.md`) |
| Categoria non coperta: come mapparne l'ecosistema | `references/nuova-categoria.md` |
| Manuali e banche dati da consultare | `references/manuali-consigliati.md` |
| Biblioteca di 20 manuali storici in testo completo (marchi di ceramiche, punzoni d'argento, orologiai, pittori dell'Ottocento, numismatica, armi, tappeti, vetro, mobili) | `manuali/INDICE.md` e `manuali/testi/` |
| Indici aperti di produttori e artisti (Met 62.000 nomi, MoMA 16.000, Tate 3.500): date di attività, ruolo, tipi di oggetto | `dati/` (guida in `dati/README.md`) |
| Repository GitHub utili e loro attendibilità (dati di carte, API di prezzi, scanner) | `references/librerie-github.md` |
| Manuali in PDF dell'utente (se presenti) | `manuali/` |

Quando devi leggere un marchio, un punzone, una firma o il nome di una manifattura o di un
artigiano, **cerca prima nei manuali** (`grep -n -i -C3 "<nome>" manuali/testi/*.txt`;
l'indice dice quale libro usare), poi negli indici di `dati/` (`grep -i "<nome>"
dati/*.tsv`: date di attività e tipi di oggetto per verificare la coerenza) e poi in rete. Sono libri storici: affidabili per marchi,
date e biografie, non per i prezzi. Cita il libro e la pagina quando lo usi.

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
