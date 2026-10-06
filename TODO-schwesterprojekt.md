# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

**Bereinigt am 28.09.2026:** Alle Einträge wurden gegen das Physik-Repo geprüft
(Stand `f115899`, nur gelesen). Erledigte und gegenstandslose sind entfernt —
ihr Wortlaut steht in der Git-Geschichte dieser Datei. Übrig waren danach drei; neue kommen unten dazu.
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 30.09.2026 · Zwei Styleguide-Regeln übernehmen (Entscheid Auftraggeber 30.09.2026)

**Was.** Zwei Regeln, die Mathe am 29.09.2026 eingeführt hat, gelten auch in Physik.
Nachgezählt im Physik-Repo (Stand `5f27e6f`, nur gelesen).

**1. Aufzählende Mengen mit Strichpunkt.** Mathe STYLEGUIDE §2.11, Absatz «Aufzählende
Mengen»: \(\{3;\,4\}\) statt \(\{3,\,4\}\), in JS-Text `{ 3; 4 }`; Komma nur in Prosa,
Koordinaten weiter `(3 | 4)`.
- *Wo in Physik:* `STYLEGUIDE.md` §2 (Physikalische Notation) hat heute **keinen**
  Abschnitt zu Mengen oder Intervallen — die Regel kommt als neuer Unterabschnitt dazu,
  sinnvollerweise nach §2.6 (Schreibweise von Werten).
- *Inhalt anfassen: nichts.* Aufzählende Mengen gibt es in Physik **keine**: 0 Treffer
  in `themen/*.html` (18 Seiten), `leitprogramme/*.html` (11), `clips/*.json` und den
  übrigen HTML-Seiten (`grep -P '\\\{\s*-?[0-9a-z.]+\s*[,;]'`). Die Regel wirkt nur für
  künftige Inhalte.

**2. Vertiefungsaufgaben stehen am Ende der Aufgabenreihe.** Mathe STYLEGUIDE §5.4 und
Checkliste §8: reguläre Aufgaben vor der Vertiefung; kommt eine dazu, rückt die
Vertiefung nach hinten, mit allen IDs, `toggleL`-Argumenten und Prüffunktionen.
- *Wo in Physik:* Die Regel setzt eine Vertiefungsaufgabe voraus, und die kennt Physik
  heute nicht: `STYLEGUIDE.md` §4.3 sagt «**Genau** 6 Aufgaben (A1–A6), nicht mehr»,
  §9 «Genau 6 Aufgaben», `style.css` hat **keine** Klasse `aufg-vertiefung` (0 Treffer),
  keine Themenseite nutzt sie.
- *Was dafür nötig ist:* (a) §4.3 und §9 um «optional A7 Vertiefung, am Ende der Reihe»
  ergänzen, wie Mathe §8; (b) die Klasse `.aufg-vertiefung` aus Mathe `style.css`
  (Z. 467–486, Orange-Familie, Pille hinter `aufg-titel-text`) übernehmen — sie nutzt
  `--orange`, `--orange-hell`, `--orange-rand`; prüfen, ob Physik diese Tokens hat.
- *Sonderfälle, die dabei auffallen:* Vier Themenseiten haben schon heute mehr als sechs
  Aufgaben, ohne Vertiefungs-Markierung: `p0-1-vorwissen-mathematik` (A1–A12),
  `p0-2-vorwissen-physik` (A1–A12), `p6-2-elektrizitaet` (A1–A16) und
  `p6-2-prototyp-layout` (A1–A16). In der Physik-Sitzung entscheiden: als Vertiefung
  markieren und ans Ende ordnen, oder die §4.3-Ausnahme für diese Seiten festhalten.
- *Verwandt, schon vorhanden:* Die Physik-Leitprogramme kennen «Kern zuerst, Vertiefung
  danach» (`.task-id .kern` / `.vert`, z. B. `leitprogramm-vorwissen.html` Z. 428–431;
  in allen zehn Leitprogrammen vergeben, je 9–17 `kern` und 7–9 `vert`,
  `uebungstest-waermelehre.html` ohne). Dieselbe Idee, andere Klassen — nicht vermischen.

