// Treiber: lädt alle Themenseiten über http://localhost:8001/, wertet die
// Canvas-Beschriftungen in der Startposition aus und schreibt Rohbefunde als JSON.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const OUT = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad';
const BASIS = 'http://localhost:8001/';
const instrument = fs.readFileSync('scripts/audit-beschriftungen/audit-instrument.js', 'utf-8');

const seiten = [
  ...fs.readdirSync('grundlagen').filter(f => f.endsWith('.html')).sort().map(f => 'grundlagen/' + f),
  ...fs.readdirSync('schwerpunkt').filter(f => f.endsWith('.html')).sort().map(f => 'schwerpunkt/' + f),
];

const browser = await chromium.launch();
const alles = [];

for (const [i, rel] of seiten.entries()) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await ctx.addInitScript(instrument);
  const page = await ctx.newPage();
  const jsFehler = [];
  page.on('pageerror', e => jsFehler.push(String(e).slice(0, 200)));

  try {
    await page.goto(BASIS + rel, { waitUntil: 'load', timeout: 45000 });
    // Alle Canvas in den Viewport bringen, damit IntersectionObserver-Autostarts zeichnen
    await page.evaluate(async () => {
      const cvs = [...document.querySelectorAll('canvas')];
      for (const c of cvs) { c.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 45)); }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(1200);
    const res = await page.evaluate(() => window.__auditAuswerten());
    // Sichtbare Position und Kapitelanker je Canvas für den Direktlink
    const meta = await page.evaluate(() => {
      const m = {};
      document.querySelectorAll('canvas').forEach(c => {
        let anker = '';
        let e = c;
        while (e && e !== document.body) {
          if (e.id && e.tagName !== 'CANVAS') { anker = e.id; break; }
          let p = e.previousElementSibling;
          while (p) { if (/^H2$/.test(p.tagName) && p.id) { anker = p.id; break; } p = p.previousElementSibling; }
          if (anker) break;
          e = e.parentElement;
        }
        if (!anker) {
          const h2 = [...document.querySelectorAll('.content h2[id]')]
            .filter(h => h.getBoundingClientRect().top + scrollY < c.getBoundingClientRect().top + scrollY).pop();
          anker = h2 ? h2.id : '';
        }
        const titel = (() => {
          const w = c.closest('.anim-widget, .widget, .aufgabe, section, div');
          const t = w && w.querySelector('.widget-titelzeile h3, h3, .anim-titel');
          return t ? t.textContent.replace(/\s+/g, ' ').trim().slice(0, 90) : '';
        })();
        m[c.id || 'ohne-id'] = { anker, titel, w: c.width, h: c.height,
                                 cssW: Math.round(c.getBoundingClientRect().width) };
      });
      return m;
    });
    alles.push({ seite: rel, jsFehler, meta, ...res });
    process.stdout.write(`[${String(i + 1).padStart(2)}/${seiten.length}] ${rel.padEnd(52)} ${res.canvases.length} Canvas, ${res.canvases.reduce((s, c) => s + c.texte.length, 0)} Texte\n`);
  } catch (e) {
    alles.push({ seite: rel, fehler: String(e).slice(0, 300), canvases: [], meta: {}, jsFehler });
    process.stdout.write(`[${String(i + 1).padStart(2)}/${seiten.length}] ${rel.padEnd(52)} FEHLER: ${String(e).slice(0, 90)}\n`);
  }
  await ctx.close();
}

await browser.close();
fs.writeFileSync(path.join(OUT, 'audit-roh.json'), JSON.stringify(alles));
const nTexte = alles.reduce((s, p) => s + p.canvases.reduce((t, c) => t + c.texte.length, 0), 0);
console.log(`\nFertig: ${alles.length} Seiten, ${alles.reduce((s, p) => s + p.canvases.length, 0)} Canvas, ${nTexte} Beschriftungen.`);
