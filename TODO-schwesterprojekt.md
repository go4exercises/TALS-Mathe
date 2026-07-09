# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

## Offen

- **2026-06-24 · MathJax-Re-Typeset serialisieren (zentraler Helfer `mjTypeset`) ·
  `physiklib.js` + alle Themenseiten · warum:** Einzelne Formeln rendern sporadisch
  leer — aber nur beim **Hard-Refresh**, nicht beim Zurückblättern aus dem bfcache.
  Ursache: seiten-eigene `MathJax.typesetPromise(…)`-Aufrufe beim Laden kollidieren
  mit MathJax' initialem Seiten-Render (Race), zusätzlich überlappen sich Re-Typesets
  auf denselben Elementen — verstärkt durch `svg.fontCache:'global'`.
  **Massnahme (in Mathe umgesetzt):**
  1. In `mathlib.js` (Physik: `physiklib.js`) den Helfer `mjTypeset(els)` ergänzen —
     serialisiert alle Durchläufe über eine Promise-Kette, deren erste Stufe auf
     `MathJax.startup.promise` wartet (läuft also nach dem Initial-Render). Code 1:1
     aus `mathlib.js` (Abschnitt „MathJax: serialisiertes … Typesetting") übernehmen,
     ist farb-/projektneutral.
  2. Alle direkten `[window.]MathJax.typesetPromise(args)`-Aufrufe (inkl. ihrer
     redundanten `if (window.MathJax && …typesetPromise)`-Guards) durch
     `mjTypeset(args)` ersetzen; `mjTypeset()` ohne Argument = ganze Seite.
     Guard-Tokens (`!MathJax.typesetPromise` in Early-Returns) bleiben unverändert.
  3. Nur bei dynamisch (per `innerHTML`) geänderter Mathematik aufrufen — statische
     HTML-Formeln rendert MathJax beim Laden selbst (kein erneutes Typeset).
  Doku-Stellen, die in Physik analog nachzuziehen sind: `TEMPLATE.html` (Helfer-Liste)
  und `HOWTO-neue-themenseite.md` (Troubleshooting „Formeln rendern sporadisch leer").
  Verifikation in Mathe: Pre-Flight-Tiefencheck `verify_mathjax` 5698 Ausdrücke / 0
  Fehler, `verify_js_runtime` ok. **Render-Check 1280/360 px steht noch aus** (kein
  Browser lokal) — in Physik vor dem Abschluss nachholen.

- **Slider-Wert-Farbkopplung (CSS-Muster, aus Audit-Paket 4).**
  Auf mehreren Seiten färbt die seiten-lokale Regel `.sl-val { color: var(--blau) }`
  **alle** Slider-Werte blau — auch die von orange/grünen Reglern (akz-orange/-gruen).
  Der Wert passt dann nicht zu Reglerfarbe und (falls vorhanden) zur farbcodierten
  Live-Formel. **Massnahme (in Mathe umgesetzt auf g3-1, s1-2, s1-3, s2-2c, s3-5):**
  je Seite zwei Regeln nachziehen —
  `.sl-grp.akz-orange .sl-val, .sl-row.akz-orange .sl-val { color: var(--orange); }`
  und analog für `.akz-gruen`. Farbneutral, kein JS. In Physik dort prüfen, wo ein
  Widget mehrere Regler mit unterschiedlichen akz-Farben hat (Amber/Bernstein-Palette
  entsprechend). Verwandt: Live-Formel-Werte via `.tx-…`-Spans an dieselben Farben koppeln.

## Erledigt / portiert

- (noch leer)
