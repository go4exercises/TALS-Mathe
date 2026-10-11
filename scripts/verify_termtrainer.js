#!/usr/bin/env node
// Selbsttest des Termtrainers (werkzeuge/termtrainer.html), ohne Browser: Der Block zwischen
// «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_termtrainer.js            # 400 Aufgaben je Thema (Pre-Flight)
//   node scripts/verify_termtrainer.js 3000       # gründlicher
// Geprüft wird:
//   – die Musterlösung ist gleichwertig und wird als richtig angenommen; die Aufgabe selbst gilt
//     nur als «fast» (sie hat die verlangte Form noch nicht)
//   – jede Zeile des Lösungswegs ist gleichwertig; die letzte wird angenommen, keine gilt als falsch
//   – jeder Denkfehler-Wert ist nicht gleichwertig und wird als genau dieser Fehler erkannt
//   – Formprüfung: ausmultiplizierte Lösung bei «Produkt» und erweiterter Bruch gelten als «fast»
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined», ohne doppeltes Vorzeichen
//   – Gegenrechnung in python3 mit fractions.Fraction, unabhängig vom Leser des Werkzeugs: Aufgabe,
//     Lösung, Weg und Denkfehler werden aus dem Eingabetext an Zufallsstellen ausgewertet;
//     quadratische Faktoren der Lösung sind über ℚ unzerlegbar, gekürzte Brüche haben keinen
//     gemeinsamen Faktor (Polynom-ggT)
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'termtrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, aufgabe, pruefe, parse, wert, rGleich, T, faktorListe, pMul, pKonst };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 400;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\left/g) || []).length !== (z.match(/\\right/g) || []).length) melde('LaTeX: \\left/\\right unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+|- \+|\+ -/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
  if (/(^|[^0-9])1[a-z]/.test(z.replace(/\\[a-z]+/g, ' '))) melde('LaTeX: Koeffizient 1 ausgeschrieben', wo + ': ' + z);
}
const gleich = (u, v) => K.rGleich(K.wert(K.parse(u)), K.wert(K.parse(v)));
const koeff = p => [...p.entries()];

const py = [];
let zahl = 0;
for (const thema of Object.keys(K.THEMEN)) for (let i = 0; i < N; i++) {
  const a = K.aufgabe([thema]);
  zahl++;
  const wo = thema + ' «' + a.aufg + '»';
  latexOk(a.ausdruck, wo); latexOk(a.loesTex, wo + ' Lösung');
  if (!gleich(a.aufg, a.loes)) melde('Lösung nicht gleichwertig', wo + ' → ' + a.loes);
  const r = K.pruefe(a, a.loes);
  if (r.status !== 'ok') melde('Musterlösung nicht angenommen', wo + ' → ' + a.loes + ' ' + JSON.stringify(r));
  const ra = K.pruefe(a, a.aufg);
  if (ra.status !== 'fast') melde('Aufgabe selbst nicht als «fast»', wo + ' ' + JSON.stringify(ra));
  const zeilen = a.weg.filter(w => w.a);
  zeilen.forEach((w, j) => {
    latexOk(K.T(w.a), wo + ' Weg');
    if (!gleich(a.aufg, w.a)) melde('Wegzeile nicht gleichwertig', wo + ' → ' + w.a);
    const s = K.pruefe(a, w.a).status;
    if (j === zeilen.length - 1 && s !== 'ok') melde('Letzte Wegzeile nicht angenommen', wo + ' → ' + w.a + ' ' + s);
    if (s === 'falsch') melde('Wegzeile als falsch bewertet', wo + ' → ' + w.a);
  });
  a.weg.filter(w => w.text).forEach(w => latexOk(w.text, wo + ' Text'));
  if (!zeilen.length || K.T(zeilen[zeilen.length - 1].a) !== a.loesTex) melde('Weg endet nicht bei der Lösung', wo);
  for (const [code, w] of a.diag) {
    if (!K.FEHLER[code]) melde('Fehlercode ohne Text', code);
    if (gleich(a.aufg, w)) { melde('Denkfehler-Wert ist gleichwertig', wo + ' ' + code + ' ' + w); continue; }
    const p = K.pruefe(a, w);
    const erster = a.diag.find(([, u]) => gleich(u, w))[0];
    if (p.status !== 'falsch' || p.code !== erster) melde('Denkfehler nicht erkannt', wo + ' ' + code + ' ' + w + ' → ' + JSON.stringify(p));
  }
  // Formprüfung gezielt
  if (a.form === 'produkt') {
    const aus = K.wert(K.parse(a.loes));
    const p = K.pruefe(a, [...aus.z.entries()].map(([m, c]) => (c < 0 ? '-' : '+') + Math.abs(c) + m.replace(/([a-z])(\d+)/g, '$1^$2')).join(''));
    if (p.status !== 'fast') melde('Ausmultiplizierte Lösung nicht als «fast»', wo + ' ' + JSON.stringify(p));
    const fl = K.faktorListe(K.parse(a.loes));
    py.push({ art: 'faktoren', f: fl.map(koeff), wo });
  }
  if (a.form === 'bruch') {
    const p = K.pruefe(a, '(2*(' + a.loes.replace(/\/(.*)$/, '))/(2*$1)') + (a.loes.includes('/') ? '' : '))/2'));
    if (p.status !== 'fast') melde('Erweiterter Bruch nicht als «fast»', wo + ' ' + JSON.stringify(p));
    const rl = K.wert(K.parse(a.loes));
    py.push({ art: 'gekuerzt', z: koeff(rl.z), n: koeff(rl.n), wo });
  }
  if (K.pruefe(a, 'y').status !== 'format' && !a.aufg.includes('y')) melde('Fremde Variable nicht abgewiesen', wo);
  py.push({ art: 'werte', aufg: a.aufg, loes: a.loes, weg: zeilen.map(w => w.a), diag: a.diag.map(([, w]) => w), wo });
}
// Leser: Fehleingaben werden abgefangen, Schreibweisen gelesen
const a0 = K.aufgabe(['binome']);
for (const e of ['x^', '(x+1', 'x+1)', '3x2', '2,5x', 'x^-1', '', '3*-2', '?', '()']) if (K.pruefe(a0, e).status !== 'format') melde('Fehleingabe nicht abgefangen', e);
for (const [u, v] of [['−3x²', '-3x^2'], ['2·x', '2x'], ['[x+1]', '(x+1)'], ['x:2', 'x/2'], ['X^3', 'x^3']]) if (!gleich(u, v)) melde('Schreibweise nicht gelesen', u);

