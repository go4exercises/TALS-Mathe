# TODO — Animations-Audit Schwerpunktfach

**Stand: 1. August 2026.** Vollprüfung aller interaktiven Canvas-Animationen im
Schwerpunktfach (23 Seiten). Ersetzt kein früheres Audit — dies ist die erste Prüfung dieses Bereichs.

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
stichprobenweise geprüft. Die Messungen sind vollständig, die didaktische Bewertung
der Einzelfälle ist es nicht — sie ist als Leseliste gedacht, nicht als Urteil.

---

## Bestand

| | Anzahl |
|---|---:|
| Canvas gesamt | 98 |
| davon interaktiv (mit Bedienelement) | 94 |
| **ohne Hinweispaar** | **16** |
| **ohne Term/Formel im Bild** | **73** |
| davon ganz ohne Inhaltstext (nur Achsenzahlen) | 31 — 17 im Lehrteil, 14 in Aufgaben |
| tote Regler | **0** |

---

## AN-S01 — Hinweispaar fehlt auf 16 interaktiven Animationen · **P2**

Der STYLEGUIDE führt das Paar «Worauf achten?» / «Erkenntnis» als Pflicht je
interaktiver Animation. Tatsächlich hat es nur ein Teil. Ohne den Hinweis bleibt
offen, *worauf* beim Schieben zu achten ist und *was* dabei herauskommen soll —
genau die Kopplung, die eine Animation didaktisch trägt.



**`s2-2a-potenz-wurzel-rationale-gleichungen`**
- [ ] `a1-canvas` · §aufgaben

**`s2-2b-exponential-logarithmische-gleichungen`**
- [ ] `a1-canvas` · §aufgaben

**`s2-2c-betrag-polynom-ungleichungen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-1-grundlagen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-2a-potenzfunktionen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-2b-wurzelfunktionen`**
- [ ] `wz-canvas` · §typen
- [ ] `a1-canvas` · §aufgaben

**`s3-3-polynomfunktionen`**
- [ ] `a2-canvas` · §aufgaben

**`s3-4a-exponentialfunktionen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-4b-logarithmusfunktionen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-5-trigonometrische-funktionen`**
- [ ] `a1-canvas` · §aufgaben

**`s3-6-betragsfunktionen`**
- [ ] `a1-canvas` · §aufgaben

**`s4-1-grundlagen`**
- [ ] `cv-a1` · §aufgaben

**`s4-3a-vektorbegriff-komponenten`**
- [ ] `a1-canvas` · §aufgaben

**`s4-3b-skalarprodukt`**
- [ ] `a1-canvas` · §aufgaben

**`s4-3c-geraden`**
- [ ] `a1-canvas` · §aufgaben


---

## AN-S02 — Kurve ohne Term im Bild: 17 Animationen im Lehrteil · **P2**

Diese Animationen zeigen im Canvas **gar keinen** Inhaltstext — nur Achsenzahlen.
Man sieht eine Kurve oder Figur, erfährt im Bild aber nicht, welche. Der Term steht
jeweils daneben im Fliesstext oder in der Reglerzeile; im Bild fehlt die Kopplung
«Parameter → Darstellung → Formel», die der STYLEGUIDE als Kern der Widgets nennt.

Vorschlag je Fall: den aktuellen Term als Beschriftung an die Kurve setzen
(`beschriftung()`, §2.9) — dieselbe Farbe wie die Kurve, am rechten Kurvenende.

**Nicht** in dieser Liste: 14 Aufgaben-Grafiken ohne Term. Dort ist das
Weglassen oft gewollt — der Term ist die gesuchte Antwort. Vor einer Änderung je
Aufgabe entscheiden.


**`s2-2b-exponential-logarithmische-gleichungen`**
- [ ] `gl-canvas` · §darstellungen

**`s2-2c-betrag-polynom-ungleichungen`**
- [ ] `vz-canvas` · §typen

**`s3-1-grundlagen`**
- [ ] `st-canvas` · §darstellungen
- [ ] `ug-canvas` · §theorie

