#!/usr/bin/env node
// Selbsttest der Präsentation Sinussatz und Cosinussatz (praesentationen/sinussatz-cosinussatz.html), ohne Browser:
// Der Block zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_sinussatz-cosinussatz.js      # alle ganzzahligen Angaben der Regler (Pre-Flight)
// Für jeden der sechs Fälle (SSS, SWS, WSW, SWW, SsW, sSw) jede Kombination der Reglerwerte, bei mehr als
// 20000 eine Zufallsauswahl. Gegenrechnung in python3, unabhängig vom Sinus- und Cosinussatz: Das Dreieck wird aus
// den Angaben konstruiert (Koordinaten, Schnitt von Strahl und Strahl oder Strahl und Kreis), Seiten und Winkel
// werden daraus gemessen. Verglichen werden: ob es ein Dreieck gibt, alle sechs Stücke, bei sSw beide Lösungen.
// In JS: die Ecken aus punkte() haben die berechneten Seitenlängen, der Rechenweg nennt die berechneten Werte und
// enthält kein undefined, NaN oder Dezimalkomma. Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'praesentationen', 'sinussatz-cosinussatz.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { FALL, loese, punkte, rechnung, f, deg };', ctx);
const K = ctx.K;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

// Zufall mit festem Startwert, damit ein Befund wiederholbar ist
let s = 20261123;
const zufall = () => ((s = (s * 1103515245 + 12345) % 2147483648) / 2147483648);

const faelle = [];
for (const [fl, F] of Object.entries(K.FALL)) {
  const bereiche = F.geg.map(([k, , lo, hi]) => [k, lo, hi]);
  const anzahl = bereiche.reduce((p, [, lo, hi]) => p * (hi - lo + 1), 1);
  const kombis = [];
  if (anzahl <= 20000) {
    const rek = (i, v) => { if (i === bereiche.length) { kombis.push({ ...v }); return; }
      const [k, lo, hi] = bereiche[i]; for (let x = lo; x <= hi; x++) { v[k] = x; rek(i + 1, v); } };
    rek(0, {});
  } else for (let i = 0; i < 20000; i++) {
    const v = {}; for (const [k, lo, hi] of bereiche) v[k] = lo + Math.floor(zufall() * (hi - lo + 1)); kombis.push(v);
  }
  for (const v of kombis) {
    const R = K.loese(fl, v);
    const fall = { fl, v, ok: R.ok };
    if (R.ok) {
      for (const k of ['a', 'b', 'c', 'al', 'be', 'ga', 'c2', 'be2', 'ga2']) if (k in R) fall[k] = R[k];
      for (const k of Object.keys(v)) {
        const soll = k.length > 1 ? v[k] * Math.PI / 180 : v[k];
        if (Math.abs(R[k] - soll) > 1e-12) melde('Angabe verändert', fl + ' ' + JSON.stringify(v) + ' ' + k);
      }
      // Ecken der Figur: Seitenlängen wie berechnet
      const P = K.punkte(fl, R), d = (X, Y) => Math.hypot(X[0] - Y[0], X[1] - Y[1]);
      for (const [k, X, Y] of [['a', P.B, P.C], ['b', P.C, P.A], ['c', P.A, P.B]])
        if (Math.abs(d(X, Y) - R[k]) > 1e-9) melde('Figur: Seitenlänge weicht ab', fl + ' ' + JSON.stringify(v) + ' ' + k);
      // Rechenweg nennt die berechneten Werte
      const Q = K.rechnung(fl, v, R), text = Q.Z.join(' ');
      if (/undefined|NaN|Infinity/.test(text)) melde('Rechenweg kaputt', fl + ' ' + JSON.stringify(v));
      if (/\d,\d/.test(text)) melde('Dezimalkomma im Rechenweg', fl + ' ' + JSON.stringify(v));
      if (Q.gibt.length !== 3) melde('nicht drei gesuchte Stücke', fl);
      for (const k of Q.gibt) {
        const wert = k.length > 1 ? K.f(K.deg(R[k]), 1) : K.f(R[k], 2);
        if (!text.includes(wert)) melde('Rechenweg nennt einen berechneten Wert nicht', fl + ' ' + JSON.stringify(v) + ' ' + k + ' = ' + wert);
      }
      if (fl === 'sSw') for (const [k, n] of [['be2', 1], ['ga2', 1], ['c2', 2]]) {
        const wert = n === 1 ? K.f(K.deg(R[k]), 1) : K.f(R[k], 2);
        if (!text.includes(wert)) melde('Rechenweg nennt die zweite Lösung nicht', fl + ' ' + JSON.stringify(v) + ' ' + k);
      }
    } else if (!R.msg) melde('kein Dreieck, aber keine Meldung', fl + ' ' + JSON.stringify(v));
    faelle.push(fall);
  }
}

