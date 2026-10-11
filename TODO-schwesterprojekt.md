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
**Abgeräumt am 07.10.2026:** die zwei Einträge vom 06.10.2026 (Leitprogramme-Seite mit Kacheln,
`clips.html` in drei Spalten) — in Physik umgesetzt (Commit `2641b57`; nachgesehen: `scripts/clips_bibliothek.py`,
21 Tabellen in `clips.html`, Kachelzeilen in `leitprogramme.html`).
**Abgeräumt am 08.10.2026:** die zwei Einträge vom 07.10.2026 (`abgleich.py` mit DATEN und Suchtitel der
Leitprogramme; gemeinsamer `build-clips.py`) — in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik, 07.10.2026;
nachgesehen: `TEXTBREITE_BEGRENZEN` in Physiks `build-clips.py`, Ähnlichkeit 99.8 %).
**Abgeräumt am 10.10.2026:** der Eintrag vom 08.10.2026 (`clips_bibliothek.py`, Clipnamen mit Grossbuchstaben) —
in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik; Physiks `abgleich.py` hier übernommen).
**Abgeräumt am 11.10.2026:** der Eintrag «Marken wörtlich kopieren» vom 11.10.2026 — in Physik umgesetzt
(nachgesehen: HOWTO-werkzeuge Z.42, HOWTO-simulationen Z.39; Physiks `abgleich.py` hier übernommen).
**Abgeräumt am 10.10.2026 (zweiter Durchgang):** der Eintrag vom 10.10.2026 (`build-clip-ton.py`, sieben
Aussprache-Einträge) — in Physik umgesetzt (`1aca43e`; nachgesehen: `build-clip-ton.py` deckungsgleich, 12 Clips und
2 Fragen neu vertont, «ppm, parts per million,» in drei Clips).
**Abgeräumt am 08.10.2026 (zweiter Durchgang):** die zwei Einträge vom 08.10.2026 (`build-clips.py` dritte Runde;
Teilvertonung `--szenen`/`--fragen`) — in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik, 08.10.2026;
nachgesehen: `build-clip-ton.py` byte-gleich, `abgleich.py` meldet keine Drift in `build-clips.py`).
**Abgeräumt am 11.10.2026:** die drei Einträge vom 10.10.2026 («Footer aus einer Quelle») und 11.10.2026 (Selbsttest
prüft auch Rückmeldung; kompakte Kacheln) — in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik; nachgesehen:
`VERSION = '2.0'` und `fuss()` in Physiks `build-seo.py`, neun `verify_*.js`, `.lp-pillen` in `werkzeuge.html`,
`simulationen.html` und beiden HOWTOs, keine `.lp-zeile` mehr; Physiks `abgleich.py` hier übernommen).
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 11.10.2026 · Trainer-Rahmen und «Nächster Schritt»

**Wo.** `werkzeuge/trainer.css`, `werkzeuge/trainer.js`, HOWTO-werkzeuge §3 «Trainer-Rahmen».
**Warum.** Die sieben Mathe-Trainer sahen verschieden aus, ihre Karten passten
nicht auf einen Bildschirm (Oberkante 250–480 px, Höhe 470–785 px bei 800 px Fensterhöhe), und die neue Taste
«Nächster Schritt» stand jedes Mal woanders. Jetzt gemeinsam: Karte bis zum unteren Bildschirmrand (Höhe per
`trainer.js`), Kopf mit «Nächster Schritt» oben rechts, Arbeitsfläche, in der sich die Lösung unter der Aufgabe
Schritt für Schritt entwickelt (nur sie scrollt), Bedienleiste unten. Vorbild `werkzeuge/systemtrainer.html`.
**Was.** In Physik nachgezählt (nur gelesen): sechs Werkzeuge in `werkzeuge/` — `einheitentrainer.html` (2588 Zeilen),
`formeln-umstellen.html` (1117), `bewegungsdiagramme.html` (1120), `fall-und-wurf.html` (1509),
`freischneiden.html` (1992), `schaltungen-zusammenfassen.html` (2195); keins hat «Nächster Schritt» oder einen
gemeinsamen Rahmen, Physiks HOWTO-werkzeuge kennt den Rahmen nicht. Übertrag: zuerst HOWTO-werkzeuge §3 angleichen
(Datei ist in beiden Repos gleich gegliedert), dann entscheiden, welche der sechs Trainer sind (Einheitentrainer,
Formeln umstellen sicher; die übrigen eher Rechner/Simulation-nahe) und nur diese umbauen. Leitfarbe Bernstein statt
Blau beachten (`--blau` in `.tr-opt.aktiv`).
