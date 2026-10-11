<script>
/* Leitprogramm Lineare Gleichungen — Umformer (Kapitel 1–3) und Simulationen (Kapitel 4: drei Sichten,
   Kapitel 5: Parameter) mit Aufgabenleiste, Übungen mit Rückmeldung, Minigrafen. Grundgerüst (Zahlen und
   Lösungsmengen lesen, Koordinatensystem, Aufgabenleiste, Umformer) wie im Leitprogramm Lineare und quadratische
   Gleichungen (scripts/lp/lineare-quadratische-gleichungen/seite.js). Notation wie auf der Themenseite 2.2a:
   Lösungsmenge 𝕃 mit Strichpunkt, leere Menge {}, 𝕃 = ℝ, Normalform a · x + b = 0.
   Eine Farbe, eine Bedeutung (wie in den Clips): blau = Gleichung, linke Seite · orange = Umformung, rechte Seite,
   Parameter k · grün = Lösungen · rot = Fehler · Tinte = Differenz links − rechts. Zahlen mit Dezimalpunkt. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function z(n){ var r = Math.round(n * 1000) / 1000; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function sp(cls, s){ return '<span class="' + cls + '">' + s + '</span>'; }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function zz(v){ var r = Math.round(v * 1000) / 1000; return (Math.abs(v - r) > 1e-9 ? '≈ ' : '') + z(v); }
  function gl(a, b){ return Math.abs(a - b) < 1e-9; }

  /* ---------- Zahlen und Lösungsmengen lesen ----------
     Zahl: -3, 0.5, 1/2, -2/3, Dezimalkomma wird verstanden (und angemerkt).
     Menge: «{0; 3}», «0; 3», «3;0;0» (Reihenfolge und Doppelte egal), «{}» oder «leer» für die leere
     Menge, «R» oder «ℝ» für alle Zahlen. Getrennt wird mit Strichpunkt; «0, 3» (Komma mit Leerschlag)
     gilt auch als Trenner. */
  function zahl(s){
    var komma = /\d,\d/.test(s);
    s = String(s).trim().replace(/\u2212/g, '-').replace(/(\d),(\d)/g, '$1.$2').replace(/\s+/g, '').replace(/^\+/, '');
    if (!s) return { wert: NaN, leer: true };
    var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(-?\d+(?:\.\d+)?)$/);
    if (m) return { wert: parseFloat(m[1]) / parseFloat(m[2]), komma: komma };
    return { wert: /^-?(\d+(\.\d+)?|\.\d+)$/.test(s) ? parseFloat(s) : NaN, komma: komma };
  }
  function menge(s){
    var t = String(s).trim().replace(/\u2212/g, '-');
    if (!t) return { leer: true };
    var komma = /\d,\d/.test(t);
    t = t.replace(/^𝕃\s*=\s*/, '').replace(/^L\s*=\s*/i, '');
    if (/^(r|ℝ|\{\s*(r|ℝ)\s*\}|alle|alle zahlen)$/i.test(t)) return { alle: true, werte: [] };
    t = t.replace(/^\{/, '').replace(/\}$/, '').trim();
    if (!t || /^(leer|keine|∅)$/i.test(t)) return { werte: [], komma: komma };
    if (/^[a-z]\w*\s*=/i.test(t)) return { kaputt: true, xgleich: true };
    t = t.replace(/-\s+(?=[\d.])/g, '-');   // «- 3» wie «-3»
    var teile = t.split(/;|,\s+|\||\s+/), w = [];
    for (var i = 0; i < teile.length; i++){
      if (!teile[i].trim()) continue;
      var r = zahl(teile[i]); if (isNaN(r.wert)) return { kaputt: true };
      if (r.komma) komma = true;
      if (!w.some(function(v){ return gl(v, r.wert); })) w.push(r.wert);
    }
    return { werte: w, komma: komma };
  }
  /* Vergleich mit der Soll-Menge: soll = Zahlenliste, [] (leer) oder 'R' (alle). */
  function mengeGleich(e, soll){
    if (soll === 'R') return !!e.alle;
    if (e.alle) return false;
    if (e.werte.length !== soll.length) return false;
    return soll.every(function(v){ return e.werte.some(function(w){ return gl(v, w); }); });
  }
  function mengeTex(soll){
    if (soll === 'R') return '\\mathbb{L} = \\mathbb{R}';
    if (!soll.length) return '\\mathbb{L} = \\{\\,\\}';
    return '\\mathbb{L} = \\{' + soll.slice().sort(function(a, b){ return a - b; }).map(texZahl).join(';\\ ') + '\\}';
  }
  /* Zahl in LaTeX: ganze und Dezimalzahlen direkt, Drittel und Sechstel als Bruch. */
  function texZahl(v){
    if (gl(v, Math.round(v))) return tz(Math.round(v));
    for (var d of [2, 3, 4, 5, 6, 8, 9, 10, 12]){
      var n = Math.round(v * d);
      if (gl(v * d, n)){
        if (d === 2 || d === 4 || d === 5 || d === 8 || d === 10) return tz(Math.round(v * 1000) / 1000);
        return (n < 0 ? '-' : '') + '\\tfrac{' + Math.abs(n) + '}{' + d + '}';
      }
    }
    return tz(Math.round(v * 1000) / 1000);
  }
  function tz(n){ return n < 0 ? '-' + Math.abs(n) : String(n); }

  /* ---------- Koordinatensystem (wie in den anderen Leitprogrammen) ---------- */
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
    var pf = o.pfeil || 7, namen = [];
    if (y0 <= 0 && y1 >= 0){
      el(g, 'polygon', { points: W + ',' + Y(0) + ' ' + (W - pf) + ',' + (Y(0) - pf / 2) + ' ' + (W - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
      namen.push([W - 3, Y(0) - pf, 'end', o.xname || 'x']);
    }
    if (x0 <= 0 && x1 >= 0){
      el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
      namen.push([X(0) + pf, pf + 3, 'start', o.yname || 'y']);
    }
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(Math.max(0, y0)) + 13, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(Math.max(0, x0)) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    var ebene = el(svg, 'g', {}), schilder = el(svg, 'g', {});
    namen.forEach(function(n){ el(schilder, 'text', { x: n[0], y: n[1], 'text-anchor': n[2], 'class': 'achsname' }, n[3]); });
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ while (ebene.firstChild) ebene.removeChild(ebene.firstChild); },
      kurve: function(f, cls){
        var d = '', an = false, Hh = y1 - y0;
        for (var k = 0; k <= 400; k++){
          var x = x0 + (x1 - x0) * k / 400, y = f(x);
          if (y == null || !isFinite(y)){ an = false; continue; }
          y = Math.max(y0 - 3 * Hh, Math.min(y1 + 3 * Hh, y));
          d += (an ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); an = true;
        }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      }
    };
  }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht immer. */
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
        if (sim.ende) sim.ende();
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
    // Beim Wechsel alles auf den Startwert, sonst erfüllt der Endzustand der vorigen Aufgabe die
    // nächste schon (HOWTO §15).
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; });
      fig.querySelectorAll('.sim-schalter input').forEach(function(inp){ inp.checked = inp.defaultChecked; });
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

  /* ---------- Umformer: Lösungswege selbst wählen ----------
     Unterschied zur Themenseite («Schrittweise» in 2.2a): Dort klickt man
     einen festen Weg durch. Hier wählen die Lernenden jeden Schritt selbst, füllen Lücken und
     geben am Schluss die Lösungsmenge ein; gültige andere Wege führen ebenfalls ans Ziel, Fehler
     bekommen eine eigene Rückmeldung (HOWTO-leitprogramme §8d).

     Eine Aufgabe ist ein kleiner Graph von Knoten:
       { z: 'LaTeX der Zeile', frage: 'Text über den Knöpfen',
         w: [[Knopftext, Ziel | '!Rückmeldung', Umformung, Hinweis], …]   — Schritt wählen
         feld: { muster: 'D = {D}', soll: { D: 49 } | pruef: function(e){ … }, fehler: [[{…}, 'Text']],
                 tipp: 'Text', nach: Ziel }                               — Lücke füllen
         L: [Zahlen] | [] | 'R', probe: 'LaTeX' }                         — Lösungsmenge eingeben
     Die Umformung (z. B. '\\mid -2x') steht wie im Heft rechts neben der Zeile, auf die sie wirkt. */
  function Umformer(fig, aufgaben){
    var verl = fig.querySelector('.uf-verlauf'), frage = fig.querySelector('.uf-frage'), wahl = fig.querySelector('.uf-wahl'),
        rueck = fig.querySelector('.uf-rueck'), zur = fig.querySelector('.uf-zurueck');
    var A = null, pfad = [], ops = [], fertig = false, pruefen = function(){};
    function knoten(id){ return A.k[id]; }
    function zeile(id, op){
      var K = knoten(id);
      return '<div class="uf-zeile"><span class="uf-gl">\\(' + K.z + '\\)</span><span class="uf-op">' + (op ? '\\(' + op + '\\)' : '') + '</span></div>';
    }
    function meldung(cls, html){ rueck.className = 'uf-rueck ' + cls; rueck.innerHTML = html; setzen(rueck); }
    function zeichnen(){
      if (!A){ verl.innerHTML = ''; frage.innerHTML = ''; wahl.innerHTML = ''; return; }
      var html = '', zeilen = [];
      pfad.forEach(function(id, j){ if (knoten(id).z != null) zeilen.push([id, ops[j]]); });
      zeilen.forEach(function(p){ html += zeile(p[0], p[1]); });
      verl.innerHTML = html;
      var K = knoten(pfad[pfad.length - 1]);
      zur.disabled = pfad.length < 2 || fertig;
      if (fertig){
        frage.innerHTML = '';
        wahl.innerHTML = '<div class="uf-loesung">\\(' + mengeTex(K.L) + '\\)</div>' + (K.probe ? '<p class="uf-probe">Probe: \\(' + K.probe + '\\)</p>' : '');
      } else if (K.w){
        frage.innerHTML = K.frage || 'Wähle den nächsten Schritt:';
        wahl.innerHTML = K.w.map(function(o, j){ return '<button type="button" class="uf-knopf" data-j="' + j + '">' + o[0] + '</button>'; }).join('');
        wahl.querySelectorAll('.uf-knopf').forEach(function(b){ b.addEventListener('click', function(){ waehle(+b.dataset.j); }); });
      } else if (K.feld){
        frage.innerHTML = K.frage || 'Fülle die Lücke:';
        wahl.innerHTML = '<span class="uf-feld">' + K.feld.muster.replace(/\{(\w+)\}/g, function(m, f){
          return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">'; })
          + '</span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', feldPruefen);
        wahl.querySelectorAll('input').forEach(function(i){ i.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') feldPruefen(); }); });
      } else if (K.L != null){
        frage.innerHTML = K.frage || 'Gib die Lösungsmenge an — Elemente mit Strichpunkt, leere Menge {}, alle Zahlen R:';
        wahl.innerHTML = '<span class="uf-feld">\\(\\mathbb{L} = \\)<input type="text" class="uf-menge" inputmode="text" autocomplete="off" aria-label="Lösungsmenge" placeholder="{ … }"></span><button type="button" class="uf-pruefen">Prüfen</button>';
        wahl.querySelector('.uf-pruefen').addEventListener('click', mengePruefen);
        wahl.querySelector('input').addEventListener('keydown', function(ev){ if (ev.key === 'Enter') mengePruefen(); });
      }
      setzen(verl); setzen(frage); setzen(wahl);
    }
    function weiter(ziel, op, hinweis){
      ops[pfad.length - 1] = op || '';
      pfad.push(ziel); ops.push('');
      if (hinweis) meldung('hinweis', hinweis); else { rueck.className = 'uf-rueck'; rueck.innerHTML = ''; }
      zeichnen();
    }
    function waehle(j){
      var o = knoten(pfad[pfad.length - 1]).w[j];
      if (typeof o[1] === 'string' && o[1].charAt(0) === '!') return meldung('falsch', o[1].slice(1));
      // '?': eine gültige Umformung, die hier ein Umweg ist — Hinweis (grau), kein Fehler (Prüfung 06.10.2026, M5)
      if (typeof o[1] === 'string' && o[1].charAt(0) === '?') return meldung('hinweis', o[1].slice(1));
      weiter(o[1], o[2], o[3]);
    }
    function feldPruefen(){
      var F = knoten(pfad[pfad.length - 1]).feld, e = {}, leer = false, kaputt = false;
      wahl.querySelectorAll('input').forEach(function(i){ var r = zahl(i.value); e[i.dataset.f] = r.wert; if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; });
      if (leer) return meldung('hinweis', 'Fülle alle Lücken aus.');
      if (kaputt) return meldung('hinweis', 'Zahlen wie <code>-3</code>, <code>0.5</code> oder <code>1/2</code>.');
      var f = F.pruef ? F.pruef(e) : (function(){
        for (var k in F.soll) if (!gl(e[k], F.soll[k])) return 'x';
        return null; })();
      if (f === null) return weiter(F.nach, F.op, F.richtig);
      for (var q = 0; F.fehler && q < F.fehler.length; q++){
        var pass = true; for (var kk in F.fehler[q][0]) if (!gl(e[kk], F.fehler[q][0][kk])) pass = false;
        if (pass) return meldung('falsch', F.fehler[q][1]);
      }
      meldung('falsch', f !== 'x' ? f : (F.tipp || 'Noch nicht. Rechne nach.'));
    }
    function mengePruefen(){
      var K = knoten(pfad[pfad.length - 1]), i = wahl.querySelector('input'), e = menge(i.value);
      if (e.leer) return meldung('hinweis', 'Gib die Lösungsmenge ein, zum Beispiel <code>{2; -1}</code>, <code>{}</code> oder <code>R</code>.');
      if (e.kaputt) return meldung('hinweis', e.xgleich ? 'Gefragt ist die Lösungsmenge, zum Beispiel <code>{3}</code> statt <code>x = 3</code>.' : 'Trenne die Lösungen mit Strichpunkt: <code>{0; 3}</code>. Brüche als <code>1/3</code>.');
      if (mengeGleich(e, K.L)){
        fertig = true; meldung('richtig', '✓ Richtig' + (e.komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + '.'); zeichnen(); pruefen(); return;
      }
      var soll = K.L, t;
      if (K.Lfalsch) for (var q = 0; q < K.Lfalsch.length; q++) if (mengeGleich(e, K.Lfalsch[q][0])) return meldung('falsch', K.Lfalsch[q][1]);
      if (soll === 'R') t = e.werte.length ? 'Die Aussage, die übrig bleibt, ist wahr — für <b>jedes</b> \\(x\\). Schreib <code>R</code>.' : 'Die Aussage ist wahr, nicht falsch: Jede Zahl ist Lösung.';
      else if (!soll.length) t = e.alle ? 'Die Aussage, die übrig bleibt, ist falsch — keine Zahl erfüllt die Gleichung.' : 'Schau auf die letzte Zeile: Gibt es überhaupt eine Zahl, die passt?';
      else if (e.werte.length < soll.length && e.werte.every(function(w){ return soll.some(function(v){ return gl(v, w); }); })) t = 'Es fehlt eine Lösung — schau auf die letzte Zeile: Dort stehen ' + soll.length + '.';
      else t = 'Noch nicht. Lies die Lösungen in der letzten Zeile ab.';
      meldung('falsch', t);
    }
    zur.addEventListener('click', function(){ if (pfad.length > 1 && !fertig){ pfad.pop(); ops.pop(); ops[pfad.length - 1] = ''; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); } });
    return {
      laden: function(a){ A = a; pfad = [a.start || 'a']; ops = ['']; fertig = false; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); },
      leeren: function(){ A = null; pfad = []; ops = []; fertig = false; rueck.className = 'uf-rueck'; rueck.innerHTML = ''; zeichnen(); },
      zustand: function(){ return { fertig: fertig, aufgabe: A }; },
      knoten: function(){ return pfad[pfad.length - 1]; },
      setPruefen: function(f){ pruefen = f; }
    };
  }
  /* Eine Umformer-Simulation: Die Leiste lädt Aufgabe für Aufgabe; ✓, sobald die Lösungsmenge stimmt. */
  function umformerSim(id, aufgaben){
    var fig = document.getElementById(id); if (!fig) return;
    var U = Umformer(fig, aufgaben);
    fig.__aufgaben = aufgaben; fig.__U = U;      // Testhaken (Prüfskript des Umformers)
    var sim = { zustand: U.zustand, aufraeumen: function(){}, ende: U.leeren };
    var pr = Leiste(fig, aufgaben.map(function(a){
      return { text: a.text, setup: function(){ U.laden(a); }, ok: function(s){ return s.fertig && s.aufgabe === a; } }; }), sim);
    U.setPruefen(pr);
  }
  var ODER = '\\;\\text{ oder }\\;';
  var MAL0 = '!Das gibt \\(0 = 0\\), wahr für jedes \\(x\\). Mit \\(0\\) multiplizieren ist keine Äquivalenzumformung: Aus der Gleichung mit genau einer Lösung würde eine, die jede Zahl erfüllt.';
  var DURCHX = '!Durch einen Term mit \\(x\\) zu teilen ist keine Äquivalenzumformung, denn er kann null sein. Subtrahiere die \\(x\\)-Glieder.';
  var FALSCH = '\\(x\\) ist weg, und es bleibt eine Aussage. Ist sie wahr oder falsch? Gib die Lösungsmenge an:';
  var WAHR = '\\(x\\) ist weg, und es bleibt eine Aussage. Ist sie wahr oder falsch? Gib die Lösungsmenge an:';

  /* ---------- Kapitel 1: Äquivalenzumformungen und Probe ----------
     Startgleichungen sind nicht die Beispiele aus den Clips (5x − 7 = 2x + 8, 2x = 3x − 6). */
  umformerSim('sim1', [
    { text: 'Löse \\(4x + 7 = 31\\).', k: {
      a: { z: '4x + 7 = 31', w: [['beidseitig \\(-7\\)', 'b', '\\mid -7'],
        ['beidseitig \\(+7\\)', '?Erlaubt, aber ein Umweg: Dann steht links \\(4x + 14\\), die Zahl wird grösser statt null. Die Gegenoperation zu \\(+7\\) ist \\(-7\\).'],
        ['beidseitig \\(:4\\)', '?Erlaubt, gibt aber Brüche: \\(x + \\tfrac{7}{4} = \\tfrac{31}{4}\\). Einfacher: zuerst die \\(7\\) wegschaffen.']] },
      b: { z: '4x = 24', w: [['beidseitig \\(:4\\)', 'c', '\\mid :4'],
        ['beidseitig \\(-4\\)', '?Erlaubt, aber es bringt nichts: Dann steht \\(4x - 4 = 20\\) da. \\(4x\\) heisst \\(4 \\cdot x\\): Die Gegenoperation ist \\(:4\\).']] },
      c: { z: 'x = 6', L: [6], probe: '4 \\cdot 6 + 7 = 31\\ \\checkmark' } } },
    { text: 'Löse \\(6x - 5 = 2x + 11\\).', k: {
      a: { z: '6x - 5 = 2x + 11', w: [['beidseitig \\(-2x\\)', 'b', '\\mid -2x'], ['beidseitig \\(+5\\)', 'c', '\\mid +5'],
        ['beidseitig \\(+2x\\)', '?Erlaubt, aber ein Umweg: Dann steht rechts \\(4x + 11\\), das \\(x\\)-Glied rechts wird grösser statt null. Die Gegenoperation zu \\(+2x\\) ist \\(-2x\\).']] },
      b: { z: '4x - 5 = 11', w: [['beidseitig \\(+5\\)', 'd', '\\mid +5'],
        ['beidseitig \\(-5\\)', '?Erlaubt, aber ein Umweg: Dann steht links \\(4x - 10\\). Die Gegenoperation zu \\(-5\\) ist \\(+5\\).']] },
      c: { z: '6x = 2x + 16', w: [['beidseitig \\(-2x\\)', 'd', '\\mid -2x']] },
      d: { z: '4x = 16', w: [['beidseitig \\(:4\\)', 'e', '\\mid :4']] },
      e: { z: 'x = 4', L: [4], Lfalsch: [[[-4], 'Vorzeichen: \\(16 : 4 = 4\\).']], probe: '6 \\cdot 4 - 5 = 19 \\text{ und } 2 \\cdot 4 + 11 = 19\\ \\checkmark' } } },
    { text: 'Löse \\(9 - 2x = 3\\).', k: {
      a: { z: '9 - 2x = 3', w: [['beidseitig \\(-9\\)', 'b', '\\mid -9'], ['beidseitig \\(+2x\\)', 'c', '\\mid +2x'],
        ['beidseitig \\(+9\\)', '?Erlaubt, aber ein Umweg: Dann steht links \\(18 - 2x\\). Die Gegenoperation zu \\(+9\\) ist \\(-9\\).']] },
      b: { z: '-2x = -6', w: [['beidseitig \\(:(-2)\\)', 'd', '\\mid :(-2)'],
        ['beidseitig \\(+2\\)', '?Erlaubt, aber es bringt nichts: \\(-2x\\) heisst \\(-2 \\cdot x\\). Die Gegenoperation ist das Teilen durch \\(-2\\).'],
        ['beidseitig \\(:2\\)', '?Erlaubt: \\(-x = -3\\). Dann bleibt noch ein Schritt. Teile gleich durch den ganzen Faktor vor \\(x\\), also durch \\(-2\\).']] },
      c: { z: '9 = 3 + 2x', w: [['beidseitig \\(-3\\)', 'c2', '\\mid -3']] },
      c2: { z: '6 = 2x', w: [['beidseitig \\(:2\\)', 'e', '\\mid :2']] },
      d: { z: 'x = 3', L: [3], Lfalsch: [[[-3], 'Vorzeichen: \\(-6 : (-2) = 3\\), minus durch minus gibt plus.']], probe: '9 - 2 \\cdot 3 = 3\\ \\checkmark' },
      e: { z: '3 = x', L: [3], Lfalsch: [[[-3], 'Lies die letzte Zeile: \\(3 = x\\) heisst \\(x = 3\\).']], probe: '9 - 2 \\cdot 3 = 3\\ \\checkmark' } } },
    { text: 'Löse \\(3x - 8 = 5x + 2\\).', k: {
      a: { z: '3x - 8 = 5x + 2', w: [['beidseitig \\(-5x\\)', 'b', '\\mid -5x'], ['beidseitig \\(-3x\\)', 'c', '\\mid -3x'],
        ['beidseitig \\(+5x\\)', '?Erlaubt, aber ein Umweg: Dann steht rechts \\(10x + 2\\). Die Gegenoperation zu \\(+5x\\) ist \\(-5x\\).']] },
      b: { z: '-2x - 8 = 2', w: [['beidseitig \\(+8\\)', 'd', '\\mid +8']] },
      d: { z: '-2x = 10', w: [['beidseitig \\(:(-2)\\)', 'e', '\\mid :(-2)'],
        ['beidseitig \\(:2\\)', '?Erlaubt: \\(-x = 5\\). Dann bleibt noch ein Schritt. Teile gleich durch den ganzen Faktor \\(-2\\).']] },
      e: { z: 'x = -5', L: [-5], Lfalsch: [[[5], 'Vorzeichen: \\(10 : (-2) = -5\\).']], probe: '3 \\cdot (-5) - 8 = -23 \\text{ und } 5 \\cdot (-5) + 2 = -23\\ \\checkmark' },
      c: { z: '-8 = 2x + 2', w: [['beidseitig \\(-2\\)', 'c2', '\\mid -2']] },
      c2: { z: '-10 = 2x', w: [['beidseitig \\(:2\\)', 'e2', '\\mid :2']] },
      e2: { z: '-5 = x', L: [-5], Lfalsch: [[[5], 'Vorzeichen: \\(-10 : 2 = -5\\).']], probe: '3 \\cdot (-5) - 8 = -23 \\text{ und } 5 \\cdot (-5) + 2 = -23\\ \\checkmark' } } },
    { text: 'Löse \\(0.5x + 2 = 3.5\\).', k: {
      a: { z: '0.5x + 2 = 3.5', w: [['beidseitig \\(-2\\)', 'b', '\\mid -2'], ['beidseitig \\(\\cdot 2\\)', 'c', '\\mid \\cdot 2']] },
      b: { z: '0.5x = 1.5', w: [['beidseitig \\(:0.5\\)', 'd', '\\mid :0.5'], ['beidseitig \\(\\cdot 2\\)', 'd', '\\mid \\cdot 2'],
        ['beidseitig \\(-0.5\\)', '?Erlaubt, aber es bringt nichts: \\(0.5x\\) heisst \\(0.5 \\cdot x\\). Die Gegenoperation ist \\(:0.5\\), also \\(\\cdot 2\\).']] },
      c: { z: 'x + 4 = 7', w: [['beidseitig \\(-4\\)', 'd', '\\mid -4']] },
      d: { z: 'x = 3', L: [3], probe: '0.5 \\cdot 3 + 2 = 3.5\\ \\checkmark' } } },
    { text: 'Löse \\(-x + 7 = 2x - 8\\).', k: {
      a: { z: '-x + 7 = 2x - 8', w: [['beidseitig \\(+x\\)', 'b', '\\mid +x'], ['beidseitig \\(-2x\\)', 'c', '\\mid -2x'], ['beidseitig \\(\\cdot 0\\)', MAL0]] },
      b: { z: '7 = 3x - 8', w: [['beidseitig \\(+8\\)', 'b2', '\\mid +8']] },
      b2: { z: '15 = 3x', w: [['beidseitig \\(:3\\)', 'b3', '\\mid :3']] },
      b3: { z: '5 = x', L: [5], probe: '-5 + 7 = 2 \\text{ und } 2 \\cdot 5 - 8 = 2\\ \\checkmark' },
      c: { z: '-3x + 7 = -8', w: [['beidseitig \\(-7\\)', 'c2', '\\mid -7']] },
      c2: { z: '-3x = -15', w: [['beidseitig \\(:(-3)\\)', 'c3', '\\mid :(-3)'],
        ['Minus weglassen: \\(3x = -15\\)', '!Das Minus gehört zur Zahl \\(-3\\). Teile beide Seiten durch \\(-3\\).']] },
      c3: { z: 'x = 5', L: [5], Lfalsch: [[[-5], 'Vorzeichen: \\(-15 : (-3) = 5\\).']], probe: '-5 + 7 = 2 \\text{ und } 2 \\cdot 5 - 8 = 2\\ \\checkmark' } } }
  ]);

  /* ---------- Kapitel 2: Klammern und Brüche ----------
     Nicht die Clip-Beispiele 4(x − 2) = 2x + 6, 5 − 2(x + 1) = x, x/3 + 2 = x/2 − 1, (x − 1)/2 − (x + 1)/3 = 1. */
  umformerSim('sim2', [
    { text: 'Löse \\(3(x - 2) = x + 4\\).', k: {
      a: { z: '3(x - 2) = x + 4', w: [['Klammer auflösen: \\(3x - 6 = x + 4\\)', 'b'],
        ['Klammer auflösen: \\(3x - 2 = x + 4\\)', '!Der Faktor \\(3\\) gilt für jedes Glied in der Klammer: \\(3 \\cdot (-2) = -6\\).'],
        ['beidseitig \\(:3\\)', '?Erlaubt, gibt aber rechts einen Bruch: \\(\\tfrac{x + 4}{3}\\). Einfacher: zuerst die Klammer auflösen.']] },
      b: { z: '3x - 6 = x + 4', w: [['beidseitig \\(-x\\)', 'c', '\\mid -x'], ['beidseitig \\(+6\\)', 'c2', '\\mid +6']] },
      c: { z: '2x - 6 = 4', w: [['beidseitig \\(+6\\)', 'd', '\\mid +6']] },
      c2: { z: '3x = x + 10', w: [['beidseitig \\(-x\\)', 'd', '\\mid -x']] },
      d: { z: '2x = 10', w: [['beidseitig \\(:2\\)', 'e', '\\mid :2']] },
      e: { z: 'x = 5', L: [5], probe: '3 \\cdot 3 = 9 \\text{ und } 5 + 4 = 9\\ \\checkmark' } } },
    { text: 'Löse \\(2(x + 3) - (x - 1) = 10\\).', k: {
      a: { z: '2(x + 3) - (x - 1) = 10', w: [['Klammern auflösen: \\(2x + 6 - x + 1 = 10\\)', 'b'],
        ['Klammern auflösen: \\(2x + 6 - x - 1 = 10\\)', '!Das Minus vor \\((x - 1)\\) dreht jedes Vorzeichen in der Klammer: \\(-(x - 1) = -x + 1\\).'],
        ['Klammern auflösen: \\(2x + 3 - x + 1 = 10\\)', '!Der Faktor \\(2\\) gilt auch für die \\(3\\): \\(2 \\cdot 3 = 6\\).']] },
      b: { z: '2x + 6 - x + 1 = 10', w: [['zusammenfassen: \\(x + 7 = 10\\)', 'c'], ['zusammenfassen: \\(3x + 7 = 10\\)', '!\\(2x - x = x\\), nicht \\(3x\\).']] },
      c: { z: 'x + 7 = 10', w: [['beidseitig \\(-7\\)', 'd', '\\mid -7']] },
      d: { z: 'x = 3', L: [3], probe: '2 \\cdot 6 - 2 = 10\\ \\checkmark' } } },
    { text: 'Löse \\(6 - 3(x + 1) = x - 5\\).', k: {
      a: { z: '6 - 3(x + 1) = x - 5', w: [['Klammer auflösen: \\(6 - 3x - 3 = x - 5\\)', 'b'],
        ['Klammer auflösen: \\(6 - 3x + 3 = x - 5\\)', '!Das Minus vor \\(3(x + 1)\\) gilt für beide Glieder: \\(-3 \\cdot 1 = -3\\).'],
        ['zuerst \\(6 - 3\\) rechnen: \\(3(x + 1) = x - 5\\)', '!Punkt vor Strich: \\(3(x + 1)\\) ist ein Produkt. Die \\(3\\) gehört zur Klammer, \\(6 - 3\\) darf man nicht vorziehen.']] },
      b: { z: '6 - 3x - 3 = x - 5', w: [['zusammenfassen: \\(3 - 3x = x - 5\\)', 'c']] },
      c: { z: '3 - 3x = x - 5', w: [['beidseitig \\(+3x\\)', 'd', '\\mid +3x'], ['beidseitig \\(-x\\)', 'd2', '\\mid -x']] },
      d: { z: '3 = 4x - 5', w: [['beidseitig \\(+5\\)', 'e', '\\mid +5']] },
      e: { z: '8 = 4x', w: [['beidseitig \\(:4\\)', 'f', '\\mid :4']] },
      f: { z: '2 = x', L: [2], probe: '6 - 3 \\cdot 3 = -3 \\text{ und } 2 - 5 = -3\\ \\checkmark' },
      d2: { z: '3 - 4x = -5', w: [['beidseitig \\(-3\\)', 'e2', '\\mid -3']] },
      e2: { z: '-4x = -8', w: [['beidseitig \\(:(-4)\\)', 'f2', '\\mid :(-4)']] },
      f2: { z: 'x = 2', L: [2], Lfalsch: [[[-2], 'Vorzeichen: \\(-8 : (-4) = 2\\).']], probe: '6 - 3 \\cdot 3 = -3 \\text{ und } 2 - 5 = -3\\ \\checkmark' } } },
    { text: 'Löse \\(\\tfrac{x}{2} + 1 = \\tfrac{x}{5} + 4\\).', k: {
      a: { z: '\\tfrac{x}{2} + 1 = \\tfrac{x}{5} + 4', w: [['beidseitig \\(\\cdot 10\\) (Hauptnenner)', 'b', '\\mid \\cdot 10'],
        ['beidseitig \\(\\cdot 7\\)', '?Erlaubt, aber \\(7\\) ist kein Vielfaches von \\(2\\) und \\(5\\): Die Brüche bleiben. Der Hauptnenner von \\(2\\) und \\(5\\) ist \\(10\\).'],
        ['nur die Brüche mal \\(10\\): \\(5x + 1 = 2x + 4\\)', '!Mal \\(10\\) heisst: jedes Glied auf beiden Seiten, auch \\(1\\) und \\(4\\).']] },
      b: { z: '5x + 10 = 2x + 40', w: [['beidseitig \\(-2x\\)', 'c', '\\mid -2x'], ['beidseitig \\(-10\\)', 'c2', '\\mid -10']] },
      c: { z: '3x + 10 = 40', w: [['beidseitig \\(-10\\)', 'd', '\\mid -10']] },
      c2: { z: '5x = 2x + 30', w: [['beidseitig \\(-2x\\)', 'd', '\\mid -2x']] },
      d: { z: '3x = 30', w: [['beidseitig \\(:3\\)', 'e', '\\mid :3']] },
      e: { z: 'x = 10', L: [10], probe: '\\tfrac{10}{2} + 1 = 6 \\text{ und } \\tfrac{10}{5} + 4 = 6\\ \\checkmark' } } },
    { text: 'Löse \\(\\tfrac{x + 5}{4} = \\tfrac{x + 1}{2}\\).', k: {
      a: { z: '\\tfrac{x + 5}{4} = \\tfrac{x + 1}{2}', w: [['beidseitig \\(\\cdot 4\\) (Hauptnenner)', 'b', '\\mid \\cdot 4'],
        ['Nenner weglassen: \\(x + 5 = x + 1\\)', '!Die Nenner sind verschieden. Mal \\(4\\) macht aus \\(\\tfrac{x + 1}{2}\\) das Doppelte, \\(2(x + 1)\\).'],
        ['beidseitig \\(\\cdot 2\\)', '?Erlaubt: \\(\\tfrac{x + 5}{2} = x + 1\\), links bleibt ein Bruch. Der Hauptnenner von \\(4\\) und \\(2\\) ist \\(4\\).']] },
      b: { z: 'x + 5 = 2(x + 1)', w: [['Klammer auflösen: \\(x + 5 = 2x + 2\\)', 'c'],
        ['Klammer auflösen: \\(x + 5 = 2x + 1\\)', '!Der Bruchstrich wirkt wie eine Klammer: \\(2\\) mal den ganzen Zähler, also auch \\(2 \\cdot 1 = 2\\).']] },
      c: { z: 'x + 5 = 2x + 2', w: [['beidseitig \\(-x\\)', 'd', '\\mid -x'], ['beidseitig \\(-2x\\)', 'd2', '\\mid -2x']] },
      d: { z: '5 = x + 2', w: [['beidseitig \\(-2\\)', 'e', '\\mid -2']] },
      e: { z: '3 = x', L: [3], probe: '\\tfrac{8}{4} = 2 \\text{ und } \\tfrac{4}{2} = 2\\ \\checkmark' },
      d2: { z: '-x + 5 = 2', w: [['beidseitig \\(-5\\)', 'e2', '\\mid -5']] },
      e2: { z: '-x = -3', w: [['beidseitig \\(\\cdot (-1)\\)', 'f2', '\\mid \\cdot (-1)'],
        ['Minus weglassen: \\(x = -3\\)', '!Aus \\(-x = -3\\) folgt nicht \\(x = -3\\): Mal \\((-1)\\) dreht beide Vorzeichen.']] },
      f2: { z: 'x = 3', L: [3], Lfalsch: [[[-3], 'Vorzeichen: Aus \\(-x = -3\\) folgt \\(x = 3\\).']], probe: '\\tfrac{8}{4} = 2 \\text{ und } \\tfrac{4}{2} = 2\\ \\checkmark' } } },
    { text: 'Löse \\(\\tfrac{2x - 1}{3} - \\tfrac{x - 2}{2} = 1\\).', k: {
      a: { z: '\\tfrac{2x - 1}{3} - \\tfrac{x - 2}{2} = 1', w: [['beidseitig \\(\\cdot 6\\) (Hauptnenner)', 'b', '\\mid \\cdot 6'],
        ['nur links mal \\(6\\): \\(2(2x - 1) - 3(x - 2) = 1\\)', '!Mal \\(6\\) gilt für beide Seiten: Rechts wird aus \\(1\\) die \\(6\\).'],
        ['beidseitig \\(\\cdot 5\\)', '?Erlaubt, aber \\(5\\) ist kein Vielfaches von \\(3\\) und \\(2\\): Die Brüche bleiben. Der Hauptnenner ist \\(6\\).']] },
      b: { z: '2(2x - 1) - 3(x - 2) = 6', w: [['Klammern auflösen: \\(4x - 2 - 3x + 6 = 6\\)', 'c'],
        ['Klammern auflösen: \\(4x - 2 - 3x - 6 = 6\\)', '!Das Minus vor dem zweiten Bruch gilt für den ganzen Zähler: \\(-3 \\cdot (-2) = +6\\).']] },
      c: { z: '4x - 2 - 3x + 6 = 6', w: [['zusammenfassen: \\(x + 4 = 6\\)', 'd']] },
      d: { z: 'x + 4 = 6', w: [['beidseitig \\(-4\\)', 'e', '\\mid -4']] },
      e: { z: 'x = 2', L: [2], probe: '\\tfrac{3}{3} - \\tfrac{0}{2} = 1\\ \\checkmark' } } }
  ]);

  /* ---------- Kapitel 3: drei Lösungsfälle ----------
     Nicht die Clip-Beispiele 3x + 2 = 11, 2(x + 3) = 2x + 9, 4x + 8 = 4(x + 2). Gemischt, auch die Lösung 0. */
  umformerSim('sim3', [
    { text: 'Löse \\(4(x - 1) = 4x + 3\\).', k: {
      a: { z: '4(x - 1) = 4x + 3', w: [['Klammer auflösen: \\(4x - 4 = 4x + 3\\)', 'b'],
        ['Klammer auflösen: \\(4x - 1 = 4x + 3\\)', '!Der Faktor \\(4\\) gilt für beide Glieder: \\(4 \\cdot (-1) = -4\\).']] },
      b: { z: '4x - 4 = 4x + 3', w: [['beidseitig \\(-4x\\)', 'c', '\\mid -4x'], ['beidseitig \\(:4x\\)', DURCHX]] },
      c: { z: '-4 = 3', frage: FALSCH, L: [],
        Lfalsch: [['R', 'Die Aussage \\(-4 = 3\\) ist falsch, egal welches \\(x\\) man einsetzt.'],
                  [[0], '\\(\\{0\\}\\) enthält die Zahl \\(0\\). Macht \\(x = 0\\) die Aussage \\(-4 = 3\\) wahr?'],
                  [[3], 'Im Rest steht kein \\(x\\) mehr. Keine Zahl macht \\(-4 = 3\\) wahr.']] } } },
    { text: 'Löse \\(3(2x + 1) - 1 = 6x + 2\\).', k: {
      a: { z: '3(2x + 1) - 1 = 6x + 2', w: [['Klammer auflösen: \\(6x + 3 - 1 = 6x + 2\\)', 'b'],
        ['Klammer auflösen: \\(6x + 1 - 1 = 6x + 2\\)', '!Der Faktor \\(3\\) gilt auch für die \\(1\\) in der Klammer: \\(3 \\cdot 1 = 3\\).']] },
      b: { z: '6x + 3 - 1 = 6x + 2', w: [['zusammenfassen: \\(6x + 2 = 6x + 2\\)', 'c']] },
      c: { z: '6x + 2 = 6x + 2', w: [['beidseitig \\(-6x\\)', 'd', '\\mid -6x'],
        ['beidseitig \\(\\cdot 0\\)', '!Mit \\(0\\) multiplizieren ist keine Äquivalenzumformung: Aus jeder Gleichung wird \\(0 = 0\\). Die Lösungsmenge kann sich dabei ändern; dass hier am Ende auch jede Zahl Lösung ist, darf man daraus nicht schliessen. Subtrahiere die \\(x\\)-Glieder.']] },
      d: { z: '2 = 2', frage: WAHR, L: 'R',
        Lfalsch: [[[], 'Die Aussage \\(2 = 2\\) ist wahr, und zwar für jedes \\(x\\). Schreib <code>R</code>.'],
                  [[2], 'Nicht nur \\(x = 2\\): Setz \\(x = 5\\) ein. Stimmt die Gleichung auch dann?']] } } },
    { text: 'Löse \\(2(x + 4) = 5x - 1\\).', k: {
      a: { z: '2(x + 4) = 5x - 1', w: [['Klammer auflösen: \\(2x + 8 = 5x - 1\\)', 'b'],
        ['Klammer auflösen: \\(2x + 4 = 5x - 1\\)', '!Der Faktor \\(2\\) gilt für jedes Glied: \\(2 \\cdot 4 = 8\\).']] },
      b: { z: '2x + 8 = 5x - 1', w: [['beidseitig \\(-2x\\)', 'c', '\\mid -2x'], ['beidseitig \\(-5x\\)', 'c2', '\\mid -5x']] },
      c: { z: '8 = 3x - 1', w: [['beidseitig \\(+1\\)', 'd', '\\mid +1']] },
      d: { z: '9 = 3x', w: [['beidseitig \\(:3\\)', 'e', '\\mid :3']] },
      e: { z: '3 = x', frage: 'Hier bleibt \\(x\\) stehen. Gib die Lösungsmenge an:', L: [3],
        Lfalsch: [['R', 'Hier ist \\(x\\) nicht verschwunden: Nur \\(x = 3\\) erfüllt die Gleichung.']], probe: '2 \\cdot 7 = 14 \\text{ und } 15 - 1 = 14\\ \\checkmark' },
      c2: { z: '-3x + 8 = -1', w: [['beidseitig \\(-8\\)', 'd2', '\\mid -8']] },
      d2: { z: '-3x = -9', w: [['beidseitig \\(:(-3)\\)', 'e2', '\\mid :(-3)']] },
      e2: { z: 'x = 3', L: [3], Lfalsch: [[[-3], 'Vorzeichen: \\(-9 : (-3) = 3\\).']], probe: '2 \\cdot 7 = 14 \\text{ und } 15 - 1 = 14\\ \\checkmark' } } },
    { text: 'Löse \\(5x - 2(x + 1) = 3x + 4\\).', k: {
      a: { z: '5x - 2(x + 1) = 3x + 4', w: [['Klammer auflösen: \\(5x - 2x - 2 = 3x + 4\\)', 'b'],
        ['Klammer auflösen: \\(5x - 2x + 2 = 3x + 4\\)', '!Das Minus vor \\(2(x + 1)\\) gilt für beide Glieder: \\(-2 \\cdot 1 = -2\\).']] },
      b: { z: '5x - 2x - 2 = 3x + 4', w: [['zusammenfassen: \\(3x - 2 = 3x + 4\\)', 'c']] },
      c: { z: '3x - 2 = 3x + 4', w: [['beidseitig \\(-3x\\)', 'd', '\\mid -3x'], ['beidseitig \\(:3x\\)', DURCHX]] },
      d: { z: '-2 = 4', frage: FALSCH, L: [],
        Lfalsch: [['R', 'Die Aussage \\(-2 = 4\\) ist falsch, für jedes \\(x\\).'],
                  [[0], '\\(\\{0\\}\\) enthält die Zahl \\(0\\). Macht \\(x = 0\\) die Aussage \\(-2 = 4\\) wahr?']] } } },
    { text: 'Löse \\(6 - 2x = 2(3 - x)\\).', k: {
      a: { z: '6 - 2x = 2(3 - x)', w: [['Klammer auflösen: \\(6 - 2x = 6 - 2x\\)', 'b'],
        ['Klammer auflösen: \\(6 - 2x = 6 - x\\)', '!Der Faktor \\(2\\) gilt auch für das \\(x\\): \\(2 \\cdot (-x) = -2x\\).']] },
      b: { z: '6 - 2x = 6 - 2x', w: [['beidseitig \\(+2x\\)', 'c', '\\mid +2x']] },
      c: { z: '6 = 6', frage: WAHR, L: 'R',
        Lfalsch: [[[], 'Die Aussage \\(6 = 6\\) ist wahr, für jedes \\(x\\). Schreib <code>R</code>.'],
                  [[6], 'Nicht nur \\(6\\): Jede Zahl macht \\(6 = 6\\) wahr.']] } } },
    { text: 'Löse \\(3(x + 2) = 5x + 6\\).', k: {
      a: { z: '3(x + 2) = 5x + 6', w: [['Klammer auflösen: \\(3x + 6 = 5x + 6\\)', 'b'],
        ['Klammer auflösen: \\(3x + 2 = 5x + 6\\)', '!Der Faktor \\(3\\) gilt für jedes Glied: \\(3 \\cdot 2 = 6\\).']] },
      b: { z: '3x + 6 = 5x + 6', w: [['beidseitig \\(-3x\\)', 'c', '\\mid -3x'], ['beidseitig \\(-6\\)', 'c2', '\\mid -6']] },
      c: { z: '6 = 2x + 6', w: [['beidseitig \\(-6\\)', 'd', '\\mid -6']] },
      c2: { z: '3x = 5x', w: [['beidseitig \\(-3x\\)', 'd', '\\mid -3x'],
        ['beidseitig \\(:x\\)', '!Durch \\(x\\) teilen setzt \\(x \\neq 0\\) voraus. Gerade hier ginge die Lösung verloren. Subtrahiere \\(3x\\).']] },
      d: { z: '0 = 2x', w: [['beidseitig \\(:2\\)', 'e', '\\mid :2'],
        ['\\(x\\) ist weg: keine Lösung', '!Hier steht noch \\(2x\\), \\(x\\) ist nicht verschwunden. Teile durch \\(2\\).']] },
      e: { z: '0 = x', frage: 'Hier bleibt \\(x\\) stehen. Gib die Lösungsmenge an:', L: [0],
        Lfalsch: [[[], 'Die Menge ist nicht leer: \\(x = 0\\) ist eine Lösung, die Zahl \\(0\\). Probe: \\(3 \\cdot 2 = 6\\) und \\(0 + 6 = 6\\).'],
                  ['R', 'Nur \\(x = 0\\): Setz \\(x = 1\\) ein, dann steht \\(9 = 11\\).']], probe: '3 \\cdot 2 = 6 \\text{ und } 5 \\cdot 0 + 6 = 6\\ \\checkmark' } } }
  ]);

  /* ---------- Kapitel 4: drei Sichten (Tabelle, Graph, Normalform) ----------
     Unterschied zur Animation «Drei Darstellungen» der Themenseite: Dort steht eine feste Gleichung (2x − 3 = 5)
     mit Tabelle; hier wechselt die Leiste die Gleichung, zeigt die Vergleichszeile wie eine Tabellenzeile, kann die
     Differenz links − rechts (Normalform) zuschalten und zeigt mit 4x − 2 = −x + 6, dass der Regler nicht jede Lösung
     trifft. Startgleichung 3x − 1 = 1 wie im Clip. Regler x in Schritten von 0.5, Start x = 0 (löst keine Aufgabe). */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 280, x0: -2, x1: 6, y0: -8, y1: 16, sy: 2, xm: [-1, 1, 2, 3, 4, 5], ym: [-4, 4, 8, 12] });
    var xr = fig.querySelector('input[data-p="x"]'), schalter = fig.querySelector('.sim-schalter input');
    var bewegt = {}, besucht = {}, pruefen = function(){};
    var GL = [[3, -1, 0, 1], [1, 2, 3, -4], [-1, 4, 1, -1], [4, -2, -1, 6], [3, -5, 1, 1], [2, 1, 2, -1]];   // m1, q1, m2, q2
    var gl = 0;
    xr.addEventListener('input', function(){ bewegt.x = true; besucht[xr.value] = true; zeichnen(); });
    schalter.addEventListener('change', zeichnen);
    function term(m, q){ var s = (m === 0 ? '' : m === 1 ? 'x' : m === -1 ? '−x' : z(m) + 'x');
      if (q) s += s ? (q < 0 ? ' − ' + z(-q) : ' + ' + z(q)) : z(q); return s || '0'; }
    function einsetzen(m, q, x){ var xs = x < 0 ? '(' + z(x) + ')' : z(x);
      var s = m === 0 ? '' : (m === 1 ? '' : m === -1 ? '−' : z(m) + '·') + xs;
      if (q) s += s ? (q < 0 ? ' − ' + z(-q) : ' + ' + z(q)) : z(q); return s || '0'; }
    function zust(){
      var g = GL[gl], x = +xr.value, l = g[0] * x + g[1], r = g[2] * x + g[3];
      xr.parentNode.querySelector('.sl-val').textContent = z(x);
      return { gl: gl, x: x, l: l, r: r, gleich: gl3(l, r), normal: schalter.checked, bewegt: bewegt, besucht: besucht };
    }
    function gl3(a, b){ return Math.abs(a - b) < 1e-9; }
    var sim = { zustand: zust, zeichnen: zeichnen,
      aufraeumen: function(){ for (var k in bewegt) delete bewegt[k]; for (var j in besucht) delete besucht[j]; gl = 0; } };
    function zeichnen(){
      var s = zust(), g = GL[gl], x = s.x;
      K.leeren();
      K.kurve(function(t){ return g[0] * t + g[1]; }, 'kurve');
      K.kurve(function(t){ return g[2] * t + g[3]; }, 'kurve rechts');
      if (s.normal) K.kurve(function(t){ return (g[0] - g[2]) * t + g[1] - g[3]; }, 'kurve diff');
      var lin = el(K.ebene, 'line', { x1: K.X(x), y1: 0, x2: K.X(x), y2: 280, 'class': 'senk' });
      K.punkt(x, s.l, s.gleich ? 'p-loes' : 'p-links');
      K.punkt(x, s.r, s.gleich ? 'p-loes' : 'p-rechts');
      if (s.normal) K.punkt(x, s.l - s.r, gl3(s.l, s.r) ? 'p-loes' : 'p-diff');
      var zeichen = s.gleich ? '=' : s.l < s.r ? '<' : '>';
      var txt = sp('tx-blau', term(g[0], g[1])) + ' = ' + sp('tx-orange', term(g[2], g[3]))
        + '<br><span class="nb">links: ' + einsetzen(g[0], g[1], x) + ' = ' + z(s.l) + ';</span> <span class="nb">rechts: ' + einsetzen(g[2], g[3], x) + ' = ' + z(s.r) + ';</span>'
        + ' <span class="nb">' + (s.gleich ? sp('tx-gruen', 'links = rechts') : 'links ' + zeichen + ' rechts') + '</span>';
      if (s.normal) txt += g[0] === g[2]
        ? '<br><span class="nb">links − rechts = ' + z(g[1] - g[3]) + ' für jedes x:</span> <span class="nb">kein x mehr, keine Normalform</span>'
        : '<br><span class="nb">Normalform: ' + term(g[0] - g[2], g[1] - g[3]) + ' = 0;</span> <span class="nb">links − rechts = ' + z(s.l - s.r) + '</span>';
      fig.querySelector('[data-rolle="formel"]').innerHTML = txt;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde \\(3x - 1 = 1\\): Zieh an \\(x\\). Wo kippt das Zeichen zwischen links und rechts?', ok: function(s){ return s.gl === 0 && s.bewegt.x; } },
      { text: 'Neue Gleichung \\(x + 2 = 3x - 4\\): Stell \\(x\\) auf die Lösung.', setup: function(){ gl = 1; }, ok: function(s){ return s.gl === 1 && s.gleich; } },
      { text: 'Gleichung \\(-x + 4 = x - 1\\): Stell \\(x\\) auf die Lösung.', setup: function(){ gl = 2; }, ok: function(s){ return s.gl === 2 && s.gleich; } },
      { text: 'Gleichung \\(4x - 2 = -x + 6\\): Der Regler trifft die Lösung nicht genau. Stell \\(x\\) so ein, dass links und rechts am nächsten beieinander liegen.', setup: function(){ gl = 3; }, ok: function(s){ return s.gl === 3 && s.x === 1.5; } },
      { text: 'Gleichung \\(3x - 5 = x + 1\\): Schalte die Normalform ein und stell \\(x\\) auf die Nullstelle der Differenz links − rechts.', setup: function(){ gl = 4; }, ok: function(s){ return s.gl === 4 && s.normal && s.gleich; } },
      { text: 'Gleichung \\(2x + 1 = 2x - 1\\): Zieh \\(x\\) vom linken bis zum rechten Ende. Kippt das Zeichen irgendwo?', setup: function(){ gl = 5; }, ok: function(s){ return s.gl === 5 && s.besucht['-2'] && s.besucht['6']; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Parameterdiskussion ----------
     Unterschied zur Animation «Parameter» der Themenseite (Beispiele A und B, nur Text): Drei Familien, dazu das Bild
     der Differenz links − rechts, y = a(k)·x − c(k) wie bei der Normalform in Kapitel 4 — ihre Nullstelle ist die
     Lösung; bei a(k) = 0 wird sie waagrecht. Familie C hat zwei kritische Werte. Start k = 4, Familie A wie im Clip;
     keine Aufgabe ist damit schon gelöst (A: x = 3, B: x = 1, C: x = 1/6). */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var K = Achsen(fig.querySelector('svg'), { w: 300, h: 280, x0: -4, x1: 6, y0: -8, y1: 8, sy: 2, xm: [-2, 2, 4], ym: [-4, 4] });
    var kr = fig.querySelector('input[data-p="k"]'), fam = fig.querySelector('.sim-wahl'), bewegt = {}, pruefen = function(){};
    kr.addEventListener('input', function(){ bewegt.k = true; zeichnen(); });
    fam.addEventListener('change', zeichnen);
    function ac(f, k){ return f === 'A' ? [k - 2, 3 * (k - 2)] : f === 'B' ? [k - 2, 2] : [k * k - 4, k - 2]; }
    function zust(){
      var k = +kr.value, f = fam.value, p = ac(f, k), L;
      kr.parentNode.querySelector('.sl-val').textContent = z(k);
      if (gl(p[0], 0)) L = gl(p[1], 0) ? 'R' : []; else L = [p[1] / p[0]];
      return { k: k, fam: f, a: p[0], c: p[1], L: L, bewegt: bewegt };
    }
    var sim = { zustand: zust, zeichnen: zeichnen, aufraeumen: function(){ for (var bk in bewegt) delete bewegt[bk]; fam.value = 'A'; } };
    function kT(k){ return k < 0 ? '(' + z(k) + ')' : z(k); }
    // Lösung als Bruch, wo sie keine endliche Dezimalzahl ist (Familie C, k = 1: x = 1/3)
    function bruch(v){ for (var d = 1; d <= 12; d++){ var n = Math.round(v * d); if (gl(v * d, n)) return d === 1 || [2, 4, 5, 8, 10].indexOf(d) >= 0 ? z(v) : (n < 0 ? '−' : '') + Math.abs(n) + '/' + d; } return zz(v); }
    var FORM = { A: '(k − 2) · x = 3 · (k − 2)', B: '(k − 2) · x = 2', C: '(k² − 4) · x = k − 2' };
    function zeichnen(){
      var s = zust(), k = s.k;
      K.leeren();
      K.kurve(function(x){ return s.a * x - s.c; }, 'kurve');
      if (s.L !== 'R' && s.L.length) K.punkt(s.L[0], 0, 'p-loes');
      var einges = s.fam === 'A' ? '(' + kT(k) + ' − 2) · x = 3 · (' + kT(k) + ' − 2)' : s.fam === 'B' ? '(' + kT(k) + ' − 2) · x = 2' : '(' + kT(k) + '² − 4) · x = ' + kT(k) + ' − 2';
      var fall = s.L === 'R' ? 'jede Zahl ist Lösung: 𝕃 = ℝ' : !s.L.length ? 'keine Lösung: 𝕃 = { }' : 'genau eine Lösung: 𝕃 = {' + bruch(s.L[0]) + '}';
      fig.querySelector('[data-rolle="formel"]').innerHTML = sp('tx-blau', FORM[s.fam].replace(/k/g, sp('tx-orange', 'k'))) + '<br><span class="nb">mit k = ' + z(k) + ':</span> <span class="nb">' + einges + ',</span> <span class="nb">also ' + z(s.a) + ' · x = ' + z(s.c) + '</span><br>' + sp('tx-gruen', fall);
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Erkunde Familie A: Zieh an \\(k\\). Was passiert mit der Lösung, was bei \\(k = 2\\)?', ok: function(s){ return s.fam === 'A' && s.bewegt.k; } },
      { text: 'Familie A: Stell \\(k\\) so ein, dass <b>jede</b> Zahl eine Lösung ist.', ok: function(s){ return s.fam === 'A' && s.L === 'R'; } },
      { text: 'Wähle Familie B. Stell \\(k\\) so ein, dass \\(x = 2\\) die Lösung ist.', ok: function(s){ return s.fam === 'B' && s.k === 3; } },
      { text: 'Familie B: Für welches \\(k\\) gibt es <b>keine</b> Lösung?', setup: function(){ fam.value = 'B'; }, ok: function(s){ return s.fam === 'B' && s.L !== 'R' && !s.L.length; } },
      { text: 'Familie B: Die Lösung soll \\(x = -1\\) sein.', setup: function(){ fam.value = 'B'; }, ok: function(s){ return s.fam === 'B' && s.k === 0; } },
      { text: 'Wähle Familie C. Sie hat zwei kritische Werte. Stell den ein, bei dem es <b>keine</b> Lösung gibt.', ok: function(s){ return s.fam === 'C' && s.L !== 'R' && !s.L.length; } },
      { text: 'Familie C: Stell den anderen kritischen Wert ein. Was gilt dort?', setup: function(){ fam.value = 'C'; }, ok: function(s){ return s.fam === 'C' && s.L === 'R'; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Übungen mit Rückmeldung ---------- */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
    function glied(c, v, erst){
      if (c === 0) return '';
      var s = Math.abs(c) === 1 && v ? '' : String(Math.abs(c));
      return (c < 0 ? (erst ? '-' : ' - ') : (erst ? '' : ' + ')) + s + v;
    }
    function lin(m, q){ var t = glied(m, 'x', true); t += glied(q, '', !t); return t || '0'; }
    function vz(v){ return v < 0 ? '-' + (-v) : '+' + v; }        // «+5», «-3» für Umformungen
    function zx(v){ return v === 0 ? 'x' : 'x ' + (v < 0 ? '+ ' + (-v) : '- ' + v); }   // x − v
    function xp(q){ return q < 0 ? 'x - ' + (-q) : 'x + ' + q; }   // x + q
    function zT(v){ return String(+v); }            // volle Genauigkeit: zahl() liest denselben Wert zurück

    /* Feste Aufgaben, die eine Zufallsübung nicht treffen darf (HOWTO §15): Clips · Umformer · Simulation 4 ·
       Aufgaben der Kapitel · Vortest · Gesamttest. Je Typ ein eigener Schlüssel (T.schl); dieselbe Gleichung
       a x + b = c x + d hat in «zweischritt» (c = 0), «linear-loesen» und «normalform» denselben Schlüssel li|a|b|c|d. */
    var SPERRE = [
      // ax + b = cx + d (Kapitel 1 und 4)
      'li|4|7|0|31', 'li|-2|9|0|3', 'li|2|5|0|11', 'li|-1|6|0|2', 'li|3|2|0|11', 'li|3|-1|0|1', 'li|3|-2|0|8', 'li|4|-10|0|0', 'li|-4|0|0|20',
      'li|5|-7|2|8', 'li|2|0|3|-6', 'li|6|-5|2|11', 'li|3|-8|5|2', 'li|-1|7|2|-8', 'li|4|-3|1|9', 'li|-2|7|1|-2', 'li|4|11|9|-4',
      'li|-3|8|1|-12', 'li|5|4|2|-5', 'li|3|-2|1|2', 'li|2|-2|-1|4', 'li|4|-3|2|4', 'li|3|4|1|0', 'li|3|2|-2|9', 'li|1|2|3|-4',
      'li|-1|4|1|-1', 'li|4|-2|-1|6', 'li|3|-5|1|1', 'li|7|-4|3|12', 'li|1|1|-0.5|4', 'li|12|45|0|117', 'li|5|-4|3|0',
      // Klammern: A p(x + q) = s x + r, B c − p(x + q) = s x + r (Kapitel 2 und 3)
      'kl|A|4|-2|2|6', 'kl|B|5|2|1|1|0', 'kl|A|3|-2|1|4', 'kl|B|6|3|1|1|-5', 'kl|A|3|4|0|18', 'kl|A|-2|-4|0|6', 'kl|A|3|-2|2|1',
      'kl|A|2|4|5|-1', 'kl|A|3|2|5|6', 'kl|A|2|-1|-1|4',
      // Nenner: x/m + u = x/n + v
      'ne|3|2|2|-1', 'ne|2|5|1|4', 'ne|4|6|1|0', 'ne|3|4|2|0', 'ne|4|2|3|-1',
      // Lösungsfall: p(x + q) = s x + r
      'lf|2|3|2|9', 'lf|4|2|4|8', 'lf|4|-1|4|3', 'lf|3|2|5|6', 'lf|5|-1|5|-5', 'lf|2|1|2|2', 'lf|3|-2|3|-6', 'lf|2|1|4|-1',
      'lf|2|3|2|7', 'lf|3|4|3|12', 'lf|2|-3|2|-2', 'lf|2|-1|2|1', 'lf|2|0.5|2|1',
      // Fall-Zahl: p(x + q) (Kontrollclip, Aufgabe 3d)
      'fz|2|1', 'fz|3|4',
      // Gleich teuer: G1 + p t = G2 + q t (Gesamttest G5)
      'gs|15|4|0|7', 'gs|10|4|0|7',
      // Parameter: k x + A = n x + B k; (k + a) x = c mit Lösung r
      'pk|2|6|3', 'pk|2|1|0', 'pk|1|-3|2', 'pk|2|-4|2', 'pk|5|5|1',
      'pw|-2|6|3', 'pw|2|1|12|4', 'pw|3|12|4', 'pw|-2|2|2', 'pw|-2|2|-1', 'pw|-4|3|1'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function liSchl(A){ return 'li|' + A.a + '|' + A.b + '|' + A.c + '|' + A.d; }

    var TYPEN = {
      /* ── Kapitel 1 ─────────────────────────────────────────────── */
      'zweischritt': { felder: ['x'], muster: 'x = {x}', schl: liSchl,
        neu: function(){
          var a = zufall([-5, -4, -3, -2, -1, 2, 3, 4, 5, 6, 7, 8]), x = zufallG(-6, 6), b;
          if (a % 2 === 0 && Math.random() < 0.25) x += 0.5;
          do { b = zufallG(-12, 12); } while (b === 0);
          var c = a * x + b;
          return { a: a, b: b, c: 0, d: c, x: x, text: 'Löse \\(' + lin(a, b) + ' = ' + c + '\\).' }; },
        kandidaten: function(A){
          var k = [];
          k.push([(A.d + A.b) / A.a, 'Hinüberbringen']);
          k.push([-A.x, 'samt Vorzeichen']);
          k.push([A.d - A.b - A.a, 'teilen, nicht']);
          return k.filter(function(e, i){ return !gl(e[0], A.x) && !(A.x === 0 && e[1] === 'samt Vorzeichen') &&
            !k.slice(0, i).some(function(f){ return gl(f[0], e[0]); }); }); },
        fehler: function(A){ return this.kandidaten(A).map(function(e){ return [{ x: zT(e[0]) }, e[1] === 'samt Vorzeichen' ? 'Vorzeichen' : e[1]]; }); },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          var k = this.kandidaten(A);
          for (var i = 0; i < k.length; i++) if (gl(e.x, k[i][0])) {
            if (k[i][1] === 'Hinüberbringen') return 'Vorzeichen beim Hinüberbringen: Steht links \\(' + vz(A.b) + '\\), rechnest du beidseitig \\(' + vz(-A.b) + '\\).';
            if (k[i][1] === 'samt Vorzeichen') return A.a < 0 ? 'Vorzeichen: Am Schluss durch \\(' + tz(A.a) + '\\) teilen, samt Vorzeichen. Mach die Probe.' : 'Vorzeichen: Prüf das Vorzeichen des Ergebnisses mit der Probe.';
            return '\\(' + lin(A.a, 0) + '\\) heisst \\(' + tz(A.a) + ' \\cdot x\\): Die Gegenoperation ist teilen, nicht subtrahieren.';
          }
          return 'Zuerst die Zahl \\(' + tz(A.b) + '\\) hinüberbringen, dann durch \\(' + tz(A.a) + '\\) teilen. Mach die Probe.'; },
        loesung: function(A){ return lin(A.a, 0) + ' = ' + (A.d - A.b) + '\\ \\Rightarrow\\ x = ' + texZahl(A.x); } },

      'linear-loesen': { felder: ['x'], muster: 'x = {x}', schl: liSchl,
        neu: function(){
          var a, c, x, b, d;
          do { a = zufallG(-4, 8); c = zufallG(-4, 6); } while (a === c || a === 0 || c === 0 || a - c === 1 && Math.random() < 0.7);
          x = zufallG(-6, 6); b = zufallG(-9, 9); d = (a - c) * x + b;
          return { a: a, b: b, c: c, d: d, x: x, text: 'Löse \\(' + lin(a, b) + ' = ' + lin(c, d) + '\\).' }; },
        kandidaten: function(A){
          var k = [[(A.d + A.b) / (A.a - A.c), 'Hinüberbringen'], [-A.x, 'samt Vorzeichen']];
          if (A.a + A.c !== 0) k.push([(A.d - A.b) / (A.a + A.c), '-Glied rechts']);
          return k.filter(function(e, i){ return isFinite(e[0]) && !gl(e[0], A.x) && !(A.x === 0 && e[1] === 'samt Vorzeichen') &&
            !k.slice(0, i).some(function(f){ return gl(f[0], e[0]); }); }); },
        fehler: function(A){ return this.kandidaten(A).map(function(e){ return [{ x: zT(e[0]) }, e[1] === 'samt Vorzeichen' ? 'Vorzeichen' : e[1]]; }); },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          var k = this.kandidaten(A);
          for (var i = 0; i < k.length; i++) if (gl(e.x, k[i][0])) {
            if (k[i][1] === 'Hinüberbringen') return 'Vorzeichen beim Hinüberbringen: Steht links \\(' + vz(A.b) + '\\), rechnest du beidseitig \\(' + vz(-A.b) + '\\).';
            if (k[i][1] === 'samt Vorzeichen') return A.a - A.c < 0 ? 'Vorzeichen: Am Schluss durch \\(' + tz(A.a - A.c) + '\\) teilen, samt Vorzeichen. Mach die Probe.' : 'Vorzeichen: Prüf das Vorzeichen des Ergebnisses mit der Probe.';
            return 'Das \\(x\\)-Glied rechts: beidseitig \\(' + vz(-A.c) + 'x\\), nicht addieren.';
          }
          return 'Sammle die \\(x\\)-Glieder links und die Zahlen rechts, dann teilen. Mach die Probe.'; },
        loesung: function(A){ return lin(A.a - A.c, 0) + ' = ' + (A.d - A.b) + '\\ \\Rightarrow\\ x = ' + A.x; } },

      /* ── Kapitel 2 ─────────────────────────────────────────────── */
      'klammer': { felder: ['x'], muster: 'x = {x}',
        schl: function(A){ return A.form === 'A' ? 'kl|A|' + A.p + '|' + A.q + '|' + A.s + '|' + A.r : 'kl|B|' + A.c + '|' + A.p + '|' + A.q + '|' + A.s + '|' + A.r; },
        neu: function(){
          // A: p(x + q) = s x + r   B: c − p(x + q) = s x + r; links α x + β
          var form = zufall(['A', 'B']), p = zufall([2, 3, 4, 5, -2, -3]), q, s, x = zufallG(-5, 6), c = 0, al, be;
          do { q = zufallG(-6, 6); } while (q === 0 || q === 1 || q === -1);
          if (form === 'B'){ p = Math.abs(p); c = zufallG(1, 12); }
          al = form === 'A' ? p : -p; be = form === 'A' ? p * q : c - p * q;
          do { s = zufallG(-3, 5); } while (s === al || s === 0);
          var r = al * x + be - s * x;
          var links = form === 'A' ? (p === 1 ? '' : p === -1 ? '-' : tz(p)) + '(' + xp(q) + ')' : c + ' - ' + (p === 1 ? '' : p) + '(' + xp(q) + ')';
          return { form: form, p: p, q: q, c: c, s: s, r: r, al: al, be: be, x: x, text: 'Löse \\(' + links + ' = ' + lin(s, r) + '\\).' }; },
        kandidaten: function(A){
          var k = [];
          if (A.form === 'A') k.push([(A.r - A.q) / (A.al - A.s), 'jedes Glied']);
          else { k.push([(A.r - (A.c + A.p * A.q)) / (A.al - A.s), 'jedes Vorzeichen']); k.push([(A.r - (A.c - A.q)) / (A.al - A.s), 'jedes Glied']); }
          return k.filter(function(e, i){ return isFinite(e[0]) && !gl(e[0], A.x) && !k.slice(0, i).some(function(f){ return gl(f[0], e[0]); }); }); },
        fehler: function(A){ return this.kandidaten(A).map(function(e){ return [{ x: zT(e[0]) }, e[1] === 'samt Vorzeichen' ? 'Vorzeichen' : e[1]]; }); },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          var k = this.kandidaten(A);
          for (var i = 0; i < k.length; i++) if (gl(e.x, k[i][0])) {
            if (k[i][1] === 'jedes Vorzeichen') return 'Das Minus vor der Klammer dreht jedes Vorzeichen in der Klammer: \\(-' + (A.p === 1 ? '' : A.p) + '(' + xp(A.q) + ') = ' + lin(-A.p, -A.p * A.q) + '\\).';
            return 'Der Faktor vor der Klammer gilt für jedes Glied in der Klammer: \\(' + tz(A.form === 'A' ? A.p : -A.p) + ' \\cdot ' + (A.q < 0 ? '(' + A.q + ')' : A.q) + ' = ' + tz((A.form === 'A' ? A.p : -A.p) * A.q) + '\\).';
          }
          return 'Zuerst die Klammer auflösen, dann sortieren und teilen. Mach die Probe.'; },
        loesung: function(A){ return lin(A.al, A.be) + ' = ' + lin(A.s, A.r) + '\\ \\Rightarrow\\ x = ' + A.x; } },

      'nenner': { felder: ['x'], muster: 'x = {x}',
        schl: function(A){ return 'ne|' + A.m + '|' + A.n + '|' + A.u + '|' + A.v; },
        neu: function(){
          var m, n; do { m = zufall([2, 3, 4, 5, 6]); n = zufall([2, 3, 4, 5, 6]); } while (m === n);
          var L = m * n / ggT(m, n), j = zufall([-3, -2, -1, 1, 2, 3]), x = L * j, u = zufallG(-6, 6);
          var v = x / m + u - x / n;
          function seite(d, w){ return '\\tfrac{x}{' + d + '}' + (w ? (w < 0 ? ' - ' + (-w) : ' + ' + w) : ''); }
          return { m: m, n: n, u: u, v: v, L: L, x: x, text: 'Löse \\(' + seite(m, u) + ' = ' + seite(n, v) + '\\).' }; },
        fehler: function(A){ return [[{ x: zT(A.x / A.L) }, 'jedes Glied']]; },
        pruefen: function(A, e){
          if (gl(e.x, A.x)) return null;
          if (gl(e.x, A.x / A.L)) return 'Mal \\(' + A.L + '\\) heisst: jedes Glied auf beiden Seiten, auch die Zahlen ohne Bruch.';
          return 'Mit dem Hauptnenner \\(' + A.L + '\\) multiplizieren (jedes Glied), dann sortieren. Mach die Probe.'; },
        loesung: function(A){ return '\\cdot ' + A.L + ':\\ ' + lin(A.L / A.m, A.L * A.u) + ' = ' + lin(A.L / A.n, A.L * A.v) + '\\ \\Rightarrow\\ x = ' + A.x; } },

      /* ── Kapitel 3 ─────────────────────────────────────────────── */
      'loesungsfall': { felder: ['fall', 'L'], muster: '{fall:genau eine Lösung|keine Lösung|jede Zahl ist Lösung}; 𝕃 = {L}',
        schl: function(A){ return 'lf|' + A.p + '|' + A.q + '|' + A.s + '|' + A.r; },
        eingabe: function(A){ return { fall: A.fall, L: A.L === 'R' ? 'R' : '{' + A.L.join('; ') + '}' }; },
        neu: function(){
          var p = zufall([2, 3, 4, 5, -2, -3]), q = zufall([-4, -3, -2, -1, 1, 2, 3, 5]), art = zufall(['R', 'leer', 'eine']), s = p, r, L, fall;
          if (art === 'R'){ r = p * q; L = 'R'; fall = 'jede Zahl ist Lösung'; }
          else if (art === 'leer'){ r = p * q + zufall([-3, -2, -1, 1, 2, 4]); L = []; fall = 'keine Lösung'; }
          else { s = p + zufall([-2, -1, 1, 2, 3]); if (s === 0) s = p + 4; var x = zufallG(-5, 5); r = (p - s) * x + p * q; L = [x]; fall = 'genau eine Lösung'; }
          return { p: p, q: q, s: s, r: r, L: L, fall: fall, text: 'Welcher Lösungsfall liegt vor? \\(' + tz(p) + '(' + xp(q) + ') = ' + lin(s, r) + '\\)' }; },
        fehler: function(A){ return A.L === 'R' ? [[{ fall: 'keine Lösung', L: '{}' }, 'wahr oder falsch']] : !A.L.length ? [[{ fall: 'jede Zahl ist Lösung', L: 'R' }, 'wahr oder falsch'], [{ fall: 'keine Lösung', L: '{0}' }, 'Zahl 0']] :
          [[{ fall: 'genau eine Lösung', L: '{' + (A.L[0] + 1) + '}' }, 'nochmals']]; },
        pruefen: function(A, e){
          var m = menge(e.L);
          if (m.kaputt) return 'Lösungsmenge wie <code>{3}</code>, <code>{}</code> oder <code>R</code>.';
          if (e.fall === A.fall && mengeGleich(m, A.L)) return null;
          if (e.fall !== A.fall) return 'Klammer auflösen und die \\(x\\)-Glieder sammeln: Bleibt \\(x\\) stehen? Wenn nein: Ist die Aussage, die bleibt, wahr oder falsch?';
          if (A.L === 'R') return 'Bei «jede Zahl» heisst die Lösungsmenge \\(\\mathbb{R}\\): <code>R</code>.';
          if (!A.L.length) return mengeGleich(m, [0]) ? '\\(\\{0\\}\\) enthält die Zahl 0. Keine Lösung heisst leere Menge: <code>{}</code>.' : 'Keine Lösung: leere Menge <code>{}</code>.';
          return 'Der Fall stimmt. Rechne \\(x\\) nochmals nach und mach die Probe.'; },
        loesung: function(A){ return lin(A.p, A.p * A.q) + ' = ' + lin(A.s, A.r) + ':\\ ' + mengeTex(A.L); } },

      'fall-zahl': { felder: ['z'], muster: '□ = {z}',
        schl: function(A){ return 'fz|' + A.p + '|' + A.q; },
        eingabe: function(A){ return { z: String(A.v === 'keineZahl' ? A.p * A.q + 1 : A.soll) }; },
        neu: function(){
          var p = zufall([2, 3, 4, 5, 6, -2, -3]), q = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), v = zufall(['alle', 'keineX', 'keineZahl']);
          var li = tz(p) + '(' + xp(q) + ')', A = { p: p, q: q, v: v };
          if (v === 'alle'){ A.soll = p * q; A.text = 'Für welche Zahl \\(\\square\\) hat \\(' + li + ' = ' + lin(p, 0) + ' + \\square\\) unendlich viele Lösungen?'; }
          else if (v === 'keineX'){ A.r = p * q + zufall([-3, -2, -1, 1, 2, 3]); A.soll = p;
            A.text = 'Für welche Zahl \\(\\square\\) hat \\(' + li + ' = \\square \\cdot x ' + (A.r < 0 ? '- ' + (-A.r) : '+ ' + A.r) + '\\) keine Lösung?'; }
          else A.text = 'Gib eine Zahl \\(\\square\\) an, für die \\(' + li + ' = ' + lin(p, 0) + ' + \\square\\) keine Lösung hat.';
          return A; },
        fehler: function(A){
          if (A.v === 'alle') return [[{ z: String(A.q) }, 'jedes Glied'], [{ z: String(-A.p * A.q) }, 'Vorzeichen']].filter(function(f){ return +f[0].z !== A.soll; });
          if (A.v === 'keineX') return [[{ z: String(A.p + 1) }, 'genau eine'], [{ z: '0' }, 'genau eine']];
          return [[{ z: String(A.p * A.q) }, 'jede Zahl']]; },
        pruefen: function(A, e){
          var pq = A.p * A.q;
          if (A.v === 'keineZahl'){
            if (!gl(e.z, pq)) return null;
            return 'Mit \\(' + pq + '\\) steht links und rechts dasselbe: Dann ist jede Zahl Lösung. Gesucht ist keine Lösung.';
          }
          if (gl(e.z, A.soll)) return null;
          if (A.v === 'alle'){
            if (gl(e.z, A.q)) return 'Der Faktor \\(' + tz(A.p) + '\\) gilt für jedes Glied in der Klammer: Links steht \\(' + lin(A.p, pq) + '\\).';
            if (gl(e.z, -pq)) return 'Vorzeichen: Löse die Klammer auf, \\(' + lin(A.p, pq) + '\\). Rechts muss genau dasselbe stehen.';
            return 'Löse die Klammer links auf. Unendlich viele Lösungen heisst: Rechts steht genau dasselbe.';
          }
          return 'Mit \\(\\square = ' + zT(e.z) + '\\) bleibt \\(x\\) nach dem Sortieren stehen: genau eine Lösung. Keine Lösung gibt es nur, wenn sich die \\(x\\)-Glieder wegheben.'; },
        loesung: function(A){ var pq = A.p * A.q;
          return A.v === 'alle' ? lin(A.p, pq) + ' = ' + lin(A.p, 0) + ' + ' + (pq < 0 ? '(' + pq + ')' : pq) + ':\\ \\square = ' + pq
            : A.v === 'keineX' ? '\\square = ' + A.p + ':\\ ' + lin(A.p, pq) + ' = ' + lin(A.p, A.r) + '\\ \\Rightarrow\\ ' + pq + ' = ' + A.r + '\\ \\text{(falsch)}'
            : '\\text{jede Zahl ausser } ' + pq; } },

      /* ── Kapitel 4 ─────────────────────────────────────────────── */
      'normalform': { felder: ['a', 'b', 'x'], muster: '{a} · x + {b} = 0; x = {x}', schl: liSchl,
        eingabe: function(A){ return { a: String(A.a - A.c), b: String(A.b - A.d), x: zT(A.x) }; },
        neu: function(){
          var a, c, x, b, d;
          do { a = zufallG(-4, 8); c = zufallG(-4, 6); } while (a === c || a === 0 || c === 0);
          x = zufallG(-6, 6); if ((a - c) % 2 === 0 && Math.random() < 0.3) x += 0.5;
          do { b = zufallG(-9, 9); } while (b === 0);
          d = (a - c) * x + b;
          if (d === 0 || x === 0) return TYPEN['normalform'].neu();   // x = 0 hiesse b = 0: dann wäre jedes a «gleichwertig»
          return { a: a, b: b, c: c, d: d, x: x, text: 'Bring \\(' + lin(a, b) + ' = ' + lin(c, d) + '\\) auf die Normalform \\(a \\cdot x + b = 0\\) und gib die Lösung an. (\\(b\\) darf negativ sein.)' }; },
        fehler: function(A){ var f = [[{ a: String(A.a - A.c), b: String(A.b + A.d), x: zT(A.x) }, 'Vorzeichen']];
          if (A.a + A.c !== 0 && A.c !== 0) f.push([{ a: String(A.a + A.c), b: String(A.b - A.d), x: zT(A.x) }, '-Glied rechts']);
          if (A.x !== 0) f.push([{ a: String(A.a - A.c), b: String(A.b - A.d), x: zT(-A.x) }, '−b']);
          return f; },
        pruefen: function(A, e){
          var a0 = A.a - A.c, b0 = A.b - A.d, r = [];
          var nfOk = !gl(e.a, 0) && gl(e.a * b0, e.b * a0);
          if (nfOk && gl(e.x, A.x)) return null;
          if (!nfOk){
            if (gl(e.a, a0) && gl(e.b, A.b + A.d)) r.push('Vorzeichen: Die Zahl rechts kommt mit umgekehrtem Vorzeichen nach links, \\(' + vz(-A.d) + '\\).');
            else if (gl(e.a, A.a + A.c)) r.push('Das \\(x\\)-Glied rechts kommt mit \\(' + vz(-A.c) + 'x\\) nach links.');
            else r.push('Bring alles nach links: \\(' + vz(-A.c) + 'x\\) und \\(' + vz(-A.d) + '\\), dann zusammenfassen.');
          }
          if (!gl(e.x, A.x)) r.push(gl(e.x, -A.x) ? 'Die Lösung ist \\(x = -\\tfrac{b}{a}\\), das Minus nicht vergessen (−b).' : 'Die Lösung ist \\(x = -\\tfrac{b}{a}\\). Mach die Probe.');
          return r.join(' '); },
        loesung: function(A){ var a0 = A.a - A.c, b0 = A.b - A.d; return lin(a0, b0) + ' = 0\\ \\Rightarrow\\ x = -\\tfrac{' + b0 + '}{' + a0 + '} = ' + texZahl(A.x); } },

      'gleichstand': { felder: ['t', 'K'], muster: 't = {t} h; K = {K} CHF',
        schl: function(A){ return 'gs|' + A.G1 + '|' + A.p + '|' + A.G2 + '|' + A.q; },
        neu: function(){
          var ort = zufall(['Velo-Verleih', 'Kletterhalle', 'Parkhaus', 'Carsharing']), p = zufallG(2, 6), d = zufall([1, 2, 3, 4, 5]), t = zufallG(2, 8);
          var G2 = zufall([0, 0, 5, 10]), q = p + d, G1 = G2 + d * t;
          return { ort: ort, p: p, q: q, G1: G1, G2: G2, t: t, K: G1 + p * t,
            text: ort + ': Anbieter A kostet \\(K_A(t) = ' + G1 + ' + ' + p + 't\\), Anbieter B \\(K_B(t) = ' + (G2 ? G2 + ' + ' : '') + q + 't\\) (\\(t\\) in h, \\(K\\) in CHF). Bei welcher Dauer kosten beide gleich viel, und wie viel?' }; },
        fehler: function(A){ var f = [[{ t: String(A.t), K: String(A.q * A.t) }, 'Kosten']];
          var t2 = (A.G1 + A.G2) / (A.q - A.p); if (!gl(t2, A.t)) f.push([{ t: zT(t2), K: zT(A.G1 + A.p * t2) }, 'Grundgebühr']);
          return A.G2 ? f : [[{ t: zT(A.G1 / (A.q + A.p)), K: zT(A.G1 + A.p * A.G1 / (A.q + A.p)) }, 'Gleichsetzen']]; },
        pruefen: function(A, e){
          var r = [];
          if (!gl(e.t, A.t)){
            if (A.G2 && gl(e.t, (A.G1 + A.G2) / (A.q - A.p))) r.push('Grundgebühr: Gleichsetzen und sortieren, \\(' + A.G1 + ' - ' + A.G2 + ' = ' + (A.q - A.p) + 't\\).');
            else if (!A.G2 && gl(e.t, A.G1 / (A.q + A.p))) r.push('Beim Gleichsetzen: \\(' + A.G1 + ' + ' + A.p + 't = ' + A.q + 't\\), also beidseitig \\(-' + A.p + 't\\).');
            else r.push('Setz \\(K_A(t) = K_B(t)\\) und löse nach \\(t\\).');
          } else if (!gl(e.K, A.K)) r.push('Die Kosten: \\(t = ' + A.t + '\\) in \\(K_A\\) oder \\(K_B\\) einsetzen, beide geben denselben Wert.');
          if (!gl(e.t, A.t) && !r.length) r.push('Setz \\(K_A(t) = K_B(t)\\).');
          return r.length ? r.join(' ') : null; },
        loesung: function(A){ return A.G1 + ' + ' + A.p + 't = ' + (A.G2 ? A.G2 + ' + ' : '') + A.q + 't\\ \\Rightarrow\\ ' + (A.G1 - A.G2) + ' = ' + (A.q - A.p) + 't,\\ t = ' + A.t + '\\ \\text{h};\\ K = ' + A.K + '\\ \\text{CHF}'; } },

      /* ── Kapitel 5 ─────────────────────────────────────────────── */
      'param-krit': { felder: ['k', 'fall'], muster: 'kritisch: k = {k}; dort: {fall:keine Lösung|jede Zahl ist Lösung|genau eine Lösung}',
        schl: function(A){ return 'pk|' + A.n + '|' + A.A + '|' + A.B; },
        eingabe: function(A){ return { k: String(A.n), fall: A.R ? 'jede Zahl ist Lösung' : 'keine Lösung' }; },
        neu: function(){
          // k x + A = n x + B k  ⇔  (k − n) x = B k − A; bei k = n: 0 = B n − A
          var n = zufall([-3, -2, -1, 1, 2, 3, 4]), B = zufall([1, 2, 3, -1, -2]), R = Math.random() < 0.5;
          var A = R ? B * n : B * n + zufall([-4, -3, -2, -1, 1, 2, 3, 5]);
          if (A === 0) A = 7;                       // nur im Fall «keine Lösung» möglich (B n ≠ 0)
          var links = 'kx' + glied(A, '', false), rechts = glied(n, 'x', true) + glied(B, 'k', false);
          return { n: n, A: A, B: B, R: R, text: 'Für welches \\(k\\) gibt es nicht genau eine Lösung, und was gilt dort? \\(' + links + ' = ' + rechts + '\\)' }; },
        fehler: function(A){ return [[{ k: String(-A.n), fall: A.R ? 'jede Zahl ist Lösung' : 'keine Lösung' }, 'Vorzeichen'],
                                     [{ k: String(A.n), fall: A.R ? 'keine Lösung' : 'jede Zahl ist Lösung' }, 'rechts ein']]; },
        pruefen: function(A, e){
          var r = [], soll = A.R ? 'jede Zahl ist Lösung' : 'keine Lösung';
          if (gl(e.k, A.n) && e.fall === soll) return null;
          if (!gl(e.k, A.n)) r.push(gl(e.k, -A.n) ? 'Vorzeichen: Sortiert steht \\((k ' + (A.n < 0 ? '+ ' + (-A.n) : '- ' + A.n) + ') \\cdot x\\), der Faktor wird null bei \\(k = ' + A.n + '\\).' : 'Sortiere auf \\(a(k) \\cdot x = c(k)\\): Kritisch ist das \\(k\\), bei dem der Faktor vor \\(x\\) null wird.');
          if (e.fall !== soll) r.push(e.fall === 'genau eine Lösung' ? 'Beim kritischen \\(k\\) verschwindet \\(x\\): Dann gibt es nie genau eine Lösung.' : 'Setz das kritische \\(k\\) rechts ein: ' + (A.R ? 'Rechts wird es auch \\(0\\), und \\(0 = 0\\) ist wahr.' : 'Rechts bleibt \\(' + tz(A.B * A.n - A.A) + ' \\neq 0\\), und \\(0 = ' + tz(A.B * A.n - A.A) + '\\) ist falsch.'));
          return r.join(' '); },
        loesung: function(A){ var c = A.B * A.n - A.A; return '(k ' + (A.n < 0 ? '+ ' + (-A.n) : '- ' + A.n) + ') \\cdot x = ' + lin(A.B, -A.A).replace(/x/g, 'k') + ';\\ k = ' + A.n + ':\\ 0 = ' + c + (A.R ? ',\\ \\mathbb{L} = \\mathbb{R}' : ',\\ \\mathbb{L} = \\{\\,\\}'); } },

      /* (p k + a) · x = c mit der Lösung x = r. Seit der Prüfung 11.10.2026: auch p = 2, 3 (Faktor vor k, wie G7
         im Gesamttest), |r| ≥ 2 — bei r = ±1 fielen «mal statt durch» und «Faktor vergessen» mit der Lösung zusammen. */
      'param-wert': { felder: ['k'], muster: 'k = {k}',
        schl: function(A){ return 'pw|' + (A.p === 1 ? '' : A.p + '|') + A.a + '|' + A.c + '|' + A.r; },
        neu: function(){
          var p = zufall([1, 1, 2, 3]), a = zufall([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), r = zufall([-4, -3, -2, 2, 3, 4]), m;
          do { m = zufall([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]); } while (p > 1 && ((m - a) * 2) % p !== 0);
          var c = r * m, k = (m - a) / p;
          if (k === 0 && Math.random() < 0.7) return TYPEN['param-wert'].neu();
          return { p: p, a: a, r: r, c: c, m: m, k: k, text: 'Für welches \\(k\\) hat \\((' + this.fak(p, a) + ') \\cdot x = ' + c + '\\) die Lösung \\(x = ' + r + '\\)?' }; },
        fak: function(p, a){ return (p === 1 ? 'k' : p + 'k') + (a < 0 ? ' - ' + (-a) : ' + ' + a); },
        kandidaten: function(A){
          var k = [[(A.m + A.a) / A.p, 'Vorzeichen'], [(A.c * A.r - A.a) / A.p, 'teilen'], [(A.c - A.a) / A.p, 'Einsetzen']];
          if (A.p > 1) k.push([A.m - A.a, 'Faktor vor']);
          return k.filter(function(e, i){ return !gl(e[0], A.k) && !k.slice(0, i).some(function(f){ return gl(f[0], e[0]); }); }); },
        fehler: function(A){ return this.kandidaten(A).map(function(e){ return [{ k: zT(e[0]) }, e[1]]; }); },
        pruefen: function(A, e){
          if (gl(e.k, A.k)) return null;
          var k = this.kandidaten(A), f = this.fak(A.p, A.a), rr = A.r < 0 ? '(' + A.r + ')' : A.r;
          for (var i = 0; i < k.length; i++) if (gl(e.k, k[i][0])) {
            if (k[i][1] === 'Vorzeichen') return 'Vorzeichen: Aus \\(' + f + ' = ' + A.m + '\\) folgt \\(' + (A.p === 1 ? 'k' : A.p + 'k') + ' = ' + A.m + ' ' + (A.a < 0 ? '+ ' + (-A.a) : '- ' + A.a) + '\\).';
            if (k[i][1] === 'teilen') return 'Setz \\(x = ' + A.r + '\\) ein: \\((' + f + ') \\cdot ' + rr + ' = ' + A.c + '\\). Dann durch \\(' + A.r + '\\) teilen, nicht multiplizieren.';
            if (k[i][1] === 'Faktor vor') return 'Fast: Aus \\(' + A.p + 'k = ' + (A.m - A.a) + '\\) folgt noch durch \\(' + A.p + '\\) teilen — der Faktor vor \\(k\\) gehört dazu.';
            return 'Beim Einsetzen fehlt der Faktor \\(' + A.r + '\\): \\((' + f + ') \\cdot ' + rr + ' = ' + A.c + '\\). Teile zuerst durch \\(' + A.r + '\\).';
          }
          return 'Setz \\(x = ' + A.r + '\\) ein und löse nach \\(k\\). Probe: Für dein \\(k\\) muss \\(x = ' + A.r + '\\) herauskommen.'; },
        loesung: function(A){ return '(' + this.fak(A.p, A.a) + ') \\cdot ' + (A.r < 0 ? '(' + A.r + ')' : A.r) + ' = ' + A.c + '\\ \\Rightarrow\\ ' + this.fak(A.p, A.a) + ' = ' + A.m + ',\\ k = ' + texZahl(A.k); } }
    };
    function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        A = T.neu();
        for (var v = 0; v < 40 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="text" autocomplete="off" aria-label="' + f + '" data-f="' + f + '"' + (f === 'L' ? ' class="menge" placeholder="{ … }"' : '') + '>';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){
          if (i.dataset.f === 'L'){ e.L = i.value; var mm = menge(i.value); if (mm.leer) leer = true; if (mm.komma) komma = true; return; }
          var r = zahl(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen wie <code>-3</code>, <code>0.5</code>, <code>1/2</code>.'; return; }
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

  /* ---------- Minigrafen: <svg class="mini" data-k="g,m,q;…"> — Geraden y = m x + q, die erste blau, die zweite orange;
       data-fenster="x0,x1,y0,y1", data-xm/data-ym (beschriftete Stellen), data-sx/data-sy (Gitter),
       data-xname/data-yname (Achsen mit Grösse und Einheit), data-titel. ---------- */
  document.querySelectorAll('svg.mini[data-k]').forEach(function(svg){
    var fe = (svg.dataset.fenster || '-5,5,-5,5').split(',').map(Number);
    svg.setAttribute('viewBox', '0 0 170 170'); svg.setAttribute('role', 'img');
    var liste = function(t, d){ return t ? t.split(',').map(Number) : d; };
    var K = Achsen(svg, { w: 170, h: 170, x0: fe[0], x1: fe[1], y0: fe[2], y1: fe[3], r: 3, sy: +svg.dataset.sy || 1, sx: +svg.dataset.sx || 1, pfeil: 6,
      xm: liste(svg.dataset.xm, []), ym: liste(svg.dataset.ym, []), xname: svg.dataset.xname, yname: svg.dataset.yname });
    svg.dataset.k.split(';').filter(Boolean).forEach(function(s, i){
      var q = s.split(',').slice(1).map(Number);
      K.kurve(function(x){ return q[0] * x + q[1]; }, 'kurve' + (i ? ' k' + i : ''));
    });
    if (svg.dataset.titel) el(svg, 'text', { x: 6, y: 14, 'class': 'mini-titel' }, svg.dataset.titel);
    if (!svg.getAttribute('aria-label')) svg.setAttribute('aria-label', 'Graph' + (svg.dataset.titel ? ' ' + svg.dataset.titel : ''));
  });
})();
</script>
