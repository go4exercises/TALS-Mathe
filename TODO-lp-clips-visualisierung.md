# Leitprogramm-Clips: Ton, Bild und Bewegung — Übersicht

Stand 07.10.2026. Geprüft: die **44 Einführungsclips** der neun sichtbaren Leitprogramme (ohne
Kontrollclips), Szene für Szene, nur gelesen. Grundlage: Drehbuch, Sprechzeiten
(`.claude/tools/sprechzeiten.py`) gegen `ein` und Bewegungs-Stützpunkte, Prüfbilder
(`pruef-clip.mjs`) und die Animation des Kapitels (`figure.sim#simN` in `scripts/lp/<name>/seite.js`).
Vier unabhängige Prüfagenten; die drei schwersten Befunde (Tangens, «Zuerst a prüfen», Umklappen)
vom Hauptagenten am Drehbuch nachgeprüft.

**Befundarten**
- **A — gesagt/notiert, aber nicht (rechtzeitig) im Bild:** Etwas, das man sehen könnte, fehlt im Bild,
  oder Bild und Ton liegen mehr als 1.5 s auseinander (meist: Ergebnis steht zu früh da).
- **B — statisch, wo die Animation des Kapitels dynamisch ist:** Der Clip zeigt die Endlage dessen,
  was man danach mit einem Regler verändert; eine Bewegung im Clip wäre die Brücke zur Animation.

**Aufwand:** *nur Bild* (Einblendezeit, Hilfslinie, Punkt) · *neue Bewegung* (Stützpunkte, kann der
Clip-Bauer heute) · *Werkzeug-Erweiterung* (`build-clips.py` muss etwas Neues können) ·
*Neuvertonung* (Sprechertext ändert sich).

## Stand der Umsetzung (07.10.2026)

**Erledigt:** alle sechs Vorrang-Befunde und die *nur Bild*-Befunde in allen neun Leitprogrammen
(39 Einführungsclips neu gebaut, Sprechertext und `dauer` unverändert, keine Neuvertonung).
Der Clip-Bauer blendet das Steigungsdreieck bei Δx = 0 aus (`build-clips.py`). Später
Eingeblendetes steht in einem zweiten `graf` als Deckblatt (HOWTO-clips, «Später einblenden»).
Die Tabellen unten zeigen noch den Befund vor der Umsetzung.

**Bewusst nicht als *nur Bild* umgesetzt** (bleibt bei Werkzeug oder Bewegung):
- Planimetrie: Zwischenstände (Winkelsumme, «Warum die Hälfte», Sektor 0°/90°/180°) — ohne `aus` blieben sie im Endbild stehen.
- Exp/Log «Gleicher Faktor», «Verdopplungszeit», «Halbwertszeit» (als Werkzeug eingestuft).
- `g2-2-lp-parameter` «Zuerst a prüfen»: Behelf mit Bewegungen (Parabel, Gerade, Parabel nacheinander); stetig durch m = 0 erst mit Normalform-Bewegung.
- `s3-6-lp-gleichungen` «Wie viele?»: Waagrechte wandert, aber ohne mitlaufende Schnittpunkte.
- `g3-3-lp-mitte` Merke «a positiv Minimum»: weggelassen (kein sinnvolles Bild im Zaunfenster).

**Zweiter Durchgang (07.10.2026): *neue Bewegung*** in 22 Einführungsclips umgesetzt (alle Leitprogramme
ausser Planimetrie, wo jede Bewegung bewegbare Figuren braucht). Dazu im Clip-Bauer: Beim Tangens läuft der
Strahl von P durch den Mittelpunkt, wenn P links der y-Achse liegt (vorher hing P neben der Linie).
Bewusst weggelassen, weil die Bewegung dem Gesagten widerspräche oder auf keinem Satz läge:
`g3-2-lp-m-und-b` Wertetabelle, `g3-2-lp-steigungsdreieck` «Die Nullstelle» (b −6 → −4),
`s3-2-lp-umkehren` n 3 → 2, `s3-4-lp-wachstum-zerfall` Startwert 200 → 400.
Brauchen einen neuen Satz (Neuvertonung): `s3-2-lp-hyperbel` a 1 → −1, `g3-3-lp-drei-formen` a 1 → −1,
`g3-3-lp-a-finden` Fall B.

**Offen:** alle Zeilen *Werkzeug-Erweiterung*, die *Neuvertonungen* (4 + die drei eben genannten).
Zusätzlich fürs Werkzeug: Tangensstrecke am Fensterrand abschneiden statt ausblenden (darum fährt P nur bis
1.245 rad); senkrechte bewegte Gerade (`g3-2-lp-typen` Merke); mitlaufende Schnittpunkte auch bei
«Faktor im Argument» (Trig-Gleichungen).

**Bei der Umsetzung neu aufgefallen:**
- ~~`g2-2-lp-verfahren` «Erst ordnen», `g2-2-lp-nullprodukt` «Der teure Fehler»: Notiz zu spät~~ — falsch
  gemessen (`sprechzeiten.py` fasst dort mehrere Sätze zusammen; Wortzeiten mit faster-whisper: «x ist zwei»
  bei 16.0 s, «Die Null ist verloren» bei 4.3 s). Zu früh waren die Punkte; im zweiten Durchgang behoben.
  Auch der Befund «Die Null ist verloren (1.8–2.7)» in der Tabelle unten ist so zu lesen.
- `s3-5-lp-periode-symmetrie`: die Sinuskurve schneidet «(π/6 | 0.5)» und «(−π/6 | −0.5)».
- `s3-6-lp-gleichungen` «Am Graphen», «Merke»: «(1 | 0)» stösst an die Achszahl 2.
- `s3-2-lp-hyperbel` «Gerade Ordnung»: Asymptoten in Tinte, kaum sichtbar (sonst jetzt rot).
- `g3-2-lp-steigungsdreieck` «Leserichtung»: bei Δx < 0 steht «Δy» rechts der Kathete, im Endbild auf der y-Achse (Werkzeug).
- Live-Beschriftungen runden auf eine Stelle (−0.75 → «−0.8», −1.25 → «−1.2»); darum an einigen Stellen feste Texte statt Begleiter (Werkzeug).

## Auf einen Blick

Rund 145 Befundzeilen; davon etwa 81 *nur Bild*, 39 *neue Bewegung*, 35 brauchen (oder hätten ideal) eine
*Werkzeug-Erweiterung*, 4 eine *Neuvertonung* (Zeilen mit mehreren Angaben doppelt gezählt). Ohne
Befund: `s3-6-lp-verschieben`; fast ohne: `s3-5-lp-parameter`, `g3-3-lp-verschieben`, `s3-3-lp-vielfachheit`.

**Häufigste Muster**
1. **Ergebnis zu früh im Bild** (alle Leitprogramme): Punkte, Lösungen, Proben, Tabellen stehen ab
   Szenenbeginn, gesprochen werden sie 3–14 s später. Behebung meist nur `ein` — ausser bei festen
   `punkte` im `graf`, die heute kein eigenes `ein` haben (Notbehelf: mehrere `graf` übereinander).
2. **Gesagte Hilfslinien fehlen:** Symmetrieachsen, Abstände, Höhen, Leserichtungen, Probe-Rechtecke,
   Zahlen in der Figur. Mit `figuren`/`marken` heute machbar.
3. **Bewegung neben dem Satz statt zu ihm,** vor allem in den Merke-Szenen. Neue Stützpunkte genügen.
4. **Brücke zur Animation fehlt** dort, wo die Animation einen *Läufer*, eine *Waagrechte y = c* oder
   eine *bewegte Figur* hat (Planimetrie, Exp/Log, Polynom-Extrema, Betragsgleichungen).

**Vorrang** (falsches oder leeres Bild zu einer Erklärung)
- `s3-5-lp-tangens`, «Am Einheitskreis»: P steht 9 s auf 0 — die erklärte Tangensstrecke hat Länge 0.
  *Neue Bewegung (nur Stützpunkte).*
- `g2-2-lp-parameter`, «Zuerst a prüfen»: 20 s nur Formeln, «eine/zwei/keine Lösung» ohne Bild.
  *Behelf nur Bild (feste Parabeln nacheinander), ideal Werkzeug-Erweiterung.*
- `s3-6-lp-umklappen`: «das Stück klappt nach oben» — es wird nur eingeblendet. *Neue Bewegung.*
- `s3-6-lp-gleichungen`, «Wie viele?»: fünf Fälle für c, die Waagrechte steht fest auf 4. *Neue Bewegung.*
- `g3-3-lp-mitte`: Das Rechteck (Feld), um das es geht, ist nie zu sehen. *Nur Bild.*
- `g3-2-lp-steigungsdreieck`, «Leserichtung»: 5 s leeres Dreieck mit «Δx = 0» während «Δx > 0» gesagt
  wird. *Kleine Werkzeug-Korrektur.*

**Werkzeug-Erweiterungen, gebündelt** (je eine Änderung in `build-clips.py` deckt mehrere Befunde)
| Erweiterung | deckt ab |
|---|---|
| `ein` je fester Punkt im `graf` | Exp/Log (Wachstum ×3, Basis), Kreis-Kurve, Nullprodukt, Linearfaktoren u. a. |
| Läufer für `kurven` (wie bei Parabel/Gerade) | Hyperbel, Raten, Extrema, Wachstum, Sättigung, Logarithmus, Betragsfunktion |
| Δ-Beschriftung des Steigungsdreiecks bei dx = 0 ausblenden | steigungsdreieck ×2, aufstellen, typen |
| bewegbare `figuren` (Ecke ziehen, Strecken, Drehen) | alle fünf Planimetrie-Clips (C ziehen, Spitze t, Trapez d, Winkel φ, Faktor k) |
| `von`/`bis` in der `bewegung` | Umkehren (Einschränken), Extrema (Rand), aufstellen (Gerade ab x = 0) |
| Parabel-Bewegung in Normalform [t, a, b, c] | «Zuerst a prüfen» (Leitkoeffizient durch 0) |
| Begleiter «Symmetrieachse» an bewegter Parabel | achse-bleibt (b-Regler) |
| mitlaufende Schnittpunkte Kurve–Waagrechte | Trig-Gleichungen, Betragsgleichungen |
| bewegtes Fenster (Zoom) | Globalverlauf |

