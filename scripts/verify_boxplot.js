#!/usr/bin/env node
// Selbsttest der Simulation Boxplot (simulationen/boxplot.html), ohne Browser:
// Der Block zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_boxplot.js         # 3000 Zufallsdatensätze (Pre-Flight)
// Geprüft wird gegen python3 (statistics): Quartile nach 4.3 (Median der Hälften, bei ungeradem n ohne den Median),
// R und QD, Mittelwert, die Plätze in der sortierten Liste (der Wert am Platz ist das Quartil), die vier Teile
// (gleich viele Werte, zusammen mit den Grenzplätzen genau 1…n), die Faustregel 1.5 · QD mit Whiskerenden,
// die Ränge, die Aussagen von Schritt 6 (mindestens drei Viertel ≤ Q3, mindestens die Hälfte ≥ Median),
// dazu die Form der Beispiele, die Eingabe und die Rundung. Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'simulationen', 'boxplot.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { kennzahlen, plaetze, viertel, raenge, form, zaeune, liesWerte, zahl, gerundet, X_MIN, X_MAX, N_MIN, N_MAX };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 3000;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

// Beispiele der Seite: Form, wie im Text versprochen
const BSP = { symmetrisch: [4, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 16], rechtsschief: [2, 3, 3, 4, 4, 5, 5, 6, 7, 9, 12, 17],
  linksschief: [3, 8, 11, 13, 14, 15, 15, 16, 16, 17, 17, 18] };
for (const [f, d] of Object.entries(BSP)) if (K.form(K.kennzahlen(d)) !== f) melde('Form des Beispiels', f + ' → ' + K.form(K.kennzahlen(d)));
if (!K.zaeune([6, 7, 8, 8, 9, 9, 10, 10, 11, 12, 19]).aus.includes(19)) melde('Beispiel «mit Ausreisser» ohne Ausreisser', '19');
if (K.form(K.kennzahlen([7, 7, 7, 7])) !== 'keine') melde('Form ohne Streuung', '7,7,7,7');
// Beispielknöpfe in der Seite: gültige Eingaben
for (const m of html.matchAll(/data-werte="([^"]+)"/g)) if (K.liesWerte(m[1]).fehler) melde('Beispielknopf ungültig', m[1]);

