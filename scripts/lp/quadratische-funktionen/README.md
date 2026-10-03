# Bauskripte: Leitprogramm Quadratische Funktionen

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/quadratische-funktionen.html` aus einer Kapitelbeschreibung (Kopf und Grundskript werden aus der bestehenden Seite übernommen) | **ja** — für Änderungen an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Koordinatensysteme, Aufgabenleiste, Simulationen sim1–sim5, Übungen mit Rückmeldung (`TYPEN`), Minigrafen | wird von `seite.py` eingesetzt |
| `kontrollclips.py` | Archiv: hat die fünf Kontrollclips erzeugt | **nein** — die JSONs in `clips/` sind die Quelle |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/quadratische-funktionen/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/quadratische-funktionen.html
```

Änderungen **nur hier** machen, nicht direkt in der HTML-Datei — sonst überschreibt der
nächste Lauf sie. Ausnahme: der Kopf (`<style>`, SEO-Block), den `seite.py` aus der Seite liest.

Clips ändern: Drehbuch `clips/g3-3-lp-*.json` bearbeiten, dann
`build-clip-ton.py` (wenn sich Sprechertext oder Szenen ändern) → `build-clip-fragen-ton.py`
(Kontrollclips) → `build-clips.py`. Laufzeiten auf den Clip-Karten in `seite.py` nachführen.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/quadratische-funktionen/*.tex`,
bauen mit `python3 scripts/build-lp-pdf.py`.
