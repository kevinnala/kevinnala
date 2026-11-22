#!/usr/bin/env node
// Legge pagine di ricerca di Vinted con un browser vero e stampa un annuncio per riga in JSON.
// Usa solo la pagina pubblica (le schede degli annunci), non chiamate dirette alle API.
// Input da stdin: array JSON di {url, query}. Ritmo prudente come per Subito.
const { chromium } = require('playwright');

function leggiStdin() {
  return new Promise((ok) => { let s = ''; process.stdin.on('data', (d) => (s += d)); process.stdin.on('end', () => ok(s)); });
}
const attesa = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const richieste = JSON.parse(await leggiStdin());
  const browser = await chromium.launch();
  const pagina = await browser.newPage({ locale: 'it-IT' });
  let errori = 0;
  for (const [i, r] of richieste.entries()) {
    try {
      const risp = await pagina.goto(r.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      if (risp.status() !== 200) throw new Error('HTTP ' + risp.status());
      await pagina.waitForTimeout(2500);
      const schede = await pagina.evaluate(() =>
        [...document.querySelectorAll('a[data-testid$="--overlay-link"][href*="/items/"]')].map((a) => ({
          href: a.href.split('?')[0], titolo: a.getAttribute('title') || '', testid: a.getAttribute('data-testid') || '',
          img: (a.closest('[data-testid*="grid-item"]') || a.parentElement).querySelector('img')?.src || '',
        })));
      for (const s of schede) {
        // "Titolo, Condizioni: Ottime, [Taglia: ..., ]10.00 €, 11.20 €"
        const m = s.titolo.match(/^(.*?), Condizioni: ([^,]*)(?:, .*?)?, ([\d.]+) €, ([\d.]+) €$/);
        const id = (s.testid.match(/product-item-id-(\d+)/) || [])[1] || '';
        console.log(JSON.stringify({
          id: 'vt-' + id, fonte: 'Vinted', titolo: m ? m[1] : s.titolo, testo: '',
          prezzo: m ? Number(m[3]) : null, data: '', categoria_subito: '', url: s.href,
          comune: '', provincia: '', locale: false, azienda: false, n_foto: s.img ? 1 : 0,
          foto: s.img ? [s.img] : [], condizione: m ? m[2] : '', spedizione: true, zona: 'Vinted', query: r.query,
        }));
      }
      process.stderr.write(`[Vinted ${i + 1}/${richieste.length}] "${r.query}": ${schede.length} annunci\n`);
    } catch (e) {
      errori++;
      process.stderr.write(`[Vinted ${i + 1}/${richieste.length}] ERRORE "${r.query}": ${e.message}\n`);
      if (errori >= 5) { process.stderr.write('Vinted: troppi errori, mi fermo.\n'); break; }
    }
    if (i < richieste.length - 1) await attesa(3000 + Math.random() * 3000);
  }
  await browser.close();
})();
