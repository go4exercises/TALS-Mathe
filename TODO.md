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

- [x] **Aussprache** «x s», «y s», «x plus eins in der Klammer», «null Komma fünf», «D», «Symmetrieachse»:
  Hörprobe 10.10.2026 (`~/hoerproben/2026-10-10`). Umgesetzt `6d9571b`: «die Diskriminante» statt «D»,
  «y s, gleich» mit Komma; übrige wie bisher.
- [ ] **Hörprobe** der Kontrollclips: je eine Frage absichtlich falsch beantworten, damit auch die
  Rückmeldungen zu hören sind. Fundstellen (Clip, Sekunde) melden → Sprechertext bzw. Tabelle, neu vertonen.
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
- [x] **Teilvertonung in `build-clip-ton.py`** (Wunsch 08.10.2026; erledigt: `--szenen`, dazu `--fragen` in `build-clip-fragen-ton.py`, Übertrag in `TODO-schwesterprojekt.md` und `OFFEN`): Das Skript vertont immer den ganzen Clip in eine
  Spur. Für Korrekturen an einzelnen Szenen entstanden zwei Behelfe — `scripts/lp/einheitskreis/teilton.py` und ein
  gleichartiges Skript im Scratchpad (Themen-Clips g5): geänderte Szenen neu sprechen, die übrigen aus der alten Spur
  schneiden. Als Schalter `--szenen` ins geteilte Werkzeug übernehmen (dann auch `TODO-schwesterprojekt.md`).
- [ ] Clip-Bauer-Wünsche aus dem LP Modellieren (08.10.2026, ohne Auftrag offen): Rechnerfolge (`stapel`) mit je
  einem Ankerwort pro Schirm statt Startzeit plus festem Schritt; `build-clip-ton.py` erkennt geänderte Sprechertexte
  selbst und warnt vor langer Stille am Szenenende (Behelf: `scripts/lp/modellieren/clips.py` meldet «NEU VERTONEN …»).
  Geteiltes Werkzeug — bei Umsetzung auch `TODO-schwesterprojekt.md` und `OFFEN`.
- [x] Clip-Bauer-Wünsche aus den LPs 5.3–5.5 (08.10.2026; alle umgesetzt, HOWTO-clips «Dritte Runde», Übertrag in `TODO-schwesterprojekt.md` und `OFFEN`): `aus` an einem ganzen `graf`-Element; Klickziel als Strecke
  und nächstgelegene Falle gewinnt; `kreis`-Begleiter beschriftet P; Text-Figuren folgen einem bewegten Punkt;
  Achsenzahlen neben statt auf dem Einheitskreis; Bogen entlang des Kreises statt linear; Farbe je Zeitabschnitt in
  `bewegung`; eigene Strichart für `asymptoten`; Kurven direkt in Grad; Beschriftungen weichen einander aus.

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

## Prüfung Planimetrie (06.10.2026)

Skill `/lp-pruefung leitprogramme/planimetrie.html`, drei Agenten (Seite, Clips, PDFs), Stand Commit
`2641d79` (unverlinkt, noindex, nicht live). `seite.*`/`clips.py` = `scripts/lp/planimetrie/`,
`GT`/`BP` = `downloads/leitprogramme/planimetrie/{gesamttest,bewertungspaket}.tex`. Arbeitsbereich = `arbeitsbereich('simN')` in `seite.js`.

**Rechenfehler: keine** in Vortest, 1a–5e, Arbeitsbereichen (Soll- und Fehlwerte), Clip-Beispielen, 25 Kontrollfragen
und GT G1–G7 samt Folgefehlern. Werkzeuge grün (`pruef-uebungen` 10 × 2000, `pruef-leiste` 5, `pruef-geo` 5, `pruef-fragen` 5).
Nachgeprüft vom Hauptagenten: H1, H2, H5, M1, M4, M5, N (Karo, «= ≈», leere Rückmeldung).

**Behoben 06.10.2026**: Seite (Festhalten 1/2/4/5, 4g Segment 60°, 5b-Figur massstäblich, Vortest 0b/0c, Kompetenzbox und
Matrix ehrlich), Arbeitsbereiche (AB2 A1 t = 2, γ verborgen und Soll 86.82 ± 0.03, Live-Zeilen ohne Antworten, Strahlensatz-Figur
mit S, AB3 A5 neue Werte, AB4 Fenster), Übungen (neuer Typ «Welche Linie ist die Höhe?» mit Figur in wechselnder Lage,
Parallelogramm mit schräger Seite, ohne r = 2 und Stab = Schatten, Sperrliste), Clips (H2, H4, M6, M8, NIEDRIG; neu vertont:
Kontrolle Fläche F1, Kreis Segment/Kreisring, Ähnlichkeit Negativer Faktor/Strahlensätze, Fragetöne Fläche/Dreiecke/Vierecke),
Gesamttest neu (G1–G7 ohne Wiederholungen, jedes Kapitelziel), Raster widerspruchsfrei. `pruef-geo` prüft deckungsgleiche
Kandidaten; HOWTO §15 um drei Fehlerklassen ergänzt; `figuren` kann `deckkraft`. Abnahme offen.

### HOCH
- [x] **H1 · Arbeitsbereich 2, Aufgabe 1 mit der Maus unlösbar**: Startwert t = 4 → C(4 | 3) über der Mitte von AB, Kandidaten Höhe und Seitenhalbierende deckungsgleich, `s` liegt oben; Tipp gibt «Das ist die Seitenhalbierende … nicht senkrecht» (falsch, das Dreieck ist gleichschenklig). → `setup` t = 2 (und sperren). Neue Fehlerklasse: **deckungsgleiche Kandidaten** — `pruef-geo` soll Kandidaten auf Abstand prüfen.
- [x] **H2 · «Im stumpfwinkligen Dreieck liegt die Höhe ausserhalb»** (Kontrollclip Fläche F1 Option und Sprecher; Seite Festhalten 2 «Häufiger Fehler», Festhalten 1): Die Höhe von der stumpfen Ecke liegt innen (Kontrollclip Dreiecke F3, Lot von B auf AC bei t = 0.53). → «zwei Höhen liegen ausserhalb» / «kann ausserhalb liegen»; **Neuvertonung** Kontrollclip Fläche, Szene «Frage 1».
- [x] **H3 · Gesamttest wiederholt Modelle** (HOWTO §9): G1(a) = 1b(b)/Übung winkelsumme; G2(b) = Arbeitsbereich 2 A7; G3 = 3b + Arbeitsbereich 3 A6; G4 = 4c/Clip/Übung sektor (φ-Liste enthält 135°); G5 = Clip Kreis (Segment 60°, gleichseitig) und Themenseite 5.2c (r = 10, φ = 60°, 9.06); G6 = 5e/Festhalten/Clip/Kontrollclip/Übung (alles Schatten); G7 = 5c. Auch Selbsttests wiederholen Clip/Festhalten (3d = 3-4-5-Trapez, 5e Schatten, 4c Sektor). → Umkehr- und Transferaufgaben (Winkel aus Bogenlänge, Strahlensatz an Figur, Modellfläche gesucht, Basiswinkel gesucht).
- [x] **H4 · Segment bei 60° nie geübt, im GT verlangt (G5)**: Kapitel 4 übt nur φ = 90° (rechtwinkliges Dreieck); Clip zeigt «A_Δ ≈ 15.59» ohne Weg (§15 «Schritte sichtbar»). → im Clip Höhe √(6² − 3²) zeigen (**Neuvertonung** Clip Kreis, Szene Segment) und eine 60°-Aufgabe einbauen — oder G5 mit 90°.
- [x] **H5 · Arbeitsbereich 1, Aufgabe 7: Antwort steht in der Live-Zeile** («γ ≈ 86.8°»), und 86.82 (exakt) gibt fälschlich «Fast — runde auf zwei Dezimalen». → γ bei Frage-Aufgaben ausblenden, Soll 86.82 mit Toleranz für 86.8.

