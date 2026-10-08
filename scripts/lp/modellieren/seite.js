<script>
/* Leitprogramm Modellieren — vier Simulationen mit Aufgabenleiste, Bilder zu den Aufgaben, Übungen mit
   Rückmeldung. Notation wie auf Themenseite 2.M: Unbekannte mit Bedeutung und Einheit; Zahl = 10 · z + e;
   Mengenbilanz x + y = M und Stoffbilanz p₁ · x + p₂ · y = p · M (Anteile als Dezimalzahl); Stückbilanz
   x + y = N und Wertbilanz a · x + b · y = W; Kapitalgleichung x + y = K und Zinsgleichung
   p₁ · t₁ · x + p₂ · t₂ · y = Z; Zinseszins K · (1 + p)² (Themenseite A7). Lösungsmengen mit Strichpunkt.
   Eine Farbe, eine Bedeutung (gleich wie in den Clips g2-M-lp-*): blau = erste Unbekannte und ihre Sorte,
   orange = zweite Unbekannte und ihre Sorte, grün = Ergebnis, Mischung, Lösung, rot = Fehler.
   Zahlen mit Dezimalpunkt, echtem Minus und schmalem Leerzeichen als Tausendertrenner. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', NB = ' ';
  /* Zahl für Anzeigen: höchstens 6 Nachkommastellen (Faktoren wie 0.00375 exakt, Prüfung 08.10.2026, H2 — mit 4 Stellen
     stand «0.0038» als Lösung da), Tausendertrenner ab 5 Stellen (wie die Themenseite: 7000, 30 000) */
  function z(v, st){
    var r = Math.round(v * 1e6) / 1e6; if (Object.is(r, -0)) r = 0;
    var s = st == null ? String(Math.abs(r)) : Math.abs(r).toFixed(st);
    var t = s.split('.'), g = t[0];
    if (g.length > 4) g = g.replace(/\B(?=(\d{3})+(?!\d))/g, NB);
    return (r < 0 ? '−' : '') + g + (t[1] ? '.' + t[1] : '');
  }
  function zt(v){ return z(v).replace(/ /g, '\\,').replace('−', '-'); }      // dieselbe Zahl in LaTeX
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function leer(svg){ while (svg.firstChild) svg.removeChild(svg.firstChild); }
  function gleich(a, b){ return Math.abs(a - b) < 1e-9; }
  /* Franken auf Rappen: exakt mit «=», gerundet mit «≈» (Live-Anzeigen runden nur mit «≈», HOWTO §15) */
  function chf(v){ return (Math.abs(v * 100 - Math.round(v * 100)) > 1e-6 ? '≈ ' : '') + z(Math.round(v * 100) / 100, 2); }

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
      r[k].parentNode.querySelector('.sl-val').textContent = (st < 1 ? z(v, 1) : z(v)) + e;
    }
    return w;
  }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function wahlWert(fig, name){ var e = fig.querySelector('input[name="' + name + '"]:checked'); return e ? e.value : null; }
  function wahlSetzen(fig, name, w){ fig.querySelectorAll('input[name="' + name + '"]').forEach(function(rb){ rb.checked = rb.value === w; }); }
  /* Merk-Objekte werden geleert, nie neu zugewiesen (Prüfung Trigonometrie 05.10.2026, H1). */
  function leeren(o){ for (var k in o) delete o[k]; }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ----------
     Beim Wechsel gehen Regler und Auswahlknöpfe auf ihren Startwert zurück, damit der Endzustand der
     vorigen Aufgabe die nächste nicht schon löst (HOWTO §15). */
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
        if (k === n){ nr.textContent = '✓'; tx.innerHTML = 'Alle ' + n + ' Aufgaben gelöst — weiter mit den Kontrollclips.'; bt.textContent = 'nochmals'; bv.hidden = true; box.classList.add('fertig'); }
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
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; inp.disabled = false; });
      fig.querySelectorAll('input[type=radio]').forEach(function(inp){ inp.checked = inp.defaultChecked; });
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

  /* ---------- Zeichenhilfen ---------- */
  function rechteck(g, x, y, b, h, cls){ return el(g, 'rect', { x: x, y: y, width: Math.max(0, b), height: Math.max(0, h), 'class': cls }); }
  function text(g, x, y, t, cls, anker){ return el(g, 'text', { x: x, y: y, 'text-anchor': anker || 'middle', 'class': cls || 'bt' }, t); }
  /* Zehnerstange: Rechteck mit neun Teilstrichen; Einerwürfel: kleines Quadrat */
  function stange(g, x, y0, b, h, farbe){
    rechteck(g, x, y0 - h, b, h, 'st ' + farbe);
    for (var k = 1; k < 10; k++) el(g, 'line', { x1: x, y1: y0 - h * k / 10, x2: x + b, y2: y0 - h * k / 10, 'class': 'st-teil ' + farbe });
  }
  /* Zahl aus Zehnerstangen und Einerwürfeln, links unten bei (x0 | y0) */
  function zahlbild(g, x0, y0, zehner, einer, fZ, fE, s){
    s = s || 1;
    var b = 11 * s, h = 110 * s, lz = 14 * s;
    for (var k = 0; k < zehner; k++) stange(g, x0 + k * lz, y0, b, h, fZ);
    var xe = x0 + Math.max(zehner, 0) * lz + 6 * s;
    for (var j = 0; j < einer; j++) rechteck(g, xe, y0 - (j + 1) * 11 * s, b, b * 0.92, 'st ' + fE);
    return xe + b;
  }

  /* ---------- Kapitel 1: Stellenwert ----------
     Die Themenseite hat zur Grundgleichung keine Animation (nur den Ansatz-Trainer). Hier steht die Zahl als
     Zehnerstangen und Einerwürfel neben der vertauschten Zahl: 10 · z + e und 10 · e + z zum Bedienen. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'); svg.setAttribute('viewBox', '0 0 560 250');
    var pruefen = function(){}, merk = {};
    var r = regler(fig, zeichnen);
    // vor dem Zeichnen registriert: Der Merkzettel steht, bevor geprüft wird (HOWTO §15)
    function merken(){ var w = werte(r); merk.bewegt = true; if (w.e > w.z) merk.groesser = true; if (w.e < w.z) merk.kleiner = true;
      merk['z' + w.z + 'e' + w.e] = true; }
    Object.keys(r).forEach(function(k){ r[k].addEventListener('input', merken); r[k].addEventListener('input', function(){ pruefen(); }); });
    function zust(){ var w = werte(r); return { z: w.z, e: w.e, merk: merk }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(merk); } };
    function zeichnen(){
      var w = werte(r), zz = w.z, ee = w.e, n = 10 * zz + ee, v = 10 * ee + zz;
      leer(svg);
      var g = el(svg, 'g', {});
      text(g, 130, 22, 'Zahl', 'bt-kopf'); text(g, 420, 22, 'vertauscht', 'bt-kopf');
      zahlbild(g, 22, 190, zz, ee, 'blau', 'orange', 1.25);
      zahlbild(g, 300, 190, ee, zz, 'orange', 'blau', 1.25);
      text(g, 130, 222, String(n), 'bt-zahl'); text(g, 420, 222, ee === 0 ? '0' + zz + ' = ' + zz : String(v), 'bt-zahl');
      el(g, 'line', { x1: 280, y1: 40, x2: 280, y2: 228, 'class': 'trenn' });
      var d = v - n;
      rolle(fig, 'formel').innerHTML = 'Zahl: 10 · ' + sp('tx-blau', zz) + ' + ' + sp('tx-orange', ee) + ' = ' + n
        + '; &nbsp;vertauscht: 10 · ' + sp('tx-orange', ee) + ' + ' + sp('tx-blau', zz) + ' = ' + v
        + '<br>Differenz ' + z(v) + ' − ' + z(n) + ' = ' + z(d) + ' = 9 · (' + ee + ' − ' + zz + ')'
        + '; &nbsp;Quersumme ' + (zz + ee) + '; &nbsp;Produkt der Ziffern ' + (zz * ee);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Stelle Zahlen ein, die beim Vertauschen grösser werden, und solche, die kleiner werden.',
        ok: function(s){ return s.merk.groesser && s.merk.kleiner; } },
      { text: 'Stelle die Zahl 50 ein. Welche Zahl entsteht beim Vertauschen?', ok: function(s){ return s.z === 5 && s.e === 0; } },
      { text: 'Finde eine Zahl, die beim Vertauschen um 54 kleiner wird.', ok: function(s){ return 9 * (s.z - s.e) === 54; } },
      { text: 'Die Quersumme ist 13, und beim Vertauschen wird die Zahl um 27 kleiner.',
        ok: function(s){ return s.z + s.e === 13 && 9 * (s.z - s.e) === 27; } },
      { text: 'Die Einerziffer ist um 2 grösser als das Doppelte der Zehnerziffer, und die Quersumme ist 11.',
        ok: function(s){ return s.e === 2 * s.z + 2 && s.z + s.e === 11; } },
      { text: 'Quersumme 9 und Produkt der Ziffern 20: Stelle nacheinander beide Zahlen ein, die passen.',
        ok: function(s){ return s.merk.z4e5 && s.merk.z5e4; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Mischen ----------
     Unterschied zur Themenseite: dort keine Animation. Hier drei Gefässe — Sorte 1, Sorte 2, Mischung —, die
     Menge als Füllhöhe und der Stoff als kräftiger Teil unten: Mengenbilanz und Stoffbilanz sieht man im Bild. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'); svg.setAttribute('viewBox', '0 0 560 300');
    var pruefen = function(){}, merk = {}, START = { p1: 0.2, p2: 0.5, n1: 'Sirup A', n2: 'Sirup B', stoff: 'Zucker' }, S = {};
    function sorten(o){ leeren(S); for (var k in o) S[k] = o[k]; }
    sorten(START);
    var r = regler(fig, zeichnen);
    Object.keys(r).forEach(function(k){ r[k].addEventListener('input', function(){ pruefen(); }); });
    function zust(){ var w = werte(r), st = S.p1 * w.x + S.p2 * w.y, m = w.x + w.y;
      return { x: w.x, y: w.y, m: m, stoff: st, anteil: m ? st / m : 0, p1: S.p1, p2: S.p2 }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ sorten(START); } };
    function pz(p){ return z(Math.round(p * 1000) / 10) + NB + '%'; }
    function becher(g, x, menge, stoff, fM, fS, titel, unter){
      var y0 = 250, k = 3.5, b = 110;
      rechteck(g, x, y0 - 62 * k, b, 62 * k, 'becher');
      rechteck(g, x, y0 - menge * k, b, menge * k, 'fuell ' + fM);
      rechteck(g, x, y0 - stoff * k, b, stoff * k, 'stoff ' + fS);
      text(g, x + b / 2, y0 + 18, titel, 'bt'); text(g, x + b / 2, y0 + 36, unter, 'bt-klein');
      if (menge > 0) text(g, x + b / 2, y0 - menge * k - 6, z(menge) + ' kg', 'bt-klein');
    }
    function zeichnen(){
      var s = zust();
      leer(svg);
      var g = el(svg, 'g', {});
      becher(g, 20, s.x, S.p1 * s.x, 'blau', 'blau', S.n1, pz(S.p1));
      text(g, 165, 160, '+', 'bt-zahl');
      becher(g, 210, s.y, S.p2 * s.y, 'orange', 'orange', S.n2, pz(S.p2));
      text(g, 355, 160, '=', 'bt-zahl');
      becher(g, 400, s.m, s.stoff, 'gruen', 'gruen', 'Mischung', s.m ? (gleich(s.anteil * 1000, Math.round(s.anteil * 1000)) ? '' : '≈ ') + pz(s.anteil) : '—');
      var anteil = s.m ? (Math.abs(s.anteil * 1000 - Math.round(s.anteil * 1000)) < 1e-9 ? '= ' : '≈ ') + pz(s.anteil) : '—';
      rolle(fig, 'formel').innerHTML = 'Menge: ' + sp('tx-blau', z(s.x)) + ' + ' + sp('tx-orange', z(s.y)) + ' = ' + z(s.m) + ' kg'
        + '; &nbsp;' + S.stoff + ': ' + z(S.p1) + ' · ' + sp('tx-blau', z(s.x)) + ' + ' + z(S.p2) + ' · ' + sp('tx-orange', z(s.y)) + ' = ' + z(s.stoff) + ' kg'
        + '<br>Anteil der Mischung ' + anteil;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Mische gleich viel von beiden Sorten. Welchen Anteil hat die Mischung?',
        ok: function(s){ return s.x === s.y && s.x > 0; } },
      { text: 'Stelle 24 kg Mischung mit 40 % Zucker ein.', ok: function(s){ return s.m === 24 && gleich(s.stoff, 9.6); } },
      { text: 'Die Mischung soll 6 kg Zucker enthalten und 25 % Zucker haben.', ok: function(s){ return gleich(s.stoff, 6) && s.m === 24; } },
      { text: 'Jetzt ist Sorte 2 Wasser. Verdünne 15 kg der 10-%-Lösung auf 6 %.',
        setup: function(){ sorten({ p1: 0.1, p2: 0, n1: 'Lösung', n2: 'Wasser', stoff: 'Salz' }); },
        ok: function(s){ return s.x === 15 && s.m > 0 && gleich(s.anteil, 0.06); } },
      { text: 'Zielspiel mit Sirup A und B: 30 kg mit 32 % Zucker.', ok: function(s){ return s.m === 30 && gleich(s.stoff, 9.6); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Verteilen, Rechteckmodell ----------
     Themenseite ohne Animation. Hier ist jede Sorte ein Rechteck: Breite = Anzahl, Höhe = Wert pro Stück,
     Fläche = Wert. Die Stückbilanz ist die ganze Breite, die Wertbilanz die ganze Fläche. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'); svg.setAttribute('viewBox', '0 0 560 300');
    var pruefen = function(){}, merk = {}, START = { a: 18, b: 14, stueck: 'Fahrten', wert: 't', n1: 'A', n2: 'B' }, S = {};
    function sorte(o){ leeren(S); for (var k in o) S[k] = o[k]; }
    sorte(START);
    var r = regler(fig, zeichnen);
    function merken(){ var w = werte(r); if (w.x + w.y === 12) merk['x' + w.x] = true; }
    Object.keys(r).forEach(function(k){ r[k].addEventListener('input', merken); r[k].addEventListener('input', function(){ pruefen(); }); });
    function zust(){ var w = werte(r); return { x: w.x, y: w.y, n: w.x + w.y, w: S.a * w.x + S.b * w.y, a: S.a, merk: merk }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(merk); sorte(START); } };
    function zeichnen(){
      var s = zust(), X0 = 48, Y0 = 250, kx = 11.5, ky = 9;    // Breite bis 40 Stück (Regler 20 + 20) passt in die viewBox
      leer(svg);
      var g = el(svg, 'g', {});
      for (var t = 0; t <= 40; t += 5) { el(g, 'line', { x1: X0 + t * kx, y1: Y0, x2: X0 + t * kx, y2: Y0 + 5, 'class': 'achse' }); text(g, X0 + t * kx, Y0 + 18, String(t), 'skala'); }
      [S.a, S.b].forEach(function(h){ el(g, 'line', { x1: X0 - 5, y1: Y0 - h * ky, x2: X0 + 40 * kx, y2: Y0 - h * ky, 'class': 'gitter' }); text(g, X0 - 8, Y0 - h * ky + 4, String(h), 'skala', 'end'); });
      rechteck(g, X0, Y0 - S.a * ky, s.x * kx, S.a * ky, 'fl blau');
      rechteck(g, X0 + s.x * kx, Y0 - S.b * ky, s.y * kx, S.b * ky, 'fl orange');
      if (s.x > 2) text(g, X0 + s.x * kx / 2, Y0 - S.a * ky / 2, S.a + '·x', 'bt-klein');
      if (s.y > 2) text(g, X0 + (s.x + s.y / 2) * kx, Y0 - S.b * ky / 2, S.b + '·y', 'bt-klein');
      var oben = Y0 - Math.max(S.a, S.b) * ky - 16;
      if (s.n > 0) { el(g, 'line', { x1: X0, y1: oben, x2: X0 + s.n * kx, y2: oben, 'class': 'klammer' }); text(g, X0 + s.n * kx / 2, oben - 6, s.n + ' ' + S.stueck, 'bt-klein gruen'); }
      el(g, 'line', { x1: X0, y1: Y0, x2: 530, y2: Y0, 'class': 'achse' }); el(g, 'line', { x1: X0, y1: Y0, x2: X0, y2: 20, 'class': 'achse' });
      el(g, 'polygon', { points: '536,' + Y0 + ' 528,' + (Y0 - 4) + ' 528,' + (Y0 + 4), 'class': 'pfeil' });
      el(g, 'polygon', { points: X0 + ',14 ' + (X0 - 4) + ',22 ' + (X0 + 4) + ',22', 'class': 'pfeil' });
      text(g, 536, Y0 - 8, 'Anzahl', 'achsname', 'end'); text(g, X0 + 8, 18, S.wert + ' pro Stück', 'achsname', 'start');
      rolle(fig, 'formel').innerHTML = 'Stück: ' + sp('tx-blau', s.x) + ' + ' + sp('tx-orange', s.y) + ' = ' + s.n + ' ' + S.stueck
        + '; &nbsp;Wert: ' + S.a + ' · ' + sp('tx-blau', s.x) + ' + ' + S.b + ' · ' + sp('tx-orange', s.y) + ' = ' + z(s.w) + ' ' + S.wert;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Verteile die 12 Fahrten auf mindestens drei Arten (Breite immer 12). Wie ändert sich die Masse?',
        ok: function(s){ return Object.keys(s.merk).length >= 3; } },
      { text: 'Liefere mit 10 Fahrten genau 160 t.', ok: function(s){ return s.n === 10 && s.w === 160; } },
      { text: 'Liefere genau 200 t mit möglichst wenigen Fahrten.', ok: function(s){ return s.w === 200 && s.n === 12; } },
      { text: 'Jetzt Billette: Erwachsene 16 CHF, Kinder 9 CHF. 30 Personen bezahlen zusammen 382 CHF.',
        setup: function(){ sorte({ a: 16, b: 9, stueck: 'Billette', wert: 'CHF', n1: 'Erwachsene', n2: 'Kinder' }); },
        ok: function(s){ return s.n === 30 && s.w === 382; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Zins ----------
     Themenseite ohne Animation. Zwei Bilder: «zwei Anlagen» (Kapital geteilt, Zins je Teil als Säule, Zeitanteil
     umschaltbar) und «Zinseszins» (5000 CHF wachsen zwei Jahre mit dem Faktor 1 + p). */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'); svg.setAttribute('viewBox', '0 0 420 330');   // schmal: Schrift bei 360 px rund 13 px
    var pruefen = function(){}, merk = {}, S = { t2: 1 }, K = 30000, K2 = 5000;
    var r = regler(fig, zeichnen);
    function merken(){ var w = werte(r); if (wahlWert(fig, 's4-art') === 'a'){ if (w.x <= 6000) merk.wenig = true; if (w.x >= 24000) merk.viel = true; } }
    Object.keys(r).forEach(function(k){ r[k].addEventListener('input', merken); r[k].addEventListener('input', function(){ pruefen(); }); });
    fig.querySelectorAll('input[name="s4-art"]').forEach(function(rb){ rb.addEventListener('change', zeichnen); });
    function zust(){ var w = werte(r), art = wahlWert(fig, 's4-art'), x = w.x, y = K - x, p = w.p / 100;
      return { art: art, x: x, zins: 0.0075 * x + 0.02 * S.t2 * y, p: w.p, k2: K2 * (1 + p) * (1 + p), merk: merk }; }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ leeren(merk); S.t2 = 1; } };
    function zeichnen(){
      var s = zust(), g;
      fig.querySelectorAll('.sl-grp').forEach(function(gr){ var p = gr.querySelector('input').dataset.p; gr.hidden = (s.art === 'a') !== (p === 'x'); });
      leer(svg); g = el(svg, 'g', {});
      if (s.art === 'a'){
        /* Beschriftung gross genug für 360 px (Prüfung 08.10.2026: dort rund 7 px) und mit den Namen der Anlagen */
        var b = 360, X0 = 30, y = K - s.x, kz = 0.55;
        text(g, X0, 22, 'Kapital 30' + NB + '000 CHF', 'bt-kopf', 'start');
        rechteck(g, X0, 30, b * s.x / K, 44, 'fl blau'); rechteck(g, X0 + b * s.x / K, 30, b * y / K, 44, 'fl orange');
        if (s.x >= 7000) text(g, X0 + b * s.x / K / 2, 58, z(s.x), 'bt-klein');
        if (y >= 7000) text(g, X0 + b * (s.x + y / 2) / K, 58, z(y), 'bt-klein');
        rechteck(g, X0, 88, 15, 15, 'fl blau'); text(g, X0 + 22, 101, 'x: Sparkonto, 0.75' + NB + '%', 'bt-klein', 'start');
        rechteck(g, X0, 112, 15, 15, 'fl orange');
        text(g, X0 + 22, 125, 'y: Obligation, 2' + NB + '%' + (S.t2 === 1 ? '' : ', nur ½ Jahr'), 'bt-klein', 'start');
        text(g, X0, 162, 'Zins in CHF', 'bt-kopf', 'start');
        var z1 = 0.0075 * s.x, z2 = 0.02 * S.t2 * y;
        rechteck(g, X0, 170, z1 * kz, 34, 'fl blau dunkel'); rechteck(g, X0 + z1 * kz, 170, z2 * kz, 34, 'fl orange dunkel');
        text(g, X0, 234, '0.0075 · x = ' + z(z1, 2), 'bt-klein', 'start');
        text(g, X0, 262, (S.t2 === 1 ? '0.02' : '0.02 · ½') + ' · y = ' + z(z2, 2), 'bt-klein', 'start');
        text(g, X0, 302, 'Zins: ' + z(s.zins, 2) + ' CHF', 'bt gruen', 'start');
        rolle(fig, 'formel').innerHTML = 'Kapital: ' + sp('tx-blau', z(s.x)) + ' + ' + sp('tx-orange', z(y)) + ' = 30' + NB + '000 CHF'
          + '; &nbsp;Zins: 0.0075 · ' + sp('tx-blau', z(s.x)) + ' + ' + (S.t2 === 1 ? '0.02' : '0.02 · ½') + ' · ' + sp('tx-orange', z(y)) + ' = ' + z(s.zins, 2) + ' CHF';
      } else {
        var p = s.p / 100, w = [K2, K2 * (1 + p), K2 * (1 + p) * (1 + p)], X = [30, 165, 300], ky = 0.036, Y0 = 280;
        w.forEach(function(v, k){
          rechteck(g, X[k], Y0 - K2 * ky, 90, K2 * ky, 'fl blau');
          rechteck(g, X[k], Y0 - v * ky, 90, (v - K2) * ky, 'fl gruen dunkel');
          text(g, X[k] + 45, Y0 - v * ky - 8, chf(v), 'bt-klein');
          text(g, X[k] + 45, Y0 + 22, ['Start', 'nach 1 Jahr', 'nach 2 Jahren'][k], 'bt-klein');
          if (k) text(g, X[k] - 22, 36, '· (1 + p)', 'bt-klein', 'middle');
        });
        rolle(fig, 'formel').innerHTML = 'p = ' + z(p) + ' (' + z(s.p, 1) + NB + '%)' + '; &nbsp;5000 → ' + chf(w[1]) + ' → ' + chf(w[2]) + ' CHF'
          + '; &nbsp;Zins in zwei Jahren ' + chf(w[2] - K2) + ' CHF';
      }
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde: Lege fast alles aufs Sparkonto, dann fast alles in die Obligation. Wie ändert sich der Zins?',
        ok: function(s){ return s.merk.wenig && s.merk.viel; } },
      { text: 'Herr Keller möchte 500 CHF Zins nach einem Jahr. Wie viel legt er aufs Sparkonto?', ok: function(s){ return s.art === 'a' && s.x === 8000; } },
      { text: 'Die Obligation läuft jetzt nur ein halbes Jahr. Erreiche 260 CHF Zins.',
        setup: function(){ S.t2 = 0.5; }, ok: function(s){ return s.art === 'a' && s.x === 16000; } },
      { text: 'Zinseszins: Bei welchem Zinssatz werden aus 5000 CHF in zwei Jahren 5202 CHF?',
        setup: function(){ wahlSetzen(fig, 's4-art', 'b'); }, ok: function(s){ return s.art === 'b' && Math.abs(s.p - 2) < 0.05; } },
      { text: 'Bei welchem Zinssatz wächst das Kapital in zwei Jahren um 408 CHF?',
        setup: function(){ wahlSetzen(fig, 's4-art', 'b'); }, ok: function(s){ return s.art === 'b' && Math.abs(s.p - 4) < 0.05; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Bilder zu den Aufgaben: svg.mo-bild[data-bild] ----------
     {"art": "zahl", "z": 3, "e": 6} · {"art": "misch", "x": 30, "p1": 0.2, "y": 10, "p2": 0.6}
     {"art": "rechteck", "x": 4, "a": 18, "y": 8, "b": 7} · {"art": "zins", "x": 12000, "p1": 0.01, "y": 8000, "p2": 0.025} */
  document.querySelectorAll('svg.mo-bild[data-bild]').forEach(function(svg){
    var d = JSON.parse(svg.dataset.bild), g;
    if (d.art === 'zahl'){
      svg.setAttribute('viewBox', '0 0 200 170'); g = el(svg, 'g', {});
      zahlbild(g, 20, 150, d.z, d.e, 'blau', 'orange', 1);
    } else if (d.art === 'misch'){
      svg.setAttribute('viewBox', '0 0 330 200'); g = el(svg, 'g', {});
      var k = 2.6, Y0 = 170;
      [[10, d.x, d.p1, 'blau', 'Sorte 1'], [120, d.y, d.p2, 'orange', 'Sorte 2']].forEach(function(b){
        rechteck(g, b[0], Y0 - 60 * k, 80, 60 * k, 'becher'); rechteck(g, b[0], Y0 - b[1] * k, 80, b[1] * k, 'fuell ' + b[3]);
        rechteck(g, b[0], Y0 - b[1] * b[2] * k, 80, b[1] * b[2] * k, 'stoff ' + b[3]);
        text(g, b[0] + 40, Y0 - b[1] * k - 5, z(b[1]) + ' kg', 'bt-klein'); text(g, b[0] + 40, Y0 + 16, b[4] + ': ' + z(b[2] * 100) + NB + '%', 'bt-klein');
        text(g, b[0] + 40, Y0 - b[1] * b[2] * k / 2 + 4, z(b[1] * b[2]) + ' kg', 'bt-klein hell');
      });
      rechteck(g, 230, Y0 - 60 * k, 80, 60 * k, 'becher'); rechteck(g, 230, Y0 - (d.x + d.y) * k, 80, (d.x + d.y) * k, 'fuell gruen');
      text(g, 270, Y0 + 16, 'Mischung', 'bt-klein'); text(g, 270, Y0 - (d.x + d.y) * k - 5, z(d.x + d.y) + ' kg', 'bt-klein');
    } else if (d.art === 'rechteck'){
      svg.setAttribute('viewBox', '0 0 300 210'); g = el(svg, 'g', {});
      var X0 = 34, Y = 180, kx = 20, ky = 8;
      rechteck(g, X0, Y - d.a * ky, d.x * kx, d.a * ky, 'fl blau'); rechteck(g, X0 + d.x * kx, Y - d.b * ky, d.y * kx, d.b * ky, 'fl orange');
      el(g, 'line', { x1: X0, y1: Y, x2: 290, y2: Y, 'class': 'achse' }); el(g, 'line', { x1: X0, y1: Y, x2: X0, y2: 20, 'class': 'achse' });
      el(g, 'polygon', { points: '296,' + Y + ' 288,' + (Y - 4) + ' 288,' + (Y + 4), 'class': 'pfeil' });
      el(g, 'polygon', { points: X0 + ',14 ' + (X0 - 4) + ',22 ' + (X0 + 4) + ',22', 'class': 'pfeil' });
      for (var t = 0; t <= d.x + d.y; t++) el(g, 'line', { x1: X0 + t * kx, y1: Y, x2: X0 + t * kx, y2: Y + 4, 'class': 'achse' });
      [d.x, d.x + d.y].forEach(function(t){ text(g, X0 + t * kx, Y + 16, String(t), 'skala'); });
      [d.a, d.b].forEach(function(h){ text(g, X0 - 5, Y - h * ky + 4, String(h), 'skala', 'end'); el(g, 'line', { x1: X0, y1: Y - h * ky, x2: X0 + 4, y2: Y - h * ky, 'class': 'achse' }); });
      text(g, 292, Y - 6, 'Anzahl', 'achsname', 'end'); text(g, X0 + 6, 18, 'CHF pro Stück', 'achsname', 'start');
    } else if (d.art === 'zins'){
      svg.setAttribute('viewBox', '0 0 330 170'); g = el(svg, 'g', {});
      var b2 = 280, KK = d.x + d.y;
      text(g, 20, 20, 'Kapital ' + z(KK) + ' CHF', 'bt-klein', 'start');
      rechteck(g, 20, 28, b2 * d.x / KK, 34, 'fl blau'); rechteck(g, 20 + b2 * d.x / KK, 28, b2 * d.y / KK, 34, 'fl orange');
      text(g, 20 + b2 * d.x / KK / 2, 50, z(d.x) + ' zu ' + z(d.p1 * 100) + NB + '%', 'bt-klein');
      text(g, 20 + b2 * (d.x + d.y / 2) / KK, 50, z(d.y) + ' zu ' + z(d.p2 * 100) + NB + '%', 'bt-klein');
      text(g, 20, 96, 'Zins in CHF nach einem Jahr', 'bt-klein', 'start');
      var z1 = d.p1 * d.x, z2 = d.p2 * d.y, kz = 0.6;
      rechteck(g, 20, 104, z1 * kz, 30, 'fl blau dunkel'); rechteck(g, 20 + z1 * kz, 104, z2 * kz, 30, 'fl orange dunkel');
    }
    svg.setAttribute('role', 'img');
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function ri(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }
    /* Eingaben: Zahl, Dezimalkomma, echtes Minus; Brüche wie 1/50. */
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/[\s\u202f]+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/);
      if (m) return { wert: +m[1] / +m[2], komma: komma };
      return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
    }
    var gl = function(a, b){ return Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b)); };
    /* r ist ein Vielfaches (≠ 0) von s: gleichwertige Zeile */
    function prop(r, s){
      var k = -1; for (var i = 0; i < 3; i++) if (Math.abs(s[i]) > 1e-12){ k = i; break; }
      if (k < 0) return false;
      var l = r[k] / s[k]; if (!isFinite(l) || Math.abs(l) < 1e-12) return false;
      for (i = 0; i < 3; i++) if (!gl(r[i], l * s[i])) return false;
      return true;
    }
    function zeilen(e){ return [[e.a1, e.b1, e.c1], [e.a2, e.b2, e.c2]]; }
    function paarOk(e, T1, T2){ var R = zeilen(e); return (prop(R[0], T1) && prop(R[1], T2)) || (prop(R[0], T2) && prop(R[1], T1)); }
    /* welche eingegebene Zeile passt zu keiner richtigen? */
    function falscheZeile(e, T1, T2){ var R = zeilen(e); return [0, 1].filter(function(i){ return !prop(R[i], T1) && !prop(R[i], T2); }); }
    function trifft(e, F){ var R = zeilen(e); return prop(R[0], F) || prop(R[1], F); }
    function ein6(r1, r2){ return { a1: tz(r1[0]), b1: tz(r1[1]), c1: tz(r1[2]), a2: tz(r2[0]), b2: tz(r2[1]), c2: tz(r2[2]) }; }
    /* Zeile a · u + b · v = c in LaTeX, mit Vorzeichen und ohne «1 ·» */
    function glied(k, v, erst){
      if (gl(k, 0)) return '';
      var s = k < 0 ? (erst ? '-' : ' - ') : (erst ? '' : ' + '), a = Math.abs(k);
      return s + (gl(a, 1) ? '' : zt(a) + ' \\cdot ') + v;
    }
    function zeileTex(r, u, v){ var t = glied(r[0], u, true); t += glied(r[1], v, !t); return (t || '0') + ' = ' + zt(r[2]); }
    function sysTex(r1, r2, u, v){ return '\\begin{cases} ' + zeileTex(r1, u, v) + ' \\\\ ' + zeileTex(r2, u, v) + ' \\end{cases}'; }
    function grundTex(a, b, c, v){ var t = glied(a, v + '^2', true); t += glied(b, v, !t); t += (gl(c, 0) ? '' : (c < 0 ? ' - ' : ' + ') + zt(Math.abs(c))); return t + ' = 0'; }
    function poly(a, b, c){ var D = b * b - 4 * a * c, w = Math.sqrt(D); return [(-b + w) / (2 * a), (-b - w) / (2 * a)]; }
    var MUSTER6 = function(u, v){ return 'I: {a1} · ' + u + ' + {b1} · ' + v + ' = {c1}<br>II: {a2} · ' + u + ' + {b2} · ' + v + ' = {c2}'; };

    /* Sperrliste: Keine Zufallsübung würfelt eine feste Aufgabe des Leitprogramms (Clips, Simulationen,
       Kapitelaufgaben, Vortest, Gesamttest) oder ein Beispiel der Themenseite. Schlüssel je Typ. */
    var SPERRE = [
      // ziffern: Zahlen aus Clips (72, 27, 48, 64, 47/74), Aufgaben 1a (49), 1d (36/63), Leiste (50, 71, 82, 93, 85, 38, 45, 54),
      // Gesamttest G1 (69), Themenseite (84, 24)
      'zf|72', 'zf|27', 'zf|48', 'zf|84', 'zf|64', 'zf|47', 'zf|74', 'zf|49', 'zf|36', 'zf|63', 'zf|85', 'zf|38', 'zf|45', 'zf|54',
      'zf|71', 'zf|82', 'zf|93', 'zf|69', 'zf|24', 'zf|50',
      // folge: Clip (Quadratsumme 113), Aufgabe 1c (Abstand 2, 168), Themenseite (72 mit Abstand 1, 84 mit Abstand 5); 145 (frühere G2)
      'fo|qsum|1|113', 'fo|qsum|1|145', 'fo|prod|2|168', 'fo|prod|1|72', 'fo|prod|5|84',
      // art: Gleichungen aus Clips (132, 113, 216, 312, Quersumme 12/36, Quersumme 9/Produkt 14), Aufgabe 1c (168), Leiste (Produkt 20, 5202)
      'ar|n + (n + 1) + (n + 2) = 132', 'ar|n^2 + (n + 1)^2 = 113', 'ar|n^2 + (n + 1)^2 = 145', 'ar|n \\cdot (n + 2) = 168',
      'ar|n \\cdot (n + 6) = 216', 'ar|18 \\cdot x + 12 \\cdot (24 - x) = 312', 'ar|5000 \\cdot (1 + p)^2 = 5202',
      'ar|\\begin{cases} z + e = 12 \\\\ 10 \\cdot e + z = 10 \\cdot z + e + 36 \\end{cases}',
      'ar|\\begin{cases} z + e = 9 \\\\ z \\cdot e = 14 \\end{cases}', 'ar|\\begin{cases} z + e = 9 \\\\ z \\cdot e = 20 \\end{cases}',
      // stoff: Einführung/Themenseite (20 %, 50 %, 30 kg, 30 %), Kontrollclip (60, 85, 50, 70), Leiste
      'st|20|50|30|30', 'st|60|85|50|70', 'st|20|50|24|40', 'st|20|50|24|25', 'st|20|50|30|32', 'st|58|90|40|66',
      // verduennen: Kontrollclip (12 l, 25 % → 10 %), Themenseite und Einführung (2 l, 40 → 16; 5 l, 30 → 12), Leiste (15, 10 → 6)
      'vd|12|25|10', 'vd|2|40|16', 'vd|5|30|12', 'vd|15|10|6',
      // verdunsten: frühere Gesamttestaufgabe (5 kg, 12 % → 20 %)
      'vu|5|12|20',
      // wertbilanz: Einführung, Kontrollclip, Aufgabe 3a, Leiste, Gesamttest G2, Themenseite (Mini-Check 20 Personen, 15 und 9 CHF)
      'wb|12|18|14|188', 'wb|70|30|55|2600', 'wb|150|17|11|2190', 'wb|10|18|14|160', 'wb|30|16|9|382', 'wb|300|22|30|7400', 'wb|40|18|7|500', 'wb|24|18|12|312',
      'wb|20|15|9|252',
      // reihen: Kontrollclip (216 Stühle, 6 mehr)
      'rh|plus|6|216',
      // faktor: Aufgabe 4b, Themenseite (Mini-Checks, A5), Gesamttest G7 (2 % für 9 Monate, 1.2 % ein Jahr), Kontrollclip (2 % ein halbes Jahr)
      'fk|1.8|8', 'fk|0.9|3', 'fk|2.4|5', 'fk|1.5|4', 'fk|2.7|4', 'fk|2|9', 'fk|2|6', 'fk|2.4|6', 'fk|0.6|12', 'fk|1.2|12',
      // zinseszins: Kontrollclip, Einführung/Themenseite A7, frühere Aufgabe 4c, Leiste, Gesamttest G6 (Abhebung)
      'zz|5000|2000|2', 'zz|5000|0|3', 'zz|8000|0|1.5', 'zz|5000|0|2', 'zz|5000|0|4', 'zz|6000|-1000|1'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    var HAND = 'von Hand (oder num-solv)';
    var FACH = { 2: 'Doppelte', 3: 'Dreifache', 4: 'Vierfache', 5: 'Fünffache', 6: 'Sechsfache' };
    var MAL = { 2: 'doppelt', 3: 'dreimal', 4: 'viermal' };

    var TYPEN = {
      /* ── Kapitel 1: Ziffernrätsel in die Grundform für sys-solv ───────────────── */
      'ziffern': { felder: ['a1', 'b1', 'c1', 'a2', 'b2', 'c2'], muster: MUSTER6('z', 'e'),
        schl: function(A){ return 'zf|' + (10 * A.z + A.e); },
        eingabe: function(A){ return ein6(A.T1, A.T2); },
        neu: function(){
          var z_, e_, s1, s2, T1, T2, t1, t2, F = [], k, c;
          do {
            z_ = ri(1, 9); e_ = ri(1, 9); if (z_ === e_) continue;     // e ≠ 0: sonst hiesse die vertauschte Zahl «03»
            var verh = (z_ > 0 && e_ % z_ === 0 && e_ / z_ >= 2 && e_ / z_ <= 4) || (e_ > 0 && z_ % e_ === 0 && z_ / e_ >= 2 && z_ / e_ <= 4);
            s1 = verh && Math.random() < 0.4 ? 'verh' : 'qs';
            s2 = zufall(s1 === 'verh' ? ['tausch', 'vielf'] : ['tausch', 'diff', 'vielf']);
            F = [];
            if (s1 === 'qs'){ T1 = [1, 1, z_ + e_]; t1 = 'Die Quersumme ist ' + (z_ + e_) + '.'; F.push([[10, 1, z_ + e_], 'Quersumme']); }
            else if (e_ > z_){ k = e_ / z_; T1 = [k, -1, 0]; t1 = 'Die Einerziffer ist ' + (MAL[k] || k + '-mal') + ' so gross wie die Zehnerziffer.'; F.push([[1, -k, 0], 'Welche Ziffer']); }
            else { k = z_ / e_; T1 = [1, -k, 0]; t1 = 'Die Zehnerziffer ist ' + (MAL[k] || k + '-mal') + ' so gross wie die Einerziffer.'; F.push([[k, -1, 0], 'Welche Ziffer']); }
            var D = 9 * Math.abs(e_ - z_);
            if (s2 === 'tausch'){
              T2 = [9, -9, 9 * (z_ - e_)];
              t2 = 'Vertauscht man die Ziffern, wird die Zahl um ' + D + (e_ > z_ ? ' grösser.' : ' kleiner.');
              F.push([[9, -9, -9 * (z_ - e_)], 'Richtung'], [[1, -1, 9 * (z_ - e_)], 'Stellenwert']);
            } else if (s2 === 'diff'){
              T2 = [1, -1, z_ - e_];
              t2 = 'Die Zehnerziffer ist um ' + Math.abs(z_ - e_) + (z_ > e_ ? ' grösser' : ' kleiner') + ' als die Einerziffer.';
              F.push([[1, -1, e_ - z_], 'Richtung']);
            } else {
              k = ri(2, 6); c = 10 * z_ + e_ - k * (z_ + e_);
              if (Math.abs(c) > 30) continue;
              T2 = [10 - k, 1 - k, c];
              t2 = c === 0 ? 'Die Zahl ist ' + (MAL[k] || k + '-mal') + ' so gross wie ihre Quersumme.'
                 : 'Die Zahl ist um ' + Math.abs(c) + (c > 0 ? ' grösser' : ' kleiner') + ' als das ' + FACH[k] + ' ihrer Quersumme.';
              if (c !== 0) F.push([[10 - k, 1 - k, -c], 'Richtung']);
              F.push([[1 - k, 1 - k, c], 'Stellenwert']);
            }
            var det = T1[0] * T2[1] - T1[1] * T2[0];
            if (Math.abs(det) < 1e-9) continue;
            break;
          } while (true);
          return { z: z_, e: e_, T1: T1, T2: T2, F: F,
            text: 'Eine zweistellige Zahl: ' + t1 + ' ' + t2 + ' Schreib beide Aussagen als Gleichung in der Form \\(a \\cdot z + b \\cdot e = c\\) (\\(z\\): Zehnerziffer, \\(e\\): Einerziffer) — so tippst du sie in sys-solv.' }; },
        fehler: function(A){
          var aus = [];
          // die falsche Zeile ersetzt die Zeile ihrer Aussage; die andere bleibt richtig
          A.F.forEach(function(f){ var zu1 = f[1] === 'Quersumme' || f[1] === 'Welche Ziffer';
            aus.push([zu1 ? ein6(f[0], A.T2) : ein6(A.T1, f[0]), f[1]]); });
          return aus; },
        pruefen: function(A, e){
          if (paarOk(e, A.T1, A.T2)) return null;
          var R = zeilen(e);
          if (R.some(function(r){ return r.every(function(v){ return gl(v, 0); }); })) return 'In jeder Zeile muss mindestens ein Koeffizient ungleich 0 sein.';
          for (var i = 0; i < A.F.length; i++) if (trifft(e, A.F[i][0])){
            var w = A.F[i][1];
            if (w === 'Richtung') return 'Richtung: Welche Zahl ist die grössere? Der Unterschied kommt zur kleineren Seite dazu.';
            if (w === 'Stellenwert') return 'Stellenwert: Die Zahl ist \\(10 \\cdot z + e\\), vertauscht \\(10 \\cdot e + z\\) — nicht \\(z + e\\).';
            if (w === 'Quersumme') return 'Quersumme heisst Summe der Ziffern: \\(z + e\\), nicht die Zahl \\(10 \\cdot z + e\\).';
            if (w === 'Welche Ziffer') return 'Welche Ziffer ist die grössere? Sie ist das Vielfache der anderen.';
          }
          var f = falscheZeile(e, A.T1, A.T2);
          return 'Gleichung ' + (f.length === 2 ? 'I und II stimmen' : (f[0] === 0 ? 'I stimmt' : 'II stimmt')) + ' noch nicht. Übersetze jede Aussage einzeln und ordne dann: \\(z\\) und \\(e\\) links, die Zahl rechts. Kontrolle: Setz eine Zahl ein, die passen könnte.'; },
        loesung: function(A){ return sysTex(A.T1, A.T2, 'z', 'e') + '\\quad \\text{Zahl } ' + (10 * A.z + A.e); } },

      /* ── Kapitel 1: Zahlenrätsel mit Quadrat, Grundform für poly-solv ─────────── */
      'folge': { felder: ['a', 'b', 'c', 'n'], muster: 'Grundform: {a} · n² + {b} · n + {c} = 0<br>kleinere Zahl: n = {n}',
        schl: function(A){ return 'fo|' + A.t + '|' + A.d + '|' + A.w; },
        eingabe: function(A){ return { a: tz(A.G[0]), b: tz(A.G[1]), c: tz(A.G[2]), n: String(A.n) }; },
        neu: function(){
          var t = zufall(['prod', 'qsum', 'qsum']), n = ri(3, 14), d = t === 'prod' ? ri(1, 6) : (Math.random() < 0.5 ? 1 : ri(2, 5)), G, w, text;
          if (t === 'prod'){ w = n * (n + d); G = [1, d, -w];
            text = 'Zwei natürliche Zahlen unterscheiden sich um ' + d + ', ihr Produkt ist ' + w + '. \\(n\\) ist die kleinere Zahl.'; }
          else { w = n * n + (n + d) * (n + d); G = [2, 2 * d, d * d - w];
            text = d === 1 ? 'Die Summe der Quadrate zweier aufeinanderfolgender natürlicher Zahlen ist ' + w + '. \\(n\\) ist die kleinere Zahl.'
                           : 'Zwei natürliche Zahlen unterscheiden sich um ' + d + '; die Summe ihrer Quadrate ist ' + w + '. \\(n\\) ist die kleinere Zahl.'; }
          return { t: t, n: n, d: d, w: w, G: G, text: text + ' Bring die Gleichung in die Grundform für poly-solv und gib \\(n\\) an.' }; },
        fehler: function(A){
          var f = [], G = A.G, ein = function(g, n){ return { a: tz(g[0]), b: tz(g[1]), c: tz(g[2]), n: String(n) }; };
          f.push([ein([G[0], 0, A.t === 'prod' ? G[2] : -A.w], A.n), A.t === 'prod' ? 'Ausmultiplizieren' : 'Binom']);
          f.push([ein([G[0], G[1], -G[2]], A.n), 'Vorzeichen']);
          f.push([ein(G, -A.n - A.d), 'natürliche']);
          f.push([ein(G, A.n + A.d), 'kleinere']);
          return f; },
        pruefen: function(A, e){
          var r = [e.a, e.b, e.c], G = A.G;
          if (!prop(r, G)){
            if (gl(r[1], 0)) return A.t === 'prod' ? 'Ausmultiplizieren: \\(n \\cdot (n + ' + A.d + ') = n^2 + ' + A.d + ' \\cdot n\\) — das lineare Glied fehlt.'
                                                   : 'Binom: \\((n + ' + A.d + ')^2 = n^2 + ' + (2 * A.d) + ' \\cdot n + ' + (A.d * A.d) + '\\) — das Mittelglied fehlt.';
            if (prop(r, [G[0], G[1], -G[2]])) return 'Vorzeichen: Die Zahl rechts wechselt beim Hinüberbringen das Vorzeichen.';
            if (A.t !== 'prod' && prop(r, [G[0], G[1], -A.w])) return 'Binom: Auch das letzte Glied \\(' + A.d + '^2 = ' + (A.d * A.d) + '\\) gehört dazu.';
            return 'Multipliziere aus, bring alles auf eine Seite und fasse zusammen: \\(a \\cdot n^2 + b \\cdot n + c = 0\\).';
          }
          if (gl(e.n, A.n)) return null;
          if (gl(e.n, -A.n - A.d)) return 'poly-solv liefert zwei Lösungen. Eine negative Zahl ist keine natürliche Zahl.';
          if (gl(e.n, A.n + A.d)) return 'Das ist die grössere Zahl. Gefragt ist die kleinere, \\(n\\).';
          return 'Die Grundform stimmt. Löse sie mit poly-solv und wähle die Lösung, die eine natürliche Zahl ist.'; },
        loesung: function(A){ return grundTex(A.G[0], A.G[1], A.G[2], 'n') + ',\\quad n = ' + A.n + '\\ (\\text{die zweite Lösung } ' + (-A.n - A.d) + ' \\text{ ist keine natürliche Zahl})'; } },

      /* ── Kapitel 1: Gleichungsart und Löser bestimmen (RLP 2.1: den Typ einer Gleichung bestimmen) ── */
      'art': { felder: ['art', 'loeser'],
        muster: 'Gleichungsart: {art:linear|quadratisch|lineares System|quadratisches System}<br>Löser: {loeser:von Hand (oder num-solv)|poly-solv|sys-solv|erst einsetzen, dann poly-solv}',
        schl: function(A){ return 'ar|' + A.tex; },
        eingabe: function(A){ return { art: A.art, loeser: A.loeser }; },
        neu: function(){
          var art = zufall(['linear', 'quadratisch', 'lineares System', 'quadratisches System']), t, a, b, N, x;
          if (art === 'linear') t = zufall([
            function(){ a = ri(12, 30); b = ri(5, a - 3); N = ri(15, 40); x = ri(2, N - 2); return a + ' \\cdot x + ' + b + ' \\cdot (' + N + ' - x) = ' + (a * x + b * (N - x)); },
            function(){ var V = ri(3, 12), p = zufall([0.3, 0.4, 0.25, 0.5]); return zt(p) + ' \\cdot ' + V + ' = ' + zt(p / 2) + ' \\cdot (' + V + ' + w)'; },
            function(){ return 'n + (n + 1) + (n + 2) = ' + (3 * ri(10, 60) + 3); }])();
          else if (art === 'quadratisch') t = zufall([
            function(){ a = ri(3, 15); b = ri(1, 7); return 'n \\cdot (n + ' + b + ') = ' + a * (a + b); },
            function(){ a = ri(2, 9) * 1000; return a + ' \\cdot (1 + p)^2 = ' + zt(Math.round(a * 1.0404 * 100) / 100); },
            function(){ a = ri(4, 15); return 'n^2 + (n + 1)^2 = ' + (a * a + (a + 1) * (a + 1)); }])();
          else if (art === 'lineares System') t = zufall([
            function(){ a = ri(12, 30); b = ri(5, a - 3); N = ri(15, 40); x = ri(2, N - 2); return '\\begin{cases} x + y = ' + N + ' \\\\ ' + a + ' \\cdot x + ' + b + ' \\cdot y = ' + (a * x + b * (N - x)) + ' \\end{cases}'; },
            function(){ a = ri(1, 4); b = a + ri(1, 5); return '\\begin{cases} z + e = ' + (a + b) + ' \\\\ 10 \\cdot e + z = 10 \\cdot z + e + ' + 9 * (b - a) + ' \\end{cases}'; },
            function(){ return '\\begin{cases} 0.02 \\cdot x + 0.03 \\cdot y = ' + ri(3, 9) * 60 + ' \\\\ 0.03 \\cdot x + 0.02 \\cdot y = ' + ri(3, 9) * 60 + ' \\end{cases}'; }])();
          else t = zufall([
            function(){ a = ri(8, 20); b = ri(2, 6) * 6; return '\\begin{cases} x \\cdot y = ' + a * b + ' \\\\ (x - 2) \\cdot (y + ' + ri(2, 8) + ') = ' + a * b + ' \\end{cases}'; },
            function(){ a = ri(1, 4); b = a + ri(1, 5); return '\\begin{cases} z + e = ' + (a + b) + ' \\\\ z \\cdot e = ' + a * b + ' \\end{cases}'; },
            function(){ return '\\begin{cases} m \\cdot p = ' + ri(3, 9) + ' \\\\ (m + ' + ri(5, 20) + ') \\cdot (p - 0.1) = ' + ri(3, 9) + ' \\end{cases}'; }])();
          var L = { 'linear': HAND, 'quadratisch': 'poly-solv', 'lineares System': 'sys-solv', 'quadratisches System': 'erst einsetzen, dann poly-solv' }[art];
          return { art: art, loeser: L, tex: t,
            text: 'Welche Art von Gleichung ist das, und welcher Löser des TI-30X passt? \\(' + t + '\\)' }; },
        fehler: function(A){
          var F = { 'linear': [['quadratisch', 'poly-solv', 'ersten Potenz'], ['lineares System', 'sys-solv', 'Unbekannte']],
                    'quadratisch': [['linear', HAND, 'Quadrat'], ['quadratisches System', 'erst einsetzen, dann poly-solv', 'Unbekannte']],
                    'lineares System': [['quadratisches System', 'erst einsetzen, dann poly-solv', 'multipliziert'], ['linear', HAND, 'Unbekannte']],
                    'quadratisches System': [['lineares System', 'sys-solv', 'Produkt'], ['quadratisch', 'poly-solv', 'Unbekannte']] }[A.art];
          var aus = F.map(function(f){ return [{ art: f[0], loeser: f[1] }, f[2]]; });
          var L2 = { 'linear': 'poly-solv', 'quadratisch': 'sys-solv', 'lineares System': 'poly-solv', 'quadratisches System': 'sys-solv' }[A.art];
          aus.push([{ art: A.art, loeser: L2 }, 'Löser']);
          return aus; },
        pruefen: function(A, e){
          var sys = function(a){ return a.indexOf('System') >= 0; };
          if (e.art !== A.art){
            if (sys(e.art) !== sys(A.art)) return sys(A.art) ? 'Zähle die Unbekannten: zwei Unbekannte, zwei Gleichungen — ein System.' : 'Zähle die Unbekannten: eine Unbekannte, eine Gleichung — kein System.';
            if (A.art === 'quadratisch') return 'Multipliziere aus: Kommt die Unbekannte im Quadrat vor?';
            if (A.art === 'linear') return 'Ausmultipliziert steht die Unbekannte nur in der ersten Potenz.';
            if (A.art === 'quadratisches System') return 'Ein Produkt zweier Unbekannter (wie \\(x \\cdot y\\)) ist nicht linear.';
            return 'In keiner Gleichung werden Unbekannte multipliziert oder quadriert.';
          }
          if (e.loeser === A.loeser) return null;
          // Von Hand geht jede dieser Gleichungen (RLP 2.3 «auch ohne Hilfsmittel», Lösungsformel) — Prüfung 08.10.2026, M7
          if (e.loeser === HAND) return null;
          if (A.art === 'linear') return 'Löser: Eine lineare Gleichung löst du von Hand — ordnen, dann teilen (oder mit num-solv).';
          if (A.art === 'quadratisch') return 'Löser: poly-solv löst \\(a \\cdot x^2 + b \\cdot x + c = 0\\) — zuerst in diese Grundform bringen.';
          if (A.art === 'lineares System') return 'Löser: Für zwei lineare Gleichungen mit zwei Unbekannten gibt es sys-solv (oder du löst von Hand).';
          return 'Löser: sys-solv löst nur lineare Systeme, poly-solv nur eine Unbekannte. Erst einsetzen, dann entsteht eine quadratische Gleichung.'; },
        loesung: function(A){ return '\\text{' + A.art + '; Löser: ' + A.loeser + '}'; } },

      /* ── Kapitel 2: Mengen- und Stoffbilanz in die Grundform ─────────────────── */
      'stoff': { felder: ['a1', 'b1', 'c1', 'a2', 'b2', 'c2'], muster: MUSTER6('x', 'y'),
        schl: function(A){ return 'st|' + A.p1 + '|' + A.p2 + '|' + A.M + '|' + A.p; },
        eingabe: function(A){ return ein6(A.T1, A.T2); },
        neu: function(){
          // Gehalt je Sachzusammenhang (Prüfung 08.10.2026, H4): Kochsalz löst sich nur bis rund 26 %, Flüssigdünger bis rund 30 %
          // Stickstoff, Sirup bis rund 65 % Zucker. p = M ausgeschlossen: Sonst träfe die richtige Mengenbilanz die Falle [1, 1, p] (M2).
          var K = zufall([['Sirup', 'Zucker', 65], ['Legierung', 'Kupfer', 95], ['Salzlösung', 'Salz', 25], ['Düngerlösung', 'Stickstoff', 30]]);
          var p1, p2, x, y, M, P, hoch = K[2] / 5;
          do { p1 = ri(1, hoch - 2) * 5; p2 = ri(p1 / 5 + 2, hoch) * 5; x = ri(2, 30); y = ri(2, 30); M = x + y; P = p1 * x + p2 * y; }
          while (P % M !== 0 || P / M === p1 || P / M === p2 || P / M === M);
          var p = P / M;
          return { p1: p1, p2: p2, M: M, p: p, x: x, y: y, T1: [1, 1, M], T2: [p1 / 100, p2 / 100, p * M / 100],
            text: K[0] + ' 1 enthält ' + p1 + NB + '% ' + K[1] + ', ' + K[0] + ' 2 enthält ' + p2 + NB + '%. Daraus entstehen ' + M + ' kg mit ' + p + NB + '% ' + K[1]
              + '. \\(x\\): Masse von Sorte 1 in kg, \\(y\\): Masse von Sorte 2 in kg. Schreib Mengenbilanz und Stoffbilanz in der Form \\(a \\cdot x + b \\cdot y = c\\).' }; },
        fehler: function(A){ return [
          [ein6(A.T1, [A.p1 / 100, A.p2 / 100, A.p / 100]), 'Stoffmenge'],
          [ein6(A.T1, [A.p1 / 100, A.p2 / 100, A.p * A.M]), 'Einheiten'],
          [ein6(A.T1, [A.p2 / 100, A.p1 / 100, A.p * A.M / 100]), 'Sorte 1'],
          [ein6([1, 1, A.p / 100], A.T2), 'Gesamtmenge']]; },
        pruefen: function(A, e){
          if (paarOk(e, A.T1, A.T2)) return null;
          if (trifft(e, [A.p1, A.p2, A.p])) return 'Rechts steht ein Anteil. In die Stoffbilanz gehört die Stoffmenge der Mischung: Anteil mal Gesamtmenge.';
          if (trifft(e, [A.p1 / 100, A.p2 / 100, A.p * A.M]) || trifft(e, [A.p1, A.p2, A.p * A.M / 100])) return 'Links und rechts verschiedene Einheiten: Prozent und Dezimalzahl gemischt. Beide Seiten in kg Stoff.';
          if (trifft(e, [A.p2, A.p1, A.p * A.M])) return '\\(x\\) ist Sorte 1. Welcher Anteil gehört zu \\(x\\)?';
          if (trifft(e, [1, 1, A.p]) || trifft(e, [1, 1, A.p / 100])) return 'Mengen addieren sich zur Gesamtmenge, nicht zum Anteil.';
          return 'Mengenbilanz: Die Mengen ergeben die Gesamtmenge. Stoffbilanz: Anteil mal Menge, für beide Sorten, ergibt den Stoff der Mischung.'; },
        loesung: function(A){ return sysTex(A.T1, A.T2, 'x', 'y') + '\\quad (x = ' + A.x + ',\\ y = ' + A.y + ')'; } },

      /* ── Kapitel 2: Verdünnen, eine Unbekannte ─────────────────────────────────── */
      'verduennen': { felder: ['w'], muster: 'Wasser: w = {w} l',
        schl: function(A){ return 'vd|' + A.V + '|' + A.p1 + '|' + A.p2; },
        neu: function(){
          var V, p1, p2, w;
          do { V = ri(2, 20); p1 = ri(2, 12) * 5; p2 = ri(1, p1 - 1); w = V * (p1 - p2) / p2; } while (Math.abs(w * 2 - Math.round(w * 2)) > 1e-9 || w > 80 || V * p1 / p2 === w);
          return { V: V, p1: p1, p2: p2, w: w,
            text: V + ' l Konzentrat enthalten ' + p1 + NB + '% Wirkstoff. Wie viele Liter Wasser \\(w\\) muss man dazugeben, damit die Mischung nur noch ' + p2 + NB + '% Wirkstoff enthält?' }; },
        fehler: function(A){ return [[{ w: String(A.V * A.p1 / A.p2) }, 'Mischung'], [{ w: String(A.w + 1) }, 'vorher']]; },
        pruefen: function(A, e){
          if (gl(e.w, A.w)) return null;
          if (gl(e.w, A.V * A.p1 / A.p2)) return 'Das ist die ganze Mischung. \\(w\\) ist nur das Wasser: Die Mischung hat \\(' + A.V + ' + w\\) Liter.';
          return 'Stoff vorher = Stoff nachher: \\(' + zt(A.p1 / 100) + ' \\cdot ' + A.V + ' = ' + zt(A.p2 / 100) + ' \\cdot (' + A.V + ' + w)\\). Wasser bringt keinen Wirkstoff mit.'; },
        loesung: function(A){ return zt(A.p1 / 100) + ' \\cdot ' + A.V + ' = ' + zt(A.p2 / 100) + ' \\cdot (' + A.V + ' + w) \;\\Rightarrow\; w = ' + zt(A.w); } },

      /* ── Kapitel 2: Eindampfen — Wasser verdunstet, eine Unbekannte (Prüfung 08.10.2026, M3: im Gesamttest verlangt) ── */
      'verdunsten': { felder: ['w'], muster: 'verdunstetes Wasser: w = {w} kg',
        schl: function(A){ return 'vu|' + A.V + '|' + A.p1 + '|' + A.p2; },
        neu: function(){
          // Salz löst sich nur bis rund 26 %: Salzlösung bis 25 %, Zuckerlösung bis 60 %. p2 = 2 · p1 nicht: Dann wäre die
          // Masse danach gleich dem verdunsteten Wasser, und die Falle «Masse danach» gälte als richtig.
          var K = zufall([['Salzlösung', 'Salz', 25], ['Zuckerlösung', 'Zucker', 60]]), V, p1, p2, w;
          do { V = ri(4, 40); p1 = ri(1, K[2] / 5 - 1) * 5; p2 = ri(p1 / 5 + 1, K[2] / 5) * 5; w = V * (p2 - p1) / p2; }
          while (Math.abs(w * 2 - Math.round(w * 2)) > 1e-9 || p2 === 2 * p1);
          return { V: V, p1: p1, p2: p2, w: w, stoff: K[1],
            text: V + ' kg ' + K[0] + ' enthalten ' + p1 + NB + '% ' + K[1] + '. Wie viele Kilogramm Wasser \\(w\\) müssen verdunsten, damit die Lösung ' + p2 + NB + '% ' + K[1] + ' enthält?' }; },
        fehler: function(A){ return [[{ w: String(A.V * A.p1 / A.p2) }, 'danach'], [{ w: String(-A.w) }, 'leichter']]; },
        pruefen: function(A, e){
          if (gl(e.w, A.w)) return null;
          if (gl(e.w, A.V * A.p1 / A.p2)) return 'Das ist die Masse danach. \\(w\\) ist das verdunstete Wasser: Danach wiegt die Lösung \\(' + A.V + ' - w\\) kg.';
          if (gl(e.w, -A.w)) return 'Beim Verdunsten wird die Lösung leichter: danach \\(' + A.V + ' - w\\) kg, nicht \\(' + A.V + ' + w\\).';
          return A.stoff + ' vorher = ' + A.stoff + ' nachher: \\(' + zt(A.p1 / 100) + ' \\cdot ' + A.V + ' = ' + zt(A.p2 / 100) + ' \\cdot (' + A.V + ' - w)\\). Es verdunstet nur Wasser.'; },
        loesung: function(A){ return zt(A.p1 / 100) + ' \\cdot ' + A.V + ' = ' + zt(A.p2 / 100) + ' \\cdot (' + A.V + ' - w) \;\\Rightarrow\; w = ' + zt(A.w); } },

      /* ── Kapitel 3: Stück- und Wertbilanz in die Grundform ─────────────────────── */
      'wertbilanz': { felder: ['a1', 'b1', 'c1', 'a2', 'b2', 'c2'], muster: MUSTER6('x', 'y'),
        schl: function(A){ return 'wb|' + A.N + '|' + A.a + '|' + A.b + '|' + A.W; },
        eingabe: function(A){ return ein6(A.T1, A.T2); },
        neu: function(){
          var K = zufall([['Billette', 'Erwachsenenbillette', 'Kinderbillette', 'CHF', 'zu', 30, 8],
                          ['Fahrten', 'Fahrten mit Lastwagen A', 'Fahrten mit Lastwagen B', 't', 'mit je', 25, 6],
                          ['Pakete', 'grosse Pakete', 'kleine Pakete', 'kg', 'zu je', 30, 3]]);
          var a = ri(K[6] + 4, K[5]), b = ri(K[6], a - 2), x = ri(2, 30), y = ri(2, 30);
          return { a: a, b: b, x: x, y: y, N: x + y, W: a * x + b * y, T1: [1, 1, x + y], T2: [a, b, a * x + b * y],
            text: 'Insgesamt ' + (x + y) + ' ' + K[0] + ': ' + K[1] + ' ' + K[4] + ' ' + a + ' ' + K[3] + ', ' + K[2] + ' ' + K[4] + ' ' + b + ' ' + K[3] + '. Zusammen ' + z(a * x + b * y) + ' ' + K[3]
              + '. \\(x\\): Anzahl ' + K[1] + ', \\(y\\): Anzahl ' + K[2] + '. Schreib Stückbilanz und Wertbilanz in der Form \\(a \\cdot x + b \\cdot y = c\\).' }; },
        fehler: function(A){ return [[ein6([1, 1, A.W], [A.a, A.b, A.N]), 'Stückbilanz'], [ein6(A.T1, [A.b, A.a, A.W]), 'gehört']]; },
        pruefen: function(A, e){
          if (paarOk(e, A.T1, A.T2)) return null;
          if (trifft(e, [1, 1, A.W]) || trifft(e, [A.a, A.b, A.N])) return 'Die Stückbilanz zählt Stück, die Wertbilanz den Wert. Welche Zahl gehört rechts in welche Gleichung?';
          if (trifft(e, [A.b, A.a, A.W])) return '\\(x\\) zählt die erste Sorte. Welcher Wert pro Stück gehört zu \\(x\\)?';
          return 'Stückbilanz: Die Anzahlen ergeben zusammen die Gesamtzahl. Wertbilanz: Anzahl mal Wert pro Stück, für beide Sorten, ergibt den Gesamtwert.'; },
        loesung: function(A){ return sysTex(A.T1, A.T2, 'x', 'y') + '\\quad (x = ' + A.x + ',\\ y = ' + A.y + ')'; } },

      /* ── Kapitel 3: Anzahl mal Wert pro Stück, quadratisch ─────────────────────── */
      'reihen': { felder: ['a', 'b', 'c', 'r'], muster: 'Grundform: {a} · r² + {b} · r + {c} = 0<br>Anzahl Reihen: r = {r}',
        schl: function(A){ return 'rh|' + A.t + '|' + A.d + '|' + A.N; },
        eingabe: function(A){ return { a: tz(A.G[0]), b: tz(A.G[1]), c: tz(A.G[2]), r: String(A.r) }; },
        neu: function(){
          var t = zufall(['plus', 'minus', 'doppelt']), r, d, N, G, text, pro;
          if (t === 'plus'){ r = ri(5, 20); d = ri(2, 9); pro = r + d; N = r * pro; G = [1, d, -N];
            text = 'In einem Saal stehen ' + N + ' Stühle in Reihen mit gleich vielen Stühlen. Jede Reihe hat ' + d + ' Stühle mehr, als es Reihen gibt.'; }
          else if (t === 'minus'){ r = ri(8, 25); d = ri(2, 6); pro = r - d; N = r * pro; G = [1, -d, -N];
            text = 'Auf einer Tribüne sind ' + N + ' Plätze in Reihen mit gleich vielen Plätzen. Jede Reihe hat ' + d + ' Plätze weniger, als es Reihen gibt.'; }
          else { r = ri(4, 15); d = ri(1, 6); pro = 2 * r + d; N = r * pro; G = [2, d, -N];
            text = 'In einem Kino gibt es ' + N + ' Plätze in Reihen mit gleich vielen Plätzen. Jede Reihe hat ' + d + ' Plätze mehr als doppelt so viele, wie es Reihen gibt.'; }
          var neg = poly(G[0], G[1], G[2]).filter(function(v){ return !gl(v, r); })[0];
          return { t: t, r: r, d: d, N: N, G: G, pro: pro, neg: neg, text: text + ' Mit \\(r\\): Anzahl Reihen — bring die Gleichung in die Grundform für poly-solv und gib \\(r\\) an.' }; },
        fehler: function(A){
          var G = A.G, ein = function(g, r){ return { a: tz(g[0]), b: tz(g[1]), c: tz(g[2]), r: String(r) }; };
          return [[ein([G[0], G[1], -G[2]], A.r), 'Vorzeichen'], [ein(G, A.pro), 'Anzahl Reihen'], [ein([G[0], -G[1], G[2]], A.r), 'Vorzeichen']]; },
        pruefen: function(A, e){
          var rr = [e.a, e.b, e.c], G = A.G;
          if (!prop(rr, G)){
            if (prop(rr, [G[0], G[1], -G[2]]) || prop(rr, [G[0], -G[1], G[2]])) return 'Vorzeichen: Prüfe, welches Glied mit Minus nach links kommt — und «mehr» oder «weniger» in der Klammer.';
            return 'Anzahl Reihen mal Plätze pro Reihe ergibt alle Plätze. Ausmultiplizieren, alles auf eine Seite: \\(a \\cdot r^2 + b \\cdot r + c = 0\\).';
          }
          if (gl(e.r, A.r)) return null;
          if (gl(e.r, A.pro)) return 'Das sind die Plätze pro Reihe. Gefragt ist die Anzahl Reihen.';
          if (e.r < 0) return 'Eine Anzahl Reihen ist nie negativ. Welche Lösung von poly-solv passt?';
          return 'Die Grundform stimmt. Löse mit poly-solv und wähle die Lösung, die eine Anzahl sein kann.'; },
        loesung: function(A){ return grundTex(A.G[0], A.G[1], A.G[2], 'r') + ',\\quad r = ' + A.r + '\\ (\\text{die zweite Lösung } ' + zt(Math.round(A.neg * 100) / 100) + ' \\text{ ist keine Anzahl})'; } },

      /* ── Kapitel 4: Faktor vor dem Kapital (Zinssatz mal Zeitanteil) ───────────── */
      'faktor': { felder: ['f'], muster: 'Faktor vor dem Kapital: {f}',
        schl: function(A){ return 'fk|' + A.p + '|' + A.m; },
        neu: function(){
          // nicht 1 Monat: «Monate nicht durch 12» und «Zeitanteil vergessen» gäben dieselbe Zahl
          var p, m, f;
          do { p = zufall([0.6, 0.8, 0.9, 1.2, 1.5, 1.8, 2, 2.4, 2.5, 3, 3.6]); m = zufall([2, 3, 4, 6, 8, 9, 12]); f = p / 100 * m / 12; }
          while (Math.abs(f * 1e6 - Math.round(f * 1e6)) > 1e-6);
          f = Math.round(f * 1e6) / 1e6;
          var dauer = m === 12 ? 'ein ganzes Jahr' : m === 6 ? 'ein halbes Jahr' : m + (m === 1 ? ' Monat' : ' Monate');
          return { p: p, m: m, f: f, text: 'Ein Kapital \\(x\\) liegt ' + dauer + ' zu ' + z(p) + NB + '%. Welcher Faktor steht in der Zinsgleichung vor \\(x\\)? (Dezimalzahl)' }; },
        fehler: function(A){
          var f = [[{ f: String(Math.round(A.p * A.m / 12 * 1e6) / 1e6) }, 'Dezimalzahl']];
          if (A.m !== 12) f.push([{ f: String(Math.round(A.p / 100 * A.m * 1e6) / 1e6) }, 'Jahren'], [{ f: String(A.p / 100) }, 'Zeitanteil']);
          return f; },
        pruefen: function(A, e){
          if (gl(e.f, A.f)) return null;
          if (gl(e.f, A.p * A.m / 12) || gl(e.f, A.p)) return 'Zinssatz als Dezimalzahl: ' + z(A.p) + NB + '% sind ' + z(A.p / 100) + '.';
          if (gl(e.f, A.p / 100 * A.m)) return 'Die Zeit zählt in Jahren: ' + A.m + ' Monate sind \\(\\tfrac{' + A.m + '}{12}\\) Jahr.';
          if (gl(e.f, A.p / 100)) return 'Der Zeitanteil fehlt: Das Kapital liegt nicht ein ganzes Jahr.';
          return 'Faktor = Zinssatz als Dezimalzahl mal Zeit in Jahren.'; },
        loesung: function(A){ return zt(A.p / 100) + ' \\cdot ' + (A.m === 12 ? '1' : '\\tfrac{' + A.m + '}{12}') + ' = ' + zt(A.f); } },

      /* ── Kapitel 4: Zinseszins in die Grundform für poly-solv ─────────────────── */
      'zinseszins': { felder: ['a', 'b', 'c', 'p'], muster: 'Grundform: {a} · p² + {b} · p + {c} = 0<br>Zinssatz: p = {p}',
        schl: function(A){ return 'zz|' + A.K + '|' + A.E + '|' + A.pp; },
        eingabe: function(A){ return { a: tz(A.G[0]), b: tz(A.G[1]), c: tz(A.G[2]), p: String(A.p) }; },
        neu: function(){
          var K, E, pp, S;
          // E ≠ K: sonst gäben «Binom vergessen» (b = K + E) und «E · (1 + p) vergessen» (b = 2 · K) dieselbe Zahl.
          // E < 0 ist eine Abhebung (wie Gesamttest G6, Prüfung 08.10.2026: dort verlangt, hier geübt); E ≠ −K, sonst b = K + E = 0.
          do { K = ri(2, 9) * 1000; E = zufall([0, 0, 1000, 2000, 3000, -1000, -2000]); pp = zufall([1, 1.5, 2, 2.5, 3, 4, 5]);
               S = K * (1 + pp / 100) * (1 + pp / 100) + E * (1 + pp / 100); }
          while (E === K || E === -K || Math.abs(S * 100 - Math.round(S * 100)) > 1e-6);
          S = Math.round(S * 100) / 100;
          var p = pp / 100, G = [K, 2 * K + E, Math.round((K + E - S) * 100) / 100];
          return { K: K, E: E, pp: pp, p: p, S: S, G: G, neg: poly(G[0], G[1], G[2])[1],
            text: (E > 0 ? z(K) + ' CHF werden eingezahlt, nach einem Jahr nochmals ' + z(E) + ' CHF.'
                   : E < 0 ? z(K) + ' CHF werden eingezahlt; nach einem Jahr werden ' + z(-E) + ' CHF abgehoben.'
                   : z(K) + ' CHF liegen zwei Jahre auf einem Konto.')
              + ' Der Zins wird mitverzinst, der Zinssatz bleibt gleich. Nach zwei Jahren sind es ' + z(S, 2) + ' CHF. Bring die Gleichung für den Zinssatz \\(p\\) (Dezimalzahl) in die Grundform und gib \\(p\\) an.' }; },
        fehler: function(A){
          var G = A.G, ein = function(g, p){ return { a: tz(g[0]), b: tz(g[1]), c: tz(g[2]), p: String(p) }; }, f = [];
          f.push([ein([G[0], A.K + A.E, G[2]], A.p), 'Binom']);
          if (A.E) f.push([ein([G[0], 2 * A.K, G[2]], A.p), 'Glied mit p'], [ein([G[0], G[1], Math.round((A.K - A.S) * 100) / 100], A.p), A.E > 0 ? 'Einzahlung' : 'Abhebung']);
          f.push([ein([G[0], G[1], -G[2]], A.p), 'Vorzeichen'], [ein(G, A.pp), 'Dezimalzahl'], [ein(G, Math.round(A.neg * 1e6) / 1e6), 'passt nicht']);
          return f; },
        pruefen: function(A, e){
          var r = [e.a, e.b, e.c], G = A.G;
          if (!prop(r, G)){
            if (prop(r, [G[0], A.K + A.E, G[2]])) return 'Binom: \\((1 + p)^2 = 1 + 2 \\cdot p + p^2\\) — das Glied \\(2 \\cdot ' + z(A.K) + ' \\cdot p\\) fehlt.';
            if (A.E && prop(r, [G[0], 2 * A.K, G[2]])) return 'Auch \\(' + (A.E > 0 ? A.E : '-' + (-A.E)) + ' \\cdot (1 + p)\\) liefert ein Glied mit p.';
            if (A.E && prop(r, [G[0], G[1], A.K - A.S])) return (A.E > 0 ? 'Die Einzahlung' : 'Die Abhebung') + ' steht auch ohne p da: Sie gehört ins konstante Glied \\(c\\).';
            if (prop(r, [G[0], G[1], -G[2]])) return 'Vorzeichen: Der Endbetrag kommt mit Minus nach links.';
            return 'Multipliziere \\((1 + p)^2\\) aus, bring alles auf eine Seite und fasse zusammen: \\(a \\cdot p^2 + b \\cdot p + c = 0\\).';
          }
          if (gl(e.p, A.p)) return null;
          if (gl(e.p, A.pp)) return 'p als Dezimalzahl: ' + z(A.pp) + NB + '% sind ' + z(A.p) + '.';
          // nur bei der zweiten Lösung von poly-solv (unter −100 %), nicht bei jeder negativen Eingabe (Prüfung 08.10.2026, M1)
          if (e.p <= -1) return 'Diese Lösung von poly-solv passt nicht: Einen Zinssatz unter −100 % gibt es nicht.';
          if (gl(e.p, -A.p)) return 'Vorzeichen: Das Kapital wächst, der Zinssatz ist positiv. Welche Lösung zeigt poly-solv?';
          return 'Die Grundform stimmt. Löse mit poly-solv und wähle die Lösung, die ein Zinssatz sein kann.'; },
        loesung: function(A){ return grundTex(A.G[0], A.G[1], A.G[2], 'p') + ',\\quad p = ' + zt(A.p) + ' = ' + z(A.pp) + '\\,\\%'; } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        // Trifft der Wurf eine feste Aufgabe des Leitprogramms, wird neu gewürfelt (SPERRE oben).
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
        if (geloest) return;   // nach ✓ zählt erst die nächste Aufgabe
        var e = {}, leer_ = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer_ = true; });
        ein.querySelectorAll('input').forEach(function(i){
          var r = lesen(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer_ = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer_){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('input') ? 'Fülle alle Felder aus — auch Koeffizienten 0 oder 1.' : 'Wähle aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen mit Dezimalpunkt, zum Beispiel <code>0.02</code>, <code>-36</code> oder <code>1/50</code>.'; return; }
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
