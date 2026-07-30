// ─────────────────────────────────────────────────────────────
//  TALS Mathematik — Shared Math/Canvas Library (mathlib.js)
//
//  Single Source of Truth für alle Themenseiten:
//    - Canvas-Helper (initCanvas, drawGrid, drawLine, drawDot)
//    - Zahlen-Formatierer (fmt, fmtS, fmtMx)
//    - Term-Parser (parseL)   ─ tolerant, FTB-konform
//    - Lösungs-Toggle (toggleL)
//
//  Einbindung auf Themenseiten:
//    <script src="../mathlib.js"></script>
//
//  Achsenskalierung (gemäss STYLEGUIDE §3):
//    - initCanvas(id, H, true)   → reine Mathematik (1:1, square)
//    - initCanvas(id, H, false)  → Anwendungsaufgaben (aufgabenbezogen)
//
//  Bei Anwendungsaufgaben die generischen Achsenlabels „x"/„y" NICHT
//  übermalen, sondern gar nicht zeichnen lassen — und die eigenen mit
//  beschriftung() setzen, damit sie freigestellt und im Canvas bleiben:
//    const {cx, cy} = drawGrid(ctx, W, H, 0, 15, 0, 35, {achsenLabels:false});
//    ctx.fillStyle='#374151'; ctx.font='bold 13px monospace';
//    beschriftung(ctx, 'x [kg]',  W-2,      cy(0)-7, {align:'right', W, H});
//    beschriftung(ctx, 'K [CHF]', cx(0)+5,  11,      {align:'left',  W, H});
//  Mit eigener Zahlenteilung zusätzlich {zahlen:false}, sonst liegen zwei
//  Zahlenreihen übereinander. Der frühere fillRect-Trick liess je nach
//  Skalierung einen Strichrest des generischen Labels stehen.
// ─────────────────────────────────────────────────────────────

/* ── Zahlen-Formatierer ──────────────────────────────────── */
const fmt  = n => n === 0 ? '0' : (n % 1 === 0 ? n.toString() : n.toFixed(1));
// Vorzeichen-Term für Verkettung: '+ 5' / '− 5' (Unicode-Minus U+2212)
const fmtS = n => n >= 0 ? `+ ${fmt(n)}` : `− ${fmt(Math.abs(n))}`;
// Steigungsterm m·x mit Sonderfällen für m∈{0,1,−1}, sonst „m·x" (FTB-konform mit ·)
// Verwendet Unicode-Minus U+2212 (−), konsistent zu fmtS.
const fmtMx = m => {
  if (m === 0)  return '0';
  if (m === 1)  return 'x';
  if (m === -1) return '−x';
  if (m < 0)    return `−${fmt(Math.abs(m))}·x`;
  return `${fmt(m)}·x`;
};
// Komplette affin-lineare Funktion m·x + b mit sauberer Behandlung der Sonderfälle:
//   m=0, b=5  →  '5'
//   m=2, b=0  →  '2·x'
//   m=0, b=0  →  '0'
//   m=2, b=5  →  '2·x + 5'
//   m=2, b=-5 →  '2·x − 5'
const fmtAffine = (m, b) => {
  if (m === 0) return fmt(b);
  if (b === 0) return fmtMx(m);
  return `${fmtMx(m)} ${fmtS(b)}`;
};

/* ── Term-Parser ──────────────────────────────────────────
   Toleranter Eingabe-Parser für lineare Funktionen:
   - Whitespace entfernen, Komma → Punkt, Unicode-Minus → ASCII
   - Multiplikationszeichen (·, *, ×) zwischen Zahl und x entfernen
   Liefert {m, b} oder null bei Parsefehler.
─────────────────────────────────────────────────────────── */
function parseL(s) {
  s = s.replace(/\s/g, '').replace(/,/g, '.').toLowerCase().replace(/−/g, '-')
       .replace(/([0-9.])[·*×]x/g, '$1x')
       .replace(/[·*×]x/g, 'x');
  const m1 = s.match(/^(-?[\d.]+)x([+-][\d.]+)$/); if (m1) return { m: +m1[1], b: +m1[2] };
  const m2 = s.match(/^(-?[\d.]+)x$/);             if (m2) return { m: +m2[1], b: 0 };
  const m3 = s.match(/^x([+-][\d.]+)$/);           if (m3) return { m: 1,      b: +m3[1] };
  const m4 = s.match(/^-x([+-][\d.]+)$/);          if (m4) return { m: -1,     b: +m4[1] };
  if (s === 'x')  return { m: 1,  b: 0 };
  if (s === '-x') return { m: -1, b: 0 };
  return null;
}

