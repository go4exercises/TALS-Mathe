# TODO — Animations-Audit Schwerpunktfach

**Stand: 1. August 2026.** Vollprüfung aller interaktiven Canvas-Animationen im
Schwerpunktfach (23 Seiten). Ersetzt kein früheres Audit — dies ist die erste Prüfung dieses Bereichs.

> **Vollständig abgearbeitet am 2. August 2026.** Alle 98 Punkte aus AN-S01,
> AN-S02, AN-S02b, AN-S04 und AN-S05 sind erledigt; AN-S03 war von Anfang an
> ohne Befund. Einer der Punkte (AN-S04g) erwies sich bei der Nachprüfung als
> bereits behoben, sieben Punkte aus AN-S02b sind als «bewusst ohne Term»
> entschieden — beides ist an Ort und Stelle begründet. Jede Änderung ist im
> Browser bei 1280 **und** 360 px gerendert und im Bild gesichtet worden.

## Wie geprüft wurde

Drei Messungen im Browser über alle Seiten, dazu eine Sichtung der gerenderten
Startbilder:

| Messung | Was sie findet |
|---|---|
| **Hinweispaar** | Hat die Animation das laut STYLEGUIDE §10 verbindliche Paar «👁 Worauf achten?» / «💡 Erkenntnis»? Zuordnung über die `.widget-titelzeile` zum folgenden Canvas. |
| **Term im Bild** | Steht im Canvas selbst irgendwo eine Funktionsgleichung oder ein Wert-Term (`f(x)`, `y =`, `a =`, `sin`, `lg`)? Achsenzahlen zählen nicht. |
| **Reaktionstest** | Verändert das Betätigen eines Bedienelements das Canvas-Bild oder die Live-Werte? Findet tote Regler und Knöpfe. |

**Nicht** Gegenstand dieses Audits: Lesbarkeit und Platzierung der Beschriftungen.
Die sind am 30./31.07. separat überarbeitet worden (228 → 4 gemessene Konflikte);
Ergebnis und Restbestand stehen in `_intern/BERICHT-beschriftungen-animationen.md`.

**Grenzen:** Die Sichtung erfasst die **Startposition** bei 1280 px. Was erst beim
Ziehen eines Reglers oder in einer anderen Preset-Stellung sichtbar wird, ist nur
stichprobenweise geprüft.

**Stand 01.08.2026: die Sichtung ist vollständig.** Alle 98 sichtbaren Animationen
sind einzeln im Bild beurteilt (AN-S04 für s1-1…s3-2b, AN-S05 für den Rest).
Acht weitere Canvas liegen in zugeklappten Bereichen und wurden nicht erfasst.

---

## Bestand

| | Anzahl |
|---|---:|
| Canvas gesamt | 98 |
| davon interaktiv (mit Bedienelement) | 94 |
| **ohne Hinweispaar** | **16** → **0** (erledigt 02.08.) |
| **ohne Term/Formel im Bild** | **73** |
| davon ganz ohne Inhaltstext (nur Achsenzahlen) | 31 — 17 im Lehrteil (erledigt 02.08.), 14 in Aufgaben |
| tote Regler | **0** |

---

## AN-S01 — Hinweispaar fehlt auf 16 interaktiven Animationen · **P2**

Der STYLEGUIDE führt das Paar «Worauf achten?» / «Erkenntnis» als Pflicht je
interaktiver Animation. Tatsächlich hat es nur ein Teil. Ohne den Hinweis bleibt
offen, *worauf* beim Schieben zu achten ist und *was* dabei herauskommen soll —
genau die Kopplung, die eine Animation didaktisch trägt.

> **Erledigt am 02.08.2026.** Alle 16 Paare sind ergänzt. Die Liste wurde vorher am
> Quelltext gegengeprüft (jede `.widget-titelzeile` gehört zum nächsten `<canvas>`
> darunter): alle 16 Einträge waren korrekt, kein Fehlbefund.



