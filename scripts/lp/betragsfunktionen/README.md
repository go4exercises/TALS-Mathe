# Bauskripte: Leitprogramm Betragsfunktionen

Leitprogramm zum Teilgebiet SP 3.6 (`s3-6-betragsfunktionen.html`) — eine **Ergänzung des
TALS-Lehrmittels, kein RLP-2030-Teilgebiet**. Bezug zum RLP: SP 2.2 «elementare
Betragsgleichungen lösen (auch ohne Hilfsmittel)» und die Funktionssicht aus SP 3.1. Die fünf
Kompetenzen stehen in der Box «Ergänzung TALS» der Themenseite; je eine trägt ein Kapitel:
Die Betragsfunktion · Verschieben und Strecken · Umklappen · Abschnittsweise schreiben (mit der
Wanne) · Gleichungen und Ungleichungen. Alles ohne Taschenrechner.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/betragsfunktionen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | fünf Simulationen mit Aufgabenleiste, 10 Übungstypen, Minigrafen (`data-k`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/s3-6-lp-*.json` (Reihe «Knick sehen») | **ja** — rettet die gemessenen `dauer` |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/betragsfunktionen/*.tex`,
gebaut mit `python3 scripts/build-lp-pdf.py betrag`.

## Farben — eine Farbe, eine Bedeutung

1 blau = Betragskurve · 2 orange = Waagrechte y = c und Lösungen · 3 grün = die Äste als
Geraden (abschnittsweise Terme) · 4 rot = Gegenbeispiel · 5 Tinte = f vor dem Betrag,
Symmetrieachse. Weil grün hier die Äste sind, ist die Zielkurve der Simulationen grau.

## Minigrafen

`data-k="v,a,u,v;…"` mit Teilen `v` (a·|x − u| + v), `w` (|x − a| + |x − b|), `G`/`Q`
(|m x + q|, |a x² + b x + c|) und `g`/`q` (die Funktion vor dem Betrag, gestrichelt).

## Bewegte Kurven

`vk([[t, a, u, v], …], knick=True, achse=True)` für y = a·|x − u| + v (HOWTO-clips.md,
«Betragskurven»). Für |f(x)| mit krummem f eine feste `formel` mit `abs(…)`.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/betragsfunktionen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        s3-6-lp-<name>
python3 scripts/build-clip-fragen-ton.py s3-6-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           s3-6-lp-<name>
python3 scripts/lp/betragsfunktionen/seite.py
```

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/betragsfunktionen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/betragsfunktionen.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/betragsfunktionen.html
node .claude/tools/pruef-fragen.mjs s3-6-lp-kontrolle-betragsfunktion s3-6-lp-kontrolle-verschieben \
     s3-6-lp-kontrolle-umklappen s3-6-lp-kontrolle-abschnittsweise s3-6-lp-kontrolle-gleichungen
```
