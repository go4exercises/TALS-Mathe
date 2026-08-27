import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const SEL = '.fl-eq, .ll-val, .lt-frage, .zs-formel, .fl-eval, .cr, .lt-antwort, [id$="-eq"], [id$="-val"], [id$="-info"], [id$="-formel"], [id$="-asym"]';
const browser = await chromium.launch();
const treffer = new Map();
for (const seite of process.argv.slice(2)) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  for (let runde = 0; runde < 3; runde++) {
    const texte = await page.$$eval(SEL, els => els.map(e => e.innerText.replace(/\s+/g,' ').trim()));
    for (const t of texte) if (t.includes('·')) {
      const k = seite + ' :: ' + t.slice(0, 150);
      if (!treffer.has(k)) treffer.set(k, true);
    }
    await page.evaluate(r => {
      document.querySelectorAll('input[type=range]').forEach(x => {
        const min=+x.min||0, max=+x.max||100, st=+x.step||1;
        x.value = String(Math.min(max, Math.max(min, min + (max-min)*(r+1)/4)));
        x.dispatchEvent(new Event('input',{bubbles:true})); x.dispatchEvent(new Event('change',{bubbles:true}));
      });
      document.querySelectorAll('.typ-btn, .preset-btn, button[data-kuh], .zs-btn').forEach((b,i)=>{ if(i===r) b.click(); });
    }, runde);
    await page.waitForTimeout(250);
  }
  await page.close();
}
await browser.close();
for (const k of [...treffer.keys()].sort()) console.log(k);
console.log('\n' + treffer.size + ' Anzeigen mit ·');
