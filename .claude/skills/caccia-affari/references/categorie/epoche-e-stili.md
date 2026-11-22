# Epoche, stili e manifatture che hanno valore

Guida generale, valida per oggetti di **qualunque provenienza** (italiana o internazionale)
e di qualunque epoca. Il criterio è uno solo: **l'oggetto ha un valore di rivendita?** La
provenienza geografica dell'oggetto non conta; la zona conta solo per il ritiro a mano
(vedi lo scanner in `SKILL.md`).

Per approfondire usa i manuali: Melani (`stili-melani-*`), De Mauri *L'amatore di oggetti
d'arte e di curiosità* (`oggetti-de-mauri-*`), Meyer (`stili-meyer-*`).

## Il criterio: valore di rivendita

Un oggetto merita attenzione se tutte e tre queste cose sono vere:

1. **C'è un mercato**: si trovano vendite concluse di oggetti uguali o simili (aste, eBay
   venduti, marketplace di settore). Niente vendite concluse = niente valore dimostrabile.
2. **È riconoscibile**: manifattura, marchio, autore, modello o tipologia identificabili
   (o un'epoca dimostrabile per oggetti senza firma ma di qualità).
3. **Il margine regge**: prezzo di rivendita realistico − commissioni − spedizione −
   eventuali perizie o restauri, contro il prezzo d'acquisto (`scripts/margine.py`).

Un oggetto bello ma senza nome, senza epoca dimostrabile e senza mercato vale quanto il
suo uso decorativo: di solito poco.

## Manifatture e marchi che fanno prezzo (Italia e mondo)

Un nome nell'annuncio non è una prova (i marchi famosi sono i più falsificati), ma è il
primo segnale da verificare. Esempi per settore:

| Settore | Italia | Resto del mondo |
|---|---|---|
| Porcellane e ceramiche | Ginori / Richard-Ginori (e Gio Ponti), Real Fabbrica di Capodimonte, Lenci, Fornasetti, Bitossi, Vietri periodo tedesco | Meissen, Sèvres, KPM Berlino, Nymphenburg, Herend, Royal Copenhagen, Rosenthal, Wedgwood, Royal Worcester, Moorcroft, Limoges (Haviland) |
| Vetro | Venini, Barovier & Toso, Seguso, Salviati, AVEM, Cenedese | Gallé, Daum, Lalique, Loetz, Moser, Baccarat, Orrefors, Kosta, Iittala |
| Argenti e metalli | Buccellati, argentieri antichi con punzoni di città | Christofle (spesso argentato), Puiforcat, Odiot, Georg Jensen, Tiffany, Fabergé, Gorham; bronzi Barbedienne, Susse, bronzi viennesi Bergman |
| Orologi | Panerai (vintage) | Patek Philippe, Vacheron Constantin, Audemars Piguet, Rolex, Omega, Longines, Jaeger-LeCoultre, Universal Genève, Heuer, Zenith, Cartier |
| Gioielli e moda | Bulgari, Buccellati, Gucci e Prada vintage | Cartier, Van Cleef & Arpels, Tiffany, Hermès, Chanel, Louis Vuitton |
| Penne | Aurora, Omas, Montegrappa | Montblanc, Parker, Waterman, Pelikan |
| Fotografia | — | Leica, Hasselblad, Rolleiflex, Zeiss, Nikon F |
| Giocattoli | Ingap, Lenci, Rivarossi, Mercury, Politoys | Märklin, Schuco, Steiff, Lehmann, Dinky, Corgi, Kenner, LEGO |
| Design | Cassina, Arteluce, FontanaArte, Flos, Artemide, Kartell, Olivetti, Brionvega, Gio Ponti, Sottsass | Thonet, Knoll, Vitra / Herman Miller (Eames), Fritz Hansen, Louis Poulsen, Braun |
| Strumenti musicali e hi-fi | liuteria italiana, Eko, Wandrè | Fender, Gibson, Martin, Selmer, Steinway; McIntosh, Marantz, Thorens, Revox, Bang & Olufsen |
| Arte orientale | — | porcellane cinesi con marchi di regno, Satsuma e Imari giapponesi, netsuke, cloisonné, bronzi e giade |

Per ogni settore la scheda della categoria (`categoria.py`) dice come verificare
l'autenticità e dove rivendere.

## Guida rapida alle epoche

I venditori usano i nomi degli stili a caso ("barocco" per qualunque curva, "impero" per
qualunque cosa dorata). Lo stile dice solo il **modello**: molti stili sono stati ripresi
nell'Ottocento e nel Novecento ("in stile"). L'epoca reale la dicono costruzione, materiali
e usura (vedi `../metodo-perizia.md`).

| Stile | Periodo originale | Come si riconosce | Ripreso (attenzione) |
|---|---|---|---|
| Barocco | Seicento – primo Settecento | forme pesanti, volute, intagli profondi, putti, colonne tortili | sì, molto, fine '800 e '900 |
| Rococò / Luigi XV | circa 1730–1770 | curve asimmetriche, conchiglie (rocaille), gambe mosse, laccature, a Napoli e Venezia molto decorato | sì, molto ("Luigi XV" da negozio) |
| Neoclassico / Luigi XVI | circa 1770–1800 | linee dritte, gambe affusolate e scanalate, festoni, nastri, medaglioni, motivi da Ercolano e Pompei | sì |
| Impero / Direttorio | circa 1795–1820 (a Napoli sotto i Murat) | mogano, bronzi dorati applicati, cigni, sfingi, aquile, palmette, colonne | sì, molto |
| Restaurazione / Carlo X / Biedermeier | circa 1815–1840 | linee semplici e comode, legni chiari (noce, ciliegio), poco bronzo | poco |
| Luigi Filippo | circa 1830–1850 | mobili borghesi in noce o mogano, curve morbide, specchiere | sì |
| Napoleone III / eclettismo | circa 1850–1890 | mescolanza di stili precedenti, ebanizzato con intarsi, bronzo dorato, porcellane applicate, ricchezza | è già esso stesso una ripresa |
| Liberty / Art Nouveau | circa 1890–1915 | fiori, steli e figure femminili sinuose, linee a colpo di frusta, vetri di Gallé e Daum | sì (anche riproduzioni recenti) |
| Déco | circa 1920–1940 | geometria, linee spezzate, materiali preziosi (radiche, lacche, avorio, cromo), figure stilizzate | sì |
| Novecento italiano / razionalismo | anni '20–'40 | forme classiche semplificate (Gio Ponti), mobili razionalisti in tubolare | poco |
| Modernariato | anni '50–'70 | plastiche, colori vivi, forme organiche, design firmato | riedizioni ufficiali e copie |

Indizi rapidi di età nel mobile e negli oggetti (dettagli in `../metodo-perizia.md`): viti a
croce = dopo gli anni '30; compensato e truciolare = Novecento; segni di sega circolare = dopo
la metà dell'Ottocento; incastri a coda di rondine irregolari = lavoro a mano.

## Esempi: specialità regionali italiane

Ogni regione italiana ha specialità con un mercato da collezione. Quelle che seguono sono
esempi del Sud, frequenti nelle zone di ritiro; lo stesso metodo vale per le specialità di
altre regioni e di altri Paesi.

### Presepe napoletano

Il collezionismo di pastori napoletani del Settecento e dell'Ottocento è un mercato vero,
con case d'asta dedicate. Negli sgomberi campani compaiono spesso pastori vecchi mescolati
a quelli moderni di San Gregorio Armeno.

- **Pastore antico (Settecento–Ottocento)**: testa, mani e spesso piedi in **terracotta
  dipinta**, **occhi di vetro** nelle figure migliori, corpo in **stoppa e fil di ferro**
  (snodabile), arti in legno, **abiti in tessuti d'epoca** cuciti a mano (seta, broccati).
  Le teste dei maestri hanno espressioni realistiche e intense.
- **Maestri** citati nei cataloghi d'asta: Giuseppe Sanmartino, Francesco Celebrano,
  Lorenzo Mosca, Salvatore Di Franco, Giuseppe Gori, Nicola Ingaldi; per gli animali
  Francesco Gallo e Saverio Vassallo. Le attribuzioni sono materia da specialisti:
  scrivi "scuola napoletana, XVIII secolo" finché non hai un parere.
- **Finimenti**: cesti, strumenti musicali, armi, gioielli e ceste di frutta in miniatura,
  in argento, legno o cera. Anche da soli hanno mercato.
- **Moderno**: figure tutte in terracotta o resina, abiti incollati o dipinti, colori
  vivaci uniformi. Valore decorativo, basso.
- **Foto da chiedere**: testa e mani da vicino, sotto gli abiti (stoppa e fil di ferro?),
  base o piedi, cuciture.
- **Dove vendere**: case d'asta con aste di arte presepiale (Napoli, Roma), Catawiki,
  collezionisti e associazioni del presepe; i pastori modesti su eBay e Subito.

### Corallo e cammei (Torre del Greco)

Torre del Greco è il centro mondiale della lavorazione del corallo e dei cammei.

- **Corallo rosso mediterraneo** (*Corallium rubrum*): venature parallele visibili con la
  lente, freddo al tatto, colore non perfettamente uniforme. Il rosa pallido "pelle
  d'angelo" e il rosso intenso "sangue di bue" valgono di più. Le collane antiche a grani
  grossi possono valere molto.
- **Falsi e sostituti**: plastica (leggera, tiepida, linee di stampo), vetro, corallo
  bambù tinto (venature diverse, colore troppo uniforme), polvere di corallo ricostruita.
- **Cammei**: incisi in **conchiglia** (i più comuni: sardonica, corniola), in **pietra
  dura** (agata, onice: più pregiati), in **lava vesuviana** (souvenir del Grand Tour,
  Ottocento, ricercati dai collezionisti), in **corallo**. Il valore dipende dalla qualità
  dell'incisione (finezza dei capelli, delle mani, del profilo), dal soggetto, dalla firma e
  dalla montatura (oro antico, punzoni).
- **Segnali d'epoca**: montature in oro basso titolo con punzoni antichi, spilla con
  "chiusura a C" senza sicura (Ottocento), soggetti mitologici; i cammei moderni in serie
  hanno soggetti standard e incisione più povera.
- **Legge**: il corallo rosso mediterraneo non è vietato come l'avorio, ma verifica sempre
  le regole aggiornate se spedisci fuori dall'UE.
- **Dove vendere**: aste di gioielli, commercianti di Torre del Greco, Catawiki, eBay.

### Ceramica di Vietri e maiolica campana

- **Vietri sul Mare**: la produzione turistica moderna vale poco. Vale molto il
  **"periodo tedesco"** (anni '20–'40): artisti stranieri come Richard Dölker e Irene
  Kowaliska e la manifattura **ICS (Industria Ceramica Salernitana)**. Poi Guido Gambone
  (dagli anni '30) e la Solimene. Cerca marchi e sigle sotto il pezzo, soggetti con
  figure stilizzate, asinelli, paesaggi della costiera dipinti con tratto moderno.
- **Cerreto Sannita e San Lorenzello** (Benevento): maioliche dal Seicento all'Ottocento,
  colori caldi (giallo, arancio, verde ramina, blu), soggetti devozionali e decorazioni
  vegetali. Antiche e rare; molte imitazioni moderne.
- **Ariano Irpino**: maiolica popolare antica (colori brillanti, verde e giallo).
- **Napoli**: porcellane della Real Fabbrica (vedi `ceramiche-vetri.md`), maioliche
  napoletane del Settecento (Giustiniani nell'Ottocento).
- Per i marchi: De Mauri, *L'amatore di maioliche e porcellane*, e Chaffers (`ceramica-*`).

### Arte sacra ed ex voto

- **Argenti sacri**: calici, ostensori, reliquiari, corone di statue, ex voto in lamina
  d'argento sbalzata (cuori, gambe, occhi). Gli argenti napoletani antichi hanno i
  punzoni della città (sigla NAP coronata) e del console dell'arte: verificali sui manuali
  (Rosenberg) prima di pagare più del peso.
- **Ex voto dipinti**: tavolette con naufragi, incidenti, guarigioni, con la scritta
  "V.F.G.A." (voto fatto, grazia ricevuta). Arte popolare ricercata, specie se marinara.
- **Statue e busti lignei**, **acquasantiere**, **paliotti**, **paramenti** in seta ricamata.
- **Legge (importante)**: l'arte sacra è tra le categorie più rubate. Se ci sono timbri
  di parrocchie o confraternite, numeri d'inventario, o il venditore non sa dire da dove
  viene, controlla la banca dati dei Carabinieri TPC (app iTPC) prima di comprare.

### Fotografie d'epoca

L'Italia del Grand Tour (Napoli, Roma, Firenze, Venezia) ha prodotto una quantità enorme di fotografie ottocentesche di
qualità, spesso finite in cassetti e album di famiglia.

- **Tecniche, dalla più antica**: dagherrotipo (immagine su lastra a specchio, in custodia,
  anni 1840–1860), ambrotipo (su vetro, in custodia), ferrotipo (su latta), **stampe
  all'albumina** (carta sottile, toni bruno-seppia, montate su cartoncino, 1850–1895),
  carte de visite e carte cabinet (formati su cartoncino con il nome dello studio sul retro).
- **Fotografi che valgono**: **Giorgio Sommer** e **Roberto Rive** (Napoli), Alphonse
  Bernoud, i fratelli Alinari e Giacomo Brogi (Firenze), Carlo Naya (Venezia). Le vedute di
  Napoli, Pompei, del Vesuvio in eruzione e i "tipi" popolari napoletani sono le più
  richieste. Spesso il nome e il numero sono scritti nel negativo, in basso.
- **Attenzione**: ristampe moderne da negativi antichi e riproduzioni fotomeccaniche
  (con la lente si vede il retino).
- **Dove vendere**: aste di fotografia, Catawiki, eBay internazionale, Delcampe per le
  carte de visite.

## Piccoli oggetti di pregio

Oggetti piccoli, spesso dimenticati nei cassetti: tabacchiere, portasigarette e
portacipria in argento o smalto, astucci, carnet de bal, ventagli (con stecche in avorio o
madreperla e pagina dipinta), bastoni da passeggio con pomo d'argento o intagliato, sigilli,
calamai, temperini, bomboniere d'argento antiche.

- **Valore**: firma o punzoni (argentiere, città), qualità dello smalto o dell'intaglio,
  materiali, condizioni.
- **Manuali**: De Mauri, *L'amatore di oggetti d'arte e di curiosità* (tabacchiere, ventagli,
  cammei, oggetti di curiosità), Rosenberg e Jackson per i punzoni.
- **Legge**: ventagli e bastoni con avorio o tartaruga ricadono sotto CITES.
