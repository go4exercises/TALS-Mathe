# TODO — Korrekturen an den Mathe-Trainern

Prüfung vom 11.10.2026: alle sechs Trainer unter `werkzeuge/` auf fachliche Richtigkeit und
didaktische Qualität. Je Trainer ein Prüfdurchgang: Kern in `node:vm` geladen, tausende
Zufallsaufgaben erzeugt, Werte mit `python3` nachgerechnet. Geprüft wurden gezielt Fälle, die die
Selbsttests nicht abdecken. Notations- und Einheitskreistrainer liefen zusätzlich im Browser bei
1280 und 360 px. Drei B-Befunde sind von Hand nachgestellt (RT-B1, GT-B1, TT-B2).

**Ergebnis:** In keinem Trainer gibt es eine fachlich falsche Aussage (Stufe A). Die Mängel betreffen:
- die Bewertung von Antworten: richtige Antworten abgelehnt, falsche angenommen;
- Rückmeldungen, die einen Denkfehler nennen, der zur Aufgabe nicht passt;
- einzelne didaktische Schwächen.

**Schweregrade**
- **B:** falsche Bewertung einer Antwort oder didaktisch deutlich verbesserungswürdig. Zuerst beheben.
- **C:** Kleinigkeit oder Wortlaut.

**Bei jeder Korrektur:**
- Den Fall zuerst als Prüfung in `scripts/verify_<name>.js` aufnehmen, die rot wird.
- Dann den Kern ändern.
- Dann den Pre-Flight laufen lassen.

---

## Gesetzetrainer (`werkzeuge/gesetzetrainer.html`)

- [ ] **GT-B1 · Vorzeichen-Aufgaben mit ungeradem Exponenten** (`potenzWert`, Art `vorzeichen`)
  - Bei ungeradem n ist (−a)ⁿ = −aⁿ, die Aufgabe übt also nichts.
  - Trotzdem wird eine falsche Antwort als Klammerfehler etikettiert: `(-3)^{3}`, Eingabe 27 → «Klammer um die negative Basis übersehen». Wer die Klammer übersieht, käme aber auf −27, also auf das richtige Ergebnis.
  - Betrifft 41 % dieser Aufgaben.
  - → Nur n = 2 oder 4 verwenden, oder bei ungeradem n `negKlammer`/`negsq` weglassen.
- [ ] **GT-B2 · `basenVerschieden` bei gleicher Basis** (`potenzWert`, Art `gesetz`)
  - `3^{-1}·3^{-2}`, Wert 9⁻³ → «Verschiedene Basen wie gleiche behandelt». Der Text erklärt dann P4 mit 5³·2³.
  - → Eigener Code `basenMal` («a^m·a^n ≠ (a·a)^{m+n}»), oder die Diagnose streichen.
- [ ] **GT-B3 · Subtraktion als Addition etikettiert** (`wurzelAufgabe('produkt')` beim Quotienten, `summe` mit Minus)
  - `√18/√2`, Wert √16 → «Radikanden addiert statt multipliziert (W1)».
  - `√27 − √12`, Wert √15 → ebenfalls «addiert».
  - → Code `wurzelDiv` («subtrahiert statt dividiert, W2») und für `radikandAddiert` einen Text für das Minus.
- [ ] **GT-B4 · Nenner-Diagnose ohne Nenner** (`logZusammenfassen`)
  - `['logZerlVz', [m, −n]]` wird auch bei positivem n gesetzt.
  - `3log₂x + 2log₂y`, Eingabe n = −2 → «Nenner mit falschem Vorzeichen».
  - → Nur bei n < 0 setzen, sonst ein eigener Text: «Summe → Produkt».
- [ ] **GT-B5 · Bereich Wurzeln enthält SF-Stoff, verlinkt aus GF**
  - g1.4 behandelt nur ⁿ√a = a^{1/n}. Rationale Exponenten m/n stehen erst in SF 1.2.
  - g1.4 (`#wurzelgesetze`) verlinkt `#bereich=wurzeln`, dort verlangen etwa 35 % der Aufgaben m/n-Exponenten: `x/∛(x⁴)`, `x³·∛x`, `ratWert` wie 8^{2/3}.
  - → Einen Bereich «Rationale Exponenten (SF)» abspalten (`wurzelPotenz` mit m ≠ 1, `ratWert`), und den Link in g1.4 auf die GF-Typen setzen. Die Bausteine in g1.4 und s1.2 anpassen.
