// Zählt 20 000 Würfe je Übungstyp: Schlüssel, Sperrtreffer (vor der Sperre), Verteilung der Sollwerte.
import path from 'node:path';
import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage();
await p.route('**/vendor/mathjax/**', r => r.abort());
await p.goto('file://' + path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../../leitprogramme/kreis-kreisteile.html')); await p.waitForTimeout(800);
const r = await p.evaluate(() => {
  const aus = {};
  document.querySelectorAll('.uebung[data-typ]').forEach(box => {
    const T = box.__typ, typ = box.dataset.typ, n = 20000, schl = {}, soll = {}; let ohne = 0;
    for (let i = 0; i < n; i++){ const A = T.neu(); const k = T.schl ? T.schl(A) : '-'; schl[k] = (schl[k] || 0) + 1;
      const s = JSON.stringify(A.soll); soll[s] = (soll[s] || 0) + 1; }
    const top = Object.entries(soll).sort((a, b) => b[1] - a[1]).slice(0, 4).map(e => e[0] + ':' + (e[1] / n * 100).toFixed(1) + '%');
    aus[typ] = { schluessel: Object.keys(schl).length, sollwerte: Object.keys(soll).length, top };
  });
  return aus;
});
console.log(JSON.stringify(r, null, 1));
await b.close();
