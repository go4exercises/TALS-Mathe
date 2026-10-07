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
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 07.10.2026 · `build-clips.py`: gemeinsamer Bauer mit TEXTBREITE_BEGRENZEN, Korrekturen und Werkzeug-Erweiterungen

**Was.** Im Zweig `bew-gd` (bewegtes Steigungsdreieck an einer bewegten Geraden) eine Bedingung mehr:
`sichtbar = Math.abs(dx) > 1e-9 && innen(xa, ya) && innen(xb, yb);` — vorher stand bei dx = 0 ein leeres
Dreieck mit der Beschriftung «Δx = 0» im Bild, solange es noch nicht wuchs (Mathe: `g3-2-lp-steigungsdreieck`,
fünf Sekunden «Δx = 0», während «Δx grösser als null» gesagt wird).

**Wo in Physik** (nur gelesen): `scripts/build-clips.py` Z. 1127, gleicher Wortlaut wie vorher in Mathe.
**Zweite Stelle, gleicher Anlass (07.10.2026):** Einheitskreis beim Tangens (`bew-kk`, Zweig `if (tg)`):
Liegt P links der y-Achse (2. und 3. Quadrant), lief die Linie vom Mittelpunkt zur Tangente und P hing
daneben. Neu beginnt sie dort bei P (`const vonP = ok && Math.cos(th) < 0;` und `lin('.kk-radius', vonP ? P[0] : cx,
vonP ? P[1] : cy, …)`). Physik: gleiche Zeile Z. 1358.
**Einstellung TEXTBREITE_BEGRENZEN** (Mathe 07.10.2026, beim Übernehmen von Physiks zusammengeführter
Fassung): Physiks Textbreite (Rand 130 px bei zentrierten Zeilen, `width` aus `breite` bei links gesetzten
Elementen) gilt nur, wenn die Konstante am Dateianfang `True` ist. **In Physik `True` setzen** — dann ändert
sich dort nichts. Mathe hat `False`: Mit `True` brachen 62 Textelemente in 56 Mathe-Clips neu um.
Ausserdem nennen zwei Kommentare zu `clipRahmen` jetzt «physiklib.js bzw. mathlib.js».

**Am einfachsten:** `scripts/build-clips.py` aus Mathe übernehmen und drei Werte zurücksetzen —
Seitenname «physik.begreifbar.ch» (zweimal), `KARO_OHNE_ACHSEN = False`, `TEXTBREITE_BEGRENZEN = True`;
das Feld `"werkzeug"` im Index kann bleiben oder raus. Warteschlange `OFFEN`, Quelle Mathe, 07.10.2026.

**Später am 07.10.2026 dazu** (Werkzeug-Erweiterungen, ohne die neuen Felder wirkungslos): `ein`/`aus` an
jedem Teil eines `graf`, `laeufer` an Kurven (bewegt und fest), zwei Nachkommastellen in Live-Beschriftungen
wenn der Wert genau zwei hat (**wirkt auch in Physik auf bestehende Beschriftungen**, z. B. 1.25 statt 1.3 —
dort nach der Übernahme kurz durchsehen), Parabel `normalform` und `achse`, `schnitte` an bewegten Geraden,
`bewegung` an `figuren`, `grenzen` an bewegten Kurven, Tangensstrecke am Rand abgeschnitten. Doku in
Mathes HOWTO-clips.md, Abschnitt «Später einblenden, bewegen, mitlaufen». Auch dafür: Datei übernehmen.
Nachgetragen: `ein`/`aus` an `laeufer` und `dreieck`, Figuren-Bewegung Feld für Feld (ein Fehler, der sie
springen liess), `farbe` umgeschaltet, gleiche Nachbarbilder zusammengefasst, «Δy» links bei Δx < 0.
Zweite Runde: `drehung`/`um` an Figuren, Formelkurven mit `parameter` (der Abspieler zeichnet sie; die
Formel wird über den Python-Syntaxbaum nach JavaScript übersetzt, `formel_js`) samt mitfahrenden `punkte`,
`betrag_von`, `lage` am Läufer und an `marken`, `ein`/`aus` je mitfahrendem Punkt. **Wirkt auch in Physik auf bestehende Clips:** Läufer liegen über festen
Punkten, und Beschriftungen mitfahrender Punkte klappen am Bildrand auf die andere Seite (in Mathe
betraf das keinen bestehenden Clip; in Physik nach der Übernahme kurz durchsehen).