**`s3-2a-potenzfunktionen`**
- [ ] `dr-canvas` · §darstellungen
- [ ] `hy-canvas` · §theorie
- [ ] `pa-canvas` · §typen

**`s3-3-polynomfunktionen`**
- [ ] `lf-canvas` · §darstellungen
- [ ] `gv-canvas` · §typen

**`s3-4a-exponentialfunktionen`**
- [ ] `dr-canvas` · §darstellungen
- [ ] `tr-canvas` · §theorie

**`s3-4b-logarithmusfunktionen`**
- [ ] `tr-canvas` · §theorie

**`s3-5-trigonometrische-funktionen`**
- [ ] `ek-kreis` · §darstellungen

**`s3-6-betragsfunktionen`**
- [ ] `uk-canvas` · §typen

**`s4-2a-prismen-zylinder`**
- [ ] `qd-canvas` · §definition

**`s4-2b-pyramiden-kegel-stuempfe`**
- [ ] `ke-canvas` · §darstellungen

**`s4-3c-geraden`**
- [ ] `cv-lot` · §theorie


---

## AN-S02b — Term im Bild fehlt, aber es gibt andere Beschriftung: 42 weitere

Diese tragen zwar Text im Bild (Achsentitel, Punktnamen, Einheiten), aber keinen
Term. Schwächerer Fall als AN-S02 — je Animation entscheiden, ob der Term
etwas beiträgt.


**`s1-1-grundlagen`**
- [ ] `sw-canvas` · §einstieg
- [ ] `cv-pruefstand` · §typen

**`s1-2-potenzen`**
- [ ] `ex-canvas` · §rationale-exponenten
- [ ] `cv-zehnerpot` · §hierarchie

**`s2-1-grundlagen`**
- [ ] `wa-canvas` · §einstieg
- [ ] `cv-sl` · §definition

**`s2-2a-potenz-wurzel-rationale-gleichungen`**
- [ ] `sw-canvas` · §einstieg
- [ ] `sc-canvas` · §darstellungen

**`s2-2b-exponential-logarithmische-gleichungen`**
- [ ] `al-canvas` · §einstieg

**`s2-2c-betrag-polynom-ungleichungen`**
- [ ] `to-canvas` · §einstieg

**`s3-1-grundlagen`**
- [ ] `dn-canvas` · §einstieg
- [ ] `tr-canvas` · §typen

**`s3-2a-potenzfunktionen`**
- [ ] `ba-canvas` · §einstieg
- [ ] `typ-canvas` · §typen

**`s3-2b-wurzelfunktionen`**
- [ ] `pe-canvas` · §einstieg
- [ ] `wz-canvas` · §typen
- [ ] `tf-canvas` · §theorie

**`s3-3-polynomfunktionen`**
- [ ] `sc-canvas` · §einstieg
- [ ] `cv-lt` · §typen

**`s3-4a-exponentialfunktionen`**
- [ ] `bk-canvas` · §einstieg
- [ ] `ty-canvas` · §typen

**`s3-4b-logarithmusfunktionen`**
- [ ] `ek-canvas` · §einstieg
- [ ] `sp-canvas` · §definition
- [ ] `ty-canvas` · §eigenschaften
- [ ] `c14-canvas` · §theorie

**`s3-5-trigonometrische-funktionen`**
- [ ] `rr-rad` · §einstieg
- [ ] `ty-canvas` · §typen
- [ ] `tr-canvas` · §theorie
- [ ] `a1-canvas` · §aufgaben

**`s3-6-betragsfunktionen`**
- [ ] `ab-canvas` · §einstieg
- [ ] `tr-canvas` · §darstellungen

**`s4-1-grundlagen`**
- [ ] `sb-canvas` · §einstieg

**`s4-2a-prismen-zylinder`**
- [ ] `cv-canvas` · §einstieg
- [ ] `zy-canvas` · §darstellungen

**`s4-2b-pyramiden-kegel-stuempfe`**
- [ ] `fu-canvas` · §einstieg
- [ ] `cv-k3` · §typen