/* ── Beschriftung mit Freistellung ────────────────────────
   Zeichnet Text und legt vorher ein Feld in Hintergrundfarbe darunter, damit
   die Beschriftung auf Gitterlinien, Kurven und Flächen lesbar bleibt. Das
   Feld wird zusätzlich in den Canvas geklemmt — so läuft keine Beschriftung
   über den Rand hinaus und verschwindet.

   beschriftung(ctx, txt, x, y, {align, baseline, frei, halo, bg, pad, W, H})
     align/baseline  wie ctx.textAlign / ctx.textBaseline (Standard left/alphabetic)
     frei:false      keine Freistellung, nur Klemmen
     halo:true       statt eines Kastens eine Kontur entlang der Buchstaben.
                     Richtig überall, wo der Untergrund nicht einfarbig ist —
                     Geometriefiguren mit Füllung, farbige Bereiche, Fotos.
     bg              Farbe der Freistellung. Fehlt sie, wird der Untergrund an
                     den vier Ecken des Textfelds abgetastet und die häufigste
                     Farbe genommen; das passt sich Papier, Weiss und Füllungen
                     von selbst an.
     pad             Luft um den Text (Standard 2 px)
     W, H            Canvasmasse; nur mit ihnen kann geklemmt werden
   Rückgabe: die tatsächlich benutzte Position {x, y}.

   Farbe und Font kommen wie bei fillText vom Aufrufer (ctx.fillStyle/ctx.font). */
