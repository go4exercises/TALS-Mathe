# Bauskripte: Leitprogramm Polynomfunktionen

Leitprogramm zum Teilgebiet SP 3.3 (`schwerpunkt/s3-3-polynomfunktionen.html`), alle drei
RLP-Kompetenzen. Fünf Kapitel: Linearfaktoren · mehrfache Nullstellen · Globalverlauf ·
Nullstellen berechnen · Hoch- und Tiefpunkte.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/polynomfunktionen.html` (Gerüst aus der bestehenden Seite, Inhalt hier, Clipzeiten aus den Drehbüchern) | **ja**, nach jeder Änderung an `seite.py` oder `seite.js` |
| `seite.js` | Simulationen mit Aufgabenleiste, 15 Übungstypen, Minigrafen | wird von `seite.py` eingebunden |
| `clips.py` | erzeugt die zehn Drehbücher `clips/s3-3-lp-*.json` | **ja** — es rettet beim Neulauf die gemessenen `dauer` (Szenenname + Sprechertext gleich) |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/polynomfunktionen/*.tex`,
gebaut mit `python3 scripts/build-lp-pdf.py polynomfunktionen`.

## Farben — eine Farbe, eine Bedeutung

1 blau = die Kurve und ihr Leitkoeffizient @a@ · 2 orange = Nullstellen und Linearfaktoren ·
3 grün = Hoch- und Tiefpunkte · 4 rot = Gegenbeispiel · 5 Tinte = neutral (Leitterm,
Bezugskurve, Läufer, y-Achsenabschnitt). Abweichung von der Themenseite: Deren
Linearfaktor-Baukasten gibt jeder Nullstelle eine eigene Reglerfarbe; hier sind alle orange.

## Bewegte Polynome

`poly([[t, a, x1, x2, …], …])` für \(y = a\,(x-x_1)(x-x_2)\cdots\) — neu im Clip-Bauer seit
dem 04.10.2026 (`"polynom": true`, HOWTO-clips.md). Legt man zwei Nullstellen aufeinander,
entsteht die doppelte Nullstelle von selbst. Begleiter `nullstellen` (Beschriftungen
abwechselnd über und unter der x-Achse) und `extrema` (H und T, numerisch).
Wo ein Polynom keine reellen Linearfaktoren hat, steht `fest('x**2+1')`.

## Ablauf bei einer Änderung am Clip

```sh
python3 scripts/lp/polynomfunktionen/clips.py
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py        s3-3-lp-<name>   # wenn Sprechertext oder Szenen ändern
python3 scripts/build-clip-fragen-ton.py s3-3-lp-<name>   # nur Kontrollclips
python3 scripts/build-clips.py           s3-3-lp-<name>
python3 scripts/lp/polynomfunktionen/seite.py            # Clipzeiten auf der Seite nachführen
```

Bewegungen auf den Ton legen: `python3 .claude/tools/sprechzeiten.py s3-3-lp-<name>`.

## Prüfen

```sh
python3 .claude/skills/preflight/preflight.py leitprogramme/polynomfunktionen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/polynomfunktionen.html 1000
node .claude/tools/pruef-leiste.mjs leitprogramme/polynomfunktionen.html
node .claude/tools/pruef-fragen.mjs s3-3-lp-kontrolle-linearfaktoren s3-3-lp-kontrolle-vielfachheit \
     s3-3-lp-kontrolle-globalverlauf s3-3-lp-kontrolle-nullstellen s3-3-lp-kontrolle-extrema
SP=<ablage> node .claude/tools/pruef-clip.mjs clips/s3-3-lp-<name>.html <sekunden…>
```

Die Clip-Bilder **ansehen**. Und eine neue Bewegung über `window.__seek(t)` im
`?render`-Modus an mehreren Zeitpunkten abtasten (HOWTO-leitprogramme §15).

## Footer

Den Footer schreibt `scripts/build-seo.py` (seit 10.10.2026, eine Version für das ganze Lehrmittel):
`seite.py` gibt nur leere FUSS-Marken aus. **Nach jedem Bau `python3 scripts/build-seo.py`**, sonst fehlt
der Footer (der Pre-Flight meldet es).
