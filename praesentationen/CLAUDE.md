# CLAUDE.md — praesentationen/

Lädt nur, wenn Claude an Dateien in `praesentationen/` arbeitet. Aufbau, Eintragen und Prüfen stehen in
`HOWTO-praesentationen.md`. Hier: die einzelnen Präsentationen.

Alle sind extern gebaut und mit wenig Eingriff übernommen. Sie haben ihr eigenes Aussehen (Heft-Look,
Bühne 1600 × 900, eigene Navigationsleiste) und öffnen sich in einem neuen Fenster. Alle Formeln stehen
in MathJax; Texte aus dem Skript laufen über `mjHTML`. Beschriftungen in den SVG-Figuren sind Text.
Das Karoraster des Originals ist entfernt (Wunsch vom 23.11.2026, gilt für jede neue Präsentation).
Die Fusszeile jeder Folie («Raphael Arnold Kohler · 23.11.2026») ist vom Original übernommen und fest.

- `praesentationen/rechtwinkliges-dreieck.html` (seit 23.11.2026), 18 Folien: rechtwinkliges Dreieck,
  Thaleskreis, Satz des Pythagoras, Kathetensatz und Höhensatz (je mit Scherungen bewiesen),
  \(\sqrt{n}\) mit dem Höhensatz konstruieren, drei ähnliche Dreiecke, Seitenverhältnisse und
  Sinus/Cosinus/Tangens, dazu sieben Aufgabenfolien mit 20 Aufgaben (alle Lösungen am 23.11.2026 in
  `python3` nachgerechnet). Verlinkt aus g5.2a (`#pythagoras`) und g5.3 (`#recht-dreieck`).
  Farbmakros `\ca`, `\cb`, `\cc`, `\ch`, `\cr` in der MathJax-Einstellung (Farben wie `--a`, `--b`, `--c`,
  `--h`, `--rot`). Ergebnisse über `E(tex)` (fett, grün durch `.loes b`). Kein Rechenkern; geprüft von
  `verify_praesentationen.js`.
  **Notation vom Original:** GK, AK, H für die Seiten, \(p\) bei \(a\), \(q\) bei \(b\).
- `praesentationen/sinussatz-cosinussatz.html` (seit 23.11.2026), 6 Folien: allgemeines Dreieck, Herleitung
  von Sinussatz (mit Umkreis) und Cosinussatz über die Höhe, «Welcher Satz führt zum Ziel?» mit sechs Fällen
  (Konstruktion und Rechenweg, Werte über Regler), Überblick. Verlinkt aus g5.3 (`#strategie`, Rücklink auf
  `#schief-dreieck`). Rechenkern (`FALL`, `loese`, `punkte`, `rechnung`) zwischen den KERN-Marken; Selbsttest
  `scripts/verify_sinussatz-cosinussatz.js` mit allen ganzzahligen Reglerwerten (bis 20000 je Fall) gegen eine
  Konstruktion aus Koordinaten in `python3`.
  **Notation vom Original, auf Wunsch nicht an g5.3 angeglichen:** Fälle SsW, sSw (zwei Lösungen) und SWW,
  wo g5.3 SSW und WWS schreibt.
  Angepasst: Im Überblick stand «Cosinussatz» rot (Rot = Fehler/Achtung); jetzt blau.
