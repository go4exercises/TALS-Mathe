#!/usr/bin/env node
// Selbsttest des Einheitskreistrainers (werkzeuge/einheitskreistrainer.html), ohne Browser: Der Block
// zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_einheitskreistrainer.js         # 300 Aufgaben je Teil (Pre-Flight)
// Geprüft wird:
//   – jeder exakte Wert (sin, cos, tan für alle Winkel der Aufgaben) gegen Math.sin/cos/tan und
//     unabhängig in python3 (math); «nicht definiert» genau dort, wo cos = 0
//   – die Herleitung endet beim richtigen Wert; die Palette nimmt genau den richtigen Wert an
//   – Grad ↔ Bogenmass: exakt in python3 mit Fraction; Eingaben «5pi/6», «5π/6», «5/6pi» werden
//     angenommen, ungekürzte als «fast», «5/6» als «π vergessen», das Doppelte als «halb»
//   – Vom Wert zum Winkel: Die Lösungsmenge stimmt mit der in python3 berechneten überein
//     (asin/acos/atan, auf [0°; 360°[ gebracht); fehlende Lösung → «nur eine Lösung»
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined»
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'einheitskreistrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, KREIS, AUSSEN, PALETTE, wert, wertZahl, wertTex, herleitung, pruefe, radTex, mod360 };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 300;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\\(/g) || []).length !== (z.match(/\\\)/g) || []).length) melde('LaTeX: \\( \\) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
}

const py = [];
// 1. Werte aller Aufgabenwinkel
for (const g of K.KREIS.concat(K.AUSSEN)) for (const f of ['sin', 'cos', 'tan']) {
  const k = K.wert(f, g), z = K.wertZahl(k), r = g * Math.PI / 180;
  const soll = f === 'sin' ? Math.sin(r) : f === 'cos' ? Math.cos(r) : (Math.abs(Math.cos(r)) < 1e-12 ? null : Math.tan(r));
  if ((soll === null) !== (z === null) || (z !== null && Math.abs(z - soll) > 1e-12)) melde('Exakter Wert falsch', f + ' ' + g + '° → ' + k);
  py.push({ art: 'wert', f, g, z });
  for (const mass of ['grad', 'rad']) {
    const h = K.herleitung(f, g, mass);
    h.forEach(x => latexOk(x, f + ' ' + g));
    if (!h[h.length - 1].includes(k === 'nd' ? 'nicht definiert' : K.wertTex(k))) melde('Herleitung endet nicht beim Wert', f + ' ' + g + ' ' + mass + ': ' + h[h.length - 1]);
  }
}
// 2. Aufgaben je Teil
const radEingaben = g => {
  const t = K.radTex(g);            // z.B. -\frac{5\pi}{6}
  const m = /^(-?)(?:\\frac\{(\d*)\\pi\}\{(\d+)\}|(\d*)\\pi)$/.exec(t);
  if (t === '0') return ['0'];
  const vz = m[1], z = m[2] !== undefined ? m[2] : m[4], n = m[3];
  return n ? [vz + z + 'pi/' + n, vz + z + 'π/' + n, vz + (z || '1') + '/' + n + 'pi'] : [vz + z + 'pi'];
};
let zahl = 0;
for (const thema of Object.keys(K.THEMEN)) for (const mass of ['grad', 'rad', 'mix']) for (let i = 0; i < N / 3; i++) {
  const a = K.THEMEN[thema].neu(mass);
  if (!a) continue;
  zahl++;
  const wo = thema + ' «' + a.ausdruck + '»';
  latexOk(a.ausdruck, wo); latexOk(a.auftrag, wo); a.weg.forEach(z => latexOk(z, wo + ' Weg'));
  if (a.art === 'rad') {
    for (const e of radEingaben(a.grad)) { const r = K.pruefe(a, e); if (r.status !== 'ok') melde('Bogenmass-Eingabe nicht angenommen', wo + ' ' + e + ' ' + JSON.stringify(r)); }
    const zN = a.grad / 180;
    const doppelt = K.pruefe(a, (2 * a.grad) + '/180pi');
    if (doppelt.status === 'ok') melde('Doppeltes als richtig angenommen', wo);
    if (a.grad % 180 !== 0) {
      const g = a.grad / 15, ungek = K.pruefe(a, g + 'pi/12');          // z.B. 10pi/12 für 150°
      if (ungek.status !== (ggt(g, 12) === 1 ? 'ok' : 'fast')) melde('Ungekürzt nicht als «fast»', wo + ' ' + g + 'pi/12 → ' + ungek.status);
      const ohne = K.pruefe(a, (a.grad / ggt(a.grad, 180)) + '/' + (180 / ggt(a.grad, 180)));
      if (ohne.code !== 'ohnePi') melde('«π vergessen» nicht erkannt', wo + ' ' + JSON.stringify(ohne));
    }
    py.push({ art: 'rad', g: a.grad, tex: K.radTex(a.grad) });
  } else if (a.art === 'grad') {
    if (K.pruefe(a, String(a.grad)).status !== 'ok' || K.pruefe(a, a.grad + '°').status !== 'ok') melde('Grad-Eingabe nicht angenommen', wo);
    if (K.pruefe(a, String(2 * a.grad)).code !== 'halb') melde('Doppeltes nicht als «halb» erkannt', wo);
  } else if (a.art === 'palette') {
    let ok = 0;
    for (const k of K.PALETTE) { const r = K.pruefe(a, k); if (r.status === 'ok') ok++; else if (!K.FEHLER[r.code]) melde('Fehlercode ohne Text', r.code); }
    if (ok !== 1) melde('Palette: nicht genau ein richtiger Wert', wo + ' ' + ok);
    if (!K.PALETTE.includes(a.loesung)) melde('Lösung fehlt in der Palette', wo + ' ' + a.loesung);
  } else {
    if (K.pruefe(a, a.loesung.slice()).status !== 'ok') melde('Umkehr: Lösung nicht angenommen', wo);
    if (a.loesung.length > 1 && K.pruefe(a, a.loesung.slice(0, 1)).code !== 'umkehrEine') melde('Umkehr: fehlende Lösung nicht erkannt', wo);
    py.push({ art: 'umkehr', f: a.f, z: K.wertZahl(a.w), loes: a.loesung, wo });
  }
}
function ggt(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; }

