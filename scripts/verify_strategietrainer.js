#!/usr/bin/env node
// Selbsttest des Strategietrainers (werkzeuge/strategietrainer.html), ohne Browser: Der Block
// zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_strategietrainer.js            # 400 Aufgaben je Vorlage (Pre-Flight)
//   node scripts/verify_strategietrainer.js 5000       # gründlicher
// Je Vorlage werden Zufallsaufgaben erzeugt und alle passenden Wege bis zum Ende verfolgt.
// Geprüft wird:
//   – jeder Schritt der Liste liefert in jedem Zustand ok/um/x mit Text, ohne «undefined»/«NaN»
//   – jeder Zustand hat mindestens einen passenden Schritt und einen Tipp
//   – Gleichungen: Die Lösungen erfüllen die gestellte Gleichung, es fehlt keine; bei
//     Bruchgleichungen fallen genau die verbotenen Zahlen weg
//   – Terme: Das Ergebnis hat an Zufallsstellen denselben Wert wie der gestellte Term, ist
//     vollständig zerlegt bzw. gekürzt, und 𝔻 stimmt mit den Nullstellen des Nenners überein
//   – Systeme: Jedes Lösungspaar erfüllt beide Gleichungen, die Anzahl stimmt
//   – LaTeX: Klammern ausgeglichen, keine «+ -», «1x», «x^1», «+ 0»
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'strategietrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { LISTEN, familie, regel, ausfuehren, passend, tipp, VORLAGEN, wzWert, analyse, aktiv, gemeinsam, gegen, resid };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 400;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

