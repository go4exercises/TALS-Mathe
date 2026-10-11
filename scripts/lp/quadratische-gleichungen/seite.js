<script>
/* Leitprogramm Quadratische Gleichungen — Umformer mit Aufgabenleiste, Parameter-Simulation, Übungen mit
   Rückmeldung, Minigrafen (11.10.2026). Grundgerüst (Zahlen und Mengen lesen, Achsen, Aufgabenleiste,
   Umformer) aus dem Leitprogramm «Lineare und quadratische Gleichungen». Notation wie auf der Themenseite 2.2b:
   Lösungsmenge 𝕃 mit Strichpunkt, leere Menge {}, Mitternachtsformel, D = b² − 4ac.
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Gleichung, Parabel · orange = Umformung,
   Parameter k · grün = Lösungen · rot = Fehler. Zahlen mit Dezimalpunkt und echtem Minus. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function z(n){ var r = Math.round(n * 1000) / 1000; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function zz(v){ var r = Math.round(v * 1000) / 1000; return (Math.abs(v - r) > 1e-9 ? '≈\u00a0' : '') + z(v); }
  function gl(a, b){ return Math.abs(a - b) < 1e-9; }

  /* ---------- Zahlen und Lösungsmengen lesen ----------
     Zahl: -3, 0.5, 1/2, -2/3, Dezimalkomma wird verstanden (und angemerkt).
     Menge: «{0; 3}», «0; 3», «3;0;0» (Reihenfolge und Doppelte egal), «{}» oder «leer» für die leere
     Menge, «R» oder «ℝ» für alle Zahlen. Getrennt wird mit Strichpunkt; «0, 3» (Komma mit Leerschlag)
     gilt auch als Trenner. */
  function zahl(s){
    var komma = /\d,\d/.test(s);
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^\+/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(-?\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  function menge(s){
    var t = String(s).trim().replace(/\u2212/g, '-');
    if (!t) return { leer: true };
    var komma = /\d,\d/.test(t);
    t = t.replace(/^𝕃\s*=\s*/, '').replace(/^L\s*=\s*/i, '');
    if (/^(r|ℝ|\{\s*(r|ℝ)\s*\}|alle|alle zahlen)$/i.test(t)) return { alle: true, werte: [] };
    t = t.replace(/^\{/, '').replace(/\}$/, '').trim();
    if (!t || /^(leer|keine|∅)$/i.test(t)) return { werte: [], komma: komma };
    if (/^[a-z]\w*\s*=/i.test(t)) return { kaputt: true, xgleich: true };
    t = t.replace(/-\s+(?=[\d.])/g, '-');   // «- 3» wie «-3»
    var teile = t.split(/;|,\s+|\||\s+/), w = [];
    for (var i = 0; i < teile.length; i++){
      if (!teile[i].trim()) continue;
      var r = zahl(teile[i]); if (isNaN(r.wert)) return { kaputt: true };
      if (r.komma) komma = true;
      if (!w.some(function(v){ return gl(v, r.wert); })) w.push(r.wert);
    }
    return { werte: w, komma: komma };
  }
  /* Vergleich mit der Soll-Menge: soll = Zahlenliste, [] (leer) oder 'R' (alle). */
  function mengeGleich(e, soll){
    if (soll === 'R') return !!e.alle;
    if (e.alle) return false;
    if (e.werte.length !== soll.length) return false;
    return soll.every(function(v){ return e.werte.some(function(w){ return gl(v, w); }); });
  }
  function mengeTex(soll){
    if (soll === 'R') return '\\mathbb{L} = \\mathbb{R}';
    if (!soll.length) return '\\mathbb{L} = \\{\\,\\}';
    return '\\mathbb{L} = \\{' + soll.slice().sort(function(a, b){ return a - b; }).map(texZahl).join(';\\ ') + '\\}';
  }
  /* Zahl in LaTeX: ganze und Dezimalzahlen direkt, Drittel und Sechstel als Bruch. */
  function texZahl(v){
    if (gl(v, Math.round(v))) return tz(Math.round(v));
    for (var d of [2, 3, 4, 5, 6, 8, 9, 10, 12]){
      var n = Math.round(v * d);
      if (gl(v * d, n)){
        if (d === 2 || d === 4 || d === 5 || d === 8 || d === 10) return tz(Math.round(v * 1000) / 1000);
        return (n < 0 ? '-' : '') + '\\tfrac{' + Math.abs(n) + '}{' + d + '}';
      }
    }
    return tz(Math.round(v * 1000) / 1000);
  }
  function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }

  /* ---------- Koordinatensystem (wie in den anderen Leitprogrammen) ---------- */
  function Achsen(svg, o){
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1;
    var id = 'k' + Math.random().toString(36).slice(2, 8);
    function X(x){ return (x - x0) / (x1 - x0) * W; }
    function Y(y){ return H - (y - y0) / (y1 - y0) * H; }
    var g = el(svg, 'g', {});
    var cp = el(g, 'clipPath', { id: id }); el(cp, 'rect', { x: 0, y: 0, width: W, height: H });
    var sx = o.sx || 1, sy = o.sy || 1, i;
    for (i = Math.ceil(x0 / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    if (y0 <= 0 && y1 >= 0) el(g, 'line', { x1: 0, y1: Y(0), x2: W, y2: Y(0), 'class': 'achse' });
    if (x0 <= 0 && x1 >= 0) el(g, 'line', { x1: X(0), y1: 0, x2: X(0), y2: H, 'class': 'achse' });
    var pf = o.pfeil || 7, namen = [];
    if (y0 <= 0 && y1 >= 0){
      el(g, 'polygon', { points: W + ',' + Y(0) + ' ' + (W - pf) + ',' + (Y(0) - pf / 2) + ' ' + (W - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
      namen.push([W - 3, Y(0) - pf, 'end', o.xname || 'x']);
    }
    if (x0 <= 0 && x1 >= 0){
      el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
      namen.push([X(0) + pf, pf + 3, 'start', o.yname || 'y']);
    }
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(Math.max(0, y0)) + 13, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(Math.max(0, x0)) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    var ebene = el(svg, 'g', {}), schilder = el(svg, 'g', {});
    namen.forEach(function(n){ el(schilder, 'text', { x: n[0], y: n[1], 'text-anchor': n[2], 'class': 'achsname' }, n[3]); });
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      kurve: function(f, cls){
        var d = '', an = false, Hh = y1 - y0;
        for (var k = 0; k <= 400; k++){
          var x = x0 + (x1 - x0) * k / 400, y = f(x);
          if (y == null || !isFinite(y)){ an = false; continue; }
          y = Math.max(y0 - 3 * Hh, Math.min(y1 + 3 * Hh, y));
          d += (an ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); an = true;
        }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      }
    };
  }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht immer. */
  function Leiste(fig, aufgaben, sim){
    var box = fig.querySelector('.leiste'); if (!box) return function(){};
    var n = aufgaben.length, i = 0, erledigt = {};
    box.innerHTML = '<span class="ls-nr"></span><span class="ls-text"></span><span class="ls-ok" aria-live="polite"></span><button type="button" class="ls-weiter"></button><button type="button" class="ls-neu" hidden>von vorn</button>';
    var nr = box.querySelector('.ls-nr'), tx = box.querySelector('.ls-text'), ok = box.querySelector('.ls-ok'),
        bt = box.querySelector('.ls-weiter'), bv = box.querySelector('.ls-neu');
    function anzahl(){ var k = 0; for (var j = 0; j < n; j++) if (erledigt[j]) k++; return k; }
    function offen(ab){ for (var j = ab; j < n; j++) if (!erledigt[j]) return j; return n; }
    function zeigen(){
      if (i >= n){
        var k = anzahl();
        ok.textContent = ''; box.classList.remove('geloest');
        if (k === n){ nr.textContent = '✓'; tx.innerHTML = 'Alle ' + n + ' Aufgaben gelöst — weiter mit dem Kontrollclip.'; bt.textContent = 'nochmals'; bv.hidden = true; box.classList.add('fertig'); }
        else { nr.textContent = k + '/' + n; tx.innerHTML = k + ' von ' + n + ' gelöst, ' + (n - k) + ' übersprungen.'; bt.textContent = 'zu den offenen ▶'; bv.hidden = false; box.classList.remove('fertig'); }
        if (sim.ende) sim.ende();
        return;
      }
      box.classList.remove('fertig'); bv.hidden = true;
      nr.textContent = (i + 1) + '/' + n; tx.innerHTML = aufgaben[i].text; setzen(tx);
      if (aufgaben[i].setup) aufgaben[i].setup(sim);
      pruefen();
    }
    function pruefen(){
      if (i >= n) return;
      var gut = !!aufgaben[i].ok(sim.zustand());
      if (gut) erledigt[i] = true;
      ok.textContent = erledigt[i] ? '✓' : '';
      bt.textContent = erledigt[i] ? 'Nächste ▶' : 'überspringen';
      box.classList.toggle('geloest', !!erledigt[i]);
    }
    // Beim Wechsel alles auf den Startwert, sonst erfüllt der Endzustand der vorigen Aufgabe die
    // nächste schon (HOWTO §15).
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; });
      fig.querySelectorAll('.sim-schalter input').forEach(function(inp){ inp.checked = inp.defaultChecked; });
      if (sim.aufraeumen) sim.aufraeumen(); zeigen(); if (sim.zeichnen) sim.zeichnen();
    }
    bt.addEventListener('click', function(){
      if (i >= n){ if (anzahl() === n){ erledigt = {}; gehe(0); } else gehe(offen(0)); }
      else gehe(offen(i + 1));
    });
    bv.addEventListener('click', function(){ erledigt = {}; gehe(0); });
    setTimeout(zeigen, 0);
    return pruefen;
  }

  /* ---------- Umformer: Lösungswege selbst wählen ----------
     Unterschied zur Themenseite («Schrittweise» in 2.2a, Faktorisieren in 2.2b): Dort klickt man
     einen festen Weg durch. Hier wählen die Lernenden jeden Schritt selbst, füllen Lücken und
     geben am Schluss die Lösungsmenge ein; gültige andere Wege führen ebenfalls ans Ziel, Fehler
     bekommen eine eigene Rückmeldung (HOWTO-GleichungLP, Abschnitt 2).

     Eine Aufgabe ist ein kleiner Graph von Knoten:
       { z: 'LaTeX der Zeile', frage: 'Text über den Knöpfen',
         w: [[Knopftext, Ziel | '!Rückmeldung', Umformung, Hinweis], …]   — Schritt wählen
         feld: { muster: 'D = {D}', soll: { D: 49 } | pruef: function(e){ … }, fehler: [[{…}, 'Text']],
                 tipp: 'Text', nach: Ziel }                               — Lücke füllen
         L: [Zahlen] | [] | 'R', probe: 'LaTeX' }                         — Lösungsmenge eingeben
     Die Umformung (z. B. '\\mid -2x') steht wie im Heft rechts neben der Zeile, auf die sie wirkt. */
  function Umformer(fig, aufgaben){
    var verl = fig.querySelector('.uf-verlauf'), frage = fig.querySelector('.uf-frage'), wahl = fig.querySelector('.uf-wahl'),
        rueck = fig.querySelector('.uf-rueck'), zur = fig.querySelector('.uf-zurueck');
    var A = null, pfad = [], ops = [], fertig = false, pruefen = function(){};
    function knoten(id){ return A.k[id]; }
    function zeile(id, op){
      var K = knoten(id);
      return '<div class="uf-zeile"><span class="uf-gl">\\(' + K.z + '\\)</span><span class="uf-op">' + (op ? '\\(' + op + '\\)' : '') + '</span></div>';
    }
    function meldung(cls, html){ rueck.className = 'uf-rueck ' + cls; rueck.innerHTML = html; setzen(rueck); }
    function zeichnen(){
      if (!A){ verl.innerHTML = ''; frage.innerHTML = ''; wahl.innerHTML = ''; return; }
      var html = '', zeilen = [];
      pfad.forEach(function(id, j){ if (knoten(id).z != null) zeilen.push([id, ops[j]]); });
      zeilen.forEach(function(p){ html += zeile(p[0], p[1]); });
      verl.innerHTML = html;
      var K = knoten(pfad[pfad.length - 1]);
      zur.disabled = pfad.length < 2 || fertig;
      if (fertig){
        frage.innerHTML = '';
        wahl.innerHTML = '<div class="uf-loesung">\\(' + mengeTex(K.L) + '\\)</div>' + (K.probe ? '<p class="uf-probe">Probe: \\(' + K.probe + '\\)</p>' : '');
      } else if (K.w){
        frage.innerHTML = K.frage || 'Wähle den nächsten Schritt:';
        wahl.innerHTML = K.w.map(function(o, j){ return '<button type="button" class="uf-knopf" data-j="' + j + '">' + o[0] + '</button>'; }).join('');
        wahl.querySelectorAll('.uf-knopf').forEach(function(b){ b.addEventListener('click', function(){ waehle(+b.dataset.j); }); });
      } else if (K.feld){
        frage.innerHTML = K.frage || 'Fülle die Lücke:';
        wahl.innerHTML = '<span class="uf-feld">' + K.feld.muster.replace(/\{(\w+)\}/g, function(m, f){
          return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">'; })
          + '</span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', feldPruefen);
        wahl.querySelectorAll('input').forEach(function(i){ i.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') feldPruefen(); }); });
      } else if (K.L != null){
        frage.innerHTML = K.frage || 'Gib die Lösungsmenge an — Elemente mit Strichpunkt, leere Menge {}, alle Zahlen R:';
        wahl.innerHTML = '<span class="uf-feld">\\(\\mathbb{L} = \\)<input type="text" class="uf-menge" inputmode="text" autocomplete="off" aria-label="Lösungsmenge" placeholder="{ … }"></span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', mengePruefen);
        wahl.querySelector('input').addEventListener('keydown', function(ev){ if (ev.key === 'Enter') mengePruefen(); });
      }
      setzen(verl); setzen(frage); setzen(wahl);
    }
    function weiter(ziel, op, hinweis){
      ops[pfad.length - 1] = op || '';
      pfad.push(ziel); ops.push('');
      if (hinweis) meldung('hinweis', hinweis); else { rueck.className = 'uf-rueck'; rueck.innerHTML = ''; }
      zeichnen();
    }
    function waehle(j){
      var o = knoten(pfad[pfad.length - 1]).w[j];
      if (typeof o[1] === 'string' && o[1].charAt(0) === '!') return meldung('falsch', o[1].slice(1));
      // '?': eine gültige Umformung, die hier ein Umweg ist — Hinweis (grau), kein Fehler (Prüfung 06.10.2026, M5)
      if (typeof o[1] === 'string' && o[1].charAt(0) === '?') return meldung('hinweis', o[1].slice(1));
      weiter(o[1], o[2], o[3]);
    }
    function feldPruefen(){
      var F = knoten(pfad[pfad.length - 1]).feld, e = {}, leer = false, kaputt = false;
      wahl.querySelectorAll('input').forEach(function(i){ var r = zahl(i.value); e[i.dataset.f] = r.wert; if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; });
      if (leer) return meldung('hinweis', 'Fülle alle Lücken aus.');
      if (kaputt) return meldung('hinweis', 'Zahlen wie <code>-3</code>, <code>0.5</code> oder <code>1/2</code>.');
      var f = F.pruef ? F.pruef(e) : (function(){
        for (var k in F.soll) if (!gl(e[k], F.soll[k])) return 'x';
        return null; })();
      if (f === null) return weiter(F.nach, F.op, F.richtig);
      for (var q = 0; F.fehler && q < F.fehler.length; q++){
        var pass = true; for (var kk in F.fehler[q][0]) if (!gl(e[kk], F.fehler[q][0][kk])) pass = false;
        if (pass) return meldung('falsch', F.fehler[q][1]);
      }
      meldung('falsch', f !== 'x' ? f : (F.tipp || 'Noch nicht. Rechne nach.'));
    }
    function mengePruefen(){
      var K = knoten(pfad[pfad.length - 1]), i = wahl.querySelector('input'), e = menge(i.value);
      if (e.leer) return meldung('hinweis', 'Gib die Lösungsmenge ein, zum Beispiel <code>{2; -1}</code>, <code>{}</code> oder <code>R</code>.');
      if (e.kaputt) return meldung('hinweis', e.xgleich ? 'Gefragt ist die Lösungsmenge, zum Beispiel <code>{3}</code> statt <code>x = 3</code>.' : 'Trenne die Lösungen mit Strichpunkt: <code>{0; 3}</code>. Brüche als <code>1/3</code>.');
      if (mengeGleich(e, K.L)){
        fertig = true; meldung('richtig', '✓ Richtig' + (e.komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + '.'); zeichnen(); pruefen(); return;
      }
      var soll = K.L, t;
      if (K.Lfalsch) for (var q = 0; q < K.Lfalsch.length; q++) if (mengeGleich(e, K.Lfalsch[q][0])) return meldung('falsch', K.Lfalsch[q][1]);
      if (soll === 'R') t = e.werte.length ? 'Die Aussage, die übrig bleibt, ist wahr — für <b>jedes</b> \\(x\\). Schreib <code>R</code>.' : 'Die Aussage ist wahr, nicht falsch: Jede Zahl ist Lösung.';
      else if (!soll.length) t = e.alle ? 'Die Aussage, die übrig bleibt, ist falsch — keine Zahl erfüllt die Gleichung.' : 'Schau auf die letzte Zeile: Gibt es überhaupt eine Zahl, die passt?';
      else if (e.werte.length < soll.length && e.werte.every(function(w){ return soll.some(function(v){ return gl(v, w); }); })) t = 'Es fehlt eine Lösung — schau auf die letzte Zeile: Dort stehen ' + soll.length + '.';
      else t = 'Noch nicht. Lies die Lösungen in der letzten Zeile ab.';
      meldung('falsch', t);
    }
    zur.addEventListener('click', function(){ if (pfad.length > 1 && !fertig){ pfad.pop(); ops.pop(); ops[pfad.length - 1] = ''; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); } });
    return {
      laden: function(a){ A = a; pfad = [a.start || 'a']; ops = ['']; fertig = false; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); },
      leeren: function(){ A = null; pfad = []; ops = []; fertig = false; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); },
      zustand: function(){ return { fertig: fertig, aufgabe: A }; },
      knoten: function(){ return pfad[pfad.length - 1]; },
      setPruefen: function(f){ pruefen = f; }
    };
  }
  /* Eine Umformer-Simulation: Die Leiste lädt Aufgabe für Aufgabe; ✓, sobald die Lösungsmenge stimmt. */
  function umformerSim(id, aufgaben){
    var fig = document.getElementById(id); if (!fig) return;
    var U = Umformer(fig, aufgaben);
    fig.__aufgaben = aufgaben; fig.__U = U;      // Testhaken (Prüfskript des Umformers)
    var sim = { zustand: U.zustand, aufraeumen: function(){}, ende: U.leeren };
    var pr = Leiste(fig, aufgaben.map(function(a){
      return { text: a.text, setup: function(){ U.laden(a); }, ok: function(s){ return s.fertig && s.aufgabe === a; } }; }), sim);
    U.setPruefen(pr);
  }
  var NULL = '!Division durch \\(x\\) setzt \\(x \\neq 0\\) voraus — die Lösung \\(x = 0\\) ginge verloren. Bring zuerst alles auf eine Seite.';
  var ODER = '\\;\\text{ oder }\\;';
  var BETRAG = '!Aus einer Summe oder Differenz darf man nicht gliedweise die Wurzel ziehen. Bring zuerst das Quadrat allein auf eine Seite.';

  /* Zweiklammersatz wie auf der Themenseite 2.2b: gesucht sind die Lösungen x₁, x₂ mit x₁ + x₂ = −p und
     x₁ · x₂ = q; dann ist x² + px + q = (x − x₁)(x − x₂). */
  function zweiklammer(p, q, nach){
    var w = Math.sqrt(p * p - 4 * q);
    return { muster: '\\((x - \\) {m} \\()(x - \\) {n} \\() = 0\\)', nach: nach, beispiel: { m: (-p - w) / 2, n: (-p + w) / 2 },
      pruef: function(e){
        if (gl(e.m + e.n, -p) && gl(e.m * e.n, q)) return null;
        if (gl(e.m * e.n, q) && gl(e.m + e.n, p)) return 'Das Produkt stimmt, die Summe hat das falsche Vorzeichen. Die Lösungen haben die Summe \\(-p = ' + tz(-p) + '\\) und das Produkt \\(q = ' + tz(q) + '\\).';
        if (gl(e.m + e.n, -p)) return 'Die Summe stimmt, das Produkt nicht: \\(' + tz(e.m) + ' \\cdot ' + klamT(e.n) + ' \\neq ' + tz(q) + '\\).';
        return 'Gesucht sind die Lösungen: Summe \\(-p = ' + tz(-p) + '\\), Produkt \\(q = ' + tz(q) + '\\).';
      } };
  }
  function klamT(v){ return v < 0 ? '(' + tz(v) + ')' : tz(v); }

  /* ---------- Kapitel 1: erkennen und Wurzel ziehen ----------
     Startgleichungen sind nicht die Beispiele aus dem Clip (x² = 9, (x − 2)² = 9). */
  umformerSim('sim1', [
    { text: 'Löse \\(3x^2 - 75 = 0\\).', k: {
      a: { z: '3x^2 - 75 = 0', w: [['beidseitig \\(+75\\)', 'b', '\\mid +75'], ['Wurzel ziehen: \\(\\sqrt{3}\\,x - \\sqrt{75} = 0\\)', BETRAG],
        ['beidseitig \\(:3\\)', 'a2', '\\mid :3']] },
      a2: { z: 'x^2 - 25 = 0', w: [['beidseitig \\(+25\\)', 'c', '\\mid +25']] },
      b: { z: '3x^2 = 75', w: [['beidseitig \\(:3\\)', 'c', '\\mid :3'], ['beidseitig \\(-3\\)', '!Dann steht \\(3x^2 - 3\\) da. \\(3x^2\\) heisst \\(3 \\cdot x^2\\): Die Gegenoperation ist \\(:3\\).']] },
      c: { z: 'x^2 = 25', w: [['Wurzel ziehen: \\(x = \\pm 5\\)', 'd'], ['Wurzel ziehen: \\(x = 5\\)', '!Auch \\((-5)^2 = 25\\). Zu \\(x^2 = 25\\) gehören zwei Lösungen.']] },
      d: { z: 'x = -5' + ODER + 'x = 5', L: [-5, 5], Lfalsch: [[[5], 'Es fehlt \\(-5\\): \\((-5)^2 = 25\\).']], probe: '3 \\cdot 25 - 75 = 0' } } },
    { text: 'Löse \\(x^2 + 7 = 3\\).', k: {
      a: { z: 'x^2 + 7 = 3', w: [['beidseitig \\(-7\\)', 'b', '\\mid -7'], ['Wurzel ziehen: \\(x + \\sqrt{7} = \\sqrt{3}\\)', BETRAG]] },
      b: { z: 'x^2 = -4', frage: 'Kann ein Quadrat negativ sein? Gib die Lösungsmenge an:', L: [],
        Lfalsch: [[[-2, 2], 'Prüf: \\(2^2 + 7 = 11\\), nicht \\(3\\). Ein Quadrat ist nie negativ.'], [[2], 'Prüf: \\(2^2 + 7 = 11\\), nicht \\(3\\). Ein Quadrat ist nie negativ.'],
                  ['R', 'Kein \\(x\\) erfüllt \\(x^2 = -4\\) — ein Quadrat ist nie negativ.']] } } },
    { text: 'Löse \\((x - 1)^2 = 25\\).', k: {
      a: { z: '(x - 1)^2 = 25', w: [['Wurzel ziehen: \\(x - 1 = \\pm 5\\)', 'b'], ['Wurzel ziehen: \\(x - 1 = 5\\)', '!Auch \\((-5)^2 = 25\\): Die Klammer kann \\(5\\) oder \\(-5\\) sein.'],
        ['ausmultiplizieren', '?Erlaubt, aber ein Umweg: Links steht schon ein Quadrat. Zieh die Wurzel.']] },
      b: { z: 'x - 1 = 5' + ODER + 'x - 1 = -5', w: [['beidseitig \\(+1\\)', 'c', '\\mid +1'], ['beidseitig \\(-1\\)', '!Die Gegenoperation zu \\(-1\\) ist \\(+1\\).']] },
      c: { z: 'x = 6' + ODER + 'x = -4', L: [6, -4], Lfalsch: [[[4, -6], 'Vorzeichen: Zu beiden Seiten \\(1\\) addieren: \\(5 + 1\\) und \\(-5 + 1\\).'], [[6], 'Es fehlt die Lösung aus \\(x - 1 = -5\\).']],
        probe: '(6 - 1)^2 = 25;\\ \\ (-4 - 1)^2 = 25' } } },
    { text: 'Löse \\(4x^2 = 9\\).', k: {
      a: { z: '4x^2 = 9', w: [['beidseitig \\(:4\\)', 'b', '\\mid :4'], ['Wurzel ziehen: \\(2x = \\pm 3\\)', 'b2'],
        ['Wurzel ziehen: \\(4x = \\pm 3\\)', '!\\(\\sqrt{4x^2} = 2x\\), denn \\((2x)^2 = 4x^2\\).']] },
      b: { z: 'x^2 = \\tfrac{9}{4}', w: [['Wurzel ziehen: \\(x = \\pm\\tfrac{3}{2}\\)', 'c'], ['Wurzel ziehen: \\(x = \\pm\\tfrac{3}{4}\\)', '!Die Wurzel gilt für Zähler und Nenner: \\(\\sqrt{4} = 2\\).'],
        ['Wurzel ziehen: \\(x = \\pm\\tfrac{9}{2}\\)', '!Auch aus dem Zähler die Wurzel ziehen: \\(\\sqrt{9} = 3\\).']] },
      b2: { z: '2x = 3' + ODER + '2x = -3', w: [['beidseitig \\(:2\\)', 'c', '\\mid :2']] },
      c: { z: 'x = 1.5' + ODER + 'x = -1.5', L: [1.5, -1.5], Lfalsch: [[[1.5], 'Es fehlt \\(-1.5\\).']], probe: '4 \\cdot 2.25 = 9' } } },
    { text: 'Löse \\(2(x + 4)^2 - 50 = 0\\).', k: {
      a: { z: '2(x + 4)^2 - 50 = 0', w: [['beidseitig \\(+50\\)', 'b', '\\mid +50'], ['beidseitig \\(:2\\)', 'a2', '\\mid :2'],
        ['Klammer ausmultiplizieren', '?Erlaubt, gibt aber \\(2x^2 + 16x - 18 = 0\\) — eine Gleichung mit allen drei Gliedern. Einfacher: das Quadrat allein auf eine Seite bringen.']] },
      a2: { z: '(x + 4)^2 - 25 = 0', w: [['beidseitig \\(+25\\)', 'c', '\\mid +25']] },
      b: { z: '2(x + 4)^2 = 50', w: [['beidseitig \\(:2\\)', 'c', '\\mid :2'], ['Wurzel ziehen: \\(2(x + 4) = \\pm\\sqrt{50}\\)', '!Die \\(2\\) steht vor dem Quadrat, nicht darin. Teile zuerst durch \\(2\\).']] },
      c: { z: '(x + 4)^2 = 25', w: [['Wurzel ziehen: \\(x + 4 = \\pm 5\\)', 'd'], ['Wurzel ziehen: \\(x + 4 = 5\\)', '!Auch \\((-5)^2 = 25\\).']] },
      d: { z: 'x + 4 = 5' + ODER + 'x + 4 = -5', w: [['beidseitig \\(-4\\)', 'e', '\\mid -4']] },
      e: { z: 'x = 1' + ODER + 'x = -9', L: [1, -9], Lfalsch: [[[-1, 9], 'Vorzeichen: \\(5 - 4 = 1\\) und \\(-5 - 4 = -9\\).'], [[1], 'Es fehlt die Lösung aus \\(x + 4 = -5\\).']],
        probe: '2 \\cdot (1 + 4)^2 - 50 = 0;\\ \\ 2 \\cdot (-9 + 4)^2 - 50 = 0' } } },
    { text: 'Löse \\((x + 2)^2 = 0\\).', k: {
      a: { z: '(x + 2)^2 = 0', w: [['Wurzel ziehen: \\(x + 2 = 0\\)', 'b'], ['Wurzel ziehen: \\(x + 2 = \\pm 2\\)', '!Rechts steht \\(0\\), und \\(\\sqrt{0} = 0\\). Die Klammer selbst muss null sein.'],
        ['ausmultiplizieren', '?Erlaubt, aber ein Umweg: Ein Quadrat ist null, wenn die Klammer null ist.']] },
      b: { z: 'x + 2 = 0', w: [['beidseitig \\(-2\\)', 'c', '\\mid -2']] },
      c: { z: 'x = -2', frage: 'Nur eine Lösung. Gib die Lösungsmenge an:', L: [-2], Lfalsch: [[[2], 'Vorzeichen: \\(x + 2 = 0\\) gibt \\(x = -2\\).'], [[-2, 2], 'Prüf \\(x = 2\\): \\((2 + 2)^2 = 16\\), nicht \\(0\\).']] } } }
  ]);

  /* ---------- Kapitel 2: ausklammern und faktorisieren ---------- */
  umformerSim('sim2', [
    { text: 'Löse \\(2x^2 = 7x\\).', k: {
      a: { z: '2x^2 = 7x', w: [['beidseitig \\(-7x\\) (auf null bringen)', 'b', '\\mid -7x'], ['beidseitig \\(:x\\)', NULL],
        ['Fallunterscheidung: erst \\(x = 0\\) prüfen, dann \\(x \\neq 0\\)', 'f']] },
      b: { z: '2x^2 - 7x = 0', w: [['\\(x\\) ausklammern', 'c'],
        ['nur \\(2\\) ausklammern', '?\\(2(x^2 - 3.5x) = 0\\) stimmt, ist aber noch kein Produkt mit einem \\(x\\)-Faktor. Klammere das \\(x\\) aus.']] },
      c: { feld: { muster: '\\(x\\,(2x - \\) {a} \\() = 0\\)', soll: { a: 7 }, nach: 'd', fehler: [[{ a: -7 }, 'Mit \\(-7\\) in der Lücke stünde \\(2x + 7\\) in der Klammer, und \\(x \\cdot 7 = +7x\\). Gesucht ist \\(-7x\\).']],
        tipp: 'Kontrolle durch Ausmultiplizieren: \\(x \\cdot 2x = 2x^2\\), und \\(x\\) mal die Zahl muss \\(-7x\\) geben.' } },
      d: { z: 'x\\,(2x - 7) = 0', w: [['Nullprodukt: \\(x = 0\\) oder \\(2x - 7 = 0\\)', 'e'],
        ['Nullprodukt: \\(x = 0\\) und \\(2x - 7 = 0\\)', '!«und» hiesse: beide Faktoren gleichzeitig null — das schafft kein \\(x\\). Ein Faktor null genügt: «oder».']] },
      e: { z: 'x = 0' + ODER + '2x - 7 = 0', w: [['\\(2x - 7 = 0\\) lösen: \\(x = 3.5\\)', 'g'], ['\\(2x - 7 = 0\\) lösen: \\(x = -3.5\\)', '!\\(2x - 7 = 0 \\mid +7\\) gibt \\(2x = 7\\), dann \\(:2\\).']] },
      g: { z: 'x = 0' + ODER + 'x = 3.5', L: [0, 3.5], Lfalsch: [[[3.5], 'Es fehlt \\(x = 0\\) — auch der Faktor \\(x\\) kann null sein.']], probe: '2 \\cdot 3.5^2 = 24.5 = 7 \\cdot 3.5' },
      f: { z: '\\text{Fall } x = 0{:}\\ \\ 2 \\cdot 0^2 = 7 \\cdot 0\\ \\checkmark', w: [['Fall \\(x \\neq 0\\): beidseitig \\(:x\\)', 'f2', '\\mid :x \\ (x \\neq 0)']] },
      f2: { z: '2x = 7', w: [['beidseitig \\(:2\\)', 'f3', '\\mid :2']] },
      f3: { z: 'x = 3.5', frage: 'Zusammen mit dem Fall \\(x = 0\\): Gib die Lösungsmenge an.', L: [0, 3.5],
        Lfalsch: [[[3.5], 'Der Fall \\(x = 0\\) hat schon eine Lösung geliefert — sie gehört dazu.']] } } },
    { text: 'Löse \\(x^2 + 8x + 16 = 0\\).', k: {
      a: { z: 'x^2 + 8x + 16 = 0', frage: 'Erkennst du ein Binom?', w: [['Binom: \\((x + 4)^2 = 0\\)', 'b'], ['Binom: \\((x + 8)^2 = 0\\)', '!\\((x + 8)^2 = x^2 + 16x + 64\\). Gesucht: \\(2 \\cdot 4 = 8\\) und \\(4^2 = 16\\).'],
        ['Binom: \\((x - 4)^2 = 0\\)', '!\\((x - 4)^2 = x^2 - 8x + 16\\). Hier steht \\(+8x\\).'], ['Zweiklammersatz', 'z']] },
      z: { frage: 'Die Lösungen haben die Summe \\(-8\\) und das Produkt \\(16\\):', feld: zweiklammer(8, 16, 'z2') },
      z2: { z: '(x + 4)(x + 4) = 0', w: [['Nullprodukt: \\(x + 4 = 0\\)', 'c']] },
      b: { z: '(x + 4)^2 = 0', w: [['\\(x + 4 = 0\\)', 'c']] },
      c: { z: 'x = -4', frage: 'Nur eine Lösung — eine doppelte. Gib die Lösungsmenge an:', L: [-4], Lfalsch: [[[4], 'Vorzeichen: \\(x + 4 = 0\\) gibt \\(x = -4\\).']], probe: '16 - 32 + 16 = 0' } } },
    { text: 'Löse \\(x^2 - 2x - 15 = 0\\) mit dem Zweiklammersatz.', k: {
      a: { z: 'x^2 - 2x - 15 = 0', frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(2\\) und das Produkt \\(-15\\):', feld: zweiklammer(-2, -15, 'b') },
      b: { z: '(x + 3)(x - 5) = 0', w: [['Nullprodukt: \\(x + 3 = 0\\) oder \\(x - 5 = 0\\)', 'c']] },
      c: { z: 'x = -3' + ODER + 'x = 5', L: [-3, 5], Lfalsch: [[[3, -5], 'Vorzeichen: \\(x + 3 = 0\\) gibt \\(x = -3\\).']], probe: '9 + 6 - 15 = 0;\\ \\ 25 - 10 - 15 = 0' } } },
    { text: 'Löse \\(x^2 - 36 = 0\\).', k: {
      a: { z: 'x^2 - 36 = 0', w: [['Binom: \\((x - 6)(x + 6) = 0\\)', 'b'], ['beidseitig \\(+36\\)', 'b2', '\\mid +36'],
        ['Binom: \\((x - 6)^2 = 0\\)', '!\\((x - 6)^2 = x^2 - 12x + 36\\). Hier fehlt das Glied mit \\(x\\): \\(a^2 - b^2 = (a - b)(a + b)\\).'],
        ['\\(x\\) ausklammern', '!Die \\(36\\) enthält kein \\(x\\) — ausklammern geht nicht.']] },
      b: { z: '(x - 6)(x + 6) = 0', w: [['Nullprodukt: \\(x - 6 = 0\\) oder \\(x + 6 = 0\\)', 'c']] },
      b2: { z: 'x^2 = 36', w: [['Wurzel ziehen: \\(x = \\pm 6\\)', 'c']] },
      c: { z: 'x = 6' + ODER + 'x = -6', L: [6, -6], Lfalsch: [[[6], 'Es fehlt \\(-6\\).']] } } },
    { text: 'Löse \\((x - 3)(x + 5) = 0\\).', k: {
      a: { z: '(x - 3)(x + 5) = 0', w: [['Nullprodukt: \\(x - 3 = 0\\) oder \\(x + 5 = 0\\)', 'b'],
        ['ausmultiplizieren: \\(x^2 + 2x - 15 = 0\\)', '?Erlaubt, aber ein Umweg: Das Produkt steht schon da, und rechts steht \\(0\\). Nutze den Satz vom Nullprodukt.'],
        ['Nullprodukt: \\(x - 3 = 0\\) und \\(x + 5 = 0\\)', '!Ein Faktor null genügt: «oder».']] },
      b: { z: 'x = 3' + ODER + 'x = -5', L: [3, -5], Lfalsch: [[[-3, 5], 'Vorzeichen: \\(x - 3 = 0\\) gibt \\(x = 3\\), \\(x + 5 = 0\\) gibt \\(x = -5\\).']] } } },
    { text: 'Löse \\(x^2 + 10x + 21 = 0\\) mit dem Zweiklammersatz.', k: {
      a: { z: 'x^2 + 10x + 21 = 0', frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(-10\\) und das Produkt \\(21\\):', feld: zweiklammer(10, 21, 'b') },
      b: { z: '(x + 3)(x + 7) = 0', w: [['Nullprodukt: \\(x + 3 = 0\\) oder \\(x + 7 = 0\\)', 'c']] },
      c: { z: 'x = -3' + ODER + 'x = -7', L: [-3, -7], Lfalsch: [[[3, 7], 'Vorzeichen: \\(x + 3 = 0\\) gibt \\(x = -3\\).']], probe: '9 - 30 + 21 = 0;\\ \\ 49 - 70 + 21 = 0' } } }
  ]);

  /* ---------- Kapitel 3: quadratisch ergänzen und Mitternachtsformel ---------- */
  function ergaenzFeld(soll, b, nach, op){
    return { muster: 'beidseitig \\(+\\) {e}', soll: { e: soll }, nach: nach, op: op,
      fehler: [[{ e: b * b }, 'Ergänzt wird das Quadrat der <b>halben</b> Zahl vor \\(x\\): \\(\\left(\\tfrac{' + Math.abs(b) + '}{2}\\right)^2\\).'],
               [{ e: Math.abs(b) / 2 }, 'Die halbe Zahl vor \\(x\\) noch <b>quadrieren</b>.'], [{ e: Math.abs(b) }, 'Ergänzt wird \\(\\left(\\tfrac{' + Math.abs(b) + '}{2}\\right)^2\\).']],
      tipp: 'Die halbe Zahl vor \\(x\\), im Quadrat.' };
  }
  umformerSim('sim3', [
    { text: 'Löse \\(x^2 - 10x + 21 = 0\\) mit quadratischer Ergänzung.', k: {
      a: { z: 'x^2 - 10x + 21 = 0', w: [['beidseitig \\(-21\\)', 'b', '\\mid -21'],
        ['gleich hier ergänzen: beidseitig \\(+25\\)', '?Erlaubt: \\((x - 5)^2 + 21 = 25\\). Einfacher: zuerst die Zahl ohne \\(x\\) nach rechts — dann steht links ein reines Binom.']] },
      b: { z: 'x^2 - 10x = -21', frage: 'Welche Zahl ergänzt links zu einem Binom?', feld: ergaenzFeld(25, -10, 'c', '\\mid +25') },
      c: { z: 'x^2 - 10x + 25 = 4', w: [['links Binom: \\((x - 5)^2 = 4\\)', 'd'], ['links Binom: \\((x + 5)^2 = 4\\)', '!\\((x + 5)^2 = x^2 + 10x + 25\\). Hier steht \\(-10x\\).']] },
      d: { z: '(x - 5)^2 = 4', w: [['Wurzel ziehen: \\(x - 5 = \\pm 2\\)', 'e'], ['Wurzel ziehen: \\(x - 5 = 2\\)', '!Auch \\(-2\\) hat das Quadrat \\(4\\).']] },
      e: { z: 'x - 5 = 2' + ODER + 'x - 5 = -2', w: [['beidseitig \\(+5\\)', 'f', '\\mid +5']] },
      f: { z: 'x = 7' + ODER + 'x = 3', L: [7, 3], probe: '49 - 70 + 21 = 0;\\ \\ 9 - 30 + 21 = 0' } } },
    { text: 'Löse \\(2x^2 + 12x + 10 = 0\\) mit quadratischer Ergänzung.', k: {
      a: { z: '2x^2 + 12x + 10 = 0', w: [['beidseitig \\(:2\\)', 'b', '\\mid :2'],
        ['gleich ergänzen: beidseitig \\(+36\\)', '!Die Ergänzung braucht den Faktor \\(1\\) vor \\(x^2\\). Teile zuerst durch \\(2\\).']] },
      b: { z: 'x^2 + 6x + 5 = 0', w: [['beidseitig \\(-5\\)', 'c', '\\mid -5']] },
      c: { z: 'x^2 + 6x = -5', frage: 'Welche Zahl ergänzt links zu einem Binom?', feld: ergaenzFeld(9, 6, 'd', '\\mid +9') },
      d: { z: 'x^2 + 6x + 9 = 4', w: [['links Binom: \\((x + 3)^2 = 4\\)', 'e'], ['links Binom: \\((x + 9)^2 = 4\\)', '!\\((x + 9)^2 = x^2 + 18x + 81\\). Gesucht ist \\((x + 3)^2 = x^2 + 6x + 9\\).']] },
      e: { z: '(x + 3)^2 = 4', w: [['Wurzel ziehen: \\(x + 3 = \\pm 2\\)', 'f']] },
      f: { z: 'x + 3 = 2' + ODER + 'x + 3 = -2', w: [['beidseitig \\(-3\\)', 'g', '\\mid -3']] },
      g: { z: 'x = -1' + ODER + 'x = -5', L: [-1, -5], Lfalsch: [[[1, 5], 'Vorzeichen: \\(2 - 3 = -1\\) und \\(-2 - 3 = -5\\).']], probe: '2 - 12 + 10 = 0;\\ \\ 50 - 60 + 10 = 0' } } },
    { text: 'Löse \\(3x^2 + 5x - 2 = 0\\) mit der Mitternachtsformel.', k: {
      a: { z: '3x^2 + 5x - 2 = 0', frage: 'Lies die Koeffizienten ab — samt Vorzeichen:', feld: { muster: '\\(a = \\) {a}; \\(b = \\) {b}; \\(c = \\) {c}', soll: { a: 3, b: 5, c: -2 }, nach: 'b',
        fehler: [[{ a: 3, b: 5, c: 2 }, 'Vorzeichen von \\(c\\): Vor der \\(2\\) steht ein Minus, \\(c = -2\\).']], tipp: '\\(a\\) steht vor \\(x^2\\), \\(b\\) vor \\(x\\), \\(c\\) ist die Zahl ohne \\(x\\).' } },
      b: { z: 'a = 3,\\ b = 5,\\ c = -2', frage: 'Berechne die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: 49 }, nach: 'c',
        fehler: [[{ D: 1 }, 'Vorzeichen: \\(-4 \\cdot 3 \\cdot (-2) = +24\\), also \\(D = 25 + 24\\).']], tipp: '\\(D = 5^2 - 4 \\cdot 3 \\cdot (-2)\\).' } },
      c: { z: 'D = 49,\\ \\sqrt{D} = 7', w: [['einsetzen: \\(x = \\dfrac{-5 \\pm 7}{6}\\)', 'd'], ['einsetzen: \\(x = \\dfrac{5 \\pm 7}{6}\\)', '!Vorne steht \\(-b\\), und \\(b = 5\\): \\(-b = -5\\).'],
        ['einsetzen: \\(x = \\dfrac{-5 \\pm 7}{3}\\)', '!Der Nenner ist \\(2a = 6\\).']] },
      d: { z: 'x = \\tfrac{2}{6} = \\tfrac{1}{3}' + ODER + 'x = \\tfrac{-12}{6} = -2', L: [1 / 3, -2], probe: '\\tfrac{1}{3} + \\tfrac{5}{3} - 2 = 0;\\ \\ 12 - 10 - 2 = 0' } } },
    { text: 'Löse \\(x^2 - 3x + 4 = 0\\) mit der Mitternachtsformel.', k: {
      a: { z: 'x^2 - 3x + 4 = 0', frage: 'Berechne zuerst die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: -7 }, nach: 'b',
        fehler: [[{ D: 25 }, '\\(4ac = 4 \\cdot 1 \\cdot 4 = 16\\) wird <b>abgezogen</b>: \\(D = 9 - 16\\).'], [{ D: 7 }, 'Vorzeichen: \\(9 - 16 = -7\\).'], [{ D: -25 }, '\\(b^2 = (-3)^2 = +9\\).']], tipp: '\\(D = (-3)^2 - 4 \\cdot 1 \\cdot 4\\).' } },
      b: { z: 'D = 9 - 16 = -7 \\lt 0', frage: 'Was folgt aus \\(D \\lt 0\\)? Gib die Lösungsmenge an:', L: [],
        Lfalsch: [['R', 'Bei \\(D \\lt 0\\) gibt es keine reelle Wurzel aus \\(D\\) — also keine Lösung, nicht alle Zahlen.']] } } },
    { text: 'Löse \\(4x^2 + 4x + 1 = 0\\).', k: {
      a: { z: '4x^2 + 4x + 1 = 0', w: [['Mitternachtsformel', 'b'], ['Binom erkennen: \\((2x + 1)^2 = 0\\)', 'c'], ['Binom erkennen: \\((4x + 1)^2 = 0\\)', '!\\((4x + 1)^2 = 16x^2 + 8x + 1\\). Vorne steht \\(4x^2 = (2x)^2\\).']] },
      b: { frage: 'Berechne die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: 0 }, nach: 'b2', fehler: [[{ D: 32 }, '\\(4ac = 16\\) wird abgezogen: \\(D = 16 - 16\\).']], tipp: '\\(D = 4^2 - 4 \\cdot 4 \\cdot 1\\).' } },
      b2: { z: 'D = 16 - 16 = 0', w: [['einsetzen: \\(x = \\dfrac{-4 \\pm 0}{8}\\)', 'd'], ['einsetzen: \\(x = \\dfrac{4 \\pm 0}{8}\\)', '!Vorne steht \\(-b = -4\\).']] },
      c: { z: '(2x + 1)^2 = 0', w: [['\\(2x + 1 = 0\\)', 'c2']] },
      c2: { z: '2x + 1 = 0', w: [['beidseitig \\(-1\\), dann \\(:2\\)', 'd', '\\mid -1;\\ :2']] },
      d: { z: 'x = -0.5', frage: 'Nur eine Lösung — eine doppelte. Gib die Lösungsmenge an:', L: [-0.5], Lfalsch: [[[0.5], 'Vorzeichen: \\(-\\tfrac{4}{8} = -0.5\\).']], probe: '1 - 2 + 1 = 0' } } },
    { text: 'Löse \\(-x^2 + 3x + 4 = 0\\) mit der Mitternachtsformel.', k: {
      a: { z: '-x^2 + 3x + 4 = 0', frage: 'Lies die Koeffizienten ab — samt Vorzeichen:', feld: { muster: '\\(a = \\) {a}; \\(b = \\) {b}; \\(c = \\) {c}', soll: { a: -1, b: 3, c: 4 }, nach: 'b',
        fehler: [[{ a: 1, b: 3, c: 4 }, 'Vor \\(x^2\\) steht ein Minus: \\(a = -1\\).']], tipp: 'Vor \\(x^2\\) steht \\(-1\\).' } },
      b: { z: 'a = -1,\\ b = 3,\\ c = 4', frage: 'Berechne die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: 25 }, nach: 'c',
        fehler: [[{ D: -7 }, 'Vorzeichen: \\(-4 \\cdot (-1) \\cdot 4 = +16\\), also \\(D = 9 + 16\\).']], tipp: '\\(D = 3^2 - 4 \\cdot (-1) \\cdot 4\\).' } },
      c: { z: 'D = 25,\\ \\sqrt{D} = 5', w: [['einsetzen: \\(x = \\dfrac{-3 \\pm 5}{-2}\\)', 'd'], ['einsetzen: \\(x = \\dfrac{-3 \\pm 5}{2}\\)', '!Der Nenner ist \\(2a = 2 \\cdot (-1) = -2\\).']] },
      d: { z: 'x = \\tfrac{2}{-2} = -1' + ODER + 'x = \\tfrac{-8}{-2} = 4', L: [-1, 4], Lfalsch: [[[1, -4], 'Vorzeichen: Durch \\(-2\\) teilen dreht das Vorzeichen.']], probe: '-1 - 3 + 4 = 0;\\ \\ -16 + 12 + 4 = 0' } } }
  ]);

  /* ---------- Kapitel 4: das passende Verfahren ---------- */
  umformerSim('sim4', [
    { text: 'Löse \\(x^2 - 11x + 30 = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: 'x^2 - 11x + 30 = 0', frage: 'Welches Verfahren?', w: [['Faktorisieren (Zweiklammersatz)', 'b'],
        ['Mitternachtsformel', 'm', '', 'Geht immer. Hier hätte auch der Zweiklammersatz gereicht: zwei Lösungen mit Summe \\(11\\) und Produkt \\(30\\).'],
        ['Ausklammern', '!Ausklammern hilft, wenn jedes Glied ein \\(x\\) hat. Hier steht \\(+30\\).'], ['Wurzelziehen', '!Wurzelziehen geht, wenn das Glied mit \\(x\\) fehlt. Hier steht \\(-11x\\).']] },
      b: { frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(11\\) und das Produkt \\(30\\):', feld: zweiklammer(-11, 30, 'c') },
      c: { z: '(x - 5)(x - 6) = 0', w: [['Nullprodukt', 'd']] },
      m: { frage: 'Diskriminante:', feld: { muster: '\\(D = \\) {D}', soll: { D: 1 }, nach: 'm2', tipp: '\\(D = (-11)^2 - 4 \\cdot 1 \\cdot 30\\).' } },
      m2: { z: 'D = 121 - 120 = 1', w: [['einsetzen: \\(x = \\dfrac{11 \\pm 1}{2}\\)', 'd']] },
      d: { z: 'x = 5' + ODER + 'x = 6', L: [5, 6], Lfalsch: [[[-5, -6], 'Vorzeichen: \\(x - 5 = 0\\) gibt \\(x = 5\\).']] } } },
    { text: 'Löse \\(2x^2 = 98\\). Wähle zuerst das Verfahren.', k: {
      a: { z: '2x^2 = 98', frage: 'Welches Verfahren?', w: [['Wurzelziehen', 'c', '\\mid :2'],
        ['Ausklammern', '?Geht nach dem Ordnen: \\(2x^2 - 98 = 2(x^2 - 49) = 2(x - 7)(x + 7)\\). Schneller: nach \\(x^2\\) auflösen und die Wurzel ziehen.'],
        ['Mitternachtsformel', 'm', '', 'Geht, mit \\(b = 0\\). Schneller: nach \\(x^2\\) auflösen und die Wurzel ziehen.']] },
      c: { z: 'x^2 = 49', w: [['Wurzel ziehen: \\(x = \\pm 7\\)', 'd'], ['Wurzel ziehen: \\(x = 7\\)', '!Auch \\((-7)^2 = 49\\).']] },
      m: { z: '2x^2 - 98 = 0', frage: 'Diskriminante (\\(b = 0\\)):', feld: { muster: '\\(D = \\) {D}', soll: { D: 784 }, nach: 'm2', tipp: '\\(D = 0^2 - 4 \\cdot 2 \\cdot (-98)\\).' } },
      m2: { z: 'D = 784,\\ \\sqrt{D} = 28', w: [['einsetzen: \\(x = \\dfrac{0 \\pm 28}{4}\\)', 'd']] },
      d: { z: 'x = -7' + ODER + 'x = 7', L: [-7, 7], Lfalsch: [[[7], 'Es fehlt \\(-7\\).']] } } },
    { text: 'Löse \\((x + 2)^2 = x^2 + 16\\).', k: {
      a: { z: '(x + 2)^2 = x^2 + 16', frage: 'Erst ordnen, dann den Typ bestimmen:', w: [['Binom ausmultiplizieren: \\(x^2 + 4x + 4 = x^2 + 16\\)', 'b'],
        ['Binom ausmultiplizieren: \\(x^2 + 4 = x^2 + 16\\)', '!\\((x + 2)^2 = x^2 + 4x + 4\\) — das mittlere Glied \\(4x\\) fehlt.'],
        ['Wurzel ziehen: \\(x + 2 = \\pm\\sqrt{x^2 + 16}\\)', '?Erlaubt — aber rechts steht noch \\(x\\) unter der Wurzel, so kommst du nicht weiter. Multipliziere aus und schau, was übrig bleibt.']] },
      b: { z: 'x^2 + 4x + 4 = x^2 + 16', w: [['beidseitig \\(-x^2\\)', 'c', '\\mid -x^2']] },
      c: { z: '4x + 4 = 16', frage: 'Was für eine Gleichung ist das jetzt?', w: [['linear — weiter mit \\(-4\\)', 'd', '\\mid -4'], ['quadratisch — Mitternachtsformel', '!\\(x^2\\) hat sich weggehoben: Die Gleichung ist linear.']] },
      d: { z: '4x = 12', w: [['beidseitig \\(:4\\)', 'e', '\\mid :4']] },
      e: { z: 'x = 3', L: [3], Lfalsch: [[[-3], 'Vorzeichen: \\(12 : 4 = 3\\).']], probe: '(3 + 2)^2 = 25 = 9 + 16' } } },
    { text: 'Löse \\(x\\,(x - 3) = 10\\).', k: {
      a: { z: 'x\\,(x - 3) = 10', w: [['Nullprodukt: \\(x = 10\\) oder \\(x - 3 = 10\\)', '!Rechts steht \\(10\\), nicht \\(0\\). Der Satz vom Nullprodukt gilt nur, wenn das Produkt null ist.'],
        ['ausmultiplizieren und auf null bringen', 'b', '\\mid -10']] },
      b: { z: 'x^2 - 3x - 10 = 0', frage: 'Welches Verfahren?', w: [['Faktorisieren (Zweiklammersatz)', 'c'], ['Mitternachtsformel', 'm']] },
      c: { frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(3\\) und das Produkt \\(-10\\):', feld: zweiklammer(-3, -10, 'd') },
      d: { z: '(x - 5)(x + 2) = 0', w: [['Nullprodukt', 'e']] },
      m: { feld: { muster: '\\(D = \\) {D}', soll: { D: 49 }, nach: 'm2', tipp: '\\(D = (-3)^2 - 4 \\cdot 1 \\cdot (-10)\\).', fehler: [[{ D: -31 }, '\\(-4 \\cdot 1 \\cdot (-10) = +40\\).']] } },
      m2: { z: 'D = 9 + 40 = 49', w: [['einsetzen: \\(x = \\dfrac{3 \\pm 7}{2}\\)', 'e']] },
      e: { z: 'x = 5' + ODER + 'x = -2', L: [5, -2], Lfalsch: [[[-5, 2], 'Vorzeichen: \\(x - 5 = 0\\) gibt \\(x = 5\\).']], probe: '5 \\cdot 2 = 10;\\ \\ -2 \\cdot (-5) = 10' } } },
    { text: 'Löse \\(5x^2 - 3x - 2 = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: '5x^2 - 3x - 2 = 0', frage: 'Welches Verfahren?', w: [['Mitternachtsformel', 'b'],
        ['Faktorisieren', '?Möglich ist es: \\((5x + 2)(x - 1) = 0\\). Aber vor \\(x^2\\) steht \\(5\\), der Zweiklammersatz greift nicht, und eine solche Zerlegung findet man schwer — die Formel ist der sichere Weg.'],
        ['Wurzelziehen', '!Hier steht ein Glied mit \\(x\\). Wurzelziehen allein reicht nicht.']] },
      b: { feld: { muster: '\\(a = \\) {a}; \\(b = \\) {b}; \\(c = \\) {c}', soll: { a: 5, b: -3, c: -2 }, nach: 'c', fehler: [[{ a: 5, b: 3, c: -2 }, 'Vorzeichen von \\(b\\): \\(b = -3\\).']], tipp: '\\(b\\) steht vor \\(x\\), \\(c\\) ist die Zahl ohne \\(x\\).' } },
      c: { z: 'a = 5,\\ b = -3,\\ c = -2', feld: { muster: '\\(D = \\) {D}', soll: { D: 49 }, nach: 'd', fehler: [[{ D: -31 }, '\\(-4 \\cdot 5 \\cdot (-2) = +40\\).']], tipp: '\\(D = (-3)^2 - 4 \\cdot 5 \\cdot (-2)\\).' } },
      d: { z: 'D = 49', w: [['einsetzen: \\(x = \\dfrac{3 \\pm 7}{10}\\)', 'e'], ['einsetzen: \\(x = \\dfrac{3 \\pm 7}{5}\\)', '!Der Nenner ist \\(2a = 10\\).'], ['einsetzen: \\(x = \\dfrac{-3 \\pm 7}{10}\\)', '!Vorne steht \\(-b\\), und \\(b = -3\\).']] },
      e: { z: 'x = \\tfrac{10}{10} = 1' + ODER + 'x = \\tfrac{-4}{10} = -0.4', L: [1, -0.4], probe: '5 - 3 - 2 = 0;\\ \\ 0.8 + 1.2 - 2 = 0' } } },
    { text: 'Löse \\(2x^2 + 6x = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: '2x^2 + 6x = 0', frage: 'Welches Verfahren?', w: [['Ausklammern', 'b'],
        ['Mitternachtsformel', 'm', '', 'Geht, mit \\(c = 0\\). Schneller: \\(x\\) ausklammern.'],
        ['Wurzelziehen', '!Hier steht ein Glied mit \\(x\\): \\(6x\\). Wurzelziehen allein reicht nicht.'], ['beidseitig \\(:x\\)', NULL]] },
      b: { feld: { muster: '\\(2x\\,(x + \\) {a} \\() = 0\\)', soll: { a: 3 }, nach: 'c', fehler: [[{ a: -3 }, 'Kontrolle: \\(2x \\cdot (-3) = -6x\\), gesucht ist \\(+6x\\).'], [{ a: 6 }, '\\(2x \\cdot 6 = 12x\\). Gesucht ist \\(6x\\).']], tipp: '\\(2x\\) mal die Zahl muss \\(6x\\) geben.' } },
      c: { z: '2x\\,(x + 3) = 0', w: [['Nullprodukt: \\(2x = 0\\) oder \\(x + 3 = 0\\)', 'd']] },
      m: { feld: { muster: '\\(D = \\) {D}', soll: { D: 36 }, nach: 'm2', tipp: '\\(D = 6^2 - 4 \\cdot 2 \\cdot 0\\).' } },
      m2: { z: 'D = 36', w: [['einsetzen: \\(x = \\dfrac{-6 \\pm 6}{4}\\)', 'd']] },
      d: { z: 'x = 0' + ODER + 'x = -3', L: [0, -3], Lfalsch: [[[-3], 'Es fehlt \\(x = 0\\).'], [[0, 3], 'Vorzeichen: \\(x + 3 = 0\\) gibt \\(x = -3\\).']] } } }
  ]);

  /* ---------- Kapitel 5: Parameterdiskussion ----------
     Unterschied zur Animation «Parameter k» der Themenseite (eine Familie x² − 6x + k, Parabel und Zahlenstrahl
     für D): drei Familien in einer Figur — Parameter im konstanten Glied (A: x² − 2x + k), im linearen Glied mit D > 0 für
     jedes k (B) und vor x² mit dem linearen Fall k = 0 (C). Die Anzeige nennt D(k) und den Lösungsfall.
     Startwert k = −2: keine Aufgabe ist schon gelöst, auch nicht nach einem Wechsel der Familie
     (A: D = 12, B: Lösungen −1 und 3, C: D = 12). Familie A ist x² − 2x + k: Ihre Ziele (k = 1, k = 0) sind keine
     Gleichung aus Clip oder Aufgaben (Prüfung 12.10.2026, M6: x² − 4x + k traf 3f). */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    // Fenster je Familie (Prüfung 12.10.2026, H1): Alle Lösungen und der Scheitel bleiben für jedes k von −3 bis 6 im Bild —
    // A: Nullstellen 1 ± √(1 − k) in [−1; 3], Scheitel (1 | k − 1); B: Nullstellen von −6.46 (k = 6) bis 3.79 (k = −3), Scheitel bis y = −12;
    // C: Nullstellen in [−1; 1] (k = −3) bzw. −0.5 (k = 0).
    var FENSTER = { A: { x0: -3, x1: 5, y0: -5, y1: 8, xm: [-2, 2, 4], ym: [-4, -2, 2, 4, 6] },
                    B: { x0: -8, x1: 5, y0: -13, y1: 8, sy: 2, xm: [-6, -4, -2, 2, 4], ym: [-12, -8, -4, 4] },
                    C: { x0: -4, x1: 6, y0: -6, y1: 8, xm: [-2, 2, 4], ym: [-4, -2, 2, 4, 6] } };
    var svg5 = fig.querySelector('svg'), K = null, kFam = null;
    function achsen(f){ if (kFam === f) return; while (svg5.firstChild) svg5.removeChild(svg5.firstChild);
      var o = FENSTER[f]; K = Achsen(svg5, { w: 300, h: 280, x0: o.x0, x1: o.x1, y0: o.y0, y1: o.y1, sy: o.sy || 1, xm: o.xm, ym: o.ym }); kFam = f; }
    var kr = fig.querySelector('input[data-p="k"]'), fam = fig.querySelector('.sim-wahl'), bewegt = {}, pruefen = function(){};
    kr.addEventListener('input', function(){
      bewegt.k = true;
      if (fam.value === 'B'){ var k = +kr.value; bewegt.min = Math.min(bewegt.min == null ? k : bewegt.min, k); bewegt.max = Math.max(bewegt.max == null ? k : bewegt.max, k); }
      zeichnen(); });
    fam.addEventListener('change', function(){ bewegt.min = bewegt.max = null; zeichnen(); });
    function zust(){
      var k = +kr.value, f = fam.value, L, D = null;
      kr.parentNode.querySelector('.sl-val').textContent = z(k);
      if (f === 'A'){ D = 4 - 4 * k; L = D > 0 ? [1 - Math.sqrt(D) / 2, 1 + Math.sqrt(D) / 2] : D === 0 ? [1] : []; }
      else if (f === 'B'){ D = k * k + 12; L = [(-k - Math.sqrt(D)) / 2, (-k + Math.sqrt(D)) / 2]; }
      else { if (k === 0) L = [-0.5]; else { D = 4 - 4 * k; L = D > 0 ? [(-2 - Math.sqrt(D)) / (2 * k), (-2 + Math.sqrt(D)) / (2 * k)].sort(function(a, b){ return a - b; }) : D === 0 ? [-1 / k] : []; } }
      return { k: k, fam: f, D: D, L: L, n: L.length, bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; fam.value = 'A'; } };
    function kT(k){ return k < 0 ? '(' + z(k) + ')' : z(k); }
    function zeichnen(){
      var s = zust(), k = s.k, txt;
      achsen(s.fam); K.leeren();
      if (s.fam === 'A'){
        K.kurve(function(x){ return x * x - 2 * x + k; }, 'kurve');
        txt = sp('tx-blau', 'x² − 2x' + (k === 0 ? '' : k < 0 ? ' − ' + sp('tx-orange', z(-k)) : ' + ' + sp('tx-orange', z(k))) + ' = 0') + '<br>D = 4 − 4 · ' + kT(k) + ' = ' + z(s.D);
      } else if (s.fam === 'B'){
        K.kurve(function(x){ return x * x + k * x - 3; }, 'kurve');
        txt = sp('tx-blau', 'x² ' + (k === 0 ? '' : (k < 0 ? '− ' + sp('tx-orange', z(-k)) : '+ ' + sp('tx-orange', z(k))) + 'x ') + '− 3 = 0') + '<br>D = ' + kT(k) + '² + 12 = ' + z(s.D);
      } else {
        K.kurve(function(x){ return k * x * x + 2 * x + 1; }, 'kurve');
        txt = sp('tx-blau', sp('tx-orange', kT(k)) + ' · x² + 2x + 1 = 0') + (k === 0 ? '<br>k = 0: linear, 2x + 1 = 0' : '<br>D = 4 − 4 · ' + kT(k) + ' = ' + z(s.D));
      }
      s.L.forEach(function(x){ K.punkt(x, 0, 'p-loes'); });
      var fall = !s.L.length ? 'keine Lösung: 𝕃 = { }' : s.L.length === 1 ? 'genau eine Lösung: 𝕃 = { ' + zz(s.L[0]) + ' }' : 'zwei Lösungen: 𝕃 = { ' + zz(s.L[0]) + '; ' + zz(s.L[1]) + ' }';
      fig.querySelector('[data-rolle="formel"]').innerHTML = txt + '<br>' + sp('tx-gruen', fall);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde Familie A: Zieh an \\(k\\). Wann gibt es zwei, eine, keine Lösung?', ok: function(s){ return s.fam === 'A' && s.bewegt.k; } },
      { text: 'Familie A: Stell \\(k\\) so ein, dass es genau <b>eine</b> Lösung gibt.', ok: function(s){ return s.fam === 'A' && s.k === 1; } },
      { text: 'Familie A: Die Lösungen sollen \\(0\\) und \\(2\\) sein.', ok: function(s){ return s.fam === 'A' && s.k === 0; } },
      { text: 'Wähle Familie B und zieh \\(k\\) über den ganzen Bereich. Gibt es ein \\(k\\) mit nur einer Lösung?', ok: function(s){ return s.fam === 'B' && s.bewegt.min != null && s.bewegt.min <= -3 && s.bewegt.max >= 6; } },
      { text: 'Familie B: Die Lösungen sollen \\(2\\) und \\(-1.5\\) sein.', ok: function(s){ return s.fam === 'B' && s.k === -0.5; } },
      { text: 'Wähle Familie C. Für welches \\(k\\) wird die Gleichung linear?', ok: function(s){ return s.fam === 'C' && s.k === 0; } },
      { text: 'Familie C: Stell eine <b>doppelte</b> Lösung ein.', ok: function(s){ return s.fam === 'C' && s.k === 1; } },
      { text: 'Familie C: Stell ein \\(k\\) ein, für das es <b>keine</b> Lösung gibt.', ok: function(s){ return s.fam === 'C' && s.k > 1; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    /* Terme in LaTeX: a x² + b x + c ohne «1x» und «+ −». */
    function glied(c, v, erst){
      if (c === 0) return '';
      var s = Math.abs(c) === 1 && v ? '' : String(Math.abs(c));
      return (c < 0 ? (erst ? '-' : ' - ') : (erst ? '' : ' + ')) + s + v;
    }
    function poly(a, b, c){ var t = glied(a, 'x^2', true); t += glied(b, 'x', !t); t += glied(c, '', !t); return t || '0'; }
    function lin(m, q){ var t = glied(m, 'x', true); t += glied(q, '', !t); return t || '0'; }
    function klam(v){ return v < 0 ? '(' + tz(v) + ')' : tz(v); }
    function zx(v){ return v === 0 ? 'x' : 'x ' + (v < 0 ? '+ ' + (-v) : '- ' + v); }   // x − v
    function anz(D){ return D > 0 ? 'zwei Lösungen' : D === 0 ? 'eine Lösung' : 'keine Lösung'; }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Typschlüssel für die
       Parameter-Typen, alle festen quadratischen Gleichungen als Normalform (FESTE_Q, von zahlen.py geprüft). */
    var SPERRE = [
      'pq|-6', 'pq|6', 'pq|10',               // x² ∓ 6x + k (Clip, Kontrollclip), x² + 10x + k (5a)
      'pl|4', 'pl|16', 'pl|9',                // x² + kx + 4 (Clip), + 16 (Kontrollclip), + 9 (5b)
      'pv|-4|1', 'pv|8|4', 'pv|2|1'           // k x² − 4x + 1 (Kontrollclip), m x² + 8x + 4 (5d), k x² + 2x + 1 (Sim 5 C)
    ];
    var FESTE_Q = [
      [1, -16, 64], [1, -14, 49], [1, -13, 0], [1, -11, 28], [1, -11, 30], [1, -10, -11], [1, -10, 21], [1, -10, 25], [1, -8, 13], [1, -8, 15],
      [1, -8, 16], [1, -7, 12], [1, -6, -7], [1, -6, 0], [1, -6, 5], [1, -6, 8], [1, -6, 9], [1, -6, 10], [1, -5, -14], [1, -5, -6],
      [1, -5, 0], [1, -5, 4], [1, -4, -21], [1, -4, -12], [1, -4, -7], [1, -4, -5], [1, -4, 0], [1, -4, 3], [1, -4, 4], [1, -4, 6],
      [1, -3, -10], [1, -3, -4], [1, -3, 2], [1, -3, 4], [1, -2, -24], [1, -2, -15], [1, -2, -8], [1, -2, -4], [1, -2, -3], [1, -2, 0],
      [1, -2, 1], [1, -1, -30], [1, -1, -12], [1, -1, -6], [1, 0, -144], [1, 0, -100], [1, 0, -81], [1, 0, -64], [1, 0, -49], [1, 0, -36],
      [1, 0, -25], [1, 0, -16], [1, 0, -9], [1, 0, -4], [1, 0, -3], [1, 0, 4], [1, 0, 9], [1, 0, 25], [1, 1, -20], [1, 1, -6],
      [1, 2, -24], [1, 2, -15], [1, 2, -8], [1, 2, -5], [1, 2, -3], [1, 3, -28], [1, 3, -10], [1, 3, 0], [1, 4, -21], [1, 4, -12],
      [1, 4, -5], [1, 4, 4], [1, 5, -6], [1, 5, 0], [1, 5, 7], [1, 6, -16], [1, 6, 2], [1, 6, 5], [1, 7, 0], [1, 8, -9],
      [1, 8, 16], [1, 9, 0], [1, 10, 16], [1, 10, 21], [1, 10, 26], [1, 12, 36], [2, -7, 0], [2, -5, -3], [2, -3, -5], [2, -3, -1],
      [2, -3, 0], [2, -1, -6], [2, -1, -3], [2, 1, -6], [3, -1, -1], [3, 1, -5], [3, 2, -2], [3, 4, -2], [3, 5, -2], [4, -20, 25],
      [4, 0, -9], [4, 4, 1], [5, -3, -2], [9, 0, -4]
    ];
    function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
    function qSchl(q){ var a = q[0], b = q[1], c = q[2]; if (a < 0){ a = -a; b = -b; c = -c; }
      var n = 1; while ((!gl(a * n, Math.round(a * n)) || !gl(b * n, Math.round(b * n)) || !gl(c * n, Math.round(c * n))) && n < 1000) n++;
      a = Math.round(a * n); b = Math.round(b * n); c = Math.round(c * n);
      var g = ggT(ggT(a, b), c) || 1; return [a / g, b / g, c / g].join('|'); }
    var SPERRE_Q = FESTE_Q.map(qSchl);
    /* Reine a·x² = 0 (b = c = 0) nicht über qSchl sperren — gekürzt wären sie alle x² = 0. */
    function gesperrt(T, A){ var q = T.quad && T.quad(A);
      return (T.schl && SPERRE.indexOf(T.schl(A)) >= 0) || (q && (q[1] || q[2]) && SPERRE_Q.indexOf(qSchl(q)) >= 0); }
    /* So tippt man die Menge ein: Drittel und Sechstel als Bruch, sonst Dezimalzahl. */
    function zText(v){
      for (var d of [1, 3, 6]){ var n = Math.round(v * d); if (gl(v * d, n)) return d === 1 ? String(n) : (d === 6 && n % 2 === 0 ? (n / 2) + '/3' : n + '/' + d); }
      return String(Math.round(v * 1000) / 1000);
    }
    function mText(L){ return L === 'R' ? 'R' : '{' + L.map(zText).join('; ') + '}'; }
    function fast(m, soll){
      return soll !== 'R' && !m.alle && m.werte.length === soll.length &&
        soll.every(function(v){ return m.werte.some(function(w){ return Math.abs(v - w) < 0.006; }); });
    }
    var FAST = 'Fast — schreib Drittel und Sechstel als Bruch, zum Beispiel <code>-2/3</code>: \\(0.33\\) ist nicht genau \\(\\tfrac{1}{3}\\).';
    function mengeOk(e){ var m = menge(e); return m.kaputt ? null : m; }
    var MENGE = 'Lösungsmenge wie <code>{-2; 3}</code> oder <code>{}</code>.';

    /* Quadratzahlen mit exakter Wurzel (0.7 · 0.7 ist in JavaScript nicht 0.49); dritte Zahl: Faktor vor x², der ganze
       Koeffizienten gibt. Viele Werte, weil die Sperrliste die üblichen (9, 16, 25, 36, 49 …) schon belegt (HOWTO §15). */
    var WURZELN = [[4, 2], [9, 3], [16, 4], [25, 5], [36, 6], [49, 7], [64, 8], [81, 9], [100, 10], [121, 11], [144, 12], [169, 13],
      [196, 14], [225, 15], [0.25, 0.5, 4], [0.36, 0.6, 25], [0.49, 0.7, 100], [0.64, 0.8, 25], [0.81, 0.9, 100], [1.44, 1.2, 25],
      [2.25, 1.5, 4], [6.25, 2.5, 4], [12.25, 3.5, 4]];
    function WURZEL_VON(r){ for (var i = 0; i < WURZELN.length; i++) if (gl(WURZELN[i][0], r)) return WURZELN[i][1]; return Math.sqrt(r); }
    var TYPEN = {
      /* ── Kapitel 1 ─────────────────────────────────────────────── */
      'normalform': { felder: ['p', 'q'], muster: '\\(p = \\) {p}; \\(q = \\) {q}',
        schl: function(A){ return 'nf|' + A.a + '|' + A.b + '|' + A.c + '|' + A.art; }, quad: function(A){ return [A.a, A.b, A.c]; },
        neu: function(){
          var a = zufall([2, 3, 4, 5, -1, -2, -3, -4]), p = zufall([-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]), q = zufall([-12, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]);
          var b = a * p, c = a * q, art = Math.random() < 0.4 ? 'rechts' : 'null';
          var gl_ = art === 'null' ? poly(a, b, c) + ' = 0' : poly(a, b, 0) + ' = ' + tz(-c);
          return { a: a, b: b, c: c, p: p, q: q, art: art, text: 'Bring \\(' + gl_ + '\\) auf die Normalform \\(x^2 + px + q = 0\\) und gib \\(p\\) und \\(q\\) an.' }; },
        fehler: function(A){
          var f = A.a === -1 ? [] : [[{ p: String(A.b), q: String(A.c) }, 'jedes Glied']];   // bei a = −1 ist das der Vorzeichenfehler
          if (A.a < 0) f.push([{ p: String(-A.p), q: String(-A.q) }, 'Vorzeichen']);
          if (A.art === 'rechts') f.push([{ p: String(A.p), q: String(-A.q) }, 'null']);
          return f.filter(function(x){ return !(gl(+x[0].p, A.p) && gl(+x[0].q, A.q)); }); },
        pruefen: function(A, e){
          if (gl(e.p, A.p) && gl(e.q, A.q)) return null;
          if (A.a < 0 && gl(e.p, -A.p) && gl(e.q, -A.q)) return 'Vorzeichen: Teilen durch \\(' + tz(A.a) + '\\) dreht jedes Vorzeichen.';
          if (gl(e.p, A.b) && gl(e.q, A.c)) return 'Für die Normalform durch \\(' + tz(A.a) + '\\) teilen — jedes Glied, damit vorne nur \\(x^2\\) steht.';
          if (A.art === 'rechts' && gl(e.p, A.p) && gl(e.q, -A.q)) return '\\(p\\) stimmt. Bring zuerst die rechte Seite auf null: Die Zahl wechselt dabei das Vorzeichen.';
          if (gl(e.p, A.p)) return '\\(p\\) stimmt. Rechne \\(q\\) nochmals nach: Zahl ohne \\(x\\) (auf der linken Seite), geteilt durch \\(' + tz(A.a) + '\\).';
          if (gl(e.q, A.q)) return '\\(q\\) stimmt. Rechne \\(p\\) nochmals nach: Zahl vor \\(x\\), geteilt durch \\(' + tz(A.a) + '\\).';
          return 'Alles auf eine Seite, dann jedes Glied durch die Zahl vor \\(x^2\\) teilen.'; },
        loesung: function(A){ return poly(1, A.p, A.q) + ' = 0:\\ p = ' + tz(A.p) + ',\\ q = ' + tz(A.q); } },

      'wurzel': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'wu|' + A.art + '|' + A.a + '|' + A.p + '|' + A.r; }, quad: function(A){ return A.art === 'rein' ? [A.a, 0, -A.a * A.r] : [1, -2 * A.p, A.p * A.p - A.r]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          var art = Math.random() < 0.45 ? 'rein' : 'klammer', a = 1, p = 0, r, L;
          var los = Math.random();
          if (art === 'rein'){
            a = zufall([1, 2, 3, 4, 5]);
            if (los < 0.15) r = -zufall([1, 4, 9, 16, 25, 36]);
            else { var paar = zufall(WURZELN); r = paar[0]; if (!gl(a * r, Math.round(a * r))) a = paar[2] || 1; }
          } else {
            p = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]);
            if (los < 0.12) r = 0; else if (los < 0.24) r = -zufall([1, 4, 9]); else r = zufall([4, 9, 16, 25, 36]);   // r = 1 verdeckt «x = ±r statt ±√r»
          }
          var w = r > 0 ? WURZEL_VON(r) : 0;
          L = r < 0 ? [] : r === 0 ? [p] : [p - w, p + w];
          var t;
          if (art === 'rein') t = Math.random() < 0.5 ? poly(a, 0, 0) + ' = ' + tz(a * r) : poly(a, 0, -a * r) + ' = 0';
          else t = '(' + zx(p) + ')^2 = ' + tz(r);
          return { art: art, a: a, p: p, r: r, L: L, text: 'Löse \\(' + t + '\\).' }; },
        fehler: function(A){
          if (A.r < 0) return [[{ L: mText([-Math.sqrt(-A.r), Math.sqrt(-A.r)]) }, 'nie negativ'], [{ L: 'R' }, null]];
          if (A.r === 0) return [[{ L: mText([A.p, -A.p]) }, null]];
          var f = [[{ L: mText([A.p + WURZEL_VON(A.r)]) }, 'zwei']];
          if (A.p !== 0) f.push([{ L: mText([-A.p - WURZEL_VON(A.r), -A.p + WURZEL_VON(A.r)]) }, 'Vorzeichen']);
          return f; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return MENGE;
          if (mengeGleich(m, A.L)) return null;
          if (A.r < 0) return 'Ein Quadrat ist nie negativ — prüf eine deiner Zahlen in der Gleichung.';
          if (A.r > 0 && m.werte.length === 1 && gl(m.werte[0], A.p + WURZEL_VON(A.r))) return 'Es gibt zwei Lösungen: Auch die negative Wurzel gehört dazu.';
          if (A.p !== 0 && mengeGleich(m, A.r === 0 ? [-A.p] : [-A.p - WURZEL_VON(A.r), -A.p + WURZEL_VON(A.r)])) return 'Vorzeichen: Aus \\(' + zx(A.p) + ' = \\ldots\\) folgt \\(x = ' + tz(A.p) + ' + \\ldots\\).';
          if (A.r === 0) return 'Ein Quadrat ist null, wenn die Klammer null ist: genau eine Lösung.';
          if (A.art === 'rein') return 'Erst \\(x^2\\) allein auf eine Seite, dann die Wurzel mit \\(\\pm\\).';
          return 'Wurzel ziehen mit \\(\\pm\\), dann nach \\(x\\) auflösen.'; },
        loesung: function(A){ return A.r < 0 ? (A.art === 'rein' ? 'x^2 = ' + tz(A.r) + ':\\ ' : '') + '\\mathbb{L} = \\{\\,\\}' : (A.art === 'rein' ? 'x^2 = ' + tz(A.r) + ':\\ ' : zx(A.p) + ' = \\pm ' + WURZEL_VON(A.r) + ':\\ ') + mengeTex(A.L); } },

      /* ── Kapitel 2 ─────────────────────────────────────────────── */
      'ausklammern': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'ak|' + A.a + '|' + A.b; }, quad: function(A){ return [A.a, A.b, 0]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          var a = zufall([1, 2, 3, 4, 5, -1, -2, -3]), w = zufall([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 0.5, -0.5, 1.5]), b = -a * w;   // kein w = 0 (5x² = 0 verdeckt Fehler, Prüfung 12.10.2026)
          if (!gl(b, Math.round(b))){ a *= 2; b = -a * w; }
          var gleich = Math.random() < 0.5 && b !== 0;   // auch als a x² = −b x gestellt
          return { a: a, b: b, w: w, L: w === 0 ? [0] : [0, w],
            text: 'Löse \\(' + (gleich ? poly(a, 0, 0) + ' = ' + lin(-b, 0) : poly(a, b, 0) + ' = 0') + '\\).' }; },
        fehler: function(A){ return A.w === 0 ? [[{ L: '{0; 1}' }, null]] : [[{ L: mText([A.w]) }, 'geteilt'], [{ L: mText([0, -A.w]) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return MENGE;
          if (mengeGleich(m, A.L)) return null;
          if (A.w !== 0 && mengeGleich(m, [A.w])) return 'Es fehlt \\(x = 0\\). Hast du durch \\(x\\) geteilt? Das setzt \\(x \\neq 0\\) voraus — klammere stattdessen \\(x\\) aus.';
          if (A.w !== 0 && mengeGleich(m, [0, -A.w])) return 'Vorzeichen: Aus \\(x\\,(' + lin(A.a, A.b) + ') = 0\\) folgt \\(' + lin(A.a, A.b) + ' = 0\\).';
          if (A.w === 0) return 'Hier ist \\(b = 0\\): \\(' + poly(A.a, 0, 0) + ' = 0\\) hat nur die Lösung \\(0\\).';
          return 'Auf null bringen, \\(x\\) ausklammern, jeden Faktor null setzen.'; },
        loesung: function(A){ return (A.w === 0 ? poly(A.a, 0, 0) + ' = 0' : 'x\\,(' + lin(A.a, A.b) + ') = 0') + ':\\ ' + mengeTex(A.L); } },

      'binom': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'bi|' + A.art + '|' + A.m + '|' + A.k; }, quad: function(A){ return A.art === 'q' ? [A.m, 2 * A.m * A.k, A.m * A.k * A.k] : [A.m * A.m, 0, -A.k * A.k]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          var art = Math.random() < 0.6 ? 'q' : 'd', m = zufall([1, 1, 1, 2, 3]), k;
          if (art === 'q'){ k = zufall([-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
            return { art: art, m: m, k: k, L: [-k], text: 'Löse \\(' + poly(m, 2 * m * k, m * k * k) + ' = 0\\). Erkennst du ein Binom?' }; }
          // a²x² − k² = (ax − k)(ax + k) mit teilerfremden a, k: Lösungen ±k/a
          m = zufall([1, 1, 2, 3]); k = zufallG(2, 15);
          if (ggT(m, k) !== 1) return TYPEN['binom'].neu();
          return { art: art, m: m, k: k, L: [-k / m, k / m], text: 'Löse \\(' + poly(m * m, 0, -k * k) + ' = 0\\) mit einer binomischen Formel.' }; },
        fehler: function(A){ return A.art === 'q' ? [[{ L: mText([A.k]) }, 'Vorzeichen'], [{ L: mText([A.k, -A.k]) }, 'nur eine']] : [[{ L: mText([A.k / A.m]) }, 'Zwei Faktoren']].concat(A.m > 1 ? [[{ L: mText([-A.k, A.k]) }, 'durch']] : []); },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return MENGE;
          if (mengeGleich(m, A.L)) return null;
          if (A.art === 'q'){
            if (m.werte.length === 2) return 'Ein Quadrat \\((x ' + (A.k < 0 ? '- ' + (-A.k) : '+ ' + A.k) + ')^2 = 0\\) ist nur null, wenn die Klammer null ist: nur eine Lösung.';
            if (mengeGleich(m, [A.k])) return 'Vorzeichen: Setz die Klammer null — prüf deine Zahl in der Gleichung.';
            return 'Vergleiche mit \\((x + a)^2 = x^2 + 2a\\,x + a^2\\): Welches \\(a\\) passt?';
          }
          var ax = A.m === 1 ? 'x' : A.m + 'x';
          if (m.werte.length === 1) return 'Zwei Faktoren: \\((' + ax + ' - ' + A.k + ')(' + ax + ' + ' + A.k + ')\\) — jeder kann null sein.';
          if (A.m > 1 && mengeGleich(m, [-A.k, A.k])) return 'Setz \\(' + ax + ' - ' + A.k + ' = 0\\): Am Schluss noch durch \\(' + A.m + '\\) teilen.';
          return 'Dritte binomische Formel: \\(a^2 - b^2 = (a - b)(a + b)\\).'; },
        loesung: function(A){ var ax = A.m === 1 ? 'x' : A.m + 'x'; return (A.art === 'q' ? (A.m === 1 ? '' : A.m) + '(' + zx(-A.k) + ')^2 = 0' : '(' + ax + ' - ' + A.k + ')(' + ax + ' + ' + A.k + ') = 0') + ':\\ ' + mengeTex(A.L); } },

      'zweiklammer': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'zk|' + A.p + '|' + A.q; }, quad: function(A){ return [1, A.p, A.q]; },
        eingabe: function(A){ return { L: mText([A.r1, A.r2]) }; },
        neu: function(){
          var r1 = zufallG(-8, 8), r2 = zufallG(-8, 8);
          if (r1 === r2 || r1 === 0 || r2 === 0 || r1 === -r2) return TYPEN['zweiklammer'].neu();
          var p = -(r1 + r2), q = r1 * r2;
          return { p: p, q: q, r1: r1, r2: r2, text: 'Faktorisiere mit dem Zweiklammersatz und löse: \\(' + poly(1, p, q) + ' = 0\\).' }; },
        fehler: function(A){ return [[{ L: mText([-A.r1, -A.r2]) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return MENGE;
          if (mengeGleich(m, [A.r1, A.r2])) return null;
          if (mengeGleich(m, [-A.r1, -A.r2])) return 'Vorzeichen: Bei Faktoren \\((x - x_1)\\) ist \\(x_1\\) die Lösung — die Summe der Lösungen ist \\(-p = ' + tz(-A.p) + '\\).';
          return 'Gesucht sind die Lösungen: Summe \\(-p = ' + tz(-A.p) + '\\), Produkt \\(q = ' + tz(A.q) + '\\). Kontrolle durch Ausmultiplizieren.'; },
        loesung: function(A){ return '(' + zx(A.r1) + ')(' + zx(A.r2) + ') = 0:\\ ' + mengeTex([A.r1, A.r2]); } },

      /* ── Kapitel 3 ─────────────────────────────────────────────── */
      'ergaenzen': { felder: ['e', 'L'], muster: 'ergänzen mit {e}; 𝕃 = {L}',
        schl: function(A){ return 'er|' + A.b + '|' + A.c; }, quad: function(A){ return [1, A.b, A.c]; },
        eingabe: function(A){ return { e: String(A.h * A.h), L: mText(A.L) }; },
        neu: function(){
          var h = zufall([-6, -5, -4, -3, 3, 4, 5, 6]),   // |h| ≥ 3: bei ±1, ±2 fiele «nicht quadriert» bzw. «nicht halbiert» mit der richtigen Zahl zusammen
              s = zufall([1, 4, 9, 16, 25, 1, 4, 9, 0, -1, -4]), b = 2 * h, c = h * h - s;
          if (c === 0) return TYPEN['ergaenzen'].neu();
          var L = s < 0 ? [] : s === 0 ? [-h] : [-h - Math.sqrt(s), -h + Math.sqrt(s)];
          return { h: h, s: s, b: b, c: c, L: L, text: 'Löse \\(' + poly(1, b, c) + ' = 0\\) mit quadratischer Ergänzung: Welche Zahl ergänzt du auf beiden Seiten, und wie heisst die Lösungsmenge?' }; },
        fehler: function(A){
          var f = [[{ e: String(A.b * A.b), L: mText(A.L) }, 'halbe']];
          if (Math.abs(A.h) > 1) f.push([{ e: String(Math.abs(A.h)), L: mText(A.L) }, 'quadrieren']);
          if (A.s > 0) f.push([{ e: String(A.h * A.h), L: mText([A.h - Math.sqrt(A.s), A.h + Math.sqrt(A.s)]) }, 'Vorzeichen']);
          if (A.s < 0) f.push([{ e: String(A.h * A.h), L: mText([-A.h - Math.sqrt(-A.s), -A.h + Math.sqrt(-A.s)]) }, 'negativ']);
          return f; },
        pruefen: function(A, e){
          var m = mengeOk(e.L), r = [];
          if (!m) return MENGE;
          if (gl(e.e, A.h * A.h) && mengeGleich(m, A.L)) return null;
          if (!gl(e.e, A.h * A.h)) r.push(gl(e.e, A.b * A.b) ? 'Ergänzt wird das Quadrat der <b>halben</b> Zahl vor \\(x\\).' : gl(e.e, Math.abs(A.h)) ? 'Die halbe Zahl vor \\(x\\) noch quadrieren.' : 'Ergänzt wird \\(\\left(\\tfrac{p}{2}\\right)^2\\): die halbe Zahl vor \\(x\\), im Quadrat.');
          if (!mengeGleich(m, A.L)){
            if (A.s < 0) r.push('Nach dem Ergänzen steht rechts eine negative Zahl. Kann ein Quadrat negativ sein?');
            else if (A.s > 0 && mengeGleich(m, [A.h - Math.sqrt(A.s), A.h + Math.sqrt(A.s)])) r.push('Vorzeichen: Aus \\((' + zx(-A.h) + ')^2\\) wird beim Auflösen \\(x = ' + tz(-A.h) + ' \\pm \\ldots\\).');
            else if (A.s > 0 && m.werte.length === 1) r.push('Es fehlt eine Lösung: \\(\\pm\\) beim Wurzelziehen.');
            else r.push('Die Lösungsmenge stimmt noch nicht — mach die Probe.');
          }
          return r.join(' '); },
        loesung: function(A){ return '(' + zx(-A.h) + ')^2 = ' + tz(A.s) + ':\\ ' + mengeTex(A.L); } },

      'mitternacht': { felder: ['D', 'L'], muster: 'D = {D}; 𝕃 = {L}',
        schl: function(A){ return 'mi|' + A.a + '|' + A.b + '|' + A.c; }, quad: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { D: String(A.D), L: mText(A.L) }; },
        neu: function(){
          var art = Math.random(), a, b, c;
          if (art < 0.15){ a = zufall([1, 2, 3]); b = zufall([-4, -2, 2, 4]); c = Math.floor(b * b / (4 * a)) + zufall([1, 2, 3]); }
          else if (art < 0.27){ var r = zufall([-3, -2, -1, 1, 2, 3]), k = zufall([1, 4]); a = k; b = -2 * k * r; c = k * r * r; }
          else { a = zufall([1, 2, 2, 3]); var r1 = zufall([-4, -3, -2, -1, 1, 2, 3, 4]), r2n = zufall([-5, -3, -1, 1, 3, 5, -4, -2, 2, 4]);
                 b = -a * r1 - r2n; c = r1 * r2n; if (b === 0 || c === 0) return TYPEN['mitternacht'].neu(); }
          var D = b * b - 4 * a * c, L = D < 0 ? [] : D === 0 ? [-b / (2 * a)] : [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)];
          if (D > 0 && !gl(Math.sqrt(D), Math.round(Math.sqrt(D)))) return TYPEN['mitternacht'].neu();
          return { a: a, b: b, c: c, D: D, L: L, text: 'Löse \\(' + poly(a, b, c) + ' = 0\\) mit der Mitternachtsformel. (Bei \\(D \\lt 0\\): \\(\\mathbb{L} = \\{\\,\\}\\) als <code>{}</code>.)' }; },
        fehler: function(A){ var f = []; if (A.a * A.c !== 0) f.push([{ D: String(A.b * A.b + 4 * A.a * A.c), L: mText(A.L) }, 'abgezogen']);
          if (A.D > 0) f.push([{ D: String(A.D), L: mText(A.L.map(function(v){ return -v; })) }, '-b']); return f; },
        pruefen: function(A, e){
          var m = mengeOk(e.L), r = [];
          if (!m) return MENGE;
          if (gl(e.D, A.D) && mengeGleich(m, A.L)) return null;
          if (!gl(e.D, A.D)) r.push(gl(e.D, A.b * A.b + 4 * A.a * A.c) ? 'Diskriminante: \\(4ac\\) wird abgezogen: \\(D = ' + A.b * A.b + ' - 4 \\cdot ' + klam(A.a) + ' \\cdot ' + klam(A.c) + '\\).' : 'Diskriminante: \\(D = b^2 - 4ac\\) mit \\(a = ' + A.a + '\\), \\(b = ' + tz(A.b) + '\\), \\(c = ' + tz(A.c) + '\\).');
          if (!mengeGleich(m, A.L)){
            if (fast(m, A.L)) r.push(FAST);
            else if (A.D > 0 && mengeGleich(m, A.L.map(function(v){ return -v; }))) r.push('Vorne steht \\(-b = ' + tz(-A.b) + '\\).');
            else if (A.D < 0) r.push('Bei \\(D \\lt 0\\) gibt es keine Lösung.');
            else if (A.D === 0) r.push('Bei \\(D = 0\\) gibt es genau eine Lösung: \\(x = -\\tfrac{b}{2a}\\).');
            else r.push('Lösungen: \\(x = \\dfrac{-b \\pm \\sqrt{D}}{2a}\\) — der Nenner ist \\(2a = ' + 2 * A.a + '\\).');
          }
          return r.join(' '); },
        loesung: function(A){ return 'D = ' + A.D + ':\\ ' + mengeTex(A.L); } },

      /* Exakte Lösungen mit Wurzel (Prüfung 12.10.2026, M5): x² − 2h x + h² − s = 0 hat x = h ± √s;
         die Mitternachtsformel gibt (2h ± √(4s))/2 — teilweise Wurzel ziehen und kürzen. */
      'exakt': { felder: ['h', 's'], muster: '\\(x = \\) {h} \\(\\pm\\) √ {s}',
        schl: function(A){ return 'ex|' + A.h + '|' + A.s; }, quad: function(A){ return [1, -2 * A.h, A.h * A.h - A.s]; },
        eingabe: function(A){ return { h: String(A.h), s: String(A.s) }; },
        neu: function(){
          var h = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), s = zufall([2, 3, 5, 6, 7, 10, 11, 13]);
          return { h: h, s: s, text: 'Löse \\(' + poly(1, -2 * h, h * h - s) + ' = 0\\) exakt und gib die Lösungen in der Form \\(x = h \\pm \\sqrt{s}\\) an.' }; },
        fehler: function(A){ return [[{ h: String(-A.h), s: String(A.s) }, 'Vorzeichen'], [{ h: String(A.h), s: String(4 * A.s) }, 'teilweise']]; },
        pruefen: function(A, e){
          if (gl(e.h, A.h) && gl(e.s, A.s)) return null;
          var r = [];
          if (!gl(e.h, A.h)) r.push(gl(e.h, -A.h) ? 'Vorzeichen: Vorne steht \\(-b\\), geteilt durch \\(2\\).' : 'Die Zahl vor \\(\\pm\\) ist \\(-\\tfrac{b}{2a}\\).');
          if (!gl(e.s, A.s)) r.push(gl(e.s, 4 * A.s) ? 'Noch teilweise Wurzel ziehen: \\(\\sqrt{' + 4 * A.s + '} = \\sqrt{4 \\cdot ' + A.s + '} = 2\\sqrt{' + A.s + '}\\), dann durch \\(2\\) kürzen.' : 'Unter der Wurzel: \\(D = ' + 4 * A.s + '\\), \\(\\sqrt{D} = 2\\sqrt{' + A.s + '}\\), und das durch \\(2a = 2\\).');
          return r.join(' '); },
        loesung: function(A){ return 'D = ' + 4 * A.s + ',\\ x = \\dfrac{' + 2 * A.h + ' \\pm 2\\sqrt{' + A.s + '}}{2} = ' + A.h + ' \\pm \\sqrt{' + A.s + '}'; } },

      'anzahl': { felder: ['D', 'n'], muster: 'D = {D}; also {n:zwei Lösungen|eine Lösung|keine Lösung}',
        schl: function(A){ return 'an|' + A.a + '|' + A.b + '|' + A.c; }, quad: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { D: String(A.D), n: anz(A.D) }; },
        neu: function(){
          var art = zufall(['p', 'n', 'z']), a, b, c, D;
          if (art === 'z'){ var mm = zufall([1, 2, 3]), nn = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), kk = zufall([1, 1, -1]); a = kk * mm * mm; b = kk * 2 * mm * nn; c = kk * nn * nn; }
          else { for (var v = 0; v < 200; v++){ a = zufall([1, 2, 3, 4, -1, -2]); b = zufallG(-8, 8); c = zufall([-9, -7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 9]);
            D = b * b - 4 * a * c; if (art === 'p' ? D > 0 : D < 0) break; } }
          D = b * b - 4 * a * c;
          return { a: a, b: b, c: c, D: D, text: 'Wie viele Lösungen hat \\(' + poly(a, b, c) + ' = 0\\)? Entscheide mit der Diskriminante, ohne zu lösen.' }; },
        fehler: function(A){ var f = [], D2 = A.b * A.b + 4 * A.a * A.c; f.push([{ D: String(D2), n: anz(D2) }, 'abgezogen']);
          f.push([{ D: String(A.D), n: anz(A.D) === 'keine Lösung' ? 'zwei Lösungen' : 'keine Lösung' }, null]); return f; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.D, A.D) && e.n === anz(A.D)) return null;
          if (!gl(e.D, A.D)) r.push(gl(e.D, A.b * A.b + 4 * A.a * A.c) ? '\\(4ac\\) wird abgezogen: \\(D = ' + A.b * A.b + ' - 4 \\cdot ' + klam(A.a) + ' \\cdot ' + klam(A.c) + '\\).' : '\\(D = b^2 - 4ac\\) mit \\(a = ' + tz(A.a) + '\\), \\(b = ' + tz(A.b) + '\\), \\(c = ' + tz(A.c) + '\\).');
          else r.push('\\(D\\) stimmt. Positiv, null oder negativ — was heisst das für die Anzahl?');
          return r.join(' '); },
        loesung: function(A){ return 'D = ' + A.D + ':\\ \\text{' + anz(A.D) + '}'; } },

      /* ── Kapitel 4 ─────────────────────────────────────────────── */
      'verfahren': { felder: ['v', 'L'], muster: 'Am schnellsten: {v:Wurzelziehen|Ausklammern|Faktorisieren|Mitternachtsformel}; 𝕃 = {L}',
        schl: function(A){ return 've|' + A.a + '|' + A.b + '|' + A.c; }, quad: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { v: A.v, L: mText(A.L) }; },
        neu: function(){
          var art = zufall(['W', 'A', 'F', 'M']), a = 1, b, c, L, v;
          if (art === 'W'){   // a·x² − a·r² = 0; viele r, weil die Sperrliste die kleinen Quadratzahlen belegt (HOWTO §15)
            var wr = zufall([[1, 1], [8, 1], [11, 1], [13, 1], [14, 1], [15, 1], [0.5, 4], [2.5, 4], [3.5, 4], [4.5, 4], [1 / 3, 9], [4 / 3, 9], [5 / 3, 9]]), r = wr[0];
            a = wr[1] === 1 ? zufall([1, 2, 3]) : wr[1]; b = 0; c = -Math.round(a * r * r); L = [-r, r]; v = 'Wurzelziehen'; }
          else if (art === 'A'){ var w = zufall([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]); a = zufall([1, 2, 3]); b = -a * w; c = 0; L = [0, w]; v = 'Ausklammern'; }
          else if (art === 'F'){ var r1 = zufallG(-6, 6), r2 = zufallG(-6, 6); if (r1 === r2 || r1 === 0 || r2 === 0 || r1 === -r2) return TYPEN['verfahren'].neu();
            b = -(r1 + r2); c = r1 * r2; L = [r1, r2]; v = 'Faktorisieren'; }
          else { a = zufall([2, 3, 5]); var p1 = zufall([1, 2, 3, -1, -2]), q1 = zufall([1, -1, 2, -2, 3]);
            if (q1 % a === 0) return TYPEN['verfahren'].neu(); b = -a * p1 - q1; c = p1 * q1; L = [p1, q1 / a]; v = 'Mitternachtsformel'; if (b === 0 || c === 0) return TYPEN['verfahren'].neu(); }
          return { a: a, b: b, c: c, L: L, v: v, text: 'Welches Verfahren führt am schnellsten zum Ziel? Löse dann: \\(' + poly(a, b, c) + ' = 0\\).' }; },
        fehler: function(A){ return A.v === 'Mitternachtsformel' ? [[{ v: 'Faktorisieren', L: mText(A.L) }, 'Zweiklammersatz']] : [[{ v: 'Mitternachtsformel', L: mText(A.L) }, 'Geht immer']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L), r = [];
          if (!m) return MENGE;
          // Faktorisieren geht auch bei a·x² − c (Binom) und a·x² + bx (x ausklammern): gleich schnell.
          var auchF = e.v === 'Faktorisieren' && (A.v === 'Wurzelziehen' || A.v === 'Ausklammern');
          if ((e.v === A.v || auchF) && mengeGleich(m, A.L)) return null;
          if (e.v !== A.v && !auchF){
            if (e.v === 'Mitternachtsformel') r.push('Geht immer — aber hier gibt es einen kürzeren Weg. ' + (A.v === 'Wurzelziehen' ? 'Das Glied mit \\(x\\) fehlt.' : A.v === 'Ausklammern' ? 'Die Zahl ohne \\(x\\) fehlt.' : 'Zwei ganze Zahlen mit Summe \\(' + tz(-A.b) + '\\) und Produkt \\(' + tz(A.c) + '\\) gibt es.'));
            else if (A.v === 'Mitternachtsformel') r.push(e.v === 'Wurzelziehen' ? 'Wurzelziehen braucht eine Gleichung ohne lineares Glied (\\(b = 0\\)) — hier sind alle drei Glieder da.' : e.v === 'Ausklammern' ? 'Ausklammern braucht eine Gleichung ohne Zahl ohne \\(x\\) — hier sind alle drei Glieder da.' : 'Vor \\(x^2\\) steht \\(' + A.a + '\\), und alle drei Glieder sind da — der Zweiklammersatz geht hier nicht glatt.');
            else r.push(e.v === 'Wurzelziehen' ? 'Wurzelziehen braucht eine Gleichung ohne lineares Glied (\\(b = 0\\)).' : e.v === 'Ausklammern' ? 'Ausklammern braucht eine Gleichung ohne Zahl ohne \\(x\\).' : 'Vor \\(x^2\\) steht \\(' + A.a + '\\) — der Zweiklammersatz braucht \\(1\\) vor \\(x^2\\).');
          }
          if (!mengeGleich(m, A.L)) r.push(fast(m, A.L) ? FAST : m.werte.length < A.L.length ? 'Es fehlt eine Lösung.' : 'Die Lösungsmenge stimmt noch nicht — mach die Probe.');
          return r.join(' '); },
        loesung: function(A){ return '\\text{' + A.v + '}:\\ ' + mengeTex(A.L); } },

      'ordnen': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'or|' + A.m + '|' + A.c; }, quad: function(A){ return [1, A.m, -A.c]; },
        eingabe: function(A){ return { L: mText([A.r1, A.r2]) }; },
        neu: function(){
          var r1 = zufallG(-7, 7), r2 = zufallG(-7, 7);
          if (r1 === r2 || r1 === 0 || r2 === 0 || r1 === -r2) return TYPEN['ordnen'].neu();
          var m = -(r1 + r2), c = -r1 * r2;
          var falsch = [c, c - m];
          if (mengeGleich({ werte: falsch }, [r1, r2]) || falsch[0] === falsch[1]) return TYPEN['ordnen'].neu();
          return { r1: r1, r2: r2, m: m, c: c, text: 'Löse \\(x\\,(' + lin(1, m) + ') = ' + tz(c) + '\\).' }; },
        fehler: function(A){ return [[{ L: mText([A.c, A.c - A.m]) }, 'Nullprodukt'], [{ L: mText([-A.r1, -A.r2]) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return MENGE;
          if (mengeGleich(m, [A.r1, A.r2])) return null;
          if (mengeGleich(m, [A.c, A.c - A.m])) return 'Rechts steht \\(' + tz(A.c) + '\\), nicht \\(0\\): Das Nullprodukt gilt hier nicht. Erst ausmultiplizieren und auf null bringen.';
          if (mengeGleich(m, [-A.r1, -A.r2])) return 'Vorzeichen: Bei Faktoren \\((x - x_1)\\) ist \\(x_1\\) die Lösung. Mach die Probe.';
          return 'Ausmultiplizieren, auf null bringen, faktorisieren — und die Probe in der Ausgangsgleichung.'; },
        loesung: function(A){ return poly(1, A.m, -A.c) + ' = 0 \\Rightarrow (' + zx(A.r1) + ')(' + zx(A.r2) + ') = 0:\\ ' + mengeTex([A.r1, A.r2]); } },

      'vieta': { felder: ['urteil', 'L'], muster: '{urteil:beide richtig|nicht beide richtig}; 𝕃 = {L}',
        schl: function(A){ return 'vi|' + A.p + '|' + A.q; }, quad: function(A){ return [1, A.p, A.q]; },
        eingabe: function(A){ return { urteil: A.richtig ? 'beide richtig' : 'nicht beide richtig', L: mText([A.r1, A.r2]) }; },
        neu: function(){
          var r1 = zufallG(-8, 8), r2 = zufallG(-8, 8);
          if (r1 === r2 || r1 === 0 || r2 === 0 || r1 === -r2) return TYPEN['vieta'].neu();
          var p = -(r1 + r2), q = r1 * r2, ang, richtig = Math.random() < 0.5;
          if (richtig) ang = [r1, r2];
          else { ang = zufall([[-r1, -r2], [r1, -r2], [r1 + 1, r2 - 1]]);
            if (ang[0] === ang[1] || mengeGleich({ werte: ang }, [r1, r2])) return TYPEN['vieta'].neu(); }
          return { r1: r1, r2: r2, p: p, q: q, u: ang[0], v: ang[1], richtig: richtig,
            text: 'Prüfe mit dem Satz von Vieta: Sind \\(' + tz(ang[0]) + '\\) und \\(' + tz(ang[1]) + '\\) die Lösungen von \\(' + poly(1, p, q) + ' = 0\\)? Gib danach die Lösungsmenge an.' }; },
        fehler: function(A){ return [[{ urteil: A.richtig ? 'nicht beide richtig' : 'beide richtig', L: mText([A.r1, A.r2]) }, null],
                                     A.richtig ? [{ urteil: 'beide richtig', L: mText([-A.r1, -A.r2]) }, null] : [{ urteil: 'beide richtig', L: mText([A.u, A.v]) }, null]]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L), r = [], soll = A.richtig ? 'beide richtig' : 'nicht beide richtig';
          if (!m) return MENGE;
          if (e.urteil === soll && mengeGleich(m, [A.r1, A.r2])) return null;
          if (e.urteil !== soll) r.push('Vergleiche: Summe \\(' + tz(A.u) + ' + ' + klam(A.v) + '\\) mit \\(-p = ' + tz(-A.p) + '\\), Produkt \\(' + tz(A.u) + ' \\cdot ' + klam(A.v) + '\\) mit \\(q = ' + tz(A.q) + '\\).');
          if (!mengeGleich(m, [A.r1, A.r2])) r.push('Die Lösungsmenge: zwei Zahlen mit Summe \\(-p = ' + tz(-A.p) + '\\) und Produkt \\(q = ' + tz(A.q) + '\\).');
          return r.join(' '); },
        loesung: function(A){ return '\\text{' + (A.richtig ? 'beide richtig' : 'nicht beide richtig') + '}:\\ ' + mengeTex([A.r1, A.r2]); } },

      /* ── Kapitel 5 ─────────────────────────────────────────────── */
      'param-quadr': { felder: ['k', 'x'], muster: 'genau eine Lösung für \\(k = \\) {k}; sie heisst \\(x = \\) {x}',
        schl: function(A){ return 'pq|' + A.b; },
        eingabe: function(A){ return { k: String(A.b * A.b / 4), x: String(-A.b / 2) }; },
        neu: function(){
          var b = zufall([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10, 12, -12]);
          return { b: b, text: 'Für welches \\(k\\) hat \\(' + poly(1, b, 0) + ' + k = 0\\) genau eine Lösung? Wie heisst sie?' }; },
        fehler: function(A){ return [[{ k: String(A.b * A.b / 4), x: String(A.b / 2) }, 'Vorzeichen'], [{ k: String(A.b * A.b / 2), x: String(-A.b / 2) }, '4']]; },
        pruefen: function(A, e){
          var r = [], k0 = A.b * A.b / 4;
          if (gl(e.k, k0) && gl(e.x, -A.b / 2)) return null;
          if (!gl(e.k, k0)) r.push('Genau eine Lösung bei \\(D = 0\\): \\(D = ' + klam(A.b) + '^2 - 4k = ' + A.b * A.b + ' - 4k\\).');
          if (!gl(e.x, -A.b / 2)) r.push(gl(e.x, A.b / 2) ? 'Vorzeichen: \\(x = -\\tfrac{b}{2a}\\).' : 'Bei \\(D = 0\\) ist \\(x = -\\tfrac{b}{2a}\\).');
          return r.join(' '); },
        loesung: function(A){ return 'D = ' + A.b * A.b + ' - 4k = 0 \\Rightarrow k = ' + A.b * A.b / 4 + ';\\ x = ' + tz(-A.b / 2); } },

      'param-lin': { felder: ['L'], muster: '\\(k \\in \\) {L}',
        schl: function(A){ return 'pl|' + A.c; },
        eingabe: function(A){ return { L: mText([-2 * A.w, 2 * A.w]) }; },
        neu: function(){
          var w = zufallG(1, 9), c = w * w;
          return { w: w, c: c, text: 'Für welche \\(k\\) hat \\(x^2 + kx + ' + c + ' = 0\\) genau eine Lösung? Gib alle als Menge an, zum Beispiel <code>{1.5; -1.5}</code>.' }; },
        fehler: function(A){ return [[{ L: mText([2 * A.w]) }, 'zweiten Wert'], [{ L: mText([-A.w, A.w]) }, 'Faktor']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return 'Gib die Werte als Menge an, zum Beispiel <code>{1.5; -1.5}</code>.';
          if (mengeGleich(m, [-2 * A.w, 2 * A.w])) return null;
          if (m.werte.length === 1 && gl(Math.abs(m.werte[0]), 2 * A.w)) return 'Es gibt einen zweiten Wert: Auch \\((' + tz(-m.werte[0]) + ')^2 = ' + 4 * A.c + '\\).';
          if (mengeGleich(m, [-A.w, A.w])) return '\\(D = k^2 - 4 \\cdot ' + A.c + '\\) — der Faktor \\(4\\) fehlt.';
          return 'Genau eine Lösung bei \\(D = 0\\): \\(D = k^2 - 4 \\cdot 1 \\cdot ' + A.c + '\\).'; },
        loesung: function(A){ return 'k^2 - ' + 4 * A.c + ' = 0 \\Rightarrow k = \\pm ' + 2 * A.w; } },

      'param-vorne': { felder: ['L'], muster: '\\(k \\in \\) {L}',
        schl: function(A){ return 'pv|' + A.b + '|' + A.c; },
        eingabe: function(A){ return { L: mText([0, A.k0]) }; },
        neu: function(){
          var b = zufall([-8, -6, -4, -2, 2, 4, 6, 8]), c = zufall([1, 2, 4, -1, -2, -4]);
          return { b: b, c: c, k0: b * b / (4 * c), text: 'Für welche \\(k\\) hat \\(k \\cdot x^2 ' + (b < 0 ? '- ' + (-b) : '+ ' + b) + 'x ' + (c < 0 ? '- ' + (-c) : '+ ' + c) + ' = 0\\) genau eine Lösung? Denk an alle Fälle und gib die Werte als Menge an.' }; },
        fehler: function(A){ return [[{ L: mText([A.k0]) }, 'k = 0'], [{ L: mText([0]) }, null], [{ L: mText([0, -A.k0]) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          var m = mengeOk(e.L); if (!m) return 'Gib die Werte als Menge an, zum Beispiel <code>{0; 3}</code>.';
          if (mengeGleich(m, [0, A.k0])) return null;
          if (mengeGleich(m, [A.k0])) return 'Der Fall \\(k = 0\\) fehlt: Dann ist die Gleichung linear und hat genau eine Lösung.';
          if (mengeGleich(m, [0])) return '\\(k = 0\\) stimmt. Für \\(k \\neq 0\\) gibt \\(D = 0\\) einen zweiten Wert.';
          if (mengeGleich(m, [0, -A.k0])) return 'Vorzeichen: \\(D = ' + A.b * A.b + ' - 4 \\cdot k \\cdot ' + klam(A.c) + '\\).';
          return 'Zwei Fälle: \\(k = 0\\) (linear) und \\(k \\neq 0\\) mit \\(D = b^2 - 4 \\cdot k \\cdot c = 0\\).'; },
        loesung: function(A){ return 'k = 0\\ \\text{(linear)};\\ ' + A.b * A.b + ' - 4 \\cdot ' + klam(A.c) + ' \\cdot k = 0 \\Rightarrow k = ' + texZahl(A.k0); } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '"' + (f === 'L' ? ' class="menge" placeholder="{ … }"' : '') + '>';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){
          if (i.dataset.f === 'L'){ e.L = i.value; var mm = menge(i.value); if (mm.leer) leer = true; if (mm.komma) komma = true; return; }
          var r = zahl(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-3</code>, <code>0.5</code>, <code>1/2</code>.'; return; }
        versuche++;
        var f = T.pruefen(A, e);
        if (f === null){
          serie = versuche === 1 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + ' <button type="button" class="ue-weiter">Nächste</button>';
          rueck.querySelector('.ue-weiter').addEventListener('click', neu);
        } else {
          serie = 0; rueck.className = 'ue-rueck falsch';
          rueck.innerHTML = f + (versuche >= 2 ? ' <details class="ue-loes"><summary>Lösung</summary>\\(' + T.loesung(A) + '\\)</details>' : '');
        }
        zaehler.textContent = serie + ' in Folge' + (serie >= 3 ? ' ✓' : '');
        setzen(rueck);
      }
      box.querySelector('.ue-pruefen').addEventListener('click', pruefen);
      box.querySelector('.ue-neu').addEventListener('click', neu);
      ein.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') pruefen(); });
      neu();
    });
  })();

  /* ---------- Minigrafen: <svg class="mini" data-k="…;…">, Teile durch «;» getrennt:
       g,m,q → m x + q (Gerade)      q,a,b,c → a x² + b x + c (Parabel)
     dazu data-fenster="x0,x1,y0,y1", data-punkte="x,y;…", data-xm/data-ym, data-titel. ---------- */
  document.querySelectorAll('svg.mini[data-k]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-5,5,-5,5').split(',').map(Number);
    svg.setAttribute('viewBox', '0 0 170 170'); svg.setAttribute('role', 'img');
    var liste = function(t, d){ return t ? t.split(',').map(Number) : d; };
    var K = Achsen(svg, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, sy: +svg.dataset.sy || 1, sx: +svg.dataset.sx || 1, pfeil: 6,
      xm: liste(svg.dataset.xm, []), ym: liste(svg.dataset.ym, []) });
    svg.dataset.k.split(';').filter(Boolean).forEach(function(s, i){
      var p = s.split(','), art = p[0], q = p.slice(1).map(Number);
      var f = art === 'g' ? function(x){ return q[0] * x + q[1]; } : function(x){ return q[0] * x * x + q[1] * x + q[2]; };
      K.kurve(f, 'kurve' + (i ? ' k' + i : ''));
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){ var a = p.split(',').map(Number); K.punkt(a[0], a[1], 'p-loes'); });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
