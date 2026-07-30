// Erzeugt je auffälligem Canvas ein Kontrollbild: Canvas 2x vergrössert,
// die beanstandeten Textfelder rot umrahmt.
import { chromium } from 'playwright';
import fs from 'node:fs';

const SC = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad';
const OUT = SC + '/audit-crops';
fs.mkdirSync(OUT, { recursive: true });
const instrument = fs.readFileSync('scripts/audit-beschriftungen/audit-instrument.js', 'utf-8');
const kand = JSON.parse(fs.readFileSync(SC + '/audit-kandidaten.json', 'utf-8'));

// nach Seite -> Canvas -> Boxen gruppieren
const proSeite = new Map();
for (const b of kand) {
  if (!proSeite.has(b.seite)) proSeite.set(b.seite, new Map());
  const m = proSeite.get(b.seite);
  if (!m.has(b.canvas)) m.set(b.canvas, []);
  if (b.b) m.get(b.canvas).push(b.b);
}

const browser = await chromium.launch();
let n = 0;
for (const [seite, canvases] of proSeite) {
  // deviceScaleFactor MUSS 1 sein wie im Messlauf — sonst ist der Canvas-Puffer
  // doppelt so gross und die aufgezeichneten Boxen landen auf halber Position.
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await ctx.addInitScript(instrument);
  const page = await ctx.newPage();
  await page.goto('http://localhost:8001/' + seite, { waitUntil: 'load', timeout: 45000 });
  await page.evaluate(async () => {
    for (const c of document.querySelectorAll('canvas')) {
      c.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 45));
    }
  });
  await page.waitForTimeout(900);

  for (const [cvId, boxen] of canvases) {
    const ok = await page.evaluate(({ cvId, boxen }) => {
      const cv = document.getElementById(cvId);
      if (!cv) return false;
      // Overlay exakt über dem Canvas, Boxen in CSS-Pixel umrechnen
      const r = cv.getBoundingClientRect();
      const sx = r.width / cv.width, sy = r.height / cv.height;
      const ov = document.createElement('div');
      ov.id = '__audit-ov';
      ov.style.cssText = `position:absolute; left:${r.left + scrollX}px; top:${r.top + scrollY}px;
        width:${r.width}px; height:${r.height}px; pointer-events:none; z-index:9999;`;
      for (const b of boxen) {
        const d = document.createElement('div');
        d.style.cssText = `position:absolute; left:${b.x0 * sx}px; top:${b.y0 * sy}px;
          width:${(b.x1 - b.x0) * sx}px; height:${(b.y1 - b.y0) * sy}px;
          outline:1.5px solid #e00; outline-offset:1px;`;
        ov.appendChild(d);
      }
      document.body.appendChild(ov);
      cv.scrollIntoView({ block: 'center' });
      return true;
    }, { cvId, boxen });
    if (!ok) { console.log('  fehlt:', seite, cvId); continue; }
    await page.waitForTimeout(120);
    const cv = await page.$(`#${cvId}`);
    const box = await cv.boundingBox();
    await page.screenshot({
      path: `${OUT}/${seite.split('/')[1].replace('.html', '')}__${cvId}.png`,
      clip: { x: box.x - 6, y: box.y - 6, width: box.width + 12, height: box.height + 12 },
    });
    await page.evaluate(() => document.getElementById('__audit-ov')?.remove());
    n++;
  }
  await ctx.close();
}
await browser.close();
console.log(`${n} Kontrollbilder in ${OUT}`);
