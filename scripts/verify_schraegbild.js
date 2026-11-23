#!/usr/bin/env node
// Selbsttest der Schrägbild-Werkstatt (werkzeuge/schraegbild-werkstatt.html), ohne Browser.
//   node scripts/verify_schraegbild.js        # Pre-Flight
// Geladen werden die Blöcke zwischen «KERN:ANFANG»/«KERN:ENDE» (Geometrie, Erkennung, Übungen, Prüfen) und
// «KERN-ZUSATZ:ANFANG»/«KERN-ZUSATZ:ENDE» (Details, Drucken, Striche aus einem Modell) in node:vm, mit Platzhaltern
// für Zeichenblatt und DOM. Geprüft wird:
//   1. Prüfen nimmt die Musterlösung an: Für jede Übung zeichnet strokesFrom() die Vorlage mit Zittern wie von Hand
//      (drei Anläufe mit festem Startwert, an drei Stellen des Blatts), die Erkennung baut daraus einen Körper,
//      checkSchraeg() muss «Richtig» melden. Dasselbe in der Dreitafel mit rissStrokesFrom() und checkRiss().
//   2. Prüfen ist nicht blind: Fehlt in der Zeichnung eine Kante, darf es nicht «Richtig» melden.
//   3. Körper: Für jede Übung und jedes Beispiel (auch die fünf platonischen Körper) rechnet python3 Oberfläche und
//      Volumen nach, einmal aus den Flächen (Newell, Divergenzsatz), einmal mit der Formel des Körpers, und prüft
//      Eulers Polyedersatz E − K + F = 2.
//   4. Details: Die Rechenwege im Dialog enthalten kein undefined, NaN und kein Dezimalkomma.
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');
const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'schraegbild-werkstatt.html'), 'utf8');
const block = (a, e) => { const i = html.indexOf(a), j = html.indexOf(e); if (i < 0 || j < 0) throw new Error('Marke fehlt: ' + a); return html.slice(i, j); };
const kern = block('// ── KERN:ANFANG', '// ── KERN:ENDE');
const zusatz = block('// ── KERN-ZUSATZ:ANFANG', '// ── KERN-ZUSATZ:ENDE');

// Platzhalter für alles, was ausserhalb der Blöcke deklariert ist (Zeilen am Anfang des Seitenskripts)
const prelude = `
const G = 28, SNAP = 0.4, EPS = 1e-6;
const fake = () => ({ textContent: '', innerHTML: '', className: '', disabled: false, value: '', checked: false, open: false, style: {},
  classList: { add(){}, remove(){}, toggle(){} }, setAttribute(){}, addEventListener(){}, show(){}, showModal(){}, close(){},
  querySelectorAll(){ return []; }, appendChild(){}, getContext(){ return null; } });
const ELS = {}; const $ = id => ELS[id] || (ELS[id] = fake());
const document = { querySelectorAll(){ return []; }, createElement(){ return fake(); }, body: fake() };
const window = { addEventListener(){} };
const FONT = () => 'sans-serif';
let DW = 1600, DH = 900, VW = 800, VH = 600;
let inputMode = "schraeg";
const drawings = { schraeg: { strokes: [], history: [], future: [] }, riss: { strokes: [], history: [], future: [] } };
let strokes = [], history = [], future = [];
let current = null, activeId = null;
let penKind = "edge", slantDir = "auto", penOnly = false, showRec = true, depthGrid = false;
let alphaDeg = 45, q = 0.5;
let K = null;
let task = null, targetModel = null, userModel = null, showWhich = "target";
let checkRes = null, showSolution = false;
let lern = { versuche: 0, tipp: 0, loesung: false, richtig: false };
let zoom = 1, pan = [0, 0];
function drawPaper(){} function renderInfo(){} function renderView(){}
function initK(){ K = [40, 30]; }
let seed = 1; Math.random = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
`;
const ctx = {};
vm.createContext(ctx);
vm.runInContext(prelude + kern + '\n' + zusatz + `
;globalThis.T = {
  TASKS, EXAMPLES, PROJ, buildTarget, strokesFrom, rissStrokesFrom, analyseSchraeg, analyseRiss, checkSchraeg, checkRiss, detailsHtml,
  setzen: o => { if ('alphaDeg' in o) alphaDeg = o.alphaDeg; if ('q' in o) q = o.q; if ('projIdx' in o) projIdx = o.projIdx;
    if ('task' in o) task = o.task; if ('targetModel' in o) targetModel = o.targetModel; if ('userModel' in o) userModel = o.userModel;
    if ('strokes' in o) strokes = o.strokes; if ('inputMode' in o) inputMode = o.inputMode; if ('K' in o) K = o.K;
    if ('lastRiss' in o) lastRiss = o.lastRiss; if ('seed' in o) seed = o.seed; },
  ergebnis: () => ({ cls: $("result").className, text: $("result").innerHTML || $("result").textContent }),
};`, ctx);
const T = ctx.T;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
const knapp = s => String(s).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 160);

