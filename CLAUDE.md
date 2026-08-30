# CLAUDE.md — TALS Mathe

Statisches HTML/CSS/JS-Lehrmittel für die BM (RLP-BM 2030), gehostet via GitHub Pages.
Schwester-Projekt zu TALS Physik. Diese Datei ist die lokale Claude-Code-Variante der
COLLABORATION.md — sie ersetzt den alten ZIP-Workflow durch einen Git-Workflow.

**Autoritative Detail-Konventionen stehen in `STYLEGUIDE.md` (im Repo). Diese Datei ist
die Kurzfassung + der verbindliche Pre-Flight. Bei Widerspruch gilt STYLEGUIDE.md.**

## Sprache & Notation (nicht verhandelbar)

- Schweizer Hochdeutsch. **Kein ß** — immer „dass", „muss", „Schluss".
- **Dezimaltrennzeichen ist der Punkt, nie das Komma** — überall: LaTeX (`9.81`, nicht
  `9{,}81`), Aufgabentexte, Live-Anzeigen, JS-Code.
- MathJax-Delimiter: `\(…\)` inline, `\[…\]` abgesetzt. Niemals `$…$`.
- Alles Mathematische in LaTeX/MathJax.

## Bereichs- & Farbsystem (STYLEGUIDE §5)

- **Bereichsfarben:** Grundlagenfach = **Blau** (`--blau`, `--blau-hell`),
  Schwerpunktfach = **Violett** (`--lila`, `--lila-hell`). Das ist die Mathe-Identität
  (Physik dagegen Bernstein/Amber).
- **Didaktische Farben — kapitelübergreifend IMMER dieselbe Bedeutung:**
  Blau = Definition/Theorie (`block-def`, 📘) · Grün = Beispiel/Lösung · Orange =
  Aufgabe/Übung (`block-aufg`) · Rot = Fehler/Achtung · Lila = Beweis/Herleitung ·
  Blau-Variante = Merksatz/Schlussfazit (`block-merksatz`, ⭐). Farben nie umdeuten.

## Projektstruktur

- `grundlagen/` — Grundlagenfach: `g1-*` … `g5-*` (23 Seiten, inkl. Sub-Splits `g2-2a/b`, `g5-2a–d`).
- `schwerpunkt/` — Schwerpunktfach: `s1-*` … `s4-*` (23 Seiten, inkl. Sub-Splits `s2-2a–c`,
  `s3-2a/b`, `s3-4a/b`, `s4-2a–c`, `s4-3a–d` und Ergänzungen `s3-6`, `s4-3d`). Alle Teilgebiete
  sind ausgebaut — es gibt keine Stubs mehr.
- `mathlib.js` — Canvas-Bibliothek + globale Helfer (`toggleL` u.a.).
- `minicheck.js` (Mini-Check-Akkordeon), `anim-hinweise.js` (👁/💡-Rollover, Pflicht bei
  interaktiven Animationen), `nav.js` (`buildNav`), `style.css`.
- `formelsammlung.html`, `glossar.html` — zwei Nachschlag-Seiten im Repo-Root.
- `schriften.css` + `schriften/` — lokal ausgelieferte Schriften (Fontsource 5.3.0,
  OFL). `vendor/mathjax/` — MathJax 3.2.2 (Apache 2.0). **Keine Seite lädt etwas von
  einem fremden Host**; Details und Fallstricke in STYLEGUIDE §5.3.1. Umgestellt wird
  mit `scripts/schriften-lokal.py` und `scripts/mathjax-lokal.py`.
