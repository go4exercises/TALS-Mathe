# TODO — Leitprogramm Quadratische Funktionen (Stand 02.10.2026)

Legende: `[x]` erledigt · `[–]` bewusst nicht geändert (Grund dahinter) · `[ ]` offen.
Prio: **HOCH** = Lernende lernen Falsches · **MITTEL** = irreführend, widersprüchlich oder
unvollständig · **NIEDRIG** = Kleinigkeit/Konvention.

Seite: `leitprogramme/quadratische-funktionen.html`, gebaut aus
`_intern/lp-quadratische-funktionen/seite.py` + `seite.js` (Änderungen dort, nicht in der HTML-Datei).
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
Zeilen: Stand Commit `3ebeed9`. `seite.*` = `_intern/lp-quadratische-funktionen/`.

### HOCH

- [ ] **Clip `verschieben`, Szenen «Merke» und «v senkt»:** «x s schiebt sie waagrecht, mit
  umgekehrtem Vorzeichen» und «Beim y s stimmt das Vorzeichen mit der Richtung überein» sind
  falsch: \(x_s = 2\) schiebt nach rechts, gleiches Vorzeichen. Umgekehrt ist nur die Zahl *in
  der Klammer*. Der Kontrollclip sagt es richtig. → «x_s steht in der Klammer mit umgekehrtem
  Vorzeichen», «Hinter der Klammer stimmt …»; Bildtext gleich; neu vertonen.
- [ ] **Clip `verschieben`, Szene «Warum rechts»:** Die Bewegung `[[0,1,2,0],[1.5,1,2,0],[3.0,1,1,0],
  [4.5,1,2,0]]` zeigt bei 3 s \(S(1 \mid 0)\), während Bild und Ton «\(x = 2\)» sagen. → Parabel bei
  \(x_s = 2\) stehen lassen.
- [ ] **Übung «Nullstellen bestimmen», Hinweis** (`seite.js:389`): «Produkt c, Summe b» — für die
  Nullstellen gilt Summe \(-b\) (\(x^2-x-6\): Nullstellen −2, 3, Summe +1). Führt direkt zum
  Vorzeichenfehler. → «zwei Zahlen mit Produkt c und Summe −b».
- [ ] **Übung «Produktform → Grundform», Diagnose** (`seite.js:365–366`): Bei \(b = 0\) bzw.
  \(c = 0\) (wird gewürfelt) trifft `gl(e.b,-A.b)` bzw. `gl(e.c,-A.c)` immer zu → falsche Meldung
  (z. B. \(2(x-3)(x+3)\), nur c falsch → «Vorzeichen von b»). → Bedingung `A.b !== 0` bzw. `A.c !== 0`.

### MITTEL

- [ ] **Gesamttest prüft Kapitel 3 nicht:** keine Diskriminante, keine Nullstellen aus der
  Grundform, keine Produktform aus der Grundform (HOWTO §9: «Jedes Kapitelziel wird geprüft»).
  → Aufgabe ergänzen, z. B. \(x^2-2x-8\): Anzahl Nullstellen mit \(D\), Nullstellen, Produktform
  (3 P, Teil A); Punkte, Paket, Selbsteinschätzung und Seite nachführen.
- [ ] **Kontrollclips verraten die Antwort im Bild**, weil der erste Stützpunkt schon die Lösung
  ist: `kontrolle-nullstellen` F4 (Nullstellen −2, 4 beschriftet), `kontrolle-extremwert` F1–F4
  (Hochpunkt bei 5, Läufer «A = 25»), `kontrolle-formen` F3. → neutrale Startparabel, Lösung erst
  nach der Antwort.
- [ ] **Abgefragt, aber nicht eingeführt:** Wertemenge (Aufgabe 1c, `seite.py:162`); quadratische
  Ergänzung (Aufgabe 2b; nur das Wort in `seite.py:199`, kein Clip, keine Übung). Die Übungen in
  Kapitel 2 gehen nur Richtung Grundform; Grund- → Scheitel-/Produktform fehlt als Übung.
- [ ] **Definition fehlt:** \(f(x)=ax^2+bx+c,\ a \neq 0\) steht nirgends; das Wort «Diskriminante»
  nur im Link; im Clip `achse-bleibt` erscheint \(D\) ohne \(D = b^2-4ac\).
- [ ] **«Achse» ohne Zusatz** in `kontrolle-nullstellen` (13 ×, mal x-Achse, mal Symmetrieachse),
  `kontrolle-formen` F4, `kontrolle-aufstellen` F2-Rückmeldung, `kontrolle-extremwert` F3 —
  wie im Einführungsclip (Commit 9c1a4a5) angleichen; neu vertonen.
- [ ] **Clip `a-finden`, «Merke»:** \(a(x-u)^2+v\) → \(a(x-x_s)^2+y_s\).
- [ ] **Sim 2, Grundform gerundet ohne «≈»** (`seite.js:157,162`): \(a=0.25,\ x_s=0.5\) zeigt
  «0.06» statt 0.0625 (HOWTO §8b). → `genau`-Prüfung wie bei der Produktform.
