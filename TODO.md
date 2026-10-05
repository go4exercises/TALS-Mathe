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

- [ ] `scripts/abgleich.py`: `build-clips.py` liegt am 03.10.2026 bei **94.2 %**
  (Grundlinie 84 %) — die Datei ist dem Schwesterrepo also *näher* als die Grundlinie
  verlangt, und das Skript bittet um das Nachtragen der höheren Grundlinie. Eintrag in
  `OFFEN` und neue Grundlinie erst nach Abnahme, und vorher
  `python3 scripts/abgleich.py --diff scripts/abgleich.py`: die Datei selbst steht bei
  93.1 % gegen Grundlinie 100 %, drüben liegt also eine neuere Fassung.
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
- [x] Bewegte Grafen im Clip (`bewegung`) über Parabeln hinaus: **Geraden** (`[t, m, q]`,
  02.10.2026) und **Potenz-, Hyperbel- und Wurzelkurven** (`[t, a, p, u, v]` für
  \(a(x-u)^p + v\), 03.10.2026) stehen, mit den Begleitern `yachse`, `nullstelle`,
  `marken`, `laeufer`, `dreieck`, `startpunkt`, `asymptoten` und `spiegel`.
  Offen bleiben Exponential- und Logarithmusfunktionen — sie brauchen einen eigenen
  Schlüssel, weil \(a \cdot b^{x}\) nicht in \(a(x-u)^p + v\) passt.

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

---

## Prüfung Potenz- und Wurzelfunktionen (03.10.2026)

Seite `leitprogramme/potenz-wurzelfunktionen.html`, gebaut aus
`scripts/lp/potenz-wurzelfunktionen/seite.py` + `seite.js`; Clips aus `clips.py`;
PDFs unter `downloads/leitprogramme/potenz-wurzelfunktionen/`. Drei Agenten gegen die
Prüfliste (HOWTO-leitprogramme §15), alle Zahlen mit `python3` nachgerechnet.

**Rechenfehler in den Inhalten: keine.** Vortest 0a–0d, Aufgaben 1a–5e, Festhalten-Kästen,
Minigrafen, alle 25 Kontrollfragen, alle Stützpunkte der Bewegungen und beide PDFs stimmen.
Die 17 Übungsgeneratoren liefern immer lösbare Aufgaben, keine richtige Antwort wird als
falsch gewertet (je 2000 Zufallsfälle), jede Diagnose ist für die auslösende Eingabe wahr.
Alle fünf Aufgabenleisten sind im Reglerraster erfüllbar und keine im Startzustand.
Punkte: 9 + 10 + 5 = 24, deckungsgleich in Test, Paket, Selbsteinschätzung und Seite.
RLP-Bindung wörtlich aus `Math-SP.pdf` belegt.

**Behoben am 03.10.2026** — bis auf den einen Punkt, der dem Prüfer selbst gilt.
Entscheid des Auftraggebers zur Definitionsmenge: Das Leitprogramm behält \(D = \mathbb{R}\)
für ungerade Wurzeln und benennt die Abweichung; die Themenseite 3.2b wird in einem
eigenen Durchgang nachgezogen (eigener Abschnitt unten).

### HOCH

- [x] **Alle bewegten Geraden und Kurven standen still.** `scripts/build-clips.py`,
  `BEWEGUNG_JS`: `bewegeGerade` und `bewegeKurve` lasen `T.L.t0`, aber `T.L` ist das
  DOM-Element — `t0` lag nur auf dem Hüllobjekt in `BEW`. `t - undefined` ist `NaN`,
  und `bewZustand` fällt bei `NaN` auf den **letzten** Stützpunkt. Gemessen: Pfad über
  die ganze Szene unverändert im Endzustand. Betroffen waren 17 Szenen in 6 der neuen
  Clips **und alle bewegten Geraden des freigeschalteten Leitprogramms Lineare
  Funktionen**. Nur der Parabel-Zweig (`L.t0` aus dem Hüllobjekt) war richtig.
  *Behoben:* jedes Teil trägt sein eigenes `t0`; 28 Clips neu gebaut, Bewegung in allen
  drei Zweigen im Browser nachgemessen.
- [x] **Kapitel 5 widerspricht der Konvention der Themenseite 3.2b.** Dort:
  «… beschränkt man sie **in diesem Kapitel durchgehend auf \(D = \mathbb{R}_0^+\)**»,
  ausdrücklich auch für die Kubikwurzel. Das Leitprogramm lehrt \(D = \mathbb{R}\) bei
  ungeradem Wurzelexponenten — im Festhalten, in sim5, im Clip `s3-2-lp-wurzel`
  («Definitionsmenge», «Merke»), in `kontrolle-wurzel` Frage 2 und in Aufgabe 5a.
  Auch der Vorwissensclip `s1-2-anim-exponenten-treppe` sagt «für a grösser null».
  **Die Themenseite ist dabei selbst uneins** (ein Kasten schreibt
  «\(f^{-1}: y = \sqrt[3]{x}\) mit \(x \in \mathbb{R}\)»). Entscheid des Auftraggebers
  nötig; HOWTO verlangt: nicht still angleichen, melden.
- [x] **Fünf Fragen zeigen ihre Antwort, wenn sie erscheinen** (§15). `kontrolle-exponent`
  F3: die Marke ist mit «(1 | 1)» angeschrieben — genau das Klickziel. `kontrolle-hyperbel`
  F3: der Punkt «(−2 | −0.5)» steht angeschrieben im Bild; zudem zeigt die versteckte
  Kurve \(1/(x-2.6)\), die Frage spricht von \(1/x\). `kontrolle-wurzel` F3: beide
  Stützpunkte tragen den Endzustand, der grüne Startpunkt-Ring sitzt auf dem Klickziel.
  `kontrolle-verschieben` F1/F2: mit dem Stillstand (oben) stand der Startpunkt
  «(2 | 0)» bzw. «(0 | 3)» von Anfang an da — nach dem Fix nochmals ansehen.
- [x] **Die Übung «Einschränken nötig?» ist entartet.** `seite.js`, Typ `einschraenken`
  würfelt \(n \in \{2…7\}\); die `FEST`-Liste sperrt `[1,2,0,0]` … `[1,6,0,0]`, also
  alles ausser \(n = 7\). 20 000 simulierte Würfe: \(n = 7\) in 99.94 %. Die Antwort ist
  praktisch immer «nicht nötig», der gerade Exponent — der Punkt von Kapitel 4 — wird
  nie geübt.
- [x] **Die Zufallsübungen können fünf Gesamttest-Aufgaben auswürfeln** (§15).
  Nicht in `FEST`: G1 \((-2,3,0,0)\), G2 \((0.5,4,0,0)\), G3 \((-2,-2,0,0)\),
  G4 \((1,4,1,-16)\), G7 \((2,2,-3,-4)\) — dazu die Kapitelaufgaben 1a, 1c, 2a, 2b, 3a,
  3c, 4a, 4b, 5b, 5e und Vortest 0d. Nach dem zweiten Fehlversuch zeigt die Übung die Lösung.
- [x] **«Ordnung» und «Exponent» verwechselt.** `s3-2-lp-hyperbel`, Szene «Die Ordnung
  wächst»: «Jetzt wächst die Ordnung: von minus eins über … bis minus vier.» Die Ordnung
  ist positiv und wächst von 1 auf 4; der Exponent fällt von −1 auf −4. Ebenso im Merke:
  «Negatives n gibt eine Hyperbel n-ter Ordnung» mit dem Bild \(y = x^{-n} = 1/x^n\) —
  `n` steht im selben Satz für beides. Zieht Neuvertonung zweier Szenen nach sich.
