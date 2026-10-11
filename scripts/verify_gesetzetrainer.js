#!/usr/bin/env node
// Selbsttest des Gesetzetrainers (werkzeuge/gesetzetrainer.html), ohne Browser: Der Block zwischen
// «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_gesetzetrainer.js          # 1500 Aufgaben je Bereich (Pre-Flight)
//   node scripts/verify_gesetzetrainer.js 10000    # gründlicher
// Geprüft wird:
//   – die Musterlösung wird angenommen; ein ungekürzter Bruch bzw. eine Quadratzahl unter der Wurzel
//     gilt als «fast»; jeder Denkfehler-Wert wird als genau dieser Fehler erkannt, nie als richtig
//   – der Lösungsweg endet bei der Lösung (Exponentenbäume: letzte Zeile = Ergebnis)
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined», ohne doppeltes Vorzeichen
//   – Gegenrechnung in python3, unabhängig von der Rechnung des Werkzeugs: Aufgabe (links) und Lösung
//     (rechts) werden aus eigenen Python-Ausdrücken ausgewertet — Potenzen mit math und Fraction,
//     Wurzeln als (x**m)**(1/n), Logarithmen mit math.log; mit Variablen an Zufallsstellen
//   – «Regel prüfen»: Eine gültige Regel stimmt in Python an Zufallswerten, eine ungültige scheitert
//     am angegebenen Gegenbeispiel
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'gesetzetrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { BEREICHE, FEHLER, FALLEN, aufgabe, pruefe, loesungTex, zielTex, qTex, dezimal, Q };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 1500;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\left/g) || []).length !== (z.match(/\\right/g) || []).length) melde('LaTeX: \\left/\\right unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\\(/g) || []).length !== (z.match(/\\\)/g) || []).length) melde('LaTeX: \\( \\) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+|- \+|\+ -/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
}
const alsEingabe = (q, dez) => (dez && q.d !== 1 ? K.dezimal(q) : q.d === 1 ? String(q.n) : q.n + '/' + q.d);