**`s4-3a-vektorbegriff-komponenten`**
- [ ] `fl-canvas` · §einstieg
- [ ] `ad-canvas` · §darstellungen

**`s4-3b-skalarprodukt`**
- [ ] `wl-canvas` · §darstellungen

**`s4-3c-geraden`**
- [ ] `dr-canvas` · §einstieg

**`s4-3d-ebenen`**
- [ ] `cv-haus` · §darstellungen
- [ ] `da-canvas` · §einstieg

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

- [ ] **AN-S04a** `s1-1` · `cv-pruefstand` · **P3** — Die Werte stehen mit vier
  Nachkommastellen da («Differenz 12.0000», «25.0000», «13.0000»), obwohl es
  ganze Zahlen sind. Wirkt nach Maschine, nicht nach Mathematik. Auf ganzzahlige
  Anzeige umstellen, Nachkommastellen nur wo nötig.
- [ ] **AN-S04b** `s1-1` · `cv-pruefstand` · **P2** — Unter den Balken steht
  «(a+b)² = a² + b²» ohne Kennzeichnung. Das ist genau die **falsche** Gleichung,
  die das Widget widerlegen soll. Ohne Markierung (durchgestrichen, rot, «≠»)
  liest sie sich wie eine Merkformel.
- [ ] **AN-S04c** `s1-2` · `ex-canvas` · **P4** — Die y-Achse ist logarithmisch
  (1/256 … 256), aber nur die x-Achse ist beschriftet («Exponent x»). Der y-Achse
  fehlt die Angabe, was sie zeigt.
- [ ] **AN-S04d** `s1-3` · `cv-rechenschieber` · **P3** — Die verschiebbare
  C-Skala läuft rechts aus dem Bild, ohne dass das angedeutet wird. Beim Schieben
  verschwinden Zahlen wortlos. Entweder Skala kürzen oder den Rand andeuten.
- [ ] **AN-S04e** `s2-1` · `wa-canvas` · **P2** — Die Waage steht waagrecht, obwohl
  links «x x x + 2» und rechts 12 Kugeln liegen. Ohne Zahlenanzeige ist nicht
  ablesbar, ob die Seiten gleich sind — dasselbe Muster wie AN-11 im
  Grundlagen-Audit (`g2-1` · `uf-canvas`, dort als «faktisch tot» notiert).
  Beide zusammen anschauen.
- [ ] **AN-S04f** `s2-2a` · `a1-canvas` · **P3** — x-Achse von −25 bis 25, die
  Kurve liegt vollständig im rechten Viertel. Drei Viertel der Fläche sind leer.
  Skalierung an den dargestellten Bereich anpassen (STYLEGUIDE §3: aufgabenbezogen).
- [ ] **AN-S04g** `s3-1` · `ug-canvas` · **P3** — Die x-Achsenzahlen liegen in den
  grün hinterlegten Lösungsbereichen und sind dort schlecht lesbar. Die Zahlen
  nach der Flächenfüllung setzen (`zahlenOben()` aus `drawGrid`).
- [ ] **AN-S04h** `s3-2a` · `hy-canvas` · **P4** — Die Hyperbeläste laufen oben und
  unten ohne Andeutung aus dem Bild; es sieht nach abgeschnitten statt nach
  «geht weiter» aus.
- [ ] **AN-S04i** `s3-1` · `we-graph` · **P4** — «x [m]» am rechten Rand berührt die
  letzte Achsenzahl (30). Dasselbe Muster wie auf den bereits korrigierten Seiten:
  letzte Zahl weglassen, dort steht die Achsenbeschriftung.

### Noch nicht einzeln gesichtet

Die Animationen der Seiten **s3-2b bis s4-3d** (Blätter 4–9 des Kontaktabzugs,
rund 70 Stück) sind über die Messungen oben erfasst, aber im Bild noch nicht
einzeln beurteilt. Der Kontaktabzug liegt bereit — die Fortsetzung ist ein
eigener Durchgang.
