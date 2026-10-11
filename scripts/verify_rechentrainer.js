#!/usr/bin/env node
// Selbsttest des Rechentrainers (werkzeuge/rechentrainer.html), ohne Browser: Der Block zwischen
// «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_rechentrainer.js            # 400 Aufgaben je Thema (Pre-Flight)
//   node scripts/verify_rechentrainer.js 5000       # gründlicher
// Geprüft wird:
//   – die Musterlösung wird als richtig angenommen, in der verlangten Form
//   – jeder hinterlegte Denkfehler-Wert wird als genau dieser Fehler erkannt und nie als richtig
//   – ein ungekürzter Bruch gilt als «fast», nicht als falsch
//   – der Lösungsweg endet beim Ergebnis; LaTeX ohne unausgeglichene Klammern, ohne «undefined»
//   – Schrittliste («Nächster Schritt»): nicht leer, jeder Titel konkret (nicht «Schritt 2», «Rechnen»),
//     LaTeX in Titeln und Zeilen ausgeglichen, jedes Stück des Lösungswegs kommt in einem Schritt vor;
//     bei Hierarchie und Vorzeichen nennt jeder Titel eine Teilrechnung «Regel: \(… = …\)»
//   – Gegenrechnung in python3 mit fractions.Fraction: jede Lösung unabhängig nachgerechnet
//     (Terme mit Pythons eigener Rangfolge, in der −3**2 = −9 gilt; Perioden über die
//     ausgeschriebene Dezimalzahl; abbrechend/periodisch über die Langdivision)
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'rechentrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, pruefe, dezimal, qTex, Q, ggT, termAufgabe, F_REIHE, F_VZ, lies, parse, rechne, schrittListe };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 400;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  let r = 0; for (const ch of z.replace(/\\[a-z]+/g, '')) { if (ch === '(') r++; if (ch === ')') r--; }
  if (r !== 0) melde('LaTeX: ( ) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+|- \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
}
// Schrittliste: Stücke der weg-Zeilen (getrennt an «=») müssen in start oder den Schrittzeilen stehen,
// {text}-Zeilen in einem Titel oder als Schrittzeile.
const norm = z => z.replace(/\\quad\s*\\Rightarrow\s*\\quad/g, '=').replace(/\\displaystyle|\s+/g, '');
const GENERISCH = /^(schritt\s*\d*|rechnen|ausrechnen|lösung|weiter|vereinfachen)[.:]?$/i;
function schrittePruefen(a, thema, wo) {
  const liste = K.schrittListe(a);
  if (!Array.isArray(liste) || !liste.length) { melde('Schrittliste leer', wo); return; }
  const stuecke = new Set(), texte = [];
  const zerlege = z => norm(z).split('=').filter(Boolean).forEach(t => stuecke.add(t));
  if (a.start) { latexOk(a.start, wo + ' Start'); zerlege(a.start); }
  for (const s of liste) {
    if (typeof s.titel !== 'string' || s.titel.trim().length < 10 || GENERISCH.test(s.titel.trim())) melde('Schritttitel leer oder generisch', wo + ': ' + s.titel);
    else latexOk(s.titel, wo + ' Titel');
    texte.push(norm(s.titel || ''));
    if (!s.zeilen || !s.zeilen.length) melde('Schritt ohne Zeile', wo + ': ' + s.titel);
    for (const z of s.zeilen || []) {
      if (typeof z === 'string') { latexOk(z, wo + ' Schritt'); zerlege(z); }
      else { latexOk(z.text, wo + ' Schritt'); texte.push(norm(z.text)); }
    }
    if ((thema === 'reihenfolge' || thema === 'vorzeichen') && !/^[^\\]{6,}: \\\(.+ = .+\\\)/.test(s.titel)) melde('Schritttitel ohne Regel und Teilrechnung', wo + ': ' + s.titel);
  }
  for (const w of a.weg) {
    if (typeof w === 'string') { for (const t of norm(w).split('=').filter(Boolean)) if (!stuecke.has(t)) melde('Lösungsweg-Stück fehlt in den Schritten', wo + ': ' + t); }
    else { const t = norm(w.text).replace(/[.:]$/, ''); if (!texte.some(x => x.includes(t))) melde('Lösungsweg-Text fehlt in den Schritten', wo + ': ' + w.text); }
  }
}
const alsEingabe = (q, art) => art === 'dezimal' ? K.dezimal(q) : art === 'prozent' ? K.dezimal(q) + '%' : q.d === 1 ? String(q.n) : q.n + '/' + q.d;

