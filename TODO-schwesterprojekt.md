# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

**Bereinigt am 28.09.2026:** Alle Einträge wurden gegen das Physik-Repo geprüft
(Stand `f115899`, nur gelesen). Erledigte und gegenstandslose sind entfernt —
ihr Wortlaut steht in der Git-Geschichte dieser Datei. Übrig waren danach drei; neue kommen unten dazu.
**Abgeräumt am 06.10.2026:** vier Einträge vom 30.09.–03.10.2026 (Styleguide-Regeln, `build-clips.py`
mit Bewegung und Fragen, drei Werkzeuge, Leitprogramm-Erstellung) — in Physik umgesetzt
(Warteschlange `OFFEN` in `scripts/abgleich.py`, Quelle Physik, 03.10.2026; nachgesehen: STYLEGUIDE §2.6a
und §5.5, `scripts/lp/` mit sechs Leitprogrammen, Skill `lp-pruefung`, vier Prüfwerkzeuge).
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

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

### 06.10.2026 · Clip-Bibliothek `clips.html`: drei Spalten je Themenseite (Auftrag Auftraggeber 06.10.2026)

**Was.** Den Aufbau übernehmen, den Mathe am 06.10.2026 eingeführt hat (Commits `d1403b0`, `9b87336`,
`4bcae0c`, `a8b9c0d`, `36f874b`). Grundstruktur bleibt (Lerngebiete aufklappbar). Im Lerngebiet je
Themenseite eine Zwischenüberschrift (Nummer + Titel, Link zur Seite) und eine dreispaltige Tabelle:
1. **Animationen** — Clips mit `animation`, hinterlegt, Link «Anim» (Reihenfolge = Lage auf der Seite).
2. **Leitprogramm** — die eigenen Clips (`"probe": true`) der sichtbaren Leitprogramme, in deren
   Reihenfolge; Spaltenkopf verlinkt das Leitprogramm; je Zeile vorn «LP» auf die Animation des Kapitels
   (`leitprogramme/<name>.html#simN`, die `figure.sim` im selben `section.kap`). Kontrollclips stehen
   mit drin und zeigen auf dieselbe Animation. Bibliotheksclips, die ein Leitprogramm mitbenutzt,
   bleiben in Spalte 1 oder 3.
3. **Weitere Clips** — der Rest, ruhige weisse Zeilen.
Unter 720 px untereinander. Leere Spalte «—».

**Technik in Mathe** (Vorlage): `scripts/clips_bibliothek.py` (Mathe-Modul, baut den Block,
`REIHEN_VORN`) und in `build-clips-einbau.py` nur zwei Zeilen: `import clips_bibliothek; REIHEN = …`
nach `REIHEN` und der Aufruf `clips_bibliothek.block_bibliothek(alle, seiten, sys.modules[__name__])`
statt `block_bibliothek(alle, seiten)` — so bleibt die KERN-Datei auf ihrer Grundlinie (Mathe 83.0 %).
CSS nur im `<style>` von `clips.html`, nicht in `style.css`.

**Nachgezählt im Physik-Repo** (Stand `57fde7e`, nur gelesen):
- `clips.json`: 205 Clips, davon 116 mit `animation` (Spalte 1 wird oft die volle sein), **0 mit
  `werkzeug`** — die Mathe-Regel «TR-Clips dunkel mit Marke TR» ist in Physik vorerst gegenstandslos.
- 97 Drehbücher mit `"probe": true`, alle mit `lektion`. In Leitprogrammen: Kinematik 10, Dynamik 10,
  Energie 12, Statik 12, Hydrostatik 12, Elektrizität 14 (= **70** für Spalte 2), dazu
  `uebungstest-waermelehre` 15. Die übrigen 12 hängen an keinem Leitprogramm und bleiben draussen.
  Die acht älteren Leitprogramme (Rechnen, Vorwissen, Wärme …) benutzen nur Bibliotheksclips — ihre
  Spalte 2 bleibt leer.
- Die sechs neuen Leitprogramme haben `section.kap#kN` und `figure.sim#simN` wie Mathe — die LP-Links
  lassen sich gleich bestimmen.
- **Anpassungen gegenüber Mathe:**
  - `lerngebiete()` liefert in Physik **3-Tupel** `(nr, titel, ids)` ohne Fach (flache Liste
    0, 4, 5, 6, 99) — die Schleife in `clips_bibliothek.block_bibliothek` und die Gliederung nach
    Fach (`h2` Grundlagen-/Schwerpunktfach, `.cl-sp`) entfallen.
  - «Sichtbar» bestimmt Mathe über den Kommentar `<!-- ALTE LEITPROGRAMME`; in Physik heisst die
    Grenze `<h2 id="veraltet">` (drei veraltete Elektrizitäts-LPs). Die Funktion
    `sichtbare_leitprogramme` dort schneiden.
  - Farben: eine Bereichsfarbe, **Bernstein** (`--bernstein`, `--bernstein-hell`, `--bernstein-rand`).
    Mathe: Spalte 1 in `--blau-hell`/`--lila-hell`, Spalte 2 in einem helleren Ton derselben Farbe
    (#eef4fb / #f5f1fb), Spalte 3 weiss mit Nummer in der Bereichsfarbe. In Physik entsprechend
    Bernstein-hell und ein hellerer Bernsteinton; die Animationsclips sind in Physiks `style.css`
    heute so gefärbt, wie Physik es für Animationen vorsieht — prüfen, ob Spalte 1 dort schon passt.
  - `REIHEN_VORN` ist Mathe-Inhalt; Physik braucht eine eigene Liste, falls Reihen einer Seite
    alphabetisch nicht aufbauend stehen (nachsehen: Themenseiten mit mehreren Reihen).

**Offene Frage an den Auftraggeber, vor dem Übertrag:** Gehören die 15 Clips des
`uebungstest-waermelehre` (Prüfungsbogen, sichtbar) in Spalte 2? In Mathe sind die Prüfungsbogen-LPs
ausgeblendet und darum draussen. Ohne `section.kap`/`figure.sim` hätten ihre «LP»-Links kein
Animationsziel (Rückfall: Kapitelanfang bzw. Seite).

**Warum.** Gleiche Bibliothek in beiden Fächern; die Leitprogramm-Clips sind sonst nur im
Leitprogramm auffindbar.