**`s2-2a-potenz-wurzel-rationale-gleichungen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s2-2b-exponential-logarithmische-gleichungen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s2-2c-betrag-polynom-ungleichungen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-1-grundlagen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-2a-potenzfunktionen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-2b-wurzelfunktionen`**
- [x] `wz-canvas` · §typen — Hinweispaar ergänzt (02.08.2026)
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-3-polynomfunktionen`**
- [x] `a2-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-4a-exponentialfunktionen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-4b-logarithmusfunktionen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-5-trigonometrische-funktionen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s3-6-betragsfunktionen`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s4-1-grundlagen`**
- [x] `cv-a1` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s4-3a-vektorbegriff-komponenten`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s4-3b-skalarprodukt`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)

**`s4-3c-geraden`**
- [x] `a1-canvas` · §aufgaben — Hinweispaar ergänzt (02.08.2026)


---

## AN-S02 — Kurve ohne Term im Bild: 17 Animationen im Lehrteil · **P2**

Diese Animationen zeigen im Canvas **gar keinen** Inhaltstext — nur Achsenzahlen.
Man sieht eine Kurve oder Figur, erfährt im Bild aber nicht, welche. Der Term steht
jeweils daneben im Fliesstext oder in der Reglerzeile; im Bild fehlt die Kopplung
«Parameter → Darstellung → Formel», die der STYLEGUIDE als Kern der Widgets nennt.

Vorschlag je Fall: den aktuellen Term als Beschriftung an die Kurve setzen
(`beschriftung()`, §2.9) — dieselbe Farbe wie die Kurve, am rechten Kurvenende.

> **Erledigt am 02.08.2026.** Alle 17 haben jetzt den Term im Bild, in der Farbe
> der zugehörigen Kurve und mit `beschriftung(… halo:true, W, H)` gesetzt. Das
> rechte Kurvenende taugte nur selten als Ort — bei Exponential-, Logarithmus-
> und Hyperbelkurven verlässt es das Bild. Regelfall wurde deshalb die freie
> obere linke Ecke; wo die Kurve dort liegt (`cv-lot`), steht der Term unten links.
> Drei Widgets haben mehr als den Term bekommen: `vz-canvas` die Legende
> «f(x) > 0» / «f(x) < 0» direkt an den gefärbten Achsenabschnitten (das war
> zugleich AN-S05a), `qd-canvas` die Raumdiagonalformel samt Wert und die
> Kantenmasse (AN-S05e), `ke-canvas` die Formeln für Mantellinie und Volumen.
> Geprüft: Rendercheck aller 17 Canvas bei 1280 **und** 360 px, Bilder gesichtet,
> Beschriftungskollisionen in sechs Fällen nachträglich entzerrt.

**Nicht** in dieser Liste: 14 Aufgaben-Grafiken ohne Term. Dort ist das
Weglassen oft gewollt — der Term ist die gesuchte Antwort. Vor einer Änderung je
Aufgabe entscheiden.


**`s2-2b-exponential-logarithmische-gleichungen`**
- [x] `gl-canvas` · §darstellungen — Term ergänzt (02.08.2026)

**`s2-2c-betrag-polynom-ungleichungen`**
- [x] `vz-canvas` · §typen — Term ergänzt (02.08.2026)

**`s3-1-grundlagen`**
- [x] `st-canvas` · §darstellungen — Term ergänzt (02.08.2026)
- [x] `ug-canvas` · §theorie — Term ergänzt (02.08.2026)

**`s3-2a-potenzfunktionen`**
- [x] `dr-canvas` · §darstellungen — Term ergänzt (02.08.2026)
- [x] `hy-canvas` · §theorie — Term ergänzt (02.08.2026)
- [x] `pa-canvas` · §typen — Term ergänzt (02.08.2026)

**`s3-3-polynomfunktionen`**
- [x] `lf-canvas` · §darstellungen — Term ergänzt (02.08.2026)
- [x] `gv-canvas` · §typen — Term ergänzt (02.08.2026)

**`s3-4a-exponentialfunktionen`**
- [x] `dr-canvas` · §darstellungen — Term ergänzt (02.08.2026)
- [x] `tr-canvas` · §theorie — Term ergänzt (02.08.2026)

**`s3-4b-logarithmusfunktionen`**
- [x] `tr-canvas` · §theorie — Term ergänzt (02.08.2026)

