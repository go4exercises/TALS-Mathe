<script>
/* Leitprogramm Kreis und Kreisteile — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit Rückmeldung,
   Figuren zu den Aufgaben. Gerüst (Flaeche, Leiste, arbeitsbereich, Übungsrahmen, Figuren) als Kopie aus dem
   Leitprogramm Trigonometrische Berechnungen (dort aus Planimetrie übernommen); neu: Sektor, Kreisring,
   Kandidat auf einem Bogen, Korrektur zweier gekoppelter Regler. Inhalte neu.
   Notation wie auf der Themenseite 5.2c: Mittelpunkt M, Radius r, Durchmesser d, Sehne s, Abstand a der Geraden
   von M; Zentriwinkel φ, Bogenlänge b, Sektorfläche A_SK, Segmentfläche A_SG; Kreisring mit Aussenradius R,
   Innenradius r, Ringbreite b = R − r, mittlerem Radius r_m. Winkel in Grad.
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Figur · orange = Element, Hilfslinie, Kandidat ·
   grün = Fläche, gesuchte Grösse, Ergebnis · rot = Fehler. Dezimalpunkt; gerundet mit «≈». */
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
  function zahl(s){
    var komma = /\d,\d/.test(s);
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^≈/, '').replace(/°$/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  /* Vergleich gerundeter Ergebnisse: richtig auf zwei Dezimalen (Toleranz 0.006, bei Winkeln 0.011);
     «nah» heisst: richtig gerechnet, aber zu grob gerundet. */
  function stimmt(e, soll, tol){ return Math.abs(e - soll) <= (tol || 0.006) + 1e-9; }
  function nah(e, soll, tol){ return !stimmt(e, soll, tol) && Math.abs(e - soll) <= Math.max(0.06, Math.abs(soll) * 0.005); }
  var RUNDEN = 'Fast — runde auf zwei Dezimalen (Zwischenresultate ungerundet weiterverwenden, \\(\\pi\\) mit der Taste).';
  var PI3 = 'Mit \\(\\pi \\approx 3\\) oder \\(3.14\\) gerechnet? Nimm die \\(\\pi\\)-Taste.';
  function grad(w){ return w * PI / 180; }

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
    function P(p){ return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }
    var F = {
      s: s, ebene: ebene, X: X, Y: Y,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      vieleck: function(pts, cls){ return el(ebene, 'polygon', { points: pts.map(P).join(' '), 'class': cls }); },
      linienzug: function(pts, cls){ return el(ebene, 'polyline', { points: pts.map(P).join(' '), 'class': cls }); },
      strecke: function(a, b, cls){ return el(ebene, 'line', { x1: X(a[0]), y1: Y(a[1]), x2: X(b[0]), y2: Y(b[1]), 'class': cls }); },
      gerade: function(a, b, cls){   // ganze Gerade durch a und b, am Bild abgeschnitten
        var dx = b[0] - a[0], dy = b[1] - a[1], L = 100 / Math.hypot(dx, dy);
        return F.strecke([a[0] - dx * L, a[1] - dy * L], [a[0] + dx * L, a[1] + dy * L], cls); },
      kreis: function(m, r, cls){ return el(ebene, 'circle', { cx: X(m[0]), cy: Y(m[1]), r: r * s, 'class': cls }); },
      /* Sektor von w0 bis w1 (Bogenmass, gegen den Uhrzeigersinn); nurBogen: nur der Bogen */
      sektor: function(m, r, w0, w1, cls, nurBogen){
        if (w1 - w0 >= 2 * PI - 1e-9) return F.kreis(m, r, cls);
        var a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var gross = (w1 - w0) > PI ? 1 : 0;
        var d = (nurBogen ? 'M' : 'M' + X(m[0]) + ' ' + Y(m[1]) + ' L') + X(a[0]) + ' ' + Y(a[1]) + ' A' + r * s + ' ' + r * s + ' 0 ' + gross + ' 0 ' + X(b[0]) + ' ' + Y(b[1]) + (nurBogen ? '' : ' Z');
        return el(ebene, 'path', { d: d, 'class': cls }); },
      /* Kreisring zwischen den Radien ri und ra (Füllregel evenodd) */
      ring: function(m, ra, ri, cls){
        function k(r){ return 'M' + X(m[0] + r) + ' ' + Y(m[1]) + ' A' + r * s + ' ' + r * s + ' 0 1 0 ' + X(m[0] - r) + ' ' + Y(m[1]) + ' A' + r * s + ' ' + r * s + ' 0 1 0 ' + X(m[0] + r) + ' ' + Y(m[1]) + ' Z'; }
        return el(ebene, 'path', { d: k(ra) + ' ' + k(ri), 'class': cls, 'fill-rule': 'evenodd' }); },
      /* Winkelbogen um m von Richtung w0 bis w1 (Bogenmass, gegen den Uhrzeigersinn), Radius in Pixeln */
      bogen: function(m, w0, w1, rpx, cls){
        var r = rpx / s, a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var gross = (w1 - w0) > PI ? 1 : 0;
        return el(ebene, 'path', { d: 'M' + X(a[0]) + ' ' + Y(a[1]) + ' A' + rpx + ' ' + rpx + ' 0 ' + gross + ' 0 ' + X(b[0]) + ' ' + Y(b[1]), 'class': cls }); },
      punkt: function(p, cls){ return el(ebene, 'circle', { cx: X(p[0]), cy: Y(p[1]), r: 3.5, 'class': cls || 'g-pkt' }); },
      text: function(p, t, cls, dx, dy, anker){
        return el(ebene, 'text', { x: X(p[0]) + (dx || 0), y: Y(p[1]) + (dy || 0), 'text-anchor': anker || 'middle', 'class': 'g-text ' + (cls || '') }, t); },
      rechts: function(fuss, r1, r2, cls){   // Zeichen für den rechten Winkel, Richtungen als Vektoren
        var q = 9 / s, n1 = Math.hypot(r1[0], r1[1]), n2 = Math.hypot(r2[0], r2[1]);
        var u = [r1[0] / n1 * q, r1[1] / n1 * q], v = [r2[0] / n2 * q, r2[1] / n2 * q];
        return el(ebene, 'polyline', { points: [P([fuss[0] + u[0], fuss[1] + u[1]]), P([fuss[0] + u[0] + v[0], fuss[1] + u[1] + v[1]]), P([fuss[0] + v[0], fuss[1] + v[1]])].join(' '), 'class': 'g-rechts ' + (cls || '') }); },
      /* Kandidat zum Antippen: sichtbare Linie plus breiter, unsichtbarer Treffstreifen. */
      kandidat: function(id, a, b, wahl, ganz){
        var gr = el(ebene, 'g', { 'class': 'kandidat', tabindex: 0, role: 'button', 'aria-label': 'Linie ' + id, 'data-id': id });
        var A = a, B = b;
        if (ganz){ var dx = B[0] - A[0], dy = B[1] - A[1], L = 100 / Math.hypot(dx, dy); A = [A[0] - dx * L, A[1] - dy * L]; B = [B[0] + dx * L, B[1] + dy * L]; }
        el(gr, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': 'k-sicht' });
        el(gr, 'line', { x1: X(A[0]), y1: Y(A[1]), x2: X(B[0]), y2: Y(B[1]), 'class': 'k-treffer' });
        gr.addEventListener('click', function(){ wahl(id); });
        gr.addEventListener('keydown', function(ev){ if (ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); wahl(id); } });
        return gr; },
      /* Kandidat auf einem Linienzug (Kreisbogen). Die Attribute x1 … y2 nennen Anfang und Mitte des Zugs: Daran
         erkennt das Prüfwerkzeug pruef-geo deckungsgleiche Kandidaten. Anfang und Ende allein fielen mit der Sehne
         über demselben Bogen zusammen, die aber sichtbar daneben liegt. */
      kandidatZug: function(id, pts, wahl){
        var gr = el(ebene, 'g', { 'class': 'kandidat', tabindex: 0, role: 'button', 'aria-label': 'Linie ' + id, 'data-id': id });
        var m = pts[Math.floor(pts.length / 2)], at = { x1: X(pts[0][0]), y1: Y(pts[0][1]), x2: X(m[0]), y2: Y(m[1]) };
        var a1 = el(gr, 'polyline', { points: pts.map(P).join(' '), 'class': 'k-sicht' }), a2 = el(gr, 'polyline', { points: pts.map(P).join(' '), 'class': 'k-treffer' });
        for (var k in at){ a1.setAttribute(k, at[k]); a2.setAttribute(k, at[k]); }
        gr.addEventListener('click', function(){ wahl(id); });
        gr.addEventListener('keydown', function(ev){ if (ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); wahl(id); } });
        return gr; }
    };
    return F;
  }
  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function pol(m, r, w){ return [m[0] + r * Math.cos(w), m[1] + r * Math.sin(w)]; }
  /* Punkte auf dem Kreisbogen von w0 bis w1 (Bogenmass) */
  function bogenPunkte(m, r, w0, w1, n){
    var p = [], k; n = n || Math.max(8, Math.ceil(Math.abs(w1 - w0) / 0.06));
    for (k = 0; k <= n; k++) p.push(pol(m, r, w0 + (w1 - w0) * k / n));
    return p;
  }
  function richtung(p, q){ return Math.atan2(q[1] - p[1], q[0] - p[0]); }
  /* Winkel bei p zwischen den Richtungen zu a und zu b: Bogen gegen den Uhrzeigersinn, Beschriftung auf der
     Winkelhalbierenden. */
  function winkelMarke(F, p, a, b, rpx, cls, text, tcls){
    var w0 = richtung(p, a), w1 = richtung(p, b);
    while (w1 < w0) w1 += 2 * PI;
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
     arbeitsbereich(id, { fenster, zeichnen(F, w, k), aufgaben, korrigiere }) — jede Aufgabe:
       text, setup(sim) (Regler setzen: sim.setze({ r: 4 }), sim.sperre('r')),
       wahl: { richtig: 'sehne', rueck: { id: 'Text' } }    — Linie antippen
       frage: [{ name, label, einheit, soll, tol, fehler: [[wert, 'Text']] }] — Grössen eingeben
       ziel: function(w) — Reglerzustand (w = Werte der Regler, w.bewegt); probe: ein Zustand, der es löst
       fest: { … } — Werte, die die Figur statt der Regler zeigt (nicht auf dem Reglerraster); verdeckt: Regler mit «?»;
       ohne: Regler, die in dieser Figur nichts bedeuten (Anzeige «–»)
     korrigiere(regler, p): hält gekoppelte Regler gültig (Kreisring: r < R); läuft vor dem Zeichnen. */
  function arbeitsbereich(id, o){
    var fig = document.getElementById(id); if (!fig) return;
    var F = Flaeche(fig.querySelector('svg'), o.fenster), regler = {}, bewegt = {}, aufgabe = null, gewaehlt = null, richtig = false, pruefen = function(){};
    var ein = fig.querySelector('.g-eingabe'), rueck = fig.querySelector('.g-rueck'), formel = fig.querySelector('[data-rolle="formel"]');
    fig.querySelectorAll('input[type=range]').forEach(function(inp){
      regler[inp.dataset.p] = inp;
      inp.addEventListener('input', function(){ bewegt[inp.dataset.p] = true; if (o.korrigiere) o.korrigiere(regler, inp.dataset.p); zeichnen(); });
    });
    function werte(){
      var w = { bewegt: bewegt };
      for (var k in regler) w[k] = +regler[k].value;
      return w;
    }
    /* Anzeige neben den Reglern aus den Werten, die die Figur zeigt (mit `fest`), die gesuchte Grösse als «?» */
    function anzeigen(w){
      var verdeckt = (aufgabe && aufgabe.verdeckt) || [], ohne = (aufgabe && aufgabe.ohne) || [];
      for (var k in regler){ var sv = regler[k].parentNode.querySelector('.sl-val'); if (!sv) continue;
        sv.textContent = verdeckt.indexOf(k) >= 0 ? '?' : ohne.indexOf(k) >= 0 ? '–' : z(w[k]) + (regler[k].dataset.einheit || ''); }
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
        r.push((aufgabe.frage.length > 1 ? f.name + ': ' : '') + (t || (nah(e.wert, f.soll, f.tol) ? RUNDEN : f.tipp || 'Noch nicht. Rechne nach.')));
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
      aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; aufgabe = null; gewaehlt = null; richtig = false; rueck.className = 'g-rueck'; rueck.innerHTML = ''; eingabeZeigen(); }
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
  var gleich = function(a, b){ return Math.abs(a - b) < 1e-9; };

  /* ---------- Kapitel 1: Linien am Kreis ----------
     Unterschied zur Animation 1 der Themenseite (sechs Begriffe per Chip, Punkte ziehen, Abstand-Regler bei festem
     r = 3): Hier sind Abstand a und Radius r die Regler — die Tangente entsteht auch, wenn man r an a anpasst —,
     die Linien werden angetippt und Sehne, Abstand und Tangentenstrecke mit Pythagoras berechnet.
     Startwert r = 5 cm, a = 3 cm wie im Einführungsclip. Die Gerade liegt waagrecht im Abstand a über M. */
  var W1 = { pas: -6.2, tw: grad(140), sek: { n: grad(250), a: 2 }, sehne: [grad(20), grad(95)], rad: grad(300) };
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 320, x0: -7.5, x1: 7.5, y0: -7.2 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, M = [0, 0];
      if (Au.tangente){
        /* Tangente von P aus: M(−3.4 | 0), r = 4, P(5.1 | 0), MP = 8.5; Berührpunkt B mit cos θ = r / MP */
        var Mt = [-3.4, 0], rt = 4, Pt = [5.1, 0], th = Math.acos(rt / 8.5), B = pol(Mt, rt, th);
        F.kreis(Mt, rt, 'figur kreis');
        F.strecke(Mt, Pt, 'hilfe2');
        F.strecke(Mt, B, 'radius');
        F.gerade(B, Pt, 'tangente-linie');
        F.rechts(B, [Mt[0] - B[0], Mt[1] - B[1]], [Pt[0] - B[0], Pt[1] - B[1]], '');
        if (w.richtig) F.strecke(B, Pt, 'hilfe');
        [[Mt, 'M', -2, 15], [Pt, 'P', 6, 15], [B, 'B', -4, -8]].forEach(function(q){ F.punkt(q[0]); F.text(q[0], q[1], 'ecke', q[2], q[3]); });
        F.text(mitte(Mt, B), 'r = 4 cm', 'mass', -6, 0, 'end');
        F.text(mitte(Mt, Pt), 'MP = 8.5 cm', 'mass', 0, 15);
        F.text(mitte(B, Pt), w.richtig ? 'PB = 7.5 cm' : 'PB = ?', w.richtig ? 'mass ergebnis' : 'mass', 8, -6, 'start');
        return '\\(r = 4\\,\\text{cm}\\); \\(\\overline{MP} = 8.5\\,\\text{cm}\\); gesucht: Tangentenstrecke \\(\\overline{PB}\\)';
      }
      if (k.wahl){
        /* feste Figur mit r = 5: Passante, Tangente, Sekante, Sehne, Radius — keine zwei Linien deckungsgleich */
        var rr = 5;
        F.kreis(M, rr, 'figur kreis');
        var T = pol(M, rr, W1.tw), td = [-Math.sin(W1.tw), Math.cos(W1.tw)];
        var sn = [Math.cos(W1.sek.n), Math.sin(W1.sek.n)], sf = [W1.sek.a * sn[0], W1.sek.a * sn[1]], sd = [-sn[1], sn[0]];
        var S1 = pol(M, rr, W1.sehne[0]), S2 = pol(M, rr, W1.sehne[1]);
        F.kandidat('passante', [-6, W1.pas], [6, W1.pas], k.wahl, true);
        F.kandidat('tangente', [T[0] - 3 * td[0], T[1] - 3 * td[1]], [T[0] + 3 * td[0], T[1] + 3 * td[1]], k.wahl, true);
        F.kandidat('sekante', [sf[0] - 3 * sd[0], sf[1] - 3 * sd[1]], [sf[0] + 3 * sd[0], sf[1] + 3 * sd[1]], k.wahl, true);
        F.kandidat('sehne', S1, S2, k.wahl);
        F.kandidat('radius', M, pol(M, rr, W1.rad), k.wahl);
        if (w.richtig && Au.wahl.richtig === 'tangente'){ F.strecke(M, T, 'hilfe'); F.rechts(T, [-T[0], -T[1]], td, 'hilfe'); F.punkt(T, 'g-pkt hilfe'); }
        if (w.richtig && Au.wahl.richtig === 'sehne'){ F.strecke(S1, S2, 'hilfe'); F.punkt(S1, 'g-pkt hilfe'); F.punkt(S2, 'g-pkt hilfe'); }
        F.punkt(M); F.text(M, 'M', 'ecke', -9, 14);
        return '\\(r = 5\\,\\text{cm}\\)';
      }
      var r = w.r, a = w.a, typ = a > r + 1e-9 ? 'p' : gleich(a, r) ? 't' : 's';
      F.kreis(M, r, 'figur kreis');
      F.gerade([-1, a], [1, a], 'gerade-linie');
      F.strecke(M, [0, a], 'lot');
      if (a > 0.3) F.rechts([0, a], [1, 0], [0, -1], '');
      var R0 = pol(M, r, grad(215));
      F.strecke(M, R0, 'radius');
      if (typ === 's'){ var q = Math.sqrt(r * r - a * a); F.strecke([-q, a], [q, a], 'sehne'); F.punkt([-q, a], 'g-pkt hilfe'); F.punkt([q, a], 'g-pkt hilfe'); }
      if (typ === 't') F.punkt([0, a], 'g-pkt hilfe');
      F.punkt(M); F.text(M, 'M', 'ecke', 9, 14);
      var la = Au.lab || {};
      F.text(mitte(M, R0), la.r || 'r', 'seite' + (la.r ? ' mass' : ''), -6, 4, 'end');
      F.text([0, a / 2], la.a || 'a', 'seite' + (la.a ? ' mass' : ''), -6, 4, 'end');
      if (la.s) F.text([0, a], la.s, 'mass', 0, -8);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      var art = typ === 'p' ? '\\(a \\gt r\\): Passante, kein gemeinsamer Punkt' : typ === 't' ? '\\(a = r\\): Tangente, genau ein gemeinsamer Punkt' : '\\(a \\lt r\\): Sekante, zwei gemeinsame Punkte';
      return '\\(r = ' + z(r) + '\\,\\text{cm}\\); \\(a = ' + z(a) + '\\,\\text{cm}\\); ' + art;
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(a\\). Wie viele Punkte hat die Gerade mit dem Kreis gemeinsam?', probe: { a: 4 }, ziel: function(w){ return w.bewegt.a; } },
      { text: 'Mach die Gerade zur Passante.', probe: { a: 6 }, ziel: function(w){ return w.a > w.r + 1e-9; } },
      { text: 'Lass \\(a = 3\\,\\text{cm}\\) und mach die Gerade zur Tangente — nur mit dem Radius.', setup: function(s){ s.sperre('a'); }, probe: { r: 3 }, ziel: function(w){ return gleich(w.r, w.a); } },
      { text: 'Tipp die Sehne an.', ohne: ['a'], setup: function(s){ s.sperre('r', 'a'); },
        wahl: { richtig: 'sehne', gut: 'Die Sehne ist eine Strecke: Sie verbindet zwei Punkte der Kreislinie.', rueck: {
          sekante: 'Das ist eine Sekante: eine Gerade, die über den Kreis hinausgeht. Die Sehne endet an der Kreislinie.',
          tangente: 'Das ist eine Tangente: Sie berührt den Kreis nur in einem Punkt.',
          passante: 'Das ist eine Passante: Sie hat keinen Punkt mit dem Kreis gemeinsam.',
          radius: 'Das ist ein Radius: Er beginnt im Mittelpunkt \\(M\\).' } } },
      { text: 'Tipp die Tangente an.', ohne: ['a'], setup: function(s){ s.sperre('r', 'a'); },
        wahl: { richtig: 'tangente', gut: 'Sie berührt den Kreis in genau einem Punkt und steht dort senkrecht auf dem Radius.', rueck: {
          sekante: 'Das ist eine Sekante: Sie schneidet die Kreislinie in zwei Punkten.',
          sehne: 'Das ist eine Sehne — eine Strecke zwischen zwei Kreispunkten, keine Gerade.',
          passante: 'Das ist eine Passante: Sie hat keinen Punkt mit dem Kreis gemeinsam.',
          radius: 'Das ist ein Radius: eine Strecke von \\(M\\) zur Kreislinie.' } } },
      { text: '\\(r = 6\\,\\text{cm}\\), \\(a = 2.5\\,\\text{cm}\\). Wie lang ist die Sehne?', setup: function(s){ s.setze({ r: 6, a: 2.5 }); s.sperre('r', 'a'); },
        lab: { r: 'r = 6 cm', a: 'a = 2.5 cm', s: 's = ?' }, gegeben: '\\(r = 6\\,\\text{cm}\\), \\(a = 2.5\\,\\text{cm}\\)', gesucht: 'Sehne \\(s\\)',
        frage: [{ name: 's', label: '\\(s \\approx\\)', einheit: 'cm', soll: 10.91, fehler: [[5.45, 'Das ist die halbe Sehne. Das Lot von \\(M\\) halbiert die Sehne — verdopple.'], [13, 'Im rechtwinkligen Dreieck ist \\(r\\) die Hypotenuse: \\(\\left(\\tfrac{s}{2}\\right)^2 = r^2 - a^2\\), minus statt plus.'], [6.5, 'Minus statt plus — und das Ergebnis ist erst die halbe Sehne.'], [7, 'Mit Längen rechnet Pythagoras nicht: Quadrate subtrahieren, dann die Wurzel.']], tipp: 'Rechtwinkliges Dreieck aus \\(a\\), der halben Sehne und \\(r\\) als Hypotenuse.' }] },
      { text: 'Eine Sehne ist \\(8\\,\\text{cm}\\) lang, \\(r = 6\\,\\text{cm}\\). Wie weit ist sie von \\(M\\) entfernt?', fest: { r: 6, a: Math.sqrt(20) }, verdeckt: ['a'], setup: function(s){ s.sperre('r', 'a'); },
        lab: { r: 'r = 6 cm', a: 'a = ?', s: 's = 8 cm' }, gegeben: '\\(r = 6\\,\\text{cm}\\), \\(s = 8\\,\\text{cm}\\)', gesucht: 'Abstand \\(a\\)',
        frage: [{ name: 'a', label: '\\(a \\approx\\)', einheit: 'cm', soll: 4.47, fehler: [[7.21, 'Im rechtwinkligen Dreieck ist \\(r\\) die Hypotenuse: \\(a^2 = r^2 - \\left(\\tfrac{s}{2}\\right)^2\\).'], [5.29, 'Das ist \\(\\sqrt{8^2 - 6^2}\\): mit der ganzen Sehne als Hypotenuse. Im rechtwinkligen Dreieck sind die <b>halbe</b> Sehne \\(4\\,\\text{cm}\\) und \\(a\\) die Katheten, \\(r\\) ist die Hypotenuse.'], [2, 'Mit Längen rechnet Pythagoras nicht: Quadrate subtrahieren, dann die Wurzel.']], tipp: '\\(a^2 + \\left(\\tfrac{s}{2}\\right)^2 = r^2\\).' }] },
      { text: 'Von \\(P\\) aus berührt eine Tangente den Kreis in \\(B\\). \\(\\overline{MP} = 8.5\\,\\text{cm}\\), \\(r = 4\\,\\text{cm}\\). Wie lang ist \\(\\overline{PB}\\)?', tangente: true, fest: { r: 4 }, ohne: ['a'], setup: function(s){ s.sperre('r', 'a'); },
        frage: [{ name: 'PB', label: '\\(\\overline{PB} \\approx\\)', einheit: 'cm', soll: 7.5, fehler: [[9.39, 'Der rechte Winkel liegt bei \\(B\\): \\(\\overline{MP}\\) ist die Hypotenuse. Also \\(\\overline{PB}^2 = \\overline{MP}^2 - r^2\\).'], [4.5, 'Das ist der Abstand von \\(P\\) zur Kreislinie, nicht die Tangentenstrecke.']], tipp: 'Die Tangente steht in \\(B\\) senkrecht auf dem Radius: Pythagoras im Dreieck \\(MBP\\).' }] }
    ]
  });

  /* ---------- Kapitel 2: Umfang, Fläche und π ----------
     Wie Animation 4 der Themenseite: Der Kreis wird in n Sektoren geschnitten und abwechselnd zu einem Streifen
     gelegt. Unterschied: kein Umordnungs-Regler, dafür der Radius als Regler, eine Seite des Streifens zum
     Antippen und Umfang, Fläche und Radius zum Berechnen. Startwert r = 3 cm, n = 8 wie im Einführungsclip.
     Streifen: Spitze-unten-Sektoren (gerade k) bei x_s + 2kc, Spitze-oben (ungerade) bei x_s + (2k+1)c mit
     c = r sin(π/n); unten liegen n/2 Bögen, zusammen π r. */
  var C2 = [0, 4.2], YB = -4.3;
  function sektorZug(m, r, w0, w1){ return [m].concat(bogenPunkte(m, r, w0, w1, 10)); }
  function streifen(r, n){
    var c = r * Math.sin(PI / n), h = r * Math.cos(PI / n), xs = -(n - 1) * c / 2, aus = [];
    for (var k = 0; k < n; k++){
      var j = Math.floor(k / 2), oben = k % 2 === 1;
      // Spitze unten: Spitze (x, YB), Bogen oben um die Senkrechte; Spitze oben: Spitze (x, YB + h), Bogen unten
      var sp = oben ? [xs + (2 * j + 1) * c, YB + h] : [xs + 2 * j * c, YB], mw = oben ? -PI / 2 : PI / 2;
      aus.push({ pts: sektorZug(sp, r, mw - PI / n, mw + PI / n), k: k });
    }
    return { teile: aus, xs: xs, c: c, h: h, breite: n * c };
  }
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 357, x0: -6.5, x1: 6.5, y0: -6.0 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, r = w.r, n = w.n, i;
      if (Au.nurKreis){            // Umkehraufgabe: nur der Kreis mit der Angabe (Skizze; der Radius ist gesucht)
        F.kreis(C2, 3.5, 'figur kreis'); F.punkt(C2);
        F.strecke(C2, pol(C2, 3.5, grad(30)), 'hilfe');
        F.text(pol(C2, 1.9, grad(30)), 'r = ?', 'mass', 0, -9);
        F.text([C2[0], C2[1] - 3.5], Au.angabe, 'mass ergebnis-gross', 0, 20);
        return Au.gegeben + '; gesucht: ' + Au.gesucht;
      }
      for (i = 0; i < n; i++) F.vieleck(sektorZug(C2, r, 2 * PI * i / n, 2 * PI * (i + 1) / n), i % 2 ? 'figur satt' : 'figur');
      F.punkt(C2);
      var S = streifen(r, n);
      S.teile.forEach(function(t){ F.vieleck(t.pts, t.k % 2 ? 'figur satt' : 'figur'); });
      var bl = [S.xs, YB - 0.45], br = [S.xs + S.breite, YB - 0.45], hu = [S.xs - S.c - 0.4, YB], ho = [S.xs - S.c - 0.4, YB + r];
      var dl = [C2[0] - r, C2[1]], dr = [C2[0] + r, C2[1]];
      if (k.wahl){
        F.kandidat('breite', bl, br, k.wahl); F.kandidat('hoehe', hu, ho, k.wahl); F.kandidat('durchmesser', dl, dr, k.wahl);
      }
      var beschr = Au.labels || (Au.wahl && w.richtig);
      if (beschr){
        F.strecke(bl, br, 'hilfe'); F.strecke(hu, ho, 'hilfe');
        F.text(mitte(bl, br), '≈ π · r', 'hilfe', 0, 16); F.text(mitte(hu, ho), 'r', 'hilfe', -6, 4, 'end');
      }
      if (Au.lab) F.text(pol(C2, r + 0.2, grad(45)), Au.lab, 'mass', 4, -2, 'start');
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      var t = '\\(r = ' + z(r) + '\\,\\text{cm}\\); \\(n = ' + n + '\\) Sektoren';
      if (beschr) t += '<br>Streifen: Höhe \\(r\\), Breite \\(\\approx \\pi \\cdot r\\) (der halbe Umfang); Fläche \\(\\approx \\pi r \\cdot r = \\pi r^2\\)';
      return t;
    },
    aufgaben: [
      { text: 'Erkunde: Erhöhe die Anzahl Sektoren \\(n\\). Welche Form nimmt der Streifen unten an?', probe: { n: 16 }, ziel: function(w){ return w.bewegt.n; } },
      { text: 'Tipp die Strecke an, die so lang ist wie der halbe Umfang des Kreises.', setup: function(s){ s.setze({ n: 24 }); s.sperre('r', 'n'); },
        wahl: { richtig: 'breite', gut: 'Unten liegen die Bögen der halben Sektoren: zusammen der halbe Umfang, \\(\\pi \\cdot r\\).', rueck: {
          hoehe: 'Das ist die Höhe des Streifens: so lang wie der Radius \\(r\\). Der halbe Umfang ist länger.',
          durchmesser: 'Das ist der Durchmesser \\(d = 2r\\). Er passt rund \\(3.14\\)-mal in den ganzen Umfang — der halbe Umfang ist also länger.' } } },
      { text: 'Halbiere den Radius. Was geschieht mit der Höhe, der Breite und der Fläche des Streifens?', labels: true, probe: { r: 1.5 }, ziel: function(w){ return gleich(w.r, 1.5); } },
      { text: '\\(r = 3.5\\,\\text{cm}\\). Berechne Umfang und Fläche des Kreises.', labels: true, lab: 'r = 3.5 cm', setup: function(s){ s.setze({ r: 3.5, n: 24 }); s.sperre('r', 'n'); },
        gegeben: '\\(r = 3.5\\,\\text{cm}\\)', gesucht: '\\(U\\) und \\(A\\)',
        frage: [{ name: 'U', label: '\\(U \\approx\\)', einheit: 'cm', soll: 21.99, fehler: [[11.00, 'Das ist der halbe Umfang \\(\\pi r\\) — die Breite des Streifens. Der ganze Umfang ist \\(2\\pi r\\).'], [38.48, 'Das ist die Fläche. Der Umfang ist \\(2\\pi r\\).'], [21, PI3]], tipp: '\\(U = 2\\pi r\\).' },
                { name: 'A', label: '\\(A \\approx\\)', einheit: 'cm²', soll: 38.48, fehler: [[21.99, 'Das ist der Umfang. Die Fläche ist \\(\\pi r^2\\).'], [153.94, 'In \\(\\pi r^2\\) gehört der Radius, nicht der Durchmesser.'], [36.75, PI3]], tipp: '\\(A = \\pi r^2\\).' }] },
      { text: 'Ein Kreis hat den Umfang \\(30\\,\\text{cm}\\). Wie gross ist sein Radius?', nurKreis: true, angabe: 'U = 30 cm', verdeckt: ['r'], ohne: ['n'], setup: function(s){ s.sperre('r', 'n'); },
        gegeben: '\\(U = 30\\,\\text{cm}\\)', gesucht: '\\(r\\)',
        frage: [{ name: 'r', label: '\\(r \\approx\\)', einheit: 'cm', soll: 4.77, fehler: [[9.55, 'Das ist der Durchmesser: \\(U = \\pi d\\). Der Radius ist die Hälfte, \\(r = \\tfrac{U}{2\\pi}\\).'], [3.09, 'Eine Wurzel braucht es nur bei der Fläche. Aus \\(U = 2\\pi r\\) folgt \\(r = \\tfrac{U}{2\\pi}\\).'], [5, PI3]], tipp: '\\(U = 2\\pi r\\) nach \\(r\\) auflösen.' }] },
      { text: 'Ein Kreis hat die Fläche \\(80\\,\\text{cm}^2\\). Wie gross ist sein Radius?', nurKreis: true, angabe: 'A = 80 cm²', verdeckt: ['r'], ohne: ['n'], setup: function(s){ s.sperre('r', 'n'); },
        gegeben: '\\(A = 80\\,\\text{cm}^2\\)', gesucht: '\\(r\\)',
        frage: [{ name: 'r', label: '\\(r \\approx\\)', einheit: 'cm', soll: 5.05, fehler: [[25.46, 'Das ist \\(r^2\\). Zum Schluss die Wurzel ziehen.'], [12.73, 'Das gehört zum Umfang. Aus \\(A = \\pi r^2\\) folgt \\(r = \\sqrt{\\tfrac{A}{\\pi}}\\).'], [10.09, 'Das ist der Durchmesser. Gefragt ist der Radius.']], tipp: '\\(A = \\pi r^2\\): durch \\(\\pi\\) teilen, dann die Wurzel.' }] }
    ]
  });

  /* ---------- Kapitel 3: Bogen und Sektor ----------
     Wie Animation 7 der Themenseite (Radius und Zentriwinkel als Regler). Unterschied: Bogenlänge und Sektorfläche
     werden nicht angezeigt, sondern berechnet, auch rückwärts (Winkel aus der Fläche), und Bogen, Sehne und Radius
     werden angetippt. Startwert r = 4 cm, φ = 45° wie im Einführungsclip. Der Winkel-Regler geht in Schritten von 15°
     (25 Stellungen): So lassen sich die Zielwinkel 120° und 225° auch mit dem Finger treffen; 100° steht als `fest`. */
  arbeitsbereich('sim3', {
    fenster: { w: 320, h: 320, x0: -5.6, x1: 5.6, y0: -5.6 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, r = w.r, phi = w.phi, M = [0, 0], P1 = [r, 0], P2 = pol(M, r, grad(phi));
      F.kreis(M, r, 'figur kreis');
      if (phi > 0){ F.sektor(M, r, 0, grad(phi), 'sektor'); }
      if (phi > 0 && !k.wahl) F.sektor(M, r, 0, grad(phi), Au.rand ? 'bogen rand' : 'bogen', true);
      if (Au.rand){ F.strecke(M, P1, 'hilfe'); F.strecke(M, P2, 'hilfe'); }
      if (phi > 0 && phi < 360) winkelMarke(F, M, P1, P2, 22, 'winkelbogen', Au.lab && Au.lab.phi ? '' : 'φ');
      if (k.wahl){
        F.kandidatZug('bogen', bogenPunkte(M, r, 0, grad(phi)), k.wahl);
        F.kandidat('sehne', P1, P2, k.wahl);
        F.kandidat('radius', M, P1, k.wahl);
        if (w.richtig) F.sektor(M, r, 0, grad(phi), 'bogen', true);
      }
      F.punkt(M); F.text(M, 'M', 'ecke', -10, 4);
      var la = Au.lab || {};
      if (la.r) F.text(mitte(M, P1), la.r, 'mass', 0, 14);
      if (la.phi) F.text(pol(M, 1.45, grad(phi / 2)), la.phi, 'mass', 0, 4);
      if (la.b) F.text(pol(M, r + 0.55, grad(phi / 2)), la.b, 'mass', 0, 4);
      if (la.A) F.text(pol(M, r * 0.74, grad(phi / 2)), la.A, 'mass', 0, 4);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      var t = '\\(r = ' + z(r) + '\\,\\text{cm}\\); \\(\\varphi = ' + z(phi) + '°\\)';
      if (!k.wahl) t += '; Anteil \\(\\tfrac{\\varphi}{360°} ' + zz(phi / 360, 3) + '\\)';
      return t;
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(\\varphi\\). Welchen Anteil des Kreises nimmt der Sektor ein?', probe: { phi: 90 }, ziel: function(w){ return w.bewegt.phi; } },
      { text: 'Stell einen Drittelkreis ein.', probe: { phi: 120 }, ziel: function(w){ return gleich(w.phi, 120); } },
      { text: 'Stell einen Sektor ein, dessen Bogen \\(\\tfrac{5}{8}\\) des Umfangs ist.', probe: { phi: 225 }, ziel: function(w){ return gleich(w.phi, 225); } },
      { text: 'Tipp den Bogen des Sektors an.', fest: { phi: 100 }, setup: function(s){ s.sperre('r', 'phi'); },
        wahl: { richtig: 'bogen', gut: 'Der Bogen ist das Stück der Kreislinie zwischen den beiden Radien. Seine Länge ist \\(b\\).', rueck: {
          sehne: 'Das ist die Sehne: die gerade Verbindung der beiden Bogenenden. Der Bogen ist gekrümmt — und länger.',
          radius: 'Das ist ein Radius: Er begrenzt den Sektor seitlich.' } } },
      { text: '\\(r = 4.5\\,\\text{cm}\\), \\(\\varphi = 100°\\). Wie lang ist der Bogen?', fest: { r: 4.5, phi: 100 }, setup: function(s){ s.sperre('r', 'phi'); },
        lab: { r: 'r = 4.5 cm', phi: '100°', b: 'b = ?' }, gegeben: '\\(r = 4.5\\,\\text{cm}\\), \\(\\varphi = 100°\\)', gesucht: '\\(b\\)',
        frage: [{ name: 'b', label: '\\(b \\approx\\)', einheit: 'cm', soll: 7.85, fehler: [[28.27, 'Das ist der ganze Umfang. Der Bogen ist der Anteil \\(\\tfrac{100°}{360°}\\) davon.'], [17.67, 'Das ist die Sektorfläche. Für die Länge: \\(\\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).'], [3.93, 'Die \\(2\\) fehlt: Der Umfang ist \\(2\\pi r\\).'], [450, '\\(b = r \\cdot \\varphi\\) gilt nur im Bogenmass. Im Grad: \\(\\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).']], tipp: '\\(b = \\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).' }] },
      { text: '\\(r = 3.5\\,\\text{cm}\\), \\(\\varphi = 150°\\). Wie gross ist die Sektorfläche?', setup: function(s){ s.setze({ r: 3.5, phi: 150 }); s.sperre('r', 'phi'); },
        lab: { r: 'r = 3.5 cm', phi: '150°', A: 'A = ?' }, gegeben: '\\(r = 3.5\\,\\text{cm}\\), \\(\\varphi = 150°\\)', gesucht: '\\(A_{SK}\\)',
        frage: [{ name: 'A', label: '\\(A_{SK} \\approx\\)', einheit: 'cm²', soll: 16.04, fehler: [[38.48, 'Das ist die ganze Kreisfläche. Der Sektor ist der Anteil \\(\\tfrac{150°}{360°}\\) davon.'], [9.16, 'Das ist die Bogenlänge. Für die Fläche: \\(\\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).'], [32.07, 'Bei der Fläche gibt es keine \\(2\\): \\(\\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).']], tipp: '\\(A_{SK} = \\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).' }] },
      { text: 'Ein Sektor mit \\(r = 4.5\\,\\text{cm}\\) hat die Fläche \\(20\\,\\text{cm}^2\\). Wie gross ist sein Zentriwinkel?', fest: { r: 4.5, phi: 360 * 20 / (PI * 20.25) }, verdeckt: ['phi'], setup: function(s){ s.sperre('r', 'phi'); },
        lab: { r: 'r = 4.5 cm', phi: '?', A: 'A = 20 cm²' }, gegeben: '\\(r = 4.5\\,\\text{cm}\\), \\(A_{SK} = 20\\,\\text{cm}^2\\)', gesucht: '\\(\\varphi\\)',
        frage: [{ name: 'phi', label: '\\(\\varphi \\approx\\)', einheit: '°', soll: 113.18, tol: 0.011, fehler: [[0.31, 'Das ist der Anteil \\(\\tfrac{A_{SK}}{\\pi r^2}\\). Mal \\(360°\\) gibt den Winkel.'], [31.44, 'Das ist der Anteil in Prozent. Gesucht ist der Winkel: Anteil mal \\(360°\\).'], [254.65, 'Bei einer Fläche gehört \\(\\pi r^2\\) in den Nenner, nicht der Umfang.']], tipp: 'Anteil \\(= \\tfrac{A_{SK}}{\\pi r^2}\\), dann mal \\(360°\\).' }] },
      { text: '\\(r = 5\\,\\text{cm}\\), \\(\\varphi = 90°\\). Wie lang ist der ganze Rand des Sektors?', rand: true, setup: function(s){ s.setze({ r: 5, phi: 90 }); s.sperre('r', 'phi'); },
        lab: { r: 'r = 5 cm', phi: '90°' }, gegeben: '\\(r = 5\\,\\text{cm}\\), \\(\\varphi = 90°\\)', gesucht: 'Umfang des Sektors (orange)',
        frage: [{ name: 'U', label: '\\(U_S \\approx\\)', einheit: 'cm', soll: 17.85, fehler: [[7.85, 'Das ist nur der Bogen. Zum Rand gehören auch die beiden Radien.'], [12.85, 'Der Sektor hat zwei Radien als Seiten.'], [31.42, 'Das ist der Umfang des ganzen Kreises.']], tipp: 'Rand = Bogen \\(+ 2r\\).' }] }
    ]
  });

  /* ---------- Kapitel 4a: Segment ----------
     Wie Animation 8 der Themenseite (r und φ, Dreieck ein/aus). Unterschied: Die Segmentfläche wird nicht angezeigt,
     sondern berechnet — nur bei Winkeln, deren Dreieck ohne Trigonometrie geht (90° und 270°: rechtwinklig, 60°:
     gleichseitig); die Zeile sagt, ob das Dreieck abgezogen oder addiert wird. Startwert r = 5 cm, φ = 90° wie im
     Einführungsclip. */
  arbeitsbereich('sim4', {
    fenster: { w: 320, h: 320, x0: -6.6, x1: 6.6, y0: -6.6 },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, r = w.r, phi = w.phi, M = [0, 0], P1 = [r, 0], P2 = pol(M, r, grad(phi));
      F.kreis(M, r, 'figur kreis');
      if (phi > 0 && phi < 360){
        F.sektor(M, r, 0, grad(phi), 'sektor blass');
        F.vieleck(bogenPunkte(M, r, 0, grad(phi)), 'segment');
        if (!gleich(phi, 180)) F.vieleck([M, P1, P2], 'dreieck-seg');
        F.strecke(P1, P2, 'sehne');
        winkelMarke(F, M, P1, P2, 20, 'winkelbogen', 'φ');
      }
      if (k.wahl){
        var Fu = [P2[0], 0], Ms = mitte(P1, P2);
        F.kandidat('hoehe', Fu, P2, k.wahl); F.kandidat('lot', M, Ms, k.wahl); F.kandidat('radius', M, P2, k.wahl); F.kandidat('sehne', P1, P2, k.wahl);
        if (w.richtig){ F.strecke(Fu, P2, 'hilfe'); F.rechts(Fu, [1, 0], [0, 1], 'hilfe'); F.text(mitte(Fu, P2), 'hΔ', 'hilfe', 7, 4, 'start'); }
      }
      F.punkt(M); F.text(M, 'M', 'ecke', -10, 4);
      if (phi > 0 && phi < 360){ F.punkt(P1); F.punkt(P2); F.text(P1, 'P₁', 'ecke', 12, 4, 'start'); F.text(P2, 'P₂', 'ecke', 0, P2[1] >= 0 ? -9 : 17); }
      var la = Au.lab || {};
      if (la.r) F.text(mitte(M, P1), la.r, 'mass', 0, 14);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      var regel = phi === 0 || phi === 360 ? '' : phi < 180 ? '; \\(\\varphi \\lt 180°\\): Segment = Sektor − Dreieck'
        : gleich(phi, 180) ? '; \\(\\varphi = 180°\\): Das Dreieck hat keine Fläche, das Segment ist der Halbkreis' : '; \\(\\varphi \\gt 180°\\): Segment = Sektor + Dreieck';
      return '\\(r = ' + z(r) + '\\,\\text{cm}\\); \\(\\varphi = ' + z(phi) + '°\\)' + regel;
    },
    aufgaben: [
      { text: 'Erkunde: Zieh \\(\\varphi\\) über \\(180°\\) hinaus. Wo liegt jetzt das Dreieck \\(MP_1P_2\\)?', probe: { phi: 240 }, ziel: function(w){ return w.bewegt.phi && w.phi > 180; } },
      { text: 'Stell \\(\\varphi\\) so ein, dass das Dreieck \\(MP_1P_2\\) keine Fläche hat.', probe: { phi: 180 }, ziel: function(w){ return gleich(w.phi, 180); } },
      { text: '\\(\\varphi = 60°\\): Tipp die Höhe des Dreiecks auf die Seite \\(MP_1\\) an.', setup: function(s){ s.setze({ phi: 60 }); s.sperre('r', 'phi'); },
        wahl: { richtig: 'hoehe', gut: 'Sie steht senkrecht auf \\(MP_1\\) und geht durch \\(P_2\\). Bei \\(60°\\) ist das Dreieck gleichseitig: \\(h_\\Delta = \\sqrt{r^2 - \\left(\\tfrac{r}{2}\\right)^2}\\).', rueck: {
          lot: 'Das ist auch eine Höhe — aber auf die Sehne \\(P_1P_2\\), nicht auf \\(MP_1\\).',
          radius: 'Das ist der Radius \\(MP_2\\). Er steht nicht senkrecht auf \\(MP_1\\).',
          sehne: 'Das ist die Sehne \\(P_1P_2\\), eine Seite des Dreiecks.' } } },
      { text: '\\(r = 3.5\\,\\text{cm}\\), \\(\\varphi = 90°\\). Wie gross ist das Segment?', setup: function(s){ s.setze({ r: 3.5, phi: 90 }); s.sperre('r', 'phi'); },
        lab: { r: 'r = 3.5 cm' }, gegeben: '\\(r = 3.5\\,\\text{cm}\\), \\(\\varphi = 90°\\)', gesucht: '\\(A_{SG}\\)',
        frage: [{ name: 'A', label: '\\(A_{SG} \\approx\\)', einheit: 'cm²', soll: 3.50, fehler: [[9.62, 'Das ist der ganze Sektor. Zieh das Dreieck ab.'], [15.75, 'Unter \\(180°\\) wird das Dreieck abgezogen, nicht addiert.'], [6.13, 'Das ist das Dreieck. Gesucht ist Sektor minus Dreieck.']], tipp: 'Sektor \\(\\tfrac{90°}{360°} \\cdot \\pi r^2\\) minus das rechtwinklige Dreieck \\(\\tfrac{1}{2}\\, r \\cdot r\\).' }] },
      { text: '\\(r = 4.5\\,\\text{cm}\\), \\(\\varphi = 60°\\). Wie gross ist das Segment?', setup: function(s){ s.setze({ r: 4.5, phi: 60 }); s.sperre('r', 'phi'); },
        lab: { r: 'r = 4.5 cm' }, gegeben: '\\(r = 4.5\\,\\text{cm}\\), \\(\\varphi = 60°\\)', gesucht: '\\(A_{SG}\\)',
        frage: [{ name: 'A', label: '\\(A_{SG} \\approx\\)', einheit: 'cm²', soll: 1.83, fehler: [[10.60, 'Das ist der ganze Sektor. Zieh das Dreieck ab.'], [0.48, 'Bei \\(60°\\) ist das Dreieck nicht rechtwinklig, sondern gleichseitig: Höhe mit Pythagoras.'], [19.37, 'Unter \\(180°\\) wird das Dreieck abgezogen, nicht addiert.'], [8.77, 'Das ist das Dreieck. Gesucht ist Sektor minus Dreieck.']], tipp: 'Gleichseitiges Dreieck mit der Seite \\(4.5\\): \\(h_\\Delta = \\sqrt{4.5^2 - 2.25^2}\\).' }] },
      { text: '\\(r = 4\\,\\text{cm}\\), \\(\\varphi = 270°\\). Wie gross ist das Segment?', setup: function(s){ s.setze({ r: 4, phi: 270 }); s.sperre('r', 'phi'); },
        lab: { r: 'r = 4 cm' }, gegeben: '\\(r = 4\\,\\text{cm}\\), \\(\\varphi = 270°\\)', gesucht: '\\(A_{SG}\\)',
        frage: [{ name: 'A', label: '\\(A_{SG} \\approx\\)', einheit: 'cm²', soll: 45.70, fehler: [[29.70, 'Über \\(180°\\) liegt das Dreieck im Segment: Es wird addiert.'], [37.70, 'Das ist der Sektor. Über \\(180°\\) kommt das Dreieck dazu.']], tipp: 'Über \\(180°\\): Sektor plus Dreieck.' }] }
    ]
  });

  /* ---------- Kapitel 4b: Kreisring ----------
     Wie Animation 5 der Themenseite (R und r als Regler, r_m und b eingezeichnet). Unterschied: Die Fläche wird
     nicht angezeigt, sondern berechnet, auf beide Arten; die Ringbreite wird angetippt. r bleibt kleiner als R.
     Startwert R = 6 cm, r = 4 cm wie im Einführungsclip. */
  arbeitsbereich('sim5', {
    fenster: { w: 320, h: 320, x0: -6.6, x1: 6.6, y0: -6.6 },
    korrigiere: function(reg, p){
      var R = +reg.R.value, r = +reg.r.value;
      if (r >= R - 1e-9){ if (p === 'R') reg.r.value = Math.max(0.5, R - 0.5); else reg.r.value = R - 0.5; }
    },
    zeichnen: function(F, w, k){
      var Au = k.aufgabe || {}, R = w.R, r = w.r, M = [0, 0], rm = (R + r) / 2;
      F.ring(M, R, r, 'ringflaeche');
      F.kreis(M, R, 'figur kreis-linie'); F.kreis(M, r, 'figur kreis-linie');
      if (!k.wahl) F.kreis(M, rm, 'mittelkreis');
      var wR = grad(60), wr = grad(180), wb = grad(300);
      if (k.wahl){
        F.kandidat('b', pol(M, r, wb), pol(M, R, wb), k.wahl); F.kandidat('R', M, pol(M, R, wR), k.wahl); F.kandidat('r', M, pol(M, r, wr), k.wahl);
        if (w.richtig){ F.strecke(pol(M, r, wb), pol(M, R, wb), 'hilfe'); F.text(pol(M, rm, wb), 'b', 'hilfe', 9, 4, 'start'); }
      } else {
        var la = Au.lab || { R: 'R', r: 'r', b: 'b', rm: 'r' };
        if (la.R){ F.strecke(M, pol(M, R, wR), 'radius'); F.text(pol(M, R * 0.55, wR), la.R, 'seite', 8, 0, 'start'); }
        if (la.r){ F.strecke(M, pol(M, r, wr), 'radius'); F.text(pol(M, r / 2, wr), la.r, 'seite', 0, -6); }
        if (la.b){ F.strecke(pol(M, r, wb), pol(M, R, wb), 'hilfe'); F.text(pol(M, rm, wb), la.b, 'hilfe', 9, 4, 'start'); }
        if (la.rm){ var tr = F.text(pol(M, rm, grad(125)), la.rm, 'mittel-text', -4, -4, 'end');   // «r» mit tiefgestelltem m
          var sub = document.createElementNS(NS, 'tspan'); sub.setAttribute('dy', '3'); sub.setAttribute('font-size', '9'); sub.textContent = 'm';
          tr.appendChild(sub); var nach = document.createElementNS(NS, 'tspan'); nach.setAttribute('dy', '-3'); nach.textContent = la.rmRest || ''; tr.appendChild(nach); }
      }
      F.punkt(M); F.text(M, 'M', 'ecke', 10, 14);
      if (Au.frage) return Au.gegeben + '; gesucht: ' + Au.gesucht;
      if (k.wahl) return '\\(R = ' + z(R) + '\\,\\text{cm}\\); \\(r = ' + z(r) + '\\,\\text{cm}\\)';
      return '\\(R = ' + z(R) + '\\,\\text{cm}\\); \\(r = ' + z(r) + '\\,\\text{cm}\\); Ringbreite \\(b = R - r = ' + z(R - r) + '\\,\\text{cm}\\); mittlerer Radius \\(r_m = ' + z(rm) + '\\,\\text{cm}\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(R\\) und \\(r\\). Wovon hängt die Ringfläche ab?', probe: { R: 5 }, ziel: function(w){ return w.bewegt.R || w.bewegt.r; } },
      { text: 'Stell einen Ring ein, der \\(1\\,\\text{cm}\\) breit ist und den mittleren Radius \\(3.5\\,\\text{cm}\\) hat.', probe: { R: 4, r: 3 }, ziel: function(w){ return gleich(w.R, 4) && gleich(w.r, 3); } },
      { text: 'Tipp die Ringbreite \\(b\\) an.', setup: function(s){ s.sperre('R', 'r'); },
        wahl: { richtig: 'b', gut: '\\(b = R - r\\) ist der Abstand der beiden Kreislinien.', rueck: {
          R: 'Das ist der Aussenradius \\(R\\): von \\(M\\) bis zum äusseren Kreis.',
          r: 'Das ist der Innenradius \\(r\\): von \\(M\\) bis zum inneren Kreis.' } } },
      { text: '\\(R = 5.5\\,\\text{cm}\\), \\(r = 2.5\\,\\text{cm}\\). Wie gross ist die Ringfläche?', setup: function(s){ s.setze({ R: 5.5, r: 2.5 }); s.sperre('R', 'r'); },
        lab: { R: 'R = 5.5', r: 'r = 2.5' }, gegeben: '\\(R = 5.5\\,\\text{cm}\\), \\(r = 2.5\\,\\text{cm}\\)', gesucht: 'Ringfläche \\(A\\)',
        frage: [{ name: 'A', label: '\\(A \\approx\\)', einheit: 'cm²', soll: 75.40, fehler: [[28.27, '\\(\\pi (R - r)^2\\) ist die Fläche eines Kreises mit dem Radius \\(b\\). Der Ring ist die Differenz zweier Kreisflächen: \\(\\pi (R^2 - r^2)\\).'], [114.67, 'Die kleine Kreisfläche wird abgezogen, nicht addiert.'], [103.67, 'In \\(2\\pi r_m \\cdot b\\) gehört der mittlere Radius \\(r_m = 4\\,\\text{cm}\\), nicht \\(R\\).']], tipp: '\\(A = \\pi R^2 - \\pi r^2\\).' }] },
      { text: 'Ein Ring ist \\(2\\,\\text{cm}\\) breit, sein mittlerer Radius ist \\(4.5\\,\\text{cm}\\). Wie gross ist seine Fläche?', verdeckt: ['R', 'r'], setup: function(s){ s.setze({ R: 5.5, r: 3.5 }); s.sperre('R', 'r'); },
        lab: { b: 'b = 2', rm: 'r', rmRest: ' = 4.5' }, gegeben: '\\(b = 2\\,\\text{cm}\\), \\(r_m = 4.5\\,\\text{cm}\\)', gesucht: 'Ringfläche \\(A\\)',
        frage: [{ name: 'A', label: '\\(A \\approx\\)', einheit: 'cm²', soll: 56.55, fehler: [[28.27, 'Das ist der mittlere Umfang. Mal die Breite \\(b\\) gibt die Fläche.'], [12.57, 'Das ist ein Kreis mit dem Radius \\(b\\). Der Ring ist mittlerer Umfang mal Breite.']], tipp: '\\(A = 2\\pi r_m \\cdot b\\) — oder \\(R\\) und \\(r\\) bestimmen.' }] }
    ]
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function r2(v){ return Math.round(v * 100) / 100; }
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche ·
       Kapitelaufgaben · Gesamttest · Themenseite (Aufgaben, Animationen, Mini-Checks). Je Typ ein eigener Schlüssel. */
    var SPERRE = [
      // sehne: sh|art|r|Wert (art s: Wert = a; a: Wert = Sehne s; t: Wert = MP; h: Wert = Abstand P–Kreislinie in cm); sh|r|s|a
      'sh|s|5|3', 'sh|t|5|13', 'sh|r|9|6', 'sh|r|10|5', 'sh|s|6|2.5', 'sh|a|6|8', 'sh|t|4|8.5', 'sh|a|6.5|12', 'sh|t|6|10', 'sh|s|10|6', 'sh|t|8|17', 'sh|s|4|2.5',
      // lage: lg|r|a (r als Radius, auch wenn d gegeben ist)
      'lg|4|4', 'lg|5|6', 'lg|4.5|4.6', 'lg|4|2.5', 'lg|4|5', 'lg|3|3.6', 'lg|3|3', 'lg|3|1.8',
      // kreis: kr|r
      'kr|3', 'kr|3.5', 'kr|13', 'kr|4', 'kr|6', 'kr|5', 'kr|15',
      // zurueck: zr|U oder A|Wert|r oder d
      'zr|U|40|r', 'zr|A|50|r', 'zr|U|30|r', 'zr|A|80|r', 'zr|U|200|d', 'zr|U|50|r', 'zr|A|100|r', 'zr|U|25|r',
      // sektor: sk|r|φ
      'sk|4|45', 'sk|4.5|100', 'sk|3.5|150', 'sk|5|90', 'sk|9|120', 'sk|7|50', 'sk|10|54', 'sk|9|20', 'sk|12|135', 'sk|8|120', 'sk|3|60', 'sk|3|120', 'sk|3|70', 'sk|15|45', 'sk|5|60',
      // winkel-zurueck: wz|b oder A|r|Wert
      'wz|b|4|6', 'wz|A|4.5|20', 'wz|b|6|10', 'wz|A|7.5|50',
      // sektor-rand: sr|u|r|φ und sr|a|b|r
      'sr|u|5|90', 'sr|u|9|20', 'sr|a|8|5', 'sr|a|10|6', 'sr|u|12|135',
      // segment: sg|r|φ
      'sg|5|90', 'sg|5|60', 'sg|3.5|90', 'sg|4.5|60', 'sg|4|270', 'sg|10|90', 'sg|7|60', 'sg|3|90', 'sg|3|270', 'sg|10|60', 'sg|6|90', 'sg|4|60', 'sg|6|60', 'sg|4|90',
      // ring: rg|R|r
      'rg|6|4', 'rg|5.5|2.5', 'rg|5.5|3.5', 'rg|5.8|2.3', 'rg|7|3', 'rg|8|5', 'rg|12.5|6', 'rg|3|2', 'rg|2|1', 'rg|3.5|2.5', 'rg|5|3'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function feld(A, f, e, soll, tipp, fehler, tol){
      if (stimmt(e[f], soll, tol)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (!stimmt(fehler[j][0], soll, tol) && stimmt(e[f], r2(fehler[j][0]), tol)) return fehler[j][1];
      return nah(e[f], soll, tol) ? RUNDEN : tipp;
    }
    /* Gezielte Fehler für das Prüfwerkzeug: nur Werte, die sich vom Sollwert unterscheiden. */
    function fehlerListe(A, f, liste, tol){
      var aus = [], gesehen = [];   // gleiche Fehlwerte zweier Fehlerarten: nur die erste zählt (so prüft auch pruefen)
      liste.forEach(function(x){ if (isFinite(x[0]) && x[0] > 0 && !stimmt(r2(x[0]), A.soll, tol) && Math.abs(r2(x[0]) - A.soll) > 0.07
          && !gesehen.some(function(g){ return stimmt(r2(x[0]), g, tol); })) { gesehen.push(r2(x[0])); var o = {}; o[f] = String(r2(x[0])); aus.push([o, x[2] || null]); } });
      return aus;
    }
    function nurAndere(A, liste){ return liste.filter(function(x){ return isFinite(x[0]) && x[0] > 0 && Math.abs(r2(x[0]) - A.soll) > 0.07; }); }
    function halbe(){ var a = []; for (var i = 0; i < arguments.length; i++) a.push(arguments[i]); return a; }
    var NAMEN = ['Radius', 'Durchmesser', 'Sehne', 'Sekante', 'Tangente', 'Passante'];

    var TYPEN = {
      /* ── Kapitel 1 ── */
      /* Linie benennen: Im Bild ist eine Linie hervorgehoben (Radius, Sehne, Sekante, Tangente oder Passante) in
         zufälliger Lage. Der Durchmesser wird nie gezeichnet (er ist auch eine Sehne — die Antwort wäre doppeldeutig). */
      'linie': { felder: ['s'], muster: 'Die markierte Linie ist ein(e) {s:Radius|Durchmesser|Sehne|Sekante|Tangente|Passante}.',
        neu: function(){
          var soll = zufall(['Radius', 'Sehne', 'Sekante', 'Tangente', 'Passante']), w = Math.random() * 2 * PI, a;
          if (soll === 'Sehne') a = zufall([0.9, 1.3, 1.7, 2.1]);
          else if (soll === 'Sekante') a = zufall([0.7, 1.2, 1.8, 2.3]);
          else if (soll === 'Tangente') a = 3;
          else if (soll === 'Passante') a = zufall([3.6, 3.9]);
          return { soll: soll, w: w, a: a, text: 'Im Bild ist eine Linie am Kreis orange markiert. Wie heisst sie?' }; },
        eingabe: function(A){ return { s: A.soll }; },
        zeichne: function(svg, A){
          var F = Flaeche(svg, { w: 240, h: 240, x0: -4.5, x1: 4.5, y0: -4.5, karo: false }), M = [0, 0], r = 3;
          F.kreis(M, r, 'figur kreis'); F.punkt(M); F.text(M, 'M', 'ecke', -9, 14);
          var n = [Math.cos(A.w), Math.sin(A.w)], d = [-n[1], n[0]], f = [A.a * n[0], A.a * n[1]];
          if (A.soll === 'Radius'){ F.strecke(M, pol(M, r, A.w), 'hilfe'); F.punkt(pol(M, r, A.w), 'g-pkt hilfe'); return; }
          if (A.soll === 'Sehne'){ var q = Math.sqrt(r * r - A.a * A.a), P = [f[0] + q * d[0], f[1] + q * d[1]], Q = [f[0] - q * d[0], f[1] - q * d[1]];
            F.strecke(P, Q, 'hilfe'); F.punkt(P, 'g-pkt hilfe'); F.punkt(Q, 'g-pkt hilfe'); return; }
          F.gerade(f, [f[0] + d[0], f[1] + d[1]], 'hilfe');
          if (A.soll === 'Sekante'){ var q2 = Math.sqrt(r * r - A.a * A.a); F.punkt([f[0] + q2 * d[0], f[1] + q2 * d[1]], 'g-pkt'); F.punkt([f[0] - q2 * d[0], f[1] - q2 * d[1]], 'g-pkt'); }
          if (A.soll === 'Tangente') F.punkt(f, 'g-pkt');
        },
        fehler: function(A){ return NAMEN.filter(function(o){ return o !== A.soll; }).map(function(o){ return [{ s: o }, null]; }); },
        pruefen: function(A, e){
          var s = e.s, ist = A.soll;
          if (s === ist) return null;
          var strecke = ist === 'Radius' || ist === 'Sehne';
          if (s === 'Durchmesser') return ist === 'Radius' ? 'Ein Durchmesser geht durch \\(M\\) hindurch bis zur anderen Seite. Diese Strecke beginnt in \\(M\\).' : 'Ein Durchmesser geht durch den Mittelpunkt \\(M\\) — die markierte Linie nicht.';
          if (s === 'Radius') return 'Ein Radius beginnt im Mittelpunkt \\(M\\) — die markierte Linie nicht.';
          if (ist === 'Sehne' && s === 'Sekante') return 'Die markierte Linie endet an der Kreislinie: eine Strecke. Eine Sekante ist eine Gerade, die darüber hinausgeht.';
          if (ist === 'Sekante' && s === 'Sehne') return 'Die markierte Linie geht über den Kreis hinaus: eine Gerade. Die Sehne ist nur ihr Stück im Kreis.';
          if (ist === 'Radius' && s === 'Sehne') return 'Eine Sehne verbindet zwei Punkte der Kreislinie. Die markierte Strecke beginnt im Mittelpunkt \\(M\\).';
          if (strecke) return 'Die markierte Linie ist eine Strecke mit zwei Endpunkten — keine Gerade.';
          if (s === 'Sehne') return 'Die markierte Linie geht über den Bildrand hinaus: eine Gerade, keine Strecke.';
          return 'Zähle die gemeinsamen Punkte mit der Kreislinie: Passante keinen, Tangente genau einen, Sekante zwei.'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* Gerade und Kreis: Lage aus Abstand a und Radius (oder Durchmesser) — oder umgekehrt aus der Lage die Bedingung. */
      'lage': { felder: ['s'], muster: 'Antwort: {s:–}',
        schl: function(A){ return A.art === 'w' ? 'lg|' + A.r + '|' + A.a : null; },
        neu: function(){
          if (Math.random() < 0.3){
            var lage = zufall([['Passante', 'keinen Punkt', 'a > r'], ['Tangente', 'genau einen Punkt', 'a = r'], ['Sekante', 'zwei Punkte', 'a < r']]);
            return { art: 'b', soll: lage[2], optionen: ['a < r', 'a = r', 'a > r'], name: lage[0],
              text: 'Eine Gerade hat mit einem Kreis ' + lage[1] + ' gemeinsam. Was gilt für ihren Abstand \\(a\\) vom Mittelpunkt?' }; }
          var r = zufall([2.5, 3.5, 4.5, 5, 6, 7.5, 8, 9]), dGeg = Math.random() < 0.5, art = zufall(['p', 't', 's', 'p', 's']), a;
          if (art === 't') a = r;
          else if (art === 's') a = r2(r * zufall([0.3, 0.5, 0.7, 0.85]));
          else a = dGeg && Math.random() < 0.7 ? r2(r * zufall([1.2, 1.5, 1.8])) : r2(r + zufall([0.4, 1, 2.5]));
          var soll = a > r + 1e-9 ? 'Passante' : gleich(a, r) ? 'Tangente' : 'Sekante';
          var mitD = dGeg ? (a > 2 * r + 1e-9 ? 'Passante' : gleich(a, 2 * r) ? 'Tangente' : 'Sekante') : null;
          return { art: 'w', r: r, a: a, dGeg: dGeg, soll: soll, mitD: mitD, optionen: ['Passante', 'Tangente', 'Sekante'],
            text: 'Ein Kreis hat ' + (dGeg ? 'den Durchmesser \\(d = ' + 2 * r + '\\,\\text{cm}\\)' : 'den Radius \\(r = ' + r + '\\,\\text{cm}\\)') + '. Eine Gerade hat vom Mittelpunkt den Abstand \\(a = ' + a + '\\,\\text{cm}\\). Was für eine Gerade ist das?' }; },
        vorbereiten: function(box, A){
          var s = box.querySelector('select[data-f="s"]'); if (!s) return;
          s.innerHTML = '<option value="">?</option>' + A.optionen.map(function(o){ return '<option>' + o + '</option>'; }).join('');
        },
        eingabe: function(A){ return { s: A.soll }; },
        fehler: function(A){ return A.optionen.filter(function(o){ return o !== A.soll; }).map(function(o){
          return [{ s: o }, A.art === 'w' && A.dGeg && o === A.mitD ? 'Durchmesser' : null]; }); },
        pruefen: function(A, e){
          if (e.s === A.soll) return null;
          if (A.art === 'b') return 'Vergleiche den Abstand mit dem Radius: Ist er grösser, trifft die Gerade den Kreis nicht; ist er kleiner, schneidet sie ihn zweimal.';
          if (A.dGeg && e.s === A.mitD) return 'Du hast \\(a\\) mit dem Durchmesser verglichen. Entscheidend ist der Radius \\(r = \\tfrac{d}{2} = ' + A.r + '\\,\\text{cm}\\).';
          return 'Vergleiche \\(a\\) mit \\(r\\): \\(a \\gt r\\) Passante, \\(a = r\\) Tangente, \\(a \\lt r\\) Sekante.'; },
        gut: function(A){ return A.art === 'b' ? 'Bei einer ' + A.name + ' gilt \\(' + A.soll.replace('<', '\\lt').replace('>', '\\gt') + '\\).' : '\\(a = ' + A.a + '\\,\\text{cm}\\), \\(r = ' + A.r + '\\,\\text{cm}\\).'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* Pythagoras am Kreis: Sehne aus r und a, Abstand aus r und s, Radius aus s und a, Tangentenstrecke aus r und
         MP oder aus r und dem Abstand h des Punkts P von der Kreislinie (auch in mm: Einheiten angleichen). Mit Skizze. */
      'sehne': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return A.art === 'r' ? 'sh|r|' + A.s + '|' + A.w : 'sh|' + A.art + '|' + A.r + '|' + A.w; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['s', 'a', 't', 'r', 'h']), r = zufall([4, 5, 6, 6.5, 7.5, 8, 9, 10, 12]), w, soll, falsch, text;
          if (art === 'r'){ var sr = zufall([6, 8, 9, 10, 12, 14, 16]); w = zufall([2, 2.5, 3, 4, 5, 6, 7.5]);
            r = Math.sqrt(sr * sr / 4 + w * w); soll = r;
            falsch = [[Math.sqrt(sr * sr + w * w), 'Im rechtwinkligen Dreieck liegt die <b>halbe</b> Sehne, \\(' + r2(sr / 2) + '\\,\\text{cm}\\).', 'halbe'],
                      [sr / 2 + w, 'Pythagoras rechnet mit Quadraten: \\(r^2 = \\left(\\tfrac{s}{2}\\right)^2 + a^2\\).', 'Quadraten'],
                      [Math.sqrt(Math.abs(sr * sr / 4 - w * w)), 'Der Radius ist die Hypotenuse: Die Quadrate werden addiert, nicht subtrahiert.', 'addiert'],
                      [2 * r, 'Das ist der Durchmesser. Gefragt ist der Radius.', 'Durchmesser']];
            text = 'In einem Kreis ist eine Sehne \\(s = ' + sr + '\\,\\text{cm}\\) lang und hat vom Mittelpunkt den Abstand \\(a = ' + w + '\\,\\text{cm}\\). Wie gross ist der Radius \\(r\\)?';
            return { art: art, r: r, s: sr, w: w, soll: r2(soll), falsch: falsch, text: text }; }
          if (art === 'h'){   // P liegt h ausserhalb der Kreislinie: MP = r + h; nie r = 2h (dort ist √(r² + h²) zufällig richtig)
            w = zufall([0.5, 1, 1.5, 2, 2.5, 3, 4, 5].filter(function(v){ return !gleich(r, 2 * v); }));
            var mm = (w % 1 !== 0 || Math.random() < 0.3), mp = r + w;
            soll = Math.sqrt(mp * mp - r * r);
            falsch = [[Math.sqrt(mp * mp + r * r), 'Der rechte Winkel liegt beim Berührpunkt \\(B\\): \\(\\overline{MP}\\) ist die Hypotenuse.', 'Hypotenuse'],
                      [Math.sqrt(r * r + w * w), 'Die Hypotenuse ist \\(\\overline{MP} = r + h\\) — von \\(M\\) bis \\(P\\), nicht nur das Stück ausserhalb des Kreises.', 'MP'],
                      [w, 'Das ist der Abstand von \\(P\\) zur Kreislinie, nicht die Tangentenstrecke.', 'Abstand']];
            if (mm) falsch.push([Math.sqrt(Math.pow(r + 10 * w, 2) - r * r), 'Einheiten angleichen: \\(' + r2(10 * w) + '\\,\\text{mm} = ' + w + '\\,\\text{cm}\\).', 'Einheiten']);
            text = 'Ein Punkt \\(P\\) liegt \\(' + (mm ? r2(10 * w) + '\\,\\text{mm}' : w + '\\,\\text{cm}') + '\\) ausserhalb eines Kreises mit \\(r = ' + r + '\\,\\text{cm}\\) — so weit ist er von der Kreislinie entfernt. Von \\(P\\) aus berührt eine Tangente den Kreis in \\(B\\). Wie lang ist \\(\\overline{PB}\\)?';
            return { art: art, r: r, w: w, mp: mp, mm: mm, soll: r2(soll), falsch: falsch, text: text }; }
          if (art === 's'){ w = zufall([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7].filter(function(v){ return v < r - 0.4; }));
            soll = 2 * Math.sqrt(r * r - w * w);
            falsch = [[soll / 2, 'Das ist die halbe Sehne. Das Lot von \\(M\\) halbiert die Sehne — verdopple.', 'halbe'],
                      [2 * Math.sqrt(r * r + w * w), 'Im rechtwinkligen Dreieck ist \\(r\\) die Hypotenuse: minus statt plus.', 'Hypotenuse'],
                      [2 * (r - w), 'Pythagoras rechnet mit Quadraten: \\(\\left(\\tfrac{s}{2}\\right)^2 = r^2 - a^2\\).', 'Quadraten']];
            text = 'Ein Kreis hat den Radius \\(r = ' + r + '\\,\\text{cm}\\). Eine Sehne hat vom Mittelpunkt den Abstand \\(a = ' + w + '\\,\\text{cm}\\). Wie lang ist die Sehne?'; }
          else if (art === 'a'){ w = zufall([3, 4, 5, 6, 7, 8, 9, 10, 11, 14].filter(function(v){ return v < 2 * r - 0.8; }));
            soll = Math.sqrt(r * r - w * w / 4);
            falsch = [[Math.sqrt(r * r + w * w / 4), 'Im rechtwinkligen Dreieck ist \\(r\\) die Hypotenuse: \\(a^2 = r^2 - \\left(\\tfrac{s}{2}\\right)^2\\).', 'Hypotenuse'],
                      [w > r ? Math.sqrt(w * w - r * r) : Math.sqrt(r * r - w * w), 'Im Dreieck liegt die <b>halbe</b> Sehne, \\(' + r2(w / 2) + '\\,\\text{cm}\\).', 'halbe'],
                      [r - w / 2, 'Pythagoras rechnet mit Quadraten: \\(a^2 + \\left(\\tfrac{s}{2}\\right)^2 = r^2\\).', 'Quadraten']];
            text = 'In einem Kreis mit dem Radius \\(r = ' + r + '\\,\\text{cm}\\) ist eine Sehne \\(s = ' + w + '\\,\\text{cm}\\) lang. Wie weit ist sie vom Mittelpunkt entfernt?'; }
          else { w = r2(r + zufall([1, 2, 2.5, 3, 4, 5, 6, 8]));
            soll = Math.sqrt(w * w - r * r);
            falsch = [[Math.sqrt(w * w + r * r), 'Der rechte Winkel liegt beim Berührpunkt \\(B\\): \\(\\overline{MP}\\) ist die Hypotenuse.', 'Hypotenuse'],
                      [w - r, 'Das ist der Abstand von \\(P\\) zur Kreislinie, nicht die Tangentenstrecke.', 'Abstand']];
            text = 'Ein Punkt \\(P\\) liegt \\(' + w + '\\,\\text{cm}\\) vom Mittelpunkt eines Kreises mit \\(r = ' + r + '\\,\\text{cm}\\) entfernt. Von \\(P\\) aus berührt eine Tangente den Kreis in \\(B\\). Wie lang ist \\(\\overline{PB}\\)?'; }
          return { art: art, r: r, w: w, mp: art === 't' ? w : null, soll: r2(soll), falsch: falsch, text: text }; },
        zeichne: function(svg, A){
          var F = Flaeche(svg, { w: 240, h: 200, x0: -3.6, x1: 6.2, y0: -3.6, karo: false }), M = [0, 0], k = 2.8 / A.r;
          F.kreis(M, 2.8, 'figur kreis'); F.punkt(M); F.text(M, 'M', 'ecke', -9, 14);
          if (A.art === 't' || A.art === 'h'){
            // massstäblich: Kreis kleiner zeichnen, wenn P sonst aus dem Bild fiele
            var kt = Math.min(k, 5.8 / A.mp), rt = A.r * kt, mp = A.mp * kt, th = Math.acos(rt / mp), B = pol(M, rt, th), P = [mp, 0];
            F.leeren(); F.kreis(M, rt, 'figur kreis'); F.punkt(M); F.text(M, 'M', 'ecke', -9, 14);
            F.strecke(M, P, 'hilfe2'); F.strecke(M, B, 'radius'); F.strecke(B, P, 'hilfe'); F.rechts(B, [-B[0], -B[1]], [P[0] - B[0], P[1] - B[1]], '');
            F.punkt(P); F.punkt(B); F.text(P, 'P', 'ecke', 0, 15); F.text(B, 'B', 'ecke', -2, -8);
            F.text(mitte(M, B), 'r', 'seite', -6, 0, 'end'); F.text(mitte(B, P), '?', 'mass ergebnis-gross', 6, -6, 'start');
            if (A.art === 'h'){ F.strecke([rt, 0], P, 'hilfe'); F.text(mitte([rt, 0], P), 'h', 'seite', 0, -6); }
            return; }
          var a = (A.art === 's' || A.art === 'r' ? A.w : Math.sqrt(A.r * A.r - A.w * A.w / 4)) * k, q = Math.sqrt(Math.max(0, 2.8 * 2.8 - a * a));
          F.strecke([-q, a], [q, a], 'hilfe'); F.strecke(M, [0, a], 'lot'); F.strecke(M, [q, a], 'radius');
          if (a > 0.3) F.rechts([0, a], [1, 0], [0, -1], '');
          F.text([0, a / 2], A.art === 'a' ? 'a = ?' : 'a', 'seite', -5, 4, 'end'); F.text(mitte(M, [q, a]), A.art === 'r' ? 'r = ?' : 'r', 'seite', 7, 8, 'start');
          F.text([0, a], A.art === 's' ? 's = ?' : 's', 'seite', 0, -8);
        },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, 'Such das rechtwinklige Dreieck: Wo liegt der rechte Winkel, welche Strecke ist die Hypotenuse?', nurAndere(A, A.falsch)); },
        loesung: function(A){ if (A.art === 'r') return 'r = \\sqrt{' + r2(A.s / 2) + '^2 + ' + A.w + '^2} \\approx ' + A.soll + '\\,\\text{cm}';
          if (A.art === 'h') return '\\overline{MP} = ' + A.r + ' + ' + A.w + ' = ' + r2(A.mp) + '\\,\\text{cm};\\ \\overline{PB} = \\sqrt{' + r2(A.mp) + '^2 - ' + A.r + '^2} \\approx ' + A.soll + '\\,\\text{cm}';
          return A.art === 's' ? 's = 2\\sqrt{' + A.r + '^2 - ' + A.w + '^2} \\approx ' + A.soll + '\\,\\text{cm}'
          : A.art === 'a' ? 'a = \\sqrt{' + A.r + '^2 - ' + r2(A.w / 2) + '^2} \\approx ' + A.soll + '\\,\\text{cm}' : '\\overline{PB} = \\sqrt{' + A.w + '^2 - ' + A.r + '^2} \\approx ' + A.soll + '\\,\\text{cm}'; } },

      /* ── Kapitel 2 ── */
      'kreis': { felder: ['U', 'A'], muster: 'U ≈ {U} cm; A ≈ {A} cm²',
        schl: function(A){ return 'kr|' + A.r; },
        eingabe: function(A){ return { U: String(r2(2 * PI * A.r)), A: String(r2(PI * A.r * A.r)) }; },
        neu: function(){
          var r = zufall([1.5, 2.5, 4.5, 5.5, 6.5, 7, 7.5, 8, 9, 10, 12, 14]), d = Math.random() < 0.45;   // nie r = 2: dort ist 2πr = πr²
          return { r: r, d: d, text: d ? 'Ein Kreis hat den Durchmesser \\(d = ' + 2 * r + '\\,\\text{cm}\\). Berechne Umfang und Fläche.' : 'Ein Kreis hat den Radius \\(r = ' + r + '\\,\\text{cm}\\). Berechne Umfang und Fläche.' }; },
        fehler: function(A){ var f = []; if (A.d) f.push([{ U: String(r2(2 * PI * A.r)), A: String(r2(PI * 4 * A.r * A.r)) }, 'Radius']); f.push([{ U: String(r2(PI * A.r * A.r)), A: String(r2(PI * A.r * A.r)) }, 'Fläche']); return f; },
        pruefen: function(A, e){
          var r = [], U = 2 * PI * A.r, F = PI * A.r * A.r;
          var f1 = feld(A, 'U', e, r2(U), '\\(U = 2\\pi r = \\pi d\\).', [[PI * A.r, 'Das ist der halbe Umfang \\(\\pi r\\). Der Umfang ist \\(2\\pi r\\) — oder \\(\\pi d\\).'], [F, 'Das ist die Fläche — der Umfang ist \\(2\\pi r\\).'], [4 * PI * A.r, 'Mit dem Durchmesser statt dem Radius: \\(2\\pi r = \\pi d\\).']]);
          var f2 = feld(A, 'A', e, r2(F), '\\(A = \\pi r^2\\).', [[PI * 4 * A.r * A.r, 'In \\(\\pi r^2\\) gehört der <b>Radius</b> — der halbe Durchmesser.'], [2 * PI * A.r, 'Das ist der Umfang — die Fläche ist \\(\\pi r^2\\).'], [Math.pow(PI * A.r, 2), '\\(\\pi r^2\\): nur \\(r\\) wird quadriert, nicht \\(\\pi\\).']]);
          if (f1) r.push('Umfang: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'U = 2\\pi \\cdot ' + A.r + ' \\approx ' + r2(2 * PI * A.r) + '\\,\\text{cm};\\ A = \\pi \\cdot ' + A.r + '^2 \\approx ' + r2(PI * A.r * A.r) + '\\,\\text{cm}^2'; } },

      /* Rückwärts: Radius oder Durchmesser aus dem Umfang oder der Fläche. */
      'zurueck': { felder: ['x'], muster: '{gross} ≈ {x} cm',
        schl: function(A){ return 'zr|' + A.art + '|' + A.wert + '|' + A.ges; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = zufall(['U', 'A']), ges = Math.random() < 0.7 ? 'r' : 'd', wert, r, falsch;
          if (art === 'U'){ wert = zufall([12, 15, 18, 20, 24, 35, 45, 60, 75, 100]); r = wert / (2 * PI);
            falsch = [[ges === 'r' ? wert / PI : wert / (2 * PI), ges === 'r' ? 'Das ist der Durchmesser: \\(U = \\pi d\\). Der Radius ist die Hälfte.' : 'Das ist der Radius. Der Durchmesser ist doppelt so lang: \\(d = \\tfrac{U}{\\pi}\\).', ges === 'r' ? 'Durchmesser' : 'Radius'],
                      [(ges === 'r' ? 1 : 2) * Math.sqrt(wert / PI), 'Eine Wurzel braucht es nur bei der Fläche. Aus \\(U = 2\\pi r\\) folgt ' + (ges === 'r' ? '\\(r = \\tfrac{U}{2\\pi}\\).' : '\\(d = \\tfrac{U}{\\pi}\\).'), 'Wurzel']]; }
          else { wert = zufall([10, 20, 30, 40, 60, 75, 120, 150, 200, 250]); r = Math.sqrt(wert / PI);
            falsch = [[(ges === 'r' ? 1 : 2) * wert / PI, 'Zum Schluss die Wurzel ziehen: \\(r = \\sqrt{\\tfrac{A}{\\pi}}\\)' + (ges === 'r' ? '.' : ', dann \\(d = 2r\\).'), 'Wurzel'],
                      [ges === 'r' ? 2 * r : r, ges === 'r' ? 'Das ist der Durchmesser. Gefragt ist der Radius.' : 'Das ist der Radius. Der Durchmesser ist doppelt so lang.', ges === 'r' ? 'Durchmesser' : 'Radius'],
                      [ges === 'r' ? wert / (2 * PI) : wert / PI / 2, 'Mit der Fläche wird nicht wie mit dem Umfang gerechnet: Aus \\(A = \\pi r^2\\) folgt \\(r = \\sqrt{\\tfrac{A}{\\pi}}\\).', 'Umfang']]; }
          var soll = ges === 'r' ? r : 2 * r;
          return { art: art, wert: wert, ges: ges, soll: r2(soll), falsch: falsch,
            text: 'Ein Kreis hat ' + (art === 'U' ? 'den Umfang \\(U = ' + wert + '\\,\\text{cm}\\)' : 'die Fläche \\(A = ' + wert + '\\,\\text{cm}^2\\)') + '. Wie gross ist sein ' + (ges === 'r' ? 'Radius \\(r\\)' : 'Durchmesser \\(d\\)') + '?' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{gross}', A.ges); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.art === 'U' ? '\\(U = 2\\pi r\\) nach \\(r\\) auflösen.' : '\\(A = \\pi r^2\\): durch \\(\\pi\\) teilen, dann die Wurzel.', nurAndere(A, A.falsch)); },
        loesung: function(A){ var r = A.art === 'U' ? '\\tfrac{' + A.wert + '}{2\\pi}' : '\\sqrt{\\tfrac{' + A.wert + '}{\\pi}}';
          return (A.ges === 'r' ? 'r = ' + r : 'd = 2r = 2 \\cdot ' + r) + ' \\approx ' + A.soll + '\\,\\text{cm}'; } },

      /* Sachaufgabe Rad: Weg aus Umdrehungen oder Umdrehungen aus dem Weg. Velo- und Rollstuhlräder. */
      'rad': { felder: ['x'], muster: '{x} {einh}',
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var rad = zufall([['Ein Velorad', 0.7], ['Ein Velorad', 0.66], ['Ein Kindervelorad', 0.5], ['Ein Rollstuhlrad', 0.6], ['Ein Trottinettrad', 0.2]]), d = rad[1], U = PI * d;
          if (Math.random() < 0.5){ var N = zufall([100, 150, 250, 400, 500, 800, 1000]);
            return { art: 'weg', d: d, N: N, soll: r2(N * U), einh: 'm', falsch: [[N * 2 * PI * d, 'Der Umfang ist \\(\\pi \\cdot d\\) — mit dem Durchmesser, nicht \\(2\\pi \\cdot d\\).', 'Durchmesser'], [N * PI * d / 2, 'Das ist \\(\\pi \\cdot r\\), der halbe Umfang. Ein Rad legt je Umdrehung \\(\\pi \\cdot d\\) zurück.', 'halbe'], [N * PI * d * 100, 'Gefragt ist der Weg in Metern.', 'Metern']],
              text: rad[0] + ' hat den Durchmesser \\(' + Math.round(d * 100) + '\\,\\text{cm}\\). Wie weit rollt es bei \\(' + N + '\\) Umdrehungen (in Metern)?' }; }
          var s = zufall([100, 200, 500, 1000, 1500, 2000]);
          return { art: 'n', d: d, s: s, soll: r2(s / U), einh: 'Umdrehungen', falsch: [[s / (2 * PI * d), 'Der Umfang ist \\(\\pi \\cdot d\\) — mit dem Durchmesser, nicht \\(2\\pi \\cdot d\\).', 'Durchmesser'], [s / (PI * d / 2), 'Je Umdrehung legt das Rad den ganzen Umfang \\(\\pi \\cdot d\\) zurück, nicht \\(\\pi \\cdot r\\).', 'ganzen'], [s * U, 'Weg geteilt durch den Umfang, nicht mal.', 'geteilt'], [s / (PI * d * 100), 'Einheiten angleichen: \\(' + Math.round(d * 100) + '\\,\\text{cm} = ' + d + '\\,\\text{m}\\).', 'Einheiten']],
            text: rad[0] + ' hat den Durchmesser \\(' + Math.round(d * 100) + '\\,\\text{cm}\\). Wie viele Umdrehungen macht es auf \\(' + s + '\\,\\text{m}\\)? (auf zwei Dezimalen)' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, 'Je Umdrehung rollt das Rad seinen Umfang \\(U = \\pi \\cdot d\\) ab (in Metern).', nurAndere(A, A.falsch)); },
        loesung: function(A){ return A.art === 'weg' ? A.N + ' \\cdot \\pi \\cdot ' + A.d + '\\,\\text{m} \\approx ' + A.soll + '\\,\\text{m}' : '\\tfrac{' + A.s + '}{\\pi \\cdot ' + A.d + '} \\approx ' + A.soll; } },

      /* ── Kapitel 3 ── */
      'sektor': { felder: ['b', 'A'], muster: 'b ≈ {b} cm; A ≈ {A} cm²',
        schl: function(A){ return 'sk|' + A.r + '|' + A.phi; },
        eingabe: function(A){ return { b: String(r2(A.phi / 360 * 2 * PI * A.r)), A: String(r2(A.phi / 360 * PI * A.r * A.r)) }; },
        neu: function(){
          var r = zufall([3, 4, 5, 6, 7, 8, 10, 2.5, 4.5, 5.5]), phi = zufall([24, 30, 40, 45, 60, 72, 80, 100, 135, 150, 210, 240, 270, 300]);
          return { r: r, phi: phi, text: 'Kreissektor mit \\(r = ' + r + '\\,\\text{cm}\\) und \\(\\varphi = ' + phi + '°\\). Berechne Bogenlänge und Sektorfläche.' }; },
        fehler: function(A){ return [[{ b: String(r2(2 * PI * A.r)), A: String(r2(A.phi / 360 * PI * A.r * A.r)) }, 'Anteil'], [{ b: String(r2(A.phi / 360 * 2 * PI * A.r)), A: String(r2(PI * A.r * A.r)) }, 'Anteil']]; },
        pruefen: function(A, e){
          var r = [], q = A.phi / 360, b = q * 2 * PI * A.r, F = q * PI * A.r * A.r;
          var f1 = feld(A, 'b', e, r2(b), '\\(b = \\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).', [[2 * PI * A.r, 'Das ist der ganze Umfang — der Bogen ist nur der Anteil \\(\\tfrac{' + A.phi + '°}{360°}\\).'], [F, 'Das ist die Fläche.'], [q * PI * A.r, 'Die \\(2\\) fehlt: Der Umfang ist \\(2\\pi r\\).']]);
          var f2 = feld(A, 'A', e, r2(F), '\\(A_{SK} = \\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).', [[PI * A.r * A.r, 'Das ist die ganze Kreisfläche — der Sektor ist der Anteil \\(\\tfrac{' + A.phi + '°}{360°}\\).'], [b, 'Das ist die Bogenlänge.'], [2 * F, 'Bei der Fläche gibt es keine \\(2\\).']]);
          if (f1) r.push('Bogen: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'b \\approx ' + r2(A.phi / 360 * 2 * PI * A.r) + '\\,\\text{cm};\\ A_{SK} \\approx ' + r2(A.phi / 360 * PI * A.r * A.r) + '\\,\\text{cm}^2'; } },

      /* Zentriwinkel aus Bogenlänge oder Sektorfläche. */
      'winkel-zurueck': { felder: ['x'], muster: 'φ ≈ {x} °',
        schl: function(A){ return 'wz|' + A.art + '|' + A.r + '|' + A.wert; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var art = Math.random() < 0.5 ? 'b' : 'A', r = zufall([3, 4, 5, 6, 7.5, 8, 10]), wert, voll, q;
          if (art === 'b'){ voll = 2 * PI * r; wert = zufall([3, 4, 5, 6, 7.5, 9, 10, 12, 15, 20].filter(function(v){ return v / voll > 0.06 && v / voll < 0.94; })); }
          else { voll = PI * r * r; wert = zufall([5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100, 150].filter(function(v){ return v / voll > 0.06 && v / voll < 0.94; })); }
          q = wert / voll;
          var falsch = [[q, 'Das ist der Anteil \\(' + (art === 'b' ? '\\tfrac{b}{2\\pi r}' : '\\tfrac{A_{SK}}{\\pi r^2}') + '\\). Mal \\(360°\\) gibt den Winkel.', 'Anteil'],
                        [q * 100, 'Das ist der Anteil in Prozent. Gesucht ist der Winkel: Anteil mal \\(360°\\).', 'Prozent'],
                        [art === 'b' ? wert / (PI * r * r) * 360 : wert / (2 * PI * r) * 360, art === 'b' ? 'Ein Bogen ist ein Stück des <b>Umfangs</b> \\(2\\pi r\\), nicht der Fläche.' : 'Eine Sektorfläche ist ein Stück der <b>Kreisfläche</b> \\(\\pi r^2\\), nicht des Umfangs.', art === 'b' ? 'Umfangs' : 'Kreisfläche']];
          return { art: art, r: r, wert: wert, soll: r2(q * 360), falsch: falsch,
            text: 'Ein Sektor mit \\(r = ' + r + '\\,\\text{cm}\\) hat ' + (art === 'b' ? 'den Bogen \\(b = ' + wert + '\\,\\text{cm}\\)' : 'die Fläche \\(A_{SK} = ' + wert + '\\,\\text{cm}^2\\)') + '. Wie gross ist sein Zentriwinkel \\(\\varphi\\)?' }; },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch, 0.011); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, 'Zuerst der Anteil am ganzen Kreis, dann mal \\(360°\\).', nurAndere(A, A.falsch), 0.011); },
        loesung: function(A){ return '\\varphi = \\tfrac{' + A.wert + '}{' + (A.art === 'b' ? '2\\pi \\cdot ' + A.r : '\\pi \\cdot ' + A.r + '^2') + '} \\cdot 360° \\approx ' + A.soll + '°'; } },

      /* Rand und Fläche eines Sektors: Umfang b + 2r aus r und φ, Fläche ½ b r aus Bogen und Radius. */
      'sektor-rand': { felder: ['x'], muster: '{gross} ≈ {x} {einh}',
        schl: function(A){ return A.art === 'u' ? 'sr|u|' + A.r + '|' + A.phi : 'sr|a|' + A.b + '|' + A.r; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var r = zufall([3, 4, 5, 6, 7.5, 8, 10, 12]);
          if (Math.random() < 0.5){ var phi = zufall([30, 45, 60, 72, 90, 120, 150, 210, 240]), b = phi / 360 * 2 * PI * r;
            return { art: 'u', r: r, phi: phi, soll: r2(b + 2 * r), gross: 'U_S', einh: 'cm',
              falsch: [[b, 'Das ist nur der Bogen. Zum Rand gehören auch die beiden Radien.', 'Bogen'], [b + r, 'Der Sektor hat <b>zwei</b> Radien als Seiten.', 'zwei'], [2 * PI * r, 'Das ist der Umfang des ganzen Kreises.', 'ganzen']],
              text: 'Ein Sektor hat \\(r = ' + r + '\\,\\text{cm}\\) und \\(\\varphi = ' + phi + '°\\). Wie lang ist sein ganzer Rand (Bogen und beide Radien)?' }; }
          var bb = zufall([4, 5, 6, 7, 9, 10, 12, 15].filter(function(v){ return v < 2 * PI * r * 0.9; }));
          return { art: 'a', r: r, b: bb, soll: r2(bb * r / 2), gross: 'A_SK', einh: 'cm²',
            falsch: [[bb * r, 'Die Hälfte fehlt: \\(A_{SK} = \\tfrac{1}{2}\\, b \\cdot r\\), wie beim Dreieck.', 'Hälfte'], [bb * r * r / 2, 'Nur einmal \\(r\\): \\(A_{SK} = \\tfrac{1}{2}\\, b \\cdot r\\).', 'einmal']],
            text: 'Ein Sektor mit \\(r = ' + r + '\\,\\text{cm}\\) hat den Bogen \\(b = ' + bb + '\\,\\text{cm}\\). Wie gross ist seine Fläche? (Den Winkel brauchst du nicht.)' }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); e.innerHTML = e.innerHTML.replace('{gross}', A.gross).replace('{einh}', A.einh); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.art === 'u' ? 'Rand = Bogen \\(+ 2r\\), Bogen \\(= \\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).' : '\\(A_{SK} = \\tfrac{1}{2}\\, b \\cdot r\\).', nurAndere(A, A.falsch)); },
        loesung: function(A){ return A.art === 'u' ? 'U_S = \\tfrac{' + A.phi + '°}{360°} \\cdot 2\\pi \\cdot ' + A.r + ' + 2 \\cdot ' + A.r + ' \\approx ' + A.soll + '\\,\\text{cm}' : 'A_{SK} = \\tfrac{1}{2} \\cdot ' + A.b + ' \\cdot ' + A.r + ' = ' + A.soll + '\\,\\text{cm}^2'; } },

      /* ── Kapitel 4 ── */
      /* Segment bei 60°, 90°, 270°, 300°: Dreieck rechtwinklig oder gleichseitig, über 180° addiert. Mit Bild. */
      'segment': { felder: ['x'], muster: 'A_SG ≈ {x} cm²',
        schl: function(A){ return 'sg|' + A.r + '|' + A.phi; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var r = zufall([2.5, 3, 4, 5, 5.5, 6, 7, 8, 9, 10]), phi = zufall([60, 90, 90, 270, 300]);
          var sek = phi / 360 * PI * r * r, recht = phi === 90 || phi === 270, dr = recht ? r * r / 2 : r / 2 * Math.sqrt(r * r - r * r / 4), klein = phi < 180;
          var soll = klein ? sek - dr : sek + dr;
          var falsch = [[sek, 'Das ist der ganze Sektor. Das Dreieck ' + (klein ? 'wird abgezogen.' : 'kommt dazu.'), 'Sektor'],
                        [klein ? sek + dr : sek - dr, klein ? 'Unter \\(180°\\) wird das Dreieck abgezogen, nicht addiert.' : 'Über \\(180°\\) liegt das Dreieck im Segment: Es wird addiert.', klein ? 'abgezogen' : 'addiert'],
                        [klein ? sek - (recht ? r * r : r * r / 2) : sek + (recht ? r * r : r * r / 2), recht ? 'Das Dreieck ist ein halbes Quadrat: \\(\\tfrac{1}{2}\\, r \\cdot r\\).' : 'Das Dreieck ist gleichseitig, nicht rechtwinklig: Höhe \\(\\sqrt{r^2 - \\left(\\tfrac{r}{2}\\right)^2}\\) mit Pythagoras.', recht ? 'halbes' : 'gleichseitig']];
          return { r: r, phi: phi, soll: r2(soll), falsch: falsch, recht: recht, klein: klein,
            text: 'Kreis mit \\(r = ' + r + '\\,\\text{cm}\\). Die Sehne \\(P_1P_2\\) gehört zum Zentriwinkel \\(\\varphi = ' + phi + '°\\). Berechne die Fläche des grünen Segments.' }; },
        zeichne: function(svg, A){
          var F = Flaeche(svg, { w: 220, h: 220, x0: -3.8, x1: 3.8, y0: -3.8, karo: false }), M = [0, 0], r = 3, P2 = pol(M, r, grad(A.phi));
          F.kreis(M, r, 'figur kreis');
          F.vieleck(bogenPunkte(M, r, 0, grad(A.phi)), 'segment');
          F.vieleck([M, [r, 0], P2], 'dreieck-seg'); F.strecke([r, 0], P2, 'sehne');
          winkelMarke(F, M, [r, 0], P2, 16, 'winkelbogen', A.phi + '°', 'winkel klein');
          F.punkt(M); F.text(M, 'M', 'ecke', -9, 14); F.text([r, 0], 'P₁', 'ecke', 10, 4, 'start'); F.text(P2, 'P₂', 'ecke', 0, P2[1] >= 0 ? -8 : 16);
        },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, (A.klein ? 'Sektor minus Dreieck' : 'Sektor plus Dreieck') + '; das Dreieck ist ' + (A.recht ? 'rechtwinklig mit den Katheten \\(r\\).' : 'gleichseitig mit der Seite \\(r\\).'), nurAndere(A, A.falsch)); },
        loesung: function(A){ var d = A.recht ? '\\tfrac{1}{2} \\cdot ' + A.r + '^2' : '\\tfrac{1}{2} \\cdot ' + A.r + ' \\cdot \\sqrt{' + A.r + '^2 - ' + r2(A.r / 2) + '^2}';
          return '\\tfrac{' + A.phi + '°}{360°} \\cdot \\pi \\cdot ' + A.r + '^2 ' + (A.klein ? '-' : '+') + ' ' + d + ' \\approx ' + A.soll + '\\,\\text{cm}^2'; } },

      /* Kreisring aus R und r, aus den Durchmessern, aus r und der Breite b oder aus r_m und b. */
      'ring': { felder: ['x'], muster: 'A ≈ {x} cm²',
        schl: function(A){ return 'rg|' + A.R + '|' + A.r; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var r = zufall([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7]), b = zufall([0.5, 1, 1.5, 2, 2.5, 3, 4]), R = r2(r + b), art = zufall(['Rr', 'dd', 'rb', 'mb']), rm = r2((R + r) / 2);
          var soll = PI * (R * R - r * r), text;
          var falsch = [[PI * b * b, '\\(\\pi (R - r)^2\\) ist ein Kreis mit dem Radius \\(b\\). Der Ring ist die Differenz zweier Kreisflächen.', 'Differenz'],
                        [PI * (R * R + r * r), 'Die kleine Kreisfläche wird abgezogen, nicht addiert.', 'abgezogen']];
          if (art === 'Rr') text = 'Ein Kreisring hat den Aussenradius \\(R = ' + R + '\\,\\text{cm}\\) und den Innenradius \\(r = ' + r + '\\,\\text{cm}\\). Wie gross ist seine Fläche?';
          if (art === 'dd'){ text = 'Ein Rohr hat aussen den Durchmesser \\(' + r2(2 * R) + '\\,\\text{cm}\\), innen den Durchmesser \\(' + r2(2 * r) + '\\,\\text{cm}\\). Wie gross ist seine Querschnittsfläche (der Kreisring)?';
            falsch.push([4 * soll, 'In \\(\\pi R^2\\) gehören die Radien, nicht die Durchmesser.', 'Radien']); }
          if (art === 'rb'){ text = 'Um ein rundes Beet mit dem Radius \\(' + r + '\\,\\text{m}\\) führt ein \\(' + b + '\\,\\text{m}\\) breiter Weg. Wie gross ist die Wegfläche (in m²)?';
            falsch.push([PI * R * R, 'Das ist die ganze Fläche mit dem Beet. Die Beetfläche \\(\\pi r^2\\) abziehen.', 'Beet']); }
          if (art === 'mb'){ text = 'Ein Kreisring ist \\(' + b + '\\,\\text{cm}\\) breit, sein mittlerer Radius ist \\(r_m = ' + rm + '\\,\\text{cm}\\). Wie gross ist seine Fläche?';
            falsch.push([2 * PI * rm, 'Das ist der mittlere Umfang. Mal die Breite \\(b\\) gibt die Fläche.', 'mittlere Umfang']); }
          return { art: art, R: R, r: r, b: b, rm: rm, soll: r2(soll), falsch: falsch, text: text }; },
        vorbereiten: function(box, A){ var e = box.querySelector('.ue-eingabe'); if (A.art === 'rb') e.innerHTML = e.innerHTML.replace('cm²', 'm²'); },
        fehler: function(A){ return fehlerListe(A, 'x', A.falsch); },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, A.art === 'mb' ? '\\(A = 2\\pi r_m \\cdot b\\).' : '\\(A = \\pi (R^2 - r^2)\\) mit den Radien.', nurAndere(A, A.falsch)); },
        loesung: function(A){ return A.art === 'mb' ? 'A = 2\\pi \\cdot ' + A.rm + ' \\cdot ' + A.b + ' \\approx ' + A.soll : 'A = \\pi (' + A.R + '^2 - ' + A.r + '^2) \\approx ' + A.soll; } }
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
       ["k", [x,y], r, cls] Kreis · ["sek", [x,y], r, w0, w1, cls] Sektor (Grad) · ["bog", [x,y], r, w0, w1, cls] Bogen ·
       ["seg", [x,y], r, w0, w1, cls] Segment · ["t", [x,y], "Text", cls, dx, dy, anker] · ["p", [x,y]] Punkt ·
       ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel · ["w", Scheitel, [x,y], [x,y], "Text"] Winkelbogen. ---------- */
  document.querySelectorAll('svg.geo-mini[data-fig]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-1,9,-1').split(',').map(Number), b = +(svg.dataset.breite || 220), h = +(svg.dataset.hoehe || 150);
    var F = Flaeche(svg, { w: b, h: h, x0: fe[0], x1: fe[1], y0: fe[2], karo: svg.dataset.karo === 'ja' ? 1 : false });
    JSON.parse(svg.dataset.fig).forEach(function(e){
      var t = e[0];
      if (t === 'v') F.vieleck(e[1], e[2] || 'figur');
      else if (t === 's') F.strecke(e[1], e[2], e[3] || 'hilfe');
      else if (t === 'g') F.gerade(e[1], e[2], e[3] || 'gerade-linie');
      else if (t === 'k') F.kreis(e[1], e[2], e[3] || 'figur kreis');
      else if (t === 'sek') F.sektor(e[1], e[2], grad(e[3]), grad(e[4]), e[5] || 'sektor');
      else if (t === 'bog') F.sektor(e[1], e[2], grad(e[3]), grad(e[4]), e[5] || 'bogen', true);
      else if (t === 'seg') F.vieleck(bogenPunkte(e[1], e[2], grad(e[3]), grad(e[4])), e[5] || 'segment');
      else if (t === 't') F.text(e[1], e[2], e[3] || 'mass', e[4], e[5], e[6]);
      else if (t === 'p') F.punkt(e[1]);
      else if (t === 'r') F.rechts(e[1], e[2], e[3], '');
      else if (t === 'w') winkelMarke(F, e[1], e[2], e[3], e[5] || 20, 'winkelbogen', e[4], 'winkel klein');
    });
    svg.setAttribute('role', 'img');
  });
})();
</script>
