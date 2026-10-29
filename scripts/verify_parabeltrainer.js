#!/usr/bin/env node
// Selbsttest des Geraden- und Parabeltrainers (werkzeuge/parabeltrainer.html), ohne Browser:
// Der Block zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_parabeltrainer.js        # 2000 Zufallsaufgaben je Form und Modus (Pre-Flight)
// Geprüft wird gegen python3 (fractions): Scheitelform, allgemeine Form und Produktform beschreiben dieselbe
// Funktion (b = −2au, c = au² + v, Nullstellen aus −v/a), jeder Zielpunkt eines Zeichenschritts liegt exakt auf
// dem Graphen, die Rückwege mkParABC und mkParRoots treffen ihre Eingabe. In JS: Grenzen des Erzeugers, und kein
// Schritttext enthält undefined, NaN oder ein Dezimalkomma. Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'parabeltrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { Q, mkLin, mkPar, mkParRoots, mkParABC, rnd, drawSteps, readSteps, fnTeX,' +
  ' setze: (f, fo) => { F = f; form = fo; } };', ctx);   // F und form stehen als let im Kern
const K = ctx.K;
const N = +process.argv[2] || 2000;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
const q = x => [x.n, x.d];
const name = F => F.type === 'lin' ? `y = ${F.m.n}/${F.m.d} x + ${F.q.n}/${F.q.d}` : `a=${F.a.n}/${F.a.d} u=${F.u.n}/${F.u.d} v=${F.v.n}/${F.v.d}`;