**`s3-5-trigonometrische-funktionen`**
- [x] `ek-kreis` · §darstellungen — Term ergänzt (02.08.2026)

**`s3-6-betragsfunktionen`**
- [x] `uk-canvas` · §typen — Term ergänzt (02.08.2026)

**`s4-2a-prismen-zylinder`**
- [x] `qd-canvas` · §definition — Term ergänzt (02.08.2026)

**`s4-2b-pyramiden-kegel-stuempfe`**
- [x] `ke-canvas` · §darstellungen — Term ergänzt (02.08.2026)

**`s4-3c-geraden`**
- [x] `cv-lot` · §theorie — Term ergänzt (02.08.2026)


---

## AN-S02b — Term im Bild fehlt, aber es gibt andere Beschriftung: 42 weitere

Diese tragen zwar Text im Bild (Achsentitel, Punktnamen, Einheiten), aber keinen
Term. Schwächerer Fall als AN-S02 — je Animation entscheiden, ob der Term
etwas beiträgt.

> **Erledigt am 02.08.2026 — je Fall entschieden.** 35 der 42 haben jetzt den
> Term im Bild, 7 bleiben bewusst ohne.
>
> **Term ergänzt** überall dort, wo die Formel die Aussage des Widgets *ist*:
> die Typen-Visualisierungen (`typ-canvas`, beide `ty-canvas`, `wz-canvas` —
> letzteres bisher nur in der Sammelansicht «alle drei» beschriftet), die
> Transformations-Labore (`tr-canvas` auf s3-1/s3-6, `tf-canvas`), die
> Anwendungsgraphen mit Funktionsterm (`sw`, `al`, `dn`, `ba`, `bk`, `ek`,
> `c14`, `sc` auf s3-3, `ab`), die Scheinlösungs-Grafiken (`cv-sl`, `sc` auf
> s2-2a — dort beide Seiten der Gleichung benannt), das Toleranzband (`to`),
> die Zylinderformeln (`zy`), die Geraden-Parameterform (`dr` auf s4-3c) und
> die Dachebene (`da`). Die übrigen waren durch AN-S02, AN-S04 oder AN-S05
> schon versorgt.
>
> **Bewusst ohne Term** — dort trägt er nichts bei oder stünde im Weg:
> `cv-zehnerpot` (es wandert der Dezimalpunkt, es gibt keinen Funktionsterm),
> `rr-rad` (die Rad-Szene selbst; \(h(t)\) steht seit AN-S05k im Graphen
> daneben), `s3-5 a1-canvas` (Aufgabe — der Term ist die gesuchte Antwort),
> `sb-canvas` (Schrägbild-Geometrie; die Bildlänge steht in der Reglerzeile),
> `fl-canvas` und `ad-canvas` (Vektorszenen: die Pfeile sind einzeln benannt,
> ein Term daneben verdoppelt nur die Komponentenanzeige) und `cv-haus`
> (Schrägbild; der Durchstosspunkt steht in der Reglerzeile, die Ebenen-
> gleichung im Grundriss-Widget `da-canvas` derselben Seite).
>
> Geprüft: Rendercheck aller 22 geänderten Canvas bei 1280 **und** 360 px,
> Bilder gesichtet, elf Beschriftungen danach entzerrt.


**`s1-1-grundlagen`**
- [x] `sw-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `cv-pruefstand` · §typen — Term im Bild (02.08.2026)

**`s1-2-potenzen`**
- [x] `ex-canvas` · §rationale-exponenten — Term im Bild (02.08.2026)
- [x] `cv-zehnerpot` · §hierarchie — **bewusst ohne Term** (02.08.2026)

**`s2-1-grundlagen`**
- [x] `wa-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `cv-sl` · §definition — Term im Bild (02.08.2026)

**`s2-2a-potenz-wurzel-rationale-gleichungen`**
- [x] `sw-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `sc-canvas` · §darstellungen — Term im Bild (02.08.2026)

**`s2-2b-exponential-logarithmische-gleichungen`**
- [x] `al-canvas` · §einstieg — Term im Bild (02.08.2026)

**`s2-2c-betrag-polynom-ungleichungen`**
- [x] `to-canvas` · §einstieg — Term im Bild (02.08.2026)

**`s3-1-grundlagen`**
- [x] `dn-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `tr-canvas` · §typen — Term im Bild (02.08.2026)

