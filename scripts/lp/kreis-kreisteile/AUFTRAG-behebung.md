# Auftrag: Prüfbefunde in EINEM Leitprogramm GF 5.2a/b/c/d beheben

Repo /home/paps/tals-mathe. Vier Bearbeiter arbeiten parallel, je an EINEM Leitprogramm (dreiecke / vierecke /
kreis-kreisteile / aehnlichkeit — steht in deinem Startauftrag).

## Lesen
1. `CLAUDE.md`; `HOWTO-leitprogramme.md` §9, §14, §15 (Prüfliste); `HOWTO-clips.md` soweit nötig (Teilvertonung, Fragen, Figuren).
2. In `TODO.md` den Abschnitt «Prüfung Leitprogramme GF 5.2a–d (08.10.2026)», DEIN Unterabschnitt — das ist die Arbeitsliste.
   Der Unterabschnitt «Themenseiten 5.2a–d» ist NICHT deine Aufgabe (macht der Hauptagent).
3. `scripts/lp/<name>/README.md` und `AUFTRAG.md` (Bauauftrag: RLP-Kompetenzen einhalten, hohe fachliche und didaktische Qualität — gilt weiter).

## Arbeit
- Alle HOCH und MITTEL beheben, NIEDRIG so weit sinnvoll (bewusst Gelassenes mit Grund im Bericht). Jeden Befund zuerst an der
  Quelle bestätigen; was sich nicht bestätigt, nicht ändern, im Bericht sagen.
- Gesamttest: jede Teilkompetenz/Kapitelziel geprüft (oder Ziel ehrlich streichen), jedes verlangte Verfahren und jede Variante
  vorher geübt, keine Wiederholung von Kapitelaufgaben/Clips (HOWTO §9: neu kombinieren), Raster widerspruchsfrei und für eine KI
  eindeutig (gleiche Zahlen gleiche Punkte; gleichartige Ergebnisse gleich bewertet; Folgewerte aus ungerundeten Zwischenwerten;
  kein Folgepunkt für Unmögliches — eine Regel). Kompetenzmatrix im Planungskommentar nachführen. Sperrliste nachführen.
- Figuren: jede geänderte Koordinate/Länge/Label-Position vorher mit python3 rechnen; verdeckte Grössen nicht am Raster abzählbar.
- JEDE neue oder geänderte Zahl in `zahlen.py` — muss am Ende bestehen.
- Clips: Änderungen in `clips.py`, neu bauen. Geänderter Sprechtext → nur betroffene Szenen/Fragen neu vertonen:
  `export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx;
   python3 scripts/build-clip-ton.py <clip> --szenen 2,5` bzw. `python3 scripts/build-clip-fragen-ton.py <clip> --fragen 2,5:r1`,
  danach `python3 scripts/build-clips.py <clip>`. Wortzeiten der geänderten Szenen neu messen; Anker nicht auf Zahlwörter und
  nicht auf kurze Wörter, die Whisper verwechselt; danach Szenendauer prüfen (keine Stille > 2 s am Ende). Formeln mit Klammern
  so sprechen, dass man sie hört («die Summe aus …»). clip-zeit-Angaben auf der Seite nachführen.
- PDFs nur mit deinem Namen als Filter bauen (`python3 scripts/build-lp-pdf.py <name>`), danach `git status`: keine fremden PDFs.

## Grenzen
- Schreibe NUR in: `leitprogramme/<name>.html`, `scripts/lp/<name>/*`, `clips/g5-2X-lp-*`, `clips/sprechertext-g5-2X-lp-*`,
  `clips/ton/g5-2X-lp-*`, `downloads/leitprogramme/<name>/*`.
- NICHT anfassen: Themenseiten und deren Clips (`g5-2X-*` ohne `lp`), `TODO.md`, HOWTOs, `scripts/build-clips.py`,
  `scripts/lp/fragebild.py` und andere gemeinsame Werkzeuge, `build-seo.py`, andere Leitprogramme (auch `planimetrie`),
  `clips/clips.json`, `clips.html`. Kein git commit/push, kein `rm -rf`. Fehlt etwas im Clip-Bauer: Behelf + Wunsch im Bericht.
- noindex-Meta bleibt; der SEO-Block mit JSON-LD wird nie überschrieben.

## Abschluss (§14 vollständig)
pruef-uebungen 2000, pruef-formelsatz 60, pruef-leiste, pruef-geo, pruef-fragen auf alle Kontrollclips (Stapel, ohne kurzen
timeout), pruef-clip auf geänderte Clips (Bilder ANSEHEN), pruef-mathjax mit eigenem http.server auf deinem Port (danach beenden),
render-check, Preflight `python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html`. Geänderte Stellen bei 360 und
1280 px ansehen. Bilder unter `/tmp/claude-1000/-home-paps-tals-mathe/5ce60464-7415-4eef-95b6-ccf61adcaff3/scratchpad/fix-<name>/`.

## Bericht (Deutsch)
Je Befund-ID: behoben (wie) / nicht bestätigt / bewusst gelassen (warum). Liste der neu vertonten Szenen und Fragen (Hörprobe).
Zeiten. Prüfergebnisse. Neue Fehlerklassen für §15. Wünsche an den Clip-Bauer. Ehrlich, was nicht angesehen wurde.
