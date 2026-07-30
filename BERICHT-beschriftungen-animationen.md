# Beschriftungs-Konflikte in den Canvas-Animationen

**Stand: 30.07.2026, nach der Überarbeitung.** Prüflauf über alle 46 Themenseiten,
jede Animation in der Startposition, 1280 px.

| | vorher | nachher |
|---|---:|---:|
| Einzelbefunde | **228** | **4** |
| betroffene Animationen | **55** | **4** |
| betroffene Seiten | **27** | **4** |
| geprüfte Beschriftungen | 2573 | 2455 |

Was übrig ist, sind vier Stellen, an denen eine **Achsenzahl bzw. ein kleiner
Marker teilweise von einer Inhalts-Beschriftung verdeckt** wird, die bewusst
obenauf liegt. Die jeweils wichtigere Beschriftung ist in allen vier Fällen
vollständig lesbar. Details in §4.

---

## 0. Nachbesserung 30.07.2026 (nach Durchsicht)

Elf Rückmeldungen aus der Sichtprüfung sind eingearbeitet:

- **Ruckeln beim Reglerziehen behoben.** Die Freistellung hatte die Hintergrundfarbe
  pixelweise abgetastet — vier `getImageData` je Beschriftung, also 16 GPU-Readbacks
  pro Neuzeichnung. Neu kommt die Farbe aus dem Stylesheet des Canvas, einmal gelesen
  und am Element gemerkt. Abtasten gibt es nur noch auf ausdrücklichen Wunsch
  (`bgAuto`). Messung: `drawElem` in g5-2a **0.50 → 0.17 ms**, Readbacks **16 → 0**.
- **Punktbeschriftungen** sitzen jetzt rechts bzw. rechts unterhalb des Punktes statt
  darüber: `ks-canvas`, `ws-canvas`, `ba-canvas`, `dr-canvas`, `cv-lbuschel`.
- **Winkelbeschriftungen im Dreieck** (`cv-cossatz`, `cv-flaeche`): `drawAngleArc()`
  bildet die Richtung neu aus den beiden normierten Schenkeln. Die frühere Mittelung
  der Winkel landete je nach `ccw`-Fall in der Gegenrichtung — die Beschriftung stand
  ausserhalb der Figur, bei `cv-cossatz` sogar ausserhalb des Canvas.
- **`einstieg-glas`**: das Glas ist 24 px schmaler, dadurch stehen die Skalenzahlen
  rechts neben ihren Strichen statt an den Rand geklemmt auf ihnen.
- **`sw-canvas`**: „100 km" ans rechte Ende der Marke. **`cv-equiv`**: die zwei
  Vermerkzeilen wieder unterhalb des Ergebniskastens statt hineingeschoben.
- **`ws-canvas`**: die letzte x-Zahl entfällt, dort steht die Achsenbeschriftung.

---

## 1. Was geändert wurde

### 1.1 Neuer Helfer `beschriftung()` in `mathlib.js`

Ersetzt `ctx.fillText` überall dort, wo eine Beschriftung auf Grafik treffen oder
aus dem Bild laufen kann. Er leistet dreierlei:

- **Freistellung** — ein Feld in Hintergrundfarbe unter dem Text (`frei`), oder
  eine Kontur entlang der Buchstaben (`halo:true`) für ungleichmässigen Untergrund
  wie Geometriefüllungen.
- **Klemmen** — mit `W`/`H` bleibt das Textfeld im Canvas; nichts läuft mehr hinaus.
- **Farbwahl** — ohne `bg` wird der Untergrund an den vier Ecken des Textfelds
  abgetastet. Genommen wird die Farbe nur bei klarer Mehrheit (3 von 4) und
  ausreichendem Kontrast zur Textfarbe; sonst die Notfarbe. Ohne diese zwei Regeln
  wurde an Figurenecken die dunkle Kantenfarbe abgetastet und der Halo machte den
  Buchstaben zum Klumpen.

### 1.2 `drawGrid()` — drei Korrekturen

- **Achsenzahlen wandern nicht mehr aus dem Bild.** Die Seite der Achse wird
  bestimmt statt angenommen: liegt der Nullpunkt am Canvasrand (`xMin=0`/`yMin=0`),
  stehen die Zahlen innen an der Achse statt ausserhalb. Das war die Ursache mit der
  grössten Wirkung — fünf Anwendungsgraphen hatten **gar keine** Achsenzahlen mehr,
  `ks-canvas` etwa 24 von 29 Beschriftungen ausserhalb der Zeichenfläche.
- **Schrittweite nach Platz** statt fest 1. Bei weiten Bereichen (−28…28 auf 460 px)
  verschmolzen die Zahlen zu einem unlesbaren Band; jetzt greift eine 1-2-5-10-Folge.
  Auf der y-Achse bleibt es bei jeder zweiten Einheit — eng wird nur weiter, nie dichter.