**Warum.** Gleiche Notation und gleicher Aufgabenaufbau in beiden Lehrmitteln; Lernende
wechseln zwischen den Fächern.

### 02.10.2026 · `build-clips.py`: bewegte Parabel im `graf` und Fragen im Clip (**abgenommen 03.10.2026, portierbar**)

**Was.** Neuer Schlüssel `bewegung` für `parabeln` im `graf` (Stützpunkte `[t, a, u, v]`,
Begleiter `scheitel`, `nullstellen`, `yachse`, `marken`, `laeufer`) und neues Drehbuchfeld `fragen` (Clip hält an
und fragt, `FRAGEN_JS`, Vorlesen über das Mathe-eigene `scripts/build-clip-fragen-ton.py`;
HOWTO-clips «Fragen im Clip»), dazu die Konstante `BEWEGUNG_JS`, die nur in Clips mit Bewegung
`seek(t)` um `bewegen(t)` erweitert, und `data-t0` am Bild-Layer. Beschreibung in Mathe
`HOWTO-clips.md`, «Bewegte Parabel im `graf`».
**Wo in Physik.** `scripts/build-clips.py` hat `graf_svg` mit `parabeln` und denselben
Abspieler (`window.__seek = seek;` je 1 Treffer, nachgezählt 02.10.2026, nur gelesen).
Physik nutzt den `graf` heute in **keinem** seiner 234 Drehbücher — der Übertrag hält das
Werkzeug gleich, er ändert keinen Clip.
**Warum.** Clips sollen Zusammenhänge zeigen statt beschreiben (Auftraggeber,
30.09.2026). `abgleich.py`: `scripts/build-clips.py` fällt dadurch von 83.6 % auf
74.5 % (Grundlinie 84 %) — der Eintrag in `OFFEN` kommt erst, wenn der Prototyp
angenommen ist. **Abgenommen am 03.10.2026** mit der Freischaltung von
`leitprogramme/lineare-funktionen.html` (Hörprobe und KI-Test durch den Auftraggeber);
der `OFFEN`-Eintrag in `abgleich.py` kann damit gesetzt werden.

**Nachtrag 03.10.2026 — `bewegung` auch für `geraden`.** Derselbe Schlüssel an einer
Geraden, Stützpunkte `[t, m, q]` für \(y = m x + q\); gezeichnet wird die am Fenster
abgeschnittene Strecke. Begleiter: `yachse`, `nullstelle`, `marken`, `laeufer` und
`dreieck` (mitlaufendes Steigungsdreieck mit Δx und Δy). Dazu im Abspieler
`bewegeGerade()` in `BEWEGUNG_JS`, die Sammelliste `BEW` nimmt `[data-bewg]` mit auf,
und `bewZustand()` ist auf beliebig viele Zahlen je Stützpunkt verallgemeinert
(`[t, a, u, v]`, `[t, m, q]`, `[t, x]`). `fragen` vom Typ `klick` funktionieren damit
auch über einer bewegten Geraden — der Tipp wird aus dem `data-fenster` des bewegten
Pfads in Koordinaten umgerechnet, und das trägt jetzt auch eine Gerade.
- *Nachgewiesen gleich geblieben:* `clips/g3-2-achsenabschnitt.html` (ohne Bewegung)
  baut Byte für Byte gleich; `g3-3-lp-verschieben` unterscheidet sich nur im
  eingefügten Skript und rendert bei 3/12/28/48/70 s pixelgleich.
- *Wo in Physik:* unverändert — der `graf` wird in keinem der 234 Drehbücher genutzt;
  der Übertrag hält nur das Werkzeug gleich. Zusammen mit dem Eintrag oben portieren.
- *Vorbild:* die acht Clips `g3-2-lp-*` («Gerade sehen»), Leitprogramm Lineare Funktionen.


### 02.10.2026 · Drei Werkzeuge aus dem Leitprogramm Quadratische Funktionen (Theme, Gesamttest als PDF, vorgelesene Fragen)

