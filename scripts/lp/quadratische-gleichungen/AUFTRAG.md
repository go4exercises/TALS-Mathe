Du arbeitest im Repo /home/paps/tals-mathe (statisches Mathe-Lehrmittel für die Berufsmaturität, RLP-BM 2030; Schweizer Hochdeutsch, KEIN ß, Dezimalpunkt statt Komma, MathJax nur mit \( \) und \[ \], leere Menge \{\,\}, Lösungsmenge \mathbb{L}, Elemente mit Strichpunkt).

AUFTRAG des Auftraggebers (wörtlich): «erstelle ein leitprogramm für die gleichungssysteme g2.3 und ein eigenes für lineare gleichungen g2.2a und ein eigenes für quadratische gleichungen g2.2b, prüfe diese und gib sie frei: alles in einem schub»

Drei Agenten bauen gleichzeitig je eines der drei Leitprogramme. DEIN Leitprogramm:
  «Quadratische Gleichungen», GF 2.2b (Themenseite grundlagen/g2-2b-quadratische-gleichungen.html).

LIES ZUERST (vollständig, verbindlich):
- /home/paps/tals-mathe/CLAUDE.md (Projektregeln, Verifikations-Standard, Pre-Flight)
- /home/paps/tals-mathe/HOWTO-leitprogramme.md (ganz, inkl. §15 Prüfliste — die Prüfung kommt danach von unabhängigen Agenten, die genau diese Liste abarbeiten; baue so, dass sie nichts findet)
- /home/paps/tals-mathe/HOWTO-clips.md (Drehbücher, Fragen im Clip, Vertonung, Bewegung in Graphen)
- /home/paps/tals-mathe/STYLEGUIDE.md §2 (Notation), §6.4, §6.5
- Die Themenseite(n) grundlagen/g2-2b-quadratische-gleichungen.html (Vorwissen: g2-2a, g1-3 Faktorisieren) — sie ist die fachliche Wahrheit (§1.2); ihre RLP-Box bestimmt die Kompetenzen (§1.1).
- Vorbild und Bausteine: `leitprogramme/lineare-quadratische-gleichungen.html` mit `scripts/lp/lineare-quadratische-gleichungen/` (README: der Umformer, §8d — für Gleichungen verbindlich) und `leitprogramme/quadratische-funktionen.html` (Kapitelmuster). Das bisherige gemeinsame Leitprogramm «Lineare und quadratische Gleichungen» (GF 2.2) wird durch die neuen Leitprogramme zu 2.2a und 2.2b abgelöst (wie am 08.10.2026 die Planimetrie durch 5.2a–d, siehe `scripts/lp/dreiecke/` usw.); seine Kapitel, Umformer-Aufgaben, Clips und Übungen sind Ausgangsmaterial — übernimm und erweitere, was passt, aber jedes neue Leitprogramm steht für sich (eigenes Vorwissen, eigene Clips `g2-2b-lp-*`, eigene Übungen, eigener Gesamttest, kein Verweis auf die Schwesterseite für fehlende Inhalte). Gleiche Beispiele wie dort sind erlaubt, wo sie passen, aber kein Selbsttest/Gesamttest darf ein Beispiel wiederholen (§9).
- Speicher-Notizen mit Erfahrungen aus früheren Leitprogrammen: /home/paps/.claude/projects/-home-paps-tals-mathe/memory/ — besonders leitprogramm-gleichungen.md, leitprogramme-g5-2.md, leitprogramm-modellieren.md, fragebild-nur-gegebenes.md, leitprogramm-betragsfunktionen.md, piper-vertonung-einrichten.md, pruef-clip-bilder-ablage.md, footer-version-2.md, intervallgrenzen-klammer-notation.md.

UMFANG: Kapitelmuster (§3/§4): Vorwissen mit Vortest, 4–5 Kapitel à 35–45 min (je Einführungsclip → Tüfteln (Umformer bzw. passende Simulation mit Aufgabenleiste) → Kontrollclip mit Fragen → Festhalten → 2–3 Übungen mit Rückmeldung → 3–4 Aufgaben mit Lösungen), Gesamttest und Bewertungspaket als PDF aus LaTeX (`downloads/leitprogramme/quadratische-gleichungen/`, `python3 scripts/build-lp-pdf.py quadratische-gleichungen` — immer mit Filter!). Alle Clips vertont (Piper, siehe Notiz), `"probe": true`, eigene Reihe, Theme `begreifbar-schlicht`.

DATEI UND NAMEN (fest):
- Seite: `leitprogramme/quadratische-gleichungen.html`, gebaut von `scripts/lp/quadratische-gleichungen/seite.py` (+ README.md im Ordner, wie bei den anderen). Die Datei gibt es schon: ein ALTES, ausgeblendetes Leitprogramm (noindex, «Alte Leitprogramme»). Du ERSETZT sie vollständig durch das neue (gleiche Adresse, damit alte Links weiter funktionieren); den alten Inhalt nur als Materialquelle lesen (er bleibt in git). Alte Schlüssel waren lp-quadratische-*. Alte Clips, die nur das alte Leitprogramm benutzte, nicht löschen.
- localStorage-Schlüssel: `lp-quadratische-gleichungen-thema`, `lp-quadratische-gleichungen-stand` (neu, nicht die alten).
- Clips: `clips/g2-2b-lp-*.json` (Präfix gehört nur dir), Reihe «Quadratische Gleichungen lösen».
- `build-seo.py` hat schon einen Eintrag mit `noindex=True` für deine Seite (unverlinkt bis zur Freischaltung) — nicht ändern.

