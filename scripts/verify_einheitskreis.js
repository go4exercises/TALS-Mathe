#!/usr/bin/env node
// Selbsttest der Präsentation Einheitskreis (praesentationen/einheitskreis.html), ohne Browser:
// Der Block zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_einheitskreis.js      # Pre-Flight
// Geprüft wird gegen python3, auf einem anderen Weg als im Kern:
//   - loesungen(fn, v) für jeden Wert der Regler (sin/cos −1…1 in 0.05, tan −3…3 in 0.1): python3 sucht alle Winkel
//     in [0°, 360°) mit fn(φ) = v durch Abtasten und Halbieren, nicht mit arcsin/arccos/arctan.
//   - exakt(g) für jeden ganzzahligen Winkel 0°…360°: der TeX-Text (\dfrac, \sqrt) wird in python3 ausgewertet und
//     mit sin/cos/tan verglichen; nur die Vielfachen von 30° und 45° sind «speziell».
//   - piTeX(g) und piText(g): der Wert des Bruchs ist g · π / 180.
//   - BSP: Die Beispiele mit Gleichung nennen im Rechenweg genau die Lösungen, die python3 findet.
// In JS: Rechenwege und Symmetrie-Texte ohne undefined, NaN oder Dezimalkomma. Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'praesentationen', 'einheitskreis.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { loesungen, exakt, piTeX, piText, BSP, UMK, f, deg, gT, g1 };', ctx);
const K = ctx.K;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
const kaputt = (t, wo) => {
  if (/undefined|NaN|Infinity/.test(t)) melde('Text kaputt', wo + ': ' + t.slice(0, 80));
  if (/\d,\d/.test(t)) melde('Dezimalkomma', wo + ': ' + t.slice(0, 80));
};

const umkehr = [];
for (const fn of ['sin', 'cos', 'tan']) {
  const [lo, hi, st] = fn === 'tan' ? [-3, 3, 0.1] : [-1, 1, 0.05];
  for (let i = 0; lo + i * st <= hi + 1e-9; i++) {
    const v = +(lo + i * st).toFixed(2), L = K.loesungen(fn, v);
    const winkel = (L.eins ? [L.a1] : [L.a1, L.a2]).map(K.deg);
    umkehr.push({ fn, v, winkel });
    // Texte der Folie «Vom Wert zum Winkel» in Grad und im Bogenmass
    for (const b of [false, true]) {
      const W = b ? w => K.f(w, 3) : K.gT;
      if (!L.eins) kaputt(K.UMK[fn].zwei(L, W, b), `UMK ${fn} ${v}`);
    }
  }
}
const spezial = [];
for (let g = 0; g <= 360; g++) {
  const e = K.exakt(g);
  spezial.push({ g, e: e && { sin: e.sin, cos: e.cos, tan: e.tan }, pi: K.piTeX(g), piText: K.piText(g) });
}
const beispiele = [];
K.BSP.forEach((B, i) => {
  if (!B.fn) { B.z().forEach(z => kaputt(z, 'BSP ' + i)); return; }
  const L = K.loesungen(B.fn, B.v), Z = B.z(L);
  Z.forEach(z => kaputt(z, 'BSP ' + i));
  beispiele.push({ i, fn: B.fn, v: B.v, rad: !!B.W, text: Z.join(' ') });
});