- [ ] **GT-B6 · «Regel prüfen»: zwei Regeln scheinen sich zu widersprechen** (`FALLEN.wurzeln`)
  - «√(a²) = a» gilt laut Trainer nicht.
  - «ⁿ√(aᵐ) = a^{m/n}» gilt laut Trainer immer; mit m = n = 2 ist das genau √(a²) = a.
  - Die Voraussetzung a > 0 steht erst in der Begründung.
  - → Die Voraussetzung in die Aussage schreiben («für a > 0»), oder die Regel als «gilt nicht immer» mit a = −3, m = n = 2 führen.
- [ ] GT-C1 · Der Lösungsweg nennt «P4 rückwärts» und «P7»; das ist die Nummerierung von g1.4. SF 1.2 nummeriert «Gesetz 1–5». Dort ist Gesetz 4 = aⁿbⁿ = (ab)ⁿ. → Die Regel ausschreiben oder beide Nummern nennen.
- [ ] GT-C2 · `ln(√e)` mit Eingabe 2 ergibt `logKehr` statt `logWurzel`. → Bei Wurzel-Argumenten `logWurzel` zuerst prüfen.
- [ ] GT-C3 · `FEHLER.falleGeglaubt`: Der Satz «… nicht für Summen» passt bei mehreren Fallen nicht, etwa (aᵐ)ⁿ = a^{m+n} und log(u/v) = log u/log v. → Satz streichen.
- [ ] GT-C4 · Die Fehler-Links `negBasis`, `basisMal`, `nullExp`, `kehrVergessen`, `negsq` und `negKlammer` zeigen auf s1-2. Im Bereich Potenzen und für GF-Lernende → auf g1.4 (`#potenzgesetze`, `#hierarchie`).
- [ ] GT-C5 · Voraussetzungen fehlen:
  - in den Aufgaben: x ≠ 0 bei negativen Exponenten;
  - in der Merktabelle: a, b ≥ 0 bei den Wurzelgesetzen, a > 0 bei rationalen Exponenten, a > 0, a ≠ 1, b > 0 beim Logarithmus.
- [ ] GT-C6 · Eingabe:
  - `5.` wird nicht verstanden.
  - `0.333` statt 1/3 → Hinweis «exakt als Bruch» statt nur «falsch».
- [ ] GT-C7 · `aria-label="<id>"` an den Feldern überschreibt das sichtbare `<label>`: Der Screenreader sagt «w», «m», «k». → `aria-label` entfernen.
- [ ] GT-C8 · `loesungTex` gibt bei Ziel `{w}` `{3}` aus. → Klammern entfernen.

## Termtrainer (`werkzeuge/termtrainer.html`)

- [ ] **TT-B1 · Koeffizienten mit Brüchen gelten als «noch kein Produkt»** (`faktorListe`, `FORM.keinProdukt`)
  - `4x^2-1` → `4(x+1/2)(x-1/2)`, und `(x/2+1)(2x+2)`.
  - → Eigener Text: «Schreib die Faktoren mit ganzen Zahlen: 4(x+½) = 2(2x+1)».
- [ ] **TT-B2 · Doppelbruch gilt als richtig gekürzt** (`formPruefen`, Zweig Bruch)
  - `3/((x+3)/1)` → ok; `(x+3)/((x-3)/4)` → ok.
  - → «fast», wenn Zähler oder Nenner noch ein `div` enthält.
- [ ] **TT-B3 · Unvereinfachte Summen in Faktoren und im gekürzten Bruch gelten als richtig**
  - `(x+5-2)(x-3)`, `3x(x+x-3)`, `x+x-3-x`.
  - → In jeder Klammer, die zu `faktorListe` beiträgt, und im Bruch zusätzlich `summenform(...) === 'ok'` verlangen.
