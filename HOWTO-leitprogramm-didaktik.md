# HOWTO — ein Leitprogramm didaktisch aufbauen

Richtlinie für Claude. Gilt für **mathe.begreifbar.ch und physik.begreifbar.ch**.
Ergänzt `HOWTO-leitprogramme.md`: Dort steht, wie eine Leitprogramm-Datei technisch
ins Repo kommt. Hier steht, **was hineingehört und in welcher Reihenfolge**, wenn ein
Leitprogramm zu einer bestehenden Themenseite mit bestehenden Animationen und Clips
entsteht.

Entstanden am 30.09.2026 aus dem Vergleich von vier Paaren (Mathe: quadratische
Gleichungen, Gleichungssysteme; Physik: 5.2/5.3 Wärmelehre, 6.2 Elektrizität). Jede
Regel unten steht für einen Befund aus diesem Vergleich.

---

## 1 · Grundsatz: eine Quelle, zwei Wege

| | Themenseite | Leitprogramm |
|---|---|---|
| Rolle | Referenz: nachschlagen, erkunden, im Unterricht zeigen | Geführter Pfad: selbstständig erarbeiten, nachholen, Fernunterricht |
| Umfang | ganzes Lerngebiet nach RLP | der **Kern**, ausdrücklich abgegrenzt |
| Reihenfolge | nach Sachlogik, springbar | linear, jeder Schritt baut auf dem vorigen auf |
| Animationen | offen, mehrere Regler | Erkundungsauftrag mit einer Frage |
| Übungen | Mini-Checks, Aufgaben | Vortest, Selbsttests mit Punkten, Gesamttest |

**Die Themenseite ist die fachliche Wahrheit.** Begriffe, Notation, Vorzeichenkonventionen,
Achsen, Konstanten, Stoffwerte und Merksätze übernimmt das Leitprogramm von dort und
erfindet nichts Eigenes. Variation zwischen den beiden Spuren ist erlaubt, wenn sie eine
Funktion hat (anderes Format, weniger Regler, anderer Kontext). Zufällige Abweichung
ist ein Fehler.

**Prüfkriterium für jede Abweichung:** Lässt sich in einem Satz sagen, *warum* das
Leitprogramm es anders macht? Ja → bleibt, und der Satz steht als Kommentar im Code.
Nein → angleichen.

---

## 2 · Vor dem Schreiben: Bestandsaufnahme (Pflicht)

Aus Themenseite, Clips und Styleguide eine **Planungstabelle** bauen und dem
Auftraggeber vorlegen, **bevor** eine Zeile HTML entsteht:

```
Kapitel | Lernziel («Du …») | Clip(s) | Animation (Anker) | Beispiel aus Themenseite | Häufiger Fehler | Minuten
```

Dazu drei Listen:

1. **Kern / Vertiefung / bewusst weggelassen.** Was weggelassen wird, steht später im
   Leitprogramm als «Nicht in diesem Leitprogramm → Themenseite, Abschnitt …».
2. **Konventionen der Themenseite**, die im Leitprogramm vorkommen werden: Fachbegriffe
   (wie heisst welche Form?), Vorzeichenkonventionen, Achsen, Einheiten, Konstanten,
   Lösungsmengen-Notation. Abgleich mit `STYLEGUIDE.md`.
3. **Widersprüche in der Themenseite selbst** (Text gegen eigene Clips, Tabelle gegen
   Mini-Check). Diese **nicht ins Leitprogramm übernehmen**, sondern melden und zuerst in
   der Themenseite entscheiden lassen. Ein Leitprogramm auf einer widersprüchlichen
   Quelle erbt den Widerspruch oder erzeugt einen neuen.

Beispiele für Befunde aus Liste 2 und 3:

- Mathe g2-2b nennt `x² + px + q = 0` «Normalform» und `ax² + bx + c = 0` «allgemeine
  Form». Das Leitprogramm nannte `ax² + bx + c = 0` «Normalform».
