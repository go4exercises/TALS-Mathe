# Bauskripte: Leitprogramm Trigonometrische Gleichungen

Leitprogramm zum Teilgebiet GF 5.5 (`g5-5-trigonometrische-gleichungen.html`), gebaut am 07./08.10.2026 im
Kapitelmuster (HOWTO-leitprogramme §4). Eine Kompetenz («elementare trigonometrische Gleichungen am
Einheitskreis visualisieren und mithilfe der Arkusfunktion lösen»), kein Vermerk «ohne Hilfsmittel»; die
besonderen Werte aus GF 5.4 werden trotzdem exakt verlangt. Vier Kapitel: Gleichungen am Einheitskreis ·
Mit der Arkusfunktion: die zweite Lösung · Tangensgleichungen · Alle Lösungen: Periode und Lösungsmenge.
Vorwissen: LP Einheitskreis (GF 5.4). Weiter: Themenseite; im Schwerpunktfach LP Trigonometrische Funktionen.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/trigonometrische-gleichungen.html` (Gerüst beim ersten Lauf aus `einheitskreis.html`) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | vier Simulationen mit Aufgabenleiste, 8 Übungstypen, Kreis- und Kurvenbilder zu den Aufgaben (`svg.ek-mini[data-ek]`, `svg.kv-mini[data-kv]`) | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/g5-5-lp-*.json` (Reihe «Winkel finden») | **ja** — rettet die gemessenen `dauer` |
| `zahlen.py` | rechnet jede Zahl der Seite, der Clips, der Simulationsziele und des Gesamttests nach | vor jedem Bau |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/trigonometrische-gleichungen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py trigonometrische-gleichungen` (Teil A ohne, Teil B mit Taschenrechner).

## Die Simulationen

- **sim1** Kreis und Gerade: `sin φ = c` → Waagrechte, `cos φ = c` → Senkrechte, Schnittpunkte; keine Winkel als Zahl.
- **sim2** Rechner und zweite Lösung: Hauptwert φ₁ (mit Hauptwertbereich als Band), zweiter Kreispunkt hohl, Probepunkt P (Regler in ganzen Grad über die ganze Breite, Toleranz 1° gegen den ungerundeten Zielwinkel — mit Maus und Finger bei 360 und 1280 px jedes Ziel erreichbar, Prüfung 08.10.2026).
- **sim3** Tangens: S(1 | c), Gerade durch O und S, Hauptwert, Gegenpunkt hohl, Probepunkt P.
- **sim4** Kurve von −360° bis 720° mit Regler k: Das Paar φ₁ + k · p, φ₂ + k · p ist gefüllt, alle übrigen Lösungen hohl. Auf dem Handy mindestens 560 px breit und im Rahmen seitlich verschiebbar; der Rahmen folgt den markierten Lösungen (`folgen()`), ein Hinweis steht darunter.

Aufgaben mit fester Gleichung setzen und sperren Wert und Funktion (`s.setze`); beim Wechsel gibt die Leiste alles frei
und setzt Regler und Auswahl auf den Startwert zurück.

## Clips

Kreis-Clips: Der laufende Punkt P ist der `kreis`-Begleiter einer ausgeblendeten Sinus- bzw. Tangenskurve
(`lauf()`), mitlaufende Schnittpunkte über `schnitte` an bewegten Geraden mit den Halbkreisen als Formelkurven.
Kapitel 4: Kurven intern im Bogenmass, Achse in Grad beschriftet; die Klickfrage zeichnet `sin(x*pi/180)` in Grad.
Fragebild über `frage_bild()` in `clips.py` (nur das Gegebene ab 0.05 s, `tippbar`), nicht über
`scripts/lp/fragebild.py`. `kpb()` setzt die Beschriftung eines Kreispunkts frei, wo sie radial mit S zusammenstösst.

## Zeiten auf den Ton

```sh
python3 scripts/lp/trigonometrische-gleichungen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        g5-5-lp-<name>
python3 scripts/build-clip-fragen-ton.py g5-5-lp-<name>   # nur Kontrollclips
python3 .claude/tools/sprechzeiten.py    g5-5-lp-<name>   # danach ein-Zeiten in clips.py auf die Wörter legen
python3 scripts/lp/trigonometrische-gleichungen/clips.py
python3 scripts/build-clips.py           g5-5-lp-<name>
```

Die Wortzeiten (faster-whisper) stehen als Kommentar an den Szenen in `clips.py`.

## Nur einzelne Szenen neu vertonen

`build-clip-ton.py` spricht immer den ganzen Clip neu. Am 08.10.2026 (Behebung der Prüfung) wurden nur die Szenen
mit geändertem Text neu gesprochen, die übrigen aus der alten Tonspur übernommen: Drehbuch und mp3 vorher sichern,
dann für jede Szene mit gleichem Namen und Sprechertext das Stück `[start, start + dauer]` der alten Spur nach dem
alten Szenenplan (`szenen_planen`) kopieren, nur die neuen mit `sprich()` erzeugen und `dauer` messen wie
`build-clip-ton.py`. Fragetöne ebenso: `build-clip-fragen-ton.py` laufen lassen, danach die Dateien unveränderter
Texte (`fragen_texte`) aus der Sicherung zurückholen.

## Farben — eine Farbe, eine Bedeutung

1 blau = Sinus · 2 orange = Tangens · 3 grün = Cosinus · 4 rot = Gegenbeispiel · 5 Tinte = neutral (Kreis,
Gerade y = c bzw. x = c, Tangente). Gleich wie im LP Einheitskreis. Polgeraden des Tangens in den Kurvenbildern der Clips rot (`POLE`, wie «nicht definiert»), damit sie sich von der Waagrechten y = c unterscheiden.

## Prüfen

```sh
python3 scripts/lp/trigonometrische-gleichungen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/trigonometrische-gleichungen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/trigonometrische-gleichungen.html 2000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/trigonometrische-gleichungen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/trigonometrische-gleichungen.html
node .claude/tools/pruef-fragen.mjs g5-5-lp-kontrolle-einheitskreis g5-5-lp-kontrolle-arkus \
     g5-5-lp-kontrolle-tangens g5-5-lp-kontrolle-loesungsmenge
```
