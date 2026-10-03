# TODO — Leitprogramm Quadratische Funktionen (Stand 02.10.2026)

Legende: `[x]` erledigt · `[–]` bewusst nicht geändert (Grund dahinter) · `[ ]` offen.
Prio: **HOCH** = Lernende lernen Falsches · **MITTEL** = irreführend, widersprüchlich oder
unvollständig · **NIEDRIG** = Kleinigkeit/Konvention.

Seite: `leitprogramme/quadratische-funktionen.html`, gebaut aus
`scripts/lp/quadratische-funktionen/seite.py` + `seite.js` (Änderungen dort, nicht in der HTML-Datei).
Ein erledigter Punkt wird abgehakt; ist die Liste leer, wird die Datei gelöscht (steht in der Git-Geschichte).

---

## Prüfung auf fachliche und didaktische Richtigkeit (02.10.2026)

Geprüft werden die Seite (Vorwissen, 5 Kapitel, Aufgaben, Übungen mit Rückmeldung,
Logik der Animationen), die 11 Clips (10 eigene + `g1-3-binome-erkennen`) sowie
`gesamttest.pdf` und `bewertungspaket.pdf`. Alle Zahlen wurden mit `python3` nachgerechnet.

**Rechenfehler: keine.** Alle Zahlen in Vortest, Aufgaben 0a–5c, Festhalten-Kästen, Minigrafen,
25 Kontrollfragen, Stützpunkten der Bewegungen und beiden PDFs stimmen (`python3`). Die elf
Übungsgeneratoren liefern immer lösbare Aufgaben, und keine richtige Antwort wird als falsch
gewertet (je 20 000 Zufallsfälle in node). Alle Zielwerte der Aufgabenleisten liegen auf dem
Reglerraster. Punkte im Gesamttest: 11 + 6 + 7 = 24, stimmen mit Paket und Seite überein.
**Behoben am 03.10.2026** (alle Punkte unten). Neu: Gesamttest 25 P (G4 Diskriminante/Nullstellen, G8 «Quadrat im Quadrat», Minimum über \(-\frac{b}{2a}\)); 7 Clips neu vertont (10:31 min); Theme `begreifbar-schlicht` mit Farbe 5 = Tinte; Kapiteltests 11/13/12/16/14 P.
Bewusst gelassen: «Häufiger Fehler» in Kapitel 5 rechnet mit 40 m wie der Clip (Sim jetzt 36 m); in `a-finden` reichen bewegte Probeparabeln am Rand bis −0.6 m (ganz nur mit Skriptänderung).
Zeilen: Stand Commit `3ebeed9`. `seite.*` = `scripts/lp/quadratische-funktionen/`.

### HOCH

- [x] **Clip `verschieben`, Szenen «Merke» und «v senkt»:** «x s schiebt sie waagrecht, mit
  umgekehrtem Vorzeichen» und «Beim y s stimmt das Vorzeichen mit der Richtung überein» sind
  falsch: \(x_s = 2\) schiebt nach rechts, gleiches Vorzeichen. Umgekehrt ist nur die Zahl *in
  der Klammer*. Der Kontrollclip sagt es richtig. → «x_s steht in der Klammer mit umgekehrtem
  Vorzeichen», «Hinter der Klammer stimmt …»; Bildtext gleich; neu vertonen.
- [x] **Clip `verschieben`, Szene «Warum rechts»:** Die Bewegung `[[0,1,2,0],[1.5,1,2,0],[3.0,1,1,0],
  [4.5,1,2,0]]` zeigt bei 3 s \(S(1 \mid 0)\), während Bild und Ton «\(x = 2\)» sagen. → Parabel bei
  \(x_s = 2\) stehen lassen.
- [x] **Übung «Nullstellen bestimmen», Hinweis** (`seite.js:389`): «Produkt c, Summe b» — für die
  Nullstellen gilt Summe \(-b\) (\(x^2-x-6\): Nullstellen −2, 3, Summe +1). Führt direkt zum
  Vorzeichenfehler. → «zwei Zahlen mit Produkt c und Summe −b».
- [x] **Übung «Produktform → Grundform», Diagnose** (`seite.js:365–366`): Bei \(b = 0\) bzw.
  \(c = 0\) (wird gewürfelt) trifft `gl(e.b,-A.b)` bzw. `gl(e.c,-A.c)` immer zu → falsche Meldung
  (z. B. \(2(x-3)(x+3)\), nur c falsch → «Vorzeichen von b»). → Bedingung `A.b !== 0` bzw. `A.c !== 0`.

### MITTEL