- **`{achsenLabels:false}` und `{zahlen:false}`** statt Übermalen. Der bisherige Weg,
  die generischen „x"/„y" mit `fillRect` abzudecken, arbeitete mit festen Pixelwerten
  und liess je nach Skalierung einen Strichrest neben der neuen Caption stehen.
- Neu liefert `drawGrid` ausserdem `zahlenOben()`, damit eine Seite die Achsenzahlen
  nach ihren Kurven noch einmal obenauf setzen kann.

### 1.3 Seitenseitig

- Der gemeinsame `txt()`-Helfer der sechs Geometrieseiten zeichnet jetzt mit Halo und
  Klemmung — das deckt über 300 Beschriftungen auf einen Schlag ab.
- Der seiteneigene `plotChart()` in `g3-1` wurde auf `beschriftung()` umgestellt;
  Achsenzahlen liegen dort nach den Kurven, aber vor den Punkt-Beschriftungen.
- Rund 30 einzelne Beschriftungen wurden umgestellt oder verschoben, darunter
  „Klasse A/B" und die MW-Zeilen in `sl-canvas`, „α=60°"/„φ=55°" in den Dreiecken,
  „Hinweg/Rückweg" in `velo-canvas` und die Zeichenreihenfolge von „a²"/„b²" in
  `cv-pyth`, die in der Startposition von der animierten Kopie verdeckt waren.

---

## 2. Prüfung

- **Messverfahren unverändert**: `fillText` instrumentiert, Textfeld aus `measureText`
  samt `textAlign`/`textBaseline` und Transformationsmatrix, Canvas-Pixel vor und nach
  dem Zeichnen sowie im Endbild. `strokeText` zählt nicht mehr als eigene Beschriftung —
  es ist die Halo-Kontur und läge deckungsgleich unter dem `fillText` desselben Textes.
- **Pre-Flight** über alle 46 Themenseiten: `ALLE CHECKS BESTANDEN`.
- **Render-Check** aller 46 Seiten bei **1280 px und 360 px**: keine JS-Fehler,
  kein Horizontalscroll.
- **205 Canvas zeichnen wie vorher** — die Zahl war zwischenzeitlich auf 197 gefallen,
  weil drei Umstellungen auf Variablen ausserhalb ihres Gültigkeitsbereichs zugriffen;
  das ist behoben und wird vom Lauf mitgeprüft.

Werkzeug: `scripts/audit-beschriftungen/` — `audit-run.mjs` (messen),
`audit-analyse.py` (bewerten), `audit-crops.mjs` (Kontrollbilder), `audit-orte.py`
(Quellzeilen finden). Voraussetzung: `python3 -m http.server 8001` im Repo-Root.

---

## 3. Was der Prüflauf nicht abdeckt

- **Nur die Startposition.** Regler und Knöpfe können neue Kollisionen erzeugen.
- **Nur 1280 px** für die Beschriftungsmessung; der Render-Check lief zusätzlich bei 360 px,
  prüft dort aber nur JS-Fehler und Horizontalscroll, nicht die Beschriftungslage.
- **Nur Canvas-Text.** HTML/MathJax neben der Grafik ist nicht erfasst.
- Die Grenzwerte (25 % Überdeckung, 1.5 px Rand) sind gesetzt, nicht hergeleitet.

---

## 4. Restbestand — vier Stellen

Alle vier sind vom selben Typ: eine **Achsenzahl oder ein kleiner Marker** wird von
einer Inhalts-Beschriftung teilweise verdeckt, die bewusst darüber liegt. Die
Alternative wäre, die Achsenzahl über die Inhalts-Beschriftung zu legen — das wurde
probiert und ist sichtbar schlechter, weil dann die eigentliche Aussage der Grafik
angeschnitten wird. Kein Eingriff empfohlen.

| Animation | verdeckt | sichtbar | verdeckt durch |
|---|---|---:|---|
| [`ach1-canvas`](http://localhost:8001/grundlagen/g3-1-grundlagen.html#ach1-canvas)<br>g3-1-grundlagen | `4` | 19 % | Punkt-Beschriftung «(3 | 0)» |
| [`cv-steig`](http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#cv-steig)<br>g3-2-lineare-funktionen | `3` | 28 % | Steigungsdreieck (Δy-Klammer) |
| [`cv-stv`](http://localhost:8001/grundlagen/g5-2b-vierecke.html#cv-stv)<br>g5-2b-vierecke | `M` | 40 % | Radiuslinie und Eckpunkt-Marker |
| [`wa-canvas`](http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#wa-canvas)<br>s3-6-betragsfunktionen | `6` | 44 % | Beschriftung «Boden = 5» |