const skript = `
import sys, json, math
from fractions import Fraction
fehler = []
for z in json.load(sys.stdin):
    if z['art'] == 'wert':
        r = math.radians(z['g'])
        if z['f'] == 'tan' and abs(math.cos(r)) < 1e-12:
            soll = None
        else:
            soll = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[z['f']](r)
        if (soll is None) != (z['z'] is None) or (soll is not None and abs(soll - z['z']) > 1e-12):
            fehler.append(['python: Wert weicht ab', z['f'] + ' ' + str(z['g'])])
    elif z['art'] == 'rad':
        q = Fraction(z['g'], 180)
        t = z['tex']; vz = -1 if t.startswith('-') else 1; t = t.lstrip('-')
        if t == '0': ist = Fraction(0)
        elif t.startswith('\\\\frac'):
            zae, nen = t[6:].split('}{'); zae = zae.strip('{').replace('\\\\pi', '') or '1'; nen = nen.strip('}')
            ist = vz * Fraction(int(zae), int(nen))
        else: ist = vz * Fraction(int(t.replace('\\\\pi', '') or '1'))
        if ist != q: fehler.append(['python: Bogenmass weicht ab', str(z['g']) + ' ' + z['tex']])
    elif z['art'] == 'umkehr':
        v = z['z']; f = z['f']
        if f == 'sin': a = math.degrees(math.asin(v)); kand = [a, 180 - a]
        elif f == 'cos': a = math.degrees(math.acos(v)); kand = [a, -a]
        else: a = math.degrees(math.atan(v)); kand = [a, a + 180]
        loes = sorted(set(round(x % 360, 6) % 360 for x in kand))
        if loes != sorted(float(g) for g in z['loes']): fehler.append(['python: Lösungsmenge weicht ab', z['wo'] + ' py=' + str(loes)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 26 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 400));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.THEMEN).length} Teile · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