const py = [];
let zahl = 0;
const typen = new Map();
for (const bereich of Object.keys(K.BEREICHE)) for (let i = 0; i < N; i++) {
  const a = K.aufgabe([bereich]);
  zahl++;
  typen.set(bereich + ' · ' + a.typ, (typen.get(bereich + ' · ' + a.typ) || 0) + 1);
  const wo = bereich + ' «' + a.ausdruck + '»';
  latexOk(a.ausdruck, wo); latexOk(a.auftrag, wo);
  a.weg.forEach(w => latexOk(w.text || w.z, wo + ' Weg'));
  if (a.art === 'wahl') {
    if (K.pruefe(a, a.loesung).status !== 'ok') melde('Wahl: Lösung nicht angenommen', wo);
    const falsch = a.wahl.find(([k]) => k !== a.loesung)[0];
    const r = K.pruefe(a, falsch);
    if (r.status !== 'falsch' || !K.FEHLER[r.code]) melde('Wahl: falsche Antwort nicht erkannt', wo);
    continue;
  }
  const lt = K.loesungTex(a);
  latexOk(lt, wo + ' Lösung'); latexOk(K.zielTex(a, []), wo + ' Ziel');
  const dez = a.ziel.includes('10^');
  const r = K.pruefe(a, a.loesung.map((q, j) => alsEingabe(q, dez && j === 0)));
  if (r.status !== 'ok') melde('Musterlösung nicht angenommen', wo + ' → ' + JSON.stringify(a.loesung) + ' ' + JSON.stringify(r));
  // ungekürzter Bruch → fast
  const j = a.loesung.findIndex(q => q.d !== 1);
  if (j >= 0 && !dez) {
    const e = a.loesung.map(q => alsEingabe(q)); e[j] = (2 * a.loesung[j].n) + '/' + (2 * a.loesung[j].d);
    const f = K.pruefe(a, e);
    if (f.status !== 'fast') melde('Ungekürzter Bruch nicht als «fast»', wo + ' ' + JSON.stringify(f));
  }
  if (a.ziel.includes('\\sqrt{{r}}')) {                 // k√r mit Quadrat unter der Wurzel → fast
    const [k, rr] = a.loesung;
    if (k.d === 1 && k.n % 2 === 0) { const f = K.pruefe(a, [String(k.n / 2), String(rr.n * 4)]); if (f.status !== 'fast') melde('Quadrat unter der Wurzel nicht als «fast»', wo + ' ' + JSON.stringify(f)); }
  }
  if (dez) {                                            // Mantisse ausserhalb [1; 10) → fast
    const f = K.pruefe(a, [K.dezimal(K.Q(a.loesung[0].n * 10, a.loesung[0].d)), String(a.loesung[1].n - 1)]);
    if (f.status !== 'fast') melde('Mantisse ≥ 10 nicht als «fast»', wo + ' ' + JSON.stringify(f));
  }
  for (const [code, w] of a.diag) {
    if (!K.FEHLER[code]) melde('Fehlercode ohne Text', code);
    if (w.some(q => q && (!Number.isFinite(q.n) || !Number.isFinite(q.d)))) { melde('Denkfehler-Wert nicht endlich', wo + ' ' + code); continue; }
    const e = w.map((q, i2) => (q ? alsEingabe(q, dez && i2 === 0) : alsEingabe(a.loesung[i2], dez && i2 === 0)));
    const p = K.pruefe(a, e);
    if (p.status === 'ok') melde('Denkfehler-Wert als richtig angenommen', wo + ' ' + code + ' ' + e);
    else if (p.status !== 'falsch' || p.code !== a.diag.find(([, u]) => JSON.stringify(u) === JSON.stringify(w) || p.code === code)[0]) {
      const erster = a.diag.find(([, u]) => u.every((q, i3) => !q || !w[i3] || (q.n === w[i3].n && q.d === w[i3].d)));
      if (!erster || erster[0] !== p.code) melde('Denkfehler nicht erkannt', wo + ' ' + code + ' ' + e + ' → ' + JSON.stringify(p));
    }
  }
  // Lösungsweg endet beim Ergebnis
  const zeilen = a.weg.filter(w => w.z);
  const letzte = zeilen.length ? zeilen[zeilen.length - 1].z : '';
  const norm = s => s.replace(/[{}\s]/g, '').replace(/\\cdot/g, '').replace(/^x=/, '');
  if (norm(letzte) !== norm(lt) && !(a.typ === 'Basiswechsel')) melde('Weg endet nicht bei der Lösung', wo + ' | ' + letzte + ' | ' + lt);
  py.push({ ...a.py, wo, diag: a.diag.length });
}
// Fallen: alle Einträge, nicht nur die gezogenen
for (const [bereich, liste] of Object.entries(K.FALLEN)) for (const [regel, gilt, , , , , p] of liste) py.push({ falle: true, gilt, links: p[0], rechts: p[1], wo: bereich + ' ' + regel });

const skript = `
import sys, json, math, random
from fractions import Fraction
fehler = []
random.seed(11)
for z in json.load(sys.stdin):
    try:
        if z.get('falle'):
            if z['gilt']:
                for _ in range(20):
                    bel = {'a': random.uniform(0.2, 9), 'b': random.uniform(0.2, 9), 'u': random.uniform(1.1, 50), 'v': random.uniform(1.1, 50),
                           'm': random.randint(-4, 6), 'n': random.randint(1, 5), 'k': random.randint(-3, 4), 'math': math}
                    l, r = eval(z['links'], {}, bel), eval(z['rechts'], {}, bel)
                    if abs(l - r) > 1e-9 * max(1, abs(l)): fehler.append(['python: gültige Regel stimmt nicht', z['wo']]); break
            else:
                l, r = eval(z['links'], {'math': math}), eval(z['rechts'], {'math': math})
                if abs(l - r) < 1e-9: fehler.append(['python: Gegenbeispiel widerlegt nicht', z['wo']])
            continue
        vs = z.get('vars') or []
        for _ in range(3 if vs else 1):
            bel = {v: random.uniform(1.2, 3.7) for v in vs}
            bel.update({'math': math, 'Fraction': Fraction})
            l, r = eval(z['links'], {}, bel), eval(z['rechts'], {}, bel)
            l, r = float(l), float(r)
            if abs(l - r) > 1e-9 * max(1, abs(r)): fehler.append(['python: Aufgabe und Lösung verschieden', z['wo'] + ' links=' + repr(l) + ' rechts=' + repr(r)]); break
    except Exception as e:
        fehler.append(['python-Fehler', z['wo'] + ' ' + repr(e)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 28 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.BEREICHE).length} Bereiche · ${typen.size} Aufgabentypen · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
