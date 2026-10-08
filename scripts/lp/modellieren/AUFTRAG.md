# Auftrag: Leitprogramm «Modellieren» zur Themenseite grundlagen/g2-modellieren.html

Repo /home/paps/tals-mathe. Du baust EIN neues Leitprogramm im Kapitelmuster. Massstab: hohe fachliche und
didaktische Qualität — lieber weniger, dafür richtig und gut erklärt.

## Wortlaut des Auftraggebers (verbindlich)
«erstelle zu https://mathe.begreifbar.ch/grundlagen/g2-modellieren.html ein leitprogramm mit je einem kapitel pro
Aufgabenart (Zahlenrätsel, Mischen, Verteilen, Zins) mit Animationen, die die jeweilige Grundgleichung der
aufgabenart verständlich macht und Kontrollfragen-clips wo je aufgabenart mehrere aufgaben schrittweise vom text
über die deklaration zum ansatz geführt werden, dabei mal lineare gleichung dann quadratische gleichung dann
lineares gleichungssystem und quadratisches gleichungssystem entsteht - umformen in Grundform zum lösen mit TI30X
pro multiview»

Daraus folgt:
- **Vier Kapitel** = vier Aufgabenarten der Themenseite (Typ 1 Zahlen-/Ziffernrätsel, Typ 2 Mischen, Typ 3 Verteilen,
  Typ 4 Zins), dazu Vorwissen (Kapitel 0: Bilanzprinzip in vier Schritten der Themenseite, Gleichungstypen,
  TI-30X-Löser kurz) und Gesamttest. Kapitelzeit 35–45 min; die Kontrollclips dürfen länger sein als sonst.
- **Je Kapitel eine Animation (Simulation mit Aufgabenleiste)**, die die **Grundgleichung der Aufgabenart** sichtbar
  macht (z. B. Mischen: Menge × Gehalt addiert sich — Balken/Gefässe; Verteilen: Anteile/Stückpreis × Anzahl;
  Zins: Kapital × (1 + p/100)^n bzw. einfacher Zins, so wie die Themenseite; Zahlenrätsel: Stellenwert 10a + b,
  Ziffern tauschen). Grundgleichung so, wie die Themenseite sie formuliert — nachlesen, nicht erfinden.
- **Kontrollfragen-Clips je Aufgabenart mit MEHREREN Aufgaben**, jede **schrittweise**: Text → Deklaration
  (Variablen mit Bedeutung und Einheit) → Ansatz (Bilanz) → Umformen in die **Grundform für den TI-30X Pro MultiView**
  → Lösung mit dem Rechner → Antwortsatz/Probe. An jedem Schritt eine Kontrollfrage (Wahl- oder Klickfrage) mit
  Rückmeldung, die nicht die Lösung verrät. **Pro Aufgabenart sollen alle vier Gleichungsarten vorkommen**:
  lineare Gleichung, quadratische Gleichung, lineares Gleichungssystem (2×2), quadratisches Gleichungssystem
  (nichtlinear, z. B. Produkt und Summe). Sinnvoll: pro Kapitel zwei Kontrollclips (z. B. «eine Unbekannte»: linear +
  quadratisch; «zwei Unbekannte»: LGS + quadratisches GS). Wenn eine Kombination für eine Aufgabenart unnatürlich
  wäre, sag es im Bericht und begründe die Wahl — keine konstruierten Aufgaben, die niemand so stellt.