const py = String.raw`
import json, math, re, sys
d = json.load(sys.stdin)
fehler = []
F = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}
def loese(fn, v):
    # alle Winkel in [0, 360) mit fn(phi) = v: abtasten in 0.1°, Vorzeichenwechsel halbieren, Berührpunkte über Minimum
    g = lambda x: F[fn](math.radians(x)) - v
    gef = []
    n = 3600
    for k in range(n):
        a, b = k * 0.1, (k + 1) * 0.1
        ga, gb = g(a), g(b)
        if fn == 'tan' and (abs(a % 180 - 90) < 0.11 or abs(b % 180 - 90) < 0.11):
            if abs(ga) < 1e-12: gef.append(a)
            continue
        if ga == 0: gef.append(a)
        elif ga * gb < 0:
            for _ in range(80):
                m = (a + b) / 2
                if g(a) * g(m) <= 0: b = m
                else: a = m
            gef.append((a + b) / 2)
    if fn != 'tan' and abs(abs(v) - 1) < 1e-9:   # Berührpunkt: kein Vorzeichenwechsel
        gef = [ (90 if v > 0 else 270) if fn == 'sin' else (0 if v > 0 else 180) ]
    out = []
    for x in sorted(gef):
        if not out or abs(x - out[-1]) > 1e-6: out.append(x % 360)
    return sorted(set(round(x, 6) for x in out))
for u in d['umkehr']:
    soll = loese(u['fn'], u['v'])
    ist = sorted(round(w % 360, 6) for w in u['winkel'])
    if len(soll) != len(ist) or any(abs(a - b) > 1e-5 and abs(abs(a - b) - 360) > 1e-5 for a, b in zip(soll, ist)):
        fehler.append(['python: Lösungen weichen ab', '%s φ = %s: JS %s, python %s' % (u['fn'], u['v'], ist, soll)])
def atom(s):
    if s.startswith('\\sqrt{'): return math.sqrt(int(s[6:-1]))
    if s.endswith('\\pi'): return (float(s[:-3]) if s[:-3] else 1.0) * math.pi
    return float(s)
def wert(tex):
    # Formen aus exakt() und piTeX(): [-]Atom oder [-]\dfrac{Atom}{Zahl}; Atom = Zahl, \sqrt{n}, [n]\pi
    if tex is None or 'nicht definiert' in tex: return None
    neg = tex.startswith('-'); t = tex[1:] if neg else tex
    m = re.fullmatch(r'\\dfrac\{(.*)\}\{(\d+)\}', t)
    v = atom(m.group(1)) / int(m.group(2)) if m else atom(t)
    return -v if neg else v
def wert_text(s):   # piText: «nπ/d», «π», «2π»
    z, _, n = s.partition('/'); return (float(z[:-1]) if z[:-1] else 1.0) * math.pi / (float(n) if n else 1.0)
for s in d['spezial']:
    g = s['g']; ist_spez = g % 30 == 0 or g % 45 == 0
    if (s['e'] is not None) != ist_spez:
        fehler.append(['exakt: speziell ja/nein falsch', str(g)]); continue
    if s['e']:
        for fn in ('sin', 'cos', 'tan'):
            w = wert(s['e'][fn]); r = math.radians(g)
            if fn == 'tan' and abs(math.cos(r)) < 1e-9:
                if w is not None: fehler.append(['exakt: tan sollte nicht definiert sein', str(g)])
                continue
            if w is None or abs(w - F[fn](r)) > 1e-9:
                fehler.append(['exakt: Wert falsch', '%s %d° = %s' % (fn, g, s['e'][fn])])
    if s['pi'] is not None:
        if abs(wert(s['pi']) - math.radians(g)) > 1e-9: fehler.append(['piTeX falsch', '%d° = %s' % (g, s['pi'])])
        if s['piText'] != '0' and abs(wert_text(s['piText']) - math.radians(g)) > 1e-9:
            fehler.append(['piText falsch', '%d° = %s' % (g, s['piText'])])
for b in d['beispiele']:
    for x in loese(b['fn'], b['v']):
        s = [('%.3f' % math.radians(x))] if b['rad'] else ['%.1f^\\circ' % x] + (['%d^\\circ' % round(x)] if abs(x - round(x)) < 1e-9 else [])
        if not any(z in b['text'] for z in s): fehler.append(['Beispiel nennt eine Lösung nicht', 'BSP %d: %s fehlt' % (b['i'], s[0])])
json.dump(fehler, sys.stdout)
`;
const r = spawnSync('python3', ['-c', py], { input: JSON.stringify({ umkehr, spezial, beispiele }), encoding: 'utf8' });
if (r.status !== 0) { console.log('python3 fehlgeschlagen:\n' + r.stderr); process.exit(1); }
for (const [art, info] of JSON.parse(r.stdout)) melde(art, info);
console.log(`Einheitskreis: ${umkehr.length} Werte umgekehrt, ${spezial.filter(s => s.e).length} spezielle Winkel, ${beispiele.length} Beispiele · Gegenrechnung in python3`);
if (!befunde.size) { console.log('alles stimmt mit python3 überein'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`[${n}×] ${art}: ${info}`);
process.exit(1);