- [x] **Rundung macht Lösungen falsch.** `seite.js`, Typ `vergleich`: `z()` rundet auf zwei
  Stellen, also «\(0.04^2 = 0\)», «\(0.09^2 = 0.01\)», «\(0.16^2 = 0.03\)» — und
  «\(= 0\)» widerspricht der Ordnungsaussage derselben Aufgabe. Kein «≈».
  *Behebung:* `String(A.x*A.x)`; die vier Startwerte sind in IEEE exakt.

### MITTEL

- [x] **Rasterfehler im Bewertungspaket.** G1: «\(f(-2) = 24\) (Exponent als Faktor)» —
  \(-2 \cdot 3 \cdot (-2) = 12\), 24 ist aus keinem Fehler erreichbar. G7:
  «\(x_0 = 5\) (die 2 nicht weggeteilt, also \(\sqrt{x+3} = 4\))» — das gibt \(x = 13\);
  5 entsteht aus \(2(x+3) = 16\). G5: «\((-6 \mid -2)\) (an einer Achse gespiegelt)» —
  das ist die Spiegelung an \(y = -x\). G7: zwei Zeilen geben \(S(3 \mid -4)\)
  widersprüchlich 1 oder 0 Punkte. G8: «ein Zahlenbeispiel … kann es nicht geben» ist
  falsch (\(x = 4\): \(16 > 4 > 2\)) — es liegt nur ausserhalb des Bereichs.
- [x] **G2 ist aus der Abbildung nicht eindeutig lösbar.** Markiert sind nur
  \((\pm 2 \mid 8)\); \(2x^2\), \(0.5x^4\), \(0.125x^6\) erfüllen das alle. Die
  Musterlösung begründet nur «\(n\) gerade und \(n > 2\)». Der im Kapitel geübte Weg
  (\(f(1) = a\) ablesen) ist versperrt: \(f(1) = 0.5\) liegt zwischen zwei Gitterlinien.
- [x] **`a = 0` ist in sim1, sim2, sim3 und sim5 einstellbar**, obwohl das Festhalten
  \(a \in \mathbb{R}\setminus\{0\}\) definiert. sim3 behauptet dann Asymptoten für die
  Gerade \(y = v\). Der Exponentenregler wird mit `ohneNull()` um die 0 geführt — beim
  Faktor fehlt das Gegenstück. (sim1 fängt den Fall mit «Nullfunktion» ab.)
- [x] **Die Wertemenge wird abgefragt, aber nie eingeführt** (5 von 12 Punkten in
  Kapitel 2: Aufgaben 2b und 2e). Der Begriff kommt sonst nur einmal vor — im Festhalten
  von Kapitel **4**, also nach dem Test.
- [x] **Der Gesamttest wiederholt Selbsttests.** G1 ist Aufgabe 1b mit **denselben**
  Argumenten (\(f(-2)\), \(f(0.5)\) zu \(-2x^3\)), dazu G1(b) ↔ 1c, G7 ↔ 5b, G8 ↔ 5d.
  Teil C ist damit ganz, Teil A zur Hälfte Wiederholung. (Derselbe Befund wie bei den
  Linearen Funktionen, dort behoben.)
- [x] **Kapitelziele ohne Gesamttest-Aufgabe.** K3 verspricht Verschiebung und
  mitgewanderte Asymptoten — geprüft werden nur die Nullstellen (G4). K5 verspricht
  «grafisch wie rechnerisch» — der ungerade Wurzelexponent und das grafische Lösen
  kommen nicht vor. Teil C trägt 5 von 24 Punkten für das namengebende Kapitel.
- [x] **Aufgabe 4d verweist auf eine Gerade, die im Bild fehlt.** Lösung: «Spiegelbild …
  an der **gestrichelten Geraden**»; der Minigraf-Renderer zeichnet nur `data-k` und
  `data-punkte`, keine Winkelhalbierende.
- [x] **Bild-Ton-Versatz.** `s3-2-lp-exponent` «a streckt»: bei «Zwei macht sie schmaler»
  ist \(a \approx 0.8\), bei «null Komma fünf breiter» bereits \(a \approx -0.42\).
  `s3-2-lp-verschieben` «v schiebt senkrecht»: die Bewegung endet 0.5 s bevor der Satz
  dazu beginnt. `s3-2-lp-hyperbel` «Ein neuer Fall»: das Bild kommt 2.1 s nach dem ersten
  genannten Punkt. (Alle drei waren bisher wegen des Stillstands unsichtbar — nach dem
  Fix neu messen.)
- [x] **`s3-2-lp-umkehren` «Das Rezept»: Ton nennt zwei Schritte, das Bild drei.**
  «… nach x auflösen, dann x und y vertauschen, **fertig**» gegen «3. Definitionsmenge
  prüfen» — gerade der fachlich heikle Schritt wird nie gesprochen.