- [x] **Gesamttest prüft Kapitel 3 nicht:** keine Diskriminante, keine Nullstellen aus der
  Grundform, keine Produktform aus der Grundform (HOWTO §9: «Jedes Kapitelziel wird geprüft»).
  → Aufgabe ergänzen, z. B. \(x^2-2x-8\): Anzahl Nullstellen mit \(D\), Nullstellen, Produktform
  (3 P, Teil A); Punkte, Paket, Selbsteinschätzung und Seite nachführen.
- [x] **Kontrollclips verraten die Antwort im Bild**, weil der erste Stützpunkt schon die Lösung
  ist: `kontrolle-nullstellen` F4 (Nullstellen −2, 4 beschriftet), `kontrolle-extremwert` F1–F4
  (Hochpunkt bei 5, Läufer «A = 25»), `kontrolle-formen` F3. → neutrale Startparabel, Lösung erst
  nach der Antwort.
- [x] **Abgefragt, aber nicht eingeführt:** Wertemenge (Aufgabe 1c, `seite.py:162`); quadratische
  Ergänzung (Aufgabe 2b; nur das Wort in `seite.py:199`, kein Clip, keine Übung). Die Übungen in
  Kapitel 2 gehen nur Richtung Grundform; Grund- → Scheitel-/Produktform fehlt als Übung.
- [x] **Definition fehlt:** \(f(x)=ax^2+bx+c,\ a \neq 0\) steht nirgends; das Wort «Diskriminante»
  nur im Link; im Clip `achse-bleibt` erscheint \(D\) ohne \(D = b^2-4ac\).
- [x] **«Achse» ohne Zusatz** in `kontrolle-nullstellen` (13 ×, mal x-Achse, mal Symmetrieachse),
  `kontrolle-formen` F4, `kontrolle-aufstellen` F2-Rückmeldung, `kontrolle-extremwert` F3 —
  wie im Einführungsclip (Commit 9c1a4a5) angleichen; neu vertonen.
- [x] **Clip `a-finden`, «Merke»:** \(a(x-u)^2+v\) → \(a(x-x_s)^2+y_s\).
- [x] **Sim 2, Grundform gerundet ohne «≈»** (`seite.js:157,162`): \(a=0.25,\ x_s=0.5\) zeigt
  «0.06» statt 0.0625 (HOWTO §8b). → `genau`-Prüfung wie bei der Produktform.
- [x] **Übung «Scheitel + Punkt → a»** (`seite.js:393`): Bei \(d = \pm 1\) (≈ 37 %) prüft sie das
  Quadrieren nicht (bei \(d=1\) gilt die falsche Rechnung als richtig). → \(|d| \ge 2\).
- [x] **Bewertungspaket, Raster für die KI unscharf:** welcher Punkt der «Ergebnispunkt» ist (`:44`);
  «Typische Fehler»-Abzüge überschneiden sich mit Rasterzeilen (G7 `:105`, G8 `:115`); G2 koppelt
  Scheitel und \((0 \mid 10)\) in einem Punkt; G6 zeigt den Scheitelweg nur halb (`:92–93`);
  gleichwertige Schreibweisen (\(-\tfrac14\)) nicht geregelt; Selbsteinschätzung 16–20 P ohne
  Kapitelzuordnung (`:121`).
- [x] **Beispiele wiederholt** (HOWTO §4): Sim 2 A6 \(x^2-4x+3\), Sim 3 A2/A5, Sim 4 Fall A,
  Sim 5 A1/A2 nehmen die Clip-Beispiele; Übung «Mauer» kann \(L = 60\) würfeln = Aufgabe 5a;
  Gesamttest G8 hat dasselbe Modell \(x(L-2x)\) wie 5a.
- [x] **HOWTO §9/§10:** «Warum»-Aufgabe nur in Kapitel 2; Kapitel 2 und 5 ohne Aufgabe am Graphen;
  Gesamttest ohne Begründungsteil; Synonyme der Themenseite (Linearfaktorform, allgemeine Form)
  fehlen.
- [x] **Farben wechseln die Bedeutung** zwischen Kapitel 1 (\fa = a, \fb = x_s, \fc = y_s) und
  Kapitel 2/3 (\fa = c, \fb = Nullstellen, \fc = Scheitel).
- [x] **Extremwert-Regel zu eng** (`seite.py:295`): nur «Nullstellen → Mitte → Maximum»; Hinweis auf
  \(-\frac{b}{2a}\) und Minimum bei \(a \gt 0\) fehlt. «Drei Punkte → drei Gleichungen»
  (`seite.py:263`) steht im Festhalten, wird aber nirgends geübt.

