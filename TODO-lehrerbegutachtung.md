# Todo-Liste — Lehrerbegutachtungen TALS-Mathematik

**Quelle:** 27 Lehrerbegutachtungs-Dokumente (5 LG-Themenseiten-Reviews + 7 lange Druckdateien-Reviews g1-1…g2-2a + 13 kurze Druck-Reviews g3-1…g5-5 + 2 Sonder-Begutachtungen g2-2b/g2-3).
**Methodik:** Aus jedem Review die Empfehlungen extrahiert, anschliessend nach **Synergien** gebündelt — Patches, die in einer einzigen Iteration über mehrere Dateien laufen, stehen als „Welle". Einzel-Items bleiben pro Themenseite separat.
**Reihenfolge der Abarbeitung:** Prio 1 zwingend zuerst, dann Wellen nach Aufwand-zu-Nutzen, dann seitenspezifische Items.

**Konvention:**
- `[P1]…[P5]` = Priorität aus Quellreview übernommen (P1 = Sachfehler, P2 = Konsistenz/Skelett, P3 = didaktischer Ertrag, P4 = Politur, P5 = Stimmigkeit).
- `(LGx)` / `(g1-1 Druck)` / `(g3-2 Druck)` = Quell-Review.
- Wo Items aus mehreren Reviews zur selben Welle gehören, ist die Welle der primäre Anker; das einzelne Item nennt die Datei.

---

## Welle 0 — Sachfehler (zwingend, vor allem anderen)

Aus den fünf LG-Themenseiten-Reviews stammen exakt **5 Prio-1-Sachfehler**. Alle Druck-Reviews (lang + kurz) sind sachfrei — die Themenseiten haben in einigen Fällen Fehler, die in den Druckdateien bereits korrekt sind.

- [ ] **T0.1 (LG1, g1-3 A6)** Quadrat-Seitenlänge anpassen, sodass das Quadrat ins Rechteck `(x+4)×(x−1)` passt. Vorschlag: Quadratseite `(x−2)` m, Restfläche `(x+4)(x−1) − (x−2)²`. Alternativ Aufgabentext umformulieren („Werkstück + quadratischer Verschnitt aus grossem Holzbrett").
- [ ] **T0.2 (LG1, g1-2 A6)** „Wochenmittelwert" → „Tagesdurchschnitt aus drei Messungen" oder fünf bis sieben Werte angeben.
- [ ] **T0.3 (LG2, g2-2a A6 Lösung)** „je 60 Fr." → „je 70 CHF". Probe: `0.20·200 + 30 = 70`, `0.35·200 = 70`. **Hinweis Synergie:** das Druck-Material g2-2a hat den Fehler nicht (siehe g2-2a Druck-Review Fazit) — Druck als Wahrheits-Quelle nehmen.
- [ ] **T0.4 (LG2, g2-1 A6)** Widerspruch lösen zwischen Wurzelgleichung in A6 und Theorie-Hinweis „Wurzelgleichungen im Schwerpunktfach". Zwei Varianten: (a) Aufgabe ersetzen durch eine ohne Wurzel (z.B. „aus `x = 3` wurde durch Quadrieren `x² = 9` mit Lösungen `±3` — was bedeutet das?"); (b) Theorie-Hinweis lockern auf „im Grundlagenfach exemplarisch, vertieft im Schwerpunktfach". **Hinweis:** das Druck-Material g2-1 hat den Widerspruch nicht.
- [ ] **T0.5 (LG4, g4-0 Z. 790/794)** Quartil-Erklärtext bei n=26 korrigieren. Z. 790: „Q₁ = Mittel der Werte an Rang 7 und 8" → „Q₁ = Wert an Rang 7 (die untere Hälfte hat 13 Werte, also einen einzelnen mittleren Wert)". Z. 794 analog: „Q₃ = Wert an Rang 20 (= Rang 14 + 7)". Der JS-Code in Z. 886-905 ist korrekt — nur der Erklärtext muss angepasst werden.
- [ ] **T0.6 (LG5, g5-2c A7(c) Z. 899)** Sprinkler-Beispiel ersetzen: „bei 0°, 110° und 220° Drehung" → „bei 0°, 120° und 240°" (überlappungsfrei) oder den Klammer-Zusatz ganz weglassen. Lücke `[340°; 360°]` wird sonst nicht überdeckt.
- [ ] **T0.7 (LG5, g5-3 A1(b))** „Sinussatz (WSW)" präzisieren zu „WWS" oder neutral „Zwei Winkel und eine Seite — Sinussatz anwendbar".
- [ ] **T0.8 (LG5, g5-2d Z. 295)** „Gleichsinnige Abbildung" präzisieren: Gleichsinnigkeit gilt nur bei `k > 0`. Klammerzusatz zur Spiegelung bei `k < 0` separat erläutern, nicht als Unterfall der Gleichsinnigkeit.

---

## Welle A — Promath/SBFI/FTB-Verweis-Konsistenz (Find-Replace-Welle)

Wiederkehrender Befund über sieben Druck-Reviews: Promath-Verweis fehlt im Formelauszug bzw. ist inkonsistent zwischen Druckdateien. Reine Find-Replace-Operation. **Vorbild-Snippet (aus g1-1, g2-1):** `<div class="quelle">Ergänzung zur Formelsammlung Promath (SBFI). Notation gemäss FTB.</div>`