**`s3-2a-potenzfunktionen`**
- [x] `ba-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `typ-canvas` · §typen — Term im Bild (02.08.2026)

**`s3-2b-wurzelfunktionen`**
- [x] `pe-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `wz-canvas` · §typen — Term im Bild (02.08.2026)
- [x] `tf-canvas` · §theorie — Term im Bild (02.08.2026)

**`s3-3-polynomfunktionen`**
- [x] `sc-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `cv-lt` · §typen — Term im Bild (02.08.2026)

**`s3-4a-exponentialfunktionen`**
- [x] `bk-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `ty-canvas` · §typen — Term im Bild (02.08.2026)

**`s3-4b-logarithmusfunktionen`**
- [x] `ek-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `sp-canvas` · §definition — Term im Bild (02.08.2026)
- [x] `ty-canvas` · §eigenschaften — Term im Bild (02.08.2026)
- [x] `c14-canvas` · §theorie — Term im Bild (02.08.2026)

**`s3-5-trigonometrische-funktionen`**
- [x] `rr-rad` · §einstieg — **bewusst ohne Term** (02.08.2026)
- [x] `ty-canvas` · §typen — Term im Bild (02.08.2026)
- [x] `tr-canvas` · §theorie — Term im Bild (02.08.2026)
- [x] `a1-canvas` · §aufgaben — **bewusst ohne Term** (02.08.2026)

**`s3-6-betragsfunktionen`**
- [x] `ab-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `tr-canvas` · §darstellungen — Term im Bild (02.08.2026)

**`s4-1-grundlagen`**
- [x] `sb-canvas` · §einstieg — **bewusst ohne Term** (02.08.2026)

