// Wird per addInitScript VOR allen Seitenskripten ausgeführt.
// Protokolliert jeden Text-Aufruf auf einem 2D-Canvas mitsamt Pixel-Befund:
//   - welche Grafik-Pixel liegen UNTER den Glyphen (Label steht auf einer Linie/Fläche)?
//   - welche Glyphen-Pixel werden SPÄTER überzeichnet?
//   - liegt das Textfeld ausserhalb des Canvas (abgeschnitten)?
// Erfasst wird nur der ERSTE Zeichendurchgang je Canvas — die Startposition.
(() => {
  const P = CanvasRenderingContext2D.prototype;
  const o = {
    fillText: P.fillText, strokeText: P.strokeText,
    save: P.save, restore: P.restore,
    translate: P.translate, scale: P.scale, rotate: P.rotate,
    transform: P.transform, setTransform: P.setTransform, resetTransform: P.resetTransform,
    clearRect: P.clearRect, fillRect: P.fillRect,
  };

  window.__AUDIT = { canvases: {}, fehler: [] };

  // ── eigene Transformationsverwaltung (a,b,c,d,e,f) ──────────
  const M = new WeakMap();          // ctx -> {m:[...], stack:[...]}
  function st(ctx) {
    if (!M.has(ctx)) M.set(ctx, { m: [1, 0, 0, 1, 0, 0], stack: [] });
    return M.get(ctx);
  }
  const mul = (A, B) => [
    A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1],
    A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3],
    A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5],
  ];
  const pt = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];

  P.save = function () { const s = st(this); s.stack.push(s.m.slice()); return o.save.call(this); };
  P.restore = function () { const s = st(this); if (s.stack.length) s.m = s.stack.pop(); return o.restore.call(this); };
  P.translate = function (x, y) { const s = st(this); s.m = mul(s.m, [1, 0, 0, 1, x, y]); return o.translate.call(this, x, y); };
  P.scale = function (x, y) { const s = st(this); s.m = mul(s.m, [x, 0, 0, y, 0, 0]); return o.scale.call(this, x, y); };
  P.rotate = function (a) { const s = st(this); s.m = mul(s.m, [Math.cos(a), Math.sin(a), -Math.sin(a), Math.cos(a), 0, 0]); return o.rotate.call(this, a); };
  P.transform = function (a, b, c, d, e, f) { const s = st(this); s.m = mul(s.m, [a, b, c, d, e, f]); return o.transform.call(this, a, b, c, d, e, f); };
  P.setTransform = function (a, b, c, d, e, f) {
    const s = st(this);
    s.m = (a && typeof a === 'object') ? [a.a, a.b, a.c, a.d, a.e, a.f] : [a, b, c, d, e, f];
    return o.setTransform.apply(this, arguments);
  };
  P.resetTransform = function () { st(this).m = [1, 0, 0, 1, 0, 0]; return o.resetTransform.call(this); };

  // ── Frame-Erkennung: ein grossflächiges clearRect/fillRect beginnt ein Bild ──
  function eintrag(cv) {
    const id = cv.id || ('ohne-id-' + (cv.__auditNr || (cv.__auditNr = Math.random().toString(36).slice(2, 7))));
    if (!window.__AUDIT.canvases[id]) {
      window.__AUDIT.canvases[id] = { id, w: cv.width, h: cv.height, frame: 0, textStand: 0, texte: [] };
    }
    return window.__AUDIT.canvases[id];
  }
  function neuerFrame(ctx, w, h) {
    const cv = ctx.canvas;
    const s = st(ctx);
    const [x0, y0] = pt(s.m, 0, 0);
    const [x1, y1] = pt(s.m, w, h);
    const flaeche = Math.abs((x1 - x0) * (y1 - y0));
    if (flaeche < 0.6 * cv.width * cv.height) return;
    eintrag(cv).frame++;
  }
  P.clearRect = function (x, y, w, h) { neuerFrame(this, w, h); return o.clearRect.call(this, x, y, w, h); };
  P.fillRect = function (x, y, w, h) { neuerFrame(this, w, h); return o.fillRect.call(this, x, y, w, h); };

  // ── Textaufrufe protokollieren ──────────────────────────────
  function messen(ctx, txt, x, y) {
    const m = ctx.measureText(txt);
    const l = m.actualBoundingBoxLeft, r = m.actualBoundingBoxRight;
    const a = m.actualBoundingBoxAscent, d = m.actualBoundingBoxDescent;
    if ([l, r, a, d].some(v => typeof v !== 'number' || !isFinite(v))) return null;
    const ecken = [[x - l, y - a], [x + r, y - a], [x + r, y + d], [x - l, y + d]]
      .map(([px, py]) => pt(st(ctx).m, px, py));
    const xs = ecken.map(p => p[0]), ys = ecken.map(p => p[1]);
    return { x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys) };
  }

  function daten(ctx, b) {
    const cv = ctx.canvas;
    const x = Math.max(0, Math.floor(b.x0) - 1), y = Math.max(0, Math.floor(b.y0) - 1);
    const w = Math.min(cv.width - x, Math.ceil(b.x1 - b.x0) + 3);
    const h = Math.min(cv.height - y, Math.ceil(b.y1 - b.y0) + 3);
    if (w <= 0 || h <= 0) return null;
    const alt = ctx.getTransform ? ctx.getTransform() : null;
    o.setTransform.call(ctx, 1, 0, 0, 1, 0, 0);           // getImageData ist transformfrei, aber sicher ist sicher
    let d = null;
    try { d = ctx.getImageData(x, y, w, h); } catch (e) { window.__AUDIT.fehler.push(String(e)); }
    if (alt) o.setTransform.call(ctx, alt);
    return d ? { x, y, w, h, px: d.data } : null;
  }

  function textAufruf(orig) {
    return function (txt, x, y, maxW) {
      const cv = this.canvas;
      const e = eintrag(cv);
      // Achtung: fillText nimmt auch Zahlen (Tick-Beschriftungen werden im Repo
      // als Zahl uebergeben) — vor der Pruefung in Text wandeln, sonst fehlen
      // saemtliche Achsen-Zahlen im Protokoll.
      const s = (txt === null || txt === undefined) ? '' : String(txt);
      // Obergrenze als Reissleine fuer Endlos-Animationen.
      if (!s.trim() || e.texte.length > 600) {
        return maxW === undefined ? orig.call(this, txt, x, y) : orig.call(this, txt, x, y, maxW);
      }
      const b = messen(this, s, x, y);
      if (!b) return maxW === undefined ? orig.call(this, txt, x, y) : orig.call(this, txt, x, y, maxW);

      const vor = daten(this, b);
      const r = maxW === undefined ? orig.call(this, txt, x, y) : orig.call(this, txt, x, y, maxW);
      const nach = vor ? daten(this, b) : null;

      e.texte.push({
        txt: s, font: this.font, align: this.textAlign, baseline: this.textBaseline,
        frame: Math.max(1, e.frame),
        b, vor: vor, nach: nach ? nach.px : null,
        cvW: cv.width, cvH: cv.height,
      });
      return r;
    };
  }
  P.fillText = textAufruf(o.fillText);
  // strokeText NICHT protokollieren: es ist die Halo-Kontur von beschriftung()
  // in mathlib.js und liegt deckungsgleich unter dem fillText desselben Textes.
  // Als eigene Beschriftung gezaehlt ergaebe jede Freistellung ein Phantom-Paar.
  // (Geprueft: keine Themenseite ruft strokeText selbst auf.)

  // ── Auswertung, vom Treiber aufgerufen ──────────────────────
  window.__auditAuswerten = function () {
    const raus = [];
    for (const id of Object.keys(window.__AUDIT.canvases)) {
      const c = window.__AUDIT.canvases[id];
      const cv = document.getElementById(id);
      const ctx = cv && cv.getContext ? cv.getContext('2d') : null;
      const texte = [];
      const letzterFrame = c.texte.reduce((m, t) => Math.max(m, t.frame || 1), 1);

      for (const t of c.texte) {
        if ((t.frame || 1) !== letzterFrame) continue;
        if (!t.vor || !t.nach) { texte.push({ txt: t.txt, b: t.b, unlesbar: true }); continue; }
        const { x, y, w, h, px: vor } = t.vor;
        const nach = t.nach;

        // Hintergrundfarbe = häufigste Farbe im Feld VOR dem Text
        const zaehler = new Map();
        for (let i = 0; i < vor.length; i += 4) {
          const k = (vor[i] >> 3) + ',' + (vor[i + 1] >> 3) + ',' + (vor[i + 2] >> 3) + ',' + (vor[i + 3] >> 5);
          zaehler.set(k, (zaehler.get(k) || 0) + 1);
        }
        let bg = null, max = -1;
        for (const [k, n] of zaehler) if (n > max) { max = n; bg = k.split(',').map(Number); }
        const istBg = i => Math.abs((vor[i] >> 3) - bg[0]) <= 1 && Math.abs((vor[i + 1] >> 3) - bg[1]) <= 1 &&
                           Math.abs((vor[i + 2] >> 3) - bg[2]) <= 1 && Math.abs((vor[i + 3] >> 5) - bg[3]) <= 0;

        // Glyphenpixel = vor→nach verändert
        let glyph = 0, glyphAufGrafik = 0, grafikImFeld = 0;
        const glyphIdx = [];
        for (let i = 0; i < vor.length; i += 4) {
          const anders = Math.abs(vor[i] - nach[i]) > 12 || Math.abs(vor[i + 1] - nach[i + 1]) > 12 ||
                         Math.abs(vor[i + 2] - nach[i + 2]) > 12 || Math.abs(vor[i + 3] - nach[i + 3]) > 12;
          const grafik = !istBg(i);
          if (grafik) grafikImFeld++;
          if (anders) { glyph++; glyphIdx.push(i); if (grafik) glyphAufGrafik++; }
        }

        // später überzeichnet? Feld am Ende erneut lesen und mit „nach" vergleichen
        let ueberzeichnet = 0;
        if (ctx && glyph) {
          try {
            const jetzt = ctx.getImageData(x, y, w, h).data;
            for (const i of glyphIdx) {
              if (Math.abs(jetzt[i] - nach[i]) > 12 || Math.abs(jetzt[i + 1] - nach[i + 1]) > 12 ||
                  Math.abs(jetzt[i + 2] - nach[i + 2]) > 12 || Math.abs(jetzt[i + 3] - nach[i + 3]) > 12) ueberzeichnet++;
            }
          } catch (e) { /* egal */ }
        }

        const px = w * h;
        texte.push({
          txt: t.txt, font: t.font, b: t.b,
          glyph, glyphPx: px,
          aufGrafik: glyph ? glyphAufGrafik / glyph : 0,      // Anteil Glyphenpixel auf Grafik
          grafikDichte: px ? grafikImFeld / px : 0,           // Grafikanteil im Textfeld
          ueberzeichnet: glyph ? ueberzeichnet / glyph : 0,   // Anteil später überzeichnet
          raus: {
            links: Math.max(0, -t.b.x0), oben: Math.max(0, -t.b.y0),
            rechts: Math.max(0, t.b.x1 - t.cvW), unten: Math.max(0, t.b.y1 - t.cvH),
          },
        });
      }
      raus.push({ id, w: c.w, h: c.h, frames: c.frame, letzterFrame,
                  texteGesamt: c.texte.length, texte });
    }
    return { canvases: raus, fehler: window.__AUDIT.fehler.slice(0, 5) };
  };
})();
