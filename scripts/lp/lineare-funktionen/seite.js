<script>
/* Leitprogramm Lineare Funktionen — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Notation wie auf Themenseite 3.2: f(x) = m·x + b, Steigung m,
   y-Achsenabschnitt b, Nullstelle x₀ = −b/m. Achsen, Farben und Startwerte wie dort bzw.
   wie im Clip davor.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15): blau = m und die Gerade,
   orange = b und der Punkt (0 | b), grün = Nullstelle und Zielgerade, rot = Gegenbeispiel.
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
      kurve: function(f, cls, a, b){
        var d = '', A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 240; k++){ var x = A + (B - A) * k / 240, y = Math.max(y0 - 3 * (y1 - y0), Math.min(y1 + 3 * (y1 - y0), f(x)));
          d += (d ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); }
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
  var FENSTER = { w: 300, h: 300, x0: -7.5, x1: 7.5, y0: -7.5, y1: 7.5, xm: [-5, 5], ym: [-5, 5] };

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  function werte(r){ var w = {}; for (var k in r){ w[k] = +r[k].value; r[k].parentNode.querySelector('.sl-val').textContent = z(w[k]); } return w; }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }

  /* Term m·x + b als HTML, mit den Farben des Leitprogramms. */
  function linText(m, b){
    var s;
    if (m === 0) s = sp('tx-orange', z(b));
    else {
      s = (Math.abs(m) === 1 ? (m < 0 ? '−' : '') : sp('tx-blau', z(m)) + '·') + 'x';
      if (Math.abs(m) === 1) s = sp('tx-blau', (m < 0 ? '−' : '')) + 'x';
      if (b !== 0) s += (b > 0 ? ' + ' : ' − ') + sp('tx-orange', z(Math.abs(b)));
    }
    return 'f(x) = ' + s;
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

  /* ---------- Kapitel 1: m kippt, b schiebt ----------
     Unterschied zur Animation «Drei Darstellungen» auf Themenseite 3.2: dort stehen
     Gleichung, Wertetabelle und Graph nebeneinander und ein dritter Regler wählt x.
     Hier bleibt nur der Graph, dafür liegt die Ursprungsgerade y = m·x gestrichelt
     darunter — so sieht man, dass b nur senkrecht schiebt. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), ziel = null, pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r); return { m: w.m, b: w.b, bewegt: bewegt }; },
                zeichnen: zeichnen, aufraeumen: function(){ ziel = null; bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), m = w.m, b = w.b;
      K.leeren();
      K.kurve(function(x){ return m * x; }, 'normal hilfslinie');
      if (ziel) K.kurve(function(x){ return ziel[0] * x + ziel[1]; }, 'zielkurve');
      K.kurve(function(x){ return m * x + b; }, 'kurve');
      // Die Beschriftung kommt auf die Seite, auf der die Gerade unter ihr durchlaeuft:
      // bei m > 0 links davon, bei m < 0 rechts davon.
      K.punkt(0, b, 'p-b', '(0 | ' + z(b) + ')', m > 0 ? -9 : 9, -7, m > 0 ? 'end' : 'start');
      if (m !== 0) K.punkt(-b / m, 0, 'p-null');
      rolle(fig, 'formel').innerHTML = linText(m, b);
      pruefen();
    }
    function bau(m, b, tex){ return { text: 'Bau nach: \\(' + tex + '\\)', ok: function(s){ return s.m === m && s.b === b; } }; }
    function zielAufgabe(t){ return { text: 'Triff die grüne Gerade.', setup: function(){ ziel = t; }, ok: function(s){ return s.m === t[0] && s.b === t[1]; } }; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an beiden Reglern und beobachte, was sich ändert.', ok: function(s){ return s.bewegt.m && s.bewegt.b; } },
      bau(3, -2, 'f(x) = 3x - 2'), bau(-1.5, 4, 'f(x) = -1.5x + 4'), bau(-2, -3, 'f(x) = -2x - 3'),
      { text: 'Stell eine Gerade durch den Ursprung ein.', ok: function(s){ return s.b === 0 && s.m !== 0; } },
      { text: 'Stell eine waagrechte Gerade ein.', ok: function(s){ return s.m === 0; } },
      zielAufgabe([1.5, -3]), zielAufgabe([-2.5, 2])
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Steigungsdreieck ----------
     Unterschied zur Animation «Steigungsdreieck zum Ziehen» auf Themenseite 3.2: dort
     zieht man beide Punkte frei (am Handy fummelig) und sieht nur m. Hier liegt der linke
     Punkt fest, ein Regler ändert nur die Breite des Dreiecks — und der Bruch Δy/Δx steht
     mit beiden Zahlen da, damit sichtbar wird, dass er sich nicht ändert. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), pruefen = function(){}, bewegt = {};
    var X1 = -3;                                   // linker Punkt des Dreiecks, fest
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r); return { m: w.m, b: w.b, dx: w.dx, bewegt: bewegt,
                  x0: w.m === 0 ? null : -w.b / w.m }; },
                zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), m = w.m, b = w.b, dx = w.dx;
      var ya = m * X1 + b, yb = m * (X1 + dx) + b, dy = yb - ya;
      K.leeren();
      K.kurve(function(x){ return m * x + b; }, 'kurve');
      K.strecke(X1, ya, X1 + dx, ya, 'dreieck hilfslinie');
      K.strecke(X1 + dx, ya, X1 + dx, yb, 'dreieck hilfslinie');
      K.text(X1 + dx / 2, ya - 0.75, 'Δx = ' + z(dx), 'p-m hilfslinie');
      K.text(X1 + dx + 0.3, (ya + yb) / 2, 'Δy = ' + z(dy), 'p-m hilfslinie', 'start');
      K.punkt(X1, ya, 'p-pkt'); K.punkt(X1 + dx, yb, 'p-pkt');
      K.punkt(0, b, 'p-b');
      if (m !== 0){
        var x0 = -b / m, rund = Math.abs(x0 * 100 - Math.round(x0 * 100)) > 1e-9;   // gerundet: nur mit «≈»
        K.punkt(x0, 0, 'p-null', 'x\u2080 ' + (rund ? '≈ ' : '= ') + z(x0), m > 0 ? -9 : 9, -8, m > 0 ? 'end' : 'start');
      }
      rolle(fig, 'formel').innerHTML = 'm = ' + sp('tx-blau', z(dy)) + ' : ' + sp('tx-blau', z(dx))
        + ' = <b>' + sp('tx-blau', z(m)) + '</b> &nbsp;·&nbsp; ' + linText(m, b);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh nur an \\(\\Delta x\\). Was passiert mit \\(\\Delta y\\), was mit \\(m\\)?', ok: function(s){ return s.bewegt.dx; } },
      { text: 'Stell \\(m = 1.5\\) ein und lies \\(\\Delta y\\) bei \\(\\Delta x = 2\\) ab.', ok: function(s){ return s.m === 1.5 && s.dx === 2; } },
      { text: 'Stell eine fallende Gerade ein.', ok: function(s){ return s.m < 0; } },
      { text: 'Stell \\(m = 0\\) ein. Wie gross ist \\(\\Delta y\\) jetzt?', ok: function(s){ return s.m === 0; } },
      { text: 'Stell eine Gerade mit der Nullstelle \\(3\\) ein.', ok: function(s){ return s.x0 === 3; } },
      { text: 'Stell \\(f(x) = -2.5x + 5\\) ein. Wo liegt ihre Nullstelle?', ok: function(s){ return s.m === -2.5 && s.b === 5; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: zwei Geraden ----------
     Unterschied zur Animation «Typen linearer Funktionen» auf Themenseite 3.2: dort zeigt
     ein Knopf je einen fertigen Fall. Hier stellt man die zweite Gerade selbst ein, und
     die Simulation sagt laufend, wie die beiden zueinander liegen — samit dem Produkt
     \(m_1 \cdot m_2\), an dem die Bedingung für «senkrecht» hängt. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), pruefen = function(){}, bewegt = {};
    var M1 = -2, B1 = 3;                           // g: y = −2x + 3, fest (kein Clip-Beispiel)
    var r = regler(fig, zeichnen);
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r); return { m: w.m2, b: w.b2, bewegt: bewegt }; },
                zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), m = w.m2, b = w.b2;
      K.leeren();
      K.kurve(function(x){ return M1 * x + B1; }, 'kurve g2');
      K.kurve(function(x){ return m * x + b; }, 'kurve');
      K.punkt(0, B1, 'p-b'); K.punkt(0, b, 'p-b');
      K.text(-5.4, 6.6, 'g fest', 'p-m', 'start');
      var lage = m === M1 && b === B1 ? 'dieselbe Gerade'
        : m === M1 ? 'parallel'
        : Math.abs(m * M1 + 1) < 1e-9 ? 'senkrecht'
        : 'schneidend';
      rolle(fig, 'formel').innerHTML = 'g: y = ' + sp('tx-blau', '−2') + '·x + ' + sp('tx-orange', '3')
        + ' &nbsp;·&nbsp; h: y = ' + linText(m, b).replace('f(x) = ', '')
        + '<br>m<sub>1</sub>·m<sub>2</sub> = ' + z(M1 * m) + ' — <b>' + lage + '</b>';
      fig.classList.toggle('treffer', lage === 'parallel' || lage === 'senkrecht');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an beiden Reglern und lies mit, wie die Simulation die Lage nennt.', ok: function(s){ return s.bewegt.m2 && s.bewegt.b2; } },
      { text: 'Mach \\(h\\) parallel zu \\(g\\).', ok: function(s){ return s.m === M1 && s.b !== B1; } },
      { text: 'Mach \\(h\\) senkrecht zu \\(g\\).', ok: function(s){ return Math.abs(s.m * M1 + 1) < 1e-9; } },
      { text: 'Mach \\(h\\) zur selben Geraden wie \\(g\\).', ok: function(s){ return s.m === M1 && s.b === B1; } },
      { text: 'Stell für \\(h\\) eine konstante Funktion ein.', ok: function(s){ return s.m === 0; } },
      { text: 'Stell für \\(h\\) eine proportionale Funktion ein, die nicht konstant ist.', ok: function(s){ return s.b === 0 && s.m !== 0; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: die Gleichung finden ----------
     Unterschied zur Aufgabe A2 auf Themenseite 3.2: dort zieht man zwei Punkte mit der
     Maus auf eine vorgegebene Gerade. Hier ist umgekehrt die Vorgabe gegeben (Steigung
     und Punkt, zwei Punkte, eine Lagebeziehung), und die Regler stellen m und b ein —
     dieselben zwei Zahlen, die man beim Rechnen bestimmt. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), FENSTER), pruefen = function(){}, fall = 'A';
    var r = regler(fig, zeichnen);
    var FAELLE = {
      A: { m: [3, 3, 1, 3], b: [-5, 5, 0.5, 0], punkte: [[-1, 2, 'P']] },
      B: { m: [-3, 3, 0.25, 1], b: [-5, 5, 0.5, 0], punkte: [[-2, 4, 'A'], [2, -1, 'B']] },
      C: { m: [-3, 3, 0.25, 1], b: [-5, 5, 0.5, 0], punkte: [[-2, 1, 'P']], hilfs: [1.5, -2] },
      D: { m: [-3, 3, 0.25, 1], b: [-5, 5, 0.5, 0], punkte: [[1, -1, 'P']], hilfs: [0.5, -1] }
    };
    function aufbauen(f){
      fall = f; var F = FAELLE[f];
      ['m', 'b'].forEach(function(p){
        r[p].min = F[p][0]; r[p].max = F[p][1]; r[p].step = F[p][2]; r[p].value = F[p][3];
        r[p].disabled = F[p][0] === F[p][1];
      });
      zeichnen();
    }
    var bewegt = {};
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
    var sim = { zustand: function(){ var w = werte(r); return { fall: fall, m: w.m, b: w.b, bewegt: bewegt }; },
                zeichnen: zeichnen, aufraeumen: function(){ bewegt = {}; } };
    function zeichnen(){
      var w = werte(r), m = w.m, b = w.b, F = FAELLE[fall];
      var treffer = F.punkte.every(function(p){ return Math.abs(m * p[0] + b - p[1]) < 1e-9; });
      K.leeren();
      if (F.hilfs) K.kurve(function(x){ return F.hilfs[0] * x + F.hilfs[1]; }, 'normal');
      K.kurve(function(x){ return m * x + b; }, 'kurve');
      F.punkte.forEach(function(p){ K.punkt(p[0], p[1], treffer ? 'p-null' : 'p-pkt', p[2] + '(' + z(p[0]) + ' | ' + z(p[1]) + ')', 8, -8); });
      K.punkt(0, b, 'p-b');
      rolle(fig, 'formel').innerHTML = linText(m, b) + (treffer ? ' &nbsp;✓' : '');
      fig.classList.toggle('treffer', treffer);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: \\(m = 3\\) ist fest. Zieh an \\(b\\) und beobachte, wann die Gerade \\(P\\) trifft.',
        setup: function(){ aufbauen('A'); }, ok: function(s){ return s.fall === 'A' && s.bewegt.b; } },
      { text: '\\(m = 3\\) ist fest. Stell \\(b\\) so ein, dass die Gerade durch \\(P(-1 \\mid 2)\\) geht.',
        setup: function(){ aufbauen('A'); }, ok: function(s){ return s.fall === 'A' && s.b === 5; } },
      { text: 'Jetzt zwei Punkte: Stell die Gerade durch \\(A(-2 \\mid 4)\\) und \\(B(2 \\mid -1)\\) ein.',
        setup: function(){ aufbauen('B'); }, ok: function(s){ return s.fall === 'B' && s.m === -1.25 && s.b === 1.5; } },
      { text: 'Stell die Gerade parallel zur gestrichelten ein, die durch \\(P(-2 \\mid 1)\\) geht.',
        setup: function(){ aufbauen('C'); }, ok: function(s){ return s.fall === 'C' && s.m === 1.5 && s.b === 4; } },
      { text: 'Stell die Gerade <b>senkrecht</b> zur gestrichelten ein, die durch \\(P(1 \\mid -1)\\) geht.',
        setup: function(){ aufbauen('D'); }, ok: function(s){ return s.fall === 'D' && s.m === -2 && s.b === 1; } }
    ], sim);
    aufbauen('A');
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
    var STEIG = [-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3];      // nie 0: diese Typen brauchen eine echte Steigung
    /* Geraden, nach denen das Leitprogramm an fester Stelle fragt — eine Zufallsübung
       darf keine davon treffen, sonst steht ihre Lösung schon irgendwo (HOWTO §15).
       Reihenfolge: Aufgaben der Kapitel · Vortest · Gesamttest · Clipfragen. */
    var FEST = [
      [2, -3], [-1, 2], [0.5, 0], [-2, -1], [1.5, -1], [1.5, -2], [-1, -1],
      [-0.5, 3], [2, -2], [0, 5], [4, -6], [-2, 8], [0.5, 3], [-1.5, 3],
      [-0.5, 0], [0, 4], [1, 0], [3, 1], [-1 / 3, 2], [3, -4], [1 / 3, 0],
      [-1.5, -2], [1, -2], [-1, 3], [-3, 7], [2, 2], [-2, 3], [-2, 10],
      [3, -1], [3, 4], [2, 1], [-0.5, 5], [0.05, 12], [0.5, 2], [2, -1],
      [0.5, -2], [2 / 3, -2], [-3, 6], [-4, 1], [-4, 5], [0.25, 2], [0, -2],
      [-2, 0], [-0.5, 4], [-1.5, 18],
      [3, -4], [-2, 5], [0.8, 1], [2, -6], [-1.5, 2.5], [1.5, -6], [-0.5, 2],
      [2, 1], [2, 3], [0.5, 1], [-1.5, 1], [1.5, 0], [0, 3], [4, -1],
      [-0.25, 1], [3, 2], [3, -3], [3, -5], [-2, 4], [-1, 5], [4, 80], [-0.5, 1.5]
    ];
    function fest(m, b){
      return FEST.some(function(p){ return gl(p[0], m) && gl(p[1], b); });
    }

    var TYPEN = {
      /* ── Kapitel 1 ───────────────────────────────────────────── */
      'mb-lesen': { felder: ['m', 'b'], muster: 'm = {m}   b = {b}',
        neu: function(){ var m, b;
          do { m = zufall(STEIG); b = zufall(bereich(-6, 6, [0])); } while (Math.abs(m) === Math.abs(b));
          return { m: m, b: b, text: 'Steigung und \\(y\\)-Achsenabschnitt von \\(f(x) = ' + lin(m, b) + '\\)?' }; },
        fehler: function(A){ return [[{ m: String(A.b), b: String(A.m) }, 'Vertauscht'],
                                     [{ m: String(-A.m), b: String(A.b) }, 'Vorzeichen'],
                                     [{ m: String(A.m), b: String(-A.b) }, 'Vorzeichen']]; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.b, A.b)) return null;
          if (gl(e.m, A.b) && gl(e.b, A.m)) return 'Vertauscht: \\(m\\) steht <em>vor</em> dem \\(x\\), \\(b\\) allein dahinter.';
          if (gl(e.m, -A.m) && gl(e.b, A.b)) return 'Vorzeichen von \\(m\\): Vor dem \\(x\\) steht \\(' + tz(A.m) + '\\).';
          if (gl(e.m, A.m) && gl(e.b, -A.b)) return 'Vorzeichen von \\(b\\): Hinten steht \\(' + tz(A.b) + '\\).';
          if (!gl(e.m, A.m)) return '\\(m\\) ist der Faktor vor \\(x\\) — mit Vorzeichen.';
          return '\\(b = f(0)\\): die Zahl ohne \\(x\\), mit Vorzeichen.'; },
        loesung: function(A){ return 'm = ' + tz(A.m) + ',\\quad b = ' + tz(A.b); } },

      'beschreibung-g': { felder: ['m', 'b'], muster: 'f(x) = {m} · x + {b}',
        neu: function(){ var m = zufall(STEIG), b = zufall(bereich(-6, 6));
          return { m: m, b: b, text: 'Eine Gerade ' + (m > 0 ? 'steigt' : 'fällt') + ' pro Schritt nach rechts um \\('
            + Math.abs(m) + '\\) und schneidet die \\(y\\)-Achse bei \\(' + tz(b) + '\\). Wie lautet \\(f(x)\\)?' }; },
        fehler: function(A){ var f = [[{ m: String(-A.m), b: String(A.b) }, 'Vorzeichen']];
          if (A.b !== 0) f.push([{ m: String(A.m), b: String(-A.b) }, 'Vorzeichen']);
          if (A.m !== A.b) f.push([{ m: String(A.b), b: String(A.m) }, 'Vertauscht']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.b, A.b)) return null;
          if (gl(e.m, A.b) && gl(e.b, A.m)) return 'Vertauscht: Der Zuwachs pro Schritt ist \\(m\\), die Höhe auf der \\(y\\)-Achse ist \\(b\\).';
          if (gl(e.m, -A.m)) return 'Vorzeichen von \\(m\\): «' + (A.m > 0 ? 'steigt' : 'fällt') + '» heisst \\(m ' + (A.m > 0 ? '\\gt' : '\\lt') + ' 0\\).';
          if (A.b !== 0 && gl(e.b, -A.b)) return 'Vorzeichen von \\(b\\): Die Gerade schneidet die \\(y\\)-Achse bei \\(' + tz(A.b) + '\\).';
          if (!gl(e.m, A.m)) return 'Der Zuwachs pro Schritt nach rechts ist \\(m\\).';
          return '\\(b\\) ist die Höhe, in der die Gerade die \\(y\\)-Achse schneidet.'; },
        loesung: function(A){ return 'f(x) = ' + lin(A.m, A.b); } },

      'graf-mb': { felder: ['m', 'b'], muster: 'f(x) = {m} · x + {b}', graf: true,
        neu: function(){ var m = zufall([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 1 / 3, -1 / 3, 2 / 3, -2 / 3]),
            b = zufall(bereich(-3, 3)), n3 = Math.abs(Math.round(m * 3) - m * 3) < 1e-9 && !Number.isInteger(m * 2);
          return { m: m, b: b, s: n3 ? 3 : (Math.abs(m) === 0.5 || Math.abs(m) === 1.5 ? 2 : 1),
            text: 'Gleichung der Geraden? (Die Punkte liegen auf Gitterpunkten.)' }; },
        fehler: function(A){ var f = [[{ m: String(-A.m), b: String(A.b) }, 'Steigt']];
          if (A.b !== 0) f.push([{ m: String(A.m), b: String(-A.b) }, 'Dort schneidet']);
          if (!gl(1 / A.m, A.m) && !gl(1 / A.m, -A.m)) f.push([{ m: String(1 / A.m), b: String(A.b) }, 'Bruch ist verkehrt']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.b, A.b)) return null;
          var r = [];
          if (gl(e.m, -A.m)) r.push('Steigt die Gerade oder fällt sie? Hier ist \\(m ' + (A.m > 0 ? '\\gt' : '\\lt') + ' 0\\).');
          else if (gl(e.m, 1 / A.m)) r.push('Der Bruch ist verkehrt: hinauf geteilt durch nach rechts, also \\(\\dfrac{\\Delta y}{\\Delta x}\\).');
          else if (!gl(e.m, A.m)) r.push('\\(m\\): ' + A.s + ' nach rechts — wie weit hinauf oder hinunter?');
          if (!gl(e.b, A.b)) r.push('\\(b\\): Dort schneidet die Gerade die \\(y\\)-Achse.');
          return r.join(' '); },
        loesung: function(A){ return 'f(x) = ' + lin(A.m, A.b); } },

      /* ── Kapitel 2 ───────────────────────────────────────────── */
      'steigung-punkte': { felder: ['m'], muster: 'm = {m}',
        neu: function(){ var m = zufall(STEIG), x1 = zufall(bereich(-5, 3)), d = zufall([2, 2, 4, 4, 6]), y1 = zufall(bereich(-5, 5));
          return { m: m, b: y1 - m * x1, x1: x1, y1: y1, x2: x1 + d, y2: y1 + m * d, dx: d, dy: m * d,
            text: 'Steigung der Geraden durch \\(A' + pkt(x1, y1) + '\\) und \\(B' + pkt(x1 + d, y1 + m * d) + '\\)?' }; },
        fehler: function(A){ var f = [[{ m: String(-A.m) }, 'geht es hin']];
          if (!gl(A.dy, A.m) && !gl(A.dy, -A.m)) f.push([{ m: String(A.dy) }, 'Teile noch durch']);
          if (!gl(1 / A.m, A.m) && !gl(1 / A.m, -A.m) && !gl(1 / A.m, A.dy)) f.push([{ m: String(1 / A.m) }, 'Bruch ist verkehrt']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m)) return null;
          if (gl(e.m, -A.m)) return 'Von \\(A\\) nach \\(B\\) geht es ' + (A.m > 0 ? 'hinauf' : 'hinunter') + ': \\(\\Delta y = ' + tz(A.dy) + '\\).';
          if (gl(e.m, A.dy)) return 'Das ist \\(\\Delta y\\). Teile noch durch \\(\\Delta x = ' + A.dx + '\\).';
          if (gl(e.m, 1 / A.m)) return 'Der Bruch ist verkehrt: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\), nicht umgekehrt.';
          return '\\(m = \\dfrac{y_2 - y_1}{x_2 - x_1} = \\dfrac{' + tz(A.dy) + '}{' + A.dx + '}\\).'; },
        loesung: function(A){ return 'm = \\dfrac{' + tz(A.dy) + '}{' + A.dx + '} = ' + tz(A.m); } },

      'nullstelle': { felder: ['x_0'], muster: 'x₀ = {x_0}',
        eingabe: function(A){ return { x_0: String(A.x0) }; },
        neu: function(){ var m = zufall([-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3]),
            x0 = zufall(Number.isInteger(m) ? bereich(-5, 5, [0]) : [-4, -2, 2, 4, 6]), b = -m * x0;   // halbe Steigung nur auf geraden Stellen: b bleibt ganzzahlig
          return { m: m, b: b, x0: x0, text: 'Nullstelle von \\(f(x) = ' + lin(m, b) + '\\)?' }; },
        fehler: function(A){ var f = [[{ x_0: String(-A.x0) }, 'Vorzeichen']];
          if (!gl(A.b, A.x0) && !gl(A.b, -A.x0)) f.push([{ x_0: String(A.b) }, 'Schnitt mit der']);
          if (!gl(A.m, A.x0) && !gl(A.m, -A.x0) && !gl(A.m, A.b)) f.push([{ x_0: String(A.m) }, 'Das ist \\(m\\)']);
          return f.filter(function(p){ return !gl(+p[0].x_0, A.x0); }); },
        pruefen: function(A, e){
          if (gl(e.x_0, A.x0)) return null;
          if (gl(e.x_0, -A.x0)) return 'Vorzeichen: \\(x_0 = -\\dfrac{b}{m} = -\\dfrac{' + tz(A.b) + '}{' + tz(A.m) + '} = ' + tz(A.x0) + '\\).';
          if (gl(e.x_0, A.b)) return '\\(' + tz(A.b) + '\\) ist \\(b\\), der Schnitt mit der \\(y\\)-Achse. Gesucht ist die Stelle mit \\(f(x) = 0\\).';
          if (gl(e.x_0, A.m)) return 'Das ist \\(m\\). Setz \\(f(x) = 0\\) und löse nach \\(x\\) auf.';
          return 'Setz \\(0 = ' + lin(A.m, A.b) + '\\) und löse nach \\(x\\) auf.'; },
        loesung: function(A){ return 'x_0 = -\\dfrac{' + tz(A.b) + '}{' + tz(A.m) + '} = ' + tz(A.x0); } },

      'punkt-pruefen': { felder: ['y', 'lage'], muster: 'Ergebnis {y}   →   P liegt {lage:auf g|nicht auf g}',
        eingabe: function(A){ return { y: String(A.y), lage: A.drauf ? 'auf g' : 'nicht auf g' }; },
        neu: function(){ var m = zufall(STEIG), b = zufall(bereich(-5, 5)), xp = zufall([-4, -2, 2, 4, 6]),
            y = m * xp + b, drauf = Math.random() < 0.5, yp = drauf ? y : y + zufall([-3, -2, -1, 1, 2, 3]);
          return { m: m, b: b, xp: xp, yp: yp, y: y, drauf: drauf,
            text: 'Liegt \\(P' + pkt(xp, yp) + '\\) auf \\(g: f(x) = ' + lin(m, b) + '\\)? Rechne \\(f(' + tz(xp) + ')\\) aus.' }; },
        fehler: function(A){ return [[{ y: String(A.y), lage: A.drauf ? 'nicht auf g' : 'auf g' }, 'Vergleich'],
                                     [{ y: String(A.y + 1), lage: A.drauf ? 'auf g' : 'nicht auf g' }, A.drauf ? 'Nicht ganz' : null]]; },
        pruefen: function(A, e){
          var richtigLage = A.drauf ? 'auf g' : 'nicht auf g';
          if (gl(e.y, A.y) && e.lage === richtigLage) return null;
          if (!gl(e.y, A.y)){
            if (gl(e.y, A.m * A.xp - A.b)) return 'Vorzeichen von \\(b\\): \\(f(' + tz(A.xp) + ') = ' + tz(A.m) + ' \\cdot ' + tz(A.xp) + plus(A.b) + '\\).';
            if (gl(e.y, A.yp)) return 'Nicht ganz: Gefragt ist \\(f(' + tz(A.xp) + ')\\), nicht die \\(y\\)-Koordinate von \\(P\\).';
            return 'Nicht ganz: \\(f(' + tz(A.xp) + ') = ' + tz(A.m) + ' \\cdot ' + tz(A.xp) + plus(A.b) + '\\) — Klammer um die negative Zahl nicht vergessen.';
          }
          return 'Der Wert stimmt. Jetzt der Vergleich: \\(f(' + tz(A.xp) + ') = ' + tz(A.y) + '\\), und \\(P\\) hat die Höhe \\(' + tz(A.yp) + '\\).'; },
        loesung: function(A){ return 'f(' + tz(A.xp) + ') = ' + tz(A.y) + ' \\Rightarrow P \\text{ liegt ' + (A.drauf ? '' : 'nicht ') + 'auf } g'; } },

      /* ── Kapitel 3 ───────────────────────────────────────────── */
      // «am genauesten», weil die Typen ineinander liegen: die Identität ist auch
      // proportional, eine proportionale Funktion mit m ≠ 0 auch eine lineare.
      'typ-erkennen': { felder: ['typ'], muster: '{typ:allgemeine lineare Funktion|proportionale Funktion|konstante Funktion|Identität|senkrechte Gerade (keine Funktion)}',
        eingabe: function(A){ return { typ: A.typ }; },
        neu: function(){
          var art = zufall(['allg', 'prop', 'konst', 'id', 'keine']), m, b, text, typ;
          if (art === 'prop'){ m = zufall([-3, -2, -0.5, 0.5, 2, 3]); text = 'f(x) = ' + kx(m); typ = 'proportionale Funktion'; }
          else if (art === 'konst'){ b = zufall(bereich(-5, 5, [0])); text = 'f(x) = ' + tz(b); typ = 'konstante Funktion'; }
          else if (art === 'id'){ text = 'f(x) = x'; typ = 'Identität'; }
          else if (art === 'keine'){ b = zufall(bereich(-5, 5, [0])); text = 'x = ' + tz(b); typ = 'senkrechte Gerade (keine Funktion)'; }
          else { m = zufall([-3, -2, -1.5, 1.5, 2, 3]); b = zufall(bereich(-5, 5, [0])); text = 'f(x) = ' + lin(m, b); typ = 'allgemeine lineare Funktion'; }
          return { art: art, typ: typ, gl: text, text: 'Welcher Typ passt am genauesten zu \\(' + text + '\\)?' }; },
        fehler: function(A){
          var andere = ['allgemeine lineare Funktion', 'proportionale Funktion', 'konstante Funktion', 'Identität', 'senkrechte Gerade (keine Funktion)']
            .filter(function(t){ return t !== A.typ; });
          return andere.slice(0, 2).map(function(t){ return [{ typ: t }, null]; }); },
        pruefen: function(A, e){
          if (e.typ === A.typ) return null;
          if (A.art === 'id') return 'Schau genau: \\(m = 1\\) und \\(b = 0\\) — jedes \\(x\\) wird auf sich selbst abgebildet.';
          if (A.art === 'prop') return 'Hier ist \\(b = 0\\): Die Gerade geht durch den Ursprung — genauer als «linear», und wegen \\(m \\neq 1\\) nicht die Identität.';
          if (A.art === 'konst') return 'Hier steht kein \\(x\\): \\(m = 0\\), der Graph ist waagrecht.';
          if (A.art === 'keine') return 'Hier ist \\(x\\) festgelegt, nicht \\(y\\): Zu dieser einen Stelle gehören unendlich viele \\(y\\)-Werte.';
          return 'Hier sind \\(m \\neq 0\\) und \\(b \\neq 0\\) — keiner der drei Sonderfälle trifft zu.'; },
        loesung: function(A){ return '\\text{' + A.typ + '}'; } },

      'parallel-senkrecht': { felder: ['m_2'], muster: 'm₂ = {m_2}',
        eingabe: function(A){ return { m_2: String(A.m2) }; },
        // m1 nur mit abbrechendem Kehrwert, sonst zeigt loesung() 16 Dezimalstellen
        neu: function(){ var m1 = zufall([-4, -2, -1, -0.5, 0.5, 1, 2, 4]), b1 = zufall(bereich(-5, 5)),
            senk = Math.random() < 0.5, m2 = senk ? -1 / m1 : m1;
          return { m1: m1, b1: b1, m2: m2, senk: senk, m: m1, b: b1,
            text: 'Welche Steigung hat eine Gerade ' + (senk ? '<b>senkrecht</b>' : '<b>parallel</b>')
              + ' zu \\(g: y = ' + lin(m1, b1) + '\\)?' }; },
        fehler: function(A){ var f = [], zweit = A.senk ? A.m1 : -1 / A.m1;
          if (!gl(-A.m2, A.m2)) f.push([{ m_2: String(-A.m2) }, A.senk ? 'Kehrwert' : 'gleiche']);
          if (!gl(zweit, A.m2) && !gl(zweit, -A.m2)) f.push([{ m_2: String(zweit) }, A.senk ? 'nicht parallel' : 'senkrecht']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m_2, A.m2)) return null;
          if (A.senk){
            if (gl(e.m_2, 1 / A.m1)) return 'Kehrwert stimmt, Vorzeichen nicht: \\(m_1 \\cdot m_2 = -1\\).';
            if (gl(e.m_2, -A.m1)) return 'Nur das Vorzeichen gedreht — der Kehrwert fehlt: \\(m_2 = -\\dfrac{1}{m_1}\\).';
            if (gl(e.m_2, A.m1)) return 'Senkrecht ist nicht parallel: \\(m_1 \\cdot m_2 = -1\\).';
            return '\\(m_2 = -\\dfrac{1}{' + tz(A.m1) + '}\\).';
          }
          if (gl(e.m_2, -A.m1)) return 'Parallel heisst <em>gleiche</em> Steigung, nicht die entgegengesetzte.';
          if (gl(e.m_2, -1 / A.m1)) return 'Das wäre senkrecht: Parallel heisst gleiches \\(m\\).';
          return 'Parallel heisst \\(m_2 = m_1 = ' + tz(A.m1) + '\\).'; },
        loesung: function(A){ return 'm_2 = ' + tz(A.m2); } },

      /* ── Kapitel 4 ───────────────────────────────────────────── */
      'aufstellen-m-punkt': { felder: ['b'], muster: 'b = {b}',
        neu: function(){ var m = zufall(STEIG), xp = zufall([-6, -4, -2, 2, 4, 6]), b = zufall(bereich(-6, 6, [0]));
          return { m: m, b: b, xp: xp, yp: m * xp + b,
            text: 'Eine Gerade mit \\(m = ' + tz(m) + '\\) geht durch \\(P' + pkt(xp, m * xp + b) + '\\). Wie gross ist \\(b\\)?' }; },
        fehler: function(A){ var f = [[{ b: String(A.yp + A.m * A.xp) }, 'abziehen']];
          if (!gl(A.yp, A.b) && !gl(A.yp, A.yp + A.m * A.xp)) f.push([{ b: String(A.yp) }, 'Koordinate von']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.b, A.b)) return null;
          if (gl(e.b, A.yp + A.m * A.xp)) return 'Vorzeichen: \\(m \\cdot x_1\\) abziehen, nicht dazuzählen — \\(b = y_1 - m\\,x_1\\).';
          if (gl(e.b, A.yp)) return 'Das ist die \\(y\\)-Koordinate von \\(P\\). \\(b\\) ist der Wert bei \\(x = 0\\).';
          if (gl(e.b, -A.b)) return 'Vorzeichen: \\(b = ' + tz(A.yp) + ' - (' + tz(A.m) + ') \\cdot (' + tz(A.xp) + ') = ' + tz(A.b) + '\\).';
          return 'Setz \\(P\\) in \\(y = ' + tz(A.m) + 'x + b\\) ein und löse nach \\(b\\) auf.'; },
        loesung: function(A){ return 'b = ' + tz(A.yp) + ' - (' + tz(A.m) + ') \\cdot (' + tz(A.xp) + ') = ' + tz(A.b); } },

      'aufstellen-zwei-punkte': { felder: ['m', 'b'], muster: 'f(x) = {m} · x + {b}',
        neu: function(){ var m = zufall(STEIG), d = zufall([2, 2, 4, 4, 6]), b = zufall(bereich(-5, 5)),
            x1 = Number.isInteger(m) ? zufall(bereich(-5, 2)) : zufall([-4, -2, 0, 2]);   // halbe Steigung nur auf geraden Stellen
          return { m: m, b: b, x1: x1, y1: m * x1 + b, x2: x1 + d, y2: m * (x1 + d) + b, dx: d, dy: m * d,
            text: 'Gleichung der Geraden durch \\(A' + pkt(x1, m * x1 + b) + '\\) und \\(B' + pkt(x1 + d, m * (x1 + d) + b) + '\\)?' }; },
        fehler: function(A){ var f = [[{ m: String(-A.m), b: String(A.b) }, 'geht es hin']];
          if (!gl(A.y1 - A.m * A.x1, A.y1 + A.m * A.x1)) f.push([{ m: String(A.m), b: String(A.y1 + A.m * A.x1) }, 'abziehen']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.b, A.b)) return null;
          if (!gl(e.m, A.m)){
            if (gl(e.m, -A.m)) return 'Von \\(A\\) nach \\(B\\) geht es ' + (A.m > 0 ? 'hinauf' : 'hinunter') + ': \\(\\Delta y = ' + tz(A.dy) + '\\), \\(\\Delta x = ' + A.dx + '\\).';
            if (gl(e.m, A.dy)) return 'Das ist \\(\\Delta y\\). Teile noch durch \\(\\Delta x = ' + A.dx + '\\).';
            return 'Zuerst \\(m = \\dfrac{\\Delta y}{\\Delta x} = \\dfrac{' + tz(A.dy) + '}{' + A.dx + '}\\).';
          }
          if (gl(e.b, A.y1 + A.m * A.x1)) return '\\(m \\cdot x_1\\) abziehen, nicht dazuzählen: \\(b = y_1 - m\\,x_1\\).';
          return '\\(m\\) stimmt. Jetzt \\(A\\) einsetzen: \\(b = ' + tz(A.y1) + ' - (' + tz(A.m) + ') \\cdot (' + tz(A.x1) + ')\\).'; },
        loesung: function(A){ return 'm = \\dfrac{' + tz(A.dy) + '}{' + A.dx + '} = ' + tz(A.m) + ',\\quad f(x) = ' + lin(A.m, A.b); } },

      'aufstellen-lage': { felder: ['m', 'b'], muster: 'f(x) = {m} · x + {b}',
        neu: function(){ var m1 = zufall([-4, -2, -1, -0.5, 0.5, 1, 2, 4]), b1 = zufall(bereich(-5, 5)),
            senk = Math.random() < 0.5, m = senk ? -1 / m1 : m1,
            xp = zufall(Number.isInteger(m) ? bereich(-4, 4, [0]) : Math.abs(m) === 0.25 ? [-8, -4, 4, 8] : [-4, -2, 2, 4]),
            b = zufall(bereich(-5, 5));   // halbe/viertel Steigung nur auf passenden Stellen: ganzzahlige Punkte
          return { m1: m1, b1: b1, senk: senk, m: m, b: b, xp: xp, yp: m * xp + b,
            text: 'Gesucht: die Gerade ' + (senk ? '<b>senkrecht</b>' : '<b>parallel</b>') + ' zu \\(g: y = '
              + lin(m1, b1) + '\\) durch \\(P' + pkt(xp, m * xp + b) + '\\).' }; },
        fehler: function(A){ var f = [], falschM = A.senk ? A.m1 : -1 / A.m1;
          if (!gl(falschM, A.m)) f.push([{ m: String(falschM), b: String(A.b) }, A.senk ? 'nicht parallel' : 'gleiches']);
          if (!gl(A.yp + A.m * A.xp, A.b)) f.push([{ m: String(A.m), b: String(A.yp + A.m * A.xp) }, 'abziehen']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.m, A.m) && gl(e.b, A.b)) return null;
          if (!gl(e.m, A.m)){
            if (A.senk && gl(e.m, A.m1)) return 'Senkrecht ist nicht parallel: \\(m_1 \\cdot m_2 = -1\\), also \\(m = -\\dfrac{1}{' + tz(A.m1) + '}\\).';
            if (!A.senk && gl(e.m, -1 / A.m1)) return 'Parallel heisst gleiches \\(m\\), nicht der negative Kehrwert.';
            if (gl(e.m, -A.m)) return 'Vorzeichen von \\(m\\): ' + (A.senk ? '\\(m_1 \\cdot m_2 = -1\\)' : 'gleiche Steigung wie \\(g\\)') + '.';
            return A.senk ? 'Zuerst \\(m = -\\dfrac{1}{m_1}\\).' : 'Zuerst \\(m = m_1 = ' + tz(A.m1) + '\\).';
          }
          if (gl(e.b, A.yp + A.m * A.xp)) return '\\(m \\cdot x_1\\) abziehen, nicht dazuzählen: \\(b = y_1 - m\\,x_1\\).';
          return '\\(m\\) stimmt. Jetzt \\(P\\) einsetzen und nach \\(b\\) auflösen.'; },
        loesung: function(A){ return 'm = ' + tz(A.m) + ',\\quad f(x) = ' + lin(A.m, A.b); } }
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
        for (var v = 0; v < 40 && A.m !== undefined && A.b !== undefined && fest(A.m, A.b); v++) A = T.neu();
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
            var mi = Math.min(A.b, A.b + A.m * 3, A.b - A.m * 3), ma = Math.max(A.b, A.b + A.m * 3, A.b - A.m * 3);
            var mitte = Math.round((mi + ma) / 2), fe = [-4, 4, mitte - 4, mitte + 4];
            bild.setAttribute('viewBox', '0 0 170 170');
            var K = Achsen(bild, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3.5, pfeil: 6, xm: [1], ym: [1] });
            K.kurve(function(x){ return A.m * x + A.b; }, 'kurve');
            K.punkt(0, A.b, 'p-b'); K.punkt(A.s, A.b + A.m * A.s, 'p-pkt');
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

  /* ---------- Minigrafen: <svg class="mini" data-g="m,b[;m,b…]" data-fenster data-punkte data-titel data-xname data-yname> ---------- */
  document.querySelectorAll('svg.mini[data-g]').forEach(function(svg){
    var gg = svg.dataset.g.split(';').map(function(s){ return s.split(',').map(Number); });
    var fe = (svg.dataset.fenster || '-5,5,-5,5').split(',').map(Number);
    var w = 150, h = 150 * (fe[3] - fe[2]) / (fe[1] - fe[0]);
    svg.setAttribute('viewBox', '0 0 150 ' + h.toFixed(1)); svg.setAttribute('role', 'img');
    var K = Achsen(svg, { w: w, h: h, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, xm: [1], ym: [1], pfeil: 6,
      xname: svg.dataset.xname, yname: svg.dataset.yname });
    gg.forEach(function(g, i){ K.kurve(function(x){ return g[0] * x + g[1]; }, 'kurve' + (i ? ' g2' : '')); });
    // Eine Farbe, eine Bedeutung — auch im Minigrafen: (0 | b) orange, die Nullstelle
    // grün, jeder andere Gitterpunkt neutral.
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){
      var q = p.split(',').map(Number);
      K.punkt(q[0], q[1], q[0] === 0 ? 'p-b' : q[1] === 0 ? 'p-null' : 'p-pkt');
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Gerade' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
