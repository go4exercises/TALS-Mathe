# Lineare Funktionen — Zusatzmaterial

Standardmaterialien für das Thema **Lineare Funktionen** (Grundlagenfach 3.2).
Reihenfolge und Datei-Naming gemäss STYLEGUIDE.md (Kapitel 4 und 6).

## Dateien

| Reihenfolge | Datei | Typ | Inhalt | Status |
|---|---|---|---|---|
| 1 | `handout.html`           | Druckseite (HTML, A4) | Theorie ohne Beispiele/Aufgaben, 9 Abschnitte | ✅ |
| 3 | `ankideck.apkg`          | Anki-Karteikarten     | Karteikarten zum Auswendiglernen | ⏳ in Arbeit |
| 4 | `teste-dich-selbst.html` | Druckseite (HTML, A4) | 12 Grundlagenaufgaben mit Lösungen | ✅ |
| 5 | `aufgabenserie.html`     | Druckseite (HTML, A4) | 10 technische Anwendungen mit Lösungen | ✅ |

Die HTML-Druckseiten öffnen sich von der Themenseite aus in einem neuen Tab und enthalten oben einen
„Seite drucken"-Knopf. Druck-CSS (`@page` + `@media print`) sorgt für saubere A4-Ausnutzung und gute
Seitenwechsel.

Bis das `ankideck.apkg` hier liegt, führt der Download-Link auf der Themenseite zu 404.

## Diagramme in den Druckseiten

Diagramme werden mit `../../diagram.js` als SVG erzeugt. In den Aufgaben sind die Diagramm-Container
leer (Aufgaben zum Eintragen mit Achsen + Skalierung); in den Lösungen werden Geraden, Punkte und
Marker eingezeichnet. Konfigurationen stehen am Ende der jeweiligen HTML-Datei in
`window.TalsDiagrams = { ... }`.

**Skalierungs-Regel** (gemäss Styleguide Kap. 3): reine Mathematik 1:1 (`square: true`), Anwendungen
aufgabenbezogen mit Achsenbeschriftung und Einheit (z.B. `xLabel: 't [h]'`, `yLabel: 's [km]'`).

## Druck-Stylesheet

Alle vier HTML-Druckseiten teilen sich das Stylesheet `../../print.css` (im Verzeichnis
`downloads/print.css`). Anpassungen am Layout (Schriftgrösse, Ränder, Farben) gehen dort.

## Inhaltsquellen

`teste-dich-selbst.pdf`, `aufgabenserie.pdf`).
