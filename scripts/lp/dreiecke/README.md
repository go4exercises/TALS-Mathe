# Bauskripte: Leitprogramm Dreiecke

Leitprogramm zur Themenseite GF 5.2a Dreiecke (`grundlagen/g5-2a-dreiecke.html`), gebaut am 08.10.2026 im Kapitelmuster
mit dem Geometrie-Arbeitsbereich der Leitprogramme Planimetrie und Trigonometrische Berechnungen. Auftrag: `AUFTRAG.md`.
Kapitel: Winkel im Dreieck · Höhen, Halbierende, Mittelsenkrechte · Fläche und Umfang · Rechtwinklige Dreiecke und
Pythagoras. RLP 5.2 trägt keinen Vermerk «ohne Hilfsmittel»: Taschenrechner erlaubt. Vorwissen: GF 5.1 (Clip
`g5-1-winkelarten`); weiter: Leitprogramm Vierecke (5.2b).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/dreiecke.html` (erster Lauf: Gerüst aus `trigonometrische-berechnungen.html`, SEO-Block nur `noindex`; danach bleibt ein vorhandener SEO-Block unangetastet) | **ja**, nach jeder Änderung an `seite.py`, `seite.js`, `seite.css` oder nach einer Neuvertonung (Clipzeiten) |
| `seite.css` | eigener Teil des `<style>` (Block aus Trig. Berechnungen, Ergänzungen am Schluss) | wird eingebunden |
| `seite.js` | vier Arbeitsbereiche mit Aufgabenleiste, neun Übungstypen, Figuren zu den Aufgaben | wird eingebunden |
| `geom.py` | Geometrie-Helfer (Lot, Schnittpunkte H, S, M_I, M_U, dritte Ecke aus zwei Winkeln) | von `clips.py`, `seite.py`, `zahlen.py` benutzt |
| `clips.py` | erzeugt die acht Drehbücher `clips/g5-2a-lp-*.json` (Reihe «Dreiecke sehen») | **ja** — rettet die gemessenen `dauer` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper) → `wortzeiten.json` | nach einer Neuvertonung |
| `zahlen.py` | rechnet alle Zahlen nach (Seite, Clips, Kontrollfragen, Gesamttest samt Fehlerfällen, Klickflächen) | **ja**, muss «ALLE ZAHLEN STIMMEN» melden |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/dreiecke/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py leitprogramme/dreiecke/` (der Pfad als Filter, damit kein fremdes PDF neu entsteht).

## Arbeitsbereiche

Wie in `scripts/lp/planimetrie/README.md` (`arbeitsbereich('simN', …)`, Aufgaben mit `ziel`/`probe`, `wahl`, `frage`, dazu
`fest` und `verdeckt` aus Trig. Berechnungen). Eigenheiten:
- **sim1** stellt α und β ein (Schritt 5°); das Dreieck entsteht über AB und wird ins Bild eingepasst (die Grösse spielt für
  Winkel keine Rolle). α + β ≥ 180° zeigt die nicht schneidenden Schenkel. `aussen: true` zeichnet den Aussenwinkel bei C.
- **sim2** zieht C mit zwei Reglern; `zeige: 'h' | 's' | 'w' | 'm'` zeichnet die drei Linien einer Familie mit ihrem
  Schnittpunkt (bei `w`/`m` mit In-/Umkreis); die Zeile nennt die Lage von H bzw. M_U, auch ausserhalb des Bildes.
- **sim3** wie Planimetrie Kapitel 2 (Spitze parallel zur Grundseite), mit g = 6 cm, h = 4 cm; `ha: true` macht BC zur Grundseite.
- **sim4** Katheten a und b; `dreh` dreht um die Bildmitte, `form: 'gs' | 'gls'` zeigt ein gleichschenkliges bzw. gleichseitiges Dreieck.

## Farben — eine Farbe, eine Bedeutung

1 blau = Figur · 2 orange = Element, Hilfslinie · 3 grün = Gesuchtes, Ergebnis, Schnittpunkt · 4 rot = Fehler · 5 Tinte =
neutral. In Kapitel 1 tragen die drei Winkel je eine Farbe (α orange, β grün, γ Tinte), damit man α und β im Beweis der
Winkelsumme an der Parallelen wiederfindet; dort steht kein Ergebnis grün.

## Prüfen

```sh
python3 scripts/lp/dreiecke/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/dreiecke.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/dreiecke.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/dreiecke.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/dreiecke.html
node .claude/tools/pruef-geo.mjs leitprogramme/dreiecke.html
node .claude/tools/pruef-fragen.mjs g5-2a-lp-kontrolle-winkel g5-2a-lp-kontrolle-elemente g5-2a-lp-kontrolle-flaeche g5-2a-lp-kontrolle-pythagoras
```
