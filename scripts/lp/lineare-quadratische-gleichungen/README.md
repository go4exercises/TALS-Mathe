# Bauskripte: Leitprogramm Lineare und quadratische Gleichungen

Leitprogramm zum Teilgebiet GF 2.2 (Themenseiten `g2-2a-lineare-gleichungen.html` und
`g2-2b-quadratische-gleichungen.html`), gebaut am 06.10.2026 nach dem Leitfaden des
Auftraggebers (`HOWTO-GleichungLP.md`) im Kapitelmuster der Funktionen-Leitprogramme. Die eine
RLP-Kompetenz ist für die Matrix in fünf Teile gegliedert, je ein Kapitel: Lineare Gleichungen
umformen · Ausklammern und Nullprodukt (das ausgearbeitete Kapitel des Leitfadens) · Wurzelziehen,
Ergänzen, Mitternachtsformel · Das passende Verfahren · Parameterdiskussion. Alles ohne
Taschenrechner. Ersetzt später das ältere Leitprogramm *Quadratische Gleichungen*.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/lineare-quadratische-gleichungen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | Umformer (Kapitel 1–4) und Parameter-Simulation (Kapitel 5) mit Aufgabenleiste, 10 Übungstypen, Minigrafen (`data-k`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g2-2-lp-*.json` (Reihe «Gleichungen lösen») | **ja** — rettet die gemessenen `dauer` |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/lineare-quadratische-gleichungen/*.tex`,
gebaut mit `python3 scripts/build-lp-pdf.py lineare-quadratische`.

## Der Umformer

Statt Reglern wählen die Lernenden jeden Umformungsschritt selbst, füllen Lücken (Faktorform,
Koeffizienten, Diskriminante) und geben am Schluss die Lösungsmenge ein. Eine Aufgabe ist ein
kleiner Graph von Knoten in `seite.js` (`umformerSim('simN', [...])`):

- `w: [[Knopftext, Ziel, Umformung, Hinweis], …]` — ein Schritt. Ziel `'!Text'` ist ein Fehler mit
  eigener Rückmeldung; gültige andere Wege führen auf eigene Knoten (z. B. erst `−4`, dann `−x`).
- `feld: { muster, soll | pruef, fehler, tipp, nach }` — eine Lücke; `fehler` sind bekannte
  Fehleingaben mit eigener Rückmeldung.
- `L: [Zahlen] | [] | 'R'` mit `Lfalsch` und `probe` — die Lösungsmenge. Eingabe mit Strichpunkt,
  Reihenfolge und Doppelte egal, Brüche wie `-2/3`, `{}` leer, `R` alle Zahlen.

Die Umformung steht wie im Heft rechts neben der Zeile, auf die sie wirkt.

## Farben — eine Farbe, eine Bedeutung

1 blau = Gleichung, Graph · 2 orange = Umformung, Parameter k · 3 grün = Lösungen ·
4 rot = Fehler, verlorene Lösung · 5 Tinte = neutral (Bezugslinien). Die rechte Seite einer Gleichung im Graph ist orange, wie `.kurve.rechts` auf der Seite.

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/lineare-quadratische-gleichungen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/lineare-quadratische-gleichungen.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/lineare-quadratische-gleichungen.html
node .claude/tools/pruef-umformer.mjs leitprogramme/lineare-quadratische-gleichungen.html
node .claude/tools/pruef-fragen.mjs clips/g2-2-lp-kontrolle-*.html
```

`pruef-umformer` prüft jeden Umformer: alle Ziele vorhanden und erreichbar, keine Sackgasse; jede
Aufgabe auf dem ersten und dem letzten gültigen Weg lösbar; jeder Fehlerknopf, jede falsche Lücke
und jede falsche Lösungsmenge gibt eine Rückmeldung.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/lineare-quadratische-gleichungen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g2-2-lp-<name>
python3 scripts/build-clip-fragen-ton.py g2-2-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           g2-2-lp-<name>
python3 scripts/lp/lineare-quadratische-gleichungen/seite.py
```