const skript = `
import sys, json, re, random
from fractions import Fraction
fehler = []
def pyterm(s):
    s = s.lower().replace(' ', '').replace('^', '**')
    s = re.sub(r'([0-9a-z)])(?=[a-z(])', r'\\1*', s)
    return re.sub(r'(\\d+)', r'Fraction(\\1)', s)
def auswerten(s, bel):
    try: return eval(pyterm(s), {'Fraction': Fraction}, dict(bel))
    except ZeroDivisionError: return None
def poly(koeff):
    # Map Monom -> Koeffizient aus dem Werkzeug, nur in x (fuer die Bruchterme)
    p = {}
    for m, c in koeff:
        e = int(m[1:]) if m else 0
        p[e] = p.get(e, 0) + Fraction(c)
    g = max(p) if p else 0
    return [p.get(k, Fraction(0)) for k in range(g + 1)]
def prest(a, b):
    a = a[:]
    while len(a) >= len(b) and any(a):
        f = a[-1] / b[-1]; s = len(a) - len(b)
        for k in range(len(b)): a[s + k] -= f * b[k]
        a.pop()
        while a and a[-1] == 0: a.pop()
    return a
def pggt(a, b):
    while b and any(b):
        a, b = b, prest(a, b)
    return len(a) - 1
random.seed(7)
for z in json.load(sys.stdin):
    if z['art'] == 'werte':
        vs = sorted(set(re.findall(r'[a-z]', z['aufg'])))
        for _ in range(4):
            bel = {v: Fraction(random.randint(-40, 40), random.randint(1, 9)) for v in vs}
            soll = auswerten(z['aufg'], bel)
            if soll is None: continue
            for t, wo in [(z['loes'], 'Lösung')] + [(w, 'Weg') for w in z['weg']]:
                v = auswerten(t, bel)
                if v is not None and v != soll: fehler.append(['python: ' + wo + ' weicht ab', z['wo'] + ' ' + t])
            for t in z['diag']:
                pass
        # Denkfehler: an mindestens einer Stelle verschieden
        for t in z['diag']:
            ok = False
            for _ in range(6):
                bel = {v: Fraction(random.randint(-40, 40), random.randint(1, 9)) for v in vs}
                u, w = auswerten(z['aufg'], bel), auswerten(t, bel)
                if u is not None and w is not None and u != w: ok = True; break
            if not ok: fehler.append(['python: Denkfehler gleich der Aufgabe', z['wo'] + ' ' + t])
    elif z['art'] == 'faktoren':
        for f in z['f']:
            ms = {}
            for m, c in f: ms[m] = c
            werte = [abs(c) for c in ms.values()]
            from math import gcd
            g = 0
            for c in werte: g = gcd(g, c)
            if len(ms) > 1 and g > 1: fehler.append(['python: Faktor mit Zahlinhalt', z['wo']])
            if all(re.fullmatch(r'x\\d*', m) or m == '' for m in ms):
                p = poly(f)
                if len(p) == 3:
                    D = p[1] ** 2 - 4 * p[2] * p[0]
                    if D >= 0:
                        r = D.numerator ** 0.5, D.denominator ** 0.5
                        if int(r[0]) ** 2 == D.numerator and int(r[1]) ** 2 == D.denominator:
                            fehler.append(['python: quadratischer Faktor zerlegbar', z['wo']])
                if len(p) > 3: fehler.append(['python: Faktor vom Grad > 2', z['wo']])
    elif z['art'] == 'gekuerzt':
        zz, nn = poly(z['z']), poly(z['n'])
        if len(nn) > 1 and len(zz) > 0 and pggt(zz, nn) > 0: fehler.append(['python: Bruch nicht gekürzt', z['wo']])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 28 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.THEMEN).length} Themen · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
