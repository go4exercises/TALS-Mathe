# Grundlagen Gleichungen — Zusatzmaterial

Standardmaterialien für das Thema **Grundlagen Gleichungen** (Grundlagenfach 2.1).
Reihenfolge und Datei-Naming gemäss STYLEGUIDE.md (Kapitel 4 und 6).

## Dateien

| Reihenfolge | Datei | Typ | Inhalt | Status |
|---|---|---|---|---|
| 1 | `handout.html`           | Druckseite (HTML, A4) | Theorie ohne Beispiele/Aufgaben, 9 Abschnitte | ✅ |
| 2 | `formelauszug.html`      | Druckseite (HTML, A4) | Kompakte Formelsammlung, 8 Abschnitte | ✅ |
| 3 | `ankideck.apkg`          | Anki-Karteikarten     | 25 Karten zu Begriffen, Äquivalenzumformungen, Gleichungstypen, Probe | ✅ |
| 4 | `teste-dich-selbst.html` | Druckseite (HTML, A4) | 12 Aufgaben (Begriffe · Modellieren · Umformungen · Typ & Probe) mit Lösungen | ✅ |
| 5 | `aufgabenserie.html`     | Druckseite (HTML, A4) | 6 technische Anwendungen (Bauwesen, Mechanik, Elektrotechnik, Architektur, Logistik, Life Sciences) mit Musterlösungen | ✅ |

Die HTML-Druckseiten öffnen sich von der Themenseite aus in einem neuen Tab und enthalten oben einen
„Seite drucken"-Knopf. Druck-CSS (`@page` + `@media print`) sorgt für saubere A4-Ausnutzung und gute
Seitenwechsel.

## Inhaltlicher Fokus

Die Materialien decken die drei RLP-Kompetenzen für 2.1 ab:

1. Sachverhalte als Gleichung, Ungleichung oder Gleichungssystem formulieren.
2. Algebraische Äquivalenz erklären und anwenden.
3. Gleichungstyp bestimmen, geeignete Lösungsmethode wählen, Lösung durch Probe überprüfen.

## Druck-Stylesheet

Alle vier HTML-Druckseiten teilen sich das Stylesheet `../../print.css` (im Verzeichnis
`downloads/print.css`). Anpassungen am Layout (Schriftgrösse, Ränder, Farben) gehen dort.

## Anki-Deck

Das `ankideck.apkg` enthält 25 Front/Back-Karten in der Vorlage „TALS Basic". Es importiert sich
in Anki 2.x unter der Deck-Hierarchie `TALS Mathematik::Grundlagen::2.1 Grundlagen Gleichungen`.
