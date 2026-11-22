#!/usr/bin/env node
// Scarica pagine di risultati di Subito.it con un browser vero (Playwright) e stampa
// un annuncio per riga in JSON. Legge da stdin un array JSON di {url, zona, query}.
// Ritmo prudente: una pagina alla volta, pausa casuale tra le richieste.
// Uso: echo '[{"url":"https://www.subito.it/annunci-campania/vendita/usato/?q=quadro&order=datedesc","zona":"campania","query":"quadro"}]' | node subito_fetch.js
const { chromium } = require('playwright');

function leggiStdin() {
  return new Promise((ok) => { let s = ''; process.stdin.on('data', (d) => (s += d)); process.stdin.on('end', () => ok(s)); });
}
const attesa = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const richieste = JSON.parse(await leggiStdin());
  const pausaMin = Number(process.env.PAUSA_MIN_MS || 3000), pausaMax = Number(process.env.PAUSA_MAX_MS || 6000);
  const browser = await chromium.launch();
  const pagina = await browser.newPage({ locale: 'it-IT' });
  let errori = 0;
  for (const [i, r] of richieste.entries()) {
    try {
      const risp = await pagina.goto(r.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      if (risp.status() !== 200) throw new Error('HTTP ' + risp.status());
      const testo = await pagina.evaluate(() => document.getElementById('__NEXT_DATA__')?.textContent || '');
      const items = JSON.parse(testo || '{}')?.props?.pageProps?.initialState?.items?.originalList || [];
      for (const a of items) {
        const f = a.features || {};
        const prezzo = f['/price']?.values?.[0]?.key;
        console.log(JSON.stringify({
          id: (a.urn || '').split(':').pop(), titolo: a.subject || '', testo: a.body || '',
          prezzo: prezzo !== undefined ? Number(prezzo) : null, data: a.date || '',
          categoria_subito: a.category?.label || '', url: a.urls?.default || '',
          comune: a.geo?.town?.value || '', provincia: a.geo?.city?.shortName || '',
          azienda: !!a.advertiser?.company, n_foto: (a.images || []).length,
          foto: (a.images || []).slice(0, 3).map((x) => x.cdnBaseUrl + '?rule=gallery-desktop-2x-auto'),
          condizione: f['/item_condition']?.values?.[0]?.value || '',
          spedizione: f['/item_shippable']?.values?.[0]?.key === '1', zona: r.zona, query: r.query,
        }));
      }
      process.stderr.write(`[${i + 1}/${richieste.length}] ${r.zona} "${r.query}": ${items.length} annunci\n`);
    } catch (e) {
      errori++;
      process.stderr.write(`[${i + 1}/${richieste.length}] ERRORE ${r.zona} "${r.query}": ${e.message}\n`);
      if (errori >= 5) { process.stderr.write('Troppi errori: mi fermo (possibile blocco del sito).\n'); break; }
    }
    if (i < richieste.length - 1) await attesa(pausaMin + Math.random() * (pausaMax - pausaMin));
  }
  await browser.close();
})();