- [ ] **TT-B4 · Häufige Fehler landen nur bei der Zahlenprobe** (`diag` ergänzen)
  - `bruchterme`: Sieben von neun Arten haben `diag: []`. Zu ergänzen:
    - Vorzeichen beim Kürzen: `(x^2-9)/(x+3)` → `x+3`;
    - Art `vz`: das Minus vergessen.
  - `faktorisieren` Art `kombi`: den ausgeklammerten Faktor vergessen (`2x^2-18` → `(x+3)(x-3)`).
  - `binome`: Bei `(x-3)^2` die Antworten `x^2+6x+9` (Vorzeichen des Mittelglieds) und `x^2-9` (Verwechslung mit der 3. binomischen Formel).
- [ ] TT-C1 · `(x+3)(x-3)2`: Die Meldung lenkt zu `^` und damit zu einem falschen Term. → «Schreib die Zahl vorne oder mit `*`; Hochzahlen mit `^`».
- [ ] TT-C2 · `x^2+5x+6/1` meldet «noch Klammern», obwohl gar keine Klammer dasteht. → Eigener Text «noch ein Bruchstrich».
- [ ] TT-C3 · Kosmetisches gilt als fertig: `1x^2`, `x^1`, `x^0`, `4xx(x+1)`. → In `glied()` als «glied» melden.
- [ ] TT-C4 · `FORM.einBruch` zeigt das Beispiel `(x-3)/(x+3)` fest an. → Neutral formulieren: «(Zähler)/(Nenner)».
- [ ] TT-C5 · `FEHLER.vietaVz`: p und q werden nicht eingeführt. → «Für x² + px + q …».
- [ ] TT-C6 · `klammern` Art `zwei`: `minusKlammer` und `nurErstes` geben denselben Wert (9 von 3000 Aufgaben). → Solche Aufgaben verwerfen.
- [ ] TT-C7 · `vzProdukt` auch bei r, s > 0, etwa `x^2+7x-10` zu `(x+2)(x+5)`: kein realistischer Fehler. → Nur bei einem negativen Faktor anbieten.
- [ ] TT-C8 · Leser:
  - `2 3x` wird zu `23x`.
  - `⁴` und `÷` werden nicht verstanden.
  - Die Vorschau zeigt beides an, Handlungsbedarf ist gering.
- [ ] TT-C9 · Am Handy liegen `^ ( ) /` auf der zweiten Symbolebene. → Kleine Tastenleiste.
- [ ] TT-C10 · Konstante `L_S` (Link «SF 1.1 Struktur-Regeln») wird nie benutzt. → Zuordnen oder entfernen.

## Rechentrainer (`werkzeuge/rechentrainer.html`)

- [ ] **RT-B1 · Gemischte Zahlen werden still falsch gelesen** (`lies()`, Leerzeichen werden entfernt)
  - `1 1/2` wird zu 11/2; bei der Lösung 3/2 → «falsch», und der Versuch zählt als Fehler.
  - → Das Muster `ganz zähler/nenner` erkennen, bevor die Leerzeichen entfernt werden. Dann entweder richtig lesen und «fast» melden («als Bruch angeben»), oder als Format ablehnen.
- [ ] **RT-B2 · «Klammer übersehen» mit unpassendem Text und Link** (`FEHLER.ohneKlammer`)
  - Der Text erklärt immer a − (b − c), erscheint aber auch hier:
    - `6·(5−6)²` → −6;
    - `(3+5)² − 11` → 17;
    - `(−3)² − (−6)` → −3; eigentlich `klammerPot`, der Code fehlt in `F_VZ`.
  - → Aufteilen in `minusKlammer` (Link g1.3) und `klammerVorrang` (Link g1.1), und `klammerPot` in `F_VZ` aufnehmen.
- [ ] **RT-B3 · Vier Vorzeichen-Vorlagen ohne Diagnose** (`VZ[7]`, `[8]`, `[9]`, `[11]`)
  - Diese Antworten ergeben nur «Noch nicht»:
    - `2·(−4) − 8·(−3)` → −32;
    - `−9 − 8·(−2)` → −25;
    - `−(−5) + 7` → 2.
  - → `minusminus` auf jeden negativen rechten Operanden ausdehnen. Dazu `neg` über einer negativen Zahl und die Regel «+(−b) als +b».