### NIEDRIG

- [x] Übungen: Nochmals «Prüfen» nach ✓ setzt die Serie auf 0 (`seite.js:465–468`); «+3» und
  «.5» werden abgelehnt; Schreibweise \(2(x-3)x\) statt \(2x(x-3)\) (`seite.js:360`).
- [x] Aufgabenleisten: Sim 2 A6 und Sim 3 A5 verlangen den Startzustand (sofort ✓); Sim 1
  «nochmals» setzt `bewegt` nicht zurück; Sim 5 A1: x = 4 beim Start schon besucht.
- [x] Formulierungen: `seite.py:147` «\(a\) verschiebt nichts: \(a \gt 0\) nach oben» →
  «nach oben geöffnet», «schmaler als die Normalparabel»; `:232` «Bei \(b=-4\)» → «Bei \(a=1,\ b=-4\)»;
  `:237` «ohne Rechnen» → «ohne die Nullstellen zu berechnen»; «gespiegelt», «gestaucht» in Übungen
  (`seite.js:318–329`) nie eingeführt; Kapitel 3 trägt nur K2 (auch K1); 5a ohne Definition von x.
- [x] Clips, Zeitversätze in `verschieben` («a formt», «v senkt» sagt «um eins», sichtbar um 3;
  «Zusammen») und `kontrolle-scheitelform` F4; Beschriftung «S(0 | 0)» überdeckt die Achsenzahl 1.
- [x] Clips, Fragen: `kontrolle-nullstellen` F4 zwei verschiedene «Summen» und Rückmeldung verrät
  die Lösung (Text ≠ Ton); `kontrolle-scheitelform` F1 «y_s hinter der Klammer» ohne Klammer;
  `kontrolle-extremwert` F3 ohne `fallen`; `kontrolle-aufstellen` F5 Falle (3 | 3) schwach.
- [x] Clips, Wortlaut: `mitte` «Die Fläche ist eine Parabel» → «Der Graph der Fläche …»;
  `kontrolle-extremwert` F4: Lage von x zur Mauer nicht gesagt; `a-finden`: Wurfbahn bis −4 m.
- [x] `g1-3-binome-erkennen` nennt die Binomvariablen a, b — im LP sind das Koeffizienten; kurzer
  Hinweis neben dem Clip.
- [x] PDFs: G8 «Gib die Masse» → «die Abmessungen»; G8 nur 7 Linien (→ 10–12), G6 → 6–7;
  G3-Grafik: Punkt \((0 \mid -1)\) überdeckt die Zahl −1; Bewertungspaket: Überschrift §3 allein
  am Seitenende (`\needspace`); Datenschutz: Hinweis auf Foto-Metadaten (Standort) fehlt; «die
  Summe von 24» → «die Gesamtpunktzahl (von 24)».

---

## Zweite Prüfung (`../TODOx.md`, ausgewertet 03.10.2026)

Unabhängige Prüfung desselben Stands (02.10.2026). Was die erste Prüfung schon abgedeckt hat,
ist dort erledigt; hier stehen nur die zusätzlichen Punkte, im Code nachgeprüft.
**Behoben am 03.10.2026** bis auf den Entscheid zum Umfang. Neu u. a.: Aufgaben 5f (Wurf) und 5g (Minimum),
Übung «Extremwert aus der Grundform», Nullstellen-Übung mit Anzahl 0/1/2, Fragen im Clip: Spulen nur
noch ausdrücklich, R setzt Fragen zurück (`FRAGEN_JS`); 4 Clips neu vertont (11 Clips 10:54).

### Wichtig

- [x] **Extremwerte nur über Nullstellen-Mitte geübt** (TODOx 01, 16): Kapitel 5 (5a–5e, Clips
  `mitte`, `kontrolle-extremwert`) übt nur «Nullstellen → Mitte». G7 (Wurf) und G8 (Minimum, \(D \lt 0\))
  verlangen \(-\frac{b}{2a}\) bzw. Scheitelform. → Festhalten mit allgemeinem Vorgehen (Variable,
  Zielfunktion, zulässiger Bereich, Scheitel, Art des Extremums, Antwort), Aufgabe Wurf \(h(t)\) in
  Grundform, Aufgabe mit Minimum; in den Clips die Nullstellen-Mitte als Abkürzung kennzeichnen.
- [x] **Aufgabenleiste meldet «Alle Aufgaben gelöst» auch nach Überspringen** (TODOx 07,
  `seite.js:96`). → gelöst/übersprungen zählen, Rückweg zu offenen Aufgaben.