**Empfohlene Reihenfolge:** (1) die Vorrang-Befunde; (2) alle *nur Bild*-Befunde je Leitprogramm in einem
Durchgang (Clips neu bauen, keine Neuvertonung); (3) *neue Bewegung* — vor allem die Brücken zur Animation;
(4) Werkzeug: zuerst `ein` je Punkt und der Läufer für `kurven` (grösste Wirkung), dann bewegte Figuren für
die Planimetrie. Nach jeder Änderung: `pruef-clip.mjs` an den betroffenen Zeiten und Bilder ansehen.

---

## Lineare und quadratische Gleichungen (GF 2.2)

### `g2-2-lp-umformen` · Kap. 1 Lineare Gleichungen umformen · 91.7 s
Waage-Bild, die Umformung von \(4(x-2)=2x+6\) mit Probe, dann die Sonderfälle «keine Lösung» und «alle Zahlen».

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Vorgelöst (10.6–25.9 s) | B | Die Zeilen wandern bis «x = 7», der Graph bleibt fest auf \(y=4x-8\) und \(y=2x+6\) | Die Geraden je Schritt mitführen: blau \(m\) 4→2→2→1, \(q\) −8→−8→0→0; orange \(m\) 2→0, \(q\) 6→6→14→7. Der Schnitt bleibt bei \(x=7\) und zeigt so «Lösungsmenge bleibt gleich». Stützpunkte auf 6.2 / 9.6 / 11.8 s | neue Bewegung |
| Wenn x verschwindet (39.4 s, ab 9.4) | B | «Minus zwei x: sechs gleich neun» | Die Geraden zu den Waagrechten \(y=6\) und \(y=9\) drehen lassen: parallel, kein Schnitt | neue Bewegung |
| Alles ist Lösung (56.4 s, ab 7.8) | B | «Minus vier x: acht gleich acht» | Beide Geraden zur Waagrechten \(y=8\) drehen | neue Bewegung |

Szene 1 nennt die Waage nur als Bild im Kopf, das ist kein Befund. Die Probe ist synchron: Punkt bei 9.67, Satz bei 9.74.

### `g2-2-lp-nullprodukt` · Kap. 2 Ausklammern und Nullprodukt · 74.4 s
Satz vom Nullprodukt, \(x^2=5x\) in vier Schritten, Probe, und der Fehler «durch x teilen».

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Vorgelöst (20.1–35.6 s) | B | Der Graph erscheint erst bei 13.0, gleich mit Nullstellen | Ab Szenenbeginn \(y=x^2\) und \(y=5x\) zeigen (Schnitt bei 0 und 5). Bei «Minus fünf x» (0.6 s) die Parabel zum Scheitel (2.5 \| −6.25) und die Gerade auf \(m=0\) führen. Die Lösungen werden so zu Nullstellen | neue Bewegung |
| Der teure Fehler (49.4 s) | A | «Die Null ist verloren» (1.8–2.7) – kein Bild | Parabel \(y=x^2-5x\) mit Nullstelle (5\|0) grün und (0\|0) rot bzw. durchgestrichen | nur Bild |

### `g2-2-lp-ergaenzen` · Kap. 3 Wurzelziehen, Ergänzen, Mitternachtsformel · 96.8 s
Wurzelziehen mit ±, quadratische Ergänzung, Mitternachtsformel mit Beispiel, Anzahl Lösungen über D.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Ein Quadrat mit Klammer (12.8 s) | A | «x gleich fünf oder x gleich minus eins» – die Szene hat keinen Graphen | Die Parabel der Vorszene um 2 nach rechts schieben (\(u\) 0→2, 0.4–2.4 s). Die Waagrechte \(y=9\) bleibt, die Schnittpunkte −1 und 5 werden grün | neue Bewegung |
| Quadratisch ergänzen (22.3 s) | A (Zeit) | Die Nullstellen «(−1\|0)», «(5\|0)» stehen ab 0.31. Die Lösung kommt erst bei 14.4, rund 14 s später | Die Nullstellen erst mit \(\mathbb{L}\) einblenden | nur Bild |
| dito | B | Der Graph bleibt \(y=x^2-4x-5\), während die Gleichung zu \((x-2)^2=9\) wird | Graph mitlaufend: «\|+5» bei 5.2 → Parabel \(y=x^2-4x\) (Scheitel (2\|−4)) und Waagrechte \(y=5\). «\|+4» bei 8.9 → Scheitel (2\|0) und Waagrechte \(y=9\), wie in Szene 1. Die Schnittpunkte bleiben bei −1 und 5 | neue Bewegung (Parabel und Gerade, beides kann der Clip-Bauer) |

«Was D verrät» ist gut: die Bewegungen liegen genau auf den Sätzen (7.6–8.7 / 10.9–12.0).

### `g2-2-lp-verfahren` · Kap. 4 Das passende Verfahren · 98.5 s
Ordnen, dann je nach Typ Wurzel, Ausklammern, Zweiklammersatz, Binom oder Mitternachtsformel.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Erst ordnen (0–19 s, ab 8.1) | A | «heben sich die x Quadrat weg … eine lineare Gleichung» – im Bild bleiben zwei Parabeln | Bei «\|−x²» (10.4) zweites Bild mit \(y=2x+1\) und \(y=5\) einblenden, Schnitt bei \(x=2\). Eine Parabel kann nicht stetig in \(2x+1\) übergehen | nur Bild |
| Ein Binom (56.3 s) | A + B | «Es gibt nur eine Lösung: drei» – kein Graph. Die ganze Kette «x²−6x+9 = (x−3)² = 0» steht ab 0.25, als Standbild | Zweiteilen: «(x−3)² = 0» erst bei ~3.5 s. Parabel mit Scheitel (3\|0) zeigen: sie berührt die x-Achse, wie in Kap. 3 bei D = 0 | nur Bild |
| Wenn b fehlt (19.0 s) / Sonst die Formel (65.3 s) | A (schwach) | «±3», «(−1 ± √33)/4» – kein Bild | Optional: Parabel mit Nullstellen | nur Bild |

### `g2-2-lp-parameter` · Kap. 5 Parameterdiskussion (sim5: Regler k, Familien A/B/C) · 91.7 s
Lineare Parametergleichung mit dem Fall \(k=2\), Fallunterscheidung über \(D(k)\), und Parameter vor \(x^2\).

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Die Fälle (20.9 s, ab 8.5) | A | «schneiden sich die beiden Seiten immer bei x gleich drei» – der Schnittpunkt ist nicht markiert, und kein \(k\)-Wert ist sichtbar | Bei der blauen Geraden `marken: [{x: 3, text: "(3 \| {y})"}]` setzen. Dazu kurze Notizen «k = 5 / 3 / 2» zu den Stützpunkten 0 / 10.6 / 13.7 | nur Bild |
| Quadratisch (36.2 s, ab 7.0) | B (schwach) | «Für k kleiner als neun … zwei Lösungen» – die Parabel steht bis 9.4 bei \(k=5\) | Kurz durch mehrere \(k<9\) fahren (z. B. \(v\) −9→−4), dann wie heute weiter; \(k\)-Wert als Notiz | neue Bewegung |
| Zuerst a prüfen (53.2–73.6 s) | A + B | 20 s ohne jedes Bild, obwohl «linear», «eine Lösung», «zwei», «keine» gesagt wird. sim5, Familie C, zieht \(k\) genau durch den Fall «Leitkoeffizient 0» | Ideal: \(mx^2-4x-3\) für \(m\) von 1 über 0 bis −2 stetig zeigen. Das geht heute nicht: Scheitel- und Linearfaktorform laufen bei \(m=0\) davon → **Werkzeug-Erweiterung** (Parabel-`bewegung` in Normalform \([t,a,b,c]\)). Behelf: feste `parabeln` mit a, b, c nacheinander zu den Sätzen – \(m=1\) (zwei Lösungen), Gerade \(-4x-3\) bei 5.7, \(m=-\tfrac43\) berührt bei 13.6, \(m=-2\) ohne Lösung | Werkzeug-Erweiterung / Behelf nur Bild |

## Lineare Funktionen (GF 3.2)

### `g3-2-lp-m-und-b` · LF Kap. 1 (sim1: Regler m, b) · 1:37 · Von der Wertetabelle zur Geraden; b schiebt die Gerade senkrecht, m kippt sie um (0 | b).

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Wertetabelle (11.3 / 15.3 s) | A, Timing | Alle sechs Punkte erscheinen bei 11.3 s auf einmal, «Jedes Wertepaar wird ein Punkt» kommt erst bei 15.32 s (4 s später). Den Einleitungssatz «… nach oben, nach unten oder gar nicht» (0.6–5.0 s) begleitet kein Bild. | `ein` des Grafs auf ≈ 15.3 s setzen. Optional schon im ersten Satz eine Gerade, die 2 → −1 → 0 kippt. | nur Bild / neue Bewegung |
| Merke (77.9 s; Bewegung bei 1.0–6.0 s) | A, Timing | Zu «b … schiebt die Gerade senkrecht» (1.3–3.0 s) kippt das Bild bereits. «Positives m steigt, negatives fällt, m gleich null bleibt waagrecht» (8.2–12.3 s) läuft über einem stehenden Bild mit m = 2; die Waagrechte kommt nicht vor. | Stützpunkte neu legen: b-Verschiebung bei 1.3–3.0 s, Kippen bei 3–8 s, dann bei 8.2–12.3 s m = 2 → −1 → 0 und bei 0 halten. | neue Bewegung |
| m als Schritt / Merke (69–91 s) | Nebenbefund | Das Label «Δx = 1» des Steigungsdreiecks bei x = 0 liegt genau auf «(0 \| 1)» und ist unleserlich (Bilder 71–88 s). | Dreieck bei x = 1 ansetzen, wie in sim1. | nur Bild |

