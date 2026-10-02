// Druckseite (HTML, A4) → PDF, mit fertig gesetzten Formeln.
//   node .claude/tools/druck-pdf.mjs downloads/…/gesamttest.html [weitere.html …]
// Schreibt <name>.pdf neben die HTML-Datei. Liest per file:// — kein Server nötig.
// Wartet auf MathJax (startup.promise) und auf data-diagram-Container, druckt mit
// der @page-Grösse aus print.css (A4, 14 mm Rand); .no-print verschwindet im Druck.
import { chromium } from 'playwright';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const dateien = process.argv.slice(2);
if (!dateien.length) { console.error('Aufruf: node .claude/tools/druck-pdf.mjs <seite.html> …'); process.exit(1); }
const browser = await chromium.launch();
let fehler = 0;
for (const d of dateien) {
  const seite = await browser.newPage();
  const probleme = [];
  seite.on('pageerror', e => probleme.push(e.message));
  seite.on('requestfailed', r => probleme.push('nicht geladen: ' + r.url()));
  await seite.goto(pathToFileURL(path.resolve(d)).href, { waitUntil: 'load' });
  await seite.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 15000 });
  await seite.evaluate(() => MathJax.startup.promise);
  await seite.waitForFunction(() => [...document.querySelectorAll('[data-diagram]')].every(c => c.querySelector('svg')), null, { timeout: 15000 });
  const merror = await seite.$$eval('mjx-merror', e => e.length);
  if (merror) probleme.push(merror + ' Formel(n) mit Fehler');
  const ziel = d.replace(/\.html$/, '.pdf');
  await seite.pdf({ path: ziel, preferCSSPageSize: true, printBackground: true });
  console.log((probleme.length ? '  FEHLER ' : '  ok     ') + ziel + (probleme.length ? '\n         ' + probleme.join('\n         ') : ''));
  fehler += probleme.length;
  await seite.close();
}
await browser.close();
process.exit(fehler ? 1 : 0);
