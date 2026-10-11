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

### 11.10.2026 · HOWTO-simulationen / HOWTO-werkzeuge: Marken wörtlich kopieren (auch in `OFFEN`)

**Was.** Ein Satz in §3: Die SEO- und FUSS-Marken wörtlich aus der Vorlage kopieren, samt «— generiert von
scripts/build-seo.py, nicht von Hand ändern».
**Wo.** Physik `HOWTO-simulationen.md` Z.37 und `HOWTO-werkzeuge.md` Z.39 (beide «leere FUSS-Marken»). Physiks
`build-seo.py` sucht dieselben vollen Marken (`MARKE_AUF` Z.502, `FUSS_AUF` Z.504).
**Warum.** Beim Bau von `simulationen/boxplot.html` (Mathe 84f1a7f) standen nackte Marken in der Seite:
`build-seo.py` setzte einen zweiten SEO-Kopf davor und liess den Footer leer.
