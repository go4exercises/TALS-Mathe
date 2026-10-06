<script>
/* Leitprogramm Lineare und quadratische Gleichungen — Umformer mit Aufgabenleiste, Parameter-
   Simulation, Übungen mit Rückmeldung, Minigrafen. Notation wie auf den Themenseiten 2.2a/2.2b:
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
  function zz(v){ var r = Math.round(v * 1000) / 1000; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(v); }
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
    if (/^[a-z]\s*=/i.test(t)) return { kaputt: true, xgleich: true };
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

  /* ---------- Kapitel 1: lineare Gleichungen umformen ----------
     Startgleichungen sind nicht die Beispiele aus dem Clip (4(x − 2) = 2x + 6 usw.). */
  umformerSim('sim1', [
    { text: 'Löse \\(3x + 4 = x - 6\\).', k: {
      a: { z: '3x + 4 = x - 6', w: [['beidseitig \\(-x\\)', 'b', '\\mid -x'], ['beidseitig \\(-4\\)', 'c', '\\mid -4'],
        ['beidseitig \\(\\cdot 0\\)', '!Das gibt \\(0 = 0\\) — wahr für jedes \\(x\\). Mit \\(0\\) multiplizieren ist keine Äquivalenzumformung: Die Lösungsmenge ändert sich.']] },
      b: { z: '2x + 4 = -6', w: [['beidseitig \\(-4\\)', 'd', '\\mid -4'], ['beidseitig \\(+4\\)', '!Dann steht links \\(2x + 8\\) — die \\(4\\) soll aber weg. Die Gegenoperation zu \\(+4\\) ist \\(-4\\).']] },
      c: { z: '3x = x - 10', w: [['beidseitig \\(-x\\)', 'd', '\\mid -x'], ['beidseitig \\(:3\\)', '?Erlaubt, aber rechts steht noch \\(x\\). Sammle zuerst alle \\(x\\)-Glieder auf einer Seite.']] },
      d: { z: '2x = -10', w: [['beidseitig \\(:2\\)', 'e', '\\mid :2'], ['beidseitig \\(-2\\)', '!Dann steht \\(2x - 2\\) da. \\(2x\\) heisst \\(2 \\cdot x\\): Die Gegenoperation ist \\(:2\\).']] },
      e: { z: 'x = -5', L: [-5], Lfalsch: [[[5], 'Vorzeichen: \\(-10 : 2 = -5\\).']], probe: '3 \\cdot (-5) + 4 = -11 \\text{ und } -5 - 6 = -11\\ \\checkmark' } } },
    { text: 'Löse \\(5(x - 1) = 2(x + 2)\\).', k: {
      a: { z: '5(x - 1) = 2(x + 2)', w: [['Klammern auflösen: \\(5x - 5 = 2x + 4\\)', 'b'],
        ['Klammern auflösen: \\(5x - 1 = 2x + 2\\)', '!Der Faktor vor der Klammer gilt für <b>jedes</b> Glied in der Klammer: \\(5 \\cdot (-1) = -5\\) und \\(2 \\cdot 2 = 4\\).'],
        ['beidseitig \\(:5\\)', '?Erlaubt, gibt aber rechts einen Bruch: \\(\\tfrac{2}{5}(x + 2)\\). Einfacher: zuerst die Klammern auflösen.']] },
      b: { z: '5x - 5 = 2x + 4', w: [['beidseitig \\(-2x\\)', 'c', '\\mid -2x'], ['beidseitig \\(+5\\)', 'c2', '\\mid +5']] },
      c: { z: '3x - 5 = 4', w: [['beidseitig \\(+5\\)', 'd', '\\mid +5'], ['beidseitig \\(-5\\)', '!Dann steht links \\(3x - 10\\). Die Gegenoperation zu \\(-5\\) ist \\(+5\\).']] },
      c2: { z: '5x = 2x + 9', w: [['beidseitig \\(-2x\\)', 'd', '\\mid -2x']] },
      d: { z: '3x = 9', w: [['beidseitig \\(:3\\)', 'e', '\\mid :3']] },
      e: { z: 'x = 3', L: [3], probe: '5 \\cdot 2 = 10 \\text{ und } 2 \\cdot 5 = 10\\ \\checkmark' } } },
    { text: 'Löse \\(3(x + 2) = 3x + 5\\).', k: {
      a: { z: '3(x + 2) = 3x + 5', w: [['Klammer auflösen: \\(3x + 6 = 3x + 5\\)', 'b'], ['Klammer auflösen: \\(3x + 2 = 3x + 5\\)', '!Der Faktor \\(3\\) gilt auch für die \\(2\\): \\(3 \\cdot 2 = 6\\).']] },
      b: { z: '3x + 6 = 3x + 5', w: [['beidseitig \\(-3x\\)', 'c', '\\mid -3x'], ['beidseitig \\(:3x\\)', '!Durch einen Term mit \\(x\\) zu teilen setzt \\(x \\neq 0\\) voraus — keine Äquivalenzumformung. Subtrahiere die \\(x\\)-Glieder.']] },
      c: { z: '6 = 5', frage: '\\(x\\) ist weg, und es bleibt eine Aussage. Ist sie wahr oder falsch? Gib die Lösungsmenge an:', L: [],
        Lfalsch: [['R', 'Die Aussage \\(6 = 5\\) ist falsch — egal, welches \\(x\\) man einsetzt.']] } } },
    { text: 'Löse \\(2(3x - 1) = 6x - 2\\).', k: {
      a: { z: '2(3x - 1) = 6x - 2', w: [['Klammer auflösen: \\(6x - 2 = 6x - 2\\)', 'b'], ['Klammer auflösen: \\(6x - 1 = 6x - 2\\)', '!Der Faktor \\(2\\) gilt für beide Glieder: \\(2 \\cdot (-1) = -2\\).']] },
      b: { z: '6x - 2 = 6x - 2', w: [['beidseitig \\(-6x\\)', 'c', '\\mid -6x'], ['beidseitig \\(:6x\\)', '!Durch einen Term mit \\(x\\) zu teilen ist keine Äquivalenzumformung. Subtrahiere die \\(x\\)-Glieder.']] },
      c: { z: '-2 = -2', frage: '\\(x\\) ist weg. Die Aussage ist wahr — für welche \\(x\\)? Gib die Lösungsmenge an:', L: 'R',
        Lfalsch: [[[], 'Die Aussage \\(-2 = -2\\) ist wahr, und zwar für jedes \\(x\\). Schreib <code>R</code>.']] } } },
    { text: 'Löse \\(\\tfrac{x}{2} + 1 = \\tfrac{x}{3} + 2\\).', k: {
      a: { z: '\\tfrac{x}{2} + 1 = \\tfrac{x}{3} + 2', w: [['beidseitig \\(\\cdot 6\\) (Hauptnenner)', 'b', '\\mid \\cdot 6'],
        ['beidseitig \\(\\cdot 5\\)', '?Erlaubt, aber \\(5\\) ist kein Vielfaches von \\(2\\) und \\(3\\) — die Brüche bleiben. Der Hauptnenner von \\(2\\) und \\(3\\) ist \\(6\\).'],
        ['nur die Brüche mal \\(6\\): \\(3x + 1 = 2x + 2\\)', '!Mal \\(6\\) heisst: <b>jedes</b> Glied auf beiden Seiten, auch \\(1\\) und \\(2\\).']] },
      b: { z: '3x + 6 = 2x + 12', w: [['beidseitig \\(-2x\\)', 'c', '\\mid -2x'], ['beidseitig \\(-6\\)', 'c2', '\\mid -6']] },
      c: { z: 'x + 6 = 12', w: [['beidseitig \\(-6\\)', 'd', '\\mid -6']] },
      c2: { z: '3x = 2x + 6', w: [['beidseitig \\(-2x\\)', 'd', '\\mid -2x']] },
      d: { z: 'x = 6', L: [6], probe: '\\tfrac{6}{2} + 1 = 4 \\text{ und } \\tfrac{6}{3} + 2 = 4\\ \\checkmark' } } },
    { text: 'Löse \\(-2x + 7 = 3 - (x - 1)\\).', k: {
      a: { z: '-2x + 7 = 3 - (x - 1)', w: [['Minusklammer auflösen: \\(-2x + 7 = 4 - x\\)', 'b'],
        ['Minusklammer auflösen: \\(-2x + 7 = 2 - x\\)', '!Das Minus vor der Klammer dreht <b>jedes</b> Vorzeichen in der Klammer: \\(-(x - 1) = -x + 1\\), also \\(3 - x + 1 = 4 - x\\).']] },
      b: { z: '-2x + 7 = 4 - x', w: [['beidseitig \\(+2x\\)', 'c', '\\mid +2x'], ['beidseitig \\(+x\\)', 'c2', '\\mid +x']] },
      c: { z: '7 = 4 + x', w: [['beidseitig \\(-4\\)', 'd', '\\mid -4']] },
      c2: { z: '-x + 7 = 4', w: [['beidseitig \\(-7\\)', 'c3', '\\mid -7']] },
      c3: { z: '-x = -3', w: [['beidseitig \\(\\cdot (-1)\\)', 'e', '\\mid \\cdot (-1)'], ['Minus weglassen: \\(x = -3\\)', '!Aus \\(-x = -3\\) folgt nicht \\(x = -3\\): Mal \\((-1)\\) dreht <b>beide</b> Vorzeichen.']] },
      d: { z: '3 = x', L: [3], probe: '-6 + 7 = 1 \\text{ und } 3 - 2 = 1\\ \\checkmark' },
      e: { z: 'x = 3', L: [3], probe: '-6 + 7 = 1 \\text{ und } 3 - 2 = 1\\ \\checkmark' } } }
  ]);

  /* ---------- Kapitel 2: Ausklammern und Nullprodukt (Prototyp-Kapitel des Auftraggebers) ---------- */
  umformerSim('sim2', [
    { text: 'Löse \\(2x^2 = 6x\\).', k: {
      a: { z: '2x^2 = 6x', w: [['beidseitig \\(-6x\\) (auf null bringen)', 'b', '\\mid -6x'], ['beidseitig \\(:x\\)', NULL],
        ['Fallunterscheidung: erst \\(x = 0\\) prüfen, dann \\(x \\neq 0\\)', 'f']] },
      b: { z: '2x^2 - 6x = 0', w: [['\\(2x\\) ausklammern', 'c'], ['\\(x\\) ausklammern', 'c2'],
        ['nur \\(2\\) ausklammern', '?\\(2(x^2 - 3x) = 0\\) stimmt, ist aber noch kein Produkt mit einem \\(x\\)-Faktor. Klammere so viel aus wie möglich — auch das \\(x\\).']] },
      c: { feld: { muster: '\\(2x\\,(x - \\) {a} \\() = 0\\)', soll: { a: 3 }, nach: 'd', fehler: [[{ a: -3 }, 'Vorzeichen: \\(2x \\cdot (-3) = -6x\\). In der Klammer steht \\(x - 3\\).']],
        tipp: 'Kontrolle durch Ausmultiplizieren: \\(2x \\cdot x = 2x^2\\), und \\(2x\\) mal die Zahl muss \\(-6x\\) geben.' } },
      c2: { feld: { muster: '\\(x\\,(\\) {a} \\(x - \\) {b} \\() = 0\\)', soll: { a: 2, b: 6 }, nach: 'd2', tipp: 'Kontrolle: \\(x \\cdot (\\ldots) = 2x^2 - 6x\\).' } },
      d: { z: '2x\\,(x - 3) = 0', w: [['Nullprodukt: \\(2x = 0\\) oder \\(x - 3 = 0\\)', 'e'],
        ['Nullprodukt: \\(2x = 0\\) und \\(x - 3 = 0\\)', '!«und» hiesse: beide Faktoren gleichzeitig null — das schafft kein \\(x\\). Ein Faktor null genügt: «oder».']] },
      d2: { z: 'x\\,(2x - 6) = 0', w: [['Nullprodukt: \\(x = 0\\) oder \\(2x - 6 = 0\\)', 'e'],
        ['Nullprodukt: \\(x = 0\\) und \\(2x - 6 = 0\\)', '!Ein Faktor null genügt: «oder».']] },
      e: { z: 'x = 0' + ODER + 'x = 3', L: [0, 3], Lfalsch: [[[3], 'Es fehlt \\(x = 0\\) — auch der Faktor \\(x\\) kann null sein.']], probe: '2 \\cdot 0^2 = 0 = 6 \\cdot 0;\\ \\ 2 \\cdot 3^2 = 18 = 6 \\cdot 3' },
      f: { z: '\\text{Fall } x = 0{:}\\ \\ 2 \\cdot 0^2 = 6 \\cdot 0\\ \\checkmark', w: [['Fall \\(x \\neq 0\\): beidseitig \\(:2x\\)', 'g', '\\mid :2x \\ (x \\neq 0)']] },
      g: { z: 'x = 3', frage: 'Zusammen mit dem Fall \\(x = 0\\): Gib die Lösungsmenge an.', L: [0, 3],
        Lfalsch: [[[3], 'Der Fall \\(x = 0\\) hat schon eine Lösung geliefert — sie gehört dazu.']], probe: '2 \\cdot 3^2 = 18 = 6 \\cdot 3' } } },
    { text: 'Löse \\((x - 4)(x + 1) = 0\\).', k: {
      a: { z: '(x - 4)(x + 1) = 0', w: [['Nullprodukt: \\(x - 4 = 0\\) oder \\(x + 1 = 0\\)', 'b'],
        ['ausmultiplizieren: \\(x^2 - 3x - 4 = 0\\)', '?Erlaubt, aber ein Umweg: Das Produkt steht schon da, und rechts steht \\(0\\). Nutze den Satz vom Nullprodukt.']] },
      b: { z: 'x = 4' + ODER + 'x = -1', L: [4, -1], Lfalsch: [[[-4, 1], 'Vorzeichen: \\(x - 4 = 0\\) gibt \\(x = 4\\), \\(x + 1 = 0\\) gibt \\(x = -1\\).']] } } },
    { text: 'Löse \\(-x^2 = 4x\\).', k: {
      a: { z: '-x^2 = 4x', w: [['beidseitig \\(-4x\\)', 'b', '\\mid -4x'], ['beidseitig \\(:x\\)', NULL], ['beidseitig \\(:(-x)\\)', NULL]] },
      b: { z: '-x^2 - 4x = 0', w: [['\\(-x\\) ausklammern', 'c'], ['\\(x\\) ausklammern', 'c2']] },
      c: { feld: { muster: '\\(-x\\,(x + \\) {a} \\() = 0\\)', soll: { a: 4 }, nach: 'd', fehler: [[{ a: -4 }, 'Kontrolle: \\(-x \\cdot (-4) = +4x\\), gesucht ist \\(-4x\\).']], tipp: '\\(-x \\cdot x = -x^2\\), und \\(-x\\) mal die Zahl muss \\(-4x\\) geben.' } },
      c2: { feld: { muster: '\\(x\\,(-x - \\) {a} \\() = 0\\)', soll: { a: 4 }, nach: 'd2', tipp: '\\(x \\cdot (-x) = -x^2\\), und \\(x\\) mal \\(-\\)Zahl muss \\(-4x\\) geben.' } },
      d: { z: '-x\\,(x + 4) = 0', w: [['Nullprodukt: \\(-x = 0\\) oder \\(x + 4 = 0\\)', 'e']] },
      d2: { z: 'x\\,(-x - 4) = 0', w: [['Nullprodukt: \\(x = 0\\) oder \\(-x - 4 = 0\\)', 'e']] },
      e: { z: 'x = 0' + ODER + 'x = -4', L: [0, -4], Lfalsch: [[[-4], 'Es fehlt \\(x = 0\\).'], [[0, 4], 'Vorzeichen: \\(x + 4 = 0\\) gibt \\(x = -4\\).']], probe: '-(-4)^2 = -16 = 4 \\cdot (-4)' } } },
    { text: 'Löse \\(4x^2 = 0\\).', k: {
      a: { z: '4x^2 = 0', w: [['beidseitig \\(:4\\)', 'b', '\\mid :4'], ['Nullprodukt: \\(4 = 0\\) oder \\(x^2 = 0\\)', 'b2']] },
      b: { z: 'x^2 = 0', w: [['\\(x \\cdot x = 0\\): ein Faktor null', 'c']] },
      b2: { z: '4 \\neq 0,\\ \\text{also } x^2 = x \\cdot x = 0', w: [['ein Faktor null', 'c']] },
      c: { z: 'x = 0', frage: 'Beide Faktoren sind dasselbe \\(x\\). Gib die Lösungsmenge an:', L: [0], probe: '4 \\cdot 0^2 = 0' } } },
    { text: 'Löse \\((2x - 3) \\cdot x = 0\\).', k: {
      a: { z: '(2x - 3) \\cdot x = 0', w: [['Nullprodukt: \\(2x - 3 = 0\\) oder \\(x = 0\\)', 'b'], ['beidseitig \\(:x\\)', '!Rechts steht schon \\(0\\) — das ist ein Nullprodukt. Durch \\(x\\) teilen verlöre die Lösung \\(x = 0\\).']] },
      b: { z: '2x - 3 = 0' + ODER + 'x = 0', w: [['\\(2x - 3 = 0\\) lösen: \\(x = 1.5\\)', 'c'],
        ['\\(2x - 3 = 0\\) lösen: \\(x = -1.5\\)', '!\\(2x - 3 = 0 \\mid +3\\) gibt \\(2x = 3\\), dann \\(:2\\): \\(x = 1.5\\).']] },
      c: { z: 'x = 1.5' + ODER + 'x = 0', L: [1.5, 0], Lfalsch: [[[1.5], 'Es fehlt die Lösung aus dem Faktor \\(x\\).']], probe: '(3 - 3) \\cdot 1.5 = 0;\\ \\ (0 - 3) \\cdot 0 = 0' } } },
    { text: 'Löse \\((x + 2)^2 = 5(x + 2)\\).', k: {
      a: { z: '(x + 2)^2 = 5(x + 2)', w: [['beidseitig \\(-5(x + 2)\\)', 'b', '\\mid -5(x + 2)'],
        ['beidseitig \\(:(x + 2)\\)', '!Division durch \\(x + 2\\) setzt \\(x \\neq -2\\) voraus — die Lösung \\(x = -2\\) ginge verloren.'],
        ['alles ausmultiplizieren', '?Geht, aber dann musst du neu faktorisieren. Der gemeinsame Faktor \\((x + 2)\\) steht schon da.']] },
      b: { z: '(x + 2)^2 - 5(x + 2) = 0', w: [['\\((x + 2)\\) ausklammern', 'c']] },
      c: { feld: { muster: '\\((x + 2)(x - \\) {a} \\() = 0\\)', soll: { a: 3 }, nach: 'd', fehler: [[{ a: 7 }, 'Ausgeklammert bleibt \\((x + 2) - 5 = x - 3\\).'], [{ a: 5 }, 'Ausgeklammert bleibt \\((x + 2) - 5\\) — die \\(+2\\) gehört mit in die Klammer.']],
        tipp: 'Klammert man \\((x + 2)\\) aus, bleibt von \\((x + 2)^2\\) noch \\((x + 2)\\) und von \\(5(x + 2)\\) die \\(5\\): \\((x + 2)\\,[(x + 2) - 5]\\).' } },
      d: { z: '(x + 2)(x - 3) = 0', w: [['Nullprodukt: \\(x + 2 = 0\\) oder \\(x - 3 = 0\\)', 'e']] },
      e: { z: 'x = -2' + ODER + 'x = 3', L: [-2, 3], Lfalsch: [[[3], 'Es fehlt die Lösung aus dem Faktor \\(x + 2\\).']], probe: '0^2 = 0 = 5 \\cdot 0;\\ \\ 5^2 = 25 = 5 \\cdot 5' } } }
  ]);

  /* ---------- Kapitel 3: Wurzelziehen, quadratische Ergänzung, Mitternachtsformel ---------- */
  umformerSim('sim3', [
    { text: 'Löse \\(2x^2 - 50 = 0\\).', k: {
      a: { z: '2x^2 - 50 = 0', w: [['beidseitig \\(+50\\)', 'b', '\\mid +50'],
        ['Wurzel ziehen: \\(\\sqrt2\\,x - \\sqrt{50} = 0\\)', '!Aus einer Summe oder Differenz darf man nicht gliedweise die Wurzel ziehen. Bring zuerst \\(x^2\\) allein auf eine Seite.']] },
      b: { z: '2x^2 = 50', w: [['beidseitig \\(:2\\)', 'c', '\\mid :2']] },
      c: { z: 'x^2 = 25', w: [['Wurzel ziehen: \\(x = \\pm 5\\)', 'd'], ['Wurzel ziehen: \\(x = 5\\)', '!Auch \\((-5)^2 = 25\\). Zu \\(x^2 = 25\\) gehören zwei Lösungen.']] },
      d: { z: 'x = -5' + ODER + 'x = 5', L: [-5, 5], Lfalsch: [[[5], 'Es fehlt \\(-5\\): \\((-5)^2 = 25\\).']] } } },
    { text: 'Löse \\((x + 1)^2 = 16\\).', k: {
      a: { z: '(x + 1)^2 = 16', w: [['Wurzel ziehen: \\(x + 1 = \\pm 4\\)', 'b'], ['Wurzel ziehen: \\(x + 1 = 4\\)', '!Auch \\((-4)^2 = 16\\): \\(x + 1\\) kann \\(4\\) oder \\(-4\\) sein.'],
        ['ausmultiplizieren', '?Geht, ist aber ein Umweg: Links steht schon ein Quadrat. Zieh die Wurzel.']] },
      b: { z: 'x + 1 = 4' + ODER + 'x + 1 = -4', w: [['beidseitig \\(-1\\)', 'c', '\\mid -1']] },
      c: { z: 'x = 3' + ODER + 'x = -5', L: [3, -5], Lfalsch: [[[-3, 5], 'Vorzeichen: Von beiden Seiten \\(1\\) abziehen: \\(4 - 1 = 3\\), \\(-4 - 1 = -5\\).']] } } },
    { text: 'Löse \\(x^2 + 6x = 7\\) mit quadratischer Ergänzung.', k: {
      a: { z: 'x^2 + 6x = 7', w: [['quadratisch ergänzen: beidseitig \\(+9\\)', 'b', '\\mid +9'],
        ['quadratisch ergänzen: beidseitig \\(+36\\)', '!Ergänzt wird das Quadrat der <b>halben</b> Zahl vor \\(x\\): \\(\\left(\\tfrac{6}{2}\\right)^2 = 9\\).'],
        ['quadratisch ergänzen: beidseitig \\(+3\\)', '!Ergänzt wird das <b>Quadrat</b> der halben Zahl: \\(\\left(\\tfrac{6}{2}\\right)^2 = 9\\), nicht \\(\\tfrac{6}{2}\\).']] },
      b: { z: 'x^2 + 6x + 9 = 16', w: [['links Binom: \\((x + 3)^2 = 16\\)', 'c'], ['links Binom: \\((x + 9)^2 = 16\\)', '!\\((x + 9)^2 = x^2 + 18x + 81\\). Gesucht ist \\((x + 3)^2 = x^2 + 6x + 9\\).']] },
      c: { z: '(x + 3)^2 = 16', w: [['Wurzel ziehen: \\(x + 3 = \\pm 4\\)', 'd'], ['Wurzel ziehen: \\(x + 3 = 4\\)', '!Auch \\(-4\\) hat das Quadrat \\(16\\).']] },
      d: { z: 'x + 3 = 4' + ODER + 'x + 3 = -4', w: [['beidseitig \\(-3\\)', 'e', '\\mid -3']] },
      e: { z: 'x = 1' + ODER + 'x = -7', L: [1, -7], probe: '1 + 6 = 7;\\ \\ 49 - 42 = 7' } } },
    { text: 'Löse \\(x^2 - 8x + 12 = 0\\) mit quadratischer Ergänzung.', k: {
      a: { z: 'x^2 - 8x + 12 = 0', w: [['beidseitig \\(-12\\)', 'b', '\\mid -12'],
        ['quadratisch ergänzen: beidseitig \\(+16\\)', '?Erlaubt: \\((x - 4)^2 + 12 = 16\\). Einfacher: zuerst die Zahl ohne \\(x\\) auf die rechte Seite — dann steht links ein reines Binom.']] },
      b: { z: 'x^2 - 8x = -12', w: [['quadratisch ergänzen: beidseitig \\(+16\\)', 'c', '\\mid +16'], ['quadratisch ergänzen: beidseitig \\(+64\\)', '!Die <b>halbe</b> Zahl vor \\(x\\) quadrieren: \\(\\left(\\tfrac{-8}{2}\\right)^2 = 16\\).']] },
      c: { z: 'x^2 - 8x + 16 = 4', w: [['links Binom: \\((x - 4)^2 = 4\\)', 'd'], ['links Binom: \\((x + 4)^2 = 4\\)', '!Das lineare Glied ist \\(-8x\\): \\((x - 4)^2 = x^2 - 8x + 16\\).']] },
      d: { z: '(x - 4)^2 = 4', w: [['Wurzel ziehen: \\(x - 4 = \\pm 2\\)', 'e']] },
      e: { z: 'x - 4 = 2' + ODER + 'x - 4 = -2', w: [['beidseitig \\(+4\\)', 'f', '\\mid +4']] },
      f: { z: 'x = 6' + ODER + 'x = 2', L: [6, 2], probe: '36 - 48 + 12 = 0;\\ \\ 4 - 16 + 12 = 0' } } },
    { text: 'Löse \\(3x^2 - 5x - 2 = 0\\) mit der Mitternachtsformel.', k: {
      a: { z: '3x^2 - 5x - 2 = 0', frage: 'Lies die Koeffizienten ab — samt Vorzeichen:', feld: { muster: '\\(a = \\) {a}; \\(b = \\) {b}; \\(c = \\) {c}', soll: { a: 3, b: -5, c: -2 }, nach: 'b',
        fehler: [[{ a: 3, b: 5, c: -2 }, 'Vorzeichen von \\(b\\): Vor \\(5x\\) steht ein Minus, \\(b = -5\\).'], [{ a: 3, b: -5, c: 2 }, 'Vorzeichen von \\(c\\): \\(c = -2\\).'], [{ a: 3, b: 5, c: 2 }, 'Die Vorzeichen gehören zu den Zahlen: \\(b = -5\\), \\(c = -2\\).']],
        tipp: '\\(a\\) steht vor \\(x^2\\), \\(b\\) vor \\(x\\), \\(c\\) ist die Zahl ohne \\(x\\).' } },
      b: { z: 'a = 3,\\ b = -5,\\ c = -2', frage: 'Berechne die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: 49 }, nach: 'c',
        fehler: [[{ D: 1 }, 'Vorzeichen: \\(-4 \\cdot 3 \\cdot (-2) = +24\\), also \\(D = 25 + 24\\).'], [{ D: -1 }, '\\(b^2 = (-5)^2 = +25\\), und \\(-4 \\cdot 3 \\cdot (-2) = +24\\).'], [{ D: -49 }, '\\(b^2 = (-5)^2 = +25\\), nicht \\(-25\\).']],
        tipp: '\\(D = (-5)^2 - 4 \\cdot 3 \\cdot (-2)\\).' } },
      c: { z: 'D = 49,\\ \\sqrt{D} = 7', w: [['einsetzen: \\(x = \\dfrac{5 \\pm 7}{6}\\)', 'd'], ['einsetzen: \\(x = \\dfrac{-5 \\pm 7}{6}\\)', '!Vorne steht \\(-b\\), und \\(b = -5\\): \\(-b = 5\\).'],
        ['einsetzen: \\(x = \\dfrac{5 \\pm 7}{3}\\)', '!Der Nenner ist \\(2a = 6\\).']] },
      d: { z: 'x = \\tfrac{12}{6} = 2' + ODER + 'x = \\tfrac{-2}{6} = -\\tfrac{1}{3}', L: [2, -1 / 3], probe: '12 - 10 - 2 = 0;\\ \\ \\tfrac{1}{3} + \\tfrac{5}{3} - 2 = 0' } } },
    { text: 'Löse \\(x^2 + 2x + 5 = 0\\) mit der Mitternachtsformel.', k: {
      a: { z: 'x^2 + 2x + 5 = 0', frage: 'Berechne zuerst die Diskriminante:', feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: -16 }, nach: 'b',
        fehler: [[{ D: 24 }, '\\(4ac = 4 \\cdot 1 \\cdot 5 = 20\\) wird <b>abgezogen</b>: \\(D = 4 - 20\\).'], [{ D: 16 }, 'Vorzeichen: \\(4 - 20 = -16\\).']], tipp: '\\(D = 2^2 - 4 \\cdot 1 \\cdot 5\\).' } },
      b: { z: 'D = 4 - 20 = -16 \\lt 0', frage: 'Was folgt aus \\(D \\lt 0\\)? Gib die Lösungsmenge an:', L: [],
        Lfalsch: [['R', 'Bei \\(D \\lt 0\\) gibt es keine reelle Wurzel aus \\(D\\) — also keine Lösung, nicht alle Zahlen.']] } } },
    { text: 'Löse \\(4x^2 - 12x + 9 = 0\\).', k: {
      a: { z: '4x^2 - 12x + 9 = 0', w: [['Mitternachtsformel', 'b'], ['Binom erkennen: \\((2x - 3)^2 = 0\\)', 'c'], ['Binom erkennen: \\((4x - 3)^2 = 0\\)', '!\\((4x - 3)^2 = 16x^2 - 24x + 9\\). Vorne steht \\(4x^2 = (2x)^2\\).']] },
      b: { feld: { muster: '\\(D = b^2 - 4ac = \\) {D}', soll: { D: 0 }, nach: 'b2', tipp: '\\(D = (-12)^2 - 4 \\cdot 4 \\cdot 9 = 144 - 144\\).' } },
      b2: { z: 'D = 0', w: [['einsetzen: \\(x = \\dfrac{12 \\pm 0}{8}\\)', 'd']] },
      c: { z: '(2x - 3)^2 = 0', w: [['\\(2x - 3 = 0\\)', 'c2']] },
      c2: { z: '2x - 3 = 0', w: [['beidseitig \\(+3\\), dann \\(:2\\)', 'd', '\\mid +3;\\ :2']] },
      d: { z: 'x = 1.5', frage: 'Nur eine Lösung — eine doppelte. Gib die Lösungsmenge an:', L: [1.5], probe: '9 - 18 + 9 = 0' } } }
  ]);

  /* ---------- Kapitel 4: das passende Verfahren ---------- */
  /* Zweiklammersatz wie auf Themenseite 2.2b: gesucht sind die Lösungen x₁, x₂ mit x₁ + x₂ = −p und
     x₁ · x₂ = q; dann ist x² + px + q = (x − x₁)(x − x₂). Eine Lesart im ganzen Leitprogramm (Prüfung 06.10.2026, M2). */
  function zweiklammer(p, q, nach){
    var w = Math.sqrt(p * p - 4 * q), r1 = (-p - w) / 2, r2 = (-p + w) / 2;
    return { muster: '\\((x - \\) {m} \\()(x - \\) {n} \\() = 0\\)', nach: nach, beispiel: { m: r1, n: r2 },
      pruef: function(e){
        if (gl(e.m + e.n, -p) && gl(e.m * e.n, q)) return null;
        if (gl(e.m * e.n, q) && gl(e.m + e.n, p)) return 'Das Produkt stimmt, die Summe hat das falsche Vorzeichen. Die Lösungen haben die Summe \\(-p = ' + tz(-p) + '\\) und das Produkt \\(q = ' + tz(q) + '\\).';
        if (gl(e.m + e.n, -p)) return 'Die Summe stimmt, das Produkt nicht: \\(' + tz(e.m) + ' \\cdot ' + tz(e.n) + ' \\neq ' + tz(q) + '\\).';
        return 'Gesucht sind die Lösungen: Summe \\(-p = ' + tz(-p) + '\\), Produkt \\(q = ' + tz(q) + '\\).';
      } };
  }
  umformerSim('sim4', [
    { text: 'Löse \\(x^2 - 9x + 20 = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: 'x^2 - 9x + 20 = 0', frage: 'Welches Verfahren?', w: [['Faktorisieren (Zweiklammersatz)', 'b'],
        ['Mitternachtsformel', 'm', '', 'Geht immer. Hier hätte auch der Zweiklammersatz gereicht: zwei Lösungen mit Summe \\(9\\) und Produkt \\(20\\).'],
        ['Ausklammern', '!Ausklammern hilft, wenn jedes Glied ein \\(x\\) hat. Hier steht \\(+20\\).'], ['Wurzelziehen', '!Wurzelziehen geht, wenn das Glied mit \\(x\\) fehlt. Hier steht \\(-9x\\).']] },
      b: { frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(9\\) und das Produkt \\(20\\):', feld: zweiklammer(-9, 20, 'c') },
      c: { z: '(x - 4)(x - 5) = 0', w: [['Nullprodukt', 'd']] },
      m: { frage: 'Diskriminante:', feld: { muster: '\\(D = \\) {D}', soll: { D: 1 }, nach: 'm2', tipp: '\\(D = (-9)^2 - 4 \\cdot 1 \\cdot 20\\).' } },
      m2: { z: 'D = 81 - 80 = 1', w: [['einsetzen: \\(x = \\dfrac{9 \\pm 1}{2}\\)', 'd']] },
      d: { z: 'x = 4' + ODER + 'x = 5', L: [4, 5], Lfalsch: [[[-4, -5], 'Vorzeichen: \\(x - 4 = 0\\) gibt \\(x = 4\\).']] } } },
    { text: 'Löse \\(5x^2 = 45\\). Wähle zuerst das Verfahren.', k: {
      a: { z: '5x^2 = 45', frage: 'Welches Verfahren?', w: [['Wurzelziehen', 'c', '\\mid :5'],
        ['Ausklammern', '?Geht: \\(5x^2 - 45 = 5(x^2 - 9) = 5(x - 3)(x + 3)\\). Schneller: nach \\(x^2\\) auflösen und die Wurzel ziehen.'],
        ['Mitternachtsformel', 'm', '', 'Geht, mit \\(b = 0\\). Schneller: nach \\(x^2\\) auflösen und die Wurzel ziehen.']] },
      c: { z: 'x^2 = 9', w: [['Wurzel ziehen: \\(x = \\pm 3\\)', 'd'], ['Wurzel ziehen: \\(x = 3\\)', '!Auch \\((-3)^2 = 9\\).']] },
      m: { z: '5x^2 - 45 = 0', frage: 'Diskriminante (\\(b = 0\\)):', feld: { muster: '\\(D = \\) {D}', soll: { D: 900 }, nach: 'm2', tipp: '\\(D = 0^2 - 4 \\cdot 5 \\cdot (-45)\\).' } },
      m2: { z: 'D = 900,\\ \\sqrt{D} = 30', w: [['einsetzen: \\(x = \\dfrac{0 \\pm 30}{10}\\)', 'd']] },
      d: { z: 'x = -3' + ODER + 'x = 3', L: [-3, 3], Lfalsch: [[[3], 'Es fehlt \\(-3\\).']] } } },
    { text: 'Löse \\(x^2 + 10x + 25 = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: 'x^2 + 10x + 25 = 0', frage: 'Welches Verfahren?', w: [['Binom erkennen', 'b'],
        ['Mitternachtsformel', 'm', '', 'Geht. Schneller: \\(x^2 + 10x + 25\\) ist ein Binom.'], ['Ausklammern', '!Hier steht \\(+25\\) ohne \\(x\\) — ausklammern geht nicht.']] },
      b: { frage: 'Welches Binom?', feld: { muster: '\\((x + \\) {a} \\()^2 = 0\\)', soll: { a: 5 }, nach: 'c', fehler: [[{ a: 25 }, '\\((x + 25)^2\\) gäbe \\(50x\\). Gesucht: \\(2 \\cdot 5 = 10\\) und \\(5^2 = 25\\).'], [{ a: -5 }, '\\((x - 5)^2 = x^2 - 10x + 25\\). Hier steht \\(+10x\\).']], tipp: '\\((x + a)^2 = x^2 + 2a\\,x + a^2\\).' } },
      c: { z: '(x + 5)^2 = 0', w: [['\\(x + 5 = 0\\)', 'd']] },
      m: { feld: { muster: '\\(D = \\) {D}', soll: { D: 0 }, nach: 'm2', tipp: '\\(D = 10^2 - 4 \\cdot 1 \\cdot 25\\).' } },
      m2: { z: 'D = 0', w: [['einsetzen: \\(x = \\dfrac{-10}{2}\\)', 'd']] },
      d: { z: 'x = -5', L: [-5], Lfalsch: [[[5], 'Vorzeichen: \\(x + 5 = 0\\) gibt \\(x = -5\\).']] } } },
    { text: 'Löse \\((x - 2)^2 = x^2 - 8\\).', k: {
      a: { z: '(x - 2)^2 = x^2 - 8', frage: 'Erst umformen, dann den Typ bestimmen:', w: [['Binom ausmultiplizieren: \\(x^2 - 4x + 4 = x^2 - 8\\)', 'b'],
        ['Binom ausmultiplizieren: \\(x^2 + 4 = x^2 - 8\\)', '!\\((x - 2)^2 = x^2 - 4x + 4\\) — das mittlere Glied \\(-4x\\) fehlt.'],
        ['Wurzel ziehen: \\(x - 2 = \\pm\\sqrt{x^2 - 8}\\)', '!Rechts steht kein Quadrat einer Zahl — so kommst du nicht weiter. Multipliziere aus und schau, was übrig bleibt.']] },
      b: { z: 'x^2 - 4x + 4 = x^2 - 8', w: [['beidseitig \\(-x^2\\)', 'c', '\\mid -x^2']] },
      c: { z: '-4x + 4 = -8', frage: 'Was für eine Gleichung ist das jetzt?', w: [['linear — weiter mit \\(-4\\)', 'd', '\\mid -4'], ['quadratisch — Mitternachtsformel', '!\\(x^2\\) hat sich weggehoben: Die Gleichung ist linear.']] },
      d: { z: '-4x = -12', w: [['beidseitig \\(:(-4)\\)', 'e', '\\mid :(-4)']] },
      e: { z: 'x = 3', L: [3], Lfalsch: [[[-3], 'Vorzeichen: \\(-12 : (-4) = 3\\).']], probe: '(3 - 2)^2 = 1 = 9 - 8' } } },
    { text: 'Löse \\(x\\,(x + 3) = 10\\).', k: {
      a: { z: 'x\\,(x + 3) = 10', w: [['Nullprodukt: \\(x = 10\\) oder \\(x + 3 = 10\\)', '!Rechts steht \\(10\\), nicht \\(0\\). Der Satz vom Nullprodukt gilt nur, wenn das Produkt null ist.'],
        ['ausmultiplizieren und auf null bringen', 'b', '\\mid -10']] },
      b: { z: 'x^2 + 3x - 10 = 0', frage: 'Welches Verfahren?', w: [['Faktorisieren (Zweiklammersatz)', 'c'], ['Mitternachtsformel', 'm']] },
      c: { frage: 'Die Lösungen \\(x_1\\), \\(x_2\\) haben die Summe \\(-3\\) und das Produkt \\(-10\\):', feld: zweiklammer(3, -10, 'd') },
      d: { z: '(x + 5)(x - 2) = 0', w: [['Nullprodukt', 'e']] },
      m: { feld: { muster: '\\(D = \\) {D}', soll: { D: 49 }, nach: 'm2', tipp: '\\(D = 3^2 - 4 \\cdot 1 \\cdot (-10)\\).', fehler: [[{ D: -31 }, '\\(-4 \\cdot 1 \\cdot (-10) = +40\\).']] } },
      m2: { z: 'D = 9 + 40 = 49', w: [['einsetzen: \\(x = \\dfrac{-3 \\pm 7}{2}\\)', 'e']] },
      e: { z: 'x = -5' + ODER + 'x = 2', L: [-5, 2], Lfalsch: [[[5, -2], 'Vorzeichen: \\(x + 5 = 0\\) gibt \\(x = -5\\).']], probe: '-5 \\cdot (-2) = 10;\\ \\ 2 \\cdot 5 = 10' } } },
    { text: 'Löse \\(6x^2 + x - 2 = 0\\). Wähle zuerst das Verfahren.', k: {
      a: { z: '6x^2 + x - 2 = 0', frage: 'Welches Verfahren?', w: [['Mitternachtsformel', 'b'],
        ['Faktorisieren (Zweiklammersatz)', '!Der Zweiklammersatz \\((x - x_1)(x - x_2)\\) braucht \\(1\\) vor \\(x^2\\). Hier steht \\(6\\) — die Formel ist sicherer.'],
        ['Wurzelziehen', '!Hier steht ein Glied mit \\(x\\). Wurzelziehen allein reicht nicht.']] },
      b: { feld: { muster: '\\(a = \\) {a}; \\(b = \\) {b}; \\(c = \\) {c}', soll: { a: 6, b: 1, c: -2 }, nach: 'c', tipp: '\\(b\\) steht vor \\(x\\) — dort steht unsichtbar eine \\(1\\).' } },
      c: { z: 'a = 6,\\ b = 1,\\ c = -2', feld: { muster: '\\(D = \\) {D}', soll: { D: 49 }, nach: 'd', fehler: [[{ D: -47 }, '\\(-4 \\cdot 6 \\cdot (-2) = +48\\).']], tipp: '\\(D = 1^2 - 4 \\cdot 6 \\cdot (-2)\\).' } },
      d: { z: 'D = 49', w: [['einsetzen: \\(x = \\dfrac{-1 \\pm 7}{12}\\)', 'e'], ['einsetzen: \\(x = \\dfrac{-1 \\pm 7}{6}\\)', '!Der Nenner ist \\(2a = 12\\).']] },
      e: { z: 'x = \\tfrac{6}{12} = \\tfrac{1}{2}' + ODER + 'x = \\tfrac{-8}{12} = -\\tfrac{2}{3}', L: [0.5, -2 / 3], probe: '\\tfrac{6}{4} + \\tfrac{1}{2} - 2 = 0;\\ \\ 6 \\cdot \\tfrac{4}{9} - \\tfrac{2}{3} - 2 = 0' } } }
  ]);

  /* ---------- Kapitel 5: Parameterdiskussion ----------
     Unterschied zu den Animationen «Parameter» (2.2a) und «Parameter k» (2.2b): Drei Familien in einer
     Figur, auch der Fall, in dem der Leitkoeffizient null wird; die Anzeige nennt die Zwischenform,
     D(k) und den Lösungsfall. Startwert k = 2: keine Aufgabe ist schon gelöst, auch nicht nach
     einem Wechsel der Familie (A: D = 8, B: x = 3, C: D = −4). */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 280, x0: -4, x1: 6, y0: -6, y1: 8, xm: [-2, 2, 4], ym: [-4, -2, 2, 4, 6] });
    var kr = fig.querySelector('input[data-p="k"]'), fam = fig.querySelector('.sim-wahl'), bewegt = {}, pruefen = function(){};
    kr.addEventListener('input', function(){ bewegt.k = true; zeichnen(); });
    fam.addEventListener('change', zeichnen);
    function zust(){
      var k = +kr.value, f = fam.value, L, fall, D = null;
      kr.parentNode.querySelector('.sl-val').textContent = z(k);
      if (f === 'A'){ D = 16 - 4 * k; L = D > 0 ? [2 - Math.sqrt(D) / 2, 2 + Math.sqrt(D) / 2] : D === 0 ? [2] : []; }
      else if (f === 'B'){ L = k === 1 ? 'R' : [k + 1]; }
      else { if (k === 0) L = [-0.5]; else { D = 4 - 4 * k; L = D > 0 ? [(-2 - Math.sqrt(D)) / (2 * k), (-2 + Math.sqrt(D)) / (2 * k)].sort(function(a, b){ return a - b; }) : D === 0 ? [-1 / k] : []; } }
      return { k: k, fam: f, D: D, L: L, n: L === 'R' ? Infinity : L.length, bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; fam.value = 'A'; } };
    function kT(k){ return k < 0 ? '(' + z(k) + ')' : z(k); }
    function zeichnen(){
      var s = zust(), k = s.k, txt;
      K.leeren();
      if (s.fam === 'A'){
        K.kurve(function(x){ return x * x - 4 * x + k; }, 'kurve');
        txt = sp('tx-blau', 'x² − 4x' + (k === 0 ? '' : k < 0 ? ' − ' + sp('tx-orange', z(-k)) : ' + ' + sp('tx-orange', z(k))) + ' = 0') + '<br>D = 16 − 4 · ' + kT(k) + ' = ' + z(s.D);
      } else if (s.fam === 'B'){
        K.kurve(function(x){ return (k - 1) * x; }, 'kurve');
        K.kurve(function(){ return k * k - 1; }, 'kurve rechts');
        txt = sp('tx-blau', '(' + sp('tx-orange', 'k') + ' − 1) · x = ' + sp('tx-orange', 'k') + '² − 1') + ' mit k = ' + z(k) + ':<br>' + z(k - 1) + ' · x = ' + z(k * k - 1)
          + '; &nbsp;<span class="nb">links y = ' + (k - 1 === 0 ? '0' : k - 1 === 1 ? 'x' : k - 1 === -1 ? '−x' : z(k - 1) + 'x') + ', rechts y = ' + z(k * k - 1) + '</span>'
          + (k * k - 1 > 8 ? '<br><span class="nb">(Schnittpunkt oberhalb des Bildes)</span>' : '');
      } else {
        K.kurve(function(x){ return k * x * x + 2 * x + 1; }, 'kurve');
        txt = sp('tx-blau', sp('tx-orange', kT(k)) + ' · x² + 2x + 1 = 0') + (k === 0 ? '<br>k = 0: linear, 2x + 1 = 0' : '<br>D = 4 − 4 · ' + kT(k) + ' = ' + z(s.D));
      }
      if (s.L !== 'R') s.L.forEach(function(x){ K.punkt(x, s.fam === 'B' ? k * k - 1 : 0, 'p-loes'); });
      var fall = s.L === 'R' ? 'jede Zahl ist Lösung: 𝕃 = ℝ' : !s.L.length ? 'keine Lösung: 𝕃 = { }' : s.L.length === 1 ? 'genau eine Lösung: 𝕃 = {' + zz(s.L[0]) + '}' : 'zwei Lösungen: 𝕃 = {' + zz(s.L[0]) + '; ' + zz(s.L[1]) + '}';
      fig.querySelector('[data-rolle="formel"]').innerHTML = txt + '<br>' + sp('tx-gruen', fall);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde Familie A: Zieh an \\(k\\). Wann gibt es zwei, eine, keine Lösung?', ok: function(s){ return s.fam === 'A' && s.bewegt.k; } },
      { text: 'Familie A: Stell \\(k\\) so ein, dass es genau <b>eine</b> Lösung gibt.', ok: function(s){ return s.fam === 'A' && s.k === 4; } },
      { text: 'Familie A: Die Lösungen sollen \\(1\\) und \\(3\\) sein.', ok: function(s){ return s.fam === 'A' && s.k === 3; } },
      { text: 'Wähle Familie B. Für welches \\(k\\) ist jede Zahl eine Lösung?', ok: function(s){ return s.fam === 'B' && s.k === 1; } },
      { text: 'Familie B: Die Lösung soll \\(x = 0.5\\) sein.', ok: function(s){ return s.fam === 'B' && s.k === -0.5; } },
      { text: 'Wähle Familie C. Für welches \\(k\\) wird die Gleichung linear?', ok: function(s){ return s.fam === 'C' && s.k === 0; } },
      { text: 'Familie C: Stell eine <b>doppelte</b> Lösung ein.', ok: function(s){ return s.fam === 'C' && s.k === 1; } }
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

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Umformer ·
       Aufgaben der Kapitel · Vortest · Gesamttest. Je Typ ein eigener Schlüssel (T.schl). */
    var SPERRE = [
      // Kapitel 1 (lineare: a|b|c|d für ax + b = cx + d)
      'li|4|-8|2|6', 'li|3|4|1|-6', 'li|5|-5|2|4', 'li|7|-4|3|12', 'li|4|-11|0|1', 'li|5|-6|3|4', 'li|3|-4|1|0',
      // Kapitel 2 (ausklammern: a|b für ax² + bx = 0; nullprodukt: Faktoren)
      'ak|1|-5', 'ak|2|-6', 'ak|-1|-4', 'ak|4|0', 'ak|3|12', 'ak|1|2', 'ak|1|3', 'ak|4|-20', 'ak|1|4', 'ak|3|-6',
      'np|4|1|1', 'np|2|1|1', 'np|0|1|3', 'np|0|2|-3',
      // Kapitel 3 (wurzel: p|q für (x − p)² = q; mitternacht: a|b|c)
      'wu|2|9', 'wu|-1|16', 'wu|-3|16', 'wu|4|4', 'wu|3|4', 'wu|3|25', 'wu|-3|25',
      'mi|2|3|-2', 'mi|3|-5|-2', 'mi|1|2|5', 'mi|4|-12|9', 'mi|2|-7|3', 'mi|2|-5|2', 'mi|1|-4|-5', 'mi|1|-2|-3', 'mi|1|4|-21', 'mi|1|6|-16',
      // Kapitel 4 (zweiklammer: p|q für x² + px + q)
      'zk|-7|12', 'zk|-9|20', 'zk|3|-10', 'zk|-7|10', 'zk|1|-12', 'zk|-1|-12', 'zk|1|-6', 'zk|-1|-2', 'zk|2|-24', 'zk|10|25', 'zk|-6|9',
      // Lösungsfall (lf: p|q|s|r für p(x + q) = s x + r): 1d, Umformer 1 A3, Clip, Kontrollclip, Gesamttest G2
      'lf|4|-1|4|-4', 'lf|3|2|3|5', 'lf|2|3|2|9', 'lf|3|1|3|3', 'lf|2|-3|2|-6', 'lf|3|-2|3|-6', 'lf|3|-2|3|-5', 'lf|3|-2|3|0',
      // Kapitel 5 (pl: a|art; pq: b für x² + bx + k)
      'pl|2|A', 'pl|3|A', 'pl|3|B', 'pq|-6', 'pq|2', 'pq|-4', 'pq|8', 'pq|-10'
    ];
    /* Alle festen quadratischen Gleichungen des Leitprogramms als Normalform a|b|c (gekürzt, a > 0):
       Clips, Umformer, Kapitelaufgaben, Vortest, Gesamttest. Jeder quadratische Übungstyp nennt seine
       Normalform (T.quad) — so sperrt ein Eintrag alle Schreibweisen derselben Gleichung (Prüfung 06.10.2026, H4). */
    var FESTE_Q = [
      [1, -5, 0], [2, 3, -2], [1, -4, -5], [1, 0, -9], [1, 0, -25], [1, 0, -16], [1, 4, 0], [1, -7, 12], [1, -7, 10], [1, -6, 9],
      [1, 1, -12], [1, 3, 0], [1, -2, -3], [3, 0, -27], [2, 1, -4], [1, 0, -4],
      [2, -6, 0], [1, -3, -4], [4, 0, 0], [2, -3, 0], [1, -1, -6], [2, 0, -50], [1, 2, -15], [1, 6, -7], [1, -8, 12], [3, -5, -2],
      [1, 2, 5], [4, -12, 9], [1, -9, 20], [5, 0, -45], [1, 10, 25], [1, 3, -10], [6, 1, -2],
      [3, 12, 0], [1, -1, -2], [1, -5, 4], [1, 2, 0], [100, 0, -49], [1, 4, -21], [2, -7, 3], [1, -6, 10], [9, 6, 1], [1, 1, -1],
      [1, -4, 3], [4, 0, -1], [3, -6, 0], [1, -1, -12], [1, 1, -6], [1, -4, 1], [1, -4, 0], [1, 8, 12], [1, 8, 16], [1, 8, 20],
      [1, -10, 25], [1, 0, -49],
      [1, -1, -20], [1, -6, 5], [1, -2, -1], [4, 0, -9], [1, 6, 9], [2, 5, -1]
    ];
    function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
    function qSchl(q){ var a = q[0], b = q[1], c = q[2]; if (a < 0){ a = -a; b = -b; c = -c; }
      var g = ggT(ggT(a, b), c) || 1; return [a / g, b / g, c / g].join('|'); }
    var SPERRE_Q = FESTE_Q.map(qSchl);
    function gesperrt(T, A){ return (T.schl && SPERRE.indexOf(T.schl(A)) >= 0) || (T.quad && SPERRE_Q.indexOf(qSchl(T.quad(A))) >= 0); }
    /* So tippt man die Menge ein: Drittel und Sechstel als Bruch, sonst Dezimalzahl. */
    function zText(v){
      for (var d of [1, 3, 6]){ var n = Math.round(v * d); if (gl(v * d, n)) return d === 1 ? String(n) : (d === 6 && n % 2 === 0 ? (n / 2) + '/3' : n + '/' + d); }
      return String(Math.round(v * 1000) / 1000);
    }
    function mText(L){ return L === 'R' ? 'R' : '{' + L.map(zText).join('; ') + '}'; }
    /* Gerundete Drittel (0.33 statt 1/3): fast richtig — eigene Rückmeldung statt «falsch gerechnet». */
    function fast(m, soll){
      return soll !== 'R' && !m.alle && m.werte.length === soll.length &&
        soll.every(function(v){ return m.werte.some(function(w){ return Math.abs(v - w) < 0.006; }); });
    }
    var FAST = 'Fast — schreib Drittel und Sechstel als Bruch, zum Beispiel <code>-2/3</code>: \\(0.33\\) ist nicht genau \\(\\tfrac{1}{3}\\).';

    var TYPEN = {
      /* ── Kapitel 1 ─────────────────────────────────────────────── */
      'linear-loesen': { felder: ['x'], muster: 'x = {x}',
        schl: function(A){ return 'li|' + A.a + '|' + A.b + '|' + A.c + '|' + A.d; },
        neu: function(){
          var a, c, x, b, d;
          do { a = zufallG(-4, 8); c = zufallG(-4, 6); } while (a === c || a === 0 || a - c === 1 && Math.random() < 0.7);
          x = zufallG(-6, 6); b = zufallG(-9, 9); d = (a - c) * x + b;
          return { a: a, b: b, c: c, d: d, x: x, text: 'Löse \\(' + lin(a, b) + ' = ' + lin(c, d) + '\\).' }; },
        fehler: function(A){
          var f = [], k1 = (A.d + A.b) / (A.a - A.c), k2 = (A.d - A.b) / (A.a + A.c);
          if (!gl(k1, A.x) && isFinite(k1)) f.push([{ x: String(k1) }, 'Vorzeichen']);
          if (A.a + A.c !== 0 && !gl(k2, A.x) && !gl(k2, k1) && !gl(k2, -A.x)) f.push([{ x: String(k2) }, 'Glied rechts']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          if (gl(e.x, (A.d + A.b) / (A.a - A.c))) return 'Vorzeichen beim Hinüberbringen: Steht links \\(' + (A.b < 0 ? '-' + (-A.b) : '+' + A.b) + '\\), rechnest du beidseitig \\(' + (A.b < 0 ? '+' + (-A.b) : '-' + A.b) + '\\).';
          if (gl(e.x, -A.x)) return 'Vorzeichen: Am Schluss durch \\(' + tz(A.a - A.c) + '\\) teilen — samt Vorzeichen.';
          if (A.a + A.c !== 0 && gl(e.x, (A.d - A.b) / (A.a + A.c))) return 'Das \\(x\\)-Glied rechts: beidseitig \\(' + (A.c < 0 ? '+' + (-A.c) : '-' + A.c) + 'x\\), nicht addieren.';
          return 'Sammle die \\(x\\)-Glieder links und die Zahlen rechts, dann teilen. Mach die Probe.'; },
        loesung: function(A){ return lin(A.a - A.c, 0) + ' = ' + (A.d - A.b) + '\\ \\Rightarrow\\ x = ' + A.x; } },

      'loesungsfall': { felder: ['fall', 'L'], muster: '{fall:genau eine Lösung|keine Lösung|jede Zahl ist Lösung}; 𝕃 = {L}',
        schl: function(A){ return 'lf|' + A.p + '|' + A.q + '|' + A.s + '|' + A.r; },
        eingabe: function(A){ return { fall: A.fall, L: mText(A.L) }; },
        neu: function(){
          // p(x + q) = s x + r: s = p und r = pq → alle; s = p, r ≠ pq → keine; s ≠ p → eine (ganzzahlig)
          var p = zufall([2, 3, 4, 5, -2, -3]), q = zufall([-4, -3, -2, -1, 1, 2, 3, 5]), art = zufall(['R', 'leer', 'eine']), s = p, r, L, fall;
          if (art === 'R'){ r = p * q; L = 'R'; fall = 'jede Zahl ist Lösung'; }
          else if (art === 'leer'){ r = p * q + zufall([-3, -2, -1, 1, 2, 4]); L = []; fall = 'keine Lösung'; }
          else { s = p + zufall([-2, -1, 1, 2, 3]); if (s === 0) s = p + 4; var x = zufallG(-5, 5); r = (p - s) * x + p * q; L = [x]; fall = 'genau eine Lösung'; }
          return { p: p, q: q, s: s, r: r, L: L, fall: fall, text: 'Welcher Lösungsfall liegt vor? \\(' + tz(p) + '(' + lin(1, q) + ') = ' + lin(s, r) + '\\)' }; },
        fehler: function(A){ return A.L === 'R' ? [[{ fall: 'keine Lösung', L: '{}' }, 'wahr']] : !A.L.length ? [[{ fall: 'jede Zahl ist Lösung', L: 'R' }, 'falsch']] : []; },
        pruefen: function(A, e){
          var r = [], m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{3}</code>, <code>{}</code> oder <code>R</code>.';
          if (e.fall === A.fall && mengeGleich(m, A.L)) return null;
          var nach = tz(A.p * A.q) === tz(A.r) ? '' : '';
          if (e.fall !== A.fall) r.push('Klammer auflösen und die \\(x\\)-Glieder sammeln: Bleibt \\(x\\) stehen? Wenn nein — ist die Aussage, die bleibt, wahr oder falsch?');
          else if (!mengeGleich(m, A.L)) r.push(A.L === 'R' ? 'Bei «jede Zahl» heisst die Lösungsmenge \\(\\mathbb{R}\\): <code>R</code>.' : !A.L.length ? 'Keine Lösung: leere Menge <code>{}</code>.' : 'Der Fall stimmt — rechne \\(x\\) nochmals nach.');
          return r.join(' ') + nach; },
        loesung: function(A){ return tz(A.p) + 'x ' + (A.p * A.q < 0 ? '- ' + (-A.p * A.q) : '+ ' + A.p * A.q) + ' = ' + lin(A.s, A.r) + ':\\ ' + mengeTex(A.L); } },

      /* ── Kapitel 2 ─────────────────────────────────────────────── */
      'ausklammern': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'ak|' + A.a + '|' + A.b; }, quad: function(A){ return [A.a, A.b, 0]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          var a = zufall([1, 2, 3, 4, 5, -1, -2, -3]), w = Math.random() < 0.12 ? 0 : zufall([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 0.5, -0.5, 1.5]), b = -a * w;
          if (!gl(b, Math.round(b))){ a *= 2; b = -a * w; }
          var gleich = Math.random() < 0.5 && b !== 0;   // auch als a x² = −b x gestellt
          return { a: a, b: b, w: w, L: w === 0 ? [0] : [0, w],
            text: 'Löse \\(' + (gleich ? poly(a, 0, 0) + ' = ' + lin(-b, 0) : poly(a, b, 0) + ' = 0') + '\\).' + (w === 0 ? '' : '') }; },
        fehler: function(A){ return A.w === 0 ? [[{ L: '{0; 1}' }, null]] : [[{ L: mText([A.w]) }, 'geteilt'], [{ L: mText([0, -A.w]) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          var m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{0; 3}</code>.';
          if (mengeGleich(m, A.L)) return null;
          if (A.w !== 0 && mengeGleich(m, [A.w])) return 'Es fehlt \\(x = 0\\). Hast du durch \\(x\\) geteilt? Das setzt \\(x \\neq 0\\) voraus — klammere stattdessen \\(x\\) aus.';
          if (A.w !== 0 && mengeGleich(m, [0, -A.w])) return 'Vorzeichen: Aus \\(x(' + lin(A.a, A.b) + ') = 0\\) folgt \\(' + lin(A.a, A.b) + ' = 0\\).';
          if (A.w === 0) return 'Hier ist \\(b = 0\\): \\(' + tz(A.a) + 'x^2 = 0\\) hat nur die Lösung \\(0\\).';
          return 'Auf null bringen, \\(x\\) ausklammern, jeden Faktor null setzen.'; },
        loesung: function(A){ return (A.w === 0 ? tz(A.a) + 'x^2 = 0' : 'x\\,(' + lin(A.a, A.b) + ') = 0') + ':\\ ' + mengeTex(A.L); } },

      'nullprodukt': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'np|' + A.p + '|' + A.m + '|' + A.n; }, quad: function(A){ return [A.m, A.n - A.p * A.m, -A.p * A.n]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          // (x − p)(m x + n) = 0 mit schöner zweiter Lösung −n/m
          var p = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 0]), m = zufall([1, 1, 2, 3, -1]), w = zufall([-4, -3, -2, -1, 1, 2, 3, 0.5, -1.5, 2.5]);
          if (m === 3) w = zufall([-2, -1, 1, 2, 1 / 3, -2 / 3]);
          var n = -m * w; if (!gl(n, Math.round(n))){ m = 2; n = -2 * w; }
          if (!gl(n, Math.round(n)) || gl(w, p)) return TYPEN['nullprodukt'].neu();
          var f1 = p === 0 ? 'x' : '(' + zx(p) + ')';
          return { p: p, m: m, n: n, w: w, L: [p, w], text: 'Löse \\(' + f1 + '(' + lin(m, n) + ') = 0\\).' }; },
        fehler: function(A){ return A.p !== 0 && !mengeGleich({ werte: [-A.p, -A.w] }, A.L) ? [[{ L: mText([-A.p, -A.w]) }, 'Vorzeichen']] : []; },
        pruefen: function(A, e){
          var m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{-2; 1.5}</code>.';
          if (mengeGleich(m, A.L)) return null;
          if (fast(m, A.L)) return FAST;
          if (mengeGleich(m, [-A.p, -A.w])) return A.p === 0
            ? 'Vorzeichen beim zweiten Faktor: \\(' + lin(A.m, A.n) + ' = 0\\) gibt \\(x = ' + texZahl(A.w) + '\\).'
            : 'Vorzeichen: Setz jeden Faktor null und löse: \\(' + zx(A.p) + ' = 0\\) gibt \\(x = ' + tz(A.p) + '\\).';
          if (m.werte.length === 1) return 'Zwei Faktoren — jeder kann null sein. Es gibt zwei Lösungen.';
          return 'Satz vom Nullprodukt: \\(' + (A.p === 0 ? 'x' : zx(A.p)) + ' = 0\\) oder \\(' + lin(A.m, A.n) + ' = 0\\).'; },
        loesung: function(A){ return mengeTex(A.L); } },

      /* ── Kapitel 3 ─────────────────────────────────────────────── */
      'wurzel': { felder: ['L'], muster: '𝕃 = {L}',
        schl: function(A){ return 'wu|' + A.p + '|' + A.q; }, quad: function(A){ return [1, -2 * A.p, A.p * A.p - A.q]; },
        eingabe: function(A){ return { L: mText(A.L) }; },
        neu: function(){
          var p = zufall([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5]), art = Math.random(), q, r;
          if (art < 0.12){ q = 0; } else if (art < 0.24){ q = -zufall([1, 4, 9]); } else { r = zufall([1, 2, 3, 4, 5, 6]); q = r * r; }
          var L = q < 0 ? [] : q === 0 ? [p] : [p - Math.sqrt(q), p + Math.sqrt(q)];
          return { p: p, q: q, L: L, text: 'Löse \\(' + (p === 0 ? 'x^2' : '(' + zx(p) + ')^2') + ' = ' + tz(q) + '\\).' }; },
        fehler: function(A){ return A.q > 0 ? [[{ L: mText([A.p + Math.sqrt(A.q)]) }, 'zwei'], A.p !== 0 ? [{ L: mText([-A.p - Math.sqrt(A.q), -A.p + Math.sqrt(A.q)]) }, 'Vorzeichen'] : null].filter(Boolean) : A.q < 0 ? [[{ L: 'R' }, null]] : []; },
        pruefen: function(A, e){
          var m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{-1; 5}</code> oder <code>{}</code>.';
          if (mengeGleich(m, A.L)) return null;
          if (A.q < 0) return 'Ein Quadrat ist nie negativ — \\(' + tz(A.q) + '\\) kann kein Quadrat sein.';
          if (A.q > 0 && m.werte.length === 1 && gl(m.werte[0], A.p + Math.sqrt(A.q))) return 'Es gibt zwei Lösungen: Die Klammer kann \\(+' + Math.sqrt(A.q) + '\\) oder \\(-' + Math.sqrt(A.q) + '\\) sein.';
          if (A.p !== 0 && mengeGleich(m, A.q === 0 ? [-A.p] : [-A.p - Math.sqrt(A.q), -A.p + Math.sqrt(A.q)])) return 'Vorzeichen: Aus \\(' + zx(A.p) + ' = \\ldots\\) folgt \\(x = ' + tz(A.p) + ' + \\ldots\\).';
          if (A.q === 0) return 'Ein Quadrat ist null, wenn die Klammer null ist: genau eine Lösung.';
          return 'Wurzel ziehen mit \\(\\pm\\), dann nach \\(x\\) auflösen.'; },
        loesung: function(A){ return A.q < 0 ? '\\mathbb{L} = \\{\\,\\}' : A.q === 0 ? zx(A.p) + ' = 0:\\ ' + mengeTex(A.L) : zx(A.p) + ' = \\pm ' + Math.sqrt(A.q) + ':\\ ' + mengeTex(A.L); } },

      'mitternacht': { felder: ['D', 'L'], muster: 'D = {D}; 𝕃 = {L}',
        schl: function(A){ return 'mi|' + A.a + '|' + A.b + '|' + A.c; }, quad: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { D: String(A.D), L: mText(A.L) }; },
        neu: function(){
          // aus Lösungen r1, r2 (ganz oder halb) mit a ∈ {1, 2}: a(x − r1)(x − r2); manchmal D ≤ 0
          var art = Math.random(), a, b, c;
          if (art < 0.15){ a = zufall([1, 2, 3]); b = zufall([-4, -2, 2, 4]); c = Math.floor(b * b / (4 * a)) + zufall([1, 2, 3]); }
          else if (art < 0.27){ var r = zufall([-3, -2, -1, 1, 2, 3]), k = zufall([1, 4]); a = k; b = -2 * k * r; c = k * r * r; }
          else { a = zufall([1, 2, 2, 3]); var r1 = zufall([-4, -3, -2, -1, 1, 2, 3, 4]), r2n = zufall([-5, -3, -1, 1, 3, 5, -4, -2, 2, 4]);
                 // a(x − r1)(x − r2n/a): b = −a·r1 − r2n, c = r1·r2n
                 b = -a * r1 - r2n; c = r1 * r2n; if (b === 0 || c === 0) return TYPEN['mitternacht'].neu(); }
          var D = b * b - 4 * a * c, L = D < 0 ? [] : D === 0 ? [-b / (2 * a)] : [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)];
          if (D > 0 && !gl(Math.sqrt(D), Math.round(Math.sqrt(D)))) return TYPEN['mitternacht'].neu();
          return { a: a, b: b, c: c, D: D, L: L, text: 'Löse \\(' + poly(a, b, c) + ' = 0\\) mit der Mitternachtsformel. (Bei \\(D \\lt 0\\): \\(\\mathbb{L} = \\{\\,\\}\\) als <code>{}</code>.)' }; },
        fehler: function(A){ var f = []; if (A.a * A.c !== 0) f.push([{ D: String(A.b * A.b + 4 * A.a * A.c), L: mText(A.L) }, 'abgezogen']);
          if (A.D > 0) f.push([{ D: String(A.D), L: mText(A.L.map(function(v){ return -v; })) }, '-b']); return f; },
        pruefen: function(A, e){
          var m = menge(e.L), r = [];
          if (m.kaputt) return 'Lösungsmenge wie <code>{-2; 0.5}</code> oder <code>{}</code>.';
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

      /* ── Kapitel 4 ─────────────────────────────────────────────── */
      'verfahren': { felder: ['v', 'L'], muster: 'Am schnellsten: {v:Wurzelziehen|Ausklammern|Faktorisieren|Mitternachtsformel}; 𝕃 = {L}',
        schl: function(A){ return 'zk|' + A.b + '|' + A.c; }, quad: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { v: A.v, L: mText(A.L) }; },
        neu: function(){
          var art = zufall(['W', 'A', 'F', 'M']), a = 1, b, c, L, v;
          if (art === 'W'){ var r = zufall([1, 2, 3, 4, 5, 6, 7]); a = zufall([1, 2, 3]); b = 0; c = -a * r * r; L = [-r, r]; v = 'Wurzelziehen'; }
          else if (art === 'A'){ var w = zufall([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]); a = zufall([1, 2, 3]); b = -a * w; c = 0; L = [0, w]; v = 'Ausklammern'; }
          else if (art === 'F'){ var r1 = zufallG(-6, 6), r2 = zufallG(-6, 6); if (r1 === r2 || r1 === 0 || r2 === 0 || r1 === -r2) return TYPEN['verfahren'].neu();
            b = -(r1 + r2); c = r1 * r2; L = [r1, r2]; v = 'Faktorisieren'; }
          else { a = zufall([2, 3, 5]); var p1 = zufall([1, 2, 3, -1, -2]), q1 = zufall([1, -1, 2, -2, 3]);   // a(x − p1)(x − q1/a), q1/a kein ganzes
            if (q1 % a === 0) return TYPEN['verfahren'].neu(); b = -a * p1 - q1; c = p1 * q1; L = [p1, q1 / a]; v = 'Mitternachtsformel'; if (b === 0 || c === 0) return TYPEN['verfahren'].neu(); }
          return { a: a, b: b, c: c, L: L, v: v, text: 'Welches Verfahren führt am schnellsten zum Ziel? Löse dann: \\(' + poly(a, b, c) + ' = 0\\).' }; },
        fehler: function(A){ return A.v === 'Mitternachtsformel' ? [] : [[{ v: 'Mitternachtsformel', L: mText(A.L) }, 'Geht immer']]; },
        pruefen: function(A, e){
          var m = menge(e.L), r = [];
          if (m.kaputt) return 'Lösungsmenge wie <code>{-3; 3}</code>.';
          // Bei a = 1 geht Faktorisieren auch bei x² − r² (Binom) und x² + bx (x ausklammern): gleich schnell.
          var auchF = e.v === 'Faktorisieren' && A.a === 1 && (A.v === 'Wurzelziehen' || A.v === 'Ausklammern');
          if ((e.v === A.v || auchF) && mengeGleich(m, A.L)) return null;
          if (e.v !== A.v && !auchF){
            if (e.v === 'Mitternachtsformel') r.push('Geht immer — aber hier gibt es einen kürzeren Weg. ' + (A.v === 'Wurzelziehen' ? 'Das Glied mit \\(x\\) fehlt.' : A.v === 'Ausklammern' ? 'Die Zahl ohne \\(x\\) fehlt.' : 'Zwei ganze Zahlen mit Summe \\(' + tz(-A.b) + '\\) und Produkt \\(' + tz(A.c) + '\\) gibt es.'));
            else if (A.v === 'Mitternachtsformel') r.push('Vor \\(x^2\\) steht \\(' + A.a + '\\), und alle drei Glieder sind da — der Zweiklammersatz geht hier nicht glatt.');
            else r.push(e.v === 'Wurzelziehen' ? 'Wurzelziehen braucht eine Gleichung ohne lineares Glied (\\(b = 0\\)).' : e.v === 'Ausklammern' ? 'Ausklammern braucht eine Gleichung ohne Zahl ohne \\(x\\).' : 'Vor \\(x^2\\) steht \\(' + A.a + '\\) — der Zweiklammersatz braucht \\(1\\) vor \\(x^2\\).');
          }
          if (!mengeGleich(m, A.L)) r.push(fast(m, A.L) ? FAST : m.werte.length < A.L.length ? 'Es fehlt eine Lösung.' : 'Die Lösungsmenge stimmt noch nicht — mach die Probe.');
          return r.join(' '); },
        loesung: function(A){ return '\\text{' + A.v + '}:\\ ' + mengeTex(A.L); } },

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
          var m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{2; 3}</code>.';
          if (mengeGleich(m, [A.r1, A.r2])) return null;
          if (mengeGleich(m, [-A.r1, -A.r2])) return 'Vorzeichen: Aus \\((x ' + (A.r1 < 0 ? '+ ' + (-A.r1) : '- ' + A.r1) + ')\\) wird \\(x = ' + tz(A.r1) + '\\). Bei Faktoren \\((x - x_1)\\) ist \\(x_1\\) die Lösung.';
          return 'Gesucht sind die Lösungen: Summe \\(-p = ' + tz(-A.p) + '\\), Produkt \\(q = ' + tz(A.q) + '\\). Kontrolle durch Ausmultiplizieren.'; },
        loesung: function(A){ return '(' + zx(A.r1) + ')(' + zx(A.r2) + ') = 0:\\ ' + mengeTex([A.r1, A.r2]); } },

      /* ── Kapitel 5 ─────────────────────────────────────────────── */
      'param-linear': { felder: ['k', 'fall'], muster: 'kritisch: k = {k}; dort: {fall:keine Lösung|jede Zahl ist Lösung|genau eine Lösung}',
        schl: function(A){ return 'pl|' + A.a + '|' + A.art; },
        eingabe: function(A){ return { k: String(A.a), fall: A.art === 'A' ? 'jede Zahl ist Lösung' : 'keine Lösung' }; },
        neu: function(){
          // A: (k − a)x = m(k − a) → bei k = a alle;  B: (k − a)x = c (c ≠ 0) → bei k = a keine
          var a = zufall([-4, -3, -2, -1, 1, 2, 3, 4, 5]), art = zufall(['A', 'B']), m = zufall([2, 3, -2, 4]), c = zufall([1, 2, 3, -1, -5]);
          var rechts = art === 'A' ? (m === 1 ? '' : tz(m)) + '(k ' + (a < 0 ? '+ ' + (-a) : '- ' + a) + ')' : tz(c);
          return { a: a, art: art, m: m, c: c, text: 'Für welches \\(k\\) gibt es nicht genau eine Lösung, und was gilt dort? \\((k ' + (a < 0 ? '+ ' + (-a) : '- ' + a) + ') \\cdot x = ' + rechts + '\\)' }; },
        fehler: function(A){ return [[{ k: String(-A.a), fall: A.art === 'A' ? 'jede Zahl ist Lösung' : 'keine Lösung' }, 'Vorzeichen'],
                                     [{ k: String(A.a), fall: A.art === 'A' ? 'keine Lösung' : 'jede Zahl ist Lösung' }, null]]; },
        pruefen: function(A, e){
          var r = [], soll = A.art === 'A' ? 'jede Zahl ist Lösung' : 'keine Lösung';
          if (gl(e.k, A.a) && e.fall === soll) return null;
          if (!gl(e.k, A.a)) r.push(gl(e.k, -A.a) ? 'Vorzeichen: \\(k ' + (A.a < 0 ? '+ ' + (-A.a) : '- ' + A.a) + ' = 0\\) gibt \\(k = ' + tz(A.a) + '\\).' : 'Kritisch ist das \\(k\\), bei dem der Faktor vor \\(x\\) null wird.');
          if (e.fall !== soll) r.push(e.fall === 'genau eine Lösung' ? 'Beim kritischen \\(k\\) verschwindet \\(x\\) — dann gibt es nie genau eine Lösung.' : 'Setz das kritische \\(k\\) rechts ein: ' + (A.art === 'A' ? 'Rechts wird es auch \\(0\\) — \\(0 = 0\\) ist wahr.' : 'Rechts bleibt \\(' + tz(A.c) + ' \\neq 0\\) — \\(0 = ' + tz(A.c) + '\\) ist falsch.'));
          return r.join(' '); },
        loesung: function(A){ return 'k = ' + tz(A.a) + ':\\ 0 = ' + (A.art === 'A' ? '0,\\ \\mathbb{L} = \\mathbb{R}' : tz(A.c) + ',\\ \\mathbb{L} = \\{\\,\\}'); } },

      'param-quadr': { felder: ['k', 'x'], muster: 'genau eine Lösung für k = {k}; sie heisst x = {x}',
        schl: function(A){ return 'pq|' + A.b; },
        eingabe: function(A){ return { k: String(A.b * A.b / 4), x: String(-A.b / 2) }; },
        neu: function(){
          var b = zufall([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10, 12, -12]);
          return { b: b, text: 'Für welches \\(k\\) hat \\(' + poly(1, b, 0) + ' + k = 0\\) genau eine Lösung? Wie heisst sie?' }; },
        fehler: function(A){ return [[{ k: String(A.b * A.b / 4), x: String(A.b / 2) }, 'Vorzeichen'], [{ k: String(A.b * A.b / 2), x: String(-A.b / 2) }, '4']]; },
        pruefen: function(A, e){
          var r = [], k0 = A.b * A.b / 4;
          if (gl(e.k, k0) && gl(e.x, -A.b / 2)) return null;
          if (!gl(e.k, k0)) r.push('Genau eine Lösung bei \\(D = 0\\): \\(D = ' + (A.b < 0 ? '(' + A.b + ')' : A.b) + '^2 - 4k = ' + A.b * A.b + ' - 4k\\).');
          if (!gl(e.x, -A.b / 2)) r.push(gl(e.x, A.b / 2) ? 'Vorzeichen: \\(x = -\\tfrac{b}{2a}\\).' : 'Bei \\(D = 0\\) ist \\(x = -\\tfrac{b}{2a}\\).');
          return r.join(' '); },
        loesung: function(A){ return 'D = ' + A.b * A.b + ' - 4k = 0 \\Rightarrow k = ' + A.b * A.b / 4 + ';\\ x = ' + tz(-A.b / 2); } }
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
