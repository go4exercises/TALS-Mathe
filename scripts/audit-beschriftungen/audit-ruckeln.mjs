// Ruckel-Prüfung über alle Themenseiten.
//
// Zwei Messungen je Seite:
//   A  Regler: für jeden <input type=range> werden 12 input-Ereignisse mit
//      wechselndem Wert ausgelöst und die Dauer des synchronen Handlers
//      gemessen. Nebenbei gezählt: getImageData (GPU-Readback) und
//      MathJax-Typesets. Ein Bild dauert bei 60 Hz 16.7 ms — alles darüber
//      ist als Stocken sichtbar.
//   B  Dauer-Animationen: 1.5 s lang die Abstände zwischen requestAnimationFrame
//      messen und die langen Bilder zählen.
//
// Aufruf vom Mathe-Repo-Root, Server auf 8001:
//   node scripts/audit-beschriftungen/audit-ruckeln.mjs
//
// Gegen ein anderes TALS-Repo (rein lesend, es wird dort nichts geschrieben):
//   cd /pfad/zum/anderen/repo && python3 -m http.server 8002 &
//   node scripts/audit-beschriftungen/audit-ruckeln.mjs \
//        --root /pfad/zum/anderen/repo --basis http://localhost:8002/
// Die Seitenordner werden erkannt (themen/ in Physik, grundlagen/+schwerpunkt/
// in Mathe); Playwright wird aus dem Mathe-Repo aufgeloest.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
const ROOT = arg('--root') || '.';
const BASIS = arg('--basis') || 'http://localhost:8001/';
const AUSGABE = arg('--out') ||
  '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad/ruckeln.json';

const ORDNER = ['themen', 'grundlagen', 'schwerpunkt']
  .filter(d => fs.existsSync(path.join(ROOT, d)));
if (!ORDNER.length) { console.error('[FEHLER] keine Seitenordner in ' + ROOT); process.exit(2); }
const seiten = ORDNER.flatMap(d =>
  fs.readdirSync(path.join(ROOT, d)).filter(f => f.endsWith('.html')).map(f => d + '/' + f)).sort();
console.log(`${seiten.length} Seiten aus ${ORDNER.join(', ')} unter ${BASIS}\n`);

const MESSER = () => {
  window.__M = { readbacks: 0, mathjax: 0, resizes: 0 };
  const o = CanvasRenderingContext2D.prototype.getImageData;
  CanvasRenderingContext2D.prototype.getImageData = function (...a) { window.__M.readbacks++; return o.apply(this, a); };
  // Canvas-Grösse neu setzen bedeutet Puffer neu anlegen und löschen
  const d = Object.getOwnPropertyDescriptor(HTMLCanvasElement.prototype, 'width');
  Object.defineProperty(HTMLCanvasElement.prototype, 'width', {
    get: d.get,
    set(v) { if (this.width !== v) window.__M.resizes++; d.set.call(this, v); },
    configurable: true,
  });
  const warte = setInterval(() => {
    if (window.MathJax && MathJax.typesetPromise && !MathJax.__gezaehlt) {
      const t = MathJax.typesetPromise.bind(MathJax);
      MathJax.typesetPromise = (...a) => { window.__M.mathjax++; return t(...a); };
      MathJax.__gezaehlt = true;
      clearInterval(warte);
    }
  }, 100);
};

const browser = await chromium.launch();
const ergebnis = [];

for (const [i, rel] of seiten.entries()) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  await ctx.addInitScript(MESSER);
  const page = await ctx.newPage();
  const jsFehler = [];
  page.on('pageerror', e => jsFehler.push(String(e).slice(0, 120)));
  try {
    await page.goto(BASIS + rel, { waitUntil: 'load', timeout: 45000 });
    await page.evaluate(async () => {
      for (const c of document.querySelectorAll('canvas')) {
        c.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 30));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(1200);

    // ── A  Regler ──────────────────────────────────────────
    const regler = await page.evaluate(async () => {
      const raus = [];
      const sl = [...document.querySelectorAll('input[type=range]')];
      for (const s of sl) {
        if (s.offsetParent === null) continue;          // unsichtbar -> nicht bedienbar
        const min = parseFloat(s.min || 0), max = parseFloat(s.max || 100);
        const step = parseFloat(s.step || 1) || (max - min) / 20;
        const start = parseFloat(s.value);
        const m0 = { ...window.__M };
        const zeiten = [];
        for (let k = 0; k < 12; k++) {
          const v = min + ((max - min) * ((k + 1) / 13));
          s.value = String(Math.round(v / step) * step);
          const t0 = performance.now();
          s.dispatchEvent(new Event('input', { bubbles: true }));
          zeiten.push(performance.now() - t0);
          await new Promise(r => setTimeout(r, 0));
        }
        s.value = String(start);
        s.dispatchEvent(new Event('input', { bubbles: true }));
        zeiten.sort((a, b) => a - b);
        raus.push({
          id: s.id || s.name || '(ohne id)',
          median: +zeiten[Math.floor(zeiten.length / 2)].toFixed(2),
          max: +zeiten[zeiten.length - 1].toFixed(2),
          readbacks: Math.round((window.__M.readbacks - m0.readbacks) / 12),
          mathjax: +((window.__M.mathjax - m0.mathjax) / 12).toFixed(1),
          resizes: +((window.__M.resizes - m0.resizes) / 12).toFixed(1),
        });
      }
      return raus;
    });

    // ── B  Dauer-Animationen ───────────────────────────────
    const frames = await page.evaluate(() => new Promise(res => {
      const t = []; let last = performance.now(); const bis = last + 1500;
      (function tick(now) {
        t.push(now - last); last = now;
        if (now < bis) requestAnimationFrame(tick); else {
          t.shift();
          if (!t.length) return res({ bilder: 0, lang: 0, schlimmstes: 0 });
          res({ bilder: t.length, lang: t.filter(x => x > 22).length,
                schlimmstes: +Math.max(...t).toFixed(1) });
        }
      })(performance.now());
    }));

    ergebnis.push({ seite: rel, regler, frames, jsFehler });
    const schlimm = regler.reduce((m, r) => Math.max(m, r.max), 0);
    const rb = regler.reduce((m, r) => Math.max(m, r.readbacks), 0);
    const mj = regler.reduce((m, r) => Math.max(m, r.mathjax), 0);
    process.stdout.write(
      `[${String(i + 1).padStart(2)}/${seiten.length}] ${rel.split('/')[1].padEnd(46)}` +
      `${String(regler.length).padStart(2)} Regler  max ${String(schlimm.toFixed(1)).padStart(6)} ms` +
      `  Readback ${String(rb).padStart(3)}  MathJax ${String(mj).padStart(4)}` +
      `  lange Bilder ${frames.lang}/${frames.bilder}\n`);
  } catch (e) {
    ergebnis.push({ seite: rel, fehler: String(e).slice(0, 150) });
    process.stdout.write(`[${i + 1}/${seiten.length}] ${rel} FEHLER\n`);
  }
  await ctx.close();
}
await browser.close();
fs.writeFileSync(AUSGABE, JSON.stringify(ergebnis, null, 1));
console.log('\nRohdaten: ' + AUSGABE);
