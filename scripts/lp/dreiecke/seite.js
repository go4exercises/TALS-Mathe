<script>
/* Leitprogramm Dreiecke — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit Rückmeldung, Figuren zu den
   Aufgaben. Gerüst (Flaeche, Leiste, arbeitsbereich, Übungsrahmen) wie in den Leitprogrammen Planimetrie und
   Trigonometrische Berechnungen (scripts/lp/planimetrie/seite.js, scripts/lp/trigonometrische-berechnungen/seite.js),
   Inhalte neu. Notation wie auf der Themenseite 5.2a: Ecken A, B, C gegen den Uhrzeigersinn, Seite a gegenüber A,
   Winkel α bei A, Aussenwinkel α′, Höhen h_a, h_b, h_c, Winkelhalbierende w_α, Seitenmitten M_a, M_b, M_c,
   Schnittpunkte H, S, M_I, M_U; Fläche A = ½ g h. Die Seitenhalbierende heisst hier s_c (die Themenseite gibt ihr
   kein Zeichen; wie im Leitprogramm Planimetrie).
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Figur · orange = Element, Hilfslinie (in Kapitel 1: der
   Winkel α) · grün = Gesuchtes, Ergebnis, Schnittpunkt (in Kapitel 1: der Winkel β) · rot = Fehler.
   Dezimalpunkt; gerundet mit «≈». */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', PI = Math.PI;
  function z(n, st){ var f = Math.pow(10, st == null ? 2 : st), r = Math.round(n * f) / f; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  /* gerundete Werte mit «≈» und fester Stellenzahl, exakte mit «=» */
  function zz(v, st){ st = st == null ? 2 : st; var f = Math.pow(10, st), r = Math.round(v * f) / f;
    if (Math.abs(v - r) <= 1e-9) return '= ' + z(v, st);
    return '\\approx ' + (r < 0 ? '−' : '') + Math.abs(r).toFixed(st); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function gl(a, b){ return Math.abs(a - b) < 1e-9; }
  function zahl(s){
    var komma = /\d,\d/.test(s);
    s = String(s).trim().replace(/−/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^≈/, '').replace(/°$/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  /* Vergleich gerundeter Ergebnisse: richtig auf zwei Dezimalen (Toleranz 0.006); «nah» heisst: richtig gerechnet,
     aber zu grob gerundet. */
  function stimmt(e, soll, tol){ return Math.abs(e - soll) <= (tol || 0.006) + 1e-9; }
  function nah(e, soll, tol){ return !stimmt(e, soll, tol) && Math.abs(e - soll) <= Math.max(0.06, Math.abs(soll) * 0.005); }
  var RUNDEN = 'Fast — runde auf zwei Dezimalen (Zwischenresultate ungerundet weiterverwenden).';
  function grad(w){ return w * PI / 180; }
  function sinG(w){ return Math.sin(grad(w)); } function cosG(w){ return Math.cos(grad(w)); }

  /* ---------- Geometrie ---------- */
  function lot(p, a, b){   // Fusspunkt des Lots von p auf die Gerade ab, dazu der Parameter t (0 … 1 = auf der Strecke)
    var dx = b[0] - a[0], dy = b[1] - a[1], t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy);
    return [a[0] + t * dx, a[1] + t * dy, t];
  }
  function abst(p, q){ return Math.hypot(p[0] - q[0], p[1] - q[1]); }
  function winkel(p, a, b){   // Innenwinkel bei p zwischen pa und pb, Grad
    var u = [a[0] - p[0], a[1] - p[1]], v = [b[0] - p[0], b[1] - p[1]];
    return Math.acos(Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]))))) * 180 / PI;
  }
  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function richtung(p, q){ return Math.atan2(q[1] - p[1], q[0] - p[0]); }
  function schnitt(p, d, q, e){
    var det = d[0] * (-e[1]) - d[1] * (-e[0]);
    var s = ((q[0] - p[0]) * (-e[1]) - (q[1] - p[1]) * (-e[0])) / det;
    return [p[0] + s * d[0], p[1] + s * d[1]];
  }
  function wfuss(C, A, B){ var ca = abst(C, A), cb = abst(C, B); return [A[0] + (B[0] - A[0]) * ca / (ca + cb), A[1] + (B[1] - A[1]) * ca / (ca + cb)]; }
  /* Höhenschnittpunkt, Schwerpunkt, Inkreis- und Umkreismittelpunkt mit Radien (wie geom.py der Bauskripte) */
  function besondere(A, B, C){
    var fa = lot(A, B, C), fb = lot(B, A, C);
    var H = schnitt(A, [fa[0] - A[0], fa[1] - A[1]], B, [fb[0] - B[0], fb[1] - B[1]]);
    var S = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
    var a = abst(B, C), b = abst(C, A), c = abst(A, B), u = a + b + c;
    var MI = [(a * A[0] + b * B[0] + c * C[0]) / u, (a * A[1] + b * B[1] + c * C[1]) / u];
    var mc = mitte(A, B), mb = mitte(A, C);
    var MU = schnitt(mc, [-(B[1] - A[1]), B[0] - A[0]], mb, [-(C[1] - A[1]), C[0] - A[0]]);
    var s = u / 2, ri = Math.sqrt(s * (s - a) * (s - b) * (s - c)) / s;
    return { H: H, S: S, MI: MI, MU: MU, ri: ri, ru: abst(MU, A) };
  }
  /* Art nach Winkeln: Toleranz gegen Rundung der Lage (Reglerwerte auf halben Zentimetern) */
  function artWinkel(w){ var m = Math.max(w[0], w[1], w[2]); return m > 90 + 1e-6 ? 'stumpfwinklig' : Math.abs(m - 90) <= 1e-6 ? 'rechtwinklig' : 'spitzwinklig'; }

  /* ---------- Zeichenfläche in Weltkoordinaten (1 Einheit = 1 cm, beide Achsen gleich) ---------- */
  function Flaeche(svg, o){
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, s = W / (x1 - x0), y1 = o.y0 + H / s, y0 = o.y0;
    function X(x){ return (x - x0) * s; }
    function Y(y){ return H - (y - y0) * s; }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    var g = el(svg, 'g', {}), i, schritt = o.karo || 1;
    if (o.karo !== false){
      for (i = Math.ceil(x0 / schritt) * schritt; i <= x1; i += schritt) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
      for (i = Math.ceil(y0 / schritt) * schritt; i <= y1; i += schritt) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    }
    var ebene = el(svg, 'g', {});
    var rot = 0, dreh = function(p){ if (!rot) return p; var c = Math.cos(rot), sn = Math.sin(rot), m = o.drehpunkt || [0, 0];
      return [m[0] + (p[0] - m[0]) * c - (p[1] - m[1]) * sn, m[1] + (p[0] - m[0]) * sn + (p[1] - m[1]) * c]; };
    function P(p){ p = dreh(p); return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }
    var F = {
      s: s, ebene: ebene, x0: x0, x1: x1, y0: y0, y1: y1,
      drehen: function(w){ rot = w; },
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      vieleck: function(pts, cls){ return el(ebene, 'polygon', { points: pts.map(P).join(' '), 'class': cls }); },
      strecke: function(a, b, cls){ var A = dreh(a), B = dreh(b); return el(ebene, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': cls }); },
      gerade: function(a, b, cls){   // ganze Gerade durch a und b, am Bild abgeschnitten
        var dx = b[0] - a[0], dy = b[1] - a[1], L = 100 / Math.hypot(dx, dy);
        return F.strecke([a[0] - dx * L, a[1] - dy * L], [a[0] + dx * L, a[1] + dy * L], cls); },
      strahl: function(a, w, cls){ return F.strecke(a, [a[0] + 100 * Math.cos(w), a[1] + 100 * Math.sin(w)], cls); },
      kreis: function(m, r, cls){ var M = dreh(m); return el(ebene, 'circle', { cx: X(M[0]), cy: Y(M[1]), r: r * s, 'class': cls }); },
      /* Winkel um m von Richtung w0 bis w1 (Bogenmass, gegen den Uhrzeigersinn), Radius in Pixeln; gefüllt = Sektor */
      bogen: function(m, w0, w1, rpx, cls, gefuellt){
        var r = rpx / s, a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var A = dreh(a), B = dreh(b), M = dreh(m), gross = (w1 - w0) > PI ? 1 : 0;
        var d = (gefuellt ? 'M' + X(M[0]) + ' ' + Y(M[1]) + ' L' : 'M') + X(A[0]) + ' ' + Y(A[1]) + ' A' + rpx + ' ' + rpx + ' 0 ' + gross + ' 0 ' + X(B[0]) + ' ' + Y(B[1]) + (gefuellt ? ' Z' : '');
        return el(ebene, 'path', { d: d, 'class': cls }); },
      punkt: function(p, cls){ var A = dreh(p); return el(ebene, 'circle', { cx: X(A[0]), cy: Y(A[1]), r: 3.5, 'class': cls || 'g-pkt' }); },
      text: function(p, t, cls, dx, dy, anker){ var A = dreh(p);
        return el(ebene, 'text', { x: X(A[0]) + (dx || 0), y: Y(A[1]) + (dy || 0), 'text-anchor': anker || 'middle', 'class': 'g-text ' + (cls || '') }, t); },
      /* Name mit tiefgestelltem Index (h_c, M_U): ein text mit tspan */
      name: function(p, t, idx, cls, dx, dy, anker){ var e = F.text(p, t, cls, dx, dy, anker);
        if (idx){ var ts = el(e, 'tspan', { dy: 4, 'font-size': '0.72em' }, idx); } return e; },
      rechts: function(fuss, r1, r2, cls){   // Zeichen für den rechten Winkel, Richtungen als Vektoren
        var q = 9 / s, n1 = Math.hypot(r1[0], r1[1]), n2 = Math.hypot(r2[0], r2[1]);
        var u = [r1[0] / n1 * q, r1[1] / n1 * q], v = [r2[0] / n2 * q, r2[1] / n2 * q];
        return el(ebene, 'polyline', { points: [P([fuss[0] + u[0], fuss[1] + u[1]]), P([fuss[0] + u[0] + v[0], fuss[1] + u[1] + v[1]]), P([fuss[0] + v[0], fuss[1] + v[1]])].join(' '), 'class': 'g-rechts ' + (cls || '') }); },
      /* Kandidat zum Antippen: sichtbare Linie plus breiter, unsichtbarer Treffstreifen. */
      kandidat: function(id, a, b, wahl, ganz){
        var gr = el(ebene, 'g', { 'class': 'kandidat', tabindex: 0, role: 'button', 'aria-label': 'Linie ' + id, 'data-id': id });
        var A = dreh(a), B = dreh(b);
        if (ganz){ var dx = B[0] - A[0], dy = B[1] - A[1], L = 100 / Math.hypot(dx, dy); A = [A[0] - dx * L, A[1] - dy * L]; B = [B[0] + dx * L, B[1] + dy * L]; }
        el(gr, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': 'k-sicht' });
        el(gr, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': 'k-treffer' });
        gr.addEventListener('click', function(){ wahl(id); });
        gr.addEventListener('keydown', function(ev){ if (ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); wahl(id); } });
        return gr; }
    };
    return F;
  }
  /* Winkel bei p zwischen den Richtungen zu a und zu b (der kleinere), Beschriftung auf der Winkelhalbierenden. */
  function winkelMarke(F, p, a, b, rpx, cls, text, tcls, gefuellt){
    var w0 = richtung(p, a), w1 = richtung(p, b);
    while (w1 < w0) w1 += 2 * PI;
    if (w1 - w0 > PI){ var t = w0; w0 = w1; w1 = t + 2 * PI; }
    F.bogen(p, w0, w1, rpx, cls, gefuellt);
    if (text){ var wm = (w0 + w1) / 2, r = (rpx + 12) / F.s;
      F.text([p[0] + r * Math.cos(wm), p[1] + r * Math.sin(wm)], text, tcls || 'winkel', 0, 4); }
  }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ---------- */
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
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; inp.disabled = false; });
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

  /* ---------- Geometrie-Arbeitsbereich (wie in den Leitprogrammen Planimetrie und Trig. Berechnungen) ----------
     Unterschied zu den Animationen der Themenseite 5.2a: Dort zeigt eine Animation eine Beziehung, frei bedienbar.
     Hier trägt die Figur Aufgaben: Figur verändern (Regler), Linie antippen (Kandidaten mit eigener Rückmeldung),
     Grösse berechnen und eingeben. Gefragte Werte stehen nicht im Bild, bevor die Antwort stimmt.
     arbeitsbereich(id, { fenster, zeichnen(F, w, k), aufgaben }) — jede Aufgabe:
       text, setup(sim) (Regler setzen: sim.setze({ t: 10 }), sim.sperre('t')),
       wahl: { richtig, gut, rueck: { id: 'Text' } }            — Linie antippen
       frage: [{ name, label, einheit, soll, tol, fehler: [[wert, 'Text']], tipp }] — Grössen eingeben
       ziel: function(w) — Reglerzustand (w.bewegt); probe: ein Zustand, der es löst (für pruef-geo)
       fest: { … } — Werte, die die Figur statt der Regler zeigt; verdeckt: Regler, deren Wert «?» zeigt */
  function arbeitsbereich(id, o){
    var fig = document.getElementById(id); if (!fig) return;
    var F = Flaeche(fig.querySelector('svg'), o.fenster), regler = {}, bewegt = {}, aufgabe = null, gewaehlt = null, richtig = false, pruefen = function(){};
    var ein = fig.querySelector('.g-eingabe'), rueck = fig.querySelector('.g-rueck'), formel = fig.querySelector('[data-rolle="formel"]');
    fig.querySelectorAll('input[type=range]').forEach(function(inp){
      regler[inp.dataset.p] = inp;
      inp.addEventListener('input', function(){ bewegt[inp.dataset.p] = true; zeichnen(); });
    });
    function werte(){
      var w = { bewegt: bewegt };
      for (var k in regler) w[k] = +regler[k].value;
      return w;
    }
    function anzeigen(w){
      var verdeckt = (aufgabe && aufgabe.verdeckt) || [];
      for (var k in regler){ var sv = regler[k].parentNode.querySelector('.sl-val'); if (!sv) continue;
        sv.textContent = verdeckt.indexOf(k) >= 0 ? '?' : z(w[k]) + (regler[k].dataset.einheit || ''); }
    }
    function meldung(cls, html){ rueck.className = 'g-rueck ' + cls; rueck.innerHTML = html; setzen(rueck); }
    function wahl(kid){
      if (!aufgabe || !aufgabe.wahl || richtig) return;
      gewaehlt = kid;
      if (kid === aufgabe.wahl.richtig){ richtig = true; meldung('richtig', '✓ ' + (aufgabe.wahl.gut || 'Richtig.')); }
      else meldung('falsch', (aufgabe.wahl.rueck || {})[kid] || 'Das ist nicht die gesuchte Linie.');
      zeichnen();
    }
    function eingabeZeigen(){
      ein.innerHTML = '';
      if (!aufgabe || !aufgabe.frage){ ein.hidden = true; return; }
      ein.hidden = false;
      ein.innerHTML = aufgabe.frage.map(function(f){
        return '<label class="g-feld"><span>' + f.label + '</span><input type="text" inputmode="decimal" autocomplete="off" data-n="' + f.name + '" aria-label="' + f.name + '"><span>' + (f.einheit || '') + '</span></label>';
      }).join('') + '<button type="button" class="g-pruefen">Prüfen</button>';
      ein.querySelector('.g-pruefen').addEventListener('click', eingabePruefen);
      ein.querySelectorAll('input').forEach(function(i){ i.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') eingabePruefen(); }); });
      setzen(ein);
    }
    function eingabePruefen(){
      if (richtig) return;
      var r = [], alle = true, komma = false;
      for (var q = 0; q < aufgabe.frage.length; q++){
        var f = aufgabe.frage[q], inp = ein.querySelector('[data-n="' + f.name + '"]'), e = zahl(inp.value);
        if (e.leer) return meldung('hinweis', 'Fülle alle Felder aus.');
        if (isNaN(e.wert)) return meldung('hinweis', 'Eine Zahl wie <code>12</code> oder <code>4.8</code> — ohne Einheit.');
        if (e.komma) komma = true;
        if (stimmt(e.wert, f.soll, f.tol)) continue;
        alle = false;
        var t = null;
        (f.fehler || []).forEach(function(fe){ if (!t && stimmt(e.wert, fe[0], f.tol)) t = fe[1]; });
        r.push(t || (nah(e.wert, f.soll, f.tol) ? RUNDEN : f.tipp || 'Noch nicht. Rechne nach.'));
      }
      if (alle){ richtig = true; meldung('richtig', '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + '.' + (aufgabe.loesung ? ' ' + aufgabe.loesung : '')); zeichnen(); }
      else meldung('falsch', r.join(' '));
    }
    var sim = {
      F: F,
      zustand: function(){ var w = werte(); w.gewaehlt = gewaehlt; w.richtig = richtig; return w; },
      zeichnen: zeichnen,
      setze: function(werteNeu){ for (var k in werteNeu) regler[k].value = werteNeu[k]; },
      sperre: function(){ for (var j = 0; j < arguments.length; j++) regler[arguments[j]].disabled = true; },
      aufgabe: function(a){ aufgabe = a; gewaehlt = null; richtig = false; rueck.className = 'g-rueck'; rueck.innerHTML = ''; eingabeZeigen(); zeichnen(); },
      aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; aufgabe = null; gewaehlt = null; richtig = false; F.drehen(0); rueck.className = 'g-rueck'; rueck.innerHTML = ''; eingabeZeigen(); }
    };
    function zeichnen(){
      var w = werte(); w.gewaehlt = gewaehlt; w.richtig = richtig;
      if (aufgabe && aufgabe.fest) for (var fk in aufgabe.fest) w[fk] = aufgabe.fest[fk];
      anzeigen(w);
      F.leeren();
      var text = o.zeichnen(F, w, { aufgabe: aufgabe, wahl: aufgabe && aufgabe.wahl ? wahl : null });
      // Formeln nur neu setzen, wenn sich der Text geändert hat (Regler feuern viele Ereignisse)
      if (formel && formel.__text !== text){ formel.__text = text; formel.innerHTML = text || ''; setzen(formel); }
      pruefen();
    }
    pruefen = Leiste(fig, o.aufgaben.map(function(a){
      return { text: a.text,
        setup: function(s){ if (a.setup) a.setup(s); s.aufgabe(a); },
        ok: function(w){ return (a.wahl || a.frage) ? w.richtig : a.ziel(w); } }; }), sim);
    fig.__sim = sim; fig.__aufgaben = o.aufgaben;     // Testhaken
    zeichnen();
  }

  function ecken(F, E, namen){   // Ecken mit Namen, je vom Schwerpunkt weg nach aussen
    var S = [(E[0][0] + E[1][0] + E[2][0]) / 3, (E[0][1] + E[1][1] + E[2][1]) / 3];
    E.forEach(function(p, i){ var d = [p[0] - S[0], p[1] - S[1]], n = Math.hypot(d[0], d[1]) || 1, r = 14 / F.s;
      F.punkt(p); F.text([p[0] + d[0] / n * r, p[1] + d[1] / n * r], namen[i], 'ecke', 0, 5); });
  }

  /* ---------- Kapitel 1: Winkel im Dreieck ----------
     Unterschied zur Animation «Allgemeines Dreieck» der Themenseite: Dort zieht man die Ecken und liest die Winkel ab.
     Hier stellt man α und β ein (Schritt 5°), das Dreieck entsteht aus den beiden Schenkeln über AB, γ wird an der Figur
     gemessen. So lassen sich Zielspiele stellen (rechtwinklig bei C, gleichschenklig, die Grenze α + β < 180°), und der
     Fall «kein Dreieck» wird sichtbar. Die Figur passt ihre Grösse dem Bild an — für Winkel spielt die Grösse keine Rolle.
     Startwert α = 50°, β = 60° wie im Einführungsclip (Themenseite, Mini-Check). Farben: α orange, β grün, γ Tinte. */
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 230, x0: 0, x1: 10, y0: 0, karo: false },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, al = w.al, be = w.be, vd = Au.verdeckt || [];
      if (al + be >= 180){
        var A0 = [1.2, 1.4], B0 = [8.8, 1.4];
        F.strecke(A0, B0, 'figur-linie');
        F.strahl(A0, grad(al), 'strahl'); F.strahl(B0, grad(180 - be), 'strahl');
        winkelMarke(F, A0, B0, [A0[0] + Math.cos(grad(al)), A0[1] + Math.sin(grad(al))], 30, 'w-a', null, null, true);
        winkelMarke(F, B0, [B0[0] + Math.cos(grad(180 - be)), B0[1] + Math.sin(grad(180 - be))], A0, 30, 'w-b', null, null, true);
        F.text(A0, 'A', 'ecke', -10, 16); F.text(B0, 'B', 'ecke', 10, 16);
        return '\\(\\alpha + \\beta = ' + (al + be) + '° \\geq 180°\\): Die Schenkel treffen sich nicht — kein Dreieck.';
      }
      // Dreieck aus AB = 1 und den Winkeln, dann ins Bild eingepasst
      var t = sinG(be) / sinG(al + be), roh = [[0, 0], [1, 0], [t * cosG(al), t * sinG(al)]];
      var xs = roh.map(function(p){ return p[0]; }), ys = roh.map(function(p){ return p[1]; });
      if (Au.aussen) xs.push(roh[2][0] + 0.35 * cosG(al));
      var bx0 = Math.min.apply(null, xs), bx1 = Math.max.apply(null, xs), by1 = Math.max.apply(null, ys);
      var m = Math.min(8.4 / (bx1 - bx0), 5.1 / by1), ox = 5 - (bx0 + bx1) / 2 * m;
      var E = roh.map(function(p){ return [ox + p[0] * m, 1.25 + p[1] * m]; }), A = E[0], B = E[1], C = E[2];
      var ga = 180 - al - be;
      F.vieleck(E, 'figur');
      if (Au.aussen){   // Verlängerung von b über C hinaus, Aussenwinkel γ′
        var ext = [C[0] + (C[0] - A[0]) / abst(A, C) * 1.6, C[1] + (C[1] - A[1]) / abst(A, C) * 1.6];
        F.strecke(C, ext, 'verlaengerung');
        winkelMarke(F, C, ext, B, 22, 'w-c', null, null, true);
        var wm = (richtung(C, ext) + richtung(C, B)) / 2;
        F.text([C[0] + 40 / F.s * Math.cos(wm), C[1] + 40 / F.s * Math.sin(wm)], 'γ′ ' + (Au.aussenText || '?'), 'winkel tinte', 0, 4);
      }
      var lab = function(wert, name, key){ return vd.indexOf(key) >= 0 ? name : (Au.lab && Au.lab[key]) || (name + ' = ' + z(wert) + '°'); };
      winkelMarke(F, A, B, C, 26, 'w-a', lab(al, 'α', 'al'), 'winkel', true);
      winkelMarke(F, B, C, A, 26, 'w-b', lab(be, 'β', 'be'), 'winkel gruen', true);
      winkelMarke(F, C, A, B, 22, 'w-c', vd.indexOf('ga') >= 0 || Au.frage ? 'γ' : 'γ = ' + z(ga) + '°', 'winkel tinte', true);
      if (k.wahl){
        F.kandidat('par', C, [C[0] + 1, C[1]], k.wahl, true);
        var fu = lot(C, A, B); F.kandidat('h', C, [fu[0], fu[1]], k.wahl);
        F.kandidat('s', C, mitte(A, B), k.wahl);
      }
      if (Au.wahl && w.richtig){   // die Wechselwinkel an der Parallelen
        F.strecke([C[0] - 3, C[1]], [C[0] + 3, C[1]], 'hilfe');
        winkelMarke(F, C, [C[0] - 1, C[1]], A, 36, 'w-a', null, null, true);
        winkelMarke(F, C, B, [C[0] + 1, C[1]], 36, 'w-b', null, null, true);
      }
      ecken(F, E, ['A', 'B', 'C']);
      if (Au.frage || Au.wahl) return Au.zeile || '';
      var art = artWinkel([al, be, ga]), seiten = (al === 60 && be === 60) ? '; gleichseitig' : (al === be || al === ga || be === ga) ? '; gleichschenklig' : '';
      return '\\(\\alpha = ' + al + '°\\); \\(\\beta = ' + be + '°\\); \\(\\gamma = ' + ga + '°\\) — ' + art + seiten;
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(\\alpha\\) und \\(\\beta\\). Was geschieht mit \\(\\gamma\\)?', probe: { al: 70 }, ziel: function(w){ return w.bewegt.al || w.bewegt.be; } },
      { text: 'Mach das Dreieck rechtwinklig, mit dem rechten Winkel bei \\(C\\).', probe: { al: 30, be: 60 }, ziel: function(w){ return w.al + w.be === 90; } },
      { text: 'Mach das Dreieck gleichschenklig, mit der Spitze bei \\(C\\).', probe: { al: 70, be: 70 }, ziel: function(w){ return w.al === w.be; } },
      { text: 'Mach es gleichseitig.', probe: { al: 60, be: 60 }, ziel: function(w){ return w.al === 60 && w.be === 60; } },
      { text: 'Stell \\(\\alpha = 120°\\) ein und mach \\(\\beta\\) so gross wie möglich.', probe: { al: 120, be: 55 }, ziel: function(w){ return w.al === 120 && w.be === 55; } },
      // α = 40°, β = 80°: Höhe und Seitenhalbierende aus C liegen weit genug auseinander, um sie anzutippen
      { text: 'Tipp die Hilfslinie an, mit der man \\(\\alpha + \\beta + \\gamma = 180°\\) begründet.', setup: function(s){ s.setze({ al: 40, be: 80 }); s.sperre('al', 'be'); },
        zeile: 'Welche Linie bringt \\(\\alpha\\) und \\(\\beta\\) zur Ecke \\(C\\)?',
        wahl: { richtig: 'par', gut: 'Die Parallele zu \\(AB\\) durch \\(C\\): Links und rechts von \\(\\gamma\\) entstehen Wechselwinkel, gleich gross wie \\(\\alpha\\) und \\(\\beta\\). Zusammen mit \\(\\gamma\\) liegen sie auf einer Geraden: \\(180°\\).', rueck: {
          h: 'Das ist die Höhe \\(h_c\\): Sie steht senkrecht auf \\(AB\\). Gesucht ist eine Linie, an der \\(\\alpha\\) und \\(\\beta\\) als Wechselwinkel wieder auftauchen.',
          s: 'Das ist die Seitenhalbierende \\(s_c\\). Gesucht ist eine Linie, an der \\(\\alpha\\) und \\(\\beta\\) als Wechselwinkel wieder auftauchen.' } } },
      { text: '\\(\\alpha = 35°\\), \\(\\beta = 75°\\). Wie gross ist der Aussenwinkel \\(\\gamma^{\\prime}\\) bei \\(C\\)?', aussen: true,
        setup: function(s){ s.setze({ al: 35, be: 75 }); s.sperre('al', 'be'); }, zeile: 'gegeben \\(\\alpha = 35°\\), \\(\\beta = 75°\\); gesucht \\(\\gamma^{\\prime}\\)',
        frage: [{ name: 'g', label: '\\(\\gamma^{\\prime} =\\)', einheit: '°', soll: 110, fehler: [[70, 'Das ist der Innenwinkel \\(\\gamma\\). Der Aussenwinkel liegt an der Verlängerung von \\(b\\) und ergänzt \\(\\gamma\\) zu \\(180°\\).'], [145, 'Das ist der Aussenwinkel bei \\(A\\) (\\(180° - \\alpha\\)). Gesucht ist der bei \\(C\\).'], [105, 'Das ist der Aussenwinkel bei \\(B\\) (\\(180° - \\beta\\)). Gesucht ist der bei \\(C\\).']], tipp: '\\(\\gamma^{\\prime} = 180° - \\gamma\\) — oder direkt \\(\\gamma^{\\prime} = \\alpha + \\beta\\).' }],
        loesung: 'Aussenwinkelsatz: \\(\\gamma^{\\prime} = \\alpha + \\beta\\).' },
      { text: 'Gleichschenklig mit der Spitze \\(C\\), der Aussenwinkel bei \\(C\\) misst \\(100°\\). Wie gross sind \\(\\alpha\\) und \\(\\gamma\\)?', aussen: true, aussenText: '= 100°',
        verdeckt: ['al', 'be'], setup: function(s){ s.setze({ al: 50, be: 50 }); s.sperre('al', 'be'); }, zeile: 'gegeben \\(\\gamma^{\\prime} = 100°\\), \\(\\alpha = \\beta\\); gesucht \\(\\alpha\\) und \\(\\gamma\\)',
        frage: [{ name: 'a', label: '\\(\\alpha =\\)', einheit: '°', soll: 50, fehler: [[40, 'Das wäre richtig, wenn \\(\\gamma = 100°\\) wäre. \\(100°\\) ist aber der Aussenwinkel.'], [100, 'Der Aussenwinkel ist \\(\\alpha + \\beta\\) — zwei gleiche Winkel zusammen.']], tipp: '\\(\\gamma^{\\prime} = \\alpha + \\beta = 2\\alpha\\).' },
                { name: 'c', label: '\\(\\gamma =\\)', einheit: '°', soll: 80, fehler: [[100, 'Das ist der Aussenwinkel. \\(\\gamma\\) ergänzt ihn zu \\(180°\\).'], [20, 'Rechne nochmals: \\(\\gamma = 180° - \\gamma^{\\prime}\\).']], tipp: '\\(\\gamma = 180° - \\gamma^{\\prime}\\).' }] }
    ]
  });

  /* ---------- Kapitel 2: Höhen, Halbierende, Mittelsenkrechte ----------
     Unterschied zur Animation «Dreieckselemente» der Themenseite: Dort schaltet man die vier Familien um und zieht die
     Ecken. Hier zieht man C mit zwei Reglern (Schritt 0.5 cm), die Leiste lässt Linien unterscheiden und antippen,
     Lage-Ziele erfüllen (H aussen, H auf einer Ecke) und mit der Teilung 2 : 1 und dem Umkreisradius rechnen.
     A(0 | 0), B(6 | 0). Startwert C(2 | 3.5): spitzwinklig, ungleichseitig. */
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 250, x0: -3.5, x1: 9.5, y0: -3 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, A = [0, 0], B = [6, 0], C = [w.cx, w.cy], P = besondere(A, B, C), zg = Au.zeige;
      var fa = lot(A, B, C), fb = lot(B, A, C), fc = lot(C, A, B), wa = [];
      F.vieleck([A, B, C], 'figur');
      if (zg === 'h'){
        [[A, fa, B, C], [B, fb, A, C], [C, fc, A, B]].forEach(function(q){ F.gerade(q[0], [q[1][0], q[1][1]], 'hilfe2');
          var f = [q[1][0], q[1][1]], u = abst(q[2], f) > 1e-6 ? q[2] : q[3];
          F.rechts(f, [q[0][0] - f[0], q[0][1] - f[1]], [u[0] - f[0], u[1] - f[1]], 'hilfe'); });
        [[A, fa], [B, fb], [C, fc]].forEach(function(q){ F.strecke(q[0], [q[1][0], q[1][1]], 'hilfe'); });
        F.punkt(P.H, 'g-pkt loes'); F.text(P.H, 'H', 'loes', 9, -6, 'start');
      }
      if (zg === 's'){
        [[A, mitte(B, C)], [B, mitte(A, C)], [C, mitte(A, B)]].forEach(function(q){ F.strecke(q[0], q[1], 'hilfe'); F.punkt(q[1], 'g-pkt'); });
        F.punkt(P.S, 'g-pkt loes'); F.text(P.S, 'S', 'loes', 9, -6, 'start');
      }
      if (zg === 'w'){
        [[A, wfuss(A, B, C)], [B, wfuss(B, C, A)], [C, wfuss(C, A, B)]].forEach(function(q){ F.strecke(q[0], q[1], 'hilfe'); });
        F.kreis(P.MI, P.ri, 'umkreis'); F.punkt(P.MI, 'g-pkt loes'); F.name(P.MI, 'M', 'I', 'loes', 8, -6, 'start');
      }
      if (zg === 'm'){
        [[A, B], [B, C], [C, A]].forEach(function(q){ var m = mitte(q[0], q[1]); F.gerade(m, [m[0] - (q[1][1] - q[0][1]), m[1] + (q[1][0] - q[0][0])], 'hilfe2'); });
        F.kreis(P.MU, P.ru, 'umkreis'); F.punkt(P.MU, 'g-pkt loes'); F.name(P.MU, 'M', 'U', 'loes', 8, -6, 'start');
        if (Au.radius){ F.strecke(P.MU, A, 'loes-linie'); }
      }
      if (k.wahl){
        F.kandidat('h', C, [fc[0], fc[1]], k.wahl);
        F.kandidat('s', C, [3, 0], k.wahl);
        F.kandidat('w', C, wfuss(C, A, B), k.wahl);
        F.kandidat('m', [3, -1], [3, 1], k.wahl, true);
      }
      if (fc[2] < 0 || fc[2] > 1) F.strecke(fc[2] < 0 ? A : B, [fc[0], 0], 'verlaengerung');
      if (Au.wahl && w.richtig){
        var r = Au.wahl.richtig;
        if (r === 'h'){ F.strecke(C, [fc[0], 0], 'hilfe'); F.rechts([fc[0], 0], [0, 1], [fc[2] < 0.5 ? 1 : -1, 0], 'hilfe'); }
        if (r === 's'){ F.strecke(C, [3, 0], 'hilfe'); F.punkt([3, 0], 'g-pkt hilfe'); }
        if (r === 'w'){ F.strecke(C, wfuss(C, A, B), 'hilfe'); winkelMarke(F, C, A, wfuss(C, A, B), 30, 'winkelbogen'); winkelMarke(F, C, wfuss(C, A, B), B, 36, 'winkelbogen'); }
        if (r === 'm'){ F.gerade([3, 0], [3, 1], 'hilfe'); F.rechts([3, 0], [1, 0], [0, 1], 'hilfe'); }
      }
      ecken(F, [A, B, C], ['A', 'B', 'C']);
      F.text([3, 0], 'c', 'seite', 0, 16);
      if (Au.zeile) return Au.zeile;
      var wi = [winkel(A, B, C), winkel(B, C, A), winkel(C, A, B)];
      // Lage des gezeigten Schnittpunkts (H oder M_U) in Worten — er kann weit ausserhalb des Bildes liegen
      var lage = '';
      if (zg === 'h' || zg === 'm'){
        var Q = zg === 'h' ? P.H : P.MU, nm = zg === 'h' ? '\\(H\\)' : '\\(M_U\\)', ecke = null;
        [[A, 'A'], [B, 'B'], [C, 'C']].forEach(function(e){ if (abst(e[0], Q) < 1e-6) ecke = e[1]; });
        var kr = function(p, q, r){ return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]); };
        var d1 = kr(A, B, Q), d2 = kr(B, C, Q), d3 = kr(C, A, Q), eps = 1e-9;
        var innen = d1 > eps && d2 > eps && d3 > eps, aufRand = !innen && d1 > -eps && d2 > -eps && d3 > -eps;
        var imBild = Q[0] >= F.x0 && Q[0] <= F.x1 && Q[1] >= F.y0 && Q[1] <= F.y1;
        lage = '<br>' + nm + (ecke ? ' liegt auf der Ecke \\(' + ecke + '\\)' : innen ? ' liegt innen' : aufRand ? ' liegt auf einer Seite' : ' liegt aussen' + (imBild ? '' : ' (ausserhalb des Bildes)'));
      }
      return '\\(\\alpha ' + zz(wi[0], 1) + '°\\); \\(\\beta ' + zz(wi[1], 1) + '°\\); \\(\\gamma ' + zz(wi[2], 1) + '°\\) — ' + artWinkel(wi) + lage;
    },
    aufgaben: [
      // Lagen so gewählt, dass keine zwei Kandidaten aufeinanderliegen (pruef-geo)
      { text: 'Tipp die Höhe \\(h_c\\) an.', setup: function(s){ s.setze({ cx: 1, cy: 4 }); s.sperre('cx', 'cy'); }, zeile: 'Vier Linien zur Seite \\(c\\) — welche ist \\(h_c\\)?',
        wahl: { richtig: 'h', gut: 'Die Höhe geht durch \\(C\\) und steht senkrecht auf der Geraden \\(AB\\).', rueck: {
          s: 'Das ist die Seitenhalbierende \\(s_c\\): Sie endet in der Mitte von \\(c\\), steht aber nicht senkrecht.',
          w: 'Das ist die Winkelhalbierende \\(w_\\gamma\\): Sie teilt den Winkel bei \\(C\\) in zwei gleiche Teile.',
          m: 'Das ist die Mittelsenkrechte von \\(c\\): Sie steht senkrecht, geht aber durch die Mitte von \\(c\\), nicht durch \\(C\\).' } } },
      { text: 'Tipp die Winkelhalbierende \\(w_\\gamma\\) an.', setup: function(s){ s.setze({ cx: 5.5, cy: 4 }); s.sperre('cx', 'cy'); }, zeile: 'Welche Linie teilt \\(\\gamma\\) in zwei gleiche Teile?',
        wahl: { richtig: 'w', gut: 'Sie teilt \\(\\gamma\\) in zwei gleiche Teile — sie liegt zwischen Höhe und Seitenhalbierender.', rueck: {
          h: 'Das ist die Höhe \\(h_c\\): Sie steht senkrecht auf \\(AB\\). Die beiden Winkel bei \\(C\\) links und rechts davon sind verschieden.',
          s: 'Das ist die Seitenhalbierende \\(s_c\\): Sie endet in der Mitte von \\(c\\).',
          m: 'Das ist die Mittelsenkrechte von \\(c\\). Sie geht nicht durch \\(C\\).' } } },
      { text: 'Tipp die Mittelsenkrechte von \\(c\\) an.', setup: function(s){ s.setze({ cx: 1.5, cy: 3.5 }); s.sperre('cx', 'cy'); }, zeile: 'Welche Linie steht in der Mitte von \\(c\\) senkrecht?',
        wahl: { richtig: 'm', gut: 'Sie steht in der Mitte von \\(c\\) senkrecht auf \\(c\\). Jeder ihrer Punkte ist von \\(A\\) und \\(B\\) gleich weit entfernt.', rueck: {
          h: 'Das ist die Höhe \\(h_c\\): Sie steht auch senkrecht, geht aber durch die Ecke \\(C\\), nicht durch die Mitte von \\(c\\).',
          s: 'Das ist die Seitenhalbierende \\(s_c\\): Sie geht durch die Mitte von \\(c\\), steht aber nicht senkrecht.',
          w: 'Das ist die Winkelhalbierende \\(w_\\gamma\\).' } } },
      { text: 'Die drei Höhen schneiden sich in \\(H\\). Zieh \\(C\\) so, dass \\(H\\) ausserhalb des Dreiecks liegt.', zeige: 'h', probe: { cx: -1 },
        ziel: function(w){ return w.cx < 0 || w.cx > 6 || w.cx * (w.cx - 6) + w.cy * w.cy < -1e-9; } },
      { text: 'Zieh \\(C\\) so, dass \\(H\\) genau auf einer Ecke liegt.', zeige: 'h', probe: { cx: 0 },
        ziel: function(w){ return w.cx === 0 || w.cx === 6 || Math.abs(w.cx * (w.cx - 6) + w.cy * w.cy) < 1e-9; } },
      { text: 'Die Winkelhalbierenden schneiden sich in \\(M_I\\), dem Mittelpunkt des Inkreises. Zieh \\(C\\) herum: Kann \\(M_I\\) ausserhalb liegen?', zeige: 'w', probe: { cx: 7 },
        ziel: function(w){ return w.bewegt.cx || w.bewegt.cy; } },
      { text: 'Die Seitenhalbierende \\(s_c\\) ist \\(5\\,\\text{cm}\\) lang. Wie weit ist der Schwerpunkt \\(S\\) von \\(C\\) entfernt?', zeige: 's',
        setup: function(s){ s.setze({ cx: 0, cy: 4 }); s.sperre('cx', 'cy'); }, zeile: 'gegeben \\(s_c = 5\\,\\text{cm}\\); gesucht \\(\\overline{CS}\\)',
        frage: [{ name: 'cs', label: '\\(\\overline{CS} \\approx\\)', einheit: 'cm', soll: 3.33, fehler: [[2.5, 'Das ist die Mitte von \\(s_c\\). \\(S\\) teilt \\(s_c\\) im Verhältnis \\(2 : 1\\) — der längere Teil liegt bei der Ecke.'], [1.67, 'Das ist der kürzere Teil, von \\(S\\) bis zur Seitenmitte. Gefragt ist der Teil von \\(C\\) bis \\(S\\).']], tipp: '\\(\\overline{CS} = \\tfrac{2}{3} \\cdot s_c\\).' }] },
      { text: '\\(M_U\\) ist von \\(A\\) rund \\(3.30\\,\\text{cm}\\) entfernt. Wie weit ist \\(M_U\\) von \\(C\\) entfernt?', zeige: 'm', radius: true,
        setup: function(s){ s.setze({ cx: 1, cy: 4 }); s.sperre('cx', 'cy'); }, zeile: 'gegeben \\(\\overline{M_U A} \\approx 3.30\\,\\text{cm}\\); gesucht \\(\\overline{M_U C}\\)',
        frage: [{ name: 'r', label: '\\(\\overline{M_U C} \\approx\\)', einheit: 'cm', soll: 3.30, tol: 0.011, fehler: [[1.65, 'Nicht die Hälfte: \\(M_U\\) ist von allen drei Ecken gleich weit entfernt.'], [6.6, 'Das ist der Durchmesser des Umkreises. Gefragt ist der Abstand zu einer Ecke.']], tipp: '\\(M_U\\) liegt auf allen drei Mittelsenkrechten — wie weit ist er von jeder Ecke?' }],
        loesung: '\\(M_U\\) ist von allen Ecken gleich weit entfernt: Der Umkreis geht durch \\(A\\), \\(B\\) und \\(C\\).' }
    ]
  });

  /* ---------- Kapitel 3: Fläche und Umfang ----------
     Unterschied zur Animation «Flächenberechnung» der Themenseite (Zerlegen in ein Rechteck): Hier wandert die Spitze C
     parallel zur Grundseite, die Leiste lässt die Höhe antippen — auch ausserhalb und zu einer schrägen Grundseite — und
     die Fläche und eine zweite Höhe berechnen. A(0 | 0), B(6 | 0), C(t | 4): g = 6 cm, h = 4 cm, A = 12 cm² wie im
     Einführungsclip (Themenseite, Mini-Check). Startwert t = 2. */
  arbeitsbereich('sim3', {
    fenster: { w: 320, h: 240, x0: -4, x1: 11, y0: -3.8 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, A = [0, 0], B = [6, 0], C = [w.t, 4], fc = lot(C, A, B), ha = Au.ha;
      F.strecke([-4, 4], [11, 4], 'parallele');
      F.vieleck([A, B, C], 'figur');
      if (fc[2] < 0 || fc[2] > 1) F.strecke(fc[2] < 0 ? A : B, [fc[0], 0], 'verlaengerung');
      var fa = lot(A, B, C);
      if (ha) F.gerade(B, C, 'verlaengerung');
      if (k.wahl){
        if (!ha){ F.kandidat('b', A, C, k.wahl); F.kandidat('a', B, C, k.wahl); F.kandidat('h', C, [fc[0], 0], k.wahl); F.kandidat('s', C, [3, 0], k.wahl); }
        else { F.kandidat('ha', A, [fa[0], fa[1]], k.wahl); F.kandidat('hc', C, [fc[0], 0], k.wahl); F.kandidat('b', A, C, k.wahl); F.kandidat('sa', A, mitte(B, C), k.wahl); }
      }
      var zeigeH = (!ha && w.richtig) || Au.zeigeH;
      if (zeigeH){ F.strecke(C, [fc[0], 0], 'hilfe'); F.rechts([fc[0], 0], [0, 1], [fc[2] < 0.5 ? 1 : -1, 0], 'hilfe'); F.text([fc[0], 2], 'h', 'hilfe', -6, 4, 'end'); }
      if (ha && w.richtig && Au.wahl){ F.strecke(A, [fa[0], fa[1]], 'hilfe'); F.rechts([fa[0], fa[1]], [A[0] - fa[0], A[1] - fa[1]], [C[0] - B[0], C[1] - B[1]], 'hilfe'); }
      ecken(F, [A, B, C], ['A', 'B', 'C']);
      F.text([3, 0], ha ? 'c = 6 cm' : 'g = 6 cm', 'mass', 0, 16);
      if (ha) F.text(mitte(B, C), 'a = 5 cm', 'mass', 8, 0, 'start');
      if (Au.zeile) return Au.zeile;
      return 'Spitze \\(C(' + z(w.t) + ' \\mid 4)\\); \\(g = 6\\,\\text{cm}\\)' + (zeigeH ? '; \\(h = 4\\,\\text{cm}\\)' : '');
    },
    aufgaben: [
      // t = 1.5: Höhe (x = 1.5) und Seitenhalbierende (Ende bei 3) liegen auseinander (pruef-geo)
      { text: 'Die Grundseite ist \\(AB\\). Tipp die zugehörige Höhe an.', setup: function(s){ s.setze({ t: 1.5 }); s.sperre('t'); },
        wahl: { richtig: 'h', gut: 'Die Höhe ist der senkrechte Abstand von \\(C\\) zur Geraden \\(AB\\): \\(h = 4\\,\\text{cm}\\).', rueck: {
          a: 'Das ist die Seite \\(a = BC\\) — sie steht nicht senkrecht auf \\(AB\\).',
          b: 'Das ist die Seite \\(b = AC\\) — sie steht nicht senkrecht auf \\(AB\\).',
          s: 'Das ist die Seitenhalbierende: Sie endet in der Mitte von \\(AB\\) und steht nicht senkrecht.' } } },
      { text: 'Berechne die Fläche des Dreiecks.', zeigeH: true, setup: function(s){ s.setze({ t: 1.5 }); s.sperre('t'); }, zeile: 'gegeben \\(g = 6\\,\\text{cm}\\), \\(h = 4\\,\\text{cm}\\); gesucht \\(A\\)',
        frage: [{ name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 12, fehler: [[24, 'Das ist \\(g \\cdot h\\) — die Fläche des Rechtecks. Das Dreieck ist die Hälfte davon.'], [10, 'Das ist \\(g + h\\). Eine Fläche ist ein Produkt.']], tipp: '\\(A = \\tfrac{1}{2}\\, g \\cdot h\\).' }] },
      { text: 'Schieb die Spitze so weit, dass der Fusspunkt der Höhe ausserhalb der Grundseite liegt.', zeigeH: true, probe: { t: 8 }, ziel: function(w){ return w.t < 0 || w.t > 6; } },
      { text: 'Die Spitze steht bei \\(t = 9\\), die schräge Seite \\(BC\\) ist \\(5\\,\\text{cm}\\) lang. Wie gross ist die Fläche?', setup: function(s){ s.setze({ t: 9 }); s.sperre('t'); }, zeile: 'gegeben \\(g = 6\\,\\text{cm}\\), \\(\\overline{BC} = 5\\,\\text{cm}\\); gesucht \\(A\\)',
        frage: [{ name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 12, fehler: [[15, 'Die schräge Seite \\(BC\\) ist keine Höhe. Die Höhe ist der senkrechte Abstand zur <b>Geraden</b> \\(AB\\) — auch ausserhalb der Strecke.'], [24, 'Das ist \\(g \\cdot h\\). Das Dreieck ist die Hälfte.'], [30, 'Das ist \\(g \\cdot \\overline{BC}\\). Die schräge Seite ist keine Höhe, und das Dreieck ist die Hälfte.']], tipp: 'Grundseite und Höhe haben sich nicht geändert.' }],
        loesung: 'Grundseite und Höhe sind gleich geblieben — also auch die Fläche.' },
      { text: 'Stell ein rechtwinkliges Dreieck ein.', probe: { t: 0 }, ziel: function(w){ return w.t === 0 || w.t === 6; } },
      { text: 'Jetzt ist \\(a = BC\\) die Grundseite. Tipp die Höhe \\(h_a\\) an.', ha: true, setup: function(s){ s.setze({ t: 9 }); s.sperre('t'); }, zeile: 'Grundseite \\(a = BC\\): Welche Linie ist \\(h_a\\)?',
        wahl: { richtig: 'ha', gut: 'Das Lot von \\(A\\) auf die Gerade \\(BC\\) — sein Fusspunkt liegt auf der Verlängerung über \\(B\\) hinaus.', rueck: {
          hc: 'Das ist die Höhe zur Grundseite \\(AB\\). Zu \\(a = BC\\) gehört das Lot von der gegenüberliegenden Ecke \\(A\\).',
          b: 'Das ist die Seite \\(b\\) — sie steht nicht senkrecht auf \\(BC\\).',
          sa: 'Das ist die Seitenhalbierende von \\(A\\) aus: Sie endet in der Mitte von \\(BC\\).' } } },
      { text: '\\(a = BC = 5\\,\\text{cm}\\) und \\(A = 12\\,\\text{cm}^2\\). Wie lang ist \\(h_a\\)?', ha: true, setup: function(s){ s.setze({ t: 9 }); s.sperre('t'); }, zeile: 'gegeben \\(a = 5\\,\\text{cm}\\), \\(A = 12\\,\\text{cm}^2\\); gesucht \\(h_a\\)',
        frage: [{ name: 'ha', label: '\\(h_a =\\)', einheit: 'cm', soll: 4.8, fehler: [[2.4, 'Aus \\(A = \\tfrac{1}{2}\\, a \\cdot h_a\\) folgt \\(h_a = \\tfrac{2A}{a}\\) — das Doppelte.'], [60, 'Teilen, nicht multiplizieren: \\(h_a = \\tfrac{2A}{a}\\).'], [4, 'Das ist \\(h_c\\), die Höhe zu \\(AB\\). Zu \\(a\\) gehört eine andere Höhe.']], tipp: '\\(h_a = \\tfrac{2A}{a}\\).' }],
        loesung: '\\(h_a = 4.8\\,\\text{cm}\\) ist zugleich der Abstand der Ecke \\(A\\) von der Geraden \\(BC\\).' }
    ]
  });

  /* ---------- Kapitel 4: Rechtwinklige Dreiecke und Pythagoras ----------
     Unterschied zu den Animationen «Satzgruppe Pythagoras» und «Pythagoras-Anwendung» der Themenseite (Scherung,
     Seitenverhältnisse): Hier stellt man die Katheten a und b ein (Schritt 0.5 cm), die Zeile zeigt a² + b² und c²; die
     Leiste lässt die Hypotenuse in gedrehter Lage antippen, Ziel-Dreiecke einstellen und Seiten und Höhen berechnen.
     Rechter Winkel bei C(0 | 0), A(b | 0), B(0 | a). Startwert a = 3, b = 4 wie im Einführungsclip (Themenseite,
     Mini-Check). In den Aufgaben 6 und 7 zeigt die Figur ein gleichschenkliges bzw. gleichseitiges Dreieck. */
  arbeitsbereich('sim4', {
    fenster: { w: 300, h: 300, x0: -1.5, x1: 9.5, y0: -1.5, drehpunkt: [4, 4] },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, a = w.a, b = w.b, c = Math.hypot(a, b);
      if (Au.form === 'gs' || Au.form === 'gls'){
        var g = Au.form === 'gs' ? 6 : 6, hh = Au.form === 'gs' ? 4 : Math.sqrt(27), L = [1.5, 0.5], R = [1.5 + g, 0.5], S = [1.5 + g / 2, 0.5 + hh];
        F.vieleck([L, R, S], 'figur');
        F.vieleck([[S[0], 0.5], R, S], 'haelfte');
        F.strecke(S, [S[0], 0.5], 'hilfe'); F.rechts([S[0], 0.5], [1, 0], [0, 1], 'hilfe');
        F.text(mitte(L, R), Au.form === 'gs' ? 'Basis 6 cm' : '6 cm', 'mass', 0, 16);
        F.text(mitte(R, S), Au.form === 'gs' ? '5 cm' : '6 cm', 'mass', 8, 0, 'start');
        if (Au.form === 'gls') F.text(mitte(L, S), '6 cm', 'mass', -8, 0, 'end');
        F.text([S[0], 0.5 + hh / 2], w.richtig ? 'h ' + (Au.form === 'gs' ? '= 4' : '≈ 5.20') : 'h = ?', 'loes', -10, 4, 'end');
        return Au.zeile;
      }
      // gedreht: um die Bildmitte (4 | 4), das Dreieck mit dem Schwerpunkt dorthin verschoben
      var v = Au.dreh ? [4 - b / 3, 4 - a / 3] : [0, 0];
      if (Au.dreh) F.drehen(grad(Au.dreh));
      var C = [v[0], v[1]], A = [v[0] + b, v[1]], B = [v[0], v[1] + a];
      F.vieleck([A, B, C], 'figur');
      F.rechts(C, [1, 0], [0, 1], '');
      if (k.wahl){ F.kandidat('a', B, C, k.wahl); F.kandidat('b', C, A, k.wahl); F.kandidat('c', A, B, k.wahl); }
      if (Au.wahl && w.richtig) F.strecke(A, B, 'loes-linie');
      var vd = Au.verdeckt || [], lab = Au.lab || {};
      F.text(mitte(B, C), lab.a || (Au.wahl ? '' : 'a = ' + z(a)), 'mass', -7, 4, 'end');
      F.text(mitte(C, A), lab.b || (Au.wahl ? '' : 'b = ' + z(b)), 'mass', 0, 16);
      F.text(mitte(A, B), lab.c || (Au.wahl ? '' : 'c'), 'mass', 8, -4, 'start');
      ecken(F, [A, B, C], ['A', 'B', 'C']);
      F.drehen(0);
      if (Au.zeile) return Au.zeile;
      return '\\(a^2 + b^2 = ' + z(a * a) + ' + ' + z(b * b) + ' = ' + z(a * a + b * b) + '\\); \\(c ' + zz(c) + '\\,\\text{cm}\\), \\(c^2 ' + zz(c * c) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(a\\) und \\(b\\). Vergleiche \\(a^2 + b^2\\) mit \\(c^2\\) in der Zeile.', probe: { a: 5 }, ziel: function(w){ return w.bewegt.a || w.bewegt.b; } },
      { text: 'Das Dreieck ist gedreht. Tipp die Hypotenuse an.', dreh: 140, setup: function(s){ s.sperre('a', 'b'); }, zeile: 'Welche Seite liegt dem rechten Winkel gegenüber?',
        wahl: { richtig: 'c', gut: 'Die Hypotenuse liegt dem rechten Winkel gegenüber — die längste Seite.', rueck: {
          a: 'Das ist eine Kathete: Sie liegt am rechten Winkel an.', b: 'Das ist eine Kathete: Sie liegt am rechten Winkel an.' } } },
      { text: 'Stell ein Dreieck mit der Hypotenuse \\(c = 10\\,\\text{cm}\\) ein.', probe: { a: 6, b: 8 }, ziel: function(w){ return Math.abs(w.a * w.a + w.b * w.b - 100) < 1e-9; } },
      { text: 'Mach die beiden Katheten gleich lang (ein halbes Quadrat). Wie lang ist \\(c\\) im Vergleich zu \\(a\\)?', probe: { a: 4 }, ziel: function(w){ return w.a === w.b; } },
      { text: 'Eine Kathete ist \\(3.5\\,\\text{cm}\\), die Hypotenuse \\(8\\,\\text{cm}\\) lang. Wie lang ist die andere Kathete \\(b\\)?', fest: { a: 3.5, b: Math.sqrt(64 - 12.25) }, verdeckt: ['b'],
        setup: function(s){ s.sperre('a', 'b'); }, lab: { a: 'a = 3.5', b: 'b = ?', c: 'c = 8' }, zeile: 'gegeben \\(a = 3.5\\,\\text{cm}\\), \\(c = 8\\,\\text{cm}\\); gesucht \\(b\\)',
        frage: [{ name: 'b', label: '\\(b \\approx\\)', einheit: 'cm', soll: 7.19, fehler: [[8.73, 'Länger als die Hypotenuse? Für eine Kathete wird subtrahiert: \\(b^2 = c^2 - a^2\\).'], [4.5, 'Das ist \\(8 - 3.5\\). Subtrahiert werden die Quadrate, danach die Wurzel.'], [51.75, 'Das ist \\(b^2\\). Zieh noch die Wurzel.']], tipp: '\\(b = \\sqrt{c^2 - a^2}\\).' }] },
      { text: 'Gleichschenkliges Dreieck: Basis \\(6\\,\\text{cm}\\), Schenkel \\(5\\,\\text{cm}\\). Wie hoch ist es?', form: 'gs', verdeckt: ['a', 'b'], setup: function(s){ s.sperre('a', 'b'); },
        zeile: 'Die Höhe halbiert die Basis: Die grüne Hälfte ist rechtwinklig.',
        frage: [{ name: 'h', label: '\\(h =\\)', einheit: 'cm', soll: 4, fehler: [[5.83, 'Der Schenkel ist die Hypotenuse der Hälfte, die längste Seite. Für eine Kathete wird subtrahiert.'], [2, 'Das ist \\(5 - 3\\). Subtrahiert werden die Quadrate, danach die Wurzel.'], [16, 'Das ist \\(h^2\\). Zieh noch die Wurzel.']], tipp: 'Die Hälfte hat die Hypotenuse \\(5\\) und die Kathete \\(3\\) (halbe Basis): \\(h = \\sqrt{5^2 - 3^2}\\).' }] },
      { text: 'Gleichseitiges Dreieck mit der Seite \\(6\\,\\text{cm}\\). Wie hoch ist es?', form: 'gls', verdeckt: ['a', 'b'], setup: function(s){ s.sperre('a', 'b'); },
        zeile: 'Die Höhe halbiert die Seite: Die grüne Hälfte ist rechtwinklig.',
        frage: [{ name: 'h', label: '\\(h \\approx\\)', einheit: 'cm', soll: 5.2, fehler: [[6.71, 'Die Seite \\(6\\) ist die Hypotenuse der Hälfte. Für eine Kathete wird subtrahiert.'], [3, 'Das ist die halbe Seite, eine Kathete. Gesucht ist die andere Kathete.'], [27, 'Das ist \\(h^2\\). Zieh noch die Wurzel.']], tipp: '\\(h = \\sqrt{6^2 - 3^2}\\).' }] }
    ]
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function r2(v){ return Math.round(v * 100) / 100; }
    function mischen(l){ l = l.slice(); for (var i = l.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = l[i]; l[i] = l[j]; l[j] = t; } return l; }
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche · Kapitelaufgaben ·
       Gesamttest · Beispiele der Themenseite. Je Typ und Variante ein eigener Schlüssel. */
    var SPERRE = [
      // winkel: ws|α|β (γ aus zwei Winkeln), wa|kleiner|grösser (Aussenwinkel aus zwei Innenwinkeln), wi|Aussen|Innen,
      // gb|Basiswinkel, gs|Spitze, ga|Aussenwinkel an der Spitze, gab|Aussenwinkel an der Basis, rw|α, wv|k|γ
      'ws|50|60', 'ws|40|50', 'ws|47|68', 'ws|48|75', 'ws|35|75', 'wa|35|75', 'wa|50|70', 'wa|35|65', 'wa|47|68', 'wa|38|65',
      'wi|115|38', 'gb|72', 'gb|52', 'gs|40', 'gs|30', 'ga|100', 'gab|116', 'rw|35', 'rw|34', 'wv|2|54', 'wv|2|72',
      // dreiecksart: da|sortierte Winkel
      'da|40|50|90',
      // elem-rechnen: sp|Art|Wert, wh|α, adc|α|γ, hw|α
      'sp|s|9', 'sp|s|5', 'sp|s|7.5', 'wh|64', 'wh|70', 'adc|70|60', 'hw|74', 'hw|58',
      // flaeche: fa|g|h (cm), fh|A|g, fz|a|ha|b, fu|Art|…
      'fa|6|4', 'fa|6|5', 'fa|9|4', 'fa|45|18', 'fa|7|4', 'fh|15|6', 'fh|20|8', 'fh|12|5', 'fh|18|5', 'fh|18|9',
      'fz|8|3|6', 'fz|9|4|6', 'fz|9|4|5', 'fu|gs|7|25',
      // pyth-figur: ph|Kathete|Kathete (sortiert), pk|Hypotenuse|Kathete
      'ph|3|4', 'ph|6|8', 'ph|9|12', 'ph|5|12', 'pk|13|5', 'pk|10|6', 'pk|8|3.5', 'pk|25|7', 'pk|8.5|4', 'pk|5|3',
      // pyth-anwendung: gsh|Basis|Schenkel, gss|Basis|Höhe, glh|s, gla|s, lh|Länge|Abstand
      'gsh|6|5', 'gsh|12|10', 'gsh|10|13', 'gss|9.6|3.6', 'gss|8|3.5', 'glh|6', 'glh|8', 'glh|10', 'gla|10', 'gla|8', 'lh|4.5|1.2'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function feld(A, f, e, soll, tipp, fehler, tol){
      if (stimmt(e[f], soll, tol)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (!stimmt(fehler[j][0], soll, tol) && stimmt(e[f], fehler[j][0], tol)) return fehler[j][1];
      return nah(e[f], soll, tol) ? RUNDEN : tipp;
    }
    /* Gezielte Fehler für das Prüfwerkzeug: nur Werte, die sich vom Sollwert unterscheiden; gleiche Fehlwerte zählen einmal. */
    function fehlerListe(A, f, liste, tol){
      var aus = [], gesehen = [];
      liste.forEach(function(x){ var v = r2(x[0]);
        if (isFinite(v) && !stimmt(v, A.soll, tol) && Math.abs(v - A.soll) > 0.07 && !gesehen.some(function(g){ return stimmt(v, g, tol); })){
          gesehen.push(v); var o = {}; o[f] = String(v);
          // Stichwort für das Prüfwerkzeug: der Anfang der eigenen Meldung bis zur ersten Formel
          var kw = String(x[1] || '').replace(/<[^>]+>/g, '').split('\\')[0].trim().slice(0, 24);
          aus.push([o, kw.length > 3 ? kw : null]); } });
      return aus;
    }
    function falschOhneSoll(A){ return A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; }); }
    var GR = { A: 'α', B: 'β', C: 'γ' }, GRL = { A: '\\alpha', B: '\\beta', C: '\\gamma' }, KL = { A: 'a', B: 'b', C: 'c' };

    var TYPEN = {
      /* ── Kapitel 1 ── */
      /* Winkel berechnen: Winkelsumme, Aussenwinkel, gleichschenklig, rechtwinklig, Winkel im Verhältnis. */
      'winkel': { felder: ['w'], muster: '{w} °',
        schl: function(A){ return A.schl; },
        eingabe: function(A){ return { w: String(A.soll) }; },
        neu: function(){
          var art = zufall(['summe', 'summe', 'aussen', 'aussen', 'innen', 'gb', 'gs', 'ga', 'gab', 'rw', 'wv']), a, b, x;
          if (art === 'summe'){ a = zufallG(4, 20) * 5 + zufall([0, 2, 3]); b = zufallG(15, 150 - a - 10);
            return { art: art, schl: 'ws|' + Math.min(a, b) + '|' + Math.max(a, b), soll: 180 - a - b, text: 'In einem Dreieck ist \\(\\alpha = ' + a + '°\\) und \\(\\beta = ' + b + '°\\). Wie gross ist \\(\\gamma\\)?',
              falsch: [[360 - a - b, 'Die Winkelsumme im Dreieck ist \\(180°\\), nicht \\(360°\\).', '180'], [a + b, 'Das ist \\(\\alpha + \\beta\\). \\(\\gamma\\) ist der Rest bis \\(180°\\).', 'Rest']],
              tipp: '\\(\\gamma = 180° - \\alpha - \\beta\\).', loes: '180° - ' + a + '° - ' + b + '° = ' + (180 - a - b) + '°' }; }
          if (art === 'aussen'){
            // nicht a + b = 90 (Innen- = Aussenwinkel) und nicht 180° − a oder 180° − b = a + b (falsche Ecke gäbe dasselbe)
            do { a = zufallG(20, 80); b = zufallG(20, 140 - a); } while (a + b === 90 || 180 - a === a + b || 180 - b === a + b);
            var eck = zufall(['A', 'B', 'C']), and = ['A', 'B', 'C'].filter(function(e){ return e !== eck; });
            var bk = [Math.min(a, b), Math.max(a, b)];
            return { art: art, schl: 'wa|' + bk[0] + '|' + bk[1], soll: a + b, text: 'In einem Dreieck ist \\(' + GRL[and[0]] + ' = ' + a + '°\\) und \\(' + GRL[and[1]] + ' = ' + b + '°\\). Wie gross ist der Aussenwinkel \\(' + GRL[eck] + '^{\\prime}\\) bei \\(' + eck + '\\)?',
              falsch: [[180 - a - b, 'Das ist der Innenwinkel \\(' + GRL[eck] + '\\). Der Aussenwinkel ergänzt ihn zu \\(180°\\).', 'Innenwinkel'], [180 - a, 'Das ist der Aussenwinkel bei \\(' + and[0] + '\\). Gesucht ist der bei \\(' + eck + '\\).', 'andere'], [180 - b, 'Das ist der Aussenwinkel bei \\(' + and[1] + '\\). Gesucht ist der bei \\(' + eck + '\\).', 'andere']],
              tipp: 'Aussenwinkelsatz: Der Aussenwinkel ist so gross wie die beiden nicht anliegenden Innenwinkel zusammen.', loes: GRL[eck] + "' = " + a + '° + ' + b + '° = ' + (a + b) + '°' }; }
          if (art === 'innen'){   // Aussenwinkel bei A, Innenwinkel β gegeben, γ gesucht; nicht α = γ (sonst fiele «α statt γ» nicht auf)
            do { x = zufallG(95, 160); b = zufallG(20, x - 20); } while (180 - x === x - b);
            return { art: art, schl: 'wi|' + x + '|' + b, soll: x - b, text: 'Der Aussenwinkel bei \\(A\\) misst \\(' + x + '°\\), und \\(\\beta = ' + b + '°\\). Wie gross ist \\(\\gamma\\)?',
              falsch: [[180 - x, 'Das ist \\(\\alpha\\), der Nebenwinkel des Aussenwinkels. Gesucht ist \\(\\gamma\\).', 'alpha'], [x + b, 'Der Aussenwinkel bei \\(A\\) ist \\(\\beta + \\gamma\\) — also \\(\\gamma = \\alpha^{\\prime} - \\beta\\).', 'plus'], [180 - b, 'Das ist der Aussenwinkel bei \\(B\\).', 'beta']],
              tipp: '\\(\\alpha^{\\prime} = \\beta + \\gamma\\), also \\(\\gamma = \\alpha^{\\prime} - \\beta\\). Oder: zuerst \\(\\alpha = 180° - \\alpha^{\\prime}\\).', loes: x + '° - ' + b + '° = ' + (x - b) + '°' }; }
          if (art === 'gb'){ b = zufallG(46, 84); if (b === 60) b = 62;
            return { art: art, schl: 'gb|' + b, soll: 180 - 2 * b, text: 'Ein gleichschenkliges Dreieck hat die Basiswinkel \\(' + b + '°\\). Wie gross ist der Winkel an der Spitze?',
              falsch: [[180 - b, 'Es gibt zwei Basiswinkel: \\(180° - 2 \\cdot ' + b + '°\\).', 'zwei'], [(180 - b) / 2, 'So rechnet man den Basiswinkel aus der Spitze. Hier ist ein Basiswinkel gegeben.', 'umgekehrt']],
              tipp: 'Winkelsumme \\(180°\\), die beiden Basiswinkel sind gleich gross.', loes: '180° - 2 \\cdot ' + b + '° = ' + (180 - 2 * b) + '°' }; }
          if (art === 'gs'){ x = zufallG(5, 35) * 4 + zufall([0, 2]); if (x === 60) x = 64;
            return { art: art, schl: 'gs|' + x, soll: (180 - x) / 2, text: 'Ein gleichschenkliges Dreieck hat an der Spitze den Winkel \\(' + x + '°\\). Wie gross ist ein Basiswinkel?',
              falsch: [[180 - x, 'Das sind beide Basiswinkel zusammen. Jeder ist die Hälfte.', 'Hälfte']].concat(x < 90 ? [[180 - 2 * x, 'Gegeben ist die Spitze, nicht ein Basiswinkel.', 'umgekehrt']] : []),
              tipp: 'Für die beiden Basiswinkel bleiben \\(180° - ' + x + '°\\), jeder ist die Hälfte.', loes: '(180° - ' + x + '°) : 2 = ' + (180 - x) / 2 + '°' }; }
          if (art === 'ga'){ x = zufallG(21, 79) * 2; if (x === 120 || x === 90) x = 124;   // Aussenwinkel an der Spitze → Basiswinkel = x/2
            return { art: art, schl: 'ga|' + x, soll: x / 2, text: 'Gleichschenkliges Dreieck mit der Spitze \\(C\\): Der Aussenwinkel bei \\(C\\) misst \\(' + x + '°\\). Wie gross ist ein Basiswinkel?',
              falsch: [[(180 - x) / 2, 'Das wäre richtig, wenn \\(\\gamma = ' + x + '°\\) wäre. \\(' + x + '°\\) ist aber der Aussenwinkel.', 'Innen'], [180 - x, 'Das ist der Innenwinkel \\(\\gamma\\) an der Spitze.', 'gamma']],
              tipp: 'Der Aussenwinkel bei \\(C\\) ist \\(\\alpha + \\beta\\) — zwei gleiche Basiswinkel.', loes: x + '° : 2 = ' + x / 2 + '°' }; }
          if (art === 'gab'){ x = zufallG(48, 84) * 2; if (x === 120 || x === 144) x = 122;   // Aussenwinkel an einer Basisecke → Spitze
            var bw = 180 - x;
            return { art: art, schl: 'gab|' + x, soll: 180 - 2 * bw, text: 'In einem gleichschenkligen Dreieck misst der Aussenwinkel an einer Basisecke \\(' + x + '°\\). Wie gross ist der Winkel an der Spitze?',
              falsch: [[bw, 'Das ist der Basiswinkel (Nebenwinkel des Aussenwinkels). Gesucht ist die Spitze.', 'Basis'], [180 - x / 2, 'Zuerst den Basiswinkel: \\(180° - ' + x + '°\\). Es gibt zwei davon.', 'halb']],
              tipp: 'Basiswinkel \\(= 180° - ' + x + '°\\); dann die Spitze aus der Winkelsumme.', loes: '180° - 2 \\cdot ' + bw + '° = ' + (180 - 2 * bw) + '°' }; }
          if (art === 'rw'){ a = zufallG(12, 78); if (a === 45) a = 46;
            return { art: art, schl: 'rw|' + a, soll: 90 - a, text: 'In einem rechtwinkligen Dreieck misst ein spitzer Winkel \\(' + a + '°\\). Wie gross ist der andere spitze Winkel?',
              falsch: [[180 - a, 'Der rechte Winkel braucht schon \\(90°\\). Für die beiden spitzen Winkel bleiben zusammen \\(90°\\).', '90'], [90 + a, 'Die beiden spitzen Winkel ergeben zusammen \\(90°\\).', 'plus']],
              tipp: 'Die beiden spitzen Winkel ergänzen sich zu \\(90°\\).', loes: '90° - ' + a + '° = ' + (90 - a) + '°' }; }
          // wv: β = k · α, γ gegeben → α
          var kf = zufall([2, 3]), al = zufallG(12, 40); if (al * (kf + 1) > 165) al = 30;
          var ga = 180 - al * (kf + 1);
          return { art: 'wv', schl: 'wv|' + kf + '|' + ga, soll: al, text: 'In einem Dreieck ist \\(\\beta\\) ' + (kf === 2 ? 'doppelt' : 'dreimal') + ' so gross wie \\(\\alpha\\), und \\(\\gamma = ' + ga + '°\\). Wie gross ist \\(\\alpha\\)?',
            falsch: [[(180 - ga) / kf, 'Das wäre \\(\\alpha\\), wenn \\(\\beta\\) fehlte. \\(\\alpha + \\beta = ' + (kf + 1) + '\\alpha\\).', 'k'], [180 - ga, 'Das ist \\(\\alpha + \\beta\\) zusammen. Teile durch \\(' + (kf + 1) + '\\).', 'zusammen'], [(180 - ga) / (kf + 1) * kf, 'Das ist \\(\\beta\\). Gefragt ist \\(\\alpha\\).', 'beta']],
            tipp: '\\(\\alpha + ' + kf + '\\alpha = 180° - \\gamma\\).', loes: (kf + 1) + '\\alpha = ' + (180 - ga) + '°,\\ \\alpha = ' + al + '°' }; },
        fehler: function(A){ return fehlerListe(A, 'w', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'w', e, A.soll, A.tipp, falschOhneSoll(A)); },
        loesung: function(A){ return A.loes; } },

      /* Dreiecke einteilen: aus zwei Winkeln die Art nach Winkeln und nach Seiten bestimmen (der dritte Winkel zählt mit). */
      'dreiecksart': { felder: ['w', 's'], muster: 'nach Winkeln {w:spitzwinklig|rechtwinklig|stumpfwinklig}; nach Seiten {s:gleichseitig|gleichschenklig|keine zwei gleich}',
        schl: function(A){ return 'da|' + A.sortiert.join('|'); },
        eingabe: function(A){ return { w: A.sw, s: A.ss }; },
        neu: function(){
          var fall = zufall(['spitz', 'spitz-gs', 'recht', 'recht-gs', 'stumpf', 'stumpf-gs', 'gleichseitig', 'spitz', 'stumpf']), w;
          if (fall === 'gleichseitig') w = [60, 60, 60];
          else if (fall === 'recht-gs') w = [45, 45, 90];
          else if (fall === 'recht'){ var p = zufallG(15, 75); if (p === 45) p = 40; w = [p, 90 - p, 90]; }
          else if (fall === 'spitz-gs'){ var bs = zufallG(46, 84); if (bs === 60) bs = 70; w = [bs, bs, 180 - 2 * bs]; }
          else if (fall === 'stumpf-gs'){ var b2 = zufallG(12, 44); w = [b2, b2, 180 - 2 * b2]; }
          else if (fall === 'stumpf'){ var gr = zufallG(95, 150), r = 180 - gr, k1 = zufallG(5, r - 5); if (k1 * 2 === r) k1 += 1; w = [k1, r - k1, gr]; }
          else { do { w = [zufallG(35, 85), zufallG(35, 85)]; w.push(180 - w[0] - w[1]); } while (w[2] >= 90 || w[2] < 10 || w[0] === w[1] || w[0] === w[2] || w[1] === w[2]); }
          w = mischen(w);
          var gegeben = [0, 1], m = Math.max(w[0], w[1], w[2]);
          var sw = m > 90 ? 'stumpfwinklig' : m === 90 ? 'rechtwinklig' : 'spitzwinklig';
          var ss = (w[0] === w[1] && w[1] === w[2]) ? 'gleichseitig' : (w[0] === w[1] || w[0] === w[2] || w[1] === w[2]) ? 'gleichschenklig' : 'keine zwei gleich';
          return { w: w, sortiert: w.slice().sort(function(x, y){ return x - y; }), sw: sw, ss: ss,
            text: 'Ein Dreieck hat die Winkel \\(\\alpha = ' + w[gegeben[0]] + '°\\) und \\(\\beta = ' + w[gegeben[1]] + '°\\). Was für ein Dreieck ist es?' }; },
        fehler: function(A){ var f = [];
          ['spitzwinklig', 'rechtwinklig', 'stumpfwinklig'].forEach(function(x){ if (x !== A.sw) f.push([{ w: x, s: A.ss }, null]); });
          ['gleichseitig', 'gleichschenklig', 'keine zwei gleich'].forEach(function(x){ if (x !== A.ss) f.push([{ w: A.sw, s: x }, null]); });
          return f; },
        gut: function(A){ return '\\(\\gamma = ' + A.w[2] + '°\\).'; },
        pruefen: function(A, e){
          var r = [], g = A.w[2];
          if (e.w !== A.sw){
            if (A.sw !== 'spitzwinklig' && Math.max(A.w[0], A.w[1]) < 90) r.push('Rechne zuerst den dritten Winkel aus: Er entscheidet hier über die Art.');
            else r.push('Nach Winkeln entscheidet der grösste Winkel: unter \\(90°\\) spitz-, genau \\(90°\\) recht-, über \\(90°\\) stumpfwinklig.');
          }
          if (e.s !== A.ss){
            if (A.ss === 'gleichseitig') r.push('Alle drei Winkel sind \\(60°\\): gleichseitig (das ist der speziellere Name).');
            else if (A.ss === 'gleichschenklig' && A.w[0] !== A.w[1]) r.push('Rechne den dritten Winkel aus: Zwei gleiche Winkel heissen zwei gleiche Seiten.');
            else if (A.ss === 'gleichschenklig') r.push('Zwei gleiche Winkel (Basiswinkel) heissen zwei gleiche Seiten.');
            else r.push('Gleiche Seiten gehören zu gleichen Winkeln — hier sind alle drei Winkel verschieden.');
          }
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return '\\gamma = ' + A.w[2] + '°:\\ \\text{' + A.sw + ', ' + A.ss + '}'; } },

      /* ── Kapitel 2 ── */
      /* Linie oder Punkt aus einer Beschreibung erkennen. */
      'element': { felder: ['e'], muster: '{e:Höhe|Seitenhalbierende|Winkelhalbierende|Mittelsenkrechte|Höhenschnittpunkt|Schwerpunkt|Inkreismittelpunkt|Umkreismittelpunkt}',
        eingabe: function(A){ return { e: A.soll }; },
        neu: function(){
          var e = zufall(['A', 'B', 'C']), and = ['A', 'B', 'C'].filter(function(x){ return x !== e; }), s = KL[e];
          var t = zufall([
            ['Diese Linie geht durch \\(' + e + '\\) und steht senkrecht auf der Geraden durch die Gegenseite \\(' + s + '\\).', 'Höhe'],
            ['Diese Linie verbindet \\(' + e + '\\) mit der Mitte der Gegenseite \\(' + s + '\\).', 'Seitenhalbierende'],
            ['Diese Linie teilt den Winkel \\(' + GRL[e] + '\\) in zwei gleiche Teile.', 'Winkelhalbierende'],
            ['Jeder Punkt dieser Linie ist von den Seiten \\(' + KL[and[0]] + '\\) und \\(' + KL[and[1]] + '\\) gleich weit entfernt.', 'Winkelhalbierende'],
            ['Diese Linie steht in der Mitte der Seite \\(' + s + '\\) senkrecht auf ihr.', 'Mittelsenkrechte'],
            ['Jeder Punkt dieser Linie ist von \\(' + and[0] + '\\) und \\(' + and[1] + '\\) gleich weit entfernt.', 'Mittelsenkrechte'],
            ['Dieser Punkt ist von allen drei Ecken gleich weit entfernt.', 'Umkreismittelpunkt'],
            ['Dieser Punkt ist von allen drei Seiten gleich weit entfernt.', 'Inkreismittelpunkt'],
            ['Dieser Punkt teilt jede Seitenhalbierende im Verhältnis \\(2 : 1\\).', 'Schwerpunkt'],
            ['In einem rechtwinkligen Dreieck liegt dieser Punkt genau auf der Ecke mit dem rechten Winkel.', 'Höhenschnittpunkt'],
            ['In ihm schneiden sich die drei Lote von den Ecken auf die Gegenseiten.', 'Höhenschnittpunkt']]);
          return { soll: t[1], text: t[0] + ' Wie heisst ' + (t[1].indexOf('punkt') >= 0 ? 'er' : 'sie') + '?' }; },
        fehler: function(A){ var paar = { 'Höhe': 'Mittelsenkrechte', 'Mittelsenkrechte': 'Höhe', 'Inkreismittelpunkt': 'Umkreismittelpunkt', 'Umkreismittelpunkt': 'Inkreismittelpunkt',
          'Seitenhalbierende': 'Mittelsenkrechte', 'Winkelhalbierende': 'Seitenhalbierende', 'Schwerpunkt': 'Inkreismittelpunkt', 'Höhenschnittpunkt': 'Umkreismittelpunkt' };
          return [[{ e: paar[A.soll] }, null]]; },
        pruefen: function(A, e){
          var s = A.soll, x = e.e;
          if (x === s) return null;
          var istPunkt = function(n){ return n.indexOf('punkt') >= 0; };
          if (istPunkt(x) !== istPunkt(s)) return istPunkt(s) ? 'Gesucht ist ein Punkt, keine Linie.' : 'Gesucht ist eine Linie, kein Punkt.';
          if (s === 'Höhe' && x === 'Mittelsenkrechte') return 'Beide stehen senkrecht — die Mittelsenkrechte geht aber durch die Seitenmitte, nicht durch die Ecke.';
          if (s === 'Mittelsenkrechte' && x === 'Höhe') return 'Beide stehen senkrecht — die Höhe geht aber durch die Ecke, nicht durch die Seitenmitte.';
          if (s === 'Mittelsenkrechte' && x === 'Seitenhalbierende') return 'Die Seitenhalbierende endet in der Ecke gegenüber und steht nicht senkrecht. Gleich weit von zwei Punkten: Mittelsenkrechte.';
          if (s === 'Seitenhalbierende' && x === 'Mittelsenkrechte') return 'Die Mittelsenkrechte steht senkrecht auf der Seite und geht nicht durch die Ecke.';
          if (s === 'Winkelhalbierende') return 'Gleich weit von zwei Seiten, einen Winkel in zwei gleiche Teile: Das tut die Winkelhalbierende.';
          if (s === 'Inkreismittelpunkt' && x === 'Umkreismittelpunkt') return 'Gleich weit von den <b>Ecken</b> ist der Umkreismittelpunkt. Hier sind es die <b>Seiten</b>.';
          if (s === 'Umkreismittelpunkt' && x === 'Inkreismittelpunkt') return 'Gleich weit von den <b>Seiten</b> ist der Inkreismittelpunkt. Hier sind es die <b>Ecken</b>.';
          if (s === 'Schwerpunkt') return 'Die Teilung \\(2 : 1\\) gehört zu den Seitenhalbierenden — und ihrem Schnittpunkt.';
          if (s === 'Höhenschnittpunkt') return 'Lote von den Ecken auf die Gegenseiten sind die Höhen.';
          return 'Lies genau: Ecke oder Seitenmitte, senkrecht oder nicht, Ecken oder Seiten?'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* Linien aus einer Ecke an der Figur erkennen: Höhe, Seitenhalbierende, Winkelhalbierende, in wechselnder Lage. */
      'linie-figur': { felder: ['n'], muster: 'Linie {n:1|2|3}',
        eingabe: function(A){ return { n: String(A.richtig) }; },
        neu: function(){
          var g, h, t, C, fussW, fuesse;
          for (var v = 0; v < 60; v++){
            g = zufall([6, 7, 8]); h = zufall([3, 3.5, 4, 4.5, 5]);
            t = zufall([g * zufall([0.1, 0.18, 0.26]), g * zufall([0.74, 0.82, 0.9]), -1, g + 1]);
            C = [t, h]; fussW = wfuss(C, [0, 0], [g, 0])[0]; fuesse = [t, g / 2, fussW];
            if (Math.abs(t - g / 2) >= 1.6 && Math.abs(fussW - t) >= 0.9 && Math.abs(fussW - g / 2) >= 0.9) break;
          }
          var linien = mischen([{ art: 'h', b: [t, 0] }, { art: 's', b: [g / 2, 0] }, { art: 'w', b: [fussW, 0] }]);
          var frage = zufall(['h', 's', 'w']), richtig = 1 + linien.findIndex(function(l){ return l.art === frage; });
          var nm = { h: 'Höhe', s: 'Seitenhalbierende', w: 'Winkelhalbierende' };
          return { g: g, h: h, t: t, C: C, linien: linien, frage: frage, richtig: richtig, dreh: zufall([0, 20, 70, 110, 160, 200, 250, 300]),
            text: 'Welche der drei Linien aus der Ecke ist die <b>' + nm[frage] + '</b> zur orangen Seite?' }; },
        zeichne: function(svg, A){
          var F = Flaeche(svg, { w: 280, h: 230, x0: A.g / 2 - 7.5, x1: A.g / 2 + 7.5, y0: A.h / 2 - 6.16, drehpunkt: [A.g / 2, A.h / 2], karo: false });
          F.drehen(grad(A.dreh));
          F.vieleck([[0, 0], [A.g, 0], A.C], 'figur');
          if (A.t < 0 || A.t > A.g) F.strecke(A.t < 0 ? [0, 0] : [A.g, 0], [A.t, 0], 'verlaengerung');
          F.strecke([0, 0], [A.g, 0], 'grundseite');
          A.linien.forEach(function(l, i){ F.strecke(A.C, l.b, 'kandidat-linie');
            F.text([A.C[0] * 0.3 + l.b[0] * 0.7, A.C[1] * 0.3 + l.b[1] * 0.7], String(i + 1), 'nummer', 0, -6); });
          F.drehen(0); },
        fehler: function(A){ return A.linien.map(function(l, i){ return l.art !== A.frage ? [{ n: String(i + 1) }, null] : null; }).filter(Boolean); },
        pruefen: function(A, e){
          var l = A.linien[+e.n - 1];
          if (l.art === A.frage) return null;
          var was = { h: 'Diese Linie steht senkrecht auf der Geraden der orangen Seite — die Höhe.', s: 'Diese Linie endet in der Mitte der orangen Seite — die Seitenhalbierende.',
            w: 'Diese Linie teilt den Winkel an der Ecke in zwei gleiche Teile — die Winkelhalbierende.' }[l.art];
          var ziel = { h: 'Gesucht ist die Linie, die senkrecht steht.', s: 'Gesucht ist die Linie zur Mitte der Seite.', w: 'Gesucht ist die Linie, die den Winkel halbiert — sie liegt zwischen Höhe und Seitenhalbierender.' }[A.frage];
          return was + ' ' + ziel; },
        loesung: function(A){ return '\\text{Linie ' + A.richtig + '}'; } },

      /* Rechnen mit den Elementen: Teilung 2 : 1, halbe Winkel, Winkel an Höhe und Winkelhalbierender. */
      'elem-rechnen': { felder: ['x'], muster: '{x} {einh}',
        schl: function(A){ return A.schl; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['sp', 'sp', 'wh', 'adc', 'hw']);
          if (art === 'sp'){ var s = zufall([4.5, 6, 7.2, 8.4, 9.6, 10.5, 12, 13.5, 15]), was = zufall(['ecke', 'mitte', 'ganz-e', 'ganz-m']);
            if (was === 'ecke') return { art: art, schl: 'sp|s|' + s, soll: r2(s * 2 / 3), einh: 'cm', text: 'Die Seitenhalbierende \\(s_a\\) ist \\(' + s + '\\,\\text{cm}\\) lang. Wie weit ist der Schwerpunkt \\(S\\) von \\(A\\) entfernt?',
              falsch: [[s / 2, 'Das ist die Mitte von \\(s_a\\). \\(S\\) teilt im Verhältnis \\(2 : 1\\), der längere Teil liegt bei der Ecke.', 'Mitte'], [s / 3, 'Das ist der kürzere Teil, von \\(S\\) bis zur Seitenmitte.', 'kurz']], tipp: '\\(\\overline{AS} = \\tfrac{2}{3}\\, s_a\\).', loes: '\\tfrac{2}{3} \\cdot ' + s + ' = ' + r2(s * 2 / 3) };
            if (was === 'mitte') return { art: art, schl: 'sp|m|' + s, soll: r2(s / 3), einh: 'cm', text: 'Die Seitenhalbierende \\(s_b\\) ist \\(' + s + '\\,\\text{cm}\\) lang. Wie weit ist der Schwerpunkt \\(S\\) von der Seitenmitte \\(M_b\\) entfernt?',
              falsch: [[s / 2, 'Das ist die Mitte von \\(s_b\\). \\(S\\) teilt im Verhältnis \\(2 : 1\\).', 'Mitte'], [s * 2 / 3, 'Das ist der längere Teil, von der Ecke bis \\(S\\).', 'lang']], tipp: '\\(\\overline{SM_b} = \\tfrac{1}{3}\\, s_b\\).', loes: '\\tfrac{1}{3} \\cdot ' + s + ' = ' + r2(s / 3) };
            if (was === 'ganz-e'){ var ce = r2(s * 2 / 3); return { art: art, schl: 'sp|ce|' + ce, soll: s, einh: 'cm', text: 'Der Schwerpunkt \\(S\\) ist \\(' + ce + '\\,\\text{cm}\\) von \\(C\\) entfernt. Wie lang ist die Seitenhalbierende \\(s_c\\)?',
              falsch: [[ce * 3, 'Das wäre richtig, wenn \\(' + ce + '\\,\\text{cm}\\) der kurze Teil wäre. \\(\\overline{CS}\\) ist der lange Teil: zwei Drittel.', 'drei'], [ce * 2, 'S liegt nicht in der Mitte: \\(\\overline{CS}\\) ist zwei Drittel von \\(s_c\\).', 'zwei']], tipp: '\\(\\overline{CS} = \\tfrac{2}{3}\\, s_c\\), also \\(s_c = \\tfrac{3}{2} \\cdot \\overline{CS}\\).', loes: '\\tfrac{3}{2} \\cdot ' + ce + ' = ' + s }; }
            var sm = r2(s / 3); return { art: art, schl: 'sp|sm|' + sm, soll: s, einh: 'cm', text: 'Der Schwerpunkt \\(S\\) ist \\(' + sm + '\\,\\text{cm}\\) von der Seitenmitte \\(M_c\\) entfernt. Wie lang ist die Seitenhalbierende \\(s_c\\)?',
              falsch: [[sm * 2, 'Das ist der Teil von \\(C\\) bis \\(S\\). Dazu kommt noch \\(\\overline{SM_c}\\).', 'Teil'], [sm * 1.5, 'Der kurze Teil ist ein Drittel der Seitenhalbierenden.', 'halb']], tipp: '\\(\\overline{SM_c} = \\tfrac{1}{3}\\, s_c\\).', loes: '3 \\cdot ' + sm + ' = ' + s }; }
          if (art === 'wh'){ var a = zufallG(14, 70) * 2; if (a === 90) a = 88;
            return { art: art, schl: 'wh|' + a, soll: a / 2, einh: '°', text: 'Im Dreieck ist \\(\\alpha = ' + a + '°\\). Welchen Winkel schliesst die Winkelhalbierende \\(w_\\alpha\\) mit der Seite \\(c\\) ein?',
              falsch: [[a, 'Das ist der ganze Winkel \\(\\alpha\\). Die Winkelhalbierende halbiert ihn.', 'ganz'], [90 - a, 'Die Winkelhalbierende steht nicht senkrecht — sie halbiert \\(\\alpha\\).', 'Höhe']], tipp: '\\(w_\\alpha\\) teilt \\(\\alpha\\) in zwei gleiche Teile.', loes: a + '° : 2 = ' + a / 2 + '°' }; }
          if (art === 'adc'){ var al, ga;
            do { al = zufallG(30, 100); ga = zufallG(14, 60) * 2; } while (al + ga > 165);
            return { art: art, schl: 'adc|' + al + '|' + ga, soll: 180 - al - ga / 2, einh: '°', text: 'Im Dreieck ist \\(\\alpha = ' + al + '°\\) und \\(\\gamma = ' + ga + '°\\). Die Winkelhalbierende \\(w_\\gamma\\) trifft die Seite \\(c\\) in \\(D\\). Wie gross ist der Winkel \\(\\angle ADC\\)?',
              falsch: [[180 - al - ga, 'Das ist \\(\\beta\\). Im Dreieck \\(ADC\\) liegt bei \\(C\\) nur die Hälfte von \\(\\gamma\\).', 'beta'], [180 - ga / 2, 'Im Dreieck \\(ADC\\) liegt auch \\(\\alpha\\) — Winkelsumme \\(180°\\).', 'ohne'], [al + ga / 2, 'Das ist der Nebenwinkel \\(\\angle BDC\\). Gesucht ist der Winkel bei \\(D\\) im Dreieck \\(ADC\\).', 'neben']],
              tipp: 'Im Dreieck \\(ADC\\): \\(\\alpha\\), \\(\\tfrac{\\gamma}{2}\\) und der gesuchte Winkel ergeben \\(180°\\).', loes: '180° - ' + al + '° - ' + ga / 2 + '° = ' + (180 - al - ga / 2) + '°' }; }
          var b = zufallG(20, 80); if (b === 45) b = 44;   // hw: Winkel zwischen h_c und b bei C
          return { art: 'hw', schl: 'hw|' + b, soll: 90 - b, einh: '°', text: 'Im Dreieck ist \\(\\alpha = ' + b + '°\\). Die Höhe \\(h_c\\) trifft \\(c\\) im Fusspunkt \\(F\\). Wie gross ist der Winkel zwischen \\(h_c\\) und der Seite \\(b\\) bei \\(C\\)?',
            falsch: [[b, 'Im Dreieck \\(AFC\\) liegen \\(\\alpha\\), der rechte Winkel bei \\(F\\) und der gesuchte Winkel.', 'alpha'], [b / 2, 'Die Höhe halbiert den Winkel nicht — sie steht senkrecht auf \\(c\\).', 'halb'], [180 - b, 'Im Dreieck \\(AFC\\) ist schon ein rechter Winkel: Für die beiden spitzen bleiben \\(90°\\).', '180']],
            tipp: 'Das Dreieck \\(AFC\\) ist rechtwinklig bei \\(F\\).', loes: '90° - ' + b + '° = ' + (90 - b) + '°' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.tipp, falschOhneSoll(A)); },
        loesung: function(A){ return A.loes; } },

      /* ── Kapitel 3 ── */
      /* Grundseite und Höhe zuordnen: spitze, rechtwinklige und stumpfe Dreiecke in wechselnder Lage (aus dem
         Leitprogramm Planimetrie übernommen). Drei nummerierte Linien, eine davon ist die Höhe zur orangen Grundseite. */
      'hoehe-figur': { felder: ['n'], muster: 'Die Höhe zur orangen Grundseite ist Linie {n:1|2|3}',
        eingabe: function(A){ return { n: String(A.richtig) }; },
        neu: function(){
          var g = zufall([5, 6, 7, 8]), h = zufall([2.5, 3, 3.5, 4]), art = zufall(['spitz', 'recht', 'stumpf']);
          var t = art === 'spitz' ? g * zufall([0.3, 0.45, 0.6]) : art === 'recht' ? zufall([0, g]) : zufall([-2, -1.5, g + 1.5, g + 2]);
          var C = [t, h], fuss = [t, 0], mi = [g / 2, 0];
          var linien = [{ art: 'h', a: C, b: fuss }, { art: 's', a: C, b: mi }, { art: 'seite', a: C, b: t < g / 2 ? [g, 0] : [0, 0] }];
          if (art === 'recht' || Math.abs(t - g / 2) < 0.6) linien[1] = { art: 'schief', a: C, b: [t < g / 2 ? Math.min(g - 0.3, t + 1.8) : Math.max(0.3, t - 1.8), 0] };
          linien = mischen(linien);
          var richtig = 1 + linien.findIndex(function(l){ return l.art === 'h'; });
          return { g: g, h: h, t: t, C: C, linien: linien, richtig: richtig, dreh: zufall([0, 25, 60, 120, 160, 200, 300]),
            text: 'Welche der drei nummerierten Linien ist die Höhe zur orangen Grundseite?' }; },
        zeichne: function(svg, A){
          var F = Flaeche(svg, { w: 280, h: 230, x0: A.g / 2 - 8, x1: A.g / 2 + 8, y0: A.h / 2 - 6.57, drehpunkt: [A.g / 2, A.h / 2], karo: false });
          F.drehen(grad(A.dreh));
          F.vieleck([[0, 0], [A.g, 0], A.C], 'figur');
          if (A.t < 0 || A.t > A.g) F.strecke(A.t < 0 ? [0, 0] : [A.g, 0], [A.t, 0], 'verlaengerung');
          F.strecke([0, 0], [A.g, 0], 'grundseite');
          A.linien.forEach(function(l, i){ F.strecke(l.a, l.b, 'kandidat-linie'); F.text([(l.a[0] * 0.4 + l.b[0] * 0.6), (l.a[1] * 0.4 + l.b[1] * 0.6)], String(i + 1), 'nummer', 9, 4, 'start'); });
          F.drehen(0); },
        fehler: function(A){ var f = [];
          A.linien.forEach(function(l, i){ if (l.art !== 'h') f.push([{ n: String(i + 1) }, l.art === 'seite' ? 'Seite' : l.art === 's' ? 'Mitte' : 'senkrecht']); });
          return f; },
        pruefen: function(A, e){
          var l = A.linien[+e.n - 1];
          if (l.art === 'h') return null;
          if (l.art === 'seite') return 'Das ist eine Seite des Dreiecks. Die Höhe steht <b>senkrecht</b> auf der Geraden durch die Grundseite — auch wenn die Figur gedreht ist.';
          if (l.art === 's') return 'Diese Linie endet in der Mitte der Grundseite — das ist die Seitenhalbierende. Die Höhe steht senkrecht auf der Grundseite.';
          return 'Diese Linie steht nicht senkrecht auf der Grundseite. Gesucht ist das Lot von der Spitze auf die Gerade durch die Grundseite.'; },
        loesung: function(A){ return '\\text{Linie ' + A.richtig + '}'; } },

      /* Fläche, Höhe, Grundseite, zweite Höhe und Umfang. */
      'flaeche': { felder: ['x'], muster: '{x} {einh}',
        schl: function(A){ return A.schl; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['A', 'A', 'h', 'g', 'zwei', 'zwei', 'umfang']), g, h, F_;
          if (art === 'A'){ g = zufall([4, 5, 7, 8, 9, 11, 12, 3.5, 4.5, 7.5]); h = zufall([3, 5, 6, 2.5, 3.6, 4.4, 7]); var misch = Math.random() < 0.35;
            if (misch) return { art: art, schl: 'fa|' + g + '|' + h, soll: r2(g * h / 2), einh: 'cm²', text: 'Grundseite \\(g = ' + r2(g / 100) + '\\,\\text{m}\\), zugehörige Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne die Fläche in \\(\\text{cm}^2\\).',
              falsch: [[g * h, '\\(g \\cdot h\\) ist das Rechteck — das Dreieck ist die <b>Hälfte</b>.', 'Hälfte'], [g / 100 * h / 2, 'Einheiten: \\(g\\) in m, \\(h\\) in cm — vorher angleichen.', 'Einheiten']],
              tipp: 'Zuerst die Einheiten angleichen: \\(g = ' + g + '\\,\\text{cm}\\), dann \\(A = \\tfrac{1}{2}\\, g \\cdot h\\).', loes: 'A = \\tfrac{1}{2} \\cdot ' + g + ' \\cdot ' + h + ' = ' + r2(g * h / 2) + '\\,\\text{cm}^2' };
            return { art: art, schl: 'fa|' + g + '|' + h, soll: r2(g * h / 2), einh: 'cm²', text: 'Grundseite \\(g = ' + g + '\\,\\text{cm}\\), zugehörige Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne die Fläche.',
              falsch: [[g * h, '\\(g \\cdot h\\) ist das Rechteck — das Dreieck ist die <b>Hälfte</b>.', 'Hälfte'], [g + h, 'Eine Fläche ist ein Produkt, keine Summe.', 'Summe']],
              tipp: '\\(A = \\tfrac{1}{2}\\, g \\cdot h\\).', loes: 'A = \\tfrac{1}{2} \\cdot ' + g + ' \\cdot ' + h + ' = ' + r2(g * h / 2) + '\\,\\text{cm}^2' }; }
          if (art === 'h' || art === 'g'){ g = zufall([4, 5, 6, 8, 10, 12, 7.5]); h = zufall([2, 3, 4, 5, 6, 1.5, 2.4, 4.8, 9]); F_ = r2(g * h / 2);
            if (art === 'h') return { art: art, schl: 'fh|' + F_ + '|' + g, soll: h, einh: 'cm', text: 'Ein Dreieck hat die Fläche \\(' + F_ + '\\,\\text{cm}^2\\) und die Grundseite \\(' + g + '\\,\\text{cm}\\). Wie weit ist die gegenüberliegende Ecke von der Geraden der Grundseite entfernt?',
              falsch: [[F_ / g, 'Das ist die Hälfte: \\(h = \\tfrac{2A}{g}\\) — die \\(\\tfrac{1}{2}\\) der Formel wandert als \\(2\\) nach oben.', 'Doppelte'], [F_ * g * 2, 'Teilen, nicht multiplizieren: \\(h = \\tfrac{2A}{g}\\).', 'teilen']],
              tipp: 'Der Abstand ist die Höhe: aus \\(A = \\tfrac{1}{2}\\, g \\cdot h\\) folgt \\(h = \\tfrac{2A}{g}\\).', loes: 'h = \\tfrac{2 \\cdot ' + F_ + '}{' + g + '} = ' + h + '\\,\\text{cm}' };
            return { art: art, schl: 'fg|' + F_ + '|' + h, soll: g, einh: 'cm', text: 'Ein Dreieck hat die Fläche \\(' + F_ + '\\,\\text{cm}^2\\), die Höhe zur Grundseite ist \\(' + h + '\\,\\text{cm}\\). Wie lang ist die Grundseite?',
              falsch: [[F_ / h, 'Das ist die Hälfte: \\(g = \\tfrac{2A}{h}\\).', 'Doppelte'], [F_ * h * 2, 'Teilen, nicht multiplizieren: \\(g = \\tfrac{2A}{h}\\).', 'teilen']],
              tipp: '\\(g = \\tfrac{2A}{h}\\).', loes: 'g = \\tfrac{2 \\cdot ' + F_ + '}{' + h + '} = ' + g + '\\,\\text{cm}' }; }
          if (art === 'zwei'){ var a, ha, b;
            do { a = zufall([5, 6, 7, 8, 9, 10, 12]); ha = zufall([2, 3, 4, 4.5, 5, 6]); b = zufall([4, 5, 6, 7.5, 8, 10]); } while (a === b);
            return { art: art, schl: 'fz|' + a + '|' + ha + '|' + b, soll: r2(a * ha / b), einh: 'cm', text: 'Im Dreieck ist \\(a = ' + a + '\\,\\text{cm}\\), die Höhe \\(h_a = ' + ha + '\\,\\text{cm}\\) und \\(b = ' + b + '\\,\\text{cm}\\). Wie lang ist die Höhe \\(h_b\\)?',
              falsch: [[b * ha / a, 'Verkehrt: Zur kürzeren Seite gehört die längere Höhe. Rechne zuerst die Fläche, dann \\(h_b = \\tfrac{2A}{b}\\).', 'verkehrt'], [a * ha / 2, 'Das ist die Fläche. Daraus folgt die Höhe: \\(h_b = \\tfrac{2A}{b}\\).', 'Fläche'], [a * ha / 2 / b, 'Aus \\(A = \\tfrac{1}{2}\\, b \\cdot h_b\\) folgt \\(h_b = \\tfrac{2A}{b}\\) — das Doppelte.', 'Hälfte']],
              tipp: 'Beide Höhen gehören zur selben Fläche: \\(A = \\tfrac{1}{2}\\, a \\cdot h_a = \\tfrac{1}{2}\\, b \\cdot h_b\\).', loes: 'A = ' + r2(a * ha / 2) + ',\\ h_b = \\tfrac{2A}{b} \\approx ' + r2(a * ha / b) + '\\,\\text{cm}' }; }
          // Umfang: gleichschenklig (Basis, Schenkel ↔ Umfang) oder gleichseitig
          var v = zufall(['gsU', 'gsS', 'glS']);
          if (v === 'gsU'){ var bs = zufall([4, 5, 6, 7, 8, 9.5]), sk = zufall([5, 6, 7.5, 8, 9, 11]); if (sk * 2 <= bs) sk = bs;
            return { art: 'umfang', schl: 'fu|gsU|' + bs + '|' + sk, soll: r2(bs + 2 * sk), einh: 'cm', text: 'Ein gleichschenkliges Dreieck hat die Basis \\(' + bs + '\\,\\text{cm}\\) und die Schenkel je \\(' + sk + '\\,\\text{cm}\\). Wie gross ist der Umfang?',
              falsch: [[bs + sk, 'Es gibt zwei Schenkel.', 'zwei'], [2 * bs + sk, 'Die Basis zählt einmal, die Schenkel zweimal.', 'verkehrt']], tipp: '\\(U = \\text{Basis} + 2 \\cdot \\text{Schenkel}\\).', loes: 'U = ' + bs + ' + 2 \\cdot ' + sk + ' = ' + r2(bs + 2 * sk) + '\\,\\text{cm}' }; }
          if (v === 'gsS'){ var bs2 = zufall([4, 5, 6, 8, 10]), sk2 = zufall([5, 6, 7, 8.5, 9, 12]), U = bs2 + 2 * sk2;
            return { art: 'umfang', schl: 'fu|gs|' + bs2 + '|' + U, soll: sk2, einh: 'cm', text: 'Ein gleichschenkliges Dreieck hat den Umfang \\(' + U + '\\,\\text{cm}\\) und die Basis \\(' + bs2 + '\\,\\text{cm}\\). Wie lang ist ein Schenkel?',
              falsch: [[U - bs2, 'Das sind beide Schenkel zusammen.', 'zwei'], [(U - bs2) / 3, 'Die Basis ist schon abgezogen; es bleiben zwei Schenkel.', 'drei']], tipp: 'Umfang minus Basis, dann durch \\(2\\).', loes: '(' + U + ' - ' + bs2 + ') : 2 = ' + sk2 + '\\,\\text{cm}' }; }
          var U3 = zufall([12, 15, 16.5, 18, 21, 22.5, 24, 27, 30]);
          return { art: 'umfang', schl: 'fu|gl|' + U3, soll: r2(U3 / 3), einh: 'cm', text: 'Ein gleichseitiges Dreieck hat den Umfang \\(' + U3 + '\\,\\text{cm}\\). Wie lang ist eine Seite?',
            falsch: [[U3 / 2, 'Ein Dreieck hat drei gleiche Seiten.', 'drei'], [U3 * 3, 'Der Umfang ist schon die Summe der drei Seiten: teilen.', 'teilen']], tipp: 'Drei gleiche Seiten: \\(U = 3s\\).', loes: U3 + ' : 3 = ' + r2(U3 / 3) + '\\,\\text{cm}' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.tipp, falschOhneSoll(A)); },
        loesung: function(A){ return A.loes; } },

      /* ── Kapitel 4 ── */
      /* Pythagoras an der Figur: rechtwinkliges Dreieck in wechselnder Lage, gesucht die Seite x — Hypotenuse oder Kathete. */
      'pyth-figur': { felder: ['x'], muster: 'x ≈ {x} cm',
        schl: function(A){ return A.hyp ? 'ph|' + Math.min(A.p, A.q) + '|' + Math.max(A.p, A.q) : 'pk|' + A.c + '|' + A.p; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var p = zufall([2, 3, 4, 5, 6, 7, 8, 9, 1.5, 2.5, 4.5, 7.5]), q = zufall([3, 4, 5, 6, 8, 10, 12, 2.5, 5.5]), hyp = Math.random() < 0.5;
          if (p === q) q += 1;
          if (Math.max(p, q) / Math.min(p, q) > 3) return TYPEN['pyth-figur'].neu();   // keine zu spitzen Figuren
          var c = r2(Math.hypot(p, q)), A = { p: p, q: q, hyp: hyp, dreh: zufall([0, 35, 90, 140, 200, 250, 310]), spiegel: Math.random() < 0.5 };
          if (hyp){ A.soll = r2(Math.hypot(p, q)); A.lab = [String(p), String(q), 'x'];
            A.falsch = [[Math.sqrt(Math.abs(q * q - p * p)), 'Die gesuchte Seite liegt dem rechten Winkel gegenüber: Sie ist die Hypotenuse. Für die Hypotenuse werden die Quadrate <b>addiert</b>.', 'addieren'], [p + q, 'Nicht die Längen addieren, sondern die Quadrate — dann die Wurzel.', 'Quadrate'], [p * p + q * q, 'Das ist \\(x^2\\). Zieh noch die Wurzel.', 'Wurzel']]; }
          else { // gegeben Hypotenuse c (gerundet nicht: aus einem Tripel oder halben cm) und Kathete p
            c = zufall([5, 6.5, 7.5, 8, 10, 12.5, 13, 15]); p = zufall([2, 3, 4, 4.5, 5, 6, 2.5, 3.5].filter(function(x){ return x < c - 0.5 && x >= c / 3.2 && Math.sqrt(c * c - x * x) / x <= 3; }));
            A.c = c; A.p = p; A.q = Math.sqrt(c * c - p * p); A.soll = r2(A.q); A.lab = [String(p), 'x', String(c)];
            A.falsch = [[Math.hypot(c, p), 'Die längste Seite ist gegeben: die Hypotenuse (gegenüber dem rechten Winkel). Für eine Kathete wird <b>subtrahiert</b>.', 'subtrahieren'], [c - p, 'Nicht die Längen subtrahieren, sondern die Quadrate — dann die Wurzel.', 'Quadrate'], [c * c - p * p, 'Das ist \\(x^2\\). Zieh noch die Wurzel.', 'Wurzel']]; }
          A.text = 'Im rechtwinkligen Dreieck sind zwei Seiten gegeben (in cm). Wie lang ist die Seite \\(x\\)?';
          return A; },
        zeichne: function(svg, A){
          var a = A.hyp ? A.p : A.p, b = A.hyp ? A.q : A.q, m = 6 / Math.max(a, b), sy = A.spiegel ? -1 : 1;
          var R = [0, 0], P = [a * m, 0], Q = [0, sy * b * m], cx = (P[0] + Q[0]) / 3, cy = (P[1] + Q[1]) / 3;
          var F = Flaeche(svg, { w: 280, h: 240, x0: cx - 6, x1: cx + 6, y0: cy - 5.14, drehpunkt: [cx, cy], karo: false });
          F.drehen(grad(A.dreh));
          F.vieleck([R, P, Q], 'figur'); F.rechts(R, [1, 0], [0, sy], '');
          [[R, P, A.lab[0]], [R, Q, A.lab[1]], [P, Q, A.lab[2]]].forEach(function(s){ var mm = mitte(s[0], s[1]), d = [mm[0] - cx, mm[1] - cy], n = Math.hypot(d[0], d[1]) || 1;
            F.text([mm[0] + d[0] / n * 0.75, mm[1] + d[1] / n * 0.75], s[2], s[2] === 'x' ? 'mass gesucht' : 'mass gross', 0, 4); });
          F.drehen(0); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.hyp ? '\\(x\\) liegt dem rechten Winkel gegenüber: \\(x = \\sqrt{a^2 + b^2}\\).' : 'Die Hypotenuse ist gegeben: \\(x = \\sqrt{c^2 - a^2}\\).', falschOhneSoll(A)); },
        loesung: function(A){ return A.hyp ? 'x = \\sqrt{' + A.p + '^2 + ' + A.q + '^2} \\approx ' + A.soll : 'x = \\sqrt{' + A.c + '^2 - ' + A.p + '^2} \\approx ' + A.soll; } },

      /* Pythagoras in Anwendungen: Höhe und Schenkel im gleichschenkligen Dreieck, Höhe und Fläche im gleichseitigen, Leiter. */
      'pyth-anwendung': { felder: ['x'], muster: '{x} {einh}',
        schl: function(A){ return A.schl; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['gsh', 'gsh', 'gss', 'glh', 'gla', 'lh']);
          if (art === 'gsh'){ var g = zufall([4, 6, 8, 10, 12, 7, 9]), s = zufall([5, 6, 7, 8.5, 9, 10, 13].filter(function(x){ return x > g / 2 + 0.6; }));
            var h = Math.sqrt(s * s - g * g / 4);
            return { art: art, schl: 'gsh|' + g + '|' + s, soll: r2(h), einh: 'cm', text: 'Ein gleichschenkliges Dreieck hat die Basis \\(' + g + '\\,\\text{cm}\\) und die Schenkel je \\(' + s + '\\,\\text{cm}\\). Wie hoch ist es (Höhe auf die Basis)?',
              falsch: [[Math.sqrt(Math.max(0, s * s - g * g)), 'Die Höhe halbiert die Basis: Rechne mit der <b>halben</b> Basis.', 'halbe'], [Math.sqrt(s * s + g * g / 4), 'Der Schenkel ist die Hypotenuse der Hälfte, die längste Seite. Für die Kathete \\(h\\) wird subtrahiert.', 'subtrahieren'], [s - g / 2, 'Nicht die Längen subtrahieren, sondern die Quadrate.', 'Quadrate']],
              tipp: 'Die Hälfte ist rechtwinklig: Hypotenuse = Schenkel, Katheten = halbe Basis und \\(h\\).', loes: 'h = \\sqrt{' + s + '^2 - ' + g / 2 + '^2} \\approx ' + r2(h) + '\\,\\text{cm}' }; }
          if (art === 'gss'){ var g2 = zufall([6, 8, 10, 4.8, 7.2, 12]), h2 = zufall([2, 3, 4, 4.5, 5, 6, 2.4]);
            var s2 = Math.hypot(g2 / 2, h2);
            // bewusst kein Dachgiebel: den kombiniert der Gesamttest (G6) mit Fläche und Umfang
            return { art: art, schl: 'gss|' + g2 + '|' + h2, soll: r2(s2), einh: 'cm', text: 'Ein gleichschenkliges Dreieck hat die Basis \\(' + g2 + '\\,\\text{cm}\\) und die Höhe \\(' + h2 + '\\,\\text{cm}\\) auf die Basis. Wie lang ist ein Schenkel?',
              falsch: [[Math.hypot(g2, h2), 'Die Höhe halbiert die Basis: Rechne mit der <b>halben</b> Basis.', 'halbe'], [g2 / 2 + h2, 'Nicht die Längen addieren, sondern die Quadrate — dann die Wurzel.', 'Quadrate']],
              tipp: 'Halbes Dreieck: Katheten halbe Basis und Höhe, der Schenkel ist die Hypotenuse.', loes: 's = \\sqrt{' + g2 / 2 + '^2 + ' + h2 + '^2} \\approx ' + r2(s2) + '\\,\\text{cm}' }; }
          if (art === 'glh' || art === 'gla'){ var a = zufall([3, 4, 5, 7, 9, 12, 2.5, 4.5, 7.5]), hh = a / 2 * Math.sqrt(3);
            if (art === 'glh') return { art: art, schl: 'glh|' + a, soll: r2(hh), einh: 'cm', text: 'Ein gleichseitiges Dreieck hat die Seite \\(' + a + '\\,\\text{cm}\\). Wie hoch ist es?',
              falsch: [[Math.sqrt(a * a + a * a / 4), 'Die Seite ist die Hypotenuse der Hälfte. Für die Kathete \\(h\\) wird subtrahiert.', 'subtrahieren'], [a / 2, 'Das ist die halbe Seite — eine Kathete. Gesucht ist die andere Kathete.', 'halbe'], [a * a * 3 / 4, 'Das ist \\(h^2\\). Zieh noch die Wurzel.', 'Wurzel']],
              tipp: '\\(h = \\sqrt{s^2 - (\\tfrac{s}{2})^2}\\).', loes: 'h = \\sqrt{' + a + '^2 - ' + a / 2 + '^2} \\approx ' + r2(hh) + '\\,\\text{cm}' };
            return { art: art, schl: 'gla|' + a, soll: r2(a * hh / 2), einh: 'cm²', text: 'Ein gleichseitiges Dreieck hat die Seite \\(' + a + '\\,\\text{cm}\\). Wie gross ist seine Fläche?',
              falsch: [[a * hh, 'Das \\(\\tfrac{1}{2}\\) fehlt: \\(A = \\tfrac{1}{2}\\, s \\cdot h\\).', 'Hälfte'], [a * a / 2, 'Die Seite ist keine Höhe. Zuerst \\(h\\) mit Pythagoras.', 'Höhe']],
              tipp: 'Zuerst die Höhe \\(h = \\sqrt{s^2 - (\\tfrac{s}{2})^2}\\), dann \\(A = \\tfrac{1}{2}\\, s \\cdot h\\).', loes: 'h \\approx ' + r2(hh) + ',\\ A = \\tfrac{1}{2} \\cdot ' + a + ' \\cdot h \\approx ' + r2(a * hh / 2) + '\\,\\text{cm}^2' }; }
          var L = zufall([3, 3.5, 4, 5, 6, 7.5]), d = zufall([0.8, 1, 1.2, 1.5, 1.8, 2].filter(function(x){ return x < L / 2.5; })), hl = Math.sqrt(L * L - d * d);
          return { art: 'lh', schl: 'lh|' + L + '|' + d, soll: r2(hl), einh: 'm', text: 'Eine \\(' + L + '\\,\\text{m}\\) lange Leiter lehnt an einer senkrechten Wand, ihr Fuss steht \\(' + d + '\\,\\text{m}\\) von der Wand entfernt. Wie hoch reicht sie?',
            falsch: [[Math.hypot(L, d), 'Die Leiter ist die Hypotenuse, die längste Seite. Für die Höhe an der Wand wird subtrahiert.', 'subtrahieren'], [L - d, 'Nicht die Längen subtrahieren, sondern die Quadrate.', 'Quadrate']],
            tipp: 'Wand, Boden und Leiter bilden ein rechtwinkliges Dreieck; die Leiter ist die Hypotenuse.', loes: '\\sqrt{' + L + '^2 - ' + d + '^2} \\approx ' + r2(hl) + '\\,\\text{m}' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.tipp, falschOhneSoll(A)); },
        loesung: function(A){ return A.loes; } }
    };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'), zaehler = box.querySelector('.ue-serie');
      function neu(){
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="decimal" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        if (T.vorbereiten) T.vorbereiten(box, A);
        var bild = box.querySelector('.ue-bild');
        if (bild){ while (bild.firstChild) bild.removeChild(bild.firstChild); if (T.zeichne) T.zeichne(bild, A); }
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){ var r = zahl(i.value); e[i.dataset.f] = r.wert; if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true; i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>12</code> oder <code>4.8</code> — ohne Einheit.'; return; }
        versuche++;
        var f = T.pruefen(A, e);
        if (f === null){
          serie = versuche === 1 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + (T.gut ? '. ' + T.gut(A) : '') + ' <button type="button" class="ue-weiter">Nächste</button>';
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

  /* ---------- Figuren zu den Aufgaben: <svg class="geo-mini" data-fig='[…]' data-fenster="x0,x1,y0">
       Einträge: ["v", [[x,y],…], cls] Vieleck · ["s", [x,y], [x,y], cls] Strecke · ["g", [x,y], [x,y], cls] Gerade ·
       ["k", [x,y], r, cls] Kreis · ["t", [x,y], "Text", cls, dx, dy, anker] · ["p", [x,y]] Punkt ·
       ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel · ["w", Scheitel, [x,y], [x,y], "Text", rpx] Winkelbogen. ---------- */
  document.querySelectorAll('svg.geo-mini[data-fig]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-1,9,-1').split(',').map(Number), b = +(svg.dataset.breite || 220), h = +(svg.dataset.hoehe || 150);
    var F = Flaeche(svg, { w: b, h: h, x0: fe[0], x1: fe[1], y0: fe[2], karo: svg.dataset.karo === 'ja' ? 1 : false });
    JSON.parse(svg.dataset.fig).forEach(function(e){
      var t = e[0];
      if (t === 'v') F.vieleck(e[1], e[2] || 'figur');
      else if (t === 's') F.strecke(e[1], e[2], e[3] || 'hilfe');
      else if (t === 'g') F.gerade(e[1], e[2], e[3] || 'hilfe2');
      else if (t === 'k') F.kreis(e[1], e[2], e[3] || 'umkreis');
      else if (t === 't') F.text(e[1], e[2], e[3] || 'mass', e[4], e[5], e[6]);
      else if (t === 'p') F.punkt(e[1]);
      else if (t === 'r') F.rechts(e[1], e[2], e[3], '');
      else if (t === 'w') winkelMarke(F, e[1], e[2], e[3], e[5] || 20, 'winkelbogen', e[4], 'winkel klein');
    });
    svg.setAttribute('role', 'img');
  });
})();
</script>
