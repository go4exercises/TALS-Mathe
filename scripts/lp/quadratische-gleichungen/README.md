# Bauskripte: Leitprogramm Quadratische Gleichungen

Leitprogramm zur Themenseite GF 2.2b Quadratische Gleichungen (`grundlagen/g2-2b-quadratische-gleichungen.html`),
gebaut am 11.10.2026 im Kapitelmuster mit dem Umformer (HOWTO-leitprogramme §8d). Auftrag: `AUFTRAG.md`.
Löst zusammen mit dem Leitprogramm *Lineare Gleichungen* (2.2a) das gemeinsame Leitprogramm *Lineare und quadratische
Gleichungen* ab (dessen Bauskripte unter `scripts/lp/lineare-quadratische-gleichungen/` das Ausgangsmaterial waren) und
ersetzt unter derselben Adresse das ältere Leitprogramm *Quadratische Gleichungen* (Git-Geschichte).

Kapitel: Erkennen und Wurzel ziehen · Ausklammern und faktorisieren · Quadratisch ergänzen und Mitternachtsformel ·
Das passende Verfahren · Parameterdiskussion. Alles ohne Taschenrechner (RLP 2.2 «auch ohne Hilfsmittel»).
Nicht hier (nur Themenseite): Bruchgleichungen, Substitution, quadratische Ungleichungen.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/quadratische-gleichungen.html` (erster Lauf: Gerüst aus `lineare-quadratische-gleichungen.html`, SEO-Block und Footer aus der alten Zieldatei; danach alles aus der eigenen Seite; Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` und nach einer Neuvertonung |
| `seite.js` | Umformer (Kapitel 1–4), Parameter-Simulation mit drei Familien und Fenster je Familie (Kapitel 5), 15 Übungstypen, Minigrafen | wird eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/g2-2b-lp-*.json` (Reihe «Quadratische Gleichungen lösen») | **ja** — rettet die gemessenen `dauer` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper) → `wortzeiten.json` | nach einer Neuvertonung |
| `zahlen.py` | rechnet alle festen Zahlen nach (Clips, Umformer, Aufgaben, Vortest, Gesamttest, Fehlerwerte im Raster), prüft doppelte Gleichungen und die Sperrliste | **ja**, muss «ALLE ZAHLEN STIMMEN» melden; `--schreiben` schreibt `FESTE_Q` in `seite.js` neu |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/quadratische-gleichungen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py leitprogramme/quadratische-gleichungen/` — **mit diesem Filter**: `quadratische-gleichungen`
allein träfe auch `lineare-quadratische-gleichungen`.

## Zeiten im Clip: Anker statt Sekunden

In `clips.py` darf jedes `ein`, `aus` und jeder Stützpunkt einer `bewegung` ein Anker sein: `'~Wort'`, `'~zwei Wörter'`,
`'~Wort+0.6'`, `'~Wort#2'` (zweites Vorkommen). Vor der Vertonung wird er aus der Lage im Sprechertext geschätzt; nach der
Vertonung richtet `clips.py` den Sprechertext gegen die Whisper-Wörter aus (`wortzeiten.json`; Whisper schreibt Ziffern
und klebt Wörter zusammen, darum eine Ausrichtung statt Suche) und legt den Anker auf das gesprochene Wort.

```sh
python3 scripts/lp/quadratische-gleichungen/clips.py                 # Drehbücher (Anker geschätzt)
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g2-2b-lp-<name>             # einzelne Szene: --szenen n
python3 scripts/build-clip-fragen-ton.py g2-2b-lp-kontrolle-<name>   # nur Kontrollclips
python3 scripts/lp/quadratische-gleichungen/wortzeiten.py <name>
python3 scripts/lp/quadratische-gleichungen/clips.py                 # Anker jetzt auf den Wörtern, dauer bleibt
python3 scripts/build-clips.py           g2-2b-lp-<name>
python3 scripts/lp/quadratische-gleichungen/seite.py
```

Wer den Text einer Szene ändert: `clips.py` behält die alte `dauer` (sonst kann `--szenen` die übrigen Szenen nicht aus der
Spur schneiden) und meldet «hat neuen Text — build-clip-ton.py … --szenen n». Genau diese Szene neu vertonen, dann
`wortzeiten.py <name>`, `clips.py`, `build-clips.py`. Nachgeprüft 12.10.2026 (§15-Befunde behoben, sieben Szenen neu vertont).

## Umformer und Sperrliste

Knoten wie im Vorgänger (`scripts/lp/lineare-quadratische-gleichungen/README.md`): `w` (Knöpfe; `'!'` Fehler, `'?'`
gültiger Umweg), `feld` (Lücke; `zweiklammer(p, q, nach)` prüft Summe und Produkt, `ergaenzFeld` die Ergänzung), `L`
(Lösungsmenge). Keine Zufallsübung würfelt eine feste Gleichung: `FESTE_Q` (alle festen quadratischen Gleichungen als
gekürzte Normalform, aus `zahlen.py`) und `SPERRE` (Typschlüssel der Parameter-Typen). Nach einer neuen festen Gleichung:
in `zahlen.py` eintragen, `zahlen.py --schreiben`, `seite.py`, und die Verteilung zählen (20 000 Würfe je Typ, keine Treffer,
kein Fall darf verschwinden — Stand 11.10.2026: 0 Treffer, Wurzelziehen in «Verfahren» rund 39 %).

## Farben — eine Farbe, eine Bedeutung

1 blau = Gleichung, Parabel · 2 orange = Umformung, Parameter, rechte Seite im Graph · 3 grün = Lösungen, Ergänzung ·
4 rot = Fehler, verlorene Lösung · 5 Tinte = neutral.

## Prüfen

```sh
python3 scripts/lp/quadratische-gleichungen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/quadratische-gleichungen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/quadratische-gleichungen.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/quadratische-gleichungen.html 60
node .claude/tools/pruef-umformer.mjs leitprogramme/quadratische-gleichungen.html
node .claude/tools/pruef-leiste.mjs leitprogramme/quadratische-gleichungen.html
node .claude/tools/pruef-fragen.mjs g2-2b-lp-kontrolle-wurzel g2-2b-lp-kontrolle-faktorisieren g2-2b-lp-kontrolle-formel g2-2b-lp-kontrolle-verfahren g2-2b-lp-kontrolle-parameter
```

## Footer

Den Footer schreibt `scripts/build-seo.py`; `seite.py` übernimmt den Block zwischen den FUSS-Marken unverändert aus der
Seite. Nach der Freischaltung (neuer Eintrag in `SEITEN`) `python3 scripts/build-seo.py`.
