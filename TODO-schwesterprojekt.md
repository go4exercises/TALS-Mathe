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
**Abgeräumt am 08.10.2026 (zweiter Durchgang):** die zwei Einträge vom 08.10.2026 (`build-clips.py` dritte Runde;
Teilvertonung `--szenen`/`--fragen`) — in Physik umgesetzt (Eintrag in `OFFEN`, Quelle Physik, 08.10.2026;
nachgesehen: `build-clip-ton.py` byte-gleich, `abgleich.py` meldet keine Drift in `build-clips.py`).
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 10.10.2026 · `build-clip-ton.py`: Aussprache nach Hörprobe (auch in `OFFEN`)

**Was.** Sieben Einträge in `AUSSPRACHE` (Block «Nach Hoerprobe 10.10.2026»): amontons `amɔ̃tˈɔ̃`,
isochor `iːzoːxˈoːɐ`, glycerin `ɡlytsəʁˈiːn`, stimulierte `ʃtiːmuːlˈiːɐtə`, kacheln/kachel `kˈaxːəln`,
parts per million; dazu der Kommentar mit den als «wie bisher» entschiedenen Wörtern.
**Wo.** Physik `scripts/build-clip-ton.py` (KERN, Grundlinie 1.000: Mathes Datei übernehmen). Betroffen in Physik
(gezählt 10.10.2026, `aussprache(text) != text`): Amontons in p5-3-anim-gasgesetze, p5-3-gas-isochor,
p5-3-lp-spezialfaelle; isochor in p5-3-gas-gleichung, p5-3-gas-isochor, p5-3-lp-kontrolle-spezialfaelle,
p5-3-lp-spezialfaelle, uebungstest-b2-kuehlschrank; Glycerin in p5-1-lp-aggregat; stimulierte in
p6-1-lp-kontrolle-licht, p6-1-lp-licht — 10 Clips, nur die Szenen/Fragen mit dem Wort neu vertonen.
Sprechertext: «ppm» bei der ersten Nennung je Clip als «ppm, parts per million,» (6 Stellen in 3 Clips, u. a.
p5-2-anim-treibhaus). **Warum.** Entscheide des Auftraggebers nach Hörprobe in drei Runden
(`~/hoerproben/2026-10-10`); die Tabelle gilt für beide Repos.