function texte(S, F, wo) {
  for (const s of S) {
    const t = [s.t, s.how, s.sol ? s.sol() : ''].join(' ');
    if (/undefined|NaN|Infinity|\[object/.test(t)) melde(`Schritttext kaputt (${wo})`, name(F) + ' · ' + s.t);
    if (/\d\{,\}\d|\d,\d/.test(t.replace(/\\[a-z]+/g, ''))) melde(`Dezimalkomma im Schritttext (${wo})`, name(F) + ' · ' + s.t);
  }
}

const faelle = [];
for (const form of ['lin', 'sf', 'pf', 'af']) for (const lesen of [false, true]) for (let i = 0; i < N; i++) {
  const F = K.rnd(form, lesen);
  const fall = { form, lesen, typ: F.type, pkt: [] };
  if (F.type === 'lin') { fall.m = q(F.m); fall.q = q(F.q); }
  else {
    if (F.a.isZero()) melde('a = 0', name(F));
    Object.assign(fall, { a: q(F.a), u: q(F.u), v: q(F.v), b: q(F.b), c: q(F.c), art: F.roots.kind });
    if (F.roots.x1 instanceof K.Q) { fall.x1 = q(F.roots.x1); fall.x2 = q(F.roots.x2); }
    if (F.roots.kind === 'irr') { fall.r = q(F.roots.r); fall.x1v = F.roots.x1v; fall.x2v = F.roots.x2v; }
    if (form === 'pf') {
      if (!['two', 'double'].includes(F.roots.kind)) melde('Produktform ohne rationale Nullstellen', name(F));
      if (Math.abs(F.v.v) > 8 || Math.abs(F.c.v) > 12) melde('Produktform ausserhalb der Grenzen', name(F));
    }
    if (form === 'af' && lesen && !F.c.isInt()) melde('Ablesen: c nicht ganzzahlig', name(F));
    if (!K.fnTeX(F, form)) melde('keine Gleichung in der gegebenen Form', form + ' ' + name(F));
  }
  // Zeichnen: jeder Zielpunkt liegt auf dem Graphen
  K.setze(F, form);
  const S = K.drawSteps();
  for (const s of S) if (s.kind === 'point') {
    const [x, y] = s.target;
    const fx = F.type === 'lin' ? F.m.mul(x).add(F.q) : F.fQ(x);
    if (!fx.eq(y)) melde('Zielpunkt nicht auf dem Graphen', `${form} ${name(F)} · ${s.t}: (${x.n}/${x.d} | ${y.n}/${y.d})`);
    fall.pkt.push([q(x), q(y)]);
  }
  texte(S, F, 'Zeichnen');
  texte(K.readSteps(), F, 'Ablesen');
  faelle.push(fall);
}
// Rückwege: eigene Eingaben in allgemeiner Form und Produktform
const rueck = [];
const zufallQ = () => new K.Q(Math.floor(Math.random() * 21) - 10, 1 + Math.floor(Math.random() * 4));
for (let i = 0; i < N; i++) {
  let a = zufallQ(); if (a.isZero()) a = new K.Q(1);
  const b = zufallQ(), c = zufallQ(), F = K.mkParABC(a, b, c);
  if (!F.b.eq(b) || !F.c.eq(c) || !F.a.eq(a)) melde('mkParABC trifft a, b, c nicht', `${a.n}/${a.d} ${b.n}/${b.d} ${c.n}/${c.d}`);
  const x1 = zufallQ(), x2 = zufallQ(), G = K.mkParRoots(a, x1, x2);
  const [k, g] = x1.v <= x2.v ? [x1, x2] : [x2, x1];
  if (!G.roots.x1.eq(k) || !G.roots.x2.eq(g) || !G.fQ(x1).isZero() || !G.fQ(x2).isZero()) melde('mkParRoots trifft die Nullstellen nicht', `${x1.n}/${x1.d} ${x2.n}/${x2.d}`);
  rueck.push({ a: q(a), x1: q(x1), x2: q(x2), u: q(G.u), v: q(G.v), b: q(G.b), c: q(G.c) });
}

const skript = `
import sys, json, math
from fractions import Fraction as Fr
fehler = []
d = json.load(sys.stdin)
Q = lambda p: Fr(p[0], p[1])
for f in d['faelle']:
    if f['typ'] == 'lin':
        m, q = Q(f['m']), Q(f['q'])
        for x, y in f['pkt']:
            if m * Q(x) + q != Q(y): fehler.append(['python: Punkt nicht auf der Geraden', str(f)])
        continue
    a, u, v = Q(f['a']), Q(f['u']), Q(f['v'])
    if a == 0: fehler.append(['python: a = 0', str(f)]); continue
    if Q(f['b']) != -2 * a * u or Q(f['c']) != a * u * u + v: fehler.append(['python: b oder c weicht ab', str(f)])
    fn = lambda x: a * (x - u) ** 2 + v
    for x, y in f['pkt']:
        if fn(Q(x)) != Q(y): fehler.append(['python: Punkt nicht auf der Parabel', str(f)])
    r = -v / a
    art = 'none' if r < 0 else 'double' if r == 0 else None
    if art is None:
        wn, wd = math.isqrt(r.numerator), math.isqrt(r.denominator)
        art = 'two' if wn * wn == r.numerator and wd * wd == r.denominator else 'irr'
    if art != f['art']: fehler.append(['python: Art der Nullstellen weicht ab', str(f) + ' erwartet ' + art])
    elif art in ('two', 'double'):
        x1, x2 = Q(f['x1']), Q(f['x2'])
        if fn(x1) != 0 or fn(x2) != 0 or x1 > x2: fehler.append(['python: Nullstellen falsch', str(f)])
        if art == 'two' and x1 == x2: fehler.append(['python: zwei gleiche Nullstellen', str(f)])
        if x1 + x2 != 2 * u: fehler.append(['python: Scheitel nicht in der Mitte', str(f)])
    elif art == 'irr':
        w = math.sqrt(r)
        if abs(f['x1v'] - (float(u) - w)) > 1e-9 or abs(f['x2v'] - (float(u) + w)) > 1e-9: fehler.append(['python: irrationale Nullstellen falsch', str(f)])
for g in d['rueck']:
    a, x1, x2 = Q(g['a']), Q(g['x1']), Q(g['x2'])
    u, v, b, c = Q(g['u']), Q(g['v']), Q(g['b']), Q(g['c'])
    if u != (x1 + x2) / 2 or v != a * (u - x1) * (u - x2): fehler.append(['python: mkParRoots Scheitel falsch', str(g)])
    if b != -a * (x1 + x2) or c != a * x1 * x2: fehler.append(['python: mkParRoots b, c falsch', str(g)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify({ faelle, rueck }), encoding: 'utf8', maxBuffer: 1 << 27 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 600));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);
const pkt = faelle.reduce((s, f) => s + f.pkt.length, 0);
console.log(`${faelle.length} Aufgaben (4 Formen × Zeichnen/Ablesen), ${pkt} Zielpunkte, ${rueck.length} Rückwege · Gegenrechnung in python3 (fractions)`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
