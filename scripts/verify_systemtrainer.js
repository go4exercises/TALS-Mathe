#!/usr/bin/env node
// Selbsttest des Systemtrainers (werkzeuge/systemtrainer.html), ohne Browser: Der Block zwischen
// «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_systemtrainer.js          # 400 Aufgaben je Thema, je 4 Zufallswege (Pre-Flight)
//   node scripts/verify_systemtrainer.js 3000     # gründlicher
// Geprüft wird:
//   – jede Aufgabe hat einen Musterweg; auf jedem Zufallsweg (an jeder Stelle ein zufälliger passender Schritt)
//     gibt es an jeder Stelle mindestens einen passenden Schritt, und der Weg endet beim richtigen Lösungsfall
//     und bei der richtigen Lösung (STATISTIK.widerspruch bleibt 0)
//   – jeder Umweg und jeder Fehlgriff trägt eine Begründung, jeder Fehlgriff einen Code der Bilanz; Fehlgriffe
//     beim Addieren eliminieren wirklich keine Variable; jede Phase hat Frage und Tipp
//   – jede Art von Schritt kommt als passend vor, die Fehlgriffe ebenso (verschwindet eine, ist ihr Zweig kaputt)
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined», ohne doppeltes Vorzeichen, ohne «1x»
//   – Gegenrechnung in python3 mit fractions.Fraction, unabhängig von der Rechnung des Werkzeugs:
//     Gauss löst jedes System selbst (Fall und Lösung); jede Zeile jedes Wegs wird aus ihrem Tex gelesen und
//     muss aus dem System folgen (ihre Gleichung liegt im Zeilenraum der erweiterten Matrix)
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'systemtrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, FRAGE, aufgabe, zustand, optionen, tipp, Q, STATISTIK };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 400, WEGE = 4;
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
const art = id => (/^[UOVPRWZE]\d/.test(id) ? id[0] : id);   // U01 → U, Z1 → Z, E0 → E
const py = [];
let zahl = 0, schritte = 0, laengste = 0;
const stat = {}, gewaehlt = {}, angeboten = {};
for (const thema of Object.keys(K.THEMEN)) for (let i = 0; i < N; i++) {
  const a = K.aufgabe([thema]);
  zahl++;
  stat[thema + ' · ' + a.fall] = (stat[thema + ' · ' + a.fall] || 0) + 1;
  const wo = thema + ' ' + a.fall + ' ' + a.form.join(',') + ' «' + a.gl.map(g => g.k.join(',') + '=' + g.r).join('; ') + '»';
  latexOk(a.ausdruck, wo); latexOk(a.loesTex, wo + ' Lösung');
  if (!a.muster || a.muster[a.muster.length - 1].L !== true) melde('Musterweg endet nicht mit der Lösungsmenge', wo);
  for (let w = 0; w < WEGE; w++) {
    const S = K.zustand(a), pfad = [];
    for (let n = 0; S.phase !== 'ende'; n++) {
      if (n > 60) { melde('Weg endet nicht', wo + ' ' + pfad.join(' ')); break; }
      const opt = K.optionen(S), ph = S.phase;
      latexOk(K.FRAGE[ph](S), wo + ' Frage ' + ph);
      if (ph !== 'lage' && !K.tipp(S)) melde('Phase ohne Tipp', ph);
      if (new Set(opt.map(o => o.id)).size !== opt.length) melde('Doppelte Schritte', wo + ' ' + ph + ' ' + opt.map(o => o.id));
      for (const o of opt) {
        latexOk(o.label, wo + ' ' + o.id);
        angeboten[art(o.id) + ':' + o.st] = (angeboten[art(o.id) + ':' + o.st] || 0) + 1;
        if (o.st !== 'ok') { if (!o.grund) melde('Umweg oder Fehlgriff ohne Begründung', wo + ' ' + ph + ' ' + o.id); else latexOk(o.grund, wo + ' ' + o.id); }
        if (o.st === 'x' && !K.FEHLER[o.code]) melde('Fehlgriff ohne Code der Bilanz', o.id + ' ' + o.code);
        if (o.st === 'ok' && typeof o.tun !== 'function') melde('Passender Schritt ohne Ausführung', o.id);
        // Fehlgriff beim Addieren: wirklich keine Variable weg
        if (ph === 'anw' && S.methode === 'A' && o.st === 'x') {
          const sg = o.id === 'A+' ? 1 : -1, k = S.eq[0].k.map((c, j) => c * S.fak[0] + sg * S.eq[1].k[j] * S.fak[1]);
          if (k.some((c, j) => c === 0 && (S.eq[0].k[j] || S.eq[1].k[j]))) melde('Addieren als Fehlgriff, eliminiert aber', wo);
        }
      }
      const ok = opt.filter(o => o.st === 'ok');
      if (!ok.length) { melde('Sackgasse: kein passender Schritt', wo + ' ' + ph + ' nach ' + pfad.join(' ')); break; }
      const o = ok[Math.floor(Math.random() * ok.length)];
      gewaehlt[art(o.id)] = (gewaehlt[art(o.id)] || 0) + 1;
      pfad.push(o.id);
      o.tun(S);
    }
    schritte += pfad.length; laengste = Math.max(laengste, pfad.length);
    if (S.phase !== 'ende') continue;
    if (S.kaputt) melde('Weg endet beim falschen Ergebnis', wo + ' ' + pfad.join(' '));
    if (S.verlauf[S.verlauf.length - 1].L !== true) melde('Weg endet nicht mit der Lösungsmenge', wo);
    S.verlauf.forEach(z => latexOk(z.text || z.z || '', wo + ' Weg'));
    if (a.fall === 'eine' && a.art !== 'lage') a.loes.forEach((v, j) => {
      const re = new RegExp('^' + 'xyz'[j] + ' = (.* = )?' + String(v).replace('-', '\\-') + '$');
      if (!S.verlauf.some(z => z.z && re.test(z.z))) melde('Wert einer Variablen fehlt im Weg', wo + ' ' + 'xyz'[j] + ' = ' + v + ' · ' + pfad.join(' '));
    });
    py.push({ gl: a.gl.map(g => [...g.k, g.r]), fall: a.fall, loes: a.fall === 'eine' ? a.loes : a.fall === 'unendlich' ? a.loes.map(([m, q]) => [[m.n, m.d], [q.n, q.d]]) : null, weg: S.verlauf.filter(z => z.z).map(z => z.z), wo: wo + ' ' + pfad.join(' ') });
  }
}
if (K.STATISTIK.widerspruch) melde('Weg endet beim falschen Ergebnis oder in einer Sackgasse (Erzeuger)', K.STATISTIK.widerspruch + '× z.B. ' + K.STATISTIK.beispiel);
// Jede Art von Schritt kommt als passend vor, jeder Fehlgriff wird angeboten
for (const id of ['ME', 'MG', 'MA', 'U', 'O', 'V', 'D', 'E', 'G', 'A+', 'A-', 'L1', 'L2', 'L3', 'Z', 'W', 'P', 'R', 'Feine', 'Fkeine', 'Funendlich'])
  if (!(gewaehlt[id] > 0)) melde('Schritt kommt nie als passend vor', id);
for (const id of ['U:um', 'ME:um', 'MG:um', 'MA:um', 'V:um', 'D:x', 'Ex:x', 'Gx:x', 'A+:x', 'A-:x', 'L1:x', 'L2:x', 'L3:x', 'Zx:x', 'Z:x', 'W:um', 'P:x', 'P:um', 'R:x'])
  if (!(angeboten[id] > 0)) melde('Umweg oder Fehlgriff kommt nie vor', id);
for (const [k, v] of Object.entries(stat)) if (v < N * 0.04) melde('Thema/Fall zu selten', k + ' ' + v);

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

console.log(`${Object.keys(K.THEMEN).length} Themen · ${zahl} Aufgaben · ${py.length} Wege (Ø ${(schritte / py.length).toFixed(1)} Schritte, höchstens ${laengste}) in python3 nachgerechnet`);
console.log('  ' + Object.entries(stat).map(([k, v]) => k + ' ' + v).join(' · '));
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