- [x] **Neustart mit R setzt die Fragen nicht zurück** (TODOx 22, `build-clips.py:848`, `:1560`):
  `erledigt` wird nie geleert.
- [x] **Frage 1 kann beim Laden übersprungen werden** (TODOx 27): Auslöser `t − letzt < 0.3`, Frage 1
  bei 0.35 s; ein verspätetes erstes Bild gilt als Spulen. → nachstellen, Spulen ausdrücklich erkennen.
- [x] **Themenseite g3-3** (TODOx 23): Zeile 901 «das Minuszeichen … macht das Vorzeichen von u im
  Punkt positiv» (gleicher Fehler wie oben HOCH 1); Zeile 422 «Jede quadratische Funktion … in drei
  äquivalenten Formen» ohne «Produktform nur bei \(D \ge 0\)».

### Mittel

- [x] **Nullstellen-Übung** nur \(a = 1\) mit zwei ganzzahligen Nullstellen (TODOx 03) → auch
  \(a \ne 1\), \(D = 0\), \(D \lt 0\) mit Antworten «eine»/«keine».
- [x] **Zufallsgraph «Graph → Gleichung» ohne Achsenzahlen** (TODOx 11, `seite.js:467`).
- [x] **Zeitplan** (TODOx 20): jedes Kapitel fix «≈ 30 min», Lektion 2 und 3 je zwei Kapitel; die
  Kapiteltests sind gewachsen. → Zeiten je Kapitel neu schätzen, Lektionen neu aufteilen.
- [x] **Selbsteinschätzung verspricht zu viel** (TODOx 06): «Sitzt. K1–K4 im Griff» bei 22 P auch ohne
  G7. → «Die geprüften Teile sitzen; jede Aufgabe mit Abzug → ihr Kapitel» (Seite und Paket).
- [x] **Produktform = reelle Linearfaktoren** (TODOx 09), bei \(D = 0\): \(a(x-x_1)^2\); 2d «keine
  reellen Nullstellen».
- [x] **Zulässige Bereiche in Sachaufgaben** (TODOx 15): 4c, 5a–5c, G6–G8.
- [x] **Sim 2, Aufgabe zu \(y_s\)** setzt stillschweigend \(a \gt 0\) voraus (TODOx 12, Zusatz) — prüfen.

- [x] **Entscheid Auftraggeber: Umfang über HOWTO §3.** → Variante 3 (03.10.2026): §3 unterscheidet jetzt klassisch / Kapitelmuster (bis 5 Lektionen, Kapitel 35–45 min). Ehrlich geschätzt ≈ 235 min (Kapitel 35–45 min,
  rund fünf Lektionen + Gesamttest); §3 sagt «höchstens 30 min je Kapitel», «mehr als 4 Lektionen →
  teilen». Möglichkeiten: in zwei Leitprogramme teilen (Kapitel 1–3 / 4–5), Aufgaben als Vertiefung
  markieren und aus der Zeit nehmen, oder §3 für dieses Format anpassen.

### Klein

- [x] Ansatz «Scheitel + Punkt»: \(x_P \ne x_s\) (TODOx 10).
- [x] Clip `kontrolle-formen` F1: «Der Faktor 0.5 streckt nur» → «ändert nur die Form» (TODOx 17).
- [x] Vortest: zu jeder Aufgabe der Rückweg (0b → Binome, 0c/0d → g2-2) (TODOx 19).
- [x] Häkchen der Kapitelnavigation als «bearbeitet» beschriften (TODOx 26).

## Abnahme durch den Auftraggeber

- [ ] **Hörprobe** der 10 Leitprogramm-Clips: Aussprache von «x s», «y s», «x plus eins in
  Klammern», «null Komma fünf», «D», «Symmetrieachse»; in den 5 Kontrollclips je eine Frage
  absichtlich falsch beantworten, damit auch die Rückmeldungen zu hören sind. Fundstellen
  (Clip, Sekunde) melden → Sprechertext bzw. Aussprachetabelle anpassen, neu vertonen.
- [ ] **KI-Bewertung durchspielen**: eine echte (oder realistisch fehlerhafte) Schülerlösung
  des Gesamttests zusammen mit `bewertungspaket.pdf` einer KI geben; prüfen, ob Punkte,
  Folgefehler und Rückmeldung stimmen. Kriterien danach schärfen.

## Übertrag und Werkzeug

- [ ] `scripts/abgleich.py`: `build-clips.py` liegt bei 74.3 % (Grundlinie 84 %). Eintrag in
  `OFFEN` erst nach Abnahme — vorher `python3 scripts/abgleich.py --diff scripts/abgleich.py`.
