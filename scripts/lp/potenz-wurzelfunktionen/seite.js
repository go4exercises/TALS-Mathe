<script>
/* Leitprogramm Potenz- und Wurzelfunktionen — Simulationen mit Aufgabenleiste, Übungen
   mit Rückmeldung, Minigrafen. Notation wie auf den Themenseiten 3.2a und 3.2b:
   f(x) = a·xⁿ mit n ∈ ℤ∖{0}, Wurzelfunktion f(x) = ⁿ√x = x^(1/n), verschoben
   a·(x−u)ⁿ + v bzw. a·ⁿ√(x−u) + v.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = die Potenzkurve und ihr Faktor a · orange = der Exponent n · grün = Wurzelkurve,
   Umkehrfunktion und Startpunkt · rot = Gegenbeispiel, Polstelle, verbotener Bereich ·
   Tinte = neutral (gemeinsame Punkte, Asymptoten, Bezugskurve, Spiegelachse y = x).
   Zahlen mit Dezimalpunkt und echtem Minus. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function z(n){ var r = Math.round(n * 100) / 100; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }

  /* ---------- Koordinatensystem (wie im Leitprogramm Quadratische Funktionen) ---------- */
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
      /* Streckenzug; wo f keinen Wert hat (Pol, verbotener Radikand), bricht er ab und
         beginnt danach neu — genau so entstehen die zwei Äste einer Hyperbel. */
      kurve: function(f, cls, a, b){
        var d = '', an = false, A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 300; k++){
          var x = A + (B - A) * k / 300, y = f(x);
          if (y == null || isNaN(y) || !isFinite(y)){ an = false; continue; }
          y = Math.max(y0 - 3 * (y1 - y0), Math.min(y1 + 3 * (y1 - y0), y));
          d += (an ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); an = true;
        }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      /* Dieselbe Kurve an y = x gespiegelt: aus (x | y) wird (y | x). Das ist der Graph
         der Umkehrfunktion — und bei geradem Exponenten ohne Einschränkung eben keiner. */
      gespiegelt: function(f, cls, a, b){
        var d = '', an = false, A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 300; k++){
          var x = A + (B - A) * k / 300, y = f(x);
          if (y == null || isNaN(y) || !isFinite(y)){ an = false; continue; }
          if (y < x0 || y > x1 || x < y0 || x > y1){ an = false; continue; }
          d += (an ? ' L' : 'M') + X(y).toFixed(1) + ' ' + Y(x).toFixed(1); an = true;
        }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      strecke: function(xa, ya, xb, yb, cls){
        return el(ebene, 'line', { x1: X(xa), y1: Y(ya), x2: X(xb), y2: Y(yb), 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      senkrecht: function(x, cls){ return el(ebene, 'line', { x1: X(x), y1: 0, x2: X(x), y2: H, 'class': cls }); },
      text: function(x, y, s, cls, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': 'p-text ' + cls }, s);
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      }
    };
  }
  // Beide Fenster sind quadratisch — nur dann sieht die Spiegelung an y = x wie eine aus.
  var FENSTER3 = { w: 300, h: 300, x0: -3, x1: 3, y0: -3, y1: 3, xm: [-2, -1, 1, 2], ym: [-2, -1, 1, 2] };
  var FENSTER5 = { w: 300, h: 300, x0: -5, x1: 5, y0: -5, y1: 5, xm: [-4, -2, 2, 4], ym: [-4, -2, 2, 4] };

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  function werte(r){ var w = {}; for (var k in r){ w[k] = +r[k].value; r[k].parentNode.querySelector('.sl-val').textContent = z(w[k]); } return w; }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }


  /* Ungerade Wurzel aus einer negativen Zahl: Math.pow(-8, 1/3) ist NaN, die dritte
     Wurzel aus −8 ist −2. Dieselbe Regel steckt in scripts/build-clips.py (BEWEGUNG_JS),
     damit Clip und Simulation dieselbe Kurve zeigen. */
  function pot(b, p){
    if (b >= 0 || Number.isInteger(p)) return Math.pow(b, p);
    var q = Math.round(1 / p);
    return (Math.abs(1 / p - q) < 1e-9 && q % 2 !== 0) ? -Math.pow(-b, p) : NaN;
  }
  /* y = a·(x−u)^p + v; null, wo es keinen Wert gibt (Pol, verbotener Radikand). */
  function kurveF(a, p, u, v){
    return function(x){ var y = a * pot(x - u, p) + v; return isFinite(y) ? y : NaN; };
  }
  /* «n» als Exponent oder als Wurzelexponent, in HTML mit den Farben des Leitprogramms. */
  function potText(a, n, u, v){
    var k = (u === 0 ? 'x' : '(x ' + (u > 0 ? '− ' : '+ ') + z(Math.abs(u)) + ')');
    var s = (a === 1 ? '' : a === -1 ? '−' : sp('tx-blau', z(a)) + '·') + k + '<sup>' + sp('tx-orange', z(n)) + '</sup>';
    if (v !== 0) s += (v > 0 ? ' + ' : ' − ') + z(Math.abs(v));
    return 'f(x) = ' + s;
  }
  function wurzelText(a, n, u, v){
    var k = (u === 0 ? 'x' : 'x ' + (u > 0 ? '− ' : '+ ') + z(Math.abs(u)));
    var s = (a === 1 ? '' : a === -1 ? '−' : sp('tx-blau', z(a)) + '·')
      + '<span class="wz">' + (n === 2 ? '' : '<sup>' + sp('tx-orange', z(n)) + '</sup>') + '√<span class="rad">' + k + '</span></span>';
    if (v !== 0) s += (v > 0 ? ' + ' : ' − ') + z(Math.abs(v));
    return 'f(x) = ' + s;
  }
  /* Ein Exponentenregler darf nie auf 0 stehenbleiben — x⁰ ist keine Potenzfunktion.
     Er springt über die Null hinweg, in die Richtung, aus der er kommt. */
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

  /* ---------- Kapitel 1: der Exponent formt den Graphen ----------
     Unterschied zur Animation «Potenzfunktionen erkunden» auf Themenseite 3.2a: dort
     läuft n nur über 1…5 und a ist fest. Hier kommt a dazu, die Bezugskurve y = x²
     liegt gestrichelt darunter, und die beiden Punkte, an denen sich alles entscheidet —
     (1 | a) und (−1 | ±a) — tragen ihre Werte mit. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER3), ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r);
                  return { a: w.a, n: w.n, bewegt: bewegt,
                           gerade: w.n % 2 === 0, sym: w.n % 2 === 0 ? 'achs' : 'punkt' }; },
                zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), a = w.a, n = w.n;
      K.leeren();
      K.kurve(kurveF(1, 2, 0, 0), 'normal hilfslinie');
      if (ziel) K.kurve(kurveF(ziel[0], ziel[1], 0, 0), 'zielkurve');
      K.kurve(kurveF(a, n, 0, 0), 'kurve');
      K.punkt(1, a, 'p-pkt', '(1 | ' + z(a) + ')', 8, -8);
      K.punkt(-1, a * (n % 2 === 0 ? 1 : -1), 'p-pkt', '(−1 | ' + z(a * (n % 2 === 0 ? 1 : -1)) + ')', -8, -8, 'end');
      rolle(fig, 'formel').innerHTML = potText(a, n, 0, 0) + ' &nbsp;·&nbsp; '
        + (a === 0 ? 'Nullfunktion' : n % 2 === 0 ? 'gerade Funktion, achsensymmetrisch zur <i>y</i>-Achse'
                                                  : 'ungerade Funktion, punktsymmetrisch zum Ursprung');
      pruefen();
    }
    function bau(a, n, tex){ return { text: 'Bau nach: \\(' + tex + '\\)', ok: function(s){ return s.a === a && s.n === n; } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an beiden Reglern. Welcher ändert die <em>Form</em>, welcher die <em>Höhe</em>?',
        ok: function(s){ return s.bewegt.a && s.bewegt.n; } },
      // Keine Aufgabe darf im Startzustand (a = 1, n = 2) schon erfuellt sein —
      // sonst steht das ✓ da, bevor jemand etwas getan hat (pruef-leiste.mjs).
      { text: 'Stell einen Graphen ein, der <b>achsensymmetrisch</b> zur \\(y\\)-Achse ist und einen Exponenten \\(n \\gt 2\\) hat.',
        ok: function(s){ return s.gerade && s.n > 2 && s.a !== 0; } },
      { text: 'Stell einen Graphen ein, der <b>punktsymmetrisch</b> zum Ursprung ist.',
        ok: function(s){ return !s.gerade && s.a !== 0; } },
      bau(2, 3, 'f(x) = 2x^3'), bau(-0.5, 4, 'f(x) = -0.5x^4'),
      { text: 'Stell \\(n = 6\\) ein und vergleich die Kurve mit der gestrichelten \\(y = x^2\\): Wo liegt sie flacher, wo steiler?',
        ok: function(s){ return s.n === 6; } },
      { text: 'Stell einen Graphen ein, für den \\(f(1) = -1.5\\) gilt.',
        ok: function(s){ return s.a === -1.5; } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [-2, 5]; }, ok: function(s){ return s.a === -2 && s.n === 5; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: negative Exponenten ----------
     Unterschied zur Animation «Hyperbeln n-ter Ordnung» auf Themenseite 3.2a: dort
     zeigt ein Knopf je eine fertige Ordnung. Hier läuft n stufenlos durch die negativen
     ganzen Zahlen, a kommt dazu, und die Simulation sagt laufend, wo die Äste liegen —
     daran hängt die Parität. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER3), pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r);
                  return { a: w.a, n: w.n, bewegt: bewegt, gerade: w.n % 2 === 0,
                           f2: kurveF(w.a, w.n, 0, 0)(2) }; },
                zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), a = w.a, n = w.n, f = kurveF(a, n, 0, 0);
      K.leeren();
      K.senkrecht(0, 'asym hilfslinie');
      K.strecke(-3, 0, 3, 0, 'asym hilfslinie');
      K.kurve(f, 'kurve', -3, -0.02); K.kurve(f, 'kurve', 0.02, 3);
      K.punkt(1, a, 'p-pkt', '(1 | ' + z(a) + ')', 8, -8);
      var lage = a === 0 ? '—' : n % 2 === 0 ? (a > 0 ? 'beide Äste oben' : 'beide Äste unten') : 'die Äste liegen diagonal';
      rolle(fig, 'formel').innerHTML = potText(a, n, 0, 0) + ' = ' + (a === 1 ? '' : z(a) + '·')
        + '<span class="br"><span>1</span><span>x<sup>' + z(-n) + '</sup></span></span>'
        + ' &nbsp;·&nbsp; <b>' + lage + '</b> &nbsp;·&nbsp; D = ℝ∖{0}';
      pruefen();
    }
    function bau(a, n, tex){ return { text: 'Bau nach: \\(' + tex + '\\)', ok: function(s){ return s.a === a && s.n === n; } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(n\\). Was geschieht an der Stelle \\(x = 0\\), und was weit draussen?',
        ok: function(s){ return s.bewegt.n; } },
      // Startzustand ist a = 1, n = −1 (die Hyperbel 1/x) — keine Aufgabe darf ihn treffen.
      bau(1, -2, 'f(x) = \\dfrac{1}{x^2}'),
      { text: 'Stell eine Hyperbel ein, deren beide Äste <b>oben</b> liegen.',
        ok: function(s){ return s.gerade && s.a > 0; } },
      { text: 'Stell eine Hyperbel <b>dritter</b> Ordnung ein, deren Äste <b>diagonal</b> liegen (links unten, rechts oben).',
        ok: function(s){ return s.n === -3 && s.a > 0; } },
      { text: 'Stell eine Hyperbel ein, deren beide Äste <b>unten</b> liegen.',
        ok: function(s){ return s.gerade && s.a < 0; } },
      { text: 'Stell \\(f(x) = \\dfrac{2}{x}\\) ein und lies \\(f(2)\\) am Graphen ab.',
        ok: function(s){ return s.a === 2 && s.n === -1; } },
      { text: 'Stell eine Hyperbel ein, für die \\(f(1) = -2\\) gilt.',
        ok: function(s){ return s.a === -2; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: verschieben und strecken ----------
     Unterschied zur Animation «Transformationen» auf Themenseite 3.1: dort wird eine
     Parabel verschoben. Hier gilt dasselbe Schema für jeden ganzzahligen Exponenten,
     und bei negativem n wandern die Asymptoten sichtbar mit — das ist der Fall, den
     die Parabel nicht zeigt. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER5), ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    if (r.n) ohneNull(r.n);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r);
                  return { a: w.a, n: w.n, u: w.u, v: w.v, bewegt: bewegt,
                           hyperbel: w.n < 0, f0: kurveF(w.a, w.n, w.u, w.v)(0) }; },
                zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), a = w.a, n = w.n, u = w.u, v = w.v, f = kurveF(a, n, u, v);
      K.leeren();
      K.kurve(kurveF(a, n, 0, 0), 'normal hilfslinie');
      if (ziel) K.kurve(kurveF(ziel[0], ziel[1], ziel[2], ziel[3]), 'zielkurve');
      if (n < 0){
        K.senkrecht(u, 'asym'); K.strecke(-5, v, 5, v, 'asym');
        K.kurve(f, 'kurve', -5, u - 0.02); K.kurve(f, 'kurve', u + 0.02, 5);
        K.text(u + 0.25, 4.6, 'x = ' + z(u), 'p-m', 'start');
        K.text(4.8, v + 0.4, 'y = ' + z(v), 'p-m', 'end');
      } else {
        K.kurve(f, 'kurve');
        K.punkt(u, v, 'p-pkt', '(' + z(u) + ' | ' + z(v) + ')', 8, -8);
      }
      rolle(fig, 'formel').innerHTML = potText(a, n, u, v)
        + (n < 0 ? ' &nbsp;·&nbsp; Asymptoten <i>x</i> = ' + z(u) + ', <i>y</i> = ' + z(v)
                 : (u === 0 && v === 0) ? ' &nbsp;·&nbsp; nicht verschoben'
                 : ' &nbsp;·&nbsp; verschoben um (' + z(u) + ' | ' + z(v) + ')');
      pruefen();
    }
    function bau(a, n, u, v, tex){
      return { text: 'Bau nach: \\(' + tex + '\\)',
               ok: function(s){ return s.a === a && s.n === n && s.u === u && s.v === v; } };
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(u\\) und an \\(v\\). Welcher schiebt waagrecht, welcher senkrecht?',
        ok: function(s){ return s.bewegt.u && s.bewegt.v; } },
      bau(1, 3, 2, 0, 'f(x) = (x-2)^3'),
      bau(1, 3, 0, -2, 'f(x) = x^3 - 2'),
      { text: 'Stell eine Hyperbel mit der Polgeraden \\(x = -2\\) ein.',
        ok: function(s){ return s.hyperbel && s.u === -2; } },
      bau(1, -1, 2, 1, 'f(x) = \\dfrac{1}{x-2} + 1'),
      { text: 'Stell eine Kurve ein, deren Graph durch den Punkt \\((0 \\mid 0)\\) geht und <em>nicht</em> \\(f(x) = x^n\\) ist.',
        ok: function(s){ return Math.abs(s.f0) < 1e-9 && (s.u !== 0 || s.v !== 0); } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [-1, 2, 1, 3]; },
        ok: function(s){ return s.a === -1 && s.n === 2 && s.u === 1 && s.v === 3; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: umkehren heisst spiegeln ----------
     Das Herzstück des Teilgebiets: die einzige RLP-Kompetenz zu 3.2 verlangt die
     Wurzelfunktion ausdrücklich «als Umkehrfunktion der Potenzfunktion». Der Schalter
     «nur x ≥ 0» macht den Unterschied sichtbar: bei geradem n ist das Spiegelbild ohne
     ihn rot — über einem x lägen zwei Punkte, das ist kein Funktionsgraph. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER3), pruefen = function(){}, bewegt = {};
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    if (schalter) schalter.addEventListener('change', function(){ bewegt.ein = true; zeichnen(); });
    function istFunktion(n, ein){ return n % 2 !== 0 || ein; }
    var sim = { zustand: function(){ var w = werte(r), ein = !!(schalter && schalter.checked);
                  return { n: w.n, ein: ein, bewegt: bewegt, gerade: w.n % 2 === 0,
                           funktion: istFunktion(w.n, ein) }; },
                zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), n = w.n, ein = !!(schalter && schalter.checked), f = kurveF(1, n, 0, 0);
      var von = ein ? 0 : -3, gut = istFunktion(n, ein);
      K.leeren();
      K.kurve(function(x){ return x; }, 'normal');
      K.kurve(f, 'kurve', von, 3);
      // Spiegelbild an y = x: Punkt für Punkt (x | y) ↦ (y | x).
      K.gespiegelt(f, gut ? 'umkehr' : 'umkehr falsch', von, 3);
      K.punkt(1, 1, 'p-pkt');
      rolle(fig, 'formel').innerHTML = 'f(x) = x<sup>' + sp('tx-orange', z(n)) + '</sup>'
        + (ein ? ', &nbsp;x ≥ 0' : '') + ' &nbsp;·&nbsp; '
        + (gut ? 'Spiegelbild ist ein Funktionsgraph: f<sup>−1</sup>(x) = '
                 + '<span class="wz">' + (n === 2 ? '' : '<sup>' + sp('tx-orange', z(n)) + '</sup>') + '√<span class="rad">x</span></span>'
               : '<b class="rot">Spiegelbild ist kein Funktionsgraph</b> — über einem x lägen zwei Punkte');
      fig.classList.toggle('treffer', gut);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(n\\) und setz den Haken «nur \\(x \\geq 0\\)» einmal und wieder weg.',
        ok: function(s){ return s.bewegt.n && s.bewegt.ein; } },
      { text: 'Stell einen Exponenten ein, bei dem das Spiegelbild <b>ohne</b> Einschränkung schon ein Funktionsgraph ist.',
        ok: function(s){ return !s.gerade && !s.ein; } },
      { text: 'Stell \\(n = 4\\) ein. Was zeigt die Simulation, solange der Haken fehlt?',
        ok: function(s){ return s.n === 4 && !s.ein; } },
      { text: 'Setz jetzt bei \\(n = 4\\) den Haken. Wie heisst die Umkehrfunktion?',
        ok: function(s){ return s.n === 4 && s.ein; } },
      { text: 'Welche <b>zwei</b> Punkte liegen bei jedem \\(n\\) auf beiden Kurven? Stell \\(n = 5\\) ein und such sie.',
        ok: function(s){ return s.n === 5; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Wurzelfunktionen nutzen ----------
     Dieselben vier Parameter wie in Kapitel 3, nur steht n jetzt im Wurzelexponenten.
     Die Simulation schreibt die Definitionsmenge laufend mit — bei geradem n beginnt
     sie beim Startpunkt, bei ungeradem ist sie ganz ℝ und es gibt keinen Startpunkt. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER5), ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function nullstelle(a, n, u, v){            // a·ⁿ√(x−u) + v = 0
      if (a === 0) return null;
      var w = -v / a;                           // ⁿ√(x − u) = w
      if (n % 2 === 0 && w < 0) return null;    // eine gerade Wurzel wird nie negativ
      return u + Math.pow(w, n);                // x = u + wⁿ
    }
    var sim = { zustand: function(){ var w = werte(r);
                  return { a: w.a, n: w.n, u: w.u, v: w.v, bewegt: bewegt, gerade: w.n % 2 === 0,
                           x0: nullstelle(w.a, w.n, w.u, w.v) }; },
                zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), a = w.a, n = w.n, u = w.u, v = w.v, f = kurveF(a, 1 / n, u, v);
      K.leeren();
      if (ziel) K.kurve(kurveF(ziel[0], 1 / ziel[1], ziel[2], ziel[3]), 'zielkurve');
      K.kurve(f, 'kurve gruen', n % 2 === 0 ? u : -5, 5);
      if (n % 2 === 0) K.punkt(u, v, 'p-null', '(' + z(u) + ' | ' + z(v) + ')', 8, 14);
      var x0 = nullstelle(a, n, u, v);
      // Faellt die Nullstelle mit dem Startpunkt zusammen, traegt dieser schon seine
      // Beschriftung — zwei Schilder uebereinander waeren nur unleserlich.
      if (x0 !== null && Math.abs(x0) <= 5 && !(n % 2 === 0 && Math.abs(x0 - u) < 1e-9))
        K.punkt(x0, 0, 'p-pkt', 'x₀ ' + (Math.abs(x0 - Math.round(x0 * 100) / 100) > 1e-12 ? '≈ ' : '= ')
                + z(x0), 8, -8);
      rolle(fig, 'formel').innerHTML = wurzelText(a, n, u, v) + ' &nbsp;·&nbsp; '
        + (n % 2 === 0 ? 'Startpunkt (' + z(u) + ' | ' + z(v) + '), D = [' + z(u) + '; +∞['
                       : 'kein Startpunkt, D = ℝ');
      pruefen();
    }
    function bau(a, n, u, v, tex){
      return { text: 'Bau nach: \\(' + tex + '\\)',
               ok: function(s){ return s.a === a && s.n === n && s.u === u && s.v === v; } };
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(n\\). Wann beginnt die Kurve an einem Startpunkt, wann läuft sie nach links weiter?',
        ok: function(s){ return s.bewegt.n; } },
      bau(1, 2, 3, 0, 'f(x) = \\sqrt{x-3}'),
      { text: 'Stell eine Wurzelfunktion mit \\(D = [-2;\\, +\\infty[\\) ein.',
        ok: function(s){ return s.gerade && s.u === -2; } },
      { text: 'Stell eine Wurzelfunktion mit \\(D = \\mathbb{R}\\) ein.',
        ok: function(s){ return !s.gerade; } },
      bau(2, 2, -1, -4, 'f(x) = 2\\sqrt{x+1} - 4'),
      { text: 'Stell eine Wurzelfunktion ein, deren Nullstelle bei \\(x_0 = 4\\) liegt.',
        ok: function(s){ return s.x0 !== null && Math.abs(s.x0 - 4) < 1e-9; } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [-1, 3, 2, 1]; },
        ok: function(s){ return s.a === -1 && s.n === 3 && s.u === 2 && s.v === 1; } }
    ], sim);
    zeichnen();
  })();
  /* ---------- Hilfslinien-Schalter: blendet alles mit Klasse .hilfslinie in seiner Animation aus ---------- */
  document.querySelectorAll('.hilfs-schalter input').forEach(function(hs){
    var fig = hs.closest('figure');
    hs.addEventListener('change', function(){ fig.classList.toggle('ohne-hilfslinien', !hs.checked); });
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function bereich(a, b, ohne){ var r = []; for (var i = a; i <= b; i++) if (!ohne || ohne.indexOf(i) < 0) r.push(i); return r; }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    function kx(m){ return m === 1 ? 'x' : m === -1 ? '-x' : tz(m) + 'x'; }
    function plus(v){ return v === 0 ? '' : (v > 0 ? ' + ' + v : ' - ' + (-v)); }
    /* Term m·x + b in LaTeX; m = 0 gibt die konstante Funktion. */
    function lin(m, b){ return m === 0 ? tz(b) : kx(m) + plus(b); }
    function pkt(x, y){ return '(' + tz(x) + ' \\mid ' + tz(y) + ')'; }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    /* Potenzterm a·(x−u)^n + v in LaTeX. */
    function kl(u){ return u === 0 ? 'x' : '(x ' + (u > 0 ? '- ' + u : '+ ' + (-u)) + ')'; }
    function vor(a){ return a === 1 ? '' : a === -1 ? '-' : tz(a); }
    function potT(a, n, u, v){ return vor(a) + kl(u) + '^{' + tz(n) + '}' + plus(v); }
    function wzT(a, n, u, v){
      var w = (n === 2 ? '\\sqrt{' : '\\sqrt[' + n + ']{') + (u === 0 ? 'x' : 'x ' + (u > 0 ? '- ' + u : '+ ' + (-u))) + '}';
      return vor(a) + w + plus(v);
    }
    /* Exponenten und Faktoren, mit denen die Aufgaben rechnen. */
    var EXP_P = [2, 3, 4, 5], EXP_N = [-1, -2, -3], FAK = [-3, -2, -1, 1, 2, 3];
    /* Funktionen, nach denen das Leitprogramm an fester Stelle fragt — eine Zufalls-
       übung darf keine davon treffen, sonst steht ihre Lösung schon irgendwo
       (HOWTO §15). Je Eintrag [a, n, u, v]; n ist der Exponent bzw. Wurzelexponent.
       Reihenfolge: Clips · Simulationen · Aufgaben der Kapitel · Vortest · Gesamttest. */
    var FEST = [
      [1, 2, 0, 0], [1, 3, 0, 0], [1, 4, 0, 0], [1, 5, 0, 0], [1, 6, 0, 0],
      [2, 3, 0, 0], [-0.5, 4, 0, 0], [-1.5, 3, 0, 0], [-2, 5, 0, 0], [0.5, 3, 0, 0],
      [1, -1, 0, 0], [1, -2, 0, 0], [1, -3, 0, 0], [1, -4, 0, 0], [2, -1, 0, 0],
      [1, 3, 2, 0], [1, 3, 0, -2], [1, 3, 0, 3], [1, -1, 2, -1], [1, -1, 2, 1],
      [1, -1, -1, 2], [1, 4, 3, -16], [-1, 2, 1, 3], [1, 3, 0, 1], [1, 3, 0, -1],
      [1, 2, 3, 0], [2, 2, -1, -4], [1, 3, -2, 0], [1, 4, 1, -2], [-1, 3, 2, 1],
      [1, 2, -1, 0], [1, 3, 3, 0], [2, 3, -1, -4], [1, 2, 0, -4], [3, 2, 0, 0],
      [1, -2, 1, -2], [-2, 2, 0, 3], [1, 5, -1, 0], [0.5, 4, 0, -2], [-1, 4, 2, 1],
      // Gesamttest G1…G8 (downloads/leitprogramme/potenz-wurzelfunktionen/gesamttest.tex)
      [3, 4, 0, 0], [0.5, 4, 0, 0], [-2, -2, 0, 0], [1, 4, 1, -16], [2, 2, -3, -4],
      // Aufgaben der Kapitel und Vortest, die eine feste Funktion nennen
      [-1, 3, 0, 0], [2, 2, 0, 0], [-2, 3, 0, 0], [3, 6, 0, 0], [-1, 7, 0, 0],
      [4, -1, 0, 0], [3, -2, 0, 0], [1, -1, 0, 0], [-1, -1, 0, 0], [-1, -2, 0, 0],
      [1, 3, -1, -2], [2, -1, 3, 1], [1, 4, -2, -81], [1, 3, 1, 8], [1, -1, -2, 3],
      [1, 5, 0, -3], [1, 4, 0, 0], [1, 6, 0, 0], [3, 2, -1, -6], [1, 2, 2, -1],
      [1, 2, 5, 0], [1, 3, -1, 0], [1, 4, -2, -1], [1, 2, 0, 0]
    ];
    function fest(a, n, u, v){
      return FEST.some(function(p){ return gl(p[0], a) && p[1] === n && gl(p[2], u || 0) && gl(p[3], v || 0); });
    }
    /* Typen, deren Aufgabe gar nicht an der Funktion haengt, sondern nur an der Parität
       des Exponenten: Dort sperrte FEST fast den ganzen Wurfraum. «Einschränken nötig?»
       zeigte so in 99.9 % der Fälle x⁷ — und hatte damit immer dieselbe Antwort. */
    var OHNE_FEST = { einschraenken: 1, symmetrie: 1, aeste: 1, vergleich: 1 };

    var TYPEN = {
      /* ── Kapitel 1: der Exponent formt den Graphen ───────────── */
      'potenz-wert': { felder: ['y'], muster: 'f(x₁) = {y}',
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){ var a = zufall(FAK), n = zufall(EXP_P), x = zufall([-2, -1, 1, 2, 3].filter(function(q){ return Math.abs(Math.pow(q, n)) <= 81; }));
          return { a: a, n: n, u: 0, v: 0, x: x, y: a * Math.pow(x, n),
            text: 'Berechne \\(f(' + tz(x) + ')\\) für \\(f(x) = ' + potT(a, n, 0, 0) + '\\).' }; },
        fehler: function(A){ var f = [[{ y: String(-A.y) }, 'Vorzeichen']], m = A.a * A.n * A.x;
          // Die Probe «Exponent als Faktor» faellt manchmal mit −y zusammen; dann
          // greift die Vorzeichen-Diagnose, und die Probe waere nicht unterscheidbar.
          if (!gl(m, A.y) && !gl(m, -A.y)) f.push([{ y: String(m) }, 'ist kein Faktor']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, -A.y)) return A.x < 0 && A.n % 2 === 0
            ? 'Vorzeichen: Eine negative Zahl hoch einen <em>geraden</em> Exponenten wird positiv.'
            : 'Vorzeichen: Rechne \\((' + tz(A.x) + ')^{' + A.n + '} = ' + tz(Math.pow(A.x, A.n)) + '\\), dann mal \\(' + tz(A.a) + '\\).';
          if (gl(e.y, A.a * A.n * A.x)) return 'Der Exponent ist kein Faktor: \\(x^{' + A.n + '}\\) heisst \\(' + A.n + '\\)-mal \\(x\\) <em>multipliziert</em>.';
          if (gl(e.y, Math.pow(A.a * A.x, A.n))) return 'Zuerst die Potenz, dann mal \\(' + tz(A.a) + '\\) — das \\(a\\) steht ausserhalb der Potenz.';
          return 'Zuerst \\((' + tz(A.x) + ')^{' + A.n + '} = ' + tz(Math.pow(A.x, A.n)) + '\\), dann mal \\(' + tz(A.a) + '\\).'; },
        loesung: function(A){ return 'f(' + tz(A.x) + ') = ' + tz(A.a) + ' \\cdot (' + tz(A.x) + ')^{' + A.n + '} = ' + tz(A.y); } },

      'symmetrie': { felder: ['sym'], muster: 'Der Graph ist {sym:achsensymmetrisch zur y-Achse|punktsymmetrisch zum Ursprung}',
        eingabe: function(A){ return { sym: A.n % 2 === 0 ? 'achsensymmetrisch zur y-Achse' : 'punktsymmetrisch zum Ursprung' }; },
        neu: function(){ var a = zufall(FAK), n = zufall([2, 3, 4, 5, 6, 7]);
          return { a: a, n: n, u: 0, v: 0, gerade: n % 2 === 0,
            text: 'Welche Symmetrie hat der Graph von \\(f(x) = ' + potT(a, n, 0, 0) + '\\)?' }; },
        fehler: function(A){ return [[{ sym: A.gerade ? 'punktsymmetrisch zum Ursprung' : 'achsensymmetrisch zur y-Achse' }, 'Exponent']]; },
        pruefen: function(A, e){
          var richtig = A.gerade ? 'achsensymmetrisch zur y-Achse' : 'punktsymmetrisch zum Ursprung';
          if (e.sym === richtig) return null;
          return 'Der Exponent \\(' + A.n + '\\) ist ' + (A.gerade ? 'gerade' : 'ungerade')
            + '. Rechne \\(f(-x)\\) aus: ' + (A.gerade ? '\\(f(-x) = f(x)\\)' : '\\(f(-x) = -f(x)\\)') + '.'; },
        loesung: function(A){ return A.gerade ? 'f(-x) = f(x) \\text{ — achsensymmetrisch zur } y\\text{-Achse}'
                                              : 'f(-x) = -f(x) \\text{ — punktsymmetrisch zum Ursprung}'; } },

      'graf-potenz': { felder: ['a', 'n'], muster: 'f(x) = {a} · x^{n}', graf: 'potenz',
        neu: function(){ var a = zufall([-3, -2, -1, 1, 2, 3]), n = zufall([2, 3, 4, 5]);
          return { a: a, n: n, u: 0, v: 0,
            text: 'Gleichung der Kurve? (Der markierte Punkt liegt auf einem Gitterpunkt.)' }; },
        fehler: function(A){ var f = [[{ a: String(-A.a), n: String(A.n) }, 'Vorzeichen von']];
          f.push([{ a: String(A.a), n: String(A.n + 1) }, 'Symmetrie']);     // Parität gekippt
          return f; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.n, A.n)) return null;
          var r = [];
          if (!gl(e.n, A.n)){
            if (e.n % 2 !== A.n % 2) r.push('Symmetrie: Der Graph ist ' + (A.n % 2 === 0 ? 'achsensymmetrisch, der Exponent also gerade' : 'punktsymmetrisch, der Exponent also ungerade') + '.');
            else r.push('Der Exponent stimmt noch nicht: Vergleich die Kurve mit \\(y = x^2\\) — innen flacher heisst grösseres \\(n\\).');
          }
          if (!gl(e.a, A.a)) r.push('Vorzeichen von \\(a\\) und Wert bei \\(x = 1\\): Dort ist \\(f(1) = a\\).');
          return r.join(' '); },
        loesung: function(A){ return 'f(x) = ' + potT(A.a, A.n, 0, 0); } },

      /* ── Kapitel 2: negative Exponenten ──────────────────────── */
      'hyperbel-wert': { felder: ['y'], muster: 'f(x₁) = {y}',
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){ var a = zufall([-4, -2, -1, 1, 2, 4]), n = zufall(EXP_N), x = zufall([-2, -1, 1, 2]);
          return { a: a, n: n, u: 0, v: 0, x: x, y: a * Math.pow(x, n),
            text: 'Berechne \\(f(' + tz(x) + ')\\) für \\(f(x) = ' + potT(a, n, 0, 0) + '\\).' }; },
        fehler: function(A){ var f = [[{ y: String(-A.y) }, 'Vorzeichen']];
          if (!gl(A.a * Math.pow(A.x, -A.n), A.y)) f.push([{ y: String(A.a * Math.pow(A.x, -A.n)) }, 'Kehrwert']);
          return f.filter(function(p){ return !gl(+p[0].y, A.y); }); },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, A.a * Math.pow(A.x, -A.n))) return 'Der negative Exponent bedeutet den Kehrwert: \\(x^{' + A.n + '} = \\dfrac{1}{x^{' + (-A.n) + '}}\\).';
          if (gl(e.y, -A.y)) return 'Vorzeichen: \\((' + tz(A.x) + ')^{' + (-A.n) + '} = ' + tz(Math.pow(A.x, -A.n)) + '\\) — ein gerader Exponent macht positiv.';
          return 'Erst \\((' + tz(A.x) + ')^{' + (-A.n) + '} = ' + tz(Math.pow(A.x, -A.n)) + '\\), dann \\(' + tz(A.a) + '\\) durch diese Zahl.'; },
        loesung: function(A){ return 'f(' + tz(A.x) + ') = \\dfrac{' + tz(A.a) + '}{(' + tz(A.x) + ')^{' + (-A.n) + '}} = ' + tz(A.y); } },

      'aeste': { felder: ['lage'], muster: 'Die Äste liegen {lage:beide oben|beide unten|diagonal}',
        eingabe: function(A){ return { lage: A.lage }; },
        neu: function(){ var a = zufall([-3, -2, -1, 1, 2, 3]), n = zufall([-1, -2, -3, -4]);
          return { a: a, n: n, u: 0, v: 0, lage: n % 2 !== 0 ? 'diagonal' : (a > 0 ? 'beide oben' : 'beide unten'),
            text: 'Wo liegen die beiden Äste von \\(f(x) = ' + potT(a, n, 0, 0) + '\\)?' }; },
        fehler: function(A){ return [[{ lage: A.lage === 'diagonal' ? 'beide oben' : 'diagonal' }, 'Exponent']]; },
        pruefen: function(A, e){
          if (e.lage === A.lage) return null;
          if (A.lage === 'diagonal') return 'Der Exponent \\(' + A.n + '\\) ist ungerade — dann hat \\(f(-x)\\) das andere Vorzeichen als \\(f(x)\\).';
          if (e.lage === 'diagonal') return 'Der Exponent \\(' + A.n + '\\) ist gerade — dann haben \\(f(-x)\\) und \\(f(x)\\) dasselbe Vorzeichen.';
          return 'Der Exponent ist gerade, also entscheidet \\(a\\): Setz \\(x = 1\\) ein.'; },
        loesung: function(A){ return '\\text{' + A.lage + '}'; } },

      'def-hyperbel': { felder: ['u'], muster: 'D = ℝ ∖ { {u} }',
        eingabe: function(A){ return { u: String(A.u) }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2, 3]), n = zufall(EXP_N), u = zufall(bereich(-4, 4, [0]));
          return { a: a, n: n, u: u, v: 0,
            text: 'Welche Zahl fehlt in der Definitionsmenge von \\(f(x) = ' + potT(a, n, u, 0) + '\\)?' }; },
        fehler: function(A){ return [[{ u: String(-A.u) }, 'Vorzeichen'], [{ u: '0' }, 'verschoben']]
          .filter(function(p){ return !gl(+p[0].u, A.u); }); },
        pruefen: function(A, e){
          if (gl(e.u, A.u)) return null;
          if (gl(e.u, -A.u)) return 'Vorzeichen: Die Klammer wird null bei \\(x = ' + tz(A.u) + '\\), nicht bei \\(' + tz(-A.u) + '\\).';
          if (gl(e.u, 0)) return 'Die Kurve ist verschoben: Setz die Klammer null und löse nach \\(x\\) auf.';
          return 'Gesucht ist die Stelle, an der die Klammer null wird: \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = 0\\).'; },
        loesung: function(A){ return 'D = \\mathbb{R} \\setminus \\{' + tz(A.u) + '\\}'; } },

      /* ── Kapitel 3: verschieben und strecken ─────────────────── */
      'transformation-lesen': { felder: ['u', 'v'], muster: 'u = {u}   v = {v}',
        eingabe: function(A){ return { u: String(A.u), v: String(A.v) }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2]), n = zufall([2, 3, 4]),
            u = zufall(bereich(-4, 4, [0])), v = zufall(bereich(-4, 4, [0]));
          return { a: a, n: n, u: u, v: v,
            text: 'Um wie viel ist \\(f(x) = ' + potT(a, n, u, v) + '\\) gegenüber \\(' + vor(a) + 'x^{' + n + '}\\) verschoben?' }; },
        fehler: function(A){ return [[{ u: String(-A.u), v: String(A.v) }, 'In der Klammer'],
                                     [{ u: String(A.v), v: String(A.u) }, 'Vertauscht']]
          .filter(function(p){ return !(gl(+p[0].u, A.u) && gl(+p[0].v, A.v)); }); },
        pruefen: function(A, e){
          if (gl(e.u, A.u) && gl(e.v, A.v)) return null;
          if (gl(e.u, A.v) && gl(e.v, A.u)) return 'Vertauscht: \\(u\\) steht in der Klammer, \\(v\\) dahinter.';
          if (!gl(e.u, A.u) && gl(e.u, -A.u)) return 'In der Klammer kehrt sich das Vorzeichen um: \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + '\\) heisst \\(u = ' + tz(A.u) + '\\).';
          if (!gl(e.u, A.u)) return '\\(u\\) liest man in der Klammer ab — mit umgekehrtem Vorzeichen.';
          return '\\(v\\) steht hinter der Potenz und behält sein Vorzeichen.'; },
        loesung: function(A){ return 'u = ' + tz(A.u) + ',\\quad v = ' + tz(A.v); } },

      'asymptoten': { felder: ['xa', 'ya'], muster: 'x = {xa}   y = {ya}',
        eingabe: function(A){ return { xa: String(A.u), ya: String(A.v) }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2]), n = zufall([-1, -2]),
            u = zufall(bereich(-4, 4, [0])), v = zufall(bereich(-4, 4, [0]));
          return { a: a, n: n, u: u, v: v,
            text: 'Gib die beiden Asymptoten von \\(f(x) = ' + potT(a, n, u, v) + '\\) an.' }; },
        fehler: function(A){ return [[{ xa: String(-A.u), ya: String(A.v) }, 'In der Klammer'],
                                     [{ xa: String(A.v), ya: String(A.u) }, 'Vertauscht']]
          .filter(function(p){ return !(gl(+p[0].xa, A.u) && gl(+p[0].ya, A.v)); }); },
        pruefen: function(A, e){
          if (gl(e.xa, A.u) && gl(e.ya, A.v)) return null;
          if (gl(e.xa, A.v) && gl(e.ya, A.u)) return 'Vertauscht: Die Polgerade liegt bei \\(x = u\\), die waagrechte Asymptote bei \\(y = v\\).';
          if (!gl(e.xa, A.u)) return 'In der Klammer kehrt sich das Vorzeichen um: Die Klammer wird null bei \\(x = ' + tz(A.u) + '\\).';
          return 'Die waagrechte Asymptote liegt auf der Höhe, die hinter der Potenz steht: \\(y = ' + tz(A.v) + '\\).'; },
        loesung: function(A){ return 'x = ' + tz(A.u) + ',\\quad y = ' + tz(A.v); } },

      'nullstelle-potenz': { felder: ['x1', 'x2'], muster: 'x₁ = {x1}   x₂ = {x2}',
        eingabe: function(A){ return { x1: String(A.x1), x2: String(A.x2) }; },
        neu: function(){ var n = zufall([2, 4]), u = zufall(bereich(-3, 3)), w = zufall([1, 2, 3]),
            v = -Math.pow(w, n);
          return { a: 1, n: n, u: u, v: v, w: w, x1: u - w, x2: u + w,
            text: 'Berechne die Nullstellen von \\(f(x) = ' + potT(1, n, u, v) + '\\).' }; },
        fehler: function(A){ return [[{ x1: String(A.x2), x2: String(A.x2) }, 'zwei Lösungen'],
                                     [{ x1: String(A.u - A.w * 2), x2: String(A.u + A.w * 2) }, 'Wurzel']]
          .filter(function(p){ return !(gl(+p[0].x1, A.x1) && gl(+p[0].x2, A.x2)); }); },
        pruefen: function(A, e){
          var kl2 = Math.min(e.x1, e.x2), gr = Math.max(e.x1, e.x2);
          if (gl(kl2, A.x1) && gl(gr, A.x2)) return null;
          if (gl(e.x1, e.x2)) return 'Ein gerader Exponent gibt beim Wurzelziehen <em>zwei</em> Lösungen: \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = \\pm ' + A.w + '\\).';
          if (gl(kl2, A.u - A.w * 2) || gl(gr, A.u + A.w * 2)) return 'Die \\(' + A.n + '\\)-te Wurzel aus \\(' + (-A.v) + '\\) ist \\(' + A.w + '\\) — nachrechnen: \\(' + A.w + '^{' + A.n + '} = ' + (-A.v) + '\\).';
          return 'Setz \\(f(x) = 0\\): \\(' + kl(A.u) + '^{' + A.n + '} = ' + (-A.v) + '\\), also \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = \\pm ' + A.w + '\\).'; },
        loesung: function(A){ return 'x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = \\pm ' + A.w + ' \\Rightarrow x_1 = ' + tz(A.x1) + ',\\ x_2 = ' + tz(A.x2); } },

      /* ── Kapitel 4: umkehren ─────────────────────────────────── */
      'einschraenken': { felder: ['noetig'], muster: 'Einschränken auf x ≥ 0 {noetig:nötig|nicht nötig}',
        eingabe: function(A){ return { noetig: A.gerade ? 'nötig' : 'nicht nötig' }; },
        neu: function(){ var n = zufall([2, 3, 4, 5, 6, 7]);
          return { a: 1, n: n, u: 0, v: 0, gerade: n % 2 === 0,
            text: 'Muss man \\(f(x) = x^{' + n + '}\\) einschränken, bevor man sie umkehrt?' }; },
        fehler: function(A){ return [[{ noetig: A.gerade ? 'nicht nötig' : 'nötig' }, 'Exponent']]; },
        pruefen: function(A, e){
          if (e.noetig === (A.gerade ? 'nötig' : 'nicht nötig')) return null;
          return A.gerade
            ? 'Der Exponent \\(' + A.n + '\\) ist gerade: \\(f(-x) = f(x)\\), also lägen im Spiegelbild über einem \\(x\\) zwei Punkte.'
            : 'Der Exponent \\(' + A.n + '\\) ist ungerade: Die Kurve steigt überall, jedem \\(y\\) gehört genau ein \\(x\\).'; },
        loesung: function(A){ return A.gerade ? '\\text{nötig — gerader Exponent}' : '\\text{nicht nötig — ungerader Exponent}'; } },

      'spiegelpunkt': { felder: ['x', 'y'], muster: 'Bildpunkt ( {x} | {y} )',
        eingabe: function(A){ return { x: String(A.py), y: String(A.px) }; },
        neu: function(){ var n = zufall([2, 3, 4]), px = zufall([2, 3, 2, 3, 4]).valueOf(),
            py = Math.pow(px, n);
          if (py > 81){ px = 2; py = Math.pow(2, n); }
          return { a: 1, n: n, u: 0, v: 0, px: px, py: py,
            text: 'Auf \\(f(x) = x^{' + n + '}\\)' + (n % 2 === 0 ? ' mit \\(x \\geq 0\\)' : '')
              + ' liegt \\(P' + pkt(px, py) + '\\). Welcher Punkt liegt dann auf \\(f^{-1}\\)?' }; },
        fehler: function(A){ return [[{ x: String(A.px), y: String(A.py) }, 'tauschen'],
                                     [{ x: String(-A.py), y: String(A.px) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          if (gl(e.x, A.py) && gl(e.y, A.px)) return null;
          if (gl(e.x, A.px) && gl(e.y, A.py)) return 'Das ist \\(P\\) selbst. Beim Spiegeln an \\(y = x\\) tauschen die beiden Koordinaten.';
          if (gl(e.x, -A.py) || gl(e.y, -A.px)) return 'Kein Vorzeichenwechsel: Gespiegelt wird an \\(y = x\\), nicht an einer Achse.';
          return 'Aus \\((x \\mid y)\\) wird \\((y \\mid x)\\): aus \\(' + pkt(A.px, A.py) + '\\) also …'; },
        loesung: function(A){ return 'P\'' + pkt(A.py, A.px); } },

      'umkehrfunktion': { felder: ['n', 'v'], muster: 'f⁻¹(x) = ⁿ√( x + {v} ),  n = {n}',
        eingabe: function(A){ return { n: String(A.n), v: String(-A.v) }; },
        neu: function(){ var n = zufall([3, 5, 3, 5, 7]), v = zufall(bereich(-5, 5, [0]));
          return { a: 1, n: n, u: 0, v: v,
            text: 'Bestimme die Umkehrfunktion von \\(f(x) = x^{' + n + '}' + plus(v) + '\\). '
              + 'Gib \\(n\\) und die Zahl an, die <em>unter</em> der Wurzel zu \\(x\\) dazukommt.' }; },
        fehler: function(A){ return [[{ n: String(A.n), v: String(A.v) }, 'andere Seite'],
                                     [{ n: String(1 / A.n), v: String(-A.v) }, 'Wurzelexponent']]
          .filter(function(p){ return !(gl(+p[0].n, A.n) && gl(+p[0].v, -A.v)); }); },
        pruefen: function(A, e){
          if (gl(e.n, A.n) && gl(e.v, -A.v)) return null;
          if (!gl(e.n, A.n)) return 'Der Wurzelexponent ist derselbe wie der Exponent von \\(f\\) — lies ihn dort ab.';
          if (gl(e.v, A.v)) return 'Beim Auflösen wandert \\(' + tz(A.v) + '\\) auf die andere Seite — mit umgekehrtem Vorzeichen.';
          return 'Erst \\(y ' + (A.v > 0 ? '- ' + A.v : '+ ' + (-A.v)) + ' = x^{' + A.n + '}\\), dann die Wurzel ziehen, dann \\(x\\) und \\(y\\) vertauschen.'; },
        loesung: function(A){ return 'f^{-1}(x) = \\sqrt[' + A.n + ']{x ' + (A.v > 0 ? '- ' + A.v : '+ ' + (-A.v)) + '}'; } },

      /* ── Kapitel 5: Wurzelfunktionen nutzen ──────────────────── */
      'wurzel-def': { felder: ['grenze'], muster: 'D = [ {grenze} ; +∞ [',
        eingabe: function(A){ return { grenze: String(A.u) }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2, 3]), n = zufall([2, 4, 6]),
            u = zufall(bereich(-5, 5, [0])), v = zufall(bereich(-3, 3));
          return { a: a, n: n, u: u, v: v,
            text: 'Welche Definitionsmenge hat \\(f(x) = ' + wzT(a, n, u, v) + '\\)?' }; },
        fehler: function(A){ return [[{ grenze: String(-A.u) }, 'Vorzeichen'], [{ grenze: '0' }, 'Radikand']]
          .filter(function(p){ return !gl(+p[0].grenze, A.u); }); },
        pruefen: function(A, e){
          if (gl(e.grenze, A.u)) return null;
          if (gl(e.grenze, -A.u)) return 'Vorzeichen: \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' \\geq 0\\) gibt \\(x \\geq ' + tz(A.u) + '\\).';
          if (gl(e.grenze, A.v)) return 'Die Zahl hinter der Wurzel ändert die Definitionsmenge nicht — nur der Radikand zählt.';
          return 'Der Radikand muss \\(\\geq 0\\) sein: Löse \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' \\geq 0\\).'; },
        loesung: function(A){ return 'D = [' + tz(A.u) + ';\\, +\\infty['; } },

      'wurzel-startpunkt': { felder: ['x', 'y'], muster: 'Startpunkt ( {x} | {y} )',
        eingabe: function(A){ return { x: String(A.u), y: String(A.v) }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2, 3]), n = zufall([2, 4]),
            u = zufall(bereich(-4, 4, [0])), v = zufall(bereich(-4, 4, [0]));
          return { a: a, n: n, u: u, v: v,
            text: 'Wo liegt der Startpunkt von \\(f(x) = ' + wzT(a, n, u, v) + '\\)?' }; },
        fehler: function(A){ return [[{ x: String(-A.u), y: String(A.v) }, 'Vorzeichen'],
                                     [{ x: String(A.v), y: String(A.u) }, 'Vertauscht']]
          .filter(function(p){ return !(gl(+p[0].x, A.u) && gl(+p[0].y, A.v)); }); },
        pruefen: function(A, e){
          if (gl(e.x, A.u) && gl(e.y, A.v)) return null;
          if (gl(e.x, A.v) && gl(e.y, A.u)) return 'Vertauscht: \\(u\\) steht unter der Wurzel, \\(v\\) dahinter.';
          if (gl(e.x, -A.u) && gl(e.y, A.v)) return 'Vorzeichen: Der Radikand wird null bei \\(x = ' + tz(A.u) + '\\), nicht bei \\(' + tz(-A.u) + '\\).';
          if (!gl(e.x, A.u)) return 'Der Startpunkt liegt dort, wo der Radikand null wird: \\(x = ' + tz(A.u) + '\\).';
          return 'Die Höhe des Startpunkts ist die Zahl hinter der Wurzel: \\(v = ' + tz(A.v) + '\\).'; },
        loesung: function(A){ return 'S' + pkt(A.u, A.v); } },

      'wurzel-nullstelle': { felder: ['x_0'], muster: 'x₀ = {x_0}',
        eingabe: function(A){ return { x_0: String(A.x0) }; },
        neu: function(){ var n = zufall([2, 3]), a = zufall([1, 2, 1, 2, 3]),
            w = zufall([1, 2, 3]), v = -a * w, u = zufall(bereich(-3, 3));
          return { a: a, n: n, u: u, v: v, w: w, x0: u + Math.pow(w, n),
            text: 'Berechne die Nullstelle von \\(f(x) = ' + wzT(a, n, u, v) + '\\).' }; },
        fehler: function(A){ var f = [[{ x_0: String(A.u + A.w) }, 'noch nicht']];
          if (!gl(A.u - Math.pow(A.w, A.n), A.x0)) f.push([{ x_0: String(A.u - Math.pow(A.w, A.n)) }, 'Vorzeichen']);
          return f.filter(function(p){ return !gl(+p[0].x_0, A.x0); }); },
        pruefen: function(A, e){
          if (gl(e.x_0, A.x0)) return null;
          if (gl(e.x_0, A.u + A.w)) return 'Der Wurzelwert stimmt — er ist aber noch nicht \\(x\\). Nimm beide Seiten hoch \\(' + A.n + '\\).';
          if (gl(e.x_0, A.u - Math.pow(A.w, A.n))) return 'Vorzeichen: \\(x = ' + tz(A.u) + ' + ' + Math.pow(A.w, A.n) + '\\).';
          if (gl(e.x_0, Math.pow(A.w, A.n))) return 'Das \\(u\\) fehlt noch: \\(x = u + ' + Math.pow(A.w, A.n) + '\\).';
          return 'Setz \\(f(x) = 0\\): Wurzel \\(= ' + A.w + '\\), beide Seiten hoch \\(' + A.n + '\\), dann nach \\(x\\) auflösen.'; },
        loesung: function(A){ return '\\sqrt[' + A.n + ']{x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + '} = ' + A.w
          + ' \\Rightarrow x_0 = ' + tz(A.u) + ' + ' + Math.pow(A.w, A.n) + ' = ' + tz(A.x0); } },

      'wurzelgleichung': { felder: ['x'], muster: 'x = {x}',
        eingabe: function(A){ return { x: String(A.x) }; },
        neu: function(){ var n = zufall([2, 3]), u = zufall(bereich(-4, 4)), c = zufall([2, 3, 4]);
          return { a: 1, n: n, u: u, v: 0, c: c, x: u + Math.pow(c, n),
            text: 'Löse \\(' + (n === 2 ? '\\sqrt{' : '\\sqrt[' + n + ']{') + 'x ' + (u > 0 ? '- ' + u : '+ ' + (-u)) + '} = ' + c + '\\).' }; },
        fehler: function(A){ var f = [[{ x: String(A.u + A.c) }, 'hoch']];
          if (!gl(A.u - Math.pow(A.c, A.n), A.x)) f.push([{ x: String(A.u - Math.pow(A.c, A.n)) }, 'Vorzeichen']);
          return f.filter(function(p){ return !gl(+p[0].x, A.x); }); },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          if (gl(e.x, A.u + A.c)) return 'Beide Seiten hoch \\(' + A.n + '\\): rechts steht dann \\(' + A.c + '^{' + A.n + '} = ' + Math.pow(A.c, A.n) + '\\).';
          if (gl(e.x, Math.pow(A.c, A.n))) return 'Das \\(u\\) fehlt: \\(x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = ' + Math.pow(A.c, A.n) + '\\).';
          if (gl(e.x, A.u - Math.pow(A.c, A.n))) return 'Vorzeichen beim Auflösen: \\(x = ' + tz(A.u) + ' + ' + Math.pow(A.c, A.n) + '\\).';
          return 'Beide Seiten hoch \\(' + A.n + '\\), dann nach \\(x\\) auflösen. Probe nicht vergessen.'; },
        loesung: function(A){ return 'x ' + (A.u > 0 ? '- ' + A.u : '+ ' + (-A.u)) + ' = ' + A.c + '^{' + A.n + '} = '
          + Math.pow(A.c, A.n) + ' \\Rightarrow x = ' + tz(A.x); } },

      'vergleich': { felder: ['ordnung'], muster: 'Es gilt {ordnung:√x > x > x²|x² > x > √x}',
        eingabe: function(A){ return { ordnung: A.klein ? '√x > x > x²' : 'x² > x > √x' }; },
        neu: function(){ var klein = Math.random() < 0.5, x = klein ? zufall([0.25, 0.04, 0.09, 0.16]) : zufall([4, 9, 16, 25]);
          return { a: 1, n: 2, u: 0, v: 0, klein: klein, x: x,
            text: 'Ordne \\(\\sqrt{x}\\), \\(x\\) und \\(x^2\\) der Grösse nach für \\(x = ' + x + '\\).' }; },
        fehler: function(A){ return [[{ ordnung: A.klein ? 'x² > x > √x' : '√x > x > x²' }, 'Setz']]; },
        pruefen: function(A, e){
          if (e.ordnung === (A.klein ? '√x > x > x²' : 'x² > x > √x')) return null;
          // Nicht z(): das rundet auf zwei Stellen, und «0.04^2 = 0» waere falsch.
          return 'Setz \\(x = ' + A.x + '\\) ein und rechne alle drei Werte aus: \\(\\sqrt{' + A.x + '} = '
            + String(Math.sqrt(A.x)) + '\\), \\(' + A.x + '\\), \\(' + A.x + '^2 = ' + String(A.x * A.x) + '\\).'; },
        loesung: function(A){ return '\\sqrt{' + A.x + '} = ' + String(Math.sqrt(A.x)) + ',\\quad ' + A.x
          + ',\\quad ' + A.x + '^2 = ' + String(A.x * A.x); } }
    };
    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie'), bild = box.querySelector('.ue-bild');
      function neu(){
        // Trifft der Wurf eine Gerade, nach der eine feste Aufgabe fragt, wird neu
        // gewürfelt (FEST oben). 40 Versuche reichen weit; danach gilt der letzte Wurf.
        A = T.neu();
        if (!OHNE_FEST[box.dataset.typ])
          for (var v = 0; v < 40 && fest(A.a, A.n, A.u, A.v); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="decimal" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        if (T.wahl) ein.querySelectorAll('select').forEach(function(w){ w.addEventListener('change', function(){ T.wahl(ein); }); });
        if (bild){
          while (bild.firstChild) bild.removeChild(bild.firstChild);
          if (T.graf){
            // Fenster so weit, dass der markierte Punkt (1 | a) und der Verlauf
            // bis x = ±2 hineinpassen — sonst ist der Exponent nicht ablesbar.
            // Je steiler die Kurve, desto ENGER das Fenster — sonst ist die interessante
            // Zone zusammengedrückt und f(2) liegt ausserhalb.
            var hoch = Math.abs(A.a * Math.pow(2, A.n));
            var gr = hoch > 24 ? 1.3 : hoch > 10 ? 1.8 : 2.4, fe = [-gr, gr, -8, 8];
            bild.setAttribute('viewBox', '0 0 170 170');
            var K = Achsen(bild, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3.5, pfeil: 6, xm: [1], ym: [2] });
            K.kurve(kurveF(A.a, A.n, 0, 0), 'kurve');
            K.punkt(1, A.a, 'p-pkt');
          }
        }
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;   // nach ✓ zählt erst die nächste Aufgabe
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){ if (i.disabled){ e[i.dataset.f] = NaN; i.classList.remove('falsch'); return; }
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


  /* ---------- Minigrafen: <svg class="mini" data-k="a,n,u,v[;a,n,u,v…]" data-fenster
       data-punkte data-titel data-wurzel="1" (n ist dann der Wurzelexponent)> ---------- */
  document.querySelectorAll('svg.mini[data-k]').forEach(function(svg){
    var kk = svg.dataset.k.split(';').map(function(s){ return s.split(',').map(Number); });
    var wz = svg.dataset.wurzel === '1';
    var fe = (svg.dataset.fenster || '-3,3,-3,3').split(',').map(Number);
    var w = 150, h = 150 * (fe[3] - fe[2]) / (fe[1] - fe[0]);
    svg.setAttribute('viewBox', '0 0 150 ' + h.toFixed(1)); svg.setAttribute('role', 'img');
    var K = Achsen(svg, { w: w, h: h, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, xm: [1], ym: [1], pfeil: 6,
      xname: svg.dataset.xname, yname: svg.dataset.yname });
    kk.forEach(function(k, i){
      var a = k[0], n = k[1], u = k[2] || 0, v = k[3] || 0, p = wz ? 1 / n : n;
      var f = kurveF(a, p, u, v);
      // Wurzelkurven grün, Potenzkurven blau; jede weitere Kurve neutral (Bezugskurve).
      var cls = i ? 'kurve g2' : (wz ? 'kurve gruen' : 'kurve');
      if (!wz && n < 0){ K.kurve(f, cls, fe[0], u - 0.02); K.kurve(f, cls, u + 0.02, fe[1]); }
      else K.kurve(f, cls);
    });
    // data-diagonale="1": die Spiegelachse y = x, gestrichelt und neutral.
    if (svg.dataset.diagonale === '1') K.kurve(function(x){ return x; }, 'normal');
    // Ein markierter Punkt ist hier immer ein neutraler Hinweis (gemeinsamer Punkt,
    // abgelesener Gitterpunkt) — grün bleibt der Wurzel und dem Startpunkt vorbehalten.
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){
      var q = p.split(',').map(Number);
      K.punkt(q[0], q[1], 'p-pkt');
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Kurve' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
