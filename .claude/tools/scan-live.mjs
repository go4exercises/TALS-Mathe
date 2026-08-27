// Liest den GESAMTEN sichtbaren Text jeder Seite aus — im Startzustand, nach dem
// Ziehen aller Regler und nach dem Klick auf jeden Umschalt-Knopf — und meldet
// jede Zeile mit einem '·'. So werden auch Anzeigen erfasst, die erst beim
// Bedienen entstehen (Preset-Beschreibungen, Sonderfall-Zweige).
//   node .claude/tools/scan-live.mjs grundlagen/*.html schwerpunkt/*.html
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const BTN = '.typ-btn, .preset-btn, .zs-btn, .fall-btn, .btn-typ, [data-kuh], .kk-btn, .lt-weiter';
const browser = await chromium.launch();
const treffer = new Map();
for (const seite of process.argv.slice(2)) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on('pageerror', e => console.log(`!! ${seite}: ${e.message}`));
  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const anzahlBtn = await page.$$eval(BTN, b => b.length);
  for (let runde = 0; runde <= Math.min(anzahlBtn, 12); runde++) {
    const text = await page.evaluate(() => document.body.innerText);
    for (const z of text.split('\n')) {
      const t = z.replace(/\s+/g, ' ').trim();
      if (t.includes('·')) treffer.set(seite + ' :: ' + t.slice(0, 160), true);
    }
    await page.evaluate(([r, sel]) => {
      document.querySelectorAll('input[type=range]').forEach(x => {
        const mi = +x.min || 0, ma = +x.max || 100;
        x.value = String(mi + (ma - mi) * ((r % 4) + 1) / 5);
        x.dispatchEvent(new Event('input', { bubbles: true }));
        x.dispatchEvent(new Event('change', { bubbles: true }));
      });
      const btns = document.querySelectorAll(sel);
      if (btns[r]) btns[r].click();
    }, [runde, BTN]);
    await page.waitForTimeout(200);
  }
  await page.close();
}
await browser.close();
for (const k of [...treffer.keys()].sort()) console.log(k);
console.log(`\n${treffer.size} sichtbare Zeilen mit ·`);