- [x] **TA.1 [P2]** Formelauszug **g1-2**: `quelle`-Div ergänzen.
- [x] **TA.2 [P2]** Formelauszug **g1-3**: `quelle`-Div ergänzen.
- [x] **TA.3 [P2]** Formelauszug **g1-4**: `quelle`-Div ergänzen. **Zusatz-Konsistenz prüfen:** entweder beide Druckseiten (Handout, Formelauszug) führen Tera/Pico oder beide nicht.
- [ ] **TA.4 [P4]** Formelauszug **g4-1** und Handout/Selbsttest g4-1: strategische Entscheidung — wenn FTB-Verankerung TALS-weit gewünscht, alle drei Dateien ergänzen mit knappem Footer-Satz „Begriffe in Anlehnung an SBFI-Rahmenlehrplan Mathematik §4.1 und Promath FTB §11" (LG4 hat wenig Notation, daher Verweis zur Begrifflichkeit).
- [x] **TA.5 [P4, druck-g5-3 / druck-g5-4 / druck-g5-5]** Formelauszug **g5-3**, **g5-4**, **g5-5**: Quellen-Footer aus g5-2d übernehmen („Quelle: Anlehnung an Formeln, Tabellen, Begriffe, Orell Füssli Lehrmittel."). Bei g5-3 ist die FTB-Referenz inhaltlich schon da als Tabellen-Überschrift „Notation (FTB)" — entweder Footer zusätzlich ergänzen oder als Vorbild für g5-4/g5-5 nehmen.
- [ ] **TA.6 [P5]** **Themenseiten allgemein** (alle 5 LG): einmaliger FTB-Hinweis in RLP-Header oder Footer („Notation nach FTB / Promath").

---

## Welle B — Anki-Intervall-Notation (Generator-Skript zentral)

Wiederkehrender Befund: US-Intervall-Format (`(a, b)`, `[a, ∞)`) statt Schweizer Format (`]a; b[`, `[a; ∞[`) in mehreren Anki-Decks. **Empfehlung:** Anki-Generator-Skript zentral anfassen, alle 22+ Decks regenerieren lassen, statt jedes Deck einzeln zu editieren.

- [x] **TB.1 [P2]** Generator-Skript: Find-Replace-Regeln für Intervall-Notation einbauen (`(x, y)` → `]x; y[`, `[x, y)` → `[x; y[`, `(x, y]` → `]x; y]`, `(-∞, y)` → `]-∞; y[` etc.).
- [x] **TB.2 [P2]** Konkret verifizierte Decks: **g1-2 (Karten 10, 11, 12)**, **g2-2a (Karten 10, 11)**, **g3-1 (Karten 10, 11)** — nach Regenerierung diese Karten als Smoke-Test sichten.
- [ ] **TB.3 [P5]** Anki-Deck-Namen systematisch auf Schema `TALS-Mathe G{X.Y} {Titel}` setzen. Aus den Reviews konkret nötig: **g1-1**, **g1-2**, **g1-3**, **g1-4**, **g2-1**, **g2-2a**. Wahrscheinlich auch g2-2b, g2-3, alle g3, g4, g5 — Smoke-Check bei allen.
- [x] **TB.4 [P3, g1-1 Anki Karten 7-10]** Listen-Items mit `<br>` trennen. Aktuell kleben „1. Klammern2. Potenzen…" und „a + b = b + aa · b = b · a" zusammen. Generator-Separator korrigieren.

---

## Welle C — Schreiblinien (`lin-mehr`) in Teste-dich-Selbst ergänzen

Wiederkehrender Befund: `<div class="lin-mehr">` fehlt im Selbsttest mehrerer Themen, obwohl in g1-1 vorbildlich vorhanden.

- [x] **TC.1 [P2, g1-2 Teste]** Nach jeder Aufgabe 2-3 Schreiblinien einfügen (analog g1-1).
- [x] **TC.2 [P2, g1-3 Teste]** dito.
- [x] **TC.3 [P2, g1-4 Teste]** dito.
- [x] **TC.4 (aus begutachtung-g2-3) [P3, g2-3 Teste]** Schreiblinien ergänzen (g2-2a und g2-2b haben 1–3 Linien je Aufgabe, g2-3 hat keine).
- [x] **TC.5 [P4, g1-1 Teste Aufg. 4]** Vier Linien für vier Teilaufgaben (a)-(d) statt zwei.

---

## Welle D — Footer `doc-fuss` Vereinheitlichung g2-3 ↔ g2-2

Aus der g2-3-Begutachtung: Footer `<footer class="doc-fuss">` fehlt durchgängig in allen fünf Druckseiten von g2-3, ist aber in allen acht von g2-2a und g2-2b vorhanden. Reine HTML-Konsistenz.

- [x] **TD.1** Footer-Block aus z.B. `downloads/.../g2-2a-lineare-gleichungen/handout.html` in alle fünf Dateien von `downloads/.../g2-3-lineare-gleichungssysteme/` ergänzen: `handout.html`, `formelauszug.html`, `teste-dich-selbst.html`, `aufgabenserie.html`, `zusatz-gauss-cramer.html`.

---

## Welle E — Download-Galerie-Reihenfolge (Anki ans Ende)

Aus g1-1 bis g1-4 Druck-Reviews: Galerie-Reihenfolge `Handout → Formelauszug → Anki → Teste-dich-Selbst → Aufgabenserie` widerspricht dem Lernpfad. Empfohlene Reihenfolge: `Handout → Formelauszug → Teste-dich-Selbst → Aufgabenserie → Anki`.

- [x] **TE.1 [P3-P5]** Reihenfolge umstellen in den Themenseiten **g1-1, g1-2, g1-3, g1-4**. Bei den anderen LGs Smoke-Test, ob das gleiche Muster vorliegt — falls ja, gleiche Umstellung in g2-1, g2-2a, g2-2b, g2-3, g3-1, g3-2, g3-3, g4-1, g4-2, g4-3 (+ g4-0), g5-1, g5-2a, g5-2b, g5-2c, g5-2d, g5-3, g5-4, g5-5.

---

## Welle F — A7-Aufgaben als „Vertiefung / Brücke zu …" markieren

Aus LG1 (Stilistik), LG2 und LG3: A7 ist auf vielen Seiten thematisch breiter als A1–A6, aber strukturell nicht abgehoben. Empfehlung: dezenter Banner oder Subtitel „Vertiefung" bzw. „Brücke zu …".

- [x] **TF.1 [P2, LG1]** Styleguide §4 abgleichen: entweder A1–A7 als Standard oder A7 explizit als optionale Vertiefung kennzeichnen. Dann Markierung auf allen vier LG1-Seiten konsistent setzen.
- [x] **TF.2 [P5, LG2]** Auf allen vier LG2-Seiten (g2-1, g2-2a, g2-2b, g2-3) A7 als „Vertiefung" oder „Brücke zu …" markieren.
- [x] **TF.3 [P5, LG3]** Auf allen drei LG3-Seiten (g3-1, g3-2, g3-3) A7 dito markieren.

---

## Welle G — Bidirektionale Quer-Verweise und FTB-Querverlinkung

Aus LG1, LG2, LG3, LG4 Übergreifend-Abschnitten: `<a class="quer">`-Verweise fehlen oft in der Rückrichtung. Im Detail:

- [ ] **TG.1 [P5, LG1]** Bidirektionale Quer-Verweise zwischen g1-1↔g1-4, g1-2↔g1-3, g1-3↔g1-4. Die `quer`-Spans gibt es in g1-3/g1-4 bereits in eine Richtung, fehlen aber zurück.
- [ ] **TG.2 [P5, LG2]** Hinzufügen: g2-1 ↔ g1-3 (Termumformungen/Distributiv), g2-2a → g1-3 (Klammern), g2-3 → g2-2a (Lösungsfälle).
- [ ] **TG.3 [P5, LG3]** Am Ende von g3-1 eine Brücken-Tabelle „Du kannst jetzt die zwei wichtigsten Funktionstypen vertiefen …" mit Link zu g3-2 und g3-3.
- [ ] **TG.4 [P3, LG4 g4-1]** Querverweise auf g4-2 und g4-3 nach Merkmalstypen-Tabelle („Welches Diagramm zu welchem Typ passt → 4.2; welche Masszahlen → 4.3").
- [ ] **TG.5 [P5, LG4]** Querverweise-Matrix vervollständigen zwischen allen vier LG4-Seiten (inkl. g4-0).
- [ ] **TG.6 [P5, LG5]** g5-3 → g5-4 und g5-4 → g5-5 explizit hinzufügen.
- [ ] **TG.7 [P2/P5, g2-1/g2-2a]** Anker `#spezialfaelle` in g2-2a-Themenseite verifizieren (Querverweis aus g2-1 Lösung 2 zeigt darauf).

---

## Welle H — `block-tipp` 💡 systematisch einführen

Aus LG1 (g1-1, g1-2), LG2, LG3, LG4 (g4-2), LG5 (g5-2a, g5-2c, g5-4) Übergreifend: `block-tipp 💡` ist auf einigen Seiten vorhanden, auf anderen nicht — diese Stilistik-Inkonsistenz wirkt subjektiv wie „weniger durchdacht". Vorschläge pro Seite:

- [ ] **TH.1 [P2, LG1 g1-1]** Tipp „Bei langen Termen erst die Hauptoperation finden, dann arbeiten".
- [ ] **TH.2 [P2, LG1 g1-2]** Tipp „Bei Vergleich von Brüchen Dezimal-Vergleich oder Hauptnenner".
- [ ] **TH.3 [P3, LG2]** Mindestens je einen `block-tipp` auf allen vier LG2-Seiten (g2-1, g2-2a, g2-2b, g2-3) an natürlichen Stellen — Strategie- oder Werkzeug-Hinweise.
- [ ] **TH.4 [P3, LG3]** Mindestens je einen `block-tipp` auf g3-1, g3-2, g3-3.
- [ ] **TH.5 [P2, LG4 g4-2]** Mindestens einen `block-tipp` einbauen — natürlicher Platz vor/nach der Datentyp→Diagramm-Entscheidungstabelle (Z. 480).
- [ ] **TH.6 [P3, LG5]** Je 2-3 `block-tipp` auf g5-2a, g5-2c, g5-4.

---

## Welle I — STYLEGUIDE-Klassen-Hygiene

Wiederkehrend: Eigenkreations-Klassen oder Symbol-Inkonsistenzen (siehe COLLABORATION §3.6).

- [x] **TI.1 [P2, LG3 g3-1]** 5× `💡 Beispiel` (Z. 255, 439, 455, 528, 543) zu `🟢 Beispiel` ändern (`💡` ist für `block-tipp` reserviert). **Erledigt** — g3-1 enthält keine `💡 Beispiel`-Stellen mehr (verifiziert 2026-05-27 im Konsistenz-Sweep).
- [ ] **TI.2 [P2, LG3 g3-2 und g3-3]** `block-beweis`-Blöcke für Aufstell-Beispiele (g3-2 Z. 259, g3-3 Z. 420, 427, 434) zu `block-def` (📘) oder `block-bsp` (🟢) ändern — Konstruktionsanleitungen, keine Beweise.
- [ ] **TI.3 [P2, LG3 g3-3 Z. 207-224]** `📝`-Notations-Hinweis-Block neu strukturieren: entweder als `block-tipp` mit `💡` oder Titel-Symbol auf `📘` ändern. `📝` ist nicht im STYLEGUIDE-Inventar.
- [ ] **TI.4 [P2, LG3 g3-3 Z. 281]** `🟢 Hinweis zur Linearfaktorform` → entweder Titel zu `🟢 Beispiel — ...` oder Block zu `block-tipp 💡 Hinweis`.
- [ ] **TI.5 [P2, LG4 g4-0 Z. 486]** `📌 Wann welche Kennzahl?` → `block-tipp 💡` oder Symbol auf `⭐ Merksatz`.
- [x] **TI.6 [P2, LG4 g4-3 Z. 303]** `🎯 Merksatz — Robustheit` → entweder auf `⭐` vereinheitlichen oder zu `block-tipp 💡` umstellen. **Erledigt** — Titel ist `⭐ Merksatz — Robustheit` (g4-3 Z. 304, verifiziert 2026-05-27).
- [ ] **TI.7 [P2, LG4 g4-0 Z. 480-483]** „Plausibilitätsprüfung der Masszahlen"-Box mit eigenem `pl-titel` → `block-def` mit `📘`-Titel.
- [ ] **TI.8 [P2, LG4 g4-1 Z. 299]** Ersten Merksatz zu `block-tipp 💡` umwandeln; nur den abschliessenden (Z. 474) als `⭐ Merksatz` belassen.
- [ ] **TI.9 [P2, LG5 g5-2a Z. 254, 258, 308, 445]** Vier Block-Klassen ohne `block`-Präfix korrigieren: auf `<div class="block block-def">` bzw. `<div class="block block-merksatz">` umschreiben.
- [ ] **TI.10 [P2, LG5 g5-2a Z. 308, 445]** `block-merksatz`-Titel mit `⭐ Innenwinkelsumme` und `⭐ Flächenformel` versehen statt der inline-`<strong>Satz.</strong>`-Form.
- [ ] **TI.11 [P3, druck-g5-2d]** CSS-Klasse `aufg-block` ist nirgends definiert. Zwei Wege: (a) durch `block block-aufg` ersetzen + Lösung in `block-bsp` (Falt-Lösungen gehen verloren); (b) `aufg-block` + `.aufg-block details summary`-Styling in `print.css` ergänzen und Format ins STYLEGUIDE aufnehmen. Variante (b) didaktisch attraktiver.
- [ ] **TI.12 [P5, LG5]** Eigenkreations-Klassen in STYLEGUIDE übernehmen oder durch Standard-Klassen ersetzen.

---

## Welle J — Notations-Vereinheitlichungen

- [x] **TJ.1 [P2, LG5 g5-5 A4(1) und A4(2)]** `\mathbb{L} = \{\,\}` durch `\emptyset` ersetzen (Standard für leere Lösungsmenge).
- [x] **TJ.2 [P2, LG5 g5-4 Z. 533]** Definitionsmenge des Tangens `{π/2 ± kπ}` → `{π/2 + kπ : k ∈ ℤ}`.
- [x] **TJ.3 [P2, LG2 g2-2a Definitionstabelle]** „Standardlösung" → „Lösungsformel" oder „aufgelöste Form" (Schweizer BM-Konvention).
- [x] **TJ.4 [P2, LG2 g2-1]** „Definitionsmenge" und „Definitionsbereich" konsistent — bei Gleichungen „Definitionsmenge", bei Funktionen „Definitionsbereich".
- [x] **TJ.5 [P2, LG2 g2-2a Z. 245]** „kgV" → „Hauptnenner" (konsistent zu g1-2) oder Klammer-Erklärung.
- [x] **TJ.6 [P2, LG2 g2-1 Z. 277 und 348-350]** Doppelter Fehler-Block „Multiplikation mit einem Term" — einen streichen.
- [x] **TJ.7 [P2, LG2 g2-1 A2(d)]** Variablen `a, b` → `x, y` (konsistent zu g2-3).
- [ ] **TJ.8 [P5, g2-1 Druck]** Inkonsistenz Handout (`ℒ = ℝ` für Identität) vs. Formelauszug (`ℒ = 𝔾`) — einheitliche Konvention.
- [x] **TJ.9 (aus begutachtung-g2-2b) [P3, g2-2b Lösung 3]** Vieta-Probe verwendet $p = b/a = 0.5$ mit „$-6/2$" für $q$ — mischt $p,q$-Konvention mit $c/a$. Konsequente Schreibweise: entweder „erst normieren, dann Vieta" oder „verallgemeinertes Vieta: $x_1 \cdot x_2 = c/a$, $x_1 + x_2 = -b/a$".

---

## Welle K — Lösungsweg-Granularität & Marginalien (didaktische Tiefe)

Querschnitt aus mehreren Reviews: Lösungen oft sehr kompakt, Zwischenschritte fehlen, Vorausgriff-Marginalien sparsam.

### LG1 / Druck g1-x
- [x] **TK.1 [P3, LG1 g1-2]** Eigenständige Mini-Sektion „Doppelminus-Regel" mit drei Beispielen (Sek-I-Lücke, in g1-3 vorausgesetzt).
- [x] **TK.2 [P3, LG1 g1-3 A3(c)]** Faktorisierten Lösungsweg als Alternative ergänzen: `(x−y)·((x+y)−(x−y)) = 2y(x−y)`.
- [x] **TK.3 [P3, LG1 g1-3 A7]** Zweiten falschen Slogan einbauen (statt einer korrekten + einer falschen), z.B. „`√(a²+b²) = a+b`".
- [x] **TK.4 [P3, g1-1 Druck Aufgabenserie A1]** Distributivgesetz explizit benennen, wenn `28+12 = 40` zusammengefasst wird.
- [x] **TK.5 [P3, g1-1 Druck Aufgabenserie A2(c)]** Linearen-Funktions-Aspekt erwähnen.
- [x] **TK.6 [P3, g1-1 Druck Aufgabenserie A6(a)]** Vorausgriff-Marginalie zu Funktionen in 3.x.
- [x] **TK.7 [P3, g1-1 Druck Teste Aufg. 6(c)]** Distributiv-über-Differenz mit Zwischenschritt `b − c = b + (−c)`.
- [x] **TK.8 [P3, g1-1 Druck Handout Abschnitt 4]** „Konstante 3" → „Koeffizient 3".
- [x] **TK.9 [P3, g1-2 Druck Handout Abschnitt 4]** „bei Division gilt die gleiche Regel" + zwei Division-Beispiele `(-12)/(-4) = +3`, `(-12)/(+4) = -3`.
- [x] **TK.10 [P3, g1-2 Druck Teste 9(c)]** Vorzeichen-Falle expliziter: „`-3² = -(3²) = -9`; `(-3)² = (-3)·(-3) = +9`; Summe: 0".
- [x] **TK.11 [P3, g1-3 Druck Aufgabenserie A2]** **WICHTIG**: Bremsweg-Disclaimer als Marginalie: „Achtung: dies ist eine vereinfachte Modellformel, nicht die offizielle Schweizer Verkehrs-Faustformel. Offiziell: Bremsweg = `(v/10)²`, Reaktionsweg = `(v/10)·3`." Schüler könnten sonst falsche Verkehrsregel lernen.
- [x] **TK.12 [P3, g1-3 Druck Teste Aufg. 8(c)]** Marginalie zur Mitternachtsformel: „Vollständige Faktorisierung: `3x(x-1)(2x-1)` (wird in 2.2 behandelt)".
- [x] **TK.13 [P3, g1-3 Druck Handout Abschnitt 7 Falle 1]** Zahlen-Beispiel ergänzen: „Für `a=5, b=3`: `-(5-3) = -2`. Falsch: `-5-3 = -8`. Richtig: `-5+3 = -2`."
- [x] **TK.14 [P4, LG1 g1-4]** Liste der Faustwerte für Quadratwurzeln auf `√2, √3, √5, √7, √10` erweitern.
- [x] **TK.15 [P3, g1-4 Druck Handout Abschnitt 5 W4]** `block-fehler`-Block zur Vorzeichen-Falle: „`√(a²) = |a|`, nicht `a`!".

### LG2 / Druck g2-x
- [x] **TK.16 [P3, LG2 g2-2b A1]** Vieta-Probe: „p = −5, also −p = 5" — Zwischenrechnung explizit.
- [x] **TK.17 [P3, LG2 g2-2b A6 Anna-Velo]** Umformungs-Schritte von Bruchgleichung zur quadratischen Gleichung explizit ausschreiben (`24(v−4) + 24v = 3v(v−4) → … → v² − 20v + 32 = 0`).
- [x] **TK.18 [P3, LG2 g2-3 A6 Mischung]** Marginalie zur „Massenbilanz" — zweite Gleichung pädagogisch begründen.
- [x] **TK.19 [P3, LG2 g2-3 A5]** Hinweis „Subtrahiere G3 von G1" weglassen oder als optionalen Klick (mehr Eigenleistung).
- [x] **TK.20 [P3, LG2 g2-3 A7]** „maximal bauen" → „damit alle drei Materialien vollständig verbraucht werden" (Begriffsklarheit).
- [x] **TK.21 [P3, LG2 g2-1]** Eigener Theorie-Block „Ungleichungen formulieren" mit 2–3 Werkstatt-Beispielen (RLP 2.1).
- [x] **TK.22 [P4, LG2 g2-2a]** Zweites Parameter-Diskussions-Beispiel das Fall 2 (leere Lösungsmenge) zeigt.
- [x] **TK.23 [P4, LG2 g2-2a]** A8 (kurz) als reine Ungleichungs-Aufgabe mit Zeichenkippung.
- [x] **TK.24 [P4, LG2 g2-3]** 3×3-Beispiel mit Geraden-Lösung („unterbestimmt").
- [x] **TK.25 [P4, LG2 g2-2b A6]** Marginalie „quadratische Gleichung kennt den Sachzusammenhang nicht — Sachkontext sortiert die unsinnige Lösung aus".
- [x] **TK.26 [P4, LG2 g2-2b A7]** Goldener-Schnitt-Klarstellung: `φ_2 ≈ −1.618` (Lösung) ≠ Goldene Zahl `Φ = (1+√5)/2 ≈ 1.618`.
- [x] **TK.27 [P3, g2-1 Druck Aufgabenserie A4]** SIA-358-Bezug expliziter (Schrittmass-Formel `2s + a = 63cm`).
- [x] **TK.28 [P3, g2-1 Druck Selbsttest A12]** Bedingung `r(x) ≥ 0` als zweite Erkennungsmethode für Scheinlösung.
- [x] **TK.29 [P3, g2-1 Druck Selbsttest A8]** Marginalie zur Vorzeichen-Regel bei Division durch −1.
- [x] **TK.30 [P3, g2-1 Druck Formelauszug Abschnitt 6]** 4-Schritt-Ablauf der Probe ergänzen.
- [x] **TK.31 [P3, g2-2a Druck]** Mehrere Lösungs-Zwischenschritte explizit: A4 Klammer-Auflösung, A11 Faktorisierung `(k-2)·x = (k-2)(k+2)`, Aufgabenserie A1 Spannungsteiler.

### LG3 / Druck g3-x
- [x] **TK.32 [P3, LG3 g3-2 A3(e)]** Punkt `P(0|4)` durch `P(2|10)` ersetzen, sodass parallele Gerade echte Rechnung erfordert.
- [x] **TK.33 [P3, LG3 g3-2 A6 Fahrenheit]** Lösung um Steigungsschritt `m = (212-32)/100 = 1.8` ergänzen.
- [x] **TK.34 [P3, LG3 g3-2 A4 und A5]** Lösungen detaillierter mit benannten Zwischenwerten.
- [x] **TK.35 [P3, LG3 g3-3 A4]** `a = -4/25` als exakten Bruch zeigen, dann Dezimalwert `-0.16`.
- [x] **TK.36 [P3, LG3 g3-3 A5 Umsatz]** Antwort um Stückzahl ergänzen: „Bei Preis 22.50 CHF werden 90 Stück verkauft, Umsatz 2025 CHF".
- [x] **TK.37 [P3, LG3 g3-3 A6 Brücke]** Marginalie „Die Bogenfüsse liegen auf der x-Achse, also sind `x=0` und `x=20` Nullstellen → Linearfaktorform geeignet".
- [x] **TK.38 [P3, LG3 g3-3 A7 Hängebrücke]** Brücken-Bemerkung „A6 und A7 lösen ähnliche Aufgaben mit unterschiedlichen Formen; die Wahl hängt von den gegebenen Informationen ab".
- [x] **TK.39 [P3, LG3 g3-1 A6(c)]** Marginalie zur Definitionsbereich-Reflexion „`[0;25]` vs. `[0;25[`".
- [x] **TK.40 [P3, LG3 g3-1 A7]** Präziser: „über 5 GB ist B günstiger, bei genau 5 GB sind beide gleich teuer" (statt „ab 5 GB").
- [x] **TK.41 [P4, druck-g3-2]** A2a: Rundungs-Drift „1.39 h ≈ 1 h 23 min" präzisieren, optional „≈ 1 h 23 min 20 s" oder „1 h 23 min (gerundet auf ganze Minuten)".
- [x] **TK.42 [P4, druck-g3-3]** A6(b): pharmakologische Standard-Termini „MEC" und „MTC" optional ergänzen.
- [x] **TK.43 [P4, druck-g3-3]** A6(b) Mitternachtsformel-Darstellung mit positivem Nenner umformulieren (`c_{1,2} = 40 ∓ sqrt(1200)` statt mit `-1` als Nenner).
- [x] **TK.43a [P5, druck-g3-1]** A6(c) Sensor B Lösung „Ablesegenauigkeit ist bei B daher in der Regel besser" optional präzisieren zu „Bei gleicher Spannungs-Anzeige-Auflösung ist Sensor B daher genauer" (Empfindlichkeit ≠ Ablesegenauigkeit). Explizit als optional markiert.

### LG4 / Druck g4-x
- [x] **TK.44 [P3, LG4 g4-3 KRITISCH]** **Excel-Quartil-Diskrepanz** adressieren: `block-tipp` oder `block-fehler` nach QUARTILE.INKL-Tabelle (Z. 272): „Excel `QUARTILE.INKL` verwendet lineare Interpolation, die hier gelernte Tukey-Methode rechnet nach Median-der-Hälften. Bei kleinen Stichproben können beide unterschiedliche Werte liefern."
- [x] **TK.45 [P3, LG4 g4-2 A3 Lösung]** Histogramm in der Lösung als SVG ergänzen (analog A4 Boxplot).
- [x] **TK.46 [P3, LG4 g4-2 A2 Klasseneinteilung]** Marginalie „letzte Klasse beidseitig geschlossen, damit Maximalwert mitgezählt wird".
- [x] **TK.47 [P3, LG4 g4-3 A1 Lösung]** Marginalie zur Excel-`QUARTILE.INKL`-Variante.
- [x] **TK.48 [P3, LG4 g4-3 A6 Eigene Daten]** Konkrete Mini-Beispiel-Lösung mit fiktivem Datensatz.
- [x] **TK.49 [P3, LG4 g4-3]** „Klasse A / Klasse B / Klasse X / Klasse Y" konsolidieren — durchgehende Wiederverwendung oder klare Differenzierung.
- [x] **TK.50 [P3, LG4 g4-1 A2(1) Schuhgrösse]** Entweder eindeutigeres diskretes Beispiel (z.B. „Anzahl Sprachen") oder didaktische Grauzone explizit thematisieren.
- [x] **TK.51 [P3, druck-g4-2 Befund 1]** Whisker-Definition: kurze Tukey-Erweiterung in g4-2 Handout Z. 66 oder g4-3 Handout Z. 105: „In Excel u.a. werden Whisker oft bis zu Datenpunkten innerhalb 1.5·QD gezogen — alles darüber heisst Ausreisser und wird als Punkt eingezeichnet."
- [x] **TK.52 [P4, druck-g4-3 Befund 1]** Häufige-Fehler-Block im Handout g4-3 ergänzen (analog g4-1 und g4-2): n vs. n−1 in Std.abw., Median-Sortieren, Tukey vs. INKL, Mittelwert von kategorialen Daten, Std.abw. = 0.
- [x] **TK.53 [P4, druck-g4-3 Befund 3]** Modus „multimodal"-Begriff im Handout/Formelauszug Z. 48: „Bei mehreren Werten mit gleicher Maximalhäufigkeit spricht man von *mehrmodalen* / *multimodalen* Verteilungen".
- [x] **TK.54 [P4, druck-g4-3 Befund 4]** A5(b) Lösung: expliziten Schritt „Mittelwert > Median → langer Schwanz nach rechts" zeigen.
- [x] **TK.55 [P4, druck-g4-2 Befund 4]** A4(b) Lösung sauberer trennen: Korrelation ≠ Kausalität explizit von individuellen Unterschieden differenzieren.
- [x] **TK.56 [P4, druck-g4-1 Befund 1]** `KKLEINSTE(A:A;ZEILE())`-Trick im Handout als Tipp-Box auslagern, im Formelauszug nur Kernform — Mehrfach-Erklärung vermeiden.

### LG5 / Druck g5-x
- [x] **TK.57 [P3, LG5 g5-2c A3]** „Umkreisradius R des Sechsecks" durch klare 30-60-90-Argumentation ersetzen.
- [x] **TK.58 [P3, LG5 g5-2b A2(4)]** Marginalie zur inklusiven Trapez-Definition.
- [x] **TK.59 [P3, LG5 g5-4]** Symmetrie-Tabelle um `−α`-Beziehung erweitern: `sin(−α) = −sin α`, `cos(−α) = cos α`, `tan(−α) = −tan α`.
- [x] **TK.60 [P3, LG5 g5-4 Tangens-Erklärtext]** Erwähnen, dass in Q II und Q III die rückwärtige Verlängerung des Strahls OP auf die rechte Tangente nötig ist.
- [x] **TK.61 [P3, LG5 g5-5 Tangens-Lösungsschema Z. 249-258]** Klarstellen, dass im Hauptintervall [0°; 360°[ zwei Lösungen auftreten (Taschenrechner-Wert und +180°).
- [x] **TK.62 [P3, LG5 g5-3 Cosinussatz-Theorie]** Vorzeichen-Anmerkung für stumpfe Winkel (cos α < 0) ergänzen.
- [x] **TK.63 [P3, LG5 g5-2a A6 und g5-2c A5(2)]** Als „mit Vorgriff auf 5.3" markieren oder ohne Trigonometrie umformulieren.
- [x] **TK.64 [P4, druck-g5-2a]** A5(b) Probe: Wert auf 499.3 angleichen (statt 499.5 mit gerundetem 33.3 cm Zwischenwert) oder „mit Rundungstoleranz" annotieren.
- [x] **TK.65 [P4, druck-g5-2c]** A1: „rund 16 %" in Klammer den genauen Wert 15.5 % anfügen.
- [x] **TK.66 [P4, druck-g5-2d Befund 2]** Selbsttest L15 (`k = 0`): Lösung umformulieren als zwei Schritte „Der Fall k = 0 ist als Streckfaktor definitionsgemäss ausgeschlossen … Hätte man dennoch k = 0 formal eingesetzt, würde jede Figur auf den Punkt Z degenerieren."
- [x] **TK.67 [P4, druck-g5-3]** A2 (Bergbahn): Pythagoras-Probe-Wert auf 1144.7 m korrigieren oder Toleranz-Anmerkung „Differenz zur Cosinus-Rechnung von 0.2 m entsteht durch Rundung von α auf 17.5°".

---

## Welle L — Aufgaben-Politur & Lerner-Erlebnis

Kleinere Verbesserungen pro Seite, gebündelt nach LG.

- [x] **TL.1 [P4, LG1 g1-1 Tabelle „Begriffe"]** „Term" als ersten Eintrag.
- [x] **TL.2 [P4, LG1 g1-1 A3(4)]** Vorgriff-Vermerk auf Kap. 1.4 (Wurzel-Gesetze) oder Beispiel mit Potenzen.
- [x] **TL.3 [P4, LG1 g1-2 A7]** Tipp im Aufgabentext streichen (verrät die Pointe).
- [x] **TL.4 [P4, LG1 g1-2 A3(5)/(6)]** Endwert isoliert sichtbar (Format-Konsistenz zu A3(1)-(4)).
- [x] **TL.5 [P4, LG1 g1-4 A7 Avogadro]** Redundante Doppel-Erklärung zusammenfassen.
- [x] **TL.6 [P4, LG1 g1-4 A5(d) und A6]** Hierarchie/Exponenten-Vorzeichen-Marginalien in Lösungen.
- [x] **TL.7 [P4, LG1 g1-1 A7]** Substanziell andere Übung statt Variation des Einstiegs.
- [x] **TL.8 [P3-P4, LG3 g3-1 A3 Vertikaltest]** Interaktive ✓/✗-Buttons statt nur Lösungs-Toggle.
- [x] **TL.9 [P3-P4, LG3 g3-2 A4, A5, A6]** Eingabe-Prüfung ergänzen (Konsistenz zu A3 und g3-3 A3).
- [x] **TL.10 [P3-P4, LG3 g3-3 Anwendungs-Tabelle Z. 357-394]** Spalte „Wann besonders gut" (analog g2-3).
- [x] **TL.11 [P4, LG3 g3-1 A2(c)]** `1/√x` als „Vertiefung" markieren oder durch reine Bruch-Aufgabe ersetzen.
- [x] **TL.12 [P4, LG3 g3-3 Linearfaktorform D<0]** Notiz „falls D<0: Linearfaktorform existiert nicht in ℝ" auch im Live-Box-Bereich.
- [x] **TL.13 [P4, LG3 g3-3 Diskriminanten-Beispiele]** Konkrete Zahlenbeispiele für drei Fälle (D=1, D=0, D=-3) statt nur Klick-Karten.
- [x] **TL.14 [P4, LG4 g4-1 A6]** Eigene-Mini-Erhebung Beispiel-Lösung vollständiger.
- [x] **TL.15 [P4, LG4 g4-3 A4(d)]** Alternative kompaktere Formel diskutieren.
- [x] **TL.16 [P4, LG4 g4-2 A5(3)]** „Heteroskedastizität" optional als Marginalie.
- [x] **TL.17 [P4, LG4 g4-0]** Marginalie am Anfang „Spielwiese — Theorie und Aufgaben in 4.1, 4.2, 4.3" + lange Tabellenkalkulations-Box aufteilen.
- [x] **TL.18 [P4, LG4 g4-0 Z. 702-703]** Internen Entwicklungs-Kommentar entfernen.
- [x] **TL.19 [P4, LG5 g5-2a A6 Dachgiebel]** Neigungswinkel-Frage durch eine ohne arctan ersetzen oder „Vorgriff" markieren.
- [x] **TL.20 [P4, LG5 g5-2b A7 Drachen]** SVG-Skizze der Diagonalen-Anordnung.
- [x] **TL.21 [P4, LG5 g5-2d A4 (WW)]** Erweiterung um Kontrast-Fall (sss mit 3-4-5 und 6-8-10).
- [x] **TL.22 [P4, LG5 g5-3 A6c Goldenes Dreieck]** Marginalie zum Goldenen Schnitt `φ = (1+√5)/2`.
- [x] **TL.23 [P4, LG5 g5-3 Strategie-Übersicht]** Flussdiagramm-SVG.
- [x] **TL.24 [P4, LG5 g5-4 A7 Tagestemperatur]** Sinuskurve-SVG.
- [x] **TL.25 [P4, LG5 g5-5 A7]** Durch konzeptuell andere Anwendung ersetzen (Mondphase, Wassertiefe, Schwingung) — aktuell zu ähnlich zu A6.
- [x] **TL.26 [P4, LG5 g5-1 A6]** Als „Praxis-Projekt" kennzeichnen.
- [x] **TL.27 [P4, LG5 g5-1 A7 Fahnenstange]** Marginalie „Dieses ist der Strahlensatz, formal in 5.2d".
- [x] **TL.28 [P4, LG5 g5-2a]** Innenwinkelsumme-Beweis SVG: Wechselwinkel-Paare farblich markieren.
- [x] **TL.29 [P4, druck-g5-1 Befund 1]** Aufgabe 4 Titel Z. 52 von „Skizze einer Anwendung" auf „🟠 Aufgabe 4 — Wendeltreppe" angleichen.
- [x] **TL.30 [P3, druck-g5-2c]** Aufgabenstruktur auf LG5-Standard umstellen: alle 6 Aufgaben als `block-aufg` zuerst, dann `<h2>Lösungen</h2>` mit `block-bsp`-Lösungen. Alternativ: Lösungen in `<details>`-Falt-Container.

### Druck Aufgaben-Politur (LG1-Druck, LG2-Druck)
- [x] **TL.31 [P3, g1-2 Druck Aufgabenserie 2]** Schweizer 5-Rappen-Rundung-Marginalie „In der Praxis: 34.15 Fr".
- [x] **TL.32 [P3, g1-2 Druck Teste]** Aufgaben-Titel ergänzen (analog g1-1, `<span class="aufg-titel">…</span>`).
- [x] **TL.33 [P3, g1-2 Druck Aufg. 11]** Sortierung Lösung ausführlicher: „dezimal: `-3/4 = -0.75`, `-2/3 ≈ -0.667`".
- [x] **TL.34 [P3, g1-2 Druck Handout Bruch-Dezimal-Tabelle]** `1/4`, `1/8`, `2/5`, `-3/4` ergänzen.
- [x] **TL.35 [P4, g1-2 Druck Anki 17]** Grenzfall „bei genau 5" mit kaufmännischer vs. wissenschaftlicher Rundung.
- [x] **TL.36 [P4, g1-2 Druck Aufgabenserie 1(c), 3, 4, 5, 6]** Diverse Marginalien (Idealisierung, Toleranz, Tiefststand≠Endbestand, Massstab-Faustregel, Konzentration vs. Volumen).
- [x] **TL.37 [P4, g1-2 Druck Teste 12]** Logistik-Bezug der Beträge.
- [x] **TL.38 [P4, g1-2 Druck Anki 1-6]** Pro Definition ein konkretes Zahlen-Beispiel.
- [x] **TL.39 [P4, g1-2 Druck Anki 22]** Explizite Zwei-Lösungen: „±√2: zwei Lösungen, beide irrational".
- [x] **TL.40 [P5, g1-2 Druck]** Konvention „0 ∈ ℕ" in Aufg. 1-Lösung explizit benennen.
- [x] **TL.41 [P5, g1-2 Druck]** Schwierigkeitsmarkierung Gruppe „Betrag/Ordnung" auf ●●○ herunterstufen.
- [x] **TL.42 [P5, g1-2 Druck Anki 7]** Intervall-Marginalie „2.5 zu gross" — Begründung explizit.
- [x] **TL.43 [P5, g1-2 Druck Formelauszug]** Marginalie zur Schweizer vs. US-Konvention bei Intervallen.
- [x] **TL.44 [P3, g1-3 Druck Teste 5(c)]** Zwischenschritt `(a+b)(a+b+c) = a(a+b+c) + b(a+b+c) = …`.
- [x] **TL.45 [P3, g1-3 Druck Teste 12]** Didaktische Schlussfolgerung: „Strategie: symbolisch vereinfachen, dann einsetzen".
- [x] **TL.46 [P3, g1-3 Druck Aufgabenserie 1]** SVG-Grafik des Quadrats mit Rand-Streifen.
- [x] **TL.47 [P3, g1-3 Druck Aufgabenserie 4]** „Distributivgesetz rückwärts: `4rx + 4r² = 4r(x+r)`" benennen.
- [x] **TL.48 [P3, g1-3 Druck Aufgabenserie 6]** Modell-Disclaimer „Vereinfachung — in 3.4 realistischeres Exponentialmodell".
- [x] **TL.49 [P3, g1-3 Druck Handout Abschnitt 6]** Strategie-Reihenfolge beim Faktorisieren (analog Anki-Karte 21).
- [x] **TL.50 [P3, g1-3 Druck Handout Abschnitt 5]** Herleitung-Marginalie „Binomische Formeln folgen direkt aus Klammerregel 4".
- [x] **TL.51 [P4, g1-3 Druck Anki 11, 14, 19, 22, 23 + neue Polynom-Karten]** Diverse Anki-Verbesserungen (Vorzeichen, ggT, Beispielzahlen, Polynom-Begriffe).
- [x] **TL.52 [P4, g1-3 Druck Aufgabenserie 3]** Kirchhoff-Mini-Marginalie für Schüler ohne ET-Vorwissen.
- [x] **TL.53 [P5, g1-3 Druck]** Schwierigkeitsmarkierung Gruppe „Binomische Formeln" differenzieren — Aufg. 6 auf ●●○.
- [x] **TL.54 [P5, g1-3 Druck]** Formelauszug Tabellen-Reihenfolge: Polynom-Begriffe vor Faktorisieren.
- [x] **TL.55 [P5, g1-3 Druck]** Handout/Formelauszug Beispiel-Polynom konsistent (z.B. immer `5x³ - 2x² + 7x - 4`).
- [x] **TL.56 [P2, g1-4 Druck Handout/Formelauszug]** **SI-Vorsätze-Tabelle ergänzen**: Centi (c, 10⁻²), Deci (d, 10⁻¹), Hekto (h, 10²) mit Schweizer Beispielen (cm, dl, hPa). Wichtige Stoff-Ergänzung. + Konsistenz Handout↔Formelauszug.
- [x] **TL.57 [P2, g1-4 Druck Anki]** 6-10 neue Karten zu SI-Vorsätzen („G = ?", „µ = ?", „c → ?", „cm in m → ?", „1 hPa → ? Pa").
- [x] **TL.58 [P3-P4, g1-4 Druck Aufgabenserie 1-6]** Diverse Marginalien (Dezibel-Brücke→LG3, Flächen-Umrechnung 1 cm²=10⁻⁴ m², `U_max=U_eff·√2`, Lichtlaufzeit, MHz=Mio. Zyklen, Raumgrösse, Bit-Grenze=Wellenlänge).
- [x] **TL.59 [P3, g1-4 Druck Teste 7(c)]** Vorzeichen-Begründung „per Definition ist `√` die nicht-negative Zahl".
- [x] **TL.60 [P3, g1-4 Druck Teste 12]** Drei-Gesetze-Marginalie P3, P2, P1 explizit.
- [x] **TL.61 [P4, g1-4 Druck Anki 7, 17, 23/24]** Avogadro-Bezug, Dezimal-Wurzel-Falle `√0.25=0.5`, Erweiterungs-Begründung.
- [x] **TL.62 [P4, g1-4 Druck Reihenfolge Aufgabenserie]** „Von gross zu klein" (Astronomie → Bauwesen → ET → Akustik → Optik → Mikroelektronik).
- [x] **TL.63 [P5, g1-4 Druck Formelauszug]** Quadratzahlen unmittelbar vor Wurzelgesetze. Wissenschaftliche-Notation-Beispiel ergänzen.
- [x] **TL.64 [P5, g1-4 Druck]** Handout Quadratzahlen-Tabelle als `n↔n²`-Zuordnung.
- [x] **TL.65 [P5, g1-4 Druck]** Schwierigkeit Gruppe „Teilweises Wurzelziehen" differenzieren — Aufg. 8 ●●○, Aufg. 9 ●●●.
- [x] **TL.66 [P4, g2-1 Druck Aufgabenserie A5]** Schwierigkeit auf ●○○ herabsetzen oder A1 auf ●●●.
- [x] **TL.67 [P4, g2-1 Druck Teste A5]** Lieferwagen-Lösung mit Probe ergänzen.
- [x] **TL.68 [P4, g2-1 Druck Anleitung]** Zeitvorgabe „40 Minuten" → „40-50 Minuten".
- [x] **TL.69 [P4, g2-1 Druck Anki 8, 11, 13]** Mathematische Präzisierungen.
- [x] **TL.70 [P5, g2-1 Druck]** `dk-untertitel` in Aufgabenserie und Selbsttest ergänzen (analog g1-2/3/4).
- [x] **TL.71 [P5, g2-1 Druck Handout Abschnitt 8]** Spalte „Bezeichnung" mit „Identität" explizit benennen.
- [x] **TL.72 [P3, g2-2a Druck Selbsttest A8]** Praxis-Marginalie zu 30-Minuten-Schritten.
- [x] **TL.73 [P3, g2-2a Druck Aufgabenserie A4-A6]** Diverse Marginalien (leer am 14. Tag, SIA 500, Grenzfall `c→0`).
- [x] **TL.74 [P3, g2-2a Druck Handout Abschnitt 6]** Konkrete Parameter-Beispielrechnung ergänzen.
- [x] **TL.75 [P3, g2-2a Druck Formelauszug Abschnitt 5]** 4-Punkte-Lösungsschema für Parameter.
- [x] **TL.76 [P4, g2-2a Druck Teste A9, A12]** Exakte Bruchwerte + intuitive Erklärung `p=0`-Fall.
- [x] **TL.77 [P4, g2-2a Druck]** Teste-Anleitung ergänzen (Zeitvorgabe, Hilfsmittel).
- [x] **TL.78 [P4, g2-2a Druck Aufgabenserie A2, A3]** Rundungs-Detail, Newtonsches Abkühlungsgesetz.
- [x] **TL.79 [P4, g2-2a Druck Handout Merksatz und Abschnitt 3]** Sonderfall „ausser bei Identität" präzisieren, Lösen-Tabelle kürzen.
- [x] **TL.80 [P4, g2-2a Druck Anki 4, 14, 22]** Diverse Anki-Verbesserungen.

---

## Welle M — Strukturelle Inkonsistenzen g2-3 vs. g2-2 (aus begutachtung-g2-3)

Aus der g2-3-Begutachtung: g2-3 unterscheidet sich strukturell von g2-2a/g2-2b in fünf Punkten. Vermutlich ältere Iteration.

- [x] **TM.1** Footer `doc-fuss` (siehe Welle D).
- [x] **TM.2** Lösungsbloack-Struktur in `teste-dich-selbst.html`: g2-2a/g2-2b verwenden einzelne `<div class="loes">` mit `loes-titel` pro Lösung; g2-3 verwendet *einen* Container mit 10 Absätzen ohne einzelne Titel — angleichen.
- [x] **TM.3** Schreiblinien `lin-mehr` (siehe Welle C, TC.4).
- [x] **TM.4** MathJax-Skalierung: g2-3-Teste und g2-3-Formelauszug verwenden `scale: 0.92`, g2-2a/g2-2b-Teste `scale: 1.0` — vereinheitlichen.
- [x] **TM.5** Anleitungs-Block: g2-2a/g2-2b haben `block-def` mit Hilfsmittel-Angabe und Zeitvorgabe; g2-3 hat nur Untertitel. Anleitungs-Block ergänzen.

---

## Welle N — Aufgaben-Sterne-System & Schwierigkeits-Konsistenz (optional, P5)

Aus LG5 und g1-1 Druck-Reviews: Schwierigkeitsmarkierung `⭐/⭐⭐/⭐⭐⭐` (bzw. `●○○/●●○/●●●`) nicht überall konsistent.

- [x] **TN.1 [P5]** Strategieentscheidung treffen: ⭐-System für Schwierigkeit auf allen Themenseiten einführen oder weglassen. Wenn ja, in `block-titel` integrieren.
- [x] **TN.2 [P4, g1-1 Druck]** Teste-Aufg. 1 von ●○○ auf ●●○ (Hauptoperation bestimmen ist nicht trivial).
- [x] **TN.3 [P4, g1-1 Druck Aufgabenserie]** Schwierigkeits-Legende in Übersichtstabelle ergänzen + `●○○`-Aufgabe ergänzen (Aufgabenserie hat aktuell nur ●●○ und ●●●).
- [x] **TN.4 [P4, g1-1 Druck Aufgabenserie]** Teste-dich-Selbst-Anleitung Zeitvorgabe „30 Minuten" → „30-45 Minuten".

---

## Welle O — Diverse Detail-Politur (P5)

- [x] **TO.1 [P5, LG3 g3-2 Typen-Tabelle Z. 234]** Variable `c` in `x = c` durch `x = k` ersetzen (Verwechslung mit Konstanter `c` in `ax² + bx + c`).
- [x] **TO.2 [P5, LG3 g3-1 Vier-Darstellungs-Block]** Optional konstruiertes Gegenbeispiel „warum Tabelle allein nicht reicht".
- [x] **TO.3 [P5, LG3 g3-2 A2]** Hinweis „Funktioniert am besten am Computer mit Maus" für mobile Nutzer.
- [x] **TO.4 [P5, LG3 g3-2/g3-3]** Marginalie zum Definitionsbereich „Standardmässig `D = ℝ`. Bei Anwendungsaufgaben oft eingeschränkt".
- [x] **TO.5 [P5, LG4]** g4-0 Sonderstatus dokumentieren („Praxisbeispiel — keine Theorieseite; durchlaufendes Anwendungsbeispiel für 4.1–4.3").
- [ ] **TO.6 [P5, LG4]** Schreibweise Klasse-Begriffe konsistent — entweder Klasse A immer mit denselben Daten oder X/Y/Z.
- [x] **TO.7 [P5, LG4 g4-3 Robustheits-Box]** Marginalie „Werte sortiert — bei realen Datenlisten zuerst sortieren!".
- [ ] **TO.8 [P5, LG5]** 5.2-Sub-Seiten JS in separate Dateien `g5-2a.js` … `g5-2d.js` auslagern (Wartbarkeit).
- [x] **TO.9 [P5, LG5 g5-2a]** SsW vs. sSW-Konvention vor g5-2d einführen.
- [ ] **TO.10 [P5, LG5 g5-5]** `block-fehler`-Doppelungen prüfen (Theorieblock und „Häufiger Fehler" redundant).
- [x] **TO.11 [P5, LG5]** Schweizer Hochdeutsch-Konsistenz: „300 Billionen Stellen" (Schweizer Zählweise = 10¹²) explizit als 10¹² markieren.
- [x] **TO.12 [P5, druck-g5-3/4/5]** Wenn man sich nicht für Variante (a) des Quellen-Footers entscheidet (Welle A, TA.5), könnte das `Notation (FTB)`-Block-Format aus g5-3 als Vorbild für g5-4 und g5-5 dienen.

---

## Bewusste Auslassungen / Nicht-Probleme

Folgende Punkte tauchen in den Reviews auf, sind aber explizit als **kein Handlungsbedarf** klassifiziert oder als rein optional/strategisch markiert:

- druck-g4-1 Befund 2 (Stichprobenumfang Black Box) — explizit „okay so".
- druck-g4-2 Befund 2 (`√n`-Faustregel) — „Keine Korrektur nötig; nur als Inflation, nicht zwingend".
- druck-g4-2 Befund 3 (Mittelwert > Median Faustregel) — „**Kein Handlungsbedarf**".
- druck-g5-2b Befund 1 (Sehnenviereck Z-Winkel-Dichte) — „**Kein Handlungsbedarf** — didaktische Beobachtung notiert".
- druck-g5-1 Befund 2 (neutrale Selbsttest-Titel) — „**Keine Korrektur nötig**".
- LG1 Übergreifend 1.2 ℕ-Konvention — bewusst Schweizer DACH-Konvention.

---

## Abarbeitungs-Reihenfolge (Empfehlung)

1. **Welle 0** (Sachfehler) — sofort, alle 8 Items.
2. **Welle A** (Promath-Verweis Find-Replace) — eine Iteration über alle betroffenen Formelauszüge.
3. **Welle B** (Anki-Generator + Intervall-Notation) — wenn der Generator zentral angefasst wird, sind alle Decks erledigt.
4. **Welle C** (Schreiblinien `lin-mehr`) — eine Iteration über 4 Selbsttest-Dateien.
5. **Welle D** (Footer g2-3) — schnell, 5 Dateien.
6. **Welle E** (Download-Galerie-Reihenfolge) — strategische Entscheidung, dann Welle.
7. **Welle F** (A7-Markierung) — abhängig von Styleguide-Entscheidung TF.1.
8. **Welle G** (Bidirektionale Quer-Verweise) — kann parallel zu seitenspezifischen Wellen laufen.
9. **Welle H** (`block-tipp` einführen) — pro LG ein Durchgang.
10. **Welle I** (STYLEGUIDE-Klassen-Hygiene) — pro LG ein Durchgang.
11. **Welle J** (Notations-Vereinheitlichungen) — schnelle Find-Replace.
12. **Welle M** (g2-3 strukturell an g2-2 angleichen) — eine Iteration.
13. **Welle K** (Lösungsweg-Granularität & Marginalien) — grösster Block, pro LG/pro Seite einzeln.
14. **Welle L** (Aufgaben-Politur) — pro LG/pro Seite einzeln, niedrige Prio.
15. **Welle N** (Sterne-System) — optional, strategische Entscheidung zuerst.
16. **Welle O** (Detail-Politur) — am Schluss, falls Zeit.

**Hinweis für die Tool-Quoten-Planung (COLLABORATION §3.5):** Wellen A, B, C, D, J sind ressourcen-sparend (Find-Replace, ein Skript pro Welle). Wellen K und L sind die teuersten — pro Item ein eigener Patch, evtl. mit Verifikation der Lösung. Bei knappem Budget zuerst Welle 0 + A + B + C + D + J in einer Sitzung, dann pro weiterer Sitzung eine LG-spezifische Welle.
