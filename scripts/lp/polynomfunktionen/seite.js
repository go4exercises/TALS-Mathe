<script>
/* Leitprogramm Polynomfunktionen — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Notation wie auf Themenseite 3.3:
   f(x) = aₙxⁿ + … + a₁x + a₀ (Grad n, Leitkoeffizient aₙ), Linearfaktordarstellung
   f(x) = a·(x − x₁)(x − x₂)…, Hochpunkt H, Tiefpunkt T.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = die Kurve und ihr Leitkoeffizient a · orange = Nullstellen und Linearfaktoren ·
   grün = Hoch- und Tiefpunkte · rot = Gegenbeispiel · Tinte = neutral (Leitterm,
   Bezugskurve, Läufer, y-Achsenabschnitt).
   Zahlen mit Dezimalpunkt und echtem Minus. */
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
  /* Ein Leitkoeffizient darf nie auf 0 stehenbleiben — dann wäre der Grad ein anderer.
     Der Regler springt über die Null hinweg, in die Richtung, aus der er kommt. */
  function ohneNull(inp){
    var letzt = +inp.value, st = parseFloat(inp.step) || 1;
    inp.addEventListener('input', function(){
      if (+inp.value === 0) inp.value = letzt > 0 ? -st : st;
      letzt = +inp.value;
    });
  }

  /* ---------- Polynome ----------
     Koeffizienten als Liste, höchster Exponent zuerst: [aₙ, …, a₁, a₀]. */
  function ausWurzeln(a, w){
    var c = [a];
    w.forEach(function(r){
      var n = c.concat([0]);
      for (var i = 1; i < n.length; i++) n[i] -= r * c[i - 1];
      c = n;
    });
    return c.map(function(k){ return Math.round(k * 1e9) / 1e9; });
  }
  function wert(c, x){ return c.reduce(function(s, k){ return s * x + k; }, 0); }
  function ableitung(c){ var n = c.length - 1; return c.slice(0, n).map(function(k, i){ return k * (n - i); }); }
  /* Horner: c durch (x − r) geteilt — Quotient und Rest. */
  function teilen(c, r){
    var q = [c[0]];
    for (var i = 1; i < c.length; i++) q.push(c[i] + r * q[i - 1]);
    return { q: q.slice(0, -1), rest: q[q.length - 1] };
  }
  /* Summenform in HTML, mit Dezimalpunkt und echtem Minus. */
  function summeText(c){
    var n = c.length - 1, s = '';
    c.forEach(function(k, i){
      var e = n - i; if (Math.abs(k) < 1e-12) return;
      var b = Math.abs(k), vz = k < 0 ? '−' : '+';
      var zahl = (b === 1 && e > 0) ? '' : z(b);
      var pot = e === 0 ? '' : e === 1 ? 'x' : 'x<sup>' + e + '</sup>';
      s += (s ? ' ' + vz + ' ' : (k < 0 ? '−' : '')) + zahl + pot;
    });
    return s || '0';
  }
  /* Linearfaktoren in HTML; gleiche Nullstellen werden zur Potenz zusammengefasst. */
  function faktorText(a, w, farbe){
    var zaehl = {}, reihe = [];
    w.forEach(function(r){ var k = z(r); if (!zaehl[k]){ zaehl[k] = 0; reihe.push(r); } zaehl[k]++; });
    var s = a === 1 ? '' : a === -1 ? '−' : sp('tx-blau', z(a)) + '·';
    reihe.forEach(function(r){
      var k = zaehl[z(r)];
      var kl = r === 0 ? 'x' : '(x ' + (r > 0 ? '− ' : '+ ') + sp(farbe || 'tx-orange', z(Math.abs(r))) + ')';
      s += kl + (k > 1 ? '<sup>' + k + '</sup>' : '');
    });
    return s;
  }
  /* Reelle Nullstellen und Extremstellen numerisch, im Fenster [a; b].
     Eine Nullstelle, an der der Graph nur berührt, wechselt das Vorzeichen nicht —
     sie wird darum über die Extremstellen gefunden (|f| dort fast null). */
  function extrema(c, a, b){
    var d = ableitung(c), aus = [], N = 2000, p = a, dp = wert(d, a);
    for (var i = 1; i <= N; i++){
      var q = a + (b - a) * i / N, dq = wert(d, q);
      if ((dp > 0 && dq <= 0) || (dp < 0 && dq >= 0)){
        var lo = p, hi = q;
        for (var k = 0; k < 50; k++){ var m = (lo + hi) / 2; if ((wert(d, m) > 0) === (dp > 0)) lo = m; else hi = m; }
        aus.push({ x: (lo + hi) / 2, hoch: dp > 0 });
      }
      if (dq !== 0) { p = q; dp = dq; }
    }
    return aus;
  }
  function nullstellen(c, a, b){
    var aus = [], N = 4000, p = a, fp = wert(c, a);
    for (var i = 1; i <= N; i++){
      var q = a + (b - a) * i / N, fq = wert(c, q);
      if (fp === 0) aus.push(p);
      else if (fp * fq < 0){
        var lo = p, hi = q;
        for (var k = 0; k < 60; k++){ var m = (lo + hi) / 2; if (wert(c, m) * fp > 0) lo = m; else hi = m; }
        aus.push((lo + hi) / 2);
      }
      p = q; fp = fq;
    }
    if (fp === 0) aus.push(p);
    extrema(c, a, b).forEach(function(e){ if (Math.abs(wert(c, e.x)) < 1e-7) aus.push(e.x); });
    aus.sort(function(u, v){ return u - v; });
    return aus.filter(function(x, i){ return i === 0 || Math.abs(x - aus[i - 1]) > 1e-4; });
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

  /* ---------- Kapitel 1: Linearfaktoren und Nullstellen ----------
     Unterschied zum «Linearfaktor-Baukasten» auf Themenseite 3.3: dort hat jede Nullstelle
     ihre eigene Reglerfarbe. Hier sind alle drei orange — eine Farbe, eine Bedeutung
     (Nullstelle) im ganzen Leitprogramm —, der y-Achsenabschnitt (0 | f(0)) ist markiert,
     weil Kapitel 1 über ihn a bestimmt, und die Aufgabenleiste führt. */
  var FENSTER1 = { w: 300, h: 300, x0: -4, x1: 5, y0: -8, y1: 10, sy: 2, xm: [-3, -2, -1, 1, 2, 3, 4], ym: [-6, -4, -2, 2, 4, 6, 8] };
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER1), ziel = null, pruefen = function(){}, bewegt = {};
    // ohneNull zuerst: Es muss den Regler korrigieren, bevor zeichnen() ihn liest.
    ohneNull(fig.querySelector('input[data-p="a"]'));
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function zust(){ var w = werte(r), ws = [w.x1, w.x2, w.x3], c = ausWurzeln(w.a, ws);
      return { a: w.a, w: ws, c: c, f0: wert(c, 0), bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (ziel) K.kurve(function(x){ return wert(ausWurzeln(ziel[0], ziel[1]), x); }, 'zielkurve');
      K.kurve(function(x){ return wert(s.c, x); }, 'kurve');
      K.punkt(0, s.f0, 'p-pkt', '(0 | ' + z(s.f0) + ')', 8, -8);
      var gesehen = {};
      s.w.forEach(function(x){ if (gesehen[x]) return; gesehen[x] = 1; K.punkt(x, 0, 'p-ns'); });
      var ns = Object.keys(gesehen).map(Number).sort(function(p, q){ return p - q; });
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + faktorText(s.a, s.w) + ' = ' + summeText(s.c)
        + '<br>Nullstellen: ' + ns.map(function(x){ return sp('tx-orange', z(x)); }).join(', ')
        + ' &nbsp;·&nbsp; Grad 3, Leitkoeffizient ' + sp('tx-blau', z(s.a));
      pruefen();
    }
    function bau(a, w, tex){ return { text: 'Bau nach: \\(' + tex + '\\)', ok: function(s){ return s.a === a && gleicheMenge(s.w, w); } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an allen drei Nullstellen-Reglern. Was geschieht mit dem Graphen?',
        ok: function(s){ return s.bewegt.x1 && s.bewegt.x2 && s.bewegt.x3; } },
      // Startzustand a = 0.5, Nullstellen −2, 1, 3 (wie im Clip) — keine Aufgabe trifft ihn.
      bau(1, [-3, 0, 2], 'f(x) = (x+3)\\,x\\,(x-2)'),
      { text: 'Stell \\(a = -1\\) ein. Was ändert sich am Graphen — und was nicht?',
        ok: function(s){ return s.a === -1; } },
      { text: 'Stell eine Funktion ein, deren Graph die \\(y\\)-Achse bei \\((0 \\mid 4)\\) schneidet.',
        ok: function(s){ return Math.abs(s.f0 - 4) < 1e-9; } },
      { text: 'Bau nach: \\(f(x) = 2x^3 - 2x\\). Tipp: Leitkoeffizient ablesen, dann die Nullstellen suchen.',
        ok: function(s){ return s.a === 2 && gleicheMenge(s.w, [-1, 0, 1]); } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [-0.5, [-3, -1, 2]]; },
        ok: function(s){ return s.a === -0.5 && gleicheMenge(s.w, [-3, -1, 2]); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: mehrfache Nullstellen ----------
     Unterschied zum Baukasten der Themenseite: dort entsteht eine doppelte Nullstelle nur,
     wenn man zwei Regler zufällig aufeinanderlegt. Hier hat jede der zwei Nullstellen ihren
     eigenen Vielfachheits-Regler k bzw. m, und die Anzeige sagt an jeder Nullstelle,
     ob der Graph schneidet, berührt oder eine Terrasse bildet. */
  var FENSTER2 = { w: 300, h: 300, x0: -4, x1: 4, y0: -6, y1: 6, sy: 1, xm: [-3, -2, -1, 1, 2, 3], ym: [-4, -2, 2, 4] };
  function verhalten(k){ return k === 1 ? 'einfach: schneidet' : k === 2 ? 'doppelt: berührt' : k === 3 ? 'dreifach: Terrasse' : k + '-fach: ' + (k % 2 ? 'schneidet flach' : 'berührt flach'); }
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER2), ziel = null, pruefen = function(){}, bewegt = {};
    // ohneNull zuerst: Es muss den Regler korrigieren, bevor zeichnen() ihn liest.
    ohneNull(fig.querySelector('input[data-p="a"]'));
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function liste(w){ var l = []; for (var i = 0; i < w.k; i++) l.push(w.p); for (i = 0; i < w.m; i++) l.push(w.q); return l; }
    function zust(){
      var w = werte(r), l = liste(w), c = ausWurzeln(w.a, l), vf = {};
      l.forEach(function(x){ vf[x] = (vf[x] || 0) + 1; });
      return { a: w.a, p: w.p, k: w.k, q: w.q, m: w.m, l: l, c: c, vf: vf, grad: l.length, bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (ziel) K.kurve(function(x){ return wert(ausWurzeln(ziel[0], ziel[1]), x); }, 'zielkurve');
      K.kurve(function(x){ return wert(s.c, x); }, 'kurve');
      var stellen = Object.keys(s.vf).map(Number).sort(function(u, v){ return u - v; });
      stellen.forEach(function(x){ K.punkt(x, 0, 'p-ns'); });
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + faktorText(s.a, s.l) + ' &nbsp;·&nbsp; Grad ' + s.grad + '<br>'
        + stellen.map(function(x){ return 'bei ' + sp('tx-orange', z(x)) + ': ' + verhalten(s.vf[x]); }).join(' &nbsp;·&nbsp; ');
      pruefen();
    }
    function vielfach(s, x){ return s.vf[x] || 0; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(k\\) von 1 bis 3. Was tut der Graph an der Stelle \\(p\\)?',
        ok: function(s){ return s.bewegt.k; } },
      // Startzustand 0.5·(x − 1)²(x + 2), wie im Clip — er berührt bei 1, schneidet bei −2.
      { text: 'Stell ein: Der Graph <b>berührt</b> die \\(x\\)-Achse bei \\(2\\) und <b>schneidet</b> sie bei \\(-1\\).',
        ok: function(s){ return vielfach(s, 2) % 2 === 0 && vielfach(s, 2) > 0 && vielfach(s, -1) % 2 === 1 && Object.keys(s.vf).length === 2; } },
      { text: 'Stell einen <b>Terrassenpunkt</b> bei \\(x = 0\\) ein.',
        ok: function(s){ return vielfach(s, 0) === 3; } },
      { text: 'Stell ein Polynom vom Grad 4 ein, dessen Graph die \\(x\\)-Achse an <b>zwei</b> Stellen nur berührt.',
        ok: function(s){ var st = Object.keys(s.vf); return s.grad === 4 && st.length === 2 && st.every(function(x){ return s.vf[x] % 2 === 0; }); } },
      { text: 'Stell \\(k = 1\\), \\(m = 2\\) ein und schieb \\(q\\) auf \\(p\\). Welche Vielfachheit hat die gemeinsame Nullstelle?',
        ok: function(s){ return s.k === 1 && s.m === 2 && s.p === s.q; } },
      { text: 'Triff die grüne Kurve.', setup: function(){ ziel = [-1, [0, 0, 0, 2]]; },
        ok: function(s){ return s.a === -1 && gleicheMenge(s.l, [0, 0, 0, 2]); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: der Globalverlauf ----------
     Unterschied zu den Animationen «Globalverlauf» und «Leitterm-Zoom» der Themenseite:
     dort zeigt ein Knopf je einen fertigen Fall bzw. zoomt eine feste Funktion. Hier stellt
     man f(x) = a·xⁿ + c·xⁿ⁻² + d selbst ein — Grad, Leitkoeffizient und zwei Zusatzterme —,
     der Schalter «von weitem» weitet das Fenster auf das Zehnfache, und die Anzeige zählt
     Nullstellen und Extremstellen und nennt die Symmetrie nach den Exponenten. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), pruefen = function(){}, bewegt = {};
    var weit = fig.querySelector('.sim-schalter input');
    // ohneNull zuerst: Es muss den Regler korrigieren, bevor zeichnen() ihn liest.
    ohneNull(fig.querySelector('input[data-p="a"]'));
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    if (weit) weit.addEventListener('change', function(){ bewegt.weit = true; zeichnen(); });
    function koeff(w){
      var c = []; for (var i = 0; i <= w.n; i++) c.push(0);
      c[0] += w.a; c[2] += w.c; c[w.n] += w.d;        // xⁿ, xⁿ⁻², x⁰ (bei n = 2 fallen c und d zusammen)
      return c;
    }
    function zust(){
      var w = werte(r), c = koeff(w), ex = extrema(c, -12, 12), ns = nullstellen(c, -12, 12);
      var exps = [w.n]; if (w.c !== 0) exps.push(w.n - 2); if (w.d !== 0) exps.push(0);
      if (w.n === 2 && w.c + w.d === 0) exps = [2];
      var ger = exps.every(function(e){ return e % 2 === 0; }), ung = exps.every(function(e){ return e % 2 === 1; });
      return { n: w.n, a: w.a, c: w.c, d: w.d, k: c, ns: ns.length, ex: ex.length, weit: !!(weit && weit.checked),
               sym: ger ? 'achs' : ung ? 'punkt' : 'weder', bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var o;
      if (s.weit){
        // Von weitem: x bis ±30, y so hoch, wie der Leitterm am Rand reicht.
        var R = Math.abs(s.a) * Math.pow(30, s.n) * 1.15;
        o = { w: 300, h: 300, x0: -30, x1: 30, y0: -R, y1: R, sx: 10, sy: R / 4, xm: [-20, -10, 10, 20], ym: [] };
      } else o = { w: 300, h: 300, x0: -3, x1: 3, y0: -6, y1: 6, sx: 1, sy: 1, xm: [-2, -1, 1, 2], ym: [-4, -2, 2, 4] };
      var K = Achsen(svg, o);
      K.kurve(function(x){ return s.a * Math.pow(x, s.n); }, 'normal hilfslinie');
      K.kurve(function(x){ return wert(s.k, x); }, 'kurve');
      var vz = s.a > 0;
      var enden = s.n % 2 === 0 ? (vz ? 'beide Enden oben' : 'beide Enden unten')
                                : (vz ? 'von links unten nach rechts oben' : 'von links oben nach rechts unten');
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + summeText(s.k) + '<br>Grad ' + s.n + ', Leitkoeffizient ' + sp('tx-blau', z(s.a))
        + ' &nbsp;·&nbsp; <b>' + enden + '</b><br>' + s.ns + ' Nullstelle' + (s.ns === 1 ? '' : 'n') + ' (höchstens ' + s.n + ') · '
        + s.ex + ' Extremstelle' + (s.ex === 1 ? '' : 'n') + ' (höchstens ' + (s.n - 1) + ') · '
        + (s.sym === 'achs' ? 'nur gerade Exponenten: achsensymmetrisch zur <i>y</i>-Achse'
           : s.sym === 'punkt' ? 'nur ungerade Exponenten: punktsymmetrisch zum Ursprung' : 'gemischte Exponenten: keine dieser Symmetrien');
      fig.classList.toggle('ohne-hilfslinien', !fig.querySelector('.hilfs-schalter input').checked);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(n\\) und an \\(a\\). Wohin zeigen die beiden Enden?',
        ok: function(s){ return s.bewegt.n && s.bewegt.a; } },
      // Startzustand x³ − 4x (wie im Clip): Grad 3, a > 0 — keine Aufgabe trifft ihn.
      { text: 'Stell ein Polynom ein, dessen <b>beide Enden nach unten</b> zeigen.',
        ok: function(s){ return s.n % 2 === 0 && s.a < 0; } },
      { text: 'Stell ein Polynom ein, das <b>von links oben nach rechts unten</b> verläuft.',
        ok: function(s){ return s.n % 2 === 1 && s.a < 0; } },
      { text: 'Stell \\(n = 5\\) ein und setz den Haken «von weitem». Was bleibt von den Zusatztermen übrig?',
        ok: function(s){ return s.n === 5 && s.weit; } },
      { text: 'Stell ein Polynom vom Grad 4 mit <b>vier</b> Nullstellen ein.',
        ok: function(s){ return s.n === 4 && s.ns === 4; } },
      { text: 'Stell ein Polynom vom Grad 4 <b>ohne</b> Nullstelle ein.',
        ok: function(s){ return s.n === 4 && s.ns === 0; } },
      { text: 'Stell ein Polynom vom Grad 3 ein, das <b>nicht</b> punktsymmetrisch zum Ursprung ist.',
        ok: function(s){ return s.n === 3 && s.sym === 'weder'; } },
      { text: 'Stell ein Polynom vom Grad 5 mit genau <b>einer</b> Nullstelle ein. Geht es auch mit keiner?',
        ok: function(s){ return s.n === 5 && s.ns === 1; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Nullstellen berechnen ----------
     Keine Animation der Themenseite entspricht diesem Schritt. Die Simulation macht das
     Raten sichtbar: Die Probestelle wandert über die Teiler von a₀, f(r) steht daneben, und
     sobald f(r) = 0 ist, spaltet sie den Linearfaktor (x − r) ab und zeigt den Rest. */
  var POLY4 = { p0: [1, -2, -5, 6], p1: [1, 2, -1, -2], p2: [1, -1, -8, 12], p3: [1, -3, -4, 12] };
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -5, x1: 5, y0: -15, y1: 15, sy: 5, xm: [-4, -2, 2, 4], ym: [-10, -5, 5, 10] });
    var pruefen = function(){}, bewegt = {}, c = POLY4.p0, gefunden = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    function echte(){ return nullstellen(c, -7, 7).map(function(x){ return Math.round(x); }); }
    function zust(){ var w = werte(r);
      return { r: w.r, f: wert(c, w.r), gefunden: Object.keys(gefunden).map(Number), alle: echte(), c: c, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen,
                aufraeumen: function(){ bewegt = {}; } };
    function teiler(n){ n = Math.abs(n); var t = []; for (var i = 1; i <= n; i++) if (n % i === 0) t.push(i); return t; }
    function zeichnen(){
      var w = werte(r), y = wert(c, w.r);
      if (y === 0) gefunden[w.r] = true;
      K.leeren();
      K.kurve(function(x){ return wert(c, x); }, 'kurve');
      K.senkrecht(w.r, 'asym');
      Object.keys(gefunden).forEach(function(x){ K.punkt(+x, 0, 'p-ns'); });
      K.punkt(w.r, Math.max(-15, Math.min(15, y)), 'p-pkt');
      var a0 = c[c.length - 1];
      var t = teiler(a0).map(function(q){ return '±' + q; }).join(', ');
      var zeile = 'f(x) = ' + summeText(c) + '<br>Kandidaten (Teiler von ' + z(a0) + '): ' + t
        + '<br>f(' + z(w.r) + ') = ' + z(y);
      if (y === 0){
        var q = teilen(c, w.r).q;
        zeile += ' &nbsp;→ <b>Nullstelle!</b> &nbsp;f(x) = (x ' + (w.r > 0 ? '− ' : '+ ') + sp('tx-orange', z(Math.abs(w.r))) + ')·(' + summeText(q) + ')';
      }
      var gf = Object.keys(gefunden).map(Number).sort(function(u, v){ return u - v; });
      zeile += '<br>gefunden: ' + (gf.length ? gf.map(function(x){ return sp('tx-orange', z(x)); }).join(', ') : '—');
      rolle(fig, 'formel').innerHTML = zeile;
      pruefen();
    }
    function wechsle(p){ return function(){ c = POLY4[p]; gefunden = {}; r.r.value = 0; }; }
    function alleGefunden(s){ return s.alle.every(function(x){ return s.gefunden.indexOf(x) >= 0; }); }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Fahr die Probestelle über die Teiler von 6 und finde alle drei Nullstellen von \\(x^3 - 2x^2 - 5x + 6\\).',
        ok: alleGefunden },
      { text: 'Neues Polynom: \\(f(x) = x^3 + 2x^2 - x - 2\\). Finde eine Nullstelle unter den Teilern von \\(-2\\).',
        setup: wechsle('p1'), ok: function(s){ return s.gefunden.length >= 1; } },
      { text: 'Lies ab, was nach dem Abspalten bleibt, und finde die beiden anderen Nullstellen auch.',
        ok: alleGefunden },
      { text: '\\(f(x) = x^3 - x^2 - 8x + 12\\): Finde alle Nullstellen. Es sind nur zwei — woran liegt das?',
        setup: wechsle('p2'), ok: alleGefunden },
      { text: '\\(f(x) = x^3 - 3x^2 - 4x + 12\\): Finde alle drei Nullstellen.',
        setup: wechsle('p3'), ok: alleGefunden }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Hoch- und Tiefpunkte ----------
     Unterschied zur Schachtel-Animation und zu Beispiel 2 der Themenseite: dort ist das
     Extremum fertig eingezeichnet. Hier sucht man es mit einem Läufer selbst, und ein
     Schalter schränkt die Definitionsmenge ein — dann zeigt sich, dass das absolute
     Maximum auch am Rand liegen kann. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -3, x1: 3, y0: -10, y1: 20, sy: 5, xm: [-2, -1, 1, 2], ym: [-5, 5, 10, 15] });
    var pruefen = function(){}, bewegt = {};
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    if (schalter) schalter.addEventListener('change', function(){ bewegt.ein = true; zeichnen(); });
    function f(x){ return x * x * x - 3 * x; }
    function zust(){ var w = werte(r), ein = !!(schalter && schalter.checked);
      return { x: w.x, y: f(w.x), l: w.l, r: w.r, ein: ein, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var s = zust();
      // Ohne Einschränkung läuft der Läufer frei; mit ihr bleibt er in D.
      if (s.ein){ var x = Math.max(s.l, Math.min(s.r, s.x)); if (x !== s.x){ r.x.value = x; s = zust(); } }
      fig.querySelectorAll('.d-regler input').forEach(function(i){ i.disabled = !s.ein; });
      K.leeren();
      if (s.ein){
        K.kurve(f, 'normal');
        K.kurve(f, 'kurve', s.l, s.r);
        K.punkt(s.l, f(s.l), 'p-pkt'); K.punkt(s.r, f(s.r), 'p-pkt');
      } else K.kurve(f, 'kurve');
      // Gerundete Werte mit «≈» (HOWTO §15).
      var gr = Math.abs(s.y - Math.round(s.y * 1000) / 1000) > 1e-12, yt = (gr ? '≈ ' : '') + z(s.y);
      K.punkt(s.x, s.y, 'p-lauf', '(' + z(s.x) + ' | ' + yt + ')', s.x > 1.5 ? -8 : 8, -10, s.x > 1.5 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML = 'f(x) = x<sup>3</sup> − 3x &nbsp;·&nbsp; Läufer bei x = ' + z(s.x)
        + ', f(x) ' + (gr ? '≈ ' : '= ') + z(s.y)
        + ' &nbsp;·&nbsp; ' + (s.ein ? 'D = [' + z(s.l) + '; ' + z(s.r) + ']' : 'D = ℝ');
      pruefen();
    }
    function nah(a, b){ return Math.abs(a - b) < 0.051; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Fahr den Läufer von links nach rechts. Wo steigt der Graph, wo fällt er?',
        ok: function(s){ return s.bewegt.x; } },
      // Startzustand: Läufer bei x = 0 — weder Hoch- noch Tiefpunkt.
      { text: 'Bring den Läufer auf den <b>Hochpunkt</b>. Lies \\(H\\) ab.',
        ok: function(s){ return nah(s.x, -1); } },
      { text: 'Bring den Läufer auf den <b>Tiefpunkt</b>. Lies \\(T\\) ab.',
        ok: function(s){ return nah(s.x, 1); } },
      { text: 'Finde eine Stelle, an der \\(f\\) <b>grösser</b> ist als im Hochpunkt.',
        ok: function(s){ return !s.ein && s.y > 2 + 1e-9; } },
      // Nicht das Clip-Beispiel D = [−1.5; 2.5] (HOWTO §15).
      { text: 'Setz den Haken «\\(D\\) einschränken», stell \\(D = [-2;\\, 3]\\) ein und bring den Läufer auf den grössten Wert in \\(D\\).',
        ok: function(s){ return s.ein && s.l === -2 && s.r === 3 && nah(s.x, 3); } },
      // Bei r = 2 ist f(2) = 2 = f(−1): Der Hochpunkt bleibt absolutes Maximum (gleichauf mit dem Rand).
      { text: 'Stell \\(D\\) so ein, dass der Hochpunkt das <b>absolute</b> Maximum auf \\(D\\) ist, und bring den Läufer dorthin.',
        ok: function(s){ return s.ein && s.l <= -1 && s.r <= 2 && nah(s.x, -1); } }
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
    function mischen(l){ l = l.slice(); for (var i = l.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = l[i]; l[i] = l[j]; l[j] = t; } return l; }
    function ziehe(l, k){ return mischen(l).slice(0, k); }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    /* Linearfaktor (x − r) in LaTeX; gleiche r werden zur Potenz zusammengefasst. */
    function klT(r){ return r === 0 ? 'x' : '(x ' + (r > 0 ? '- ' + r : '+ ' + (-r)) + ')'; }
    function vor(a){ return a === 1 ? '' : a === -1 ? '-' : tz(a); }
    function faktT(a, w){
      var zaehl = {}, reihe = [];
      w.forEach(function(r){ if (!zaehl[r]){ zaehl[r] = 0; reihe.push(r); } zaehl[r]++; });
      // x zuerst (wie «x(x − 3)(x + 3)»), sonst in der gewürfelten Reihenfolge
      reihe.sort(function(u, v){ return (u === 0 ? -1 : 0) - (v === 0 ? -1 : 0); });
      return vor(a) + reihe.map(function(r){ return klT(r) + (zaehl[r] > 1 ? '^{' + zaehl[r] + '}' : ''); }).join('');
    }
    /* Summenform in LaTeX. */
    function sumT(c){
      var n = c.length - 1, s = '';
      c.forEach(function(k, i){
        var e = n - i; if (Math.abs(k) < 1e-12) return;
        var b = Math.abs(k), zahl = (b === 1 && e > 0) ? '' : String(b);
        var pot = e === 0 ? '' : e === 1 ? 'x' : 'x^{' + e + '}';
        s += s ? (k < 0 ? ' - ' : ' + ') + zahl + pot : (k < 0 ? '-' : '') + zahl + pot;
      });
      return s;
    }
    /* Polynome, nach denen das Leitprogramm an fester Stelle fragt — eine Zufallsübung
       darf keines davon treffen, sonst steht ihre Lösung schon irgendwo (HOWTO §15).
       Je Eintrag Leitkoeffizient und alle Nullstellen samt Vielfachheit.
       Reihenfolge: Clips · Simulationen · Aufgaben der Kapitel · Vortest · Gesamttest. */
    var FEST = [
      [0.5, -2, 1, 3], [0.5, -2, 1, 4], [0.5, -2, 1, 2], [1, -2, 1, 3], [-0.5, -2, 1, 3], [0.5, -2, 1, 1],
      [0.5, 1, 1, 1], [1, -1, -1, 2], [0.5, 4, -1, -3], [-3, 1, -2], [-0.5, -3, 1, 2], [0.5, -1, 2, 4],
      [1, 2, 2, -1], [1, -1, -1, -1], [-1, -2, 1, 1], [0.5, -1, 3, 3], [1, 0, 0, 2, 2], [1, -2, 0, 2],
      [0.25, -2, -1, 1, 2], [1, -3, 0, 3], [1, 0, 0, 4], [1, -1, -2, 2], [1, 1, 5],
      // Simulationen
      [1, -3, 0, 2], [2, -1, 0, 1], [-0.5, -3, -1, 2], [-1, 0, 0, 0, 2], [1, -2, -1, 1], [1, 2, 2, -3], [1, -2, 2, 3],
      // Aufgaben der Kapitel und Vortest
      [-1, 2, -1, -5], [2, -1, 3], [-0.5, -3, 1, 2], [1, -1, 1, 3], [-0.5, 2, 2, -1], [-2, -1, -1, 3],
      [1, 0, -4, 2], [1, 1, 2, 3], [1, 1, 1, -3], [1, 0, 2, -2], [1, -1, 2, -3], [1, 1, 3, -3], [0.5, -4, 1, 2], [1, 2, 3, -1], [1, 2, -1, -3],
      // Gesamttest (downloads/leitprogramme/polynomfunktionen/gesamttest.tex)
      [3, 2, 2, -1], [-0.5, -2, -2, 1], [1, -1, 2, 3], [-2, -3, 1, 1, 1], [0.5, -2, 2, 2], [-1, 0, 0, 6]
    ].map(schluessel);
    function schluessel(p){ return p[0] + '|' + p.slice(1).sort(function(u, v){ return u - v; }).join(','); }
    function fest(a, w){ return w && FEST.indexOf(schluessel([a].concat(w))) >= 0; }
    /* Typen ohne Nullstellen-Liste haben einen eigenen Schlüssel (T.schl) und eine eigene
       Sperrliste — sonst würfelte «Grad 2: exakt berechnen» genau G6 des Gesamttests. */
    var SPERRE = [
      // extrem-ablesen [s, q, u, v]: x³ − 3x (Clip, Sim 5) · −x³ + 3x + 1 (Kontrollclip) · 5a · 5d · GT G6
      'e|1|1|0|0', 'e|-1|1|0|1', 'e|1|1|1|1', 'e|1|1|1|-2', 'e|-1|1|1|3', 'e|1|1|1|2',
      // scheitel-extrem [a, b, c]: Clip, Kontrollclip, 5b, GT G7
      's|-1|4|-1', 's|1|-6|5', 's|2|-8|5', 's|0.5|-3|2', 's|-2|8|-3',
      // lokal-global [s, l, r]: Clip «Am Rand», Kontrollclip F5
      'l|1|-1.5|2.5', 'l|1|0|4'
    ];
    function gesperrt(T, A){ return T.schl ? SPERRE.indexOf(T.schl(A)) >= 0 : fest(A.a, A.w); }

    var TYPEN = {
      /* ── Kapitel 1: Linearfaktoren und Nullstellen ───────────── */
      'nullstellen-ablesen': { felder: ['x1', 'x2', 'x3'], muster: 'Nullstellen: {x1}  {x2}  {x3}',
        eingabe: function(A){ return { x1: String(A.w[0]), x2: String(A.w[1]), x3: String(A.w[2]) }; },
        neu: function(){ var w = ziehe(bereich(-5, 5, [0]), 3), a = zufall([-3, -2, -1, 0.5, 2, 3]);
          return { a: a, w: w, text: 'Gib die Nullstellen von \\(f(x) = ' + faktT(a, w) + '\\) an (Reihenfolge egal).' }; },
        fehler: function(A){ return [[{ x1: String(-A.w[0]), x2: String(-A.w[1]), x3: String(-A.w[2]) }, 'umgekehrtem Vorzeichen'],
                                     [{ x1: String(A.a), x2: String(A.w[1]), x3: String(A.w[2]) }, 'keine Nullstelle']]
          .filter(function(p, i){ return !gleich(A, p[0]) && (i === 0 || (A.w.indexOf(A.a) < 0 && A.w.indexOf(-A.a) < 0)); }); },
        pruefen: function(A, e){
          var ein = [e.x1, e.x2, e.x3];
          if (gleich(A, e)) return null;
          if (ein.some(function(x, i){ return A.w.indexOf(-x) >= 0 && A.w.indexOf(x) < 0; }))
            return 'Vorzeichen: In der Klammer steht die Nullstelle mit umgekehrtem Vorzeichen — \\(' + klT(A.w[0]) + '\\) wird null bei \\(x = ' + tz(A.w[0]) + '\\).';
          if (ein.some(function(x){ return gl(x, A.a); }) && A.w.indexOf(A.a) < 0)
            return 'Der Faktor \\(' + tz(A.a) + '\\) vor den Klammern ist keine Nullstelle — er wird nie null.';
          return 'Setz jede Klammer einzeln null und löse nach \\(x\\) auf.'; },
        loesung: function(A){ return 'x \\in \\{' + A.w.slice().sort(function(u, v){ return u - v; }).map(tz).join(';\\ ') + '\\}'; } },

      'grad-leitkoeff': { felder: ['n', 'an'], muster: 'Grad {n}   Leitkoeffizient {an}',
        eingabe: function(A){ return { n: String(A.n), an: String(A.a) }; },
        // Nur verschiedene, einfache Linearfaktoren: Potenzen wie (x − p)² führt erst Kapitel 2 ein.
        neu: function(){ var a = zufall([-4, -3, -2, -1, 0.5, 2, 3, 5]), w = ziehe(bereich(-5, 5), zufall([2, 3, 4]));
          return { a: a, w: w, n: w.length,
            text: 'Gib Grad und Leitkoeffizient von \\(f(x) = ' + faktT(a, w) + '\\) an.' }; },
        fehler: function(A){ return [[{ n: String(A.n), an: String(-A.a) }, 'Vorzeichen'], [{ n: String(A.n + 1), an: String(A.a) }, 'Klammern']]; },
        pruefen: function(A, e){
          if (gl(e.n, A.n) && gl(e.an, A.a)) return null;
          var r = [];
          if (!gl(e.n, A.n)) r.push('Grad: Zähl die Klammern mit \\(x\\) — jede bringt einen Faktor \\(x\\). Der Faktor vorne zählt nicht.');
          if (!gl(e.an, A.a)) r.push(gl(e.an, -A.a) ? 'Vorzeichen des Leitkoeffizienten: Jede Klammer beginnt mit \\(+x\\), das Vorzeichen kommt nur vom Faktor vorne.'
                                                    : 'Leitkoeffizient: Multiplizier nur die \\(x\\)-Terme aus — übrig bleibt der Faktor vorne.');
          return r.join(' '); },
        loesung: function(A){ return '\\text{Grad } ' + A.n + ',\\ a_' + A.n + ' = ' + tz(A.a); } },

      'a-bestimmen': { felder: ['a'], muster: 'a = {a}',
        eingabe: function(A){ return { a: String(A.a) }; },
        neu: function(){ var w = ziehe(bereich(-4, 4, [0]), 3), a = zufall([-2, -1, -0.5, 0.5, 1, 2, 3]);
          var p = w.reduce(function(s, r){ return s * (-r); }, 1);
          if (Math.abs(a * p) > 60) a = p > 0 ? 0.5 : -0.5;
          return { a: a, w: w, p: p, f0: a * p,
            text: 'Grad 3, Nullstellen \\(' + w.map(tz).join(',\\ ') + '\\), und der Graph geht durch \\((0 \\mid ' + tz(a * p) + ')\\). '
              + 'Bestimme \\(a\\) in \\(f(x) = a' + faktT(1, w) + '\\).' }; },
        fehler: function(A){ return [[{ a: String(-A.a) }, 'Minuszeichen'], [{ a: String(A.f0 * A.p) }, 'geteilt']]
          .filter(function(p){ return !gl(+p[0].a, A.a); }); },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, -A.a)) return 'Zähl die Minuszeichen in \\(f(0) = a \\cdot (' + A.w.map(function(r){ return tz(-r); }).join(') \\cdot (') + ')\\).';
          if (gl(e.a, A.f0 * A.p)) return 'Du hast multipliziert statt geteilt: \\(' + tz(A.p) + 'a = ' + tz(A.f0) + '\\), also \\(a = ' + tz(A.f0) + ' : ' + tz(A.p) + '\\).';
          return 'Setz \\(x = 0\\) ein: \\(f(0) = a \\cdot ' + tz(A.p) + '\\), und das muss \\(' + tz(A.f0) + '\\) sein.'; },
        loesung: function(A){ return 'f(0) = ' + tz(A.p) + 'a = ' + tz(A.f0) + ' \\Rightarrow a = ' + tz(A.a); } },

      /* ── Kapitel 2: mehrfache Nullstellen ────────────────────── */
      'vielfachheit': { felder: ['v'], muster: 'An dieser Stelle {v:schneidet der Graph die x-Achse|berührt der Graph die x-Achse|schneidet der Graph mit Terrasse}',
        eingabe: function(A){ return { v: A.richtig }; },
        neu: function(){ var p = ziehe(bereich(-4, 4), 2), k = zufall([1, 2, 3]), m = zufall([1, 2, 3]), a = zufall([-2, -1, 1, 2]);
          var w = []; for (var i = 0; i < k; i++) w.push(p[0]); for (i = 0; i < m; i++) w.push(p[1]);
          return { a: a, w: mischen(w), k: k, p: p[0],
            richtig: k === 1 ? 'schneidet der Graph die x-Achse' : k === 2 ? 'berührt der Graph die x-Achse' : 'schneidet der Graph mit Terrasse',
            text: 'Was tut der Graph von \\(f(x) = ' + faktT(a, w) + '\\) an der Stelle \\(x = ' + tz(p[0]) + '\\)?' }; },
        fehler: function(A){ return [[{ v: A.k === 2 ? 'schneidet der Graph die x-Achse' : 'berührt der Graph die x-Achse' }, 'Exponent']]; },
        pruefen: function(A, e){
          if (e.v === A.richtig) return null;
          return 'Schau auf den Exponenten des Faktors \\(' + klT(A.p) + '\\): \\(' + A.k + '\\) ist '
            + (A.k % 2 ? 'ungerade — das Vorzeichen wechselt' : 'gerade — das Vorzeichen wechselt nicht')
            + (A.k === 3 ? ', und bei 3 wird der Graph dort flach.' : A.k === 1 ? '. Flach (Terrasse) wird der Graph erst bei Vielfachheit 3.' : '.'); },
        loesung: function(A){ return klT(A.p) + (A.k > 1 ? '^{' + A.k + '}' : '') + ':\\ \\text{' + A.richtig.replace('der Graph ', '') + '}'; } },

      'graf-vielfachheit': { felder: ['b', 's'], muster: 'berührt bei x = {b}   schneidet bei x = {s}', graf: 'vielfach',
        eingabe: function(A){ return { b: String(A.b), s: String(A.s) }; },
        // Abstand der Nullstellen mindestens 2 — bei Abstand 1 wäre der Buckel 1–2 px hoch.
        neu: function(){ var p; do { p = ziehe(bereich(-2, 2), 2); } while (Math.abs(p[0] - p[1]) < 2);
          var a = zufall([-0.5, 0.5, -1, 1]);
          return { a: a, b: p[0], s: p[1], w: [p[0], p[0], p[1]],
            text: 'An welcher Stelle berührt der Graph die \\(x\\)-Achse, an welcher schneidet er sie? (Nullstellen auf Gitterpunkten)' }; },
        fehler: function(A){ return [[{ b: String(A.s), s: String(A.b) }, 'Vertauscht']]; },
        pruefen: function(A, e){
          if (gl(e.b, A.b) && gl(e.s, A.s)) return null;
          if (gl(e.b, A.s) && gl(e.s, A.b)) return 'Vertauscht: Beim Berühren bleibt der Graph auf derselben Seite der \\(x\\)-Achse, beim Schneiden wechselt er.';
          return 'Such die beiden Stellen, an denen der Graph die \\(x\\)-Achse trifft. Wechselt er dort die Seite oder nicht?'; },
        loesung: function(A){ return '\\text{berührt bei } ' + tz(A.b) + ',\\ \\text{schneidet bei } ' + tz(A.s) + ':\\ f(x) = ' + faktT(A.a, A.w); } },

      'gleichung-mehrfach': { felder: ['a'], muster: 'a = {a}',
        eingabe: function(A){ return { a: String(A.a) }; },
        // Doppelte Nullstelle ±2 oder ±3: Bei ±1 gäbe das vergessene Quadrat dasselbe (oder −a).
        neu: function(){ var d = zufall([-3, -2, 2, 3]), p = [d, zufall(bereich(-3, 3, [0, d]))], a = zufall([-2, -1, -0.5, 0.5, 1, 2]);
          var prod = p[0] * p[0] * (-p[1]);
          if (Math.abs(a * prod) > 60) a = prod > 0 ? 0.5 : -0.5;
          return { a: a, w: [p[0], p[0], p[1]], d: p[0], e: p[1], prod: prod, f0: a * prod,
            text: 'Grad 3, doppelte Nullstelle \\(' + tz(p[0]) + '\\), einfache Nullstelle \\(' + tz(p[1]) + '\\), Graph durch \\((0 \\mid ' + tz(a * prod) + ')\\). '
              + 'Bestimme \\(a\\) in \\(f(x) = a' + klT(p[0]) + '^2' + klT(p[1]) + '\\).' }; },
        fehler: function(A){ var f = [[{ a: String(-A.a) }, 'Vorzeichen']];
          var ohneQ = A.f0 / (-A.d * -A.e);                               // Quadrat vergessen
          if (!gl(ohneQ, A.a) && !gl(ohneQ, -A.a)) f.push([{ a: String(ohneQ) }, 'Quadrat']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, -A.a)) return 'Vorzeichen: \\(' + klT(A.d) + '^2\\) ist bei \\(x = 0\\) positiv, nur \\(' + klT(A.e) + '\\) bringt ein Vorzeichen.';
          if (gl(e.a, A.f0 / (A.d * A.e))) return 'Das Quadrat fehlt: Der Faktor \\(' + klT(A.d) + '\\) steht zweimal drin.';
          return 'Setz \\(x = 0\\) ein: \\(f(0) = a \\cdot (' + tz(-A.d) + ')^2 \\cdot (' + tz(-A.e) + ') = ' + tz(A.prod) + 'a\\).'; },
        loesung: function(A){ return tz(A.prod) + 'a = ' + tz(A.f0) + ' \\Rightarrow a = ' + tz(A.a); } },

      /* ── Kapitel 3: Globalverlauf ────────────────────────────── */
      'enden': { felder: ['v'], muster: 'Der Graph verläuft {v:von links unten nach rechts oben|von links oben nach rechts unten|mit beiden Enden nach oben|mit beiden Enden nach unten}',
        eingabe: function(A){ return { v: A.richtig }; },
        neu: function(){ var n = zufall([2, 3, 4, 5, 6]), an = zufall([-3, -2, -1, -0.5, 0.5, 1, 2, 3]);
          var c = [an]; for (var i = 1; i <= n; i++) c.push(Math.random() < 0.5 ? 0 : zufall([-7, -5, -4, -3, -1, 1, 2, 3, 6, 8]));
          // Der Leitterm steht nicht immer vorne — sonst übt man nur das erste Zeichen.
          var terme = c.map(function(k, i){ return [k, n - i]; }).filter(function(t){ return t[0] !== 0; });
          var vorne = terme.length > 1 && Math.random() < 0.5;
          if (vorne) terme.push(terme.shift());
          var s = '';
          terme.forEach(function(t){ var b = Math.abs(t[0]), zahl = (b === 1 && t[1] > 0) ? '' : String(b), pot = t[1] === 0 ? '' : t[1] === 1 ? 'x' : 'x^{' + t[1] + '}';
            s += s ? (t[0] < 0 ? ' - ' : ' + ') + zahl + pot : (t[0] < 0 ? '-' : '') + zahl + pot; });
          var r = n % 2 ? (an > 0 ? 'von links unten nach rechts oben' : 'von links oben nach rechts unten') : (an > 0 ? 'mit beiden Enden nach oben' : 'mit beiden Enden nach unten');
          return { n: n, an: an, richtig: r, text: 'Wie verläuft der Graph von \\(f(x) = ' + s + '\\) global?' }; },
        fehler: function(A){ return [[{ v: A.n % 2 ? (A.an > 0 ? 'mit beiden Enden nach oben' : 'mit beiden Enden nach unten') : (A.an > 0 ? 'von links unten nach rechts oben' : 'von links oben nach rechts unten') }, 'Grad']]; },
        pruefen: function(A, e){
          if (e.v === A.richtig) return null;
          var parit = /beiden/.test(e.v) !== (A.n % 2 === 0);
          return parit ? 'Schau auf den Grad: \\(' + A.n + '\\) ist ' + (A.n % 2 ? 'ungerade — die Enden zeigen in entgegengesetzte Richtungen.' : 'gerade — beide Enden zeigen in dieselbe Richtung.')
                       : 'Schau auf das Vorzeichen des Leitkoeffizienten \\(' + tz(A.an) + '\\) — er steht beim höchsten Exponenten, nicht unbedingt vorne.'; },
        loesung: function(A){ return '\\text{Grad } ' + A.n + ',\\ a_n = ' + tz(A.an) + ':\\ \\text{' + A.richtig + '}'; } },

      'hoechstzahl': { felder: ['N', 'E'], muster: 'höchstens {N} Nullstellen, höchstens {E} Extremstellen',
        eingabe: function(A){ return { N: String(A.n), E: String(A.n - 1) }; },
        neu: function(){ var n = zufall([2, 3, 4, 5, 6, 7]);
          return { n: n, text: 'Eine Polynomfunktion hat den Grad \\(' + n + '\\). Wie viele Nullstellen und wie viele lokale Extremstellen kann sie höchstens haben?' }; },
        fehler: function(A){ return [[{ N: String(A.n), E: String(A.n) }, 'n − 1'], [{ N: String(A.n - 1), E: String(A.n - 1) }, 'Nullstellen']]; },
        pruefen: function(A, e){
          if (gl(e.N, A.n) && gl(e.E, A.n - 1)) return null;
          var r = [];
          if (!gl(e.N, A.n)) r.push('Nullstellen: höchstens so viele wie der Grad.');
          if (!gl(e.E, A.n - 1)) r.push('Extremstellen: höchstens eine weniger als der Grad, also n − 1.');
          return r.join(' '); },
        loesung: function(A){ return '\\le ' + A.n + ' \\text{ Nullstellen},\\ \\le ' + (A.n - 1) + ' \\text{ Extremstellen}'; } },

      'symmetrie-poly': { felder: ['s'], muster: 'Der Graph ist {s:achsensymmetrisch zur y-Achse|punktsymmetrisch zum Ursprung|weder noch}',
        eingabe: function(A){ return { s: A.richtig }; },
        neu: function(){ var art = zufall(['g', 'u', 'w']), ex;
          if (art === 'g') ex = ziehe([0, 2, 4, 6], zufall([2, 3]));
          else if (art === 'u') ex = ziehe([1, 3, 5, 7], zufall([2, 3]));
          else ex = ziehe([0, 1, 2, 3, 4, 5], 3);
          ex.sort(function(u, v){ return v - u; });
          var gerade = ex.every(function(e){ return e % 2 === 0; }), ungerade = ex.every(function(e){ return e % 2 === 1; });
          var n = ex[0], c = []; for (var i = 0; i <= n; i++) c.push(0);
          ex.forEach(function(e){ c[n - e] = zufall([-5, -3, -2, -1, 1, 2, 4, 7]); });
          return { ex: ex, konst: ex.indexOf(0) >= 0,
            richtig: gerade ? 'achsensymmetrisch zur y-Achse' : ungerade ? 'punktsymmetrisch zum Ursprung' : 'weder noch',
            text: 'Welche Symmetrie hat der Graph von \\(f(x) = ' + sumT(c) + '\\)?' }; },
        fehler: function(A){ return [[{ s: A.richtig === 'weder noch' ? 'punktsymmetrisch zum Ursprung' : 'weder noch' }, 'Exponent']]; },
        pruefen: function(A, e){
          if (e.s === A.richtig) return null;
          if (A.konst && e.s !== 'achsensymmetrisch zur y-Achse') return 'Das konstante Glied ist ein Term mit \\(x^0\\) — und \\(0\\) ist gerade. Schau alle Exponenten an: \\(' + A.ex.join(',\\ ') + '\\).';
          return 'Schau alle Exponenten an: \\(' + A.ex.join(',\\ ') + '\\). Nur gerade → achsensymmetrisch zur \\(y\\)-Achse, nur ungerade → punktsymmetrisch zum Ursprung, gemischt → weder noch.'; },
        loesung: function(A){ return '\\text{Exponenten } ' + A.ex.join(',\\ ') + ':\\ \\text{' + A.richtig + '}'; } },

      /* ── Kapitel 4: Nullstellen berechnen ────────────────────── */
      'ausklammern': { felder: ['x1', 'x2', 'x3'], muster: 'Nullstellen: {x1}  {x2}  {x3}',
        eingabe: function(A){ return { x1: '0', x2: String(A.w[1]), x3: String(A.w[2]) }; },
        neu: function(){ var p = ziehe(bereich(-6, 6, [0]), 2), w = [0, p[0], p[1]];
          return { a: 1, w: w, c: ausWurzeln(1, w),
            text: 'Berechne alle Nullstellen von \\(f(x) = ' + sumT(ausWurzeln(1, w)) + '\\) (Reihenfolge egal).' }; },
        fehler: function(A){ return [[{ x1: String(-A.w[1]), x2: String(-A.w[2]), x3: '0' }, 'Vorzeichen']]
          .filter(function(p){ return !gleich(A, p[0]); }); },
        pruefen: function(A, e){
          var ein = [e.x1, e.x2, e.x3];
          if (gleich(A, e)) return null;
          if (!ein.some(function(x){ return gl(x, 0); })) return 'Nach dem Ausklammern steht \\(x \\cdot (\\dots) = 0\\) — der Faktor \\(x\\) liefert die Nullstelle \\(0\\).';
          if (ein.some(function(x){ return !gl(x, 0) && A.w.indexOf(-x) >= 0 && A.w.indexOf(x) < 0; }))
            return 'Vorzeichen: Faktorisier die Klammer \\(' + sumT([1, A.c[1], A.c[2]]) + '\\) und setz jeden Faktor null.';
          return '\\(x\\) ausklammern, dann die Nullstellen der Klammer suchen: zwei Zahlen mit Produkt \\(' + tz(A.c[2]) + '\\) und Summe \\(' + tz(-A.c[1]) + '\\).'; },
        loesung: function(A){ return sumT(A.c) + ' = x' + klT(A.w[1]) + klT(A.w[2]) + ' \\Rightarrow x \\in \\{0;\\ ' + tz(A.w[1]) + ';\\ ' + tz(A.w[2]) + '\\}'; } },

      'probe-teiler': { felder: ['y'], muster: 'f(r) = {y}',
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){ var w = ziehe(bereich(-3, 3, [0]), 3), c = ausWurzeln(1, w);
          // Nur echte Teiler von a₀ — das ist das gelehrte Verfahren.
          var a0 = Math.abs(c[3]), t = zufall([1, 2, 3, 4, 6, 9].filter(function(q){ return a0 % q === 0; })) * zufall([1, -1]);
          return { a: 1, w: w, c: c, r: t, y: wert(c, t),
            text: 'Prüfe, ob \\(' + tz(t) + '\\) eine Nullstelle von \\(f(x) = ' + sumT(c) + '\\) ist: Berechne \\(f(' + tz(t) + ')\\).' }; },
        fehler: function(A){ var f = [], b = wert(A.c, -A.r);
          if (!gl(b, A.y)) f.push([{ y: String(b) }, 'eingesetzt']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, wert(A.c, -A.r))) return 'Du hast \\(' + tz(-A.r) + '\\) eingesetzt statt \\(' + tz(A.r) + '\\). Klammer um die negative Zahl!';
          return 'Rechne Term für Term: \\((' + tz(A.r) + ')^3\\), dann \\((' + tz(A.r) + ')^2\\) mal den Koeffizienten, und so weiter.'; },
        richtig: function(A){ return A.y === 0 ? '— also ist ' + z(A.r) + ' eine Nullstelle.' : '— nicht null, also keine Nullstelle.'; },
        loesung: function(A){ return 'f(' + tz(A.r) + ') = ' + tz(A.y) + (A.y === 0 ? ' \\Rightarrow \\text{Nullstelle}' : ' \\ne 0'); } },

      /* Abspalten über Ansatz und Koeffizientenvergleich (das Verfahren des Leitprogramms;
         die Polynomdivision steht auf der Themenseite): (x − r)(x² + px + q) mit
         p = a₂ + r und q = −a₀ / r. Gefragt ist der Quotient, nicht nur die Nullstellen. */
      'abspalten': { felder: ['p', 'q'], muster: 'Quotient x² + {p}·x + {q}',
        eingabe: function(A){ return { p: String(A.p), q: String(A.q) }; },
        neu: function(){ var w = ziehe(bereich(-4, 4, [0]), 3), c = ausWurzeln(1, w), qq = teilen(c, w[0]).q;
          return { a: 1, w: w, c: c, r: w[0], p: qq[1], q: qq[2],
            text: '\\(x_1 = ' + tz(w[0]) + '\\) ist eine Nullstelle von \\(f(x) = ' + sumT(c) + '\\). Bestimme \\(p\\) und \\(q\\) im Ansatz \\(f(x) = '
              + klT(w[0]) + '(x^2 + px + q)\\).' }; },
        fehler: function(A){ var f = [], p2 = A.c[1] - A.r, q2 = A.c[3] / A.r;      // Vorzeichen von r falsch übernommen
          if (!gl(p2, A.p)) f.push([{ p: String(p2), q: String(A.q) }, 'Vorzeichen']);
          if (!gl(q2, A.q)) f.push([{ p: String(A.p), q: String(q2) }, 'konstante']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.p, A.p) && gl(e.q, A.q)) return null;
          var r = [];
          if (!gl(e.p, A.p)) r.push(gl(e.p, A.c[1] - A.r) ? 'Vorzeichen beim \\(x^2\\)-Glied: Ausmultipliziert steht dort \\(p ' + (A.r > 0 ? '- ' + A.r : '+ ' + (-A.r)) + '\\), und das muss \\(' + tz(A.c[1]) + '\\) sein.'
                                                      : 'Multiplizier \\(' + klT(A.r) + '(x^2 + px + q)\\) aus und vergleich das \\(x^2\\)-Glied.');
          if (!gl(e.q, A.q)) r.push('Das konstante Glied: ausmultipliziert \\(' + tz(-A.r) + ' \\cdot q\\), und das muss \\(' + tz(A.c[3]) + '\\) sein.');
          return r.join(' '); },
        richtig: function(A){ return '— der Quotient ist \\(' + sumT([1, A.p, A.q]) + ' = ' + klT(A.w[1]) + klT(A.w[2]) + '\\), also sind \\(' + tz(A.w[1]) + '\\) und \\(' + tz(A.w[2]) + '\\) die anderen Nullstellen.'; },
        loesung: function(A){ return sumT(A.c) + ' = ' + klT(A.r) + '(' + sumT([1, A.p, A.q]) + ')'; } },

      /* ── Kapitel 5: Hoch- und Tiefpunkte ─────────────────────── */
      'extrem-ablesen': { felder: ['hx', 'hy', 'tx', 'ty'], muster: 'H( {hx} | {hy} )   T( {tx} | {ty} )', graf: 'extrem',
        schl: function(A){ return ['e', A.s, A.q, A.u, A.v].join('|'); },
        eingabe: function(A){ return { hx: String(A.hx), hy: String(A.hy), tx: String(A.tx), ty: String(A.ty) }; },
        neu: function(){ var s = zufall([1, -1]), u = zufall(bereich(-2, 2)), v = zufall(bereich(-2, 2)), q = zufall([1, 0.5]);
          // f(x) = s·q·((x−u)³ − 3(x−u)) + v: Extremstellen bei u ± 1, Werte v ± 2q
          return { s: s, u: u, v: v, q: q, hx: u - s, hy: v + 2 * q, tx: u + s, ty: v - 2 * q,
            text: 'Lies Hochpunkt und Tiefpunkt am Graphen ab (sie liegen auf Gitterpunkten).' }; },
        fehler: function(A){ return [[{ hx: String(A.tx), hy: String(A.ty), tx: String(A.hx), ty: String(A.hy) }, 'Vertauscht']]; },
        pruefen: function(A, e){
          if (gl(e.hx, A.hx) && gl(e.hy, A.hy) && gl(e.tx, A.tx) && gl(e.ty, A.ty)) return null;
          if (gl(e.hx, A.tx) && gl(e.hy, A.ty)) return 'Vertauscht: Der Hochpunkt ist der lokal höchste Punkt — dort wechselt der Graph von steigend zu fallend.';
          var hOk = gl(e.hx, A.hx) && gl(e.hy, A.hy), tOk = gl(e.tx, A.tx) && gl(e.ty, A.ty);
          if (!hOk && A.hx !== A.hy && gl(e.hx, A.hy) && gl(e.hy, A.hx)) return 'Beim Hochpunkt: erst die \\(x\\)-Koordinate, dann die \\(y\\)-Koordinate.';
          if (hOk && A.tx !== A.ty && gl(e.tx, A.ty) && gl(e.ty, A.tx)) return 'Beim Tiefpunkt: erst die \\(x\\)-Koordinate, dann die \\(y\\)-Koordinate.';
          if (hOk && !tOk) return 'Der Hochpunkt stimmt. Lies den Tiefpunkt nochmals ab — dort wechselt der Graph von fallend zu steigend.';
          if (tOk && !hOk) return 'Der Tiefpunkt stimmt. Lies den Hochpunkt nochmals ab — dort wechselt der Graph von steigend zu fallend.';
          return 'Such die beiden Stellen, an denen der Graph die Richtung wechselt, und lies je \\(x\\) und \\(y\\) ab.'; },
        loesung: function(A){ return 'H(' + tz(A.hx) + ' \\mid ' + tz(A.hy) + '),\\ T(' + tz(A.tx) + ' \\mid ' + tz(A.ty) + ')'; } },

      'scheitel-extrem': { felder: ['xs', 'ys', 'art'], muster: 'xₛ = {xs}   yₛ = {ys}   {art:Hochpunkt|Tiefpunkt}',
        schl: function(A){ return ['s', A.a, A.b, A.c].join('|'); },
        eingabe: function(A){ return { xs: String(A.xs), ys: String(A.ys), art: A.a < 0 ? 'Hochpunkt' : 'Tiefpunkt' }; },
        neu: function(){ var a = zufall([-2, -1, 1, 2]), xs = zufall(bereich(-4, 4, [0])), ys = zufall(bereich(-6, 6));
          var b = -2 * a * xs, c = a * xs * xs + ys;
          return { a: a, b: b, c: c, xs: xs, ys: ys,
            text: 'Berechne den Extrempunkt von \\(f(x) = ' + sumT([a, b, c]) + '\\). Hoch- oder Tiefpunkt?' }; },
        fehler: function(A){ return [[{ xs: String(-A.xs), ys: String(A.ys), art: A.a < 0 ? 'Hochpunkt' : 'Tiefpunkt' }, 'Minus'],
                                     [{ xs: String(A.xs), ys: String(A.ys), art: A.a < 0 ? 'Tiefpunkt' : 'Hochpunkt' }, 'Vorzeichen von']]; },
        pruefen: function(A, e){
          var art = A.a < 0 ? 'Hochpunkt' : 'Tiefpunkt', r = [];
          if (gl(e.xs, A.xs) && gl(e.ys, A.ys) && e.art === art) return null;
          if (!gl(e.xs, A.xs)) r.push(gl(e.xs, -A.xs) ? 'Das Minus in \\(x_s = -\\frac{b}{2a}\\) nicht vergessen.' : '\\(x_s = -\\frac{b}{2a} = -\\frac{' + tz(A.b) + '}{' + tz(2 * A.a) + '}\\).');
          else if (!gl(e.ys, A.ys)) r.push('\\(y_s = f(x_s)\\): Setz \\(x_s = ' + tz(A.xs) + '\\) in \\(f\\) ein.');
          if (e.art !== art) r.push('Schau auf das Vorzeichen von \\(a\\): ' + (A.a > 0 ? 'positiv heisst nach oben geöffnet, also Tiefpunkt.' : 'negativ heisst nach unten geöffnet, also Hochpunkt.'));
          return r.join(' '); },
        loesung: function(A){ return 'x_s = -\\frac{' + tz(A.b) + '}{' + tz(2 * A.a) + '} = ' + tz(A.xs) + ',\\ y_s = f(' + tz(A.xs) + ') = ' + tz(A.ys) + ':\\ ' + (A.a < 0 ? 'H' : 'T') + '(' + tz(A.xs) + ' \\mid ' + tz(A.ys) + ')'; } },

      'lokal-global': { felder: ['wo'], muster: 'Das absolute Maximum liegt {wo:im Hochpunkt|am linken Rand|am rechten Rand}',
        schl: function(A){ return ['l', A.s, A.l, A.r].join('|'); },
        eingabe: function(A){ return { wo: A.richtig }; },
        neu: function(){ var s = zufall([1, -1]), l = zufall([-2.5, -1.5, -0.5]), r = zufall([0.5, 1.5, 2.5]);
          if (s < 0){ var t = l; l = -r; r = -t; }
          var f = function(x){ return s * (x * x * x - 3 * x); }, hx = -s;
          var kand = [['am linken Rand', f(l)], ['am rechten Rand', f(r)]];
          if (hx > l && hx < r) kand.push(['im Hochpunkt', 2]);
          kand.sort(function(p, q){ return q[1] - p[1]; });
          return { s: s, l: l, r: r, hx: hx, fl: f(l), fr: f(r), richtig: kand[0][0], hin: hx > l && hx < r,
            text: '\\(f(x) = ' + (s > 0 ? '' : '-(') + 'x^3 - 3x' + (s > 0 ? '' : ')') + '\\) hat den Hochpunkt \\(H(' + tz(hx) + ' \\mid 2)\\). '
              + 'Wo liegt das absolute Maximum auf \\(D = [' + tz(l) + ';\\, ' + tz(r) + ']\\)?' }; },
        fehler: function(A){ return [[{ wo: A.richtig === 'im Hochpunkt' ? 'am rechten Rand' : 'im Hochpunkt' }, A.richtig === 'im Hochpunkt' ? 'Rechne' : (A.hin ? 'Rechne' : 'liegt nicht')]]; },
        pruefen: function(A, e){
          if (e.wo === A.richtig) return null;
          if (e.wo === 'im Hochpunkt' && !A.hin) return 'Der Hochpunkt liegt bei \\(x = ' + tz(A.hx) + '\\) — der liegt nicht in \\(D\\).';
          return 'Rechne die Randwerte aus: \\(f(' + tz(A.l) + ') = ' + tz(A.fl) + '\\), \\(f(' + tz(A.r) + ') = ' + tz(A.fr) + '\\)' + (A.hin ? ', und vergleich mit dem Hochpunkt (2).' : '.'); },
        loesung: function(A){ return 'f(' + tz(A.l) + ') = ' + tz(A.fl) + ',\\ f(' + tz(A.r) + ') = ' + tz(A.fr) + (A.hin ? ',\\ f(' + tz(A.hx) + ') = 2' : '') + ':\\ \\text{' + A.richtig + '}'; } }
    };
    function gleicheMenge2(a, b){
      var u = a.slice().sort(function(p, q){ return p - q; }), v = b.slice().sort(function(p, q){ return p - q; });
      return u.length === v.length && u.every(function(x, i){ return gl(x, v[i]); });
    }
    function gleich(A, e){ return gleicheMenge2([+e.x1, +e.x2, +e.x3], A.w); }

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie'), bild = box.querySelector('.ue-bild');
      function neu(){
        // Trifft der Wurf ein Polynom, nach dem eine feste Aufgabe fragt, wird neu
        // gewürfelt (FEST oben). 40 Versuche reichen weit; danach gilt der letzte Wurf.
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
          if (T.graf === 'vielfach'){
            var K = Achsen(bild, { w: 170, h: 170, x0: -4, x1: 4, y0: -6, y1: 6, r: 3.5, pfeil: 6, xm: [-2, 2], ym: [-4, 4], sy: 2 });
            K.kurve(function(x){ return wert(ausWurzeln(A.a, A.w), x); }, 'kurve');
          } else if (T.graf === 'extrem'){
            var y0 = A.v - 2 * A.q - 3, y1 = A.v + 2 * A.q + 3;
            var ya = Math.min(y0, -1), yb = Math.max(y1, 1), xmk = [], ymk = [];
            for (var t = Math.ceil(A.u - 3); t < A.u + 3; t++) if (t !== 0 && t % 2 === 0) xmk.push(t);
            for (t = Math.ceil(ya); t < yb; t++) if (t !== 0 && t % 2 === 0) ymk.push(t);
            var K2 = Achsen(bild, { w: 170, h: 170, x0: A.u - 3, x1: A.u + 3, y0: ya, y1: yb, r: 3.5, pfeil: 6, xm: xmk, ym: ymk });
            K2.kurve(function(x){ var t = x - A.u; return A.s * A.q * (t * t * t - 3 * t) + A.v; }, 'kurve');
          }
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

  /* ---------- Minigrafen: <svg class="mini" data-p="a;x1,x2,…" (Linearfaktoren) oder
       data-c="aₙ,…,a₀" (Summenform), data-fenster data-punkte data-titel data-xname data-yname> ---------- */
  document.querySelectorAll('svg.mini[data-p], svg.mini[data-c]').forEach(function(svg){
    // data-c="aₙ,…,a₀": Summenform, wo die Nullstellen keine schönen Zahlen sind.
    var c;
    if (svg.dataset.c) c = svg.dataset.c.split(',').map(Number);
    else { var teile = svg.dataset.p.split(';'); c = ausWurzeln(+teile[0], teile[1] ? teile[1].split(',').map(Number) : []); }
    var fe = (svg.dataset.fenster || '-4,4,-6,6').split(',').map(Number);
    var w_ = 150, h = 150;
    svg.setAttribute('viewBox', '0 0 150 150'); svg.setAttribute('role', 'img');
    var sy = (fe[3] - fe[2]) > 20 ? 5 : (fe[3] - fe[2]) > 12 ? 2 : 1;
    var K = Achsen(svg, { w: w_, h: h, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, xm: [1], ym: [sy], sy: sy, pfeil: 6,
      xname: svg.dataset.xname, yname: svg.dataset.yname });
    K.kurve(function(x){ return wert(c, x); }, 'kurve');
    // Markierte Punkte sind neutral — abgelesene Gitterpunkte; orange bleibt den Nullstellen.
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){
      var q = p.split(',').map(Number);
      K.punkt(q[0], q[1], q[1] === 0 ? 'p-ns' : 'p-pkt');
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
