# Auftrag: Prüfbefunde im Leitprogramm «Textaufgaben modellieren» beheben

Repo /home/paps/tals-mathe. Du behebst die Befunde in `leitprogramme/modellieren.html` (Quelle `scripts/lp/modellieren/`).

## Lesen
1. `CLAUDE.md` (Schweizer Hochdeutsch, kein ß, Dezimalpunkt, `\(…\)`, leere Menge `\{\,\}`, Mengen mit Strichpunkt).
2. `HOWTO-leitprogramme.md` §9, §14, §15 (Prüfliste), `HOWTO-clips.md` soweit nötig (Rechneranzeige, Teilvertonung).
3. In `TODO.md` den Abschnitt «Prüfung Textaufgaben modellieren (08.10.2026)» — das ist die Arbeitsliste (H1–H4, M1–M12, NIEDRIG).
   Der Unterabschnitt «Themenseite g2-modellieren» ist NICHT deine Aufgabe (macht der Hauptagent).
4. `scripts/lp/modellieren/README.md`, `AUFTRAG.md` (ursprünglicher Bauauftrag — dessen Anforderungen bleiben gültig).

## Arbeit
- Alle HOCH und MITTEL beheben, NIEDRIG so weit sinnvoll (was du bewusst lässt, mit Grund im Bericht).
  Jeden Befund zuerst an der Quelle bestätigen; was sich nicht bestätigt, nicht ändern, im Bericht sagen.
- H1: G2 durch ein quadratisches System mit Produkt der Unbekannten ersetzen, mit Rechner (Teil-Zuordnung und Hilfsmittel
  auf Seite und PDF nachführen); die übrigen Kapitelziele (Sets, «ganz, nicht negativ») prüfbar machen, wo es ohne
  Aufblähen geht. Gesamttest-Wiederholungen (HOWTO §9): neue Aufgaben, die Geübtes neu kombinieren; jedes verlangte
  Verfahren muss vorher geübt sein (oder G4 Verdunsten vorher üben). Sperrliste nachführen. Raster widerspruchsfrei und
  für eine KI eindeutig («gleiche Zahlen, gleiche Punkte»; gleichwertige Wege nennen).
- M6: Rechneranzeigen bei Dezimal-Koeffizienten: entweder ganzzahlige Grundform (mit Faktor erweitern) oder keine Aussage zur
  Anzeigeform — nichts Unbelegtes behaupten. Lösungen mit 1 + p bleiben, p als Dezimalzahl.
- M12: Zeiten realistisch neu schätzen (Kapitel, Gesamttest) und überall gleich nachführen (Seite, Übersicht, README).
- JEDE neue oder geänderte Zahl mit python3 nachrechnen — `zahlen.py` nachführen, muss am Ende bestehen.
- Clips: Änderungen in `clips.py`, dann neu bauen. Ändert sich gesprochener Text, nur betroffene Szenen/Fragen neu vertonen:
  `export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx;
   python3 scripts/build-clip-ton.py <clip> --szenen 2,5` (Szenen ab 1) bzw.
  `python3 scripts/build-clip-fragen-ton.py <clip> --fragen 2,5:r1`, danach `python3 scripts/build-clips.py <clip>`.
  Wortzeiten der geänderten Szenen neu messen (`scripts/lp/modellieren/wortzeiten.py`, `.claude/tools/sprechzeiten.py`).
  Ergebnis nie vor dem Satz, der es nennt. Fragebild nur das Gegebene. Text der Frage = gesprochener Text.
  clip-zeit-Angaben auf der Seite nachführen.
- PDFs neu bauen — **nur mit dem Filter `modellieren`** (README warnt: Filter `gesamttest.tex` baut 12 fremde PDFs neu!).
  Danach `git status` prüfen: keine fremden PDFs geändert. PDFs ansehen.

## Grenzen
- Schreibe NUR in: `leitprogramme/modellieren.html`, `scripts/lp/modellieren/*`, `clips/g2-M-lp-*`, `clips/sprechertext-g2-M-lp-*`,
  `clips/ton/g2-M-lp-*`, `downloads/leitprogramme/modellieren/*`.
- NICHT anfassen: Themenseiten (auch `grundlagen/g2-modellieren.html` und `clips/g2-M-deklarieren*`/andere `g2-M-*` ohne `lp`),
  `TODO.md`, HOWTOs, `scripts/build-clips.py` und andere gemeinsame Werkzeuge, `build-seo.py`, andere Leitprogramme,
  `clips/clips.json`, `clips.html`. Kein git commit/push, kein `rm -rf`. Fehlt etwas im Clip-Bauer: Behelf in clips.py + Wunsch.
- noindex-Meta bleibt; der SEO-Block mit JSON-LD wird nicht überschrieben.

## Abschluss (§14 vollständig)
pruef-uebungen 2000, pruef-formelsatz 60, pruef-leiste, pruef-fragen auf alle 8 Kontrollclips (in Stapeln, ohne kurzen timeout),
pruef-clip auf geänderte Clips (Bilder ANSEHEN), pruef-mathjax mit eigenem http.server auf Port 8908, render-check, Preflight
`python3 .claude/skills/preflight/preflight.py leitprogramme/modellieren.html`. Geänderte Stellen bei 360 und 1280 px ansehen.
Bilder unter `/tmp/claude-1000/-home-paps-tals-mathe/5ce60464-7415-4eef-95b6-ccf61adcaff3/scratchpad/fix-g2M/`.

## Bericht (Deutsch)
Je Befund-ID: behoben (wie) / nicht bestätigt / bewusst gelassen (warum). Liste der neu vertonten Szenen und Fragen (für die
Hörprobe). Neue Zeiten. Ergebnisse der Prüfwerkzeuge. Neue Fehlerklassen für die Prüfliste §15. Wünsche an den Clip-Bauer.
Ehrlich, was nicht angesehen wurde.