B: keine Befunde. b und m werden schon so bewegt wie in sim1, mit gestrichelter Ursprungsgerade und Dreieck bei x = 1.

### `g3-2-lp-steigungsdreieck` · LF Kap. 2 (sim2: Regler m, b, Δx) · 1:45 · m = Δy/Δx am wachsenden und schrumpfenden Dreieck, Leserichtung, Nullstelle, Δx = 0.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Leserichtung (47.6–52.6 s, 0–5.0 s) | A | Fünf Sekunden lang steht bei B ein leeres Dreieck mit «Δx = 0, Δy = 0» (Bild 49 s). Gleichzeitig heisst es «… mit Delta x grösser als null». Das «Δx = 0» nimmt die spätere Szene «Delta x null» vorweg. | Dreieck erst ab dem Bewegungsbeginn zeigen. Allgemein: Der Abspieler sollte die Δ-Beschriftungen bei dx = 0 ausblenden. | Werkzeug-Erweiterung (klein) |
| dasselbe in «Grosses Dreieck» (6.6–7.8 s) und «Ein Beispiel» (34.5–36.1 s) | A | «Δx = 0 / Δy = 0» liegt über den Labels von P bzw. A, bevor das Dreieck wächst. | wie oben | wie oben |
| Delta x null (72.8 s ff.) | A | Gesagt wird «zwei verschiedene Punkte mit derselben x-Koordinate … Die Gerade … steht senkrecht». Gezeigt werden zehn unbeschriftete rote Punkte, keine Gerade. | Zwei beschriftete Punkte, z. B. (2 \| −1) und (2 \| 3), dazu eine rote senkrechte Linie aus `figuren` als `strecke`. | nur Bild |
| Merke (94.3–96.6 s, 8.0–10.3 s) | A | «die Nullstelle ist minus b durch m»: Die Nullstelle (−1.25 \| 0) ist im Bild nicht markiert. | Begleiter `nullstelle` an die bewegte Gerade hängen. | nur Bild |
| Die Nullstelle (57.5 s, 15 s lang) | B, schwach | Gerade und Nullstelle stehen fest. In sim2 wandert die Nullstelle mit den Reglern («Stell eine Gerade mit der Nullstelle 3 ein»). | Zu «Der Achsenabschnitt minus sechs liegt ganz woanders» (11.7–14.5 s) b z. B. von −6 nach −4 schieben. Dabei laufen (0 \| b) und x₀ sichtbar verschieden. | neue Bewegung |

### `g3-2-lp-typen` · LF Kap. 3 (sim3: g fest, h mit Reglern m₂, b₂) · 1:44 · Proportional, Identität, konstant, senkrecht (keine Funktion), parallel, senkrecht zueinander, warum −1.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Proportional (13.1–15.3 s, 4.2–6.4 s) | A | «doppeltes x gibt doppeltes f von x» wird nicht gezeigt. | `marken` bei x = 1 und x = 2 («f(1) = {y}», «f(2) = {y}») an die bewegte Gerade. | nur Bild |
| Identität (23.9–29.0 s, 5.5–10.6 s) | A | «halbiert den Winkel zwischen der positiven x-Achse und der positiven y-Achse» wird nicht gezeigt. | Zwei 45°-Winkelbögen bei (0 \| 0) aus `figuren`/`winkel`. | nur Bild |
| Parallel (57.4–59.5 s, 6.6–8.8 s) | A, Timing | «ist auch b gleich, ist es dieselbe Gerade»: Die Bewegung (b 4 → −3) ist schon bei 3.8 s fertig. Deckungsgleich waren die Geraden nur kurz bei ≈ 2.2 s, also rund 4.4 s vor dem Satz. | Stützpunkte neu legen: b → −3 während «parallel … treffen sich nie» (3.5–6.5 s), dann b → 1 bei 6.6–8.8 s. | neue Bewegung |
| Warum minus eins (75.5–79.3 s, 5.3–9.2 s) | A | «Dreht man das Dreieck um neunzig Grad»: Nichts dreht sich. Ein neues Dreieck wächst bei 7.0–10.8 s aus dx = 0, anfangs mit «Δx = 0, Δy = −0» auf (0 \| 1) (Bild 73 s). Die Labels der zwei Dreiecke liegen übereinander. | Ein sich drehendes Dreieck braucht eine bewegte Figur, die der Bauer nicht hat. Ersatz ohne Werkzeug: das erste Dreieck gestrichelt stehen lassen und das zweite mit Abstand zu (0 \| 1) ansetzen. | Werkzeug-Erweiterung oder nur Bild |
| Merke (84.6–87.5 s, 0.9–3.8 s) | A, Timing | Die senkrechte Gerade rastet schon während «proportional … konstant» (0.4–5.2 s) ein. «senkrecht heisst Produkt … minus eins» kommt erst bei 7.1–13.4 s. Für proportional, konstant und parallel gibt es kein Bild. | Zweite Gerade synchron durch die Fälle führen: b → 0, m → 1, m → 0, parallel, zuletzt das Einrasten bei ≈ 10–12 s. | neue Bewegung |

B: keine Befunde. Das Einrasten senkrecht ist die Brücke zu sim3. Live m₁·m₂ wie in der Animation ginge nur mit Live-Zahlen in der Formelzeile, und die kann der Bauer noch nicht.

### `g3-2-lp-aufstellen` · LF Kap. 4 (sim4: m und b einstellen, Fälle A–D) · 1:47 · Ansatz y = mx + b aus m und Punkt, aus zwei Punkten, aus einer Lage, aus einem Sachtext.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Punkt einsetzen (25.1 s, 2.4 s) | A, Timing | Die Notiz «Probe: … = −1 ✓» erscheint bei 2.4 s. Die Gerade liegt da noch bei b = −4, nicht durch P (Bild 26 s), und rastet erst bei 8.6–10.9 s ein. Die Probe wird nicht gesprochen. | Notiz-`ein` ≈ 10.9 s, nach dem Einrasten. | nur Bild |
| Zwei Punkte: dann b (48.9 s, 2.4 s) | A, Timing | Die Notiz «Probe mit A … ✓» steht 7 s vor dem Satz «Die Probe mit A bestätigt es» (9.4 s) und vor der Gerade durch A (5.8 s). A und B sind von Anfang an grün («bestätigt»). | Notiz-`ein` ≈ 9.4 s. Punkte bis dahin in Tinte. | nur Bild |
| Aus einer Lage (60.8 s, 2.4 s) | A, Timing | Die Lösung «b = 1.5, also y = −0.5x + 1.5» steht ab 2.4 s da. Die Gerade dreht sich erst bei 6.8–9.4 s, die Verschiebung kommt bei 12.2–14.2 s («Punkt einsetzen, b ausrechnen», 12.5 s). Die Lösung ist damit rund 10 s zu früh. | Notiz-`ein` ≈ 12.4 s. | nur Bild |
| Zwei Punkte: erst m (34.7–39.5 s) | A | Das Dreieck mit dx = 0 zeigt «Δx = 0, Δy = 0» auf A (Bild 38 s). Später liegt «Δx = 3» auf «A(−2 \| −2)» (Bild 43 s). | wie im Clip steigungsdreieck | Werkzeug-Erweiterung (klein) |
| Aus einem Sachtext (84.9–88.5 s, 11.2–14.9 s) | A, schwach | «nur dort [ab x = 0] ist die Gerade sinnvoll»: Die Gerade läuft auch links der y-Achse weiter. | Für bewegte Geraden `von`/`bis` ergänzen. Die Doku nennt das bisher nur für `kurven`. | Werkzeug-Erweiterung |

B: keine Befunde. b gleitet durch P, die Gerade dreht sich auf senkrecht und verschiebt sich dann. Das entspricht den Fällen A, C und D von sim4.

## Quadratische Funktionen (GF 3.3)

### `g3-3-lp-verschieben` · QF Kap. 1 (sim1: Regler a, xₛ, yₛ) · 1:41 · Normalparabel aus der Wertetabelle, dann yₛ, xₛ und a einzeln, zusammen und im Merke.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Wertetabelle (0.05 / 9.6 s) | A, Timing | Alle Punkte sind ab 0.05 s da. «Jedes Wertepaar wird ein Punkt» folgt erst bei 9.64 s. | Graf-`ein` ≈ 9.6 s. | nur Bild |
| Merke (82.6–91.1 s, 1.4–9.8 s) | A/B | «a formt … xₛ schiebt waagrecht … yₛ schiebt senkrecht» läuft über einem stehenden Bild S(2 \| −1). In sim1 bewegt man genau diese drei Regler. | Kurze Wiederholung im Takt der Sätze: a 1 → 2 → 1, u 0 → 2, v 0 → −1. | neue Bewegung |

Sonst gibt es nichts zu beanstanden. Jede Verschiebung läuft zu ihrem Satz, «Jetzt du» führt zurück zur Normalparabel, also zum Startzustand von sim1.

