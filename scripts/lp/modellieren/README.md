# Bauskripte: Leitprogramm Textaufgaben modellieren

Leitprogramm zur Themenseite 2.M (`grundlagen/g2-modellieren.html`, RLP GF 2.1 und 2.3), gebaut am 08.10.2026 im
Kapitelmuster (HOWTO-leitprogramme §4) nach dem Auftrag in `AUFTRAG.md`. Vier Kapitel, je eine Aufgabenart der
Themenseite: Zahlen- und Ziffernrätsel · Mischen · Verteilen · Zins. Je Kapitel ein Einführungsclip mit der
Grundgleichung der Aufgabenart, eine Simulation mit Aufgabenleiste und **zwei Kontrollclips**: «eine Unbekannte»
(lineare und quadratische Gleichung) und «zwei Unbekannte» (lineares und quadratisches System). Jede der 16
Aufgaben läuft in fünf Schritten — Deklaration → Ansatz → Grundform → Lösen → Antwort —, an jedem Schritt eine
Kontrollfrage. Gelöst wird mit dem TI-30X Pro (poly-solv, sys-solv); die linearen Systeme der Kapitelaufgaben
1a–4a und die Teile A und B des Gesamttests ohne Rechner (RLP 2.3, «auch ohne Hilfsmittel»).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `zahlen.py` | rechnet jede Zahl nach: 16 Clip-Aufgaben samt falschen Angeboten, Einführungen, Leistenziele, Vortest, Kapitelaufgaben, Gesamttest und Fehlerbeispiele des Rasters | vor jedem Bau |
| `clips_basis.py` | Bausteine und Layout der Clips, Zahlwörter, Zeiten auf den Ton (`ein: "@wort"`), Kontrollclip-Gerüst | wird von `clips.py` benutzt |
| `clips.py` | erzeugt die zwölf Drehbücher `clips/g2-M-lp-*.json` (Reihe «Ansatz finden») | **ja** — rettet die gemessenen `dauer` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper) → `wortzeiten.json` | nach jeder Vertonung |
| `seite.py` | baut `leitprogramme/modellieren.html` (Gerüst beim ersten Lauf aus `trigonometrische-gleichungen.html`) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | vier Simulationen mit Aufgabenleiste, Bilder zu den Aufgaben (`svg.mo-bild[data-bild]`), neun Übungstypen | wird von `seite.py` eingebunden |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/modellieren/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py modellieren` (**Filter `modellieren`** — ein Filter wie `gesamttest` baut die PDFs aller
Leitprogramme neu).

## Kontrollclips

Layout (1920 × 1080): Kopfzeile mit dem Fahrplan der fünf Schritte, rechts oben der Aufgabentext, links oben das
Gegebene aus den früheren Schritten (über dem Fragekasten des Abspielers, der links unten ab y = 560 steht), rechts
unten die Auflösung. Beim Erscheinen der Frage (0.3 s) steht nur das Gegebene da; die Auflösung kommt mit dem Wort,
das sie nennt. Angebote, die länger als 18 Zeichen sind, stehen als **A, B, C im Bild** (mit Formelsatz, `abc()`),
die Knöpfe heissen nur A, B, C — sonst ragte der Fragekasten mit Rückmeldung über die Bühne (gemessen). Kopf der Frage:
«Schritt ② Ansatz» usw. (`kopf`).

Rechneranzeigen wie in `g2-2b-ti30x-poly-solv` und `g2-3-ti30x-sys-solv`, belegt in der TI-Online-Hilfe
«Gleichungslöser» (`mt_solvers.HTML`, Bildschirmfotos 11–26): poly-solv fragt a, b, c je auf einem Schirm, zeigt x1 und
x2 je auf einem Schirm, exakt als Bruch; sys-solv-Maske `(a)x+(b)y=c`, Zeichen vor dem y-Glied mit + oder −, negative
Zahl mit (−); die Umschalttaste (↔, in der Hilfe `r`) zeigt Brüche als Dezimalzahl (Bild 22 → 23: y = 3/25 → 0.12).
Reihenfolge x1, x2: x1 mit +√D (beide belegten Beispiele). Höchstens 16 Zeichen je Zeile (`zeile()` prüft).

## Farben — eine Farbe, eine Bedeutung

1 blau = erste Unbekannte und ihre Sorte · 2 orange = zweite Unbekannte und ihre Sorte · 3 grün = Ergebnis,
Mischung, Lösung · 4 rot = Fehler, verworfene Lösung · 5 Tinte = neutral. Gleich auf der Seite (`tx-blau`, `.fl.blau` …).

## Sperrliste der Übungen

`SPERRE` in `seite.js`, ein Schlüssel je Typ (`zf|Zahl`, `fo|…`, `st|…`, `vd|…`, `wb|…`, `rh|…`, `fk|…`, `zz|…`). Neue feste
Aufgabe = neuer Eintrag. Zwei Würfelräume sind bewusst eingeschränkt, weil sonst zwei Fehlermuster dieselbe Zahl
gäben: `faktor` würfelt nicht 1 Monat, `zinseszins` nicht E = K.

## Zeiten auf den Ton

```sh
python3 scripts/lp/modellieren/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g2-M-lp-<name>
python3 scripts/build-clip-fragen-ton.py g2-M-lp-<name>   # nur Kontrollclips
python3 scripts/lp/modellieren/wortzeiten.py <name>       # Wortzeiten → wortzeiten.json
python3 scripts/lp/modellieren/clips.py                   # «@wort» auf die gemessenen Zeiten
python3 scripts/build-clips.py           g2-M-lp-<name>
python3 scripts/lp/modellieren/seite.py                   # Clipzeiten auf der Seite
```

Einzelne Szenen neu: `build-clip-ton.py --szenen`, Fragen `build-clip-fragen-ton.py --fragen` (HOWTO-clips).

## Prüfen

```sh
python3 scripts/lp/modellieren/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/modellieren.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/modellieren.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/modellieren.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/modellieren.html
node .claude/tools/pruef-fragen.mjs g2-M-lp-kontrolle-zahlen-1 g2-M-lp-kontrolle-zahlen-2   # usw., in Stapeln
```
