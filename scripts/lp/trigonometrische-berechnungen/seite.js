<script>
/* Leitprogramm Trigonometrische Berechnungen — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit
   Rückmeldung, Figuren zu den Aufgaben. Gerüst (Flaeche, Leiste, arbeitsbereich, Übungsrahmen) wie im
   Leitprogramm Planimetrie (scripts/lp/planimetrie/seite.js), Inhalte neu.
   Notation wie auf der Themenseite 5.3: rechtwinkliges Dreieck mit dem rechten Winkel bei C, der betrachtete
   Winkel heisst x, die Seiten GK, AK, H; im allgemeinen Dreieck a gegenüber A, α bei A; Arcusfunktionen
   arcsin, arccos, arctan (Rechner: sin⁻¹, cos⁻¹, tan⁻¹). Winkel in Grad (DEG).
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Figur · orange = betrachteter Winkel, gegebene Stücke,
   Hilfslinie · grün = gesuchte Grösse, Ergebnis · rot = Fehler. Die Animation der Themenseite färbt die
   Gegenkathete rot; hier ist Rot für Fehler reserviert. Dezimalpunkt; gerundet mit «≈». */
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
        el(gr, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': 'k-treffer' });
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
      inp.addEventListener('input', function(){ bewegt[inp.dataset.p] = true; zeichnen(); });
    });
    function werte(){
      var w = { bewegt: bewegt };
      for (var k in regler){ w[k] = +regler[k].value; var sv = regler[k].parentNode.querySelector('.sl-val'); if (sv) sv.textContent = z(w[k]) + (regler[k].dataset.einheit || ''); }
      return w;
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

  /* ---------- Rechtwinkliges Dreieck der Kapitel 1 und 2 ----------
     Wie die Animation «Definition» der Themenseite: rechter Winkel bei C unten links, A unten rechts, B oben.
     Seiten a = BC (senkrecht), b = CA (waagrecht), c = AB (Hypotenuse). Liegt x bei A, ist a die Gegen- und
     b die Ankathete; liegt x bei B, tauschen sie die Rollen. */
  function rwDreieck(F, a, b, o){
    var C = [0, 0], A = [b, 0], B = [0, a];
    F.vieleck([A, B, C], 'figur');
    F.rechts(C, [1, 0], [0, 1], '');
    if (o.beiB) winkelMarke(F, B, C, A, 30, 'winkelbogen', 'x'); else winkelMarke(F, A, B, C, 30, 'winkelbogen', 'x');
    var seite = { a: [B, C], b: [C, A], c: [A, B] };
    (o.hervor || []).forEach(function(h){ F.strecke(seite[h[0]][0], seite[h[0]][1], h[1]); });
    [[A, 'A', 9, 15], [B, 'B', -10, -4], [C, 'C', -10, 15]].forEach(function(p){ F.punkt(p[0]); F.text(p[0], p[1], 'ecke', p[2], p[3]); });
    var la = o.lab || {};
    F.text(mitte(B, C), la.a || 'a', 'seite' + (la.a ? ' mass' : ''), -8, 4, 'end');
    F.text(mitte(C, A), la.b || 'b', 'seite' + (la.b ? ' mass' : ''), 0, 16);
    F.text(mitte(A, B), la.c || 'c', 'seite' + (la.c ? ' mass' : ''), 8, -6, 'start');
    return { A: A, B: B, C: C };
  }
  function kandidatenSeiten(F, P, k, ids){   // die drei Seiten als Kandidaten: ids = { a: 'gk', b: 'ak', c: 'h' }
    F.kandidat(ids.a, P.B, P.C, k.wahl); F.kandidat(ids.b, P.C, P.A, k.wahl); F.kandidat(ids.c, P.A, P.B, k.wahl);
  }

  /* ---------- Kapitel 1: Sinus, Cosinus, Tangens ----------
     Unterschied zur Animation «Definition» der Themenseite: Dort ist H fest 10, man schaltet die Funktion um.
     Hier ändert der Regler H die Grösse bei festem x (Ähnlichkeit wie in Anim 1), und die Leiste lässt die
     Seiten antippen und berechnen. Startwert x = 35°, H = 10 cm wie im Einführungsclip und auf der Themenseite. */
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 312, x0: -1.8, x1: 11.5, y0: -1.5 },
    zeichnen: function(F, w, k){
      var A = k.aufgabe || {}, beiB = !!A.beiB, x = w.x, H = w.H;
      var gk = H * sinG(x), ak = H * cosG(x), a = beiB ? ak : gk, b = beiB ? gk : ak;
      var lab = {};
      if (A.frage){ lab = A.lab || {}; }
      var P = rwDreieck(F, a, b, { beiB: beiB, lab: lab, hervor: A.hervor });
      if (k.wahl){ kandidatenSeiten(F, P, k, beiB ? { a: 'ak', b: 'gk', c: 'h' } : { a: 'gk', b: 'ak', c: 'h' }); }
      if (A.wahl && w.richtig){ var s_ = A.wahl.richtig, seite = beiB ? { ak: 'a', gk: 'b', h: 'c' }[s_] : { gk: 'a', ak: 'b', h: 'c' }[s_];
        var pp = { a: [P.B, P.C], b: [P.C, P.A], c: [P.A, P.B] }[seite]; F.strecke(pp[0], pp[1], 'hilfe'); }
      if (A.frage) return '\\(x = ' + z(x) + '°\\); ' + A.gegeben + '; gesucht: ' + A.gesucht;
      if (A.wahl) return '\\(x = ' + z(x) + '°\\) liegt bei \\(' + (beiB ? 'B' : 'A') + '\\)';
      return '\\(x = ' + z(x) + '°\\); \\(H = ' + z(H) + '\\,\\text{cm}\\); \\(GK ' + zz(gk) + '\\); \\(AK ' + zz(ak) + '\\)<br>'
        + '\\(\\sin x = \\tfrac{GK}{H} ' + zz(gk / H, 3) + '\\); \\(\\cos x = \\tfrac{AK}{H} ' + zz(ak / H, 3) + '\\); \\(\\tan x = \\tfrac{GK}{AK} ' + zz(gk / ak, 3) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Ändere mit \\(H\\) die Grösse des Dreiecks, \\(x\\) bleibt. Welche Zahlen in der Zeile bleiben gleich?', probe: { H: 6 }, ziel: function(w){ return w.bewegt.H; } },
      { text: 'Tipp die Gegenkathete von \\(x\\) an.', setup: function(s){ s.sperre('x', 'H'); },
        wahl: { richtig: 'gk', gut: 'Die Gegenkathete liegt dem Winkel \\(x\\) gegenüber.', rueck: {
          ak: 'Das ist die Ankathete: Sie liegt am Winkel \\(x\\) an.',
          h: 'Das ist die Hypotenuse: Sie liegt dem rechten Winkel gegenüber.' } } },
      { text: 'Jetzt liegt \\(x\\) bei \\(B\\). Tipp die Gegenkathete von \\(x\\) an.', beiB: true, setup: function(s){ s.sperre('x', 'H'); },
        wahl: { richtig: 'gk', gut: 'Vom Winkel \\(x\\) bei \\(B\\) aus gesehen liegt jetzt die untere Kathete gegenüber.', rueck: {
          ak: 'Diese Kathete war die Gegenkathete, als \\(x\\) bei \\(A\\) lag. Jetzt liegt sie am Winkel \\(x\\) an.',
          h: 'Das ist die Hypotenuse: Sie liegt dem rechten Winkel gegenüber.' } } },
      { text: 'Stell \\(x\\) so ein, dass Gegenkathete und Ankathete gleich lang sind.', probe: { x: 45 }, ziel: function(w){ return w.x === 45; } },
      { text: 'Stell \\(x\\) so ein, dass \\(\\tfrac{GK}{H} \\approx 0.766\\) ist.', probe: { x: 50 }, ziel: function(w){ return w.x === 50; } },
      { text: '\\(x = 40°\\), \\(H = 8\\,\\text{cm}\\). Berechne die Gegenkathete.', setup: function(s){ s.setze({ x: 40, H: 8 }); s.sperre('x', 'H'); },
        lab: { c: 'H = 8 cm', a: '?' }, gegeben: '\\(H = 8\\,\\text{cm}\\)', gesucht: '\\(GK\\)',
        frage: [{ name: 'GK', label: '\\(GK \\approx\\)', einheit: 'cm', soll: 5.14, fehler: [[6.13, 'Das ist die Ankathete. Zur Gegenkathete und der Hypotenuse gehört der Sinus.'], [12.45, 'Die Gegenkathete ist kürzer als die Hypotenuse. Aus \\(\\sin x = \\tfrac{GK}{H}\\) folgt \\(GK = H \\cdot \\sin x\\).'], [5.96, RAD]], tipp: '\\(\\sin x = \\tfrac{GK}{H}\\), also \\(GK = H \\cdot \\sin x\\).' }] },
      { text: '\\(x = 55°\\), Ankathete \\(AK = 4\\,\\text{cm}\\). Wie lang ist die Hypotenuse?', fest: { x: 55, H: 4 / Math.cos(55 * PI / 180) }, setup: function(s){ s.sperre('x', 'H'); },
        lab: { b: 'AK = 4 cm', c: '?' }, gegeben: '\\(AK = 4\\,\\text{cm}\\)', gesucht: '\\(H\\)',
        frage: [{ name: 'H', label: '\\(H \\approx\\)', einheit: 'cm', soll: 6.97, fehler: [[2.29, 'Die Hypotenuse ist die längste Seite. Aus \\(\\cos x = \\tfrac{AK}{H}\\) folgt \\(H = \\tfrac{AK}{\\cos x}\\) — teilen, nicht multiplizieren.'], [4.88, 'Mit \\(AK\\) und \\(H\\) gehört der Cosinus dazu, nicht der Sinus.'], [180.78, RAD]], tipp: '\\(\\cos x = \\tfrac{AK}{H}\\), nach \\(H\\) umstellen.' }] }
    ]
  });

  /* ---------- Kapitel 2: Winkel berechnen ----------
     Unterschied zur Themenseite (dort keine Animation zu den Arcusfunktionen): Die Katheten sind die Regler,
     die Zeile zeigt das Verhältnis und den Winkel, den tan⁻¹ daraus macht. Startwert GK = 5, AK = 12 wie im
     Einführungsclip (Themenseite, Aufgabe A3a). */
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 220, x0: -1.8, x1: 13.5, y0: -1.5 },
    zeichnen: function(F, w, k){
      var A = k.aufgabe || {}, gk = w.gk, ak = w.ak, x = atanG(gk / ak), H = Math.hypot(gk, ak);
      rwDreieck(F, gk, ak, { lab: A.lab || { a: 'GK = ' + z(gk), b: 'AK = ' + z(ak) } });
      if (A.frage) return A.gegeben + '; gesucht: \\(x\\)';
      return '\\(\\tan x = \\tfrac{GK}{AK} = \\tfrac{' + z(gk) + '}{' + z(ak) + '} ' + zz(gk / ak, 3) + '\\) (Steigung \\(' + zz(gk / ak * 100, 1) + '\\,\\%\\))<br>'
        + '\\(x = \\arctan\\tfrac{' + z(gk) + '}{' + z(ak) + '} ' + zz(x) + '°\\); \\(H ' + zz(H) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(GK\\) und \\(AK\\). Wann wird \\(x\\) grösser?', probe: { gk: 7 }, ziel: function(w){ return w.bewegt.gk || w.bewegt.ak; } },
      { text: 'Stell ein Dreieck mit \\(x = 45°\\) ein.', probe: { gk: 6, ak: 6 }, ziel: function(w){ return w.gk === w.ak; } },
      { text: 'Stell eine Steigung von \\(25\\,\\%\\) ein: \\(\\tfrac{GK}{AK} = 0.25\\).', probe: { gk: 2, ak: 8 }, ziel: function(w){ return Math.abs(w.gk / w.ak - 0.25) < 1e-9; } },
      { text: 'Stell ein Dreieck ein, in dem \\(x\\) grösser als \\(60°\\) ist.', probe: { gk: 8, ak: 4 }, ziel: function(w){ return atanG(w.gk / w.ak) > 60; } },
      { text: '\\(AK = 6\\,\\text{cm}\\), \\(H = 10\\,\\text{cm}\\). Wie gross ist \\(x\\)?', setup: function(s){ s.setze({ gk: 8, ak: 6 }); s.sperre('gk', 'ak'); },
        lab: { b: 'AK = 6', c: 'H = 10', a: ' ' }, gegeben: '\\(AK = 6\\,\\text{cm}\\), \\(H = 10\\,\\text{cm}\\)',
        frage: [{ name: 'x', label: '\\(x \\approx\\)', einheit: '°', soll: 53.13, tol: 0.011, fehler: [[36.87, 'Das ist \\(\\arcsin 0.6\\) — der Winkel bei \\(B\\). Zu \\(AK\\) und \\(H\\) gehört der Cosinus: \\(x = \\arccos\\tfrac{AK}{H}\\).'], [0.93, RAD], [0.6, 'Das ist \\(\\cos x\\), noch nicht der Winkel. Die Umkehrtaste \\(\\cos^{-1}\\) macht daraus den Winkel.'], [1.67, '\\(\\cos^{-1}\\) heisst Umkehrung, nicht Kehrwert.']], tipp: '\\(\\cos x = \\tfrac{AK}{H} = 0.6\\), dann \\(x = \\arccos 0.6\\).' }] },
      { text: '\\(GK = 3.5\\,\\text{cm}\\), \\(AK = 8\\,\\text{cm}\\). Wie gross ist \\(x\\)?', setup: function(s){ s.setze({ gk: 3.5, ak: 8 }); s.sperre('gk', 'ak'); },
        lab: { a: 'GK = 3.5', b: 'AK = 8' }, gegeben: '\\(GK = 3.5\\,\\text{cm}\\), \\(AK = 8\\,\\text{cm}\\)',
        frage: [{ name: 'x', label: '\\(x \\approx\\)', einheit: '°', soll: 23.63, tol: 0.011, fehler: [[66.37, 'Vertauscht: \\(\\arctan\\tfrac{AK}{GK}\\) gibt den Winkel bei \\(B\\). Für \\(x\\) gilt \\(\\tan x = \\tfrac{GK}{AK}\\).'], [0.44, 'Das ist \\(\\tan x\\), noch nicht der Winkel.'], [0.41, RAD], [25.94, 'Der Sinus braucht die Hypotenuse. Mit den zwei Katheten nimmst du den Tangens.']], tipp: '\\(\\tan x = \\tfrac{GK}{AK}\\), dann \\(\\arctan\\).' }] },
      { text: 'Eine Strasse steigt \\(12\\,\\%\\). Wie gross ist der Steigungswinkel?', fest: { gk: 1.2, ak: 10 }, setup: function(s){ s.sperre('gk', 'ak'); },
        lab: { a: ' ', b: ' ' }, gegeben: 'Steigung \\(12\\,\\% = \\tfrac{12}{100}\\)',
        frage: [{ name: 'x', label: '\\(x \\approx\\)', einheit: '°', soll: 6.84, tol: 0.011, fehler: [[85.24, '\\(12\\,\\%\\) heisst \\(\\tfrac{12}{100} = 0.12\\) — nicht \\(12\\).'], [12, 'Prozent sind keine Grad: Die Steigung ist \\(\\tan x = 0.12\\).'], [6.89, 'Die Steigung ist Höhe durch waagrechte Strecke, \\(\\tfrac{GK}{AK}\\) — also der Tangens.'], [0.12, 'Das ist \\(\\tan x\\) (oder der Winkel im Bogenmass). Gesucht ist \\(x\\) in Grad.']], tipp: 'Steigung \\(= \\tan x = 0.12\\).' }] }
    ]
  });

  /* ---------- Kapitel 3: Höhen und Distanzen ----------
     Wie die Animation «Baumhöhe» der Themenseite: Abstand d, Höhenwinkel α, die Augenhöhe vernachlässigt (ausser
     in Aufgabe 6, die sie nennt). Unterschied: Hier wird das rechtwinklige Dreieck eingezeichnet, die Seiten
     werden angetippt und die Höhe berechnet. Startwert d = 15 m, α = 52° wie auf der Themenseite und im Clip. */
  arbeitsbereich('sim3', {
    fenster: { w: 300, h: 369, x0: -3, x1: 23, y0: -2 },
    zeichnen: function(F, w, k){
      var A = k.aufgabe || {}, d = w.d, al = w.alpha, e = A.auge || 0, h = d * tanG(al);
      var P = [0, e], Fu = [d, e], T = [d, e + h];
      F.strecke([-3, 0], [23, 0], 'boden');
      F.strecke([d, 0], T, 'baum');
      F.kreis([d, e + h - 0.2], 1.0, 'krone');
      if (e){ F.strecke([0, 0], P, 'person'); F.strecke([0, e], [d, e], 'hilfe2'); F.text([0, e / 2], '1.6 m', 'mass', -6, 4, 'end'); }
      F.vieleck([P, Fu, T], 'figur');
      F.rechts(Fu, [-1, 0], [0, 1], '');
      winkelMarke(F, P, Fu, T, 34, 'winkelbogen', 'α');
      if (k.wahl){ F.kandidat('ak', P, Fu, k.wahl); F.kandidat('gk', Fu, T, k.wahl); F.kandidat('h', P, T, k.wahl); }
      if (A.wahl && w.richtig) F.strecke(P, Fu, 'hilfe');
      F.punkt(P); F.punkt(T);
      var lab = A.lab || { d: 'd = ' + z(d) + ' m', h: 'h' };
      F.text(mitte(P, Fu), lab.d, 'mass', 0, 15);
      F.text(mitte(Fu, T), lab.h, 'mass', 8, 4, 'start');
      if (A.frage) return A.gegeben + '; gesucht: ' + A.gesucht;
      if (A.wahl) return '\\(d = ' + z(d) + '\\,\\text{m}\\); \\(\\alpha = ' + z(al) + '°\\)';
      return '\\(d = ' + z(d) + '\\,\\text{m}\\); \\(\\alpha = ' + z(al) + '°\\); \\(h = d \\cdot \\tan\\alpha ' + zz(h) + '\\,\\text{m}\\); \\(\\tfrac{h}{d} ' + zz(h / d, 3) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(d\\) und \\(\\alpha\\). Wovon hängt die Höhe \\(h\\) ab?', probe: { d: 10 }, ziel: function(w){ return w.bewegt.d || w.bewegt.alpha; } },
      { text: 'Halbiere den Abstand \\(d\\), ohne \\(\\alpha\\) zu ändern. Was wird aus \\(h\\)?', probe: { d: 7.5 }, ziel: function(w){ return w.d === 7.5 && w.alpha === 52; } },
      { text: 'Stell \\(\\alpha\\) so ein, dass der Baum so hoch ist, wie du entfernt stehst.', probe: { alpha: 45 }, ziel: function(w){ return w.alpha === 45; } },
      { text: 'Tipp die Ankathete des Höhenwinkels \\(\\alpha\\) an.', setup: function(s){ s.sperre('d', 'alpha'); },
        wahl: { richtig: 'ak', gut: 'Der Abstand \\(d\\) am Boden liegt am Winkel \\(\\alpha\\) an.', rueck: {
          gk: 'Das ist der Baum: Er liegt dem Winkel \\(\\alpha\\) gegenüber — die Gegenkathete.',
          h: 'Das ist der Sehstrahl zur Spitze: Er liegt dem rechten Winkel gegenüber — die Hypotenuse.' } } },
      { text: '\\(d = 12\\,\\text{m}\\), \\(\\alpha = 38°\\). Wie hoch ist der Baum?', setup: function(s){ s.setze({ d: 12, alpha: 38 }); s.sperre('d', 'alpha'); },
        lab: { d: 'd = 12 m', h: 'h = ?' }, gegeben: '\\(d = 12\\,\\text{m}\\), \\(\\alpha = 38°\\)', gesucht: '\\(h\\)',
        frage: [{ name: 'h', label: '\\(h \\approx\\)', einheit: 'm', soll: 9.38, fehler: [[7.39, 'Der Sinus braucht die Hypotenuse — \\(d\\) ist aber die Ankathete. Mit \\(h\\) und \\(d\\): Tangens.'], [15.36, '\\(\\tan\\alpha = \\tfrac{h}{d}\\), also \\(h = d \\cdot \\tan\\alpha\\) — multiplizieren.'], [9.46, 'Mit Gegen- und Ankathete gehört der Tangens dazu, nicht der Cosinus.'], [3.72, RAD]], tipp: '\\(\\tan\\alpha = \\tfrac{h}{d}\\).' }] },
      { text: 'Augenhöhe \\(1.6\\,\\text{m}\\), \\(d = 18\\,\\text{m}\\), \\(\\alpha = 40°\\). Wie hoch ist der Baum?', auge: 1.6, setup: function(s){ s.setze({ d: 18, alpha: 40 }); s.sperre('d', 'alpha'); },
        lab: { d: 'd = 18 m', h: '?' }, gegeben: 'Augenhöhe \\(1.6\\,\\text{m}\\), \\(d = 18\\,\\text{m}\\), \\(\\alpha = 40°\\)', gesucht: 'Baumhöhe',
        frage: [{ name: 'h', label: 'Höhe \\(\\approx\\)', einheit: 'm', soll: 16.70, fehler: [[15.1, 'Das ist die Höhe über deinen Augen. Die Augenhöhe kommt dazu.'], [13.5, 'Die Augenhöhe wird addiert: Das Dreieck beginnt auf Augenhöhe, der Baum am Boden.']], tipp: 'Erst \\(18 \\cdot \\tan 40°\\), dann die Augenhöhe.' }] },
      { text: 'Der Baum ist \\(14\\,\\text{m}\\) hoch, du stehst \\(20\\,\\text{m}\\) entfernt. Unter welchem Höhenwinkel siehst du die Spitze?', fest: { d: 20, alpha: atanG(0.7) }, setup: function(s){ s.sperre('d', 'alpha'); },
        lab: { d: 'd = 20 m', h: 'h = 14 m' }, gegeben: '\\(h = 14\\,\\text{m}\\), \\(d = 20\\,\\text{m}\\)', gesucht: '\\(\\alpha\\)',
        frage: [{ name: 'a', label: '\\(\\alpha \\approx\\)', einheit: '°', soll: 34.99, tol: 0.011, fehler: [[55.01, 'Vertauscht: \\(\\tan\\alpha = \\tfrac{h}{d}\\), die Höhe steht oben.'], [0.7, 'Das ist \\(\\tan\\alpha\\), noch nicht der Winkel.'], [44.43, 'Der Sinus braucht die Hypotenuse (den Sehstrahl). Mit \\(h\\) und \\(d\\): Tangens.'], [0.61, RAD]], tipp: '\\(\\alpha = \\arctan\\tfrac{h}{d}\\).' }] }
    ]
  });

  /* ---------- Kapitel 4: Sinussatz und der Fall SSW ----------
     Wie die Animation «SSW» der Themenseite: α = 35° bei A, c = AB = 6 fest, a über den Regler (Kreis um B).
     Unterschied: Die Leiste lässt die Höhe antippen und die Winkel bei C mit dem Sinussatz berechnen.
     Startwert a = 4.5 wie auf der Themenseite und im Clip. Die Grenzfälle a = h und a = c der Themenseite
     (Knöpfe) gibt es hier nicht; a = h liegt nicht auf dem Raster, a = c gibt ein Dreieck. */
  var AL4 = 35, C4 = 6, H4 = C4 * sinG(AL4), T4 = C4 * cosG(AL4);
  function sswPunkte(a){
    if (a < H4 - 1e-9) return [];
    var q = Math.sqrt(Math.max(0, a * a - H4 * H4)), ts = [T4 - q, T4 + q].filter(function(t){ return t > 1e-9; });
    if (q < 1e-9) ts = [T4];
    // der ferne Schnittpunkt zuerst: C1 mit dem spitzen γ1, C2 mit dem stumpfen γ2 (wie im Clip)
    return ts.reverse().map(function(t){ return [t * cosG(AL4), t * sinG(AL4)]; });
  }
  arbeitsbereich('sim4', {
    fenster: { w: 320, h: 237, x0: -1.5, x1: 12, y0: -1.5 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, a = w.a, A = [0, 0], B = [C4, 0], Cs = sswPunkte(a);
      F.strahl(A, grad(AL4), 'strahl');
      F.kreis(B, a, 'kreisbogen');
      Cs.forEach(function(C, i){ F.vieleck([A, B, C], i === 0 ? 'figur' : 'figur zwei'); });
      var fuss = [T4 * cosG(AL4), T4 * sinG(AL4)];
      if (k.wahl){ var c1 = sswPunkte(a); F.kandidat('h', B, fuss, k.wahl); F.kandidat('a1', B, c1[0], k.wahl); F.kandidat('a2', B, c1[1], k.wahl); }
      if ((Au.wahl && w.richtig) || Au.zeigeH){ F.strecke(B, fuss, 'hilfe'); F.rechts(fuss, [-cosG(AL4), -sinG(AL4)], [sinG(AL4), -cosG(AL4)], 'hilfe'); F.text(mitte(B, fuss), 'h', 'hilfe', 6, 4, 'start'); }
      winkelMarke(F, A, B, [10, 10 * tanG(AL4)], 30, 'winkelbogen', '35°', 'winkel klein');
      F.punkt(A); F.punkt(B); F.text(A, 'A', 'ecke', -9, 14); F.text(B, 'B', 'ecke', 9, 14);
      F.text(mitte(A, B), 'c = 6', 'mass', 0, 15);
      Cs.forEach(function(C, i){ F.punkt(C); F.text(C, Cs.length > 1 ? 'C' + ['₁', '₂'][i] : 'C', 'ecke', -6, -8, 'end'); });
      var n = Cs.length, art = n === 0 ? 'kein Dreieck' : n === 1 ? 'ein Dreieck' : 'zwei Dreiecke';
      if (Au.frage) return '\\(\\alpha = 35°\\); \\(c = 6\\); \\(a = ' + z(a) + '\\); gesucht: ' + Au.gesucht;
      if (Au.wahl) return '\\(\\alpha = 35°\\); \\(c = 6\\); \\(a = ' + z(a) + '\\)';
      return '\\(\\alpha = 35°\\); \\(c = 6\\); \\(a = ' + z(a) + '\\); Höhe \\(h = c \\cdot \\sin\\alpha \\approx 3.44\\) — ' + art;
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(a\\). Wie oft trifft der Kreis um \\(B\\) den Schenkel von \\(\\alpha\\)?', probe: { a: 7 }, ziel: function(w){ return w.bewegt.a; } },
      { text: 'Tipp die Höhe \\(h\\) von \\(B\\) auf den Schenkel an — sie entscheidet über die Anzahl.', setup: function(s){ s.sperre('a'); },
        wahl: { richtig: 'h', gut: 'Das Lot von \\(B\\) auf den Schenkel: \\(h = c \\cdot \\sin\\alpha \\approx 3.44\\).', rueck: {
          a1: 'Das ist die Seite \\(a\\) zum Schnittpunkt \\(C_1\\). Sie steht nicht senkrecht auf dem Schenkel.',
          a2: 'Das ist die Seite \\(a\\) zum Schnittpunkt \\(C_2\\). Gesucht ist das Lot, der kürzeste Weg von \\(B\\) zum Schenkel.' } } },
      { text: 'Stell \\(a\\) so ein, dass es kein Dreieck gibt.', zeigeH: true, probe: { a: 3 }, ziel: function(w){ return w.a < H4; } },
      { text: 'Stell \\(a\\) so ein, dass es genau ein Dreieck gibt.', zeigeH: true, probe: { a: 7 }, ziel: function(w){ return w.a >= C4; } },
      { text: '\\(a = 5\\): Berechne beide möglichen Winkel \\(\\gamma\\) bei \\(C\\).', setup: function(s){ s.setze({ a: 5 }); s.sperre('a'); }, gesucht: '\\(\\gamma_1\\), \\(\\gamma_2\\)',
        frage: [{ name: 'g1', label: '\\(\\gamma_1 \\approx\\)', einheit: '° (spitz)', soll: 43.50, tol: 0.011, fehler: [[0.69, 'Das ist \\(\\sin\\gamma\\), noch nicht der Winkel.'], [0.76, RAD], [17.49, 'Sinussatz: \\(\\tfrac{\\sin\\gamma}{c} = \\tfrac{\\sin\\alpha}{a}\\) — die Seite \\(c\\) gehört zu \\(\\gamma\\), die Seite \\(a\\) zu \\(\\alpha\\).']], tipp: '\\(\\sin\\gamma = \\tfrac{c \\cdot \\sin\\alpha}{a}\\).' },
                { name: 'g2', label: '\\(\\gamma_2 \\approx\\)', einheit: '° (stumpf)', soll: 136.50, tol: 0.011, fehler: [[43.5, 'Das ist der spitze Winkel. Der zweite Schnittpunkt gibt den stumpfen: \\(180° - \\gamma_1\\).'], [46.5, 'Nicht \\(90° - \\gamma_1\\): Der stumpfe Winkel mit demselben Sinus ist \\(180° - \\gamma_1\\).']], tipp: '\\(\\gamma_2 = 180° - \\gamma_1\\).' }] },
      { text: '\\(a = 7\\): Berechne \\(\\gamma\\). Warum gibt es nur eine Lösung?', setup: function(s){ s.setze({ a: 7 }); s.sperre('a'); }, gesucht: '\\(\\gamma\\)',
        frage: [{ name: 'g', label: '\\(\\gamma \\approx\\)', einheit: '°', soll: 29.45, tol: 0.011, fehler: [[150.55, 'Der stumpfe Winkel geht hier nicht: \\(35° + 150.55°\\) wäre mehr als \\(180°\\).'], [0.49, 'Das ist \\(\\sin\\gamma\\), noch nicht der Winkel.'], [0.51, RAD]], tipp: '\\(\\sin\\gamma = \\tfrac{c \\cdot \\sin\\alpha}{a}\\).' }],
        loesung: 'Der stumpfe Kandidat \\(150.55°\\) hätte mit \\(\\alpha = 35°\\) zusammen mehr als \\(180°\\).' },
      { text: '\\(a = 7\\): Wie lang ist die Seite \\(b = AC\\)?', setup: function(s){ s.setze({ a: 7 }); s.sperre('a'); }, gesucht: '\\(b\\)',
        frage: [{ name: 'b', label: '\\(b \\approx\\)', einheit: '', soll: 11.01, fehler: [[6, 'Das ist \\(c\\). Zu \\(b\\) gehört der Gegenwinkel \\(\\beta = 180° - \\alpha - \\gamma\\).'], [3.82, 'Seite durch Sinus des Gegenwinkels: \\(\\tfrac{b}{\\sin\\beta} = \\tfrac{a}{\\sin\\alpha}\\), also \\(b = \\tfrac{a \\cdot \\sin\\beta}{\\sin\\alpha}\\).']], tipp: 'Zuerst \\(\\beta = 180° - 35° - \\gamma\\), dann \\(\\tfrac{b}{\\sin\\beta} = \\tfrac{a}{\\sin\\alpha}\\).' }] }
    ]
  });

  /* ---------- Kapitel 5: Cosinussatz und Dreiecksfläche ----------
     Wie die Animation «Cosinussatz» der Themenseite (Seiten b, c und der Zwischenwinkel α), dazu die Fläche wie in
     Anim 6. Unterschied: Die Leiste lässt die Höhe antippen und rechnen; die Zeile zeigt beide Formeln.
     Startwert b = 7, c = 10, α = 55° wie im Clip (Themenseite, Aufgabe A4b). */
  arbeitsbereich('sim5', {
    fenster: { w: 320, h: 186, x0: -8, x1: 11.5, y0: -1.6 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, b = w.b, c = w.c, al = w.alpha;
      var A = [0, 0], B = [c, 0], C = [b * cosG(al), b * sinG(al)], a2 = b * b + c * c - 2 * b * c * cosG(al), a = Math.sqrt(a2);
      var fuss = [C[0], 0];
      if (C[0] < 0 || C[0] > c) F.strecke(C[0] < 0 ? A : B, fuss, 'verlaengerung');
      F.vieleck([A, B, C], 'figur');
      winkelMarke(F, A, B, C, 26, 'winkelbogen', 'α');
      if (k.wahl){ F.kandidat('h', C, fuss, k.wahl); F.kandidat('b', A, C, k.wahl); F.kandidat('a', B, C, k.wahl); F.kandidat('s', C, [c / 2, 0], k.wahl); }
      if ((Au.wahl && w.richtig) || Au.zeigeH){ F.strecke(C, fuss, 'hilfe'); F.rechts(fuss, [0, 1], [C[0] < c / 2 ? 1 : -1, 0], 'hilfe'); }
      [[A, 'A', -8, 14], [B, 'B', 8, 14], [C, 'C', 0, -9]].forEach(function(p){ F.punkt(p[0]); F.text(p[0], p[1], 'ecke', p[2], p[3]); });
      var lab = Au.lab || { b: 'b = ' + z(b), c: 'c = ' + z(c), a: 'a' };
      F.text(mitte(A, B), lab.c, 'mass', 0, 15);
      F.text(mitte(A, C), lab.b, 'mass', -7, -3, 'end');
      F.text(mitte(B, C), lab.a, 'mass', 7, -3, 'start');
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      if (Au.wahl) return '\\(b = ' + z(b) + '\\); \\(c = ' + z(c) + '\\); \\(\\alpha = ' + z(al) + '°\\)';
      return '\\(a^2 = ' + z(b * b) + ' + ' + z(c * c) + ' - ' + z(2 * b * c) + ' \\cdot \\cos ' + z(al) + '° ' + zz(a2) + '\\)<br>'
        + '\\(a ' + zz(a) + '\\); Korrekturglied \\(-2bc\\cos\\alpha ' + zz(-2 * b * c * cosG(al)) + '\\)<br>'
        + 'Fläche \\(A = \\tfrac{b \\cdot c}{2} \\sin\\alpha ' + zz(b * c / 2 * sinG(al)) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh \\(\\alpha\\) über \\(90°\\) hinaus. Was macht das Korrekturglied \\(-2bc\\cos\\alpha\\)?', probe: { alpha: 120 }, ziel: function(w){ return w.bewegt.alpha && w.alpha > 90; } },
      { text: 'Stell \\(\\alpha = 90°\\) ein: Was bleibt vom Cosinussatz?', probe: { alpha: 90 }, ziel: function(w){ return w.alpha === 90; } },
      { text: 'Tipp die Höhe auf die Seite \\(c\\) an — sie gehört zur Fläche.', setup: function(s){ s.setze({ alpha: 70 }); s.sperre('b', 'c', 'alpha'); },
        wahl: { richtig: 'h', gut: 'Das Lot von \\(C\\) auf \\(c\\): \\(h = b \\cdot \\sin\\alpha\\).', rueck: {
          b: 'Das ist die Seite \\(b\\). Sie steht schräg auf \\(c\\); die Höhe steht senkrecht.',
          a: 'Das ist die Seite \\(a\\). Gesucht ist das Lot von \\(C\\) auf \\(c\\).',
          s: 'Diese Linie endet in der Mitte von \\(c\\) — die Seitenhalbierende. Die Höhe steht senkrecht auf \\(c\\).' } } },
      { text: '\\(b = 5\\), \\(c = 8\\), \\(\\alpha = 70°\\). Berechne \\(a\\).', setup: function(s){ s.setze({ b: 5, c: 8, alpha: 70 }); s.sperre('b', 'c', 'alpha'); },
        lab: { b: 'b = 5', c: 'c = 8', a: 'a = ?' }, gegeben: '\\(b = 5\\), \\(c = 8\\), \\(\\alpha = 70°\\)', gesucht: '\\(a\\)',
        frage: [{ name: 'a', label: '\\(a \\approx\\)', einheit: '', soll: 7.85, fehler: [[9.43, 'Das ist \\(\\sqrt{b^2 + c^2}\\) — das Korrekturglied \\(-2bc\\cos\\alpha\\) fehlt.'], [10.79, 'Vorzeichen: Das Korrekturglied wird abgezogen, \\(a^2 = b^2 + c^2 - 2bc\\cos\\alpha\\).'], [61.64, 'Das ist \\(a^2\\). Zieh noch die Wurzel.'], [6.19, RAD]], tipp: '\\(a^2 = b^2 + c^2 - 2bc\\cos\\alpha\\), dann die Wurzel.' }] },
      { text: 'Drei Seiten: \\(a = 8\\), \\(b = 5\\), \\(c = 7\\). Wie gross ist \\(\\alpha\\)?', fest: { b: 5, c: 7, alpha: acosG(1 / 7) }, setup: function(s){ s.sperre('b', 'c', 'alpha'); },
        lab: { b: 'b = 5', c: 'c = 7', a: 'a = 8' }, gegeben: '\\(a = 8\\), \\(b = 5\\), \\(c = 7\\)', gesucht: '\\(\\alpha\\)',
        frage: [{ name: 'al', label: '\\(\\alpha \\approx\\)', einheit: '°', soll: 81.79, tol: 0.011, fehler: [[0.14, 'Das ist \\(\\cos\\alpha\\), noch nicht der Winkel.'], [1.43, RAD], [60, 'Das ist der Winkel gegenüber \\(c\\). Für \\(\\alpha\\) steht \\(a^2\\) allein: \\(\\cos\\alpha = \\tfrac{b^2 + c^2 - a^2}{2bc}\\).'], [38.21, 'Das ist der Winkel gegenüber \\(b\\). Für \\(\\alpha\\) steht \\(a^2\\) allein.']], tipp: '\\(\\cos\\alpha = \\tfrac{b^2 + c^2 - a^2}{2bc}\\).' }] },
      { text: '\\(b = 5\\), \\(c = 8\\), \\(\\alpha = 70°\\). Wie gross ist die Fläche?', zeigeH: true, setup: function(s){ s.setze({ b: 5, c: 8, alpha: 70 }); s.sperre('b', 'c', 'alpha'); },
        lab: { b: 'b = 5', c: 'c = 8', a: ' ' }, gegeben: '\\(b = 5\\), \\(c = 8\\), \\(\\alpha = 70°\\)', gesucht: 'Fläche',
        frage: [{ name: 'A', label: '\\(A \\approx\\)', einheit: '', soll: 18.79, fehler: [[20, 'Das wäre ein rechter Winkel. Die Höhe ist \\(h = b \\cdot \\sin\\alpha\\), nicht \\(b\\).'], [37.59, 'Das \\(\\tfrac{1}{2}\\) fehlt: \\(A = \\tfrac{b \\cdot c}{2}\\sin\\alpha\\).'], [15.48, RAD], [6.84, 'Die Höhe kommt mit dem Sinus, nicht mit dem Cosinus.']], tipp: '\\(A = \\tfrac{b \\cdot c}{2} \\sin\\alpha\\).' }] },
      { text: '\\(b = 4\\), \\(c = 6\\), \\(\\alpha = 120°\\). Wie lang ist \\(a\\)?', setup: function(s){ s.setze({ b: 4, c: 6, alpha: 120 }); s.sperre('b', 'c', 'alpha'); },
        lab: { b: 'b = 4', c: 'c = 6', a: 'a = ?' }, gegeben: '\\(b = 4\\), \\(c = 6\\), \\(\\alpha = 120°\\)', gesucht: '\\(a\\)',
        frage: [{ name: 'a', label: '\\(a \\approx\\)', einheit: '', soll: 8.72, fehler: [[5.29, 'Bei einem stumpfen Winkel ist \\(\\cos\\alpha\\) negativ: Minus mal minus gibt plus, \\(a\\) wird länger.'], [7.21, 'Das ist \\(\\sqrt{b^2 + c^2}\\) — das Korrekturglied fehlt.']], tipp: '\\(\\cos 120° = -0.5\\); \\(a^2 = 16 + 36 - 48 \\cdot (-0.5)\\).' }] }
    ]
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function r2(v){ return Math.round(v * 100) / 100; }
    function tz(v){ return String(v).replace('-', '−'); }
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche ·
       Kapitelaufgaben · Gesamttest. Je Typ ein eigener Schlüssel (Typkürzel | Winkel | Seite …). */
    var SPERRE = [
      // seite-rw: sr|Winkel|gegeben|Länge|gesucht (gegeben/gesucht: gk, ak, h)
      'sr|35|h|10|gk', 'sr|35|h|10|ak', 'sr|40|h|8|gk', 'sr|55|ak|4|h', 'sr|28|h|15|gk', 'sr|28|h|15|ak', 'sr|62|ak|9|h', 'sr|62|ak|9|gk',
      'sr|50|gk|6|h', 'sr|40|h|12|gk', 'sr|25|gk|6|h', 'sr|36|h|11|ak', 'sr|36|h|11|gk', 'sr|70|h|6|gk', 'sr|70|h|6|ak', 'sr|40|ak|8|h', 'sr|40|ak|8|gk', 'sr|35|h|10|ak',
      // winkel-rw: wr|gegeben1|Wert1|gegeben2|Wert2 (Seiten in fester Reihenfolge gk, ak, h)
      'wr|gk|5|ak|12', 'wr|ak|6|h|10', 'wr|gk|3.5|ak|8', 'wr|gk|9|ak|14', 'wr|gk|4|h|9.5', 'wr|gk|3|ak|7', 'wr|gk|4|ak|7', 'wr|ak|4|h|9', 'wr|gk|3.2|ak|5', 'wr|gk|7|ak|7',
      // steigung: st|Prozent bzw. st|w|Winkel
      'st|12', 'st|25', 'st|37.5', 'st|8', 'st|20',
      // hoehe: hw|d|Winkel|Auge, hw|w|h|d
      'hw|15|52|0', 'hw|12|38|0', 'hw|18|40|1.6', 'hw|w|14|20', 'hw|30|20|0',
      // leiter/tiefe: lt|Art|Länge|Winkel
      'lt|leiter|6|70', 'lt|leiter|5|70', 'lt|tiefe|45|12', 'lt|tiefe|32|24', 'lt|tiefe|32|15', 'lt|tiefe|60|18',
      // sinussatz: ss|α|β|gegebene Seite|Wert|gesuchte Seite
      'ss|42|71|c|9|a', 'ss|42|71|c|9|b', 'ss|58|75|c|120|b', 'ss|58|75|c|120|a', 'ss|40|65|a|8|b', 'ss|40|65|a|8|c',
      // ssw: sw|α|c|a
      'sw|35|6|4.5', 'sw|35|6|2.5', 'sw|42|10|8', 'sw|35|6|5', 'sw|35|6|7', 'sw|34|9|6', 'sw|40|10|7',
      // cosinussatz: cs|sws|b|c|α bzw. cs|sss|a|b|c
      'cs|sws|7|10|55', 'cs|sws|5|8|70', 'cs|sws|4|6|120', 'cs|sss|8|5|7', 'cs|sss|7|9|12', 'cs|sws|4.2|3.5|48', 'cs|sws|3|5|60', 'cs|sws|60|85|125',
      // flaeche: fl|p|q|φ
      'fl|7|10|55', 'fl|5|8|70', 'fl|32|45|110', 'fl|6|4|30', 'fl|60|85|125'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function feld(A, f, e, soll, tipp, fehler, tol){
      if (stimmt(e[f], soll, tol)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (!stimmt(fehler[j][0], soll, tol) && stimmt(e[f], fehler[j][0], tol)) return fehler[j][1];
      return nah(e[f], soll, tol) ? RUNDEN : tipp;
    }
    /* Gezielte Fehler für das Prüfwerkzeug: nur Werte, die sich vom Sollwert unterscheiden. */
    function fehlerListe(A, f, liste, tol){
      var aus = [];
      var gesehen = [];   // gleiche Fehlwerte zweier Fehlerarten: nur die erste zählt (so prüft auch pruefen)
      liste.forEach(function(x){ if (isFinite(x[0]) && !stimmt(r2(x[0]), A.soll, tol) && Math.abs(r2(x[0]) - A.soll) > 0.07
          && !gesehen.some(function(g){ return stimmt(r2(x[0]), g, tol); })) { gesehen.push(r2(x[0])); var o = {}; o[f] = String(r2(x[0])); aus.push([o, x[2] || null]); } });
      return aus;
    }
    var NAME = { gk: 'Gegenkathete', ak: 'Ankathete', h: 'Hypotenuse' };
    var KURZ = { gk: 'GK', ak: 'AK', h: 'H' };
    /* rechtwinkliges Dreieck aus Winkel x und Hypotenuse 1 */
    function seiten(x){ return { gk: sinG(x), ak: cosG(x), h: 1 }; }
    function seitenRad(x){ return { gk: Math.sin(x), ak: Math.cos(x), h: 1 }; }

    var TYPEN = {
      /* ── Kapitel 1 ── */
      /* Seiten benennen am gedrehten Dreieck: Der rechte Winkel liegt bei V0, gefragt ist eine Seite vom Winkel bei
         V1 aus. Buchstaben und Lage wechseln. */
      'benennen': { felder: ['s'], muster: 'Seite {s:–}',
        neu: function(){
          var namen = zufall([['A', 'B', 'C'], ['P', 'Q', 'R'], ['D', 'E', 'F'], ['K', 'L', 'M']]).slice();
          for (var i = 2; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = namen[i]; namen[i] = namen[j]; namen[j] = t; }
          var V0 = namen[0], V1 = namen[1], V2 = namen[2], rolle = zufall(['gk', 'ak', 'h']);
          function seite(p, q){ return [p, q].sort().join(''); }
          var richtig = { gk: seite(V0, V2), ak: seite(V0, V1), h: seite(V1, V2) }[rolle];
          var optionen = [seite(V0, V1), seite(V0, V2), seite(V1, V2)].sort();
          return { V0: V0, V1: V1, V2: V2, rolle: rolle, soll: richtig, optionen: optionen, falschAk: seite(V0, V1), falschGk: seite(V0, V2), falschH: seite(V1, V2),
            p: zufall([4, 4.5, 5]), q: zufall([2.5, 3, 3.5]), dreh: zufall([0, 30, 90, 150, 200, 250, 320]), spiegel: Math.random() < 0.5,
            text: 'Im Bild liegt der rechte Winkel bei \\(' + V0 + '\\). Welche Seite ist die <b>' + NAME[rolle] + '</b> des markierten Winkels bei \\(' + V1 + '\\)?' }; },
        vorbereiten: function(box, A){
          var s = box.querySelector('select[data-f="s"]'); if (!s) return;
          s.innerHTML = '<option value="">?</option>' + A.optionen.map(function(o){ return '<option>' + o + '</option>'; }).join('');
        },
        eingabe: function(A){ return { s: A.soll }; },
        zeichne: function(svg, A){
          var sy = A.spiegel ? -1 : 1, cx = A.p / 3, cy = sy * A.q / 3;
          var F = Flaeche(svg, { w: 240, h: 210, x0: cx - 5, x1: cx + 5, y0: cy - 4.375, drehpunkt: [cx, cy], karo: false });
          F.drehen(grad(A.dreh));
          var P0 = [0, 0], P1 = [A.p, 0], P2 = [0, sy * A.q];
          F.vieleck([P0, P1, P2], 'figur');
          F.rechts(P0, [1, 0], [0, sy], '');
          winkelMarke(F, P1, P0, P2, 24, 'winkelbogen');
          [[P0, A.V0], [P1, A.V1], [P2, A.V2]].forEach(function(e){ var d = [e[0][0] - cx, e[0][1] - cy], n = Math.hypot(d[0], d[1]);
            F.punkt(e[0]); F.text([e[0][0] + d[0] / n * 0.7, e[0][1] + d[1] / n * 0.7], e[1], 'ecke', 0, 4); });
          F.drehen(0);
        },
        fehler: function(A){ var f = [];
          A.optionen.forEach(function(o){ if (o !== A.soll) f.push([{ s: o }, o === A.falschH ? 'rechten' : o === A.falschAk ? 'am Winkel an' : 'gegenüber']); });
          return f; },
        pruefen: function(A, e){
          if (e.s === A.soll) return null;
          if (e.s === A.falschH) return 'Das ist die Hypotenuse: Sie liegt dem <b>rechten</b> Winkel gegenüber.';
          if (e.s === A.falschAk) return 'Diese Kathete berührt den Winkel bei \\(' + A.V1 + '\\) — sie liegt am Winkel an: die Ankathete.';
          return 'Diese Kathete liegt dem Winkel bei \\(' + A.V1 + '\\) gegenüber: die Gegenkathete.'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* Eine Seite aus Winkel und Seite: Funktion wählen, umstellen. Halb in der Sprache GK/AK/H, halb mit den
         Standardnamen (γ = 90°, α bei A, β bei B). */
      'seite-rw': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return 'sr|' + A.w + '|' + A.geg + '|' + A.wert + '|' + A.ges; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var w = zufall([18, 22, 24, 27, 32, 33, 38, 41, 48, 52, 57, 63, 66, 72]);
          var paare = [['h', 'gk'], ['h', 'ak'], ['gk', 'h'], ['ak', 'h'], ['gk', 'ak'], ['ak', 'gk']], p = zufall(paare);
          var geg = p[0], ges = p[1], wert = zufall([4, 5, 6, 7.5, 8, 9, 12, 15, 2.8, 3.6]);
          var s = seiten(w), k = wert / s[geg], soll = r2(k * s[ges]);
          var std = Math.random() < 0.5, beiA = Math.random() < 0.5, text;
          if (std){
            var nm = beiA ? { gk: 'a', ak: 'b', h: 'c' } : { gk: 'b', ak: 'a', h: 'c' }, wn = beiA ? '\\alpha' : '\\beta';
            text = 'Rechtwinkliges Dreieck mit \\(\\gamma = 90°\\): \\(' + wn + ' = ' + w + '°\\), \\(' + nm[geg] + ' = ' + wert + '\\,\\text{cm}\\). Berechne \\(' + nm[ges] + '\\).';
          } else text = 'Rechtwinkliges Dreieck: \\(x = ' + w + '°\\), ' + NAME[geg] + ' \\(' + KURZ[geg] + ' = ' + wert + '\\,\\text{cm}\\). Berechne die ' + NAME[ges] + ' von \\(x\\).';
          // typische Fehler: falsche Funktion (Rollen von GK und AK vertauscht), umgekehrt umgestellt, RAD
          var tausch = { gk: 'ak', ak: 'gk', h: 'h' }, sr = seitenRad(w);
          var falsch = [
            [wert / s[tausch[geg]] * s[tausch[ges]], 'Gegen- und Ankathete vertauscht: Benenne die Seiten vom Winkel aus.', 'vertauscht'],
            [wert * s[geg] / s[ges], 'Falsch umgestellt. Schreib die Gleichung hin, zum Beispiel \\(\\sin x = \\tfrac{GK}{H}\\), und stell nach der gesuchten Seite um.', 'umgestellt'],
            [wert / sr[geg] * sr[ges], RAD, 'Bogenmass']];
          return { w: w, geg: geg, ges: ges, wert: wert, soll: soll, falsch: falsch, text: text, std: std }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){
          var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'x', e, A.soll, 'Welche zwei Seiten kommen vor (gegeben und gesucht)? Dazu gehört genau eine der drei Funktionen.', f); },
        loesung: function(A){ var fk = { 'gk|h': '\\sin', 'h|gk': '\\sin', 'ak|h': '\\cos', 'h|ak': '\\cos', 'gk|ak': '\\tan', 'ak|gk': '\\tan' }[A.geg + '|' + A.ges];
          var ok = A.ges === 'h' || (A.geg === 'gk' && A.ges === 'ak');
          return (ok ? '\\tfrac{' + A.wert + '}{' + fk + ' ' + A.w + '°}' : A.wert + ' \\cdot ' + fk + ' ' + A.w + '°') + ' \\approx ' + A.soll + '\\,\\text{cm}'; } },

      /* ── Kapitel 2 ── */
      'winkel-rw': { felder: ['w'], muster: 'x ≈ {w} °',
        schl: function(A){ return 'wr|' + A.k1 + '|' + A.v1 + '|' + A.k2 + '|' + A.v2; },
        eingabe: function(A){ return { w: String(A.soll) }; },
        neu: function(){
          var art = zufall(['gk|h', 'ak|h', 'gk|ak']), k = art.split('|');
          var v1, v2, soll;
          if (art === 'gk|ak'){ v1 = zufall([2, 3, 4, 5, 6, 7, 2.5, 4.5]); v2 = zufall([3, 5, 6, 8, 9, 10, 12]); if (v1 === v2) v2 += 1; soll = atanG(v1 / v2); }
          else { v2 = zufall([5, 6, 8, 9, 10, 12, 7.5]); v1 = r2(v2 * zufall([0.2, 0.3, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85])); soll = art === 'gk|h' ? asinG(v1 / v2) : acosG(v1 / v2); }
          var q = v1 / v2, std = Math.random() < 0.5, text;
          if (std){ var nm = { gk: 'a', ak: 'b', h: 'c' };
            text = 'Rechtwinkliges Dreieck mit \\(\\gamma = 90°\\): \\(' + nm[k[0]] + ' = ' + v1 + '\\,\\text{cm}\\), \\(' + nm[k[1]] + ' = ' + v2 + '\\,\\text{cm}\\). Wie gross ist \\(\\alpha\\)?'; }
          else text = 'Rechtwinkliges Dreieck: ' + NAME[k[0]] + ' von \\(x\\) \\(' + KURZ[k[0]] + ' = ' + v1 + '\\,\\text{cm}\\), ' + NAME[k[1]] + ' \\(' + KURZ[k[1]] + ' = ' + v2 + '\\,\\text{cm}\\). Wie gross ist \\(x\\)?';
          var soll2 = r2(soll), wn = std ? '\\alpha' : 'x';
          var falsch = [[90 - soll, 'Das ist der andere spitze Winkel. Benenne die Seiten von \\(' + wn + '\\) aus.', 'andere'],
                        [q, 'Das ist das Verhältnis, noch nicht der Winkel. Die Umkehrtaste macht daraus den Winkel.', 'Verhältnis'],
                        [soll * PI / 180, RAD, 'Bogenmass']];
          if (art === 'gk|ak'){ falsch.push([asinG(q), 'Mit den zwei Katheten nimmst du den Tangens.', 'Tangens']); falsch.push([1 / tanG(q), '\\(\\tan^{-1}\\) heisst Umkehrung, nicht Kehrwert.', 'Kehrwert']); }
          else falsch.push([art === 'gk|h' ? acosG(q) : asinG(q), art === 'gk|h' ? 'Zu Gegenkathete und Hypotenuse gehört der Sinus.' : 'Zu Ankathete und Hypotenuse gehört der Cosinus.', 'Funktion']);
          return { k1: k[0], v1: v1, k2: k[1], v2: v2, art: art, soll: soll2, falsch: falsch, text: text, std: std }; },
        fehler: function(A){ return fehlerListe(A, 'w', A.falsch, 0.011); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'w', e, A.soll, 'Welche zwei Seiten sind gegeben? Daraus die Funktion, dann die Umkehrtaste.', f, 0.011); },
        loesung: function(A){ var fk = { 'gk|h': '\\arcsin', 'ak|h': '\\arccos', 'gk|ak': '\\arctan' }[A.art];
          return fk + '\\tfrac{' + A.v1 + '}{' + A.v2 + '} \\approx ' + A.soll + '°'; } },

      'steigung': { felder: ['w'], muster: '{w} {einh}',
        schl: function(A){ return A.art === 'pw' ? 'st|' + A.p : A.art === 'wp' ? 'st|w|' + A.w : 'st|hl|' + A.hh + '|' + A.l; },
        eingabe: function(A){ return { w: String(A.soll) }; },
        neu: function(){
          var art = zufall(['pw', 'wp', 'hl']);
          if (art === 'pw'){ var p = zufall([5, 6, 7, 9, 10, 14, 15, 18, 20, 22, 30, 45]), s = atanG(p / 100);
            return { art: art, p: p, soll: r2(s), einh: '°', tol: 0.011, text: 'Eine Strasse hat \\(' + p + '\\,\\%\\) Steigung. Wie gross ist der Steigungswinkel?',
              falsch: [[atanG(p), '\\(' + p + '\\,\\%\\) heisst \\(\\tfrac{' + p + '}{100}\\) — nicht \\(' + p + '\\).', 'heisst'], [p, 'Prozent sind keine Grad: \\(\\tan x = \\tfrac{' + p + '}{100}\\).', 'Grad'], [asinG(p / 100), 'Die Steigung ist Höhe durch <b>waagrechte</b> Strecke: Tangens.', 'Tangens']] }; }
          if (art === 'wp'){ var w = zufall([3, 4, 6, 8, 10, 15, 20, 25]);
            return { art: art, w: w, soll: r2(tanG(w) * 100), einh: '%', text: 'Eine Rampe ist um \\(' + w + '°\\) geneigt. Wie viel Prozent Steigung hat sie?',
              falsch: [[tanG(w), 'Das ist die Steigung als Zahl. In Prozent: mal \\(100\\).', 'Prozent'], [sinG(w) * 100, 'Steigung ist Höhe durch waagrechte Strecke: Tangens, nicht Sinus.', 'Tangens'], [Math.tan(w) * 100, RAD, 'Bogenmass']] }; }
          var hh = zufall([12, 18, 24, 30, 45, 60, 75]), l = zufall([2, 2.5, 3, 4, 5, 6]) ;
          return { art: art, hh: hh, l: l, soll: r2(atanG(hh / 100 / l)), einh: '°', tol: 0.011, text: 'Eine Rampe überwindet \\(' + hh + '\\,\\text{cm}\\) Höhe auf \\(' + String(l).replace('.', '.') + '\\,\\text{m}\\) waagrechter Länge. Wie gross ist ihr Steigungswinkel?',
            falsch: [[atanG(hh / l), 'Einheiten angleichen: \\(' + hh + '\\,\\text{cm} = ' + r2(hh / 100) + '\\,\\text{m}\\).', 'Einheiten'], [atanG(l * 100 / hh), 'Vertauscht: Steigung ist Höhe durch waagrechte Strecke.', 'Vertauscht'], [asinG(hh / 100 / l), 'Die Länge ist waagrecht gemessen, also die Ankathete: Tangens.', 'Tangens']] }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh === '%' ? '%' : '°'); },
        fehler: function(A){ return fehlerListe(A, 'w', A.falsch, A.tol); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'w', e, A.soll, 'Steigung \\(= \\tan x = \\tfrac{\\text{Höhe}}{\\text{waagrechte Strecke}}\\); in Prozent mal \\(100\\).', f, A.tol); },
        loesung: function(A){ return A.art === 'pw' ? '\\arctan 0.' + String(A.p / 100).split('.')[1] + ' \\approx ' + A.soll + '°'
          : A.art === 'wp' ? '\\tan ' + A.w + '° \\cdot 100\\,\\% \\approx ' + A.soll + '\\,\\%' : '\\arctan\\tfrac{' + r2(A.hh / 100) + '}{' + A.l + '} \\approx ' + A.soll + '°'; } },

      /* ── Kapitel 3 ── */
      'hoehe': { felder: ['h'], muster: '{h} {einh}',
        schl: function(A){ return A.art === 'w' ? 'hw|w|' + A.hh + '|' + A.d : 'hw|' + A.d + '|' + A.w + '|' + A.e; },
        eingabe: function(A){ return { h: String(A.soll) }; },
        neu: function(){
          var art = zufall(['h', 'h', 'e', 'w']), obj = zufall([['eines Baums', 'der Baum'], ['eines Turms', 'der Turm'], ['eines Masts', 'der Mast'], ['eines Gebäudes', 'das Gebäude']]);
          var d = zufall([15, 18, 22, 25, 28, 35, 40, 45, 60]), w = zufall([16, 22, 26, 29, 33, 37, 42, 47, 53]);
          if (art === 'w'){ var hh = zufall([8, 12, 15, 21, 24, 30, 36]);
            return { art: art, hh: hh, d: d, soll: r2(atanG(hh / d)), einh: '°', tol: 0.011, text: 'Die Spitze ' + obj[0] + ' liegt \\(' + hh + '\\,\\text{m}\\) über deinen Augen, du stehst \\(' + d + '\\,\\text{m}\\) entfernt. Unter welchem Höhenwinkel siehst du sie?',
              falsch: [[atanG(d / hh), 'Vertauscht: \\(\\tan\\alpha = \\tfrac{h}{d}\\), die Höhe steht oben.', 'Vertauscht'], [hh / d, 'Das ist \\(\\tan\\alpha\\), noch nicht der Winkel.', 'Winkel'], [Math.atan(hh / d), RAD, 'Bogenmass']] }; }
          var e = art === 'e' ? zufall([1.5, 1.6, 1.7, 1.8]) : 0, h0 = d * tanG(w);
          var text = 'Aus \\(' + d + '\\,\\text{m}\\) Abstand siehst du die Spitze ' + obj[0] + ' unter dem Höhenwinkel \\(' + w + '°\\)'
            + (e ? ', deine Augen sind \\(' + e + '\\,\\text{m}\\) über dem Boden' : ' (Augenhöhe vernachlässigt)') + '. Wie hoch ist ' + obj[1] + '?';
          var falsch = [[d * sinG(w) + e, 'Der Abstand \\(d\\) ist die Ankathete, nicht die Hypotenuse: Tangens.', 'Tangens'], [d / tanG(w) + e, '\\(\\tan\\alpha = \\tfrac{h}{d}\\), also \\(h = d \\cdot \\tan\\alpha\\) — multiplizieren.', 'multiplizieren'], [d * Math.tan(w) + e, RAD, 'Bogenmass']];
          if (e) falsch.push([h0, 'Das ist die Höhe über deinen Augen — die Augenhöhe kommt dazu.', 'Augenhöhe']);
          return { art: art, d: d, w: w, e: e, soll: r2(h0 + e), einh: 'm', text: text, falsch: falsch }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'h', A.falsch, A.tol); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'h', e, A.soll, 'Skizze: Abstand am Boden = Ankathete, Höhe = Gegenkathete — also Tangens.', f, A.tol); },
        loesung: function(A){ return A.art === 'w' ? '\\arctan\\tfrac{' + A.hh + '}{' + A.d + '} \\approx ' + A.soll + '°' : A.d + ' \\cdot \\tan ' + A.w + '°' + (A.e ? ' + ' + A.e : '') + ' \\approx ' + A.soll + '\\,\\text{m}'; } },

      'leiter-tiefe': { felder: ['x'], muster: '{x} m',
        schl: function(A){ return 'lt|' + A.art + '|' + A.L + '|' + A.w; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['leiter', 'leiter', 'tiefe', 'tiefe', 'seil']);
          if (art === 'tiefe'){ var H = zufall([25, 30, 40, 50, 55, 70, 80]), w = zufall([8, 10, 14, 16, 20, 22, 27, 31]);
            return { art: art, L: H, w: w, soll: r2(H / tanG(w)), text: 'Von einem \\(' + H + '\\,\\text{m}\\) hohen Turm siehst du ein Boot unter dem Tiefenwinkel \\(' + w + '°\\). Wie weit ist das Boot vom Fuss des Turms entfernt?',
              falsch: [[H * tanG(w), 'Der Tiefenwinkel liegt oben (gegen die Waagrechte), am Boot ist der gleich grosse Höhenwinkel: \\(\\tan ' + w + '° = \\tfrac{' + H + '}{d}\\), also teilen.', 'teilen'], [H / sinG(w), 'Das ist der Sehstrahl zum Boot. Gesucht ist der Abstand am Boden: Tangens.', 'Tangens'], [H / Math.tan(w), RAD, 'Bogenmass']] }; }
          var L = zufall([4, 5, 6, 7, 8, 9]), w2 = zufall([58, 62, 65, 68, 72, 75]), frage = zufall(['hoch', 'fuss']);
          if (art === 'seil'){ L = zufall([30, 40, 50, 60, 80]); w2 = zufall([35, 40, 48, 55, 61]); frage = 'hoch'; }
          var soll = frage === 'hoch' ? L * sinG(w2) : L * cosG(w2);
          var text = art === 'seil' ? 'Ein Drachen hängt an einer \\(' + L + '\\,\\text{m}\\) langen, straff gespannten Schnur, die mit dem Boden den Winkel \\(' + w2 + '°\\) bildet. Wie hoch fliegt er (über der Hand)?'
            : 'Eine \\(' + L + '\\,\\text{m}\\) lange Leiter lehnt an einer Wand und bildet mit dem Boden den Winkel \\(' + w2 + '°\\). ' + (frage === 'hoch' ? 'Wie hoch reicht sie an der Wand?' : 'Wie weit steht ihr Fuss von der Wand entfernt?');
          var falsch = [[frage === 'hoch' ? L * cosG(w2) : L * sinG(w2), frage === 'hoch' ? 'Das ist der Abstand am Boden. Die Höhe liegt dem Winkel gegenüber: Sinus.' : 'Das ist die Höhe an der Wand. Der Fuss liegt am Winkel an: Cosinus.', 'Winkel'],
                        [frage === 'hoch' ? L / sinG(w2) : L / cosG(w2), 'Die Leiter (die Schnur) ist die Hypotenuse, die längste Seite: mit dem Sinus bzw. Cosinus multiplizieren.', 'multiplizieren'],
                        [frage === 'hoch' ? L * Math.sin(w2) : L * Math.cos(w2), RAD, 'Bogenmass']];
          return { art: art, L: L, w: w2, frage: frage, soll: r2(soll), text: text, falsch: falsch }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'x', e, A.soll, 'Skizze machen, den rechten Winkel suchen, die Seiten vom gegebenen Winkel aus benennen.', f); },
        loesung: function(A){ return A.art === 'tiefe' ? '\\tfrac{' + A.L + '}{\\tan ' + A.w + '°} \\approx ' + A.soll + '\\,\\text{m}' : A.L + ' \\cdot ' + (A.frage === 'hoch' ? '\\sin' : '\\cos') + ' ' + A.w + '° \\approx ' + A.soll + '\\,\\text{m}'; } },

      /* ── Kapitel 4 ── */
      /* Sinussatz bei zwei gegebenen Winkeln (WWS und WSW). */
      'sinussatz': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return 'ss|' + A.al + '|' + A.be + '|' + A.geg + '|' + A.wert + '|' + A.ges; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var al = zufall([28, 34, 41, 47, 52, 63, 76]), be = zufall([37, 44, 58, 66, 71, 84]);
          if (al + be > 150 || al === be) return TYPEN['sinussatz'].neu();
          var ga = 180 - al - be, W = { a: al, b: be, c: ga }, geg = zufall(['a', 'b', 'c']), ges = zufall(['a', 'b', 'c'].filter(function(s){ return s !== geg; }));
          var wert = zufall([5, 6, 7.5, 8, 9, 11, 12, 14]), soll = r2(wert * sinG(W[ges]) / sinG(W[geg]));
          var gw = { a: '\\alpha', b: '\\beta', c: '\\gamma' };
          var text = 'Dreieck mit \\(\\alpha = ' + al + '°\\), \\(\\beta = ' + be + '°\\) und \\(' + geg + ' = ' + wert + '\\,\\text{cm}\\). Berechne \\(' + ges + '\\).';
          var falsch = [[wert * sinG(W[geg]) / sinG(W[ges]), 'Umgekehrt: \\(\\tfrac{' + ges + '}{\\sin ' + gw[ges] + '} = \\tfrac{' + geg + '}{\\sin ' + gw[geg] + '}\\), also \\(' + ges + ' = \\tfrac{' + geg + ' \\cdot \\sin ' + gw[ges] + '}{\\sin ' + gw[geg] + '}\\).', 'Umgekehrt'],
                        [wert * Math.sin(W[ges]) / Math.sin(W[geg]), RAD, 'Bogenmass']];
          if (ges === 'c' || geg === 'c') falsch.push([wert * sinG(ges === 'c' ? 90 : W[ges]) / sinG(geg === 'c' ? 90 : W[geg]), 'Zu \\(c\\) gehört der Gegenwinkel \\(\\gamma = 180° - \\alpha - \\beta = ' + ga + '°\\).', 'gamma']);
          var andere = ['a', 'b', 'c'].filter(function(s){ return s !== geg && s !== ges; })[0];
          falsch.push([wert * sinG(W[andere]) / sinG(W[geg]), 'Falsches Paar: Über den Bruchstrich gehört die Seite, darunter der Sinus <b>ihres Gegenwinkels</b> — zu \\(' + ges + '\\) gehört \\(' + gw[ges] + '\\).', 'Paar']);
          return { al: al, be: be, ga: ga, geg: geg, ges: ges, wert: wert, soll: soll, falsch: falsch, text: text }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'x', e, A.soll, 'Zuerst den dritten Winkel, dann \\(\\tfrac{a}{\\sin\\alpha} = \\tfrac{b}{\\sin\\beta} = \\tfrac{c}{\\sin\\gamma}\\).', f); },
        loesung: function(A){ var gw = { a: '\\alpha', b: '\\beta', c: '\\gamma' }, W = { a: A.al, b: A.be, c: A.ga };
          return A.ges + ' = \\tfrac{' + A.wert + ' \\cdot \\sin ' + W[A.ges] + '°}{\\sin ' + W[A.geg] + '°} \\approx ' + A.soll + '\\,\\text{cm}'; } },

      /* SSW: Wie viele Dreiecke? Gegeben α, c und die Gegenseite a (wie in der Animation). */
      'ssw': { felder: ['n'], muster: 'Anzahl Dreiecke: {n:0|1|2}',
        schl: function(A){ return 'sw|' + A.al + '|' + A.c + '|' + A.a; },
        eingabe: function(A){ return { n: String(A.n) }; },
        neu: function(){
          var al = zufall([25, 30, 38, 42, 50, 55]), c = zufall([6, 8, 9, 10, 12]), h = c * sinG(al);
          var lage = zufall(['kein', 'zwei', 'zwei', 'eins']), a;
          if (lage === 'kein') a = Math.floor((h - 0.3) * 2) / 2;
          else if (lage === 'zwei') a = Math.min(c - 0.5, Math.ceil((h + 0.3) * 2) / 2 + zufall([0, 0.5, 1]));
          else a = c + zufall([0.5, 1, 2, 3]);
          if (a <= 0.5 || Math.abs(a - h) < 0.25 || a === c) return TYPEN['ssw'].neu();
          var n = a < h ? 0 : a < c ? 2 : 1;
          return { al: al, c: c, a: a, h: r2(h), n: n, text: 'Gegeben sind \\(\\alpha = ' + al + '°\\), \\(c = ' + c + '\\,\\text{cm}\\) und die Gegenseite \\(a = ' + a + '\\,\\text{cm}\\) von \\(\\alpha\\). Wie viele Dreiecke gibt es?' }; },
        fehler: function(A){ return [0, 1, 2].filter(function(k){ return k !== A.n; }).map(function(k){ return [{ n: String(k) }, null]; }); },
        pruefen: function(A, e){
          if (+e.n === A.n) return null;
          var hT = 'Rechne die Höhe \\(h = c \\cdot \\sin\\alpha \\approx ' + A.h + '\\,\\text{cm}\\) und vergleiche: ';
          if (A.n === 0) return hT + '\\(a\\) ist kürzer als \\(h\\) — der Kreis um \\(B\\) erreicht den Schenkel nicht.';
          if (A.n === 2) return hT + '\\(h \\lt a \\lt c\\): Der Kreis um \\(B\\) schneidet den Schenkel zweimal (spitzes und stumpfes \\(\\gamma\\)).';
          return hT + '\\(a\\) ist mindestens so lang wie \\(c\\): Der zweite Schnittpunkt läge hinter \\(A\\), es bleibt ein Dreieck.'; },
        loesung: function(A){ return 'h \\approx ' + A.h + ';\\ ' + (A.n === 0 ? 'a \\lt h' : A.n === 2 ? 'h \\lt a \\lt c' : 'a \\geq c') + '\\ \\Rightarrow\\ ' + A.n; } },

      /* ── Kapitel 5 ── */
      'cosinussatz': { felder: ['x'], muster: '{x} {einh}',
        schl: function(A){ return A.art === 'sws' ? 'cs|sws|' + A.b + '|' + A.c + '|' + A.al : 'cs|sss|' + A.a + '|' + A.b + '|' + A.c; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          if (Math.random() < 0.55){
            var b = zufall([4, 5, 6, 7, 8, 9, 12]), c = zufall([3, 5, 6, 8, 10, 11]), al = zufall([28, 36, 47, 64, 78, 95, 104, 118, 132]);
            var a2 = b * b + c * c - 2 * b * c * cosG(al);
            return { art: 'sws', b: b, c: c, al: al, soll: r2(Math.sqrt(a2)), einh: '', text: 'Dreieck mit \\(b = ' + b + '\\), \\(c = ' + c + '\\) und dem Zwischenwinkel \\(\\alpha = ' + al + '°\\). Berechne \\(a\\).',
              falsch: [[Math.sqrt(b * b + c * c), 'Das ist \\(\\sqrt{b^2 + c^2}\\) — das Korrekturglied \\(-2bc\\cos\\alpha\\) fehlt.', 'Korrektur'],
                       [Math.sqrt(b * b + c * c + 2 * b * c * cosG(al)), 'Vorzeichen: \\(a^2 = b^2 + c^2 - 2bc\\cos\\alpha\\)' + (al > 90 ? ' — und \\(\\cos ' + al + '°\\) ist negativ.' : '.'), 'Vorzeichen'],
                       [a2, 'Das ist \\(a^2\\). Zieh noch die Wurzel.', 'Wurzel'],
                       [Math.sqrt(Math.max(0, b * b + c * c - 2 * b * c * Math.cos(al))), RAD, 'Bogenmass']] }; }
          var S = zufall([[4, 5, 6], [5, 6, 8], [6, 7, 9], [4, 6, 7], [5, 8, 9], [3, 5, 7], [6, 8, 11], [4, 7, 9]]).slice();
          var ganz = S.slice(); for (var i = 2; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = ganz[i]; ganz[i] = ganz[j]; ganz[j] = t; }
          var a = ganz[0], bb = ganz[1], cc = ganz[2], ca = (bb * bb + cc * cc - a * a) / (2 * bb * cc);
          return { art: 'sss', a: a, b: bb, c: cc, soll: r2(acosG(ca)), einh: '°', tol: 0.011, text: 'Dreieck mit den Seiten \\(a = ' + a + '\\), \\(b = ' + bb + '\\), \\(c = ' + cc + '\\). Wie gross ist \\(\\alpha\\)?',
            falsch: [[ca, 'Das ist \\(\\cos\\alpha\\), noch nicht der Winkel.', 'Winkel'],
                     [acosG((a * a + bb * bb - cc * cc) / (2 * a * bb)), 'Das ist der Winkel gegenüber \\(c\\). Für \\(\\alpha\\) steht \\(a^2\\) allein: \\(\\cos\\alpha = \\tfrac{b^2 + c^2 - a^2}{2bc}\\).', 'gegenüber'],
                     [Math.acos(ca), RAD, 'Bogenmass']] }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh === '°' ? '°' : ''); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch, A.tol); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'x', e, A.soll, A.art === 'sws' ? '\\(a^2 = b^2 + c^2 - 2bc\\cos\\alpha\\), dann die Wurzel.' : '\\(\\cos\\alpha = \\tfrac{b^2 + c^2 - a^2}{2bc}\\), dann \\(\\arccos\\).', f, A.tol); },
        loesung: function(A){ return A.art === 'sws' ? 'a = \\sqrt{' + A.b + '^2 + ' + A.c + '^2 - 2 \\cdot ' + A.b + ' \\cdot ' + A.c + ' \\cdot \\cos ' + A.al + '°} \\approx ' + A.soll
          : '\\alpha = \\arccos\\tfrac{' + A.b + '^2 + ' + A.c + '^2 - ' + A.a + '^2}{2 \\cdot ' + A.b + ' \\cdot ' + A.c + '} \\approx ' + A.soll + '°'; } },

      'flaeche': { felder: ['A'], muster: 'A ≈ {A} cm²',
        schl: function(A){ return 'fl|' + A.p + '|' + A.q + '|' + A.phi; },
        eingabe: function(A){ return { A: String(A.soll) }; },
        neu: function(){
          var p = zufall([3, 4, 5, 6, 7.5, 8, 9, 12]), q = zufall([4, 5, 6, 8, 10, 11]), phi = zufall([25, 35, 48, 62, 75, 105, 118, 136, 142]);
          var gn = zufall([['a', 'b', '\\gamma'], ['b', 'c', '\\alpha'], ['a', 'c', '\\beta']]);
          return { p: p, q: q, phi: phi, soll: r2(p * q / 2 * sinG(phi)), text: 'Dreieck mit \\(' + gn[0] + ' = ' + p + '\\,\\text{cm}\\), \\(' + gn[1] + ' = ' + q + '\\,\\text{cm}\\) und dem Zwischenwinkel \\(' + gn[2] + ' = ' + phi + '°\\). Berechne die Fläche.',
            falsch: [[p * q / 2, 'Das wäre ein rechter Winkel. Die Höhe ist \\(' + gn[0] + ' \\cdot \\sin ' + gn[2] + '\\), nicht \\(' + gn[0] + '\\).', 'rechter'],
                     [p * q * sinG(phi), 'Das \\(\\tfrac{1}{2}\\) fehlt: Dreieck ist die Hälfte.', 'Hälfte'],
                     [p * q / 2 * cosG(phi), 'Die Höhe kommt mit dem Sinus, nicht mit dem Cosinus.', 'Sinus'],
                     [p * q / 2 * Math.sin(phi), RAD, 'Bogenmass']] }; },
        fehler: function(A){ return fehlerListe(A, 'A', A.falsch); },
        pruefen: function(A, e){ var f = A.falsch.filter(function(x){ return Math.abs(r2(x[0]) - A.soll) > 0.07; });
          return feld(A, 'A', e, A.soll, '\\(A = \\tfrac{p \\cdot q}{2}\\sin\\varphi\\) mit dem Winkel <b>zwischen</b> den beiden Seiten.', f); },
        loesung: function(A){ return 'A = \\tfrac{' + A.p + ' \\cdot ' + A.q + '}{2} \\sin ' + A.phi + '° \\approx ' + A.soll + '\\,\\text{cm}^2'; } },

      'welcher-satz': { felder: ['s'], muster: '{s:Sinussatz|Cosinussatz}',
        eingabe: function(A){ return { s: A.soll }; },
        neu: function(){
          var faelle = [
            ['\\(\\alpha\\), \\(\\beta\\) und \\(a\\)', 'Sinussatz', 'WWS', 'Das Paar \\(a\\) und \\(\\alpha\\) ist vollständig.'],
            ['\\(\\beta\\), \\(\\gamma\\) und \\(a\\)', 'Sinussatz', 'WSW', 'Zuerst \\(\\alpha = 180° - \\beta - \\gamma\\) — dann ist das Paar \\(a\\), \\(\\alpha\\) vollständig.'],
            ['\\(a\\), \\(b\\) und \\(\\alpha\\)', 'Sinussatz', 'SSW', 'Das Paar \\(a\\) und \\(\\alpha\\) ist vollständig (an die zweite Lösung denken).'],
            ['\\(b\\), \\(c\\) und \\(\\alpha\\)', 'Cosinussatz', 'SWS', 'Kein Paar: \\(\\alpha\\) liegt zwischen \\(b\\) und \\(c\\), seine Gegenseite \\(a\\) fehlt.'],
            ['\\(a\\), \\(c\\) und \\(\\beta\\)', 'Cosinussatz', 'SWS', 'Kein Paar: \\(\\beta\\) liegt zwischen \\(a\\) und \\(c\\).'],
            ['\\(a\\), \\(b\\) und \\(c\\)', 'Cosinussatz', 'SSS', 'Kein Winkel bekannt, also kein Paar.'],
            ['\\(b\\), \\(c\\) und \\(\\beta\\)', 'Sinussatz', 'SSW', 'Das Paar \\(b\\) und \\(\\beta\\) ist vollständig.'],
            ['\\(\\alpha\\), \\(\\gamma\\) und \\(b\\)', 'Sinussatz', 'WSW', 'Zuerst \\(\\beta\\) aus der Winkelsumme — dann ist das Paar \\(b\\), \\(\\beta\\) vollständig.']];
          var f = zufall(faelle);
          return { soll: f[1], fall: f[2], grund: f[3], text: 'Gegeben sind ' + f[0] + ' (' + f[2] + '). Mit welchem Satz beginnst du?' }; },
        fehler: function(A){ return [[{ s: A.soll === 'Sinussatz' ? 'Cosinussatz' : 'Sinussatz' }, null]]; },
        pruefen: function(A, e){
          if (e.s === A.soll) return null;
          return A.soll === 'Sinussatz' ? 'Suche ein Paar aus einer Seite und ihrem Gegenwinkel. ' + A.grund : 'Gibt es ein vollständiges Paar aus Seite und Gegenwinkel? ' + A.grund; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } }
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

  /* ---------- Figuren zu den Aufgaben: <svg class="geo-mini" data-fig='[…]' data-fenster="x0,x1,y0">
       Einträge: ["v", [[x,y],…], cls] Vieleck · ["s", [x,y], [x,y], cls] Strecke · ["t", [x,y], "Text", cls, dx, dy, anker] ·
       ["p", [x,y]] Punkt · ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel · ["w", Scheitel, [x,y], [x,y], "Text"] Winkelbogen
       von der Richtung zum ersten zum zweiten Punkt. ---------- */
  document.querySelectorAll('svg.geo-mini[data-fig]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-1,9,-1').split(',').map(Number), b = +(svg.dataset.breite || 220), h = +(svg.dataset.hoehe || 150);
    var F = Flaeche(svg, { w: b, h: h, x0: fe[0], x1: fe[1], y0: fe[2], karo: svg.dataset.karo === 'ja' ? 1 : false });
    JSON.parse(svg.dataset.fig).forEach(function(e){
      var t = e[0];
      if (t === 'v') F.vieleck(e[1], e[2] || 'figur');
      else if (t === 's') F.strecke(e[1], e[2], e[3] || 'hilfe');
      else if (t === 't') F.text(e[1], e[2], e[3] || 'mass', e[4], e[5], e[6]);
      else if (t === 'p') F.punkt(e[1]);
      else if (t === 'r') F.rechts(e[1], e[2], e[3], '');
      else if (t === 'w') winkelMarke(F, e[1], e[2], e[3], e[5] || 20, 'winkelbogen', e[4], 'winkel klein');
    });
    svg.setAttribute('role', 'img');
  });
})();
</script>
