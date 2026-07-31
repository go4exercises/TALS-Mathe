# TODO — Didaktisches Animations-Audit Grundlagenfach

Stand: 2026-07-25. Vollreview aller interaktiven Animationen (Canvas, SVG, Slider-Widgets)
auf den 23 Grundlagen-Seiten aus didaktischer Sicht: Verständlichkeit, Nachvollziehbarkeit
(Kopplung Parameter → Darstellung → Formel), Anregungsgrad, Parametrisierung, Bestand.

**Gesamtbild:** Die Widget-Qualität ist hoch; kein einziges Widget ist streichwürdig,
Zusammenlegungen drängen sich nur an einer Stelle auf (AN-32). Referenz-Widgets, die als
Muster taugen: g1-2 `cv-zahlmenge`, g2-2a `cv-vkipp`, g2-2b `cv-pk`, g2-3 `cv-lbuschel`,
g3-2 `cv-steig`, g4-2 `cv-manip`, g4-3 `cv-robust`, g5-2a `cv-dreiungl`, g5-2c `cv-ringroll`,
g5-4 `cv-symm`, g5-5 `gl-svg`.

> **Stand-Prüfung 01.08.2026 (vor Version 1.0):** Die Punkte sind **tatsächlich offen**,
> nicht bloss nicht abgehakt. Stichprobe im Quelltext und im Browser:
> **AN-01** (`cv-defWF`) — der Code kommentiert das Problem selbst („wir zeichnen das gleiche
> Dreieck … tauschen a und b nicht"); **AN-02** (`par-canvas`) — die Live-Formel zeigt
> weiterhin «(x − 1)² + −2»; **AN-03** (`ws-canvas`) — der Slider läuft unverändert bis
> `max="9"`. Die Beschriftungs-Überarbeitung vom 30.07. hat Lesbarkeit und Platzierung
> behoben, **keinen** der hier gelisteten fachlich-didaktischen Punkte.

Prioritäten: **P1** = fachlicher Fehler / faktischer Defekt (zuerst beheben) ·
**P2** = didaktisch hoch (Kernaussage kommt nicht an) · **P3** = mittel · **P4** = niedrig (Feinschliff).

---

## P1 — Fachliche Fehler und faktische Defekte

- [ ] **AN-01** `g5-3` · `cv-defWF` (Definition sin/cos/tan): Position «bei B» liefert
  **mathematisch falsche Werte** — das Dreieck wird stets mit Winkel x bei A konstruiert,
  bei «bei B» werden nur die Beschriftungen getauscht. Anzeige behauptet z.B.
  «sin 35° = 0.819» (korrekt: 0.574; 0.819 = sin 55°). Fix: bei Position B das Dreieck mit
  Winkel x bei B konstruieren (a = c·cos x, b = c·sin x) — gleicher Winkel, andere Ecke,
  andere Seiten heissen GK/AK.
- [ ] **AN-02** `g3-1` · `par-canvas` (Parabel-Scheitelform): Live-Formel zeigt fehlerhafte
  Notation «(x − −3)² + −2» statt «(x + 3)² − 2» — ausgerechnet beim Vorzeichen-Ablesen,
  dem dokumentierten Standardfehler. Vorzeichenlogik aus g3-3 (`fmtKlammer`/`vPart`) übernehmen.
- [ ] **AN-03** `g3-3` · `ws-canvas` (schiefer Wurf): Slider läuft bis x = 9, Tabelle endet
  bei 8; bei x = 9 wird «h(9) = −1.25 m» (negative Höhe) angezeigt. Fix: bei x > 8.47
  «Ball ist gelandet (x ≈ 8.47 m)» anzeigen (macht den Definitionsbereich erlebbar) —
  oder schlicht Slider-Max auf 8.
- [ ] **AN-04** `g2-2a` · `cv-faelle` (drei Lösungsfälle): Geradenlabels werden in **allen
  drei Fällen** unterdrückt (Bedingung labelY ≤ 14 bei festem labelX = 5.5 schlägt immer
  fehl); in Fall 3 trägt die Gerade gar kein Label, obwohl «y = 4x + 8 (beide Seiten)» die
  Pointe ist. Fix: Labelposition dort setzen, wo die Gerade im Fenster liegt (Muster
  `labelAn()` aus g2-3).
- [ ] **AN-05** `g5-2c` · `cv-flaecheKr` (Sektoren → Quasi-Rechteck): Das Ziel-Rechteck
  endet rechnerisch bei ≈ 1.15·W — **ca. 15 % des Rechtecks samt Beschriftung «Breite = π·r»
  liegen bei jeder Canvasbreite ausserhalb des Bilds**. Layout skalieren:
  Rpx ≤ (W − rectStartX − 20)/π.
- [ ] **AN-06** `g5-2c` · `cv-umfang` (Rad abrollen): Fester Massstab 50 px/m — bei d ≥ 2.5–3.0 m
  laufen Streckenende und π·d-Marke aus dem Bild; genau der Zielzustand «volle Umdrehung = π·d»
  ist abgeschnitten. PX_PER_M dynamisch aus der Canvasbreite berechnen.
- [ ] **AN-07** `g5-2b` · `fam-canvas` (Vierecks-Familie): Preset «Drachen» meldet Typ
  «Drachen», aber alle vier Eigenschafts-Häkchen zeigen ✗ — das Drachen-Kriterium (zwei
  Paare benachbart gleicher Seiten) fehlt in der Checkliste. Fünfte Häkchen-Zeile ergänzen;
  optional Seitenlängen klein an die Kanten schreiben, damit die Häkchen begründet sind.

## P2 — Didaktisch hoch (Kernaussage kommt nicht an)

- [ ] **AN-08** `g1-1` · Strukturbaum-Widget: Implizite Multiplikation wird nicht geparst —
  «2x+3» oder «3(x+2)» (genau die Schreibweise, die BM-Lernende zuerst tippen) scheitern mit
  kryptischer Meldung («Unerwartetes Token: {"t":"var"…}»). Tokenizer erweitern (Zahl vor
  Variable/Klammer → implizites ·, analog `parseL` in mathlib.js) und Fehlermeldungen in
  verständliches Deutsch übersetzen.
- [ ] **AN-09** `g1-2` · Konverter `cv-p`/`cv-q`: Die 👁-Frage (periodisch vs. abbrechend je
  nach Nenner) wird vom Widget nicht beantwortet — es zeigt nur «0.3333…». Badge ergänzen:
  «abbrechend (Nenner 4 = 2·2)» bzw. «periodisch (Nenner 3 enthält Faktor ≠ 2, 5)», der Code
  zerlegt den gekürzten Nenner bereits.
- [ ] **AN-10** `g1-3` · `cv-equiv` (Einstieg, vier Terme): (a) Spaltenlayout sprengt die
  Boxen schon ab ~560 px, bei 360 px unlesbar — bei Schmalbreite 2×2-Anordnung; (b) warum
  Dario falsch liegt, wird nirgends erklärt — Erklärfeld ergänzen («(80+50)(x+y) erzeugt
  die gemischten Glieder 80y und 50x zu viel»).
- [ ] **AN-11** `g2-1` · `uf-canvas` (Äquivalenzumformung): Die Waage ist faktisch tot
  (beide Seiten in allen Schritten gleich → Neigung immer 0), und der 👁-Hinweis «Was
  passiert, wenn du nur auf einer Seite wegnimmst?» ist im Widget nicht ausführbar. Fix:
  (a) Waageninhalt als Objekte (Kisten/Gewichte), die bei «−3» beidseitig verschwinden und
  bei «:4» schrumpfen; (b) Kontrast-Button «✗ nur links −3», der die Waage kippen lässt.
- [ ] **AN-12** `g2-2a` · `cv-three` (drei Darstellungen): Tabelle statisch (reagiert bei
  den meisten Sliderwerten gar nicht), Schnittpunkt S(4|5) samt Label von Anfang an verraten.
  Fix: Zeile «aktuelles x» immer live anzeigen (x, 2x−3, 5, </=/>) ; Schnittpunkt-Label erst
  beim Erreichen einblenden; zweiten Punkt auf y = 5 mit vertikaler Differenzstrecke
  («Abstand der Seiten → 0»).
- [ ] **AN-13** `g2-2a` · Parameterdiskussions-Widget (`sl-k`): Fall 𝕃 = ∅ ist nicht
  explorierbar (b(k) verschwindet mit a(k)), und die Lösung ist konstant x = 3 («Slider tut
  nichts»). Umschalter «Beispiel A: (k−2)x = 3(k−2)» / «Beispiel B: (k−2)x = 2» einbauen —
  bei B variiert x = 2/(k−2) sichtbar und der Widerspruchsfall tritt bei k = 2 ein.
  Optional (P3): kleines Canvas mit den Geraden beider Seiten.
- [ ] **AN-14** `g2-3` · `cv-kino` (Einstieg): Statisch, obwohl der 👁-Hinweis auffordert,
  Punkte zu verfolgen, die nur eine/beide Gleichungen erfüllen. Slider «Anzahl Erwachsene x»
  ergänzen: Punkt wandert auf der roten Geraden, Live-Doppel-Check Personen ✓ / Geld ✓|✗ —
  macht «eine Gleichung = ganze Gerade von Lösungen, beide = ein Punkt» erlebbar.
- [ ] **AN-15** `g5-1` · Winkelpaare-Widget (`wp-*`): Als «interaktiv» betitelt, aber nur
  Reiter sind klickbar — die Kern-Invarianz («α wächst, β schrumpft, Summe bleibt 90°/180°»)
  ist nicht erlebbar. Gemeinsamen α-Slider ergänzen, der alle drei Panels nachführt, mit
  Live-Summenanzeige «α + β = 90° ✓».
- [ ] **AN-16** `g5-2a` · `cv-anw` (Pythagoras-Anwendung): Chips «Gegebene Seite»/«Wert»
  verändern die Zeichnung nicht — Kopplung Parameter → Bild gebrochen. Gewählte Seite im
  Canvas grün/dick zeichnen, gesuchte gestrichelt, Wert «1» bzw. «g» direkt an die Seite.
- [ ] **AN-17** `g5-2d` · `sch-canvas` (Schatten-Einstieg): Das per 👁-Hinweis zu beobachtende
  konstante Verhältnis (Mast→Schattenende : Mast→Person = 1.43) wird nirgends angezeigt —
  Readout-Zelle ergänzen, farblich hervorgehoben. Optional: zweiter Slider Personenhöhe h.
- [ ] **AN-18** `g5-3` · `cv-aehnl` (ähnliche Dreiecke → konstante Verhältnisse): Die
  Legendenwerte werden alle direkt als sin(α) gesetzt statt aus Längen gemessen — beim
  Schieben von k ändert sich keine einzige Zahl, die Invarianz wirkt behauptet statt gezeigt.
  Pro Dreieck Seitenlängen anzeigen (a = 2.9, c = 5.0 / a' = 4.6, c' = 8.0 …) und die
  Quotienten daraus rechnen; b/c und a/b als Ausblick auf cos/tan vorbereiten.
- [ ] **AN-19** `g5-3` · `cv-ssw` (SSW 0/1/2 Dreiecke): Der didaktisch wichtigste Berührfall
  a = h = 3.44 ist mit Schrittweite 0.5 unerreichbar. Chips «a = h» und «a = c» ergänzen,
  die den Slider exakt setzen (oder Schrittweite 0.01).
- [ ] **AN-20** `g5-5` · `cv-rad` (Riesenrad-Einstieg): Die Textzweige «keine Lösung»
  (< 2 m / > 42 m) und «Berührfall» (= 2/42 m) sind mit Slider-Bereich 5–35 m unerreichbar —
  genau die Analoga zu «sin x = 1.5 unlösbar» und «c = ±1». Zielhöhen-Slider auf 0–45 m
  erweitern (Grenzfälle aufs Raster). Zusatz (P3): Play/Pause-Button für die Fahrt.
- [ ] **AN-21** `g1-4` · **Neue Animation Potenzgesetze** (grösste Lücke des Audits): P1–P7
  sind Kernkompetenz laut RLP, haben aber null Interaktivität. Faktor-Kachel-Animation für
  P1/P2: Slider n, m; 2ⁿ·2ᵐ als zwei Kachelreihen, die zu n+m Kacheln verschmelzen;
  Divisions-Modus streicht Kacheln; Fehlerfall 2³·5⁴ ≠ 10⁷ («Kacheln passen nicht zusammen»).

## P3 — Mittel

### Neue Animationen / Ergänzungen
- [ ] **AN-22** `g2-2b`: Quadratische Ergänzung geometrisch — Flächenmodell (Quadrat x² +
  zwei Rechtecke (p/2)·x → fehlendes Eckquadrat (p/2)²) als schrittgesteuertes Canvas;
  nimmt der pq-Formel die Willkür. (Verwandt: `g3-3` Umformung allgemeine Form →
  Scheitelform als Schritt-Widget, P4.)
- [ ] **AN-23** `g1-2`: Zahlengeraden-Widget Vorzeichenregeln (7 − (−2) als Pfeilkette,
  Chips für die vier Fälle) — die grösste Fehlerquelle der Zielgruppe ist bisher rein
  tabellarisch.
- [ ] **AN-24** `g1-1`: Schritt-Animation «Auswertungs-Reihenfolge» (Schritt-Slider hebt die
  jeweils nächste Operation hervor, letzte = Hauptoperation) — verbindet Hierarchie,
  Strukturbaum und Klassifizier-Übung.
- [ ] **AN-25** `g3-1`: Fehler-Box «Wertetabelle legt Funktion nicht eindeutig fest» um
  einen Graphen ergänzen: f(x) = x² und h(x) durch dieselben vier Punkte — der Aha-Moment
  ist visuell, nicht rechnerisch.
- [ ] **AN-26** `g5-1`: Stufen-/Wechselwinkel an Parallelen animieren (Slider Neigung der
  Schneidenden, F-/Z-Winkel laufen synchron; Parallelität aufhebbar → Winkel ungleich) —
  trägt in 5.2a den Innenwinkelsummen-Beweis.
- [ ] **AN-27** `g5-4` · `cv-abw` (Sinus-Abwickler): Chip «sin/cos» zum Umschalten — der
  cos-Abwickler erklärt nebenbei, warum die cos-Kurve bei 1 startet (tragend für 5.5).
- [ ] **AN-28** `g5-5` · `kr-svg` (Kurven-Ansicht): Tabs sin/cos/tan ergänzen; beim tan
  Polstellen-Asymptoten strichliert — zeigt unmittelbar, warum k·180° genügt
  (tan-Periodizität ist der Fehlerbrennpunkt der Seite).
- [ ] **AN-29** `g5-5` · Lösungs-Trainer: 2–3 tan-Aufgaben ergänzen (φ₂ = φ₁ + 180° wird
  bisher nicht trainiert); optional Aufgaben aus Zufallswerten generieren.
- [ ] **AN-30** `g4-2`: Klassieren-Abschnitt (√n-Faustregel) — Klassenbreiten-Widget am
  60er-Datensatz ergänzen oder (billiger, P4) prominenter Querverweis auf das
  Histogramm-Widget in 4.0.
- [ ] **AN-31** `g4-3`: Quartile/Boxplot ohne interaktive Stütze — das passende Widget
  existiert auf g4-0: prominent verlinken oder kompakt wiederverwenden (sortierte Liste mit
  Q₁/Median/Q₃-Markern + Boxplot am Klasse-B-Datensatz).

### Zusammenlegung
- [ ] **AN-32** `g2-3` · `cv-lf` ↔ Büschel-Widget: Zwei Chips-Leisten mit gleicher Semantik
  (eindeutig/parallel/identisch) direkt untereinander. Entweder cv-lf-Karten als Presets ins
  Büschel-Widget integrieren und cv-lf streichen, oder cv-lf behalten und pro Fall das
  konkrete Gleichungssystem in der Live-Zeile ergänzen.

### Verbesserungen bestehender Widgets
- [ ] **AN-33** `g1-1` · `cv-hauptop`: Hauptoperation (das letzte «+») in allen drei Formen
  farblich markieren; redundante 3-Zeilen-Legende durch «alle drei = N» ersetzen; Layout
  unter 400 px prüfen (360-px-Shot).
- [ ] **AN-34** `g1-1` · Würfel-Demos Rechengesetze: pro Wurf grünes «✓ beide Seiten = N»;
  vierte Box «Gegenprobe a − b vs. b − a» mit rotem ✗ (zeigt, warum die Gesetze auf +/·
  beschränkt sind).
- [ ] **AN-35** `g1-2` · Intervall-Widget `cv-iv`: sechste Zeile ]a;b] ergänzen (Vergleich
  [0;4[ vs. ]0;4] festigt die Klammer-Richtung); optional kleine Slider für a, b.
