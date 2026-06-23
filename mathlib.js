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
//  Bei Anwendungsaufgaben NACH drawGrid die generischen Achsenlabels
//  „x"/„y" mit fillRect überdecken und mit Einheit neu schreiben:
//    ctx.fillStyle='#fff';
//    ctx.fillRect(W-30, cy(0)-22, 30, 18);   // alter "x"-Bereich
//    ctx.fillRect(cx(0)+4, 0, 22, 18);       // alter "y"-Bereich
//    ctx.fillStyle='#374151'; ctx.font='bold 13px monospace';
//    ctx.textAlign='right'; ctx.fillText('x [kg]', W-2, cy(0)-7);
//    ctx.textAlign='left';  ctx.fillText('K [CHF]', cx(0)+5, 11);
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

function drawGrid(ctx, W, H, xMin, xMax, yMin, yMax) {
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
  // Zahlen-Labels (generisch — bei Anwendungen überschreiben)
  ctx.font = '13px JetBrains Mono,monospace'; ctx.fillStyle = '#9ca3af';
  ctx.textAlign = 'center';
  for (let gx = Math.ceil(xMin) + 1; gx < xMax; gx++) { if (gx !== 0) ctx.fillText(gx, cx(gx), cy(0) + 14); }
  ctx.textAlign = 'right';
  for (let gy = Math.ceil(yMin) + 1; gy < yMax; gy += 2) { if (gy !== 0) ctx.fillText(gy, cx(0) - 5, cy(gy) + 4); }
  // Achsen-Labels (generisch — bei Anwendungen überschreiben)
  ctx.fillStyle = '#374151'; ctx.font = 'bold 13px monospace';
  ctx.textAlign = 'left';   ctx.fillText('x', W - 14, cy(0) - 7);
  ctx.textAlign = 'center'; ctx.fillText('y', cx(0) + 13, 14);
  return { cx, cy };
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
