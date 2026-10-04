# Bauskripte: Leitprogramm Exponential- und Logarithmusfunktionen

Leitprogramm zum Teilgebiet SP 3.4, für **beide** Themenseiten (`s3-4a-exponentialfunktionen.html`,
`s3-4b-logarithmusfunktionen.html`): Die vierte Kompetenz verlangt die Logarithmusfunktion
ausdrücklich als Umkehrfunktion der Exponentialfunktion. Fünf Kapitel: Exponentialfunktion ·
Wachstum und Zerfall · e-Funktion und Basiswechsel · Sättigung · Logarithmusfunktion.
Alle vier Kompetenzen tragen «auch ohne Hilfsmittel» — Übungen, Aufgaben und Gesamttest sind
ohne Taschenrechner lösbar (schöne Zahlen, Halbierungen statt Logarithmen mit Komma).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/exp-log-funktionen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | fünf Simulationen mit Aufgabenleiste, 15 Übungstypen, Minigrafen (`data-e`, `data-l`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/s3-4-lp-*.json` | **ja** — rettet die gemessenen `dauer` (Szenenname + Sprechertext gleich) |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/exp-log-funktionen/*.tex`,
gebaut mit `python3 scripts/build-lp-pdf.py exp-log`.

## Farben — eine Farbe, eine Bedeutung

1 blau = Exponentialkurve und Basis @a@ · 2 orange = Startwert und Faktor (N₀, A, b) ·
3 grün = Logarithmuskurve, Umkehrfunktion, e-Form · 4 rot = Gegenbeispiel ·
5 Tinte = neutral (Asymptote, Sättigungswert, y = x).

## Bewegte Kurven

`ek([[t, c, a, v], …])` für \(y = c \cdot a^x + v\) und `lk([[t, c, a, v], …])` für
\(y = c \cdot \log_a x + v\) — neu im Clip-Bauer seit dem 04.10.2026 (HOWTO-clips.md).
`spiegel` an einer Exponentialkurve zeichnet die Logarithmuskurve. Die Live-Beschriftung
rundet auf eine Stelle; Werte wie 0.125 als feste Marke schreiben.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/exp-log-funktionen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        s3-4-lp-<name>   # wenn Sprechertext oder Szenen ändern
python3 scripts/build-clip-fragen-ton.py s3-4-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           s3-4-lp-<name>
python3 scripts/lp/exp-log-funktionen/seite.py           # Clipzeiten auf der Seite nachführen
```

**Klickfragen:** Die Toleranz gilt in Dateneinheiten, für beide Achsen gleich. In Fenstern
mit grosser \(y\)-Spanne (bis 1000) ist ein Punkt so kaum zu treffen — dort Wahlfragen stellen.

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/exp-log-funktionen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/exp-log-funktionen.html 1000
node .claude/tools/pruef-leiste.mjs leitprogramme/exp-log-funktionen.html
node .claude/tools/pruef-fragen.mjs s3-4-lp-kontrolle-exponentialfunktion s3-4-lp-kontrolle-wachstum \
     s3-4-lp-kontrolle-e-funktion s3-4-lp-kontrolle-saettigung s3-4-lp-kontrolle-logarithmus
```
