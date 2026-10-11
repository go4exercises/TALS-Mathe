# Bauskripte: Leitprogramm Lineare Gleichungen

Leitprogramm zur Themenseite GF 2.2a (`grundlagen/g2-2a-lineare-gleichungen.html`), gebaut am 11.10.2026 im
Kapitelmuster (HOWTO-leitprogramme §4). Löst zusammen mit dem Leitprogramm zu 2.2b das gemeinsame Leitprogramm
*Lineare und quadratische Gleichungen* ab; Umformer, Aufgabenleiste und Übungsgerüst stammen von dort
(`scripts/lp/lineare-quadratische-gleichungen/`, README: der Umformer). Fünf Kapitel: Äquivalenzumformungen und
Probe · Klammern und Brüche · Drei Lösungsfälle · Normalform: Tabelle, Graph und Rechnung · Parameterdiskussion.
Alles ohne Taschenrechner.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/lineare-gleichungen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js`, danach `python3 scripts/build-seo.py` |
| `seite.js` | Umformer (Kapitel 1–3), Simulation «Drei Sichten» (Kapitel 4) und «Parameter» (Kapitel 5) mit Aufgabenleiste, 10 Übungstypen, Minigrafen (`data-k`, auch `data-xname`/`data-yname`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g2-2a-lp-*.json` (Reihe «Lineare Gleichungen lösen») | **ja** — rettet die gemessenen `dauer` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips mit faster-whisper → `wortzeiten.json` | nach jeder (Teil-)Vertonung |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/lineare-gleichungen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py /lineare-gleichungen/` (mit Schrägstrichen — ohne trifft der Filter nichts
Fremdes, aber so ist es eindeutig).

## Zeiten im Drehbuch: Anker statt Sekunden

In `clips.py` stehen Einblendungen und Bewegungsstützpunkte als Anker: `'@beidseitig'` (erstes Wort des
Sprechertexts, das so beginnt), `'@Bei#3'` (drittes), `'@also+0.7'` (versetzt), `'@wort>'` (Wortende). `sz()`
ordnet Sprechertext und Whisper-Wörter einander zu (Zahlwörter als Ziffern, «2x» getrennt) und nimmt die
gemessene Zeit; hat Whisper ein Wort anders geschrieben, wird zwischen den Nachbarn interpoliert (die Liste
«interpoliert» am Ende der Ausgabe). Ohne Wortzeiten (neuer Text) wird geschätzt. Darum:

```sh
python3 scripts/lp/lineare-gleichungen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g2-2a-lp-<name>            # oder --szenen 2,5
python3 scripts/lp/lineare-gleichungen/wortzeiten.py <name>
python3 scripts/lp/lineare-gleichungen/clips.py                     # Anker auf den neuen Ton
python3 scripts/build-clip-fragen-ton.py g2-2a-lp-<name>            # nur Kontrollclips
python3 scripts/build-clips.py           g2-2a-lp-<name>
python3 scripts/lp/lineare-gleichungen/seite.py                     # Clipzeiten
```

## Sperrliste der Übungen

Keine Zufallsübung darf eine feste Gleichung des Leitprogramms würfeln (Clips, Umformer, Simulation 4,
Kapitelaufgaben, Vortest, Gesamttest): Liste `SPERRE` in `seite.js`, je Typ ein Schlüssel. Dieselbe Gleichung
\(ax + b = cx + d\) hat in `zweischritt` (\(c = 0\)), `linear-loesen` und `normalform` denselben Schlüssel
`li|a|b|c|d`. **Neue feste Gleichung = Eintrag in `SPERRE`**, danach die Verteilung zählen (4000 Würfe je Typ).

## Farben — eine Farbe, eine Bedeutung

1 blau = Gleichung, linke Seite · 2 orange = Umformung, rechte Seite, Parameter k · 3 grün = Lösungen ·
4 rot = Fehler · 5 Tinte = Differenz links − rechts, Bezugslinien.

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/lineare-gleichungen.html
node .claude/tools/pruef-uebungen.mjs  leitprogramme/lineare-gleichungen.html 1000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/lineare-gleichungen.html 60
node .claude/tools/pruef-leiste.mjs    leitprogramme/lineare-gleichungen.html
node .claude/tools/pruef-umformer.mjs  leitprogramme/lineare-gleichungen.html
node .claude/tools/pruef-fragen.mjs    g2-2a-lp-kontrolle-umformen g2-2a-lp-kontrolle-klammern g2-2a-lp-kontrolle-faelle g2-2a-lp-kontrolle-sichten g2-2a-lp-kontrolle-parameter
node .claude/tools/render-check.mjs    leitprogramme/lineare-gleichungen.html
```

## Footer

Den Footer schreibt `scripts/build-seo.py`; `seite.py` gibt nur leere FUSS-Marken aus. **Nach jedem Bau
`python3 scripts/build-seo.py`**, sonst fehlt der Footer.