### `g3-3-lp-drei-formen` · QF Kap. 2 (sim2: Regler a, xₛ, yₛ; Formen anklickbar) · 1:01 · Grundform zeigt c, Scheitelform den Scheitel, Produktform die Nullstellen; bei yₛ > 0 keine Produktform.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Grundform (7.6–8.8 s, 0–1.2 s) | A, schwach | In der Grundform-Szene steht der Läufer zuerst auf dem Scheitel mit «(2 \| −1)» (Bild 9 s). | Läufer bei x = 1 oder 3 starten. | nur Bild |
| ganzer Clip | B | a ist im ganzen Clip 1. sim2 hat einen a-Regler, die Produktform heisst dort a·(…)(…), und eine Aufgabe verlangt −x² − 2x + 3. Im Clip steht die Produktform ohne Faktor a. | In «Alle drei» oder einer neuen Szene a 1 → −1 bewegen, mit Begleitern `yachse`, `scheitel` und `nullstellen`. c kippt, die Nullstellen bleiben. | neue Bewegung und Neuvertonung (ein Satz) |
| Merke (46.4 s) | A, schwach | Die drei Formeln erscheinen nacheinander, aber alle vier Punkte samt Labels stehen ab 0.2 s. In sim2 erscheinen die Labels erst beim Klick. | Je Punkt ein eigenes `ein` (oder überlagerte Grafs). | Werkzeug-Erweiterung |

### `g3-3-lp-achse-bleibt` · QF Kap. 3 (sim3: Regler **b und c**, a = 1, Achse und D live) · 1:07 · Nur c ändert sich; D > 0, = 0, < 0; die Symmetrieachse x = −b/(2a) bleibt.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Achse / Merke (40.2 s ff.) | B | Gesagt wird «minus b durch zwei a», aber b bewegt sich nie, und die Achse ist eine feste Kurve bei x = 2. In sim3 ist b ein Regler («Schieb b auf 2. Wo liegt jetzt die Symmetrieachse?»), und die Achse wandert mit. | Nach «Darin kommt c nicht vor» b −4 → 2 bewegen; Scheitel und Achse wandern nach x = −1. Dazu braucht der Bauer einen Begleiter «Symmetrieachse x = u» für bewegte Parabeln. | Werkzeug-Erweiterung und Neuvertonung (ein Satz) |
| Merke (51.2–56.9 s) | A, schwach | Zu «c hebt und senkt die Parabel» stehen drei gleichfarbige Parabeln für c = 3, 4, 7 still. Welche Kurve zu welcher D-Zeile gehört, sieht man nicht. | Eine Parabel durch c = 3 → 4 → 7, mit `nullstellen`, im Takt der Zeilen D > 0, = 0, < 0. | neue Bewegung |

### `g3-3-lp-a-finden` · QF Kap. 4 (sim4: Regler a; Fall A Scheitel + Punkt, Fall B Nullstellen + Punkt) · 0:56 · a durch Probieren (zu schmal, zu breit, Treffer), dann durch Einsetzen.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Merke (≈ 42.8–45.1 s) | A und B | «Nullstellen und Punkt: a(x − x₁)(x − x₂)» steht nur als Formel da, ohne Bild. Fall B von sim4 (Nullstellen −1 und 3 fest, P(1 \| −8), a schieben) hat im Clip keine Brücke. | Neue Szene: Nullstellen fest, a gleitet, bis die Kurve P trifft. Geht heute mit `kurven` und `"polynom": true`, Stützpunkte [t, a, x₁, x₂]. | neue Bewegung und Neuvertonung |

Fall A ist gut überbrückt: a gleitet von −0.3 über −0.1 nach −0.25, mit Live-Marke h(0).

### `g3-3-lp-mitte` · QF Kap. 5 (sim5: Regler x, **Rechteck x × (18 − x)** und Graph) · 1:00 · Zaun 40 m, A(x) = x(20 − x), gleich hohe Punkte, Maximum in der Mitte.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Titel, x = 4, x = 16, x = 10 (0–37 s) | **A und B (Hauptbefund)** | «Vierzig Meter Zaun, ein rechteckiges Feld … die andere zwanzig minus x», «dasselbe Feld, nur gedreht», «Das Quadrat …»: Ein Feld ist nie zu sehen, nur Graph und Läufer. sim5 zeigt das Rechteck, das sich mit dem Regler verformt. | Sofort möglich: je Szene ein festes Rechteck aus `figuren`/`vieleck` in einem zweiten Graf mit `"achsen": false` (4 × 16, 16 × 4, 10 × 10). Eine echte Brücke wäre ein Rechteck, das mit dem Läufer mitwächst. | nur Bild; bewegt: Werkzeug-Erweiterung |
| Mitte (25.8–29.7 s, 4.2–8.1 s) | A | «Der Scheitel liegt in der Mitte … bei zehn»: Im Bild ist bei x = 10 weder Scheitel noch Achse markiert (Bilder 24 und 28 s). | Punkt S(10 \| 100) oder eine Achse bei x = 10 mit `ein` ≈ 4.5 s. | nur Bild |
| Merke (52.6–53.8 s) | A, schwach | Zu «a positiv Minimum» gibt es kein Bild. | Weglassen oder kurz eine nach oben geöffnete Parabel zeigen. | nur Bild |

## Planimetrie (GF 5.2)

### `g5-2-lp-dreiecke` · Kap. 1 Dreiecke beschreiben (sim1: Ecke C ziehen) · 107.9 s
Beschriftung, Winkelsumme über die Parallele, Sonderdreiecke, Höhe, Transversalen und ihre Schnittpunkte.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Beschriften (0 s) | A (Zeit) | b, c erscheinen mit a bei 5.0, gesagt bei 7.3 / 8.8. γ erscheint bei 10.4, gesagt bei 13.4 (3 s früher) | Seiten und Winkel einzeln einblenden (5.0 / 7.3 / 8.8 bzw. 10.4 / 12.3 / 13.4) | nur Bild |
| Winkelsumme (14.9 s) | B | sim1, Aufgabe 1: «Zieh die Ecke C herum. Was bleibt gleich?» Der Clip zeigt ein festes Dreieck | C entlang der Parallelen schieben, die drei Winkelbögen laufen mit, die Summe bleibt 180° | Werkzeug-Erweiterung (Behelf: 2–3 Dreiecke nacheinander, nur Bild) |
| Vorgelöst (29.2 s) | A | «α = 50°, β = 60° … γ = 70°» – kein Bild | Dreieck mit diesen Winkeln und Bögen | nur Bild |
| Spezielle Dreiecke (38.5 s) | A (Zeit) | Alle drei Dreiecke stehen ab 0.3. «rechtwinklig» kommt bei 11.7, «gleichseitig … 60°» bei 7.7; gleiche Seiten und 60°-Bögen fehlen | Dreiecke einzeln zu den Sätzen einblenden (2.5 / 7.7 / 11.7); Gleichheitsstriche und 60°-Bögen | nur Bild |
| dito | B | sim1: «gleichschenklig mit Basis c einstellen», «rechten Winkel bei C einstellen» | C zieht das Dreieck nacheinander in die Sonderformen | Werkzeug-Erweiterung |
| Die Höhe (53.0 s) | B | sim1: «Mach das Dreieck bei A stumpfwinklig. Wo liegt der Fusspunkt?» Der Clip zeigt nur die Endlage | C wandert von spitz zu stumpf, der Fusspunkt verlässt die Seite c | Werkzeug-Erweiterung |
| Schnittpunkte (75.1 s, ab 6.5) | A | «Ebenso … Höhen, Winkelhalbierende, Mittelsenkrechte … Beim stumpfen Dreieck liegen H und M_U aussen» – im Bild nur die Seitenhalbierenden mit S. Die Notiz listet ab 0.6 alle vier | Je Satzteil ein Bild mit den drei Linien und H, M_I, M_U (6.5–13.7). Bei 13.9 ein stumpfes Dreieck mit H und M_U aussen | nur Bild |

### `g5-2-lp-flaeche` · Kap. 2 Dreiecksfläche und zugehörige Höhe (sim2: Spitze t) · 73.3 s
Grundseite und Höhe, Begründung über das Parallelogramm, stumpfes Beispiel, Spitze verschieben bei gleicher Fläche.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Warum die Hälfte (9.1 s, ab 0.7) | A/B | «Leg ein zweites, gleiches Dreieck **gedreht** daneben» – es springt bei 1.6 fertig ins Bild | 180°-Drehung um die Mitte von BC zeigen | Werkzeug-Erweiterung (Behelf: Zwischenstand, nur Bild) |
| Stumpf vorgelöst (30.1 s, ab 14.1) | A | «Probe: Das Rechteck acht mal drei hat vierundzwanzig» – kein Rechteck im Bild (geprüft bei 47 s) | Gestricheltes Rechteck (0\|1)–(8\|4) bei 14.1 | nur Bild |
| Spitze verschieben (48.4 s) | A | «Grundseite und Höhe bleiben gleich» – in den drei Dreiecken ist keine Höhe gezeichnet | Höhe je Dreieck | nur Bild |
| dito | B | sim2: «Verschieb die Spitze nach t = 10». Im Clip drei feste Überlagerungen (0.3 / 2.4 / 3.4) | Die Spitze gleitet auf der gestrichelten Parallelen, die Höhe läuft mit, «A = 12 cm²» bleibt stehen | Werkzeug-Erweiterung |