- [ ] **AN-36** `g1-3` · `cv-binomi` (3. Binom, Schritt 2): Streifen wird an alter UND neuer
  Position identisch gezeichnet — Ausgangslage gestrichelt/halbtransparent plus Umlege-Pfeil.
- [ ] **AN-37** `g1-3` · Faktorisier-Übung: `norm()` um `−`→`-` und `²`→`^2` ergänzen
  (Unicode-Minus von der Seite kopiert wird sonst als falsch gewertet); pro Zeile
  Lösungs-Toggle ergänzen (einzige Übung der Seite ohne Lösungszugang).
- [ ] **AN-38** `g1-4` · `cv-zoom`: 13 von 38 Slider-Stufen haben keinen Anker — Legende
  und Bild zeigen dann verschiedene Grössenordnungen. Slider auf die 24 Ankerstufen rastern
  (Index-Slider) oder Zwischenstufen explizit als «zwischen X und Y» rendern.
- [ ] **AN-39** `g2-1` · `wg-canvas` (Waage): Story sichtbar machen — links 4 Kisten
  (Höhe ∝ x) + Werkzeugkasten, rechts 15 Einheitsgewichte statt reiner Textlabels.
- [ ] **AN-40** `g2-1` · Probe-Widget: dieselbe Gleichung 4x+3=15 zum dritten Mal auf der
  Seite — wechseln (z.B. 5x − 7 = 2x + 8, Brücke zu 2.2a).