- [–] Physik-Übertrag: steht in `TODO-schwesterprojekt.md` (zwei Einträge vom 02.10.2026),
  wird in einer Physik-Session abgearbeitet.

## Ältere Leitprogramme ans Vorbild angleichen

- [ ] `potenzen`, `quadratische-gleichungen`, `gleichungssysteme`: Warnkasten orange statt rot,
  `\mathbb{L}` statt `L` (gezählt 02.10.2026: `quadratische-gleichungen` 34 ×
  `\(L =`, `gleichungssysteme` 8 ×, `potenzen` 0) — per Skript, danach Pre-Flight.
- [ ] Entscheid offen: Sollen diese Leitprogramme auch auf das Kapitelmuster
  (Einführungsclip → Animation mit Aufgabenleiste → Kontrollclip) und auf Gesamttest als PDF
  umgestellt werden, oder bleibt das neuen Leitprogrammen vorbehalten?

## Ideen (ohne Auftrag)

- [ ] Verteiltes/gemischtes Üben über die Kapitel, adaptiver Weg nach dem Vorwissenstest.
- [ ] Bewegte Grafen im Clip (`bewegung`) über Parabeln hinaus (Geraden, Exponentialfunktionen)
  — Voraussetzung für weitere Leitprogramme dieser Art.

---

## Prüfung Lineare Funktionen (03.10.2026)

Seite: `leitprogramme/lineare-funktionen.html`, gebaut aus
`scripts/lp/lineare-funktionen/seite.py` + `seite.js` (Änderungen dort, nicht in der HTML-Datei);
Clips aus `clips.py`, PDFs aus `downloads/leitprogramme/lineare-funktionen/*.tex`.

Drei unabhängige Agenten (Seite, Clips, PDFs) nach `/lp-pruefung`, Stand Commit `bb34526`.
Geprüft wurden Vorwissen, vier Kapitel, Aufgaben und Selbsttests, die vier Simulationen mit
ihren Aufgabenleisten, elf Zufallsübungen, neun Clips, Gesamttest und Bewertungspaket.

**Rechenfehler: keine.** Alle Zahlen in Vortest, Aufgaben 1a–4e, Festhalten-Kästen, Minigrafen,
Clips und beiden PDFs stimmen (`python3`); die elf Übungsgeneratoren liefern nur lösbare
Aufgaben und werten keine richtige Antwort als falsch (je 2000 Zufallsfälle). Alle Ziele der
Aufgabenleisten liegen auf dem Reglerraster und sind im Startzustand nicht erfüllt.
Punkte: Vortest 10, Kapitel 13/12/11/14, Gesamttest 9 + 5 + 8 = 22 — überall deckungsgleich.

**Alle Befunde behoben am 03.10.2026**, zusammen mit dem Entscheid des Auftraggebers,
die Clips zu **bewegen** und Fragen beider Typen (`wahl` und `klick`) zu stellen.

---

### HOCH — fachlich falsch oder im Widerspruch zur Seite

- [x] **Clip `kontrolle-typen`, Frage 4:** Die Frage nennt \(g: y = 4x - 1\), gezeichnet war
  \(\{m: 4,\ q: 1\}\). Bild und Text widersprachen sich. → `q: -1`; die Frage ist jetzt
  ausserdem eine `klick`-Frage, bei der \(g\) allein im Bild steht.
- [x] **Nullstellenformel ohne ihre Bedingung** (4 Stellen in `steigungsdreieck` und
  `kontrolle-steigung`): Bild zeigte nur \(x_0 = -\frac{b}{m}\), Seite und Themenseite
  schreiben \((m \neq 0)\) dazu. → Erst das allgemeine Verfahren
  (\(0 = mx + b \Rightarrow \ldots\)), dann die Abkürzung, mit Bedingung.
- [x] **Clip `typen`, «Vier Typen»:** «vier Fälle … unterscheiden sich nur in m und b» — der
  vierte Fall \(x = 3\) hat weder \(m\) noch \(b\). → «Drei davon … und einer fällt aus der
  Reihe: Er ist gar keine Funktion.»
- [x] **Clip `kontrolle-aufstellen`, Frage 3:** Rückmeldung «Bruch verkehrt: Δy = −4 geteilt
  durch Δx = 4» ergibt \(-1\) — die *richtige* Antwort; der Distraktor war \(-0.25\).
  → Distraktor \(-4\) («Δy ohne Teilen»), Rückmeldung passend.
