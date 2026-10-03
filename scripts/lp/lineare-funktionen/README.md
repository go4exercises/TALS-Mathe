# Bauskripte: Leitprogramm Lineare Funktionen

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/lineare-funktionen.html` aus einer Kapitelbeschreibung (Kopf und Grundskript werden aus der bestehenden Seite übernommen) | **ja** — für Änderungen an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Koordinatensysteme, Aufgabenleiste, Simulationen sim1–sim4, Übungen mit Rückmeldung (`TYPEN`), Minigrafen | wird von `seite.py` eingesetzt |
| `clips.py` | hat am 03.10.2026 die acht Drehbücher `clips/g3-2-lp-*.json` erzeugt | **nein** — die JSONs sind seit der Vertonung die Quelle und tragen die gemessenen `dauer` |
| `pruef-graf.py` | rechnet die Koordinatenbilder der Clips nach: alles im Fenster, keine Beschriftung auf Gerade, Punkt, Achsenmarke oder anderer Beschriftung | vor jedem Clip-Bau, wenn ein `graf` geändert wurde |
| `grafgeom.py` | die Geometrie dahinter (Pixelmasse aus `build-clips.py`), geteilt von `clips.py` und `pruef-graf.py` | wird eingebunden |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/lineare-funktionen/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/lineare-funktionen.html
```

Änderungen **nur hier** machen, nicht direkt in der HTML-Datei — sonst überschreibt der
nächste Lauf sie. Ausnahme: der Kopf (`<style>`, SEO-Block), den `seite.py` aus der Seite liest.

Clips ändern: Drehbuch `clips/g3-2-lp-*.json` bearbeiten, dann

```sh
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g3-2-lp-<name>   # wenn Sprechertext oder Szenen ändern
python3 scripts/build-clip-fragen-ton.py g3-2-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           g3-2-lp-<name>
```

Laufzeiten auf den Clip-Karten in `seite.py` danach nachführen (und, sobald das
Leitprogramm freigeschaltet ist, die Gesamtzeit auf dem Kärtchen in `leitprogramme.html`).

Gesamttest und Bewertungspaket: `downloads/leitprogramme/lineare-funktionen/*.tex`,
bauen mit `python3 scripts/build-lp-pdf.py`. Gemeinsame Gestaltung:
`downloads/leitprogramme/lp-druck.sty` — Name und RLP-Nummer setzt jede Quelle selbst
mit `\renewcommand{\lpname}` und `\renewcommand{\lpteilgebiet}`. Dort kein `\lt`/`\gt`:
pdfLaTeX kennt sie nicht, `<` und `>` tun es.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/lineare-funktionen.html 2000
node .claude/tools/pruef-leiste.mjs   leitprogramme/lineare-funktionen.html
node .claude/tools/pruef-fragen.mjs   g3-2-lp-kontrolle-m-und-b g3-2-lp-kontrolle-steigung \
                                      g3-2-lp-kontrolle-typen g3-2-lp-kontrolle-aufstellen
node .claude/tools/render-check.mjs   leitprogramme/lineare-funktionen.html
python3 scripts/lp/lineare-funktionen/pruef-graf.py
```

`seite.js` setzt dafür die Testhaken `box.__aufgabe` und `box.__typ`; jeder Übungstyp
liefert mit `fehler(A)` gezielte Falscheingaben samt Stichwort der erwarteten Meldung
(HOWTO-leitprogramme §14). Die Stichwörter dürfen **kein LaTeX** enthalten — im
Prüflauf bleibt `\(y\)-Achse` ungesetzt stehen, «y-Achse» passt dann nicht.
