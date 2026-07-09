# Audit aller Themenseiten — 6. Juli 2026

**Auftrag:** Vollaudit über alle 46 Themenseiten (Grundlagen- + Schwerpunktfach) in den Dimensionen Notation, Konsistenz, RLP-Abdeckung, Verständlichkeit Sek II, fachliche Richtigkeit, Didaktik und Visualisierungspotenzial. **Ohne** Druckseiten und **ohne** Bewertung der externen Ressourcen. Es wurde **nichts geändert** — dieser Bericht und die TODO-Liste sind das einzige Ergebnis.

**Methode:** Ein mechanischer Gesamtpass (Skelett-Anker, Mini-Check-/Aufgaben-Zählung, ß/Dezimalkomma/Delimiter, Nav-Ketten-Symmetrie, Terminologie-Zähler, Widget-Statistik) plus sechs parallele Prüfgruppen (GF LG1+2, GF LG3+4, GF LG5, SP LG1+2, SP LG3, SP LG4), die jede Seite vollständig gelesen und **über 400 Zahlenwerte mit python3 nachgerechnet** haben (Beispiele, Aufgabenlösungen, chkNum-Targets, Canvas-Geometrien).

**Severity:** **A** = Fehler (fachlich falsch, kaputt gerendert) · **B** = Mangel (Konsistenz, Didaktik, RLP-Lücke) · **C** = Idee (Verbesserung, Visualisierung).

---

## 1. Gesamtbild

Das Lehrmittel ist in bemerkenswert gutem Zustand:

- **Notation:** Kein ß, durchgehend Dezimalpunkt (auch in JS-Live-Anzeigen), ausschliesslich `\(…\)`/`\[…\]` — auf allen 46 Seiten. Die wenigen `$…$`-Treffer sind korrektes TeX in `\colorbox{}`.
- **Fachliche Richtigkeit:** Von >400 nachgerechneten Werten waren **alle Schwerpunkt-Werte korrekt** (LG 1–4: null Rechenfehler). Die A-Funde konzentrieren sich auf ältere Grundlagenfach-Seiten (v.a. LG 5) und sind grösstenteils Darstellungs-/Beschriftungsfehler, nicht falsche Mathematik.
- **Struktur:** Master-Schema, Mini-Checks (4 Typen), A1–A7, Fehlerblöcke, Merksätze und Sub-Split-Deklarationen sind flächendeckend vorhanden; die prev/next-Kette ist in beide Richtungen symmetrisch; alle Querlink-Ziele und Download-Dateien existieren.
- **RLP-Abdeckung:** Über die Sub-Splits vollständig — mit **neun punktuellen Lücken** (siehe §3.3), wo eine Box-Kompetenz oder ein Lernziel auf der Seite nicht eingelöst wird.
- **Systematische Muster:** Drei wiederkehrende Konsistenz-Themen ziehen sich durch mehrere Seiten: (1) fehlende 👁/💡-Rollover bei fast allen g5-Animationen, (2) A7-Vertiefungs-Pille fehlt/verrutscht + Abschnitts-Kommentare verschoben (g5-Serie, g4-1), (3) Terminologie-Divergenzen (Definitionsmenge/-bereich, Wertemenge/-bereich, Probe/Kontrolle, Streckfaktor-Varianten, waagrecht/waagerecht, Fr./CHF, Arithmetik/Algebra vs. «und»).

---

## 2. Severity A — Fehler (15 Funde)

