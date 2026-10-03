# Bauskripte: Leitprogramm Potenz- und Wurzelfunktionen

Deckt **beide** Themenseiten des Teilgebiets SP 3.2 ab — `s3-2a-potenzfunktionen.html`
und `s3-2b-wurzelfunktionen.html`. Die einzige RLP-Kompetenz des Teilgebiets («die
Wurzelfunktionen als Umkehrfunktion der Potenzfunktion …») hat ihren Kern auf 3.2b,
darum ist es ein Leitprogramm und nicht zwei.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `clips.py` | erzeugt die zehn Drehbücher `clips/s3-2-lp-*.json` | **ja** — es rettet beim Neulauf die gemessenen `dauer` (Szenenname + Sprechertext gleich) |
| `pruef-graf.py` | rechnet die Koordinatenbilder nach: Kurven im Fenster, keine Beschriftung auf Kurve, Punkt, Achsenmarke oder anderer Beschriftung | vor jedem Clip-Bau, wenn ein `graf` geändert wurde |
| `../grafgeom.py` | die Geometrie dahinter (Pixelmasse aus `build-clips.py`), geteilt mit dem Leitprogramm Lineare Funktionen | wird eingebunden |

## Farben — eine Farbe, eine Bedeutung

1 blau = Potenzkurve und ihr Faktor @a@ · 2 orange = der Exponent @n@ · 3 grün =
Wurzelkurve, Umkehrfunktion, Startpunkt · 4 rot = Gegenbeispiel, Polstelle, verbotener
Bereich · 5 Tinte = neutral (gemeinsame Punkte, Asymptoten, Bezugskurve, Spiegelachse).
Abgeleitet von den beiden Themenseiten, wo der Exponent orange gesetzt ist.

## Bewegte Kurven

`kurve([[t, a, p, u, v], …])` für \(y = a\,(x-u)^p + v\) — eine Schreibweise für
Parabeln n-ter Ordnung, Hyperbeln (\(p \lt 0\)) und Wurzelkurven (\(p = 1/n\)).
Begleiter: `startpunkt`, `asymptoten`, `marken`, `spiegel` (die Kurve an \(y = x\)
gespiegelt, also die Umkehrfunktion) und `von`/`bis`, die sie auf ein Stück
einschränken — ohne das ist \(y = x^2\) nicht umkehrbar. `stufen=True` rundet \(p\)
beim Überblenden auf ganze Zahlen; sonst löschte ein gebrochener Exponent mitten in
der Bewegung den linken Ast.

**Ungerade Wurzeln aus negativen Zahlen** rechnet `BEWEGUNG_JS` seit dem 03.10.2026
richtig (`Math.pow(-8, 1/3)` ist `NaN`, \(\sqrt[3]{-8}\) ist \(-2\)); `pruef-graf.py`
kennt dieselbe Regel. Darum zeigt \(\sqrt[3]{x}\) seinen linken Ast.

**Startpunkt nur bei geradem Wurzelexponenten.** Eine ungerade Wurzel läuft links
weiter und hat keinen — das Verschiebe-Beispiel in Kapitel 5 ist deshalb
\(y = 2\sqrt{x+1} - 4\) und nicht die dritte Wurzel.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/potenz-wurzelfunktionen/clips.py
python3 scripts/lp/potenz-wurzelfunktionen/pruef-graf.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        s3-2-lp-<name>   # wenn Sprechertext oder Szenen ändern
python3 scripts/build-clip-fragen-ton.py s3-2-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           s3-2-lp-<name>
```

## Prüfen

```sh
node .claude/tools/pruef-fragen.mjs s3-2-lp-kontrolle-exponent s3-2-lp-kontrolle-hyperbel \
     s3-2-lp-kontrolle-verschieben s3-2-lp-kontrolle-umkehren s3-2-lp-kontrolle-wurzel
SP=<ablage> node .claude/tools/pruef-clip.mjs clips/s3-2-lp-<name>.html <sekunden…>
python3 .claude/tools/sprechzeiten.py s3-2-lp-<name>
```

Die Bilder **ansehen**: Der Prüfer meldet Überlappung, nicht Gestaltung. Zwei Fehler,
die er nicht sieht und die hier beide vorkamen: zwei Formeln mit demselben `y`
(`f(text, y, groesse)` — die dritte Zahl ist die Schriftgrösse, nicht die zweite
Zeile), und eine `ger(…)` in der Liste `kurven` statt in `geraden`.