Nachgezählt im Physik-Repo (Stand `ebe6205`, nur gelesen). Vorbild in Mathe:
`leitprogramme/quadratische-funktionen.html`, seit 02.10.2026 freigeschaltet.

**1. Theme `begreifbar-schlicht`** — `clips/themes/begreifbar-schlicht.json`: Kopie von
`begreifbar.json` mit `"karo": false`, `"rand": false`, neuer `beschreibung` und einer fünften
Farbe in `farben` (Tinte, `farbe: 5` = ungefärbte Punkte, seit 03.10.2026)
(HOWTO-clips «Theme `begreifbar-schlicht`»). Karo und Koordinatengitter eines `graf`
stören sich.
- *Wo in Physik:* `clips/themes/` hat `begreifbar`, `heft`, `papier`, `tafel`;
  `scripts/build-clips.py` wertet `karo` und `rand` schon aus (Zeilen 718 ff.) — **kein
  Code nötig**, nur die Datei. Als Vorlage Physiks eigene `begreifbar.json` nehmen
  (Bernstein `#8a4a0e`, Karo `rgba(138,74,14,.10)`), nicht die Mathe-Datei — sonst
  kommen Mathes Blautöne mit.
- *Inhalt anfassen: nichts.* 233 Drehbücher setzen `begreifbar` und bleiben so; gilt für
  neue Clips. Den Satz «Standard für neue Clips» in Physiks `HOWTO-clips.md` übernehmen.

**2. Gesamttest und Bewertungspaket als PDF aus LaTeX** — `scripts/build-lp-pdf.py`
(32 Zeilen, übersetzt `downloads/leitprogramme/**/*.tex` mit `latexmk -pdf` in einem
temporären Ordner, legt nur das PDF ab) und `downloads/leitprogramme/lp-druck.sty`
(42 Zeilen: pdfLaTeX, T1, mathpazo, tcolorbox, pgfplots, needspace). Dazu der Ansatz
aus `HOWTO-leitprogramme.md` §9: Bewertungspaket (Musterlösung + Kriterien) **getrennt**,
damit Lernende ihre Lösung einer KI zur Bewertung geben können; KI-Hinweis in
Selbstverantwortung, nicht an die Schule gerichtet.
- *Wo in Physik:* Es gibt **kein** `downloads/` und kein PDF in den Leitprogrammen
  (0 Verweise auf `.pdf`, kein `window.print`); 8 der 11 Seiten in `leitprogramme/`
  haben einen Gesamttest als HTML. LaTeX liegt nur unter `.quellen/formelsammlung/`.
  `latexmk` und `pdflatex` sind auf dem Rechner da (gleiche Maschine).
- *Anpassen:* In `lp-druck.sty` die Farben auf Bernstein und die Fusszeile
  «physik.begreifbar.ch»; LuaLaTeX geht nicht (luaotfload-tool fehlt), darum pdfLaTeX.
- *Entscheid offen:* ob Physik seine HTML-Gesamttests umstellt — das ist ein
  inhaltlicher Entscheid des Auftraggebers, kein reiner Übertrag. Das Skript
  allein kann vorab übernommen werden.

**3. Vorgelesene Fragen im Clip** — `scripts/build-clip-fragen-ton.py` (77 Zeilen,
bewusst Mathe-eigen, nicht in `abgleich.py`). Holt `sprich()` und `aussprache()` aus
`build-clip-ton.py` und `fragen_texte()` aus `build-clips.py` per importlib.
- *Wo in Physik:* `build-clip-ton.py` hat `aussprache` (Z. 176) und `sprich` (Z. 199);
  `fragen_texte` fehlt in `build-clips.py` (0 Treffer) — kommt erst mit dem Eintrag
  «bewegte Parabel und Fragen im Clip» oben. **Darum erst nach diesem portieren**; die
  Datei selbst lässt sich dann unverändert kopieren (Pfade aus dem eigenen Dateipfad).
- *Inhalt anfassen: nichts.* Kein Physik-Drehbuch hat `fragen` (0 von 233).