const py = [];
let zahl = 0;
for (const thema of Object.keys(K.THEMEN)) {
  for (let i = 0; i < N; i++) {
    const a = K.THEMEN[thema].neu();
    if (!a) continue;
    zahl++;
    const wo = thema + ' «' + a.ausdruck + '»';
    latexOk(a.ausdruck, wo);
    for (const w of a.weg) latexOk(typeof w === 'string' ? w : w.text, wo + ' Weg');
    schrittePruefen(a, thema, wo);
    if (a.art === 'wahl') {
      if (K.pruefe(a, a.loesung).status !== 'ok') melde('Musterlösung nicht angenommen', wo);
      for (const [k] of a.wahl) if (k !== a.loesung && K.pruefe(a, k).status !== 'falsch') melde('Falsche Wahl nicht als falsch erkannt', wo + ' ' + k);
      if (thema === 'periodisch') py.push({ art: 'abbr', n: a.pruefPy[0], d: a.pruefPy[1], soll: a.loesung, wo });
      if (thema === 'mengen') py.push({ art: 'menge', wert: a.mengeWert, soll: a.loesung, wo });
      continue;
    }
    const r = K.pruefe(a, alsEingabe(a.loesung, a.art));
    if (r.status !== 'ok') melde('Musterlösung nicht angenommen', wo + ' → ' + alsEingabe(a.loesung, a.art) + ' ' + JSON.stringify(r));
    for (const [code, w] of a.diag) {
      if (!K.FEHLER[code]) melde('Fehlercode ohne Text', code);
      const e = alsEingabe(w, w.d === 1 || a.art === 'zahl' || a.art === 'bruch' ? 'bruch' : a.art === 'prozent' ? 'prozent' : (Number.isInteger(Math.log10(w.d)) || [2, 4, 5, 8, 16, 20, 25, 40, 50, 80].includes(w.d)) ? 'dezimal' : 'bruch');
      const p = K.pruefe(a, e);
      if (p.status === 'ok') melde('Denkfehler-Wert als richtig angenommen', wo + ' ' + code + ' ' + e);
      else if (p.status === 'falsch' && p.code !== code && !(p.code === 'stellen' && code === 'stellen')) {
        // derselbe Wert kann zu zwei Fehlern passen; dann zählt der erste der Liste
        const erster = a.diag.find(([, u]) => u.n === w.n && u.d === w.d)[0];
        if (erster !== p.code) melde('Denkfehler falsch zugeordnet', wo + ' ' + code + ' → ' + p.code);
      }
    }
    if (a.art === 'bruch' && a.loesung.d !== 1) {
      const f = K.pruefe(a, (2 * a.loesung.n) + '/' + (2 * a.loesung.d));
      if (f.status !== 'fast') melde('Ungekürzter Bruch nicht als «fast» erkannt', wo);
    }
    const letzte = a.weg.filter(w => typeof w === 'string').pop() || '';
    const ziel = a.art === 'dezimal' ? K.dezimal(a.loesung) : a.art === 'prozent' ? K.dezimal(a.loesung) + '\\%' : K.qTex(a.loesung);
    if (!letzte.endsWith(ziel) && !(thema === 'periodisch' && letzte.includes(ziel))) melde('Lösungsweg endet nicht beim Ergebnis', wo + ' → ' + letzte + ' | ' + ziel);
    py.push({ art: 'wert', ausdruck: a.pyth, n: a.loesung.n, d: a.loesung.d, wo });
    if (a.pruefPer) py.push({ art: 'periode', per: a.pruefPer, n: a.loesung.n, d: a.loesung.d, wo });
  }
}

