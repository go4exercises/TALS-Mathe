# Bauskripte: Leitprogramm Trigonometrische Funktionen

Leitprogramm zum Teilgebiet SP 3.5 (`s3-5-trigonometrische-funktionen.html`). Das Teilgebiet hat
eine einzige Kompetenz — Funktionsverlauf von Sinus, Cosinus und Tangens visualisieren,
Periodizität und Symmetrien kennen, «mit und ohne Hilfsmittel». Fünf Kapitel: Vom Einheitskreis
zur Kurve · Periode und Symmetrie · Tangensfunktion · Strecken und Verschieben (alle ohne
Hilfsmittel) · Symmetrie nutzen (mit Taschenrechner: alle Lösungen von sin x = c).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/trigonometrische-funktionen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | fünf Simulationen mit Aufgabenleiste (zwei mit Einheitskreis), 10 Übungstypen, Minigrafen (`data-t`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/s3-5-lp-*.json` | **ja** — rettet die gemessenen `dauer` |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/trigonometrische-funktionen/*.tex`,
gebaut mit `python3 scripts/build-lp-pdf.py trigonometrische` (Teil A ohne, Teil B mit Rechner).

## Farben — eine Farbe, eine Bedeutung

1 blau = Sinus · 3 grün = Cosinus · 2 orange = Tangens · 4 rot = Gegenbeispiel ·
5 Tinte = neutral (Einheitskreis, Mittellinie, Pole, Waagrechte y = c). Weil grün hier der
Cosinus ist, ist die Zielkurve der Simulationen grau (in den anderen Leitprogrammen grün).

## Eingaben mit π

Die Übungen lesen `3π/4`, `3pi/4`, `-π/2`, `2pi`, `3/4π`; gerundete Dezimalzahlen (±0.001)
gelten bei Winkeln auch. Regler für Winkel tragen `data-pi` (Nenner): Sie laufen über ganze k,
der Wert ist kπ/Nenner, die Anzeige ein Vielfaches von π.

## Bewegte Kurven

`sk([[t, a, b, u, v], …])` für a·sin(b(x − u)) + v, `ck()` die Cosinuskurve, `tk(…)` der
Tangens; `kreis=KREIS(bahn)` setzt den Einheitskreis daneben (HOWTO-clips.md, «Sinus- und
Tangenskurven»). Bild unten über die ganze Bühne (1640 × 480), Text darüber.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/trigonometrische-funktionen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        s3-5-lp-<name>
python3 scripts/build-clip-fragen-ton.py s3-5-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           s3-5-lp-<name>
python3 scripts/lp/trigonometrische-funktionen/seite.py
```

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/trigonometrische-funktionen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/trigonometrische-funktionen.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/trigonometrische-funktionen.html
node .claude/tools/pruef-fragen.mjs s3-5-lp-kontrolle-kreis-kurve s3-5-lp-kontrolle-periode-symmetrie \
     s3-5-lp-kontrolle-tangens s3-5-lp-kontrolle-parameter s3-5-lp-kontrolle-gleichungen
```