### `g5-2-lp-vierecke` · Kap. 3 Vierecke (sim3: Trapez mit c, h, d) · 77.0 s
Vierecksfamilie, Flächen von Parallelogramm, Trapez (Mittellinie), Raute/Drachen und Trapez mit Pythagoras.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Die Familie (0 s) | B | «Jedes Quadrat ist ein Rechteck … jedes Parallelogramm ein Trapez» – sechs feste Figuren. sim3: «Mach aus dem Trapez ein Parallelogramm» | Ein Trapez geht stetig über in Parallelogramm, Rechteck und Quadrat | Werkzeug-Erweiterung |
| Parallelogramm (11.0 s, ab 0.5) | A/B | «Schneid … ein Dreieck ab und setz es rechts an: Es entsteht ein Rechteck» – rotes und grünes Dreieck erscheinen gleichzeitig bei 2.6. Das Verschieben fehlt, das Rechteck ist nicht umrandet (geprüft bei 19 s) | Dreieck um 6 nach rechts verschieben, danach Rechteck (2\|1)–(8\|4) umranden | Verschieben: Werkzeug-Erweiterung; Umranden: nur Bild |
| Trapez (21.0 s, ab 3.7) | A | «Fläche gleich Mittellinie mal Höhe» – keine Höhe im Bild | Höhe h mit rechtem Winkel | nur Bild |
| dito | B | sim3, Aufgabe 1: «Verschieb die obere Seite mit d. Was bleibt gleich?» | c verschieben, m und A bleiben gleich | Werkzeug-Erweiterung |
| Raute und Drachen (32.6 s) | A | «Raute **und Drachen** füllen genau die Hälfte des Rechtecks» – nur die Raute ist gezeichnet, und die Halbierung ist nicht sichtbar | Drachen dazunehmen; die vier Eckdreiecke als Gegenstücke einfärben | nur Bild |
| Fehlende Länge (40.9 s, ab 5.1) | A | «Links **und rechts** steht je drei Zentimeter über» – nur links ist ein Dreieck markiert | Rechtes Dreieck spiegeln | nur Bild |

### `g5-2-lp-kreis` · Kap. 4 Kreis und Kreisteile (sim4: r, φ) · 105.8 s
Passante, Tangente, Sekante, Sehne; Umfang und Fläche; Bogen, Sektor, Segment, Kreisring.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Bogen und Sektor (17.3 s, ab 3.6) | B | «Er ist der Anteil Phi durch dreihundertsechzig Grad» – fester 60°-Sektor. sim4, Aufgabe 1: «Zieh an φ. Welchen Anteil …?» | Sektor öffnet sich von 0° über 90° und 180° bis 60° zurück | Werkzeug-Erweiterung (Behelf: Zwischenstände, nur Bild) |
| Vorgelöst (27.7 s, ab 4.2) | A | «Sechzig Grad sind ein Sechstel des Kreises» – der Kreis ist nicht in Sechstel geteilt | Fünf weitere Radien im 60°-Abstand, gestrichelt | nur Bild |
| Segment (47.4 s, ab 7.2) | A (Zeit) | h-Linie und Formel bei 7.2, Satz «Seine Höhe …» erst bei 9.5 (2.3 s). Das Segment selbst ist nicht abgesetzt, nur Sektor und Dreieck überlagert (geprüft bei 60 s) | `ein` auf 9.5; Segment allein kräftiger füllen oder umranden | nur Bild |

Linien am Kreis und Kreisring sind synchron und vollständig.

### `g5-2-lp-aehnlichkeit` · Kap. 5 Ähnlichkeit (sim5: Streckfaktor k, auch negativ) · 80.1 s
Zentrische Streckung mit k = 2 und k = −1, Längen mal k, Flächen mal k², Strahlensatz, Baumhöhe.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Zentrische Streckung (0 s, ab 5.0) | B | «Mit k gleich zwei wird sein Abstand zu Z doppelt so gross» – das Bilddreieck springt bei 8.3 ins Bild. sim5: «Zieh an k» | Das Bild wächst entlang der Strahlen von k = 1 bis k = 2 | Werkzeug-Erweiterung |
| Negativer Faktor (22.2 s, ab 1.7) | B | «gleich gross, aber um Z gedreht». sim5: «Zieh an k, auch unter null» | k läuft von 1 über 0 bis −1, das Bild schrumpft durch Z | Werkzeug-Erweiterung |
| Was bleibt, was wächst (10.9 s) | A (schwach) | «Die Winkel bleiben gleich» – keine Winkelbögen | Gleiche Bögen in Original und Bild | nur Bild |
| Strahlensätze (33.0 s, ab 11.7) | A | «SA Strich gleich sechs … A Strich B Strich gleich vier Komma fünf» – in der Figur stehen nur 4 und 3 | «6» an SA' und «4.5» an A'B' (diese bei 14.0) | nur Bild |

## Potenz- und Wurzelfunktionen (SP 3.2)

### `s3-2-lp-exponent` · Kapitel 1 · ≈ 1:30 · Gerade und ungerade Exponenten: Form, Symmetrie, gemeinsame Punkte, Streckung durch a.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Zwei Kurven (0–13 s) | A | «y gleich x Quadrat und y gleich x hoch drei» (3.2–6.6 s); der Graf erscheint erst bei 10.4 s. «bei minus zwei … vier, … minus acht»: Das Fenster reicht nur über x und y von −3 bis 3, die Punkte (−2 \| 4) und (−2 \| −8) sind gar nicht im Bild. | Graf bei etwa 3 s einblenden. Fenster in y auf [−9; 9] erweitern und die zwei Punkte bei x = −2 setzen. | nur Bild |
| n wächst (0.9–4.4 s) | A/B | «Zwischen minus eins und eins wird die Kurve flacher, aussen steiler» (4.8–7.4 s). Danach steht x⁵ allein da, es fehlt eine Vergleichskurve. In der Animation sim1 lässt sich die Bezugskurve y = x² zuschalten. | Gestrichelte y = x² stehen lassen, wie bei der Bezugskurve der Animation. | nur Bild |
| Gerade Funktion (0.8–3.6 s) | A | «Gerades n heisst: f(−x) = f(x)» (1.6–6.2 s). Die Bewegung mit `stufen` von 2 auf 4 zeigt um 2 s herum x³: Die Kurve ist dann punktsymmetrisch, der Punkt (−1 \| 1) liegt neben ihr. | x⁴ fest zeigen, oder den Sprung 2 → 4 in unter 0.1 s und vor 1.6 s legen. | nur Bild |
| Ungerade Funktion (0.8–3.6 s) | A | Gleicher Fall: Der Weg von 3 auf 5 zeigt kurz x⁴, der Punkt (−1 \| −1) liegt neben der Kurve, während «ungerades n» gesprochen wird. | Wie oben. | nur Bild |
| a streckt (3.4–8.8 s) | B | Die Formel zeigt nur «a», nie einen Wert. sim1 zeigt den Punkt (1 \| a) laufend an. | `marken: [{x: 1, text: "(1 \| {y})"}]` an die bewegte Kurve hängen; dann ist der Wert von a ablesbar. | nur Bild |

### `s3-2-lp-hyperbel` · Kapitel 2 · ≈ 1:24 · 1/x: Definitionslücke, Asymptoten, Ordnung und Parität, keine Nullstelle.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Asymptoten (0–9.6 s) | A | «Die beiden Achsen sind Asymptoten». Die `asymptoten` sind in Farbe 5 (Tinte) gestrichelt und decken sich mit den schwarzen Achsen; im Bild sind sie praktisch unsichtbar (Ausschnitt geprüft). Gilt auch für «Bei null ist Schluss» und «Merke». | Asymptoten in Farbe 4 oder 2 setzen. | nur Bild |
| Asymptoten / Ein neuer Fall | A | «so gross x auch wird», «je grösser x, desto kleiner y» beschreiben einen Vorgang. Gezeigt wird nur eine feste Marke bei x = 3.5 bzw. zwei feste Punkte. | Läufer, der nach rechts fährt und y mitschreibt. | Werkzeug-Erweiterung (Läufer für `kurven`) |
| ganzer Clip | B | sim2 hat einen Regler für a (−3…3), und die Aufgaben «beide Äste unten» und «f(1) = −2» brauchen ihn. Im Clip kommt a nicht vor. | In «Gerade Ordnung» 1/x² mit a von 1 auf −1 umklappen und einen Satz dazu sprechen. | neue Bewegung + Neuvertonung |

### `s3-2-lp-verschieben` · Kapitel 3 · ≈ 1:18 · Schema a(x−u)ⁿ+v, wandernde Asymptoten, Nullstellen einer verschobenen Potenzfunktion.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| u schiebt waagrecht | A | «Der ausgezeichnete Punkt … wandert mit» (6.5–11.4 s). Die Bewegung endet schon bei 3.8 s, der Punkt steht still, während der Satz fällt (2.7 s später). | Zweite Bewegung (u 2 → 0 → 2) bei etwa 6.5–10 s. | neue Bewegung |
| v schiebt senkrecht | A | Die Formel zeigt «− 2» schon ab 0.8 s, die Kurve sinkt erst ab 4.4 s: Text und Bild widersprechen sich 3.6 s lang (Regel im HOWTO zu Formelzeile und Bewegung). | Formel bei etwa 4.2 s einblenden. | nur Bild |
| Die Asymptoten wandern mit | A | «Der Kreuzungspunkt der beiden ist das neue Zentrum» (7.9–10.5 s); der Punkt ist nicht markiert. | `startpunkt` (u \| v) setzen, mit Beschriftung «(2 \| −1)». | nur Bild |
| Nullstellen (0–11 s) | A/B | Bis 5.4 s ist die Bühne leer. «Null gleich Klammer x minus drei hoch vier minus sechzehn» (4.3–8.8 s) steht nirgends geschrieben, der Graf kommt erst bei 11 s. | Zeile «0 = (x−3)⁴ − 16» bei etwa 4.3 s. Graf früh einblenden und x⁴ nach u = 3, v = −16 gleiten lassen (Brücke zu den u/v-Reglern von sim3). | nur Bild / neue Bewegung |

