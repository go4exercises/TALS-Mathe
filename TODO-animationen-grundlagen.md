# TODO — Animations-Audit Grundlagenfach

**Stand: 1. August 2026.** Vollprüfung aller interaktiven Canvas-Animationen im
Grundlagenfach (23 Seiten). Ersetzt das Audit vom 25.07.2026 — dessen 90 Punkte sind am 01.08. gegengeprüft und weiterhin offen; sie stehen unverändert in `TODO-animationen-grundlagen-2026-07-25.md`.

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
| Canvas gesamt | 107 |
| davon interaktiv (mit Bedienelement) | 96 |
| **ohne Hinweispaar** | **44** |
| **ohne Term/Formel im Bild** | **49** |
| davon ganz ohne Inhaltstext (nur Achsenzahlen) | 22 — 18 im Lehrteil, 4 in Aufgaben |
| tote Regler | **0** |

---

## AN-G01 — Hinweispaar fehlt auf 42 interaktiven Animationen · **P2**

Der STYLEGUIDE führt das Paar «Worauf achten?» / «Erkenntnis» als Pflicht je
interaktiver Animation. Tatsächlich hat es nur ein Teil. Ohne den Hinweis bleibt
offen, *worauf* beim Schieben zu achten ist und *was* dabei herauskommen soll —
genau die Kopplung, die eine Animation didaktisch trägt.


> **Liste korrigiert am 01.08.2026.** Die erste Fassung ordnete die Hinweispaare
> über die Bildschirmnähe zu und lag bei einem Teil daneben. Neu wird die Zuordnung
> am Quelltext bestimmt (jede `.widget-titelzeile` gehört zum nächsten `<canvas>`
> darunter) und gegen die DOM-Messung geprüft — beide Verfahren stimmen bei 61 von
> 62 Zuordnungen überein. Die Gesamtzahl blieb gleich, die Namen haben sich geändert:
> `lin-canvas`, `par-canvas`, `schn-canvas`, `cv-vertikal`, `sch-canvas`, `bm-canvas`
> und `cv-kk` **haben** ein Hinweispaar und sind hier zu Unrecht gestanden.


**`g1-2-zahlen-grundoperationen`**
- [ ] `cv-iv`

**`g1-3-algebraische-terme`**
- [ ] `cv-binomi-rechts`

**`g2-2a-lineare-gleichungen`**
- [ ] `cv-three`

**`g2-2b-quadratische-gleichungen`**
- [ ] `velo-canvas`
- [ ] `cv-pk`

**`g2-3-lineare-gleichungssysteme`**
- [ ] `cv-three`
- [ ] `cv-lf`
- [ ] `cv-a1`

**`g3-1-grundlagen`**
- [ ] `einstieg-glas`
- [ ] `einstieg-canvas`
- [ ] `ach1-canvas`
- [ ] `ach2-canvas`
- [ ] `schn1-canvas`
- [ ] `schn2-canvas`

**`g3-2-lineare-funktionen`**
- [ ] `a1-canvas`
- [ ] `a2-canvas`

**`g3-3-quadratische-funktionen`**
- [ ] `dr-canvas`
- [ ] `typ-canvas`
- [ ] `a2-canvas`

**`g4-1-grundlagen`**
- [ ] `sb-canvas`

**`g4-2-diagramme`**
- [ ] `ea-canvas`

**`g4-3-masszahlen`**
- [ ] `sl-canvas`
- [ ] `cv-robust`

**`g5-1-grundlagen`**
- [ ] `dg-canvas`

**`g5-2a-dreiecke`**
- [ ] `cv-stativ`
- [ ] `cv-allg`
- [ ] `cv-spez`
- [ ] `cv-elem`
- [ ] `cv-flaeche`
- [ ] `cv-kong`
- [ ] `cv-pyth`
- [ ] `cv-anw`

**`g5-2c-kreis-und-kreisteile`**
- [ ] `pizza-canvas`
- [ ] `cv-strecken`
- [ ] `cv-pi`
- [ ] `cv-umfang`
- [ ] `cv-ring`
- [ ] `cv-sektor`
- [ ] `cv-segment`

**`g5-4-einheitskreis`**
- [ ] `cv-schiff`
- [ ] `cv-tan`
- [ ] `cv-bez`

## AN-G02 — Kurve ohne Term im Bild: 18 Animationen im Lehrteil · **P2**

