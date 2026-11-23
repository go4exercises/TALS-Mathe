#!/usr/bin/env node
// Selbsttest aller Präsentationen (praesentationen/*.html), ohne Browser (HOWTO-praesentationen.md §6).
//   node scripts/verify_praesentationen.js [datei …]     # ohne Angabe: alle Präsentationen (Pre-Flight)
// Präsentationen setzen ihre Formeln zum grossen Teil erst im Skript (Folien, Live-Anzeigen, Rechenwege).
// verify_mathjax.js sieht davon nichts, weil es <script> überspringt. Darum hier:
//   1. Seite in jsdom laden und laufen lassen; jeder Laufzeitfehler ist ein Befund.
//   2. Jeden Knopf im Foliensatz einmal drücken, jeden Regler auf Minimum, Mitte und Maximum stellen.
//   3. Nach jedem Schritt alle \(…\) im Foliensatz einsammeln und mit mathjax-full setzen
//      (mit den Makros und Paketen aus der MathJax-Einstellung der Seite).
//   4. Kein Text enthält undefined, NaN, Infinity, ein Dezimalkomma oder einen Rest von $…$.
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const wurzel = path.join(__dirname, '..');
const nm = p => require(require.resolve(p, { paths: [wurzel] }));
const { JSDOM, VirtualConsole } = nm('jsdom');
const { mathjax } = nm('mathjax-full/js/mathjax.js');
const { TeX } = nm('mathjax-full/js/input/tex.js');
const { SVG } = nm('mathjax-full/js/output/svg.js');
const { liteAdaptor } = nm('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = nm('mathjax-full/js/handlers/html.js');
const { AllPackages } = nm('mathjax-full/js/input/tex/AllPackages.js');
const adaptor = liteAdaptor(); RegisterHTMLHandler(adaptor);

const dateien = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(path.join(wurzel, 'praesentationen')).filter(f => f.endsWith('.html')).map(f => path.join('praesentationen', f));

let gesamt = 0;
for (const datei of dateien) {
  const befunde = new Map();
  const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
  const html = fs.readFileSync(path.resolve(wurzel, datei), 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => melde('Laufzeitfehler', String(e.message || e).split('\n')[0]));
  vc.on('error', e => melde('console.error', String(e && e.message || e).split('\n')[0]));
  // Im Skript steht TeX in JS-Strings, also mit doppeltem Backslash. Ein einzelner vor ; , ! : verschwindet
  // still (aus «\;» wird «;») — gültiges TeX, darum sieht es die Prüfung unten nicht.
  for (const [, skript] of html.matchAll(/<script>([\s\S]*?)<\/script>/g))
    for (const m of skript.matchAll(/(^|[^\\])\\[;,!:]/g)) melde('einfacher Backslash vor ; , ! : im Skript', skript.slice(Math.max(0, m.index - 30), m.index + 10).replace(/\s+/g, ' '));
  let dom;
  try {
    dom = new JSDOM(html.replace(/<script src="[^"]*"><\/script>/g, ''), {   // MathJax und andere Dateien nicht laden
      runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
      beforeParse(w) {
        w.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
        w.Element.prototype.scrollTo = function () {};
        w.HTMLElement.prototype.requestFullscreen = function () { return Promise.resolve(); };
        w.SVGSVGElement && (w.SVGSVGElement.prototype.createSVGPoint = () => ({ x: 0, y: 0, matrixTransform() { return this; } }));
      },
    });
  } catch (e) { melde('Seite lädt nicht', e.message); }
  if (!dom) { gesamt += 1; console.log(`${datei}: Seite lädt nicht`); continue; }
  const w = dom.window, d = w.document;
  const cfg = w.MathJax && w.MathJax.tex || {};
  const texIn = new TeX({ packages: AllPackages, macros: cfg.macros || {} });
  const doc = mathjax.document('', { InputJax: texIn, OutputJax: new SVG({ fontCache: 'none' }) });
  const geprueft = new Set();
  const deck = d.getElementById('deck') || d.body;
  const sammle = wo => {
    const text = deck.textContent;
    if (/undefined|NaN|Infinity|\[object/.test(text)) melde('Text kaputt (undefined/NaN)', wo);
    if (/(^|[^\\])\$[^$]+\$/.test(text)) melde('$…$ statt \\(…\\)', wo);
    for (const m of text.matchAll(/\\\(([\s\S]*?)\\\)/g)) {
      const tex = m[1];
      if (geprueft.has(tex)) continue;
      geprueft.add(tex);
      if (/\d\{,\}\d|\d,\d/.test(tex)) melde('Dezimalkomma in einer Formel', tex);
      try {
        const out = adaptor.outerHTML(doc.convert(tex, { display: false }));
        if (out.includes('data-mjx-error') || out.includes('merror')) {
          const e = out.match(/data-mjx-error="([^"]*)"/);
          melde('MathJax-Fehler', (e ? e[1] : 'merror') + ' · ' + tex);
        }
      } catch (e) { melde('MathJax-Ausnahme', e.message + ' · ' + tex); }
    }
    const rest = text.replace(/\\\(([\s\S]*?)\\\)/g, '');
    if (/\d,\d/.test(rest)) melde('Dezimalkomma im Text', rest.match(/.{0,30}\d,\d.{0,30}/)[0]);
  };
  sammle('Start');
  // Knöpfe und Regler durchspielen (Navigationsleiste ausgenommen)
  const knoepfe = [...deck.querySelectorAll('button')];
  for (const b of knoepfe) { try { b.click(); } catch (e) { melde('Fehler beim Klick', e.message); } sammle('Knopf ' + (b.id || b.textContent.trim())); }
  for (const b of knoepfe) { try { b.click(); } catch (e) {} }
  const regler = () => [...deck.querySelectorAll('input[type=range]')];
  for (const b of [null, ...knoepfe]) {        // jeden Regler auch nach jedem Knopf (Fallauswahl baut Regler neu)
    if (b) try { b.click(); } catch (e) {}
    for (const r of regler()) {
      const lo = +r.min, hi = +r.max, st = +r.step || 1;
      for (const v of [lo, lo + Math.round((hi - lo) / 2 / st) * st, hi]) {
        r.value = String(v);
        try { r.dispatchEvent(new w.Event('input', { bubbles: true })); } catch (e) { melde('Fehler am Regler', e.message); }
        sammle(`Regler ${r.id || r.getAttribute('aria-label')} = ${v}`);
      }
    }
  }
  // alle Folien Schritt für Schritt (Pfeil rechts)
  for (let i = 0; i < 400; i++) {
    d.body.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
  }
  sammle('nach allen Schritten');
  // Auswahllisten (Themenwahl, Beispiele): jede Option wählen und ihre Schritte durchgehen
  let optionen = 0;
  for (const sel of d.querySelectorAll('select')) for (const o of [...sel.options]) {
    sel.value = o.value; optionen++;
    try { sel.dispatchEvent(new w.Event('change', { bubbles: true })); } catch (e) { melde('Fehler in der Auswahl', e.message); }
    for (let i = 0; i < 12; i++) d.body.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
    sammle(`Auswahl ${sel.id} = ${o.textContent.trim()}`);
  }
  w.close();
  const n = [...befunde.values()].reduce((s, b) => s + b.n, 0);
  gesamt += n;
  console.log(`${datei}: ${geprueft.size} Formeln gesetzt, ${knoepfe.length} Knöpfe, ${regler().length} Regler, ${optionen} Optionen — ${n ? n + ' Befund(e)' : 'keine Befunde'}`);
  for (const [art, { n, info }] of befunde) console.log(`  [${n}×] ${art}: ${info}`);
}
console.log(gesamt ? `BEFUNDE: ${gesamt}` : 'Präsentationen: alles in Ordnung');
process.exit(gesamt ? 1 : 0);
