#!/usr/bin/env node
// Legge la pagina di uno o più annunci Subito (URL come argomenti) e stampa per ognuno
// un JSON con testo completo, prezzo e URL di tutte le foto. Usa i dati strutturati
// schema.org (application/ld+json, tipo Product) che Subito pubblica nella pagina.
const { chromium } = require('playwright');
const attesa = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const urls = process.argv.slice(2);
  const browser = await chromium.launch();
  const pagina = await browser.newPage({ locale: 'it-IT' });
  for (const [i, url] of urls.entries()) {
    try {
      const r = await pagina.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      const blocchi = await pagina.evaluate(() =>
        [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent));
      let prodotto = null;
      for (const b of blocchi) {
        try {
          const d = JSON.parse(b);
          const lista = d['@graph'] || [d];
          prodotto = prodotto || lista.find((x) => x['@type'] === 'Product');
        } catch (e) { /* blocco non valido: ignora */ }
      }
      if (!prodotto) throw new Error('dati annuncio non trovati (annuncio rimosso?)');
      const offerta = Array.isArray(prodotto.offers) ? prodotto.offers[0] : prodotto.offers || {};
      const id = (url.match(/-(\d+)\.htm/) || [])[1] || '';
      console.log(JSON.stringify({
        url, stato: r.status(), id, titolo: prodotto.name || '', testo: prodotto.description || '',
        prezzo: offerta.price !== undefined ? Number(offerta.price) : null,
        condizione: (offerta.itemCondition || '').split('/').pop(),
        foto: [].concat(prodotto.image || []),
      }));
    } catch (e) {
      console.log(JSON.stringify({ url, errore: e.message }));
    }
    if (i < urls.length - 1) await attesa(3000 + Math.random() * 3000);
  }
  await browser.close();
})();
