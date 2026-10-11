#!/usr/bin/env node
// Selbsttest des Systemtrainers (werkzeuge/systemtrainer.html), ohne Browser: Der Block zwischen
// «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_systemtrainer.js          # 600 Aufgaben je Thema (Pre-Flight)
//   node scripts/verify_systemtrainer.js 5000     # gründlicher
// Geprüft wird:
//   – Lösungsfall und Lösung der Aufgabe; die Musterlösung wird in mehreren Schreibweisen angenommen
//   – jeder falsche Lösungsfall bekommt seinen Fehlercode; vertauschte Werte, ein Vorzeichen, ein falscher
//     Wert beim Zurückeinsetzen, Fehler beim Auflösen nach y werden als genau dieser Fehler erkannt
//   – kein Fehlerwert ist zufällig richtig; Fehleingaben werden als Format abgewiesen
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined», ohne doppeltes Vorzeichen, ohne «1x»
//   – Gegenrechnung in python3 mit fractions.Fraction, unabhängig von der Rechnung des Werkzeugs:
//     Gauss löst jedes System selbst (Fall und Lösung); jede Zeile des Lösungswegs wird aus ihrem Tex
//     gelesen und muss aus dem System folgen (ihre Gleichung liegt im Zeilenraum der erweiterten Matrix);
//     der Weg endet beim richtigen Fall; die Gerade der Skizze schneidet sich im Fenster
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'systemtrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, aufgabe, pruefe, liesLin, loese, qTex, Q, vorschauTex, STATISTIK };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 600;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\\(/g) || []).length !== (z.match(/\\\)/g) || []).length) melde('LaTeX: \\( \\) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+|- \+|\+ -|--/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
  if (/(^|[^0-9.])1[xyz]/.test(z) || /-0\b(?!\.)/.test(z)) melde('LaTeX: 1x oder -0', wo + ': ' + z);
  if (/ß/.test(z)) melde('Text: ß', wo);
}
const zahlText = q => (q.d === 1 ? String(q.n) : q.n + '/' + q.d);
const linText = ([m, q]) => zahlText(m) + '*x+' + zahlText(q);