**Warum.** Leitprogramme sollen in beiden Fächern gleich arbeiten: ruhiges Bild für
bewegte Grafen, Test zum Ausdrucken mit eigenständiger Bewertung, Clips, die fragen.
Die drei Dateien stehen nicht in `abgleich.py`; ein `OFFEN`-Eintrag ist nicht nötig,
solange sie nicht als KERN aufgenommen werden.

---

### 03.10.2026 · Die Leitprogramm-Erstellung als Ganzes (Didaktik, Kapitelmuster, Prüfung)

Nachgezählt im Physik-Repo (Stand `ebe6205`, nur gelesen). Die drei Einträge oben decken
das **Clip-Werkzeug** ab. Was fehlt, ist alles, was aus einer Seite ein Leitprogramm nach
dem heutigen Muster macht. Ohne diesen Block lässt sich in Physik kein Leitprogramm nach
dem Vorbild `lineare-funktionen` bauen — mit ihm schon.

**1. `HOWTO-leitprogramme.md` — Gesamtfassung** (Mathe 599 Zeilen).
- *Wo in Physik:* vorhanden, aber die **alte technische Fassung** (385 Zeilen, Kopf
  «ein Leitprogramm ins Repo holen», übernommen aus Mathe Stand 01.09.2026, Gliederung
  Übertragsliste / Prüfen / Nicht tun). Es fehlen §1 (RLP-Bindung), §2 (Planung,
  Kompetenzmatrix), §3 (Umfang nach Format), §4 (**das Kapitelmuster**), §8 (Simulationen
  mit Aufgabenleiste), §9 (Übungen mit Rückmeldung, PDF-Gesamttest), §15 (Prüfung vor der
  Freischaltung samt Prüfliste).
- *Anpassen:* Die RLP-Quelle ist eine andere (`../Physik-GL.pdf` statt `Math-GL.pdf`), und
  §10 «Notation und Fachsprache» ist mathe-eigen — in Physik gehören dort Einheiten,
  Formelzeichen und signifikante Stellen hin. §1.1 («Kompetenzliste wörtlich übernehmen»)
  gilt unverändert.
- *Inhalt anfassen:* Die **11 bestehenden Physik-Leitprogramme** bleiben, wie sie sind;
  die Fassung gilt für neue. 8 von ihnen haben einen Gesamttest als HTML — ob sie auf PDF
  umgestellt werden, ist ein eigener Entscheid (siehe Eintrag vom 02.10., Punkt 2).

**2. STYLEGUIDE §6.5 «Leitprogramme»** — in Mathe `STYLEGUIDE.md` ab Zeile 1236, das
Verbindliche hinter dem HOWTO.
- *Wo in Physik:* **kein §6.5** (0 Treffer). Der Abschnitt muss neu angelegt werden.

**3. Das Kapitelmuster als Bauskript** — Mathe `scripts/lp/lineare-funktionen/`:
`seite.py` (545 Z., baut die Seite aus einer Kapitelbeschreibung), `seite.js` (662 Z.:
Koordinatensystem, **Aufgabenleiste** `Leiste()`, Simulationen, **Übungen mit Rückmeldung**
`TYPEN`, Minigrafen), `grafgeom.py` (75 Z.) und `pruef-graf.py` (139 Z.), die jede
Beschriftung im Clipbild ausrechnen statt schätzen, dazu `clips.py` (866 Z.) und `README.md`.
- *Wo in Physik:* `scripts/lp/` **fehlt ganz**. Die 11 bestehenden Leitprogramme sind von
  Hand geschrieben, ohne Generator.
- *Anpassen:* `seite.py` und `seite.js` sind zur Hälfte Fachinhalt (Geraden, Steigung) und
  zur Hälfte Gerüst. Portierbar ist das Gerüst — `Achsen()`, `Leiste()`, der Übungsrahmen
  mit `lesen()`/`pruefen()`/`loesung()`, die Minigrafen; die `TYPEN` und die Simulationen
  schreibt Physik neu. **Nicht Datei für Datei kopieren**, sondern das Muster übernehmen
  und am ersten Physik-Leitprogramm erproben.

