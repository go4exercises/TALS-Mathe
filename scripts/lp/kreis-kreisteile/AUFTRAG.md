# Auftrag: Leitprogramm zu EINER Themenseite GF 5.2a/b/c/d

Repo /home/paps/tals-mathe. Vier Bearbeiter bauen parallel je EIN Leitprogramm nach dem Kapitelmuster, je eines pro
Themenseite. Welches du baust, steht in deinem Startauftrag. Massstab: **hohe fachliche und didaktische Qualität** —
lieber weniger, dafür richtig und gut erklärt.

## Wortlaut des Auftraggebers (verbindlich)
«Leitprogramm zu den Themenseiten g5.2a–d … zu jeder Themenseite ein eigenes Leitprogramm» — «halte dich an die
Kompetenzen aus dem RLP (siehe Themenseiten) und halte die didaktische und fachliche Qualität hoch».

## Zuordnung
| Themenseite | Datei | Bauskripte | Clips | Reihe | Port |
|---|---|---|---|---|---|
| `grundlagen/g5-2a-dreiecke.html` | `leitprogramme/dreiecke.html` | `scripts/lp/dreiecke/` | `g5-2a-lp-*` | «Dreiecke sehen» | 8931 |
| `grundlagen/g5-2b-vierecke.html` | `leitprogramme/vierecke.html` | `scripts/lp/vierecke/` | `g5-2b-lp-*` | «Vierecke sehen» | 8932 |
| `grundlagen/g5-2c-kreis-und-kreisteile.html` | `leitprogramme/kreis-kreisteile.html` | `scripts/lp/kreis-kreisteile/` | `g5-2c-lp-*` | «Kreisteile sehen» | 8933 |
| `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` | `leitprogramme/aehnlichkeit.html` | `scripts/lp/aehnlichkeit/` | `g5-2d-lp-*` | «Ähnlichkeit sehen» | 8934 |
`lektion` der Clips: `["g5-2a"]` usw. (Codes aus nav.js). localStorage `lp-<name>-thema`, `lp-<name>-stand`.
Downloads: `downloads/leitprogramme/<name>/`. Scratchpad: `/tmp/claude-1000/-home-paps-tals-mathe/5ce60464-7415-4eef-95b6-ccf61adcaff3/scratchpad/lp-<name>/`.

## Kompetenzen (RLP GF 5.2, Kompetenzbox der Themenseiten, wörtlich)
- geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke,
  Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
- deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante,
  Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen
- die Ähnlichkeit für Berechnungen in der Ebene nutzen
Alle vier Seiten tragen dieselbe Box. **Dein Leitprogramm nimmt die Teile, die zu SEINEN Objekten und Elementen
gehören** (Dreiecke: spezielle Dreiecke, Höhen, Seiten-/Winkelhalbierende, Mittelsenkrechte, Winkel, Umfang, Fläche,
Abstand …; Vierecke: Quadrat, Rechteck, Parallelogramm, Rhombus, Trapez mit Mittellinie, Diagonalen …; Kreis: Sehne,
Sekante, Tangente, Sektor, Segment, Bogen, Winkelmass, Abstand …; Ähnlichkeit: zentrische Streckung, Ähnlichkeit für
Berechnungen). Jede Teilkompetenz deiner Seite wird in einem Kapitel erarbeitet, geübt und im Gesamttest geprüft —
Kompetenzmatrix (HOWTO §2) im Planungskommentar. Was die Themenseite (Lernziele, Aufgaben A1–A7) behandelt, ist der
Stoffumfang; nichts darüber hinaus als Kern. Den RLP selbst gegenlesen: `/home/paps/Math-GL.pdf` (pypdfium2/pdftotext).

## Zuerst lesen (vollständig)
1. `CLAUDE.md`; 2. `HOWTO-leitprogramme.md` ganz (inkl. §15 Prüfliste — ALLE Fehlerklassen von vornherein vermeiden,
auch die neuen vom 08.10.2026: Einführungsbild verrät die Lösung nicht, Teile des Gesamttests nach Hilfsmittel,
Sachzusammenhang realistisch, gleiche Zahlen gleiche Punkte, Rechneranzeige nur so weit belegt …);
3. `STYLEGUIDE.md` §2.11, §6.4, §6.5; 4. `HOWTO-clips.md` (Drehbuchformat, Fragen, Figuren, «Dritte Runde»,
Teilvertonung `--szenen`/`--fragen`);
5. **Das bestehende Leitprogramm `leitprogramme/planimetrie.html` mit `scripts/lp/planimetrie/` (README, seite.py,
seite.js mit Geometrie-Arbeitsbereich, clips.py) und seinen Clips `clips/g5-2-lp-*.json`** — es deckt alle vier Seiten
mit je einem Kapitel ab (geprüft und behoben: TODO.md «Prüfung Planimetrie (06.10.2026)»). Dein Kapitel daraus ist der
Ausgangspunkt; übernimm Bewährtes (Arbeitsbereich, Figuren, Übungstypen) als **Kopie in deinen Ordner** — Planimetrie
selbst NICHT ändern, seine Clips nicht umbenennen oder überschreiben. Neue Clips heissen `g5-2X-lp-*`.
6. Neueres Vorbild für Bauweise und SEO-Block-Handling: `scripts/lp/trigonometrische-berechnungen/` (seite.py: noindex
nur beim ersten Lauf; einen vorhandenen SEO-Block mit JSON-LD NIE überschreiben), `downloads/leitprogramme/<vorbild>/*.tex`,
`scripts/build-lp-pdf.py`.
7. Deine Themenseite ganz (fachliche Wahrheit, Notation, Bezeichnungen, Farben, Beispiele) und ihre Clips
`clips/g5-2X-*.json`. Bezeichnungen und Formeln so wie die Themenseite; Widersprüche dort melden, nicht übernehmen.