/* Helligkeit 0…1 aus einer CSS-Farbe, soweit sie sich lesen lässt. */
function _helligkeit(farbe) {
  let r, g, b;
  const s = String(farbe).trim();
  let m = s.match(/^#([0-9a-f]{3})$/i);
  if (m) { r = parseInt(m[1][0] + m[1][0], 16); g = parseInt(m[1][1] + m[1][1], 16); b = parseInt(m[1][2] + m[1][2], 16); }
  if (!m) {
    m = s.match(/^#([0-9a-f]{6})$/i);
    if (m) { r = parseInt(m[1].slice(0, 2), 16); g = parseInt(m[1].slice(2, 4), 16); b = parseInt(m[1].slice(4, 6), 16); }
  }
  if (!m) {
    m = s.match(/rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/i);
    if (m) { r = +m[1]; g = +m[2]; b = +m[3]; }
  }
  if (!m) return null;
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
}

/* Untergrund an den vier Ecken des Textfelds abtasten. Genommen wird die
   häufigste Farbe — aber nur, wenn sie zur Textfarbe kontrastiert. An einem
   Eckpunkt, wo zwei dunkle Figurenkanten zusammenlaufen, würden sonst alle
   vier Proben dunkel ausfallen und der Halo den Buchstaben zum Klumpen machen. */
function _bgTasten(ctx, x0, y0, x1, y1, textFarbe) {
  const stellen = [[x0 - 2, y0 - 2], [x1 + 2, y0 - 2], [x0 - 2, y1 + 2], [x1 + 2, y1 + 2]];
  const zahl = new Map();
  for (const [px, py] of stellen) {
    let d;
    try { d = ctx.getImageData(Math.round(px), Math.round(py), 1, 1).data; } catch (e) { continue; }
    if (d[3] < 8) continue;                       // transparent -> nichts gelernt
    const k = `rgb(${d[0]},${d[1]},${d[2]})`;
    zahl.set(k, (zahl.get(k) || 0) + 1);
  }
  let best = null, max = 0;
  for (const [k, n] of zahl) if (n > max) { max = n; best = k; }
  // Nur eine klare Mehrheit gilt als Hintergrund. Sitzt die Beschriftung an
  // einer Achse oder Kante, treffen ein bis zwei Proben die Linie statt des
  // Papiers — dann ist die Probe wertlos und die Notfarbe ist besser.
  if (!best || max < 3) return null;
  const hT = _helligkeit(textFarbe), hB = _helligkeit(best);
  if (hT !== null && hB !== null && Math.abs(hT - hB) < 0.35) return null;   // zu wenig Kontrast
  return best;
}
function beschriftung(ctx, txt, x, y, opt) {
  opt = opt || {};
  const s = String(txt);
  const altAlign = ctx.textAlign, altBase = ctx.textBaseline, altFill = ctx.fillStyle;
  ctx.textAlign = opt.align || 'left';
  ctx.textBaseline = opt.baseline || 'alphabetic';
  const m = ctx.measureText(s);
  let l = m.actualBoundingBoxLeft, r = m.actualBoundingBoxRight;
  let a = m.actualBoundingBoxAscent, d = m.actualBoundingBoxDescent;
  if (!isFinite(l) || !isFinite(r)) { l = 0; r = m.width; }   // ältere Engines
  if (!isFinite(a) || !isFinite(d)) { a = 10; d = 3; }
  const pad = opt.pad === undefined ? 2 : opt.pad;
  if (opt.W !== undefined) {
    if (x - l - pad < 0) x = l + pad;
    if (x + r + pad > opt.W) x = opt.W - r - pad;
  }
  if (opt.H !== undefined) {
    if (y - a - pad < 0) y = a + pad;
    if (y + d + pad > opt.H) y = opt.H - d - pad;
  }
  if (opt.frei !== false) {
    // Ohne brauchbare Probe die zur Textfarbe passende Notfarbe: heller Text
    // bekommt einen dunklen Halo, dunkler Text einen hellen.
    // Schwelle bewusst hoch: mittelgraue Beschriftungen (#9ca3af ≈ 0.62)
    // sind noch „dunkler Text" und brauchen einen hellen Halo.
    const hell = (_helligkeit(altFill) || 0) > 0.75;
    const bg = opt.bg || _bgTasten(ctx, x - l, y - a, x + r, y + d, altFill)
               || (hell ? '#1c1a17' : '#fff');
    if (opt.halo) {
      const altStroke = ctx.strokeStyle, altLw = ctx.lineWidth, altJoin = ctx.lineJoin;
      ctx.strokeStyle = bg; ctx.lineWidth = opt.pad === undefined ? 3.5 : 2 * pad;
      ctx.lineJoin = 'round';
      ctx.strokeText(s, x, y);
      ctx.strokeStyle = altStroke; ctx.lineWidth = altLw; ctx.lineJoin = altJoin;
    } else {
      ctx.fillStyle = bg;
      ctx.fillRect(x - l - pad, y - a - pad, l + r + 2 * pad, a + d + 2 * pad);
    }
  }
  ctx.fillStyle = altFill;
  ctx.fillText(s, x, y);
  ctx.textAlign = altAlign; ctx.textBaseline = altBase;
  return { x, y };
}

/* ── Canvas-Helper ──────────────────────────────────────── */
function initCanvas(id, H, square) {
  const c = document.getElementById(id);
  const dpr = window.devicePixelRatio || 1;
  const W = c.offsetWidth || 600;
  const actualH = square ? W : H;   // square mode: height = width für 1:1
  c.width = W * dpr; c.height = actualH * dpr;
  c.style.width = W + 'px'; c.style.height = actualH + 'px';
  const ctx = c.getContext('2d'); ctx.scale(dpr, dpr);
  return { ctx, W, H: actualH };
}

/* drawGrid(ctx, W, H, xMin, xMax, yMin, yMax, opt)
   opt.achsenLabels === false  →  die generischen Labels „x"/„y" werden NICHT
   gezeichnet. Das ist der richtige Weg für Anwendungsgraphen, die eigene
   Achsenbeschriftungen mit Einheit schreiben („x [kg]", „K [CHF]"). Früher
   wurden die generischen Labels mit fillRect übermalt; die festen Pixelwerte
   trafen den Buchstaben aber nicht in jeder Skalierung und liessen einen
   Strichrest stehen.
   opt.zahlen === false  →  keine Zahlenteilung. Für Seiten mit eigener Teilung
   (z.B. „alle 2 kg"): sonst liegen zwei Zahlenreihen übereinander. */
function drawGrid(ctx, W, H, xMin, xMax, yMin, yMax, opt) {
  opt = opt || {};
  const cx = x => (x - xMin) / (xMax - xMin) * W;
  const cy = y => H - (y - yMin) / (yMax - yMin) * H;
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
  // Vertikale Gitterlinien
  for (let gx = Math.ceil(xMin); gx <= Math.floor(xMax); gx++) {
    ctx.strokeStyle = gx === 0 ? '#b8c4d4' : '#eff1f5';
    ctx.lineWidth = gx === 0 ? 1.5 : 1;
    ctx.beginPath(); ctx.moveTo(cx(gx), 0); ctx.lineTo(cx(gx), H); ctx.stroke();
  }
  // Horizontale Gitterlinien
  for (let gy = Math.ceil(yMin); gy <= Math.floor(yMax); gy++) {
    ctx.strokeStyle = gy === 0 ? '#b8c4d4' : '#eff1f5';
    ctx.lineWidth = gy === 0 ? 1.5 : 1;
    ctx.beginPath(); ctx.moveTo(0, cy(gy)); ctx.lineTo(W, cy(gy)); ctx.stroke();
  }
  // Achsen
  ctx.strokeStyle = '#374151'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(0, cy(0));   ctx.lineTo(W, cy(0));   ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx(0), 0);   ctx.lineTo(cx(0), H);   ctx.stroke();
  // Achsen-Pfeile
  ctx.fillStyle = '#374151';
  ctx.beginPath(); ctx.moveTo(W - 8, cy(0) - 4); ctx.lineTo(W, cy(0));   ctx.lineTo(W - 8, cy(0) + 4); ctx.fill();
  ctx.beginPath(); ctx.moveTo(cx(0) - 4, 8);     ctx.lineTo(cx(0), 0);   ctx.lineTo(cx(0) + 4, 8);     ctx.fill();
  // Zahlen-Labels. Die Seite der Achse wird bestimmt, nicht angenommen: bei
  // Anwendungsgraphen mit xMin=0 / yMin=0 liegt der Nullpunkt am Canvasrand,
  // dort landeten die Zahlen früher ausserhalb der Zeichenfläche und fehlten
  // ersatzlos. Freistellung, weil sie innen auf Gitter und Kurven treffen.
  const unten = cy(0) + 14 <= H - 3;      // Platz unterhalb der x-Achse?
  const links = cx(0) - 5 >= 22;          // Platz links der y-Achse?
  // Als Funktion, damit eine Seite die Zahlen nach den Kurven noch einmal
  // obenauf setzen kann (zahlenOben()) — sonst kreuzt eine Kurve sie.
  // Schrittweite der Zahlenteilung aus dem verfügbaren Platz bestimmen, nicht
  // fest annehmen: bei weiten Bereichen (z.B. −28…28 auf 460 px) verschmolzen
  // die Zahlen sonst zu einem unlesbaren Band. 1-2-5-10-Folge wie üblich.
  function schritt(spanne, pixel, mindest) {
    const proEinheit = pixel / spanne;
    if (proEinheit >= mindest) return 1;
    for (let z = 1; z <= 1e6; z *= 10) {
      for (const m of [1, 2, 5]) {
        if (z * m * proEinheit >= mindest) return z * m;
      }
    }
    return 1;
  }
  const sx = schritt(xMax - xMin, W, 26);   // 26 px reichen für bis zu 3 Zeichen
  // Auf der y-Achse bleibt es bei jeder zweiten Einheit wie bisher; eng wird
  // nur weiter, nie dichter.
  const sy = Math.max(2, schritt(yMax - yMin, H, 16));

  function zahlen() {
    const f = ctx.font, s = ctx.fillStyle;
    ctx.font = '13px JetBrains Mono,monospace'; ctx.fillStyle = '#9ca3af';
    for (let gx = Math.ceil(xMin / sx) * sx; gx < xMax; gx += sx) {
      if (gx === 0 || gx <= xMin) continue;
      beschriftung(ctx, gx, cx(gx), unten ? cy(0) + 14 : cy(0) - 6, { align: 'center', bg: '#fff', W, H });
    }
    for (let gy = Math.ceil(yMin / sy) * sy; gy < yMax; gy += sy) {
      if (gy === 0 || gy <= yMin) continue;
      beschriftung(ctx, gy, links ? cx(0) - 5 : cx(0) + 5, cy(gy) + 4,
                   { align: links ? 'right' : 'left', bg: '#fff', W, H });
    }
    ctx.font = f; ctx.fillStyle = s;
  }
  if (opt.zahlen !== false) zahlen();
  // Achsen-Labels (generisch). Seiten mit eigener Beschriftung samt Einheit
  // unterdrücken sie über opt.achsenLabels === false.
  if (opt.achsenLabels !== false) {
    ctx.fillStyle = '#374151'; ctx.font = 'bold 13px monospace';
    beschriftung(ctx, 'x', W - 14, cy(0) - 7, { align: 'left', bg: '#fff', W, H });
    beschriftung(ctx, 'y', cx(0) + 13, 14, { align: 'center', bg: '#fff', W, H });
  }
  return { cx, cy, zahlenOben: zahlen };
}

function drawLine(ctx, cx, cy, m, b, xMin, xMax, color, lw) {
  ctx.strokeStyle = color; ctx.lineWidth = lw || 2.5; ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(cx(xMin), cy(m * xMin + b));
  ctx.lineTo(cx(xMax), cy(m * xMax + b));
  ctx.stroke();
}

function drawDot(ctx, cx, cy, x, y, color, r) {
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(cx(x), cy(y), r || 6, 0, Math.PI * 2); ctx.fill();
}

/* ── Lösungs-Toggle ──────────────────────────────────────── */
function toggleL(id) {
  const b = document.getElementById(id);
  const btn = b.previousElementSibling;
  const o = b.classList.toggle('sichtbar');
  btn.textContent = o ? '▼ Lösung verbergen' : '▶ Lösung';
}

/* ── MathJax: serialisiertes, Startup-gegateetes Typesetting ───────────────────
   Zentraler Ersatz für direkte MathJax.typesetPromise(...)-Aufrufe. Behebt zwei
   Races, die einzelne Formeln sporadisch leer rendern liessen (vor allem beim
   Hard-Refresh, nicht beim Zurückblättern aus dem bfcache):
     1) eigene Typeset-Aufrufe beim Laden, die mit MathJax' initialem Render der
        ganzen Seite kollidieren  → die erste Queue-Stufe wartet auf
        MathJax.startup.promise, läuft also erst NACH dem Initial-Render;
     2) sich überlappende Re-Typesets auf denselben Elementen (verstärkt durch
        svg.fontCache:'global')  → alle Aufrufe werden seriell verkettet, ein
        neuer startet erst, wenn der vorige fertig ist.
   Aufruf:  mjTypeset([el, ...])   bzw.   mjTypeset()  für die ganze Seite.
   Gibt das Promise des Durchlaufs zurück (für optionales .then()/await). */
let _mjTypesetQueue = null;
function mjTypeset(els) {
  if (!(window.MathJax && MathJax.typesetPromise)) return Promise.resolve();
  if (!_mjTypesetQueue) {
    _mjTypesetQueue = (MathJax.startup && MathJax.startup.promise) || Promise.resolve();
  }
  _mjTypesetQueue = _mjTypesetQueue
    .then(() => MathJax.typesetPromise(els))
    .catch(err => console.error('mjTypeset:', err));
  return _mjTypesetQueue;
}
