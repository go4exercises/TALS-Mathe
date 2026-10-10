# Bauskripte: Leitprogramm Quadratische Funktionen

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/quadratische-funktionen.html` aus einer Kapitelbeschreibung (Kopf und Grundskript werden aus der bestehenden Seite übernommen) | **ja** — für Änderungen an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Koordinatensysteme, Aufgabenleiste, Simulationen sim1–sim5, Übungen mit Rückmeldung (`TYPEN`), Minigrafen | wird von `seite.py` eingesetzt |
| `kontrollclips.py` | Archiv: hat die fünf Kontrollclips erzeugt | **nein** — die JSONs in `clips/` sind die Quelle |

Fragebild (06.10.2026): `python3 scripts/lp/fragebild.py clips/g3-3-lp-kontrolle-*.json` — idempotent, Regeln in `scripts/lp/fragebild.py`.

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

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/quadratische-funktionen.html 1000
node .claude/tools/pruef-leiste.mjs leitprogramme/quadratische-funktionen.html
node .claude/tools/pruef-fragen.mjs g3-3-lp-kontrolle-scheitelform g3-3-lp-kontrolle-formen
```

`seite.js` setzt dafür die Testhaken `box.__aufgabe` und `box.__typ`; `TYPEN.nullstellen.eingabe(A)`
liefert die richtige Eingabe, wo `A[feld]` nicht reicht (HOWTO-leitprogramme §14).

## Footer

Den Footer schreibt `scripts/build-seo.py` (seit 10.10.2026, eine Version für das ganze Lehrmittel):
`seite.py` gibt nur leere FUSS-Marken aus. **Nach jedem Bau `python3 scripts/build-seo.py`**, sonst fehlt
der Footer (der Pre-Flight meldet es).