**4. Prüfung vor der Freischaltung** — Skill `.claude/skills/lp-pruefung/SKILL.md` (90 Z.)
und vier Werkzeuge: `.claude/tools/pruef-uebungen.mjs` (108 Z.), `pruef-leiste.mjs` (73 Z.),
`pruef-fragen.mjs` (127 Z.), `sprechzeiten.py` (58 Z.).
- *Wo in Physik:* `.claude/skills/` enthält **nur `preflight`**; von den vier Werkzeugen
  ist **keines** da (`.claude/tools/` hat `aufnahme-anim.mjs`, `build-bilder.mjs`,
  `pruef-clip.mjs`, `pruef-mathjax.mjs`, `render-check.mjs`, `scan-live.mjs`).
- *Reihenfolge:* `pruef-fragen.mjs` setzt `fragen` im Clip voraus (Eintrag 02.10.) und
  `pruef-uebungen.mjs` die Testhaken `box.__aufgabe`/`box.__typ` aus dem Kapitelmuster
  (Punkt 3). `pruef-leiste.mjs` und `sprechzeiten.py` laufen sofort — Letzteres ist auch
  ohne Leitprogramm nützlich, es misst nur Sprechzeiten im Clip.
- *Anpassen:* Die vier Werkzeuge sind fachneutral; einzig der Pfad-Vorspann und der
  Massstab in `SKILL.md` (Themenseite, RLP-Datei) sind einzusetzen.

**Warum.** Die Prüfung am Vorbild hat gezeigt, dass §14 (Selbstkontrolle) allein nicht
reicht: Drei unabhängige Agenten fanden danach je rund 25 Befunde, darunter fachlich
Falsches. Das Verfahren — bauen, unverlinkt veröffentlichen, prüfen lassen, beheben,
abnehmen, freischalten — gehört zum Format, nicht zum Fach.

**Aufwand, ehrlich.** Punkt 1, 2 und 4 sind Übertragsarbeit mit Anpassung (ein Durchgang).
Punkt 3 ist kein Übertrag, sondern ein **Neubau am ersten Physik-Leitprogramm**: Die
Simulationen und Übungstypen sind Fachinhalt. Realistisch ist, Punkt 1, 2 und 4 zuerst zu
portieren und Punkt 3 beim ersten neuen Leitprogramm entstehen zu lassen — so, wie es
`scripts/lp/quadratische-funktionen/` hier auch entstanden ist.

**Was in Physik heute ungenutzt bliebe.** `bewegung` und `fragen` im `graf` (Einträge
02.10./03.10.) hängen am Bildtyp `graf` — und den nutzt **kein einziges** der 234
Physik-Drehbücher. Der Übertrag hält das Werkzeug gleich; gebraucht wird er erst, wenn ein
Physik-Clip ein Koordinatenbild zeigt (etwa p-V-Diagramm, Kennlinie, Weg-Zeit-Gesetz).
Dafür spricht einiges — aber es ist ein eigener Entscheid, kein Automatismus.

### 06.10.2026 · Leitprogramme-Seite: Kacheln wie in Mathe (Auftrag Auftraggeber 06.10.2026)

**Was.** `leitprogramme.html` bekommt den Aufbau, den Mathe am 06.10.2026 eingeführt hat (Commits
`27780cf`, `f94de6b`): **eine Kachel je Leitprogramm**, die ganze Kachel führt zum Leitprogramm
(unsichtbarer Link `a.karte` über der Kachel). Auf der Kachel steht **je Themenseite eine Zeile**: der
Titel der Themenseite und rechts eine Pille mit ihrer Nummer, die zur Themenseite führt. Nur Titel und
Nummer — keine Beschreibung, keine Meta-Zeile. Gegliedert nach Themenbereich (in Physik: Lerngebiet),
innerhalb nach Nummer sortiert; keine Einleitung über den Kacheln. Vorlage: `leitprogramme.html` in Mathe,
`<style>`-Block im Kopf und Abschnitt zwischen `LEITPROGRAMME:ANFANG` und den alten Leitprogrammen;
Linkprüfung mit einem `elementFromPoint`-Lauf (Titel → Leitprogramm, Pille → Themenseite).