### MITTEL
- [x] M1 · Segment-Regel ohne Bedingung (Festhalten 4): gilt nur für φ < 180° (darüber Sektor + Dreieck; Themenseite 5.2c sagt es); Regler φ bis 360°, Übung sektor bis 300°.
- [x] M2 · GT deckt Kapitelziele nicht: Vierecksfamilie/Parallelogramm/Raute/Drachen, Sehne-Sekante-Tangente-Passante, Kreisumfang/-fläche, Kreisring, zentrische Streckung ausführen, Strahlensätze (nur Schatten), A = ½ g h begründen, Umfang Dreieck.
- [x] M3 · Raster: G7 «cm² statt m²» widerspricht der allgemeinen Gleichwertigkeitsregel (BP Z. 44 vs. 140); G2 «½ vergessen» uneinheitlich (Ansatz verlangt ½, Fehlerzeile lässt Ansatzpunkt); G6 Ansatz- und Verhältniszeile überlappen; G1(a) Begründung unklar; (A)-Punkte erklärt, aber keine (A)-Zeile; Einheitenabzug keiner Zeile zugeordnet.
- [x] M4 · Bild ≠ Text: Arbeitsbereich 5 A6 (Text SA = 4, SA' = 6, AB = 3 und «S»; Bild Z, ZA ≈ 1.12, AB = 2); Aufgabe 5b (AB gezeichnet ≈ 0.55·SA, gegeben 1.4·SA); GT G2 (C bei (−2.2 | 4.2) → AC = 4.74 statt 7; richtig (±5.6 | 4.2)).
- [x] M5 · Arbeitsbereich 3: Live-Zeile zeigt «A = 18 cm²» in A1–A4 bei denselben Werten, nach denen A5 fragt; Arbeitsbereich 5 A5 zeigt «Flächenfaktor k² = 6.25» während der Frage.
- [x] M6 · Clips: Kreis «Linien am Kreis» Sehne nicht auf der Sekante (y = 2.25 statt 5.5); Vierecke «Familie» Raute ist ein Quadrat (Diagonalen 2.4/2.4); «Parallelogramm» das abgeschnittene Dreieck links nicht markiert; Ähnlichkeit ohne Strahlensatz-Figur (S, A, A′, B, B′) und ohne k < 0, Formel «ZP′ = k·ZP» statt |k| (**Neuvertonung**, wenn eine Szene dazukommt).
- [x] M7 · Sonderwerte verdecken Fehler: kreis/sektor r = 2 (2πr = πr², b = A_S); strahlensatz Stab = Schatten.
- [x] M8 · Eingeführt? Kreisring nur in Festhalten/4f (kein Clip, keine Übung); Strahlensätze nur Formel im Clip, Arbeitsbereich 5 A6 fragt sie vor dem Festhalten; «2. Strahlensatz» (5b) nie nummeriert; Kapitel 2 nutzt Parallelogramm g·h vor Kapitel 3 (Vortest prüft nur Rechteck).
- [x] M9 · Kompetenzdeckung nicht ehrlich ausgewiesen: K2 «berechnen» — Seiten-/Winkelhalbierende, Mittelsenkrechte, Sehne, Sekante, Tangente nur erkannt; Abstand nur als Höhe; Winkelmass nur Grad (5.1 nennt Radiant; Themenseite verschiebt auf 5.4). → in Box und Matrix vermerken.
- [x] M10 · Leitfaden ④ nicht umgesetzt: Übungen dreieck-flaeche/hoehe ohne Figur, keine Zuordnung Grundseite–Höhe, keine wechselnden Lagen/Dreiecksarten; viereck/Parallelogramm ohne Ablenker «schräge Seite».

### NIEDRIG
- [x] Seite: «Schnittpunkt H» → «Höhenschnittpunkt H» (Festhalten 1); `m_c` kollidiert mit Mittellinie m, Themenseite schreibt A_SK; «Raute (Rhombus)»; gleichseitig ohne Seitendefinition; c = 8, d = 0 heisst «Parallelogramm» statt Rechteck; Arbeitsbereich 2 gedreht «C(2 | 3)» passt nicht zum Raster, h_b-Aufgaben zeigen «g = 8 cm» und nach der Antwort «h = 3 cm»; «Wo liegt der Fusspunkt jetzt?» ohne gezeichnete Höhe (AB1 A4, AB2 A3); AB1 A3 Trefferstreifen s/w überlappen; Live-Zeile «Summe 180°» zirkulär; Arbeitsbereich 4 bei r = 5 unten abgeschnitten; Vortest 0b «Faktor 100» verwirrend, 0c = Clip-Beispiel; Warnkasten 5 «SA : AA′» missverständlich; Kompetenzmatrix ohne 1e.
- [x] Technik: Karo der Aufgabenfiguren unsichtbar (`svg.geo-mini .gitter` ohne Stil; 2d/1c nicht ablesbar); `.geo .bild` trifft auch die Texte A′B′C′ (gestrichelter Umriss); Arbeitsbereich 4 «= ≈ 0.167»; Übung pythagoras: leere rote Rückmeldung (Fehlerliste `[hypot, '']`, z. B. 2/3 → 3.6); Sperrliste: `tr|14|8|4`, `py|3|5`, `py|4|3`, Diagonalen-Reihenfolge, `st` Schlüssel ohne Fläche, `gs|52/64` wirkungslos.
- [x] Clips: Kontrolle Vierecke F3 Rückmeldung Text ≠ Ton; Kontrolle Dreiecke F5 «h_c» roh; Ähnlichkeit «12 m» auf der Linie wie «2 m» (Masslinie); Rückmeldung «nicht senkrecht zum Bildrand» bei a gedreht unpassend; Winkelfarben wechseln (Dreiecke Szene 0/1); Kreis «A_Seg» erscheint vor dem Ton.
- [x] PDF: GT 30 min (HOWTO ~20); G1/G2 wenig Schreibraum für Skizzen; G3 ohne rechten Winkel; BP Seiten 1–2 halbleer; «für das ganze Gesamttest»; «das wäre die Mittelsenkrechte, wenn senkrecht» verworren.

## Prüfung Lineare und quadratische Gleichungen (06.10.2026)

Skill `/lp-pruefung leitprogramme/lineare-quadratische-gleichungen.html`, drei Agenten (Seite, Clips, PDFs), Stand
Commit `803af5b` (unverlinkt, noindex, nicht live). `seite.*`/`clips.py` = `scripts/lp/lineare-quadratische-gleichungen/`,
`GT`/`BP` = `downloads/leitprogramme/lineare-quadratische-gleichungen/{gesamttest,bewertungspaket}.tex`.
Umformer = `umformerSim('simN')` in `seite.js`.

**Rechenfehler: keine** in Vortest, 1a–5e, Festhalten, 25 Umformer-Aufgaben (jeder Knoten äquivalent), Simulation 5,
10 Clips + Vorwissensclip, 25 Kontrollfragen, GT G1–G8 samt Folgefehlern. Werkzeuge grün (`pruef-uebungen` 10 × 2000,
`pruef-leiste` 5, `pruef-umformer`, `pruef-fragen` 5). Bewegte Parabeln/Geraden über die Zeit geprüft.
Nachgeprüft vom Hauptagenten: H1, H2, H4 (Sperrschlüssel), M1.

**Behoben 06.10.2026**: Gesamttest neu (G1 Bruch + Minusklammer, G2 Lösungsfall umgekehrt, G3 Nullprodukt nur bei 0, G4 Ergänzung → Lösungsanzahl, G5 irrationale Lösungen, G6 Verfahren begründen + fremde Lösung prüfen, G7 k(k − 1)x = k, G8 (k − 1)x² + 2x + 1), Raster mit Restpunkten; Seite: 5b mit zwei kritischen Werten, 3g irrational, 2c neu, Festhalten 1/3/4/5, Kompetenzbox GF 3.1; Umformer: gültige Umwege als grauer Hinweis (`?`), Zweiklammersatz mit den Lösungen (Themenseite); Übungen: Sperrliste über Normalform (`T.quad`, 0 Treffer in 6 × 3000 Würfen), Diagnosen, Faktorisieren bei Binomen; Clips: Zweiklammersatz, «nicht durch x teilen, ohne x = 0 zu prüfen», Fragen Nullprodukt, x-Achse, Umformer statt Animation, parameter zu Ende geführt (neu vertont, Zeiten mit `ZEITVERSATZ` auf die neue Tonspur gelegt); Bibliotheksclip g2-1-aequivalenzumformungen Merkbild neu (1:07). `pruef-umformer` kennt `?`-Knöpfe; HOWTO §15 um drei Punkte ergänzt. Abnahme offen.

### HOCH
- [x] **H1 · GT G8 verlangt eine quadratische Ungleichung** (\(x^2 + kx + 9 = 0\): \(D = k^2 - 36\), \(|k| \gt 6\)) — in Kapitel 5 ist D(k) überall linear, Ungleichungen sind bewusst weggelassen; Raster gibt 0 von 3 P, wenn k = −6 fehlt. → z. B. \(kx^2 - 4x + 2 = 0\) (D = 16 − 8k; k = 0: x = 0.5; k = 2: x = 1) — prüft zugleich «Faktor vor x² null».
- [x] **H2 · GT G7 mit zwei kritischen Werten nie geübt** (\((k^2 - 1)x = k + 1\): k = 1 leer, k = −1 alle) — alle geübten a(k) haben einen kritischen Wert. → Kapitelaufgabe/Leistenaufgabe/Übungsvariante mit a(k) = k² − c, oder G7 vereinfachen.
- [x] **H3 · GT G1–G6 wiederholen Modelle** (G1 = 1b; G2 = 1d/Clip/Umformer/Übung loesungsfall; G3 = 2a+2c/Umformer/Übung; G4a = Umformer 3 A2/Übung wurzel; G4b = 3b/Umformer 3 A3; G5 = 3c; G6 = 4a/4b). → Kombinationen und Transfer innerhalb des Geübten (Minusklammer + Bruch, Ergänzung mit ungeradem b, D = 0 oder nicht quadratisches D, begründete Verfahrenswahl).
- [x] **H4 · Sperrlisten lassen feste Aufgaben und eine GT-Aufgabe durch**: `np|4|1|-1`/`np|2|1|-1` falsches Vorzeichen (2b, Umformer 2 A2 würfelbar), `np|1|2|-3` passt zu nichts; `loesungsfall` ohne Sperre (1d, Umformer 1 A3, Kontrollclip); `ausklammern` ohne `ak|1|-4` (2c); `wurzel` ohne p = 0 (x² = 9/16/25); `verfahren` Schlüssel ohne a → 18.8 % der Würfe feste Aufgaben, **G5 \(2x^2 - 5x + 2\) würfelbar**; `mitternacht`/`zweiklammer` treffen 3b, 3f, 4a(c), 4d, 4e, 5c, Umformer 3/4, Clips, GT G4b. → Sperre über Normalform (a|b|c) für alle quadratischen Typen.

### MITTEL
- [x] M1 · «Mit 0 multiplizieren oder durch einen Term mit x dividieren … dabei geht die Lösungsmenge verloren» (Festhalten 1, `seite.py:235`): mal 0 vergrössert sie auf ℝ; Teilen durch x² + 1 ist äquivalent. → «ändert die Lösungsmenge: mal 0 macht jede Zahl zur Lösung, durch x teilen kann Lösungen verlieren».
- [x] M2 · Zweiklammeransatz mit zwei Lesarten: Festhalten 4, 4e, Übung verfahren (Lösungen, Summe −p) gegen Clip verfahren, Kontrollclip F3/F5, Umformer `zweiklammer()`, Übung zweiklammer (Klammerzahlen, Summe p). → eine Lesart (Themenseite: Lösungen x₁ + x₂ = −p) und überall gleich; Begriff der Themenseite «Zweiklammersatz».
- [x] M3 · Übung verfahren: Faktorisieren bei x² − r² und x² + bx abgelehnt mit falscher Begründung («braucht 1 vor x² und alle drei Glieder») — Binome zählen laut Festhalten dazu, Raster G6a akzeptiert sie.
- [x] M4 · «Nie durch x teilen» (Clip nullprodukt Merke, Kontrollclip Nullprodukt Merke) widerspricht Seite und Umformer (Fallunterscheidung gültig). → «nicht durch x teilen, ohne x = 0 zu prüfen» (**Neuvertonung** beider Merke-Szenen).
- [x] M5 · Umformer: gültige Umformungen rot als Fehler, ohne Weiterweg (sim1 A1 :3, A2 :5, A5 ·5; sim2 A1 «nur 2 ausklammern», A2/A6 ausmultiplizieren; sim3 A2 ausmultiplizieren, A4 +16; sim4 A2 Ausklammern). Leitfaden §2: gültige Wege akzeptieren. → als Hinweis (grau) oder Umweg-Knoten; sim2 A5 «:x» eigene Meldung (rechts steht schon 0).
- [x] M6 · Kapitelziele im GT nicht geprüft: «Faktor vor x² null» (K5), «begründet wählen und prüfen» (K4, G6 nur «nenne», keine Probe bewertet). Raster: typische Fehler kosten zu viel (G8 nur k = 6 → 0/3, G7 bündelt Form und beide Werte); «0,5»-Komma doppeldeutig; ±0.67, «k² > 36», D = −41 ungeregelt; (A) nie benutzt.
- [x] M7 · Übungsdiagnosen: nullprodukt bei p = 0 verweist auf den falschen Faktor (~9 %); linear-loesen bei d = 0 Vorzeichen-/Divisionsdiagnose verwechselt (~2 %); wurzel q = 0 mit Eingabe {} «Wurzel ziehen mit ±» unpassend.
- [x] M8 · Clips: Kontrollclip Nullprodukt F4 Text ≠ Ton; F3 Rückmeldung verrät x = 0; F1 «Ausklammern geht immer» falsch (**Neuvertonung**); Kontrollclip Ergänzen F5 Falle «−b» bei −3 statt bei 1; Clip parameter «Die Fälle» Punkt x = 3 bleibt bei k = 2 (ℝ); Bild vor Ton (verfahren «Faktorisieren», ergaenzen Merke, parameter «Die Fälle»).
- [x] M9 · Parabeln benutzt (2e, 3f, 4e, 5c, Festhalten 3, Sim 5), aber nicht eingeführt; GF 3.1 «Gleichungen mithilfe von Funktionen visualisieren» nicht ausgewiesen. Sim 5 Familie B: rechte Gerade und Lösung für k ≥ 3.5 ausserhalb des Fensters.
- [x] M10 · Bibliotheksclip `g2-1-aequivalenzumformungen` Merkbild: «durch ihn teilen — gehört eine Probe dazu» — Probe findet keine verlorenen Lösungen (wirkt über das LP hinaus; **Neuvertonung**).

### NIEDRIG
- [x] Seite: (x − p)² = r ohne r ≥ 0; «berührt die Achse» → x-Achse (auch Clip ergaenzen, **Neuvertonung**); «Kein Glied mit x (ax² + c)» → «kein lineares Glied (b = 0)»; Ergänzung (b/2)² ohne «Faktor 1 vor x²»; «dann ist die Gleichung linear» → «sofern der Koeffizient von x nicht auch null ist»; 2b-Kommentar «Zahlen in Klammern = Lösungen mit umgekehrtem Vorzeichen» nur bei Faktor 1; p doppelt belegt; sim4 A2 Zeile doppelt im Verlauf; Sim 5 Live-Zeile «1x», «0x», «+ 0», rechte Seite orange; Kapitel 0 verlinkt 1.4 nicht; Umformer 4 A6 Probe nur für 0.5; 2c = Kontrollfrage und Festhalten (Antwort steht darüber); Mengen-Eingabe «{3 4}» → 34, «x=3» Meldung.
- [x] Clips: «Jetzt du … Animation» in Kap. 1–4 (dort Umformer; **Neuvertonung** 4 Clips); «√−8 gibt es nicht» → in ℝ; ergaenzen Merke «aus jeder Gleichung» → quadratischen; Kontrollclip Umformen F1 «verboten»; Mitternachtsformel ohne a ≠ 0 im Bild; parameter «Zuerst a prüfen» bricht ab, «Leitkoeffizient» nicht eingeführt; rechte Seite schwarz/orange uneinheitlich; Gerade verdeckt Achsenbeschriftung −2; Herleitung der Formel aus der Ergänzung nur behauptet (4c verlangt sie).
- [x] PDF: BP Seiten 1–2 halbleer; GT Seite 3 ein Drittel leer, G6 wenig Schreibraum; 30 min statt ~20 (bewusst festhalten); G3 doppelte Gleichwertigkeitsangabe.

## Nachprüfung Lineare und quadratische Gleichungen (06.10.2026)

Drei Agenten auf Stand `918b74e` nach der Bereinigung. Frühere Befunde: H1, H2, M1, M2, M4, M8, M9, M10 und alle Clip-Befunde
behoben; H3, H4, M3, M7 teilweise. Rechenfehler keine; Werkzeuge grün; Bild und Ton nach der Neuvertonung synchron (≤ 0.5 s,
Ausnahmen unten). Nachgeprüft vom Hauptagenten: N-H1, N-M1, N-M3.

### HOCH
- [x] **N-H1 · GT G4(b) steht wortgleich im Festhalten 5 und im Clip parameter** (\(x^2 - 6x + c\), Grenze 9, \(x = 3\)); das Raster lässt den D-Weg sogar zu. → z. B. \(x^2 - 10x + c\) (\((x - 5)^2 = 25 - c\); c = 16 → {2; 8}); Normalform in `FESTE_Q`.

### MITTEL
- [x] N-M1 · **Neue 2c widerlegt sich selbst**: «(x − 3)(x + 1) = 5 ⇒ x = 8 oder x = 4» — 4 ist eine Lösung (1 · 5 = 5); Lösung braucht zudem Kapitel 4. → z. B. \((x - 2)(x + 3) = 6\) (liefert 8 und 3; richtig {−4; 3}), Lösen in Kapitel 2 über Ausklammern oder nur Fehler + Probe.
- [x] N-M2 · Pflichtaufgabe des Leitfadens «x² = 4x ⇒ x = 4» fehlt jetzt; Kapitelziel 2 «Division verliert Lösungen» wird im GT nicht mehr geprüft (G3 ohne Ausklammern). → Aufgabe 2f wieder aufnehmen; G3 als Ausklammern mit Divisionsfehler (z. B. \(3x^2 = 7x\)).
- [x] N-M3 · **Sperrliste sperrt alle \(ax^2 = 0\)** (`[4, 0, 0]` → `1|0|0`): Übung ausklammern würfelt b = 0 nie mehr (Leitfaden verlangt es). Lücken: \(x^2 - 2x - 8\) (neue 2c), \(x^2 + 2x + 1\) (5d, Kontrollclip, Sim 5, G8), \(x^2 - 5x - 6\), \(x^2 - 4x + 4\), \(x^2 - x\) (Vorwissensclip, 13.9 % in ausklammern), `lf|4|2|4|8`, `lf|2|3|2|5`. → ausklammern mit eigenem Schlüssel a|b; Liste ergänzen; 20 000 Würfe zählen.
- [x] N-M4 · GT wiederholt weiter: G8 = Sim 5 Familie C verschoben (Sonderlösungen −0.5, −1; Raster-Fehlerfall = D von C) → \((k-1)x^2 - 4x + 2\) (D = 24 − 8k; k = 1: x = 0.5; k = 3: x = 1); G5 = 3g → «x(x − 2) = 1 exakt»; G6(d) = 4d → \(x^2 - 4x - 12\) mit angeblich «2 und 6».
- [x] N-M5 · Festhalten 5 «Mehrere kritische Werte» benutzt genau 5b → anderes Beispiel, z. B. \((k^2 - 4)\,x = k + 2\).
- [x] N-M6 · Übung verfahren: Faktorisieren bei a > 1 und b = 0 abgelehnt («Zweiklammersatz braucht 1»), obwohl Binom (11 % der Würfe); linear-loesen d = 0 Diagnose weiter verwechselt.
- [x] N-M7 · Raster: G8 «Fall k = 1 übersehen → 2 von 3» widersprüchlich; G7 (E) ohne Bedingung k ≠ 0; G2 Restpunkt für einzelne Beispiele unklar; G3(b) braucht Kapitel 3/4 (Zuordnung); G2 braucht Parameter (Zuordnung «1 und 5»).
- [x] N-M8 · Bibliotheksclip g2-1-aequivalenzumformungen Merkbild: Bild läuft dem Ton ~4 s voraus (kein `ein`), 𝔻-Zeile nie gesprochen und Bezug gekippt.

### NIEDRIG
- [x] Seite: Umformer 4 A4 «Wurzel ziehen …» als `?`; Kapitelziel 3 sagt noch \((x - p)^2\); 4c-Beispiel aus a = 2; \(\sqrt{12} = 2\sqrt3\) nicht gezeigt; «So arbeitest du» nur Umformer; Mengen-Eingabe «- 3», «x1 = 3»; Matrix ohne GF 3.1.
- [x] Clips: rechte Seite Tinte in verfahren «Erst ordnen» und ergaenzen «Wurzelziehen» (Legende «Tinte = zweite Seite» veraltet); umformen «Wenn x verschwindet»/«Alles ist Lösung» Formeln 0.8–1.4 s vor dem Ton; parameter «Die Fälle» und Kontrolle Verfahren F5 linke Hälfte leer; Merkbild ergaenzen ohne a ≠ 0; verfahren «Faktorisieren» p, q nicht eingeführt; parameter k = 2 Geraden deckungsgleich ohne Strichelung; Clipzeit 1:07 / 1:08.
- [x] PDF: BP S. 2 30 %, S. 5 75 % leer; G6 Anweisung als `\item[]`, wenig Platz in G1/G2; G8 verrät die Falle («Denk auch an …»); G4(b) «x = 3» nicht verlangt markieren; G6 Antworten «quadratische Ergänzung» ungeregelt.

**Behoben (06.10.2026):** Gesamttest neu: G3 Nullprodukt mit Faktor 2 + Division durch \(x\) bei \(3x^2 = 7x\);
G4 \(x^2 - 10x + c\) (c = 16 → {2; 8}); G5 \(x(x - 2) = 1\); G6(d) \(x^2 - 4x - 12\) mit «2 und 6»; G8 \((k - 1)x^2 - 4x + 2\)
(k = 1: 0.5; k = 3: 1) ohne verratenden Hinweis; Raster G2/G6/G7/G8 eindeutig, Zuordnung G2 → 1 und 5, `\A` weg,
G6 mit eigener Anweisung und Schreiblinien. Seite: 2c \((x - 2)(x - 3) = 6\) → {0; 5} über Ausklammern, 2f «\(x^2 = 4x\)»
wieder da, Festhalten 5 mit \((k^2 - 4)x = k + 2\), Herleitung der Mitternachtsformel im Festhalten 3, \(\sqrt{12} = 2\sqrt3\),
4c an \(x^2 + x - 1\), Kapitelziel 3 \((x - u)^2\), «So arbeitest du» nennt Kapitel 5, Matrix mit GF 3.1.
Übungen: Sperrliste ohne reine \(ax^2\)-Formen über qSchl, Lücken ergänzt (20 000 Würfe: 0 Treffer, b = 0 in 12 %);
Faktorisieren bei a > 1 anerkannt; eigene Meldungen für Wurzelziehen/Ausklammern bei Formel-Fällen und für d = 0;
Eingabe «- 3» und «x1 = 3». Umformer 4 A4 grau. Clips (ohne Neuvertonung): Bibliotheksclip Merkbild mit `ein`,
𝔻-Notiz unter «mal Term»; rechte Seite orange, Legende nachgeführt; umformen-Formeln auf den Ton gelegt;
Gleichung bzw. Notiz in parameter «Die Fälle» und Kontrolle Verfahren F5 ab Szenenbeginn; Merkbild mit
\(a \neq 0\); p, q in verfahren «Faktorisieren»; k = 2 dick/gestrichelt.
Bewusst belassen: Clipzeit 1:07 (HOWTO §7 rundet ab, die Bibliothek rundet); Bewertungspaket S. 5 nur
Selbsteinschätzung (Abschnittsfolge nach §9, Kästen nicht teilbar); optionale Neuvertonungen («Lösungen» in
Kontrolle Verfahren F3, «m ≠ 0» im Ton) nicht gemacht.

## Prüfung Trigonometrische Berechnungen (08.10.2026)

Skill `/lp-pruefung leitprogramme/trigonometrische-berechnungen.html`, drei Agenten (Seite, Clips, PDFs), Stand Commit
`2f968ca` (unverlinkt, noindex, nicht live). `seite.*`/`clips.py` = `scripts/lp/trigonometrische-berechnungen/`,
`GT`/`BP` = `downloads/leitprogramme/trigonometrische-berechnungen/{gesamttest,bewertungspaket}.tex`.

**Rechenfehler: keine** in Vortest, 1a–5e, Festhalten, Arbeitsbereichen, 10 Clips, 25 Kontrollfragen, GT G1–G7 samt
Folgefehlern. Werkzeuge grün (`pruef-uebungen` 11 × 2000, `pruef-leiste` 5, `pruef-geo` 5, `pruef-fragen` 5 × 9/9).
Nachgeprüft vom Hauptagenten: H1 (Bild `fest-sim3.png`), GT-Zahlen G1–G7.

**Behoben 08.10.2026** (7560fb2): alle HOCH/MITTEL, NIEDRIG fast alle. Gesamttest neu verteilt (Teil A 10 P, Teil B 15 P;
G1(c) gestrichen, Steigung in %, SSW kein/ein Dreieck). Keine Szene neu vertont, Fragetöne Kontrolle Seiten/Höhen neu.
Nachgetragen 08.10.2026: Sinussatz-Clip Satz zu h = c·sin α, Kontrolle Sinussatz F4 «freien Schenkel» (Teilvertonung).
Offen nur Hörprobe «a wird länger» (Cosinussatz «Stumpf»), «drei Komma vier vier», «a ist kürzer». Abnahme offen.
Hörprobe Runden 5/6 (10.10.2026): «Die Seite a ist kürzer», «Korrektur-Glied», «Arkus-Sinus» umgesetzt; «a wird länger», «drei Komma vier vier» wie bisher.

### HOCH
- [x] **H1 · Gesperrte Regler zeigen falsche Werte, teils die gesuchte Grösse** (`seite.js` `werte()`; sim1 A7, sim2 A7, sim3 A7, sim5 A5): Figur zeichnet `fest`, `.sl-val` zeigt den Startwert (sim3 A7 «15 m | 52°» bei h = 14, d = 20, gesucht α). → `.sl-val` aus `w` schreiben, gesuchte Grösse «?».
- [x] **H2 · Steigungs-Übung: Sinus statt Tangens oft als richtig gewertet** (`seite.js:627–638`): arcsin(0.05) = 2.87° vs. arctan 2.86°; rund 23 % der Würfe zählen den Fehler als richtig, 49 % unerkannt. → nur Steigungen ab ~14 % / Winkel ab 8° würfeln oder Diagnose vor dem Nah-Filter.
- [x] **H3 · Kontrolle Seiten F1: richtiger Klick zählt als falsch** (`clips.py:309`, `tol=0.9` um (0|2.5) auf BC von (0|0) bis (0|5)): nur 36 % der Seite angenommen. → `tol` 1.8 (Abstand zu AB 2.12, zu CA 2.5) und Fallen auf den anderen Seiten.
- [x] **H4 · SSW-Regel ohne «α spitz»** (Festhalten 4, `seite.py:293`): bei α = 120°, c = 6, a = 5.5 (h = 5.20 < a < c) kein Dreieck. Themenseite Z. 827 gleich (→ Themenseiten unten).

### MITTEL
- [x] M1 · Arbeitsbereich 4: Fehlwerte A5 17.49 (passt zu keiner Rechnung; a/c vertauscht ergibt 28.55) und A7 3.82 (c·sin α/sin β = 3.81 ausserhalb Toleranz; Meldung meint a·sin α/sin β = 4.45) greifen nie; RAD-Werte 0.76/0.51 nur bei gemischtem Modus.
- [x] M2 · Ein Zeichen h für zwei Höhen im selben Festhalten 4 (`seite.py:290` Höhe von C, `:293` Höhe von B). → h_c bzw. «Höhe von B».
- [x] M3 · «Welcher Satz?» nennt den Fall (SWS …) gleich mit (`seite.js:789`), nur 8 feste Fälle. → Fall erst in der Rückmeldung.
- [x] M4 · Raster BP: G3 Skizzenzeile verlangt Höhenwinkel, die die Aufgabe nicht fordert (BP:87/61); G3 zwei typische Fehler mit gleichen Zahlen (14.25/8.57), verschiedene Punkte (BP:92–93); viele E-Zeilen in Folge kosten einen Fehler doppelt (G3 Abstand, G4 b, G5 β → Folgepunkte); G7 Vergleich c² vs a² + b² nie geübt (in 5b ergänzen).
- [x] M5 · GT G5 Titel «Zwei mögliche Dreiecke» verrät (a). → «Seite, Seite, Winkel».
- [x] M6 · Clips: hoehen «Benennen» GK-Beschriftung bei 1.9 s, «Gegenkathete» bei 4.6 s; Kontrolle Höhen F3 «Vom Turm aus» → «Von der Turmspitze aus»; Kontrolle Seiten F4 Rückmeldung «Das passt zur Ankathete» zu 6.62 irreführend; cosinussatz «Pythagoras»/«Stumpf» ohne Verweis auf 5.4 und Seite a nicht markiert (**Neuvertonung** je nach Wortlaut).
- [x] M7 · GT deckt Kapitelziele nicht ganz: Steigung % ↔ Grad, SSW «kein/ein Dreieck». (Selbsteinschätzung ehrlich.)

### NIEDRIG
- [x] Seite: Tiefenwinkel-Satz (`seite.py:249`) präzisieren («Tiefenwinkel von oben = Höhenwinkel von unten»); Kapitel 2 ohne Aufgabe mit Figur; «(x ≠ 90°)» → «spitzer Winkel x»; «a wird länger» → «… als beim rechten Winkel»; Übung `flaeche` Tipp (p·q)/2; Übung `hoehe` «Baum» bis 79 m; `winkel-rw` krumme Längen, Funktionsmeldung nie erreichbar; `sinussatz` «γ vergessen» bei γ ≈ 90° unsichtbar; G4b Kapitelzuordnung.
- [x] Clips: Kontrolle Höhen F1 «(Augenhöhe vernachlässigt)»; sinussatz ein Satz zu h = c·sin α; Baumkrone über der Spitze; «35°» bei C₂, «c = 6» Tinte statt Orange; Steigungsbogen ohne «x»; «β = 90° − …» vs. «90° − x»; Kontrolle Seiten F5 «doppelt so gross»; Kontrolle Sinussatz F4 «freien Schenkel»; Hörprobe «a wird länger».
- [x] PDFs: G1 «vertauscht» (a) nur 0, wenn dort vertauscht; G2 «Rest zählt» klären; G6 Vorzeichenfehler einheitlich; G7 Urteil 0 nur bei Zustimmung; G6 «125°» im Bogen; BP Umbruch im KI-Auftrag Punkt 5; Schreibplatz G3/G7, Seite 3 halb leer; Selbsteinschätzung «Teil» vs. «Kapitel».

## Prüfung Einheitskreis (08.10.2026)

Skill `/lp-pruefung leitprogramme/einheitskreis.html`, Stand Commit `2f968ca`. `seite.*`/`clips.py` = `scripts/lp/einheitskreis/`,
`GT`/`BP` = `downloads/leitprogramme/einheitskreis/{gesamttest,bewertungspaket}.tex`.

**Rechenfehler: keine** (Vortest, 1a–5d, Festhalten, Leistenziele, 10 Clips, 25 Kontrollfragen, GT G1–G8). Werkzeuge grün
(`pruef-uebungen` 10 × 2000, `pruef-formelsatz`, `pruef-leiste` 5, `pruef-fragen` 5 × 9/9, `zahlen.py`).
Nachgeprüft vom Hauptagenten: H1, H2.

**Behoben 08.10.2026** (e1c6489): alle HOCH/MITTEL, NIEDRIG grösstenteils. GT G2–G5 neu. Neu vertont: sinus-cosinus «Weiter drehen»,
symmetrien «Anwenden», Kontrolle Tangens F5, Kontrolle Periode F3 (+ Fragetöne). Bewusst gelassen: sim4 A2/A3 (Erkennen),
Clipzeit 13.3 min (> 12). Komplement-Formel seit 08.10.2026 gesprochen. Abnahme offen.

### HOCH
- [x] **H1 · BP G7 wertet die richtige Antwort als Fehler** (BP:141): «180° − 63.4°» = 116.6° ist der richtige zweite Punkt; gemeint 180° − (−63.4°) = 243.4°.
- [x] **H2 · Festhalten 5: «sin φ = w ⇒ φ = arcsin w»** (`seite.py:433–435`): falsch (sin 150° = 0.5, arcsin 0.5 = 30°). → «arcsin w ist der Winkel aus [−90°; 90°] mit sin φ = w». Themenseite g5-4 Z. 947 gleich.
- [x] **H3 · Dreieck OQP widersprüchlich**: Clip sinus-cosinus «Weiter drehen» sagt «bei 140° kein solches Dreieck», zeichnet es aber (`P_teile` mit `'dreieck'`); Kontrollclip 3 F5 und Festhalten 3 rechnen mit OQP in jedem Quadranten; «Winkel φ bei O» (`seite.py:347`) gilt nur im I. Quadranten. → «kein Dreieck mehr mit φ bei O» + Referenzwinkel (**Neuvertonung** sinus-cosinus «Weiter drehen» falls Wortlaut).
- [x] **H4 · Übung «Aus einem Wert die anderen» verwirft richtig gerundete Dezimalzahlen** (`seite.js:693`, Toleranz 0.0015; −1.33 statt −4/3 → irreführende Meldung). → «auf drei Dezimalen» und «zu grob gerundet» erkennen.
- [x] **H5 · Übung «Exakte Werte»: Sperrliste lässt 15 Aufgaben, 60 % Achsenwerte, nie 30°/45°/60°** (`seite.js:608`). → Wurfraum erweitern (negative, > 360°, Bogenmass), Achsen seltener.

### MITTEL
- [x] M1 · Clips: Kontrolle Sinus/Cosinus F2 Falle (0.707 | −0.707) mit Rückmeldung «im Uhrzeigersinn» (gehört zu (−0.707 | −0.707)); symmetrien «Anwenden» «ohne Taschenrechner» −0.906 ohne Angabe cos 25° ≈ 0.906; Gerade OP bei 90° unsichtbar (tangens-pythagoras «Kein Wert», Kontrolle 3 F3); besondere-winkel «Referenzwinkel» dreht statt spiegelt; Kontrolle Periode F2/F3 prüfen dasselbe (+360°). (**Neuvertonung** symmetrien «Anwenden», ggf. Kontrolle Periode F3.)
- [x] M2 · Hauptwert aus β (Übung «Welchen Winkel liefert der Rechner?», GT G7b/G8b) nirgends gezeigt; Festhalten 5 braucht ein Beispiel — Abgrenzung zu LP 5.5 (zweite Lösung) wahren.
- [x] M3 · Wiederholungen (HOWTO §9): GT G3 = Aufgabe 1d (P(0.28 | −0.96)); G2(b) cos 315° = 2b; G4 = 4a mit 35°; G5 = 4e; Aufgabe 5d = Festhalten-Fehler (sin⁻¹ 0.5 → 0.524); Kontrolle Symmetrien F5 tan 35°/215° und Kontrolle Besondere F1 cos 240° wie GT.
- [x] M4 · Raster: G1 Toleranz P (±14°) vs. S (±0.25) widersprüchlich → S als Folgepunkt zur eigenen Geraden; G2 «exakt angeben» ohne Weg, Raster verlangt Weg; G8(a) Begründungszeile teilrichtig lesbar; G6 Himmelsrichtung ohne Vorlauf, Antwortform offen; Teil A Hilfsmittel (Geodreieck?); RLP-Vermerk «ohne Hilfsmittel» nur bei K3 — Auslegung als solche kennzeichnen (GT und Seite).
- [x] M5 · «Gegenwinkel» für 180° − α (`seite.py:397`) kollidiert mit LP 5.3 (Gegenwinkel = gegenüber einer Seite). → «Supplement».
- [x] M6 · Kapitel-3-Ziel «warum bei 90° kein Tangens» und Rückführung über 360° ohne HM im GT nicht geprüft.

### NIEDRIG
- [x] Seite: sim4 A2/A3 Durchklicken genügt; sim1 A4 prüft nur φ = 200; «zieh jeweils an α»; Festhalten 4 «−α = 360° − α» als Gleichung, Punktspiegelung unter «Spiegelachsen», «an der Mitte O»; tan-Spalte ohne Bedingung; Referenzwinkel-Formeln nur 0°–360° (Aufgabe 2a verlangt −60°, 420°); «Exakte Werte» auf den Achsen meldet Referenzwinkel; Sperrliste `tw|210`, `hw|cos|305`, `sw|25|cos|335`; Clipzeit 13.1 min (> 12).
- [x] Clips: Ton/Bild runden verschieden (0.84/0.839, 1.19/1.192, 0.58/0.577); «nur bei 90° und 270°»; «sein Winkel ist positiv»; Beschriftungen «23.6°» über «y = 0.4», «y = 1.2 …» über y-Achse, «20°» bei «−1», «180°−α» am Punkt, B auf A 0.8 s; Referenzbogen orange (Kommentar sagt Tinte); Komplement-Formel ungesprochen; Hörprobe «Arkussinus»/«Arkustangens».
- [x] PDFs: G3 «≈ −3.43» in Teil A, Vorzeichenbegründung; G4 «Symmetrie genannt» definieren; G5 reines Zitat; Platz für Skizzen G2/G5, halbleere Seiten GT und BP.

## Prüfung Trigonometrische Gleichungen (08.10.2026)

Skill `/lp-pruefung leitprogramme/trigonometrische-gleichungen.html`, Stand Commit `2f968ca`. `seite.*`/`clips.py` =
`scripts/lp/trigonometrische-gleichungen/`, `GT`/`BP` = `downloads/leitprogramme/trigonometrische-gleichungen/{gesamttest,bewertungspaket}.tex`.

**Rechenfehler: keine** (Vortest, 1a–4e, Festhalten, Leistenziele, 8 Clips, 20 Kontrollfragen, GT G1–G7 samt Folgefehlern,
Sperrliste deckt GT). Werkzeuge grün (`pruef-uebungen` 8 × 2000, `pruef-formelsatz`, `pruef-leiste` 4, `pruef-fragen` 4 × 9/9).
Nachgeprüft vom Hauptagenten: H1 (Toleranz 0.3 bei Schritt 0.5), H2 (Selektor `.sim-breit svg`).

**Behoben 08.10.2026** (ebd3a34): alle HOCH/MITTEL, NIEDRIG fast alle. GT G2(b), G4–G6 neu; Vortest 12 P mit Tangens.
Neu vertont: einheitskreis «Besondere Werte», Kontrolle Tangens F5 (+ zwei Fragetöne). Labels 143.1°/216.9° (Sim 4) und «31.0°»
(Kontrolle Tangens F5) am 08.10.2026 nachgetragen. Abnahme offen.

### HOCH
- [x] **H1 · Sim 2 (5 Ziele) und Sim 3 (3 Ziele) «Dreh P auf …» mit Maus/Finger kaum treffbar** (`seite.js:314, 363` Toleranz 0.3, Regler 0–360 Schritt 0.5, 144 px): bei 360 px alle 8 unerreichbar. → Schritt 1°, Toleranz ≥ 0.6 bzw. 1° gegen den ungerundeten Zielwinkel.
- [x] **H2 · Sim 4: alle Formeln der Aufgabenleiste auf eigenen Zeilen** (`seite.py:69` `.sim-breit svg{display:block…}` trifft MathJax). → `.sim-breit .kurven-rahmen > svg`.
- [x] **H3 · Raster G4/G5: nur eine Lösung gibt 3 von 4 P** (BP:97–105): «Nur 339.5°» fehlt als typischer Fehler, Folgepunkt-Zeile «Lösungsmenge, Probe» passt dazu; G6 behandelt denselben Fehler anders. Ausserdem G4 Menge + Probe in einer Zeile (Regel «teilrichtig = 0» vs. «oder»), G4 «Vorzeichen übersehen» Doppelabzug, G3(b) «beide Familien» vs. typischer Fehler.

### MITTEL
- [x] M1 · Sim 1 A6: Klick auf «cos» löst die Aufgabe (`seite.js:272`, Startwert c = 0.5 = Ziel). → anderes Ziel/Startwert.
- [x] M2 · Übung «Wie viele Lösungen?» würfelt nie n = 1 (Sperrliste sperrt alle ±1, `seite.js:503/529`). → Sperre nur je Funktion/Intervall.
- [x] M3 · Übungen Kapitel 1/3 verlangen [−180°; 180°[ vor Kapitel 4 (60 % bzw. 78 % der Würfe); positive Sinus-Sonderwerte auf [0°; 360°[ nie. → Kapitel 1/3 nur [0°; 360°[.
- [x] M4 · Kapitel-4-Kurvenbild bei 360 px 47 % verdeckt, Leistenaufgaben 2 und 5 im verdeckten Teil, kein Hinweis.
- [x] M5 · Clips: Wahlfragen-Auflösungen zeigen falsche Angebote nicht rot (§15) — Kontrolle Einheitskreis F4, Arkus F1/F2/F4, Tangens F1/F5, Lösungsmenge F2/F5; loesungsmenge «Weiter drehen» Punkte 30°/150° vor der Kurve (`ein` 1.9 / 3.35); tangens «Immer lösbar» Gerade schwenkt über die Waagrechte statt zur Senkrechten.
- [x] M6 · Lösungsbild 3d: «S» von «333.4°» ganz verdeckt; Kurvenbild 4b ohne ±1 (Beschriftung links aus dem Bild, `seite.js:129`), y = −0.9 unbeschriftet.
- [x] M7 · Wiederholungen: GT G4 ≈ 2c/Festhalten 2, G5 ≈ 4b, G6 ≈ 4c, G2(b) cos φ = 1 = 1e/4d.
- [x] M8 · Vortest prüft kein Tangens-Vorwissen (S(1 | tan φ), √3/3) — Link auf `einheitskreis.html#…` Kapitel 3.

### NIEDRIG
- [x] Seite: Lösung 4e Begründung (Abstände 120°/240°); Feldnamen «φ₁/φ₂» kollidieren mit φ₁ = Hauptwert; «≈» fehlt (Sim 4 Live-Zeile, Lösungen `anzahl` dreistellig mit Komma, `quadranten`); Sinuskurve über Achsenzahlen Sim 4; S bei c = ±2.4 halb aus dem Bild; Sim 3 A6 «ungefähr 243°» → «auf ganze Grad».
- [x] Clips: Kontrolle Einheitskreis F5 Gerade y = 1.4 über y-Achse (ybereich ±1.7) und Option «Fehlermeldung» (Rechnerangabe unbelegt); P unbeschriftet; Kontrolle Lösungsmenge F4 Farbe 120°/480°; `:` statt `\colon`; «− 210°» als Rechenzeichen; Ergebnis vor dem Ton (einheitskreis «Zwei Punkte» 150°, «Besondere Werte» Tabelle); Gradbeschriftungen von Linien gekreuzt; «Wurzel aus zwei halbe»; «minus einunddreissig Grad» ohne «ungefähr»; Kontrolle Lösungsmenge F3 Text ≠ Ton; «4. Quadrant» → «IV.»; Tangens-Kurvenbild Pole und y = 1 gleich gezeichnet.
- [x] PDFs: Dezimalkomma + Komma als Trenner mehrdeutig; Bogenmass in G3 regeln; G5 «720°» unrealistischer Fehler; Platz für Skizzen G2/G4; BP Seite 1 halb leer; G7(a) (A).

## Themenseiten 5.3–5.5: beim Bau der Leitprogramme gemeldet (08.10.2026)

**Behoben 08.10.2026** (e5c0524, Clips 6fb9b49): Seiten korrigiert, 20 Animationsbilder g5-4 neu, anim-tangens/kopplung/welche-winkelfunktion
teilweise neu vertont. Bewusst gelassen: sin x vs. sin(α), Merkregel «All Students Take Calculus», Anker `id="arcus"`.
- [x] g5-3: Fälle klein/gross (wsw/WSW); GK/AK/H neben Geg/An/Hyp, SOH-CAH-TOA, «GAGA», «HY»; «Arcus» vs. «Arkus»; cos 110° vor 5.4; Merkkasten Fläche «Pythagoras-Spezialfall»; SSW-Regel ohne «α spitz» (Z. 827).
- [x] g5-4: «sin φ = w ⇒ φ = arcsin w» (Z. 947, fachlich falsch); Koordinaten mit Komma in Animation 1/2; «Strahl OP» trifft die Tangente im II./III. Quadranten nicht, Tangens als «Länge RS»; Farben sin/cos uneinheitlich; Bogenmass-Verweis auf 5.1; «Funktionen in Kapitel 5.5».
- [x] g5-5: **Tangens in [0°; 360°[ «φ₁ und φ₁ + 180°» falsch für c < 0** (tan φ = −1: 135°, 315°); RLP-Box «Arcusfunktion» statt «Arkusfunktion»; drei Schreibweisen für alle Lösungen; Mengen mit Komma, «𝕃 ≈ {…}»; arctan-Bereich (−90°; 90°); Mini-Check Riesenrad sin x = 0.5 vs. Mittelpunktshöhe; «0° ≤ φ ≤ 720°» vs. [0°; 720°[.

## Prüfung Textaufgaben modellieren (08.10.2026)

Skill `/lp-pruefung leitprogramme/modellieren.html`, Stand Commit `69f6279`, vier Prüfer (Seite, Clips Zahlen/Mischen, Clips
Verteilen/Zins, PDFs). `seite.*`/`clips.py` = `scripts/lp/modellieren/`, `GT`/`BP` = `downloads/leitprogramme/modellieren/{gesamttest,bewertungspaket}.tex`.

**Rechenfehler: keine** in Vortest, 1a–4d, Festhalten, Leistenzielen, 12 Clips, 80 Kontrollfragen, GT G1–G7 samt Folgefehlern
(`zahlen.py` 130 Prüfungen). Werkzeuge grün (`pruef-uebungen` 9 × 2000, `pruef-formelsatz`, `pruef-leiste` 4, `pruef-fragen` 8 × 7/7,
`pruef-clip`). Simulationen bilden die Grundgleichungen richtig ab; Rechnerangaben (poly-solv/sys-solv-Schirme, (−), ↔) belegt.
Nachgeprüft vom Hauptagenten: H1 (GT:35–38 «von Hand» in Teil A), H2 (`seite.js:14` rundet auf 4 Stellen, `:691`), H3 (BP:121–122),
M1 (`seite.js:724`), N `\;` (`seite.js:619`).

**Behoben 08.10.2026:** alle HOCH/MITTEL, NIEDRIG bis auf vier. GT neu nach Hilfsmittel (A ohne Rechner 11 P: G1–G3 inkl. Set;
B mit Rechner 14 P: G4 sys-solv, G5 Eindampfen m·p, G6 Zinseszins, G7 Zeitanteil); 2c/3c/4c neu; Übung «Eindampfen»; Zeiten neu
(20 + 60 + 65 + 60 + 65 + 35 = 305 min, über HOWTO §3 — Teilung offen). Bewusst gelassen: «art» ohne Sachbezug, Zucker in Litern
(Mischen 1 A1), Balkenmassstab schematisch, «Jahreszins». Neu vertont: Szenen in allen vier Einführungsclips und sechs
Kontrollclips, 30 Fragetöne (Liste im Bericht des Bearbeiters; Hörprobe offen).

### HOCH
- [x] **H1 · GT G2 verlangt eine quadratische Gleichung (System Summe 17, Quadratsumme 145) von Hand in Teil A ohne Rechner** — das LP löst jede quadratische Gleichung mit poly-solv (Kapitel 0 Tabelle, Festhalten 1 `:812`, alle Clips); Lösen von Hand nirgends geübt, Raster gibt «nur mit Rechner» 0 P. Dazu D1: Kapitelziele «Produkt der Unbekannten» (m·p, x·y, K·p), Sets und «ganz, nicht negativ» im GT ungeprüft. → G2 durch quadratisches System mit Produkt der Unbekannten **mit Rechner** ersetzen (Teil C/D).
- [x] **H2 · Übung «Zinssatz mal Zeit»: Lösung falsch gerundet und mit «=»** (`seite.js:691`, `z()` rundet auf 4 Stellen): 1.5 % · 3/12 → «0.0038» statt 0.00375 (auch 0.01875, 0.00675 …; 5 von 62 Würfen) — wer die gezeigte Lösung tippt, bekommt «falsch». → bis 6 Stellen ausgeben.
- [x] **H3 · BP G6: gleicher Fehler, verschiedene Punkte; Fehlerzahl b = 1000 entsteht nicht** (BP:121–122): «1000 CHF nicht mitverzinst» = «Mittelglied vergessen (b = 12 000)» algebraisch dasselbe, einmal Grundform 1 P, einmal 0; Mittelglied 12 000p vergessen gibt b = −1000. Dazu G3 (BP:86 vs. :90): «Preise vertauscht» Antwortzeile Folgefehler 1 vs. 0. → je eine eindeutige Regel.
- [x] **H4 · `kontrolle-mischen-2` A2: Kochsalzlösung mit 30 %** — mehr als löslich (≈ 26.4 % bei 20 °C); Übung «Mengen- und Stoffbilanz» würfelt Salz bis 95 %, Stickstoff über 46 %, Sirup über 70 %. → Vorschlag Clip: «3 kg Salz, sinkt um 5 Prozentpunkte» (dieselbe Grundform m² + 10m − 600 = 0, m = 20, p = 0.15); Übung: Gehaltsbereich je Sachzusammenhang.

### MITTEL
- [x] M1 · Übung `zinseszins`: «Zinssatz unter −100 %» bei *jeder* negativen Eingabe (`seite.js:724`, `e.p < 0`), auch bei −p. → nur bei `gl(e.p, A.neg)`; «Einen Zinssatz …».
- [x] M2 · Übung «Mengen- und Stoffbilanz»: bei p = M trifft die richtige Mengenbilanz die Falle [1, 1, p] (0.9 % der Würfe, `seite.js:602`). → p = M ausschliessen.
- [x] M3 · GT G4 «Verdunsten» nirgends geübt (nur Verdünnen). → Wurf/Aufgabe «Wasser entziehen» in Kapitel 2.
- [x] M4 · Wiederholungen: GT G7 ≈ `kontrolle-zins-1` (Lea, ein Teil kürzer verzinst); G5 ≈ 2b (gleicher Fehler «Anteil rechts», Kupfer wie `kontrolle-mischen-2`); Kapitelaufgaben 2c ≈ `kontrolle-mischen-1` (zweimal abzapfen), 3c ≈ `kontrolle-verteilen-2` (Bus), 4c ≈ Leiste 4; Kopf GT:6 behauptet «keine Wiederholung». → neue Kombinationen.
- [x] M5 · Raster für KI: gleichwertige Wege G6 (q = 1 + p: 6000q² − 1000q − 5110.6 = 0; p in %: 0.6p² + 110p − 110.6 = 0), G2 Probieren, G5 «korrigiert» ohne eingetippte Zahlen, G4 Folgepunkt Probe.
- [x] M6 · Unbelegte Rechneranzeige bei Dezimal-Koeffizienten: 4c «poly-solv: x₁ = 3/200» bei c = −241.8 (`:1186`), «poly-solv zeigt Brüche» (`:1142`), Übung `zinseszins`, Einführung `zins` (poly(5000, 10000, −304.5)), `kontrolle-zins-*`. → ganzzahlige Grundform (4c × 5: 40 000p² + 80 000p − 1209 = 0) oder ohne Anzeigeform.
- [x] M7 · Löserwahl uneinheitlich (`seite.js:530/573`, Übung «art» `:1909–1912`): «keiner, von Hand» bei linear (num-solv existiert, Clip g2-1), beim LGS «von Hand» richtig, bei quadratisch nicht (auch nicht bei a(1+p)² = …, wo 4c «Wurzelziehen geht» sagt). → «von Hand (oder num-solv)», «von Hand» überall zulassen.
- [x] M8 · Rückmeldungen verraten die Lösung: `kontrolle-mischen-1` A2 Grundform «1600 − 900», «2 · 40 · x»; `kontrolle-mischen-2` A2 Grundform (p = 0.01·m + 0.1 nicht im Bild); `kontrolle-verteilen-1` A1 Deklaration «Bei x = 4 …» (Ergebnis von ④); `kontrolle-zins-2` A2 Lösen «1/50 … 0.02, 2 %» = Option A.
- [x] M9 · Bild-Ton: `zahlenraetsel` «Zahl = 10·z + e» 3 s vor «zehn mal z» (`@zehn#2`); nie gesprochene rote Notizen (`zahlenraetsel` drei, `zins` «Quadratisch»); stumme Tasteneingaben `kontrolle-zahlen-2` A2 und `kontrolle-mischen-2` A2 (bis 8 s Stille); `kontrolle-mischen-2` A1 Grundform Zeilen in anderer Reihenfolge als gesprochen; `verteilen` «Streifen» ohne Streifen im Bild; `kontrolle-zins-2` A2 Grundform gesprochene Zeile 0.004K = 4000p + 16 fehlt im Bild (ebenso `kontrolle-zins-1` A2 5000p² + 12000p + 7000).
- [x] M10 · Bild zeigt Lösung vor der Rechnung: `mischen` Becher bei 20/10, `verteilen` Breiten 5/7, `zins` Balken 14 : 16 — neutral beginnen. `zins` «Lösen» ohne Einsetzschritt 0.0075·(30 000 − y) + 0.02·y = 425; einfacher Zins in den Clips nie benannt (Falle K·(1 + 2p) ohne Gegenüberstellung).
- [x] M11 · «Prozente addieren sich nie» (Clip `mischen` «Die Falle»/Merke, Seite `:932`) zu absolut — das LP rechnet selbst p − 0.1. → «Die Anteile der Sorten addieren sich nicht zum Anteil der Mischung — addiert werden die Stoffmengen.» Steht auch auf der Themenseite (Z. 474).
- [x] M12 · Kapitelzeiten 45 min knapp (zwei Kontrollclips mit 20 Fragen, Sim, Übungen, 4 Aufgaben) — Schätzung 60–70 min; GT 40 min statt ≈ 20–30. Zeiten neu schätzen.

### NIEDRIG
- [x] Seite: Simulation Verteilen läuft ab n > 32 aus der viewBox (Regler 20 + 20); Simulation Zins bei 360 px Schrift ≈ 7 px, «Obligation»/«Sparkonto» unbeschriftet; Sperrliste «art» leer (kann 145, 113, 168 würfeln), fehlende Themenseiten-Werte `wb|20|15|9|252`, `fk|0.6|12`; Ziffernrätsel mit Einerziffer 0 («03»); Leiste Kapitel 1 A3/A5 nehmen 1a vorweg; «Ein Quadrat oder ein Produkt macht es quadratisch» ohne «nach dem Ausmultiplizieren»; «Grundform a·x = c» ohne a ≠ 0 (GF 2.2 nennt sie «Zwischenform»); «art» in Kapitel 1 würfelt schon Kapitel 2–4; Kommentare in `zahlen.py` (Startzustand, 1b); `\;` statt `\;` in `seite.js:619` (Strichpunkte im Satz); GT-Schreibflächen knapp (`\lpplatz` 10–12), Seiten 2–4 halb leer.
- [x] Clips: «kg» kursiv ohne Abstand (`clips_basis.py` `auto_tex()` hält Wörter < 3 Buchstaben für Mathematik → `\,\text{kg}`); «m p» ohne Malpunkt; Zucker in Litern (`kontrolle-mischen-1` A1); Antwortsätze ohne Einheit (`mischen` «Lösen», «w = 3»), ohne Zuordnung (`kontrolle-zins-2` A1 «9000 CHF zu 2 % …»); Probe 5 + 7 = 12 fehlt (`verteilen`); Fragetext ≠ Ton (`kontrolle-verteilen-2` A2 «Was prüft …», `kontrolle-zins-1` A1 «mit Probe»); Deklaration «m vor dem Verdünnen»; Sets-Szene ohne Herkunft der 21/17, z grün; Balkenmassstab Zins/Kapital; «Prozentpunkte» nicht eingeführt; «2 % Jahreszins»; x1/x2 heisst hier r bzw. p; Zeitversätze `zins` «Lösen», `kontrolle-zins-1` A2, `verteilen` «Lösen».

### Themenseite g2-modellieren: beim Bau und Prüfen gemeldet
**Behoben 08.10.2026:** Merksatz (Z. 308) nennt Sets und fehlende Gesamtmenge; Z. 474 «die Prozentsätze der Sorten aber nicht
zum Prozentsatz der Mischung»; `build-seo.py` tg «2.1 Grundlagen und 2.3 Lineare Gleichungssysteme». Bewusst gelassen: «Ungleichung»
in K1 ist RLP-Wortlaut (2.1), die Seite deckt davon nur Gleichungen und Systeme ab.
- [x] Merksatz «jede Misch-, Verteil-, Zinsaufgabe = Mengenbilanz plus Wertbilanz» passt nicht auf Sets und Zins ohne Kapitalgleichung; «Prozentsätze addieren sich nie» (Z. 474) zu absolut; Breadcrumb/JSON-LD nur «2.1», RLP-Box 2.1 und 2.3; K1 nennt Ungleichungen, die Seite hat keine.

## Prüfung Leitprogramme GF 5.2a–d (08.10.2026)

Skill `/lp-pruefung` auf `dreiecke`, `vierecke`, `kreis-kreisteile`, `aehnlichkeit`, Stand Commit `05c765e`, je drei Prüfer
(Seite, Clips, PDFs). Quellen je `scripts/lp/<name>/`, `GT`/`BP` = `downloads/leitprogramme/<name>/{gesamttest,bewertungspaket}.tex`.
**Rechenfehler: keine** in allen vier Musterlösungen, Kapitelaufgaben, Leistenzielen und Clips (`zahlen.py` je grün).
Werkzeuge grün (`pruef-uebungen`, `pruef-formelsatz`, `pruef-leiste`, `pruef-geo`, `pruef-fragen` je 9/9, `pruef-clip`).
Die Befunde unten fangen die Werkzeuge nicht. Nachgeprüft vom Hauptagenten: Vierecke F1/F2, Dreiecke F1, Ähnlichkeit F1/F2/L1, Kreis 3e.

**Behoben 08.10.2026** (ohne Nachprüfung, auf Auftrag): alle HOCH/MITTEL, NIEDRIG fast alle. Gesamttests umgebaut
(Dreiecke 25 P mit Schwerpunkt und h = 2A/g, Umkehrung Pythagoras als Ziel gestrichen; Vierecke neu 24 P, G1–G6;
Kreis 25 P mit Segment über 180°; Ähnlichkeit 25 P, G6 «Laras Fehler», Lochkamera mit Abständen vorher geübt).
Raster je mit einer Regel für (E)-/Folgezeilen und «unmöglich». Zeiten: Dreiecke 210, Vierecke 200, Kreis 215,
Ähnlichkeit 220 min. Bewusst gelassen: Aussprache «Kathete», «subtrahiert» (Hörprobe 10.10.2026: wie bisher, auch «Überstand»),
Schenkel «s» (wie Themenseite), Ähnlichkeit G3 (c) reine Ergebniszeile. Neu vertonte Szenen und Fragetöne:
Berichte der Bearbeiter (Hörprobe offen).

### Dreiecke (`dreiecke`)
**HOCH**
- [x] **D-H1 · Übung «Fläche, Höhe, Umfang», Variante `misch`: Grundseite in m gerundet angezeigt** (`seite.js:852`, `r2(g / 100)`): 3.5 cm → «0.04 m», Sollwert mit 0.035 — 28.5 % dieser Würfe werten die richtige Rechnung als falsch. → ungerundet anzeigen oder ganze cm würfeln.
- [x] **D-H2 · Gleiche Übung würfelt unmögliche Dreiecke**: Variante `zwei` h_a > b (11.8 %), gleichschenklig Basis 10/Schenkel 5 (flach). → neu würfeln.
- [x] **D-H3 · GT deckt Kompetenzen nicht**: Seitenhalbierende/Schwerpunkt 2 : 1, Höhe als Abstand h = 2A/g, Umkehrung Pythagoras ungeprüft (Matrix `seite.py:437` behauptet G2/G3). Kapitel 4 verspricht «prüfst, ob ein rechter Winkel vorliegt», nirgends erarbeitet. G4(b) Hilfsdreieck mit Fusspunkt aussen nie geübt.
**MITTEL**
- [x] D-M1 · Arbeitsbereich 2 A1–A3: Seitenhalbierende, Winkelhalbierende, Mittelsenkrechte aus C liegen so dicht, dass ein Tipp auf die sichtbare Linie zu 43–53 % die Nachbarlinie trifft (falsche Rückmeldung). → C verlegen.
- [x] D-M2 · Raster: Umfang/Fläche je Aufgabe anders bewertet (G4(b) (E) vs. G6(c) Folgepunkt; G5(c) ohne (E)); G6 Folgewert 30.10 → 30.11 (ungerundet); G1 «Aussenwinkel als Innenwinkel» γ-Zeile widersprüchlich; G2 «vertauscht» (b)/(d) zählen trotz falscher Aussage.
- [x] D-M3 · Sperrliste: `ph|2.5|6` (= G7), `ph|4|12` (G4(b)), `da|42|54|84` (G1(b)) fehlen. G4(a) = 3-4-5-Figur aus Arbeitsbereich 3 und Aufgabe 3b.
- [x] D-M4 · Clips: `elemente` «Stumpfes Dreieck» Höhe von B nur nach aussen (B→H statt Fusspunkt–H), «M_I» am Punkt S, Bewegung vor dem Satz; `flaeche` «Warum die Hälfte» Original bleibt stehen; Kontrollfragen wiederholen Einführungszahlen (6-8-10, 5-12-13, a = 5/b = 7/γ = 80°, 6/5/15); zwei gleichartige Klickfragen (Fusspunkt = x der Ecke).
**NIEDRIG**
- [x] Übung «Wie heisst sie?» Rückmeldungen verraten die Lösung; L1 «Fast» bei 7.5/1.5, «=» statt «≈»; Rückmeldung «Das wäre α, wenn β fehlte» falsch; «keine zwei gleich» → ungleichseitig; M_U auf Hypotenusenmitte fehlt; A8 gegebene Strecke grün; Clips: «nicht massstäblich» bei s_c = 9, «?» unter «100°», Klickfragen ohne `eingabe`, «ha/hb» im Fragetext, Aussprache «Zieh C», «Kathete», «subtrahiert» (Hörprobe); GT: Einheiten in G4-Figur, Platz für Skizzen, «Mittelsenk-rechte».

### Vierecke (`vierecke`)
**HOCH**
- [x] **V-H1 · Gleichschenkliges Trapez über b = d definiert** (`seite.py:187`) — jedes Parallelogramm hat b = d (LP zählt es zu den Trapezen) und ist nicht achsensymmetrisch. → b = d **und** α = β (bzw. Symmetrieachse).
- [x] **V-H2 · Übung «Wahr oder falsch?»: drei falsche Gegenbeispiele beim Trapez** (`seite.js:570–573`): «keine rechten Winkel», «Diagonalen verschieden lang», «nicht senkrecht» — rechtwinkliges, gleichschenkliges Trapez bzw. c = 3, v = 1, h = 4 widerlegen.
- [x] **V-H3 · GT G1(a) verlangt die Umkehrung** (aus Diagonalen auf die Form), nirgends geübt; Raster-Begründung «gleich lang ⇒ Rechteck» falsch (gleichschenkliges Trapez). G1(b) «α um 40° grösser» nicht geübt.
**MITTEL**
- [x] V-M1 · Verdeckte Grössen am 1-cm-Raster auszählbar (sim3 A6, sim4 A4, sim5 A4; gesperrter Regler am Anschlag); Clips `trapez` «Rückwärts», `laengen` «Trapez» ebenso. → Raster aus.
- [x] V-M2 · sim2 A6: Falle BD steht 88.2° auf AD (wirkt wie Höhe). → a = 8, h = 3, v = 4.
- [x] V-M3 · GT wiederholt Kapitelaufgaben (G2 ≈ 2d, G6 ≈ 4c, G7 ≈ 4d/Fehlerkasten, G3(b) ≈ 4b, G5 ≈ `trapez-rueck`); Raster: Fläche/Pythagoras-Länge mal (E), mal nicht; Folgepunkt bei unmöglicher Höhe √194 > 13.
- [x] V-M4 · Clips: Mittellinie im rechten Trapez verschoben (`kontrolle-trapez` F2, (7.75|2.5)–(11.75|2.5)); «f» auf e, «b» an AD statt BC, Lot «h» statt h_b; Formeln ohne Klammer gesprochen («zwei mal fünf plus drei, gleich sechzehn» u. a.); Klickfrage Hypotenuse Toleranz 0.45 (19 % Fehltreffer); «U ändert sich» nicht allgemein; Farben Diagonale/Mittellinie uneinheitlich.
**NIEDRIG**
- [x] Aufgabe 1e «Diagonale eingezeichnet» ohne Figur; b = AD in sim2 und GT G2; sim4 c > a einstellbar; Matrix «G2 (c)»; Beschriftungen sim3 A6; Erkunde-✓ bei jeder Bewegung; GT: Aufrunden 642, Umrechnungsfehler Faktor 100, «“Rechteck” genügt», Labels in G3-Figur, Platz; Clips: h_a/h_b roh im Fragetext, Schenkel «s», gesprochene Eigenschaften ohne Bild, Beschriftungen vor dem Ton; Aussprache «Überstand».

### Kreis und Kreisteile (`kreis-kreisteile`)
**HOCH**
- [x] **K-H1 · Aufgabe 3e mehrdeutig** («Am Rand misst ein Stück 7 cm») — das LP definiert den Rand als b + 2r; zweite lösbare Antwort d ≈ 5.20. → «Der Bogen eines Stücks …».
- [x] **K-H2 · GT: Segment über 180° (Kernregel Kapitel 4) ungeprüft**; G2 (Punkt in Höhe h über dem Kreis, Einheiten) und G5(a) (r aus Sehne und Abstand) nicht geübt.
**MITTEL**
- [x] K-M1 · Figur 4b: abgeschnittenes Tischstück schwarz gefüllt (`bog` mit Klasse `lot` ohne `fill:none`).
- [x] K-M2 · Übung «Linie benennen»: Radius als «Sehne» → Meldung «keine Gerade» falsch; gesperrte Regler widersprechen der Figur (sim1 A8 r = 5/a = 3 bei r = 4; sim2 A5/A6) → `verdeckt`.
- [x] K-M3 · Raster: G1(a) (A) vs. «Begründe»; G5 Folgepunkt bei a = r (unmögliche Figur); π ≈ 3.14 als «gerundeter Zwischenwert» lesbar; Einheitenregel nur für (E); Ergebniszeilen G4(b)/(c), G6 ohne (E).
- [x] K-M4 · Clips: `sektor` «Anteil» «90° : 360° = ¼» 2.6 s zu früh (Whisper «Phi» → «viel» ≈ «Viertel»), Rückbewegung nach Szenenende; `kontrolle-sektor` F2 «b ≈ 9.42» abgeschnitten; Stille 3.5–5.3 s am Ende von 9 Szenen (alte `dauer`); R/r klingen gleich («Gross R … klein r»); `kontrolle-linien` F1 Sehnenstück der Sekante als Falle.
**NIEDRIG**
- [x] Bogenmass «5.4» vs. «5.1» (richtig 5.1); h vs. h_Δ in sim4; «π erklären» nicht geübt; Unterlagsscheibe 22 cm; Meldungen `zurueck`/AB1 A7; Bildkleinigkeiten sim2/sim3/sim4; `zahlen.py` alte G5-Zeilen; KI-Beispiele «6π»; Clips: ½ b r ohne Herleitung, Tangente «eine» statt zwei, Beschriftungen R/rₘ/b, s = 8 auf Sehnenhälfte, «∓», «φ» aufrecht, Falschantwort 25°.

### Ähnlichkeit (`aehnlichkeit`)
**HOCH**
- [x] **Ä-H1 · «Ist k kleiner als eins, wird das Bild kleiner»** (Clip `streckung` «Kleiner», `clips.py:273`; ebenso `kurzbeschrieb` und Rückmeldung `kontrolle-streckung` F2) — falsch für k < 0 (k = −1.5 vergrössert). → «zwischen null und eins».
- [x] **Ä-H2 · BP G6 «Zuordnung nach den Buchstaben»: PQ = 9 falsch** (richtig ≈ 11.23); G4(c) Folgepunkt für denselben Begriffsfehler (Länge statt Fläche) widerspricht G1(b)/G5/G6(c).
- [x] **Ä-H3 · Umkehrung Strahlensatz ohne Lagebedingung** (Festhalten 2).
**MITTEL**
- [x] Ä-M1 · Arbeitsbereich 2 ohne `ohneNull: ['k']` — k = 0 zeigt «Infinity»; Laterne 2e ohne Person (`svg.geo-mini .person` fehlt); 4d Ecke C abgeschnitten; Übungsbilder schneiden «SA′ = …» (35 %) und «c = …» ab; 4a «R», 1a/1d Labels auf Achsenzahlen.
- [x] Ä-M2 · `kontrolle-dreiecke` F2: «Der grüne Kreis zeigt die Stelle» — Strecke wird als grüne Linie gezeigt.
- [x] Ä-M3 · «1.5-mal / doppelt so gross» (Fläche 2.25/4) in `streckung` «Negativ» und `kontrolle-streckung` F5 → «Seiten … so lang».
- [x] Ä-M4 · GT: G6 wiederholt 4a (Namen, k = 1.5, Zuordnung); G3 Lochkamera mit senkrechten Abständen nie geübt; G5 irrationales k (√3) kaum geübt; sWs/SsW nur genannt, nicht erfahren/geübt.
- [x] Ä-M5 · Clips: 60° vor der Rechnung im Bild (`dreiecke` «Zwei Winkel»), Fläche mit k = 1.5 neben Bild k = 2, leere Bühne «Zurück zu k», Baum massstäblich vor der Rechnung, Grün für gegebenes q; Kontrollfragen = Themenseite A4a/A6/A2.
**NIEDRIG**
- [x] Kapitel 3 ohne Aufgabe an der Figur; Leiste 2 A1 doppeldeutig; Vorwissensclip passt kaum; Tippziel A′B′ bei k = −1 (55 %); «parallelentreu»; Regler δ blau; Übungstext «flaeche»; 3b «(fast)»; Clips: Pfeil 4.9 statt 4.5, Bewegung vor Satz, A′ auf «−2», rote Gerade vor dem Kippen, «≈ 5.80», «Seite 4» mehrdeutig; GT: Einheiten gemischt, G3(b)/(c) nur (E), G4(b) cm², Platz für Skizzen.

### Themenseiten 5.2a–d: beim Bau gemeldet und bestätigt
**Behoben 08.10.2026:** alle Punkte; g5-2b Anim 4: Schenkel b/d, Versatz heisst jetzt v; Clips g5-2b-anim-scherung (Szenen 2–4, Bilder neu) und g5-2b-anim-umformung (Szene 3) neu vertont. 5.2a bleibt bei SsW/sSW, mit Hinweis auf SSW in 5.3.
- [x] g5-2c: A3 «Einheitskreis (d = 1, also r = 1/2)» (Z. 1244, falsch: r = 1); Merksatz Bogenmass «in 5.4» (Z. 1373, eingeführt in 5.1); «der Einheitskreis nimmt das π-fache» (Z. 791, gemeint Kreis mit Radius r); Lösung A1.4 «definiert die Tangente sogar» (Z. 1208); u/U; Zentri-/Mittelpunktswinkel; φ-Bereich [0°; 360°[ vs. Regler 360°; Kasten «Lieber geführt?» zeigt auf Planimetrie.
- [x] g5-2d: **k < 0 «gegensinnig»/«gespiegelt»** (Z. 487, Live-Anzeige Z. 1619, 1628, 3122) — falsch, Drehung um 180°, gleichsinnig; Verhältnistreue «gleich k» (Z. 490), «Längen mit k» (Z. 935, Fehlerkasten) → |k|, |k|³.
- [x] g5-2b: Anim 4 Schenkel «e / f» und «U = a+c+e+f» (Z. 837–838; e, f sind Diagonalen), Legende ohne «≈»; «Animation 4/5» → 6/7 (Z. 588, 605); A7 Drachen d₁, d₂ statt e, f (Z. 1275); A = a·h vs. g·h; Clip `g5-2b-anim-umformung` «zwei Trapeze ergeben das Rechteck» (zuerst Parallelogramm).
- [x] g5-2a: «Lot auf die Gegenseite/Grundseite» statt «auf die Gerade durch …» (Z. 711, 792); A7 «5√5 m»; «Waagerechte»; «SsW/sSW» vs. 5.3 «SSW».
