<script>
/* Leitprogramm Exponential- und Logarithmusfunktionen — Simulationen mit Aufgabenleiste,
   Übungen mit Rückmeldung, Minigrafen. Notation wie auf den Themenseiten 3.4a und 3.4b:
   f(x) = aˣ (a > 0, a ≠ 1), Wachstum N(t) = N₀·aᵗ, e-Funktion, Basiswechsel aˣ = e^(b·x) mit
   b = ln a, Sättigung f(t) = S − (S − A)·e^(−kt), Logarithmusfunktion y = logₐ x.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = Exponentialkurve und Basis a · orange = Startwert und Faktor (N₀, A, b) ·
   grün = Logarithmuskurve und Umkehrfunktion · rot = Gegenbeispiel · Tinte = neutral
   (Asymptote, Sättigungswert, y = x, Läufer). Zahlen mit Dezimalpunkt und echtem Minus. */
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
    // Pfeil in positiver Richtung, Achsenname am Pfeil; bei Anwendungen mit Grösse und Einheit
    var pf = o.pfeil || 7, xn = o.xname || 'x', yn = o.yname || 'y';
    var namen = [];
    if (y0 <= 0 && y1 >= 0){
      el(g, 'polygon', { points: W + ',' + Y(0) + ' ' + (W - pf) + ',' + (Y(0) - pf / 2) + ' ' + (W - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
      namen.push([W - 3, Y(0) - pf, 'end', xn]);
    }
    if (x0 <= 0 && x1 >= 0){
      el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
      namen.push([X(0) + pf, pf + 3, 'start', yn]);
    }
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(Math.max(0, y0)) + 13, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(Math.max(0, x0)) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    var ebene = el(svg, 'g', {});
    var schilder = el(svg, 'g', {});      // Achsennamen über allem, mit Hof
    namen.forEach(function(n){ el(schilder, 'text', { x: n[0], y: n[1], 'text-anchor': n[2], 'class': 'achsname' }, n[3]); });
    return {
      X: X, Y: Y,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      kurve: function(f, cls, a, b){
        var d = '', an = false, A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 400; k++){
          var x = A + (B - A) * k / 400, y = f(x);
          if (y == null || isNaN(y) || !isFinite(y)){ an = false; continue; }
          y = Math.max(y0 - 3 * (y1 - y0), Math.min(y1 + 3 * (y1 - y0), y));
          d += (an ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); an = true;
        }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      senkrecht: function(x, cls){ return el(ebene, 'line', { x1: X(x), y1: 0, x2: X(x), y2: H, 'class': cls }); },
      strecke: function(xa, ya, xb, yb, cls){
        return el(ebene, 'line', { x1: X(xa), y1: Y(ya), x2: X(xb), y2: Y(yb), 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      }
    };
  }

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  function werte(r){ var w = {}; for (var k in r){ w[k] = +r[k].value; r[k].parentNode.querySelector('.sl-val').textContent = z(w[k]); } return w; }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  /* Ein Prozentregler darf nie auf 0 stehenbleiben — ohne Änderung gibt es weder Wachstum
     noch Zerfall. Er springt über die Null hinweg, in die Richtung, aus der er kommt. */
  function ohneNull(inp){
    var letzt = +inp.value, st = parseFloat(inp.step) || 1;
    inp.addEventListener('input', function(){
      if (+inp.value === 0) inp.value = letzt > 0 ? -st : st;
      letzt = +inp.value;
    });
  }

  /* ---------- Aufgabenleiste in der Simulation ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht
     immer — wer hängt, soll nicht festsitzen. Gelöst und übersprungen werden getrennt
     gezählt; am Ende führt «zu den offenen» zurück zu den übersprungenen Aufgaben. */
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
    function gehe(j){ i = j; if (sim.aufraeumen) sim.aufraeumen(); zeigen(); if (sim.zeichnen) sim.zeichnen(); }
    bt.addEventListener('click', function(){
      if (i >= n){ if (anzahl() === n){ erledigt = {}; gehe(0); } else gehe(offen(0)); }
      else gehe(offen(i + 1));
    });
    bv.addEventListener('click', function(){ erledigt = {}; gehe(0); });
    setTimeout(zeigen, 0);
    return pruefen;
  }
  function gleicheMenge(a, b){
    if (a.length !== b.length) return false;
    var u = a.slice().sort(function(p, q){ return p - q; }), v = b.slice().sort(function(p, q){ return p - q; });
    return u.every(function(x, i){ return Math.abs(x - v[i]) < 1e-9; });
  }


  /* ---------- Exponential- und Logarithmusfunktionen ---------- */
  function logA(a, x){ return Math.log(x) / Math.log(a); }
  /* Zahl für die Live-Anzeige: Brüche wie ¼, ⅓ als Bruch, sonst Dezimalzahl; gerundet mit «≈». */
  function zz(v){
    var r = Math.round(v * 1000) / 1000;
    return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(v);
  }
  function basisText(a){
    var k = Math.round(1 / a);
    if (a < 1 && Math.abs(1 / a - k) < 1e-9) return '(1/' + k + ')';
    if (Math.abs(a - Math.E) < 1e-9) return 'e';
    return z(a);
  }
  /* Ein Basisregler darf nie auf 1 stehenbleiben — 1ˣ = 1 ist keine Exponentialfunktion.
     Er springt über die 1 hinweg, in die Richtung, aus der er kommt. */
  function ohneEins(inp){
    var letzt = +inp.value, st = parseFloat(inp.step) || 0.1;
    inp.addEventListener('input', function(){
      if (Math.abs(+inp.value - 1) < 1e-9) inp.value = letzt > 1 ? 1 - st : 1 + st;
      letzt = +inp.value;
    });
  }

  /* ---------- Kapitel 1: die Exponentialfunktion ----------
     Unterschied zur Animation «Interaktive Darstellungen» auf Themenseite 3.4a: dort sieben
     feste Basen zum Anklicken und eine Wertetabelle. Hier läuft a stufenlos von 0.2 bis 4 —
     über die 1 hinweg, wo Wachstum zu Zerfall wird —, und die drei Punkte (−1 | 1/a),
     (0 | 1), (1 | a) tragen ihre Werte mit. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -3, x1: 3, y0: -1, y1: 9, sy: 1, xm: [-2, -1, 1, 2], ym: [2, 4, 6, 8] });
    var ziel = null, pruefen = function(){}, bewegt = {}, gesehen = {};
    ohneEins(fig.querySelector('input[data-p="a"]'));
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function zust(){ var w = werte(r); gesehen[w.a > 1 ? 'g' : 'k'] = true;
      return { a: w.a, bewegt: bewegt, beide: gesehen.g && gesehen.k }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; gesehen = {}; } };
    function zeichnen(){
      var s = zust(), a = s.a;
      K.leeren();
      K.strecke(-3, 0, 3, 0, 'asym hilfslinie');
      if (ziel) K.kurve(function(x){ return Math.pow(ziel, x); }, 'zielkurve');
      K.kurve(function(x){ return Math.pow(a, x); }, 'kurve');
      K.punkt(0, 1, 'p-pkt', '(0 | 1)', -8, -8, 'end');
      K.punkt(1, a, 'p-pkt', '(1 | ' + z(a) + ')', 8, -8);
      K.punkt(-1, 1 / a, 'p-pkt', '(−1 | ' + zz(1 / a) + ')', -8, -10, 'end');
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + sp('tx-blau', z(a)) + '<sup>x</sup> &nbsp;·&nbsp; '
        + (a > 1 ? '<b>Wachstum</b>: steigt' : '<b>Zerfall</b>: fällt') + ' &nbsp;·&nbsp; je Schritt mal ' + z(a);
      pruefen();
    }
    function nah(a, b){ return Math.abs(a - b) < 1e-9; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh die Basis \\(a\\) einmal unter 1 und einmal über 1. Was ändert sich?',
        ok: function(s){ return s.beide; } },
      // Startzustand a = 2 (wie im Clip) — keine Aufgabe trifft ihn.
      { text: 'Stell eine <b>fallende</b> Kurve ein.', ok: function(s){ return s.a < 1; } },
      { text: 'Bau nach: \\(f(x) = 4^x\\)', ok: function(s){ return nah(s.a, 4); } },
      { text: 'Stell das <b>Spiegelbild</b> von \\(4^x\\) an der \\(y\\)-Achse ein.', ok: function(s){ return nah(s.a, 0.25); } },
      { text: 'Stell die Kurve ein, die durch \\((-1 \\mid 5)\\) geht.', ok: function(s){ return nah(s.a, 0.2); } },
      { text: 'Stell die Kurve ein, die durch \\((2 \\mid 6.25)\\) geht.', ok: function(s){ return nah(s.a, 2.5); } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = 0.6; }, ok: function(s){ return nah(s.a, 0.6); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Wachstum und Zerfall ----------
     Unterschied zur Animation «Bakterienkultur» auf Themenseite 3.4a: dort ist der Faktor
     fest (Verdopplung). Hier stellt man Startwert und Prozentsatz ein, die Anzeige übersetzt
     den Prozentsatz in den Faktor, und ein Läufer liest N(t) ab. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -0.6, x1: 6, y0: -60, y1: 1200, sx: 1, sy: 200,
      xm: [1, 2, 3, 4, 5], ym: [200, 400, 600, 800, 1000], xname: 't', yname: 'N' });
    var ziel = null, pruefen = function(){}, bewegt = {};
    ohneNull(fig.querySelector('input[data-p="p"]'));
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function zust(){ var w = werte(r), a = 1 + w.p / 100;
      return { n0: w.n0, p: w.p, a: a, t: w.t, nt: w.n0 * Math.pow(a, w.t), bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (ziel) K.kurve(function(t){ return ziel[0] * Math.pow(ziel[1], t); }, 'zielkurve');
      K.kurve(function(t){ return s.n0 * Math.pow(s.a, t); }, 'kurve');
      K.punkt(0, s.n0, 'p-start', '(0 | ' + z(s.n0) + ')', 8, -8);
      K.punkt(s.t, s.nt, 'p-lauf', '(' + z(s.t) + ' | ' + zz(s.nt) + ')', s.t > 4 ? -8 : 8, -10, s.t > 4 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML = 'N(t) = ' + sp('tx-orange', z(s.n0)) + ' · ' + sp('tx-blau', z(s.a)) + '<sup>t</sup>'
        + ' &nbsp;·&nbsp; ' + (s.p > 0 ? '+' : '−') + Math.abs(s.p) + ' % je Schritt → Faktor ' + sp('tx-blau', z(s.a))
        + ' &nbsp;·&nbsp; N(' + z(s.t) + ') ' + (Math.abs(s.nt - Math.round(s.nt * 1000) / 1000) > 1e-9 ? '≈ ' : '= ') + z(s.nt);
      pruefen();
    }
    function nah(a, b){ return Math.abs(a - b) < 1e-9; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh am Prozentsatz. Wann steigt die Kurve, wann fällt sie?', ok: function(s){ return s.bewegt.p; } },
      // Startzustand N₀ = 200, +50 % (wie im Clip) — keine Aufgabe trifft ihn.
      { text: 'Stell einen <b>Zerfall</b> um 20 % pro Schritt ein.', ok: function(s){ return s.p === -20; } },
      { text: 'Stell ein Modell ein, das sich in jedem Schritt <b>verdoppelt</b>.', ok: function(s){ return s.p === 100; } },
      { text: 'Stell \\(N_0 = 400\\) und eine <b>Halbierung</b> pro Schritt ein und lies \\(N(3)\\) ab.',
        ok: function(s){ return s.n0 === 400 && s.p === -50 && s.t === 3; } },
      { text: 'Stell ein Modell mit \\(N(0) = 100\\) und \\(N(2) = 144\\) ein.', ok: function(s){ return s.n0 === 100 && s.p === 20; } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [300, 0.9]; },
        ok: function(s){ return s.n0 === 300 && s.p === -10; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: e-Funktion und Basiswechsel ----------
     Keine Animation der Themenseite zeigt den Basiswechsel. Hier liegt die Zielkurve cˣ fest,
     und man baut sie mit a^(b·x) nach — zur Basis 2 oder zur Basis e. Passt b, liegen die
     beiden Kurven aufeinander: dann ist b = log_a c, bei Basis e also b = ln c. */
  var BASEN3 = [0.25, 0.5, 2, 3, 4, 8, 9];
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -2, x1: 2, y0: -0.5, y1: 9, sy: 1, xm: [-1, 1], ym: [2, 4, 6, 8] });
    var pruefen = function(){}, bewegt = {};
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    if (schalter) schalter.addEventListener('change', function(){ bewegt.e = true; zeichnen(); });
    function zust(){
      var w = werte(r), c = BASEN3[w.c], e = !!(schalter && schalter.checked), a = e ? Math.E : 2;
      r.c.parentNode.querySelector('.sl-val').textContent = basisText(c);
      return { c: c, b: w.b, e: e, a: a, passt: Math.abs(w.b - logA(a, c)) < 0.03, bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      K.kurve(function(x){ return Math.pow(s.c, x); }, 'kurve');
      K.kurve(function(x){ return Math.pow(s.a, s.b * x); }, 'kurve gruen gestrichelt');
      rolle(fig, 'formel').innerHTML = 'Ziel: y = ' + sp('tx-blau', basisText(s.c)) + '<sup>x</sup> &nbsp;·&nbsp; gebaut: y = '
        + (s.e ? 'e' : '2') + '<sup>' + sp('tx-orange', z(s.b)) + '·x</sup> &nbsp;·&nbsp; '
        + (s.passt ? '<b>passt</b>: b ' + (Math.abs(s.b - Math.round(s.b)) < 1e-9 && !s.e ? '= ' : '≈ ') + (s.e ? 'ln ' : 'log₂ ') + basisText(s.c)
                   : 'passt noch nicht');
      fig.classList.toggle('treffer', s.passt);
      pruefen();
    }
    function fall(c, e, text){ return { text: text, ok: function(s){ return s.c === c && s.e === e && s.passt; } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(b\\). Wann liegt die gestrichelte Kurve auf der blauen?', ok: function(s){ return s.bewegt.b; } },
      // Startzustand: Ziel 4ˣ, Basis 2, b = 1 — passt nicht.
      fall(4, false, 'Schreib \\(4^x\\) als \\(2^{bx}\\): Stell \\(b\\) ein.'),
      fall(0.25, false, 'Stell \\(c = \\tfrac14\\) ein und schreib \\(\\left(\\tfrac14\\right)^x\\) als \\(2^{bx}\\).'),
      fall(9, true, 'Stell \\(c = 9\\) ein. Zur Basis 2 passt keine schöne Zahl — setz den Haken «Basis \\(e\\)» und triff \\(9^x\\) mit \\(e^{bx}\\).'),
      fall(2, true, 'Basis \\(e\\): Schreib \\(2^x\\) als \\(e^{bx}\\). Welches \\(b\\) ist es ungefähr?'),
      fall(0.5, true, 'Basis \\(e\\): Und \\(\\left(\\tfrac12\\right)^x\\)? Achte auf das Vorzeichen von \\(b\\).'),
      fall(3, true, 'Basis \\(e\\): Schreib \\(3^x\\) als \\(e^{bx}\\).')
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Sättigung ----------
     Unterschied zur Themenseite 3.4a: dort steht das Sättigungsmodell nur als Formel mit dem
     Kaffee-Beispiel. Hier stellt man Startwert A, Sättigungswert S und k ein; die Asymptote
     y = S und der Rückstand S − f(t) sind eingezeichnet. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -5, x1: 40, y0: -5, y1: 110, sx: 10, sy: 20,
      xm: [10, 20, 30], ym: [20, 40, 60, 80, 100], xname: 't', yname: 'y' });
    var ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function zust(){ var w = werte(r); return { A: w.A, S: w.S, k: w.k, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var s = zust(), f = function(t){ return s.S - (s.S - s.A) * Math.exp(-s.k * t); };
      K.leeren();
      K.strecke(-5, s.S, 40, s.S, 'asym hilfslinie');
      if (ziel) K.kurve(function(t){ return ziel[1] - (ziel[1] - ziel[0]) * Math.exp(-ziel[2] * t); }, 'zielkurve', 0, 40);
      K.kurve(f, 'kurve', 0, 40);
      K.strecke(10, f(10), 10, s.S, 'rueckstand hilfslinie');
      K.punkt(0, s.A, 'p-start', '(0 | ' + z(s.A) + ')', 8, s.A > s.S ? -8 : 16);
      var D = s.S - s.A;
      rolle(fig, 'formel').innerHTML = 'f(t) = ' + z(s.S) + (D >= 0 ? ' − ' : ' + ') + z(Math.abs(D)) + '·e<sup>−' + z(s.k) + 't</sup>'
        + ' &nbsp;·&nbsp; Start ' + sp('tx-orange', z(s.A)) + ', Sättigung ' + z(s.S) + ' &nbsp;·&nbsp; '
        + (s.A < s.S ? 'steigt gegen ' + z(s.S) : s.A > s.S ? 'fällt gegen ' + z(s.S) : 'bleibt konstant')
        + '<br>Rückstand bei t = 10: ' + zz(Math.abs(D) * Math.exp(-10 * s.k));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(k\\). Was ändert sich — und was bleibt?', ok: function(s){ return s.bewegt.k; } },
      // Startzustand Kaffee A = 80, S = 20, k = 0.07 (wie im Clip) — keine Aufgabe trifft ihn.
      { text: 'Stell einen Akku ein, der von 20 % auf 100 % lädt.', ok: function(s){ return s.A === 20 && s.S === 100; } },
      { text: 'Stell eine Abkühlung von 90 °C auf eine Raumtemperatur von 25 °C ein.', ok: function(s){ return s.A === 90 && s.S === 25; } },
      { text: 'Was geschieht, wenn Startwert und Sättigungswert gleich sind? Stell es ein.', ok: function(s){ return s.A === s.S; } },
      { text: 'Bau nach: \\(f(t) = 50 - 40\\,e^{-0.2t}\\)', ok: function(s){ return s.A === 10 && s.S === 50 && Math.abs(s.k - 0.2) < 1e-9; } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [0, 60, 0.15]; },
        ok: function(s){ return s.A === 0 && s.S === 60 && Math.abs(s.k - 0.15) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: die Logarithmusfunktion ----------
     Unterschied zur Animation «Spiegelung an der Winkelhalbierenden» auf Themenseite 3.4b:
     dort vier feste Basen ohne Ablesen. Hier gehört ein Läufer dazu, der logₐ x abliest —
     so wird der Logarithmus als «gesuchter Exponent» am Graphen sichtbar. */
  var BASEN5 = [0.5, 2, Math.E, 3, 10];
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -2, x1: 11, y0: -4, y1: 9, sy: 1,
      xm: [2, 4, 6, 8, 10], ym: [-2, 2, 4, 6, 8] });
    var pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function zust(){ var w = werte(r), a = BASEN5[w.a];
      r.a.parentNode.querySelector('.sl-val').textContent = basisText(a);
      return { a: a, x: w.x, y: logA(a, w.x), bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      K.kurve(function(x){ return x; }, 'normal hilfslinie');
      K.kurve(function(x){ return Math.pow(s.a, x); }, 'kurve hilfslinie');
      K.senkrecht(0, 'asym');
      K.kurve(function(x){ return x > 0 ? logA(s.a, x) : NaN; }, 'kurve gruen', 0.0005, 11);
      K.punkt(s.x, s.y, 'p-lauf', '(' + z(s.x) + ' | ' + zz(s.y) + ')', 8, s.y > 0 ? -10 : 16);
      var name = s.a === 10 ? 'lg' : Math.abs(s.a - Math.E) < 1e-9 ? 'ln' : 'log<sub>' + basisText(s.a) + '</sub>';
      rolle(fig, 'formel').innerHTML = 'y = ' + name + ' x &nbsp;·&nbsp; Umkehrfunktion von y = ' + sp('tx-blau', basisText(s.a)) + '<sup>x</sup>'
        + '<br>Läufer: ' + name + ' ' + z(s.x) + ' ' + (Math.abs(s.y - Math.round(s.y * 1000) / 1000) > 1e-9 ? '≈ ' : '= ') + z(s.y);
      pruefen();
    }
    function nah(a, b){ return Math.abs(a - b) < 1e-9; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Fahr den Läufer von links nach rechts. Wo ist der Logarithmus negativ, wo null?', ok: function(s){ return s.bewegt.x; } },
      // Startzustand Basis 2, Läufer bei x = 4 — keine Aufgabe trifft ihn.
      { text: 'Basis 2: Bring den Läufer auf \\(\\log_2 8\\). Wie gross ist der Wert?', ok: function(s){ return s.a === 2 && nah(s.x, 8); } },
      { text: 'Basis 3: Finde die Stelle \\(x\\), an der \\(\\log_3 x = 2\\) ist.', ok: function(s){ return s.a === 3 && nah(s.x, 9); } },
      { text: 'Bring den Läufer auf die Nullstelle. Gilt sie für jede Basis?', ok: function(s){ return nah(s.x, 1); } },
      { text: 'Stell die <b>fallende</b> Logarithmuskurve ein.', ok: function(s){ return s.a < 1; } },
      { text: 'Basis 10: Wo ist \\(\\lg x = 1\\)?', ok: function(s){ return s.a === 10 && nah(s.x, 10); } },
      { text: 'Basis 2: Lies \\(\\log_2 0.5\\) ab.', ok: function(s){ return s.a === 2 && nah(s.x, 0.5); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Hilfslinien-Schalter ---------- */
  document.querySelectorAll('.hilfs-schalter input').forEach(function(hs){
    var fig = hs.closest('figure');
    hs.addEventListener('change', function(){ fig.classList.toggle('ohne-hilfslinien', !hs.checked); });
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    /* Zahl in LaTeX: ganze Zahl, Stammbruch als \tfrac{1}{n}, sonst Dezimalzahl. */
    function zT(v){
      if (Math.abs(v - Math.round(v)) < 1e-9) return tz(Math.round(v));
      var k = Math.round(1 / Math.abs(v));
      if (Math.abs(1 / Math.abs(v) - k) < 1e-9) return (v < 0 ? '-' : '') + '\\tfrac{1}{' + k + '}';
      return tz(Math.round(v * 1e6) / 1e6);
    }
    function basT(a){ return a < 1 ? '\\left(' + zT(a) + '\\right)' : zT(a); }
    function pot(a, n){ return Math.pow(a, n); }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15). Je Typ ein eigener
       Schlüssel (T.schl). Reihenfolge: Clips · Simulationen · Aufgaben der Kapitel · Vortest · Gesamttest. */
    var SPERRE = [
      'w|5|-1', 'w|2|3', 'w|4|-1', 'w|4|0.5', 'w|4|1.5',
      'b|2|3', 'b|3|2', 'b|-1|0.2', 'b|2|2.5', 'b|2|5', 'b|-2|0.25', 'b|3|0.1', 'b|-3|0.5',
      'g|3', 'g|0.5',
      'n|200|1.5|2', 'n|200|1.5|3', 'n|2000|1.05|2', 'n|400|0.5|3', 'n|100|1.2|2',
      'h|80|4|8', 'h|80|4|12', 'h|64|5|15', 'h|120|8|24', 'h|240|6|18',
      'c|8|2', 'c|9|3', 'c|4|2', 'c|16|2', 'c|0.125|2', 'c|0.25|2',
      'e|5', 'e|2', 'e|0.5',
      'l|2|8', 'l|2|32', 'l|2|64', 'l|2|0.125', 'l|10|1000', 'l|2|16', 'l|10|0.001', 'l|3|9', 'l|2|0.5', 'l|10|10',
      'u|3|-1', 'u|3|1', 'u|2|-3',
      'q|3|2|96', 'q|5|2|160',
      // Gesamttest (downloads/leitprogramme/exp-log-funktionen/gesamttest.tex)
      'n|500|1.2|2', 'c|' + (1 / 9) + '|3', 'l|2|0.0625', 'l|10|0.01'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    var TYPEN = {
      /* ── Kapitel 1: die Exponentialfunktion ──────────────────── */
      'exp-wert': { felder: ['y'], muster: 'f(x₁) = {y}',
        schl: function(A){ return 'w|' + A.a + '|' + A.x; },
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){ var a = zufall([2, 3, 4, 5, 10, 0.5, 0.25]), x = zufall([-3, -2, -1, 0, 1, 2, 3]);
          if (a === 10 && x > 2) x = 2; if ((a === 5 || a === 4) && x > 3) x = 3;
          return { a: a, x: x, y: pot(a, x),
            text: 'Berechne \\(f(' + tz(x) + ')\\) für \\(f(x) = ' + basT(a) + '^{x}\\) ohne Taschenrechner (Bruch oder Dezimalzahl).' }; },
        fehler: function(A){ var f = [];
          if (A.x < 0 && !gl(-pot(A.a, -A.x), A.y)) f.push([{ y: String(-pot(A.a, -A.x)) }, 'Kehrwert']);
          if (A.x !== 0 && A.x !== 1 && !gl(A.a * A.x, A.y) && !gl(A.a * A.x, -pot(A.a, -A.x))) f.push([{ y: String(A.a * A.x) }, 'kein Faktor']);
          if (A.x === 0 && A.a !== 1) f.push([{ y: '0' }, 'hoch null']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (A.x === 0) return 'Jede Basis hoch null ist \\(1\\) — darum gehen alle Kurven durch \\((0 \\mid 1)\\).';
          if (A.x < 0 && gl(e.y, -pot(A.a, -A.x))) return 'Ein negativer Exponent bedeutet den Kehrwert, nicht ein negatives Ergebnis: \\(a^{-n} = \\frac{1}{a^n}\\).';
          if (gl(e.y, A.a * A.x)) return 'Der Exponent ist kein Faktor: \\(' + basT(A.a) + '^{' + tz(A.x) + '}\\) heisst ' + Math.abs(A.x) + '-mal mit der Basis multiplizieren.';
          return 'Rechne \\(' + basT(A.a) + '^{' + Math.abs(A.x) + '}\\)' + (A.x < 0 ? ' und nimm davon den Kehrwert.' : '.'); },
        loesung: function(A){ return basT(A.a) + '^{' + tz(A.x) + '} = ' + zT(A.y); } },

      'basis-punkt': { felder: ['a'], muster: 'a = {a}',
        schl: function(A){ return 'b|' + A.n + '|' + A.a; },
        eingabe: function(A){ return { a: String(A.a) }; },
        neu: function(){ var a = zufall([2, 3, 4, 5, 10, 0.5, 0.2, 0.25]), n = zufall([2, 3, -1, -2]);
          if (a === 10 && n === 3) n = 2; if ((a === 0.2 || a === 0.25) && n === 3) n = -2;
          var v = pot(a, n);
          return { a: a, n: n, v: v,
            text: 'Der Graph von \\(y = a^x\\) geht durch \\((' + tz(n) + ' \\mid ' + zT(v) + ')\\). Bestimme die Basis \\(a\\).' }; },
        fehler: function(A){ var f = [], q = A.v / A.n;
          if (!gl(q, A.a) && q > 0) f.push([{ a: String(q) }, 'teilen']);
          if (A.n < 0 && !gl(1 / A.a, A.a)) f.push([{ a: String(1 / A.a) }, 'Kehrwert']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, A.v / A.n)) return 'Nicht teilen: Gesucht ist die Zahl, deren \\(' + tz(A.n) + '\\)-te Potenz \\(' + zT(A.v) + '\\) ist.';
          if (A.n < 0 && gl(e.a, 1 / A.a)) return 'Der Exponent ist negativ: \\(a^{' + tz(A.n) + '} = \\frac{1}{a^{' + (-A.n) + '}}\\). Den Kehrwert beachten.';
          if (e.a <= 0) return 'Die Basis einer Exponentialfunktion ist positiv.';
          return 'Setz ein: \\(a^{' + tz(A.n) + '} = ' + zT(A.v) + '\\), dann die ' + (A.n < 0 ? 'Kehrwert-' : '') + 'Wurzel ziehen.'; },
        loesung: function(A){ return 'a^{' + tz(A.n) + '} = ' + zT(A.v) + ' \\Rightarrow a = ' + zT(A.a); } },

      'graf-basis': { felder: ['a'], muster: 'f(x) = {a}ˣ', graf: true,
        schl: function(A){ return 'g|' + A.a; },
        eingabe: function(A){ return { a: String(A.a) }; },
        neu: function(){ var a = zufall([2, 3, 4, 0.5, 1 / 3, 0.25]);
          return { a: a, text: 'Lies die Basis \\(a\\) am Graphen von \\(y = a^x\\) ab (der markierte Punkt liegt auf einem Gitterpunkt). Bruch oder Dezimalzahl.' }; },
        zeichne: function(bild, A){
          var K = Achsen(bild, { w: 170, h: 170, x0: -3, x1: 3, y0: -0.6, y1: 5.4, r: 3.5, pfeil: 6, xm: [-2, -1, 1, 2], ym: [1, 2, 3, 4] });
          K.kurve(function(x){ return Math.pow(A.a, x); }, 'kurve');
          if (A.a > 1) K.punkt(1, A.a, 'p-pkt'); else K.punkt(-1, 1 / A.a, 'p-pkt'); },
        fehler: function(A){ return [[{ a: String(1 / A.a) }, A.a > 1 ? 'steigt' : 'fällt']]; },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, 1 / A.a)) return A.a > 1 ? 'Die Kurve steigt — die Basis ist also grösser als 1.' : 'Die Kurve fällt — die Basis ist also kleiner als 1. Bei \\(x = -1\\) steht der Kehrwert \\(\\frac{1}{a}\\).';
          return A.a > 1 ? 'Bei \\(x = 1\\) steht die Basis: \\(f(1) = a\\).' : 'Bei \\(x = -1\\) steht \\(\\frac{1}{a}\\). Daraus \\(a\\).'; },
        loesung: function(A){ return A.a > 1 ? 'f(1) = ' + zT(A.a) + ' \\Rightarrow a = ' + zT(A.a) : 'f(-1) = \\tfrac{1}{a} = ' + zT(1 / A.a) + ' \\Rightarrow a = ' + zT(A.a); } },

      /* ── Kapitel 2: Wachstum und Zerfall ─────────────────────── */
      'prozent-faktor': { felder: ['w'], muster: '{w}',
        eingabe: function(A){ return { w: String(A.loes) }; },
        neu: function(){ var p = zufall([3, 5, 8, 12, 15, 20, 25, 40, 60]) * zufall([1, -1]), richtung = Math.random() < 0.5;
          var a = Math.round((1 + p / 100) * 1000) / 1000;
          return richtung ? { p: p, a: a, loes: a, art: 'f', text: 'Eine Grösse ' + (p > 0 ? 'wächst pro Jahr um ' + p + ' %' : 'nimmt pro Jahr um ' + (-p) + ' % ab') + '. Mit welchem Faktor wird jährlich multipliziert?' }
                          : { p: p, a: a, loes: p, art: 'p', text: 'Der Faktor pro Jahr ist \\(' + a + '\\). Um wie viel Prozent ändert sich die Grösse pro Jahr? (Abnahme negativ, z. B. −5)' }; },
        fehler: function(A){ return A.art === 'f' ? [[{ w: String(Math.round(A.p) / 100) }, 'dazu'], [{ w: String(1 - A.p / 100) }, 'Vorzeichen']].filter(function(p){ return !gl(+p[0].w, A.a); })
                                       : [[{ w: String(-A.p) }, 'Vorzeichen'], [{ w: String(A.a * 100) }, '100 %']].filter(function(p){ return !gl(+p[0].w, A.p); }); },
        pruefen: function(A, e){
          if (gl(e.w, A.loes)) return null;
          if (A.art === 'f'){
            if (gl(e.w, A.p / 100)) return 'Das ist nur die Änderung. Die 100 %, die schon da sind, gehören dazu: \\(1 ' + (A.p > 0 ? '+' : '-') + ' ' + Math.abs(A.p) / 100 + '\\).';
            if (gl(e.w, 1 - A.p / 100)) return 'Vorzeichen: ' + (A.p > 0 ? 'Wachstum heisst Faktor grösser als 1.' : 'Abnahme heisst Faktor kleiner als 1.');
            return 'Rechne \\(1 ' + (A.p > 0 ? '+' : '-') + ' \\frac{' + Math.abs(A.p) + '}{100}\\).'; }
          if (gl(e.w, -A.p)) return 'Vorzeichen: Ist der Faktor ' + (A.a > 1 ? 'grösser als 1, wächst' : 'kleiner als 1, schrumpft') + ' die Grösse.';
          if (gl(e.w, A.a * 100)) return 'Das sind die Prozent, die nach einem Jahr da sind. Gefragt ist die Änderung: davon 100 % abziehen.';
          return 'Faktor minus 1, mal 100.'; },
        loesung: function(A){ return A.art === 'f' ? 'a = 1 ' + (A.p > 0 ? '+' : '-') + ' ' + Math.abs(A.p) / 100 + ' = ' + A.a : '(' + A.a + ' - 1) \\cdot 100\\,\\% = ' + tz(A.p) + '\\,\\%'; } },

      'wachstum-wert': { felder: ['n'], muster: 'N(t) = {n}',
        schl: function(A){ return 'n|' + A.n0 + '|' + A.a + '|' + A.t; },
        eingabe: function(A){ return { n: String(A.n) }; },
        neu: function(){ var n0 = zufall([100, 200, 400, 500, 1000]), a = zufall([1.1, 1.2, 1.5, 2, 0.5, 0.8, 0.9]), t = zufall([2, 3]);
          return { n0: n0, a: a, t: t, n: Math.round(n0 * pot(a, t) * 1e6) / 1e6,
            text: 'Gegeben \\(N(t) = ' + n0 + ' \\cdot ' + a + '^{t}\\). Berechne \\(N(' + t + ')\\) ohne Taschenrechner.' }; },
        fehler: function(A){ var f = [], lin = A.n0 * (1 + (A.a - 1) * A.t), mal = A.n0 * A.a * A.t;
          if (!gl(lin, A.n)) f.push([{ n: String(Math.round(lin * 1e6) / 1e6) }, 'linear']);
          if (!gl(mal, A.n) && !gl(mal, lin)) f.push([{ n: String(Math.round(mal * 1e6) / 1e6) }, 'kein Faktor']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.n, A.n)) return null;
          if (gl(e.n, A.n0 * (1 + (A.a - 1) * A.t))) return 'Das wäre linear — jedes Mal derselbe Zuwachs. Exponentiell wird jedes Mal mit \\(' + A.a + '\\) multipliziert, auch der Zuwachs.';
          if (gl(e.n, A.n0 * A.a * A.t)) return 'Der Exponent ist kein Faktor: \\(' + A.a + '^{' + A.t + '}\\) heisst ' + A.t + '-mal mit \\(' + A.a + '\\) multiplizieren.';
          return 'Schritt für Schritt: \\(' + A.n0 + ' \\cdot ' + A.a + ' = ' + Math.round(A.n0 * A.a * 1e6) / 1e6 + '\\), dann weiter mal \\(' + A.a + '\\).'; },
        loesung: function(A){ return 'N(' + A.t + ') = ' + A.n0 + ' \\cdot ' + A.a + '^{' + A.t + '} = ' + A.n; } },

      'halbwertszeit': { felder: ['m'], muster: 'm = {m}',
        schl: function(A){ return 'h|' + A.m0 + '|' + A.T + '|' + A.t; },
        eingabe: function(A){ return { m: String(A.m) }; },
        neu: function(){ var j = zufall([1, 2, 3, 4]), T = zufall([2, 3, 4, 5, 6, 8, 10]), m0 = zufall([16, 32, 48, 64, 80, 96, 160, 240]);
          var verd = Math.random() < 0.3;
          return { m0: m0, T: T, t: j * T, j: j, verd: verd, m: verd ? m0 * pot(2, j) : m0 / pot(2, j),
            text: verd ? 'Eine Kultur von ' + m0 + ' Zellen verdoppelt sich alle ' + T + ' Stunden. Wie viele Zellen sind es nach ' + j * T + ' Stunden?'
                       : 'Ein Stoff hat eine Halbwertszeit von ' + T + ' Tagen. Von ' + m0 + ' mg — wie viel ist nach ' + j * T + ' Tagen übrig?' }; },
        fehler: function(A){ var f = [], lin = A.verd ? A.m0 * (1 + A.j) : A.m0 / (2 * A.j);
          if (!gl(lin, A.m) && A.j > 1) f.push([{ m: String(lin) }, 'nicht']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m)) return null;
          if (A.j > 1 && gl(e.m, A.verd ? A.m0 * (1 + A.j) : A.m0 / (2 * A.j))) return 'Das wäre nicht exponentiell: In jeder ' + (A.verd ? 'Verdopplungszeit wird verdoppelt' : 'Halbwertszeit wird halbiert') + ' — immer vom neuen Wert aus.';
          return 'Zähl, wie oft \\(' + A.T + '\\) in \\(' + A.t + '\\) passt, und ' + (A.verd ? 'verdopple' : 'halbiere') + ' so oft.'; },
        loesung: function(A){ return A.m0 + ' \\cdot ' + (A.verd ? '2' : '\\left(\\tfrac12\\right)') + '^{' + A.t + '/' + A.T + '} = ' + A.m0 + ' \\cdot ' + (A.verd ? '2' : '\\left(\\tfrac12\\right)') + '^{' + A.j + '} = ' + A.m; } },

      /* ── Kapitel 3: e-Funktion und Basiswechsel ──────────────── */
      'basiswechsel': { felder: ['b'], muster: 'b = {b}',
        schl: function(A){ return 'c|' + A.c + '|' + A.a; },
        eingabe: function(A){ return { b: String(A.b) }; },
        neu: function(){ var a = zufall([2, 3, 5, 10]), b = zufall([2, 3, -1, -2, 0.5]);
          if (a === 10 && Math.abs(b) > 2) b = 2; if (a === 5 && b === 3) b = -1;
          return { a: a, b: b, c: pot(a, b),
            text: 'Schreib \\(' + (b === 0.5 ? '\\left(\\sqrt{' + a + '}\\right)' : basT(pot(a, b))) + '^{x}\\) in der Form \\(' + a + '^{b\\,x}\\). Wie gross ist \\(b\\)?' }; },
        fehler: function(A){ var f = [[{ b: String(-A.b) }, 'Vorzeichen']];
          if (!gl(A.c / A.a, A.b) && !gl(A.c / A.a, -A.b)) f.push([{ b: String(A.c / A.a) }, 'Exponent']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.b, A.b)) return null;
          if (gl(e.b, -A.b)) return 'Vorzeichen: Eine Basis ' + (A.c < 1 ? 'kleiner' : 'grösser') + ' als 1 braucht einen ' + (A.c < 1 ? 'negativen' : 'positiven') + ' Exponenten \\(b\\).';
          if (gl(e.b, A.c / A.a)) return 'Nicht teilen: Gesucht ist der Exponent \\(b\\) mit \\(' + A.a + '^{b} = ' + zT(A.c) + '\\).';
          return 'Schreib die Basis als Potenz von \\(' + A.a + '\\): \\(' + zT(A.c) + ' = ' + A.a + '^{b}\\).'; },
        loesung: function(A){ return zT(A.c) + ' = ' + A.a + '^{' + zT(A.b) + '} \\Rightarrow b = ' + zT(A.b); } },

      'e-form': { felder: ['c'], muster: 'Basis c = {c}',
        schl: function(A){ return 'e|' + A.c; },
        eingabe: function(A){ return { c: String(A.c) }; },
        neu: function(){ var a = zufall([2, 3, 4, 5, 7, 10]), minus = Math.random() < 0.4;
          return { a: a, minus: minus, c: minus ? 1 / a : a,
            text: 'Schreib \\(y = e^{' + (minus ? '-' : '') + '(\\ln ' + a + ')\\,x}\\) in der Form \\(y = c^x\\). Wie gross ist \\(c\\)? (Bruch oder Dezimalzahl)' }; },
        fehler: function(A){ return [[{ c: String(A.minus ? A.a : 1 / A.a) }, 'Minus'], [{ c: String(Math.E) }, 'Basis']]; },
        pruefen: function(A, e){
          if (gl(e.c, A.c)) return null;
          if (gl(e.c, A.minus ? A.a : 1 / A.a)) return A.minus ? 'Das Minus im Exponenten heisst Kehrwert: \\(e^{-(\\ln ' + A.a + ')x} = \\left(\\tfrac{1}{' + A.a + '}\\right)^x\\).' : 'Kein Minus im Exponenten — also kein Kehrwert.';
          if (Math.abs(e.c - Math.E) < 0.01) return 'Die Basis \\(e\\) steckt schon im \\(\\ln\\): \\(e^{\\ln ' + A.a + '} = ' + A.a + '\\).';
          return 'Nutze \\(e^{\\ln a} = a\\): \\(e^{(\\ln ' + A.a + ')\\,x} = \\left(e^{\\ln ' + A.a + '}\\right)^{x}\\).'; },
        loesung: function(A){ return 'e^{' + (A.minus ? '-' : '') + '(\\ln ' + A.a + ')x} = \\left(e^{\\ln ' + A.a + '}\\right)^{' + (A.minus ? '-' : '') + 'x} = ' + basT(A.c) + '^{x}'; } },

      'wachstum-zerfall': { felder: ['art'], muster: 'Das ist ein {art:Wachstum|Zerfall}',
        eingabe: function(A){ return { art: A.art }; },
        neu: function(){ var f = zufall([
            ['e^{0.3t}', 'Wachstum'], ['e^{-0.2t}', 'Zerfall'], ['e^{-t}', 'Zerfall'], ['2^{-t}', 'Zerfall'],
            ['\\left(\\tfrac13\\right)^{t}', 'Zerfall'], ['\\left(\\tfrac12\\right)^{-t}', 'Wachstum'], ['0.8^{t}', 'Zerfall'],
            ['1.05^{t}', 'Wachstum'], ['0.9^{-t}', 'Wachstum'], ['e^{0.01t}', 'Wachstum'], ['3^{-0.5t}', 'Zerfall'], ['e^{\\ln 2 \\cdot t}', 'Wachstum']]);
          var n0 = zufall([5, 20, 100, 250]);
          return { f: f[0], art: f[1], text: 'Beschreibt \\(N(t) = ' + n0 + ' \\cdot ' + f[0] + '\\) ein Wachstum oder einen Zerfall?' }; },
        fehler: function(A){ return [[{ art: A.art === 'Wachstum' ? 'Zerfall' : 'Wachstum' }, 'Exponent']]; },
        pruefen: function(A, e){
          if (e.art === A.art) return null;
          return 'Schreib es als \\(a^t\\) oder \\(e^{bt}\\): Basis grösser als 1 bzw. \\(b \\gt 0\\) heisst Wachstum. Ein Minus im Exponenten kehrt das um.'; },
        loesung: function(A){ return A.f + ':\\ \\text{' + A.art + '}'; } },

      /* ── Kapitel 4: Sättigung ────────────────────────────────── */
      'saettigung-lesen': { felder: ['A', 'S'], muster: 'Startwert A = {A}   Sättigungswert S = {S}',
        eingabe: function(A){ return { A: String(A.A), S: String(A.S) }; },
        neu: function(){ var S = zufall([20, 30, 50, 60, 80, 100]), D = zufall([10, 20, 30, 40, 50]) * zufall([1, -1]), k = zufall([0.1, 0.2, 0.3, 0.5]);
          if (S - D < 0) D = -D;
          return { S: S, A: S - D, D: D,
            text: 'Gegeben \\(f(t) = ' + S + (D > 0 ? ' - ' : ' + ') + Math.abs(D) + '\\,e^{-' + k + 't}\\). Gib Startwert und Sättigungswert an.' }; },
        fehler: function(A){ return [[{ A: String(Math.abs(A.D)), S: String(A.S) }, 'f(0)'], [{ A: String(A.S), S: String(A.A) }, 'Vertauscht']]
          .filter(function(p){ return !(gl(+p[0].A, A.A) && gl(+p[0].S, A.S)); }); },
        pruefen: function(A, e){
          if (gl(e.A, A.A) && gl(e.S, A.S)) return null;
          if (gl(e.A, A.S) && gl(e.S, A.A)) return 'Vertauscht: Der Sättigungswert ist der Summand allein — dahin strebt \\(f\\), wenn \\(e^{-kt}\\) gegen 0 geht.';
          var r = [];
          if (!gl(e.A, A.A)) r.push('Startwert: Setz \\(t = 0\\) ein, \\(e^{0} = 1\\): \\(f(0) = ' + A.S + (A.D > 0 ? ' - ' : ' + ') + Math.abs(A.D) + '\\).');
          if (!gl(e.S, A.S)) r.push('Sättigungswert: Für grosse \\(t\\) fällt der zweite Summand weg.');
          return r.join(' '); },
        loesung: function(A){ return 'A = f(0) = ' + A.A + ',\\ S = ' + A.S; } },

      'saettigung-wert': { felder: ['y'], muster: 'f(t₁) = {y}',
        eingabe: function(A){ return { y: String(A.y) }; },
        // Rückstand durch 8 teilbar, damit drei Halbierungen ganze Zahlen geben; Startwert ≥ 0.
        neu: function(){ var S = zufall([20, 40, 60, 100]), D = zufall([16, 32, 40, 48, 80]) * zufall([1, -1]),
            T = zufall([2, 5, 10]), j = zufall([1, 2, 3]);
          if (S - D < 0) D = -D;
          var A = S - D;
          return { S: S, A: A, T: T, j: j, y: S - (S - A) / pot(2, j),
            text: 'Ein Vorgang startet bei ' + A + ' und strebt gegen ' + S + '; der Rückstand zum Sättigungswert halbiert sich alle ' + T + ' Minuten. Welchen Wert hat er nach ' + j * T + ' Minuten?' }; },
        fehler: function(A){ var f = [], halbW = A.A / pot(2, A.j);
          if (!gl(halbW, A.y)) f.push([{ y: String(halbW) }, 'Rückstand']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, A.A / pot(2, A.j))) return 'Halbiert wird der Rückstand \\(' + Math.abs(A.S - A.A) + '\\), nicht der Wert selbst. Danach zum Sättigungswert zurückrechnen.';
          return 'Rückstand am Anfang: \\(|' + A.S + ' - ' + A.A + '| = ' + Math.abs(A.S - A.A) + '\\). Nach ' + A.j + ' Halbierungen: \\(' + Math.abs(A.S - A.A) / pot(2, A.j) + '\\). Dann vom Sättigungswert aus.'; },
        loesung: function(A){ return A.S + ' - (' + A.S + ' - ' + A.A + ') \\cdot \\left(\\tfrac12\\right)^{' + A.j + '} = ' + A.y; } },

      'saettigung-art': { felder: ['v'], muster: 'Die Kurve {v:steigt gegen S|fällt gegen S|bleibt konstant}',
        eingabe: function(A){ return { v: A.v }; },
        neu: function(){ var S = zufall([20, 25, 40, 100]), A = zufall([0, 15, 30, 60, 90]);
          if (A === S) A = S + 10;
          var D = S - A;
          return { S: S, A: A, v: A < S ? 'steigt gegen S' : 'fällt gegen S',
            text: '\\(f(t) = ' + S + (D > 0 ? ' - ' : ' + ') + Math.abs(D) + '\\,e^{-0.4t}\\). Steigt oder fällt die Kurve?' }; },
        fehler: function(A){ return [[{ v: A.v === 'steigt gegen S' ? 'fällt gegen S' : 'steigt gegen S' }, 'Startwert']]; },
        pruefen: function(A, e){
          if (e.v === A.v) return null;
          return 'Vergleich den Startwert \\(f(0) = ' + A.A + '\\) mit dem Sättigungswert \\(' + A.S + '\\).'; },
        loesung: function(A){ return 'f(0) = ' + A.A + (A.A < A.S ? ' \\lt ' : ' \\gt ') + A.S + ':\\ \\text{' + A.v + '}'; } },

      /* ── Kapitel 5: die Logarithmusfunktion ──────────────────── */
      'log-wert': { felder: ['y'], muster: 'Logarithmus = {y}',
        schl: function(A){ return 'l|' + A.a + '|' + A.x; },
        eingabe: function(A){ return { y: String(A.n) }; },
        neu: function(){ var a = zufall([2, 3, 4, 5, 10]), n = zufall([-3, -2, -1, 0, 1, 2, 3, 4]);
          if (a === 10 && n > 3) n = 3; if (a >= 4 && n > 3) n = 3;
          var x = pot(a, n);
          return { a: a, n: n, x: x,
            text: 'Berechne ohne Taschenrechner: \\(' + (a === 10 ? '\\lg' : '\\log_{' + a + '}') + ' ' + zT(x) + '\\).' }; },
        fehler: function(A){ var f = [];
          if (A.n !== 0) f.push([{ y: String(-A.n) }, 'Vorzeichen']);
          if (A.x > 1 && !gl(A.x / A.a, A.n)) f.push([{ y: String(A.x / A.a) }, 'Exponent']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.n)) return null;
          if (A.n === 0) return 'Jede Basis hoch 0 ist 1 — darum ist der Logarithmus von 1 immer 0.';
          if (gl(e.y, -A.n)) return 'Vorzeichen: ' + (A.x < 1 ? 'Zahlen zwischen 0 und 1 haben einen negativen Logarithmus (Basis grösser als 1).' : 'Zahlen grösser als 1 haben einen positiven Logarithmus.');
          if (gl(e.y, A.x / A.a)) return 'Der Logarithmus ist ein Exponent, kein Quotient: \\(' + A.a + '\\) hoch wie viel ergibt \\(' + zT(A.x) + '\\)?';
          return 'Frag dich: \\(' + A.a + '\\) hoch wie viel ergibt \\(' + zT(A.x) + '\\)?'; },
        loesung: function(A){ return A.a + '^{' + tz(A.n) + '} = ' + zT(A.x) + ' \\Rightarrow ' + (A.a === 10 ? '\\lg' : '\\log_{' + A.a + '}') + ' ' + zT(A.x) + ' = ' + tz(A.n); } },

      'umkehr-exp': { felder: ['u', 'x0'], muster: 'f⁻¹(x) = logₐ(x + {u}),   Nullstelle von f⁻¹: x₀ = {x0}',
        schl: function(A){ return 'u|' + A.a + '|' + A.v; },
        eingabe: function(A){ return { u: String(-A.v), x0: String(1 + A.v) }; },
        neu: function(){ var a = zufall([2, 3, 5, 10]), v = zufall([-4, -3, -2, -1, 1, 2, 3, 4]);
          return { a: a, v: v,
            text: 'Bestimme die Umkehrfunktion von \\(f(x) = ' + a + '^{x} ' + (v > 0 ? '+ ' + v : '- ' + (-v)) + '\\) als \\(f^{-1}(x) = \\log_{' + a + '}(x + u)\\) und ihre Nullstelle.' }; },
        fehler: function(A){ return [[{ u: String(A.v), x0: String(1 + A.v) }, 'Vorzeichen'], [{ u: String(-A.v), x0: String(A.v) }, 'Nullstelle']]; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.u, -A.v) && gl(e.x0, 1 + A.v)) return null;
          if (!gl(e.u, -A.v)) r.push(gl(e.u, A.v) ? 'Vorzeichen: Aus \\(y = ' + A.a + '^x ' + (A.v > 0 ? '+ ' + A.v : '- ' + (-A.v)) + '\\) wird \\(' + A.a + '^x = y ' + (A.v > 0 ? '- ' + A.v : '+ ' + (-A.v)) + '\\).'
                                             : 'Erst nach \\(' + A.a + '^x\\) auflösen, dann logarithmieren, dann \\(x\\) und \\(y\\) tauschen.');
          if (!gl(e.x0, 1 + A.v)) r.push('Nullstelle von \\(f^{-1}\\): \\(\\log_{' + A.a + '}(x + u) = 0\\) heisst \\(x + u = 1\\).');
          return r.join(' '); },
        loesung: function(A){ return 'f^{-1}(x) = \\log_{' + A.a + '}(x ' + (A.v > 0 ? '- ' + A.v : '+ ' + (-A.v)) + '),\\ x_0 = ' + tz(1 + A.v); } },

      'exp-gleichung': { felder: ['t'], muster: 't = {t}',
        schl: function(A){ return 'q|' + A.c + '|' + A.a + '|' + A.N; },
        eingabe: function(A){ return { t: String(A.t) }; },
        neu: function(){ var c = zufall([2, 3, 4, 5]), a = zufall([2, 3]), t = a === 2 ? zufall([2, 3, 4, 5, 6]) : zufall([2, 3, 4]);
          return { c: c, a: a, t: t, N: c * pot(a, t),
            text: 'Löse ohne Taschenrechner: \\(' + c + ' \\cdot ' + a + '^{t} = ' + c * pot(a, t) + '\\).' }; },
        fehler: function(A){ var f = [], q = A.N / A.c / A.a;
          if (!gl(q, A.t)) f.push([{ t: String(q) }, 'Basis']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.t, A.t)) return null;
          if (gl(e.t, A.N / A.c / A.a)) return 'Nicht durch die Basis teilen: Erst \\(' + A.a + '^{t} = ' + A.N / A.c + '\\), dann fragen: \\(' + A.a + '\\) hoch wie viel?';
          return 'Erst durch \\(' + A.c + '\\) teilen, dann logarithmieren: \\(t = \\log_{' + A.a + '} ' + A.N / A.c + '\\).'; },
        loesung: function(A){ return A.a + '^{t} = ' + A.N / A.c + ' \\Rightarrow t = \\log_{' + A.a + '} ' + A.N / A.c + ' = ' + A.t; } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie'), bild = box.querySelector('.ue-bild');
      function neu(){
        // Trifft der Wurf eine Aufgabe, die das Leitprogramm an fester Stelle stellt, wird neu
        // gewürfelt (SPERRE oben). 40 Versuche reichen weit; danach gilt der letzte Wurf.
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="decimal" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        if (bild){
          while (bild.firstChild) bild.removeChild(bild.firstChild);
          bild.setAttribute('viewBox', '0 0 170 170');
          if (T.zeichne) T.zeichne(bild, A);
        }
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;   // nach ✓ zählt erst die nächste Aufgabe
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){
          var r = lesen(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('select') ? 'Wähle aus und fülle alle offenen Felder aus.' : 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-3</code>, <code>0.5</code> oder <code>1/2</code>.'; return; }
        versuche++;
        var f = T.pruefen(A, e);
        if (f === null){
          serie = versuche === 1 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + (T.richtig ? ' ' + T.richtig(A) : '') + ' <button type="button" class="ue-weiter">Nächste</button>';
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

  /* ---------- Minigrafen: <svg class="mini" data-e="c,a,v" (y = c·aˣ + v) oder data-l="c,a,v"
       (y = c·logₐ x + v), mehrere mit «;» getrennt (die erste blau bzw. grün, weitere neutral),
       data-diagonale="1" (y = x), data-fenster, data-punkte, data-titel, data-xname, data-yname> ---------- */
  document.querySelectorAll('svg.mini[data-e], svg.mini[data-l]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-3,3,-1,5').split(',').map(Number);
    svg.setAttribute('viewBox', '0 0 150 150'); svg.setAttribute('role', 'img');
    var hy = fe[3] - fe[2], sy = hy > 40 ? 20 : hy > 20 ? 5 : hy > 12 ? 2 : 1;
    var K = Achsen(svg, { w: 150, h: 150, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, xm: [1], ym: [sy], sy: sy, pfeil: 6,
      xname: svg.dataset.xname, yname: svg.dataset.yname });
    if (svg.dataset.diagonale === '1') K.kurve(function(x){ return x; }, 'normal');
    (svg.dataset.e || '').split(';').filter(Boolean).forEach(function(s, i){
      var p = s.split(',').map(Number);
      K.kurve(function(x){ return p[0] * Math.pow(p[1], x) + p[2]; }, i ? 'kurve g2' : 'kurve');
    });
    (svg.dataset.l || '').split(';').filter(Boolean).forEach(function(s, i){
      var p = s.split(',').map(Number);
      K.kurve(function(x){ return x > 0 ? p[0] * Math.log(x) / Math.log(p[1]) + p[2] : NaN; }, i ? 'kurve g2' : 'kurve gruen', Math.max(fe[0], 0.0005), fe[1]);
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){
      var q = p.split(',').map(Number);
      K.punkt(q[0], q[1], 'p-pkt');
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
