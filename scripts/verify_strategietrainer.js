#!/usr/bin/env node
// Selbsttest des Strategietrainers (werkzeuge/strategietrainer.html), ohne Browser: Der Block
// zwischen «KERN:ANFANG» und «KERN:ENDE» wird in node:vm geladen.
//   node scripts/verify_strategietrainer.js            # 400 Aufgaben je Vorlage (Pre-Flight)
//   node scripts/verify_strategietrainer.js 5000       # gründlicher
// Je Vorlage werden Zufallsaufgaben erzeugt und alle passenden Wege bis zum Ende verfolgt.
// Geprüft wird:
//   – jeder Schritt der Liste liefert in jedem Zustand ok/um/x mit Text, ohne «undefined»/«NaN»
//   – jeder Zustand hat mindestens einen passenden Schritt und einen Tipp
//   – Gleichungen: Die Lösungen erfüllen die gestellte Gleichung, es fehlt keine; bei
//     Bruchgleichungen fallen genau die verbotenen Zahlen weg
//   – Terme: Das Ergebnis hat an Zufallsstellen denselben Wert wie der gestellte Term, ist
//     vollständig zerlegt bzw. gekürzt, und 𝔻 stimmt mit den Nullstellen des Nenners überein
//   – Systeme: Jedes Lösungspaar erfüllt beide Gleichungen, die Anzahl stimmt
//   – LaTeX: Klammern ausgeglichen, keine «+ -», «1x», «x^1», «+ 0»
//   – Einzelfälle aus TODO-trainer-korrekturen.md (ST-B1 … ST-C9, RT-C10), siehe pruefeFaelle
// Exit 1 bei einem Befund.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'werkzeuge', 'strategietrainer.html'), 'utf8');
const kern = html.slice(html.indexOf('// ── KERN:ANFANG'), html.indexOf('// ── KERN:ENDE'));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(kern + '\n;globalThis.K = { LISTEN, familie, regel, ausfuehren, passend, tipp, VORLAGEN, wzWert, analyse, aktiv, gemeinsam, gegen, resid };', ctx);
const K = ctx.K;
const N = +process.argv[2] || 400;
const befunde = new Map();
const melde = (art, info) => { if (!befunde.has(art)) befunde.set(art, { n: 0, info }); befunde.get(art).n++; };

