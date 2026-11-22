#!/usr/bin/env node
// Aste giudiziarie di beni mobili su Fallcoaste.it (pagine pubbliche, browser vero, ritmo lento).
// Legge da stdin {"elenchi": [url...], "pagine": N, "visti": [id...], "max_lotti": N}
// e stampa un lotto per riga in JSON, nello stesso formato degli annunci dello scanner.
// Apre solo le schede dei lotti non ancora visti.
const { chromium } = require('playwright');

const attesa = (ms) => new Promise((r) => setTimeout(r, ms));
function leggiStdin() {
  return new Promise((ok) => { let s = ''; process.stdin.on('data', (d) => (s += d)); process.stdin.on('end', () => ok(s)); });
}
const euro = (s) => { if (!s) return null; const n = Number(s.replace(/\./g, '').replace(',', '.')); return isNaN(n) ? null : n; };

(async () => {
  const cfg = JSON.parse(await leggiStdin());
  const visti = new Set(cfg.visti || []);
  const browser = await chromium.launch();
  const p = await browser.newPage({ locale: 'it-IT' });
  const lotti = new Map();
  for (const base of cfg.elenchi) {
    for (let pg = 1; pg <= (cfg.pagine || 2); pg++) {
      const url = pg === 1 ? base : `${base}${base.includes('?') ? '&' : '?'}page=${pg}`;
      try {
        const r = await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
        if (r.status() !== 200) throw new Error('HTTP ' + r.status());
        const links = await p.evaluate(() => [...document.querySelectorAll('a[href*="/vendita/"]')].map((a) => a.href));
        let nuovi = 0;
        for (const l of links) {
          const m = l.match(/-(\d{6,})\.html/);
          if (!m || !/www\.fallcoaste\.it\/vendita\//.test(l)) continue;
          const id = 'fc-' + m[1];
          if (!lotti.has(id)) { lotti.set(id, l); nuovi++; }
        }
        process.stderr.write(`[Fallcoaste elenco p.${pg}] ${nuovi} lotti\n`);
        if (!nuovi) break;
      } catch (e) {
        process.stderr.write(`[Fallcoaste elenco] ERRORE ${e.message}\n`);
        break;
      }
      await attesa(2500 + Math.random() * 2500);
    }
  }
  let aperti = 0;
  for (const [id, url] of lotti) {
    if (visti.has(id)) continue;
    if (aperti >= (cfg.max_lotti || 60)) break;
    aperti++;
    try {
      await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      const d = await p.evaluate(() => ({
        testo: document.body.innerText,
        foto: [...new Set([...document.querySelectorAll('img, a')].map((x) => x.src || x.href || '')
          .filter((s) => /cloudfront\.net\/.+\.(jpe?g|png)$/i.test(s)))],
      }));
      const t = d.testo;
      const trova = (re) => (t.match(re) || [])[1]?.trim() || '';
      const titolo = (t.split('\n').map((s) => s.trim()).filter(Boolean)
        .find((s, i, arr) => i > 0 && arr[i - 1].startsWith('Home')) || '').replace(/^Home.*$/, '');
      const titoloOk = titolo || trova(/Descrizione del bene\s*\n([^\n]+)/);
      const ubic = trova(/Ubicaz\.:\s*\n?([^\n]+)/);
      const prov = (ubic.match(/\(([A-Z]{2})\)/) || [])[1] || '';
      const offerta = euro(trova(/Miglior offerta €:\s*\n?\s*([\d.,]+)/));
      const base = euro(trova(/Prezzo base:\s*€\s*([\d.,]+)/));
      const totale = euro(trova(/Prezzo base totale:\s*€\s*([\d.,]+)/));
      const descr = trova(/Descrizione del bene\s*\n([\s\S]{0,1500}?)\n(?:Continua a leggere|Per partecipare)/);
      console.log(JSON.stringify({
        id, fonte: 'Asta giudiziaria (Fallcoaste)', titolo: titoloOk.slice(0, 200), testo: descr,
        prezzo: offerta || base, prezzo_con_oneri: totale,
        data: new Date().toISOString().slice(0, 19).replace('T', ' '),
        termine: trova(/Termine vendita:\s*([^\n]+)/), tribunale: trova(/Tribunale:\s*([^\n]+)/),
        categoria_subito: 'asta giudiziaria', url, comune: ubic, provincia: prov, azienda: false,
        n_foto: d.foto.length, foto: d.foto.slice(0, 6), condizione: 'visto e piaciuto, senza garanzia',
        spedizione: /spedi/i.test(descr), zona: 'Fallcoaste', query: 'aste giudiziarie',
      }));
    } catch (e) {
      process.stderr.write(`[Fallcoaste lotto] ERRORE ${url}: ${e.message}\n`);
    }
    await attesa(2000 + Math.random() * 2000);
  }
  process.stderr.write(`[Fallcoaste] lotti in elenco ${lotti.size}, schede aperte ${aperti}\n`);
  await browser.close();
})();