- «Produkt und Summe» beim Faktorisieren: Clip und Leitprogramm meinen die Zahlen in den
  Klammern (Summe = b), der Themenseitentext teils die Lösungen (Summe = −p). Beides ist
  richtig, aber im selben Satzbau führt es zu Vorzeichenfehlern. Eine Konvention wählen.
- Physik 6.2: U-I-Kennlinie einmal U über I, einmal I über U, mit gegenteiligem Merksatz.

---

## 3 · Umfang und Zeit

- **Eine Lektion = 45 Minuten.** Die Minutenangaben pro Kapitel werden addiert, die Summe
  bestimmt die Lektionenzahl im Kopf. «Angelegt für zwei Lektionen» bei 130 Minuten
  Kapitelzeit ist falsch.
- **Zielgrösse: 2–3 Lektionen.** Bei mehr als 4 Lektionen in zwei Leitprogramme teilen
  (Vorbild Physik: «Widerstand, Leistung, Energie» und «Schaltungen berechnen»).
- **3–5 Kapitel plus Vorwissen und Gesamttest.** Ein Kapitel = eine Idee, höchstens
  30 Minuten.
- Der Kern ist das, was ohne Leitprogramm in der Prüfung fehlen würde. Parameter,
  Spezialfälle, zweite Methoden gehören in «Vertiefung» oder auf die Themenseite.

---

## 4 · Aufbau

```
Kopf          Titel · ein Satz Standfirst · Lerngebiet (RLP) · Lektionen
Ablauf        Kapitelliste nach Lektionen, Fortschrittszähler
So arbeitest  Clip → Text mitrechnen → Selbsttest ohne Lösung → abhaken
Kapitel 0     Vorwissen: kurze Klärung + Vortest (Verweis auf Vorwissens-LP/Themenseite)
Kapitel 1…n   je: Lernziel · Clip · Kerntext · Beispiel · Häufiger Fehler ·
              [Erkundung] · Selbsttest · «Mehr dazu»-Link
Gesamttest    Teile A/B/C ↔ Kapitel · Punkteschlüssel
Einschätzung  Punktebereiche → konkrete Rückverweise auf Kapitel
Weiter        nächstes Leitprogramm · Themenseite für die Vertiefung
```

### Innerhalb eines Kapitels

1. **Lernziel** als ein Satz in Du-Form: «Du löst …, erkennst …, begründest …».
2. **Clip zuerst** (Gedankengang), dann der Text, der ihn vollständig macht.
3. **Kerntext kurz.** Merkkasten mit **demselben Wortlaut** wie auf der Themenseite,
   wo es einen gibt.
4. **Ein durchgerechnetes Beispiel** mit Zwischenschritten (Schritt-Tabelle). Möglichst
   dasselbe Beispiel wie im Clip davor, sonst im Text sagen, dass es ein anderes ist.
5. **Häufiger Fehler**, übernommen aus der Themenseite, wenn vorhanden.
6. **Erkundung** (optional, siehe §6).
7. **Selbsttest** (siehe §7).
8. **«Mehr dazu»**: ein Link auf den passenden Abschnitt der Themenseite.

---

## 5 · Clips

- **Nur bestehende Clips verwenden**, dieselben Dateien wie auf der Themenseite. Keine
  fast gleichen Varianten mit anderen Zahlen herstellen.
- **Themenclips** (Alltagsfrage, Verfahren, «Zum Mitnehmen») passen ins Leitprogramm.
- **Animations-Clips** (`*-anim-*`, «In der Animation hast du …») setzen voraus, dass die
  Animation vorher bedient wurde. Nur nach einer Erkundung (§6a) verwenden, sonst weglassen.
- **Clips anderer Themenseiten** sind im Vorwissen ausdrücklich erwünscht (z. B.
  `g1-3-faktorisieren-strategie` vor den quadratischen Gleichungen).
- **Zahlen im Clip = Zahlen im Text direkt danach.** Widerspricht eine Simulation im
  selben Kapitel ihrem Clip (Physik: Heizkurve 0.1 kg im Clip, 1.0 kg in der Simulation),
  wird die Simulation angepasst, nicht der Clip. Neu vertonen ist teuer.