### `s3-2-lp-umkehren` · Kapitel 4 · ≈ 1:28 · Umkehrfunktion als Spiegelung an y = x, Einschränken bei geradem Exponenten, Rechenrezept.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Gerader Exponent: es geht schief | A | «über einem x liegen zwei Punkte» (3.3–5.4 s); es sind keine Punkte gesetzt. | Punkte (1 \| 1) und (1 \| −1) auf dem roten Spiegelbild, dazu eine senkrechte Hilfslinie x = 1. | nur Bild |
| Gerader Exponent | B | sim4 hat einen Regler n von 2 bis 6. Im Clip ist der Wechsel von x³ zu x² ein Schnitt zwischen zwei Szenen. | Bewegung n 3 → 2 mit `stufen` und `spiegel`: Das Spiegelbild kippt zur liegenden Parabel. | neue Bewegung |
| Einschränken | B | sim4 nimmt mit dem Haken «nur x ≥ 0» den linken Ast weg. Der Clip schneidet von der vollen Parabel auf `von: 0`. | Linken Ast ausblenden, während «schränkt … ein» gesprochen wird. | Werkzeug-Erweiterung (`von`/`bis` in `bewegung`) |

### `s3-2-lp-wurzel` · Kapitel 5 · ≈ 1:35 · Wurzel als Potenz, Definitionsmenge nach Parität, Verschieben, Vergleich mit x und x², Gleichung grafisch lösen.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Definitionsmenge | A | «dritte Wurzel aus minus acht ist minus zwei» (10–12.2 s): Das Fenster reicht in x nur von −3 bis 3, der Punkt (−8 \| −2) fehlt. Die Legende «ausgezogen/gestrichelt» kommt erst bei 9.6 s, beide Kurven stehen aber schon ab 0 s da. | Fenster in x auf [−9; 9], Punkt (−8 \| −2). Gestrichelte ∛x erst mit ihrer Formel (7.0 s) einblenden. | nur Bild |
| Definitionsmenge | B | Aufgabe in sim5: «Zieh an n. Wann beginnt die Kurve an einem Startpunkt …». Der Clip zeigt beide Kurven fest. | Bewegung p von 1/2 auf 1/3 (ohne `stufen`): Der linke Ast erscheint erst bei 1/3. | neue Bewegung |
| Verschieben wie immer | A/B | Leer bis 3.0 s, dann sofort die fertige Kurve 2√(x+1) − 4. (0 \| −2) und (3 \| 0) stehen ab 3 s da, gesprochen werden sie erst bei 12–15.6 s. sim5 hat Regler für a, u und v. | √x gestrichelt stehen lassen und auf a = 2, u = −1, v = −4 gleiten lassen. Die Punkte bei etwa 12 s einblenden. | neue Bewegung |
| Wer ist grösser? | A | Die Notiz nennt «bei x = 0.25: 0.5 > 0.25 > 0.0625», im Bild ist nichts markiert. | `marken` bei x = 0.25 an allen drei Kurven. | nur Bild |
| Grafisch lösen | A | Der Schnittpunkt (6 \| 2) steht ab 5.8 s da; «zeichnet die Kurve und die Gerade» fällt bei 6.2–9.7 s, «liest den Schnittpunkt ab» bei 9.9–12.9 s. | Kurve bei etwa 6.2 s, Gerade bei etwa 8 s, Punkt bei etwa 10.5 s (gestaffelte `graf`). | nur Bild |

## Polynomfunktionen (SP 3.3)

### `s3-3-lp-linearfaktoren` · Kapitel 1 · ≈ 1:38 · Grad und Leitkoeffizient, Produktform, Satz vom Nullprodukt, a aus einem Punkt.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Nullprodukt | A | Gesprochen in der Reihenfolge x − 1, x − 3, x + 2 (1.9–8.3 s). Die Formel zeigt ab 0.8 s nur «x + 2 = 0», das zuletzt Gesagte (etwa 6 s zu früh). Alle drei Nullstellen erscheinen auf einmal bei 1.9 s. | Drei Formelzeilen mit gestaffeltem `ein`, Nullstellen einzeln als `punkte` in gestaffelten Grafs. | nur Bild |
| Gleichung aus Nullstellen | A/B | Ab 1.8 s steht die fertige Kurve mit a = 1 durch (0 \| 6) im Bild; hergeleitet wird «a gleich eins» erst bei 12–14 s. sim1: «… Graph schneidet die y-Achse bei (0 \| 4)», gelöst über a. | Mit a = 0.5 beginnen (Punkt (0 \| 6) liegt daneben), dann a 0.5 → 1 bei etwa 12.1–13.5 s: Die Kurve läuft in den Punkt. | neue Bewegung |

### `s3-3-lp-vielfachheit` · Kapitel 2 · ≈ 1:35 · Doppelte und dreifache Nullstelle durch zusammenrückende Faktoren, Vorzeichen, Gleichung vom Graphen.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Merke (1.5–7.5 s) | A/B | «Einfache: schneiden. Doppelte: berühren … Dreifache: Terrasse.» Gezeigt wird nur der Fall mit der doppelten Nullstelle. sim2 schaltet k von 1 bis 3. | Kurze Wiederholung als Bewegung: drei Nullstellen → (x − 1)² → (x − 1)³, im Takt der drei Satzteile. | neue Bewegung |

Die Szenen «Doppelt» und «Dreifach» sind gut im Takt: Die Bewegung läuft genau mit «rückt … nach links» (0.5–3.3 s).

### `s3-3-lp-globalverlauf` · Kapitel 3 · ≈ 1:45 · Leitterm von weitem, Enden nach Grad und Vorzeichen, höchstens n Nullstellen, Symmetrie.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Nah dran | A | «f hat drei Nullstellen, x hoch drei nur eine» (8.4–11 s); keine Nullstellen markiert. | `nullstellen` an f, Punkt (0 \| 0) an x³. | nur Bild |
| Weiter weg / Ganz weit | A | «Jetzt zoomen wir hinaus»; gezeigt wird ein Szenenschnitt mit 1 s leerer Fläche. | Fenster stetig aufziehen. | Werkzeug-Erweiterung (bewegtes Fenster) |
| Nur höchstens | A | «Bei ungeradem Grad dagegen gibt es immer mindestens eine» (5.3–11.1 s); im Bild nur x² + 1. | Zweiter Graf bei etwa 5.2 s mit einer kubischen Kurve, z. B. `formel: "x**3+1"`. | nur Bild |
| Symmetrie | A/B | Gesprochen: nur gerade Exponenten, nur ungerade, gemischt. Gezeigt: nur 0.5x³ − 2x. sim3 hat den Regler d (konstantes Glied). | Bei «Gemischt» (13–14 s) d von 0 auf 1: Nullstellen von (−2, 0, 2) nach (−2.214, 0.539, 1.675), das ergibt genau 0.5x³ − 2x + 1 (mit numpy nachgerechnet). Für «nur gerade» einen Graf mit 0.25(x+2)(x+1)(x−1)(x−2). | neue Bewegung |

### `s3-3-lp-nullstellen-berechnen` · Kapitel 4 · ≈ 1:53 · Ausklammern, Nullstelle raten, Linearfaktor abspalten, Koeffizientenvergleich, Faktorisieren.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Raten | B | sim4 ist eine Probestelle r, die über die Teiler fährt. Der Clip zeigt nur das Ergebnis f(1) = 0 (10.6 s). | Läufer über ±1, ±2, ±3 mit Live-Wert f(r). | Werkzeug-Erweiterung (Läufer für `kurven`) |
| Vergleichen | A | «Vor x Quadrat: p − 1 = −2 …»: Weder f(x) = x³ − 2x² − 5x + 6 noch die ausmultiplizierte Form stehen in dieser Szene; die Zahlen −2, −5, 6 sind nicht zu sehen. | Beide Zeilen oben stehen lassen, die Ergebnisse darunter. | nur Bild |

### `s3-3-lp-extrema` · Kapitel 5 · ≈ 1:50 · Hoch- und Tiefpunkt, lokal und absolut, Randextrema, Scheitel beim Grad 2, Schachtel-Anwendung.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Hoch und tief | A/B | «hört der Graph auf zu steigen und beginnt zu fallen» beschreibt einen Vorgang; H und T stehen ab 3.0 s fest da, T wird erst bei 8.7–13.2 s genannt. sim5 ist ganz auf einen Läufer x gebaut. | Läufer fährt von links über H und T, mit Live-Koordinaten. | Werkzeug-Erweiterung (Läufer für `kurven`) |
| Lokal | A | «Das Maximum bei H» (8–10.4 s); `beschriftung: false`, H ist nicht benannt. | Beschriftung H einschalten. | nur Bild |
| Am Rand | B | sim5 hat die Regler «D von» und «D bis» und zeigt die ganze Kurve blass dahinter. Im Clip ist die Kurve ab 1.0 s fest auf [−1.5; 2.5] gekürzt. | Heute möglich: die ganze Kurve blass gestrichelt dahinter. Ideal: das Intervall zieht sich zusammen. | nur Bild / Werkzeug-Erweiterung (`von`/`bis` bewegt) |
| Anwendung | A | «Die offene Schachtel aus einem Karton von zwanzig mal fünfzehn Zentimetern»: Es gibt kein Bild der Schachtel. «H ≈ (2.83 \| 379)» steht ab 1.0 s, gesprochen wird es erst bei 14.4–20 s. | Netz (Rechteck 20 × 15 mit Eckquadraten x) als `figuren` vor dem Grafen. Punkt H erst bei 14.4 s. | nur Bild |

## Exponential- und Logarithmusfunktionen (SP 3.4)

