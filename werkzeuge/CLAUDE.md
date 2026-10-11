# CLAUDE.md — werkzeuge/

Lädt nur, wenn Claude an Dateien in `werkzeuge/` arbeitet. Die Regeln für alle Simulationen und Werkzeuge stehen
in der Haupt-`CLAUDE.md` (Projektstruktur), Aufbau und Eintragen in `HOWTO-werkzeuge.md`. Hier: die einzelnen Seiten.

- `werkzeuge/notationstrainer.html` — Lernkartei (3 Fächer, Stand in `localStorage` unter
  `tals-mathe-notationstrainer-v1`, in `rechtliches.html` genannt) zur Notation von
  𝔻, 𝕃 und Intervallen mit wechselnder Grundmenge. Die Karten stehen als Array `KARTEN`
  im Seitenskript und nennen das **Ergebnis** der Rechnung, nicht die Aufgabe — geübt wird
  nur die Schreibweise; jede Lösung vor dem Eintrag mit `python3` nachrechnen. Verlinkt aus
  g2.1 (`#definition`); seit 10.10.2026 nur Grundlagenfach (116 Karten, die 25 des
  Schwerpunktfachs und der Fach-Filter sind entfernt). Bis 10.10.2026 lag er als `notationstrainer.html` im Root.
- `werkzeuge/strategietrainer.html` (seit 10.10.2026): Zufallsaufgaben aus sieben Bereichen —
  lineare, quadratische und Bruchgleichungen, Faktorisieren, Bruchterme, lineare Systeme und Systeme
  mit Parabel (SF). Man wählt den nächsten Schritt aus einer festen Liste je Familie (Gleichungen 15,
  Terme 10, Systeme 7); das Werkzeug führt ihn aus (✓), weist einen erlaubten Umweg grau ab (≈) oder
  begründet den Fehlgriff (✗; Tipp beim zweiten, Lösung beim dritten). Aufgaben werden von hinten
  gebaut, gerechnet wird exakt (Brüche, Wurzeln, ganzzahlige Paare). Der Kern steht zwischen
  `KERN:ANFANG`/`KERN:ENDE` und wird von `scripts/verify_strategietrainer.js` (im Pre-Flight) mit
  Zufallsaufgaben durchgespielt: alle Wege, Lösungen gegen die gestellte Aufgabe, Terme an
  Zufallsstellen, 𝔻 gegen den Nenner. Neue Vorlage oder Regel → dort zuerst grün. Vorwahl über
  `#bereich=fakt,bruchterm` (kein `?`: `check_sim_wz` liest die Adresse bis `#` als Dateinamen).
  Verlinkt aus g1.3, g2.2a, g2.2b, g2.3, s2.2a, s3.1. Weitere Trainer-Ideen: `../TODO-trainer-mathe.md`.
- `werkzeuge/rechentrainer.html` (seit 11.10.2026): Rechnen ohne Taschenrechner (GF 1.1/1.2) in sechs
  Themen — Hierarchie der Operationen, Vorzeichen, Brüche, Bruch–Dezimal–Prozent, Perioden, Zahlenmengen. Kern ist die
  **Fehlerdiagnose**: Jede Aufgabe wird zusätzlich mit typischen Denkfehlern gerechnet (Parser mit
  umschaltbaren Regeln: Strich vor Punkt, −3² als 9, a − (−b) als a − b …); trifft die Antwort einen
  davon, nennt die Rückmeldung den Fehler mit Link (`FEHLER`). Lösungsweg Stufe für Stufe nach g1.1.
  Vorwahl `#thema=reihenfolge,vorzeichen`. Selbsttest `scripts/verify_rechentrainer.js` rechnet jede
  Aufgabe in `python3` mit `Fraction` nach.
- `werkzeuge/einheitskreistrainer.html` (seit 11.10.2026): Grad ↔ Bogenmass, exakte Werte von sin/cos/tan
  (Palette, Diagnose: Vorzeichen, sin/cos bzw. 30°/60° vertauscht, Kehrwert, «nicht definiert»), vom Wert
  zum Winkel (Punkte am Kreis anklicken). Werte aus Quadrant und Referenzwinkel, Herleitung mit Skizze.
  Anzeige Grad/Bogenmass/gemischt; Vorwahl `#teil=werte&mass=rad`. Selbsttest
  `scripts/verify_einheitskreistrainer.js` mit Gegenrechnung in `python3`.
- `werkzeuge/termtrainer.html` (seit 11.10.2026): Terme umformen (GF 1.3, SF 1.1) in sieben Themen — Zusammenfassen,
  Klammern, Klammer mal Klammer, binomische Formeln, Ausklammern, Faktorisieren, Bruchterme kürzen. Die Eingabe
  (`3x^2-2x+1`, `2x(x+3)(x-3)`, `(x-3)/(x+3)`) wird exakt als Quotient zweier Polynome verglichen; die Form
  (ausmultipliziert, vollständig faktorisiert, gekürzt) am Syntaxbaum. Aufgaben stehen als Eingabetext,
  Lösungsweg und Denkfehler ebenso (`diag`, `FEHLER`). Vorwahl `#thema=binome,faktorisieren`. Selbsttest
  `scripts/verify_termtrainer.js` wertet alles in `python3` mit `Fraction` aus und prüft Unzerlegbarkeit.
- `werkzeuge/gesetzetrainer.html` (seit 11.10.2026): Potenz-, Wurzel- und Logarithmengesetze (GF 1.4, SF 1.2, 1.3),
  Bereiche wählbar (`#bereich=potenzen,wurzeln,rational,logarithmen`; `wurzeln` nur GF-1.4-Stoff mit
  ⁿ√x = x^{1/n}, m/n-Exponenten im Bereich `rational` (SF)). Antwort in Feldern einer Zielform (`ziel`, z.B.
  `x^{{n}}`, `{k}\sqrt{{r}}`); Potenzterme als Exponentenbäume, Denkfehler durch umgeschaltete Regeln
  (`expo(x, 'p1mal')` …), dazu «Regel prüfen» (`FALLEN`). Selbsttest `scripts/verify_gesetzetrainer.js` rechnet
  in `python3` unabhängig nach (Wurzeln als `(x**m)**(1/n)`, `math.log`).
- `werkzeuge/systemtrainer.html` (seit 11.10.2026): lineare Gleichungssysteme (GF 2.3) in vier Themen — 2×2 lösen,
  Sonderfälle 2×2, 3×3 lösen, Lösungsfall erkennen (`#thema=zwei,sonder,drei,lage`). Man wählt den Lösungsfall und gibt
  𝕃 ein: Zahlen bzw. bei unendlich vielen Lösungen \(y\) (und \(z\)) als Ausdruck in \(x\), Schreibweise
  \(\{(x \mid \ldots) : x \in \mathbb{R}\}\) wie in g2.3 und im Notationstrainer. Die Prüfung macht die Probe und
  erkennt vertauschte Werte, Vorzeichen, falschen Lösungsfall, Fehler beim Auflösen nach y. Lösungsweg nach Form
  (Einsetzen, Gleichsetzen, Addieren mit kleinerem kgV; 3×3: eliminieren, 2×2, zurück), bei 2×2 Skizze der Geraden (SVG).
  Selbsttest `scripts/verify_systemtrainer.js`: python3 löst jedes System selbst und prüft, dass jede Wegzeile aus dem
  System folgt (Zeilenraum der erweiterten Matrix); `STATISTIK.widerspruch` muss 0 bleiben, sonst verwirft der
  Erzeuger kaputte Wege still.
