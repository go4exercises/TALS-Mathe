# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

## Offen

> **Empfohlene Reihenfolge für eine Physik-Portiersitzung** (die Einträge stehen
> darunter neuestes zuerst, die Abhängigkeiten laufen aber andersherum):
> 1. **`.widget` zentralisieren** — Fundament; ohne das greift die Einbettungsregel nicht.
> 2. **Einbettung vereinheitlichen** nach demselben Verfahren (Klasse als Namensraum
>    behalten, Karten-Optik abgeben, in `.widget` wickeln). `.anim` NICHT entfernen.
> 3. **Gedankenstrich vor Formeln in Titeln** — unabhängig, rein textlich, schnell.
> 4. **Intervallgrenzen als Klammer** — braucht den Helfer in `physiklib.js`.
> 5. **SEO-Generator nachbessern** (`tex_weg`) — unabhängig, betrifft nur Metadaten.
> 6. **`mjTypeset`** — der älteste Eintrag, unabhängig von allem oberen.
>
> Für jeden Punkt gilt: nach dem Umbau im Browser nachmessen, nicht nur den Pre-Flight
> laufen lassen. Der Pre-Flight prüft Struktur, JS und MathJax — eine still entkleidete
> Bedienspalte besteht alle Checks.

- **2026-08-30 · Drittanbieter entfernen: Schriften und MathJax lokal ausliefern ·
  alle Physik-Seiten + `apex-startseite`-Pendant · warum:** In Mathe geht seit dem
  30.8.2026 keine Anfrage mehr aus dem Haus. Physik hat exakt dasselbe Muster —
  `fonts.googleapis.com` im Kopf jeder Seite und `cdn.jsdelivr.net/npm/mathjax@3` auf
  jeder Themenseite — und denselben Fussbereich, der „Keine Cookies · Kein Tracking"
  verspricht. Solange das CDN drinsteht, stimmt die Aussage dort nicht.
  **Massnahme in Physik:** die beiden Skripte `scripts/schriften-lokal.py` und
  `scripts/mathjax-lokal.py` aus Mathe übernehmen (sie sind repo-agnostisch, sie
  leiten die Wurzel aus dem eigenen Pfad ab), dazu den Ordner `schriften/` und
  `vendor/mathjax/`. Vier Punkte, an denen es in Mathe geklemmt hätte:
  1. **Griechisch mitnehmen.** Fontsource liefert latin/latin-ext getrennt vom
     Greek-Subset. In Physik steht ausserhalb von MathJax noch mehr Griechisch als in
     Mathe (ω, λ, ρ, μ, Ω in Canvas- und SVG-Beschriftungen), sonst fällt das auf eine
     Systemschrift zurück. Vorher einmal zählen, wie in Mathe geschehen.
  2. **`boldsymbol` mitkopieren.** Wenn die Physik-Seiten ebenfalls
     `loader: { load:['[tex]/boldsymbol'] }` setzen, muss
     `vendor/mathjax/input/tex/extensions/boldsymbol.js` daneben liegen — MathJax lädt
     Erweiterungen relativ zum Pfad der Startdatei nach, sonst bricht der Formelsatz
     dort, wo `\boldsymbol` steht.
  3. **Die Datenschutzseite nachziehen.** In Mathe nennt `rechtliches.html` die beiden
     Anbieter ausdrücklich beim Namen; nach der Umstellung ist der Absatz falsch. Dazu
     ein Abschnitt „Verwendete Fremdsoftware" mit OFL und Apache 2.0.
  4. **Eigenständige Ordner ausnehmen.** In Mathe ist das `apex-startseite/`, das aus
     einem eigenen Repo ausgeliefert wird und darum eine eigene Schriftkopie trägt.
     Falls Physik so etwas hat, im Skript ausschliessen.
  Absicherung: der Mathe-Pre-Flight hat neu `check_keine_fremdhosts` — ein
  wiedereingeschleppter CDN-Aufruf ist ein `[FEHLER]`. Denselben Check in den
  Physik-Pre-Flight übernehmen, sonst kommt es beim nächsten Kopieren einer alten
  Vorlage zurück. Umfang in Mathe zum Vergleich: 233 Dateien Schriften, 230 Dateien
  MathJax, Repo +4 MB, ausgeliefert gleich viel wie vorher.

