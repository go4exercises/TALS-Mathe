# TODO — Leitprogramm Quadratische Funktionen (Stand 02.10.2026)

Legende: `[x]` erledigt · `[–]` bewusst nicht geändert (Grund dahinter) · `[ ]` offen.
Prio: **HOCH** = Lernende lernen Falsches · **MITTEL** = irreführend, widersprüchlich oder
unvollständig · **NIEDRIG** = Kleinigkeit/Konvention.

Seite: `leitprogramme/quadratische-funktionen.html`, gebaut aus
`_intern/lp-quadratische-funktionen/seite.py` + `seite.js` (Änderungen dort, nicht in der HTML-Datei).
Ein erledigter Punkt wird abgehakt; ist die Liste leer, wird die Datei gelöscht (steht in der Git-Geschichte).

---

## Prüfung auf fachliche und didaktische Richtigkeit (02.10.2026)

Geprüft werden die Seite (Vorwissen, 5 Kapitel, Aufgaben, Übungen mit Rückmeldung,
Logik der Animationen), die 11 Clips (10 eigene + `g1-3-binome-erkennen`) sowie
`gesamttest.pdf` und `bewertungspaket.pdf`. Alle Zahlen werden mit `python3` nachgerechnet.

- [ ] Befunde eintragen — Prüfung läuft.

---

## Abnahme durch den Auftraggeber

- [ ] **Hörprobe** der 10 Leitprogramm-Clips: Aussprache von «x s», «y s», «x plus eins in
  Klammern», «null Komma fünf», «D», «Symmetrieachse»; in den 5 Kontrollclips je eine Frage
  absichtlich falsch beantworten, damit auch die Rückmeldungen zu hören sind. Fundstellen
  (Clip, Sekunde) melden → Sprechertext bzw. Aussprachetabelle anpassen, neu vertonen.
- [ ] **KI-Bewertung durchspielen**: eine echte (oder realistisch fehlerhafte) Schülerlösung
  des Gesamttests zusammen mit `bewertungspaket.pdf` einer KI geben; prüfen, ob Punkte,
  Folgefehler und Rückmeldung stimmen. Kriterien danach schärfen.

## Übertrag und Werkzeug

- [ ] `scripts/abgleich.py`: `build-clips.py` liegt bei 74.3 % (Grundlinie 84 %). Eintrag in
  `OFFEN` erst nach Abnahme — vorher `python3 scripts/abgleich.py --diff scripts/abgleich.py`.
- [–] Physik-Übertrag: steht in `TODO-schwesterprojekt.md` (zwei Einträge vom 02.10.2026),
  wird in einer Physik-Session abgearbeitet.

## Ältere Leitprogramme ans Vorbild angleichen

- [ ] `potenzen`, `quadratische-gleichungen`, `gleichungssysteme`: Warnkasten orange statt rot,
  `\mathbb{L}` statt `L` (gezählt 02.10.2026: `quadratische-gleichungen` 34 ×
  `\(L =`, `gleichungssysteme` 8 ×, `potenzen` 0) — per Skript, danach Pre-Flight.
- [ ] Entscheid offen: Sollen diese Leitprogramme auch auf das Kapitelmuster
  (Einführungsclip → Animation mit Aufgabenleiste → Kontrollclip) und auf Gesamttest als PDF
  umgestellt werden, oder bleibt das neuen Leitprogrammen vorbehalten?

## Ideen (ohne Auftrag)

- [ ] Verteiltes/gemischtes Üben über die Kapitel, adaptiver Weg nach dem Vorwissenstest.
- [ ] Bewegte Grafen im Clip (`bewegung`) über Parabeln hinaus (Geraden, Exponentialfunktionen)
  — Voraussetzung für weitere Leitprogramme dieser Art.
