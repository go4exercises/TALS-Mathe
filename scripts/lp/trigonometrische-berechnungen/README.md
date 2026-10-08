# Bauskripte: Leitprogramm Trigonometrische Berechnungen

Leitprogramm zum Teilgebiet GF 5.3 (Themenseite `g5-3-trigonometrische-berechnungen`), gebaut am 07.10.2026 im
Kapitelmuster mit dem Geometrie-Arbeitsbereich des Leitprogramms Planimetrie. Kapitel: Sinus, Cosinus und Tangens ·
Winkel berechnen · Höhen und Distanzen · Sinussatz (mit SSW) · Cosinussatz und Dreiecksfläche. RLP 5.3 trägt keinen
Vermerk «ohne Hilfsmittel»: Taschenrechner erlaubt (Gradmodus). Vorwissen: Leitprogramm Planimetrie; weiter:
Leitprogramm Einheitskreis (5.4).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/trigonometrische-berechnungen.html` | **ja**, nach jeder Änderung an `seite.py`, `seite.js` oder `seite.css` |
| `seite.css` | eigener Teil des `<style>` (Block aus Planimetrie übernommen, Ergänzungen am Schluss) | wird von `seite.py` eingebunden |
| `seite.js` | fünf Geometrie-Arbeitsbereiche mit Aufgabenleiste, 11 Übungstypen, Figuren zu den Aufgaben | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g5-3-lp-*.json` (Reihe «Dreiecke berechnen») | **ja** — rettet die gemessenen `dauer` |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/trigonometrische-berechnungen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py trigonometrische-berechnungen`.

Die Seite steht bis zur Freischaltung unverlinkt (`noindex, nofollow` im SEO-Block, den `build-seo.py` übernimmt).

## Arbeitsbereich

Wie in `scripts/lp/planimetrie/README.md`: `arbeitsbereich('simN', { fenster, zeichnen(F, w, k), aufgaben })`, Aufgaben
mit `ziel`/`probe`, `wahl` (Linie antippen) oder `frage` (Grösse eingeben). Neu: `fest: { … }` an einer Aufgabe setzt
Werte, die nicht auf dem Reglerraster liegen (H = 4 / cos 55°, α = arctan 0.7); `lab` und `gegeben`/`gesucht` steuern,
was Figur und Live-Zeile zeigen — bei Fragen nur das Gegebene. Die Figurenliste kennt zusätzlich `["w", Scheitel, P1, P2,
"Text"]` (Winkelbogen).

## Farben — eine Farbe, eine Bedeutung

1 blau = Figur · 2 orange = betrachteter Winkel, gegebene Stücke, Höhe · 3 grün = Gesuchtes, Ergebnis · 4 rot = Fehler ·
5 Tinte = neutral. (Die Animation «Definition» der Themenseite färbt die Gegenkathete rot; hier nicht.)

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/trigonometrische-berechnungen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/trigonometrische-berechnungen.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/trigonometrische-berechnungen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/trigonometrische-berechnungen.html
node .claude/tools/pruef-geo.mjs leitprogramme/trigonometrische-berechnungen.html
node .claude/tools/pruef-fragen.mjs g5-3-lp-kontrolle-seiten g5-3-lp-kontrolle-winkel g5-3-lp-kontrolle-hoehen g5-3-lp-kontrolle-sinussatz g5-3-lp-kontrolle-cosinussatz
```