function latexOk(z, wo) {
  let tiefe = 0;
  for (const ch of z) { if (ch === '{') tiefe++; if (ch === '}') tiefe--; if (tiefe < 0) break; }
  if (tiefe !== 0) melde('LaTeX: Klammern { } unausgeglichen', wo + ': ' + z);
  let rund = 0;
  for (const ch of z.replace(/\\[a-z]+/g, '')) { if (ch === '(') rund++; if (ch === ')') rund--; }
  if (rund !== 0) melde('LaTeX: Klammern ( ) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
  if (/(^|[^0-9.])1[xy](?![0-9])/.test(z)) melde('LaTeX: 1x', wo + ': ' + z);
  if (/[xy]\^1(?!\d)/.test(z)) melde('LaTeX: x^1', wo + ': ' + z);
  // «- 0» ist beim Zurückeinsetzen von x = 0 richtig (y = 0^2 - 0 - 4)
  if (/[+-] 0(?![.\d])/.test(z) && !/zurueck/.test(wo)) melde('LaTeX: ± 0', wo + ': ' + z);
}

// Reelle Nullstellen einer Funktion, die ein Polynom höchstens 2. Grades ist (aus Stützstellen)
function nullstellen(f) {
  const f0 = f(0), f1 = f(1), fm = f(-1);
  const a = (f1 + fm) / 2 - f0, b = (f1 - fm) / 2, c = f0;
  const eps = 1e-9;
  if (Math.abs(f(2) - (4 * a + 2 * b + c)) > 1e-6) return 'grad>2';
  if (Math.abs(a) < eps) {
    if (Math.abs(b) < eps) return Math.abs(c) < eps ? 'alle' : [];
    return [-c / b];
  }
  const D = b * b - 4 * a * c;
  if (D < -1e-9) return [];
  if (Math.abs(D) < 1e-9) return [-b / (2 * a)];
  return [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort((u, v) => u - v);
}
const nah = (u, v) => Math.abs(u - v) < 1e-7 * (1 + Math.abs(u));

function pruefeGl(ende, a, wo) {
  const d = ende.gl;
  if (!d) { melde('Ende ohne Daten (Gleichung)', wo); return; }
  const Dw = a.dW || [];
  if (Dw.length && !(d.Dw && d.Dw.length === Dw.length)) melde('Bruchgleichung: 𝔻 fehlt am Ende', wo);
  let soll = nullstellen(a.g || a.f);
  if (soll === 'grad>2') { melde('Prüfung: Gleichung nicht höchstens quadratisch', wo); return; }
  if (d.wahr !== undefined) {
    if ((soll === 'alle') !== d.wahr) melde('Lösung: wahr/falsch vertauscht', wo + ' ' + ende.z);
    if (soll !== 'alle' && soll.filter(v => !Dw.some(p => nah(p, v))).length) melde('Lösung: Widerspruch, aber Gleichung lösbar', wo);
    return;
  }
  if (soll === 'alle') { melde('Lösung: ℝ erwartet', wo); return; }
  soll = soll.filter(v => !Dw.some(p => nah(p, v)));
  const ist = d.w.map(K.wzWert).sort((u, v) => u - v);
  if (ist.length !== soll.length || ist.some((v, i) => !nah(v, soll[i])))
    melde('Lösung: falsch oder unvollständig', wo + ' → ' + ende.z + ' | soll ' + JSON.stringify(soll));
  for (const v of ist) if (Math.abs(a.f(v)) > 1e-6 * (1 + Math.abs(v) ** 2)) melde('Lösung erfüllt die Gleichung nicht', wo + ' x = ' + v);
}
function pruefeTerm(ende, a, wo) {
  const d = ende.term;
  if (!d) { melde('Ende ohne Daten (Term)', wo); return; }
  const Dw = a.dW || [];
  for (const x of [-3.7, -1.3, 0.6, 2.9, 5.1]) {
    if (Dw.some(p => Math.abs(p - x) < 1e-9)) continue;
    if (!nah(d.wert(x), a.wert(x))) { melde('Term: Ergebnis hat einen anderen Wert', wo + ' → ' + ende.z); break; }
  }
  for (const pr of d.teile) for (const fa of pr.f) if (K.analyse(fa.p).m) melde('Term: nicht vollständig zerlegt', wo + ' → ' + ende.z);
  if (d.teile.length === 2) {
    if (K.gemeinsam(d.teile[0], d.teile[1])) melde('Bruchterm: noch kürzbar', wo + ' → ' + ende.z);
    if (K.gegen(d.teile[0], d.teile[1])) melde('Bruchterm: Vorzeichen nicht angeglichen', wo + ' → ' + ende.z);
    const ist = (d.Dw || []).slice().sort((u, v) => u - v), soll = Dw.slice().sort((u, v) => u - v);
    if (ist.length !== soll.length || ist.some((v, i) => v !== soll[i])) melde('Bruchterm: 𝔻 falsch', wo + ' → ' + ende.z + ' | soll ' + soll);
  }
}
function pruefeSys(ende, a, wo) {
  const d = ende.sys;
  if (!d) { melde('Ende ohne Daten (System)', wo); return; }
  const res = a.g.map(K.resid);
  if (d.gerade) {
    if (a.anzahl !== 'unendlich') melde('System: unendlich viele Lösungen gemeldet', wo);
    for (const t of [-2, 0, 3]) if (res.some(r => Math.abs(r(t, d.gerade[0] * t + d.gerade[1])) > 1e-9)) melde('System: Gerade erfüllt die Gleichungen nicht', wo);
    return;
  }
  if (d.paare.length !== a.anzahl) melde('System: Anzahl Lösungen falsch', wo + ' → ' + ende.z + ' | soll ' + a.anzahl);
  for (const [x, y] of d.paare) {
    if (!Number.isInteger(x) || !Number.isInteger(y)) melde('System: Lösung nicht ganzzahlig', wo + ' → ' + ende.z);
    if (res.some(r => Math.abs(r(x, y)) > 1e-9)) melde('System: Paar erfüllt die Gleichungen nicht', wo + ' → ' + ende.z);
  }
}

let zustaende = 0, wege = 0;
function gehe(st, a, wo, tiefe) {
  zustaende++;
  if (tiefe > 16) { melde('Weg zu lang', wo); return; }
  latexOk(st.z, wo);
  const ok = K.passend(st);
  if (!ok.length) { melde('Zustand ohne passenden Schritt', wo + ' ' + st.k + ': ' + st.z); return; }
  const t = K.tipp(st);
  if (typeof t !== 'string' || !t) melde('Tipp fehlt', st.k); else latexOk(t, 'Tipp ' + st.k);
  for (const [id] of K.LISTEN[K.familie(st)]) {
    const r = K.regel(st, id);
    if (!r || !['ok', 'um', 'x'].includes(r[0])) { melde('Regel fehlt', st.k + '/' + id); continue; }
    if (r[0] !== 'ok') {
      if (typeof r[1] !== 'string' || !r[1]) melde('Regeltext fehlt', st.k + '/' + id);
      else { latexOk(r[1], st.k + '/' + id); if (r[1] === 'Dieser Schritt passt hier nicht.') melde('Regel ohne eigene Begründung', st.k + '/' + id); }
    }
  }
  for (const id of ok) {
    const aus = K.ausfuehren(st, id);
    for (const [z] of aus.zeilen) latexOk(z, wo + ' ' + id);
    if (aus.ersetzen) latexOk(aus.ersetzen, wo + ' ' + id);
    if (aus.info) latexOk(aus.info, wo + ' ' + id);
    if (aus.next.k === 'ende') {
      latexOk(aus.next.z, wo + ' Ende');
      wege++;
      const f = K.familie(st);
      if (f === 'gl') pruefeGl(aus.next, a, wo); else if (f === 'term') pruefeTerm(aus.next, a, wo); else pruefeSys(aus.next, a, wo);
      continue;
    }
    gehe(aus.next, a, wo + ' →' + id, tiefe + 1);
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
      gehe(a.st, a, fn.name + ' «' + a.st.z + '»', 0);
    }
  }
}

console.log(`${Object.keys(zaehl).length} Vorlagen · ${Object.values(zaehl).reduce((s, v) => s + v, 0)} Aufgaben · ${zustaende} Zustände · ${wege} Wege bis zum Ende`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
