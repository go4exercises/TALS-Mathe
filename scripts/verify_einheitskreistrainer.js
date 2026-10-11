#!/usr/bin/env node
// Selbsttest des Einheitskreistrainers (werkzeuge/einheitskreistrainer.html), ohne Browser: Der Block
// zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_einheitskreistrainer.js         # 300 Aufgaben je Teil (Pre-Flight)
// Geprüft wird:
//   – jeder exakte Wert (sin, cos, tan für alle Winkel der Aufgaben) gegen Math.sin/cos/tan und
//     unabhängig in python3 (math); «nicht definiert» genau dort, wo cos = 0
//   – die Herleitung endet beim richtigen Wert; die Palette nimmt genau den richtigen Wert an
//   – Grad ↔ Bogenmass: exakt in python3 mit Fraction; Eingaben «5pi/6», «5π/6», «5/6pi» werden
//     angenommen, ungekürzte als «fast», «5/6» als «π vergessen», das Doppelte als «halb»
//   – Vom Wert zum Winkel: Die Lösungsmenge stimmt mit der in python3 berechneten überein
//     (asin/acos/atan, auf [0°; 360°[ gebracht); fehlende Lösung → «nur eine Lösung»
//   – LaTeX ohne unausgeglichene Klammern, ohne «undefined»
//   – Taste «Nächster Schritt»: Schrittliste nicht leer, jeder Titel nicht leer und nicht generisch («Schritt 2»),
//     LaTeX ausgeglichen, und die Schritte zusammengefügt ergeben genau den bisherigen Weg (a.weg bzw. herleitung)
//   – gezielte Fälle aus der Prüfung vom 11.10.2026 (EK-B1 … EK-C11): «*» als Produkt, Diagnosen für
//     Grad statt Bogenmass, π vergessen, Faktor bzw. Bruch umgedreht, zwei Fehler auf einmal, sin/cos
//     vertauscht und falsche Symmetrie beim Rückweg, Tangens-Herleitung über sin/cos, Intervall [0°; 360°[
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { spawnSync } = require('child_process');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'einheitskreistrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { THEMEN, FEHLER, KREIS, AUSSEN, PALETTE, wert, wertZahl, wertTex, herleitung, herleitungSchritte, schrittListe, pruefe, radTex, mod360 };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 300;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };
function latexOk(z, wo) {
  let t = 0; for (const ch of z) { if (ch === '{') t++; if (ch === '}') t--; if (t < 0) break; }
  if (t !== 0) melde('LaTeX: { } unausgeglichen', wo + ': ' + z);
  if ((z.match(/\\\(/g) || []).length !== (z.match(/\\\)/g) || []).length) melde('LaTeX: \\( \\) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|null|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
}

// Schritte zusammengefügt = bisheriger Weg. Eine Fortsetzung «\(= …» hängt sich an die Formel davor an.
const zusammen = zeilen => zeilen.join(' ').replace(/\\\) \\\(= /g, ' = ').replace(/\s+/g, ' ').trim();
function schritteOk(schritte, weg, wo) {
  if (!Array.isArray(schritte) || !schritte.length) { melde('Schritte: Liste leer', wo); return; }
  for (const st of schritte) {
    if (!st.titel || !String(st.titel).trim()) melde('Schritte: Titel leer', wo);
    else if (/^\s*(schritt|step)?\s*\d*\s*[.:]?\s*$/i.test(st.titel) || st.titel.replace(/\\\(|\\\)/g, '').trim().length < 6) melde('Schritte: Titel generisch', wo + ': ' + st.titel);
    latexOk(st.titel, wo + ' Schritttitel');
    if (!Array.isArray(st.zeilen) || !st.zeilen.length) melde('Schritte: Schritt ohne Inhalt', wo + ': ' + st.titel);
    else st.zeilen.forEach(z => latexOk(z, wo + ' Schritt'));
  }
  const ist = zusammen(schritte.flatMap(st => st.zeilen || [])), soll = zusammen(weg);
  if (ist !== soll) melde('Schritte: ergeben nicht den bisherigen Weg', wo + '\n    Schritte: ' + ist + '\n    Weg:      ' + soll);
}

const py = [];
// 1. Werte aller Aufgabenwinkel
for (const g of K.KREIS.concat(K.AUSSEN)) for (const f of ['sin', 'cos', 'tan']) {
  const k = K.wert(f, g), z = K.wertZahl(k), r = g * Math.PI / 180;
  const soll = f === 'sin' ? Math.sin(r) : f === 'cos' ? Math.cos(r) : (Math.abs(Math.cos(r)) < 1e-12 ? null : Math.tan(r));
  if ((soll === null) !== (z === null) || (z !== null && Math.abs(z - soll) > 1e-12)) melde('Exakter Wert falsch', f + ' ' + g + '° → ' + k);
  py.push({ art: 'wert', f, g, z });
  for (const mass of ['grad', 'rad']) {
    const h = K.herleitung(f, g, mass);
    h.forEach(x => latexOk(x, f + ' ' + g));
    schritteOk(K.herleitungSchritte(f, g, mass), h, 'Schritte ' + f + ' ' + g + ' ' + mass);
    if (!h[h.length - 1].includes(k === 'nd' ? 'nicht definiert' : K.wertTex(k))) melde('Herleitung endet nicht beim Wert', f + ' ' + g + ' ' + mass + ': ' + h[h.length - 1]);
  }
}
// 2. Aufgaben je Teil
const radEingaben = g => {
  const t = K.radTex(g);            // z.B. -\frac{5\pi}{6}
  const m = /^(-?)(?:\\frac\{(\d*)\\pi\}\{(\d+)\}|(\d*)\\pi)$/.exec(t);
  if (t === '0') return ['0'];
  const vz = m[1], z = m[2] !== undefined ? m[2] : m[4], n = m[3];
  return n ? [vz + z + 'pi/' + n, vz + z + 'π/' + n, vz + (z || '1') + '/' + n + 'pi'] : [vz + z + 'pi'];
};
let zahl = 0;
for (const thema of Object.keys(K.THEMEN)) for (const mass of ['grad', 'rad', 'mix']) for (let i = 0; i < N / 3; i++) {
  const a = K.THEMEN[thema].neu(mass);
  if (!a) continue;
  zahl++;
  const wo = thema + ' «' + a.ausdruck + '»';
  latexOk(a.ausdruck, wo); latexOk(a.auftrag, wo); a.weg.forEach(z => latexOk(z, wo + ' Weg'));
  schritteOk(K.schrittListe(a), a.weg, wo + ' Schritte');
  if (a.art === 'rad') {
    for (const e of radEingaben(a.grad)) { const r = K.pruefe(a, e); if (r.status !== 'ok') melde('Bogenmass-Eingabe nicht angenommen', wo + ' ' + e + ' ' + JSON.stringify(r)); }
    const zN = a.grad / 180;
    const doppelt = K.pruefe(a, (2 * a.grad) + '/180pi');
    if (doppelt.status === 'ok') melde('Doppeltes als richtig angenommen', wo);
    if (a.grad % 180 !== 0) {
      const g = a.grad / 15, ungek = K.pruefe(a, g + 'pi/12');          // z.B. 10pi/12 für 150°
      if (ungek.status !== (ggt(g, 12) === 1 ? 'ok' : 'fast')) melde('Ungekürzt nicht als «fast»', wo + ' ' + g + 'pi/12 → ' + ungek.status);
      const ohne = K.pruefe(a, (a.grad / ggt(a.grad, 180)) + '/' + (180 / ggt(a.grad, 180)));
      if (ohne.code !== 'ohnePi') melde('«π vergessen» nicht erkannt', wo + ' ' + JSON.stringify(ohne));
    }
    py.push({ art: 'rad', g: a.grad, tex: K.radTex(a.grad) });
  } else if (a.art === 'grad') {
    if (K.pruefe(a, String(a.grad)).status !== 'ok' || K.pruefe(a, a.grad + '°').status !== 'ok') melde('Grad-Eingabe nicht angenommen', wo);
    if (K.pruefe(a, String(2 * a.grad)).code !== 'halb') melde('Doppeltes nicht als «halb» erkannt', wo);
  } else if (a.art === 'palette') {
    let ok = 0;
    for (const k of K.PALETTE) { const r = K.pruefe(a, k); if (r.status === 'ok') ok++; else if (!K.FEHLER[r.code]) melde('Fehlercode ohne Text', r.code); }
    if (ok !== 1) melde('Palette: nicht genau ein richtiger Wert', wo + ' ' + ok);
    if (!K.PALETTE.includes(a.loesung)) melde('Lösung fehlt in der Palette', wo + ' ' + a.loesung);
  } else {
    if (K.pruefe(a, a.loesung.slice()).status !== 'ok') melde('Umkehr: Lösung nicht angenommen', wo);
    if (a.loesung.length > 1 && K.pruefe(a, a.loesung.slice(0, 1)).code !== (a.f === 'tan' ? 'umkehrEineTan' : 'umkehrEine')) melde('Umkehr: fehlende Lösung nicht erkannt', wo);
    py.push({ art: 'umkehr', f: a.f, z: K.wertZahl(a.w), loes: a.loesung, wo });
  }
}
function ggt(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; }

// 3. Gezielte Fälle (Prüfung vom 11.10.2026, TODO-trainer-korrekturen.md)
const fall = (art, bed, info) => { if (!bed) melde(art, info); };
const istCode = (r, code) => r && r.code === code;
{
  const rad = g => ({ thema: 'umrechnen', art: 'rad', grad: g }), grad = g => ({ thema: 'umrechnen', art: 'grad', grad: g });
  // EK-B1: ohne Diagnose beim Umrechnen keine Rede von Quadrant und Referenzwinkel
  for (const [a, e] of [[rad(150), '7pi/3'], [grad(150), '17']]) {
    const r = K.pruefe(a, e), f = K.FEHLER[r.code];
    fall('EK-B1: Rückmeldung beim Umrechnen spricht vom Quadranten', f && !/Quadrant|Referenzwinkel/.test(f[1]) && /180/.test(f[1]), a.art + ' ' + e + ' → ' + r.code);
  }
  // EK-B2: «*» als Produkt
  for (const e of ['pi/6*5', 'pi*5/6', '5*pi/6', '5/6*pi', '(5*pi)/6', '5 * pi / 6', '5π/6', '5/6pi', '(5pi)/6'])
    fall('EK-B2: Produkt mit * nicht gelesen', K.pruefe(rad(150), e).status === 'ok', e + ' → ' + JSON.stringify(K.pruefe(rad(150), e)));
  fall('EK-B2: Produkt mit * nicht gelesen', K.pruefe(rad(-45), '-pi/4*1').status === 'ok' && K.pruefe(rad(-45), '-1*pi/4').status === 'ok', '-pi/4');
  fall('EK-B2: ungekürzt mit * nicht «fast»', K.pruefe(rad(150), 'pi/12*10').status === 'fast', 'pi/12*10');
  // EK-C11: Grad statt Bogenmass, π vergessen als Dezimalzahl, Faktor umgedreht
  fall('EK-C11: Grad statt Bogenmass nicht erkannt', istCode(K.pruefe(rad(150), '150'), 'gradStattRad') && istCode(K.pruefe(rad(150), '150°'), 'gradStattRad'), JSON.stringify(K.pruefe(rad(150), '150')));
  fall('EK-C11: π vergessen (Dezimalzahl) nicht erkannt', istCode(K.pruefe(rad(150), '0.8333'), 'ohnePi') && istCode(K.pruefe(rad(-30), '-0.1667'), 'ohnePi'), JSON.stringify(K.pruefe(rad(150), '0.8333')));
  fall('EK-C11: 6π bei 30° als «Faktor umgedreht»', !istCode(K.pruefe(rad(30), '6pi'), 'kehr') && K.FEHLER[K.pruefe(rad(30), '6pi').code], JSON.stringify(K.pruefe(rad(30), '6pi')));
  fall('EK-C11: Faktor umgedreht nicht erkannt', istCode(K.pruefe(rad(30), '1718.87'), 'kehr') && istCode(K.pruefe(rad(30), '5400/pi'), 'kehr'), JSON.stringify(K.pruefe(rad(30), '5400/pi')));
  // EK-C9: Umrechnungsweg mit Gradzeichen, Vorzeichen vor dem Bruch
  for (let i = 0; i < 400; i++) {
    const a = K.THEMEN.umrechnen.neu('grad'); if (!a) continue;
    fall('EK-C9: Umrechnungsweg ohne Gradzeichen', a.weg[0].includes(a.grad + '° \\cdot \\frac{\\pi}{180°}'), a.weg[0]);
    fall('EK-C9: Minus im Zähler', !/\\frac\{-/.test(a.weg.join(' ')), a.weg[0]);
  }
  // EK-C5: zwei Fehler auf einmal
  const pal = (f, g) => ({ thema: 'werte', art: 'palette', f, grad: g, mass: 'grad', loesung: K.wert(f, g) });
  fall('EK-C5: vertauscht + Vorzeichen', istCode(K.pruefe(pal('sin', 30), '-w3/2'), 'vertauschtVz'), JSON.stringify(K.pruefe(pal('sin', 30), '-w3/2')));
  fall('EK-C5: vertauscht ohne Vorzeichen', istCode(K.pruefe(pal('sin', 30), 'w3/2'), 'vertauscht'), JSON.stringify(K.pruefe(pal('sin', 30), 'w3/2')));
  fall('EK-C5: Kehrwert + Vorzeichen', istCode(K.pruefe(pal('tan', 30), '-w3'), 'tanKehrVz'), JSON.stringify(K.pruefe(pal('tan', 30), '-w3')));
  // EK-C6: Tangens-Herleitung mit sin/cos
  for (const g of [30, 45, 150, 240, 315, -60, 510]) fall('EK-C6: Tangens-Herleitung ohne sin/cos', K.herleitung('tan', g, 'grad').some(z => z.includes('\\frac{\\sin')), String(g));
  // EK-C10: kein Gedankenstrich neben Formeln bei «nicht definiert»
  fall('EK-C10: Gedankenstrich in FEHLER.nd', !/—/.test(K.FEHLER.nd[1]), K.FEHLER.nd[1]);
  // Vom Wert zum Winkel
  const um = (f, w) => ({ thema: 'umkehr', art: 'kreis', f, w, mass: 'grad', loesung: K.KREIS.filter(g => K.wert(f, g) === w) });
  for (let i = 0; i < 300; i++) {
    const a = K.THEMEN.umkehr.neu(i % 2 ? 'rad' : 'grad');
    fall('EK-C1: Intervall nicht als [0°; 360°[', a.auftrag.includes('[0°;\\,360°[') || a.auftrag.includes('[0;\\,2\\pi['), a.auftrag);
    // EK-C3: Lösungsmenge der anderen Funktion
    if (a.f !== 'tan') {
      const andere = K.KREIS.filter(g => K.wert(a.f === 'sin' ? 'cos' : 'sin', g) === a.w);
      if (andere.join() !== a.loesung.join()) fall('EK-C3: sin/cos vertauscht nicht erkannt', istCode(K.pruefe(a, andere), 'umkehrVertauscht'), a.ausdruck + ' ' + andere);
    }
  }
  // EK-C2: Text beim Tangens
  const t1 = K.pruefe(um('tan', '-w3'), [120]), ft = K.FEHLER[t1.code];
  fall('EK-C2: «nur eine Lösung» beim Tangens', ft && !/zwischen/.test(ft[1]) && /180°/.test(ft[1]), JSON.stringify(t1));
  fall('EK-C2: «nur eine Lösung» bei sin', istCode(K.pruefe(um('sin', '1/2'), [30]), 'umkehrEine'), JSON.stringify(K.pruefe(um('sin', '1/2'), [30])));
  // EK-C4: Tangens wie Sinus oder Cosinus gespiegelt
  for (const e of [[45, 135], [45, 315]]) fall('EK-C4: falsche Symmetrie beim Tangens', istCode(K.pruefe(um('tan', '1'), e), 'umkehrSymTan'), e + ' → ' + JSON.stringify(K.pruefe(um('tan', '1'), e)));
  fall('EK-C4: Vorzeichen beim Rückweg (sin)', istCode(K.pruefe(um('sin', '1/2'), [210, 330]), 'umkehrVz'), JSON.stringify(K.pruefe(um('sin', '1/2'), [210, 330])));
}

const skript = `
import sys, json, math
from fractions import Fraction
fehler = []
for z in json.load(sys.stdin):
    if z['art'] == 'wert':
        r = math.radians(z['g'])
        if z['f'] == 'tan' and abs(math.cos(r)) < 1e-12:
            soll = None
        else:
            soll = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[z['f']](r)
        if (soll is None) != (z['z'] is None) or (soll is not None and abs(soll - z['z']) > 1e-12):
            fehler.append(['python: Wert weicht ab', z['f'] + ' ' + str(z['g'])])
    elif z['art'] == 'rad':
        q = Fraction(z['g'], 180)
        t = z['tex']; vz = -1 if t.startswith('-') else 1; t = t.lstrip('-')
        if t == '0': ist = Fraction(0)
        elif t.startswith('\\\\frac'):
            zae, nen = t[6:].split('}{'); zae = zae.strip('{').replace('\\\\pi', '') or '1'; nen = nen.strip('}')
            ist = vz * Fraction(int(zae), int(nen))
        else: ist = vz * Fraction(int(t.replace('\\\\pi', '') or '1'))
        if ist != q: fehler.append(['python: Bogenmass weicht ab', str(z['g']) + ' ' + z['tex']])
    elif z['art'] == 'umkehr':
        v = z['z']; f = z['f']
        if f == 'sin': a = math.degrees(math.asin(v)); kand = [a, 180 - a]
        elif f == 'cos': a = math.degrees(math.acos(v)); kand = [a, -a]
        else: a = math.degrees(math.atan(v)); kand = [a, a + 180]
        loes = sorted(set(round(x % 360, 6) % 360 for x in kand))
        if loes != sorted(float(g) for g in z['loes']): fehler.append(['python: Lösungsmenge weicht ab', z['wo'] + ' py=' + str(loes)])
print(json.dumps(fehler))
`;
const p = spawnSync('python3', ['-c', skript], { input: JSON.stringify(py), encoding: 'utf8', maxBuffer: 1 << 26 });
if (p.status !== 0) melde('python3 nicht gelaufen', (p.stderr || '').slice(0, 400));
else for (const [art, info] of JSON.parse(p.stdout)) melde(art, info);

console.log(`${Object.keys(K.THEMEN).length} Teile · ${zahl} Aufgaben · ${py.length} Gegenrechnungen in python3`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