| # | Seite | Stelle | Befund |
|---|-------|--------|--------|
| A1 | g1-1-grundlagen | A6-Lösung (Z.732) | «aus \(2(3b+4)\) liest man ab, dass der Umfang stets **gerade** ist» — gilt nur für ganzzahlige \(b\) (b=0.5 → U=11) |
| A2 | g1-3-algebraische-terme | Fehlerblock Vorzeichen (Z.519–521) | Satz widerspricht sich: «wird zu +2, nicht etwa zu −(−2) = −2» — die Gleichung −(−2)=−2 ist falsch |
| A3 | g2-2b-quadratische-gleichungen | Diskriminanten-Widget, JS `D_FAELLE 'pos'` (Z.940–947) | Fall D>0 zeigt «25−24=**16**», «√16=4», «5±4» — für a=1, b=−5, c=6 ist D=1, √D=1; die angezeigten Zahlen ergäben 4.5/0.5 statt 3/2 |
| A4 | g4-2-diagramme | Balkendiagramm-Demo-SVG (Z.188–203) | Balkenhöhen widersprechen der beschrifteten y-Achse (Labels 22/32/17/12, Skala liest 18/26/14/10) — auf der Seite, die Achsen-Ablesen lehrt |
| A5 | g5-2a-dreiecke | Anim «Spezielle Dreiecke» (Z.1473) | Slider-Label «Basiswinkel β = γ» falsch — Basiswinkel sind α und β, γ ist der Spitzenwinkel |
| A6 | g5-2a-dreiecke | A6-Lösung Teil 3 (Z.853) | Dachfläche 63.85/127.7 m² falsch; exakt s=√28.25 → 63.78 bzw. 127.6 m² (Zwischenrundung) |
| A7 | g5-2a-dreiecke | load-Handler (Z.3423–3432) | `drawStativ()` fehlt im load-Handler — Einstiegs-Canvas ist beim ersten Laden **leer** |
| A8 | g5-2b-vierecke | A7-SVG (Z.843) | Verirrtes `<p>`-Tag statt Drachen-Polygon im SVG — Umriss fehlt, nachfolgende SVG-Elemente werden nicht gerendert; Skizze kaputt |
| A9 | g5-2c-kreis-und-kreisteile | Def-Tabelle (Z.303) vs. A1.1/Mini-Check | Sehne definiert als Strecke «(ohne durch M zu gehen)» — direkter Widerspruch zu «jeder Durchmesser ist auch eine Sehne: Wahr» |
| A10 | g5-2c-kreis-und-kreisteile | A6-Lösung (Z.965) | 120.25π = 377.78, Seite schreibt 377.79 m² |
| A11 | g5-2c-kreis-und-kreisteile | A2-Lösung (Z.859) | `\);\quad \(` — `\quad` steht ausserhalb der Delimiter, rendert als Literaltext |
| A12 | g5-2d-zentrische-streckung | Anim 5 Legende (Z.573–576) | Katheten-Labels vertauscht («a Kathete bei A» — a liegt gegenüber A); statische Startwerte ebenfalls vertauscht (JS überschreibt die Zahlen, nicht die Texte) |
| A13 | g5-3-trigonometrische-berechnungen | Strategie-Flussdiagramm-SVG (Z.700–733) | `\(…\)` in SVG-`<text>` wird von MathJax nicht gerendert — vier Diagramm-Zeilen (Sinussatz, Cosinussatz…) **unsichtbar** (mathjax-full-verifiziert) |
| A14 | g5-3-trigonometrische-berechnungen | A1-Lösung Punkt 2 (Z.849) | Fall falsch klassifiziert: α=40°, β=70°, c=10 ist **WSW**, nicht WWS (Zahlenwert selbst korrekt) |
| A15 | g5-5-trigonometrische-gleichungen | Einstieg (Z.109) vs. JS (Z.947) · Widgets 1/2 | Text sagt Mitte 20 m/Start 0 m, Code rechnet 22 m/2 m — markierte Schnittpunkte sind nicht die «halbe Höhe». Zudem: bei c=±1 zeigen beide Widgets doppelte identische «Lösungen» (φ₁=φ₂=90°) statt einer |
| A16 | s2-2a-potenz-wurzel-rationale-gleichungen | Mini-Check «Verfahren», Transfer (Z.322) | Behauptet, bei 6/(x−2)=x+3 könne x=2 als Scheinlösung «hereinrutschen» — falsch: Lösungen sind 3 und −4, x=2 kann bei korrekter Rechnung nicht entstehen |

*(Nummerierung A1–A16; A15 fasst zwei zusammenhängende g5-5-Funde zusammen.)*

---

## 3. Severity B — Mängel

### 3.1 Systematische Muster (mehrere Seiten, je ein Sammel-Durchgang)