- Fehlt für einen Kernschritt ein Clip, das melden. Nicht ohne Auftrag einen neuen bauen.

---

## 6 · Animationen und Simulationen

Entscheidung pro Kapitel, in dieser Reihenfolge:

**a) Eine Animation der Themenseite passt → Erkundungsauftrag, kein Code-Kopie.**
Kasten «🔍 Erkunden» mit Link auf den Anker (`../grundlagen/<seite>.html#anim-…`,
neuer Tab) und einem **konkreten Auftrag**: was einstellen, was beobachten, was
notieren. Die Frage dazu kommt im Selbsttest wieder. Danach darf der passende
`*-anim-*`-Clip folgen. Höchstens eine Erkundung pro Kapitel.

> 🔍 Öffne die Animation *Flächenmodell* auf der Themenseite. Stell p = 6 ein und klick
> bis Schritt 4. Welche Fläche fehlt zum grossen Quadrat? Ändert sie sich, wenn du nur x
> verschiebst? Notiere beides.

**b) Das Leitprogramm braucht eine geführte Variante** (ein Regler, eine Aussage,
eingebettet) → kleine SVG-Simulation im Leitprogramm. Dann gilt verbindlich:
- Achsen (was waagrecht, was senkrecht), Variablennamen, Einheiten, Konstanten und
  Stoffwerte **identisch zur Themenseiten-Animation**
- **Startwert = Beispiel im Text bzw. Clip** desselben Kapitels
- Merksatz in der Bildlegende gleichlautend wie in der «Erkenntnis» der Themenseite
- der Unterschied zur Themenseiten-Animation als Ein-Satz-Kommentar im Code
- beide Reglerenden gegen nachgerechnete Werte prüfen

**c) Reine Rechentechnik ohne Anschauung** → keine Animation. Das ist erlaubt, aber
mindestens das Kernkapitel sollte eine Erkundung haben. Die Mathe-Leitprogramme haben
bisher keine, obwohl die Themenseiten dafür passende haben (Flächenmodell,
Lösungsfälle, Vorzeichenmuster, Geradenbüschel).

---

## 7 · Selbsttests und Gesamttest

- **Vortest** prüft nur Voraussetzungen, 8–13 Punkte, mit Verweis bei Lücken.
- **Selbsttest je Kapitel**, 7–16 Punkte, 3–6 Aufgaben, 2–5 Punkte pro Aufgabe. Mischung:
  - Rechnen (Verfahren anwenden)
  - Erkennen/Entscheiden («Welcher Fall? Welches Verfahren?»)
  - Begründen (mindestens eine «Warum»-Frage)
- **Keine Selbsttest-Aufgabe ist das durchgerechnete Beispiel.** Gleicher Typ, andere
  Zahlen. In den beiden Mathe-Leitprogrammen wiederholt rund ein Drittel der
  Selbsttest-Aufgaben wörtlich ein Beispiel darüber (Gleichungssysteme 1a–1d: alle vier
  Verfahrensbeispiele). Damit wird genau das Wiedererkennen geprüft, vor dem
  «So arbeitest du» warnt.
- **Lösung aufklappbar**, darunter optional eine Zeile zur typischen Fehlerquelle.
- **Gesamttest** 20–25 Punkte, rund 20 Minuten, in Teile gegliedert, die den Kapiteln
  entsprechen. Neue Zahlen, keine Wiederholung aus den Selbsttests. Hilfsmittel
  ausdrücklich angeben.
- **Selbsteinschätzung** mit Punktebereichen, die auf **bestimmte Kapitel** zurückverweisen
  (Teil A → Kapitel 1 …), nicht nur «wiederholen».
- Punkte summieren (Kopf des Tests = Summe der Aufgaben), Minuten summieren (§3).

---

## 8 · Notation und Fachsprache (Kurzliste)

Immer nach `STYLEGUIDE.md`. Diese Punkte sind beim Vergleich schiefgegangen:

| Was | Regel |
|---|---|
| Lösungsmenge | `\mathbb{L}`, nie ein einfaches L (§2.11) |
| leere Menge | `\mathbb{L} = \{\,\}` |
| Elemente einer Menge | Semikolon: `\{-3;\ 3\}` (auf den Themenseiten teils Komma, dort nachziehen) |
| Lösung eines Systems | als Menge: `\mathbb{L} = \{(2 \mid 3)\}`, nicht nur «Lösung (2 \| 3)» |
| Parametrisierte Menge | Doppelpunkt: `\{(x \mid 2x-3) : x \in \mathbb{R}\}`; der senkrechte Strich ist schon Koordinatentrenner |
| Intervalle | `]a;\, b[`, Klammer nach aussen = Grenze nicht dabei |
| Zahlen | Dezimalpunkt; Brüche, wo die Themenseite Brüche verwendet |
| Fachbegriffe | den Begriff der Themenseite einführen und verwenden (z. B. «identische Geraden», nicht nur «dieselbe Gerade») |
| Methodenwahl | Verwendet das Leitprogramm eine andere Hauptmethode als die Themenseite (Ungleichungen: Parabelskizze statt Vorzeichenmuster), beide nennen und die Wahl in einem Satz begründen |
| Physik | Konstanten und Stoffwerte aus der Tabelle der Themenseite (c_Wasser = 4182, 273.15 K); Kennlinien I über U |

Sprache: Du-Form, kurze Sätze, Schweizer Rechtschreibung (ss), kein «wir».

---

## 9 · Verknüpfung

- **Themenseite → Leitprogramm:** Kasten direkt nach den Lernzielen: «🧭 Lieber geführt?
  Leitprogramm *…* (≈ n Lektionen, mit Vortest und Gesamttest)».
- **Leitprogramm → Themenseite:** «Mehr dazu»-Link am Ende jedes Kapitels und ein
  Abschlusskasten mit dem, was bewusst weggelassen wurde.
- **Leitprogramm → Leitprogramm:** Vorwissen verweist auf das vorausgehende, der Schluss
  auf das folgende.
- Physik 6.2 macht das in beide Richtungen, Physik 5.2/5.3 nur vom Leitprogramm zur
  Themenseite, Mathe g2-2b/g2-3 bisher in keine.

---

## 10 · Abnahme vor dem Commit

1. Jede Lösung nachrechnen, am besten mit einem kurzen Skript. Keine Zahl ungeprüft.
2. Punkte- und Minutensummen stimmen mit Kopf und Ablauf überein.
3. Konventions-Grep gegen die Themenseite: Fachbegriffe, `\mathbb{L}`, Konstanten,
   Achsenbeschriftungen.
4. Clip-Zahlen gegen Text und Simulationsstartwerte desselben Kapitels.
5. Links in beide Richtungen vorhanden; Anker der Erkundungen existieren.
6. Kein Selbsttest wiederholt ein Beispiel, kein Gesamttest wiederholt einen Selbsttest.
7. Technische Prüfungen nach `HOWTO-leitprogramme.md` (Pre-Flight, MathJax, 360/1280 px,
   hell/dunkel).
8. Kurzer Bericht an den Auftraggeber: was bewusst anders ist als auf der Themenseite und
   warum; welche Widersprüche in der Themenseite gefunden wurden.

---

## Nicht tun

- Keine Animation der Themenseite in das Leitprogramm kopieren. Verlinken (§6a) oder eine
  bewusst reduzierte Variante mit identischen Konventionen bauen (§6b).
- Keine neuen Beispiele erfinden, wenn die Themenseite ein passendes hat. Gemeinsame
  Beispiele sind Wiedererkennung, die gewollt ist.
- Keine Inhalte, die weder auf der Themenseite noch im RLP stehen. Geht das Leitprogramm
  weiter als die Themenseite, zuerst die Themenseite ergänzen.
- Nicht still angleichen, wenn die Themenseite selbst widersprüchlich ist. Melden.
