# CLAUDE.md — werkzeuge/

Lädt nur, wenn Claude an Dateien in `werkzeuge/` arbeitet. Die Regeln für alle Simulationen und Werkzeuge stehen
in der Haupt-`CLAUDE.md` (Projektstruktur), Aufbau und Eintragen in `HOWTO-werkzeuge.md`. Hier: die einzelnen Seiten.

**Alle sieben Trainer laufen im gemeinsamen Rahmen** `trainer.css` + `trainer.js` (Klassen `tr-`, HOWTO-werkzeuge §3
«Trainer-Rahmen», Vorbild `systemtrainer.html`): Karte bis zum unteren Bildschirmrand, «Nächster Schritt» oben rechts
im Kopf, Lösung wächst in der Arbeitsfläche unter der Aufgabe, Bedienleiste unten. Geprüft bei 1280×800 und 360×740:
Karte ganz im Fenster, Seite scrollt nicht. Seiteneigenes `<style>` nur noch für Besonderheiten (Palette, Kreis,
Phasen, Verlauf). Was mehrere Trainer brauchen, gehört in `trainer.css`, nicht in die Seiten. In Zeichenketten im
Skript `'</div>'` nicht unausgeglichen notieren — die div-Bilanz des Pre-Flights zählt sie mit.

**Alle sieben Trainer haben die Taste «Nächster Schritt»** (seit 11.10.2026): Sie deckt die Lösung Schritt für Schritt
auf, jeder Schritt mit Kopf «Schritt n · Bezeichnung» (Regel bzw. Operation, nie nur «Schritt 2»). Zählt nicht als
Fehler, aber nicht mehr als «auf Anhieb»; nach dem letzten Schritt ist die Aufgabe abgeschlossen (Notationstrainer:
Karte dreht sich um und geht zurück in Fach 1). Eingabe-Trainer bilden die Schritte im Kern mit `schrittListe(a)`
→ `[{ titel, zeilen }]`, gezeigt von `wegHtml(a, k)`; ihre Selbsttests prüfen Titel und dass keine Wegzeile verloren
geht. Strategie- und Systemtrainer führen den nächsten passenden Schritt aus (Taste N) und schreiben jeden Schritt mit
Kopf in den Verlauf. Einheitskreistrainer: Schritte stehen neben `herleitung()` ein zweites Mal, der Selbsttest
meldet, wenn sie auseinanderlaufen.

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
  Sonderfälle 2×2, 3×3 lösen, Lösungsfall erkennen (`#thema=zwei,sonder,drei,lage`). Seit 11.10.2026 ein **Trainer für
  das Vorgehen, nicht für das Rechnen**: Man wählt konkrete Schritte, das Werkzeug führt sie aus. Phasen: Verfahren
  wählen oder zuerst umformen (ordnen, nach einer Variablen auflösen, vervielfachen; beide Reihenfolgen gehen) →
  vorbereiten → anwenden (einsetzen, gleichsetzen, I ± II) → Gleichung mit einer Variablen deuten (auflösen,
  Widerspruch, immer wahr) → zurück einsetzen; bei 3×3 davor Variable und Gleichung zum Eliminieren. Bewertung wie
  im Strategietrainer: ok / um (Umweg, grau, kein Fehler) / x (Begründung, Code für die Bilanz), Tipp beim zweiten,
  Schritt beim dritten Fehlgriff. Die Eingabe von 𝕃 gibt es nicht mehr; 𝕃 schreibt das Werkzeug ans Ende des Wegs.
  Erzeuger mit Formen std, roh (ungeordnet), nach x oder y aufgelöst. Selbsttest `scripts/verify_systemtrainer.js`:
  je Aufgabe vier Zufallswege über passende Schritte, nie eine Sackgasse, Ende beim Gauss-Ergebnis, jede Art von
  Schritt und Fehlgriff kommt vor; python3 prüft jede Zeile jedes Wegs gegen den Zeilenraum.
  `STATISTIK.widerspruch` muss 0 bleiben, sonst verwirft der Erzeuger kaputte Wege still.
- `werkzeuge/parabeltrainer.html` (seit 29.10.2026): Geraden- und Parabeltrainer (GF 3.2, 3.3), **bewusste Ausnahme vom
  Trainer-Rahmen**: extern gebaut und auf Wunsch des Auftraggebers fast unverändert übernommen, mit eigenem `<style>`,
  ohne `nav.js`, `style.css` und Taste «Nächster Schritt». Er **öffnet in einem neuen Fenster**: Baustein auf g3.2
  (`#gleichung-aufstellen`) und g3.3 (`#darstellungen`) und Kachel in `werkzeuge.html` mit `target="_blank"`. Darum steht
  die Datei in `EIGENES_SKELETT` des Pre-Flights (kein `page-wrap`, keine nav). Angepasst wurde nur der Rahmen:
  HTML-Gerüst, `../schriften.css` statt Google Fonts (Titelschrift Source Sans 3 statt Bricolage Grotesque),
  `../vendor/mathjax/tex-svg.js` statt CDN, SEO- und FUSS-Marken samt `.site-footer`-Regel im `<style>`, KERN-Marken.
  Zwei Modi (Zeichnen: Gleichung → Graph, Ablesen: Graph → Gleichung), vier Formen (Gerade `mx + q`, Scheitelform,
  Produktform, allgemeine Form), Zufallsaufgaben oder eigene Parameter, Punkte setzen oder vorführen, Skizze mit
  Abweichungsprüfung. Kein `localStorage`. Gerechnet wird exakt mit der Bruchklasse `Q`. **Notation weicht von den
  Themenseiten ab** (`q` statt `b`, «Produktform» statt «Linearfaktorform», \(x_S, y_S\) statt \(u, v\)) — vom
  Auftraggeber so übernommen. Selbsttest `scripts/verify_parabeltrainer.js`: je Form und Modus 2000 Zufallsaufgaben,
  jeder Zielpunkt eines Zeichenschritts exakt auf dem Graphen, Formen, Nullstellen und Rückwege (`mkParABC`,
  `mkParRoots`) in `python3` mit `Fraction` nachgerechnet, Schritttexte ohne `undefined`/`NaN`/Dezimalkomma.
  Die Zustandsvariablen `F` und `form` stehen als `let` im Kern; der Test setzt sie über `setze()`.