- [ ] **AN-41** `g2-2a` · `cv-budget`: Live-Zeile um Vergleichszeichen + Status ergänzen
  («81 < 117 — Budget nicht ausgeschöpft»); Budget-Label von cx(7) nach links verschieben
  (kollidiert mit K(x)-Label, Abstand ~12 px).
- [ ] **AN-42** `g2-2b` · Drei-Darstellungen-Widget: Vorzeichenwechsel in der f(x)-Spalte
  markieren («Nullstelle zwischen 0 und −1»); bei Lösungen ausserhalb der Tabelle Fussnote
  «liegt ausserhalb» (sonst wirkt 𝕃 der Tabelle widersprechend).
- [ ] **AN-43** `g2-3` · `cv-three`: Schnittpunkt-Label und Lösungszeile erst nach Erreichen
  von x = 2 einblenden; Spalte «y₁ = y₂?» (✓/✗) ergänzen.
- [ ] **AN-44** `g2-3` · `cv-verf`: Graph an die Schritte koppeln — bei «x = 2» gestrichelte
  Vertikale, bei «y = 3» Horizontale einblenden (Elimination = Projektion auf eine Koordinate).
- [ ] **AN-45** `g3-3` · `disk-canvas`: Die drei D-Beispiele wechseln b und c gleichzeitig —
  auf eine Familie x² − 4x + c mit c-Slider umstellen (D = 16 − 4c läuft live durch 0),
  Buttons bleiben als Schnellwahl.
