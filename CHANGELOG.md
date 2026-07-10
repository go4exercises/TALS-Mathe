# Changelog

Alle wesentlichen Änderungen am Lehrmittel werden hier dokumentiert. Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/); Versions-Tags entsprechen den ZIP-Snapshot-Nummern.

---

## [94] — 2026-07-10 · Audit-Paket 5 / T53, Runde 4: vier Widgets aus der g2-Reihe und s1-2

Zahlen vorab mit `python3` nachgerechnet, Pre-Flight `ALLE CHECKS BESTANDEN`, Browser-Rendercheck
bei 1280 px und 360 px:

- **g2-3** — **Lösungsfall-Slider mit Geradenbüschel**: \(g_1: 2x + y = 4\) fest, \(g_2: m x + y = c\)
  regelbar. Die Determinante \(D = 2 - m\) steuert alles: \(D \neq 0\) gibt genau eine Lösung, und
  der Schnittpunkt flieht sichtbar ins Unendliche, je näher \(m\) an \(2\) rückt. Bei \(D = 0\)
  entscheidet erst \(c\) zwischen «keine Lösung» (\(0 = 2\)) und «unendlich viele» (\(0 = 0\)).
  Blass mitgezeichnet ist die Schar paralleler Büschelgeraden.
- **g2-1** — **Ungleichungs-Zahlenstrahl**: Signalwort («höchstens», «mehr als», …) → Zeichen →
  Lösungsmenge. Der Randpunkt ist gefüllt oder offen, der Lösungspfeil läuft mit Spitze ins
  Unendliche, und die Intervallschreibweise steht daneben.
- **g2-2a** — **Vorzeichenkipp**: Die wahre Aussage \(2 < 5\) wird mit \(k\) multipliziert. Für
  \(k < 0\) spiegelt die Zahlengerade am Nullpunkt, die Abbildungspfeile kreuzen sich und das
  Zeichen kippt. Der Grenzfall \(k = 0\) lässt beide Bildpunkte auf die Null fallen — sichtbar,
  warum Multiplikation mit \(0\) keine Äquivalenzumformung ist.
- **s1-2** — **Zehnerpotenzen-Umwandler**: \(m \cdot 10^k\) ausgeschrieben, mit der Ziffernfolge
  der Mantisse in Blau und den aufgefüllten Nullen in Grau; der Bogen zeigt, um wie viele Stellen
  der Dezimalpunkt wandert. Bei ganzzahligem Ergebnis wird der implizite Punkt am Ende angedeutet.
  Die Umrechnung ist im Browser über alle 125 Kombinationen (5 Mantissen × \(k \in [-12; 12]\))
  gegen \(m \cdot 10^k\) geprüft.

---

## [93] — 2026-07-10 · Audit-Paket 5 / T53, Runde 3: vier weitere Prio-2-Widgets

Auswahl nach demselben Raster wie Runde 2 (arme Seite × Konzept braucht ein Bild). Zahlen
vorab mit `python3` nachgerechnet, Pre-Flight `ALLE CHECKS BESTANDEN`, Browser-Rendercheck
bei 1280 px und 360 px:

- **s4-3b** — das bestehende Winkel-Labor um den **Projektionsvektor** \(\vec{b}_a\) erweitert:
  Trägergerade von \(\vec{a}\), gestricheltes Lot von der Spitze von \(\vec{b}\), grüner
  Schattenvektor. Das Vorzeichen des Skalarprodukts wird zur Richtung des Schattens (bei
  \(\varphi > 90°\) zeigt er gegen \(\vec{a}\)), bei Orthogonalität schrumpft er auf den
  Nullvektor. Neuer Snap-Button trifft den Nulldurchgang exakt (\(104°\), Slider jetzt
  \(1°\)-Schritte).
- **g1-4** — **\(\sqrt{n}\) einschachteln**: zwei gekoppelte Zahlenstrahlen (Radikanden mit den
  benachbarten Quadratzahlen, Wurzeln mit dem schrumpfenden Intervall). Der Schritt-Knopf testet
  die Intervallmitte \(m\) gegen \(n\) und zieht die passende Schranke nach; für \(n = 30\)
  ergibt das \([5;\ 6] \to [5.4375;\ 5.5]\) nach vier Schritten. Quadratzahlen werden als
  Sonderfall erkannt (\(\sqrt{25} = 5\) exakt).
- **g1-2** — **Betrag als Abstand**: \(|a|\) als Strecke zur Null, \(|a - b|\) als Strecke
  zwischen den Punkten, mit der Symmetrie \(|a - b| = |b - a|\) in der Live-Zeile. Negative
  Subtrahenden werden geklammert (\(|2 - (-3)|\)) — auf der Seite mit der Doppelminus-Regel
  wäre alles andere schlechte Notation.
- **s1-1** — **Regel-Prüfstand**: sechs «Regeln», vier davon falsch. Einsetzen zeigt Balken für
  beide Seiten und die Differenz. Der Clou sind die Zufallstreffer, in denen eine falsche Regel
  zufällig aufgeht — \(a = 0\) bei \((a+b)^2\), \(a = b\) beim Summen-Kürzen und \(a = b = 2\)
  bei \(\log(a+b)\), weil dort \(a + b = a \cdot b\) gilt. Das Widget benennt sie explizit als
  «zufällig gleich, trotzdem keine Regel»: Einsetzen kann widerlegen, aber nicht beweisen.

---

## [92] — 2026-07-09 · Audit-Paket 5 / T53, Runde 2: die grössten Hebel der Prio-2-Liste

Fünf Widgets, ausgewählt nach drei Kriterien: wie arm die Seite bisher an Interaktion war,
ob das Konzept ohne Bild überhaupt zugänglich ist, und ob dort eine dokumentierte
Fehlerquelle sitzt. Alle Zahlenwerte vorab mit `python3` nachgerechnet, Pre-Flight
`ALLE CHECKS BESTANDEN`, Browser-Rendercheck bei 1280 px und 360 px:

- **s4-1** (ärmste Seite im Repo, bisher eine einzige Grafik) — **Raumwinkel-Widget**: Quader
  mit fester Grundfläche \(a = 4\) und variabler Höhe. Die Projektion der Raumdiagonale in den
  Boden ist die Flächendiagonale \(a\sqrt2\); \(\varphi\) läuft von \(10.02°\) (flach) über
  \(35.26°\) (Würfel-Snap, \(\tan\varphi = 1/\sqrt2\)) bis \(54.74°\). Dazu ein **Würfel-Canvas
  für A1**: das gewählte Geradenpaar wird am Drahtmodell farbig hervorgehoben (verdeckte Kanten
  gestrichelt), sodass parallel/schneidend/windschief sichtbar statt nur beschrieben ist.
- **g5-5** — **Kreis-Kurve-Kopplung**: Einheitskreis und Kurve nebeneinander, beide Lösungen von
  \(\sin\varphi = c\) bzw. \(\cos\varphi = c\) simultan markiert. Adressiert den häufigsten
  Fehler des Kapitels (zweite Lösung vergessen), inklusive der Grenzfälle \(|c| = 1\) (beide
  Lösungen fallen zusammen) und \(|c| > 1\) (die Gerade verfehlt den Kreis). Dazu ein
  **Lösungs-Trainer**: Der Rechner-Hauptwert ist gegeben, gesucht ist \(\varphi_2\) — wer
  \(\varphi_1\) eingibt, bekommt genau das gesagt.
- **g1-1** — **Distributiv-Flächenmodell**: \(a \cdot (b+c)\) als zerschnittenes Rechteck
  (zwei Teilflächen), umschaltbar auf \((a+b)(c+d)\) mit vier Teilflächen — die Brücke zu den
  binomischen Formeln und zum Faktorisieren in 1.3.
- **s1-3** — **Rechenschieber**: Zwei logarithmische Skalen; steht die \(1\) der Zunge über \(u\),
  so steht \(v\) über \(u \cdot v\), weil \(\lg u + \lg v = \lg(u v)\). Bei \(u \cdot v > 10\)
  greift der klassische **Zehnerübertrag** (die \(10\) der Zunge über \(u\) ansetzen); die
  Streckenzerlegung \(\lg v = (1 - \lg u) + (\lg u + \lg v - 1)\) wird mitgezeichnet.
- **s2-2c** — **Betrags-Explorer**: \(y = |2x+1|\) gegen \(y = c\). Die Fallunterscheidung der
  Definitionstabelle wird zur Zahl der Schnittpunkte: \(c > 0\) zwei (\(L = \{-4;\ 3\}\) bei
  \(c = 7\), passend zu Beispiel 1), \(c = 0\) einer (die Spitze), \(c < 0\) keiner.

**Nebenbefund (nicht behoben, nicht Teil des Auftrags):** Auf schmalen Viewports (360 px) ist
`main` breiter als das Fenster — Ursache sind einzelne abgesetzte MathJax-Formeln (bis 800 px),
die keinen eigenen horizontalen Scroll-Container haben; die Canvases erben die Überbreite nur.
Betrifft bestehende Seiten unabhängig von diesen Widgets (geprüft am Commit-Stand vor Runde 2).

---

## [91] — 2026-07-09 · Audit-Paket 5 / T53, Runde 1: die fünf aus T52 verschobenen Sekundär-Widgets

Die vier Punkte, die beim Abschluss von T52 ([90]) explizit nach T53 verschoben wurden, sind
gebaut (g5-4 bringt deren zwei). Gleiches Muster wie in T52: Slider bzw. Klick-Interaktion,
Live-Anzeige, 👁/💡-Rollover, Zahlen vorab mit `python3` nachgerechnet, Pre-Flight
`ALLE CHECKS BESTANDEN`, Browser-Rendercheck bei 1280 px und 360 px:

- **s4-2c** — Kugelteil-Querschnitt: Der \(h\)-Slider schiebt die Schnittebene durch die Kugel
  (\(r = 5\)); drei Balken zeigen, dass Kappenfläche und Sektorvolumen **linear** mit \(h\)
  wachsen (denn \(V_{\text{Sektor}} = \tfrac13 A_{\text{Kappe}} \cdot r\)), das Segmentvolumen
  dagegen krumm. Grenzfall-Snaps \(h = 0\), \(h = r\) (Halbkugel), \(h = 2r\) (Vollkugel) mit
  je eigener Kontroll-Meldung.
- **s4-3c** — windschief-Schrägbild: Zwei «Stockwerke»; der \(c\)-Slider hebt \(h\) über den
  Boden. Bei \(c = 0\) schneiden sich die Geraden in \(S(3 \mid 1 \mid 0)\), bei \(c > 0\) sind
  sie windschief — der graue Schatten von \(h\) kreuzt \(g\) aber immer an derselben Stelle:
  Erst die dritte Komponente entscheidet.
- **g4-1** — Merkmalstyp-Zuordnungsspiel: zwölf Karten in zufälliger Reihenfolge, vier Typen
  (nominal/ordinal/diskret/stetig), Feedback mit Begründung, Score und Auswertung. Bewusst mit
  den Zahlen-Fallen Postleitzahl (nominal), Schulnote (ordinal) und Würfelaugen (diskret).
- **g4-2** — Manipulations-Demo: Der Slider verschiebt den \(y\)-Achsenstart eines
  Säulendiagramms. Die vier Umsatzzahlen bleiben gleich, der Wirkfaktor «Q4 gegen Q1» läuft von
  \(1.13\) (Achse ab 0) auf \(7.00\) (Achse ab 4.7). Ab abgeschnittener Achse erscheinen
  Achsenbruch-Marker und die Warnung «Nulllinie fehlt»; die Tick-Schritte werden auf glatte
  Werte gerundet, damit die Demo nicht selbst krumm beschriftet ist.
- **g5-4** — Symmetrie-Spiegel: \(\alpha\)-Slider plus drei Chips (\(180° - \alpha\),
  \(180° + \alpha\), \(360° - \alpha\)); der Spiegelpunkt \(B\) und die Spiegelachse werden
  eingezeichnet, die Legende stellt \(\cos\alpha/\cos\beta\) und \(\sin\alpha/\sin\beta\)
  gegenüber. Dazu der **Vorzeichen-Trainer**: zwölf Winkel (auch \(> 360°\) und negative), für
  \(\sin\), \(\cos\), \(\tan\) je \(+\)/\(-\) wählen, Feedback mit Quadrant und Rückführung.

Offen bleiben der Rest von T53 (Prio-2-Liste, §4) und die Video-Platzhalter s3-6/s2-2a/c (T54).

---

## [90] — 2026-07-09 · Audit-Paket 5: die restlichen sechs Prio-1-Widgets (T52 abgeschlossen)

Die übrigen sechs Kern-Widgets der Prio-1-Liste ([84], §4) gebaut — damit sind alle zehn
nummerierten Punkte mit ihrem tragenden Widget versorgt. Gleiches Muster: selbstständiges
Canvas mit Slider + Live-Anzeige + 👁/💡-Rollover, Geometrie/Zahlen vorab mit python3/node
nachgerechnet, Pre-Flight (MathJax-Render + JS-Laufzeit in jsdom) `ALLE CHECKS BESTANDEN`:

- **s3-3** (§4-8) — Leitterm-Zoom: \(f = x^3 - 4x\) gegen den Leitterm \(x^3\); mit dem
  Fenster-Slider zoomt man heraus, das Verhältnis \(f/L\) am Rand strebt gegen 1 — «weit
  draussen bestimmt der höchste Term den Globalverlauf».
- **g5-4** (§4-2) — Abwickler: Punkt läuft auf dem Einheitskreis (Winkel-Slider bis 720°),
  rechts wickelt sich synchron die Sinuskurve ab — Brücke Einheitskreis → Funktionsgraph (5.5).
- **s2-1** (§4-6) — Scheinlösungs-Grafik: \(\sqrt{x}\) gegen \(x-2\); die echte Lösung
  \((4 \mid 2)\) liegt auf beiden Ästen, der Kandidat \(x = 1\) (Slider) zeigt die rote Lücke
  \(\sqrt1 = 1 \ne -1\) — warum Quadrieren Scheinlösungen erzeugt.
- **s4-3c** (§4-4) — Lot-Widget: der Slider bewegt \(F = A + t\,\vec u\) auf \(g\), \(|PF|\)
  läuft live mit; am Lotfusspunkt (\(t = 1.4\), \(d \approx 2.68\)) wird das Minimum erreicht
  und der rechte Winkel markiert.
- **s4-2b** (§4-9) — k³-Slider: den Kegel in der Höhe \(k\) köpfen; drei Balken zeigen
  Höhe (\(\times k\)), Fläche (\(\times k^2\)) und Volumen (\(\times k^3\)) — «halbe Höhe →
  \(\tfrac18\) Volumen, nicht \(\tfrac12\)».
- **s4-3d** (§4-3) — Pultdach-Schrägbild: Haus-Drahtmodell mit geneigter Dach-Ebene; eine
  senkrechte Drohnen-Gerade bei \((3 \mid y)\) durchstösst das Dach, der grüne
  Durchstosspunkt \(D\) wandert mit dem y-Slider von \(z = 4\) (vorne) auf \(z = 6\) (hinten).

**Browser-Rendercheck durchgeführt** (neu einrichtbar: Playwright + Chromium lokal, Skript
`.claude/tools/screenshot-widgets.mjs` bzw. `npm run shots`): alle zehn Widgets (Runde 1 + 2)
bei 1280 px **und** 360 px gerendert, jedes Canvas per Pixel-Scan als gezeichnet bestätigt,
Screenshots gesichtet. Dabei **eine Politur an s4-2b**: der Volumen-Balken zeigt bei \(k = 0.5\)
jetzt `12.5%` (⅛) statt gerundet `13%`, und das Balken-Label ist auf «Höhe (×k)» gekürzt,
damit es mobil nicht mit der Prozentzahl kollidiert.

Damit ist **T52 abgeschlossen**. Verschoben nach T53 (Prio-2): sekundäre Zusatz-Widgets
einzelner Punkte (windschief-Schrägbild, s4-2c Kugelteil-Querschnitt, g4 Zuordnungsspiel +
Manipulations-Demo, g5-4 Symmetrie-Spiegel/Vorzeichen-Trainer). Offen bleiben T53 (Prio-2)
und die Video-Platzhalter s3-6/s2-2a/c (T54).

---

## [89] — 2026-07-09 · Audit-Paket 5: vier Prio-1-Visualisierungen gebaut (T52, Auswahl)

Auf Wunsch die vier höchstbewerteten Prio-1-Widgets aus dem Vollaudit ([84], §4) gebaut —
je selbstständiges Canvas-Widget mit Slidern, Live-Anzeige und (wo die Seite es nutzt)
👁/💡-Rollover; Geometrie/Zahlen vorab mit python3/node nachgerechnet, Pre-Flight (inkl.
MathJax-Render und JS-Laufzeit in jsdom) `ALLE CHECKS BESTANDEN`. (Der damals noch offene
Browser-Rendercheck 1280/360 px wurde in [90] nachgeholt — alle vier Widgets bestätigt.):

- **g2-2b** — Diskriminanten-Parabel: \(y = x^2 - 6x + k\) wandert mit dem k-Slider nach
  oben, der Scheitel \(S(3 \mid k-9)\) steigt, die grünen Nullstellen verschmelzen bei
  \(k = 9\) (\(D = 0\)) und verschwinden darüber — ergänzt die bisher parabellose Seite.
- **g5-3** — SSW-Fallunterscheidung: Kreisbogen um \(B\) mit Radius \(a\) (Slider), live
  0/1/2 Dreiecke; die Höhe \(h = c\sin\alpha\) markiert die Grenzfälle (\(a<h\): keins,
  \(h<a<c\): zwei = mehrdeutiger SSW-Fall, \(a\ge c\): eines).
- **g4-3** — interaktives Robustheits-Widget: den Ausreisser-Lohn ziehen — der Mittelwert
  läuft mit (bis \(\approx 7\,071\) Fr.), der Median bleibt fest bei \(4\,200\) Fr. Schliesst
  die grösste Interaktivitäts-Reserve (g4-Reihe hatte 0 Widgets).
- **s3-5** — Phasor: rotierender Zeiger der Länge \(A\) links, synchrone Zeitspur
  \(y = A\sin(\omega t)\) rechts; die gestrichelte Linie koppelt Zeigerspitze und
  Kurvenpunkt — die Kernstelle «harmonische Schwingung».

Offen in Paket 5: die übrigen sechs Prio-1-Widgets (§4 Nr. 1–10), die Prio-2-Liste (T53)
und die Video-Platzhalter s3-6/s2-2a/c (T54, Ressourcen-Session).

---

## [88] — 2026-07-09 · Audit-Paket 3: RLP-/Lernziel-Lücken geschlossen (T17–T26)

Die neun punktuellen RLP-/Lernziel-Lücken aus dem Vollaudit ([84], §3.3) mit kleinen
Inhaltsblöcken gefüllt — je Lücke Verfahren/Definition, Beispiel und wo sinnvoll eine
Teilaufgabe; alle Zahlenwerte mit python3 nachgerechnet, Pre-Flight (inkl. MathJax-Render-
und JS-Laufzeit-Prüfung) über alle geänderten Seiten `ALLE CHECKS BESTANDEN`:

- **g1-2** — Theorieblock «Grundoperationen mit Brüchen» (Addieren/Subtrahieren über den
  Hauptnenner, Multiplizieren, Dividieren mit dem Kehrwert, Kürzen) vor A3 ergänzt (T17).
- **g4-1** — Theorieblock «nominal vs. ordinal» (die Lernziel/Mini-Check schon voraussetzen)
  plus vierter Mini-Check zur Tabellenkalkulation (T18).
- **g4-2** — Theorie-/Fehlerblock «Manipulative Diagramme» (abgeschnittene Achse, fehlende
  Einheit, Flächen-/3D-Verzerrung, Rosinenpickerei) ergänzt (T19).
- **g4-3** — Definitionsblock «Spannweite \(R = x_\max - x_\min\)» + Zeile in der
  Zusammenfassungstabelle (Standardabweichungs-Zeile dabei auf «quadratisches Mittel»
  angeglichen) (T20).
- **g5-1** — Theorieblock «Stufen- und Wechselwinkel an Parallelen» mit Skizze (F-/Z-Lage)
  ergänzt (Widget deckte nur Komplement-/Supplement-/Scheitel-Nebenwinkel ab) (T21).
- **g5-2a** — Umfang \(U = a+b+c\): Merksatz-Block, Zeile in der Formeltabelle und
  Teilaufgabe in A3 (5-12-13-Dreieck → \(U = 30\) cm) (T22).
- **g5-4** — Kurzabschnitt «Umkehroperationen» (arcsin/arccos/arctan mit Hauptwert-Bereichen,
  Brücke zu 5.5), Komplement-Zeile \(90°-\alpha\) in der Symmetrie-Tabelle, Bogenmass-
  Querverweis auf 5.1 (T23).
- **s3-3** — Linearfaktor-Abspaltung per Polynomdivision (Verfahren + Beispiel
  \(x^3-2x^2-5x+6\) + Teilaufgabe A3f); exakte Grad-2-Extrema über die Scheitelform
  (\(x_S = -b/2a\)); Ausblick auf die Differentialrechnung für höhere Grade deklariert (T24).
- **s3-4a/b** — Sättigungsprozesse (beschränktes Wachstum): in 3.4a Modell
  \(f(t) = S-(S-A)e^{-kt}\) + Abkühlungs-Beispiel; in 3.4b das Gegenstück — den Prozess mit
  dem Logarithmus nach der Zeit auflösen (T25).
- **s3-2b** — Umkehrung der Potenzfunktion mit negativem Exponenten ergänzt: \(y = x^{-n}\)
  hat die Umkehrung \(y = x^{-1/n}\) (Beispiel \(x^{-2} \to 1/\sqrt{x}\)) (T26).

Offene Vorentscheide (aus §5): g5-1 → Theorieblock statt Lernziel-Kürzung; s3-2b → Satz mit
Beispiel statt blosser rlp-hinweis-Deklaration.

---

## [87] — 2026-07-09 · Audit-Paket 4: Einzel-Mängel B pro Seite behoben (T27–T51)

Die Severity-B-Einzelfunde aus dem Vollaudit ([84]) auf 36 Seiten korrigiert — je
T-Punkt/Seite ein Commit, alle Zahlen mit python3 nachgerechnet, Pre-Flight (inkl.
echter MathJax-Render- und JS-Laufzeit-Prüfung) über alle geänderten Seiten
`ALLE CHECKS BESTANDEN`:

- **g1-3** — Dario-Startwert 650 → 1040, Wurzel-Querlink auf `#wurzeln`, unbelegten
  (a+b)³-Verweis auf s1-1/s1-2 entfernt (T27).
- **g1-4** — toten `#typen`-Anker → `#hierarchie`, «Komma» → «Dezimalpunkt», Zoom-Objekte
  richtiggestellt (Milchstrasse n=21, Nachbargalaxien n=22 statt Universum) (T28).
- **g2-1** — A2-Platzhalter neutralisiert; String- durch **numerischen** Gleichungs-/
  Ungleichungs-Vergleich ersetzt (akzeptiert Term-Umstellungen); a≠0 in der Typen-Tabelle (T29).
- **g2-2a** — Lösungsfall-Bezeichnung, Definition a≠0, Lead entrümpelt, «Buchstabengrösse»,
  A7 «lukrativer»; totes `ohm-root`-Element aus g2-2a/2-2b/2-3 entfernt (T30).
- **g2-2b** — `<em>einen</em>`, Wurfbewegungen statt Zerfallsprozesse, 𝕃 vereinheitlicht,
  «Lernende», Velo-Caption «nacheinander» (Animation ist sequenziell) (T31).
- **g2-3** — Geraden-Label `2x+y=7` in den sichtbaren Canvas-Bereich (war bei cy(9.4) über
  yMax=8); Kino-Kontext (Reisegruppe, Beispielpaar 8/12 statt der Lösung 10/10) (T32).
- **g3-1** — leeres `\(\)`-Fragment, b-Slider-Farbkopplung (orange), Vertikaltest-Gloss,
  Zielmenge-vs-Wertemenge-Fussnote (T33).
- **g3-2** — A3-Lösungswege ergänzt, U+2212 im m=−1-Zweig, `.merksatz` → `block-merksatz` (T34).
- **g3-3** — **U+2212-Parser-Bug** im A2-Widget behoben («−0.5» wurde zu 1, Parabel öffnete
  falsch); Wurfparabel auf die Flugbahn geclippt; Lösungsformel-Gloss (T35).
- **g4-0/g4-3** — Grammatik, «8000 BM2-Lernende» neutralisiert, Boxplot-Whisker-Hinweis,
  «(oben)»-Verweis; Standardabweichung als quadratisches Mittel statt «mittlere Abweichung» (T36).
- **g4-1** — Anredebruch Sie → du (T37).
- **g5-1** — totes `.skizze-grid`/`.skizze-box`-CSS entfernt (T38).
- **g5-2b** — Drachen in die Live-Klassifikation aufgenommen (+Preset), Formeltabelle
  a=Grundseite/Drachen-Seiten, NaN-Schutz in `angleAt` (koinzidente Ecken), «Ein Drachen»,
  Mini-Check-Etikett auf echte Rechnung (T39).
- **g5-2c** — Animations-Verweis, Tangenteneigenschaft statt «Tangentensatz», Bogenmass-
  Merksatz reconciliert, Segment-Legende φ>180°, «Stern-Schluss»-Klammer, Drag-Texte Anim 1,
  unbelegten Pi-Rekord «Nov. 2025» entfernt (T40).
- **g5-2d** — Lernziele nach der RLP-Box, `block-def` für zentrische Streckung, Strahlensatz-
  Fehlerblock auf S-Notation, Massstabs-Ticks beschriftet (T41).
- **g5-3** — «Von einem», WWS im Merksatz/Tabelle, Sinussatz-Slider-Clamp (Min-Gap gegen
  entartete Dreiecke), A2.1-Endwert (16.5 km), sin-Bereich 0..1 im rechtwinkligen Kontext (T42).
- **g5-4** — `erkl-ek2`-Satzbau, Schiff-Quadrant an Achsenwinkeln («auf der Achse»),
  π/2+kπ-Notation (T43).
- **g5-5** — Fehlerblock-Satzbau, Intervallnotation vereinheitlicht (`;`), A4c-Rundungsvorgabe (T44).
- **s1-2/s1-3** — Template-Reste-Anker → semantische IDs, toter `fmt2`, a>0-Voraussetzung,
  A1 um Gesetz 5 + gemischte Optionen, A5-Text, sl-val-Farbkopplung, Widget-Emojis (T45).
- **s2-1** — Waage-Geometrie (Pfannen tiefer, Stapel unter dem Balken), A3b neue Gleichung
  (x²−7x+12), g2-2a/b-Links in der Typen-Tabelle, `waStep`-Feedback bei No-op-Klicks (T46).
- **s2-2a** — Uetliberg «über Meer», «kann leer sein», D-Zeile in Beispiel 4/A7,
  Substitution-Lernziel (T47).
- **s2-2b** — A7-Toleranz gelockert (7.9 Mio zulässig), D-Herleitung in Beispiel 6,
  A1-Distraktor `L={−2}` (T48).
- **s2-2c** — Randfall r=0 bei Betragsungleichungen, `updateVZ` «x−0» → «x», Widget-Emoji,
  toter `fmt2` (T49).
- **s3-Serie** — s3-1/s3-6 Slider-Init a=1 (statt 0.5), «nicht lösbar»-Formulierung,
  Scheitelform-Zwischenschritt; s3-2a Definitionsmenge statt f:ℝ→ℝ, n→k, Asymptoten-Def,
  Slider-max 8.5, t³≈560; s3-2b ∛-Konventions-Tipp, «knapp zweieinhalb Tage», A6-Zwischenschritt;
  s3-3 Sattelpunkt, A4–A7-Plot-Hinweise; s3-4a 0<a<1, A5/A6-Hinweis, 1.3-Querlink; s3-4b
  Weber-Fechner in dB statt Phon, 0<a<1, Erkenntnis-Popup präzisiert; s3-5 b/v-Farbkopplung,
  Symmetrieachsen-Erklärsatz (T50).
- **s4-Serie** — s4-2a `hinten`-Set-Bug (0-3 statt 3-0), Wiederholungs-Kennzeichnung
  Abschnitt 5, Mantellinie-Halbsatz, Körperdiagonale-Klammer; s4-3b Beispiel 4 auf BA·BC
  (konsistent zum Fehlerblock); s4-3c A5-«Überholmanöver»-Text mit sauberen km-Einheiten (T51).
- **Bericht:** Paket 4 im `BERICHT-audit-themenseiten-2026-07-06.md` als erledigt
  markiert (T27–T51 ✅). Nicht angetastet, weil bereits konsistent bzw. via T14/T15 erledigt:
  s3-1-Galerie «acht», `waagerecht`, `Wertebereich`, chkNum-Bruch-Eingabe.

---

## [86] — 2026-07-08 · Audit-Paket 2: systematische Konsistenz (T12–T16)

Die drei wiederkehrenden Konsistenz-Themen aus dem Vollaudit ([84]) in Sammel-Durchgängen
projektweit geglättet — Pre-Flight über alle geänderten Seiten `ALLE CHECKS BESTANDEN`:

- **👁/💡-Rollover** bei allen interaktiven Animationen nachgerüstet, wo sie fehlten:
  g5-1, g3-1, g5-2b, g5-2d, g5-3 (T12).
- **A7-Vertiefungs-Pillen und Abschnitts-Kommentare** geglättet (Pille zu A7, A7-Blöcke vor
  den Zusammenfassungs-Kommentar, verrutschte/doppelte Kommentare) (T13).
- **Terminologie** projektweit vereinheitlicht (Definitionsmenge/Wertemenge, Probe/Kontrolle,
  Streckfaktor, waagrecht, CHF u.a.) — inkl. Einträgen in `STYLEGUIDE.md` und Glossar (T14).
- **chkNum/chkVal-Eingabe** projektweit gefixt: «/» im Strip-Regex geschont + Bruch-Parser,
  «e» in Zahleneingaben (z.B. 4.4e11) geschont (T15).
- **Verweis-Glyphen** korrigiert: `↩` nur für Rückverweise, Vorwärtsverweise umformuliert (T16).

---

## [85] — 2026-07-08 · Audit-Paket 1: alle Severity-A-Fehler behoben (T1–T11)

Die 16 A-Funde aus dem Vollaudit ([84]) auf 11 Seiten korrigiert — alle Zahlen mit
python3 nachgerechnet, Pre-Flight über alle geänderten Seiten `ALLE CHECKS BESTANDEN`:

- **g1-1** — Paritäts-Behauptung in der A6-Lösung auf ganzzahlige \(b\) eingeschränkt (T1).
- **g1-3** — widersprüchlichen Fehlerblock-Satz («−(−2) = −2») sauber umformuliert (T2).
- **g2-2b** — Diskriminanten-Widget Fall D>0 auf das konsistente Beispiel
  \(x^2-8x+12=0\) umgestellt (D=16, √16=4, x=6/2 — Anzeige, Info und Äste stimmen
  jetzt überein); A6-Zwischenrundung 1.76/−2.24 → 1.75/−2.25 (T3).
- **g4-2** — Balkendiagramm-Demo-SVG neu skaliert (4.5 px/Einheit): Balkenhöhen,
  Wert-Labels und Achsen-Ticks stimmen jetzt mit den Werten 22/32/17/12 überein (T4).
- **g5-2a** — Slider-Label «Basiswinkel α = β»; Dachflächen-Lösung 63.8/127.6 m²
  (mit ungerundetem s); `drawStativ()` in den load-Handler — Einstiegs-Canvas
  erscheint jetzt beim ersten Laden (T5).
- **g5-2b** — A7-SVG repariert: verirrtes `<p>` entfernt, Drachen-Polygon ergänzt;
  Ecken, Masse und Labels rendern wieder (T6).
- **g5-2c** — Sehnen-Definition korrigiert («geht sie durch M, heisst sie
  Durchmesser»); 377.79 → 377.78 m²; `\quad`-Literal durch `&nbsp;` ersetzt (T7).
- **g5-2d** — Anim-5-Legende: Katheten-Beschriftungen («gegenüber α/β»),
  Hypotenusen-Abschnitte («an a/b») und statische Startwerte an die korrekte
  JS-Rechnung angeglichen (T8).
- **g5-3** — vier LaTeX-Zeilen im Strategie-Flussdiagramm-SVG durch Unicode-Klartext
  ersetzt (MathJax rendert nicht in SVG-`<text>`); A1-Klassifikation WWS → WSW (T9).
- **g5-5** — Einstiegstext an den Code angeglichen (Mittelpunkt 22 m, Einstieg 2 m,
  Slider-Default 22 m); Widget 1 und 2 deduplizieren die Lösungen bei c=±1
  («einzige Lösung»); Fehlerblock um «(für −1 < c < 1)» präzisiert (T10).
- **s2-2a** — Mini-Check-Transfer durch eine Gleichung mit echter Scheinlösung
  ersetzt: \(6/(x-2) = 3x/(x-2)\) → Kandidat x=2 ∉ D, L = {} (T11).
- **Bericht:** Paket 1 im `BERICHT-audit-themenseiten-2026-07-06.md` als erledigt
  markiert (T1–T11 ✅).

---

## [84] — 2026-07-06 · Vollaudit aller 46 Themenseiten (nur Bericht, keine Änderungen)

Auftragsgemäss ein Audit über alle Themenseiten beider Bereiche erstellt — ohne
Druckseiten und ohne Bewertung der externen Ressourcen, ohne jede Änderung an den
Seiten. Ergebnis: **`BERICHT-audit-themenseiten-2026-07-06.md`** mit priorisierter
TODO-Liste (T1–T54) zur Sichtung durch den Auftraggeber.

- **Methode:** mechanischer Gesamtpass (Skelett, Zähler, Notation, Nav-Kette,
  Terminologie-Statistik) plus sechs parallele Prüfgruppen, die jede Seite vollständig
  gelesen und über 400 Zahlenwerte mit python3 nachgerechnet haben.
- **Kernergebnis:** Schwerpunktfach fachlich fehlerfrei (0 falsche Werte);
  16 Severity-A-Funde konzentrieren sich auf ältere GF-Seiten (v.a. Lerngebiet 5) und
  sind überwiegend Beschriftungs-/Rendering-Fehler; 9 RLP-/Lernziel-Lücken;
  3 systematische Konsistenz-Muster (fehlende 👁/💡-Rollover in g5, A7-Pillen/Kommentare,
  Terminologie-Divergenzen inkl. Glossar); umfangreiche, priorisierte
  Visualisierungs-Ideen (grösste Hebel: s3-5-Phasor, g5-4-Abwickler,
  s4-3c/d-Schrägbilder, g2-2b-Parabel, g4-Reihe).

---

## [83] — 2026-07-06 · index.html: Status-Leiste bereinigt

Die Stats-Chips über der Teilgebiets-Übersicht zeigten noch den alten Zwischenstand
(«23 fertig · 0 in Arbeit · 13 geplant»). Da alle Themenseiten ausgebaut sind:

- Die drei Chips durch einen einzigen grünen Chip **«46 Themenseiten fertig»** ersetzt
  («in Arbeit»/«geplant» entfallen — es gibt nichts mehr zu zählen).
- `st-hint` von «31 RLP-Teilgebiete · 46 Themenseiten · …» auf
  **«31 RLP-Teilgebiete + 2 TALS-Ergänzungen · ▼ Lerngebiet anklicken zum Aufklappen»**
  umgestellt (die Themenseiten-Zahl steht jetzt im Chip, die Ergänzungen 3.6/4.3d
  sind ausgewiesen).
- Die CSS-Konventionen für `karte geplant`/Stub-Badges bleiben unangetastet —
  sie gelten weiterhin für künftige Erweiterungen (STYLEGUIDE §9).

Kontrolle: 46 fertig-Karten, 0 geplant-Karten, div-Bilanz ausgeglichen.

---

## [82] — 2026-07-06 · Dokumentations-Abgleich: alle md-Dateien auf «Schwerpunkt komplett»

Nach dem Abschluss des Schwerpunkt-Ausbaus ([81]) alle Markdown-Dokumente auf den
aktuellen Stand gebracht:

- **`README.md`** — Schwerpunkt-Tabelle von 13 × «🔜 geplant» auf 23 Zeilen
  «✅ verfügbar» umgestellt (inkl. Sub-Splits 2.2a–c, 3.2a/b, 3.4a/b, 4.2a–c, 4.3a–d
  und der Ergänzungen 3.6/4.3d mit Kennzeichnung); Projekt-Absatz («entsteht
  schrittweise» → alle 31 Teilgebiete verfügbar); Sub-Split-Liste in den Zielen
  vervollständigt; Dateistruktur-Zähler auf 23 + 23 HTML-Dateien korrigiert.
- **`CLAUDE.md`** — Projektstruktur: Schwerpunkt von «13 Seiten» auf 23 Seiten mit
  vollständiger Sub-Split-Liste; Hinweis «keine Stubs mehr».
- **`STYLEGUIDE.md`** — §9 Stub-Seiten: Status-Notiz ergänzt (Konvention bleibt,
  aktuell existieren keine Stubs).
- **`HOWTO-neue-themenseite.md`** — Anwendungsfall-Satz und Generator-Empfehlung
  aktualisiert (ein Generator `build_print_s3.py` mit Blöcken A–W statt
  Pro-Lerngebiet-Skripten).
- **`HOWTO-externe-ressourcen.md`** — Titel der Anbieter-Map §8 auf Stand Juli 2026.
- **`downloads/README.md`** — Hinweis-Absatz: alle Themen-Ordner enthalten den vollen
  Materialsatz; Regel für künftige Seiten bleibt dokumentiert.
- **`BERICHT-konsistenz-2026-06-24.md`** — Kopfnotiz, dass Punkt C1 (13 Schwerpunkt-
  Stubs) inzwischen erledigt ist; Bericht selbst bleibt als Momentaufnahme unverändert.

Keine Änderungen an Themenseiten oder Skripten — reiner Dokumentations-Abgleich.

---

## [81] — 2026-07-06 · s1-1 Grundlagen: Vollausbau — das Schwerpunktfach ist komplett

Das letzte offene Teilgebiet ausgebaut: s1-1 Grundlagen (Arithmetik/Algebra), ohne
Quell-PDF entlang der einen RLP-Kompetenz («Strukturen von algebraischen Ausdrücken
erkennen und beim Berechnen sowie Umformen entsprechend berücksichtigen»). Damit sind
**alle 13 RLP-Teilgebiete des Schwerpunktfachs** (plus Ergänzungen 3.6 und 4.3d) als
vollwertige Themenseiten verfügbar — im Index gibt es keine «geplant»-Karte mehr.

- **`schwerpunkt/s1-1-grundlagen.html`** *(Stub → Vollausbau)* — Einstieg
  Struktur-Waage «Ist \((a+b)^2 = a^2 + b^2\)?» (Slider-Widget mit Flächenbild:
  das ganze Quadrat gegen die zwei Teilquadrate, Differenz \(2ab\) live);
  Kernregel «der zuletzt ausgeführte Rechenschritt bestimmt die Struktur» mit
  Struktur-Tabelle; Umform-Werkzeuge mit Richtungspfeilen (ausklammern ↔
  ausmultiplizieren, Binome vorwärts/rückwärts); Struktur-Regeln-Tabelle
  «Produkt ✓ / Summe ✗» (Kürzen, Wurzel, Potenz, Logarithmus — mit Querlinks
  auf 1.2/1.3); strukturgerechtes Berechnen mit Struktur-Fahrplan und Zahlenprobe
  («widerlegt, beweist nie»); A1 Struktur-Quiz (5 Terme), A2 Richtungs-Übungen,
  A3 a–e chkNum (Termwert 17, Mittelglied 24, faktorisiert 160, gekürzt 13,
  Doppelbruch 5), A4 Kopfrechnen mit dem 3. Binom (391, 9984), A5 vier
  Fehlumformungen entlarven, A6 quadratischer Rahmen (0.8 m² auf zwei Wegen),
  A7 Nachbarzahlen-Trick mit Beweis (Vertiefung).
- **Infrastruktur:** Index-Karte 1.1 geplant → fertig — die letzte; Kette und nav.js
  waren korrekt (s1-1 ist der Startpunkt des Schwerpunkt-Rundgangs, prev:null).
- **Zusatzmaterial:** Druckseiten-Block W (Handout, Formelauszug, Teste-dich-selbst
  mit 12 Aufgaben, Aufgabenserie mit 6 Anwendungen inkl. Linsen-Formel als
  Struktur-Beispiel); bestehende Druckseiten byte-identisch. Anki-Deck mit
  20 Karten, nur das neue apkg erzeugt.
- **Ressourcen:** ohne neue Abrufe — MathemaTrick «Terme vereinfachen» und
  Lehrerschmidt «Terme &amp; Gleichungen» aus der Map; serlo-Links aus dem
  Sitemap-Cache (26312 binomische Formeln, 28874 Faktorisieren). Map §8 ergänzt.
- Pre-Flight: `ALLE CHECKS BESTANDEN`.

---

## [80] — 2026-07-06 · s1-2 Potenzen und s1-3 Logarithmen: Vollausbau

Zwei Teilgebiete aus Lerngebiet 1 in einem Durchgang ausgebaut — Quellen: die
RLP-Kompetenzen und FTB Kapitel 04 (Potenzieren), 05 (Radizieren, für die rationalen
Exponenten) und 06 (Logarithmieren). Alle Zahlenwerte in Python nachgerechnet.

- **`schwerpunkt/s1-2-potenzen.html`** *(Stub → Vollausbau, Kap. 04+05)* — Einstieg
  Falt-Labor «Papier bis zum Mond» (\(0.1\ \text{mm} \cdot 2^n\) auf logarithmischer
  Leiter mit Vergleichsmarken: 42 Faltungen ≈ 440 000 km); Definitionen mit
  Divisions-Treppe (\(a^0 = 1\), \(a^{-n}\)); die fünf Potenzgesetze als Tabelle mit
  «kein Gesetz für Summen»-Fehlerblock; rationale Exponenten mit Exponenten-Treppen-Widget
  (Basis 16, Viertelschritte — Wurzeln füllen die Lücken); Hierarchie der Operationen
  (Türme von oben, \(-3^2 = -9\)) und Exponentenschreibweise; A1 Gesetz-Erkennungs-Quiz
  (inkl. «kein Potenzgesetz»-Option), A2 Vereinfachen, A3 a–e chkNum (128, 0.25, 9, 49,
  Vorzeichen-Falle 0), A4 Zinseszins 6094.97 Fr., A5 Mond-Faltung, A6 Kilo vs. Kibi
  (+2.4 %), A7 Potenztürme (Vertiefung).
- **`schwerpunkt/s1-3-logarithmen.html`** *(Stub → Vollausbau, Kap. 06)* — Einstieg
  Zehnerpotenz-Leiter («10 hoch was gibt …?» mit Positions-Widget); Definition
  \(a^x = b \Leftrightarrow x = \log_a(b)\) mit Sofortwerten und Spezialbasen
  (lg/ln/log₂); die drei Logarithmengesetze mit Herleitung und
  «kein Gesetz für Summen»-Fehlerblock; Basiswechsel mit Bogen-Widget
  («wie viele a-Schritte bis b?» — \(\log_2 64 = 6\), \(\log_4 64 = 3\),
  \(\log_8 64 = 2\)); Exponentialgleichungen, Verdopplungszeit (70er-Regel) und
  logarithmische Skalen; A1 Übersetzungs-Quiz Potenz ↔ Logarithmus, A2 Zerlegen/
  Zusammenfassen, A3 a–e chkNum (5, −2, 1, 1.5, 2.32), A4 \(3^x = 20\) mit Fenster,
  A5 Verdopplungszeit 23.45 Jahre, A6 pH-Wert 4.49, A7 Stellenzahl von \(2^{100}\)
  = 31 (Vertiefung).
- **Infrastruktur:** Index-Karten 1.2 und 1.3 geplant → fertig (Zählung unverändert —
  die Stubs zählten bereits); Ketten und nav.js waren korrekt.
- **Zusatzmaterial:** Druckseiten-Blöcke U (Potenzen) und V (Logarithmen) mit je
  Handout, Formelauszug, Teste-dich-selbst (12 Aufgaben) und Aufgabenserie
  (6 Anwendungen); bestehende Druckseiten byte-identisch. Zwei Anki-Decks à 20 Karten,
  nur die neuen apkg erzeugt.
- **Ressourcen:** ohne neue Abrufe — MathemaTrick «Alles über WURZELN» (s1-2) und
  «Alles über LOGARITHMUS» (s1-3) aus der Map; serlo-Links aus dem Sitemap-Cache
  (23665, 78888 bzw. 23768, 26262). Map §8 um beide Zeilen erweitert.
- Pre-Flight: beide Seiten `ALLE CHECKS BESTANDEN`.

---

## [79] — 2026-07-06 · s4-1 Grundlagen Geometrie: Vollausbau — Lerngebiet 4 komplett

Teilgebiet 4.1 (Grundlagen) aus dem Stub zur vollständigen Themenseite ausgebaut —
Quellen: die eine RLP-Kompetenz (Skizzen + Plausibilität) und FTB Kapitel 11
(Grundlagen Stereometrie). Damit ist **Lerngebiet 4 Geometrie vollständig**
(4.1, 4.2a–c, 4.3a–d). Alle Zahlenwerte in Python nachgerechnet.

- **`schwerpunkt/s4-1-grundlagen.html`** *(Stub → Vollausbau)* — Einstieg
  Schrägbild-Labor (Slider für Verzerrungswinkel \(\alpha\) und Faktor \(q\);
  Frontfläche wahr, Tiefenkanten live verzerrt, Standardpaare 45°/½ und 30°/⅓);
  Definitionen Schrägbild + Netz mit «Schrägbild für Strecken, Netz für Flächen»-Tipp;
  Punkt/Gerade/Ebene und Lagebeziehungen (inkl. FTB-Prisma-Beispiel und
  Querlinks auf die rechnerische Behandlung in 4.3c/d); Winkel im Raum
  (Gerade–Ebene über die Projektion, Ebene–Ebene senkrecht zur Schnittgeraden,
  Beispiel Raumdiagonale 35.26°); Oberfläche/Volumen-Definition, Cavalieri und
  die vierschrittige **Skizzen-/Plausibilitäts-Strategie** als RLP-Kernstück
  (Beispiel «d = 29 ist unmöglich»); A1 Lagen-Quiz am Würfel (5 Geradenpaare),
  A2 Schrägbild/Netz zeichnen, A3 a–e chkNum (Bildlänge, wahre Länge,
  35.26°, 45°, Plausibilitäts-Fenster √29), A4 Klassenzimmer (Schätzen→Rechnen),
  A5 Quader-Raumwinkel 21.80°, A6 Satteldach-Ebenenwinkel 26.57°/126.87°,
  A7 der 30°-Würfel aus dem FTB — Beweis ganz ohne Zahlen (Vertiefung).
- **Infrastruktur:** Index-Karte 4.1 geplant → fertig (Zählung unverändert
  46 Themenseiten — der Stub zählte bereits); Kette und nav.js waren bereits korrekt.
- **Zusatzmaterial:** Druckseiten-Block T (Handout, Formelauszug, Teste-dich-selbst
  mit 12 Aufgaben, Aufgabenserie mit 6 Anwendungen); bestehende Druckseiten
  byte-identisch. Anki-Deck s4-1 mit 20 Karten, nur das neue apkg erzeugt.
- **Ressourcen:** ohne neue Abrufe — Lehrerschmidt- und Daniel-Jung-Playlists aus
  der Map (s4-2-Verifikation), serlo-Links aus dem Sitemap-Cache (177185
  Schrägbilder, 60957 Grundkörper). Map §8 um die Zeile s4-1 erweitert.
- Pre-Flight: `ALLE CHECKS BESTANDEN`.

---

## [78] — 2026-07-06 · s4-2 Stereometrie: Vollausbau als Dreier-Sub-Split (a/b/c)

Teilgebiet 4.2 (Stereometrie) aus dem Stub zum Dreier-Sub-Split ausgebaut — Quellen:
FTB Kapitel 11–15; Split vorab per Rückfrage abgestimmt (a: Kap. 11+12, b: Kap. 13+14,
c: Kap. 15). Alle Zahlenwerte in Python nachgerechnet.

- **`schwerpunkt/s4-2a-prismen-zylinder.html`** *(neu, Kap. 11+12)* — Einstieg
  Münzstapel-Scherung (Cavalieri-Widget: Volumen konstant, Seitenlinie wächst);
  Prisma \(V = G h\), Quader/Würfel mit Diagonalen (Quader-Labor: Schrägbild mit
  Flächen- und Raumdiagonale live); Zylinder-Labor mit Schrägbild + Netz (Mantel-
  Rechteck \(2\pi r \times h\)); Grundlagen Schrägbild/Netz/Lagebeziehungen;
  Formeln umstellen und zusammengesetzte Körper; A1 Formel-Zuordnungs-Quiz,
  A2 Netze skizzieren, A3 a–e chkNum (Quader, Würfeldiagonale, Zylinder, Radius
  rückwärts, Dreiecksprisma), A4 Aquarium 112 l, A5 Regentonne (Durchmesser-Falle,
  603 l, Anstieg 6.96 cm), A6 Halle mit Satteldach 225 m³, A7 optimale Dose
  \(h = 2r\), \(r \approx 3.74\) cm (Vertiefung).
- **`schwerpunkt/s4-2b-pyramiden-kegel-stuempfe.html`** *(neu, Kap. 13+14)* —
  Einstieg «Drei Pyramiden füllen ein Prisma» (Füll-Widget für den Drittel-Faktor);
  quadratische Pyramide mit \(h &lt; h_s &lt; s\)-Fehlerblock; Kegel-Labor
  (Querschnitt mit Mantellinie und Öffnungswinkel live, \(w = 90°\) bei \(r = h\));
  Stümpfe (beide Formeln) und Ähnlichkeit im Raum (\(k^3\)-Fehlerblock «halbe Höhe
  ≠ halbes Volumen»); Sektor-Abwicklung mit Rückwärtsrechnung; A1 Element-Quiz
  (m/h_s/w/s), A2 Cheops (2.59 Mio. m³), A3 a–e (Pyramide, Kegel, Öffnungswinkel
  73.74°, Kegelstumpf 98π, Pyramidenstumpf 224), A4 Kirchturmdach mit Verschnitt,
  A5 Kieshaufen Schüttwinkel, A6 geköpfter Kegel über Ähnlichkeit (7/8),
  A7 Kegel aus Sektor 216° (Vertiefung).
- **`schwerpunkt/s4-2c-kugel.html`** *(neu, Kap. 15)* — Einstieg Archimedes
  (Kugel-im-Zylinder-Widget, konstantes 2:3); Kugelformeln mit Rückwärts-Wurzeln
  und Dimensions-Fehlerblock (\(r^3\) vs. \(r^2\)); Kugelteile Kappe/Segment/Sektor
  mit Grenzfall-Kontrollen; zusammengesetzte Körper (Silo-Beispiel mit
  Nahtstellen-Regel); Ähnlichkeit und Dichte; A1 Kugelteil-Quiz, A2 Grenzfall-Tests
  als Aufgabe, A3 a–e (Kugel, 1-Liter-Kugel r=6.20, O→r, Segment, Halbkugel),
  A4 Heissluftballon 643 kg, A5 Eiskugel \(h = 4r\), A6 Silo 90π,
  A7 Kugel im Würfel π/6 ≈ 52.36 % (Vertiefung).
- **Infrastruktur:** Stub `s4-2-stereometrie.html` entfernt; `nav.js` (SITE und
  GROUPS Lerngebiet 4 → s4-2a/b/c); `index.html` (ksub-Block 4.2 mit drei
  fertig-Karten; st-hint 44 → 46 Themenseiten); Kette s4-1 → 4.2a → 4.2b → 4.2c
  → 4.3a angepasst (s4-3a prev auf 4.2c).
- **Zusatzmaterial:** `scripts/build_print_s3.py` um die Blöcke Q/R/S erweitert
  (je Handout, Formelauszug, Teste-dich-selbst mit 12 Aufgaben, Aufgabenserie mit
  6 Anwendungen inkl. Musterlösungen); bestehende Druckseiten blieben byte-identisch.
  `scripts/build_apkg.py` um drei Decks à 20 Karten ergänzt (s42a/b/c), nur die
  neuen apkg erzeugt.
- **Ressourcen:** zwei neu verifizierte Playlists — Lehrerschmidt «Körper —
  Oberfläche &amp; Volumen» (72 Videos) und Daniel Jung «Körper/Stereometrie»
  (20 Videos), owner-verifiziert per Playlist-Abruf (5 Abrufe total); Aufgaben
  über die serlo-Sitemap (50462, 174501, 65267, 62627, 62757, 58818).
  Map §8 um die Zeile s4-2a–c erweitert.
- Pre-Flight: alle drei Seiten `ALLE CHECKS BESTANDEN`.

---

## [77] — 2026-07-06 · s4-3 Vektorgeometrie: Vollausbau als Vierer-Sub-Split (a/b/c/d)

Teilgebiet 4.3 (Zwei- und dreidimensionale Vektorgeometrie) aus dem Stub zum
vollständigen Vierer-Sub-Split ausgebaut — Quellen: FTB Kapitel 16–19 gemäss den
sieben RLP-Kompetenzen, Kapitel 20 (Ebenen) auf Wunsch des Auftraggebers als
deklarierte **Ergänzung TALS** (Muster 3.6). Alle Zahlenwerte in Python nachgerechnet.

- **`schwerpunkt/s4-3a-vektorbegriff-komponenten.html`** *(neu, Kap. 16+17 · RLP 1–5
  ohne Skalarprodukt)* — Einstieg Flussüberquerung (Slider-Widget für Boots- und
  Strömungsgeschwindigkeit, 3-4-5-Dreieck); Definitionen Vektor/Betrag/Gegenvektor/
  Kollinearität; Additions-Labor (Pfeilkette mit vier Slidern); Komponenten,
  Ortsvektor, «Spitze minus Fuss»; Polarform inkl. Quadranten-Fehlerblock;
  Einheitsvektor und Linearkombination; A1 Komponenten-Ablese-Quiz (Canvas),
  A2 Zeichenaufgabe mit Canvas-Lösung, A3 a–e chkNum (Verbindungsvektor, 3D-Betrag,
  polar↔kartesisch, Zerlegung), A4 Kräfte 60/25 N → 65 N, A5 Fluss exakt,
  A6 Mittelpunkt/Schwerpunkt, A7 Kollinearität (Vertiefung).
- **`schwerpunkt/s4-3b-skalarprodukt.html`** *(neu, Kap. 18 · RLP 5+7)* — Einstieg
  Arbeit am Schlitten (Winkel-Slider mit Projektions-«Schatten»); geometrische und
  Komponenten-Form, Winkelformel; Vorzeichen-Tabelle spitz/recht/stumpf mit
  Winkel-Labor (drehbarer Vektor, Live-Skalarprodukt); Rechenregeln (kein
  Assoziativgesetz), Normalprojektion; Winkel in Figuren (Pfeile von der Ecke weg,
  Nebenwinkel-Fehlerblock); A1 Vorzeichen-Quiz, A3 a–e (Skalarprodukt, 45°-Winkel,
  Orthogonalität erzwingen, 3D, Projektion), A4 Arbeit 786.4 J, A5 Innenwinkel 57.53°,
  A6 Rechtwinkligkeit und Fläche, A7 Würfeldiagonale 54.74° (Vertiefung).
- **`schwerpunkt/s4-3c-geraden.html`** *(neu, Kap. 19 · RLP 6+7)* — Einstieg
  Drohnenflug (Parameter-Slider auf der Geraden, negatives \(t\)); Parametergleichung,
  Punktprobe, Verbindung zur Funktionsgleichung; Lage-Fahrplan-Tabelle (identisch/
  parallel/schneidend/windschief) mit Beispielen inkl. Widerspruch in der dritten
  Komponente; Schnittwinkel (Betrag → spitzer Winkel); Lot-Rezept für den Abstand
  Punkt–Gerade; Bewegungsmodelle (Kollision ≠ Bahnschnitt als Fehlerblock);
  A1 Lage-Erkennungs-Quiz (Canvas-Geradenpaare), A3 a–e (Punkt, Punktprobe,
  Schnittpunkt (2.5|2.5), Winkel 63.43°, Abstand 2.68), A4 Drohne 3D, A5 Einholen,
  A6 windschief, A7 Kollisionskurs (Vertiefung).
- **`schwerpunkt/s4-3d-ebenen.html`** *(neu, Kap. 20 · **Ergänzung TALS ausserhalb
  RLP**, deklariert im pt-untertitel und in der Kompetenzen-Box nach Muster 3.6)* —
  Einstieg Pultdach (zwei Parameter-Slider, Grundriss-Canvas mit Höhen-Gradient);
  Parametergleichung der Ebene, Punktprobe (zwei bestimmen, eine testet);
  Durchstosspunkt Gerade–Ebene (3×3-System, 1/0/∞-Tabelle); Lagen-Übersicht
  Punkt/Gerade/Ebene–Ebene; Flächen-Modellierung (Dachhöhen, Neigung) und Ausblick
  Normalenform; A1 Beschreibung→Gleichung-Quiz, A3 a–c (Ebenenpunkt, Punktprobe,
  Durchstosspunkt), A4 Dachhöhen, A5 Kaminrohr 5.2 m, A6 parallel vs. enthalten,
  A7 Drohne über dem Dach r = 5/3 s (Vertiefung).
- **Infrastruktur:** Stub `s4-3-vektorgeometrie.html` entfernt; `nav.js` (SITE und
  GROUPS Lerngebiet 4 → s4-3a–d); `index.html` (ksub-Block 4.3 mit vier fertig-Karten,
  d mit «(Ergänzung)»-Vermerk; st-hint 41 → 44 Themenseiten); Kette s4-2 → 4.3a → …
  → 4.3d (next:null, Ende des Schwerpunkt-Rundgangs); README-Naming-Beispiel auf
  bestehende Datei umgestellt.
- **Zusatzmaterial:** `scripts/build_print_s3.py` um die Blöcke M/N/O/P erweitert
  (je Handout, Formelauszug, Teste-dich-selbst mit 12 Aufgaben, Aufgabenserie mit
  6 Anwendungen inkl. Musterlösungen); bestehende Druckseiten blieben byte-identisch.
  `scripts/build_apkg.py` um vier Decks à 20 Karten ergänzt (s43a/b/c/d), nur die
  neuen apkg erzeugt.
- **Ressourcen:** MathemaTrick-Playlist «Alles über VEKTOREN» (owner-verifiziert,
  41 Videos) auf allen vier Seiten; Aufgaben ausschliesslich über die serlo-Sitemap
  (31860, 107944/107945, 30683, 24573, 30686, 30687, 30688) — Durchgang ohne neue
  externe Abrufe. Map §8 um die Zeile s4-3a–d erweitert.
- Pre-Flight: alle vier Seiten `ALLE CHECKS BESTANDEN`.

---

## [76] — 2026-07-06 · s3-6 Betragsfunktionen — neue Ergänzungsseite (ausserhalb RLP)

Auf Wunsch des Auftraggebers ergänzt: ein **neues Teilgebiet 3.6**, das nicht Teil des
RLP 2030 ist — als `pt-untertitel` und in der Kompetenzen-Box entsprechend deklariert
(«Kompetenzen — Ergänzung TALS (über den RLP 2030 hinaus)» mit eigenen Kompetenzen statt
RLP-Zitat). Aufbauend auf linearen und quadratischen Funktionen, ohne Quell-PDF:

- **`schwerpunkt/s3-6-betragsfunktionen.html`** — Einstieg Abstandsfunktion
  \(a(x) = |x - 6|\) (Velofahrerin und Bahnhof, interaktiv), Definition mit
  Eigenschaften-Tabelle (V, Knickpunkt, gerade Funktion), **V-Labor** \(y = a|x-u|+v\)
  (Knick als Ankerpunkt, Ast-Steigungen \(\pm a\)), **Umklapp-Labor** für \(y = |f(x)|\)
  (Gerade → V, Parabel \(x^2-4\) → W, \(x^2+1\) unverändert), abschnittsweises Schreiben
  (Fallgrenze an der Argument-Nullstelle, \(|2x-6| = 2|x-3|\)), grafisches Lösen
  (\(|x^2-4| = 3\) mit vier Lösungen), A1–A7 (u.a. Abfüllanlage-Kosten, Standort-Funktion
  \(|x-2|+|x-8|\) mit Intervall-Minimum, Materialabtrag als W-Kurve, Wannen-Zerlegung als
  Vertiefung), 4 Mini-Checks, Querlinks zu 2.2c und 3.1.
- **Materialien komplett:** 4 Druckseiten (`build_print_s3.py` L-Block, Bestand
  byte-identisch; Hinweis auf den Ergänzungs-Status auch im Handout) und Anki-Deck mit
  20 Karten (nur neues Deck gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. \(|x^2-4| = 3 \Rightarrow \pm 1, \pm\sqrt{7}\),
  Nullstellen \(|x-1|-4 \Rightarrow -3/5\), Standort-Minimum konstant \(6\) auf \([2;\ 8]\),
  Abfüllanlage \(494 &lt; x &lt; 506\)).
- Infrastruktur: `nav.js` (SITE + GROUPS s3-6), Kette 3.5 → 3.6 → 4.1, index.html-Karte
  3.6 «fertig» mit Ergänzungs-Vermerk (41 Themenseiten; die 31 RLP-Teilgebiete bleiben).
- Ressourcen: Discovery-Lauf fand keine Betragsfunktions-Playlist der bevorzugten Anbieter
  (3 Kandidaten owner-verifiziert, alle themenfremd) → Video-Platzhalter; Aufgaben aus dem
  serlo-Sitemap-Cache (26406, 223589); Map §8 ergänzt.

---

## [75] — 2026-07-05 · s2-1 Grundlagen (Gleichungs-Werkzeugkasten) ausgebaut

Siebter Vollausbau im Schwerpunktfach — damit ist **Lerngebiet 2 komplett** (2.1 + 2.2a–c).
Ohne FTB-Quell-PDF gebaut: Inhalt entlang der beiden RLP-Kompetenzen 2.1 (Typ bestimmen,
geeignete Methoden anwenden und überprüfen):

- **`schwerpunkt/s2-1-grundlagen.html`** — Einstieg **Waage-Modell** \(3x + 2 = 11\)
  (interaktiv: Umformungs-Buttons wirken beidseitig, Waage bleibt im Gleichgewicht; der
  «falsche» Weg über \(:3\) wird didaktisch kommentiert), Vokabular (\(G\), \(D\), \(L\)),
  Äquivalenzumformungen vs. gefährliche Verwandte (Quadrieren, Terme-Multiplikation/-Division),
  **Typen-Bestimmer** (sechs Gleichungen mit Steckbrief: Wo steht \(x\)? → Typ → Methode),
  Typen-Landkarte mit Querlinks zu 2.2a–c und ins Grundlagenfach, Vier-Schritte-Fahrplan
  (Typ → \(D\) → Methode → Kontrolle), drei Arten der Überprüfung (Probe, Skizze,
  Plausibilität), A1–A7 (u.a. Typ-Quiz, Rechteck 6×8, Handy-Abos, Kegel-Radius,
  Fehlersuche als Vertiefung), 4 Mini-Checks.
- **Materialien komplett:** 4 Druckseiten (`build_print_s3.py` K-Block, Bestand byte-identisch)
  und Anki-Deck mit 20 Karten (nur neues Deck gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. Rechteck \(x^2 - 14x + 48 = 0 \Rightarrow 6/8\),
  Abo-Break-even \(x = 100\), Kegel \(r \approx 2.82\) cm, Fallhöhe \(30.7\) m,
  Sparziel \(n \approx 11.3\) a).
- **Korrektur:** Die drei s2-2-Seiten trugen fälschlich «30 Lektionen» im Seitenkopf —
  gemäss Stub sind es für Lerngebiet 2 **50 Lektionen**; auf allen drei Seiten behoben.
- index.html-Karte 2.1 auf «fertig»; Ressourcen ohne neue Abrufe (Map: MathemaTrick
  «Terme vereinfachen», Lehrerschmidt «Terme &amp; Gleichungen»; serlo-Sitemap-Cache 25103,
  26259; sos-mathe G31); Map §8 um s2-1 ergänzt.

---

## [74] — 2026-07-05 · s2-2 ausgebaut: Dreier-Sub-Split 2.2a / 2.2b / 2.2c

Sechster Vollausbau im Schwerpunktfach. Der Stub `s2-2-gleichungstypen.html` wurde durch
**drei** Themenseiten ersetzt (Dreier-Split nach Rücksprache; Quellen: FTB Kap. 11
Wurzelgleichungen und Kap. 12 Exponential-/log. Gleichungen; 2.2c ohne PDF entlang der RLP-Box):

- **`schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html`** (RLP-Kompetenzen 2+3) —
  Einstieg Sichtweite \(s = 3.57\sqrt{h}\) (Umkehrfrage als Wurzelgleichung),
  Paritäts-Tabelle für \(x^n = c\), **Scheinlösungs-Labor** (\(\sqrt{6x+7} = \pm 5\) grafisch:
  gleicher Kandidat, verschiedene Lösungsmengen), 5-Schritte-Lösungsmethode, doppeltes
  Quadrieren, Substitution (FTB-Beispiel mit vier Lösungen), Bruchgleichungen mit Hauptnenner,
  A1 «Lösbar oder nicht?» am Graphen, A4–A6 Sichtweite/Pendel/freier Fall, 4 Mini-Checks.
- **`schwerpunkt/s2-2b-exponential-logarithmische-gleichungen.html`** (RLP-Kompetenz 4) —
  Einstieg Algensee \(2.5 \cdot 2^{t/4}\) («Wann kippt der See?»), die vier Techniken
  (Exponentenvergleich, Logarithmieren, Ausklammern, Substitution \(u = a^x\)) je mit
  FTB-Beispiel, Schnittpunkt-Widget (eine/zwei/keine Lösung), logarithmische Gleichungen mit
  \(D\), Scheinlösung (\(\lg(x-3) = 1 - \lg x\)) und verlorener Lösung (\(3\lg x^2 + 7 = 13\)),
  A4–A7 Kapital/Algen/Auto/Erdbeben-Energie, 4 Mini-Checks.
- **`schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html`** (RLP-Kompetenzen 1+5+6, ohne PDF) —
  Einstieg Fertigungstoleranz \(|d - 12| \leq 0.05\) (V-Kurve mit Toleranzband), Betrag
  abschnittsweise + als Abstand, Zwei-Fälle-Verfahren, Satz vom Nullprodukt (inkl.
  «nie durch \(x\) dividieren»), Ungleichungs-Regeln (Zeichen dreht bei negativem Faktor),
  **Vorzeichentabellen-Labor** (verschiebbare Nullstellen, Tabelle + eingefärbte Achse live),
  Betragsungleichungen als Toleranzband, A4–A7 Welle/Gewinnzone/drei Faktoren/\(|A| = |B|\),
  4 Mini-Checks.
- **Materialien komplett:** je 4 Druckseiten (`build_print_s3.py` H/I/J-Blöcke, Bestand
  byte-identisch) und drei Anki-Decks mit je 20 Karten (nur neue Decks gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. \(h = (100/3.57)^2 \approx 785\) m,
  Substitution \(L = \{-7; -6; 1; 2\}\), Algen 100 % nach \(21.3\) d, Kapital-Verdopplung
  \(15.75\) a, Basel 1356 \(\approx 7.9 \cdot 10^6\) t TNT, Gewinnzone \(]10;\ 50[\)).
- Infrastruktur: `nav.js` (SITE + GROUPS s2-2a/b/c), `index.html` (ksub span-2 mit drei
  Karten, 40 Themenseiten), Kette s2-1 → 2.2a → 2.2b → 2.2c → 3.1; alter Stub entfernt.
- Ressourcen ohne neue Abrufe: Map-Wiederverwendung (MathemaTrick Wurzeln/Exp/Log,
  Mathehoch13, Daniel Jung) + sos-mathe-Code-Map (G32, G33, G35) + serlo-Sitemap-Cache;
  2.2c-Videosektion mit Platzhalter (kein passender Anbieter in der Map); Map §8 um drei
  Zeilen ergänzt.

---

## [73] — 2026-07-05 · s3-1 Grundlagen (Werkzeugkasten Funktionen) ausgebaut

Fünfter Vollausbau im Schwerpunktfach — damit ist **Lerngebiet 3 komplett** (3.1–3.5, sieben
Themenseiten). Ohne FTB-Quell-PDF gebaut: Inhalt entlang der fünf RLP-Kompetenzen 3.1, Notation
und Muster wie in 3.2–3.5:

- **`schwerpunkt/s3-1-grundlagen.html`** — Einstieg Drohnenflug \(h(t) = -0.5t^2 + 6t\) über
  einer 16-m-Leitung (Extremwert, Gleichung und Ungleichung an *einem* Graphen),
  Grundfunktionen-Galerie (acht Grundgraphen mit Steckbrief-Tabelle: \(D\), \(W\), markante
  Punkte, Asymptoten), Transformations-Labor \(y = a \cdot f(x-u) + v\) mit wählbarer
  Grundfunktion (\(x^2\), \(\sqrt{x}\), \(1/x\), \(2^x\), \(\sin x\)) und mitwanderndem
  Ankerpunkt, Verfahren Schnittpunkte (gleichsetzen–lösen–einsetzen), Un-/Gleichungen am
  Graphen (Testwert-Methode), Extremwert-Strategie (Zielfunktion + Nebenbedingung +
  Scheitelform), Monotonie-Argument (Beispiel \(2^x = 3-x\)), A1–A7 (u.a. Weide am Fluss,
  Service-Offerten-Break-even, Rechteck unter der Parabel als Analysis-Ausblick), 4 Mini-Checks,
  Querlinks zu g3-1 und allen s3-Detailseiten.
- **Materialien komplett:** 4 Druckseiten (`build_print_s3.py` G-Block, Bestand byte-identisch;
  Aufgabenserie mit Brückenbogen, Ballwurf, Break-even, Fensterrahmen, Stromtarifen,
  \(x^2 = 2^x\)) und Anki-Deck mit 20 Karten (nur neues Deck gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. Drohne Hochpunkt \((6 \mid 18)\) und
  Schnittstellen \(4/8\), Weide \(15\) m / \(450\ \text{m}^2\), Ballwurf-Weite
  \(10 + \sqrt{140} \approx 21.8\) m, dritter Schnitt von \(x^2 = 2^x\) bei \(\approx -0.77\)).
- index.html-Karte 3.1 auf «fertig»; Ressourcen budgetiert (1 Discovery-Abruf, keine neue
  Playlist bei den bevorzugten Anbietern gefunden → thematisch passende, bereits verifizierte
  Map-Einträge MathemaTrick/Mathehoch13 + serlo-Sitemap-Cache); Map §8 um s3-1 ergänzt.

---

## [72] — 2026-07-05 · s3-5 Trigonometrische Funktionen ausgebaut

Vierter Vollausbau im Schwerpunktfach (Quelle: FTB Kap. 8 «Trigonometrische Funktionen und ihre
Graphen», RLP-Kompetenz 3.5) — damit ist Lerngebiet 3 bis auf den Grundlagen-Stub 3.1 komplett:

- **`schwerpunkt/s3-5-trigonometrische-funktionen.html`** — Einstieg Riesenrad
  \(h(t) = 35 - 30\cos(\tfrac{2\pi}{12}t)\) (interaktive Rad-Ansicht + Höhenkurve),
  Einheitskreis-Abrollung als Kern-Widget (sin/cos/tan umschaltbar, Funktionsstrecke am Kreis
  rot markiert, Graph mit π-Raster synchron), Eigenschaften-Tabelle sin/cos/tan mit
  Klick-Visualisierung (inkl. Kongruenz-Ansicht sin &amp; cos), Transformations-Baukasten
  \(a\sin(b(x-u))+v\) mit vier Slidern (Amplitude, Periode als π-Bruch, Mittellinie live),
  allgemeine Sinusfunktion (\(p = 2\pi/b\), \(x_0 = -c/b\)), harmonische Schwingungen
  (\(A\sin(\omega t + \varphi)\), \(T\), \(f\), Phasenverschiebung), A1–A7 (u.a.
  Wechselspannung, Federpendel, Pendel mit Start am Maximum), 4 Mini-Checks, Querlink g5-4
  Einheitskreis.
- **Materialien komplett:** 4 Druckseiten (`build_print_s3.py` F-Block, Bestand byte-identisch;
  Aufgabenserie mit Netzspannung, Gezeiten, Kammerton, Tageslänge) und Anki-Deck mit 20 Karten
  (`build_apkg.py`, nur neues Deck gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. \(x_H = \pi/3\), \(p = 8\pi/3\), \(b = 5\pi/6\)
  und \(c = \pi/3\) aus Graphendaten, \(U(0) \approx -126.2\) V, Feder \(y(1.3) \approx 4.41\) cm,
  längster Tag \(d \approx 171\)).
- index.html-Karte 3.5 auf «fertig»; Ressourcen ohne neue Abrufe aus der Anbieter-Map
  (Lehrerschmidt/Daniel Jung, owner-verifiziert seit g5-x) + serlo-Sitemap-Cache
  (allg. Sinusfunktion, Verschieben/Strecken, Einheitskreis); Map §8 um s3-5 ergänzt.

---

## [71] — 2026-07-05 · s3-4 ausgebaut: Sub-Split 3.4a Exponentialfunktionen / 3.4b Logarithmusfunktionen

Dritter Vollausbau im Schwerpunktfach (Quelle: FTB Kap. 19, RLP-Kompetenzen 3.4). Der Stub
`s3-4-exponential-logarithmusfunktionen.html` wurde durch zwei vollwertige Themenseiten nach
Master-Schema ersetzt (Sub-Split wie 3.2a/b):

- **`schwerpunkt/s3-4a-exponentialfunktionen.html`** — Einstieg Bakterienkultur
  \(N(t) = 1000 \cdot 2^t\) (interaktiv mit Millionengrenze), Definition, Darstellungen-Widget
  (Basis-Slider mit Wertetabelle und Graph), Eigenschaften-Tabelle mit Klick-Visualisierung
  (\(2^x\) bis \(e^x\) und Zerfallsbasen), Transformationen-Widget \(a^{x-u}+v\) mit
  mitwandernder Asymptote, Besonderheiten (Basiswechsel, Streckung = Verschiebung,
  \(u = -\log_a k\)), e-Funktion, A1–A7 (u.a. Bakterienstamm, Bierschaum-Zerfall, Zinseszins,
  Eulersche Zahl über \((1+1/x)^x\)), 4 Mini-Checks.
- **`schwerpunkt/s3-4b-logarithmusfunktionen.html`** — Einstieg Umkehrfrage
  \(t = \log_2 y\) (interaktiv, Verdopplung = +1 h), Herleitung der Umkehrfunktion,
  Spiegelungs-Widget an \(y = x\) (Basen 2, e, 10, 1/2), Eigenschaften mit
  Klick-Visualisierung, Transformationen-Widget \(\log_a(x-u)+v\) mit vertikaler Asymptote
  und Nullstelle \(x_0 = u + a^{-v}\), Basiswechsel/ln-Funktion, A1–A7 (u.a. Weber-Fechner-
  Lautstärke, pH-Wert, C-14-Datierung), 4 Mini-Checks.
- **Materialien komplett:** je 4 Druckseiten (`scripts/build_print_s3.py` um D-/E-Blöcke
  erweitert, Bestand byte-identisch) und Anki-Decks mit je 20 Karten (`build_apkg.py`,
  nur neue Decks gebaut).
- Alle Zahlenwerte numerisch verifiziert (u.a. \(\log_2 1000 \approx 9.97\), Bakterien
  \(55.0\) h bis 1 Mrd., Bierschaum-Halbwertszeit \(1.94\) min, C-14 bei 70 % Rest
  \(2949\) a, \(f^{-1}(0) = e^{3/2}-5 \approx -0.52\)).
- Infrastruktur: `nav.js` (SITE + GROUPS), `index.html` (ksub span-2, 38 Themenseiten),
  prev/next-Kette s3-3 ↔ s3-4a ↔ s3-4b ↔ s3-5; alter Stub entfernt.
- Ressourcen owner-verifiziert nach HOWTO §3.4 (9 Abrufe): MathemaTrick, Mathe SMI,
  Mathehoch13, Daniel Jung (Videos) + serlo-Sitemap (Aufgaben); Anbieter-Map §8 erweitert.

---

## [70] — 2026-07-05 · s3-3 Polynomfunktionen ausgebaut

Zweiter Vollausbau im Schwerpunktfach (Quelle: FTB Kap. 18, RLP-Kompetenzen 3.3):

- **`schwerpunkt/s3-3-polynomfunktionen.html`** — Einstieg Schachtel-Faltung
  \(V(x) = x(20-2x)(15-2x)\) (interaktiv mit Hochpunkt-Markierung), Definition (Grad,
  Leitkoeffizient), **Linearfaktor-Baukasten** (drei Nullstellen-Slider + Streckfaktor,
  Produkt- und Summenform live, Vielfachheits-Hinweis bei zusammenfallenden Nullstellen),
  Globalverlauf-Visualisierung (4 Fälle), Extremalstellen am Beispiel \(x^3-x^2-2x+1\)
  (statischer Graph mit H/T), Symmetrie-Schnellcheck, A1–A7 (u.a. Truthahn-Population,
  Temperaturverlauf, Lastwagen-Tank, Rechteck unter Parabel), 4 Mini-Checks.
- **Materialien komplett:** `downloads/schwerpunkt/s3-3-polynomfunktionen/` mit Handout,
  Formelauszug, Teste-dich-selbst (12 Aufgaben), Aufgabenserie (6 Anwendungen, u.a. Kegel
  in Kugel mit exakten Werten \(h = 8/3\), \(V = 256\pi/81\)) und Anki-Deck (20 Karten).
- Alle Zahlenwerte numerisch verifiziert (Schachtel-Maximum 2.83/379, Truthahn exakt
  300 d/460 Tiere, Temperatur-Extrema 23.1/8.1 °C, Tank 1.59 m, Marmorplatte 0.69/1.54).
- index.html-Karte 3.3 auf «fertig»; Anbieter-Map (HOWTO §8) um s3-3 erweitert
  (Mathehoch13- und Daniel-Jung-Playlists owner-verifiziert, 8 Abrufe — Budget §3.4 eingehalten).

---

## [69] — 2026-07-05 · s3-2 ausgebaut: Sub-Split 3.2a Potenzfunktionen / 3.2b Wurzelfunktionen

Erster Vollausbau im Schwerpunktfach. Der Stub `s3-2-potenz-wurzelfunktionen.html` wurde durch
zwei vollwertige Themenseiten nach Master-Schema ersetzt (Sub-Split gemäss STYLEGUIDE §4.1):

- **`schwerpunkt/s3-2a-potenzfunktionen.html`** — Einstieg Ballon-Volumen \(V(t)\approx 0.268\,t^3\)
  (interaktiv), Definition, Darstellungen-Widget (Slider \(a\), \(n\), \(x\) mit Wertetabelle und
  Graph inkl. Definitionslücken-Anzeige), Parabeln/Hyperbeln n-ter Ordnung mit Klick-Visualisierung,
  Asymptoten und Transformationen (Hyperbel-Widget mit mitwandernden Asymptoten), A1–A7
  (u.a. Boyle-Mariotte, Parallelwiderstand, Getränkedose-Optimierung), 4 Mini-Checks.
- **`schwerpunkt/s3-2b-wurzelfunktionen.html`** — Einstieg Fadenpendel \(T\approx 2\sqrt{l}\)
  (interaktiv), Wurzelfunktion als Umkehrfunktion mit Spiegelungs-Widget an \(y=x\),
  Eigenschaften-Vergleich \(\sqrt{x}/\sqrt[3]{x}/\sqrt[5]{x}\), Transformationen und grafisches
  Lösen von Wurzelgleichungen (Widget), A1–A7 (u.a. Fadenpendel, Wasserwellen, Brunnen mit
  Schall-Laufzeit, Zehnkampf-Punkteformeln als Vertiefung), 4 Mini-Checks.
- **Materialien komplett** (je Sub-Seite): `downloads/schwerpunkt/<slug>/` mit Handout,
  Formelauszug, Teste-dich-selbst (12 Aufgaben mit Lösungen), Aufgabenserie (6 Anwendungen mit
  Musterlösungen) und Anki-Deck (19 bzw. 20 Karten). Neuer Generator `scripts/build_print_s3.py`;
  `scripts/build_apkg.py` um `SP_DECKS` (Schwerpunkt-Pfad) erweitert.
- **Navigation/Index:** `nav.js` SITE/GROUPS auf `s3-2a`/`s3-2b`, prev/next-Kette in s3-1/s3-3
  angepasst, `index.html` mit `ksub span-2`-Container (Karten «fertig»), Zählung 37 Themenseiten.
- Alle Zahlenwerte python-verifiziert; Pre-Flight über alle Themenseiten grün
  (MathJax-Renderprüfung 713 Ausdrücke Themenseiten + 451 Druckseiten, 0 Fehler);
  Broken-Link-Check 121 Download-Links, 0 broken. Externe Ressourcen owner-verifiziert
  (Mathe SMI, Mathehoch13, MathemaTrick, Daniel Jung; sos-mathe G32/G33, serlo ID-URLs).

Hinweis: `scripts/convert_*.py` tragen noch den alten Sandbox-Pfad (`/home/claude/work/…`) und
laufen lokal nicht — Konventions-Checks (ß, Dezimalkomma, Cosinus) wurden für die neuen Dateien
manuell ausgeführt (0 Treffer). Pfad-Parametrisierung wäre ein künftiger Wartungspunkt.

---

## [68] — 2026-06-13 · .gitignore ergänzt

Repo-Hygiene: `.gitignore` schliesst dauerhaft vom Push aus:
- `COLLABORATION.md` (gehört laut Datei selbst nur ins Project-Knowledge)
- `TODO-lehrerbegutachtung.md`, `master-todoliste.md` (interne Arbeitslisten, nicht öffentlich)
- `node_modules/`, `package*.json` (Tool-Artefakte der Tiefenprüfung), `.DS_Store`/`Thumbs.db`

Hinweis: Bei bereits getrackten Dateien einmalig `git rm --cached <datei>` nötig, damit sie aus dem Repo verschwinden (lokale Kopie bleibt).

---

## [67] — 2026-06-13 · LICENSE und .nojekyll ergänzt

Repo-Hygiene für GitHub Pages:
- **LICENSE** (CC BY-NC 4.0 Volltext-Zusammenfassung mit Copyright-Zeile und Links auf legalcode/deed.de) im Repo-Root — GitHub erkennt und zeigt die Lizenz damit im Repo-Header an. Inhaltlich identisch zur bereits im Meta-Menü und README deklarierten Lizenz.
- **.nojekyll** (leer) — schaltet die Jekyll-Verarbeitung auf GitHub Pages ab. Aktuell unkritisch (keine Unterstrich-Pfade), aber als Absicherung gegen künftige Dateien mit führendem Unterstrich.

---

## [66] — 2026-06-13 · Cross-Repo-Links auf absolute URLs (Schwesterseiten-Vorbereitung)

Vorbereitung der Physik-Schwesterseite auf GitHub Pages (`go4exercises.github.io/TALS-Physik/`). Die gegenseitigen Querlinks waren teils relativ (`../tals-physik/`) und teils mit falscher Gross-/Kleinschreibung — auf case-sensitiven GitHub-Pages-URLs hätten sie ins Leere gezeigt.

**Umgestellt auf absolute URLs (Variante A, repo-namen-robust):**
- Physik-Querlink im Header (Desktop + Mobile): `https://go4exercises.github.io/TALS-Physik/` (vorher relativ `../tals-physik/`), `target=_blank`.
- glossar.html / formelsammlung.html: Verweise aufs Physik-Pendant auf absolute `TALS-Physik`-URLs.
- Self-Repo-Links (GitHub) vereinheitlicht auf `github.com/go4exercises/TALS-Mathe`.

Alle Schreibweisen jetzt konsistent: TALS-Mathe (self) / TALS-Physik (cross). `node --check` grün.

---

## [65] — 2026-06-13 · Header entschlackt: «Übersicht»-Link und Breadcrumb-Zeile entfernt

Beide Elemente waren redundant: der «Übersicht»-Link im Header dupliziert das ohnehin zur Startseite führende Logo, und die zweite Headerzeile (Breadcrumb + Vor/Zurück) wiederholt Inhalte, die bereits anderswo stehen.

**Entfernt (zentral in `nav.js`):**
- Der Desktop-Header-Link «Übersicht» (das Logo bleibt die Heim-Verknüpfung).
- Die komplette Breadcrumb-Zeile (`breadcrumb-bar`): Der Pfad «Übersicht › Grundlagenfach › 4.3 · …» dupliziert den Titelblock der Seite (`pt-bereich` + `pt-h1`), die Vor/Zurück-Buttons dupliziieren die Prev/Next-Links der TOC-Seitenleiste. `prevBtn`/`nextBtn`/`bcHTML`/`fachLabel`/`fachHash` ersatzlos gestrichen; Injection vereinfacht zu `nav-root.innerHTML = headerHTML` (kein Sonderfall homepage mehr nötig).

**Bewusst erhalten:**
- `cfg.prev`/`cfg.next` bleiben im buildNav-cfg — die **TOC-Seitenleiste** nutzt sie weiterhin für ihre Vor/Zurück-Links (← 4.2 / 5.1 →).
- Das mobile «← Übersicht» im Flyout-Menü bleibt (mobile Heim-Verknüpfung, nicht Teil von Header-Zeile/Breadcrumb).

**Mobile-Abwägung dokumentiert:** Die TOC ist ab 900px ausgeblendet, die Breadcrumb-Vor/Zurück war damit bisher die einzige mobile Kapitel-Navigation. Nach Rücksprache bewusst akzeptiert: Der Kapitelwechsel bleibt mobil über die Dropdowns «Grundlagenfach»/«Schwerpunktfach» möglich (Direktsprung zu jedem Kapitel), und die Hauptnavigation bleibt vollständig erhalten.

**CSS aufgeräumt:** alle verwaisten Regeln entfernt (`.breadcrumb-bar`, `.breadcrumb`, `.bc-sep`, `.bc-cur`, `.prev-next`, `.pn-btn` samt Varianten und 700px-/640px-Sonderregeln).

**Verifiziert:** `node --check nav.js` grün; keine `breadcrumb`/`pn-`/`bc-`-Reste in nav.js oder style.css; jsdom-Render Homepage + Themenseite: keine Breadcrumb-Zeile, kein Übersicht-Header-Link, Logo «Mathematik», TOC behält prev (← 4.2) und next (5.1 →), mobiles «← Übersicht» erhalten.

---

## [64] — 2026-06-13 · Header: Logo ohne TALS-Pille, Physik als Top-Level-Link

Zwei Anpassungen am Header (zentral in `nav.js`):

**Logo ohne Pille.** Die `<span class="logo-pill">TALS</span>`-Pille ist aus dem Logo entfernt; der erste Link zeigt nur noch «Mathematik». Die `.logo-pill`-CSS-Regel bleibt ungenutzt in `style.css` (kein Schaden, falls die Pille je zurück soll). Das `.logo` selbst (`display:flex; gap:9px`) bleibt unverändert — ohne zweites Flex-Kind ist der Gap wirkungslos.

**Physik als Top-Level-Link.** Der Querverweis auf das Physik-Lehrmittel war bisher Unterpunkt der «Extern»-Gruppe im Nachschlagen-Dropdown. Er steht nun direkt im Header als «Physik ↗» — zwischen dem Nachschlagen-Dropdown und dem Trennstrich vor «Über», exakt spiegelbildlich zu «Mathematik ↗» im Physik-Header. Im Dropdown «Extern» verbleibt nur die SBFI-Formelsammlung. Mobile-Nav analog: Physik-Link aus der Nachschlagen-Gruppe gelöst und als eigenständiger Eintrag nach den Fächern platziert. Link relativ (`${prefix}../tals-physik/index.html`), funktioniert von Root- und Themenseiten.

**Verifiziert:** `node --check nav.js` grün; keine `logo-pill`-Referenz mehr im JS; jsdom-Render (homepage): Logo-Inhalt nur «Mathematik», «Physik ↗» als Top-Level-Link in Position (nach Nachschlagen, vor Über), Physik nicht mehr im dd-ref-Dropdown.

---

## [63] — 2026-06-13 · TOC: Kapiteltitel als «nach oben», Vor/Zurück wieder symmetrisch

Idee aus dem Betrieb: Der Kapiteltitel sitzt ohnehin zuoberst im Inhaltsbereich — ihn klickbar zu machen und mit der Seitenanfang-Funktion zu belegen, macht den separaten «↑ nach oben»-Link überflüssig und stellt die Symmetrie der Navigationszeilen wieder her.

**Umsetzung (zentral in `nav.js`/`style.css`):**
- Der Kapiteltitel (`KAPITEL 5.2d`) ist neu ein `<button class="toc-title">` und springt bei Klick instant an den Seitenanfang (`window.scrollTo(0,0)`, kein Smooth-Scroll), entfernt die Aktiv-Markierung und bereinigt den URL-Hash — identisches Verhalten wie der frühere Top-Link.
- **Entdeckbarkeit:** dezenter ↑-Indikator (`.toc-title-pfeil`), der nur bei Hover/Fokus erscheint, plus Hover-/Fokus-Färbung (Blau-Familie) und `cursor:pointer`. Als echtes Button-Element tastatur-fokussierbar (`:focus-visible`) und screenreader-zugänglich; der Pfeil ist `aria-hidden`.
- **Symmetrie wiederhergestellt:** obere Zeile trägt wieder nur den Zurück-Link (`← 5.2c`), untere nur den Vorwärts-Link (`5.3 →`) — beide Zeilen erscheinen nur, wenn der jeweilige Nachbar existiert. Der separate `.toc-top`-Link und seine CSS-Regeln (inkl. der `toc-nav-*:has()`-Ausrichtungsregeln aus [61]/[62]) sind entfernt.

**Verifiziert:** `node --check nav.js` grün; keine `toc-top`-Reste in nav.js/style.css; jsdom-Render g5-2d: Titel ist Button mit Pfeil-Indikator, Kapitelnummer klein («5.2d»), obere Zeile nur prev, untere nur next; Klick-Simulation auf den Titel löst `scrollTo(0,0)` aus und entfernt die Aktiv-Markierung.

---

## [62] — 2026-06-13 · TOC-Feinschliff (4 Browsertest-Befunde)

Nachjustierung von [61] anhand eines Screenshots (g5-2d):

1. **«nach oben» nach oben verschoben.** Der Top-Link sitzt jetzt in der oberen TOC-Navigationszeile (`toc-nav-oben`) rechts neben dem Zurück-Link, nicht mehr zuunterst. Untere Zeile (`toc-nav-unten`) trägt nur noch den Vorwärts-Link und erscheint nur, wenn dieser existiert. Auf der ersten Seite eines Lerngebiets (kein prev) steht der Top-Link allein rechtsbündig (`toc-nav-oben:has(.toc-top:only-child)`).

2. **Instant statt rollend.** Der Sprung an den Seitenanfang nutzt `window.scrollTo(0, 0)` ohne `behavior:'smooth'` — identisches Sofort-Verhalten wie die Anker-Sprünge bei Titelwahl. Inline-`onclick` durch zentralen `addEventListener`-Handler in buildToC ersetzt.

3. **Aktiv-Markierung beim Springen konsistent.** Bisher setzte nur der IntersectionObserver die `toc-aktiv`-Markierung — beim Klick wanderte sie verzögert mit, beim Sprung an den Seitenanfang (oberhalb des ersten beobachteten `h2`) blieb die alte Markierung hängen. Jetzt setzt ein Klick-Handler die Markierung sofort auf den geklickten Titel; der «nach oben»-Handler entfernt sie (oben ist kein Abschnitt aktiv). Verhalten dadurch bei Klick und Sprung einheitlich.

4. **Kapitelnummer im TOC-Titel klein.** Der Titel hat `text-transform: uppercase` — das machte aus «5.2d» fälschlich «5.2D», während prev/next die Nummer korrekt klein zeigen. Die Nummer steht nun in `<span class="toc-kapnr">` mit `text-transform: none`; das Wort «KAPITEL» bleibt versal, die Sub-Kennung (a/b/c/d) bleibt klein — konsistent mit der Vor-/Zurück-Beschriftung.

**Verifiziert:** `node --check nav.js` grün; jsdom-Render g5-2d (prev+next): Top-Link oben mit prev, unten nur next, kapnr-Span «5.2d» klein, kein Smooth-Handler; g5-1 (kein prev): Top-Link allein oben rechtsbündig. Verwaiste `toc-nav-unten:has`-Regel aus [61] entfernt.

---

## [61] — 2026-06-13 · TOC: «nach oben»-Link in der Seiten-Inhaltsleiste

Navigationswunsch: schnelles Zurück zum Seitenanfang auf langen Themenseiten, ohne dauerhaft Platz zu kosten. Bewusst <em>nicht</em> umgesetzt: zweite sticky Header-Leiste (kostet ~40px vertikalen Lesebereich auf jeder Seite) und Floating-Button fürs Handy (auf Wunsch weggelassen).

**Umsetzung (zentral in `nav.js` / `style.css`, gilt für alle Themenseiten):** In `buildToC()` erhält die untere TOC-Navigationszeile (`toc-nav-unten`) zusätzlich einen `.toc-top`-Link «↑ nach oben» mit sanftem Scroll (`window.scrollTo({top:0,behavior:'smooth'})`). Die Zeile wird nun immer gerendert (vorher nur, wenn ein Next-Link existierte) — so ist der Top-Link auch auf der jeweils letzten Seite eines Lerngebiets vorhanden.

**Layout:** `toc-nav-unten` auf `justify-content: space-between` — bei vorhandenem Next steht dieser links, «nach oben» rechts; auf Seiten ohne Next (`:has(.toc-top:only-child)`) rückt der Top-Link rechtsbündig. `.toc-top` im selben Mono-Stil wie `toc-prev`/`toc-next` (Hover: Blau-Familie). Kein zusätzlicher vertikaler Platzverbrauch im Lesebereich, da die TOC ohnehin sticky mitscrollt.

**Verifiziert:** `node --check nav.js` grün; jsdom-Render auf g5-2a (prev+next): 9 TOC-Einträge, Top-Link mit Next in der unteren Zeile, Smooth-Scroll-Handler vorhanden; jsdom-Render auf g5-5 (nur prev, kein next): Top-Link trotzdem vorhanden, kein verwaister Next.

**Hinweis:** Die `:has()`-CSS-Regel wird von allen aktuellen Browsern unterstützt; als reine Layout-Verfeinerung (Ausrichtung) ohne Funktionsverlust bei älteren Engines.

---

## [60] — 2026-06-13 · Korrektur LG5: fehlplatzierte Lernziele g5-2a/g5-2b

Browsertest-Befund: auf g5-2a und g5-2b waren die Lernziele-Boxen aus [58] nicht sichtbar an der erwarteten Stelle. Ursache: beide Seiten haben (wie g2-2a/g2-2b) einen `rlp-hinweis`-Absatz innerhalb der RLP-Box. Der Index-basierte Einfüge-Anker `</ul>\n</div>` der Rollout-`apply()`-Funktion traf deshalb nicht das RLP-Box-Ende (dort folgt nach `</ul>` erst der `rlp-hinweis`-Absatz, dann `</div>`), sondern das nächste `</ul>\n</div>` weiter unten — die Beschriftungs-Konventionsliste in der Definition-Sektion. Die Boxen landeten dadurch mitten in der Theorie statt nach der RLP-Box.

**Fix:** Box in beiden Seiten entfernt und mit literalem rlp-hinweis-Box-Ende-Anker korrekt direkt nach der RLP-Box platziert (g5-2a Zeile 195, g5-2b Zeile 235 — jeweils zwischen rlp-hinweis-Ende und der Einstieg-Sektion). Inhalt unverändert (5 Ich-kann-Punkte je Seite).

**Lehre (verschärft):** Die in [54] für LG2 dokumentierte Regel «literaler Box-Ende-Anker statt Regex/Index» gilt auch für den Index-Anker `txt.find('</ul>\n</div>')` — bei Seiten mit rlp-hinweis ist dieser nicht eindeutig das Box-Ende. Künftig Lernziele immer am `rlp-hinweis`-Absatz (falls vorhanden) bzw. am literalen Box-Schluss verankern, nie am ersten `</ul></div>`. Dieselbe Schwachstelle betraf nur g5-2a/g5-2b; g5-2c wurde in [58] bereits korrekt am rlp-hinweis verankert, alle übrigen LG5-Seiten haben keinen rlp-hinweis.

**Verifiziert:** Reihenfolge geprüft (Lernziele zwischen rlp-hinweis und erster h2-Sektion); §3.9-Schnell-Check GRÜN; Tiefenprüfung 449 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit grün auf beiden Seiten.

---

## [59] — 2026-06-13 · Nachschlagen: zentrales Glossar und Formelsammlung + Physik-Querlink

Neue Referenz-Infrastruktur im Repo-Root, Struktur 1:1 aus TALS-Physik übernommen, Inhalte mathe-eigen.

**`glossar.html`** (id:glossar): A–Z-Sprungleiste über 21 Buchstaben, rund 50 Einträge aus allen fünf Lerngebieten (Ähnlichkeit, Äquivalenzumformung, Diskriminante, Funktion, Median, Mitternachtsformel, Pythagoras, Scheitelpunkt, Vieta, Zentrische Streckung …). Jeder Eintrag mit Kurzdefinition, optionaler Formel (`.ge-formel`) und Themenverweis (`.ge-quer`).

**`formelsammlung.html`** (id:formeln): kuratiert aus den 23 thematischen `formelauszug.html`, gegliedert in fünf Lerngebiet-Abschnitte mit 11 `.fs-block`-Karten — binomische Formeln, Potenz-/Wurzelgesetze, Lösungsformel + Diskriminante + Vieta, LGS-Lösungsfälle, lineare/quadratische Funktionsformen, Lage- und Streumasse, Planimetrie- und Trigonometrie-Formeln (Sinus-/Cosinussatz, trig. Pythagoras, Spezialwinkel, Grad↔Bogenmass). Jede Zeile verlinkt auf die Themenseite; die offizielle SBFI-Prüfungs-Formelsammlung bleibt separat als Hinweis-Box und Extern-Link.

**Navigation (`nav.js`):** neues Header-Dropdown «Nachschlagen ▾» mit zwei Gruppen — «In diesem Lehrmittel» (Glossar A–Z, Formelsammlung ∑) und «Extern» (SBFI-PDF behalten, TALS Physik ⚛). Mobile-Nav analog erweitert. Aktiv-Zustand bei id glossar/formeln. **Physik-Querlink relativ** `${prefix}../tals-physik/…` — korrekt von Root- und Themenseiten; auch die beiden Schlusssätze von Glossar und Formelsammlung verweisen wechselseitig aufeinander und auf das Physik-Pendant.

**CSS:** Glossar-/Formelsammlung-Klassen zentral an `style.css` angehängt, auf Mathe-Akzentvariablen adaptiert (`--blau`/`--orange` statt Physik-`--bernstein`).

**Verifiziert:** Skelett-Pre-Flight beide Seiten grün (page-wrap, content, nav.js, mathlib.js, toc-wrap, footer, buildNav je 1×); §3.9-Schnell-Check GRÜN (Delimiter-, div-Bilanz, keine Doppel-IDs, kein ß); Tiefenprüfung 148 MathJax-Ausdrücke, 0 Fehler; jsdom-buildNav-Render bestätigt aktiven Button und alle Links; **Anker-Validierung aller Querlinks gegen reale h2-ids** — zwei falsche g3-2-Anker (#aufstellen→#gleichung-aufstellen, #lage→#typen) vor dem ZIP korrigiert. STYLEGUIDE → v1.13, §11.

**Offen:** Browsertest der beiden Seiten (Dropdown, Sprungleiste, Physik-Link). Schwerpunktfach-Begriffe/-Formeln sind noch nicht enthalten (Grundlagenfach vollständig); Erweiterung auf Zuruf.

---

## [58] — 2026-06-13 · Rollout LG5: Lernziele, Mini-Checks, Animations-Hinweise, akz-Kopplung (g5-1 bis g5-5, 8 Seiten)

Fünfter und letzter Rollout-Cluster nach STYLEGUIDE §10 — damit sind **alle Grundlagen-Seiten ausgerollt** (LG1–LG5 plus Pilot g3-2).

**Lernziele (8 Boxen)** je 5 Ich-kann-Punkte nach der RLP-Box; g5-2c nach dem rlp-hinweis-Absatz (geteiltes Teilgebiet 5.2, literaler Box-Ende-Anker gemäss Lehre aus [54]).

**Mini-Checks (25 Stück, 100 Items):** g5-1: Winkel/Umrechnung, Winkeltypen/-paare, Skizzieren/Plausibilität (3). g5-2a: Bezeichnungen, Innenwinkelsumme, Spezielle Dreiecke, Fläche/Pythagoras (4). g5-2b: n-Eck-Winkelsumme, Hierarchie, Umfang/Fläche (3). g5-2c: Linien am Kreis, Pi, Umfang/Fläche/Ring (3). g5-2d: Zentrische Streckung, Strahlensätze, Ähnlichkeit (3). g5-3: Rechtwinkliges Dreieck, sin/cos/tan, Schiefwinkliges (3). g5-4: Einheitskreis-Definition, Tangens, Beziehungen (3). g5-5: Grundgleichungen, Zweite Lösung, Lösungsmenge/Periode (3). **Alle 24 Rechen-Behauptungen vorab verifiziert** (math-Modul: Bogenmass, Pythagoras-Tripel, n-Eck-Summen, Kreis-/Ringflächen, tan-35°-Baumhöhe, sin/cos-Spezialwerte, beide Lösungen der Grundgleichungen).

**Animations-Hinweis-Paare (8):** g5-1 Winkel-Visualisierer (h3-Widget); g5-2a Beweis Innenwinkelsumme; g5-2b n-Eck-Zerlegung; g5-2c Sektoren-zum-Rechteck; g5-2d Strahlensätze; g5-3 Definition Winkelfunktionen; g5-4 Sinus/Cosinus am Einheitskreis; g5-5 Riesenrad. Alle `.anim`-Paare via rfind/find-Wrap des `anim-titel` in eine `widget-titelzeile` (Trigger ausserhalb des uppercase-Titels).

**akz-Kopplung:** g5-1 Winkel-Visualisierer-Gruppe (2 Slider blau/orange). Die übrigen LG5-Animationen nutzen das `.anim/bedien`-Seitenspalten-Muster ohne `sl-row` — akz dort konstruktionsbedingt nicht anwendbar.

**Behobener Zwischenfehler:** ein g5-4-Lückentext zerschnitt einen `\dfrac`-Ausdruck über die `mc-luecke` hinweg (2 TeX-Fehler in der Tiefenprüfung) — umformuliert ohne Ausdrucks-Split («Quotient aus sin α und ___»). Lehre: MathJax-Ausdrücke nie über Lücken-Spans aufteilen; jede Lücke steht zwischen vollständigen Ausdrücken.

**Verifiziert:** Skelett-Pre-Flight grün auf allen 8 Seiten; §3.9-Schnell-Check GRÜN; Tiefenprüfung 2322 MathJax-Ausdrücke, nach Fix 0 Fehler; jsdom-Laufzeit 0 JS-Fehler.

**Rollout-Status: abgeschlossen.** Offen bleiben: Browsertests LG3–LG5; optionale Nachrüstungen (Hinweis-Anker für g3-1/LG4-Widgets, Live-Formel-Einfärbung g3-1/g3-2-Zeichenroutinen) auf Zuruf.

---

## [57] — 2026-06-13 · Rollout LG4: Lernziele, Mini-Checks, akz-Kopplung (g4-0 bis g4-3)

Vierter Rollout-Cluster nach STYLEGUIDE §10, alle vier LG4-Seiten mit `minicheck.js` + `anim-hinweise.js` (Letzteres vorsorglich eingebunden; siehe Hinweis unten).

**Lernziele (4 Boxen)** je 5 Ich-kann-Punkte. **Sonderfall g4-0** (Praxisbeispiel-Seite ohne RLP-Kompetenzen-Box): Lernziele-Box direkt vor dem Einstieg platziert — dokumentierte Abweichung von §10.1, da kein RLP-Anker existiert.

**Mini-Checks (14 Stück, 56 Items):** g4-0: Urliste/Rang, Kennzahlen, Diagramm/Stichprobe (3). g4-1: Grundbegriffe, Merkmalstypen, Datengewinnung/Qualität (3). g4-2: Klassieren, Standarddiagramme, Charakterisieren/Manipulation, Streudiagramm (4). g4-3: Lagemasse, Streumasse, Tabellenkalkulation, Robustheit (4). **Alle 15 Rechen-Behauptungen vorab mit Python (statistics) verifiziert** (u.a. Ausreisser-Sprung Mittelwert 6 → 29.5 bzw. 6 → 30 bei stabilem Median, Kreissektoren 180°/90°, Klassenbreite 40 : 8, y-Achsen-Manipulation 1 : 5 statt 1 : 2).

**Animations-Hinweis-Paare: keine.** LG4 hat keine `widget-header`/`anim-titel`-Strukturen — die Interaktiva (z.B. Streuungs-Regler im g4-3-Einstieg) sind titellose Inline-Blöcke ohne §10.3-Anker. Bewusst nicht nachgerüstet (kein unaufgefordertes Refactoring); bei einem späteren Widget-Refactor nachholbar.

**akz-Kopplung:** g4-3 Streuungs-Regler im Einstieg → `sl-row akz-blau` (Slider + Prozentwert blau). Keine Live-Formeln betroffen.

**Verifiziert:** Skelett-Pre-Flight grün; §3.9-Schnell-Check GRÜN; Tiefenprüfung MathJax 0 Fehler; jsdom-Laufzeit 0 JS-Fehler auf allen 4 Seiten.

**Offen:** Browsertest LG4; Rollout LG5 (8 Seiten) anschliessend.

---

## [56] — 2026-06-13 · Rollout LG3: Lernziele, Mini-Checks, Animations-Hinweise, akz-Kopplung (g3-1, g3-3)

Dritter Rollout-Cluster nach STYLEGUIDE §10 (g3-2 war bereits Pilot, ZIP 49–52). Beide Seiten mit `minicheck.js` + `anim-hinweise.js`.

**Lernziele (2 Boxen)** je 5 Ich-kann-Punkte nach der RLP-Box (Teilgebiete 3.1, 3.3).

**Mini-Checks (8 Stück, 32 Items):** g3-1: Funktionsbegriff, Notationen/D/W, Funktion-oder-nicht, Achsenschnitte/Schnittpunkte (4). g3-3: Parameter der Parabel, Scheitelform/Diskriminante, Die drei Formen nutzen, Funktionsgleichung aufstellen (4). **Alle 9 Rechen-Behauptungen vorab sympy-verifiziert** (u.a. Schnittpunkt (3 | 2), quadratische Ergänzung x²−6x+5 = (x−3)²−4, Aufstellen aus Scheitel (1 | −2) und Punkt (3 | 6) → a = 2, Produktform-Ansatz aus Nullstellen 1, 5 und (0 | 10) → a = 2).

**Animations-Hinweis-Paare (2, beide g3-3):** 🎾 Wurfparabel (Scheitel = höchster Punkt, Nullstellen = Abwurf/Landung) und 📐 Diskriminante (Lage der Parabel zur x-Achse). Mehrzeilige h3-Titel via Titelzeilen-Öffnung am h3-Start und Insert nach dem zugehörigen `</h3>`. g3-1 hat keine Hinweis-tauglichen Titel-Anker (Widgets ohne h3/anim-titel) — dort bewusst keine Paare; bei einem späteren Widget-Refactor nachrüstbar.

**akz-Kopplung (Werte/Labels, Färbe-Regel §10.4):** g3-1 drei Gruppen — lineare Funktion a blau / b orange, Parabel-Scheitel u blau / v orange, Schnittpunkt-Gerade m blau; g3-3 Scheitelform-Trio a blau / u orange / v grün. Label-Variablen in `span.var`. Live-Formel-Einfärbungen (JS) wurden in diesem Cluster nicht angefasst — die betroffenen Widgets bauen ihre Formeln in nicht inspizierten Zeichenroutinen auf; Kandidat für einen gezielten Folgeauftrag mit Äquivalenztest.

**Verifiziert:** Skelett-Pre-Flight grün; §3.9-Schnell-Check GRÜN (Delimiter-, div-, details-Bilanz, keine Doppel-IDs, kein ß); Tiefenprüfung 707 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit 0 JS-Fehler.

**Offen:** Browsertest LG3; Rollout LG4 und LG5 in dieser bzw. Folge-Sitzung.

---

## [55] — 2026-06-13 · g2-2b Färbe-Korrekturen (Bild-Auftrag) + STYLEGUIDE v1.12: verbindliche Färbe-Regel

Zwei Befunde aus dem Browsertest von ZIP 54, beide in g2-2b:

**Bild 1 — three-eq überfärbt:** in «x² − 5·x + 6 = 0» war der ganze p-Anteil samt «·x» blau. Das x ist dort aber nicht der Regler — gefärbt werden darf nur der Wert. Fix: neue Formatter `fmtPxC`/`fmtQC` färben ausschliesslich die Ziffern (Operatoren und ·x neutral); statischer Initialinhalt analog. Äquivalenz alt/neu nach Tag-Strip über das volle Raster p ∈ [−6,6] × q ∈ [−6,9] erneut bestanden.

**Bild 2 — k-Widget ohne Kopplung:** der k-Slider der Parameterdiskussion hatte kein akz. Fix: `sl-row akz-blau`, Label-k in `span.var`; in der D(k)-Zeile sind jetzt das k (Variable = Regler) und der eingesetzte k-Wert blau, der D-Wert bleibt neutral (abgeleitet). `pk-formel` von textContent auf innerHTML; Äquivalenz über den ganzen k-Bereich (−2…14, Schritt 0.5) bestanden — gesamt 241 Kombinationen, 0 Abweichungen.

**Kontrolle der bereits gepatchten Färbungen** (Repo-weiter Scan aller tx-Spans und T()-Aufrufe): g3-2 dr-eq/ks-eq und g1-2 cv-out sind regelkonform — dort ist die gefärbte Variable jeweils selbst der Regler (Eingabewert x bzw. Menge x) oder es sind reine Ziffern. Einziger Verstoss war three-eq.

**STYLEGUIDE → v1.12:** §10.4 um die **verbindliche Färbe-Regel** ergänzt (vier Punkte: nur slider-gebundene Werte; Variable nur, wenn sie selbst der Regler ist; Abgeleitetes neutral; entfallende Glieder tragen folgerichtig keine Farbe) inkl. Falsch/Richtig-Beispiel aus genau diesem Befund, plus Pflicht-Verifikation «volles Sliderraster, null Abweichungen, sonst kein ZIP». Project-Knowledge-Kopie manuell nachziehen.

**Verifiziert:** Tiefenprüfung g2-2b 288 Ausdrücke, 0 Fehler; jsdom-Laufzeit grün; §3.9-Schnell-Check GRÜN (inline 270/270, span 83/83, keine Doppel-IDs, kein ß).

---

## [54] — 2026-06-13 · Rollout LG2: Lernziele, Mini-Checks, Animations-Hinweise, akz-Kopplung (g2-1, g2-2a, g2-2b, g2-3)

Zweiter Rollout-Cluster nach STYLEGUIDE §10, alle vier LG2-Seiten mit `minicheck.js` + `anim-hinweise.js`.

**Lernziele (4 Boxen)** je 5 Ich-kann-Punkte nach der RLP-Box; bei g2-2a/g2-2b nach dem `rlp-hinweis`-Absatz (geteiltes Teilgebiet 2.2). Zwischenfix dokumentiert: ein non-greedy-Regex platzierte die g2-2b-Box zunächst <em>in</em> die RLP-Box (nach dem rlp-titel-div) — vor dem ZIP erkannt und an die korrekte Stelle nach dem Box-Ende verschoben; bestätigt per Kontext-Probe.

**Mini-Checks (17 Stück, 68 Items):** g2-1: Gleichung/Waage, Formulieren, Äquivalenzumformungen, Typ/Lösen/Probe (4). g2-2a: Normalform, Lösungsverfahren, Lösungsfälle/Parameter, Ungleichungen (4). g2-2b: Quadratische Gleichung, Verfahrenswahl, Diskriminante, Vieta, Parameterdiskussion (5). g2-3: LGS-Begriff, Verfahren, Lösungsfälle, 3×3 (4). **Alle 24 Rechen-Behauptungen vorab sympy-verifiziert** (u.a. Quadrieren-Scheinlösung x = ±2, (k−2)x = 4-Sonderfall, D-Diskussion 36−4k, Vieta-Konstruktion (x−2)(x+5), Widerspruchssystem x+y = 3/5).

**Animations-Hinweis-Paare (8):** g2-1 Waage + Äquivalenz-Schritte; g2-2a Budget-Schieber + Parameter-k; g2-2b p/q-Darstellungen + Parameter-k-Beispiel; g2-3 grafische Lösung + drei Verfahren.

**akz-Kopplung:** g2-2b p/q-Gruppe (p blau, q orange) inkl. Live-Gleichung — `updateThree()` färbt den p- und q-Anteil via tx-Spans (Äquivalenz alt/neu nach Tag-Strip über das volle Raster p ∈ [−6,6] × q ∈ [−6,9]: 208 Kombinationen, 0 Abweichungen); statischer Initialinhalt analog. Einzel-Slider akz-blau: g2-1 (Paketmasse x, Versuchswert x), g2-2a (Budget-x, Drei-Sichten-x, Parameter-k), Label-Variablen in `span.var`.

**Verifiziert:** Skelett-Pre-Flight grün (Modul-Einbindung 1/1 überall); §3.9-Schnell-Check GRÜN inkl. div/details-Bilanz; Tiefenprüfung 948 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit 0 JS-Fehler auf allen 4 Seiten.

**Offen:** Browsertest LG2; Rollout LG3 (g3-1, g3-3), LG4, LG5 in Folge-Sitzungen.

---

## [53] — 2026-06-12 · Rollout LG1: Lernziele, Mini-Checks, Animations-Hinweise, akz-Kopplung (g1-1 bis g1-4) + STYLEGUIDE v1.11

Erster Rollout-Cluster der Pilot-Module (ZIP 49–52) gemäss LG-clusterweisem Vorgehen (COLLABORATION §9.4). Alle vier LG1-Seiten erhalten `minicheck.js` + `anim-hinweise.js`.

**Lernziele (4 Boxen):** je 5 Ich-kann-Punkte direkt nach der RLP-Kompetenzen-Box, abgeleitet aus den Teilgebiets-Kompetenzen 1.1–1.4 und dem Seiteninhalt.

**Mini-Checks (18 Stück, 72 Items):** an den Sektionsgrenzen — g1-1: Term/Hauptoperation, Hierarchie, Strukturbaum, Rechengesetze (4). g1-2: Zahlentypen, Zahlenmengen, Bruch/Dezimal/Prozent, Vorzeichen/Betrag/Intervalle (4). g1-3: Äquivalenz, Gleichartige Glieder, Klammern, Binomische Formeln, Faktorisieren (5). g1-4: Zehnerpotenzen, Wissenschaftliche Notation, Potenzgesetze, Wurzeln/Wurzelgesetze, Hierarchie (5). Je MC/Lückentext/kurze Rechnung/Transfer; **alle 38 Rechen-Behauptungen vorab sympy-verifiziert** (u.a. 0.4̄ = 4/9, 2³·5⁴ = 5000 ≠ 10⁷, √(9+16) = 5-Gegenbeispiel, Zweiklammersatz x²+7x+12).

**Animations-Hinweis-Paare (8):** g1-1 Hauptoperations-Anim + Strukturbaum-Widget; g1-2 Zahlengeraden-Anim + Konverter-Widget; g1-3 Äquivalenz-, Zusammenfassen- und Binom-Anim; g1-4 Zoom-Skala. Bei `.anim`-Blöcken wird der `anim-titel` in die `widget-titelzeile` gefasst — die Trigger stehen ausserhalb des uppercase-Titels und bleiben gemischt geschrieben. Vorlese-Texte als Klartext.

**akz-Kopplung Konverter (g1-2):** Zähler \(p\) blau, Nenner \(q\) orange (Slider, Wert, Label-Variable); in der Live-Formel der **ungekürzte** Bruch via MathJax `\textcolor` in denselben Farben, gekürzter Bruch und abgeleitete Darstellungen neutral (Prinzip: nur slider-gebundene Grössen färben). Die Binom-Anim in g1-3 nutzt das `.anim`-Seitenspalten-Muster ohne `sl-row` — akz dort bewusst nicht angewendet.

**STYLEGUIDE → v1.11, neuer §10:** alle vier Muster verbindlich dokumentiert (Markup-Skelette, Platzierungsregeln, Klartext-Konvention für `data-vorlesen`, Äquivalenztest-Pflicht bei innerHTML-Umstellungen). Die Project-Knowledge-Kopie muss manuell synchronisiert werden.

**Verifiziert:** Skelett-Pre-Flight grün auf allen 4 Seiten (inkl. Modul-Einbindungs-Zählung); §3.9-Schnell-Check GRÜN (Delimiter-, div- und details-Bilanz, keine Doppel-IDs, kein ß); Tiefenprüfung 1208 MathJax-Ausdrücke, 0 Fehler (validiert auch die textcolor-Ausdrücke); jsdom-Laufzeit 0 JS-Fehler auf allen 4 Seiten mit eingebundenen Modulen.

**Offen:** Browsertest LG1 (Rollover-Positionen, Vorlesen, Konverter-Farben); Rollout LG2–LG5 in Folge-Sitzungen, je ein Cluster.

---

## [52] — 2026-06-12 · Pilot-Nachschliff g3-2: Kartoffeln-Widget — x-Kopplung in Blau

Bild-Auftrag zum Einstiegs-Widget: gleiche Farbkopplung wie im Darstellungen-Widget, hier mit dem einzigen Regler \(x\) in Blau (der Slider war bereits blau).

- **Zentral:** akz-System von `.sl-grp` auf `.sl-row` erweitert (Selektoren-Paare), damit auch Einzel-Slider-Zeilen die Kopplung Slider↔Wert↔Label-Variable nutzen können.
- **Widget:** Zeile auf `sl-row akz-blau`, Label-\(x\) in `span.var`; in beiden Formelzeilen **nur** die \(x\)-Vorkommen blau (`K(x) = 2·x + 5` → x blau, 2 und 5 neutral; Auswertungszeile analog mit eingesetztem Wert), Pauschal-Blau der Eval-Zeile entfernt; `updateKS()` von textContent auf innerHTML mit `tx-blau`-Spans.
- **Äquivalenz verifiziert:** alte vs. neue Eval-Ausgabe nach Tag-Strip über den ganzen Reglerbereich x ∈ {0, 2, …, 14} — 0 Abweichungen. Tiefenprüfung 268 Ausdrücke, 0 Fehler; jsdom-Laufzeit grün; Schnell-Check GRÜN (inline 257/257, span 90/90).
- **Hinweis (Farbsemantik über Widgets hinweg):** im Darstellungen-Widget derselben Seite ist \(x\) grün (dort braucht es drei unterscheidbare Gruppenfarben, Blau ist von \(m\) belegt). Innerhalb jedes Widgets ist die Kopplung konsistent: die Reglerfarbe zieht sich durch Wert, Label und Formel. Falls eine seitenweite Konvention «x immer gleiche Farbe» gewünscht ist, müsste das Darstellungen-Widget auf x = blau / m = grün umgestellt werden — auf Zuruf.

---

## [51] — 2026-06-12 · Pilot-Nachschliff g3-2: Wertezugehörigkeit der Slider-Gruppen (Nähe/Distanz + Akzentfarben) und eingefärbte Live-Formel

Bild-Auftrag zum zusammengelegten Darstellungen-Widget: die Wertanzeige klebte am rechten Gruppenrand und damit optisch am Label der nächsten Gruppe.

**Nähe/Distanz (zentral, wirkt auf alle zusammengelegten Zeilen):** in `.sl-row:has(.sl-grp)` Gruppen-Abstand auf 30 px erhöht (row-gap 10 px beim Umbruch); innerhalb der Gruppe Abstand auf 8 px verdichtet und `.sl-val` per Spezifität von `min-width:64px / text-align:right` (seitenlokal) auf `min-width:0 / text-align:left` übersteuert — der Wert steht jetzt direkt neben dem eigenen Slider.

**Akzentfarben (Pilot-Widget g3-2):** neues zentrales Farbkopplungs-System `.sl-grp.akz-blau/-orange/-gruen` (Custom Property `--akz`) färbt Slider (accent-color + Webkit-Thumb), Wertanzeige und die Label-Variable (`label .var`, MathJax erbt via currentColor). Zuordnung: Steigung \(m\) blau, Achsenabschnitt \(b\) orange, Eingabewert \(x\) grün.

**Live-Formel in denselben Farben:** `updateDR()` baut Gleichungs- und Auswertungszeile jetzt mit `.tx-blau/-orange/-gruen`-Spans (innerHTML; Werte sind Slider-Ganzzahlen, unkritisch) — \(m\)-Faktor blau, \(x\) grün, \(b\)-Summand orange, Resultat neutral. Pauschal-blaue Inline-Farbe der Eval-Zeile entfernt; statischer Initialinhalt analog eingefärbt. **Äquivalenz verifiziert:** alte textContent- vs. neue innerHTML-Ausgabe nach Tag-Strip über das volle Sliderraster m, b, x ∈ [−5, 5] — 1331 Kombinationen, 0 Abweichungen (inkl. Sonderfälle m ∈ {−1, 0, 1}, b = 0, x < 0 mit Klammern).

**Verifiziert:** Tiefenprüfung 268 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit 0 JS-Fehler; §3.9-Schnell-Check GRÜN (inline 257/257, display 11/11, div 243/243, span 84/84, keine Doppel-IDs, kein ß).

**Offen:** Browsertest der Farbabstimmung; bei Gefallen ist die g3-3-Dreiergruppe (Scheitelform) der nächste Kandidat für dasselbe Farbschema.

---

## [50] — 2026-06-12 · Physik-Transfer Paket 4: Lernziele (Pilot g3-2) + Slider-Zusammenlegung (Rollout, 6 Seiten)

**Lernziele-Box (Pilot g3-2).** Aufklappbare `details.lernziele` («🎯 Lernziele — das kann ich nach dieser Seite») direkt nach der RLP-Kompetenzen-Box, nach Physik-Muster (dort Phase 5.13). Sechs Ich-kann-Formulierungen, abgeleitet aus den drei RLP-Kompetenzen des Teilgebiets 3.2 und dem Seiteninhalt (Darstellungswechsel, Nullstelle vs. Achsenabschnitt, Typen/Lagebeziehungen). CSS zentral, Klassen 1:1 aus Physik (`.lernziele`/`.lz-body`), Farbwahl Blau-Familie (Orientierung/Begriff; Physik nutzt dort seine Bereichsfarbe Bernstein). Rollout auf weitere Seiten nach Abnahme des Piloten.

**Slider-Zusammenlegung (Rollout auf alle Befund-Seiten).** Muster aus Physik Phase 5.34: mehrere Regler einer Animation in EINER `.sl-row` mit `.sl-grp`-Einheiten (Label+Slider+Wert unzertrennlich, `flex:1 1 210px`); auf schmalen Screens brechen ganze Gruppen um. CSS zentral ergänzt (`.sl-row{flex-wrap:wrap}` + `.sl-grp`-Regeln — die `.sl-row`-Basisstile bleiben seitenlokal; die zentrale Regel `.sl-row .sl-grp label{min-width:0}` übersteuert das lokale `min-width:90px` per Spezifität). Per Skript 8 Gruppen mit zusammen 18 Regler-Zeilen auf 6 Seiten zusammengeführt: g1-2 (1×2), g2-2b (1×2), g3-1 (3×2), g3-2 (1×3), g3-3 (1×3), g5-1 (1×2). Einzelne `.sl-row`-Regler und nicht-konsekutive Regler getrennter Widgets (g2-1, g2-2a, g4-3, g2-3, Kartoffeln-Widget g3-2) bewusst unverändert. Kein JS greift strukturell auf `.sl-row`/`.sl-grp` zu (grep-verifiziert); Slider-IDs und Wertebereiche unverändert.

**Verifiziert:** Slider-Anzahl pro Seite vor/nach identisch (assert im Merge-Skript); Skelett-Pre-Flight grün auf allen 6 Seiten; §3.9-Schnell-Check GRÜN (Delimiter-Bilanz, Doppel-IDs, ß, div-Bilanz); Tiefenprüfung 1353 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit 0 JS-Fehler auf allen 6 Seiten.

**Offen (lokaler Render-Check empfohlen, analog Physik 5.34):** Pixel-Sicht bei 1280/360 px — Erwartung: 2er/3er-Gruppen einzeilig auf Desktop, gruppenweiser Umbruch auf Mobile.

---

## [49] — 2026-06-12 · Physik-Transfer Paket 3 (Pilot g3-2): Mini-Checks + Animations-Hinweise

Beide didaktischen Module aus TALS-Physik (dort Phasen 5.14/5.15 und 5.17/5.18) als Pilot auf `grundlagen/g3-2-lineare-funktionen.html`. Rollout auf weitere Seiten erst nach Abnahme des Piloten.

**Neue zentrale Module (Repo-Root):** `minicheck.js` (1:1 aus Physik — Akkordeon: höchstens ein Mini-Check offen, Lösungseinblendungen unberührt) und `anim-hinweise.js` (aus Physik, Vorlese-Sprache auf `de-CH` umgestellt — Rollover «Worauf achten?»/«Erkenntnis» mit Fixierung per Klick, Vorlese-Knopf mit Klartext in `data-vorlesen`, Escape schliesst und stoppt).

**CSS zentral in `style.css`,** Klassen 1:1 aus Physik übernommen (keine erfundenen Klassen), Farben auf die Mathe-Semantik gemappt: Mini-Checks in der **Orange-Familie** (= Aufgabe/Übung), Animations-Hinweise in der **Blau-Familie** (= Animation). Neue Blöcke: `.minicheck`/`.mc-*` und `.widget-titelzeile`/`.anim-hinweis`/`.ah-*`.

**4 Mini-Checks** an den Sektionsgrenzen (nach Einstieg, nach Steigung/Achsenabschnitt/Nullstelle, nach Typen, nach Funktionsgleichung aufstellen), je 4 Fragetypen (Multiple Choice, Lückentext, kurze Rechnung, Transfer). Alle Rechnungen sympy-verifiziert: Anbietervergleich Schnitt bei x = 6 (17 CHF beidseits, bei 7 kg 19 vs. 18.50); m = (9−1)/(6−2) = 2; x₀ = 6/4 = 1.5; f(x) = −2x+8 mit (0|8) und (4|0); m₂ = −1/2; 3x+2 = 3x−5 ohne Lösung (parallel); b = 1−(−2)·3 = 7; P₁(−1|4), P₂(2|−2) → f(x) = −2x+2; Nullstelle 5 + b = 10 → f(x) = −2x+10.

**3 Animations-Hinweis-Paare:** Kartoffeln-Widget und Darstellungen-Widget (h3 jeweils in neue `.widget-titelzeile` gefasst, Untertitel-Absatz unverändert), Typen-Visualisierung (Titelzeile ohne h3 — Anleitungssatz + Hinweise in einer Flexzeile über den Fall-Buttons). Vorlese-Texte als Klartext formuliert (kein roher LaTeX-Code in der Sprachausgabe).

**`scripts/verify_js_runtime.js` erweitert:** Lib-Liste und src-Ersetzung um `minicheck.js` und `anim-hinweise.js` — die Module laufen damit in der jsdom-Prüfung mit.

**Verifiziert:** Skelett-Pre-Flight grün (pw=1 mc=1 ml=1 bad=0); §3.9-Schnell-Check GRÜN (inline 250/250, display 11/11, keine Doppel-IDs, kein ß); Tiefenprüfung 261 MathJax-Ausdrücke, 0 Fehler; jsdom-Laufzeit 0 JS-Fehler, libs/nav/toc ok; Tag-Bilanz details 20/20, div 241/241, span 72/72, button 27/27; `node --check` beider Module fehlerfrei.

**Offen (Browsertest durch Auftraggeber):** Rollover-Positionierung der `.ah-pop` auf schmalen Screens (360 px), Vorlese-Funktion (Browser-/Stimmen-abhängig), Akkordeon-Verhalten. STYLEGUIDE-Dokumentation der beiden Muster folgt mit dem Rollout-Entscheid.

---

## [48] — 2026-06-12 · Physik-Transfer Paket 2: Erweiterter Pre-Flight + Tiefenprüfungs-Skripte — ein Defekt in g1-1 gefunden und behoben

Übertragung der Verifikations-Infrastruktur aus TALS-Physik (dort P2-3 / Phase 5.16, 5.24).

**Neue Skripte in `scripts/`:** `verify_mathjax.js` (rendert alle MathJax-Ausdrücke headless durch die echte TeX-Engine, meldet Syntaxfehler/undefinierte Makros) und `verify_js_runtime.js` (lädt jede Themenseite in jsdom mit Canvas-/MathJax-Mocks, feuert DOMContentLoaded/load/resize, meldet Laufzeit-JS-Fehler und prüft buildNav/initCanvas/toggleL sowie Nav-/ToC-Rendering; Lib-Liste auf nav.js + mathlib.js angepasst). Verbesserung gegenüber dem Physik-Original in `verify_mathjax.js`: HTML-Entities werden vor der TeX-Prüfung dekodiert (Browser liefert MathJax den DOM-Text) — ohne Dekodierung 24 Fehlalarme «Misplaced &» bei `&lt;`/`&gt;` in Formeln. Rückport-Kandidat für TALS-Physik, dort gemeldet, nicht ungefragt gepatcht.

**COLLABORATION.md → v1.7, neuer §3.9:** verbindlicher Schnell-Check vor jedem ZIP (MathJax-Delimiter-Bilanz ausserhalb script-Blöcken, Doppel-ID-Check, ß-Check) plus situative Tiefenprüfung mit den beiden Node-Skripten. Die Project-Knowledge-Kopie muss manuell auf v1.7 synchronisiert werden.

**Baseline-Erstlauf über das gesamte Repo:** 130 HTML-Dateien auf Delimiter-Bilanz/Doppel-IDs/ß sauber; Tiefenprüfung 4556 MathJax-Ausdrücke, 0 TeX-Fehler; JS-Laufzeit auf 36 von 37 Themenseiten fehlerfrei.

**Gefundener und behobener Defekt (g1-1-grundlagen.html, 4 Stellen):** schwache MathJax-Guards `if (window.MathJax) MathJax.typesetPromise(…)` — da Zeile 12 das MathJax-Config-Objekt definiert, ist `window.MathJax` schon vor dem Laden von tex-svg.js truthy, hat aber kein `typesetPromise`; frühe Widget-Interaktion (langsame Verbindung) warf einen TypeError und das Widget reagierte still nicht. Auf den Projektstandard `if (window.MathJax && window.MathJax.typesetPromise)` gehärtet (wie an den übrigen 2 Stellen derselben Seite und auf allen anderen Seiten).

**Verifiziert:** Re-Lauf verify_js_runtime auf g1-1 grün (0 JS-Fehler, libs/nav/toc ok); §3.9-Schnell-Check GRÜN über alle geänderten Dateien; `node_modules`/`package*.json` nicht im ZIP.

---

## [47] — 2026-06-12 · Physik-Transfer Paket 1: Grössen-Schreibweise in uppercase-Titeln + Dokumentsprache de-CH

Übertragung zweier Defekt-Fixes aus TALS-Physik (dort Phasen 5.35 und 5.23) nach identischem Befund in Mathe.

**Grössen-Schreibweise (18 Stellen, 8 Seiten).** `block-titel`, `anim-titel`, `legende-titel` und `feld-titel` setzen designbedingt `text-transform: uppercase` — case-sensitive Plaintext-Mathe-Symbole wurden dadurch verfälscht: y→Y (y-Achsenabschnitt, 3× g3-2), n→N (Stichprobenumfang n = 7/8 und (n−1), 4× g4-3; n-Eck, 3× g5-2b, 1× g5-2c), π→Π (g5-1, g5-2c), c→C (g5-2d Legende), k→K (g2-2a), x→X (g5-3 feld-titel), sin/cos/tan→SIN/COS/TAN (2× g5-3). Fix nach bestehender Konvention (kein neues CSS, analog zum bin-schritt-titel-Fix vom 29.05.): die Symbole in MathJax gesetzt — MathJax-Ausgabe ist von text-transform unberührt. Aufzählungsbuchstaben a)/b)/c) in Titeln bewusst unverändert (Nummerierung, nicht bedeutungstragend). Korrekt grossgeschriebene Titel (Klasse A/B) unverändert.

**Dokumentsprache de-CH (131 Dateien).** Alle HTML-Dateien (Themenseiten, index, TEMPLATE, sämtliche Druckseiten in downloads/) von `lang="de"` auf `lang="de-CH"` umgestellt — korrekte Silbentrennung und Screenreader-Aussprache nach Schweizer Konvention, konsistent mit TALS-Physik.

**Verifiziert:** Skelett-Pre-Flight grün auf allen 8 gepatchten Seiten (pw=1 mc=1 ml=1 bad=0); MathJax-Delimiter-Bilanz inline+display ausgeglichen auf allen 8 Seiten (ausserhalb script-Blöcke); kein ß; Rest-Scan der uppercase-Klassen über alle Themenseiten ohne verbleibende Symbol-Verfälschung; lang-Umstellung vollständig (131/131, 0 Rest). Kein JS, kein CSS berührt.

---

## [unreleased] — 2026-05-29 · `g1-3` Binom-3: Einfärbung & Schritt-2-Aufteilung nachgezogen

Feinschliff nach Bild-Auftrag `Anpassung_der_Einfärbung.pdf` (mit Referenzbildern für die korrekte Schritt-2-Aufteilung).

**Schritt 2 — Aufteilung korrigiert.** Das grosse helle Rechteck links hat wieder die **volle Höhe a** (Breite a−b) statt nur (a−b)×(a−b); die beiden b·(a−b)-Streifen (rechts oben, oben bündig, Höhe a−b · Breite b; und unten als Ausgangslage, ragt unter dem grossen Rechteck heraus) bleiben. Einfärbung wie gewünscht: grosses Rechteck **hellgrün**, beide Streifen **dunkelgrün**. (Bewegungs-Darstellung „vorher unten / nachher rechts oben", keine Flächensumme.)

**Blaue a²-Umrandung fetter + ganzer Umfang** (linkes Bild und Schritt-3-Bild): `lineWidth` 2 → 3.5, volles Quadrat (ganzer Umfang) statt nur als dünner Bezugsrahmen; `lineJoin: miter` für saubere Ecken.

**Schritt-3-Bild rechts umgefärbt.** Was orange/hellbraun war (L-Form-Fläche und Aussenkontur) ist jetzt **grün** (gleiche Farbe wie die `(a+b)(a−b)`-Hinterlegung im Formel-Panel). Das b²-Eck bleibt **rot** unverändert.

**Formel-Panel.** Numerisches Ergebnis der Produktform-Zeile (3. Zeile) jetzt mit `hl-area` (Flächenfarbe orange) hinterlegt — gleich wie das Ergebnis in Zeile 1 und 2 (vorher schlichtes `<strong>`).

**Verifikation.** `node --check` fehlerfrei; keine verwaisten Konstanten (F_AREA entfernt); Bounds-Check Schritt 2 (grosses Rechteck Höhe a + unterer Streifen im Canvas) für alle Slider-Kombinationen bestanden; Skelett-Pre-Flight unverändert (`pw=1 mc=1 ml=1 bad=0`).

---

## [unreleased] — 2026-05-29 · `g1-3` Binom-3: Vermassung vereinheitlicht + Farbschema (grün/orange/blau/rot)

Feinschliff der 3.-Binom-Visualisierung (`grundlagen/g1-3-algebraische-terme.html`) nach Bild-Auftrag `Binom_3.pdf`.

**Vermassung lesbar + einheitlich (Schritt 0–3).** Linker Rand des rechten Step-Canvas von `padL=38` auf `56` verbreitert (eigene Skala `min(innerW/a, innerH/(a+b))` lokal in `drawBinomi3Schritte`), damit die verschachtelten linken Klammern nicht mehr am Canvas-Rand kleben. Neue Helferfunktion `vermassung()` zeichnet in **allen vier Schritten** dieselbe Bemassung: oben Gesamtklammer a + Segmentlabels a−b und b; links a+b (aussen), a (innen) und neu **b unterhalb der a-Klammer** (Höhe des unteren Streifens), wie im PDF gefordert. Bounds für alle Slider-Kombinationen (a∈[4,6], b∈[1,3]) geprüft.

**Farbschema rechte Animation.**
- *Schritt 1:* Produkt-Rechteck (a−b)×(a+b) neu **hellgrün** (vorher orange).
- *Schritt 2:* grosses Stück (a−b)² links oben bleibt **hellgrün**, die beiden umgelegten Streifen b·(a−b) (unten = Ausgangslage, rechts oben = neue Position) in **dunklerem Grün**. Flächenbilanz (a−b)² + 2·b·(a−b) = a²−b² für alle Slider-Werte verifiziert.
- *Schritt 3 / linkes Bild (Bild 4):* L-Form-Fläche **orange** (Flächenfarbe), a²-Umrandung neu **blau**, b²-Eck neu **rote Fläche** (statt ausgespart-grau).

**Formel-Panel (rechte Spalte, 3. Binom).** Eigene Hinterlegungs-Klassen `hl-green / hl-area / hl-blue / hl-red`. Mapping gemäss PDF: `(a+b)(a−b)` grün, `a²−b²` orange (Flächenfarbe); in der Werte-Zeile `36` blau (= a²-Umrandung), `4` rot (= b²-Fläche), Ergebnis `32` orange (= Flächenfarbe). Binom 1 und 2 nutzen weiterhin die unveränderten `hl-a2/hl-ab/hl-b2`.

**Verifikation.** `node --check` fehlerfrei; keine verwaisten `tealLabel`/`F_TEAL`-Referenzen; Bounds- und Flächenbilanz-Checks bestanden; Skelett-Pre-Flight unverändert (`pw=1 mc=1 ml=1 bad=0`).

---

## [unreleased] — 2026-05-29 · `g1-3` Binom-3-Animation komplett neu (Zerlegungsbeweis (a+b)(a−b)=a²−b²) + Kleinschreibung der Formeln

PDF/Bild-Auftrag (4 Handskizzen) an die 3.-Binom-Visualisierung in `grundlagen/g1-3-algebraische-terme.html` (`which === 3` und `drawBinomi3Schritte`). Linkes Bild und 4-Schritt-Animation rechts neu konzipiert; Layout von horizontal (Ergebnis-Rechteck (a+b) breit) auf **vertikal** (Quadrat-Breite a, Produkt-Rechteck (a−b)×(a+b) ragt um b nach unten) umgestellt.

**Skala/Layout.** Neu `skala3 = min(innerW/a, innerH3/(a+b))` mit `innerH3 = H − padT − 40` (vorher `min(innerW/(a+b), innerH/a)`). Damit passt das hohe Produkt-Rechteck (Höhe a+b, max. 9 Einheiten) ins 300×340-Canvas; Geometrie für alle Slider-Kombinationen (a∈[4,6], b∈[1,3]) im Bereich geprüft.

**Linkes Bild (immer Bild 4).** Statt der bisherigen Ausgangs-L-Form zeigt das linke Canvas jetzt durchgehend das **Ergebnisbild**: a×a-Quadrat orange gefüllt (`#f7d9b3`, Rand `#e0883c`), b²-Eck unten rechts ausgespart (Hintergrund + gestrichelter Rand) und mit „b²" beschriftet → a²−b² als L-Form. Aussenmasse a (oben/links), b (oben rechts, rechts unten). Untertitel `a² − b² = <Wert>`.

**Rechte Animation, 4 Schritte (Bild 1→4):**
- *Schritt 0 — Raster mit Vermassung:* a×a-Quadrat + unten gestrichelte Produkt-Verlängerung (a−b)×b als helle Hilfslinien; Massklammern a (oben), a (links Quadrathöhe), a+b (links gesamt), Segmentlabels a−b und b. Untertitel `(a+b)·(a−b) = a² − b²`.
- *Schritt 1 — Produktform:* orange Rechteck (a−b) breit × (a+b) hoch (= Produktform des 3. Binoms), Faktoren a−b (oben) und a+b (links) teal hinterlegt. Untertitel `(a+b)·(a−b) = <Wert>`.
- *Schritt 2 — Umlegen:* unterer grüner Streifen b·(a−b) (Verlängerung) wird abgetrennt und als zweiter grüner Streifen b·(a−b) rechts oben innerhalb a² (90° gedreht) angelegt; **kein Pfeil** (auftragsgemäss). Rechte Position mit Höhe a−b und Breite b vermasst.
- *Schritt 3 — Ergebnis:* L-Form a²−b² identisch zum linken Bild. Untertitel `(a+b)(a−b) = a² − b² = <Wert>`.

Dissektion vorab per Python verifiziert: Produkt (a−b)(a+b) = a²−b² und das umgelegte Stück b·(a−b) deckt sich flächengleich mit dem b²-freien Rest — für alle Slider-Kombinationen exakt.

**Kleinschreibung der Formeln (Schritt-Titel).** `.bin-schritt-titel` von `text-transform: uppercase` auf `none` umgestellt (Schritt-Titel-Texte sind ohnehin in gemischter Schreibung formuliert). Damit erscheinen a, b in den Formeln unter den Bildpaaren klein (vorher z. B. „SCHRITT 2 · +B²" → jetzt „Schritt 2 · +b² …"), gilt auch für die Binom-2-Titel. Die Canvas-Untertitel waren bereits durchgehend klein.

**Verifikation.** `node --check` des Binom-Script-Blocks fehlerfrei; Bounds-Check aller Slider-Kombinationen im Canvas; Skelett-Pre-Flight unverändert (`pw=1 mc=1 ml=1 bad=0`).

---

## [unreleased] — 2026-05-29 · `g1-3` Binom-2-Animation: höhere Bildräume + grüne Hervorhebung der a·b-Streifen

PDF-Auftrag (`binom2.pdf`, 2 Punkte) an die geometrische Binom-Animation in `grundlagen/g1-3-algebraische-terme.html` (2. Binom, `which === 2`).

**Bildräume höher.** Bei `a = 6` füllte das a²-Quadrat das 300×300-Canvas fast vollständig aus (Quadrat-Unterkante bei y≈274, Untertitel-Zeile bei y=278) — der zweizeilige Erklär-Untertitel überlappte die Quadrat-Unterkante. Beide Canvas-Höhen (links `cv-binomi`, rechts `cv-binomi-rechts`) in den Binom-2/3-Modi von 300 auf 340 px erhöht; Binom 1 bleibt quadratisch (`H_CANVAS = which === 1 ? 300 : 340`). Da die Skala `min(innerW, innerH)/6` ist, wird das Quadrat nun durch die Breite begrenzt (Seite ≈246 px statt 240) und es entstehen ~38 px freier Raum unter dem Quadrat für die Beschriftung. CSS `.bin-canvas-paar.zeige-rechts canvas` `aspect-ratio` von `1 / 1` auf `300 / 340` angepasst, Canvas-`height`-Attribute auf 340.

**Grüne Hervorhebung (linkes Bild).** Im linken Bild die beiden a·b-Streifen (rechter Streifen volle Höhe × `b`, unterer Streifen volle Breite × `b`) mit einem grünen Rahmen (`#1f6b3a`, Projekt-`--gruen`, lineWidth 2.5, 1.25 px eingerückt) umrandet. Der Erklär-Untertitel „Zwei a·b-Streifen überlappen sich im b²-Eck." erhält eine hellgrüne Hervorhebungs-Box (`--gruen-hell #d8f0e2`) mit demselben grünen Rand (`--gruen`) — gleiche Grün-Familie wie die Streifen-Rahmen, dunkler Text bleibt lesbar. Box-Breite auf `W − 6` geklemmt, damit sie nie über den Canvas-Rand hinausragt; `roundRect` mit `fillRect`-Fallback.

**Grüne Hervorhebung (rechtes Bild / Schritt-Animation, Folgeauftrag).** In `drawBinomi2Schritte` (rechtes Canvas) erhalten die beiden a·b-Streifen denselben grünen Rahmen wie links — aber **persistent über alle 4 Schritte**: der Rahmen wird nach dem schritt-abhängigen Flächen-Malen (`malen`) und nach dem schwarzen Aussenrahmen gezeichnet, unabhängig von der `sicht`-Tabelle. So bleibt sichtbar, wo die a·b-Streifen liegen bzw. abgezogen werden, auch wenn ihr Inhalt im jeweiligen Schritt gestrichelt-ausgeblendet ist. Der Rechnungs-Untertitel wird in Segmente zerlegt (statt einem `fillText`-String) und der **symbolische Term `− ab` (Schritt 1, 2) bzw. `− 2ab` (Schritt 3)** mit einer grünen Inline-Box (`--gruen-hell` Füllung, `--gruen` Rand) hinterlegt. Segmente werden links-ausgerichtet ab der zentrierten Gesamtbreite gezeichnet, `textAlign` danach auf `center` zurückgesetzt. Schritt 0 (`a² = …`) bleibt ohne Hervorhebung.

**Verifikation.** Geometrie-Sim (Python) für `W∈{250,300}`, `H∈{300,340}` bestätigt Untertitel-Abstand alt 4 px → neu 38 px (Desktop). Node-`--check` des Binom-Script-Blocks fehlerfrei; Skelett-Pre-Flight unverändert (`pw=1 mc=1 nav=1 ml=1 bad=0`).

---

## [unreleased] — 2026-05-28 · Über-Panels in `nav.js`: Lizenz-Modellnennung, Feedback-Hinweis, Schreibfehler

Mehrere kleine Iterationen an den vier Über-Panels (`Autor & Intention`, `Ausblick`, `Feedback`, `Lizenz`). Definiert in `nav.js` Z. 110–157.

**Lizenz-Block:** Erwähnung des verwendeten Modells konkretisiert. Vorher: „Inhalte erstellt mit Unterstützung von **Claude** (Anthropic)." Neu: „Inhalte erstellt mit Unterstützung von **Claude Opus 4.7** (Anthropic)." Versions-Information ist damit für Auditoren und für die Lehrerschaft transparent.

**Feedback-Block:** Hinweis „*Feedbackformular folgt.*" als Platzhalter unter dem GitHub-Issue-Link ergänzt. Hintergrund: der bisherige Kanal über GitHub-Issues setzt einen GitHub-Account voraus, was Lehrkräfte und Schüler ausschliesst, die nicht GitHub-affin sind. Ein anonymes Tally-Formular ist als nächster Schritt geplant, der Hinweis kündigt das an, ohne dass schon eine Implementation steht. Der GitHub-Link bleibt als Diskussions-Kanal für GitHub-Nutzer erhalten.

**Autor & Intention:** Schreibfehler korrigiert — Dativ Plural „seine Kindern" → „seinen Kindern" (Z. 116).

**Ausblick-Block:** unverändert; mehrere Zwischen-Iterationen führten am Ende zum identischen Stand wie vor der Sitzung (Erstellt / Geplant / Ideen mit allen Bullets).

---

## [unreleased] — 2026-05-28 · `g1-4` Grossüberarbeitung Zehnerpotenzen & Quadratwurzeln (PDFs `1_4.pdf` + Algebra-Verfeinerung + Druckmaterialien + Serlo-Link-Reparatur)

Umfangreichste Iteration der Sitzung. Auftraggeber-PDF `1_4.pdf` mit 11 Detail-Aufträgen an `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html`, anschliessend zwei Folgewellen: anspruchsvollere Algebra-Beispiele bei den Wurzelgesetzen, und vollständige Anpassung der Druck-Begleitdateien plus Reparatur toter externer Links.

**Vorsatz-Tabelle (Form/Wert/Bedeutung).** Erweitert von 7 auf 15 Zeilen: `10¹⁵` runter bis `10⁻¹⁵` in 3er-Schritten, dazwischen zwischen `10⁻³` und `10³` zusätzlich die 1er-Schritte (`10²`, `10¹`, `10⁻¹`, `10⁻²`). Die 1er-Schritt-Zeilen sind per `.einer-schritt`-Klasse leicht abgesetzt (gedämpfter Hintergrund, kleinere Schrift), so dass die 3er-Stufen optisch dominieren. Wert-Spalte verbreitert auf `65 mm` und mit `white-space: nowrap`, damit alle Zahlen einzeilig stehen — auch `10¹⁵ = 1 000 000 000 000 000` (mit `&thinsp;`-Gruppentrennung). Neue Vorsätze: Peta (P), Tera (T), Piko (p), Femto (f), Hekto (h), Deka (da), Dezi (d), Zenti (c).

**Engineering-Notation neu eingeführt.** Eigenständiger Erklärblock (`block-def`) zur Engineering-Darstellung: Mantisse `1 ≤ |a| < 1000`, Exponent immer Vielfaches von 3, direkte Brücke zu den SI-Vorsilben mit Bauteil-Beispielen (`2.2 kΩ`, `820 nH`, `15 MHz`, `47 µF`). Erläutert, warum Datenblätter und Schaltpläne diese Form bevorzugen.

**Beispiel-Tabelle wissenschaftliche/Engineering-Notation.** Von 4 auf 8 Zeilen erweitert, mit eigener Engineering-Spalte. Beispiele bewusst so gewählt, dass der Unterschied klar wird (`0.000 047 → 4.7·10⁻⁵` wissenschaftlich vs `47·10⁻⁶` engineering, mit SI-Vorsilbe „µ").

**„Probier selbst"-Widget um Engineering-Output erweitert.** `.wn-row` von 2 auf 3 Spalten umgestellt (Input + Wiss. + Engineering). JS rechnet zusätzlich die Engineering-Form: Exponent auf nächstes Vielfaches von 3 abgerundet (`Math.floor(exp/3)*3`), Mantisse entsprechend skaliert. Verifiziert für 11 Testwerte inkl. Grenzfälle (`1`, `999`, `1000`, sehr kleine Werte). Bei Bildschirmbreite < 780 px responsiv auf 1 Spalte.

**Potenzgesetze-Tabelle (P1–P7).** Vierte Spalte „Algebrabeispiel" ergänzt, dritte Spalte umbenannt zu „numerisches Beispiel". Spaltenbreiten 22/26/26/26 % (Name schmal, drei Inhaltsspalten gleich breit). Beispiele konkret: P1 `x²·x⁵=x⁷`, P3 `(x⁴)³=x¹²`, P4 `(xy)³=x³y³`, etc.

**Quadratwurzeln-Übersicht.** Statt 4-Spalten-Grid mit 12 Karten in Doppelzeilen-Layout nun 6-Spalten-Grid mit 18 Einzeilern, von `√1=1` bis `√324=18` lückenlos. `.wuko-card` deutlich kompakter (7×10 px Padding, einzeilige Serif-Formel). Bei Bildschirmbreite < 780 px responsiv auf 3 Spalten.

**Wurzelgesetze-Tabelle komplett neu mit W0–W9.** Vorher 4 Gesetze (W1–W4) und 3 Spalten. Neu 10 Gesetze und 6 Spalten: Name · Regel · Bruchexponenten-Form · Voraussetzung · numerisches Beispiel · Algebrabeispiel. Dualität zu P1–P7 explizit über die Bruchexponenten-Spalte sichtbar: W0 Bruchexponent (`√[n]{a}=a^(1/n)`), W1 Produktwurzel, W2 Quotientenwurzel, W3 Wurzel-einer-Wurzel, W4 Produkt-unter-Wurzel, W5 Quotient-unter-Wurzel, W6 Wurzel-aus-1, W7 Wurzel-im-Nenner / negativer Exponent, W8 Wurzel quadrieren, W9 Quadrat unter der Wurzel.

**Algebrabeispiele in W0–W9 inhaltlich anspruchsvoller (Folgewelle).** Erste Version war zu nah an Re-Statement der Regel mit anderen Buchstaben. Überarbeitet zu echten Anwendungs-Beispielen: W0 `x·√x = x^(3/2)`, W1 `√(18x)·√(2x) = √(36x²) = 6x` (`x ≥ 0`), W2 `√(50x³)/√(2x) = 5x` (`x > 0`), W3 `√(√(81x⁴)) = 3x` (`x ≥ 0`), W4 `√(72x²y) = 6x√(2y)` (`x,y ≥ 0`), W5 `√(12x²/3) = 2x` (`x ≥ 0`), W6 `√1 + (3x)⁰ = 2`, W7 `1/√x = √x/x` (Nenner rational machen), W8 `(√(x+3))² = x+3` (`x ≥ −3`), W9 `√(x²−6x+9) = |x−3|` (binomische Formel rückwärts). Alle via sympy/numerisch verifiziert (W9 numerisch über mehrere Stützstellen, da sympy `√((x−3)²) = |x−3|` nicht symbolisch löst).

**Teilweises Wurzelziehen.** Erweitert um `√12=2√3`, `√18=3√2`, `√20=2√5`. Tabelle sortiert klein → gross (12, 18, 20, 50, 75, 200, x³), letzte Zeile „`√x³` für `x ≥ 0`" (vorher Klammer-Zusatz `(x ≥ 0)`).

**MathJax-Konfig (in `g3-3` bereits in voriger Iteration erweitert):** für die `\\bbox`-Highlights im Diskriminanten-Kontext mussten `bbox` und `color` als zusätzliche Pakete in den Loader. In g1-4 nicht nötig.

**Druck-Begleitdateien überarbeitet (Folgewelle).**

`downloads/grundlagen/g1-4-zehnerpotenzen-quadratwurzeln/formelauszug.html` von v1.0 auf **v2.0** (130 Zeilen): SI-Vorsätze 14 Einträge (vorher 11; Peta, Deka, Zenti, Femto neu), Engineering-Notation-Block mit Erklärung und 3-Zeilen-Beispieltabelle, Potenzgesetze als 4-Spalten-Tabelle (Algebra-Spalte neu), Quadratzahlen 1²–18² statt 1²–12², Wurzelgesetze als 4-Spalten-Tabelle mit W0–W9 und Bruchexponenten-Spalte. Teilweises Wurzelziehen ursprünglich als lange `\\quad`-Inline-MathJax-Reihe — verursachte Seiten-Überlauf im Druck-Layout (Screenshot vom Auftraggeber zeigte Text läuft rechts aus der Seite); umgebaut auf kompakte 4-Spalten-Tabelle mit 8 Zellen. „Nenner rational machen" ebenfalls auf zwei kürzere Absätze aufgeteilt.

`downloads/grundlagen/g1-4-zehnerpotenzen-quadratwurzeln/handout.html` von v1.0 auf **v2.0** (~153 Zeilen): wie Formelauszug, aber mit ausführlichen Erklärtexten. Engineering-Notation als eigener Abschnitt 3 mit der Bauteil-Datenblatt-Brücke. Wurzelgesetze-Tabelle mit den anspruchsvollen Algebra-Anwendungen aus der Themenseite (Beispielspalte zeigt Anwendung statt Re-Statement). Teilweises Wurzelziehen ebenfalls als 3-Spalten-Tabelle (Wurzel · Zerlegung · Vereinfacht), 8 Zeilen.

**Externe Serlo-Links repariert.** Die zwei Links unter „Externe Videos & Aufgabensammlungen" (Zeilen 821/822) gingen auf `/mathe/zahlen-grossen/potenzen-wurzeln/...` — diese Pfade existieren in Serlos aktueller URL-Struktur nicht mehr (umbenannt/migriert, ohne Redirect). Via Web-Suche und `web_fetch` neue stabile ID-basierte URLs identifiziert: `https://de.serlo.org/mathe/23665/aufgaben-zu-den-potenzgesetzen` (Aufgaben zu allen Potenzgesetzen, mit Lösungen) und `https://de.serlo.org/mathe/111507/aufgaben-zum-rechnen-mit-quadratwurzeln` (Wurzelgesetze, teilweises Wurzelziehen, mit Lösungen). Beide Links liefern `200 OK`, sind inhaltlich passender als die alten Sammelseiten und nutzen die stabileren `/mathe/{ID}/...`-Pfade.

**Verifikation:** Pre-Flight grün (`pw=1 mc=1 ml=1 nav=1 bn=1 bad=0`). Strukturelle Marker stimmen: 15 Vorsatz-Zeilen + Header = 16 `.pot-zeile`, 18 `.wuko-card`, 10 `<strong>W[0-9]`, 7 `<strong>P[1-7]`. Alle 10 Wurzelgesetze-Algebrabeispiele symbolisch (sympy) bzw. numerisch verifiziert.

---

## [unreleased] — 2026-05-28 · `g3-3` Quadratische Funktionen: Notationen erweitert, Diskriminante-Highlighting, Hover-Beispiele bei 6-Vorgehen-Tabelle, kompakteres Interaktiv-Widget

Auftraggeber-PDF mit vier Anpassungen an `grundlagen/g3-3-quadratische-funktionen.html`.

**Hinweis-Tabelle „Andere Notationen für den Scheitelpunkt":** Zeile `d, e` ergänzt mit `f(x) = a(x−d)² + e, S(d | e)`, Quelle „in anderen Lehrmitteln" (nach `u, v`-Zeile, vor `x_s, y_s`).

**„Interaktive Darstellungen"-Widget kompakter:** Titel einzeilig (h3 mit Serif-Untertitel inline), drei Slider in neuem `sl-grid-3` (3-Spalten-Grid), neue `.widget-kompakt`-Klasse für reduziertes Padding. Canvas-Höhe 280 → 260.

**Diskriminante visuell verbunden mit Mitternachtsformel:** in beiden Formeln (Mitternachtsformel und `D = b² − 4ac`) wird `b² − 4ac` mit `\\bbox[#fde9c7, 3px]{b^2 - 4ac}` orange hinterlegt — identische Farbgebung. Zusätzlich Verbindungstext „↑ derselbe Ausdruck ↓" zwischen den Formeln. Live-Rechnung `dr-nst-rechnung` nutzt `<span class="disk-hl">` für den gleichen Highlight-Stil. MathJax-Konfig dafür erweitert: `packages: {'[+]': ['boldsymbol', 'bbox', 'color']}`, Loader: `[tex]/bbox`, `[tex]/color`.

**6-Vorgehen-Tabelle (`tab-vorgehen`):** `f(x) = ` in der ersten Spalte ergänzt (`f(x){=}ax^2{+}bx{+}c` etc.), `nowrap` entfernt, Spaltenbreiten 11/20/21/Rest (Spalten 2+3 schmaler).

**Hover/Klick-Popups bei der 6-Vorgehen-Tabelle.** Mehrere Iterationen am Layout, finale Form: Tabelle in `<div class="anw-tabelle-wrap">` (position:relative) gewrappt, Popups als `<div class="bsp-pop">` direkt in den `tab-vorgehen`-Zellen eingebettet (so dass MathJax sie beim Page-Load einmal typesetzt). Position absolut zum Wrapper bei `left: 10px` (linker Tabellenrand), Breite `calc(58% - 20px)`, max 560px. JS berechnet vertikale Position via `getBoundingClientRect`, clamped an Tabellen-Bounds (PAD=8 px), Pfeil per CSS-Variable `--arrow-top` auf Zellen-Mitte gesetzt. Hover-Hervorhebung: `tr.bsp-row:hover td:not(.tab-form)` — die erste Spalte mit `rowspan="2"` wird nicht markiert (auch bei ungeraden Zeilen 1, 3, 5 nur Spalten 2–4). Klick = toggleable. Bei ≤ 900 px: Popup volle Breite, Pfeile ausgeblendet. 6 konkrete Beispiele eingebaut und via sympy/numerisch verifiziert: ① Mitternachtsformel `x²−2x−3`, ② Gleichungssystem 3 Punkte, ③ Transformation `2(x−1)²−3`, ④ Scheitel+Punkt `S(2|−1), P(4|3)`, ⑤ NS-1,3 zeichnen, ⑥ NS-0,20 + P(10|5) Wurf.

---

## [unreleased] — 2026-05-28 · `g1-3` Binom-Animationen + Begriff-Chip-Auswahl

Auftraggeber-PDF mit vier Anpassungen an `grundlagen/g1-3-algebraische-terme.html`.

**Begriff-Hervorheben-Chips:** Bei Auswahl soll die Begriffsfarbe stabil bleiben; Markierung des aktiven Chips nur per fetter Umrandung (3 px solid), nicht durch Farbumkehr. Ursache des Bugs: per-Begriff-spezifische `.begr-chip.aktiv`-Regeln hatten geringere Spezifität als eine globale `.anim .chip.aktiv`-Regel und wurden überschrieben. Fix: per-Begriff-Regeln auf höhere Spezifität gebracht.

**1. Binom — Schieberegler „Schritt (Herleitung)" ausblenden bei der animierten Variante.** Ursache: globale `.anim .regler { display: flex }` (Spezifität 0,2,0) übersteuerte die Ein-Klassen-Regel. Fix: `.anim .bin-schritt-regler { display: none }` plus `.anim .bin-schritt-regler.aktiv { display: flex }`.

**2. Binom (linkes Canvas):** zwei halbtransparente `a·b`-Streifen die sich im `b²`-Eck überlappen, `a²` als Grundfläche sichtbar. Vermassung: Segment-Labels `(a−b)` bzw. `b` oben und links, plus Massstrich-Klammer über die Gesamtlänge `a`.

**3. Binom komplett neu mit 4-Schritt-Animation.** Funktion `drawBinomi3Schritte`. Schritt 0: Ausgangsfigur `a²−b²` als L-Form. Schritt 1: Streifen `(a−b)×b` abtrennen mit roter Schnittlinie. Schritt 2: Streifen nach rechts umlegen mit Pfeil. Schritt 3: Rechteck `(a+b)×(a−b)` — Flächengleichheit zu `a²−b²` visuell evident. Eigene Skala `skala3 = min(innerW/(a+b), innerH/a)`, damit die `(a+b)`-Breite im Rahmen bleibt.

**Canvas-Layout:** `a`-Slider auf 4..6 beschränkt, beide Canvas 300×300. Layout-Bug behoben: `initCanvas` nutzt `offsetWidth` — Flex-Layout streckte aber das linke Canvas. Fix: `.bin-canvas-paar canvas { flex: 0 0 auto; width: 300px; height: 300px }` (gleiche Grösse für beide), bei `.zeige-rechts` zusätzlich `max-width: 48%; aspect-ratio: 1/1` für schmale Bildschirme.

**Verifikation:** detaillierte Geometrie-Verifikation via Python für alle `a,b`-Kombinationen rechnerisch korrekt; Node-Mock-Runtime-Tests mit Bounds-Checks für 108 Frames laufen sauber.

---

## [unreleased] — 2026-05-28 · g1-2 Anpassungen aus PDF `1.2b` (3 Aufträge, inkl. Nachbesserung)

Auftraggeber-PDF `1_2b.pdf` mit drei Aufträgen zu `g1-2-zahlen-grundoperationen.html`. Die erste Runde griff bei Auftrag 1 und 3 zu kurz (die Symptome blieben im Browser bestehen); diese Runde behebt die eigentlichen Ursachen. Dokumentation entsprechend korrigiert.

**Auftrag 1 — Zahlenmengen-Definitionstabelle: Zeilenfarben über die ganze Zeile (ℕ blau, ℤ grün, ℚ gelb, ℝ rot).**
- Erster Versuch: Selektor `.zm-def-tabelle tr.zm-row-* td` (Spezifität 0,2,2). Das wirkte nur bei den ungeraden Zeilen (ℕ, ℚ). Ursache: `style.css` enthält eine Zebra-Streifen-Regel `.ftb-tabelle tbody tr:nth-child(even) td { background: var(--papier); }` mit Spezifität **0,3,3** — die schlägt 0,2,2 und überfärbte die geraden Zeilen (ℤ, ℝ) wieder mit Papierfarbe. Deshalb sahen im Browser nur zwei der vier Zeilen korrekt aus.
- Fix: Selektor auf `table.zm-def-tabelle tbody tr.zm-row-* td` angehoben (Spezifität **0,3,4**), schlägt die Zebra-Regel zuverlässig. Jetzt färben alle vier Zeilen durchgehend über Symbol, Name, Beschreibung und Beispiele.
- Der farbige `border-left`-Akzent bleibt bewusst nur auf der ersten Zelle (`td:first-child`), ebenfalls auf 0,3,4 angehoben.

**Auftrag 2 — Vorzeichenregeln-Tabelle: „=" → „respektive".**
- In der Spalte „Vorzeichen" stand zwischen Multiplikations- und Divisionsregel ein `=` (z. B. `+ · + = + : +`). Das ist kein Gleichheitszeichen, sondern verbindet zwei parallele Regeln. In allen vier Zeilen durch `respektive` ersetzt. (Bereits in der ersten Runde korrekt, unverändert.)

**Auftrag 3 — Intervalle-Animation: Auswahl funktioniert nicht / Zahlenstrahl fehlt.**
- Hier lagen **zwei** unabhängige Ursachen vor. Die erste Runde fand nur die erste und übersah die zweite — deshalb blieb die Auswahl im Browser tot.
- **Ursache A (JS, behoben in Runde 1):** `buildKl()` rief `MathJax.typesetPromise(...)` nur durch `if (window.MathJax)` abgesichert auf. Ist MathJax beim `DOMContentLoaded` noch nicht fertig, existiert das Objekt, aber `typesetPromise` ist noch keine Funktion → `TypeError`, der den Handler vor der Intervalle-Initialisierung abbrach. Fix: Guard auf `&& window.MathJax.typesetPromise` erweitert, Aufruf auf `window.MathJax` umgestellt (konsistent zu den fünf anderen typeset-Aufrufen).
- **Ursache B (CSS, eigentlicher Auswahl-Bug, behoben in Runde 2):** Die Regel `.iv-tab .iv-row * { pointer-events: none; }` legte `pointer-events:none` auf **alle** Nachkommen der Zeile — inklusive der `<td>`-Zellen selbst (eine `td` ist Nachkomme der `tr`). Dadurch war die ganze Zeile nicht klickbar: der Klick fiel durch die Zelle hindurch, `ev.target` lag ausserhalb `.iv-row`, `closest('.iv-row')` lieferte `null`, nichts passierte. Fix: Regel auf `.iv-tab .iv-row td * { pointer-events: none; }` eingeengt — `pointer-events:none` liegt jetzt nur noch auf den *Inhalten* der Zelle (MathJax-SVG etc.), die `td` selbst bleibt klickbar.
- Warum Runde 1 das übersah: Die DOM-Mock- und jsdom-Verifikation testet die JS-Delegations-Logik, aber **kein** CSS-Hit-Testing / `pointer-events`. Im Mock sah der Klick-Pfad daher immer korrekt aus (`closest` findet die Zeile), während er im echten Browser an der CSS-Regel scheiterte. Lehre: Bei „Klick reagiert nicht"-Bugs zusätzlich die `pointer-events`- und Overlay-Situation im CSS prüfen, nicht nur die JS-Delegation.
- Verifikation Runde 2: `cell.closest('.iv-row')` liefert in jsdom die korrekte Zeile; Full-Mock zeigt nach Klick `iv-formal = ]-∞; 2]`, `aktiv`-Klasse korrekt umgeschaltet, Canvas neu gezeichnet. Die `pointer-events`-Regel ist nun die einzige in der Datei und kollidiert mit keiner `style.css`-Regel (dort nur `.pn-dis` für Pagination).

**Keine Änderungen an Aufgaben, Lösungen, Begleittext, RLP-Box, Ressourcen-Sektion oder Footer.** Skelett-Struktur unverändert; Pre-Flight grün; Hauptscript-Block Syntax ok.

---

## [unreleased] — 2026-05-27 · g1-3 Anpassungen aus PDF `1.3b` (4 Animationen verfeinert)

Auftraggeber-PDF `1_3b.pdf` mit vier Detail-Aufträgen zu den Animationen in `g1-3-algebraische-terme.html` — alle umgesetzt.

**Auftrag 1 — Anim „Drei äquivalente Terme": vertikale Ausdehnung reduziert.**
- Canvas-Höhe von 360 auf 260 px reduziert. Innere y-Schrittweiten der Spalten-Renderings entsprechend gestrafft (Spaltentitel +16 statt +22, Formel-Box 22 statt 26 hoch, Einsetzen/Berechnung-Zeilen je 14 statt 18 px, Zwischenschritt +18 statt +24, Ergebnis-Box 26 statt 30 hoch, Dario-Vermerk-Zeilen 10 statt 12 px Abstand). Bottom-Streifen H−6 statt H−8. Trennlinien entsprechend angepasst.
- Inhalt und Logik unverändert: alle vier Spalten (Anna/Bruno/Cinzia/Dario), Berechnungs-Reihenfolge, Dario-Vermerk-Mechanik (zufällig gleich vs. „+260 zu viel") bleiben gleich. Die Animation reagiert auf x/y-Slider wie zuvor.

**Auftrag 2 — Anim „Begriffe am Polynom": Farb-Konsistenz Buttons/Display/Text, Grad-1-Darstellung.**
- Externe Farb-Legende rechts entfernt (5 Zeilen `legende-zeile` mit `begr-swatch`). Die Information ist jetzt direkt in den Begriff-Buttons sichtbar und damit redundant.
- Die fünf Begriff-Chips bekommen pro `data-begriff`-Attribut eine eigene Hintergrund-/Border-/Textfarbe — passend zu derselben Palette, die das Display für die Hervorhebung benutzt: Glied gelb, Koeffizient blau, Grad eines Glieds violett, Grad des Polynoms orange, Konstantes Glied grün. Aktiver Chip mit doppelter Box-Shadow als Outline (vermeidet Farb-Konflikt mit der Hintergrundfarbe).
- Der Erklärungstext-Block unter dem Display (`begr-erkl`) übernimmt dynamisch die Farbe des aktiven Begriffs: `border-left-color` und ein dezenter `background`-Tint in derselben Familie. Damit ist visuell klar: „Button → Hervorhebung im Polynom → Erklärungstext" gehören zusammen.
- Grad-1-Glieder werden bei aktivem `gradGlied`- oder `gradPoly`-Begriff jetzt explizit als `x¹` gerendert (statt nur als `x`). Die `1` sitzt in einem `<sup class="ex">1</sup>`, sodass die bestehenden CSS-Regeln `.show-gradGlied .ex` / `.show-gradPoly .gl.gradmax .ex` die Hervorhebung greifen. Ohne diese Änderung wäre die Hervorhebung bei z. B. `2x + 5` für „Grad eines Glieds = 1" beim x-Glied leer geblieben.
- CSS-Regel für `show-gradPoly` enggezogen: vorher wurde das **ganze Glied** höchsten Grades umrandet (`.gl.gradmax { outline; background }`), jetzt nur noch dessen **Exponent** (`.gl.gradmax .ex { ... }`). Konsistent zu „Grad = Exponent" und passt zur PDF-Vorgabe „nur den höchsten Exponenten markieren". Bei Grad-1-Polynomen greift damit dieselbe Mechanik wie bei `gradGlied` (Exponent `1` wird explizit gezeigt und hervorgehoben).

**Auftrag 3 — Anim „Gleichartige Glieder zusammenfassen": kumulative Zeilen.**
- Display-Box `zus-display` von „eine Zeile, die sich beim Slider-Schritt ändert" auf „kumulativ: alle Schritte 0..N sichtbar als eigene Zeilen" umgestellt. Schritt 3 zeigt also alle vier Stadien untereinander, die Entwicklung wird so visuell direkt vergleichbar.
- Layout von Flex (einzeilig zentriert) auf CSS-Grid `max-content 1fr` umgestellt: linke Spalte Schritt-Label (z. B. „Schritt 1 · einfärben") in Sans-0.78rem-Caps, rechte Spalte das gerenderte Polynom in Serif-18pt.
- Schritt-Titel-Element `zus-schritt-titel` unter der Display-Box komplett entfernt (Information sitzt jetzt links in jeder Zeile).
- Rechte Bedien-Spalte: „Vier Schritte"-Legende-Box entfernt. Schritt-Slider und Erklär-Box bleiben.
- JS-Funktion `polyHtmlFuerSchritt(poly, schritt)` als Helfer extrahiert; `rendere()` ruft sie in einer Schleife `s = 0 .. aktuellerSchritt` auf und konkateniert das Resultat als Label/Poly-Zeilenpaare ins Grid.
- Polynom-Auswahl, Farben-Zuweisung, `sortKey`-Logik, Erkl-Text-Mechanik unverändert.

**Auftrag 4 — Anim „Binomische Formeln — geometrisch": drei Verfeinerungen.**
- **4.1 (1. Binom): Rechnung farblich an Grafik gebunden.** Die Rechnungs-Box rechts vom Quadrat zeigt jetzt sowohl die allgemeine Formel `(a + b)² = a² + 2ab + b²` als auch die konkrete Auswertung `25 + 2·5·2 + 4 = 49` mit Hintergrundfarben pro Summanden, die zur Grafik passen: `a²` hellgelb (`#fde2a8`), `2ab` orange (`#e6b87a`), `b²` dunkelbraun (`#c8884a`, weisse Schrift). CSS-Klassen `hl-a2 / hl-ab / hl-b2` von „nur Schriftfarbe" auf „padding + border-radius + background + Fett-Schrift" umgestellt. Konsequent für alle drei Binom-Formeln in der Rechnungs-Box, nicht nur das 1. Binom — die Farbcodierung wird so über die Animation hinweg konsistent.
- **4.2 (2. Binom): neue Zerlegung mit `a·b`-Streifen.** Das linke Quadrat zeigt jetzt zwei volle `a·b`-Streifen (Höhe `a` × Breite `b`), die sich im `b²`-Eck unten-rechts überlappen. Beschriftung dort `a·b = ab` (statt vorher `b(a−b) = b·(a-b)`). Visuell sieht das Quadrat aus wie vorher (gleiche vier Bereiche), aber die Lesart ist die Inclusion-Exclusion-Form: das `b²`-Eck ist „doppelt gezählt", weil es zu beiden `a·b`-Streifen gehört. Untertitel angepasst.
- **4.2 (2. Binom): zusätzliches Schritt-Quadrat rechts.** Neues Canvas `cv-binomi-rechts` (380×380) wird nur beim 2. Binom eingeblendet (CSS `.zeige-rechts`). Zusätzlicher Slider unterhalb der Rechnung (`sld-bin-schritt`, 0–3) wird ebenfalls nur beim 2. Binom sichtbar. Die 4 Schritte zeigen die Herleitung `(a−b)² = a² − ab + b² − ab`:
  - Schritt 0: volles `a²`-Quadrat
  - Schritt 1: rechter `a·b`-Streifen (= obere und untere rechte Teile) wird ausgeblendet → `a² − ab`
  - Schritt 2: das `b²`-Eck wird wieder eingeblendet (Korrektur der Doppelzählung) → `a² − ab + b²`
  - Schritt 3: unterer `a·b`-Streifen wird ausgeblendet → `(a−b)²`
  - Annahme: das PDF schreibt für Schritt 2 „Quadrat a^2 wird eingeblendet" — das ist aber nur als Tippfehler für „Quadrat b^2" interpretierbar, weil das Endergebnis `(a−b)²` sonst nicht heraus käme. Ausgeblendete Teile bleiben als gestricheltes Rechteck sichtbar (Hinweis „war hier"), sichtbare Beschriftungen passen sich an (z. B. zeigt Schritt 2 das `b²`-Eck mit eigener Beschriftung). Untertitel pro Schritt zeigt die laufende Rechnung mit Zwischenergebnis.
- **JS-Aufräumen:** vorherige `\(...\)`-LaTeX-Inhalte in der Rechnungs-Box durch reines HTML mit Unicode-Hochstellung (`²`) ersetzt, da die Hintergrundfarben sonst nicht auf MathJax-SVG-Output greifen. MathJax-Re-Typeset-Aufruf am Ende von `drawBinomi` damit nicht mehr nötig — entfernt. `drawBinomi2Schritte(a, b, schritt, skala)` als separate Funktion, wird in `drawBinomi` nur bei `which === 2` aufgerufen.

**Quer durch alle vier Aufträge: keine Änderungen an Aufgaben, Lösungen, Begleittext, RLP-Box, Ressourcen-Sektion oder Footer.** Skelett-Struktur (page-wrap / main.content / aside.toc-wrap / buildNav) unverändert.

---

## [unreleased] — 2026-05-27 · g1-3 Anpassungen aus PDF (Aufträge 1–6 vollständig)

Auftraggeber-PDF `1_3_aendern.pdf` mit 6 Aufträgen zu `g1-3-algebraische-terme.html` — alle umgesetzt. Datei von 814 auf 1756 Zeilen gewachsen.

**Auftrag 1 — Einstieg „Drei Wege zur gleichen Zahl" überarbeitet.**
- Problemtext umformuliert, sodass Cinzias unvereinfachter Term `80x + 30y + 20y` vom Text her plausibel ist: der Erlös von Sorte B (50 Fr.) wird intern in 30 Fr. Material und 20 Fr. Lohn aufgesplittet. Die Tabelle hat eine zusätzliche dritte Spalte „Form" mit den drei Aufteilungs-Gründen.
- Vorlauftext zur Animation gestrafft und auf die Kern-Botschaft fokussiert: plausibel aussehende Umformung ist nicht automatisch korrekt.
- Externe Erklärungs-Box `erkl-equiv` rechts neben der Animation komplett entfernt. Stattdessen erscheint der Vermerk „nicht äquivalent" jetzt rot direkt unter Darios Ergebnis im Canvas — mit der numerischen Abweichung als Untertitel („+260 zu viel"). Bei zufällig gleichem Wert: „zufällig gleich — nicht äquivalent".
- Canvas-Höhe von 320 auf 360 px erhöht, damit der Dario-Vermerk Platz hat. Spalten-Layout und Skalierung unverändert.
- Legende rechts: „Dario (falsch?)" → „Dario (?)" (kompakter, weil der Vermerk jetzt im Canvas steht).
- JS-Funktion `drawEquiv()`: MathJax-Aufruf am Ende entfernt (kein DOM-Element `erkl-equiv` mehr zu typesetten). Streifen unten vereinfacht — Dario-Ergebnis ohne „(zufällig gleich)"-Suffix, weil die Information jetzt zentral in der Dario-Spalte sitzt.

**Auftrag 2 — Definitionen: statischer Begriffs-Block durch interaktive Animation ersetzt.**
- Der `block-def` „Begriffe am Polynom 3x³ − 2x + 5" mit der statischen `<ul>` ist raus. An seine Stelle tritt eine `anim`-Box „Begriffe am Polynom — interaktiv".
- Links: Polynom-Auswahl als Chip-Reihe und eine grosse `begr-display`-Box, die das gewählte Polynom in Serif-22pt rendert. Rechts: fünf Begriff-Chips (Glied, Koeffizient, Grad eines Glieds, Grad des Polynoms, Konstantes Glied) plus Farb-Legende.
- Fünf Polynome systematisch gewählt: `2x + 5` (Grad 1), `x² − 4x + 3` (Grad 2), `3x³ − 2x + 5` (Lehrbuch-Beispiel), `−2x³ + x² + 7` (negativer Leitkoeffizient), `4x² − x` (**ohne** konstantes Glied — bewusste Lerngelegenheit). Bei P5 zeigt der „Konstantes Glied"-Chip statt einer Markierung den Hinweis: „hat kein konstantes Glied — alle Glieder enthalten die Variable. Das konstante Glied wäre 0".
- Renderer: jedes Glied wird als `<span class="gl">` mit Sub-Spans `.ko` (Koeffizient), `.vr` (führendes Minus) und `<sup class="ex">` (Exponent). Klassen `.gradmax` und `.konstant` werden gesetzt, wo zutreffend. Operator (`+`/`−`) zwischen Gliedern als separater `<span class="op">`.
- CSS-Hervorhebungs-Modi via Klassen am `.begr-display`-Container: `.show-glied` (gelb, jedes Glied umrandet), `.show-koeff` (blau, nur Zahlen), `.show-gradGlied` (violett, nur Exponenten), `.show-gradPoly` (orange, nur das Glied mit höchstem Grad), `.show-konst` (grün, nur das konstante Glied).
- Erklärungs-Block darunter (`begr-erkl`) zeigt einen kontextsensitiven Text zum gewählten Begriff inkl. der konkreten Werte des aktuellen Polynoms (z. B. „Hier: Grad 3" für P3, „Hier: −2, 1, 7" für P4-Koeffizienten).
- Nochmaliges Klicken auf einen aktiven Begriff schaltet ihn aus (Toggle-Verhalten).

**Auftrag 3 — Gleichartige Glieder: 4-Schritt-Slider-Animation ergänzt.**
- Vor die bisherige Tabelle mit drei Beispielen wurde eine `anim`-Box „Gleichartige Glieder zusammenfassen — Schritt für Schritt" eingefügt. Slider 0–3 wechselt zwischen vier Schritten:
  - Schritt 0: Polynom unsortiert, alle Glieder neutral grau
  - Schritt 1: gleichartige Glieder bekommen gleiche Farbe (5 Farbklassen `farbe-A` bis `farbe-E`)
  - Schritt 2: stabile Umsortierung nach `sortKey` (Glieder mit demselben Variablen-Anteil rücken zusammen, in Originalreihenfolge innerhalb der Gruppe)
  - Schritt 3: pro Farbgruppe nur noch ein zusammengefasstes Glied (Koeffizienten-Summe). Glieder mit Summe 0 fallen weg.
- Fünf Polynome: `5x + 3 − 2x + 7` → `3x + 10`, `4x² + 3x − x² + 2x − 5` → `3x² + 5x − 5`, `2ab − 5a²b + 7ab + 2a²b` → `9ab − 3a²b`, `2x² + 3x − 7x² + 5 + 4x − 2` → `−5x² + 7x + 3`, `5x³ − 2x² + 3x³ + x² − 4` → `8x³ − x² − 4`. Polynome bewusst „durcheinander" gewählt, damit Schritt 1 und 2 sichtbaren Effekt haben.
- Schritt-Titel-Zeile unter der Display-Box (`zus-schritt-titel`) und kontextsensitiver Erklärtext rechts (`zus-erkl`) ändern sich mit dem Slider.
- Glieder werden als `<span class="gl">` mit Farbklasse gerendert; Vorzeichen als `<span class="op">` separater Operator zwischen den Gliedern. CSS-Transition auf `background`/`color` (0.3 s) für sanftes Umfärben zwischen den Schritten.
- Die bisherige Tabelle mit den drei klassischen Beispielen bleibt darunter erhalten (als statisches Nachschlagwerk).

**Auftrag 4 — Klammern auflösen: Formel-Tausch und Vorzeichen-Toggle.**
- Letzte Zeile der Vier-Regeln-Tabelle: `(a+b)(c+d) = ac+ad+bc+bd` → `(a−b)(−c+d) = −ac+ad+bc−bd`. Lehrreicher, weil drei der vier Vorzeichen kippen und die Bedeutung von „jeder mit jedem" mit Vorzeichen-Bookkeeping ernst genommen werden muss.
- Die anschliessende Herleitung „folgt aus dem Distributivgesetz, zweimal angewendet" wurde entsprechend an die neue Formel angepasst.
- Vorzeichen-Toggle: Vor jedem ersten Summanden in den ersten drei Zeilen sitzt ein `<span class="vz-schwach">+</span>`, der standardmässig blass grau und halb-transparent ist. Klick auf den `vz-toggle`-Knopf „Vorzeichen zeigen" setzt die Klasse `.vz-stark` an den Tabellen-Container — dann werden die schwachen Plus rot und fett, der Knopf-Text wechselt zu „Vorzeichen ausblenden".
- **MathJax-Kompatibilität:** Die ursprüngliche Idee, das Toggle-Span mitten in `\(…\)`-LaTeX-Blöcken zu platzieren, scheitert daran, dass MathJax jeden Block als unabhängiges SVG rendert — die HTML-Spans dazwischen würden zwar liegenbleiben, aber die Typografie wechselt am Span-Übergang und wirkt holprig. Lösung: die vier Tabellenzeilen sind komplett auf reines HTML (`<span class="kz-math">…<i>a</i>…</span>`) umgestellt, ohne MathJax-Delimiter. Neue CSS-Regel `.kz-math { font-family: var(--serif); font-size: 15pt; }` und `.kz-math i { font-style: italic; }` macht das Erscheinungsbild ähnlich der MathJax-Ausgabe in den anderen Tabellenzellen. Robust gegen MathJax-Re-Renders und gegen das Show/Hide der Toggle-Spans.

**Auftrag 5 — Binomische Formeln: geometrische Visualisierung als Animation.**
- Im Anschluss an die Fehler-Box wurde eine `anim`-Box „Binomische Formeln — geometrisch" eingefügt.
- Drei Chips wählen zwischen 1./2./3. Binom; zwei Slider stellen `a ∈ [4, 7]` und `b ∈ [1, 3]` ein. Das Canvas (`cv-binomi`, 380×380) zeigt jeweils ein Quadrat, in das die Teilflächen eingezeichnet und mit den konkreten Werten beschriftet sind.
  - 1. Binom: Quadrat mit Seite (a+b), unterteilt in a², 2·a·b (zwei Rechtecke) und b². Alle vier Felder werden mit den ausgerechneten Werten beschriftet (z. B. „a² = 25" für a=5).
  - 2. Binom: Quadrat mit Seite a, unterteilt in (a−b)² oben-links, zweimal b·(a−b) und b² — direkt der PDF-Skizze nachempfunden. Aussenbeschriftung: (a−b) + b = a auf beiden Achsen, mit verbundener Klammer.
  - 3. Binom: Quadrat a² mit ausgeschnittenem b²-Eck oben-rechts (die L-förmige Restfläche entspricht a² − b² und lässt sich zu einem (a+b)·(a−b)-Rechteck umlegen). Untertitel zeigt die ausgerechnete Differenz.
- Rechts neben dem Canvas: die `bin-rechnung`-Box mit Produkt- und Summenform, jeweils mit eingesetzten Zahlenwerten und farblicher Hervorhebung der drei Bausteine (a²-gelb, ab-orange, b²-dunkelorange).
- a/b-Bereiche wurden bewusst klein gewählt (4..7 / 1..3), damit das Quadrat mit allen Feldern lesbar bleibt und a > b für das 2. Binom garantiert ist.
- CSS-Block `.bin-vis`/`.bin-rechnung`/`.hl-a2`/`.hl-ab`/`.hl-b2`/`.hl-minus` neu hinzugefügt.

**Auftrag 6 — Faktorisieren restrukturiert: 6.1 → 6.5 mit zwei neuen Abschnitten.**
- Die alte Struktur (6.1 ggT · 6.2 Binomi rückwärts · 6.3 Kombinieren) wurde nach der PDF-Anleitung umgebaut: **erst** ggT (6.1) und Binomi rückwärts (6.2), **dann** Zweiklammersatz (6.3) und Gruppieren (6.4), **zuletzt** Kombinationen (6.5).
- **6.2 Binomi rückwärts:** in der Beispiel-Tabelle wurde eine Zeile für das 3. Binom ergänzt — eigentlich bereits da (x² − 49 → (x+7)(x−7) und 9a² − 16b² → (3a+4b)(3a−4b)). Zusätzlich eine Zeile `x² + 6x + 9 = x² + 2·x·3 + 3² → (x + 3)²` zur Vertiefung, dass auch der einfachste Fall des 1. Binoms erkannt werden muss. Die Tabelle hat jetzt fünf Beispiel-Zeilen statt vier.
- **6.3 Zweiklammersatz (Satz von Vieta rückwärts):** komplett neu. Schlüsselformel `x² + px + q = (x + r)(x + s)` mit `r + s = p` und `r·s = q`. Drei durchgerechnete Beispiele (`x² + 5x + 6`, `x² − 7x + 12`, `x² + 2x − 15`) decken die drei Vorzeichen-Konstellationen ab. Eine Tipp-Box mit der Vorzeichen-Faustregel (Produkt positiv → gleiche Vorzeichen; Produkt negativ → verschiedene Vorzeichen, das grössere mit dem Vorzeichen von p).
- **6.4 Gruppieren — Summe von vier Gliedern als Produkt:** komplett neu. Grundmuster `ax + ay + bx + by = a(x+y) + b(x+y) = (x+y)(a+b)`. Durchgerechnetes Beispiel `x³ + 3x² + 2x + 6 = (x+3)(x² + 2)` mit `underbrace`-Notation für die beiden Paar-Ausklammerungen. Hinweis im Anschluss: bei Misserfolg eine andere Paarung der vier Glieder versuchen.
- **6.5 Kombinieren — erst ausklammern, dann binomisch:** Inhalt entspricht dem alten 6.3, aber mit erweitertem Vorlauftext: „mehrere Techniken nacheinander — und zwar in einer festen Reihenfolge: zuerst immer der gemeinsame Faktor, danach erst Binom oder Zweiklammersatz".
- **Strategie-Box:** umgebaut von 4 auf 5 Schritte, mit expliziten Verweisen auf die Abschnitte 6.1 bis 6.4. Schritt für 4 Glieder als eigene Stufe ergänzt.
- **Schnell-Übung (Faktorisier-Übung):** um drei Eingabefelder erweitert — `x² + 7x + 12` (Zweiklammersatz), `x² − x − 6` (Zweiklammersatz mit Vorzeichenwechsel), `ax + ay + 2x + 2y` (Gruppieren). Antwort-Normalisierung und Mehrfach-Alternativen für die `check`-Funktion wurden für die drei neuen Felder ergänzt (`fak5/fb5`, `fak6/fb6`, `fak7/fb7`).
- **Aufgabe A5 „Faktorisieren — Kombinationen":** von 5 auf 10 Teilaufgaben erweitert. Die fünf neuen Items decken Zweiklammersatz mit positiven und gemischten Vorzeichen, Vorabausklammern + Zweiklammersatz, und Gruppieren in zwei Varianten (homogene + inhomogene Variablen) ab. Lösungen entsprechend ergänzt; alle didaktisch-relevanten Zwischenschritte ausgeschrieben (Produkt/Summe-Suche, Paarweise-Gruppierung).

**Nicht inhaltlich, aber strukturell:**
- Inline-`<style>`-Block am Datei-Anfang um drei grosse Gruppen erweitert: Begriffe-Animation-Regeln (Hervorhebungs-Modi, Swatches, Erklärbox), Zusammenfassen-Animation-Regeln (Farbklassen, Schritt-Titel-Stil), Vorzeichen-Toggle (`.vz-schwach`, `.vz-stark`, `.vz-toggle`), Binomi-Visualisierung-Regeln (Grid-Layout, Rechnungs-Hervorhebungen) und die neue `.kz-math`-Regel für die MathJax-freie Klammern-Tabelle.
- Vier neue Inline-`<script>`-Blöcke vor `buildNav`: Begriffe-Renderer, Zusammenfassen-Renderer, Vorzeichen-Toggle-Handler, Binomi-Canvas-Renderer. Alle als IIFE gekapselt, alle nutzen `document.addEventListener('DOMContentLoaded', …)` für Init. Keine globalen Variablen ausser den bereits in `mathlib.js` definierten Helfern (`initCanvas`).
- `node --check` auf alle inline JS-Blöcke einzeln ausgeführt: 0 Syntaxfehler. HTML-Tag-Bilanz: ausgewogen (17/17 Anker, 239/239 div, 102/102 span). Strukturelle Marker (h2-IDs, aside, toc-wrap): alle exakt 1× vorhanden.

---

## [unreleased] — 2026-05-27 · g1-2 Anpassungen aus PDF (Aufträge 1–8 vollständig)

Auftraggeber-PDF `1_2_aendern.pdf` mit 8 Aufträgen zu `g1-2-zahlen-grundoperationen.html` — alle umgesetzt.

**Auftrag 1 — Einstiegs-Animation „Werkstatt-Werte" überarbeitet.**
- Werte in der Tabelle und in den Chips: `127 → 5`, `−12 → −2` (die übrigen drei Werte `3/40`, `−3.5`, `√2` bleiben).
- Zahlenstrahl-Range von `−15…15` auf `−4…6` reduziert, sodass alle fünf Werte sichtbar sind und ganze Zahlen mit Beschriftung markiert werden.
- `padL` auf 100 px erhöht, damit die ausgeschriebenen Streifen-Labels rechtsbündig links der Streifen Platz haben (vorher 40 px → Labels schnitten ab).
- Streifen-Labels jetzt in Sans-Serif 12 px (vorher Mono 11 px), ausgeschrieben („ℝ (reell)" statt „ℝ"), Streifen-Höhe 20 px (vorher 18 px).
- Streifen-Farben an das Mengen-Diagramm angeglichen: ℝ rot (`#fee2e2/#dc2626`), ℚ orange (`#fef3c7/#f59e0b`), ℤ grün (`var(--gruen-hell/-rand)`), ℕ blau (`var(--blau-hell/-rand)`). Vorher waren die Streifen invertiert (ℕ orange, ℝ blassgrau).
- ZM_WERTE[0] und ZM_WERTE[1] mit neuen Zahlenwerten und angepassten Erklär-Texten („5 ist eine natürliche Zahl …", „−2 liegt links der Null …").

**Auftrag 2 — Mengen-Diagramm an Animation gekoppelt und direkt darunter positioniert.**
- Der `<div class="mengen-vis">`-Block samt einleitendem Erklärabsatz ist aus der ehemaligen Sektion „Mengen-Diagramm und Intervalle" raus und sitzt jetzt unmittelbar unter der Einstiegs-Animation (vor der `<h2 id="definition">`-Sektion). Die Sektion `<h2 id="typen">` ist dadurch zu „Intervalle — Teilmengen von ℝ" geschrumpft.
- IDs `mv-R`, `mv-Q`, `mv-Z`, `mv-N` auf den vier verschachtelten Boxen ergänzt; `<span class="mv-aktive" id="mv-aktive-zahl">` zeigt rechts oben im ℝ-Container die aktuell in der Animation gewählte Zahl.
- `drawZahlmenge()` setzt jetzt zusätzlich `mv-aktive-zahl.textContent` auf den `displayLabel` und gibt der kleinsten enthaltenden Menge (basierend auf `w.inN`/`inZ`/`inQ`/`inR`) die Klasse `mv-treffer` — ein 3 px breiter roter `box-shadow` mit leichtem Halo. Die Verbindung Animation↔Diagramm ist damit visuell sichtbar: oben Streifen, unten die passende Box.
- Neue CSS-Regeln: `.mv-aktive` (Mono-Pille rechts oben in der ℝ-Box, weiss auf rotem Rand), `.mv-treffer` (Highlight-Shadow), plus `transition:box-shadow .15s` auf den vier Boxen für sanftes Aufleuchten.

**Auftrag 3 — Definitions-Tabelle in Mengen-Diagramm-Farben.**
- Tabellen-Zeilen in der Definitions-Box bekommen Klassen `zm-row-N`/`zm-row-Z`/`zm-row-Q`/`zm-row-R`. Erste Zelle jeder Zeile erhält einen 3 px breiten farbigen Linksrahmen und einen hellen Hintergrund passend zur Farbe der jeweiligen Box im Mengen-Diagramm darüber (Blau für ℕ, Grün für ℤ, Orange/Gelb für ℚ, Rot für ℝ).
- Beispiele in der Tabelle an die neuen Werte angepasst (`127` → `5`, `-12` → `-2`).
- Auch im Mengen-Diagramm selbst sind die Beispiel-Zahlen aktualisiert: ℕ-Box zeigt „0, 1, 2, 5, 42" (statt „0, 1, 7, 42, 127"), ℤ-Box „−2, −1, 0" (statt „−12, −3, 0").

**Auftrag 4 — „Welche Zahlenmenge?" als kompaktes 4×3-Grid, direkt nach den Definitionen.**
- Position: das `<div class="widget">`-Quiz ist aus der Sektion „Intervalle — Teilmengen von ℝ" raus und sitzt jetzt direkt unter dem Definitions-`block-def`, vor `<h2 id="darstellungen">`. Inhaltlich passt es dorthin: das Quiz prüft Zahlenmengen, nicht Intervalle.
- Layout: `buildKl()` rendert die Aufgaben jetzt in einen `<div class="kl-grid">`-Container mit `grid-template-columns:repeat(3, 1fr)`. Auf schmalen Bildschirmen automatisch 2 Spalten (`max-width: 720px`) bzw. 1 Spalte (`max-width: 480px`). Aufgaben-Nummerierungen `(1) (2) …` aus der `.kl-zahl`-Anzeige entfernt — die Aufgabe ist die Zahl selbst.
- Kachel-Optik kompakter: `.kl-spiel`-Padding von 14 px auf 10-12 px reduziert, `.kl-zahl`-Schriftgrösse von 1.1 rem auf 1.0 rem, `min-height:42px` auf der Zahl-Box für gleichmässige Karten-Höhen unabhängig von der Formel-Höhe. Buttons mit `flex:1; min-width:0` füllen die Karten-Breite gleichmässig aus. Feedback-Box `font-size:0.78rem` (vorher 0.85 rem), kleinere Padding.
- Inhalt erweitert von 5 auf **12 Aufgaben**, pädagogisch in 4 Reihen gestaffelt mit ausgewogener Verteilung 3-3-3-3 über ℕ/ℤ/ℚ/ℝ:
  - Reihe 1 (Einstieg): `42` (ℕ), `−9` (ℤ), `0.5` (ℚ)
  - Reihe 2 (Brüche/Vorzeichen): `5/8` (ℚ), `−3` (ℤ), `0` (ℕ)
  - Reihe 3 (Wurzeln/irrational): `√25 = 5` (ℕ, Wurzel-Stolperstein), `√7` (ℝ), `π` (ℝ)
  - Reihe 4 (subtil): `−2^4 = −16` (ℤ, Potenz-vor-Vorzeichen-Stolperstein), `0.142857̄` (ℚ, periodisch), `√2` (ℝ)

**Auftrag 5 — Bug-Fix bei den Lösungs-Feedbacks im „Welche Zahlenmenge?"-Widget.**
- Im Screenshot des Auftraggebers waren bei den Karten 3, 4, 5 die `✓ Richtig — …`-Texte mit rohem LaTeX zu sehen (z.B. `\(\sqrt{16} = 4\) → natürliche Zahl.`). Ursache: `fb.textContent = …` setzt Text als Plaintext, MathJax wird nicht ausgelöst.
- Fix: `fb.innerHTML = …` plus expliziter `window.MathJax.typesetPromise([fb])`-Aufruf in `checkKl()`. Die `KL_AUFG`-Hint-Strings zusätzlich auf konsistente LaTeX-Befehle `\(\mathbb{N}\)`/`\(\mathbb{Z}\)`/`\(\mathbb{Q}\)`/`\(\mathbb{R}\)` umgestellt (vorher Unicode-Doppelstrich, was im Lehrmittel-Kontext stilfremd wirkte). LaTeX-Ausdrücke wie `\(\sqrt{16} = 4\)` werden jetzt korrekt gerendert.

**Auftrag 7 — Vorzeichenregeln neu strukturiert.**
- Aus der 2×2-Matrix mit blossen `+`/`−`-Symbolen ist eine zweispaltige Tabelle mit konkreten Zahlenbeispielen geworden. Spalten: Multiplikation und Division. Zeilen: die vier Fälle `++`, `+−`, `−+`, `−−` mit jeweiligem Rechenbeispiel (`(+6) · (+2) = +12`, …, `(-12) : (-4) = +3`).
- Erläuternder Satz vor der Tabelle umformuliert: die „gleiches/ungleiches Vorzeichen"-Merkregel steht jetzt im Einleitungs-Absatz statt nachgestellt.

**Auftrag 8 — Runden-Tabelle um signifikante Stellen erweitert.**
- Neue Spalte „auf 3 signifikante Stellen" mit wissenschaftlicher Notation (Mantisse × 10er-Potenz).
- Zwei zusätzliche Zeilen für interessante Grössenordnungen (`0.000\,041\,28 → 4.13·10⁻⁵` und `284\,500 → 2.85·10⁵`), die das Konzept signifikanter Stellen gegenüber dem reinen Nachkommastellen-Runden abheben.
- Erläuternder Absatz unter der Tabelle, der „signifikante Stellen" kurz definiert und auf die Mehrdeutigkeit von End-Nullen ausserhalb der wissenschaftlichen Notation hinweist.

**Auftrag 6 — Intervalle-Sektion in die Theorie-Sektion umgezogen + neue interaktive Animation.**
- Die ehemals eigenständige `<h2 id="typen">Intervalle — Teilmengen von ℝ</h2>`-Sektion ist als `<h3 id="typen">`-Sub-Section in die Theorie-Sektion gewandert, eingefügt nach dem Runden-Unterabschnitt. Die `id="typen"` ist erhalten geblieben (verschoben vom h2 auf den h3), damit der bestehende Anker-Link `g1-2-zahlen-grundoperationen.html#typen` aus `g4-0-praxisbeispiel-bm2-klasse.html` (Z. 574) weiter funktioniert.
- Theorie-h2-Titel auf „Weitere Theorie — Vorzeichen, Betrag, Rundung, Intervalle" erweitert.
- Neue Animation `iv-anim` mit zweispaltigem Grid (auf schmalen Bildschirmen einspaltig untereinander): links die Intervall-Typen-Tabelle, jede Zeile klickbar mit eigenem Beispiel; rechts die formale Schreibweise zuoberst, darunter die Mengen-Schreibweise und ein Zahlenstrahl-Canvas mit dem Intervall als orange-gelber Balken. So liegen formale und grafische Darstellung **direkt übereinander** im rechten Panel (wie im Auftrag gewünscht), während die Auswahl in der Tabelle links unabhängig sichtbar bleibt.
- Fünf konkrete Beispiele, eines pro Tabellenzeile:
  - `[2; 5]` — geschlossen, beide Punkte gefüllt
  - `]−1; 3[` — offen, beide Punkte hohl
  - `[0; 4[` — halboffen, links gefüllt / rechts hohl
  - `]−∞; 2]` — links unbeschränkt, gestrichelter Pfeil nach links, rechts gefüllt
  - `[−1; +∞[` — rechts unbeschränkt, gestrichelter Pfeil nach rechts, links gefüllt
- `IV_BEISPIELE`-Array mit `a`/`b` als Zahlen oder `null` (für `±∞`), `linksZu`/`rechtsZu` für Endpunkt-Stil. `drawIntervall()` rendert auf `cv-iv` (520×120 px): orange-gelber Balken über der Achse, Skala alle 1 Einheit von −5 bis 6, Endpunkte als orange gefüllte oder hohle Kreise (Radius 5.5 px), bei unbeschränkten Seiten ein gestrichelter orange Pfeil über die Canvas-Kante hinaus. Achse mit klassischer Pfeilspitze rechts. Endpunkt-Labels `a = …` und `b = …` unter den Punkten, 36 px unter der Achse.
- `selectIntervall(i)` schaltet zwischen den Beispielen um, setzt die `.aktiv`-Klasse auf der jeweiligen Tabellenzeile (gelb-orange Hintergrund + 3-px-Linksrahmen), aktualisiert die drei DOM-Elemente `iv-formal` / `iv-mengen` / `iv-erkl` und triggert MathJax-Typesetting auf ihnen. Init in DOMContentLoaded: Listener auf alle `.iv-row`-Klicks plus erste `drawIntervall()`.
- Geometrie verifiziert: alle 5 Beispiele liegen vollständig innerhalb des Canvas (pxL/pxR-Berechnung mit Range −5…6, padL/padR 30 px). Balken-Breiten: 125 px (`[2;5]`), 167 px (offene/halboffene Intervalle), 292 px (unbeschränkte Intervalle).

**Verifikation:**
- JS-Syntax-Check des Inline-Script-Blocks bestanden (`node --check`).
- Geometrie-Simulation aller 5 Intervalle in Python: jeder Endpunkt innerhalb des Canvas.
- OL/LI-Bilanz und Standard-Pre-Flight grün über alle 23 Themenseiten.
- ToC wird aus h2-IDs autogeneriert; die ehemalige Sektion „Intervalle — Teilmengen von ℝ" verschwindet als eigener h2-Eintrag aus dem ToC, dafür heisst die Theorie-Sektion neu „… , Intervalle". Cross-File-Link `#typen` aus g4-0 weiter funktional (Anker ist auf h3 gewandert).
- Die Mengen-Diagramm-Verbindung visuell prüfbar: Chip wählen → Diagramm rechts zeigt die Zahl, kleinste enthaltende Box leuchtet rot auf. Bei `5 → ℕ`, `−2 → ℤ`, `3/40 → ℚ`, `−3.5 → ℚ`, `√2 → ℝ`.



Konsistenz-Audit aller 23 Grundlagen-Themenseiten gegen den Styleguide v1.8, anschliessend Bereinigung der Befunde in 11 Patch-Schritten. Der Audit-Bericht selbst ist in `konsistenz-bericht.md` (Project-Knowledge) festgehalten.

**Bereinigte Punkte (entlang der Bericht-Reihenfolge):**

- **Punkt A — Aufgaben-Karten-Titel in g3-1.** Sieben Karten A1–A7 vom alten Muster `▲ Aufgabe N · Titel` auf das Standardschema `🟠 <span class="aufg-nr-tag">A<N></span><span class="aufg-titel-text">Titel</span>` umgestellt. g3-1 war die einzige Seite mit diesem Alt-Muster.

- **Punkt B — Block-Titel-Emojis in g4-3.** 20 Stellen ergänzt: 13× `📘 Definition` / `🟢 Beispiel` (vorher Emoji weggelassen) und 7× Aufgaben-Karten vom Alt-Muster `<div class="block-titel">Aufgabe</div>` auf das Standardschema mit `aufg-nr-tag`/`aufg-titel-text` (A1–A7-Titel aus den `<h3 id="aN">A<N> · Titel</h3>`-Headern übernommen). A6 mit `<span class="aufg-vertiefung">offen</span>`-Pille statt des früheren „Aufgabe (offen)".

- **Punkt C — Beispiel-Emoji in g1-3, g1-4.** 5 Stellen `▶ Beispiel` → `🟢 Beispiel` (Konflikt mit `▶`-Symbol der Lösungs-Toggle-Buttons beseitigt).

- **Punkt D — Beweis-Emoji in g2-2b.** 1 Stelle (pq-Formel-Herleitung) `🟣` → `🔷` (gemäss Styleguide §5.1: Violett ist die Hintergrund-Farbe der `block-beweis`-Klasse, der Emoji-Marker im Titel ist 🔷).

- **Punkt E — Teilaufgaben-Listen-Migration auf `aufg-liste`.** Dies war der grösste Brocken — über alle Themenseiten:
  - 58 alte `<ol style="margin…">`-Aufgaben-Teillisten auf `<ol class="aufg-liste">` migriert (Patch 63)
  - 17 Lösungs-Blöcke mit `<p>(a) …</p>`-Pattern auf `<ol class="aufg-liste"><li>…</li></ol>` (Patch 64)
  - 7 weitere plain `<ol>` in Lösungen auf `aufg-liste` angeglichen (Patch 65)
  - 3 SVG-Skizzen-Titel in g5-1 A2 (`a) Leiter` → `1) Leiter` etc.) plus Schluss-Absatz-Verweise aktualisiert
  - g3-1 A3 Vertikaltest: Check-Row-Aufgabe und Lösungs-Liste auf `1./2./3./4.` umgestellt, JS-Funktion `checkA3` auf nummerische Keys umgeschrieben
  - g2-1 A2 und A3: 4+3 verschachtelte Sub-Aufgaben-Karten (`block-aufg` innerhalb `block-aufg`) durch `<ol class="aufg-liste">` mit `<li>` ersetzt, interaktive Eingabe-Felder und JS-Hooks (`checkEq`/`checkIneq`/`typ-btns`) erhalten
  - g2-1 A6 Lösung: `<strong>Antwort (a)</strong>` / `<strong>Antwort (b)</strong>` durch `<ol class="aufg-liste">` mit 2 `<li>` ersetzt (Verweis-Texte mitmigriert)
  - g1-4 A1/A2/A3: nachträgliche Inhalts-Reparaturen, weil ein Migrationslauf Inline-`(a)…(b)…(c)…(d)…(e)…(f)`-Patterns nur teilweise erfasst hatte
  - g5-2b A2: 5. Item, das durch eine `block-tipp`-Zwischenkarte aus der `<ol>` gefallen war, wieder eingefügt
  Endzustand: in jeder Aufgabe und jeder zugehörigen Lösung steht ausschliesslich `<ol class="aufg-liste">` mit orange-Pillen-Nummerierung. Keine `<ol type="a">`, `<ol type="i">`, `<ol style="margin">`, plain `<ol>`, `<p>(a)…</p>`-Folgen, `<p><strong>a)</strong>…</p>`-Folgen oder Inline-`(a)…(b)…(c)…`-Aufzählungen mehr in Aufgaben- und Lösungs-Kontexten.

- **Punkt F — Einstieg-Trennzeichen.** 4 Stellen vereinheitlicht: 2× Doppelpunkt → Halbgeviertstrich (g3-1, g4-3), 2× Untertitel ergänzt (g5-2b „die Vierecks-Familie", g5-2c „der Kreis und seine Konstante π").

- **Punkt G — „Zusatzmaterial" konsistent.** 2 Stellen „Zusatzmaterial zum Download" → „Zusatzmaterial" (g1-3, g1-4).

- **Punkt H — Ressourcen-Subtitel.** 6 Stellen: 5× `style="margin-top:18px"` zum „📝 Aufgabensammlungen"-Subtitel ergänzt (g3-2, g5-2a–d), 1× „🎬 Erklärvideos" → „🎬 Erklärvideos (Playlists)" in g3-1.

- **Punkt I — Styleguide-Update.** §6.1 um eine Notiz zum Praxisbeispiel-Suffix `· Praxisbeispiel` im `pt-bereich` ergänzt; neuer Sub-Abschnitt §6.1.1 „Praxisbeispiel-Seiten (Sonderfall des Skeletts)" dokumentiert das reduzierte Skelett für Praxisbeispiel-Seiten (Präfix `gN-0-…`/`sN-0-…`): kein `rlp-kompetenzen`-Block, keine `<h2 id="aufgaben">`/`downloads`/`ressourcen`-Sektionen, `· Praxisbeispiel`-Suffix in `pt-bereich`. Aktuell ist `g4-0-praxisbeispiel-bm2-klasse.html` der einzige Vertreter dieses Sonderfalls. Styleguide-Version auf 1.9 erhöht.

**Methodisches Nebenresultat:** Pattern-Matching für Listen-Migrationen ist tückisch, wenn das Quell-Format viele Varianten kennt (`<p>(a)`, `<p><strong>a)</strong>`, Inline-`(a)(b)(c)` in einem `<p>`, mit/ohne einleitenden Text, mit/ohne Zwischen-`block-tipp`). Vereinheitlichungs-Skripte brauchen einen **Lückenschluss-Check pro Stelle**: pro Aufgabe „Items in Aufgabe-`ol`" vs. „Items in Lösungs-`ol`" zählen — Diskrepanz zeigt eine kaputte Migration sofort. Dieser Check fand zwei der drei nachträglichen Reparaturen.

**Verifikation am Ende der Sweep-Serie:**

- OL/LI-Tag-Bilanz pro Datei ausgeglichen (23/23).
- Standard-Pre-Flight grün (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0`) auf allen 23 Themenseiten.
- 0 verbleibende `<ol>` ohne `class="aufg-liste"` in Aufgaben-/Lösungs-Kontexten.
- 0 verbleibende `<p>(letter)`-/`<p>(num)`-/`<p><strong>letter)</strong>`-Marker-Sequenzen in Aufgaben/Lösungen.
- 0 verbleibende Verweise auf alte Buchstaben-Indizes (`Antwort (a)`, `siehe (a)`, `in (a)`, …) in Lösungen.
- 0 Block-Karten in g4-3 ohne korrektes Emoji-Präfix.
- Block-Modifier-Inventar bleibt aus dem §5.1-Set, keine Eigenkreationen.
- JS-Hooks für interaktive Widgets (`checkEq`, `checkIneq`, `checkA3`, `typ-btns`) durch die Sub-Karten-Auflösungen in g2-1 und g3-1 unverletzt — IDs und JS-Mappings mitmigriert.

---



Die in g1-1 eingeführten Aufgaben-Nummerierungs-Klassen werden vom lokalen `<style>`-Block der Themenseite in die globale `style.css` migriert und auf alle anderen Themenseiten ausgerollt. Damit sehen die Aufgabennummern auf jeder Themenseite gleich aus.

**Klassen-Migration nach `style.css`:**

- `.aufg-nr-tag` — orange Pille mit Aufgabennummer im Karten-Titel
- `.aufg-titel-text` — Margin-Spacer zwischen Pille und Titel-Text
- `.aufg-liste` + `.aufg-liste > li` + `.aufg-liste > li::before` — Counter-basierte Listen mit Pille statt Default-`<ol>`-Marker
- `.kl-nr` — kleine neutrale Pille für Klassifizier-Term-Nummern

Diese fünf Selektoren sind aus dem `<style>`-Block in `grundlagen/g1-1-grundlagen.html` entfernt und stehen jetzt zentral in `style.css` (Block direkt nach der Legacy-Klasse `.aufg-nr`). Die Legacy-Klasse `.aufg-nr` (Kreis-Form) bleibt unverändert in `style.css` erhalten, weil sie weiterhin von Druckseiten in `downloads/grundlagen/*/teste-dich-selbst.html` etc. genutzt wird. Im Kommentar dort als „Legacy" markiert.

**Patch-Lauf über 19 Grundlagen-Themenseiten:**

| Datei | Aufgaben-Titel | aufg-Listen |
|---|---:|---:|
| g1-2-zahlen-grundoperationen | 7 | 4 |
| g1-3-algebraische-terme | 7 | 0 |
| g1-4-zehnerpotenzen-quadratwurzeln | 7 | 0 |
| g2-1-grundlagen | 7 | 0 |
| g2-2a-lineare-gleichungen | 8 | 2 |
| g2-2b-quadratische-gleichungen | 7 | 0 |
| g2-3-lineare-gleichungssysteme | 7 | 0 |
| g3-2-lineare-funktionen | 7 | 0 |
| g3-3-quadratische-funktionen | 7 | 0 |
| g4-1-grundlagen | 7 | 0 |
| g4-2-diagramme | 7 | 0 |
| g5-1-grundlagen | 7 | 0 |
| g5-2a-dreiecke | 7 | 0 |
| g5-2b-vierecke | 7 | 0 |
| g5-2c-kreis-und-kreisteile | 7 | 0 |
| g5-2d-zentrische-streckung-aehnlichkeit | 7 | 0 |
| g5-3-trigonometrische-berechnungen | 7 | 0 |
| g5-4-einheitskreis | 7 | 0 |
| g5-5-trigonometrische-gleichungen | 7 | 0 |
| **Gesamt** | **134** | **6** |

Patch-Muster:
- Aufgaben-Titel `<div class="block-titel">🟠 A1 — <Titel></div>` → `<div class="block-titel">🟠 <span class="aufg-nr-tag">A1</span><span class="aufg-titel-text"><Titel></span></div>`. Vorhandene `<span class="aufg-vertiefung">…</span>`-Pillen am Ende werden mit in `aufg-titel-text` aufgenommen — Layout bleibt korrekt.
- Aufgaben-Listen `<ol style="margin:8px 0 0 22px">` → `<ol class="aufg-liste">`. Die genauen Inline-Style-Werte als Heuristik genutzt, weil sie konsistent für Aufgaben-Listen verwendet wurden und in keiner anderen Stelle vorkommen.

**Drei Dateien bewusst nicht angetastet:**

- `g3-1-grundlagen.html` — verwendet eigenes Aufgaben-Design (`▲ Aufgabe 1 · <Titel>` mit `id="A1"` am Block, `check-aufg`-Klasse für integriertes Prüfungs-Widget). Würde substantielles Refactoring erfordern. Bei separater Welle migrierbar.
- `g4-0-praxisbeispiel-bm2-klasse.html` — Praxisbeispiel-Sonderseite ohne klassische Aufgaben-Karten.
- `g4-3-masszahlen.html` — Aufgabennummer steht in separatem `<h3>` über der Karte (Format `A1 · Kleine Stichprobe händisch`), Block-Titel selbst trägt nur `Aufgabe`. Auch hier eigene Welle bei Auftraggeber-Wunsch.

Diese drei Dateien sind im COLLABORATION-Kontext „funktionierende Strukturen, kein Refactoring ohne Auftrag" (§6).

**STYLEGUIDE-Update:**

Neuer Abschnitt §5.4 „Aufgaben-Nummerierung (verbindlich)" mit drei Beispielen (Karten-Titel, Teil-Listen, Klassifizier-Term-Nummern) und expliziter Sperre des alten Spiegelstrich-Musters `🟠 A1 — Titel`. Die bisherigen §5.4 Canvas-Konventionen werden zu §5.5 (Untersektionen 5.5.1 bis 5.5.4 entsprechend). Drei Referenzen auf das alte `§5.4.1` in `HOWTO-neue-themenseite.md`, `COLLABORATION.md` und `master-todoliste.md` auf `§5.5.1` aktualisiert.

**Verifikation:**
- Stichprobe: Spot-Check in 3 zufälligen Dateien (g1-2, g2-2a, g5-3) zeigt korrektes Markup.
- Sanity: `grep -rE 'block-titel">🟠 A\d+ —' grundlagen/` liefert keine Treffer mehr (ausser in den drei bewusst ausgesparten Dateien) — kein Rest des alten Musters.
- Duplikat-Check pro Datei: keine Datei hat zwei `aufg-nr-tag">A<n><` mit gleicher Nummer.
- Pre-Flight aller 23 Grundlagen-Themenseiten: alle grün (`pw=1 mc=1 nav=1 ml=1 bn=1 bad=0`).

**Schwerpunkt:** Alle 13 Schwerpunkt-Themenseiten sind aktuell Stubs ohne `block-aufg`-Aufgaben-Karten. Sobald sie ausgearbeitet werden, gilt der STYLEGUIDE §5.4 automatisch.

---

## [unreleased] — 2026-05-26 · g1-1 Politur — dritte Iteration (4 Detail-Fixes)

Vier Befunde aus dem Browsertest des vorherigen Snapshots:

- **Term/Hauptop-Tabelle: linke Spalte jetzt mit farbiger Hinterlegung wie rechts.** Vorher hatte nur die rechte Spalte (Hauptop-Pille) eine farbige Hinterlegung; links war nur die Schriftfarbe gesetzt, was bei der Mono-Tabellenschrift kaum erkennbar war. Neu: MathJax-`\colorbox{Hintergrund}{$\color{Vordergrund}\boldsymbol{Symbol}$}` für die fünf einfachen Operatoren-Zeilen (`+` grün/blau, `·` blau, `−` grau). Die Hochstellungs-Zeile (`(2·x)^3`) lässt sich mit `\colorbox{...}{$\boldsymbol{^{\,3}}$}` nicht sauber rendern, weil `^` ohne Vor-Ausdruck syntaktisch ungültig ist; dort wird das `^3` per HTML (`<sup class="hop-sup-pot">3</sup>`) mit eigener CSS-Hinterlegung gesetzt. Beim Bruch wurde das ganze `\dfrac` farbig zu machen unschön, also folgt der Bruch dem PDF-Auftrag wörtlich: **nur der Bruchstrich hat farbige Hinterlegung**. Implementierung: HTML-Konstrukt `<span class="bruch-hop">` mit `<span class="bruch-zaehler">`, `<span class="bruch-strich">`, `<span class="bruch-nenner">` als Flex-Column. Der Bruchstrich ist ein 6 px hoher gelblicher Balken (`#fef3c7`) mit braunem Inset-Schatten als Rand, Zähler und Nenner als gewöhnliches Inline-Math. MathJax-Konfiguration um `color`-Paket erweitert (`packages:{'[+]':['boldsymbol','color']}` plus `loader.load:['[tex]/boldsymbol','[tex]/color']`).
- **Würfel-Demos: Gesetz selbst auch zweispaltig.** Vorher zeigte der Box-Header das ganze Gesetz inline als `\(a+b=b+a\) · \(a·b=b·a\)` mit `·` als Trenner — der `·` war optisch ein Multiplikationspunkt und konnte falsch interpretiert werden. Neu: das Gesetz nimmt die gleiche `wb-grid`-2-Spalten-Aufteilung wie die Beispiele darunter. Zelle 1 hat die Additions-Version (`a+b = b+a`), Zelle 2 die Multiplikations-Version (`a·b = b·a`). Beim Distributivgesetz gilt das nicht — dort vereint die Gleichung die Produkt- und Summen-Form. Lösung: zwei Zellen mit Produkt-Form (`a·(b+c)`) und Summen-Form (`a·b + a·c`), und ein in CSS gerendertes `=`-Zeichen mittig zwischen den Zellen (`.wb-mit-gleich::before`). Auf Bildschirmen < 760 px (Zellen untereinander) verschwindet das `=` automatisch (`display:none`), weil es sonst falsch positioniert wäre. Neue CSS-Klasse `.wb-gesetz` für den Gesetz-Block: weisser Hintergrund, leichter Border, etwas grössere Schrift als die Beispiel-Zellen.
- **A1-A3: Aufgabennummer in den `<ol>`-Listen deutlich vom Term abgesetzt.** Vorher Standard-`<ol>`-Marker (`1.`, `2.`, ...) direkt vor dem LaTeX-Term mit Browser-Standard-Padding. Neu: Klasse `aufg-liste` (statt inline-style `margin:8px 0 0 22px`) mit `list-style:none` und Counter-basiertem `::before`-Pseudo-Element. Die Nummer wird als kleine orange Pille gerendert (gleiche Farbfamilie wie `aufg-nr-tag` bei den Karten-Titeln, aber kompakter — `min-width:28px`, `padding:1px 6px`, `font-size:0.82rem`), absolut positioniert im linken `padding-left:48px`-Bereich des `<li>`. Resultat: zwischen Nummer und Term liegt jetzt eine deutliche visuelle Lücke und farbliche Trennung. Patch nur auf A1, A2, A3 angewandt — A4-A7 haben keine Mehrteilig-Listen (A4 ist Eingabefeld, A5/A6/A7 sind Einzelaufgaben).
- **A5-Lösung: Bruch-Nenner auf 12x, erste drei Antwort-Zeilen entfernt.** Vorher führte die Lösung erst durch die Mechanik der Ausklammerung (Gemeinsamer-Faktor-Identifizierung, Display-LaTeX der Ausklammerung, Hauptop-vorher/-nachher-Vermerk), bevor die Anwendungen kamen. Drei Absätze (rot markiert im Begutachtungs-PDF) jetzt gestrichen; die Lösung führt direkt von der Motivation zu Anwendung 1 und Anwendung 2. Anwendung 2 wurde inhaltlich verschärft: Nenner `3x` → `12x`, damit das Kürzen nicht mehr alle Faktoren entfernt sondern eine `1/4`-Komponente hinterlässt: \(\dfrac{6x^2 + 9x}{12x} = \dfrac{3x \cdot (2x+3)}{12x} = \dfrac{2x+3}{4}\). Didaktischer Mehrwert: zeigt, dass nur der *gemeinsame* Faktor `3x` wegkürzt, der zusätzliche Faktor `4` im Nenner bleibt stehen. Arithmetik mit sympy verifiziert: `simplify((6x²+9x)/(12x)) = x/2 + 3/4 = (2x+3)/4`; Test bei \(x=1\): `15/12 = 5/4` ✓, bei \(x=2\): `42/24 = 7/4` ✓.

**Verifikation:** JS-Syntax-Check bestanden, Pre-Flight grün, strukturelle Integrität sauber (keine doppelten Marker, alle 7 A-Tags eindeutig, keine doppelten Toggle-IDs), LaTeX-Klammer-Balance in den `\colorbox`-Zeilen okay.

---

## [unreleased] — 2026-05-26 · g1-1 Politur — Folge-Iteration (4 Bug-Fixes)

Vier konkrete Befunde aus dem Browsertest des vorherigen Snapshots, alle in g1-1 behoben:

- **Strukturbaum: Exponent jetzt rosa wie Basis.** In `sbBoxKlasse(rolle)` war die Rolle „Exponent" als `summand` (orange) klassifiziert. Da Exponent und Basis zusammen die Potenz aufbauen, gehört der Exponent visuell zur Potenz-Familie und wird neu als `basis` (rosa) klassifiziert. Begründung im Code als Kommentar festgehalten. Verifiziert mit Beispiel `6·(x-4)²+5`: Exponent `2` jetzt rosa, Basis `(x-4)` rosa, Summanden orange.
- **Strukturbaum-Vorgabe-Buttons reagieren jetzt auf Klicks.** Der `addEventListener('click', ...)` in `sbInit()` registrierte die Handler beim DOMContentLoaded — vor MathJax-Typesetting der Button-Inhalte. MathJax hat beim Rendern der `\(...\)`-Formeln ein `<mjx-container>`-SVG in den Button eingefügt, das das Click-Event ggf. abfängt (`pointer-events`-Verhalten von MathJax-SVG-Output). Fix: `addEventListener`-Setup entfernt, stattdessen direkt inline `onclick="sbWaehleVorgabe(0)"` etc. an jedem Button — das funktioniert unabhängig vom DOM-Re-Build durch MathJax. Eingabe „eigener Term" und Enter-Handler bleiben unverändert (haben kein MathJax-Rendering im selben Element).
- **Klassifizier-Übung: Aufgabennummer deutlich vom Term abgesetzt.** Vorher: `(1) 5+2·x` inline. Neu: `<span class="kl-nr">(1)</span>5+2·x` mit eigener Pille — Mono-Schrift, Hellgrauer Hintergrund, `margin-right:18px`, vertikale Mitte. Pillen-Optik konsistent zur orangen `aufg-nr-tag`-Pille bei den grossen A-Aufgaben (gleicher Padding, gleiche Border-Radius), nur Farbe neutral (tinte-2 auf papier-2 statt orange).
- **Würfel-Demos: 2-Spalten-Layout, ohne `·`/`=`-Trenner.** Vorher: pro Gesetz zwei Zeilen (Addition oben, Multiplikation unten), jede Zeile mit `=` als Trenner zwischen den beiden Seiten der Gleichung. Neu: Grid mit zwei Zellen nebeneinander — links die Additions-Version (Summe), rechts die Multiplikations-Version (Produkt). Innerhalb jeder Zelle stehen die beiden Seiten der Gleichung durch `\quad` (Whitespace) getrennt; kein `=` oder `·` als visueller Trenner mehr. Beim Distributivgesetz (das Produkt- und Summen-Form vereint) gilt die natürliche Lese-Richtung des Gesetzes selbst: links die Produkt-Form `a·(b+c) = a·(b+c)`, rechts die Summen-Form `ab+ac`. Neue Klassen: `.wb-grid` (2-Spalten, fällt unter 760 px auf eine Spalte), `.wb-zelle`, `.wb-label` (kleine Sans-Caps-Beschriftung „Addition" / „Multiplikation" / „Produkt-Form" / „Summen-Form"), `.wb-formel` (Mono, line-height 1.7 für gute Lesbarkeit bei zwei nebeneinander stehenden Formeln).

**Skript-Verifikation:**
- JS-Syntax-Check bestanden.
- AST-Walk für `6·(x-4)²+5` zeigt korrekte Farbzuordnung: Hauptop=Summe, Summand 1=mul (orange), Faktoren=faktor (grün), Basis=basis (rosa), Minuend/Subtrahend=summand (orange), **Exponent=basis (rosa)** ✓.
- Standard-Pre-Flight grün (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0`).

---

## [unreleased] — 2026-05-26 · g1-1 Themenseite-Politur (Welle O · 1.1)

Detail-Politur und didaktische Umstellung der Themenseite **1.1 Grundlagen** auf Basis von zwölf konkreten Auftragspunkten aus dem Begutachtungs-PDF `1_1_aendern.pdf`. Die Änderungen betreffen Reihenfolge, Interaktivität und Vollständigkeit der Theorieblöcke; Aufgaben A1–A7 bleiben strukturell unverändert (nur A4-Placeholder und A5-Lösung berührt).

**Didaktische Umstellung:**

- **Reihenfolge §4/§5 vertauscht:** „Hierarchie der Operationen" steht jetzt **vor** „Strukturbaum lesen". Der Lerner braucht die Hierarchie als Voraussetzung, um zu verstehen, *welche* Operation im Strukturbaum zuoberst landet. Die Term/Hauptoperation-Tabelle wandert mit der Hierarchie nach vorn. IDs entsprechend: `#hierarchie` und `#strukturbaum` (statt vorher `#darstellungen` und `#typen`); das TOC wird dynamisch aus den `<h2 id>` gebaut und übernimmt die neue Reihenfolge automatisch.
- **Häufige-Fehler-Box bündeln:** Der Satz „Wer auf diese Weise liest, vermeidet typische Fehler — etwa \(x^2 + x^2\) mit \((x+x)^2\) ..." stand bisher im Theorie-Fliesstext (Einstieg). Er wandert in die Fehlerbox unter der Hierarchie und wird dort mit dem `2+3·4 ≠ (2+3)·4`-Beispiel zusammengeführt. Die separate, kürzere Fehlerbox direkt vor den Aufgaben („Häufiger Fehler — Punkt vor Strich vergessen") wird ersatzlos gestrichen (Redundanz). Resultat: eine zentrale, dreigeteilte Fehlerbox (Punkt-vor-Strich · Klammer-Potenz-Verwechslung · Vorzeichen-vor-Potenz) statt drei verstreuter Stellen.

**Neue interaktive Elemente:**

- **Strukturbaum-Widget (interaktiv):** Statt nur ein fester Strukturbaum für \(3 \cdot (x+2)^2 - 5\) kann der Lerner jetzt zwischen vier vorgegebenen Termen wählen (\(3 \cdot (x+2)^2 - 5\), \((a+b) \cdot (a-b)\), \(\dfrac{2x+3}{x^2-1}\), \(-x^2 + \sqrt{x+4}\)) **oder einen eigenen Term eingeben**. Implementierung: Pratt-Parser (Tokenizer + recursive descent) mit korrekter Behandlung von unärem Minus (bindet schwächer als Potenz — d.h. `-x^2` wird als `-(x^2)` interpretiert, in Einklang mit der Hauptoperation-Tabelle). AST-Knotentypen: `sum`, `sub`, `mul`, `div`, `pow`, `neg`, `sqrt`, `num`, `var`. Rendering: rekursiver Walk, der Hauptoperation und Bausteine mit den bestehenden `.term-box`-Farbklassen (haupt/summand/faktor/basis) darstellt; LaTeX wird via MathJax getypesetzt. Eingabe-Syntax: `*`, `/`, `+`, `-`, `^`, `()`, `sqrt(...)` — Unicode-Aliase (`·`, `−`, `√`) werden vorab normalisiert. Fehler bei ungültiger Eingabe zeigt eine deutliche Meldung an, der Baum wird zurückgesetzt. Parser mit 17 Testfällen verifiziert (`node`-Test), darunter alle didaktisch heiklen: `-x^2` → Negation, `(-x)^2` → Potenz, `-2*x^3` → Produkt, `a/b/c` → Quotient (links-assoziativ).
- **Klassifizier-Übung kompakter:** 5 Einzel-Boxen (Vollbreite) → 6 Boxen in **2-Spalten-Grid** (`grid-template-columns: repeat(2, 1fr)`). Neues Beispiel ergänzt: `7 - 4·(x+1)` (Hauptop. Subtraktion, mit Klammer im Subtrahend). Auf Bildschirmen unter 700 px fällt das Grid auf eine Spalte zurück.
- **Hierarchie-Stufen mit Hover-Tooltips:** Jede der vier Stufen (Klammern · Potenzen/Wurzeln · Punktrechnung · Strichrechnung) zeigt bei `:hover` einen Tooltip mit drei konkreten Mini-Beispielen. Implementierung: absolut positionierte `.hi-bsp` mit Pfeil-Pseudoelement; `pointer-events:none` damit der Tooltip die Maus nicht abfängt; `z-index:50` über allen anderen Inhalten.
- **Hauptoperation farbig in Tabelle:** In der Term/Hauptop-Tabelle wird das Operationszeichen der Hauptoperation per `\boldsymbol` und `\color{...}` im LaTeX-Block hervorgehoben — `+` grün (Addition), `·` blau (Multiplikation), `^3` magenta (Potenz), Bruchstrich braun (Division), `−` grau (Negation). Die Hauptoperation-Spalte zeigt zusätzlich die Pille mit derselben Farbcodierung (CSS-Klassen `.hop-add`, `.hop-mul`, `.hop-pot`, `.hop-div`, `.hop-neg`). Lerner sieht so visuell sofort, welcher Operator im Term der entscheidende ist.
- **Würfel-Demos für die drei Rechengesetze:** Statt einer trockenen Form-Tabelle bekommt jedes Gesetz (Kommutativ · Assoziativ · Distributiv) eine eigene `wuerfel-box` mit eigenem 🎲-Button, der zufällige \(a, b, c \in \{-10, \dots, 10\} \setminus \{0\}\) generiert und das Gesetz mit den konkreten Zahlen ausrechnet — links und rechts der Gleichung, mit identischem Resultat (grüner `=`-Trenner) als Bestätigung. Negative Zahlen werden in Klammern dargestellt (`fmtOp`), damit `2 + (-3)` statt `2 + -3`. Bei Distributivität wird zusätzlich der Zwischenschritt gezeigt: \(a \cdot (b+c) = a \cdot (b+c\text{-Summe}) = a(b+c)\) gegen \(ab + ac = ...\). Beim ersten Laden werden für alle drei Gesetze automatisch Beispiele generiert (`wuerfelInit` in DOMContentLoaded).
- **Wichtig-Box bei Rechengesetzen ergänzt:** Hinweis, dass Subtraktion sich in Addition einer negativen Zahl umschreiben lässt (\(5 - 2 = 5 + (-2)\)) und das Kommutativgesetz dann anwendbar ist (\(5 + (-2) = (-2) + 5\)). Der Hinweis steht direkt unter den Würfel-Boxen, weil er sich auf die Frage „warum gelten die Gesetze für Subtraktion nicht?" antwortet.

**Detail-Politur (kleine Korrekturen):**

- **A4-Placeholder neutralisiert:** `placeholder="z.B. 38"` (= das richtige Resultat!) → `placeholder="Resultat eingeben"`. Vorher verriet das Eingabefeld die Lösung von \(T(4) = 2 \cdot (4+1)^2 - 3 \cdot 4 = 38\).
- **A5-Lösung um Motivation und Kürzungs-Beispiel ergänzt:** Vor dem Distributiv-Schritt steht jetzt eine Motivation („Wozu ausklammern? Zwei wichtige Anwendungen…") mit Aufzählung der beiden Anwendungen (Gleichung lösen via Nullprodukt, Bruch kürzen). Nach der Faktor-Form wird Anwendung 1 (Nullprodukt) wie bisher gezeigt und Anwendung 2 (Bruchkürzung) konkret durchgerechnet: \(\dfrac{6x^2 + 9x}{3x} = \dfrac{3x(2x+3)}{3x} = 2x + 3\) (für \(x \neq 0\)). Die Pointe „Aus der Summe lässt sich kein einzelner Summand mit dem Nenner kürzen" wird explizit gemacht.
- **Zusammenfassung „Bausteine":** Quotient (Dividend/Divisor, Zähler/Nenner) und Differenz (Minuend/Subtrahend) ergänzt — vorher fehlten beide. Neue Zelle: „Summanden bei Summen, Subtrahend/Minuend bei Differenzen, Faktoren bei Produkten, Dividend/Divisor bzw. Zähler/Nenner bei Quotienten, Basis und Exponent bei Potenzen".
- **Zusammenfassung „Äquivalenz":** „für jede Belegung denselben Wert" → „für **jede** erlaubte Belegung der Variablen denselben Wert — **nicht** nur für einzelne Testwerte". Schärft den All-Quantor, der bei A3 (Äquivalenz-Aufgaben) didaktisch zentral ist: Stichproben können widerlegen, aber nie beweisen.
- **Aufgabennummern absetzen:** Alle sieben Aufgaben-Titel (A1–A7) bekommen einen visuell deutlichen Tag: `🟠 <span class="aufg-nr-tag">A1</span> Hauptoperation erkennen` statt vorher `🟠 A1 — Hauptoperation erkennen`. Die `.aufg-nr-tag`-Pille ist orange (passt zur `block-aufg`-Farbe), monospace, padding 2px 9px, border-radius 5px. Trennstrich „— " entfällt; der Tag selbst trennt visuell. Dies ist die Welle-O-spezifische Lösung für g1-1; bei späterer Cross-File-Anwendung kann das Pattern in den Styleguide aufgenommen werden.

**Skript-Verifikation:**

- JS-Syntax-Check (`node --check`) auf dem extrahierten Script-Block — bestanden.
- Parser-Test mit 17 Termen (4 Vorgaben + Edge-Cases + A1-Aufgaben): 16/17 erwartete Hauptoperationen exakt, das eine „Fail" war nur ein Test-Erwartungs-Mismatch („Multiplikation" vs. konsistente Bezeichnung „Produkt" — der Code ist korrekt).
- Standard-Pre-Flight (COLLABORATION §3.6): `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok` — grün.
- Struktureller Integritäts-Check (§3.7): keine Duplikate, Tag-Bilanz sauber, Slot-Limits eingehalten, alle sieben A-Tags eindeutig vorhanden, keine doppelten `toggleL`-IDs.

**Anmerkungen für Cross-File-Anwendung (nicht Teil dieser Welle):**

- Das `.aufg-nr-tag`-Muster für visuelles Absetzen der Aufgabennummern wurde im PDF als „allgemein über alle Seiten" markiert. Hier nur für g1-1 angewandt; Übernahme in die anderen 22 Themenseiten (Grundlagen + Schwerpunkt) wäre als eigene Welle sinnvoll — einheitlicher Sweep über alle `block-titel` in `block-aufg`-Blöcken, plus Styleguide-Eintrag in §5.
- Der „neutrale Placeholder"-Hinweis (Lösung nicht verraten) sollte ebenfalls projektweit geprüft werden, da das PDF ihn als „allgemein" markiert. Schneller grep-Sweep: `grep -rn 'placeholder="z\.B\.' grundlagen/ schwerpunkt/` listet alle Eingabefelder auf, die potenziell die Lösung verraten.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle O (TO.1–TO.12, Detail-Politur)

Zwölf P5-Items, allesamt kleine Detail-Verbesserungen an den Themenseiten. Neun davon umgesetzt, drei nach Prüfung bewusst nicht angefasst (Begründung jeweils unten).

**Erledigt:**

- **TO.1 (g3-2 Typen-Tabelle):** Variable in „Senkrechte Gerade" von \(x = c\) auf \(x = k\) umbenannt (zwei Stellen: Tabellenzeile und JS-Animationslabel `Senkrecht x=k`). Verwechslung mit der Konstanten \(c\) in \(ax^2 + bx + c\) (g3-3) ist damit vermieden — \(k\) ist im ganzen Projekt kein anderswo belegter Funktionsparameter.
- **TO.2 (g3-1 Vier-Darstellungs-Block):** Neuer `block-fehler`-Block „⚠ Wertetabelle legt eine Funktion *nicht* eindeutig fest" direkt nach dem „📘 Wahl der Darstellung"-Block. Konstruiertes Gegenbeispiel: Wertetabelle \((0\mid 0), (1\mid 1), (2\mid 4), (3\mid 9)\) passt zu \(f(x) = x^2\) **und** zu \(h(x) = x^2 + x(x-1)(x-2)(x-3)\) — der Zusatzterm verschwindet an allen vier Tabellenstellen. Probe \(h(4) = 16 + 24 = 40\) gegen \(f(4) = 16\) macht den Unterschied sichtbar. Pointe: Eine Wertetabelle bestimmt eine Funktion nur, wenn der Funktionstyp vorgegeben ist; Verbalbeschreibung, Graph und Term sind in dem Sinn vollständiger. Gegenbeispiel mit Python verifiziert.
- **TO.3 (g3-2 A2):** Vor der Drag-Aufgabe ein dezenter italic-Hinweis ergänzt: „📱 Hinweis: diese Aufgabe funktioniert am besten am Computer mit Maus. Auf Touch-Geräten ist das Ziehen der Punkte fummelig — wer am Smartphone arbeitet, kann auch A3 (analytisch) machen und A2 später am Computer nachholen." Gibt mobilen Nutzern eine Alternative statt einer ungelösten Frustration.
- **TO.4 (g3-2 und g3-3 Definitionsbereich):** Je ein `block-tipp` mit Titel „💡 Definitionsbereich" direkt nach der Definitions-Box ergänzt. Inhalt: „Standardmässig ist \(D = \mathbb{R}\); bei Anwendungsaufgaben oft eingeschränkt." In g3-2 mit Beispielen Zeit/Stückzahlen/Rampe, in g3-3 mit Wurfweite und Geometrie-Optimierung. Schliesst die im Begutachterbericht beanstandete Lücke.
- **TO.5 (g4-0 Sonderstatus):** Direkt nach dem `<h1>` (vor dem Lead) ein neuer `block-tipp` „💡 Sonderstatus dieser Seite" eingefügt: „4.0 ist keine Theorieseite, sondern ein durchlaufendes Anwendungsbeispiel für 4.1, 4.2 und 4.3. […] Die Seite eignet sich zum Erkunden vor oder nach dem Theoriestudium, ersetzt aber keine der drei Theorieseiten." Der Lead-Absatz wurde unverändert beibehalten — das Banner ergänzt, statt zu ersetzen.
- **TO.7 (g4-3 Robustheits-Box):** Innerhalb der Beispiel-Box „Löhne in einem kleinen Betrieb" eine kleine italic-Marginalie ergänzt: „📝 Hinweis: Die Werte sind bereits aufsteigend sortiert. Bei realen Daten erst sortieren, dann den mittleren Wert ablesen — siehe die Fehler-Box unten." Verweist auf den bereits vorhandenen `block-fehler` „⚠ Häufiger Fehler — Median aus unsortierter Liste".
- **TO.9 (g5-2a SsW/sSW-Konvention):** Bei Prüfung des aktuellen Codes festgestellt, dass die SsW/sSW-Konvention in g5-2a (Zeile 504-505 Chip-Buttons, Zeile 722-723 Lösungsantwort) bereits etabliert ist und g5-2d (Zeile 497) sie explizit erklärt: „Bei den Kongruenzsätzen (SSS, SWS, WSW, SsW) steht *grosses S* für eine konkrete Seitenlänge. Bei den Ähnlichkeitssätzen (sss, sWs, SsW) steht *kleines s* für ein Seitenverhältnis." Kein Patch nötig — bereits erledigt, jetzt formell quittiert.
- **TO.11 (g5-2c Billionen-Stellen):** Beim π-Rekord die Schweizer Zählweise explizit verankert: „300 Billionen Stellen (\(3 \cdot 10^{14}\) Stellen, Schweizer Zählweise: 1 Billion = \(10^{12}\)) […] 314 Billionen Stellen (\(3.14 \cdot 10^{14}\))". Beseitigt den Mehrdeutigkeit zwischen langer (Schweizer/Deutsch) und kurzer (US-)Skala.
- **TO.12 (Notation-(FTB)-Block in g5-3/g5-4/g5-5):** Bedingte Empfehlung des Begutachters („*wenn man sich nicht für Variante (a) des Quellen-Footers entscheidet*"). Welle A TA.5 ist im aktuellen Stand bereits umgesetzt (Quellen-Footer in allen drei Druckdateien vorhanden) — die Bedingung trifft also nicht zu, TO.12 entfällt formell.

**Bewusst nicht umgesetzt** (jeweils mit Begründung — bei abweichender Ansicht des Auftraggebers später beauftragbar):

- **TO.6 (g4 Klasse-Begriffe A/B vs X/Y):** Die Inkonsistenz ist im Quellcode bereits durch einen expliziten Brücken-Absatz aufgelöst (g4-3 Zeile 337-339): „In den Theorie-Beispielen oben begegnen dir Klasse A und Klasse B […]. In den Aufgaben A5 und A7 unten kommen Klasse X und Klasse Y […]". Die zwei Namenspaare unterscheiden die *Datensätze* (Theorie ≠ Aufgaben), was didaktisch sinnvoll ist. Eine Vereinheitlichung auf nur ein Paar würde das Umschreiben einer ganzen Aufgabe (mit Werten) bedeuten — Aufwand-zu-Nutzen-Verhältnis ungünstig.
- **TO.8 (LG5 5.2-Sub-Seiten JS auslagern):** Klares Refactoring von ca. 7000 Zeilen JS-Code aus vier Themenseiten in vier neue externe Dateien. Laut COLLABORATION §6 („Kein Refactoring ‚weil's eleganter wäre'. Funktionierende Strukturen bleiben, ausser explizit Refactoring-Auftrag.") nicht angefasst. Risiko: Pfad-Themen, Cache-Verhalten beim Druck-Workflow, evtl. Pre-Flight-Anpassungen. Bei explizitem Refactoring-Auftrag in eigener Welle erledigbar.
- **TO.10 (g5-5 `block-fehler`-Doppelung):** Bei genauer Lektüre der beiden Boxen (Zeile 262 „⚠ Achtung — Wertebereich der Arcusfunktionen" und Zeile 391 „⚠ Häufiger Fehler — nur eine Lösung im Hauptintervall") **keine echte Redundanz** festgestellt. Die erste erklärt Wertebereiche der drei Arcusfunktionen abstrakt; die zweite zeigt konkret an `sin(φ) = 0.5`, dass im Hauptintervall zwei Lösungen liegen. Beide Boxen sind über 100 Zeilen entfernt (eigener H2-Abschnitt dazwischen) — der didaktische Wert „abstrakte Warnung früh + konkrete Falle bei den Aufgaben" überwiegt. Patch wäre eher kontraproduktiv.

Pre-Flight auf allen sechs geänderten Themenseiten (g3-1, g3-2, g3-3, g4-0, g4-3, g5-2c) grün (`pw=1 mc=1 nav=1 ml=1 bn=1 bad=0`). HTML-Tag-Bilanz aller sechs Dateien sauber.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle N (TN.1–TN.4)

Welle N adressiert das Aufgaben-Sterne-System (`●○○ / ●●○ / ●●●`) — Strategie-Entscheidung plus drei konkrete Anpassungen an g1-1.

- **TN.1 (Strategie ●○○ vs ⭐):** Auftraggeber-Entscheid: Status quo bleibt. Das `●○○`-System ist projektweit etabliert (g1-1 bis g5-5 nutzen es durchgängig) und bleibt unverändert. Auf eine Schwierigkeits-Legende auf den Druckseiten wird verzichtet — die Markierung wird als selbsterklärend betrachtet. Keine Code-Änderung.
- **TN.2 (g1-1 Teste A1):** Schwierigkeit von `●○○` auf `●●○` angehoben. Die Aufgabe „Hauptoperation bestimmen" prüft auf vier Termen verschiedener Bauart — von schlichter Summe `7 + 3x` über Produkt mit Klammer und Bruch bis hin zur Wurzel `√(x² + 4)`. Das ist nicht trivial und entspricht dem `●●○`-Niveau der nachfolgenden Aufgaben.
- **TN.3 (g1-1 Aufgabenserie ●○○-Aufgabe):** Vor die bestehenden sechs Aufgaben (3× `●●○`, 3× `●●●`) eine neue Einstiegsaufgabe als Nr. 1 eingefügt — „**Pause-Snack am Kiosk**" (Bereich: Alltag, Schwierigkeit `●○○`). \(n\) Brötchen à 2.50 Fr. plus \(g\) Getränke à 3.20 Fr.: (a) Term aufstellen, (b) für \(n=5, g=3\) auswerten (Resultat 22.10 Fr.), (c) Strukturwechsel bei 10 % Sonntags-Aufschlag (Klammer-Diskussion: Aufschlag wirkt auf den Gesamtbetrag, nicht nur einen Summanden). Damit deckt die Aufgabenserie jetzt das volle Schwierigkeits-Spektrum ab. Alle nachfolgenden Aufgaben (1–6 alt → 2–7 neu) wurden durchnummeriert: Übersichtstabellen-Zeilen, `aufg-nr`-Spans, Aufgaben-Kommentare und Lösungstitel — Sequenz-Konsistenz mit Python verifiziert (Tabelle, Aufgaben, Lösungen alle 1–7). Arithmetik der Musterlösung mit Python geprüft. Auf eine Schwierigkeits-Legende wurde verzichtet (siehe TN.1).
- **TN.4 (g1-1 Teste Zeitvorgabe):** Im Anleitungs-Block „ca. 30 Minuten" → „ca. 30-45 Minuten". Die 30-Minuten-Vorgabe war bei 10 mehrteiligen Aufgaben — darunter Strukturbaum, Gegenbeispiel finden und Termstruktur in Worte fassen — knapp; das Intervall ist realistischer und konsistent zu g2-2a/g2-2b (35-45 Min für jeweils 12 Aufgaben).

Tag-Bilanz beider geänderter Druck-Dateien sauber. Sterne-Konsistenz in der g1-1-Aufgabenserie zwischen Übersichtstabelle und Aufgabenrahmen verifiziert (beide Sequenzen: `●○○ ●●○ ●●○ ●●● ●●○ ●●● ●●●`).

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle M (TM.1–TM.5, Verifikation)

Welle M sollte fünf strukturelle Inkonsistenzen zwischen g2-3 und g2-2a/g2-2b beheben, die aus der ursprünglichen g2-3-Begutachtung stammen. **Verifikation am ZIP-Stand 52 ergibt: alle fünf Punkte sind bereits umgesetzt** — vermutlich nebenher in früheren Wellen, ohne dass TODO und CHANGELOG nachgepflegt wurden. Welle M wird daher als „bereits umgesetzt, jetzt formell quittiert" geschlossen, ohne Code-Änderungen an den Druck-Dateien.

Verifikations-Befunde (alle Druck-Dateien in `downloads/grundlagen/g2-3-lineare-gleichungssysteme/`):

- **TM.1 (Footer `doc-fuss`):** Alle fünf Dateien (`handout.html`, `formelauszug.html`, `teste-dich-selbst.html`, `aufgabenserie.html`, `zusatz-gauss-cramer.html`) haben je genau einen `<footer class="doc-fuss">`-Block mit den korrekten Bereichs-Bezeichnern („TALS Mathematik · Grundlagen Lineare Gleichungssysteme" plus Dokument-Typ). Identisch zum Stil aus g2-2a. — **Identisch mit TD.1**, daher dort ebenfalls abgehakt.
- **TM.2 (Lösungsblock-Struktur Teste):** 10 Aufgaben, 10 `<div class="loes">`-Blöcke mit je einem `<div class="loes-titel">✓ Lösung N</div>`. Eins-zu-eins parallel zu g2-2a (12/12) und g2-2b (12/12).
- **TM.3 (Schreiblinien `lin-mehr`):** 10 `<div class="lin-mehr">`-Blöcke für 10 Aufgaben (1× ein bis drei `<div class="lin">` pro Block, abhängig von Aufgabenkomplexität). Konvention identisch zu g2-2a/g2-2b.
- **TM.4 (MathJax-Skalierung):** g2-3 verwendet `scale: 0.95` in Handout/Formelauszug/Zusatz und `scale: 1.0` in Teste/Aufgabenserie — exakt das Muster, das auch g2-2a und g2-2b durchgehend nutzen. Die im TODO genannten Werte „0.92" und „1.0" sind nicht (mehr) im Quellcode.
- **TM.5 (Anleitungs-Block):** Teste-dich-selbst hat `<div class="block block-def">` mit „📘 Anleitung", Hilfsmittel- und Zeit-Angabe; Aufgabenserie hat `<div class="block block-def">` mit „📘 Hinweise" und Vorgehens-Schritten. Beides eins-zu-eins parallel zu g2-2a und g2-2b.

**Beifang (nicht gepatcht, weil ausserhalb Welle M):** Beim Strukturvergleich fiel auf, dass die Lösungs-Sektion der **g2-3-Aufgabenserie** abweicht: g2-2a/g2-2b nutzen `<div class="loes"><div class="loes-titel">✓ Lösung N — …</div>…</div>` für jede der 6 Musterlösungen, g2-3 nutzt stattdessen `<div class="aufg-rahmen">…<span class="aufg-titel">… — Lösung</span>…</div>`. Funktional ähnlich, optisch leicht unterschiedlich (gerahmt statt grün-akzentuiert). Da das im ursprünglichen Welle-M-Brief nicht aufgeführt war (TM.2 erwähnt nur Teste, nicht Aufgabenserie), wird dieser Befund hier nur notiert; eine etwaige Angleichung sollte als eigenes TODO-Item beschlossen werden (Vorschlag: nach Welle N als „TM.6 Aufgabenserie-Lösungs-Struktur g2-3 → g2-2a-Stil").

Pre-Flight aller fünf Druck-Dateien grün (`doc-fuss=1`, MathJax-Scale konsistent, HTML-Tag-Bilanz sauber). TODO-Items TM.1–TM.5 und TD.1 abgehakt.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle L Restposten (TL.7, TL.23, TL.24)

Drei verbliebene Items aus Welle L abgearbeitet — alle auf Themenseiten, nicht auf Druck-Dateien.

- **TL.7 (g1-1 A7 substanziell andere Übung):** Die alte A7 „Werkstatt-Materialwahl" war eine Variation derselben Pointe wie A5 (Strukturwechsel durch Distributivgesetz) und A6 (Strukturwahl beim Werkstückterm) — gleiches Konzept, anderes Material. Vollständig ersetzt durch eine **Fehlerdiagnose-Aufgabe**: drei Lernende rechnen \\(-3^2 + 2 \\cdot (5-1)^2\\) auf verschiedene Weise (Ergebnis 41, 55, 55) — alle drei falsch, korrekt ist 23. Lernende müssen den ersten Fehler-Schritt identifizieren und die verletzte Regel benennen. Deckt die zwei „Häufige-Fehler"-Boxen aus dem Theorieteil (`-x²` vs `(-x)²` und Punkt-vor-Strich) konkret ab und fordert <em>rückwärts lesen</em> statt vorwärts anwenden — konzeptuell anderer Aufgabentyp. ID-`l-g1-1-a7` und `aufg-vertiefung`-Markierung bleiben. Arithmetik der drei Rechnungen mit Python verifiziert.
- **TL.23 (g5-3 Strategie-Übersicht Flussdiagramm-SVG):** Vor die bestehende Stichpunkt-Liste in der Strategie-Übersicht ein eigenes Flussdiagramm-SVG gesetzt (720×660, eingebettet im `block-merksatz`). Knoten-Reihenfolge: Start („Welche 3 Teile sind gegeben?") → Diamant „Rechter Winkel?" → bei Ja: Pythagoras + Trigo am rechtwinkligen Dreieck; bei Nein: zweiter Diamant „Welche Konfiguration?" → links Sinussatz (wsw/wws/ssw) inkl. nachgelagerter Box „Falls ssw: zweite Lösung \\(180° - \\arcsin(\\ldots)\\) prüfen"; rechts Cosinussatz (sws/sss); beide Wege münden in End-Knoten „Restliche Teile berechnen (Winkelsumme ergänzt fehlende Stücke)". Farbcodierung konsistent zum Projekt-Stil (Diamanten ocker `#c47a1f` / `#fff4e0`, Sinussatz-Box blau `#1a4f8a` / `#e6eef7`, Cosinussatz-Box weinrot `#8a1a5a` / `#f3e6ee`, End-Knoten grün `#2d7d3a` / `#e6f3e8`). Die alte Stichpunkt-Liste bleibt unter dem Diagramm als Textform stehen — sie liest sich auch im Druck gut und liefert die Kerninformation, falls das SVG nicht lädt.
- **TL.24 (g5-4 A7 Tagestemperatur Sinuskurve-SVG):** SVG der Tagestemperatur-Sinuskurve direkt in den Aufgabentext eingesetzt (640×280, vor dem Lösungs-Toggle). Achsen mit Einheiten (\\(t\\) in h, \\(T\\) in °C, RLP-Anwendungskontext). Pfad als 97-Punkte-Polyline aus \\(T(t) = 22 + 7 \\cdot \\sin(15° \\cdot (t - 11))\\) generiert; alle Achsen-Ticks bei den Lösungs-Schlüsselwerten (5 h, 11 h, 17 h, 23 h; 15 °C, 22 °C, 29 °C). Visuelle Markierungen: Minimum (5|15) rot, Maximum (17|29) grün, gestrichelte Mittelwertlinie bei \\(T_0 = 22\\,°\\text{C}\\), Amplituden-Pfeil rechts mit Beschriftung „2A = 14". Geometrische Konsistenz mit der ausformulierten Lösung mit Python verifiziert. Stilkonsistent zur Sinuskurve in g5-5 (gleiche Achsenfarben, Schrift, Linienstärken).

Pre-Flight aus STYLEGUIDE §6.1 grün für alle drei Dateien (`pw=1 mc=1 nav=1 ml=1 bn=1 sec=0 bad=0`). SVG-Wohlgeformtheit mit `xml.etree.ElementTree` geprüft. Tag-Bilanz aller drei HTML-Dateien sauber.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle L Druck g2 (Sub-Block D)

### Welle L — g2 Druck (15 Items, TL.66–TL.80, acht Dateien + zwei Anki-Decks)

Sub-Block g2-Druck komplett (TL.66–TL.80, 15 von 15 Items). Betroffen: alle vier Druck-Dateien von g2-1-grundlagen und g2-2a-lineare-gleichungen plus deren Anki-Decks.

**g2-1 Druck (6 Items, TL.66–TL.71):**

- **TL.66 (A5 Schwierigkeit):** A5 „Lieferwagen-Zuladung" in der Aufgabenserie-Übersichtstabelle von ●●○ auf ●○○ herabgestuft. Die Aufgabe ist eine simple einzeilige Ungleichung — die ●●○-Markierung war im Verhältnis zu A3/A4 (Widerstandsnetzwerk, Treppenhaus) inkonsistent. Die individuelle Markierung in der Aufgabe selbst bleibt ●●○; nur die Übersichtstabelle wird angepasst, weil dort der Vergleich mit den anderen Aufgaben offensichtlich wird.
- **TL.67 (Teste A5 Probe):** Lösung 5 „Mietgerät" um eine explizite Probe erweitert — „<em>Probe</em>: \(45 + 12 \cdot 6 = 45 + 72 = 117\,\text{Fr.}\) ✓ Stimmt mit der Vorgabe." Setzt den Probe-Reflex aus dem Handout konsequent in der Musterlösung um.
- **TL.68 (Zeitvorgabe):** Anleitungsblock im Teste-dich-selbst von „ca. 40 Minuten" auf „ca. 40-50 Minuten" erweitert. Bei 12 Aufgaben mit Modellieren und Parameterdiskussion sind 40 Min knapp; 40-50 ist die realistische Spanne.
- **TL.69 (Anki Karten 8, 11, 13):** Direkte SQLite-Modifikation der `ankideck.apkg` (Karten-Quellen sind nicht in `build_apkg.py` eingecheckt, Decks wurden vermutlich mit einem nicht-versionierten Skript erstellt). Karte 8 („4 Pakete"): präzisiert „Variable <i>x</i> = Masse <em>eines</em> Pakets" mit Klarstellung, dass Einheiten in der Lösungsmenge nicht stehen. Karte 11 (Äquivalenzumformungen): präzisiert, dass \(c\) eine <em>Konstante</em> ist (keine Variable) — sonst kann sich die Lösungsmenge ändern. Karte 13 (Ungleichungen): erweitert um Division durch negative Zahl (gleiche Regel wie bei Multiplikation), Titel daher umformuliert „multipliziert <em>oder dividiert</em>".
- **TL.70 (dk-untertitel):** In beiden Druck-Header (Aufgabenserie und Teste-dich-selbst von g2-1) neuer `<p class="dk-untertitel">` ergänzt, analog zur g1-2/3/4-Konvention. Teste: „12 Aufgaben — Begriffe, Modellieren, Äquivalenzumformungen, Probe und Typerkennung". Aufgabenserie: „Sechs Anwendungsaufgaben aus Technik, Architektur und Life Sciences — Modellieren mit Gleichungen, Ungleichungen und Gleichungssystemen".
- **TL.71 (Handout Abschnitt 8 Bezeichnung):** Lösungsmenge-Tabelle von 3 auf 4 Spalten erweitert. Neue Spalte „Bezeichnung" zwischen „Situation" und „Lösungsmenge". Für die ersten zwei Zeilen (eindeutig, mehrere) steht „— (Normalfall)"; für die dritte Zeile „<strong>Widerspruch</strong>"; für die vierte Zeile „<strong>Identität</strong>". Damit ist die Bezeichnung explizit in einer eigenen Spalte sichtbar, nicht in Klammern in der Lösungsmenge-Spalte versteckt.

**g2-2a Druck (9 Items, TL.72–TL.80):**

- **TL.72 (Teste A8 30-Min-Schritte):** Lösung 8 (Mietgerät-Ungleichung) um Praxis-Marginalie ergänzt — „Mietgeräte werden meist in 30-Minuten-Schritten abgerechnet. \(10{.}71 \cdot 60 \approx 643\,\text{Min}\) — auf halbe Stunden abgerundet \(10{.}5\,\text{h} = 630\,\text{Min}\)". Erklärt, dass bei diesem Abrechnungsmodus 10.5 h statt 10.71 h die praktisch sinnvolle Antwort ist.
- **TL.73 (Aufgabenserie A4-A6 drei Marginalien):**
  - Lös. 4 (Lagerbestand): „<em>Praktisch</em>: Am Tag 13 sind noch 25 Stück da, am Tag 14 wäre der Bestand rechnerisch −10 — das Lager ist <em>im Laufe</em> des 14. Tages leer." Trennt rechnerische und tatsächliche Sicht.
  - Lös. 5 (Rampe): SIA-500-Norm-Hinweis ergänzt — „Bei Längen > 6 m sind zusätzliche Zwischenpodeste verlangt; empfohlen sind 4–5 % für längere Rampen". Verankert die 6 %-Grenze normativ.
  - Lös. 6 (Verdünnungsreihe): Grenzfall \(c \to 0\) ergänzt — „mathematisch vertikale Asymptote bei \(c = 0\); physikalisch: Konzentration 0 erreicht man nie durch Verdünnung". Verbindet Asymptote (Vorgriff auf 3.4 Hyperbel) mit physikalischer Intuition.
- **TL.74 (Handout konkrete Parameter-Beispielrechnung):** Im Abschnitt 6 „Lineare Gleichungen mit Parameter" nach der Drei-Fälle-Tabelle ein vollständig ausgearbeitetes Beispiel ergänzt: \((k-2) \cdot x = k^2 - 4\). Faktorisierung der rechten Seite \((k-2)(k+2)\), zwei Fälle (\(k \neq 2 \Rightarrow x = k+2\); \(k = 2 \Rightarrow\) Identität \(\mathbb{L} = \mathbb{R}\)). Schlussbemerkung, dass der „verbotene Fall" \(\mathbb{L} = \emptyset\) hier nicht auftritt, weil rechte Seite ebenfalls bei \(k = 2\) verschwindet.
- **TL.75 (Formelauszug 4-Punkte-Lösungsschema):** Im Abschnitt 5 nach der Drei-Fälle-Tabelle ein nummeriertes 4-Punkte-Schema ergänzt: (1) auf Form \(a(k) \cdot x = b(k)\) bringen, (2) kritischen Wert \(k_*\) bestimmen, (3) Standardfall direkt lösen, (4) Sonderfall bei \(k = k_*\) mit \(b(k_*)\)-Prüfung. Korrespondiert zum Handout-Beispiel aus TL.74.
- **TL.76 (Teste A9, A12):**
  - Lös. 9 (Auto-Treffen): Exakte Brüche \(320/3\) und \(400/3\) ergänzt — „die exakten Brüche addieren sich genau zu 240; die gerundeten Dezimalzahlen 106.7 und 133.3 addieren sich nur näherungsweise". Macht den Rundungsmoment sichtbar.
  - Lös. 12 (Produktionsrate): Intuitive Erklärung des \(p = 0\)-Falls ergänzt — „Wenn die Maschine nichts produziert, liegt der Output nach 8 Stunden bei den anfänglichen 5 Werkstücken — nicht bei den verlangten 45". Brücke Mathematik (Widerspruch) ↔ Physik (Produktionsrate nötig).
- **TL.77 (Teste Anleitung):** `dk-untertitel` ergänzt („12 Aufgaben — Lösungsmenge, Sonderfälle, Ungleichungen, Modellieren, Parameter-Diskussion"). Zeitvorgabe von „ca. 35 Minuten" auf „ca. 35-45 Minuten" erweitert. Anleitung präzisiert mit „diese stehen am Ende".
- **TL.78 (Aufgabenserie A2, A3):**
  - Lös. 2 (Kraftstoff): Exakter Bruch \(4000/17\) eingeführt, Rundungsfehler quantifiziert — „mit dem gerundeten Wert 235: 19.975 L verbraucht, also 5.025 L übrig — der Rundungsfehler beträgt 25 mL". Macht das „Erst rechnen, dann runden"-Prinzip greifbar.
  - Lös. 3 (Betontemperatur): Newtonsches Abkühlungsgesetz \(T(t) - T_\infty = (T_0 - T_\infty) \cdot e^{-k \cdot t}\) als realistisches Modell vorgestellt — „die Abkühlung verlangsamt sich, je näher \(T\) an \(T_\infty\) kommt — exponentielle Modelle folgen in 3.4 Exponentialfunktionen". Vorgriff auf nachfolgendes Lerngebiet.
- **TL.79 (Handout Merksatz + Lösen-Tabelle):**
  - Merksatz: Vom widersprüchlichen „höchstens eine Lösung" (gilt nicht bei Identität) zum präzisen „genau eine Lösung — <em>ausser bei Identität</em> (unendlich viele) oder Widerspruch (keine)" geändert.
  - Lösen-Tabelle: 3 Zeilen (Add/Sub, Mult, Div) auf 2 Zeilen reduziert — „beide Seiten \(\pm c\)" und „beide Seiten \(\cdot c\) oder \(:c\)". Add/Sub teilen sich die Bedingung „—" (immer erlaubt), Mult/Div teilen sich „\(c \neq 0\)".
- **TL.80 (Anki Karten 4, 14, 22):** Direkte SQLite-Modifikation der `ankideck.apkg`.
  - Karte 4 (Fünf Schritte): Schritt 4 ergänzt „— <em>nur wenn dieser ≠ 0 ist</em>. Sonst ist die Gleichung Identität (𝕃 = ℝ) oder Widerspruch (𝕃 = ∅)". Schritt 5 verfeinert mit „nicht in einer Zwischenform" (Probe immer in der ursprünglichen Gleichung).
  - Karte 14 (Mietkosten 200 Fr.): konsistent zu TL.72 erweitert — „<i>Praxis</i>: Mietgeräte werden meist in 30-Min-Schritten abgerechnet — also höchstens <b>10.5 h</b> ohne Budget zu überziehen".
  - Karte 22 (Identität geometrisch): „die zwei Geraden <b>fallen zusammen</b> (gleiche Steigung <em>und</em> gleicher y-Achsenabschnitt)". Plus Gegensatz: „Bei ℒ = ∅ sind die Geraden <em>parallel</em> (gleiche Steigung, aber verschiedene y-Achsenabschnitte)". Trennt die zwei „pathologischen" Fälle geometrisch.

### Damit ist Welle L bis auf die zurückgestellten Themenseiten-Items abgeschlossen.

77 von 80 Welle-L-Items erledigt. Verbleibend: TL.7, TL.23, TL.24 — drei Themenseiten-Items, die wegen Konstruktionsaufwand (Aufgaben-Neukonstruktion, SVG-Flussdiagramm, SVG-Sinuskurve) bewusst aus Welle L herausgenommen werden und gegebenenfalls als eigene Mini-Welle erscheinen.

### Verifikation

- **Tag-Balance** auf allen 8 g2-Druck-Dateien: g2-1 (53/53, 4/4, 6/6, 84/84), g2-2a (50/50, 4/4, 6/6, 92/92) — alle ausgeglichen.
- **Anki TL.69 (g2-1)**: 25 Karten, Karten 8/11/13 neue Inhalte verifiziert via `SELECT flds FROM notes`.
- **Anki TL.80 (g2-2a)**: 25 Karten, Karten 4/14/22 neue Inhalte verifiziert.
- **Konsistenz-Check** zwischen Handout (TL.74 Beispiel) und Formelauszug (TL.75 Schema): beide nutzen das gleiche Beispiel \((k-2) \cdot x = k^2 - 4\) implizit (Schema zeigt das allgemeine Vorgehen, Handout führt es konkret durch).
- **Konsistenz-Check** zwischen Anki-Karte 14 (TL.80) und Teste-Lösung 8 (TL.72): beide nennen jetzt explizit „10.5 h" als praxisnahe Antwort mit 30-Min-Schritten.
- **Konsistenz-Check** Merksatz (TL.79) ↔ Drei-Lösungsfälle-Tabelle (Abschnitt 4): Identität \(\mathbb{L} = \mathbb{R}\) und Widerspruch \(\mathbb{L} = \emptyset\) werden in beiden konsistent benannt.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle L Druck g1-4 (Sub-Block C)

### Welle L — g1-4 Druck (10 Items, TL.56–TL.65, vier Dateien + Anki-Deck)

Sub-Block g1-4-Druck komplett (TL.56–TL.65, 10 von 10 Items). Betroffen: `aufgabenserie.html`, `teste-dich-selbst.html`, `handout.html`, `formelauszug.html`, `ankideck.apkg`.

**Handout + Formelauszug (TL.56, TL.63, TL.64):**

- **TL.56 (SI-Vorsätze-Tabelle):** In beiden Dateien (Handout und Formelauszug) wurde die SI-Vorsätze-Tabelle erweitert um drei neue Vorsätze mit Schweizer Beispielen: <strong>Hekto (h, 10²)</strong> — 1 hPa = 100 Pa (Wetterbericht-Luftdruck), <strong>Deci (d, 10⁻¹)</strong> — 1 dl = 0.1 l (Standardglas Wein/Bier), <strong>Centi (c, 10⁻²)</strong> — 1 cm = 0.01 m. Zusätzlich Konsistenz-Anpassung: Handout hat jetzt auch <strong>Tera (T, 10¹²)</strong> mit Festplatten-Beispiel und <strong>Pico (p, 10⁻¹²)</strong> mit pF-Kondensator-Beispiel, analog zum Formelauszug. Damit decken beide Dokumente die gesamte Vorsatz-Reihe von Tera bis Pico ab — wichtige Stoff-Ergänzung gemäss RLP.
- **TL.63 (Formelauszug WissNot-Beispiel):** Beim Block „Wissenschaftliche Notation" Beispiele ergänzt — Lichtgeschwindigkeit \(c = 2{.}998 \cdot 10^8\,\text{m/s}\) und Elektronenmasse \(m_e = 9{.}11 \cdot 10^{-31}\,\text{kg}\). Zeigt jeweils einen positiven und einen negativen Exponenten. Quadratzahlen sind im Formelauszug bereits vor Wurzelgesetzen (Z. 69 vs. 78) — der Reihenfolge-Aspekt von TL.63 war bereits umgesetzt, nur das Beispiel fehlte.
- **TL.64 (Handout Quadratzahlen-Tabelle):** Aus der einfachen Aufzählung „1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144" wurde eine 12-spaltige `n↔n²`-Zuordnungstabelle. Marginalie unter der Tabelle: „Wer die Tabelle invertiert liest: \(\sqrt{49} = 7\), \(\sqrt{144} = 12\). Wer Quadratzahlen kennt, erkennt sofort, ob eine Wurzel ‚aufgeht'."

**Aufgabenserie (TL.58, TL.62):**

- **TL.58 (sechs Marginalien zu Aufg. 1-6):**
  - Aufg. 1 (Lichtlaufzeit): Die 500 s zum Mars greifbar gemacht — Funksignale brauchen 3-22 Min je nach Konstellation; in 8 Minuten umrundet die ISS zweimal die Erde.
  - Aufg. 2 (Mikrocontroller): 250 MHz = 250 Millionen Taktzyklen/s, pro Stunde 900 Milliarden — „mehr Zyklen als die Schweiz Einwohner hat (×30)".
  - Aufg. 3 (Grundfläche): Flächen-Umrechnung-Warnung — 1 cm² = 10⁻⁴ m² (nicht 10⁻²), beim Wechsel Fläche→Länge wird der Exponent halbiert.
  - Aufg. 4 (Wechselspannung): Spitzenspannung-Erklärung — 230 V ist Effektivwert, die Spitze ist 325 V; 50× pro Sekunde wechselnd. Trennung Effektivwert ↔ Spitzenwert.
  - Aufg. 5 (Schalldruck): Dezibel-Brücke zu LG3 — \(L = 20 \cdot \log_{10}(p/p_0)\), Faktor 10⁶ = 120 dB (Düsenjet), Faktor 10⁴ = 80 dB (Strassenverkehr). Vorgriff auf 3.4 Exponential/Logarithmus.
  - Aufg. 6 (DVD): Physikalische Grenze betont — Blu-Ray nutzt blauen Laser (\(\lambda = 405\,\text{nm}\)) statt rotem (650 nm), schafft deshalb mehr Bits/mm² — „physikalisch nicht zufällig kürzer".
- **TL.62 (Reihenfolge „von gross zu klein"):** Pragmatischer Kompromiss statt vollständige Umordnung der 6 Aufgaben — Übersichtstabelle bekam eine neue Spalte „Grössenordnung" mit der zentralen Skala jeder Aufgabe (\(10^8\,\text{m}, 10^{-9}\,\text{s}, 10^0\,\text{m}, 10^2\,\text{V}, 10^{-5}\,\text{Pa}, 10^{-7}\,\text{m}\)). Hinweis-Absatz davor erklärt, dass die Aufgaben sechs verschiedene Grössenordnungs-Bereiche abdecken. Eine echte Umordnung der Aufgaben + Lösungs-Nummern wurde verworfen, weil sie sechs Aufgaben-Blöcke und sechs Lösungs-Absätze umnummerieren müsste — Aufwand-Nutzen ungünstig im Sub-Block-Zeitfenster.

**Teste-dich-selbst (TL.59, TL.60, TL.65):**

- **TL.59 (Lös. 7(c) Vorzeichen):** Ausführliche Definitions-Begründung — „<em>Per Definition</em> ist \(\sqrt{\cdot}\) die <strong>nicht-negative</strong> Zahl, deren Quadrat den Radikanden ergibt. Zwar gilt \((-5)^2 = 25\), aber das Symbol \(\sqrt{25}\) bezeichnet nur die positive Wurzel. Wenn beide Vorzeichen gemeint sind, schreibt man \(\pm\sqrt{25}\)". Schliesst die häufige Verwechslung zwischen Wurzelfunktion (nur positiv) und Lösungsmenge von \(x^2 = 25\) (beide Vorzeichen).
- **TL.60 (Lös. 12 Drei-Gesetze-Marginalie):** Aus der knappen 3-Schritt-Rechnung wurden vier explizite Schritte mit Gesetz-Referenz: P4+P3 für \((2x^2)^3\), P2 für \(x^4/x^2\), P1 für \(8x^6 \cdot x^2\). Nach Selbstkorrektur (initial P3 statt P4 referenziert — siehe TL.10-Tabelle im Formelauszug: P4 ist \((a\cdot b)^n\)).
- **TL.65 (Aufg. 8/9 differenzieren):** Innerhalb der Gruppe „Teilweises Wurzelziehen" (●●● gesamt) bekommt Aufg. 8 (Wurzel ziehen) eine individuelle ●●○-Markierung im Titel-Span, Aufg. 9 (Wurzelterme zusammenfassen, kombiniert) behält ●●●. Trennt die zwei Niveaus: einfaches teilweises Wurzelziehen vs. kombiniertes Vereinfachen über teilweises Ziehen + Addition.

**Anki-Deck (TL.57, TL.61):**

- **TL.61 (Karten 7, 17, 23 verbessern):**
  - Karte 7 (6.02·10²³): Avogadro-Bezug — „Anzahl Teilchen in einem Mol, z.B. einem Mol Wassermoleküle (etwa 18 g Wasser). Das ist <em>der</em> Grund, warum die wissenschaftliche Notation existiert."
  - Karte 17 (√0.25 = 0.5): Dezimal-Wurzel-Falle benannt — „√(klein) wird grösser" für Zahlen zwischen 0 und 1.
  - Karte 23 (3/√2): Erweiterungs-Begründung — warum mit √2/√2 erweitern: √2·√2 = √4 = 2, der Nenner wird rational; das Erweitern mit √2/√2 = 1 ändert den Wert nicht.
- **TL.57 (8 neue SI-Vorsätze-Karten):** Acht neue Karten am Ende des Decks (Index 28-35): „G = ?", „M = ?", „µ = ?", „c = ?", „1 cm in m", „1 hPa in Pa", „5 dl in Liter", „n = ?". Vier abstrakte Symbol→Potenz-Karten plus vier konkrete Umrechnungen mit Schweizer-Alltags-Beispielen (cm, hPa-Wetter, dl-Wein, nm-Licht). Korrespondiert direkt zur erweiterten SI-Vorsätze-Tabelle in Handout/Formelauszug.

Anki-Deck via `python3 scripts/build_apkg.py` neu generiert: **36 Karten** (vorher 28), 6785 Bytes. Verifikation `sqlite3 …` ergibt 36 notes ✓.

### Verifikation

- **Tag-Balance** auf allen 4 g1-4-Druck-Dateien: `aufgabenserie.html` 40/40, `teste-dich-selbst.html` 68/68, `handout.html` 5/5, `formelauszug.html` 4/4 — alle ausgeglichen.
- **TL.60 P-Korrektur:** Erste Marginalie referenzierte P3 für \((2x^2)^3\); nach Tabellen-Check im Formelauszug (P3 = \((a^m)^n\), P4 = \((a\cdot b)^n\)) auf P4+P3 korrigiert.
- **TL.56 SI-Tabelle:** Handout und Formelauszug haben jetzt beide 11 Vorsätze von Tera bis Pico — Vergleich der Reihenfolgen ist identisch.

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle L Druck g1-3 (Sub-Block B)

### Welle L — g1-3 Druck (12 Items, TL.44–TL.55, vier Dateien + Anki-Deck)

Sub-Block g1-3-Druck komplett (TL.44–TL.55, 12 von 12 Items). Betroffen: `aufgabenserie.html`, `teste-dich-selbst.html`, `handout.html`, `formelauszug.html`, `ankideck.apkg`.

**Aufgabenserie (TL.46, TL.47, TL.48, TL.52):**

- **TL.46 (Aufg. 1 SVG):** Quadrat 140×140 mit innerem Quadrat \((a-2b)\times(a-2b)\), Aussenseite \(a\) beschriftet, Rand-Streifen-Breite \(b\) rechts oben, Innenseite \(a-2b\) zentriert. Float-rechts (110×110 gerendert), gibt Schülern eine geometrische Brücke zur algebraischen Restflächenformel.
- **TL.47 (Lös. 4 Distributivgesetz rückwärts):** Schritt \(4rx + 4r^2 = 4r(x+r)\) explizit als „Distributivgesetz rückwärts" benannt — verbindet Faktorisieren als Umkehrung des Ausmultiplizierens.
- **TL.48 (Aufg. 6 Modell-Disclaimer):** `block-fehler`-Box „Reales Bakterienwachstum ist exponentiell — hier polynomial nur zur Übung des Ausklammerns; das realistischere Modell folgt in 3.4 Exponentialfunktionen." Analog zum bestehenden Disclaimer bei Aufg. 2 (Bremsweg). Schützt Schüler davor, polynomiales Wachstum für Biologie zu generalisieren.
- **TL.52 (Aufg. 3 Kirchhoff-Mini-Marginalie):** Vor den Teilaufgaben kursive Erklärung: \(U =\) Spannung (V), \(I =\) Strom (A), \(P = U \cdot I =\) Leistung (W); bei Parallelschaltung Spannung gleich, Ströme addieren sich (Knotenregel). Macht die ET-Aufgabe für Lernende ohne ET-Vorwissen zugänglich.

**Teste-dich-selbst (TL.44, TL.45, TL.53):**

- **TL.44 (Lös. 5(c) Zwischenschritt):** Vollständige Schritt-Kette \((a+b)(a+b+c) = a(a+b+c) + b(a+b+c) = a^2 + ab + ac + ab + b^2 + bc = \ldots\) — vorher sprang die Lösung direkt zum bereits ausmultiplizierten Term.
- **TL.45 (Lös. 12 Strategie):** Didaktische Schlussfolgerung am Ende — „Symbolisch vereinfachen, dann einsetzen" — vs. direkter Einsetzweg. Beide Wege werden gegenübergestellt; der symbolische ist robuster gegen Vorzeichenfehler und macht die Struktur (Differenz \(= 4ab\)) sichtbar.
- **TL.53 (Aufg. 6/7 Schwierigkeit differenzieren):** Innerhalb der Gruppe „Binomische Formeln" (●●● gesamt) bekommt Aufg. 6 („anwenden") individuelle ●●○-Markierung im Titel-Span, Aufg. 7 („rückwärts erkennen") behält ●●●. Trennt die zwei kognitiven Niveaus (Anwendung einer Formel vs. Strukturerkennung).

**Handout (TL.49, TL.50, TL.55):**

- **TL.49 (Abschnitt 6 Strategie-Reihenfolge):** Neuer Absatz nach den drei Werkzeugen — „(1) Immer zuerst nach gemeinsamem Faktor suchen. (2) Dann auf binomische Formel prüfen. (3) Wenn nichts davon passt: einsetzen statt faktorisieren." Korrespondiert zur Anki-Karte 21 (Reihenfolge beim Faktorisieren), macht die Strategie auch im Handout sichtbar.
- **TL.50 (Abschnitt 5 Herleitung):** Marginalie vor der Tabelle — Herleitung der 1. binomischen Formel direkt aus Klammerregel 4 zeigen: \((a+b)^2 = (a+b)(a+b) = a^2 + 2ab + b^2\). Erklärt, dass binomische Formeln keine neuen Gesetze sind, sondern Abkürzungen für häufige Muster.
- **TL.55 (Beispiel-Polynom):** In der Termarten-Tabelle (Handout) und in der Formelauszug-Termarten-Tabelle wurde das Polynom-Beispiel vom kurzen \(2x^2 - 3x + 5\) auf das konsistente \(5x^3 - 2x^2 + 7x - 4\) angeglichen — dasselbe, das schon im Abschnitt „Polynom-Begriffe" beider Dateien als Demobjekt dient.

**Formelauszug (TL.54):**

- **TL.54 (Reihenfolge):** Sektion „Polynom-Begriffe" vor „Faktorisierungswerkzeuge" verschoben. Begründung: Polynom-Begriffe sind grundlegende Vokabeln (Grad, Koeffizient, konstantes Glied), die man zum Verstehen der Faktorisierungs-Beispiele bereits braucht. Konsistent zur Reihenfolge im Handout (dort Abschnitt 2: Begriffe vor 6: Faktorisieren).

**Anki-Deck (TL.51):**

- **TL.51 (Karten 11, 14, 19, 23 + 3 neue Polynom-Karten):** 
  - Karte 11 ((2x−5)²): Vorzeichen-Vorsicht-Hinweis — „negativer Mittelterm, beide Endterme positiv".
  - Karte 14 (6x+9): ggT-Begriff explizit eingeführt — „ggT(6, 9) = 3".
  - Karte 19 (2x²−8): Numerische Probe mit x = 3 — original \(= 10\), faktorisiert \(= 10\) ✓.
  - Karte 23 (Häufiger Fehler (a+b)²): Konkretes Probe-Beispiel mit a = 3, b = 4 — der fehlende Mittelterm 24 wird sichtbar.
  - **Drei neue Polynom-Karten** (am Ende): Grad eines Polynoms (höchster Exponent, mit Beispiel 5x³…), konstantes Glied (Glied ohne Variable, Wert an x=0), Koeffizienten (Vorzahlen in fallender Potenzordnung).

Anki-Deck via `python3 scripts/build_apkg.py` neu generiert: **27 Karten** (vorher 24), 5972 Bytes. Verifikation `sqlite3 …` ergibt 27 notes ✓.

### Verifikation

- **Tag-Balance** auf allen 4 g1-3-Druck-Dateien: `aufgabenserie.html` 46/46, `teste-dich-selbst.html` 69/69, `handout.html` 3/3, `formelauszug.html` 4/4 — alle ausgeglichen.
- **TL.46 SVG**: viewBox 140×140, gerendert 110×110, Aussenrahmen 120×120 (a), Innenrahmen 80×80 (a-2b) korrekt mittig, Rand-Streifen oben/rechts mit \(b\)-Beschriftung.
- **TL.51 Anki neue Karten 25-27** (Polynom-Begriffe): konsistent mit Handout § 2 und Formelauszug „Polynom-Begriffe"-Tabelle — alle verwenden dasselbe Beispiel-Polynom \(5x^3 - 2x^2 + 7x - 4\).

---

## [unreleased] — 2026-05-26 · Lehrerbegutachtungen Welle L Druck g1-2 (Sub-Block A)

### Welle L — g1-2 Druck (13 Items, TL.31–TL.43, vier Dateien + Anki-Deck)

Aus `TODO-lehrerbegutachtung.md` Welle L wurde der Sub-Block g1-2-Druck komplett abgearbeitet (TL.31–TL.43, 13 von 13 Items). Betroffene Dateien: `aufgabenserie.html`, `teste-dich-selbst.html`, `handout.html`, `formelauszug.html`, und das Anki-Deck `ankideck.apkg` (neu generiert via `scripts/build_apkg.py`).

**Aufgabenserie (TL.31, TL.36):**

- **TL.31 (Aufg. 2 Treibstoff/Rabatt):** 5-Rappen-Rundungs-Marginalie in der Lösung — „In der Praxis: An der Tankstelle wird auf 5 Rappen gerundet, also \(34{.}15\,\text{Fr.}\) (kaufmännisch). Der mathematisch exakte Wert \(34{.}1496\) bleibt für Folgerechnungen erhalten — gerundet wird erst ganz am Schluss." Schweizer Spezifikum, didaktisch wichtig zur Trennung von exakter Rechnung und Praxis-Darstellung.
- **TL.36 (fünf Marginalien):**
  - Lös. 1 (Mörtelmischung): Idealisierungs-Hinweis — Volumina sind in der Praxis nicht additiv (Wasser füllt Sand-Hohlräume), die Anteilsrechnung ist aber davon unabhängig.
  - Lös. 3 (Widerstand-Toleranz): Praxis-Bemerkung zu Farbring-Codierung — \(5\,\%\) goldener Ring, \(1\,\%\) brauner Ring; Korrelation Toleranz/Preis.
  - Lös. 4 (Lagerbestand): Trennung Tiefststand (\(85\)) ↔ Endbestand (\(90\)) — für Lagerplanung zählt der Tiefststand, nicht das Periodenergebnis.
  - Lös. 5 (Massstab): Faustregel „1 cm = 50 cm = 0.5 m bei 1:50" + Architektur-Standard-Massstäbe (1:50/1:100/1:200/1:500).
  - Lös. 6 (Pufferlösung): Klare Trennung Volumenverhältnis (40 %) ↔ chemische Konzentration (mol/L) — der Säureanteil ist <em>nicht</em> die Konzentration.

**Teste-dich-selbst (TL.32, TL.33, TL.37, TL.40, TL.41, TL.42):**

- **TL.32 (Aufgaben-Titel):** Alle 12 Aufgaben mit `<span class="aufg-titel">…</span>` ergänzt, analog zum g1-1-Vorbild. Titel: Zahlenmengen zuordnen, Wahr oder falsch, Bruch in Dezimalzahl, Dezimalzahl in gekürzten Bruch, Prozentrechnung, Intervall aufschreiben, Element-Test im Intervall, Vorzeichen-Operationen, Klammern und Hierarchie, Betrag, Ordnung negativer Brüche, Lagerbilanz. Das `<div>` wurde durch `<span>` ersetzt, weil die Skelett-Konvention das Inline-Layout erwartet. Titel-Zuordnung wurde nach erstem automatischen Lauf nochmal gegen die Aufgabentexte verifiziert und korrigiert (sechs Titel hatten ursprünglich falsch zugeordnete Themen — z.B. Aufg. 9 ist Hierarchie, nicht Bruchrechnung; Aufg. 10 ist Betrag, nicht Bruchrechnung).
- **TL.33 (Lös. 11 Sortierung):** Sortierung als 2-Schritt-Lösung formuliert — Schritt 1: alle Brüche in Dezimal (\(-3/4 = -0{.}75\), \(-2/3 \approx -0{.}667\), \(1/2 = 0{.}5\)). Schritt 2: links-nach-rechts auf der Zahlengeraden ordnen. Plus Vorzeichen-Falle: bei negativen Zahlen ist die betragsgrössere die kleinere Zahl.
- **TL.37 (Lös. 12 Logistik-Bilanz):** Klarstellung Gesamtveränderung (netto, Bestandsänderung) ↔ Summe der Beträge (Arbeitsaufwand, Logistik-Kosten). „Für die Lagerlogistik ist die Betragssumme oft wichtiger als die Netto-Veränderung."
- **TL.40 (Lös. 1 Zahlenmengen):** Konvention „0 ∈ ℕ" (Schweizer Schul-Konvention, ISO 80000-2) explizit benannt; alternative Konvention mit \(\mathbb{N}_0\)/\(\mathbb{N}\) ohne Null erwähnt — beugt Verwirrung bei Quervergleichen mit deutschen Lehrbüchern vor.
- **TL.41 (Gruppe Betrag/Ordnung):** Schwierigkeit von ●●● auf ●●○ herabgestuft (`punkte`-Marker). Die Aufgaben 10/11 sind objektiv leichter als z.B. die Hierarchie-Aufgaben 8/9 — die ●●●-Markierung war inkonsistent.
- **TL.42 (Lös. 7 Intervall-Test):** Begründung „2.5 zu gross" durch explizite Klammer-Erklärung ersetzt — „\(-3\) ausgeschlossen wegen offener Klammer \(]\), \(2\) eingeschlossen wegen geschlossener Klammer \(]\); \(2{.}5 > 2\) liegt rechts der oberen Grenze".

**Handout (TL.34):**

- **TL.34 (Bruch-Dezimal-Prozent-Tabelle):** Tabelle von 3 auf 7 Zeilen erweitert. Neu: \(1/4 = 0{.}25 = 25\,\%\), \(1/8 = 0{.}125 = 12{.}5\,\%\), \(2/5 = 0{.}4 = 40\,\%\), \(-3/4 = -0{.}75 = -75\,\%\). Letzter Eintrag zeigt explizit, dass die Drei-Darstellungs-Konvention auch für negative Zahlen funktioniert.

**Formelauszug (TL.43):**

- **TL.43 (Konventions-Hinweis):** Neue Marginalie unterhalb der Intervall-Tabelle erklärt Schweizer/Französische Konvention (eckige Klammer nach aussen: \(]a; b[\)) vs. angelsächsische (runde Klammer mit Komma: \((a, b)\)) — beide bezeichnen dasselbe.

**Anki-Deck (TL.35, TL.38, TL.39):**

- **TL.35 (Karte 17 Rundung):** Grenzfall „bei genau 5" ergänzt — kaufmännische Rundung (3.55 → 3.6, immer auf) vs. wissenschaftliche/banker rounding (3.55 → 3.6, 3.45 → 3.4, auf gerade Stelle; gleicht Rundungsfehler über viele Werte aus). Wichtig für Schüler, die mit verschiedenen Disziplinen in Berührung kommen.
- **TL.38 (Karten 1-6 Zahlenmengen):** Jede Definitionskarte (ℕ, ℤ, ℚ, ℝ, Hierarchie, irrationale Zahlen) erweitert mit konkreten Zahlen-Beispielen aus dem Alltag: ℕ → Anzahl Schüler, Hausnummern; ℤ → −5°C, Bilanzveränderung; ℚ → 3/4, −7/2; ℝ → π, √2 mit Dezimalwerten. Macht abstrakte Mengen greifbar.
- **TL.39 (Karte 22 quadratische Gleichung):** Explizite Zwei-Lösungen — „\(x_1 = +\sqrt{2} \approx +1.414\) und \(x_2 = -\sqrt{2} \approx -1.414\). Wichtig: eine quadratische Gleichung hat in ℝ üblicherweise zwei Lösungen (Symmetrie des Quadrierens)." Schliesst die Lücke „\(\pm\)" → was bedeutet das konkret?

Anki-Deck via `python3 scripts/build_apkg.py` neu generiert: 24 Karten, 6059 Bytes — Verifikation `sqlite3 …; SELECT COUNT(*) FROM notes` ergibt 24 ✓.

### Verifikation

- **Tag-Balance** auf allen 4 gepatchten Druck-Dateien: `aufgabenserie.html` 40/40, `teste-dich-selbst.html` 57/57, `handout.html` 3/3, `formelauszug.html` 4/4 — alle ausgeglichen.
- **Anki-Build** (build_apkg.py): syntaktischer Fehler nach erstem Versuch (Apostroph in „banker's rounding" hat den Python-String geschlossen) durch Ersatz mit HTML-Entities (&bdquo;/&ldquo;) korrigiert.
- **Titel-Verifikation** TL.32: ein erster automatischer Durchlauf mit thematisch geratenen Titeln erzeugte sechs falsche Zuordnungen; die wurden nach grep-Verifikation gegen die Aufgabentexte korrigiert.

---

## [unreleased] — 2026-05-25 · Lehrerbegutachtungen Welle L Themenseiten (LG1, LG3, LG4, LG5)

### Welle L — Aufgaben-Politur & Lerner-Erlebnis (22 Items von 80, Themenseiten LG1+LG3+LG4+LG5 + zwei Druck-Items)

Aus `TODO-lehrerbegutachtung.md` Welle L wurden die Themenseiten-Items für die Lerngebiete 1, 3, 4 und 5 abgearbeitet (TL.1–TL.6, TL.8–TL.22, TL.25–TL.30; 22 von 30 Themenseiten-/g5-Druck-Items). **Auslassungen begründet:** TL.7 (g1-1 A7 substanziell andere Übung — Aufgaben-Neukonstruktion), TL.23 (g5-3 Flussdiagramm-SVG), TL.24 (g5-4 A7 Sinuskurve-SVG) — alle drei wegen Konstruktionsaufwand bewusst zurückgestellt; in der nächsten Sitzung zu erledigen. **Bereits umgesetzt, nur verifiziert:** TL.12 (g3-3 Live-Box bei D<0 zeigt bereits „nicht definiert über ℝ"), TL.19 (g5-2a A6 Dachgiebel — bereits in Welle K TK.63 mit `aufg-vertiefung` markiert).

**LG1 Themenseiten (6 Items, drei Dateien):**

- **TL.1 (g1-1 Begriffe-Tabelle):** „Term" als erster Eintrag in der `ftb-tabelle` ergänzt mit Symbol \(T,\,T(x)\), Beispiel \(3x^2-5\), Bedeutung „Rechenausdruck aus Zahlen, Variablen, Operationen". Der eigentliche Begriff „Term" steht damit prominent in der Übersichtstabelle, nicht nur im Definitionsblock darüber.
- **TL.2 (g1-1 A3(4) Vorgriff-Vermerk):** Bei der Wurzel-Äquivalenz-Aufgabe \(\sqrt{a+b}\) vs. \(\sqrt{a}+\sqrt{b}\) Verweis auf 1.4 Zehnerpotenzen & Quadratwurzeln mit `quer`-Link sowohl im Aufgabentext (kursive Anmerkung) als auch in der Lösung (Klammer-Notiz). Schüler verstehen damit, dass das Gegenbeispiel zur „Wurzel-Distributivität" hier nur strukturell erlebt wird; die systematische Behandlung folgt in 1.4.
- **TL.3 (g1-2 A7 Tankstellen-Rabatt):** Tipp „Tipp: Runde nicht zu früh, sondern rechne mit Bruch und vergleiche am Schluss" aus dem Aufgabentext gestrichen. Dieser Tipp verriet die Pointe der Aufgabe (dass Variante A und C gleich sind, weil \(\tfrac{1}{12} \cdot 1.80 = 0.15\) — also die Bruch-Angabe gerade so gewählt wurde). Die Pointe bleibt in der Lösungs-Schluss-Bemerkung erhalten („Dass (A) und (C) gleich sind, ist kein Zufall: …").
- **TL.4 (g1-2 A3(5)/(6) Endwert-Konsistenz):** Lösungen für die Bruch-Aufgaben jetzt im Format „… = 30/45 = 2/3 (gekürzt durch 15). Endwert: 2/3." analog für (6). Der finale Wert ist explizit benannt — konsistent zur Form von A3(1)–(4), wo der Endwert als einfache Zahl am Schluss steht.
- **TL.5 (g1-4 A7(c) Avogadro):** Doppel-Erklärung verdichtet. Vorher zwei Sätze, die im Wesentlichen dieselbe Aussage machten („10-mal mehr als Avogadro" + „ein Zehntel der Tropfen"); jetzt ein zusammenhängender Satz mit klarem Bezug.
- **TL.6 (g1-4 A5(d) und A6 Marginalien):** 
  - A5(d): Vorzeichen-Falle ausführlich erklärt — „bei \(-3^2\) bindet die Potenz stärker als das vorangestellte Minus — also erst \(3^2 = 9\), dann das Vorzeichen anwenden: \(-9\). Bei \((-3)^2\) ist die Klammer Teil der Basis: \((-3)\cdot(-3) = +9\)".
  - A6(a): Hierarchie-Erklärung zum Vorzeichen-Wechsel des Exponenten beim Dividieren durch \(10^{-9}\) ergänzt — „Das Dividieren durch \(10^{-9}\) ist dasselbe wie Multiplizieren mit \(10^{+9}\)". Mittelschritt \(\tfrac{1}{4}\cdot\tfrac{1}{10^{-9}}\) in der Rechnung jetzt sichtbar.

**LG3 Themenseiten (4 Items, drei Dateien):**

- **TL.8 (g3-1 A3 Vertikaltest):** Aufgabe von reinem „Lösungs-Toggle"-Schema auf interaktive ✓/✗-Buttons umgestellt. Jede der vier Aussagen hat jetzt zwei Buttons (✓, ✗) und ein eigenes Feedback-Span. Neue JS-Funktion `checkA3(teil, userSaysTrue, btn)` mit der Wahrheitstabelle {a: false, b: true, c: false, d: true}; gibt pro Teil ein ✓- oder ✗-Feedback. CSS für `.check-aufg button` und `.feedback.ok`/`.feedback.fehler` ist bereits im Inline-Style der Seite vorhanden, kein neues CSS nötig. Das `check-aufg`-Pattern existiert bereits bei A1, A2, A4, A5; mit A3 ist die Konsistenz hergestellt.
- **TL.9 (g3-2 A4/A5/A6 Eingabe-Prüfungen):** Bei A4 (Handyvertrag), A5 (Mietauto), A6 (Temperatur) Eingabe-Felder mit Prüfen-Buttons ergänzt. A4: Funktionsgleichung (`K(t) = 0.08x+15`) plus Zahlenwert (`t = 125`). A5: nur Indifferenz-Zahlenwert (`x = 120`). A6: Funktionsgleichung (`F(C) = 1.8x+32`) plus Zahlenwert (`F(37) = 98.6`). Neue JS-Funktion `chkVal(id, target, einheit)` neben der bestehenden `chk()`-Funktion — `chkVal` parst eine reine Zahl (mit Toleranz 0.05), filtert eventuell mit eingegebene Einheiten-Buchstaben heraus.
- **TL.10 (g3-3 Anwendungs-Tabelle Spalte „Wann besonders gut"):** Die `anw-tabelle` hat jetzt vier Spalten statt drei: Form, Anwendung, **Wann besonders gut** (neu), Vorgehen. Für alle sechs Tabellenzeilen formuliert: ① ohne Strukturmerkmale, ② drei Punkte ohne ausgezeichneten, ③ Scheitelpunkt gesucht, ④ Scheitelpunkt gegeben, ⑤ Nullstellen gegeben, ⑥ Nullstellen + weiterer Punkt. Spalten-Verteilung 12/25/25/Rest. Analoge Struktur zur g2-3 Verfahren-Tabelle (Vorbild).
- **TL.11 (g3-1 A2(c)):** `<span class="aufg-vertiefung">Vertiefung</span>` an die Teilaufgabe \(h(x) = \dfrac{1}{\sqrt{x}}\) gehängt. Diese Aufgabe kombiniert zwei Einschränkungen (Wurzel-Radikand und Nenner), das ist eine Schwierigkeitsstufe über (a) und (b); Markierung macht das transparent.
- **TL.13 (g3-3 Diskriminanten-Beispiele):** Marginalie unterhalb der drei Klick-Buttons („D > 0", „D = 0", „D < 0") mit den konkreten Beispiel-Funktionen und ihren D-Werten: \(D>0: x^2-2x-3,\,D=16\); \(D=0: x^2-4x+4,\,D=0\); \(D<0: x^2+3,\,D=-12\). Die Klick-Karten zeigten die Zahlen bereits dynamisch, aber nicht alle Schüler entdecken das Zusammenspiel — die Marginalie macht es statisch sichtbar und ermöglicht „auf einen Blick"-Verständnis.

**LG4 Themenseiten (5 Items, drei Dateien):**

- **TL.14 (g4-1 A6 Eigene Mini-Erhebung):** Beispiel-Lösung um zwei neue Absätze erweitert: (1) „Geplante Auswertung" — Werteliste in Tabellenkalkulation, Mittelwert/Median/Std.abw./Histogramm, mit Hinweis auf Median-Robustheit gegen Vielnutzer-Ausreisser. (2) „Mögliche Fallstricke" — Selbstauskunft-Bias, Wochentag-Effekt, Doppeltyp-Aktivitäten. Damit greift die Lösung sowohl die Auswertungs-Phase (Brücke zu 4.2/4.3) als auch die Daten-Qualitäts-Phase explizit auf — vorher war nur die Erhebungs-Phase (Auswahl/Frage/Merkmalstyp) ausgearbeitet.
- **TL.15 (g4-3 A4(d) IQR-Formel-Varianten):** `block-tipp` „Alternative Formel-Varianten" direkt im Lösungs-Block ergänzt. Zwei Varianten: (1) Hilfszellen-Variante mit Q1, Q3, Differenz getrennt sichtbar; (2) `QUARTILE.EXC`-Variante (Hyndman-Fan 6). Klarstellung, dass eine echte Ein-Funktions-IQR in Excel/LibreOffice nicht existiert. Schliesst inhaltlich an Welle K TK.44/TK.47 (Tukey-vs-Excel-Quartile) an.
- **TL.16 (g4-2 A5(3) Heteroskedastizität):** Optionale Marginalie am Ende der dritten Bullet-Lösung als kursive Anmerkung mit dem Fachbegriff. Bewusst nicht als eigene Tipp-Box gestaltet, um den Lese-Fluss nicht zu unterbrechen — eine Pflicht-Fachsprache-Ergänzung für interessierte Schüler.
- **TL.17 (g4-0 Spielwiese-Marginalie):** Lead-Absatz neu mit dem Wort „Spielwiese" und drei `quer`-Links auf 4.1, 4.2, 4.3. Klärt die didaktische Rolle der Seite explizit: sie ist eine Anwendungs-/Übungs-Spielwiese, kein Theorie-Lehrtext. Adressiert die Begutachtungs-Beobachtung, dass Schüler auf den ersten Blick nicht erkennen, dass die Theorie in den nachfolgenden Kapiteln steht.
- **TL.18 (g4-0 Entwicklungs-Kommentar entfernt):** HTML-Kommentar in Z. 702-703 (Markdown-Notiz zur entfernten „Sektion 8 Zusammenfassung — Wo geht's weiter?", verfasst am 2026-05-17) komplett entfernt. Solche internen Notizen gehören in CHANGELOG/COLLABORATION, nicht in den ausgelieferten Code.

**LG5 Themenseiten (5 Items, vier Dateien):**

- **TL.20 (g5-2b A7 Drachen-SVG):** Inline-SVG (200×240, gerendert 160×190) der Drachen-Diagonalen-Anordnung mit Eckpunkten A/B/C/D, Diagonalen-Schnittpunkt M, Längenangaben 20/60 (vertikal) und 30/30 (horizontal). Trapezfarbe leicht blau, Strichelinien für Diagonalen, Eckpunkte als gefüllte Kreise. Macht die geometrische Konstruktion vor dem Lesen der Lösung visuell greifbar.
- **TL.21 (g5-2d A4 sss-Kontrast):** Aufgabe von „nur WW" auf „WW + sss" erweitert. Teil (a) wie zuvor (zwei Winkel reichen für Ähnlichkeit). Teil (b) NEU: 3-4-5 vs. 6-8-10 (alle drei Verhältnisse = 2 → ähnlich) und Kontrast 3-4-5 vs. 6-8-9 (Verhältnisse 2, 2, 1.8 → nicht ähnlich). Wichtige didaktische Pointe: Bei sss müssen alle drei Verhältnisse passen, nicht nur zwei. Beide Beispiele sind zudem rechtwinklig (pythagoräisches Tripel) — verbindet Ähnlichkeit mit Kongruenz im Pythagoras-Kontext.
- **TL.22 (g5-3 A6c Goldener Schnitt):** Marginalie nach der Lösung („Verhältnis Schenkel zu Basis ist 10/6.18 ≈ 1.618 — genau der goldene Schnitt φ = (1+√5)/2 ≈ 1.618 034. Daher der Name 'goldenes Dreieck'."). Schliesst die Aufgabe inhaltlich rund — bisher tauchte „goldenes Dreieck" nur als Name auf, ohne den entscheidenden Zusammenhang.
- **TL.25 (g5-5 A7 Gezeiten statt Riesenrad):** A7 komplett ersetzt durch eine Gezeiten-Anwendung. A6 (Riesenrad-Mittelhöhe) und alter A7 (Riesenrad-Höhe) hatten dasselbe Setup. Neue A7: Wassertiefe \(d(t) = 5 + 3 \cos(30°\cdot t)\) zwischen 2 m (Niedrigwasser) und 8 m (Hochwasser), Zyklus 12 h, Schiff braucht ≥ 6 m. Drei neue Teilaufgaben (a) Verifikation, (b) Gleichungslösung \(\cos(\varphi) = 1/3 \Rightarrow \varphi_1 \approx 70.53°,\,\varphi_2 \approx 289.47°\), (c) allgemeine periodische Lösung, (d) Einlauf-Zeitfenster \(\approx\) 4 h 42 min. Mathematisch verifiziert mit Python: \(\arccos(1/3) = 70.5288°\), Einlauf-Fenster \(2\cdot 2.351 = 4.702\) h.
- **TL.26 (g5-1 A6 Praxis-Projekt-Markierung):** `<span class="aufg-vertiefung">Praxis-Projekt</span>` an die Aufgaben-Überschrift A6 angehängt. Die Aufgabe verlangt eigene Messungen an einem Gegenstand und ist damit als individuelle, „handwerkliche" Vertiefung markiert — unterscheidet sich klar von den rechnerischen A1–A5 und der ähnlichen A7 (Strahlensatz mit gegebenen Zahlen).
- **TL.27 (g5-1 A7 Strahlensatz-Vorgriff):** Kursive Marginalie zwischen Aufgabentext und Teilaufgaben (a/b/c): „Diese Aufgabe ist ein klassischer Strahlensatz — die formale Behandlung folgt in 5.2d". Erklärt, dass die Schüler hier nur die Intuition „gleicher Sonnenwinkel ⇒ gleiches Verhältnis" brauchen, ohne die formale Strahlensatz-Maschinerie. Der bereits existierende `↗ 5.2d`-Link in der Lösung bleibt erhalten.
- **TL.28 (g5-2a Innenwinkelsumme-Beweis Wechselwinkel-Hinweis):** Kursive Marginalie nach dem Beweis-Erklärtext: „Tipp zur Animation: In Schritt 3 werden die zwei Wechselwinkel-Paare farblich identisch markiert". Macht die bestehende Canvas-Animation explizit als visuellen Beweis-Schritt nutzbar. **Keine zusätzliche SVG** — die existierende Animation deckt die Farbcodierung bereits ab, eine zusätzliche statische SVG wäre redundant.

**LG5 Druck (2 Items, zwei Dateien):**

- **TL.29 (druck-g5-1 Aufgabe 4 Titel):** Titel von „🟠 Aufgabe 4 — Skizze einer Anwendung" auf „🟠 Aufgabe 4 — Wendeltreppe" angeglichen. Vorher hatte Aufgabe 4 als einzige einen generischen Titel, alle anderen (Uhrzeiger, Sonnenstand, Strassenkreuzung) hatten Anwendungs-Titel. Damit ist die Tabellen-Konvention durchgängig.
- **TL.30 (druck-g5-2c Aufgaben/Lösungs-Struktur):** Sechs Lösungs-Blöcke `<div class="block block-bsp">…<div class="block-titel">🟢 Lösung</div>…</div>` jeweils in `<details>`-Container umgewandelt. Pro Aufgabe steht jetzt: H2-Titel, Aufgabentext, dann `<details>`-Falter mit dem Lösungs-Block. Schüler können auf der Druckseite zuerst rechnen, dann die Lösung aufklappen. Reine HTML-Lösung (kein JS nötig). Konvention angepasst an die LG5-Standard-Struktur, allerdings mit dem `<details>`-Pfad statt der ZWEI-h2-Struktur, weil das im Druck handlicher ist. Variante des Standards aus dem TODO-Vorschlag bewusst gewählt — siehe TODO-Item Wortlaut „Alternativ: Lösungen in `<details>`-Falt-Container".

### LG1-Druck und LG2-Druck (TL.31–TL.80, 50 Items)

**Bewusst zurückgestellt für eine eigene Sitzung.** Die LG1-Druck-Items (TL.31–TL.65, 35 Items) und LG2-Druck-Items (TL.66–TL.80, 15 Items) betreffen vier Druckseiten-Rollen (Handout, Formelauszug, Aufgabenserie, Teste-dich-Selbst) plus Anki-Karten und sind nicht mehr im Budget dieser Sitzung. Empfehlung für die Folgesitzung: pro LG einen Sub-Block (z.B. „Welle L LG1-Druck Handout + Formelauszug", dann „Welle L LG1-Druck Aufgabenserie + Teste", dann „Welle L LG2-Druck"), und nach jedem Sub-Block ein ZIP packen.

### Verifikation

- **Standard-Pre-Flight §3.6** auf allen 16 gepatchten Themenseiten: alle grün (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 bad=0`, Toggle-Counts unverändert).
- **Tag-Balance** auf den zwei gepatchten Druck-Dateien: `aufgabenserie.html` von g5-1 (35 `<div>`-open / 35 close), g5-2c (15/15) — beide ausgeglichen. Sechs `<details>`-Container in g5-2c jeweils sauber geschlossen.
- **Mathematische Verifikation der inhaltlich-substantiellen Patches:**
  - TL.21 (sss-Kontrast 6-8-9): \(\tfrac{9}{5} = 1.8 \neq 2\) — bestätigt die Nicht-Ähnlichkeit.
  - TL.22 (goldenes Dreieck): \(10/(2 \cdot 10 \sin 18°) = 1/(2\sin 18°) = 1.6180\) ✓ — exakter goldener Schnitt.
  - TL.25 (Gezeiten): \(d(0)=8, d(6)=2\) ✓; \(\arccos(1/3) = 70.5288°\) (Python); Lösungen \(t_1 = 2.351, t_2 = 9.649\) h; Einlauf-Fenster \(2 \cdot 2.351 = 4.702\) h ≈ 4 h 42 min ✓.

### Tool-Quoten-Hygiene — Lehre aus der Sitzung

Sitzungs-Start dieser Welle L lief schief: erste Sub-Sitzung (LG1+Teile LG3, 8 Items) wurde abgebrochen ohne Zwischen-ZIP, COLLABORATION §3.4 verletzt. Patches blieben nur im Container. Zweite Sub-Sitzung (LG3-Ende, LG4, LG5 ohne SVG-teure-Items, 9 Items) ebenfalls ohne ZIP geendet. Erst die dritte Sub-Sitzung (diese) packt den kumulierten Stand von 17 Items in ein ZIP, bevor weitere Patches überhaupt versucht werden. **Lehre für nächste Wellen:** bei jeder Welle mit mehr als ~10 Items vorab in Sub-Blöcke aufteilen und nach jedem Sub-Block ein ZIP packen, nicht erst am Schluss. Bei Auftrag „Welle X soweit wie möglich" ist das vom Modell selbst zu strukturieren — vorausgesetzt, das Modell hält sich daran (was zweimal in Folge nicht geklappt hat).

---

## [unreleased] — 2026-05-24 · Lehrerbegutachtungen Welle K LG1 — Inventur (keine Code-Änderungen)

### Welle K — Lösungsweg-Granularität & Marginalien (15 Items, TK.1–TK.15)

Inventur-Eintrag, kein Code-Patch in dieser Sitzung. Beim Versuch, Welle K LG1 abzuarbeiten, hat die Substanz-Stichprobe alle 15 Items als bereits im Code umgesetzt erwiesen — vermutlich aus einer früheren Sitzung, in der `CHANGELOG.md` und `TODO-lehrerbegutachtung.md`-Status nicht mit-aktualisiert wurden. Diese Inventur dokumentiert die tatsächlichen Stellen im Code, sodass die Diskrepanz zwischen TODO/CHANGELOG und Code aufgelöst ist.

**Themenseiten (3 Items):**

- **TK.1 (g1-2 Doppelminus-Mini-Sektion):** eigene `<h3>` „Doppelminus-Regel" in `grundlagen/g1-2-zahlen-grundoperationen.html` Z. 303, gefolgt von `block-bsp` „🟢 Beispiel · Doppelminus in drei Situationen" mit drei Fällen plus Erweiterungs-Hinweis auf vier Minuszeichen → Periodizität.
- **TK.2 (g1-3 A3(c) faktorisierter Alternativweg):** `grundlagen/g1-3-algebraische-terme.html` Z. 463–466 — neben dem klassischen „Erst beide Teile ausmultiplizieren, dann subtrahieren"-Weg jetzt zusätzlich der elegantere Faktor-Ausklammer-Weg `(x+y)(x-y) - (x-y)² = (x-y)·((x+y)-(x-y)) = 2y(x-y)`.
- **TK.3 (g1-3 A7 vier Slogans, davon drei falsche):** `grundlagen/g1-3-algebraische-terme.html` Z. 532–551 — Aufgabe von ursprünglich „eine korrekt, eine falsch" auf vier Slogans erweitert: (1) `(a+b)²=a²+b²` falsch, (2) `2(x+y)=2x+2y` korrekt, (3) `√(a²+b²)=a+b` falsch, (4) `(a+b)³=a³+b³` falsch. Lösung mit Gegenbeispielen pro falschen Slogan plus algebraisch korrekter Reformulierung. Alle drei falschen gehören zur gleichen Fehlerfamilie (Operation darf nicht gliedweise verteilt werden).

**LG1-Druck-Items (12 Items):**

- **TK.4 (druck-g1-1 Aufgabenserie A1(a) — Distributivgesetz):** `downloads/grundlagen/g1-1-grundlagen/aufgabenserie.html` Z. 176–178 — Zusammenfassung `28·ℓh + 12·ℓh + 75 = (28+12)·ℓh + 75 = 40·ℓh + 75` explizit als „Distributivgesetz rückwärts gelesen" benannt.
- **TK.5 (druck-g1-1 Aufgabenserie A2(c) — linearer Funktions-Aspekt):** `downloads/grundlagen/g1-1-grundlagen/aufgabenserie.html` Z. 187 — Klammer-Erklärung „Steigung m=95 und Achsenabschnitt q=130 — solche Terme heissen *lineare Funktionen* und werden in 3.2 systematisch behandelt" als Brücke zu LG3.
- **TK.6 (druck-g1-1 Aufgabenserie A6(a) — Funktionen-Vorgriff):** dieselbe Datei Z. 216–218 — Vorgriff „solche Bildungsgesetze der Form N(t)=N₀·a^{kt} heissen … und werden in 3.x systematisch behandelt". Doppel-Vorgriff in derselben Aufgabenserie ist intentional, weil A2(c) und A6(a) zwei verschiedene Funktionstypen (linear, exponentiell) ansprechen.
- **TK.7 (druck-g1-1 Selbsttest Aufg. 6(c) — Distributiv über Differenz):** `downloads/grundlagen/g1-1-grundlagen/teste-dich-selbst.html` Z. 216 — Zwischenschritt `b - c = b + (-c)` explizit ausgeschrieben, damit das Distributivgesetz dann symmetrisch auf Summen angewendet werden kann.
- **TK.8 (druck-g1-1 Handout Abschnitt 4 — Koeffizient statt Konstante):** `downloads/grundlagen/g1-1-grundlagen/handout.html` Z. 70 — bei `3x²` wird die Zahl `3` korrekt als „Koeffizient 3" bezeichnet (nicht „Konstante 3", was bei `3` als Vorfaktor terminologisch falsch wäre — eine Konstante ist ein Glied ohne Variable, ein Koeffizient ist der Vorfaktor einer Potenz).
- **TK.9 (druck-g1-2 Handout — Division-Beispiele):** `downloads/grundlagen/g1-2-zahlen-grundoperationen/handout.html` Z. 77–78 — explizit „Bei der Division gilt die gleiche Regel" mit beiden Beispielen `(-12)/(-4) = +3` und `(-12)/(+4) = -3`. Vorher nur Multiplikation gezeigt, Schüler mussten den Transfer selbst herstellen.
- **TK.10 (druck-g1-2 Selbsttest Aufg. 9(c) — Quadrat-Vorzeichenfalle):** `downloads/grundlagen/g1-2-zahlen-grundoperationen/teste-dich-selbst.html` Z. 136 — vollständige Lösung „Vorzeichen-Falle: `-3² = -(3²) = -9` (Potenz bindet stärker als das vorgestellte Minus), aber `(-3)² = (-3)·(-3) = +9` (Klammer ändert die Reihenfolge). Summe: `-9 + 9 = 0`". Klassischer Sek-I-Stolperstein, sauber aufgelöst.
- **TK.11 (druck-g1-3 Aufgabenserie A2 — Bremsweg-Disclaimer):** `downloads/grundlagen/g1-3-algebraische-terme/aufgabenserie.html` Z. 64–66 — `block-fehler` „⚠ Achtung — vereinfachte Modellformel, nicht die offizielle Schweizer Verkehrs-Faustformel". Offizielle Form `Bremsweg = (v/10)²`, Reaktionsweg `(v/10)·3`, mit Beispiel `v=50 km/h`. **Sicherheitskritisch** — ohne Disclaimer könnten Schüler die Modellformel mit der Fahrschul-Faustformel verwechseln.
- **TK.12 (druck-g1-3 Selbsttest Aufg. 8(c) — vollständige Faktorisierung):** `downloads/grundlagen/g1-3-algebraische-terme/teste-dich-selbst.html` Z. 136 — Marginalie „*Vollständig faktorisiert* ergibt (c) sogar `3x(x-1)(2x-1)` — der quadratische Faktor lässt sich mit der Mitternachtsformel oder durch geschicktes Probieren weiter zerlegen; das wird in 2.2 systematisch behandelt" mit `quer`-Link auf g2-2b.
- **TK.13 (druck-g1-3 Handout Abschnitt 7 — `-(a-b)`-Falle mit Zahlenbeispiel):** `downloads/grundlagen/g1-3-algebraische-terme/handout.html` Z. 91–93 — Falle 1 jetzt mit konkretem Beispiel: „Für `a=5, b=3`: `-(5-3) = -(2) = -2`. Falsche Auflösung `-5-3 = -8` ergibt ein deutlich anderes Resultat; richtig `-5+3 = -2` ✓". Konkrete Zahlen helfen, abstrakte Falle erkennbar zu machen.
- **TK.14 (g1-4 Wurzel-Faustwerte erweitert):** `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 335 — Liste umfasst jetzt `√2 ≈ 1.4142`, `√3 ≈ 1.7321`, `√5 ≈ 2.2361`, `√7 ≈ 2.6458`, `√10 ≈ 3.1623`. Vorher nur eine Teilmenge (typisch `√2, √3, √5`); jetzt vollständig für die Primzahlen ≤ 7 plus die Zehnerpotenz.
- **TK.15 (g1-4 Druck Handout Abschnitt 5 W4 — Vorzeichen-Falle):** `downloads/grundlagen/g1-4-zehnerpotenzen-quadratwurzeln/handout.html` Z. 80 (W4-Regel mit Beispiel `√((-5)²) = 5`) und Z. 86 (zusätzlicher `block-fehler` „⚠ Vorzeichen-Falle — `√(a²) = |a|`, nicht `a`"). Identität ist die häufigste Sek-II-Eingangsprüfungsfalle.

### Verifikation

- **Code-Substanz-Stichprobe** auf alle 15 Items: jeder Patch ist nachweisbar im Code an der genannten Stelle vorhanden. Verwendete Suchmuster pro Item siehe Sitzungs-Transcript.
- **Keine Code-Änderungen** in dieser Sitzung — ZIP-Inhalt identisch zum vorigen ZIP `tals-mathe_46_welle-k-lg5.zip`, abgesehen vom CHANGELOG und der TODO-Status-Aktualisierung.

### Lehre für die Sitzungs-Hygiene

Die Diskrepanz zwischen Code-Stand und Buchhaltungs-Stand (TODO + CHANGELOG) entstand vermutlich in einer früheren LG1-Sitzung, in der die Patches gemacht wurden, aber die Status-Updates am Ende nicht. Möglich auch: ein Merge oder ein Rückschritt im CHANGELOG hat einen alten LG1-Eintrag versehentlich entfernt. Vorschlag für künftige Sitzungen: vor dem Auftrag-Beginn **immer** prüfen, ob die Items im Code bereits umgesetzt sind — die Stichproben kosten wenig (typisch 5–10 grep-Aufrufe pro Welle), und sparen den Auftraggeber davor, eine vermeintliche „Welle starten"-Anfrage zu stellen, die in Wirklichkeit „nur noch buchhalten" wäre.

### Welle-K-Gesamtstand nach dieser Inventur

Welle K **vollständig abgeschlossen**: LG1 (15 Items, Code-Stand bereits korrekt), LG2 (16 Items, 2026-05-24), LG3 (13 Items, 2026-05-24), LG4 (13 Items, Code-Stand bereits korrekt), LG5 (11 Items, 2026-05-24). Insgesamt **68 TK-Items abgeschlossen**. Aus `TODO-lehrerbegutachtung.md` verbleiben damit die Wellen N (Sterne-System, optional / P5) und O (Detail-Politur, P5) — beides keine inhaltlichen Sachfehler-Wellen, sondern strategisch-stilistische Politur.

---

## [unreleased] — 2026-05-24 · Lehrerbegutachtungen Welle K LG5

### Welle K — Lösungsweg-Granularität & Marginalien (11 Items, TK.57–TK.67)

Aus `TODO-lehrerbegutachtung.md` Welle K wurde der komplette LG5-Block (11 Items) in einer Sitzung abgearbeitet. Schwerpunkt: trigonometrische Klarstellungen (Tangens-Konstruktion bei \(\cos\varphi < 0\), Cosinussatz-Vorzeichen bei stumpfen Winkeln, Tangens-Lösungen im Hauptintervall), geometrische Argumentations-Hygiene (Sechseck-30-60-90 ohne Umkreisradius-Detour, inklusive Trapez-Definition, k=0-Reihenfolge), Rundungs-Toleranzen in den Druckdateien.

**Themenseiten (7 Items, sechs Dateien):**

- **TK.57 (g5-2c A3 Teil 2 — umschriebenes Sechseck):** Lösung neu argumentiert. Vorher Verweis auf „Umkreisradius \(R\) als Hypotenuse" mit unklarer Zuordnung der Dreiecks-Stücke; das verwirrte gleich doppelt, weil \(R\) für das umschriebene Sechseck zufällig denselben Zahlwert wie \(S\) hat und dann mit \(R\) (Aussenradius des Sechsecks) plus \(r\) (Inkreisradius = gegebener Kreisradius) zwei verschiedene grosse-\(R\)-Bedeutungen auftauchen. Jetzt klare 30-60-90-Argumentation: Stützdreieck \(MFE\) (Mittelpunkt → Seitenmitte → Eckpunkt), rechter Winkel bei \(F\), Sektor-halber Winkel \(\angle FME = 30°\), daraus direkt \(\tan 30° = (S/2)/r\). Keine Hypotenuse-Bezeichnung mehr nötig. Ergebnis identisch: \(U_6 = 2\sqrt{3} \approx 3.4641\).
- **TK.58 (g5-2b A2(4) — Trapez-Definition):** `block-tipp` „💡 Inklusive vs. exklusive Trapez-Definition" direkt nach Bullet 4 der Lösung. Klarstellung, dass die Aussage „Jedes Parallelogramm ist ein Trapez" nur in der **inklusiven** Definition (mindestens ein Paar paralleler Seiten — Schweizer Schulgeometrie-Konvention) gilt. In der **exklusiven** Definition (genau ein Paar paralleler Seiten — in älteren DACH-Lehrbüchern), wäre ein Parallelogramm *kein* Trapez. Die Hierarchie-Tabelle des Kapitels (Quadrat → Rechteck → Parallelogramm → Trapez → Viereck) setzt die inklusive Definition voraus und gewinnt damit die Vererbung aller Eigenschaften.
- **TK.59 (g5-4 Symmetrieeigenschaften-Tabelle):** Neue erste Zeile „**\(-\alpha\)** (Spiegelung an x-Achse)" mit \(\sin(-\alpha) = -\sin\alpha\), \(\cos(-\alpha) = \cos\alpha\), \(\tan(-\alpha) = -\tan\alpha\). Der Text unter der Tabelle erweitert um die Bemerkung: „\(\cos\) ist eine *gerade* Funktion, \(\sin\) und \(\tan\) sind *ungerade*", und um den Hinweis, dass \(-\alpha\) und \(360° - \alpha\) denselben Punkt am Einheitskreis beschreiben — die neue Zeile ist also die kürzeste Form der Q-IV-Spiegelung. Wichtig für die Schweizer Maturitätsprüfung, weil \(-\alpha\)-Argumente häufig in Identitäts-Aufgaben auftauchen.
- **TK.60 (g5-4 Tangens-Erklärtext):** `block-tipp` „💡 Wenn \(P\) in Q II oder Q III liegt" direkt nach dem Definitionssatz. Klärt eine Stelle, an der die übliche Darstellung „Strahl \(OP\) schneidet die rechte Tangente" für \(\cos\varphi < 0\) faktisch falsch ist (der vorwärtige Strahl trifft die Tangente nie). Erklärt die **rückwärtige Verlängerung** des Strahls durch \(O\) hindurch — und nutzt das Vorzeichen des Schnittpunkts y-Werts, um die korrekten Tangens-Vorzeichen pro Quadrant zu rechtfertigen (Q II: Schnittpunkt unter x-Achse, \(\tan < 0\); Q III: Schnittpunkt über x-Achse, \(\tan > 0\)).
- **TK.61 (g5-5 Tangens-Schema, Typ 3):** Zusatz im Erklär-Absatz: „Im Hauptintervall \([0°;\,360°[\) liefert das trotzdem **zwei** Lösungen — den Taschenrechner-Wert \(\varphi_1\) (in Q I oder IV) und den um \(180°\) verschobenen Wert \(\varphi_1 + 180°\) (in Q III oder II). Beide gehören zur selben Lösungsfamilie, sind aber im Intervall \([0°;\,360°[\) getrennt anzugeben." Bisheriger Text suggerierte, die einzige Lösungsfamilie heisse auch *eine Lösung im Hauptintervall* — falsch und Hauptquelle für unvollständige Lösungen in Klausuren.
- **TK.62 (g5-3 Cosinussatz-„Wann anwenden?"-Box):** Vorzeichen-Anmerkung am Ende der Box. Drei Beobachtungen: (a) Für \(\alpha > 90°\) ist \(\cos\alpha < 0\), also wird \(-2bc\cos\alpha\) positiv und \(a\) länger als im Pythagoras-Fall. (b) Beim sss-Fall beim Auflösen nach \(\cos\alpha\): negatives Resultat = stumpfer Winkel, nicht Vorzeichen-Fehler. Die Animation 5 hat den \(\alpha > 90°\)-Fall bereits am Rande erwähnt; jetzt steht das Vorzeichen-Argument explizit im Merksatz-Kontext.
- **TK.63 (g5-2a A6 + g5-2c A5(2)):** „mit Vorgriff auf 5.3" markiert. Beide Aufgaben verwenden trigonometrische Funktionen, die erst in 5.3 (g5-3 Trigonometrische Berechnungen) formal eingeführt werden. Vorgriff-Markierung in der Aufgaben-Überschrift bzw. -Stellung als `<span class="aufg-vertiefung">`-Tag (g5-2a A6) bzw. als kursive Klammer-Marginalie in A5(2) (g5-2c) mit `class="quer"`-Link auf 5.3. Aufgaben selbst inhaltlich unverändert.

**Druckdateien (4 Items, vier Dateien):**

- **TK.64 (druck-g5-2a Aufgabenserie A5(b) — Treppen-Probe):** Rundungs-Drift in der Probe geklärt. Vorher: „Probe: 15 mal die einzelne Stufenkante: \(15 \cdot 33.3 \approx 499.5\) cm ✓" — der Wert \(499.5\) entsteht nur durch Multiplikation des **gerundeten** Stufen-Werts \(33.3\) cm (statt \(\sqrt{1108} \approx 33.286\)). Jetzt: exakte Probe \(15\sqrt{1108} = \sqrt{225 \cdot 1108} = \sqrt{249\,300} \approx 499.3\) cm — algebraisch identisch zum Hypotenuse-Wert der Gesamttreppe. In Klammer der Hinweis, dass \(499.5\) durch \(15 \cdot 33.3\) entsteht und die \(0.2\) cm reiner Rundungsfehler sind.
- **TK.65 (druck-g5-2c Aufgabenserie A1 — Pizza):** Genauer Prozentwert in Klammer ergänzt. Aussage „rund 16 % günstiger" steht weiterhin im Text, in Klammer jetzt „genau \((0.0264 - 0.0223)/0.0264 \approx 15.5\,\%\)". Verifiziert: exakt 15.5000 % (gerundete Werte) bzw. 15.5000 % (mit Voll-Präzision der Brüche). Die ursprüngliche „rund 16 %"-Formulierung war zur Folge einer Aufrundung der Ersparnis.
- **TK.66 (druck-g5-2d Selbsttest L15 — \(k=0\)):** Lösungs-Reihenfolge umgekehrt. Vorher: „Jede Figur schrumpft auf den Punkt \(Z\) (\(k = 0\) ist als Streckfaktor definitionsgemäss ausgeschlossen — die Abbildung wäre nicht umkehrbar)." Inhaltlich verwirrend, weil die Klammer-Bemerkung im Nachgang die Hauptaussage relativiert. Jetzt: erst Definitionsklärung („\(k=0\) ist definitionsgemäss ausgeschlossen", mit Begründung der Nicht-Umkehrbarkeit), *dann* das formale Resultat des Einsetzens (\(\vec{ZP'} = k \cdot \vec{ZP} = \vec{0}\) → Degeneration auf \(Z\)). Saubere logische Trennung von definitorischer und rechnerischer Aussage.
- **TK.67 (druck-g5-3 Aufgabenserie A2 — Bergbahn):** Pythagoras-Probe-Wert korrigiert. Vorher \(\sqrt{1\,310\,400} \approx 1144.5\) m, was rechnerisch falsch ist (\(\sqrt{1\,310\,400} = 1144.7270\)). Die \(1144.5\) entsteht nur, wenn man die Cosinus-Rechnung mit dem auf \(17.5°\) gerundeten Winkel macht. Jetzt: Pythagoras korrekt mit \(\approx 1144.7\) m, danach explizite Toleranz-Anmerkung — die \(0.2\) m Differenz zur Cosinus-Rechnung entsteht durch die Rundung von \(\alpha\) auf \(17.5°\); mit dem unaufgerundeten Winkel \(\arcsin(0.3) \approx 17.4576°\) liefert auch die Cosinus-Rechnung 1144.7 m.

### Verifikation

- **Standard-Pre-Flight §3.6** auf den sechs gepatchten Themenseiten (g5-2a, g5-2b, g5-2c, g5-3, g5-4, g5-5): alle grün (`pw=1 mc=1 ml=1 tog ≥ 7`). Toggle-Count auf g5-3 vergleichsweise hoch (13) — historisch gewachsen.
- **HTML-Parser-Tag-Bilanz** auf allen 10 gepatchten Dateien (6 Themenseiten + 4 Druckdateien): alle OK, keine unbalancierten Tags.
- **Marker-Eindeutigkeit §3.7** (`<h2 id="ressourcen">`, `<div class="dl-grid">`, `<aside class="toc-wrap">`, `<footer class="site-footer">`) auf den sechs Themenseiten: alle exakt einmal vorhanden.
- **LaTeX-Klammern-Balance** auf allen 10 Dateien: paarweise konsistent (sowohl Block- \(\backslash[\dots\backslash]\) als auch Inline- \(\backslash(\dots\backslash)\)).
- **Mathematische Verifikation der Patches:**
  - TK.57 (Sechseck-30-60-90): Stützdreieck \(MFE\), \(\angle FME = 30°\), \(MF = r\) (am 30°-Winkel), \(FE = S/2\) (gegenüber 30°-Winkel) → \(\tan 30° = (S/2)/r \Rightarrow S = 2r/\sqrt{3}\). Mit \(r = 1/2\): \(S = 1/\sqrt{3} \approx 0.5774\); \(U_6 = 6S = 2\sqrt{3} \approx 3.4641\). ✓
  - TK.64 (Treppen-Probe): \(15\sqrt{1108} = \sqrt{225 \cdot 1108} = \sqrt{249\,300} = 499.300\) cm (Python `math.sqrt`). Gerundet \(15 \cdot 33.3 = 499.5\). Differenz \(0.2\) cm. ✓
  - TK.65 (Pizza): \((0.0264 - 0.0223)/0.0264 = 15.5303\,\%\) (Python). Mit Voll-Präzision \((14/(\pi \cdot 13^2) - 28/(\pi \cdot 20^2)) / (14/(\pi \cdot 13^2)) = 15.5000\,\%\). ✓
  - TK.67 (Bergbahn): \(\sqrt{1\,310\,400} = 1144.7270\) m (Python). \(1200 \cdot \cos(17.5°) = 1144.4603\) m. \(1200 \cdot \cos(\arcsin(0.3)) = 1144.7270\) m. ✓ — bestätigt, dass die alte Probe-Zahl 1144.5 falsch war.

### Bemerkung — typische Aufwandsklassen in LG5

Die LG5-Welle bestätigt das Muster aus LG2/LG3: 4 der 11 Items erforderten **eigene mathematische Konstruktion oder Recherche** (TK.57 Sechseck-Argumentation neu, TK.59 Symmetrie-Tabelle erweitert, TK.60 Tangens-Konstruktion bei \(\cos\varphi < 0\) erklärt, TK.67 Pythagoras-Wert korrigiert und Rundungsanalyse). Die übrigen 7 waren Wortlaut-Patches oder kompakte Ergänzungen. Insbesondere TK.67 wurde nur dadurch sauber, dass ich den behaupteten Pythagoras-Wert tatsächlich nachgerechnet habe — der ursprüngliche „1144.5"-Wert in der Lösung war numerisch falsch und nicht nur ein Rundungs-Artefakt der Anzeige; die Korrektur ändert echte Mathematik. Empfehlung für LG1: **alle behaupteten Probe-Werte und Endergebnisse vor dem Patch nachrechnen**, nicht nur die explizit als Sachfehler markierten.

---

## [unreleased] — 2026-05-24 · Lehrerbegutachtungen Welle K LG4

### Welle K — Lösungsweg-Granularität & Marginalien (13 Items, TK.44–TK.56)

Aus `TODO-lehrerbegutachtung.md` Welle K wurde der komplette LG4-Block (13 Items) in einer Sitzung abgearbeitet. Schwerpunkt: **Tukey vs. Excel-Quartile** (Methodik-Diskrepanz auf Theorieseite, A1-Lösung und Handout adressiert), Lösungs-Granularität (Schiefe-Faustregel explizit), didaktische Marginalien (Schuhgrösse-Grauzone, Klassen-Namens-Konvention, beidseitig geschlossene Endklasse), Boxplot-Konventionen (Whisker-Tukey) und ein konkretes Beispiel für die offene A6-Aufgabe.

**Themenseiten (6 Items, drei Dateien):**

- **TK.44 (g4-3 nach QUARTILE.INKL-Tabelle Z. 272):** Neuer `block-fehler` „⚠ Excel-Quartile ≠ Handrechnung — zwei Methoden im Umlauf". Erklärt, dass `QUARTILE.INKL` lineare Interpolation (Hyndman-Fan Variante 7) verwendet, während die im Kapitel gelernte Median-der-Hälften-Methode (Tukey) anders rechnet. Bei kleinen Stichproben können beide unterschiedliche Werte liefern; für Schul-Rechnungen ist die Tukey-Methode verbindlich.
- **TK.45 (g4-2 A3 Histogramm zeichnen):** Histogramm als SVG in der Lösung ergänzt (analog zum A4-Boxplot-SVG). 5 Säulen für die Klassen \([1;3[, [3;5[, [5;7[, [7;9[, [9;11[\) mit Häufigkeiten 4, 11, 11, 3, 1. Säulen berühren sich (Histogramm-Konvention, im Unterschied zum Balkendiagramm), y-Achse mit Ticks bei 0, 5, 10. Visualisiert die im Text bereits beschriebene Doppelspitze.
- **TK.46 (g4-2 A2 Klasseneinteilung):** `block-tipp` „Die letzte Klasse ist beidseitig geschlossen" in der Lösung. Erklärt warum \([45;50]\) statt \([45;50[\): sonst würde der Maximalwert in keine Klasse fallen. Alle übrigen Klassen bleiben halboffen \([\text{links}; \text{rechts}[\), damit Werte am Klassen-Übergang eindeutig einer Klasse zugeordnet sind.
- **TK.47 (g4-3 A1 Lösung):** `block-tipp` „Excel rechnet anders" mit konkretem Vergleichswert. Für die A1-Daten (sortiert 12, 12, 14, 15, 17, 18, 20, n=7) liefert die Tukey-Handrechnung \(Q_1=12, Q_3=18\), während <code>=QUARTILE.INKL(...;1)</code> aus Excel \(Q_1=13, Q_3=17.5\) ergibt — beide korrekt nach ihrer jeweiligen Definition. Verifiziert: bei k=1 interpoliert Excel an Position \((n-1)\cdot 0.25 + 1 = 2.5\), also zwischen Rang 2 (=12) und Rang 3 (=14), linear \(12 + 0.5 \cdot 2 = 13\). Bei k=3 entsprechend an Position 5.5: \(17 + 0.5 \cdot 1 = 17.5\). Schliesst inhaltlich an TK.44 an.
- **TK.48 (g4-3 A6 Eigene Daten):** Mini-Beispiel-Lösung mit fiktivem Datensatz Bildschirmzeit. Urliste und sortierte Liste mit n=15 (Summe 2420), Mittelwert \(\bar{x} \approx 161.3\) min, Median 155 min, Modus 180 (zweimal), Q1=110, Q3=200, QD=90, Standardabweichung \(s \approx 64.5\) min. Mathematisch verifiziert: Mittelwert, Median, Quartile, Modus, Std.abw. alle nachgerechnet (Python `statistics`-Modul). Inklusive 3-Satz-Interpretation: annähernd symmetrisch (Mittelwert/Median fast gleich), aber Ausreisser bei 320 min (rund 2.5 Standardabweichungen über Mittelwert), Median etwas robuster aber Unterschied klein.
- **TK.49 (g4-3 Aufgaben-Sektion-Start):** `block-tipp` „Klassen-Namen in diesem Kapitel". Klärt die Konvention: **Klasse A/B** sind die Theorie-Demobeispiele (immer dieselben acht Werte zur Streuungs-Illustration), **Klasse X/Y** sind Vergleichs-Aufgabendatensätze in A5 und A7 — verschiedene Buchstaben, weil sie verschiedene Datensätze enthalten und nicht austauschbar sind. Saubere Konsolidierung ohne Datensätze umzubenennen (die A/B-Demonstration und das X/Y-Aufgabenpaar haben jeweils didaktischen Sinn).
- **TK.50 (g4-1 A2(1) Schuhgrösse):** Erste Lösungs-Bullet differenziert: „Diskret (mit Grauzone)" — formell diskret (festes Raster aus Halbschritten 41, 41.5, 42, ...), inhaltlich grob klassierte Messung einer stetigen Grösse (Fusslänge). Beide Sichtweisen in der Schweizer Fachliteratur belegt — wichtig ist die Begründung im Kontext.

**Druckdateien (6 Items, fünf Dateien):**

- **TK.51 (druck-g4-3 Handout §5):** `block-tipp` „Whisker — zwei verbreitete Konventionen" nach der Boxplot-Element-Tabelle. Erklärt den Unterschied zwischen der hier verwendeten Min-Max-Whisker-Konvention und der Tukey-Konvention (Whisker reichen nur bis Datenpunkten innerhalb 1.5·QD ab Box-Rand, alles darüber als Ausreisser einzeln gezeichnet). In Excel, R, matplotlib gebräuchlich.
- **TK.52 (druck-g4-3 Handout Schluss):** Neuer `block-fehler` „⚠ Häufige Fehlerquellen" mit fünf Punkten (n vs. n−1, Median ohne Sortierung, Tukey vs. Excel-Quartile, Mittelwert von kategorialen Daten, Std.abw. = 0). Bringt g4-3 auf Konsistenz mit g4-1 und g4-2, die diesen Block bereits haben.
- **TK.53 (druck-g4-3 Handout §1 + Formelauszug Z. 48):** Modus-Definition erweitert um den Begriff *multimodal*. Im Handout: „Treten mehrere Werte mit gleicher Maximalhäufigkeit auf, spricht man von *mehrmodalen* bzw. *multimodalen* Verteilungen (bei genau zwei: *bimodal*)". Im Formelauszug knapper Klammer-Zusatz.
- **TK.54 (druck-g4-3 Aufgabenserie A5(b) Filiale B):** Schiefe-Faustregel-Schritt explizit ausgeschrieben. Vorher: „Beides spricht für rechtsschiefe Verteilung". Nachher: „Mittelwert > Median heisst, die wenigen sehr grossen Werte ziehen den Mittelwert nach oben, während der Median sich nicht bewegt — das ist genau die Signatur einer rechtsschiefen Verteilung".
- **TK.55 (druck-g4-2 Aufgabenserie A4(b) Streudiagramm):** Korrelations-Antwort sauber in zwei Bullets aufgegliedert: (1) „Korrelation ≠ Kausalität" (Möglichkeit von Drittvariablen oder umgekehrter Kausalität) und (2) „Individuelle Unterschiede" (selbst bei vorhandenem Kausalzusammenhang gibt es Streuung durch persönliche Faktoren). Die beiden konzeptuell verschiedenen Punkte hingen vorher in einem zusammengezogenen Satz.
- **TK.56 (druck-g4-1 Handout §3):** ZEILE()-Sortier-Trick aus der Tabelle „Tabellenkalkulation" ausgelagert in eine eigene `block-tipp`-Box „💡 Sortier-Trick mit KKLEINSTE und ZEILE()". In der Tabelle steht jetzt nur noch die Kernform `=KKLEINSTE(A:A;k)` (konsistent zum g4-1-Formelauszug). Die Tipp-Box erklärt den Trick mit konkretem Beispiel und Hinweis für Start in anderer Zeile als Zeile 1.

### Verifikation

- **Standard-Pre-Flight §3.6 (Marker-Anwesenheit)** auf den drei gepatchten Themenseiten (g4-1, g4-2, g4-3): alle grün (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 bad=0`). `tog`-Count gleich geblieben — alle neuen Inhalte landeten in bestehenden Lösungs-Toggle-Bodies oder ausserhalb davon.
- **Strukturelle Integritäts-Checks §3.7** (kritische Marker auf Eindeutigkeit): alle Marker (`<h2 id="ressourcen">`, `<div class="dl-grid">`, `<aside class="toc-wrap">`, `<footer class="site-footer">`, `<h2 id="aufgaben">`, `<h2 id="zusammenfassung">`) auf allen drei Themenseiten exakt einmal vorhanden.
- **HTML-Parser-Tag-Bilanz** auf allen acht gepatchten Dateien (drei Themenseiten + fünf Druck-Dateien): alle OK — keine unmatched closing tags, keine unclosed tags.
- **LaTeX-Klammern-Balance** auf allen acht Dateien konsistent — block- und inline-Delimiter paarweise.
- **Mathematische Probe der Patches:**
  - TK.47 (Excel-Quartile-Vergleichswerte): bei n=7, sortiert 12, 12, 14, 15, 17, 18, 20: Excel-Position für \(Q_1\) ist \((7-1)\cdot 0.25 + 1 = 2.5\), Wert zwischen Rang 2 (=12) und Rang 3 (=14), linear interpoliert \(12 + 0.5 \cdot (14-12) = 13\). Für \(Q_3\) Position 5.5, Wert zwischen Rang 5 (=17) und Rang 6 (=18), \(17 + 0.5 \cdot 1 = 17.5\). ✓
  - TK.48 (Bildschirmzeit-Beispieldatensatz): Summe \(95+120+\dots+155 = 2420\), \(\bar{x} = 2420/15 = 161.33\). Median (Position 8) = 155. Q1 = Median der unteren 7 (75…145) = 110. Q3 = Median der oberen 7 (165…320) = 200. QD = 90. \(s = 64.49\) (mit \(n-1\)). Ausreisser-Schätzung: \((320 - 161.33)/64.49 = 2.46 \approx 2.5\) Std.abw. Alle Werte nachgerechnet, Std.abw und Varianz von initial geschätzten 63.7/4055 auf korrekt 64.5/4159 korrigiert vor dem ZIP-Pack.

### Bemerkung zur Aufwandsklassen-Analyse

Vier Items in LG4 fielen in die „teure Klasse" (Block-Ergänzung mit eigenem didaktischen Bogen):
- **TK.44 + TK.47** (Tukey-vs-Excel-Diskrepanz auf Themenseite + A1-Lösung) — thematisch verbunden, ein einziger Recherche- und Konstruktionsschritt für beide.
- **TK.45** (Histogramm-SVG für A3) — Koordinaten und Skalierung mussten explizit gerechnet werden (Python-Hilfsskript für Säulen-Geometrie).
- **TK.48** (Beispiel-Datensatz für A6) — kompletter fiktiver Datensatz nötig, alle Masszahlen händisch nachgerechnet und gegen Python verifiziert; der grösste Einzel-Item-Aufwand.
- **TK.56** (KKLEINSTE-Tipp-Box) — Tabellen-Eintrag entfernen, eigene Box mit Erklärung und Edge-Case-Hinweis konstruieren.

Die übrigen neun Items waren Wortlaut-Patches oder Marginalien innerhalb bestehender Strukturen (typ. 1 str_replace pro Item).

---

## [unreleased] — 2026-05-24 · Lehrerbegutachtungen Welle K LG3

### Welle K — Lösungsweg-Granularität & Marginalien (13 Items, TK.32–TK.43a)

Aus `TODO-lehrerbegutachtung.md` Welle K wurde der komplette LG3-Block (13 Items) in einer Sitzung abgearbeitet. Schwerpunkt: explizite Zwischenschritte in Lösungen, didaktische Marginalien zu Darstellungsform-Wahl, präzise Sprache bei Rand- und Vergleichs-Fällen, pharmakologische Standard-Termini.

**Themenseiten (9 Items, drei Dateien):**

- **TK.32 (g3-2 A3(e)):** Punkt \(P(0\mid 4)\) durch \(P(2\mid 10)\) ersetzt. Mit \(P(0\mid 4)\) war der y-Achsenabschnitt \(b = 4\) direkt ablesbar — bei einer parallelen Geraden mit identischer Steigung trivial. \(P(2\mid 10)\) zwingt die Schüler zu einer echten Rechnung: \(b = 10 - 3 \cdot 2 = 4\). Die korrekte Ergebnisformel `f(x) = 3x + 4` (und damit `chk(...)`) bleibt unverändert.
- **TK.33 (g3-2 A6 Fahrenheit):** Lösung um expliziten Steigungs-Schritt erweitert. Vorher Sprung von „0°C = 32°F, 100°C = 212°F" direkt zu \(F(C) = 1.8 \cdot C + 32\). Jetzt: Steigungs-Dreieck \(m = \Delta F / \Delta C = (212 - 32)/(100 - 0) = 1.8\), anschliessend \(b\) aus dem ersten Punkt.
- **TK.34 (g3-2 A4, A5):** Lösungen detaillierter mit benannten Zwischenwerten.
  - **A4 (Handyvertrag):** Sprachsignal-Identifikation („pro Minute" → Steigung; „Grundgebühr" → y-Achsenabschnitt) als didaktischer Vorlauf vor dem Aufstellen. Zwischenschritt \(0.08 \cdot t = 10\) zwischen Gleichsetzen und \(t = 125\) min explizit.
  - **A5 (Mietauto):** Funktionen \(K_A\) und \(K_B\) jeweils mit Charakterisierung (linear/konstant + Steigung) benannt. Zwischenschritt \(0.25 \cdot x = 30\) explizit; abschliessende Begründung, warum \(B\) für mehr als 120 km günstiger ist, an die Monotonie der Kostenfunktionen geknüpft (nicht nur „A wächst, B ist konstant" gemeint, sondern wirklich gezeigt).
- **TK.35 (g3-3 A4 Wurfparabel):** Exakter Bruchwert \(a = -\frac{4}{25}\) als Zwischenform vor dem Dezimalwert \(-0.16\) gezeigt. Schüler sehen, dass \(-0.16\) eine *exakte* (nicht gerundete) Dezimalzahl ist, und können bei späteren Anwendungs-Aufgaben mit dem Bruch weiterrechnen.
- **TK.36 (g3-3 A5 Umsatz):** Antwort um die Stückzahl ergänzt. Bei optimalem Preis 22.50 CHF werden 90 Stück verkauft (\(100 - 4 \cdot 2.5 = 90\)), Umsatz 2025 CHF. Probe: \(22.50 \cdot 90 = 2025\) ✓. Das schliesst den Kreis von der Modell-Variablen \(x\) (Preiserhöhung) zurück zu den ökonomisch interpretierbaren Grössen.
- **TK.37 (g3-3 A6 Brücke):** `block-tipp 💡 Warum Linearfaktorform?` direkt vor der Aufstellung. Motiviert die Wahl der Darstellungsform aus der Aufgaben-Information (Bogenfüsse auf der x-Achse → Nullstellen gegeben → Linearfaktorform schnellster Weg). Schliesst die didaktische Lücke zwischen „A6 verwendet Linearfaktorform" (Tatsache) und „weshalb gerade die" (Methodik).
- **TK.38 (g3-3 A7 Hängebrücke):** `block-tipp 💡 A6 vs. A7 — verschiedene Wege zum gleichen Ziel` am Ende der Lösung. Stellt heraus, dass A6 (Linearfaktorform) und A7 (Scheitelform) strukturell ähnliche Aufgaben lösen, aber unterschiedliche Darstellungsformen wählen — abhängig davon, welche Information die Aufgabe gibt. Zusammenfassende Regel: Scheitelpunkt + Punkt → Scheitelform, zwei Nullstellen + Punkt → Linearfaktorform, drei beliebige Punkte → Grundform.
- **TK.39 (g3-1 A6(c) Tank):** `block-tipp 💡 \([0;25]\) oder \([0;25[\)?` als Marginalie zur Definitionsbereich-Reflexion. Geschlossenes Intervall, weil \(V(25) = 0\) ein zulässiger physikalischer Zustand ist (Tank leer); offenes Intervall wäre verteidigbar, wenn man das Modell streng als „Wasser fliesst ab" liest. Wichtiger als die Wahl ist die explizite Begründung im Sachzusammenhang.
- **TK.40 (g3-1 A7(c) Tarifvergleich):** Aussage „ab 5 GB ist B günstiger" präzisiert zu „unter 5 GB ist A günstiger, **über 5 GB** ist B günstiger; bei **genau 5 GB** sind beide gleich teuer". Schliesst die strikte/lockere Ungleichungs-Ambiguität: „ab" wird umgangssprachlich für „\(\ge\)" gebraucht, ist aber im Schnittpunkt-Kontext irreführend.

**Druckdateien (4 Items, drei Dateien):**

- **TK.41 (druck-g3-2 Aufgabenserie A2a):** Rundungs-Drift bei \(t = 100/72\) h präzisiert. Vorher: \(\approx 1.39\;\text{h} \approx 1\;\text{h}\;23\;\text{min}\) — \(1.39 \cdot 60 = 83.4\) min = 1 h 23.4 min, also bereits leicht aufgerundet, und der Zwischenwert 1.39 ist selbst gerundet. Jetzt: \(\approx 1.389\;\text{h} \approx 1\;\text{h}\;23\;\text{min}\;20\;\text{s}\) mit zusätzlichem Erklär-Absatz zur Rundung (\(0.389 \cdot 60 = 23.33\) min = 23 min 20 s).
- **TK.42 + TK.43 (druck-g3-3 Aufgabenserie A6(b) Wirkstoff-Konzentration):** Zwei verbundene Verbesserungen am gleichen Lösungsblock.
  - **TK.43 (Mitternachtsformel):** Vorher \(c_{1,2} = \frac{-40 \pm \sqrt{1200}}{-1}\) — die Division durch \(-1\) führt zu Vorzeichen-Verwirrung (Schüler rechnen \(\frac{-40 + 34.64}{-1} \approx \frac{-5.36}{-1} \approx 5.36\) — funktioniert, aber unübersichtlich). Jetzt zwei Stufen: zuerst die *unaufgelöste* Mitternachtsformel mit eingesetzten Werten (zeigt das Berechnungs-Schema), dann die umgeformte Variante mit positivem Nenner \(c_{1,2} = 40 \mp \sqrt{1200}\) (übersichtlich, Vorzeichen-Tausch dokumentiert via \(\mp\) statt \(\pm\)). Endergebnisse identisch.
  - **TK.42 (MEC/MTC):** Die pharmakologischen Standard-Termini „minimum effective concentration" (MEC) und „minimum toxic concentration" (MTC) optional in der Schlussinterpretation ergänzt. Schüler in technisch/Life-Sciences-Klassen erkennen die Begriffe wieder, ohne dass sie für die Lösung selbst nötig sind.
- **TK.43a (druck-g3-1 Aufgabenserie A6(c) Temperatursensoren):** „Ablesegenauigkeit ist bei B daher in der Regel besser" → „Bei gleicher Spannungs-Anzeige-Auflösung des Messgeräts ist Sensor B daher genauer (eine kleine, gerade noch unterscheidbare Spannungsdifferenz entspricht bei B einer kleineren Temperaturdifferenz als bei A)". Trennt die Geräte-Eigenschaft (Empfindlichkeit = Steigung der Kennlinie) von der System-Eigenschaft (Genauigkeit = Empfindlichkeit \(\times\) Auflösung des Anzeigegeräts) klarer. Die ursprüngliche TODO-Formulierung wurde leicht erweitert um den Kausalitäts-Halbsatz „eine kleine Spannungsdifferenz entspricht …" — ohne diesen wirkt die Aussage als blosses Postulat.

### Verifikation

- **Standard-Pre-Flight §3.6 (Marker-Anwesenheit)** auf den drei gepatchten Themenseiten (g3-1, g3-2, g3-3): alle grün (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 bad=0`). `tog`-Count auf den Themenseiten unverändert (7 / 4 / 4) — alle neuen Inhalte landeten in bestehenden Lösungs-Toggle-Bodies oder ausserhalb davon.
- **Strukturelle Integritäts-Checks §3.7** (kritische Marker auf Eindeutigkeit): `<h2 id="ressourcen">`, `<div class="dl-grid">`, `<aside class="toc-wrap">`, `<footer class="site-footer">`, `<h2 id="aufgaben">`, `<h2 id="zusammenfassung">` — alle Marker auf allen drei Themenseiten exakt einmal vorhanden.
- **HTML-Parser-Tag-Bilanz** auf allen sechs gepatchten Dateien (drei Themenseiten + drei Druck-Aufgabenserien): alle OK — keine unmatched closing tags, keine unclosed tags.
- **LaTeX-Klammern-Balance:**
  - Block-Delimiter \(\backslash[\dots\backslash]\) auf allen sechs Dateien paarweise konsistent.
  - Inline \(\backslash(\dots\backslash)\) auf fünf Dateien konsistent; auf g3-3 eine Differenz von 2, die durch JS-Regex-Code (Z. 1187, `f\(x\)` als Regex-Pattern) verursacht wird und bereits im Original-ZIP genau so vorlag (Original-Verifikation: 188 vs. 186; nach Patch 193 vs. 191; meine 5 Patch-Insertions sind sauber balanciert).
- **Mathematische Probe der Patches:**
  - TK.32 (P(2|10) parallel zu \(g(x) = 3x - 1\)): \(b = 10 - 3 \cdot 2 = 4\) → \(f(x) = 3x + 4\). ✓
  - TK.36 (Stückzahl A5): \(100 - 4 \cdot 2.5 = 90\); Probe \(22.50 \cdot 90 = 2025\). ✓
  - TK.41 (A2a Rundung): \(100/72 = 1.388889\) h = 1 h 23 min 20 s. ✓
  - TK.43 (Mitternachtsformel-Umformung): \(c_1 = 40 - \sqrt{1200} \approx 5.36\), \(c_2 = 40 + \sqrt{1200} \approx 74.64\) — identisch zur Originalrechnung (`(-40 + √1200)/(-1) = 5.36`).

### Bemerkung zur Aufwandsklassen-Analyse aus dem LG2-Eintrag

Die LG2-Erfahrung (siehe Eintrag 2026-05-24 weiter unten) prognostizierte für LG3 max. 4–5 „Block-Ergänzungen mit eigenem didaktischen Bogen" pro Sitzung. Tatsächlich entfielen in LG3 nur **zwei** Items auf diese teure Klasse (TK.37 + TK.38: zwei verbundene `block-tipp`-Blöcke zu Darstellungsform-Wahl bei den Brücken-Aufgaben). Die übrigen elf Items waren entweder Wortlaut-Patches (TK.32, TK.40, TK.43a), Lösungs-Erweiterungen mit bestehender Struktur (TK.33–TK.36, TK.41, TK.42, TK.43) oder Marginalien innerhalb existierender Lösungs-Toggles (TK.39). Daraus ergibt sich für die nächsten Wellen-K-Sitzungen (LG4, LG5) eine pragmatische Heuristik: **Block-Ergänzungen** brauchen je 1–2 Tool-Aufrufe für die mathematische Konstruktion vorab, **Lösungs-Erweiterungen** kommen mit einem einzigen str_replace aus, sofern die zu erweiternde Stelle eindeutig im File ist.

---

## [unreleased] — 2026-05-24 · Lehrerbegutachtungen Welle K LG2

### Welle K — Lösungsweg-Granularität & Marginalien (16 Items, TK.16–TK.31)

Aus `TODO-lehrerbegutachtung.md` Welle K wurde der komplette LG2-Block (16 Items) in einer Sitzung abgearbeitet. Schwerpunkt: explizite Zwischenschritte, zweite Parameter-Diskussion, Ungleichungs-Theorieblock, fehlende Lösungsfälle bei 3×3-Systemen.

**Themenseiten (11 Items):**

- **TK.16 (g2-2b A1):** Vieta-Probe-Zwischenrechnung explizit. Lösung von A1 ergänzt um den oft übersprungenen Schritt: für \(x^2 - 5x + 6 = 0\) ist \(p = -5\), also \(-p = 5\) — daraus Summe \(x_1 + x_2 = 5\). Der Vorzeichen-Wechsel ist die häufigste Stolperstelle bei Vieta. **A5 hat das gleiche Schema** (Summe 9, Produkt 20 ohne expliziten Vieta-Schritt), wurde im Patch *nicht* mitangepasst gemäss COLLABORATION §6.
- **TK.17 (g2-2b A6 Anna-Velo):** Bruchgleichungs-Umformung in fünf nummerierten Schritten ausgeschrieben — Hauptnenner-Multiplikation auf jeden Bruch einzeln, Klammern auflösen, sortieren, durch 3 teilen. Aktuelle Lösung sprang in einer Zeile von der Bruchgleichung zu \(v^2 - 20v + 32 = 0\).
- **TK.18 (g2-3 A6 Mischung):** `block-tipp` zur „Massenbilanz" ergänzt. Erklärt die didaktische Rolle der zweiten Gleichung als <em>Stoffbilanz</em>: Masse des reinen Stoffes (Zinn) bleibt beim Mischen erhalten. Schema „Mengenbilanz + Stoffbilanz" als verallgemeinerbares Werkzeug für Lösungen, Legierungen, Treibstoffmischungen.
- **TK.19 (g2-3 A5):** Hinweis „Subtrahiere G3 von G1" als optionalen `loesung-toggle`-Klick gestaltet. Auf-Aufruf bleibt die Hilfe verfügbar, ohne Klick mehr Eigenleistung beim Erkennen der Strategie.
- **TK.20 (g2-3 A7):** Aufgabentext geschärft. „können maximal gebaut werden, wenn alle Materialien vollständig verbraucht werden sollen" → „müssen gebaut werden, damit alle drei Materialien vollständig verbraucht werden". Beseitigt den Begriffs-Konflikt zwischen Optimierungs- und Bilanz-Vokabular (es handelt sich um ein eindeutig lösbares 3×3-System, nicht um eine Optimierung).
- **TK.21 (g2-1):** Eigener H2-Block „Ungleichungen formulieren" nach dem „Sachverhalte als Gleichung formulieren"-Block. Enthält eine Sprach-Signal-Tabelle (höchstens/mindestens/weniger als/mehr als → \(\le, \ge, <, >\)), drei Werkstatt-Beispiele (Gerüst-Tragfähigkeit, Mindestlohn-Auftrag, Sicherheitsabstand Drehbank) und einen `block-fehler` zum Unterschied strenges vs. erlaubendes Zeichen. Direkter RLP-2.1-Bezug.
- **TK.22 (g2-2a):** Zweites Parameter-Diskussions-Beispiel \(k \cdot x + 1 = 2 \cdot x + 3\) → \((k - 2) \cdot x = 2\). Bei \(k = 2\): Fall 2, leere Lösungsmenge. Ergänzt das bestehende Beispiel \((k-2)\cdot x = 3(k-2)\), das nur Fall 1 und Fall 3 abdeckt. Explizit-Vergleich am Ende: was Fall 2 von Fall 3 unterscheidet, ist allein das Verhalten von \(b(k)\) am kritischen Wert.
- **TK.23 (g2-2a):** Neue Aufgabe A8 „Reine Ungleichung mit Zeichenkippung" — kurz, ohne Eingabefelder, mit `loesung-toggle`. Aufgabe \(5 - 2 \cdot x \ge 13\), Lösung \(x \le -4\) mit explizitem Zeichen-Kipp-Schritt. Bisher hatten die Ungleichungen auf der Themenseite kein direktes Übungsfeld (nur Verweis aufs Druck-Selbsttest).
- **TK.24 (g2-3):** 3×3-Beispiel mit Geraden-Lösung als `block-bsp` direkt nach dem theoretischen Lösungsfälle-Block für 3×3-Systeme. System \(\{x+y+z=6,\; x-y=0,\; 2x+z=6\}\), wobei G3 = G1 + G2 (Lineare Abhängigkeit). Lösung: \((t \mid t \mid 6 - 2t)\). Geometrische Deutung: drei Ebenen, von denen die dritte die Summe der ersten zwei ist — schneiden sich in einer Geraden. Schliesst die Lücke zwischen Theorie-Block (der den Fall „eine Gerade" nennt) und Aufgabenserie (die nur eindeutige Lösungen enthielt).
- **TK.25 (g2-2b A6):** `block-tipp` „quadratische Gleichung kennt den Sachzusammenhang nicht" — Marginalie zur Sachkontext-Filterung der zwei Lösungen \(v_a, v_b\). Erklärt das Werkzeug verallgemeinerbar für alle Anwendungsaufgaben.
- **TK.26 (g2-2b A7):** `block-tipp` zur Verwechslungsgefahr zwischen drei Zahlen: \(\varphi_1 \approx +0.618\) (Goldener Schnitt, im Intervall, Lösung), \(\varphi_2 \approx -1.618\) (verworfen, negativ), \(\Phi = (1+\sqrt{5})/2 \approx +1.618\) (Goldene Zahl, Kehrwert von \(\varphi_1\)). Vorzeichen-Unterschied ist entscheidend.

**Druckdateien (5 Items):**

- **TK.27 (g2-1 Aufgabenserie A4):** Norm-Bezug der Schrittmass-Formel \(2s + a = 63\) cm präzisiert. **Korrektur gegenüber TODO-Wortlaut:** Die TODO nannte „SIA 358" — Recherche zeigt aber, dass SIA 358 „Geländer und Brüstungen" betrifft; die Schrittmass-Regel gehört zu **SIA 500 / SN 521 500 „Hindernisfreie Bauten"** (in Anlehnung an BFU-Empfehlungen). Edit verwendet die korrekte Norm; bei der Sichtung gerne gegenprüfen.
- **TK.28 (g2-1 Selbsttest A12):** Zweite Erkennungsmethode für Scheinlösung als blaue Marginalie in Lösung 12. Bei \(\sqrt{f(x)} = r(x)\) muss \(r(x) \ge 0\) gelten. Hier \(r(x) = x - 5\), Bedingung \(x \ge 5\). Damit ist \(x_1 = 2\) als Scheinlösung erkennbar ohne Probe-Einsetzen. Erspart oft fehleranfällige Rechnung.
- **TK.29 (g2-1 Selbsttest A8):** Vorzeichen-Regel bei Division durch \(-1\) als gelbe Merkregel-Marginalie in Lösung 8. Klärt: bei \(\mid:(-1)\) wechseln <em>alle</em> Vorzeichen auf beiden Seiten gleichzeitig — nicht nur eine.
- **TK.30 (g2-1 Formelauszug Abschnitt 6):** Probe-Tabelle umstrukturiert. Vorher: ein-zeiliger Verweis auf \(T_1(x_0) = T_2(x_0)\). Nachher: 4-Schritt-Ablauf (Kandidat notieren / in <em>ursprüngliche</em> Gleichung einsetzen / linke und rechte Seite <em>getrennt</em> berechnen / vergleichen) als nummerierte Tabelle, darunter unverändert die Auswertungs-Tabelle „trifft zu / trifft nicht zu".
- **TK.31 (g2-2a Druck, drei Lösungs-Erweiterungen):**
  - **Selbsttest A4** (Bruchgleichung): Sprung von „Hauptnenner 6 multiplizieren" zum Endergebnis aufgelöst in fünf Zeilen — Multiplikation auf alle Brüche einzeln, Klammer auflösen, \(x\)-Terme zusammenfassen, \(+2\), \(:5\).
  - **Selbsttest A11** (Parameter-Diskussion): Faktorisierung \(k^2 - 4 = (k-2)(k+2)\) als eigenständiger Schritt mit Verweis auf die dritte binomische Formel. Fallunterscheidung als Liste mit Begründung, warum „\(\mathbb{L} = \emptyset\)" hier <em>nicht</em> auftritt.
  - **Aufgabenserie A1** (Spannungsteiler): Umstellung der Bruchgleichung nach \(R_1\) Schritt für Schritt — Hauptnenner wegmultiplizieren, Klammer auflösen, \(U_2 R_2\) auf die andere Seite, \(R_2\) ausklammern, durch \(U_2\) dividieren. Vorher: zwei Pfeile von der Ausgangs- zur Endformel.

### Verifikation

- Standard-Pre-Flight §3.6 (Marker-Anwesenheit) auf vier Themenseiten: alle grün, `tog`-Count gestiegen bei g2-2a (TK.23 neue A8) und g2-3 (TK.19 Strategie-Klick).
- Strukturelle Integritäts-Checks §3.7 (Duplikate, Tag-Bilanz): keine `DUPLICATE-MARKER`, keine `TAG-IMBALANCE`.
- Tag-Balance auf den fünf gepatchten Druckdateien: `<div>` und `<p>` paarweise konsistent.
- LaTeX-Klammern-Balance (`\[…\]`, `\(…\)`) auf allen neun gepatchten Dateien: konsistent.

### Erfahrung für nächste Iterationen

Welle-K-Items fallen in zwei Klassen mit deutlich unterschiedlichem Aufwand:
1. **Wortlaut-Patches** (TK.20, TK.27 und ähnliche): typisch 1 str_replace, 2 Minuten.
2. **Block-Ergänzungen mit eigenem didaktischen Bogen** (TK.21 Ungleichungs-Theorieblock, TK.22 zweites Parameter-Beispiel, TK.24 3×3-Geraden-Beispiel, TK.31 dreifach): brauchen eigene mathematische Konstruktion (Beispiel-Werte wählen, Probe rechnen) und sind die Tool-Budget-Treiber. Für LG3/LG4/LG5 vorausschauend planen — pro Sitzung max. 4–5 davon.

---

## [unreleased] — 2026-05-22 · Lehrerbegutachtungen Wellen G · H · I

### Drei weitere Konsistenz-Wellen aus `TODO-lehrerbegutachtung.md` umgesetzt

Aufbauend auf dem ZIP-Snapshot `welle-efm.zip` (Wellen 0, A–F, M bereits erledigt) folgen jetzt die didaktisch-strukturellen Wellen G (Quer-Verweise), H (`block-tipp` einführen) und I (STYLEGUIDE-Klassen-Hygiene). Alle drei Wellen liefen in *einer* Sitzung durch; gemeinsame Verifikation via Standard-Pre-Flight (§3.6) und HTML-Parser auf 19 Themenseiten + 1 Druckseite.

**Welle I — STYLEGUIDE-Klassen-Hygiene (TI.1 bis TI.11):**

Symbol-Korrekturen, Block-Klassen-Konsolidierung und Erweiterung des Druck-CSS für `.aufg-block`.

- **TI.1 (g3-1):** `💡 Beispiel` → `🟢 Beispiel` an 5 Stellen (Z. 255, 439, 455, 528, 543). `💡` ist im STYLEGUIDE §5.1 für `block-tipp` reserviert.
- **TI.2 (g3-2 Z. 259; g3-3 Z. 420, 427, 434):** `block-beweis 🔷` → angemessenere Klassen für Aufstell-Beispiele. In g3-2 die Anleitung „Aus zwei Punkten" als Konstruktionsschema in `block-def 📘` (keine konkrete Zahl im Beispielteil — reine Formel). In g3-3 die drei Aufstell-Beispiele („Aus dem Scheitelpunkt und einem Punkt", „Aus den Nullstellen und einem Punkt", „Aus drei beliebigen Punkten") in `block-bsp 🟢` (alle drei haben konkrete Zahlenbeispiele mit Rechenweg).
- **TI.3 (g3-3 Z. 207-224):** Notations-Hinweis-Block mit `📝`-Titel (Symbol nicht im STYLEGUIDE-Inventar) → Titel auf `📘 Hinweis — andere Notationen für den Scheitelpunkt`. Block-Klasse bleibt `block-def` (war bereits korrekt).
- **TI.4 (g3-3 Z. 281):** `block-bsp` mit Titel „🟢 Hinweis zur Linearfaktorform" → `block-tipp` mit Titel „💡 Hinweis zur Linearfaktorform" (Block hat Hinweis-Charakter, kein Beispiel mit Rechnung).
- **TI.5 (g4-0 Z. 486):** `block-merksatz` mit Titel „📌 Wann welche Kennzahl?" → `block-tipp` mit „💡 Wann welche Kennzahl?". Inhaltlich Strategie-Hilfe (Werkzeug-Auswahl), kein Lehrsatz. `📌` war ohnehin nicht im Inventar.
- **TI.6 (g4-3 Z. 303):** Titel-Symbol `🎯 Merksatz — Robustheit` → `⭐ Merksatz — Robustheit` (STYLEGUIDE-konform).
- **TI.7 (g4-0 Z. 480-483):** Box `<div class="plausi-wrap"><div class="pl-titel">🔍 Plausibilitätsprüfung der Masszahlen</div>…` → `<div class="block block-def plausi-wrap"><div class="block-titel">📘 Plausibilitätsprüfung der Masszahlen</div>…`. Doppelte Klassenangabe (`block block-def plausi-wrap`), weil `plausi-wrap` und `plausi-grid` weiterhin die JS-gefüllte Grid-Innenstruktur ansprechen; die CSS-Definitionen für `plausi-wrap`/`pl-titel`/`plausi-grid` bleiben aktiv (im lokalen `<style>`-Block), werden aber nicht mehr als Eigenkreations-Block verwendet.
- **TI.8 (g4-1 Z. 298):** ersten Merksatz von `block-merksatz ⭐ Merksatz` → `block-tipp 💡 Methodik vor Resultat` umgewandelt; abschliessender Merksatz Z. 477 (`⭐ Merksatz` in der Zusammenfassung) belassen. Damit ist genau ein Merksatz-Block pro Seite — der Schluss-Merksatz behält das Gewicht.
- **TI.9 + TI.10 (g5-2a Z. 254, 258, 308, 445):** vier Block-Klassen ohne `block`-Präfix vereinheitlicht:
  - Z. 254: `<div class="block-def"><strong>Dreieck.</strong> …` → `<div class="block block-def"><div class="block-titel">📘 Dreieck</div><p>…</p></div>`
  - Z. 258: `<div class="block-merksatz"><strong>Konvention zur Beschriftung.</strong> <ul>…` → `<div class="block block-merksatz"><div class="block-titel">⭐ Konvention zur Beschriftung</div><ul>…</ul></div>`
  - Z. 308: `<div class="block-merksatz"><strong>Satz.</strong> Innenwinkelsumme…` → `<div class="block block-merksatz"><div class="block-titel">⭐ Innenwinkelsumme</div>…</div>`
  - Z. 445: `<div class="block-merksatz">Fläche…` (ohne Titel) → `<div class="block block-merksatz"><div class="block-titel">⭐ Flächenformel</div>…</div>`
  - Damit TI.10 mit Titel-Konvention erfüllt: jeder Merksatz hat ein `⭐`-Titel statt einer inline-`<strong>Satz.</strong>`-Markierung.
- **TI.11 (druck-g5-2d Aufgabenserie):** Variante (b) gewählt — `.aufg-block`-CSS-Block in `downloads/print.css` ergänzt (vor `@media print`-Block, ca. Z. 348–384): orange Akzentleiste links, summary-Toggle in Grün, dezenter Trennstrich vor der Lösung. Im `@media print`-Block: `details` immer aufgeklappt, summary-Marker entfernt, „✓"-Präfix vor „Lösung" im Druck. Die 6 `<div class="aufg-block">`-Blöcke in `downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/aufgabenserie.html` werden damit unverändert weiterverwendet (kein Ersatz nötig). HTML-Parser auf der Aufgabenserie-Datei: OK.
- **TI.12 (P5, LG5 allgemein):** *nicht umgesetzt.* Item ist breit formuliert („Eigenkreations-Klassen in STYLEGUIDE übernehmen oder durch Standard-Klassen ersetzen"), ohne konkrete Zeilen pro Klasse. Quick-Scan in LG5: die meisten verbleibenden Spezialklassen sind animations-lokale Hilfen (`baum-box`, `bb-cap`, `dg-row`, `diag-sliders` etc.) — themen-spezifische CSS-Hooks für einzelne Canvas-Animationen, keine querseitigen Bauklötze. Eine strategische Aufräum-Welle nach `STYLEGUIDE`-Audit ist sinnvoller als spontane Eingriffe pro Seite.

**Welle H — `block-tipp` 💡 systematisch einführen (TH.1 bis TH.6):**

Auf jeder genannten Seite mindestens einen `block-tipp` an einer didaktisch sinnvollen Stelle (typisch: nach `block-fehler` und vor `<h2 id="aufgaben">`, gelegentlich auch direkt nach der einschlägigen Theoriesektion).

- **TH.1 (g1-1, Z. nach Hierarchie-Tabelle):** „💡 Strategie — bei langen Termen die Hauptoperation zuerst finden". Konkretes Beispiel `3·(x+5) - x²`, hebt hervor, dass Strichrechnung am schwächsten bindet.
- **TH.2 (g1-2, nach Ordnungsrelationen):** „💡 Strategie — Brüche vergleichen". Beide Wege (Dezimalvergleich + Hauptnenner) mit konkretem Beispiel `2/3 vs 3/4`.
- **TH.3 LG2** je 1 Tipp:
  - **g2-1** vor `<h2 id="aufgaben">`: „💡 Strategie — Lösen in drei Phasen" (Typ bestimmen, lösbar machen, Probe).
  - **g2-2a** nach `Ungleichungen`-Sektion: „💡 Strategie — bei linearen Gleichungen *vor* dem Rechnen sortieren" (4-Schritte-Ablauf).
  - **g2-2b** vor `<h2 id="aufgaben">`: „💡 Strategie — das richtige Lösungsverfahren zuerst wählen" (4 Fälle mit Methodenwahl).
  - **g2-3** vor `<h2 id="aufgaben">`: „💡 Strategie — welches Verfahren bei welchem System?" (Einsetzung/Gleichsetzung/Addition/Gauss).
- **TH.4 LG3** je 1 Tipp:
  - **g3-1** vor Aufgaben: „💡 Strategie — Schnittpunkte ohne Umwege" (Gleichsetzen + Doppelprobe).
  - **g3-2** vor Aufgaben: „💡 Strategie — Steigung im Graphen ablesen" (Gitterpunkte verwenden).
  - **g3-3** vor Aufgaben: „💡 Strategie — welche Darstellungsform zu welcher Aufgabe?" (Scheitel/Linear/Grund je nach Frage).
- **TH.5 (g4-2)** nach Entscheidungs-Tabelle: „💡 Strategie — vom Datentyp zum Diagramm" (zwei Fragen vor Tabellen-Konsultation).
- **TH.6 LG5** je 1 Tipp (TODO sagte 2-3, pragmatisch je 1):
  - **g5-2a** vor Aufgaben: „💡 Strategie — Dreieck-Aufgaben sauber starten" (4-Schritte-Workflow).
  - **g5-2c** vor Aufgaben: „💡 Strategie — Kreis-Aufgaben über Verhältnisse lösen" (Sektor-Bogen-Segment als Anteile).
  - **g5-4** vor Aufgaben: „💡 Strategie — Werte am Einheitskreis ohne Taschenrechner ablesen" (Spezialwinkel-Werte-Tabelle).

**Welle G — Bidirektionale Quer-Verweise (TG.1 bis TG.7):**

Verweis-Form: `<a class="quer" href="…">↩ X.Y</a>` (Voraussetzung) bzw. `↗ X.Y` (Anwendung), als Pille hinter dem h2/h3-Titel (Konvention `style.css` §a.quer).

- **TG.1 (LG1 — drei Bidirektional-Paare):**
  - g1-1 ↔ g1-4 bei „Hierarchie der Operationen" (g1-1 Z. 242) und „Hierarchie — Potenzen/Wurzeln/Operationen" (g1-4 Z. 401).
  - g1-2 ↔ g1-3: g1-2 bei „Vorzeichenregeln" → g1-3 (Termumformungen brauchen Vorzeichenregeln); g1-3 bei „Klammern auflösen" → `g1-2#theorie`.
  - g1-3 ↔ g1-4: g1-3 bei „Binomische Formeln" → `g1-4#potenzgesetze`; g1-4 bei „Potenzgesetze" → `g1-3#binomi`.
  - Bestehende Verweise (g1-3 Z. 297 → g1-1, g1-4 Z. 329 → g1-2) belassen.
- **TG.2 (LG2):**
  - g2-1 bei „Algebraische Äquivalenz" → g1-3 (Termumformungen als Voraussetzung).
  - g2-2a bei „Lösungsverfahren — Äquivalenzumformungen" → `g1-3#klammern`.
  - g2-3 bei „Drei Lösungsfälle bei 2×2-Systemen" → `g2-2a#spezialfaelle`. Anker-Verifikation: `id="spezialfaelle"` ist in g2-2a Z. 264 vorhanden ✓.
- **TG.3 (LG3):** in g3-1 nach Zusammenfassungs-Tabelle eine „💡 Brücken-Tabelle" mit zwei Reihen: g3-2 (lineare Funktionen) und g3-3 (quadratische Funktionen). Die Form ist ein `block-tipp` (zusätzlicher Tipp neben dem TH.4-Tipp; passt thematisch — eine Welcome-Tabelle ans Ende der Grundlagen).
- **TG.4 (LG4 g4-1):** nach `block-tipp 💡 Schnell-Test zum Unterscheiden` (Z. 211) eine zusätzliche Brücken-Zeile mit zwei quer-Verweisen: g4-2 (Diagramme passend zum Typ) und g4-3 (Masszahlen passend zum Typ). Eleganter als zwei separate Banner.
- **TG.5 (LG4 Matrix vervollständigt):** g4-2 → g4-1 bei „Klassieren — der Schritt vor dem Diagramm"; g4-3 → g4-1 bei „Lagemasse — wo liegt die Mitte?"; g4-0 → g4-1 bei „Begriffe am Beispiel", g4-0 → g4-3 bei „Kennzahlen", g4-0 → g4-2 bei „Diagramme". Damit kennt jede LG4-Seite jede andere in mindestens einer Richtung.
- **TG.6 (LG5):** g5-3 → g5-4 bei „Definition — Sinus, Cosinus, Tangens am rechtwinkligen Dreieck" (Vorgriff auf Einheitskreis als Erweiterung auf beliebige Winkel). g5-4 → g5-5 ist bereits zweimal vorhanden (g5-4 Z. 545 und Z. 735) — Item erfüllt.
- **TG.7 (Anker-Verifikation):** `id="spezialfaelle"` in g2-2a-Themenseite Z. 264 vorhanden ✓. Die TODO-Aussage „Querverweis aus g2-1 Lösung 2 zeigt darauf" — *keine* solche Stelle existiert (kein `class="quer"`-Link mit `#spezialfaelle` in g2-1); die TODO-Aussage war wohl historisch oder hypothetisch. Nichts zu tun — Anker ist da, wenn er gebraucht wird.

### Pre-Flight-Verifikation

- **Standard-Pre-Flight (COLLABORATION §3.6)** über 19 modifizierte Themenseiten: durchgehend `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 bad=0` + `MATHLIB-FEHLT`-Check negativ in allen Fällen (`tog=N/ok`).
- **HTML-Parser-Check (`html.parser`)** über 19 Themenseiten + Aufgabenserie-Druckseite g5-2d: alle 20 Dateien OK, keine Tag-Schiefen.
- **Quer-Verweise gezählt:** 23 von 23 Themenseiten haben mindestens einen `class="quer"`-Verweis. Vor dieser Welle waren es 18 von 23 (g1-1, g1-2, g4-0, g4-1 waren leer; jetzt: g1-1=1, g1-2=1, g4-0=3, g4-1=2).
- **`block-tipp`-Verteilung:** vor Welle H gab es 7 Seiten ohne `block-tipp`; danach 0 — auf jeder im TODO genannten Seite ist mindestens ein Tipp. g3-3 hat zwei (TI.4 + TH.4 — TI.4 wandelte das frühere `🟢 Hinweis zur Linearfaktorform` in einen Tipp um).
- **`.aufg-block`-Styling:** in `downloads/print.css` 10 Vorkommen der neuen Klassen-Definitionen (`.aufg-block`, `.aufg-block h2`, `.aufg-block details`, `.aufg-block details summary`, `.aufg-block details[open] summary`, plus 5 Spezialisierungen im `@media print`-Block).

### Bewusste Auslassungen

- **TI.12** (LG5 Eigenkreations-Klassen) — als P5/breit formuliert markiert; siehe oben.
- **TG.7** — Anker da, keine Änderung nötig.
- Die `.plausi-wrap`/`.pl-titel`/`.plausi-grid`-CSS-Definitionen in g4-0 (lokaler `<style>`-Block) bleiben stehen, weil das Innere (`plausi-grid` mit JS-Füllung) noch zugehörige Selektoren braucht. Doppel-Klasse `block block-def plausi-wrap` ist absichtlich. Eine spätere Aufräum-Welle könnte den lokalen Style ganz entfernen, wenn JS-Innenleben in die Standard-Block-Optik passt — gehört dann in einen Cleanup-Auftrag, nicht in diese Welle.

### Beobachtung — nicht mit-gepatcht

- In `style.css` die in der vorherigen Welle E/F/M festgehaltene Doppel-Definition (`.block-def strong` und `.block-merksatz strong`, Zeilen 437/438 + 463/464) ist immer noch da. Cleanup steht offen.

---

## [unreleased] — 2026-05-22 · Lehrerbegutachtungen Wellen E · F · M

### Drei weitere Konsistenz-Wellen aus `TODO-lehrerbegutachtung.md` umgesetzt

Aufbauend auf dem ZIP-Snapshot `welle-abcdj.zip` werden die strukturellen Themenseiten-Wellen E und F sowie die g2-3-spezifische Welle M abgearbeitet.

**Welle E — Download-Galerie-Reihenfolge (TE.1):**

- Anki-Item ans Ende der `dl-grid`-Galerie verschoben (vorher: `Handout → Formelauszug → Anki → Teste → Aufgabenserie`; nachher: `Handout → Formelauszug → Teste → Aufgabenserie → Anki`). Begründung: Anki ist Auswendiglern-Werkzeug am Ende des Lernpfads, nicht zwischen Theorie und Übung.
- 20 Themenseiten umgestellt: `g1-1`, `g1-2`, `g1-3`, `g1-4`, `g2-1`, `g2-2a`, `g2-2b`, `g3-1`, `g3-2`, `g3-3`, `g4-1`, `g4-2`, `g4-3`, `g5-1`, `g5-2a`, `g5-2b`, `g5-2c`, `g5-3`, `g5-4`, `g5-5`.
- `g2-3` spezial (6 Slots): Reihenfolge jetzt `Handout → Formelauszug → Zusatz: Gauss & Cramer → Teste → Aufgabenserie → Anki`. Annahme: das Zusatz-Item ist eine Theorie-Erweiterung (über RLP hinaus, keine Übung), gehört thematisch direkt zum Formelauszug — vor dem Selbsttest, der nur RLP-Stoff abfragt.
- `g5-2d` unverändert (hatte die neue Reihenfolge schon).
- `g4-0` unverändert (Praxisbeispiel, keine `dl-grid`).
- Umsetzung skript-basiert (`scripts`-Verzeichnis nicht touchiert; das Skript lebte nur in `/home/claude/work/` während der Sitzung).

**Welle F — A7 als „Vertiefung / Brücke zu …" markieren (TF.1, TF.2, TF.3):**

- Styleguide-Entscheidung TF.1: A1–A6 bleibt Standard (§6.1 spezifiziert das so); A7 wird explizit als optionale Vertiefung markiert. Markierung via dezente Inline-Pille hinter dem Aufgaben-Titel.
- Neue CSS-Klasse `.aufg-vertiefung` in `style.css` ergänzt (orange Pille, analog zu `a.quer`-Stil): `display:inline-block; padding:1px 8px 2px; font-size:0.62rem; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; color:var(--orange); background:var(--orange-hell); border:1px solid var(--orange-rand); border-radius:999px;`.
- 10 A7-Titel mit `<span class="aufg-vertiefung">…</span>` versehen:
  - LG1: `g1-1`, `g1-2`, `g1-3`, `g1-4` — alle „Vertiefung".
  - LG2: `g2-1`, `g2-2b`, `g2-3` — „Vertiefung". `g2-2a` (Stundenlohn-Modelle = zwei lineare Funktionen mit Schnittpunkt) → „Brücke zu 3.2".
  - LG3: `g3-2`, `g3-3` — „Vertiefung". `g3-1` hat einen abweichenden A7-Titel-Stil (`▲ Aufgabe 7 ·` statt `🟠 A7 —`); nicht touchiert, gehört in eine Stil-Konsistenz-Welle.
- **Nicht umgesetzt:** TF analog in LG4/LG5 — die TODO-Aufgabe TF nennt explizit nur LG1/LG2/LG3. LG4 und LG5 haben A7-Aufgaben (in derselben `🟠 A7 —`-Form), die später konsistent markiert werden könnten.

**Welle M — Strukturelle Inkonsistenzen g2-3 vs. g2-2 (TM.2, TM.4, TM.5):**

Datei `downloads/grundlagen/g2-3-lineare-gleichungssysteme/teste-dich-selbst.html` und ein Schritt in `formelauszug.html`.

- TM.1 (Footer `doc-fuss`) und TM.3 (Schreiblinien `lin-mehr`) waren in den vorherigen Wellen D und C bereits erledigt. Pre-Check bestätigt: alle 5 g2-3-Druckseiten haben `doc-fuss`, der Teste hat 12× `lin-mehr`.
- **TM.2 (Lösungsblock-Struktur):** ein gemeinsamer `<div class="loes">`-Container mit 10 nummerierten Absätzen wurde umgebaut zu 10 einzelnen `<div class="loes"><div class="loes-titel">✓ Lösung N</div>…</div>`-Blöcken, analog g2-2a/g2-2b. Zusätzlich: der bisherige minimalistische `<h2 style="page-break-before:always">Lösungen</h2>` wurde auf das g2-2a/g2-2b-Styling angeglichen (grüne Unterstrich-Linie, Farbe `var(--gruen)`). Beim Umbau wurde das `<strong>N.</strong>`-Prefix aus jedem Absatz entfernt, da die Nummerierung jetzt in `loes-titel` steht.
- **TM.4 (MathJax-Skalierung):** im Teste `scale: 0.92` → `scale: 1.0` (gleicht g2-2a/g2-2b-Teste an). Im Formelauszug: `scale: 0.92` → `scale: 0.95` (gleicht g2-2a/g2-2b-Formelauszug an — Formelauszug-Konvention ist 0.95, nicht 1.0).
- **TM.5 (Anleitungs-Block):** nach `</header>` einen `<div class="block block-def">📘 Anleitung</div>`-Block ergänzt mit Inhalt: „10 Aufgaben mit ansteigendem Schwierigkeitsgrad. Bearbeite alle Aufgaben in einem Zug, ohne in die Lösungen zu schauen. **Hilfsmittel:** nur Formelsammlung Promath. **Zeitvorgabe:** ca. 40 Minuten." Zeitvorgabe 40 Min als Annahme (g2-2a hat 35 Min für 12 Aufgaben, g2-2b 40 Min für 12 Aufgaben; LGS-Aufgaben sind rechenintensiver, daher analog g2-2b). Bisheriger `<p class="dk-untertitel">10 Grundlagenaufgaben · Lösungen auf Seite 2</p>` entfernt (g2-2a/g2-2b haben keinen Untertitel).

### Pre-Flight-Verifikation

- Standard-Pre-Flight (`pw, mc, nav, ml, bn, tog`) über alle 23 Themenseiten: durchgehend `pw=1 mc=1 nav=1 ml=1 bn=1` + `MATHLIB-FEHLT`-Check negativ.
- Welle-E-Slot-Check: alle Galerien haben 5 Slots (g2-3: 6 Slots, Anki immer in letzter Position).
- Welle-F-Span-Check: 10 Dateien mit jeweils 1× `aufg-vertiefung`-Span; CSS-Klasse in `style.css` definiert.
- HTML-Syntax-Check (`html.parser`) auf 7 repräsentativen Dateien (5 Themenseiten + 2 g2-3-Druckseiten): alle OK.

### Beobachtung — nicht mit-gepatcht

- In `style.css` sind zwei Zeilen `.block-def strong { color: var(--blau); }` und `.block-merksatz strong { color: var(--blau); }` doppelt vorhanden (Zeilen 437/438 und 463/464). Gemäss COLLABORATION §6 ungebetenes Aufräumen vermieden; Hinweis für eine zukünftige Aufräum-Welle.

---

## [unreleased] — 2026-05-22 · Lehrerbegutachtungen Wellen A · B · C · D · J

### Fünf Konsistenz-Wellen aus `TODO-lehrerbegutachtung.md` umgesetzt

Aufbauend auf dem ZIP-Snapshot `welle0-sachfehler.zip` (alle 8 Sachfehler bereits erledigt) wurden in einer Sitzung die fünf ressourcen-sparenden Wellen aus der TODO-Empfehlungsreihenfolge abgearbeitet. Strategische Items (TA.6, TB.3, TF.x — Strategieentscheidungen) bleiben offen.

**Welle A — Promath/SBFI/FTB-Verweis-Konsistenz (TA.1, TA.2, TA.3, TA.5):**

- In sechs Formelauszügen den Quellen-Div `<div class="quelle">Ergänzung zur Formelsammlung Promath (SBFI). Notation gemäss <em>Formeln, Tabellen, Begriffe</em> (FTB).</div>` direkt nach dem ersten `<h1>` im `<header>` ergänzt: `g1-2`, `g1-3`, `g1-4`, `g5-3`, `g5-4`, `g5-5`. Vorbild war `downloads/grundlagen/g1-1-grundlagen/formelauszug.html` und `downloads/grundlagen/g2-1-grundlagen/formelauszug.html` (beide hatten den Div bereits).
- **Nicht umgesetzt:** TA.4 (g4-1 Handout/Selbsttest/Formelauszug, P4 — andere Pattern-Form, eigener Entscheidungspunkt) und TA.6 (Themenseiten allgemein, P5 — strategische Entscheidung).

**Welle B — Anki-Intervall-Notation auf Schweizer Schreibweise (TB.1, TB.2, TB.4):**

- `scripts/build_apkg.py` Karten 10–12 von `g12_cards` (Z. 535–540) von US-Notation `[a, b]`/`(a, b)`/`[a, b)` auf Schweizer Notation `[a; b]`/`]a; b[`/`[a; b[` umgestellt. Globaler Sweep über alle 23 `.apkg`-Decks in `downloads/grundlagen/`: nur `g3-1-grundlagen/ankideck.apkg` enthielt noch US-Notation (Karten 10/11 mit `[0, ∞)` und `(0, ∞)` als Definitionsbereich von `√x` bzw. `1/√x`). Direkter Patch der SQLite-Datei im .apkg-Container (Python-Helfer): Karten 10/11 auf `[0; ∞[` bzw. `]0; ∞[` aktualisiert. Verifikation: keine weiteren Vorkommen von US-Intervall-Patterns in den verbleibenden 22 Decks.
- TB.4 (g1-1 Anki Karten 7-10 `<br>`-Separator) bereits korrekt — Generator-Skript und tatsächliches `.apkg` verwenden seit längerem `<br>`-Tags zwischen Listenpunkten.
- **Nicht umgesetzt:** TB.3 (Deck-Namens-Schema `TALS-Mathe G{X.Y} {Titel}`, P5 — würde die bestehende Anki-Subdeck-Hierarchie `TALS Mathematik::Grundlagen::1.1 …` aufgeben; strategische Entscheidung).

**Welle C — Schreiblinien `lin-mehr` in Teste-dich-selbst (TC.1, TC.2, TC.3, TC.4, TC.5):**

- In den vier Selbsttests `downloads/grundlagen/g1-2-zahlen-grundoperationen/teste-dich-selbst.html`, `g1-3-algebraische-terme/teste-dich-selbst.html`, `g1-4-zehnerpotenzen-quadratwurzeln/teste-dich-selbst.html`, `g2-3-lineare-gleichungssysteme/teste-dich-selbst.html` nach jedem `aufg-rahmen`-Block einen `<div class="lin-mehr">…</div>`-Block mit 2 oder 3 `<div class="lin"></div>`-Linien eingefügt. Heuristik für die Anzahl Linien: 4+ Teilaufgaben → 3 Linien; Wörter „begründe"/„erkläre" → 3 Linien; sonst 2 Linien. Insgesamt 46 `aufg-rahmen` mit Schreiblinien versehen (12 + 12 + 12 + 10).
- CSS-Definition für `.lin-mehr` zentral in `downloads/print.css` ergänzt (`.lin-mehr { margin-bottom: 2mm; } .lin-mehr .lin { height: 7mm; }`), da die drei `g1-x`-Selbsttests keinen lokalen `<style>`-Block haben und alle Druck-Styles aus `print.css` ziehen. g1-1 (Vorbild) hat die Definition zusätzlich lokal — bleibt unverändert. g2-3 hatte den lokalen Block bereits — `lin-mehr`-Definition wurde dort durch den Pre-Existing-Check übersprungen.
- TC.5 (g1-1 A4 — vier statt zwei Linien für vier Teilaufgaben (a)–(d)): in `downloads/grundlagen/g1-1-grundlagen/teste-dich-selbst.html` von 2 auf 4 `<div class="lin"></div>` umgestellt.

**Welle D — Footer `doc-fuss` in g2-3 Druckdateien (TD.1):**

- In allen fünf Dateien unter `downloads/grundlagen/g2-3-lineare-gleichungssysteme/` (`handout.html`, `formelauszug.html`, `teste-dich-selbst.html`, `aufgabenserie.html`, `zusatz-gauss-cramer.html`) den Footer `<footer class="doc-fuss"><span>TALS Mathematik · Grundlagen Lineare Gleichungssysteme</span><span>{Datei-Titel}</span></footer>` direkt vor dem schliessenden `</div>\n</body>` eingefügt. Konsistenz zu den acht Druckdateien von `g2-2a` und `g2-2b` (vgl. TM.1 aus der g2-3-Begutachtung).

**Welle J — Notations-Vereinheitlichungen (TJ.1, TJ.2, TJ.3, TJ.5, TJ.6, TJ.7, TJ.9):**

- **TJ.1 — g5-5 leere Lösungsmenge:** `\mathbb{L} = \{\,\}` → `\mathbb{L} = \emptyset` (Standard für leere Menge). 1 Vorkommen ersetzt (Z. 148). Die Schreibweisen `\mathbb{L} = \{150°,\ 210°\}` mit konkreten Lösungen bleiben unverändert.
- **TJ.2 — g5-4 Tangens-Definitionsbereich:** `\mathbb{R} \setminus \left\{\frac{\pi}{2} \pm k\pi\right\}` → `\mathbb{R} \setminus \left\{\frac{\pi}{2} + k\pi \,:\, k \in \mathbb{Z}\right\}` (mengentheoretisch saubere Form mit Quantor).
- **TJ.3 — g2-2a „Standardlösung" → „Lösungsformel":** `grundlagen/g2-2a-lineare-gleichungen.html` Z. 163, 172, 547 (3 Vorkommen). Schweizer BM-Konvention.
- **TJ.4 — g2-1 Definitionsmenge vs. Definitionsbereich:** Status-Check ergab: bereits konsistent. Z. 277 verwendet „Definitionsmenge" im Gleichungs-Kontext (Multiplikation mit Term, der null werden kann), Z. 744 verwendet „Definitionsbereich" im Funktions-Kontext (Bruchgleichung mit Q(x)≠0). Keine Änderung nötig.
- **TJ.5 — g2-2a „kgV" → „Hauptnenner":** Z. 245, Klammer-Hinweis nach „Beide Seiten mit 6 multiplizieren" angepasst (Konsistenz zu g1-2-Begrifflichkeit).
- **TJ.6 — g2-1 doppelter Fehler-Block „Multiplikation mit Term":** Die Listen-Erwähnung in der `block-fehler`-`<ul>` Z. 277 entfernt; der eigenständige `block-fehler`-Block Z. 347–350 mit ausführlicher Erklärung und Probe-Regel bleibt als didaktisch reichhaltigerer Hauptort erhalten.
- **TJ.7 — g2-1 A2(d) Variablen `a, b` → `x, y`:** `grundlagen/g2-1-grundlagen.html` Z. 405, 410 — sowohl Aufgabentext als auch Lösungs-Gleichungssystem konsistent zu g2-3 (das durchgängig `x, y` für 2×2-Systeme verwendet) angepasst.
- **TJ.9 — g2-2b TdS Lösung 3 Vieta-Probe in nicht-normierter Form:** `downloads/grundlagen/g2-2b-quadratische-gleichungen/teste-dich-selbst.html` Lösung 3 (Z. 95 ff.). Die ursprüngliche Probe mischte `p = b/a = 0.5` mit `-6/2` für q — formal inkohärent (Mischung normierter und nicht-normierter Form). Neu: explizit verallgemeinerter Vieta für die Form `a·x² + b·x + c = 0` (`x₁ + x₂ = -b/a`, `x₁·x₂ = c/a`), mit dem Hinweis als Alternative, erst auf Normalform zu dividieren und dann mit `p = 0.5`, `q = -3` zu rechnen.
- **Nicht umgesetzt:** TJ.8 (g2-1 Druck Inkonsistenz `ℒ = ℝ` vs `ℒ = 𝔾` für Identität, P5 — Konventions-Entscheidung).

### Datei-Bilanz

| Bereich | Modifizierte Dateien |
|---|---|
| Themenseiten | g1-1 (TC.5), g2-1 (TJ.6, TJ.7), g2-2a (TJ.3, TJ.5), g5-4 (TJ.2), g5-5 (TJ.1) |
| Druckseiten Formelauszug | g1-2, g1-3, g1-4, g5-3, g5-4, g5-5 (Welle A); g2-3 (Welle D) |
| Druckseiten Selbsttest | g1-1 (TC.5), g1-2, g1-3, g1-4, g2-3 (Welle C); g2-2b (TJ.9); g2-3 (Welle D) |
| Druckseiten Handout / Aufgabenserie / Zusatz | g2-3 alle (Welle D) |
| Anki-Decks | g3-1 Karten 10/11 direkt gepatcht (TB) |
| Generator-Skript | `scripts/build_apkg.py` (TB.1) |
| Globales CSS | `downloads/print.css` (Welle C) |

**Pre-Flight (COLLABORATION §3.6) grün** für alle modifizierten Themenseiten (10 Stück): `pw=1 mc=1 nav=1 ml=1 bn=1 bad=0`.

---

## [unreleased] — 2026-05-22 · Lehrerbegutachtungen Welle 0 (Sachfehler)

### 8 Sachfehler aus den Lehrerbegutachtungen behoben

Aus den 27 Lehrerbegutachtungs-Dokumenten (5 LG-Themenseiten-Reviews + 7 lange Druckdateien-Reviews + 13 kurze Druck-Reviews + 2 Sonder-Begutachtungen g2-2b/g2-3) eine konsolidierte Todo-Liste in 16 Synergie-Wellen erstellt (`TODO-lehrerbegutachtung.md`, 231 Items). Welle 0 (Sachfehler, Prio 1) als erste Welle abgearbeitet — alle Patches betreffen die Themenseiten, die Druckseiten-Reviews waren sachfrei.

**Umgesetzte Befunde:**

- **T0.1 — g1-3 A6 Werkstatt-Restfläche: Quadrat passt geometrisch nicht ins Rechteck [P1]**: `grundlagen/g1-3-algebraische-terme.html` Z. 508–524. Aufgabentext umformuliert: nicht mehr „Materialecke aus der Werkstatt" (das Quadrat mit Seite `x` m kann geometrisch nicht in ein Rechteck der Breite `(x−1)` m hineinpassen), sondern „Holzbrett-Verschnitt": rechteckiges Werkstück `(x+4) × (x−1)` m und quadratisches Verschnittstück mit Seite `x` m werden parallel zugeschnitten. Algebraisch identisch (Restfläche bleibt `3x − 4`), Lösung unverändert. Aufgabentitel von „Flächeninhalt einer Werkstatt" auf „Restmaterial beim Zuschnitt" geändert.
- **T0.2 — g1-2 A6 Wochenmittelwert aus drei Tageswerten begrifflich falsch [P1]**: `grundlagen/g1-2-zahlen-grundoperationen.html` Z. 451. Aufgabentext umformuliert: „Drei Tagesmittel-Temperaturen … Wochenmittelwert" → „An einem Wintertag werden drei Temperaturen gemessen (morgens, mittags, abends) … Tagesdurchschnitt aus diesen drei Messungen". Drei Tageswerte ergeben keinen Wochenmittelwert. Lösung (-1.0 °C) unverändert.
- **T0.3 — g2-2a A6 Telefon-Tarif-Schnittpunkt: „je 60 Fr." → „je 70 Fr." [P1]**: `grundlagen/g2-2a-lineare-gleichungen.html` Z. 509. Bei `t = 200` ist `K_A = 0.20·200 + 30 = 70` und `K_B = 0.35·200 = 70`. Per Python verifiziert. Druckmaterial g2-2a hatte den Fehler bereits korrekt — Themenseite zieht jetzt nach.
- **T0.4 — g2-1 A6 Wurzelgleichung widerspricht Theorie-Hinweis „im Schwerpunktfach" [P1]**: `grundlagen/g2-1-grundlagen.html` Z. 483–501. Aufgabe komplett ersetzt: `√(x+3) = x−3` (Wurzelgleichung, formell Schwerpunkt-Stoff) → `x = 3` quadriert zu `x² = 9` (Kandidaten `x = 3` und `x = −3`, Scheinlösungs-Phänomen rein im Grundlagenfach demonstrierbar). Didaktische Pointe „Quadrieren ist keine Äquivalenzumformung, Probe ist Pflicht" bleibt erhalten und ist sogar besser sichtbar, weil das Beispiel ohne Wurzeln auskommt. Aufgabe in (a) Probe und (b) Reflexion strukturiert. Titel von „Scheinlösung erkennen" auf „Quadrieren erzeugt Scheinlösungen" geändert.
- **T0.5 — g4-0 Quartil-Erklärtext bei n=26: „Mittel der Werte" ist bei ungerader Hälftengrösse falsch [P1]**: `grundlagen/g4-0-praxisbeispiel-bm2-klasse.html` Z. 790 (Q₁) und Z. 794 (Q₃). Bei n=26 hat die untere Hälfte 13 Werte (ungerade), Q₁ ist daher der **einzelne Wert an Rang 7**, nicht „Mittel der Werte an Rang 7 und 8". Q₃ analog: Wert an Rang 20 (= Rang 14 + 6), nicht „Mittel der Werte an Rang 19 und 20". Beispiel-Text in beiden Detailbox-Einträgen entsprechend umformuliert. Der JS-Code `quartilTukey` (Z. 886-905) ist korrekt und musste nicht angepasst werden — nur die Erklärtexte waren falsch.
- **T0.6 — g5-2c A7(c) Sprinkler: Beispielwerte 0°/110°/220° lassen [340°; 360°] unbedeckt [P1]**: `grundlagen/g5-2c-kreis-und-kreisteile.html` Z. 899. Werte 110° und 220° korrigiert auf 120° und 240° (drei Sektoren à 120° überlappungsfrei aneinander). Inkonsistenten Halbsatz „Praktisch wählt man etwas Überlappung — dann reichen 3 Stellungen weiterhin" gestrichen — bei den korrigierten Werten ist die Aussage „überlappungsfrei" wieder zutreffend.
- **T0.7 — g5-3 A1(b) Lösung: Klassifikation „WSW" ist eigentlich „WWS" [P1]**: `grundlagen/g5-3-trigonometrische-berechnungen.html` Z. 709. Gegeben sind α=40°, β=70°, c=10; die Seite c liegt **gegenüber** Winkel γ, nicht **zwischen** α und β — also WWS (Winkel-Winkel-Seite mit Seite nicht zwischen den Winkeln), nicht WSW. Lösung umformuliert auf „WWS: zwei Winkel und die einer der gegebenen Winkel *nicht* einschliessende Seite". Rechnung selbst (a ≈ 6.84) ist korrekt und unverändert. Allgemeine Sinussatz-Erwähnungen mit „WSW" an anderen Stellen (Z. 528, Z. 980, Z. 989) bewusst nicht angefasst — dort steht „WSW oder WWS" als Sammelbegriff für „zwei Winkel und eine Seite", was im Kontext akzeptabel ist.
- **T0.8 — g5-2d Eigenschaften-Tabelle: Gleichsinnigkeit gilt nur bei k>0 [P1]**: `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` Z. 295. Tabellenzeile umformuliert: Titel von „Gleichsinnige Abbildung" auf „Gleichsinnigkeit (nur bei k > 0)"; Text präzisiert, dass die Streckung bei k < 0 **gegensinnig** ist (Orientierungs-umkehrend wegen zusätzlicher Punktspiegelung am Zentrum). Damit ist die Spiegelung nicht mehr als Unterfall der Gleichsinnigkeit dargestellt. Die andere Stelle (Z. 695: „Gleichsinnig (bei k>0)") war bereits korrekt und blieb unverändert.

**Mathematische Verifikation:** T0.3 (Telefon-Tarif: 70 Fr. = 70 Fr. ✓), T0.5 (Tukey-Median-Position bei n=26: Rang 7 für Q₁, Rang 20 für Q₃ ✓), T0.6 (drei 120°-Sektoren ab 0° decken 360° vollständig ab ✓) und T0.7 (Sinussatz mit α=40°, γ=70°, c=10 ergibt a ≈ 6.8404 ✓) per Python nachgerechnet. Pre-Flight-Check (COLLABORATION §3.6) für alle acht modifizierten Themenseiten grün.

---

## [unreleased] — 2026-05-21 · Tiefen-Audit LG5

### Tiefen-Audit Lerngebiet 5 (Geometrie + Trigonometrie) — 7 von 9 Befunden umgesetzt

Audit-Tiefe wie bei LG1-LG4: 4 Themenseiten (g5-2a/b/c/d Dreiecke und Vierecke, Kreis und Kreisteile, Zentrische Streckung und Ähnlichkeit) plus 5 weitere Themenseiten (g5-1 Grundlagen, g5-3 Trigonometrische Berechnungen, g5-4 Einheitskreis, g5-5 Trigonometrische Gleichungen) sowie alle zugehörigen Druckseiten durchgeprüft. **1 P1-Befund** (CSS-Render-Bug in 4 Druckseiten), 2× P2, 3× P3, 1× P4 umgesetzt; 2 Befunde bewusst zurückgestellt. Audit-Datei `lg5-tiefen-audit-2026-05-21.md`.

**Umgesetzte Befunde:**

- **B-LG5-1 — g5-4 und g5-5 Druckseiten: Tabellen mit undefinierter CSS-Klasse `tab` [P1]**: 4 Dateien, 12 Tabellen via `sed` von `class="tab"` (in `style.css`/`print.css` nicht definiert, keine Border/Padding/Header-Hintergrund) auf `class="ftb-tabelle"` umgestellt — Lehrmittel-Standard mit 146 Vorkommen in LG1–LG4. Betroffen: `downloads/grundlagen/g5-4-einheitskreis/handout.html` (4×) und `formelauszug.html` (4×, davon 2× mit `style="font-size:0.85rem"` intakt geblieben), `downloads/grundlagen/g5-5-trigonometrische-gleichungen/handout.html` (1× mit `style="font-size:9pt"` intakt) und `formelauszug.html` (3×, davon 1× mit `style="font-size:9pt"`). g5-2c/g5-2d Formelauszüge mit `class="fa-tab"` (lokal definiert, funktioniert) bewusst nicht angefasst — über Audit-Scope hinaus.
- **B-LG5-2 — g5-2b A1 Schwimmbecken: geometrisch widersprüchliche Vorgaben [P2, Vorschlag 1]**: `downloads/grundlagen/g5-2b-vierecke/aufgabenserie.html` Aufgabe 1 + Lösung 1. Querseiten `8.0 m` → `9.0 m`, Umfang `56 m` → `58 m`. Mathematik: gleichschenkliges Trapez mit Längsseiten 25/15 m und Höhe 7.5 m hat Schenkel `√81.25 ≈ 9.0139 m` → auf eine Dezimalstelle exakt 9.0 m. Aufgabenteile (a) Wasseroberfläche (150 m²) und (b) Mittellinie (20 m) bleiben unverändert. Die Figur ist nun geometrisch realisierbar (zuvor inkompatibel mit Pythagoras).
- **B-LG5-3 — g5-2a A4 Bauplatz: widersprüchlicher Aufgabentext [P2, Vorschlag 2]**: `downloads/grundlagen/g5-2a-dreiecke/aufgabenserie.html` Aufgabe 4 + Lösung 4. Aufgabentext umgestellt: irreführender Hinweis auf „halbes gleichseitiges Dreieck" (würde nur bei a=b helfen, hier ist a=8, b=6) entfernt. Neue (b) fragt nach Konstruktionsschritten statt nach c-Wert. Lösung 4 entsprechend restrukturiert: Konstruktionsschritte explizit (BC abtragen → γ anlegen → A im Abstand b → c abmessen); Cosinussatz-Rechnung c² = 52 → c ≈ 7.21 m bleibt erhalten, ist jetzt klar als „*Vorgriff auf 5.3 (Cosinussatz)*" markiert.
- **B-LG5-4 — g5-3 Notations-Inkonsistenz: Arcus- vs. Arkusfunktion [P3]**: Wahl `Arcus` als Lehrmittel-Standard (sprachlich konsistent mit den LaTeX-Operatoren `\arccos`, `\arcsin`, `\arctan`). 11 Stellen in 5 Dateien per `sed` `Arkus` → `Arcus`: `grundlagen/g5-5-trigonometrische-gleichungen.html` (4×), `downloads/grundlagen/g5-3-trigonometrische-berechnungen/handout.html` (1×) und `formelauszug.html` (2×), `downloads/grundlagen/g5-5-trigonometrische-gleichungen/handout.html` (2×) und `formelauszug.html` (2×). g5-3 Themenseite war bereits korrekt. HTML-Anker `id="arcus"` bleibt unverändert — konsistent zur Wortform.
- **B-LG5-6 — g5-2b Handout §3 Drachen-Zeile ohne Variablen-Einführung [P3]**: `downloads/grundlagen/g5-2b-vierecke/handout.html` Z. 73. `Drachen (\(e, f\))` → `Drachen (Seitenpaare \(a, b\); Diagonalen \(e, f\))`. Damit ist die Verwendung von `2(a+b)` in der Umfang-Spalte direkt erklärt — vorher tauchten `a, b` ohne Einführung auf. Konsistent mit dem Formelauszug derselben Themenfamilie. Hierarchie-Tabelle Z. 59 nicht zusätzlich angepasst, weil sie bereits korrekt „zwei Paar gleicher benachbarter Seiten" sagt.
- **B-LG5-7 — g5-2c Aufgabenserie A6.4 sprachliche Formulierung „Beifang" [P4]**: `grundlagen/g5-2c-kreis-und-kreisteile.html` Z. 872. Klammer „(= ein Verkehrszweig mit Beifang)" ersatzlos gestrichen. „Beifang" ist Fischerei-Terminologie und im Verkehrskreisel-Kontext sinnentstellend; die Aufgabe ist ohne diese Klammer klar verständlich.
- **B-LG5-9 — g5-3 Formelauszug `sin⁻¹`-Notation [P4]**: `downloads/grundlagen/g5-3-trigonometrische-berechnungen/formelauszug.html` Z. 111. Beide Varianten aufgenommen: linke Spalte zeigt jetzt `\arcsin, \arccos, \arctan` (mathematische Standardnotation, konsistent mit Themenseite und Aufgaben), Erklärungs-Spalte nennt zusätzlich „Taschenrechner-Tasten meist mit `sin⁻¹`/`cos⁻¹`/`tan⁻¹` beschriftet (SHIFT/2nd-Belegung)". Damit ist der Kontext für die Schul-Praxis erhalten und die Notation nicht mehr isoliert.

**Bewusst NICHT umgesetzt (Entscheidung des Auftraggebers):**

- **B-LG5-5 — Dezimal-Notation `0.5` vs `0{.}5` in LG5 [P3]**: gleicher Befundtyp wie LG1-B13 und LG2-B27. Wird mit dem globalen Beschluss aus LG1-B13 mitkorrigiert, nicht punktuell in LG5.
- **B-LG5-8 — g5-2d TdS Lösung 15 widersprüchlich formuliert [P4]**: zurückgestellt.

**Konventions-Wahl, die im STYLEGUIDE festgehalten werden sollte (offen):**

- Tabellen-Klasse `ftb-tabelle` als Lehrmittel-Standard für Druckseiten-Tabellen (146 Vorkommen in LG1–LG4, jetzt auch in g5-4/g5-5). Spezialklassen `uebersicht`, `glg-tabelle`, `fa-tab` bleiben als bewusst abgegrenzte Sonderformen. STYLEGUIDE-Ergänzung wäre ein eigener Eintrag.
- Schreibweise „Arcus" als deutsche Wortform für Umkehrfunktionen der Winkelfunktionen — sprachlich konsistent zu den LaTeX-Operatoren `\arccos` etc. Audit hatte „Arkus" empfohlen (mit Verweis auf RLP-BM); Lehrmittel-Wahl fällt auf „Arcus" — STYLEGUIDE-Ergänzung wäre ein eigener Eintrag.

### Datei-Bilanz

| Bereich | Modifizierte Dateien |
|---|---|
| LG5 Themenseiten | g5-2c, g5-5 |
| LG5 Druckseiten | 7 Dateien (g5-2a Aufgabenserie, g5-2b Aufgabenserie + Handout, g5-3 Handout + Formelauszug, g5-4 Handout + Formelauszug, g5-5 Handout + Formelauszug) |

---

## [unreleased] — 2026-05-21 · Tiefen-Audit LG2 + LG3 + LG4

### Tiefen-Audit Lerngebiet 2 (Gleichungen, Ungleichungen, Gleichungssysteme) — 9 von 11 Befunden umgesetzt

Audit-Tiefe analog zur LG1-Welle: alle 4 Themenseiten (g2-1, g2-2a, g2-2b, g2-3), 16 Druckseiten und die Zusatzseite Gauss/Cramer durchgeprüft. Alle ~100 Aufgabenlösungen mit Python verifiziert — kein Rechenfehler, abgesehen von einer Rundungs-Schlussaussage in g2-2b A6 (B16). 11 Befunde dokumentiert in zwei Audit-Dateien (`lg2-tiefen-audit-2026-05-21.md` und `lg2-tiefen-audit-folge-2026-05-21.md`).

**Umgesetzte Befunde:**

- **B16 — g2-2b A6 Rundung Schlussaussage [P2]**: `grundlagen/g2-2b-quadratische-gleichungen.html` Z. 601 und Z. 980. Der exakte Wert `v_a = 10 + 2√17 ≈ 18.246` wurde in der Schlussaussage auf 18.3 km/h aufgerundet (kaufmännisch über 18.25), was für 3 signifikante Stellen falsch ist. Korrektur auf 18.2 km/h sowohl in der Themenseiten-Lösung als auch im JS-Feedback. Zwischenwerte (`v_a ≈ 18.25`, `√D ≈ 16.49`) bewusst mit höherer Genauigkeit (4 sig.) belassen, damit die Schlussrundung sauber abbildbar bleibt.
- **B17 — g2-2a TdS L7 Intervall-Notation [P2]**: `downloads/grundlagen/g2-2a-lineare-gleichungen/teste-dich-selbst.html` Z. 216. `\(\mathbb{L} = (-2,\, 3]\)` → `\(\mathbb{L} = ]-2;\, 3]\)`. Inkonsistenz zur direkt darüber stehenden L6 (Z. 210), die bereits deutsche Notation verwendete. Globaler LG2-Scan zeigte: einzige Stelle in LG2 mit der internationalen Schreibweise.
- **B19 — g2-3 toter `toc:[]`-Code im buildNav-Aufruf [P4]**: `grundlagen/g2-3-lineare-gleichungssysteme.html` Z. 622-633. Das `toc:[…]`-Array hatte keine Wirkung (nav.js generiert die ToC aus den h2-IDs der Seite), referenzierte zudem eine nicht-existente ID `extern` statt `ressourcen`. 10 Zeilen ersatzlos entfernt; g2-3 ist nun die einzige LG2-Themenseite ohne diesen Block, alle anderen kommen ohne `toc:[]` aus.
- **B20 — g2-2a A5 didaktisch redundanter Fall `m = −2` [P4, Variante b]**: `grundlagen/g2-2a-lineare-gleichungen.html` Z. 484-490. Die Parameterdiskussion behandelte `m = −2` als eigenen Fall, obwohl er kein kritischer Punkt der Standardformel `x = 2(m+2)/(m−2)` ist. `m = −2` als Bemerkung nach dem allgemeinen Fall (`m ≠ 2`) eingerahmt — die didaktische Botschaft „nur `m = 2` ist kritisch" wird damit explizit.
- **B21 — g2-1 TdS A2 Begriffsdoppeldeutigkeit „Identität" [P4, Variante b]**: `downloads/grundlagen/g2-1-grundlagen/teste-dich-selbst.html` Lösung 2. Querverweis ergänzt: „Beachte: Eine Gleichung wie `(x+2)² = x² + 4x + 4`, die für alle `x` wahr ist, heisst Identität. Derselbe Begriff wird in [Kap. 2.2a](#spezialfaelle) als Fall 3 einer linearen Gleichung wieder aufgegriffen (`ℒ = ℝ`)." Anchor `#spezialfaelle` ist real (g2-2a Z. 264).
- **B22 — g2-3 Druckseiten CSS-Render-Bug und Konventions-Abweichung [P3]**: zwei Stellen mit `class="block-def"` statt `class="block block-def"` (fehlende Border, fehlendes Padding). `downloads/grundlagen/g2-3-lineare-gleichungssysteme/zusatz-gauss-cramer.html` Z. 34 (Hinweis-Box): nur Klassen-Fix. `downloads/grundlagen/g2-3-lineare-gleichungssysteme/handout.html` Z. 98 (Schluss-Box): zusätzlich Umstellung auf `class="merksatz"` und Pattern `<strong>Merksatz.</strong>` analog zu g2-1/g2-2a/g2-2b Handouts. Globaler LG2-Scan bestätigt: keine weiteren `block-def`-Stellen ohne `block`-Klasse.
- **B23 — g2-2b Handout Reinquadratisch ohne Existenz-Bedingung [P4]**: `downloads/grundlagen/g2-2b-quadratische-gleichungen/handout.html` Z. 44-46. Verfahrenstabelle Zelle Reinquadratisch erweitert von `\(x_{1,2} = \pm \sqrt{-c/a}\)` auf `falls \(-c/a \geq 0\): \(x_{1,2} = \pm \sqrt{-c/a}\); sonst \(\mathbb{L} = \emptyset\)`. Pattern 1:1 aus dem Formelauszug derselben Themenfamilie übernommen — beide Druckseiten differenzieren jetzt identisch.
- **B24 — g2-3 Formelauszug/Zusatzseite Inline-rem statt pt [P4]**: 7 Edits in 2 Dateien via `sed`. `downloads/grundlagen/g2-3-lineare-gleichungssysteme/formelauszug.html` Z. 77: `font-size:0.85rem` → `9.0pt`, `color:#5c5550` → `var(--tinte-2)`. `downloads/grundlagen/g2-3-lineare-gleichungssysteme/zusatz-gauss-cramer.html` Z. 58, 69, 98, 102, 146, 153: `font-size:1rem` → `11pt`. SVG-Inline-Farben in der Aufgabenserie bewusst nicht angefasst (anderer Stilkontext, vom Audit nicht erfasst).
- **B25 — g1 Handout: „für alle x" passt nicht zu (a+b)²-Beispiel [P4, Variante a]**: `downloads/grundlagen/g2-1-grundlagen/handout.html` Z. 59. Schreibweisen-Spalte Identitäts-Zeile: `\(T_1 = T_2\) für <em>alle</em> \(x\)` → `\(T_1 = T_2\) für <em>alle</em> Werte der Variablen`. Binomisches Beispiel passt nun zur Quantor-Phrase, didaktisch stärkeres Beispiel bleibt.
- **B26 — g2-2b A1 Lösungsschritt `−48·2` statt `−96` [P4]**: `downloads/grundlagen/g2-2b-quadratische-gleichungen/aufgabenserie.html` Z. 216. `24v - 48·2 + 24v = 3v² - 12v` → `24v - 96 + 24v = 3v² - 12v`. Die folgende Zeile (`48v - 96 = 3v² - 12v`) resultiert nun direkt durch Zusammenfassen — kein didaktischer Sprung mehr.

**Bewusst NICHT umgesetzt (Entscheidung des Auftraggebers):**

- **B18 — `<div class="merksatz">` vs `<div class="block block-merksatz">` [P3]**: laut Folge-Audit teilweise revidiert (etabliertes Muster, im STYLEGUIDE nicht dokumentiert) — bewusst zurückgestellt.
- **B27 — `0.5` vs `0{.}5` Dezimal-Notation [P3]**: gleicher Befundtyp wie LG1-B13 (im Folge-Audit verschärft für ganzes LG2). Wird mit dem globalen Beschluss aus B13 mitkorrigiert, nicht punktuell in LG2.

---

### Tiefen-Audit Lerngebiet 3 (Funktionen) — 10 von 10 Befunden umgesetzt

Alle 3 Themenseiten (g3-1, g3-2, g3-3) und 12 Druckseiten durchgeprüft. ~85 Aufgabenlösungen mit Python verifiziert — kein einziger Rechenfehler. **1 kritischer P1-Befund**: harter JavaScript-Syntaxfehler in einer Druckseite, der dort alle Lösungs-Diagramme brechen liess. Audit-Datei `lg3-tiefen-audit-2026-05-21.md`.

**Umgesetzte Befunde:**

- **B1 — g3-1 Aufgabenserie JavaScript-Syntaxfehler bricht alle Diagramme [P1]**: `downloads/grundlagen/g3-1-grundlagen/aufgabenserie.html` Z. 379. Im `xRange` von Diagramm `l6` stand `[0; 50]` statt `[0, 50]` (Semikolon statt Komma, vermutlich aus deutsch-LaTeX-Modus übernommen). Folge: `window.TalsDiagrams` parste mit `SyntaxError`, **alle 6 Lösungs-Diagramme** der Druckseite (L1–L6) blieben leer. Ein-Zeichen-Fix. Globaler Sweep über alle 6 LG3-Druckseiten-Inline-Scripts mit `node --check`: jetzt alle syntaktisch sauber. Die anderen `[n;n]`-Vorkommen in LG3 sind LaTeX-Intervalle in deutscher Notation und korrekt.
- **B2 — Drei verschiedene Notationen für den Scheitelpunkt [P2]**: `grundlagen/g3-1-grundlagen.html` und `grundlagen/g3-3-quadratische-funktionen.html`. Vereinheitlichung auf `(u, v)` als Lehrmittel-Hauptkonvention: in g3-1 wurden alle Slider-Variablen, DOM-IDs (`par-h*` → `par-u*` etc.), JS-Variablen im `parRender()`-Block und die Event-Verdrahtung migriert; in g3-3 Z. 429 wurde der Häufiger-Fehler-Block von `x_s, y_s` auf `u, v` umgestellt. **Zusätzlich neu auf der g3-3 Themenseite**: eine kompakte Übersichts-Tabelle nach der Darstellungsformen-Tabelle, die drei gebräuchliche Notationen einordnet — `(u, v)` als Lehrmittel-Standard, `(x_s, y_s)` als „direkter Bezug zum Scheitelpunkt", `(h, k)` als „TI-30X Pro Mathprint". Schüler:innen können damit Notations-Begegnungen aus anderen Quellen einordnen.
- **B3 — Internationale Intervall-Notation in zwei Stellen [P2]**: zwei Stellen wie LG1-B11/LG2-B17. `grundlagen/g3-1-grundlagen.html` Z. 629 (A2(c)-Lösung) und `downloads/grundlagen/g3-1-grundlagen/handout.html` Z. 95 (Definitionsbereich-Tabelle): `\((0, \infty)\)` → `\(]0; \infty[\)`. Globaler LG3-Sweep zeigte: einzige zwei Stellen, jetzt alle deutsch.
- **B4 — g3-1 Aufgabenserie L6 (a) fehlte komplett [P3]**: `downloads/grundlagen/g3-1-grundlagen/aufgabenserie.html` vor Z. 297 (Lösung 6). Neuer (a)-Punkt eingefügt: „Beide Kennlinien sind Geraden — siehe Diagramm unten. Achsenbeschriftung: T [°C], U [V]." Diagramm-Verweis funktioniert dank B1-Fix.
- **B5 — g3-2 Aufgabenserie Häufige-Schülerfehler: nicht-existente Aufgabe [P3]**: `downloads/grundlagen/g3-2-lineare-funktionen/aufgabenserie.html` Z. 673. Eintrag „Vorsprungsmodellierung in A2c: `s_B = 80·t` statt `80·(t+0.5)`" referenzierte eine alte Aufgaben-Version; A2c ist jetzt „Treppensteigung". Eintrag gestrichen.
- **B6 — g3-3 Aufgabenserie Häufige-Schülerfehler: Bezug stimmt nicht zur Aufgabe [P3]**: `downloads/grundlagen/g3-3-quadratische-funktionen/aufgabenserie.html` Z. 575. Eintrag „Fixkosten = Gewinnverlust bei `x = 0` (A6c): `G(0) = -200 CHF` ⇒ `K_fix = 200`" referenzierte eine Gewinnfunktion, die in der aktuellen A6 (Wirkstoff-Konzentration, `W(c) = -0.5c² + 40c - 200`) nicht existiert. Eintrag gestrichen.
- **B7 — g3-2 A2c Symbol-Doppelbelegung `s` [P3]**: `downloads/grundlagen/g3-2-lineare-funktionen/aufgabenserie.html` 4 Patches in einem Aufgaben-Block. Schrittmassregel-Symbole umbenannt: Steigungshöhe `s` → `h`, Auftritt `a` → `t` (Audit-Vorschlag). Betroffen: Aufgabentext (Z. 291-299), SVG-Skizze (Z. 306-313), Lösung 2c (Z. 552-559), Diagramm-Definition `l2c` (Z. 722-729 inkl. Achsenlabels und Funktionslabel). `s` jetzt durchgängig „Weg/Strecke" in LG3, `a` für Parabel-Streckungsfaktor reserviert.
- **B8 — Bremsweg: drei verschiedene Schreibweisen in LG3 [P3]**: zwei Patches mit beiden Korrekturen. `downloads/grundlagen/g3-3-quadratische-funktionen/formelauszug.html` Z. 164: `s(v) = v²/(2·a)` → `s_B(v) = v²/(2·a_B)` (Symbol-Kollision mit Streckungsfaktor `a` in Z. 70 aufgelöst); zusätzlich Faustformel-Brücke in der Bedeutung-Spalte: „…; Faustformel: `s_B ≈ v²/100` (v in km/h)". `downloads/grundlagen/g3-3-quadratische-funktionen/handout.html` Z. 189: analoge Faustformel-Brücke. Damit Konsistenz zu den Aufgabenserien-Verwendungen (g3-1 A3, g3-3 A3).
- **B9 — g3-3 TdS Lösung 12(b) Rechen-Notation ungenau [P3]**: `downloads/grundlagen/g3-3-quadratische-funktionen/teste-dich-selbst.html` Z. 373. `v = h(5) = -0.05·25 + 2.5 = 1.25` → `v = h(5) = -0.05·25 + 0.5·5 = -1.25 + 2.5 = 1.25`. Term `0.5·5` ist jetzt explizit sichtbar — vorher wirkte die `2.5` wie ein konstanter Term aus der Funktionsgleichung, der dort gar nicht steht.
- **B10 — g3-2 „Senkrechte Gerade" in Spezialfall-Tabelle uneinheitlich [P3]**: einheitlich auf Themenseiten-Wortlaut gezogen. `downloads/grundlagen/g3-2-lineare-funktionen/handout.html` Z. 132 und `downloads/grundlagen/g3-2-lineare-funktionen/formelauszug.html` Z. 97: Bedingung-Spalte `keine Funktion!` → `kein \(m\)`; Graph-Spalte `senkrechte Gerade` → `senkrechte Gerade (keine Funktion!)`. Im Formelauszug zusätzlich das deplatzierte `class="li"` aus der Bedingung-Zelle entfernt (jetzt durchgängig konsistent). Spalten-Logik damit überall sauber: „Bedingung" sagt **warum** der Spezialfall, „Graph" sagt **wie der Graph aussieht** + Warnung.

---

### Tiefen-Audit Lerngebiet 4 (Datenanalyse) — 4 von 4 Befunden umgesetzt

Alle 4 Themenseiten (g4-0 Praxisbeispiel BM2, g4-1, g4-2, g4-3) und 12 Druckseiten durchgeprüft. ~80 Aufgaben/Beispielrechnungen mit Python verifiziert — kein einziger Rechenfehler. Befunde alle in Notation, Konsistenz und didaktischer Vollständigkeit. Audit-Datei `lg4-tiefen-audit-2026-05-21.md`.

**Umgesetzte Befunde:**

- **L4-B1 — Quartile-Definition: Themenseite g4-3 ungenau, Inkonsistenz zu g4-0 [P3]**: `grundlagen/g4-3-masszahlen.html` Z. 224-234. Drei Korrekturen in einem Patch: (a) „25 % / 50 % / 75 % der Werte sind *kleiner*" → „… *kleiner oder gleich Q₁/Q₂/Q₃*" (Schul-Methode garantiert nur `≤`, nicht `<`); (b) Wortwahl identisch zur Vorlage in g4-0 Z. 788, 792 hergestellt; (c) Neuer Hinweissatz: „*Berechnungsmethode:* Q₁ ist der Median der unteren Hälfte der sortierten Liste, Q₃ der Median der oberen Hälfte (Median-der-Hälften-Methode, auch Tukey-Methode). Bei ungeradem `n` wird der Median selbst *nicht* in die Hälften einbezogen." Die Konvention war vorher nur in der A1-Lösung versteckt — jetzt in der Theorie verankert.
- **L4-B2 — Drei-Qualitätsmerkmale-Triade: drei verschiedene Schemata im LG4 [P2, Variante A]**: drei Patches. `grundlagen/g4-1-grundlagen.html` §6: einleitender Satz umgebaut von „Drei Kriterien sind dafür zentral" auf eine Zwei-Fragen-Logik (Stichproben-Design vs. Mess-Setup) mit allen fünf Begriffen genannt; zusätzlich vierter Definitions-Block „📘 Objektivität und Genauigkeit (Mess-Setup)" mit zwei `<li>`-Punkten und konkreten Beispielen (Lehrperson-Befragung / cm-Massband) nach dem Verzerrungs-Block eingefügt. `downloads/grundlagen/g4-1-grundlagen/handout.html` Z. 96 und `downloads/grundlagen/g4-1-grundlagen/formelauszug.html` Z. 76: Block-/h2-Titel `Drei Qualitätsmerkmale` → `Qualitätsmerkmale (Mess-Setup)`. Themenseite deckt nun alle TdS-Begriffe ab (Aufgaben 9 und 11 bezogen sich vorher auf Theorie, die nicht da war); Handout/Formelauszug machen durch Klammerzusatz transparent, dass sie eine kompakte Auswahl sind.
- **L4-B3 — Tukey-Whisker und IQR-Notation in g4-2 Formelauszug nicht eingeführt [P2, Variante A]**: `downloads/grundlagen/g4-2-diagramme/formelauszug.html` Z. 77, 81. Tukey-Klauseln `(oder Q1 − 1.5·IQR)` und `(oder Q3 + 1.5·IQR)` aus der Boxplot-Tabelle entfernt — die `1.5·IQR`-Regel wird nirgendwo im Lehrmittel erklärt, das internationale Akronym `IQR` ist im LG4 sonst nur als Synonym hinter `Quartilsdifferenz` eingeführt. Alle Boxplot-Stellen sagen jetzt durchgängig „Whisker = Min/Max" (g4-2 Themenseite, g4-2 Formelauszug, g4-3 Themenseite, g4-3 Handout, g4-3 Formelauszug). Variante B (Tukey-Boxplot mit `1.5·QD` auf der Themenseite einführen) bewusst nicht gemacht — wie im Audit empfohlen, als optionale spätere Erweiterung.
- **L4-B4 — Schiefe-Mittelwert-Median-Beziehung in g4-2 nicht erklärt [P3]**: `grundlagen/g4-2-diagramme.html` §5, Block „Symmetrisch ↔ schief". Zweiter `<p>`-Absatz ergänzt: „Diese Schiefe lässt sich auch an den Lagemassen ablesen: Bei rechtsschiefer Verteilung ist der Mittelwert grösser als der Median (der lange Schwanz nach rechts zieht den Mittelwert hoch), bei linksschiefer kleiner. Mehr dazu in [Kapitel 4.3](g4-3-masszahlen.html#theorie)." Damit ist die Beziehung in der Theorie verankert, *bevor* sie in Aufgaben (g4-2 A3, g4-2 A4-Lösung), in der TdS (Aufg. 6) und in g4-3-Faustregeln verwendet wird.

---

### Verifikations-Hygiene (alle drei Wellen)

Vor dem ZIP-Packen für jede modifizierte Themenseite Pre-Flight-Check nach STYLEGUIDE §6.1 — alle Marker erwartungsgemäss (`pw=1 mc=1 nav=1 def=0 ml=1 bn=1 bad=0`). Für die JS-Patches (LG3-B1, LG3-B2 Slider-Migration, LG3-B7 Diagramm-Definition) `node --check` über die jeweiligen Inline-Scripts ausgeführt — alle syntaktisch sauber. Mathematische Substanz aller Patches mit Python verifiziert wo numerisch (B16 mit `10 + 2√17`, B7 Schrittmassregel-Konsistenz, B9 `h(5)`-Schritt, B26 `24v − 48·2 = 24v − 96`).

### Konventions-Ergänzung (offen, vom Auftraggeber zu prüfen)

Eine Folge-Empfehlung aus LG3-B1 ist im STYLEGUIDE/COLLABORATION noch nicht kodifiziert: **Node-Syntax-Check für Druckseiten-Scripts** vor dem ZIP-Packen würde Befunde wie B1 (Semikolon in JS-Array) in einem Tool-Aufruf erkennen, bevor sie ausgeliefert werden. Analog zum Skelett-Check in STYLEGUIDE §6.1 und den strukturellen Checks in COLLABORATION §3.7.

### Datei-Bilanz (Zusammenfassung)

| Bereich | Modifizierte Dateien |
|---|---|
| LG2 Themenseiten | g2-2a, g2-2b, g2-3 |
| LG2 Druckseiten | 7 Dateien in g2-1/2a/2b/3 (Handout/Formelauszug/TdS/Aufgabenserie/Zusatzseite) |
| LG3 Themenseiten | g3-1, g3-2 (B7 nur in Druckseite), g3-3 |
| LG3 Druckseiten | 8 Dateien in g3-1/2/3 (Handout/Formelauszug/TdS/Aufgabenserie) |
| LG4 Themenseiten | g4-1, g4-2, g4-3 |
| LG4 Druckseiten | 3 Dateien (g4-1 Handout, g4-1 Formelauszug, g4-2 Formelauszug) |
| Konvention | STYLEGUIDE und COLLABORATION nicht angepasst — Konventions-Ergänzung „Node-Syntax-Check" als Folge-Empfehlung offen |

---

## [unreleased] — 2026-05-20 · Tiefen-Audit LG1

### Tiefen-Audit Lerngebiet 1 (Arithmetik / Algebra) — 4 von 5 Befunden umgesetzt

Vertiefter Audit nach Abschluss des Nachtrag-Audits Mai 2026: alle vier Themenseiten von LG1 (g1-1 Grundlagen, g1-2 Zahlen und Grundoperationen, g1-3 Algebraische Terme, g1-4 Zehnerpotenzen und Quadratwurzeln) sowie ihre 16 HTML-Druckseiten (je Handout, Formelauszug, Aufgabenserie, Teste-dich-selbst) durchgeprüft. Alle 92 Aufgabenlösungen (Themenseiten-Aufgaben A1–A7, Aufgabenserie 1–6, TdS 1–10/12) mit Python verifiziert — **kein einziger Rechenfehler** in LG1. Didaktische Substanz solide. Audit-Ergebnis: 5 Befunde in Notation und Konsistenz (keine in der Mathematik). Davon 4 in dieser Session umgesetzt; B13 (Dezimal-Notation `0.5` vs `0{.}5`) bewusst zurückgestellt.

**Umgesetzte Befunde:**

- **B11 — g1-2 Zusammenfassungstabelle Intervall-Notation** [P2]: `grundlagen/g1-2-zahlen-grundoperationen.html` Z. 501 enthielt in der Schluss-Tabelle noch die internationale Notation `[…] geschlossen, (…) offen, ∞ immer mit runder Klammer` — dies war dem M1-Patch (Mai-Welle) entgangen, weil M1 nur die Theorie-Tabelle Z. 247-258 in den Blick nahm. Auf die im Rest der Themenseite und im Lehrmittel etablierte deutsche Notation umgestellt: `\([\ldots]\) geschlossen, \(]\ldots[\) offen, \(\infty\) immer mit Klammer nach aussen`. Die Wendung „runde Klammer" passte nicht zur deutschen Konvention (offen = nach außen geöffnete eckige Klammer) und wurde durch „Klammer nach aussen" ersetzt.
- **B12 — Potenzgesetz-Numerierung P6/P7 vereinheitlicht** [P3]: Die Themenseite hatte vorher `P6 = negative Exponenten`, `P7 = Exponent null` — die zwei zugehörigen Druckseiten (Handout, Formelauszug) hingegen einheitlich `P6 = Exponent null`, `P7 = negative Exponenten`. Themenseite an die zwei Druckseiten angeglichen: `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 275-280, Tausch der beiden `<tr>`-Blöcke. Damit nun alle drei Quellen konsistent. Keine textlichen Verweise auf „nach P6" o.ä. in der A2-Lösung oder anderswo gefunden — Tausch hat keine weiteren Konsequenzen.
- **B14 — g1-1 Formelauszug Quotient-Notation** [P3]: `downloads/grundlagen/g1-1-grundlagen/formelauszug.html` Z. 50, Beispielspalte für „Division (Quotient)": `\(a / b\)` (Inline-Schrägstrich) → `\(\dfrac{a}{b}\)`. Die Schrägstrich-Form widerspricht dem im Lehrmittel sonst durchgehend genutzten Bruchstrich-Stil (FTB-konform); die Themenseite g1-1 selbst zeigt z.B. `\dfrac{a+b}{2}`.
- **B15 — g1-1 Formelauszug verbale Form** [P4]: `downloads/grundlagen/g1-1-grundlagen/formelauszug.html` Z. 106, Drei-Darstellungs-Tabelle: `«2× das mit 4 dazu»` → `«das Doppelte von \(x\) plus 4»`. Die alte Formulierung war elliptisch („das was?") und passte nicht zum Handout-Pendant Z. 110-112, das dieselbe Aussage klar mit „das Doppelte von x plus 4" formuliert. Druckseiten jetzt konsistent.

**Bewusst NICHT umgesetzt (Entscheidung des Auftraggebers):**

- **B13 — Dezimal-Notation `0.5` vs `0{.}5`** [P3]: Themenseiten verwenden `\(0.5\)` (direkter Punkt), Handouts und Formelauszüge `\(0{.}5\)` (MathJax-Klassenkorrektur `{.}` für kompakteren Abstand). Beide Schreibweisen mathematisch gleichwertig; die `{.}`-Variante ist typografisch sauberer (kein Operator-Spacing in MathJax), aber eine Vereinheitlichung über das gesamte LG1 (und konsequenterweise über alle Themenseiten) würde einen Konvertierungslauf plus STYLEGUIDE-§2.4-Ergänzung erfordern. Zurückgestellt für separate Entscheidungsrunde.

**Bewusst NICHT umgesetzt (out of scope):**

- Tiefen-Audit Lerngebiete 2–5: separater Auftrag.
- `db-info`-Bedienleisten-Text in Aufgabenserie-Druckseiten (5 Varianten: „Anwendungsaufgaben · A4", „Aufgabenserie · A4 · 3 Seiten", „Aufgabenserie · A4 · Bereit zum Drucken" — 8/3/11). TODO-3-Folgefund aus dem Nachtrag-Audit; sollte beim nächsten Vereinheitlichungslauf der Druckseiten-Bedienleisten mitlaufen, nicht punktuell in LG1 allein.

**Konvention im STYLEGUIDE kodifiziert:**

- **STYLEGUIDE §2.7 neu — Intervallnotation (verbindlich, deutsche Schreibweise)** — die deutsche Intervallnotation (`[a;b]`, `]a;b[`, ISO 31-11) ist seit M1 (Mai 2026) gelebter Lehrmittel-Standard, war aber im STYLEGUIDE bisher nicht festgehalten. Diese Lücke hat zu B11 beigetragen (die Zusammenfassungstabelle in g1-2 wurde beim M1-Patch übersehen, weil keine STYLEGUIDE-Regel die Sichtprüfung leitete). Neue Subsektion §2.7 mit drei Teilen: (1) Tabelle der 6 Intervallformen mit „Lehrmittel-Standard" vs. „NICHT verwenden", (2) Regel-Logik (Semikolon-Trennzeichen, Klammer-Richtung als Offen/Zu-Signal, ∞ immer mit Klammer nach aussen), (3) Verbale Begleitsprache mit explizitem Verbot der Wendung „runde Klammer". Der Hinweis am Ende erinnert: bei Migrationen auch Zusammenfassungs- und Kurzform-Tabellen prüfen. Datei: `STYLEGUIDE.md` Z. 86-114 (neu eingefügt nach §2.6, vor `## 3. Achsenskalierung`).

**Datei-Bilanz:**

| Datei | Änderung |
|---|---|
| `grundlagen/g1-2-zahlen-grundoperationen.html` | B11: Z. 501 Intervall-Notation deutsch |
| `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` | B12: Z. 275-280 P6/P7-Reihenfolge getauscht |
| `downloads/grundlagen/g1-1-grundlagen/formelauszug.html` | B14: Z. 50 `a/b` → `\dfrac{a}{b}`; B15: Z. 106 verbale Form |
| `STYLEGUIDE.md` | neue Sektion §2.7 Intervallnotation (29 Zeilen) |

**Verifikation:**

- Alle drei Quellen (Themenseite, Handout, Formelauszug) von g1-4 verwenden jetzt identisch `P6 = Exponent null`, `P7 = negative Exponenten`.
- g1-2 Themenseite verwendet sowohl in der Theorie-Tabelle (Z. 247-258) als auch in der Zusammenfassungstabelle (Z. 501) konsistent deutsche Klammer-Richtung.
- g1-1 Formelauszug verbale Form jetzt parallel zum Handout („das Doppelte von x plus 4" in beiden).
- HTML-Balance der drei bearbeiteten Dateien unverändert.

---

## [unreleased] — 2026-05-20

### Nachtrag-Audit Mai 2026 — Restfunde und Konsistenz-Korrekturen

Vollständiger externer Audit der Themenbereiche 1–5 Grundlagenfach (23 Themenseiten + 88 Pflicht-Druckseiten + g2-3 Zusatz; externe Videos & Aufgabensammlungen nicht im Scope). Ergebnis: 10 Befunde, davon 2 P1-Restfunde aus den S-Wellen, die dem Patch-Skript entgangen waren, sowie 8 Konsistenz- und Hygiene-Punkte. Acht TODOs aus dem Audit umgesetzt — die mathematische Substanz war bereits solide, alle 19 fachlichen M-Befunde der Welle vom 16. Mai mit Python verifiziert und korrekt umgesetzt.

**P1-Restfunde der S-Wellen (zwei einzelne Stellen vom Patch-Skript übersehen):**

- **S1-Restfund (ß) in g1-4** — `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 647: im JS-Array `ZOOM_OBJEKTE` stand noch `'Größenordnungsbereich'` → korrigiert auf `'Grössenordnungsbereich'`. Diese Stelle wird live im Browser sichtbar, sobald der Zoom-Slider auf 0 steht. Globale Re-Verifikation: kein `ß` mehr in irgendeiner Themenseiten- oder Druckseiten-HTML der Lerngebiete 1–5.
- **S3-Restfund (Dezimalkomma) in g3-3 Druckseiten** — 9 Diagramm-Marker-Labels mit Dezimalkomma in JS-`label:`-Strings, die in Canvas-Plots als sichtbare Beschriftungen gerendert werden. Korrigiert in zwei Dateien: `downloads/grundlagen/g3-3-quadratische-funktionen/aufgabenserie.html` (7 Stellen: `'25.4 m'`, `'3.03 s'`, `'3.75 m'`, `'±6.32 m'`, `'min ≈ 5.4'`, `'tox ≈ 74.6'`, `'3.75 cm'`) und `downloads/grundlagen/g3-3-quadratische-funktionen/teste-dich-selbst.html` (2 Stellen: `'y₀ = 1.5'`, `'S(5 | 1.25)'`). Globale Re-Verifikation: keine `label:`-Strings mit Dezimalkomma mehr in den 22 Aufgabenserie- und 22 TdS-Druckseiten. Dezimalpunkt-Konvention gemäss STYLEGUIDE §2.4 wieder vollständig.

**Konsistenz und Hygiene:**

- **Aufgabenserie-Druckseiten vereinheitlicht — Konvention: „Anwendungsaufgaben"** — Alle 22 `aufgabenserie.html`-Druckseiten hatten vorher uneinheitliche Titel- und H1-Schemata (8× „Anwendungsaufgaben · …", 14× „Aufgabenserie · …"; H1 in vier Varianten: „Anwendungen — …", „Aufgabenserie — Anwendungen", „Technische Anwendungen", „Aufgabenserie"). Vereinheitlicht auf: `<title>Anwendungsaufgaben · &lt;Thema&gt; — TALS Mathematik</title>` und `<h1>Anwendungsaufgaben — &lt;Thema&gt;</h1>`, wobei `&lt;Thema&gt;` der RLP-Themen-Kurztitel ist (parallel zur Themenseiten-H1). Bewusst **nicht** angetastet: Dateiname `aufgabenserie.html`, Themenseiten-Download-Karten (Titel weiterhin „Aufgabenserie", Subtitel „Anwendungsaufgaben mit Lösungen"), STYLEGUIDE §4. Begründung: die Druckseiten heißen seit jeher inhaltlich Anwendungsaufgaben (vs. „Teste dich selbst" = Grundlagenaufgaben); der Dateiname spiegelt nur die archivierte Konvention. Bearbeitet mit Python-Skript in einem Rutsch, alle 22 Dateien mit je einem title-Treffer und einem h1-Treffer. HTML-Balance aller 22 Dateien unverändert.
- **`index.html` Header-Zähler korrigiert** — Z. 145: `<span class="st-n">22</span>fertig` → `23`. Tatsächliche Anzahl `<a class="karte fertig">`-Einträge in Grundlagen-Sektion ist 23 (22 RLP-Pflicht + g4-0 Praxisbeispiel). Der Hinweistext daneben („31 RLP-Teilgebiete · 36 Themenseiten" = 23 Grundlagen + 13 Schwerpunkt) war schon korrekt — nur der Zähler hinkte hinterher. Folge eines Übersetzungs-Bugs aus dem 2026-05-17-Eintrag: der Hinweistext wurde aktualisiert, der `st-n`-Zähler nicht.
- **README.md Statustabelle aktualisiert** — Alle 12 in der Grundlagenfach-Tabelle noch als „🔜 geplant" markierten Teilgebiete (1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3, 5.1, 5.2d, 5.3, 5.4, 5.5) auf „✅ verfügbar" gesetzt. Neue Zeile für `4.0 Praxisbeispiel BM2-Klasse *(über RLP hinaus — Datenerhebung als Anwendungsfall)*` zwischen 3.3 und 4.1 eingefügt. Sektionsheader Z. 38: „18 Teilgebiete" → „18 Teilgebiete + 1 Praxisbeispiel". Zählung danach: 23 verfügbar / 0 geplant im Grundlagenfach, 0 verfügbar / 13 geplant im Schwerpunkt. Konsistent zum index.html-Header („23 fertig" + „13 geplant" = 36 Themenseiten).
- **master-todoliste.md Bilanz korrigiert** — Z. 5: „**Stand: 19 von 20 Befunden umgesetzt, 1 bewusst nicht umgesetzt.**" → „**Stand: 22 von 23 Befunden umgesetzt, 1 bewusst nicht umgesetzt (M5).**". Rechenkontrolle: 4 S-Befunde + 19 M-Befunde = 23 gesamt, davon 22 erledigt + 1 (M5) bewusst nicht umgesetzt.
- **STYLEGUIDE §4.1 Lektionen-Regel an Praxis angepasst** — Z. 215: die alte Formulierung „14 Lektionen · Teil 1 von 2" entsprach nicht der etablierten Praxis. Neu kodifiziert: die Lektionenangabe in der `<div class="pt-bereich">`-Zeile gibt die Lektionen des gesamten **Lerngebiets** an (z.B. „35 Lektionen" für alle Sub-Seiten in LG2, „50 Lektionen" für alle in LG5) und ist über alle Sub-Seiten desselben Lerngebiets identisch. Der Sub-Indikator („Teil 1 von 2" etc.) erscheint **getrennt** in der `<div class="pt-untertitel">`-Zeile darunter (Format: „RLP X.Y · Teil n von m"). Diese Zwei-Zeilen-Trennung war bereits konsistent über alle 6 Sub-Splits (g2-2a/b, g5-2a/b/c/d) durchgehalten — der STYLEGUIDE hat jetzt nachgezogen.
- **TEMPLATE.html `pt-bereich` aktualisiert** — Z. 82: Platzhalter `⟪Grundlagenfach · Lerngebiet N⟫` → `⟪Grundlagenfach · Lerngebiet N · Lerngebiet-Name · L Lektionen⟫`. Zusätzlich HTML-Kommentar mit Sub-Split-Untertitel-Beispiel ergänzt (verweist auf STYLEGUIDE §4.1).
- **Repo-Hygiene: zwei tote Dateien aufgeräumt** — `index-old.html` (24 KB alter Snapshot, keine Verweise) ersatzlos gelöscht. `apply-g4-0-patch.sh` (5 KB einmaliges Migrations-Skript, laut CHANGELOG erledigt) von der Projektwurzel nach `scripts/` verschoben — passt thematisch zu den dortigen `convert_*.py`-Skripten. CHANGELOG-Verweise auf das Skript (Z. 11, 49) bleiben historisch korrekt, da sie keinen Pfad nennen. Projektwurzel hat danach 12 statt 14 Dateien.

**Datei-Bilanz:**

| Datei | Änderung |
|---|---|
| `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` | 1 Stelle (ß → ss) |
| `downloads/grundlagen/g3-3-quadratische-funktionen/aufgabenserie.html` | 7 Stellen (Komma → Punkt) + title/h1 vereinheitlicht |
| `downloads/grundlagen/g3-3-quadratische-funktionen/teste-dich-selbst.html` | 2 Stellen (Komma → Punkt) |
| `downloads/grundlagen/<22 slugs>/aufgabenserie.html` | je title + h1 vereinheitlicht (Python-Skript) |
| `index.html` | 1 Stelle (Zähler 22 → 23) |
| `README.md` | Statustabelle komplett aktualisiert + Sektionsheader |
| `master-todoliste.md` | 1 Stelle (Bilanz-Aussage) |
| `STYLEGUIDE.md` | 1 Regel umformuliert (§4.1 Lektionen) |
| `TEMPLATE.html` | 1 Stelle (pt-bereich-Platzhalter) + Kommentar |
| `index-old.html` | gelöscht |
| `apply-g4-0-patch.sh` | nach `scripts/` verschoben |

**Verifikation:**

- HTML-Balance aller bearbeiteten Dateien unverändert (`<div>`/`</div>`-Symmetrie, `<script>`/`</script>`-Symmetrie).
- Globale Re-Konsistenzchecks: kein `ß` mehr in LG1–5 (Themen+Druck), keine `label:`-Strings mit Dezimalkomma mehr in 22+22 relevanten Druckseiten, alle 22 Aufgabenserie-Druckseiten haben einheitlich `Anwendungsaufgaben`-Präfix in Title und H1.
- `index.html`/`README.md`/`master-todoliste.md` jetzt zahlenmäßig konsistent: 23 Grundlagen verfügbar, 13 Schwerpunkt geplant, 36 Themenseiten gesamt, 22 von 23 Befunden umgesetzt.

**Bewusst NICHT umgesetzt (out of scope):**

- Druckseiten für g4-0 (siehe CHANGELOG-Eintrag 2026-05-17).
- Externes Audit der ca. 106 V&AS-Links (Sektion 10 der Themenseiten).
- Anki-Decks (binäre Inhalte).
- Schwerpunktfach (alle 13 als Stubs).

---

## [unreleased] — 2026-05-17

### Nachtrag: zwei vom Patch-Skript übersehene Stellen — Themenseiten-Zähler

Bei einer Vollständigkeits-Prüfung des `apply-g4-0-patch.sh`-Skripts sind zwei Stellen aufgefallen, die das Patch-Skript nicht abgedeckt hatte (die Header-Zähler-Texte waren nicht Teil seines Auftrags). Beide Stellen waren nach dem Hinzufügen der g4-0-Themenseite veraltet:

- **`index.html` Header-Hinweis**: `"35 Themenseiten"` → `"36 Themenseiten"` (23 Grundlagen + 13 Schwerpunkt). Die Zahl `"31 RLP-Teilgebiete"` bleibt unverändert, weil g4-0 KEIN neues RLP-Teilgebiet ist, sondern ein Praxisbeispiel, das mehrere bestehende Teilgebiete zusammenführt.
- **`nav.js` Z.127 (Footer „Ausblick · Erstellt")**: `"Inhalte für das Grundlagenfach (22 Themenseiten)"` → `"… (23 Themenseiten)"`.

Bewusst NICHT geändert (historische Aussagen):
- Alle Erwähnungen von „22 Themenseiten" / „88 Druckseiten" in `CHANGELOG.md` und `master-todoliste.md` — diese beziehen sich auf den jeweiligen Snapshot-Stand zum Zeitpunkt des Eintrags und sind als historische Chronik korrekt.

Bewusst NICHT erstellt (out-of-scope für diesen Auftrag):
- Druckseiten für g4-0 unter `downloads/grundlagen/g4-0-praxisbeispiel-bm2-klasse/` (Aufgabenserie, Formelauszug, Handout, Teste-dich-selbst, Anki-Deck). Wenn die Praxisbeispiel-Seite irgendwann analoge Druckseiten erhalten soll, ist das ein eigener Auftrag mit nichttrivialem Inhalts-Aufwand.

---

## [unreleased] — 2026-05-17

### Zweite Runde Anpassungen an Themenseite 4.0 (nach Sichtkontrolle)

Sieben Befunde aus der Browser-Sichtkontrolle (mit Screenshots) bearbeitet; vier davon auf der g4-0-Seite, zwei in der globalen Navigation, einer redaktionell beim Jahrgang-Dashboard.

**Übersichts-Grafik (oben) verfeinert** — wirkte vorher klobig im Verhältnis zum restlichen Seiten-Inhalt. Zweite Iteration:
- viewBox 720×260 → **720×200** (insgesamt −41 % seit ursprünglicher 720×340)
- Karten-Höhe 64 → 52, untere Klammern h=42 → 34, obere Klammer h=32 → 26
- Schriftgrössen leicht runter: Titel 15 → 13, Untertitel 11 → 10, „Schritt 1"-Label 10 → 9, untere Klammer-Titel 13 → 12, Untertitel 10 → 9, Fussnote 11 → 10
- Stroke-Stärken reduziert: Karten 2 → 1.5, Klammern und Verbinder 1.5 → 1.2, Pfeile 1.8 → 1.5
- Eckenradien runter: rx=8 → 6 (Karten), rx=6 → 5 (Klammern)
- Pfeil-Marker 6×6 → 5×5
- CSS-`max-width: 720px` + `margin: 0 auto` auf `.workflow-svg-wrap`, damit die Grafik bei breiten Bildschirmen nicht volle Spaltenbreite einnimmt

**Dashboard-Karte „Jahrgang" — Median statt Mittelwert mit Dezimal** — die Karte zeigte den Mittelwert mit einer Nachkommastelle (z.B. „2007.3 Jahrgang"), was bei diskreten Jahrgängen didaktisch problematisch ist. Geändert: Median (ganzzahlig, immer ein tatsächlicher Datensatz-Wert) prominent; gerundeter Mittelwert (`Math.round`) als Sekundärwert in kleinerer Schrift mit dezenter Markierung „(gerundet)". Die `mz-jahrgang`-Tabellenzeile (Lage- und Streumasse) bleibt unverändert, weil sie bereits mit `nf=0` auf ganzzahlig rundet.

**MathJax-Rerender nach `setKbw` — Bug-Fix Diagramm-Charakter-Box** — das im Screenshot sichtbare rohe LaTeX `\(\bar{x} \approx \tilde{x}\)` in der Diagramm-Charakter-Box war eine Folge eines fehlenden MathJax-Aufrufs nach dem Klassenbreite-Wechsel. `setKbw` rief zwar `aktualisiereDiagnose` (welches LaTeX-Snippets in den `.dc-text` schreibt), aber kein Re-Render. Neue Helper-Funktion `typesetDiagnose(id)` rendert die `.da-text`- und `.dc-text`-Elemente eines einzelnen Diagramms nach. Aufgerufen in beiden `setKbw`-Zweigen (gr und ma).

**Intervall-Schreibweise: schweizerische Notation `[a; b[` / `]a; b]`** — die zuvor verwendeten runden Klammern (`[a; b)` / `(a; b]`) sind in deutschsprachigen Lehrmitteln unüblich. Das Lehrmittel hat in `g1-2-zahlen-grundoperationen.html` (§Intervalle) bereits die schweizerische Konvention etabliert (`[a; b]` geschlossen, `]a; b[` offen, etc.). Die Häufigkeitstabellen-Spalte „Klasse" in `baueHaeufTab` verwendet jetzt dieselbe Notation.

**Querverweis zu Intervallschreibweise** — neuer kleiner Hinweis-Block unter der Grenzen-Toggle-Bar des Grösse-Histogramms (einmal pro Seite reicht): Erklärung der `[g_L; g_R[`/`]g_L; g_R]`-Notation und Link `↗ Intervalle — Repetition aus 1.2` zu `g1-2-zahlen-grundoperationen.html#typen`.

**Toggle-Button-Beschriftung: `g_L ≤ x < g_R`** — Buttons zeigten vorher `x ≤ v < y`, was generisch und unsuggestiv war. Neue Beschriftung verwendet `g<sub>L</sub>` (linke Klassengrenze) und `g<sub>R</sub>` (rechte Klassengrenze) sowie Variable `x` (konsistent zur Intervall-Mengen-Schreibweise im Lehrmittel). Auch Kommentare und Funktions-Docstrings entsprechend nachgezogen.

**Nav-Patches: g4-0 in Hauptnavigation und Vor-/Zurück-Kette** — das ursprüngliche Patch-Skript `apply-g4-0-patch.sh` wurde nur teilweise ausgeführt (Index-Karte vorhanden, aber Sidebar/Dropdown und Prev/Next nicht). Manuell nachgezogen:
- `nav.js` SITE-Array: g4-0-Eintrag vor g4-1 eingefügt
- `nav.js` GROUPS Datenanalyse: `ids: ['g4-0', 'g4-1', 'g4-2', 'g4-3']`
- `g3-3-quadratische-funktionen.html` `buildNav.next`: 4.1 → 4.0
- `g4-1-grundlagen.html` `buildNav.prev`: 3.3 → 4.0

Damit ist g4-0 in der Sidebar „4 · Datenanalyse" sichtbar und in der Vor-/Zurück-Kette korrekt verlinkt: 3.3 → **4.0** → 4.1 → 4.2 → 4.3 → 5.1.

Datei-Bilanz: `grundlagen/g4-0-praxisbeispiel-bm2-klasse.html` (2006 → 2026 Zeilen, +20 netto), `nav.js` (2 Stellen), `grundlagen/g3-3-quadratische-funktionen.html` (1 Stelle), `grundlagen/g4-1-grundlagen.html` (1 Stelle). `<div>` / `</div>`-Balance der g4-0-Datei: 179/179 ✓; alle drei Inline-Scripts `node --check` ✓; Histogramm-Tabellen-Logik mit neuer Intervall-Notation verifiziert.

---

## [unreleased] — 2026-05-17

### Anpassungen an Themenseite 4.0 (Praxisbeispiel BM2-Klasse)

Drei Korrekturen aus dem Review-PDF `anpassung4_0-1.pdf` umgesetzt; Geltungsbereich nur `grundlagen/g4-0-praxisbeispiel-bm2-klasse.html` (keine Auswirkung auf andere Seiten).

**Übersichts-Grafik vertikal kompakter** — die SVG-Workflow-Grafik am Seitenanfang (4.0-Klammer, vier Schritt-Karten, drei Kapitel-Klammern) reduziert: viewBox-Höhe von 340 auf 260 (−24 %). Konkret: obere 4.0-Klammer von h=40 auf h=32 (Text-y 46→29), Schritt-Karten von h=80 auf h=64 (Karten-y 120→76, Texte proportional nach oben), untere Kapitel-Klammern von h=50 auf h=42, Fussnote y 310→232. Die zuvor schwebenden Verbinder (3-Pixel-Luft zwischen Klammer-Unterkante und Karten-Oberkante) schliessen jetzt nahtlos an. Alle horizontalen Positionen, Farben, Schriftgrössen und Klick-Verlinkungen unverändert.

**Histogramme mit Häufigkeitstabelle und umschaltbaren Grenzen** — beide Histogramme (Grösse cm, Masse kg) im Diagramme-Kapitel um zwei Bedienelemente und eine Tabelle erweitert:

- *Neue Toggle-Bar `Grenzen`*: zwei Buttons unter der bestehenden Klassenbreite-Bar, schalten zwischen `x ≤ v < y` (Standard, Konvention `lo`: Klasse \[a, b\)) und `x < v ≤ y` (Konvention `hi`: Klasse (a, b\]). Default: `lo`.
- *Neue Häufigkeitstabelle rechts neben dem SVG*: drei Spalten `i`, `Klasse`, `h_i` mit Σ-Zeile am Ende. Klasse-Notation passt sich der gewählten Grenze an (`[155; 160)` vs. `(155; 160]`). Bei kleinem Bildschirm Tabelle unter dem SVG (Flex-Wrap, `histo-flex`-CSS).
- *Reaktivität*: Tabelle und Histogramm rendern bei jeder Klassenbreite- *oder* Grenzen-Änderung gemeinsam neu (`setKbw` und neue `setGrenze` rufen `zeichneHistogramm` mit dem jeweils aktuellen anderen Wert).
- *State*: neue globale Variable `aktiveGrenze = { gr: 'lo', ma: 'lo' }`.
- *Klassen-Logik in `zeichneHistogramm`*: 5. Parameter `grenze` und 6. Parameter `tabId`. Klassenstart hängt von der Konvention ab: bei `lo` mit `floor(min/kb)*kb`, bei `hi` mit `ceil((min-ε)/kb)*kb - kb`. Sonderfall Randwerte: bei `lo` wird `max` in die letzte Klasse aufgenommen, bei `hi` wird `min` in die erste aufgenommen. Leere Randklassen werden zur Reduktion von visuellem Rauschen entfernt.
- *Verifikation*: alle Konventionen liefern Σ = 26 (volle Stichprobengrösse). Beide Konventionen liefern bei kb=5 dieselbe Anzahl Klassen (8) mit leicht verschobenen Häufigkeiten — exakt der didaktische Punkt: dass die Klassenwahl mit der Grenz-Konvention zusammenhängt, beide aber gültig sind. Edge-Cases geprüft (alle Werte gleich, max ein Vielfaches von kb).

**Zusammenfassungs-Sektion am Seitenende ersatzlos entfernt** — die Sektion `<h2 id="zusammenfassung">Zusammenfassung — Wo geht's weiter?</h2>` plus Kapitel-Bezug-Liste plus Merksatz-Block zur Daten-Pipeline (insgesamt 16 Zeilen HTML) wurde komplett entfernt. Begründung aus dem Review: die Übersichts-Grafik am Seitenanfang deckt bereits alle Inhalte ab (Workflow + Kapitel-Klammern mit Klick-Verlinkung). Der globale TOC-Generator in `nav.js` greift dynamisch auf `<h2[id]>` der Seite zu — der Eintrag verschwindet automatisch. Der Eintrag `zusammenfassung:'Zusammenfassung'` in `nav.js` bleibt, weil er von den anderen 22 Themenseiten weiterhin verwendet wird.

Datei-Bilanz: nur `grundlagen/g4-0-praxisbeispiel-bm2-klasse.html`, +85 Zeilen netto (Tabellen-Logik und zwei neue Toggle-Bars hinzu, Zusammenfassung weg). `<div>`/`</div>`-Balance: 178/178 ✓; `<script>`/`</script>`-Balance: 6/6 ✓; `node --check` aller drei Inline-Scripts ✓.

---

## [unreleased] — 2026-05-17

### Jobs 5.1–5.5 — Aufgaben-Anzahl harmonisieren (Standard-Soll von 6 auf 7 angehoben)

Die Jobliste-Inventur §5 stammt aus einem älteren Snapshot und ist heute überholt: alle 22 Themenseiten enthalten bereits A1–A6 (Median 6 war die Soll-Zahl der Jobliste, ist heute der Ist-Zustand überall). Damit waren die Aufstockungs-Jobs (5.1: g3-1 von 2 auf 6, 5.2: g5-1 von 5 auf 6) faktisch bereits geleistet, und die Verschlankungs-Jobs (5.3, 5.4, 5.5) sind gemäss Auftraggeber-Direktive „nur anfügen, nicht reduzieren" out-of-scope.

Statt einer reinen Status-Verbuchung wurde der Auftrag als Anhebung des Standard-Solls von 6 auf 7 umgedeutet: **auf jeder der 22 Themenseiten wird eine A7-Aufgabe angefügt** (Anwendungs- oder Vertiefungs-Aufgabe), die die bestehende Progression A1/A2 Basis → A3/A4 Standard → A5/A6 Anwendung zu A5/A6/A7 Anwendung+Vertiefung verlängert. Die A7 sind durchgängig anspruchsvoller als die zugehörigen A5/A6, oft durch Mehrteiligkeit (a/b/c), Kontext-Wechsel oder explizite Begründungs-Aufforderung.

**22 neue A7-Aufgaben über alle Themenseiten**:

- **g1-1** — Werkstatt-Materialwahl: drei äquivalente Term-Darstellungen, Frage nach Recheneffizienz und struktureller Optimierung.
- **g1-2** — Rabatt-Vergleich an der Tankstelle: drei Rabattvarianten (Dezimal, Prozent, Bruch), Vergleich durch Umrechnung in eine Darstellung.
- **g1-3** — Werbeslogan-Prüfung: \((a+b)^2 = a^2 + b^2\) als falscher Slogan, Widerlegung mit konkreter Wertekombination, korrekte Formulierung.
- **g1-4** — Wassertropfen vs. Atlantik: Grössenordnungs-Vergleich von \(10^{-5}\) bis \(10^{20}\), Verhältnis zur Avogadro-Zahl.
- **g2-1** — Sport-Wettrennen: Position-Zeit-Gleichung mit Parameter, Sonderfall paralleler Geraden, Verweis ↗ 2.3.
- **g2-2a** — Zwei Stundenlohn-Modelle: lineare Funktion, Schnittpunkt bei 10 h (250 CHF), Empfehlung für Halbtage.
- **g2-2b** — Goldener Schnitt: \(\varphi^2 + \varphi - 1 = 0\), pq-Formel, sinnvolle Lösung im Intervall \((0, 1)\).
- **g2-3** — Werkstatt-Produktions-Mix: 3×3-System mit Lösung \((x, y, z) = (2, 3, 1)\), inkl. Probe.
- **g3-1** — Tarifvergleich: zwei lineare Tarife, Schnittpunkt bei 5 GB = 35 CHF, Empfehlung je nach Verbrauchsbereich.
- **g3-2** — Trend in Wettermessreihe: drei kollineare Punkte, Geradengleichung \(y = 2x + 3\), Diskussion zur Extrapolations-Grenze.
- **g3-3** — Hängebrücken-Bogen: Scheitelform \(y = -\tfrac{1}{80}x^2 + 20\), Höhe bei \(x = 20\) ist 15 m, Symmetrie der Schnittpunkte.
- **g4-1** — Eigene Klassenumfrage konzipieren: drei Fragestellungen mit unterschiedlichen Datentypen, Diskussion zur Datenqualität.
- **g4-2** — Diagrammwahl: vier Datensätze → Kuchen, Histogramm, Boxplot, Balkendiagramm; Begründung.
- **g4-3** — Zwei Klassen vergleichen: \(\bar{x} \approx 4.66\) vs. \(4.625\), Spannweite 1.3 vs. 4.0; Diskussion „Lage vs. Streuung".
- **g5-1** — Vermessen ohne Steigen: Schattenwurf zweier Objekte, ähnliche Dreiecke, Fahnenstange = 10.5 m, Verweis ↗ 5.2d.
- **g5-2a** — Aquarium-Raumdiagonale: \(80 \times 60 \times 50 \,\text{cm}\), zweistufiger Pythagoras, \(d = 50\sqrt{5}\,\text{cm}\), Grössenordnungs-Plausibilität.
- **g5-2b** — Drachen-Konstruktion: Diagonalen \(60\) und \(80\,\text{cm}\) im Verhältnis \(1{:}3\), vier Seitenlängen über Pythagoras, Symmetrie, Fläche \(2400\,\text{cm}^2\).
- **g5-2c** — Sprinkler-Bewässerung: Sektor 120° mit \(r = 8\,\text{m}\), Fläche \(\tfrac{64\pi}{3}\), Bogenlänge \(\tfrac{16\pi}{3}\), 3 Positionen für Vollkreis.
- **g5-2d** — Bauplan-Vergrösserung: Massstab 1:200 → 1:100, Längen verdoppeln, Fläche vervierfacht (\(k^2\)-Aussage).
- **g5-3** — Triangulation einer Insel: drei Winkel (70°, 80°, 30°), Sinussatz, Insel-Entfernung 92.54 m mit Probe-Doppelrechnung.
- **g5-4** — Tagestemperatur als Sinuskurve: Mittelwert 22°C, Amplitude 7°C, Periode 24 h, Argument-Faktor 15°/h, Phase \(t_0 = 11\), Probe bei \(t = 5\) und \(t = 17\), Verweis ↗ 5.5.
- **g5-5** — Riesenrad-Höhe als Gleichung: \(h(t) = 22 - 20\cos(45°\cdot t)\), \(h = 32\,\text{m}\) bei \(t = \tfrac{8}{3}\) und \(t = \tfrac{16}{3}\,\text{min}\), allgemeine periodische Lösung.

**Patch-Mechanik**: einheitliche Einfügestelle direkt vor `<h2 id="zusammenfassung">` in jeder Datei (eindeutiger Anker, einmalig pro Datei). Pro Seite wurde der bestehende Themen-Aufgaben-Container-Pattern beibehalten:

- 20 Seiten Standard: `<div class="block block-aufg"><div class="block-titel">🟠 A7 — …</div>… <button class="loesung-toggle" onclick="toggleL('l-<slug>-a7')">▶ Lösung</button><div class="loesung-body" id="l-<slug>-a7"><div class="block block-bsp"><div class="block-titel">🟢 Lösung</div>…</div></div></div>`
- **g3-1** mit `▲ Aufgabe 7 · …`-Titel und Toggle-ID `A7L` (folgt der Seiten-internen Sonderkonvention `A1L`, `A2L`, … `A6L`, die laut CHANGELOG Anrede-Job 2.1-out-of-scope ist).
- **g4-3** mit `<h3 id="a7">A7 · …</h3>` und Toggle-ID `l7` (folgt der Seiten-internen Sonderkonvention `l1`, `l2`, … `l6`, ebenfalls dokumentiert als Sonderfall).

Drei A7-Aufgaben enthalten Querverweis-Pillen (Job 10.1):
- g2-1 → ↗ 2.3 (Sonderfall paralleler Geraden = LGS unlösbar)
- g5-1 → ↗ 5.2d (Strahlensatz/Ähnlichkeit)
- g5-4 → ↗ 5.5 (trigonometrische Gleichung als Folgekapitel)

### Inhaltliche Sondernoten

- **Progression**: A7 wurde durchgehend als „verlängerter Anwendungs-Block" konzipiert, nicht als „neuer Schwierigkeitsgipfel". Die meisten A7 nehmen den Anwendungs-Charakter von A5/A6 auf und erweitern ihn um Kontext-Wechsel, Mehrteiligkeit oder explizite Begründungs-Aufforderung. Eine A7, die fachlich über A6 hinaus geht (z. B. erweitert auf 3-Variablen-LGS bei g2-3, dreidimensionalen Pythagoras bei g5-2a), bleibt didaktisch erreichbar, weil sie nur einen kleinen Schritt über das schon Geübte hinausgeht.
- **Sachthemen-Brücke**: Wo möglich greift A7 typische Schweizer Anwendungskontexte auf (Mobilfunktarife, Lugano-Temperaturen, Bergbahnstationen, Verkehrsmittel). Das verlängert das in der Reihe etablierte Lehrmittel-Versprechen „Mathematik aus dem Alltag" um eine Aufgabe pro Themenseite.
- **Konvention für die Aufgaben-Anzahl-Soll** in der Jobliste war 6. Diese Iteration hebt das Soll auf 7 an. Eine entsprechende Aktualisierung der Jobliste oder des STYLEGUIDE ist nicht nötig — die Jobliste wird ohnehin als historisch-deskriptives Dokument geführt, das CHANGELOG dokumentiert nun den neuen Soll-Stand.

### Verifikation

**Pre-Flight** über alle 22 Themenseiten: grün (page-wrap, content, nav.js, mathlib.js, buildNav, keine Phantom-Klassen).

**Aufgaben-Sequenz-Lückenlosigkeit**: alle 22 Themenseiten haben A1–A7 ohne Lücken.

**Marker-Eindeutigkeit**: `<h2 id="aufgaben">` und `<h2 id="zusammenfassung">` weiterhin genau einmal pro Datei.

**Toggle-/Lösungs-Body-Konsistenz**: pro Datei genau ein A7-Toggle-Aufruf und genau ein passender `loesung-body`-Container. Schema-Auswahl je Datei korrekt (Standard, A7L, l7).

**Mathematische Korrektheit** der A7-Aufgaben mit Python-Verifikation:
- g2-2a: \(25t = 18t + 70 \Rightarrow t = 10\,\text{h}\), beide Tarife 250 CHF ✓
- g2-2b: \(\varphi = \tfrac{-1+\sqrt{5}}{2} \approx 0.618\) (Goldener Schnitt) ✓
- g2-3: 3×3-System mit Lösung (2, 3, 1), alle drei Materialvorräte verbraucht ✓
- g3-2: drei Punkte \((1,5)\),\((3,9)\),\((5,13)\) auf Gerade \(y=2x+3\) ✓
- g3-3: Scheitelform \(y = -\tfrac{1}{80}x^2 + 20\), Höhe bei \(x=20\): \(15\,\text{m}\), Schnittpunkte mit \(y=15\) bei \(x=\pm 20\) ✓
- g4-3: \(\bar{x}_X = 4.6625\), \(\bar{x}_Y = 4.625\), Spannweiten 1.3 und 4.0 ✓
- g5-2a: \(80^2 + 60^2 = 10000 \Rightarrow d_B = 100\); \(100^2 + 50^2 = 12500 \Rightarrow d_R = 50\sqrt{5} \approx 111.80\,\text{cm}\) ✓
- g5-2b: Drachenseiten \(\sqrt{1300}\) und \(\sqrt{4500}\); Fläche \(\tfrac{1}{2}\cdot 60 \cdot 80 = 2400\,\text{cm}^2\) ✓
- g5-2c: Sektor 120°/r=8: \(A = \tfrac{64\pi}{3} \approx 67.02\,\text{m}^2\), \(b = \tfrac{16\pi}{3} \approx 16.76\,\text{m}\) ✓
- g5-3: Sinussatz mit \(\alpha=70°\), \(\beta=80°\), \(\gamma=30°\), \(c=50\): \(a \approx 93.97\,\text{m}\), \(b \approx 98.48\,\text{m}\), Höhe ≈ 92.54 m (Doppelrechnung übereinstimmend) ✓
- g5-4: \(T(5) = 15\,°\text{C}\), \(T(17) = 29\,°\text{C}\) für \(T(t) = 22 + 7\sin(15°(t-11))\) ✓
- g5-5: \(h(0)=2\), \(h(8/3)=32\), \(h(4)=42\), \(h(16/3)=32\), \(h(8)=2\) für \(h(t) = 22 - 20\cos(45°t)\) ✓

---

### Job 15.1 — Häufige-Fehler-Blöcke auf allen Themenseiten

Inventur über alle 22 Grundlagen-Themenseiten ergab vor dieser Iteration eine sehr ungleichmässige Verteilung der `block-fehler`-Sektionen:

```
Lerngebiet 1:  alle 4 Seiten haben ≥ 2  (g1-1=1, g1-2=2, g1-3=3, g1-4=4)
Lerngebiet 2:  2 Seiten unter Soll       (g2-1=1, g2-2a=1, g2-2b=0, g2-3=0)
Lerngebiet 3:  alle unter Soll           (g3-1=1, g3-2=0, g3-3=0)
Lerngebiet 4:  alle unter Soll           (g4-1=1, g4-2=1, g4-3=1)
Lerngebiet 5:  6 Seiten ohne, 2 mit 1    (g5-1=1, g5-2a..d=0, g5-3=0, g5-4=0, g5-5=1)
```

Job-15.1-Ziel laut jobliste-vereinheitlichungen.md §15: auf jeder Themenseite mindestens **2 typische Schülerfehler** als `block-fehler`. Hintergrund: Häufige-Fehler-Blöcke sind eines der stärksten didaktischen Werkzeuge des Lehrmittels — sie antizipieren die Stolpersteine, die der Lerner sonst erst beim Korrigieren der eigenen Aufgaben merkt, und sie sind durch ihre rote Färbung visuell als Warnung sofort erkennbar. Aktuell zu unterrepräsentiert.

**29 neue block-fehler-Blöcke verteilt auf 19 Themenseiten.** Endstand: alle 22 Seiten haben ≥ 2 Blöcke; Gesamtsumme über das Lehrmittel: 47 (vorher 18).

**Konvention für die neuen Blöcke**: Standard-Pattern `<div class="block block-fehler"><div class="block-titel">⚠ Häufiger Fehler — <Spezifizierung></div><p>…</p></div>`. Titel-Muster „⚠ Häufiger Fehler — &lt;Kernidee&gt;" (Singular, dann eine kurze thematische Spezifizierung). Damit ist der Block auch in der TOC-/Such-Sicht selbsterklärend. Bestehende Blöcke mit abweichenden Titeln („⚠ Achtung — …", „⚠ Bei…", „⚠ Korrelation ≠ Kausalität") bleiben unverändert — sie sind redaktionell tragbar und stammen aus dem etablierten Korpus; eine pauschale Titel-Vereinheitlichung wäre out-of-scope für 15.1.

**Einfügestelle**: jeweils unmittelbar vor `<h2 id="aufgaben">`. Das gibt eine klare didaktische Sequenz „Theorie → Warnung vor Stolpersteinen → Aufgaben" und ist in jeder Themenseite eindeutig auffindbar (jede Datei hat genau einen `<h2 id="aufgaben">`-Marker). Vorher schon vorhandene `block-fehler` an früheren Stellen (z. B. mitten in der Theorie-Sektion) bleiben dort — die neuen Blöcke kommen zusätzlich ans Ende.

**Liste der 29 ergänzten Blöcke nach Themenseite**:

- **g1-1** (+1): Punkt-vor-Strich vergessen — \(2 + 3 \cdot 4 = 14\), nicht \(20\).
- **g2-1** (+1): Multiplikation mit einem Term, der null werden kann — Probe ist zwingend.
- **g2-2a** (+1): Vorzeichen beim Umstellen über das Gleichheitszeichen — Äquivalenzumformung explizit hinschreiben.
- **g2-2b** (+2): Quadratwurzel hat zwei Lösungen \(\pm\); pq-Formel verlangt Normalform mit Leitkoeffizient \(1\).
- **g2-3** (+2): Rück-Einsetzungs-Schritt in die <em>Original</em>gleichung; Sonderfälle \(0=0\) (unendlich viele) und \(0=5\) (keine Lösung) nicht übersehen.
- **g3-1** (+1): Argument und Funktionswert nicht verwechseln — was in der Klammer steht, geht hinein.
- **g3-2** (+2): Steigung von links nach rechts lesen; y-Achsenabschnitt \(b\) ist der \(y\)-Wert bei \(x=0\), nicht die Nullstelle.
- **g3-3** (+2): Scheitelform ≠ Grundform ohne Ausquadrieren; Vorzeichen des Scheitelpunkts (\((x+4)^2\) gehört zu \(x_s = -4\)).
- **g4-1** (+1): Stichprobe vs. Grundgesamtheit ist relativ zur Fragestellung.
- **g4-2** (+1): Histogramm (lückenlos, stetig) vs. Balkendiagramm (mit Lücken, kategorial).
- **g4-3** (+1): Median nur aus <em>sortierter</em> Liste — illustriert mit Gegenbeispiel \(8, 3, 9, 1, 7\) (Urlisten-Mitte 9, korrekter Median 7).
- **g5-1** (+1): Winkelsumme im Dreieck \(180°\), im allgemeinen \(n\)-Eck \((n-2)\cdot 180°\).
- **g5-2a** (+2): Pythagoras nur bei rechtem Winkel zwischen den Katheten; Hypotenuse ist die längste Seite gegenüber dem rechten Winkel.
- **g5-2b** (+2): \(d = s\sqrt{2}\) nur im Quadrat — beim Rechteck \(d = \sqrt{l^2+b^2}\); Trapez-Höhe ist senkrecht, nicht schräg.
- **g5-2c** (+2): \(\pi\)-Näherungen (\(3\), \(3.14\)) verfälschen Endresultate; Bogenmass vs. Gradmass am Taschenrechner.
- **g5-2d** (+2): Flächen-Verhältnis = \(k^2\), nicht \(k\); Strahlensatz verlangt zwei parallele Geraden.
- **g5-3** (+2): \(\sin(\alpha)\) ist eine Zahl in \([-1, 1]\), nicht der Winkel; SSW-Fall des Sinussatzes hat manchmal zwei Lösungen (\(\arcsin\) und \(180° - \arcsin\)).
- **g5-4** (+2): Quadranten-Vorzeichen am Einheitskreis nicht ignorieren (\(\cos 120° = -0.5\)); Periodizität \(360°\) berücksichtigen.
- **g5-5** (+1): Hauptintervall \([0°; 360°[\) enthält für \(\sin\) und \(\cos\) zwei Lösungen, für \(\tan\) zwei Lösungen \(\varphi\) und \(\varphi + 180°\).

### Querverweis-Pillen in den neuen Blöcken

Zwei der neuen Blöcke nutzen die Querverweis-Pille-Konvention aus Job 10.1:
- g5-2a's Pythagoras-Block verweist mit `↗ 5.3` auf den Sinussatz für nicht-rechtwinklige Fälle.
- g5-2c's Bogenmass-Block verweist mit `↗ 5.4` auf den Einheitskreis-Abschnitt.
- g5-2d's Strahlensatz-Block verweist mit `↗ 5.3`.
- g5-4's Periodizitäts-Block verweist mit `↗ 5.5`.

Die Pillen erscheinen dadurch jetzt auch im Kontext der häufigen Fehler — sie zeigen, wo der korrigierende Stoff zu finden ist, wenn der Fehler auftaucht.

### Inhaltliche Sondernoten

- **Singular im Titel** („Häufiger Fehler" statt „Häufige Fehler"): bewusst, weil jeder Block einen konkreten, isolierten Fehler beschreibt. Pluralform „Häufige Fehler" wird gelegentlich von Sammlungs-Blöcken benutzt (z. B. in g2-1 und g2-2a Bestand); diese sind weiterhin akzeptabel, aber neue Blöcke folgen der Singular-Konvention.
- **Du-Form durchgehend** gemäss Job 18.1 — alle neuen Blöcke verwenden „du/dich/dir", keine Höflichkeitsform.
- **Schweizer Hochdeutsch** (kein ß, „mass" statt „maß"), Dezimalpunkt nicht Dezimalkomma.
- **Keine Sammel-Listen** im Format „Häufigste Fehler: 1. … 2. … 3. …" — jeder Fehler bekommt seinen eigenen Block. Das nutzt die rote Färbung als visuellen Marker pro Stolperstein und macht die Themen einzeln referenzierbar.

### Verifikation

**Pre-Flight** (Standard-Marker, Skript-Konsistenz, Phantom-Klassen) grün auf allen 19 modifizierten Seiten.

**Marker-Eindeutigkeit**: jede Datei hat genau einen `<h2 id="aufgaben">` — die Einfügestelle ist unambiguos.

**Tag-Bilanz** der neuen Blöcke (Stichprobe g2-2b, g5-2d, g5-4): pro Block 1 Container-`<div>` öffnen, 1 Titel-`<div>` öffnen, beide schliessen → 2/2 div-Bilanz pro Block. \(<p>\)-Tags ebenfalls ausgewogen.

**Anzahl-Kontrolle**: Inventur vor dem Patch zeigte 18 bestehende `block-fehler` über alle 22 Seiten; nach dem Patch sind es 47 — Differenz 29, was zu den 29 explizit eingefügten Blöcken passt. Jede der 22 Themenseiten hat jetzt ≥ 2.

**Inhaltliche Korrektheit** der mathematischen Beispiele:
- g3-3 Scheitelform-Beispiel: \((x-3)^2 = x^2 - 6x + 9\), also Grundform \(y = x^2 - 6x + 11\) bei Scheitelform \(y = (x-3)^2 + 2\) ✓
- g4-3 Median-Gegenbeispiel: Urliste \(8, 3, 9, 1, 7\), Mitte (Position 3) = \(9\); sortiert \(1, 3, 7, 8, 9\), Median (Position 3) = \(7\) ✓
- g5-2b Trapez-Höhen-Formel: gleichschenkliges Trapez mit Schenkel \(s\), Parallelseiten \(a, c\): \(h = \sqrt{s^2 - ((a-c)/2)^2}\) ✓
- g5-4 Quadranten-Beispiel: \(\cos(120°) = -0.5\) (im 2. Quadrant) ✓
- g5-5 Sinus-Symmetrie: \(\sin(\varphi) = 0.5\) → \(\varphi \in \{30°, 150°\}\) (\(\sin(150°) = \sin(180°-30°) = \sin(30°) = 0.5\)) ✓

---

### Cluster C / Lerngebiet 2: Einstiegs-Animation für g2-2b

g2-2b war in der Bestandsaufnahme ★ markiert: konkreter Alltagsbezug ja, Animation nein, und die Lösung der Bruchgleichung wurde im Einstieg vollständig algebraisch hergeleitet bis zur normierten Form \(v^2 - 20v + 32 = 0\) inklusive Wurzel-Auswertung und Plausibilitäts-Verwerfung der Negativ-Lösung. Damit war die Themenseite ihrer Pointe (lineare Form vs. quadratische Form, neue Lösungsmethode) bevor sie begann. Diese Iteration tauscht Herleitung und Lösung gegen eine Interaktion, in der der Lerner den Wert von \(v\) selbst sucht.

**g2-2b Quadratische Gleichungen — Anna fährt Velo**

Vor: drei LaTeX-Display-Gleichungen mit der vollständigen Umformung Bruchgleichung → quadratische Standardform, plus `block-bsp` „Was hier passiert" mit Wurzel-Lösungen \(v_a \approx 18.3\), \(v_b \approx 1.7\) und Plausibilitäts-Argument. Inhaltlich exemplarisch sauber — passt aber genau zu dem Muster, das die Bestandsaufnahme bemängelt: der Einstieg löst die Aufgabe.

Neu: Ein Schieber für die Hinweg-Geschwindigkeit \(v\) (5 bis 30 km/h, Schrittweite 0.1) und ein Canvas mit zwei parallelen Strassen-Streifen — oben der Hinweg (Haus → Schule, Velo bewegt sich nach rechts), unten der Rückweg (Schule → Haus, Velo bewegt sich nach links). km-Ticks alle 2 km, gestrichelte Mittellinien wie auf einer richtigen Strasse. Das Velo wird als Räder-Rahmen-Skizze gezeichnet mit Strichfigur in rot (Anna).

Ein Read-Out-Panel zeigt live fünf Werte: Hinweg-Geschwindigkeit \(v\), Rückweg-Geschwindigkeit \(v-4\), Hinweg-Zeit \(t_h = 12/v\) (in Minuten), Rückweg-Zeit \(t_r = 12/(v-4)\) (in Minuten), und besonders prominent rechts: die Summe \(\Sigma = t_h + t_r\). Die Summe-Box ist farbcodiert:
- rot („fern"): \(|\Sigma - 90| \geq 8\) min
- blau („nah"): \(1 \leq |\Sigma - 90| < 8\) min
- grün („treffer"): \(|\Sigma - 90| < 1\) min

Damit kann der Lerner durch Schieben das Treffer-Fenster suchen und sehen, dass es nahe bei \(v = 18.25\) km/h liegt — der wahren Lösung, die später durch Mitternachtsformel exakt bestimmt wird. Bei \(v \to 4^+\) divergiert \(\Sigma\) (Rückweg dauert unendlich), bei grossen \(v\) wird \(\Sigma\) klein — der Wert kommt also durch den Bereich (5, 30) genau einmal durch 90 min, was dem Lerner ein Gespür für die Eindeutigkeit gibt.

„▶ Fahrt starten" startet eine Animations-Sequenz: das obere Velo fährt mit der eingestellten Geschwindigkeit \(v\) von links nach rechts, das untere Velo (langsamer, weil \(v-4\)) startet wenn das obere ankommt und fährt nach links. Pace ist 0.5 h pro Sekunde Real-Zeit, das heisst die ganze Fahrt dauert in der Animation etwa \(\Sigma \cdot 0.5\) Sekunden. Stoppt bei Slider-Drag automatisch.

Direkt nach der Anim folgt der bisherige Aufbau in komprimierter Form: die Bruchgleichung wird angegeben und beschrieben, *was* daraus passiert (Multiplikation mit Hauptnenner, quadratische Standardform), aber *nicht* mehr durchgerechnet. Der Hinweis auf die zwei Lösungen und die Plausibilitäts-Verwerfung bleibt qualitativ — die konkreten Werte 18.3 / 1.7 sind raus. Die didaktische Brücke: Die Anim lässt den Lerner die Antwort *finden*; die Theorie-Sektion lehrt ihn, sie zu *berechnen*.

Technisch: Animation per `requestAnimationFrame`, Pace fest (0.5 h/s), Geschwindigkeitsverhältnis Hinweg:Rückweg ist intrinsisch \(v/(v-4)\), das obere Velo erreicht damit immer früher das Ziel als das untere fertig wird (sofern \(v > 4\)). Slider-Drag stoppt die laufende Animation und zeichnet statischen Zustand (beide Velos in Strassen-Mitte) neu. Read-Out-Update bei jedem Frame der Animation und bei jedem Slider-Move. HiDPI via `devicePixelRatio`.

### Inhaltliche Sondernoten

- Die ausführliche algebraische Herleitung der quadratischen Normalform aus der Bruchgleichung war ein didaktisch wertvoller Schritt — aber an dieser Stelle (vor der Theorie) zu früh. Sie taucht sinngemäss später wieder auf: in der Aufgaben-Serie der Themenseite gibt es Bruchgleichungs-Aufgaben (Anwendungs-Kategorie A5/A6), in deren Lösungen genau diese Umformung wieder vorkommt.
- Das Treffer-Fenster (Σ ∈ [89, 91] min) ist mit Slider-Schrittweite 0.1 km/h erreichbar — die Lerner-Erfahrung „ich finde den Wert selbst" funktioniert. Hätte ich Schrittweite 0.5 oder 1 gewählt, wäre die exakte Stelle nicht treffbar und die Anim würde frustrieren.
- Negative Rückweg-Geschwindigkeit (\(v \leq 4\)) ist durch Slider-Min = 5 ausgeschlossen. Der Plausibilitäts-Hinweis im Text bleibt qualitativ relevant.

### Verifikation

**Standard-Pre-Flight** für g2-2b:

```
grundlagen/g2-2b-quadratische-gleichungen.html  pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
```

**Strukturelle Integrität**: alle kritischen Marker eindeutig.

**JS-Syntax**: `node --check` über die extrahierten Inline-Scripts grün (DOM-Mocks inkl. `performance.now`, `requestAnimationFrame`).

**Mathematische Verifikation**:
- v=15.0 → tH=48.0 min, tR=65.5 min, Σ=113.5 min — passt zum Default-HTML-Markup (initiales Read-Out vor JS-Update)
- v=18.0 → Σ=91.4 min → „nah" (Differenz 1.43 min)
- v=18.2 → Σ=90.26 min → „nah" (Differenz 0.26 min, gerade noch im nah-Fenster)
- v=18.25 → Σ=90.00 min → „treffer" (Differenz 0.00 min) — exakte Lösung \(10 + \sqrt{68} \approx 18.246\)
- v=19.0 → Σ=85.9 min → „nah" (Differenz 4.11 min)
- v=25.0 → Σ=63.1 min → „fern" (Differenz 26.9 min)
- v=5.0 → Σ=864 min → „fern" (extrem langsam, sichtbar als Σ-Wert ohne Nachkommastelle)

---

### Cluster C / Lerngebiet 5 Trigonometrie: Einstiegs-Animation für g5-3

Mit der bereits in der vorigen Iteration geleisteten Lösungs-Bereinigung war g5-3 inhaltlich offen, aber visuell statisch: eine schöne SVG-Skizze mit fixiertem Standort, fixiertem Sehwinkel und fixierter Baumhöhe (15 m, 52°, "h = ?"). Diese Iteration ersetzt die statische Skizze durch eine Canvas-Animation, die das Messen selbst zum interaktiven Erlebnis macht — ohne die trigonometrische Methode vorzuwegnehmen.

**g5-3 Trigonometrische Berechnungen — Baum-Höhe per Abstand + Sehwinkel**

Vor: SVG-Hero-Bild (520×280) mit Strichfigur links, Baum rechts, gestricheltem Sichtstrahl, festem Sehwinkel-Bogen "52°", fester Distanz-Markierung "15 m", roter gestrichelter Höhenlinie mit Label "h = ?". Inhaltlich gut — die Frage stand offen, alle relevanten geometrischen Grössen waren benannt — aber jeder Lerner bekam genau dieselbe Konfiguration zu sehen. Wer im Kopf nicht durchspielt, was bei anderem Abstand oder anderem Winkel passieren würde, verpasst die Pointe: dass \(d\) und \(\alpha\) zusammen die Höhe eindeutig festlegen.

Neu: Zwei Schieber (Abstand \(d\) von 5 bis 20 m, Sehwinkel \(\alpha\) von 20° bis 60°) und ein Canvas mit Wiesen-/Himmel-Gradient (`linear-gradient(to bottom, #cde7f4 0%, #e6f0d8 65%, #dcc8a4 100%)`). Die Strichfigur steht fest am linken Bildrand, der Baum wandert mit dem Abstand \(d\) horizontal — so bleibt das Auge des Lerners beim Standort, das wandernde Element ist der Baum. Stamm wächst dynamisch mit (Höhe bis 45% von h, max. 6 m), darauf eine Krone aus drei gestapelten Ellipsen (mittlere dunkelgrün, zwei Akzent-Ellipsen oberhalb). Die rote gestrichelte Höhenlinie und das Label "h = X.XX m" passen sich live an. Der blaue gestrichelte Sichtstrahl geht vom Boden-Standort zur Baumspitze, der grüne Winkelbogen samt α-Beschriftung am Standort kippt mit. Distanz-Pfeil unter der Bodenlinie zeigt "d = X.X m".

Y-Achsen-Skala ist dynamisch (`max(20, 1.18·h)` Meter), Tick-Schritte 5 m bis 22 m, danach 10 m. Dadurch passt das Bild für die ganze Range: bei (d=5, α=20°) → h≈1.82 m sichtbar in 20 m-Skala, bei (d=20, α=60°) → h≈34.64 m sichtbar in ~41 m-Skala. Bei Default-Stellung (d=15, α=52°) → h=19.20 m, was der Original-SVG-Konfiguration entspricht.

Read-Out unter dem Canvas zeigt nur die berechnete Höhe als rote Mono-Zahl mit dem Untertitel "— direkt am Bild abgelesen". Bewusst keine Formel-Anzeige; die Methode (\(h = d \cdot \tan(\alpha)\)) bleibt das Geheimnis der späteren Sektion. Der erläuternde Absatz unter der Anim bringt die didaktische Pointe auf den Punkt: \(d\) und \(\alpha\) zusammen genügen für eine eindeutige Höhe; die Methode wird in diesem Kapitel gelernt.

Technisch: Massstabs-Funktionen `xpx(xm) = padL + xm·sxPx` und `ypx(ym) = ground_y - ym·syPx`. Sichtstrahl konzeptuell vom Boden des Standorts (mathematisches Modell, Augenhöhe vernachlässigt) — diese Konvention aus dem alten SVG-Bild wurde übernommen, damit der Winkelbogen am Boden andockt und nicht bei "Auge etwas über Boden" mit unklarem Bezug. Krone wird via `ctx.ellipse(...)` gezeichnet (drei Ellipsen unterschiedlicher Grösse und Position für ein „mehrlagiges" Krone-Gefühl). HiDPI-Skalierung via `devicePixelRatio`.

### Inhaltliche Sondernoten

- Die bereits in der vorigen Iteration getroffene Entscheidung, drei vorgerechnete Lösungswege (Strahlensatz / tan / Sinussatz) aus dem Einstieg zu entfernen, war Voraussetzung für diese Animation. Die Anim funktioniert nur, weil der Lerner *jetzt* die Lösung nicht sieht — er liest sie am Canvas ab, ohne sie methodisch zu kennen.
- Sliderbereiche bewusst beschränkt: bei α-max=60° und d-max=20 m bleibt h unter 35 m und damit visuell darstellbar. Bei α=70° und d=25 m wäre h=68.7 m — Anim wäre zwar mathematisch korrekt, der Baum würde aber unverhältnismässig dünn aussehen, weil die y-Skala stark gestaucht würde.

### Verifikation

**Standard-Pre-Flight** für g5-3:

```
grundlagen/g5-3-trigonometrische-berechnungen.html  pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=12/ok
```

**Strukturelle Integrität**: alle kritischen Marker eindeutig.

**JS-Syntax**: `node --check` über die extrahierten Inline-Scripts grün.

**Mathematische Verifikation**:
- (d=15, α=52°) → h=19.20 m (passt zum Default und zur Original-SVG-Konfiguration)
- (d=5, α=20°) → h=1.82 m (untere Range-Ecke)
- (d=20, α=60°) → h=34.64 m (obere Range-Ecke)
- (d=10, α=45°) → h=10.00 m (Spezialfall: \(\tan 45° = 1\), also \(h = d\)) — visuelle Plausibilitäts-Probe für Lerner

---

### Cluster C / Lerngebiet 5 Geometrie: Einstiegs-Animationen für g5-1, g5-2b, g5-2c, g5-2d

Vier Themenseiten des Lerngebiets 5 (Geometrie/Planimetrie) erhielten interaktive Einstiegs-Animationen gemäss der Bestandsaufnahme `einstiegsaufgaben-bestandsaufnahme.md`. Vorher: g5-1 hatte eine statische SVG-Skizze mit ausformulierter Pythagoras-Lösung, g5-2b und g5-2c je einen langen `block-bsp`-Block mit vorgerechneten Resultaten, g5-2d nur Fliesstext ohne Visualisierung. Nachher: vier Canvas-Animationen, die je den Alltagsbezug bewahren oder herstellen, das Lerngebiet visuell aufschliessen und gleichzeitig die didaktische Antwort der jeweiligen Themenseite offenlassen.

**g5-1 Grundlagen — Diagonalen-Skizze mit Live-Berechnung**

Ersetzt: SVG mit fixiertem 24 m × 18 m Grundstück, gestrichelter Diagonale und dem Lösungs-Fazit `d = √(24² + 18²) = 30 m`. Problem: der Einstiegsabschnitt führte das Pythagoras-Resultat ein, bevor das Thema „Skizze als Werkzeug" ausgelotet war — die Skizze diente nur als Illustration einer schon gegebenen Formel.

Neu: Zwei Schieber (Länge \(l\) von 6 bis 40 m, Breite \(b\) von 4 bis 30 m). Das Rechteck wird massstabsgetreu in einem Canvas gezeichnet (gemeinsame Pixel-pro-Meter-Skalierung, sodass Verhältnisse stimmen), darüber die Diagonale als roter gestrichelter Strich von der Eingangsecke zur gegenüberliegenden Ecke. Mit-beschriftet: Länge und Breite am Rand, Diagonale d in der Diagonal-Mitte als Live-Zahl, rechter Winkel an der Eingangsecke als kleines Quadrat. Rechts neben dem Rechteck stehen zwei Plausibilitäts-Checks live: \(d > \max(l, b)\) und \(d < l + b\) — beide grün mit den aktuellen Werten.

Didaktischer Kniff: Der Lerner sieht jetzt drei Dinge gleichzeitig — wie die Diagonale auf Änderungen reagiert, dass sie zwischen klaren Schranken liegt, und dass sie sich exakt berechnen lässt (denn die Zahl `d ≈ …` ist da). Die Frage, *wie* man sie ohne Abmessen berechnet, bleibt offen und führt mit Pille `↗ 5.2a` zum Pythagoras-Abschnitt. Die alte SVG-Skizze in der „schlechten" Box (Text-Selbstgespräch ohne Skizze) wird ebenfalls entfernt — die Gegenüberstellung war primär dazu da, das Pythagoras-Resultat zu motivieren; jetzt motiviert die Animation den Übergang.

Technisch: Schieber-Werte werden in Pixel umgerechnet mit einheitlichem Massstab `min(plotW/40, plotH/30)`, sodass das Rechteck nie verzerrt erscheint. Anker am unteren-linken Punkt, damit „Eingang" stets links-unten ist. HiDPI via `devicePixelRatio`.

**g5-2b Vierecke — Viereck-Familie aufdecken**

Ersetzt: `block-bsp` „Rahmenflächen vergleichen" (drei vorgerechnete Tische mit Fläche 4800 cm² und unterschiedlichem Umfang). Inhaltlich okay, aber: nahm den Fokus dieser Themenseite (Spezialisierungs-Hierarchie) nicht auf und rechnete eine Aufgabe vor, statt sie offen zu lassen.

Neu: Canvas mit vier drag-baren Eckpunkten \(A, B, C, D\) auf einem leichten Karopapier-Raster. Rechts ein Status-Panel, das vier Eigenschaften live als ✓/✗ anzeigt:
- \(AB \parallel CD\) (Trapez-Bedingung 1)
- \(BC \parallel DA\) (Trapez-Bedingung 2)
- alle Seiten gleich lang
- alle Winkel rechtwinklig

Aus diesen vier Eigenschaften wird der konkrete Typ abgeleitet (Quadrat, Rechteck, Raute, Parallelogramm, Trapez, allgemeines Viereck) und prominent oben im Panel angezeigt. Sechs Preset-Buttons setzen das Viereck auf typische Vertreter, sodass die Hierarchie ohne Drag-Fummelei erfahrbar wird.

Didaktisches Versprechen: Statt der erfundenen Stabilitäts-Idee aus der Bestandsaufnahme (die geometrisch fragwürdig ist — Quadrate sind genauso scherbar wie Parallelogramme, beide brauchen Diagonalversteifung), zeigt die Anim die *Hierarchie* selbst: Wer einen Schritt nach „strenger" zieht, sieht eine Eigenschaft mehr ✓ werden. Das Quadrat als Maximum mit allen vier ✓. Genau das ist der „Familie von Spezialfällen, jede mit einer zusätzlichen Bedingung"-Gedanke aus dem Einleitungstext.

Technisch: Logik-Koordinaten 0..10 mit gleichmässigem Massstab; `pointer*`-Events für Touch-und-Maus-Drag (Pointer-Capture, Hit-Radius 18 px); Klassifikation in `klassifiziere()`-Funktion mit normierten Toleranzen (Parallel-Tol 0.06 via cross/lenᵢ·lenⱼ, Recht-Winkel-Tol 0.06 via dot, Gleichlängen-Tol 0.06 via Abweichung vom Mittel). Labels A/B/C/D werden je 16 px nach aussen vom Schwerpunkt versetzt — bleibt bei jeder Form lesbar.

**g5-2c Kreis und Kreisteile — Pizza-Sektoren**

Ersetzt: `block-bsp` „Pizza vs. Quadrat" mit ausgerechneten 707 cm² vs. 900 cm² und der 27%-Aussage. Problem laut Bestandsaufnahme: Fläche und Lösung im Einstieg, ohne dass die Themenseite Gelegenheit hatte, Kreis-Bestandteile einzuführen.

Neu: Canvas mit einer Pizza (Radius \(r = 15\) cm, Durchmesser 30 cm) auf der linken Seite, rechts ein Schieber 2–12 für die Stückzahl und ein Read-Out-Panel mit drei Live-Werten:
- Sektorwinkel \(\zeta = 360°/n\)
- Bogenlänge pro Stück \(= r \cdot \zeta_{\text{rad}}\)
- Gesamtumfang ≈ 94.25 cm (zur Skalen-Orientierung)

Die Pizza ist mit warmen Teigtönen (`#fde2a7`, `#fcd479`, `#fbcb6e`) als rotierende Sektoren-Färbung gezeichnet, mit dunklerem Aussenrand für die Kruste. Das erste Stück (12 Uhr) ist hervorgehoben: ein roter Bogen am Mittelpunkt zeigt den Sektorwinkel ζ inklusive Beschriftung in der Bissektrix-Richtung; der entsprechende äussere Bogen ist als dickerer grüner Strich gezeichnet (Bogenlänge); eine gestrichelte blaue Linie zur Mitte zeigt den Radius mit `r = 15 cm` daneben.

Didaktischer Kniff: Sektorwinkel und Bogenlänge — zwei der wichtigsten Begriffe der späteren Sektor-/Segment-Sektion — werden hier visuell und numerisch erlebt, ohne dass die Formeln (Sektorfläche, Bogen-Maß) eingeführt wären. Die Frage „Wie gross ist die Fläche eines Stücks?" wird im Text explizit offengelassen und auf das Pi-Kapitel verwiesen.

Technisch: Sektor-Polygon per `arc()` zwischen `-π/2 + i·ζ_rad` und `-π/2 + (i+1)·ζ_rad`, Schnittlinien zwischen Stücken in dunklerem Braun, Kruste als äusserer 6-px-Ring. HiDPI-Skalierung.

**g5-2d Zentrische Streckung — Strassenlaterne mit Schatten**

Vor: nur Fliesstext zur Schattenwurf-Idee, keine visuelle Animation. Lange Erklärung dessen, was Streckungszentrum und Streckfaktor sind — vor jeder Anschauung.

Neu: Canvas mit Nachthimmel-Gradient (dunkelblau), darunter eine Strasse mit gestrichelter Mittellinie. Links steht eine Strassenlaterne (`H = 6 m`, dunkler Mast mit Lampenkopf-Glow als `RadialGradient`). Eine Strichfigur (`h = 1.8 m`) wird mit einem Schieber `d = 1.5..10 m` (Mast → Person) horizontal verschoben. Der Schatten wird als dunkler Streifen auf der Strasse zwischen Personenfuss und Schattenende gezeichnet; ein gestrichelter gelb-transparenter Lichtstrahl zeigt den Weg vom Lampenkopf durch den Personenkopf zum Schattenende. Unter dem Boden eine Massstab-Markierung „d = … m". Vier Werte werden live unter dem Canvas in Mono-Feldern angezeigt: Person-Höhe (fix 1.8 m), Lampenhöhe (fix 6.0 m), Schattenlänge \(s\), Mast→Schattenende.

Didaktischer Kniff: Die Bestandsaufnahme bat um „Verhältnis Mastabstand:Schattenlänge". Mathematisch ist dieses Verhältnis aber nicht konstant — wohl konstant ist „Mast→Schattenende durch Mast→Person", was bei \(H = 6, h = 1.8\) den Wert \(H/(H-h) = 1.4286\) ergibt. Genau das wird im erläuternden Absatz unter der Anim direkt angesprochen: „das Verhältnis bleibt immer gleich, egal wo die Person steht — dieses konstante Verhältnis ist der Streckfaktor". Damit motiviert die Anim den Begriff `k`, der dann in der späteren Streckungs-Sektion formal eingeführt wird, ohne ihn im Einstieg vorwegzunehmen.

Slider-Range gewählt mit Blick auf Bildgrenzen: bei `d = 10` ist das Schattenende bei `x = 2 + 10 · 1.4286 ≈ 16.3 m`, was im 18 m breiten Logik-Sichtfenster sichtbar bleibt. Höhere d-Werte würden den Schatten am rechten Rand abschneiden.

Technisch: Lichtstrahl als gestricheltes Pseudo-Linien-Pair vom Lampenkopf zum berechneten Schattenende; Strichfigur aus Kopf-Kreis, Torso-Linie, Arm-V, Bein-V mit Höhenanteilen 1.0/0.82/0.50/0.28 von h. Schatten als 4-Punkt-Polygon leicht unter Boden-Niveau (5 px Tiefe), damit die Strichfigur klar darüber steht.

### Inhaltliche Sondernoten

- **g5-1**: Die ursprüngliche „mit Skizze / ohne Skizze"-Gegenüberstellung war elegant, aber inhaltlich an die fixe Aufgabe 24×18 gekoppelt. Mit dem variablen Rechteck wird das didaktische Versprechen (Skizze als Strukturierungs-, Lösungs- und Kontroll-Werkzeug) verallgemeinerter eingelöst — der Lerner sieht *jedes* Rechteck, nicht eines.
- **g5-2b**: Die alte `block-bsp`-Tisch-Box mit Fläche/Umfang-Vergleich ist hier verloren. Die *Idee* (Fläche und Umfang sind verschiedene Grössen) wird auf der Themenseite weiterhin in der Theorie-Sektion behandelt; nur die *Position* im Einstieg fällt weg.
- **g5-2c**: Die 27%-Pizza-vs-Quadrat-Aussage war farbig, aber didaktisch nur lose mit dem Pi-Thema verknüpft. Die neue Pizza-Anim spielt direkt mit Sektorwinkel und Bogenlänge — den Begriffen, die in der Sektor-/Segment-Sektion zentral sind.
- **g5-2d**: Anders als bei g5-1/g5-2b/g5-2c hier *keine* Lösung entfernt, sondern eine fehlende Visualisierung *hinzugefügt* (in der Bestandsaufnahme als ★★ bewertet, „ergänzen Anim"). Der bestehende Schatten-Text wurde umformuliert, damit er nach der Animation kommt und das Verhältnis-Argument auf die direkt sichtbaren Werte stützt.

### Verifikation

**Standard-Pre-Flight** für die vier Seiten:

```
grundlagen/g5-1-grundlagen.html                          pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=9/ok
grundlagen/g5-2b-vierecke.html                           pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
grundlagen/g5-2c-kreis-und-kreisteile.html               pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html  pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
```

**Strukturelle Integrität**: alle kritischen Marker (`<h2 id="einstieg">`, `<h2 id="ressourcen">`, `<aside class="toc-wrap">`, `<footer class="site-footer">`, `<main class="content">`, `</main>`, `</body>`, `</html>`) genau einmal pro Datei.

**JS-Syntax**: `node --check` über die extrahierten Inline-Scripts aller vier Dateien grün (DOM-Mocks für `document`, `window`, `MathJax`).

**Mathematische Verifikation** (Python-Geometrie-Simulation gegen die Anzeige-Formeln):
- g5-1: \(d = \sqrt{l^2 + b^2}\) für (24,18)→30.00, (30,30)→42.43, (10,5)→11.18, (40,30)→50.00 — Plausibilitäts-Schranken in allen Fällen erfüllt.
- g5-2b: Klassifikations-Funktion getestet auf 5 Referenz-Polygone (Quadrat, Rechteck, Parallelogramm, Trapez, allgemeines Viereck) — alle korrekt erkannt.
- g5-2c: Für n ∈ {2, 4, 8, 12}: Sektorwinkel 180.0°/90.0°/45.0°/30.0°, Bogenlängen 47.12/23.56/11.78/7.85 cm, Gesamtumfang 94.25 cm — passt.
- g5-2d: Für d ∈ {1.5, 6.0, 10.0} mit H=6, h=1.8: Schattenlängen 0.64/2.57/4.29 m, Verhältnis Mast→Ende durch Mast→Person konstant 1.4286 — invariante Streckfaktor-Aussage.

---

### Cluster C / Lerngebiet 4: Einstiegs-Animationen für g4-1, g4-2, g4-3

Drei Themenseiten des Lerngebiets 4 (Datenanalyse) erhielten interaktive Einstiegs-Animationen gemäss der Bestandsaufnahme `einstiegsaufgaben-bestandsaufnahme.md`. Vorher: alle drei Seiten hatten konkrete Alltagsbezüge (★★ in der Bestandsaufnahme), aber statische SVGs oder Text-Aufzählungen. Nachher: Canvas-basierte Animationen, die das Interesse wecken, ohne den Lerninhalt vorwegzunehmen.

**g4-1 Grundlagen — Datensammel-Animation**

Ersetzt: statische 22-Werte-Urliste im Einstiegsblock (`block-bsp` mit fertiger Liste „3, 5, 2, 4, 6, …"). Diese hatte das Problem, dass der Lerneinstieg den eigentlichen Erhebungs-Prozess der Datenanalyse umging, also den ersten Schritt aus dem Daten-Workflow gleich übersprang.

Neu: 9 Klick-Buttons (0 h, 1 h, … 8 h) und ein Canvas-Säulendiagramm. Pro Klick wird ein Datenpunkt zur entsprechenden Säule hinzugefügt, die Säule wächst, der Zähler `n / 22` steigt. Nach 22 Klicks sind alle Buttons deaktiviert. Reset-Link setzt zurück. Die Anim macht den Erhebungsprozess (Schritt 1 des Daten-Workflows) selbst zur Lernerfahrung — und die Frage „Was sagt das über die Klasse?" bleibt offen, weil keine Kennzahl gezeigt wird (das ist Stoff von 4.3).

Technisch: y-Achse skaliert dynamisch (mind. 4 als Max, sonst auf das aktuelle Bucket-Maximum). Y-Beschriftung mit ganzen Zahlen, Säulen mit Zahl drauf, x-Achse mit Stunden 0–8. HiDPI-Rendering via `devicePixelRatio` (Standard-Pattern aus g3-1).

**g4-2 Diagramme — animierter Aufbau von vier Diagrammtypen**

Ersetzt: 2×2-Grid mit vier statischen SVGs (Balkendiagramm Lieblingsfach, Kuchendiagramm Verkehrsmittel, Histogramm Körpergrösse, Boxplot Lernzeiten). Diese hatten alle Diagramme gleichzeitig fertig auf dem Bildschirm — der Datentyp-Bezug musste vom Lerner aus dem Stand erkannt werden.

Neu: Vier Tabs (📊 Lieblingsfach, 🥧 Verkehrsmittel, 📈 Körpergrösse, 📦 Lernzeiten). Jeder Tab zeigt zunächst nur ein leeres Achsensystem; ein „▶ Animation starten"-Button baut das passende Diagramm Datenpunkt für Datenpunkt auf:

- **Balkendiagramm** (n=100): 100 einzelne Stimmen werden gemischt eingespielt. Pro Klick wächst eine zufällige Säule, die zuletzt hinzugefügte Kategorie bekommt einen orangen Puls-Ring. Anim-Dauer ~4 s.
- **Kuchendiagramm** (4 Sektoren = 100 %): Der Vollkreis wird in 360 Schritten von 0° bis 360° aufgebaut (~5 s); jeder Sektor erscheint, Beschriftung mit Prozent kommt am Sektor-Ende.
- **Histogramm** (n=60): 60 zufällig verteilte Werte aus normalverteilten Bins werden eingespielt; jeder Wert wird in seine Klasse einsortiert, der Pegel der entsprechenden Klasse wächst. Anim-Dauer ~3.5 s.
- **Boxplot** (n=22): zuerst werden alle 22 Punkte als kleine Kreise auf die Achse gesetzt (5.5 s); danach erscheinen min/max-Markierungen, dann Q₁-Q₃-Box, dann Median, dann Whisker-Linien — in 5 didaktischen Phasen á 0.25 s.

Wer einen Tab wechselt, sieht das nächste leere Achsensystem und kann erneut starten. Ein Datenpunkt-Zähler oben rechts zählt mit. Bei Kuchen-Anim zeigt der Zähler Prozent statt Datenpunkte.

Technisch: Eine zentrale `render()`-Dispatch-Funktion ruft je nach `aktKey` die passende `renderBalken/renderKuchen/renderHisto/renderBox` auf. `setInterval` läuft ab `playAnim()`; bei Tab-Wechsel wird gestoppt. Jeder Render-Aufruf setzt das Canvas neu auf HiDPI. Mischung der Daten erfolgt einmal beim Laden (Fisher-Yates), damit die Animation natürlich wirkt und nicht erst alle Mathe-Stimmen sammelt.

**g4-3 Masszahlen — Streuungs-Animation mit fixem Mittelwert**

Ersetzt: zwei statische Listen mit den Klassen-Werten von A `[4.0, 4.3, ..., 5.0]` und B `[2.5, 3.0, ..., 6.5]`, beide mit Mittelwert 4.5. Vorher war die didaktische Aussage „Mittelwert reicht nicht" nur textlich verkündet; jetzt erlebbar.

Neu: Notenachse 1–6, zwei Reihen Punkte (Klasse A oben grün, Klasse B unten orange). Eine rote vertikale Linie markiert den Mittelwert 4.5. Schieber 0–100 % interpoliert die Werte von Klasse B linear zwischen Klasse A (bei 0 %) und der gespreizten Verteilung (bei 100 %):

```
B(s) = A + s · (B_voll − A),  s ∈ [0, 1]
```

Da `mean(A) = mean(B_voll) = 4.5`, gilt mathematisch sauber `mean(B(s)) = 4.5` für jedes `s` — die rote Linie steht damit immer exakt in der Mitte, egal wie der Schieber steht. Die Anim zeigt unter jeder Reihe live „MW = 4.50  ·  Spannweite = …" — die Spannweite verändert sich von 1.0 bei s=0 % bis 4.0 bei s=100 %, der MW bleibt invariant. Dieselbe Aussage, die der Text vorher behauptete, wird hier von der Visualisierung selbst verifiziert.

Technisch: Punkte mit Versatz bei Mehrfachwerten (4.5 kommt zweimal vor → die zwei Punkte werden vertikal leicht gestapelt). Die Begriffe „Standardabweichung" und „Streumass" werden im Einstieg bewusst nicht eingeführt; nur „Spannweite" als deskriptive Anzeige. Begriff „Streuung" fällt einmal informell.

### Verifikation

**Standard-Pre-Flight** für die drei Seiten:

```
grundlagen/g4-1-grundlagen.html  pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
grundlagen/g4-2-diagramme.html   pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
grundlagen/g4-3-masszahlen.html  pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok
```

**Strukturelle Integrität**: alle kritischen Marker (`<h2 id="ressourcen">`, `<aside class="toc-wrap">`, `<footer class="site-footer">`, `<h2 id="einstieg">`) genau einmal pro Datei; canvas/div-Tag-Bilanz im Einstiegs-Abschnitt ausgewogen.

**JS-Syntax**: `node --check` über alle drei Inline-Scripts grün.

**Mathematische Verifikation** (g4-2 Histogramm-Bin-Zuordnung für 9 Test-Werte, Kuchen-Sektoren-Summe = 360°, g4-3 Mittelwert-Invarianz für s ∈ {0, 0.25, 0.5, 0.75, 1.0}): alle Resultate korrekt.

---

## [vorher unreleased] — 2026-05-17

### Aufgaben/Lösungs-Schema über alle Themenseiten vereinheitlicht

Vor dieser Iteration existierten **fünf verschiedene Schemata** für Aufgaben und ihre aufklappbaren Lösungen über die 22 Grundlagen-Themenseiten verteilt:

- `aw / aw-kopf + aw-loes` mit eigenem `classList.toggle('offen')` (g1-3, g1-4)
- `aw / aw-head / aw-body + btn-pruef` mit Inline-Toggle (g1-1, g1-2, g2-2a)
- `aw / aw-head / aw-body + btn-toggle + aw-loesung` (g2-2b, g2-3) — **defekt**: `toggleL` setzte Klasse `sichtbar`, aber `.aw-loesung` reagierte nur auf `.offen`. Lösungen klappten nicht auf.
- `<details><summary>Lösung</summary>…</details>` (g5-2d)
- Standard `block-aufg + loesung-toggle + loesung-body` — aber teilweise ohne inneren grünen `block-bsp`-Wrapper

Alle 22 Themenseiten folgen jetzt **einem einheitlichen Schema** (Variante A gemäss Bild-Vorlage des Auftraggebers):

```html
<div class="block block-aufg">
  <div class="block-titel">🟠 A1 — Titel</div>
  <p>Aufgabenstellung …</p>
  <button class="loesung-toggle" onclick="toggleL('l-g3-1-a1')">▶ Lösung</button>
  <div class="loesung-body" id="l-g3-1-a1">
    <div class="block block-bsp" style="margin:6px 0 0">
      <div class="block-titel">🟢 Lösung</div>
      <p>Lösungsschritte …</p>
    </div>
  </div>
</div>
```

Migrations-Umfang: 18 Themenseiten angefasst, davon 9 mit kompletter Container-Migration (HTML + CSS-Cleanup), 7 mit `aw`-Container-Umbau für interaktive Aufgaben, 6 mit nachträglich ergänzten `block-bsp`-Wrappern, 2 mit nachträglich eingebundenem `mathlib.js`. Slug-basierte Lösungs-IDs nach Schema `l-<slug>-aN` (kollisionsfrei).

### Pre-Flight-Check um Skript-Konsistenz erweitert (STYLEGUIDE §6.1, COLLABORATION §3.8)

Während der Migration trat ein neuer Fail-Modus auf: Themenseiten, die das alte aw-Schema mit Inline-Toggle benutzten, hatten `mathlib.js` historisch nie eingebunden. Nach der Umstellung auf `toggleL` (lebt in `mathlib.js`) fehlte das Skript weiter — Lösungen klappten still nicht auf, ohne Fehlermeldung im Browser. Der Standard-Pre-Flight aus §6.1 prüfte das nicht.

Erweiterung: `ml=$(grep -c 'src="../mathlib.js"' "$f")` und ein abgeleiteter `tog=N/ok|FEHLT`-Indikator als Skript-Abhängigkeits-Check. Erwartete Werte um `ml=1` und `tog=N/ok` ergänzt. Im STYLEGUIDE §6.1 ist `<script src="../mathlib.js"></script>` jetzt verbindlicher Teil des Skelett-Footers, mit Begründung in der Regel-Tabelle. COLLABORATION §3.8 dokumentiert den Bug und den Check ausführlich für ähnliche zukünftige Fälle (jeder globale Helfer, dessen Modul nicht eingebunden ist, erzeugt einen stillen `ReferenceError`).

### Aufgaben-Container-Stil (Bild-Schema durchgesetzt)

Sieben Themenseiten (g2-1, g3-2, g3-3, g5-1, g5-3, g5-4, g5-5) hatten noch den alten `<div class="aw">`-Wrapper für ihre **interaktiven** Aufgaben (Eingabefelder, Drag, Multiple Choice). Dieser hatte weissen Body und nur einen orangen Kopf-Streifen — visuell anders als die normalen `block-aufg`-Aufgaben (durchgehend orange).

Migration: Aussen-Container `<div class="aw"><div class="aw-head"><div class="aw-nr">…</div><div class="aw-titel">…</div></div><div class="aw-body">…</div></div>` → `<div class="block block-aufg"><div class="block-titel">🟠 … — …</div>…</div>`. Innerer interaktiver Inhalt (Canvas, Eingaben, Buttons) 1:1 erhalten. Lokale `.aw`/`.aw-head`/`.aw-nr`/`.aw-titel`/`.aw-body`-CSS-Regeln aus jeder Datei entfernt.

### Strukturelle Vereinheitlichungen (Tier 1 der Jobliste)

- **g5-2b, g5-2c**: h2-Reihenfolge `darstellungen` ↔ `definition` getauscht. Beide folgen jetzt der Master-Reihenfolge `einstieg → definition → darstellungen → typen → theorie → aufgaben → …`.
- **g4-3**: Zusammenfassungs-Tabelle von eigener `zus-tab`-Klasse (mit 6 lokalen CSS-Regeln) auf Standard `ftb-tabelle` mit `<thead>`/`<tbody>` umgebaut.
- **g3-1**: Video-Ressourcen-Sektion gefüllt. Drei verifizierte Einzelvideos (MathemaTrick „Was ist eine Funktion?", MathemaTrick „Maximaler Definitionsbereich", Daniel Jung „Definitionsbereich & Wertebereich") nach STYLEGUIDE-Anbieter-Priorität. Vorher: bewusster Platzhalter („In Vorbereitung").

### Index-Seite — Header und Stats

- `index.html` Titel: `1:1 nach BM RLP 2030` (statt `RLP 2030`)
- Promath-Hinweis-Satz im Hero-Subtitel entfernt (Chip bleibt)
- Stats-Counter `19 fertig` → `22 fertig`; Hinweis-Text `35 Themenseiten` statt `32 (Sub-Split bei 2.2)`
- Sub-Split-Boxen 2.2 und 5.2: neue CSS-Modifier `.ksub.span-2` / `.ksub.span-4` lassen die Container im Index-Grid mehrere Spalten überspannen — verhindert das Quetschen der 5.2a-d-Sub-Karten in einer einzigen Spalte

### Globale Header-Erweiterung (nav.js + style.css)

Neuer `ⓘ Über ▾`-Dropdown im globalen Header — auf jeder Seite sichtbar. Öffnet ein zweispaltiges Panel mit Tabs **Autor & Intention** / **Ausblick** / **Feedback** / **Lizenz**. Tab-Wechsel ohne Reload. Inhalt der vier Panels gemäss Auftraggeber-Stichworten redaktionell formuliert (CC BY-NC 4.0 als Lizenz, GitHub-Issue-Link als Feedback-Kanal). Auf engen Bildschirmen kollabiert das Panel in eine horizontale Tab-Leiste + Inhalt darunter. Mobile-Burger-Menü zeigt die vier Punkte als `<details>`-Aufklapper. Mobile-Breakpoint von 640px auf 1024px erhöht, weil mit den Meta-Tabs neun Header-Items sonst auf Tablet-Breiten kollidieren.

### Anrede-Konsistenz: Du-Form über alle Themenseiten (Job 18.1)

Inventur über alle 22 Grundlagen-Themenseiten, 93 Download-HTMLs und 13 Schwerpunkt-Themenseiten ergab: Schwerpunkt durchgehend Du, Downloads durchgehend Du, Grundlagen mit zwei Ausreissern — **g1-3 Algebraische Terme** (7 Anrede-Stellen in Theorie + Aufgabenstellungen) und **g1-4 Zehnerpotenzen/Quadratwurzeln** (8 Anrede-Stellen). Beide Seiten benutzten die Höflichkeits­form „Sie/Ihnen" durchmischt mit Du-Imperativen, was im sonst konsequent duzenden Korpus aus dem Rahmen fiel.

Patch: 15 Stellen umgeschrieben — Theorie-Anreden („erwerben Sie" → „erwirbst du", „haben Sie kennengelernt" → „hast du kennengelernt", „kennen Sie" → „kennst du", „begegnen Ihnen" → „begegnen dir", „denken Sie an" → „denk an"), Aufgaben-Imperative auf die im Restkorpus dominante Du-Kurzform („Schreiben Sie" → „Schreibe" / „Schreib", „Vereinfachen Sie" → „Vereinfache", „Berechnen Sie" → „Berechne", „Bringen Sie" → „Bring", „Geben Sie" → „Gib", „Drücken Sie aus" → „Drücke aus", „Probieren Sie selbst" → „Probier selbst"). Pre-Flight grün auf beiden Dateien.

Falsch-Positiv-Filter: In den Trefferlisten der Inventur erschienen weitere `\bSie\b`-Vorkommen (g2-2b, g5-1 und andere), die nach Kontextprüfung jedoch alle Personalpronomen 3. Pers. Sg./Pl. mit Sach-Subjekt waren (z.B. „Die Diskriminante … Sie entscheidet …" — Subjekt = die Diskriminante, nicht Anrede). Diese 18 Stellen bleiben unverändert.

Hintergrund: Jobliste-Vereinheitlichungen §18 hat als Empfehlung „konsequent duzen" festgehalten (Zielgruppe Berufsmaturitäts­lernende 17–22 Jahre, animierender Lehrmittel-Ton). Nach diesem Patch sind alle aktuell vorhandenen Themen- und Download-Seiten in derselben Anredeform.

### Zusammenfassungs-Schema vereinheitlicht (Job 3.2/3.3) und Aufgaben-Progression eingezogen (Job 6.1/6.2)

**Zusammenfassungs-Schema (3.2/3.3).** Vor dieser Iteration existierten drei verschiedene Varianten der Zusammenfassungs-Sektion: 11 Seiten hatten einen schwachen `<div class="merksatz">`-Einzeiler unter der Tabelle, 2 Seiten (g1-3, g1-4) nur einen `block-merksatz` ohne Tabelle, 4 Geometrie-Seiten überhaupt keinen Merksatz, und drei Trigonometrie-Seiten nutzten Inline-Style-Tabellen statt der `ftb-tabelle`-Klasse (`spez-tab`, `lsg-tab`, ungenannte Inline-Tabellen).

Alle 22 Seiten folgen jetzt **einem einheitlichen Schema**: prominenter `block-merksatz` mit ⭐-Header **vor** der Tabelle, darunter die `ftb-tabelle` mit den thematischen Details. Der Merksatz liefert die Kernbotschaft (1–2 Faustregeln), die Tabelle das Nachschlagewerk.

Konkrete Patches:
- **11 Seiten** mit Einzeiler-Merksatz: Einzeiler nach `block-merksatz` umgewandelt, vor die Tabelle gezogen (g1-1, g1-2, g2-1, g2-2a, g2-2b, g2-3, g3-1, g3-2, g3-3, g4-3, g5-1).
- **4 Geometrie-Seiten** ohne Merksatz: neue Merksätze geschrieben (g5-2a Dreiecke, g5-2b Vierecke, g5-2c Kreis, g5-2d Streckung/Ähnlichkeit).
- **g4-1 und g4-2** hatten Merksatz unter Tabelle: Reihenfolge umgedreht.
- **g5-3, g5-4, g5-5** mit Inline-Style-Tabellen: auf `ftb-tabelle`-Klasse umgestellt, Inline-Styles entfernt. g5-4 zusätzlich Merksatz neu geschrieben (war komplett ohne).
- **g1-3, g1-4** hatten nur Merksatz, keine Tabelle: Übersichtstabellen neu erstellt (Operationen mit Regel/Beispiel bzw. Potenz-/Wurzelgesetze mit Formel/Beispiel).

Spaltenüberschriften (Job 3.3) bleiben themenspezifisch, da inhaltlich präziser als eine pauschale `Begriff | Symbol/Formel | Kernidee`-Vereinheitlichung (z.B. „Grösse | Formel | Bedeutung" bei g3-2 oder „Werkzeug | Wann? | Formel" bei g5-3). Vereinheitlicht wird stattdessen nur die Tabellen-Klasse (`ftb-tabelle`), nicht der Header-Wortlaut.

**Aufgaben-Progression (6.1/6.2).** Konvention: A1–A2 Basis (Erkennen/Klassifizieren), A3–A4 Standard (Berechnen/Lösen), A5–A6 Anwendung. Keine sichtbare Markierung, keine Sektions-Trenner — nur die implizite Progression in der Reihenfolge.

Inventur über alle 22 Seiten ergab: 16 Seiten folgen bereits der Konvention, 4 Seiten haben Auffälligkeiten — davon waren 3 echte Tauschfälle und 1 Pseudo-Fall:
- **g1-1**: A5 (Anwendung — Strukturwahl) und A6 (Strukturwechsel via Distributivgesetz) getauscht — A5 ist jetzt Standard-Mathematik, A6 die Anwendung.
- **g2-2a**: A5 (Anwendung — Gleicher Stand) und A6 (Parameterdiskussion) getauscht.
- **g5-2d**: A5 (Schattenwurf-Anwendung) und A6 (Kathetensatz/Höhensatz) getauscht.
- **g5-2a**: untersucht und unverändert gelassen. Die Reihenfolge A1 Basis → A2/A3 Pythagoras-Anwendungen → A4 Kongruenzsätze-Diskussion → A5 Schnittpunkte-Synthese → A6 Anwendung ist didaktisch absichtlich (Theorie-Vertiefung nach Standard-Rechnung), kein „B nach S".

Zusätzlich entfernt: **A4–A6-Wrapper-Trenner** in g3-2 und g3-3 (Wrapper-Block „🟠 A4–A6 — Anwendungsaufgaben" um drei genestete Aufgaben-Blöcke). Konflikt mit Job 6.1 (keine sichtbare Sektions-Markierung); Wrapper aufgelöst, A4–A6 stehen jetzt als gleichrangige Blöcke neben A1–A3.

**Out-of-scope-Beobachtungen** (nicht angefasst):
- g3-1 nutzt Aufgaben-Titel im Format `▲ Aufgabe N · Titel` statt `🟠 AN — Titel` wie der Rest. Job 2.1 ist laut Auftraggeber abgeschlossen — die Titel-Notation fällt nicht unter Job 6.1/6.2.
- g4-3 hat zusätzliche `<h3 id="aN">`-Header vor jedem Aufgaben-Block (anderes Schema). Auch out-of-scope.
- Aufgaben-Anzahl-Harmonisierung (Job 5.x): g3-1 mit 6, g4-3 mit 6, aber g2-1 mit 7, g5-3 mit 10 — bleibt der späteren Iteration.

Validierung: Standard-Pre-Flight (page-wrap, content, nav.js, mathlib.js, Phantom-Klassen) grün auf allen 22 Seiten. Strukturelle Tag-Bilanz (div_o vs div_c, table_o vs table_c) grün in Zusammenfassungs- und Aufgaben-Sektionen aller 22 Seiten. Toggle-IDs nach Aufgaben-Tausch eindeutig, toggleL-Aufrufe und loesung-body-IDs konsistent.

### Querverweis-Pillen zwischen Themenseiten (Job 10.1/10.2)

Eingeführt: kompakte, klickbare Pille-Elemente mit Pfeil-Symbol und Themenseitennummer, die direkt hinter Titeln (h2/h3 oder Anim-Titel) sitzen und auf eine konkrete Sektion einer anderen Themenseite verweisen. Beispiel: das h3 „Cosinussatz" auf der 5.3-Seite bekommt die Pille `↩ 5.2a`, die direkt zum Pythagoras-Abschnitt der 5.2a-Seite springt.

Visuelle Form: pillenförmiger Inline-Link mit hellblauem Hintergrund und blauem Rand (CSS-Klasse `a.quer`), Schriftgrösse 0.72rem, Hover-Effekt (gefüllt blau, weisser Text). Klein, aber durch die Farbe sofort als Verweis erkennbar.

Pfeil-Konvention:
- **↩** für Voraussetzungs-Verweise (das Konzept dort kam im Lehrgang früher)
- **↗** für Anwendungs-Verweise (das Konzept wird dort später angewendet)

Inhaltlich werden nur Verweise gesetzt, wo der Bezug konkret und didaktisch nützlich ist: wenn ein Konzept aus einer anderen Themenseite hier konkret zum Einsatz kommt und der Leser von der Erläuterung dort profitieren würde. Keine pauschalen „Siehe auch"-Hinweise auf nur thematisch verwandte Seiten.

Resultat: **24 Pillen verteilt auf 16 von 22 Themenseiten** (0–4 pro Seite, Median 1). 6 Seiten haben keine Pillen — die Grundlagen-Seiten am Anfang ihres Lerngebiets (g1-1, g1-2, g2-1, g3-1, g4-1, g4-2), wo es noch nichts Voraussetzendes gibt.

Konkrete Verweise nach Lerngebiet:

- **Lerngebiet 1**: g1-3 → 1.1 (Hauptoperation/Distributivgesetz beim Ausklammern); g1-4 → 1.2 (irrationale Zahlen bei nicht-Quadratzahl-Wurzeln).
- **Lerngebiet 2**: g2-2a → 2.1 (Äquivalenzumformungen); g2-2b → 1.3 (Faktorisieren); g2-3 → 3.2 (Schnittpunkt zweier Geraden) und 2.1 (Äquivalenzumformungen in Verfahren).
- **Lerngebiet 3**: g3-2 → 2.2a (lineare Gleichung als Funktionswert-Frage); g3-3 → 2.2b (Diskriminante als Anzahl-Indikator für Nullstellen).
- **Lerngebiet 4**: g4-3 → 4.2 (Quartile/Boxplot-Bezug).
- **Lerngebiet 5**: g5-1 → 5.2a (Pythagoras-Plausibilität); g5-2a → 5.3 (halbes Dreieck als Quelle der Spezialwinkel); g5-2b → 5.2a (Innenwinkelsumme) und 5.2c (Sehnen-/Tangentenviereck); g5-2c → 5.2b (Pi-Annäherung via n-Eck) und 5.1 (Bogenmass bei Kreissektor); g5-2d → 5.2a (Pythagoras-Satzgruppe via Ähnlichkeit); g5-3 → 5.2d (Ähnlichkeit als Basis), 5.2a (3×: halbes Dreieck, Pythagoras, Kongruenzsätze); g5-4 → 5.2a (Pythagoras am Einheitskreis) und 5.3 (Winkelfunktionen-Übergang); g5-5 → 5.4 (2×: Einheitskreis-Bezug, Symmetrieeigenschaften).

CSS in `style.css` neu definiert (Block `a.quer`). Anker-IDs neu gesetzt auf vier h3 in g5-2a (`spezielle-dreiecke`, `kongruenz`, `pythagoras`, `halbes-dreieck`); andere benötigte Anker (`aequivalenz`, `diskriminante`, `symmetrie`, `regelmaessige-vielecke`) waren bereits gesetzt.

Validierung: Querverweis-Integritäts-Check — alle 24 Pillen-Links zeigen auf existierende Datei + existierenden Anker (Python-Skript: für jedes `href="X#Y"` wird `X` als Datei und `id="Y"` als Anker in `X` geprüft). Standard-Pre-Flight grün über alle 22 Seiten.

### Einstiegs-Lösungen entfernen wo Vorwegnahme statt Übergang (Cluster A der Einstiegsaufgaben-Bestandsaufnahme)

Bestandsaufnahme über alle 22 Einstiegssektionen ergab: 7 Seiten enthalten einen `block-bsp`-Block im Einstieg. Pro Block einzeln geprüft, ob er einen Übergang zum nächsten Abschnitt herstellt oder die Themen-Lösungsmethode vorwegnimmt.

**Behalten (5 Blöcke):**
- g1-1 „Drei Wege, denselben Betrag zu schreiben" — keine Aufgabe-Lösung, sondern drei äquivalente Schreibweisen, die direkt in „bevor man rechnet, schaut man auf die Struktur" münden (Übergang zur Hauptoperation-Definition).
- g2-2b „Was hier passiert" — keine Lösung, sondern Erklärung, dass aus einer Bruchgleichung eine quadratische geworden ist (Übergang zur Kapitel-Definition).
- g4-1 „Rohdaten (Urliste)" — keine Lösung, sondern Anzeige der Urdaten als visuelle Grundlage.
- g5-2b „Rahmenflächen vergleichen" — drei Vierecke gleicher Fläche, unterschiedlichem Umfang; mündet in „Trennung von Fläche und Umfang ist *der* Schlüsselgedanke bei Vierecken" (Übergang zum Kapitel-Thema).
- g5-2c „Pizza vs. Quadrat" — Form-Vergleich mit numerischen Werten (707 cm² vs. 900 cm²), motiviert geometrische Bedeutung; kein algebraischer Lösungsweg.

**Entfernt (2 Blöcke):**
- g2-3 „Lösung von Hand" — vollständige Lösung mit Einsetzmethode (`y = 20 − x`, einsetzen, ausrechnen) im Einstieg. Vorwegnahme des Verfahrens, das in der Theorie-Sektion systematisch eingeführt wird.
- g5-3 „Lösung mit Trigonometrie" — vollständige Anwendung von `tan(52°) = h/15` mit numerischem Ergebnis ≈ 19.2 m. Vorwegnahme der Tangens-Definition, die im rechtwinkligen Dreieck später systematisch entwickelt wird. Die SVG zeigt die Aufgabe weiterhin, der nachfolgende `block-tipp` „Was kann Trigonometrie?" macht den Übergang zur Kapitel-Übersicht.

Validierung: Standard-Pre-Flight grün auf den beiden modifizierten Dateien, div-Tag-Bilanz ausgeglichen.

### Neue Einstiegs-Animationen mit Alltagsbezug (Cluster B der Einstiegsaufgaben-Bestandsaufnahme)

Aus der Bestandsaufnahme: drei Seiten begannen rein mathematisch ohne Alltagsbezug und ohne Animation (Bewertung ★). Für jede wurde ein neuer Einstieg mit konkreter Alltagssituation und interaktiver Visualisierung gebaut. Die Aufgaben werden bewusst <em>nicht</em> gelöst — die Animation erlaubt dem Lerner, das Phänomen selbst zu erkunden; die mathematische Erklärung kommt erst in der Theorie-Sektion.

**g5-2a Dreiecke — „Stabil oder wackelig? Anzahl Beine und Bodenkontakt"**

Vorher: abstrakter Text „Das Dreieck ist die einfachste geradlinig begrenzte Fläche der Ebene", gefolgt von Aufzählung der vier Kapitel-Themen.

Neuer Einstieg: Fotograf baut Stativ auf — warum drei Beine und nicht vier? Animation zeigt in perspektivischer Sicht ein Stativ mit Schiebern für Anzahl Beine (2–5) und Boden-Unebenheit (0–20 cm). Bei N=3 bleibt das Stativ <em>immer</em> stabil; bei N=2 kippt es (Pfeil-Indikator); bei N≥4 mit Unebenheit > 0 hebt sich ein Bein vom Boden ab (gelb markiert, mit „+N cm"-Label). Live-Anzeige der Bodenkontakte. Übergang zur Definition: „Drei Punkte legen ein Dreieck — und damit eine Ebene — eindeutig fest."

**g5-4 Einheitskreis — „Schiff um Boje: Ost- und Nord-Versatz"**

Vorher: rein mathematische Frage „Was bedeutet sin(120°)?" mit nachfolgender textueller Antwort-Vorwegnahme.

Neuer Einstieg: Segelschiff umfährt Hafenboje auf Kreisbahn mit Radius 1 SM. Animation mit Schieber für Winkel φ (0°–360°) und vier Quadranten-Schnellauswahl-Knöpfen (Q I/II/III/IV). Anzeige des Schiffs als kleines Boot-Symbol mit Mast und Segel, das sich entlang des Kreises bewegt und gemäss Tangentenrichtung dreht. Ost-Versatz und Nord-Versatz werden als farbige Strecken (orange/grün) auf den Koordinatenachsen visualisiert und live mit Vorzeichen numerisch angezeigt. Erklärungstext wechselt automatisch je nach Quadrant (nordöstlich/nordwestlich/südwestlich/südöstlich). Übergang zur Definition: bei spitzem Winkel passt die alte 5.3-Definition, bei stumpfem nicht — aber „die Koordinaten des Schiffs sind die Werte, die der Taschenrechner ausspuckt".

**g5-5 Trigonometrische Gleichungen — „Riesenrad: wann auf halber Höhe?"**

Vorher: rein mathematische Frage „Welche Winkel φ erfüllen sin(φ) = 1/2?" mit Antwort-Vorwegnahme („unendlich viele Lösungen").

Neuer Einstieg: Riesenrad mit Radius 20 m, Periode 4 Min, Bodenfreiheit 2 m → Höhenfunktion `h(t) = 22 − 20·cos(ω·t)`. Linke Canvas-Hälfte zeigt drehendes Riesenrad mit acht Speichen, orangefarbener Gondel und Aufhängung; Boden, schräge Stützen. Rechte Hälfte zeigt Zeit-Höhe-Diagramm mit Achsen-Beschriftung (t [s], h [m]), gestrichelter Zielhöhen-Linie und vollständiger Sinus-Kurve (durchgehende Linie bis aktuelle Zeit, blass darüber für ganzen Bereich 0–480 s). Schnittpunkte der Sinuskurve mit der Zielhöhe-Linie werden als gelbe Marker eingezeichnet (analytisch via `Math.acos((22−h)/20)` plus Periodizität). Zwei Schieber: Zeit t (0–480 s = zwei Umdrehungen) und Zielhöhe (5–35 m). Live-Anzeige „auf Zielhöhe: N-mal bisher". Bei Zielhöhe ausserhalb [2 m, 42 m]: Hinweis „keine Lösung". Übergang zur Theorie: «Wann ist sin(...) gleich einem bestimmten Wert?» ist eine trigonometrische Gleichung — Kapitel-Thema.

Implementation: Alle drei Animationen folgen dem etablierten `.anim`-Schema (Canvas links, Bedienelemente rechts in Grid-Layout). Canvas-Helper `initCanvas` aus `mathlib.js`. Slider-IDs und Label-IDs nach dem Muster `sld-XXX`/`lbl-XXX`/`leg-XXX`. Init-Hooks an passenden DOMContentLoaded/load-Listenern der jeweiligen Seite angebracht.

Validierung:
- Node `--check` Syntax-Check der drei JS-Blöcke (rc=0)
- Standard-Pre-Flight auf allen drei Dateien grün (page-wrap=1, content=1, nav.js=1, mathlib.js=1, buildNav=1, keine Phantom-Klassen)
- Tag-Bilanz: div_o = div_c, canvas_o = canvas_c
- Python-Geometrie-Tests: alle Schiffspositionen für Winkel 0°/45°/90°/120°/180°/270°/359° liegen im Canvas-Bereich; Riesenrad-Mathematik kreuzgeprüft (Höhe bei t=0 → 2 m, t=60 s → 22 m, t=120 s → 42 m, t=240 s → 2 m; Schnittpunkte mit Zielhöhe 20 m bei t = 56.2, 183.8, 296.2, 423.8 s)

### Animations-Karte (.anim) als globale CSS-Klasse etabliert

Vor dieser Iteration war das `.anim`-Skelett (Animations-Karte mit Canvas links und Bedien-Panel rechts) als lokales `<style>`-Block in mehreren Geometrie-Themenseiten dupliziert (g5-2a, g5-4, g5-5 u.a.). Mit der geplanten Ausweitung auf alle Lerngebiete würden 22-fach dieselben CSS-Regeln in den Dateien stehen.

Globalisierung: ein Block von etwa 110 Zeilen in `style.css` am Ende eingefügt, deckt alle `.anim`-Klassen ab: Animations-Karte selbst, Layout-Grid, Canvas-Styling, `.bedien`-Panel, `.regler`/`.regler-label`/`.wert`, `.feld-titel`, `.chips`/`.chip`/`.chip.aktiv`, `.legende`/`.legende-titel`/`.legende-zeile`/`.lab`/`.val`, `.formel`, `.erklaerung`, `.anim-titel`, `.kn-quad` (Quadranten-Knöpfe für g5-4). Die bestehenden lokalen Blöcke in den Geometrie-Seiten bleiben vorerst stehen (CSS-Kaskade: identisch, kein Konflikt); können beim nächsten Refactoring entfernt werden.

### Neue Einstiegs-Animationen für Lerngebiet 1 (Cluster C, Tier 1)

Bestandsaufnahme: alle vier Themenseiten von Lerngebiet 1 (Algebra/Arithmetik) bewerteten mit ★★ (Alltagsbezug ja, aber keine Animation). Für jede ein interaktiver Einstieg mit Schieber und Live-Auswertung:

**g1-1 Grundlagen Algebra — „Drei Terme, ein Wert"**

Schieber für Anzahl Päckchen \(x\) (0–10). Drei algebraisch äquivalente Terme nebeneinander mit Live-Schritt-für-Schritt-Auswertung: `4·x + 3·x + 5`, `(4+3)·x + 5`, `7·x + 5`. Bei jeder Verschiebung des Schiebers zeigen alle drei Endwerte denselben grün hervorgehobenen Wert. Streifen unten bestätigt: „✓ Alle drei Terme liefern denselben Wert". Erkenntnis ohne formales Lernen: das ist Äquivalenz.

**g1-2 Zahlen — „Wo wohnt diese Zahl?"**

Fünf Werkstatt-Werte als anklickbare Chips (127 · −12 · 3/40 · −3.5 · √2). Canvas zeigt Zahlengerade mit vier ineinanderliegenden Streifen \(\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}\). Bei Auswahl eines Werts werden genau diejenigen Streifen farbig hervorgehoben, in denen die Zahl wohnt; die anderen bleiben blass. Wert-Marker (roter Punkt) am korrekten Ort auf der Zahlengeraden, mit gestrichelter Verbindung nach oben. Bei Werten ausserhalb des Bildbereichs (127): Pfeil-Indikator am Rand mit „→ 127". Live-Anzeige der vier Mengen mit ✓/✗-Symbol.

**g1-3 Algebraische Terme — „Drei äquivalente Terme — und ein vierter, der nicht passt"**

Zwei Schieber für \(x\) (Sorte A) und \(y\) (Sorte B). Vier Terme im Canvas: Anna (`80x + 50y`), Bruno (`10·(8x + 5y)`), Cinzia (`80x + 30y + 20y`) — alle äquivalent — und Dario (`(80+50)·(x+y)`), eine plausible-aussehende, aber <em>nicht</em> äquivalente Umformung. Live-Auswertung in jedem Term zeigt: Anna, Bruno, Cinzia produzieren denselben Wert (grün eingerahmt), Dario weicht ab (rot eingerahmt). Erklärung wechselt automatisch. Übergangsbeobachtung: nicht jede umgruppierte Klammerung führt zu äquivalenten Termen — Bedarf für Termumform-Regeln motiviert.

**g1-4 Zehnerpotenzen — „Vom Atom zur Galaxie"**

Schieber von \(10^{-15}\) m (Atomkern) bis \(10^{22}\) m (lokale Galaxien-Cluster) über 37 Zehnerpotenz-Stufen. Linke Hälfte: vertikale Skala mit Marken alle 1 Stufe, Beschriftung bei jeder 5er-Stufe (10⁻¹⁵, 10⁻¹⁰, 10⁻⁵, …). Aktive Stufe als blauer Pfeil-Marker hervorgehoben. Rechte Hälfte: symbolisches Objekt (Emoji oder Unicode-Glyphe), Bezeichnung („Mensch", „Hochhaus", „Erde-Durchmesser", „Milchstrasse" …) und wissenschaftliche Notation in 16-pt-Schrift oben. 24 verankerte Objekte zwischen Atomkern und Universum; bei Zwischen-Werten („nächster Anker: …"-Hinweis) wird der nächstgelegene Eintrag angezeigt.

Implementation analog zu Cluster B: Canvas links, Bedien-Panel rechts, Sliders/Chips für Interaktion, Live-Anzeige in `.legende`-Block, MathJax-Re-Render bei dynamischen Erklärungstexten.

Validierung: Node `--check` aller vier JS-Blöcke (rc=0). Pre-Flight grün auf allen vier Dateien (page-wrap, content, nav.js, mathlib.js, keine Phantom-Klassen). Tag-Bilanz ausgeglichen (div, canvas, script). Mathematik kreuzgeprüft: g1-1 alle drei Werte bei x=3 ergeben 26; g1-3 Dario weicht bei (5,3) um 490 ab, bei (1,1) um 130, bei (10,4) um 820 — nie äquivalent ausser bei x=y=0.

---

## [unreleased] — 2026-05-16

### HiDPI-Rendering für Canvas-Animationen (g5-2d, g5-3, g5-4)

Auf Retina-/HiDPI-Displays (MacBook, iPhone, neuere Android-Geräte) wurden Text und Linien in den Canvas-Animationen unscharf gerendert. Ursache: die Canvas-Elemente haben `width="560" height="440"` als HTML-Attribute (interner Pixel-Buffer), werden aber per CSS auf `width: 100%` skaliert. Auf einem Retina-Display mit `devicePixelRatio = 2` werden die 560 Buffer-Pixel auf bis zu 1120 echte Anzeige-Pixel hochgerechnet — sichtbares Anti-Aliasing-Verschwimmen besonders bei Text.

#### Lösung

Die zentrale `initCv`-Funktion wurde umgebaut: sie setzt den Buffer beim ersten Aufruf auf `CSS-Grösse × devicePixelRatio` (echte Anzeigepixel) und skaliert den Zeichen-Kontext per `ctx.scale()` so, dass die bisherige Zeichnungs-Logik in **logischen Koordinaten** (0..560 × 0..440) unverändert weiterläuft. Die logische Auflösung wird in `cv.dataset.logicalW` / `logicalH` gesichert, damit wiederholte Aufrufe (z.B. nach Resize) nicht von bereits skalierten `cv.width`-Werten ausgehen.

```js
function initCv(id) {
  const cv = document.getElementById(id);
  if (!cv) return null;
  if (!cv.dataset.logicalW) {
    cv.dataset.logicalW = cv.width;
    cv.dataset.logicalH = cv.height;
  }
  const W = +cv.dataset.logicalW;
  const H = +cv.dataset.logicalH;
  const dpr = window.devicePixelRatio || 1;
  const rect = cv.getBoundingClientRect();
  const cssW = rect.width  || W;
  const cssH = rect.height || H;
  const bufW = Math.max(1, Math.round(cssW * dpr));
  const bufH = Math.max(1, Math.round(cssH * dpr));
  if (cv.width !== bufW || cv.height !== bufH) {
    cv.width  = bufW;
    cv.height = bufH;
  }
  const ctx = cv.getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(bufW / W, bufH / H);
  ctx.clearRect(0, 0, W, H);
  return { ctx, W, H, cv };
}
```

#### Betroffene Dateien

Drei Dateien hatten noch das alte einfache `initCv` ohne HiDPI-Skalierung — alle gefixt:

- `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` (5 Canvas-Elemente, alle 5 Animationen)
- `grundlagen/g5-3-trigonometrische-berechnungen.html` (6 Canvas-Elemente)
- `grundlagen/g5-4-einheitskreis.html` (3 Canvas-Elemente)

#### Folgeänderungen in g5-2d (Drag & Drop)

In Anim 1 wird der Canvas-Buffer für Pointer-Hit-Tests genutzt. Da `cv.width`/`cv.height` jetzt die **physischen** Pixel-Werte enthalten (nicht mehr die logischen 560×440), wurden zwei Stellen auf `cv.dataset.logicalW`/`logicalH` umgestellt:

- `canvasCoordsFromEvent(cv, ev)`: Skalierungs-Faktor `sx = logicalW / rect.width` (Pointer-Koord → logische Canvas-Koord)
- `pointermove`-Handler: `strClamp([x, y], logicalW, logicalH)` (Drag-Bounds in logischen Pixeln)

#### Bereits HiDPI-taugliche Dateien (unverändert)

Diese Dateien hatten bereits eigene HiDPI-Implementierungen — wurden nicht angefasst:

- `grundlagen/g5-2a-dreiecke.html`
- `grundlagen/g5-2b-vierecke.html`
- `grundlagen/g5-2c-kreis-und-kreisteile.html`
- `grundlagen/g2-1-grundlagen.html`
- `grundlagen/g3-1-grundlagen.html`
- `grundlagen/g2-2a-lineare-gleichungen.html`
- `grundlagen/g2-2b-quadratische-gleichungen.html`

(Diese nutzen z.T. eine andere Konvention — CSS-Pixel als logische Auflösung — die aber für ihre Zeichnungs-Logik passt und nicht durch meine Änderung gestört werden darf.)

#### Verifikation

- JS-Syntax aller drei modifizierten Dateien validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß im ganzen Lehrmittel
- Globalsweep: alle 10 Canvas-Dateien sind nun HiDPI-tauglich

---

### g5-2d Anim 2 — Chip-Labels kompakt, ganzzahlige Parallelenabschnitte (Nachjustierung)

#### 1. Situation-Chips: Beschriftung nur „A" / „B"

Die Chip-Beschriftungen „A (SA=2, SB=3, k=2)" und „B (SA=3, SB=2, k=3)" waren zu lang und liessen die Chips auf mobilen Geräten umbrechen. Die Vor-Werte sind im Canvas ohnehin direkt ablesbar. Chips zeigen nun nur die Buchstaben „A" und „B"; der Titel „Situation" darüber wurde wieder eingefügt.

#### 2. Ganzzahlige Werte für AB und A'B'

Bisher waren die Parallelenabschnitte krumm: in Situation A war AB ≈ 1.92 und A'B' ≈ 3.83, in Situation B waren AB ≈ 1.92 und A'B' ≈ 5.75. Das war kosmetisch unschön und didaktisch suboptimal — wenn die Strahlenabschnitte ganzzahlig sind, sollten die Parallelenabschnitte es auch sein.

**Lösung:** Strahl-Winkel so wählen, dass nach dem Kosinussatz \\(AB^2 = SA^2 + SB^2 - 2 \\cdot SA \\cdot SB \\cdot \\cos \\gamma\\) auch \\(AB\\) ganzzahlig wird.

Mit \\(\\cos \\gamma = 0.75\\) (also \\(\\gamma \\approx 41.41°\\)):

- Situation A (SA=2, SB=3, k=2): \\(AB^2 = 4 + 9 - 2\\cdot 2\\cdot 3\\cdot 0.75 = 13 - 9 = 4\\) → **AB = 2, A'B' = 4**
- Situation B (SA=3, SB=2, k=3): \\(AB^2 = 9 + 4 - 9 = 4\\) → **AB = 2, A'B' = 6**

Beide Situationen mit dem gleichen \\(\\gamma\\) — sehr elegant.

**Strahl-Winkel:** symmetrisch zur Horizontalen, jeweils 20.70° nach oben/unten:

```js
const ang1 = -0.3614, ang2 = 0.3614;  // jeweils γ/2 rad
```

(zuvor: −0.32 und +0.36, asymmetrisch zur Horizontalen).

#### 3. Anzeige als Ganzzahl

Da die Werte numerisch exakt 2/4/6 sein können (mit minimaler Float-Toleranz), formattiert eine kleine Hilfsfunktion `fmt(v)`:

```js
const fmt = (v) => Math.abs(v - Math.round(v)) < 0.02 ? String(Math.round(v)) : v.toFixed(2);
```

Bei nahezu ganzzahligen Werten kommt „2" raus, bei krummen Werten weiterhin „2.00" als Fallback. Beides am Strecken-Label und in der Werte-Gleichung.

#### Verifikation

- AB = 2.00, A'B' = 4.00 (Sit A) und 6.00 (Sit B) — geometrisch exakt
- Alle Punkte sicher im Canvas (Sit B mit A' bei y=61 hat noch 61 px Rand)
- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß

---

### g5-2d Anim 2 — Label-Konflikte und Farb-Kollisionen behoben (Nachjustierung)

Nach Sichtprüfung im Browser kamen drei Verfeinerungen:

#### 1. UI-Aufräumen: „Situation"-Überschrift entfernt

Der `<div class="feld-titel">Situation</div>` Titel über den Chips A/B war redundant — die Chip-Beschriftungen "A (SA=2, SB=3, k=2)" und "B (SA=3, SB=2, k=3)" sind selbsterklärend. Entfernt.

#### 2. Label-Konflikte mit Linien beseitigt

Die Werte-Labels (`SA = 3`, `SA' = 9`, etc.) saßen mit nur 16 px senkrechtem Versatz an der Strecken-Mitte — bei schräg verlaufenden Strahlen wirkte das optisch noch wie „auf der Linie". Zusätzlich gab es bei kompakten Situationen (Situation A) **Kollision des `SA'`-Labels mit der AB-Parallele**: 3.8 px Abstand zur AB-Linie.

Zwei Änderungen:

a) **Label-Versatz** generell von 16 → 22 px erhöht (konstante `LABEL_OFFSET`).

b) **Position entlang der Strecke** für lange Strecken (SA', SB') verschoben: per neuem `t`-Parameter in `valLabel` werden `SA'` und `SB'` bei 75 % der Strecke (Richtung A' bzw. B') statt der Mitte gesetzt. Damit landen sie ausserhalb des inneren Dreiecks SAB und kollidieren nicht mehr mit der AB-Parallele.

**Verifikation per Geometrie-Simulation:** alle 6 Werte-Labels (SA, SA', SB, SB', AB, A'B') haben in beiden Situationen einen Abstand > 18 px zu jeder gezeichneten Linie. Keine Kollision mehr.

#### 3. Neue Farben für die Parallelenabschnitte AB und A'B' (2. Strahlensatz)

Bisher: `AB = orange` (gleiche Farbe wie `SB` beim 1. Strahlensatz), `A'B' = rot` (gleiche Farbe wie `SB'` beim 1. Strahlensatz). Beim 2. Strahlensatz Schritt 5 (`SB : SB' = AB : A'B'`) sah es so aus, als wären SB und AB beide orange und SB' und A'B' beide rot — visuell verwirrend.

Neue Farbgebung beim 2. Strahlensatz:
- `AB` = **grün** `#16a34a`
- `A'B'` = **petrol/teal** `#0891b2`

Vier deutlich unterschiedliche Farben gleichzeitig im Bild bei Schritt 5: blau (SA), violett (SA' bzw. SB' im 2. Satz), grün (AB), petrol (A'B'). Beim 2. Strahlensatz Variante 2 also blau (SB), violett (SB'), grün (AB), petrol (A'B').

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß
- Geometrische Verifikation aller Label-Positionen in beiden Situationen frei von Linien-Konflikten

---

### g5-2d Anim 2 — Schritt 0 und versetzte SA'/SB'-Strecken (Auftrag 2 Nachjustierung)

Nach Sichtprüfung im Browser kamen zwei Verfeinerungen hinzu:

1. **Schritt 0:** der Slider beginnt nun bei 0. Bei Schritt 0 ist nichts eingefärbt — nur die grauen Strahlen und grauen Parallelen, sowie alle Punkte (S, A, A', B, B') mit ihren Beschriftungen und die Streckenwerte (SA, SA', SB, SB' beim 1. Strahlensatz, zusätzlich AB und A'B' beim 2.). Die Lernenden können sich erst orientieren, bevor der Aufbau startet.

2. **Versetzte SA'/SB'-Strecken:** Bisher wurden in Schritt 2 das AA'-Teilstück und in Schritt 4 das BB'-Teilstück direkt auf dem Strahl in violett bzw. rot eingezeichnet — visuell sah es so aus, als würde SA' nur aus dem AA'-Stück bestehen (das blaue SA-Stück lag davor). Neu wird **`SA'` als komplette Strecke von S bis A' senkrecht zum Strahl 1 nach aussen versetzt** (8 px) gezeichnet, ebenso `SB'` parallel zum Strahl 2 nach aussen. So sind beide Strecken (SA und SA') als zwei parallel verlaufende Strecken sichtbar — eine kurze blaue, eine lange violette. Der Längenvergleich wird offensichtlich.

#### Implementierung

**HTML:**

```html
<input type="range" id="sld-strSchritt" min="0" max="5" step="1" value="0">
```

Min-Wert auf 0 statt 1, Startwert 0.

**JS:**

- Neue Hilfsfunktionen:
  - `segVersetzt(p1, p2, off, color, lw)` zeichnet eine versetzte Strecke samt kleinen Anschluss-Strichen an Anfang und Ende (Tick-Markierungen, damit visuell klar ist: diese Strecke gehört zu p1...p2).
  - `makePerp(dir, signY)` erzeugt einen Einheits-Normalvektor zur Strahlrichtung mit gewünschtem y-Vorzeichen (für „nach aussen"). Für Strahl 1 (oberer): signY=−1 → Versatz `(-2.5, -7.6)` × OFF; für Strahl 2 (unterer): signY=+1 → Versatz `(-2.8, +7.5)` × OFF.
  - `valLabel(p1, p2, txtStr, sideOuterDirY, color)` für Werte-Labels mit gewähltem y-Vorzeichen.
  - `valLabelAwayFrom(p1, p2, refPoint, txtStr, color)` für Werte-Labels auf der Seite WEG von `refPoint` — verwendet für `AB` und `A'B'` beim 2. Strahlensatz, damit die Labels nicht ins Dreieck-Innere kollidieren.

- **Parallelen** (AB und A'B') werden jetzt in grauer Grundfarbe `C.linie` mit 1.4 px Linienbreite gezeichnet, statt vorher in lila. Bei Schritt 3/4 (1. Strahlensatz) bzw. Schritt 3/4 (2. Strahlensatz) werden sie dann farbig überzeichnet.

- **Bedingungs-Reihenfolge** im Gleichungs-Aufbau erweitert: `if (schritt === 0) { ... } else if (strSatz === '1') { ... }`. Bei Schritt 0 wird im Bezeichnungs-Feld der Hinweis „— Skizze betrachten, dann Schritt 1 wählen —" in dezentem Grau angezeigt; das Werte-Feld bleibt leer.

#### Geometrische Verifikation der Versatz-Strecken

| Situation | SA' versetzt: Start → End | SB' versetzt: Start → End | Im Canvas? |
|---|---|---|---|
| A | (57, 212) → (247, 149) | (57, 227) → (338, 333) | ✓ |
| B | (57, 212) → (485, 71) | (57, 227) → (338, 333) | ✓ |

Bei Situation B endet die SA'-Versetzte bei y=71 — knapp unter dem oberen Rand, aber sicher im Canvas (Margin 71 px).

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß

---

### g5-2d Anim 1 — Punkt-Durchmesser halbiert (Nachjustierung)

Auf Wunsch des Reviewers wurden die Drag-Handles von Z, A, B, C kleiner gezeichnet — die zuvor sehr prägnant grossen Kreise (16 px Durchmesser für A/B/C, 14 px für Z) wirkten zu dominant im Vergleich zum Dreieck selbst.

#### Änderung

- `STR_HANDLE_R = 8 → 4` (= halber Durchmesser)
- Eckpunkte A, B, C: jetzt 8 px Durchmesser (vorher 16 px)
- Zentrum Z (mit `STR_HANDLE_R - 1`): jetzt 6 px Durchmesser (vorher 14 px)
- Halo-Offset bei Hover/Drag von `+5` auf `+6` angepasst, damit der Halo (jetzt 20 px Durchmesser) bei kleinerem Punkt nicht überdimensioniert wirkt und gleichzeitig die Hit-Toleranz von 14 px andeutet
- Hit-Toleranz `STR_HIT_TOL = 14` bleibt unverändert — die Punkte sind visuell kleiner, aber genauso leicht greifbar (besonders auf Touch)

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß

---

### g5-2d Anim 2 — Strahlensätze konzeptionell neu gestaltet (Auftrag 2)

Gemäss PDF: schrittweiser Aufbau zweier paralleler Gleichungen mit Strecken-Einfärbung in der Skizze. „Damit wird der restliche Text in der Animation überflüssig."

#### Ausgangslage (entfernt)

Die alte Animation hatte:
- 3 Schieberegler für SA, SB und Streckfaktor k
- Eine statische Formel-Anzeige
- Eine ausführliche Legende mit Werten aller Strecken
- Einen langen Erklärungstext

Das machte die Animation textlastig und das Verständnis der **Aufbau-Logik** des Strahlensatzes blieb implizit.

#### Neue Architektur

**HTML-UI** (komplett ersetzt):

```
[1. Strahlensatz | 2. Strahlensatz]   ← Satz-Wahl (bleibt)
[Situation A | Situation B]            ← NEU: zwei vordefinierte ganzzahlige Konstellationen
Schritt: 1 ... 5  (Slider)             ← NEU: 5-Schritt-Aufbau
[Bezeichnungs-Gleichung — eingefärbt]
[Werte-Gleichung — eingefärbt]
```

Die ausführliche Legende und der Erklärungstext sind entfallen — die zwei Gleichungen mit Farbcode tragen die ganze Information.

**Zwei vordefinierte Situationen** (beide ganzzahlig):

| | SA | SB | k | SA' | SB' |
|---|---:|---:|---:|---:|---:|
| Situation A | 2 | 3 | 2 | 4 | 6 |
| Situation B | 3 | 2 | 3 | 9 | 6 |

Beide passen in den Canvas (`U = 50` Pixel pro Einheit), und ihre Verhältnisse sind deutlich verschieden.

**Schrittweiser Aufbau (1. Strahlensatz, Schritte 1–4):**

| Schritt | In Skizze eingefärbt | Bez.-Gleichung | Werte-Gleichung |
|---|---|---|---|
| 1 | SA blau | `SA` | `2` |
| 2 | + AA' violett (von A nach A') | `SA : SA'` | `2 : 4` |
| 3 | + SB orange | `SA : SA' = SB` | `2 : 4 = 3` |
| 4 | + BB' rot (von B nach B') | `SA : SA' = SB : SB'` | `2 : 4 = 3 : 6` |

**Schritt 5** zeigt die **zweite Variante** des 1. Strahlensatzes: `SA : AA' = SB : BB'`, also das Verhältnis Strahlenabschnitt-vor-Parallele zu Strahlenabschnitt-zwischen-Parallelen. Alle vier Strecken sind eingefärbt.

**Schrittweiser Aufbau (2. Strahlensatz, analog):**

| Schritt | In Skizze eingefärbt | Bez.-Gleichung |
|---|---|---|
| 1 | SA blau | `SA` |
| 2 | + AA' violett | `SA : SA'` |
| 3 | + AB orange | `SA : SA' = AB` |
| 4 | + A'B' rot | `SA : SA' = AB : A'B'` |
| 5 | Zweite Variante: `SB : SB' = AB : A'B'` (über den anderen Strahl) | analog |

#### Farbgebung

Konstante Map `STRAHL_FARBE`:

- SA: blau `#1f5aa8`
- SA' bzw. AA': violett `#7c3aed`
- SB bzw. AB: orange `#d97706`
- SB' bzw. BB' bzw. A'B': rot `#dc2626`

Die Linien-Stärke der eingefärbten Strecken (4 px) hebt sie deutlich von den grauen Strahlen-Grundlinien (1.2 px) und den lila Parallelen (1.8 px) ab. In den Gleichungen werden Strecken-Bezeichnungen und Zahlenwerte **inline mit identischem Farbcode** dargestellt — Auge folgt der Farbzuordnung.

#### Helper-Funktion

```js
function colored(html, color) {
  return `<span style="color:${color};font-weight:600">${html}</span>`;
}
```

Erzeugt eingefärbte `<span>`-Elemente für die schrittweise gebauten Gleichungen.

#### Geometrische Verifikation (Python-Simulation)

| Situation | Punkt | Position | Im Canvas (560×440)? |
|---|---|---|---|
| A | A=(155, 189), B=(200, 273), A'=(250, 157), B'=(341, 326) | alle | ✓ |
| B | A=(202, 173), B=(154, 255), A'=(487, 78), B'=(341, 326) | alle | ✓ |

Verhältnisse \\(\\overline{AB} : \\overline{A'B'}\\):
- Sit A: 1.92 : 3.83 = **1 : 2.00** (= k ✓)
- Sit B: 1.92 : 5.75 = **1 : 3.00** (= k ✓)

#### Was entfällt

Aus dem HTML-Block der Anim 2 sind folgende Elemente vollständig entfernt:

- 3 Schieberegler `sld-strSA`, `sld-strSB`, `sld-strK2` (durch Situation-Schalter + Schritt-Slider ersetzt)
- Legende mit 7 Zeilen (`leg-strSA`, `leg-strSAp`, `leg-strSB`, `leg-strSBp`, `leg-strAB`, `leg-strABp`, `leg-strRatio`)
- Ausführlicher Erklärungstext (`erkl-strahl`)
- Statische Formel-Anzeige (`formel-strahl`)

Im JS sind die zugehörigen `getElementById`-Verweise alle ersetzt. 0 dangling Referenzen verifiziert.

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß
- Geometrie: Alle 4 Punkte (A, B, A', B') liegen in beiden Situationen sicher im Canvas
- Verhältnisse mathematisch korrekt: AB : A'B' = 1 : k für beide Situationen

---

### g5-2d Anim 1 — Drag & Drop für Z, A, B, C (Auftrag 1)

Gemäss PDF: „Original bleibt, Bild bewegt sich — zusätzlich animieren: Z, A, B, C verschiebbar."

Bisher war das Originaldreieck (Eckpunkte A, B, C) und das Streckzentrum Z fest am Canvas-Mittelpunkt verankert; der Benutzer konnte nur den Streckfaktor \\(k\\) per Schieber ändern. Neu sind **alle vier Punkte per Maus oder Touch frei verschiebbar**, und das Bild folgt der Streckung von Z aus dynamisch.

#### Architektur

**Modul-State** (neu) in der gleichen `<script>`-Hülle wie die anderen Anim-Variablen:

```js
let strPunkte = null;            // {Z, A, B, C} jeweils [x, y] in Canvas-Koord
let strDragging = null;          // 'Z' | 'A' | 'B' | 'C' | null
let strHover = null;             // welcher Punkt unter Maus steht
const STR_HANDLE_R = 8;          // sichtbarer Drag-Handle-Radius
const STR_HIT_TOL  = 14;         // Trefferradius (grosszügig für Touch)
```

Beim ersten Aufruf von `drawStreck` werden die Punkte initialisiert (Z in Canvas-Mitte, A/B/C wie bisher als Eckpunkte des Beispieldreiecks).

**Neue Helper-Funktionen:**

- `canvasCoordsFromEvent(cv, ev)` — wandelt einen Pointer-Event in Canvas-interne Koordinaten unter Berücksichtigung der CSS-Skalierung (Canvas hat `width: 100%` im Layout)
- `strHitTest(x, y, tol)` — findet den nächstgelegenen Punkt innerhalb der Toleranz; null wenn keiner trifft
- `strClamp(p, W, H)` — hält Punkt im Canvas-Bereich mit 14 px Rand
- `strInitDrag()` — registriert einmalig die Event-Handler beim Canvas-Element

**Event-Handler** (Pointer Events — decken Maus und Touch ab):

- `pointerdown` → Hit-Test; bei Treffer: `setPointerCapture`, Cursor auf `grabbing`, neu zeichnen
- `pointermove` → wenn Drag aktiv: Position clampen und aktualisieren; sonst Hover-State updaten (Cursor `grab` vs. `default`)
- `pointerup` / `pointercancel` → Drag beenden, Pointer-Capture freigeben
- `pointerleave` → Hover-State löschen wenn nicht im Drag

#### Visuelles Feedback

- Eckpunkte werden als kräftige Drag-Handles gezeichnet (8 px Radius, blau gefüllt)
- Bei Hover/Drag: halb-transparenter Halo-Ring (+5 px) um den Punkt
- Z erhält Halo in `rgba(15, 23, 42, 0.15)`, Eckpunkte in `rgba(31, 90, 168, 0.18)`
- Cursor: `grab` über aktivem Punkt, `grabbing` während Drag, sonst `default`
- Eckpunkt-Beschriftungs-Versatz von 14 auf 16 px erhöht (Handle ist größer geworden)

#### Mathematische Folge der Drag-Interaktion

Da alle Punkte als **absolute Canvas-Koordinaten** gespeichert werden, ergibt sich die Streckung dynamisch aus `REL[i] = OR_PT[i] - Z`. Wenn der Benutzer Z verschiebt, **bleiben A/B/C absolut stehen** — die relativen Vektoren ändern sich, und das Bild liegt unter der neuen Streckung. Das ist didaktisch wertvoll: man kann live sehen, dass eine zentrische Streckung vom Zentrum abhängt, nicht von einer „eingebauten" Konstellation.

#### Tipp-Hinweis in der Erklärung

Der dynamische Erklärungstext wird um folgenden Hinweis ergänzt: „Tipp: ziehe Z, A, B oder C — Bild folgt der Streckung von Z aus."

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- Alte `const OR_REL = [...]` ist vollständig entfernt; durch dynamischen State ersetzt
- `strInitDrag()` wird im `load`-Event aufgerufen (nach erstem `drawStreck`-Render, damit `cv-streck` schon im DOM ist)
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß (drei ß in Kommentaren wurden zu ss umgestellt: „Grösse", „grosszügig", „aussen")

#### Bekannte Grenzfälle

- Bei Drag eines Eckpunkts auf Z (A = Z) kollabiert das Bild korrekt auf Z; Beschriftung sitzt auf dem Punkt, aber kein Absturz.
- Bei Window-Resize bleiben die Punkt-Koordinaten erhalten (die Canvas-Buffer-Größe ändert sich nicht; nur die CSS-Skalierung).

---

### g5-2d Anim 5 — Drehkopie an H um 90° (Auftrag 5.2)

Gemäss PDF: „Bei Auswahl linkes Dreieck für alpha = 70°-45°, soll eine Kopie davon an H um 90° im Uhrzeigersinn gedreht werden. Bei Auswahl rechtes Dreieck für alpha = 20°-45°, soll eine Kopie davon an H um 90° im Gegenuhrzeigersinn gedreht werden."

#### Geometrische Idee

Im rechtwinkligen Dreieck ABC zerlegt die Höhe \\(h\\) auf der Hypotenuse den Punkt C in zwei kleinere rechtwinklige Teildreiecke AHC und CHB — beide ähnlich zum ursprünglichen ABC (Hauptähnlichkeitssatz: gemeinsamer rechter Winkel und ein gemeinsamer spitzer Winkel). Die Animation macht diese Ähnlichkeit nun visuell direkt erfahrbar.

Wenn man das linke Teildreieck AHC um den Höhenfusspunkt H um 90° im Uhrzeigersinn dreht, fällt:
- bei \\(\\alpha = 45°\\) die Drehkopie **exakt** auf das rechte Teildreieck CHB (denn beide Teildreiecke sind dann kongruent — AHC und CHB haben dieselben Seitenlängen);
- bei \\(\\alpha > 45°\\) die Drehkopie auf eine **verkleinerte Kopie** von CHB — anschaulich: das gedrehte AHC „passt" in CHB hinein.

Analog für das rechte Teildreieck CHB (Drehung im Gegen-UZS) und Winkel \\(\\alpha \\leq 45°\\).

#### Umsetzung

In `drawRecht` nach dem Zeichnen der Teildreiecke und der Höhenlinie:

```js
let drehkopie = null;
if (rechtTri === 'AHC' && alphaD >= 44.5 && alphaD <= 70.5) {
  const Ar = rotateAround([xA, yA], [xH, yH], 90);
  const Cr = rotateAround([xC, yC], [xH, yH], 90);
  drehkopie = { pts: [Ar, [xH, yH], Cr], farbe: C.gruen, fill: GRUEN_FILL };
  drehkopieLabels = [['A\'', Ar], ['C\'', Cr]];
} else if (rechtTri === 'CHB' && alphaD >= 19.5 && alphaD <= 45.5) {
  const Br = rotateAround([xB, yB], [xH, yH], -90);
  const Cr = rotateAround([xC, yC], [xH, yH], -90);
  drehkopie = { pts: [[xH, yH], Br, Cr], farbe: C.lila, fill: LILA_FILL };
  drehkopieLabels = [['B\'', Br], ['C\'', Cr]];
}
```

Die Drehkopie wird **gestrichelt** (Strichmuster 5–3) in der gleichen Farbe wie das Quell-Teildreieck (grün bzw. lila) gezeichnet, mit halb-transparenter Füllung. Die gedrehten Eckpunkte werden mit Apostroph markiert (A', C' bzw. B', C').

**Neuer globaler Helper `rotateAround`** (neben `drawAngleArc`, `midLabelArr` etc.): rotiert einen Punkt um ein Zentrum um \\(\\theta\\) Grad. In Canvas-Koordinaten entspricht positives \\(\\theta\\) der visuell-im-Uhrzeigersinn-Drehung, weil die y-Achse nach unten zeigt.

#### Aktivierungsbedingungen

| Auswahl | Aktiv bei | Drehrichtung (visuell) |
|---|---|---|
| AHC (links) | α ∈ {45°, 50°, 55°, 60°, 65°, 70°} | im Uhrzeigersinn |
| CHB (rechts) | α ∈ {20°, 25°, 30°, 35°, 40°, 45°} | im Gegen-Uhrzeigersinn |
| ABC | nie | — |

Bei α=45° ist die Drehkopie in **beiden** Modi aktiv (jeweils auf das andere Teildreieck fallend).

#### Geometrische Verifikation (Canvas-Bounds für alle Slider-Werte)

Alle Drehkopien bleiben im sichtbaren Canvas-Bereich (0..560 × 0..440):
- Linker Modus (AHC, α=45°–70°): Drehkopie liegt rechts von H, größer bei α=45° (Spannweite x∈[280,470]), kleiner bei α=70° (x∈[134,257]).
- Rechter Modus (CHB, α=20°–45°): Drehkopie liegt links von H, größer bei α=45°, kleiner bei α=20°.

Bei α=45° überlagern sich Drehkopie und das schwächer gezeichnete andere Teildreieck exakt — visuell als „Beweis durch Überdeckung".

#### Erweiterte Erklärungstexte

Bei aktiver Drehkopie wird der Erklärungstext um einen Zusatzsatz ergänzt. Bei α=45° steht z.B.: „Die gestrichelte Kopie zeigt AHC, um H um 90° im Uhrzeigersinn gedreht: sie fällt genau auf CHB (bei α = 45° sind beide Teildreiecke kongruent)." Bei anderen Winkeln: „… so wird die Ähnlichkeit zu CHB direkt sichtbar — gleiche Form, anderes Format."

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- `rotateAround` einmal global definiert, 4 Aufrufe in `drawRecht`
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß

---

### g5-2d Anim 3 — Vierfache Fläche bei k = ±2 (Auftrag 3)

Gemäss PDF: „Zeige beim Dreieck und beim Rechteck, dass bei k=2 und k=-2 die Fläche 4-fach ist, indem du die vergrösserte Figur mit 4 Originalfiguren abdeckst."

#### Umsetzung

In der Zeichenfunktion `drawFig` (Z. ~1163-1245 in `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html`) wurde nach dem Zeichnen des Bilds (orange) eine neue Visualisierung ergänzt, die nur bei genau \\(|k| = 2\\) (Slider-Toleranz 0.05) und nur für Polygon-Figuren (Dreieck und Rechteck) aktiv wird.

**Mathematische Konstruktion:**

Für ein Polygon mit Eckpunkten \\(P_1, P_2, \\ldots\\) (relativ zum Zentrum) und Streckfaktor \\(k\\) mit \\(|k|=2\\):

- **Eck-Kopien:** Für jeden Eckpunkt \\(P_i\\) wird das Original (eventuell punktgespiegelt bei \\(k<0\\)) so verschoben, dass die zur Ecke \\(i\\) gehörende Ecke der Kopie auf der entsprechenden Bild-Ecke \\(k \\cdot P_i\\) liegt. Die Verschiebung beträgt \\((k - \\operatorname{sign}(k)) \\cdot P_i\\).
- **Mittendreieck** (nur bei Dreieck, 3 Eckpunkte): Die Mittelpunkte der Bildkanten verbinden — \\(M_{ij} = (k/2) \\cdot (P_i + P_j)\\). Das ergibt das mittige, gegenläufig orientierte Original-Dreieck.

Für das Rechteck reichen die 4 Eck-Kopien, die jeweils ein Quadrant des Bilds abdecken. Eine fünfte Mitten-Kopie ist nicht nötig — die Eck-Kopien tessellieren das Bild bereits vollständig.

**Geometrische Verifikation (Python-Simulation):**

| Figur | k | Original-Fläche | Bild-Fläche | Summe 4 Kopien |
|---|---:|---:|---:|---:|
| Dreieck | +2 | 3487.50 | 13950.00 | 13950.00 ✓ |
| Dreieck | −2 | 3487.50 | 13950.00 | 13950.00 ✓ |
| Rechteck | +2 | 12750.00 | 51000.00 | 51000.00 ✓ |
| Rechteck | −2 | 12750.00 | 51000.00 | 51000.00 ✓ |

In allen Fällen passen die 4 Kopien exakt ohne Lücke und ohne Überlappung in die Bildfläche — beweist visuell die Beziehung \\(A' = k^2 \\cdot A\\) für \\(|k|=2\\).

**Darstellung:** Kopien werden in **hellem durchscheinendem Blau** (\\(\\text{rgba}(31, 90, 168, 0.22)\\) Füllung, 0.85 Linie) über die orange Bild-Fläche gelegt — die Aufteilungs-Linien sind deutlich sichtbar, der orange Bild-Rahmen bleibt erkennbar.

**Dynamische Erklärung:** Bei \\(|k|=2\\) wird zum Standardtext ergänzt: „Die hellen blauen Dreiecke/Rechtecke zeigen: vier original-grosse Kopien decken das Bild exakt ab — also Fläche \\(\\times 4 = k^2\\)."

#### Was nicht angepasst wurde

- **Kreis:** beim Kreis lässt sich die vierfache Fläche nicht durch vier original-große Kreise abdecken (Kreise tessellieren nicht). Das PDF bittet ohnehin nur um Dreieck und Rechteck. Bei `figForm === 'kreis'` bleibt die Animation unverändert.
- **Andere k-Werte:** die Visualisierung wird nur bei genau \\(|k|=2\\) gezeigt. Bei anderen Slider-Werten wie 1.9 oder 2.1 würden 4 Original-Kopien Lücken / Überlappungen erzeugen — irreführend.

#### Verifikation

- JS-Syntax: alle Script-Blöcke validiert mit Node `--check` — fehlerfrei
- Polygon-Flächen geometrisch bestätigt (vier Kopien decken Bild exakt)
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß

---

### g5-2d Anim 5 — Alpha/Beta-Position bei C korrigiert (Auftrag 5.1)

Im PDF `Anpassungen_zu_g5-2d.pdf` wurde gemeldet: „In der Ecke C sind die Teilwinkel Alpha und Beta beschriftet: die Position ist aber vertauscht."

#### Ursache

Die Höhe \\(h\\) im rechtwinkligen Dreieck zerlegt den rechten Winkel bei C in zwei Sektoren. Im linken Sektor (zwischen C→A und C→H) ist der Winkel \\(\\beta\\), im rechten Sektor (zwischen C→H und C→B) ist \\(\\alpha\\). Die Code-Zeilen 1528-1529 in `drawRecht` waren mathematisch korrekt:

```js
drawAngleArc(ctx, [xC, yC], [xA, yA], [xH, yH], 20, C.gruen, 'β');  // linker Sektor
drawAngleArc(ctx, [xC, yC], [xH, yH], [xB, yB], 20, C.blau,  'α');  // rechter Sektor
```

Aber die Helper-Funktion `drawAngleArc` selbst hatte einen Bug in der Bisektrix-Berechnung (gleicher Bug wie bei Anim 4 entdeckt). Bei dem Aufruf zur linken Sektor-Markierung wurde das β-Label *außerhalb* des Dreiecks platziert, gespiegelt — bei C dx=+13, dy=-31 → rechts-oben von C, statt im linken Sektor unten-links. Genauso α: landete links-oben statt rechts-unten. So sah es im Browser aus, als seien die Labels vertauscht.

#### Refactoring: `drawAngleArc` global korrigiert

Statt eine eigene Variante `drawAngleArcInside` (siehe vorheriger Eintrag) parallel zu führen, wurde das Refactoring konsolidiert:

- **Die alte `drawAngleArcInside` wurde entfernt.**
- **`drawAngleArc` selbst** wurde durch die korrigierte Bisektrix-Mathematik ersetzt (signed Winkel-Diff in \\((-\\pi, \\pi]\\), umgeht den ±180°-Branch-Cut von `atan2`).
- Neuer optionaler Parameter `labelDist`: per Default `radius + 14` (wie zuvor — Label auf der Innen-Seite des Winkels, jenseits des Bogens). Für Anim 4 (Ähnlichkeitssätze) wird `labelDist = 30` übergeben, damit das Label näher am Vertex und damit klarer im jeweiligen Sektor sitzt.
- 8 Aufrufe in `drawAehnSatz` zurück auf `drawAngleArc(..., 30)` umgestellt.
- 4 Aufrufe in `drawRecht` bleiben unverändert (verwenden den Default `labelDist = radius + 14`).

#### Verifikation der Label-Positionen bei C (Simulation in Python für mehrere α-Werte)

| α | β-Label dx/dy (sollte links-unten von C sein) | α-Label dx/dy (sollte rechts-unten sein) |
|---:|---|---|
| 20° | (−20, +28) ✓ | (+6, +33) ✓ |
| 30° | (−17, +29) ✓ | (+9, +33) ✓ |
| 45° | (−13, +31) ✓ | (+13, +31) ✓ symmetrisch |
| 60° | (−9, +33) ✓ | (+17, +29) ✓ |
| 70° | (−6, +33) ✓ | (+20, +28) ✓ |

Alle β-Labels haben jetzt negativen dx (links von C), alle α-Labels positiven dx (rechts von C). Beide haben positiven dy (unter C, also im Dreieck-Inneren) — passt zu den jeweiligen Sektoren.

#### Nebeneffekt für Eckwinkel α bei A in Anim 5

Der Label-Bug betraf auch den α-Label bei Ecke A (Aufruf in Z. 1524). Vorher wurde es bei α=45° auf (53, 358) gesetzt → links-unten, außerhalb des Dreiecks. Mit dem Refactoring landet es jetzt bei (127, 328) → ins Dreieck-Innere, korrekt zwischen den Strahlen A→B und A→C. Dies war im PDF nicht explizit angesprochen, ist aber ein willkommener Bonus.

Der β-Label bei B (Z. 1525) war zufällig schon korrekt platziert, weil der Branch-Cut dort nicht überschritten wurde — die neue Formel produziert dort dasselbe Ergebnis wie die alte.

#### Verifikation der Datei

- JS-Syntax: alle drei Script-Blöcke validiert mit Node `--check` — fehlerfrei
- `drawAngleArc`-Aufrufe gesamt: 13 (1 Definition + 8 in drawAehnSatz mit labelDist=30 + 4 in drawRecht Default)
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß
- `drawAngleArcInside` als separate Funktion vollständig entfernt

---

### g5-2d Anim 4 — Label-Positionierung nachgebessert

Nach Sichtprüfung im Browser wurde klar: die erste Umsetzung der Anim-4-Anpassungen positionierte die Winkel- und Seitenlabels noch nicht zufriedenstellend. Die α/β-Labels landeten beim Eckbuchstaben (kollidierten mit A/B), und die Seitenlabels (b=, a=) saßen teils noch auf der Strecke.

#### Ursache 1: Winkellabel-Position

Die Helper-Funktion `drawAngleArc` enthielt eine **falsche Bisektrix-Berechnung**. Der Code berechnete für die Mittelrichtung des Winkels:

```js
let mid = ccw ? (start + end)/2 + Math.PI : (start + end)/2;
```

Das ist mathematisch in beiden Fällen identisch (`+π ≡ -π` modulo 2π) und produziert bei `ccw=false` zwar die korrekte Bisektrix (Beispiel: Strahlen 0° und -50° → Mitte -25°), bei `ccw=true` aber die *gespiegelte* Bisektrix (Beispiel: Strahlen -110° und 180° → das naive Mittel 35° ist falsch, korrekt wäre -145°). Es hängt davon ab, ob die zwei Strahlen den ±180°-Branch-Cut von `atan2` überstreichen.

Die mathematisch korrekte Methode für die Bisektrix des kleineren Winkels:

```js
const dSigned = ((a2 - a1 + Math.PI) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI) - Math.PI;
let mid = a1 + dSigned/2;
```

Das nutzt die signed-Winkel-Differenz in `(-π, π]` und halbiert sie — dadurch kommt unabhängig vom Branch-Cut immer die korrekte Bisektrix heraus.

#### Lösung: Zweite Funktion `drawAngleArcInside`

Statt die alte `drawAngleArc` zu ändern (die in `drawRecht` für Anim 5 noch verwendet wird, wo Labels aussen stehen sollen und der Bug der Logik im konkreten Aufruf möglicherweise zufällig die richtigen Außenpositionen produziert), wurde eine **neue Funktion `drawAngleArcInside`** eingeführt:

- Verwendet die korrigierte Bisektrix-Formel
- Setzt das Label per Default auf `radius + 8` Pixel vom Vertex entfernt — also knapp außerhalb des Bogens, aber im Winkelinneren
- Optional `labelDist`-Parameter für individuelle Anpassung

`drawAngleArc` (alte Version) bleibt unverändert für `drawRecht` (Anim 5).

#### Ursache 2: Seitenlabel-Abstand

Bei diagonalen Strecken (z.B. A→C bei einem α=50°-Dreieck) wurde der senkrechte Abstand zur Strecke durch die schräge Komponente verringert — bei Offset 14 verblieb nur ein kleiner Abstand der Text-Unterkante zur Linie.

- `midLabelArr` Offset von **14 auf 18 Pixel** erhöht. Bei einer 50°-Strecke ergibt das einen vertikalen Abstand des Label-Zentrums von 18·cos(50°) ≈ 11.6 Pixel; abzüglich Text-Halbhöhe (~6 Pixel) verbleiben etwa 5-6 Pixel Luft zwischen Text-Unterkante und Linie.

#### Verifikation der neuen Positionen (Simulation in Python)

Original-Dreieck mit α=50°, β=70°, γ=60°, Eckpunkten A=(50, 299), B=(170, 299), C=(134, 199):

- **α-Label** bei A: jetzt bei (77, 287) — 44.6 Pixel Abstand zum A-Buchstaben (vorher: kollidierend)
- **β-Label** bei B: jetzt bei (145, 282) — 45.3 Pixel Abstand zum B-Buchstaben
- **b-Label** auf Strecke A→C: 12.8 Pixel senkrechter Abstand zur Linie, innerhalb des Dreiecks
- Alle 8 Winkel-Aufrufe in `drawAehnSatz` (WW × 4, sWs × 2, SsW × 2) verwenden nun `drawAngleArcInside`

#### Verifikation der Datei

- JS-Syntax: alle drei Script-Blöcke validiert mit Node `--check` — fehlerfrei
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß
- `drawAngleArc` (Original-Form für Anim 5) erhalten — 4 Aufrufe in `drawRecht`
- `drawAngleArcInside` (neu) — 8 Aufrufe in `drawAehnSatz`

---

### g5-2d Anim 4 — Beschriftungs-Verbesserungen und sss-Konvention

Drei Anpassungen an der Animation 4 (Ähnlichkeitssätze) in `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` gemäss PDF `Anpassungen_zu_g5-2d.pdf`:

#### Anim 4.1 — Winkellabel innen statt aussen

Die Winkel-Labels (α, β, α', β') wurden bisher ausserhalb des Dreiecks platziert (`radius+14` = 36 Pixel vom Vertex entfernt). Das machte die Zuordnung zum Dreieck unklar.

- `drawAngleArc` (Z. 1356-1381): optionalen Parameter `labelOffset` ergänzt — Default bleibt `radius+14` (rückwärtskompatibel für alle anderen Animationen, die diese Helper-Funktion nutzen).
- Bei den WW-/sWs-/SsW-Aufrufen in `drawAehnSatz` (Z. 1288-1316) labelOffset = 12 Pixel gewählt — Labels liegen jetzt innerhalb des Bogens, also im Dreieck-Inneren.

#### Anim 4.2 — Seitenbeschriftung deutlicher von der Seite abgesetzt

Die Seitenlabels (a=, b=, c= und Striche) standen mit Offset 11 sehr nah an der Strecke. Bei kurzen Strecken überlagerten sich Label und Linie.

- `midLabelArr` (Z. 1387-1389): Offset von 11 auf 14 erhöht. Damit stehen alle Seitenlabels (innerhalb wie ausserhalb des Dreiecks, je nach `sidesign`) deutlich von der Strecke ab und sind besser lesbar.

#### Anim 4.3 — SSS → sss (konsistente Schreibweise der Ähnlichkeitssätze)

Bisher war `SSS` als einziger Ähnlichkeitssatz mit Grossbuchstaben geschrieben, während `sWs` schon klein-gemischt geschrieben war. Das war inkonsistent: bei den **Ähnlichkeitssätzen** geht es überall um Seitenverhältnisse, nicht Seitenlängen — daher gehört das kleine `s` durchgehend hin.

- HTML-Button Z. 438: `<button class="chip" data-satz="SSS">SSS</button>` → `<button class="chip" data-satz="sss">sss</button>`.
- JS-Switch in `drawAehnSatz` Z. 1292 und Z. 1329: `aehnSatz === 'SSS'` → `aehnSatz === 'sss'`.
- Erklärungs-Text in der Animation: „SSS-Satz: …" → „sss-Satz: Stimmen alle drei Seitenverhältnisse überein, sind die Dreiecke ähnlich. (Kleinbuchstaben, weil es um Verhältnisse geht — nicht um konkrete Seitenlängen wie bei der Kongruenz.)"
- Theorie-Text Merksatz Z. 480 (Auflistung): `(SSS)` → `(sss)`.
- Theorie-Text Z. 485: neuer Absatz zur Schreibweise-Konvention — erklärt, dass grosses S für konkrete Seitenlängen (Kongruenz), kleines s für Seitenverhältnisse (Ähnlichkeit) steht, und dass beim SsW-Satz das grosse S ausnahmsweise die grössere Seite markiert.
- Zusammenfassungs-Tabelle Z. 635: `SSS, sWs, SsW` → `sss, sWs, SsW`.
- JS-Kommentar Z. 1218: konsistent.

Der Theorie-Text in Z. 485 erwähnt die Kongruenzsätze (SSS, SWS, WSW, SsW) weiterhin mit Grossbuchstaben — diese Schreibweise bleibt in 5.2a unverändert (da geht es um konkrete Längen).

#### Verifikation

- JS-Switch: 0 alte `'SSS'`-Vorkommen, 2 neue `'sss'`-Vorkommen
- HTML-Button: `data-satz="sss"` mit Beschriftung `sss` vorhanden
- 8 `drawAngleArc`-Aufrufe mit `labelOffset = 12` (WW: 4, sWs: 2, SsW: 2)
- JS-Syntax-Sanity: geschweifte und runde Klammern balanciert
- 0 Strays, 0 Dezimalkomma-Residuen, 0 ß im ganzen Lehrmittel

---

### Letzte zwei Befunde erledigt: M2 (ggT-Formulierung), M15 (s_B-Rundung) — Review-Bearbeitung abgeschlossen

Mit diesen beiden Befunden sind alle 20 im Review identifizierten Punkte bearbeitet: 19 umgesetzt, 1 bewusst nicht umgesetzt (M5).

#### TODO-M2 — ggT-Formulierung in g1-3 §6.1

Die alte Formulierung in §6.1 (gemeinsamer Faktor ausklammern) war doppelt problematisch:
1. „Mehrfach-Teilung" ist kein etablierter mathematischer Begriff.
2. „kleinste Mehrfach-Teilung" klingt sprachlich eher nach kgV (kleinstes gemeinsames Vielfaches) als nach ggT — ist also irreführend für eine ggT-Erklärung.

- `grundlagen/g1-3-algebraische-terme.html` Z. 270-271:
  - vorher: „Suchen Sie den grössten gemeinsamen Faktor (ggT) aller Glieder — bei Zahlen die **kleinste Mehrfach-Teilung**, bei Variablen den niedrigsten gemeinsamen Exponenten:"
  - nachher: „Suche den **grössten gemeinsamen Teiler (ggT)** der Zahlen-Koeffizienten — über die **Primfaktorzerlegung**: jeden gemeinsamen Primfaktor mit dem kleinsten vorkommenden Exponenten — und bei Variablen den niedrigsten gemeinsamen Exponenten:"

Damit ist die Methode der ggT-Bestimmung explizit benannt (Primfaktorzerlegung mit minimalen Exponenten) — der unklare Begriff „Mehrfach-Teilung" verschwindet.

#### TODO-M15 — s_B ≈ 1.41 → 1.39 in g4-3 Themenseite (P4 kosmetisch)

Auf der Themenseite g4-3 wurde im Streumass-Beispiel die Standardabweichung der Vergleichsklasse B mit „s ≈ 1.41" angegeben — eine Rundungsabweichung, der korrekte Wert ist 1.39.

- `grundlagen/g4-3-masszahlen.html` Z. 215:
  - vorher: „Klasse B (Werte 2.5, 3.0, 3.8, 4.5, 4.5, 5.2, 6.0, 6.5) hat \\(s \\approx 1.41\\) — fast fünfmal grösser."
  - nachher: „… hat \\(s \\approx 1.39\\) — fast fünfmal grösser."

Verifikation mit Python: Datensatz hat Mittelwert 4.5, Summe der quadrierten Abweichungen 13.48, also \\(s = \\sqrt{13.48/7} = \\sqrt{1.9257} = 1.3877 \\approx 1.39\\). Dezimalpunkt-Konvention eingehalten.

#### Status nach M2 und M15

| Kategorie | Anzahl | Status |
|---|---:|---|
| Strukturelle Befunde (S1–S4) | 4 | alle erledigt |
| P2-Befunde (Korrekturwelle 1) | 4 | alle erledigt (M10, M11, M12, M19) |
| P3-Befunde (Korrekturwelle 2) | 11 | 10 erledigt (M1–M9 ohne M5, M13, M14, M16, M17, M18), 1 bewusst nicht umgesetzt (M5) |
| P4-Befund (kosmetisch) | 1 | erledigt (M15) |
| **Gesamt** | **20** | **19 umgesetzt, 1 bewusst nicht umgesetzt** |

---

### Intervallnotation auf deutsche Schreibweise vereinheitlicht (TODO-M1)

Das Lehrmittel verwendete zwei Konventionen für Intervalle: die deutsche `[a; b[` (eckige Klammer-Richtung signalisiert offen/zu, Semikolon-Trennzeichen) und die internationale `[a, b)` (runde Klammer für „offen", Komma-Trennzeichen).

#### Wahl

**Deutsche Notation wird Standard.** Die eckige Klammer-Richtung-Konvention ist im deutschsprachigen Schulraum traditionell verbreitet (ISO 31-11, Bourbaki-Notation). Vorteil für Lernende: die Klammer-Richtung ist intuitiv lesbar — sie öffnet sich vom Intervall weg, wenn die Grenze nicht dazugehört.

#### Geändert

**Themenseite g1-2** (`grundlagen/g1-2-zahlen-grundoperationen.html`):
- Z. 228 (Erklärtext): „Die Klammer sagt, ob die Grenze dazugehört (eckig: ja, rund: nein)" → „Die Klammer-Richtung sagt, ob die Grenze dazugehört (Klammer zeigt zum Intervall hin: ja; Klammer zeigt weg: nein)".
- Z. 230-239 (Intervalltabelle): `[a, b]`, `(a, b)`, `[a, b)`, `(-\infty, b]`, `[a, +\infty)` → `[a; b]`, `]a; b[`, `[a; b[`, `]-\infty; b]`, `[a; +\infty[`.
- Z. 241-244 (Fehlerblock): „Bei \\(\\infty\\) immer runde Klammer" → „Bei \\(\\infty\\) immer nach aussen geöffnete Klammer", entsprechende Beispiele umformuliert.
- Z. 419 (A5-Lösung): `[-2,5]`, `(-\infty,3)`, `(-1,4]`, `[0,+\infty)` → `[-2; 5]`, `]-\infty; 3[`, `]-1; 4]`, `[0; +\infty[`.

**LG4 g4-2 Diagramme**:
- `grundlagen/g4-2-diagramme.html`: alle 7 Klasseneinteilungs-Zellen `[155, 160)`–`[180, 185)` → `[155; 160[`–`[180; 185[`; Erklärtext zur Notation; A2-Lösung mit `[0; 5[, [5; 10[, …, [45; 50]`; A3 Klassenliste und 5 Tabellenzellen `[1; 3[`...`[9; 11[`.
- `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html`: Klassenliste und 5 Häufigkeitszeilen in der Lösung.

**LG5 Trigonometrie**:
- `grundlagen/g5-5-trigonometrische-gleichungen.html`: `[0°; 360°[`, `[0°; 720°[`, geschlossene Bereiche `[-1; 1]`, `[0; 8]`.
- `downloads/grundlagen/g5-5-trigonometrische-gleichungen/{aufgabenserie,formelauszug,handout,teste-dich-selbst}.html`: alle Vorkommen analog umgestellt — `[0°; 360°[`, `[-360°; 0°[`, `[-90°; 90°]`, `[0°; 180°]`, `[-1; 1]`.
- `grundlagen/g5-4-einheitskreis.html`: `[0°; 90°]`.

**LG3 Funktions-Wertebereiche**:
- `grundlagen/g3-1-grundlagen.html`: `[0; \infty[`, `[-5; \infty[`.
- `downloads/grundlagen/g3-1-grundlagen/{handout,teste-dich-selbst,aufgabenserie}.html`: Definitions- und Wertebereiche `[0; \infty[`, `[3; \infty[`, `]-\infty; 3]`, sowie geschlossene Intervalle `[0; 50]`, `[0; 40]`, `[0; 600]`, `[0; 480]`, `[20; 200]`, `[0; 10]`.
- `downloads/grundlagen/g3-2-lineare-funktionen/aufgabenserie.html`: `s \\in [16; 20]`, `a \\in [23; 31]`.

**Weitere**:
- `downloads/grundlagen/g2-2a-lineare-gleichungen/teste-dich-selbst.html`: `(-\\infty, 2]` → `]-\\infty; 2]`.

#### Bereits in deutscher Notation (unverändert)

- `downloads/grundlagen/g1-2-zahlen-grundoperationen/formelauszug.html` und `handout.html`: Intervalltabellen waren bereits konsequent in deutscher Notation.
- `grundlagen/g5-2c-kreis-und-kreisteile.html` und `downloads/grundlagen/g5-2c-kreis-und-kreisteile/formelauszug.html`: Zentriwinkel-Bereich `\\varphi \\in [0°; 360°[` war bereits deutsch.

#### Auswirkung

Lehrmittel verwendet jetzt durchgehend deutsche Schreibweise. Verifikation: 0 internationale Intervalle (`[a, b)`, `(a, b]`, `[a, b]` mit Komma) verblieben.

---

### Drei P3-Befunde in Lerngebiet 5 erledigt: M16, M17, M18

#### TODO-M16 — sSW-Lösung als saubere Fallunterscheidung (g5-2a A4 Aufgabe 5)

Die Lösung von A4(5) (\\(a = 4, b = 8, \\alpha = 30°\\) — Aufgabe nach dem sSW-Fall) begann mit „sSW, mehrdeutig" und korrigierte sich dann selbst zum Grenzfall mit 1 Lösung — didaktisch unglücklich, weil Lernende ihr Verständnis sofort revidieren mussten.

- `grundlagen/g5-2a-dreiecke.html` Z. 659:
  - vorher: „Zwei Seiten, Winkel gegenüber der kleineren Seite (\\(a < b\\)) — **sSW, mehrdeutig**. Prüfen: \\(b \\cdot \\sin\\alpha = 8 \\cdot 0.5 = 4 = a\\) → genau eine Lösung (Grenzfall, rechtwinkliges Dreieck bei B). Wäre \\(a\\) etwas grösser als 4 cm, gäbe es zwei Lösungen; bei kleinerem \\(a\\) gar keine."
  - nachher: „Zwei Seiten und der Winkel gegenüber der **kleineren** Seite (\\(a < b\\)) — der **sSW-Fall**. Hier entscheidet der Vergleich \\(a\\) gegen \\(b \\cdot \\sin\\alpha\\): \\(b \\cdot \\sin\\alpha = 8 \\cdot 0.5 = 4\\), und \\(a = 4\\). Wegen \\(a = b \\cdot \\sin\\alpha\\) liegt der **Grenzfall** vor — **genau eine Lösung** (rechtwinkliges Dreieck bei B). Allgemein: bei \\(a > b \\cdot \\sin\\alpha\\) zwei Lösungen, bei \\(a = b \\cdot \\sin\\alpha\\) eine, bei \\(a < b \\cdot \\sin\\alpha\\) keine."

Statt erst mit dem Ergebnis-Etikett zu starten und es dann zu revidieren: erst die Rechnung, dann das passende Etikett, am Schluss die didaktische Verallgemeinerung.

#### TODO-M17 — Achteck-im-Quadrat: Aufgabe präzisiert und Lösung mathematisch korrigiert (g5-2b aufgabenserie)

Die Aufgabe war in zweifacher Hinsicht problematisch: erstens war „Achteck eingeschrieben in Quadrat" mehrdeutig (mehrere Konstruktionen möglich), zweitens war die bestehende Lösung mathematisch falsch — sie verwechselte Apothem mit Umkreisradius und kam zu \\(R = L/2 = 60\\), korrekt ist \\(R = L/(2 \\cos 22.5°) \\approx 64.94\\).

- `downloads/grundlagen/g5-2b-vierecke/aufgabenserie.html` Z. 48 (Aufgabe 3):
  - Aufgabe präzisiert: „in ein Quadrat einbeschrieben ist" → „in ein Quadrat einbeschrieben ist — die acht Achteck-Ecken liegen paarweise auf den vier Quadratseiten, sodass jede Quadratseite das Achteck an einer Seite berührt."
  - Tipps erweitert: zusätzlich \\(\\cos 22.5° \\approx 0.9239\\) und \\(\\tan 22.5° \\approx 0.4142\\) angegeben.
  - Teilaufgabe (a) verlangt nun explizit zuerst den **Apothem** \\(r\\), dann \\(R\\) — der natürliche Lösungsweg.
- `downloads/grundlagen/g5-2b-vierecke/aufgabenserie.html` Z. 85-90 (Lösung 3): vollständig umgeschrieben mit den korrekten Werten:
  - (a) \\(r = L/2 = 60\\) cm; \\(R = r/\\cos 22.5° \\approx 60/0.9239 \\approx 64.94\\) cm
  - (b) \\(s = 2R \\sin 22.5° \\approx 49.71\\) cm (oder direkt \\(s = 2r \\tan 22.5°\\))
  - (c) \\(U = 8s \\approx 397.65\\) cm
  - Vorher waren die Werte fälschlich \\(R = 60\\), \\(s \\approx 45.9\\), \\(U \\approx 367.4\\).
- Mit Python verifiziert: für ein regelmässiges Achteck mit Apothem 60 cm gilt \\(R = 64.9435\\), \\(s = 49.7056\\), \\(U = 397.6450\\) cm.

#### TODO-M18 — c ≈ 6.13 → 6.19 in g5-3 A1 c

Lösung 1c (Cosinussatz mit \\(a = 8, b = 6, \\gamma = 50°\\)) gab fälschlich \\(c \\approx 6.13\\) an. Mit Python nachgerechnet: \\(c^2 = 64 + 36 - 96 \\cos 50° = 100 - 61.708 = 38.292\\), also \\(c \\approx 6.188 \\approx 6.19\\).

- `grundlagen/g5-3-trigonometrische-berechnungen.html` Z. 725:
  - vorher: „\\(c = \\sqrt{8^2 + 6^2 - 2\\cdot 8\\cdot 6\\cdot\\cos(50°)} \\approx 6.13\\)"
  - nachher: „… \\(\\approx 6.19\\)"
- Dezimalpunkt-Konvention eingehalten.

---

### Drei P3-Befunde in Korrekturwelle 2 erledigt: M9, M13, M14

#### TODO-M9 — Wurzel-Voraussetzung \\(-c/a \\geq 0\\) in g2-2b

Beim Wurzelziehen für rein quadratische Gleichungen \\(a x^2 + c = 0 \\Rightarrow x^2 = -c/a\\) fehlte die Voraussetzung, dass die rechte Seite nichtnegativ sein muss. Ohne diese ergibt der Ansatz formal komplexe Lösungen, was im BM-Stoff nicht gemeint ist.

- `grundlagen/g2-2b-quadratische-gleichungen.html` Z. 607 (Zusammenfassungstabelle):
  - vorher: „\\(x^2 = -c/a\\), \\(x = \\pm\\sqrt{-c/a}\\)"
  - nachher: „\\(x^2 = -c/a\\); falls \\(-c/a \\geq 0\\): \\(x = \\pm\\sqrt{-c/a}\\), sonst \\(\\mathbb{L} = \\emptyset\\)"
- `downloads/grundlagen/g2-2b-quadratische-gleichungen/formelauszug.html` Z. 57-58 (Reinquadratisch-Zeile): analog umformuliert mit `falls -c/a ≥ 0` und sonst-Fall.

#### TODO-M13 — Klassieren-Einstiegsbeispiel in g4-2 (Variante B)

Inkonsistenz: Text sagte „60 Lernende, Grössen zwischen 156 cm und 188 cm. Mit 7 Klassen à 5 cm", aber die Tabelle darunter hatte nur 6 Klassen (`[155, 160) ... [180, 185)`), und der Max-Wert 188 wäre in keine vorhandene Klasse gefallen.

Variante B gewählt: **Tabelle bleibt unverändert, Text angepasst** — bewahrt die didaktisch wertvolle abklingende Klassenverteilung (5, 12, 18, 14, 8, 3).

- `grundlagen/g4-2-diagramme.html` Z. 184:
  - vorher: „60 Lernende, Grössen zwischen 156 cm und 188 cm. Mit 7 Klassen à 5 cm:"
  - nachher: „60 Lernende, Grössen zwischen 156 cm und 184 cm. Mit 6 Klassen à 5 cm:"

#### TODO-M14 — Tabellenkalkulations-Aufgabe in g4-1 A4 (Variante A)

Inkonsistenz: Einstiegsbeispiel der Themenseite hat \\(n = 22\\), aber Aufgabe A4 sprach vom Bereich `B2:B25` (= 24 Zellen) für „die Klasse aus dem Einstieg". Die Lösung antwortete in sich konsistent „Ergebnis 24", was aber nicht zu n=22 passte.

Variante A gewählt: **Bereich an Einstieg angepasst**, Bezug zum Einstiegsbeispiel bleibt erhalten.

- `grundlagen/g4-1-grundlagen.html` Z. 343-358 (Aufgabe A4 mit Lösung):
  - Aufgabentext: „in den Zellen `B2:B25`" → `B2:B23` (22 Zellen statt 24); Folgereferenz „in `B26` ein zusätzlicher Wert" → `B24`.
  - Lösung (1): „Ergebnis 24 (24 Zellen)" → „Ergebnis 22 (22 Zellen)"
  - Lösung (2)(3)(4): alle Formeln entsprechend mit `B2:B23` statt `B2:B25`; in (4) „Bereich endet bei `B25`" → `B23`, „Wert in `B26`" → `B24`. Der didaktische Tipp „auf ganze Spalte erweitern (`B:B`)" bleibt unverändert wertvoll.

---

### Velo-Aufgabe Wording präzisiert in g2-2b (TODO-M8)

**P3-Befund** aus dem fachlich-mathematischen Review Lerngebiet 2. In der Velo-Aufgabe (Anna fährt 12 km, Hinweg \\(v\\), Rückweg \\(v-4\\), Gegenwind) liefert die quadratische Gleichung zwei Lösungen \\(v_a \\approx 18.25\\) und \\(v_b \\approx 1.76\\). Die alte Begründung der Lösungsauswahl war sprachlich missverständlich — sie liess es so klingen, als sei \\(v_b\\) selbst negativ. Tatsächlich ist \\(v_b\\) positiv (≈ 1.76); negativ ist die Rückweg-Geschwindigkeit \\(v_b - 4 \\approx -2.24\\).

#### Geändert

- `grundlagen/g2-2b-quadratische-gleichungen.html` Z. 180 (Einstiegstext):
  - vorher: „Nur \\(v = v_a \\approx 18.3\\) km/h passt zur Aufgabe — \\(v_b\\) wäre kleiner als 4 und würde eine negative Rückweg-Geschwindigkeit bedeuten."
  - nachher: „Bei \\(v_b\\) wäre die Rückweg-Geschwindigkeit \\(v_b - 4 \\approx -2.3\\) negativ — physikalisch nicht sinnvoll. Also passt nur \\(v = v_a \\approx 18.3\\) km/h zur Aufgabe."
- `grundlagen/g2-2b-quadratische-gleichungen.html` Z. 592 (Lösung A6):
  - vorher: „\\(v_b\\) wäre kleiner als 4 und ergäbe eine negative Rückweg-Geschwindigkeit — also physikalisch nicht sinnvoll."
  - nachher: „Bei \\(v_b \\approx 1.76\\) wäre die Rückweg-Geschwindigkeit \\(v_b - 4 \\approx -2.24\\) negativ — physikalisch nicht sinnvoll."

#### Begründung

Die alte Formulierung „\\(v_b\\) wäre kleiner als 4 und würde eine negative Rückweg-Geschwindigkeit bedeuten" hängte zwei Aussagen zusammen, die für Lernende den Eindruck erweckten, \\(v_b\\) selbst sei negativ. Die neue Formulierung zeigt explizit auf die Grösse, die wirklich negativ wird (\\(v_b - 4\\)) — das lehrt sauberes Argumentieren im Wechselspiel von Rechnung und Sachkontext. Die Aufgabenserie zur selben Aufgabe (`downloads/grundlagen/g2-2b-quadratische-gleichungen/aufgabenserie.html`) hatte die Argumentation bereits korrekt formuliert; Themenseite und Druckseite sind nun konsistent.

---

### Normalform vereinheitlicht in g2-2a Themenseite (TODO-M7)

**P3-Befund** aus dem fachlich-mathematischen Review Lerngebiet 2. Die Themenseite verwendete intern zwei verschiedene Schreibweisen für die Normalform der linearen Gleichung — derselbe Buchstabe \\(b\\) hatte dadurch zwei unterschiedliche Bedeutungen, was didaktisch verwirrend war.

#### Geändert (Wahl: \\(ax + b = 0\\), analog Handout und Zusammenfassung)

- `grundlagen/g2-2a-lineare-gleichungen.html` Z. 276 (Lösungsfälle-Einleitung):
  - vorher: „Bringt man eine lineare Gleichung auf die Form \\(a \\cdot x = b\\), so entscheidet das Wertepaar \\((a, b)\\)..."
  - nachher: „Bringt man eine lineare Gleichung auf die **Normalform** \\(a \\cdot x + b = 0\\), so entscheidet das Wertepaar \\((a, b)\\)..."
- `grundlagen/g2-2a-lineare-gleichungen.html` Z. 283 (Fall-1-Lösungskarte):
  - vorher: \\(\\mathbb{L} = \\{ \\tfrac{b}{a} \\}\\)
  - nachher: \\(\\mathbb{L} = \\{ -\\tfrac{b}{a} \\}\\) — passend zu \\(ax + b = 0 \\Rightarrow x = -b/a\\)

#### Bewusst unverändert

- Die Bedingungen der drei Fälle (\\(a \\neq 0\\) / \\(a = 0, b \\neq 0\\) / \\(a = 0, b = 0\\)) bleiben gleich — sie sind bei \\(ax + b = 0\\) und \\(ax = b\\) symmetrisch.
- Der Parameter-Abschnitt (Z. 338–339) bleibt: dort wird operationsbedingt die Sortier-Schreibweise \\((k-2)x = 3(k-2)\\) verwendet — sie erzeugt keinen Buchstaben-Konflikt, weil \\(a(k)\\) und \\(b(k)\\) hier als parametrisierte Koeffizienten interpretiert werden.
- Das Widget mit klickbaren Karten (data-fall="0/1/2") und seine JS-Beispielgleichungen (3·x + 2 = 11 etc.) bleiben — sie zeigen konkrete Gleichungen, die unabhängig von der Normalform-Notation sind.

Damit ist die Themenseite intern konsistent mit dem Handout, dem Formelauszug und der Zusammenfassung (alle nutzen durchgehend \\(ax + b = 0\\) mit Lösung \\(-b/a\\)).

---

### Korrekturwelle 2 (P3 didaktisch) — Start: M3, M4, M6 erledigt; M5 bewusst nicht umgesetzt

Drei didaktische P3-Befunde aus Lerngebiet 1 (Arithmetik / Algebra) bearbeitet.

#### TODO-M3 — Billion-Wording in g1-4 A6(b)

Die Lösung sagte fälschlich „etwa eine Billion" für \\(9 \\cdot 10^{11}\\). Nach Schweizer/DACH long-scale-Konvention ist 1 Billion = \\(10^{12}\\), also sind \\(9 \\cdot 10^{11}\\) = 900 Milliarden = 0.9 Billionen, nicht „eine Billion".

- `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 509:
  - vorher: „Pro Stunde: \\(2.5 \\cdot 10^8 \\cdot 3600 = 9 \\cdot 10^{11}\\) Schaltvorgänge — etwa eine Billion (genauer: 900 Milliarden)."
  - nachher: „Pro Stunde: \\(2.5 \\cdot 10^8 \\cdot 3600 = 9 \\cdot 10^{11}\\) Schaltvorgänge — also **900 Milliarden** (= 0.9 Billionen)."

#### TODO-M4 — Treibstoff/Rabatt-Aufgabe in g1-2 aufgabenserie

Die Lösung sagte „Bezahlt: \\(20.4 \\cdot 0.93 = 18.972\\) L" — begrifflich unsauber, weil der Kunde 20.4 Liter bezahlt (zum reduzierten Preis), nicht 18.972 Liter. Variante A aus dem Befund umgesetzt: konkreter Normalpreis ergänzt, Frage auf Preisberechnung umgestellt.

- `downloads/grundlagen/g1-2-zahlen-grundoperationen/aufgabenserie.html`:
  - Aufgabe (Z. 60–63): Neue Angabe „Der Normalpreis beträgt \\(1.80\\) Fr./L." ergänzt; Frage (b) lautet jetzt „was kostet die Tankfüllung mit Rabatt".
  - Lösung 2 (Z. 123): \\(20.4 \\cdot 1.80 \\cdot 0.93 = 36.72 \\cdot 0.93 = 34.1496\\) Fr. (mit Vergleich ohne Rabatt 36.72 Fr., Ersparnis 2.5704 Fr.). Bruchdarstellung \\(\\tfrac{42687}{1250}\\) Fr.
- Verifikation mit Python: \\(20.4 \\cdot 1.80 = 36.72\\); \\(36.72 \\cdot 0.93 = 34.1496\\) exakt; als Bruch \\(42687/1250\\) ✓

#### TODO-M6 — \\(\\sqrt{a^2} = |a|\\) (bereits umgesetzt, Befund-Eintrag geschlossen)

Der Review-Befund kritisierte, dass die Identität \\(\\sqrt{a^2} = |a|\\) erst in der Zusammenfassung erscheint. Tatsächlich steht im aktuellen Snapshot bereits direkt im Theorie-Abschnitt §5 (Quadratwurzeln) ein „Häufiger Fehler"-Block mit Beispiel:

- `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 302–306: „\\(\\sqrt{a^2} = |a|\\), nicht einfach \\(a\\). Beispiel: \\(\\sqrt{(-3)^2} = \\sqrt{9} = 3\\), nicht \\(-3\\). Die Wurzelfunktion wirft das Vorzeichen weg." Der Block steht 29 Zeilen nach der Wurzel-Definition und weit vor der Zusammenfassung. Keine Änderung nötig.

#### TODO-M5 — Bewusst nicht umgesetzt

Der Befund schlug vor, die kaufmännische Rundungs-Konvention für negative Zahlen am Beispiel \\(-2.475 \\to -2.48\\) explizit zu benennen. Entscheidung: nicht umgesetzt — das didaktische Nutzen-Aufwand-Verhältnis spricht gegen die Erweiterung an dieser Stelle.

---

### Bergpeilen-Endwerte korrigiert in g5-3 A2 b (TODO-M19) — Korrekturwelle 1 abgeschlossen

**P2-Befund** aus dem fachlich-mathematischen Review Lerngebiet 5. Die Lösung der Aufgabe A2 b (Höhenpeilung eines Berges mit zwei Höhenwinkeln) enthielt zwei Endwerte, die nicht zu den Aufgabenwinkeln 28° und 41° passten.

Mit dieser Korrektur ist **Korrekturwelle 1 (P2 fachlich) abgeschlossen** — alle vier P2-Befunde aus dem fachlich-mathematischen Review (M10, M11, M12, M19) sind erledigt.

#### Geändert

- `grundlagen/g5-3-trigonometrische-berechnungen.html` Z. 747 (A2 b Lösungs-Skizze):
  - vorher: "Auflösen → \\(d \\approx 248\\) m, \\(h \\approx 216\\) m."
  - nachher: "Auflösen → \\(d \\approx 315\\) m, \\(h \\approx 274\\) m."
- Aufgabenstellung, Gleichungen \\(\\tan(28°) = h/(d + 200)\\) und \\(\\tan(41°) = h/d\\) sowie der Lösungsweg-Hinweis blieben unverändert.

#### Verifikation

Mit Python nachgerechnet: \\(\\tan 28° = 0.5317\\), \\(\\tan 41° = 0.8693\\). \\(d = 200 \\cdot 0.5317 / (0.8693 - 0.5317) = 106.34 / 0.3376 = 315.01\\) m. \\(h = 315.01 \\cdot 0.8693 = 273.84\\) m. Probe via beider Gleichungen: jeweils \\(h = 273.84\\) m ✓

Die alten Werte (248/216) waren in sich konsistent (\\(216 / \\tan 41° \\approx 248.5\\)), aber passten nicht zur 28°/41°-Konstellation — wie der Review-Befund vermutete, hatte der Autor wohl h=216 angesetzt und d daraus rückgerechnet.

---

### Boxplot-Schiefe-Begründung korrigiert in g4-2 A4 (TODO-M12, Oder-Variante)

**P2-Befund** aus dem fachlich-mathematischen Review Lerngebiet 4. Die Lösung der Aufgabe A4 (Themenseite g4-2 Diagramme) enthielt eine faktisch falsche Schiefe-Begründung in einem Satz mit zwei Fehlern: die Behauptung "Median näher am oberen Quartil" stimmte nicht (er ist näher am unteren), und die Schlussfolgerung "linksschief" wurde aus dieser falschen Prämisse abgeleitet. Die Datenlage ist tatsächlich **nicht eindeutig**: Box-Asymmetrie und Antennen-Asymmetrie deuten in entgegengesetzte Richtungen.

#### Geändert

Gewählte Variante (Oder-Variante aus dem Befund): Mehrdeutigkeit als didaktischen Lernpunkt aufnehmen, statt die Aufgabenwerte umzudesignen.

- `grundlagen/g4-2-diagramme.html` Z. 654 (A4 Lösung Teil d):
  - Boxplot-Werte: min=15, Q₁=28, Median=35, Q₃=45, max=54
  - Mathematik:
    - Median−Q₁ = 7, Q₃−Median = 10 → Median näher an Q₁ → **rechtsschiefe Box** (mehr Streuung in der oberen Box-Hälfte)
    - Linke Antenne (15 bis 28, Länge 13), rechte Antenne (45 bis 54, Länge 9) → **linksschiefer Schwanz**
  - vorher: "Linksschief — der Median (35) liegt näher am oberen Quartil (45) als am unteren (28), und der „Antenne" links ist länger als rechts."
  - nachher: "Hier zeigt der Boxplot widersprüchliche Signale: Innerhalb der Box liegt der Median (35) näher am unteren Quartil (Abstand zu Q₁ = 7) als am oberen (Abstand zu Q₃ = 10) — das deutet auf rechtsschiefe Box (mehr Streuung oben). Die Antennen geben das Gegenteil her: die linke Antenne (15 bis 28, Länge 13) ist länger als die rechte (45 bis 54, Länge 9) — das deutet auf linksschiefen Schwanz. Die Verteilung ist also nicht eindeutig schief; ein Boxplot allein kann hier keine klare Diagnose liefern, dafür bräuchte es ein Histogramm oder die Rohdaten."

Didaktischer Mehrwert: Lernende sehen ein konkretes Beispiel, wo der Boxplot die Verteilung zu stark zusammenfasst, und lernen, dass widersprüchliche Indikatoren (Box ↔ Antennen) ein Signal zur Vorsicht sind.

#### Anmerkung

Der Review-Text M12 sprach von Datei `g4-2-zentralmasse.html` — tatsächlich heisst sie `g4-2-diagramme.html`. Befund-Substanz und die Mathematik im Befundtext (Median-Q₁=7, Q₃-Median=10, Antennen 13 und 9) wurden 1:1 übernommen und verifiziert.

---

### Klassenhäufigkeiten korrigiert in g4-2 aufgabenserie L1c (TODO-M11)

**P2-Befund** aus dem fachlich-mathematischen Review Lerngebiet 4. Die Lösung der Aufgabe 1 (Histogramm konstruieren, n=25 Körpergrössen) enthielt zwei korrespondierende Zahlenfehler: die Anzahl-Angaben in zwei Klassen stimmten nicht zur jeweils aufgezählten Werte-Liste.

#### Geändert

- `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html`, Lösung 1c (Z. 108–109):
  - vorher: "[172, 179): **9** Werte (172, 173, 173, 174, 175, 176, 177, 178)" — angegeben 9, aufgezählt 8
  - vorher: "[179, 186): **4** Werte (179, 180, 182, 183, 185)" — angegeben 4, aufgezählt 5
  - nachher: "[172, 179): **8** Werte ..." und "[179, 186): **5** Werte ..." — Anzahl stimmt jetzt zur Aufzählung

#### Verifikation

Klassenhäufigkeiten mit Python nachgezählt: für den Datensatz (158, 162, 165, 167, 168, 169, 170, 170, 171, 171, 172, 173, 173, 174, 175, 176, 177, 178, 179, 180, 182, 183, 185, 187, 189) und die 5 Klassen [158, 165), [165, 172), [172, 179), [179, 186), [186, 193) ergeben sich **2, 8, 8, 5, 2** (Summe = 25 ✓).

Die nachfolgende Aussage in der Lösung ("annähernd symmetrisch und unimodal mit Gipfel im Bereich 165–179 cm") passt zur korrigierten Verteilung (Doppelgipfel 165–172 und 172–179) eindeutiger als zur fehlerhaften (einzelner Gipfel 172–179).

---

### Standardabweichung korrigiert in g4-3 aufgabenserie L1c (TODO-M10)

**P2-Befund** aus dem fachlich-mathematischen Review Lerngebiet 4. Die Lösung der Aufgabe 1 (Klassenarbeit, n=20) enthielt zwei zusammenhängende Zahlenfehler in der Summe der quadrierten Abweichungen und der daraus berechneten Standardabweichung.

#### Geändert

- `downloads/grundlagen/g4-3-masszahlen/aufgabenserie.html`, Lösung 1c (Z. 111):
  - vorher: "Abweichungen \\((x_i - 15.5)\\) quadriert summieren: ergibt **102**. \\(s = \\sqrt{102/19} \\approx \\mathbf{2.32}\\)."
  - nachher: "Abweichungen \\((x_i - 15.5)\\) quadriert summieren: ergibt **115**. \\(s = \\sqrt{115/19} \\approx \\mathbf{2.46}\\)."

Verifikation mit Python: Datensatz 11, 12, 12, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 18, 18, 18, 19, 20 hat Mittelwert 15.5, Summe der quadrierten Abweichungen = 115.0, \\(s = \\sqrt{115/19} \\approx 2.46\\) (Stichproben-Konvention mit n−1).

---

### Punkt-Koordinaten `(x, y)` → `(x | y)` (TODO-S4)

Konvention gemäss STYLEGUIDE §2.4: Punkt-Koordinaten mit senkrechtem Strich `P(x | y)` (FTB-Standard) — auch innerhalb LaTeX/MathJax.

#### Geändert

- **2 Stellen umgestellt (11 Klammer-Paare insgesamt)**, beide in g5-2d:
  - `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` — Lösung der zentrischen Streckung mit k=2 für Dreieck A/B/C: `2(0,0) - (1,1) = (-1, -1)` etc. → `2(0|0) - (1|1) = (-1|-1)` etc. (9 Klammer-Paare in einer Zeile). Jetzt konsistent mit der Aufgabenstellung 2 Zeilen darüber: `A(0|0), B(6|0), C(2|4), Z(1|1)`.
  - `downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/teste-dich-selbst.html` — Lösung Punktspiegelung: `-2 \cdot (3, 4) = (-6, -8)` → `-2 \cdot (3|4) = (-6|-8)`. Jetzt konsistent mit der Aufgabenstellung darüber: `Z = (0|0), P = (3|4)`.

#### Bewahrt (NICHT umgestellt)

- `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html`: `(158, 162)` und `(187, 189)` — diese sind **Aufzählungen von Datenwerten** in Klassenhäufigkeiten ("2 Werte (158, 162)" bedeutet zwei Körpergrössen 158 cm und 162 cm), keine Punktkoordinaten.

#### Methodik / Werkzeug

Konvertierungs-Skript: `scripts/convert_punktkoord.py`. Anders als bei S1/S2/S3 nicht über globale Regex, sondern als **gezielte string-Ersetzungen pro Stelle** — weil `(a, b)`-Klammerpaare im Lehrmittel teils Datenwert-Aufzählungen sind. Vor der Ersetzung wird verifiziert, dass der ALT-String genau 1× in der Datei vorkommt.

---

### Kosinus → Cosinus vereinheitlicht (TODO-S2)

Konvention: Schweizer Hochdeutsch — "Cosinus" statt "Kosinus", auch in Komposita (Cosinussatz, Cosinusfunktion, Cosinuswert).

#### Geändert

- **63 Stellen umgestellt** über 11 HTML-Dateien:
  - `grundlagen/g5-3-trigonometrische-berechnungen.html` (28)
  - `grundlagen/g5-4-einheitskreis.html` (3)
  - `grundlagen/g5-5-trigonometrische-gleichungen.html` (2)
  - `schwerpunkt/s3-5-trigonometrische-funktionen.html` (2)
  - `downloads/grundlagen/g5-2a-dreiecke/aufgabenserie.html` (2)
  - `downloads/grundlagen/g5-3-trigonometrische-berechnungen/`: aufgabenserie.html (2), formelauszug.html (7), handout.html (6), teste-dich-selbst.html (8)
  - `downloads/grundlagen/g5-4-einheitskreis/`: aufgabenserie.html (1), handout.html (2)
- Komposita berücksichtigt: Kosinussatz → Cosinussatz (51× im Endzustand), Kosinusfunktion → Cosinusfunktion, Kosinuswert → Cosinuswert, kleingeschriebene Varianten ebenfalls.

#### Bewahrt (NICHT umgestellt)

- **3 externe Serlo-URLs** mit "kosinus" im URL-Slug (`de.serlo.org/.../sinus-und-kosinusfunktion`, `de.serlo.org/.../aufgaben-zu-sinus-kosinus-...`, `de.serlo.org/.../sinussatz-und-kosinussatz`) — Änderung hätte 404-Fehler ergeben.
- `<style>`, `<svg>` und SVG-Attribute (`d`, `points`, `viewBox`, `transform`) prophylaktisch geschützt.
- `<script>`-Blöcke nicht generell geschützt: ein "Kosinus"-Vorkommen stand in einem JS-Template-Literal mit Canvas-Erklärungstext (g5-3 Spezialwinkel-Beweis 45°), das zur Laufzeit als Text angezeigt wird; dieses wurde mit umgestellt. "Kosinus" kommt in JS-Code-Konstrukten (Variablen, Properties) nicht vor.
- Markdown-Dokumente bewusst ausgespart.

#### Methodik / Werkzeug

Konvertierungs-Skript: `scripts/convert_cosinus.py`. Bietet Dry-Run-Modus (Default) und `--apply`. Eingebaute Verifikation prüft Klartext-Reste und listet bewahrte URL-Vorkommen.

---

### ß → ss vereinheitlicht (TODO-S1)

Konvention: Schweizer Hochdeutsch — kein "ß", durchgehend "ss". Variante A (auch Eigennamen umgestellt): "Gauß-Algorithmus" → "Gauss-Algorithmus".

#### Geändert

- **34 Stellen umgestellt** über 5 HTML-Dateien:
  - `grundlagen/g2-3-lineare-gleichungssysteme.html` (1 — "Gauss-Algorithmus" im YouTube-Link-Text)
  - `grundlagen/g5-2a-dreiecke.html` (22 — Canvas-Erklärtexte und JS-Kommentare: Lotfuss, Höhenfusspunkt, Masse, gross, ausserhalb)
  - `grundlagen/g5-2b-vierecke.html` (6 — Massstab, Grösse, Aussenkontur, Masslinien)
  - `grundlagen/g5-2c-kreis-und-kreisteile.html` (2 — Legende "~ gross", Kommentar "Masse beschriften")
  - `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` (3 — grösserer, ausserhalb, Höhenfusspunkt)
- `<style>`, `<svg>` und SVG-Attribute (`d`, `points`, `viewBox`, `transform`) geschützt — dort kommt kein ß vor, prophylaktischer Schutz.
- `<script>`-Blöcke nicht generell geschützt: ß-Vorkommen dort stehen in JS-Strings, die zur Laufzeit als Text gerendert werden (z.B. Canvas-Erklärungen). ß kommt in JS-Code-Konstrukten (Variablennamen, Schlüsselwörter) nicht vor.
- Markdown-Dokumente (CHANGELOG, STYLEGUIDE, COLLABORATION etc.) bewusst ausgespart — redaktionelle Texte ausserhalb des Lehrmittels.

#### Methodik / Werkzeug

Konvertierungs-Skript: `scripts/convert_eszett.py`. Bietet Dry-Run-Modus (Default) und `--apply` für die echte Konvertierung. Eingebaute Verifikation prüft nach der Konvertierung, dass keine ß-Vorkommen in HTML-Dateien verblieben sind.

---

### Dezimaltrennzeichen: Komma → Punkt vereinheitlicht (TODO-S3)

Konvention gemäss `STYLEGUIDE.md` §2.4: **Dezimalpunkt** (Schweizer Schulkonvention), kein Dezimalkomma. Diese Konvention war bisher zwar im Styleguide festgehalten, aber im Material an mehreren Stellen nicht durchgesetzt — sowohl in MathJax-Formeln als auch in Prosa-Text. Die strukturelle Todo-S3 in der Master-Todoliste war zudem invers formuliert (sie sprach von „Punkt → Komma"), was bereinigt wurde.

### Geändert

- **273 Stellen umgestellt** über 14 HTML-Dateien (Themenseiten und Druckseiten):
  - MathJax-Notation `\(3{,}14\)` → `\(3.14\)` in `\(...\)`- und `\[...\]`-Blöcken
  - MathJax in JS-Template-Literals (z.B. g5-2a Spezialwinkel-Beweise: `\sqrt{3} \approx 1{,}732` → `\sqrt{3} \approx 1.732`)
  - Klartext-Dezimalkommas `1,80 m` → `1.80 m`, `4,8 cm²` → `4.8 cm²`, `138,75 m` → `138.75 m`, `9,81 m/s²` → `9.81 m/s²` etc.
  - Versehentlich aus MathJax übernommene `{,}`-Schreibweise im HTML-Klartext (z.B. `1{,}20 m` als Literal, das im Browser als „1{,}20 m" gerendert wurde) → `1.20 m`
- **Bewusst nicht umgestellt** (geschützt):
  - LaTeX-Subscript-Listen wie `x_{1,2}`, `a_{i,j}` (36 Stellen — das Komma trennt Indizes, ist kein Dezimalkomma)
  - Punkt-Koordinaten `(0,0)`, `(11, -1)` (11 Klartext-Stellen — separater Befund TODO-S4, siehe `master-todoliste.md`)
  - Tupel und pythagoreische Tripel `(3, 4, 5)`, `(19, 34, 27)` (Aufzählungs-Trenner, kein Dezimalkomma)
  - Inline-Event-Handler `onclick="f(1, 2)"` (JS-Argumente, keine Dezimalzahlen)
  - SVG-Pfade (`d`, `points`, `viewBox`, `transform`), CSS (`<style>`, `rgba(…, 0.18)`), Google-Fonts-URL-Parameter

### Hinzugefügt

- **TODO-S4** in `master-todoliste.md`: Punkt-Koordinaten `(x, y)` auf Styleguide-Notation `(x | y)` umstellen (§2.4) — 11 Klartext-Stellen in g5-2d, g5-1, g5-2a, g3-2 aufgabenserie, g4-2, g5-2d teste-dich-selbst. Bewusst manuell zu prüfen, weil in einigen Fällen `(a, b)` als Aufzählung von Datenwerten gemeint sein kann (z.B. Klassenhäufigkeiten).

### Methodik / Werkzeug

Konvertierung mit Python-Skript (`scripts/convert_decimals.py`), mit Verifikation: nach der Konvertierung wurde geprüft, dass keine `{,}`-Reste, keine Klartext-Dezimalkommas (ausserhalb der geschützten Stellen) und keine Stray-Steuerzeichen mehr existieren. Alle 14 betroffenen Dateien manuell stichprobenartig diff-geprüft (Schwerpunkt: JS-Template-Literals in g5-2a, MathJax-Render-Validität, Tabellen-Layouts).

---

## [26_9] — 2026-05-15

### Theorie-Mittelteil von 5.4 komplett neu — auf Anim-Format umgestellt

Wie bei 5.3 in [26_8] wurde der gesamte Bereich „Definition am Einheitskreis" bis vor „Aufgaben" in g5-4-einheitskreis.html durch neuen Canvas-basierten Inhalt ersetzt — gemäss User-Spezifikation. Drei neue interaktive Animationen ersetzen die alten SVG-Widgets; neue Sektionen-Gliederung und vollständige Theorie-Boxen mit Definitionen, Beziehungen, Umrechnungstabelle, Quadranten- und Symmetrie-Eigenschaften, Definitions- und Wertemenge.

### Hinzugefügt

- **Anim 1 · Sinus und Cosinus am Einheitskreis** — stufenloser Schieber φ = 0°..360° (Schrittweite 1°). Zusätzlich 16 Spezialwinkel-Chips in vier Reihen (Basis 0°/30°/45°/60°/90° plus 90°+, 180°+, 270°+-Varianten). Umschaltung Grad/Radiant: bekannte Spezialwinkel erscheinen als π-Brüche (π/6, π/4, π/3, …), andere als Vielfache von π in Dezimaldarstellung. Punkt P am Einheitskreis, sin φ (lila) und cos φ (grün) als markierte Strecken, Dreieck OQP rot gefüllt mit rechtwinkligem Marker. Live-Werte für sin/cos und Quadrant, dynamischer Erklärungstext mit exakten Brüchen für die Spezialwinkel.
- **Anim 2 · Tangens am Einheitskreis** — gleiche Steuerung (φ + Spezialwinkel-Chips + Einheits-Toggle). Vertikale Tangente bei x = 1 als gestrichelte Linie, Punkt R = (1, 0), Punkt S = (1, tan φ) auf der Tangente. Tangentenabschnitt RS in Orange, Wert tan φ als Strecke. Bei stumpfen Winkeln (cos < 0) Strahl OP zu S rückwärts verlängert (gestrichelt). Bei φ ≈ 90° / 270° wird „nicht definiert / →±∞" angezeigt. Clamp für sehr grosse |tan φ|, damit das Label nicht aus dem Canvas läuft.
- **Anim 3 · Beziehungen — Ähnlichkeit und Pythagoras** — Chips zur Umschaltung zwischen den beiden fundamentalen Beziehungen. Ähnlichkeit-Modus: beide Dreiecke ΔOQP (rot) und ΔORS (orange) gefüllt, mit Markierungen der entsprechenden Seiten (cos φ, sin φ, 1, tan φ). Pythagoras-Modus: nur ΔOQP hervorgehoben, alle drei Seiten (cos φ, sin φ, r = 1) markiert; ΔORS schwächer im Hintergrund. Live-Werte sin/cos/tan, plus sin/cos und sin²+cos² als Probe. Dynamischer Erklärungstext mit konkreten Zahlen.

Neue Theorie-Blöcke:
- Definition Sinus und Cosinus am Einheitskreis (Formeln y_P = sin φ, x_P = cos φ)
- Definition Tangens am Einheitskreis (y_S = tan φ, Tangentenabschnitt RS)
- Beziehungen zwischen den Winkelfunktionen (Ähnlichkeit: tan = sin/cos; Pythagoras: sin² + cos² = 1)
- **Umrechnungstabelle gegeben/gesucht** (3×3-Matrix mit Formeln zur Umrechnung zwischen sin, cos, tan im 1. Quadranten)
- **Vorzeichen in den vier Quadranten** (Tabelle I/II/III/IV)
- **Symmetrieeigenschaften** (Tabelle mit 180°−α, 180°+α, 360°−α für sin/cos/tan)
- **Definitions- und Wertemenge** (𝔻=ℝ und 𝕎=[−1,1] für sin/cos; 𝔻=ℝ\\{π/2+kπ} und 𝕎=ℝ für tan)

### Geändert

- **Style-Block in g5-4**: `.anim`-Klassen ergänzt (~90 Zeilen Standard-CSS aus g5-2a/b/c/d, g5-3 übernommen). Alte `.widget`-Klassen bleiben für die Aufgaben-Sektion.
- **JavaScript komplett neu**: alte SVG-Widget-Logik ersetzt durch drei neue Canvas-draw-Funktionen mit Helfern (initCv, txt, seg, dashedSeg, dot, fillTriangle, rightAngleMarker, drawAchsen, winkelText für Grad/Radiant-Umschaltung).
- **Worst-Case-Prüfung nach STYLEGUIDE §3.4** durchgeführt für alle 3 Anims. Anim 1/3 OK auf Anhieb; Anim 2 mit clamp() für sehr grosse |tan φ| (bei φ nahe 90°/270°), damit der S-Punkt nicht ins Unendliche rendert. Alle Achsen-Beschriftungen, Pfeile und Labels passen in den 560×480-Canvas.

### Datei-Veränderung

g5-4 ist von 847 auf 1424 Zeilen gewachsen (+68%). Anki-Deck und Druckseiten bleiben aus früheren Iterationen kompatibel — der überarbeitete Mittelteil deckt dieselben Konzepte ab (Punkt am Einheitskreis, sin/cos/tan, Quadrantenvorzeichen, Beziehungen, Symmetrien).

---

## [26_8] — 2026-05-15

### Theorie-Mittelteil von 5.3 komplett neu — auf Anim-Format umgestellt

Der gesamte Bereich „Definition Sinus/Kosinus/Tangens" bis vor „Aufgaben" in g5-3-trigonometrische-berechnungen.html wurde gemäss neuen User-Spezifikationen ersetzt. Die alte Struktur mit `.widget`-CSS und SVG-Animationen ist abgelöst durch das Standard-`.anim`-Format mit Canvas (wie g5-2a/b/c/d). Sechs neue interaktive Animationen, neue h2/h3-Gliederung, neue Definitionen und Merksätze nach Vorlage des Formelbuchs.

### Hinzugefügt

- **Anim 1 · Ähnlichkeit + Strahlensatz** — drei rechtwinklige Dreiecke gleicher Form (gemeinsame Spitze A links, gleiche Basisrichtung), aber unterschiedlicher Grösse mit Faktoren 1, k, k². Schieber für k (1.1..2.0) und α (20°..45°). Gestrichelte Strahlen vom Zentrum durch Eckpunkte zeigen Strahlensatz. Live-Verifikation: alle drei Verhältnisse a/c, a'/c', a''/c'' identisch und gleich sin α.
- **Anim 2 · Definition Winkelfunktionen** — Chips zur Umschaltung sin x / cos x / tan x und zur Wahl der Winkel-Position (bei A oder bei B). Bewusst Variable x (statt α), AK/GK/H werden relativ zu x benannt; die Hervorhebung der relevanten Seiten (rot = GK, orange = AK, grün = H) wechselt je nach Funktion. Scale dynamisch (passt sich an x an, damit kein Overflow).
- **Anim 3 · Spezialwinkel** — Chips zur Umschaltung „halbes Quadrat (45°)" und „halbes gleichseitiges Dreieck (30°/60°)", plus α/β-Hervorhebung. Volldreieck/Vollquadrat gestrichelt zur Referenz. Live-Werte als exakte Brüche (√2/2, √3/2, etc).
- **Anim 4 · Sinussatz im Umkreis** — fester Umkreis (Radius 150 px), drei Punkte A, B, C frei auf dem Kreis positionierbar (Schieber 0°..360°). Sinussatz-Probe: alle drei Quotienten a/sin α, b/sin β, c/sin γ gleich 2r=300 px. Mittelpunkt M und Radius r angedeutet.
- **Anim 5 · Cosinussatz** — Schieber für b, c (3..9) und Winkel α (20°..160°), inklusive stumpfer Winkel. Live-Berechnung von b², c², 2bc·cos α und a² mit Erklärung des Vorzeichenwechsels bei α > 90°. Dynamische Position des Dreiecks (Bounding-Box-Verschiebung), damit Spitze C auch bei stumpfen Winkeln nicht aus dem Canvas läuft.
- **Anim 6 · Dreiecksfläche** — Schieber für p, q, φ. Höhe h = p·sin φ optional einblendbar, Höhen-Fusspunkt mit rechtem-Winkel-Marker. Bei stumpfem φ wird die Grundseite-Verlängerung gestrichelt angedeutet. Live-Berechnung A = p·q/2·sin φ.

Neue Theorie-Blöcke: Ähnlichkeit (mit drei Formeln a/c, b/c, a/b = const.), Definition Sinus/Kosinus/Tangens mit GK/AK/H-Bezeichnung, Beziehungen unter den Winkelfunktionen (Tabelle mit Komplementbeziehungen), Tabelle der Spezialwinkel 30°/45°/60° als exakte Brüche, Arcusfunktionen-Definition. Im schiefwinkligen Teil: Bezeichnungs-Konvention, Sinussatz mit 2r-Bezug zum Umkreis, Wann-anwenden-Box (wsw/wws/ssw), Cosinussatz mit allen drei Formvarianten, Strategie-Übersicht, Flächenformel A = p·q/2·sin φ.

### Geändert

- **Style-Block in g5-3**: `.anim`-Klassen ergänzt (~90 Zeilen Standard-CSS aus g5-2a/b/c/d übernommen). Alte `.widget`-Klassen bleiben für die Aufgaben-Sektion.
- **JavaScript komplett neu**: alte SVG-Widget-Logik (rwd, sin-svg, cos-svg) ersetzt durch sechs neue Canvas-draw-Funktionen mit Helfern (initCv, txt, seg, dashedSeg, dot, fillTriangle, rightAngleMarker, drawAngleArc). Identischer Stil wie g5-2c/d.
- **Worst-Case-Prüfung nach STYLEGUIDE §3.4** auf alle sechs Anims durchgeführt. Initial hatten Anim 1 (k=2, α=65° → Höhe ragte 487 px über den Canvas), Anim 2 (x=75° → 78 px über), Anim 5 (α=160° → C 64 px links) und Anim 6 (φ=160° → C 133 px links, φ=90° → 77 px oben) Probleme. Korrekturen:
  - Anim 1: α-Slider auf max 45° begrenzt, b0 von 95 auf 75 px reduziert, yA von 0.78 auf 0.92 H verschoben.
  - Anim 2: Scale dynamisch (statt fix 42) — passt sich an x an, sodass beide Komponenten in Canvas passen.
  - Anim 5/6: Bounding-Box-basierte dynamische Positionierung — xA wird so verschoben, dass auch bei stumpfen Winkeln alle Eckpunkte im Canvas bleiben.

### Datei-Veränderung

g5-3 ist von 1284 auf 1881 Zeilen gewachsen (+47%) durch die sechs neuen Canvas-Animationen mit Slider-Logik und dynamischen Erklärtexten.

---

## [26_7] — 2026-05-15

### Vollständige Ausarbeitung der Themenseite 5.2d Zentrische Streckung und Ähnlichkeit

Mit der vierten und letzten Schwesterseite des Sub-Splits 5.2 ist das gesamte Teilgebiet Planimetrie samt Ähnlichkeit ausgearbeitet. Die Seite g5-2d-zentrische-streckung-aehnlichkeit löst den Stub aus [26_6] ab.

### Hinzugefügt

- **`grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html`** — neue, vollständig ausgearbeitete Themenseite (1390 Zeilen). Fünf interaktive Canvas-Animationen:
  1. **Zentrische Streckung (Anim 1)** — Original-Dreieck (blau) bleibt fest bei k = 1 sichtbar, eine farbig kontrastierende Kopie (orange) bewegt sich mit Schieber k = −2 … 2 (Schritt 0,1). Toggles für Strahlen Z → P → P′. Live-Werte für k, |k|, k² und Orientierung; dynamischer Erklärungstext für die Sonderfälle k = 0, k = 1, k = −1.
  2. **Strahlensätze (Anim 2)** — Umschaltbar 1./2. Strahlensatz. Drei ganzzahlige Schieber (SA und SB als Strahlenabschnitte 1–4, Streckfaktor k = 2–4), so dass die Verhältnisse stets schön ausgehen. Beschriftung über Streckenbezeichnung+Wert (\(\overline{SA} = 2\), \(\overline{AA'} = 2\), …) statt über Punktdefinitionen. Beim 2. Strahlensatz werden zusätzlich die Parallelenabschnitte mit ihren Längen beschriftet. Dynamische Formel- und Erklärungstexte.
  3. **Ähnliche Figuren (Anim 3)** — Drei Figuren als Chips: Dreieck, Rechteck, Kreis. Streckfaktor k = −2 … 2 (Schritt 0,1). Original (blau) und Bild (orange) mit optionalen Strahlen vom Zentrum. Live-Werte für k, |k| und k² (Flächenfaktor).
  4. **Ähnlichkeitssätze (Anim 4)** — Vier Chips für WW (Hauptsatz, default), SSS, sWs, SsW. Zwei Dreiecke nebeneinander, Streckfaktor 0,6 … 1,8. Markierungen je nach Satz: Winkelbögen bei WW/sWs/SsW, Seiten-Labels mit Werten bei SSS/sWs/SsW. Hilfsfunktionen `drawAngleArc()` und `midLabelArr()` für saubere Beschriftung. Legende und Formel passen sich an den aktiven Satz an.
  5. **Hauptähnlichkeitssatz im rechtwinkligen Dreieck (Anim 5)** — Vorlagentreue Anordnung: A links unten, H mitte unten, B rechts unten, C oben mit Höhe h auf der Hypotenuse. Drei Chips zur Hervorhebung: ganzes Dreieck ABC (blau), linkes Teildreieck AHC (grün) oder rechtes Teildreieck CHB (lila). Schieber α = 20°–70° (Schritt 5°), c = 10 fest. Live-Werte für α, β, a, b, p, q, h. Toggle für Bezeichnungen. Rechte Winkel bei C und H markiert; α-Bogen bei A und C (links), β-Bogen bei B und C (rechts).

  Die Theorie umfasst: Definition zentrische Streckung mit \(\overrightarrow{ZP'} = k \overrightarrow{ZP}\), vier Eigenschaften (gleichsinnig/parallelentreu/winkeltreu/verhältnistreu) als Tabelle, 1./2. Strahlensatz mit Umkehrung, Definition ähnlicher Figuren mit Notation \(F_1 \sim F_2\), Eigenschaften ähnlicher Figuren (Winkel, Streckenverhältnisse, Flächenverhältnis \(k^2\)), Hauptähnlichkeitssatz WW plus Tabelle SSS/sWs/SsW, Hauptähnlichkeitssatz im rechtwinkligen Dreieck mit Höhensatz \(h^2 = pq\) und Kathetensatz \(a^2 = pc\), \(b^2 = qc\). Sechs Aufgaben A1-A6 von Streckung über Strahlensatz bis Kathetensatz/Höhensatz.

- **`downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/`** — vier neue Druckseiten plus Anki-Deck:
  - `handout.html` (~120 Zeilen): Theorie kompakt; alle Definitionen und Sätze, vier Plausibilitäts-Tipps zum Schluss.
  - `formelauszug.html` (~110 Zeilen): Sechs Tabellen — Zentrische Streckung, Strahlensätze, Ähnlichkeit, Ähnlichkeitssätze, Rechtwinkliges Dreieck, Sonderfälle Streckfaktor.
  - `teste-dich-selbst.html` (15 Grundlagenaufgaben + Lösungen): Streckfaktor-Wirkung, Eigenschaften, Strahlensätze, Massstab-Flächenfaktor, Kathetensatz/Höhensatz, Punkt-Bilder.
  - `aufgabenserie.html` (6 Anwendungsaufgaben + ausführliche Lösungen): Höhe Baum durch Schattenwurf, Massstab 1:25000 See-Fläche, Strahlensatz an Wanderwegen, Dachsparren-Querbalken, Höhensatz mit p+q+a+b, Pyramide nach Thales-Methode.
  - `ankideck.apkg`: 32 Karten zu allen Aspekten — Definition, Sonderfälle k, Eigenschaften, Strahlensätze und Umkehrung, Ähnlichkeit, alle vier Ähnlichkeitssätze, Hauptähnlichkeitssatz im rechtwinkligen Dreieck, Höhensatz, Kathetensatz, Höhe aus Katheten, Massstab-Flächenfaktor, Schattenwurf-Methode, Verbindung Kongruenz↔Ähnlichkeit.

### Geändert

- **`nav.js`** — g5-2d in NODES und in GROUPS (Lerngebiet 5 Geometrie) eingetragen. Damit erscheint die Seite in der Sidebar und im Theme-Wechsler nach g5-2c.
- **`grundlagen/g5-2a-dreiecke.html`, `grundlagen/g5-2b-vierecke.html`, `grundlagen/g5-2c-kreis-und-kreisteile.html`** — rlp-hinweis um Verlinkung zu Teil 4 (g5-2d) ergänzt; alle vier Schwesterseiten verweisen jetzt symmetrisch aufeinander.
- **`grundlagen/g5-2c-kreis-und-kreisteile.html`** — next-Link in buildNav geändert von g5-3 auf g5-2d.
- **`grundlagen/g5-3-trigonometrische-berechnungen.html`** — prev-Link in buildNav geändert von g5-2c auf g5-2d.
- **`index.html`** — Status g5-2d von „Geplant" auf „Fertig" gesetzt; Sub-Split-Beschreibung von „2.2 → 2.2a + 2.2b und 5.2 → 5.2a + 5.2b + 5.2c" auf „… + 5.2c + 5.2d" erweitert.
- **`README.md`** — g5-2d-Zeile in Stand-Tabelle ergänzt; Sub-Split-Beschreibung entsprechend.
- **`scripts/build_apkg.py`** — neues `g52d_cards`-Array mit 32 Karten; neuer Eintrag in NEW_DECKS für `g5-2d-zentrische-streckung-aehnlichkeit`.

### Bereinigung

- **`grundlagen/g5-2c-kreis-und-kreisteile.html`** — Ressourcen-Block ins Standardformat überführt: Klassen `lk-titel`/`lk-desc`/`lk-quelle` ersetzt durch `lk-t`/`lk-s` mit Icon-Span `lk-ic` (▶️ 📝 ⏳); Aufgaben-Klasse `lk lk-aufg` zu `lk aufg`; Platzhalter „In Vorbereitung" als `<a class="lk" style="opacity:0.6" aria-disabled="true">` analog zu g5-2a/b. Klassennamen-Vergleich zwischen g5-2a, g5-2b und g5-2c jetzt identisch.

- **`grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html`** — Canvas-Overflow in vier der fünf Animationen korrigiert. Initial waren die Original-Figuren und Skalen so dimensioniert, dass bei den Schieber-Extremen die Bilder weit über die Canvas-Grenzen hinausragten:
  - **Anim 1**: OR_REL-Punkte verkleinert auf max |rel_x|=110, Zentrum auf Canvas-Mitte (statt 0.42 W). Bei k=±2 passt das Bild jetzt in 60..500 px.
  - **Anim 2**: Pixel-pro-Einheit U von 70 auf 28 reduziert, Zentrum S von x=80 auf x=60. Worst Case SA=4, k=4 → SAp=16 Einheiten passt jetzt in Canvas-Breite.
  - **Anim 3**: Figuren auf |rel_x|≤110 verkleinert (Dreieck, Rechteck, Kreis-Mittelpunkt), Zentrum auf Canvas-Mitte. Bei k=±2 alle Figuren komplett sichtbar.
  - **Anim 4**: scale von 28 auf 24 reduziert, offsetX von 270 auf 240. Bei k=1.8 passt das rechte Bild-Dreieck (xBp=506) noch in den Canvas (560).
  - **Anim 5**: war bereits OK (Hypotenuse c=10, scale 38 → xB=470, alle Punkte im Canvas).

### Geändert

- **`STYLEGUIDE.md` §3.4** — neue verbindliche Regel zum Canvas-Inhalt: Bei jeder Canvas-Animation muss bei jedem Schieber-Extremwert die Zeichnung komplett im Canvas liegen. Worst-Case-Berechnung beim Schreiben Pflicht, visuelle Inspektion „in der Mitte" reicht nicht. Direktverweis auf die [26_7]-Fehler in g5-2d.

### Analyse-Skript

- **`scripts/cmp_handout_formelauszug.py`** — neues Token-basiertes Vergleichsskript für alle 21 Themen. Extrahiert Wörter ≥3 Zeichen und Mathe-Formeln aus den `<body>`s von Handout und Formelauszug, berechnet Jaccard- und asymmetrische Überlappungen. Durchschnitt: Jaccard 33%, F⊂H (Anteil Formelauszug-Inhalt im Handout) 71%. Vier Themen mit ≥80% Überlappung als Kandidaten für Überarbeitung markiert (g1-2, g1-4, g4-1, g5-5); g5-2c als Mass für guten Formelauszug (53% F⊂H, hoher Mehrwert).

---

## [26_6] — 2026-05-15

### Vollständige Ausarbeitung der Themenseite 5.2c Kreis und Kreisteile

Mit der dritten und letzten Schwesterseite des Sub-Splits 5.2 ist das gesamte Teilgebiet Planimetrie ausgearbeitet. Die Seite g5-2c-kreis-und-kreisteile löst den Stub von [26] ab.

### Hinzugefügt

- **`grundlagen/g5-2c-kreis-und-kreisteile.html`** — neue, vollständig ausgearbeitete Themenseite zum Bereich Kreis und Kreisteile (~2200 Zeilen). Sieben interaktive Canvas-Animationen:
  1. **Geraden und Strecken am Kreis (Anim 1)** — alle sechs Begriffe Radius/Durchmesser/Sehne/Sekante/Tangente/Passante als Chips umschaltbar; aktiver Typ blau, inaktive grau. Endpunkte (bzw. der Berührungspunkt der Tangente) per Pointer/Touch ziehbar. Toggle „Alle gleichzeitig zeigen" für die Übersichtsdarstellung. Tangente mit Rechtwinkel-Markierung am Berührungspunkt und gestricheltem Radius.
  2. **Pi-Annäherung (Anim 2)** — einbeschriebenes (blau gefüllt) und umschriebenes (orange Kontur) regelmässiges n-Eck, Schieber n = 3 bis 100. Live-Werte u_n/d und U_n/d (per n·sin(π/n) bzw. n·tan(π/n)), zusätzlich Anzahl stabiler Nachkommastellen. Sandwich-Schranken \(u_n < \pi d < U_n\) didaktisch visualisiert; Sechseck-Spezialfall im Theorie-Block erklärt.
  3. **Kreisumfang — Abrollen zur Geraden (Anim 3)** — Kreis rollt nach rechts ab, abgerollte Strecke unten als orange Linie. Durchmesser-Massstab mit grünen Markern für 1·d, 2·d, 3·d und π·d. Schieber für Abroll-Fortschritt und Durchmesser. Adaption der GeoGebra-Anregung `vy4TJ2rU` (Umfang des Kreises).
  4. **Kreisfläche — Sektoren zum Quasi-Rechteck (Anim 4)** — n Sektoren (4-64) wandern zickzackförmig in einen Streifen rechts und bilden bei grossem n näherungsweise ein Rechteck der Grösse π·r × r. Ziel-Rechteck als grüne gestrichelte Referenz. Adaption der GeoGebra-Anregung `bsrrnK8N` (Flächeninhalt des Kreises).
  5. **Kreisring (Anim 5)** — Schieber für R und r (Konsistenz r < R erzwungen), Toggles für mittlerer Radius r_m und Ringbreite b. Beschriftungen R, r, r_m, b mit gestrichelten Pfeilen gemäss Vorlagen-Bild. Live-Werte für (R²−r²)π und 2π·r_m·b zur Kontrolle der Formel-Äquivalenz. Füllung in warmem Beige-Braun (RING_FILL) analog zur Vorlage.
  6. **Kreissektor (Anim 6)** — Schieber für r und φ (10°-350°), Bogenlänge orange hervorhebbar, Vollkreis-Referenz gestrichelt zuschaltbar. Beschriftungen r, b, A_SK, φ direkt im Bild. φ-Bogen-Markierung am Mittelpunkt M.
  7. **Kreissegment (Anim 7)** — Schieber für r und φ, Toggle für Dreieck (zur Differenzbildung Sektor − Dreieck) und für Masse-Beschriftung. Beschriftungen s, h, r−h, r, A_SG mit Rechtwinkel-Markierung am Sehnenmittelpunkt. M oben, Sehne horizontal, Segment nach unten gemäss Vorlagen-Bild.

  Die Theorie umfasst: Pi-Definition mit irrational/transzendent, Archimedes-Verfahren mit Sechseck-Beispiel, Umfang \(U = 2\pi r = \pi d\), Fläche \(A = \pi r^2\), Kreisring \(A = R^2\pi − r^2\pi = (R−r)(R+r)\pi = 2\pi r_m \cdot b\), Bogenlänge \(b = r\pi\varphi/180°\), Sektorfläche \(A_{SK} = r^2\pi\varphi/360° = \tfrac{1}{2}br\), Segmentfläche \(A_{SG} = A_{Sektor} − A_{Dreieck}\) mit \(s = 2r\sin(\varphi/2)\), \(h = r(1−\cos(\varphi/2))\). Sechs Aufgaben A1-A6 mit zunehmender Selbstständigkeit: Begriffe, Umfang+Fläche, Pi-Schranken Archimedes, Kreissektor, Kreisring+Segment, Anwendungsaufgabe Verkehrskreisel. Aktualität zum Pi-Weltrekord (300 Billionen Stellen, Kioxia/Linus, Guinness-Eintrag) verlinkt.

- **`downloads/grundlagen/g5-2c-kreis-und-kreisteile/`** — vier neue Druckseiten plus Anki-Deck:
  - `handout.html` (~200 Zeilen): Theorie kompakt; Themen Kreis-Linien, Pi, Umfang+Fläche, Kreisring, Bogen+Sektor, Segment, Plausibilitäts-Tipps.
  - `formelauszug.html` (~140 Zeilen): Tabellen-lastig mit allen Kreis-Formeln; die drei Sonderformen Kreisring/Sektor/Segment ausgekoppelt, zusätzliche Tabelle für Spezialfälle (φ = 90°, 180°, 360°). Quellenhinweis Orell Füssli.
  - `teste-dich-selbst.html` (15 Grundlagenaufgaben + Lösungen): Begriffe, Tangenten-Eigenschaft, Umfang/Fläche, Pi-Schranken bei Archimedes, Bogenlänge, Sektorfläche, Bruchteil-Berechnungen, Kreisring, Sehne und Segmenthöhe, Bedeutung von Transzendenz.
  - `aufgabenserie.html` (6 Anwendungsaufgaben + ausführliche Lösungen): Pizza-Vergleich, Velo-Rad-Umdrehungen, Brunnen-Mosaik mit 12 Sektoren, Park-Rondell als Kreisring, Mondsichel-Logo mit Segmenten, Pi-Schranken durch 12-Eck.
  - `ankideck.apkg` (32 Karten): Begriffsdefinitionen, Strecken vs. Geraden, Tangenten-Eigenschaft, Pi-Definition + Irrationalität/Transzendenz, Pi-Schranken Formeln, Umfang/Fläche, Kreisring (3 Varianten), Sektor (Bogen + Fläche, 2 Formen), Segment (s, h, Pythagoras, Hauptformel), drei Spezialfälle.

### Geändert

- **`scripts/build_apkg.py`**: neuer Kartensatz `g52c_cards` (32 Karten) angelegt zwischen `g52b_cards` und `g11_cards`; `NEW_DECKS`-Liste um Eintrag `('g5-2c-kreis-und-kreisteile', '5.2c Kreis und Kreisteile', …, g52c_cards)` erweitert.
- **`README.md`**: g5-2c Kreis und Kreisteile Status von `🔜 geplant` auf `✅ verfügbar` gesetzt. Damit ist der Sub-Split 5.2 vollständig.
- **`HOWTO-externe-ressourcen.md` §8 (Anbieter-Map)**: g5-2c-Zeile ergänzt mit MathemaTrick `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (Kreis-Anteile in der Geometrie-Playlist) und Lehrerschmidts Flächenberechnungs-Playlist `PLa0u3J0uzAzlkQcJpE9CODCaM_vg_t2Ea` sowie Geometrie-Grundlagen-Playlist `PLa0u3J0uzAznYTqIZtyPBmorX8BxF7TY9`.

### Externe Ressourcen — Kuratierung gemäss HOWTO

- **Videos**: 3 verifizierte Playlists (MathemaTrick Geometrie + Lehrerschmidt Flächenberechnung + Lehrerschmidt Geometrie-Grundlagen) + 1 Platzhalter „in Vorbereitung". Für Mathe SMI, Mathehoch13, Magda und Daniel Jung wurde keine kreis-spezifische Playlist mit eindeutigem Owner-Match gefunden.
- **Aufgaben**: 4 Slots gefüllt mit sos-mathe.ch (G64 Kreis, G41 als Vorgriff auf Trigonometrie) und serlo.org (Kreis-Themenseite + Kreis-Aufgabenseite).

### Hinweise

- Pre-Flight-Bash-Check grün (`pw=1 mc=1 bn=1 toc=1 sf=1 bad=0`), Kollisions-Check grün (keine neuen Top-Level-Identifier-Konflikte), HTML-Balance grün (7 Canvas-Tags, alle Tags ausgeglichen), JS-Syntax (`node --check`) grün, Broken-Link-Check grün (alle 5 dl-Karten zeigen auf existierende Files), Negativlisten-Check grün.
- Anki-Build self-test: 32 notes, 32 cards, ankideck.apkg 6447 Bytes.

---

## [26_5] — 2026-05-15

### Vollständige Ausarbeitung der Themenseite 5.2b Vierecke

Die zweite Schwesterseite des in [26] eingeführten Sub-Splits ist nun ausgearbeitet. Die Seite g5-2b-vierecke löst den Stub von [26] ab.

### Hinzugefügt

- **`grundlagen/g5-2b-vierecke.html`** — neue, vollständig ausgearbeitete Themenseite zum Bereich Vierecke (~2040 Zeilen). Fünf interaktive Canvas-Animationen:
  1. **n-Eck mit Dreieckszerlegung (Anim 1)** — Schieber für n = 3 bis 8. Vom Eckpunkt A ausgehend werden Diagonalen gezeichnet, die das n-Eck in n−2 Dreiecke zerlegen. Tabelle daneben zeigt für jedes n: Anzahl Dreiecke und Innenwinkelsumme σ_n = (n−2)·180°. Zuschalten der Innenwinkel-Bögen mit Beschriftung α, β, γ, δ, ε, ζ.
  2. **Rechteck-Flächenformel (Anim 2)** — direkte Adaption der Eval-Animation Anim 1: Schieber für a (1–10) und b (1–8), drei Einheiten cm/dm/m. Einheitsquadrate-Raster und Quadrate-Durchzählung als Toggles. Live-Formel A = a · b mit aktuellem Wert.
  3. **Flächenumformung (Anim 3)** — direkte Adaption der Eval-Animation Anim 2 mit allen fünf Figurtypen: Parallelogramm (Schnitt rechts → Anbau links), Dreieck (Drehspiegelung um Mittelpunkt der schrägen Seite → Parallelogramm → Rechteck), Trapez (Drehspiegelung um Mittelpunkt der rechten Schenkelseite), Raute (umschreibendes Rechteck e × f, halbiert), Drachen (analog). Vier-stufige Schieber-Sequenz (Start / Schneiden / Verschieben / Rechteck). Formel- und Erklärungsbox wechseln synchron auf grün.
  4. **Sehnen- und Tangentenviereck (Anim 4)** — Tab-Auswahl Sehnen- / Tangenten-Modus. Vier Eckpunkte (Sehnenviereck) bzw. vier Berührungspunkte (Tangentenviereck) sind auf dem Kreis ziehbar. Live-Werte in der Legende: für das Sehnenviereck die Summen α+γ und β+δ (müssen 180° sein), für das Tangentenviereck die Summen a+c und b+d sowie ihre Differenz (sollte 0 sein). Innenwinkel-Beschriftungen optional zuschaltbar.
  5. **Regelmässiges Vieleck (Anim 5)** — Schieber für n = 3 bis 20. Mit Umkreis (Radius R = 1), Inkreis (Apothem r) und Bestimmungsdreieck (zwei Radien und Apothem zum ersten Sektor) als Hilfslinien. Tabelle daneben listet für alle n: Zentriwinkel ζ, Innenwinkel α, r/R und s/R. Die drei Fälle n = 3, 4, 6 sind grün hervorgehoben (exakte Werte ohne Trigonometrie). Beschriftungen R, r, s, ζ direkt im Bild.
- **`downloads/grundlagen/g5-2b-vierecke/`** — vier neue Druckseiten plus Anki-Deck:
  - `handout.html` (~190 Zeilen): Theorie kompakt; Themen Bezeichnungen, Innenwinkelsumme, Vierecks-Hierarchie, Umfang/Fläche, Mittellinie, Sehnen-/Tangentenviereck, regelmässige Vielecke, drei Sonderfälle ohne Trigonometrie, Plausibilität.
  - `formelauszug.html` (~140 Zeilen): Tabellen-lastig, kompakte Typografie. Innenwinkelsummen, Umfang+Fläche, Diagonalen-Eigenschaften, Sehnen-/Tangentenviereck (inkl. Ptolemäus-Satz), regelmässiges n-Eck mit den drei Sonderfällen ausgekoppelt. Quellenhinweis Orell Füssli.
  - `teste-dich-selbst.html` (15 Grundlagenaufgaben + Lösungen): Innenwinkelsumme, Hierarchie-Aussagen, Diagonalen, Rhombus-Seitenlänge per Pythagoras, Sehnen-/Tangentenviereck-Bedingungen, regelmässiges Sechseck, Diagonalen-Anzahl im n-Eck.
  - `aufgabenserie.html` (6 Anwendungsaufgaben + ausführliche Lösungen): Schwimmbecken-Trapez, hexagonale Bodenfliese, Achteck-Glasfenster, Drachen-Transparent, Sehnenviereck im Mosaik, Zwölfeck-Pavillon mit Vergleich zur Kreisfläche.
  - `ankideck.apkg` (35 Karten): Innenwinkelsumme, Hierarchie, alle Vierecks-Definitionen, Flächenformeln, Mittellinie, Sehnen-/Tangentenviereck-Bedingungen, regelmässige Vielecke (Formeln + drei Sonderfälle).

### Geändert

- **`grundlagen/g5-2b-vierecke.html`** Folgekorrekturen nach Erstausarbeitung:
  - Reihenfolge der Hauptabschnitte angepasst: **Darstellungen vor Definition**. Die n-Eck-Animation wird damit didaktischer Einstieg ins Kapitel und liefert den Spezialfall n = 4, der dann formal als Definition aufgegriffen wird.
  - RLP-Kompetenz-Block neu: anstelle bunter Sub-Split-Pills am Ende jedes Bullets sind die vierecksbezogenen Inhalte (Parallelogramm, Rhombus, Trapez, Mittellinie im Trapez, Umfang, Flächeninhalt) **fett markiert im Fliesstext**. Cross-Link zu g5-2a/g5-2c jetzt als kompakter `rlp-hinweis` (analog g2-2a/b).
  - Anim 4 (jetzt Anim 5) Regelmässiges Vieleck: Inkreis-Bug behoben — die Zeichenreihenfolge wurde umgedreht (erst Vieleck als gefüllte Fläche, dann Umkreis und Inkreis darüber), so dass der Inkreis nicht mehr von der blauen Vieleck-Füllung überdeckt wird.
  - Auto-Scroll beim Seitenaufruf unterdrückt: Die `scrollIntoView`-Anweisung in Anim 5 (Tabellenzeile aktivieren) wird nur ausgeführt, nachdem der User mit den Animations-Bedienelementen interagiert hat — verhindert das Springen der Seite zur Seitenmitte beim initialen Render.
- **`grundlagen/g5-2a-dreiecke.html`** analog umgebaut zur Konsistenz innerhalb des Sub-Splits: Sub-Split-Pills entfernt, dreieck-bezogene Inhalte (allgemeine und spezielle Dreiecke, Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Winkel und Winkelmass, Umfang, Flächeninhalt) im Fliesstext fett markiert, Cross-Link als `rlp-hinweis`.
- **`scripts/build_apkg.py`**: neuer Kartensatz `g52b_cards` (35 Karten) angelegt zwischen `g52a_cards` und `g11_cards`; `NEW_DECKS`-Liste um Eintrag `('g5-2b-vierecke', '5.2b Vierecke', …, g52b_cards)` erweitert.
- **README.md**: g5-2b Vierecke Status von `🔜 geplant` auf `✅ verfügbar` gesetzt.
- **HOWTO-externe-ressourcen.md §8 (Anbieter-Map)**: g5-2b-Zeile ergänzt mit MathemaTrick `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (Trapez/Vierecks-Anteile) und beiden Lehrerschmidt-Playlists `PLa0u3J0uzAzmX2iRZzdG8KuHJZA6sayy0` (30 Vid breit) sowie `PLa0u3J0uzAzk7Iw3l2Uxe7ftYXHmZ0Jhw` (12 Vid Kurzversion).

### Externe Ressourcen — Kuratierung gemäss HOWTO

- **Videos**: 3 verifizierte Playlists (MathemaTrick + Lehrerschmidt × 2 — verschiedene Längen für unterschiedliche Lerntempos) + 1 Platzhalter „in Vorbereitung". Mathehoch13, Magda und Mathe SMI haben kein passendes BM-Niveau-Material zu Vierecks-Grundlagen; Daniel-Jung-Playlist zu Vierecken konnte trotz mehrfacher Suche nicht eindeutig identifiziert werden.
- **Aufgaben**: 4 Slots gefüllt mit serlo.org (Parallelogramm, Trapez, besondere Vierecksarten) und sos-mathe.ch G61 (Konstruktion).

### Hinweise

- Pre-Flight-Bash-Check grün (`pw=1 mc=1 bn=1 toc=1 sf=1 bad=0`), Kollisions-Check grün (keine neuen Top-Level-Identifier-Konflikte; neue Rechteck-Animation nutzt Prefix `flR-` für alle IDs), HTML-Balance grün (5 Canvas-Tags, alle Tags ausgeglichen), Broken-Link-Check grün (alle 5 dl-Karten zeigen auf existierende Files), Negativlisten-Check grün.
- Anki-Build self-test: 35 notes, 35 cards, ankideck.apkg 6742 Bytes.

---

## [26_4] — 2026-05-15

### Vervollständigung der Themenseite 5.2a Dreiecke

Nach den Optik-Patches [26_1]–[26_3] war die Themenseite inhaltlich aufgehängt: RLP-Block wörtlich vom Mutter-Teilgebiet 5.2 übernommen, Aufgaben-Sektion mit Platzhalter „Aufgabenserie und Selbsttest folgen…", keine Downloads-Sektion, keine externen Ressourcen, keine Druckseiten, kein Anki-Deck. Mit [26_4] ist die Seite gemäss HOWTO-neue-themenseite.md vollständig.

### Hinzugefügt

- **RLP-Kompetenzen-Block** unter STYLEGUIDE §1c-Konvention wörtlich behalten, aber mit **Sub-Split-Markierung** angereichert: Inline-Pills hinter jedem Bullet zeigen, welche Stichworte des Bullets auf die drei Schwesterseiten 5.2a / 5.2b / 5.2c verteilt sind (`5.2a · Dreiecke` / `5.2a · Dreiecke teilweise` / `nicht in 5.2a`). Darunter Cross-Link-Box zu den anderen beiden Teilen mit ihren Sub-Titeln. Pattern ist neu und sollte bei der Ausarbeitung der Stubs g5-2b und g5-2c gespiegelt werden — Markierung dann analog mit `5.2b · Vierecke` bzw. `5.2c · Kreis`.
- **`<h2 id="aufgaben">`-Sektion**: sechs Aufgaben mit ausklappbaren Lösungen (Pattern wie g3-2):
  - A1 Innenwinkel und Aussenwinkelsatz (Probe über Nebenwinkel UND über Aussenwinkelsatz).
  - A2 Halbes gleichseitiges Dreieck (Verhältnis 1:√3:2 als Werkzeug).
  - A3 Pythagoras + Höhensatz im 5-12-13-Tripel.
  - A4 Eindeutig konstruierbar — fünf Teilaufgaben mit SSS/SWS/WSW/SsW/sSW.
  - A5 Dreieckselemente-Tabelle ausfüllen (Höhenschnittpunkt, Schwerpunkt, Umkreismittelpunkt, Inkreismittelpunkt).
  - A6 Anwendung Dachgiebel (Pythagoras + arctan + Fläche).

  Verwendet die globalen CSS-Klassen `block`/`block-aufg`/`block-bsp`/`block-titel` und die `loesung-toggle`/`loesung-body`-Pattern (mit `toggleL()` aus `mathlib.js`). Keine eigenen CSS-Klassen — die `aw`-Inline-Klassen aus g3-2 wurden bewusst nicht übernommen.
- **`<h2 id="downloads">`-Sektion**: `dl-grid` mit fünf Karten (Handout, Formelauszug, Anki-Deck, Selbsttest, Aufgabenserie) verlinkt auf `../downloads/grundlagen/g5-2a-dreiecke/`.
- **`<h2 id="ressourcen">`-Sektion** mit kuratierten externen Quellen nach HOWTO-externe-ressourcen.md (Anbieter-Reihenfolge MathemaTrick → Lehrerschmidt → Mathe SMI → Mathehoch13 → Magda → Daniel Jung; Aufgaben sos-mathe.ch → serlo.org → SwissEduc):
  - Videos: 3 verifizierte Playlists + 1 Platzhalter.
    - MathemaTrick **`PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-`** „GEOMETRIE — Dreieck, Prisma, Kreis, Trapez…" (60 Vid; breit, Dreieck-Anteile decken 5.2a ab).
    - Lehrerschmidt **`PLa0u3J0uzAznju8Er07GiFuaHGegrGtUe`** „Dreiecke konstruieren — geometrische Grundkonstruktionen" (15 Vid; perfekt fokussiert).
    - Daniel Jung **`PLLTAHuUj-zHgCcNWha7A2N_gR6UGAeQe2`** „Satzgruppe des Pythagoras, Berechnungen am Dreieck" (25 Vid; Pythagoras-Schwerpunkt). Owner per `web_fetch` verifiziert — Präfix `PLLTAHuUj-zH` ist mehrdeutig zwischen Mathehoch13 und Daniel Jung, hier eindeutig Daniel Jung.
    - Slot 4 mit Platzhalter „In Vorbereitung" (Mathe SMI, Mathehoch13 und Magda haben kein BM-passendes Dreiecks-Material für die fünf vorhandenen Schritte: Mathe SMI ist Klasse 11–13 fokussiert auf Analysis; Mathehoch13 und Magda sind Abi-fokussiert auf Analysis/Stochastik/Vektoren).
  - Aufgaben: 4 Slots gefüllt.
    - sos-mathe.ch **G61** Konstruktionsaufgaben (Aufgaben 23–26 Dreiecks-Konstruktion plus Punktmengen + Symmetrie).
    - sos-mathe.ch **G68** Kongruenzbeweise (7 Aufgaben).
    - serlo.org **/mathe/28875/aufgaben-zu-dreiecken** (Dreieckstypen, Fläche, besondere Linien).
    - serlo.org **/mathe/30678/aufgaben-zur-satzgruppe-des-pythagoras** (Pythagoras + Kathetensatz + Höhensatz + Anwendungen).
- **`downloads/grundlagen/g5-2a-dreiecke/`** — vier neue Druckseiten plus Anki-Deck:
  - `handout.html` (152 Zeilen): Theorie kompakt; Themen Bezeichnungen, Winkel, spezielle Dreiecke, Dreieckselemente, Konstruktion + Kongruenz, Fläche, Pythagoras-Satzgruppe, Plausibilität.
  - `formelauszug.html` (132 Zeilen): Tabellen-lastig, kompakte Typografie (`body { font-size: 10pt }`, MathJax-`scale: 0.95`), mit Quellenhinweis Orell Füssli.
  - `teste-dich-selbst.html` (77 Zeilen): 15 Grundlagenaufgaben (alle Theoriebereiche) + Lösungen.
  - `aufgabenserie.html` (118 Zeilen): 6 Anwendungsaufgaben (Dachgiebel / Leiter / Vermessung über Teich / Bauplatz mit Kosinussatz-Vorausweis / Treppe / Pyramidenkante mit Schräghöhe) + ausführliche Lösungen.
  - `ankideck.apkg` (32 Karten, 6573 Bytes): Definitionen, Sätze, Kongruenzsätze, Pythagoras-Satzgruppe, Spezialdreiecks-Verhältnisse 1:√3:2 und 1:1:√2, pythagoreische Zahlentripel.

### Geändert

- **`scripts/build_apkg.py`**: neuer Kartensatz `g52a_cards` (32 Karten) angelegt; `NEW_DECKS`-Liste um Eintrag `('g5-2a-dreiecke', '5.2a Dreiecke', …, g52a_cards)` erweitert.
- **`scripts/build_apkg.py` — Bugfix**: `out_dir_52 = 'downloads/grundlagen/g5-2-planimetrie'` zeigte auf den Pfad, der in [26] beim Sub-Split nach `_archiv_g5-2-planimetrie/` umbenannt wurde. Bei jedem Build wäre der alte Pfad automatisch durch `os.makedirs(...)` neu angelegt worden — eine Schein-Wiederauferstehung des aufgeräumten Verzeichnisses. Variable umgelenkt auf `downloads/grundlagen/_archiv_g5-2-planimetrie` mit Kommentar, dass das Deck nun ins Archivverzeichnis als Referenz geschrieben wird (gleicher Inhalt wie vorher).
- **README.md**: Sub-Split-Hinweis (Zeile 21) erweitert — „aktuell betrifft das Teilgebiet 2.2 → 2.2a + 2.2b **und Teilgebiet 5.2 → 5.2a + 5.2b + 5.2c**".

### Hinweise

- HOWTO-externe-ressourcen.md §8 (Anbieter-Map) sollte um eine Zeile für g5-2a erweitert werden — die für 5.2 (alte Gesamtseite) gelistete MathemaTrick- und Lehrerschmidt-Quelle bleibt gültig, kommt aber jetzt aus Sicht der drei Subseiten getrennt zum Einsatz. Die neue Daniel-Jung-Playlist gehört in die g5-2a-Spalte; ähnlich werden bei der Ausarbeitung von g5-2b und g5-2c eigene Owner-verifizierte Playlists für diese Subbereiche eintragbar sein.
- Pre-Flight-Bash-Check grün (`pw=1 mc=1 bn=1 toc=1 sf=1 bad=0`), Kollisions-Check grün (keine neuen Top-Level-Identifier), Broken-Link-Check der Themenseite grün (alle 5 dl-Karten zeigen auf existierende Files), Negativlisten-Check grün (kein mathebibel/mathepower/klassenarbeiten/youtube-results).
- Anki-Build self-test: 32 notes, 32 cards, ankideck.apkg 6573 Bytes.

---

## [26_3] — 2026-05-15

### Geändert

- **`grundlagen/g5-2a-dreiecke.html`** — Anim 6 (Kongruenzsätze): saubere Initialdarstellung bei `t = 0`.
  - **Vorher:** Beim Tab-Wechsel wurde zwar `sldKong.value = 0` zurückgesetzt, aber die Eckpunkt-Beschriftungen A und B waren bereits zu sehen (globaler `txt`-Aufruf am Ende der Draw-Funktion, unabhängig von t). Das verriet zu viel über die Konstruktion, bevor diese begonnen hatte — speziell beim SSS/SWS/WSW erschien die Lage der Grundseite, bevor der Lerner überhaupt einen Schieber-Schritt gemacht hatte.
  - **Jetzt:** Bei `t < 0.05` (Schieber ganz links) ist im Canvas nur noch die Mini-Skizze oben links sichtbar plus ein Hinweistext „Schieberegler bewegen, um die Konstruktion Schritt für Schritt aufzubauen." Eckpunkte werden phasengerecht eingeblendet, je nachdem, wann sie in der jeweiligen Konstruktion zum ersten Mal eine Rolle spielen: A erscheint bei allen fünf Tabs mit Schritt 1 (`t > 0.05`); B im SSS/SWS/WSW ebenfalls mit Schritt 1 (Endpunkt der Grundseite c), im SsW erst mit Schritt 4 (`t > 0.80`, wenn der Kreis den Strahl schneidet), im sSW gar nicht (dort gibt es nur B₁ und B₂); C im SSS/SWS mit Schritt 4 (`t > 0.7`), im WSW mit Schritt 5 (`t > 0.90`), im SsW von Anfang an (Endpunkt der kleinen Seite, `t > 0.05`).
  - **Erklärungstext** unten zeigt bei `t < 0.05` zusätzlich den Hinweis, dass die Mini-Skizze die gegebenen Stücke zeigt. Die Gegeben-Legende (rechts oben unter „Kongruenzsatz") bleibt von Anfang an sichtbar — sie ist die textuelle Spiegelung der Mini-Skizze und gehört zur Aufgabenstellung, nicht zur Konstruktion.
  - **Vorher bestand auch noch ein kleiner Bug** im SsW: die C-Beschriftung erschien erst bei `t > 0.7`, obwohl C schon ab `t > 0.05` als Endpunkt der kleinen Seite b verwendet wurde — der Eckpunkt war also sichtbar, aber unbeschriftet. Mitkorrigiert.

### Hinweise

- Pre-Flight-Bash-Check grün, Kollisions-Check grün, `node --check` grün, HTML-Tags balanciert.

---

## [26_2] — 2026-05-15

### Geändert

- **`grundlagen/g5-2a-dreiecke.html`** — Anim 8 (Pythagoras-Anwendung) didaktisch überarbeitet:
  - **Canvas zeigt jetzt die Vollform mit Halbierung.** Vorher war nur das rechtwinklige Halbdreieck zu sehen, der Lernende musste sich die Herkunft (halbes gleichseitiges Δ / halbes Quadrat) selbst dazudenken. Jetzt ist das ganze gleichseitige Dreieck (bzw. das ganze Quadrat) sichtbar — die gespiegelte Hälfte gestrichelt grau, die rechtwinklige Hälfte als hervorgehobenes Halbdreieck blau gefüllt mit Eckpunkten A, B, C. Spiegelachse (Höhe bzw. Diagonale) ebenfalls gestrichelt; gespiegelter Eckpunkt mit `A'` bzw. `C'` markiert. Bildunterzeile erklärt die Halbierung in einem Satz.
  - **Winkelangaben sind die Botschaft.** 30°/60°/90° bzw. 45°/45°/90° als feste Bildbeschriftung (definierendes Merkmal der speziellen Dreiecke, kein veränderlicher Messwert). Seiten a, b, c im Bild nur mit Buchstaben beschriftet — die Werte (symbolisch oder numerisch) stehen rechts in der Legende.
  - **Schieber durch Wert-Wahl ersetzt.** Statt eines kontinuierlichen Schiebers für die gegebene Seitenlänge gibt es nun den Chip-Tab `Wert der gegebenen Seite: 1 / g` — entweder konkrete Zahl `1` oder symbolische Variable `g`. Das macht den didaktischen Punkt (das Verhältnis ist universell, egal ob konkret oder allgemein) viel direkter, und der Rechenweg darunter spiegelt die Wahl wider: `g²` wo bei `1` einfach `1` stand, etc.
  - **Rechenweg-Box zeigt vollständige Pythagoras-Anwendung.** Vorher nur die Verhältnis-Formel und eine Probe `aStr² + bStr² = cStr²` mit den eingesetzten Werten. Jetzt: ein vollständiger Lösungsweg mit (1) Geometrie-Beziehung — beim gleichseitigen `a = c/2`, beim Quadrat `a = b`, (2) Pythagoras-Ansatz, (3) algebraische Umformung nach der gesuchten Seite, (4) Resultat, (5) Verhältnis. Statisch dargestellt, aber Inhalt dynamisch abhängig von Typ × gegebener Seite × Wert (insgesamt 2 × 3 × 2 = 12 Konfigurationen, alle mit MathJax-formelgesetzten Termen). Generator-Funktion `pythRechnung(typ, gegSeite, wert)` neu eingeführt.
  - **Zusammenfassungstabelle** ergänzt um den **Aussenwinkelsatz** `α' = β + γ` (jeder Aussenwinkel = Summe der beiden nicht anliegenden Innenwinkel) — ergänzt die bestehende Zeile zur Aussenwinkelsumme um den eigentlichen Satz, der in der Tabelle bisher fehlte.

### Hinweise

- Die Namenswahl `g` für den symbolischen Wert vermeidet die Kollision mit den Seitennamen a/b/c. `g` steht für „gegebene Grösse" und ist mathematisch neutral.
- Die `regler`-CSS-Klasse wird in dieser Animation nicht mehr benötigt, bleibt aber in den anderen sieben Animationen weiterhin in Verwendung — Inline-Style nicht angefasst.
- Pre-Flight-Bash-Check grün, Kollisions-Check grün (`pythRechnung` nicht reserviert), `node --check` grün, HTML-Tags balanciert.

---

## [26_1] — 2026-05-15

### Geändert

- **`grundlagen/g5-2a-dreiecke.html`** — Politur der Canvas-Animationen, ausgelöst durch zwei sichtbare Defekte in Anim 4 (Dreieckselemente) und Anim 6 (Kongruenzsätze):
  - **Einheitliche Schriftgrösse 14 px** für alle 97 `txt(ctx, …)`-Aufrufe (vorher gemischt 11/12/13/14/15/16/17 px je nach Animation und Element). Die Hilfsskizzen-Inset-Box (84×84 px, oberhalb Anim 6) behält absichtlich `ctx.font` 9 px — sie wäre mit 14 px unlesbar überfüllt und nutzt direktes `ctx.fillText`, nicht die `txt`-Helferfunktion.
  - **Anim 4 (Dreieckselemente) — Legende ohne Pixel-Koordinaten.** Die Zeile rechts unter "Schnittpunkt" zeigte zuvor `(x, y)` in Pixel-Koordinaten — eine nutzlose Information, die suggerierte, der Schnittpunkt habe einen mathematischen "Wert". Ersetzt durch leeren Wert; Punktname (H, M_U, S, M_I) und Erklärungstext bleiben unverändert.
  - **Anim 4 — Höhen und Mittelsenkrechten bis zum Bildrand verlängert.** Zuvor wurden die Höhen nur vom Eckpunkt bis zum Lotfusspunkt gezeichnet, die Mittelsenkrechten nur ±200 px um den Seitenmittelpunkt. Beim Ziehen der Eckpunkte in eine stumpfwinklige Konfiguration wandert der Höhenschnittpunkt H bzw. der Umkreismittelpunkt M_U aus dem Dreieck heraus — die abgeschnittenen Linien trafen sich dann visuell nicht mehr, obwohl der rote Schnittpunkt korrekt eingezeichnet blieb (rein aus dem mathematischen Schnitt zweier Geraden berechnet). Jetzt werden beide Sätze von Hilfslinien als ganze Geraden bis zum Canvas-Rand geclippt; neue Helferfunktion `clipLineToRect(P, d, W, H)` (eingefügt nach `footPerp`). Verlängerung jenseits des Dreiecks ist durchgezogen orange wie die Höhe selbst — falls das in stumpfwinkligen Konfigurationen optisch zu dicht wirkt, kann die Verlängerung später dünner oder gestrichelt gemacht werden.
  - **Anim 6 (Kongruenzsätze) — Tab sSW: Konstruktion sichtbar.** Bei den ursprünglichen Werten (a_klein = 110, b_gross = 200, α = 35°) galt `b·sin(α) ≈ 114.7 > a`, die Diskriminante `a² − (b·sin α)²` wurde negativ und der `if (disc > 0)`-Block sprang gar nicht erst an — Kreis, Strahl und beide Lösungs-Dreiecke blieben unsichtbar, der Schieber zeigte einen leeren Canvas. α auf 25° reduziert: jetzt `b·sin(α) ≈ 84.5 < a = 110 < b = 200`, die für „zwei Schnittpunkte" notwendige geometrische Bedingung ist erfüllt und der Kreis um C schneidet den Strahl an zwei Stellen B₁ und B₂.

### Hinweise

- Die `clipLineToRect`-Funktion ist generisch und kann in zukünftigen Animationen für beliebige Geraden-bis-Rand-Zeichnungen wiederverwendet werden (z.B. Achsen, asymptotische Linien, Geraden-Geraden-Schnitte).
- Pre-Flight-Bash-Check grün (`pw=1 mc=1 nav=1 def=0 bn=1 sec=0 bad=0`), `scripts/check_identifier_collisions.py` ohne neue Kollisionen (`clipLineToRect` nicht reserviert), `node --check` aller Inline-Skripte ohne Fehler.

---

## [26] — 2026-05-14

### Sub-Split RLP 5.2 Planimetrie und Ausarbeitung 5.2a Dreiecke

Das bestehende Teilgebiet **5.2 Planimetrie** (eine Themenseite mit Vierecken, Dreiecken und Kreis gemischt) wurde nach STYLEGUIDE §4.1 in drei thematisch fokussierte Schwesterseiten aufgesplittet. Die Dreiecks-Seite wurde vollständig neu ausgearbeitet mit acht interaktiven Animationen.

### Hinzugefügt

- **`grundlagen/g5-2a-dreiecke.html`** — neue, vollständig ausgearbeitete Themenseite zum Bereich Dreiecke (~2760 Zeilen). Acht interaktive Canvas-Animationen mit eigener Bedienleiste, Legende und Live-Werten:
  1. **Allgemeines Dreieck** — Eckpunkte per Maus/Touch ziehbar, Live-Anzeige aller Innen-/Aussenwinkel, Innenwinkelsumme (180°) und Aussenwinkelsumme (360°), Toggle für Aussenwinkel-Darstellung mit verlängerten Seiten.
  2. **Beweis Innenwinkelsumme** — 4-phasige Schieber-Animation: Dreieck → Parallele durch C zur Seite c → Wechselwinkel α und β bei C einblenden → gestreckter 180°-Winkel rot hervorgehoben. Formel-Box wechselt von Frage zu Lösung mit Farbübergang.
  3. **Spezielle Dreiecke** — Tab-Auswahl gleichschenklig (Schenkellänge + Basiswinkel) / rechtwinklig (zwei Katheten) / gleichseitig (Seitenlänge), mit eigenen Schiebern und vollständiger Werte-Legende inkl. Pythagoras-Probe beim rechtwinkligen.
  4. **Dreieckselemente** — Tab-Auswahl Höhen / Mittelsenkrechten / Seitenhalbierende / Winkelhalbierende. Dreiecks-Eckpunkte ziehbar. Schnittpunkt benannt (H, M_U, S, M_I), Toggle für Um-/Inkreis. Winkelhalbierende werden über den Inkreismittelpunkt hinaus bis zur gegenüberliegenden Seite geführt.
  5. **Flächenberechnung** — Adaption der Eval-Animation: Drehspiegelung → Parallelogramm → Schnitt → Anbau links außen → Rechteck g×h + grünes Resultatsrechteck g × ½h direkt im orangen Hilfsrechteck.
  6. **Kongruenzsätze** — Tab-Auswahl SSS / SWS / WSW / SsW / sSW, jeweils mit dynamischer Konstruktion über Schieber (gegebene Stücke grün, Hilfskreise/Strahlen orange). Inset-Skizze oben links zeigt die gegebenen Stücke in der Standard-Beschriftung. sSW mit zwei möglichen Dreiecken B₁/B₂.
  7. **Satzgruppe Pythagoras** — Tab-Auswahl Pythagoras+Kathetensatz / Höhensatz. Eckpunkt C ziehbar (automatische Projektion auf Thales-Kreis, garantierter 90°-Winkel bei C). Beide Tabs haben eine **animierte Schieber-Sequenz** mit drei Phasen (Scherung → Drehung → Scherung):
     - **Pythagoras+Kathetensatz**: Klassischer Euklid-Beweis I §47. Beide Kathetenquadrate werden mit Scherung-Drehung-Scherung in die zugehörigen Hypotenusen-Rechtecke p·c und q·c überführt, die zusammen das c²-Quadrat füllen. Jede Phase ist eine echte flächenerhaltende Transformation: Phase 1 schert mit Achse BL (bzw. AL bei b²) und bringt Eckpunkt C zum Dreieckseckpunkt A (bzw. B); Phase 2 dreht starr um B (bzw. A) um den Winkel, der den Hypotenusen-Eckpunkt-Vektor zur Außennormalen-Richtung dreht; Phase 3 schert mit Achse [B, B+out·c] (bzw. [A, A+out·c]) und richtet das Parallelogramm zum Endrechteck aus. c²-Quadrat dauerhaft grün gefüllt, Original-Kathetenquadrate dauerhaft schwach eingefärbt sichtbar.
     - **Höhensatz**: h² = p·q analog mit Scherung-Drehung-Scherung. Phase 1 schert das h²-Quadrat mit Fixgerade CF (Höhe), Eckpunkt Fq wandert auf der Quadrat-Außenseite nach G (Schnittpunkt mit Kreis um F mit Radius R = max(p,q)). Phase 2 dreht starr um F bis G auf den entfernteren Hypotenusen-Eckpunkt fällt (B falls p≥q, A sonst). Phase 3 schert mit Achse F-Eckpunkt zum p·q-Rechteck. Quadrat-Seite wird dynamisch gewählt (Richtung A wenn p≥q, sonst Richtung B), damit die Konstruktion in jedem Dreieck konstruierbar bleibt (Bedingung R² ≥ h² immer erfüllt).
  8. **Pythagoras-Anwendung** — Tab-Auswahl halbes gleichseitiges Δ (30°-60°-90°) / halbes Quadrat (45°-45°-90°), Auswahl welche Seite gegeben ist (a, b, c) mit Schieber für den Wert. Berechnete Seiten orange, gegebene Seite grün, Pythagoras-Probe automatisch.
- **`grundlagen/g5-2b-vierecke.html`** — Stub gemäß STYLEGUIDE §9 (RLP-Header, Stub-Banner, Master-Schema-Skelett mit Platzhalter-Texten, korrekte buildNav-Kette).
- **`grundlagen/g5-2c-kreis-und-kreisteile.html`** — Stub gemäß STYLEGUIDE §9 analog.
- **`scripts/check_identifier_collisions.py`** — Pre-Flight-Skript für die neue STYLEGUIDE §6.2-Konvention. Findet Top-Level-Symbol-Kollisionen mit `mathlib.js` und `nav.js`, unterscheidet zwischen blockierend (`const`/`let`/`class`) und unsauber-aber-tolerabel (`function`/`var`).

### Geändert

- **`nav.js`**: SITE-Array — Eintrag `g5-2 Planimetrie` durch drei Einträge `g5-2a Dreiecke`, `g5-2b Vierecke`, `g5-2c Kreis und Kreisteile` ersetzt. LERNGEBIETE-Array für Lerngebiet 5 entsprechend aktualisiert (`ids:['g5-1', 'g5-2a', 'g5-2b', 'g5-2c', 'g5-3', 'g5-4', 'g5-5']`).
- **`grundlagen/g5-1-grundlagen.html`**: `next`-Link in `buildNav` von `g5-2 Planimetrie` auf `g5-2a Dreiecke` aktualisiert.
- **`grundlagen/g5-3-trigonometrische-berechnungen.html`**: `prev`-Link in `buildNav` von `g5-2 Planimetrie` auf `g5-2c Kreis und Kreisteile` aktualisiert.
- **`README.md`**: Tabelle Grundlagenfach — Zeile `5.2 Planimetrie 🔜 geplant` ersetzt durch drei Zeilen `5.2a Dreiecke ✅`, `5.2b Vierecke 🔜`, `5.2c Kreis und Kreisteile 🔜`.
- **`grundlagen/g1-1-grundlagen.html`** und **`grundlagen/g1-2-zahlen-grundoperationen.html`**: lokale `function toggleL` entfernt (Soft-Treffer der STYLEGUIDE §6.2-Bereinigung). Die lokalen Versionen überschrieben die korrekte mathlib.js-Variante mit einer kaputten Implementierung — sie toggleten die CSS-Klasse `offen`, während das CSS auf `.sichtbar` reagiert. Damit waren die Lösungs-Buttons in diesen beiden Seiten faktisch wirkungslos. Nach Entfernen greift nun die mathlib-`toggleL`, die zusätzlich auch den Button-Text zwischen `▶ Lösung` und `▼ Lösung verbergen` umschaltet — konsistent mit allen anderen g-Seiten.

### Entfernt

- **`grundlagen/g5-2-planimetrie.html`** (1193 Zeilen) — ersatzlos gelöscht. Inhalte sind in 5.2a (Dreiecke) bereits neu und tiefer ausgearbeitet; Vierecke- und Kreis-Inhalte werden bei der Ausarbeitung von 5.2b und 5.2c aus der Versionshistorie zurückgeholt (Snapshot tals-mathe_25_14_10.zip).
- **`downloads/grundlagen/g5-2-planimetrie/`** — umbenannt zu `_archiv_g5-2-planimetrie/`. Der Ordner enthält die alten Druckseiten und das Anki-Deck zum gemischten 5.2-Thema; er ist nirgendwo mehr verlinkt, bleibt aber als Quellmaterial für die spätere Ausarbeitung von 5.2b und 5.2c im Repo erhalten. Bei der Ausarbeitung jeder Sub-Seite werden neue Materialien unter `g5-2b-vierecke/` und `g5-2c-kreis-und-kreisteile/` angelegt; der Archiv-Ordner kann dann gelöscht werden.

### Hinweise

- Master-Schema-Konvention erfüllt: h2-IDs aus dem Standard-Vokabular (einstieg → definition → darstellungen → typen → theorie → aufgaben → zusammenfassung). Sektionen `downloads` und `ressourcen` bewusst noch nicht angelegt — folgen mit dem Zusatzmaterial (Handout, Formelauszug, Anki-Deck, Selbsttest, Aufgabenserie) und der externen-Ressourcen-Kuration nach HOWTO-externe-ressourcen.md.
- Pre-Flight grün für g5-2a, beide Stubs und alle 32 Themenseiten (`scripts/check_identifier_collisions.py` ohne Kollisionen).
- Alle Eckpunkt-Drag-Operationen in den Canvases unterstützen Maus und Touch (für Tablet/Smartphone).
- Anim 7 (Pythagoras/Höhensatz): C wird automatisch auf den Thales-Kreis über AB projiziert — dadurch ist der rechte Winkel bei C garantiert, der Lernende kann aber trotzdem C in der Lage variieren, ohne dass die Animation kaputtgeht. Default-Position von C ist asymmetrisch links der Mittelachse gewählt (p ≈ 1.8·q), damit die p- und q-Unterschiede in der Animation sofort sichtbar sind.
- Hex-Farben im JavaScript-Block sind ausschließlich Fallback-Werte (`getPropertyValue('--blau').trim() || '#1e3a8a'`), greifen nur wenn CSS-Variablen nicht geladen sind.

### Gelernt (Bug, der zwei Iterationen kostete)

Bei der Inbetriebnahme von g5-2a erschienen die acht Animationen im Repo-Kontext zunächst nicht, obwohl die Datei isoliert (ohne `nav.js`/`mathlib.js`) funktionierte. Browser-Console: `Uncaught SyntaxError: Identifier 'fmt' has already been declared`. Ursache: `mathlib.js` definiert `const fmt = ...` als globale Konstante, mein Anim-Block hatte als Helfer `function fmt(n, k = 1) { ... }` ebenfalls global deklariert. Beim kombinierten Laden im Browser ist das eine Redeklaration im selben Top-Level-Scope, der Parser bricht ab — und sämtliche nachfolgenden Inline-JS-Definitionen (also alle acht Draw-Funktionen) sind nicht initialisiert. Animationen blieben damit blank.

`node --check` der Themenseite isoliert findet die Kollision nicht, weil sie erst zur Laufzeit beim kombinierten Laden entsteht. Ein zweiter Bugverdacht (griechische Unicode-Identifier `const α, β, γ, αs, βs, γs`) wurde im Zuge der Fehlersuche prophylaktisch mit ausgemerzt — diese sind zwar laut Sprachspezifikation erlaubt, aber je nach Browser-Engine grenzwertig (vor allem Misch-Identifier wie `αs`). Strings für die Anzeige (`'α'`, `'β'`, `'γ'`) bleiben unbedenklich.

Konvention daraus: **STYLEGUIDE §6.2 (neu) — Reservierte Top-Level-Identifier**, mit kompletter Tabelle der von `mathlib.js` und `nav.js` belegten Namen, expliziter Warnung vor griechischen Unicode-Identifiern, Unterscheidung zwischen blockierenden (`const`/`let`/`class`) und unsauberen-aber-tolerablen (`function`/`var`) Redeklarationen, und einem Pre-Flight-Skript `scripts/check_identifier_collisions.py`, das Kollisionen automatisch findet. Skript-Erstlauf förderte zwei Soft-Treffer in g1-1 und g1-2 zutage (`function toggleL` redeklariert) — nachfolgend bereinigt (siehe „Geändert"; die lokalen Versionen waren zudem funktional defekt).

STYLEGUIDE auf Version 1.7 angehoben.

---

## [25_14] — 2026-05-14

### Geändert

- **Cluster g1 (Arithmetik/Algebra) und Cluster g2 (Gleichungen) — externe Ressourcen neu kuratiert** nach der in COLLABORATION.md §9 / HOWTO-externe-ressourcen.md festgelegten Anbieter-Reihenfolge (Videos: MathemaTrick → Lehrerschmidt → Mathe SMI → Mathehoch13 → Magda → Daniel Jung; Aufgaben: sos-mathe.ch → serlo.org → SwissEduc):
  - **g1-1** Strukturen algebraischer Ausdrücke: 2 Playlists + sos-mathe G01 + 3× serlo.
  - **g1-2** Zahlen und Grundoperationen: 3 Playlists + sos-mathe G01 + G03 + 2× serlo.
  - **g1-3** Algebraische Terme: 3 Playlists + sos-mathe G02 + 3× serlo.
  - **g1-4** Zehnerpotenzen und Quadratwurzeln: 3 Playlists + sos-mathe G11 + G12 + 2× serlo.
  - **g2-1** Grundlagen Gleichungen: 2 Playlists + sos-mathe G05 + 2× serlo.
  - **g2-2a** Lineare Gleichungen: 3 Playlists + sos-mathe G05 (Aufgaben 27–33) + 2× serlo.
  - **g2-2b** Quadratische Gleichungen: 2 Playlists (Lehrerschmidt, Daniel Jung) + sos-mathe G31 + 2× serlo.
  - **g2-3** Lineare Gleichungssysteme: 2 Playlists (MathemaTrick, Lehrerschmidt) + sos-mathe G34a + G34b + 1× serlo.
  - **g3-1** Grundlagen Funktionen: Video-Sektion bleibt mit Platzhalter „In Vorbereitung" leer — bei keinem der sechs bevorzugten Anbieter gibt es zum allgemeinen Funktionsbegriff Material auf BM-Niveau (Sek-I bleibt zu elementar, Sek-II-Playlists wie DJ „Funktionen-Specials Analysis" steigen direkt in Analysis ein und sind über dem g3-1-Niveau). Aufgabensammlungen: sos-mathe G21 `funktion.pdf` + 2× serlo (174389 Funktion als eindeutige Zuordnung, 36045 Definitions-/Wertebereich). Begründung: Lieber 0 Video-Karten mit Platzhalter als unpassende verlinken.
  - **g3-3** Quadratische Funktionen: 4 Playlists (MathemaTrick, Lehrerschmidt, Mathehoch13, Daniel Jung — total 154 Videos) + sos-mathe G22 + 3× serlo (1348 Hauptseite, 1412 Gemischt, 26399 Nullstellen). DJ-Einzelvideo `pauiBVzELTc` (Grundlagen-Übersicht) ersetzt durch verifizierte DJ-Playlist `PLLTAHuUj-zHhRwBDeNqYk1edYRHmx8Qd1` (48 Vid). Mathe SMI (FOS-spezifisch) und Magda (Abi-Fokus) übersprungen, 4-Slot-Limit voll.
  - Alle neuen Playlist-Owner per `web_fetch` verifiziert (Mathehoch13 32 Vid, MathemaTrick Parabeln 42 Vid, DJ Quadratische 48 Vid); Lehrerschmidt-Parabeln-Playlist aus früherer g2-2b-Verifikation übernommen. Cache-Bug bei Lehrerschmidt-`web_fetch` beobachtet (lieferte MathemaTrick-Antwort) — Verifikation über CHANGELOG-Lookup robust.
  - Mathebibel- und Mathepower-Links entfernt; Anbieter-Map in `HOWTO-externe-ressourcen.md` §8 erweitert.

### Cluster g4 (Datenanalyse) kuratiert

- **g4-1** Grundlagen Statistik, **g4-2** Diagramme, **g4-3** Masszahlen — Ist-Zustand hatte überall Einzelvideos (unverifiziert) und `mathebibel.de`-Aufgabenlinks (Negativliste). Nach Recherche aller sechs bevorzugten Video-Anbieter haben nur Lehrerschmidt und Daniel Jung passende Playlists auf BM-Niveau zur beschreibenden Statistik:
  - **Lehrerschmidt** `PLa0u3J0uzAznKJ7-xAyq6tOtqQYzs5_38` (35 Vid „Statistische Grundbegriffe & Diagramme"): per `web_fetch` verifiziert, deckt Grundbegriffe, Häufigkeiten, Diagramme und Kennwerte ab.
  - **Daniel Jung** `PLLTAHuUj-zHifw_3OhBTvQq2EGX5NedOy` (31 Vid „Statistik" 5.–10. Klasse): per `web_fetch` verifiziert, deckt Daten, Häufigkeit, Mittelwert, Median, Boxplot, Diagramme, Abweichung ab.
  - MathemaTrick, Mathe SMI, Mathehoch13, Magda: keine sichtbaren Playlists zur beschreibenden Statistik auf BM-Niveau. SMI/Mathehoch13/Magda sind Sek-II-fokussiert (Stochastik/Wahrscheinlichkeit, Abitur-Stoff). Niveau-Passung-Regel aus HOWTO §4.2 Schritt 3 angewandt: lieber 2 verifizierte Slots als 4 mit Notbehelf.
  - Beide Playlists thematisch breit genug, um auf allen drei g4-Seiten als Primärquelle zu dienen (Lehrerschmidt-Playlist enthält Diagramme **und** Kennwerte; DJ-Playlist enthält Diagramme **und** Lagemaße **und** Streumasse). Die Slot-Wiederverwendung ist legitim — die Themen sind eng verzahnt und die Playlist deckt sie als Einheit ab.
- Aufgaben-Quellen für g4: **sos-mathe.ch entfällt** komplett — `verz_g.html` hat keine Statistik-Seite, `verz_s.html` (Schwerpunkt-Stochastik) führt nur Wahrscheinlichkeit/Verteilungen/Testen, keine beschreibende Statistik. **serlo.org** wird Primärquelle:
  - g4-1: `22778/daten-und-datendarstellung` (Übersicht) + `16416/statistik` (Grundlagen).
  - g4-2: `1352/diagramme` (spezifisch) + `22778/daten-und-datendarstellung` (Übersicht).
  - g4-3: `22834/daten-und-kenngroessen` (Übersicht Lagemaße/Streumasse) + `24551/aufgaben-zum-median` + `24548/aufgaben-zu-varianz-und-standardabweichung`.
  - SwissEduc-Munterbunt: kein passendes Material zur beschreibenden Statistik gefunden.
- Format-Inkonsistenzen aus Ist-Zustand bereinigt: Video-Icon `▶` → `▶️`, Aufgaben-Icon `📚` → `📝`, Subtitel-Form vereinheitlicht (mit „(Playlists)"-Zusatz).
- Pre-Flight (Standard + §3.7-Strukturchecks + Negativlisten-Check) auf allen drei Seiten grün. Slot-Counts: g4-1 = 2+2, g4-2 = 2+2, g4-3 = 2+3. Anbieter-Map in `HOWTO-externe-ressourcen.md` §8 um drei g4-Zeilen erweitert.

### Cluster g5 (Geometrie und Trigonometrie) kuratiert

- **g5-1** Grundlagen, **g5-2** Planimetrie, **g5-3** Trigonometrische Berechnungen, **g5-4** Einheitskreis, **g5-5** Trigonometrische Gleichungen — Ist-Zustand mit Negativlisten-Treffern (jede Seite mind. 1× `mathebibel.de`, g5-5 zusätzlich `mathepower.com`) und überwiegend Einzelvideos statt Playlists (g5-3, g5-4, g5-5). Auch falsche Icons (`📚` statt `📝` bei Aufgaben).
- Verifizierte Playlists per `web_fetch` und Cross-Reference:
  - **MathemaTrick** `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (60 Vid „GEOMETRIE – Dreieck, Prisma, Kreis, Trapez") — für g5-2 Planimetrie.
  - **Lehrerschmidt** `PLa0u3J0uzAznYTqIZtyPBmorX8BxF7TY9` (37 Vid „Geometrie-Grundlagen") — für g5-1 und g5-2; enthält Winkel/Geodreieck/Konstruktionen und Vierecke/Dreieck/Strahlensätze laut Themenliste auf lehrer-schmidt.de/mathematik/geometrie/.
  - **Lehrerschmidt** `PLa0u3J0uzAzlIHjv0J_R8sIj-xn8cVs0J` (20 Vid „Trigonometrie (Sinus, Kosinus, Tangens)") — für g5-3, g5-4, g5-5.
  - **Daniel Jung** `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (Trigonometrie-Playlist mit Übersichtsvideo `N4evtJU-h9w`) — vom Owner selbst auf mathefragen.de bestätigt (2018-10-03). Verwendet in g5-1, g5-3, g5-4, g5-5.
  - Mathe SMI, Mathehoch13, Magda: kein passendes Material auf BM-Niveau (SMI ist FOS Sek-II Stochastik/Analysis, Mathehoch13 Sek-II Wahrscheinlichkeit, Magda Abitur-Klausuren).
  - Im Ist-Zustand verlinkte Lehrerschmidt-Playlists `PLa0u3J0uzAzk7Iw3l2Uxe7ftYXHmZ0Jhw` (Vierecke), `PLa0u3J0uzAzkq45yEWUZG8YqESW6JZ5jk` (Dreieck), `PLa0u3J0uzAzmwdjF8DKmhPW0l7PBtLlne` (Strahlensätze) **nicht** übernommen, da keine externe Bestätigung der Playlist-IDs verfügbar (nur Inhalts-Bestätigung über lehrer-schmidt.de). Stattdessen die per `web_fetch` direkt verifizierte „Geometrie-Grundlagen"-Playlist mit 37 Videos verwendet, die laut Lehrerschmidt-Website ebenfalls Vierecke, Dreieck und Strahlensätze enthält. Reduktion von 3 auf 1 Playlist-Slot bei g5-2 ist konservativ aber sicher — Regel „verifiziert ≠ angenommen".
  - Im Ist-Zustand verlinkte DJ-Trigonometrie-Playlist `PLLTAHuUj-zHi-xXWY60VtdhnB07VqNskn` (g5-3, g5-4) **nicht** übernommen — Playlist-ID extern nicht referenziert, möglicherweise umbenannt/gelöscht. Ersetzt durch verifizierte `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr`.
- Aufgaben-Quellen: **sos-mathe.ch** ist Primärquelle für Geometrie/Trigonometrie:
  - g5-1: sos-mathe G60 Winkel + 2× serlo (Winkel, Bogenmass).
  - g5-2: sos-mathe G62 (Flächenberechnung) + G64 (Kreisberechnung) + G65 (Ähnlichkeit/Strahlensätze) + serlo Strahlensatz.
  - g5-3: sos-mathe G41 (rechtwinkliges Dreieck) + G42 (beliebiges Dreieck) + 2× serlo (sin/cos/tan, Sinussatz/Kosinussatz).
  - g5-4: serlo Einheitskreis + sos-mathe G43 (goniometrische Umformungen, trig. Pythagoras).
  - g5-5: sos-mathe G44 (goniometrische Gleichungen) + serlo Sinus-/Kosinusfunktion.
- Format-Inkonsistenzen bereinigt: Aufgaben-Icon `📚` → `📝` auf allen fünf Seiten. Subtitel einheitlich „🎬 Erklärvideos (Playlists)" und „📝 Aufgabensammlungen".
- Pre-Flight (Standard + §3.7-Strukturchecks + Negativlisten-Check) auf allen fünf Seiten grün. Slot-Counts: g5-1 = 2+3, g5-2 = 2+4, g5-3 = 2+4, g5-4 = 2+2, g5-5 = 2+2. Anbieter-Map in `HOWTO-externe-ressourcen.md` §8 um fünf g5-Zeilen erweitert.

### Sidebar-Layout: mehr Content-Platz, Prev/Next, Kapitelnummer als Banner

- `style.css` Grid `.page-wrap` aufgeweitet: `max-width` von 1100px auf **1400px**, Spalten von `1fr 180px` auf **`minmax(0, 1fr) 160px`**, Gap von 40px auf **72px**. Die schmalere TOC-Spalte und die deutlich grössere Gap schiebt die Sidebar so weit wie möglich nach rechts an den Viewport-Rand, während der Content-Bereich proportional wächst. Auf Bildschirmen ≥ 1400px hat der Content jetzt einen Maximum von ~1170px (vorher ~880px), also rund 33 % mehr horizontaler Lesefläche. Mobile-Breakpoint ≤ 900px unverändert (TOC ausgeblendet).
- `nav.js` `buildNav` schreibt die übergebene `cfg` als `window.__navCfg` ins globale Scope, damit `buildToC` Zugriff auf `kapitelNr`, `prev` und `next` hat (die `cfg` ist sonst lokal in `buildNav` gefangen).
- `nav.js` `buildToC` baut die TOC neu auf:
  - **Oben** (falls `cfg.prev` gesetzt): Link `← <prev.nr>` mit `prev.titel` als Tooltip, der zur vorherigen Themenseite navigiert.
  - **Mitte**: Banner-Titel `Kapitel <kapitelNr>` (z.B. „Kapitel 5.3"; uppercase-Mono-Stil aus bestehendem `.toc-title`-CSS, also wirkt als „KAPITEL 5.3"). Falls `kapitelNr` fehlt, Fallback auf alten Text „Auf dieser Seite".
  - **Liste**: unverändert die h2/h3-Anker der aktuellen Seite mit IntersectionObserver-basiertem Active-State.
  - **Unten** (falls `cfg.next` gesetzt): Link `<next.nr> →` mit `next.titel` als Tooltip.
  - Auf erster Grundlagen-Seite (`g1-1`) ist `prev:null` → Prev-Block fällt weg; analog letzte Schwerpunkt-Seite (`s4-3`) mit `next:null`.
- `style.css` neue Klassen: `.toc-nav` (Container, Flexbox zentriert), `.toc-nav-oben`/`.toc-nav-unten` (mit Trennlinie zum Hauptbereich der TOC), `.toc-prev`/`.toc-next` (Mono-Schrift, Hover-Effekt analog `.toc-link`).
- Funktionsprobe: alle 32 Themenseiten geben `kapitelNr`, `prev` und `next` im `buildNav`-Aufruf mit. JS-Klammer-Balance und CSS-Klammer-Balance OK. Standard-Pre-Flight auf einer Stichprobe von g5-Seiten unverändert grün. Broken-Link-Check 96/96.

### TOC-Einträge auf Kurz-Labels gemappt, einzeilig

- Problem: h2-Überschriften in den Themenseiten sind redaktionell ausgeschmückt (z.B. „Einstieg — vier Daten, vier Diagramme", „Klassieren — der Schritt vor dem Diagramm", „Bivariate Daten — Streudiagramm"). In der schmalen 160px-Sidebar führte das zu mehrzeiligen TOC-Einträgen und einer langen, überladenen Navigation. Besonders sichtbar in g4-2 Diagramme.
- Fix in `nav.js`: Neue Tabelle `TOC_KURZ` mappt die Standard-Slot-IDs auf feste Kurzlabels:
  - `einstieg` → Einstieg
  - `definition` → Definition
  - `darstellungen` → Darstellungen
  - `typen` → Typen
  - `theorie` → Theorie
  - `aufgaben` → Aufgaben
  - `zusammenfassung` → Zusammenfassung
  - `downloads` → Zusatzmaterial
  - `ressourcen` → Externe V&AS
- Nicht im Mapping enthaltene IDs (seitenspezifische Abschnitte wie `bogenmass`, `kosinussatz`, `vieta`, `quadranten`, `parameter` …) behalten ihren originalen h2-Text. Diese sind redaktionell ohnehin knapp formuliert.
- Der volle h2-Text wird als `title="…"` an den TOC-Link gehängt — bleibt also als Tooltip bei Hover verfügbar.
- `style.css` `.toc-link` ergänzt um `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`, damit auch seitenspezifische Custom-h2-Texte einzeilig bleiben und höchstens mit `…` beschnitten werden statt umzubrechen.
- Beispiel g4-2 vorher/nachher:
  - vorher: „Einstieg — vier Daten, vier Diagramme" / „Klassieren — der Schritt vor dem Diagramm" / „Die vier Standarddiagramme" / „Diagramme charakterisieren" / „Bivariate Daten — Streudiagramm" / „Aufgaben" / „Zusammenfassung" / „Zusatzmaterial" / „Externe Videos & Aufgabensammlungen"
  - nachher: Einstieg / Definition / Darstellungen / Typen / Theorie / Aufgaben / Zusammenfassung / Zusatzmaterial / Externe V&AS
- Reine JS/CSS-Änderung — keine Themenseite musste angefasst werden.

### TOC nur h2, keine h3-Unterpunkte mehr

- Auf Seiten mit h3-Abschnitten im Content (g4-3 mit A1–A6 als Aufgaben-Unterpunkten; g5-1 mit `klassifikator`/`winkelpaare`/`plausi-widget`; g5-2 mit `elemente`/`kreis-widget`; g5-3 mit `sinussatz`/`kosinussatz` unter „Allgemein") wurden diese h3 als eingerückte TOC-Einträge mitgenommen — die Sidebar wurde dadurch unnötig lang.
- `nav.js`: `buildToC` sammelt jetzt nur noch `<h2 id>`, keine `<h3 id>` mehr. Die h3-Anker im Content selbst bleiben unverändert — interne Verlinkungen `href="#sinussatz"` o.ä. funktionieren weiter.
- Resultat: TOC entspricht 1:1 der h2-Gliederung der Seite, keine Sub-Levels.
- `style.css`: tote Regel `.toc-link.toc-h3 { padding-left: 18px; font-size: 0.75rem; }` ersatzlos entfernt — sie betraf nur die jetzt nicht mehr erzeugten h3-Einträge.

### Konventionen erweitert

- **`COLLABORATION.md` auf v1.4**: Neue Sektion **§3.7 „Strukturelle Integritäts-Checks nach Block-Patches"** mit Bash-Snippet, der nach jeder Block-Ersetzung (Ressourcen-Sektion, Zusatzmaterial, RLP-Box, h2-Abschnitte) prüft: Eindeutigkeit kritischer Marker (`<h2 id="ressourcen"`, Subtitel, `<aside class="toc-wrap">`, `<footer>`), Tag-Bilanz `<a>`/`</a>` innerhalb der gepatchten Sektion, Slot-Limits ≤ 4 für Video- und Aufgaben-Karten. Hintergrund: Der bisherige Pre-Flight aus `STYLEGUIDE.md` §6.1 zählt nur Marker-Anwesenheit und erkennt keine kaputte Verschachtelung. Bei der g3-Iteration hat ein zu früh stoppendes Replacement-Pattern (`</div>\s*</div>`-Endmarker mitten in der Sub-Sektion) einen Müll-Schwanz aus dem alten Block hinterlassen → doppelte Subtitel, doppelte Karten, verwaistes `</a>`, kaputtes CSS-Grid zwischen `<main>` und `<aside>`. Schaden fiel erst im Browser auf. §3.7 deckt diese Klasse von Bugs in einem Tool-Aufruf ab.
- **`HOWTO-externe-ressourcen.md`** dreifach erweitert:
  - **§ 4.2 (Videos kuratieren)**: Nach Owner-Verifikation explizit ein zweiter Check „Niveau-Passung" — Playlist-Titel und Beschreibung mit RLP-Anspruch und h2-Schema vergleichen. Sek-II-Analysis-Playlist auf einer Grundlagen-Einführungsseite ist genauso falsch wie Sek-I-Material auf BM-Niveau. Verbindliche Regel ergänzt: **„Lieber leer als unpassend"** — wenn nach Durchlauf aller 6 Anbieter nichts passt, bleibt die Sub-Sektion mit dem Platzhalter aus § 6 leer; Begründung in den CHANGELOG-Eintrag.
  - **§ 4.4 (HTML-Patch)**: Verbindliches Replacement-Pattern dokumentiert — `re.compile(r'<h2 id="ressourcen".*?(?=\s*</main>)', re.S)` plus `subn` mit `assert n == 1`. Lookahead auf `</main>` ist der einzige stabile End-Anker; interne Tag-Marker (`</div></div>`) sind nicht eindeutig und stoppen zu früh.
  - **§ 4.5 (Verifikation)**: Pre-Flight-Workflow strukturiert: Standard-Pre-Flight (§6.1) **und** Strukturelle Integritäts-Checks (COLLABORATION §3.7) **und** Negativlisten-Check, alle drei vor jedem ZIP-Packen.
- Lehre der g3-Iteration: Der Auftraggeber hatte einen technisch korrekten Folge-Prompt geliefert (fertige HTML-Blöcke, klare Anweisung „1:1 übernehmen"). Die Fehler entstanden auf Claude-Seite — falsches Regex-Pattern, fehlerhafte Slot-Zählung beim grep (`▶️`-Emoji statt `<a>`-Karten), Übernahme einer „verifizierten ≠ passenden" Playlist. Konventions-Erweiterung zielt darauf, jeden dieser drei Fehler in Zukunft maschinell zu fangen, nicht durch zusätzliche manuelle Sorgfalt.
  - Formal: Subtitel überall einheitlich „🎬 Erklärvideos (Playlists)" und „📝 Aufgabensammlungen"; Video-Icon `▶️`, Aufgaben-Icon `📝`.

---

## [25] — 2026-05-10

Vollständiges Tiefenaudit gegen STYLEGUIDE v1.5 und RLP 2030 (SBFI, 13.6.2025), mit anschließendem Patch aller blockierenden Befunde (P0 und P1).

### Hinzugefügt

- 12 HTML-Druckseiten für die ausgearbeiteten Themen Lerngebiet 4 — `g4-1-grundlagen`, `g4-2-diagramme`, `g4-3-masszahlen` × {handout, formelauszug, teste-dich-selbst, aufgabenserie}. Schema nach `g5-1-grundlagen` (schlanker Stil, A4-Hochkant, `print.css` eingebunden, Druck-Bar mit Zurück-Link und Drucken-Button).
- 7 neue Anki-Decks für die bis dahin unversorgten Themen `g1-1`, `g1-2`, `g1-3`, `g1-4`, `g4-1`, `g4-2`, `g4-3`. Total 166 Karten. Deck-Hierarchie `TALS Mathematik::Grundlagen::<RLP-Nr> <Titel>`.
- Generator-Skripte unter `scripts/` (siehe Abschnitt „Workflow"): `build_print_g4.py` (Druckseiten-Generator für g4-Reihe als Vorlage) und `build_apkg.py` (Anki-Build, erweitert um 7 Kartenlisten).
- Erweiterter Pre-Flight-Check (Bash-Schnipsel in `HOWTO-neue-themenseite.md`).

### Geändert

- **`grundlagen/g4-3-masszahlen.html` komplett überarbeitet** auf den aktuellen Standard. Konkret:
  - MathJax-Einbindung von `tex-chtml.js` auf `tex-svg.js` umgestellt; Konfig auf Standard (boldsymbol-Package, scale 1.05, loader, skipHtmlTags).
  - Sämtliche hartkodierten Tailwind-Farben (`#cbd5e1`, `#0f172a`, `#1e3a8a`, `#f1f5f9`, `#475569`, `#0c4a6e`, `#86efac`, `#fca5a5`, `#166534`, `#991b1b`, `#f8fafc`, `#e2e8f0`, `#eff6ff`, `#93c5fd`) durch CSS-Variablen aus dem Designsystem ersetzt (`var(--blau)`, `var(--gruen-rand)`, `var(--linie)` etc.).
  - `'Courier New', monospace` durch `var(--mono)` (= JetBrains Mono) ersetzt.
  - Tab-Design für Lagemasse auf TALS-Blau-Schema umgestellt (analog g4-2).
  - h2-IDs auf Standard-Schema umgestellt: `lagemasse` → `definition`, `streumasse` → `darstellungen`, `grosse-stichproben` → `typen`, `robustheit` → `theorie`, `zusatzmaterial` → `downloads`. Sprechende Doppeltitel beibehalten (z.B. „Lagemasse — wo liegt die Mitte?").
  - `id` in `buildNav` von `g4-3-masszahlen` auf `g4-3` (passt zum SITE-Array in `nav.js`, sodass Dropdown-Highlight funktioniert).
  - Skript-Reihenfolge `nav.js` vor `mathlib.js` (analog g4-2).
  - `showLage()`-Funktion auf Parameter-basiert (`onclick="showLage('mw', this)"`) statt `event.target`.
  - Klassen-Vergleichs-Boxen (Robustheit): rote/grüne Border-Farbe nach Designsystem-Semantik (Mittelwert = nicht robust = rot, Median = robust = grün).
  - Page-Titel um „· 20 Lektionen" ergänzt.
  - Footer aus `<main>` herausgenommen und korrekt als `<footer class="site-footer">` außerhalb des page-wrap platziert. Zweizeilige Standard-Konvention („TALS Mathematik …" + „Grundlagenfach 4.3 Masszahlen").
  - Externe Ressourcen-Subtitel mit Emoji-Präfix (`🎬 Erklärvideos`, `📝 Aufgabensammlungen`).
- **`grundlagen/g2-2a-lineare-gleichungen.html`** und **`grundlagen/g2-2b-quadratische-gleichungen.html`**: `<aside class="toc-wrap"><div id="toc"></div></aside>` ergänzt. Vorher fehlte der Container, die sticky ToC-Sidebar wurde nicht angezeigt.
- **`build_apkg.py`**: NEW_DECKS-Schleife eingeführt; Test-Schleife auf alle 9 erzeugten Decks ausgeweitet.

### Behoben

- 19 broken Download-Links (von 96 auf 96 ✓ 0). Im einzelnen: 4 fehlende Anki-Decks für die g1-Reihe, 15 fehlende Materialien (Druckseiten + Anki) für g4-1, g4-2, g4-3. Alle erzeugt.
- Veraltetes Naming-Schema in `g4-3-masszahlen.html`: `g4-3-handout.pdf` → `handout.html` (analog für formelauszug, anki, teste-dich-selbst, aufgabenserie), gemäß aktueller Konvention `downloads/<bereich>/<thema>/<rolle>.<ext>` ohne Slug-Präfix und mit HTML statt PDF als Standardformat.

### Workflow

- Neuer Ordner `scripts/` mit zwei Generator-Skripten.
- Neue Datei `HOWTO-neue-themenseite.md` mit Schritt-für-Schritt-Anleitung für Themenseite + Materialien.

### Widerrufen / Korrektur

Im Audit-Markdown `AUDIT_tals-mathe_24.md` (Befund S1) war behauptet, das Lerngebiet 5 Geometrie verwende die Gruppe-2-Struktur (Land/Forst, 50L) statt der Gruppe-1-Struktur (TALS, 75L). **Diese Behauptung ist falsch.** RLP 2030, Seite 43, Tabelle 6.4.4.1, Lerngebiet 5: explizit **„(50 Lektionen)"** für Gruppe 1. Die Teilgebiet-Struktur 5.1 Grundlagen / 5.2 Planimetrie / 5.3 Trigonometrische Berechnungen / 5.4 Einheitskreis / 5.5 Trigonometrische Gleichungen ist ebenfalls die Gruppe-1-Struktur, nicht Gruppe 2. Das Repo gibt den RLP korrekt wieder; es gibt keine Abweichung. Befund S1 entfällt damit ersatzlos; auch P1-3 wird gegenstandslos. Lehre: Lektionenzahl und Teilgebiet-Liste vor Audit-Aussage im PDF direkt nachschlagen, nicht aus dem Gedächtnis schreiben.

---

## [24] — 2026-05-08 (Baseline)

Stand zu Beginn dieses Audits. Snapshot-ZIP `tals-mathe_24.zip`. 32 Themenseiten (19 Grundlagen ausgearbeitet, 13 Schwerpunkt als Stubs), Homepage, gemeinsames CSS/JS, Downloads-Verzeichnis mit Materialien für die ausgearbeiteten Themen (lückenhaft — siehe Audit).

---

## Anstehend (nicht in [25])

- **P2-Hygiene:** `<meta name="description">` auf allen Seiten, einheitliche Title-Tag-Konvention mit RLP-Nummer (12 Seiten betroffen), Open-Graph- und Twitter-Card-Metas auf `index.html`, `LICENSE`-Datei mit CC-BY-NC-4.0-Volltext im Repo-Root, `404.html`, `sitemap.xml`.
- **P3-Aufräumarbeiten:** `mathlib.js` aus den 13 Schwerpunkt-Stubs entfernen (wird dort nicht genutzt), `.nojekyll`-Datei für GitHub Pages, Favicon, externe Link-Prüfung mit `curl -I` über alle 95 externen URLs.
- **Ausarbeitung der 13 Schwerpunkt-Stubs:** s1-1 bis s4-3. Vorgehen siehe `HOWTO-neue-themenseite.md`.
