#!/usr/bin/env node
// Selbsttest des Strategietrainers (werkzeuge/strategietrainer.html), ohne Browser: Der Block
// zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_strategietrainer.js            # 500 Aufgaben je Vorlage (Pre-Flight)
//   node scripts/verify_strategietrainer.js 5000       # gründlicher
// Je Vorlage werden Zufallsaufgaben erzeugt und alle passenden Wege bis zur Lösungsmenge
// verfolgt. Geprüft wird:
//   – jede Strategie liefert in jedem Zustand ok/um/x, Texte ohne «undefined»/«NaN»
//   – jeder Zustand hat mindestens einen passenden Schritt und einen Tipp
//   – die Lösungen erfüllen die gestellte Gleichung, und es fehlt keine (numerisch)
//   – LaTeX: Klammern ausgeglichen, keine «+ -», «1x», «x^1», «+0»
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'strategietrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { STRAT, REGELN, regel, passend, tipp, VORLAGEN, wzWert };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 500;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

function latexOk(z, wo) {
  let tiefe = 0;
  for (const ch of z) { if (ch === '{') tiefe++; if (ch === '}') tiefe--; if (tiefe < 0) break; }
  if (tiefe !== 0) melde('LaTeX: Klammern { } unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
  if (/(^|[^0-9.])1x/.test(z)) melde('LaTeX: 1x', wo + ': ' + z);
  if (/x\^1(?!\d)/.test(z)) melde('LaTeX: x^1', wo + ': ' + z);
  if (/[+-] 0(?![.\d])/.test(z)) melde('LaTeX: ± 0', wo + ': ' + z);
}

// Reelle Nullstellen von f (linear oder quadratisch), aus drei Stützstellen bestimmt
function nullstellen(f) {
  const f0 = f(0), f1 = f(1), fm = f(-1);
  const a = (f1 + fm) / 2 - f0, b = (f1 - fm) / 2, c = f0;
  const eps = 1e-9;
  if (Math.abs(a) < eps) {
    if (Math.abs(b) < eps) return Math.abs(c) < eps ? 'alle' : [];
    return [-c / b];
  }
  const D = b * b - 4 * a * c;
  if (D < -1e-9) return [];
  if (Math.abs(D) < 1e-9) return [-b / (2 * a)];
  return [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort((u, v) => u - v);
}

function pruefeEnde(st, f, wo) {
  const soll = nullstellen(f);
  if (st.k === 'wid') {
    if ((soll === 'alle') !== st.wahr) melde('Lösung: wahr/falsch vertauscht', wo + ' ' + st.z);
    if (soll !== 'alle' && soll.length) melde('Lösung: Widerspruch, aber Gleichung lösbar', wo + ' ' + st.z);
    return;
  }
  const ist = st.w.map(K.wzWert).sort((u, v) => u - v);
  if (soll === 'alle') { melde('Lösung: ℝ erwartet', wo); return; }
  if (ist.length !== soll.length || ist.some((v, i) => Math.abs(v - soll[i]) > 1e-7 * (1 + Math.abs(v))))
    melde('Lösung: falsch oder unvollständig', wo + ' → ' + st.z + ' | soll ' + JSON.stringify(soll));
}

let zustaende = 0, wege = 0;
function gehe(st, f, wo, tiefe) {
  zustaende++;
  if (tiefe > 14) { melde('Weg zu lang', wo); return; }
  latexOk(st.z, wo);
  const ok = K.passend(st);
  if (!ok.length) { melde('Zustand ohne passenden Schritt', wo + ' ' + st.k + ': ' + st.z); return; }
  const t = K.tipp(st);
  if (typeof t !== 'string' || !t) melde('Tipp fehlt', st.k);
  for (const [id] of K.STRAT) {
    const r = K.regel(st, id);
    if (!r || !['ok', 'um', 'x'].includes(r[0])) { melde('Regel fehlt', st.k + '/' + id); continue; }
    if (r[0] !== 'ok') { if (typeof r[1] !== 'string' || !r[1]) melde('Regeltext fehlt', st.k + '/' + id); else latexOk(r[1], st.k + '/' + id); }
  }
  for (const id of ok) {
    const aus = K.regel(st, id)[2]();
    for (const [z] of aus.zeilen) latexOk(z, wo + ' ' + id);
    if (aus.next.k === 'ende') { latexOk(aus.next.z, wo + ' L'); pruefeEnde(st, f, wo + ' [' + st.k + ']'); wege++; continue; }
    gehe(aus.next, f, wo + ' →' + id, tiefe + 1);
  }
}

const zaehl = {};
for (const bereich of Object.keys(K.VORLAGEN)) {
  for (const [, fn] of K.VORLAGEN[bereich]) {
    let n = 0, leer = 0;
    while (n < N) {
      const a = fn();
      if (!a) { if (++leer > 50 * N) { melde('Vorlage liefert fast nie eine Aufgabe', fn.name); break; } continue; }
      n++;
      zaehl[fn.name] = (zaehl[fn.name] || 0) + 1;
      gehe(a.st, a.f, fn.name + ' «' + a.st.z + '»', 0);
    }
  }
}

console.log(`${Object.keys(zaehl).length} Vorlagen · ${Object.values(zaehl).reduce((s, v) => s + v, 0)} Aufgaben · ${zustaende} Zustände · ${wege} Wege bis zur Lösungsmenge`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