- **2026-08-10 · Umzug auf `physik.begreifbar.ch` · ganzes Physik-Repo · warum:**
  Mathe liegt seit dem 10.8.2026 auf `mathe.begreifbar.ch`. Die DNS-Seite ist für
  Physik **bereits erledigt**: `physik` steht als CNAME auf `go4exercises.github.io.`
  (TTL 300), und die Domain ist auf GitHub verifiziert — der TXT-Record
  `_github-pages-challenge-go4exercises` deckt die Subdomains mit ab. Es fehlt nur
  noch die Repo-Seite. **Bis dahin zeigen die drei Physik-Querlinks aus Mathe
  (`nav.js`) sowie die Verweise in Mathes `glossar.html` und `formelsammlung.html`
  auf eine Adresse, die noch nicht ausliefert.**
  **Massnahme in Physik:** `CNAME` im Repo-Root mit `physik.begreifbar.ch` (eine
  Zeile, LF, kein BOM), pushen, Settings → Pages prüfen, **Enforce HTTPS** setzen.
  Danach die Basis-URL im dortigen SEO-Skript umstellen und den Generator laufen
  lassen, die Rück-Querlinks auf `https://mathe.begreifbar.ch/` setzen (Kopfzeile,
  Mobilmenü, Über-Panel, Glossar, Formelsammlung) und die Namensnennung im
  Lizenzblock nachziehen. Reihenfolge und Begründung stehen in Mathes
  `DOMAIN-UMZUG.md`, Phase 5.
  **Prüfen nach dem Port:** `https://physik.begreifbar.ch/` liefert über HTTPS aus,
  `canonical` zeigt auf die neue Domain, `sitemap.xml` erreichbar, und die
  Querlinks in **beide** Richtungen landen auf einer Seite statt auf einem 404.

- **2026-08-10 · ToC markiert den aktiven Abschnitt sofort · `nav.js`,
  `buildToC()` · warum:** Die Markierung lief allein über einen
  `IntersectionObserver` mit `rootMargin: '-20% 0px -70% 0px'`. Der meldet nur,
  wenn eine Überschrift dieses schmale Band durchquert — beim Laden, nach einer
  Sprungmarke und nach schnellem Scrollen blieb im ToC darum gar nichts markiert.
  In Physik steht dieselbe Konstruktion (gleicher `rootMargin`), der Fehler ist
  also derselbe.
  **Massnahme in Physik:** Observer ersetzen durch `markiereTocAktiv()` — die
  letzte Überschrift, deren `getBoundingClientRect().top` unter 30 % der
  Fensterhöhe liegt, sonst die erste — und diese Funktion am Ende von
  `buildToC()`, bei `scroll` (auf `requestAnimationFrame` gedrosselt) und bei
  `hashchange` aufrufen. Die Horcher vor dem Binden je einmal abmelden, damit ein
  zweiter `buildToC()`-Aufruf sie nicht doppelt registriert. Die bestehende
  Klick-Markierung auf den `.toc-link` bleibt unverändert.
  **Prüfen nach dem Port:** beim Laden ist ein Eintrag markiert; Sprung auf einen
  Anker markiert dessen Abschnitt; beim Rollen wandert die Markierung lückenlos
  durch alle Überschriften. Seiten ohne ToC (Startseite) dürfen nicht brechen.

- **2026-08-03 · Animations-Karte `.widget` zentralisieren und Einbettung
  vereinheitlichen · `style.css` + Themenseiten · warum:** In Mathe lagen
  `.widget`, `.widget-header`, `.widget-header h3/p` und `.widget-body` als
  wortgleiche Kopie in 35 von 45 Themenseiten statt in `style.css` — `TEMPLATE.html`
  benutzte die Klassen, ohne sie zu definieren. Dazu standen 26 Animationen ganz
  ohne Rahmen im Textfluss, mit einer freistehenden `.widget-titelzeile`; auf
  Seiten mit gerahmten Nachbarn fiel das als Stilbruch auf, und das Hinweispaar
  brach dort auf eine zweite Zeile um.
  **Massnahme in Physik:** prüfen, ob `.widget` dort ebenfalls lokal kopiert ist
  (`grep -c '^\.widget {' themen/*.html`), zentralisieren und die lokalen Kopien
  entfernen. Achtung auf die Kaskade: die lokale Kopie überstimmt
  `.widget-titelzeile h3 { margin:0 }`; zentral gewinnt die Titelzeilen-Regel, was
  die Kopfzeile um 3 px kürzt (richtig so). Danach freistehende Animationen in die
  Widget-Form bringen. Regel dazu in STYLEGUIDE §2.10 (Mathe).
  **Nachtrag 2026-08-03 (Mathe fertig):** Statt die Karten-Optik je Behälterklasse
  einzeln zurückzunehmen, steht in Mathe jetzt eine zentrale Regel in `style.css`:
  `.widget-body > .anim { background:none; border:0; border-radius:0; padding:0;
  margin:0; box-shadow:none; }`. Sie löst das Rahmen-im-Rahmen-Problem für alle
  `.anim`-Karten auf einmal, ohne `.anim` und seine Nachfahren-Regeln anzutasten —
  in Physik dieselbe Regel setzen, bevor die erste `.anim`-Karte gewickelt wird.
  Zweiter Fallstrick aus dem Mathe-Durchgang: liegt die Titelzeile mit dem
  Hinweispaar **in einem Panel eines Tab-Umschalters**, verschwindet das Paar beim
  Umschalten. Titelzeile über den Umschalter heben, nicht in ein Panel.