- [ ] **RT-B4 · Text von `FEHLER.vz` passt bei Summen nicht** («Zähle die Minuszeichen in Produkten …»), etwa bei `5 − 6·9` → 49. → Neutral formulieren: «Betrag stimmt, Vorzeichen nicht …».
- [ ] **RT-B5 · Bruchaufgaben mit grossen Hauptnennern**
  - `7/12 + 19/11` → 305/132.
  - 10 % der Aufgaben haben Zwischenwerte über 132. Ohne Taschenrechner ist das nicht angemessen.
  - → kgV ≤ 60 oder Nenner bis 10.
- [ ] **RT-B6 · Leerer Schritt im Lösungsweg**
  - `(−5)·(−6) + 5 = −5·(−6) + 5`: Der Schritt lässt nur die Klammer weg, und das ausgerechnet beim Thema Vorzeichen.
  - → `neg` über `num` vor der ersten Ausgabe zu einer Zahl falten.
- [ ] RT-C1 · Prozentaufgaben: `150/2` wird bei 75 % als ok angenommen. → Bei `art==='prozent'` einen Bruch mit «fast» beantworten.
- [ ] RT-C2 · Die Kürzungsmeldung zu `−2/4` lässt das Vorzeichen weg.
- [ ] RT-C3 · Basis 2 bei Potenz-Vorlagen: `potmal` ergibt denselben Wert wie die richtige Rechnung, die Diagnose fällt weg. → Basis ab 3.
- [ ] RT-C4 · Mehrdeutige Diagnosen: `12 − 7·6` → 30 heisst «Strich vor Punkt», wahrscheinlicher ist ein Vorzeichenfehler (zu prüfen). → Bei Wert = −Lösung «vz» vorziehen.
- [ ] RT-C5 · «Hauptnenner 8: beide Brüche erweitern» steht auch bei gleichen Nennern und bei ganzen Zahlen.
- [ ] RT-C6 · Triviale Faktoren `1·13/10`. → Faktoren ab 2.
- [ ] RT-C7 · Bruch → Dezimal bei Nenner 16 verlangt 31·625 im Kopf. → Division zeigen oder Nenner 16 weglassen.
- [ ] RT-C8 · Wortlaut:
  - «Nenner 25 hat nur die Primfaktoren 2 und 5» → «keinen Primfaktor ausser 2 und 5».
  - `FEHLER.vorperiode` genauer fassen.
- [ ] RT-C9 · Begriffe wie in g1.1/g1.2:
  - «Hierarchie der Operationen» statt «Reihenfolge»;
  - Variable z statt x bei Perioden;
  - kein `\frac{37.5}{100}`.
- [ ] RT-C10 · Die Themen-Schalter `.rt-opt` haben kein `aria-pressed`. Gilt wohl auch für die anderen Trainer (`.tt-opt`, `.gt-opt` …), dort prüfen.

## Strategietrainer (`werkzeuge/strategietrainer.html`)

- [ ] **ST-B1 · Einsetzverfahren: «es entstehen Brüche» stimmt oft nicht** (`REGELN.s_sys`, Vorlage `sNN`)
  - `6x + 6y = −24` lässt sich zu `x + y = −4` kürzen, und dann entstehen keine Brüche. Betrifft 36 % der sNN-Aufgaben.
  - → Gleichungen mit ggT(a, b, c) = 1 erzeugen, oder in der Regel zuerst durch den ggT teilen.
- [ ] **ST-B2 · Das Additionsverfahren eliminiert immer y** (`sysAddition`)
  - `7x + 6y = 48`, `−7x + 7y = −35` → «7·I − 6·II» statt I + II.
  - → Die Variable mit dem kleineren kgV eliminieren; den Tipp entsprechend anpassen.
- [ ] **ST-B3 · Faktorisieren bei x² + 7 = 0 gilt als «erlaubt»** (`REGELN.q_x2`)
  - Die Rückmeldung legt nahe, eine Summe zweier Quadrate lasse sich zerlegen.
  - → Bei n < 0 mit ✗ werten, mit der Begründung aus `q_rein`.
