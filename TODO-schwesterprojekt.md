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

## Startseite: Lektionsangabe unter den Titel (TALS Mathe, 2026-07-30) — für Physik empfohlen

**Was in Mathe gemacht wurde** (`index.html`, eigener `<style>`-Block — nicht `style.css`):
drei Änderungen an der Startseite. Für Physik ist **eine davon** relevant, die zwei
anderen entfallen. Farben spielen keine Rolle: alle drei Änderungen sind reine
Layout-Eigenschaften, es gibt nichts von `--blau`/`--lila` auf `--bernstein*` umzustellen.

### 1. Lektionsangabe von rechts nach links unter den Titel — **portieren**

Bisher steht `.k-lek` per `margin-left: auto` am rechten Zeilenende und konkurriert dort
mit dem Titel um die Breite. Neu sitzt sie linksbündig unter dem Titel.

**Markup** — `.k-name` und `.k-lek` in einen gemeinsamen Block packen:

```html
<div class="kap-hdr" onclick="tog('p4')">
  <span class="k-nr">4</span>
  <span class="k-txt">
    <span class="k-name">Mechanik</span>
    <span class="k-lek">100 Lektionen · 5 Teilgebiete</span>
  </span>
  <span class="k-tog" id="tg-p4">▼</span>
</div>
```

**CSS** — die Zeilenhöhe bleibt gleich, weil die Polsterung sinkt und die
`line-height`-Werte knapp gesetzt sind:

```css
.kap-hdr { padding: 9px 16px; align-items: center; gap: 10px; }   /* vorher 12px 18px */
.k-txt   { display: flex; flex-direction: column; gap: 1px; min-width: 0; flex: 1; }
.k-name  { line-height: 1.2; }
.k-lek   { margin-left: 0; font-size: 0.6rem; line-height: 1.25; white-space: normal; }

/* Die Regel aus §9 richtet .k-lek unter 600px rechts aus — richtig, solange die
   Angabe am rechten Zeilenende sitzt. Unter dem Titel muss sie mit ihm
   linksbündig sein, und align-items/padding-top von dort werden hinfällig. */
@media (max-width: 600px) {
  .kap-hdr { align-items: center; }
  .k-lek   { text-align: left; }
  .k-nr, .k-name { padding-top: 0; }
}
```

**Warum es sich in Physik besonders lohnt** — Physiks `.k-lek`-Texte sind lang
(„Sek-I-Auffrischung · 3 Seiten · kein RLP-Lerngebiet", „30 Lektionen · 2 Teilgebiete
+ 1 Vertiefung"). Gemessen am 30.07.2026 im Physik-Repo:

| Breite | Zeilenhöhen | `.k-lek` bricht um |
|---|---|---|
| 1280 px | 51 px durchgehend | 1 Zeile |
| 600 px | 52 / 52 / 52 / **78** px | bis 2 Zeilen |
| 360 px | **67** / 53 / 53 / **104** px | bis 3 Zeilen |

Bei 360 px ist die Zeile „Einführung in andere Bereiche der Physik" doppelt so hoch wie
die anderen. Unter dem Titel bekommt die Angabe die volle Zeilenbreite. In Mathe sind
die Kapitelzeilen nach dem Umbau **50 px** hoch, also 1 px flacher als vorher (51 px),
und bei 360 px bleiben 50–69 px statt vorher 53–104 px.

### 2. Bereichskopf auf ein Wort kürzen — **entfällt**

Mathe hatte zwei `.bereich`-Köpfe mit Badge + langem Titel („Mathematik —
Grundlagenbereich"), jetzt nur noch „Grundlagenfach" / „Schwerpunktfach", Polsterung
`17px 20px 15px` → `11px 18px 10px`, Kopfhöhe 65 → 51 px. **Physik hat kein `.bereich`**
(nachgesehen: 0 Vorkommen) — der Kopf wurde dort in §9 ersatzlos gelöscht. Nichts zu tun.

### 3. Bereiche nebeneinander — **nicht empfohlen**

In Mathe stehen Grundlagen- und Schwerpunktfach nebeneinander
(`.spalten { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start }`,
unter 900 px zurück auf eine Spalte). Das trägt, weil es **zwei unabhängige Fachbereiche**
mit eigener Farbe und eigener Nummerierung sind.

Physik hat **eine** flache Liste aus vier Lerngebieten (0, 4, 5, 6). Zwei Spalten hätten
dort kein Gegenstück in der Sache, sondern wären eine willkürliche 2+2-Teilung. Dazu
kommt: die vier `.kap`-Zeilen teilen sich ihren Rahmen über
`.kap:first-of-type { border-top … }` und `.kap:last-of-type { border-radius … }` — die
Regeln müssten pro Spalte neu greifen. Und der Gewinn wäre gering: Physiks Liste endet
bei 1280 px schon bei y = 404 px, steht also längst im ersten Bildschirm.
**Empfehlung: einspaltig lassen.**

**Prüfen nach dem Port:** Zeilenhöhen bei 1280 / 600 / 360 px vergleichen,
`.k-lek` linksbündig zum Titel (Versatz 0 px), `document.body.scrollWidth ===
document.documentElement.clientWidth`.