- **B-M1 · 👁/💡-Rollover fehlen (Pflicht bei interaktiven Animationen):** g5-1 (3 Widgets), g5-2b (Anim 2–5 + Einstieg), g5-2d (Anim 1/3/4/5 + Einstieg), g5-3 (6 Animationen), g3-1 (3 Widgets). Jeweils nur eine Anim pro Seite hat das Markup.
- **B-M2 · A7-Vertiefungs-Pille und Abschnitts-Kommentare:** A7 ohne `aufg-vertiefung`-Pille bzw. Pille bei A6 statt A7, A7-Block unter dem «ZUSAMMENFASSUNG»-Kommentar: g5-1, g5-2a, g5-4, g5-5 (Pille erwägen), g4-1. Verrutschte/doppelte Abschnitts-Kommentare zusätzlich: g1-2, g5-2b, g5-2c, g5-4.
- **B-M3 · Terminologie (projektweite Entscheidungen nötig):**
  - «Definitionsmenge/Wertemenge» (dominant, v.a. SP) vs. «Definitionsbereich/Wertebereich» (g3-1 17×, s3-2b 12× u.a.) — **Glossar führt umgekehrt Definitionsbereich/Wertebereich**. Ein Begriffspaar festlegen (STYLEGUIDE-Eintrag) und angleichen.
  - «Probe» (s2-1 24×, g-Seiten) vs. «Kontrolle» (s2-2a/b/c ausschliesslich) — ein Leitbegriff für Lerngebiet 2 SP.
  - «Streckfaktor» (18×) vs. «Streckenfaktor/Streckungsfaktor/Ähnlichkeitsfaktor» (g5-2d).
  - «waagrecht» (CH) vs. «waagerecht» (g3-2, g3-3, g5-5).
  - «Fr.» vs. «CHF» (g2-2a mischt; g2-1 nutzt CHF).
  - pt-bereich Lerngebiet 1 SP: s1-1 «Arithmetik/Algebra» vs. s1-2/s1-3 «Arithmetik und Algebra».
  - g5-2c: drei Symbole/vier Namen für den Zentriwinkel (ζ/φ/α) auf einer Seite.
  - s4-3d: «Richtungsvektoren» vs. «Spannvektoren» ohne Gleichsetzung.
- **B-M4 · chkNum-Bruch-Eingabe:** Der Strip-Regex entfernt «/» — Eingaben wie «9/2» oder «11/4» werden als falsch gewertet (s2-1, s2-2a; gleiches Muster auf allen neueren Seiten). Einheitlich lösen: «/» schonen + Mini-Bruch-Parser oder Platzhalter «als Dezimalzahl».

### 3.2 Fachliche Präzision (kein Rechenfehler, aber unscharf)

