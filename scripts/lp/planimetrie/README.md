# Bauskripte: Leitprogramm Planimetrie

Leitprogramm zum Teilgebiet GF 5.2 (Themenseiten `g5-2a-dreiecke`, `g5-2b-vierecke`,
`g5-2c-kreis-und-kreisteile`, `g5-2d-zentrische-streckung-aehnlichkeit`), gebaut am 06.10.2026 nach dem
Leitfaden des Auftraggebers (`HOWTO-PlaniLP.md`) im Kapitelmuster der Funktionen- und
Gleichungen-Leitprogramme. Kapitel: Dreiecke beschreiben · Dreiecksfläche und zugehörige Höhe (das
ausgearbeitete Kapitel des Leitfadens) · Vierecke · Kreis und Kreisteile · Ähnlichkeit. RLP 5.2 trägt
keinen Vermerk «ohne Hilfsmittel»: Taschenrechner erlaubt.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/planimetrie.html` | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | fünf Geometrie-Arbeitsbereiche mit Aufgabenleiste, 10 Übungstypen, Figuren zu den Aufgaben (`svg.geo-mini[data-fig]`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g5-2-lp-*.json` (Reihe «Figuren sehen») | **ja** — rettet die gemessenen `dauer` |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/planimetrie/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py planimetrie`.

## Der Geometrie-Arbeitsbereich

`arbeitsbereich('simN', { fenster, zeichnen(F, w, k), aufgaben })` in `seite.js`. Die Figur steht in
Weltkoordinaten (1 Einheit = 1 cm, beide Achsen gleich geteilt). Drei Arten von Aufgaben, wie der
Leitfaden sie verlangt (Figur verändern — Hilfslinie wählen — Grösse berechnen):

- `ziel(w)` mit `probe` — Reglerzustand; `probe` ist ein Beispiel, das die Aufgabe löst (für das Prüfwerkzeug).
- `wahl: { richtig, rueck: { id: 'Text' } }` — Kandidatenlinien antippen (Tastatur: Tab und Enter);
  jede falsche Linie hat eine eigene Rückmeldung.
- `frage: [{ name, label, einheit, soll, fehler: [[wert, 'Text']] }]` — Grössen eingeben;
  richtig auf zwei Dezimalen, zu grob gerundet gibt einen eigenen Hinweis.

`setup(s)` setzt und sperrt Regler (`s.setze`, `s.sperre`); gefragte Werte erscheinen erst nach der richtigen Antwort.

## Clips: Figuren im Graf

Die Clips zeichnen Dreiecke, Vierecke, Kreise und Sektoren mit dem `graf`-Feld `"figuren"` und
`"achsen": false` (HOWTO-clips.md, «Figuren im Graf», seit 06.10.2026).

## Farben — eine Farbe, eine Bedeutung

1 blau = Figur · 2 orange = Hilfslinie, Element, Streckfaktor · 3 grün = gesuchte Grösse, Fläche ·
4 rot = Fehler · 5 Tinte = neutral.

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/planimetrie.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/planimetrie.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/planimetrie.html
node .claude/tools/pruef-geo.mjs leitprogramme/planimetrie.html
node .claude/tools/pruef-fragen.mjs clips/g5-2-lp-kontrolle-*.html
```
