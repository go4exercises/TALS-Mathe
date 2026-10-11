# CLAUDE.md — simulationen/

Lädt nur, wenn Claude an Dateien in `simulationen/` arbeitet. Die Regeln für alle Simulationen und Werkzeuge stehen
in der Haupt-`CLAUDE.md` (Projektstruktur), Aufbau und Eintragen in `HOWTO-simulationen.md`. Hier: die einzelnen Seiten.

- `simulationen/standardabweichung.html` (seit 11.10.2026, erste Simulationsseite): eine Stichprobe (2–8 Werte, 0–20)
  ziehen oder eintippen, in sechs Schritten von den Abweichungen über ihre Quadrate (flächengetreu) zu Varianz und
  \(s\) (Standard \(n - 1\) wie g4.3, umschaltbar auf \(\sigma\)), dann \(R\), \(\text{QD}\) (Median der Hälften) und
  \(\bar{x} \pm s\) im Vergleich und «ohne den äussersten Wert». Variationskoeffizient nur als Zusatz (nicht im RLP).
  Aus einer externen Vorlage übernommen und angepasst. Selbsttest `scripts/verify_standardabweichung.js` (python3
  `statistics`). Verlinkt aus g4.3 (`#darstellungen`).
- `simulationen/boxplot.html` (seit 11.10.2026): 4–15 ganze Werte (0–20) im Punktdiagramm, gemeinsam für sechs Schritte —
  sortierte Liste mit Plätzen von \(Q_0\)…\(Q_4\) (Median der Hälften), Boxplot Teil für Teil, vier Teile mit gleich vielen
  Werten (nach Rang; Plätze genau auf einer Grenze zählen zu keinem Teil, Whisker dort immer bis Min/Max) und Form (`form()`),
  Ausreisser nach der Faustregel \(1.5 \cdot \text{QD}\) aus g4.3 — standardmässig einzeln gezeichnet, Whisker bis zum letzten Wert
  davor; Schalter «Whisker» in Schritt 3, 5, 6 auf «bis Min und Max» wie in g4.2, Vergleich mit einer Gruppe B. Selbsttest `scripts/verify_boxplot.js` (python3
  `statistics`, prüft auch die Aussagen «drei Viertel ≤ \(Q_3\)» und «Hälfte ≥ Median»). Verlinkt aus g4.2 und g4.3 (`#darstellungen`).
