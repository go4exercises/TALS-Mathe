<script>
/* Leitprogramm Quadratische Funktionen — Simulationen mit Aufgabenleiste, Übungen
   mit Rückmeldung, Minigrafen. Notation wie im RLP-nahen Leitprogramm: Scheitel
   S(x_s | y_s) (Entscheid 02.10.2026; die Themenseite schreibt u, v). Achsen,
   Farben und Startwerte wie auf Themenseite 3.3 bzw. wie im Clip davor.
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
        var d = '', A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 240; k++){ var x = A + (B - A) * k / 240, y = Math.max(y0 - 3 * (y1 - y0), Math.min(y1 + 3 * (y1 - y0), f(x)));
          d += (d ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); }
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
  var FENSTER = { w: 300, h: 300, x0: -7.5, x1: 7.5, y0: -7.5, y1: 7.5, xm: [-5, 5], ym: [-5, 5] };

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  function werte(r){ var w = {}; for (var k in r){ w[k] = +r[k].value; r[k].parentNode.querySelector('.sl-val').textContent = z(w[k]); } return w; }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function kl(x){ return Math.abs(x) < 1e-9 ? 'x' : '(x ' + (x > 0 ? '− ' : '+ ') + z(Math.abs(x)) + ')'; }
  function scheitelText(a, xs, ys){
    var k = xs === 0 ? 'x²' : '(x ' + (xs > 0 ? '− ' : '+ ') + sp('tx-orange', z(Math.abs(xs))) + ')²';
    return sp('tx-blau', z(a)) + '·' + k + (ys === 0 ? '' : ' ' + (ys > 0 ? '+ ' : '− ') + sp('tx-gruen', z(Math.abs(ys))));
  }
  function grundText(a, b, c){
    var s = (a === 1 ? '' : a === -1 ? '−' : z(a)) + 'x²';
    if (b) s += (b > 0 ? ' + ' : ' − ') + (Math.abs(b) === 1 ? '' : z(Math.abs(b))) + 'x';
    if (c) s += (c > 0 ? ' + ' : ' − ') + z(Math.abs(c));
    return s;
  }

  /* ---------- Aufgabenleiste in der Simulation ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «Nächste» geht
     immer — wer hängt, soll nicht festsitzen. */
  function Leiste(fig, aufgaben, sim){
    var box = fig.querySelector('.leiste'); if (!box) return function(){};
    var i = 0, erledigt = {};
    box.innerHTML = '<span class="ls-nr"></span><span class="ls-text"></span><span class="ls-ok" aria-live="polite"></span><button type="button" class="ls-weiter"></button>';
    var nr = box.querySelector('.ls-nr'), tx = box.querySelector('.ls-text'), ok = box.querySelector('.ls-ok'), bt = box.querySelector('.ls-weiter');
    function zeigen(){
      if (i >= aufgaben.length){ nr.textContent = '✓'; tx.innerHTML = 'Alle Aufgaben gelöst — weiter mit dem Kontrollclip.'; ok.textContent = ''; bt.textContent = 'nochmals'; box.classList.add('fertig'); return; }
      box.classList.remove('fertig');
      nr.textContent = (i + 1) + '/' + aufgaben.length; tx.innerHTML = aufgaben[i].text; setzen(tx);
      if (aufgaben[i].setup) aufgaben[i].setup(sim);
      pruefen();
    }
    function pruefen(){
      if (i >= aufgaben.length) return;
      var gut = !!aufgaben[i].ok(sim.zustand());
      if (gut) erledigt[i] = true;
      ok.textContent = erledigt[i] ? '✓' : '';
      bt.textContent = erledigt[i] ? 'Nächste ▶' : 'überspringen';
      box.classList.toggle('geloest', !!erledigt[i]);
    }
    bt.addEventListener('click', function(){
      if (i >= aufgaben.length){ i = 0; erledigt = {}; } else i++;
      if (sim.aufraeumen) sim.aufraeumen();
      zeigen(); if (sim.zeichnen) sim.zeichnen();
    });
    setTimeout(zeigen, 0);
    return pruefen;
  }

  /* ---------- Kapitel 1: Parabel bewegen ---------- */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r); return { a: w.a, xs: w.xs, ys: w.ys, ziel: ziel, bewegt: bewegt }; },
                zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), a = w.a, xs = w.xs, ys = w.ys;
      K.leeren();
      K.kurve(function(x){ return x * x; }, 'normal hilfslinie');
      if (ziel) K.kurve(function(x){ return ziel[0] * (x - ziel[1]) * (x - ziel[1]) + ziel[2]; }, 'zielkurve');
      K.kurve(function(x){ return a * (x - xs) * (x - xs) + ys; }, 'kurve');
      if (a !== 0) K.punkt(xs, ys, 'p-s', 'S(' + z(xs) + ' | ' + z(ys) + ')', xs > 3 ? -8 : 8, a > 0 ? 18 : -10, xs > 3 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML = a === 0 ? 'a = 0: keine Parabel' : 'f(x) = ' + scheitelText(a, xs, ys);
      pruefen();
    }
    function zielAufgabe(t){ return { text: 'Triff die grüne Parabel.', setup: function(){ ziel = t; }, ok: function(s){ return s.a === t[0] && s.xs === t[1] && s.ys === t[2]; } }; }
    function bau(a, xs, ys, tex){ return { text: 'Bau nach: \\(f(x) = ' + tex + '\\)', ok: function(s){ return s.a === a && s.xs === xs && s.ys === ys; } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an allen drei Reglern und beobachte, was sich ändert.', ok: function(s){ return s.bewegt.a && s.bewegt.xs && s.bewegt.ys; } },
      bau(1, 0, -3, 'x^2 - 3'), bau(1, -2, 0, '(x + 2)^2'), bau(-1, 1, 4, '-(x - 1)^2 + 4'), bau(0.5, -3, -2, '0.5\\,(x + 3)^2 - 2'),
      zielAufgabe([1, -3, 2]), zielAufgabe([-1, 1, 4]), zielAufgabe([0.5, 2, -3])
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: drei Formen ---------- */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), aktiv = null, pruefen = function(){};
    var r = regler(fig, zeichnen);
    var sim = { zustand: function(){ var w = werte(r); return { a: w.a, xs: w.xs, ys: w.ys, aktiv: aktiv }; }, zeichnen: zeichnen };
    fig.querySelectorAll('[data-form]').forEach(function(k){
      k.addEventListener('click', function(){ aktiv = aktiv === k.dataset.form ? null : k.dataset.form; zeichnen(); });
    });
    function zeichnen(){
      var w = werte(r), a = w.a, xs = w.xs, ys = w.ys, b = -2 * a * xs, c = a * xs * xs + ys;
      fig.querySelectorAll('[data-form]').forEach(function(k){ k.classList.toggle('aktiv', k.dataset.form === aktiv); });
      K.leeren(); K.kurve(function(x){ return a * (x - xs) * (x - xs) + ys; }, 'kurve');
      var zeig = function(f){ return !aktiv || aktiv === f; };
      if (a === 0){ ['g', 's', 'p'].forEach(function(f){ rolle(fig, f).textContent = '—'; }); pruefen(); return; }
      var gGenau = [b, c].every(function(x){ return Math.abs(x * 100 - Math.round(x * 100)) < 1e-6; });
      rolle(fig, 'g').innerHTML = (gGenau ? '' : '≈ ') + grundText(a, b, c);
      rolle(fig, 's').innerHTML = scheitelText(a, xs, ys);
      var q = -ys / a, nst = q > 1e-12 ? [xs - Math.sqrt(q), xs + Math.sqrt(q)] : (Math.abs(q) < 1e-12 ? [xs, xs] : []);
      if (nst.length){
        var genau = nst.every(function(x){ return Math.abs(x * 100 - Math.round(x * 100)) < 1e-6; });
        rolle(fig, 'p').innerHTML = (genau ? '' : '≈ ') + z(a) + '·' + (nst[0] === nst[1] ? kl(nst[0]) + '²' : kl(nst[0]) + kl(nst[1]));
      } else rolle(fig, 'p').innerHTML = '<em>gibt es nicht</em>';
      // Punkte immer, Koordinaten erst, wenn die zugehörige Form angeklickt ist
      if (zeig('g')) K.punkt(0, c, 'p-c', aktiv === 'g' ? '(0 | ' + (Math.abs(c * 100 - Math.round(c * 100)) < 1e-6 ? '' : '≈ ') + z(c) + ')' : null);
      if (zeig('s')) K.punkt(xs, ys, 'p-s', aktiv === 's' ? 'S(' + z(xs) + ' | ' + z(ys) + ')' : null, xs > 3 ? -8 : 8, a > 0 ? 18 : -10, xs > 3 ? 'end' : 'start');
      if (zeig('p')) nst.forEach(function(x, i){
        K.punkt(x, 0, 'p-null', aktiv === 'p' ? '(' + z(x) + ' | 0)' : null, i === 0 && nst.length > 1 ? -6 : 6, a > 0 ? -8 : 16, i === 0 && nst.length > 1 ? 'end' : 'start');
      });
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Klick die <b>Grundform</b> an. Wo im Bild siehst du \\(c\\)?', ok: function(s){ return s.aktiv === 'g'; } },
      { text: 'Klick die <b>Scheitelform</b> an. Wo im Bild siehst du den Scheitelpunkt?', ok: function(s){ return s.aktiv === 's'; } },
      { text: 'Klick die <b>Produktform</b> an. Wo im Bild siehst du die Nullstellen?', ok: function(s){ return s.aktiv === 'p'; } },
      { text: 'Schieb \\(y_s\\) über \\(0\\). Was passiert mit der Produktform?', ok: function(s){ return s.a > 0 && s.ys > 0; } },
      { text: 'Stell \\(x_s = 0\\). Was fehlt jetzt in der Grundform?', ok: function(s){ return s.xs === 0 && s.a !== 0; } },
      { text: 'Stell \\(-x^2 - 2x + 3\\) ein.', ok: function(s){ return s.a === -1 && s.xs === -1 && s.ys === 4; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: b und c, Symmetrieachse und D (a = 1) ---------- */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), pruefen = function(){};
    var r = regler(fig, zeichnen);
    var sim = { zustand: function(){ var w = werte(r); return { b: w.b, c: w.c, D: w.b * w.b - 4 * w.c }; }, zeichnen: zeichnen };
    function zeichnen(){
      var w = werte(r), b = w.b, c = w.c, xs = -b / 2, ys = c - b * b / 4, D = b * b - 4 * c;
      K.leeren(); K.senkrecht(xs, 'symachse hilfslinie'); K.kurve(function(x){ return x * x + b * x + c; }, 'kurve');
      K.punkt(xs, ys, 'p-s', 'S(' + z(xs) + ' | ' + z(ys) + ')', xs > 2 ? -8 : 8, 18, xs > 2 ? 'end' : 'start');
      (D > 0 ? [xs - Math.sqrt(D) / 2, xs + Math.sqrt(D) / 2] : D === 0 ? [xs] : []).forEach(function(x){ K.punkt(x, 0, 'p-null'); });
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + grundText(1, b, c) + ' &nbsp;·&nbsp; D = <b>' + z(D) + '</b>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh nur \\(c\\). Was macht die Symmetrieachse?', ok: function(s){ return s.b === -4 && s.c !== 3; } },
      { text: 'Schieb \\(b\\) auf \\(2\\). Wo liegt jetzt die Symmetrieachse?', ok: function(s){ return s.b === 2; } },
      { text: 'Bei \\(b = -2\\): Lass die Parabel die \\(x\\)-Achse berühren.', ok: function(s){ return s.b === -2 && s.c === 1; } },
      { text: 'Stell eine Parabel ohne Nullstelle ein.', ok: function(s){ return s.D < 0; } },
      { text: 'Stell die Parabel mit den Nullstellen \\(-2\\) und \\(1\\) ein.', ok: function(s){ return s.b === 1 && s.c === -2; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: a suchen ---------- */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), inp = fig.querySelector('input[data-p="a"]'), K, fall = 'A', pruefen = function(){};
    var FAELLE = {
      A: { fenster: { w: 300, h: 300, x0: -2, x1: 9, y0: -4, y1: 7, xm: [4, 8], ym: [-2, 2, 4, 6], xname: 'x [m]', yname: 'h [m]' }, a: [-1, -0.05, 0.05, -0.5],
           f: function(a, x){ return a * (x - 5) * (x - 5) + 6; }, p: [0, 1],
           term: function(a){ return 'h(x) = ' + sp('tx-blau', z(a)) + '·(x − 5)² + 6'; },
           fest: function(){ K.punkt(5, 6, 'p-s', 'S(5 | 6)'); } },
      B: { fenster: { w: 300, h: 300, x0: -3, x1: 5, y0: -10, y1: 6, sy: 2, xm: [-2, 2, 4], ym: [-8, -4, 4] }, a: [-3, 3, 0.5, 1],
           f: function(a, x){ return a * (x + 1) * (x - 3); }, p: [1, -8],
           term: function(a){ return 'f(x) = ' + sp('tx-blau', z(a)) + '·(x + 1)(x − 3)'; },
           fest: function(){ K.punkt(-1, 0, 'p-null', '−1', -6, -8, 'end'); K.punkt(3, 0, 'p-null', '3', 6, -8); } }
    };
    function aufbauen(f){
      fall = f; while (svg.firstChild) svg.removeChild(svg.firstChild);
      var F = FAELLE[f]; K = Achsen(svg, F.fenster);
      inp.min = F.a[0]; inp.max = F.a[1]; inp.step = F.a[2]; inp.value = F.a[3];
      zeichnen();
    }
    var sim = { zustand: function(){ return { fall: fall, a: +inp.value }; }, zeichnen: function(){ zeichnen(); } };
    function zeichnen(){
      var F = FAELLE[fall], a = +inp.value, y = F.f(a, F.p[0]), hit = Math.abs(y - F.p[1]) < 1e-9;
      inp.parentNode.querySelector('.sl-val').textContent = z(a);
      K.leeren(); if (a !== 0) K.kurve(function(x){ return F.f(a, x); }, 'kurve');
      F.fest(); K.punkt(F.p[0], F.p[1], hit ? 'p-s' : 'p-c', 'P(' + z(F.p[0]) + ' | ' + z(F.p[1]) + ')', fall === 'A' ? -8 : 8, fall === 'A' ? -8 : 16, fall === 'A' ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML = a === 0 ? 'a = 0: keine Parabel' : F.term(a);
      fig.classList.toggle('treffer', hit);
      pruefen();
    }
    inp.addEventListener('input', zeichnen);
    pruefen = Leiste(fig, [
      { text: 'Der Scheitel \\(S(5 \\mid 6)\\) ist fest. Finde \\(a\\), damit die Parabel durch \\(P\\) geht.', setup: function(){ aufbauen('A'); }, ok: function(s){ return s.fall === 'A' && Math.abs(s.a + 0.2) < 1e-9; } },
      { text: 'Jetzt sind die Nullstellen \\(-1\\) und \\(3\\) fest. Finde \\(a\\) für \\(P(1 \\mid -8)\\).', setup: function(){ aufbauen('B'); }, ok: function(s){ return s.fall === 'B' && s.a === 2; } }
    ], sim);
    aufbauen('A');
  })();

  /* ---------- Kapitel 5: Zaun (36 m, anderes Beispiel als der Clip mit 40 m) ---------- */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var H = 18;   // halber Umfang: x + y = 18
    var svg = fig.querySelector('svg'), feld = el(svg, 'g', {}), gp = el(svg, 'g', { transform: 'translate(200,0)' });
    var K = Achsen(gp, { w: 240, h: 230, x0: -1, x1: 19.5, y0: -7, y1: 95, sx: 3, sy: 20, xm: [9, 18], ym: [40, 80], xname: 'x [m]', yname: 'A [m²]' });
    var besucht = {}, pruefen = function(){};
    var r = regler(fig, zeichnen);
    var sim = { zustand: function(){ var x = werte(r).x; return { x: x, besucht: besucht }; }, zeichnen: zeichnen, aufraeumen: function(){ besucht = {}; } };
    function zeichnen(){
      var x = werte(r).x, y = H - x, A = x * y, s = 10; besucht[x] = true;
      while (feld.firstChild) feld.removeChild(feld.firstChild);
      el(feld, 'rect', { x: 10, y: 20, width: H * s, height: H * s, 'class': 'feld-rahmen hilfslinie' });
      el(feld, 'rect', { x: 10, y: 20 + (H * s - y * s), width: x * s, height: y * s, 'class': 'feld' });
      el(feld, 'text', { x: 10 + x * s / 2, y: 215, 'text-anchor': 'middle', 'class': 'p-text p-n' }, 'x = ' + z(x) + ' m');
      el(feld, 'text', { x: 10 + x * s + 4, y: 20 + H * s - y * s / 2, 'class': 'skala' }, z(y) + ' m');
      K.leeren(); K.kurve(function(t){ return t * (H - t); }, 'kurve', 0, H);
      if (x !== H / 2) K.punkt(H - x, A, 'p-geist');
      K.punkt(x, A, x === H / 2 ? 'p-s' : 'p-n', 'A = ' + z(A), x > 11 ? -8 : 8, -8, x > 11 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML = 'A(' + sp('tx-orange', z(x)) + ') = ' + z(x) + ' · ' + z(y) + ' = <b>' + z(A) + ' m²</b>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Stell \\(x = 6\\) ein, dann \\(x = 12\\). Vergleiche \\(A\\).', ok: function(s){ return s.besucht[6] && s.besucht[12]; } },
      { text: 'Finde die grösste Fläche.', ok: function(s){ return s.x === 9; } },
      { text: '\\(x = 5\\) gibt \\(A = 65\\). Welches andere \\(x\\) gibt dieselbe Fläche?', ok: function(s){ return s.x === 13; } }
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
    function kl(u){ return u > 0 ? '(x - ' + u + ')' : u < 0 ? '(x + ' + (-u) + ')' : 'x'; }
    function plus(v){ return v === 0 ? '' : (v > 0 ? ' + ' + v : ' - ' + (-v)); }
    function koef(a){ return a === 1 ? '' : a === -1 ? '-' : tz(a); }
    function grund(a, b, c){ var s = koef(a) + 'x^2'; if (b) s += (b > 0 ? ' + ' : ' - ') + (Math.abs(b) === 1 ? '' : Math.abs(b)) + 'x'; return s + plus(c); }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    var TYPEN = {
      'scheitel-lesen': { felder: ['xs', 'ys'], muster: 'S( {xs} | {ys} )',
        neu: function(){ var a = zufall([-2, -1, -0.5, 0.5, 1, 2, 3]), xs = zufall(bereich(-5, 5, [0])), ys = zufall(bereich(-5, 5, [0]));
          return { a: a, xs: xs, ys: ys, text: 'Scheitelpunkt von \\(f(x) = ' + koef(a) + kl(xs) + '^2' + plus(ys) + '\\)?' }; },
        pruefen: function(A, e){
          if (gl(e.xs, A.xs) && gl(e.ys, A.ys)) return null;
          if (gl(e.xs, -A.xs) && gl(e.ys, A.ys)) return 'Vorzeichen von \\(x_s\\): \\(' + kl(A.xs) + '\\) wird bei \\(x = ' + tz(A.xs) + '\\) null.';
          if (gl(e.xs, A.xs) && gl(e.ys, -A.ys)) return '\\(y_s\\) steht mit eigenem Vorzeichen hinter der Klammer: \\(' + tz(A.ys) + '\\).';
          if (gl(e.xs, -A.xs) && gl(e.ys, -A.ys)) return 'Nur \\(x_s\\) dreht das Vorzeichen, \\(y_s\\) nicht.';
          if (gl(e.xs, A.ys) && gl(e.ys, A.xs)) return 'Vertauscht: zuerst die Stelle aus der Klammer, dann die Höhe.';
          if (gl(e.xs, A.a) || gl(e.ys, A.a)) return '\\(a\\) verschiebt nichts.';
          return '\\(x_s\\): Wo wird die Klammer null? \\(y_s\\): Was steht dahinter?'; },
        loesung: function(A){ return 'S(' + tz(A.xs) + ' \\mid ' + tz(A.ys) + ')'; } },
      'beschreibung': { felder: ['a', 'xs', 'ys'], muster: 'f(x) = {a} · (x − {xs})² + {ys}',
        neu: function(){ var a = zufall([-3, -2, -1, -0.5, 0.5, 2, 3]), xs = zufall(bereich(-4, 4, [0])), ys = zufall(bereich(-4, 4, [0])), t = [];
          if (a < 0) t.push('nach unten geöffnet');
          if (Math.abs(a) > 1) t.push('Streckfaktor \\(' + Math.abs(a) + '\\) (schmaler)');
          if (Math.abs(a) < 1) t.push('Streckfaktor \\(' + Math.abs(a) + '\\) (breiter)');
          t.push('\\(' + Math.abs(xs) + '\\) nach ' + (xs > 0 ? 'rechts' : 'links'));
          t.push('\\(' + Math.abs(ys) + '\\) nach ' + (ys > 0 ? 'oben' : 'unten'));
          return { a: a, xs: xs, ys: ys, text: 'Normalparabel: ' + t.join(', ') + '. Scheitelform?' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.xs, A.xs) && gl(e.ys, A.ys)) return null;
          var r = [];
          if (gl(e.xs, -A.xs)) r.push('Nach ' + (A.xs > 0 ? 'rechts' : 'links') + ' heisst \\(x_s = ' + tz(A.xs) + '\\).'); else if (!gl(e.xs, A.xs)) r.push('\\(x_s\\): rechts positiv, links negativ.');
          if (gl(e.ys, -A.ys)) r.push('Nach ' + (A.ys > 0 ? 'oben' : 'unten') + ' heisst \\(y_s = ' + tz(A.ys) + '\\).'); else if (!gl(e.ys, A.ys)) r.push('\\(y_s\\): oben positiv, unten negativ.');
          if (gl(e.a, -A.a)) r.push(A.a < 0 ? 'Nach unten geöffnet: \\(a\\) ist negativ.' : 'Nach oben geöffnet: \\(a \\gt 0\\).'); else if (!gl(e.a, A.a)) r.push('\\(a\\) ist der Streckfaktor, nach unten geöffnet mit Minus.');
          return r.join(' '); },
        loesung: function(A){ return 'f(x) = ' + koef(A.a) + kl(A.xs) + '^2' + plus(A.ys); } },
      'graf-scheitelform': { felder: ['a', 'xs', 'ys'], muster: 'f(x) = {a} · (x − {xs})² + {ys}', graf: true,
        neu: function(){ var a = zufall([-2, -1, -0.5, 0.5, 1, 2]), xs = zufall(bereich(-3, 3)), ys = zufall(bereich(-3, 3));
          return { a: a, xs: xs, ys: ys, s: Math.abs(a) === 0.5 ? 2 : 1, text: 'Scheitelform der Parabel? (Punkte auf Gitterpunkten)' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.xs, A.xs) && gl(e.ys, A.ys)) return null;
          var r = [];
          if (gl(e.xs, -A.xs) && A.xs !== 0) r.push('Der Scheitel liegt bei \\(x = ' + tz(A.xs) + '\\): Gib \\(x_s\\) ein, nicht das Zeichen in der Klammer.');
          else if (!gl(e.xs, A.xs) || !gl(e.ys, A.ys)) r.push('Scheitel nochmals ablesen: tiefster oder höchster Punkt.');
          if (gl(e.a, -A.a)) r.push('Öffnung nach ' + (A.a > 0 ? 'oben' : 'unten') + ': \\(a ' + (A.a > 0 ? '\\gt' : '\\lt') + ' 0\\).');
          else if (!gl(e.a, A.a)) r.push('\\(a\\): ' + A.s + ' nach rechts — wie weit hinauf oder hinunter? Bei \\(x^2\\) wären es ' + (A.s * A.s) + '.');
          return r.join(' '); },
        loesung: function(A){ return 'f(x) = ' + koef(A.a) + kl(A.xs) + '^2' + plus(A.ys); } },
      'scheitel-grund': { felder: ['a', 'b', 'c'], muster: 'f(x) = {a} x² + {b} x + {c}',
        neu: function(){ var a = zufall([1, 1, -1, 2, -2, 3]), xs = zufall(bereich(-4, 4, [0])), ys = zufall(bereich(-5, 5, [0]));
          return { a: a, b: -2 * a * xs, c: a * xs * xs + ys, xs: xs, ys: ys, text: 'In die Grundform: \\(f(x) = ' + koef(a) + kl(xs) + '^2' + plus(ys) + '\\)' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.b, A.b) && gl(e.c, A.c)) return null;
          if (!gl(e.a, A.a)) return '\\(a\\) bleibt beim Umformen derselbe: \\(' + tz(A.a) + '\\).';
          if (gl(e.b, 0)) return 'Das mittlere Glied fehlt: \\(' + kl(A.xs) + '^2 = x^2 ' + (A.xs > 0 ? '-' : '+') + ' ' + Math.abs(2 * A.xs) + 'x + ' + (A.xs * A.xs) + '\\).';
          if (gl(e.b, -A.b)) return 'Vorzeichen des mittleren Glieds: \\(' + kl(A.xs) + '^2\\) gibt \\(' + (A.xs > 0 ? '-' : '+') + Math.abs(2 * A.xs) + 'x\\).';
          if (A.a !== 1 && gl(e.b, A.b / A.a)) return '\\(a = ' + tz(A.a) + '\\) gehört auch vor das mittlere Glied.';
          if (gl(e.b, A.b) && A.a !== 1 && gl(e.c, A.xs * A.xs + A.ys)) return '\\(a\\) multipliziert auch \\(' + (A.xs * A.xs) + '\\): \\(c = ' + tz(A.a) + ' \\cdot ' + (A.xs * A.xs) + plus(A.ys) + '\\).';
          if (gl(e.b, A.b) && gl(e.c, A.a * A.xs * A.xs)) return '\\(y_s = ' + tz(A.ys) + '\\) kommt noch dazu.';
          if (gl(e.b, A.b)) return '\\(b\\) stimmt. \\(c = a \\cdot x_s^2 + y_s\\) nachrechnen.';
          return 'Klammer ausquadrieren, mit \\(a\\) multiplizieren, \\(y_s\\) dazu.'; },
        loesung: function(A){ return 'f(x) = ' + grund(A.a, A.b, A.c); } },
      'produkt-grund': { felder: ['a', 'b', 'c'], muster: 'f(x) = {a} x² + {b} x + {c}',
        neu: function(){ var a = zufall([1, 1, -1, 2, -2]), x1 = zufall(bereich(-5, 5, [0])), x2; do { x2 = zufall(bereich(-5, 5)); } while (x2 === x1);
          return { a: a, b: -a * (x1 + x2), c: a * x1 * x2, x1: x1, x2: x2, text: 'In die Grundform: \\(f(x) = ' + koef(a) + (x2 === 0 ? 'x' + kl(x1) : kl(x1) + kl(x2)) + '\\)' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.b, A.b) && gl(e.c, A.c)) return null;
          if (!gl(e.a, A.a)) return '\\(a\\) ist der Faktor vor den Klammern: \\(' + tz(A.a) + '\\).';
          if (A.a !== 1 && gl(e.b, A.b / A.a) && gl(e.c, A.c / A.a)) return 'Den Faktor \\(' + tz(A.a) + '\\) mit allen Gliedern multiplizieren.';
          if (A.b !== 0 && gl(e.b, -A.b)) return 'Vorzeichen von \\(b\\): Die Klammern ausmultiplizieren, nicht die Nullstellen addieren.';
          if (A.c !== 0 && gl(e.c, -A.c)) return 'Vorzeichen von \\(c\\): Produkt der beiden Zahlen in den Klammern, mit ihren Vorzeichen.';
          return 'Klammern ausmultiplizieren, dann mit \\(a\\) multiplizieren.'; },
        loesung: function(A){ return 'f(x) = ' + grund(A.a, A.b, A.c); } },
      'grund-scheitelform': { felder: ['a', 'xs', 'ys'], muster: 'f(x) = {a} · (x − {xs})² + {ys}',
        neu: function(){ var a = zufall([1, 1, 1, -1, 2]), xs = zufall(bereich(-4, 4, [0])), ys = zufall(bereich(-6, 6, [0])), b = -2 * a * xs, c = a * xs * xs + ys;
          return { a: a, b: b, c: c, xs: xs, ys: ys, text: 'In die Scheitelform: \\(f(x) = ' + grund(a, b, c) + '\\)' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a) && gl(e.xs, A.xs) && gl(e.ys, A.ys)) return null;
          if (!gl(e.a, A.a)) return '\\(a\\) bleibt beim Umformen derselbe: \\(' + tz(A.a) + '\\).';
          if (gl(e.xs, -A.xs)) return 'Die Klammer heisst \\(' + kl(A.xs) + '^2\\), also \\(x_s = ' + tz(A.xs) + '\\).';
          if (A.a !== 1 && gl(e.xs, -A.b / 2)) return 'Zuerst \\(a\\) ausklammern: \\(x_s = -\\dfrac{b}{2a}\\).';
          if (gl(e.xs, A.xs) && gl(e.ys, A.c)) return 'Die Ergänzung wieder abziehen: \\(y_s = c - a\\,x_s^2\\).';
          if (gl(e.xs, A.xs) && gl(e.ys, A.c + A.a * A.xs * A.xs)) return 'Die Ergänzung abziehen, nicht dazuzählen.';
          if (gl(e.xs, A.xs) && A.a !== 1 && gl(e.ys, A.c - A.xs * A.xs)) return '\\(a\\) multipliziert auch die Ergänzung: \\(y_s = c - a\\,x_s^2\\).';
          if (gl(e.xs, A.xs)) return '\\(x_s\\) stimmt. \\(y_s = f(' + tz(A.xs) + ')\\) nachrechnen.';
          return '\\(a\\) ausklammern, halbe Zahl vor \\(x\\) quadrieren, ergänzen und wieder abziehen.'; },
        loesung: function(A){ return 'f(x) = ' + koef(A.a) + kl(A.xs) + '^2' + plus(A.ys); } },
      'grund-scheitel': { felder: ['xs', 'ys'], muster: 'S( {xs} | {ys} )',
        neu: function(){ var a = zufall([1, 1, -1, 2]), xs = zufall(bereich(-4, 4, [0])), ys = zufall(bereich(-6, 6, [0])), b = -2 * a * xs, c = a * xs * xs + ys;
          return { a: a, b: b, c: c, xs: xs, ys: ys, text: 'Scheitelpunkt von \\(f(x) = ' + grund(a, b, c) + '\\)?' }; },
        pruefen: function(A, e){
          var f = function(x){ return A.a * x * x + A.b * x + A.c; };
          if (gl(e.xs, A.xs) && gl(e.ys, A.ys)) return null;
          if (gl(e.xs, -A.xs)) return 'Minus vor dem Bruch: \\(x_s = -\\dfrac{' + tz(A.b) + '}{' + tz(2 * A.a) + '} = ' + tz(A.xs) + '\\).' + (gl(e.ys, f(-A.xs)) ? ' Dein \\(y_s\\) passt zu deinem \\(x_s\\).' : '');
          if (gl(e.xs, A.xs) && gl(e.ys, A.c)) return '\\(c\\) ist der \\(y\\)-Achsenabschnitt. \\(y_s = f(' + tz(A.xs) + ')\\).';
          if (gl(e.xs, A.xs)) return '\\(x_s\\) stimmt. \\(y_s = f(' + tz(A.xs) + ')\\) nachrechnen.';
          return '\\(x_s = -\\dfrac{b}{2a}\\), dann \\(y_s = f(x_s)\\).'; },
        loesung: function(A){ return 'S(' + tz(A.xs) + ' \\mid ' + tz(A.ys) + ')'; } },
      'nullstellen': { felder: ['x_1', 'x_2'], muster: 'x₁ = {x_1}   x₂ = {x_2}',
        neu: function(){ var r1 = zufall(bereich(-6, 6)), r2; do { r2 = zufall(bereich(-6, 6)); } while (r2 === r1);
          return { r: [Math.min(r1, r2), Math.max(r1, r2)], b: -(r1 + r2), c: r1 * r2, text: 'Nullstellen von \\(f(x) = ' + grund(1, -(r1 + r2), r1 * r2) + '\\)?' }; },
        pruefen: function(A, e){
          var x = [e.x_1, e.x_2], hat = function(w){ return gl(x[0], w) || gl(x[1], w); };
          if (hat(A.r[0]) && hat(A.r[1])) return null;
          if (hat(-A.r[0]) && hat(-A.r[1])) return 'Vorzeichen gedreht: Die Klammer muss null werden.';
          if (hat(A.r[0]) || hat(A.r[1])) return 'Eine stimmt. Die andere durch Einsetzen prüfen.';
          if (hat(-A.b / 2)) return '\\(' + tz(-A.b / 2) + '\\) ist die Stelle des Scheitels.';
          return 'Zwei Zahlen mit Produkt \\(c = ' + tz(A.c) + '\\) und Summe \\(-b = ' + tz(-A.b) + '\\) — oder Mitternachtsformel.'; },
        loesung: function(A){ return 'x_1 = ' + tz(A.r[0]) + ',\\ x_2 = ' + tz(A.r[1]); } },
      'aufstellen-scheitel': { felder: ['a'], muster: 'a = {a}',
        neu: function(){ var a = zufall([-3, -2, -1, -0.5, 0.5, 1, 2, 3]), xs = zufall(bereich(-3, 3)), ys = zufall(bereich(-4, 4)),
          d = Math.abs(a) === 0.5 ? zufall([-2, 2]) : zufall([-3, -2, 2, 3]);   // |d| ≥ 2, sonst prüft die Aufgabe das Quadrieren nicht
          return { a: a, xs: xs, ys: ys, xp: xs + d, yp: a * d * d + ys, d: d,
            text: 'Scheitel \\(S(' + tz(xs) + ' \\mid ' + tz(ys) + ')\\), Punkt \\(P(' + tz(xs + d) + ' \\mid ' + tz(a * d * d + ys) + ')\\). Wie gross ist \\(a\\)?' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, -A.a)) return 'Vorzeichen: \\(P\\) liegt ' + (A.a > 0 ? 'über' : 'unter') + ' dem Scheitel.';
          if (gl(e.a, (A.yp - A.ys) / A.d)) return 'Quadrieren nicht vergessen: \\((' + tz(A.xp) + ' - ' + (A.xs < 0 ? '(' + tz(A.xs) + ')' : tz(A.xs)) + ')^2 = ' + (A.d * A.d) + '\\).';
          if (gl(e.a, (A.yp + A.ys) / (A.d * A.d))) return '\\(y_s\\) abziehen, nicht dazuzählen.';
          return 'Ansatz \\(a(x - x_s)^2 + y_s\\), \\(P\\) einsetzen, nach \\(a\\) auflösen.'; },
        loesung: function(A){ return 'a = ' + tz(A.a); } },
      'aufstellen-nullstellen': { felder: ['a'], muster: 'a = {a}',
        neu: function(){ var x1 = zufall(bereich(-4, 3)), x2, xp, a = zufall([-3, -2, -1, 1, 2, 3]);
          do { x2 = zufall(bereich(-3, 5)); } while (x2 <= x1);
          do { xp = zufall(bereich(-4, 6)); } while (xp === x1 || xp === x2);
          var yp = a * (xp - x1) * (xp - x2);
          return { a: a, x1: x1, x2: x2, xp: xp, yp: yp, text: 'Nullstellen \\(' + tz(x1) + '\\) und \\(' + tz(x2) + '\\), Punkt \\(P(' + tz(xp) + ' \\mid ' + tz(yp) + ')\\). Wie gross ist \\(a\\)?' }; },
        pruefen: function(A, e){
          if (gl(e.a, A.a)) return null;
          if (gl(e.a, -A.a)) return 'Vorzeichen: \\((' + tz(A.xp) + ' - ' + (A.x1 < 0 ? '(' + tz(A.x1) + ')' : tz(A.x1)) + ')\\) und \\((' + tz(A.xp) + ' - ' + (A.x2 < 0 ? '(' + tz(A.x2) + ')' : tz(A.x2)) + ')\\) sorgfältig rechnen.';
          var falsch = (A.xp + A.x1) * (A.xp + A.x2);
          if (falsch && gl(e.a, A.yp / falsch)) return 'In die Klammern kommt \\(x - x_1\\), nicht \\(x + x_1\\).';
          return 'Ansatz \\(a(x - x_1)(x - x_2)\\), \\(P\\) einsetzen, nach \\(a\\) auflösen.'; },
        loesung: function(A){ return 'a = ' + tz(A.a); } },
      'zaun': { felder: ['x', 'A'], muster: 'Seite x = {x} m   Fläche A = {A} m²',
        neu: function(){ var U = zufall(bereich(5, 15)) * 4; return { U: U, x: U / 4, A: U * U / 16, text: 'Mit \\(' + U + '\\) m Zaun ein Rechteck einzäunen. Bei welcher Seite \\(x\\) wird die Fläche am grössten?' }; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.A, A.A)) return null;
          if (gl(e.x, A.U / 2)) return '\\(' + (A.U / 2) + '\\) ist eine Nullstelle von \\(A(x) = x(' + (A.U / 2) + ' - x)\\). Das Maximum liegt in der Mitte.';
          if (gl(e.x, A.x)) return '\\(x\\) stimmt. \\(A = ' + A.x + ' \\cdot ' + A.x + '\\).';
          return '\\(A(x) = x(' + (A.U / 2) + ' - x)\\): Nullstellen ablesen, Mitte nehmen, einsetzen.'; },
        loesung: function(A){ return 'x = ' + A.x + '\\ \\text{m},\\ A = ' + A.A + '\\ \\text{m}^2'; } },
      'mauer': { felder: ['x', 'A'], muster: 'x = {x} m   A = {A} m²',
        neu: function(){ var L = zufall(bereich(5, 14)) * 4; return { L: L, x: L / 4, A: L * L / 8,   // ohne 60 m (= Aufgabe 5a)
          text: 'Rechteckiges Beet an einer Mauer, \\(' + L + '\\) m Zaun für die drei anderen Seiten. \\(x\\) = Seite senkrecht zur Mauer. Grösste Fläche?' }; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) && gl(e.A, A.A)) return null;
          if (gl(e.x, A.L / 2)) return 'Bei \\(x = ' + (A.L / 2) + '\\) bleibt nichts für die dritte Seite: \\(A(x) = x(' + A.L + ' - 2x)\\) ist null.';
          if (gl(e.x, A.L / 3)) return 'Kein Quadrat: Die Mauer spart eine Seite. Nullstellen von \\(x(' + A.L + ' - 2x)\\) sind \\(0\\) und \\(' + (A.L / 2) + '\\).';
          if (gl(e.x, A.x)) return '\\(x\\) stimmt. \\(A = ' + A.x + ' \\cdot ' + (A.L - 2 * A.x) + '\\).';
          return '\\(A(x) = x(' + A.L + ' - 2x)\\): Nullstellen \\(0\\) und \\(' + (A.L / 2) + '\\), Mitte nehmen.'; },
        loesung: function(A){ return 'x = ' + A.x + '\\ \\text{m},\\ A = ' + A.A + '\\ \\text{m}^2'; } }
    };
    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie'), bild = box.querySelector('.ue-bild');
      function neu(){
        A = T.neu(); versuche = 0; geloest = false; box.__aufgabe = A;   // Testhaken
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){ html = html.replace('{' + f + '}', '<input type="text" inputmode="decimal" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">'); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        if (bild){
          while (bild.firstChild) bild.removeChild(bild.firstChild);
          if (T.graf){
            var fe = [A.xs - 4, A.xs + 4, A.ys - 4, A.ys + 4];
            bild.setAttribute('viewBox', '0 0 170 170');
            var K = Achsen(bild, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3.5, pfeil: 6 });
            K.kurve(function(x){ return A.a * (x - A.xs) * (x - A.xs) + A.ys; }, 'kurve');
            K.punkt(A.xs, A.ys, 'p-s'); K.punkt(A.xs + A.s, A.ys + A.a * A.s * A.s, 'p-s');
          }
        }
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;   // nach ✓ zählt erst die nächste Aufgabe
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('input').forEach(function(i){ var r = lesen(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-3</code>, <code>0.5</code> oder <code>1/2</code>.'; return; }
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

  /* ---------- Minigrafen: <svg class="mini" data-f="a,xs,ys" data-fenster data-punkte data-titel data-xname data-yname> ---------- */
  document.querySelectorAll('svg.mini[data-f]').forEach(function(svg){
    var f = svg.dataset.f.split(',').map(Number), fe = (svg.dataset.fenster || '-5,5,-5,5').split(',').map(Number);
    var w = 150, h = 150 * (fe[3] - fe[2]) / (fe[1] - fe[0]);
    svg.setAttribute('viewBox', '0 0 150 ' + h.toFixed(1)); svg.setAttribute('role', 'img');
    var K = Achsen(svg, { w: w, h: h, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, xm: [1], ym: [1], pfeil: 6, xname: svg.dataset.xname, yname: svg.dataset.yname });
    K.kurve(function(x){ return f[0] * (x - f[1]) * (x - f[1]) + f[2]; }, 'kurve');
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){ var q = p.split(',').map(Number); K.punkt(q[0], q[1], 'p-s'); });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Parabel' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