function latexOk(z, wo) {
  let tiefe = 0;
  for (const ch of z) { if (ch === '{') tiefe++; if (ch === '}') tiefe--; if (tiefe < 0) break; }
  if (tiefe !== 0) melde('LaTeX: Klammern { } unausgeglichen', wo + ': ' + z);
  let rund = 0;
  for (const ch of z.replace(/\\[a-z]+/g, '')) { if (ch === '(') rund++; if (ch === ')') rund--; }
  if (rund !== 0) melde('LaTeX: Klammern ( ) unausgeglichen', wo + ': ' + z);
  if (/undefined|NaN|Infinity|\[object/.test(z)) melde('Text: undefined/NaN', wo + ': ' + z);
  if (/[+-] -|\+ \+/.test(z)) melde('LaTeX: doppeltes Vorzeichen', wo + ': ' + z);
  if (/(^|[^0-9.])1[xy](?![0-9])/.test(z)) melde('LaTeX: 1x', wo + ': ' + z);
  if (/[xy]\^1(?!\d)/.test(z)) melde('LaTeX: x^1', wo + ': ' + z);
  // «- 0» ist beim Zurückeinsetzen von x = 0 richtig (y = 0^2 - 0 - 4)
  if (/[+-] 0(?![.\d])/.test(z) && !/zurueck/.test(wo)) melde('LaTeX: ± 0', wo + ': ' + z);
}

// Reelle Nullstellen einer Funktion, die ein Polynom höchstens 2. Grades ist (aus Stützstellen)
function nullstellen(f) {
  const f0 = f(0), f1 = f(1), fm = f(-1);
  const a = (f1 + fm) / 2 - f0, b = (f1 - fm) / 2, c = f0;
  const eps = 1e-9;
  if (Math.abs(f(2) - (4 * a + 2 * b + c)) > 1e-6) return 'grad>2';
  if (Math.abs(a) < eps) {
    if (Math.abs(b) < eps) return Math.abs(c) < eps ? 'alle' : [];
    return [-c / b];
  }
  const D = b * b - 4 * a * c;
  if (D < -1e-9) return [];
  if (Math.abs(D) < 1e-9) return [-b / (2 * a)];
  return [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort((u, v) => u - v);
}
const nah = (u, v) => Math.abs(u - v) < 1e-7 * (1 + Math.abs(u));

function pruefeGl(ende, a, wo) {
  const d = ende.gl;
  if (!d) { melde('Ende ohne Daten (Gleichung)', wo); return; }
  const Dw = a.dW || [];
  if (Dw.length && !(d.Dw && d.Dw.length === Dw.length)) melde('Bruchgleichung: 𝔻 fehlt am Ende', wo);
  let soll = nullstellen(a.g || a.f);
  if (soll === 'grad>2') { melde('Prüfung: Gleichung nicht höchstens quadratisch', wo); return; }
  if (d.wahr !== undefined) {
    if ((soll === 'alle') !== d.wahr) melde('Lösung: wahr/falsch vertauscht', wo + ' ' + ende.z);
    if (soll !== 'alle' && soll.filter(v => !Dw.some(p => nah(p, v))).length) melde('Lösung: Widerspruch, aber Gleichung lösbar', wo);
    return;
  }
  if (soll === 'alle') { melde('Lösung: ℝ erwartet', wo); return; }
  soll = soll.filter(v => !Dw.some(p => nah(p, v)));
  const ist = d.w.map(K.wzWert).sort((u, v) => u - v);
  if (ist.length !== soll.length || ist.some((v, i) => !nah(v, soll[i])))
    melde('Lösung: falsch oder unvollständig', wo + ' → ' + ende.z + ' | soll ' + JSON.stringify(soll));
  for (const v of ist) if (Math.abs(a.f(v)) > 1e-6 * (1 + Math.abs(v) ** 2)) melde('Lösung erfüllt die Gleichung nicht', wo + ' x = ' + v);
}
function pruefeTerm(ende, a, wo) {
  const d = ende.term;
  if (!d) { melde('Ende ohne Daten (Term)', wo); return; }
  const Dw = a.dW || [];
  for (const x of [-3.7, -1.3, 0.6, 2.9, 5.1]) {
    if (Dw.some(p => Math.abs(p - x) < 1e-9)) continue;
    if (!nah(d.wert(x), a.wert(x))) { melde('Term: Ergebnis hat einen anderen Wert', wo + ' → ' + ende.z); break; }
  }
  for (const pr of d.teile) for (const fa of pr.f) if (K.analyse(fa.p).m || fa.grp) melde('Term: nicht vollständig zerlegt', wo + ' → ' + ende.z);
  if (d.teile.length === 2) {
    if (K.gemeinsam(d.teile[0], d.teile[1])) melde('Bruchterm: noch kürzbar', wo + ' → ' + ende.z);
    if (K.gegen(d.teile[0], d.teile[1])) melde('Bruchterm: Vorzeichen nicht angeglichen', wo + ' → ' + ende.z);
    const ist = (d.Dw || []).slice().sort((u, v) => u - v), soll = Dw.slice().sort((u, v) => u - v);
    if (ist.length !== soll.length || ist.some((v, i) => v !== soll[i])) melde('Bruchterm: 𝔻 falsch', wo + ' → ' + ende.z + ' | soll ' + soll);
  }
}
function pruefeSys(ende, a, wo) {
  const d = ende.sys;
  if (!d) { melde('Ende ohne Daten (System)', wo); return; }
  const res = a.g.map(K.resid);
  if (d.gerade) {
    if (a.anzahl !== 'unendlich') melde('System: unendlich viele Lösungen gemeldet', wo);
    for (const t of [-2, 0, 3]) if (res.some(r => Math.abs(r(t, d.gerade[0] * t + d.gerade[1])) > 1e-9)) melde('System: Gerade erfüllt die Gleichungen nicht', wo);
    return;
  }
  if (d.paare.length !== a.anzahl) melde('System: Anzahl Lösungen falsch', wo + ' → ' + ende.z + ' | soll ' + a.anzahl);
  for (const [x, y] of d.paare) {
    if (!Number.isInteger(x) || !Number.isInteger(y)) melde('System: Lösung nicht ganzzahlig', wo + ' → ' + ende.z);
    if (res.some(r => Math.abs(r(x, y)) > 1e-9)) melde('System: Paar erfüllt die Gleichungen nicht', wo + ' → ' + ende.z);
  }
}

// ── Einzelfälle aus der Prüfung vom 11.10.2026 (TODO-trainer-korrekturen.md) ──
const ggT = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
const kgV = (a, b) => Math.abs(a * b) / ggT(a, b);
const quadratZahl = n => n >= 0 && Math.round(Math.sqrt(n)) ** 2 === n;
const NULL_FORM = ['q_fakt', 'q_binom', 'q_teilbar', 'q_allg', 'q_rein', 'q_ohne_c', 'q_prod'];
function pruefeFaelle(st, a, wo, tiefe) {
  const fam = K.familie(st), R = id => K.regel(st, id);
  if (fam === 'gl') {
    // ST-C3: Mitternachtsformel einheitlich — ✓ nur bei ax² + bx + c = 0 ohne Spezialform,
    // ≈ bei einer Spezialform (b = 0, c = 0, Binom, Zweiklammersatz, schon faktorisiert), ✗ wenn rechts nicht 0 steht
    let soll = 'x';
    if (NULL_FORM.includes(st.k)) {
      soll = 'um';
      if (st.k === 'q_allg') soll = 'ok';
      if (st.k === 'q_teilbar') { const B = st.b / st.a, C = st.c / st.a; if (!quadratZahl(B * B - 4 * C)) soll = 'ok'; }
    }
    if (R('mf')[0] !== soll) melde('ST-C3: Mitternachtsformel uneinheitlich bewertet', st.k + ' «' + st.z + '»: ' + R('mf')[0] + ' statt ' + soll);
    // ST-B3: x² = negative Zahl — Faktorisieren ist ✗
    if (st.k === 'q_x2' && st.n < 0 && R('binom')[0] !== 'x') melde('ST-B3: Faktorisieren bei x² = negativ nicht ✗', st.z);
    // ST-C1: x² = Bruch — eigener Text
    if (st.k === 'q_x2' && st.d > 1 && R('brueche')[1] === 'Hier stehen keine Brüche.') melde('ST-C1: «keine Brüche» bei x² = Bruch', st.z);
    // ST-C2: Bruchgleichung — keine Klammern, keine Zahl vor x
    if (st.k === 'bruch_gl') for (const id of ['klammern', 'teilen']) if (R(id)[0] !== 'x') melde('ST-C2: ' + id + ' bei Bruchgleichung nicht ✗', st.z);
    // ST-C5: «nicht in Faktoren zerlegen» stimmt nicht, wenn ein Zahlfaktor ausgeklammert werden kann
    for (const [id] of K.LISTEN.gl) { const r = R(id); if (r[1] && /nicht in Faktoren zerlegen/.test(r[1])) melde('ST-C5: «nicht in Faktoren zerlegen»', st.z + ' / ' + id); }
    // ST-C8: «x = 0 geht verloren» nur, wo 0 eine Lösung ist
    const f0 = a.f(0), nullLsg = Number.isFinite(f0) && Math.abs(f0) < 1e-9 && !(a.dW || []).includes(0);
    const dx = R('durchx');
    if (!nullLsg && dx[1] && /x = 0/.test(dx[1]) && /verl/.test(dx[1])) melde('ST-C8: «x = 0 geht verloren», obwohl 0 keine Lösung ist', st.k + ' «' + st.z + '»');
    // ST-C6 und ST-C9 (Gleichungen): ausführen und Ergebnis ansehen
    for (const id of K.passend(st)) {
      const aus = K.ausfuehren(st, id);
      const ops = [aus.op, ...aus.zeilen.map(z => z[1])];
      if (ops.some(o => o === 'Binom' || o === 'faktorisieren')) melde('ST-C9: Schritt heisst nur «Binom»/«faktorisieren»', st.k + ' «' + st.z + '» → ' + ops.join(' | '));
      if (st.k === 'q_ohne_c' && id === 'ausklammern') {
        const m = /\((-?\d*)x ([+-]) (\d+)\) = 0$/.exec(aus.next.z);
        if (m) { const k = m[1] === '' ? 1 : m[1] === '-' ? -1 : +m[1];
          if (ggT(k, +m[3]) > 1 || k < 0) melde('ST-C6: Zahlfaktor in der Klammer stehen gelassen', st.z + ' → ' + aus.next.z); }
      }
    }
  }
  if (fam === 'term' && tiefe === 0) {
    // ST-C7: im ersten Schritt gibt es nichts auszumultiplizieren
    const r = R('ausmult');
    if (r[0] !== 'x' || /wieder am Anfang/.test(r[1])) melde('ST-C7: Ausmultiplizieren im ersten Schritt', st.z + ': ' + r[0] + ' ' + r[1]);
  }
  if (st.k === 's_sys' && !st.g.some(e => e.roh) && st.g.every(e => e.t === 'lin' && e.form === 'norm')) {
    const [e1, e2] = st.g;
    // ST-B1: «es entstehen Brüche» nur, wenn sich keine Gleichung ohne Brüche nach einer Variablen auflösen lässt
    const glatt = e => (e.b && e.a % e.b === 0 && e.c % e.b === 0) || (e.a && e.b % e.a === 0 && e.c % e.a === 0);
    const ein = R('einsetzen');
    if (ein[0] !== 'ok' && /Brüche/.test(ein[1]) && st.g.some(glatt)) melde('ST-B1: «es entstehen Brüche», obwohl eine Gleichung glatt auflösbar ist', st.z);
    // ST-B2: Additionsverfahren eliminiert die Variable mit dem kleineren kgV
    if (R('addition')[0] === 'ok' && e1.a && e2.a && e1.b && e2.b) {
      const aus = K.ausfuehren(st, 'addition'), kx = kgV(e1.a, e2.a), ky = kgV(e1.b, e2.b);
      const bleibt = kx < ky ? 'y' : 'x';
      if (aus.next.v && aus.next.v !== bleibt) melde('ST-B2: Additionsverfahren eliminiert nicht die Variable mit dem kleineren kgV', st.z + ' (kgV x ' + kx + ', y ' + ky + ') → ' + aus.op);
    }
  }
}

let zustaende = 0, wege = 0;
function gehe(st, a, wo, tiefe) {
  zustaende++;
  if (tiefe > 16) { melde('Weg zu lang', wo); return; }
  latexOk(st.z, wo);
  const ok = K.passend(st);
  if (!ok.length) { melde('Zustand ohne passenden Schritt', wo + ' ' + st.k + ': ' + st.z); return; }
  const t = K.tipp(st);
  if (typeof t !== 'string' || !t) melde('Tipp fehlt', st.k); else latexOk(t, 'Tipp ' + st.k);
  for (const [id] of K.LISTEN[K.familie(st)]) {
    const r = K.regel(st, id);
    if (!r || !['ok', 'um', 'x'].includes(r[0])) { melde('Regel fehlt', st.k + '/' + id); continue; }
    if (r[0] !== 'ok') {
      if (typeof r[1] !== 'string' || !r[1]) melde('Regeltext fehlt', st.k + '/' + id);
      else { latexOk(r[1], st.k + '/' + id); if (r[1] === 'Dieser Schritt passt hier nicht.') melde('Regel ohne eigene Begründung', st.k + '/' + id); }
    }
  }
  pruefeFaelle(st, a, wo, tiefe);
  for (const id of ok) {
    const aus = K.ausfuehren(st, id);
    for (const [z] of aus.zeilen) latexOk(z, wo + ' ' + id);
    if (aus.ersetzen) latexOk(aus.ersetzen, wo + ' ' + id);
    if (aus.info) latexOk(aus.info, wo + ' ' + id);
    if (aus.next.k === 'ende') {
      latexOk(aus.next.z, wo + ' Ende');
      wege++;
      const f = K.familie(st);
      if (f === 'gl') pruefeGl(aus.next, a, wo); else if (f === 'term') pruefeTerm(aus.next, a, wo); else pruefeSys(aus.next, a, wo);
      continue;
    }
    gehe(aus.next, a, wo + ' →' + id, tiefe + 1);
  }
}

const zaehl = {};
for (const bereich of Object.keys(K.VORLAGEN)) {
  for (const [, fn] of K.VORLAGEN[bereich]) {
    let n = 0, leer = 0;
    while (n < N) {
      const a = fn();
      if (!a) { if (++leer > 50 * N) { melde('Vorlage liefert fast nie eine Aufgabe', fn.name); break; } continue; }
      n++;
      zaehl[fn.name] = (zaehl[fn.name] || 0) + 1;
      gehe(a.st, a, fn.name + ' «' + a.st.z + '»', 0);
    }
  }
}

// ── Seite (ausserhalb des Kerns) ──
{
  const merk = html.slice(html.indexOf('⭐ Welcher Schritt wann?'), html.indexOf('</details>', html.indexOf('⭐ Welcher Schritt wann?')));
  const teilen = /Durch die Zahl vor[^]*?<\/tr>/.exec(merk);
  // ST-C4: «teilen bei gemeinsamem Faktor» nur bei quadratischen Gleichungen
  if (!teilen || (/gemeinsamen Faktor/.test(teilen[0]) && !/quadratisch/.test(teilen[0]))) melde('ST-C4: Merkkasten «teilen bei gemeinsamem Faktor» gilt auch für lineare Gleichungen', teilen && teilen[0]);
  // ST-C9: Einleitung verweist auf s2.2a und s3.1
  const einl = html.slice(html.indexOf('pt-untertitel'), html.indexOf('</p>', html.indexOf('pt-untertitel')));
  for (const s of ['s2-2a-', 's3-1-']) if (!einl.includes(s)) melde('ST-C9: Einleitung ohne Verweis auf ' + s, '');
  // RT-C10: Bereichs-Schalter mit aria-pressed, beim Umschalten nachgeführt
  const knoepfe = html.match(/<button[^>]*class="tr-opt[^"]*"[^>]*>/g) || [];
  if (!knoepfe.length || knoepfe.some(b => !/aria-pressed="(true|false)"/.test(b))) melde('RT-C10: tr-opt ohne aria-pressed', knoepfe[0]);
  if (!/setAttribute\('aria-pressed'/.test(html)) melde('RT-C10: aria-pressed wird nicht nachgeführt', '');
}

console.log(`${Object.keys(zaehl).length} Vorlagen · ${Object.values(zaehl).reduce((s, v) => s + v, 0)} Aufgaben · ${zustaende} Zustände · ${wege} Wege bis zum Ende`);
if (!befunde.size) { console.log('✓ keine Befunde'); process.exit(0); }
for (const [art, { n, info }] of befunde) console.log(`✗ ${art} (${n}×) — z.B. ${info}`);
process.exit(1);
