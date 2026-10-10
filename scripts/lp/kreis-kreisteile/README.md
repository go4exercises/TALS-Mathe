# Bauskripte: Leitprogramm Kreis und Kreisteile

Leitprogramm zur Themenseite GF 5.2c (`grundlagen/g5-2c-kreis-und-kreisteile.html`), gebaut am 08.10.2026 im Kapitelmuster
mit dem Geometrie-Arbeitsbereich der Leitprogramme Planimetrie und Trigonometrische Berechnungen (Auftrag: `AUFTRAG.md`).
Kapitel: Linien am Kreis · Umfang, Fläche und π · Bogen und Sektor · Segment und Kreisring. RLP 5.2 trägt keinen Vermerk
«ohne Hilfsmittel»: Taschenrechner erlaubt. Die Seite steht bis zur Freischaltung unverlinkt (`noindex, nofollow`).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/kreis-kreisteile.html` | **ja**, nach jeder Änderung an `seite.py`, `seite.js` oder `seite.css` |
| `seite.css` | eigener Teil des `<style>` (Block aus Trig. Berechnungen kopiert, Ergänzungen am Schluss) | wird eingebunden |
| `seite.js` | fünf Arbeitsbereiche mit Aufgabenleiste, 11 Übungstypen, Figuren zu den Aufgaben | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/g5-2c-lp-*.json` (Reihe «Kreisteile sehen») | **ja** — rettet die gemessenen `dauer` nach Szenenname und meldet Szenen mit neuem Text («neu zu vertonen»: `build-clip-ton.py --szenen`) |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper) → `wortzeiten.json`; `clips.py` setzt Einblendungen «@wort» darauf | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede Zahl von Seite, Clips und PDFs nach | **muss bestehen** |
| `verteilung.mjs` | zählt 20 000 Würfe je Übungstyp (Schlüssel, Sollwerte) | bei Änderungen an den Übungen |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/kreis-kreisteile/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py kreis-kreisteile` (Filter mit vollem Namen — «kreis» träfe auch einheitskreis).

## Arbeitsbereich

Wie in `scripts/lp/planimetrie/README.md`: Aufgaben mit `ziel`/`probe`, `wahl` (Linie antippen) oder `frage` (Grösse eingeben),
`fest`/`verdeckt` wie in Trig. Berechnungen, dazu `ohne` (Regler, die in der Figur der Aufgabe nichts bedeuten, zeigen «–»; Prüfung 08.10.2026). Neu: `kandidatZug` (Kandidat auf einem Kreisbogen; x1 … y2 = Anfang und Mitte für
`pruef-geo`), `F.sektor`, `F.ring`, und `korrigiere(regler, p)` hält gekoppelte Regler gültig (Kreisring r < R). Die
Winkelregler gehen in 15°-Schritten (6–7 px je Stellung), damit Zielwinkel auch mit dem Finger treffbar sind.

## Farben — eine Farbe, eine Bedeutung

1 blau = Figur (Kreis, Geraden) · 2 orange = Element (Sehne, Bogen, Lot, Dreieck M P₁ P₂), Kandidat, Gegebenes · 3 grün =
Fläche (Sektor, Segment, Ring), Ergebnis · 4 rot = Fehler · 5 Tinte = neutral.

## Prüfen

```sh
python3 scripts/lp/kreis-kreisteile/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/kreis-kreisteile.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/kreis-kreisteile.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/kreis-kreisteile.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/kreis-kreisteile.html
node .claude/tools/pruef-geo.mjs leitprogramme/kreis-kreisteile.html
node .claude/tools/pruef-fragen.mjs g5-2c-lp-kontrolle-linien g5-2c-lp-kontrolle-umfang g5-2c-lp-kontrolle-sektor g5-2c-lp-kontrolle-segment
```

## Footer

Den Footer schreibt `scripts/build-seo.py` (seit 10.10.2026, eine Version für das ganze Lehrmittel):
`seite.py` gibt nur leere FUSS-Marken aus. **Nach jedem Bau `python3 scripts/build-seo.py`**, sonst fehlt
der Footer (der Pre-Flight meldet es).
