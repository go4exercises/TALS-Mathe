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
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, FORM, aufgabe, pruefe, parse, wert, rGleich, T, tex, variablen, faktorListe, pMul, pKonst };', ctx);
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
  a.diag.forEach(([c1, w1], j) => a.diag.slice(j + 1).forEach(([c2, w2]) => { if (c1 !== c2 && gleich(w1, w2)) melde('TT-C6: zwei Denkfehler mit gleichem Wert', wo + ' ' + c1 + '/' + c2 + ' ' + w1); }));
  if (a.thema === 'ausmultiplizieren' && a.diag.some(([c]) => c === 'vzProdukt') && !a.aufg.includes('-')) melde('TT-C7: vzProdukt ohne negativen Faktor', wo);
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

// Gezielte Fälle aus der Prüfung vom 11.10.2026 (TODO-trainer-korrekturen.md, TT-B1 … TT-C10)
function fall(thema, form, aufg, loes) {
  const t = { thema, form, aufg, loes, diag: [], weg: [] };
  t.baum = K.parse(aufg); t.loesBaum = K.parse(loes); t.vars = K.variablen(t.baum);
  t.ausdruck = K.tex(t.baum); t.loesTex = K.tex(t.loesBaum);
  return t;
}
function erwarte(wo, a, eingabe, status, textTeil) {
  const r = K.pruefe(a, eingabe);
  if (r.status !== status || (textTeil && !(r.text || '').includes(textTeil))) melde('Gezielter Fall ' + wo, '«' + a.aufg + '» ← ' + eingabe + ' → ' + JSON.stringify(r));
}
function suche(thema, aufg) {
  for (let k = 0; k < 400000; k++) { const a = K.aufgabe([thema]); if (a.aufg === aufg) return a; }
  melde('Gezielter Fall: Aufgabe nicht gefunden', thema + ' ' + aufg); return null;
}
function diagnostiziert(wo, a, eingabe) {
  if (!a) return;
  const r = K.pruefe(a, eingabe);
  if (r.status !== 'falsch' || r.code === 'sonst') melde('Gezielter Fall ' + wo + ': Denkfehler nicht erkannt', '«' + a.aufg + '» ← ' + eingabe + ' → ' + JSON.stringify(r));
}
// TT-B1: Faktoren mit Brüchen
{ const a = fall('faktorisieren', 'produkt', '4x^2-1', '(2x+1)(2x-1)');
  erwarte('TT-B1', a, '4(x+1/2)(x-1/2)', 'fast', 'ganzen Zahlen');
  const b = fall('faktorisieren', 'produkt', 'x^2+3x+2', '(x+1)(x+2)');
  erwarte('TT-B1', b, '(x/2+1)(2x+2)', 'fast', 'ganzen Zahlen'); }
// TT-B2: Doppelbruch
{ const a = fall('bruchterme', 'bruch', '(3x-9)/(x^2-9)', '3/(x+3)');
  erwarte('TT-B2', a, '3/((x+3)/1)', 'fast'); erwarte('TT-B2', a, '3/(x+3)', 'ok');
  const b = fall('bruchterme', 'bruch', '(4x^2+24x+36)/(x^2-9)', '4(x+3)/(x-3)');
  erwarte('TT-B2', b, '(x+3)/((x-3)/4)', 'fast'); erwarte('TT-B2', b, '4(x+3)/(x-3)', 'ok'); }
// TT-B3: unvereinfachte Summen in Faktoren und im gekürzten Bruch
erwarte('TT-B3', fall('faktorisieren', 'produkt', 'x^2-9', '(x+3)(x-3)'), '(x+5-2)(x-3)', 'fast');
erwarte('TT-B3', fall('ausklammern', 'produkt', '6x^2-9x', '3x(2x-3)'), '3x(x+x-3)', 'fast');
erwarte('TT-B3', fall('bruchterme', 'bruch', '(x^2-3x)/x', 'x-3'), 'x+x-3-x', 'fast');
erwarte('TT-B3', fall('bruchterme', 'bruch', '(x^2-3x)/(x^2-9)', 'x/(x+3)'), 'x/(x+5-2)', 'fast');
// TT-B4: häufige Fehler mit Diagnose
{ const a = suche('binome', '(x - 3)^2'); diagnostiziert('TT-B4', a, 'x^2+6x+9'); diagnostiziert('TT-B4', a, 'x^2-9');
  diagnostiziert('TT-B4', suche('bruchterme', '(x^2 - 9)/(x + 3)'), 'x+3');
  diagnostiziert('TT-B4', suche('bruchterme', '(x^2 - 6x + 9)/(9 - x^2)'), '(x-3)/(x+3)');
  diagnostiziert('TT-B4', suche('faktorisieren', '2x^2 - 18'), '(x+3)(x-3)'); }
// TT-C1: Zahl hinter der Klammer
erwarte('TT-C1', fall('faktorisieren', 'produkt', '2x^2-18', '2(x+3)(x-3)'), '(x+3)(x-3)2', 'format', 'vorne');
// TT-C2: Bruchstrich in der Summe
erwarte('TT-C2', fall('ausmultiplizieren', 'summe', '(x+2)(x+3)', 'x^2+5x+6'), 'x^2+5x+6/1', 'fast', 'Bruchstrich');
// TT-C3: Kosmetisches
{ const a = fall('ausmultiplizieren', 'summe', '(x+2)(x+3)', 'x^2+5x+6');
  for (const e of ['1x^2+5x+6', 'x^2+5x^1+6', 'x^2+5x+6x^0']) erwarte('TT-C3', a, e, 'fast', 'Glied');
  erwarte('TT-C3', fall('ausklammern', 'produkt', '4x^3+4x^2', '4x^2(x+1)'), '4xx(x+1)', 'fast'); }
// TT-C4, TT-C5: Wortlaut
if (K.FORM.einBruch.includes('(x-3)/(x+3)')) melde('TT-C4: festes Beispiel in FORM.einBruch', K.FORM.einBruch);
if (!/px/.test(K.FEHLER.vietaVz[1])) melde('TT-C5: p und q nicht eingeführt', K.FEHLER.vietaVz[1]);
// TT-C8: Leser
if (K.pruefe(a0, '2 3x').status !== 'format') melde('TT-C8: «2 3x» nicht abgefangen', JSON.stringify(K.pruefe(a0, '2 3x')));
for (const [u, v] of [['x⁴', 'x^4'], ['x÷2', 'x/2'], ['x¹²', 'x^12']]) { try { if (!gleich(u, v)) melde('TT-C8: Schreibweise nicht gelesen', u); } catch (e) { melde('TT-C8: Schreibweise nicht gelesen', u); } }
// TT-C9, TT-C10, RT-C10: Oberfläche und Links
if (!/id="tt-tasten"/.test(html)) melde('TT-C9: Tastenleiste fehlt', '');
for (const [, n] of kern.matchAll(/const (L_[A-Z]+) =/g)) if ((kern.match(new RegExp('\\b' + n + '\\b', 'g')) || []).length < 2) melde('TT-C10: Link-Konstante nie benutzt', n);
if (!/aria-pressed/.test(html)) melde('RT-C10: Themen-Schalter ohne aria-pressed', '');

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