// Gezielte Fälle aus TODO-trainer-korrekturen.md (RT-B1 … RT-C10)
function fall(id, ok, info) { if (!ok) melde(id, info); }
{
  // RT-B1: gemischte Zahl richtig lesen, bei verlangtem Bruch «fast»
  const l = K.lies('1 1/2');
  fall('RT-B1 gemischte Zahl falsch gelesen', l.q && l.q.n === 3 && l.q.d === 2, JSON.stringify(l));
  const l2 = K.lies('-2 3/4');
  fall('RT-B1 negative gemischte Zahl falsch gelesen', l2.q && l2.q.n === -11 && l2.q.d === 4, JSON.stringify(l2));
  const ab = { thema: 'brueche', art: 'bruch', loesung: K.Q(3, 2), diag: [] };
  const r = K.pruefe(ab, '1 1/2');
  fall('RT-B1 gemischte Zahl nicht «fast»', r.status === 'fast' && /als Bruch/.test(r.text || ''), JSON.stringify(r));
  fall('RT-B1 falsche gemischte Zahl nicht «falsch»', K.pruefe(ab, '1 1/3').status === 'falsch', JSON.stringify(K.pruefe(ab, '1 1/3')));
}
const codeVon = (thema, ascii, flags, eingabe) => { const a = K.termAufgabe(thema, ascii, flags); return a ? K.pruefe(a, eingabe).code : 'keine Aufgabe'; };
const erwarte = (id, thema, ascii, flags, eingabe, code) => { const c = codeVon(thema, ascii, flags, eingabe); fall(id, c === code, ascii + ' → ' + eingabe + ': ' + c + ' statt ' + code); };
// RT-B2: Klammer übersehen getrennt nach Minus vor der Klammer und Vorrang der Klammer
erwarte('RT-B2 Klammer-Diagnose', 'reihenfolge', '4 * (7 - 5) ^ 2', K.F_REIHE, '3', 'klammerVorrang');
// 6·(5 − 6)² = 6; ohne Klammer −6 = −Lösung, darum nach RT-C4 «Vorzeichen» (auch (5 − 6)² = −1 ergibt −6)
erwarte('RT-B2 Klammer-Diagnose', 'reihenfolge', '6 * (5 - 6) ^ 2', K.F_REIHE, '-6', 'vz');
erwarte('RT-B2 Klammer-Diagnose', 'reihenfolge', '(3 + 5) ^ 2 - 11', K.F_REIHE, '17', 'klammerVorrang');
erwarte('RT-B2 Klammer-Diagnose', 'reihenfolge', '10 - (5 - 2)', K.F_REIHE, '3', 'minusKlammer');
erwarte('RT-B2 Klammer-Diagnose', 'vorzeichen', '(-3) ^ 2 - (-6)', K.F_VZ, '-3', 'klammerPot');
fall('RT-B2 ohneKlammer noch vorhanden', !K.FEHLER.ohneKlammer, '');
// RT-B3: minusminus für jeden negativen Operanden, −(−b) und +(−b)
erwarte('RT-B3 Vorzeichen ohne Diagnose', 'vorzeichen', '2 * (-4) - 8 * (-3)', K.F_VZ, '-32', 'minusminus');
erwarte('RT-B3 Vorzeichen ohne Diagnose', 'vorzeichen', '-9 - 8 * (-2)', K.F_VZ, '-25', 'minusminus');
erwarte('RT-B3 Vorzeichen ohne Diagnose', 'vorzeichen', '-(-5) + 7', K.F_VZ, '2', 'minusminus');
erwarte('RT-B3 Vorzeichen ohne Diagnose', 'vorzeichen', '(-12) : 3 + (-5)', K.F_VZ, '1', 'minusminus');
// RT-B4: Text von «vz» passt auch bei Summen
fall('RT-B4 vz-Text nennt Produkte', !/Produkten/.test(K.FEHLER.vz[1]), K.FEHLER.vz[1]);
// RT-C1: Prozent als Bruch → fast
{ const a = { thema: 'umwandeln', art: 'prozent', loesung: K.Q(75), diag: [] };
  fall('RT-C1 Bruch bei Prozent angenommen', K.pruefe(a, '150/2').status === 'fast', JSON.stringify(K.pruefe(a, '150/2'))); }
// RT-C2: Kürzungsmeldung mit Vorzeichen
{ const r = K.pruefe({ thema: 'brueche', art: 'bruch', loesung: K.Q(-1, 2), diag: [] }, '-2/4');
  fall('RT-C2 Vorzeichen fehlt in der Kürzungsmeldung', r.status === 'fast' && r.text.includes('-\\frac{2}{4} = -\\frac{1}{2}'), JSON.stringify(r)); }