### `s3-4-lp-exponentialfunktion` · Kap. 1 Exponentialfunktion · 1:21 · Faktor je Schritt, Basis a (2→3→1.5), Zerfall, Spiegelbild, Asymptote, Basis aus einem Punkt.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Gleicher Faktor (3.0 / 6.6–11.6) | A | Alle sechs Punkte und die ganze Tabelle stehen ab 3.0. Gesprochen wird «ein Viertel, ein Halb, eins, zwei, vier, acht» erst ab 6.6, also 3.6 bis 8.6 s später. «mal zwei» je Schritt ist nicht zu sehen. | Punkte einzeln zum Wort einblenden, dazu Schrittpfeile ×2. | Werkzeug-Erweiterung (`ein` je Punkt; Notlösung: mehrere `graf` übereinander) |
| Die Basis (4.9–8.1) | A | «Drei hoch x ist steiler» (etwa 3.3–4.8): Die Kurve erreicht a = 3 erst bei 6.5. «eins Komma fünf … flacher» (4.96–6.56): Die Bewegung zu 1.5 läuft erst 6.7–8.1, während schon «Ein Punkt bleibt immer gleich» kommt. Etwa 1.5–1.7 s zu spät. | Stützpunkte um etwa 1.5 s vorziehen: [3.4,2] [4.8,3] [5.0,3] [6.4,1.5]. | nur Bild |
| Basis aus einem Punkt (0.4 / 5.44) | A + B | Die fertige Kurve 3^x durch (2 \| 9) steht schon ab 0.4. «Also ist a gleich drei» kommt erst ab 5.44, das Bild verrät das Ergebnis. In sim1 heisst die Aufgabe «Stell die Kurve ein, die durch (2 \| 6.25) geht» und wird mit dem Regler gelöst. | Kurve mit a = 1.5 beginnen lassen, bei 5.4–7.5 auf a = 3 ziehen, Marke bei x = 2 «(2 \| {y})» läuft mit bis 9. | neue Bewegung |

### `s3-4-lp-wachstum-zerfall` · Kap. 2 Wachstum und Zerfall · 1:18 · N₀ · a^t, Prozent→Faktor, Verdopplungs- und Halbwertszeit, Quotiententest.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Startwert und Faktor (2.0 / 7.66–10.9) | A + B | Die Punkte 300, 450, 675 stehen ab 2.0, gesprochen werden sie erst ab 7.66 (6–9 s später). sim2 hat einen Läufer t, der N(t) abliest. | Läufer auf der Kurve t = 0→1→2→3 mit «({x} \| {y})», zum Aufzählen. | Werkzeug-Erweiterung (`laeufer` für `kurven`) |
| Verdopplungszeit (1.0 / 4.64–8.82) | A | «nach drei … sechs … neun»: Die Punkte stehen ab 1.0, also 4–8 s früher. | Punkte zeitversetzt einblenden. | Werkzeug-Erweiterung (`ein` je Punkt) |
| Halbwertszeit (1.0 / 5.78–10.2) | A | «nach vier … acht … zwölf»: Die Punkte stehen ab 1.0, 5–9 s früher. | wie oben | Werkzeug-Erweiterung |
| Exponentiell oder linear (7.96–10.28) | A | «Bei linearem Wachstum wäre die Differenz gleich», aber eine lineare Vergleichsreihe ist nicht zu sehen. | Gestrichelte Gerade durch (0 \| 50) mit Steigung 10 ab 7.9 einblenden. | nur Bild |
| ganzer Clip | B | Regler N₀ in sim2 (50–500): Der Startwert bewegt sich im Clip nie. | Optional in «Startwert und Faktor»: c von 200 auf 400 und zurück, der Startpunkt läuft mit. | neue Bewegung |

### `s3-4-lp-e-funktion` · Kap. 3 e-Funktion und Basiswechsel · 1:20 · Grenzwert e, e^x zwischen 2^x und 3^x, 8^x = 2^{3x}, a^x = e^{(ln a)x}, Vorzeichen von b.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Die Zahl e (3.0 / 9.1 / 12.3) | A | Die Tabelle mit 2.718 steht ab 3.0, «e, ungefähr zwei Komma sieben eins acht» kommt erst ab 12.3 (9 s). Die Formel «→ e ≈ 2.718» steht ab 9.1, also 3.2 s zu früh. | Tabelle spaltenweise aufbauen (mehrere `formel`), die Grenzwertformel auf 12.3 legen. | nur Bild |
| Zur Basis e (0–10.8) | B | «zwei hoch x gleich e hoch ln zwei mal x … ungefähr null Komma sechs neun»: Die beiden Kurven liegen von Anfang an fest aufeinander. In sim3 wird b gezogen, bis e^{bx} auf dem Ziel liegt. | e^{bx} mit b = 1 starten (a = e) und bei etwa 5.3–8 auf b = 0.69 ziehen (a = 2), bis die Kurve auf der gestrichelten 2^x liegt. | neue Bewegung |

### `s3-4-lp-saettigung` · Kap. 4 Sättigung · 1:15 · Kaffee 80→20 °C, Rückstand halbiert sich alle 10 min, allgemeine Form, Erwärmen (Akku).

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Startwert und Sättigungswert (5.76–8.54) | A | «Dazwischen liegt der Rückstand: sechzig Grad am Anfang»: Der Abstand ist nicht eingezeichnet. | Senkrechte `figuren`-Strecke von (0 \| 20) nach (0 \| 80) mit «60» ab 5.7. | nur Bild |
| Der Rückstand zerfällt (3.78–9.16) | A | «sechzig, dreissig, fünfzehn, sieben Komma fünf Grad»: Keine Abstände zu y = 20. sim4 zeichnet genau diesen Abstand bei t = 10. | Senkrechte Strecken bei t = 10, 20, 30 bis zur Asymptote, einzeln zum Wort. | nur Bild |
| Ein Kaffee kühlt ab (6.14–8.76) | B (schwach) | «erst schnell, dann immer langsamer»: Das Bild ist fest. | Läufer, der den Abkühlverlauf abfährt. | Werkzeug-Erweiterung |
| Erwärmen (0.54–9.98) | A + B | «Die Form ist dieselbe, nur gespiegelt»: Es kommt ein neues Bild ohne Vergleich. sim4 zieht A durch S, eine Aufgabe ist «Startwert = Sättigungswert». | Im selben Fenster c von +40 über 0 nach −40 bewegen (v = 50, A 90→50→10): fallend, waagrecht, steigend. | neue Bewegung |
| Merke (7.90–9.72) | A + B | «je grösser k, desto schneller»: Das Bild ist fest. Die erste Aufgabe in sim4 lautet «Zieh an k». | a = e^{−k} von 0.933 (k ≈ 0.07) nach 0.80 (k ≈ 0.22) und zurück. | neue Bewegung |

### `s3-4-lp-logarithmusfunktion` · Kap. 5 Logarithmusfunktion · 1:18 · Umkehrfrage 2^x = 8, Spiegelung an y = x, vertauschte Rollen, Basis, Gleichung 3 · 2^t = 96.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Die Umkehrfrage (3.62–4.92) | A | «Wie viele Schritte braucht es bis acht?»: Die Leserichtung von y = 8 zurück zu x = 3 wird nicht gezeigt. | Gestrichelt (0 \| 8)→(3 \| 8)→(3 \| 0) ab etwa 4 einblenden. | nur Bild |
| Was sich vertauscht (2.3 / 5.30–11.6) | A | Alle drei Notizen stehen ab 2.3. «Asymptote» kommt bei 5.3, «Definitionsmenge» bei 8.6. Ausserdem stösst die Beschriftung «(1 \| 0)» mit der Achszahl 2 zusammen. | Notiz zeilenweise auf den Ton legen, Beschriftung versetzen. | nur Bild |
| ganzer Clip | B | sim5 dreht sich um einen Läufer, der log_a x abliest («Wo ist der Logarithmus negativ, wo null?»). Der Clip hat keinen Läufer. | Läufer auf der Logarithmuskurve x = 0.5→1→8 mit «({x} \| {y})», etwa in «Was sich vertauscht». | Werkzeug-Erweiterung |
| Merke (7.32–13.3) | A (schwach) | «Sie geht durch eins, null, hat die y-Achse als Asymptote»: Weder Punkt noch Asymptote sind eingezeichnet. | Punkt (1 \| 0) und x = 0 gestrichelt einzeichnen. | nur Bild |

---

## Trigonometrische Funktionen (SP 3.5)

### `s3-5-lp-kreis-kurve` · Kap. 1 Vom Einheitskreis zur Kurve · 1:17 · Bogenmass, Abrollen sin, fünf Stützstellen, Cosinus als waagrechte Koordinate.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Fünf Stützstellen (0.3 / 10.48–12.3) | A | «Dazwischen zieht man einen weichen Bogen», aber die ganze Kurve steht schon ab 0.3 (10 s vorher). Die Werte der Tabelle (ab 2.6) werden erst bei 6.1–9.9 genannt. | Erst nur die fünf Punkte zeigen, Kurve ab 10.4 (zweiter `graf`). | nur Bild |
| Merke (1.48–13.36) | A (schwach) | «P auf dem Einheitskreis hat die Koordinaten cos x und sin x»: Ohne Kreis im Bild. | `kreis` mit festem Punkt P dazunehmen. | nur Bild |

Das Abrollen ist gut abgestimmt (Abstand 1.5 s oder weniger), ebenso der Cosinus.

### `s3-5-lp-periode-symmetrie` · Kap. 2 Periode und Symmetrie · 1:11 · Periode 2π, Nullstellen kπ, Symmetrie, cos = um π/2 verschobener sin.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Periode (3.50–6.00) | B | «Darum wiederholt sich die Sinuskurve nach zwei pi»: Das Bild ist fest. Die Aufgabe in sim2 lautet «Schiebe so, dass die Kurve wieder genau auf sich selbst liegt» (Regler u). | Durchgezogene Sinuskurve u: 0→2π über die gestrichelte schieben, sie landet auf sich selbst. | neue Bewegung |
| Symmetrie (6.0 / 6.26–12.6) | A | «Cosinus von minus x ist Cosinus von x»: Kein Punktepaar für den Cosinus, beim Sinus gibt es eines. | Punkte (±π/3 \| 0.5) im zweiten `graf`. | nur Bild |

Der Szene «Versetzt» fehlt nichts: Die Verschiebung um π/2 läuft genau zum Satz.

