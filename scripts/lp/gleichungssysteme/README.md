# Bauskripte: Leitprogramm Lineare Gleichungssysteme

Leitprogramm zum Teilgebiet GF 2.3 (Themenseite `grundlagen/g2-3-lineare-gleichungssysteme.html`), gebaut am 11.10.2026
im Kapitelmuster (HOWTO-leitprogramme §4). Ersetzt das ältere, klassische Leitprogramm unter derselben Adresse
`leitprogramme/gleichungssysteme.html` (Git-Geschichte). Zwei RLP-Kompetenzen, beide «auch ohne Hilfsmittel»:
K1 lösen (Kapitel 1–5), K2 grafisch veranschaulichen und interpretieren (Kapitel 1 und 4).

Kapitel: Lösung und Schnittpunkt · Einsetzen und Gleichsetzen · Additionsverfahren und Verfahrenswahl ·
Keine oder unendlich viele Lösungen (mit Parameter k) · Drei Variablen. Zeiten: Vorwissen 15 · 40 · 40 · 40 · 45 · 40 ·
Gesamttest 25 = 245 min.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `lgs.py` | Rechenkern ohne Fremdpakete: lineare Terme lesen, Lösung eines Systems, «folgt aus» (Zeilenraum), Normalform-Schlüssel | wird benutzt |
| `umformer.py` | die Aufgaben der System-Umformer (Kapitel 2, 3, 5); prüft jede Zeile gegen ihr System | `python3 …/umformer.py` |
| `zahlen.py` | rechnet jede feste Zahl nach (Clips, Simulationen, Aufgaben, Vortest, Gesamttest, Fehlerbeispiele) und liefert die Sperrliste der Übungen | **vor jedem Bau** |
| `seite.py` | baut die Seite (beim ersten Lauf Gerüst aus `lineare-quadratische-gleichungen.html`, SEO und Fuss aus der alten Seite) | **ja**, nach jeder Änderung |
| `seite.js` | Punkt-Sucher (Kap. 1), System-Umformer (Kap. 2, 3, 5), Lösungsfall-Labor (Kap. 4), zehn Übungstypen, Minigrafen | von `seite.py` eingebunden |
| `clips.py` | zehn Drehbücher `clips/g2-3-lp-*.json`, Reihe «Gleichungssysteme lösen»; rettet gemessene `dauer`, nennt «NEU VERTONEN» | **ja** |
| `wortzeiten.py` | Wortzeiten der vertonten Clips (faster-whisper) → `wortzeiten.json`, damit `ein: "@wort"` auf dem Ton sitzt | nach jeder Vertonung |
| `pruef-lgs-umformer.mjs` | Prüfer der System-Umformer (abgeleitet von `.claude/tools/pruef-umformer.mjs`, der Lösungen als Zahlenmenge tippt — für Paare falsch) | ja |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/gleichungssysteme/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py gleichungssysteme` (immer mit Filter).

## System-Umformer

Wie der Umformer der Gleichungen (`../lineare-quadratische-gleichungen/README.md`), erweitert auf Systeme: Ein Knoten zeigt
ein System (`z` als Liste, «@» trennt die Beschriftung (I), (II) …) oder eine Gleichung; `w` sind Schritte (Ziel `'!…'` Fehler,
`'?…'` erlaubter Umweg), `feld` eine Lücke (zurück einsetzen), `L` die Lösung als Tupel `[x, y]` bzw. `[x, y, z]` oder `[]`.
Eingabe der Lösungsmenge: `{(2 | 3)}`, `(2; 3)`, `{}`; vertauschte Koordinaten haben eine eigene Rückmeldung.
`umformer.py` prüft: jede angezeigte Gleichung folgt aus dem Ausgangssystem, jede als Fehler angebotene Gleichung nicht,
Lösungen und Lücken stimmen. Die Figuren heissen `figure.lgs-umformer` — der geteilte `pruef-umformer` sieht sie bewusst nicht.

## Sperrliste der Übungen

`zahlen.FEST` enthält jedes feste System; `seite.py` schreibt daraus `SPERRE` (Normalform wie `sysSchl()` in `seite.js`:
Gleichungen ganzzahlig, gekürzt, erste Zahl positiv, sortiert; bei 3×3 auch jedes Paar). Dazu einzelne Gleichungen
(`nach-y`) und Parameterfamilien (`param-k`). Neue feste Aufgabe = Eintrag in `FEST`. Verteilung nachzählen
(20 000 Würfe je Typ, 0 Treffer am 11.10.2026).

## Farben

blau = Gleichung (I) · orange = Gleichung (II) · grün = Lösung, Schnittpunkt · rot = Fehler · neutral = Umformungsschritte,
Parameter k, Punkt P. Gleich in Clips (`\fa`, `\fb`, `\fc`, `\fd`).

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/gleichungssysteme/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g2-3-lp-<name> [--szenen 2,5]
python3 scripts/build-clip-fragen-ton.py g2-3-lp-<name>   # nur Kontrollclips
python3 scripts/lp/gleichungssysteme/wortzeiten.py <name>
python3 scripts/lp/gleichungssysteme/clips.py            # «@wort» auf die gemessenen Zeiten
python3 scripts/build-clips.py           g2-3-lp-<name>
python3 scripts/lp/gleichungssysteme/seite.py            # Clipzeiten auf der Seite
```

Whisper schreibt Zahlwörter als Ziffern; `passt()` vergleicht sie darum mit `ZAHLWORT`. Wo Whisper abbricht, steht die Zeit fest
im Skript (Kommentar dabei).

## Prüfen

```sh
python3 scripts/lp/gleichungssysteme/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/gleichungssysteme.html
node scripts/lp/gleichungssysteme/pruef-lgs-umformer.mjs leitprogramme/gleichungssysteme.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/gleichungssysteme.html 1000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/gleichungssysteme.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/gleichungssysteme.html
node .claude/tools/pruef-fragen.mjs g2-3-lp-kontrolle-schnittpunkt g2-3-lp-kontrolle-einsetzen g2-3-lp-kontrolle-addition g2-3-lp-kontrolle-faelle g2-3-lp-kontrolle-drei
```

## Footer

Den Footer schreibt `scripts/build-seo.py`. `seite.py` übernimmt den bestehenden FUSS-Block der Seite; nach dem Bau
`python3 scripts/build-seo.py` (beim Freischalten).