// RT-C4: Wert = −Lösung heisst «Vorzeichen», nicht «Strich vor Punkt»
erwarte('RT-C4 Mehrdeutige Diagnose', 'reihenfolge', '12 - 7 * 6', K.F_REIHE, '30', 'vz');
// RT-C8, RT-C9: Wortlaut
fall('RT-C8 «nur die Primfaktoren 2 und 5»', !/nur die Primfaktoren/.test(html), '');
fall('RT-C9 Thema heisst nicht «Hierarchie der Operationen»', /Hierarchie/.test(K.THEMEN.reihenfolge.name), K.THEMEN.reihenfolge.name);
// RT-C10: Themen-Schalter mit aria-pressed
fall('RT-C10 aria-pressed fehlt', /aria-pressed/.test(html.slice(html.indexOf('// ── KERN:ENDE'))), '');
// Zufallsaufgaben gezielt
const ohneKl = s => s.replace(/^= /, '').replace(/[()]/g, '');
const asciiVon = py => py.replace(/Fraction\((\d+)\)/g, '$1').replace(/\*\*/g, '^').replace(/\//g, ':');
for (let i = 0; i < N; i++) {
  for (const thema of ['reihenfolge', 'vorzeichen']) {
    const a = K.THEMEN[thema].neu(); if (!a) continue;
    const zeilen = a.weg.filter(w => typeof w === 'string');
    for (let k = 1; k < zeilen.length; k++)   // RT-B6: kein Schritt, der nur Klammern weglässt
      if (ohneKl(zeilen[k]) === ohneKl(zeilen[k - 1])) melde('RT-B6 leerer Schritt im Lösungsweg', zeilen[k - 1] + ' | ' + zeilen[k]);
    if (thema === 'vorzeichen' && !a.diag.some(([c]) => c !== 'vz')) melde('RT-B3 Vorzeichen-Aufgabe ohne Diagnose', a.ausdruck);
    if (a.pyth.includes('**')) {             // RT-C3: Hochzahl als Faktor muss sich vom richtigen Wert unterscheiden
      const asc = asciiVon(a.pyth), w = K.rechne(K.parse(asc, { potmal: true }), { potmal: true });
      if (w && w.n === a.loesung.n && w.d === a.loesung.d) melde('RT-C3 potmal ergibt die Lösung', a.ausdruck);
    }
  }
  { const a = K.THEMEN.brueche.neu();
    if (a) {
      const m = /^Fraction\((-?\d+), (\d+)\) (.) Fraction\((-?\d+), (\d+)\)$/.exec(a.pyth);
      const ad = +m[2], bd = +m[5], op = m[3], N2 = ad * bd / K.ggT(ad, bd);
      if (ad > 10 || bd > 10) melde('RT-B5 Nenner über 10', a.ausdruck);
      if ((op === '+' || op === '-') && N2 > 60) melde('RT-B5 Hauptnenner über 60', a.ausdruck);
      const txt = a.weg.map(w => typeof w === 'string' ? w : w.text).join(' ');
      if (/beide Brüche erweitern/.test(txt) && (ad === N2 || bd === N2)) melde('RT-C5 «beide Brüche erweitern» ohne Grund', a.ausdruck);
      if (/^1 /.test(a.ausdruck) || /\}\{1 \\cdot|\}\{\d+ \\cdot 1\}/.test(txt)) melde('RT-C6 trivialer Faktor 1', a.ausdruck + ' | ' + txt);
    } }
  { const a = K.THEMEN.umwandeln.neu();
    if (a) {
      const txt = a.weg.map(w => typeof w === 'string' ? w : w.text).join(' ');
      for (const [, f] of txt.matchAll(/\\cdot (\d+)\}/g)) if (+f > 250) melde('RT-C7 Erweiterungsfaktor über 250', txt);
      if (/\\frac\{-?\d+\.\d/.test(txt)) melde('RT-C9 Dezimalzahl im Bruch', txt);
    } }
  { const a = K.THEMEN.periodisch.neu();
    if (a) {
      const txt = a.weg.map(w => typeof w === 'string' ? w : w.text).join(' ');
      if (/(^|[^a-z\\])x\b/.test(txt)) melde('RT-C9 Variable x statt z', txt);
    } }
}

// Gegenrechnung in python3
const skript = `
import sys, json
from fractions import Fraction
fehler = []
for z in json.load(sys.stdin):
    try:
        if z['art'] == 'wert':
            v = eval(z['ausdruck'], {'Fraction': Fraction})
            if Fraction(v) != Fraction(z['n'], z['d']):
                fehler.append(['Python rechnet anders', z['wo'] + ' py=' + str(v)])
        elif z['art'] == 'periode':
            p = z['per']
            s = str(p['ganz']) + '.' + p['vor'] + p['per'] * 40
            if abs(float(s) - z['n'] / z['d']) > 1e-12:
                fehler.append(['Periode falsch umgerechnet', z['wo']])
        elif z['art'] == 'abbr':
            q = Fraction(z['n'], z['d']); r = q.numerator % q.denominator; seen = set(); abbr = True
            while r:
                if r in seen: abbr = False; break
                seen.add(r); r = (r * 10) % q.denominator
            if ('abbrechend' if abbr else 'periodisch') != z['soll']:
                fehler.append(['abbrechend/periodisch falsch', z['wo']])
        elif z['art'] == 'menge':
            w = z['wert']; ganz = abs(w - round(w)) < 1e-12
            if z['soll'] in ('N', 'Z') and not ganz: fehler.append(['Menge: Zahl nicht ganz', z['wo']])
            if z['soll'] == 'N' and w < -1e-12: fehler.append(['Menge: negative Zahl in N', z['wo']])
            if z['soll'] == 'Z' and w >= 0: fehler.append(['Menge: Z, aber nicht negativ', z['wo']])
            if z['soll'] in ('Q', 'R') and ganz: fehler.append(['Menge: ganze Zahl in Q/R', z['wo']])
    except Exception as e:
        fehler.append(['Python-Fehler', z['wo'] + ' ' + str(e)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 28 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 300));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.THEMEN).length} Themen · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
