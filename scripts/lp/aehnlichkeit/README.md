# Bauskripte: Leitprogramm Zentrische Streckung und Ähnlichkeit

Leitprogramm zur Themenseite GF 5.2d (`grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html`), gebaut am 08.10.2026
im Kapitelmuster mit dem Geometrie-Arbeitsbereich der Leitprogramme Planimetrie und Trigonometrische Berechnungen
(Auftrag: `AUFTRAG.md`). Kapitel: Zentrische Streckung · Strahlensätze · Ähnliche Figuren (Längen, Flächen, Massstab) ·
Ähnliche Dreiecke (WW, sss, sWs, SsW, Schatten, Höhe im rechtwinkligen Dreieck). RLP 5.2 ohne Vermerk «auch ohne
Hilfsmittel»: Taschenrechner erlaubt. Vorwissen: Leitprogramm Planimetrie; weiter: Trigonometrische Berechnungen (5.3).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/aehnlichkeit.html` (erster Lauf: Gerüst aus `planimetrie.html`, SEO-Block nur `noindex`; danach bleibt der SEO-Block) | **ja**, nach jeder Änderung an `seite.py`, `seite.js`, `seite.css` |
| `seite.css` | eigener Teil des `<style>` (Block aus Trigonometrische Berechnungen, Ergänzungen am Schluss) | wird eingebunden |
| `seite.js` | vier Arbeitsbereiche mit Aufgabenleiste, 9 Übungstypen, Figuren zu den Aufgaben | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/g5-2d-lp-*.json` (Reihe «Ähnlichkeit sehen») | **ja** — rettet die gemessenen `dauer`; Zeiten stehen auf den Wortzeiten der Vertonung |
| `zahlen.py` | rechnet alle Zahlen der Seite, der Clips und des Gesamttests nach | **ja**, muss «alle Zahlen stimmen» melden |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper) nach `wortzeiten.json` — Grundlage für `ein` und `bewegung` in `clips.py` | nach jeder (Teil-)Vertonung |
| `AUFTRAG-behebung.md` | Auftrag zur Behebung der Prüfbefunde (TODO.md, Prüfung 08.10.2026) | — |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/aehnlichkeit/*.tex`, gebaut mit `python3 scripts/build-lp-pdf.py aehnlichkeit`.

## Arbeitsbereich

Wie in `scripts/lp/planimetrie/README.md` (`ziel`/`probe`, `wahl`, `frage`, `fest`, `verdeckt`). Neu in dieser Kopie:
`fenster.achsen` (Achsenkreuz mit Pfeil und Zahlen, Kapitel 1), `ohneNull: ['k']` (Regler springt über 0, bevor gezeichnet
wird), gleiche Meldungen zweier Felder nur einmal, Winkelbögen mit 1–3 Bögen (gleich markierte Winkel), Figuren-Eintrag `g`
(ganze Gerade) und `data-achsen="ja"`.

## Farben — eine Farbe, eine Bedeutung

1 blau = Original, Figur · 2 orange = Bild, Streckfaktor, Hilfslinie · 3 grün = Gesuchtes, Ergebnis · 4 rot = Fehler · 5 Tinte = neutral.

## Prüfen

```sh
python3 scripts/lp/aehnlichkeit/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/aehnlichkeit.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/aehnlichkeit.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/aehnlichkeit.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/aehnlichkeit.html
node .claude/tools/pruef-geo.mjs leitprogramme/aehnlichkeit.html
node .claude/tools/pruef-fragen.mjs g5-2d-lp-kontrolle-streckung g5-2d-lp-kontrolle-strahlensaetze g5-2d-lp-kontrolle-figuren g5-2d-lp-kontrolle-dreiecke
```

## Behebung der Prüfbefunde (08.10.2026)

`clips.py` behält bei geändertem Sprechertext die alte `dauer` (nach Szenenname) und meldet die Szene mit «!» — dann
`build-clip-ton.py <clip> --szenen N`, danach `wortzeiten.py <clip>` und die Zeiten in `clips.py` nachführen. Neu vertont:
streckung «Kleiner», «Negativ»; kontrolle-streckung «Frage 5», Frage 2 r1; strahlensaetze «Nur mit Parallelen»;
kontrolle-strahlensaetze «Frage 3», Frage 3; kontrolle-figuren Frage 1 r0, r2; kontrolle-dreiecke «Frage 1», «Frage 4»,
Fragen 1 und 4, Frage 2 falsch.

## Footer

Den Footer schreibt `scripts/build-seo.py` (seit 10.10.2026, eine Version für das ganze Lehrmittel):
`seite.py` gibt nur leere FUSS-Marken aus. **Nach jedem Bau `python3 scripts/build-seo.py`**, sonst fehlt
der Footer (der Pre-Flight meldet es).
