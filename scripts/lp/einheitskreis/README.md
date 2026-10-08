# Bauskripte: Leitprogramm Einheitskreis

Leitprogramm zum Teilgebiet GF 5.4 (`g5-4-einheitskreis.html`), gebaut am 07.10.2026 im Kapitelmuster
(HOWTO-leitprogramme §4). Drei Kompetenzen; K3 trägt den Vermerk «auch ohne Hilfsmittel», die besonderen
Werte (K2) gehören dazu. Fünf Kapitel: Sinus und Cosinus am Einheitskreis · Besondere Winkel (ohne
Rechner) · Tangens und trigonometrischer Pythagoras · Symmetrien (ohne Rechner) · Periode und
Umkehroperationen. Vorwissen: LP Trigonometrische Berechnungen (GF 5.3), Bogenmass (GF 5.1). Weiter:
LP Trigonometrische Gleichungen (GF 5.5).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/einheitskreis.html` (Gerüst beim ersten Lauf aus `planimetrie.html`) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | fünf Kreisbild-Simulationen mit Aufgabenleiste, 10 Übungstypen, Kreisbilder zu den Aufgaben (`svg.ek-mini[data-ek]`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g5-4-lp-*.json` (Reihe «Einheitskreis sehen») | **ja** — rettet die gemessenen `dauer` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips mit faster-whisper → `wortzeiten.json` | nach jeder Neuvertonung |
| `teilton.py` | vertont nur einzelne Szenen (`szenen <clip> "<Szene>"`) oder Fragetöne (`fragen <clip> <i>[:<schl>]`) neu; die übrigen Szenen kommen unverändert aus der bisherigen Tonspur | nach einer Textkorrektur statt `build-clip-ton.py` |
| `zahlen.py` | rechnet jede Zahl der Seite, der Clips und des Gesamttests nach | vor jedem Bau |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/einheitskreis/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py einheitskreis` (Teil A ohne, Teil B mit Taschenrechner).

## Das Kreisbild

Seite: `Kreisbild(svg, { w, x0, x1, y0, y1 })` in `seite.js` — gleich geteilte Achsen, die Höhe folgt aus
der Breite, damit der Kreis rund bleibt. `zeichneP(K, φ)` zeichnet Dreieck OQP, Winkelbogen (über eine
Runde hinaus als Spirale), Radius, cos-Strecke (grün) und sin-Strecke (blau).

Clips: Der Einheitskreis besteht aus `figuren` (HOWTO-clips, «Figuren im Graf»). `Lauf([[t, θ], …])`
gibt den Winkel θ(t) weich zwischen Stützwinkeln; `P_teile(L)` und `tan_teile(L)` rechnen daraus alle
Teile mit dichten Stützpunkten (0.05 s) — Punkt, Radius, Strecken und S bleiben beieinander, und P läuft
auf dem Kreisbogen statt auf der Sehne. Die Achsenzahlen ±1 setzt `graf()` als Text neben den Kreis
(die Teilung des Bauers schriebe sie auf die Kreislinie).

## Zeiten auf den Ton

```sh
python3 scripts/lp/einheitskreis/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g5-4-lp-<name>
python3 scripts/build-clip-fragen-ton.py g5-4-lp-<name>   # nur Kontrollclips
python3 scripts/lp/einheitskreis/wortzeiten.py <name>     # Wortzeiten messen
python3 scripts/lp/einheitskreis/clips.py                 # Einblendungen auf die Wörter legen
python3 scripts/build-clips.py           g5-4-lp-<name>
python3 scripts/lp/einheitskreis/seite.py
```

`wann(clip, szene, wort)` in `clips.py` liest die gemessene Zeit des Wortes; fehlt sie, schätzt es aus
der Lage im Sprechertext und meldet das am Ende.

## Farben — eine Farbe, eine Bedeutung

1 blau = Sinus · 2 orange = Tangens (und der Spiegelpunkt B in Kapitel 4) · 3 grün = Cosinus ·
4 rot = Gegenbeispiel (in den Clips auch die Gerade OP bei 90°, die die Tangente nicht trifft) · 5 Tinte = neutral
(Kreis, Radius, P, Winkel, Spiegelachsen, Referenzwinkel als Bogen — seit der Prüfung vom 08.10.2026 nicht mehr orange). Die Themenseite färbt Sinus und Cosinus in ihren Animationen uneinheitlich; hier
gilt die Zuordnung des Leitprogramms Trigonometrische Funktionen (SP 3.5).

## Prüfen

```sh
python3 scripts/lp/einheitskreis/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/einheitskreis.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/einheitskreis.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/einheitskreis.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/einheitskreis.html
node .claude/tools/pruef-fragen.mjs g5-4-lp-kontrolle-sinus-cosinus g5-4-lp-kontrolle-besondere-winkel \
     g5-4-lp-kontrolle-tangens-pythagoras g5-4-lp-kontrolle-symmetrien g5-4-lp-kontrolle-periode-umkehr
```

## Prüfung vom 08.10.2026

Befunde in `TODO.md` («Prüfung Einheitskreis»). Neu vertont mit `teilton.py` (alles andere unverändert):
sinus-cosinus «Weiter drehen» · kontrolle-tangens-pythagoras «Frage 5» · symmetrien «Anwenden» ·
kontrolle-periode-umkehr «Frage 3» (neue Frage zur Periode des Tangens); Fragetöne
kontrolle-sinus-cosinus f1-fall1/fall2, kontrolle-tangens-pythagoras f0-r0, kontrolle-symmetrien f4-r2,
kontrolle-periode-umkehr f2-* und f4-r2.

Übung «Exakte Werte»: Verteilung mit 20 000 Würfen nachgezählt (Sperrliste angewendet):
52 verschiedene Aufgaben (vorher 15); Achsenwinkel 16.5 % (vorher 60 %), negative Winkel 30 %, über 360° 36 %,
Bogenmass 15 %. Nachzählen wie in der Prüfliste (§15): 20 000-mal «Neue Zahlen» und die Schlüssel zählen.