const py = String.raw`
import json, math, sys
faelle = json.load(sys.stdin)
D = math.pi / 180
fehler = []
def winkel(V, P, Q):
    u = (P[0] - V[0], P[1] - V[1]); w = (Q[0] - V[0], Q[1] - V[1])
    return math.acos(max(-1, min(1, (u[0]*w[0] + u[1]*w[1]) / (math.hypot(*u) * math.hypot(*w)))))
def strahlen(P, wp, Q, wq):
    # Schnitt der Strahlen P + s(cos wp, sin wp) und Q + t(cos wq, sin wq)
    dp = (math.cos(wp), math.sin(wp)); dq = (math.cos(wq), math.sin(wq))
    det = dp[0] * (-dq[1]) - dp[1] * (-dq[0])
    s = ((Q[0] - P[0]) * (-dq[1]) - (Q[1] - P[1]) * (-dq[0])) / det
    return (P[0] + s * dp[0], P[1] + s * dp[1])
def stuecke(A, B, C):
    return dict(a=math.dist(B, C), b=math.dist(C, A), c=math.dist(A, B),
                al=winkel(A, B, C), be=winkel(B, C, A), ga=winkel(C, A, B))
def strahl_kreis(al, M, r):
    # Punkte t(cos al, sin al), t > 0, im Abstand r von M — alle positiven t, absteigend
    p = -2 * (M[0] * math.cos(al) + M[1] * math.sin(al)); q = M[0]**2 + M[1]**2 - r * r
    disk = p * p / 4 - q
    if disk < -1e-9: return []
    if abs(disk) < 1e-9: return [-p / 2] if -p / 2 > 0 else []
    return sorted([t for t in (-p / 2 + math.sqrt(disk), -p / 2 - math.sqrt(disk)) if t > 1e-12], reverse=True)
for F in faelle:
    fl, v = F['fl'], F['v']
    erg = []      # Liste der Dreiecke (dict der sechs Stücke)
    if fl == 'SSS':
        a, b, c = v['a'], v['b'], v['c']
        if a + b > c and a + c > b and b + c > a:
            x = (b*b - a*a + c*c) / (2*c)          # C aus den zwei Kreisen um A und B
            erg = [stuecke((0, 0), (c, 0), (x, math.sqrt(b*b - x*x)))]
    elif fl == 'SWS':
        b, c, al = v['b'], v['c'], v['al'] * D
        erg = [stuecke((0, 0), (c, 0), (b * math.cos(al), b * math.sin(al)))]
    elif fl == 'WSW':
        if v['al'] + v['be'] < 170:
            c = v['c']; C = strahlen((0, 0), v['al'] * D, (c, 0), math.pi - v['be'] * D)
            erg = [stuecke((0, 0), (c, 0), C)]
    elif fl == 'SWW':
        if v['al'] + v['be'] < 170:
            a = v['a']; ga = math.pi - v['al'] * D - v['be'] * D
            A = strahlen((0, 0), v['be'] * D, (a, 0), math.pi - ga)      # B = (0,0), C = (a,0)
            erg = [stuecke(A, (0, 0), (a, 0))]
    else:  # SsW und sSw: A = (0,0), C = (b,0), B auf dem Strahl von A unter alpha mit |CB| = a
        a, b, al = v['a'], v['b'], v['al'] * D
        ts = strahl_kreis(al, (b, 0), a)
        if fl == 'SsW' and a > b: erg = [stuecke((0, 0), (t * math.cos(al), t * math.sin(al)), (b, 0)) for t in ts]
        if fl == 'sSw' and a < b and len(ts) == 2: erg = [stuecke((0, 0), (t * math.cos(al), t * math.sin(al)), (b, 0)) for t in ts]
    if bool(erg) != F['ok']:
        fehler.append(['python: Dreieck ja/nein weicht ab', fl + ' ' + json.dumps(v) + ' JS ' + str(F['ok']) + ', python ' + str(len(erg))])
        continue
    if not erg: continue
    if fl == 'SsW' and len(erg) != 1: fehler.append(['python: SsW mit mehr als einer Lösung', fl + ' ' + json.dumps(v)])
    for k in ('a', 'b', 'c', 'al', 'be', 'ga'):
        if abs(F[k] - erg[0][k]) > 1e-7: fehler.append(['python: ' + k + ' weicht ab', fl + ' ' + json.dumps(v) + ' JS %.6f python %.6f' % (F[k], erg[0][k])])
    if abs(F['al'] + F['be'] + F['ga'] - math.pi) > 1e-9: fehler.append(['Winkelsumme nicht 180°', fl + ' ' + json.dumps(v)])
    if fl == 'sSw':
        for k, kp in (('c2', 'c'), ('be2', 'be'), ('ga2', 'ga')):
            if abs(F[k] - erg[1][kp]) > 1e-7: fehler.append(['python: zweite Lösung ' + k + ' weicht ab', fl + ' ' + json.dumps(v)])
json.dump(fehler, sys.stdout)
`;
const r = spawnSync('python3', ['-c', py], { input: JSON.stringify(faelle), encoding: 'utf8', maxBuffer: 1 << 28 });
if (r.status !== 0) { console.log('python3 fehlgeschlagen:\n' + r.stderr); process.exit(1); }
for (const [art, info] of JSON.parse(r.stdout)) melde(art, info);

const proFall = {};
for (const F of faelle) { const p = proFall[F.fl] || (proFall[F.fl] = [0, 0]); p[0]++; if (F.ok) p[1]++; }
console.log('Sinussatz und Cosinussatz: ' + Object.entries(proFall).map(([fl, [n, ok]]) => `${fl} ${n} (${ok} Dreiecke)`).join(', '));
if (!befunde.size) { console.log('alle Fälle stimmen mit python3 überein'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`[${n}×] ${art}: ${info}`);
process.exit(1);