const faelle = [];
const bsp = [[3, 5, 6, 7, 8, 8, 9, 11, 12, 15], ...Object.values(BSP), [6, 7, 8, 8, 9, 9, 10, 10, 11, 12, 19], [2, 3, 3, 4, 5, 15, 16, 16, 17, 18], [0, 0, 20, 20], [5, 5, 5, 5, 5]];
for (let i = 0; i < N + bsp.length; i++) {
  const n = K.N_MIN + Math.floor(Math.random() * (K.N_MAX - K.N_MIN + 1));
  const d = i < bsp.length ? bsp[i] : Array.from({ length: n }, () => K.X_MIN + Math.floor(Math.random() * (K.X_MAX - K.X_MIN + 1)));
  const k = K.kennzahlen(d), z = K.zaeune(d), v = K.viertel(d.length), rg = K.raenge(d);
  for (const x of [k.m, k.q0, k.q1, k.q2, k.q3, k.q4, k.R, k.QD]) if (!Number.isFinite(x)) melde('Kennzahl nicht endlich', JSON.stringify(d));
  // vier Teile gleich gross, zusammen mit den Grenzen genau 1…n, jeder Teil zwischen seinen Grenzplätzen
  const alle = [...v.teile.flat(), ...v.grenze].sort((a, b) => a - b);
  if (alle.length !== d.length || alle.some((r, j) => r !== j + 1)) melde('Teile decken 1…n nicht genau ab', JSON.stringify(d));
  if (new Set(v.teile.map(t => t.length)).size !== 1) melde('Teile ungleich gross', d.length + ': ' + JSON.stringify(v.teile));
  const g = [0, ...k.p.slice(1, 4), d.length + 1];
  v.teile.forEach((t, j) => t.forEach(r => { if (!(r > g[j] && r < g[j + 1])) melde('Platz im falschen Teil', d.length + ': ' + r + ' in Teil ' + (j + 1)); }));
  // Ränge: eine Permutation, die die Liste sortiert
  const nachRang = []; d.forEach((x, j) => { nachRang[rg[j] - 1] = x; });
  if (new Set(rg).size !== d.length || nachRang.some((x, j) => x !== k.s[j])) melde('Ränge sortieren nicht', JSON.stringify(d));
  faelle.push({ d, m: k.m, q: [k.q0, k.q1, k.q2, k.q3, k.q4], p: k.p, R: k.R, QD: k.QD, z: { u: z.u, o: z.o, aus: z.aus, wu: z.wu, wo: z.wo } });
}
// Eingabe
for (const [t, ok] of [['1, 2, 3, 4', true], ['1 2;3,4  5', true], ['1, 2, 3', false], ['1, 2, 3.5, 4', false], ['1, 2, 3, 21', false], ['1, -2, 3, 4', false],
  [Array(16).fill(3).join(','), false], [Array(15).fill(3).join(' '), true], ['', false]]) {
  const r = K.liesWerte(t);
  if (!r.fehler !== ok) melde('Eingabe', JSON.stringify(t) + ' → ' + JSON.stringify(r));
}
// Rundung
for (const [x, t, r] of [[8.4166, '8.42', true], [10, '10', false], [2.5, '2.5', false], [-1.5, '-1.5', false], [1 / 3, '0.33', true]]) {
  if (K.zahl(x) !== t || K.gerundet(x) !== r) melde('Rundung', x + ' → ' + K.zahl(x) + ' ' + K.gerundet(x));
}
const skript = `
import sys, json, statistics as st
fehler = []
def tukey(a):
    s = sorted(a); n = len(s); m = n // 2
    unten, oben = (s[:m], s[m+1:]) if n % 2 else (s[:m], s[m:])
    return [s[0], st.median(unten), st.median(s), st.median(oben), s[-1]]
nah = lambda a, b: abs(a - b) < 1e-9 * max(1, abs(b))
for f in json.load(sys.stdin):
    d = f['d']; s = sorted(d); n = len(d)
    q = tukey(d); QD = q[3] - q[1]
    if any(not nah(a, b) for a, b in zip(f['q'], q)): fehler.append(['python: Quartile weichen ab', str(d) + ' ' + str(f['q']) + ' ' + str(q)])
    if not nah(f['R'], q[4] - q[0]) or not nah(f['QD'], QD): fehler.append(['python: R oder QD weicht ab', str(d)])
    if not nah(f['m'], st.mean(d)): fehler.append(['python: Mittelwert weicht ab', str(d)])
    for p, w in zip(f['p'], q):
        lo, hi = int(p // 1), int(-(-p // 1))
        if not nah((s[lo-1] + s[hi-1]) / 2, w) or (p != lo and p != lo + 0.5): fehler.append(['python: Platz passt nicht zum Quartil', str(d) + ' ' + str(f['p'])])
    u, o = q[1] - 1.5 * QD, q[3] + 1.5 * QD
    aus = sorted(x for x in d if x < u or x > o); drin = [x for x in d if u <= x <= o]
    z = f['z']
    if not nah(z['u'], u) or not nah(z['o'], o) or z['aus'] != aus or z['wu'] != min(drin) or z['wo'] != max(drin):
        fehler.append(['python: Faustregel weicht ab', str(d) + ' ' + str(z)])
    if sum(x <= q[3] for x in d) < 0.75 * n or sum(x >= q[1] for x in d) < 0.75 * n: fehler.append(['Aussage «drei Viertel» falsch', str(d)])
    if sum(x >= q[2] for x in d) < n / 2 or sum(x <= q[2] for x in d) < n / 2: fehler.append(['Aussage «mindestens die Hälfte» falsch', str(d)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(faelle), encoding: 'utf8', maxBuffer: 1 << 26 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);
console.log(`${faelle.length} Datensätze · Gegenrechnung in python3 (statistics)`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