GRENZEN (drei Agenten arbeiten gleichzeitig im selben Repo):
- Schreiben NUR: deine Seite, `scripts/lp/quadratische-gleichungen/`, deine Clips `clips/g2-2b-lp-*` (json/html/sprechertext/Ton), `downloads/leitprogramme/quadratische-gleichungen/`.
- NICHT anfassen: leitprogramme.html, index.html, Themenseiten, scripts/build-seo.py, scripts/build-suchindex.py, clips.html, scripts/clips_bibliothek.py, clips/clips.json, TODO.md, gemeinsame Module (scripts/lp/*.py, .claude/tools/*, mathlib.js, style.css, build-clips.py, build-clip-ton.py). Braucht ein gemeinsames Werkzeug eine Änderung oder findest du einen Fehler/Widerspruch in einer Themenseite: NICHT ändern, sondern in der Schlussmeldung genau beschreiben (Datei, Stelle, Vorschlag). Ein Widerspruch in der Themenseite wird nach §2d behandelt.
- NICHT ausführen: `build-seo.py`, `build-suchindex.py`, `build-clips.py` OHNE Clipnamen, `clips_bibliothek.py`, `build-lp-pdf.py` ohne Filter. `build-clips.py <clip>` mit Namen ist erlaubt (schreibt bei Probe-Clips kein clips.json). Fehlende Footer/SEO-Warnungen im Pre-Flight sind deshalb erwartet.
- Kein git ausser status/diff/log/show. Nicht committen (das macht der Auftraggeber-Agent).
- Browserprüfungen: eigener Server auf Port 8932 (PID merken, per PID beenden, nie pkill mit Muster); die .claude/tools/pruef-*.mjs wählen ihren Port selbst. Temporäre Dateien ins Scratchpad /tmp/claude-1000/-home-paps-tals-mathe/5ca7c177-e926-4cbb-997e-8116ba8ffc4b/scratchpad/quadratische-gleichungen/ (anlegen), `SP=` dorthin für pruef-clip.mjs.

QUALITÄT (hoher Anspruch — die unabhängige Prüfung nach §15 folgt):
- Jede Zahl, jede Lösung, jede Übungsaufgabe, jede Clipzahl und jede PDF-Lösung mit python3 nachrechnen (fractions/sympy wenn nötig). Zufallsübungen mit pruef-uebungen (1000) inkl. `fehler(A)`-Diagnosen; Umformer mit pruef-umformer; Aufgabenleisten mit pruef-leiste; Fragen in Kontrollclips mit pruef-fragen; Formelsatz mit pruef-formelsatz; render-check; pruef-mathjax.
- Clips: Drehbücher per Skript, zuerst ohne Ton mit pruef-clip.mjs Szene für Szene ansehen (Bilder mit dem Read-Tool ANSEHEN), dann build-clip-ton.py → build-clips.py; clip-zeit auf der Seite = gemessene Tonlänge. Nach der Vertonung das Erzeugerskript nicht mehr laufen lassen (überschreibt dauer).
- Kontrollfragen-Bilder zeigen nur das Gegebene (fragebild-nur-gegebenes.md).
- Kompetenzmatrix und Planung als HTML-Kommentar im Kopf (§2); Punkte- und Minutensummen stimmen; Hilfsmittel je Teil nach «auch ohne Hilfsmittel» im RLP.
- Hinschauen: hell und dunkel, 360 / 1280 / 1600 px (Playwright, Bildschirmfotos ansehen).
- `python3 .claude/skills/preflight/preflight.py leitprogramme/quadratische-gleichungen.html` — keine [FEHLER] in deiner Datei (Warnungen zu SEO/Footer/Suchindex sind erwartet, Fehler in fremden Selbsttests ignorieren).
- Wenn sich eine RLP-Kompetenz nicht im Zeitrahmen unterbringen lässt oder ein Kernkapitel einen Widerspruch der Themenseite berührt: trotzdem bauen (Konvention der Themenseite nehmen, §2d) und in der Meldung hervorheben — der Auftraggeber will alles in einem Schub.

SCHLUSSMELDUNG (knapp, deutsch): Kompetenzen K1… und ihre Kapitel; Kapitel mit Minuten und Clips (Namen, Dauer); Gesamtzeit/Lektionen; Punktesummen; was bewusst anders ist als auf der Themenseite und warum; gefundene Widersprüche/Fehler in Themenseite oder gemeinsamen Werkzeugen (mit Ort und Vorschlag); Ergebnisse aller Prüfwerkzeuge; was offen ist; Liste der erstellten/geänderten Dateien.
