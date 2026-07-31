// Inventar + Reaktions-Test aller interaktiven Animationen.
//
// Je Canvas wird erhoben:
//   - Titel, Abschnitt, zugehoerige Bedienelemente (Regler, Knoepfe, Auswahl)
//   - die Texte von «Worauf achten?» und «Erkenntnis»
//   - REAKTION: bewegt sich das Bild, wenn ein Bedienelement betaetigt wird?
//     Gemessen ueber den Pixel-Unterschied des Canvas vor/nach der Bedienung.
//     Ein Regler ohne Bildwirkung ist ein toter Regler — der haeufigste
//     didaktische Defekt (Beispiel AN-11 im alten Audit).
//   - reagieren die Live-Werte im Bedienbereich (.wert/.sl-val/.legende)?
//
// Aufruf (Server auf 8001):
//   node scripts/audit-beschriftungen/audit-widgets.mjs [--bereich grundlagen|schwerpunkt]
import { chromium } from 'playwright';
import fs from 'node:fs';

const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
const BEREICH = arg('--bereich');
const BASIS = 'http://localhost:8001/';
const ORDNER = BEREICH ? [BEREICH] : ['grundlagen', 'schwerpunkt'];
const seiten = ORDNER.flatMap(d =>
  fs.readdirSync(d).filter(f => f.endsWith('.html')).map(f => d + '/' + f)).sort();

const browser = await chromium.launch();
const alles = [];

for (const [i, rel] of seiten.entries()) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const jsFehler = [];
  page.on('pageerror', e => jsFehler.push(String(e).slice(0, 140)));
  await page.goto(BASIS + rel, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => {
    for (const c of document.querySelectorAll('canvas')) {
      c.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 30));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(1200);

  const widgets = await page.evaluate(async () => {
    const sig = cv => {                       // grobe Bildsignatur
      try {
        const x = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
        let h = 0; for (let k = 0; k < x.length; k += 401) h = (h * 31 + x[k]) >>> 0;
        return h;
      } catch (e) { return null; }
    };
    const txt = e => e ? e.textContent.replace(/\s+/g, ' ').trim() : '';
    const raus = [];

    for (const cv of document.querySelectorAll('canvas')) {
      // Die Widgets sind flache Geschwister (Regler-Box, Canvas, Legende), kein
      // gemeinsamer Container. Also den Geschwister-Bereich abgrenzen: vom Canvas
      // aus nach oben und unten, bis eine Ueberschrift oder ein anderer Canvas kommt.
      const grenze = e => !e || /^H[1-4]$/.test(e.tagName) || e.querySelector?.('canvas') || e.tagName === 'CANVAS';
      const stueck = [];
      let anker = cv;
      while (anker && anker.parentElement && !anker.previousElementSibling && !anker.nextElementSibling) anker = anker.parentElement;
      stueck.push(anker);
      for (let e = anker.previousElementSibling, k = 0; e && k < 4; e = e.previousElementSibling, k++) {
        if (grenze(e)) break; stueck.unshift(e);
      }
      for (let e = anker.nextElementSibling, k = 0; e && k < 4; e = e.nextElementSibling, k++) {
        if (grenze(e)) break; stueck.push(e);
      }
      const box = { querySelector: sel => stueck.map(x => x.querySelector?.(sel)).find(Boolean) || null,
                    querySelectorAll: sel => stueck.flatMap(x => [...(x.querySelectorAll?.(sel) || [])]),
                    textContent: stueck.map(x => x.textContent || '').join(' ') };
      const bedien = box.querySelectorAll('input[type=range],input[type=checkbox],input[type=radio],button,select')
        .filter(e => e.offsetParent !== null && !e.closest('.ah-pop') && !e.closest('.minicheck'));

      // Abschnitt = vorangehendes h2[id]
      let abschnitt = '';
      const h2s = [...document.querySelectorAll('.content h2[id], h2[id]')];
      const oben = cv.getBoundingClientRect().top + scrollY;
      for (const h of h2s) if (h.getBoundingClientRect().top + scrollY < oben) abschnitt = h.id;

      const titelEl = box.querySelector('.widget-titelzeile h3, .anim-titel, h3');
      const hinweise = box.querySelectorAll('.anim-hinweis');
      const worauf = hinweise.find(h => /Worauf/.test(txt(h.querySelector('.ah-titel'))));
      const erkenntnis = hinweise.find(h => /Erkenntnis/.test(txt(h.querySelector('.ah-titel'))));

      // Reaktionstest je Bedienelement
      const reaktion = [];
      for (const b of bedien.slice(0, 8)) {
        const vor = sig(cv);
        const vorTxt = txt(box).slice(0, 400);
        if (b.tagName === 'INPUT' && b.type === 'range') {
          const min = parseFloat(b.min || 0), max = parseFloat(b.max || 100);
          const alt = b.value;
          b.value = String(parseFloat(alt) < (min + max) / 2 ? max : min);
          b.dispatchEvent(new Event('input', { bubbles: true }));
          await new Promise(r => setTimeout(r, 90));
          const nach = sig(cv), nachTxt = txt(box).slice(0, 400);
          reaktion.push({ el: b.id || b.name || 'range', typ: 'regler',
                          bild: vor !== null && nach !== null && vor !== nach,
                          text: vorTxt !== nachTxt });
          b.value = alt; b.dispatchEvent(new Event('input', { bubbles: true }));
          await new Promise(r => setTimeout(r, 60));
        } else if (b.tagName === 'BUTTON' || (b.tagName === 'INPUT' && /checkbox|radio/.test(b.type))) {
          b.click();
          await new Promise(r => setTimeout(r, 140));
          const nach = sig(cv), nachTxt = txt(box).slice(0, 400);
          reaktion.push({ el: b.id || txt(b).slice(0, 18) || b.type, typ: b.tagName === 'BUTTON' ? 'knopf' : b.type,
                          bild: vor !== null && nach !== null && vor !== nach,
                          text: vorTxt !== nachTxt });
        }
      }

      raus.push({
        id: cv.id || '(ohne id)', abschnitt,
        titel: txt(titelEl).slice(0, 90),
        breite: cv.width, hoehe: cv.height,
        bedienAnzahl: bedien.length,
        regler: bedien.filter(b => b.type === 'range').length,
        knoepfe: bedien.filter(b => b.tagName === 'BUTTON').length,
        worauf: txt(worauf && worauf.querySelector('.ah-text')),
        erkenntnis: txt(erkenntnis && erkenntnis.querySelector('.ah-text')),
        reaktion,
      });
    }
    return raus;
  });

  alles.push({ seite: rel, jsFehler, widgets });
  const tot = widgets.flatMap(w => w.reaktion).filter(r => !r.bild && !r.text).length;
  const ohneHinweis = widgets.filter(w => !w.worauf || !w.erkenntnis).length;
  process.stdout.write(`[${String(i + 1).padStart(2)}/${seiten.length}] ${rel.split('/')[1].padEnd(46)}` +
    `${String(widgets.length).padStart(2)} Anim  ${String(widgets.reduce((s, w) => s + w.bedienAnzahl, 0)).padStart(2)} Bedien` +
    `  ohne Wirkung ${tot}  ohne Hinweispaar ${ohneHinweis}\n`);
  await ctx.close();
}
await browser.close();
const out = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad/widgets' +
            (BEREICH ? '-' + BEREICH : '') + '.json';
fs.writeFileSync(out, JSON.stringify(alles, null, 1));
console.log('\nRohdaten: ' + out);
