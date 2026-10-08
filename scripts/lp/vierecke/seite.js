<script>
/* Leitprogramm Vierecke — Geometrie-Arbeitsbereiche mit Aufgabenleiste, Übungen mit Rückmeldung, Figuren zu
   den Aufgaben. Gerüst (Flaeche, Leiste, arbeitsbereich, Übungsrahmen) wie im Leitprogramm Planimetrie
   (scripts/lp/planimetrie/seite.js) in der Fassung von Trigonometrische Berechnungen (fest, verdeckt,
   Winkelbögen); Inhalte neu.
   Notation wie auf der Themenseite 5.2b: Ecken A, B, C, D gegen den Uhrzeigersinn, Seiten a = AB, b = BC,
   c = CD, d = DA, Winkel α, β, γ, δ, Diagonalen e = AC und f = BD; Trapez mit den Parallelseiten a und c,
   Höhe h, Mittellinie m = ½(a + c). Der Versatz der oberen Seite heisst hier v (die Themenseite schreibt d —
   das ist hier schon die Seite DA).
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Figur · orange = Element (Höhe, Diagonale,
   Mittellinie, Symmetrieachse) · grün = gesuchte Grösse, Teildreieck, Ergebnis · rot = Fehler.
   Dezimalpunkt; gerundet mit «≈». */
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
  /* Vergleich gerundeter Ergebnisse: richtig auf zwei Dezimalen (Toleranz 0.006, je Feld `tol`);
     «nah» heisst: richtig gerechnet, aber zu grob gerundet. */
  function stimmt(e, soll, tol){ return Math.abs(e - soll) <= (tol || 0.006) + 1e-9; }
  function nah(e, soll, tol){ return !stimmt(e, soll, tol) && Math.abs(e - soll) <= Math.max(0.06, Math.abs(soll) * 0.005); }
  var RUNDEN = 'Fast — runde auf zwei Dezimalen (Zwischenresultate ungerundet weiterverwenden).';

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
      s: s, ebene: ebene,
      drehen: function(){},
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      vieleck: function(pts, cls){ return el(ebene, 'polygon', { points: pts.map(P).join(' '), 'class': cls }); },
      strecke: function(a, b, cls){ return el(ebene, 'line', { x1: X(a[0]), y1: Y(a[1]), x2: X(b[0]), y2: Y(b[1]), 'class': cls }); },
      gerade: function(a, b, cls){   // ganze Gerade durch a und b, am Bild abgeschnitten
        var dx = b[0] - a[0], dy = b[1] - a[1], L = 100 / Math.hypot(dx, dy);
        return F.strecke([a[0] - dx * L, a[1] - dy * L], [a[0] + dx * L, a[1] + dy * L], cls); },
      /* Winkelbogen um m von Richtung w0 bis w1 (Bogenmass, gegen den Uhrzeigersinn), Radius in Pixeln */
      bogen: function(m, w0, w1, rpx, cls){
        var r = rpx / s, a = [m[0] + r * Math.cos(w0), m[1] + r * Math.sin(w0)], b = [m[0] + r * Math.cos(w1), m[1] + r * Math.sin(w1)];
        var gross = (w1 - w0) > PI ? 1 : 0;
        return el(ebene, 'path', { d: 'M' + X(a[0]) + ' ' + Y(a[1]) + ' A' + rpx + ' ' + rpx + ' 0 ' + gross + ' 0 ' + X(b[0]) + ' ' + Y(b[1]), 'class': cls }); },
      punkt: function(p, cls){ return el(ebene, 'circle', { cx: X(p[0]), cy: Y(p[1]), r: 3.5, 'class': cls || 'g-pkt' }); },
      /* «h_b» setzt den Index tief (SVG kennt kein LaTeX) */
      text: function(p, t, cls, dx, dy, anker){
        var m = /^(.*?)_(\w)(.*)$/.exec(t);
        var e = el(ebene, 'text', { x: X(p[0]) + (dx || 0), y: Y(p[1]) + (dy || 0), 'text-anchor': anker || 'middle', 'class': 'g-text ' + (cls || '') }, m ? m[1] : t);
        if (m){ el(e, 'tspan', { 'baseline-shift': 'sub', 'font-size': '75%' }, m[2]); if (m[3]) el(e, 'tspan', {}, m[3]); }
        return e; },
      rechts: function(fuss, r1, r2, cls){   // Zeichen für den rechten Winkel, Richtungen als Vektoren
        var q = 8 / s, n1 = Math.hypot(r1[0], r1[1]), n2 = Math.hypot(r2[0], r2[1]);
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
        return gr; }
    };
    return F;
  }
  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function richtung(p, q){ return Math.atan2(q[1] - p[1], q[0] - p[0]); }
  function abst(p, q){ return Math.hypot(p[0] - q[0], p[1] - q[1]); }
  function lot(p, a, b){   // Fusspunkt des Lots von p auf die Gerade ab, dazu t (0 … 1 heisst: auf der Strecke)
    var dx = b[0] - a[0], dy = b[1] - a[1], t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy);
    return [a[0] + t * dx, a[1] + t * dy, t];
  }
  function winkelGrad(p, a, b){   // Innenwinkel bei p zwischen pa und pb, in Grad
    var u = [a[0] - p[0], a[1] - p[1]], v = [b[0] - p[0], b[1] - p[1]];
    return Math.acos(Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]))))) * 180 / PI;
  }
  /* Winkel bei p zwischen den Richtungen zu a und zu b (der kleinere), Beschriftung auf der Winkelhalbierenden. */
  function winkelMarke(F, p, a, b, rpx, cls, text, tcls){
    var w0 = richtung(p, a), w1 = richtung(p, b);
    while (w1 < w0) w1 += 2 * PI;
    if (w1 - w0 > PI){ var t = w0; w0 = w1; w1 = t + 2 * PI; }
    F.bogen(p, w0, w1, rpx, cls);
    if (text){ var wm = (w0 + w1) / 2, r = (rpx + 12) / F.s;
      F.text([p[0] + r * Math.cos(wm), p[1] + r * Math.sin(wm)], text, tcls || 'winkel', 0, 4); }
  }
  /* Beschriftung einer Seite p→q aussen (Ecken gegen den Uhrzeigersinn: aussen ist rechts der Laufrichtung). */
  function seitenText(F, p, q, t, cls, px){
    var m = mitte(p, q), dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy), a = (px || 12) / F.s;
    return F.text([m[0] + dy / L * a, m[1] - dx / L * a], t, cls || 'seite', 0, 4);
  }
  function ecken(F, P, namen){   // Punkte und Namen, je vom Schwerpunkt weg
    var sx = 0, sy = 0; P.forEach(function(p){ sx += p[0]; sy += p[1]; }); sx /= P.length; sy /= P.length;
    P.forEach(function(p, i){ var dx = p[0] - sx, dy = p[1] - sy, L = Math.hypot(dx, dy) || 1;
      F.punkt(p); F.text(p, namen[i], 'ecke', dx / L * 11, -dy / L * 11 + 4); });
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
      // Regler beim Wechsel zurück auf den Startwert (HOWTO §15: kein Endzustand löst die nächste Aufgabe)
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
       text, setup(sim) (Regler setzen: sim.setze({ c: 5 }), sim.sperre('c')),
       wahl: { richtig: 'm', rueck: { id: 'Text' } }      — Linie antippen
       frage: [{ name, label, einheit, soll, tol, fehler: [[wert, 'Text']] }] — Grössen eingeben
       ziel: function(w) — Reglerzustand (w = Werte der Regler, w.bewegt); probe: ein Zustand, der es löst
       verdeckt: ['h'] — die gesuchte Grösse steht neben ihrem Regler als «?» */
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
      aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; aufgabe = null; gewaehlt = null; richtig = false; rueck.className = 'g-rueck'; rueck.innerHTML = ''; eingabeZeigen(); }
    };
    function zeichnen(){
      var w = werte(); w.gewaehlt = gewaehlt; w.richtig = richtig;
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
  function cm(v){ return '\\,\\text{cm}' + (v || ''); }

  /* ---------- Kapitel 1: Die Vierecks-Familie ----------
     Unterschied zur Animation «Vierecks-Familie» der Themenseite: Dort zieht man vier freie Ecken und liest
     Typ und Eigenschaften ab. Hier ist die Figur immer ein Trapez (AB ∥ CD, a = 5 cm fest), drei Regler
     machen daraus Parallelogramm, Rechteck, Rhombus, Quadrat; der Typ steht nicht im Bild — die Seiten- und
     Winkelzeile zeigt, ob die Bedingung erfüllt ist. Dazu Symmetrieachse und Diagonale antippen und Winkel
     berechnen. Startwert c = 3.5, v = 1, h = 3.5: das Trapez aus dem Einführungsclip. */
  var A5 = 5;
  function viereck1(w){ var A = [0, 0], B = [A5, 0], D = [w.v, w.h], C = [w.v + w.c, w.h]; return { A: A, B: B, C: C, D: D }; }
  arbeitsbereich('sim1', {
    fenster: { w: 320, h: 170, x0: -3.6, x1: 10.6, y0: -1.3 },
    zeichnen: function(F, w, k){
      var a = k.aufgabe || {}, P = viereck1(w), A = P.A, B = P.B, C = P.C, D = P.D;
      F.vieleck([A, B, C, D], 'figur');
      if (!k.wahl && !a.frage){ F.strecke(A, C, 'hilfe2'); F.strecke(B, D, 'hilfe2'); }
      if (k.wahl){
        if (a.symm){
          F.kandidat('s', [2.5, 0], [2.5, 1], k.wahl, true);
          F.kandidat('m', mitte(A, D), mitte(B, C), k.wahl);
          F.kandidat('e', A, C, k.wahl);
          F.kandidat('h', D, [D[0], 0], k.wahl);
          if (w.richtig){ F.gerade([2.5, 0], [2.5, 1], 'hilfe'); }
        } else {
          F.kandidat('e', A, C, k.wahl); F.kandidat('f', B, D, k.wahl); F.kandidat('h', D, [D[0], 0], k.wahl);
          if (w.richtig){ F.strecke(A, C, 'hilfe');
            winkelMarke(F, A, B, C, 34, 'winkelbogen', '½α'); winkelMarke(F, A, C, D, 26, 'winkelbogen'); }
        }
      }
      if (a.frage){
        if (a.winkel === 'p'){ winkelMarke(F, A, B, D, 22, 'winkelbogen', '45°'); winkelMarke(F, B, C, A, 18, 'winkelbogen', w.richtig ? '135°' : 'β');
          winkelMarke(F, C, D, B, 22, 'winkelbogen', w.richtig ? '45°' : 'γ'); }
        else { winkelMarke(F, A, B, D, 22, 'winkelbogen', '45°'); F.rechts(B, [-1, 0], [0, 1], 'hilfe'); F.text(B, '90°', 'winkel klein', -16, -16);
          winkelMarke(F, C, D, B, 18, 'winkelbogen', w.richtig ? '90°' : 'γ'); winkelMarke(F, D, A, C, 18, 'winkelbogen', w.richtig ? '135°' : 'δ'); }
      }
      ecken(F, [A, B, C, D], ['A', 'B', 'C', 'D']);
      seitenText(F, A, B, 'a'); seitenText(F, B, C, 'b'); seitenText(F, C, D, 'c'); seitenText(F, D, A, 'd');
      var sb = abst(B, C), sd = abst(D, A), e = abst(A, C), f = abst(B, D);
      var seiten = '\\(a = 5' + cm() + '\\); \\(b ' + zz(sb) + cm() + '\\); \\(c = ' + z(w.c) + cm() + '\\); \\(d ' + zz(sd) + cm() + '\\)';
      if (a.frage) return seiten;
      if (k.wahl) return seiten + (a.symm ? ' — gleichschenkliges Trapez' : ' — Rhombus');
      return seiten + '<br>Diagonalen \\(e ' + zz(e) + cm() + '\\), \\(f ' + zz(f) + cm() + '\\); \\(\\alpha ' + zz(winkelGrad(A, B, D), 1) + '°\\); \\(\\beta ' + zz(winkelGrad(B, C, A), 1)
        + '°\\); \\(\\gamma ' + zz(winkelGrad(C, D, B), 1) + '°\\); \\(\\delta ' + zz(winkelGrad(D, A, C), 1) + '°\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an allen drei Reglern. Welche zwei Seiten bleiben immer parallel?', probe: { v: 2 }, ziel: function(w){ return w.bewegt.c || w.bewegt.v || w.bewegt.h; } },
      { text: 'Mach aus dem Trapez ein Parallelogramm.', probe: { c: 5 }, ziel: function(w){ return w.c === 5; } },
      { text: 'Stell ein Rechteck ein.', probe: { c: 5, v: 0 }, ziel: function(w){ return w.c === 5 && w.v === 0; } },
      { text: 'Stell einen Rhombus ein, der kein Quadrat ist: vier gleich lange Seiten.', probe: { c: 5, v: 3, h: 4 },
        ziel: function(w){ return w.c === 5 && w.v !== 0 && gl(w.v * w.v + w.h * w.h, 25); } },
      { text: 'Stell ein Quadrat ein.', probe: { c: 5, v: 0, h: 5 }, ziel: function(w){ return w.c === 5 && w.v === 0 && w.h === 5; } },
      { text: 'Tipp die Symmetrieachse dieses gleichschenkligen Trapezes an.', symm: true, setup: function(s){ s.setze({ c: 2, v: 1.5, h: 3 }); s.sperre('c', 'v', 'h'); },
        wahl: { richtig: 's', gut: 'Sie geht durch die Mitten von \\(a\\) und \\(c\\) und steht senkrecht auf ihnen. Beim Spiegeln tauschen \\(A\\) und \\(B\\), \\(C\\) und \\(D\\).', rueck: {
          m: 'Das ist die Mittellinie. Spiegelst du an ihr, landet \\(a\\) nicht auf \\(c\\): Die beiden sind verschieden lang.',
          e: 'Das ist die Diagonale \\(e = AC\\). Spiegelst du an ihr, landet \\(B\\) nicht auf \\(D\\).',
          h: 'Das ist eine Höhe durch \\(D\\). Spiegelst du an ihr, landet \\(A\\) nicht auf \\(B\\).' } } },
      { text: 'Tipp in diesem Rhombus die Diagonale an, die den Winkel \\(\\alpha\\) halbiert.', setup: function(s){ s.setze({ c: 5, v: 3, h: 4 }); s.sperre('c', 'v', 'h'); },
        wahl: { richtig: 'e', gut: 'Die Diagonale \\(e = AC\\) halbiert \\(\\alpha\\) und \\(\\gamma\\); \\(f = BD\\) halbiert \\(\\beta\\) und \\(\\delta\\).', rueck: {
          f: 'Die Diagonale \\(f = BD\\) beginnt bei \\(B\\), nicht bei \\(A\\). Welche Diagonale geht durch \\(A\\)?',
          h: 'Das ist eine Höhe, keine Diagonale: Sie verbindet keine zwei Ecken.' } } },
      { text: 'In diesem Parallelogramm ist \\(\\alpha = 45°\\). Wie gross sind \\(\\beta\\) und \\(\\gamma\\)?', winkel: 'p', setup: function(s){ s.setze({ c: 5, v: 3, h: 3 }); s.sperre('c', 'v', 'h'); },
        frage: [{ name: 'beta', label: '\\(\\beta =\\)', einheit: '°', soll: 135, fehler: [[45, '\\(\\beta\\) liegt neben \\(\\alpha\\) an der Seite \\(a\\). Gleich gross sind die gegenüberliegenden Winkel.'], [315, 'Das ist \\(360° - \\alpha\\). Was gilt für zwei Winkel an derselben Seite zwischen zwei Parallelen?']], tipp: 'Benachbarte Winkel im Parallelogramm ergänzen sich zu \\(180°\\).' },
                { name: 'gamma', label: '\\(\\gamma =\\)', einheit: '°', soll: 45, fehler: [[135, '\\(\\gamma\\) liegt \\(\\alpha\\) gegenüber. Was gilt für gegenüberliegende Winkel?']], tipp: 'Gegenüberliegende Winkel sind gleich gross.' }] },
      { text: 'In diesem Trapez ist \\(\\alpha = 45°\\) und \\(\\beta = 90°\\). Wie gross sind \\(\\gamma\\) und \\(\\delta\\)?', winkel: 't', setup: function(s){ s.setze({ c: 3, v: 2, h: 2 }); s.sperre('c', 'v', 'h'); },
        frage: [{ name: 'gamma', label: '\\(\\gamma =\\)', einheit: '°', soll: 90, fehler: [[45, '\\(\\gamma\\) gehört nicht zu \\(\\alpha\\). \\(\\beta\\) und \\(\\gamma\\) liegen am selben Schenkel \\(b\\) zwischen den Parallelen.']], tipp: '\\(\\beta\\) und \\(\\gamma\\) liegen am Schenkel \\(b\\) zwischen den Parallelen \\(a\\) und \\(c\\).' },
                { name: 'delta', label: '\\(\\delta =\\)', einheit: '°', soll: 135, fehler: [[45, '\\(\\delta = \\alpha\\) gilt im Parallelogramm für gegenüberliegende Winkel — hier liegen \\(\\alpha\\) und \\(\\delta\\) am selben Schenkel \\(d\\).'], [225, 'Das ist \\(360° - \\alpha - \\beta\\). Darin steckt \\(\\gamma\\) noch mit.'], [90, '\\(\\delta\\) liegt am Schenkel \\(d\\), zusammen mit \\(\\alpha\\) — nicht mit \\(\\beta\\).']], tipp: '\\(\\alpha\\) und \\(\\delta\\) liegen am Schenkel \\(d\\) zwischen den Parallelen.' }] }
    ]
  });

  /* ---------- Kapitel 2: Fläche und Umfang — Parallelogramm ----------
     Unterschied zu den Animationen «Umformung zum Rechteck» und «Trapez-Scherung» der Themenseite: Hier ist es
     ein Parallelogramm mit Reglern für a, h und den Versatz v; man sieht, dass die Fläche a · h nicht vom
     Versatz abhängt, tippt die Höhe zu a und zu b an und berechnet A, U und den Abstand h_b.
     Startwert a = 8, h = 3, v = 4 (b = 5) wie im Einführungsclip. */
  function viereck2(w){ return { A: [0, 0], B: [w.a, 0], C: [w.a + w.v, w.h], D: [w.v, w.h] }; }
  arbeitsbereich('sim2', {
    fenster: { w: 320, h: 190, x0: -3.6, x1: 14.6, y0: -4.7 },
    zeichnen: function(F, w, k){
      var a = k.aufgabe || {}, P = viereck2(w), A = P.A, B = P.B, C = P.C, D = P.D, b = abst(A, D), hb = a.hb;
      F.vieleck([A, B, C, D], 'figur');
      var fuss = [D[0], 0];
      if (hb){ F.gerade(B, C, 'verlaengerung'); }
      if (k.wahl){
        if (!hb){ F.kandidat('h', D, fuss, k.wahl); F.kandidat('b', A, D, k.wahl); F.kandidat('e', A, C, k.wahl); F.kandidat('f', B, D, k.wahl); }
        else { var L = lot(A, B, C); F.kandidat('hb', A, [L[0], L[1]], k.wahl); F.kandidat('ha', D, fuss, k.wahl); F.kandidat('e', A, C, k.wahl); F.kandidat('f', B, D, k.wahl); }
      }
      var zeigeH = !k.wahl || (w.richtig && !hb);
      if (zeigeH && !(hb && a.frage)){
        if (D[0] < 0 || D[0] > w.a) F.strecke(D[0] < 0 ? A : B, fuss, 'verlaengerung');
        F.strecke(D, fuss, k.wahl ? 'hilfe' : 'hilfe2'); F.rechts(fuss, [0, 1], [D[0] <= w.a / 2 ? 1 : -1, 0], '');
        F.text([D[0], w.h / 2], a.frage && !hb ? 'h = ' + z(w.h) : 'h', 'hilfe', -6, 4, 'end');
      }
      if (hb && (w.richtig || a.frage)){
        var L2 = lot(A, B, C); F.strecke(A, [L2[0], L2[1]], 'hilfe'); F.rechts([L2[0], L2[1]], [-L2[0], -L2[1]], [C[0] - B[0], C[1] - B[1]], '');
        F.text(mitte(A, [L2[0], L2[1]]), a.frage && !w.richtig ? 'h_b = ?' : 'h_b', 'hilfe', -8, 10, 'end');
        if (a.frage){ F.strecke(D, fuss, 'hilfe2'); F.text([D[0], w.h / 2], 'h_a = 4', 'mass', 6, 4, 'start'); }
      }
      ecken(F, [A, B, C, D], ['A', 'B', 'C', 'D']);
      seitenText(F, A, B, 'a'); seitenText(F, D, A, 'b');
      var Af = w.a * w.h, U = 2 * (w.a + b);
      var kopf = '\\(a = ' + z(w.a) + cm() + '\\); \\(b ' + zz(b) + cm() + '\\); \\(h = ' + z(w.h) + cm() + '\\)';
      if (hb) return '\\(a = 8' + cm() + '\\); \\(h_a = 4' + cm() + '\\); \\(b = 5' + cm() + '\\)' + (a.frage ? '; \\(h_b = {?}\\)' : '');
      if (a.frage || a.ohneA) return kopf;
      return kopf + '<br>\\(A = a \\cdot h = ' + z(Af) + cm('^2') + '\\); \\(U = 2(a + b) ' + zz(U) + cm() + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Verschieb die obere Seite mit \\(v\\). Was passiert mit der Fläche, was mit dem Umfang?', probe: { v: 0 }, ziel: function(w){ return w.bewegt.v; } },
      { text: 'Tipp die Höhe zur Grundseite \\(a\\) an.', setup: function(s){ s.setze({ a: 6, h: 3, v: 2 }); s.sperre('a', 'h', 'v'); },
        wahl: { richtig: 'h', gut: 'Die Höhe ist der senkrechte Abstand der Seite \\(c\\) von der Seite \\(a\\).', rueck: {
          b: 'Das ist die Seite \\(b\\) — sie steht schräg, nicht senkrecht auf \\(a\\).',
          e: 'Das ist die Diagonale \\(e = AC\\). Die Höhe steht senkrecht auf \\(a\\).',
          f: 'Das ist die Diagonale \\(f = BD\\). Die Höhe steht senkrecht auf \\(a\\).' } } },
      { text: '\\(a = 6\\,\\text{cm}\\), \\(h = 3\\,\\text{cm}\\), \\(b \\approx 3.61\\,\\text{cm}\\). Berechne Fläche und Umfang.', setup: function(s){ s.setze({ a: 6, h: 3, v: 2 }); s.sperre('a', 'h', 'v'); },
        frage: [{ name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 18, fehler: [[21.63, 'Das ist \\(a \\cdot b\\). Die schräge Seite ist keine Höhe.'], [9, 'Das ist die Hälfte — so rechnet man beim Dreieck. Das Parallelogramm ist ganz \\(a \\cdot h\\).']], tipp: '\\(A = a \\cdot h\\).' },
                { name: 'U', label: '\\(U \\approx\\)', einheit: 'cm', soll: 19.21, tol: 0.011, fehler: [[18, 'Im Umfang zählt die Seite \\(b\\), nicht die Höhe.'], [9.61, 'Das sind nur zwei Seiten. Ein Parallelogramm hat zwei Seiten \\(a\\) und zwei Seiten \\(b\\).']], tipp: '\\(U = 2(a + b)\\).' }] },
      { text: 'Stell ein Parallelogramm mit der Fläche \\(20\\,\\text{cm}^2\\) ein, das kein Rechteck ist.', ohneA: true, probe: { a: 5, h: 4 },
        ziel: function(w){ return gl(w.a * w.h, 20) && w.v !== 0; } },
      { text: 'Stell einen Rhombus ein, der kein Quadrat ist: auch \\(b\\) soll so lang sein wie \\(a\\).', probe: { a: 5, v: 3, h: 4 },
        ziel: function(w){ return w.v !== 0 && gl(Math.hypot(w.v, w.h), w.a); } },
      { text: 'Jetzt ist \\(b = AD\\) die Grundseite. Tipp die zugehörige Höhe \\(h_b\\) an.', hb: true, setup: function(s){ s.setze({ a: 8, h: 4, v: 3 }); s.sperre('a', 'h', 'v'); },
        wahl: { richtig: 'hb', gut: 'Das Lot von \\(A\\) auf die Gerade \\(BC\\): der Abstand der Seiten \\(b\\) und \\(BC\\). Sein Fusspunkt liegt auf der Verlängerung.', rueck: {
          ha: 'Das ist die Höhe zur Grundseite \\(a\\). Zu \\(b\\) gehört der senkrechte Abstand von \\(AD\\) zur Geraden \\(BC\\).',
          e: 'Das ist die Diagonale \\(e = AC\\). Sie steht nicht senkrecht auf \\(BC\\).',
          f: 'Das ist die Diagonale \\(f = BD\\). Sie steht nicht senkrecht auf \\(AD\\).' } } },
      { text: '\\(a = 8\\,\\text{cm}\\), \\(h_a = 4\\,\\text{cm}\\), \\(b = 5\\,\\text{cm}\\). Wie gross ist der Abstand \\(h_b\\) der Seiten \\(AD\\) und \\(BC\\)?', hb: true, setup: function(s){ s.setze({ a: 8, h: 4, v: 3 }); s.sperre('a', 'h', 'v'); },
        frage: [{ name: 'hb', label: '\\(h_b =\\)', einheit: 'cm', soll: 6.4, fehler: [[2.5, 'Umgekehrt: Zuerst die Fläche \\(A = a \\cdot h_a\\), dann durch \\(b\\) teilen.'], [12.8, 'Das ist \\(\\tfrac{2A}{b}\\) — so rechnet man beim Dreieck. Beim Parallelogramm ist \\(A = b \\cdot h_b\\).'], [32, 'Das ist die Fläche. Aus \\(A = b \\cdot h_b\\) folgt \\(h_b\\).']], tipp: 'Die Fläche ist dieselbe, egal welche Seite Grundseite ist: \\(a \\cdot h_a = b \\cdot h_b\\).' }] }
    ]
  });

  /* ---------- Kapitel 3: Trapez und Mittellinie ----------
     Unterschied zur Animation «Trapez-Scherung» der Themenseite (a = 8, Versatz d): Hier a = 6 cm wie im
     Mini-Check und Einführungsclip, Versatz v (d ist die Seite DA); die Leiste lässt die Mittellinie antippen,
     Trapeze mit vorgegebener Mittellinie oder Fläche einstellen und Fläche oder Höhe berechnen.
     Startwert c = 4, h = 3, v = 0.5 (m = 5, A = 15 cm² wie im Clip). */
  var A6 = 6;
  function viereck3(w){ return { A: [0, 0], B: [A6, 0], C: [w.v + w.c, w.h], D: [w.v, w.h] }; }
  arbeitsbereich('sim3', {
    fenster: { w: 320, h: 175, x0: -2.6, x1: 10.6, y0: -1.3 },
    zeichnen: function(F, w, k){
      var a = k.aufgabe || {}, P = viereck3(w), A = P.A, B = P.B, C = P.C, D = P.D, M1 = mitte(A, D), M2 = mitte(B, C);
      F.vieleck([A, B, C, D], 'figur');
      if (k.wahl){
        F.kandidat('m', M1, M2, k.wahl); F.kandidat('e', A, C, k.wahl);
        F.kandidat('x', [A6 / 2, 0], [w.v + w.c / 2, w.h], k.wahl); F.kandidat('hc', C, [C[0], 0], k.wahl);
        if (w.richtig) F.strecke(M1, M2, 'hilfe');
      } else {
        F.strecke(M1, M2, 'hilfe'); F.punkt(M1, 'g-pkt hilfe'); F.punkt(M2, 'g-pkt hilfe');
        F.text(mitte(M1, M2), 'm', 'hilfe', 0, -6);
        var fuss = [D[0], 0];
        if (D[0] < 0 || D[0] > A6) F.strecke(D[0] < 0 ? A : B, fuss, 'verlaengerung');
        F.strecke(D, fuss, 'hilfe2'); F.rechts(fuss, [0, 1], [D[0] <= A6 / 2 ? 1 : -1, 0], '');
        F.text([D[0], w.h * 0.25], (a.verdeckt || []).indexOf('h') >= 0 ? 'h = ?' : 'h', 'mass', -5, 4, 'end');
      }
      ecken(F, [A, B, C, D], ['A', 'B', 'C', 'D']);
      seitenText(F, A, B, 'a'); seitenText(F, C, D, 'c');
      var m = (A6 + w.c) / 2, Af = m * w.h, U = A6 + w.c + abst(B, C) + abst(D, A);
      if (a.rueck) return '\\(A = 14' + cm('^2') + '\\); \\(a = 6' + cm() + '\\); \\(c = 1' + cm() + '\\); \\(h = {?}\\)';
      var kopf = '\\(a = 6' + cm() + '\\); \\(c = ' + z(w.c) + cm() + '\\); \\(h = ' + z(w.h) + cm() + '\\)';
      if (a.frage || a.ohneM) return kopf;
      return kopf + '<br>\\(m = \\tfrac{1}{2}(a + c) = ' + z(m) + cm() + '\\); \\(A = m \\cdot h = ' + z(Af) + cm('^2') + '\\); \\(U ' + zz(U) + cm() + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Verschieb die obere Seite mit \\(v\\). Was bleibt gleich, was ändert sich?', probe: { v: 2 }, ziel: function(w){ return w.bewegt.v; } },
      { text: 'Tipp die Mittellinie \\(m\\) an.', setup: function(s){ s.sperre('c', 'h', 'v'); },
        wahl: { richtig: 'm', gut: 'Sie verbindet die Mitten der Schenkel \\(b\\) und \\(d\\) und liegt auf halber Höhe.', rueck: {
          e: 'Das ist die Diagonale \\(e = AC\\).',
          x: 'Diese Linie verbindet die Mitten der Parallelseiten \\(a\\) und \\(c\\). Die Mittellinie verbindet die Mitten der <b>Schenkel</b>.',
          hc: 'Das ist eine Höhe: Sie steht senkrecht auf \\(a\\) und \\(c\\).' } } },
      { text: 'Stell ein Trapez mit der Mittellinie \\(m = 4.5\\,\\text{cm}\\) ein.', ohneM: true, probe: { c: 3 }, ziel: function(w){ return gl((A6 + w.c) / 2, 4.5); } },
      { text: 'Stell ein Trapez mit der Fläche \\(20\\,\\text{cm}^2\\) ein.', ohneM: true, probe: { h: 4 }, ziel: function(w){ return gl((A6 + w.c) / 2 * w.h, 20); } },
      { text: '\\(c = 5\\,\\text{cm}\\), \\(h = 2.5\\,\\text{cm}\\): Wie lang ist die Mittellinie, wie gross die Fläche?', setup: function(s){ s.setze({ c: 5, h: 2.5, v: 0.5 }); s.sperre('c', 'h', 'v'); },
        frage: [{ name: 'm', label: '\\(m =\\)', einheit: 'cm', soll: 5.5, fehler: [[11, 'Das ist \\(a + c\\). Die Mittellinie ist der <b>Mittelwert</b> von \\(a\\) und \\(c\\).'], [0.5, 'Mittelwert, nicht halbe Differenz.']], tipp: '\\(m = \\tfrac{1}{2}(a + c)\\).' },
                { name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 13.75, fehler: [[27.5, 'Das ist \\((a + c) \\cdot h\\), das Doppelte. Rechne \\(m \\cdot h\\).'], [75, '\\(a \\cdot c \\cdot h\\) ist keine Trapezformel: \\(A = m \\cdot h\\).'], [15, 'Das ist \\(a \\cdot h\\), ein Rechteck. Beim Trapez zählt die Mittellinie.']], tipp: '\\(A = m \\cdot h\\).' }] },
      { text: '\\(A = 14\\,\\text{cm}^2\\), \\(a = 6\\,\\text{cm}\\), \\(c = 1\\,\\text{cm}\\): Wie hoch ist das Trapez?', rueck: true, verdeckt: ['h'], setup: function(s){ s.setze({ c: 1, h: 4, v: 0.5 }); s.sperre('c', 'h', 'v'); },
        frage: [{ name: 'h', label: '\\(h =\\)', einheit: 'cm', soll: 4, fehler: [[2, 'Du hast durch \\(a + c\\) geteilt. Geteilt wird durch die Mittellinie \\(m = \\tfrac{1}{2}(a + c)\\).'], [2.33, 'Du hast durch \\(a\\) geteilt. Es braucht die Mittellinie \\(m = \\tfrac{1}{2}(a + c)\\).'], [49, 'Multipliziert statt geteilt: Aus \\(A = m \\cdot h\\) folgt \\(h = A : m\\).']], tipp: 'Zuerst \\(m = \\tfrac{1}{2}(a + c)\\), dann \\(h = \\tfrac{A}{m}\\).' }] }
    ]
  });

  /* ---------- Kapitel 4: Fehlende Längen — gleichschenkliges Trapez (sim4) und Rhombus (sim5) ----------
     Unterschied zur Themenseite: Dort steht die Trapezhöhe im Fehlerkasten und die Rhombusseite nur in A7
     (Drachen); eine Animation dazu gibt es nicht. Hier zeigt die Figur das rechtwinklige Teildreieck (grün),
     die Leiste lässt die Hypotenuse antippen, ein Trapez mit vorgegebenem Schenkel einstellen und rechnen.
     Startwerte wie im Einführungsclip: a = 12, c = 4, h = 3 (Schenkel 5) und e = 8, f = 6 (Seite 5). */
  arbeitsbereich('sim4', {
    fenster: { w: 320, h: 180, x0: -3, x1: 13.2, y0: -1.9 },
    zeichnen: function(F, w, k){
      var a = k.aufgabe || {}, ue = (w.a - w.c) / 2, A = [0, 0], B = [w.a, 0], D = [ue, w.h], C = [w.a - ue, w.h], s = Math.hypot(ue, w.h);
      F.vieleck([A, B, C, D], 'figur');
      F.vieleck([A, [ue, 0], D], 'teil');
      if (ue < 0) F.strecke(A, [ue, 0], 'verlaengerung');
      if (ue < 0) F.strecke(B, [w.a - ue, 0], 'verlaengerung');
      F.strecke(C, [C[0], 0], 'hilfe2'); F.rechts([C[0], 0], [0, 1], [ue >= 0 ? 1 : -1, 0], '');
      if (k.wahl){
        F.kandidat('d', A, D, k.wahl); F.kandidat('h', D, [ue, 0], k.wahl); F.kandidat('u', A, [ue, 0], k.wahl); F.kandidat('e', A, C, k.wahl);
        if (w.richtig) F.strecke(A, D, 'hilfe');
      } else {
        F.strecke(D, [ue, 0], 'hilfe2'); F.rechts([ue, 0], [0, 1], [ue >= 0 ? -1 : 1, 0], '');
        var vd = a.verdeckt || [];
        F.text([ue, w.h / 2], vd.indexOf('h') >= 0 ? 'h = ?' : 'h', 'mass', 5, 4, 'start');
        F.text([ue / 2, 0], 'ü', 'mass', 0, 14);
        seitenText(F, D, A, a.ohneS ? 's = ?' : 's', 'seite');
      }
      ecken(F, [A, B, C, D], ['A', 'B', 'C', 'D']);
      seitenText(F, A, B, 'a', 'seite', 22); seitenText(F, C, D, 'c');
      if (a.zeile) return a.zeile;
      var kopf = '\\(a = ' + z(w.a) + cm() + '\\); \\(c = ' + z(w.c) + cm() + '\\); \\(h = ' + z(w.h) + cm() + '\\); Überstand \\(\\text{ü} = \\tfrac{a - c}{2} = ' + z(Math.abs(ue)) + cm() + '\\)';
      if (a.ohneS || k.wahl) return kopf;
      return kopf + '<br>Schenkel \\(s = \\sqrt{\\text{ü}^2 + h^2} ' + zz(s) + cm() + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(c\\). Wie lang ist der Überstand links und rechts, und wie lang wird der Schenkel?', probe: { c: 6 }, ziel: function(w){ return w.bewegt.c || w.bewegt.a || w.bewegt.h; } },
      { text: 'Tipp im grünen Teildreieck die Hypotenuse an.', setup: function(s){ s.sperre('a', 'c', 'h'); },
        wahl: { richtig: 'd', gut: 'Der Schenkel liegt dem rechten Winkel gegenüber: \\(s^2 = \\text{ü}^2 + h^2\\).', rueck: {
          h: 'Die Höhe ist eine Kathete: Sie bildet den rechten Winkel. Die Hypotenuse liegt ihm gegenüber.',
          u: 'Der Überstand ist die zweite Kathete. Die Hypotenuse liegt dem rechten Winkel gegenüber.',
          e: 'Die Diagonale gehört nicht zum grünen Dreieck.' } } },
      { text: 'Die Schenkel sollen \\(5\\,\\text{cm}\\) lang sein und die Höhe \\(4\\,\\text{cm}\\). Stell ein solches Trapez ein.', ohneS: true, probe: { h: 4, c: 6 },
        ziel: function(w){ return w.h === 4 && gl(Math.abs(w.a - w.c), 6); } },
      { text: '\\(a = 10\\,\\text{cm}\\), \\(c = 5\\,\\text{cm}\\), Schenkel \\(6.5\\,\\text{cm}\\): Wie hoch ist das Trapez, wie gross seine Fläche?', verdeckt: ['h'],
        zeile: '\\(a = 10' + cm() + '\\); \\(c = 5' + cm() + '\\); Schenkel \\(s = 6.5' + cm() + '\\); \\(h = {?}\\)',
        setup: function(s){ s.setze({ a: 10, c: 5, h: 6 }); s.sperre('a', 'c', 'h'); },
        frage: [{ name: 'h', label: '\\(h =\\)', einheit: 'cm', soll: 6, fehler: [[4.15, 'Der Überstand ist nicht \\(a - c = 5\\), sondern die Hälfte davon.'], [6.96, 'Der Schenkel ist die Hypotenuse: \\(h^2 = s^2 - \\text{ü}^2\\), nicht plus.'], [4, 'Pythagoras gilt für die Quadrate: \\(h = \\sqrt{s^2 - \\text{ü}^2}\\).']], tipp: 'Überstand \\(\\text{ü} = \\tfrac{a - c}{2}\\), dann \\(h = \\sqrt{s^2 - \\text{ü}^2}\\).' },
                { name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 45, fehler: [[48.75, 'Mit dem Schenkel statt der Höhe gerechnet.'], [90, 'Das ist \\((a + c) \\cdot h\\), das Doppelte.']], tipp: '\\(A = \\tfrac{1}{2}(a + c) \\cdot h\\).' }] },
      { text: '\\(a = 7\\,\\text{cm}\\), \\(c = 4\\,\\text{cm}\\), \\(h = 2\\,\\text{cm}\\): Wie lang ist ein Schenkel, wie gross der Umfang?', ohneS: true,
        zeile: '\\(a = 7' + cm() + '\\); \\(c = 4' + cm() + '\\); \\(h = 2' + cm() + '\\); Schenkel \\(s = {?}\\)', setup: function(s){ s.setze({ a: 7, c: 4, h: 2 }); s.sperre('a', 'c', 'h'); },
        frage: [{ name: 's', label: '\\(s =\\)', einheit: 'cm', soll: 2.5, fehler: [[3.5, 'Nicht die Längen addieren, sondern ihre Quadrate — dann die Wurzel.'], [3.61, 'Der Überstand ist die Hälfte von \\(a - c\\), also \\(1.5\\).']], tipp: '\\(s = \\sqrt{\\text{ü}^2 + h^2}\\).' },
                { name: 'U', label: '\\(U =\\)', einheit: 'cm', soll: 16, fehler: [[13.5, 'Das Trapez hat zwei Schenkel.'], [15, 'Im Umfang zählen die Schenkel, nicht die Höhe.']], tipp: '\\(U = a + c + 2s\\).' }] }
    ]
  });
  arbeitsbereich('sim5', {
    fenster: { w: 300, h: 300, x0: -9.4, x1: 9.4, y0: -9.4 },
    zeichnen: function(F, w, k){
      var a = k.aufgabe || {}, e = w.e, f = w.f, A = [-e / 2, 0], B = [0, -f / 2], C = [e / 2, 0], D = [0, f / 2], M = [0, 0], s = Math.hypot(e / 2, f / 2);
      F.vieleck([A, B, C, D], 'figur');
      F.vieleck([M, C, D], 'teil');
      F.strecke(A, C, 'hilfe'); F.strecke(B, D, 'hilfe');
      F.rechts(M, [1, 0], [0, 1], '');
      var vd = a.verdeckt || [];
      F.text([e / 4, 0], 'e/2', 'mass', 0, 14);
      F.text([0, f / 4], vd.indexOf('f') >= 0 ? 'f/2 = ?' : 'f/2', 'mass', -5, 4, 'end');
      seitenText(F, C, D, a.ohneA ? 'a = ?' : 'a', 'seite');
      ecken(F, [A, B, C, D], ['A', 'B', 'C', 'D']);
      if (a.zeile) return a.zeile;
      var kopf = '\\(e = ' + z(e) + cm() + '\\); \\(f = ' + z(f) + cm() + '\\)';
      if (a.ohneA) return kopf;
      return kopf + '<br>Seite \\(a = \\sqrt{(\\tfrac{e}{2})^2 + (\\tfrac{f}{2})^2} ' + zz(s) + cm() + '\\); \\(A = \\tfrac{1}{2}\\, e \\cdot f = ' + z(e * f / 2) + cm('^2') + '\\)';
    },
    aufgaben: [
      { text: 'Erkunde: Zieh an \\(e\\) und \\(f\\). Wo schneiden sich die Diagonalen, und unter welchem Winkel?', probe: { e: 10 }, ziel: function(w){ return w.bewegt.e || w.bewegt.f; } },
      { text: 'Wann ist der Rhombus ein Quadrat? Stell es ein.', probe: { e: 6 }, ziel: function(w){ return w.e === w.f; } },
      { text: 'Stell einen Rhombus mit der Seite \\(a = 6.5\\,\\text{cm}\\) ein.', ohneA: true, probe: { e: 12, f: 5 }, ziel: function(w){ return gl(Math.hypot(w.e / 2, w.f / 2), 6.5); } },
      { text: 'Seite \\(a = 10\\,\\text{cm}\\), Diagonale \\(e = 12\\,\\text{cm}\\): Wie lang ist \\(f\\), wie gross die Fläche?', verdeckt: ['f'],
        zeile: 'Seite \\(a = 10' + cm() + '\\); \\(e = 12' + cm() + '\\); \\(f = {?}\\)',
        setup: function(s){ s.setze({ e: 12, f: 16 }); s.sperre('e', 'f'); },
        frage: [{ name: 'f', label: '\\(f =\\)', einheit: 'cm', soll: 16, fehler: [[8, 'Das ist \\(\\tfrac{f}{2}\\). Die Diagonalen halbieren sich: \\(f\\) ist doppelt so lang.'], [23.32, 'Die Seite \\(a\\) ist die Hypotenuse: \\((\\tfrac{f}{2})^2 = a^2 - (\\tfrac{e}{2})^2\\).']], tipp: '\\((\\tfrac{f}{2})^2 = a^2 - (\\tfrac{e}{2})^2\\), dann verdoppeln.' },
                { name: 'A', label: '\\(A =\\)', einheit: 'cm²', soll: 96, fehler: [[192, 'Das ist \\(e \\cdot f\\), das Rechteck um die Diagonalen. Der Rhombus ist die Hälfte.'], [48, 'Mit \\(\\tfrac{f}{2}\\) statt \\(f\\) gerechnet.']], tipp: '\\(A = \\tfrac{1}{2}\\, e \\cdot f\\).' }] }
    ]
  });

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function r2(v){ return Math.round(v * 100) / 100; }
    function ganz2(v){ return gl(Math.round(v * 100) / 100, v); }   // höchstens zwei Dezimalen
    function sortiert(a, b){ return a < b ? a + '|' + b : b + '|' + a; }
    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Arbeitsbereiche ·
       Kapitelaufgaben · Gesamttest. Je Typ ein eigener Schlüssel. */
    var SPERRE = [
      // familie: fa|X|Y («Jedes X ist ein Y») · fe|X|Eigenschaft
      'fa|Rhombus|Quadrat', 'fa|Quadrat|Rhombus', 'fe|Rechteck|dg', 'fe|Rhombus|dg', 'fe|Parallelogramm|dg', 'fe|Rechteck|dh', 'fe|Rechteck|ds',
      // viereck-winkel: pw|α|gefragt · tw|α|β|gefragt · vw|drei Winkel sortiert
      'pw|45|beta', 'pw|45|gamma', 'pw|45|delta', 'pw|70|beta', 'pw|70|gamma', 'pw|70|delta', 'pw|65|beta', 'pw|65|gamma', 'pw|65|delta',
      'pw|58|beta', 'pw|58|gamma', 'pw|58|delta', 'pw|50|beta', 'pw|50|gamma', 'pw|50|delta', 'pw|110|beta', 'pw|110|gamma', 'pw|110|delta',
      'tw|72|64|gamma', 'tw|72|64|delta', 'vw|75|85|110',
      // pa-flaeche: pa|a|b|h · rh|a|h · re|a|b
      'pa|8|5|3', 'pa|9|6|4', 'pa|7.5|5|4', 'pa|12|7.5|5', 'pa|8|5|4', 'pa|10|5|3', 'pa|7|5|3', 're|5|3', 're|3|5', 're|7|3', 're|3|7',
      // raute-ef: ef|e|f (sortiert) · er|A|e
      'ef|6|8', 'ef|18|24', 'ef|7|10', 'ef|9|12', 'ef|14|48', 'ef|12|16', 'ef|5|12', 'er|24|8', 'er|24|6', 'er|35|10', 'er|35|7', 'er|54|12', 'er|54|9', 'er|96|12', 'er|96|16',
      // abstand: ab|a|h_a|b
      'ab|8|4|5', 'ab|8|3|5', 'ab|10|3|5', 'ab|7.5|4|5', 'ab|12|5|7.5',
      // trapez: tr|a|c|h · trapez-rueck: th|A|a|c · tc|A|h|a
      'tr|6|4|3', 'tr|6|5|2.5', 'tr|9|5|6', 'tr|11|7|4.5', 'tr|8|5|3', 'tr|12|7|4.5', 'tr|6|2|3', 'tr|6|4|4', 'tr|6|2|5', 'tr|12|4|3', 'tr|10|5|6', 'tr|7|4|2',
      'tr|18|8|12', 'tr|20|12|7.5', 'tr|13|7|6', 'tr|10|4|4',
      'th|15|6|4', 'th|12|6|2', 'th|14|6|1', 'th|20|6|4', 'th|20|6|2', 'th|42|9|5', 'th|40.5|11|7', 'th|19.5|8|5', 'th|42.75|12|7', 'th|60|13|7', 'th|45|10|5',
      'tc|15|3|6', 'tc|12|3|6', 'tc|14|4|6', 'tc|42|6|9', 'tc|60|6|13', 'tc|40.5|4.5|11', 'tc|19.5|3|8', 'tc|42.75|4.5|12',
      // diagonale: dr|a|b (sortiert) · dq|a · db|d|a
      'dr|5|12', 'dr|9|12', 'dr|50|89', 'dr|6|8', 'dr|3|4', 'dq|5', 'dq|6', 'db|13|12', 'db|13|5', 'db|15|9', 'db|15|12', 'db|10|6', 'db|10|8',
      // raute-seite: rs|e|f (sortiert) · rf|a|e
      'rs|6|8', 'rs|18|24', 'rs|10|24', 'rs|5|12', 'rs|14|48', 'rs|40|70', 'rs|12|16', 'rf|10|12', 'rf|5|8', 'rf|5|6', 'rf|13|24', 'rf|13|10', 'rf|6.5|12', 'rf|6.5|5', 'rf|17|16', 'rf|17|30', 'rf|10|16',
      // trapez-hoehe: hh|a|c|s · hs|a|c|h
      'hh|12|4|5', 'hh|10|5|6.5', 'hh|20|12|8.5', 'hh|18|8|13', 'hh|10|4|5', 'hh|7|4|2.5', 'hs|12|4|3', 'hs|10|5|6', 'hs|7|4|2', 'hs|20|12|7.5', 'hs|18|8|12', 'hs|10|4|4', 'hs|13|3|12', 'hh|13|3|13'
    ];
    function gesperrt(T, A){ return (T.schl && SPERRE.indexOf(T.schl(A)) >= 0) || (T.extra && T.extra(A)); }
    function feld(e, f, soll, tipp, fehler, tol){
      if (stimmt(e[f], soll, tol)) return null;
      for (var j = 0; fehler && j < fehler.length; j++) if (stimmt(e[f], fehler[j][0], tol)) return fehler[j][1];
      return nah(e[f], soll, tol) ? RUNDEN : tipp;
    }

    /* ── Kapitel 1: die Familie ── */
    var KLASSEN = ['Trapez', 'Parallelogramm', 'Rechteck', 'Rhombus', 'Quadrat'];
    var OBER = { Trapez: ['Trapez'], Parallelogramm: ['Parallelogramm', 'Trapez'], Rechteck: ['Rechteck', 'Parallelogramm', 'Trapez'],
                 Rhombus: ['Rhombus', 'Parallelogramm', 'Trapez'], Quadrat: ['Quadrat', 'Rechteck', 'Rhombus', 'Parallelogramm', 'Trapez'] };
    var JEDES = { Trapez: 'Jedes Trapez', Parallelogramm: 'Jedes Parallelogramm', Rechteck: 'Jedes Rechteck', Rhombus: 'Jeder Rhombus', Quadrat: 'Jedes Quadrat' };
    var EIN = { Trapez: 'ein Trapez', Parallelogramm: 'ein Parallelogramm', Rechteck: 'ein Rechteck', Rhombus: 'ein Rhombus', Quadrat: 'ein Quadrat' };
    var KEIN = { Trapez: 'kein Trapez', Parallelogramm: 'kein Parallelogramm', Rechteck: 'kein Rechteck', Rhombus: 'kein Rhombus', Quadrat: 'kein Quadrat' };
    var DENK = { Trapez: 'ein Trapez, das', Parallelogramm: 'ein Parallelogramm, das', Rechteck: 'ein Rechteck, das', Rhombus: 'einen Rhombus, der', Quadrat: 'ein Quadrat, das' };
    var BED = { Trapez: 'ein Paar paralleler Gegenseiten', Parallelogramm: 'zwei Paare paralleler Gegenseiten', Rechteck: 'vier rechte Winkel (und parallele Gegenseiten)',
                Rhombus: 'vier gleich lange Seiten', Quadrat: 'vier gleich lange Seiten und vier rechte Winkel' };
    /* Eigenschaft: Satz, die allgemeinste Klasse, in der sie immer gilt, und was ein Gegenbeispiel zeigt. */
    var EIG = {
      dh: { satz: 'halbieren sich die Diagonalen gegenseitig', ab: 'Parallelogramm', gegen: 'Seine Diagonalen halbieren sich nicht.' },
      dg: { satz: 'sind die Diagonalen gleich lang', ab: 'Rechteck', gegen: 'Seine Diagonalen sind verschieden lang.' },
      ds: { satz: 'stehen die Diagonalen senkrecht aufeinander', ab: 'Rhombus', gegen: 'Seine Diagonalen stehen nicht senkrecht.' },
      gs: { satz: 'sind alle vier Seiten gleich lang', ab: 'Rhombus', gegen: 'Seine Seiten sind nicht alle gleich lang.' },
      rw: { satz: 'sind alle vier Winkel rechte Winkel', ab: 'Rechteck', gegen: 'Es hat keine rechten Winkel.' },
      gw: { satz: 'sind gegenüberliegende Winkel gleich gross', ab: 'Parallelogramm', gegen: 'Seine gegenüberliegenden Winkel sind verschieden.' },
      pp: { satz: 'sind beide Paare von Gegenseiten parallel', ab: 'Parallelogramm', gegen: 'Nur ein Paar Gegenseiten ist parallel.' }
    };
    var IN = { Trapez: 'In jedem Trapez', Parallelogramm: 'In jedem Parallelogramm', Rechteck: 'In jedem Rechteck', Rhombus: 'In jedem Rhombus', Quadrat: 'In jedem Quadrat' };
    function istEin(X, Y){ return OBER[X].indexOf(Y) >= 0; }

    var TYPEN = {
      'familie': { felder: ['w'], muster: '{w:wahr|falsch}',
        schl: function(A){ return A.art === 'a' ? 'fa|' + A.X + '|' + A.Y : 'fe|' + A.X + '|' + A.E; },
        eingabe: function(A){ return { w: A.soll }; },
        neu: function(){
          var X = zufall(KLASSEN), A;
          if (Math.random() < 0.45){ var Y = zufall(KLASSEN.filter(function(k){ return k !== X; }));
            A = { art: 'a', X: X, Y: Y, wahr: istEin(X, Y), text: 'Wahr oder falsch? «' + JEDES[X] + ' ist ' + EIN[Y] + '.»' }; }
          else { var E = zufall(Object.keys(EIG));
            A = { art: 'e', X: X, E: E, wahr: istEin(X, EIG[E].ab), text: 'Wahr oder falsch? «' + IN[X] + ' ' + EIG[E].satz + '.»' }; }
          A.soll = A.wahr ? 'wahr' : 'falsch';
          return A; },
        fehler: function(A){ return [[{ w: A.wahr ? 'falsch' : 'wahr' }, A.wahr ? 'Doch' : 'Nicht']]; },
        pruefen: function(A, e){
          if (e.w === A.soll) return null;
          if (A.art === 'a'){
            if (A.wahr) return 'Doch: ' + EIN[A.X].replace('ein', 'Ein') + ' hat alles, was ' + EIN[A.Y] + ' braucht — ' + BED[A.Y] + '.';
            return 'Nicht jedes: ' + EIN[A.Y].replace('ein', 'Ein') + ' braucht ' + BED[A.Y] + '. Hat das ' + JEDES[A.X].replace('Jedes', 'jedes').replace('Jeder', 'jeder') + '?';
          }
          var G = EIG[A.E];
          if (A.wahr) return 'Doch: ' + (A.X === G.ab ? 'Das gehört zu jedem ' + A.X + '.' : JEDES[A.X] + ' ist ' + EIN[G.ab] + ', und ' + IN[G.ab].replace('In', 'in') + ' ' + G.satz + '.');
          return 'Nicht in jedem: Denk an ' + DENK[A.X] + ' ' + KEIN[G.ab] + ' ist. ' + G.gegen; },
        loesung: function(A){ return '\\text{' + A.soll + '}'; } },

      'viereck-winkel': { felder: ['w'], muster: '{w} °',
        schl: function(A){ return A.art === 'p' ? 'pw|' + A.al + '|' + A.q : A.art === 't' ? 'tw|' + A.al + '|' + A.be + '|' + A.q : 'vw|' + A.drei.slice().sort(function(x, y){ return x - y; }).join('|'); },
        eingabe: function(A){ return { w: String(A.soll) }; },
        neu: function(){
          var r = Math.random(), NAME = { beta: '\\beta', gamma: '\\gamma', delta: '\\delta' };
          if (r < 0.4){
            var al = zufallG(8, 28) * 5; if (al === 90) al = 95;
            var q = zufall(['beta', 'gamma', 'delta']), fig = zufall(['Parallelogramm', 'Rhombus']);
            return { art: 'p', al: al, q: q, soll: q === 'gamma' ? al : 180 - al,
              text: 'Im ' + fig + ' \\(ABCD\\) ist \\(\\alpha = ' + al + '°\\). Wie gross ist \\(' + NAME[q] + '\\)?' }; }
          if (r < 0.75){
            var a1, b1;
            do { a1 = zufallG(8, 28) * 5; b1 = zufallG(8, 28) * 5; } while (a1 === 90 || b1 === 90 || a1 === b1 || a1 + b1 === 180);
            var q2 = zufall(['gamma', 'delta']);
            return { art: 't', al: a1, be: b1, q: q2, soll: q2 === 'delta' ? 180 - a1 : 180 - b1,
              text: 'Trapez \\(ABCD\\) mit \\(AB \\parallel CD\\): \\(\\alpha = ' + a1 + '°\\), \\(\\beta = ' + b1 + '°\\). Wie gross ist \\(' + NAME[q2] + '\\)?' }; }
          var drei, s;
          do { drei = [zufallG(10, 34) * 5, zufallG(10, 34) * 5, zufallG(10, 34) * 5]; s = drei[0] + drei[1] + drei[2]; } while (s < 200 || s > 320 || 360 - s === 90);
          return { art: 'v', drei: drei, soll: 360 - s,
            text: 'Ein Viereck hat die Winkel \\(\\alpha = ' + drei[0] + '°\\), \\(\\beta = ' + drei[1] + '°\\) und \\(\\gamma = ' + drei[2] + '°\\). Wie gross ist \\(\\delta\\)?' }; },
        fehler: function(A){
          if (A.art === 'p') return A.q === 'gamma' ? [[{ w: String(180 - A.al) }, 'gegenüber']] : [[{ w: String(A.al) }, 'neben'], [{ w: String(360 - A.al) }, '360']];
          if (A.art === 't') return A.q === 'delta' ? [[{ w: String(A.al) }, 'Schenkel'], [{ w: String(180 - A.be) }, 'Schenkel']] : [[{ w: String(A.be) }, 'Schenkel'], [{ w: String(180 - A.al) }, 'Schenkel']];
          var s = A.drei[0] + A.drei[1] + A.drei[2]; return [[{ w: String(s) }, 'Summe']]; },
        pruefen: function(A, e){
          if (gl(e.w, A.soll)) return null;
          if (A.art === 'p'){
            if (A.q === 'gamma' && gl(e.w, 180 - A.al)) return '\\(\\gamma\\) liegt \\(\\alpha\\) gegenüber — gegenüberliegende Winkel sind gleich gross.';
            if (A.q !== 'gamma' && gl(e.w, A.al)) return 'Dieser Winkel liegt neben \\(\\alpha\\), nicht gegenüber. Benachbarte Winkel ergänzen sich zu \\(180°\\).';
            if (gl(e.w, 360 - A.al)) return 'Das ist \\(360° - \\alpha\\). Zwei benachbarte Winkel ergänzen sich zu \\(180°\\).';
            return 'Benachbarte Winkel ergänzen sich zu \\(180°\\), gegenüberliegende sind gleich gross.'; }
          if (A.art === 't'){
            if (A.q === 'delta' && (gl(e.w, A.al) || gl(e.w, 180 - A.be))) return '\\(\\delta\\) liegt mit \\(\\alpha\\) am Schenkel \\(d\\) zwischen den Parallelen: \\(\\alpha + \\delta = 180°\\).';
            if (A.q === 'gamma' && (gl(e.w, A.be) || gl(e.w, 180 - A.al))) return '\\(\\gamma\\) liegt mit \\(\\beta\\) am Schenkel \\(b\\) zwischen den Parallelen: \\(\\beta + \\gamma = 180°\\).';
            return 'Die zwei Winkel an einem Schenkel ergänzen sich zu \\(180°\\).'; }
          var s = A.drei[0] + A.drei[1] + A.drei[2];
          if (gl(e.w, s)) return 'Das ist die Summe der drei Winkel. Die vier Winkel ergeben zusammen \\(360°\\).';
          return 'Die Winkelsumme im Viereck ist \\(360°\\).'; },
        loesung: function(A){ return A.soll + '°'; } },

      /* ── Kapitel 2 ── */
      'pa-flaeche': { felder: ['A', 'U'], muster: 'A = {A} cm²; U = {U} cm',
        schl: function(A){ return A.art === 'pa' ? 'pa|' + A.a + '|' + A.b + '|' + A.h : A.art === 'rh' ? 'rh|' + A.a + '|' + A.h : 're|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { A: String(A.F), U: String(A.U) }; },
        neu: function(){
          var r = Math.random(), a, b, h;
          if (r < 0.55){ a = zufall([5, 6, 7, 8, 9, 10, 11, 12, 6.5, 7.5]); h = zufall([2, 3, 4, 5, 2.5, 3.5]); b = h + zufall([1, 1.5, 2, 3, 4]);
            return { art: 'pa', a: a, b: b, h: h, F: r2(a * h), U: r2(2 * (a + b)),
              text: 'Parallelogramm: Grundseite \\(a = ' + a + '\\,\\text{cm}\\), zweite Seite \\(b = ' + b + '\\,\\text{cm}\\), Höhe auf \\(a\\): \\(h = ' + h + '\\,\\text{cm}\\). Berechne Fläche und Umfang.' }; }
          if (r < 0.85){ a = zufall([4, 5, 6, 7, 8, 9, 10]); h = a - zufall([0.5, 1, 1.5, 2]);
            return { art: 'rh', a: a, h: h, F: r2(a * h), U: 4 * a,
              text: 'Rhombus mit der Seite \\(a = ' + a + '\\,\\text{cm}\\) und der Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne Fläche und Umfang.' }; }
          a = zufall([4, 6, 7, 8, 9, 12, 2.5, 4.5]); b = zufall([2, 3, 5, 1.5, 3.5]);
          return { art: 're', a: a, b: b, F: r2(a * b), U: r2(2 * (a + b)), text: 'Rechteck mit \\(a = ' + a + '\\,\\text{cm}\\) und \\(b = ' + b + '\\,\\text{cm}\\). Berechne Fläche und Umfang.' }; },
        fehler: function(A){
          if (A.art === 'pa') return [[{ A: String(r2(A.a * A.b)), U: String(A.U) }, 'schräge'], [{ A: String(r2(A.a * A.h / 2)), U: String(A.U) }, 'Dreieck'], [{ A: String(A.F), U: String(r2(2 * (A.a + A.h))) }, 'nicht die Höhe']];
          if (A.art === 'rh') return [[{ A: String(r2(A.a * A.a)), U: String(A.U) }, 'Quadrat'], [{ A: String(A.F), U: String(r2(2 * A.a)) }, 'vier']];
          return [[{ A: String(A.F), U: String(r2(A.a + A.b)) }, 'zwei']]; },
        pruefen: function(A, e){
          var r = [], f1, f2;
          if (A.art === 'pa'){
            f1 = feld(e, 'A', A.F, '\\(A = a \\cdot h\\).', [[A.a * A.b, 'Das ist \\(a \\cdot b\\) — die schräge Seite ist keine Höhe.'], [A.a * A.h / 2, 'Die Hälfte gilt beim Dreieck. Das Parallelogramm ist ganz \\(a \\cdot h\\).']]);
            f2 = feld(e, 'U', A.U, '\\(U = 2(a + b)\\).', [[2 * (A.a + A.h), 'Im Umfang zählt die Seite \\(b\\), nicht die Höhe.'], [A.a + A.b, 'Das sind zwei Seiten — es braucht alle vier: zweimal \\(a\\) und zweimal \\(b\\).']]);
          } else if (A.art === 'rh'){
            f1 = feld(e, 'A', A.F, '\\(A = a \\cdot h\\) — der Rhombus ist ein Parallelogramm.', [[A.a * A.a, 'Das wäre ein Quadrat. Beim Rhombus zählt die Höhe: \\(A = a \\cdot h\\).'], [A.a * A.h / 2, 'Die Hälfte gilt beim Dreieck.']]);
            f2 = feld(e, 'U', A.U, 'Vier gleich lange Seiten: \\(U = 4a\\).', [[2 * A.a, 'Ein Rhombus hat vier gleich lange Seiten: \\(U = 4a\\).'], [2 * (A.a + A.h), 'Im Umfang zählen die Seiten, nicht die Höhe.']]);
          } else {
            f1 = feld(e, 'A', A.F, '\\(A = a \\cdot b\\).', [[2 * (A.a + A.b), 'Das ist der Umfang.']]);
            f2 = feld(e, 'U', A.U, '\\(U = 2(a + b)\\).', [[A.a + A.b, 'Das sind zwei Seiten — das Rechteck hat vier.'], [A.a * A.b, 'Das ist die Fläche.']]);
          }
          if (f1) r.push('Fläche: ' + f1); if (f2) r.push('Umfang: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'A = ' + (A.art === 're' ? A.a + ' \\cdot ' + A.b : A.a + ' \\cdot ' + A.h) + ' = ' + A.F + '\\,\\text{cm}^2;\\ U = ' + A.U + '\\,\\text{cm}'; } },

      'raute-ef': { felder: ['x'], muster: '{x}',
        schl: function(A){ return A.vor ? 'ef|' + sortiert(A.e, A.f) : 'er|' + A.F + '|' + A.e; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var e, f;
          do { e = zufallG(3, 16); f = zufallG(3, 16); } while (e === f || gl(e + f, e * f / 2));   // sonst gälte die Summe als richtig
          var F = r2(e * f / 2);
          if (Math.random() < 0.55) return { vor: true, e: e, f: f, F: F, soll: F, einheit: 'cm²',
            text: 'Rhombus mit den Diagonalen \\(e = ' + e + '\\,\\text{cm}\\) und \\(f = ' + f + '\\,\\text{cm}\\). Wie gross ist die Fläche \\(A\\) (in cm²)?' };
          return { vor: false, e: e, f: f, F: F, soll: f, einheit: 'cm',
            text: 'Ein Rhombus hat die Fläche \\(' + F + '\\,\\text{cm}^2\\) und die Diagonale \\(e = ' + e + '\\,\\text{cm}\\). Wie lang ist die Diagonale \\(f\\) (in cm)?' }; },
        fehler: function(A){ return A.vor ? [[{ x: String(A.e * A.f) }, 'Hälfte'], [{ x: String(A.e + A.f) }, 'Produkt']] : (gl(A.F / A.e, A.f) ? [] : [[{ x: String(r2(A.F / A.e)) }, 'doppelt']]); },
        pruefen: function(A, e){
          if (A.vor) return feld(e, 'x', A.soll, '\\(A = \\tfrac{1}{2}\\, e \\cdot f\\).', [[A.e * A.f, 'Das ist das Rechteck um die Diagonalen. Der Rhombus füllt genau die Hälfte davon.'], [A.e + A.f, 'Eine Fläche ist ein Produkt, keine Summe: \\(\\tfrac{1}{2}\\, e \\cdot f\\).']]);
          return feld(e, 'x', A.soll, 'Aus \\(A = \\tfrac{1}{2}\\, e \\cdot f\\) folgt \\(f = \\tfrac{2A}{e}\\).', [[A.F / A.e, 'Das ist die Hälfte. Wegen des \\(\\tfrac{1}{2}\\) ist \\(f = \\tfrac{2A}{e}\\) — doppelt so viel.'], [A.F * A.e, 'Teilen, nicht multiplizieren: \\(f = \\tfrac{2A}{e}\\).']]); },
        loesung: function(A){ return A.vor ? 'A = \\tfrac{1}{2} \\cdot ' + A.e + ' \\cdot ' + A.f + ' = ' + A.F + '\\,\\text{cm}^2' : 'f = \\tfrac{2 \\cdot ' + A.F + '}{' + A.e + '} = ' + A.f + '\\,\\text{cm}'; } },

      'abstand': { felder: ['hb'], muster: 'h<sub>b</sub> = {hb} cm',
        schl: function(A){ return 'ab|' + A.a + '|' + A.ha + '|' + A.b; },
        eingabe: function(A){ return { hb: String(A.soll) }; },
        neu: function(){
          var a, b, ha, hb, n = 0;
          do { a = zufall([6, 7, 8, 9, 10, 12, 14, 15, 7.5]); b = zufall([4, 5, 6, 8, 10]); ha = zufallG(2, b - 1); hb = a * ha / b; n++; }
          while ((a === b || !ganz2(hb) || !ganz2(b * ha / a) || gl(hb, b * ha / a)) && n < 200);
          return { a: a, b: b, ha: ha, F: a * ha, soll: r2(hb),
            text: 'Parallelogramm mit \\(a = ' + a + '\\,\\text{cm}\\), \\(b = ' + b + '\\,\\text{cm}\\) und der Höhe \\(h_a = ' + ha + '\\,\\text{cm}\\) auf \\(a\\). Wie gross ist der Abstand \\(h_b\\) der beiden Seiten \\(b\\)?' }; },
        fehler: function(A){ return [[{ hb: String(r2(A.b * A.ha / A.a)) }, 'Umgekehrt'], [{ hb: String(r2(2 * A.F / A.b)) }, 'Dreieck']]; },
        pruefen: function(A, e){ return feld(e, 'hb', A.soll, 'Zuerst \\(A = a \\cdot h_a\\), dann \\(h_b = \\tfrac{A}{b}\\).',
          [[A.b * A.ha / A.a, 'Umgekehrt: Die Fläche ist \\(a \\cdot h_a\\), und \\(h_b\\) ist diese Fläche geteilt durch \\(b\\).'], [2 * A.F / A.b, 'Das ist \\(\\tfrac{2A}{b}\\) — so rechnet man beim Dreieck. Beim Parallelogramm: Dreieck-Formel ohne \\(\\tfrac{1}{2}\\), \\(A = b \\cdot h_b\\).'], [A.F, 'Das ist die Fläche \\(a \\cdot h_a\\). Jetzt noch durch \\(b\\) teilen.']]); },
        loesung: function(A){ return 'A = ' + A.a + ' \\cdot ' + A.ha + ' = ' + A.F + ';\\ h_b = \\tfrac{' + A.F + '}{' + A.b + '} = ' + A.soll + '\\,\\text{cm}'; } },

      /* ── Kapitel 3 ── */
      'trapez': { felder: ['m', 'A'], muster: 'm = {m} cm; A = {A} cm²',
        schl: function(A){ return 'tr|' + A.a + '|' + A.c + '|' + A.h; },
        extra: function(A){ return (A.a === 12 && A.c === 8) || (A.a === 14 && A.c === 8); },   // Kontrollclips 3 und 4: m bzw. Überstand
        eingabe: function(A){ return { m: String(A.m), A: String(A.F) }; },
        neu: function(){
          var a = zufallG(6, 16), c = zufallG(2, a - 2), h = zufall([2, 3, 4, 5, 6, 7, 8, 2.5, 3.5, 4.5]);
          if (Math.random() < 0.3) c = c + 0.5;
          return { a: a, c: c, h: h, m: (a + c) / 2, F: r2((a + c) / 2 * h),
            text: 'Trapez mit den Parallelseiten \\(a = ' + a + '\\,\\text{cm}\\) und \\(c = ' + c + '\\,\\text{cm}\\), Höhe \\(h = ' + h + '\\,\\text{cm}\\). Berechne die Mittellinie und die Fläche.' }; },
        fehler: function(A){ return [[{ m: String(A.a + A.c), A: String(A.F) }, 'Mittelwert'], [{ m: String(A.m), A: String(r2((A.a + A.c) * A.h)) }, 'Doppelte']]; },
        pruefen: function(A, e){
          var r = [];
          var f1 = feld(e, 'm', A.m, '\\(m = \\tfrac{1}{2}(a + c)\\).', [[A.a + A.c, 'Das ist \\(a + c\\). Die Mittellinie ist der <b>Mittelwert</b> von \\(a\\) und \\(c\\).'], [(A.a - A.c) / 2, 'Mittelwert, nicht halbe Differenz: \\(m = \\tfrac{1}{2}(a + c)\\).']]);
          var f2 = feld(e, 'A', A.F, '\\(A = m \\cdot h\\).', [[(A.a + A.c) * A.h, 'Das ist das Doppelte, \\((a + c) \\cdot h\\). Rechne \\(m \\cdot h\\).'], [A.a * A.c * A.h, '\\(a \\cdot c \\cdot h\\) ist keine Trapezformel: \\(A = m \\cdot h\\).'], [A.a * A.h, 'Das ist \\(a \\cdot h\\), ein Rechteck. Beim Trapez zählt die Mittellinie.']]);
          if (f1) r.push('Mittellinie: ' + f1); if (f2) r.push('Fläche: ' + f2);
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return 'm = \\tfrac{1}{2}(' + A.a + ' + ' + A.c + ') = ' + A.m + ';\\ A = ' + A.m + ' \\cdot ' + A.h + ' = ' + A.F + '\\,\\text{cm}^2'; } },

      'trapez-rueck': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return A.was === 'h' ? 'th|' + A.F + '|' + A.a + '|' + A.c : 'tc|' + A.F + '|' + A.h + '|' + A.a; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var a = zufallG(6, 15), c = zufallG(2, a - 2), h = zufall([2, 3, 4, 5, 6, 8, 2.5, 1.5]), F = (a + c) / 2 * h;
          if (!ganz2(F)) h = Math.round(h), F = (a + c) / 2 * h;
          if (Math.random() < 0.5) return { was: 'h', a: a, c: c, h: h, F: F, soll: h,
            text: 'Ein Trapez hat die Fläche \\(' + F + '\\,\\text{cm}^2\\) und die Parallelseiten \\(a = ' + a + '\\,\\text{cm}\\) und \\(c = ' + c + '\\,\\text{cm}\\). Wie hoch ist es?' };
          return { was: 'c', a: a, c: c, h: h, F: F, soll: c,
            text: 'Ein Trapez hat die Fläche \\(' + F + '\\,\\text{cm}^2\\), die Höhe \\(h = ' + h + '\\,\\text{cm}\\) und die Grundseite \\(a = ' + a + '\\,\\text{cm}\\). Wie lang ist die zweite Parallelseite \\(c\\)?' }; },
        fehler: function(A){ var m = (A.a + A.c) / 2;
          if (A.was === 'h') return [[{ x: String(r2(A.F / (A.a + A.c))) }, 'Mittellinie'], [{ x: String(r2(A.F / A.a)) }, 'Mittellinie']].filter(function(f){ return !stimmt(+f[0].x, A.soll); });
          return [[{ x: String(r2(2 * A.F / A.h)) }, 'a + c'], [{ x: String(r2(A.F / A.h - A.a)) }, 'Mittellinie']].filter(function(f){ return !stimmt(+f[0].x, A.soll); }); },
        pruefen: function(A, e){
          if (A.was === 'h') return feld(e, 'x', A.soll, 'Zuerst \\(m = \\tfrac{1}{2}(a + c)\\), dann \\(h = \\tfrac{A}{m}\\).',
            [[A.F / (A.a + A.c), 'Du hast durch \\(a + c\\) geteilt. Geteilt wird durch die Mittellinie \\(m = \\tfrac{1}{2}(a + c)\\).'], [A.F / A.a, 'Du hast durch \\(a\\) geteilt. Es braucht die Mittellinie \\(m = \\tfrac{1}{2}(a + c)\\).']]);
          return feld(e, 'x', A.soll, 'Aus \\(A = m \\cdot h\\) folgt \\(m = \\tfrac{A}{h}\\), und aus \\(m = \\tfrac{1}{2}(a + c)\\) folgt \\(c = 2m - a\\).',
            [[2 * A.F / A.h, 'Das ist \\(a + c\\). Zieh noch \\(a\\) ab.'], [A.F / A.h - A.a, 'Das ist \\(m - a\\). Die Mittellinie ist erst die Hälfte von \\(a + c\\): \\(c = 2m - a\\).'], [A.F / A.h, 'Das ist die Mittellinie \\(m\\). Aus \\(m = \\tfrac{1}{2}(a + c)\\) folgt \\(c\\).']]); },
        loesung: function(A){ var m = (A.a + A.c) / 2;
          return A.was === 'h' ? 'm = ' + m + ';\\ h = \\tfrac{' + A.F + '}{' + m + '} = ' + A.h + '\\,\\text{cm}' : 'm = \\tfrac{' + A.F + '}{' + A.h + '} = ' + m + ';\\ c = 2 \\cdot ' + m + ' - ' + A.a + ' = ' + A.c + '\\,\\text{cm}'; } },

      /* ── Kapitel 4 ── */
      'diagonale': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return A.art === 'r' ? 'dr|' + sortiert(A.a, A.b) : A.art === 'q' ? 'dq|' + A.a : 'db|' + A.d + '|' + A.a; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var r = Math.random(), a, b;
          if (r < 0.45){ a = zufallG(3, 15); b = zufallG(2, 12); if (a === b) b++;
            return { art: 'r', a: a, b: b, soll: r2(Math.hypot(a, b)), text: 'Rechteck mit \\(a = ' + a + '\\,\\text{cm}\\) und \\(b = ' + b + '\\,\\text{cm}\\). Wie lang ist die Diagonale \\(d\\)?' }; }
          if (r < 0.7){ a = zufall([3, 4, 7, 8, 9, 10, 12, 2.5, 4.5]);
            return { art: 'q', a: a, soll: r2(a * Math.SQRT2), text: 'Quadrat mit der Seite \\(a = ' + a + '\\,\\text{cm}\\). Wie lang ist die Diagonale \\(d\\)?' }; }
          var T = zufall([[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [6, 8, 10], [9, 12, 15], [2.5, 6, 6.5], [4.5, 6, 7.5]]), k = Math.random() < 0.5;
          a = k ? T[0] : T[1]; b = k ? T[1] : T[0];
          return { art: 'b', d: T[2], a: a, soll: b, text: 'Ein Rechteck hat die Diagonale \\(d = ' + T[2] + '\\,\\text{cm}\\) und die Seite \\(a = ' + a + '\\,\\text{cm}\\). Wie lang ist die Seite \\(b\\)?' }; },
        fehler: function(A){
          if (A.art === 'r') return [[{ x: String(A.a + A.b) }, 'Quadrate'], [{ x: String(r2(Math.max(A.a, A.b) * Math.SQRT2)) }, 'Quadrat']];
          if (A.art === 'q') return [[{ x: String(2 * A.a) }, 'Quadrate']];
          return [[{ x: String(r2(Math.hypot(A.d, A.a))) }, 'Hypotenuse'], [{ x: String(r2(A.d - A.a)) }, 'Quadrate']]; },
        pruefen: function(A, e){
          if (A.art === 'r') return feld(e, 'x', A.soll, 'Die Diagonale ist die Hypotenuse: \\(d = \\sqrt{a^2 + b^2}\\).',
            [[A.a + A.b, 'Nicht die Seiten addieren, sondern ihre <b>Quadrate</b> — dann die Wurzel.'], [A.a * Math.SQRT2, '\\(d = a\\sqrt{2}\\) gilt nur im Quadrat.'], [A.b * Math.SQRT2, '\\(d = a\\sqrt{2}\\) gilt nur im Quadrat.']]);
          if (A.art === 'q') return feld(e, 'x', A.soll, 'Im Quadrat: \\(d = \\sqrt{a^2 + a^2} = a\\sqrt{2}\\).',
            [[2 * A.a, 'Nicht die Seiten addieren, sondern ihre <b>Quadrate</b>: \\(d = \\sqrt{a^2 + a^2}\\).'], [A.a * A.a, 'Das ist die Fläche.']]);
          return feld(e, 'x', A.soll, 'Die Diagonale ist die Hypotenuse: \\(b = \\sqrt{d^2 - a^2}\\).',
            [[Math.hypot(A.d, A.a), 'Die Diagonale ist schon die Hypotenuse. Die gesuchte Seite ist kürzer: \\(b = \\sqrt{d^2 - a^2}\\).'], [A.d - A.a, 'Nicht die Längen subtrahieren, sondern ihre <b>Quadrate</b>.']]); },
        loesung: function(A){ return A.art === 'r' ? 'd = \\sqrt{' + A.a + '^2 + ' + A.b + '^2} \\approx ' + A.soll : A.art === 'q' ? 'd = ' + A.a + '\\sqrt{2} \\approx ' + A.soll : 'b = \\sqrt{' + A.d + '^2 - ' + A.a + '^2} = ' + A.soll; } },

      'raute-seite': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return A.vor ? 'rs|' + sortiert(A.e, A.f) : 'rf|' + A.a + '|' + A.e; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          if (Math.random() < 0.55){ var e = 2 * zufallG(2, 10), f = 2 * zufallG(2, 10); if (e === f) f += 2;
            return { vor: true, e: e, f: f, soll: r2(Math.hypot(e / 2, f / 2)), text: 'Rhombus mit den Diagonalen \\(e = ' + e + '\\,\\text{cm}\\) und \\(f = ' + f + '\\,\\text{cm}\\). Wie lang ist eine Seite \\(a\\)?' }; }
          var T = zufall([[3, 4, 5], [5, 12, 13], [8, 15, 17], [6, 8, 10], [9, 12, 15], [2.5, 6, 6.5], [4.5, 6, 7.5], [12, 16, 20]]), k = Math.random() < 0.5;
          var ehalb = k ? T[0] : T[1], fhalb = k ? T[1] : T[0];
          return { vor: false, a: T[2], e: 2 * ehalb, soll: 2 * fhalb, text: 'Ein Rhombus hat die Seite \\(a = ' + T[2] + '\\,\\text{cm}\\) und die Diagonale \\(e = ' + 2 * ehalb + '\\,\\text{cm}\\). Wie lang ist die Diagonale \\(f\\)?' }; },
        fehler: function(A){
          if (A.vor) return [[{ x: String((A.e + A.f) / 2) }, 'Quadrate'], [{ x: String(r2(Math.hypot(A.e, A.f))) }, 'Hälften']];
          return [[{ x: String(A.soll / 2) }, 'doppelt'], [{ x: String(r2(2 * Math.hypot(A.a, A.e / 2))) }, 'Hypotenuse']]; },
        pruefen: function(A, e){
          if (A.vor) return feld(e, 'x', A.soll, 'Die Diagonalen halbieren sich senkrecht: \\(a = \\sqrt{(\\tfrac{e}{2})^2 + (\\tfrac{f}{2})^2}\\).',
            [[(A.e + A.f) / 2, 'Nicht die Hälften addieren, sondern ihre <b>Quadrate</b> — dann die Wurzel.'], [Math.hypot(A.e, A.f), 'Die Katheten sind die <b>Hälften</b> der Diagonalen: \\(\\tfrac{e}{2}\\) und \\(\\tfrac{f}{2}\\).']]);
          return feld(e, 'x', A.soll, '\\((\\tfrac{f}{2})^2 = a^2 - (\\tfrac{e}{2})^2\\), dann verdoppeln.',
            [[A.soll / 2, 'Das ist \\(\\tfrac{f}{2}\\). Die Diagonalen halbieren sich: \\(f\\) ist doppelt so lang.'], [2 * Math.hypot(A.a, A.e / 2), 'Die Seite \\(a\\) ist die Hypotenuse: \\((\\tfrac{f}{2})^2 = a^2 - (\\tfrac{e}{2})^2\\).']]); },
        loesung: function(A){ return A.vor ? 'a = \\sqrt{' + A.e / 2 + '^2 + ' + A.f / 2 + '^2} \\approx ' + A.soll : '\\tfrac{f}{2} = \\sqrt{' + A.a + '^2 - ' + A.e / 2 + '^2} = ' + A.soll / 2 + ';\\ f = ' + A.soll; } },

      'trapez-hoehe': { felder: ['x'], muster: '{x} cm',
        schl: function(A){ return A.was === 'h' ? 'hh|' + A.a + '|' + A.c + '|' + A.s : 'hs|' + A.a + '|' + A.c + '|' + A.h; },
        extra: function(A){ return A.a === 14 && A.c === 8; },
        eingabe: function(A){ return { x: String(A.soll) }; },
        neu: function(){
          var T = zufall([[3, 4, 5], [4, 3, 5], [5, 12, 13], [12, 5, 13], [8, 6, 10], [6, 8, 10], [1.5, 2, 2.5], [2, 1.5, 2.5], [2.5, 6, 6.5], [4.5, 6, 7.5], [6, 4.5, 7.5], [2, 3, 3.61], [3, 5, 5.83], [1, 4, 4.12]]);
          var ue = T[0], h = T[1], c = zufallG(2, 10), a = c + 2 * ue;
          if (Math.abs(ue + h - Math.hypot(2 * ue, h)) < 0.02) return TYPEN['trapez-hoehe'].neu();   // zwei Fehler gäben dieselbe Zahl
          if (Math.random() < 0.5) return { was: 's', a: a, c: c, h: h, ue: ue, soll: r2(Math.hypot(ue, h)),
            text: 'Gleichschenkliges Trapez mit \\(a = ' + a + '\\,\\text{cm}\\), \\(c = ' + c + '\\,\\text{cm}\\) und der Höhe \\(h = ' + h + '\\,\\text{cm}\\). Wie lang ist ein Schenkel \\(s\\)?' };
          if (!gl(T[2], Math.hypot(T[0], T[1]))) return TYPEN['trapez-hoehe'].neu();   // gerundete Schenkel nur als Ergebnis
          return { was: 'h', a: a, c: c, s: T[2], ue: ue, soll: h,
            text: 'Gleichschenkliges Trapez mit \\(a = ' + a + '\\,\\text{cm}\\), \\(c = ' + c + '\\,\\text{cm}\\) und den Schenkeln \\(s = ' + T[2] + '\\,\\text{cm}\\). Wie hoch ist es?' }; },
        fehler: function(A){
          if (A.was === 's') return [[{ x: String(A.ue + A.h) }, 'Quadrate'], [{ x: String(r2(Math.hypot(2 * A.ue, A.h))) }, 'Hälfte']].filter(function(f){ return !stimmt(+f[0].x, A.soll); });
          var f = [[{ x: String(r2(Math.hypot(A.s, A.ue))) }, 'Hypotenuse'], [{ x: String(r2(A.s - A.ue)) }, 'Quadrate']];
          if (A.s > 2 * A.ue) f.push([{ x: String(r2(Math.sqrt(A.s * A.s - 4 * A.ue * A.ue))) }, 'Hälfte']);
          return f.filter(function(g){ return !stimmt(+g[0].x, A.soll); }); },
        pruefen: function(A, e){
          if (A.was === 's') return feld(e, 'x', A.soll, 'Überstand \\(\\text{ü} = \\tfrac{a - c}{2}\\), dann \\(s = \\sqrt{\\text{ü}^2 + h^2}\\).',
            [[A.ue + A.h, 'Nicht die Längen addieren, sondern ihre <b>Quadrate</b> — dann die Wurzel.'], [Math.hypot(2 * A.ue, A.h), 'Der Überstand ist die <b>Hälfte</b> von \\(a - c\\): Er verteilt sich auf zwei Seiten.']]);
          var f = [[Math.hypot(A.s, A.ue), 'Der Schenkel ist die Hypotenuse: \\(h^2 = s^2 - \\text{ü}^2\\), nicht plus.'], [A.s - A.ue, 'Pythagoras gilt für die <b>Quadrate</b>: \\(h = \\sqrt{s^2 - \\text{ü}^2}\\).']];
          if (A.s > 2 * A.ue) f.push([Math.sqrt(A.s * A.s - 4 * A.ue * A.ue), 'Der Überstand ist die <b>Hälfte</b> von \\(a - c\\): Er verteilt sich auf zwei Seiten.']);
          return feld(e, 'x', A.soll, 'Überstand \\(\\text{ü} = \\tfrac{a - c}{2}\\), dann \\(h = \\sqrt{s^2 - \\text{ü}^2}\\).', f); },
        loesung: function(A){ return '\\text{ü} = \\tfrac{' + A.a + ' - ' + A.c + '}{2} = ' + A.ue + ';\\ ' + (A.was === 's' ? 's = \\sqrt{' + A.ue + '^2 + ' + A.h + '^2} \\approx ' + A.soll : 'h = \\sqrt{' + A.s + '^2 - ' + A.ue + '^2} = ' + A.soll); } }
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
        if (A.einheit) html += ' ' + A.einheit;
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
       Einträge: ["v", [[x,y],…], cls] Vieleck · ["s", [x,y], [x,y], cls] Strecke · ["t", [x,y], "Text", cls, dx, dy, anker] ·
       ["p", [x,y]] Punkt · ["r", [x,y], [dx,dy], [dx,dy]] rechter Winkel · ["w", Scheitel, [x,y], [x,y], "Text"] Winkelbogen
       von der Richtung zum ersten zum zweiten Punkt. data-karo="ja" zeichnet Häuschen (1 Häuschen = 1 cm). ---------- */
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
