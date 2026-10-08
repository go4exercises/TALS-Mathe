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
**Abgeräumt am 08.10.2026 (zweiter Durchgang):** die zwei Einträge vom 08.10.2026 (`build-clips.py` dritte Runde;
Teilvertonung `--szenen`/`--fragen`) — in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik, 08.10.2026;
nachgesehen: `build-clip-ton.py` byte-gleich, `abgleich.py` meldet keine Drift in `build-clips.py`).
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 08.10.2026 · `clips_bibliothek.py`: Clipnamen mit Grossbuchstaben

**Was.** Die Muster `clips/([a-z0-9-]+)\.html` übersehen Clips mit Grossbuchstaben im Namen; in Mathe fehlten so
die 12 Clips `g2-M-lp-*` des Leitprogramms Modellieren in `clips.html`. Mathe: `[A-Za-z0-9-]` (Zeilen 67, 69).
**Wo.** Physik `scripts/clips_bibliothek.py` Zeilen 90, 94, 112 (FACH-Datei, nicht im Abgleich).
**Warum.** Physik hat heute keinen Drehbuchnamen mit Grossbuchstaben (gezählt 08.10.2026: 0) — der Fehler ist dort
still, trifft aber den ersten solchen Clip. **Getestet (Mathe).** `build-clips-einbau.py --schreiben`: 12 neue
Einträge, übrige Bibliothek unverändert.