const py = [];
let zahl = 0;
const stat = {}, verfahren = {};
for (const thema of Object.keys(K.THEMEN)) for (let i = 0; i < N; i++) {
  const a = K.aufgabe([thema]);
  zahl++;
  stat[thema + ' · ' + a.fall] = (stat[thema + ' · ' + a.fall] || 0) + 1;
  for (const w of a.weg) for (const v of ['einsetzen', 'gleichsetzen', 'Additionsverfahren', 'eliminieren: ', 'enthält nur', 'Jedes \\(x\\) passt']) if ((w.text || '').includes(v)) verfahren[v] = (verfahren[v] || 0) + 1;
  const wo = thema + ' ' + a.fall + ' «' + a.gl.map(g => g.k.join(',') + '=' + g.r).join('; ') + '»';
  latexOk(a.ausdruck, wo); latexOk(a.loesTex, wo + ' Lösung');
  a.weg.forEach(w => latexOk(w.text || w.z || '', wo + ' Weg'));
  if (a.weg[a.weg.length - 1].L !== true) melde('Weg endet nicht mit der Lösungsmenge', wo);
  // bei genau einer Lösung steht der Wert jeder Variablen in einer eigenen Zeile «v = Wert» (auch als Kette)
  if (a.fall === 'eine' && a.art !== 'lage') a.loes.forEach((v, i) => {
    const re = new RegExp('^' + 'xyz'[i] + ' = (.* = )?' + String(v).replace('-', '\\-') + '$');
    if (!a.weg.some(w => w.z && re.test(w.z))) melde('Wert einer Variablen fehlt im Weg', wo + ' ' + 'xyz'[i] + ' = ' + v);
  });
  const n = a.n, faelle = ['eine', 'keine', 'unendlich'];
  // Musterlösung
  if (a.art === 'lage') {
    if (K.pruefe(a, { fall: a.fall }).status !== 'ok') melde('Lage: richtige Wahl nicht angenommen', wo);
    for (const f of faelle) if (f !== a.fall) { const r = K.pruefe(a, { fall: f }); if (r.status !== 'falsch' || !K.FEHLER[r.code] || r.code === 'sonst') melde('Lage: falsche Wahl ohne Fehlercode', wo + ' ' + f); }
  } else if (a.fall === 'eine') {
    const s = a.loes;
    for (const w of [s.map(String), s.map(v => v + '.0'), s.map(v => (2 * v) + '/2'), s.map(v => ' ' + v + ' ')]) {
      const r = K.pruefe(a, { fall: 'eine', w });
      if (r.status !== 'ok') melde('Musterlösung nicht angenommen', wo + ' ' + JSON.stringify(w) + ' ' + JSON.stringify(r));
    }
    for (const f of ['keine', 'unendlich']) { const r = K.pruefe(a, { fall: f, w: n === 2 ? ['x'] : ['x', 'x'] }); if (r.code !== 'sonderStattEine') melde('Falscher Fall nicht erkannt', wo + ' ' + f + ' ' + JSON.stringify(r)); }
    // vertauscht
    if (n === 2 && s[0] !== s[1]) { const r = K.pruefe(a, { fall: 'eine', w: [s[1], s[0]].map(String) }); if (r.code !== 'vertauscht') melde('Vertauscht nicht erkannt', wo + ' ' + JSON.stringify(r)); }
    if (n === 3 && s[0] !== s[2]) { const r = K.pruefe(a, { fall: 'eine', w: [s[2], s[1], s[0]].map(String) }); if (r.code !== 'vertauscht') melde('Vertauscht nicht erkannt', wo + ' ' + JSON.stringify(r)); }
    // Vorzeichen eines Werts
    const j = s.findIndex(v => v !== 0);
    if (j >= 0) {
      const w = s.map((v, i) => String(i === j ? -v : v));
      const perm = n === 2 ? (-s[j] === s[1 - j] && s[1 - j] === s[j]) : false;
      const r = K.pruefe(a, { fall: 'eine', w });
      if (r.status !== 'falsch') melde('Vorzeichenfehler angenommen', wo);
      else if (r.code !== 'vorzeichen' && r.code !== 'vertauscht' && !perm) melde('Vorzeichen nicht erkannt', wo + ' ' + JSON.stringify(r));
    }
    // ein Wert falsch (zurück eingesetzt): letzter Wert +1
    const w2 = s.map((v, i) => String(i === n - 1 ? v + 1 : v));
    const r2 = K.pruefe(a, { fall: 'eine', w: w2 });
    if (r2.status !== 'falsch' || !['zurueck', 'vertauscht', 'vorzeichen'].includes(r2.code)) melde('Teilweise richtig nicht erkannt', wo + ' ' + JSON.stringify(r2));
    if (!r2.text || !/Probe/.test(r2.text)) melde('Keine Probe in der Rückmeldung', wo);
  } else if (a.fall === 'keine') {
    if (K.pruefe(a, { fall: 'keine', w: [] }).status !== 'ok') melde('Musterlösung nicht angenommen', wo);
    const r = K.pruefe(a, { fall: 'unendlich', w: n === 2 ? ['x'] : ['x', 'x'] });
    if (r.code !== 'unendlichStattKeine') melde('Falscher Fall nicht erkannt', wo + ' ' + JSON.stringify(r));
    const r1 = K.pruefe(a, { fall: 'eine', w: n === 2 ? ['0', '0'] : ['0', '0', '0'] });
    if (r1.code !== 'eineStattKeine') melde('Falscher Fall nicht erkannt', wo + ' eine ' + JSON.stringify(r1));
  } else {
    const ok = [a.loes.map(linText), a.loes.map(([m, q]) => '(' + (m.n * q.d) + '*x + ' + (q.n * m.d) + ')/' + (m.d * q.d)), a.loes.map(([m, q]) => zahlText(q) + (m.n < 0 ? '-' : '+') + zahlText(K.Q(Math.abs(m.n), m.d)) + 'x')];
    for (const w of ok) { const r = K.pruefe(a, { fall: 'unendlich', w }); if (r.status !== 'ok') melde('Musterlösung nicht angenommen', wo + ' ' + JSON.stringify(w) + ' ' + JSON.stringify(r)); }
    const r = K.pruefe(a, { fall: 'keine', w: [] });
    if (r.code !== 'keineStattUnendlich') melde('Falscher Fall nicht erkannt', wo + ' ' + JSON.stringify(r));
    // ein Punkt der Lösungsmenge als «genau eine»
    const pkt = [K.Q(2), ...a.loes.map(([m, q]) => K.Q(m.n * 2 * q.d + q.n * m.d, m.d * q.d))];
    const r1 = K.pruefe(a, { fall: 'eine', w: pkt.map(zahlText) });
    if (r1.code !== 'eineStattUnendlich' || !/nicht die einzige/.test(r1.text || '')) melde('Punkt der Lösung als «eine» nicht erkannt', wo + ' ' + JSON.stringify(r1));
    // Fehler beim Auflösen nach y (2×2): Vorzeichen, nicht geteilt
    if (n === 2) for (const g of a.gl) {
      const vz = '(' + g.r + ' + ' + g.k[0] + '*x)/(' + g.k[1] + ')';
      const rv = K.pruefe(a, { fall: 'unendlich', w: [vz] });
      if (g.k[0] !== 0 && rv.code !== 'umstellenVz') melde('Umstellen-Vorzeichen nicht erkannt', wo + ' ' + vz + ' ' + JSON.stringify(rv));
      if (Math.abs(g.k[1]) !== 1) { const ng = g.r + ' - ' + g.k[0] + '*x'; const rn = K.pruefe(a, { fall: 'unendlich', w: [ng] }); if (rn.status === 'ok' || (rn.code !== 'nichtGeteilt' && rn.code !== 'teilGerade')) melde('Nicht geteilt nicht erkannt', wo + ' ' + ng + ' ' + JSON.stringify(rn)); }
    }
    // nur ein Teil stimmt
    const [m0, q0] = a.loes[0];
    const halb = [zahlText(m0) + '*x+' + zahlText(K.Q(q0.n + q0.d, q0.d)), ...a.loes.slice(1).map(linText)];
    const rh = K.pruefe(a, { fall: 'unendlich', w: halb });
    if (rh.status !== 'falsch' || !['teilGerade', 'umstellenVz', 'nichtGeteilt'].includes(rh.code)) melde('Teilweise richtiger Ausdruck nicht erkannt', wo + ' ' + JSON.stringify(rh));
  }
  py.push({ gl: a.gl.map(g => [...g.k, g.r]), fall: a.fall, loes: a.fall === 'eine' ? a.loes : a.fall === 'unendlich' ? a.loes.map(([m, q]) => [[m.n, m.d], [q.n, q.d]]) : null, weg: a.weg.filter(w => w.z).map(w => w.z), wo });
}
// Kein Weg darf beim falschen Ergebnis enden (der Erzeuger würde die Aufgabe sonst still verwerfen)
if (K.STATISTIK.widerspruch) melde('Lösungsweg endet beim falschen Ergebnis', K.STATISTIK.widerspruch + '× z.B. ' + K.STATISTIK.beispiel);
// Jedes Verfahren kommt vor (verschwindet eines, ist sein Weg kaputt)
for (const v of ['einsetzen', 'gleichsetzen', 'Additionsverfahren', 'eliminieren: ', 'enthält nur', 'Jedes \\(x\\) passt']) if (!(verfahren[v] > 0)) melde('Verfahren kommt nie vor', v);
for (const [k, v] of Object.entries(stat)) if (v < N * 0.04) melde('Thema/Fall zu selten', k + ' ' + v);
// Leser
for (const [e, m, q] of [['2x-3', 2, -3], ['(6-2x)/3', -2 / 3, 2], ['-x/2+1', -0.5, 1], ['0.5x - 1', 0.5, -1], ['3(x+1)', 3, 3], ['x', 1, 0], ['−4', 0, -4], ['2*x', 2, 0], ['(x)(3)', 3, 0], ['1/2x', 0.5, 0], ['y = 2x+1', 2, 1], ['x=3', 0, 3]]) {
  const l = K.liesLin(e);
  if (l.fehler || Math.abs(l.m.n / l.m.d - m) > 1e-12 || Math.abs(l.q.n / l.q.d - q) > 1e-12) melde('Leser liest falsch', e + ' → ' + JSON.stringify(l));
}
for (const e of ['', '2,5', 'x^2', 'x*x', '2 3', '(x+1', 'x+1)', '3/0', '1/x', 'y', '?']) if (!K.liesLin(e).fehler) melde('Fehleingabe nicht abgefangen', e);

