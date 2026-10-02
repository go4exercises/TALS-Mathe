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

### 02.10.2026 · `build-clips.py`: bewegte Parabel im `graf` und Fragen im Clip (Prototyp — erst nach Abnahme portieren)

**Was.** Neuer Schlüssel `bewegung` für `parabeln` im `graf` (Stützpunkte `[t, a, u, v]`,
Begleiter `scheitel`, `nullstellen`, `yachse`, `marken`, `laeufer`) und neues Drehbuchfeld `fragen` (Clip hält an
und fragt, `FRAGEN_JS`; HOWTO-clips «Fragen im Clip»), dazu die Konstante `BEWEGUNG_JS`, die nur in Clips mit Bewegung
`seek(t)` um `bewegen(t)` erweitert, und `data-t0` am Bild-Layer. Beschreibung in Mathe
`HOWTO-clips.md`, «Bewegte Parabel im `graf`».
**Wo in Physik.** `scripts/build-clips.py` hat `graf_svg` mit `parabeln` und denselben
Abspieler (`window.__seek = seek;` je 1 Treffer, nachgezählt 02.10.2026, nur gelesen).
Physik nutzt den `graf` heute in **keinem** seiner 234 Drehbücher — der Übertrag hält das
Werkzeug gleich, er ändert keinen Clip.
**Warum.** Clips sollen Zusammenhänge zeigen statt beschreiben (Auftraggeber,
30.09.2026). `abgleich.py`: `scripts/build-clips.py` fällt dadurch von 83.6 % auf
75.7 % (Grundlinie 84 %) — der Eintrag in `OFFEN` kommt erst, wenn der Prototyp
angenommen ist.