- [x] **Übung «Typ erkennen» wertete richtige Antworten als falsch:** Bei \(f(x) = x\) galt
  nur «Identität», obwohl die Lösung von Aufgabe 3a selbst «auch proportional» sagt.
  → Frage lautet «Welcher Typ passt **am genauesten**?»; Tabellenzeile und Optionsname
  («senkrechte Gerade (keine Funktion)») angeglichen.
- [x] **Restpunkte in G6 widersprachen der eigenen Bedingung:** «\(m = -10\) … Rest
  folgerichtig → 2 von 3 P (Typ nur, wenn \(b\) wirklich 0 ist)» — mit \(m = -10\) ist
  \(b = -24\). → Eine Regel für alle Folgefehler der Aufgabe: «Die Typ-Zeile zählt, wenn
  die Typ-Aussage zum selbst gefundenen \(b\) passt.»
- [x] **«es gibt keine Nullstelle» in G8 war falsch** (sie liegt bei \(t = -25\), nur
  ausserhalb des Sachbereichs). → Aufgabe auf ein neues Modell (Kerze) gestellt und die
  Begründung auf «liegt vor dem Beginn» geändert.
- [x] **(E) und (A) waren widersprüchlich definiert** — G1 liess die Nullstelle «ohne
  Rechnung» gelten, G3 verlangte bei einer (E)-Zeile ausdrücklich den Weg. → Drei Stufen
  sauber getrennt, in Abschnitt 3 und im KI-Auftrag gleichlautend.

### MITTEL — irreführend, doppelt oder didaktisch verfehlt

- [x] **Der Clip über das Steigungsdreieck zeigte nie ein Steigungsdreieck** (vier Szenen),
  ebenso `typen` «Warum minus eins». → Neuer Begleiter `dreieck` am bewegten Graphen:
  Katheten, Δx und Δy laufen mit, und in «Kleines Dreieck» schrumpft es sichtbar, während
  der Quotient bleibt.
- [x] **«Die Gerade steht senkrecht» — es war keine Gerade im Bild** (`steigungsdreieck`
  «Delta x null», `kontrolle-steigung` F5). → Punktleiter über die ganze Fensterhöhe, wie
  in den Typen-Clips.
- [x] **Ton und Bild drehten das Dreieck in verschiedene Richtungen** (`typen` «Warum minus
  eins»). → Ton auf «aus zwei zu eins wird minus eins zu zwei», passend zum Bild.
- [x] **Formel ≠ Ton ≠ Antwortoption** (`kontrolle-m-und-b` F3: «\(y = -1x + 3\)» gegen
  «y = −x + 3»). → `y = \fa{-}x + \fb{3}`.
- [x] **Die Lösung stand im Bild, bevor sie gerechnet wurde** (`aufstellen`, drei Szenen:
  die fertige Gerade war schon da, \(b\) also ablesbar). → Die Gerade wandert jetzt mit
  noch offenem \(b\) durchs Bild und rastet erst beim Einsetzen auf \(P\) ein.
- [x] **Bild lief dem Ton um elf Sekunden voraus** (`m-und-b` «Wertetabelle»). → Tabelle
  `ein: 5.9`, Punkte `ein: 11.3`, beides nach `sprechzeiten.py`.
- [x] **Rückmeldungen rechneten die Lösung vor** (sechs Stellen; es gibt nur einen Versuch).
  → Alle auf die Blickrichtung umgestellt («Was fehlt im Bruch noch?» statt «4 nach rechts,
  2 hinunter»).
- [x] **Beide Stützpunkte waren beim Erscheinen der Frage schon markiert und farbcodiert.**
  → Die bewegte Gerade startet neutral; Begleiter und Beschriftung erscheinen mit der
  Auflösung.
- [x] **Verzerrtes Gitter dort, wo das Auge Schritte zählen soll** (`m-und-b` Szenen 1–2:
  Verhältnis 1.71, die Steigung 2 sah aus wie 1.17). → Fenster quadratisch (12 × 12).
- [x] **Kompetenz K1 («Graph als Gerade darstellen») wurde im Gesamttest geprüft, aber
  nirgends geübt.** → Neue Aufgabe 1e in Kapitel 1 (zwei Geraden zeichnen, mit Lösungsbild);
  Kapiteltest 11 → 13 P; Kapitelziel 1 nennt das Zeichnen.
- [x] **G1 wiederholte Selbsttest 2c wörtlich** (dieselbe Funktion, dieselben Stützpunkte).
  → G1 auf \(f(x) = 0.5x - 2\), G3 auf \(f(x) = -3x + 6\), G8 auf ein neues Sachmodell.