- [ ] **AN-46** `g3-3` · A2 (Scheitel setzen): Fehler-Feedback verrät sofort die Lösung —
  beim ersten Fehlversuch nur Richtungs-Hinweis («u-Vorzeichen prüfen»), Lösung erst beim
  zweiten; Satz zur mitlaufenden Kontroll-Parabel in den Aufgabentext.
- [ ] **AN-47** `g4-0` · Stichproben-Widget: Schwankung ist ohne Gedächtnis nicht erlebbar —
  Mini-Historie der letzten ~10 Stichproben-Mittelwerte als Punktleiste; bei n = 26 Hinweis
  «Gesamterhebung — Abweichung zwingend 0».
- [ ] **AN-48** `g4-1` · `sb-canvas` (Klassenumfrage): Klick-Urliste live mitschreiben
  («Urliste: 3, 5, 2, …») — der Folgetext macht die Urliste zum zentralen Begriff, springt
  aber auf eine andere, fixe Liste um.
- [ ] **AN-49** `g4-2` · `ea-canvas`: Boxplot-Konstruktionsphasen (5 × 250 ms) sind in ~1.3 s
  vorbei — verlangsamen (≥ 800 ms) oder «▶ Schritt»-Taste.
- [ ] **AN-50** `g4-3` · `sl-canvas` (Einstieg Streuung): Slider-Label «Streuung 100 %»
  benennt den Interpolationsfaktor («100 % wovon?») — umbenennen; s live mitanzeigen
  (Brücke zum später händisch gerechneten s = 0.29 vs. 1.39).