- g2-1 (Z.415): «linear → genau 1 Lösung» ohne a≠0.
- g2-2a: Definition (a,b∈ℝ) vs. Mini-Check (verlangt a≠0) widersprechen sich; Lead verspricht Verhältnis-/Bruchgleichungen, die es nicht gibt; «dritter Lösungsfall … (Fall 2)».
- g2-2b: A6 verworfene Lösung 1.76/−2.24 statt 1.75/−2.25 (Zwischenrundung); «Zerfallsprozesse» als Beispiel für quadratische Gleichungen.
- g4-0/g4-3: Standardabweichung als «mittlere/durchschnittliche Abweichung» erklärt (korrekt: quadratisches Mittel).
- g5-2c: «Tangentensatz» für Radius⊥Tangente (nicht Standard); b=r·φ «im Bogenmass», das die Seite nie einführt; unbelegter Pi-Rekord «Nov. 2025».
- g5-3: Merksatz/Tabelle nennen nur «WSW/SSW» (WWS fehlt); Fehlerblock «sin zwischen −1 und 1» im rechtwinkligen Kontext verwirrend.
- g5-5: Fehlerblock «cos hat zwei Lösungen» gilt nicht für c=±1 (A4d behandelt selbst sin=−1 mit einer Lösung); Intervallnotation gemischt ([a, b] mit Komma neben [a; b[).
- s1-2: «Gesetze gelten für alle rationalen Exponenten» ohne die Voraussetzung a>0 an dieser Stelle.
- s2-2a: Einstieg «Uetliberg h≈900 m über dem Mittelland» — physikalisch zählt Höhe über Gelände (~460 m); Formel sagt «über Meer»; Beispiel 4/A7 ohne Definitionsmengen-Zeile trotz «D zuerst»-Tipp.
- s2-2c: Randfall r=0 bei Betragsungleichungen fehlt.
- s3-2a: «f: ℝ→ℝ» widerspricht der eigenen Hyperbel-Tabelle (D=ℝ∖{0}); Asymptoten-Definition «ohne zu schneiden» zu eng.
- s3-4b: Weber-Fechner in «Phon» statt dB (Konflikt mit Physik-Schwesterprojekt); «a<1» statt «0<a<1» in Eigenschaften-Tabellen (4a und 4b).
- s4-2a: rlp-hinweis beansprucht 4.1-Inhalte; Abschnitt 5 dupliziert s4-1 ohne Einordnung als Wiederholung.
- s4-1/s4-2a: Querverweise «hast du in ↩ 4.3c/d behandelt» — falsche Zeitrichtung (4.3 kommt in der Kette später).
- s4-3b: Beispiel 4 (AB·BC für rechten Winkel) widerspricht scheinbar dem direkt folgenden Fehlerblock («beide von der Ecke weg»).
- s4-3c: A5-Aufgabentext verunglückt («bei km 50? — nein: …», Einheiten inkonsistent) — liest sich wie ein Editier-Artefakt.

### 3.3 RLP-/Lernziel-Lücken (Kompetenz beansprucht, nicht eingelöst)

| Seite | Lücke | Vorschlag |
|-------|-------|-----------|
| g1-2 | Bruch-**Rechenregeln** (A3 verlangt sie, Theorie fehlt) | Theorieblock «Grundoperationen mit Brüchen» vor A3 |
| g4-1 | «ordinal» in Lernzielen + Mini-Check, nie gelehrt | Theorieblock nominal vs. ordinal |
| g4-2 | Lernziel «manipulative Darstellungen erkennen» ohne Theorie-Anker | Fehler-/Theorieblock «Manipulative Diagramme» |
| g4-3 | Spannweite überall verwendet, nie definiert | Def-Block + Zeile in Zusammenfassung |
| g5-1 | Lernziel «Stufen-/Wechselwinkel», Seite lehrt sie nicht | Vierten Widget-Tab oder Lernziel kürzen |
| g5-2a | Kompetenz/Lernziel «Umfang berechnen» — U=a+b+c fehlt komplett | Formel + Teilaufgabe ergänzen |
| g5-4 | RLP «Umkehroperationen erläutern» — arcsin/arccos/arctan kommen nicht vor | Kurzabschnitt mit Brücke zu 5.5 |
| s3-3 | «Extremwerte berechnen» nur grafisch; Linearfaktor-Abspaltung (Polynomdivision/Horner) fehlt | Verfahren + Beispiel + Teilaufgabe; Ausblick Differentialrechnung deklarieren |
| s3-4a/b | RLP nennt «Sättigungsprozesse» — beschränktes Wachstum fehlt in beiden Teilen | Abschnitt/Aufgabe ergänzen |
| s3-2b | RLP «ganzzahlige Exponenten»: Umkehrung von x⁻ⁿ unbehandelt und nicht deklariert | Satz ergänzen oder im rlp-hinweis deklarieren |

### 3.4 Einzelne B-Funde (Auswahl, vollständig in der TODO-Liste)

- g1-3: statischer Legenden-Startwert 650 statt 1040; Querlink «↗ 1.4» auf suboptimalen Anker; unbelegter Verweis auf s1-1/s1-2 für (a+b)³.
- g1-4: toter Anker `g1-1#typen`; durchgehend «Komma verschieben» trotz Dezimalpunkt-Konvention; Zoom-Objekte Milchstrasse/Universum verrutscht.
- g2-1: A2-Platzhalter verraten die Lösung; String-Vergleich wertet korrekte Eingaben als falsch.
- g2-3: Geraden-Label ausserhalb des Canvas (unsichtbar).
- g3-2: A3 ohne abrufbaren Lösungsweg (anders als A4–A6).
- g3-3: **a-Parsing-Bug** — U+2212-Minus wird nicht erkannt, «−0.5» wird zu 1: Parabel im A2-Widget öffnet falsch (Node-verifiziert).
- g4-0: Grammatikfehler im Scope-Text; «rund 8000 BM2-Lernende» unbelegt; Boxplot-Whisker vs. Tukey-Diagnose inkonsistent.
- g4-1: Anredebruch «Was Sie eben gesammelt haben»; nur 3 Mini-Checks.
- g5-1: totes CSS (.skizze-grid); g5-2b: Live-Klassifikation kennt den Drachen nicht, Sehnenviereck-Drag NaN-anfällig; g5-2d: Lernziele-Block an falscher Position, Massstabs-Ticks ohne Beschriftung; g5-4: defekter Satzbau (erkl-ek2), Schiff-Widget-Quadrant an Achsenwinkeln falsch, «π/2 ± kπ»-Notation; g5-5: grammatisch defekter Fehlerblock-Satz.
- s1-2/s1-3: h2-Anker-IDs sind Template-Reste (id="darstellungen" trägt «Potenzgesetze» etc.); A1-Optionen in Gleichungs-Reihenfolge (Positions-Matching); A1 fragt Gesetz 5 nie ab; toter fmt2-Helfer (mehrere neue Seiten).
- s2-1: Waage-Canvas: Gewichtestapel ragt über den Balken (Geometrie verifiziert); x²−5x+6=0 dreimal identisch (A3b = Abschreiben).
- s2-2b: A7-chkNum-Toleranz zu eng (7.9 Mio wird als falsch gewertet); Beispiel 6 «D: x>3» ohne Herleitung.
- s4-2a: Quader-Canvas: `hinten`-Set enthält '3-0' statt '0-3' — verdeckte Kante wird durchgezogen gezeichnet; tote Variable.

---

## 4. Severity C — Visualisierungs-Ideen (grösste Hebel zuerst)

**Priorität 1 — Kernkonzept der Seite ohne tragendes Widget:**

1. **s3-5 Phasor:** rotierender Zeiger + synchrone Zeitspur y=A·sin(ωt+φ) — Kernstelle «harmonische Schwingung».
2. **g5-4 «Abwickler»:** Punkt läuft auf dem Einheitskreis, rechts entsteht synchron die Sinuskurve (Brücke zu 5.5); dazu Symmetrie-Spiegel-Widget und Vorzeichen-Trainer.
3. **s4-3d Schrägbild statt Grundriss:** Haus-Drahtmodell mit geneigter Dachfläche; Kamin-/Drohnen-Gerade mit markiertem Durchstosspunkt (Kernkompetenz der Seite; `proj()` aus s4-2a wiederverwendbar).
4. **s4-3c Lot-Widget** (t-Slider bewegt F auf g, |PF| live, Minimum beim Lot) und **windschief-Schrägbild** (zwei «Stockwerke»).
5. **g2-2b Parabel-Canvas** zur Diskriminante (Parabel wandert mit k-Slider, Nullstellen verschwinden bei k=9) — die Seite kommt bislang ganz ohne Parabel aus.
6. **s2-1/s2-2a/s2-2b Scheinlösungs-Grafik:** beide Seiten einer Wurzel-/Bruch-/Log-Gleichung als Kurven, Scheinlösung als Schnittpunkt der falschen Kurve sichtbar (D-Strahl mit Ausschlüssen).
7. **g5-3 SSW-Fallunterscheidung:** Kreisbogen um B, Slider a → 0/1/2 Schnittpunkte live.
8. **s3-3 Leitterm-Zoom:** f(x) und aₙxⁿ fallen beim Herauszoomen zusammen; plus Trace-Punkt fürs «grafische Ablesen».
9. **s4-2b Sektor-Abwicklung** live neben dem Kegel-Querschnitt + **k³-Slider** («halbe Höhe ≠ halbes Volumen»); **s4-2c Kugelteil-Querschnitt** mit h-Slider und Grenzfall-Snaps.
10. **g4-Reihe interaktivieren** (0 Widgets in g4-1/2/3): Robustheits-Slider (Ausreisser-Lohn ziehen — Median vs. Mittelwert), Merkmalstyp-Zuordnungsspiel, Manipulations-Demo.

**Priorität 2 — wertvolle Ergänzungen:** g1-1 Distributivgesetz-Flächenmodell · g1-2 Zahlengeraden-Betrag · g1-3 Zweiklammersatz-Teilerpaare · g1-4 «√n einschachteln» · g2-1 Ungleichungs-Zahlenstrahl + Wettrennen-Diagramm · g2-2a Vorzeichenkipp-Zahlenstrahl + Parameter-Geraden · g2-3 Lösungsfall-Slider + Geradenbüschel · g3-1 Vertikaltest-Gerade + Schnittpunkt-Widget · g3-2 Steigungsdreieck-Canvas (ziehbare Punkte) · g3-3 Extremwert-Canvas · g5-1 Radiant-Slider + Zufallswinkel + Skizzen-Gegenüberstellung · g5-2a Dreiecksungleichungs-Explorer + Schwerpunkt 2:1 · g5-2b Trapez-Scherung + Drachen-Widget · g5-2c Kreisring-Morphing · g5-2d Strahlensatz-Drag + «auseinandergelegte» Dreiecke + Massstab-&-Fläche · g5-5 Lösungs-Trainer + Kreis-Kurve-Kopplung + Gezeiten-Canvas · s1-1 Richtungs-Umschalter + Regel-Prüfstand · s1-2 Zehnerpotenzen-Umwandler + Hierarchie-Auswerter · s1-3 Rechenschieber + Verdopplungs-Explorer · s2-2c Betrags-Explorer (V-Kurve + y=c) · s3-1 Ungleichungs-Widget + Weide-Doppelcanvas · s3-2a Paritäts-Explorer + Symmetrie-Checker · s3-2b Transformations-Slider · s3-4a a-Slider + e-Grenzwert · s3-4b Spiegel-Wanderpunkt + log-Leiter + C-14 · s3-6 c-Slider am W + Wannen-Widget · s4-1 Raumwinkel-Schrägbild + Würfel-Canvas für A1 · s4-2a Ellipsen-Münzen · s4-3a Polar-Quadranten-Widget + schiefes Gitter · s4-3b Projektionsvektor im Winkel-Labor.

---

## 5. TODO-Liste (zur Sichtung — bitte streichen/ergänzen, dann arbeite ich sie ab)

### Paket 1 — Fehler beheben (Severity A) — ✅ erledigt 2026-07-08 (CHANGELOG [85])

- [x] **T1** g1-1: Paritäts-Behauptung in A6-Lösung streichen/einschränken
- [x] **T2** g1-3: Fehlerblock-Satz «−(−2) = −2» korrigieren
- [x] **T3** g2-2b: Diskriminanten-Widget Fall D>0 — Zahlen auf D=1/√1/5±1 korrigieren (oder Beispiel x²−8x+12); zusätzlich A6-Rundung 1.75/−2.25
- [x] **T4** g4-2: Balkendiagramm-SVG auf die Achsenskala korrigieren (y=170−5·Wert)
- [x] **T5** g5-2a: Slider-Label «Basiswinkel α = β»; A6-Dachfläche 63.8/127.6 m²; `drawStativ()` in den load-Handler
- [x] **T6** g5-2b: A7-SVG reparieren (`<p>` raus, Drachen-Polygon rein)
- [x] **T7** g5-2c: Sehnen-Definition korrigieren; 377.79→377.78; `\quad`-Literal in Math-Block ziehen
- [x] **T8** g5-2d: Anim-5-Katheten-Labels und statische Startwerte korrigieren
- [x] **T9** g5-3: Flussdiagramm-SVG-Zeilen als Unicode-Klartext (LaTeX rendert in SVG-text nicht); A1-Klassifikation WWS→WSW
- [x] **T10** g5-5: Einstieg Text↔Code angleichen (Mitte/Start); Widget-Duplikate bei c=±1 dedupllizieren; Fehlerblock «(für −1<c<1)»
- [x] **T11** s2-2a: Mini-Check-Transfer Z.322 ersetzen (Gleichung mit echter Scheinlösung, z.B. 6/(x−2)=3x/(x−2))

### Paket 2 — Systematische Konsistenz (Sammel-Durchgänge) — ✅ erledigt 2026-07-08

- [x] **T12** 👁/💡-Rollover nachrüsten: g5-1 (3), g5-2b (5), g5-2d (5), g5-3 (6), g3-1 (3) — je «Worauf achten?»/«Erkenntnis»
- [x] **T13** A7-Pillen + Abschnitts-Kommentare: Pille zu A7 (g5-1, g5-2a, g5-4, g5-5, g4-1), A7-Blöcke vor den Zusammenfassungs-Kommentar, verrutschte/doppelte Kommentare glätten (g1-2, g5-2b, g5-2c, g5-4), Button-Texte angleichen (g5-4)
- [x] **T14** Terminologie-Entscheid + Angleichung (inkl. STYLEGUIDE-Eintrag und Glossar): **(a)** Definitionsmenge/Wertemenge ODER -bereich? **(b)** Probe vs. Kontrolle (LG 2 SP) **(c)** Streckfaktor **(d)** waagrecht **(e)** CHF **(f)** «Arithmetik/Algebra» (s1-2/s1-3 pt-bereich) **(g)** Zentriwinkel-Symbol g5-2c **(h)** Spannvektoren s4-3d — *Bitte bei (a) und (b) deine Präferenz markieren.*
- [x] **T15** chkNum-Bruch-Eingabe projektweit: «/» im Strip-Regex schonen + a/b-Parser (betrifft alle neueren Seiten); «e» in Zahleneingaben (4.4e11) schonen
- [x] **T16** Verweis-Glyphen: ↩ nur für Rückverweise; Vorwärtsverweise s4-1/s4-2a («wirst du behandeln») umformulieren

### Paket 3 — RLP-/Lernziel-Lücken schliessen (je kleiner Inhaltsblock)

- [ ] **T17** g1-2: Theorieblock Bruch-Grundoperationen
- [ ] **T18** g4-1: nominal vs. ordinal + 4. Mini-Check
- [ ] **T19** g4-2: Theorieblock manipulative Diagramme
- [ ] **T20** g4-3: Spannweite-Definition + Zusammenfassungs-Zeile
- [ ] **T21** g5-1: Stufen-/Wechselwinkel-Tab (oder Lernziel kürzen — bitte wählen)
- [ ] **T22** g5-2a: Umfang U=a+b+c (Formel, Tabelle, Teilaufgabe)
- [ ] **T23** g5-4: Kurzabschnitt Umkehroperationen (arcsin/arccos/arctan, Brücke 5.5) + Komplement-Zeile in Symmetrie-Tabelle + Bogenmass-Querverweis
- [ ] **T24** s3-3: Linearfaktor-Abspaltung (Polynomdivision oder Horner) + rechnerische Extrema Grad 2 + Ausblick-Deklaration
- [ ] **T25** s3-4a: Abschnitt/Aufgabe Sättigungsprozesse (beschränktes Wachstum)
- [ ] **T26** s3-2b: Umkehrung x⁻ⁿ ergänzen oder im rlp-hinweis deklarieren

### Paket 4 — Einzel-Mängel B (pro Seite, nach Sichtung) — ✅ erledigt 2026-07-09

- [x] **T27** g1-3: Startwert 650→1040; Querlink-Anker; (a+b)³-Verweis prüfen (s1-1/s1-2 existieren jetzt — ggf. präzise verlinken)
- [x] **T28** g1-4: toter Anker #typen→#hierarchie; «Komma verschieben»→«Dezimalpunkt verschieben»; Zoom-Objekte n:20/22
- [x] **T29** g2-1: A2-Platzhalter neutralisieren + numerischer Gleichungs-Vergleich statt String; a≠0-Zusatz
- [x] **T30** g2-2a: Lösungsfall-Nummerierung; Definition↔Mini-Check a≠0; Lead; ohm-root-Element (auch 2-2b/2-3); «Buchstaben-grösse»; A7 «lukrativer»
- [x] **T31** g2-2b: *einen*-Sternchen; «Zerfallsprozesse»-Beispiel ersetzen; 𝕃 vereinheitlichen; «Studierende»→«Lernende»; Velo-Caption
- [x] **T32** g2-3: Geraden-Label ins Canvas; Kino-Kontext
- [x] **T33** g3-1: \(\)-Fragment; b-Slider-Farbkopplung; Vertikaltest-Begriff; Ziel- vs. Wertebereich-Fussnote
- [x] **T34** g3-2: A3-Lösungswege; U+2212 im m=−1-Zweig; merksatz-Klasse
- [x] **T35** g3-3: **U+2212-Parser-Bug A2-Widget**; Wurfparabel clippen; «(auch: Lösungsformel)»
- [x] **T36** g4-0: Grammatik Z.781; 8000-Zahl neutralisieren; Boxplot-Ausreisser-Hinweis; «(oben)»; s-Formulierung (auch g4-3)
- [x] **T37** g4-1: Sie→du
- [x] **T38** g5-1: totes CSS (bauen oder entfernen — Vorschlag: Gut/Schlecht-Skizzen bauen, siehe T44)
- [x] **T39** g5-2b: Formeltabelle a=Grundseite/Drachen-Grössen; Drachen in Live-Klassifikation; NaN-Schutz Sehnenviereck; «Ein Drache»; Mini-Check-Etikett
- [x] **T40** g5-2c: «Wie aus der Animation oben»; Tangenteneigenschaft; Bogenmass-Merksatz; Segment-Legende φ>180°; «Stern-Schluss»-Klammer; Drag-Text Anim 1; Pi-Rekord-Halbsatz
- [x] **T41** g5-2d: Lernziele-Position; block-def zentrische Streckung; Strahlensatz-Fehlerblock auf S-Notation; Tick-Beschriftung
- [x] **T42** g5-3: «Vom einem»; WWS im Merksatz; Sinussatz-Slider-Clamp; A2.1-Endwert; sin-Bereich-Formulierung
- [x] **T43** g5-4: erkl-ek2-Satzbau; Schiff-Quadrant-Sonderfälle; ±kπ-Notation
- [x] **T44** g5-5: Fehlerblock-Satzbau; Intervallnotation; waagerecht; A4c-Rundungsvorgabe
- [x] **T45** s1-2/s1-3: h2-Anker-IDs; A1-Optionen mischen + Gesetz 5; fmt2 entfernen; a>0-Halbsatz; A5-Text/Target; sl-grp-Markup; Widget-Emoji
- [x] **T46** s2-1: Waage-Canvas-Geometrie (+ Rendercheck); A3b neue Gleichung; g2-2a/b-Links in Typen-Tabelle; waStep-Feedback
- [x] **T47** s2-2a: Uetliberg-Kontext; D-Zeile Beispiel 4/A7; «kann leer sein»; Substitution-Lernziel
- [x] **T48** s2-2b: A7-Toleranz; D-Herleitung Bsp. 6; A1-Distraktor
- [x] **T49** s2-2c: Randfall r=0; updateVZ x−0; Widget-Emoji; fmt2
- [x] **T50** s3-Serie Einzelpunkte: s3-1 Slider-Init (value 3→4, auch s3-6) + Galerie «acht»↔9 + Scheitelform-Zwischenschritt + «nicht lösbar»-Formulierung; s3-2a f:ℝ→ℝ + n-Symbolwechsel + Asymptoten-Def + Slider-max 8.5 + ≈560; s3-2b Konventions-Tipp ∛ + «knapp zweieinhalb Tage» + A6-Zwischenschritt; s3-3 «Sattel» + A4–A7-Plot-Hinweise; s3-4a A5/A6-Hinweis «grafisch/Probieren» + 1.3-Querlink + 0<a<1 + chkNum-1/5-Hinweis; s3-4b Phon→dB + Erkenntnis-Popup-Präzisierung + 0<a<1; s3-5 b/v-Farbkopplung + Wertebereich→Wertemenge + Symmetrieachsen-Erklärsatz
- [x] **T51** s4-Serie Einzelpunkte: s4-2a hinten-Set-Bug + Wiederholungs-Kennzeichnung Abschnitt 5 + Mantellinie-Halbsatz + Körperdiagonale-Klammer; s4-3b Beispiel 4 auf BA·BC; s4-3c A5-Text neu

### Paket 5 — Visualisierungen (nach deiner Priorisierung; Aufwand je ~½ Durchgang)

- [ ] **T52** Prio-1-Widgets (§4, Punkte 1–10) — bitte ankreuzen, welche gebaut werden sollen
- [ ] **T53** Prio-2-Widgets (§4, Liste) — Auswahl nach Sichtung
- [ ] **T54** s3-6 + s2-2a/c: Video-Platzhalter bei nächster Ressourcen-Session kuratieren (aus Audit-Nebenbefund)

---

## 6. Anhang — Kennzahlen

- 46 Seiten, ~57 000 Zeilen HTML; 23 GF (g1-1…g5-5), 23 SP (s1-1…s4-3d).
- Interaktivität: SP durchgehend 1–3 `widget`-Blöcke + 1–8 Canvases pro Seite; GF LG5 canvasreich (4–9), aber mit eigenem Anim-Muster; g4-Reihe nahezu ohne Interaktivität (0 Widgets, je 1 Canvas) — grösste Visualisierungs-Reserve.
- Mini-Checks: SP 4–5 pro Seite (4 Typen vollständig); GF LG4/LG5 teils 3 (ältere Konvention).
- Nachgerechnete Werte: >400, Fehlerquote ausserhalb der A-Liste: 0.
- Nav-Kette: 46/46 symmetrisch; doppelte h2-IDs: keine; tote lokale Links: keine (der einzige tote Anker ist g1-4→g1-1#typen, siehe T28).
