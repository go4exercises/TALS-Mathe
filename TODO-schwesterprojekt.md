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
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

### 08.10.2026 · `build-clips.py`: dritte Runde Werkzeug (Wünsche aus den LPs GF 5.3–5.5)

**Was.** Neue, abwählbare Felder (HOWTO-clips «Dritte Runde»): `aus` an jedem Element, auch an einem ganzen `graf`;
Figuren `parameter` (Formeln mit `sind`/`cosd`/`tand`, Bewegung über einen Winkel) und `folgt`/`versatz`/`radial`/
`mitte`/`ecke`; `graf.zahlen_neben_kreis`, `graf.ausweichen`; `farbwechsel` an bewegten Kurven, Geraden, Parabeln;
`asymptoten.strich`/`.dicke`; `grad: true` an `trig`-Kurven; `kreis.name`/`.name_abstand`; Klickfragen: `ziel` und
`fallen[].bei` auch als Strecke `[[x1,y1],[x2,y2]]`. **Verhaltensänderung ohne Feld:** Liegt ein Tipp in mehreren
Fallen, gewinnt die nächste statt der ersten (`FRAGEN_JS`).
**Wo.** `graf_svg` (Figurenschleife, Achsenzahlen, `grad`-Umrechnung, Kreisname, `farbwechsel()`), `bauen()`
(Element-`aus`, Zusatz-JS je Marke), neue Konstanten `GRAD_JS`, `KREISNAME_JS`, `FARBWECHSEL_JS`, `AUSWEICHEN_JS`;
`BEWEGUNG_JS` unverändert. Am einfachsten die ganze Datei übernehmen (gleich bis auf die Einstellungen am Anfang
und den Seitennamen); Grundlinie in `abgleich.py` danach nachführen. Dazu HOWTO-clips «Dritte Runde».
**Warum.** In den Mathe-LPs 5.3–5.5 brauchte es Behelfe (dichte Stützpunkte für Kreisbewegung, Name P als Text,
Bogenmass-Kurven mit Grad-Teilung, Farbe statt Strichart, `aus` an jeder Figur).
**Getestet (Mathe).** 543 Clips vorher/nachher gebaut: 485 byte-gleich, 58 mit `fragen` nur im `FRAGEN_JS` verschieden
(alten Code eingesetzt = HEAD). Testclips mit allen Feldern im Bild und per `__seek` vermessen, keine JS-Fehler;
`pruef-fragen` auf 49 Klickfrage-Clips 9/9; nächste Falle in den 4 Mathe-Clips mit überlappenden Fallen alt/neu im
Browser verglichen (neu jeweils die passendere Rückmeldung).
**Physik durchsehen** (gezählt 08.10.2026, nur gelesen): 334 Drehbücher, 102 mit `fragen` — deren HTML ändert sich
nur im `FRAGEN_JS`; 5 Klickfragen, keine mit überlappenden Fallen, also keine geänderte Rückmeldung. Kein neuer
Feldname kommt in Physik-Drehbüchern schon vor; alle übrigen Clips müssen byte-gleich bauen.

### 08.10.2026 · Teilvertonung: `--szenen` in `build-clip-ton.py`, `--fragen` in `build-clip-fragen-ton.py`

**Was.** `scripts/build-clip-ton.py <clip> --szenen 2,5` (Nummern ab 1, wie die Ausgabe zählt) spricht nur diese
Szenen neu und misst ihre `dauer`; die übrigen behalten `dauer` und Ton, ausgeschnitten samt Stille aus der
bisherigen `clips/ton/<clip>.mp3` nach den Dauern im Drehbuch. Kopfraum 0.95 nur für die neuen Stücke (Piper
liefert Spitze 1.0, Faktor also gleich). Abbruch, wenn die Spurlänge um mehr als 0.05 s von der Summe der Dauern
abweicht oder einer nicht genannten Szene `dauer` fehlt. Neu ist `alte_spur()`, alles Übrige hinter `if alt` —
ohne Schalter byte-gleich. `scripts/build-clip-fragen-ton.py --fragen 2,5:r1` (Fragen ab 1, optional ein
Schlüssel) löscht und spricht nur die gewählten Fragetöne.
**Wo.** Physik `scripts/build-clip-ton.py` (KERN, vorher gleich): Mathe-Fassung ganz übernehmen, Grundlinie in
`abgleich.py` wieder 1.000. Physik `scripts/build-clip-fragen-ton.py` (nicht im Abgleich, weicht nur im Docstring
ab): Block `--fragen` übernehmen. Dazu die zwei Absätze in HOWTO-clips (Ton → Bauen; Fragen im Clip → Vorlesen).
**Warum.** Piper klingt bei jedem Lauf anders (gleicher Text 6.86 s gegen 7.28 s); nach einer Textkorrektur
sollen abgenommene Szenen und Fragetöne bleiben. Bisher nur mit Behelfsskripten.
**Getestet.** Ohne Schalter: alte und neue Fassung mit festem Piper-Ersatz (`PIPER_CMD`) auf einer Kopie von
`g5-5-anim-kopplung` — JSON und MP3 byte-gleich. Mit echtem Piper (`--szenen 3`, Satz angehängt): übrige Dauern
gleich, Spur = Summe der Dauern, 0 Samples Versatz, gleicher Pegel, `sprechzeiten.py` ±0.02 s. `--fragen 2,4:r1`:
nur die 4 gewählten Dateien neu, 13 unberührt.