- **Rechner**: TI-30X Pro MultiView. Grundformen: quadratisch \(ax^2 + bx + c = 0\) → `poly-solv`;
  LGS \(a_1x + b_1y = c_1\), \(a_2x + b_2y = c_2\) → `sys-solv` 2×2; quadratisches GS: zuerst durch Einsetzen auf
  eine quadratische Gleichung in Grundform zurückführen → `poly-solv`, dann die zweite Variable; lineare Gleichung:
  von Hand umformen (oder `num-solv`, falls die Themenseite/Clips das so machen). **Jede Rechnerangabe belegen**:
  HOWTO-clips.md «Rechneranzeige — typ: "rechner"» (Quellen: TI-Online-Hilfe mit Bildschirmfotos, PDF-Handbuch,
  Links dort) und die vorhandenen Clips `clips/g2-2b-ti30x-poly-solv.json`, `g2-3-ti30x-sys-solv.json`,
  `g2-1-ti30x-num-solv-sachaufgabe.json`, `g2-2b-ti30x-real-oder-i.json` als Vorlage (Tastenfolge, Anzeige). Was nicht
  belegt ist, kommt nicht in den Clip (CLAUDE.md). Rechnerbilder mit `typ: "rechner"`.

## Zuerst lesen (vollständig)
1. `CLAUDE.md`; 2. `HOWTO-leitprogramme.md` ganz (inkl. §15 Prüfliste — alle Fehlerklassen von vornherein vermeiden);
3. `STYLEGUIDE.md` §2.11, §6.4, §6.5; 4. `HOWTO-clips.md` (Drehbuchformat, Fragen, Rechneranzeige, «Später einblenden,
bewegen, mitlaufen» inkl. «Zweite/Dritte Runde», Teilvertonung `--szenen`/`--fragen`);
5. Vorbild-Bauweise: `scripts/lp/lineare-quadratische-gleichungen/` (README, seite.py, seite.js, clips.py) und
`leitprogramme/lineare-quadratische-gleichungen.html` (GF 2.2, Gleichungen) sowie ein neueres:
`scripts/lp/trigonometrische-gleichungen/` (seite.py mit SEO-Block-Handling: nur beim ersten Lauf noindex setzen,
einen vorhandenen Block mit JSON-LD NIE überschreiben), `downloads/leitprogramme/<vorbild>/*.tex`,
`scripts/build-lp-pdf.py`.
6. Die Themenseite `grundlagen/g2-modellieren.html` ganz (fachliche Wahrheit, Notation, Bilanzprinzip,
Beispiele, Ansatz-Trainer, technische Zusatzserie), dazu ihre zwei Clips `clips/g2-M-*.json`. RLP-Text aus der
Kompetenzbox der Seite (Teilgebiete 2.1 und 2.3) wörtlich übernehmen; der RLP liegt als `/home/paps/Math-GL.pdf`
(mit python3/pypdfium2 lesbar) — die Kompetenzen dort nachlesen.
7. Für die Gleichungsarten die Themenseiten g2-1, g2-2a/b, g2-3 (Notation von Lösungsmengen, Grundform, Rechner).

## Name, Dateien, Grenzen
- `leitprogramme/modellieren.html` (Titel «Leitprogramm Modellieren» o. ä., wie die Themenseite heisst),
  `scripts/lp/modellieren/*` (README.md, seite.py, seite.js, clips.py, zahlen.py mit allen Zahlen),
  `clips/g2-M-lp-*.json/.html`, `clips/sprechertext-g2-M-lp-*.txt`, `clips/ton/g2-M-lp-*.mp3`,
  `downloads/leitprogramme/modellieren/*`. Alle Clips `"probe": true`, eigene `reihe` (z. B. «Ansatz finden»),
  `lektion: ["g2-M"]` (prüfe, welches Kürzel die Themenseite in clips.json trägt).
- localStorage-Schlüssel `lp-modellieren-thema`, `lp-modellieren-stand`.
- NICHT anfassen: `leitprogramme.html`, `index.html`, Themenseiten, `scripts/build-seo.py`, `scripts/build-suchindex.py`,
  `clips.html`, `clips/clips.json`, `scripts/build-clips.py` und andere gemeinsame Werkzeuge, TODO/HOWTO-Dateien,
  andere Leitprogramme. Kein git commit, kein git push, kein `rm -rf`. Fehlt etwas im Clip-Bauer: Behelf + Wunsch.
- Seitenkopf: `<meta name="robots" content="noindex, nofollow">` im SEO-Block (unverlinkt; das Eintragen mache ich).

