#!/usr/bin/env node
// Selbsttest der Simulation Standardabweichung (simulationen/standardabweichung.html), ohne Browser:
// Der Block zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_standardabweichung.js         # 3000 Zufallsdatensätze (Pre-Flight)
// Geprüft wird gegen python3 (statistics): Mittelwert, Summe der Quadrate, s (n − 1) und σ (n), Quartile nach 4.3
// (Median der Hälften, bei ungeradem n ohne den Median), R und QD, dazu der Vergleich ohne den äussersten Wert
// und die Rundung (zahl, gerundet). Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'simulationen', 'standardabweichung.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { kennzahlen, ohneAeussersten, zahl, gerundet, X_MIN, X_MAX, N_MIN, N_MAX };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 3000;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
const faelle = [];
const bsp = [[9, 10, 10, 11, 10], [6, 8, 10, 12, 14], [2, 6, 10, 14, 18], [3, 4, 5, 16, 17, 18], [8, 9, 10, 10, 11, 12, 19], [5, 5], [0, 20], [7, 7, 7, 7]];
for (let i = 0; i < N + bsp.length; i++) {
  const n = K.N_MIN + Math.floor(Math.random() * (K.N_MAX - K.N_MIN + 1));
  const d = i < bsp.length ? bsp[i] : Array.from({ length: n }, () => K.X_MIN + Math.floor(Math.random() * (K.X_MAX - K.X_MIN + 1)));
  const s = K.kennzahlen(d, 's'), g = K.kennzahlen(d, 'sigma'), o = K.ohneAeussersten(d, 's');
  for (const v of [s.m, s.ss, s.s, g.s, s.q1, s.q3, s.R, s.QD]) if (!Number.isFinite(v)) melde('Kennzahl nicht endlich', JSON.stringify(d));
  faelle.push({ d, m: s.m, ss: s.ss, s: s.s, sigma: g.s, q: [s.q0, s.q1, s.q2, s.q3, s.q4], R: s.R, QD: s.QD,
    ohne: o && { wert: o.wert, R: o.nachher.R, QD: o.nachher.QD, s: o.nachher.s } });
}
// Rundung
for (const [x, t, r] of [[3.16227, '3.16', true], [10, '10', false], [2.5, '2.5', false], [-0.001, '0', true], [1 / 3, '0.33', true]]) {
  if (K.zahl(x) !== t || K.gerundet(x) !== r) melde('Rundung', x + ' → ' + K.zahl(x) + ' ' + K.gerundet(x));
}
if (/\d,\d/.test(K.zahl(2.5))) melde('Dezimalkomma', K.zahl(2.5));
const skript = `
import sys, json, statistics as st
fehler = []
def tukey(a):
    s = sorted(a); n = len(s); m = n // 2
    unten, oben = (s[:m], s[m+1:]) if n % 2 else (s[:m], s[m:])
    return [s[0], st.median(unten), st.median(s), st.median(oben), s[-1]]
nah = lambda a, b: abs(a - b) < 1e-9 * max(1, abs(b))
for f in json.load(sys.stdin):
    d = f['d']
    q = tukey(d)
    soll = {'m': st.mean(d), 's': st.stdev(d), 'sigma': st.pstdev(d), 'R': q[4] - q[0], 'QD': q[3] - q[1]}
    soll['ss'] = sum((x - soll['m']) ** 2 for x in d)
    for k, v in soll.items():
        if not nah(f[k], v): fehler.append(['python: ' + k + ' weicht ab', str(d) + ' Werkzeug=' + repr(f[k]) + ' python=' + repr(v)])
    if any(not nah(a, b) for a, b in zip(f['q'], q)): fehler.append(['python: Quartile weichen ab', str(d) + ' ' + str(f['q']) + ' ' + str(q)])
    if len(d) >= 4:
        med = st.median(d); j = max(range(len(d)), key=lambda i: (abs(d[i] - med), -i))
        rest = d[:j] + d[j+1:]; qr = tukey(rest)
        o = f['ohne']
        if not o or o['wert'] != d[j] or not nah(o['R'], qr[4] - qr[0]) or not nah(o['QD'], qr[3] - qr[1]) or not nah(o['s'], st.stdev(rest)):
            fehler.append(['python: Vergleich ohne äussersten Wert weicht ab', str(d) + ' ' + str(o)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(faelle), encoding: 'utf8', maxBuffer: 1 << 26 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);
console.log(`${faelle.length} Datensätze · Gegenrechnung in python3 (statistics)`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
