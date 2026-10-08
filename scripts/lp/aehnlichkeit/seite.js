<script>
/* Leitprogramm Zentrische Streckung und Ähnlichkeit — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit
   Rückmeldung, Figuren zu den Aufgaben. Gerüst (Flaeche, Leiste, arbeitsbereich, Übungsrahmen) wie im Leitprogramm
   Trigonometrische Berechnungen (scripts/lp/trigonometrische-berechnungen/seite.js) und Planimetrie; neu sind das
   Achsenkreuz der Zeichenfläche, Regler ohne Null, mehrfache Winkelbögen und die Inhalte.
   Notation wie auf der Themenseite 5.2d: Zentrum Z, Streckfaktor k, Bildpunkt P′; Strahlensätze mit S, A, B, A′, B′
   und AB ∥ A′B′; ähnliche Figuren F₁ ~ F₂; im rechtwinkligen Dreieck rechter Winkel bei C, Höhe h, Fusspunkt H,
   Hypotenusenabschnitte p (an a) und q (an b).
   Eine Farbe, eine Bedeutung (wie in den Clips und auf der Themenseite): blau = Original, Figur · orange = Bild,
   Streckfaktor, Hilfslinie · grün = Gesuchtes, Ergebnis · rot = Fehler. Dezimalpunkt; gerundet mit «≈». */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', PI = Math.PI;
  function z(n, st){ var f = Math.pow(10, st == null ? 2 : st), r = Math.round(n * f) / f; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  /* gerundete Werte mit «≈» und fester Stellenzahl (19.20, nicht 19.2), exakte mit «=» */
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
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^≈/, '').replace(/°$/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  /* Vergleich gerundeter Ergebnisse: richtig auf zwei Dezimalen (Toleranz 0.006, bei Winkeln aus
     gerundeten Zwischenwerten 0.011); «nah» heisst: richtig gerechnet, aber zu grob gerundet. */
  function stimmt(e, soll, tol){ return Math.abs(e - soll) <= (tol || 0.006) + 1e-9; }
  function nah(e, soll, tol){ return !stimmt(e, soll, tol) && Math.abs(e - soll) <= Math.max(0.06, Math.abs(soll) * 0.005); }
  var RUNDEN = 'Fast — runde auf zwei Dezimalen (Zwischenresultate ungerundet weiterverwenden).';
  var RAD = 'Dein Rechner steht im Bogenmass (RAD). Stell ihn auf Grad (DEG) und rechne nochmals.';
  function grad(w){ return w * PI / 180; }
  function sinG(w){ return Math.sin(grad(w)); } function cosG(w){ return Math.cos(grad(w)); } function tanG(w){ return Math.tan(grad(w)); }
  function asinG(v){ return Math.asin(v) * 180 / PI; } function acosG(v){ return Math.acos(v) * 180 / PI; } function atanG(v){ return Math.atan(v) * 180 / PI; }

  /* ---------- Zeichenfläche in Weltkoordinaten (1 Einheit = 1 cm bzw. 1 m, beide Achsen gleich) ---------- */
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
    if (o.achsen){   // Achsen mit Pfeil in positiver Richtung und Namen am Pfeil (HOWTO-leitprogramme §10)
      var t = o.achsen.teil || 2, ax = X(0), ay = Y(0);
      el(g, 'line', { x1: 0, y1: ay, x2: W - 2, y2: ay, 'class': 'achse' });
      el(g, 'line', { x1: ax, y1: H, x2: ax, y2: 2, 'class': 'achse' });
      el(g, 'polygon', { points: (W - 1) + ',' + ay + ' ' + (W - 8) + ',' + (ay - 3.5) + ' ' + (W - 8) + ',' + (ay + 3.5), 'class': 'pfeil' });
      el(g, 'polygon', { points: ax + ',1 ' + (ax - 3.5) + ',8 ' + (ax + 3.5) + ',8', 'class': 'pfeil' });
      el(g, 'text', { x: W - 6, y: ay - 7, 'text-anchor': 'end', 'class': 'achsname' }, 'x');
      el(g, 'text', { x: ax + 8, y: 12, 'class': 'achsname' }, 'y');
      // Achsenzahlen nur, wo sie ganz ins Bild passen (Übungsbilder mit wechselndem Fenster: Zahl am Rand sonst halb abgeschnitten)
      for (i = Math.ceil(x0 / t) * t; i <= x1 - 1; i += t) if (Math.abs(i) > 1e-9 && X(i) > 9 && X(i) < W - 9 && ay + 15 < H) el(g, 'text', { x: X(i), y: ay + 11, 'text-anchor': 'middle', 'class': 'achszahl' }, String(i).replace('-', '−'));
      for (i = Math.ceil(y0 / t) * t; i <= y1 - 1; i += t) if (Math.abs(i) > 1e-9 && ax - 4 - 6 * String(i).length > 0 && Y(i) > 6 && Y(i) < H - 7) el(g, 'text', { x: ax - 4, y: Y(i) + 3.5, 'text-anchor': 'end', 'class': 'achszahl' }, String(i).replace('-', '−'));
    }
    var ebene = el(svg, 'g', {});
    var rot = 0, dreh = function(p){ if (!rot) return p; var c = Math.cos(rot), sn = Math.sin(rot), m = o.drehpunkt || [0, 0];
      return [m[0] + (p[0] - m[0]) * c - (p[1] - m[1]) * sn, m[1] + (p[0] - m[0]) * sn + (p[1] - m[1]) * c]; };
    function P(p){ p = dreh(p); return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }
    var F = {
      s: s, ebene: ebene,
      drehen: function(w){ rot = w; },
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      vieleck: function(pts, cls){ return el(ebene, 'polygon', { points: pts.map(P).join(' '), 'class': cls }); },
      strecke: function(a, b, cls){ var A = dreh(a), B = dreh(b); return el(ebene, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': cls }); },
      gerade: function(a, b, cls){   // ganze Gerade durch a und b, am Bild abgeschnitten
        var dx = b[0] - a[0], dy = b[1] - a[1], L = 100 / Math.hypot(dx, dy);
        return F.strecke([a[0] - dx * L, a[1] - dy * L], [a[0] + dx * L, a[1] + dy * L], cls); },
      strahl: function(a, w, cls){ return F.strecke(a, [a[0] + 100 * Math.cos(w), a[1] + 100 * Math.sin(w)], cls); },
      kreis: function(m, r, cls){ var M = dreh(m); return el(ebene, 'circle', { cx: X(M[0]), cy: Y(M[1]), r: r * s, 'class': cls }); },
      /* Winkelbogen um m von Richtung w0 bis w1 (Bogenmass, gegen den Uhrzeigersinn), Radius in Pixeln */
      bogen: function(m, w0, w1, rpx, cls){
        var r = rpx / s, a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var A = dreh(a), B = dreh(b), gross = (w1 - w0) > PI ? 1 : 0;
        return el(ebene, 'path', { d: 'M' + X(A[0]) + ' ' + Y(A[1]) + ' A' + rpx + ' ' + rpx + ' 0 ' + gross + ' 0 ' + X(B[0]) + ' ' + Y(B[1]), 'class': cls }); },
      punkt: function(p, cls){ var A = dreh(p); return el(ebene, 'circle', { cx: X(A[0]), cy: Y(A[1]), r: 3.5, 'class': cls || 'g-pkt' }); },
      text: function(p, t, cls, dx, dy, anker){ var A = dreh(p);
        return el(ebene, 'text', { x: X(A[0]) + (dx || 0), y: Y(A[1]) + (dy || 0), 'text-anchor': anker || 'middle', 'class': 'g-text ' + (cls || '') }, t); },
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
        /* Treffstreifen einer Seite an beiden Enden gekürzt (bis 9 px, höchstens ein Viertel): Sonst überdecken sich die
           16 px breiten Streifen zweier Seiten an der gemeinsamen Ecke, und bei kurzen Seiten trifft ein Tipp auf die
           Linie die Nachbarseite (Prüfung 08.10.2026: A′B′ bei k = −1 nur zu 55 % treffbar). */
        var t0 = ganz ? 0 : Math.min(0.25, 9 / (Math.hypot(X(B[0]) - X(A[0]), Y(B[1]) - Y(A[1])) || 1));
        var Ta = [A[0] + (B[0] - A[0]) * t0, A[1] + (B[1] - A[1]) * t0], Tb = [B[0] - (B[0] - A[0]) * t0, B[1] - (B[1] - A[1]) * t0];
        el(gr, 'line', { x1: X(Ta[0]), y1: Y(Ta[1]), x2: X(Tb[0]), y2: Y(Tb[1]), 'class': 'k-treffer' });
        gr.addEventListener('click', function(){ wahl(id); });
        gr.addEventListener('keydown', function(ev){ if (ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); wahl(id); } });
        return gr; }
    };
    return F;
  }
  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function richtung(p, q){ return Math.atan2(q[1] - p[1], q[0] - p[0]); }
  /* Winkel bei p zwischen den Richtungen zu a und zu b: Bogen gegen den Uhrzeigersinn, Beschriftung auf der
     Winkelhalbierenden. */
  function winkelMarke(F, p, a, b, rpx, cls, text, tcls){
    var w0 = richtung(p, a), w1 = richtung(p, b);
    while (w1 < w0) w1 += 2 * PI;
    if (w1 - w0 > PI){ var t = w0; w0 = w1; w1 = t + 2 * PI; }
    F.bogen(p, w0, w1, rpx, cls);
    if (text){ var wm = (w0 + w1) / 2, r = (rpx + 11) / F.s;
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

  /* ---------- Geometrie-Arbeitsbereich (wie im Leitprogramm Planimetrie) ----------
     arbeitsbereich(id, { fenster, zeichnen(F, w, k), aufgaben }) — jede Aufgabe:
       text, setup(sim) (Regler setzen: sim.setze({ x: 40 }), sim.sperre('x')),
       wahl: { richtig: 'gk', rueck: { id: 'Text' } }      — Linie antippen
       frage: [{ name, label, einheit, soll, tol, fehler: [[wert, 'Text']] }] — Grössen eingeben
       ziel: function(w) — Reglerzustand (w = Werte der Regler, w.bewegt); probe: ein Zustand, der es löst
       fest: { … } — Werte, die die Figur statt der Regler zeigt (nicht auf dem Reglerraster) */
  function arbeitsbereich(id, o){
    var fig = document.getElementById(id); if (!fig) return;
    var F = Flaeche(fig.querySelector('svg'), o.fenster), regler = {}, bewegt = {}, aufgabe = null, gewaehlt = null, richtig = false, pruefen = function(){};
    var ein = fig.querySelector('.g-eingabe'), rueck = fig.querySelector('.g-rueck'), formel = fig.querySelector('[data-rolle="formel"]');
    fig.querySelectorAll('input[type=range]').forEach(function(inp){
      regler[inp.dataset.p] = inp;
      inp.addEventListener('input', function(){
        // Regler ohne Null (Streckfaktor): springt über 0 hinweg, bevor gezeichnet wird (HOWTO §15 «ohneNull»)
        if ((o.ohneNull || []).indexOf(inp.dataset.p) >= 0 && +inp.value === 0) inp.value = (inp.__letzt || 0) > 0 ? -(+inp.step) : +inp.step;
        inp.__letzt = +inp.value;
        bewegt[inp.dataset.p] = true; zeichnen(); });
    });
    function werte(){
      var w = { bewegt: bewegt };
      for (var k in regler) w[k] = +regler[k].value;
      return w;
    }
    /* Anzeige neben den Reglern aus den Werten, die die Figur zeigt (mit `fest`), die gesuchte Grösse als «?» */
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
      else meldung('falsch', r.filter(function(t, j){ return r.indexOf(t) === j; }).join(' '));   // gleiche Meldung zweier Felder nur einmal
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

  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function richtung(p, q){ return Math.atan2(q[1] - p[1], q[0] - p[0]); }
  function dist(p, q){ return Math.hypot(q[0] - p[0], q[1] - p[1]); }
  /* Winkel bei p zwischen den Richtungen zu a und zu b: Bogen gegen den Uhrzeigersinn, Beschriftung auf der
     Winkelhalbierenden. anzahl: 1–3 Bögen (gleich markierte Winkel sind gleich gross). */
  function winkelMarke(F, p, a, b, rpx, cls, text, tcls, anzahl){
    var w0 = richtung(p, a), w1 = richtung(p, b);
    while (w1 < w0) w1 += 2 * PI;
    if (w1 - w0 > PI){ var t = w0; w0 = w1; w1 = t + 2 * PI; }
    for (var j = 0; j < (anzahl || 1); j++) F.bogen(p, w0, w1, rpx + 4 * j, cls);
    if (text){ var wm = (w0 + w1) / 2, r = (rpx + 4 * ((anzahl || 1) - 1) + 12) / F.s;
      F.text([p[0] + r * Math.cos(wm), p[1] + r * Math.sin(wm)], text, tcls || 'winkel', 0, 4); }
  }
  /* Beschriftung neben einer Strecke, auf der Seite weg vom Punkt «weg» (z. B. dem Schwerpunkt). */
  function seitenText(F, p, q, text, cls, weg, abst){
    var m = mitte(p, q), n = [-(q[1] - p[1]), q[0] - p[0]], l = Math.hypot(n[0], n[1]);
    n = [n[0] / l, n[1] / l];
    if (weg && (n[0] * (weg[0] - m[0]) + n[1] * (weg[1] - m[1])) > 0) n = [-n[0], -n[1]];
    var d = (abst || 11) / F.s;
    return F.text([m[0] + n[0] * d, m[1] + n[1] * d], text, cls || 'mass', 0, 4);
  }
  function eckenText(F, pts, namen, cls, abst){   // Eckennamen vom Schwerpunkt weg
    var sx = 0, sy = 0; pts.forEach(function(p){ sx += p[0]; sy += p[1]; }); sx /= pts.length; sy /= pts.length;
    pts.forEach(function(p, j){ var d = [p[0] - sx, p[1] - sy], l = Math.hypot(d[0], d[1]) || 1, r = (abst || 11) / F.s;
      F.text([p[0] + d[0] / l * r, p[1] + d[1] / l * r], namen[j], cls || 'ecke', 0, 4); });
  }
  function schwer(pts){ var sx = 0, sy = 0; pts.forEach(function(p){ sx += p[0]; sy += p[1]; }); return [sx / pts.length, sy / pts.length]; }
  function zk(v){ return z(v, 2); }

  /* ---------- Kapitel 1: Zentrische Streckung ----------
     Unterschied zur Animation 1 der Themenseite: Dort zieht man Z, A, B, C frei und liest k, |k| und k² ab. Hier
     stehen Figur und Zentrum fest im Koordinatennetz — Z(1 | 1), A(2 | 3), B(3 | 1), C(5 | 4) —, der Regler k springt
     über 0 hinweg, und die Leiste lässt Geraden und Seiten antippen und Bildpunkte berechnen. Startwert k = 1.5 wie
     im Einführungsclip und in Animation 1. Farben wie dort: Original blau, Bild orange. */
  var Z1 = [1, 1], E1 = [[2, 3], [3, 1], [5, 4]];
  function bild1(p, k){ return [Z1[0] + k * (p[0] - Z1[0]), Z1[1] + k * (p[1] - Z1[1])]; }
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 258, x0: -7.5, x1: 10.5, y0: -5.5, achsen: { teil: 2 } },
    ohneNull: ['k'],
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, kk = w.k, A = E1[0], B = E1[1], C = E1[2];
      var Bi = E1.map(function(p){ return bild1(p, kk); }), ohne = Au.ohneBild && !w.richtig;
      if (!Au.ohneStrahlen && kk !== 1) E1.forEach(function(p){ F.gerade(Z1, p, 'strahl'); });
      F.vieleck(E1, 'figur');
      if (!ohne && kk !== 1) F.vieleck(Bi, 'bild');
      if (k.wahl && Au.wahl.art === 'gerade'){
        F.kandidat('zc', Z1, C, k.wahl, true); F.kandidat('za', Z1, A, k.wahl, true); F.kandidat('zb', Z1, B, k.wahl, true);
        F.kandidat('par', C, [C[0] + (B[0] - A[0]), C[1] + (B[1] - A[1])], k.wahl, true);
      }
      if (k.wahl && Au.wahl.art === 'seite'){
        F.kandidat('ab', Bi[0], Bi[1], k.wahl); F.kandidat('bc', Bi[1], Bi[2], k.wahl); F.kandidat('ca', Bi[2], Bi[0], k.wahl);
      }
      if (Au.wahl && w.richtig){
        if (Au.wahl.art === 'gerade') F.gerade(Z1, C, 'hilfe');
        if (Au.wahl.art === 'seite'){ F.strecke(Bi[0], Bi[1], 'hilfe'); F.strecke(A, B, 'hilfe'); }
      }
      eckenText(F, E1, ['A', 'B', 'C'], 'ecke klein');
      if (!ohne && kk !== 1) eckenText(F, Bi, ['A′', 'B′', 'C′'], 'ecke klein bild');
      if (Au.zeigeA && w.richtig){ F.punkt(Bi[0], 'g-pkt hilfe'); }
      F.punkt(Z1); F.text(Z1, 'Z', 'ecke', -8, 13);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      if (Au.wahl) return '\\(k = ' + z(kk) + '\\)';
      if (kk === 1) return '\\(k = 1\\): Jeder Punkt bleibt, wo er ist — Bild und Original fallen zusammen.';
      return '\\(k = ' + z(kk) + '\\): Bild auf ' + (kk > 0 ? 'derselben Seite' : 'der anderen Seite') + ' von \\(Z\\); Abstände zu \\(Z\\) und Seiten mal \\(|k| = ' + z(Math.abs(kk)) + '\\)'
        + (kk < 0 ? '; um \\(Z\\) um \\(180°\\) gedreht' : '');
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(k\\), auch unter null. Wo liegt das Bild, und was bleibt gleich?', probe: { k: 2 }, ziel: function(w){ return w.bewegt.k; } },
      { text: 'Stell \\(k\\) so ein, dass alle Seiten des Bildes doppelt so lang sind und das Bild auf derselben Seite von \\(Z\\) liegt.', probe: { k: 2 }, ziel: function(w){ return w.k === 2; } },
      { text: 'Das Bild soll gleich lange Seiten haben wie das Original, aber auf der anderen Seite von \\(Z\\) liegen.', probe: { k: -1 }, ziel: function(w){ return w.k === -1; } },
      { text: 'Bei \\(k = 2\\): Auf welcher Geraden liegt der Bildpunkt \\(C\'\\)? Tipp sie an.', ohneBild: true, ohneStrahlen: true,
        setup: function(s){ s.setze({ k: 2 }); s.sperre('k'); },
        wahl: { art: 'gerade', richtig: 'zc', gut: 'Jeder Bildpunkt liegt auf der Geraden durch \\(Z\\) und seinen Originalpunkt.', rueck: {
          za: 'Auf dieser Geraden liegt \\(A\'\\): Sie geht durch \\(Z\\) und \\(A\\).',
          zb: 'Auf dieser Geraden liegt \\(B\'\\): Sie geht durch \\(Z\\) und \\(B\\).',
          par: 'Diese Gerade geht durch \\(C\\), aber nicht durch \\(Z\\). Gestreckt wird vom Zentrum aus.' } } },
      { text: 'Bei \\(k = -1\\): Tipp die Seite des Bildes an, die parallel zu \\(AB\\) ist.', ohneStrahlen: true,
        setup: function(s){ s.setze({ k: -1 }); s.sperre('k'); },
        wahl: { art: 'seite', richtig: 'ab', gut: '\\(A\'B\'\\) ist das Bild von \\(AB\\) — Bildseite und Originalseite sind parallel, auch bei negativem \\(k\\).', rueck: {
          bc: 'Das ist \\(B\'C\'\\), das Bild von \\(BC\\). Sie ist parallel zu \\(BC\\).',
          ca: 'Das ist \\(C\'A\'\\), das Bild von \\(CA\\). Sie ist parallel zu \\(CA\\).' } } },
      { text: 'Mit \\(k = -2\\): Berechne die Koordinaten von \\(A\'\\).', ohneBild: true, zeigeA: true, fest: { k: -2 },
        setup: function(s){ s.sperre('k'); },
        gegeben: '\\(Z(1 \\mid 1)\\), \\(A(2 \\mid 3)\\), \\(k = -2\\)', gesucht: '\\(A\'\\)',
        loesung: 'Von \\(Z\\) nach \\(A\\): \\(1\\) nach rechts, \\(2\\) nach oben; mal \\(-2\\): \\(2\\) nach links, \\(4\\) nach unten. \\(A\'(-1 \\mid -3)\\).',
        frage: [{ name: 'x', label: '\\(A\'(\\)', einheit: '', soll: -1, fehler: [
                    [-4, 'Du hast die Koordinaten von \\(A\\) mit \\(k\\) multipliziert. Gestreckt wird vom Zentrum aus: Weg von \\(Z\\) nach \\(A\\), mal \\(k\\), von \\(Z\\) aus abtragen.'],
                    [-2, 'Das ist der Weg von \\(Z\\) aus mal \\(k\\). Die Koordinaten von \\(Z\\) kommen noch dazu.'],
                    [0, 'Du bist von \\(A\\) aus weitergegangen. Der Weg beginnt bei \\(Z\\).'],
                    [3, 'Das Vorzeichen von \\(k\\) fehlt: Bei \\(k \\lt 0\\) liegt \\(A\'\\) auf der anderen Seite von \\(Z\\).']],
                  tipp: 'Weg von \\(Z\\) nach \\(A\\) in \\(x\\)-Richtung, mal \\(k\\), dazu die \\(x\\)-Koordinate von \\(Z\\).' },
                { name: 'y', label: '\\(\\mid\\)', einheit: '\\()\\)', soll: -3, fehler: [
                    [-6, 'Du hast die Koordinaten von \\(A\\) mit \\(k\\) multipliziert. Gestreckt wird vom Zentrum aus: Weg von \\(Z\\) nach \\(A\\), mal \\(k\\), von \\(Z\\) aus abtragen.'],
                    [-4, 'Das ist der Weg von \\(Z\\) aus mal \\(k\\). Die Koordinaten von \\(Z\\) kommen noch dazu.'],
                    [-1, 'Du bist von \\(A\\) aus weitergegangen. Der Weg beginnt bei \\(Z\\).'],
                    [5, 'Das Vorzeichen von \\(k\\) fehlt: Bei \\(k \\lt 0\\) liegt \\(A\'\\) auf der anderen Seite von \\(Z\\).']],
                  tipp: 'Weg von \\(Z\\) nach \\(A\\) in \\(y\\)-Richtung, mal \\(k\\), dazu die \\(y\\)-Koordinate von \\(Z\\).' }] },
      { text: 'Mit \\(k = -1.5\\): Die Seite \\(CA\\) ist \\(\\sqrt{10} \\approx 3.16\\,\\text{cm}\\) lang. Wie lang ist \\(C\'A\'\\)?', ohneBild: true,
        setup: function(s){ s.setze({ k: -1.5 }); s.sperre('k'); },
        gegeben: '\\(k = -1.5\\), \\(\\overline{CA} \\approx 3.16\\,\\text{cm}\\)', gesucht: '\\(\\overline{C\'A\'}\\)',
        frage: [{ name: 'L', label: '\\(\\overline{C\'A\'} \\approx\\)', einheit: 'cm', soll: 4.74, tol: 0.011, fehler: [
                    [-4.74, 'Eine Länge ist nie negativ: Multipliziere mit dem Betrag \\(|k| = 1.5\\).'],
                    [7.11, 'Das ist \\(k^2\\) mal die Länge. Längen wachsen mit \\(|k|\\).'],
                    [2.11, 'Geteilt statt multipliziert: Das Bild ist grösser als das Original.']],
                  tipp: '\\(\\overline{C\'A\'} = |k| \\cdot \\overline{CA}\\).' }] },
      { text: 'Stell \\(k\\) so ein, dass die Seiten des Bildes halb so lang sind wie die des Originals und das Bild auf der anderen Seite von \\(Z\\) liegt.', probe: { k: -0.5 }, ziel: function(w){ return w.k === -0.5; } }
    ]
  });

  /* ---------- Kapitel 2: Strahlensätze ----------
     Unterschied zu den Animationen 2 und 3 der Themenseite: Dort wird die Gleichung schrittweise aufgebaut bzw. werden
     S, A, B gezogen. Hier stehen S, A und B fest (SA = 4, SB = 3, AB = 2.5), k schiebt die zweite Parallele, und ein
     zweiter Regler δ kippt sie: Dann stimmen die Verhältnisse nicht mehr (Voraussetzung und Umkehrung). Startwert
     k = 2.5 wie im Einführungsclip (Themenseite, Aufgabe A2: SA = 4, SA′ = 10, SB = 3). Aufgaben mit festen Werten
     (fest: sa, sb, ab, k) zeichnen ihre eigene, massstäbliche Figur. */
  var COS2 = 0.78125;                                  // SA = 4, SB = 3, AB = 2.5: cos θ = (16 + 9 − 6.25) / 24
  function strahlenFigur(sa, sb, ab, k, dl){
    var c = ab == null ? COS2 : (sa * sa + sb * sb - ab * ab) / (2 * sa * sb), th = Math.acos(c);
    var v = [Math.cos(th), Math.sin(th)], A = [sa, 0], B = [sb * v[0], sb * v[1]], A2 = [k * sa, 0];
    var u = [B[0] - A[0], B[1] - A[1]], r = grad(dl || 0);
    u = [u[0] * Math.cos(r) - u[1] * Math.sin(r), u[0] * Math.sin(r) + u[1] * Math.cos(r)];
    var det = -u[0] * v[1] + u[1] * v[0], s = (A2[0] * v[1] - A2[1] * v[0]) / det;   // A2 + s·u liegt auf der Geraden durch S mit Richtung v
    var B2 = [A2[0] + s * u[0], A2[1] + s * u[1]];
    return { S: [0, 0], A: A, B: B, A2: A2, B2: B2, v: v, th: th };
  }
  function vz(p, v){ return p[0] * v[0] + p[1] * v[1]; }    // Lage auf der Geraden (Vorzeichen: Seite von S)
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 187, x0: -7, x1: 11, y0: -4.3, karo: false },
    ohneNull: ['k'],            // k = 0 hiesse: A′ = S, die Verhältnisse wären unendlich (Prüfung 08.10.2026)
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, sa = w.sa || 4, sb = w.sb || 3, ab = w.ab, kk = w.k, dl = Au.frage ? 0 : w.d;
      var G = strahlenFigur(sa, sb, ab, kk, dl), S = G.S, A = G.A, B = G.B, A2 = G.A2, B2 = G.B2;
      F.gerade(S, [1, 0], 'strahl-voll'); F.gerade(S, G.v, 'strahl-voll');
      F.strecke(A, B, 'figur-linie');
      if (!(Au.wahl && !w.richtig)) F.strecke(A2, B2, dl ? 'fehl-linie' : 'bild-linie');   // gekippt: rot wie im Clip (Gegenbeispiel)
      if (k.wahl){
        [['par', 0], ['p1', 20], ['p2', -20]].forEach(function(c){ var H = strahlenFigur(sa, sb, ab, kk, c[1]); F.kandidat(c[0], A2, H.B2, k.wahl); });
      }
      [[S, 'S', -2, 15], [A, 'A', 0, 14], [A2, 'A′', 0, 14]].forEach(function(q){ F.punkt(q[0]); F.text(q[0], q[1], 'ecke klein', q[2], q[3]); });
      F.punkt(B); F.text(B, 'B', 'ecke klein', -8, -4);
      if (!(Au.wahl && !w.richtig)){ F.punkt(B2); F.text(B2, 'B′', 'ecke klein bild', vz(B2, G.v) < 0 ? 9 : -9, vz(B2, G.v) < 0 ? 8 : -4); }
      var lab = Au.lab || {};
      if (lab.sa) F.text(mitte(S, A), lab.sa, 'mass', 0, -5);
      if (lab.sa2) { F.strecke([0, -1.15], [A2[0], -1.15], 'massl'); F.strecke([0, -1.35], [0, -0.95], 'massl'); F.strecke([A2[0], -1.35], [A2[0], -0.95], 'massl'); F.text([A2[0] / 2, -1.15], lab.sa2, 'mass', 0, 11); }
      if (lab.aa) F.text(mitte(A, A2), lab.aa, 'mass', 0, -5);
      if (lab.sb) seitenText(F, S, B, lab.sb, 'mass', A, 9);
      if (lab.bb) seitenText(F, B, B2, lab.bb, 'mass', A2, 9);
      if (lab.ab) seitenText(F, A, B, lab.ab, 'mass', S, 9);
      if (lab.ab2) seitenText(F, A2, B2, lab.ab2, 'mass', S, 9);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      var SA2 = Math.abs(kk) * sa, SB2 = dist(S, B2), AB = dist(A, B), AB2 = dist(A2, B2);
      if (Au.wahl) return '\\(\\overline{SA} : \\overline{SA\'} = ' + z(sa) + ' : ' + z(SA2) + '\\); \\(\\overline{SB} = ' + z(sb) + '\\)';
      return '\\(\\overline{SA} : \\overline{SA\'} = ' + z(sa) + ' : ' + z(SA2) + ' ' + zz(sa / SA2, 3) + '\\)<br>'
        + '\\(\\overline{SB} : \\overline{SB\'} ' + (gl(SB2, Math.round(SB2 * 100) / 100) ? '= ' : '\\approx ') + z(sb) + ' : ' + z(SB2) + ' ' + zz(sb / SB2, 3) + '\\)<br>'
        + '\\(\\overline{AB} : \\overline{A\'B\'} ' + (gl(AB2, Math.round(AB2 * 100) / 100) ? '= ' : '\\approx ') + z(AB) + ' : ' + z(AB2) + ' ' + zz(AB / AB2, 3) + '\\)'
        + (dl ? '<br>\\(A\'B\'\\) ist nicht parallel zu \\(AB\\).' : '');
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(k\\). Die Zeile zeigt drei Verhältnisse — was gilt für sie bei jedem \\(k\\)?', probe: { k: 1.5 }, ziel: function(w){ return w.bewegt.k; } },
      { text: 'Zieh \\(k\\) unter null, bis \\(S\\) zwischen den Parallelen liegt. Gelten die Gleichungen in dieser X-Figur auch?', probe: { k: -1 }, ziel: function(w){ return w.k < 0; } },
      { text: 'Stell \\(k\\) so ein, dass \\(A\'B\'\\) halb so lang ist wie \\(AB\\) und auf derselben Seite von \\(S\\) liegt.', probe: { k: 0.5 }, ziel: function(w){ return w.k === 0.5; } },
      { text: 'Kipp die Gerade durch \\(A\'\\) mit \\(\\delta\\). Welche Verhältnisse stimmen jetzt nicht mehr?', probe: { d: 10 }, ziel: function(w){ return w.bewegt.d && w.d !== 0; } },
      { text: 'Bei \\(k = 2\\): Für welche Gerade durch \\(A\'\\) gilt \\(\\overline{SA} : \\overline{SA\'} = \\overline{SB} : \\overline{SB\'}\\)? Tipp sie an.',
        setup: function(s){ s.setze({ k: 2, d: 0 }); s.sperre('k', 'd'); },
        wahl: { richtig: 'par', gut: 'Die Parallele zu \\(AB\\): Sie trifft den zweiten Strahl in \\(\\overline{SB\'} = 6\\), und \\(4 : 8 = 3 : 6\\). Umgekehrt: Liegen \\(A\'\\) und \\(B\'\\) auf den Strahlen \\(SA\\) und \\(SB\\) und stimmen die Verhältnisse, sind die Geraden parallel.', rueck: {
          p1: 'Diese Gerade ist nicht parallel zu \\(AB\\). Sie trifft den zweiten Strahl zu nahe bei \\(S\\) — dann ist \\(\\overline{SB} : \\overline{SB\'}\\) nicht \\(1 : 2\\).',
          p2: 'Diese Gerade ist nicht parallel zu \\(AB\\). Sie trifft den zweiten Strahl zu weit weg von \\(S\\) — dann ist \\(\\overline{SB} : \\overline{SB\'}\\) nicht \\(1 : 2\\).' } } },
      { text: '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = 3\\,\\text{cm}\\), \\(\\overline{AA\'} = 4.5\\,\\text{cm}\\), \\(\\overline{AB} = 2\\,\\text{cm}\\). Wie lang ist \\(\\overline{A\'B\'}\\)?',
        fest: { sa: 3, sb: 2.5, ab: 2, k: 2.5 }, verdeckt: ['k'], setup: function(s){ s.sperre('k', 'd'); },
        lab: { sa: '3', aa: '4.5', ab: '2', ab2: '?' }, gegeben: '\\(\\overline{SA} = 3\\), \\(\\overline{AA\'} = 4.5\\), \\(\\overline{AB} = 2\\)', gesucht: '\\(\\overline{A\'B\'}\\)',
        loesung: '\\(\\overline{SA\'} = 7.5\\); \\(\\overline{A\'B\'} = 2 \\cdot \\tfrac{7.5}{3} = 5\\,\\text{cm}\\).',
        frage: [{ name: 'L', label: '\\(\\overline{A\'B\'} =\\)', einheit: 'cm', soll: 5, fehler: [
                    [3, 'Das ist \\(\\overline{AB} \\cdot \\overline{AA\'} : \\overline{SA}\\). Zu den Parallelen gehören die ganzen Strecken ab \\(S\\): \\(\\overline{SA\'} = 3 + 4.5\\).'],
                    [0.8, 'Das Verhältnis steht verkehrt: \\(A\'\\) liegt weiter von \\(S\\) weg als \\(A\\), also ist \\(A\'B\'\\) länger als \\(AB\\).'],
                    [6.5, 'Nicht addieren: Die Strecken stehen im gleichen Verhältnis, nicht im gleichen Abstand.']],
                  tipp: '\\(\\overline{AB} : \\overline{A\'B\'} = \\overline{SA} : \\overline{SA\'}\\) mit \\(\\overline{SA\'} = \\overline{SA} + \\overline{AA\'}\\).' }] },
      { text: '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = 5\\,\\text{cm}\\), \\(\\overline{SA\'} = 8\\,\\text{cm}\\), \\(\\overline{SB} = 4\\,\\text{cm}\\). Wie lang ist \\(\\overline{BB\'}\\)?',
        fest: { sa: 5, sb: 4, k: 1.6 }, verdeckt: ['k'], setup: function(s){ s.sperre('k', 'd'); },
        lab: { sa: '5', sa2: '8', sb: '4', bb: '?' }, gegeben: '\\(\\overline{SA} = 5\\), \\(\\overline{SA\'} = 8\\), \\(\\overline{SB} = 4\\)', gesucht: '\\(\\overline{BB\'}\\)',
        loesung: '\\(\\overline{SB\'} = 4 \\cdot \\tfrac{8}{5} = 6.4\\); \\(\\overline{BB\'} = 6.4 - 4 = 2.4\\,\\text{cm}\\).',
        frage: [{ name: 'L', label: '\\(\\overline{BB\'} =\\)', einheit: 'cm', soll: 2.4, fehler: [
                    [6.4, 'Das ist \\(\\overline{SB\'}\\). Gesucht ist das Stück \\(\\overline{BB\'} = \\overline{SB\'} - \\overline{SB}\\).'],
                    [3, 'Nicht den Unterschied \\(8 - 5\\) übertragen: Die Strecken stehen im gleichen Verhältnis, nicht im gleichen Abstand.'],
                    [2.5, 'Das Verhältnis steht verkehrt: \\(B\'\\) liegt weiter von \\(S\\) weg als \\(B\\).']],
                  tipp: '1. Strahlensatz: \\(\\overline{SA} : \\overline{SA\'} = \\overline{SB} : \\overline{SB\'}\\), dann \\(\\overline{BB\'} = \\overline{SB\'} - \\overline{SB}\\).' }] },
      { text: 'X-Figur: \\(S\\) liegt zwischen den Parallelen. \\(\\overline{SA} = 4\\,\\text{cm}\\), \\(\\overline{SA\'} = 6\\,\\text{cm}\\), \\(\\overline{A\'B\'} = 4.5\\,\\text{cm}\\). Wie lang ist \\(\\overline{AB}\\)?',
        fest: { sa: 4, sb: 3.5, ab: 3, k: -1.5 }, verdeckt: ['k'], setup: function(s){ s.sperre('k', 'd'); },
        lab: { sa: '4', sa2: '6', ab2: '4.5', ab: '?' }, gegeben: '\\(\\overline{SA} = 4\\), \\(\\overline{SA\'} = 6\\), \\(\\overline{A\'B\'} = 4.5\\)', gesucht: '\\(\\overline{AB}\\)',
        loesung: '\\(\\overline{AB} = 4.5 \\cdot \\tfrac{4}{6} = 3\\,\\text{cm}\\) — dieselbe Gleichung wie ohne Kreuzung.',
        frage: [{ name: 'L', label: '\\(\\overline{AB} =\\)', einheit: 'cm', soll: 3, fehler: [
                    [6.75, 'Das Verhältnis steht verkehrt: \\(A\\) liegt näher bei \\(S\\) als \\(A\'\\), also ist \\(AB\\) kürzer als \\(A\'B\'\\).'],
                    [2.5, 'Nicht den Unterschied abziehen: Die Strecken stehen im gleichen Verhältnis.'],
                    [-3, 'Längen sind positiv, auch in der X-Figur.']],
                  tipp: '\\(\\overline{AB} : \\overline{A\'B\'} = \\overline{SA} : \\overline{SA\'}\\).' }] }
    ]
  });

  /* ---------- Kapitel 3: Ähnliche Figuren — Längen, Umfang, Fläche ----------
     Unterschied zur Animation 4 der Themenseite: Dort streckt ein einziger Regler k die Figur (immer ähnlich). Hier
     haben Breite b′ und Höhe h′ des Bildes je einen eigenen Regler: Ähnlich ist es nur, wenn beide Verhältnisse
     gleich sind — dann liegt seine Ecke auf der verlängerten Diagonale des Originals. Original 3 cm × 2 cm, Startwert
     4.5 cm × 3 cm (k = 1.5) wie im Einführungsclip. Die Zeile nennt keine Flächen (sie würden Aufgaben verraten). */
  arbeitsbereich('sim3', {
    fenster: { w: 320, h: 226, x0: -0.8, x1: 9.8, y0: -0.9 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, b = w.b, h = w.h, ohne = Au.ohneBild && !w.richtig, bb = Au.zeigeB || b, hh = Au.zeigeH || h;
      var O = [0, 0], fb = 3, fh = 2, kb = b / fb, kh = h / fh, ahnl = gl(kb, kh);
      F.strecke(O, [9.8, 9.8 * fh / fb], 'diagonale');
      if (!ohne) F.vieleck([O, [bb, 0], [bb, hh], [0, hh]], 'bild' + (ahnl || Au.frage ? '' : ' nicht'));
      F.vieleck([O, [fb, 0], [fb, fh], [0, fh]], 'figur');
      F.text([fb / 2, 0], '3', 'mass', 0, 11); F.text([fb, fh / 2], '2', 'mass', 5, 4, 'start');
      if (!ohne){ F.punkt([bb, hh], ahnl || Au.frage ? 'g-pkt hilfe' : 'g-pkt'); F.text([bb / 2, 0], Au.frage ? 'b′' : 'b′ = ' + z(bb), 'mass bild', 0, 22); F.text([bb, hh / 2], Au.frage ? 'h′' : 'h′ = ' + z(hh), 'mass bild', 5, 4, 'start'); }
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      return '\\(\\tfrac{b\'}{b} = \\tfrac{' + z(b) + '}{3} ' + zz(kb) + '\\); \\(\\tfrac{h\'}{h} = \\tfrac{' + z(h) + '}{2} ' + zz(kh) + '\\) — '
        + (ahnl ? (gl(kb, 1) ? 'deckungsgleich (\\(k = 1\\))' : 'ähnlich, \\(k ' + zz(kb) + '\\)') : 'nicht ähnlich');
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(b\'\\) und \\(h\'\\). Wann liegt die Ecke des Bildes auf der gestrichelten Diagonalen?', probe: { b: 6 }, ziel: function(w){ return w.bewegt.b || w.bewegt.h; } },
      { text: 'Mach das Bild ähnlich zum Original, mit \\(k = 2\\).', probe: { b: 6, h: 4 }, ziel: function(w){ return w.b === 6 && w.h === 4; } },
      { text: 'Stell ein zum Original ähnliches Rechteck ein, das \\(7.5\\,\\text{cm}\\) breit ist.', probe: { b: 7.5, h: 5 }, ziel: function(w){ return w.b === 7.5 && w.h === 5; } },
      { text: 'Stell ein Rechteck mit der doppelten Fläche des Originals ein, das <b>nicht</b> ähnlich ist.', probe: { b: 6, h: 2 }, ziel: function(w){ return gl(w.b * w.h, 12) && !gl(w.b / 3, w.h / 2); } },
      { text: 'Stell ein ähnliches Rechteck mit der neunfachen Fläche des Originals ein.', probe: { b: 9, h: 6 }, ziel: function(w){ return w.b === 9 && w.h === 6; } },
      { text: 'Ein zum Original ähnliches Rechteck hat die Fläche \\(8.64\\,\\text{cm}^2\\). Wie breit ist es?', ohneBild: true, zeigeB: 3.6, zeigeH: 2.4,
        setup: function(s){ s.sperre('b', 'h'); },
        gegeben: 'Original \\(3\\,\\text{cm} \\times 2\\,\\text{cm}\\); Bild ähnlich, \\(A\' = 8.64\\,\\text{cm}^2\\)', gesucht: '\\(b\'\\)',
        loesung: '\\(k^2 = \\tfrac{8.64}{6} = 1.44\\), also \\(k = 1.2\\) und \\(b\' = 1.2 \\cdot 3 = 3.6\\,\\text{cm}\\).',
        frage: [{ name: 'b', label: '\\(b\' =\\)', einheit: 'cm', soll: 3.6, fehler: [
                    [4.32, 'Eine Länge wächst mit \\(k\\), nicht mit \\(k^2\\): Aus \\(\\tfrac{A\'}{A} = k^2 = 1.44\\) zuerst \\(k\\) ziehen. (Teilst du \\(A\'\\) durch die alte Höhe \\(2\\), kommt dasselbe heraus — aber auch die Höhe ist gestreckt.)'],
                    [2.94, 'Das ist \\(\\sqrt{8.64}\\) — die Seite eines Quadrats. Das Rechteck hat das Seitenverhältnis \\(3 : 2\\).'],
                    [1.44, 'Das ist \\(k^2 = \\tfrac{A\'}{A}\\). Daraus folgt \\(k\\), dann die Breite.']],
                  tipp: '\\(k^2 = \\tfrac{A\'}{A}\\), dann \\(b\' = k \\cdot 3\\).' }] },
      { text: 'Das Original wird mit \\(k = 0.5\\) verkleinert. Wie gross sind Umfang und Fläche des Bildes?', ohneBild: true, zeigeB: 1.5, zeigeH: 1,
        setup: function(s){ s.sperre('b', 'h'); },
        gegeben: 'Original \\(3\\,\\text{cm} \\times 2\\,\\text{cm}\\): \\(u = 10\\,\\text{cm}\\), \\(A = 6\\,\\text{cm}^2\\); \\(k = 0.5\\)', gesucht: '\\(u\'\\), \\(A\'\\)',
        loesung: '\\(u\' = 0.5 \\cdot 10 = 5\\,\\text{cm}\\); \\(A\' = 0.5^2 \\cdot 6 = 1.5\\,\\text{cm}^2\\) — ein Viertel.',
        frage: [{ name: 'u', label: '\\(u\' =\\)', einheit: 'cm', soll: 5, fehler: [[2.5, 'Der Umfang ist eine Länge: Er wächst mit \\(k\\), nicht mit \\(k^2\\).'], [20, 'Bei \\(k = 0.5\\) wird verkleinert: mal \\(0.5\\), nicht geteilt.']], tipp: '\\(u\' = k \\cdot u\\).' },
                { name: 'A', label: '\\(A\' =\\)', einheit: 'cm²', soll: 1.5, fehler: [[3, 'Eine Fläche wächst mit \\(k^2 = 0.25\\), nicht mit \\(k\\).'], [24, 'Bei \\(k = 0.5\\) wird verkleinert: mal \\(k^2 = 0.25\\).']], tipp: '\\(A\' = k^2 \\cdot A\\).' }] }
    ]
  });

  /* ---------- Kapitel 4: Ähnliche Dreiecke ----------
     Unterschied zur Animation 5 der Themenseite: Dort ist das zweite Dreieck eine Kopie mit Streckfaktor und
     «Störung». Hier baut man das zweite Dreieck A′B′C′ selbst aus α′, β′ und c′ (WW-Satz) — auch mit vertauschten
     Ecken —, tippt entsprechende Seiten an und rechnet mit dem Streckfaktor. Original ABC wie in Animation 5 und im
     Einführungsclip: α = 50°, β = 70°, γ = 60°, c = 4 cm. Startwert des zweiten Dreiecks: α′ = 70°, β′ = 60°
     (γ′ = 50°), c′ = 5.5 cm — dieselbe Form, aber mit anderer Zuordnung der Ecken (wie das Dreieck PQR im Clip). */
  var AL4 = 50, BE4 = 70, C4 = 4;
  function dreieck(al, be, c, x0){   // A(x0 | 0), B(x0 + c | 0), C über AB; null, wenn es kein Dreieck gibt
    if (al + be >= 179.9) return null;
    var b = c * sinG(be) / sinG(180 - al - be), a = c * sinG(al) / sinG(180 - al - be);
    return { A: [x0, 0], B: [x0 + c, 0], C: [x0 + b * cosG(al), b * sinG(al)], a: a, b: b, c: c, w: [al, be, 180 - al - be] };
  }
  var D4 = dreieck(AL4, BE4, C4, 0);
  function aehnlich4(T){                 // gleiche Winkel (in beliebiger Zuordnung)?
    if (!T) return false;
    var u = T.w.slice().sort(function(p, q){ return p - q; }), v = D4.w.slice().sort(function(p, q){ return p - q; });
    return u.every(function(x, j){ return Math.abs(x - v[j]) < 1e-6; });
  }
  function faktor4(T){                   // Streckfaktor: Seite gegenüber 60° (γ im Original) durch c = 4
    var j = T.w.findIndex(function(x){ return Math.abs(x - 60) < 1e-6; }), s = [T.a, T.b, T.c][j];
    return s / C4;
  }
  arbeitsbereich('sim4', {
    fenster: { w: 320, h: 211, x0: -0.7, x1: 12.2, y0: -1.0, karo: false },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, T = dreieck(w.al, w.be, w.c, 5.5), O = D4;
      F.vieleck([O.A, O.B, O.C], 'figur');
      winkelMarke(F, O.A, O.B, O.C, 16, 'winkelbogen', '50°', 'winkel klein');
      winkelMarke(F, O.B, O.C, O.A, 16, 'winkelbogen', '70°', 'winkel klein');
      winkelMarke(F, O.C, O.A, O.B, 14, 'winkelbogen', '60°', 'winkel klein');
      eckenText(F, [O.A, O.B, O.C], ['A', 'B', 'C'], 'ecke klein', 12);
      var lab = Au.lab || {};
      if (lab.c) F.text(mitte(O.A, O.B), lab.c, 'mass', 0, 11);
      if (lab.b) seitenText(F, O.A, O.C, lab.b, 'mass', O.B, 9);
      if (lab.a) seitenText(F, O.B, O.C, lab.a, 'mass', O.A, 9);
      if (!T){ F.text([8.5, 3], 'kein Dreieck: α′ + β′ ≥ 180°', 'mass', 0, 0); return '\\(\\alpha\' + \\beta\' \\geq 180°\\): Die Schenkel treffen sich nicht.'; }
      F.vieleck([T.A, T.B, T.C], 'bild');
      winkelMarke(F, T.A, T.B, T.C, 16, 'winkelbogen', z(T.w[0]) + '°', 'winkel klein');
      winkelMarke(F, T.B, T.C, T.A, 16, 'winkelbogen', z(T.w[1]) + '°', 'winkel klein');
      winkelMarke(F, T.C, T.A, T.B, 14, 'winkelbogen', z(T.w[2]) + '°', 'winkel klein');
      eckenText(F, [T.A, T.B, T.C], ['A′', 'B′', 'C′'], 'ecke klein bild', 12);
      if (T.C[1] > 7.2) F.text([T.C[0], 7.0], '↑ C′ liegt höher', 'mass', 0, 0);
      if (k.wahl){ F.kandidat('a2', T.B, T.C, k.wahl); F.kandidat('b2', T.A, T.C, k.wahl); F.kandidat('c2', T.A, T.B, k.wahl); }
      if (Au.wahl && w.richtig){ F.strecke(T.B, T.C, 'hilfe'); F.strecke(O.A, O.B, 'hilfe'); }
      if (lab.c2) F.text(mitte(T.A, T.B), lab.c2, 'mass', 0, 11);
      if (lab.a2) seitenText(F, T.B, T.C, lab.a2, 'mass', T.A, 9);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      if (Au.wahl) return 'Winkel: \\(A\'B\'C\'\\) hat \\(' + z(T.w[0]) + '°\\), \\(' + z(T.w[1]) + '°\\), \\(' + z(T.w[2]) + '°\\)';
      var ae = aehnlich4(T);
      return '\\(\\alpha\' = ' + z(T.w[0]) + '°\\), \\(\\beta\' = ' + z(T.w[1]) + '°\\), \\(\\gamma\' = 180° - \\alpha\' - \\beta\' = ' + z(T.w[2]) + '°\\)<br>'
        + (ae ? 'dieselben Winkel wie \\(ABC\\): ähnlich' : 'andere Winkel als \\(ABC\\) (\\(50°\\), \\(70°\\), \\(60°\\)): nicht ähnlich');   // ohne k: die Zeile soll Aufgabe 6 nicht vorrechnen
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(\\alpha\'\\), \\(\\beta\'\\) und \\(c\'\\). Wann haben beide Dreiecke dieselbe Form?', probe: { al: 50 }, ziel: function(w){ return w.bewegt.al || w.bewegt.be || w.bewegt.c; } },
      { text: 'Mach \\(A\'B\'C\'\\) ähnlich zu \\(ABC\\), mit \\(\\alpha\' = \\alpha\\), \\(\\beta\' = \\beta\\) und \\(k = 1.5\\).', probe: { al: 50, be: 70, c: 6 }, ziel: function(w){ return w.al === 50 && w.be === 70 && w.c === 6; } },
      { text: 'Mach \\(A\'B\'C\'\\) ähnlich zu \\(ABC\\), aber so, dass der Winkel \\(50°\\) bei \\(B\'\\) liegt.', probe: { al: 70, be: 50 }, ziel: function(w){ return w.be === 50 && aehnlich4(dreieck(w.al, w.be, w.c, 5.5)); } },
      { text: 'Stell ein Dreieck ein, das zu \\(ABC\\) ähnlich und gleich gross ist (kongruent, \\(k = 1\\)).', probe: { al: 50, be: 70, c: 4 },
        ziel: function(w){ var T = dreieck(w.al, w.be, w.c, 5.5); return aehnlich4(T) && gl(faktor4(T), 1); } },
      { text: 'Tipp die Seite von \\(A\'B\'C\'\\) an, die der Seite \\(AB\\) entspricht.',
        setup: function(s){ s.setze({ al: 60, be: 50, c: 6 }); s.sperre('al', 'be', 'c'); },
        wahl: { richtig: 'a2', gut: '\\(AB\\) liegt dem Winkel \\(60°\\) gegenüber, in \\(A\'B\'C\'\\) liegt \\(60°\\) bei \\(A\'\\): Die entsprechende Seite ist \\(B\'C\'\\).', rueck: {
          c2: '\\(A\'B\'\\) trägt dieselben Buchstaben, liegt aber dem Winkel \\(70°\\) gegenüber. \\(AB\\) liegt \\(60°\\) gegenüber.',
          b2: '\\(A\'C\'\\) liegt dem Winkel \\(50°\\) gegenüber — sie entspricht \\(BC\\). \\(AB\\) liegt \\(60°\\) gegenüber.' } } },
      { text: 'Die Dreiecke sind ähnlich. \\(\\overline{AB} = 4\\,\\text{cm}\\), \\(\\overline{AC} \\approx 4.34\\,\\text{cm}\\), \\(\\overline{BC} \\approx 3.54\\,\\text{cm}\\) und \\(\\overline{A\'B\'} = 6\\,\\text{cm}\\). Wie lang ist \\(\\overline{B\'C\'}\\)?',
        setup: function(s){ s.setze({ al: 60, be: 50, c: 6 }); s.sperre('al', 'be', 'c'); },
        lab: { c: '4', b: '4.34', a: '3.54', c2: '6', a2: '?' }, gegeben: 'Winkel im Bild; \\(\\overline{A\'B\'} = 6\\)', gesucht: '\\(\\overline{B\'C\'}\\)',
        loesung: '\\(A\'B\'\\) liegt \\(70°\\) gegenüber und entspricht \\(AC\\): \\(k = \\tfrac{6}{4.34} \\approx 1.38\\). \\(B\'C\'\\) entspricht \\(AB\\): \\(\\overline{B\'C\'} = 4 \\cdot \\tfrac{6}{4.34} \\approx 5.53\\,\\text{cm}\\).',
        frage: [{ name: 'L', label: '\\(\\overline{B\'C\'} \\approx\\)', einheit: 'cm', soll: 5.53, tol: 0.011, fehler: [
                    [5.31, 'Du hast \\(A\'B\'\\) zu \\(AB\\) zugeordnet (gleiche Buchstaben) und \\(B\'C\'\\) zu \\(BC\\). Entsprechende Seiten liegen gleichen Winkeln gegenüber.'],
                    [4.89, 'Der Faktor stimmt, aber \\(B\'C\'\\) entspricht nicht \\(BC\\): \\(B\'C\'\\) liegt \\(60°\\) gegenüber, wie \\(AB\\).'],
                    [2.89, 'Geteilt statt multipliziert: \\(A\'B\'C\'\\) ist das grössere Dreieck.'],
                    [6, 'Das ist \\(\\overline{A\'B\'}\\) selbst. Gesucht ist die Seite gegenüber \\(60°\\).']],
                  tipp: 'Zuerst ein Paar entsprechender Seiten (gegenüber gleichen Winkeln) für \\(k\\), dann \\(\\overline{B\'C\'} = k \\cdot\\) die entsprechende Seite von \\(ABC\\).' }] }
    ]
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function r2(v){ return Math.round(v * 100) / 100; }
    function tz(v){ return z(v); }                                   // echtes Minus, Dezimalpunkt
    function mischen(l){ l = l.slice(); for (var i = l.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = l[i]; l[i] = l[j]; l[j] = t; } return l; }
    function ganz2(v){ return Math.abs(v * 100 - Math.round(v * 100)) < 1e-6; }   // höchstens zwei Dezimalen
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche ·
       Kapitelaufgaben · Gesamttest · Themenseite (A1–A7). Je Typ ein eigener Schlüssel. */
    var SPERRE = [
      // bildpunkt: bp|Zx|Zy|Px|Py|k — Arbeitsbereich 1, Clip 1, Kontrollclip 1, Aufgaben 1a, 1b, 1d, Gesamttest G1, Themenseite A1
      'bp|1|1|2|3|-2', 'bp|1|1|5|4|1.5', 'bp|1|1|2|3|1.5', 'bp|1|1|3|1|1.5', 'bp|1|1|5|4|0.5', 'bp|1|1|2|3|0.5', 'bp|1|1|3|1|0.5',
      'bp|1|1|5|4|-1.5', 'bp|1|1|2|3|-1.5', 'bp|1|1|3|1|-1.5', 'bp|1|1|5|4|2', 'bp|1|1|2|3|2', 'bp|1|1|3|1|2', 'bp|1|1|5|4|-1', 'bp|1|1|2|3|-1', 'bp|1|1|3|1|-1',
      'bp|-1|0|1|1|-2', 'bp|0|1|2|0|2', 'bp|0|1|3|2|2', 'bp|0|1|1.5|2.5|2',
      'bp|4|2|0|0|-0.5', 'bp|4|2|4|0|-0.5', 'bp|4|2|-2|4|-0.5', 'bp|-2|1|0|2|2.5', 'bp|-2|1|3|0|2.5', 'bp|-2|1|1|4|2.5',
      'bp|4|3|0|1|-0.5', 'bp|4|3|2|0|-0.5', 'bp|4|3|1|4|-0.5', 'bp|2|-1|4|0|-1.5', 'bp|2|-1|6|3|-1.5', 'bp|2|-1|3|2|-1.5',
      'bp|1|1|0|0|2', 'bp|1|1|6|0|2', 'bp|1|1|2|4|2',
      // streckfaktor: sf|Art|Werte — Kontrollclip 1 F4, Arbeitsbereich 1 A7, Aufgabe 1e, Gesamttest G1, Mini-Check der Themenseite
      'sf|k|4|10|-1', 'sf|bild|3.16|-1.5', 'sf|bild|3|-2', 'sf|bild|3|2',
      // strahlen: st|SA|SA′|dritte Strecke|gesucht — Clip 2, Arbeitsbereich 2, Kontrollclip 2, Aufgaben 2a–2e, G2, G3, A2, A3
      'st|4|10|3|sb2', 'st|4|10|3|bb', 'st|4|10|2.5|ab2', 'st|4|6|3|sb2', 'st|4|6|2.5|ab2', 'st|3|7.5|2|ab2', 'st|5|8|4|bb', 'st|5|8|4|sb2',
      'st|4|6|4.5|ab', 'st|3|9|2|ab2', 'st|2|5|3|sb2', 'st|2|5|3|ab2', 'st|6|9|4|sb2', 'st|2.4|4|3|sb2', 'st|2.4|4|6|ab', 'st|2.5|6|3|bb',
      'st|2.5|6|2|ab2', 'st|4|10|3|sb2', 'st|5|12|4|ab2', 'st|4|8|3|sb2',
      'st|2|5|7.5|sb', 'st|2.5|6|2|ab2aa',          // Kontrollclip 2 F3 (umgekehrt: SB aus SB′), Gesamttest G2 (b) mit AA′
      // flaeche: fl|Art|Werte — Clip 3, Arbeitsbereich 3, Kontrollclip 3, Aufgaben 3a–3e, G5, Themenseite
      'fl|bild|6|1.5', 'fl|bild|6|2', 'fl|bild|6|0.5', 'fl|k|6|13.5', 'fl|k|6|8.64', 'fl|k|20|45', 'fl|k|12|75', 'fl|k|1|16', 'fl|k|1|6.25', 'fl|k|1|9',
      'fl|umfang|10|1.5', 'fl|umfang|10|0.5', 'fl|umfang|12|3', 'fl|umfang|14|2.5', 'fl|bild|6|3',
      // massstab: ms|n|Art|Wert — Clip 3, Kontrollclip 3, Aufgabe 3c, G4, Themenseite A7
      'ms|200|laenge|2.5', 'ms|200|flaeche|6.25', 'ms|1000|flaeche|5', 'ms|50|laenge|8', 'ms|50|laenge|6', 'ms|50|flaeche|48',
      'ms|25000|laenge|18.4', 'ms|25000|flaeche|3.2', 'ms|200|laenge|0.8',
      // aehnlich: ae|Art|Werte (sortiert) — Clip 4, Kontrollclip 4, Aufgaben 4a, 4b, G6, Themenseite A4
      'ae|ww|50|60|70|50|60|70', 'ae|ww|40|65|75|40|65|75', 'ae|sss|4|5|6|6|7.5|9', 'ae|sss|4|5|6|6|7.5|8', 'ae|sss|4|6|7|8|12|15',
      'ae|sss|5|7|8|7.5|10.5|12', 'ae|sss|5|7|8|7.5|10.5|13', 'ae|ww|35|65|80|35|65|80', 'ae|sss|3|4|5|6|8|10', 'ae|sss|3|4|5|6|8|9', 'ae|sss|6|8|9|9|12|13.5',
      'ae|ww|38|65|77|38|65|77', 'ae|ww|41|63|76|41|63|76',   // Kontrollclip 4 F1, Gesamttest G6
      // zuordnen: zu|Seiten|k — Aufgabe 4a, Arbeitsbereich 4
      'zu|4|5|6|1.5',
      // hoehensatz: hs|Art|Werte — Clip 4, Kontrollclip 4, Aufgabe 4d, G7, Themenseite A5
      'hs|h|1.8|3.2', 'hs|h|4|9', 'hs|h|5|7.2', 'hs|h|16|9', 'hs|abschnitt|7.5|12.5', 'hs|kathete|1.8|5', 'hs|kathete|3.2|5', 'hs|kathete|16|25', 'hs|kathete|9|25',
      'hs|kathete|5|12.2', 'hs|kathete|7.2|12.2'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function feld(A, f, e, soll, tipp, fehler, tol){
      if (stimmt(e[f], soll, tol)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (!stimmt(fehler[j][0], soll, tol) && stimmt(e[f], fehler[j][0], tol)) return fehler[j][1];
      return nah(e[f], soll, tol) ? RUNDEN : tipp;
    }
    /* Gezielte Fehler für das Prüfwerkzeug: nur Werte, die sich vom Sollwert unterscheiden. */
    /* Stichwort für das Prüfwerkzeug: das angegebene, wenn es im Text vorkommt, sonst das erste längere Wort ausserhalb
       der Formeln (pruef-uebungen erwartet es in der Rückmeldung). */
    function stichwort(x){
      if (x[2] && x[1].indexOf(x[2]) >= 0) return x[2];
      var w = x[1].replace(/\\\(.*?\\\)/g, ' ').replace(/<[^>]*>/g, ' ').match(/[A-Za-zÄÖÜäöü]{5,}/);
      return w ? w[0] : null;
    }
    function fehlerListe(A, f, liste, tol){
      var aus = [], gesehen = [];
      liste.forEach(function(x){ if (isFinite(x[0]) && !stimmt(r2(x[0]), A.soll, tol) && Math.abs(r2(x[0]) - A.soll) > 0.07
          && !gesehen.some(function(g){ return stimmt(r2(x[0]), g, tol); })) { gesehen.push(r2(x[0])); var o = {}; o[f] = String(r2(x[0])); aus.push([o, stichwort(x)]); } });
      return aus;
    }
    function einfach(A, e, tipp){   // ein Feld x, Fehlerliste A.falsch [[Wert, Text, Stichwort]]
      var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
      return feld(A, 'x', e, A.soll, tipp, f, A.tol);
    }
    function beschriften(box, A){   // Platzhalter im Eingabemuster: Beschriftung vor und Einheit nach dem Feld
      var l = box.querySelector('.ue-lab'), u = box.querySelector('.ue-einh');
      if (l){ l.innerHTML = A.lab || ''; setzen(l); } if (u){ u.innerHTML = A.einh || ''; setzen(u); }
    }
    /* Fenster, das alle Punkte zeigt, gleich geteilt. unten: zusätzliche Pixel unter der Figur für Beschriftungen
       unter der untersten Linie («SA′ = …», «c = …» — Prüfung 08.10.2026: in 35 % der Würfe abgeschnitten). */
    function fensterUm(pts, rand, b, h, unten){
      unten = unten || 0;
      var pad = 12;   // Pixel ringsum für Eckennamen (Messung 08.10.2026: B, B′, P, Q, R in 3–8 % der Würfe am Rand abgeschnitten)
      var xs = pts.map(function(p){ return p[0]; }), ys = pts.map(function(p){ return p[1]; });
      rand = Math.max(rand, 0.1 * Math.max(Math.max.apply(null, xs) - Math.min.apply(null, xs), Math.max.apply(null, ys) - Math.min.apply(null, ys)));   // Platz für Beschriftungen
      var x0 = Math.min.apply(null, xs) - rand, x1 = Math.max.apply(null, xs) + rand, y0 = Math.min.apply(null, ys) - rand, y1 = Math.max.apply(null, ys) + rand;
      var s = Math.min((b - 2 * pad) / (x1 - x0), (h - unten - 2 * pad) / (y1 - y0)), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      return { w: b, h: h, x0: cx - b / s / 2, x1: cx + b / s / 2, y0: cy - (h - unten) / s / 2 - unten / s, karo: false };
    }

    var TYPEN = {
      /* ── Kapitel 1 ── */
      /* Bildpunkt mit Koordinaten: P′ = Z + k · (P − Z). Z ≠ (0 | 0), sonst wäre der Fehler «k · P» unsichtbar. */
      'bildpunkt': { felder: ['x', 'y'], muster: 'P′( {x} | {y} )',
        schl: function(A){ return 'bp|' + A.Z[0] + '|' + A.Z[1] + '|' + A.P[0] + '|' + A.P[1] + '|' + A.k; },
        neu: function(){
          var Zp, v, k, P, B;
          do {
            Zp = [zufallG(-3, 3), zufallG(-3, 3)]; v = [zufallG(-4, 4), zufallG(-4, 4)];
            k = zufall([2, 3, 0.5, 1.5, -1, -2, -0.5, 2.5, -1.5, -3]);
            P = [Zp[0] + v[0], Zp[1] + v[1]]; B = [Zp[0] + k * v[0], Zp[1] + k * v[1]];
          } while ((Zp[0] === 0 && Zp[1] === 0) || v[0] === 0 || v[1] === 0 || Math.abs(B[0]) > 12 || Math.abs(B[1]) > 12);
          var f = [[[k * P[0], k * P[1]], 'Du hast die Koordinaten von \\(P\\) mit \\(k\\) multipliziert. Gestreckt wird vom Zentrum aus: Weg von \\(Z\\) nach \\(P\\), mal \\(k\\), von \\(Z\\) aus abtragen.', 'Zentrum'],
                   [[k * v[0], k * v[1]], 'Das ist nur der Weg von \\(Z\\) aus, mal \\(k\\). Die Koordinaten von \\(Z\\) kommen noch dazu.', 'Weg'],
                   [[P[0] + k * v[0], P[1] + k * v[1]], 'Du bist von \\(P\\) aus weitergegangen. Abgetragen wird von \\(Z\\) aus.', 'von'],
                   [[Zp[0] - k * v[0], Zp[1] - k * v[1]], k < 0 ? 'Das Vorzeichen von \\(k\\) fehlt: Bei \\(k \\lt 0\\) liegt \\(P\'\\) auf der anderen Seite von \\(Z\\).' : 'Bei \\(k \\gt 0\\) liegt \\(P\'\\) auf derselben Seite von \\(Z\\) wie \\(P\\).', 'Seite']];
          return { Z: Zp, P: P, v: v, k: k, soll: B, falsch: f,
            text: 'Zentrische Streckung mit dem Zentrum \\(Z(' + tz(Zp[0]) + ' \\mid ' + tz(Zp[1]) + ')\\) und \\(k = ' + tz(k) + '\\). Wo liegt der Bildpunkt \\(P\'\\) von \\(P(' + tz(P[0]) + ' \\mid ' + tz(P[1]) + ')\\)?' }; },
        eingabe: function(A){ return { x: String(A.soll[0]), y: String(A.soll[1]) }; },
        fehler: function(A){ var aus = [], ges = [String(A.soll)];
          A.falsch.forEach(function(f){ var s = String(f[0]); if (ges.indexOf(s) < 0){ ges.push(s); aus.push([{ x: String(f[0][0]), y: String(f[0][1]) }, stichwort(f)]); } });
          return aus; },
        zeichne: function(svg, A){
          var B = A.soll, pts = [A.Z, A.P, B, [0, 0]];
          var fe = fensterUm(pts, 1.4, 240, 200); fe.karo = 1; fe.achsen = { teil: 2 };
          var F = Flaeche(svg, fe);
          F.gerade(A.Z, A.P, 'strahl');
          F.punkt(A.Z); F.text(A.Z, 'Z', 'ecke', -8, 13); F.punkt(A.P, 'g-pkt blau'); F.text(A.P, 'P', 'ecke', 8, -5);
        },
        pruefen: function(A, e){
          if (gl(e.x, A.soll[0]) && gl(e.y, A.soll[1])) return null;
          for (var j = 0; j < A.falsch.length; j++){ var f = A.falsch[j][0]; if (gl(e.x, f[0]) && gl(e.y, f[1]) && !(gl(f[0], A.soll[0]) && gl(f[1], A.soll[1]))) return A.falsch[j][1]; }
          if (gl(e.x, A.soll[0])) return 'Die \\(x\\)-Koordinate stimmt. Prüf die \\(y\\)-Koordinate: \\(y\\) von \\(Z\\) plus \\(k\\) mal den Weg in \\(y\\)-Richtung.';
          if (gl(e.y, A.soll[1])) return 'Die \\(y\\)-Koordinate stimmt. Prüf die \\(x\\)-Koordinate: \\(x\\) von \\(Z\\) plus \\(k\\) mal den Weg in \\(x\\)-Richtung.';
          return 'Von \\(Z\\) nach \\(P\\): wie weit nach rechts, wie weit nach oben? Diesen Weg mal \\(k\\), dann von \\(Z\\) aus abtragen.'; },
        loesung: function(A){ return 'P\' = (' + tz(A.Z[0]) + ' + ' + tz(A.k) + ' \\cdot ' + (A.v[0] < 0 ? '(' + tz(A.v[0]) + ')' : tz(A.v[0])) + ' \\mid ' + tz(A.Z[1]) + ' + ' + tz(A.k) + ' \\cdot ' + (A.v[1] < 0 ? '(' + tz(A.v[1]) + ')' : tz(A.v[1])) + ') = (' + tz(A.soll[0]) + ' \\mid ' + tz(A.soll[1]) + ')'; } },

      /* Streckfaktor aus Abständen (mit Vorzeichen), Bildlänge und Originallänge aus k. */
      'streckfaktor': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} <span class="ue-einh"></span>',
        schl: function(A){ return 'sf|' + A.art + '|' + A.werte.join('|'); },
        vorbereiten: beschriften,
        neu: function(){
          var art = zufall(['k', 'k', 'bild', 'original']), betr = zufall([0.5, 1.5, 2, 2.5, 3, 0.25, 4]), neg = Math.random() < 0.5;
          if (art === 'k'){
            var d1 = zufall([2, 2.5, 3, 4, 5, 6, 8]), d2 = r2(betr * d1), k = neg ? -betr : betr;
            return { art: art, werte: [d1, d2, neg ? -1 : 1], soll: k, lab: '\\(k =\\)', einh: '',
              text: '\\(\\overline{ZP} = ' + z(d1) + '\\,\\text{cm}\\). Der Bildpunkt \\(P\'\\) liegt auf ' + (neg ? 'der anderen Seite' : 'derselben Seite') + ' von \\(Z\\), \\(' + z(d2) + '\\,\\text{cm}\\) von \\(Z\\) entfernt. Wie gross ist \\(k\\)?',
              falsch: [[-k, neg ? 'Das Vorzeichen fehlt: Liegt \\(P\'\\) auf der anderen Seite von \\(Z\\), ist \\(k\\) negativ.' : 'Auf derselben Seite von \\(Z\\) ist \\(k\\) positiv.', 'Vorzeichen'],
                       [(neg ? -1 : 1) * d1 / d2, 'Kehrwert: \\(k\\) ist Bildabstand durch Originalabstand, \\(\\overline{ZP\'} : \\overline{ZP}\\).', 'Kehrwert'],
                       [d2 - d1, 'Nicht die Differenz: \\(k\\) ist ein Faktor, \\(\\overline{ZP\'} : \\overline{ZP}\\).', 'Differenz']] };
          }
          var kk = zufall([-3, -2, -1.5, -0.5, 0.5, 1.5, 2.5, 3]);
          if (art === 'bild'){
            var L = zufall([2, 3, 4, 5, 6, 2.4, 3.5, 4.2]);
            return { art: art, werte: [L, kk], soll: r2(Math.abs(kk) * L), lab: '\\(\\overline{A\'B\'} =\\)', einh: 'cm',
              text: 'Eine Strecke \\(AB\\) ist \\(' + z(L) + '\\,\\text{cm}\\) lang. Wie lang ist ihr Bild \\(A\'B\'\\) bei der zentrischen Streckung mit \\(k = ' + tz(kk) + '\\)?',
              falsch: [[kk * L, 'Eine Länge ist nie negativ: mit dem Betrag \\(|k|\\) multiplizieren.', 'negativ'], [kk * kk * L, 'Das ist \\(k^2\\) mal die Länge. Längen wachsen mit \\(|k|\\), Flächen mit \\(k^2\\).', 'Quadrat'],
                       [L / Math.abs(kk), 'Geteilt statt multipliziert: \\(\\overline{A\'B\'} = |k| \\cdot \\overline{AB}\\).', 'geteilt']] };
          }
          var L2 = zufall([3, 4.5, 6, 7.5, 9, 12, 2, 1.5]);
          if (!ganz2(L2 / Math.abs(kk))) return TYPEN['streckfaktor'].neu();
          return { art: art, werte: [L2, kk], soll: r2(L2 / Math.abs(kk)), lab: '\\(\\overline{AB} =\\)', einh: 'cm',
            text: 'Bei einer zentrischen Streckung mit \\(k = ' + tz(kk) + '\\) ist die Bildstrecke \\(A\'B\'\\) \\(' + z(L2) + '\\,\\text{cm}\\) lang. Wie lang ist die Originalstrecke \\(AB\\)?',
            falsch: [[L2 * Math.abs(kk), 'Das wäre das Bild von \\(A\'B\'\\). Gesucht ist das Original: \\(\\overline{AB} = \\overline{A\'B\'} : |k|\\).', 'umgekehrt'],
                     [L2 / kk, 'Eine Länge ist nie negativ: durch den Betrag \\(|k|\\) teilen.', 'negativ']] };
        },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return einfach(A, e, A.art === 'k' ? '\\(|k| = \\overline{ZP\'} : \\overline{ZP}\\); das Vorzeichen sagt, auf welcher Seite von \\(Z\\) das Bild liegt.' : 'Längen werden mit \\(|k|\\) multipliziert.'); },
        loesung: function(A){ return A.art === 'k' ? 'k = ' + (A.soll < 0 ? '-' : '') + '\\tfrac{' + z(A.werte[1]) + '}{' + z(A.werte[0]) + '} = ' + tz(A.soll)
          : A.art === 'bild' ? '|' + tz(A.werte[1]) + '| \\cdot ' + z(A.werte[0]) + ' = ' + z(A.soll) + '\\,\\text{cm}' : z(A.werte[0]) + ' : |' + tz(A.werte[1]) + '| = ' + z(A.soll) + '\\,\\text{cm}'; } },

      /* ── Kapitel 2 ── */
      /* 1. Strahlensatz (auch Variante mit den Abschnitten und X-Figur). Figur massstäblich, Gesuchtes als «?». */
      'strahlen1': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} cm',
        schl: function(A){ return 'st|' + A.sa + '|' + A.sa2 + '|' + A.dritt + '|' + A.was; },
        vorbereiten: beschriften,
        neu: function(){
          var sa, k, sb;
          do { sa = zufall([2, 2.5, 3, 4, 5, 6]); k = zufall([1.5, 2, 2.5, 3, 4]); sb = zufall([2, 3, 3.5, 4, 4.5, 5, 6]); }
          while (sb === sa || !ganz2(sa * k) || !ganz2(sb * k));
          var sa2 = r2(sa * k), sb2 = r2(sb * k), was = zufall(['sb2', 'sb2', 'bb', 'sb']), x = was !== 'bb' && Math.random() < 0.3;
          var A = { sa: sa, k: x ? -k : k, sa2: sa2, sb: sb, sb2: sb2, was: was, x: x, th: zufall([32, 40, 48]) };
          var vor = x ? '\\(S\\) liegt zwischen den Parallelen (X-Figur). ' : '';
          if (was === 'sb2'){ A.dritt = sb; A.soll = sb2; A.lab = '\\(\\overline{SB\'} =\\)';
            A.text = vor + '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = ' + z(sa) + '\\), \\(\\overline{SA\'} = ' + z(sa2) + '\\), \\(\\overline{SB} = ' + z(sb) + '\\). Wie lang ist \\(\\overline{SB\'}\\)?';
            A.falsch = [[sb * sa / sa2, 'Das Verhältnis steht verkehrt: \\(B\'\\) liegt weiter von \\(S\\) weg als \\(B\\).', 'verkehrt'], [sb + (sa2 - sa), 'Nicht den Unterschied übertragen: Die Strecken stehen im gleichen Verhältnis, nicht im gleichen Abstand.', 'Unterschied']]; }
          else if (was === 'sb'){ A.dritt = sb2; A.soll = sb; A.lab = '\\(\\overline{SB} =\\)';
            A.text = vor + '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = ' + z(sa) + '\\), \\(\\overline{SA\'} = ' + z(sa2) + '\\), \\(\\overline{SB\'} = ' + z(sb2) + '\\). Wie lang ist \\(\\overline{SB}\\)?';
            A.falsch = [[sb2 * sa2 / sa, 'Das Verhältnis steht verkehrt: \\(B\\) liegt näher bei \\(S\\) als \\(B\'\\).', 'verkehrt'], [sb2 - (sa2 - sa), 'Nicht den Unterschied abziehen: Die Strecken stehen im gleichen Verhältnis.', 'Unterschied']]; }
          else { A.dritt = sb; A.soll = r2(sb2 - sb); A.lab = '\\(\\overline{BB\'} =\\)'; A.aa = r2(sa2 - sa);
            A.text = '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = ' + z(sa) + '\\), \\(\\overline{AA\'} = ' + z(A.aa) + '\\), \\(\\overline{SB} = ' + z(sb) + '\\). Wie lang ist \\(\\overline{BB\'}\\)?';
            A.falsch = [[sb2, 'Das ist \\(\\overline{SB\'}\\). Gesucht ist das Stück \\(\\overline{BB\'}\\).', 'SB'], [sb * sa / A.aa, 'Das Verhältnis steht verkehrt: \\(\\overline{SA} : \\overline{AA\'} = \\overline{SB} : \\overline{BB\'}\\).', 'verkehrt'],
                        [A.aa, 'Gleich lange Stücke gibt es nur, wenn \\(\\overline{SA} = \\overline{SB}\\). Die Strecken stehen im gleichen Verhältnis.', 'gleich']]; }
          return A; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        zeichne: function(svg, A){ strahlenBild(svg, A, { sa: z(A.sa), sa2: A.was === 'bb' ? null : z(A.sa2), aa: A.was === 'bb' ? z(A.aa) : null,
          sb: A.was === 'sb' ? '?' : z(A.sb), sb2: A.was === 'sb2' ? '?' : A.was === 'sb' ? z(A.sb2) : null, bb: A.was === 'bb' ? '?' : null }); },
        pruefen: function(A, e){ return einfach(A, e, A.was === 'bb' ? 'Variante des 1. Strahlensatzes: \\(\\overline{SA} : \\overline{AA\'} = \\overline{SB} : \\overline{BB\'}\\).' : '1. Strahlensatz: \\(\\overline{SA} : \\overline{SA\'} = \\overline{SB} : \\overline{SB\'}\\).'); },
        loesung: function(A){ return A.was === 'sb2' ? '\\overline{SB\'} = ' + z(A.sb) + ' \\cdot \\tfrac{' + z(A.sa2) + '}{' + z(A.sa) + '} = ' + z(A.soll)
          : A.was === 'sb' ? '\\overline{SB} = ' + z(A.sb2) + ' \\cdot \\tfrac{' + z(A.sa) + '}{' + z(A.sa2) + '} = ' + z(A.soll) : '\\overline{BB\'} = ' + z(A.sb) + ' \\cdot \\tfrac{' + z(A.aa) + '}{' + z(A.sa) + '} = ' + z(A.soll); } },

      /* 2. Strahlensatz: Parallelenstück. Falle: AA′ statt SA′ (die ganzen Strecken ab S gehören dazu). */
      'strahlen2': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} cm',
        schl: function(A){ return 'st|' + A.sa + '|' + A.sa2 + '|' + A.dritt + '|' + A.was; },
        vorbereiten: beschriften,
        neu: function(){
          var sa, k, ab, sb, th, tries = 0;
          do { sa = zufall([2, 2.5, 3, 4, 5]); k = zufall([1.5, 2, 2.5, 3]); ab = zufall([1.5, 2, 2.5, 3, 3.5, 4]);
               sb = zufall([2, 2.5, 3, 3.5, 4, 5, 6]); var c = (sa * sa + sb * sb - ab * ab) / (2 * sa * sb); th = c > -1 && c < 1 ? Math.acos(c) * 180 / PI : 0; tries++; }
          while ((th < 25 || th > 75 || sb === sa || !ganz2(sa * k) || !ganz2(ab * k)) && tries < 500);
          var sa2 = r2(sa * k), ab2 = r2(ab * k), aa = r2(sa2 - sa), was = zufall(['ab2', 'ab2aa', 'ab2aa', 'ab']), x = was === 'ab2' && Math.random() < 0.4;
          var A = { sa: sa, sa2: sa2, k: x ? -k : k, sb: sb, ab: ab, ab2: ab2, aa: aa, was: was, x: x, th: th };
          if (was === 'ab2'){ A.dritt = ab; A.soll = ab2; A.lab = '\\(\\overline{A\'B\'} =\\)';
            A.text = (x ? '\\(S\\) liegt zwischen den Parallelen (X-Figur). ' : '') + '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = ' + z(sa) + '\\), \\(\\overline{SA\'} = ' + z(sa2) + '\\), \\(\\overline{AB} = ' + z(ab) + '\\). Wie lang ist \\(\\overline{A\'B\'}\\)?';
            A.falsch = [[ab / k, 'Das Verhältnis steht verkehrt: \\(A\'\\) liegt weiter von \\(S\\) weg als \\(A\\), also ist \\(A\'B\'\\) länger.', 'verkehrt'], [ab + (sa2 - sa), 'Nicht den Unterschied addieren: Die Strecken stehen im gleichen Verhältnis.', 'Unterschied']]; }
          else if (was === 'ab2aa'){ A.dritt = ab; A.soll = ab2; A.was = 'ab2aa'; A.lab = '\\(\\overline{A\'B\'} =\\)';
            A.text = '\\(AB \\parallel A\'B\'\\), \\(\\overline{SA} = ' + z(sa) + '\\), \\(\\overline{AA\'} = ' + z(aa) + '\\), \\(\\overline{AB} = ' + z(ab) + '\\). Wie lang ist \\(\\overline{A\'B\'}\\)?';
            A.falsch = [[ab * aa / sa, 'Das ist \\(\\overline{AB} \\cdot \\overline{AA\'} : \\overline{SA}\\). Zum 2. Strahlensatz gehören die ganzen Strecken ab \\(S\\): \\(\\overline{SA\'} = \\overline{SA} + \\overline{AA\'}\\).', 'ganzen'],
                        [ab / k, 'Das Verhältnis steht verkehrt: \\(A\'B\'\\) ist länger als \\(AB\\).', 'verkehrt'], [ab + aa, 'Nicht addieren: Die Strecken stehen im gleichen Verhältnis.', 'addieren']]; }
          else { var sb2 = r2(sb * k), bb = r2(sb2 - sb); if (!ganz2(sb * k)) return TYPEN['strahlen2'].neu();
            A.sb2 = sb2; A.bb = bb; A.dritt = ab2; A.soll = ab; A.lab = '\\(\\overline{AB} =\\)';
            A.text = '\\(AB \\parallel A\'B\'\\), \\(\\overline{SB} = ' + z(sb) + '\\), \\(\\overline{BB\'} = ' + z(bb) + '\\), \\(\\overline{A\'B\'} = ' + z(ab2) + '\\). Wie lang ist \\(\\overline{AB}\\)?';
            A.falsch = [[ab2 * sb / bb, 'Das ist \\(\\overline{A\'B\'} \\cdot \\overline{SB} : \\overline{BB\'}\\). Zu den Parallelen gehören die ganzen Strecken ab \\(S\\): \\(\\overline{SB\'} = \\overline{SB} + \\overline{BB\'}\\).', 'ganzen'],
                        [ab2 * k, 'Das Verhältnis steht verkehrt: \\(AB\\) liegt näher bei \\(S\\), ist also kürzer als \\(A\'B\'\\).', 'verkehrt']]; }
          return A; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        zeichne: function(svg, A){ strahlenBild(svg, A, A.was === 'ab' ? { sb: z(A.sb), bb: z(A.bb), ab2: z(A.ab2), ab: '?' }
          : { sa: z(A.sa), sa2: A.was === 'ab2' ? z(A.sa2) : null, aa: A.was === 'ab2aa' ? z(A.aa) : null, ab: z(A.ab), ab2: '?' }); },
        pruefen: function(A, e){ return einfach(A, e, '2. Strahlensatz: \\(\\overline{AB} : \\overline{A\'B\'} = \\overline{SA} : \\overline{SA\'}\\) — mit den ganzen Strecken ab \\(S\\).'); },
        loesung: function(A){ return A.was === 'ab' ? '\\overline{AB} = ' + z(A.ab2) + ' \\cdot \\tfrac{' + z(A.sb) + '}{' + z(r2(A.sb + A.bb)) + '} = ' + z(A.soll)
          : '\\overline{A\'B\'} = ' + z(A.ab) + ' \\cdot \\tfrac{' + z(A.sa2) + '}{' + z(A.sa) + '} = ' + z(A.soll); } },

      /* ── Kapitel 3 ── */
      /* Fläche mit k², Umfang mit k, k aus dem Flächenverhältnis. k = 2 nicht bei «Bildfläche»: Dort gäbe «2k statt k²»
         dasselbe Ergebnis (der Fehler wäre unsichtbar). */
      'flaeche': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} <span class="ue-einh"></span>',
        schl: function(A){ return 'fl|' + A.art + '|' + A.werte.join('|'); },
        vorbereiten: beschriften,
        neu: function(){
          var art = zufall(['bild', 'bild', 'k', 'k', 'orig', 'umfang']), fig = zufall(['Ein Dreieck', 'Ein Rechteck', 'Ein Kreis', 'Ein Sechseck', 'Ein Grundstück auf einem Plan', 'Ein Logo']);
          var k = zufall([1.5, 2.5, 3, 0.5, 4, 1.2, 0.8, 2]), A0 = zufall([4, 6, 8, 10, 12, 20, 2.5, 5]);
          if (art === 'bild'){
            if (k === 2) k = 3;
            if (!ganz2(k * k * A0)) return TYPEN['flaeche'].neu();
            return { art: art, werte: [A0, k], soll: r2(k * k * A0), lab: '\\(A\' =\\)', einh: 'cm²',
              text: fig + ' mit der Fläche \\(' + z(A0) + '\\,\\text{cm}^2\\) wird mit \\(k = ' + z(k) + '\\) gestreckt. Wie gross ist die Fläche des Bildes?',
              falsch: [[k * A0, 'Flächen wachsen mit \\(k^2\\), nicht mit \\(k\\).', 'Quadrat'], [2 * k * A0, '\\(k^2\\) heisst \\(k \\cdot k\\), nicht \\(2 \\cdot k\\).', 'mal zwei']] };
          }
          if (art === 'umfang'){
            var u = zufall([6, 8, 10, 12, 15, 18, 24]);
            return { art: art, werte: [u, k], soll: r2(k * u), lab: '\\(u\' =\\)', einh: 'cm',
              text: fig + ' mit dem Umfang \\(' + z(u) + '\\,\\text{cm}\\) wird mit \\(k = ' + z(k) + '\\) gestreckt. Wie gross ist der Umfang des Bildes?',
              falsch: [[k * k * u, 'Der Umfang ist eine Länge: Er wächst mit \\(k\\), nicht mit \\(k^2\\).', 'Länge'], [u + k, 'Strecken heisst multiplizieren.', 'plus']] };
          }
          if (art === 'k'){
            /* In 40 % der Würfe ist das Flächenverhältnis keine Quadratzahl (2, 3, 5 …): k = √2 ≈ 1.41 usw., gerundet
               auf zwei Dezimalen — wie im Gesamttest (Prüfung 08.10.2026: irrationales k kaum geübt). */
            var wurzel = Math.random() < 0.4, q2 = wurzel ? zufall([2, 3, 5, 6, 8, 10]) : null;
            var q = wurzel ? Math.sqrt(q2) : zufall([1.5, 2, 2.5, 3, 4, 1.2]), A1 = r2(wurzel ? q2 * A0 : q * q * A0);
            if (!ganz2(wurzel ? q2 * A0 : q * q * A0)) return TYPEN['flaeche'].neu();
            return { art: art, werte: [A0, A1], soll: r2(q), wurzel: wurzel, lab: '\\(k ' + (wurzel ? '\\approx' : '=') + '\\)', einh: '',
              text: fig + ' mit der Fläche \\(' + z(A0) + '\\,\\text{cm}^2\\) wird zu einer ähnlichen Figur mit der Fläche \\(' + z(A1) + '\\,\\text{cm}^2\\) vergrössert. Mit welchem Faktor \\(k\\) wachsen die Längen?' + (wurzel ? ' Runde auf zwei Dezimalen.' : ''),
              falsch: [[A1 / A0, 'Das ist \\(\\tfrac{A\'}{A} = k^2\\). Die Längen wachsen mit der Wurzel daraus.', 'Wurzel'], [A1 / A0 / 2, '\\(k^2\\) heisst \\(k \\cdot k\\), nicht \\(2 \\cdot k\\): Zieh die Wurzel.', 'halb'], [A1 - A0, 'Nicht die Differenz: Gesucht ist ein Faktor.', 'Differenz']] };
          }
          var A2 = r2(k * k * A0);
          if (!ganz2(k * k * A0)) return TYPEN['flaeche'].neu();
          return { art: art, werte: [A2, k], soll: A0, lab: '\\(A =\\)', einh: 'cm²',
            text: fig + ' wurde mit \\(k = ' + z(k) + '\\) gestreckt; das Bild hat die Fläche \\(' + z(A2) + '\\,\\text{cm}^2\\). Wie gross war die Fläche des Originals?',
            falsch: [[A2 / k, 'Flächen wachsen mit \\(k^2\\): durch \\(k^2\\) teilen, nicht durch \\(k\\).', 'Quadrat'], [A2 * k * k, 'Umgekehrt: Das Original ist ' + (k > 1 ? 'kleiner' : 'grösser') + ' als das Bild.', 'umgekehrt']] };
        },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return einfach(A, e, A.art === 'umfang' ? 'Längen — auch der Umfang — wachsen mit \\(k\\).' : 'Flächen wachsen mit \\(k^2\\): \\(A\' = k^2 \\cdot A\\).'); },
        loesung: function(A){ return A.art === 'bild' ? 'A\' = ' + z(A.werte[1]) + '^2 \\cdot ' + z(A.werte[0]) + ' = ' + z(A.soll) + '\\,\\text{cm}^2'
          : A.art === 'umfang' ? 'u\' = ' + z(A.werte[1]) + ' \\cdot ' + z(A.werte[0]) + ' = ' + z(A.soll) + '\\,\\text{cm}'
          : A.art === 'k' ? 'k = \\sqrt{\\tfrac{' + z(A.werte[1]) + '}{' + z(A.werte[0]) + '}} = \\sqrt{' + z(r2(A.werte[1] / A.werte[0])) + '} ' + (A.wurzel ? '\\approx ' : '= ') + z(A.soll)
          : 'A = \\tfrac{' + z(A.werte[0]) + '}{' + z(A.werte[1]) + '^2} = ' + z(A.soll) + '\\,\\text{cm}^2'; } },

      /* Massstab 1 : n: Längen mal n, Flächen mal n². Gefragt in m oder km bzw. m² oder km². */
      'massstab': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} <span class="ue-einh"></span>',
        schl: function(A){ return 'ms|' + A.n + '|' + A.art + '|' + A.wert; },
        vorbereiten: beschriften,
        neu: function(){
          var art = zufall(['laenge', 'flaeche', 'flaeche', 'karte']), n = zufall([200, 500, 1000, 2000, 5000, 10000, 25000, 50000]);
          var nn = '1 : ' + (n >= 10000 ? String(n).replace(/(\d)(?=(\d{3})+$)/g, '$1\\,') : n), gross = n >= 10000;
          if (art === 'laenge'){
            var L = zufall([2.4, 3.5, 4.8, 6, 7.2, 8.5, 12, 15.6]), m = L * n / 100;
            return { art: art, n: n, wert: L, soll: r2(gross ? m / 1000 : m), lab: 'In Wirklichkeit:', einh: gross ? 'km' : 'm',
              text: 'Massstab \\(' + nn + '\\): Auf dem Plan ist eine Strecke \\(' + z(L) + '\\,\\text{cm}\\) lang. Wie lang ist sie in Wirklichkeit?',
              falsch: gross ? [[m, 'Das sind Meter. Gefragt sind Kilometer: \\(1\\,\\text{km} = 1000\\,\\text{m}\\).', 'Meter'], [L * n / 1000, 'Umrechnen: \\(1\\,\\text{km} = 100\\,000\\,\\text{cm}\\).', 'Einheit']]
                : [[L * n, 'Das sind Zentimeter. Umrechnen: \\(1\\,\\text{m} = 100\\,\\text{cm}\\).', 'Zentimeter'], [L * n / 1000, 'Umrechnen: \\(1\\,\\text{m} = 100\\,\\text{cm}\\), nicht \\(1000\\).', 'Einheit']] };
          }
          var F = zufall([1.5, 2, 2.5, 3.2, 4, 4.5, 6, 8]), cm2 = F * n * n;
          if (art === 'flaeche'){
            var m2 = cm2 / 1e4;
            gross = n >= 25000 && ganz2(m2 / 1e6);
            return { art: art, n: n, wert: F, soll: r2(gross ? m2 / 1e6 : m2), lab: 'In Wirklichkeit:', einh: gross ? 'km²' : 'm²',
              text: 'Massstab \\(' + nn + '\\): Auf dem Plan hat ein Grundstück die Fläche \\(' + z(F) + '\\,\\text{cm}^2\\). Wie gross ist es in Wirklichkeit?',
              falsch: [[gross ? F * n / 1e10 : F * n / 1e4, 'Flächen wachsen mit \\(n^2\\), nicht mit \\(n\\): mal \\(' + n + '^2\\).', 'Quadrat'],
                       [gross ? cm2 / 1e8 : cm2 / 100, gross ? 'Umrechnen: \\(1\\,\\text{km}^2 = 10^{10}\\,\\text{cm}^2\\) (\\(100\\,000^2\\)).' : 'Umrechnen: \\(1\\,\\text{m}^2 = 10\\,000\\,\\text{cm}^2\\), nicht \\(100\\).', 'Einheit']] };
          }
          var Fm = gross ? zufall([0.25, 0.5, 1.25, 2, 3]) : zufall([100, 250, 400, 800, 1200, 2000]);   // km² bzw. m²
          var Fcm = gross ? Fm * 1e10 / (n * n) : Fm * 1e4 / (n * n);
          if (!ganz2(Fcm) || Fcm < 0.1 || Fcm > 400) return TYPEN['massstab'].neu();
          return { art: art, n: n, wert: Fm, gross: gross, soll: r2(Fcm), lab: 'Auf dem Plan:', einh: 'cm²',
            text: 'Massstab \\(' + nn + '\\): Ein Grundstück ist in Wirklichkeit \\(' + z(Fm) + '\\,\\text{' + (gross ? 'km' : 'm') + '}^2\\) gross. Wie gross ist es auf dem Plan?',
            falsch: [[Fcm * n, 'Flächen schrumpfen mit \\(n^2\\): durch \\(' + n + '^2\\) teilen, nicht durch \\(' + n + '\\).', 'Quadrat']].concat(gross ? [] : [[Fcm / 100, 'Umrechnen: \\(1\\,\\text{m}^2 = 10\\,000\\,\\text{cm}^2\\).', 'Einheit']]) };
        },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return einfach(A, e, 'Massstab \\(1 : n\\): Längen mal \\(n\\), Flächen mal \\(n^2\\) — dann die Einheit umrechnen.'); },
        loesung: function(A){
          if (A.art === 'laenge') return z(A.wert) + '\\,\\text{cm} \\cdot ' + A.n + ' = ' + z(r2(A.wert * A.n)) + '\\,\\text{cm} = ' + z(A.soll) + '\\,\\text{' + A.einh + '}';
          if (A.art === 'flaeche') return z(A.wert) + '\\,\\text{cm}^2 \\cdot ' + A.n + '^2 = ' + z(r2(A.wert * A.n * A.n)) + '\\,\\text{cm}^2 = ' + z(A.soll) + '\\,\\text{' + A.einh.replace('²', '}^2\\text{') + '}';
          return z(A.wert) + '\\,\\text{' + (A.gross ? 'km' : 'm') + '}^2 = ' + z(A.wert) + (A.gross ? ' \\cdot 10^{10}' : ' \\cdot 10\\,000') + '\\,\\text{cm}^2;\\ \\text{geteilt durch } ' + A.n + '^2 = ' + z(A.soll) + '\\,\\text{cm}^2'; } },

      /* ── Kapitel 4 ── */
      /* Ähnlich oder nicht? WW (dritter Winkel aus der Winkelsumme) oder sss (Seiten der Grösse nach ordnen,
         alle drei Verhältnisse vergleichen; zwei gleiche Verhältnisse genügen nicht). */
      'aehnlich': { felder: ['s'], muster: 'Die Dreiecke sind {s:ähnlich|nicht ähnlich}.',
        schl: function(A){ return 'ae|' + A.art + '|' + A.s1.slice().sort(function(p, q){ return p - q; }).join('|') + '|' + A.s2.slice().sort(function(p, q){ return p - q; }).join('|'); },
        neu: function(){
          var ja = Math.random() < 0.5, satz = Math.random();
          /* sWs und SsW (Prüfung 08.10.2026: nur genannt, nicht geübt): zwei Seiten und ein Winkel je Dreieck. Bei sWs der
             eingeschlossene Winkel, bei SsW der Gegenwinkel der grösseren Seite. «Nicht ähnlich» entweder über den Winkel
             oder über ein Seitenverhältnis — nie über einen Winkel an der falschen Stelle (dann wäre es unentscheidbar). */
          if (satz >= 0.6){
            var sws = satz < 0.8, P2 = zufall([[4, 6], [5, 8], [3, 7], [6, 9], [4, 10], [5, 6], [6, 8]]), kf = zufall([1.5, 2, 2.5, 0.5, 3]);
            var w = sws ? zufallG(5, 24) * 5 : zufallG(6, 24) * 5, w2 = w, t = [r2(P2[0] * kf), r2(P2[1] * kf)];
            if (!ja){
              if (Math.random() < 0.5){ w2 = w + zufall([-20, -15, -10, 10, 15, 20]); if (w2 < 20 || w2 > 150) return TYPEN['aehnlich'].neu(); }
              else { t[1] = r2(t[1] + zufall([-1, 1]) * (kf >= 1 ? 1 : 0.5)); if (t[1] <= t[0]) return TYPEN['aehnlich'].neu(); }
            }
            var gleichV = gl(t[0] / P2[0], t[1] / P2[1]);
            if ((gleichV && w2 === w) !== ja) return TYPEN['aehnlich'].neu();
            var art2 = sws ? 'sws' : 'ssw', reihe = Math.random() < 0.5;   // Reihenfolge der Seiten im Text von Dreieck 2
            var nenne = function(S, ww){ var a = reihe && S !== P2 ? [S[1], S[0]] : S;
              return sws ? 'zwei Seiten \\(' + z(a[0]) + '\\) und \\(' + z(a[1]) + '\\), der Winkel zwischen ihnen \\(' + ww + '°\\)'
                         : 'Seiten \\(' + z(a[0]) + '\\) und \\(' + z(a[1]) + '\\), der Winkel gegenüber der Seite \\(' + z(S[1]) + '\\) ist \\(' + ww + '°\\)'; };
            return { art: art2, ja: ja, soll: ja ? 'ähnlich' : 'nicht ähnlich', s1: [P2[0], P2[1], w], s2: [t[0], t[1], w2],
              text: 'Dreieck 1: ' + nenne(P2, w) + '. Dreieck 2: ' + nenne(t, w2) + '.',
              grund: 'Kürzere zu kürzerer, längere zu längerer Seite: \\(\\tfrac{' + z(t[0]) + '}{' + P2[0] + '} ' + zz(t[0] / P2[0]) + '\\), \\(\\tfrac{' + z(t[1]) + '}{' + P2[1] + '} ' + zz(t[1] / P2[1]) + '\\); '
                + (sws ? 'eingeschlossener Winkel ' : 'Gegenwinkel der grösseren Seite ') + '\\(' + w + '°\\) bzw. \\(' + w2 + '°\\). '
                + (ja ? 'Beide Verhältnisse gleich und der Winkel gleich: ähnlich (' + (sws ? 'sWs' : 'SsW') + ').' : (gleichV ? 'Die Winkel sind verschieden: nicht ähnlich.' : 'Die Verhältnisse sind verschieden: nicht ähnlich.')) };
          }
          if (satz < 0.3){
            var al = zufallG(6, 15) * 5, be = zufallG(6, 22) * 5, ga = 180 - al - be;
            if (ga < 25 || al === be || be === ga || al === ga) return TYPEN['aehnlich'].neu();
            var w2 = mischen([al, be, ga]).slice(0, 2);
            if (!ja){ var d = zufall([-15, -10, -5, 5, 10, 15]); w2[1] += d; if (w2[0] + w2[1] >= 175 || w2[1] < 20) return TYPEN['aehnlich'].neu(); }
            var g2 = 180 - w2[0] - w2[1];
            var gleich = [al, be, ga].sort().join() === [w2[0], w2[1], g2].sort().join();
            if (gleich !== ja) return TYPEN['aehnlich'].neu();
            return { art: 'ww', ja: ja, soll: ja ? 'ähnlich' : 'nicht ähnlich', s1: [al, be, ga], s2: [w2[0], w2[1], g2],
              text: 'Dreieck 1 hat die Winkel \\(' + al + '°\\) und \\(' + be + '°\\). Dreieck 2 hat die Winkel \\(' + w2[0] + '°\\) und \\(' + w2[1] + '°\\).',
              grund: 'Dritter Winkel: \\(180° - ' + al + '° - ' + be + '° = ' + ga + '°\\) bzw. \\(180° - ' + w2[0] + '° - ' + w2[1] + '° = ' + g2 + '°\\). '
                + (ja ? 'Beide haben die Winkel \\(' + [al, be, ga].sort(function(p, q){ return p - q; }).join('°\\), \\(') + '°\\): ähnlich (WW).' : 'Die Winkel stimmen nicht überein: nicht ähnlich.') };
          }
          var S = zufall([[4, 5, 6], [5, 6, 7], [3, 5, 7], [4, 6, 7], [5, 7, 8], [6, 7, 9], [4, 7, 8], [5, 6, 8]]), k = zufall([1.5, 2, 2.5, 0.5, 3]);
          var t2 = S.map(function(s){ return r2(s * k); });
          if (!ja){ var j = zufallG(0, 2); t2[j] = r2(t2[j] + zufall([-1, -0.5, 0.5, 1]) * (k >= 1 ? 1 : 0.5)); var srt = t2.slice().sort(function(p, q){ return p - q; }); if (srt[0] + srt[1] <= srt[2] || t2[j] <= 0) return TYPEN['aehnlich'].neu(); }
          var t2m = mischen(t2), so = t2.slice().sort(function(p, q){ return p - q; }), q = S.map(function(s, i){ return so[i] / s; });
          return { art: 'sss', ja: ja, soll: ja ? 'ähnlich' : 'nicht ähnlich', s1: S.slice(), s2: t2m, k: k,
            text: 'Dreieck 1 hat die Seiten \\(' + S.join('\\), \\(') + '\\). Dreieck 2 hat die Seiten \\(' + t2m.map(z).join('\\), \\(') + '\\).',
            grund: 'Der Grösse nach geordnet: \\(' + q.map(function(x, i){ return '\\tfrac{' + z(so[i]) + '}{' + S[i] + '} ' + zz(x); }).join('\\), \\(') + '\\). '
              + (ja ? 'Alle drei Verhältnisse sind gleich: ähnlich (sss), \\(k = ' + z(k) + '\\).' : 'Die Verhältnisse sind nicht alle gleich: nicht ähnlich.') };
        },
        eingabe: function(A){ return { s: A.soll }; },
        fehler: function(A){ return [[{ s: A.ja ? 'nicht ähnlich' : 'ähnlich' }, null]]; },
        gut: function(A){ return A.grund; },
        pruefen: function(A, e){
          if (e.s === A.soll) return null;
          if (A.art === 'ww') return A.ja ? 'Rechne zu beiden Dreiecken den dritten Winkel aus und vergleiche alle drei Winkel.' : 'Zwei Winkel genügen — aber sie müssen übereinstimmen. Rechne den dritten Winkel aus und vergleiche.';
          if (A.art === 'sws' || A.art === 'ssw') return A.ja ? 'Vergleiche kürzere mit kürzerer und längere mit längerer Seite: Stimmen beide Verhältnisse und der Winkel überein?'
            : 'Prüf beides: die zwei Seitenverhältnisse (kürzere zu kürzerer, längere zu längerer) und den Winkel.';
          return A.ja ? 'Ordne beide Seitenlisten der Grösse nach und vergleiche die Verhältnisse entsprechender Seiten.' : 'Vergleiche alle drei Verhältnisse, nicht nur zwei: Ordne die Seiten der Grösse nach.'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* Entsprechende Seiten zuordnen: Gleich markierte Winkel sind gleich, entsprechende Seiten liegen gleichen
         Winkeln gegenüber. Die Ecken von PQR sind gegenüber ABC vertauscht (nie in derselben Reihenfolge, sonst
         fiele die Zuordnung nach Buchstaben nicht auf). */
      'zuordnen': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} cm',
        schl: function(A){ return 'zu|' + A.S.join('|') + '|' + A.k; },
        vorbereiten: beschriften,
        neu: function(){
          var S = zufall([[4, 5, 6], [5, 6, 7], [3, 5, 7], [4, 6, 7], [5, 7, 8], [6, 7, 9], [4, 7, 8]]), k = zufall([1.5, 2, 2.5, 0.5, 3, 1.2]);
          var pi = zufall([[1, 2, 0], [2, 0, 1], [1, 0, 2], [0, 2, 1], [2, 1, 0]]);   // P, Q, R entsprechen den Ecken pi[0], pi[1], pi[2] von ABC (0 = A …)
          var N = ['A', 'B', 'C'], M = ['P', 'Q', 'R'];
          function seite1(i, j){ return S[3 - i - j]; }                              // Seite zwischen Ecken i und j von ABC (gegenüber der dritten)
          var paare = [[0, 1], [1, 2], [2, 0]], gp = zufall(paare), ap = zufall(paare.filter(function(p){ return p !== gp; }));
          var gl1 = seite1(pi[gp[0]], pi[gp[1]]), gl2 = r2(k * gl1), ges = r2(k * seite1(pi[ap[0]], pi[ap[1]]));
          // Zuordnung nach Buchstaben: P↔A, Q↔B, R↔C
          var naivK = gl2 / seite1(gp[0], gp[1]), naiv = naivK * seite1(ap[0], ap[1]);
          if (Math.abs(naiv - ges) < 0.07 || !ganz2(gl2) || !ganz2(ges)) return TYPEN['zuordnen'].neu();
          var nm = function(p, L){ return L[p[0]] + L[p[1]]; };
          return { S: S, k: k, pi: pi, gp: gp, ap: ap, gl2: gl2, soll: ges, lab: '\\(\\overline{' + nm(ap, M) + '} =\\)',
            text: 'Die Dreiecke \\(ABC\\) und \\(PQR\\) sind ähnlich: Gleich markierte Winkel sind gleich gross. \\(\\overline{BC} = ' + S[0] + '\\), \\(\\overline{CA} = ' + S[1] + '\\), \\(\\overline{AB} = ' + S[2] + '\\) und \\(\\overline{' + nm(gp, M) + '} = ' + z(gl2) + '\\). Wie lang ist \\(\\overline{' + nm(ap, M) + '}\\)?',
            falsch: [[naiv, 'Zugeordnet nach den Buchstaben (\\(P\\) wie \\(A\\), \\(Q\\) wie \\(B\\) …)? Entsprechende Seiten liegen gleich markierten Winkeln gegenüber.', 'Buchstaben'],
                     [seite1(pi[ap[0]], pi[ap[1]]) / k, 'Geteilt statt multipliziert: Prüf, welches Dreieck das grössere ist.', 'verkehrt'],
                     [k * k * seite1(pi[ap[0]], pi[ap[1]]), 'Das ist mit \\(k^2\\) gerechnet. Seiten wachsen mit \\(k\\).', 'Quadrat']] };
        },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        zeichne: function(svg, A){
          // ABC: A(0|0), B(c|0), C aus den Seiten; PQR: dieselbe Form mal k, gedreht und verschoben
          var a = A.S[0], b = A.S[1], c = A.S[2], cx = (b * b + c * c - a * a) / (2 * c), cy = Math.sqrt(Math.max(0, b * b - cx * cx));
          var T1 = [[0, 0], [c, 0], [cx, cy]], s = A.k, dreh = grad(A.pi[0] * 70 + 35), sp = A.pi[1] === 0 ? -1 : 1;
          var lauf = [], i;
          for (i = 0; i < 3; i++){ var p = T1[A.pi[i]], x = p[0] * s, y = p[1] * s * sp; lauf.push([x * Math.cos(dreh) - y * Math.sin(dreh), x * Math.sin(dreh) + y * Math.cos(dreh)]); }
          var minx = Math.min.apply(null, lauf.map(function(p){ return p[0]; })), miny = Math.min.apply(null, lauf.map(function(p){ return p[1]; }));
          var T2 = lauf.map(function(p){ return [p[0] - minx + c + 2.6, p[1] - miny]; });
          var F = Flaeche(svg, fensterUm(T1.concat(T2), 1.0, 260, 150));
          F.vieleck(T1, 'figur'); F.vieleck(T2, 'bild');
          var bog = function(T, j, n){ var u = T[(j + 1) % 3], v = T[(j + 2) % 3]; winkelMarke(F, T[j], u, v, 9, 'winkelbogen', null, null, n); };
          for (i = 0; i < 3; i++){ bog(T1, i, i + 1); bog(T2, i, A.pi[i] + 1); }
          eckenText(F, T1, ['A', 'B', 'C'], 'ecke klein', 9); eckenText(F, T2, ['P', 'Q', 'R'], 'ecke klein bild', 9);
        },
        pruefen: function(A, e){ return einfach(A, e, 'Suche zur gegebenen Seite von \\(PQR\\) die Seite von \\(ABC\\), die dem gleich markierten Winkel gegenüberliegt: Daraus \\(k\\).'); },
        loesung: function(A){ return '\\overline{' + ['P', 'Q', 'R'][A.ap[0]] + ['P', 'Q', 'R'][A.ap[1]] + '} = ' + z(A.k) + ' \\cdot ' + z(A.S[3 - A.pi[A.ap[0]] - A.pi[A.ap[1]]]) + ' = ' + z(A.soll); } },

      /* Höhe im rechtwinkligen Dreieck (rechter Winkel bei C, Fusspunkt H; p liegt an a, q an b):
         h² = p · q, a² = p · c, b² = q · c. */
      'hoehensatz': { felder: ['x'], muster: '<span class="ue-lab"></span> {x} cm',
        schl: function(A){ return 'hs|' + A.art + '|' + A.werte.join('|'); },
        vorbereiten: beschriften,
        neu: function(){
          var pq = zufall([[1.8, 3.2], [3.6, 6.4], [2, 8], [1, 4], [2.5, 10], [2.7, 4.8], [5.4, 9.6], [3, 12], [4.5, 8], [6.4, 3.6], [8, 2], [3.2, 1.8], [6, 2], [2, 6]]);
          var p = pq[0], q = pq[1], c = r2(p + q), h = Math.sqrt(p * q), a = Math.sqrt(p * c), b = Math.sqrt(q * c), art = zufall(['h', 'h', 'kathete', 'abschnitt', 'q']);
          var A = { p: p, q: q, c: c, art: art };
          if (art === 'h'){ A.werte = [p, q]; A.soll = r2(h); A.lab = '\\(h =\\)'; A.zeige = { p: z(p), q: z(q), h: '?' };
            A.text = 'Rechtwinkliges Dreieck, rechter Winkel bei \\(C\\). Die Höhe \\(h\\) teilt die Hypotenuse in \\(p = ' + z(p) + '\\,\\text{cm}\\) und \\(q = ' + z(q) + '\\,\\text{cm}\\). Wie lang ist \\(h\\)?';
            A.falsch = [[(p + q) / 2, 'Das ist der Mittelwert. Höhensatz: \\(h^2 = p \\cdot q\\).', 'Mittelwert'], [p * q, 'Das ist \\(h^2\\). Zieh noch die Wurzel.', 'Wurzel'], [Math.sqrt(p * p + q * q), 'Das ist Pythagoras mit \\(p\\) und \\(q\\) — die stehen nicht senkrecht aufeinander.', 'Pythagoras']]; }
          else if (art === 'kathete'){ A.werte = [p, c]; A.soll = r2(a); A.lab = '\\(a =\\)'; A.zeige = { p: z(p), c: z(c), a: '?' };
            A.text = 'Rechtwinkliges Dreieck, rechter Winkel bei \\(C\\), Hypotenuse \\(c = ' + z(c) + '\\,\\text{cm}\\). Der Abschnitt an der Kathete \\(a\\) ist \\(p = ' + z(p) + '\\,\\text{cm}\\). Wie lang ist \\(a\\)?';
            A.falsch = [[b, 'Das ist \\(\\sqrt{q \\cdot c}\\), die andere Kathete. Zu \\(a\\) gehört der anliegende Abschnitt \\(p\\).', 'anliegend'], [p * c, 'Das ist \\(a^2\\). Zieh noch die Wurzel.', 'Wurzel'], [Math.sqrt(c * c - p * p), 'Das wäre Pythagoras mit \\(c\\) und \\(p\\) — die bilden kein rechtwinkliges Dreieck mit \\(a\\).', 'Pythagoras']]; }
          else if (art === 'abschnitt'){ var ag = r2(a); if (!gl(ag * ag, p * c)) return TYPEN['hoehensatz'].neu();
            A.werte = [ag, c]; A.soll = p; A.lab = '\\(p =\\)'; A.zeige = { a: z(ag), c: z(c), p: '?' };
            A.text = 'Rechtwinkliges Dreieck, rechter Winkel bei \\(C\\): Hypotenuse \\(c = ' + z(c) + '\\,\\text{cm}\\), Kathete \\(a = ' + z(ag) + '\\,\\text{cm}\\). Wie lang ist der Abschnitt \\(p\\) an \\(a\\)?';
            A.falsch = [[c - p, 'Das ist \\(q\\), der andere Abschnitt. Kathetensatz: \\(a^2 = p \\cdot c\\).', 'andere'], [ag / c, 'Kathetensatz: \\(a^2 = p \\cdot c\\), also \\(p = \\tfrac{a^2}{c}\\) — \\(a\\) im Quadrat.', 'Quadrat'], [ag * ag, 'Noch durch \\(c\\) teilen: \\(p = \\tfrac{a^2}{c}\\).', 'teilen']]; }
          else { var hg = r2(h); if (!gl(hg * hg, p * q)) return TYPEN['hoehensatz'].neu();
            A.werte = [hg, p, 'q']; A.soll = q; A.lab = '\\(q =\\)'; A.zeige = { h: z(hg), p: z(p), q: '?' };
            A.text = 'Rechtwinkliges Dreieck, rechter Winkel bei \\(C\\): Höhe \\(h = ' + z(hg) + '\\,\\text{cm}\\), Abschnitt \\(p = ' + z(p) + '\\,\\text{cm}\\). Wie lang ist der andere Abschnitt \\(q\\)?';
            A.falsch = [[hg / p, 'Höhensatz: \\(h^2 = p \\cdot q\\), also \\(q = \\tfrac{h^2}{p}\\) — \\(h\\) im Quadrat.', 'Quadrat'], [hg * hg * p, 'Durch \\(p\\) teilen, nicht multiplizieren.', 'teilen'], [hg - p, 'Nicht subtrahieren: \\(h^2 = p \\cdot q\\).', 'Differenz']]; }
          return A; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        zeichne: function(svg, A){
          // Hypotenuse AB waagrecht: A(0|0) links, B(c|0) rechts, H(q|0), C(q|h); q liegt an A (an b), p an B (an a)
          var c = A.c, q = A.q, h = Math.sqrt(A.p * A.q), C = [q, h], H = [q, 0];
          var F = Flaeche(svg, fensterUm([[0, 0], [c, 0], C], 0.9, 240, 140, (A.zeige || {}).c ? 22 : 10));
          F.vieleck([[0, 0], [c, 0], C], 'figur'); F.strecke(C, H, 'hilfe'); F.rechts(H, [1, 0], [0, 1], 'hilfe');
          F.rechts(C, [-q, -h], [A.p, -h], '');
          eckenText(F, [[0, 0], [c, 0], C], ['A', 'B', 'C'], 'ecke klein', 9); F.text(H, 'H', 'ecke klein', 0, 12);
          var Z = A.zeige || {};
          F.text([q / 2, 0], 'q' + (Z.q ? ' = ' + Z.q : ''), 'mass', 0, 11); F.text([q + A.p / 2, 0], 'p' + (Z.p ? ' = ' + Z.p : ''), 'mass', 0, 11);
          F.text([q, h / 2], 'h' + (Z.h ? ' = ' + Z.h : ''), 'mass', 4, 4, 'start');
          seitenText(F, [0, 0], C, 'b' + (Z.b ? ' = ' + Z.b : ''), 'mass', [c, 0], 9); seitenText(F, [c, 0], C, 'a' + (Z.a ? ' = ' + Z.a : ''), 'mass', [0, 0], 9);
          if (Z.c) F.text([c / 2, 0], 'c = ' + Z.c, 'mass', 0, 23);
        },
        pruefen: function(A, e){ return einfach(A, e, A.art === 'h' || A.art === 'q' ? 'Höhensatz: \\(h^2 = p \\cdot q\\).' : 'Kathetensatz: \\(a^2 = p \\cdot c\\) (\\(p\\) ist der Abschnitt an \\(a\\)).'); },
        loesung: function(A){ return A.art === 'h' ? 'h = \\sqrt{' + z(A.p) + ' \\cdot ' + z(A.q) + '} \\approx ' + z(A.soll) : A.art === 'kathete' ? 'a = \\sqrt{' + z(A.p) + ' \\cdot ' + z(A.c) + '} \\approx ' + z(A.soll)
          : A.art === 'abschnitt' ? 'p = \\tfrac{' + z(A.werte[0]) + '^2}{' + z(A.c) + '} = ' + z(A.soll) : 'q = \\tfrac{' + z(A.werte[0]) + '^2}{' + z(A.p) + '} = ' + z(A.soll); } }
    };

    /* Figur der Strahlensatz-Übungen: S(0|0), erster Strahl waagrecht, zweiter unter A.th; massstäblich. */
    function strahlenBild(svg, A, lab){
      var th = grad(A.th), v = [Math.cos(th), Math.sin(th)], k = A.k, S = [0, 0], Ap = [A.sa, 0], Bp = [A.sb * v[0], A.sb * v[1]];
      var A2 = [k * A.sa, 0], B2 = [k * A.sb * v[0], k * A.sb * v[1]];
      var F = Flaeche(svg, fensterUm([S, Ap, Bp, A2, B2], 0.9, 280, 170, lab.sa2 ? 20 : 0));
      F.gerade(S, [1, 0], 'strahl'); F.gerade(S, v, 'strahl');
      F.strecke(Ap, Bp, 'figur-linie'); F.strecke(A2, B2, 'bild-linie');
      [[S, 'S'], [Ap, 'A'], [A2, 'A′']].forEach(function(q){ F.punkt(q[0]); F.text(q[0], q[1], 'ecke klein', 0, 12); });
      F.punkt(Bp); F.text(Bp, 'B', 'ecke klein', -7, -4); F.punkt(B2); F.text(B2, 'B′', 'ecke klein', k < 0 ? 8 : -8, k < 0 ? 9 : -4);
      // Teilstücke nur mit der Zahl, ganze Strecken ab S mit Namen (sonst wäre unklar, ob SA′ oder AA′ gemeint ist)
      if (lab.sa) F.text(mitte(S, Ap), lab.sa, 'mass', 0, -4);
      if (lab.aa) F.text(mitte(Ap, A2), lab.aa, 'mass', 0, -4);
      if (lab.sa2) F.text(mitte(S, A2), 'SA′ = ' + lab.sa2, 'mass', 0, 21);
      if (lab.sb) seitenText(F, S, Bp, lab.sb, 'mass', Ap, 7);
      if (lab.sb2) seitenText(F, S, B2, 'SB′ = ' + lab.sb2, 'mass', [-Ap[0], -Ap[1]], 8);   // innen, SB steht aussen
      if (lab.bb) seitenText(F, Bp, B2, lab.bb, 'mass', A2, 7);
      if (lab.ab) seitenText(F, Ap, Bp, lab.ab, 'mass', S, 7);
      if (lab.ab2) seitenText(F, A2, B2, lab.ab2, 'mass', S, 7);
    }
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
        setzen(auf); setzen(ein);
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
       Einträge: ["v", [[x,y],…], cls] Vieleck · ["s", [x,y], [x,y], cls] Strecke · ["t", [x,y], "Text", cls, dx, dy, anker] ·
       ["p", [x,y]] Punkt · ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel · ["w", Scheitel, [x,y], [x,y], "Text"] Winkelbogen
       von der Richtung zum ersten zum zweiten Punkt (Eintrag 6: Anzahl Bögen) · ["g", [x,y], [x,y], cls] ganze Gerade.
       data-karo="ja" zeichnet das Karo, data-achsen="ja" dazu die Achsen mit Pfeil, Namen und Zahlen (je 2). ---------- */
  document.querySelectorAll('svg.geo-mini[data-fig]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-1,9,-1').split(',').map(Number), b = +(svg.dataset.breite || 220), h = +(svg.dataset.hoehe || 150);
    var F = Flaeche(svg, { w: b, h: h, x0: fe[0], x1: fe[1], y0: fe[2], karo: svg.dataset.karo === 'ja' ? 1 : false, achsen: svg.dataset.achsen === 'ja' ? { teil: 2 } : null });
    JSON.parse(svg.dataset.fig).forEach(function(e){
      var t = e[0];
      if (t === 'v') F.vieleck(e[1], e[2] || 'figur');
      else if (t === 's') F.strecke(e[1], e[2], e[3] || 'hilfe');
      else if (t === 't') F.text(e[1], e[2], e[3] || 'mass', e[4], e[5], e[6]);
      else if (t === 'p') F.punkt(e[1], e[2]);
      else if (t === 'g') F.gerade(e[1], e[2], e[3] || 'strahl');
      else if (t === 'r') F.rechts(e[1], e[2], e[3], '');
      else if (t === 'w') winkelMarke(F, e[1], e[2], e[3], e[5] || 20, 'winkelbogen', e[4], 'winkel klein', e[6]);
    });
    svg.setAttribute('role', 'img');
  });
})();
</script>