- [ ] **Übung «Scheitel + Punkt → a»** (`seite.js:393`): Bei \(d = \pm 1\) (≈ 37 %) prüft sie das
  Quadrieren nicht (bei \(d=1\) gilt die falsche Rechnung als richtig). → \(|d| \ge 2\).
- [ ] **Bewertungspaket, Raster für die KI unscharf:** welcher Punkt der «Ergebnispunkt» ist (`:44`);
  «Typische Fehler»-Abzüge überschneiden sich mit Rasterzeilen (G7 `:105`, G8 `:115`); G2 koppelt
  Scheitel und \((0 \mid 10)\) in einem Punkt; G6 zeigt den Scheitelweg nur halb (`:92–93`);
  gleichwertige Schreibweisen (\(-\tfrac14\)) nicht geregelt; Selbsteinschätzung 16–20 P ohne
  Kapitelzuordnung (`:121`).
- [ ] **Beispiele wiederholt** (HOWTO §4): Sim 2 A6 \(x^2-4x+3\), Sim 3 A2/A5, Sim 4 Fall A,
  Sim 5 A1/A2 nehmen die Clip-Beispiele; Übung «Mauer» kann \(L = 60\) würfeln = Aufgabe 5a;
  Gesamttest G8 hat dasselbe Modell \(x(L-2x)\) wie 5a.
- [ ] **HOWTO §9/§10:** «Warum»-Aufgabe nur in Kapitel 2; Kapitel 2 und 5 ohne Aufgabe am Graphen;
  Gesamttest ohne Begründungsteil; Synonyme der Themenseite (Linearfaktorform, allgemeine Form)
  fehlen.
- [ ] **Farben wechseln die Bedeutung** zwischen Kapitel 1 (\fa = a, \fb = x_s, \fc = y_s) und
  Kapitel 2/3 (\fa = c, \fb = Nullstellen, \fc = Scheitel).
- [ ] **Extremwert-Regel zu eng** (`seite.py:295`): nur «Nullstellen → Mitte → Maximum»; Hinweis auf
  \(-\frac{b}{2a}\) und Minimum bei \(a \gt 0\) fehlt. «Drei Punkte → drei Gleichungen»
  (`seite.py:263`) steht im Festhalten, wird aber nirgends geübt.

### NIEDRIG

- [ ] Übungen: Nochmals «Prüfen» nach ✓ setzt die Serie auf 0 (`seite.js:465–468`); «+3» und
  «.5» werden abgelehnt; Schreibweise \(2(x-3)x\) statt \(2x(x-3)\) (`seite.js:360`).
- [ ] Aufgabenleisten: Sim 2 A6 und Sim 3 A5 verlangen den Startzustand (sofort ✓); Sim 1
  «nochmals» setzt `bewegt` nicht zurück; Sim 5 A1: x = 4 beim Start schon besucht.
- [ ] Formulierungen: `seite.py:147` «\(a\) verschiebt nichts: \(a \gt 0\) nach oben» →
  «nach oben geöffnet», «schmaler als die Normalparabel»; `:232` «Bei \(b=-4\)» → «Bei \(a=1,\ b=-4\)»;
  `:237` «ohne Rechnen» → «ohne die Nullstellen zu berechnen»; «gespiegelt», «gestaucht» in Übungen
  (`seite.js:318–329`) nie eingeführt; Kapitel 3 trägt nur K2 (auch K1); 5a ohne Definition von x.
- [ ] Clips, Zeitversätze in `verschieben` («a formt», «v senkt» sagt «um eins», sichtbar um 3;
  «Zusammen») und `kontrolle-scheitelform` F4; Beschriftung «S(0 | 0)» überdeckt die Achsenzahl 1.
- [ ] Clips, Fragen: `kontrolle-nullstellen` F4 zwei verschiedene «Summen» und Rückmeldung verrät
  die Lösung (Text ≠ Ton); `kontrolle-scheitelform` F1 «y_s hinter der Klammer» ohne Klammer;
  `kontrolle-extremwert` F3 ohne `fallen`; `kontrolle-aufstellen` F5 Falle (3 | 3) schwach.
- [ ] Clips, Wortlaut: `mitte` «Die Fläche ist eine Parabel» → «Der Graph der Fläche …»;
  `kontrolle-extremwert` F4: Lage von x zur Mauer nicht gesagt; `a-finden`: Wurfbahn bis −4 m.
- [ ] `g1-3-binome-erkennen` nennt die Binomvariablen a, b — im LP sind das Koeffizienten; kurzer
  Hinweis neben dem Clip.
- [ ] PDFs: G8 «Gib die Masse» → «die Abmessungen»; G8 nur 7 Linien (→ 10–12), G6 → 6–7;
  G3-Grafik: Punkt \((0 \mid -1)\) überdeckt die Zahl −1; Bewertungspaket: Überschrift §3 allein
  am Seitenende (`\needspace`); Datenschutz: Hinweis auf Foto-Metadaten (Standort) fehlt; «die
  Summe von 24» → «die Gesamtpunktzahl (von 24)».

---

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
