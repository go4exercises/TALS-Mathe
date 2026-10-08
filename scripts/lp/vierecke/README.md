# Bauskripte: Leitprogramm Vierecke

Leitprogramm zur Themenseite GF 5.2b Vierecke (`grundlagen/g5-2b-vierecke.html`), gebaut am 08.10.2026 im Kapitelmuster
mit dem Geometrie-Arbeitsbereich des Leitprogramms Planimetrie (dort Kapitel 3 als Ausgangspunkt), in der Fassung von
Trigonometrische Berechnungen. Auftrag: `AUFTRAG.md`. Kapitel: Die Vierecks-Familie · Fläche und Umfang · Trapez und
Mittellinie · Fehlende Längen. RLP 5.2 trägt keinen Vermerk «ohne Hilfsmittel»: Taschenrechner erlaubt.
Vorwissen: Leitprogramm Dreiecke (5.2a); weiter: Leitprogramm Kreis und Kreisteile (5.2c).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/vierecke.html` | **ja**, nach jeder Änderung an `seite.py`, `seite.js` oder `seite.css` |
| `seite.css` | eigener Teil des `<style>` (Block aus Planimetrie/Trig. Berechnungen, Ergänzungen am Schluss) | wird eingebunden |
| `seite.js` | fünf Geometrie-Arbeitsbereiche mit Aufgabenleiste, 10 Übungstypen, Figuren zu den Aufgaben | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/g5-2b-lp-*.json` (Reihe «Vierecke sehen») | **ja** — rettet die gemessenen `dauer` |
| `zahlen.py` | rechnet jede Zahl nach (Clips, Arbeitsbereiche, Aufgaben, Gesamttest, Bewertungspaket) | **ja**, muss «ALLE ZAHLEN STIMMEN» melden |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/vierecke/*.tex`, gebaut mit `python3 scripts/build-lp-pdf.py vierecke`.

Die Seite steht bis zur Freischaltung unverlinkt: Beim ersten Lauf setzt `seite.py` einen leeren SEO-Block mit
`noindex, nofollow`; danach bleibt der Block, wie er ist (ihn schreibt `build-seo.py`, sobald die Seite eingetragen ist).

## Arbeitsbereiche

Wie in `scripts/lp/planimetrie/README.md`: `arbeitsbereich('simN', { fenster, zeichnen(F, w, k), aufgaben })`, Aufgaben mit
`ziel`/`probe`, `wahl` (Linie antippen) oder `frage` (Grösse eingeben); `verdeckt: ['h']` zeigt den gesuchten Reglerwert als «?».

| Bereich | Figur | Regler (Start) |
|---|---|---|
| sim1 | Trapez mit fester Grundseite a = 5 cm: Parallelogramm, Rechteck, Rhombus, Quadrat einstellen; Symmetrieachse und Diagonale antippen; Winkel | c (3.5), Versatz v (1), h (3.5) — wie im Clip |
| sim2 | Parallelogramm: A = a · h, Scherung, Höhe zu a und zu b (h_b ausserhalb) | a (8), h (3), v (4) — wie im Clip |
| sim3 | Trapez mit a = 6 cm: Mittellinie, A = m · h, rückwärts | c (4), h (3), v (0.5) — wie im Clip |
| sim4 | gleichschenkliges Trapez mit grünem Teildreieck | a (12), c (4), h (3) — wie im Clip |
| sim5 | Rhombus aus den Diagonalen e = AC, f = BD | e (8), f (6) — wie in Kapitel 2 |

Der Versatz der oberen Seite heisst **v** (die Themenseite nennt ihn d, das ist hier schon die Seite DA), der Überstand im
gleichschenkligen Trapez **ü** = (a − c)/2.

## Clips

Acht Clips `g5-2b-lp-*` (Einführung und Kontrolle je Kapitel), Theme `begreifbar-schlicht`, `"probe": true`. Die Figuren
zeichnet `graf` mit `"figuren"` und `"achsen": false`; die Klickfragen zur Lage (vierte Ecke, Mitte des Schenkels) stehen mit
Achsen und `eingabe`, die Klickfrage «Hypotenuse antippen» ohne Achsen mit einer Strecke als Ziel. Zeiten auf gemessene
Wortzeiten gelegt (faster-whisper `small`, `word_timestamps`; das Audio wird vorher mit `soundfile` zu 16 kHz dekodiert, weil
die `av`-Fassung im whisper-venv `metadata_errors` nicht kennt).

## Farben — eine Farbe, eine Bedeutung

1 blau = Figur · 2 orange = Element (Höhe, Diagonale, Mittellinie, Symmetrieachse) · 3 grün = Gesuchtes, Teildreieck,
Ergebnis · 4 rot = Fehler · 5 Tinte = neutral.

## Prüfen

```sh
python3 scripts/lp/vierecke/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/vierecke.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/vierecke.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/vierecke.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/vierecke.html
node .claude/tools/pruef-geo.mjs leitprogramme/vierecke.html
node .claude/tools/pruef-fragen.mjs g5-2b-lp-kontrolle-familie g5-2b-lp-kontrolle-flaeche g5-2b-lp-kontrolle-trapez g5-2b-lp-kontrolle-laengen
```
