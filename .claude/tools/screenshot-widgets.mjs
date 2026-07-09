// screenshot-widgets.mjs — Browser-Rendercheck der Audit-Paket-5-Widgets (T52).
//
// Voraussetzung (einmalig, vom Repo-Root):
//   npm install -D playwright        # holt das Playwright-Paket
//   npx playwright install chromium  # holt den Chromium-Build
//
// Aufruf (vom Repo-Root):
//   node .claude/tools/screenshot-widgets.mjs
//
// Ergebnis: je Widget zwei PNGs (1280 px Desktop + 360 px Mobil) im Ordner
// widget-shots/ — Dateinamen mit Praefix "check_" (via .gitignore ausgeschlossen).
// Zusaetzlich prueft das Skript, ob jedes Canvas tatsaechlich gezeichnet wurde
// (nicht komplett weiss) — ein leeres Canvas verraet einen stillen JS-Fehler.

import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

// Die zehn Prio-1-Widgets aus §4 (Runde 1 [89] + Runde 2 [90]).
const WIDGETS = [
  { page: 'grundlagen/g2-2b-quadratische-gleichungen.html', id: 'cv-pk-parabel', note: 'Diskriminanten-Parabel' },
  { page: 'grundlagen/g5-3-trigonometrische-berechnungen.html', id: 'cv-ssw', note: 'SSW-Fallunterscheidung' },
  { page: 'grundlagen/g4-3-masszahlen.html', id: 'cv-robust', note: 'Robustheits-Widget' },
  { page: 'schwerpunkt/s3-5-trigonometrische-funktionen.html', id: 'cv-phasor', note: 'Phasor' },
  { page: 'schwerpunkt/s3-3-polynomfunktionen.html', id: 'cv-lt', note: 'Leitterm-Zoom' },
  { page: 'grundlagen/g5-4-einheitskreis.html', id: 'cv-abw', note: 'Abwickler' },
  { page: 'schwerpunkt/s2-1-grundlagen.html', id: 'cv-sl', note: 'Scheinloesungs-Grafik' },
  { page: 'schwerpunkt/s4-3c-geraden.html', id: 'cv-lot', note: 'Lot-Widget' },
  { page: 'schwerpunkt/s4-2b-pyramiden-kegel-stuempfe.html', id: 'cv-k3', note: 'k-hoch-3-Slider' },
  { page: 'schwerpunkt/s4-3d-ebenen.html', id: 'cv-haus', note: 'Pultdach-Schraegbild' },
  // T53 (Prio-2), Runde 1: die aus T52 verschobenen Sekundaer-Widgets.
  { page: 'schwerpunkt/s4-2c-kugel.html', id: 'cv-kugelteil', note: 'Kugelteil-Querschnitt' },
];

const VIEWPORTS = [
  { tag: '1280', width: 1280, height: 1400 },
  { tag: '360', width: 360, height: 1400 },
];

const OUT = 'widget-shots';
const REPO = process.cwd();

// Ist das Canvas nicht komplett einfarbig (also wirklich gezeichnet)?
async function canvasGezeichnet(page, id) {
  return page.evaluate((cid) => {
    const cv = document.getElementById(cid);
    if (!cv || !cv.width || !cv.height) return { ok: false, grund: 'kein Canvas / Groesse 0' };
    const ctx = cv.getContext('2d');
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    const r0 = d[0], g0 = d[1], b0 = d[2];
    for (let i = 4; i < d.length; i += 4) {
      if (d[i] !== r0 || d[i + 1] !== g0 || d[i + 2] !== b0) return { ok: true };
    }
    return { ok: false, grund: 'Canvas komplett einfarbig (leer)' };
  }, id);
}

const browser = await chromium.launch();
await mkdir(OUT, { recursive: true });

let fehler = 0;
for (const vp of VIEWPORTS) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  for (const w of WIDGETS) {
    const url = pathToFileURL(resolve(REPO, w.page)).href;
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 20000 });
      await page.waitForSelector('#' + w.id, { timeout: 10000 });
      await page.waitForTimeout(600); // MathJax-CDN + draw-on-load abwarten
      const status = await canvasGezeichnet(page, w.id);
      const el = await page.$('#' + w.id);
      await el.scrollIntoViewIfNeeded();
      const file = `${OUT}/check_${w.id}_${vp.tag}.png`;
      await el.screenshot({ path: file });
      if (status.ok) {
        console.log(`  ok   ${vp.tag}px  ${w.id.padEnd(14)} ${w.note}  ->  ${file}`);
      } else {
        fehler++;
        console.log(`  LEER ${vp.tag}px  ${w.id.padEnd(14)} ${w.note}  (${status.grund})  ->  ${file}`);
      }
    } catch (e) {
      fehler++;
      console.log(`  FAIL ${vp.tag}px  ${w.id.padEnd(14)} ${w.note}  (${e.message.split('\n')[0]})`);
    }
  }
  await ctx.close();
}
await browser.close();

console.log(`\nFertig. ${WIDGETS.length} Widgets x ${VIEWPORTS.length} Viewports.` +
  (fehler ? `  ${fehler} Auffaelligkeit(en) oben pruefen.` : `  Alle Canvases gezeichnet.`));
process.exit(fehler ? 1 : 0);
