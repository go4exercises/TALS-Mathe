# Quadratische Funktionen — Zusatzmaterial

Standardmaterialien für das Thema **Quadratische Funktionen** (Grundlagenfach 3.3).
Reihenfolge und Datei-Naming gemäss STYLEGUIDE.md (Kapitel 4 und 6).

## Dateien

| Reihenfolge | Datei | Typ | Inhalt | Status |
|---|---|---|---|---|
| 1 | `handout.html`           | Druckseite (HTML, A4) | Theorie ohne Beispiele/Aufgaben, 9 Abschnitte | ✅ |
| 3 | `ankideck.apkg`          | Anki-Karteikarten     | 25 Karteikarten zum Auswendiglernen | ✅ |
| 4 | `teste-dich-selbst.html` | Druckseite (HTML, A4) | 12 Grundlagenaufgaben mit Lösungen | ✅ |
| 5 | `aufgabenserie.html`     | Druckseite (HTML, A4) | 8 technische Anwendungen mit Lösungen | ✅ |

Die HTML-Druckseiten öffnen sich von der Themenseite aus in einem neuen Tab und enthalten oben einen
„Seite drucken"-Knopf. Druck-CSS (`@page` + `@media print`) sorgt für saubere A4-Ausnutzung und gute
Seitenwechsel.

## Anki-Deck

Das Deck `ankideck.apkg` enthält 25 Karten zu Definition, drei Darstellungsformen, Mitternachtsformel
und Diskriminante, Umwandlungen, Aufstellen der Funktionsgleichung, Spezialfälle und typischen
Anwendungen. Es importiert sauber als Unter-Deck unter
`Mathe begreifbar :: Grundlagen :: 3.3 Quadratische Funktionen` und folgt dem gleichen Karten-Modell
wie die anderen TALS-Decks (Schriftart Source Sans 3, helle Hintergrundfarbe).

## Diagramme in den Druckseiten

Diagramme werden mit `../../diagram.js` als SVG erzeugt. In den Aufgaben sind die Diagramm-Container
leer (Aufgaben zum Eintragen mit Achsen + Skalierung); in den Lösungen werden Parabeln (über
`curves: [{ fn: x => ..., color, label }]`), Punkte und Marker eingezeichnet. Konfigurationen stehen
am Ende der jeweiligen HTML-Datei in `window.TalsDiagrams = { ... }`.

> **Hinweis Erweiterung:** Für 3.3 wurde `diagram.js` um die Option `curves` erweitert (beliebige
> Funktionen \(y = f(x)\) statt nur Geraden). Bestehende `lines`-Konfigurationen aus 3.2 sind voll
> kompatibel.

**Skalierungs-Regel** (gemäss Styleguide Kap. 3): reine Mathematik 1:1 (`square: true`), Anwendungen
aufgabenbezogen mit Achsenbeschriftung und Einheit (z.B. `xLabel: 't [s]'`, `yLabel: 'h [m]'`).

## Druck-Stylesheet

Alle vier HTML-Druckseiten teilen sich das Stylesheet `../../print.css` (im Verzeichnis
`downloads/print.css`). Anpassungen am Layout (Schriftgrösse, Ränder, Farben) gehen dort.

## Inhaltsquellen

Die Druckseiten basieren auf den Lehrmittel-Vorlagen für die Berufsmaturität. Die Lehrer-PDF-Vorlage
mit den sechs Anwendungen der drei Darstellungsformen (Allgemeine Form, Scheitelform,
Linearfaktorform — je 2 Anwendungen) ist als kompakte Tabelle in das Handout und in die Themenseite
integriert.