## Umfang und Aufbau
- Vorwissenstest, **4 Kapitel** (je 35–45 min nach HOWTO §3; Zeiten aus den Teilen schätzen, nicht schönrechnen —
  wenn es mehr wird, ehrlich ausweisen), Gesamttest + Bewertungspaket (LaTeX → PDF, Teile nach Hilfsmittel).
- Je Kapitel: Einführungsclip mit Auftrag → Simulation/Geometrie-Arbeitsbereich mit Aufgabenleiste (erfahren) →
  Kontrollclip mit Fragen (Wahl/Klick, Rückmeldung verrät die Lösung nicht, Fragebild nur das Gegebene,
  `scripts/lp/fragebild.py`) → Festhalten (verallgemeinern) → Übungen mit Rückmeldung (Zufall, Diagnosen,
  Sperrliste gegen feste Aufgaben, Testhaken `box.__aufgabe`/`box.__typ`) → Aufgaben mit Lösungen.
  Je Kapitel mindestens eine «Warum»-Aufgabe (Begründen) und eine Aufgabe an der Figur.
- Clips: 8–10 neue, `"probe": true`; Sprechertexte so, dass Piper sie gut spricht (Zahlen ausgeschrieben).
  Ergebnis nie vor dem Satz, der es nennt (Zeiten auf gemessene Wortzeiten: `.claude/tools/sprechzeiten.py`,
  faster-whisper unter `~/.local/share/whisper-venv/bin/python`; Anker nicht auf Zahlwörter).
- Figuren geometrisch exakt: jede Koordinate, jeder Winkel, jede Länge, jede Label-Position mit python3 vorab
  berechnen (`zahlen.py`); Figuren massstäblich, sonst «nicht massstäblich» dazuschreiben.
- TI-30X-Angaben nur mit Beleg (HOWTO-clips «Rechneranzeige»); in der Planimetrie meist keine nötig.

## Grenzen
- Schreibe NUR in deine Dateien (Tabelle oben: Seite, Bauskripte, `clips/g5-2X-lp-*`, `clips/sprechertext-g5-2X-lp-*`,
  `clips/ton/g5-2X-lp-*`, deinen Download-Ordner).
- NICHT anfassen: `leitprogramme.html`, `index.html`, Themenseiten, `scripts/build-seo.py`, `scripts/build-suchindex.py`,
  `clips.html`, `clips/clips.json`, `scripts/build-clips.py` und andere gemeinsame Werkzeuge, TODO/HOWTO/CHANGELOG,
  andere Leitprogramme (auch `planimetrie.html` und `scripts/lp/planimetrie/`), Clips anderer Präfixe.
  Kein git commit, kein git push, kein `rm -rf`. Fehlt etwas im Clip-Bauer: Behelf in deinem clips.py + Wunsch im Bericht.
- PDFs nur mit **deinem Namen als Filter** bauen (`python3 scripts/build-lp-pdf.py <name>`) und danach mit `git status`
  prüfen, dass keine fremden PDFs geändert sind (sonst `git checkout` genau dieser Dateien).
- Seitenkopf: `<meta name="robots" content="noindex, nofollow">` im SEO-Block (unverlinkt; das Eintragen macht der Hauptagent).
- Kopiere diesen Auftrag als Erstes nach `scripts/lp/<name>/AUFTRAG.md`.

## Prüfen (§14 vollständig)
pruef-uebungen 2000, pruef-formelsatz 60, pruef-leiste, pruef-geo (Arbeitsbereich), pruef-fragen auf alle Kontrollclips
(in Stapeln, ohne kurzen timeout), pruef-clip (SP auf deinen Scratchpad-Ordner setzen!) und Bilder ANSEHEN, pruef-mathjax
mit eigenem http.server auf deinem Port, render-check, Preflight
`python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html`. Seite bei 360/1280 px hell und dunkel
ansehen, PDFs ansehen. Erreichbarkeit der Leistenziele mit Maus/Finger messen. Alle Zahlen in `zahlen.py`, muss bestehen.
Vertonen: `export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx;
python3 scripts/build-clip-ton.py <clip>`, Fragen `python3 scripts/build-clip-fragen-ton.py <clip>`, danach build-clips.py.

## Bericht (Deutsch)
Kompetenzmatrix kurz (Teilkompetenz → Kapitel → Übung → Gesamttestaufgabe), Kapitelübersicht, was bewusst anders als
die Themenseite oder das Planimetrie-Kapitel, Widersprüche/Fehler der Themenseite (mit Zeile), Dateien, Prüfergebnisse,
SEO-Beschreibung (1–2 Sätze) + Themen-Stichworte, Lektionen/Zeiten, Clipzahl und -zeit, offene Punkte, Wünsche an den
Clip-Bauer, ehrlich was nicht angesehen wurde.