- [x] **G2 verriet das verlangte Ergebnis:** Der markierte Punkt \((-3 \mid -4)\) *war*
  \(f(-3)\). → Nur noch \((0 \mid -2)\) und \((3 \mid 0)\) markiert.
- [x] **Dieselbe Einsicht wurde zweimal geprüft** (G4c und G5 fragten beide, warum
  \(x = k\) keine Funktion ist) — mit zwei verschiedenen Massstäben. → G4c gestrichen,
  dafür eine Entscheidungsaufgabe («Steht \(h\) senkrecht auf \(g\)?»), die das bis dahin
  ungeprüfte Kapitelziel 3 abdeckt.
- [x] **G4a trivialisierte das Verfahren, das es prüfen soll** (Punkt lag auf der
  \(y\)-Achse, \(b\) also ablesbar). → \(P(2 \mid -3)\).
- [x] **Animations- und Selbsttest-Aufgaben nahmen Clip-Zahlen** (Kapitel 4 Ziel 1 war
  zahlengleich mit dem Einführungsclip; Kapitel 2 Ziel 6 mit dem Kontrollclip; 2a mit zwei
  Kontrollfragen und der Warnbox darüber; 3b und 3c mit Kontrollfragen; die Warnbox in
  Kapitel 4 nannte 7 als falsch, während 4a(i) 7 als Lösung hat). → Alle entkoppelt.
- [x] **Zufallsübungen konnten eine Gesamttest-Aufgabe exakt treffen** (je ≈ 2 %).
  → Liste `FEST` in `seite.js` mit jeder Geraden, nach der eine feste Aufgabe fragt; der
  Generator würfelt neu, wenn er sie trifft. Dasselbe für die Ziele der Simulationen geprüft.
- [x] **Falsche Diagnose bei \(b = 0\)** in «Beschreibung → Gleichung»: \(-0 = 0\) liess den
  Vorzeichen-Zweig anschlagen, obwohl \(b\) richtig war (≈ 8 % der Aufgaben).
- [x] **Live-Anzeige rundete ohne «≈»** (Nullstelle in Simulation 2, 56 von 240 Fällen).
- [x] **Lösung mit 16 Dezimalstellen** in «parallel oder senkrecht» (\(m_2 = -0.333\ldots\)),
  während der Hinweis \(-\tfrac13\) schreibt. → \(\pm 3\) aus der Liste genommen.
- [x] **Der Vorwissen-Clip beantwortete den Vortest, der unter ihm steht** (dieselbe
  Wertetabelle). → Vortest 0d auf andere Stellen.
- [x] **Sachaufgaben ohne zulässigen Bereich** (Taxi, Behälter: negative Kilometer und
  Minuten im Bild, kein Wort dazu). → Fenster ab 0 bzw. Notiz «sinnvoll nur für \(x \geq 0\)»,
  und Aufgabe 4d nennt die Definitionsmenge jetzt mit.
- [x] **Simulation 4 war die dünnste bei der längsten Kapitelzeit** (3 Aufgaben, keine
  Erkunde-Aufgabe, der Fall «senkrecht» fehlte). → 5 Aufgaben mit Erkunden und Fall D.
- [x] **Die Punktprobe stand in keinem Festhalten-Kasten**, wurde aber dreimal verlangt.
- [x] **Lektion 1 wäre mit dem Vorwissen 50 Minuten lang gewesen.** → Vorwissen als «Vorab»
  ausgewiesen; die vier Kapitel sind die vier Lektionen.
- [x] **22 Punkte in 20 Minuten ohne Rechner sind knapp.** → 25 Minuten, auf Seite und PDF.
- [x] **G2 verlangte eine Drittel-Steigung, die nirgends geübt wird.** → Übung «Graph →
  Gleichung» würfelt jetzt auch Drittel.
- [x] **Regelungslücken im Raster** (G1 ohne Toleranz und ohne Fall «Gerade richtig, Punkte
  nicht notiert»; G3a und G5 ohne Regel für teilrichtige Zeilen). → Ergänzt, dazu eine
  allgemeine Zeile «Teilrichtige Zeilen».
- [x] **Zwei Konventionen für dieselbe Klammer-Schreibweise** im Raster (G6 zählte den
  bedingten Punkt mit, G8 nicht). → Einheitlich «1–2 von 3 P, je nachdem ob …».
- [x] **G3(c) prüfte etwas anderes, als das Kriterium sagte** («ohne Aussage über den
  Zuwachs», akzeptiert wurde aber «steigt, weil m > 0»). → Kriterium ist die Richtung.

### NIEDRIG — Kleinigkeiten und Konvention