let pruefungen = 0;
const koerper = [];
for (const t of T.TASKS) {
  if (!t.build) continue;
  const pi = T.PROJ.findIndex(p => p.a === t.a && Math.abs(p.q - t.q) < 1e-9);
  if (pi < 0) { melde('Übung ohne passende Projektion', t.name); continue; }
  T.setzen({ alphaDeg: t.a, q: t.q, projIdx: pi, task: t });
  const M = T.buildTarget(t);
  T.setzen({ targetModel: M });
  // 1. Schrägbild: drei Anläufe an verschiedenen Stellen des Blatts
  for (const [n, sh] of [[1, [-4, -14, 0]], [2, [-20, -6, 0]], [3, [-9, -22, 0]]]) {
    T.setzen({ seed: 1000 * n + t.name.length, inputMode: 'schraeg', lastRiss: null });
    const st = T.strokesFrom(M, sh, false);
    T.setzen({ strokes: st }); T.setzen({ userModel: T.analyseSchraeg() }); T.checkSchraeg(); pruefungen++;
    const r = T.ergebnis();
    if (r.cls !== 'ok') melde('Schrägbild: Musterlösung nicht angenommen', `${t.name}, Anlauf ${n}: ${knapp(r.text)}`);
    // 2. eine Kante weglassen (die längste sichtbare)
    if (n === 1) {
      const lang = st.map((s, i) => [i, Math.hypot(s.pts[0][0] - s.pts.at(-1)[0], s.pts[0][1] - s.pts.at(-1)[1]), s.kind])
        .filter(x => x[2] === 'edge').sort((a, b) => b[1] - a[1])[0];
      T.setzen({ strokes: st.filter((s, i) => i !== lang[0]) }); T.setzen({ userModel: T.analyseSchraeg() }); T.checkSchraeg(); pruefungen++;
      if (T.ergebnis().cls === 'ok') melde('Schrägbild: Zeichnung mit fehlender Kante gilt als richtig', t.name);
    }
  }
  // 1./2. Dreitafel
  T.setzen({ inputMode: 'riss', K: [40, 30], lastRiss: null, userModel: null });
  const rs = T.rissStrokesFrom(M);
  T.setzen({ strokes: rs }); T.setzen({ userModel: T.analyseRiss() }); T.checkRiss(); pruefungen++;
  let r = T.ergebnis();
  if (r.cls !== 'ok') melde('Dreitafel: Musterlösung nicht angenommen', `${t.name}: ${knapp(r.text)}`);
  T.setzen({ strokes: rs.slice(1) }); T.setzen({ userModel: T.analyseRiss() }); T.checkRiss(); pruefungen++;
  if (T.ergebnis().cls === 'ok') melde('Dreitafel: Risse mit fehlender Linie gelten als richtig', t.name);
  T.setzen({ inputMode: 'schraeg', userModel: null });
  koerper.push({ name: t.name, id: t.id, M });
}
for (const ex of T.EXAMPLES) {
  if (!ex.build) continue;
  T.setzen({ task: null, targetModel: null, userModel: null });
  koerper.push({ name: ex.name, id: ex.id, M: T.buildTarget({ build: ex.build }) });
}
// 4. Details
for (const k of koerper) {
  T.setzen({ targetModel: k.M, task: null });
  let h = '';
  try { h = T.detailsHtml(k.M, false); } catch (e) { melde('Details: Fehler', k.name + ': ' + e.message); continue; }
  const text = h.replace(/<[^>]+>/g, ' ');
  if (/undefined|NaN|Infinity|\[object/.test(text)) melde('Details: Text kaputt', k.name + ': ' + (text.match(/.{0,40}(undefined|NaN|Infinity|\[object).{0,20}/) || [''])[0]);
  if (/\d,\d/.test(text)) melde('Details: Dezimalkomma', k.name + ': ' + text.match(/.{0,30}\d,\d.{0,10}/)[0]);
}
// 3. Körper an python3
const daten = koerper.map(k => ({ name: k.name, id: k.id, V: k.M.V, E: k.M.E.map(e => [e.i, e.j]),
  F: k.M.F.map(f => ({ idx: f.idx, holes: f.holes || [] })), area: k.M.area, volume: k.M.volume, closed: k.M.closed }));
const py = String.raw`
import json, math, sys
d = json.load(sys.stdin)
fehler = []
def newell(V, loop):
    n = [0.0, 0.0, 0.0]
    for a, b in zip(loop, loop[1:] + loop[:1]):
        p, q = V[a], V[b]
        n[0] += (p[1] - q[1]) * (p[2] + q[2]); n[1] += (p[2] - q[2]) * (p[0] + q[0]); n[2] += (p[0] - q[0]) * (p[1] + q[1])
    return [x / 2 for x in n]
def flaeche(V, f):
    n = newell(V, f['idx']); A = math.hypot(*n)
    for h in f['holes']: A -= math.hypot(*newell(V, h))
    return A
def volumen(V, F):
    # Divergenzsatz: jede Fläche in Dreiecke vom ersten Punkt aus, Löcher abziehen (Orientierung über den Betrag)
    s = 0.0
    for f in F:
        for loop, vz in [(f['idx'], 1)] + [(h, -1) for h in f['holes']]:
            p0 = V[loop[0]]
            for a, b in zip(loop[1:-1], loop[2:]):
                p1, p2 = V[a], V[b]
                s += vz * (p0[0] * (p1[1] * p2[2] - p1[2] * p2[1]) - p0[1] * (p1[0] * p2[2] - p1[2] * p2[0]) + p0[2] * (p1[0] * p2[1] - p1[1] * p2[0]))
    return abs(s) / 6
r2, r3, r5 = math.sqrt(2), math.sqrt(3), math.sqrt(5)
def kante(V, E): return min(math.dist(V[i], V[j]) for i, j in E)
FORMEL = {   # Oberfläche, Volumen aus den Massen der Aufgabe
  'quader': (2 * (5*3 + 5*4 + 3*4), 5 * 3 * 4),
  'keil': (2 * 6 + (4 + 3 + 5) * 3, 6 * 3),
  'haus': (2 * 16 + (4 + 3 + 2 * math.sqrt(8) + 3) * 6, 16 * 6),
  'lprisma': (2 * 18 + 20 * 3, 18 * 3),
  'pyramide': (16 + 4 * 0.5 * 4 * math.sqrt(25 + 4), 16 * 5 / 3),
  'wuerfel': (96 - 3 * 2 + r3 / 4 * 8, 64 - 8 / 6),
  'satteldach': (2 * 27 + (6 + 3 + 2 * math.sqrt(18) + 3) * 5, 27 * 5),
}
for k in d:
    V, E, F = k['V'], k['E'], k['F']
    if not k['closed']: fehler.append(['Körper nicht geschlossen', k['name']]); continue
    if len(V) - len(E) + len(F) != 2: fehler.append(['Euler E − K + F ≠ 2', '%s: %d − %d + %d' % (k['name'], len(V), len(E), len(F))])
    A = sum(flaeche(V, f) for f in F); Vol = volumen(V, F)
    if abs(A - k['area']) > 1e-6: fehler.append(['Oberfläche weicht ab (Flächen)', '%s: JS %.4f, python %.4f' % (k['name'], k['area'], A)])
    if abs(Vol - k['volume']) > 1e-6: fehler.append(['Volumen weicht ab (Flächen)', '%s: JS %.4f, python %.4f' % (k['name'], k['volume'], Vol)])
    soll = FORMEL.get(k['id'])
    a = kante(V, E)
    if k['id'] == 'tetraeder': soll = (r3 * a * a, a ** 3 / (6 * r2))
    if k['id'] == 'oktaeder': soll = (2 * r3 * a * a, r2 / 3 * a ** 3)
    if k['id'] == 'dodekaeder': soll = (3 * math.sqrt(25 + 10 * r5) * a * a, (15 + 7 * r5) / 4 * a ** 3)
    if k['id'] == 'ikosaeder': soll = (5 * r3 * a * a, 5 * (3 + r5) / 12 * a ** 3)
    if k['id'] == 'wuerfel' and len(V) == 8: soll = (6 * a * a, a ** 3)
    if soll:
        if abs(soll[0] - k['area']) > 1e-6: fehler.append(['Oberfläche weicht von der Formel ab', '%s: JS %.4f, Formel %.4f' % (k['name'], k['area'], soll[0])])
        if abs(soll[1] - k['volume']) > 1e-6: fehler.append(['Volumen weicht von der Formel ab', '%s: JS %.4f, Formel %.4f' % (k['name'], k['volume'], soll[1])])
json.dump(fehler, sys.stdout)
`;
const r = spawnSync('python3', ['-c', py], { input: JSON.stringify(daten), encoding: 'utf8' });
if (r.status !== 0) { console.log('python3 fehlgeschlagen:\n' + r.stderr); process.exit(1); }
for (const [art, info] of JSON.parse(r.stdout)) melde(art, info);
console.log(`Schrägbild-Werkstatt: ${T.TASKS.filter(t => t.build).length} Übungen, ${pruefungen} Prüfungen, ${koerper.length} Körper · Oberfläche und Volumen in python3`);
if (!befunde.size) { console.log('alles in Ordnung'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`[${n}×] ${art}: ${info}`);
process.exit(1);