Diese Animationen zeigen im Canvas **gar keinen** Inhaltstext — nur Achsenzahlen.
Man sieht eine Kurve oder Figur, erfährt im Bild aber nicht, welche. Der Term steht
jeweils daneben im Fliesstext oder in der Reglerzeile; im Bild fehlt die Kopplung
«Parameter → Darstellung → Formel», die der STYLEGUIDE als Kern der Widgets nennt.

Vorschlag je Fall: den aktuellen Term als Beschriftung an die Kurve setzen
(`beschriftung()`, §2.9) — dieselbe Farbe wie die Kurve, am rechten Kurvenende.

**Nicht** in dieser Liste: 4 Aufgaben-Grafiken ohne Term. Dort ist das
Weglassen oft gewollt — der Term ist die gesuchte Antwort. Vor einer Änderung je
Aufgabe entscheiden.


**`g3-1-grundlagen`**
- [ ] `cv-vertikal` · §funktion-nicht

**`g3-2-lineare-funktionen`**
- [ ] `typ-canvas` · §typen

**`g3-3-quadratische-funktionen`**
- [ ] `disk-canvas` · §diskriminante
- [ ] `typ-canvas` · §typen

**`g5-2a-dreiecke`**
- [ ] `cv-allg` · §definition
- [ ] `cv-beweis` · §darstellungen
- [ ] `cv-spez` · §typen
- [ ] `cv-elem` · §typen
- [ ] `cv-flaeche` · §theorie
- [ ] `cv-stativ` · §einstieg

**`g5-2b-vierecke`**
- [ ] `fam-canvas` · §einstieg
- [ ] `cv-flaeche` · §theorie

**`g5-2c-kreis-und-kreisteile`**
- [ ] `cv-strecken` · §darstellungen

**`g5-2d-zentrische-streckung-aehnlichkeit`**
- [ ] `cv-streck` · §darstellungen
- [ ] `cv-figur` · §aehnlichkeit
- [ ] `cv-aehnSatz` · §aehnlichkeitssaetze

**`g5-3-trigonometrische-berechnungen`**
- [ ] `cv-sinussatz` · §schief-dreieck
- [ ] `cv-ssw` · §schief-dreieck


---

## AN-G02b — Term im Bild fehlt, aber es gibt andere Beschriftung: 27 weitere

Diese tragen zwar Text im Bild (Achsentitel, Punktnamen, Einheiten), aber keinen
Term. Schwächerer Fall als AN-G02 — je Animation entscheiden, ob der Term
etwas beiträgt.


**`g1-4-zehnerpotenzen-quadratwurzeln`**
- [ ] `cv-zoom` · §einstieg

**`g2-1-grundlagen`**
- [ ] `wg-canvas` · §einstieg

**`g2-2b-quadratische-gleichungen`**
- [ ] `velo-canvas` · §einstieg
- [ ] `cv-pk-parabel` · §parameter

**`g2-3-lineare-gleichungssysteme`**
- [ ] `cv-three` · §darstellungen
- [ ] `cv-lf` · §loesungsfaelle
- [ ] `cv-lbuschel` · §loesungsfaelle

**`g3-2-lineare-funktionen`**
- [ ] `ks-canvas` · §einstieg
- [ ] `dr-canvas` · §darstellungen

**`g3-3-quadratische-funktionen`**
- [ ] `ws-canvas` · §einstieg
- [ ] `dr-canvas` · §darstellungen

**`g4-1-grundlagen`**
- [ ] `sb-canvas` · §einstieg

**`g4-2-diagramme`**
- [ ] `ea-canvas` · §einstieg
- [ ] `cv-manip` · §typen

**`g4-3-masszahlen`**
- [ ] `cv-robust` · §theorie

**`g5-2a-dreiecke`**
- [ ] `cv-kong` · §theorie
- [ ] `cv-pyth` · §theorie
- [ ] `cv-anw` · §theorie

**`g5-2b-vierecke`**
- [ ] `cv-reg` · §theorie

**`g5-2c-kreis-und-kreisteile`**
- [ ] `cv-ring` · §theorie
- [ ] `cv-sektor` · §theorie
- [ ] `cv-segment` · §theorie

**`g5-2d-zentrische-streckung-aehnlichkeit`**
- [ ] `cv-strlabor` · §strahlensaetze

**`g5-3-trigonometrische-berechnungen`**
- [ ] `cv-aehnl` · §recht-dreieck

**`g5-4-einheitskreis`**
- [ ] `cv-schiff` · §einstieg
- [ ] `cv-abw` · §definition

**`g5-5-trigonometrische-gleichungen`**
- [ ] `cv-rad` · §einstieg

---

## AN-G03 — Tote Bedienelemente: **keine** · geprüft, nichts zu tun

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

