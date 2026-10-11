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
//   – «Nächster Schritt» (schrittListe): nie leer, jeder Titel konkret (nicht leer, nicht nur «Schritt n»),
//     LaTeX ausgeglichen, jede Wegzeile steht in einem Schritt (ausser sie wiederholt die vorige)
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
vm.runInContext(kern + '\n;globalThis.K = { BEREICHE, FEHLER, FALLEN, aufgabe, pruefe, schrittListe, loesungTex, zielTex, qTex, dezimal, Q, lies, G14 };', ctx);
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
function schritteOk(a, wo) {
  const liste = K.schrittListe(a);
  if (!liste.length) { melde('Schritte: Liste leer', wo); return; }
  const generisch = /^(Schritt|Rechnen|Umformen|Weiter|Lösung|Gesetz)\s*\d*\s*:?\s*$/i;
  for (const s of liste) {
    if (!s.titel || !s.titel.trim()) melde('Schritte: Titel leer', wo + ' ' + JSON.stringify(s.zeilen));
    else if (generisch.test(s.titel.trim()) || s.titel.trim().length < 6) melde('Schritte: Titel generisch', wo + ' «' + s.titel + '»');
    else if (/^\\\(/.test(s.titel.trim())) melde('Schritte: Titel nur Formel, ohne Gesetz/Operation', wo + ' «' + s.titel + '»');
    latexOk(s.titel || '', wo + ' Schritttitel');
    if (!s.zeilen.length) melde('Schritte: Schritt ohne Zeile', wo + ' «' + s.titel + '»');
  }
  const drin = new Set(liste.flatMap(s => s.zeilen));
  let vorher = a.art === 'wahl' ? null : a.ausdruck;
  for (const w of a.weg) {
    if (w.text) { if (!drin.has(w)) melde('Schritte: Textzeile fehlt', wo + ' ' + w.text); continue; }
    if (!drin.has(w) && w.z !== vorher) melde('Schritte: Wegzeile fehlt', wo + ' ' + w.z);
    vorher = w.z;
  }
}
const alsEingabe = (q, dez) => (dez && q.d !== 1 ? K.dezimal(q) : q.d === 1 ? String(q.n) : q.n + '/' + q.d);

// Gezielte Prüfungen zu TODO-trainer-korrekturen.md (GT-B1 … GT-C8)
const codes = a => a.diag.map(([c]) => c);
const abbr = q => { let d = q.d; while (d % 2 === 0) d /= 2; while (d % 5 === 0) d /= 5; return d === 1; };
function gezielt(a, bereich, wo) {
  // GT-B1: Vorzeichen-Aufgaben nur mit geradem Exponenten; negKlammer/negsq = Wert mit übersehener Klammer
  let m;
  if ((m = /^(\(?)-(\d+)\)?\^\{(\d+)\}$/.exec(a.ausdruck))) {
    const b = +m[2], n = +m[3], mitKl = m[1] === '(';
    if (n % 2) melde('GT-B1: Vorzeichen-Aufgabe mit ungeradem Exponenten', wo);
    const falsch = mitKl ? -(b ** n) : (-b) ** n;
    for (const [c, [v]] of a.diag) if ((c === 'negKlammer' || c === 'negsq') && v.n / v.d !== falsch) melde('GT-B1: Klammer-Diagnose mit falschem Wert', wo + ' ' + c);
  }
  // GT-B2: «verschiedene Basen» nur bei verschiedenen Basen
  if ((m = /^(\d+)\^\{-?\d+\} \\cdot (\d+)\^/.exec(a.ausdruck)) && m[1] === m[2] && codes(a).includes('basenVerschieden')) melde('GT-B2: basenVerschieden bei gleicher Basis', wo);
  // GT-B3: Quotient bzw. Differenz von Wurzeln nicht als «addiert» etikettieren
  if (/^\\frac\{\\sqrt/.test(a.ausdruck) && codes(a).includes('wurzelMal')) melde('GT-B3: Quotient als «addiert» etikettiert', wo);
  if (/ - \\sqrt/.test(a.ausdruck) && codes(a).includes('radikandAddiert')) melde('GT-B3: Differenz als «addiert» etikettiert', wo);
  // GT-B4: Nenner-Diagnose nur, wenn es einen Nenner gibt
  if (a.typ === 'Zu einem Logarithmus zusammenfassen' && a.loesung[1].n > 0 && codes(a).includes('logZerlVz')) melde('GT-B4: Nenner-Diagnose ohne Nenner', wo);
  // GT-B5: Bereich Wurzeln nur GF 1.4: Wurzeln ⁿ√x (m = 1), Ergebnis-Exponent ganz oder 1/n, keine Werte mit Bruchexponent
  if (bereich === 'wurzeln') {
    if (/\\sqrt(\[\d+\])?\{x\^/.test(a.ausdruck)) melde('GT-B5: Bereich Wurzeln mit m ≠ 1', wo);
    if (a.ziel === 'x^{{n}}' && Math.abs(a.loesung[0].n) !== 1) melde('GT-B5: Bereich Wurzeln mit Exponent m/n', wo);
    if (a.typ === 'Rationaler Exponent') melde('GT-B5: Bereich Wurzeln mit rationalem Exponenten', wo);
    for (const [c] of a.diag) if (K.FEHLER[c][2] && !K.FEHLER[c][2][0].startsWith(K.G14)) melde('GT-B5: Fehler-Link im Bereich Wurzeln nicht auf g1.4', wo + ' ' + c);
  }
  if (bereich === 'rational' && a.ziel === 'x^{{n}}' && !/\\sqrt(\[\d+\])?\{x\^/.test(a.ausdruck) && Math.abs(a.loesung[0].n) === 1) melde('GT-B5: Bereich Rational ohne m/n', wo);
  // GT-C1: keine GF-Nummern, die in SF 1.2 anders heissen
  for (const w of a.weg) if (/P[4-7] rückwärts|P7/.test((w.k || '') + (w.text || ''))) melde('GT-C1: Nummer «P4 rückwärts»/«P7» im Lösungsweg', wo);
  if (/P[4-7]/.test(a.tipp || '')) melde('GT-C1: Nummer P4–P7 im Tipp', wo);
  // GT-C2: ln(√e) u.ä.: Wurzel-Diagnose vor dem Kehrwert
  if (a.typ === 'Wert eines Logarithmus' && /sqrt/.test(a.ausdruck)) {
    const wz = a.diag.find(([c]) => c === 'logWurzel') || [];
    const kehr = a.diag.find(([c]) => c === 'logKehr');
    if (kehr && wz[1] && kehr[1][0].n === wz[1][0].n && kehr[1][0].d === wz[1][0].d) melde('GT-C2: logKehr mit gleichem Wert wie logWurzel', wo);
    if (wz[1] && K.pruefe(a, [wz[1][0].n + '/' + wz[1][0].d]).code !== 'logWurzel') melde('GT-C2: Wurzel-Fehler nicht als logWurzel erkannt', wo);
  }
  // GT-C5: x ≠ 0 im Auftrag der Potenzterme
  if ((a.typ === 'Eine Potenz' || a.typ === 'Zwei Basen') && !/neq 0/.test(a.auftrag)) melde('GT-C5: Auftrag ohne x ≠ 0', wo);
  // GT-C6: gerundete Dezimalzahl statt Bruch → Hinweis «exakt»
  if (a.art !== 'wahl' && !a.ziel.includes('10^')) {
    const j = a.loesung.findIndex(q => q.d !== 1 && !abbr(q));
    if (j >= 0) {
      const e = a.loesung.map(q => (q.d === 1 ? String(q.n) : q.n + '/' + q.d));
      e[j] = (a.loesung[j].n / a.loesung[j].d).toFixed(3);
      const r = K.pruefe(a, e);
      if (r.status !== 'fast' || !/exakt/.test(r.text)) melde('GT-C6: gerundeter Bruch nicht als «exakt angeben»', wo + ' ' + e + ' → ' + JSON.stringify(r));
    }
  }
  // GT-C8: Lösung ohne überflüssige Klammern
  if (a.art !== 'wahl' && /^\{/.test(K.loesungTex(a))) melde('GT-C8: Lösung mit { }', wo + ' ' + K.loesungTex(a));
}
// Einzelfälle ohne Zufall
if (!K.BEREICHE.rational || !/\(SF\)/.test(K.BEREICHE.rational.name)) melde('GT-B5: Bereich «Rationale Exponenten (SF)» fehlt', '');
for (const [regel, gilt] of K.FALLEN.wurzeln || []) if (/\\frac\{m\}\{n\}|\\sqrt\[3\]/.test(regel)) melde('GT-B5: SF-Regel im Bereich Wurzeln', regel);
for (const liste of Object.values(K.FALLEN)) for (const [regel, gilt] of liste) if (gilt && /\\frac\{m\}\{n\}/.test(regel) && !/a > 0/.test(regel)) melde('GT-B6: Regel mit m/n ohne «a > 0» in der Aussage', regel);
if (/Summen/.test(K.FEHLER.falleGeglaubt[1])) melde('GT-C3: falleGeglaubt spricht von Summen', '');
for (const c of ['negBasis', 'basisMal', 'nullExp', 'kehrVergessen']) if (K.FEHLER[c][2][0] !== K.G14 + '#potenzgesetze') melde('GT-C4: Link nicht auf g1.4 #potenzgesetze', c);
for (const c of ['negsq', 'negKlammer']) if (K.FEHLER[c][2][0] !== K.G14 + '#hierarchie') melde('GT-C4: Link nicht auf g1.4 #hierarchie', c);
{
  const merk = html.slice(html.indexOf('Die Gesetze auf einen Blick'), html.indexOf('</details>', html.indexOf('Die Gesetze auf einen Blick')));
  if (!/a, b \\ge 0/.test(merk)) melde('GT-C5: Merktabelle ohne a, b ≥ 0 bei Wurzeln', '');
  if (!/m\}\{n\}\}[^<]*a > 0/.test(merk)) melde('GT-C5: Merktabelle ohne a > 0 bei rationalen Exponenten', '');
  if (!/a > 0,\\ a \\neq 1/.test(merk)) melde('GT-C5: Merktabelle ohne a > 0, a ≠ 1 beim Logarithmus', '');
}
{ const l = K.lies('5.'); if (!l.q || l.q.n !== 5 || l.q.d !== 1) melde('GT-C6: «5.» nicht verstanden', JSON.stringify(l)); }
if (/aria-label="' \+ f\.id/.test(html)) melde('GT-C7: aria-label überschreibt das sichtbare label', '');
if (!/\.tr-opt[\s\S]{0,400}aria-pressed/.test(html) || (html.match(/aria-pressed/g) || []).length < 2) melde('RT-C10: .tr-opt ohne aria-pressed', '');

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
  schritteOk(a, wo);
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
  gezielt(a, bereich, wo);
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