## Technik und Prüfen
- Clips: `python3 scripts/build-clips.py <clip>`; vertonen:
  `export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx;
   python3 scripts/build-clip-ton.py <clip>` und für Fragen `python3 scripts/build-clip-fragen-ton.py <clip>`
  (siehe HOWTO), danach build-clips.py. Bei späteren Korrekturen nur betroffene Szenen: `--szenen`, `--fragen`.
  Zeiten (`ein`, Bewegungen) auf gemessene Wortzeiten: `python3 .claude/tools/sprechzeiten.py <clip>` bzw.
  faster-whisper (`~/.local/share/whisper-venv/bin/python`, mp3 vorher mit System-python3/soundfile dekodieren).
  Ergebnis nie vor dem Satz, der es nennt. Sprechertexte so, wie Piper sie gut spricht (Zahlen ausgeschrieben).
  Fragebild zeigt nur das Gegebene (`scripts/lp/fragebild.py`); Text der Frage = gesprochener Text.
- JEDE Zahl (Aufgaben, Lösungen, Clips, Leistenziele, Gesamttest, Raster, Folgefehler) in `zahlen.py` mit python3
  nachrechnen. Schöne Zahlen; Lösungen im Sachkontext sinnvoll (keine negativen Mengen, Probe), bei quadratischen
  Gleichungen die unbrauchbare Lösung im Antwortsatz begründet verwerfen. Lösungsmengen nach STYLEGUIDE §2.11.
- Übungen: Zufallsübungen mit Diagnosen (Testhaken `box.__aufgabe`/`box.__typ`, `fehler(A)`), z. B. «Deklaration
  wählen», «Ansatz zuordnen», «in Grundform bringen» (Koeffizienten a, b, c bzw. a₁ b₁ c₁ a₂ b₂ c₂ eingeben —
  das ist die Rechnereingabe), Sperrliste gegen feste Aufgaben, Verteilung über 20 000 Würfe zählen.
- Gesamttest + Bewertungspaket (LaTeX → PDF), Teile nach Aufgabenart, jede Gleichungsart mindestens einmal;
  Taschenrechner erlaubt. Raster nach §15 (Fehlerbeispiele wirklich falsch, fehlende Lösung kein Folgepunkt …).
- §14 vollständig: pruef-uebungen 2000, pruef-formelsatz 60, pruef-leiste, pruef-fragen auf alle Kontrollclips (in
  Stapeln, ohne kurzen timeout), pruef-clip (SP=/tmp/claude-1000/-home-paps-tals-mathe/5ce60464-7415-4eef-95b6-ccf61adcaff3/scratchpad/lp-g2M)
  und Bilder ANSEHEN, pruef-mathjax mit eigenem http.server auf Port 8907, render-check, Preflight
  `python3 .claude/skills/preflight/preflight.py leitprogramme/modellieren.html`. Seite bei 360/1280 px hell und
  dunkel ansehen, PDFs ansehen. Erreichbarkeit der Leistenziele mit Maus/Finger.

## Ablauf
1. Planung nach HOWTO §2 (Kompetenzmatrix, Planungstabelle mit allen Aufgaben je Kapitel und welcher Gleichungsart,
   Kern/Vertiefung/weggelassen, Konventionen, Widersprüche der Themenseite) als HTML-Kommentar im Seitenkopf.
2. Bauen. 3. Prüfen (§14). 4. Bericht (Deutsch): Planung kurz (Tabelle Kapitel × Aufgabe × Gleichungsart ×
   Rechnerlöser), was bewusst anders als die Themenseite, Widersprüche der Themenseite, Dateien, Prüfergebnisse,
   SEO-Beschreibung (1–2 Sätze) + Themen-Stichworte, Lektionen, Clipzahl/-zeit, offene Punkte, Wünsche an den
   Clip-Bauer, Rechnerangaben mit Beleg (Quelle je Angabe), ehrlich was nicht angesehen wurde.