- [x] **`farbe: "orange"` wird still verworfen.** `build-clips.py` kennt nur
  `rot|blau|tinte|gruen`; unbekannte Namen ergeben `color:None`, das der Browser
  wegwirft. Betroffen: die beiden Notizen, die den Exponenten erklären
  (`s3-2-lp-exponent` «n wächst», `s3-2-lp-hyperbel` «Die Ordnung wächst») — sie stehen
  schwarz statt orange. Dieselbe Panne in fünf `g3-2-lp-*`-Clips.
  *Behebung:* `gold` (#b85c00) in die Farbtabelle, oder beim Bau auf unbekannte Farbe abbrechen.
- [x] **Lösungen stehen in den Lehrclips ab Sekunde 0 im Bild.** `s3-2-lp-verschieben`
  «Nullstellen»: (1 | 0) und (5 | 0) angeschrieben, während der Ton 13.9 s darauf
  hinarbeitet. Ebenso `s3-2-lp-wurzel` «Verschieben wie immer» und «Grafisch lösen».
  In den Kontrollclips ist dasselbe über `ein`-Zeiten sauber gelöst.
- [x] **«Terrassenpunkt» wird abgefragt, ohne im Clip eingeführt zu sein**
  (`kontrolle-verschieben` F1; der Lehrclip benutzt das Wort nie).
- [x] **sim4, letzte Aufgabe hat zwei richtige Antworten:** «Welcher Punkt liegt bei
  jedem \(n\) auf beiden Kurven?» — \((0 \mid 0)\) und \((1 \mid 1)\), bei ungeradem
  \(n\) zusätzlich \((-1 \mid -1)\).
- [x] **`graf-potenz`: das Fenster wird breiter, je steiler die Kurve** (y-Bereich fest
  ±8, x gedehnt) — in 8 von 16 Aufgaben liegt \(f(2)\) ausserhalb, obwohl die Diagnose
  «Lies den Wert bei \(x = 1\) und bei \(x = 2\) ab» genau dorthin zeigt.
- [x] **Zwei Rückmeldungen verraten die Lösung:** `umkehrfunktion` nennt \(n\) im
  Klartext, `wurzel-nullstelle` rechnet bis zum letzten Schritt vor.
- [x] **Übung «Punkt spiegeln» spricht von \(f^{-1}\) ohne die Einschränkung** (bei
  \(n = 2, 4\) existiert sie nach dem eigenen Festhalten nicht ohne \(x \geq 0\)).
  Die Papieraufgabe 4c macht es richtig.
- [x] **«Flachpunkt» fehlt.** Die Themenseite 3.2a nennt \((u \mid v)\) bei geradem
  Exponenten «Flachpunkt», das Leitprogramm sagt durchgehend «Scheitel bzw.
  Terrassenpunkt». §10: fremden Namen einmal in Klammern nennen.
- [x] **Übung «Kurve → Gleichung»: «Der markierte Punkt liegt auf einem Gitterpunkt»
  stimmt in 6 von 16 Fällen nicht** (\(a = \pm 0.5\)).

### NIEDRIG

- [x] Intervalle als `[5;\infty[` statt `[5;\, +\infty[` (STYLEGUIDE §2.7) — 7 Stellen
  plus das Übungs-Muster und die sim5-Anzeige.
- [x] sim5 zeigt die gerundete Nullstelle ohne «≈» (318 von 2916 Reglerstellungen,
  z. B. «x₀ = 0.13» statt \(0.125\)).
- [x] Vier Clipzeiten auf der Seite abgerundet statt gerundet (0:55→0:56, 1:14→1:15,
  0:56→0:57, 1:01→1:02).
- [x] «Alle \(y = x^n\) gehen durch \((0 \mid 0)\)» steht unter der Definition mit
  \(n \in \mathbb{Z}\setminus\{0\}\) — für \(n < 0\) ist \(0 \notin D\).
- [x] «Bei geradem \(n\) gibt das Wurzelziehen zwei Lösungen» — bei \(-v/a = 0\) ist es
  eine. (Die Themenseite 3.2a lässt den Fall ebenfalls aus — melden, nicht angleichen.)
- [x] «Ordinatenabschnitt» wird in Aufgabe 5b verlangt, im Leitprogramm nie eingeführt.
- [x] Tote Verzweigung `A.n % 2 === 0 ? A.n + 1 : A.n + 1` in `graf-potenz`.
- [x] sim3 zeigt im Startzustand «verschoben um (0 | 0)».
- [x] Überlappung in `kontrolle-hyperbel` «Frage 2»: \(1/x^3\) stösst 7 px in die Notiz.
- [x] «null Punkt zwei fünf» statt «null Komma zwei fünf» in `kontrolle-wurzel` F5
  (repoweit sagen alle Clips «Komma»).
- [x] Gemischte Potenzschreibweise in `kontrolle-umkehren` F1 («y = x^(−5)» statt «x⁻⁵»).
- [x] `kontrolle-umkehren` F3 und `kontrolle-wurzel` F3: zwei identische Stützpunkte —
  Bewegungs-Overhead ohne Bewegung.
- [x] «Probe: \(2^3 - 2 = 6\)» in `s3-2-lp-wurzel` ist die Rückrechnung, nicht die Probe
  (\(\sqrt[3]{6+2} = 2\)).
- [x] Der Clip heisst «verschieben und strecken», zeigt aber kein Strecken.
- [x] `pruef-graf.py` prüft nur feste `punkte`, nicht die Begleiter bewegter Kurven —
  in `kontrolle-verschieben` F1 legt sich «(2 | 0)» über die Achsenmarke «3».
  *Behoben:* Der Prüfer rechnet die Begleiter jetzt mit (Rundung, Rand- und
  Achsenregel wie im Abspieler, 4 px Saum) und fand damit neun solche Stellen. Im
  Abspieler weicht ein Schild auf der x-Achse nach oben aus, wo keine Marken stehen,
  und jedes Begleiterschild hat einen Hof — vorher lief die Kurve durch die Schrift.
- [x] Bezugsgerade \(y = 2\) in `s3-2-lp-wurzel` «Grafisch lösen» ist blau statt Tinte;
  Startpunkt mal Tinte, mal grün. Grüne Punktfarbe im Minigrafen für gemeinsame Punkte.
- [x] G5 im Gesamttest hat die meisten Punkte (4) und die kleinste Schreibfläche.

### Folgt daraus — eigener Durchgang

- [x] **Themenseite `schwerpunkt/s3-2b-wurzelfunktionen.html` nachziehen.** Sie beschränkt
  im Kasten «💡 Konvention — die dritte Wurzel und der Definitionsbereich» alle
  Wurzelfunktionen auf \(D = \mathbb{R}_0^+\), widerspricht sich aber zwei Kästen weiter
  selbst («\(f^{-1}: y = \sqrt[3]{x}\) mit \(x \in \mathbb{R}\)»). Betroffen sind
  ausserdem die Definition (\(f : \mathbb{R}_0^+ \to \mathbb{R}_0^+\)), die
  Eigenschaften-Tabelle, die Erkenntnis des Transformations-Labors und der Kommentar
  `// Konvention: D = [u; ∞[ für jede Wurzel` im Seitenskript. Das Leitprogramm nennt
  die Abweichung seit dem 03.10.2026 ausdrücklich — die Themenseite sollte dieselbe
  Sprache sprechen.
  *Behoben:* Der Widerspruch ist weg. Der Konventionskasten ist jetzt die **einzige**
  Stelle, die einschränkt, sagt dass es eine Vereinbarung und keine Notwendigkeit ist,
  und nennt die andere Lesart samt Folge («keinen Startpunkt, \(D = \mathbb{R}\)»).
  Die Definition verweist darauf, der Umkehrbarkeits-Kasten behauptet nichts mehr, und
  die Kommentare im Seitenskript sprechen von «Vereinbarung dieser Seite». Die Seite
  bleibt bei \(\mathbb{R}_0^+\) — das ist eine verbreitete, begründete Wahl, und sie
  umzubauen hätte Definition, Tabelle, Animation und mehrere Aufgaben betroffen.
  Der Link auf das Leitprogramm kommt mit dem Kasten «🧭 Lieber geführt?» bei der
  Freischaltung (§13), nicht vorher.
- [–] **`s1-2-anim-exponenten-treppe`, Szene «Was man sich merkt»** sagt «a hoch ein
  halb ist die Wurzel aus a, für a grösser null». **Bestätigt sich nicht:** Der Satz
  gilt der *Potenzschreibweise* \(a^{1/n}\), und die ist in Teilgebiet 1.2
  ausdrücklich «für \(a \gt 0\)» definiert — der Clip gibt seine eigene Themenseite
  korrekt wieder und sagt nichts über \(\sqrt[3]{\;}\).
  *Dafür ein echter Befund an derselben Stelle, behoben:* Das Leitprogramm schrieb
  \(\sqrt[n]{x} = x^{1/n}\) **ohne Bedingung** und leitete zwei Absätze später
  \(D = \mathbb{R}\) für ungerades \(n\) daraus ab. Jetzt steht die Bedingung
  \(x \gt 0\) an der Gleichung, mit Verweis auf 1.2, und der Unterschied zwischen
  Schreibweise und Wurzelfunktion ist ausgesprochen — in Kapitel 5 und im Clip
  `s3-2-lp-wurzel` (eine Szene neu vertont).


---

## Externe Prüfung Lineare Funktionen (`../TODO-Lin.md`, ausgewertet 03.10.2026)

27 Punkte gegen die Live-Fassung 1.0. Jeden selbst an der Quelle nachgeprüft.
**Behoben: 01–07, 09–16, 18–22, 24** (und 08 war schon mit `6dc9244` erledigt).
Was offen bleibt, steht unten.

- [–] **08 — bestätigt sich nicht mehr.** «Vor der Antwort ist bereits die richtige
  Gerade samt beschriftetem \((0 \mid -5)\) sichtbar»: Das war eine Folge des
  Stillstands der bewegten Grafen (`T.L.t0` war `undefined`), der live noch drin war.
  Seit `6dc9244` steht die Gerade beim Fragen bei \(q = 4\) und wandert erst danach.
- [ ] **23 — Zugänglichkeit.** Die vier Klickfragen haben keine Tastaturalternative;
  unsichtbare Clip-Ebenen bleiben im zugänglichen Baum; nach einer richtigen Antwort
  geht es nach 1.3 s automatisch weiter. Das betrifft die **Clip-Maschine** in
  `scripts/build-clips.py`, also alle drei Leitprogramme und die 436 Clips — ein
  eigener Durchgang mit Entscheiden: Koordinateneingabe als gleichwertige Alternative?
  `aria-hidden` auf nicht aktive Ebenen? Weiter-Knopf statt Zeitschaltung?
- [ ] **25–27 — offene Abnahmetests**, ausdrücklich keine festgestellten Fehler:
  alle Kontrollfragen unter realen Bedingungen durchspielen (25), die 77 Tondateien
  hören (26), Geräte, Tastatur, Druck und ein echter Schülerdurchlauf (27). Liegen
  beim Auftraggeber; 26 betrifft nach den Neuvertonungen dieses Durchgangs alle neun
  Haupt- und 68 Fragetöne neu.
- [ ] **19 (Rest) — Gewichtung der Kapitel.** Die Zuordnung nach Fehlerart steht jetzt
  auf der Seite und im Paket. Offen bleibt, dass die vier Kapitel ungleich viele
  Gesamttest-Punkte tragen (Kapitel 4 deutlich am meisten); eine Wiederholung «nach den
  meisten verlorenen Punkten» bevorzugt es dadurch. Braucht eine Entscheidung über die
  Aufgabenverteilung, nicht nur eine Textänderung.

**Vom Prüfbericht ausdrücklich als gut bewertet und darum unangetastet:** der manuelle
Fortschritt «Aufgabenblöcke bearbeitet», die Trennung gelöst/übersprungen in der
Aufgabenleiste, der Schutz gegen mehrfaches Zählen derselben Lösung, die Sonderfälle im
Merkteil, der KI-freie Weg und die Handschriftkontrolle im Bewertungspaket.

---

## Prüfung Polynomfunktionen (04.10.2026)

Skill `/lp-pruefung leitprogramme/polynomfunktionen.html`, drei Agenten (Seite, Clips, PDFs),
Stand Commit `8fb85c4` (unverlinkt, noindex). `seite.*`/`clips.py` = `scripts/lp/polynomfunktionen/`,
`GT`/`BP` = `downloads/leitprogramme/polynomfunktionen/{gesamttest,bewertungspaket}.tex`.
Legende wie oben.

**Rechenfehler: einer** — `BP` G6, typischer Fehler «\(k(2) = -29\)» entsteht aus keinem
naheliegenden Fehler (\(+8\) statt \(-8\) gibt \(21\)). Sonst alles nachgerechnet und richtig:
Vortest, Aufgaben 1a–5d, Festhalten, Minigrafen, 25 Kontrollfragen samt Rückmeldungen,
Stützpunkte und Begleiter der bewegten Polynome (Bewegung über `__seek` abgetastet, läuft),
Gesamttest G1–G7 samt Folgefehler-Fällen, Punktesummen (10/13/12/11/14/14, GT 13 + 12 = 25).
Werkzeuge grün: `pruef-uebungen` (15 × 2000), `pruef-leiste` (5), `pruef-fragen` (5 × 9/9).
Nachgeprüft vom Hauptagenten: H1–H4, M1–M4, M6 an der Quelle bestätigt.

**Behoben am 04.10.2026** (Entscheid Auftraggeber zu H1: Themenseite führt beide Wege ein
und fragt beide ab — neuer Block «Linearfaktor abspalten — zwei Wege» mit Divisionsschema und
Ansatz, Aufgabe A3g; das Leitprogramm lehrt nur den Ansatz mit Koeffizientenvergleich, weil
er nur Ausmultiplizieren braucht). Themenseite 3.3 zusätzlich: Voraussetzung der
Linearfaktordarstellung (H3), Mini-Check «n − 1» (H2). Gesamttest neu: G1 dreifache
Nullstelle, G2 anderes Modell, G4 Mindestgrad, G6 Ablesen am Graphen mit Rand, G7 Grad 2,
G8 Flugbahn mit Ausklammern (25 P). Neu vertont: `vielfachheit`, `nullstellen-berechnen`,
`kontrolle-globalverlauf`, `kontrolle-nullstellen` (dort F4 jetzt Wahl statt Klick), Fragetöne
aller betroffenen Kontrollclips. Potenz/Wurzel: `ohneNull` ebenso behoben (M2).
Bewusst gelassen, mit Grund (`[–]` unten): Zielkurve grün (Konvention aller Leitprogramme),
Beschriftungen mit Hof über Achszahlen (lesbar), «Terrasse = dreifach» (Leitprogramm wie
Themenseite bis Vielfachheit 3), Vorwissensclip-Zeiten 1:03/0:49 (HOWTO §7: von der
Themenseite übernehmen), Gesamttest 30 min (25 P mit Rechner-Teil).

### HOCH

- [x] **H1 · Polynomdivision verlangt, nie gezeigt.** Clip `nullstellen-berechnen` («Abspalten»),
  Festhalten 4 und Sim 4 zeigen nur das Ergebnis \(x^2 - x - 6\); die Übung `abspalten` fragt nur
  die Nullstellen. 4b, 4c, Kontrollfrage 3 und GT G5 verlangen das Abspalten auf Papier.
  → Divisionsschema Schritt für Schritt in Clip (neu vertonen) und Festhalten, Übung mit dem
  Quotienten als Eingabe — oder das Abspalten über Ansatz \((x - x_1)(x^2 + px + q)\) und
  Koeffizientenvergleich lehren. RLP-Hinweis: GF 1.3 «ohne Polynomdivision auch ohne Hilfsmittel».
- [x] **H2 · Falsche Begründung «höchstens n − 1 Extremstellen».** `seite.js:691` («zwischen zwei
  Nullstellen liegt höchstens ein Hoch- oder Tiefpunkt») und Rückmeldung Kontrollclip
  Globalverlauf F2 («Zwischen Nullstellen liegen die Extremstellen»). Gegenbeispiel Aufgabe 3b:
  \(x^4 - 2x^2 - 3\), drei Extremstellen zwischen \(\pm\sqrt3\). → ohne Begründung «eins weniger als
  der Grad». **Themenseite 3.3** (Mini-Check Globalverlauf) hat denselben Satz — dort separat entscheiden.
- [x] **H3 · Voraussetzungen fehlen in Festhalten 1** (`seite.py`, fest1) und Merkbild Clip 1:
  Linearfaktordarstellung nur bei \(n\) reellen Nullstellen (mit Vielfachheit); «Faktor vorne =
  Leitkoeffizient» nur bei Klammern \((x - x_k)\) (5c: \(x(12-2x)^2\) hat \(a_3 = 4\)). Gleiche Lücke
  auf der Themenseite (Definition Linearfaktordarstellung) — melden, nicht still angleichen.
- [x] **H4 · «\(x^3 + x + 1\) ist nicht punktsymmetrisch»** (fest3, Häufiger Fehler): Der Graph ist
  punktsymmetrisch zu \((0 \mid 1)\). → «nicht punktsymmetrisch *zum Ursprung*»; Kontrollclip
  Globalverlauf F5 und Übung `symmetrie-poly` («weder noch») ebenso präzisieren.

### MITTEL

- [x] **M1 · Sim 4, Aufgabe 2 und 5 schon beim Erscheinen gelöst**, wenn die Probestelle auf einer
  gemeinsamen Nullstelle steht (\(-2\), \(1\) bei p0/p1; \(2\) bei p2/p3). → in `wechsle()` Regler auf 0.
- [x] **M2 · `ohneNull` wirkt nach `zeichnen`** (`seite.js`, Sim 1–3): Bild zeigt «Leitkoeffizient 0»,
  flache Kurve, Regler steht auf ±0.5. Aus Potenz/Wurzel übernommen — dort ebenso beheben.
- [x] **M3 · `gleichung-mehrfach`: Quadrat-vergessen bei \(d = -1\) gilt als richtig, bei \(d = 1\) Diagnose
  «Vorzeichen»** (ein Drittel der Würfe). → doppelte Nullstelle aus \(\{\pm2, \pm3\}\).
- [x] **M4 · Bild läuft dem Ton voraus**: Clip `linearfaktoren` «a streckt» (Spiegelung schon bei «Eins
  macht ihn doppelt so hoch», Ton 3.94–5.28 / 5.52–7.96 s) und `globalverlauf` «Ungerader Grad»
  (Wechsel auf \(a \lt 0\) bei 4.6–6.4 s, gesprochen gegen 8 s). → Stützpunkte nach `sprechzeiten.py`.
- [x] **M5 · Kontrollclip Globalverlauf F4**: \(2x^4 - x^2 + 3\) im Fenster \(y \in [-3; 3]\) — Minimum
  2.875, fast nichts sichtbar. → \(y\) etwa \([-1; 6]\).
- [x] **M6 · Übung `graf-vielfachheit`**: bei Nullstellenabstand 1 (40 % der Würfe) ist der Buckel
  1–2 px hoch, Berühren nicht erkennbar. → \(|b - s| \geq 2\).
- [x] **M7 · Zufallsübungen ohne Sperre gegen feste Aufgaben**: `extrem-ablesen` (trifft 5a, \(x^3-3x\),
  \(-x^3+3x+1\), 5d), `scheitel-extrem` (trifft **GT G6** samt Lösung, 5b, Clip-Beispiele),
  `lokal-global` (Clip «Am Rand»). → eigener Sperrschlüssel je Typ.
- [x] **M8 · Gesamttest wiederholt Modelle**: G7 = 5c (Schachtel, Maximum bei 2) und Clip-Schachtel;
  G2 ≈ 2b gespiegelt (\(a = -0.5\), \(|f(0)| = 2\)); G6 ≈ 5b (\(x_s = 2\)); G4 = 3d; G1 = Kontrollclip
  Vielfachheit F1 (2 doppelt, −1 einfach). Dazu: Aufgabe 1c = Kontrollclip Linearfaktoren F3.
  → neue Modelle.
- [x] **M9 · Kapitelziele ohne Gesamttest-Aufgabe**: H/T am Graphen ablesen (K3 «grafisch»),
  Ausklammern, dreifache Nullstelle, Polynomfunktion erkennen. → Ableseaufgabe in Teil B.
- [x] **M10 · Vortest 0c und Übung `ausklammern` rechnen «Produkt/Summe» verschieden** (Klammerzahlen
  vs. Nullstellen wie im Clip `g2-2b-quadratisch-faktorisieren`). → eine Lesart, ausdrücklich benannt.
- [x] **M11 · Raster für die KI**: G2 «falsches Vorzeichen in der Klammer → höchstens 3 von 4» ergibt
  nachgerechnet 2; G5 «Probe falsch → höchstens 1» widerspricht der Folgefehler-Regel; Satz ergänzen,
  dass (E)-Zeilen nie Folgepunkte sind. G6 −29 → 21 (siehe oben).
- [x] **M12 · Begriffe vor Einführung**: «Extremstellen» in Kapitel 3 (Clip, F2, Übung, 3b), eingeführt
  erst in 5; «gerade/ungerade Funktion» im Kontrollclip 3 vor dem Festhalten; \(f(-x)\)-Nachweis (3c)
  nur ein Satz ohne Beispiel. `grad-leitkoeff` (Kapitel 1) würfelt in 84 % Potenzen \((x-p)^k\),
  die erst Kapitel 2 einführt.
- [x] **M13 · Leistenziele = Clip-Beispiele**: Sim 4 A1 (\(x^3-2x^2-5x+6\)), Sim 5 A5 (\(D = [-1.5; 2.5]\)).
- [x] **M14 · Kapitel 4 ohne Aufgabe am Graphen** (HOWTO §9).

### NIEDRIG

- [x] Minigraf 1d: \((0 \mid 3)\) liegt nicht auf einer Gitterlinie (`sy = 2`) — Fenster \(-2,4,-5,5\).
- [x] `extrem-ablesen`: bei \(h_x = h_y\) falsche Diagnose «Erst die x-Koordinate»; vertauschtes T nicht erkannt.
- [x] «Rest» heisst einmal Divisionsrest, einmal Quotient (fest4, Übung `abspalten`, Clip) → «Quotient».
- [x] Gerundete Live-Werte ohne «≈» (Sim 5 Läufer, «(gerundet)»); Clip «Anwendung» H(2.83 | 379) ohne ≈.
- [x] Sim 5 letzte Aufgabe lehnt \(r = 2\) ab (Gleichstand, H bleibt absolutes Maximum) → \(r \le 2\).
- [x] Text ≠ Ton: Kontrollclip Nullstellen F3 Rückmeldung 1, F5 Rückmeldung 1.
- [x] Farben: Exponenten orange (`\fb`) bei der Symmetrie (Orange = Nullstellen) — entfärbt; [–] Zielkurve grün (Grün = H/T) — Konvention aller Leitprogramme;
  «Nah dran» \(x^3\) blau, Leitterm-Kurve Tinte. «Achse» ohne Zusatz (Notiz «Symmetrie», Übung).
- [x] Clip `vielfachheit` «Warum kein Wechsel»: auch \((x+2)\) behält sein Vorzeichen — fehlt; Marken zeigen \(f\), nicht \((x-1)^2\).
- [x] Kontrollclip Nullstellen F3/F4 am Bild ablesbar ohne Rechnen.
- [x] Clip `extrema` «Grad 2 exakt»: H(2 | 3) steht vor der Rechnung im Bild; «−1x²» → «−x²».
  Clip `nullstellen-berechnen` «Faktorisieren»: Graph 6.5 s weg.
- [–] Beschriftungen auf Achszahlen ((1 | 0), H(−1 | 2), «x [cm]») — die Beschriftungen tragen einen Hof und bleiben lesbar; Schachtel-Fenster trotzdem erweitert.
- [–] Merkbild Kontrollclip Vielfachheit «Terrasse dreifach» — Leitprogramm und Themenseite behandeln Vielfachheiten bis 3.
- [x] Übung `probe-teiler`: 13 % der Probezahlen sind keine Teiler von \(a_0\); Hinweis «Exponent der Klammer x»,
  Lösung «\((x)^3\)», «\((x-2)^1\)» in `vielfachheit`; `scheitel-extrem`-Hinweis nur für \(a \gt 0\) formuliert.
- [x] Rückmeldungen: Kontrollclip Extrema F3 «x_s» als Klartext mit Unterstrich; Kontrollclip Linearfaktoren F2
  R2 rechnet fast vor.
- [x] 5c/G7: Maximum aus 0.5er-Tabelle als exakt ausgegeben → «in der Tabelle am grössten». G7 «zu grobe
  Tabelle» kann nicht vorkommen; \([0; 5]\) als Schreibweise regeln. (A) an Zeilen, die nichts ablesen (G3c, G4, G7a).
- [x] Zeiten: Kopf jetzt «Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest». [–] Gesamttest 30 min (25 P, Teil B mit Rechner);
  [–] Vorwissensclips 1:03/0:49 wie auf der Themenseite (HOWTO §7). Kapitel 4 ohne Handdivision (Ansatz) — 40 min reichen.
- [x] Festhalten 1: \(a \lt 0\) spiegelt auch; Festhalten 4 «Beispiel: f(1)» nennt \(f\) nicht. Randfall
  (Rest ohne reelle Nullstellen) nie geübt. FEST-Eintrag `[1, 0, 6, 6]` (5c) hat \(a = 4\).
- [x] PDF-Layout: G5/G7 wenig Schreibplatz, Seiten 2–4 halb leer; G2 Tick «1» unter Kurve.

---

## Prüfung Exponential- und Logarithmusfunktionen (04.10.2026)

Skill `/lp-pruefung leitprogramme/exp-log-funktionen.html`, drei Agenten (Seite, Clips, PDFs),
Stand Commit `4022f46` (unverlinkt, noindex). `seite.*`/`clips.py` = `scripts/lp/exp-log-funktionen/`,
`GT`/`BP` = `downloads/leitprogramme/exp-log-funktionen/{gesamttest,bewertungspaket}.tex`.

**Behoben 04.10.2026** (Seite, 6 Clips neu vertont samt allen Fragetönen, GT G1/G3/G5/G8 neu, Raster dazu, Themenseite 3.4a Sättigung: «Abstand» statt «Rückstand … Zerfall»). Abnahme (Hörprobe, KI-Test) offen.

**Rechenfehler: keine** in Vortest, Aufgaben 1a–5d, Festhalten, 25 Kontrollfragen, Stützpunkten der
bewegten Kurven und GT G1–G8; alles ohne Rechner lösbar. Werkzeuge grün (`pruef-uebungen` 15 × 2000,
`pruef-leiste` 5, `pruef-fragen` 5). Nachgeprüft vom Hauptagenten: H1, H2, M1.

### HOCH
- [x] **H1 · Clip `wachstum-zerfall` «Prozent und Faktor», «Merke» und Kontrollclip «Merke»: «Faktor eins plus p»,
  Bild `a = 1 + p`** — widerspricht dem Festhalten \(1 + \frac{p}{100}\) (bei 5 % gäbe es 6). → «p Hundertstel», neu vertonen.
- [x] **H2 · Kontrollclip Sättigung F5 (Klick bei t = 8)**: \(f(8) = 98.5\) liegt 1.5 unter dem Ziel 100, Toleranz 4 —
  wer die Kurve tippt, gilt als richtig. → bei \(t = 2\) fragen, Kurve als Falle.

### MITTEL
- [x] M1 · Aufgabenleisten beim Wechsel schon gelöst (Sim 1: 1 → 2, Sim 3: 1 → 2, Sim 5: 4 → 5, Sim 2: 1 → 2). → Regler beim Wechsel zurücksetzen; Sim 1 zählt «über 1» schon beim Laden.
- [x] M2 · Sättigung: «erreicht S nie» (4d, Festhalten) ohne \(A \neq S\); «Rückstand \(S - f(t)\) ist Zerfall» stimmt beim Abkühlen nicht (negativ, steigt) → Abstand \(|S - f(t)| = |S - A|\,e^{-kt}\). Gleiche Formulierung auf **Themenseite 3.4a** (Sättigung).
- [x] M3 · `exp-wert`: Rückmeldung bei negativem Exponenten falsch («\(3^{-2}\) heisst 2-mal multiplizieren»).
- [x] M4 · Sonderwerte verdecken Fehler: `halbwertszeit` j = 2 (17 %), `exp-gleichung` a = t = 2, `wachstum-wert` a = t = 2, `basis-punkt` (2 | 4), `log-wert` \(\log_2 4\), `exp-wert` \(2^2\).
- [x] M5 · Sperrliste: `prozent-faktor`, `saettigung-lesen`, `saettigung-wert` ohne Schlüssel; fehlend \((\sqrt2)^x\), \(2^x + 1\), \(\log_3 1\), \(\log_5 1\), \(\log_2 4\), Clip-Fälle.
- [x] M6 · \(\ln\) in Kapitel 3 benutzt, erst in Kapitel 5 erklärt; Vortest prüft ln nicht.
- [x] M7 · «Zeichnen» (Kapitelziele 1 und 5, K1 «grafisch darstellen», K4 «visualisieren») nicht geübt bzw. nicht im GT; Kap. 2 ohne Aufgabe am Graphen, Kap. 5 ohne «Warum»-Aufgabe.
- [x] M8 · GT verlangt Ungeübtes: G2b gebrochener Exponent, G4b Zeit aus Menge (erst Kap. 5), G8 \(\ln e^3\); Basiswechsel *zur* Basis e nie geübt.
- [x] M9 · GT wiederholt: G5c = Aufgabe 3b, G5a = Festhalten/Clip \(8^x = 2^{3x}\), G1 = Clip-Kurvenpaar; Kapitelaufgaben 4b, 5c, 5d, 2d = Clip-/Kontrollbeispiele; Leistenziele = Clip-Beispiele (Sim 2 −20 %, Sim 3 \(2^x\)/\(\left(\frac12\right)^x\), Sim 4 Akku, Sim 5 \(\log_2 8\)).
- [x] M10 · Raster: G3 «höchstens 2» ist 1; G6 typischer Fehler «45 °C» falsch hergeleitet, 17.5/37.5 fehlen.
- [x] M11 · Basiswechsel zu beliebiger Basis: \(b = \log_a c\) fehlt, Buchstaben wechseln die Rolle; bei \(b \lt 0\) Spiegelung.
- [x] M12 · Verschobene Asymptote der Umkehrfunktion (5b, G7) nicht eingeführt.
- [x] M13 · `saettigung-wert`: «Welchen Wert hat er» mehrdeutig.

### NIEDRIG
- [x] \(\left(\tfrac12\right)^x = e^{-0.69x}\) mit «=» (Festhalten 3, Clip «Vorzeichen von b»); `basiswechsel`-Lösung \(2.236 = 5^{1/2}\).
- [x] Clips: Kurven für \(t \lt 0\); Antworten vor der rhetorischen Frage im Bild (Log «Umkehrfrage», «Gleichungen lösen»); Beschriftungen von Kurve gekreuzt; Punkt \((-2 \mid \frac14)\) fehlt; Marke 100 abgeschnitten (Kontrollclip Sättigung), Asymptote über 100 («Erwärmen»); Kontrollclip Log F4 «log drei von x plus eins» mehrdeutig gesprochen; Kontrollclip Exp F5 Text ≠ Ton; «halbiert sich gleichmässig».
- [x] Farben: Nachbau-Kurve Sim 3 grün bei Basis 2, Rückstandslinie orange; [–] Zielkurve grün (Konvention aller Leitprogramme).
- [x] Übungen: «Kehrwert-Wurzel», «1 Halbierungen», \(\tfrac13\), \(\tfrac17\) nur als Bruch eingebbar, «Bring den Läufer auf \(\log_2 8\)», Anzeige «\(-\,0 \cdot e\)» bei \(A = S\), Schalter Sim 5 «(gestrichelt)».
- [x] Aufgaben: Variablen/Einheiten in 2b, 2c, 2d, 4b; 1d \(a = 0\); 3c drei Teile für 2 P; 5d «Welcher Punkt»; Minigraf 3d \(2^x\)/\(3^x\) gleich gezeichnet; Wirkung von \(k\) nirgends gesagt.
- [x] PDF: [–] Bewertungspaket mit halbleeren Seiten (`\needspace`) — gewollt: der KI-Auftrag bleibt am Stück zum Kopieren, Abschnitte beginnen oben; [–] Kopfzeile trennt den langen Namen; [–] GT 30 min (25 P, wie die anderen Leitprogramme); [–] Teil B mischt K2–K4 (nach Kapiteln gegliedert).
- [–] Vorwissensclip `s3-2b-anim-spiegelung` 0:53 wie auf der Themenseite (HOWTO §7). Vortest verlinkt das noch unverlinkte Leitprogramm Potenz/Wurzel — erledigt sich mit dessen Freischaltung.

## Prüfung Trigonometrische Funktionen (05.10.2026)

Skill `/lp-pruefung leitprogramme/trigonometrische-funktionen.html`, drei Agenten (Seite, Clips, PDFs),
Stand Commit `d2c302d` (unverlinkt, noindex, nicht live). `seite.*`/`clips.py` = `scripts/lp/trigonometrische-funktionen/`,
`GT`/`BP` = `downloads/leitprogramme/trigonometrische-funktionen/{gesamttest,bewertungspaket}.tex`.

**Behoben 05.10.2026**: Seite (Festhalten 3–5, Aufgaben 1a, 2d, 3d, 3e, 4d, 5a, 5c, neue 5f mit \(\cos(bx) = c\), Kompetenzbox), Simulationen (Gerade durch O und P, Kurvenvergleich, Symmetrieachse je nach Vorzeichen, Schalter-Reset, «≈»), Übungen (Diagnosen, Sinus mit \(c \lt 0\)), 7 Clips neu vertont (+ Fragetöne von 3 Kontrollclips), neue Clipszene «Faktor im Argument», GT G1/G4/G5/G6 neu, Raster G6/G7. Abnahme (Hörprobe, KI-Test) offen.

**Rechenfehler: einer** — 5c «7.058» statt 7.059 (mit gerundetem 0.775 weitergerechnet). Sonst alle Werte
in Vortest, 1a–5e, Festhalten, 25 Kontrollfragen, GT G1–G8 und Folgefehler-Fällen nachgerechnet und richtig.
Werkzeuge grün (`pruef-uebungen` 10 × 2000, `pruef-leiste` 5, `pruef-fragen` 5). Nachgeprüft vom Hauptagenten:
H1, H2, H3, M1, M5 (k = −5: Abweichung 2·10⁻¹⁵), M8.

### HOCH
- [x] **H1 · «Strahl durch P» trifft die Tangente im 2./3. Quadranten nicht** (`seite.py:311` Festhalten 3, Clip `tangens`
  «Am Einheitskreis»; Sim 3 zeichnet die Strecke dort von P *weg*). Bei \(x = \tfrac{3\pi}{4}\) zeigt der Strahl nach links.
  → «Gerade durch O und P (im 2./3. Quadranten ihre Verlängerung über O hinaus)», Sim 3 von P über O zeichnen; Clip neu vertonen.
- [x] **H2 · GT G8(c) verlangt \(\sin(bx) = c\)** (Argument ersetzen, zurückrechnen) — nirgends geübt (Kap. 5 nur \(\sin x = c\)).
  → in Kap. 5 Beispiel, Festhalten-Zeile und Aufgabe mit \(\sin(bx) = c\) ergänzen, oder G8(c) ändern.
- [x] **H3 · 5c: 7.058 → 7.059.**

### MITTEL
- [x] M1 · Kompetenzdeckung: Kap. 5 (Gleichungen) steht nicht wörtlich in SP 3.5; gedeckt durch GF 5.5 («trig. Gleichungen … mithilfe der Arcusfunktion lösen») und SP 3.1; Kap. 4 durch SP 3.1 (Transformationen). → Kompetenzbox/-matrix ehrlich machen, GF 5.5 im Vorwissen/«Mehr dazu» verlinken.
- [x] M2 · GT prüft Kapitelziele nicht: Tangenskurve skizzieren (Kap. 3), Verschiebung \(u\) und schrittweise Skizze (Kap. 4), «Cosinus = verschobener Sinus» (Kap. 2). → G4 mit Skizze, G5 mit \(u\) und Skizze.
- [x] M3 · GT wiederholt: G5 = Kontrollclip «Parameter» F2+F3 (\(p = \tfrac{2\pi}{3}\), \(W = [-3;1]\)); G6 gleiches \(b = 0.5\)/Fenster wie 4c; G7(a) 0.35 ≈ 5a 0.3; G4(a) ≈ 3a; G1 ≈ 1d. Leistenziel Sim 4 A3 (\(a = 2, v = 1\)) = Clip-Schlussbeispiel; Sim 5 Startwert c = 0.3 zeigt die Lösung von 5a.
- [x] M4 · Raster: G6 «A nur bei richtigem Wert … zählt nicht» widerspricht dem KI-Auftrag (nur (E) ohne Folgepunkte) und ist unklar; G7 nur (E)-Zeilen — Symmetrieregel ohne Wegpunkt, Gradmodus-Fall «ausser … erkennbar» ohne Punktzahl.
- [x] M5 · Sim 4 A6 (und A4 mit k = ±4) lehnt gleichwertige Verschiebung ab: \(u = -\tfrac{5\pi}{6}\) trifft die Zielkurve exakt. → Kurven vergleichen statt k.
- [x] M6 · Sim 5 zeichnet beim Sinus immer die Achse \(x = \tfrac{\pi}{2}\); für \(c \lt 0\) liegen die Lösungen symmetrisch zu \(\tfrac{3\pi}{2}\). Sinus mit \(c \lt 0\) (Regel \(x_1 + 2\pi\)) wird mit Rechner nie geübt (`zweite-loesung` nur \(c \gt 0\)).
- [x] M7 · Ablesen ohne Beschriftung: 5d (\(\tfrac{7\pi}{6}\), \(\tfrac{11\pi}{6}\) auf \(\tfrac{\pi}{2}\)-Raster), GT G6 (3.5/−1.5 ohne Halbgitter), `aus-graph` bei \(b = 3\) (Periode nicht auf dem Raster, Hinweis «Hochpunkt zu Hochpunkt» führt ins Leere).
- [x] M8 · Clip `kontrolle-parameter` F1: \(3\sin x + 1\) reicht bis 4, Fenster bis 3.4 — Hochpunkt abgeschnitten, gerade bei der Amplitudenfrage.
- [x] M9 · Clip `tangens` «Am Einheitskreis»: «Tangente bei x gleich eins» (gezeichnet bei Daten-x ≈ −1.5); Bahn endet bei 1.25, \(\tan 1.25 = 3.01\) über dem Bildrand — «wächst über alle Grenzen» unsichtbar.
- [x] M10 · Übungen: `kenngroessen` leere Rückmeldung bei Mittellinie = a; `grad-bogen` Richtung Grad bei Zähler 1 kaputte Formel (\(\tfrac{\cdot 180^\circ}{6}\)); `stelle` Hinweis «eine Periode weiter» bei Nullstellen falsch (Abstand π); Rückmeldungen `tan-wert`/`kenngroessen` verraten die Lösung.
- [x] M11 · 1a «\(x = 1\) in Grad auf eine Dezimale» widerspricht «ohne Hilfsmittel». → exakt \(\tfrac{180^\circ}{\pi}\).

### NIEDRIG
- [x] Clip `kontrolle-periode-symmetrie` F4: Verschiebung (1.4–3.4 s) läuft vor «nach links» (4.9 s). Clip `kreis-kurve` «Der Cosinus» ohne Einheitskreis/P; «Bogenmass»: P läuft in 0.3 s rückwärts; «Achse» → «x-Achse». Clip `parameter` «Periode» 3 px Überlapp; «beginnt erst bei π/3» → «geht steigend durch null». Kontroll-Parameter F5 nennt Amplitude und Periode schon im Text; Merkbilder ohne \(a \gt 0\). Kontroll-Gleichungen: \([0;2\pi]\) vs. \([0;2\pi[\), Fall \(|c| = 1\) fehlt. Kontroll-Periode F5 ohne Falle bei \((0 \mid 1)\).
- [x] Seite: Live-Anzeigen ohne «≈» (Sim 1, 3, 4: «Periode 2.513» bei b = 2.5, Sim 5); Sim 1 Checkbox «Cosinus» bleibt nach «von vorn» an (A3 verlangt Sinus, Text sagt es nicht); Sim 2 «Hochpunkt» verschwindet bei u ≥ 7π/4; 2d auch \(\cos(x - \pi)\) nennen; 3d Lösungsbild ohne Polgeraden; 3e «\(\tan\tfrac{\pi}{2} = \tfrac10\)» mit «=»; 4d negativer Vorfaktor (−20 cos) unkommentiert, Festhalten setzt \(a \gt 0\); \(\sin^{-1}\) vs. arcsin (Themenseite) nicht erklärt; `grad-bogen` verlangt «exakt», nimmt Dezimal.
- [x] GT/BP: G3-Titel «Symmetrie und Periode» prüft nur Symmetrie; Zuordnung G2(c) → Kap. 3, G8(a/b) → Kap. 4; Kompetenzmatrix im Seitenkopf anpassen.

## Prüfung Betragsfunktionen (05.10.2026)

Skill `/lp-pruefung leitprogramme/betragsfunktionen.html`, drei Agenten (Seite, Clips, PDFs), Stand Commit
`e8ef159` (unverlinkt, noindex, nicht live). `seite.*`/`clips.py` = `scripts/lp/betragsfunktionen/`,
`GT`/`BP` = `downloads/leitprogramme/betragsfunktionen/{gesamttest,bewertungspaket}.tex`.

**Behoben 05.10.2026** (mit Trigonometrie: H1 Leiste, H2 Kreisfarbe — Fragetöne von 4 Kontrollclips neu). Betrag: 5 Clips mit neuem Ton, alle Fragetöne neu, GT G1/G2/G4–G7 überarbeitet, Raster neu, Vortest 0d (Parabel), neue Aufgabe 1f. Die beiden Ungenauigkeiten der **Themenseite 3.6** (Knicke an Nullstellen; «links» das Vorzeichen drehen) auf Auftrag angeglichen (05.10.2026). Leitprogramm freigeschaltet. Abnahme offen.

**Rechenfehler: keine** in Vortest, 1a–5e, Festhalten, 25 Kontrollfragen und GT G1–G7 (Raster G1 nennt
falsche Folgezahlen, siehe M8). Werkzeuge grün (`pruef-uebungen` 10 × 2000, `pruef-leiste` 5, `pruef-fragen` 5).
Nachgeprüft vom Hauptagenten: H1, H2, H3, M1.

### HOCH
- [x] **H1 · «Erkunde» nach Überspringen nie mehr lösbar** (alle 5 Simulationen; ebenso **Trigonometrie**, schon freigeschaltet):
  `bewegtMerken(r, bewegt, …)` bindet das erste Objekt, `aufraeumen` weist `bewegt = {}` neu zu. → Objekt leeren statt neu zuweisen; in beiden Leitprogrammen.
- [x] **H2 · Klickfragen nennen die falsche Kreisfarbe**: Ziel wird grün gezeichnet (`--f3`), Text/Ton sagen «blau» bzw. «orange»
  (alle 5 Kontrollclips; ebenso **Trigonometrie** «blaue/orange Kreis»). → «grüne Kreis», Fragetöne neu.
- [x] **H3 · Clip `verschieben` «Den Knick verschieben»: Ton «mit plus v nach oben», Bild fährt nach unten (v = −3).** → v = +3 im Bild.

### MITTEL
- [x] M1 · «An den Nullstellen von f entstehen Knicke» (Festhalten 3, Clip `umklappen` Knicke/Merke, Merkbild Kontrolle): Gegenbeispiel aus Sim 3, \(f = x^2\) (Nullstelle 0, kein Knick). → «wo f das Vorzeichen wechselt». **Themenseite 3.6** (Z. 421, Lückentext) gleich ungenau — melden, nicht still angleichen.
- [x] M2 · «Links der Grenze das Vorzeichen drehen» (Kontrollclip `abschnittsweise` Merke; **Themenseite** Z. 483/614): falsch bei negativer Steigung (\(|4 - 2x|\)). → «wo das Argument negativ ist».
- [x] M3 · Sim 3: Live-Formel «x.5» bei q = 0.5 (`replace(' + 0', '')`); Gerade m = 0, q < 0 meldet «nichts umzuklappen», obwohl alles hochklappt.
- [x] M4 · Leistenziele mit einem Schalterklick erfüllt: Sim 3 A5 (q = 1 ≥ 0), Sim 5 A5 (c = 3). Leistenziele = Clip-Beispiele: Sim 3 A2 (Knick 2), A4 (±2), Sim 5 A4/A5 (\(|x^2-4|\), c = 4 bzw. 3), A2 (\(|x - 1| = 2\) = Kontrollfrage), Sim 2 A4 = GT G2.
- [x] M5 · Sperrliste: `bg`/`bu`-Einträge mit falschem Vorzeichen (`bg|1|-1|3` statt `bg|1|1|3` usw.); `umklapp-parabel` würfelt nur noch 3 Aufgaben; fehlend `bg|1|2|3`, `bu|1|2|3|le`, `wa|-1|2`, `fa|2|-1`.
- [x] M6 · GT G4(a) verlangt Nullstellen/Scheitel von \(x^2 - 2x - 3\) — nirgends geübt, Vortest prüft es nicht. Ebenso Nullstellen von \(a|x-u|+v\) in 2b/G2 vor Kap. 5 ohne gezeigten Weg.
- [x] M7 · GT prüft Kapitelziele nur teilweise: K1 «skizzieren» und «abschnittsweise definieren» (G1), K4 «abschnittsweise lesen / Wanne zerlegen» (G5b nur Werte). GT wiederholt: G2 = Sim 2 A4, G7 \(|x^2-1|\) = 3b(a)/Kontrollfrage, G1(b) = Kontrollfrage; G6 (a) und (b) mit denselben Schnittstellen.
- [x] M8 · Raster: G1 Folgezahlen falsch («11 bzw. 17» → 9 bzw. 11, beide: 17); G4 Folgefehler aus falschen Nullstellen ungeregelt; G3 «begründe» und G6 «Skizze» ohne Rasterpunkt; G7 algebraische Begründung ohne Skizze ungeregelt; G1(c) (E) ohne möglichen Weg.
- [x] M9 · Übungen: Randfälle fehlen (`betrag-gleichung` nie c = 0 / c < 0, `betrag-ungleichung` nie < / >); gleichwertige Eingaben abgelehnt (`umklapp-parabel` −w, Reihenfolge); `v-aus-graph` Ablesestellen nicht beschriftet.

### NIEDRIG
- [x] Clips: Rückmeldung «Ein Betrag macht immer einen Knick» (Kontrolle verschieben F4) widerspricht Kap. 3; Merke «Vorzeichen aus dem Betrag umgekehrt» unscharf (gilt nicht für v); «Wie viele?» ohne c = 0; Falle (−3 | −3) ausserhalb des Fensters; u, v im Clip blau, in der Sim grau; «links der Wanne» → «links des Bodens»; Szene «Ungleichung» zeigt das Lösungsstück vor dem Satz.
- [x] Seite: 1e Ungleichung vor Kap. 5 → «wo liegt das V unter y = 3»; Festhalten 4 «aussen steigen die Äste mit ±2» → −2 links, +2 rechts; m doppelt (Bezugspunkt / Steigung); Abstand orange (orange = Lösungen); «dünn gezeichnete Zielkurve» → blass; Sim 4 bei a = b Lücke x = a; Minigraf 3c Gitter 0.75; Kap. 0 Kopf «SP 2.1» statt 2.2c; `betrag-wert` «+ 0»; `abschnittsweise` ohne Diagnose «nur eine Zahl umgedreht».
- [x] PDF: G3-Kurve durch Achsenbeschriftungen; G4(a) wenig Schreibraum, G6/G7 ohne KS.