- [ ] ST-C1 · `x² = 21/2` → ✗ «Hier stehen keine Brüche». → Eigener Text: «Der Bruch ist nur eine Zahl — Wurzel ziehen».
- [ ] ST-C2 · `bruch_gl`: «Klammern auflösen» und «durch die Zahl vor x teilen» gelten als ≈, obwohl es weder Klammern noch eine Zahl vor x gibt. → ✗ mit «Hier stehen keine Klammern».
- [ ] ST-C3 · Mitternachtsformel uneinheitlich bewertet:
  - mal ✗, mal ≈, wenn rechts nicht 0 steht;
  - ≈ bei `x² − 6x + 9 = 0`, aber ✓ bei `x² − 5x + 6 = 0`.
  - → Einheitlich machen.
- [ ] ST-C4 · Merkkasten «teilen bei gemeinsamem Faktor» gegen Regel «teilen kommt am Schluss» bei linearen Gleichungen. → Den Merkkasten auf quadratische Gleichungen einschränken.
- [ ] ST-C5 · «lässt sich nicht in Faktoren zerlegen» bei `3x² + 3`: 3(x² + 1) ist eine Zerlegung. → «nicht weiter in Klammern mit x».
- [ ] ST-C6 · Ausklammern lässt einen Zahlfaktor stehen: `x(2x − 4)` statt `2x(x − 2)`.
- [ ] ST-C7 · «Ausmultiplizieren» im ersten Schritt sagt «damit wärst du wieder am Anfang». → ✗ mit eigenem Text.
- [ ] ST-C8 · «Durch x teilen»: Die Begründung «x = 0 geht verloren» steht auch, wo 0 gar keine Lösung ist. → «Dann steht x im Nenner — das hilft nicht.»
- [ ] ST-C9 · Wortlaut und Verweise:
  - Bei Gleichungen heisst der Schritt «Binom» bzw. «faktorisieren». → Die Nummer der binomischen Formel nennen, wie bei Termen.
  - In der Einleitung fehlen Verweise auf s3.1 und s2.2a.

## Einheitskreistrainer (`werkzeuge/einheitskreistrainer.html`)

- [ ] **EK-B1 · Rückmeldung beim Umrechnen passt nicht** (`FEHLER.sonst`)
  - Der Text «Quadrant, Referenzwinkel, Vorzeichen» erscheint auch bei Grad ↔ Bogenmass.
  - → Eigener Text für `umrechnen`: «Faktor π/180° bzw. 180°/π».
- [ ] **EK-B2 · Richtige Eingabe wird falsch gelesen** (`liesRad`: `*` wird entfernt)
  - `pi/6*5` wird als π/65 gelesen und als falsch gewertet.
  - `pi*5/6` gilt als «unverständlich».
  - → `*` als Produkt lesen.