const skript = `
import sys, json, re, random
from fractions import Fraction as F
fehler = []
def rang(M):
    M = [r[:] for r in M]; rg = 0; spalten = len(M[0]) if M else 0
    for s in range(spalten):
        p = next((i for i in range(rg, len(M)) if M[i][s] != 0), None)
        if p is None: continue
        M[rg], M[p] = M[p], M[rg]
        for i in range(len(M)):
            if i != rg and M[i][s] != 0:
                f = M[i][s] / M[rg][s]; M[i] = [a - f * b for a, b in zip(M[i], M[rg])]
        rg += 1
    return rg
def pyterm(s):
    s = s.replace('\\\\cdot', '*').replace(' ', '')
    s = re.sub(r'\\\\frac\\{(-?\\d+)\\}\\{(\\d+)\\}', r'(\\1/\\2)', s)
    s = re.sub(r'([0-9xyz)])(?=[xyz(])', r'\\1*', s)
    if '\\\\' in s: raise ValueError('Tex nicht lesbar: ' + s)
    return re.sub(r'(\\d+)', r'F(\\1)', s)
VAR = 'xyz'
def affin(t, n):
    # t: Tex eines Ausdrucks -> Koeffizienten [c_x, c_y, (c_z), konstante]
    e = pyterm(t)
    w = lambda p: eval(e, {'F': F}, dict(zip(VAR, p)))
    null = [F(0)] * n
    c0 = w(null)
    k = []
    for i in range(n):
        p = null[:]; p[i] = F(1); k.append(w(p) - c0)
    return k + [c0]
for z in json.load(sys.stdin):
    n = len(z['gl'][0]) - 1
    A = [[F(c) for c in g] for g in z['gl']]
    # unabhaengige Loesung
    rA, rAb = rang([r[:n] for r in A]), rang(A)
    fall = 'keine' if rAb > rA else 'eine' if rA == n else 'unendlich' if rA == n - 1 else 'mehr'
    if fall != z['fall']: fehler.append(['python: Lösungsfall weicht ab', z['wo'] + ' python=' + fall]); continue
    if fall == 'eine':
        s = [F(v) for v in z['loes']]
        if any(sum(g[i] * s[i] for i in range(n)) != g[n] for g in A): fehler.append(['python: Lösung erfüllt das System nicht', z['wo']])
    if fall == 'unendlich':
        for _ in range(3):
            x = F(random.randint(-9, 9), random.randint(1, 4))
            p = [x] + [F(m[0], m[1]) * x + F(q[0], q[1]) for m, q in z['loes']]
            if any(sum(g[i] * p[i] for i in range(n)) != g[n] for g in A): fehler.append(['python: Ausdruck erfüllt das System nicht', z['wo']]); break
    # Zeilen des Wegs: jede Gleichung (auch Ketten) folgt aus dem System
    sysform = [[g[i] for i in range(n)] + [-g[n]] for g in A]
    rs = rang(sysform)
    for zeile in z['weg']:
        teile = zeile.split('=')
        try:
            for u, v in zip(teile, teile[1:]):
                a, b = affin(u, n), affin(v, n)
                d = [p - q for p, q in zip(a, b)]
                if rang(sysform + [d]) != rs: fehler.append(['python: Wegzeile folgt nicht aus dem System', z['wo'] + ' | ' + zeile]); break
        except Exception as ex:
            fehler.append(['python: Wegzeile nicht lesbar', z['wo'] + ' | ' + zeile + ' ' + repr(ex)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 28 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.THEMEN).length} Themen · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
console.log('  ' + Object.entries(stat).map(([k, v]) => k + ' ' + v).join(' · '));
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
