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
  Fehler, `verify_js_runtime` ok. Render-Check 1280/360 px ist in Mathe seither
  laufend erfolgt (Playwright lokal, `npm run shots`); in Physik vor dem Abschluss
  analog nachholen.

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

## Mobile-Overflow-Fix (TALS Mathe [97], 2026-07-10) — auch für Physik prüfen

**Was:** Auf 360 px war `body.scrollWidth` auf fast allen Seiten grösser als der Viewport.
**Wo:** `style.css` (Ende) + `.page-wrap`/`.anim-layout`-Media-Queries.
**Warum:** Drei Ursachen, die in TALS Physik sehr wahrscheinlich identisch vorliegen:

1. `mjx-assistive-mml` (MathJax-Screenreader-Kopie, `position:absolute`) zählt zur Scrollbreite.
   Gegenregel braucht `body mjx-assistive-mml { width:1px !important; … }` — MathJax setzt selbst
   `width:100% !important` und injiziert sein CSS nach `style.css`.
2. Grid-Tracks `1fr` (= `minmax(auto,1fr)`) übernehmen die min-content-Breite des Canvas
   (dessen `width`-Attribut die Canvas-Helfer auf Buffer-Pixel setzen) → `minmax(0,1fr)`.
3. Tabellen/Canvas/Formeln brauchen `max-width:100%` bzw. eigenen horizontalen Scroll.
   Achtung: seitenlokale Tabellenklassen mit `overflow:hidden` würden sonst Inhalt abschneiden.

**Prüfbefehl** (Playwright, 360 px): `document.body.scrollWidth` gegen `clientWidth` je Seite;
zusätzlich prüfen, dass keine Tabelle `scrollWidth > clientWidth` bei `overflow-x: hidden` hat.

## TEMPLATE.html: relative Footer-Links (Rückmeldung aus dem §§6–10-Port, 2026-07-29)

**Was:** In `tals-physik/TEMPLATE.html` zeigt der neue Footer auf `feedback.html` und
`rechtliches.html` **ohne** `../`.

**Warum das nicht stimmt:** Die Vorlage ist das Skelett für Themenseiten in `themen/`
und bindet konsequenterweise selbst `../nav.js` und `../style.css` ein. Wer sie kopiert,
erbt zwei Footer-Links, die von `themen/` aus ins Leere zeigen (`themen/feedback.html`).

**Massnahme in Physik:** Im Footer von `TEMPLATE.html` auf `../feedback.html` und
`../rechtliches.html` ändern — die 14 bestehenden Themenseiten sind korrekt, nur die
Vorlage nicht. In Mathe ist das beim Port bereits so gesetzt.
