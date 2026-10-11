<script>
/* Leitprogramm Lineare Gleichungssysteme — Simulationen mit Aufgabenleiste (Punkt-Sucher, System-Umformer,
   Lösungsfall-Labor), Übungen mit Rückmeldung, Minigrafen. Gebaut von scripts/lp/gleichungssysteme/seite.py.
   Notation wie auf der Themenseite 2.3: Lösung als Paar (x | y) bzw. Tripel, 𝕃 = {(2 | 3)}, leere Menge { },
   unendlich viele Lösungen 𝕃 = {(x | 2x − 4) : x ∈ ℝ}, Gleichungen (I), (II), (III).
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Gleichung (I) · orange = Gleichung (II) ·
   grün = Lösung, Schnittpunkt · rot = Fehler · Tinte = neutral (Umformungsschritte, Parameter k, Punkt P). */
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
  function gl(a, b){ return Math.abs(a - b) < 1e-9; }
  function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
  /* Zahl in LaTeX: ganze und endliche Dezimalzahlen direkt, sonst als Bruch. */
  function texZahl(v){
    if (gl(v, Math.round(v))) return tz(Math.round(v));
    for (var d of [2, 4, 5, 8, 10]) if (gl(v * d, Math.round(v * d))) return tz(Math.round(v * 1000) / 1000);
    for (var q = 3; q <= 40; q++){ var n = Math.round(v * q); if (gl(v * q, n)) return (n < 0 ? '-' : '') + '\\tfrac{' + Math.abs(n) + '}{' + q + '}'; }
    return tz(Math.round(v * 1000) / 1000);
  }
  /* So tippt man eine Zahl ein: ganz, Dezimalzahl oder Bruch a/b. */
  function zText(v){
    if (gl(v, Math.round(v))) return String(Math.round(v));
    for (var d of [2, 4, 5, 8, 10]) if (gl(v * d, Math.round(v * d))) return String(Math.round(v * 1000) / 1000);
    for (var q = 3; q <= 40; q++){ var n = Math.round(v * q); if (gl(v * q, n)) return n + '/' + q; }
    return String(Math.round(v * 1000) / 1000);
  }
  function paarTex(p){ return '(' + p.map(texZahl).join(' \\mid ') + ')'; }

  /* ---------- Zahlen und Lösungsmengen lesen ----------
     Zahl: -3, 0.5, 1/2, -2/3; das Dezimalkomma wird verstanden (und angemerkt).
     Lösungsmenge eines Systems: «{(2 | 3)}», «(2|3)», «(2; 3)», «{(1 | 2 | 3)}»; leer: «{}», «{ }», «leer». */
  function zahl(s){
    var komma = /\d,\d/.test(s);
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^\+/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(-?\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  function tupelMenge(s){
    var t = String(s).trim().replace(/\u2212/g, '-').replace(/∣/g, '|');
    if (!t) return { nichts: true };
    t = t.replace(/^𝕃\s*=\s*/, '').replace(/^L\s*=\s*/i, '').trim();
    var komma = /\d,\d/.test(t);
    if (/^\{\s*\}$/.test(t) || /^(leer|keine|keine lösung|∅)$/i.test(t)) return { tupel: [], komma: komma };
    if (/^(r|ℝ|\{\s*(r|ℝ)\s*\})$/i.test(t)) return { kaputt: true, alleZahlen: true };
    if (/[xyz]\s*=/.test(t)) return { kaputt: true, gleich: true };
    t = t.replace(/^\{/, '').replace(/\}$/, '').trim();
    var teile = t.match(/\([^()]*\)/g);
    if (!teile){ if (/[|;]/.test(t)) teile = ['(' + t + ')']; else return { kaputt: true }; }
    var rest = t.replace(/\([^()]*\)/g, '').replace(/[;,\s]/g, '');
    if (rest) return { kaputt: true };
    var tupel = [];
    for (var i = 0; i < teile.length; i++){
      var inn = teile[i].slice(1, -1).replace(/(\d),(\d)/g, '$1.$2');
      var w = inn.split(/\||;|,\s+/), p = [];
      for (var j = 0; j < w.length; j++){ var r = zahl(w[j]); if (isNaN(r.wert)) return { kaputt: true }; p.push(r.wert); }
      tupel.push(p);
    }
    return { tupel: tupel, komma: komma };
  }

  /* ---------- Koordinatensystem ---------- */
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
      namen.push([W - 3, Y(0) - pf, 'end', 'x']);
    }
    if (x0 <= 0 && x1 >= 0){
      el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
      namen.push([X(0) + pf, pf + 3, 'start', 'y']);
    }
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(Math.max(0, y0)) + 13, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(Math.max(0, x0)) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    var ebene = el(svg, 'g', {}), schilder = el(svg, 'g', {});
    namen.forEach(function(n){ el(schilder, 'text', { x: n[0], y: n[1], 'text-anchor': n[2], 'class': 'achsname' }, n[3]); });
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      /* Gerade a·x + b·y = c, auch senkrecht (b = 0); am Fenster abgeschnitten. */
      gerade: function(a, b, c, cls){
        var p, q;
        if (Math.abs(b) < 1e-12){ if (Math.abs(a) < 1e-12) return; var xs = c / a; p = [xs, y0 - 1]; q = [xs, y1 + 1]; }
        else { p = [x0 - 1, (c - a * (x0 - 1)) / b]; q = [x1 + 1, (c - a * (x1 + 1)) / b]; }
        return el(ebene, 'line', { x1: X(p[0]), y1: Y(p[1]), x2: X(q[0]), y2: Y(q[1]), 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 - 1e-9 || x > x1 + 1e-9 || y < y0 - 1e-9 || y > y1 + 1e-9) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      text: function(x, y, s, cls, anker){ el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'start', 'class': 'p-text ' + (cls || '') }, s); }
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

  /* ════════ Kapitel 1 · Punkt-Sucher ════════
     Unterschied zur Themenseite (Kino- und Drei-Darstellungen-Animation, dort sind beide Geraden von Anfang
     an gezeichnet): Hier entsteht jede Gerade erst aus Punkten, die die Lernenden selbst als Lösung einer
     Gleichung finden — die Gerade ist die Menge aller Lösungen. Zwei Regler, die Anzeige rechnet die Probe.
     Die Systeme sind nicht das Beispiel des Clips (2x + y = 7, x − y = −1); Startpunkt P(0 | 0) erfüllt in
     keinem der drei Systeme eine Gleichung (pruef-leiste). */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -2, x1: 6, y0: -2, y1: 6, xm: [-1, 1, 2, 3, 4, 5], ym: [-1, 1, 2, 3, 4, 5] });
    // Systeme als [a, b, c] für a·x + b·y = c, dazu die Schreibweise
    var SYS = [
      { I: [1, 1, 5], II: [2, -1, 4], tI: 'x + y = 5', tII: '2x − y = 4', L: [3, 2] },
      { I: [1, 2, 4], II: [1, -1, 1], tI: 'x + 2y = 4', tII: 'x − y = 1', L: [2, 1] },
      { I: [1, 1, 3], II: [1, -1, -2], tI: 'x + y = 3', tII: 'x − y = −2', L: [0.5, 2.5] }
    ];
    var rx = fig.querySelector('input[data-p="x"]'), ry = fig.querySelector('input[data-p="y"]');
    var zust = { s: 0, funde: { I: {}, II: {} }, zeigen: false, bewegt: {} }, pruefen = function(){};
    function setze(){ zust.funde.I = {}; zust.funde.II = {}; }
    [rx, ry].forEach(function(r){ r.addEventListener('input', function(){ zust.bewegt[r.dataset.p] = true; zeichnen(); }); });
    function erfuellt(g, x, y){ return gl(g[0] * x + g[1] * y, g[2]); }
    function seite(g, x, y){
      var t = [];
      if (g[0]) t.push((g[0] === 1 ? '' : g[0] === -1 ? '−' : z(g[0]) + ' · ') + (x < 0 ? '(' + z(x) + ')' : z(x)));
      if (g[1]) t.push((t.length ? (g[1] < 0 ? ' − ' : ' + ') : (g[1] < 0 ? '−' : '')) + (Math.abs(g[1]) === 1 ? '' : z(Math.abs(g[1])) + ' · ') + (y < 0 ? '(' + z(y) + ')' : z(y)));
      return t.join('');
    }
    function zustand(){
      var S = SYS[zust.s], x = +rx.value, y = +ry.value;
      return { s: zust.s, x: x, y: y, inI: erfuellt(S.I, x, y), inII: erfuellt(S.II, x, y),
               nI: Object.keys(zust.funde.I).length, nII: Object.keys(zust.funde.II).length, bewegt: zust.bewegt, zeigen: zust.zeigen };
    }
    function zeichnen(){
      var S = SYS[zust.s], s = zustand(), x = s.x, y = s.y;
      rx.parentNode.querySelector('.sl-val').textContent = z(x);
      ry.parentNode.querySelector('.sl-val').textContent = z(y);
      if (s.inI) zust.funde.I[x + '|' + y] = [x, y];
      if (s.inII) zust.funde.II[x + '|' + y] = [x, y];
      s = zustand();
      K.leeren();
      if (zust.zeigen || s.nI >= 2) K.gerade(S.I[0], S.I[1], S.I[2], 'gerade g1');
      if (zust.zeigen || s.nII >= 2) K.gerade(S.II[0], S.II[1], S.II[2], 'gerade g2');
      Object.keys(zust.funde.I).forEach(function(k){ var p = zust.funde.I[k]; K.punkt(p[0], p[1], 'p-g'); });
      Object.keys(zust.funde.II).forEach(function(k){ var p = zust.funde.II[k]; K.punkt(p[0], p[1], 'p-n'); });
      var beide = s.inI && s.inII;
      K.punkt(x, y, beide ? 'p-loes p-gross' : 'p-p', 'P', 9, -9);
      var hI = s.inI ? ' = ' + z(S.I[2]) + ' ✓' : ' = ' + z(S.I[0] * x + S.I[1] * y) + ' ≠ ' + z(S.I[2]);
      var hII = s.inII ? ' = ' + z(S.II[2]) + ' ✓' : ' = ' + z(S.II[0] * x + S.II[1] * y) + ' ≠ ' + z(S.II[2]);
      fig.querySelector('[data-rolle="formel"]').innerHTML =
        '<span class="nb">P(' + z(x) + ' | ' + z(y) + ')</span><br>' +
        sp('tx-blau', '(I) ' + S.tI.replace(/-/g, '−')) + ': <span class="nb">' + seite(S.I, x, y) + hI + '</span><br>' +
        sp('tx-orange', '(II) ' + S.tII.replace(/-/g, '−')) + ': <span class="nb">' + seite(S.II, x, y) + hII + '</span>' +
        (beide ? '<br>' + sp('tx-gruen', 'beide erfüllt: P ist der Schnittpunkt, die Lösung (' + z(x) + ' | ' + z(y) + ')') : '');
      pruefen();
    }
    var sim = { zustand: zustand, zeichnen: zeichnen, aufraeumen: function(){ for (var b in zust.bewegt) delete zust.bewegt[b]; } };
    function system(i, zeigen){ return function(){ zust.s = i; zust.zeigen = zeigen; setze(); zeichnen(); }; }
    pruefen = Leiste(fig, [
      { text: 'Zieh an \\(x\\) und \\(y\\). Erfüllt P die Gleichung (I), bleibt dort ein blauer Punkt stehen. Finde zwei solche Punkte — durch sie geht die Gerade (I).',
        setup: system(0, false), ok: function(s){ return s.s === 0 && s.nI >= 2; } },
      { text: 'Finde zwei Punkte von (II) — dann erscheint auch ihre Gerade.', setup: function(){ zust.s = 0; zust.zeigen = false; zust.funde.II = {}; zeichnen(); },
        ok: function(s){ return s.s === 0 && s.nII >= 2; } },
      { text: 'Setze P auf den Punkt, der beide Gleichungen erfüllt: die Lösung des Systems.', setup: function(){ zust.s = 0; zust.zeigen = true; zeichnen(); },
        ok: function(s){ return s.s === 0 && s.inI && s.inII; } },
      { text: 'Neues System, beide Geraden sind gezeichnet. Setze P auf die Lösung.', setup: system(1, true),
        ok: function(s){ return s.s === 1 && s.inI && s.inII; } },
      { text: 'Hier liegt der Schnittpunkt zwischen den Gitterlinien. Setze P darauf — die Anzeige macht die Probe.', setup: system(2, true),
        ok: function(s){ return s.s === 2 && s.inI && s.inII; } }
    ], sim);
    zeichnen();
  })();

  /* ════════ Kapitel 2, 3, 5 · System-Umformer ════════
     Unterschied zur Themenseite («Drei analytische Verfahren» und «3×3 schrittweise»: dort klickt man einen
     festen Weg durch): Hier wählen die Lernenden jeden Schritt selbst (welche Gleichung wohin, womit
     multiplizieren, welche Variable eliminieren), füllen Lücken und geben am Schluss die Lösungsmenge ein.
     Gültige andere Wege führen ebenfalls ans Ziel, erlaubte Umwege bekommen einen grauen Hinweis, Fehler
     eine eigene Rückmeldung (HOWTO-leitprogramme §8d, Umformer der Gleichungen erweitert auf Systeme).
     Die Knoten stehen in scripts/lp/gleichungssysteme/umformer.py und sind dort gegen das System gerechnet. */
  var UMFORMER_DATEN = /*@UMFORMER@*/null;
  function LgsUmformer(fig){
    var verl = fig.querySelector('.uf-verlauf'), frage = fig.querySelector('.uf-frage'), wahl = fig.querySelector('.uf-wahl'),
        rueck = fig.querySelector('.uf-rueck'), zur = fig.querySelector('.uf-zurueck');
    var A = null, pfad = [], ops = [], fertig = false, pruefen = function(){};
    function knoten(id){ return A.k[id]; }
    function zeile(id, op){
      var K = knoten(id);
      return '<div class="uf-zeile"><span class="uf-gl">\\(' + K.z + '\\)</span><span class="uf-op">' + (op ? '\\(' + op + '\\)' : '') + '</span></div>';
    }
    function meldung(cls, html){ rueck.className = 'uf-rueck ' + cls; rueck.innerHTML = html; setzen(rueck); }
    function loesungTex(L){ return L.length ? '\\mathbb{L} = \\{' + paarTex(L) + '\\}' : '\\mathbb{L} = \\{\\,\\}'; }
    function zeichnen(){
      if (!A){ verl.innerHTML = ''; frage.innerHTML = ''; wahl.innerHTML = ''; return; }
      var html = '';
      pfad.forEach(function(id, j){ if (knoten(id).z != null) html += zeile(id, ops[j]); });
      verl.innerHTML = html;
      var K = knoten(pfad[pfad.length - 1]);
      zur.disabled = pfad.length < 2 || fertig;
      if (fertig){
        frage.innerHTML = '';
        wahl.innerHTML = '<div class="uf-loesung">\\(' + loesungTex(K.L) + '\\)</div>' + (K.probe ? '<p class="uf-probe">Probe: \\(' + K.probe + '\\)</p>' : '');
      } else if (K.w){
        frage.innerHTML = K.frage || 'Wähle den nächsten Schritt:';
        wahl.innerHTML = K.w.map(function(o, j){ return '<button type="button" class="uf-knopf" data-j="' + j + '">' + o[0] + '</button>'; }).join('');
        wahl.querySelectorAll('.uf-knopf').forEach(function(b){ b.addEventListener('click', function(){ waehle(+b.dataset.j); }); });
      } else if (K.feld){
        frage.innerHTML = K.frage || 'Rechne den Wert aus:';
        wahl.innerHTML = '<span class="uf-feld">' + K.feld.muster.replace(/\{(\w+)\}/g, function(m, f){
          return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">'; })
          + '</span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', feldPruefen);
        wahl.querySelectorAll('input').forEach(function(i){ i.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') feldPruefen(); }); });
      } else if (K.L != null){
        var n = K.L.length || (A.n || 2);
        frage.innerHTML = K.frage || ('Gib die Lösungsmenge an, ' + (n === 3 ? 'ein Tripel wie <code>{(1 | 2 | 3)}</code>' : 'ein Paar wie <code>{(2 | 3)}</code>') + '; keine Lösung: <code>{}</code>.');
        wahl.innerHTML = '<span class="uf-feld">\\(\\mathbb{L} = \\)<input type="text" class="uf-menge" inputmode="text" autocomplete="off" aria-label="Lösungsmenge" placeholder="' + (n === 3 ? '{(x | y | z)}' : '{(x | y)}') + '"></span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', loesungPruefen);
        wahl.querySelector('input').addEventListener('keydown', function(ev){ if (ev.key === 'Enter') loesungPruefen(); });
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
      // '?': eine gültige Umformung, die hier ein Umweg ist — Hinweis (grau), kein Fehler (HOWTO §15)
      if (typeof o[1] === 'string' && o[1].charAt(0) === '?') return meldung('hinweis', o[1].slice(1));
      weiter(o[1], o[2], o[3]);
    }
    function feldPruefen(){
      var F = knoten(pfad[pfad.length - 1]).feld, e = {}, leer = false, kaputt = false;
      wahl.querySelectorAll('input').forEach(function(i){ var r = zahl(i.value); e[i.dataset.f] = r.wert; if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; });
      if (leer) return meldung('hinweis', 'Fülle die Lücke aus.');
      if (kaputt) return meldung('hinweis', 'Zahlen wie <code>-3</code>, <code>0.5</code> oder <code>1/2</code>.');
      var richtig = true; for (var k in F.soll) if (!gl(e[k], F.soll[k])) richtig = false;
      if (richtig) return weiter(F.nach, '', '');
      for (var q = 0; F.fehler && q < F.fehler.length; q++){
        var pass = true; for (var kk in F.fehler[q][0]) if (!gl(e[kk], F.fehler[q][0][kk])) pass = false;
        if (pass) return meldung('falsch', F.fehler[q][1]);
      }
      meldung('falsch', 'Noch nicht. Rechne nach: ' + (F.tipp || ''));
    }
    function loesungPruefen(){
      var K = knoten(pfad[pfad.length - 1]), i = wahl.querySelector('input'), e = tupelMenge(i.value), soll = K.L, n = soll.length || 2;
      if (e.nichts) return meldung('hinweis', 'Gib die Lösungsmenge ein, zum Beispiel <code>{(2 | 3)}</code> oder <code>{}</code>.');
      if (e.kaputt) return meldung('hinweis', e.gleich ? 'Gefragt ist die Lösungsmenge: <code>{(3 | 5)}</code> statt <code>x = 3, y = 5</code>.'
        : e.alleZahlen ? 'Die Lösungen eines Systems sind Zahlen<b>paare</b>, nicht einzelne Zahlen — \\(\\mathbb{R}\\) passt nicht.'
        : 'Schreib die Lösung als Paar in runden Klammern, die Koordinaten getrennt durch <code>|</code>: <code>{(2 | 3)}</code>. Brüche als <code>1/2</code>.');
      var T = e.tupel;
      function gleichT(p, q){ return p.length === q.length && p.every(function(v, j){ return gl(v, q[j]); }); }
      if ((soll.length === 0 && T.length === 0) || (T.length === 1 && gleichT(T[0], soll))){
        fertig = true; meldung('richtig', '✓ Richtig' + (e.komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + '.'); zeichnen(); pruefen(); return;
      }
      var t;
      if (!soll.length) t = 'Die letzte Zeile ist ein Widerspruch — kein ' + (A.n === 3 ? 'Tripel' : 'Paar') + ' erfüllt alle Gleichungen. Die Lösungsmenge ist leer: <code>{}</code>.';
      else if (!T.length) t = 'Du hast doch Werte gefunden — sie bilden die Lösung. Schreib sie als ' + (n === 3 ? 'Tripel' : 'Paar') + ' in die Menge.';
      else if (T.length > 1) t = 'Das System hat genau eine Lösung — ein einziges ' + (n === 3 ? 'Tripel' : 'Paar') + '.';
      else if (T[0].length !== n) t = n === 3 ? 'Ein Tripel hat drei Koordinaten: \\((x \\mid y \\mid z)\\).' : 'Ein Paar hat zwei Koordinaten: \\((x \\mid y)\\).';
      else if (soll.slice().sort().join() === T[0].slice().sort().join() && !gleichT(T[0], soll)) t = 'Die Zahlen stimmen, die Reihenfolge nicht: zuerst \\(x\\), dann \\(y\\)' + (n === 3 ? ', dann \\(z\\)' : '') + '.';
      else {
        var falsch = soll.map(function(v, j){ return gl(v, T[0][j]) ? null : 'xyz'.charAt(j); }).filter(Boolean);
        t = 'Noch nicht: \\(' + falsch.join('\\), \\(') + '\\) stimmt nicht. Lies die Werte in den letzten Zeilen ab.';
      }
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
  function umformerSim(id){
    var fig = document.getElementById(id); if (!fig || !UMFORMER_DATEN || !UMFORMER_DATEN[id]) return;
    var aufgaben = UMFORMER_DATEN[id];
    aufgaben.forEach(function(a){ a.n = id === 'sim5' ? 3 : 2; });
    var U = LgsUmformer(fig);
    fig.__aufgaben = aufgaben; fig.__U = U;      // Testhaken (pruef-lgs-umformer.mjs)
    var sim = { zustand: U.zustand, aufraeumen: function(){}, ende: U.leeren };
    var pr = Leiste(fig, aufgaben.map(function(a){
      return { text: a.text, setup: function(){ U.laden(a); }, ok: function(s){ return s.fertig && s.aufgabe === a; } }; }), sim);
    U.setPruefen(pr);
  }
  ['sim2', 'sim3', 'sim5'].forEach(umformerSim);

  /* ════════ Kapitel 4 · Lösungsfall-Labor ════════
     Unterschied zur Themenseite (Geradenbüschel mit Modi m/c und k): ein einziger Regler k, drei feste
     Familien — k in der Konstanten, k in einem Koeffizienten von (I), k in beiden Gleichungen —, die
     Anzeige rechnet die Elimination mit, die Aufgabenleiste stellt Zielspiele. Startwert k = 1: in keiner
     Familie ist eine Aufgabe schon gelöst, auch nicht nach einem Wechsel der Familie. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -5, x1: 5, y0: -5, y1: 5, xm: [-4, -2, 2, 4], ym: [-4, -2, 2, 4] });
    var kr = fig.querySelector('input[data-p="k"]'), fam = fig.querySelector('.sim-wahl'), bewegt = {}, pruefen = function(){};
    kr.addEventListener('input', function(){ bewegt.k = true; zeichnen(); });
    fam.addEventListener('change', zeichnen);
    function glText(a, b, c, kIn){
      // a·x + b·y = c als Text; kIn: 'a' oder 'b' heisst: an dieser Stelle steht k (mit Wert)
      function glied(w, v, erst, istK){
        if (istK) return (erst ? '' : ' + ') + 'k' + v;
        if (w === 0) return '';
        var s = Math.abs(w) === 1 ? '' : z(Math.abs(w));
        return (w < 0 ? (erst ? '−' : ' − ') : (erst ? '' : ' + ')) + s + v;
      }
      var t = glied(a, 'x', true, kIn === 'a'); t += glied(b, 'y', !t, kIn === 'b');
      return t + ' = ' + (kIn === 'c' ? 'k' : z(c));
    }
    function zust(){
      var k = +kr.value, f = fam.value, I, II, L, fall, rech;
      kr.parentNode.querySelector('.sl-val').textContent = z(k);
      if (f === 'A'){ I = [2, -1, 3]; II = [-4, 2, k]; rech = ['2 · (I) + (II):', '0 = 6 + k', '→ 0 = ' + z(6 + k) + (6 + k ? ' (falsch)' : ' (wahr)')];
        if (k === -6){ fall = 'unendlich'; } else fall = 'keine'; }
      else if (f === 'B'){ I = [k, 2, 4]; II = [2, 1, 3]; rech = ['(I) − 2 · (II):', '(k − 4) · x = −2', '→ ' + (k === 4 ? '0 = −2 (falsch)' : z(k - 4) + ' · x = −2')];
        if (k === 4) fall = 'keine'; else { fall = 'eine'; var xb = -2 / (k - 4); L = [xb, 3 - 2 * xb]; } }
      else { I = [1, k, 3]; II = [k, 9, 9]; rech = ['k · (I) − (II):', '(k² − 9) · y = 3k − 9', '→ ' + (k * k === 9 ? '0 = ' + z(3 * k - 9) + (3 * k - 9 ? ' (falsch)' : ' (wahr)') : z(k * k - 9) + ' · y = ' + z(3 * k - 9))];
        if (k === 3) fall = 'unendlich'; else if (k === -3) fall = 'keine'; else { fall = 'eine'; L = [9 / (k + 3), 3 / (k + 3)]; } }
      return { k: k, fam: f, I: I, II: II, L: L, fall: fall, rech: rech, bewegt: bewegt };
    }
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (s.fall === 'unendlich'){
        K.gerade(s.I[0], s.I[1], s.I[2], 'gerade g1 breit');
        K.gerade(s.II[0], s.II[1], s.II[2], 'gerade g2 gestrichelt');
      } else {
        K.gerade(s.I[0], s.I[1], s.I[2], 'gerade g1');
        K.gerade(s.II[0], s.II[1], s.II[2], 'gerade g2');
      }
      if (s.L) K.punkt(s.L[0], s.L[1], 'p-loes', '(' + zz(s.L[0]) + ' | ' + zz(s.L[1]) + ')', 8, -8);
      var sys = s.fam === 'A' ? [glText(2, -1, 3), glText(-4, 2, 0, 'c')] : s.fam === 'B' ? [glText(0, 2, 4, 'a'), glText(2, 1, 3)] : [glText(1, 0, 3, 'b'), glText(0, 9, 9, 'a')];
      var mitK = s.fam === 'A' ? [glText(2, -1, 3), glText(-4, 2, s.k)] : s.fam === 'B' ? [glText(s.k, 2, 4), glText(2, 1, 3)] : [glText(1, s.k, 3), glText(s.k, 9, 9)];
      var fallT = s.fall === 'eine' ? 'genau eine Lösung: Schnittpunkt, 𝕃 = {(' + zz(s.L[0]) + ' | ' + zz(s.L[1]) + ')}'
        : s.fall === 'keine' ? 'keine Lösung: parallele Geraden, 𝕃 = { }' : 'unendlich viele Lösungen: identische Geraden';
      fig.querySelector('[data-rolle="formel"]').innerHTML =
        sp('tx-blau nb', '(I) ' + sys[0]) + ' &nbsp; ' + sp('tx-orange nb', '(II) ' + sys[1]) + '<br>' +
        'mit k = ' + z(s.k) + ': <span class="nb">' + sp('tx-blau', mitK[0]) + ';</span> <span class="nb">' + sp('tx-orange', mitK[1]) + '</span><br>' +
        s.rech.map(function(t){ return sp('nb', t); }).join(' ') + '<br>' + sp('tx-gruen', fallT);
      pruefen();
    }
    function zz(v){ var r = Math.round(v * 100) / 100; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(r); }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var b in bewegt) delete bewegt[b]; fam.value = 'A'; } };
    pruefen = Leiste(fig, [
      { text: 'Familie A: Zieh an \\(k\\). Was macht die Gerade (II)?', ok: function(s){ return s.fam === 'A' && s.bewegt.k; } },
      { text: 'Familie A: Stell \\(k\\) so ein, dass die Geraden identisch sind.', ok: function(s){ return s.fam === 'A' && s.k === -6; } },
      { text: 'Wähle Familie B. Für welches \\(k\\) hat das System keine Lösung?', ok: function(s){ return s.fam === 'B' && s.k === 4; } },
      { text: 'Familie B (ist eingestellt): Stell \\(k\\) so ein, dass \\((1 \\mid 1)\\) die Lösung ist.', setup: function(){ fam.value = 'B'; }, ok: function(s){ return s.fam === 'B' && s.k === 2; } },
      { text: 'Wähle Familie C. Für welches \\(k\\) sind die Geraden identisch?', ok: function(s){ return s.fam === 'C' && s.k === 3; } },
      { text: 'Familie C (ist eingestellt): Für welches \\(k\\) gibt es keine Lösung?', setup: function(){ fam.value = 'C'; }, ok: function(s){ return s.fam === 'C' && s.k === -3; } }
    ], sim);
    zeichnen();
  })();

  /* ════════ Übungen mit Rückmeldung ════════ */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function ohne0(a, b){ var v; do { v = zufallG(a, b); } while (v === 0); return v; }
    function glied(c, v, erst){
      if (c === 0) return '';
      var s = Math.abs(c) === 1 && v ? '' : texZahl(Math.abs(c));
      return (c < 0 ? (erst ? '-' : ' - ') : (erst ? '' : ' + ')) + s + v;
    }
    /* a·x + b·y (+ c·z) = d in LaTeX */
    function lhs(k, vars){ var t = ''; for (var i = 0; i < k.length; i++) t += glied(k[i], vars[i], !t); return t || '0'; }
    function glT(g){ return g.length === 4 ? lhs(g.slice(0, 3), ['x', 'y', 'z']) + ' = ' + texZahl(g[3]) : lhs(g.slice(0, 2), ['x', 'y']) + ' = ' + texZahl(g[2]); }
    function sysT(gs){ return '\\begin{cases} ' + gs.map(function(g, i){ return g + ' & \\text{(' + ['I', 'II', 'III'][i] + ')}'; }).join(' \\\\ ') + ' \\end{cases}'; }
    function linT(m, q, v, w){ var t = glied(m, v || 'x', true); t += glied(q, '', !t); return (w || 'y') + ' = ' + (t || '0'); }
    function klam(v){ return v < 0 ? '(' + texZahl(v) + ')' : texZahl(v); }

    /* Normalform-Schlüssel eines Systems, gleich wie lgs.schl() in Python: jede Gleichung ganzzahlig,
       gekürzt, erste Zahl positiv; die Gleichungen sortiert. Gleichungen als [a, b, c] bzw. [a, b, c, d]. */
    function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
    function normGl(g){
      var nen = 1; g.forEach(function(c){ for (var d = 1; d <= 1000; d++) if (gl(c * d, Math.round(c * d))){ nen = nen * d / ggT(nen, d); break; } });
      var w = g.map(function(c){ return Math.round(c * nen); }), t = 0; w.forEach(function(c){ t = ggT(t, c); }); t = t || 1;
      w = w.map(function(c){ return c / t; });
      var erst = w.filter(function(c){ return c !== 0; })[0] || 1; if (erst < 0) w = w.map(function(c){ return -c; });
      return w.map(function(c){ return c === 0 ? 0 : c; });
    }
    function sysSchl(gs){
      var n = gs.map(normGl);
      n.sort(function(p, q){ for (var i = 0; i < p.length; i++) if (p[i] !== q[i]) return p[i] - q[i]; return 0; });
      return n.map(function(g){ return g.join('|'); }).join(';');
    }
    /* Feste Systeme und Gleichungen des Leitprogramms (Clips, Simulationen, Umformer, Kapitelaufgaben, Vortest,
       Gesamttest): keine Zufallsübung darf eines davon würfeln (HOWTO §15, Sperrliste über die Normalform).
       Geschrieben von seite.py aus zahlen.py. */
    var SPERRE = /*@SPERRE@*/{ sys: [], gl: [], pk: [] };
    function gesperrt(T, A){
      if (T.sys && SPERRE.sys.indexOf(sysSchl(T.sys(A))) >= 0) return true;
      if (T.gl && SPERRE.gl.indexOf(normGl(T.gl(A)).join('|')) >= 0) return true;
      if (T.pk && SPERRE.pk.indexOf(T.pk(A)) >= 0) return true;
      return false;
    }
    function paar(A){ return { x: zText(A.x), y: zText(A.y) }; }
    function vertauscht(e, A){ return !gl(A.x, A.y) && gl(e.x, A.y) && gl(e.y, A.x); }
    var VERT = 'Die Zahlen stimmen, die Reihenfolge nicht: \\(x\\) und \\(y\\) sind vertauscht.';
    function loesL(A){ return '\\mathbb{L} = \\{' + paarTex([A.x, A.y]) + '\\}'; }

    var FAELLE = ['ja, beide Gleichungen stimmen', 'nein, nur (I) stimmt', 'nein, nur (II) stimmt', 'nein, keine stimmt'];
    var TYPEN = {
      /* ── Kapitel 1 ─────────────────────────────────────────────── */
      'paar-pruefen': { felder: ['fall'], muster: 'Antwort: {fall:' + FAELLE.join('|') + '}',
        sys: function(A){ return [A.I, A.II]; },
        eingabe: function(A){ return { fall: A.fall }; },
        neu: function(){
          var p = zufallG(-3, 5), q = zufallG(-3, 5), a, b, d, e;
          do { a = ohne0(-3, 4); b = ohne0(-3, 3); d = ohne0(-3, 4); e = ohne0(-3, 3); } while (a * e - b * d === 0 || (a === d && b === e));
          var I = [a, b, a * p + b * q], II = [d, e, d * p + e * q], art = zufall([0, 1, 2, 3]), u = p, v = q, t = zufall([-1, 1]);
          if (art === 1){ u = p + b * t; v = q - a * t; }          // auf (I), nicht auf (II)
          else if (art === 2){ u = p + e * t; v = q - d * t; }     // auf (II)
          else if (art === 3){ u = p + zufall([-1, 1]); v = q + zufall([-1, 1]); }
          var inI = gl(a * u + b * v, I[2]), inII = gl(d * u + e * v, II[2]);
          var fall = inI && inII ? FAELLE[0] : inI ? FAELLE[1] : inII ? FAELLE[2] : FAELLE[3];
          return { I: I, II: II, u: u, v: v, fall: fall, inI: inI, inII: inII,
            text: 'Ist \\(' + paarTex([u, v]) + '\\) eine Lösung von \\(' + sysT([glT(I), glT(II)]) + '\\)? Setz in beide Gleichungen ein.' }; },
        fehler: function(A){ return FAELLE.filter(function(f){ return f !== A.fall; }).map(function(f){ return [{ fall: f }, null]; }); },
        pruefen: function(A, e){
          if (e.fall === A.fall) return null;
          var sI = A.I[0] * A.u + A.I[1] * A.v, sII = A.II[0] * A.u + A.II[1] * A.v;
          var r = [];
          var sagtI = e.fall === FAELLE[0] || e.fall === FAELLE[1], sagtII = e.fall === FAELLE[0] || e.fall === FAELLE[2];
          if (sagtI !== A.inI) r.push('(I): Links ergibt sich \\(' + texZahl(sI) + '\\), rechts steht \\(' + texZahl(A.I[2]) + '\\)' + (A.inI ? ' — (I) stimmt.' : ' — (I) stimmt nicht.'));
          if (sagtII !== A.inII) r.push('(II): Links ergibt sich \\(' + texZahl(sII) + '\\), rechts steht \\(' + texZahl(A.II[2]) + '\\)' + (A.inII ? ' — (II) stimmt.' : ' — (II) stimmt nicht.'));
          if (e.fall === FAELLE[0] && (A.inI || A.inII)) r.push('Eine Lösung des Systems muss <b>beide</b> Gleichungen erfüllen.');
          return r.join(' '); },
        loesung: function(A){ return '\\text{(I): } ' + texZahl(A.I[0] * A.u + A.I[1] * A.v) + (A.inI ? ' = ' : ' \\neq ') + texZahl(A.I[2]) +
          ';\\ \\ \\text{(II): } ' + texZahl(A.II[0] * A.u + A.II[1] * A.v) + (A.inII ? ' = ' : ' \\neq ') + texZahl(A.II[2]); } },

      'nach-y': { felder: ['m', 'q'], muster: 'y = {m} · x + {q}',
        gl: function(A){ return [A.a, A.b, A.c]; },
        eingabe: function(A){ return { m: zText(A.m), q: zText(A.q) }; },
        neu: function(){
          var b = zufall([1, -1, 2, -2, 2, 3, -3, 4]), m, q;
          do { m = zufall([-3, -2, -1, 1, 2, 3, 0.5, -0.5, 1.5]); q = zufall([-4, -3, -2, -1, 1, 2, 3, 4, 5, 0.5, -1.5]); }
          while (!gl(m * b, Math.round(m * b)) || !gl(q * b, Math.round(q * b)));
          var a = -m * b, c = q * b;
          return { a: a, b: b, c: c, m: m, q: q, text: 'Löse nach \\(y\\) auf: \\(' + glT([a, b, c]) + '\\). (Ist \\(q\\) negativ, gib die negative Zahl ein.)' }; },
        fehler: function(A){
          var f = [[{ m: zText(-A.m), q: zText(A.q) }, 'Vorzeichen']];
          if (A.b !== 1 && !gl(A.c, A.q)) f.push([{ m: zText(A.m), q: zText(A.c) }, 'rechte Seite']);
          if (Math.abs(A.b) !== 1) f.push([{ m: zText(-A.a), q: zText(A.q) }, 'teilen']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.q, A.q)) return null;
          var r = [];
          if (!gl(e.m, A.m)) r.push(gl(e.m, -A.m) ? 'Vorzeichen vor \\(x\\): Beim Hinüberbringen von \\(' + glied(A.a, 'x', true) + '\\) dreht das Vorzeichen' + (A.b < 0 ? ', und beim Teilen durch \\(' + texZahl(A.b) + '\\) dreht es nochmals.' : '.')
            : Math.abs(A.b) !== 1 && gl(e.m, -A.a) ? 'Am Schluss durch \\(' + texZahl(A.b) + '\\) teilen — auch das Glied mit \\(x\\).'
            : 'Zahl vor \\(x\\): erst \\(' + glied(A.a, 'x', true) + '\\) hinüberbringen, dann durch \\(' + texZahl(A.b) + '\\) teilen.');
          if (!gl(e.q, A.q)) r.push(A.b !== 1 && gl(e.q, A.c) ? 'Die rechte Seite gehört auch geteilt: \\(' + texZahl(A.c) + ' : ' + klam(A.b) + '\\).'
            : 'Zahl ohne \\(x\\): \\(' + texZahl(A.c) + ' : ' + klam(A.b) + '\\).');
          return r.join(' '); },
        loesung: function(A){ return linT(A.m, A.q); } },

      /* ── Kapitel 2 ─────────────────────────────────────────────── */
      'einsetzen': { felder: ['x', 'y'], muster: 'x = {x}; y = {y}',
        sys: function(A){ return A.sys; },
        eingabe: paar,
        neu: function(){
          var p = zufallG(-4, 6), r = zufallG(-4, 6), m = zufall([-3, -2, -1, 1, 2, 3]), a = ohne0(-4, 5), b = zufall([-4, -3, -2, 2, 3, 4, 5]), q, nachX = Math.random() < 0.4;
          var I, II, xs;
          if (!nachX){ q = r - m * p; if (q === 0 || Math.abs(q) > 9 || a + b * m === 0) return TYPEN['einsetzen'].neu();
            I = linT(m, q); II = glT([a, b, a * p + b * r]);
            xs = p + (b - 1) * q / (a + b * m);                         // Klammer vergessen: a x + b m x + q = c
            if (gl(xs, r) && gl(m * xs + q, p)) return TYPEN['einsetzen'].neu();   // gleich dem vertauschten Paar: zwei Diagnosen
            return { x: p, y: r, nachX: false, m: m, q: q, a: a, b: b, falschX: xs, falschY: m * xs + q,
              sys: [[-m, 1, q], [a, b, a * p + b * r]], text: 'Löse mit dem Einsetzverfahren: \\(' + sysT([I, II]) + '\\)' }; }
          // x = m y + q in a x + b y = c: der Faktor vor der Klammer ist hier a
          q = p - m * r; if (q === 0 || Math.abs(q) > 9 || b + a * m === 0 || a === 1) return TYPEN['einsetzen'].neu();
          I = linT(m, q, 'y', 'x'); II = glT([a, b, a * p + b * r]);
          var ys = r + (a - 1) * q / (b + a * m);                          // a m y + q + b y = c
          if (gl(ys, p) && gl(m * ys + q, r)) return TYPEN['einsetzen'].neu();
          return { x: p, y: r, nachX: true, m: m, q: q, a: a, b: b, falschY: ys, falschX: m * ys + q,
            sys: [[1, -m, q], [a, b, a * p + b * r]], text: 'Löse mit dem Einsetzverfahren: \\(' + sysT([I, II]) + '\\)' }; },
        fehler: function(A){
          var f = [];
          if (!gl(A.falschX, A.x) || !gl(A.falschY, A.y)) f.push([{ x: zText(A.falschX), y: zText(A.falschY) }, 'Klammer']);
          if (A.x !== A.y) f.push([{ x: zText(A.y), y: zText(A.x) }, 'Reihenfolge']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.y, A.y)) return null;
          if (vertauscht(e, A)) return VERT;
          if (gl(e.x, A.falschX) && gl(e.y, A.falschY)) return 'Klammer vergessen? Der Term aus (I) ersetzt \\(' + (A.nachX ? 'x' : 'y') + '\\) als Ganzes: \\(' +
            (A.nachX ? texZahl(A.a) + ' \\cdot (' + linT(A.m, A.q, 'y', 'x').slice(4) + ')' : texZahl(A.b) + ' \\cdot (' + linT(A.m, A.q).slice(4) + ')') + '\\).';
          if (A.nachX ? gl(e.y, A.y) : gl(e.x, A.x)) return 'Der erste Wert stimmt. Setz ihn in (I) ein, um den zweiten zu berechnen.';
          return 'Setz den Term aus (I) in Klammern in (II) ein, löse nach der verbleibenden Variablen auf und mach die Probe.'; },
        loesung: function(A){ return loesL(A); } },

      'gleichsetzen': { felder: ['x', 'y'], muster: 'x = {x}; y = {y}',
        sys: function(A){ return A.sys; },
        eingabe: paar,
        neu: function(){
          var p = zufallG(-4, 6), r = zufallG(-4, 6), m1 = zufall([-3, -2, -1, 1, 2, 3, 4]), m2, q1, q2, nachX = Math.random() < 0.3;
          do { m2 = zufall([-3, -2, -1, 1, 2, 3]); } while (m2 === m1);
          var u = nachX ? r : p, w = nachX ? p : r;      // u = Variable rechts, w = links
          q1 = w - m1 * u; q2 = w - m2 * u;
          if (q1 === 0 || Math.abs(q1) > 9 || Math.abs(q2) > 9) return TYPEN['gleichsetzen'].neu();
          var V = nachX ? ['y', 'x'] : ['x', 'y'];
          var us = (q2 + q1) / (m1 - m2);                // Vorzeichenfehler: q1 ohne Zeichenwechsel hinüber
          var ws = m1 * us + q1;
          if (gl(nachX ? ws : us, r) && gl(nachX ? us : ws, p)) return TYPEN['gleichsetzen'].neu();   // gleich dem vertauschten Paar
          return { x: p, y: r, nachX: nachX, m1: m1, m2: m2, q1: q1, q2: q2,
            falschX: nachX ? ws : us, falschY: nachX ? us : ws,
            sys: nachX ? [[1, -m1, q1], [1, -m2, q2]] : [[-m1, 1, q1], [-m2, 1, q2]],
            text: 'Löse mit dem Gleichsetzverfahren: \\(' + sysT([linT(m1, q1, V[0], V[1]), linT(m2, q2, V[0], V[1])]) + '\\)' }; },
        fehler: function(A){
          var f = [];
          if (!gl(A.falschX, A.x)) f.push([{ x: zText(A.falschX), y: zText(A.falschY) }, 'Vorzeichen']);
          if (A.x !== A.y) f.push([{ x: zText(A.y), y: zText(A.x) }, 'Reihenfolge']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.y, A.y)) return null;
          if (vertauscht(e, A)) return VERT;
          var v = A.nachX ? 'y' : 'x';
          if (gl(e.x, A.falschX) && gl(e.y, A.falschY)) return 'Vorzeichen beim Hinüberbringen: Steht links \\(' + (A.q1 < 0 ? '-' + (-A.q1) : '+' + A.q1) + '\\), rechnest du beidseitig \\(' + (A.q1 < 0 ? '+' + (-A.q1) : '-' + A.q1) + '\\).';
          if (A.nachX ? gl(e.y, A.y) : gl(e.x, A.x)) return '\\(' + v + '\\) stimmt. Setz es in eine der beiden Gleichungen ein.';
          return 'Setz die beiden rechten Seiten gleich, löse nach \\(' + v + '\\) auf und mach die Probe.'; },
        loesung: function(A){ return loesL(A); } },

      /* ── Kapitel 3 ─────────────────────────────────────────────── */
      'addition': { felder: ['x', 'y'], muster: 'x = {x}; y = {y}',
        sys: function(A){ return [A.I, A.II]; },
        eingabe: paar,
        neu: function(){
          var p = zufallG(-4, 5), r = zufallG(-4, 5), art = zufall(['direkt', 'einmal', 'einmal', 'beide']), a1, b1, a2, b2, k = 1;
          if (art === 'direkt'){ b1 = ohne0(-4, 4); b2 = zufall([-b1, b1]); a1 = ohne0(-4, 5); a2 = ohne0(-4, 5); }
          else if (art === 'einmal'){ k = zufall([2, 3]); b2 = zufall([1, -1, 2, -2]); b1 = -k * b2 * zufall([1, -1]); a1 = ohne0(-3, 5); a2 = ohne0(-3, 4); }
          else { var pr = zufall([[2, 3], [3, 2], [2, 5], [3, 4], [4, 3]]); b1 = pr[0]; b2 = -pr[1]; a1 = ohne0(-4, 5); a2 = ohne0(-4, 5); }
          if (a1 * b2 - a2 * b1 === 0) return TYPEN['addition'].neu();
          var I = [a1, b1, a1 * p + b1 * r], II = [a2, b2, a2 * p + b2 * r];
          var f = null;
          if (art === 'einmal'){
            // rechte Seite von (II) nicht mitmultipliziert: k·a2 x + k·b2 y = c2
            var A2 = k * a2, B2 = k * b2, C2 = II[2], det = a1 * B2 - A2 * b1;
            // nur schöne Fehlerwerte (Vielfache von 1/12), sonst landet niemand darauf; nicht das vertauschte Paar
            if (det !== 0){ var xs = (I[2] * B2 - C2 * b1) / det, ys = (a1 * C2 - A2 * I[2]) / det;
              if ((!gl(xs, p) || !gl(ys, r)) && gl(xs * 12, Math.round(xs * 12)) && gl(ys * 12, Math.round(ys * 12)) && !(gl(xs, r) && gl(ys, p))) f = [xs, ys]; }
          }
          return { x: p, y: r, I: I, II: II, art: art, k: k, falsch: f, text: 'Löse mit dem Additionsverfahren: \\(' + sysT([glT(I), glT(II)]) + '\\)' }; },
        fehler: function(A){
          var f = [];
          if (A.falsch) f.push([{ x: zText(A.falsch[0]), y: zText(A.falsch[1]) }, 'rechte Seite']);
          if (A.x !== A.y) f.push([{ x: zText(A.y), y: zText(A.x) }, 'Reihenfolge']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.y, A.y)) return null;
          if (vertauscht(e, A)) return VERT;
          if (A.falsch && gl(e.x, A.falsch[0]) && gl(e.y, A.falsch[1])) return 'Beim Vervielfachen gehört auch die rechte Seite dazu: \\(' + A.k + ' \\cdot ' + klam(A.II[2]) + ' = ' + texZahl(A.k * A.II[2]) + '\\).';
          if (gl(e.x, A.x) || gl(e.y, A.y)) return 'Ein Wert stimmt. Setz ihn in eine Gleichung ein und rechne den anderen nochmals aus.';
          return 'Mach die Zahlen vor \\(y\\) (oder vor \\(x\\)) entgegengesetzt gleich, addiere die Gleichungen, löse und mach die Probe.'; },
        loesung: function(A){ return loesL(A); } },

      'verfahren-wahl': { felder: ['v', 'x', 'y'], muster: 'Am besten: {v:Einsetzen|Gleichsetzen|Addition}; x = {x}; y = {y}',
        sys: function(A){ return A.sys; },
        eingabe: function(A){ return { v: A.v, x: zText(A.x), y: zText(A.y) }; },
        neu: function(){
          var p = zufallG(-4, 5), r = zufallG(-4, 5), art = zufall(['E', 'G', 'A']), T_, sys, m1, q1, m2, q2, a, b, c;
          if (art === 'E'){ m1 = zufall([-3, -2, 2, 3, -1]); q1 = r - m1 * p; a = ohne0(-4, 5); b = zufall([-3, -2, 2, 3, 4]);
            if (q1 === 0 || Math.abs(q1) > 9 || a + b * m1 === 0) return TYPEN['verfahren-wahl'].neu();
            sys = [[-m1, 1, q1], [a, b, a * p + b * r]]; T_ = [linT(m1, q1), glT(sys[1])]; }
          else if (art === 'G'){ m1 = zufall([-3, -2, -1, 1, 2, 3]); do { m2 = zufall([-3, -2, -1, 1, 2, 4]); } while (m2 === m1);
            q1 = r - m1 * p; q2 = r - m2 * p; if (Math.abs(q1) > 9 || Math.abs(q2) > 9 || q1 === 0) return TYPEN['verfahren-wahl'].neu();
            sys = [[-m1, 1, q1], [-m2, 1, q2]]; T_ = [linT(m1, q1), linT(m2, q2)]; }
          else { var s = zufall([2, 3, 4, 5]); a = ohne0(-4, 5); c = ohne0(-4, 5); if (a === c && Math.random() < 0.7) c = -a + (a > 0 ? -1 : 1);
            sys = [[a, s, a * p + s * r], [c, -s, c * p - s * r]]; if (a + c === 0) return TYPEN['verfahren-wahl'].neu(); T_ = [glT(sys[0]), glT(sys[1])]; }
          return { x: p, y: r, art: art, v: { E: 'Einsetzen', G: 'Gleichsetzen', A: 'Addition' }[art], sys: sys,
            text: 'Welches Verfahren passt am besten? Löse dann: \\(' + sysT(T_) + '\\)' }; },
        fehler: function(A){
          return ['Einsetzen', 'Gleichsetzen', 'Addition'].filter(function(v){ return v !== A.v && !(A.art === 'G' && v === 'Einsetzen'); })
            .map(function(v){ return [{ v: v, x: zText(A.x), y: zText(A.y) }, null]; }); },
        pruefen: function(A, e){
          var r = [];
          // Bei zwei nach y aufgelösten Gleichungen ist Einsetzen dasselbe wie Gleichsetzen — beides zählt.
          var vOk = e.v === A.v || (A.art === 'G' && e.v === 'Einsetzen');
          if (!vOk){
            if (A.art === 'E') r.push('In (I) steht \\(y\\) schon allein: ' + (e.v === 'Gleichsetzen' ? 'Zum Gleichsetzen müsstest du zuerst auch (II) auflösen.' : 'Zum Addieren müsstest du (I) zuerst ordnen.') + ' Einsetzen ist kürzer.');
            else if (A.art === 'G') r.push('Beide Gleichungen sind nach \\(y\\) aufgelöst: Setz die rechten Seiten gleich.');
            else r.push('Vor \\(y\\) stehen entgegengesetzt gleiche Zahlen: Beim Addieren fällt \\(y\\) sofort weg.');
          }
          if (!(gl(e.x, A.x) && gl(e.y, A.y))) r.push(vertauscht(e, A) ? VERT : 'Die Lösung stimmt noch nicht — mach die Probe in beiden Gleichungen.');
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return '\\text{' + A.v + '}:\\ ' + loesL(A); } },

      /* ── Kapitel 4 ─────────────────────────────────────────────── */
      'fall': { felder: ['fall'], muster: '{fall:genau eine Lösung|keine Lösung|unendlich viele Lösungen}',
        sys: function(A){ return A.sys; },
        eingabe: function(A){ return { fall: A.fall }; },
        neu: function(){
          var art = zufall(['eine', 'keine', 'unendlich']), yForm = Math.random() < 0.3, sys, T_, t;
          if (yForm){
            var m = zufall([-3, -2, -1, 1, 2, 3, 0.5]), q = zufallG(-4, 4), m2 = art === 'eine' ? m + zufall([-1, 1, 2]) : m, q2 = art === 'keine' ? q + zufall([-3, -2, 2, 3]) : q;
            if (art === 'unendlich'){ var s = zufall([2, -1, 3]); sys = [[-m, 1, q], [-m * s, s, q * s]]; T_ = [linT(m, q), glT(sys[1])]; }
            else { if (m2 === 0) m2 = m + 3; sys = [[-m, 1, q], [-m2, 1, q2]]; T_ = [linT(m, q), linT(m2, q2)]; }
          } else {
            var a = ohne0(-4, 4), b = ohne0(-4, 4), c = zufallG(-6, 8); t = zufall([2, 3, -1, -2, 0.5]);
            if (art === 'eine'){ var d = ohne0(-4, 4), e = ohne0(-4, 4); if (a * e - b * d === 0) return TYPEN['fall'].neu(); sys = [[a, b, c], [d, e, zufallG(-6, 8)]]; }
            else if (art === 'keine'){ var c2 = t * c + zufall([-3, -2, -1, 1, 2, 3]); sys = [[a, b, c], [t * a, t * b, c2]]; }
            else sys = [[a, b, c], [t * a, t * b, t * c]];
            if (!sys[1].slice(0, 2).every(function(v){ return gl(v, Math.round(v)); }) || !gl(sys[1][2], Math.round(sys[1][2]))) return TYPEN['fall'].neu();
            T_ = [glT(sys[0]), glT(sys[1])];
          }
          return { art: art, sys: sys, fall: { eine: 'genau eine Lösung', keine: 'keine Lösung', unendlich: 'unendlich viele Lösungen' }[art],
            text: 'Welcher Lösungsfall liegt vor? \\(' + sysT(T_) + '\\)' }; },
        fehler: function(A){ return ['genau eine Lösung', 'keine Lösung', 'unendlich viele Lösungen'].filter(function(f){ return f !== A.fall; }).map(function(f){ return [{ fall: f }, null]; }); },
        pruefen: function(A, e){
          if (e.fall === A.fall) return null;
          if (A.art === 'eine') return 'Vergleiche die Zahlen vor \\(x\\) und vor \\(y\\): (II) ist links kein Vielfaches von (I) — die Geraden haben verschiedene Steigungen und schneiden sich.';
          if (e.fall === 'genau eine Lösung') return 'Links ist (II) ein Vielfaches von (I) — gleiche Steigung. Zwei solche Geraden schneiden sich nicht in genau einem Punkt.';
          if (A.art === 'keine') return 'Links passt das Vielfache, rechts nicht: Eliminieren gibt einen Widerspruch wie \\(0 = 5\\) — parallele Geraden.';
          return 'Auch die rechte Seite passt zum Vielfachen: Eliminieren gibt \\(0 = 0\\) — dieselbe Gerade.'; },
        loesung: function(A){ return '\\text{' + A.fall + '}'; } },

      'param-k': { felder: ['k', 'sonst'], muster: 'k = {k}; für alle anderen k: {sonst:keine Lösung|genau eine Lösung|unendlich viele Lösungen}',
        pk: function(A){ return A.schl; },
        eingabe: function(A){ return { k: zText(A.k), sonst: A.sonst }; },
        neu: function(){
          if (Math.random() < 0.5){
            // k in der Konstanten: (I) a x + b y = c, (II) t a x + t b y = k → unendlich viele für k = t c, sonst keine
            var a = ohne0(-4, 4), b = ohne0(-4, 4), c = ohne0(-6, 6), t = zufall([2, 3, -2, -3, -1]);
            return { art: 'konst', a: a, b: b, c: c, t: t, k: t * c, sonst: 'keine Lösung', frage: 'unendlich viele Lösungen',
              schl: 'pk|K|' + normGl([a, b, c]).join('|') + '|' + t,
              text: 'Für welches \\(k\\) hat \\(' + sysT([glT([a, b, c]), lhs([t * a, t * b], ['x', 'y']) + ' = k']) + '\\) unendlich viele Lösungen? Was gilt für alle anderen \\(k\\)?' }; }
          // k im Koeffizienten: (I) k x + r·d y = c1, (II) a x + d y = c2 → proportional für k = r a; c1 ≠ r c2 → keine Lösung
          var r = zufall([2, 3, -2, -1, -3]), d = zufall([1, -1, 2]), a2 = ohne0(-3, 3), c2 = ohne0(-5, 5), c1 = r * c2 + zufall([-3, -2, -1, 1, 2, 3]);
          return { art: 'koeff', r: r, d: d, a2: a2, c1: c1, c2: c2, k: r * a2, sonst: 'genau eine Lösung', frage: 'keine Lösung',
            schl: 'pk|C|' + [r * d, c1, a2, d, c2].join('|'),
            text: 'Für welches \\(k\\) hat \\(' + sysT(['kx' + glied(r * d, 'y', false) + ' = ' + texZahl(c1), glT([a2, d, c2])]) + '\\) keine Lösung? Was gilt für alle anderen \\(k\\)?' }; },
        fehler: function(A){
          var f = [[{ k: zText(-A.k), sonst: A.sonst }, 'Vorzeichen']];
          if (A.art === 'konst' && Math.abs(A.t) !== 1) f.push([{ k: zText(A.c), sonst: A.sonst }, 'Vielfache']);
          if (A.art === 'koeff' && !gl(A.a2 / A.r, A.k) && !gl(A.a2 / A.r, -A.k)) f.push([{ k: zText(A.a2 / A.r), sonst: A.sonst }, 'Verhältnis']);
          f.push([{ k: zText(A.k), sonst: A.sonst === 'keine Lösung' ? 'genau eine Lösung' : 'unendlich viele Lösungen' }, null]);
          return f.filter(function(x){ return !(gl(zahl(x[0].k).wert, A.k) && x[0].sonst === A.sonst); }); },
        pruefen: function(A, e){
          var r = [];
          if (!gl(e.k, A.k)){
            if (gl(e.k, -A.k)) r.push('Vorzeichen: Rechne nach, welches Vielfache von (I) links in (II) steht.');
            else if (A.art === 'konst' && gl(e.k, A.c)) r.push('Links ist (II) das \\(' + texZahl(A.t) + '\\)-Fache von (I) — rechts muss dasselbe Vielfache stehen: \\(' + texZahl(A.t) + ' \\cdot ' + klam(A.c) + '\\).');
            else if (A.art === 'koeff' && gl(e.k, A.a2 / A.r)) r.push('Verhältnis andersherum: Vor \\(y\\) steht in (I) das \\(' + texZahl(A.r) + '\\)-Fache von (II) — vor \\(x\\) also auch.');
            else r.push(A.art === 'konst' ? 'Gleiche Steigung haben die Geraden für jedes \\(k\\). Unendlich viele Lösungen gibt es, wenn auch die Konstanten im selben Verhältnis stehen.' : 'Keine Lösung heisst: gleiche Steigung. Wähle \\(k\\) so, dass die Zahlen vor \\(x\\) und vor \\(y\\) im selben Verhältnis stehen.');
          }
          if (e.sonst !== A.sonst) r.push(A.art === 'konst' ? 'Für die anderen \\(k\\) bleiben die Geraden parallel: keine Lösung.' : 'Für die anderen \\(k\\) sind die Steigungen verschieden: Die Geraden schneiden sich in genau einem Punkt.');
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'k = ' + texZahl(A.k) + '\\ (\\text{' + A.frage + '});\\ \\text{sonst ' + A.sonst + '}'; } },

      /* ── Kapitel 5 ─────────────────────────────────────────────── */
      'stufe': { felder: ['x', 'y', 'z'], muster: 'x = {x}; y = {y}; z = {z}',
        sys: function(A){ return A.sys; },
        eingabe: function(A){ return { x: zText(A.x), y: zText(A.y), z: zText(A.z) }; },
        neu: function(){
          var p = zufallG(-3, 5), q = zufallG(-3, 5), s = zufallG(-3, 4), h = zufall([1, 2, -1, 3, 2]), e = zufall([1, 1, 2, -1]), f = ohne0(-3, 3),
              b = zufallG(-2, 3), c = ohne0(-3, 3), a = zufall([1, 1, 2]);
          var sys = [[a, b, c, a * p + b * q + c * s], [0, e, f, e * q + f * s], [0, 0, h, h * s]];
          return { x: p, y: q, z: s, sys: sys, text: 'Löse das System in Stufenform: \\(' + sysT(sys.map(glT)) + '\\)' }; },
        fehler: function(A){
          return [[{ x: zText(A.x), y: zText(A.y), z: zText(A.z + 1) }, '(III)'], [{ x: zText(A.x), y: zText(A.y + 1), z: zText(A.z) }, '(II)'],
                  [{ x: zText(A.x + 1), y: zText(A.y), z: zText(A.z) }, '(I)']]; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.y, A.y) && gl(e.z, A.z)) return null;
          if (!gl(e.z, A.z)) return 'Beginne unten: (III) enthält nur \\(z\\).';
          if (!gl(e.y, A.y)) return '\\(z\\) stimmt. Setz es in (II) ein — dort fehlt \\(x\\).';
          return '\\(y\\) und \\(z\\) stimmen. Setz beide in (I) ein und löse nach \\(x\\) auf.'; },
        loesung: function(A){ return '\\mathbb{L} = \\{' + paarTex([A.x, A.y, A.z]) + '\\}'; } },

      'eliminieren': { felder: ['a', 'b', 'd'], muster: '{a} · x + {b} · y = {d}',
        sys: function(A){ return [A.I, A.II]; },
        eingabe: function(A){ return { a: zText(A.r[0]), b: zText(A.r[1]), d: zText(A.r[3]) }; },
        neu: function(){
          var c = ohne0(-3, 3), plus = Math.random() < 0.5, I = [ohne0(-3, 4), ohne0(-3, 3), c, zufallG(-6, 9)], II = [ohne0(-3, 4), ohne0(-3, 3), plus ? -c : c, zufallG(-6, 9)];
          var r = I.map(function(v, i){ return plus ? v + II[i] : v - II[i]; });
          if (r[0] === 0 || r[1] === 0) return TYPEN['eliminieren'].neu();
          return { I: I, II: II, plus: plus, r: r, text: 'Berechne (I) ' + (plus ? '+' : '−') + ' (II): \\(' + sysT([glT(I), glT(II)]) + '\\). Welche Gleichung ohne \\(z\\) entsteht? (Negative Zahlen mit Minus.)' }; },
        fehler: function(A){
          var f = [];
          if (!A.plus){ f.push([{ a: zText(A.r[0]), b: zText(A.r[1]), d: zText(A.I[3] + A.II[3]) }, 'rechte Seite']);
            if (A.II[1] !== 0 && A.I[1] + A.II[1] !== A.r[1]) f.push([{ a: zText(A.r[0]), b: zText(A.I[1] + A.II[1]), d: zText(A.r[3]) }, 'Vorzeichen']); }
          else f.push([{ a: zText(A.r[0]), b: zText(A.r[1]), d: zText(A.I[3] - A.II[3]) }, 'rechte Seite']);
          return f.filter(function(x){ return !(gl(zahl(x[0].d).wert, A.r[3]) && gl(zahl(x[0].b).wert, A.r[1])); }); },
        pruefen: function(A, e){
          if (gl(e.a, A.r[0]) && gl(e.b, A.r[1]) && gl(e.d, A.r[3])) return null;
          var r = [];
          if (!gl(e.a, A.r[0])) r.push('Zahl vor \\(x\\): \\(' + texZahl(A.I[0]) + (A.plus ? ' + ' : ' - ') + klam(A.II[0]) + '\\).');
          if (!gl(e.b, A.r[1])) r.push(!A.plus && gl(e.b, A.I[1] + A.II[1]) ? 'Vorzeichen: Beim Subtrahieren wird jede Zahl von (II) abgezogen, auch die vor \\(y\\).' : 'Zahl vor \\(y\\): \\(' + texZahl(A.I[1]) + (A.plus ? ' + ' : ' - ') + klam(A.II[1]) + '\\).');
          if (!gl(e.d, A.r[3])) r.push(gl(e.d, A.plus ? A.I[3] - A.II[3] : A.I[3] + A.II[3]) ? 'Die rechte Seite gehört mit dazu: \\(' + texZahl(A.I[3]) + (A.plus ? ' + ' : ' - ') + klam(A.II[3]) + '\\).' : 'Rechte Seite: \\(' + texZahl(A.I[3]) + (A.plus ? ' + ' : ' - ') + klam(A.II[3]) + '\\).');
          return r.join(' '); },
        loesung: function(A){ return lhs(A.r.slice(0, 2), ['x', 'y']) + ' = ' + texZahl(A.r[3]); } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        A = T.neu();
        for (var v = 0; v < 60 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
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
       g,m,q[,farbe[,stil]] → Gerade y = m·x + q      s,c[,farbe[,stil]] → Senkrechte x = c
       farbe 1 blau, 2 orange, 3 grün, 5 Tinte; stil d = gestrichelt, b = breit.
     dazu data-fenster="x0,x1,y0,y1", data-punkte="x,y;…", data-xm/data-ym, data-titel. ---------- */
  document.querySelectorAll('svg.mini[data-k]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-5,5,-5,5').split(',').map(Number);
    svg.setAttribute('viewBox', '0 0 170 170'); svg.setAttribute('role', 'img');
    var liste = function(t, d){ return t ? t.split(',').map(Number) : d; };
    var K = Achsen(svg, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, sy: +svg.dataset.sy || 1, sx: +svg.dataset.sx || 1, pfeil: 6,
      xm: liste(svg.dataset.xm, []), ym: liste(svg.dataset.ym, []) });
    svg.dataset.k.split(';').filter(Boolean).forEach(function(s){
      var p = s.split(','), art = p[0], cls = 'gerade g' + (p[art === 'g' ? 3 : 2] || '1') + (/d/.test(p[art === 'g' ? 4 : 3] || '') ? ' gestrichelt' : '') + (/b/.test(p[art === 'g' ? 4 : 3] || '') ? ' breit' : '');
      if (art === 'g') K.gerade(-(+p[1]), 1, +p[2], cls); else K.gerade(1, 0, +p[1], cls);
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){ var a = p.split(',').map(Number); K.punkt(a[0], a[1], 'p-loes'); });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
