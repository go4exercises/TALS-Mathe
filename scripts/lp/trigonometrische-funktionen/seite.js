<script>
/* Leitprogramm Trigonometrische Funktionen — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Notation wie auf Themenseite 3.5: x im Bogenmass, P = (cos x | sin x)
   auf dem Einheitskreis, Periodenlänge p, k ∈ ℤ, y = a·sin(b(x − u)) + v.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = Sinus · grün = Cosinus · orange = Tangens · rot = Gegenbeispiel · Tinte = neutral
   (Einheitskreis, Mittellinie, Pole, Waagrechte y = c). Zahlen mit Dezimalpunkt und echtem Minus. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', PI = Math.PI;
  function z(n){ var r = Math.round(n * 1000) / 1000; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
  /* Vielfaches von π als Text (Anzeige) bzw. LaTeX: x = (n/d)·π mit d aus 1, 2, 3, 4, 6, 12. */
  function piBruch(x){
    var q = x / PI;
    for (var d of [1, 2, 3, 4, 5, 6, 7, 12]){ var n = Math.round(q * d); if (Math.abs(q * d - n) < 1e-7){ var g = ggT(n, d) || 1; return [n / g, d / g]; } }
    return null;
  }
  /* Zahl für die Live-Anzeige: gerundet mit «≈» (HOWTO §15). */
  function zz(v){ var r = Math.round(v * 1000) / 1000; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(v); }
  function piT(x){
    var b = piBruch(x); if (!b) return z(x);
    var n = b[0], d = b[1]; if (n === 0) return '0';
    var s = (n < 0 ? '−' : '') + (Math.abs(n) === 1 ? '' : Math.abs(n)) + 'π';
    return d === 1 ? s : s + '/' + d;
  }

  /* ---------- Koordinatensystem (wie in den anderen Leitprogrammen) ----------
     xm/ym: Zahlen oder Paare [Stelle, Beschriftung] — eine Sinuskurve gehört bei π/2 geteilt. */
  function Achsen(svg, o){
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1;
    var id = 'k' + Math.random().toString(36).slice(2, 8);
    function X(x){ return (x - x0) / (x1 - x0) * W; }
    function Y(y){ return H - (y - y0) / (y1 - y0) * H; }
    var g = el(svg, 'g', {});
    var cp = el(g, 'clipPath', { id: id }); el(cp, 'rect', { x: 0, y: 0, width: W, height: H });
    var sx = o.sx || 1, sy = o.sy || 1, i;
    for (i = Math.ceil((Math.max(x0, o.gx0 == null ? x0 : o.gx0)) / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: X(Math.max(x0, o.gx0 == null ? x0 : o.gx0)), y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    if (y0 <= 0 && y1 >= 0) el(g, 'line', { x1: 0, y1: Y(0), x2: W, y2: Y(0), 'class': 'achse' });
    if (x0 <= 0 && x1 >= 0) el(g, 'line', { x1: X(0), y1: 0, x2: X(0), y2: H, 'class': 'achse' });
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
    var mark = function(t){ return Array.isArray(t) ? t : [t, z(t)]; };
    (o.xm || []).forEach(function(t){ t = mark(t); el(g, 'text', { x: X(t[0]), y: Y(Math.max(0, y0)) + 13, 'text-anchor': 'middle', 'class': 'skala' }, t[1]); });
    (o.ym || []).forEach(function(t){ t = mark(t); el(g, 'text', { x: X(Math.max(0, x0)) - 5, y: Y(t[0]) + 4, 'text-anchor': 'end', 'class': 'skala' }, t[1]); });
    var ebene = el(svg, 'g', {});
    var schilder = el(svg, 'g', {});
    namen.forEach(function(n){ el(schilder, 'text', { x: n[0], y: n[1], 'text-anchor': n[2], 'class': 'achsname' }, n[3]); });
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      kurve: function(f, cls, a, b){
        var d = '', an = false, A = a == null ? x0 : a, B = b == null ? x1 : b, yl = null, Hh = y1 - y0;
        for (var k = 0; k <= 600; k++){
          var x = A + (B - A) * k / 600, y = f(x);
          if (y == null || isNaN(y) || !isFinite(y) || Math.abs(y) > 1e6){ an = false; yl = null; continue; }
          if (yl !== null && Math.abs(y - yl) > Hh) an = false;      // Pol des Tangens: nicht verbinden
          yl = y;
          y = Math.max(y0 - 3 * Hh, Math.min(y1 + 3 * Hh, y));
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
      },
      /* Einheitskreis mit Mittelpunkt (mx | 0), Radius 1 in y-Einheiten: rund, auch wenn die Achsen
         verschieden geteilt sind. Liefert die Pixelpunkte von Mittelpunkt und P. */
      kreis: function(mx, w, cls){
        var r = Math.abs(Y(1) - Y(0)), cx = X(mx), cy = Y(0);
        el(ebene, 'circle', { cx: cx, cy: cy, r: r, 'class': 'einheitskreis' });
        var Px = cx + r * Math.cos(w), Py = cy - r * Math.sin(w);
        var gross = (w % (2 * PI)) > PI ? 1 : 0;
        if (w > 1e-9) el(ebene, 'path', { d: w >= 2 * PI - 1e-9
          ? 'M' + (cx + r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 1 0 ' + (cx - r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 1 0 ' + (cx + r) + ' ' + cy
          : 'M' + (cx + r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 ' + gross + ' 0 ' + Px.toFixed(1) + ' ' + Py.toFixed(1), 'class': 'bogen ' + (cls || '') });
        el(ebene, 'line', { x1: cx, y1: cy, x2: Px, y2: Py, 'class': 'radius' });
        return { cx: cx, cy: cy, r: r, Px: Px, Py: Py };
      },
      pix: function(xa, ya, xb, yb, cls){ return el(ebene, 'line', { x1: xa, y1: ya, x2: xb, y2: yb, 'class': cls }); },
      ppunkt: function(px, py, cls){ return el(ebene, 'circle', { cx: px, cy: py, r: o.r || 4.5, 'class': cls }); }
    };
  }
  var PIM = [[PI / 2, 'π/2'], [PI, 'π'], [3 * PI / 2, '3π/2'], [2 * PI, '2π']];

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  /* Regler zeigen ihren Wert; Winkelregler (data-pi = Nenner) laufen in Schritten von π/Nenner. */
  function werte(r){
    var w = {};
    for (var k in r){
      var d = +r[k].dataset.pi || 0, v = +r[k].value;
      w[k] = d ? v * PI / d : v;
      r[k].parentNode.querySelector('.sl-val').textContent = d ? piT(w[k]) : z(v);
    }
    return w;
  }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function nahe(a, b){ return Math.abs(a - b) < 1e-9; }
  function grad(x){ return Math.round(x * 180 / PI); }

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
    // Beim Wechsel die Regler auf den Startwert: Sonst erfüllt der Endzustand der vorigen
    // Aufgabe die nächste schon, bevor jemand etwas getan hat (HOWTO §15).
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
  /* Merkt, welche Regler bewegt wurden. Das Objekt wird beim Aufgabenwechsel geleert, nie neu
     zugewiesen — sonst schrieben die Regler weiter ins alte (Prüfung 05.10.2026, H1). */
  function bewegtMerken(r, bewegt, pruefen){
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
  }

  /* ---------- Kapitel 1: vom Einheitskreis zur Kurve ----------
     Unterschied zur Animation «Einheitskreis-Abrollung» auf Themenseite 3.5: dort läuft der
     Punkt von selbst und alle drei Funktionen stehen zur Wahl. Hier stellt man den Winkel in
     Schritten von π/12 selbst ein, die Kurve entsteht nur bis dorthin, und der Schalter zeigt
     den Cosinus als waagrechte Koordinate desselben Punktes. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 440, h: 140, x0: -2.7, x1: 6.9, y0: -1.45, y1: 1.45, sx: PI / 2, sy: 1, gx0: 0,
      xm: PIM, ym: [[1, '1'], [-1, '−1']] });
    var pruefen = function(){}, bewegt = {}, maxk = 0;
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    if (schalter) schalter.addEventListener('change', zeichnen);
    function zust(){ var w = werte(r), k = Math.round(w.x * 12 / PI);
      if (bewegt.x) maxk = Math.max(maxk, k);
      return { k: k, x: w.x, cos: !!(schalter && schalter.checked), bewegt: bewegt, rund: maxk >= 24 }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; maxk = 0; } };
    function zeichnen(){
      var s = zust(), x = s.x, sn = Math.sin(x), cs = Math.cos(x);
      K.leeren();
      var c = K.kreis(-1.6, x, s.cos ? 'gruen' : 'blau');
      if (s.cos){
        K.pix(c.cx, c.cy, c.Px, c.cy, 'koord gruen');
        K.kurve(Math.cos, 'kurve gruen', 0, x);
        K.punkt(x, cs, 'p-lauf gruen', '(' + piT(x) + ' | ' + zz(cs) + ')', x > 5 ? -8 : 8, cs > 0 ? 16 : -8, x > 5 ? 'end' : 'start');
      } else {
        K.pix(c.Px, c.cy, c.Px, c.Py, 'koord blau');
        K.pix(c.Px, c.Py, K.X(x), K.Y(sn), 'projektion');
        K.kurve(Math.sin, 'kurve', 0, x);
        K.punkt(x, sn, 'p-lauf', '(' + piT(x) + ' | ' + zz(sn) + ')', x > 5 ? -8 : 8, sn > 0 ? 16 : -8, x > 5 ? 'end' : 'start');
      }
      K.ppunkt(c.Px, c.Py, 'p-pkt');
      rolle(fig, 'formel').innerHTML = 'x = ' + piT(x) + ' (' + grad(x) + '°); &nbsp;P = (' + sp('tx-gruen', zz(cs)) + ' | ' + sp('tx-blau', zz(sn)) + ')'
        + '; &nbsp;' + (s.cos ? sp('tx-gruen', 'cos x ' + (zz(cs).charAt(0) === '≈' ? '' : '= ') + zz(cs)) : sp('tx-blau', 'sin x ' + (zz(sn).charAt(0) === '≈' ? '' : '= ') + zz(sn)));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Drehe den Punkt \\(P\\) einmal ganz herum, bis \\(x = 2\\pi\\).', ok: function(s){ return s.rund; } },
      // Startzustand: x = π/6, Sinus — keine Aufgabe ist schon gelöst.
      { text: 'Stell den Winkel \\(120^\\circ\\) ein.', ok: function(s){ return s.k === 8; } },
      { text: 'Sinus: Wo ist \\(\\sin x = -\\tfrac12\\) zwischen \\(\\pi\\) und \\(\\tfrac{3\\pi}{2}\\)?', ok: function(s){ return !s.cos && s.k === 14; } },
      { text: 'Stell \\(315^\\circ\\) ein. Ist der Sinus dort positiv oder negativ?', ok: function(s){ return s.k === 21; } },
      { text: 'Schalte auf Cosinus. Wo ist \\(\\cos x = -1\\)?', ok: function(s){ return s.cos && s.k === 12; } },
      { text: 'Cosinus: Wo ist \\(\\cos x = \\tfrac12\\) im vierten Quadranten?', ok: function(s){ return s.cos && s.k === 20; } },
      { text: 'Wo sind Sinus und Cosinus gleich gross und beide negativ?', ok: function(s){ return s.k === 15; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Periode und Symmetrie ----------
     Die Sinuskurve wird um u verschoben, gestrichelt liegt die Cosinuskurve daneben. Wer sie
     aufeinanderlegt, sieht cos x = sin(x + π/2); wer weiterschiebt, sieht die Periode 2π. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 440, h: 150, x0: -7, x1: 7, y0: -1.5, y1: 1.5, sx: PI / 2, sy: 1,
      xm: [[-2 * PI, '−2π'], [-PI, '−π'], [PI, 'π'], [2 * PI, '2π']], ym: [[1, '1'], [-1, '−1']] });
    var pruefen = function(){}, bewegt = {}, ziel = null;
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r); return { k: Math.round(w.u * 4 / PI), u: w.u, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; ziel = null; } };
    function zeichnen(){
      var s = zust(), u = s.u;
      K.leeren();
      if (ziel) K.kurve(ziel, 'zielkurve');
      K.kurve(Math.cos, 'normal gruen');
      K.kurve(function(x){ return Math.sin(x - u); }, 'kurve');
      var xh = u + PI / 2; while (xh > PI) xh -= 2 * PI; while (xh < -PI) xh += 2 * PI;
      K.punkt(xh, 1, 'p-pkt', 'Hochpunkt', 8, -6);
      var gleich = function(g){ return [0.3, 1.1, 2.5].every(function(x){ return Math.abs(Math.sin(x - u) - g(x)) < 1e-9; }); };
      var lage = gleich(Math.cos) ? ' → liegt auf <b>cos x</b>' : gleich(Math.sin) ? ' → liegt auf <b>sin x</b>'
        : gleich(function(x){ return -Math.sin(x); }) ? ' → liegt auf <b>−sin x</b>'
        : gleich(function(x){ return -Math.cos(x); }) ? ' → liegt auf <b>−cos x</b>' : '';
      rolle(fig, 'formel').innerHTML = 'y = ' + sp('tx-blau', s.k === 0 ? 'sin x' : 'sin(x ' + (u > 0 ? '− ' + piT(u) : '+ ' + piT(-u)) + ')') + lage;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(u\\). Wohin wandert der Hochpunkt?', ok: function(s){ return s.bewegt.u; } },
      // Startzustand u = 0. Der Clip schiebt nach links (u = −π/2); hier nach rechts.
      { text: 'Lege die Sinuskurve auf die Cosinuskurve, indem du sie nach <b>rechts</b> schiebst (\\(u \\gt 0\\)).', ok: function(s){ return s.k === 6; } },
      { text: 'Schiebe so, dass die Kurve wieder genau auf sich selbst liegt.', ok: function(s){ return s.k === 8 || s.k === -8; } },
      { text: 'Lege die Kurve nach rechts geschoben auf \\(y = -\\sin x\\) (dünn gezeichnet).', setup: function(){ ziel = function(x){ return -Math.sin(x); }; },
        ok: function(s){ return s.k === 4; } },
      { text: 'Und jetzt nach <b>links</b> geschoben auf \\(y = -\\sin x\\).', setup: function(){ ziel = function(x){ return -Math.sin(x); }; },
        ok: function(s){ return s.k === -4; } },
      { text: 'Lege die Kurve auf \\(y = -\\cos x\\).', setup: function(){ ziel = function(x){ return -Math.cos(x); }; },
        ok: function(s){ return s.k === 2 || s.k === -6; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: die Tangensfunktion ----------
     Wie in Kapitel 1, aber mit der Tangente x = 1 am Kreis: Der Strahl durch P trifft sie in
     der Höhe tan x. Bei π/2 und 3π/2 trifft er sie nicht — dort hat die Kurve ihre Pole. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 440, h: 220, x0: -2.7, x1: 6.9, y0: -3, y1: 3, sx: PI / 2, sy: 1, gx0: 0,
      xm: PIM, ym: [[1, '1'], [-1, '−1'], [2, '2'], [-2, '−2']] });
    var pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r), k = Math.round(w.x * 12 / PI);
      return { k: k, x: w.x, def: k % 12 !== 6, t: Math.tan(w.x), bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; } };
    function zeichnen(){
      var s = zust(), x = s.x;
      K.leeren();
      [PI / 2, 3 * PI / 2].forEach(function(p){ K.strecke(p, -3, p, 3, 'asym hilfslinie'); });
      K.kurve(function(t){ return Math.abs(Math.cos(t)) < 1e-6 ? null : Math.tan(t); }, 'kurve orange hell', 0, 2 * PI);
      var c = K.kreis(-1.9, x, 'orange');
      K.pix(c.cx + c.r, 0, c.cx + c.r, K.Y(-3), 'tangente');
      if (s.def){
        var Ty = c.cy - c.r * s.t;
        // Gerade durch O und P bis zur Tangente: im 2. und 3. Quadranten trifft erst ihre
        // Verlängerung über O hinaus — darum von P aus zeichnen, nicht von O.
        K.pix(Math.cos(x) < 0 ? c.Px : c.cx, Math.cos(x) < 0 ? c.Py : c.cy, c.cx + c.r, Ty, 'strahl');
        K.pix(c.cx + c.r, c.cy, c.cx + c.r, Ty, 'koord orange');
        K.pix(c.cx + c.r, Ty, K.X(x), K.Y(s.t), 'projektion');
        K.kurve(function(t){ return Math.abs(Math.cos(t)) < 1e-6 ? null : Math.tan(t); }, 'kurve orange', 0, x);
        K.punkt(x, s.t, 'p-lauf orange', '(' + piT(x) + ' | ' + zz(s.t) + ')', x > 5 ? -8 : 8, s.t > 0 ? 16 : -8, x > 5 ? 'end' : 'start');
      }
      K.ppunkt(c.Px, c.Py, 'p-pkt');
      rolle(fig, 'formel').innerHTML = 'x = ' + piT(x) + ' (' + grad(x) + '°); &nbsp;'
        + (s.def ? sp('tx-orange', 'tan x ' + (zz(s.t).charAt(0) === '≈' ? '' : '= ') + zz(s.t)) + ' &nbsp;(' + sp('tx-blau', 'sin') + ' : ' + sp('tx-gruen', 'cos') + ')'
                 : sp('tx-orange', 'tan x nicht definiert') + ' — ' + sp('tx-gruen', 'cos x = 0'));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Fahr mit \\(x\\) von \\(0\\) bis \\(2\\pi\\). Wann wird der Tangens sehr gross?', ok: function(s){ return s.bewegt.x; } },
      // Startzustand x = π/6, tan x ≈ 0.577 — keine Aufgabe ist schon gelöst.
      { text: 'Fahr auf \\(x = \\tfrac{\\pi}{2}\\). Was geschieht mit dem Strahl?', ok: function(s){ return s.k === 6; } },
      { text: 'Wo ist \\(\\tan x = -1\\) zwischen \\(\\tfrac{\\pi}{2}\\) und \\(\\pi\\)?', ok: function(s){ return s.k === 9; } },
      { text: 'Finde die Stelle mit \\(\\tan x = 1\\) im dritten Quadranten.', ok: function(s){ return s.k === 15; } },
      { text: 'Wo ist \\(\\tan x = 0\\), ausser bei \\(x = 0\\)?', ok: function(s){ return s.k === 12 || s.k === 24; } },
      { text: 'Wo ist \\(\\tan x \\approx -1.73\\) im vierten Quadranten?', ok: function(s){ return s.k === 20; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Strecken und Verschieben ----------
     Unterschied zum «Transformations-Baukasten» auf Themenseite 3.5: dort fünf Regler mit einer
     Wertetabelle. Hier vier Regler, gestrichelt die Ausgangskurve sin x, dazu Mittellinie,
     Amplitude und Periode als Live-Anzeige — und Ziele, die nur mit der richtigen Kombination gehen. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 440, h: 220, x0: -0.9, x1: 6.9, y0: -4, y1: 4, sx: PI / 2, sy: 1,
      xm: PIM, ym: [[-3, '−3'], [-2, '−2'], [-1, '−1'], [1, '1'], [2, '2'], [3, '3']] });
    var pruefen = function(){}, bewegt = {}, ziel = null;
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r);
      return { a: w.a, b: w.b, u: w.u, k: Math.round(w.u * 6 / PI), v: w.v, bewegt: bewegt,
        gleich: function(a, b, u, v){ for (var x = -1; x <= 7; x += 0.37) if (Math.abs(w.a * Math.sin(w.b * (x - w.u)) + w.v - (a * Math.sin(b * (x - u)) + v)) > 1e-9) return false; return true; } }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; ziel = null; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (ziel) K.kurve(function(x){ return ziel[0] * Math.sin(ziel[1] * (x - ziel[2])) + ziel[3]; }, 'zielkurve');
      K.kurve(Math.sin, 'normal');
      if (s.v !== 0) K.strecke(-1, s.v, 7, s.v, 'asym hilfslinie');
      K.kurve(function(x){ return s.a * Math.sin(s.b * (x - s.u)) + s.v; }, 'kurve');
      var uT = s.k === 0 ? 'x' : 'x ' + (s.u > 0 ? '− ' + piT(s.u) : '+ ' + piT(-s.u));
      var bT = s.b === 1 ? '' : z(s.b);
      rolle(fig, 'formel').innerHTML = 'y = ' + sp('tx-blau', z(s.a)) + ' · sin(' + (s.k === 0 ? bT + 'x' : bT + (bT ? '(' + uT + ')' : uT)) + ')'
        + (s.v === 0 ? '' : (s.v > 0 ? ' + ' : ' − ') + z(Math.abs(s.v)))
        + '<br><span class="nb">Amplitude ' + z(s.a) + '</span>; &nbsp;<span class="nb">Periode ' + (piBruch(2 * PI / s.b) ? piT(2 * PI / s.b) : zz(2 * PI / s.b)) + '</span>'
        + '; &nbsp;<span class="nb">Mittellinie y = ' + z(s.v) + '</span>; &nbsp;<span class="nb">W = [' + z(s.v - s.a) + '; ' + z(s.v + s.a) + ']</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(b\\). Was geschieht mit der Periode?', ok: function(s){ return s.bewegt.b; } },
      // Startzustand a = b = 1, u = v = 0 — die Kurve liegt auf sin x, keine Aufgabe ist gelöst.
      { text: 'Stell eine Periodenlänge von \\(4\\pi\\) ein.', ok: function(s){ return s.b === 0.5; } },
      { text: 'Die Kurve soll zwischen \\(0\\) und \\(3\\) schwanken.', ok: function(s){ return s.a === 1.5 && s.v === 1.5; } },
      { text: 'Bau nach: \\(y = 0.5 \\cdot \\sin(3x)\\)', ok: function(s){ return s.gleich(0.5, 3, 0, 0); } },
      { text: 'Lass \\(a = b = 1\\) und \\(v = 0\\). Schiebe so, dass der erste Hochpunkt rechts der \\(y\\)-Achse bei \\(x = \\pi\\) liegt.',
        ok: function(s){ return s.a === 1 && s.b === 1 && s.v === 0 && s.k === 3; } },
      { text: 'Triff die dünn gezeichnete Zielkurve.', setup: function(){ ziel = [1.5, 2, PI / 6, -0.5]; },
        ok: function(s){ return s.gleich(1.5, 2, PI / 6, -0.5); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Symmetrie nutzen ----------
     Eine Waagrechte y = c schneidet Sinus- oder Cosinuskurve in [0; 2π]. Die Schnittstellen stehen
     mit drei Dezimalen daneben — und die Symmetrieachse, an der sie sich spiegeln. */
  function loesungen(cos, c, L, R){
    var aus = [];
    if (Math.abs(c) > 1 + 1e-12) return aus;
    var x1 = cos ? Math.acos(Math.max(-1, Math.min(1, c))) : Math.asin(Math.max(-1, Math.min(1, c)));
    var basis = cos ? [x1, -x1] : [x1, PI - x1];
    for (var k = Math.floor((L - 7) / (2 * PI)); k <= Math.ceil((R + 7) / (2 * PI)); k++)
      basis.forEach(function(b){ var x = b + 2 * k * PI;
        if (x >= L - 1e-9 && x <= R + 1e-9 && !aus.some(function(y){ return Math.abs(y - x) < 1e-7; })) aus.push(x); });
    return aus.sort(function(p, q){ return p - q; });
  }
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 440, h: 170, x0: -0.6, x1: 6.9, y0: -1.6, y1: 1.6, sx: PI / 2, sy: 0.5,
      xm: PIM, ym: [[1, '1'], [-1, '−1']] });
    var pruefen = function(){}, bewegt = {};
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    if (schalter) schalter.addEventListener('change', zeichnen);
    function zust(){ var w = werte(r), cos = !!(schalter && schalter.checked), c = Math.round(w.c * 10) / 10, L = loesungen(cos, c, 0, 2 * PI);
      return { c: c, cos: cos, l: L, n: L.length, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; } };
    function zeichnen(){
      var s = zust(), f = s.cos ? Math.cos : Math.sin;
      K.leeren();
      // Sinus: Achse durch den Hochpunkt (c ≥ 0) bzw. den Tiefpunkt (c < 0); Cosinus: durch den Tiefpunkt π.
      var achse = s.cos ? PI : (s.c < 0 ? 3 * PI / 2 : PI / 2);
      K.senkrecht(achse, 'asym hilfslinie');
      K.kurve(f, s.cos ? 'kurve gruen' : 'kurve', 0, 2 * PI);
      K.strecke(-0.6, s.c, 6.9, s.c, 'waagrechte');
      s.l.forEach(function(x, i){ K.punkt(x, s.c, s.cos ? 'p-lauf gruen' : 'p-lauf', zz(x), i % 2 ? 8 : -8, s.c > 0.6 ? 16 : -8, i % 2 ? 'start' : 'end'); });
      var fn = s.cos ? sp('tx-gruen', 'cos x') : sp('tx-blau', 'sin x');
      rolle(fig, 'formel').innerHTML = fn + ' = ' + z(s.c) + '; &nbsp;' + (s.n === 0 ? '<b>keine Lösung</b>' : s.n + (s.n === 1 ? ' Lösung' : ' Lösungen'))
        + ' in [0; 2π]' + (s.n ? ': ' + s.l.map(function(x){ return 'x ' + (zz(x).charAt(0) === '≈' ? '' : '= ') + zz(x); }).join(', ') : '')
        + '<br>Symmetrieachse x = ' + piT(achse) + ' (gestrichelt)';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(c\\). Wie viele Schnittpunkte gibt es?', ok: function(s){ return s.bewegt.c; } },
      // Startzustand: Sinus, c = 0.3, zwei Lösungen — keine Aufgabe ist schon gelöst.
      { text: 'Sinus: Stell \\(c\\) so ein, dass es in \\([0;\\, 2\\pi]\\) genau <b>eine</b> Lösung gibt.', ok: function(s){ return !s.cos && s.n === 1; } },
      { text: 'Stell \\(c\\) so ein, dass es <b>keine</b> Lösung gibt.', ok: function(s){ return s.n === 0; } },
      { text: 'Sinus: Bei welchem \\(c\\) gibt es in \\([0;\\, 2\\pi]\\) <b>drei</b> Lösungen?', ok: function(s){ return !s.cos && s.n === 3; } },
      { text: 'Schalte auf Cosinus und stell \\(\\cos x = 0.5\\) ein. Prüfe: \\(x_2 = 2\\pi - x_1\\)?', ok: function(s){ return s.cos && s.c === 0.5; } },
      { text: 'Cosinus: Bei welchem \\(c\\) liegen die beiden Lösungen genau \\(\\pi\\) auseinander?', ok: function(s){ return s.cos && s.c === 0; } }
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
    /* Eingaben: Zahl, Bruch, Dezimalkomma — und Vielfache von π: 3π/4, -π/2, 2pi, 3/4π. */
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/pi/gi, 'π').replace(/\*/g, '').replace(/^\+(?=[\dπ.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var Z = '(\\d+(?:\\.\\d+)?|\\.\\d+)', m;
      if ((m = s.match(new RegExp('^(-?)' + Z + '?π(?:/' + Z + ')?$'))))
        return { wert: (m[1] ? -1 : 1) * (m[2] ? parseFloat(m[2]) : 1) * PI / (m[3] ? parseFloat(m[3]) : 1), komma: komma };
      if ((m = s.match(new RegExp('^(-?)' + Z + '/' + Z + 'π$'))))
        return { wert: (m[1] ? -1 : 1) * parseFloat(m[2]) / parseFloat(m[3]) * PI, komma: komma };
      m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    /* Vielfaches von π in LaTeX: \tfrac{3\pi}{4}, -\tfrac{\pi}{2}, 2\pi. */
    function piTex(x){
      var b = piBruch(x); if (!b) return tz(Math.round(x * 1000) / 1000);
      var n = b[0], d = b[1]; if (n === 0) return '0';
      var zl = (Math.abs(n) === 1 ? '' : Math.abs(n)) + '\\pi';
      return (n < 0 ? '-' : '') + (d === 1 ? zl : '\\tfrac{' + zl + '}{' + d + '}');
    }
    function piEin(x){ return piT(x).replace('−', '-'); }      // so tippt man es ein
    function zT(v){
      if (Math.abs(v - Math.round(v)) < 1e-9) return tz(Math.round(v));
      if (gl(Math.abs(v), 0.5)) return (v < 0 ? '-' : '') + '\\tfrac{1}{2}';
      return tz(Math.round(v * 1e6) / 1e6);
    }
    function r3(v){ return Math.round(v * 1000) / 1000; }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15). Je Typ ein eigener
       Schlüssel (T.schl). Reihenfolge: Clips · Simulationen · Aufgaben der Kapitel · Vortest · Gesamttest. */
    var SPERRE = [
      // Clips und Simulationen
      'gb|b|270', 'gb|b|120', 'gb|b|315', 'gb|b|90', 'gb|b|180', 'gb|b|360',
      'sc|sin|6', 'sc|cos|6', 'sc|sin|9', 'sc|sin|7', 'sc|cos|10',
      'st|sin|N|0', 'st|cos|H|4', 'st|sin|T|3',
      'sy|0.5|-s',
      'tw|1', 'tw|2', 'tw|3', 'tw|4',
      'ts|N|2', 'ts|P|1',
      'kg|3|1|1', 'kg|1|4|0', 'kg|2|1|-1', 'kg|0.5|3|0', 'kg|2|2|1',
      'ag|2|2|0', 'ag|1.5|2|-0.5',
      'zl|sin|0.8', 'zl|cos|0.8', 'zl|sin|0.6', 'zl|cos|0.6', 'zl|sin|0.5', 'zl|cos|0.5',
      'an|sin|0.3|0|2', 'an|sin|1.2|0|2', 'an|sin|0.6|0|4',
      // Aufgaben der Kapitel
      'gb|b|225', 'gb|g|150',
      'sc|sin|9', 'sc|cos|6', 'sc|cos|9', 'sc|sin|7', 'sc|sin|1',
      'st|sin|H|-3', 'st|sin|H|1', 'st|sin|H|5', 'st|cos|N|-1', 'st|cos|N|1', 'st|cos|N|3',
      'sy|0.6|-s', 'sy|0.6|-c', 'sy|0.6|2s',
      'tw|3', 'tw|4', 'tw|-1',
      'kg|3|2|-1', 'kg|0.5|0.5|2', 'kg|2|2|1',
      'ag|1.5|0.5|0',
      'zl|sin|-0.3', 'zl|cos|-0.5',
      'an|sin|0.7|0|4',
      // Vortest und Gesamttest (downloads/leitprogramme/trigonometrische-funktionen/gesamttest.tex)
      'gb|b|60', 'gb|b|30', 'gb|g|300',
      'sc|sin|4', 'sc|cos|8', 'sc|sin|11',
      'sy|1.1|-s', 'sy|1.1|-c', 'sy|1.1|ps',
      'tw|-3', 'tw|6',
      'kg|2|3|-1', 'ag|2.5|2|1',
      'zl|sin|0.35', 'zl|cos|0.35', 'an|sin|0.35|0|2'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    var TYPEN = {
      /* ── Kapitel 1: vom Einheitskreis zur Kurve ──────────────────── */
      'grad-bogen': { felder: ['w'], muster: '{w}',
        schl: function(A){ return 'gb|' + A.r + '|' + A.g; },
        eingabe: function(A){ return { w: A.r === 'b' ? piEin(A.x) : String(A.g) }; },
        neu: function(){
          var g = zufall([15, 30, 45, 60, 75, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330, 360, 405, 450, 540, 720, -30, -45, -90, -180]),
              r = zufall(['b', 'g']), x = g * PI / 180;
          return { g: g, x: x, r: r,
            text: r === 'b' ? 'Rechne \\(' + tz(g) + '^\\circ\\) ins Bogenmass um — am besten exakt, als Vielfaches von \\(\\pi\\) (z. B. <code>3π/4</code> oder <code>3pi/4</code>).'
                            : 'Rechne \\(' + piTex(x) + '\\) in Grad um.',
            feld: r === 'b' ? 'Bogenmass' : 'Grad' }; },
        fehler: function(A){ var q = A.g / 180;
          return A.r === 'b' ? [[{ w: String(q) }, 'fehlt'], [{ w: String(A.g) }, 'Grad']]
                             : [[{ w: String(q) }, '180'], [{ w: String(A.g * 2) }, '180']]; },
        pruefen: function(A, e){
          if (A.r === 'b'){
            if (gl(e.w, A.x)) return null;
            if (Math.abs(e.w - A.x) < 0.001) return null;            // gerundet: gilt, die Lösung zeigt die exakte Form
            if (gl(e.w, A.g / 180)) return 'Das \\(\\pi\\) fehlt: \\(' + tz(A.g) + '^\\circ = \\tfrac{' + tz(A.g) + '}{180} \\cdot \\pi\\).';
            if (gl(e.w, A.g)) return 'Das ist noch in Grad. Teile durch \\(180\\) und multipliziere mit \\(\\pi\\).';
            return '\\(180^\\circ = \\pi\\). Also \\(' + tz(A.g) + '^\\circ = \\tfrac{' + tz(A.g) + '}{180}\\,\\pi\\) — gekürzt.';
          }
          if (gl(e.w, A.g)) return null;
          if (gl(e.w, A.g / 180)) return 'Das ist der Faktor vor \\(\\pi\\). In Grad: \\(\\pi\\) durch \\(180^\\circ\\) ersetzen.';
          var q = piBruch(A.x);
          return 'Ersetze \\(\\pi\\) durch \\(180^\\circ\\): \\(' + piTex(A.x) + ' = ' + (q[1] === 1 ? tz(q[0]) : '\\tfrac{' + tz(q[0]) + '}{' + q[1] + '}') + ' \\cdot 180^\\circ\\).'; },
        richtig: function(A){ return A.r === 'b' ? '\\(' + tz(A.g) + '^\\circ = ' + piTex(A.x) + '\\)' : ''; },
        loesung: function(A){ return tz(A.g) + '^\\circ = \\tfrac{' + tz(A.g) + '}{180}\\,\\pi = ' + piTex(A.x); } },

      'sin-cos-wert': { felder: ['y'], muster: 'Wert = {y}',
        schl: function(A){ return 'sc|' + A.fn + '|' + A.k; },
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){
          // Nur Stellen mit «schönen» Werten 0, ±1, ±1/2: Vielfache von π/2, beim Sinus die π/6-Familie,
          // beim Cosinus die π/3-Familie (k in Zwölfteln von π: x = kπ/12 … hier in Sechsteln).
          var fn = zufall(['sin', 'cos']);
          var ks = fn === 'sin' ? [0, 1, 3, 5, 6, 7, 9, 11, 12] : [0, 2, 3, 4, 6, 8, 9, 10, 12];
          var k = zufall(ks), x = k * PI / 6, y = Math.round((fn === 'sin' ? Math.sin(x) : Math.cos(x)) * 2) / 2;
          return { fn: fn, k: k, x: x, y: y,
            text: 'Gib ohne Taschenrechner an: \\(\\' + fn + '\\left(' + piTex(x) + '\\right)\\).' }; },
        fehler: function(A){ var f = [], ander = Math.round((A.fn === 'sin' ? Math.cos(A.x) : Math.sin(A.x)) * 2) / 2;
          var andergut = Math.abs((A.fn === 'sin' ? Math.cos(A.x) : Math.sin(A.x)) - ander) < 1e-9;
          if (A.y !== 0) f.push([{ y: String(-A.y) }, 'Vorzeichen']);
          if (andergut && !gl(ander, A.y) && !gl(ander, -A.y)) f.push([{ y: String(ander) }, 'Koordinate']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          var anderW = A.fn === 'sin' ? Math.cos(A.x) : Math.sin(A.x);
          if (A.y !== 0 && gl(e.y, -A.y)) return 'Vorzeichen: Bei \\(' + piTex(A.x) + '\\) liegt \\(P\\) ' + (A.fn === 'sin' ? (A.y < 0 ? 'unter' : 'über') + ' der waagrechten Achse.' : (A.y < 0 ? 'links' : 'rechts') + ' der senkrechten Achse.');
          if (gl(e.y, anderW)) return 'Das ist die andere Koordinate. Der ' + (A.fn === 'sin' ? 'Sinus ist die Höhe von \\(P\\).' : 'Cosinus ist die waagrechte Koordinate von \\(P\\).');
          return 'Zeichne \\(P\\) bei \\(' + piTex(A.x) + '\\) auf den Einheitskreis: ' + (A.fn === 'sin' ? 'Wie hoch liegt er?' : 'Wie weit links oder rechts liegt er?'); },
        loesung: function(A){ return '\\' + A.fn + '\\left(' + piTex(A.x) + '\\right) = ' + zT(A.y); } },

      /* ── Kapitel 2: Periode und Symmetrie ───────────────────────── */
      'stelle': { felder: ['x'], muster: 'x = {x}',
        schl: function(A){ return 'st|' + A.fn + '|' + A.art + '|' + Math.round(A.x * 2 / PI); },
        eingabe: function(A){ return { x: piEin(A.x) }; },
        neu: function(){
          var fn = zufall(['sin', 'cos']), art = zufall(['N', 'H', 'T']);
          // Stellen in Halben von π: Sinus N = 2k, H = 1 + 4k, T = 3 + 4k; Cosinus N = 1 + 2k, H = 4k, T = 2 + 4k.
          var h = [];
          for (var j = -8; j <= 8; j++){
            var m = ((j % 4) + 4) % 4;
            var ist = fn === 'sin' ? (art === 'N' ? m % 2 === 0 : art === 'H' ? m === 1 : m === 3)
                                   : (art === 'N' ? m % 2 === 1 : art === 'H' ? m === 0 : m === 2);
            if (ist) h.push(j);
          }
          var j0 = zufall(h), x = j0 * PI / 2;
          // Intervall um x: links und rechts π/6, π/4 oder π/3 — kleiner als der halbe Abstand zur nächsten Stelle.
          var d1 = zufall([PI / 6, PI / 4, PI / 3]), d2 = zufall([PI / 6, PI / 4, PI / 3]);
          var name = { N: 'Nullstelle', H: 'Hochstelle', T: 'Tiefstelle' }[art];
          return { fn: fn, art: art, x: x, a: x - d1, b: x + d2,
            text: 'Welche ' + name + ' hat \\(y = \\' + fn + ' x\\) zwischen \\(' + piTex(x - d1) + '\\) und \\(' + piTex(x + d2) + '\\)?' }; },
        fehler: function(A){
          // Verwechslung Sinus/Cosinus: um π/2 daneben; andere Art derselben Funktion: um π daneben (bei Extremstellen).
          var f = [[{ x: piEin(A.x + PI / 2) }, null]];
          if (A.art !== 'N') f.push([{ x: piEin(A.x + PI) }, 'gesucht']);
          f.push([{ x: piEin(A.x + 2 * PI) }, 'Intervall']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) || Math.abs(e.x - A.x) < 0.001) return null;
          var j = e.x * 2 / PI, ganz = Math.abs(j - Math.round(j)) < 1e-6, m = ((Math.round(j) % 4) + 4) % 4;
          var name = { N: 'Nullstelle', H: 'Hochstelle', T: 'Tiefstelle' };
          if (ganz){
            var artE = A.fn === 'sin' ? (m % 2 === 0 ? 'N' : m === 1 ? 'H' : 'T') : (m % 2 === 1 ? 'N' : m === 0 ? 'H' : 'T');
            if (artE !== A.art) return 'Bei \\(' + piTex(e.x) + '\\) hat \\(\\' + A.fn + ' x\\) eine ' + name[artE] + ' — gesucht ist eine ' + name[A.art] + '.';
            if (e.x < A.a || e.x > A.b) return 'Richtige Art, aber \\(' + piTex(e.x) + '\\) liegt nicht im Intervall von \\(' + piTex(A.a) + '\\) bis \\(' + piTex(A.b) + '\\). ' + (A.art === 'N' ? 'Nullstellen liegen \\(\\pi\\) auseinander.' : 'Gleiche Stellen liegen eine Periode \\(2\\pi\\) auseinander.');
          }
          return 'Skizziere \\(y = \\' + A.fn + ' x\\) mit den Stützstellen bei Vielfachen von \\(\\tfrac{\\pi}{2}\\) und lies im Intervall ab.'; },
        loesung: function(A){ return 'x = ' + piTex(A.x); } },

      'symmetrie-wert': { felder: ['y'], muster: 'Wert ≈ {y}',
        schl: function(A){ return 'sy|' + A.c + '|' + A.q; },
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){
          var c = zufall([0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3]), s = r3(Math.sin(c)), co = r3(Math.cos(c));
          var q = zufall(['-s', '-c', '2s', '2c', 'ps']);
          var F = { '-s': ['\\sin(-' + c + ')', -s, 's'], '-c': ['\\cos(-' + c + ')', co, 'c'],
                    '2s': ['\\sin(' + c + ' + 2\\pi)', s, 's'], '2c': ['\\cos(' + c + ' - 2\\pi)', co, 'c'],
                    'ps': ['\\sin(\\pi - ' + c + ')', s, 's'] }[q];
          return { c: c, s: s, co: co, q: q, aus: F[0], y: F[1], f: F[2],
            text: 'Es gilt \\(\\sin ' + c + ' \\approx ' + s + '\\) und \\(\\cos ' + c + ' \\approx ' + co + '\\). Gib ohne Taschenrechner an: \\(' + F[0] + '\\).' }; },
        fehler: function(A){ return [[{ y: String(-A.y) }, 'Vorzeichen'], [{ y: String(A.f === 's' ? A.co : (A.q === '-c' ? -A.s : A.s)) }, 'Gefragt']]; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, -A.y)) return A.q === '-s' ? 'Vorzeichen: Die Sinuskurve ist punktsymmetrisch zum Ursprung, \\(\\sin(-x) = -\\sin x\\).'
            : A.q === '-c' ? 'Vorzeichen: Die Cosinuskurve ist achsensymmetrisch zur \\(y\\)-Achse, \\(\\cos(-x) = \\cos x\\).'
            : A.q === 'ps' ? 'Vorzeichen: \\(\\sin(\\pi - x) = \\sin x\\) — die Sinuskurve ist symmetrisch zur Geraden \\(x = \\tfrac{\\pi}{2}\\).'
            : 'Vorzeichen: Nach einer vollen Periode \\(2\\pi\\) ist alles wie vorher.';
          if (gl(e.y, A.co) || gl(e.y, A.s) || gl(e.y, -A.s) || gl(e.y, -A.co)) return 'Gefragt ist der ' + (A.f === 's' ? 'Sinus' : 'Cosinus') + ', nicht der ' + (A.f === 's' ? 'Cosinus' : 'Sinus') + '.';
          return 'Nutze Symmetrie oder Periode: \\(\\sin(-x) = -\\sin x\\), \\(\\cos(-x) = \\cos x\\), \\(\\sin(\\pi - x) = \\sin x\\), Periode \\(2\\pi\\).'; },
        loesung: function(A){ return A.aus + ' \\approx ' + A.y; } },

      /* ── Kapitel 3: die Tangensfunktion ──────────────────────────── */
      'tan-wert': { felder: ['y'], muster: 'tan x = {y:−1|0|1|nicht definiert}',
        schl: function(A){ return 'tw|' + A.k; },
        eingabe: function(A){ return { y: A.w }; },
        neu: function(){
          var k = zufall([-7, -6, -5, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]), m = ((k % 4) + 4) % 4;
          var w = m === 0 ? '0' : m === 2 ? 'nicht definiert' : (m === 1 ? '1' : '−1');
          return { k: k, x: k * PI / 4, w: w, text: 'Gib ohne Taschenrechner an: \\(\\tan\\left(' + piTex(k * PI / 4) + '\\right)\\).' }; },
        fehler: function(A){
          if (A.w === 'nicht definiert') return [[{ y: '0' }, 'Cosinus']];
          if (A.w === '0') return [[{ y: 'nicht definiert' }, 'Sinus']];
          return [[{ y: A.w === '1' ? '−1' : '1' }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          if (e.y === A.w) return null;
          if (A.w === 'nicht definiert') return 'Wie gross ist der Cosinus bei \\(' + piTex(A.x) + '\\)? Kann man durch ihn teilen?';
          if (A.w === '0') return 'Wie gross ist der Sinus bei \\(' + piTex(A.x) + '\\) — und was ergibt das im Zähler von \\(\\tfrac{\\sin x}{\\cos x}\\)?';
          if (e.y === 'nicht definiert' || e.y === '0') return 'Bei \\(' + piTex(A.x) + '\\) sind Sinus und Cosinus gleich gross bis aufs Vorzeichen — der Quotient ist \\(\\pm 1\\).';
          return 'Vorzeichen: In welchem Quadranten liegt \\(P\\)? Haben Sinus und Cosinus dort dasselbe Vorzeichen?'; },
        loesung: function(A){ return '\\tan\\left(' + piTex(A.x) + '\\right)' + (A.w === 'nicht definiert' ? '\\text{ ist nicht definiert}' : ' = ' + A.w.replace('−', '-')); } },

      'tan-stelle': { felder: ['x'], muster: 'x = {x}',
        schl: function(A){ return 'ts|' + A.art + '|' + Math.round(A.x * 2 / PI); },
        eingabe: function(A){ return { x: piEin(A.x) }; },
        neu: function(){
          var art = zufall(['P', 'N']), j = zufall([-3, -2, -1, 0, 1, 2, 3]);
          var x = art === 'N' ? j * PI : PI / 2 + j * PI;
          var d1 = zufall([PI / 6, PI / 4, PI / 3]), d2 = zufall([PI / 6, PI / 4, PI / 3]);
          return { art: art, x: x, a: x - d1, b: x + d2,
            text: 'Welche ' + (art === 'P' ? 'Polstelle' : 'Nullstelle') + ' hat \\(y = \\tan x\\) zwischen \\(' + piTex(x - d1) + '\\) und \\(' + piTex(x + d2) + '\\)?' }; },
        fehler: function(A){ return [[{ x: piEin(A.x + PI / 2) }, A.art === 'P' ? 'Cosinus' : 'Sinus'], [{ x: piEin(A.x + PI) }, 'Intervall']]; },
        pruefen: function(A, e){
          if (gl(e.x, A.x) || Math.abs(e.x - A.x) < 0.001) return null;
          var j = e.x * 2 / PI, ganz = Math.abs(j - Math.round(j)) < 1e-6, pol = ganz && Math.abs(Math.round(j)) % 2 === 1;
          if (ganz && (pol ? 'P' : 'N') !== A.art) return A.art === 'P' ? 'Dort ist \\(\\tan x = 0\\), eine Nullstelle. Pole liegen, wo der Cosinus \\(0\\) ist.'
                                                                        : 'Dort ist ein Pol. Nullstellen liegen, wo der Sinus \\(0\\) ist.';
          if (ganz) return 'Richtige Art, aber \\(' + piTex(e.x) + '\\) liegt nicht im Intervall von \\(' + piTex(A.a) + '\\) bis \\(' + piTex(A.b) + '\\).';
          return A.art === 'P' ? 'Pole bei \\(\\tfrac{\\pi}{2} + k\\pi\\): Welche liegt im Intervall?' : 'Nullstellen bei \\(k\\pi\\): Welche liegt im Intervall?'; },
        loesung: function(A){ return 'x = ' + piTex(A.x); } },

      /* ── Kapitel 4: Strecken und Verschieben ─────────────────────── */
      'kenngroessen': { felder: ['a', 'p', 'v'], muster: 'Amplitude {a} &nbsp; Periodenlänge {p} &nbsp; Mittellinie y = {v}',
        schl: function(A){ return 'kg|' + A.a + '|' + A.b + '|' + A.v; },
        eingabe: function(A){ return { a: String(A.a), p: piEin(A.p), v: String(A.v) }; },
        neu: function(){
          var a = zufall([0.5, 1.5, 2, 3, 4, 5]), b = zufall([0.5, 2, 3, 4, 6]), v = zufall([-3, -2, -1, 0, 1, 2, 4]);
          var bT = b === 0.5 ? '\\tfrac{x}{2}' : b + 'x';
          return { a: a, b: b, v: v, p: 2 * PI / b,
            text: 'Gib Amplitude, Periodenlänge und Mittellinie an: \\(y = ' + a + '\\sin(' + bT + ')' + (v === 0 ? '' : (v > 0 ? ' + ' : ' - ') + Math.abs(v)) + '\\).' }; },
        fehler: function(A){ var f = [[{ a: String(A.a), p: piEin(2 * PI * A.b), v: String(A.v) }, 'Periode']];
          if (A.v !== 0 && A.v !== A.a) f.push([{ a: String(A.a + A.v), p: piEin(A.p), v: String(A.v) }, 'Amplitude']);
          if (A.v !== 0 && A.v !== A.a) f.push([{ a: String(A.v), p: piEin(A.p), v: String(A.a) }, 'Amplitude']);
          return f; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.a, A.a) && (gl(e.p, A.p) || Math.abs(e.p - A.p) < 0.001) && gl(e.v, A.v)) return null;
          if (!gl(e.a, A.a)) r.push(gl(e.a, A.v) ? 'Amplitude und Mittellinie vertauscht: Die Amplitude steht vor dem Sinus.' : 'Amplitude: Welcher Faktor steht vor dem Sinus? Die Mittellinie zählt nicht dazu.');
          if (!(gl(e.p, A.p) || Math.abs(e.p - A.p) < 0.001)) r.push(gl(e.p, 2 * PI * A.b) ? 'Periode: \\(2\\pi\\) <b>durch</b> \\(b\\), nicht mal \\(b\\). Grösseres \\(b\\) heisst kürzere Periode.' : 'Periode: \\(p = \\tfrac{2\\pi}{b}\\) mit \\(b = ' + A.b + '\\).');
          if (!gl(e.v, A.v) && !(gl(e.v, A.a) && gl(e.a, A.v))) r.push(gl(e.v, A.a) ? 'Mittellinie: der Summand hinter dem Sinus, nicht die Amplitude.' : 'Mittellinie: der Summand hinter dem Sinus.');
          return r.join(' '); },
        loesung: function(A){ return 'a = ' + A.a + ',\\ p = \\tfrac{2\\pi}{' + A.b + '} = ' + piTex(A.p) + ',\\ y = ' + A.v; } },

      'aus-graph': { felder: ['a', 'b', 'v'], muster: 'y = {a} · sin({b} x) + {v}',
        schl: function(A){ return 'ag|' + A.a + '|' + A.b + '|' + A.v; },
        eingabe: function(A){ return { a: String(A.a), b: String(A.b), v: String(A.v) }; },
        neu: function(){
          var a, b, v;
          do { a = zufall([0.5, 1, 1.5, 2, 2.5, 3]); b = zufall([0.5, 1, 2, 3]); v = zufall([-1, 0, 1]); } while (a + Math.abs(v) > 3.5 || (a === 1 && b === 1 && v === 0));
          return { a: a, b: b, v: v, text: 'Bestimme \\(a\\), \\(b\\) und \\(v\\) der abgebildeten Kurve \\(y = a \\cdot \\sin(b\\,x) + v\\) (mit \\(a \\gt 0\\)).' }; },
        zeichne: function(svg, A){
          var x1 = A.b === 0.5 ? 4 * PI + 0.4 : 2 * PI + 0.4;
          svg.setAttribute('viewBox', '0 0 300 170');
          var xm = A.b === 0.5 ? [[PI, 'π'], [2 * PI, '2π'], [3 * PI, '3π'], [4 * PI, '4π']] : PIM;
          var K = Achsen(svg, { w: 300, h: 170, x0: -0.5, x1: x1, y0: -4, y1: 4, sx: A.b === 0.5 ? PI / 2 : A.b === 3 ? PI / 6 : PI / 4, sy: 0.5, r: 3, pfeil: 6,
            xm: xm, ym: [[-3, '−3'], [-2, '−2'], [-1, '−1'], [1, '1'], [2, '2'], [3, '3']] });
          K.kurve(function(x){ return A.a * Math.sin(A.b * x) + A.v; }, 'kurve');
        },
        fehler: function(A){ var f = [];
          if (A.b !== 1) f.push([{ a: String(A.a), b: String(1 / A.b), v: String(A.v) }, 'Periode']);
          f.push([{ a: String(2 * A.a), b: String(A.b), v: String(A.v) }, 'Amplitude']);
          return f; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.a, A.a) && gl(e.b, A.b) && gl(e.v, A.v)) return null;
          if (!gl(e.a, A.a)) r.push(gl(e.a, 2 * A.a) ? 'Amplitude: halber Abstand zwischen höchstem und tiefstem Wert, nicht der ganze.' : 'Amplitude: Wie weit geht die Kurve über die Mittellinie hinaus?');
          if (!gl(e.b, A.b)) r.push(gl(e.b, 1 / A.b) ? 'Periode und \\(b\\) verwechselt: \\(b = \\tfrac{2\\pi}{p}\\).' : 'Lies die Periode \\(p\\) ab — von Hochpunkt zu Hochpunkt, oder zähle, wie viele Perioden in \\(2\\pi\\) passen — und rechne \\(b = \\tfrac{2\\pi}{p}\\).');
          if (!gl(e.v, A.v)) r.push('Mittellinie: genau in der Mitte zwischen höchstem und tiefstem Wert.');
          return r.join(' '); },
        loesung: function(A){ return 'p = ' + piTex(2 * PI / A.b) + ' \\Rightarrow b = ' + A.b + ',\\ a = ' + A.a + ',\\ v = ' + A.v; } },

      /* ── Kapitel 5: Symmetrie nutzen (mit Taschenrechner) ─────────── */
      'zweite-loesung': { felder: ['x'], muster: 'x₂ ≈ {x}',
        schl: function(A){ return 'zl|' + A.fn + '|' + A.c; },
        eingabe: function(A){ return { x: String(A.x2) }; },
        neu: function(){
          var fn = zufall(['sin', 'cos']);
          var c = fn === 'sin' ? zufall([-0.7, -0.4, -0.2, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.9]) : zufall([-0.9, -0.7, -0.4, -0.3, -0.2, 0.1, 0.2, 0.4, 0.7, 0.9]);
          var x1 = fn === 'sin' ? Math.asin(c) : Math.acos(c);
          // Sinus mit c < 0: Der Rechner gibt ein negatives x1. Eine Lösung ist x1 + 2π, gesucht die andere, π − x1.
          var neg = x1 < 0;
          return { fn: fn, c: c, x1: r3(x1), x2: r3(fn === 'sin' ? PI - x1 : 2 * PI - x1), x1w: x1, neg: neg,
            text: 'Der Taschenrechner (Bogenmass) liefert für \\(\\' + fn + ' x = ' + c + '\\) die Lösung \\(x_1 \\approx ' + r3(x1) + '\\).'
              + (neg ? ' Sie liegt nicht in \\([0;\\, 2\\pi]\\); dort liegt \\(x_1 + 2\\pi \\approx ' + r3(x1 + 2 * PI) + '\\). Gib die andere Lösung in \\([0;\\, 2\\pi]\\) an, auf drei Dezimalen.'
                     : ' Gib die zweite Lösung in \\([0;\\, 2\\pi]\\) an, auf drei Dezimalen.') }; },
        fehler: function(A){ return A.fn === 'sin' ? [[{ x: String(r3(2 * PI - A.x1w)) }, 'Cosinus'], [{ x: String(r3(PI + A.x1w)) }, 'Vorzeichen']]
                                                    : [[{ x: String(r3(PI - A.x1w)) }, 'Sinus'], [{ x: String(r3(PI + A.x1w)) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          if (Math.abs(e.x - A.x2) < 0.0015) return null;
          if (A.fn === 'sin' && Math.abs(e.x - (2 * PI - A.x1w)) < 0.0015) return 'Das ist die Regel beim Cosinus. Die Sinuskurve ist symmetrisch zur Geraden \\(x = \\tfrac{\\pi}{2}\\): \\(x_2 = \\pi - x_1\\).';
          if (A.fn === 'cos' && Math.abs(e.x - (PI - A.x1w)) < 0.0015) return 'Das ist die Regel beim Sinus. Die Cosinuskurve ist symmetrisch zur Geraden \\(x = \\pi\\): \\(x_2 = 2\\pi - x_1\\).';
          if (Math.abs(e.x - (PI + A.x1w)) < 0.0015) return 'Dort hat der ' + (A.fn === 'sin' ? 'Sinus' : 'Cosinus') + ' das umgekehrte Vorzeichen. Nutze die Symmetrieachse \\(x = ' + (A.fn === 'sin' ? '\\tfrac{\\pi}{2}' : '\\pi') + '\\).';
          if (Math.abs(e.x - A.x1) < 0.0015 || (A.neg && Math.abs(e.x - (A.x1w + 2 * PI)) < 0.0015)) return 'Das ist die schon bekannte Lösung. Gesucht ist die andere.';
          return A.fn === 'sin' ? 'Sinus: \\(x_2 = \\pi - x_1\\).' : 'Cosinus: \\(x_2 = 2\\pi - x_1\\).'; },
        loesung: function(A){ return 'x_2 = ' + (A.fn === 'sin' ? '\\pi' : '2\\pi') + ' - ' + A.x1 + ' \\approx ' + A.x2; } },

      'anzahl-loesungen': { felder: ['n'], muster: 'Anzahl Lösungen: {n}',
        schl: function(A){ return 'an|' + A.fn + '|' + A.c + '|' + A.L + '|' + A.R; },
        eingabe: function(A){ return { n: String(A.n) }; },
        neu: function(){
          var fn = zufall(['sin', 'cos']), c = zufall([-1.2, -1, -0.6, -0.5, 0, 0.2, 0.5, 0.8, 1, 1.5]);
          var ber = zufall([[0, 2], [0, 4], [0, 3], [-1, 1], [-2, 2], [0, 1]]);
          var Ls = loesungen(fn === 'cos', c, ber[0] * PI, ber[1] * PI);
          return { fn: fn, c: c, L: ber[0], R: ber[1], n: Ls.length,
            text: 'Wie viele Lösungen hat \\(\\' + fn + ' x = ' + c + '\\) im Intervall \\([' + piTex(ber[0] * PI) + ';\\, ' + piTex(ber[1] * PI) + ']\\)?' }; },
        fehler: function(A){ var f = [[{ n: String(A.n + 1) }, null]]; if (A.n > 0) f.push([{ n: String(A.n - 1) }, null]); return f; },
        pruefen: function(A, e){
          if (gl(e.n, A.n)) return null;
          if (Math.abs(A.c) > 1) return 'Die Werte von \\(\\' + A.fn + ' x\\) liegen zwischen \\(-1\\) und \\(1\\). Erreicht die Waagrechte \\(y = ' + A.c + '\\) die Kurve?';
          if (Math.abs(A.c) === 1) return 'Bei \\(c = ' + A.c + '\\) berührt die Waagrechte die Kurve nur in ' + (A.c > 0 ? 'Hoch' : 'Tief') + 'punkten — einer pro Periode. Zähle sie im Intervall, die Ränder eingeschlossen.';
          return 'Skizziere \\(y = \\' + A.fn + ' x\\) im Intervall und die Waagrechte \\(y = ' + A.c + '\\). Zähle die Schnittpunkte, auch auf dem Rand.'; },
        loesung: function(A){ return A.n + '\\text{ Lösung' + (A.n === 1 ? '' : 'en') + '}'; } }
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
        var html = A.feld ? A.feld + ' = ' + T.muster + (A.feld === 'Grad' ? ' °' : '') : T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
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
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('select') ? 'Wähle aus.' : 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-3</code>, <code>0.5</code>, <code>1/2</code> — oder mit π: <code>3π/4</code>, <code>-pi/2</code>, <code>2pi</code>.'; return; }
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

  /* ---------- Minigrafen: <svg class="mini" data-t="s,a,b,u,v;c,…;t,…"> für
       y = a·sin(b(x − u)) + v (s), a·cos(b(x − u)) + v (c), a·tan(b(x − u)) + v (t); die erste
       Kurve in ihrer Farbe (sin blau, cos grün, tan orange), weitere gestrichelt. Dazu
       data-fenster="x0,x1,y0,y1", data-punkte="x,y;…", data-waagrecht="c" (Waagrechte y = c),
       data-xpi="1" (x-Achse in Vielfachen von π/2 beschriftet), data-xteil="6" (Gitter alle π/6),
       data-senkrecht="x,…" (Polgeraden, gestrichelt), data-ym="…", data-titel. ---------- */
  document.querySelectorAll('svg.mini[data-t]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-0.5,6.9,-1.5,1.5').split(',').map(Number);
    var w = 300, h = 150;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h); svg.setAttribute('role', 'img');
    var xm = [];
    for (var j = Math.ceil(fe[0] / (PI / 2)); j * PI / 2 <= fe[1]; j++) if (j !== 0) xm.push([j * PI / 2, (svg.dataset.xpi === '1' || j % 2 === 0) ? piT(j * PI / 2) : '']);
    var ym = svg.dataset.ym ? svg.dataset.ym.split(',').map(Number) : [-1, 1];
    var K = Achsen(svg, { w: w, h: h, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, sx: PI / (+svg.dataset.xteil || 2), sy: +svg.dataset.sy || 1, pfeil: 6,
      xm: xm.filter(function(t){ return t[1]; }), ym: ym });
    if (svg.dataset.senkrecht) svg.dataset.senkrecht.split(',').forEach(function(x){ K.senkrecht(+x, 'asym'); });
    if (svg.dataset.waagrecht) K.strecke(fe[0], +svg.dataset.waagrecht, fe[1], +svg.dataset.waagrecht, 'waagrechte');
    svg.dataset.t.split(';').filter(Boolean).forEach(function(s, i){
      var p = s.split(','), art = p[0], q = p.slice(1).map(Number);
      var fn = art === 's' ? Math.sin : art === 'c' ? Math.cos : function(t){ return Math.abs(Math.cos(t)) < 1e-6 ? null : Math.tan(t); };
      var farbe = art === 's' ? 'kurve' : art === 'c' ? 'kurve gruen' : 'kurve orange';
      K.kurve(function(x){ var y = fn(q[1] * (x - q[2])); return y === null ? null : q[0] * y + q[3]; }, i ? farbe + ' gestrichelt' : farbe);
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){
      var a = p.split(',').map(Number);
      K.punkt(a[0], a[1], 'p-pkt');
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
