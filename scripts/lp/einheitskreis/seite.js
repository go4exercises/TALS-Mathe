<script>
/* Leitprogramm Einheitskreis — Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Kreisbilder zu den Aufgaben. Notation wie auf Themenseite 5.4: Winkel φ in Grad, gemessen ab
   der positiven x-Achse gegen den Uhrzeigersinn; P(cos φ | sin φ) auf dem Einheitskreis;
   Tangens als Höhe von S(1 | tan φ) auf der Tangente x = 1; Quadranten I bis IV.
   Eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15, gleich wie in den Clips):
   blau = Sinus · grün = Cosinus · orange = Tangens · rot = Gegenbeispiel · Tinte = neutral
   (Kreis, Radius, Winkel, Spiegelachsen). Die Themenseite färbt den Sinus in ihren Animationen
   uneinheitlich (Anim 1 rot, Abwickler grün); hier gilt dieselbe Zuordnung wie im Leitprogramm
   Trigonometrische Funktionen (SP 3.5). Zahlen mit Dezimalpunkt und echtem Minus. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', PI = Math.PI;
  function z(n){ var r = Math.round(n * 1000) / 1000; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  /* «≈ 0.643» für gerundete, «= 0.5» für exakte Werte (Live-Anzeigen runden nur mit ≈, HOWTO §15). */
  function gl3(v){ var r = Math.round(v * 1000) / 1000; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '= ') + z(v); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  /* Sinus und Cosinus in Grad — auf den Achsen exakt 0 und ±1 (Math.cos(π/2) ist 6e−17). */
  function sinG(g){ var m = ((g % 360) + 360) % 360; if (m === 0 || m === 180) return 0; if (m === 90) return 1; if (m === 270) return -1; return Math.sin(g * PI / 180); }
  function cosG(g){ return sinG(g + 90); }
  function quadrant(c, s){ if (Math.abs(c) < 1e-9 || Math.abs(s) < 1e-9) return 0; return c > 0 ? (s > 0 ? 1 : 4) : (s > 0 ? 2 : 3); }
  var ROEM = ['', 'I', 'II', 'III', 'IV'];
  function grad(g){ return (g < 0 ? '−' : '') + Math.abs(Math.round(g * 10) / 10) + '°'; }

  /* Exakte Werte der besonderen Winkel (Vielfache von 30° und 45°) als Text. */
  var BETRAG = { 0: '0', 30: '1/2', 45: '√2/2', 60: '√3/2', 90: '1' };
  function referenz(g){ var m = ((g % 360) + 360) % 360; return m <= 90 ? m : m <= 180 ? 180 - m : m <= 270 ? m - 180 : 360 - m; }
  function exaktSin(g){ var r = referenz(g); if (!(r in BETRAG)) return null; var b = BETRAG[r]; return b === '0' ? '0' : (sinG(g) < 0 ? '−' : '') + b; }
  function exaktCos(g){ return exaktSin(g + 90); }
  var TANB = { 0: '0', 30: '√3/3', 45: '1', 60: '√3' };
  function exaktTan(g){ var r = referenz(g); if (r === 90) return 'nicht definiert'; if (!(r in TANB)) return null; var b = TANB[r];
    return b === '0' ? '0' : (sinG(g) * cosG(g) < 0 ? '−' : '') + b; }

  /* ---------- Kreisbild: Koordinatensystem mit gleicher Teilung, Einheitskreis ----------
     o = { w, x0, x1, y0, y1 } — die Höhe folgt aus der gleichen Teilung, damit der Kreis rund
     bleibt und rechte Winkel recht. Gitter alle 0.5, Achsen mit Pfeil und Namen. */
  function Kreisbild(svg, o){
    var x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1, W = o.w, s = W / (x1 - x0), H = Math.round((y1 - y0) * s);
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    function X(x){ return (x - x0) * s; }
    function Y(y){ return H - (y - y0) * s; }
    var g = el(svg, 'g', {}), i;
    for (i = Math.ceil(x0 * 2) / 2; i <= x1 + 1e-9; i += 0.5) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 * 2) / 2; i <= y1 + 1e-9; i += 0.5) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    el(g, 'line', { x1: 0, y1: Y(0), x2: W, y2: Y(0), 'class': 'achse' });
    el(g, 'line', { x1: X(0), y1: 0, x2: X(0), y2: H, 'class': 'achse' });
    var pf = o.pfeil || 7;
    el(g, 'polygon', { points: W + ',' + Y(0) + ' ' + (W - pf) + ',' + (Y(0) - pf / 2) + ' ' + (W - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
    el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
    var fs = o.klein ? 8 : 10;
    [[1, '1'], [-1, '−1']].forEach(function(t){
      if (t[0] > x0 && t[0] < x1) el(g, 'text', { x: X(t[0]) + (t[0] > 0 ? 4 : -4), y: Y(0) + fs + 3, 'text-anchor': t[0] > 0 ? 'start' : 'end', 'class': 'skala' }, t[1]);
      if (t[0] > y0 && t[0] < y1) el(g, 'text', { x: X(0) - 4, y: Y(t[0]) + (t[0] > 0 ? -3 : fs + 2), 'text-anchor': 'end', 'class': 'skala' }, t[1]);
    });
    el(g, 'circle', { cx: X(0), cy: Y(0), r: s, 'class': 'einheitskreis' });
    var ebene = el(svg, 'g', {});
    var schilder = el(svg, 'g', {});
    el(schilder, 'text', { x: W - 3, y: Y(0) - pf - 2, 'text-anchor': 'end', 'class': 'achsname' }, 'x');
    el(schilder, 'text', { x: X(0) + pf + 1, y: pf + 5, 'text-anchor': 'start', 'class': 'achsname' }, 'y');
    var r = o.r || 4.5;
    return {
      X: X, Y: Y, s: s, W: W, H: H, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      strecke: function(xa, ya, xb, yb, cls){ return el(ebene, 'line', { x1: X(xa), y1: Y(ya), x2: X(xb), y2: Y(yb), 'class': cls }); },
      vieleck: function(pkte, cls){ return el(ebene, 'polygon', { points: pkte.map(function(p){ return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join(' '), 'class': cls }); },
      punkt: function(x, y, cls, text, dx, dy, anker){
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: r, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 7 : dx), y: Y(y) + (dy == null ? -7 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      text: function(x, y, t, cls, anker){ return el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': cls }, t); },
      /* Bogen auf einem Kreis um O mit Radius rr (in Einheiten), Winkel in Grad, auch über eine
         Runde hinaus: dann als Spirale, deren Radius je Runde wächst — so sieht man «mehr als eine Runde». */
      bogen: function(rr, w0, w1, cls, spirale){
        var d = '', n = Math.max(2, Math.ceil(Math.abs(w1 - w0) / 3));
        for (var k = 0; k <= n; k++){
          var w = w0 + (w1 - w0) * k / n, rk = rr + (spirale ? 0.05 * Math.abs(w - w0) / 360 : 0);
          d += (k ? 'L' : 'M') + X(rk * Math.cos(w * PI / 180)).toFixed(1) + ' ' + Y(rk * Math.sin(w * PI / 180)).toFixed(1);
        }
        return el(ebene, 'path', { d: d, 'class': cls });
      },
      /* Gerade durch zwei Punkte, am Bildrand abgeschnitten. */
      gerade: function(xa, ya, xb, yb, cls){
        var dx = xb - xa, dy = yb - ya, t0 = -1e9, t1 = 1e9;
        [[dx, xa, x0, x1], [dy, ya, y0, y1]].forEach(function(q){
          if (Math.abs(q[0]) < 1e-12) return;
          var a = (q[2] - q[1]) / q[0], b = (q[3] - q[1]) / q[0];
          t0 = Math.max(t0, Math.min(a, b)); t1 = Math.min(t1, Math.max(a, b));
        });
        return el(ebene, 'line', { x1: X(xa + t0 * dx), y1: Y(ya + t0 * dy), x2: X(xa + t1 * dx), y2: Y(ya + t1 * dy), 'class': cls });
      },
      innen: function(x, y){ return x >= x0 && x <= x1 && y >= y0 && y <= y1; }
    };
  }

  function regler(fig, weiter){
    var r = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){ r[inp.dataset.p] = inp; inp.addEventListener('input', weiter); });
    return r;
  }
  function werte(r){
    var w = {};
    for (var k in r){
      var v = +r[k].value, e = r[k].dataset.einheit || '';
      w[k] = v;
      r[k].parentNode.querySelector('.sl-val').textContent = (v < 0 ? '−' : '') + String(Math.abs(Math.round(v * 100) / 100)) + e;
    }
    return w;
  }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function wahlWert(fig, name){ var e = fig.querySelector('input[name="' + name + '"]:checked'); return e ? e.value : null; }

  /* ---------- Aufgabenleiste in der Simulation (wie in den anderen Leitprogrammen) ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht immer.
     Beim Wechsel gehen Regler, Schalter und Auswahlknöpfe auf ihren Startwert zurück, damit der
     Endzustand der vorigen Aufgabe die nächste nicht schon löst (HOWTO §15). */
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
      if (sim.zeichnen) sim.zeichnen();
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
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; });
      fig.querySelectorAll('.sim-schalter input, input[type=radio]').forEach(function(inp){ inp.checked = inp.defaultChecked; });
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
     zugewiesen — sonst schrieben die Regler weiter ins alte (Prüfung Trigonometrie 05.10.2026, H1). */
  function bewegtMerken(r, bewegt, pruefen){
    for (var k in r) (function(k){ r[k].addEventListener('input', function(){ bewegt[k] = true; pruefen(); }); })(k);
  }
  function leeren(o){ for (var k in o) delete o[k]; }

  /* Gemeinsames Bild der Kapitel 1 und 2: P mit Radius, Dreieck OQP, cos-Strecke (grün) auf der
     x-Achse, sin-Strecke (blau) senkrecht dazu, Winkelbogen (Spirale über eine Runde hinaus). */
  function zeichneP(K, phi, opt){
    opt = opt || {};
    var c = cosG(phi), s = sinG(phi);
    if (Math.abs(c) > 1e-9 && Math.abs(s) > 1e-9) K.vieleck([[0, 0], [c, 0], [c, s]], 'dreieck');
    K.bogen(0.22, 0, phi, 'winkelbogen', Math.abs(phi) > 360);
    K.strecke(0, 0, c, s, 'radius');
    if (Math.abs(c) > 1e-9) K.strecke(0, 0, c, 0, 'koord gruen');
    if (Math.abs(s) > 1e-9) K.strecke(c, 0, c, s, 'koord blau');
    var wm = phi * PI / 180 / 2, wl = Math.abs(phi) > 360 ? (phi > 0 ? 25 : -25) * PI / 180 : wm;
    K.text(0.36 * Math.cos(wl), 0.36 * Math.sin(wl) - 0.05, 'φ', 'w-text');
    K.punkt(c, s, 'p-pkt', 'P', c >= 0 ? 7 : -7, s >= 0 ? -7 : 15, c >= 0 ? 'start' : 'end');
    return { c: c, s: s };
  }
  function quadrantenSchilder(K){
    [[1.2, 1.25, 'I'], [-1.2, 1.25, 'II'], [-1.2, -1.32, 'III'], [1.2, -1.32, 'IV']].forEach(function(q){ K.text(q[0], q[1], q[2], 'q-text'); });
  }

  /* ---------- Kapitel 1: Sinus und Cosinus als Koordinaten ----------
     Unterschied zu «Anim 1 · Sinus und Cosinus am Einheitskreis» der Themenseite: dort 0° bis 360°
     mit Spezialwinkel-Knöpfen. Hier läuft der Winkel von −360° bis 720° (negative Winkel und mehr
     als eine Runde, als Spirale gezeichnet), und die Aufgaben fragen nach Quadrant und Vorzeichen. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.45, x1: 1.45, y0: -1.45, y1: 1.45 });
    var pruefen = function(){}, bewegt = {}, spur = { min: 50, max: 50, an: false }, ziel = null;
    // vor regler() registriert: der Spurenzähler steht, bevor gezeichnet und geprüft wird (HOWTO §15)
    var inp = fig.querySelector('input[data-p="phi"]');
    inp.addEventListener('input', function(){ var v = +inp.value; spur.an = true; spur.min = Math.min(spur.min, v); spur.max = Math.max(spur.max, v); });
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r), c = cosG(w.phi), s = sinG(w.phi);
      return { phi: w.phi, c: c, s: s, q: quadrant(c, s), bewegt: bewegt, rund: spur.an && spur.min <= 0 && spur.max >= 360,
               trifft: function(g){ return Math.abs(c - cosG(g)) < 1e-9 && Math.abs(s - sinG(g)) < 1e-9; } }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(bewegt); spur.min = spur.max = 50; spur.an = false; ziel = null; } };
    function zeichnen(){
      var st = zust();
      K.leeren(); quadrantenSchilder(K);
      if (ziel !== null) K.punkt(cosG(ziel), sinG(ziel), 'p-ziel');
      zeichneP(K, st.phi);
      var lage = st.q ? 'Quadrant ' + ROEM[st.q] : (Math.abs(st.s) < 1e-9 ? 'auf der x-Achse' : 'auf der y-Achse');
      rolle(fig, 'formel').innerHTML = 'φ = ' + grad(st.phi) + '; &nbsp;' + sp('tx-gruen', 'cos φ ' + gl3(st.c)) + '; &nbsp;'
        + sp('tx-blau', 'sin φ ' + gl3(st.s)) + '; &nbsp;' + lage;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Dreh \\(P\\) einmal ganz herum — von \\(0^\\circ\\) bis \\(360^\\circ\\).', ok: function(s){ return s.rund; } },
      // Startzustand φ = 50° (Quadrant I, wie im Clip) — keine Aufgabe ist schon gelöst.
      { text: 'Stell einen Winkel ein, bei dem der Cosinus negativ und der Sinus positiv ist.', ok: function(s){ return s.q === 2; } },
      { text: 'Stell einen Winkel ein, bei dem beide Koordinaten von \\(P\\) negativ sind.', ok: function(s){ return s.q === 3; } },
      { text: 'Stell \\(\\varphi = 200^\\circ\\) ein. Welches Vorzeichen hat \\(\\cos\\varphi\\)?', ok: function(s){ return s.phi === 200; } },
      { text: 'Stell einen <b>negativen</b> Winkel ein, bei dem \\(P\\) im vierten Quadranten liegt.', ok: function(s){ return s.phi < 0 && s.q === 4; } },
      { text: 'Stell einen Winkel <b>über</b> \\(360^\\circ\\) ein, bei dem \\(P\\) im zweiten Quadranten liegt.', ok: function(s){ return s.phi > 360 && s.q === 2; } },
      // Zielspiel: Der Punkt zu 335° — auch −25° und 695° treffen ihn (Vergleich der Lage, nicht des Reglerwerts).
      { text: 'Triff den grau markierten Punkt.', setup: function(){ ziel = 335; }, ok: function(s){ return s.trifft(335); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: besondere Winkel ----------
     Unterschied zur Themenseite (Anim 1 mit Spezialwinkel-Knöpfen, Werte auf drei Dezimalen): hier
     nur Vielfache von 15°, der Spiegelpunkt im ersten Quadranten (gestrichelt) zeigt den
     Referenzwinkel, und die Werte stehen exakt mit Wurzeln da, wo es sie gibt. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.45, x1: 1.45, y0: -1.45, y1: 1.45 });
    var pruefen = function(){}, besucht = {}, bewegt = {};
    var inp = fig.querySelector('input[data-p="phi"]');
    inp.addEventListener('input', function(){ besucht[+inp.value] = true; });
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r), c = cosG(w.phi), s = sinG(w.phi);
      return { phi: w.phi, c: c, s: s, q: quadrant(c, s), besucht: besucht, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(besucht); leeren(bewegt); } };
    function zeichnen(){
      var st = zust(), ref = referenz(st.phi);
      K.leeren(); quadrantenSchilder(K);
      // Spiegelbild im ersten Quadranten: derselbe Betrag, ohne Vorzeichen (Hilfslinie, abschaltbar)
      if (st.q && st.q !== 1){
        var rc = cosG(ref), rs = sinG(ref);
        K.strecke(0, 0, rc, rs, 'spiegel hilfslinie');
        K.strecke(rc, 0, rc, rs, 'spiegel hilfslinie');
        K.punkt(rc, rs, 'p-hohl hilfslinie');
      }
      zeichneP(K, st.phi);
      var es = exaktSin(st.phi), ec = exaktCos(st.phi);
      var wert = function(e, v){ return e !== null ? '= ' + e : gl3(v); };
      rolle(fig, 'formel').innerHTML = 'φ = ' + grad(st.phi) + '; &nbsp;' + (st.q ? 'Quadrant ' + ROEM[st.q] + '; &nbsp;Referenzwinkel ' + ref + '°' : 'auf einer Achse')
        + '<br>' + sp('tx-gruen', 'cos φ ' + wert(ec, st.c)) + '; &nbsp;' + sp('tx-blau', 'sin φ ' + wert(es, st.s));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Besuche alle vier Winkel mit dem Referenzwinkel \\(60^\\circ\\).', ok: function(s){ return s.besucht[60] && s.besucht[120] && s.besucht[240] && s.besucht[300]; } },
      // Startzustand φ = 45° — keine Aufgabe ist schon gelöst. Die Clipbeispiele (150°, 225°, 300°) sind keine Ziele.
      { text: 'Stell \\(\\varphi = \\tfrac{7\\pi}{4}\\) ein — der Winkel ist im Bogenmass gegeben.', ok: function(s){ return s.phi === 315; } },
      { text: 'Wo ist \\(\\cos\\varphi = -\\tfrac12\\) und \\(\\sin\\varphi \\gt 0\\)?', ok: function(s){ return s.phi === 120; } },
      { text: 'Wo ist \\(\\sin\\varphi = -\\tfrac12\\) und \\(\\cos\\varphi \\lt 0\\)?', ok: function(s){ return s.phi === 210; } },
      { text: 'Stell den Winkel im zweiten Quadranten mit dem Referenzwinkel \\(45^\\circ\\) ein.', ok: function(s){ return s.phi === 135; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Tangens und trigonometrischer Pythagoras ----------
     Unterschied zu «Anim 2 · Tangens» und «Anim 3 · Ähnlichkeit und Pythagoras» der Themenseite:
     beide in einem Bild. Die Gerade durch O und P trifft die Tangente x = 1 in S — im 2. und
     3. Quadranten ihre Verlängerung über O hinaus (so auch in jedem Quadranten nachgezeichnet,
     HOWTO §15). Ein Schalter blendet die zwei ähnlichen Dreiecke OQP und ORS ein. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 300, x0: -1.35, x1: 1.95, y0: -2.2, y1: 2.2 });
    var pruefen = function(){}, bewegt = {}, quadr = {};
    var inp = fig.querySelector('input[data-p="phi"]');
    inp.addEventListener('input', function(){ var q = quadrant(cosG(+inp.value), sinG(+inp.value)); if (q) quadr[q] = true; });
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    function zust(){ var w = werte(r), c = cosG(w.phi), s = sinG(w.phi), def = Math.abs(c) > 1e-9;
      return { phi: w.phi, c: c, s: s, q: quadrant(c, s), def: def, t: def ? s / c : null, quadr: quadr, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(bewegt); leeren(quadr); } };
    function zeichnen(){
      var st = zust(), c = st.c, s = st.s;
      K.leeren();
      K.strecke(1, -2.2, 1, 2.2, 'tangente');
      if (st.def){
        var t = st.t, tb = Math.max(-2.2, Math.min(2.2, t));
        if (Math.abs(s) > 1e-9){
          K.vieleck([[0, 0], [c, 0], [c, s]], 'dreieck hilfslinie');
          K.vieleck([[0, 0], [1, 0], [1, t]], 'dreieck orange hilfslinie');
        }
        // Gerade durch O und P bis S: im 2. und 3. Quadranten von P aus durch O hindurch.
        if (Math.abs(t) <= 2.2) K.strecke(c < 0 ? c : 0, c < 0 ? s : 0, 1, t, 'strahl');
        else K.gerade(0, 0, c, s, 'strahl');
        K.strecke(1, 0, 1, tb, 'koord orange');
        if (Math.abs(t) <= 2.2) K.punkt(1, t, 'p-lauf orange', 'S', 7, t >= 0 ? -6 : 14);
        else K.text(1.06, tb > 0 ? 2.02 : -2.1, 'S weiter ' + (t > 0 ? 'oben' : 'unten'), 's-text orange', 'start');
      } else {
        K.gerade(0, 0, c, s, 'strahl');
      }
      K.strecke(0, 0, c, s, 'radius');
      if (Math.abs(c) > 1e-9) K.strecke(0, 0, c, 0, 'koord gruen duenn');
      if (Math.abs(s) > 1e-9) K.strecke(c, 0, c, s, 'koord blau duenn');
      K.bogen(0.22, 0, st.phi, 'winkelbogen');
      K.punkt(1, 0, 'p-klein', 'R', 5, 13);
      K.punkt(c, s, 'p-pkt', 'P', c >= 0 ? -7 : -7, s >= 0 ? -7 : 15, 'end');
      var tz = st.def ? sp('tx-orange', 'tan φ = sin φ / cos φ ' + gl3(st.t)) : sp('tx-orange', 'tan φ nicht definiert') + ' (' + sp('tx-gruen', 'cos φ = 0') + ')';
      var s2 = Math.round(s * s * 1000) / 1000;
      rolle(fig, 'formel').innerHTML = 'φ = ' + grad(st.phi) + '; &nbsp;' + sp('tx-blau', 'sin φ ' + gl3(s)) + '; &nbsp;' + sp('tx-gruen', 'cos φ ' + gl3(c))
        + '<br>' + tz + '<br>sin²φ + cos²φ ' + (Math.abs(s * s - s2) > 1e-9 ? '≈ ' : '= ') + z(s2) + ' + ' + z(1 - s2) + ' = 1';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Fahr mit \\(\\varphi\\) durch alle vier Quadranten. Wo liegt \\(S\\)?', ok: function(s){ return s.quadr[1] && s.quadr[2] && s.quadr[3] && s.quadr[4]; } },
      // Startzustand φ = 40° (wie im Clip), tan φ ≈ 0.839 — keine Aufgabe ist schon gelöst.
      { text: 'Stell \\(\\varphi\\) so ein, dass es keinen Punkt \\(S\\) gibt.', ok: function(s){ return !s.def; } },
      { text: 'Wo ist \\(\\tan\\varphi = 1\\) im dritten Quadranten?', ok: function(s){ return s.phi === 225; } },
      { text: 'Stell einen Winkel ein, bei dem \\(P\\) über der \\(x\\)-Achse liegt und \\(\\tan\\varphi\\) negativ ist.', ok: function(s){ return s.q === 2; } },
      { text: 'Wo ist \\(\\tan\\varphi = -1\\) im vierten Quadranten?', ok: function(s){ return s.phi === 315; } },
      { text: 'Finde einen Winkel mit \\(\\tan\\varphi \\approx 1.73\\).', ok: function(s){ return s.phi === 60 || s.phi === 240; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Symmetrien ----------
     Unterschied zum «Symmetrie-Spiegel» der Themenseite: dort α bis 90° und vier Chips mit der Regel
     als Formel. Hier dieselben vier Spiegelungen, aber ohne fertige Regel — die Live-Zeile nennt nur
     die Koordinaten von A und B, die Regel liest man selbst ab. */
  var MODI = {
    '180-a': { beta: function(a){ return 180 - a; }, name: '180° − α', achse: 'y-Achse' },
    'neg':   { beta: function(a){ return -a; },       name: '−α',       achse: 'x-Achse' },
    '180+a': { beta: function(a){ return 180 + a; }, name: '180° + α', achse: 'Ursprung O' },
    '90-a':  { beta: function(a){ return 90 - a; },  name: '90° − α',  achse: 'Gerade y = x' }
  };
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.45, x1: 1.45, y0: -1.45, y1: 1.45 });
    var pruefen = function(){}, bewegt = {}, modi = {};
    // vor regler() registriert: Wer im Startmodus zieht, hat ihn ausprobiert.
    fig.querySelector('input[data-p="a"]').addEventListener('input', function(){ modi[wahlWert(fig, 's4-modus') || '180-a'] = true; });
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    fig.querySelectorAll('input[name="s4-modus"]').forEach(function(rb){ rb.addEventListener('change', function(){ modi[rb.value] = true; zeichnen(); }); });
    function zust(){ var w = werte(r), m = wahlWert(fig, 's4-modus') || '180-a', b = MODI[m].beta(w.a);
      return { a: w.a, m: m, beta: b, modi: modi, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(bewegt); leeren(modi); } };
    function zeichnen(){
      var st = zust(), a = st.a, b = st.beta, ca = cosG(a), sa = sinG(a), cb = cosG(b), sb = sinG(b);
      K.leeren();
      if (st.m === '180-a') K.strecke(0, -1.45, 0, 1.45, 'spiegelachse');
      else if (st.m === 'neg') K.strecke(-1.45, 0, 1.45, 0, 'spiegelachse');
      else if (st.m === '90-a') K.strecke(-1.45, -1.45, 1.45, 1.45, 'spiegelachse');
      else K.strecke(ca, sa, cb, sb, 'spiegelachse');
      // A: Koordinaten durchgezogen; B: gestrichelt
      K.strecke(0, 0, ca, sa, 'radius');
      if (Math.abs(ca) > 1e-9) K.strecke(0, 0, ca, 0, 'koord gruen');
      if (Math.abs(sa) > 1e-9) K.strecke(ca, 0, ca, sa, 'koord blau');
      K.strecke(0, 0, cb, sb, 'radius gestr');
      if (Math.abs(cb) > 1e-9) K.strecke(0, 0, cb, 0, 'koord gruen gestr');
      if (Math.abs(sb) > 1e-9) K.strecke(cb, 0, cb, sb, 'koord blau gestr');
      K.punkt(ca, sa, 'p-pkt', 'A', 7, sa >= 0 ? -7 : 15);
      K.punkt(cb, sb, 'p-lauf b', 'B', cb >= 0 ? 7 : -7, sb >= 0 ? -7 : 15, cb >= 0 ? 'start' : 'end');
      var bT = st.m === 'neg' ? '−' + a + '° (= ' + (360 - a) + '°)' : b + '°';
      rolle(fig, 'formel').innerHTML = 'Spiegelung ' + MODI[st.m].name + ' an der ' + MODI[st.m].achse.replace('Ursprung O', 'Mitte O') + '; &nbsp;α = ' + a + '°; &nbsp;β = ' + bT
        + '<br>A: ' + sp('tx-gruen', 'cos α ' + gl3(ca)) + '; ' + sp('tx-blau', 'sin α ' + gl3(sa))
        + '<br>B: ' + sp('tx-gruen', 'cos β ' + gl3(cb)) + '; ' + sp('tx-blau', 'sin β ' + gl3(sb));
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Probier alle vier Spiegelungen aus und zieh jeweils an \\(\\alpha\\).', ok: function(s){ return s.modi['180-a'] && s.modi['neg'] && s.modi['180+a'] && s.modi['90-a'] && s.bewegt.a; } },
      // Startzustand: 180° − α mit α = 25° (wie im Clip) — keine Aufgabe ist schon gelöst.
      { text: 'Stell die Spiegelung ein, bei der Sinus <b>und</b> Cosinus das Vorzeichen wechseln.', ok: function(s){ return s.m === '180+a'; } },
      { text: 'Stell die Spiegelung ein, bei der nur der Sinus das Vorzeichen wechselt.', ok: function(s){ return s.m === 'neg'; } },
      { text: 'Spiegelung \\(90^\\circ - \\alpha\\): Bei welchem \\(\\alpha\\) fallen \\(A\\) und \\(B\\) zusammen?', ok: function(s){ return s.m === '90-a' && s.a === 45; } },
      { text: 'Spiegelung \\(180^\\circ - \\alpha\\): Stell \\(\\alpha\\) so ein, dass \\(B\\) bei \\(110^\\circ\\) liegt.', ok: function(s){ return s.m === '180-a' && s.a === 70; } },
      { text: 'Wähle Spiegelung und \\(\\alpha\\) so, dass \\(B\\) bei \\(200^\\circ\\) liegt.', ok: function(s){ return s.m === '180+a' && s.a === 20; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: vom Wert zum Winkel ----------
     Unterschied zur Animation «Hauptwerte am Einheitskreis» der Themenseite: dort stehen beide
     Winkel als Zahl da. Hier nennt die Live-Zeile nur den Winkel des Rechners; die übrigen
     Kreispunkte mit demselben Wert sind grau markiert — den zweiten Winkel zu berechnen ist Stoff
     von GF 5.5 (Leitprogramm Trigonometrische Gleichungen). */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.45, x1: 1.45, y0: -1.45, y1: 1.45 });
    var pruefen = function(){}, bewegt = {};
    var r = regler(fig, zeichnen);
    bewegtMerken(r, bewegt, function(){ pruefen(); });
    fig.querySelectorAll('input[name="s5-fn"]').forEach(function(rb){ rb.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), fn = wahlWert(fig, 's5-fn') || 'sin', v = Math.round(w.w * 100) / 100, phi1 = null, n = 0;
      if (fn === 'tan'){ phi1 = Math.atan(v) * 180 / PI; n = 2; }
      else if (Math.abs(v) <= 1 + 1e-12){ phi1 = (fn === 'sin' ? Math.asin(v) : Math.acos(v)) * 180 / PI; n = Math.abs(Math.abs(v) - 1) < 1e-12 ? 1 : 2; }
      return { fn: fn, w: v, phi1: phi1, n: n, bewegt: bewegt }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(bewegt); } };
    var FARBE = { sin: 'blau', cos: 'gruen', tan: 'orange' };
    var BEREICH = { sin: '[−90°; 90°]', cos: '[0°; 180°]', tan: ']−90°; 90°[' };
    function zeichnen(){
      var st = zust(), v = st.w, f = st.fn;
      K.leeren();
      // Hauptwertbereich als breites Band auf dem Kreis
      if (f === 'cos') K.bogen(1, 0, 180, 'band gruen'); else K.bogen(1, -90, 90, 'band ' + FARBE[f]);
      if (f === 'tan'){ K.punkt(0, 1, 'p-hohl'); K.punkt(0, -1, 'p-hohl'); }
      if (f === 'sin') K.strecke(-1.45, v, 1.45, v, 'waagrechte');
      else if (f === 'cos') K.strecke(v, -1.45, v, 1.45, 'waagrechte');
      else { K.gerade(-1, -v, 1, v, 'waagrechte'); K.strecke(1, -1.45, 1, 1.45, 'tangente'); if (Math.abs(v) <= 1.45) K.punkt(1, v, 'p-klein orange', 'S', 6, v >= 0 ? -5 : 13); }
      if (st.phi1 !== null){
        var p1 = st.phi1, c1 = cosG(p1), s1 = sinG(p1), andere = [];
        if (f === 'sin' && st.n === 2) andere.push([-c1, s1]);
        if (f === 'cos' && st.n === 2) andere.push([c1, -s1]);
        if (f === 'tan') andere.push([-c1, -s1]);
        andere.forEach(function(p){ K.strecke(0, 0, p[0], p[1], 'radius gestr'); K.punkt(p[0], p[1], 'p-hohl'); });
        K.bogen(0.22, 0, p1, 'winkelbogen');
        K.strecke(0, 0, c1, s1, 'radius');
        K.punkt(c1, s1, 'p-lauf ' + FARBE[f], 'φ₁', c1 >= 0 ? 7 : -7, s1 >= 0 ? -7 : 15, c1 >= 0 ? 'start' : 'end');
      }
      var name = f === 'sin' ? 'sin' : f === 'cos' ? 'cos' : 'tan';
      var zeile = sp('tx-' + FARBE[f], name + ' φ = ' + z(v)) + '; &nbsp;';
      zeile += st.phi1 === null ? '<b>kein Winkel</b>: ' + name + ' φ liegt immer zwischen −1 und 1'
        : 'Rechner: ' + name + '⁻¹(' + z(v) + ') ' + (Math.abs(st.phi1 * 10 - Math.round(st.phi1 * 10)) > 1e-6 ? '≈ ' : '= ') + grad(st.phi1);
      zeile += '<br>Hauptwertbereich ' + BEREICH[f] + '; &nbsp;Kreispunkte mit diesem Wert: ' + st.n;
      rolle(fig, 'formel').innerHTML = zeile;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh an \\(w\\). Wie viele Kreispunkte haben denselben Wert?', ok: function(s){ return s.bewegt.w; } },
      // Startzustand: Sinus, w = 0.4 (wie im Clip) — keine Aufgabe ist schon gelöst.
      { text: 'Sinus: Stell einen Wert ein, zu dem der Rechner einen <b>negativen</b> Winkel liefert.', ok: function(s){ return s.fn === 'sin' && s.phi1 !== null && s.phi1 < 0; } },
      { text: 'Sinus: Bei welchem Wert gibt es nur <b>einen</b> Kreispunkt?', ok: function(s){ return s.fn === 'sin' && s.n === 1; } },
      { text: 'Schalte auf Cosinus. Stell einen Wert ein, zu dem der Rechner einen stumpfen Winkel liefert.', ok: function(s){ return s.fn === 'cos' && s.phi1 !== null && s.phi1 > 90 + 1e-9 && s.phi1 < 180 - 1e-9; } },
      { text: 'Cosinus: Zu welchem Wert liefert der Rechner genau \\(60^\\circ\\)?', ok: function(s){ return s.fn === 'cos' && Math.abs(s.w - 0.5) < 1e-9; } },
      { text: 'Schalte auf Tangens. Stell den Wert ein, zu dem die beiden Kreispunkte bei \\(45^\\circ\\) und \\(225^\\circ\\) liegen.', ok: function(s){ return s.fn === 'tan' && Math.abs(s.w - 1) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Hilfslinien-Schalter ---------- */
  document.querySelectorAll('.hilfs-schalter input').forEach(function(hs){
    var fig = hs.closest('figure');
    hs.addEventListener('change', function(){ fig.classList.toggle('ohne-hilfslinien', !hs.checked); });
  });

  /* ---------- Kreisbilder zu den Aufgaben: <svg class="ek-mini" data-ek='{…}'> ----------
     p: Winkel der Punkte (mit sin- und cos-Strecke, wenn sc), tan: Winkel mit Punkt S auf der
     Tangente, h: Waagrechte y = h, fenster: [x0, x1, y0, y1], namen: Beschriftung je Punkt. */
  document.querySelectorAll('svg.ek-mini[data-ek]').forEach(function(svg){
    var d = JSON.parse(svg.dataset.ek), fe = d.fenster || [-1.4, 1.4, -1.4, 1.4];
    var K = Kreisbild(svg, { w: d.breite || 200, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3.5, pfeil: 6, klein: true });
    if (d.tan) K.strecke(1, fe[2], 1, fe[3], 'tangente');
    if (d.h != null) K.strecke(fe[0], d.h, fe[1], d.h, 'waagrechte');
    (d.p || []).forEach(function(g, i){
      var c = cosG(g), s = sinG(g);
      K.strecke(0, 0, c, s, 'radius');
      if (d.sc){ if (Math.abs(c) > 1e-9) K.strecke(0, 0, c, 0, 'koord gruen'); if (Math.abs(s) > 1e-9) K.strecke(c, 0, c, s, 'koord blau'); }
      K.punkt(c, s, i && d.hohl ? 'p-hohl' : 'p-pkt', (d.namen || [])[i] || '', c >= 0 ? 5 : -5, s >= 0 ? -5 : 12, c >= 0 ? 'start' : 'end');
    });
    (d.tan || []).forEach(function(g){
      var c = cosG(g), s = sinG(g), t = s / c;
      K.strecke(c < 0 ? c : 0, c < 0 ? s : 0, 1, t, 'strahl');
      K.strecke(1, 0, 1, t, 'koord orange');
      K.punkt(1, t, 'p-lauf orange', 'S', 5, t >= 0 ? -5 : 12);
    });
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Einheitskreis');
    svg.setAttribute('role', 'img');
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    function r3(v){ return Math.round(v * 1000) / 1000; }
    var gl = function(a, b){ return Math.abs(a - b) < 1e-9; };
    /* Eingaben: Zahl, Bruch, Dezimalkomma; ein angehängtes ° wird überlesen. */
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/°$/, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    /* Exakte Werte: Text der Auswahl ↔ Zahl ↔ LaTeX. */
    var SC = ['−1', '−√3/2', '−√2/2', '−1/2', '0', '1/2', '√2/2', '√3/2', '1'];
    var TW = ['−√3', '−1', '−√3/3', '0', '√3/3', '1', '√3', 'nicht definiert'];
    function texW(t){
      if (t === 'nicht definiert') return '\\text{nicht definiert}';
      var neg = t.charAt(0) === '−', b = neg ? t.slice(1) : t;
      var m = { '1/2': '\\tfrac12', '√2/2': '\\tfrac{\\sqrt2}{2}', '√3/2': '\\tfrac{\\sqrt3}{2}', '√3/3': '\\tfrac{\\sqrt3}{3}', '√3': '\\sqrt3' }[b] || b;
      return (neg ? '-' : '') + m;
    }
    function zahlW(t){
      if (t === 'nicht definiert') return NaN;
      var neg = t.charAt(0) === '−', b = neg ? t.slice(1) : t;
      var v = { '0': 0, '1': 1, '1/2': 0.5, '√2/2': Math.SQRT2 / 2, '√3/2': Math.sqrt(3) / 2, '√3/3': Math.sqrt(3) / 3, '√3': Math.sqrt(3) }[b];
      return neg ? -v : v;
    }
    function gegen(t){ return t === '0' || t === 'nicht definiert' ? t : (t.charAt(0) === '−' ? t.slice(1) : '−' + t); }
    /* Winkel als LaTeX, wahlweise im Bogenmass (Vielfache von π/6 und π/4). */
    function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
    function bogenTex(g){
      var n = g, d = 180, k = ggT(n, d) || 1; n /= k; d /= k;
      if (n === 0) return '0';
      var zl = (Math.abs(n) === 1 ? '' : Math.abs(n)) + '\\pi';
      return (n < 0 ? '-' : '') + (d === 1 ? zl : '\\tfrac{' + zl + '}{' + d + '}');
    }
    function gradTex(g){ return tz(g) + '^\\circ'; }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15), je Typ ein eigener
       Schlüssel (T.schl). Quellen: Clips · Simulationen · Aufgaben der Kapitel · Vortest ·
       Gesamttest (downloads/leitprogramme/einheitskreis/gesamttest.tex). */
    var SPERRE = [
      // Kapitel 1 — Clips (50°, 140°, 230°, 320°, −60°), Simulation (200°, 335°), Aufgaben 1b–1d, Gesamttest G1, G6
      'vz|50', 'vz|140', 'vz|230', 'vz|320', 'vz|-60', 'vz|200', 'vz|335', 'vz|250', 'vz|-20', 'vz|480', 'vz|220', 'vz|110', 'vz|-30', 'vz|235',
      'ko|p|-0.6|0.8', 'ko|p|0.28|-0.96', 'ko|r|160', 'ko|r|250', 'ko|r|220', 'ko|r|50', 'ko|r|140', 'ko|r|235',
      // Kapitel 2 — Clip (45°, 60°, 30°, 150°, 225°, 300°), Kontrollclip (cos 240°, sin 270°), Aufgaben 2a/2b, Gesamttest G2
      'ew|sin|45', 'ew|cos|45', 'ew|sin|60', 'ew|cos|60', 'ew|sin|30', 'ew|cos|30', 'ew|sin|150', 'ew|cos|150',
      'ew|sin|225', 'ew|cos|225', 'ew|sin|300', 'ew|cos|300', 'ew|cos|240', 'ew|sin|270',
      'ew|cos|135', 'ew|sin|210', 'ew|cos|315', 'ew|sin|240', 'ew|cos|330',
      'rw|200', 'rw|150', 'rw|225', 'rw|300',
      // Kapitel 3 — Kontrollclip (tan 135°), Aufgaben 3a, Gesamttest G2; Pythagoras: Clip, Kontrollclip, 3b, G3
      'tw|135', 'tw|150', 'tw|300', 'tw|240',
      'py|sin|0.6|2', 'py|sin|0.8|2', 'py|cos|-5/13|3', 'py|sin|-0.96|4',
      // Kapitel 4 — Clip (α = 25°), Kontrollclip (40°/140°, −70°, 20°/70°), Aufgaben 4a (α = 15°), Gesamttest G4 (α = 35°)
      'sw|25|sin|155', 'sw|25|cos|155', 'sw|25|sin|-25', 'sw|25|cos|-25', 'sw|25|sin|205', 'sw|25|cos|205', 'sw|25|sin|65', 'sw|25|cos|65',
      'sw|40|sin|140', 'sw|70|cos|-70', 'sw|20|sin|70', 'sw|70|cos|20',
      'sw|15|sin|165', 'sw|15|cos|195', 'sw|15|cos|-15',
      'sw|35|sin|145', 'sw|35|cos|215', 'sw|35|sin|55', 'sw|35|cos|-35',
      'sr|sin|pi2',
      // Kapitel 5 — Clip (390°), Kontrollclip (400°, −120°), Aufgaben 5a, Hauptwert: Kontrollclip (sin −0.5, cos 0.6)
      'pe|sin|390', 'pe|cos|390', 'pe|sin|400', 'pe|cos|400', 'pe|sin|-120', 'pe|cos|-120', 'pe|sin|495', 'pe|cos|-240', 'pe|tan|585',
      'hw|sin|210', 'hw|sin|330', 'hw|cos|305'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function winkelOhneAchse(von, bis, schritt){ var l = []; for (var g = von; g <= bis; g += schritt) if (g % 90 !== 0) l.push(g); return l; }

    var TYPEN = {
      /* ── Kapitel 1: Sinus und Cosinus als Koordinaten ───────────────── */
      'vorzeichen': { felder: ['q', 's', 'c'], muster: 'Quadrant {q:I|II|III|IV} &nbsp; Vorzeichen von sin φ: {s:+|−} &nbsp; von cos φ: {c:+|−}',
        schl: function(A){ return 'vz|' + A.phi; },
        eingabe: function(A){ return { q: ROEM[A.q], s: A.s, c: A.c }; },
        neu: function(){
          var phi = zufall(winkelOhneAchse(-350, 710, 10));
          var c = cosG(phi), s = sinG(phi);
          return { phi: phi, q: quadrant(c, s), s: s > 0 ? '+' : '−', c: c > 0 ? '+' : '−',
            text: 'Zum Winkel \\(\\varphi = ' + gradTex(phi) + '\\) gehört der Punkt \\(P\\) auf dem Einheitskreis. In welchem Quadranten liegt er, und welche Vorzeichen haben \\(\\sin\\varphi\\) und \\(\\cos\\varphi\\)?' }; },
        fehler: function(A){ var f = [];
          if (A.s !== A.c) f.push([{ q: ROEM[A.q], s: A.c, c: A.s }, 'Vertauscht']);
          if (A.phi < 0){ var qg = quadrant(cosG(-A.phi), sinG(-A.phi)); if (qg !== A.q) f.push([{ q: ROEM[qg], s: A.s, c: A.c }, 'Uhrzeigersinn']); }
          return f; },
        pruefen: function(A, e){
          var qe = ROEM.indexOf(e.q);
          if (qe === A.q && e.s === A.s && e.c === A.c) return null;
          if (qe !== A.q){
            if (A.phi < 0 && qe === quadrant(cosG(-A.phi), sinG(-A.phi))) return 'Ein negativer Winkel dreht im <b>Uhrzeigersinn</b>: von der positiven \\(x\\)-Achse aus nach unten.';
            if (A.phi > 360) return 'Mehr als eine Runde: Zieh \\(360^\\circ\\) ab, bis der Winkel zwischen \\(0^\\circ\\) und \\(360^\\circ\\) liegt — dort liegt derselbe Punkt.';
            return 'Zähl ab der positiven \\(x\\)-Achse gegen den Uhrzeigersinn: Quadrant I bis \\(90^\\circ\\), II bis \\(180^\\circ\\), III bis \\(270^\\circ\\), IV bis \\(360^\\circ\\).';
          }
          if (e.s === A.c && e.c === A.s) return 'Vertauscht: Der Sinus ist die \\(y\\)-Koordinate (Höhe), der Cosinus die \\(x\\)-Koordinate.';
          return 'Der Quadrant stimmt. Liegt \\(P\\) dort über oder unter der \\(x\\)-Achse (Sinus)? Rechts oder links der \\(y\\)-Achse (Cosinus)?'; },
        loesung: function(A){ return '\\varphi = ' + gradTex(A.phi) + ':\\ \\text{Quadrant ' + ROEM[A.q] + '},\\ \\sin\\varphi ' + (A.s === '+' ? '\\gt' : '\\lt') + ' 0,\\ \\cos\\varphi ' + (A.c === '+' ? '\\gt' : '\\lt') + ' 0'; } },

      'koordinaten': { felder: ['c', 's'], muster: 'cos φ = {c} &nbsp; sin φ = {s}',
        schl: function(A){ return A.art === 'p' ? 'ko|p|' + A.c + '|' + A.s : 'ko|r|' + A.phi; },
        eingabe: function(A){ return { c: String(A.c), s: String(A.s) }; },
        neu: function(){
          if (Math.random() < 0.45){
            var p = zufall([[0.6, 0.8], [0.8, 0.6], [0.28, 0.96], [0.96, 0.28]]), sx = zufall([1, -1]), sy = zufall([1, -1]);
            var c = r3(p[0] * sx), s = r3(p[1] * sy);
            return { art: 'p', c: c, s: s, text: 'Der Punkt \\(P(' + tz(c) + ' \\mid ' + tz(s) + ')\\) liegt auf dem Einheitskreis. Gib \\(\\cos\\varphi\\) und \\(\\sin\\varphi\\) an.' };
          }
          var phi = zufall(winkelOhneAchse(95, 355, 1).filter(function(g){ return g % 15 !== 0; }));
          return { art: 'r', phi: phi, c: r3(cosG(phi)), s: r3(sinG(phi)), cw: cosG(phi), sw: sinG(phi),
            text: 'Bestimme mit dem Taschenrechner (Modus DEG) die Koordinaten von \\(P\\) zum Winkel \\(\\varphi = ' + gradTex(phi) + '\\), auf drei Dezimalen.' }; },
        fehler: function(A){ var f = [[{ c: String(A.s), s: String(A.c) }, 'Vertauscht']];
          if (A.art === 'r') f.push([{ c: String(r3(Math.cos(A.phi))), s: String(r3(Math.sin(A.phi))) }, 'DEG']);
          else f.push([{ c: String(-A.c), s: String(A.s) }, 'Vorzeichen']);
          return f.filter(function(x){ return !(gl(+x[0].c, A.c) && gl(+x[0].s, A.s)); }); },
        pruefen: function(A, e){
          var tol = A.art === 'r' ? 0.0015 : 1e-9, nah = function(a, b){ return Math.abs(a - b) <= tol; };
          if (nah(e.c, A.c) && nah(e.s, A.s)) return null;
          if (nah(e.c, A.s) && nah(e.s, A.c)) return 'Vertauscht: Der Cosinus ist die \\(x\\)-Koordinate von \\(P\\), der Sinus die \\(y\\)-Koordinate.';
          if (A.art === 'r' && Math.abs(e.c - Math.cos(A.phi)) < 0.0015 && Math.abs(e.s - Math.sin(A.phi)) < 0.0015) return 'Der Rechner steht im Bogenmass (RAD). Stell ihn auf Grad (DEG) und rechne nochmals.';
          if (nah(Math.abs(e.c), Math.abs(A.c)) && nah(Math.abs(e.s), Math.abs(A.s))) return 'Die Beträge stimmen. Prüf die Vorzeichen: In welchem Quadranten liegt \\(P\\)?';
          if (A.art === 'p') return 'Lies ab: \\(P(\\cos\\varphi \\mid \\sin\\varphi)\\) — zuerst die \\(x\\)-, dann die \\(y\\)-Koordinate.';
          return 'Tipp \\(\\cos(' + A.phi + ')\\) und \\(\\sin(' + A.phi + ')\\) ein und runde auf drei Dezimalen.'; },
        loesung: function(A){ return (A.art === 'r' ? '\\cos ' + gradTex(A.phi) + ' \\approx ' + tz(A.c) + ',\\ \\sin ' + gradTex(A.phi) + ' \\approx ' + tz(A.s)
                                                    : '\\cos\\varphi = ' + tz(A.c) + ',\\ \\sin\\varphi = ' + tz(A.s)); } },

      /* ── Kapitel 2: besondere Winkel (ohne Taschenrechner) ─────────── */
      'exakter-wert': { felder: ['y'], muster: 'Wert = {y:' + SC.join('|') + '}',
        schl: function(A){ return 'ew|' + A.fn + '|' + A.phi; },
        eingabe: function(A){ return { y: A.y }; },
        neu: function(){
          var fn = zufall(['sin', 'cos']), phi = zufall([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]);
          var bogen = Math.random() < 0.3 && phi !== 0;
          var y = fn === 'sin' ? exaktSin(phi) : exaktCos(phi);
          return { fn: fn, phi: phi, y: y, bogen: bogen,
            text: 'Gib ohne Taschenrechner exakt an: \\(\\' + fn + (bogen ? '\\left(' + bogenTex(phi) + '\\right)' : ' ' + gradTex(phi)) + '\\).' }; },
        fehler: function(A){ var f = [], ander = A.fn === 'sin' ? exaktCos(A.phi) : exaktSin(A.phi);
          if (A.y !== '0') f.push([{ y: gegen(A.y) }, 'Vorzeichen']);
          if (ander !== A.y && ander !== gegen(A.y)) f.push([{ y: ander }, 'Cosinus']);
          return f; },
        pruefen: function(A, e){
          e = { y: String(e.y) };   // Auswahlfeld: immer Text, auch wenn ein Prüfer «1» als Zahl übergibt
          if (e.y === A.y) return null;
          var ander = A.fn === 'sin' ? exaktCos(A.phi) : exaktSin(A.phi);
          if (e.y === gegen(A.y)) return 'Der Betrag stimmt, das Vorzeichen nicht: Liegt \\(P\\) ' + (A.fn === 'sin' ? 'über oder unter der \\(x\\)-Achse?' : 'rechts oder links der \\(y\\)-Achse?');
          if (e.y === ander || e.y === gegen(ander)) return 'Das ist der Betrag des ' + (A.fn === 'sin' ? 'Cosinus' : 'Sinus') + '. Der ' + (A.fn === 'sin' ? 'Sinus ist die Höhe von \\(P\\).' : 'Cosinus ist die \\(x\\)-Koordinate von \\(P\\).') + ' Miss den Referenzwinkel zur \\(x\\)-Achse.';
          return 'Quadrant bestimmen, Referenzwinkel zur \\(x\\)-Achse, Betrag aus der Tabelle, Vorzeichen aus dem Quadranten.'; },
        loesung: function(A){ var r = referenz(A.phi);
          return '\\' + A.fn + (A.bogen ? '\\left(' + bogenTex(A.phi) + '\\right) = \\' + A.fn + ' ' + gradTex(A.phi) : ' ' + gradTex(A.phi))
            + (r === A.phi || A.phi % 90 === 0 ? '' : ' = ' + ((A.fn === 'sin' ? sinG(A.phi) : cosG(A.phi)) < 0 ? '-' : '') + '\\' + A.fn + ' ' + gradTex(r)) + ' = ' + texW(A.y); } },

      'referenzwinkel': { felder: ['q', 'r'], muster: 'Quadrant {q:I|II|III|IV} &nbsp; Referenzwinkel {r} °',
        schl: function(A){ return 'rw|' + A.phi; },
        eingabe: function(A){ return { q: ROEM[A.q], r: String(A.r) }; },
        neu: function(){
          var phi = zufall(winkelOhneAchse(5, 355, 5).filter(function(g){ return g > 90; }));
          return { phi: phi, q: quadrant(cosG(phi), sinG(phi)), r: referenz(phi),
            text: 'In welchem Quadranten liegt \\(P\\) zum Winkel \\(\\varphi = ' + gradTex(phi) + '\\)? Wie gross ist der Referenzwinkel — der spitze Winkel zwischen \\(OP\\) und der \\(x\\)-Achse?' }; },
        fehler: function(A){ var f = [[{ q: ROEM[A.q], r: String(90 - A.r) }, 'Winkel zur']];
          if (A.q === 3) f.push([{ q: ROEM[A.q], r: String(360 - A.phi) }, '180']);
          if (A.q === 4) f.push([{ q: ROEM[A.q], r: String(A.phi - 180) }, '360']);
          return f.filter(function(x){ return +x[0].r !== A.r; }); },
        pruefen: function(A, e){
          var qe = ROEM.indexOf(e.q);
          if (qe !== A.q) return 'Zähl ab der positiven \\(x\\)-Achse gegen den Uhrzeigersinn: II von \\(90^\\circ\\) bis \\(180^\\circ\\), III bis \\(270^\\circ\\), IV bis \\(360^\\circ\\).';
          if (gl(e.r, A.r)) return null;
          if (gl(e.r, 90 - A.r)) return 'Das ist der Winkel zur \\(y\\)-Achse. Der Referenzwinkel liegt zwischen \\(OP\\) und der <b>\\(x\\)-Achse</b>.';
          if (A.q === 3 && gl(e.r, 360 - A.phi)) return 'Im dritten Quadranten liegt die \\(x\\)-Achse bei \\(180^\\circ\\) am nächsten: \\(\\varphi - 180^\\circ\\).';
          if (A.q === 4 && gl(e.r, A.phi - 180)) return 'Im vierten Quadranten liegt die \\(x\\)-Achse bei \\(360^\\circ\\) am nächsten: \\(360^\\circ - \\varphi\\).';
          return 'Der Referenzwinkel ist der Abstand zur nächsten Hälfte der \\(x\\)-Achse: zu \\(180^\\circ\\) oder zu \\(360^\\circ\\). Er liegt zwischen \\(0^\\circ\\) und \\(90^\\circ\\).'; },
        loesung: function(A){ var f = A.q === 2 ? '180^\\circ - ' + gradTex(A.phi) : A.q === 3 ? gradTex(A.phi) + ' - 180^\\circ' : '360^\\circ - ' + gradTex(A.phi);
          return '\\text{Quadrant ' + ROEM[A.q] + '},\\ ' + f + ' = ' + gradTex(A.r); } },

      /* ── Kapitel 3: Tangens und trigonometrischer Pythagoras ───────── */
      'tan-wert': { felder: ['y'], muster: 'tan φ = {y:' + TW.join('|') + '}',
        schl: function(A){ return 'tw|' + A.phi; },
        eingabe: function(A){ return { y: A.y }; },
        neu: function(){
          var phi = zufall([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]);
          return { phi: phi, y: exaktTan(phi), text: 'Gib ohne Taschenrechner exakt an: \\(\\tan ' + gradTex(phi) + '\\).' }; },
        fehler: function(A){
          if (A.y === 'nicht definiert') return [[{ y: '0' }, 'Cosinus']];
          if (A.y === '0') return [[{ y: 'nicht definiert' }, 'Sinus']];
          var f = [[{ y: gegen(A.y) }, 'Vorzeichen']], kehr = { '√3': '√3/3', '√3/3': '√3' };
          var b = A.y.replace('−', ''); if (kehr[b]) f.push([{ y: (A.y.charAt(0) === '−' ? '−' : '') + kehr[b] }, 'Umgekehrt']);
          return f; },
        pruefen: function(A, e){
          e = { y: String(e.y) };   // Auswahlfeld: immer Text, auch wenn ein Prüfer «1» als Zahl übergibt
          if (e.y === A.y) return null;
          if (A.y === 'nicht definiert') return 'Wie gross ist der Cosinus bei \\(' + gradTex(A.phi) + '\\)? Durch null kann man nicht teilen — und die Gerade durch \\(O\\) und \\(P\\) ist parallel zur Tangente.';
          if (A.y === '0') return 'Bei \\(' + gradTex(A.phi) + '\\) ist der Sinus \\(0\\), also auch der Zähler von \\(\\tfrac{\\sin\\varphi}{\\cos\\varphi}\\) — \\(S\\) liegt auf der \\(x\\)-Achse.';
          if (e.y === gegen(A.y)) return 'Der Betrag stimmt. Vorzeichen: Haben Sinus und Cosinus im Quadranten von \\(P\\) dasselbe Vorzeichen?';
          var b = A.y.replace('−', ''), eb = e.y.replace('−', '');
          if ((b === '√3' && eb === '√3/3') || (b === '√3/3' && eb === '√3')) return 'Umgekehrt gerechnet: \\(\\tan\\varphi = \\tfrac{\\sin\\varphi}{\\cos\\varphi}\\) — Sinus oben, Cosinus unten.';
          return 'Rechne \\(\\tan\\varphi = \\tfrac{\\sin\\varphi}{\\cos\\varphi}\\) mit den exakten Werten aus Kapitel 2.'; },
        loesung: function(A){ return A.y === 'nicht definiert' ? '\\cos ' + gradTex(A.phi) + ' = 0:\\ \\tan ' + gradTex(A.phi) + '\\ \\text{ist nicht definiert}'
                                                                : '\\tan ' + gradTex(A.phi) + ' = \\tfrac{\\sin ' + gradTex(A.phi) + '}{\\cos ' + gradTex(A.phi) + '} = ' + texW(A.y); } },

      'pythagoras': { felder: ['w', 't'], muster: function(A){ return (A.fn === 'sin' ? 'cos φ' : 'sin φ') + ' = {w} &nbsp; tan φ = {t}'; },
        schl: function(A){ return 'py|' + A.fn + '|' + A.gT + '|' + A.q; },
        eingabe: function(A){ return { w: A.wT, t: A.tT }; },
        neu: function(){
          var tr = zufall([[3, 4, 5], [4, 3, 5], [5, 12, 13], [12, 5, 13], [8, 15, 17], [15, 8, 17], [7, 24, 25], [24, 7, 25]]);
          var q = zufall([1, 2, 3, 4]), fn = zufall(['sin', 'cos']);
          var sx = (q === 1 || q === 4) ? 1 : -1, sy = (q === 1 || q === 2) ? 1 : -1;
          // gegeben g = a/c (Sinus oder Cosinus), gesucht der andere: b/c mit Vorzeichen des Quadranten
          var a = tr[0], b = tr[1], c = tr[2];
          var gs = fn === 'sin' ? sy : sx, ws = fn === 'sin' ? sx : sy;
          var dez = c === 5 || c === 25;                       // Nenner 5 und 25: als Dezimalzahl
          var gT = dez ? tz(r3(gs * a / c)) : (gs < 0 ? '-' : '') + a + '/' + c;
          var gTex = dez ? tz(r3(gs * a / c)) : (gs < 0 ? '-' : '') + '\\tfrac{' + a + '}{' + c + '}';
          var s = fn === 'sin' ? gs * a / c : ws * b / c, co = fn === 'sin' ? ws * b / c : gs * a / c;
          var tn = s / co, sn = fn === 'sin' ? a : b, cn = fn === 'sin' ? b : a;
          return { fn: fn, q: q, a: a, b: b, c: c, g: gs * a / c, w: ws * b / c, t: tn, gT: gT,
            wT: dez ? tz(r3(ws * b / c)) : (ws < 0 ? '-' : '') + b + '/' + c,
            tT: (tn < 0 ? '-' : '') + sn + '/' + cn, dez: dez,
            text: 'Es gilt \\(\\' + fn + '\\varphi = ' + gTex + '\\), und \\(\\varphi\\) liegt im ' + ['', 'ersten', 'zweiten', 'dritten', 'vierten'][q] + ' Quadranten. Berechne ohne Taschenrechner \\(\\' + (fn === 'sin' ? 'cos' : 'sin') + '\\varphi\\) und \\(\\tan\\varphi\\) (Bruch oder Dezimalzahl).' }; },
        fehler: function(A){ var f = [[{ w: (A.w < 0 ? '' : '-') + A.b + '/' + A.c, t: A.tT }, 'Vorzeichen']];
          var kehr = (A.t < 0 ? '-' : '') + (A.fn === 'sin' ? A.b + '/' + A.a : A.a + '/' + A.b);
          if (A.a !== A.b) f.push([{ w: A.wT, t: kehr }, 'Sinus oben']);
          f.push([{ w: tz(r3((A.w < 0 ? -1 : 1) * (1 - A.a / A.c))), t: A.tT }, 'Quadrate']);
          return f; },
        pruefen: function(A, e){
          var nah = function(x, y){ return Math.abs(x - y) < 0.0015; };
          var r = [];
          if (!nah(e.w, A.w)){
            if (nah(e.w, -A.w)) r.push('Vorzeichen: Die Wurzel liefert nur den Betrag. Im ' + ROEM[A.q] + '. Quadranten ist ' + (A.fn === 'sin' ? 'der Cosinus' : 'der Sinus') + ' ' + (A.w < 0 ? 'negativ' : 'positiv') + '.');
            else if (nah(Math.abs(e.w), 1 - A.a / A.c)) r.push('Nicht \\(1 - ' + A.a + '/' + A.c + '\\): Die <b>Quadrate</b> ergänzen sich zu \\(1\\) — \\(\\' + (A.fn === 'sin' ? 'cos' : 'sin') + '^2\\varphi = 1 - \\' + A.fn + '^2\\varphi\\).');
            else r.push('Rechne \\(\\' + (A.fn === 'sin' ? 'cos' : 'sin') + '^2\\varphi = 1 - \\' + A.fn + '^2\\varphi\\), zieh die Wurzel und wähle das Vorzeichen nach dem Quadranten.');
          }
          if (!nah(e.t, A.t)){
            if (nah(e.t, 1 / A.t)) r.push('Tangens: \\(\\tfrac{\\sin\\varphi}{\\cos\\varphi}\\) — Sinus oben, nicht unten.');
            else if (nah(e.t, -A.t)) r.push('Tangens: Prüf das Vorzeichen — positiv im I. und III. Quadranten, negativ im II. und IV.');
            else r.push('Tangens: \\(\\tan\\varphi = \\tfrac{\\sin\\varphi}{\\cos\\varphi}\\) mit deinen beiden Werten.');
          }
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ var an = A.fn === 'sin' ? 'cos' : 'sin';
          return '\\' + an + '^2\\varphi = 1 - \\left(\\tfrac{' + A.a + '}{' + A.c + '}\\right)^2 = \\tfrac{' + (A.b * A.b) + '}{' + (A.c * A.c) + '},\\ \\' + an + '\\varphi = ' + (A.w < 0 ? '-' : '') + '\\tfrac{' + A.b + '}{' + A.c + '},\\ \\tan\\varphi = ' + (A.t < 0 ? '-' : '') + '\\tfrac{' + (A.fn === 'sin' ? A.a : A.b) + '}{' + (A.fn === 'sin' ? A.b : A.a) + '}'; } },

      /* ── Kapitel 4: Symmetrien (ohne Taschenrechner) ─────────────── */
      'symmetrie-wert': { felder: ['y'], muster: 'Wert ≈ {y}',
        schl: function(A){ return 'sw|' + A.a + '|' + A.fn + '|' + A.beta; },
        eingabe: function(A){ return { y: String(A.y) }; },
        neu: function(){
          var a = zufall([10, 20, 25, 35, 40, 50, 55, 65, 70, 80]);
          var s = r3(sinG(a)), c = r3(cosG(a)), fn = zufall(['sin', 'cos']);
          var art = zufall(['180-a', '180+a', '360-a', 'neg', '90-a']);
          var beta = { '180-a': 180 - a, '180+a': 180 + a, '360-a': 360 - a, 'neg': -a, '90-a': 90 - a }[art];
          var y = fn === 'sin' ? { '180-a': s, '180+a': -s, '360-a': -s, 'neg': -s, '90-a': c }[art]
                               : { '180-a': -c, '180+a': -c, '360-a': c, 'neg': c, '90-a': s }[art];
          return { a: a, s: s, c: c, fn: fn, art: art, beta: beta, y: y,
            text: 'Es gilt \\(\\sin ' + gradTex(a) + ' \\approx ' + s + '\\) und \\(\\cos ' + gradTex(a) + ' \\approx ' + c + '\\). Gib ohne Taschenrechner an: \\(\\' + fn + (beta < 0 ? '(' + gradTex(beta) + ')' : ' ' + gradTex(beta)) + '\\).' }; },
        fehler: function(A){ var f = [[{ y: String(-A.y) }, 'Vorzeichen']];
          var ander = (A.y === A.s || A.y === -A.s) ? A.c : A.s;
          if (!gl(ander, Math.abs(A.y))) f.push([{ y: String(A.y < 0 ? -ander : ander) }, 'Gefragt']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.y, A.y)) return null;
          var rw = { '180-a': 'an der \\(y\\)-Achse gespiegelt: Die Höhe bleibt, die \\(x\\)-Koordinate kippt', '180+a': 'am Ursprung gespiegelt: Beide Koordinaten kippen',
                     '360-a': 'an der \\(x\\)-Achse gespiegelt: Die \\(x\\)-Koordinate bleibt, die Höhe kippt', 'neg': 'an der \\(x\\)-Achse gespiegelt: Die \\(x\\)-Koordinate bleibt, die Höhe kippt',
                     '90-a': 'an der Geraden \\(y = x\\) gespiegelt: \\(x\\) und \\(y\\) tauschen die Plätze' }[A.art];
          if (gl(e.y, -A.y)) return 'Vorzeichen: Der Punkt zu \\(' + gradTex(A.beta) + '\\) ist ' + rw + '.';
          if (gl(Math.abs(e.y), A.fn === 'sin' ? (A.art === '90-a' ? A.s : A.c) : (A.art === '90-a' ? A.c : A.s))) return 'Gefragt ist der ' + (A.fn === 'sin' ? 'Sinus' : 'Cosinus') + '. Der Punkt zu \\(' + gradTex(A.beta) + '\\) ist ' + rw + '.';
          return 'Zeichne die Punkte zu \\(' + gradTex(A.a) + '\\) und \\(' + gradTex(A.beta) + '\\) in den Einheitskreis. Wie liegen sie zueinander?'; },
        loesung: function(A){ var ausdr = { '180-a': '180^\\circ - ', '180+a': '180^\\circ + ', '360-a': '360^\\circ - ', 'neg': '-', '90-a': '90^\\circ - ' }[A.art] + gradTex(A.a);
          var regel = A.fn === 'sin' ? { '180-a': '\\sin', '180+a': '-\\sin', '360-a': '-\\sin', 'neg': '-\\sin', '90-a': '\\cos' }[A.art]
                                     : { '180-a': '-\\cos', '180+a': '-\\cos', '360-a': '\\cos', 'neg': '\\cos', '90-a': '\\sin' }[A.art];
          return '\\' + A.fn + '(' + ausdr + ') = ' + regel + ' ' + gradTex(A.a) + ' \\approx ' + tz(A.y); } },

      'symmetrie-regel': { felder: ['r'], muster: '= {r:sin α|−sin α|cos α|−cos α|tan α|−tan α}',
        schl: function(A){ return 'sr|' + A.fn + '|' + A.k; },
        eingabe: function(A){ return { r: A.r }; },
        neu: function(){
          var R = [
            ['sin', '180-', 'sin α'], ['cos', '180-', '−cos α'], ['tan', '180-', '−tan α'],
            ['sin', '180+', '−sin α'], ['cos', '180+', '−cos α'], ['tan', '180+', 'tan α'],
            ['sin', 'neg', '−sin α'], ['cos', 'neg', 'cos α'], ['tan', 'neg', '−tan α'],
            ['sin', '360-', '−sin α'], ['cos', '360-', 'cos α'],
            ['sin', '90-', 'cos α'], ['cos', '90-', 'sin α'],
            ['sin', 'pi2', 'cos α'], ['cos', 'pi2', 'sin α'], ['sin', 'pi-', 'sin α'], ['cos', 'pi+', '−cos α']];
          var w = zufall(R);
          var arg = { '180-': '180^\\circ - \\alpha', '180+': '180^\\circ + \\alpha', 'neg': '-\\alpha', '360-': '360^\\circ - \\alpha', '90-': '90^\\circ - \\alpha',
                      'pi2': '\\tfrac{\\pi}{2} - \\alpha', 'pi-': '\\pi - \\alpha', 'pi+': '\\pi + \\alpha' }[w[1]];
          return { fn: w[0], k: w[1], r: w[2], arg: arg,
            text: 'Vereinfache mit einer Symmetrie des Einheitskreises: \\(\\' + w[0] + '(' + arg + ')\\)' + (w[1].charAt(0) === 'p' ? ' — der Winkel steht im Bogenmass.' : '.') }; },
        fehler: function(A){ var f = [[{ r: gegen(A.r) }, 'Vorzeichen']];
          var neg = A.r.charAt(0) === '−' ? '−' : '', tausch = { 'sin α': 'cos α', 'cos α': 'sin α' }[A.r.replace('−', '')];
          if (tausch) f.push([{ r: neg + tausch }, A.k === '90-' || A.k === 'pi2' ? 'Komplement' : 'Funktion']);
          return f; },
        pruefen: function(A, e){
          if (e.r === A.r) return null;
          var kompl = A.k === '90-' || A.k === 'pi2';
          if (e.r === gegen(A.r)) return 'Vorzeichen: Zeichne \\(\\alpha\\) im ersten Quadranten und den gespiegelten Punkt. Liegt er ' + (A.fn === 'cos' ? 'rechts oder links der \\(y\\)-Achse?' : A.fn === 'sin' ? 'über oder unter der \\(x\\)-Achse?' : 'in einem Quadranten, in dem der Tangens positiv ist?');
          if (kompl) return 'Komplement: Die Spiegelung an der Geraden \\(y = x\\) vertauscht die Koordinaten — aus dem Sinus wird der Cosinus und umgekehrt.';
          if (e.r.indexOf(A.fn) < 0) return 'Bei dieser Spiegelung bleibt die Funktion dieselbe, nur das Vorzeichen kann kippen. Getauscht wird nur beim Komplement \\(90^\\circ - \\alpha\\).';
          return 'Zeichne \\(\\alpha\\) und den gespiegelten Punkt in den Einheitskreis und vergleiche die Koordinaten.'; },
        loesung: function(A){ return '\\' + A.fn + '(' + A.arg + ') = ' + A.r.replace('−', '-').replace('sin', '\\sin').replace('cos', '\\cos').replace('tan', '\\tan').replace('α', '\\alpha'); } },

      /* ── Kapitel 5: Periode und Umkehroperationen ─────────────────── */
      'periode': { felder: ['w'], muster: function(A){ return A.fn + ' φ = ' + A.fn + ' {w} °'; },
        schl: function(A){ return 'pe|' + A.fn + '|' + A.phi; },
        eingabe: function(A){ return { w: String(A.w) }; },
        neu: function(){
          var fn = zufall(['sin', 'cos', 'tan']), p = fn === 'tan' ? 180 : 360, phi;
          do { phi = zufall([1, -1]) * (5 * Math.floor(Math.random() * 216 + 1)); } while ((phi >= 0 && phi < p) || phi % 90 === 0 && fn === 'tan');
          var w = ((phi % p) + p) % p;
          return { fn: fn, phi: phi, p: p, w: w,
            text: 'Führe mit der Periode zurück: \\(\\' + fn + (phi < 0 ? '(' + gradTex(phi) + ')' : ' ' + gradTex(phi)) + ' = \\' + fn + ' w\\) mit \\(0^\\circ \\le w \\lt ' + p + '^\\circ\\). Gib \\(w\\) an.' }; },
        fehler: function(A){ var f = [];
          if (A.phi < 0) f.push([{ w: String((((-A.phi) % A.p) + A.p) % A.p) }, 'negativ']);
          if (A.fn === 'tan' && ((A.phi % 360) + 360) % 360 !== A.w) f.push([{ w: String(((A.phi % 360) + 360) % 360) }, '180']);
          if (A.phi > 2 * A.p) f.push([{ w: String(A.phi - A.p) }, 'Bereich']);
          return f.filter(function(x){ return +x[0].w !== A.w; }); },
        pruefen: function(A, e){
          if (gl(e.w, A.w)) return null;
          if (e.w < 0 || e.w >= A.p) return 'Ausserhalb des Bereichs: \\(w\\) soll zwischen \\(0^\\circ\\) und \\(' + A.p + '^\\circ\\) liegen. ' + (A.fn === 'tan' ? 'Der Tangens wiederholt sich schon nach \\(180^\\circ\\).' : 'Zieh so oft \\(360^\\circ\\) ab (oder zähl dazu), bis es passt.');
          if (A.phi < 0 && gl(e.w, (((-A.phi) % A.p) + A.p) % A.p)) return 'Beim negativen Winkel nicht einfach das Minus weglassen: \\(' + gradTex(A.phi) + '\\) plus Vielfache von \\(' + A.p + '^\\circ\\).';
          if (A.fn === 'tan' && gl(e.w, ((A.phi % 360) + 360) % 360)) return 'Für den Tangens genügt eine halbe Runde: Er wiederholt sich nach \\(180^\\circ\\), gesucht ist \\(w \\lt 180^\\circ\\).';
          return 'Zähl Vielfache von \\(' + A.p + '^\\circ\\) dazu oder ab: \\(' + gradTex(A.phi) + ' ' + (A.phi > 0 ? '-' : '+') + ' k \\cdot ' + A.p + '^\\circ\\).'; },
        loesung: function(A){ var k = (A.phi - A.w) / A.p;
          return '\\' + A.fn + (A.phi < 0 ? '(' + gradTex(A.phi) + ')' : ' ' + gradTex(A.phi)) + ' = \\' + A.fn + '(' + gradTex(A.phi) + (k > 0 ? ' - ' + (k === 1 ? '' : k + ' \\cdot ') : ' + ' + (k === -1 ? '' : (-k) + ' \\cdot ')) + A.p + '^\\circ) = \\' + A.fn + ' ' + gradTex(A.w); } },

      'hauptwert': { felder: ['p'], muster: 'Rechner: φ = {p} °',
        schl: function(A){ return 'hw|' + A.fn + '|' + A.beta; },
        eingabe: function(A){ return { p: String(A.p) }; },
        neu: function(){
          var fn = zufall(['sin', 'cos', 'tan']), beta = zufall(winkelOhneAchse(10, 350, 5).filter(function(g){ return g > 90; }));
          var w = r3(fn === 'sin' ? sinG(beta) : fn === 'cos' ? cosG(beta) : sinG(beta) / cosG(beta));
          var q = quadrant(cosG(beta), sinG(beta)), p;
          if (fn === 'sin') p = q === 4 ? beta - 360 : 180 - beta;            // II: 180 − β; III: 180 − β (negativ); IV: β − 360
          else if (fn === 'cos') p = beta <= 180 ? beta : 360 - beta;
          else p = q === 4 ? beta - 360 : beta - 180;
          return { fn: fn, beta: beta, w: w, p: p, q: q,
            text: 'Der Winkel \\(\\beta = ' + gradTex(beta) + '\\) hat \\(\\' + fn + '\\beta \\approx ' + tz(w) + '\\). Welchen Winkel liefert der Taschenrechner für \\(\\' + fn + '^{-1}(' + tz(w) + ')\\)? Überleg ohne Rechner, auf ganze Grad.' }; },
        fehler: function(A){ var f = [[{ p: String(A.beta) }, 'Hauptwert']];
          if (A.p < 0 && A.p + 360 !== A.beta) f.push([{ p: String(A.p + 360) }, 'negativ']);
          return f.filter(function(x){ return +x[0].p !== A.p; }); },
        pruefen: function(A, e){
          if (Math.abs(e.p - A.p) <= 0.6) return null;
          var B = { sin: '[−90°; 90°]', cos: '[0°; 180°]', tan: ']−90°; 90°[' }[A.fn];
          if (Math.abs(e.p - A.beta) <= 0.6) return '\\(\\beta\\) hat diesen Wert — aber der Rechner gibt nur Winkel aus dem Hauptwertbereich ' + B + '. Welcher Kreispunkt mit demselben Wert liegt dort?';
          if (A.p < 0 && Math.abs(e.p - A.p - 360) <= 0.6) return 'Gleicher Punkt, aber der Rechner zählt hier negativ: Er liefert einen Winkel aus ' + B + '.';
          if (A.fn === 'cos' && e.p < 0) return 'Der Arkuscosinus liefert nie negative Winkel, sondern einen aus ' + B + ' — die obere Kreishälfte.';
          return 'Zeichne den Punkt zu \\(\\beta\\) und alle Kreispunkte mit demselben ' + (A.fn === 'sin' ? 'Sinus (gleiche Höhe)' : A.fn === 'cos' ? 'Cosinus (gleiche \\(x\\)-Koordinate)' : 'Tangens (gegenüberliegender Punkt)') + '. Der Rechner nimmt den aus ' + B + '.'; },
        loesung: function(A){ return '\\' + A.fn + '^{-1}(' + tz(A.w) + ') \\approx ' + gradTex(A.p); } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        // Trifft der Wurf eine Aufgabe, die das Leitprogramm an fester Stelle stellt, wird neu
        // gewürfelt (SPERRE oben). 40 Versuche reichen weit; danach gilt der letzte Wurf.
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = typeof T.muster === 'function' ? T.muster(A) : T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
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
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('input') ? 'Fülle alle Felder aus.' : 'Wähle aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-0.6</code>, <code>0.25</code> oder Brüche wie <code>-12/13</code>.'; return; }
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
})();
</script>
