# Dove cercare

## Fonti online (Italia e vicine)

| Fonte | Punti di forza | Note pratiche |
|---|---|---|
| **Subito.it** | il più grande in Italia, tantissimi privati inconsapevoli, ritiro a mano | blocca curl/fetch: serve un browser vero. URL: `https://www.subito.it/annunci-<regione o italia>/vendita/<categoria>/?q=<parole>`; `&ps=<min>&pe=<max>` per il prezzo; ordina per "più recenti" |
| **eBay.it** (e .de, .fr) | volumi enormi; aste in chiusura a orari morti | cerca aste che finiscono di notte o di domenica mattina, titoli sbagliati, "lotto"; eBay.de per oggetti tedeschi e austriaci |
| **Facebook Marketplace e gruppi** | svuota cantine, eredità, gruppi locali "vendo tutto" | molti oggetti non finiscono mai su Subito |
| **Vinted** | abbigliamento e accessori vintage, ma anche oggetti per la casa e carte | venditori giovani che svuotano casa dei nonni |
| **Wallapop** | Spagna, crescente in Italia | |
| **Leboncoin (Francia), Kleinanzeigen (Germania), Willhaben (Austria)** | bronzi francesi, porcellane tedesche, design | spedizione e lingua: margine per chi si muove |
| **Catawiki** | non per comprare sottocosto (prezzi spesso pieni), ma utile per vedere cosa si vende | lotti senza riserva a volte chiusi bassi |
| **Aste giudiziarie e fallimentari** (astegiudiziarie.it, IVG – Istituti Vendite Giudiziarie, portale delle vendite pubbliche del Ministero) | lotti di arredi, quadri, magazzini interi | guarda di persona; i cataloghi sono spesso descritti in modo sommario |
| **Piccole case d'asta di provincia** | lotti misti, descrizioni povere | aggregatori: Invaluable, LiveAuctioneers, Lot-tissimo, Drouot (Francia) |

## Fonti fisiche

- **Svuota cantine / sgomberi**: chiedi di vedere prima dello sgombero; molti vendono
  a peso o a lotto.
- **Mercatini dell'usato conto terzi** (Mercatopoli, Mercatino Franchising e simili): i
  prezzi li fa il personale, che non può conoscere tutto.
- **Mercati dell'antiquariato** (Arezzo, Piazzola sul Brenta, Navigli a Milano, Porta
  Portese a Roma, Fiera di Parma per commercianti): presto la mattina, contanti.
- **Eredità e conoscenti**: il canale migliore e il più delicato. Paga il giusto.

## Parole che usano i venditori inconsapevoli

Cerca queste, non i nomi dei maestri (chi scrive "Fattori" sa già cosa ha):

- Generiche: `quadro antico`, `dipinto vecchio`, `quadro nonna`, `olio su tela antico`,
  `cornice antica con quadro`, `soprammobile`, `statua vecchia`, `statuina`,
  `candelabro vecchio`, `oggetti vecchi`, `cianfrusaglie`, `svuoto cantina`,
  `svuoto soffitta`, `eredità`, `sgombero`, `lotto oggetti`, `lotto carte`,
  `raccoglitore carte`, `vecchie carte pokemon`, `album figurine`, `scatola giochi vecchi`.
- Materiali sbagliati: `ottone pesante` (spesso bronzo), `metallo argentato` (a volte
  argento con punzoni), `vetro colorato pesante` (a volte Murano firmato),
  `piatto decorato` (a volte maiolica antica).
- Firme non lette: `firma illeggibile`, `firmato non so chi`, `firma in basso`,
  `timbro sotto`, `marchio sotto`, `ha un numero sotto`.
- Errori di battitura: `pokemn`, `pokémon` senza accento, `cristofle`/`christofl`,
  `vennini` (Venini), `segusso` (Seguso), `ginory`, `capodimonti`,
  `rollex`, `omegha`. Prova varianti con una lettera mancante o doppia.

## Segnali di un buon annuncio

- Foto brutte, poche, sfocate, sul tavolo di cucina: pochi concorrenti lo notano.
- Descrizione di una riga, nessun nome di autore o marca.
- Prezzo tondo e basso ("20 €", "50 € tutto il lotto").
- Pubblicato da poco (le prime ore contano: gli affari durano poco).
- Venditore privato con pochi annunci, spesso tutti dalla stessa casa.

## Segnali di truffa

- Oggetto famoso a prezzo stracciato con foto da catalogo o prese dal web
  (fai una ricerca per immagine).
- Richiesta di pagamento fuori piattaforma, anticipo, bonifico "per bloccarlo".
- Fretta, storie complicate, venditore all'estero che non può mostrare l'oggetto.
- Carte "rare" in buste nuove a decine, "lotti" con le stesse carte top in ogni foto.
- "Perizia" o "certificato" firmato dal venditore stesso o da enti sconosciuti.

## Come fare la caccia con Claude (Subito)

1. Apri il browser (Playwright: `require('playwright')`, `chromium.launch()`).
2. Per ogni parola chiave della lista e per la zona scelta, carica la pagina dei
   risultati ordinata per data; leggi titolo, prezzo, link, data, località.
   Molti siti contengono i dati in un JSON incorporato (`__NEXT_DATA__` su Subito):
   leggilo invece di analizzare l'HTML.
3. Filtra per prezzo massimo e scarta le categorie irrilevanti.
4. Apri solo gli annunci promettenti e guarda tutte le foto.
5. Pochi caricamenti, pause tra le pagine: nessuna raccolta massiva.