- [x] Clipzeiten auf der Seite waren je 3 s zu lang (`nachlauf` mitgezählt, anders als in
  der Bibliothek und beim Vorwissen-Clip auf derselben Seite). → Jetzt ohne `nachlauf`.
- [x] `\frac` statt `\dfrac` (26 Stellen in den Drehbüchern) — im Bild sichtbar klein.
- [x] «Achsenabschnitt» statt «\(y\)-Achsenabschnitt» (4 Stellen in den Clips).
- [x] Eine Gerade in Orange (`kontrolle-m-und-b` F2), während Orange im ganzen
  Leitprogramm \(b\) bedeutet; Notizfarben ohne Muster. → Farbregel im Kopf von `clips.py`
  festgeschrieben und durchgezogen; Grün heisst jetzt ausdrücklich «stimmt»
  (Nullstelle, Treffer, Probe).
- [x] Unicode-Bruch «⅓» unter lauter Dezimalzahlen (`kontrolle-aufstellen` F4). → Distraktor
  ersetzt.
- [x] Bruch und Dezimalzahl für dieselbe Zahl in einer Zeile (`aufstellen` «Aus einer Lage»).
- [x] Ungleichmässige Achsenteilung (`kontrolle-steigung` F3: 0, −10, 5).
- [x] «Gelesen wird **immer** von links nach rechts» — und direkt danach das Gegenbeispiel.
  → «Am bequemsten …».
- [x] «halbiert **den** rechten Winkel zwischen den Achsen» (es sind vier). → «den Winkel
  zwischen der positiven \(x\)- und der positiven \(y\)-Achse».
- [x] `\Rightarrow` statt `\Longrightarrow`; blaues statt rotes \(m\) in einer Merknotiz.
- [x] Kontrollfrage, die rechnerisch die Kopie des Clip-Beispiels war
  (`kontrolle-steigung` F2). → Neue Zahlen.
- [x] Falscher Lösungskommentar zu Aufgabe 1a («A und C schneiden die \(y\)-Achse über» —
  C schneidet sie bei \(-3\)).
- [x] «Nullstellen von \(4x - 6\)» — Nullstellen gehören zu einer Funktion, nicht zu einem
  Term (zwei Stellen).
- [x] «\(b = -6\) der Schnittpunkt mit der \(y\)-Achse» — \(b\) ist der Achsenabschnitt,
  der Schnittpunkt ist \((0 \mid -6)\).
- [x] «senkrecht zu \(g\)» in der Ansatz-Tabelle ohne Bedingung \(m_g \neq 0\).
- [x] Toter Code (`FAELLE[*].ziel`) und eine Vorgabe, die als Hilfslinie ausblendbar war.
- [x] Eingabemuster `f(xₚ)` führte ein Zeichen ein, das sonst nirgends vorkommt.
- [x] Minigrafen der Aufgaben färbten \((0 \mid b)\) und die Nullstelle neutral, die Übung
  dagegen farbig. → Überall dieselbe Bedeutung.
- [x] 3b-Kommentar begründete nur ein Paar; `g_4` gegen `g_2` blieb offen.
- [x] Kapitelziel 3 sprach von «Koeffizienten» auch für \(x = k\) und liess die Identität weg.
- [x] «Hilfsmittel: keine» schloss im Gesamttest das Lineal aus, obwohl G1 zeichnen lässt.
- [x] Teil-Titel deckten ihren Inhalt nicht («Teil A · … lesen» enthielt das Zeichnen).
- [x] Schreibfläche `\lpplatz` schnitt die Unterlängen der letzten Textzeile an — geerbt vom
  Vorbild, darum in `lp-druck.sty` behoben (beide Leitprogramme neu gebaut, Text unverändert).
- [x] Zu wenig Schreibfläche bei G1–G3; (A) in G5 zweckentfremdet; Bruch mit negativem Nenner.
- [x] Zuordnung Aufgabe → Kapitel: G6 beginnt mit der Steigung und gehört auch zu Kapitel 2.

### Bewusst nicht geändert

- [–] **Nullstelle, parallel/senkrecht und die Typentabelle stehen nicht wörtlich im RLP 3.2.**
  Sie sind über K2 («Koeffizienten geometrisch interpretieren») gedeckt und auf der
  Themenseite 3.2 — dem Massstab nach HOWTO §1.2 — ausgebaut. Das Leitprogramm geht nicht
  über die Themenseite hinaus.
- [–] **Themenseite 3.2 bleibt unberührt.** Die Prüfung hat dort keinen Widerspruch gefunden.