- `scripts/build-seo.py` — erzeugt Seiten-Metadaten (Beschreibung, canonical, Open
  Graph, JSON-LD nach schema.org/LearningResource), `sitemap.xml` und `robots.txt`.
  Der Kopfblock zwischen `<!-- SEO:ANFANG -->` und `<!-- SEO:ENDE -->` ist
  **generiert** — gepflegt wird die Tabelle `SEITEN` im Skript. Neue Seite = dort
  eintragen, sonst fehlen ihr Beschreibung und Sitemap-Eintrag. Der Pre-Flight
  warnt, wenn die Metadaten veraltet sind.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og-bild.png` — Bild-Assets
  der Auffindbarkeit, erzeugt von `.claude/tools/build-bilder.mjs` (braucht einmalig
  Netz für die Google Fonts). Nur neu bauen, wenn Farben oder Wortlaut ändern.
- Skelett-Quelle: `TEMPLATE.html` + `HOWTO-neue-themenseite.md`.

## Inhaltliche Regeln (STYLEGUIDE §4)

- **Master-Schema je Seite vollständig:** eigener Einstieg, eigene Definition, eigene
  Aufgaben A1–A6 (optional A7 Vertiefung), eigene Zusammenfassung. **Keine Verweise auf
  die Schwesterseite** für fehlende Inhalte — jede Sub-Seite steht für sich.
- **Sub-Split-Namen:** Buchstaben-Suffix direkt an die RLP-Nummer (`g2-2a`, `g2-2b`);
  gemeinsames Numerik-Präfix, Unterschied nur im Suffix.
- Aufgaben-Markup: `aufg-nr-tag` (orange Pille, monospace), `aufg-titel-text`, optional
  `aufg-vertiefung`-Pille am Ende.
- **x-y-Skalierung aufgabenbezogen**, nicht zwingend 1:1, wenn die Achsen
  unterschiedliche Grössen/Einheiten tragen (STYLEGUIDE §… „keine 1:1-Forderung").
- Lernziele: aufklappbare „Ich kann …"-Liste direkt nach der RLP-Kompetenzen-Box,
  Blau-Familie, 4–6 Punkte.

## Skelett & Klassen — kopieren, nicht erfinden

- Neue Seite / neuer Block: Skelett aus `TEMPLATE.html` (oder einer Nachbar-Seite)
  **1:1 kopieren**, nur Inhalt anpassen. CSS und `nav.js` sind auf die *exakten*
  Klassennamen ausgerichtet.
- **Niemals eigene Klassennamen, Container-Hierarchien oder API-Signaturen erfinden.**
  Erfundene Klassen fallen still auf Block-Default zurück (Karten werden zu Listen,
  Sidebar überlappt).
- Jede Seite mit `onclick="toggleL(…)"` o.ä. **muss `mathlib.js` einbinden**. Mit
  `.anim-hinweis`-Markup → `anim-hinweise.js`. Mit `.minicheck`-Markup → `minicheck.js`.
- Slider-Farbkopplung: `akz-blau/akz-orange/akz-gruen` auf `.sl-grp`, und dieselben
  Farben in der Live-Formel via `.tx-…`-Spans bzw. `\textcolor{#1a4f8a|#b85c00|#1f6b3a}{…}`.

## Pre-Flight (verbindlich vor jedem Commit)

Nach jeder Änderung an Themenseiten, **bevor** committet wird:

```bash
python3 .claude/skills/preflight/preflight.py grundlagen/<datei>.html
# oder über alle: python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html
```

Erwartete Ausgabe: `ALLE CHECKS BESTANDEN`. Jede `[FEHLER]`-Meldung wird vor dem Commit
behoben (`[WARN]` ist kein Blocker). Zweistufig: (1) schnelle Eigen-Checks — div/details-
Bilanz, doppelte IDs, kein ß, Dezimalkomma in Body-Math, Skelett, Phantom-Klassen,
mathlib-Einbindung, Ressourcen-Marker; (2) Aufruf der vorhandenen Repo-Skripte
`verify_mathjax.js` (echte Render-Prüfung), `verify_js_runtime.js` (JS-Laufzeit) und
`check_identifier_collisions.py`. Stufe 2 braucht einmalig `npm install mathjax-full jsdom`
im Repo-Root; fehlen die Module, werden diese Checks als `[WARN]` übersprungen.
**Vom Repo-Root aufrufen.**

## Verifikations-Standard

- **Alle Zahlenwerte vor dem Einbau mit `python3` nachrechnen** — nie aus dem Gedächtnis.
- **Geometrie/Funktionsgraphen von Canvas-Animationen vorab in Python durchrechnen**
  (Stützpunkte, Schnittpunkte, Label-Positionen), bevor der Zeichencode geändert wird.
- `node --check` auf jedem Script-Block (der Pre-Flight macht das mit).
- Render-Check bei Graph-Änderungen, wenn ein Browser verfügbar ist: Playwright headless
  bei 1280 px **und** 360 px, Screenshots der Canvases sichten.
- **Keine erfundenen Quellen, Zitate oder Lehrplan-Stellen.** Im Zweifel: „muss
  verifiziert werden" schreiben, nicht raten.

## Schwesterprojekt TALS Physik — Übertrag per Todo, nicht direkt

- Claude Code editiert **nur dieses Repo**. Es fasst das Physik-Repo nicht an.
- Änderungen, die auch ins Schwesterprojekt gehören (gemeinsame CSS-Muster, didaktische
  Module, `mathlib`/`physiklib`-Helfer, Nav-Logik), werden **nicht** quer-editiert,
  sondern als Eintrag in **`TODO-schwesterprojekt.md`** vermerkt (was, wo, warum) und
  später in einer Physik-Session von Hand portiert. So bleibt jedes Repo sauber.

## Externe Ressourcen

Anbieter-Reihenfolge, Negativ-Liste und Verifikation: STYLEGUIDE / `HOWTO-externe-ressourcen.md`.
Max. Slots je Sektion und Playlist-vor-Einzelvideo dort nachschlagen. YouTube-Verifikation
per `web_fetch` auf die Playlist-URL (liefert Owner) — Präfix-Heuristik ist unzuverlässig.

## Arbeitsweise

- **Bei klarem Auftrag direkt umsetzen**, keine Rückfrage. Annahme nötig → inline kurz
  erwähnen. Bei echter Mehrdeutigkeit max. 3 gebündelte Fragen, dann starten.
- **Keine ungebetene Verbesserungs-Initiative.** Was nicht Teil des Auftrags ist, wird
  nicht mit-gepatcht. Kein Refactoring „weil eleganter".
- Mehr als 3 gleichartige Edits → ein Skript (`sed`/`python`), nicht N Einzel-Edits.
- Vor gezielten Edits `grep -n` + enger `view`, um Whitespace/Sonderzeichen exakt zu treffen.

## Automatik: Diffs nicht bestätigen + Commit nach jedem Durchgang

Dieses Repo läuft im Modus `acceptEdits` (siehe `.claude/settings.json`): Datei-Edits
werden ohne einzelne Diff-Bestätigung übernommen. Das Sicherheitsnetz ist Git — darum:

**Nach jedem abgeschlossenen Auftrag (= ein „Durchgang") automatisch, ohne Rückfrage:**

1. Pre-Flight über die geänderten Seiten laufen lassen.
2. **Nur wenn `ALLE CHECKS BESTANDEN`:** `git add -A` und `git commit` mit aussagekräftiger
   Message (Seite + was geändert wurde).
3. Schlägt der Pre-Flight fehl: **nicht committen**, Fehler melden und beheben, dann 1.
4. **Niemals `git push`.** Der Push bleibt manuell beim Auftraggeber.

## Was die Sandbox-Werkstatt (Chat) übernimmt

Abgeleitete Artefakte mit Spezial-Werkzeug bleiben besser im Chat, falls lokal nicht
installiert: **Anki-APKG-Rebuilds** (ZIP+SQLite — lokal ok, wenn Python steht),
**xlsx-Recalc** (braucht LibreOffice), **docx-Generierung** (braucht docx-Skill/Libs).
Inhalts-Edit lokal machen, abgeleitetes Artefakt danach regenerieren.