**Nachgezählt im Physik-Repo** (Stand `57fde7e`, nur gelesen):
- Heute: 17 Kacheln `a.lp-karte` in `div.lp-liste` (Nummer, Titel, Beschreibung, Meta, Pfeil) unter vier
  `h2` (Lerngebiet 0, 4, 5, 6) plus «Veraltet: wird entfernt» (3 Kacheln).
- **Namenskonflikt:** `style.css` (Z. 1626–1670) definiert schon `.lp-liste`, `.lp-karte`, `.lp-nr`. Mathe
  benutzt `.lp-nr` für die Nummer des Themenbereichs — beim Übertrag eigene Namen oder die bestehenden
  Regeln ersetzen, nicht beide nebeneinander.
- Farbe: eine Bereichsfarbe, Bernstein (`--bernstein`, `--bernstein-hell`, `--bernstein-rand` vorhanden),
  statt Blau/Violett; die Gliederung nach Fach (Grundlagen-/Schwerpunktfach) entfällt.
- Themenseiten (`themen/`, 17): 0.0–0.5, 4.1–4.5, 5.1–5.3, 6.1, 6.1a, 6.2.
- Vorgeschlagene Zuordnung (aus der Meta-Zeile «Lerngebiet …» und den Kästen «Lieber geführt?»):

| Leitprogramm | Zeilen (Pille → Themenseite) |
|---|---|
| `leitprogramm-rechnen` | 0.1 Rechnen und Schliessen |
| `leitprogramm-vorwissen` «Grössen, Messen, Druck» | 0.2 Grössen, Einheiten und Messen; 0.3 Messen — Waagen, Dichte, Einheiten *(zu entscheiden; der Kasten steht auf 0.0–0.5 und 4.1/4.2/4.5)* |
| `leitprogramm-kinematik` … `-hydrostatik` | je eine: 4.1 Kinematik des Schwerpunkts, 4.2 Dynamik, 4.3 Energie, 4.4 Statik von Festkörpern, 4.5 Hydrostatik |
| `leitprogramm-waermemenge` | 5.1 Temperatur; 5.2 Wärme (Meta: «Lerngebiete 5.1 und 5.2») |
| `leitprogramm-experimente-waerme`, `-heizen` | je 5.2 Wärme |
| `leitprogramm-waermeausdehnung`, `-ideale-gase` | je 5.3 Wärmeausdehnung |
| `uebungstest-waermelehre` | 5.2 Wärme; 5.3 Wärmeausdehnung (Meta auch «0») |
| `leitprogramm-elektrizitaet` | 6.2 Elektrizität |

**Offene Frage an den Auftraggeber, vor dem Übertrag:** In Mathe hat jede Themenseite höchstens ein
Leitprogramm, darum reicht ihr Titel. In Physik teilen sich **drei** Leitprogramme die Themenseite 5.2
(Wärme im Experiment, Wärmemenge, Heizen) und **zwei** die 5.3 (Wärmeausdehnung, Ideale Gase) — mit nur dem
Themenseitentitel wären diese Kacheln nicht zu unterscheiden. Vorschlag: In diesen Fällen den Titel des
Leitprogramms als Kopfzeile der Kachel, darunter die Zeilen mit Nummer. Ebenso offen: ob «Veraltet: wird
entfernt» (3 Kacheln) im alten Aufbau bleibt (in Mathe bleiben die alten Leitprogramme unverändert).

**Nebenbefund, nicht Teil des Auftrags:** Die Physik-Indexseite hat keine LP-Pillen (`karte-lp`/`lp-link`:
0 Treffer), und nur 6 Themenseiten (0.x ausgenommen) tragen einen Kasten «Lieber geführt?» (4.1–4.5, 6.2).
Ob die Mathe-Regel «fünf Stellen» auch für Physik gelten soll, ist nicht entschieden.

**Warum.** Gleiche Bedienung in beiden Fächern; die Seite zeigt auf einen Blick, zu welcher Themenseite
ein Leitprogramm gehört.