- [ ] **AN-51** Sammelposten **👁/💡-Rollover nachrüsten** (laut Projektkonvention Pflicht
  bei interaktiven Animationen): g3-1 Einstieg, g4-1 `sb-canvas`, g4-2 `ea-canvas`,
  g4-3 `sl-canvas`, g1-4 `wn-konv` (optional).
- [ ] **AN-52** `g5-1` · Winkel-Visualisierer `wv-svg`: (a) 👁-Frage nach dem Winkeltyp ist
  im Widget nicht beantwortbar — Typ-Anzeige («stumpf») ergänzen; (b) Gleichheit
  Bogenlänge = Radiant explizit beschriften («= Radiant!») — das ist die Definition des
  Bogenmasses und geht als «zwei gleiche Zahlen» unter.
- [ ] **AN-53** `g5-1` · Klassifikator `kl-svg`: Zufallsmodus mit verdeckter Gradzahl
  (Form → Typ statt Zahl → Typ); Slider-Minimum 1° (0° hat keinen Typ).
- [ ] **AN-54** `g5-1` · `py-svg`: SVG-Labels a/b schwarz trotz akz-blau/akz-orange-Slidern —
  Farbkopplung gemäss STYLEGUIDE nachziehen (#1a4f8a / #b85c00).
- [ ] **AN-55** `g5-2a` · `cv-stativ`: Bei N = 3 schwebt ein Fuss sichtbar über dem Boden,
  gilt aber als «in Kontakt» (widerspricht der Kernaussage) — Boden am angehobenen Fuss als
  Buckel zeichnen; bei N = 4 die zwei Kipp-Lagen alternierend andeuten; Einheit (cm)
  vereinheitlichen.
- [ ] **AN-56** `g5-2a` · `cv-allg`: Drag auf Canvas-Inneres clampen (Punkte derzeit
  unbegrenzt ziehbar, Figur degeneriert kommentarlos); Aussenwinkel-Legende um Zeile
  «α' vs. β + γ» ergänzen — deckt den Aussenwinkelsatz (A1c) ohne neues Widget ab.
- [ ] **AN-57** `g5-2a` · `cv-kong`: Chip-Beschriftungen «SsW (1 Lösung)» / «sSW (2 Lösungen)»
  verraten die Pointe — neutral beschriften, Auflösung erst im Erklärtext; optional α oder a
  im sSW-Fall verstellbar (Grenzfall a = b·sin α aus A4.5 wird darstellbar).
- [ ] **AN-58** `g5-2a` · `cv-pyth`: Am Ende von Tab 1 die Additionszeile einblenden
  (p·c + q·c = c²) — der Schluss Kathetensätze → Pythagoras wird nie explizit gezeigt;
  Flächentreue der Scherung im Text absichern («siehe 5.2b»).
- [ ] **AN-59** `g5-2b` · `cv-scher` (Trapez-Scherung): Mittellinien-Toggle ergänzen
  («m = ½(a+c) — auch sie ist scherungsinvariant») — schliesst die RLP-Lücke Mittellinie
  ohne neues Widget.
- [ ] **AN-60** `g5-2b` · `cv-stv`: Beim Sehnenviereck wechselt der gezogene Punkt beim
  Überholen stillschweigend die Identität (Sortierung nach jedem Zug) — Überhol-Sperre
  aktivieren; Fallback bei fast-parallelen Tangenten mit einem Erklärsatz versehen.
- [ ] **AN-61** `g5-2c` · Pizza-Einstieg: Symbol-Inkonsistenz ζ (Canvas) vs. φ (Readout und
  Anim 7) vereinheitlichen; nach Anim 7 Rückverweis-Satz auf den Pizza-Cliffhanger.
- [ ] **AN-62** `g5-2c` · `cv-strecken`: Modus/Slider «Abstand der Geraden zu M» ergänzen —
  eine Gerade wandert kontinuierlich Passante → Tangente → Sekante (Live-Anzeige Abstand
  vs. r): verankert die drei Begriffe als ein Kriterium statt drei Vokabeln.
- [ ] **AN-63** `g5-2d` · `cv-figur`: Der Parkettierungs-Beweis (k²) bei exakt |k| = 2 ist
  das Highlight, aber versteckt — Marke/Chip «probiere k = 2» bzw. 👁-Hinweis konkretisieren.
- [ ] **AN-64** `g5-2d` · `cv-aehnSatz`: Konstruktionsbedingt immer ähnlich, nichts zu
  entdecken — «Störungs»-Regler ergänzen (eine Seite ±20 % → Verhältnisse laufen auseinander,
  Anzeige kippt rot auf «nicht ähnlich»); stützt A4 (6-8-9-Gegenbeispiel).
- [ ] **AN-65** `g5-3` · `bm-canvas` (Baum-Einstieg): Readout-Zelle «h/d» ergänzen (hängt
  nur von α ab — Brücke zu «Seitenverhältnis hängt nur vom Winkel ab»); Halbsatz zur
  vernachlässigten Augenhöhe.
- [ ] **AN-66** `g5-3` · `cv-sinussatz`: Quotienten erscheinen als «300.0» in nackten
  Pixeln — auf r = 1 normieren (alle Werte 2.00 = Durchmesser); Legende um α, β, γ und
  a, b, c ergänzen; Slider-Labels «Position von A auf dem Kreis» (Verwechslung mit
  Dreieckswinkeln); optional Drag-Punkte statt Slider (Muster g5-2d).

## P4 — Niedrig (Feinschliff)

- [ ] **AN-67** `g1-1` · `cv-distrib`: Slider mit akz-Farben an die Teilflächen koppeln.
- [ ] **AN-68** `g1-2` · `cv-betrag-zg`: im violetten Label «= |b − a|» andeuten.
- [ ] **AN-69** `g1-3` · Zusammenfassen-Widget: Einleitungssatz («zusammenschmelzen») an das
  diskrete Verhalten anpassen; sechstes Preset mit sich aufhebender Gruppe (3x − 3x + 5).
- [ ] **AN-70** `g1-4` · `wn-konv`: Zusatzzeile «Dezimalpunkt um N Stellen verschoben»
  (Verschiebungs-Regel sichtbar machen); optional Zwei-Zahlen-Multiplikationsmodus.
- [ ] **AN-71** `g1-4` · `cv-einschachtel`: getestete Mitte m² auch auf der Radikanden-Achse
  spiegeln.
- [ ] **AN-72** `g2-1` · Gleichungstypen-Umschalter: mit der fast identischen Tabelle
  darunter zusammenführen (Zusatzspalten Lösungsmethode/Fundstelle in die Tabelle) — oder
  beim Klick das x-Merkmal im Beispiel farbig hervorheben.
- [ ] **AN-73** `g2-1` · `cv-ungl`: Prüfpunkte g−1/g+1 mit ✓/✗ neben der Grenze.
- [ ] **AN-74** `g2-2a` · `uf-lin`: Operations-Pille an die Zeile setzen, auf die sie
  angewendet wird (Heft-Konvention).
- [ ] **AN-75** `g2-2b` · velo-canvas: mitlaufende min-Zähler pro Weg während der Animation;
  Hinweissatz zur verworfenen zweiten Lösung (Vorgriff A6).
- [ ] **AN-76** `g2-2b` · fak-stack: Stolperstein erst ab dem Kernschritt einblenden.
  Wurzelterm-Baum: drei Fälle auf eine Familie x² − 6x + c umstellen (verzahnt mit k-Widget).
- [ ] **AN-77** `g2-2b` · `cv-pk`: x₁/x₂-Labels an die grünen Nullstellen, «D = 0»-Label an
  die Grenzlinie.
- [ ] **AN-78** `g2-3` · `cv-lbuschel`: Begriff «Determinante» ersetzen oder in einem Satz
  einführen (kommt im RLP-Grundlagenfach nicht vor); Slider-Farbkopplung m/c nachziehen.
  `dd-stack`: Kommentar präzisieren («damit die y-Koeffizienten +3 und −3 werden»).
  `cv-a1`: Geraden-Legende ergänzen. `cv-kino`: Tick-Beschriftung auf 5er-Schritte.
- [ ] **AN-79** `g3-1`: `lin-canvas` Hinweis «(ausserhalb des Bildes)» wenn x₀ das Fenster
  verlässt; `schn-canvas` akz-orange auf b-Slider + Fazit-Zeile einfärben; Einstieg
  «genau ein Wert» betonen; Quiz-Feedback auf Testgeraden-Widget verweisen.
- [ ] **AN-80** `g3-2`: `dr-canvas` b-Punkt orange statt dunkelrot + «b»-Label;
  `a1-canvas` Feedback differenzieren («m stimmt, b nicht»); `ks-canvas` Schrittweite 1 kg
  erwägen (direkteste m-Ablesung).
- [ ] **AN-81** `g3-3`: `dr-canvas` Slider-Akzente vs. Punktfarben entwirren;
  typ-Button «rein quadratisch (b = 0)».
- [ ] **AN-82** `g5-1`: `dg-canvas` Plausibilitäts-Panel responsiv, optional
  Schranken-Zahlenstrahl; Zufallswinkel-Trainer-Pool um Nenner 9/18 erweitern (deckt A3 ab);
  `sk-canvas` Elemente in Schritt 2 nacheinander einblenden.
- [ ] **AN-83** `g5-2a`: `cv-beweis` C ziehbar machen («funktioniert für jedes Dreieck»);
  `cv-elem` Kreis-Toggle bei Höhen/Seitenhalbierenden ausgrauen; `cv-spez`
  Kernaussage-Zeile je Typ («a = b ⇒ α = β»).
- [ ] **AN-84** `g5-2b`: `cv-nEck` gemessene Winkelsumme in der Legende (beweisen statt
  behaupten); `cv-rect` Zähl-Toggle ohne Raster deaktivieren, Einheiten-Chips begründen
  oder streichen; `cv-flaeche` Schrittleisten-Beschriftung pro Figur (bei Raute/Drachen
  wird nichts «geschnitten/verschoben»).
- [ ] **AN-85** `g5-2c`: `cv-sektor` Legendenzeile «½·b·r» (Probe A4.2), Optik-Satz bei 90°
  streichen; `cv-segment` Label-Ausblendung bei φ < 30°, Formelbox-Hinweis bei φ > 180°.
- [ ] **AN-86** `g5-2d`: `cv-streck` Handles auf r = 6 px, Drag-Fähigkeit im 👁-Hinweis;
  `cv-strahl` Slider-Beschriftung «Schritt 0–4: Aufbau · 5: Variante 2»; `cv-recht` Hinweis,
  in welchem α-Fenster die Drehkopie sichtbar ist, optional Höhensatz-Chip.
- [ ] **AN-87** `g5-3`: `cv-spez` α/β-Chips im 45°-Modus ausblenden, optional
  Pythagoras-Overlay; `cv-cossatz` Legendenzeile als «−2bc·cos α» mit Vorzeichen;
  `cv-flaeche` Erklärsatz bei φ ≈ 90° («grösstmögliche Fläche — sin φ = 1»).
- [ ] **AN-88** `g5-4`: `cv-sincos` bei Spezialwinkeln exakten Wert in der Legende
  («0.866 = √3/2»); `cv-tan` Chips 90°/270° ergänzen (zeigen «nicht definiert»),
  Kappungsgrenze höher; `cv-symm` vierter Chip «90° − α» (Diagonale y = x — erklärt
  «Co-Sinus» visuell); Vorzeichen-Trainer Mini-Einheitskreis im Feedback.
- [ ] **AN-89** `g5-5`: `gl-svg` c beim Tab-Wechsel symmetrisch klemmen (negativer
  tan-Wert bleibt sonst stehen), im tan-Modus Tangente x = 1 mit Punkt S einblenden
  (Rückgriff 5.4); `cv-kk` Satz, warum die Brückenlinie bei cos fehlt.
- [ ] **AN-90** `g5-4`/Nachschlag: Arcus-Hauptwerte am Einheitskreis visualisieren
  (arcsin-Bereich als rechte Kreishälfte einfärben, zweiten Winkel grau) — operativ durch
  5.5 aufgefangen, darum P4.

---

## Ausdrücklich geprüft und für gut befunden (KEEP, keine Aktion)

g1-1 Klassifizier-Übung, Begriffe-am-Polynom, Vorzeichen-Toggle, Zweiklammersatz-Widget ·
g1-2 `cv-zahlmenge` · g1-4 `cv-einschachtel` · g2-1 `cv-ungl` · g2-2a `cv-vkipp` ·
g2-2b `cv-pk`(-parabel), velo-canvas · g2-3 `cv-lbuschel`, dd-stack, `cv-a1` ·
g3-1 `cv-vertikal`, fq-Quiz, ach-Canvases · g3-2 `cv-steig`, typ-, a2-canvas ·
g3-3 `dr-canvas`, `cv-extrem` · g4-0 gesamte Seite (Referenzqualität) · g4-1 mt-Spiel ·
g4-2 SVG-Galerien, `cv-manip` · g4-3 `cv-robust` · g5-1 zt-Trainer · g5-2a `cv-dreiungl`,
`cv-beweis`, `cv-flaeche`, `cv-kong` (Kern) · g5-2b `cv-drachen`, `cv-reg`, `cv-nEck` ·
g5-2c `cv-pi`, `cv-ring`, `cv-ringroll`, `cv-segment` · g5-2d `cv-strahl`, `cv-strlabor` ·
g5-3 `cv-cossatz`, `cv-flaeche` · g5-4 `cv-schiff`, `cv-sincos`, `cv-tan`, `cv-bez`,
`cv-symm` · g5-5 `gl-svg`, `cv-kk`, Lösungs-Trainer (Kern).

**Streichungen:** keine empfohlen. **Zusammenlegungen:** nur AN-32 (g2-3) und AN-72 (g2-1,
Text-Widget mit Tabelle).
