<script>
/* Leitprogramm Planimetrie — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit Rückmeldung,
   Figuren zu den Aufgaben. Notation wie auf den Themenseiten 5.2a–d: Ecken A, B, C gegen den
   Uhrzeigersinn, Seite a gegenüber A, Höhen h_a …, Mittellinie m, Mittelpunktswinkel φ, Streckfaktor k.
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Figur · orange = Hilfslinie, Element,
   Streckfaktor · grün = gesuchte Grösse, Fläche · rot = Fehler. Dezimalpunkt; gerundet mit «≈». */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', PI = Math.PI;
  function z(n, st){ var f = Math.pow(10, st == null ? 2 : st), r = Math.round(n * f) / f; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function zz(v, st){ var f = Math.pow(10, st == null ? 2 : st), r = Math.round(v * f) / f; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(v, st); }
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
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^≈/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  /* Vergleich gerundeter Ergebnisse: richtig auf zwei Dezimalen (Toleranz 0.006);
     «nah» heisst: richtig gerechnet, aber zu grob gerundet. */
  function stimmt(e, soll){ return Math.abs(e - soll) <= 0.006 + 1e-9; }
  function nah(e, soll){ return !stimmt(e, soll) && Math.abs(e - soll) <= Math.max(0.06, Math.abs(soll) * 0.005); }
  var RUNDEN = 'Fast — runde auf zwei Dezimalen (Zwischenresultate ungerundet weiterverwenden).';

  /* ---------- Zeichenfläche in Weltkoordinaten (1 Einheit = 1 cm, beide Achsen gleich) ---------- */
  function Flaeche(svg, o){
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, s = W / (x1 - x0), y1 = o.y0 + H / s, y0 = o.y0;
    function X(x){ return (x - x0) * s; }
    function Y(y){ return H - (y - y0) * s; }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    var g = el(svg, 'g', {}), i;
    if (o.karo !== false){
      for (i = Math.ceil(x0); i <= x1; i++) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
      for (i = Math.ceil(y0); i <= y1; i++) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
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
      kreis: function(m, r, cls){ var M = dreh(m); return el(ebene, 'circle', { cx: X(M[0]), cy: Y(M[1]), r: r * s, 'class': cls }); },
      sektor: function(m, r, w0, w1, cls, nurBogen){
        var a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var gross = (w1 - w0) > PI ? 1 : 0, A = dreh(a), B = dreh(b), M = dreh(m);
        if (w1 - w0 >= 2 * PI - 1e-9) return F.kreis(m, r, cls);
        var d = (nurBogen ? 'M' : 'M' + X(M[0]) + ' ' + Y(M[1]) + ' L') + X(A[0]) + ' ' + Y(A[1]) + ' A' + r * s + ' ' + r * s + ' 0 ' + gross + ' 0 ' + X(B[0]) + ' ' + Y(B[1]) + (nurBogen ? '' : ' Z');
        return el(ebene, 'path', { d: d, 'class': cls }); },
      punkt: function(p, cls){ var A = dreh(p); return el(ebene, 'circle', { cx: X(A[0]), cy: Y(A[1]), r: 3.5, 'class': cls || 'g-pkt' }); },
      text: function(p, t, cls, dx, dy, anker){ var A = dreh(p);
        return el(ebene, 'text', { x: X(A[0]) + (dx || 0), y: Y(A[1]) + (dy || 0), 'text-anchor': anker || 'middle', 'class': 'g-text ' + (cls || '') }, t); },
      rechts: function(fuss, r1, r2, cls){   // Zeichen für den rechten Winkel, Richtungen als Vektoren
        var q = 0.45, n1 = Math.hypot(r1[0], r1[1]), n2 = Math.hypot(r2[0], r2[1]);
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
  function lot(p, a, b){   // Fusspunkt des Lots von p auf die Gerade ab
    var dx = b[0] - a[0], dy = b[1] - a[1], t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy);
    return [a[0] + t * dx, a[1] + t * dy, t];
  }
  function abst(p, q){ return Math.hypot(p[0] - q[0], p[1] - q[1]); }
  function winkel(p, a, b){   // Winkel bei p zwischen pa und pb, in Grad
    var u = [a[0] - p[0], a[1] - p[1]], v = [b[0] - p[0], b[1] - p[1]];
    return Math.acos((u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]))) * 180 / PI;
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

  /* ---------- Geometrie-Arbeitsbereich ----------
     Unterschied zu den Animationen der Themenseiten 5.2a–d: Dort zeigt eine Animation eine
     Konstruktion oder eine Beziehung. Hier trägt die Figur Aufgaben (Leitfaden HOWTO-PlaniLP):
     Figur verändern (Regler), Hilfslinie antippen (Kandidaten mit eigener Rückmeldung), Grösse
     berechnen und eingeben. Gefragte Werte stehen nicht im Bild, bevor die Antwort stimmt.

     arbeitsbereich(id, { fenster, zeichnen(F, w, sim), aufgaben }) — jede Aufgabe:
       text, setup(sim) (Regler setzen: sim.setze({ t: 10 }), sim.sperre('t')),
       wahl: { richtig: 'h', rueck: { id: 'Text' } }       — Hilfslinie antippen
       frage: [{ name, label, einheit, soll, fehler: [[wert, 'Text']] }] — Grössen eingeben
       ziel: function(w) — Reglerzustand (w = Werte der Regler, w.bewegt) */
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
        if (stimmt(e.wert, f.soll)) continue;
        alle = false;
        var t = null;
        (f.fehler || []).forEach(function(fe){ if (!t && stimmt(e.wert, fe[0])) t = fe[1]; });
        r.push(t || (nah(e.wert, f.soll) ? RUNDEN : f.tipp || 'Noch nicht. Rechne nach.'));
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
  function grad(w){ return w * PI / 180; }

  /* ---------- Kapitel 1: Dreiecke beschreiben ----------
     A(0|0), B(6|0), C über zwei Regler. Kandidaten aus C: Höhe, Seitenhalbierende, Winkelhalbierende,
     dazu die Mittelsenkrechte von c. Startwert C(2|3): nicht gleichschenklig, nicht rechtwinklig. */
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 200, x0: -3.5, x1: 9.5, y0: -1.6 },
    zeichnen: function(F, w, k){
      var A = [0, 0], B = [6, 0], C = [w.cx, w.cy], fuss = lot(C, A, B);
      var ca = abst(C, A), cb = abst(C, B), wfuss = [6 * ca / (ca + cb), 0];
      var al = winkel(A, B, C), be = winkel(B, A, C), ga = 180 - al - be;
      F.vieleck([A, B, C], 'figur');
      if (fuss[2] < 0 || fuss[2] > 1) F.strecke(fuss[2] < 0 ? A : B, [fuss[0], 0], 'verlaengerung');
      if (k.wahl){
        F.kandidat('h', C, [fuss[0], 0], k.wahl);
        F.kandidat('s', C, [3, 0], k.wahl);
        F.kandidat('w', C, wfuss, k.wahl);
        F.kandidat('m', [3, -1], [3, 1], k.wahl, true);
      }
      if (w.richtig && k.aufgabe && k.aufgabe.wahl){
        var r = k.aufgabe.wahl.richtig;
        if (r === 'h'){ F.strecke(C, [fuss[0], 0], 'hilfe'); F.rechts([fuss[0], 0], [0, 1], [fuss[2] < 0.5 ? 1 : -1, 0], 'hilfe'); }
        if (r === 's'){ F.strecke(C, [3, 0], 'hilfe'); F.punkt([3, 0], 'g-pkt hilfe'); }
      }
      [[A, 'A', -8, 14], [B, 'B', 8, 14], [C, 'C', 0, -9]].forEach(function(p){ F.punkt(p[0]); F.text(p[0], p[1], 'ecke', p[2], p[3]); });
      F.text([3, 0], 'c', 'seite', 0, 15);
      F.text([(B[0] + C[0]) / 2, (B[1] + C[1]) / 2], 'a', 'seite', 9, -4, 'start');
      F.text([(A[0] + C[0]) / 2, (A[1] + C[1]) / 2], 'b', 'seite', -9, -4, 'end');
      return 'α ' + zz(al, 1) + '°; &nbsp;β ' + zz(be, 1) + '°; &nbsp;γ ' + zz(ga, 1) + '°; &nbsp;Summe ' + z(al + be + ga, 1) + '°'
        + (al > 90 + 1e-9 || be > 90 + 1e-9 || ga > 90 + 1e-9 ? ' — stumpfwinklig' : Math.abs(Math.max(al, be, ga) - 90) < 1e-6 ? ' — rechtwinklig' : ' — spitzwinklig');
    },
    aufgaben: [
      { text: 'Erkunde: Zieh die Ecke \\(C\\) herum. Was bleibt bei \\(\\alpha + \\beta + \\gamma\\) immer gleich?', probe: { cx: 4 }, ziel: function(w){ return w.bewegt.cx || w.bewegt.cy; } },
      { text: 'Tipp die Höhe \\(h_c\\) an — das Lot von \\(C\\) auf die Gerade \\(AB\\).', setup: function(s){ s.setze({ cx: 0.5, cy: 4 }); s.sperre('cx', 'cy'); },
        wahl: { richtig: 'h', gut: 'Die Höhe steht senkrecht auf \\(AB\\).', rueck: {
          s: 'Das ist die Seitenhalbierende \\(s_c\\): Sie endet in der Mitte von \\(AB\\), steht aber nicht senkrecht darauf.',
          w: 'Das ist die Winkelhalbierende \\(w_\\gamma\\): Sie halbiert den Winkel bei \\(C\\).',
          m: 'Das ist die Mittelsenkrechte von \\(c\\): Sie steht senkrecht auf \\(AB\\), geht aber durch die Mitte von \\(AB\\), nicht durch \\(C\\).' } } },
      { text: 'Tipp die Seitenhalbierende \\(s_c\\) an.', setup: function(s){ s.setze({ cx: 5, cy: 4 }); s.sperre('cx', 'cy'); },
        wahl: { richtig: 's', gut: 'Sie verbindet \\(C\\) mit der Mitte von \\(AB\\).', rueck: {
          h: 'Das ist die Höhe \\(h_c\\): Sie steht senkrecht auf \\(AB\\). Die Seitenhalbierende endet in der Mitte von \\(AB\\).',
          w: 'Das ist die Winkelhalbierende \\(w_\\gamma\\).',
          m: 'Das ist die Mittelsenkrechte: Sie geht durch die Mitte von \\(AB\\), aber nicht durch \\(C\\).' } } },
      { text: 'Mach das Dreieck bei \\(A\\) stumpfwinklig. Wo liegt der Fusspunkt der Höhe \\(h_c\\) jetzt?', probe: { cx: -1 }, ziel: function(w){ return w.cx < 0; } },
      { text: 'Stell ein gleichschenkliges Dreieck mit der Basis \\(c\\) ein.', probe: { cx: 3 }, ziel: function(w){ return w.cx === 3; } },
      { text: 'Stell einen rechten Winkel bei \\(C\\) ein.', probe: { cx: 3, cy: 3 }, ziel: function(w){ return w.cx === 3 && w.cy === 3; } },
      { text: 'In diesem Dreieck ist \\(\\alpha \\approx 56.3°\\) und \\(\\beta \\approx 36.9°\\). Wie gross ist \\(\\gamma\\)?', setup: function(s){ s.setze({ cx: 2, cy: 3 }); s.sperre('cx', 'cy'); },
        frage: [{ name: 'gamma', label: '\\(\\gamma \\approx\\)', einheit: '°', soll: 86.8, fehler: [[93.2, 'Das ist \\(\\alpha + \\beta\\). \\(\\gamma\\) ist der Rest bis \\(180°\\).'], [266.8, 'Die Winkelsumme im Dreieck ist \\(180°\\), nicht \\(360°\\).']], tipp: '\\(\\gamma = 180° - \\alpha - \\beta\\).' }] }
    ]
  });

  /* ---------- Kapitel 2: Dreiecksfläche und zugehörige Höhe (ausgearbeitetes Kapitel des Leitfadens) ----------
     A(0|0), B(8|0), Spitze C(t|3), 1 Einheit = 1 cm. Die Spitze wandert auf der Parallelen zu AB. */
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 170, x0: -3, x1: 12, y0: -2.2, karo: true },
    zeichnen: function(F, w, k){
      var A = [0, 0], B = [8, 0], C = [w.t, 3], rot = k.aufgabe && k.aufgabe.gedreht ? grad(28) : 0;
      F.drehen(rot);
      var fuss = lot(C, A, B), fussB = lot(B, A, C);
      F.vieleck([A, B, C], 'figur');
      F.strecke([-3, 3], [12, 3], 'parallele');
      if (fuss[2] < 0 || fuss[2] > 1) F.strecke(fuss[2] < 0 ? A : B, [fuss[0], 0], 'verlaengerung');
      var hb = k.aufgabe && k.aufgabe.hb;
      if (hb){ F.gerade(A, C, 'verlaengerung'); }
      if (k.wahl){
        if (!hb){
          F.kandidat('b', A, C, k.wahl); F.kandidat('a', B, C, k.wahl);
          F.kandidat('h', C, [fuss[0], 0], k.wahl); F.kandidat('s', C, [4, 0], k.wahl);
        } else {
          F.kandidat('hb', B, [fussB[0], fussB[1]], k.wahl); F.kandidat('h', C, [fuss[0], 0], k.wahl);
          F.kandidat('a', B, C, k.wahl); F.kandidat('sb', B, [C[0] / 2, C[1] / 2], k.wahl);
        }
      }
      var zeigeH = w.richtig || (k.aufgabe && k.aufgabe.zeigeH);
      if (zeigeH && !hb){ F.strecke(C, [fuss[0], 0], 'hilfe'); F.rechts([fuss[0], 0], [0, 1], [fuss[2] < 0.5 ? 1 : -1, 0], 'hilfe'); F.text([fuss[0], 1.5], 'h', 'hilfe', -8, 0, 'end'); }
      if (w.richtig && hb){ F.strecke(B, [fussB[0], fussB[1]], 'hilfe'); }
      [[A, 'A', -8, 14], [B, 'B', 8, 14], [C, 'C', 0, -9]].forEach(function(p){ F.punkt(p[0]); F.text(p[0], p[1], 'ecke', p[2], p[3]); });
      F.text([4, 0], 'g = 8 cm', 'mass', 0, 16);
      F.drehen(0);
      return 'Spitze \\(C(' + z(w.t) + ' \\mid 3)\\); \\(g = 8\\,\\text{cm}\\)' + (zeigeH || w.richtig ? '; \\(h = 3\\,\\text{cm}\\)' : '');
    },
    aufgaben: [
      { text: 'Die Grundseite ist \\(AB\\). Tipp die zugehörige Höhe an.',
        wahl: { richtig: 'h', gut: 'Die Höhe ist der senkrechte Abstand von \\(C\\) zur Geraden \\(AB\\): \\(h = 3\\,\\text{cm}\\).', rueck: {
          a: 'Das ist die Seite \\(a = BC\\) — sie steht nicht senkrecht auf \\(AB\\).',
          b: 'Das ist die Seite \\(b = AC\\) — sie steht nicht senkrecht auf \\(AB\\).',
          s: 'Das ist die Seitenhalbierende: Sie endet in der Mitte von \\(AB\\) und steht nicht senkrecht.' } } },
      { text: 'Berechne die Fläche des Dreiecks.', setup: function(s){ s.sperre('t'); },
        frage: [{ name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 12, fehler: [[24, 'Das ist \\(g \\cdot h\\) — die Fläche des Parallelogramms. Das Dreieck ist die Hälfte davon.']], tipp: '\\(A = \\tfrac{1}{2}\\, g \\cdot h\\).' }] },
      { text: 'Verschieb die Spitze nach \\(t = 10\\). Wo liegt der Fusspunkt der Höhe jetzt?', probe: { t: 10 }, ziel: function(w){ return w.t === 10; } },
      { text: 'Die Spitze steht bei \\(t = 10\\). Wie gross ist die Fläche jetzt?', setup: function(s){ s.setze({ t: 10 }); s.sperre('t'); },
        frage: [{ name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 12, fehler: [[14.42, 'Die schräge Seite \\(BC\\) ist keine Höhe. Die Höhe ist der senkrechte Abstand zur <b>Geraden</b> \\(AB\\) — auch ausserhalb der Strecke.'], [24, 'Das ist \\(g \\cdot h\\). Das Dreieck ist die Hälfte.']], tipp: 'Grundseite und Höhe haben sich nicht geändert.' }],
        loesung: 'Grundseite und Höhe sind gleich geblieben — also auch die Fläche.' },
      { text: 'Dieselbe Figur, gedreht. Tipp die Höhe zur Grundseite \\(AB\\) an.', gedreht: true, setup: function(s){ s.setze({ t: 2 }); s.sperre('t'); s.F.drehen(grad(28)); },
        wahl: { richtig: 'h', gut: 'Die Höhe steht senkrecht auf \\(AB\\) — egal, wie die Figur liegt.', rueck: {
          a: 'Das ist die Seite \\(a\\). Die Höhe steht senkrecht auf \\(AB\\), nicht senkrecht zum Bildrand.',
          b: 'Das ist die Seite \\(b\\). Die Höhe steht senkrecht auf \\(AB\\), nicht senkrecht zum Bildrand.',
          s: 'Das ist die Seitenhalbierende.' } } },
      { text: 'Jetzt ist \\(b = AC\\) die Grundseite. Tipp die Höhe \\(h_b\\) an.', hb: true, setup: function(s){ s.setze({ t: 4 }); s.sperre('t'); },
        wahl: { richtig: 'hb', gut: 'Das Lot von \\(B\\) auf die Gerade \\(AC\\) — sein Fusspunkt liegt auf der Verlängerung.', rueck: {
          h: 'Das ist die Höhe zur Grundseite \\(AB\\). Zu \\(b = AC\\) gehört das Lot von der gegenüberliegenden Ecke \\(B\\).',
          a: 'Das ist die Seite \\(a\\) — sie steht nicht senkrecht auf \\(AC\\).',
          sb: 'Das ist die Seitenhalbierende von \\(B\\) aus: Sie endet in der Mitte von \\(AC\\).' } } },
      { text: '\\(b = AC = 5\\,\\text{cm}\\) und \\(A = 12\\,\\text{cm}^2\\). Wie lang ist \\(h_b\\)?', hb: true, setup: function(s){ s.setze({ t: 4 }); s.sperre('t'); },
        frage: [{ name: 'hb', label: '\\(h_b =\\)', einheit: 'cm', soll: 4.8, fehler: [[2.4, 'Aus \\(A = \\tfrac{1}{2}\\, b \\cdot h_b\\) folgt \\(h_b = \\tfrac{2A}{b}\\) — das Doppelte.'], [30, 'Umgekehrt: \\(h_b = \\tfrac{2A}{b} = \\tfrac{24}{5}\\).']], tipp: '\\(h_b = \\tfrac{2A}{b}\\).' }] }
    ]
  });

  /* ---------- Kapitel 3: Vierecke — das Trapez als Familie ----------
     A(0|0), B(8|0), D(d|h), C(d + c|h). c = 8 macht ein Parallelogramm, d = (8 − c)/2 ein
     gleichschenkliges Trapez. Startwert c = 4, h = 3, d = 1: weder das eine noch das andere. */
  arbeitsbereich('sim3', {
    fenster: { w: 320, h: 170, x0: -2.5, x1: 15, y0: -1.6 },
    zeichnen: function(F, w, k){
      var a = 8, A = [0, 0], B = [a, 0], D = [w.d, w.h], C = [w.d + w.c, w.h];
      var M1 = [(A[0] + D[0]) / 2, w.h / 2], M2 = [(B[0] + C[0]) / 2, w.h / 2];
      F.vieleck([A, B, C, D], 'figur');
      if (k.wahl){
        F.kandidat('m', M1, M2, k.wahl); F.kandidat('e', A, C, k.wahl);
        F.kandidat('h', D, [D[0], 0], k.wahl); F.kandidat('x', [a / 2, 0], [w.d + w.c / 2, w.h], k.wahl);
      }
      if (w.richtig && k.aufgabe && k.aufgabe.wahl) F.strecke(M1, M2, 'hilfe');
      if (k.aufgabe && k.aufgabe.zeigeH){ F.strecke(D, [D[0], 0], 'hilfe2'); }
      [[A, 'A', -8, 14], [B, 'B', 8, 14], [C, 'C', 6, -8], [D, 'D', -6, -8]].forEach(function(p){ F.punkt(p[0]); F.text(p[0], p[1], 'ecke', p[2], p[3]); });
      var s1 = Math.hypot(w.d, w.h), s2 = Math.hypot(a - w.d - w.c, w.h);
      var art = w.c === a ? 'Parallelogramm' : Math.abs(w.d - (a - w.c) / 2) < 1e-9 ? 'gleichschenkliges Trapez' : 'Trapez';
      return art + ': \\(a = 8\\), \\(c = ' + z(w.c) + '\\), \\(h = ' + z(w.h) + '\\)'
        + (k.aufgabe && k.aufgabe.frage ? '' : '; \\(A = ' + z((a + w.c) / 2 * w.h) + '\\,\\text{cm}^2\\); \\(U ' + (Math.abs(s1 + s2 - Math.round((s1 + s2) * 100) / 100) > 1e-9 ? '\\approx' : '=') + ' ' + z(a + w.c + s1 + s2) + '\\,\\text{cm}\\)');
    },
    aufgaben: [
      { text: 'Erkunde: Verschieb die obere Seite mit \\(d\\). Was bleibt gleich, was ändert sich?', probe: { d: 2 }, ziel: function(w){ return w.bewegt.d; } },
      { text: 'Mach aus dem Trapez ein Parallelogramm.', probe: { c: 8 }, ziel: function(w){ return w.c === 8; } },
      { text: 'Stell ein gleichschenkliges Trapez ein (nicht ein Parallelogramm).', probe: { c: 4, d: 2 }, ziel: function(w){ return w.c < 8 && Math.abs(w.d - (8 - w.c) / 2) < 1e-9; } },
      { text: 'Tipp die Mittellinie \\(m\\) an.', setup: function(s){ s.setze({ c: 4, h: 3, d: 1 }); s.sperre('c', 'h', 'd'); },
        wahl: { richtig: 'm', gut: 'Sie verbindet die Mitten der Schenkel: \\(m = \\tfrac{1}{2}(a + c)\\).', rueck: {
          e: 'Das ist die Diagonale \\(e = AC\\).', h: 'Das ist eine Höhe: Sie steht senkrecht auf den Parallelseiten.',
          x: 'Diese Linie verbindet die Mitten der Parallelseiten — die Mittellinie verbindet die Mitten der <b>Schenkel</b>.' } } },
      { text: '\\(a = 8\\,\\text{cm}\\), \\(c = 4\\,\\text{cm}\\), \\(h = 3\\,\\text{cm}\\): Wie lang ist die Mittellinie, wie gross die Fläche?', setup: function(s){ s.setze({ c: 4, h: 3, d: 1 }); s.sperre('c', 'h', 'd'); },
        frage: [{ name: 'm', label: '\\(m =\\)', einheit: 'cm', soll: 6, fehler: [[12, 'Die Mittellinie ist der <b>Mittelwert</b> der Parallelseiten: \\(\\tfrac{1}{2}(a + c)\\).'], [2, 'Mittelwert, nicht halbe Differenz: \\(\\tfrac{1}{2}(a + c)\\).']], tipp: '\\(m = \\tfrac{1}{2}(a + c)\\).' },
                { name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 18, fehler: [[36, 'Das ist \\((a + c) \\cdot h\\) — es braucht die Hälfte davon: \\(m \\cdot h\\).'], [96, '\\(a \\cdot c \\cdot h\\) ist keine Trapezformel: \\(A = m \\cdot h\\).']], tipp: '\\(A = m \\cdot h\\).' }] },
      { text: 'Gleichschenklig mit \\(a = 8\\,\\text{cm}\\), \\(c = 2\\,\\text{cm}\\), \\(h = 4\\,\\text{cm}\\): Wie lang ist ein Schenkel?', setup: function(s){ s.setze({ c: 2, h: 4, d: 3 }); s.sperre('c', 'h', 'd'); },
        zeigeH: true,
        frage: [{ name: 's', label: 'Schenkel', einheit: 'cm', soll: 5, fehler: [[7.21, 'Der Überstand ist nicht \\(6\\), sondern die Hälfte: \\(\\tfrac{8 - 2}{2} = 3\\).'], [6.71, 'Der Überstand ist \\(\\tfrac{a - c}{2} = 3\\), die Höhe \\(4\\).'], [7, 'Pythagoras: \\(\\sqrt{3^2 + 4^2}\\), nicht \\(3 + 4\\).']], tipp: 'Rechtwinkliges Dreieck aus Höhe \\(4\\) und Überstand \\(\\tfrac{a - c}{2}\\): Pythagoras.' }] }
    ]
  });

  /* ---------- Kapitel 4: Kreis und Kreisteile ----------
     Mittelpunkt (0|0), Radius r, Mittelpunktswinkel φ. Der Sektor ist grün, sein Bogen orange. */
  arbeitsbereich('sim4', {
    fenster: { w: 320, h: 240, x0: -6.5, x1: 6.5, y0: -4.75 },
    zeichnen: function(F, w, k){
      var r = w.r, phi = grad(w.phi), M = [0, 0], seg = k.aufgabe && k.aufgabe.segment;
      F.kreis(M, r, 'figur kreis');
      if (w.phi > 0){
        F.sektor(M, r, 0, phi, seg ? 'sektor blass' : 'sektor');
        F.sektor(M, r, 0, phi, 'bogen', true);
        if (seg){ var P1 = [r, 0], P2 = [r * Math.cos(phi), r * Math.sin(phi)]; F.vieleck([M, P1, P2], 'dreieck-seg'); }
      }
      F.punkt(M); F.text(M, 'M', 'ecke', -9, 14);
      if (k.wahl){
        var w0 = grad(130), T = [r * Math.cos(w0), r * Math.sin(w0)];
        F.kandidat('t', [T[0] - 3 * Math.sin(w0), T[1] + 3 * Math.cos(w0)], [T[0] + 3 * Math.sin(w0), T[1] - 3 * Math.cos(w0)], k.wahl, true);
        F.kandidat('s', [-r, -0.4 * r], [r, 0.2 * r], k.wahl, true);
        F.kandidat('p', [-6, -r - 0.8], [6, -r - 0.3], k.wahl, true);
        var q1 = grad(200), q2 = grad(290);
        F.kandidat('h', [r * Math.cos(q1), r * Math.sin(q1)], [r * Math.cos(q2), r * Math.sin(q2)], k.wahl);
        if (w.richtig){ F.strecke(M, T, 'hilfe'); F.rechts(T, [-Math.cos(w0), -Math.sin(w0)], [Math.sin(w0), -Math.cos(w0)], 'hilfe'); }
      }
      return '\\(r = ' + z(w.r) + '\\,\\text{cm}\\); \\(\\varphi = ' + z(w.phi) + '°\\); Anteil \\(\\tfrac{\\varphi}{360°} = ' + zz(w.phi / 360, 3) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(\\varphi\\). Welchen Anteil des Kreises nimmt der Sektor ein?', probe: { phi: 100 }, ziel: function(w){ return w.bewegt.phi; } },
      { text: 'Tipp die Tangente an.',
        wahl: { richtig: 't', gut: 'Sie berührt den Kreis in genau einem Punkt und steht dort senkrecht auf dem Radius.', rueck: {
          s: 'Das ist eine Sekante: Sie schneidet den Kreis in zwei Punkten.', p: 'Das ist eine Passante: Sie hat keinen Punkt mit dem Kreis gemeinsam.',
          h: 'Das ist eine Sehne — eine Strecke zwischen zwei Kreispunkten, keine Gerade.' } } },
      { text: 'Stell den Sektor auf einen Viertelkreis ein.', probe: { phi: 90 }, ziel: function(w){ return w.phi === 90; } },
      { text: '\\(r = 4\\,\\text{cm}\\), \\(\\varphi = 90°\\): Wie lang ist der Bogen?', setup: function(s){ s.setze({ r: 4, phi: 90 }); s.sperre('r', 'phi'); },
        frage: [{ name: 'b', label: '\\(b \\approx\\)', einheit: 'cm', soll: 6.28, fehler: [[25.13, 'Das ist der ganze Umfang. Der Bogen ist der Anteil \\(\\tfrac{\\varphi}{360°}\\) davon.'], [12.57, 'Das ist die Sektorfläche \\(\\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\). Gefragt ist die Länge: \\(\\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).']], tipp: '\\(b = \\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).' }] },
      { text: '\\(r = 5\\,\\text{cm}\\), \\(\\varphi = 72°\\): Wie gross ist die Sektorfläche?', setup: function(s){ s.setze({ r: 5, phi: 72 }); s.sperre('r', 'phi'); },
        frage: [{ name: 'AS', label: '\\(A_S \\approx\\)', einheit: 'cm²', soll: 15.71, fehler: [[6.28, 'Das ist die Bogenlänge. Die Fläche: \\(\\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).'], [78.54, 'Das ist die ganze Kreisfläche. Der Sektor ist der Anteil \\(\\tfrac{72°}{360°} = \\tfrac{1}{5}\\) davon.']], tipp: '\\(A_S = \\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).' }] },
      { text: 'Das Segment zwischen Sehne und Bogen (\\(r = 4\\,\\text{cm}\\), \\(\\varphi = 90°\\)): Wie gross ist seine Fläche?', segment: true, setup: function(s){ s.setze({ r: 4, phi: 90 }); s.sperre('r', 'phi'); },
        frage: [{ name: 'Aseg', label: '\\(A \\approx\\)', einheit: 'cm²', soll: 4.57, fehler: [[12.57, 'Das ist der ganze Sektor. Zieh das Dreieck \\(\\tfrac{1}{2} \\cdot 4 \\cdot 4 = 8\\,\\text{cm}^2\\) ab.'], [20.57, 'Sektor <b>minus</b> Dreieck, nicht plus.']], tipp: 'Segment = Sektor − Dreieck.' }] }
    ]
  });

  /* ---------- Kapitel 5: Ähnlichkeit — zentrische Streckung ----------
     Zentrum Z(0|0), Dreieck A(1|0.5), B(3|0.5), C(1.5|2), also AB = 2 cm. k läuft von −2 bis 3, nie 0. */
  arbeitsbereich('sim5', {
    fenster: { w: 320, h: 230, x0: -7, x1: 10, y0: -5 },
    zeichnen: function(F, w, k){
      var kk = w.k, P = [[1, 0.5], [3, 0.5], [1.5, 2]], B = P.map(function(p){ return [kk * p[0], kk * p[1]]; });
      var strahlen = k.aufgabe && k.aufgabe.strahlen;
      P.forEach(function(p, j){ F.gerade([0, 0], p, 'strahl'); });
      F.vieleck(P, 'figur');
      F.vieleck(B, 'bild');
      F.punkt([0, 0]); F.text([0, 0], 'Z', 'ecke', -9, 14);
      ['A', 'B', 'C'].forEach(function(n, j){ F.text(P[j], n, 'ecke klein', -8, -5); if (kk !== 1) F.text(B[j], n + '′', 'ecke klein bild', 8, -5, 'start'); });
      if (strahlen) return '\\(SA = 4\\,\\text{cm}\\); \\(SA\' = 6\\,\\text{cm}\\); \\(AB = 3\\,\\text{cm}\\); \\(AB \\parallel A\'B\'\\)';
      return '\\(k = ' + z(kk) + '\\); \\(A\'B\' = ' + z(2 * Math.abs(kk)) + '\\,\\text{cm}\\) (Original \\(AB = 2\\,\\text{cm}\\)); Flächenfaktor \\(k^2 = ' + z(kk * kk) + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(k\\), auch unter null. Wo liegt das Bild, und was bleibt gleich?', probe: { k: 2 }, ziel: function(w){ return w.bewegt.k; } },
      { text: 'Stell \\(k\\) so ein, dass \\(A\'B\' = 3\\,\\text{cm}\\) ist und das Bild auf derselben Seite von \\(Z\\) liegt.', probe: { k: 1.5 }, ziel: function(w){ return w.k === 1.5; } },
      { text: 'Das Bild soll die vierfache Fläche haben.', probe: { k: -2 }, ziel: function(w){ return Math.abs(w.k) === 2; } },
      { text: 'Das Bild soll gleich gross sein, aber auf der anderen Seite von \\(Z\\) liegen.', probe: { k: -1 }, ziel: function(w){ return w.k === -1; } },
      { text: 'Eine Figur mit \\(4\\,\\text{cm}^2\\) wird mit \\(k = 2.5\\) gestreckt. Wie gross ist die Bildfläche?', setup: function(s){ s.setze({ k: 2.5 }); s.sperre('k'); },
        frage: [{ name: 'A', label: '\\(A\' =\\)', einheit: 'cm²', soll: 25, fehler: [[10, 'Längen werden mit \\(k\\) gestreckt, Flächen mit \\(k^2 = 6.25\\).'], [6.5, 'Strecken heisst multiplizieren — mit \\(k^2\\).']], tipp: '\\(A\' = k^2 \\cdot A\\).' }] },
      { text: 'Strahlensatz: \\(SA = 4\\,\\text{cm}\\), \\(SA\' = 6\\,\\text{cm}\\), \\(AB = 3\\,\\text{cm}\\). Wie lang ist \\(A\'B\'\\)?', strahlen: true, setup: function(s){ s.setze({ k: 1.5 }); s.sperre('k'); },
        frage: [{ name: 'x', label: '\\(A\'B\' =\\)', einheit: 'cm', soll: 4.5, fehler: [[2, 'Umgekehrt: \\(A\'B\'\\) ist länger als \\(AB\\), weil \\(SA\'\\) länger ist als \\(SA\\).'], [5, 'Nicht addieren: Die Strecken stehen im <b>Verhältnis</b> \\(6 : 4 = 1.5\\).']], tipp: '\\(A\'B\' : AB = SA\' : SA\\).' }] }
    ]
  });
  // k = 0 wäre keine Streckung: der Regler springt darüber hinweg.
  (function(){ var inp = document.querySelector('#sim5 input[data-p="k"]'); if (!inp) return; var letzt = +inp.value;
    inp.addEventListener('input', function(){ if (+inp.value === 0) inp.value = letzt > 0 ? -0.5 : 0.5; letzt = +inp.value; }, true); })();

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function r2(v){ return Math.round(v * 100) / 100; }
    function tz(v){ return String(v).replace('-', '−'); }
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche ·
       Kapitelaufgaben · Gesamttest. Je Typ ein eigener Schlüssel. */
    var SPERRE = [
      'ws|50|60', 'ws|48|75', 'gs|30', 'gs|40', 'gs|64', 'gs|52',
      'df|8|3', 'df|10|4', 'df|9|4.2', 'hd|20|8', 'hd|15|6', 'hd|12|5', 'hd|18.9|7',
      'tr|10|4|4', 'tr|9|5|4', 'tr|12|6|5', 'tr|11|5|6', 'tr|8|4|3', 'ra|6|8', 'dr|10|6', 'pa|7|4',
      'py|6|8', 'py|3|4', 'py|3|6',
      'kr|5', 'kr|7.5', 'kr|6', 'kr|8', 'sk|6|60', 'sk|4|90', 'sk|5|72', 'sk|10|36', 'sk|8|135', 'sk|10|60', 'sk|6|90',
      'st|1.5|2', 'st|2.5|4', 'st|3|1', 'sa|4|6|3', 'sa|1.5|2|12', 'sa|2|3|15', 'sa|1.8|2.4|14'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function feld(A, f, e, soll, tipp, fehler){
      if (stimmt(e[f], soll)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (stimmt(e[f], fehler[j][0])) return fehler[j][1];
      return nah(e[f], soll) ? RUNDEN : tipp;
    }
    var TYPEN = {
      /* ── Kapitel 1 ── */
      'winkelsumme': { felder: ['w'], muster: '{w} °',
        schl: function(A){ return A.gs ? 'gs|' + A.spitze : 'ws|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { w: String(A.soll) }; },
        neu: function(){
          if (Math.random() < 0.4){ var sp = zufallG(4, 34) * 5, basis = (180 - sp) / 2, frageSp = Math.random() < 0.5;
            return { gs: true, spitze: sp, soll: frageSp ? sp : basis, text: frageSp
              ? 'Ein gleichschenkliges Dreieck hat die Basiswinkel \\(' + basis + '°\\). Wie gross ist der Winkel an der Spitze?'
              : 'Ein gleichschenkliges Dreieck hat an der Spitze den Winkel \\(' + sp + '°\\). Wie gross ist ein Basiswinkel?', frageSp: frageSp, basis: basis }; }
          var a = zufallG(20, 100), b = zufallG(15, 150 - a);
          return { a: a, b: b, soll: 180 - a - b, text: 'In einem Dreieck ist \\(\\alpha = ' + a + '°\\) und \\(\\beta = ' + b + '°\\). Wie gross ist \\(\\gamma\\)?' }; },
        fehler: function(A){ return A.gs ? (A.frageSp ? [[{ w: String(180 - A.basis) }, 'zwei']] : [[{ w: String(180 - A.spitze) }, 'zwei']]) : [[{ w: String(360 - A.a - A.b) }, '180']]; },
        pruefen: function(A, e){
          if (gl(e.w, A.soll)) return null;
          if (A.gs){
            if (!A.frageSp && gl(e.w, 180 - A.spitze)) return 'Für die beiden Basiswinkel zusammen bleiben \\(' + (180 - A.spitze) + '°\\) — jeder ist die Hälfte (es sind zwei).';
            if (A.frageSp && gl(e.w, 180 - A.basis)) return 'Es gibt zwei Basiswinkel: \\(180° - 2 \\cdot ' + A.basis + '°\\).';
            return 'Winkelsumme \\(180°\\); die beiden Basiswinkel sind gleich gross.';
          }
          if (gl(e.w, 360 - A.a - A.b)) return 'Die Winkelsumme im Dreieck ist \\(180°\\), nicht \\(360°\\) (das gilt im Viereck).';
          return '\\(\\gamma = 180° - \\alpha - \\beta\\).'; },
        loesung: function(A){ return A.soll + '°'; } },

      'element': { felder: ['e'], muster: '{e:Höhe|Seitenhalbierende|Winkelhalbierende|Mittelsenkrechte}',
        eingabe: function(A){ return { e: A.soll }; },
        neu: function(){
          var ecke = zufall(['A', 'B', 'C']), seite = { A: 'a', B: 'b', C: 'c' }[ecke], gr = { A: 'α', B: 'β', C: 'γ' }[ecke];
          var art = zufall([0, 1, 2, 3]);
          var t = [['Sie geht von \\(' + ecke + '\\) aus und steht senkrecht auf der Geraden der Gegenseite \\(' + seite + '\\).', 'Höhe'],
                   ['Sie verbindet \\(' + ecke + '\\) mit der Mitte der Gegenseite \\(' + seite + '\\).', 'Seitenhalbierende'],
                   ['Sie teilt den Winkel \\(' + gr + '\\) bei \\(' + ecke + '\\) in zwei gleich grosse Teile.', 'Winkelhalbierende'],
                   ['Sie geht durch die Mitte der Seite \\(' + seite + '\\) und steht senkrecht auf ihr.', 'Mittelsenkrechte']][art];
          return { soll: t[1], text: 'Welche Linie ist gemeint? ' + t[0] }; },
        fehler: function(A){ return A.soll === 'Höhe' ? [[{ e: 'Mittelsenkrechte' }, 'Ecke']] : A.soll === 'Mittelsenkrechte' ? [[{ e: 'Höhe' }, 'Ecke']] : []; },
        pruefen: function(A, e){
          if (e.e === A.soll) return null;
          if (A.soll === 'Höhe' && e.e === 'Mittelsenkrechte') return 'Beide stehen senkrecht — die Mittelsenkrechte geht aber durch die Seitenmitte, nicht durch die Ecke.';
          if (A.soll === 'Mittelsenkrechte' && e.e === 'Höhe') return 'Beide stehen senkrecht — die Höhe geht aber durch die Ecke, nicht durch die Seitenmitte.';
          if (A.soll === 'Seitenhalbierende' && e.e === 'Mittelsenkrechte') return 'Die Mittelsenkrechte steht senkrecht auf der Seite; die Seitenhalbierende endet in der Ecke.';
          return 'Lies genau: Wo beginnt die Linie, wo endet sie, steht sie senkrecht?'; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      /* ── Kapitel 2 ── */
      'dreieck-flaeche': { felder: ['A'], muster: 'A = {A} ',
        schl: function(A){ return 'df|' + A.g + '|' + A.h; },
        eingabe: function(A){ return { A: String(A.soll) }; },
        neu: function(){
          var g = zufall([4, 5, 6, 7, 8, 9, 10, 12, 3.5, 4.5, 7.5]), h = zufall([2, 3, 4, 5, 6, 2.5, 3.6, 4.4]), misch = Math.random() < 0.35;
          var soll = g * h / 2, text, einh = 'cm²';
          if (misch){ text = 'Grundseite \\(g = ' + g / 100 + '\\,\\text{m}\\), zugehörige Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne die Fläche in \\(\\text{cm}^2\\).'; }
          else text = 'Grundseite \\(g = ' + g + '\\,\\text{cm}\\), zugehörige Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne die Fläche.';
          return { g: g, h: h, misch: misch, soll: r2(soll), text: text, einheit: einh }; },
        fehler: function(A){ var f = [[{ A: String(r2(A.g * A.h)) }, 'Hälfte']]; if (A.misch) f.push([{ A: String(r2(A.g / 100 * A.h / 2)) }, 'Einheiten']); return f; },
        pruefen: function(A, e){
          return feld(A, 'A', e, A.soll, A.misch ? 'Zuerst die Einheiten angleichen: \\(g = ' + A.g + '\\,\\text{cm}\\), dann \\(A = \\tfrac{1}{2}\\, g \\cdot h\\).' : '\\(A = \\tfrac{1}{2}\\, g \\cdot h\\).',
            [[A.g * A.h, '\\(g \\cdot h\\) ist das Parallelogramm — das Dreieck ist die <b>Hälfte</b>.'], [A.g / 100 * A.h / 2, 'Einheiten: \\(g\\) in m, \\(h\\) in cm — vorher angleichen.']]); },
        loesung: function(A){ return 'A = \\tfrac{1}{2} \\cdot ' + A.g + ' \\cdot ' + A.h + ' = ' + A.soll + '\\,\\text{cm}^2'; } },

      'hoehe': { felder: ['h'], muster: 'h = {h} cm',
        schl: function(A){ return 'hd|' + A.A + '|' + A.g; },
        eingabe: function(A){ return { h: String(A.soll) }; },
        neu: function(){
          var g = zufall([4, 5, 6, 8, 10, 12, 7.5]), h = zufall([2, 3, 4, 5, 6, 1.5, 2.4, 4.8]), A = g * h / 2;
          return { g: g, A: r2(A), soll: h, text: 'Ein Dreieck hat die Fläche \\(' + r2(A) + '\\,\\text{cm}^2\\) und die Grundseite \\(' + g + '\\,\\text{cm}\\). Wie lang ist die zugehörige Höhe?' }; },
        fehler: function(A){ return [[{ h: String(r2(A.A / A.g)) }, 'Doppelte']]; },
        pruefen: function(A, e){ return feld(A, 'h', e, A.soll, 'Aus \\(A = \\tfrac{1}{2}\\, g \\cdot h\\) folgt \\(h = \\tfrac{2A}{g}\\).', [[A.A / A.g, 'Das Doppelte: \\(h = \\tfrac{2A}{g}\\) — die \\(\\tfrac{1}{2}\\) der Formel wandert als \\(2\\) nach oben.'], [A.A * A.g * 2, 'Teilen, nicht multiplizieren: \\(h = \\tfrac{2A}{g}\\).']]); },
        loesung: function(A){ return 'h = \\tfrac{2 \\cdot ' + A.A + '}{' + A.g + '} = ' + A.soll + '\\,\\text{cm}'; } },

      /* ── Kapitel 3 ── */
      'viereck': { felder: ['A'], muster: 'A = {A} cm²',
        schl: function(A){ return A.schl; },
        eingabe: function(A){ return { A: String(A.soll) }; },
        neu: function(){
          var art = zufall(['pa', 'tr', 'ra', 'dr']), a, b, c;
          if (art === 'pa'){ a = zufallG(4, 12); b = zufallG(2, 8); return { art: art, schl: 'pa|' + a + '|' + b, soll: a * b, falsch: [[a * b / 2, 'Das ist ein Dreieck. Das Parallelogramm ist \\(a \\cdot h\\) — ganz.']], text: 'Parallelogramm: Grundseite \\(a = ' + a + '\\,\\text{cm}\\), Höhe \\(h = ' + b + '\\,\\text{cm}\\). Fläche?' }; }
          if (art === 'tr'){ a = zufallG(6, 14); c = zufallG(2, a - 2); b = zufallG(2, 7); return { art: art, schl: 'tr|' + a + '|' + c + '|' + b, soll: r2((a + c) / 2 * b), falsch: [[(a + c) * b, 'Das ist das Doppelte: \\(A = \\tfrac{1}{2}(a + c) \\cdot h\\).'], [a * c * b, '\\(A = m \\cdot h\\) mit der Mittellinie \\(m = \\tfrac{1}{2}(a + c)\\).']], text: 'Trapez: Parallelseiten \\(a = ' + a + '\\,\\text{cm}\\), \\(c = ' + c + '\\,\\text{cm}\\), Höhe \\(h = ' + b + '\\,\\text{cm}\\). Fläche?' }; }
          a = zufallG(3, 12); b = zufallG(3, 12); if (a === b) b++;
          return { art: art, schl: art + '|' + a + '|' + b, soll: r2(a * b / 2), falsch: [[a * b, 'Das ist das Rechteck um die Diagonalen. Die Figur füllt genau die Hälfte: \\(\\tfrac{1}{2}\\, e \\cdot f\\).']],
            text: (art === 'ra' ? 'Raute' : 'Drachen') + ': Diagonalen \\(e = ' + a + '\\,\\text{cm}\\), \\(f = ' + b + '\\,\\text{cm}\\). Fläche?' }; },
        fehler: function(A){ return A.falsch.map(function(f){ return [{ A: String(r2(f[0])) }, null]; }).filter(function(f){ return !stimmt(+f[0].A, A.soll); }); },
        pruefen: function(A, e){ return feld(A, 'A', e, A.soll, { pa: '\\(A = a \\cdot h\\).', tr: '\\(A = \\tfrac{1}{2}(a + c) \\cdot h\\).', ra: '\\(A = \\tfrac{1}{2}\\, e \\cdot f\\).', dr: '\\(A = \\tfrac{1}{2}\\, e \\cdot f\\).' }[A.art], A.falsch); },
        loesung: function(A){ return 'A = ' + A.soll + '\\,\\text{cm}^2'; } },

      'pythagoras': { felder: ['x'], muster: 'x ≈ {x} cm',
        schl: function(A){ return 'py|' + A.p + '|' + A.q; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var p = zufall([2, 3, 4, 5, 6, 7, 8, 9, 1.5, 2.5]), q = zufall([3, 4, 5, 6, 8, 10, 12, 2.5]), hyp = Math.random() < 0.6;
          if (hyp || q <= p){ return { p: p, q: q, hyp: true, soll: r2(Math.hypot(p, q)), text: 'Rechtwinkliges Dreieck mit den Katheten \\(' + p + '\\,\\text{cm}\\) und \\(' + q + '\\,\\text{cm}\\). Wie lang ist die Hypotenuse \\(x\\)?' }; }
          return { p: p, q: q, hyp: false, soll: r2(Math.sqrt(q * q - p * p)), text: 'Rechtwinkliges Dreieck mit der Hypotenuse \\(' + q + '\\,\\text{cm}\\) und einer Kathete \\(' + p + '\\,\\text{cm}\\). Wie lang ist die andere Kathete \\(x\\)?' }; },
        fehler: function(A){ return A.hyp ? [[{ x: String(A.p + A.q) }, 'Wurzel']] : [[{ x: String(r2(Math.hypot(A.p, A.q))) }, 'Hypotenuse']]; },
        pruefen: function(A, e){
          return feld(A, 'x', e, A.soll, A.hyp ? '\\(x = \\sqrt{a^2 + b^2}\\).' : '\\(x = \\sqrt{c^2 - a^2}\\): Die Hypotenuse steht allein.',
            [[A.p + A.q, 'Nicht die Längen addieren, sondern die <b>Quadrate</b> — dann die Wurzel.'], [Math.hypot(A.p, A.q), A.hyp ? '' : 'Die Hypotenuse ist gegeben — die gesuchte Kathete ist kürzer: \\(\\sqrt{c^2 - a^2}\\).']]); },
        loesung: function(A){ return 'x = ' + (A.hyp ? '\\sqrt{' + A.p + '^2 + ' + A.q + '^2}' : '\\sqrt{' + A.q + '^2 - ' + A.p + '^2}') + ' \\approx ' + A.soll + '\\,\\text{cm}'; } },

      /* ── Kapitel 4 ── */
      'kreis': { felder: ['U', 'A'], muster: 'U ≈ {U} cm; A ≈ {A} cm²',
        schl: function(A){ return 'kr|' + A.r; },
        eingabe: function(A){ return { U: String(r2(2 * PI * A.r)), A: String(r2(PI * A.r * A.r)) }; },
        neu: function(){
          var r = zufall([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6.5, 7, 9, 10, 12]), d = Math.random() < 0.4;
          return { r: r, d: d, text: d ? 'Ein Kreis hat den Durchmesser \\(d = ' + 2 * r + '\\,\\text{cm}\\). Berechne Umfang und Fläche.' : 'Ein Kreis hat den Radius \\(r = ' + r + '\\,\\text{cm}\\). Berechne Umfang und Fläche.' }; },
        fehler: function(A){ var f = []; if (A.d) f.push([{ U: String(r2(2 * PI * A.r)), A: String(r2(PI * 4 * A.r * A.r)) }, 'Radius']); return f; },
        pruefen: function(A, e){
          var r = [], U = 2 * PI * A.r, F = PI * A.r * A.r;
          var f1 = feld(A, 'U', e, r2(U), '\\(U = 2\\pi r\\).', [[PI * A.r, 'Umfang: \\(2\\pi r\\) — oder \\(\\pi d\\).'], [F, 'Das ist die Fläche — der Umfang ist \\(2\\pi r\\).']]);
          var f2 = feld(A, 'A', e, r2(F), '\\(A = \\pi r^2\\).', [[PI * 4 * A.r * A.r, 'In \\(\\pi r^2\\) gehört der <b>Radius</b> — der halbe Durchmesser.'], [2 * PI * A.r, 'Das ist der Umfang — die Fläche ist \\(\\pi r^2\\).'], [PI * 2 * A.r, '\\(\\pi r^2\\), nicht \\(\\pi \\cdot 2r\\).']]);
          if (f1) r.push('Umfang: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'U = 2\\pi \\cdot ' + A.r + ' \\approx ' + r2(2 * PI * A.r) + ';\\ A = \\pi \\cdot ' + A.r + '^2 \\approx ' + r2(PI * A.r * A.r); } },

      'sektor': { felder: ['b', 'A'], muster: 'b ≈ {b} cm; A ≈ {A} cm²',
        schl: function(A){ return 'sk|' + A.r + '|' + A.phi; },
        eingabe: function(A){ return { b: String(r2(A.phi / 360 * 2 * PI * A.r)), A: String(r2(A.phi / 360 * PI * A.r * A.r)) }; },
        neu: function(){
          var r = zufall([2, 3, 4, 5, 6, 7, 8, 10, 2.5, 4.5]), phi = zufall([30, 40, 45, 60, 72, 80, 100, 120, 135, 150, 210, 240, 270, 300]);
          return { r: r, phi: phi, text: 'Kreissektor mit \\(r = ' + r + '\\,\\text{cm}\\) und \\(\\varphi = ' + phi + '°\\). Berechne Bogenlänge und Fläche.' }; },
        fehler: function(A){ return [[{ b: String(r2(2 * PI * A.r)), A: String(r2(A.phi / 360 * PI * A.r * A.r)) }, 'Anteil']]; },
        pruefen: function(A, e){
          var r = [], q = A.phi / 360, b = q * 2 * PI * A.r, F = q * PI * A.r * A.r;
          var f1 = feld(A, 'b', e, r2(b), '\\(b = \\tfrac{\\varphi}{360°} \\cdot 2\\pi r\\).', [[2 * PI * A.r, 'Das ist der ganze Umfang — der Bogen ist nur der Anteil \\(\\tfrac{' + A.phi + '°}{360°}\\).'], [F, 'Das ist die Fläche.']]);
          var f2 = feld(A, 'A', e, r2(F), '\\(A_S = \\tfrac{\\varphi}{360°} \\cdot \\pi r^2\\).', [[PI * A.r * A.r, 'Das ist die ganze Kreisfläche — der Sektor ist der Anteil \\(\\tfrac{' + A.phi + '°}{360°}\\).'], [b, 'Das ist die Bogenlänge.']]);
          if (f1) r.push('Bogen: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'b \\approx ' + r2(A.phi / 360 * 2 * PI * A.r) + '\\,\\text{cm};\\ A_S \\approx ' + r2(A.phi / 360 * PI * A.r * A.r) + '\\,\\text{cm}^2'; } },

      /* ── Kapitel 5 ── */
      'streckung': { felder: ['L', 'F'], muster: 'Bildstrecke {L} cm; Bildfläche {F} cm²',
        schl: function(A){ return 'st|' + A.k + '|' + A.l; },
        eingabe: function(A){ return { L: String(r2(Math.abs(A.k) * A.l)), F: String(r2(A.k * A.k * A.f)) }; },
        neu: function(){
          var k = zufall([0.5, 1.5, 2, 2.5, 3, 4, -2, -0.5, 1.2]), l = zufall([2, 3, 4, 5, 6, 8]), f = zufall([2, 3, 4, 6, 10, 12]);
          return { k: k, l: l, f: f, text: 'Eine Figur wird zentrisch gestreckt mit \\(k = ' + tz(k) + '\\). Eine Seite ist \\(' + l + '\\,\\text{cm}\\) lang, die Fläche beträgt \\(' + f + '\\,\\text{cm}^2\\). Wie lang ist die Bildseite, wie gross die Bildfläche?' }; },
        fehler: function(A){ return gl(Math.abs(A.k), A.k * A.k) ? [] : [[{ L: String(r2(Math.abs(A.k) * A.l)), F: String(r2(Math.abs(A.k) * A.f)) }, 'Flächen wachsen']]; },
        pruefen: function(A, e){
          var r = [], L = Math.abs(A.k) * A.l, F = A.k * A.k * A.f;
          var f1 = feld(A, 'L', e, r2(L), 'Längen werden mit \\(|k|\\) multipliziert.', [[A.k * A.l, 'Längen sind nie negativ: mit \\(|k|\\) multiplizieren.']]);
          var f2 = feld(A, 'F', e, r2(F), 'Flächen werden mit \\(k^2\\) multipliziert.', [[Math.abs(A.k) * A.f, 'Flächen wachsen mit \\(k^2\\), nicht mit \\(k\\).']]);
          if (f1) r.push('Seite: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return r2(Math.abs(A.k) * A.l) + '\\,\\text{cm};\\ ' + r2(A.k * A.k * A.f) + '\\,\\text{cm}^2'; } },

      'strahlensatz': { felder: ['x'], muster: 'Höhe ≈ {x} m',
        schl: function(A){ return 'sa|' + A.s + '|' + A.sch + '|' + A.gross; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var s = zufall([1.5, 1.6, 1.8, 2, 1.2]), sch = zufall([1.2, 2, 2.4, 2.5, 3, 4]), gross = zufall([6, 8, 9, 10, 12, 15, 18, 20, 24]);
          return { s: s, sch: sch, gross: gross, soll: r2(s / sch * gross), text: 'Ein \\(' + s + '\\,\\text{m}\\) langer Stab wirft einen \\(' + sch + '\\,\\text{m}\\) langen Schatten. Ein Baum daneben wirft einen \\(' + gross + '\\,\\text{m}\\) langen Schatten. Wie hoch ist der Baum?' }; },
        fehler: function(A){ var f = r2(A.sch / A.s * A.gross); return stimmt(f, A.soll) ? [] : [[{ x: String(f) }, 'Verhältnis']]; },
        pruefen: function(A, e){ return feld(A, 'x', e, A.soll, 'Gleicher Sonnenstand: ähnliche Dreiecke, \\(\\tfrac{h}{' + A.gross + '} = \\tfrac{' + A.s + '}{' + A.sch + '}\\).',
          [[A.sch / A.s * A.gross, 'Das Verhältnis steht verkehrt: Höhe zu Schatten beim Baum wie beim Stab, \\(\\tfrac{h}{' + A.gross + '} = \\tfrac{' + A.s + '}{' + A.sch + '}\\).'], [A.gross - A.sch + A.s, 'Nicht addieren oder abziehen — die Längen stehen im gleichen <b>Verhältnis</b>.']]); },
        loesung: function(A){ return 'h = ' + A.gross + ' \\cdot \\tfrac{' + A.s + '}{' + A.sch + '} \\approx ' + A.soll + '\\,\\text{m}'; } }
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
        if (A.einheit) html += A.einheit;
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
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
       Einträge: ["v", [[x,y],…], cls] Vieleck · ["s", [x,y], [x,y], cls] Strecke · ["k", [x,y], r, cls] Kreis ·
       ["sek", [x,y], r, w0, w1, cls] Sektor (Grad) · ["t", [x,y], "Text", cls, dx, dy, anker] · ["p", [x,y]] Punkt ·
       ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel. ---------- */
  document.querySelectorAll('svg.geo-mini[data-fig]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-1,9,-1').split(',').map(Number), b = +(svg.dataset.breite || 220), h = +(svg.dataset.hoehe || 150);
    var F = Flaeche(svg, { w: b, h: h, x0: fe[0], x1: fe[1], y0: fe[2], karo: svg.dataset.karo !== 'nein' });
    JSON.parse(svg.dataset.fig).forEach(function(e){
      var t = e[0];
      if (t === 'v') F.vieleck(e[1], e[2] || 'figur');
      else if (t === 's') F.strecke(e[1], e[2], e[3] || 'hilfe');
      else if (t === 'k') F.kreis(e[1], e[2], e[3] || 'figur kreis');
      else if (t === 'sek') F.sektor(e[1], e[2], grad(e[3]), grad(e[4]), e[5] || 'sektor');
      else if (t === 't') F.text(e[1], e[2], e[3] || 'mass', e[4], e[5], e[6]);
      else if (t === 'p') F.punkt(e[1]);
      else if (t === 'r') F.rechts(e[1], e[2], e[3], 'hilfe');
    });
    svg.setAttribute('role', 'img');
  });
})();
</script>