- **2026-08-03 · Gedankenstrich an Formeln in Titeln beseitigen ·
  alle Themenseiten · warum:** Gerendert klebt der Gedankenstrich an der Formel und
  liest sich als Vorzeichen — aus «Labor — \(x^2 + c\)» wird optisch
  \(-x^2 + c\). In Mathe in 75 Titeln ersetzt (h2, h3, `.anim-titel`,
  `.block-titel`, `.aufg-titel-text`), Regel in STYLEGUIDE §2.8.
  **Massnahme in Physik:** dasselbe Muster suchen und ersetzen —
  `[—–]\s*\\(` in Titel-Zeilen, Ersatz `: \(`; nach `?`/`!` entfällt der
  Strich ersatzlos. **Fliesstext nicht anfassen:** dort ist der Strich ein
  Satzzeichen mit grammatischer Funktion.
  **Nachtrag 2026-08-03:** Die Regel deckte anfangs nur den Strich *vor* der Formel
  ab. Der umgekehrte Fall `\\)\s*[—–]` wirkt genauso und hängt das Minus ans
  Formelende — in Physik **beide** Muster suchen. Dort hilft kein Ersatzzeichen:
  die Tätigkeit wandert an den Anfang, die Formel ans Ende («Gerade \(f(x)=ax+b\)
  — Achsenschnitte erkunden» → «Achsenschnitte erkunden: Gerade \(f(x)=ax+b\)»).
  Ist der erste Teil nur ein Etikett (`⚠ Wichtig`, `🟢 Beispiel 2`), nicht
  umstellen, sondern Doppelpunkt. **Nur direkter Kontakt zählt:** steht zwischen
  Formel und Strich noch ein Wort, klärt es die Lesart und der Titel bleibt —
  ein weiter gefasster Suchlauf produziert Fehltreffer.

- **2026-08-02 · Intervallgrenzen am Zahlenstrahl als Klammer statt als Punkt ·
  `physiklib.js` + betroffene Themenseiten · warum:** In Mathe markieren Canvas
  eine Intervall- oder Lösungsmengengrenze neu mit derselben Klammer wie die
  Intervallschreibweise daneben (`[`, `]`) statt mit gefülltem/hohlem Punkt —
  Bild und Schreibweise sagen damit dasselbe. Neuer Helfer `intervallKlammer(ctx,
  x, y, oeffnetRechts, opt)` in `mathlib.js`, dokumentiert in STYLEGUIDE §2.7.
  Die Klammer steht immer symmetrisch zur Achse und wird weiss unterlegt; wo
  `drawGrid` Achsenzahlen setzt, gehört sie **nach** die Zahlen gezeichnet.
  **Massnahme in Physik:** Helfer 1:1 nach `physiklib.js` übernehmen (farbneutral,
  Standardfarbe `#374151`), dann die Seiten prüfen, die eine Grenze auf einer
  Achse zeichnen — in Mathe waren es drei (`g1-2 cv-iv`, `g2-1 cv-ungl`,
  `s2-2b ld-canvas`), gefunden über `.arc(` im Umfeld von «Strahl / Zahlengerade /
  Lösungsmenge / Randpunkt / Grenze».
  **Nicht umstellen**, wo es keine Intervallgrenze ist: einzelner ausgeschlossener
  Wert (Polstelle), Lösungspunkte, Wertemarken — dort bleibt der Punkt richtig.
  **Begleittexte mitziehen:** Erklärzeilen und Hinweispaare, die von «gefülltem»
  oder «hohlem Punkt» sprechen, werden sonst falsch.

- **2026-08-02 · Drei Verbesserungen am SEO-Generator zurück nach Physik ·
  `scripts/build-seo.py` · warum:** Mathe hat den Generator aus Physik (Commit
  `fc4ed40`) übernommen und dabei drei Dinge nachgebessert, die in Physik
  ebenfalls greifen würden:
  1. **`tex_weg` verstümmelt Formeln in der `teaches`-Liste.** Die alte Fassung
     löscht `^` und `_` mit weg, aus `a^x` wird «ax» und aus `\log_a(b)` wird
     «a(b)» — in Metadaten schlicht falsch. Mathe entfernt jetzt nur `{}$` und
     den Backslash und lässt `^`/`_` stehen; dazu die Makros `log`, `ln`, `lg`,
     `sin`, `cos`, `tan`, `setminus`. In Physik betrifft das u.a. die
     Kompetenzen mit Formelanteil (`v = \Delta s / \Delta t` u.ä.) — nachprüfen.
  2. **Breadcrumb vierstufig.** Mathe hat zwei Fachbereiche, deshalb
     Site → Fach → Lerngebiet → Teilgebiet. Für Physik reicht dreistufig wie
     bisher — nur übernehmen, falls dort je eine zweite Ebene dazukommt.
  3. **Bild-Assets reproduzierbar.** `.claude/tools/build-bilder.mjs` erzeugt
     `favicon-32.png`, `apple-touch-icon.png` und `og-bild.png` aus `favicon.svg`
     bzw. einer HTML-Vorlage (Playwright, Google Fonts). In Physik entstanden
     die PNGs von Hand; mit dem Skript liessen sie sich nach einer Farb- oder
     Wortlautänderung ohne Handarbeit neu bauen. Vorlage 1:1 übernehmen, nur
     Farbe (`#1a4f8a` → Bernstein) und Wortlaut tauschen.

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
