<script>
/* Leitprogramm Trigonometrische Gleichungen — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Kreis- und Kurvenbilder zu den Aufgaben. Notation wie auf Themenseite 5.5:
   Winkel φ in Grad, ab der positiven x-Achse gegen den Uhrzeigersinn; P(cos φ | sin φ) auf dem
   Einheitskreis, Tangens als Höhe von S(1 | tan φ) auf der Tangente x = 1 (wie LP Einheitskreis);
   Lösungsmenge 𝕃 mit Strichpunkt, aufsteigend; Intervalle [0°; 360°[; alle Lösungen mit k ∈ ℤ.
   Eine Farbe, eine Bedeutung (gleich wie in den Clips g5-5-lp-*):
   blau = Sinus · grün = Cosinus · orange = Tangens · rot = Gegenbeispiel · Tinte = neutral
   (Kreis, Gerade y = c bzw. x = c, Tangente). Zahlen mit Dezimalpunkt und echtem Minus. */
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
  /* Sinus und Cosinus in Grad — auf den Achsen exakt 0 und ±1 (Math.cos(π/2) ist 6e−17). */
  function sinG(g){ var m = ((g % 360) + 360) % 360; if (m === 0 || m === 180) return 0; if (m === 90) return 1; if (m === 270) return -1; return Math.sin(g * PI / 180); }
  function cosG(g){ return sinG(g + 90); }
  function tanG(g){ var c = cosG(g); return Math.abs(c) < 1e-12 ? NaN : sinG(g) / c; }
  function deg(r){ return r * 180 / PI; }
  function mod360(g){ var m = ((g % 360) + 360) % 360; return Math.abs(m - 360) < 1e-9 ? 0 : m; }
  /* «23.6°» — auf eine Dezimale, ganze Zahlen ohne «.0» nur, wenn exakt */
  function grad1(g){ var r = Math.round(g * 10) / 10; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + Math.abs(r).toFixed(Math.abs(g - Math.round(g)) < 1e-9 ? 0 : 1) + '°'; }
  function ungefaehr(g){ return Math.abs(g * 10 - Math.round(g * 10)) > 1e-6 ? '≈ ' : '= '; }

  /* Lösungen von f(φ) = c im Intervall [0°; 360°[, aufsteigend (f: 'sin', 'cos', 'tan'). */
  function loesungen(f, c){
    var l = [];
    if (f === 'tan'){ var t = deg(Math.atan(c)); l = [mod360(t), mod360(t + 180)]; }
    else {
      if (Math.abs(c) > 1 + 1e-12) return [];
      var a = f === 'sin' ? deg(Math.asin(Math.max(-1, Math.min(1, c)))) : deg(Math.acos(Math.max(-1, Math.min(1, c))));
      l = f === 'sin' ? [mod360(a), mod360(180 - a)] : [mod360(a), mod360(360 - a)];
    }
    l.sort(function(a, b){ return a - b; });
    return l.filter(function(v, i){ return i === 0 || Math.abs(v - l[i - 1]) > 1e-7; });
  }
  /* Hauptwert des Rechners */
  function hauptwert(f, c){ return f === 'sin' ? deg(Math.asin(c)) : f === 'cos' ? deg(Math.acos(c)) : deg(Math.atan(c)); }
  var FARBE = { sin: 'blau', cos: 'gruen', tan: 'orange' };

  /* ---------- Kreisbild (wie LP Einheitskreis): gleich geteilte Achsen, Einheitskreis ---------- */
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
    (o.ymarken || [[1, '1'], [-1, '−1']]).forEach(function(t){
      if (t[0] > y0 && t[0] < y1) el(g, 'text', { x: X(0) - 4, y: Y(t[0]) + (t[0] > 0 ? -3 : fs + 2), 'text-anchor': 'end', 'class': 'skala' }, t[1]);
    });
    [[1, '1'], [-1, '−1']].forEach(function(t){
      if (t[0] > x0 && t[0] < x1) el(g, 'text', { x: X(t[0]) + (t[0] > 0 ? 4 : -4), y: Y(0) + fs + 3, 'text-anchor': t[0] > 0 ? 'start' : 'end', 'class': 'skala' }, t[1]);
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
      punkt: function(x, y, cls, text, dx, dy, anker){
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: r, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 7 : dx), y: Y(y) + (dy == null ? -7 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      text: function(x, y, t, cls, anker){ return el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': cls }, t); },
      bogen: function(rr, w0, w1, cls){
        var d = '', n = Math.max(2, Math.ceil(Math.abs(w1 - w0) / 3));
        for (var k = 0; k <= n; k++){
          var w = w0 + (w1 - w0) * k / n;
          d += (k ? 'L' : 'M') + X(rr * Math.cos(w * PI / 180)).toFixed(1) + ' ' + Y(rr * Math.sin(w * PI / 180)).toFixed(1);
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
      x0: x0, x1: x1, y0: y0, y1: y1
    };
  }
  /* Beschriftung eines Kreispunkts radial aussen. */
  function kreisPunkt(K, g, cls, text){
    var c = cosG(g), s = sinG(g);
    K.punkt(c, s, cls, text, c >= 0 ? 7 : -7, s >= 0 ? -7 : 15, c >= 0 ? 'start' : 'end');
  }

  /* ---------- Kurvenbild: Winkel φ in Grad waagrecht, y senkrecht (Kapitel 4, Aufgaben) ---------- */
  function Kurvenbild(svg, o){
    // Beginnt das Bild bei 0°, steht die y-Achse am Rand: links Platz für die Zahlen ±1 (Prüfung 08.10.2026, M6).
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1, li = x0 >= 0 ? 18 : 4, re = 4;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    function X(x){ return li + (x - x0) / (x1 - x0) * (W - li - re); }
    function Y(y){ return H - 6 - (y - y0) / (y1 - y0) * (H - 12); }
    var g = el(svg, 'g', {}), schritt = o.schritt || 90, x;
    for (x = Math.ceil(x0 / schritt) * schritt; x <= x1 + 1e-9; x += schritt) el(g, 'line', { x1: X(x), y1: Y(y0), x2: X(x), y2: Y(y1), 'class': 'gitter' });
    [-1, 1].forEach(function(y){ if (y > y0 && y < y1) el(g, 'line', { x1: X(x0), y1: Y(y), x2: X(x1), y2: Y(y), 'class': 'gitter' }); });
    el(g, 'line', { x1: X(x0), y1: Y(0), x2: X(x1), y2: Y(0), 'class': 'achse' });
    if (x0 <= 0 && x1 >= 0) el(g, 'line', { x1: X(0), y1: Y(y0), x2: X(0), y2: Y(y1), 'class': 'achse' });
    var pf = 6;
    el(g, 'polygon', { points: X(x1) + ',' + Y(0) + ' ' + (X(x1) - pf) + ',' + (Y(0) - pf / 2) + ' ' + (X(x1) - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
    if (x0 <= 0 && x1 >= 0) el(g, 'polygon', { points: X(0) + ',' + Y(y1) + ' ' + (X(0) - pf / 2) + ',' + (Y(y1) + pf) + ' ' + (X(0) + pf / 2) + ',' + (Y(y1) + pf), 'class': 'pfeil' });
    var ebene = el(svg, 'g', {});
    // Achsenzahlen über der Kurve, mit Hof: Die Sinuskurve geht genau durch −180°, 180°, … (Prüfung 08.10.2026)
    var zahlen = el(svg, 'g', {}), mk = o.marken || schritt * 2;
    for (x = Math.ceil(x0 / mk) * mk; x <= x1 - mk / 3; x += mk) if (x !== 0 && x > x0 + mk / 4) el(zahlen, 'text', { x: X(x), y: Y(0) + 11, 'text-anchor': 'middle', 'class': 'skala' }, (x < 0 ? '−' : '') + Math.abs(x) + '°');
    [[1, '1'], [-1, '−1']].forEach(function(t){ if (t[0] > y0 && t[0] < y1 && x0 <= 0) el(zahlen, 'text', { x: X(0) - 3, y: Y(t[0]) + 3, 'text-anchor': 'end', 'class': 'skala' }, t[1]); });
    el(svg, 'text', { x: W - 2, y: Y(0) - 6, 'text-anchor': 'end', 'class': 'achsname' }, 'φ');
    if (x0 <= 0 && x1 >= 0) el(svg, 'text', { x: X(0) + 6, y: Y(y1) + 9, 'text-anchor': 'start', 'class': 'achsname' }, 'y');
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      /* Kurve y = f(φ); beim Tangens an den Polstellen unterbrochen und senkrecht abgeschnitten. */
      kurve: function(f, cls){
        var d = '', neu = true;
        for (var k = 0; k <= 720; k++){
          var p = x0 + (x1 - x0) * k / 720, y = f === 'sin' ? sinG(p) : f === 'cos' ? cosG(p) : tanG(p);
          if (f === 'tan'){ var m = ((p - 90) % 180 + 180) % 180; if (m < 0.8 || m > 179.2 || isNaN(y)){ neu = true; continue; } }
          if (y > y1 + 0.6 || y < y0 - 0.6){ neu = true; continue; }
          y = Math.max(y0 - 0.05, Math.min(y1 + 0.05, y));
          d += (neu ? 'M' : 'L') + X(p).toFixed(1) + ' ' + Y(y).toFixed(1); neu = false;
        }
        var e = el(ebene, 'path', { d: d, 'class': cls });
        return e;
      },
      pole: function(){ for (var p = Math.ceil((x0 - 90) / 180) * 180 + 90; p <= x1; p += 180) el(ebene, 'line', { x1: X(p), y1: Y(y0), x2: X(p), y2: Y(y1), 'class': 'pol' }); },
      waagrechte: function(c, name){ if (c >= y0 && c <= y1){ el(ebene, 'line', { x1: X(x0), y1: Y(c), x2: X(x1), y2: Y(c), 'class': 'waagrechte' });
        if (name) el(zahlen, 'text', { x: X(x1) - 2, y: Y(c) + (c < 0 ? 11 : -4), 'text-anchor': 'end', 'class': 'skala' }, name); } },
      band: function(a, b, cls){ el(ebene, 'rect', { x: X(Math.max(a, x0)), y: Y(y1), width: Math.max(0, X(Math.min(b, x1)) - X(Math.max(a, x0))), height: Y(y0) - Y(y1), 'class': cls }); },
      punkt: function(x, y, cls, text, oben, dx){
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx || 0), y: Y(y) + (oben === false ? 14 : -7), 'text-anchor': 'middle', 'class': 'p-text ' + cls }, text);
      }
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
      var v = +r[k].value, e = r[k].dataset.einheit || '', st = +r[k].step;
      w[k] = v;
      r[k].parentNode.querySelector('.sl-val').textContent = (v < 0 ? '−' : '') + (st < 1 ? Math.abs(v).toFixed(st < 0.1 ? 2 : (st === 0.5 ? 1 : 1)) : String(Math.abs(v))) + e;
    }
    return w;
  }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function wahlWert(fig, name){ var e = fig.querySelector('input[name="' + name + '"]:checked'); return e ? e.value : null; }
  function wahlSetzen(fig, name, w){ fig.querySelectorAll('input[name="' + name + '"]').forEach(function(rb){ rb.checked = rb.value === w; }); }
  /* Regler setzen und sperren (Aufgaben mit fester Gleichung); beim Wechsel wieder frei. */
  function setze(r, p, v){ r[p].value = v; }
  function sperre(r, p, an){ r[p].disabled = !!an; r[p].closest('.sl-grp').classList.toggle('gesperrt', !!an); }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ----------
     Beim Wechsel gehen Regler und Auswahlknöpfe auf ihren Startwert zurück und alle Sperren auf,
     damit der Endzustand der vorigen Aufgabe die nächste nicht schon löst (HOWTO §15). */
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
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; inp.disabled = false; var g = inp.closest('.sl-grp'); if (g) g.classList.remove('gesperrt'); });
      fig.querySelectorAll('input[type=radio]').forEach(function(inp){ inp.checked = inp.defaultChecked; inp.disabled = false; });
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
  /* Merk-Objekte werden geleert, nie neu zugewiesen (Prüfung Trigonometrie 05.10.2026, H1). */
  function leeren(o){ for (var k in o) delete o[k]; }

  /* ---------- Kapitel 1: die Gleichung am Einheitskreis ----------
     Unterschied zur Animation «Gleichung am Einheitskreis» der Themenseite (#visualisierung): dort
     stehen die Lösungswinkel und die allgemeine Lösung schon als Zahl da. Hier nur Kreis, Gerade und
     Schnittpunkte — die Winkel liest man selbst ab; der Tangens kommt erst in Kapitel 3. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.65, x1: 1.65, y0: -1.65, y1: 1.65 });
    var pruefen = function(){}, spur = { min: 0.5, max: 0.5, an: false }, ziel = null;
    var inp = fig.querySelector('input[data-p="c"]');
    // vor regler() registriert: Der Spurenzähler steht, bevor gezeichnet und geprüft wird (HOWTO §15)
    inp.addEventListener('input', function(){ var v = +inp.value; spur.an = true; spur.min = Math.min(spur.min, v); spur.max = Math.max(spur.max, v); });
    var r = regler(fig, zeichnen);
    r.c.addEventListener('input', function(){ pruefen(); });
    fig.querySelectorAll('input[name="s1-fn"]').forEach(function(rb){ rb.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), f = wahlWert(fig, 's1-fn') || 'sin', c = Math.round(w.c * 100) / 100;
      return { f: f, c: c, n: loesungen(f, c).length, ganz: spur.an && spur.min <= -1.2 && spur.max >= 1.2 }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ spur.min = spur.max = 0.5; spur.an = false; ziel = null; } };
    function zeichnen(){
      var st = zust(), f = st.f, c = st.c;
      K.leeren();
      if (ziel) ziel.forEach(function(g){ K.punkt(cosG(g), sinG(g), 'p-ziel'); });
      if (f === 'sin') K.strecke(K.x0, c, K.x1, c, 'waagrechte');
      else K.strecke(c, K.y0, c, K.y1, 'waagrechte');
      loesungen(f, c).forEach(function(g){
        var x = cosG(g), y = sinG(g);
        K.strecke(0, 0, x, y, 'radius');
        if (f === 'sin' && Math.abs(y) > 1e-9) K.strecke(x, 0, x, y, 'koord blau');
        if (f === 'cos' && Math.abs(x) > 1e-9) K.strecke(0, 0, x, 0, 'koord gruen');
        K.punkt(x, y, 'p-lauf ' + FARBE[f]);
      });
      var gl = f === 'sin' ? 'Waagrechte y = ' + z(c) : 'Senkrechte x = ' + z(c);
      rolle(fig, 'formel').innerHTML = sp('tx-' + FARBE[f], f + ' φ = ' + z(c)) + '; &nbsp;' + gl + '; &nbsp;Schnittpunkte mit dem Kreis: ' + st.n;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh \\(c\\) ganz nach unten und ganz nach oben. Wann trifft die Gerade den Kreis?', ok: function(s){ return s.ganz; } },
      // Startzustand: Sinus, c = 0.5 (wie im Clip) — keine Aufgabe ist schon gelöst.
      { text: 'Sinus: Stell \\(c\\) so ein, dass es genau <b>eine</b> Lösung gibt.', ok: function(s){ return s.f === 'sin' && Math.abs(Math.abs(s.c) - 1) < 1e-9; } },
      { text: 'Sinus: Stell \\(c\\) so ein, dass die Lösungen bei \\(210^\\circ\\) und \\(330^\\circ\\) liegen.', ok: function(s){ return s.f === 'sin' && Math.abs(s.c + 0.5) < 1e-9; } },
      { text: 'Schalte auf Cosinus. Stell \\(c\\) so ein, dass die Lösungen bei \\(90^\\circ\\) und \\(270^\\circ\\) liegen.', ok: function(s){ return s.f === 'cos' && Math.abs(s.c) < 1e-9; } },
      { text: 'Cosinus: Stell \\(c\\) so ein, dass die Gleichung <b>keine</b> Lösung hat.', ok: function(s){ return s.f === 'cos' && s.n === 0; } },
      // Zielspiel: 72.5° und 287.5° — nur cos φ = 0.3 trifft beide (sin φ = c hat nie zwei Lösungen gleicher x-Koordinate).
      // Nicht cos φ = 0.5: Der Startwert ist c = 0.5, ein Klick auf «cos» hätte die Aufgabe gelöst (Prüfung 08.10.2026, M1).
      { text: 'Triff die beiden grau markierten Punkte: Wähle Sinus oder Cosinus und \\(c\\).', setup: function(){ ziel = [72.5424, 287.4576]; }, ok: function(s){ return s.f === 'cos' && Math.abs(s.c - 0.3) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: der Rechner und die zweite Lösung ----------
     Unterschied zur gekoppelten Animation der Themenseite (#anim-kopplung): dort stehen beide
     Lösungen als Zahl da. Hier zeigt die Live-Zeile nur den Wert des Rechners (Hauptwert, sein
     Bereich als Band); den zweiten Punkt erreicht man, indem man P selbst dorthin dreht. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var K = Kreisbild(fig.querySelector('svg'), { w: 320, x0: -1.45, x1: 1.45, y0: -1.45, y1: 1.45 });
    var pruefen = function(){}, spur = { min: 0.4, max: 0.4 };
    var inp = fig.querySelector('input[data-p="c"]');
    inp.addEventListener('input', function(){ var v = +inp.value; spur.min = Math.min(spur.min, v); spur.max = Math.max(spur.max, v); });
    var r = regler(fig, zeichnen);
    r.c.addEventListener('input', function(){ pruefen(); });
    fig.querySelectorAll('input[name="s2-fn"]').forEach(function(rb){ rb.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), f = wahlWert(fig, 's2-fn') || 'sin', c = Math.round(w.c * 100) / 100;
      return { f: f, c: c, phi: w.phi, l: loesungen(f, c), h: hauptwert(f, c), beide: spur.min < 0 && spur.max > 0 }; }
    var sim = { zustand: zust, zeichnen: zeichnen,
      setze: function(f, c){ wahlSetzen(fig, 's2-fn', f); setze(r, 'c', c); sperre(r, 'c', true); fig.querySelectorAll('input[name="s2-fn"]').forEach(function(rb){ rb.disabled = true; }); },
      aufraeumen: function(){ spur.min = spur.max = 0.4; } };
    function zeichnen(){
      var st = zust(), f = st.f, c = st.c, h = st.h;
      K.leeren();
      if (f === 'cos') K.bogen(1, 0, 180, 'band gruen'); else K.bogen(1, -90, 90, 'band blau');
      if (f === 'sin') K.strecke(-1.45, c, 1.45, c, 'waagrechte'); else K.strecke(c, -1.45, c, 1.45, 'waagrechte');
      // der zweite Kreispunkt mit demselben Wert: hohl, ohne Zahl
      var x2 = f === 'sin' ? -cosG(h) : cosG(h), y2 = f === 'sin' ? sinG(h) : -sinG(h);
      if (Math.abs(x2 - cosG(h)) > 1e-6 || Math.abs(y2 - sinG(h)) > 1e-6) K.punkt(x2, y2, 'p-hohl');
      K.bogen(0.22, 0, h, 'winkelbogen');
      K.strecke(0, 0, cosG(h), sinG(h), 'radius');
      kreisPunkt(K, h, 'p-lauf ' + FARBE[f], 'φ₁');
      // der Probepunkt P zum eingestellten Winkel
      K.strecke(0, 0, cosG(st.phi), sinG(st.phi), 'radius gestr');
      kreisPunkt(K, st.phi, 'p-pkt', 'P');
      var name = f + '⁻¹(' + z(c) + ')';
      rolle(fig, 'formel').innerHTML = sp('tx-' + FARBE[f], f + ' φ = ' + z(c)) + '; &nbsp;Rechner: ' + name + ' ' + ungefaehr(h) + grad1(h)
        + '<br>P: φ = ' + st.phi + '°';
      pruefen();
    }
    /* Regler «Winkel von P» in ganzen Grad, Toleranz 1° gegen den ungerundeten Zielwinkel: Je zwei Reglerwerte
       treffen (143.13 → 143 und 144). Mit Schritt 0.5 und Toleranz 0.3 traf nur einer, und der war mit Maus oder
       Finger oft nicht erreichbar (Prüfung 08.10.2026, H1). Der Regler steht dafür über die ganze Breite. */
    var TOL = 1;
    function trifft(s, f, c, g){ return s.f === f && Math.abs(s.c - c) < 1e-9 && Math.abs(s.phi - g) <= TOL; }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh \\(c\\) von negativen zu positiven Werten. Wo liegt der Punkt des Rechners — und wo der zweite?', ok: function(s){ return s.beide; } },
      // Startzustand: Sinus, c = 0.4 (wie im Clip), P bei 0° — keine Aufgabe ist schon gelöst.
      // Zielwinkel (scripts/lp/trigonometrische-gleichungen/zahlen.py): 143.13; 194.48; 345.52; 249.51; 323.13 —
      // je zwei ganze Grad innerhalb der Toleranz 1°, keiner davon im Ziel einer anderen Aufgabe.
      { text: 'Sinus, \\(c = 0.6\\): Dreh \\(P\\) auf die zweite Lösung.', setup: function(s){ s.setze('sin', 0.6); }, ok: function(s){ return trifft(s, 'sin', 0.6, 143.13); } },
      { text: 'Sinus, \\(c = -0.25\\): Dreh \\(P\\) auf die Lösung im dritten Quadranten.', setup: function(s){ s.setze('sin', -0.25); }, ok: function(s){ return trifft(s, 'sin', -0.25, 194.48); } },
      { text: 'Sinus, \\(c = -0.25\\): Dreh \\(P\\) auf die Lösung im vierten Quadranten — zwischen \\(0^\\circ\\) und \\(360^\\circ\\).', setup: function(s){ s.setze('sin', -0.25); }, ok: function(s){ return trifft(s, 'sin', -0.25, 345.52); } },
      { text: 'Cosinus, \\(c = -0.35\\): Dreh \\(P\\) auf die Lösung, die der Rechner nicht liefert.', setup: function(s){ s.setze('cos', -0.35); }, ok: function(s){ return trifft(s, 'cos', -0.35, 249.51); } },
      { text: 'Cosinus, \\(c = 0.8\\): Dreh \\(P\\) auf die zweite Lösung.', setup: function(s){ s.setze('cos', 0.8); }, ok: function(s){ return trifft(s, 'cos', 0.8, 323.13); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Tangensgleichungen ----------
     Unterschied zur Animation der Themenseite (#visualisierung, Reiter tan): dort nennt die Live-Zeile
     beide Lösungen. Hier sieht man S(1 | c), die Gerade durch O und S und den Wert des Rechners; die
     zweite Lösung holt man mit P — sie liegt dem Rechnerpunkt am Ursprung gegenüber. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    // Fenster ±2.6 bei c bis ±2.4: S und seine Beschriftung bleiben ganz im Bild (Prüfung 08.10.2026).
    var K = Kreisbild(fig.querySelector('svg'), { w: 290, x0: -1.35, x1: 1.75, y0: -2.6, y1: 2.6, ymarken: [[1, '1'], [-1, '−1'], [2, '2'], [-2, '−2']] });
    var pruefen = function(){}, spur = { min: 1, max: 1 };
    var inp = fig.querySelector('input[data-p="c"]');
    inp.addEventListener('input', function(){ var v = +inp.value; spur.min = Math.min(spur.min, v); spur.max = Math.max(spur.max, v); });
    var r = regler(fig, zeichnen);
    r.c.addEventListener('input', function(){ pruefen(); });
    function zust(){ var w = werte(r), c = Math.round(w.c * 10) / 10;
      return { c: c, phi: w.phi, h: hauptwert('tan', c), ganz: spur.min <= -2.3 && spur.max >= 2.3 }; }
    var sim = { zustand: zust, zeichnen: zeichnen,
      setze: function(c){ setze(r, 'c', c); sperre(r, 'c', true); },
      aufraeumen: function(){ spur.min = spur.max = 1; } };
    function zeichnen(){
      var st = zust(), c = st.c, h = st.h;
      K.leeren();
      K.strecke(1, K.y0, 1, K.y1, 'tangente');
      K.gerade(-1, -c, 1, c, 'strahl');
      K.strecke(1, 0, 1, c, 'koord orange');
      K.punkt(1, c, 'p-lauf orange', 'S', 7, c >= 0 ? -6 : 14);
      K.punkt(-cosG(h), -sinG(h), 'p-hohl');
      K.bogen(0.22, 0, h, 'winkelbogen');
      K.strecke(0, 0, cosG(h), sinG(h), 'radius');
      K.punkt(cosG(h), sinG(h), 'p-lauf orange', 'φ₁', -7, sinG(h) >= 0 ? -7 : 15, 'end');
      K.strecke(0, 0, cosG(st.phi), sinG(st.phi), 'radius gestr');
      kreisPunkt(K, st.phi, 'p-pkt', 'P');
      rolle(fig, 'formel').innerHTML = sp('tx-orange', 'tan φ = ' + z(c)) + '; &nbsp;S(1 | ' + z(c) + '); &nbsp;Rechner: tan⁻¹(' + z(c) + ') ' + ungefaehr(h) + grad1(h)
        + '<br>P: φ = ' + st.phi + '°';
      pruefen();
    }
    function trifft(s, c, g){ return Math.abs(s.c - c) < 1e-9 && Math.abs(s.phi - g) <= 1; }   // wie Sim 2: ganze Grad, Toleranz 1°
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh \\(c\\) ganz nach oben und ganz nach unten. Trifft die Gerade durch \\(O\\) und \\(S\\) den Kreis immer?', ok: function(s){ return s.ganz; } },
      // Startzustand: c = 1 (wie im Clip), P bei 0° — keine Aufgabe ist schon gelöst.
      // Ziele (zahlen.py): 206.57; 123.69; 303.69 — je zwei ganze Grad innerhalb der Toleranz 1°.
      { text: '\\(c = 0.5\\): Dreh \\(P\\) auf die zweite Lösung.', setup: function(s){ s.setze(0.5); }, ok: function(s){ return trifft(s, 0.5, 206.57); } },
      { text: '\\(c = -1.5\\): Dreh \\(P\\) auf die Lösung im zweiten Quadranten.', setup: function(s){ s.setze(-1.5); }, ok: function(s){ return trifft(s, -1.5, 123.69); } },
      { text: '\\(c = -1.5\\): Dreh \\(P\\) auf die Lösung im vierten Quadranten.', setup: function(s){ s.setze(-1.5); }, ok: function(s){ return trifft(s, -1.5, 303.69); } },
      { text: 'Stell \\(c\\) so ein, dass beide Lösungen auf der \\(x\\)-Achse liegen.', ok: function(s){ return Math.abs(s.c) < 1e-9; } },
      // c = 2: 243.43° → 243°; die Nachbarn c = 1.9 und 2.1 geben 242.24° und 244.54° (zahlen.py).
      { text: 'Stell \\(c\\) so ein, dass eine Lösung, auf ganze Grad gerundet, bei \\(243^\\circ\\) liegt.', ok: function(s){ return Math.abs(s.c - 2) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: alle Lösungen an der Kurve ----------
     Unterschied zur Animation «sin-, cos- und tan-Kurve mit Lösungen» der Themenseite (#anim-kurven):
     dort alle Schnittpunkte zwischen 0° und 720° auf einmal. Hier ein Regler k: Er schiebt das
     markierte Paar (beim Tangens den einen Punkt) um k Perioden — so wird «+ k · 360°» sichtbar. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Kurvenbild(fig.querySelector('svg'), { w: 640, h: 230, x0: -360, x1: 720, y0: -1.7, y1: 1.7, schritt: 90, marken: 180 });
    var pruefen = function(){}, ks = {};
    var inp = fig.querySelector('input[data-p="k"]');
    inp.addEventListener('input', function(){ ks[+inp.value] = true; });
    var r = regler(fig, zeichnen);
    r.k.addEventListener('input', function(){ pruefen(); });
    fig.querySelectorAll('input[name="s4-fn"]').forEach(function(rb){ rb.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), f = wahlWert(fig, 's4-fn') || 'sin', c = Math.round(w.c * 100) / 100, k = w.k;
      var g = loesungen(f, c), p = f === 'tan' ? 180 : 360, m;
      if (f === 'tan'){ var t = hauptwert('tan', c); g = [t]; }
      m = g.map(function(x){ return x + k * p; });
      return { f: f, c: c, k: k, p: p, g: g, m: m, ks: ks }; }
    var sim = { zustand: zust, zeichnen: zeichnen,
      setze: function(f, c){ wahlSetzen(fig, 's4-fn', f); setze(r, 'c', c); sperre(r, 'c', true); fig.querySelectorAll('input[name="s4-fn"]').forEach(function(rb){ rb.disabled = true; }); },
      aufraeumen: function(){ leeren(ks); } };
    function zeichnen(){
      var st = zust(), f = st.f, c = st.c;
      K.leeren();
      if (f === 'tan') K.pole();
      K.kurve(f, 'kurve ' + FARBE[f]);
      K.waagrechte(c);
      // alle Lösungen im Bild hohl, das Paar zu k gefüllt und beschriftet
      for (var kk = -4; kk <= 6; kk++) st.g.forEach(function(x){ var v = x + kk * st.p; if (v >= -360 - 1e-9 && v <= 720 + 1e-9 && kk !== st.k) K.punkt(v, c, 'p-hohl'); });
      // Liegt das Paar näher als 56 Einheiten (Beschriftung «143.1°» ≈ 38 breit, mit Hof), rücken die
      // Beschriftungen gleichmässig auseinander (cos φ = −0.8: 143.1° und 216.9° sind 43 auseinander; Prüfung 08.10.2026).
      var sicht = st.m.filter(function(v){ return v >= -360 - 1e-9 && v <= 720 + 1e-9; }).sort(function(a, b){ return a - b; });
      var luecke = sicht.length === 2 ? K.X(sicht[1]) - K.X(sicht[0]) : 99, weg = luecke < 56 ? (56 - luecke) / 2 : 0;
      sicht.forEach(function(v, i){ K.punkt(v, c, 'p-lauf ' + FARBE[f], grad1(v), c < 1.2, i === 0 ? -weg : weg); });
      var zeile;
      if (!st.g.length) zeile = sp('tx-' + FARBE[f], f + ' φ = ' + z(c)) + '; &nbsp;<b>keine Lösung</b>';
      else {
        // gerundete Winkel mit «≈» (HOWTO §15, Live-Anzeigen)
        var fam = st.g.map(function(x){ return 'φ ' + ungefaehr(x) + grad1(x) + ' + k · ' + st.p + '°'; }).join(' oder ');
        zeile = sp('tx-' + FARBE[f], f + ' φ = ' + z(c)) + ': &nbsp;' + fam + '<br>k = ' + st.k + ': &nbsp;' + st.m.map(function(v){ return ungefaehr(v).replace('= ', '') + grad1(v); }).join('; ');
      }
      rolle(fig, 'formel').innerHTML = zeile;
      folgen(st.m);
      pruefen();
    }
    /* Auf dem Handy ist das Bild breiter als sein Rahmen (min. 560 px): Der Rahmen folgt den markierten
       Lösungen, sonst lägen die Aufgaben in [360°; 720°[ im verdeckten Teil (Prüfung 08.10.2026, M4). */
    var rahmen = fig.querySelector('.kurven-rahmen'), bild = fig.querySelector('.kurven-rahmen > svg');
    function folgen(m){
      if (!rahmen || !bild || rahmen.scrollWidth <= rahmen.clientWidth + 1) return;
      var drin = m.filter(function(v){ return v >= -360 && v <= 720; }); if (!drin.length) return;
      var mitte = (K.X(Math.min.apply(null, drin)) + K.X(Math.max.apply(null, drin))) / 2 * bild.clientWidth / 640;
      rahmen.scrollLeft = Math.max(0, mitte - rahmen.clientWidth / 2);
    }
    function alle(s, a, b){ return s.m.length && s.m.every(function(v){ return v >= a - 1e-9 && v < b - 1e-9; }); }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Zieh \\(k\\) einmal ganz durch. Um wie viel springen die markierten Lösungen?', ok: function(s){ return s.ks[-2] && s.ks[3]; } },
      // Startzustand: Sinus, c = 0.5, k = 0 (Beispiel des Clips) — keine Aufgabe ist schon gelöst.
      { text: 'Cosinus, \\(c = -0.8\\): Stell \\(k\\) so ein, dass beide markierten Lösungen im Intervall \\([360^\\circ;\\, 720^\\circ[\\) liegen.', setup: function(s){ s.setze('cos', -0.8); }, ok: function(s){ return s.f === 'cos' && Math.abs(s.c + 0.8) < 1e-9 && alle(s, 360, 720); } },
      { text: 'Cosinus, \\(c = -0.8\\): Stell \\(k\\) so ein, dass beide markierten Lösungen im Intervall \\([-360^\\circ;\\, 0^\\circ[\\) liegen.', setup: function(s){ s.setze('cos', -0.8); }, ok: function(s){ return s.f === 'cos' && Math.abs(s.c + 0.8) < 1e-9 && alle(s, -360, 0); } },
      { text: 'Tangens, \\(c = -0.7\\): Stell \\(k\\) so ein, dass die markierte Lösung zwischen \\(0^\\circ\\) und \\(180^\\circ\\) liegt.', setup: function(s){ s.setze('tan', -0.7); }, ok: function(s){ return s.f === 'tan' && Math.abs(s.c + 0.7) < 1e-9 && alle(s, 0, 180); } },
      { text: 'Tangens, \\(c = -0.7\\): Stell \\(k\\) so ein, dass die markierte Lösung zwischen \\(360^\\circ\\) und \\(540^\\circ\\) liegt.', setup: function(s){ s.setze('tan', -0.7); }, ok: function(s){ return s.f === 'tan' && Math.abs(s.c + 0.7) < 1e-9 && alle(s, 360, 540); } },
      { text: 'Sinus: Stell \\(c\\) so ein, dass es je Periode nur <b>eine</b> Lösung gibt.', ok: function(s){ return s.f === 'sin' && Math.abs(Math.abs(s.c) - 1) < 1e-9; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kreis- und Kurvenbilder zu den Aufgaben ----------
     <svg class="ek-mini" data-ek='{…}'>: p Winkel der Punkte, namen, h Waagrechte y = h,
     v Senkrechte x = v, tan c: Tangente x = 1 mit S(1 | c) und Gerade durch O, fenster [x0, x1, y0, y1].
     <svg class="kv-mini" data-kv='{…}'>: f, c, von, bis, punkte [[φ, Text]]. */
  document.querySelectorAll('svg.ek-mini[data-ek]').forEach(function(svg){
    var d = JSON.parse(svg.dataset.ek), fe = d.fenster || [-1.4, 1.4, -1.4, 1.4];
    var K = Kreisbild(svg, { w: d.breite || 200, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3.5, pfeil: 6, klein: true, ymarken: d.ymarken });
    if (d.tan != null){ K.strecke(1, fe[2], 1, fe[3], 'tangente'); K.gerade(-1, -d.tan, 1, d.tan, 'strahl'); K.strecke(1, 0, 1, d.tan, 'koord orange'); K.punkt(1, d.tan, 'p-lauf orange', 'S', 5, d.tan >= 0 ? -5 : 12); }
    if (d.h != null) K.strecke(fe[0], d.h, fe[1], d.h, 'waagrechte');
    if (d.v != null) K.strecke(d.v, fe[2], d.v, fe[3], 'waagrechte');
    (d.p || []).forEach(function(g, i){
      var c = cosG(g), s = sinG(g);
      K.strecke(0, 0, c, s, 'radius');
      // lagen: [dx, dy, Anker] je Name, wo die radiale Lage mit S zusammenstösst (Lösung 3d)
      var lg = (d.lagen || [])[i] || [c >= 0 ? 5 : -5, s >= 0 ? -5 : 12, c >= 0 ? 'start' : 'end'];
      K.punkt(c, s, 'p-lauf ' + (d.farbe || 'blau'), (d.namen || [])[i] || '', lg[0], lg[1], lg[2]);
    });
    svg.setAttribute('role', 'img');
  });
  document.querySelectorAll('svg.kv-mini[data-kv]').forEach(function(svg){
    var d = JSON.parse(svg.dataset.kv);
    var K = Kurvenbild(svg, { w: d.breite || 420, h: d.hoehe || 150, x0: d.von, x1: d.bis, y0: d.y0 || -1.4, y1: d.y1 || 1.4, schritt: 90, marken: d.marken || 180, r: 3.5 });
    if (d.f === 'tan') K.pole();
    K.kurve(d.f, 'kurve ' + FARBE[d.f]);
    K.waagrechte(d.c, 'y = ' + z(d.c));
    (d.punkte || []).forEach(function(p, i){ K.punkt(p[0], d.c, 'p-lauf ' + FARBE[d.f], p[1], i % 2 === 0); });   // abwechselnd über und unter der Geraden
    svg.setAttribute('role', 'img');
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    function r1(v){ var r = Math.round(v * 10) / 10; return Object.is(r, -0) ? 0 : r; }
    /* Eingaben: Zahl, Dezimalkomma; ein angehängtes ° wird überlesen. */
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/°$/, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
    }
    /* Liste von Winkeln: «30; 150; 390» (auch mit ° oder Leerzeichen). Dezimalkomma nur ohne Strichpunkt. */
    function liste(s){
      s = String(s).replace(/\u2212/g, '-').replace(/°/g, ' ').trim();
      if (!s) return null;
      var teile = s.indexOf(';') >= 0 ? s.split(';') : s.split(/\s+/);
      var l = teile.map(function(t){ t = t.trim().replace(',', '.'); return /^-?(\d+(\.\d+)?|\.\d+)$/.test(t) ? parseFloat(t) : NaN; }).filter(function(v, i){ return !(isNaN(v) && teile[i].trim() === ''); });
      return l.some(isNaN) ? NaN : l;
    }
    var gl = function(a, b, t){ return Math.abs(a - b) <= (t || 1e-6); };
    /* Zwei Eingaben gegen zwei Sollwerte, Reihenfolge egal. */
    function paar(e, a, b, t){ return (gl(e.a, a, t) && gl(e.b, b, t)) || (gl(e.a, b, t) && gl(e.b, a, t)); }
    function pz(l){ return { a: String(l[0]), b: String(l[1]) }; }

    /* Exakte Werte: Text ↔ Zahl ↔ LaTeX */
    var EX = { '0': 0, '1/2': 0.5, '√2/2': Math.SQRT2 / 2, '√3/2': Math.sqrt(3) / 2, '1': 1, '√3/3': Math.sqrt(3) / 3, '√3': Math.sqrt(3) };
    function exZahl(t){ var neg = t.charAt(0) === '−'; return (neg ? -1 : 1) * EX[neg ? t.slice(1) : t]; }
    function exTex(t){ var neg = t.charAt(0) === '−', b = neg ? t.slice(1) : t;
      return (neg ? '-' : '') + ({ '1/2': '\\tfrac{1}{2}', '√2/2': '\\tfrac{\\sqrt{2}}{2}', '√3/2': '\\tfrac{\\sqrt{3}}{2}', '√3/3': '\\tfrac{\\sqrt{3}}{3}', '√3': '\\sqrt{3}' }[b] || b); }
    function gegen(t){ return t === '0' ? t : (t.charAt(0) === '−' ? t.slice(1) : '−' + t); }
    var IV = { '0': ['0^\\circ', '360^\\circ', 0, 360], 'm': ['-180^\\circ', '180^\\circ', -180, 180] };
    function ivTex(i){ return '[' + IV[i][0] + ';\\, ' + IV[i][1] + '[' ; }
    /* Lösungen im Intervall [lo; hi[ aus den Lösungen in [0°; 360°[ */
    function imIntervall(l, p, lo, hi){ var aus = []; l.forEach(function(x){ for (var k = -4; k <= 4; k++){ var v = x + k * p; if (v >= lo - 1e-9 && v < hi - 1e-9) aus.push(v); } });
      aus.sort(function(a, b){ return a - b; }); return aus.filter(function(v, i){ return i === 0 || !gl(v, aus[i - 1]); }); }
    function lsg(f, c, iv){ var l = loesungen(f, c); return imIntervall(l, f === 'tan' ? 180 : 360, IV[iv][2], IV[iv][3]); }
    function ftex(f){ return '\\' + f + '\\varphi'; }
    function gtex(g){ return tz(Math.round(g * 1000) / 1000) + '^\\circ'; }
    /* Winkel für Lösungstexte: gerundet mit «≈» (\\approx 14.5^\\circ), exakte ohne (90^\\circ) */
    function naeh(g){ var r = r1(g); return (Math.abs(g - r) > 1e-9 ? '\\approx ' : '') + tz(r) + '^\\circ'; }
    function mtex(l){ return l.length ? '\\{' + l.map(gtex).join(';\\ ') + '\\}' : '\\{\\,\\}'; }

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15), je Typ ein Schlüssel.
       Quellen: Clips g5-5-lp-* · Aufgaben der Kapitel · Vortest · Gesamttest
       (downloads/leitprogramme/trigonometrische-gleichungen/gesamttest.tex).
       Ausnahme (Prüfung 08.10.2026, M2/M3): In «anzahl», «spezial» und «tan-spezial» sind die vorgerechneten
       Beispiele der Einführungsclips frei (sin φ = 1; sin φ = 1/2, cos φ = −1/2; tan φ = ±1). Sonst fegte die
       Liste den Wurfraum leer: «anzahl» würfelte nie eine einzige Lösung, «spezial» nie einen positiven
       Sinuswert, «tan-spezial» nur zwei Gleichungen. Gesperrt bleiben Kontrollfragen, Aufgaben, Vortest, Gesamttest. */
    var SPERRE = [
      // anzahl: Clip 1 (sin > 1), Kontrollclip 1 (cos −1, sin 1.4), Aufgaben 1d, 1e und 4d (cos 1), Gesamttest G2 (sin −1.2)
      'an|sin|1.4', 'an|cos|-1', 'an|sin|-1', 'an|cos|1.01', 'an|sin|0', 'an|cos|-0.999', 'an|sin|-1.2', 'an|cos|1',
      // spezial (Intervall [0°; 360°[): Kontrollclip 1 (sin √2/2), Aufgabe 1c, Gesamttest G1, G3
      'sp|sin|√2/2|0', 'sp|sin|√3/2|0', 'sp|cos|0|0', 'sp|cos|−√2/2|0', 'sp|cos|√3/2|0', 'sp|cos|√2/2|0',
      // quadranten: Aufgaben 1a, 1b
      'qu|sin|0.8', 'qu|cos|-0.3',
      // zweite: Clip 2 (sin 0.4, cos −0.7, sin −0.4), Kontrollclip 2 (sin 0.9, cos −0.45, sin −0.6, cos 0.25),
      // Aufgaben 2a–2d, Vortest (sin 0.6, cos −0.3), Gesamttest G4, G7
      'zw|sin|0.4', 'zw|cos|-0.7', 'zw|sin|-0.4', 'zw|sin|0.9', 'zw|cos|-0.45', 'zw|sin|-0.6', 'zw|cos|0.25',
      'zw|sin|0.7', 'zw|cos|-0.2', 'zw|sin|-0.45', 'zw|sin|0.3', 'zw|sin|0.6', 'zw|cos|-0.3', 'zw|sin|-0.35', 'zw|cos|-0.6', 'zw|cos|0.42',
      // tan-loesen: Clip 3 (2.5), Kontrollclip 3 (0.6, −5, −0.6), Aufgaben 3a, 3b, 3d, Gesamttest G6
      'tl|2.5', 'tl|0.6', 'tl|-5', 'tl|-0.6', 'tl|1.2', 'tl|-3.2', 'tl|-0.5', 'tl|-2.4',
      // tan-spezial ([0°; 360°[): Aufgabe 3c (√3/3, 0), Gesamttest G3 (−√3)
      'ts|√3/3|0', 'ts|0|0', 'ts|−√3|0',
      // allgemein: Clip 4 (sin 1/2, tan 1), Kontrollclip 4 (cos 1/2, tan −1, sin √3/2), Gesamttest G3 (tan −√3, cos √2/2)
      'al|sin|1/2', 'al|tan|1', 'al|cos|1/2', 'al|tan|−1', 'al|sin|√3/2', 'al|tan|−√3', 'al|cos|√2/2',
      // intervall: Clip 4 (30/150 in [0; 720[ und [−360; 0[), Kontrollclip 4 (210/330 in [360; 720[, 120/240 in [0; 720[)
      'iv|30|150|0|720', 'iv|30|150|-360|0', 'iv|210|330|360|720', 'iv|120|240|0|720'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    var TYPEN = {
      /* ── Kapitel 1: Anzahl der Lösungen ─────────────────────────── */
      'anzahl': { felder: ['n'], muster: 'Anzahl Lösungen in [0°; 360°[: {n:0|1|2}',
        schl: function(A){ return 'an|' + A.f + '|' + A.c; },
        eingabe: function(A){ return { n: String(A.n) }; },
        neu: function(){
          var f = zufall(['sin', 'cos']), c = zufall([-2, -1.4, -1.1, -1, -1, -0.8, -0.35, 0, 0.25, 0.65, 0.95, 1, 1, 1.05, 1.5]);
          return { f: f, c: c, n: loesungen(f, c).length,
            text: 'Wie viele Lösungen hat \\(' + ftex(f) + ' = ' + tz(c) + '\\) im Intervall \\([0^\\circ;\\, 360^\\circ[\\)? Entscheide am Einheitskreis.' }; },
        fehler: function(A){ var f = [];
          [0, 1, 2].forEach(function(w){ if (w === A.n) return;
            var stw = A.n === 0 ? 'zwischen' : A.n === 1 ? (w === 2 ? 'berührt' : 'liegt noch') : (A.c === 0 && w === 1 ? '180' : (w === 1 ? 'Wie oft' : 'trifft'));
            if (A.n === 2 && A.c === 0 && A.f === 'cos' && w === 1) stw = '270';
            f.push([{ n: String(w) }, stw]); });
          return f; },
        pruefen: function(A, e){
          var w = +e.n, g = A.f === 'sin' ? 'Waagrechte \\(y = ' + tz(A.c) + '\\)' : 'Senkrechte \\(x = ' + tz(A.c) + '\\)';
          if (w === A.n) return null;
          if (A.n === 0) return (A.f === 'sin' ? 'Der Sinus' : 'Der Cosinus') + ' liegt immer zwischen \\(-1\\) und \\(1\\). Die ' + g + ' verfehlt den Kreis.';
          if (A.n === 1 && w === 2) return 'Die ' + g + ' berührt den Kreis nur in einem Punkt' + (A.f === 'cos' && A.c === 1 ? ' — bei \\(0^\\circ\\); \\(360^\\circ\\) gehört nicht zum Intervall.' : '.');
          if (A.n === 1) return '\\(' + tz(A.c) + '\\) liegt noch auf dem Kreis: Die ' + g + ' berührt ihn.';
          if (A.c === 0 && w === 1) return A.f === 'sin' ? 'Die \\(x\\)-Achse trifft den Kreis rechts und links: bei \\(0^\\circ\\) und \\(180^\\circ\\).' : 'Die \\(y\\)-Achse trifft den Kreis oben und unten: bei \\(90^\\circ\\) und \\(270^\\circ\\).';
          if (w === 1) return 'Zeichne die ' + g + '. Wie oft schneidet sie den Kreis?';
          return '\\(' + tz(A.c) + '\\) liegt zwischen \\(-1\\) und \\(1\\): Die ' + g + ' trifft den Kreis.'; },
        loesung: function(A){ var l = loesungen(A.f, A.c); return ftex(A.f) + ' = ' + tz(A.c) + ':\\ ' + A.n + '\\ \\text{Lösung' + (A.n === 1 ? '' : 'en') + '}' + (A.n ? '\\ (' + l.map(naeh).join(';\\ ') + ')' : ''); } },

      /* ── Kapitel 1: besondere Werte, ohne Taschenrechner ──────────── */
      'spezial': { felder: ['a', 'b'], muster: 'Lösungen: {a} ° &nbsp;und&nbsp; {b} °',
        schl: function(A){ return 'sp|' + A.f + '|' + A.t + '|' + A.iv; },
        eingabe: function(A){ return pz(A.l); },
        neu: function(){
          // nur [0°; 360°[: andere Intervalle kommen erst in Kapitel 4 (Prüfung 08.10.2026, M3)
          var f = zufall(['sin', 'cos']), t = zufall(['0', '1/2', '−1/2', '√2/2', '−√2/2', '√3/2', '−√3/2']), iv = '0';
          return { f: f, t: t, iv: iv, l: lsg(f, exZahl(t), iv),
            text: 'Löse ohne Taschenrechner: \\(' + ftex(f) + ' = ' + exTex(t) + '\\) im Intervall \\(' + ivTex(iv) + '\\). Gib beide Lösungen in Grad an.' }; },
        kandidaten: function(A){
          // [Eingabe, Stichwort], in der Reihenfolge, in der pruefen() sie erkennt
          var c = exZahl(A.t), h = hauptwert(A.f, c), k = [], lo = IV[A.iv][2], hi = IV[A.iv][3];
          var falsch = A.f === 'sin' ? [h, 360 - h] : [h, 180 - h];
          k.push([imIntervall(falsch.map(mod360), 360, lo, hi), A.f === 'sin' ? 'Beim Sinus liegen' : 'Beim Cosinus haben']);
          k.push([lsg(A.f, -c, A.iv), 'Vorzeichen']);
          k.push([lsg(A.f === 'sin' ? 'cos' : 'sin', c, A.iv), A.f === 'sin' ? 'Höhe' : 'waagrechte']);
          if (A.iv === '0' && h < 0) k.push([[h, A.f === 'sin' ? 180 - h : -h].sort(function(a, b){ return a - b; }), 'Intervall']);
          if (A.iv === 'm') k.push([loesungen(A.f, c), 'Intervall']);
          return k.filter(function(x){ return x[0].length === 2; }); },
        fehler: function(A){ var T = this, aus = [], gesehen = [A.l.join('|')];
          T.kandidaten(A).forEach(function(x){ var s = x[0].join('|'); if (gesehen.indexOf(s) < 0){ gesehen.push(s); aus.push([pz(x[0]), x[1]]); } });
          return aus; },
        pruefen: function(A, e){
          if (paar(e, A.l[0], A.l[1])) return null;
          var c = exZahl(A.t), ks = this.kandidaten(A);
          for (var i = 0; i < ks.length; i++) if (paar(e, ks[i][0][0], ks[i][0][1])){
            var w = ks[i][1];
            if (w === 'Beim Sinus liegen') return 'Beim Sinus liegen beide Punkte auf derselben <b>Höhe</b>: Spiegelung an der \\(y\\)-Achse, \\(\\varphi_2 = 180^\\circ - \\varphi_1\\).';
            if (w === 'Beim Cosinus haben') return 'Beim Cosinus haben beide Punkte dieselbe \\(x\\)-Koordinate: Spiegelung an der \\(x\\)-Achse, \\(\\varphi_2 = 360^\\circ - \\varphi_1\\).';
            if (w === 'Vorzeichen') return 'Das sind die Lösungen für \\(' + exTex(gegen(A.t)) + '\\). Vorzeichen: Liegen die Punkte ' + (A.f === 'sin' ? 'über oder unter der \\(x\\)-Achse?' : 'rechts oder links der \\(y\\)-Achse?');
            if (w === 'Höhe') return 'Das sind die Lösungen von \\(\\cos\\varphi = ' + exTex(A.t) + '\\). Der Sinus ist die Höhe von \\(P\\): Zeichne die Waagrechte \\(y = ' + exTex(A.t) + '\\).';
            if (w === 'waagrechte') return 'Das sind die Lösungen von \\(\\sin\\varphi = ' + exTex(A.t) + '\\). Der Cosinus ist die waagrechte Koordinate: Zeichne die Senkrechte \\(x = ' + exTex(A.t) + '\\).';
            if (w === 'Intervall') return 'Die Punkte stimmen, aber nicht alle Winkel liegen im Intervall \\(' + ivTex(A.iv) + '\\). Zähl \\(360^\\circ\\) dazu oder ab — es bleibt derselbe Punkt.';
          }
          var ein = [e.a, e.b].filter(function(v){ return A.l.some(function(x){ return gl(v, x); }); }).length;
          if (ein === 1) return 'Eine der beiden stimmt. Wo liegt der zweite Punkt mit ' + (A.f === 'sin' ? 'derselben Höhe' : 'derselben \\(x\\)-Koordinate') + '?';
          return 'Zeichne ' + (A.f === 'sin' ? 'die Waagrechte \\(y = ' : 'die Senkrechte \\(x = ') + exTex(A.t) + '\\) in den Einheitskreis und lies die Winkel über die besonderen Werte ab.'; },
        loesung: function(A){ return ftex(A.f) + ' = ' + exTex(A.t) + ':\\ \\mathbb{L} = ' + mtex(A.l); } },

      /* ── Kapitel 2: In welchen Quadranten? ────────────────────────── */
      'quadranten': { felder: ['q'], muster: 'Die Lösungen liegen im {q:I. und II.|II. und III.|III. und IV.|I. und IV.} Quadranten.',
        schl: function(A){ return 'qu|' + A.f + '|' + A.c; },
        eingabe: function(A){ return { q: A.q }; },
        neu: function(){
          var f = zufall(['sin', 'cos']), c;
          do { c = zufall([-1, 1]) * (Math.floor(Math.random() * 90) + 6) / 100; } while (Math.abs(Math.abs(c) - 0.5) < 1e-9);
          var Q = { sin: c > 0 ? 'I. und II.' : 'III. und IV.', cos: c > 0 ? 'I. und IV.' : 'II. und III.' };
          return { f: f, c: c, q: Q[f], ander: { sin: c > 0 ? 'I. und IV.' : 'II. und III.', cos: c > 0 ? 'I. und II.' : 'III. und IV.' }[f],
            vz: { sin: c > 0 ? 'III. und IV.' : 'I. und II.', cos: c > 0 ? 'II. und III.' : 'I. und IV.' }[f],
            text: '\\(' + ftex(f) + ' = ' + tz(c) + '\\): In welchen Quadranten liegen die beiden Lösungen? Entscheide am Einheitskreis, ohne zu rechnen.' }; },
        fehler: function(A){ var f = [[{ q: A.ander }, A.f === 'sin' ? 'Höhe' : 'waagrechte'], [{ q: A.vz }, 'Vorzeichen']];
          ['I. und II.', 'II. und III.', 'III. und IV.', 'I. und IV.'].forEach(function(w){ if (w !== A.q && w !== A.ander && w !== A.vz) f.push([{ q: w }, 'Zeichne']); });
          return f; },
        pruefen: function(A, e){
          if (e.q === A.q) return null;
          if (e.q === A.ander) return A.f === 'sin' ? 'Das gilt für den Cosinus. Der Sinus ist die Höhe: Zeichne die Waagrechte \\(y = ' + tz(A.c) + '\\).' : 'Das gilt für den Sinus. Der Cosinus ist die waagrechte Koordinate: Zeichne die Senkrechte \\(x = ' + tz(A.c) + '\\).';
          if (e.q === A.vz) return 'Vorzeichen: \\(' + tz(A.c) + '\\) ist ' + (A.c > 0 ? 'positiv' : 'negativ') + ' — liegt die Gerade ' + (A.f === 'sin' ? 'über oder unter der \\(x\\)-Achse?' : 'rechts oder links der \\(y\\)-Achse?');
          return 'Zeichne ' + (A.f === 'sin' ? 'die Waagrechte \\(y = ' : 'die Senkrechte \\(x = ') + tz(A.c) + '\\) in den Einheitskreis. Ihre beiden Schnittpunkte liegen ' + (A.f === 'sin' ? 'auf gleicher Höhe, links und rechts der \\(y\\)-Achse.' : 'senkrecht übereinander, über und unter der \\(x\\)-Achse.'); },
        loesung: function(A){ var l = loesungen(A.f, A.c); return ftex(A.f) + ' = ' + tz(A.c) + ':\\ \\text{Quadranten ' + A.q + '}\\ (' + l.map(naeh).join(';\\ ') + ')'; } },

      /* ── Kapitel 2: zweite Lösung zum Wert des Rechners ───────────── */
      // Felder ohne «φ₁/φ₂»: φ₁ heisst im Festhalten der Hauptwert, der oft nicht im Intervall liegt
      'zweite': { felder: ['a', 'b'], muster: 'Lösungen: ≈ {a} ° &nbsp;und&nbsp; ≈ {b} °',
        schl: function(A){ return 'zw|' + A.f + '|' + A.c; },
        eingabe: function(A){ return pz(A.l); },
        neu: function(){
          var f = zufall(['sin', 'cos']), c;
          do { c = zufall([-1, 1]) * (Math.floor(Math.random() * 86) + 8) / 100; } while ([0.5].indexOf(Math.abs(c)) >= 0);
          var h = hauptwert(f, c), l = loesungen(f, c).map(r1);
          return { f: f, c: c, h: h, hr: r1(h), l: l,
            text: 'Der Rechner liefert für \\(' + ftex(f) + ' = ' + tz(c) + '\\): \\(\\' + f + '^{-1}(' + tz(c) + ') \\approx ' + tz(r1(h)) + '^\\circ\\). Gib beide Lösungen im Intervall \\([0^\\circ;\\, 360^\\circ[\\) an, auf \\(0.1^\\circ\\) gerundet.' }; },
        kandidaten: function(A){
          var h = A.h, k = [];
          if (A.f === 'sin'){
            k.push([[mod360(h), mod360(360 - h)], 'Cosinus']);           // Regel des Cosinus
            if (h < 0) k.push([[h, 180 - h], 'Intervall']);             // negativen Hauptwert stehen gelassen
            k.push([[mod360(h), mod360(180 + h)], 'anderen Seite der']);         // 180° + φ₁ statt 180° − φ₁
          } else {
            k.push([[h, 180 - h], 'Sinus']);                            // Regel des Sinus
            k.push([[h, 180 + h], 'anderen Seite der']);                           // 180° + φ₁
          }
          return k.map(function(x){ return [x[0].map(r1).sort(function(a, b){ return a - b; }), x[1]]; }); },
        fehler: function(A){ var aus = [], gesehen = [A.l.join('|')];
          this.kandidaten(A).forEach(function(x){ var s = x[0].join('|'); if (gesehen.indexOf(s) < 0){ gesehen.push(s); aus.push([pz(x[0]), x[1]]); } });
          return aus; },
        pruefen: function(A, e){
          if (paar(e, A.l[0], A.l[1], 0.11)) return null;
          var ks = this.kandidaten(A);
          for (var i = 0; i < ks.length; i++) if (paar(e, ks[i][0][0], ks[i][0][1], 0.11)){
            var w = ks[i][1];
            if (w === 'Cosinus') return '\\(360^\\circ - \\varphi_1\\) ist die Regel beim Cosinus. Beim Sinus liegt der zweite Punkt auf derselben Höhe: \\(180^\\circ - \\varphi_1\\).';
            if (w === 'Intervall') return '\\(' + tz(A.hr) + '^\\circ\\) liegt nicht im Intervall. Eine volle Drehung weiter ist es derselbe Punkt: \\(+\\,360^\\circ\\).';
            if (w === 'anderen Seite der' && A.f === 'sin') return 'Bei \\(180^\\circ + \\varphi_1\\) liegt \\(P\\) auf der anderen Seite der \\(x\\)-Achse. Probe: Hat der Sinus dort das Vorzeichen von \\(' + tz(A.c) + '\\)? Richtig ist \\(180^\\circ - \\varphi_1\\).';
            if (w === 'Sinus') return '\\(180^\\circ - \\varphi_1\\) ist die Regel beim Sinus. Beim Cosinus haben beide Punkte dieselbe \\(x\\)-Koordinate: \\(360^\\circ - \\varphi_1\\).';
            if (w === 'anderen Seite der') return 'Bei \\(180^\\circ + \\varphi_1\\) liegt \\(P\\) auf der anderen Seite der \\(y\\)-Achse. Probe: Hat der Cosinus dort das Vorzeichen von \\(' + tz(A.c) + '\\)? Richtig ist \\(360^\\circ - \\varphi_1\\).';
          }
          var ein = [e.a, e.b].filter(function(v){ return A.l.some(function(x){ return gl(v, x, 0.11); }); }).length;
          if (ein === 1) return 'Eine stimmt. Die andere: ' + (A.f === 'sin' ? '\\(180^\\circ - \\varphi_1\\) (Spiegelung an der \\(y\\)-Achse)' : '\\(360^\\circ - \\varphi_1\\) (Spiegelung an der \\(x\\)-Achse)') + ', danach ins Intervall bringen.';
          return 'Zeichne den Punkt des Rechners und ' + (A.f === 'sin' ? 'die Waagrechte durch ihn' : 'die Senkrechte durch ihn') + '. Wo trifft sie den Kreis ein zweites Mal?'; },
        loesung: function(A){ var x = A.f === 'sin' ? '\\varphi_2 = 180^\\circ - (' + tz(A.hr) + '^\\circ)' : '\\varphi_2 = 360^\\circ - ' + tz(A.hr) + '^\\circ';
          return '\\varphi_1 \\approx ' + tz(A.hr) + '^\\circ,\\ ' + x + (A.f === 'sin' && A.h < 0 ? ',\\ ' + tz(A.hr) + '^\\circ + 360^\\circ' : '') + ':\\ \\mathbb{L} = ' + mtex(A.l); } },

      /* ── Kapitel 3: Tangensgleichung mit dem Rechner ──────────────── */
      'tan-loesen': { felder: ['a', 'b'], muster: 'Lösungen: ≈ {a} ° &nbsp;und&nbsp; ≈ {b} °',
        schl: function(A){ return 'tl|' + A.c; },
        eingabe: function(A){ return pz(A.l); },
        neu: function(){
          var c = zufall([-1, 1]) * zufall([0.15, 0.3, 0.4, 0.7, 0.8, 0.9, 1.4, 1.6, 1.8, 2.2, 2.7, 3.5, 4, 6, 8]);
          var h = hauptwert('tan', c);
          return { c: c, h: h, l: loesungen('tan', c).map(r1),
            text: 'Löse \\(\\tan\\varphi = ' + tz(c) + '\\) im Intervall \\([0^\\circ;\\, 360^\\circ[\\), mit dem Taschenrechner, auf \\(0.1^\\circ\\) gerundet.' }; },
        kandidaten: function(A){
          var h = A.h, k = [[[h, 180 - h], 'Sinus'], [[h, 360 - h], 'Cosinus']];
          if (h < 0) k = [[[h, h + 180], 'Intervall'], [[180 - h, 360 + h], 'Sinus'], [[-h, 360 + h], 'Cosinus']];
          return k.map(function(x){ return [x[0].map(r1).sort(function(a, b){ return a - b; }), x[1]]; }); },
        fehler: function(A){ var aus = [], gesehen = [A.l.join('|')];
          this.kandidaten(A).forEach(function(x){ var s = x[0].join('|'); if (gesehen.indexOf(s) < 0){ gesehen.push(s); aus.push([pz(x[0]), x[1]]); } });
          return aus; },
        pruefen: function(A, e){
          if (paar(e, A.l[0], A.l[1], 0.11)) return null;
          var ks = this.kandidaten(A);
          for (var i = 0; i < ks.length; i++) if (paar(e, ks[i][0][0], ks[i][0][1], 0.11)){
            var w = ks[i][1];
            if (w === 'Sinus') return 'Das ist die Regel beim Sinus (\\(180^\\circ - \\varphi\\)). Beim Tangens liegt der zweite Punkt gegenüber, auf derselben Geraden durch \\(O\\): \\(+\\,180^\\circ\\).';
            if (w === 'Cosinus') return 'Das ist die Regel beim Cosinus (\\(360^\\circ - \\varphi\\)). Beim Tangens liegt der zweite Punkt gegenüber, auf derselben Geraden durch \\(O\\): \\(+\\,180^\\circ\\).';
            if (w === 'Intervall') return '\\(' + tz(r1(A.h)) + '^\\circ\\) liegt nicht im Intervall. Zähl \\(180^\\circ\\) und \\(360^\\circ\\) dazu.';
          }
          if ([e.a, e.b].some(function(v){ return gl(v, r1(A.h - 180), 0.11) || gl(v, r1(A.h + 540), 0.11); })) return 'Nicht alle Winkel liegen im Intervall \\([0^\\circ;\\, 360^\\circ[\\).';
          var ein = [e.a, e.b].filter(function(v){ return A.l.some(function(x){ return gl(v, x, 0.11); }); }).length;
          if (ein === 1) return 'Eine stimmt. Die andere liegt \\(180^\\circ\\) daneben — im Gegenpunkt.';
          return 'Tipp \\(\\tan^{-1}(' + tz(A.c) + ')\\) (Modus DEG). Dann \\(+\\,180^\\circ\\)' + (A.h < 0 ? ' und \\(+\\,360^\\circ\\)' : '') + '.'; },
        loesung: function(A){ var h = r1(A.h);
          return '\\tan^{-1}(' + tz(A.c) + ') \\approx ' + tz(h) + '^\\circ' + (A.h < 0 ? ',\\ ' + tz(h) + '^\\circ + 180^\\circ,\\ ' + tz(h) + '^\\circ + 360^\\circ' : ',\\ ' + tz(h) + '^\\circ + 180^\\circ') + ':\\ \\mathbb{L} = ' + mtex(A.l); } },

      /* ── Kapitel 3: Tangens, besondere Werte ──────────────────────── */
      'tan-spezial': { felder: ['a', 'b'], muster: 'Lösungen: {a} ° &nbsp;und&nbsp; {b} °',
        schl: function(A){ return 'ts|' + A.t + '|' + A.iv; },
        eingabe: function(A){ return pz(A.l); },
        neu: function(){
          var t = zufall(['0', '1', '−1', '√3', '−√3', '√3/3', '−√3/3']), iv = '0';   // nur [0°; 360°[ (M3)
          return { t: t, iv: iv, l: lsg('tan', exZahl(t), iv),
            text: 'Löse ohne Taschenrechner: \\(\\tan\\varphi = ' + exTex(t) + '\\) im Intervall \\(' + ivTex(iv) + '\\).' }; },
        kandidaten: function(A){
          var c = exZahl(A.t), h = hauptwert('tan', c), k = [], lo = IV[A.iv][2], hi = IV[A.iv][3];
          k.push([lsg('tan', -c, A.iv), 'Vorzeichen']);
          var kehr = { '√3': '√3/3', '√3/3': '√3' }[A.t.replace('−', '')];
          if (kehr) k.push([lsg('tan', (c < 0 ? -1 : 1) * EX[kehr], A.iv), 'Referenzwinkel']);
          k.push([imIntervall([mod360(h), mod360(180 - h)], 360, lo, hi), 'Sinus']);
          k.push([imIntervall([mod360(h), mod360(360 - h)], 360, lo, hi), 'Cosinus']);
          return k.filter(function(x){ return x[0].length === 2; }); },
        fehler: function(A){ var aus = [], gesehen = [A.l.join('|')];
          this.kandidaten(A).forEach(function(x){ var s = x[0].join('|'); if (gesehen.indexOf(s) < 0){ gesehen.push(s); aus.push([pz(x[0]), x[1]]); } });
          return aus; },
        pruefen: function(A, e){
          if (paar(e, A.l[0], A.l[1])) return null;
          var ks = this.kandidaten(A);
          for (var i = 0; i < ks.length; i++) if (paar(e, ks[i][0][0], ks[i][0][1])){
            var w = ks[i][1];
            if (w === 'Vorzeichen') return 'Vorzeichen: Der Tangens ist im I. und III. Quadranten positiv, im II. und IV. negativ.';
            if (w === 'Referenzwinkel') return 'Referenzwinkel vertauscht: \\(\\tan 30^\\circ = \\tfrac{\\sqrt{3}}{3}\\), \\(\\tan 60^\\circ = \\sqrt{3}\\).';
            if (w === 'Sinus') return 'Das ist die Regel beim Sinus. Beim Tangens liegt der zweite Punkt gegenüber: \\(+\\,180^\\circ\\).';
            if (w === 'Cosinus') return 'Das ist die Regel beim Cosinus. Beim Tangens liegt der zweite Punkt gegenüber: \\(+\\,180^\\circ\\).';
          }
          return 'Besondere Werte: \\(\\tan 0^\\circ = 0\\), \\(\\tan 30^\\circ = \\tfrac{\\sqrt{3}}{3}\\), \\(\\tan 45^\\circ = 1\\), \\(\\tan 60^\\circ = \\sqrt{3}\\). Die zweite Lösung liegt \\(180^\\circ\\) daneben.'; },
        loesung: function(A){ return '\\tan\\varphi = ' + exTex(A.t) + ':\\ \\mathbb{L} = ' + mtex(A.l); } },

      /* ── Kapitel 4: alle Lösungen mit k ───────────────────────────── */
      'allgemein': { felder: ['a', 'b', 'p'], felderTan: ['a', 'p'],
        muster: function(A){ return A.f === 'tan' ? 'φ = {a} ° + k · {p:90°|180°|360°}, &nbsp;k ∈ ℤ'
                                                  : 'φ = {a} ° + k · {p:90°|180°|360°} &nbsp; oder &nbsp; φ = {b} ° + k · (dieselbe Periode)'; },
        schl: function(A){ return 'al|' + A.f + '|' + A.t; },
        eingabe: function(A){ return A.f === 'tan' ? { a: String(A.l[0]), p: '180°' } : { a: String(A.l[0]), b: String(A.l[1]), p: '360°' }; },
        neu: function(){
          var f = zufall(['sin', 'cos', 'tan', 'sin', 'cos']);
          var t = f === 'tan' ? zufall(['1', '−1', '√3', '−√3', '√3/3', '−√3/3']) : zufall(['1/2', '−1/2', '√2/2', '−√2/2', '√3/2', '−√3/2']);
          var l = loesungen(f, exZahl(t)); if (f === 'tan') l = [l[0]];
          return { f: f, t: t, l: l, p: f === 'tan' ? 180 : 360,
            text: 'Gib alle Lösungen von \\(' + ftex(f) + ' = ' + exTex(t) + '\\) an, ohne Taschenrechner. Wähle die Grundlösung' + (f === 'tan' ? '' : 'en') + ' zwischen \\(0^\\circ\\) und \\(360^\\circ\\).' }; },
        fehler: function(A){ var f = [];
          if (A.f === 'tan'){ f.push([{ a: String(A.l[0]), p: '360°' }, 'jede zweite']); f.push([{ a: String(A.l[0]), p: '90°' }, 'Periode stimmt nicht']);
            f.push([{ a: String(mod360(180 - A.l[0])), p: '180°' }, 'Vorzeichen']); }
          else { f.push([{ a: String(A.l[0]), b: String(A.l[1]), p: '180°' }, 'erst nach']);
            var c = exZahl(A.t), h = hauptwert(A.f, c), m = A.f === 'sin' ? [mod360(h), mod360(360 - h)] : [mod360(h), mod360(180 - h)];
            m.sort(function(a, b){ return a - b; });
            if (m.join('|') !== A.l.join('|')) f.push([{ a: String(m[0]), b: String(m[1]), p: '360°' }, 'Grundlösung']); }
          return f; },
        pruefen: function(A, e){
          var p = parseInt(e.p, 10), ok1 = function(v, x){ return gl(mod360(v - x + 720) % A.p, 0) || gl(mod360(v - x + 720) % A.p, A.p); };
          var gr = A.f === 'tan' ? ok1(e.a, A.l[0]) : ((ok1(e.a, A.l[0]) && ok1(e.b, A.l[1])) || (ok1(e.a, A.l[1]) && ok1(e.b, A.l[0])));
          if (gr && p === A.p) return null;
          if (gr && A.f === 'tan' && p === 360) return 'Mit \\(360^\\circ\\) fehlt jede zweite Lösung: Der Tangens wiederholt sich schon nach \\(180^\\circ\\).';
          if (gr && A.f !== 'tan' && p === 180) return 'Sinus und Cosinus wiederholen sich erst nach \\(360^\\circ\\). Mit \\(180^\\circ\\) kämen falsche Winkel dazu.';
          if (gr) return 'Die Periode stimmt nicht: \\(360^\\circ\\) bei Sinus und Cosinus, \\(180^\\circ\\) beim Tangens.';
          if (A.f === 'tan') return 'Grundlösung prüfen: Vorzeichen und besonderer Wert — \\(\\tan 45^\\circ = 1\\), \\(\\tan 60^\\circ = \\sqrt{3}\\), \\(\\tan 30^\\circ = \\tfrac{\\sqrt{3}}{3}\\).';
          return 'Erst die Grundlösungen in \\([0^\\circ;\\, 360^\\circ[\\) bestimmen (Kapitel 1), dann die Periode anhängen.'; },
        loesung: function(A){ return A.f === 'tan' ? '\\varphi = ' + gtex(A.l[0]) + ' + k \\cdot 180^\\circ,\\ k \\in \\mathbb{Z}'
          : '\\varphi = ' + gtex(A.l[0]) + ' + k \\cdot 360^\\circ\\ \\text{oder}\\ \\varphi = ' + gtex(A.l[1]) + ' + k \\cdot 360^\\circ,\\ k \\in \\mathbb{Z}'; } },

      /* ── Kapitel 4: Lösungen in einem Intervall ───────────────────── */
      'intervall': { felder: ['l'], roh: ['l'], muster: '𝕃 = { {l} } &nbsp;<small>(Winkel in Grad, mit Strichpunkt getrennt, aufsteigend)</small>',
        schl: function(A){ return 'iv|' + A.g.join('|') + '|' + A.lo + '|' + A.hi; },
        eingabe: function(A){ return { l: A.l.join('; ') }; },
        neu: function(){
          var f = zufall(['sin', 'cos', 'tan']), r = 5 * (Math.floor(Math.random() * 16) + 1), g;
          if (f === 'sin') g = Math.random() < 0.5 ? [r, 180 - r] : [180 + r, 360 - r];
          else if (f === 'cos') g = Math.random() < 0.5 ? [r, 360 - r] : [180 - r, 180 + r];
          else g = [Math.random() < 0.5 ? r : 180 - r];
          var iv = zufall([[0, 720], [-360, 0], [360, 720], [-180, 180], [-360, 360], [0, 540]]);
          var p = f === 'tan' ? 180 : 360, l = imIntervall(g, p, iv[0], iv[1]);
          var gt = g.length === 2 ? '\\(' + g[0] + '^\\circ\\) und \\(' + g[1] + '^\\circ\\)' : '\\(' + g[0] + '^\\circ\\)';
          return { f: f, g: g, p: p, lo: iv[0], hi: iv[1], l: l,
            text: '\\(' + ftex(f) + ' = c\\) hat im Intervall \\([0^\\circ;\\, ' + (f === 'tan' ? '180' : '360') + '^\\circ[\\) die Lösung' + (g.length === 2 ? 'en ' : ' ') + gt + '. Gib alle Lösungen im Intervall \\([' + tz(iv[0]) + '^\\circ;\\, ' + tz(iv[1]) + '^\\circ[\\) an.' }; },
        fehler: function(A){ var f = [], ein = function(l){ return { l: l.join('; ') }; };
          var halb = A.p === 180 ? imIntervall(A.g, 360, A.lo, A.hi) : null, ohne = A.l.slice(0, -1);
          if (A.l.length > 1 && !(halb && halb.join('|') === ohne.join('|'))) f.push([ein(ohne), 'fehlen']);
          if (A.l.length > 1) f.push([ein(A.l.slice().reverse()), 'aufsteigend']);
          var draussen = A.l.concat([A.l[A.l.length - 1] + A.p]).filter(function(v){ return v >= A.hi; }).length ? A.l.concat([A.l[A.l.length - 1] + A.p]) : null;
          if (draussen) f.push([ein(draussen), 'nicht im']);
          if (halb && halb.length < A.l.length) f.push([ein(halb), 'Tangens']);
          return f; },
        pruefen: function(A, e){
          var l = typeof e.l === 'string' ? liste(e.l) : (typeof e.l === 'number' ? [e.l] : null);
          if (l === null) return 'Gib die Winkel ein, mit Strichpunkt getrennt, zum Beispiel <code>30; 150; 390</code>.';
          if (!Array.isArray(l)) return 'Nur Zahlen, mit Strichpunkt getrennt: <code>30; 150; 390</code>.';
          var drin = l.filter(function(v){ return v >= A.lo - 1e-9 && v < A.hi - 1e-9; });
          var stimmt = l.filter(function(v){ return A.l.some(function(x){ return gl(v, x); }); });
          var sortiert = l.every(function(v, i){ return i === 0 || v > l[i - 1]; });
          if (stimmt.length === A.l.length && l.length === A.l.length) return sortiert ? null : 'Die Winkel stimmen. In der Lösungsmenge stehen sie aufsteigend.';
          if (drin.length < l.length) return 'Mindestens ein Winkel liegt nicht im Intervall \\([' + tz(A.lo) + '^\\circ;\\, ' + tz(A.hi) + '^\\circ[\\) — die rechte Grenze gehört nicht dazu.';
          var halb = imIntervall(A.g, 360, A.lo, A.hi);
          if (A.p === 180 && l.length === halb.length && halb.every(function(x){ return l.some(function(v){ return gl(v, x); }); })) return 'Beim Tangens ist die Periode \\(180^\\circ\\): Zähl \\(180^\\circ\\) dazu, nicht \\(360^\\circ\\). So fehlen Lösungen.';
          if (stimmt.length === l.length && l.length < A.l.length) return 'Es fehlen Lösungen. Setze für \\(k\\) der Reihe nach \\(\\ldots, -1, 0, 1, 2, \\ldots\\) ein.';
          return 'Rechne jede Grundlösung \\(+\\,k \\cdot ' + A.p + '^\\circ\\) und behalte nur die Werte im Intervall.'; },
        loesung: function(A){ return '\\mathbb{L} = ' + mtex(A.l); } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        // Trifft der Wurf eine feste Aufgabe des Leitprogramms, wird neu gewürfelt (SPERRE oben).
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = typeof T.muster === 'function' ? T.muster(A) : T.muster;
        var felder = A.f === 'tan' && T.felderTan ? T.felderTan : T.felder;
        felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="' + (T.roh && T.roh.indexOf(f) >= 0 ? 'text' : 'decimal') + '" autocomplete="off" aria-label="' + f + '" data-f="' + f + '"' + (T.roh && T.roh.indexOf(f) >= 0 ? ' class="breit"' : '') + '>';
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
          if (T.roh && T.roh.indexOf(i.dataset.f) >= 0){ e[i.dataset.f] = i.value; if (!i.value.trim()) leer = true; return; }
          var r = lesen(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('input') ? 'Fülle alle Felder aus.' : 'Wähle aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Winkel als Zahl in Grad, zum Beispiel <code>156.4</code> oder <code>-23.6</code>.'; return; }
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
