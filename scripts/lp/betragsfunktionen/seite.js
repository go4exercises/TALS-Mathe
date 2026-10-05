<script>
/* Leitprogramm Betragsfunktionen — Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Notation wie auf Themenseite 3.6: |x| abschnittsweise, y = a·|x − u| + v mit
   Knickpunkt (u | v), Umklapp-Prinzip y = |f(x)|, Wanne y = |x − a| + |x − b|.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = Betragskurve · orange = Waagrechte y = c und Lösungen · grün = Äste als Geraden
   (abschnittsweise Terme) · rot = Gegenbeispiel · Tinte = f vor dem Betrag, Symmetrieachse.
   Zahlen mit Dezimalpunkt und echtem Minus. */
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

  function ohneNull(inp){
    var letzt = +inp.value, st = parseFloat(inp.step) || 1;
    inp.addEventListener('input', function(){
      if (+inp.value === 0) inp.value = letzt > 0 ? -st : st;
      letzt = +inp.value;
    });
  }
  function vor(v){ return v < 0 ? '− ' + z(-v) : '+ ' + z(v); }
  /* Betragsterm |x − m| als Text: |x|, |x − 2|, |x + 3| */
  function betragT(m){ return m === 0 ? '|x|' : '|x ' + (m > 0 ? '− ' + z(m) : '+ ' + z(-m)) + '|'; }
  var XM = [-4, -2, 2, 4];

  /* ---------- Kapitel 1: die Betragsfunktion ----------
     Unterschied zur Einstiegsanimation «Abstand zum Bahnhof» der Themenseite: Dort ist der
     Bezugspunkt fest bei 6. Hier lassen sich Bezugspunkt m und Läufer x einstellen; die Anzeige
     nennt den Fall (x ≥ m oder x < m) und den Term ohne Betragsstriche, die beiden Äste sind
     als ganze Geraden gestrichelt mitgezeichnet. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 260, x0: -6, x1: 6, y0: -2, y1: 8, sy: 1, xm: XM, ym: [2, 4, 6] });
    var pruefen = function(){}, bewegt = {}, seiten = {};
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r); if (bewegt.x) seiten[w.x >= w.m ? 'r' : 'l'] = true;
      return { m: w.m, x: w.x, y: Math.abs(w.x - w.m), beide: seiten.r && seiten.l, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; seiten = {}; } };
    function zeichnen(){
      var s = zust(), m = s.m, x = s.x;
      K.leeren();
      K.kurve(function(t){ return t - m; }, 'ast hilfslinie');
      K.kurve(function(t){ return m - t; }, 'ast hilfslinie');
      K.kurve(function(t){ return Math.abs(t - m); }, 'kurve');
      K.strecke(m, 0, x, 0, 'abstand');
      K.punkt(m, 0, 'p-pkt', 'u', -4, 16, 'end');
      K.punkt(x, s.y, 'p-lauf', '(' + z(x) + ' | ' + z(s.y) + ')', x > 2 ? -8 : 8, -8, x > 2 ? 'end' : 'start');
      var rechts = x >= m;
      var innen = m === 0 ? 'x' : 'x ' + vor(-m);
      rolle(fig, 'formel').innerHTML = 'y = ' + sp('tx-blau', betragT(m)) + ' &nbsp;·&nbsp; x = ' + z(x)
        + (rechts ? ' ≥ u: ' + sp('tx-gruen', 'y = ' + innen) : ' &lt; u: ' + sp('tx-gruen', 'y = −(' + innen + ')'))
        + ' = ' + z(s.y);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh den Läufer \\(x\\) einmal links und einmal rechts an \\(u\\) vorbei. Welcher Term gilt wo?', ok: function(s){ return s.beide; } },
      // Startzustand u = 0, x = 2.5 — keine Aufgabe ist schon gelöst.
      { text: 'Lass \\(u = 0\\): Stell ein negatives \\(x\\) mit \\(|x| = 3.5\\) ein.', ok: function(s){ return s.m === 0 && s.x === -3.5; } },
      { text: 'Lass \\(u = 0\\): Wo ist der Betrag null?', ok: function(s){ return s.m === 0 && s.x === 0; } },
      { text: 'Stell \\(u = 2\\) ein. Wo links von \\(u\\) ist der Abstand zu \\(u\\) gleich \\(3\\)?', ok: function(s){ return s.m === 2 && s.x === -1; } },
      { text: 'Stell \\(u = -2\\) ein. Wo rechts von \\(u\\) ist der Abstand \\(4\\)?', ok: function(s){ return s.m === -2 && s.x === 2; } },
      { text: 'Bei \\(u = 1\\) haben zwei Stellen den Abstand \\(2.5\\). Stell die rechte ein.', ok: function(s){ return s.m === 1 && s.x === 3.5; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: das V verschieben und strecken ----------
     Unterschied zum «V-Labor» der Themenseite: dort mit Wertetabelle. Hier mit Ziel-V, und die
     Anzeige nennt Knickpunkt, Ast-Steigungen und Öffnung live. a springt über die 0 hinweg. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -6, x1: 6, y0: -6, y1: 6, sy: 1, xm: XM, ym: [-4, -2, 2, 4] });
    var pruefen = function(){}, bewegt = {}, ziel = null;
    ohneNull(fig.querySelector('input[data-p="a"]'));
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r); return { a: w.a, u: w.u, v: w.v, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; ziel = null; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      if (ziel) K.kurve(function(x){ return ziel[0] * Math.abs(x - ziel[1]) + ziel[2]; }, 'zielkurve');
      K.kurve(Math.abs, 'normal');
      K.senkrecht(s.u, 'asym hilfslinie');
      K.kurve(function(x){ return s.a * Math.abs(x - s.u) + s.v; }, 'kurve');
      K.punkt(s.u, s.v, 'p-pkt', '(' + z(s.u) + ' | ' + z(s.v) + ')', 8, s.a > 0 ? 16 : -8);
      rolle(fig, 'formel').innerHTML = 'y = ' + sp('tx-blau', z(s.a)) + ' · ' + betragT(s.u) + (s.v === 0 ? '' : ' ' + vor(s.v))
        + '<br><span class="nb">Knick (' + z(s.u) + ' | ' + z(s.v) + ')</span> &nbsp;·&nbsp; <span class="nb">Steigung links ' + z(-s.a) + ', rechts ' + z(s.a) + '</span>'
        + ' &nbsp;·&nbsp; <span class="nb">' + (s.a > 0 ? 'V (nach oben offen)' : 'Dach (nach unten offen)') + '</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(a\\), auch unter null. Was geschieht mit den Ästen?', ok: function(s){ return s.bewegt.a; } },
      // Startzustand a = 1, u = 0, v = 0 — das V liegt auf |x|, keine Aufgabe ist gelöst.
      { text: 'Leg den Knick nach \\((-2 \\mid 1)\\).', ok: function(s){ return s.u === -2 && s.v === 1; } },
      { text: 'Der rechte Ast soll mit der Steigung \\(0.5\\) steigen.', ok: function(s){ return s.a === 0.5; } },
      { text: 'Bau ein Dach mit der Spitze bei \\((1 \\mid 3)\\).', ok: function(s){ return s.a < 0 && s.u === 1 && s.v === 3; } },
      { text: 'Ein V mit den Ast-Steigungen \\(\\pm 1\\) und den Nullstellen \\(x = -1\\) und \\(x = 3\\).', ok: function(s){ return s.a === 1 && s.u === 1 && s.v === -2; } },
      { text: 'Triff die blass gezeichnete Zielkurve.', setup: function(){ ziel = [1.5, -1.5, -2]; },
        ok: function(s){ return s.a === 1.5 && s.u === -1.5 && s.v === -2; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: das Umklapp-Prinzip ----------
     Unterschied zum «Umklapp-Labor» der Themenseite (drei feste Funktionen zum Durchschalten):
     Hier sind Gerade und Parabel verstellbar, die Knicke stehen mit ihren Koordinaten im Bild. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -5, x1: 5, y0: -5, y1: 5, sy: 1, xm: XM, ym: [-4, -2, 2, 4] });
    var pruefen = function(){}, bewegt = {};
    var schalter = fig.querySelector('.sim-schalter input');
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    if (schalter) schalter.addEventListener('change', zeichnen);
    function zust(){ var w = werte(r), par = !!(schalter && schalter.checked);
      r.m.disabled = par;
      var f = par ? function(x){ return x * x + w.q; } : function(x){ return w.m * x + w.q; };
      var nst = par ? (w.q < 0 ? [-Math.sqrt(-w.q), Math.sqrt(-w.q)] : []) : (w.m !== 0 ? [-w.q / w.m] : []);
      return { m: w.m, q: w.q, par: par, f: f, nst: nst, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      K.kurve(s.f, 'normal');
      K.kurve(function(x){ return Math.abs(s.f(x)); }, 'kurve');
      if (!(s.par && s.q === 0)) s.nst.forEach(function(x, i){ K.punkt(x, 0, 'p-pkt', '(' + zz(x) + ' | 0)', i ? 8 : -8, 16, i ? 'start' : 'end'); });
      if (s.par && s.q < 0) K.punkt(0, -s.q, 'p-lauf', '(0 | ' + z(-s.q) + ')', 8, -8);
      var rest = s.q === 0 ? '' : ' ' + vor(s.q);
      var fT = s.par ? 'x²' + rest : (s.m === 0 ? z(s.q) : (s.m === 1 ? '' : s.m === -1 ? '−' : z(s.m)) + 'x' + rest);
      var knick = s.nst.length && !(s.par && s.q === 0);    // x²: Nullstelle ohne Vorzeichenwechsel, kein Knick
      rolle(fig, 'formel').innerHTML = 'f(x) = ' + fT + ' (gestrichelt) &nbsp;·&nbsp; y = ' + sp('tx-blau', '|f(x)|')
        + ' &nbsp;·&nbsp; ' + (knick ? s.nst.length + (s.nst.length === 1 ? ' Knick' : ' Knicke')
          : s.par && s.q === 0 ? 'kein Knick — f berührt die x-Achse nur, wechselt das Vorzeichen nicht'
          : !s.par && s.m === 0 && s.q < 0 ? 'kein Knick — f liegt ganz unten und klappt als Ganzes hoch'
          : 'kein Knick — nichts umzuklappen');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(q\\). Welche Teile klappen um, welche nicht?', ok: function(s){ return s.bewegt.q; } },
      // Startzustand: Gerade f(x) = x + 1, Knick bei −1 — keine Aufgabe ist schon gelöst.
      { text: 'Gerade: Stell \\(f\\) so ein, dass \\(|f|\\) den Knick bei \\(x = -1.5\\) hat.', ok: function(s){ return !s.par && s.m !== 0 && Math.abs(-s.q / s.m + 1.5) < 1e-9; } },
      { text: 'Gerade: Stell \\(f\\) so ein, dass \\(|f|\\) gar keinen Knick hat.', ok: function(s){ return !s.par && s.m === 0; } },
      { text: 'Parabel: Schalte auf \\(f(x) = x^2 + q\\). Die Knicke sollen bei \\(-\\sqrt3\\) und \\(\\sqrt3\\) liegen.', ok: function(s){ return s.par && s.q === -3; } },
      { text: 'Parabel: Die Kurve soll die \\(x\\)-Achse nur berühren. Entsteht ein Knick?', ok: function(s){ return s.par && s.q === 0; } },
      { text: 'Parabel: Der umgeklappte Scheitel soll bei \\((0 \\mid 2.5)\\) liegen.', ok: function(s){ return s.par && s.q === -2.5; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: abschnittsweise schreiben — die Wanne ----------
     Unterschied zum «Wannen-Labor» der Themenseite: Hier steht die Wanne als dreiteilige
     abschnittsweise Funktion daneben, live mit den Termen der drei Abschnitte. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 300, x0: -5, x1: 6, y0: -1, y1: 10, sy: 1, xm: [-4, -2, 2, 4], ym: [2, 4, 6, 8] });
    var pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r), lo = Math.min(w.a, w.b), hi = Math.max(w.a, w.b);
      return { a: w.a, b: w.b, lo: lo, hi: hi, h: hi - lo, f: function(x){ return Math.abs(x - w.a) + Math.abs(x - w.b); }, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; } };
    function zeichnen(){
      var s = zust();
      K.leeren();
      K.kurve(function(x){ return Math.abs(x - s.a); }, 'normal');
      K.kurve(function(x){ return Math.abs(x - s.b); }, 'normal');
      K.kurve(s.f, 'kurve');
      K.punkt(s.lo, s.h, 'p-pkt', '(' + z(s.lo) + ' | ' + z(s.h) + ')', -8, -8, 'end');
      if (s.h > 0) K.punkt(s.hi, s.h, 'p-pkt', '(' + z(s.hi) + ' | ' + z(s.h) + ')', 8, -8);
      var term = function(m, q){ return m + (q === 0 ? '' : ' ' + vor(q)); }, nb = function(t){ return '<span class="nb">' + t + '</span>'; };
      rolle(fig, 'formel').innerHTML = 'y = ' + sp('tx-blau', betragT(s.a) + ' + ' + betragT(s.b))
        + '<br>' + nb(sp('tx-gruen', term('−2x', s.a + s.b)) + ' für x &lt; ' + z(s.lo))
        + (s.h > 0 ? ' &nbsp;·&nbsp; ' + nb(sp('tx-gruen', z(s.h)) + ' für ' + z(s.lo) + ' ≤ x ≤ ' + z(s.hi)) : '')
        + ' &nbsp;·&nbsp; ' + nb(sp('tx-gruen', term('2x', -(s.a + s.b))) + (s.h > 0 ? ' für x &gt; ' : ' für x ≥ ') + z(s.hi));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Verschiebe \\(a\\) und \\(b\\). Wie breit und wie hoch ist der Boden?', ok: function(s){ return s.bewegt.a || s.bewegt.b; } },
      // Startzustand a = −2, b = 2: Boden auf Höhe 4 — keine Aufgabe ist schon gelöst.
      { text: 'Der Boden soll auf der Höhe \\(3\\) liegen.', ok: function(s){ return s.h === 3; } },
      { text: 'Der Boden soll von \\(-1\\) bis \\(2\\) reichen.', ok: function(s){ return s.lo === -1 && s.hi === 2; } },
      { text: 'Mach aus der Wanne ein V ohne flachen Boden.', ok: function(s){ return s.h === 0; } },
      { text: 'Die Mitte des Bodens soll bei \\(x = 0.5\\) liegen, seine Höhe \\(5\\) sein.', ok: function(s){ return s.lo === -2 && s.hi === 3; } },
      { text: 'Boden auf Höhe \\(2\\), und bei \\(x = 4\\) soll \\(y = 6\\) sein.', ok: function(s){ return s.h === 2 && Math.abs(s.f(4) - 6) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Gleichungen und Ungleichungen ----------
     V-Kurve |x − u| oder W-Kurve |x² − 4| mit der Waagrechten y = c; die Schnittstellen stehen
     im Bild, mit dem Schalter «≤» auch das Lösungsintervall der Ungleichung. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 260, x0: -6, x1: 6, y0: -2, y1: 8, sy: 1, xm: XM, ym: [2, 4, 6] });
    var pruefen = function(){}, bewegt = {};
    var sch = fig.querySelectorAll('.sim-schalter input');
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    sch.forEach(function(i){ i.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), W = sch[0].checked, ug = sch[1].checked, c = w.c, L = [];
      if (W){ if (c > 4) L = [-Math.sqrt(4 + c), Math.sqrt(4 + c)]; else if (c === 4) L = [-Math.sqrt(8), 0, Math.sqrt(8)];
              else if (c > 0) L = [-Math.sqrt(4 + c), -Math.sqrt(4 - c), Math.sqrt(4 - c), Math.sqrt(4 + c)]; else if (c === 0) L = [-2, 2]; }
      else { if (c > 0) L = [w.u - c, w.u + c]; else if (c === 0) L = [w.u]; }
      r.u.disabled = W;
      return { W: W, ug: ug, u: w.u, c: c, l: L, n: L.length, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; } };
    function zeichnen(){
      var s = zust(), f = s.W ? function(x){ return Math.abs(x * x - 4); } : function(x){ return Math.abs(x - s.u); };
      K.leeren();
      if (s.ug && !s.W && s.c > 0) K.strecke(s.u - s.c, 0, s.u + s.c, 0, 'loesung');
      K.kurve(f, 'kurve');
      K.strecke(-6, s.c, 6, s.c, 'waagrechte');
      s.l.forEach(function(x, i){ K.punkt(x, s.c, 'p-lauf orange', zz(x), i < s.n / 2 ? -6 : 6, -8, i < s.n / 2 ? 'end' : 'start'); });
      var gl = (s.W ? '|x² − 4|' : betragT(s.u)) + (s.ug && !s.W ? ' ≤ ' : ' = ') + z(s.c);
      rolle(fig, 'formel').innerHTML = sp('tx-blau', gl) + ' &nbsp;·&nbsp; ' + (s.n === 0 ? '<b>keine Lösung</b>' : s.n + (s.n === 1 ? ' Schnittstelle' : ' Schnittstellen'))
        + (s.ug && !s.W ? (s.c > 0 ? ' &nbsp;·&nbsp; Lösung: ' + z(s.u - s.c) + ' ≤ x ≤ ' + z(s.u + s.c) : s.c === 0 ? ' &nbsp;·&nbsp; Lösung: x = ' + z(s.u) : '') : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh die Waagrechte \\(y = c\\) hoch und runter. Wie viele Schnittstellen gibt es?', ok: function(s){ return s.bewegt.c; } },
      // Startzustand: V |x|, c = 1.5 — zwei Lösungen ±1.5, keine Aufgabe ist schon gelöst (auch nicht mit dem Schalter W).
      { text: 'V: Stell \\(u\\) und \\(c\\) so ein, dass die Lösungen \\(-3\\) und \\(1\\) sind.', ok: function(s){ return !s.W && s.u === -1 && s.c === 2; } },
      { text: 'Stell \\(c\\) so ein, dass es <b>keine</b> Lösung gibt.', ok: function(s){ return s.n === 0; } },
      { text: 'Schalte auf das W. Genau <b>zwei</b> Lösungen, und eine davon ist \\(x = 3\\).', ok: function(s){ return s.W && s.c === 5; } },
      { text: 'W: Vier Lösungen, und eine davon ist \\(x = \\sqrt2 \\approx 1.41\\).', ok: function(s){ return s.W && s.c === 2; } },
      { text: 'V mit \\(u = 0\\): Schalte «≤» ein. Die Lösungsmenge von \\(|x| \\le c\\) soll von \\(-2.5\\) bis \\(2.5\\) reichen.', ok: function(s){ return !s.W && s.ug && s.u === 0 && s.c === 2.5; } }
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
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function betT(m){ return m === 0 ? '|x|' : '|x ' + (m > 0 ? '- ' + m : '+ ' + (-m)) + '|'; }
    function linT(m, q){ var s = m === 1 ? 'x' : m === -1 ? '-x' : tz(m) + 'x'; return q === 0 ? s : s + (q > 0 ? ' + ' + q : ' - ' + (-q)); }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15). Je Typ ein eigener
       Schlüssel (T.schl). Reihenfolge: Clips · Simulationen · Aufgaben der Kapitel · Vortest · Gesamttest. */
    var SPERRE = [
      // Clips
      'ks|1|-3|-2', 'ks|3|1|0', 'ks|-1|2|4', 'ks|-2|0|1', 'ks|2|1|-3',
      'ug|2|-6', 'ug|2|4', 'up|9', 'up|4', 'up|1',
      'ab|2|-6', 'ab|3|6', 'wa|-1|3', 'wa|0|4', 'wa|-2|1',
      'bg|1|1|3', 'bg|1|-2|5', 'bg|1|1|2', 'bu|1|1|3|le', 'bu|1|0|2|lt',
      // Simulationen
      'ks|1|-2|1', 'ks|1|1|-2', 'ks|1.5|-1.5|-2', 'up|2.25', 'wa|-2|3', 'wa|0|2', 'wa|-1|2', 'bg|1|-1|2', 'bu|1|0|2.5|le', 'fa|2|-1', 'fa|-2|2', 'fa|1|3.5',
      // Aufgaben der Kapitel
      'ks|-3|-1|2', 'ks|0.5|4|0', 'ks|2|-1|-4', 'ks|-0.5|-1|3', 'ks|3|2|-1', 'ks|-1|0|5',
      'ug|2|-6', 'up|1', 'ab|3|9', 'ab|-2|4', 'wa|-2|2', 'wa|-3|1', 'bg|1|4|6', 'bu|1|-1|4|le', 'bu|1|2|1|ge',
      // Gesamttest (downloads/leitprogramme/betragsfunktionen/gesamttest.tex)
      'ks|-2|-1|4', 'ks|0.5|-2|-1', 'wa|-1|4', 'up|1', 'bu|1|-1|2|ge'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    var TYPEN = {
      /* ── Kapitel 1: die Betragsfunktion ──────────────────────────── */
      'betrag-wert': { felder: ['y'], muster: 'Wert = {y}',
        schl: function(A){ return 'bw|' + A.a + '|' + A.b + '|' + A.x; },
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){
          // Meist ein negatives Argument — sonst wäre der Betrag nicht zu sehen; manchmal ein positives.
          var a = zufall([-3, -2, -1, 1, 2, 3]), x = zufallG(-4, 4), arg = zufall([-7, -6, -5, -4, -3, -2, -1, 2, 5]), b = arg - a * x;
          return { a: a, b: b, x: x, arg: arg, y: Math.abs(arg),
            text: 'Gegeben \\(f(x) = |' + linT(a, b) + '|\\). Berechne \\(f(' + tz(x) + ')\\).' }; },
        fehler: function(A){ return A.arg < 0 ? [[{ y: String(A.arg) }, 'Betrag']] : [[{ y: String(-A.arg) }, null]]; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          if (gl(e.y, A.arg)) return 'Das ist der Wert im Betrag, \\(' + tz(A.arg) + '\\). Der Betrag davon ist nie negativ.';
          return 'Zuerst einsetzen: \\(' + tz(A.a) + ' \\cdot ' + (A.x < 0 ? '(' + tz(A.x) + ')' : tz(A.x)) + (A.b === 0 ? '' : A.b < 0 ? ' - ' + (-A.b) : ' + ' + A.b) + '\\), dann den Betrag nehmen.'; },
        loesung: function(A){ return 'f(' + tz(A.x) + ') = |' + tz(A.arg) + '| = ' + A.y; } },

      'fall': { felder: ['t', 'y'], muster: 'Hier gilt |x − u| = {t:x − u|−(x − u)} = {y}',
        schl: function(A){ return 'fa|' + A.m + '|' + A.x; },
        eingabe: function(A){ return { t: A.rechts ? 'x − u' : '−(x − u)', y: String(Math.abs(A.x - A.m)) }; },
        neu: function(){
          var m = zufall([-4, -3, -2, -1, 1, 2, 3, 4]), x = zufallG(-6, 6);
          while (x === m) x = zufallG(-6, 6);
          return { m: m, x: x, rechts: x > m,
            text: 'Für \\(f(x) = ' + betT(m) + '\\) ist \\(u = ' + tz(m) + '\\). Welcher Term gilt bei \\(x = ' + tz(x) + '\\), und welchen Wert hat \\(f\\) dort?' }; },
        fehler: function(A){ var f = [[{ t: A.rechts ? '−(x − u)' : 'x − u', y: String(Math.abs(A.x - A.m)) }, 'Fall']];
          if (!A.rechts) f.push([{ t: '−(x − u)', y: String(A.x - A.m) }, 'Betrag']);
          return f; },
        pruefen: function(A, e){
          var r = [], soll = A.rechts ? 'x − u' : '−(x − u)';
          if (e.t === soll && gl(e.y, Math.abs(A.x - A.m))) return null;
          if (e.t !== soll) r.push('Fall: \\(x = ' + tz(A.x) + '\\) liegt ' + (A.rechts ? 'rechts' : 'links') + ' von \\(u = ' + tz(A.m) + '\\), also ist \\(x - u\\) ' + (A.rechts ? 'positiv' : 'negativ') + '.');
          if (!gl(e.y, Math.abs(A.x - A.m))) r.push(gl(e.y, A.x - A.m) ? 'Der Wert: Ein Betrag ist nie negativ.' : 'Der Wert: Abstand von \\(' + tz(A.x) + '\\) zu \\(' + tz(A.m) + '\\).');
          return r.join(' '); },
        loesung: function(A){ return '|' + tz(A.x) + (A.m < 0 ? ' + ' + (-A.m) : ' - ' + A.m) + '| = ' + Math.abs(A.x - A.m); } },

      /* ── Kapitel 2: das V verschieben und strecken ───────────────── */
      'knick-steigung': { felder: ['u', 'v', 's'], muster: 'Knick ({u} | {v}), Steigung des rechten Astes {s}',
        schl: function(A){ return 'ks|' + A.a + '|' + A.u + '|' + A.v; },
        eingabe: function(A){ return { u: String(A.u), v: String(A.v), s: String(A.a) }; },
        neu: function(){
          var a = zufall([-3, -2, -1, -0.5, 0.5, 2, 3]), u = zufall([-4, -3, -2, -1, 1, 2, 3, 4]), v = zufall([-3, -2, -1, 0, 1, 2, 4]);
          return { a: a, u: u, v: v,
            text: 'Gegeben \\(y = ' + (a === 1 ? '' : a === -1 ? '-' : tz(a)) + '\\,' + betT(u) + (v === 0 ? '' : (v > 0 ? ' + ' + v : ' - ' + (-v))) + '\\). Gib den Knickpunkt und die Steigung des rechten Astes an.' }; },
        fehler: function(A){ return [[{ u: String(-A.u), v: String(A.v), s: String(A.a) }, 'Vorzeichen'],
                                     [{ u: String(A.u), v: String(A.v), s: String(-A.a) }, 'linke Ast']]; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.u, A.u) && gl(e.v, A.v) && gl(e.s, A.a)) return null;
          if (!gl(e.u, A.u)) r.push(gl(e.u, -A.u) ? 'Vorzeichen: Der Knick liegt, wo \\(' + betT(A.u).slice(1, -1) + '\\) null wird.' : 'Knick: Wo wird das Argument im Betrag null?');
          if (!gl(e.v, A.v)) r.push('Die \\(y\\)-Koordinate des Knicks ist der Summand hinter dem Betrag.');
          if (!gl(e.s, A.a)) r.push(gl(e.s, -A.a) ? 'Das ist der linke Ast. Der rechte Ast hat die Steigung \\(a\\), den Faktor vor dem Betrag.' : 'Steigung: der Faktor vor dem Betrag.');
          return r.join(' '); },
        loesung: function(A){ return '(' + tz(A.u) + ' \\mid ' + tz(A.v) + '),\\ \\text{Steigung rechts } ' + tz(A.a); } },

      'v-aus-graph': { felder: ['a', 'u', 'v'], muster: 'y = {a} · |x − ({u})| + {v}',
        schl: function(A){ return 'ks|' + A.a + '|' + A.u + '|' + A.v; },
        eingabe: function(A){ return { a: String(A.a), u: String(A.u), v: String(A.v) }; },
        neu: function(){
          var a, u, v;
          do { a = zufall([-2, -1, -0.5, 0.5, 1, 2]); u = zufallG(-3, 3); v = zufallG(-3, 3); } while ((a === 1 && u === 0 && v === 0));
          return { a: a, u: u, v: v, text: 'Bestimme \\(a\\), \\(u\\) und \\(v\\) der abgebildeten Kurve \\(y = a\\,|x - u| + v\\).' }; },
        zeichne: function(svg, A){
          var K = Achsen(svg, { w: 170, h: 170, x0: -5, x1: 5, y0: -5, y1: 5, r: 3, pfeil: 6, xm: [-4, -3, -2, -1, 1, 2, 3, 4], ym: [-4, -3, -2, -1, 1, 2, 3, 4] });
          K.kurve(function(x){ return A.a * Math.abs(x - A.u) + A.v; }, 'kurve');
          K.punkt(A.u, A.v, 'p-pkt');
        },
        fehler: function(A){ return [[{ a: String(-A.a), u: String(A.u), v: String(A.v) }, 'Öffnung'], [{ a: String(A.a), u: String(-A.u || 1), v: String(A.v) }, null]]; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.a, A.a) && gl(e.u, A.u) && gl(e.v, A.v)) return null;
          if (!gl(e.a, A.a)) r.push(gl(e.a, -A.a) ? 'Öffnung: ' + (A.a > 0 ? 'Ein V (nach oben offen) hat \\(a \\gt 0\\).' : 'Ein Dach (nach unten offen) hat \\(a \\lt 0\\).') : 'Lies die Steigung des rechten Astes ab: zwei Einheiten nach rechts, wie viel hoch oder runter — und durch zwei teilen.');
          if (!gl(e.u, A.u) || !gl(e.v, A.v)) r.push('Der Knick liegt bei \\((u \\mid v)\\) — lies seine Koordinaten ab.');
          return r.join(' '); },
        loesung: function(A){ return 'a = ' + tz(A.a) + ',\\ u = ' + tz(A.u) + ',\\ v = ' + tz(A.v); } },

      /* ── Kapitel 3: das Umklapp-Prinzip ──────────────────────────── */
      'umklapp-gerade': { felder: ['x0', 'y0'], muster: 'Knick bei x = {x0}, Wert bei x = 0: {y0}',
        schl: function(A){ return 'ug|' + A.m + '|' + A.q; },
        eingabe: function(A){ return { x0: String(A.x0), y0: String(Math.abs(A.q)) }; },
        neu: function(){
          var m = zufall([-3, -2, -1, 1, 2, 3]), x0 = zufall([-3, -2, -1, 1, 2, 3, 4]), q = -m * x0;
          return { m: m, q: q, x0: x0, text: 'Gegeben \\(f(x) = ' + linT(m, q) + '\\). Wo hat \\(y = |f(x)|\\) ihren Knick, und welchen Wert hat sie bei \\(x = 0\\)?' }; },
        fehler: function(A){ var f = [[{ x0: String(-A.x0), y0: String(Math.abs(A.q)) }, 'Vorzeichen']]; if (A.q < 0) f.push([{ x0: String(A.x0), y0: String(A.q) }, 'Betrag']); return f; },
        pruefen: function(A, e){
          var r = [];
          if (gl(e.x0, A.x0) && gl(e.y0, Math.abs(A.q))) return null;
          if (!gl(e.x0, A.x0)) r.push(gl(e.x0, -A.x0) ? 'Vorzeichen: Der Knick liegt an der Nullstelle von \\(f\\) — löse \\(' + linT(A.m, A.q) + ' = 0\\).' : 'Der Knick liegt an der Nullstelle von \\(f\\).');
          if (!gl(e.y0, Math.abs(A.q))) r.push(gl(e.y0, A.q) ? 'Bei \\(x = 0\\): Der Betrag macht den Wert positiv.' : 'Bei \\(x = 0\\) ist \\(|f(0)| = |' + tz(A.q) + '|\\).');
          return r.join(' '); },
        loesung: function(A){ return 'x_0 = ' + tz(A.x0) + ',\\ |f(0)| = ' + Math.abs(A.q); } },

      'umklapp-parabel': { felder: ['x', 'h'], muster: 'Knicke bei x = ±{x}, Buckel (0 | {h})',
        schl: function(A){ return 'up|' + A.k; },
        eingabe: function(A){ return { x: String(A.w), h: String(A.k) }; },
        neu: function(){
          var w = zufall([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7]), k = w * w;
          return { w: w, k: k, text: 'Skizziere im Kopf \\(y = |x^2 - ' + k + '|\\). Wo liegen die Knicke, und wie hoch ist der Buckel in der Mitte?' }; },
        fehler: function(A){ var f = [[{ x: String(A.w), h: String(-A.k) }, 'Betrag']]; if (A.k !== A.w) f.push([{ x: String(A.k), h: String(A.k) }, 'Wurzel']); return f; },
        pruefen: function(A, e){
          var r = [];
          if (gl(Math.abs(e.x), A.w) && gl(e.h, A.k)) return null;
          if (!gl(Math.abs(e.x), A.w)) r.push(gl(e.x, A.k) ? 'Knicke an den Nullstellen: \\(x^2 = ' + A.k + '\\) — die Wurzel ziehen.' : 'Die Knicke liegen an den Nullstellen von \\(x^2 - ' + A.k + '\\).');
          if (!gl(e.h, A.k)) r.push(gl(e.h, -A.k) ? 'Der Scheitel \\((0 \\mid -' + A.k + ')\\) klappt hoch — der Betrag ist positiv.' : 'Der Buckel ist der umgeklappte Scheitel von \\(x^2 - ' + A.k + '\\).');
          return r.join(' '); },
        loesung: function(A){ return 'x = \\pm\\sqrt{' + A.k + '} = \\pm ' + A.w + ',\\ (0 \\mid ' + A.k + ')'; } },

      /* ── Kapitel 4: abschnittsweise schreiben ────────────────────── */
      'abschnittsweise': { felder: ['g', 'm', 'q'], muster: 'Grenze x = {g}; für x &lt; Grenze: y = {m}x + {q}',
        schl: function(A){ return 'ab|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { g: String(A.g), m: String(A.a > 0 ? -A.a : A.a), q: String(A.a > 0 ? -A.b : A.b) }; },
        neu: function(){
          var a = zufall([-3, -2, -1, 1, 2, 3, 4]), g = zufall([-3, -2, -1, 1, 2, 3]), b = -a * g;
          return { a: a, b: b, g: g, text: 'Schreib \\(y = |' + linT(a, b) + '|\\) abschnittsweise: Wo liegt die Grenze, und welcher Term gilt links davon?' }; },
        fehler: function(A){ return [[{ g: String(A.g), m: String(A.a > 0 ? A.a : -A.a), q: String(A.a > 0 ? A.b : -A.b) }, 'Links'],
                                     [{ g: String(A.g), m: String(A.a > 0 ? A.a : -A.a), q: String(A.a > 0 ? -A.b : A.b) }, 'ganzen'],
                                     [{ g: String(-A.g), m: String(A.a > 0 ? -A.a : A.a), q: String(A.a > 0 ? -A.b : A.b) }, 'Grenze']]; },
        pruefen: function(A, e){
          var m = A.a > 0 ? -A.a : A.a, q = A.a > 0 ? -A.b : A.b, r = [];
          if (gl(e.g, A.g) && gl(e.m, m) && gl(e.q, q)) return null;
          if (!gl(e.g, A.g)) r.push('Grenze: Setz das Argument \\(' + linT(A.a, A.b) + '\\) gleich null.');
          if ((gl(e.m, -m) && gl(e.q, q)) || (gl(e.m, m) && gl(e.q, -q))) r.push('Nur eine Zahl umgedreht: Das Vorzeichen des ganzen Terms wird gedreht, beide Teile.');
          else if (!gl(e.m, m) || !gl(e.q, q)) r.push(gl(e.m, -m) && gl(e.q, -q) ? 'Links der Grenze ist \\(' + linT(A.a, A.b) + '\\) ' + (A.a > 0 ? 'negativ — dort wird das Vorzeichen des ganzen Terms gedreht.' : 'positiv — dort bleibt der Term, wie er ist.')
                                                                     : 'Teste eine Stelle links der Grenze: Ist das Argument dort positiv oder negativ?');
          return r.join(' '); },
        loesung: function(A){ var m = A.a > 0 ? -A.a : A.a, q = A.a > 0 ? -A.b : A.b; return 'x = ' + tz(A.g) + ';\\ x \\lt ' + tz(A.g) + ':\\ y = ' + linT(m, q); } },

      'wanne': { felder: ['h', 'y'], muster: 'Bodenhöhe {h}, Wert an der Stelle: {y}',
        schl: function(A){ return 'wa|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { h: String(A.b - A.a), y: String(Math.abs(A.x - A.a) + Math.abs(A.x - A.b)) }; },
        neu: function(){
          var a = zufallG(-4, 1), b = zufallG(a + 1, 4), x = zufall([a - 2, a - 1, b + 1, b + 2]);
          return { a: a, b: b, x: x, text: 'Gegeben \\(y = ' + betT(a) + ' + ' + betT(b) + '\\). Wie hoch liegt der flache Boden, und welchen Wert hat \\(y\\) bei \\(x = ' + tz(x) + '\\)?' }; },
        fehler: function(A){ var f = [], y = Math.abs(A.x - A.a) + Math.abs(A.x - A.b);
          if (Math.abs(A.a + A.b) !== A.b - A.a) f.push([{ h: String(Math.abs(A.a + A.b)), y: String(y) }, 'Abstand']);
          return f; },
        pruefen: function(A, e){
          var r = [], y = Math.abs(A.x - A.a) + Math.abs(A.x - A.b);
          if (gl(e.h, A.b - A.a) && gl(e.y, y)) return null;
          if (!gl(e.h, A.b - A.a)) r.push('Boden: Zwischen \\(' + tz(A.a) + '\\) und \\(' + tz(A.b) + '\\) ist die Summe der Abstände gleich dem Abstand der beiden Stellen.');
          if (!gl(e.y, y)) r.push('Wert: Beide Beträge einzeln ausrechnen und addieren.');
          return r.join(' '); },
        loesung: function(A){ return 'h = ' + (A.b - A.a) + ',\\ y(' + tz(A.x) + ') = ' + (Math.abs(A.x - A.a) + Math.abs(A.x - A.b)); } },

      /* ── Kapitel 5: Gleichungen und Ungleichungen ────────────────── */
      'betrag-gleichung': { felder: ['x1', 'x2'], muster: 'x₁ = {x1} (kleinere), x₂ = {x2} (grössere)',
        schl: function(A){ return 'bg|' + A.k + '|' + A.u + '|' + A.c; },
        eingabe: function(A){ return { x1: String(A.x1), x2: String(A.x2) }; },
        neu: function(){
          var k = zufall([1, 1, 2]), u = zufallG(-4, 4), c = Math.random() < 0.15 ? 0 : zufallG(1, 6) * (k === 2 ? 2 : 1);
          if (u === 0) u = 1;     // sonst fielen die gespiegelten Lösungen mit den richtigen zusammen
          // |k x - k u| = c  ⇒  x = u ± c/k
          return { k: k, u: u, c: c, x1: u - c / k, x2: u + c / k,
            text: 'Löse \\(|' + linT(k, -k * u) + '| = ' + c + '\\). (Gibt es nur eine Lösung, trag sie in beide Felder ein.)' }; },
        fehler: function(A){ return A.c === 0 ? [[{ x1: String(-A.u), x2: String(-A.u) }, 'Vorzeichen'], [{ x1: String(A.u - 1), x2: String(A.u + 1) }, 'eine']]
                                              : [[{ x1: String(-A.u - A.c / A.k), x2: String(-A.u + A.c / A.k) }, 'Vorzeichen'], [{ x1: String(A.x2), x2: String(A.x2) }, 'zwei']]; },
        pruefen: function(A, e){
          if (gl(e.x1, A.x1) && gl(e.x2, A.x2)) return null;
          if (gl(e.x1, A.x2) && gl(e.x2, A.x1)) return 'Beide richtig — aber zuerst die kleinere Lösung.';
          if (A.c === 0) return gl(e.x1, -A.u) && gl(e.x2, -A.u) ? 'Vorzeichen: Das Argument wird null bei \\(x = ' + tz(A.u) + '\\).' : 'Betrag gleich null hat nur eine Lösung: Das Argument ist null. Trag sie in beide Felder ein.';
          if (gl(e.x1, e.x2)) return 'Es gibt zwei Fälle: Das Argument ist \\(' + A.c + '\\) oder \\(-' + A.c + '\\).';
          if (gl(e.x1, -A.u - A.c / A.k) && gl(e.x2, -A.u + A.c / A.k)) return 'Vorzeichen: Die Lösungen liegen symmetrisch um die Nullstelle des Arguments, \\(x = ' + tz(A.u) + '\\).';
          return 'Zwei Fälle: \\(' + linT(A.k, -A.k * A.u) + ' = ' + A.c + '\\) und \\(' + linT(A.k, -A.k * A.u) + ' = -' + A.c + '\\).'; },
        loesung: function(A){ return A.c === 0 ? 'L = \\{' + tz(A.u) + '\\}' : 'L = \\{' + tz(A.x1) + ';\\ ' + tz(A.x2) + '\\}'; } },

      'betrag-ungleichung': { felder: ['art', 'a', 'b'], muster: 'Lösung: {art:a ≤ x ≤ b|a < x < b|x ≤ a oder x ≥ b|x < a oder x > b} mit a = {a}, b = {b}',
        schl: function(A){ return 'bu|1|' + A.u + '|' + A.c + '|' + A.rel; },
        eingabe: function(A){ return { art: A.art, a: String(A.u - A.c), b: String(A.u + A.c) }; },
        neu: function(){
          var u = zufallG(-4, 4), c = zufallG(1, 5), rel = zufall(['le', 'lt', 'ge', 'gt']), innen = rel === 'le' || rel === 'lt', streng = rel === 'lt' || rel === 'gt';
          var art = innen ? (streng ? 'a < x < b' : 'a ≤ x ≤ b') : (streng ? 'x < a oder x > b' : 'x ≤ a oder x ≥ b');
          return { u: u, c: c, innen: innen, streng: streng, rel: rel, art: art,
            text: 'Löse \\(' + betT(u) + ' ' + { le: '\\le', lt: '\\lt', ge: '\\ge', gt: '\\gt' }[rel] + ' ' + c + '\\).' }; },
        fehler: function(A){ var gegen = A.innen ? (A.streng ? 'x < a oder x > b' : 'x ≤ a oder x ≥ b') : (A.streng ? 'a < x < b' : 'a ≤ x ≤ b');
          var rand = A.innen ? (A.streng ? 'a ≤ x ≤ b' : 'a < x < b') : (A.streng ? 'x ≤ a oder x ≥ b' : 'x < a oder x > b');
          return [[{ art: gegen, a: String(A.u - A.c), b: String(A.u + A.c) }, 'Waagrechte'], [{ art: rand, a: String(A.u - A.c), b: String(A.u + A.c) }, 'Grenzen']]; },
        pruefen: function(A, e){
          var r = [], innenE = e.art.indexOf('oder') < 0, strengE = e.art.indexOf('≤') < 0 && e.art.indexOf('≥') < 0;
          if (e.art === A.art && gl(e.a, A.u - A.c) && gl(e.b, A.u + A.c)) return null;
          if (innenE !== A.innen) r.push('Skizze: Wo liegt das V ' + (A.innen ? 'unter' : 'über') + ' der Waagrechten \\(y = ' + A.c + '\\) — zwischen oder ausserhalb der Schnittstellen?');
          else if (strengE !== A.streng) r.push('Grenzen: Bei ' + (A.streng ? '«&lt;» bzw. «&gt;» gehören die Schnittstellen nicht dazu.' : '«≤» bzw. «≥» gehören die Schnittstellen dazu.'));
          if (!gl(e.a, A.u - A.c) || !gl(e.b, A.u + A.c)) r.push('Die Grenzen sind die Lösungen von \\(' + betT(A.u) + ' = ' + A.c + '\\).');
          return r.join(' '); },
        loesung: function(A){ var k = A.streng ? '\\lt' : '\\le', g = A.streng ? '\\gt' : '\\ge';
          return A.innen ? tz(A.u - A.c) + ' ' + k + ' x ' + k + ' ' + tz(A.u + A.c) : 'x ' + k + ' ' + tz(A.u - A.c) + '\\ \\vee\\ x ' + g + ' ' + tz(A.u + A.c); } }
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

  /* ---------- Minigrafen: <svg class="mini" data-k="…;…"> mit Teilen, durch «;» getrennt:
       v,a,u,v  → a·|x − u| + v        G,m,q → |m x + q|        Q,a,b,c → |a x² + b x + c|
       w,a,b    → |x − a| + |x − b|    g,m,q → m x + q          q,a,b,c → a x² + b x + c
       Grossbuchstaben und v, w sind Betragskurven (blau), g und q die Funktion vor dem Betrag
       (Tinte, gestrichelt). Dazu data-fenster="x0,x1,y0,y1", data-punkte="x,y;…",
       data-waagrecht="c", data-xm/data-ym (beschriftete Stellen), data-titel. ---------- */
  document.querySelectorAll('svg.mini[data-k]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-5,5,-2,6').split(',').map(Number);
    svg.setAttribute('viewBox', '0 0 170 170'); svg.setAttribute('role', 'img');
    var liste = function(t, d){ return t ? t.split(',').map(Number) : d; };
    var K = Achsen(svg, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, sy: +svg.dataset.sy || 1, pfeil: 6,
      xm: liste(svg.dataset.xm, [-4, -2, 2, 4].filter(function(t){ return t > fe[0] && t < fe[1]; })),
      ym: liste(svg.dataset.ym, [2, 4].filter(function(t){ return t > fe[2] && t < fe[3]; })) });
    if (svg.dataset.waagrecht) K.strecke(fe[0], +svg.dataset.waagrecht, fe[1], +svg.dataset.waagrecht, 'waagrechte');
    svg.dataset.k.split(';').filter(Boolean).forEach(function(s){
      var p = s.split(','), art = p[0], q = p.slice(1).map(Number), f;
      if (art === 'v') f = function(x){ return q[0] * Math.abs(x - q[1]) + q[2]; };
      else if (art === 'w') f = function(x){ return Math.abs(x - q[0]) + Math.abs(x - q[1]); };
      else if (art === 'G' || art === 'g') f = function(x){ var y = q[0] * x + q[1]; return art === 'G' ? Math.abs(y) : y; };
      else f = function(x){ var y = q[0] * x * x + q[1] * x + q[2]; return art === 'Q' ? Math.abs(y) : y; };
      K.kurve(f, (art === 'g' || art === 'q') ? 'kurve g2' : 'kurve');
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