- [ ] EK-C1 · Intervall «zwischen 0 und 360°». → Wie in g5.4/g5.5: \([0°;\,360°[\) bzw. \([0;\,2\pi[\).
- [ ] EK-C2 · `FEHLER.umkehrEine` sagt «Jeder Wert zwischen −1 und 1 …», trifft beim Tangens aber nicht zu. → Eigener Text: «zweimal, im Abstand 180°».
- [ ] EK-C3 · «Vom Wert zum Winkel»: Wer die Lösungsmenge der anderen Funktion anklickt (sin/cos vertauscht), wird nicht erkannt.
- [ ] EK-C4 · Tangens wie Sinus gespiegelt (tan = 1 → 45°, 135°) bekommt «Vorzeichen beim Rückweg». → Eigener Code für die falsche Symmetrie.
- [ ] EK-C5 · Zwei Fehler auf einmal, nur einer wird genannt: sin 30° → −√3/2. → «… und das Vorzeichen» ergänzen.
- [ ] EK-C6 · Die Herleitung beim Tangens zeigt nur das Vorzeichen. → Zeile tan = sin/cos ergänzen.
- [ ] EK-C7 · Palette bei 360 px (4 Spalten): Die Paare ±Wert fallen auseinander, «nicht definiert» steht mitten in der Palette.
- [ ] EK-C8 · Skizze bei Achsenwinkeln: «P» und «sin» überdecken sich, «cos» steht am Ursprung. → Beschriftung einer Strecke der Länge 0 weglassen.
- [ ] EK-C9 · Umrechnungsweg ohne Gradzeichen («150 · π/180°»); bei negativen Winkeln steht \(\frac{-30\pi}{180}\).
- [ ] EK-C10 · `FEHLER.nd`: Der Gedankenstrich sieht gerendert aus wie ein Minus. → Doppelpunkt.
- [ ] EK-C11 · Ohne Diagnose:
  - Grad statt Bogenmass (Eingabe 150);
  - π vergessen (0.8333).
  - `kehr` erkennt 6π bei 30°, das passt nicht zum Text «Faktor umgedreht».
- [ ] EK-C12 · Tastatur am Kreis: Der Hinweis «Leertaste wählt, Enter prüft» fehlt. Zu prüfen: Die Trefferflächen von Punkten im Abstand von 15° berühren sich.
- [ ] EK-C13 · «Vom Wert zum Winkel»: Die Herleitung hat keine Skizze mit den zwei symmetrischen Punkten.

## Notationstrainer (`werkzeuge/notationstrainer.html`)

Alle 110 Karten sind mit `python3` nachgerechnet und stimmen. Die Konventionen passen zu STYLEGUIDE §2.7 und g1.2 (0 ∈ ℕ).

- [ ] **NT-B1 · «Genau so» lässt richtige Antworten durchfallen** (Anleitung, Z. 217)
  - Gleichwertige Schreibweisen zählen als «Noch nicht», etwa:
    - d1: `{x ∈ ℝ | x ≠ 2}`;
    - u10, u12: `ℝ \ ]−2; 2[`;
    - beschreibende Form bei u4, u6, un3, uz3, u16.
  - → Regel: «richtig und gleichwertig». Wo eine bestimmte Form geübt wird, sie in der Frage verlangen. Bei den betroffenen Karten «Ebenso richtig» ergänzen.
- [ ] **NT-B2 · Richtige Schreibweisen stehen als «Stolperfalle» da** (d2 Z. 318, d8 Z. 349, dn4 Z. 367)
  - `ℝ \ {−4} \ {0}` und `ℤ \ {0.5}` sind korrekt, nur umständlich.
  - Die Begründung bei d8 ist nicht schlüssig.
  - → Im Stil von d5 formulieren («nicht falsch, aber unnötig»), oder nach `weg` verschieben.
- [ ] NT-C1 · Die Live-Anzeige auf **g2.1** (Z. 466, 1548–1551) schreibt `[g; ∞[` ohne «+». Der Trainer und STYLEGUIDE §2.7 schreiben «+∞». → g2.1 angleichen.
- [ ] NT-C2 · Einzelne Filterkombinationen haben nur 1–2 Karten, etwa ℚ bei Ungleichungen, Schreibweisen und Systemen. Dann kommt dieselbe Karte immer wieder. → Karten ergänzen.
- [ ] NT-C3 · Leertaste auf «Kartei zurücksetzen» dreht die Karte um. → Den Knopf vom Handler ausnehmen.
- [ ] NT-C4 · uq1: «Aufzählen geht nicht (… unendlich viele)» ist ungenau, ℚ ist abzählbar. Optional: «kein ‹nächster› Bruch».

---

## Reihenfolge für die Umsetzung

Zuerst die B-Befunde, nach Wirkung geordnet:
1. **Was Lernende als Fehler gezählt bekommen, obwohl richtig:** RT-B1, EK-B2, NT-B1.
2. **Falsches Etikett:** GT-B1–B4, RT-B2, RT-B4, EK-B1.
3. **Falsches als richtig angenommen:** TT-B2, TT-B3.
4. **Stoffzuordnung GF/SF:** GT-B5. Betrifft auch die Bausteine in g1.4 und s1.2.
5. **Strategie und Didaktik:** ST-B1–B3, TT-B1, TT-B4, RT-B3, RT-B5, RT-B6, GT-B6, NT-B2.

Die C-Punkte je Trainer gesammelt in einem Durchgang erledigen.