**`s4-2a-prismen-zylinder`**
- [x] `cv-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `zy-canvas` · §darstellungen — Term im Bild (02.08.2026)

**`s4-2b-pyramiden-kegel-stuempfe`**
- [x] `fu-canvas` · §einstieg — Term im Bild (02.08.2026)
- [x] `cv-k3` · §typen — Term im Bild (02.08.2026)

**`s4-3a-vektorbegriff-komponenten`**
- [x] `fl-canvas` · §einstieg — **bewusst ohne Term** (02.08.2026)
- [x] `ad-canvas` · §darstellungen — **bewusst ohne Term** (02.08.2026)

**`s4-3b-skalarprodukt`**
- [x] `wl-canvas` · §darstellungen — Term im Bild (02.08.2026)

**`s4-3c-geraden`**
- [x] `dr-canvas` · §einstieg — Term im Bild (02.08.2026)

**`s4-3d-ebenen`**
- [x] `cv-haus` · §darstellungen — **bewusst ohne Term** (02.08.2026)
- [x] `da-canvas` · §einstieg — Term im Bild (02.08.2026)

---

## AN-S03 — Tote Bedienelemente: **keine** · geprüft, nichts zu tun

Der Reaktionstest hat jedes sichtbare Bedienelement betätigt und geprüft, ob sich
Canvas-Bild oder Live-Werte ändern. **Kein einziger toter Regler.** Drei Verdachtsfälle
haben sich bei der Einzelprüfung aufgelöst und sind hier festgehalten, damit sie
niemand erneut verfolgt:

- `g3-1` · `par-u` / `par-v` — die Zuordnung nach Bildschirmnähe hatte sie
  `lin-canvas` zugeschlagen; sie gehören zu `par-canvas`, das reagiert.
- `g5-2a` · `spez-sld-2` — wirkt nur in der Preset-Stellung «gleichschenklig»,
  nicht in der Startstellung. Bedingt, nicht tot.
- Knöpfe, die als aktives Preset erneut geklickt werden, ändern erwartungsgemäss
  nichts. Der Test meldet sie, es ist kein Defekt.

---

## AN-S04 — Befunde aus der Bildsichtung · gemischte Priorität

Aus der Durchsicht der gerenderten Startbilder. **Teilerhebung:** von den 98
sichtbaren Animationen habe ich rund ein Viertel im Bild einzeln beurteilt
(Blätter 1 und 3 des Kontaktabzugs, s1-1 bis s3-2b). Der Rest ist über die
Messungen oben erfasst, aber nicht einzeln angesehen — hier liegt der grösste
Rest an Arbeit.

- [x] **AN-S04a** `s1-1` · `cv-pruefstand` · **P3** — Die Werte stehen mit vier
  Nachkommastellen da («Differenz 12.0000», «25.0000», «13.0000»), obwohl es
  ganze Zahlen sind. Wirkt nach Maschine, nicht nach Mathematik. Auf ganzzahlige
  Anzeige umstellen, Nachkommastellen nur wo nötig.
  **Erledigt 02.08.2026:** behoben — ganzzahlige Werte ohne Nachkommastellen, Bruchteile nur wo nötig.
- [x] **AN-S04b** `s1-1` · `cv-pruefstand` · **P2** — Unter den Balken steht
  «(a+b)² = a² + b²» ohne Kennzeichnung. Das ist genau die **falsche** Gleichung,
  die das Widget widerlegen soll. Ohne Markierung (durchgestrichen, rot, «≠»)
  liest sie sich wie eine Merkformel.
  **Erledigt 02.08.2026:** behoben — die Regel steht jetzt als Behauptung da: «✗ gilt nicht» und rot durchgestrichen, gültige Regeln grün mit ✓.
- [x] **AN-S04c** `s1-2` · `ex-canvas` · **P4** — Die y-Achse ist logarithmisch
  (1/256 … 256), aber nur die x-Achse ist beschriftet («Exponent x»). Der y-Achse
  fehlt die Angabe, was sie zeigt.
  **Erledigt 02.08.2026:** behoben — die y-Achse trägt jetzt «Wert 16ˣ (log. Skala)», die x-Achse nur noch «Exponent x».
- [x] **AN-S04d** `s1-3` · `cv-rechenschieber` · **P3** — Die verschiebbare
  C-Skala läuft rechts aus dem Bild, ohne dass das angedeutet wird. Beim Schieben
  verschwinden Zahlen wortlos. Entweder Skala kürzen oder den Rand andeuten.
  **Erledigt 02.08.2026:** behoben — Verlauf nach Weiss plus «…» am rechten Rand, sobald die Zunge hinausläuft.
- [x] **AN-S04e** `s2-1` · `wa-canvas` · **P2** — Die Waage steht waagrecht, obwohl
  links «x x x + 2» und rechts 12 Kugeln liegen. Ohne Zahlenanzeige ist nicht
  ablesbar, ob die Seiten gleich sind — dasselbe Muster wie AN-11 im
  Grundlagen-Audit (`g2-1` · `uf-canvas`, dort als «faktisch tot» notiert).
  Beide zusammen anschauen.
  **Erledigt 02.08.2026:** behoben — «links: 3x + 2» / «rechts: 11» an den Schalen und darüber die Probe «mit x = 3: 11 = 11 ✓ im Gleichgewicht».
- [x] **AN-S04f** `s2-2a` · `a1-canvas` · **P3** — x-Achse von −25 bis 25, die
  Kurve liegt vollständig im rechten Viertel. Drei Viertel der Fläche sind leer.
  Skalierung an den dargestellten Bereich anpassen (STYLEGUIDE §3: aufgabenbezogen).
  **Erledigt 02.08.2026:** behoben — Fenster je Fall (−4…30 bzw. −16…4 bei √(−x)) statt fest −28…28.
- [x] **AN-S04g** `s3-1` · `ug-canvas` · **P3** — Die x-Achsenzahlen liegen in den
  grün hinterlegten Lösungsbereichen und sind dort schlecht lesbar. Die Zahlen
  nach der Flächenfüllung setzen (`zahlenOben()` aus `drawGrid`).
  **Nachgeprüft 02.08.2026: war bereits behoben.** `drawUg` ruft `drawGrid` mit
  `{zahlen:false}` und setzt am Schluss `zahlenOben()` — seit dem Beschriftungs-
  Durchgang vom 30.07. (Commit 070b84a). Im Rendercheck stehen die Zahlen mit
  weisser Freistellung über der grünen Fläche. Kein Handlungsbedarf.
- [x] **AN-S04h** `s3-2a` · `hy-canvas` · **P4** — Die Hyperbeläste laufen oben und
  unten ohne Andeutung aus dem Bild; es sieht nach abgeschnitten statt nach
  «geht weiter» aus.
  **Erledigt 02.08.2026:** behoben — Pfeilspitzen am oberen und unteren Bildrand, Austrittsstelle in geschlossener Form berechnet.
- [x] **AN-S04i** `s3-1` · `we-graph` · **P4** — «x [m]» am rechten Rand berührt die
  letzte Achsenzahl (30). Dasselbe Muster wie auf den bereits korrigierten Seiten:
  letzte Zahl weglassen, dort steht die Achsenbeschriftung.
  **Erledigt 02.08.2026:** behoben — `gridApp` lässt die letzte x-Zahl weg, wenn dort die Achsenbeschriftung steht.

### AN-S05 — Befunde aus der vollständigen Bildsichtung (01.08.2026)

Alle **98 sichtbaren Animationen** sind jetzt im Bild einzeln beurteilt (neun
Kontaktabzüge, Startposition, 1280 px). Die Sichtung von Blatt 1 und 3 steht oben
unter AN-S04; hier die Blätter 2 und 4–9.

#### Fehlende Zuordnung — man sieht etwas, weiss aber nicht was · **P2**

- [x] **AN-S05a** *(erledigt 02.08.2026 mit AN-S02)* `s2-2c` · `vz-canvas` — Die Parabel steht über einer x-Achse, auf der
  Bereiche **rot** und **grün** markiert sind. Was die zwei Farben bedeuten, steht
  nirgends im Bild. Bei einer Vorzeichentabelle ist genau das die Aussage —
  Legende «f(x) > 0» / «f(x) < 0» oder Beschriftung direkt an den Abschnitten.
- [x] **AN-S05b** `s3-3` · `cv-lt` — Zwei Kurven (blau und orange) ohne jede
  Zuordnung. Nur «y: ±27» steht dabei. Welche Kurve ist die Funktion, welche die
  Vergleichskurve? Beide benennen.
  **Erledigt 02.08.2026:** behoben — «f(x) = x³ − 4x» und «Leitterm x³ (gestrichelt)» in den Kurvenfarben.
- [x] **AN-S05c** `s3-4b` · `sp-canvas` — Spiegelung an \(y = x\) mit zwei Kurven,
  von denen keine benannt ist. Gerade hier ist die Zuordnung Exponential- ↔
  Logarithmusfunktion die ganze Aussage. Vorbild: `s3-2b` · `um-canvas`, das
  «y=x²» und «y=√x» direkt an die Kurven schreibt.
  **Erledigt 02.08.2026:** behoben — beide Kurventerme oben links, dazu «y = x» an der Winkelhalbierenden.
- [x] **AN-S05d** `s3-5` · `ek-canvas`, `ty-canvas`, `tr-canvas` — Sinus- bzw.
  Kosinuskurven ohne Angabe, welche der beiden gezeigt wird. Bei \(\sin\) und
  \(\cos\) ist die Kurvenform allein kein Unterscheidungsmerkmal, solange man den
  Startwert nicht abliest.
  **Erledigt 02.08.2026:** behoben — ek-canvas nennt die gewählte Funktion, ty-canvas beschriftet jede Kurve einzeln (bei «sin & cos» beide), tr-canvas den transformierten Term plus «gestrichelt: y = sin x».
- [x] **AN-S05e** *(erledigt 02.08.2026 mit AN-S02)* `s4-2a` · `qd-canvas` — Der Quader trägt \(a, b, c, d\), aber
  weder Zahlenwerte noch die Formel für die Raumdiagonale — obwohl das Widget
  genau davon handelt. Vergleich: `s4-1` · `cv-raumwinkel` macht es vorbildlich
  («D = 6.93», «a√2 = 5.66», «Würfel: tan φ = 1/√2»).

#### Beschriftungen, die sich berühren · **P3**

Diese Fälle liegen unterhalb der Schwelle des Beschriftungs-Audits vom 30.07.
oder entstehen erst in dieser Preset-Stellung — im Bild sind sie sichtbar:

- [x] **AN-S05f** `s3-3` · `sc-canvas` — «(2.0|352)» und «H» überlagern sich am
  Hochpunkt.
  **Erledigt 02.08.2026:** behoben — «H» über den Hochpunkt, das Trace-Label unter den Punkt.
- [x] **AN-S05g** `s4-3d` · `cv-haus` — «Dach» und «D» liegen übereinander.
  **Erledigt 02.08.2026:** behoben — «Dach» nach links versetzt, weg von der Drohnengeraden.
- [x] **AN-S05h** `s4-1` · `sb-canvas` — «Tiefe × q» sitzt auf der Würfelkante.
  **Erledigt 02.08.2026:** behoben — «Tiefe × q» rechts neben die hintere Fläche gesetzt.
- [x] **AN-S05i** `s3-6` · `ab-canvas` — «Bahnhof» berührt die gestrichelte Linie.
  **Erledigt 02.08.2026:** behoben — gestrichelte Linie endet unterhalb der Beschriftung.
- [x] **AN-S05j** `s4-3a` · `ad-canvas` — «a» und «a+b» stehen sehr eng beieinander.
  **Erledigt 02.08.2026:** behoben — Abstände vergrössert, «b» aus der Pfeilspitze heraus.

#### Term fehlt, wäre aber der Kern · **P4**

- [x] **AN-S05k** `s3-5` · `rr-canvas` — Riesenrad-Graph ohne \(h(t)\). Das direkte
  Gegenstück auf `g5-5` · `cv-rad` hat den Term am 01.08. bekommen; hier fehlt er noch.
  **Erledigt 02.08.2026:** behoben — «h(t) = 35 − 30·cos(2πt/12)» im Graphen.
- [x] **AN-S05l** `s3-2b` · `pe-canvas` — Pendelgraph ohne \(T = 2\pi\sqrt{l/g}\).
  **Erledigt 02.08.2026:** behoben — «T = 2π·√(l/g)» im Graphen.
- [x] **AN-S05m** `s4-2b` · `fu-canvas` — «Pyramide (G, h)» → «Prisma (G, h)», aber
  der Faktor \(\tfrac{1}{3}\) — die eigentliche Aussage — steht nicht im Bild.
  **Erledigt 02.08.2026:** behoben — «V(Pyramide) = ⅓ · V(Prisma)» über der Figur.
- [x] **AN-S05n** `s3-6` · `cw-canvas` — die Schnittgerade «y = 3.0» ist benannt,
  die Betragsfunktion selbst nicht.
  **Erledigt 02.08.2026:** behoben — «y = |x² − 4|» an der W-Kurve.

#### Referenz-Widgets — als Muster brauchbar

Bei der Sichtung positiv aufgefallen; wer eines der obigen Widgets nachbessert,
findet hier die Vorlage: `s4-1 cv-raumwinkel` (Winkel, Diagonale und Rechenweg im
Bild) · `s4-2a cv-canvas` (Cavalieri mit «Querschnitt π·2² — unverändert») ·
`s4-2b cv-k3` (Anteile ×k, ×k², ×k³ als Balken) · `s4-2c cv-kugelteil` ·
`s4-3b wl-canvas` («Schatten zeigt in Richtung a») · `s4-3c cv-ws` («windschief»,
«grau gestrichelt: Schatten von h») · `s3-4b ll-canvas` (lineare und logarithmische
Skala nebeneinander) · `s3-4a cv-egrenz` · `s2-2c cv-betrag` · `s3-2b um-canvas`.

#### Was die Sichtung nicht ergab

Kein Widget ist streichwürdig, keine Figur fachlich falsch gezeichnet. Die
Aufgaben-Grafiken ohne Term (`a1-canvas`/`a2-canvas` auf fast jeder Seite) sind
durchgehend so gewollt — dort ist der Term die gesuchte Antwort.