### `s3-5-lp-tangens` · Kap. 3 Tangensfunktion · 1:08 · tan = sin/cos, Tangens am Einheitskreis, Pole, Periode π, Nullstellen, Symmetrie.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Am Einheitskreis (0–9.0 / 3.04–7.44) | A (stark) | «eine Strecke auf der senkrechten Tangente … bis zur Geraden durch den Mittelpunkt und P»: P steht bis 9.0 auf dem Winkel 0. Strecke und Strahl haben die Länge 0 bzw. liegen auf der Achse, das Erklärte ist **unsichtbar** (Bild bei 4.9 geprüft). | Bahn bei etwa 3 auf π/6 fahren, bei etwa 9 zurück auf 0 («Bei null ist sie null»), dann weiter wie bisher. | neue Bewegung (nur Stützpunkte) |
| Am Einheitskreis (12.6–15.6) | A (schwach) | «die Strecke wächst über alle Grenzen»: Die Bahn endet bei 1.2 rad (tan ≈ 2.6), mitten im Bild. | Bis etwa 1.45 rad fahren, die Strecke läuft oben aus dem Fenster. | neue Bewegung |
| Sinus durch Cosinus (2.58–8.18) | A | «Wo der Cosinus null ist, bei pi halbe … nicht definiert»: Gar kein Bild. | Cosinuskurve mit gestrichelter Polgerade x = π/2. | nur Bild |
| Pole und Periode (4.28–8.10) | B | «rechts davon kommt sie von ganz unten»: Das Bild ist fest. In sim3 fährt x bis 2π, P geht über π/2 in den zweiten Quadranten. | Kreis-Bahn π/3 → 2π/3 mit `spur`, der Strahl trifft die Tangente unten. | neue Bewegung |

### `s3-5-lp-parameter` · Kap. 4 Strecken und Verschieben · 1:14 · a, b, v, u einzeln, dann alle zusammen.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Verschiebung (2.56–7.08) | A (schwach) | «geht sie erst bei pi drittel steigend durch null»: Die Stelle π/3 ist weder markiert noch an der Achse beschriftet. | Punkt (π/3 \| 0) oder Achsteilung «π/3». | nur Bild |

Sonst ist der Clip in Ordnung: Alle vier Regler aus sim4 bewegen sich im Clip, jeweils synchron zum Satz.

### `s3-5-lp-gleichungen` · Kap. 5 Symmetrie nutzen · 1:38 · sin x = 0.6 mit Rechner, x₂ = π − x₁, Cosinus, Periode, sin(2x) = ½.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Eine Waagrechte (4.78–10.32) | A + B | «Zwischen null und zwei pi sind es zwei Stellen»: Die Schnittstellen sind nicht markiert. sim5 hat den Regler «Waagrechte y = c». | Waagrechte als bewegte Gerade [t, 0, q] während der Frage von 0 auf 0.6 heben, danach zwei Punkte einblenden. | neue Bewegung (mitlaufende Schnittpunkte: Werkzeug-Erweiterung) |
| Symmetrie (2.92–10.16) | A | «achsensymmetrisch zur Geraden x gleich pi halbe … gleich weit vor pi wie die erste nach null»: Keine Achse und keine Abstände eingezeichnet. | Gestrichelte `figuren`-Strecke x = π/2, auf der x-Achse zwei gleich lange Strecken [0, x₁] und [π − x₁, π]. | nur Bild |
| Beim Cosinus (0.3 / 0.44–2.68; 8.82) | A | «Symmetrieachse bei pi»: Nicht eingezeichnet. Die Lösungspunkte stehen ab 0.3, genannt werden sie bei 8.8. | Senkrechte x = π, Punkte ab etwa 8.8. | nur Bild |
| Faktor im Argument (8.82–12.6) | A | «Sinus z gleich ein Halb gilt bei pi sechstel und fünf pi sechstel. Durch zwei geteilt»: Gezeigt wird nur sin(2x). Die Stellen von sin z und das Stauchen fehlen. | sin x mit Punkten bei π/6 und 5π/6 zeigen, bei «durch zwei geteilt» b von 1 auf 2 ziehen. | neue Bewegung |

---

## Betragsfunktionen (SP 3.6)

### `s3-6-lp-betragsfunktion` · Kap. 1 Die Betragsfunktion · 0:51 · Betrag als Abstand, zwei Äste, Knick, Symmetrie.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Abstand zur Null (2.80–7.94) | A | «Drei und minus drei sind beide drei vom Nullpunkt entfernt»: Nur Formeln, kein Bild. | Zahlenstrahl (`figuren`, `achsen: false`) mit zwei Abstandspfeilen der Länge 3. | nur Bild |
| Zwei Äste (0.4 / 8.68–11.34) | A | Beide gestrichelten Halbgeraden stehen ab 0.4. «Für negative x … minus x» kommt erst ab 8.7. | Linken Ast in einem zweiten `graf` ab 8.6. Besser: ganze Geraden y = ±x gestrichelt, wie im Hilfsschalter von sim1. | nur Bild |
| ganzer Clip | B | sim1: Läufer x und Bezugspunkt u mit eingezeichnetem Abstand. Der Clip hat beides nicht. | Läufer auf dem V mit Abstandsstrecke auf der x-Achse. | Werkzeug-Erweiterung |

### `s3-6-lp-verschieben` · Kap. 2 Das V verschieben und strecken · 0:59 · u, v, a, Dach, Beispiel 2\|x − 1\| − 3.
**Keine Befunde.** Alle drei Regler aus sim2 (u, v, a, auch a < 0) bewegen sich im Clip, und jede Bewegung liegt höchstens etwa 1 s neben ihrem Satz.

### `s3-6-lp-umklappen` · Kap. 3 Das Umklapp-Prinzip · 1:06 · \|x − 2\|, \|x² − 4\| als W, Knicke, \|f\| ≠ −f.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Eine Gerade (12.50–13.62) | A + B | «das Stück klappt nach oben»: \|f\| wird nur eingeblendet, es klappt nichts. «Rechts von zwei … ändert sich nichts» ist im Bild nicht vom linken Teil abgehoben. | Linkes Stück als Potenzkurve [t, a, 1, 2, 0] mit `bis: 2` und a von 1 nach −1, das Stück dreht sich um (2 \| 0) nach oben. | neue Bewegung |
| Eine Parabel (6.58–7.30) | A + B | «Es klappt hoch: Aus dem Scheitel null, minus vier wird ein Buckel»: wieder nur eingeblendet. | Mittelstück [t, a, 2, 0, v] mit `von: −2, bis: 2` von (1, −4) nach (−1, 4). | neue Bewegung |
| Knicke (2.20–6.76) | B | Die Knicke wandern in sim3 mit dem Regler q («Welche Teile klappen um?»). Im Clip steht f fest. | \|x² + q\| mit q von −4 auf 0: Die Knicke laufen zusammen. | Werkzeug-Erweiterung (bewegte \|f\|) |

### `s3-6-lp-abschnittsweise` · Kap. 4 Abschnittsweise schreiben · 1:03 · Grenze bei Argument = 0, zwei Fälle, Wanne \|x + 1\| + \|x − 3\|, drei Abschnitte.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Die Wanne (0.44–5.44) | A | «Addiert man zwei Beträge»: Die zwei einzelnen V sind nicht zu sehen. sim4 zeigt sie dünn. | \|x + 1\| und \|x − 3\| gestrichelt dazunehmen (Betragskurven mit u = −1 und u = 3). | nur Bild |
| Die Wanne (8.80–13.0) | A | «konstant vier, so gross wie der Abstand der beiden Stellen»: Der Abstand ist nicht eingezeichnet. | Strecke von −1 bis 3 auf der x-Achse mit «4». | nur Bild |
| Die Wanne (ganze Szene) | B | Die Regler a und b in sim4 verschieben die Stellen, Boden und Höhe ändern sich. Die Wanne im Clip steht fest. | b von 3 auf 5: Der Boden wird breiter und höher. | Werkzeug-Erweiterung (Summe zweier Beträge bewegt) |
| Zwei Fälle (0.4 / etwa 5–10) | A (schwach) | Der linke Ast «minus zwei x plus sechs» steht etwa 5 s vor dem Satz. | Linken Ast später einblenden. | nur Bild |

### `s3-6-lp-gleichungen` · Kap. 5 Gleichungen und Ungleichungen · 1:07 · \|x − 1\| = 3 am Graphen und rechnerisch, Ungleichung, W mit vier Lösungen, Anzahl der Lösungen.

| Szene (Zeit) | Befund | Was gesagt/gezeigt wird | Empfohlene Anpassung | Aufwand |
|---|---|---|---|---|
| Wie viele? (2.10–10.10) | A + B (stark) | «Unter null keine, bei null zwei, zwischen null und vier vier, auf dem Buckel vier genau drei, darüber nur noch zwei»: Die Waagrechte steht fest auf y = 4. Der Hauptregler von sim5 ist c. Die Notiz mit allen Fällen steht schon ab 4.0. | Waagrechte als bewegte Gerade [t, 0, q]: −1 → 0 → 2 → 4 → 5, synchron zu den fünf Satzteilen. Punkte je Phase mit einem eigenen `graf`. | neue Bewegung (mitlaufende Schnittpunkte: Werkzeug-Erweiterung) |
| Rechnen (7.14–9.76) | A | «Die Skizze zeigt, dass es genau zwei Lösungen sind»: In der Szene gibt es keine Skizze. | `graf` mit V, Waagrechte und den Punkten −2 und 4 stehen lassen. | nur Bild |
| Ungleichung (3.36–6.76) | A (schwach) | «zwischen den Schnittstellen»: Das Lösungsintervall ist auf der x-Achse nicht markiert, sim5 markiert es. Die Beschriftung «(1 \| 0)» stösst mit der Achszahl 2 zusammen. | Strecke [−2, 4] auf der x-Achse, Beschriftung versetzen. | nur Bild |
