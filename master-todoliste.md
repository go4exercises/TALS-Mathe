# Master-Todoliste — TALS-Mathematik-Lehrmittel

**Stand:** 16. Mai 2026 · Basis: Strukturelles Review (18 Befunde) + fachlich-mathematisches Review (19 Befunde) über alle 22 Themenseiten und 88 Druckseiten der vollständigen Hauptcurriculum-Sektionen Lerngebiet 1 bis 5.

**Letzte Aktualisierung (16. Mai 2026):** **Alle Befunde aus dem Review sind bearbeitet.** Alle strukturellen S-Befunde (S1–S4) erledigt. Alle P2-Befunde (M10, M11, M12, M19) erledigt — Korrekturwelle 1 abgeschlossen. Aus Korrekturwelle 2 (P3 didaktisch) erledigt: M1 (Intervallnotation auf deutsche Schreibweise `[a; b[`), M2 (ggT-Formulierung präzisiert), M3, M4, M6, M7, M8, M9, M13, M14, M16, M17, M18. P4-Befund M15 erledigt (s_B ≈ 1.41 → 1.39). M5 bewusst nicht umgesetzt. **Stand: 22 von 23 Befunden umgesetzt, 1 bewusst nicht umgesetzt (M5).**

**Phase 2 — Animations-Anpassungen g5-2d (abgeschlossen 16. Mai 2026):** Sämtliche fünf Aufträge aus `Anpassungen_zu_g5-2d.pdf` wurden umgesetzt:

- **Anim 1 — Zentrische Streckung:** Z, A, B, C per Maus/Touch verschiebbar (Pointer Events, Drag-Handles mit Halo, Hit-Toleranz 14 px). Punkt-Durchmesser klein gehalten (Radius 4 für Eckpunkte, 3 für Z).
- **Anim 2 — Strahlensätze:** komplett neu gestaltet. Statt drei Schiebereglern für SA, SB, k jetzt zwei vordefinierte Situationen (A: SA=2, SB=3, k=2; B: SA=3, SB=2, k=3) und ein 5-Schritt-Aufbau (Schritt 0 = Übersichts-Skizze; Schritte 1–4 farbliche Strecken-Markierung + paralleler Gleichungs-Aufbau; Schritt 5 zweite Variante). Strahl-Winkel \\(\\gamma\\) so gewählt (\\(\\cos \\gamma = 0{.}75\\)), dass auch die Parallelenabschnitte AB und A'B' ganzzahlig sind.
- **Anim 3 — Ähnliche Figuren:** bei \\(|k| = 2\\) werden 4 original-grosse Kopien über das Bild gelegt (Dreieck + Rechteck) — visualisiert \\(A' = k^2 \\cdot A\\).
- **Anim 4 — Ähnlichkeitssätze:** Beschriftungs-Verbesserungen (Winkel-Labels im Winkelinneren, Seitenlabel-Abstand 18 px), sss-Konvention (kleine Buchstaben), neuer Erklär-Absatz „SSS vs sss".
- **Anim 5 — Höhensatz / Kathetensatz:** α/β-Position bei C korrigiert (Bisektrix-Bug in `drawAngleArc` global gefixt — neue Formel mit signiertem Winkel-Diff in (−π, π]). Zusätzlich: bei α ∈ [45°, 70°] mit Auswahl AHC bzw. [20°, 45°] mit Auswahl CHB wird eine gestrichelte 90°-Drehkopie an H gezeichnet — bei α = 45° fällt sie exakt auf das andere Teildreieck.

**HiDPI-Rendering (16. Mai 2026):** in drei Dateien (`g5-2d`, `g5-3`, `g5-4`) war `initCv` noch nicht für Retina-Displays optimiert — gefixt mit `devicePixelRatio`-Skalierung und logischer Auflösung in `cv.dataset.logicalW/H`. Konvention dokumentiert in **STYLEGUIDE §5.5.1**.

## Gesamtbild

Das Lehrmittel ist **fachlich solide gebaut**. Bei systematischer Prüfung jeder Definition, Formel und ungefähr **~280 Aufgabenlösungen** durch alle fünf Lerngebiete wurden **keine P1-Fehler** gefunden — keine fundamental falschen Definitionen oder kompletten Fehlkonzepte. Die 19 fachlichen Befunde verteilen sich auf 5x P2 (sollten vor nächster Schülerauflage korrigiert werden), 12x P3 (didaktische Verfeinerung), 1x P4 (kleinere Rundungsungenauigkeit) und 1x mit unklarem Status. Drei strukturelle P1-Befunde wurden am 16. Mai 2026 erledigt: ß → ss (TODO-S1), Kosinus → Cosinus (TODO-S2) und Dezimaltrennzeichen → Dezimalpunkt (TODO-S3, gemäss STYLEGUIDE §2.4). Zusätzlich erledigt: TODO-S4 (Punkt-Koordinaten `(x | y)` in g5-2d). Damit sind alle strukturellen S-Befunde abgeschlossen.

**Prioritäten-Skala:**
- **P1** — Muss vor jeder Verwendung in einer Schülerklasse korrigiert werden (struktureller Defekt oder grober Fehler)
- **P2** — Sollte vor der nächsten Auflage korrigiert werden (Lösungs-Endwerte falsch oder didaktisch problematische Begründung)
- **P3** — Nice-to-have-Verbesserung, Konsistenz oder Wording
- **P4** — Mini-Rundungsabweichung, kosmetisch

---

## Tabellarische Übersicht aller Befunde

| # | Prio | Lerngebiet | Datei | Stichwort | Aufwand | Status |
|---|------|------------|-------|-----------|---------|--------|
| S1 | P1 | alle | global | ß → ss Schweizer Hochdeutsch | hoch | **erledigt 2026-05-16** |
| S2 | P1 | alle | global | Kosinus → Cosinus vereinheitlichen | mittel | **erledigt 2026-05-16** |
| S3 | P1 | alle | global | Dezimaltrennzeichen → **Dezimalpunkt** überall | hoch | **erledigt 2026-05-16** |
| S4 | P3 | LG5 | g5-2d | Punkt-Koordinaten `(x, y)` → `(x \| y)` | niedrig | **erledigt 2026-05-16** |
| M1 | P2 | LG1 + LG3 | g1-2, g3-1 | Intervallnotation deutsch ↔ schweizerisch | niedrig | **erledigt 2026-05-16** |
| M2 | P2 | LG1 | g1-3 §6.1 | ggT-Formulierung schwach | niedrig | **erledigt 2026-05-16** |
| M3 | P3 | LG1 | g1-4 A6(b) | "etwa eine Billion" für 9·10¹¹ sprachlich falsch | niedrig | **erledigt 2026-05-16** |
| M4 | P3 | LG1 | g1-2 | Sprachlich unsauberer "getankter Betrag" | niedrig | **erledigt 2026-05-16** |
| M5 | P3 | LG1 | g1-2 | Runden -2.475 → -2.48 Vorzeichen-Konvention | niedrig | **wird nicht umgesetzt** |
| M6 | P3 | LG1 | g1-4 | √(a²)=\|a\| erst in Zusammenfassung | niedrig | **erledigt 2026-05-16** (bereits umgesetzt) |
| M7 | P3 | LG2 | g2-2a | Normalform ax+b=0 vs ax=b | niedrig | **erledigt 2026-05-16** |
| M8 | P3 | LG2 | g2-2b A6 | Wording vb-Negativität | niedrig | **erledigt 2026-05-16** |
| M9 | P3 | LG2 | g2-2b | x = ±√(-c/a) — Voraussetzung -c/a ≥ 0 fehlt | niedrig | **erledigt 2026-05-16** |
| M10 | **P2** | LG4 | g4-3 aufgabenserie L1c | Standardabweichung falsch (102 statt 115) | niedrig | **erledigt 2026-05-16** |
| M11 | **P2** | LG4 | g4-2 aufgabenserie L1c | Zwei Klassenhäufigkeiten falsch | niedrig | **erledigt 2026-05-16** |
| M12 | **P2** | LG4 | g4-2 A4 | Boxplot-Schiefe-Begründung faktisch falsch | mittel | **erledigt 2026-05-16** |
| M13 | P3 | LG4 | g4-2 | "7 Klassen"-Text vs. 6 Klassen in Tabelle | niedrig | **erledigt 2026-05-16** |
| M14 | P3 | LG4 | g4-1 A4 | n=22 vs. B2:B25 (=24) — Bereichswiderspruch | niedrig | **erledigt 2026-05-16** |
| M15 | P4 | LG4 | g4-3 Z.215 | s_B ≈ 1.41 statt 1.39 | niedrig | **erledigt 2026-05-16** |
| M16 | P3 | LG5 | g5-2a A4 (5) | sSW-Lösung verwirrend formuliert | niedrig | **erledigt 2026-05-16** |
| M17 | P3 | LG5 | g5-2b aufgabenserie L3 | Achteck-im-Quadrat Konstruktion mehrdeutig | mittel | **erledigt 2026-05-16** |
| M18 | P3 | LG5 | g5-3 A1 c | c ≈ 6.19 statt 6.13 | niedrig | **erledigt 2026-05-16** |
| M19 | **P2** | LG5 | g5-3 A2 b | Endwerte falsch (d=315 statt 248, h=274 statt 216) | niedrig | **erledigt 2026-05-16** |

**Verteilung Lerngebiete:** LG1 mit 6 Befunden, LG2 mit 3, LG3 mit 0 (mathematisch vorbildlich), LG4 mit 6, LG5 mit 4. Plus 4 globale strukturelle Befunde (davon S3 erledigt).

---

## Korrekturwelle 1 (P2 fachlich): 4 Befunde — alle erledigt 2026-05-16

Diese vier P2-Befunde sind **konkrete Zahlenfehler in publizierten Lösungen oder didaktisch unsaubere Aussagen**, die Schülerinnen direkt verwirren oder zu falschen Resultaten geführt hätten. Alle wurden am 16. Mai 2026 korrigiert und mit Python verifiziert.

### TODO-M10 — LG4 · g4-3 aufgabenserie L1c · Standardabweichung-Fehler (erledigt 2026-05-16)

**Status: erledigt.** Die Lösung der Aufgabe 1 ("Klassenarbeit", Datensatz mit 20 Werten) enthielt zwei zusammenhängende Zahlenfehler:

- Datei: `downloads/grundlagen/g4-3-masszahlen/aufgabenserie.html`, Lösung 1c (Z. 111)
- Aufgabe: Klassenarbeit mit n=20 Werten (11, 12, 12, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 18, 18, 18, 19, 20), Mittelwert 15.5
- Vorher: "Abweichungen quadriert summieren: ergibt 102. \(s = \sqrt{102/19} \approx 2.32\)"
- Nachher: "Abweichungen quadriert summieren: ergibt 115. \(s = \sqrt{115/19} \approx 2.46\)"
- Verifikation mit Python: Summe der quadrierten Abweichungen = 115.0; \(s = \sqrt{115/19} = \sqrt{6.0526} = 2.4602 \approx 2.46\)

Anmerkung: Der ursprüngliche Review-Text M10 sprach von einem "Datensatz B mit n=8" — das war eine Verwechslung im Review (vermutlich aus einer anderen Aufgabe übernommen); die echten Aufgabendaten sind die Klassenarbeit mit n=20. Die Endzahlen 102/115 und 2.32/2.46 stimmen aber für die echte Aufgabe.

### TODO-M11 — LG4 · g4-2 aufgabenserie L1c · Klassenhäufigkeiten falsch (erledigt 2026-05-16)

**Status: erledigt.** Die Lösung der Aufgabe 1 (Histogramm konstruieren, n=25 Körpergrössen) enthielt zwei korrespondierende Zahlenfehler in den Klassenhäufigkeiten.

- Datei: `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html`, Lösung 1c (Z. 108–109)
- Aufgabe: Klassieren der Körpergrössen von 25 Schülerinnen in 5 Klassen [158, 165), [165, 172), [172, 179), [179, 186), [186, 193)
- Vorher: "[172, 179): **9** Werte (172, 173, 173, 174, 175, 176, 177, 178)" und "[179, 186): **4** Werte (179, 180, 182, 183, 185)" — Anzahl-Angabe stimmte nicht zur aufgezählten Liste
- Nachher: "8 Werte" bzw. "5 Werte" — passt zur aufgezählten Liste und zur Verifikation
- Verifikation mit Python: Klassenhäufigkeiten sind **2, 8, 8, 5, 2** (Summe 25 ✓)

Die Folge-Interpretation in der Lösung ("annähernd symmetrisch und unimodal mit Gipfel im Bereich 165–179 cm") passt zur korrigierten Verteilung (2, 8, 8, 5, 2) sogar besser als zur fehlerhaften (2, 8, 9, 4, 2) — der Doppel-Gipfel im Bereich 165–172 und 172–179 cm rechtfertigt die Beschreibung "Gipfel im Bereich 165–179 cm" eindeutiger.

Anmerkung: Der ursprüngliche Review-Text M11 sprach von "6 Klassen" und einer Datei `g4-2-zentralmasse/aufgabenserie.html`; tatsächlich sind es 5 Klassen und der Ordner heisst `g4-2-diagramme`. Die Substanz des Befunds (9/4 → 8/5) stimmt.

### TODO-M12 — LG4 · g4-2 A4 (Themenseite) · Boxplot-Schiefe-Begründung falsch (erledigt 2026-05-16, Oder-Variante)

**Status: erledigt — Oder-Variante.** Die ursprüngliche Lösung enthielt zwei Fehler in einem Satz: erstens eine falsche Behauptung zur Box-Asymmetrie ("Median näher am oberen Quartil" — tatsächlich ist er näher am unteren), zweitens die Schlussfolgerung "linksschief" aus dieser Behauptung. Die Datenlage ist tatsächlich **nicht eindeutig**: Box-Asymmetrie und Antennen-Asymmetrie deuten in entgegengesetzte Richtungen. Statt die Aufgabe umzugestalten, wurde die Mehrdeutigkeit als didaktischer Lernpunkt aufgenommen.

- Datei: `grundlagen/g4-2-diagramme.html` (A4, Z. 654)
- Boxplot-Werte: min=15, Q₁=28, Med=35, Q₃=45, max=54
- Mathematik:
  - Median−Q₁ = 7, Q₃−Median = 10 → Median näher an Q₁ → **rechtsschiefe Box** (mehr Streuung oben)
  - Linke Antenne (15→28, Länge 13), rechte Antenne (45→54, Länge 9) → **linksschiefer Schwanz**
  - Beide Indikatoren widersprechen sich
- Vorher: "Linksschief — der Median (35) liegt näher am oberen Quartil (45) als am unteren (28), und der „Antenne" links ist länger als rechts."
- Nachher (sinngemäss): "Der Boxplot zeigt widersprüchliche Signale: innerhalb der Box deutet das auf rechtsschiefe Box (Median näher an Q₁, Abstand 7 vs. 10), die Antennen auf linksschiefen Schwanz (links Länge 13, rechts 9). Die Verteilung ist nicht eindeutig schief; ein Boxplot allein kann hier keine klare Diagnose liefern."

Damit wird die Aufgabe zum Lernpunkt: Boxplots fassen die Verteilung stark zusammen und können in solchen Grenzfällen widersprüchliche Signale geben; verlässliche Schiefe-Diagnose benötigt dann Histogramm oder Rohdaten.

Anmerkung: Der ursprüngliche Review-Text M12 sprach von Datei `g4-2-zentralmasse.html` — tatsächlich heisst sie `g4-2-diagramme.html`. Befund-Substanz stimmt.

### TODO-M19 — LG5 · g5-3 A2 b · Bergpeilen Endwerte falsch (erledigt 2026-05-16)

**Status: erledigt.** Die Lösung der Aufgabe A2 b (Bergpeilen mit zwei Höhenwinkeln) enthielt zwei Endwerte, die nicht zu den Aufgabenwinkeln 28° und 41° passten.

- Datei: `grundlagen/g5-3-trigonometrische-berechnungen.html` (A2 b, Z. 747)
- Aufgabe: Bergspitze unter 28° vom Boden peilen, 200 m näher heran, dann unter 41° peilen — wie hoch ist der Berg?
- Gleichungen: \(\tan(28°) = h/(d + 200)\), \(\tan(41°) = h/d\) → \(d = 200 \tan 28° / (\tan 41° - \tan 28°)\), \(h = d \tan 41°\)
- Vorher: "d ≈ 248 m, h ≈ 216 m"
- Nachher: "d ≈ 315 m, h ≈ 274 m"
- Verifikation mit Python: tan 28° = 0.5317, tan 41° = 0.8693; d = 200·0.5317/(0.8693−0.5317) = 106.34/0.3376 = 315.01 m; h = 315.01·0.8693 = 273.84 m. Probe via beider Gleichungen: jeweils 273.84 ✓
- Die alten Werte (248/216) waren in sich konsistent (216/tan 41° ≈ 248.5), aber sie passten nicht zur 28°/41°-Konstellation. Vermutung im Review: der Autor hatte h=216 angesetzt und d rückgerechnet.

### TODO-S2 — Kosinus → Cosinus (erledigt 2026-05-16)

**Status: erledigt.** Konvention: Schweizer Hochdeutsch — "Cosinus" statt "Kosinus", auch in Komposita (Cosinussatz, Cosinusfunktion, Cosinuswert).

63 Ersetzungen über 11 HTML-Dateien:
- `grundlagen/g5-3-trigonometrische-berechnungen.html` (28 — Themenseite mit Cosinussatz)
- `grundlagen/g5-4-einheitskreis.html` (3)
- `grundlagen/g5-5-trigonometrische-gleichungen.html` (2)
- `schwerpunkt/s3-5-trigonometrische-funktionen.html` (2)
- `downloads/grundlagen/g5-2a-dreiecke/aufgabenserie.html` (2)
- `downloads/grundlagen/g5-3-trigonometrische-berechnungen/aufgabenserie.html` (2), `formelauszug.html` (7), `handout.html` (6), `teste-dich-selbst.html` (8)
- `downloads/grundlagen/g5-4-einheitskreis/aufgabenserie.html` (1), `handout.html` (2)

**Bewahrt (NICHT umgestellt):** 3 externe Serlo-URLs mit "kosinus" im Slug (`de.serlo.org/.../sinus-und-kosinusfunktion` etc.) — diese hätten 404-Fehler ergeben.

Konvertierungs-Skript: `scripts/convert_cosinus.py` (mit Dry-Run-Modus, URL-Schutz, Verifikation).

### TODO-S1 — ß → ss (erledigt 2026-05-16)

**Status: erledigt.** Konvention: Schweizer Hochdeutsch — kein "ß", durchgehend "ss". Variante A (auch Eigennamen): "Gauß-Algorithmus" → "Gauss-Algorithmus".

34 Ersetzungen über 5 HTML-Dateien:
- `grundlagen/g2-3-lineare-gleichungssysteme.html` (1 — "Gauss-Algorithmus" im YouTube-Link)
- `grundlagen/g5-2a-dreiecke.html` (22 — Canvas-Erklärtexte, JS-Kommentare: Lotfuss, Höhenfusspunkt, Masse, gross, ausserhalb etc.)
- `grundlagen/g5-2b-vierecke.html` (6 — Massstab, Grösse, Aussenkontur, Masslinien)
- `grundlagen/g5-2c-kreis-und-kreisteile.html` (2 — Legende "~ gross", Kommentar "Masse beschriften")
- `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` (3 — grösserer, ausserhalb, Höhenfusspunkt)

Konvertierungs-Skript: `scripts/convert_eszett.py` (mit Dry-Run-Modus und Verifikation).

Markdown-Dokumente (CHANGELOG, STYLEGUIDE, COLLABORATION etc.) wurden bewusst ausgespart — das sind redaktionelle Texte ausserhalb des Lehrmittels.

### TODO-S3 — Dezimaltrennzeichen → Dezimalpunkt (erledigt 2026-05-16)

**Status: erledigt.** Konvention gemäss STYLEGUIDE §2.4: **Dezimalpunkt** (Schweizer Schulkonvention) — kein Dezimalkomma, weder in Klartext noch in MathJax.

273 Stellen über 14 HTML-Dateien wurden umgestellt: MathJax-`{,}`-Notation, Klartext-Dezimalkommas, JS-Template-Literals mit MathJax-Strings, sowie versehentlich aus MathJax übernommene `{,}`-Notation im Klartext. Bewusst nicht umgestellt: LaTeX-Subscripts (`x_{1,2}`), Punkt-Koordinaten `(x, y)` (siehe TODO-S4), Tupel und pythagoreische Tripel `(3, 4, 5)`, Inline-Event-Handler, SVG-Pfade, CSS, Google-Fonts-URL-Parameter.

Konvertierungs-Skript: `scripts/convert_decimals.py` (mit eingebauter Verifikation).

Details siehe `CHANGELOG.md` Eintrag [unreleased] vom 2026-05-16.

---

## Korrekturwelle 2 (didaktische Verfeinerung): 12 P3-Befunde

### TODO-S4 — Punkt-Koordinaten `(x, y)` → `(x | y)` (erledigt 2026-05-16)

**Status: erledigt.** Konvention gemäss STYLEGUIDE §2.4: Punkt-Koordinaten mit senkrechtem Strich `P(x | y)` (FTB-Standard) — auch innerhalb LaTeX/MathJax.

**Vorgehensweise:** Anders als bei S1/S2/S3 nicht über eine globale Regex umgesetzt, sondern als gezielte string-Ersetzungen, weil `(a, b)`-Klammerpaare im Lehrmittel auch als Datenwert-Aufzählungen vorkommen (z.B. Klassenhäufigkeiten in g4-2 Statistik: "2 Werte (158, 162)") und nicht alle Vorkommen Punktkoordinaten sind.

**Umgestellt (2 Stellen, 11 Klammer-Paare insgesamt):**
- `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` — Lösung der zentrischen Streckung A'/B'/C' mit k=2: `2(0,0) - (1,1) = (-1, -1)` etc. → `2(0|0) - (1|1) = (-1|-1)` etc. (9 Paare in einer Zeile). Jetzt konsistent mit der Aufgabenstellung darüber: `A(0|0), B(6|0), C(2|4), Z(1|1)`.
- `downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/teste-dich-selbst.html` — Lösung Punktspiegelung: `-2 · (3, 4) = (-6, -8)` → `-2 · (3|4) = (-6|-8)`. Jetzt konsistent mit der Aufgabenstellung darüber: `Z = (0|0), P = (3|4)`.

**Bewahrt (nicht umgestellt):**
- `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html`: `(158, 162)` und `(187, 189)` — Aufzählungen von Datenwerten in Klassenhäufigkeiten, keine Punktkoordinaten.

Konvertierungs-Skript: `scripts/convert_punktkoord.py` (gezielte string-Ersetzungen mit Dry-Run-Verifikation).

### Lerngebiet 1 — Arithmetik / Algebra

**M3 (P3) — erledigt 2026-05-16:** g1-4 A6(b) — Lösung sagte fälschlich „etwa eine Billion" für \(9 \cdot 10^{11}\), nach Schweizer/DACH long-scale-Konvention sind das aber 900 Milliarden = 0.9 Billionen. Neu formuliert: „Pro Stunde: \(2.5 \cdot 10^8 \cdot 3600 = 9 \cdot 10^{11}\) Schaltvorgänge — also **900 Milliarden** (= 0.9 Billionen)." Datei: `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 509.

**M4 (P3) — erledigt 2026-05-16:** g1-2 aufgabenserie Aufgabe 2 (Treibstoff/Rabatt) — der Befund kritisierte die Lösung „Bezahlt: 20.4 · 0.93 = 18.972 L" als begrifflich unsauber, weil der Kunde 20.4 Liter bezahlt (zum reduzierten Preis), nicht 18.972 Liter. Aufgabe und Lösung wurden auf eine konkrete Preisberechnung umgestellt (Variante A aus der Befund-Anweisung): Aufgabentext erhält neu „Der Normalpreis beträgt 1.80 Fr./L." und Frage (b) lautet „was kostet die Tankfüllung mit Rabatt"; die Lösung berechnet \(20.4 \cdot 1.80 \cdot 0.93 = 34.1496\) Fr. (mit Vergleich ohne Rabatt 36.72 Fr., Ersparnis 2.5704 Fr.) und gibt die Bruchdarstellung \(\tfrac{42687}{1250}\) Fr. an. Datei: `downloads/grundlagen/g1-2-zahlen-grundoperationen/aufgabenserie.html` Z. 60–63 (Aufgabe) und Z. 123 (Lösung 2).

**M5 (P3) — wird nicht umgesetzt (Entscheidung 2026-05-16):** g1-2 — Beispiel \(-2.475 \to -2.48\). Die Schweizer kaufmännische Rundung mit Vorzeichen wurde als Befund festgehalten, aber bewusst nicht umgesetzt — die aktuelle Darstellung bleibt; das didaktische Nutzen-Aufwand-Verhältnis spricht gegen eine Erweiterung dieser Stelle.

**M6 (P3) — bereits umgesetzt, Befund erledigt 2026-05-16:** g1-4 — \(\sqrt{a^2} = |a|\) wird im aktuellen Snapshot bereits direkt im Theorie-Abschnitt §5 (Quadratwurzeln) erläutert. In `grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html` Z. 302–306 steht ein „Häufiger Fehler"-Block mit Beispiel: „\(\sqrt{(-3)^2} = \sqrt{9} = 3\), nicht \(-3\). Die Wurzelfunktion wirft das Vorzeichen weg." Der Block steht 29 Zeilen nach der Wurzel-Definition und 211 Zeilen vor der Zusammenfassung — genau wie die Anweisung es fordert. Der Review-Befund bezog sich offenbar auf eine frühere Lehrmittelversion vor der bereits erfolgten Umgestaltung; keine neue Änderung nötig.

### Lerngebiet 2 — Gleichungen

**M7 (P3) — erledigt 2026-05-16:** g2-2a — Themenseite war intern uneinheitlich: Normalform-Definition nutzte \(ax + b = 0\) (mit Lösung \(-b/a\)), der Lösungsfälle-Abschnitt aber \(ax = b\) (mit Lösung \(b/a\)) — derselbe Buchstabe \(b\) hatte zwei verschiedene Bedeutungen. Vereinheitlicht auf \(ax + b = 0\) (analog Handout und Zusammenfassung). Datei: `grundlagen/g2-2a-lineare-gleichungen.html`. Änderungen: Einleitungssatz „Drei Lösungsfälle" Z. 276 („Form \(ax = b\)" → „Normalform \(ax + b = 0\)") und Fall-1-Lösungsformel Z. 283 (\(\mathbb{L} = \{b/a\}\) → \(\mathbb{L} = \{-b/a\}\)). Die Bedingungen für die drei Fälle (\(a \neq 0\) / \(a = 0, b \neq 0\) / \(a = 0, b = 0\)) bleiben gleich; sie sind bei \(ax + b = 0\) und \(ax = b\) symmetrisch. Der Parameter-Abschnitt (Z. 338–339) bleibt unverändert: dort wird operationsbedingt \((k-2)x = 3(k-2)\) als konkrete Sortier-Schreibweise verwendet, was keinen Buchstaben-Konflikt erzeugt.

**M8 (P3) — erledigt 2026-05-16:** g2-2b — die Velo-Aufgabe (Anna fährt 12 km, Hinweg \(v\), Rückweg \(v-4\)) hat zwei rechnerische Lösungen \(v_a \approx 18.25\) und \(v_b \approx 1.76\). Die alte Begründung „v_b wäre kleiner als 4 und ergäbe negative Rückweg-Geschwindigkeit" liess es klingen, als sei v_b selbst negativ — tatsächlich ist v_b positiv, nur die Rückweg-Geschwindigkeit \(v_b - 4 \approx -2.24\) ist negativ. Beide Stellen umformuliert (Datei: `grundlagen/g2-2b-quadratische-gleichungen.html`): Einstiegstext Z. 180 zeigt nun explizit „\(v_b - 4 \approx -2.3\) negativ", A6-Lösung Z. 592 zeigt „\(v_b - 4 \approx -2.24\) negativ". Die Aufgabenserie hatte die Argumentation bereits korrekt — Themenseite und Druckseite sind jetzt konsistent.

**M9 (P3) — erledigt 2026-05-16:** g2-2b — Beim Wurzelziehen für rein quadratische Gleichungen \(a x^2 + c = 0 \Rightarrow x^2 = -c/a\) fehlte die Voraussetzung \(-c/a \geq 0\). Ohne diese ergibt der Ansatz formal komplexe Lösungen. An zwei Stellen ergänzt: Themenseite Z. 607 (Zusammenfassungstabelle) und Formelauszug Z. 57-58. Neue Formulierung: „falls \(-c/a \geq 0\): \(x = \pm\sqrt{-c/a}\), sonst \(\mathbb{L} = \emptyset\)". Damit ist die Bedingung sichtbar und Lernende erkennen den 0-Lösungen-Fall direkt aus der Formel.

### Lerngebiet 4 — Statistik

**M13 (P3) — erledigt 2026-05-16, Variante B:** g4-2 Klassieren-Beispiel — Inkonsistenz zwischen Text („7 Klassen", „156-188 cm") und Tabelle (6 Klassen, höchste Klasse `[180, 185)`, max 188 würde reinpassen — passt nicht). Variante B gewählt: **Tabelle bleibt, Text angepasst**. Datei: `grundlagen/g4-2-diagramme.html` Z. 184. Vorher: „60 Lernende, Grössen zwischen **156 cm und 188 cm**. Mit **7 Klassen** à 5 cm". Nachher: „60 Lernende, Grössen zwischen **156 cm und 184 cm**. Mit **6 Klassen** à 5 cm". Damit passen Wertebereich (156-184) und Anzahl Klassen zu den 6 Tabellenzeilen `[155, 160) ... [180, 185)`. Variante A (Tabelle um 7. Klasse `[185, 190)` ergänzen) wäre alternativ möglich gewesen, hätte aber die Häufigkeiten umverteilt — Variante B ist sauberer, weil die didaktisch wertvolle abklingende Klassenverteilung (5, 12, 18, 14, 8, 3) unangetastet bleibt.

**M14 (P3) — erledigt 2026-05-16, Variante A:** g4-1 A4 — Inkonsistenz zwischen Einstiegsbeispiel (\(n = 22\)) und Aufgabe A4 (Bereich `B2:B25` = 24 Werte). Variante A gewählt: **Bereich an Einstieg angepasst**. Datei: `grundlagen/g4-1-grundlagen.html` Z. 343-358. Änderungen: Aufgabentext „in den Zellen `B2:B25`" → `B2:B23` (22 Zellen); Folgereferenz `B26` → `B24`; Lösung (1) „Ergebnis 24" → „Ergebnis 22", Lösung (2)(3)(4) entsprechend mit `B2:B23` und `B23`/`B24`. Damit ist A4 nun konsistent zum Einstiegsbeispiel (n=22), und der Lösungs-Tipp „auf ganze Spalte erweitern" bleibt didaktisch wertvoll. Variante B (Bezug "der Klasse aus dem Einstieg" streichen) wäre alternativ möglich gewesen, aber Variante A bewahrt den Bezug zum Einstiegsbeispiel.

### Lerngebiet 5 — Geometrie

**M16 (P3) — erledigt 2026-05-16:** g5-2a A4 (5) — die Lösung begann mit „sSW, mehrdeutig" und korrigierte sich dann selbst zum Grenzfall mit 1 Lösung — didaktisch unglücklich, weil Lernende ihr Verständnis sofort revidieren mussten. Lösung umformuliert zu sauberer Fallunterscheidung: Zuerst `b · sin α = 8 · 0.5 = 4` rechnen, dann mit `a = 4` vergleichen → wegen `a = b · sin α` Grenzfall, **genau eine Lösung** (rechtwinkliges Dreieck bei B). Am Ende didaktische Verallgemeinerung: „Allgemein: bei `a > b·sin α` zwei Lösungen, bei `a = b·sin α` eine, bei `a < b·sin α` keine." Datei: `grundlagen/g5-2a-dreiecke.html` Z. 659.

**M17 (P3) — erledigt 2026-05-16:** g5-2b aufgabenserie Aufgabe 3 — die Aufgabenstellung „Achteck eingeschrieben in Quadrat (120 cm)" war doppelt mehrdeutig: erstens unklare Konstruktion, zweitens war die alte Lösung mathematisch falsch (sie verwechselte Apothem mit Umkreisradius und kam zu `R = L/2 = 60` statt korrekt `R = L/(2·cos 22.5°) ≈ 64.94`). Aufgabentext präzisiert („die acht Achteck-Ecken liegen paarweise auf den vier Quadratseiten") plus zusätzlicher Tipp `cos 22.5° ≈ 0.9239`. Lösung mathematisch korrigiert: `r = 60`, `R ≈ 64.94`, `s ≈ 49.71`, `U ≈ 397.65` (vorher fälschlich `R = 60`, `s ≈ 45.9`, `U ≈ 367.4`). Datei: `downloads/grundlagen/g5-2b-vierecke/aufgabenserie.html` Z. 48 (Aufgabe) und Z. 85-90 (Lösung 3). Mit Python verifiziert: bei regelmässigem Achteck mit Apothem `r = L/2 = 60` ist `R = r / cos 22.5° = 60 / 0.9239 = 64.9435 cm`, `s = 2R·sin 22.5° = 49.7056 cm`, `U = 8s = 397.6450 cm`.

**M18 (P3) — erledigt 2026-05-16:** g5-3 A1 c — Lösung sagte `c ≈ 6.13` für den Cosinussatz mit `a = 8, b = 6, γ = 50°`. Mit Python verifiziert: `c² = 64 + 36 - 96·cos 50° = 100 - 61.708 = 38.292`, also `c ≈ 6.188 ≈ 6.19` (nicht 6.13). Korrigiert in `grundlagen/g5-3-trigonometrische-berechnungen.html` Z. 725: `\approx 6.13` → `\approx 6.19`. Dezimalpunkt-Konvention eingehalten.

### Übergreifend

**M1 (P2 → P3 in Praxis) — erledigt 2026-05-16, deutsche Notation gewählt:** Intervallnotation deutsch (`[a; b[`) versus international (`[a, b)`). Wahl: **deutsche Notation als Standard** — eckige Klammer-Richtung signalisiert offen/zu (Klammer zum Intervall hin = Grenze dabei), Semikolon als Trennzeichen. Das ist die im deutschsprachigen Schulraum traditionell verbreitete Konvention (ISO 31-11). Alle Stellen, die zuvor in internationaler Notation `[a, b)` waren, wurden auf deutsche Notation `[a; b[` umgestellt — etwa 40 Stellen über mehrere Dateien.

**Geänderte Hauptstellen:**

- Themenseite `grundlagen/g1-2-zahlen-grundoperationen.html` Z. 226-244 — Intervall-Erklärtext und -Tabelle umgeschrieben: „Klammer-Richtung (zum Intervall hin: ja, weg: nein)" statt „eckig: ja, rund: nein"; Tabelle nutzt `[a; b]`, `]a; b[`, `[a; b[`, `]-\infty; b]`, `[a; +\infty[`; Fehlerhinweis bei \(\infty\) entsprechend umformuliert. A5-Lösung Z. 419: `(1) [-2; 5]. (2) ]-\infty; 3[. (3) ]-1; 4]. (4) [0; +\infty[`.
- `grundlagen/g4-2-diagramme.html` — alle Klassen-Intervalle in Tabelle (6 Klasseneinteilungs-Zellen `[155; 160[`...`[180; 185[`), Erklärtext zur Notation, Aufgabe A2 (`[0; 5[, [5; 10[, …, [45; 50]`) und A3 (5 Klassen + 5 Tabellenzellen `[1; 3[`...`[9; 11[`).
- `downloads/grundlagen/g4-2-diagramme/aufgabenserie.html` — Klassenliste in der Aufgabe und 5 Häufigkeitslisten-Zeilen in der Lösung.
- LG5 Trigonometrie (`grundlagen/g5-5-trigonometrische-gleichungen.html` + 3 Druckseiten): `[0°; 360°[`, `[0°; 720°[`, `[-360°; 0°[`, sowie geschlossene Bereiche `[-90°; 90°]`, `[0°; 180°]`, `[-1; 1]` etc.
- LG3 Wertebereiche (`grundlagen/g3-1-grundlagen.html` und Druckseiten): `[0; \infty[`, `[-5; \infty[`, `]-\infty; 3]`, geschlossene `[0; 50]`, `[0; 40]`, `[0; 600]`, `[20; 200]`, `[0; 480]`, `[16; 20]`, `[23; 31]`, etc.
- `downloads/grundlagen/g2-2a-lineare-gleichungen/teste-dich-selbst.html`: `]-\infty; 2]`.
- `grundlagen/g5-4-einheitskreis.html`: `[0°; 90°]`.

**Bereits in deutscher Notation (unverändert):**

- g1-2 Formelauszug und Handout (waren von Anfang an in deutscher Notation).
- g5-2c Themenseite und Formelauszug (Zentriwinkel-Bereich `[0°; 360°[`).

**M2 (P2) — erledigt 2026-05-16:** g1-3 §6.1 — die alte Formulierung „Suchen Sie den grössten gemeinsamen Faktor (ggT) aller Glieder — bei Zahlen die kleinste Mehrfach-Teilung, bei Variablen den niedrigsten gemeinsamen Exponenten" war doppelt problematisch: „Mehrfach-Teilung" ist kein etablierter mathematischer Begriff, und „kleinste Mehrfach-Teilung" klingt eher nach kgV als nach ggT. Datei: `grundlagen/g1-3-algebraische-terme.html` Z. 270-271. Neue Formulierung: „Suche den **grössten gemeinsamen Teiler (ggT)** der Zahlen-Koeffizienten — über die Primfaktorzerlegung: jeden gemeinsamen Primfaktor mit dem kleinsten vorkommenden Exponenten — und bei Variablen den niedrigsten gemeinsamen Exponenten:". Damit ist die Methode der Bestimmung explizit (Primfaktorzerlegung) und der Begriff „Mehrfach-Teilung" verschwunden.

---

## Korrekturwelle 3 (kosmetisch): 1 P4-Befund

**M15 (P4) — erledigt 2026-05-16:** g4-3 Themenseite Z. 215 — der angegebene Wert `s ≈ 1.41` für die Standardabweichung von Klasse B (Werte 2.5, 3.0, 3.8, 4.5, 4.5, 5.2, 6.0, 6.5) war eine Rundungsabweichung; korrekt ist `s ≈ 1.39`. Mit Python verifiziert: Mittelwert = 4.5, Summe der quadrierten Abweichungen = 13.48, \(s = \sqrt{13.48/7} = \sqrt{1.9257} = 1.3877 \approx 1.39\). Datei: `grundlagen/g4-3-masszahlen.html` Z. 215. Vorher: „hat \(s \approx 1.41\)". Nachher: „hat \(s \approx 1.39\)". Dezimalpunkt-Konvention eingehalten. Beobachtung: der Befund bezieht sich auf M10 (gleiche aufgabenserie-Lösungs-Inkonsistenz), aber das ist eine andere Aufgabe; M10 hat einen anderen Datensatz (n=20 Klassenarbeit, 11..20). M15 betrifft nur die Themenseite mit dem 8-Werte-Datensatz.

---

## Korrekturweg-Empfehlung

**Alle strukturellen S-Befunde (S1–S4) sind erledigt** (2026-05-16). **Korrekturwelle 1 (P2 fachlich) ist abgeschlossen** — M10, M11, M12, M19 sind alle korrigiert.

Verbleibend sind die didaktischen Verfeinerungen:

1. **Zweite Welle (P3 didaktisch + die zwei verbleibenden P2-Verfeinerungen):** M1 und M2 (P2: Intervallnotation und ggT-Formulierung), plus die 12 P3-Befunde M3–M9, M13, M14, M16–M18. Aufwand: 1-2 Arbeitstage.

2. **Dritte Welle (P4 kosmetisch):** M15 (Rundungsabweichung s_B ≈ 1.41 statt 1.39 auf g4-3 Themenseite — zur Konsistenz mit der jetzt korrigierten aufgabenserie L1c).

Nach diesen Wellen ist das Lehrmittel fachlich und sprachlich auf Profi-Niveau. Die mathematische Substanz steht bereits — das Review hat im Wesentlichen bestätigt, dass die ungefähr 280 geprüften Aufgabenlösungen und die ganze Theorie auf einem hohen Niveau sind.

---

## Lerngebiet 3 als Referenz

**Lerngebiet 3 (Funktionen) ist mathematisch vorbildlich** — bei ungefähr 60 nachgerechneten Aufgabenlösungen wurde kein einziger Fehler gefunden. Funktionen, Nullstellen, lineare und quadratische Funktionen, Exponential- und Logarithmusfunktion, Polynomdivision — alles makellos. Das zeigt: Die Lerngebiete sind nicht gleich sauber, sondern Lerngebiet 3 ist die Referenz-Qualität, an der die anderen vier sich messen können.

## Methodik-Notiz

Das fachliche Review wurde mit Python für jede Trig-Funktion, jede Wurzel, jede Standardabweichung und jede Cosinussatz-Anwendung verifiziert. Wo Lösungen vom erwarteten Wert abwichen, wurde explizit nach Verwechslungs-Hypothesen gesucht (z.B. "Hat der Autor versehentlich b=5 statt b=6 eingesetzt?"). Die Quote "Befund pro Aufgabenlösung" ist mit 19/280 ≈ **6.8 %** für ein in Eigenarbeit entstandenes Lehrmittel sehr gut — kommerzielle Schulbücher haben oft ähnliche oder höhere Fehlerquoten in ersten Auflagen.
