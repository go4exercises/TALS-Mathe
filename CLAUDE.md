# CLAUDE.md — TALS Mathe

Statisches HTML/CSS/JS-Lehrmittel für die BM (RLP-BM 2030), gehostet via GitHub Pages.
Schwester-Projekt zu TALS Physik. Diese Datei ist die lokale Claude-Code-Variante der
COLLABORATION.md — sie ersetzt den alten ZIP-Workflow durch einen Git-Workflow.

**Autoritative Detail-Konventionen stehen in `STYLEGUIDE.md` (im Repo). Diese Datei ist
die Kurzfassung + der verbindliche Pre-Flight. Bei Widerspruch gilt STYLEGUIDE.md.**

## Sprache & Notation (nicht verhandelbar)

- Schweizer Hochdeutsch. **Kein ß** — immer „dass", „muss", „Schluss".
- **Dezimaltrennzeichen ist der Punkt, nie das Komma** — überall: LaTeX (`9.81`, nicht
  `9{,}81`), Aufgabentexte, Live-Anzeigen, JS-Code.
- MathJax-Delimiter: `\(…\)` inline, `\[…\]` abgesetzt. Niemals `$…$`.
- **Leere Menge als `\{\,\}`**, nie `\emptyset` oder `∅` (STYLEGUIDE §2.11).
- Alles Mathematische in LaTeX/MathJax.

## Bereichs- & Farbsystem (STYLEGUIDE §5)

- **Bereichsfarben:** Grundlagenfach = **Blau** (`--blau`, `--blau-hell`),
  Schwerpunktfach = **Violett** (`--lila`, `--lila-hell`). Das ist die Mathe-Identität
  (Physik dagegen Bernstein/Amber).
- **Didaktische Farben — kapitelübergreifend IMMER dieselbe Bedeutung:**
  Blau = Definition/Theorie (`block-def`, 📘) · Grün = Beispiel/Lösung · Orange =
  Aufgabe/Übung (`block-aufg`) · Rot = Fehler/Achtung · Lila = Beweis/Herleitung ·
  Blau-Variante = Merksatz/Schlussfazit (`block-merksatz`, ⭐). Farben nie umdeuten.

## Projektstruktur

- `grundlagen/` — Grundlagenfach: `g1-*` … `g5-*` (24 Seiten, inkl. Sub-Splits `g2-2a/b`, `g5-2a–d` und der
  Modellier-Seite `g2-modellieren` mit nav-Kürzel `g2-M` / `2.M`).
- `schwerpunkt/` — Schwerpunktfach: `s1-*` … `s4-*` (23 Seiten, inkl. Sub-Splits `s2-2a–c`,
  `s3-2a/b`, `s3-4a/b`, `s4-2a–c`, `s4-3a–d` und Ergänzungen `s3-6`, `s4-3d`). Alle Teilgebiete
  sind ausgebaut — es gibt keine Stubs mehr.
- `mathlib.js` — Canvas-Bibliothek + globale Helfer (`toggleL` u.a.).
- `minicheck.js` (Mini-Check-Akkordeon), `anim-hinweise.js` (👁/💡-Rollover, Pflicht bei
  interaktiven Animationen), `nav.js` (`buildNav`), `style.css`.
- `formelsammlung.html`, `glossar.html`, `clips.html`, `leitprogramme.html`,
  `simulationen.html`, `werkzeuge.html` — sechs Nachschlag-Seiten im Repo-Root.
- `simulationen/` und `werkzeuge/` — eigene Seiten neben den Themenseiten, seit 10.10.2026
  streng getrennt: **Simulation** = ein Modell beobachten und seine Grössen verändern,
  **Werkzeug** = eigene Aufgaben oder Daten eingeben bzw. üben (Trainer, Rechner). Je eine
  Übersicht (`simulationen.html`, `werkzeuge.html`), verlinkt aus dem Abschnitt der
  Themenseite, zu dem sie gehören (Baustein `🛠 Werkzeug:` / `🧪 Simulation:` in
  `.block-tipp`) — **nicht** am Seitenanfang und **nicht** auf den Kacheln von
  `index.html`. Anleitung: `HOWTO-simulationen.md`, `HOWTO-werkzeuge.md`; der Pre-Flight
  prüft mit `check_sim_wz`. Alte Adressen leitet `404.html` weiter (Tabelle `WEITERLEITUNGEN`).
- `simulationen/standardabweichung.html` (seit 11.10.2026, erste Simulationsseite): eine Stichprobe (2–8 Werte, 0–20)
  ziehen oder eintippen, in sechs Schritten von den Abweichungen über ihre Quadrate (flächengetreu) zu Varianz und
  \(s\) (Standard \(n - 1\) wie g4.3, umschaltbar auf \(\sigma\)), dann \(R\), \(\text{QD}\) (Median der Hälften) und
  \(\bar{x} \pm s\) im Vergleich und «ohne den äussersten Wert». Variationskoeffizient nur als Zusatz (nicht im RLP).
  Aus einer externen Vorlage übernommen und angepasst. Selbsttest `scripts/verify_standardabweichung.js` (python3
  `statistics`). Verlinkt aus g4.3 (`#darstellungen`).
- `simulationen/boxplot.html` (seit 11.10.2026): 4–15 ganze Werte (0–20) im Punktdiagramm, gemeinsam für sechs Schritte —
  sortierte Liste mit Plätzen von \(Q_0\)…\(Q_4\) (Median der Hälften), Boxplot Teil für Teil, vier Teile mit gleich vielen
  Werten (nach Rang; Plätze genau auf einer Grenze zählen zu keinem Teil) und Form (`form()`), Ausreisser nach der
  Faustregel \(1.5 \cdot \text{QD}\) aus g4.3, Vergleich mit einer Gruppe B. Selbsttest `scripts/verify_boxplot.js` (python3
  `statistics`, prüft auch die Aussagen «drei Viertel ≤ \(Q_3\)» und «Hälfte ≥ Median»). Verlinkt aus g4.2 und g4.3 (`#darstellungen`).
- `werkzeuge/notationstrainer.html` — Lernkartei (3 Fächer, Stand in `localStorage` unter
  `tals-mathe-notationstrainer-v1`, in `rechtliches.html` genannt) zur Notation von
  𝔻, 𝕃 und Intervallen mit wechselnder Grundmenge. Die Karten stehen als Array `KARTEN`
  im Seitenskript und nennen das **Ergebnis** der Rechnung, nicht die Aufgabe — geübt wird
  nur die Schreibweise; jede Lösung vor dem Eintrag mit `python3` nachrechnen. Verlinkt aus
  g2.1 (`#definition`); seit 10.10.2026 nur Grundlagenfach (116 Karten, die 25 des
  Schwerpunktfachs und der Fach-Filter sind entfernt). Bis 10.10.2026 lag er als `notationstrainer.html` im Root.
- `werkzeuge/strategietrainer.html` (seit 10.10.2026): Zufallsaufgaben aus sieben Bereichen —
  lineare, quadratische und Bruchgleichungen, Faktorisieren, Bruchterme, lineare Systeme und Systeme
  mit Parabel (SF). Man wählt den nächsten Schritt aus einer festen Liste je Familie (Gleichungen 15,
  Terme 10, Systeme 7); das Werkzeug führt ihn aus (✓), weist einen erlaubten Umweg grau ab (≈) oder
  begründet den Fehlgriff (✗; Tipp beim zweiten, Lösung beim dritten). Aufgaben werden von hinten
  gebaut, gerechnet wird exakt (Brüche, Wurzeln, ganzzahlige Paare). Der Kern steht zwischen
  `KERN:ANFANG`/`KERN:ENDE` und wird von `scripts/verify_strategietrainer.js` (im Pre-Flight) mit
  Zufallsaufgaben durchgespielt: alle Wege, Lösungen gegen die gestellte Aufgabe, Terme an
  Zufallsstellen, 𝔻 gegen den Nenner. Neue Vorlage oder Regel → dort zuerst grün. Vorwahl über
  `#bereich=fakt,bruchterm` (kein `?`: `check_sim_wz` liest die Adresse bis `#` als Dateinamen).
  Verlinkt aus g1.3, g2.2a, g2.2b, g2.3, s2.2a, s3.1. Weitere Trainer-Ideen: `../TODO-trainer-mathe.md`.
- `werkzeuge/rechentrainer.html` (seit 11.10.2026): Rechnen ohne Taschenrechner (GF 1.1/1.2) in sechs
  Themen — Hierarchie der Operationen, Vorzeichen, Brüche, Bruch–Dezimal–Prozent, Perioden, Zahlenmengen. Kern ist die
  **Fehlerdiagnose**: Jede Aufgabe wird zusätzlich mit typischen Denkfehlern gerechnet (Parser mit
  umschaltbaren Regeln: Strich vor Punkt, −3² als 9, a − (−b) als a − b …); trifft die Antwort einen
  davon, nennt die Rückmeldung den Fehler mit Link (`FEHLER`). Lösungsweg Stufe für Stufe nach g1.1.
  Vorwahl `#thema=reihenfolge,vorzeichen`. Selbsttest `scripts/verify_rechentrainer.js` rechnet jede
  Aufgabe in `python3` mit `Fraction` nach.
- `werkzeuge/einheitskreistrainer.html` (seit 11.10.2026): Grad ↔ Bogenmass, exakte Werte von sin/cos/tan
  (Palette, Diagnose: Vorzeichen, sin/cos bzw. 30°/60° vertauscht, Kehrwert, «nicht definiert»), vom Wert
  zum Winkel (Punkte am Kreis anklicken). Werte aus Quadrant und Referenzwinkel, Herleitung mit Skizze.
  Anzeige Grad/Bogenmass/gemischt; Vorwahl `#teil=werte&mass=rad`. Selbsttest
  `scripts/verify_einheitskreistrainer.js` mit Gegenrechnung in `python3`.
- `werkzeuge/termtrainer.html` (seit 11.10.2026): Terme umformen (GF 1.3, SF 1.1) in sieben Themen — Zusammenfassen,
  Klammern, Klammer mal Klammer, binomische Formeln, Ausklammern, Faktorisieren, Bruchterme kürzen. Die Eingabe
  (`3x^2-2x+1`, `2x(x+3)(x-3)`, `(x-3)/(x+3)`) wird exakt als Quotient zweier Polynome verglichen; die Form
  (ausmultipliziert, vollständig faktorisiert, gekürzt) am Syntaxbaum. Aufgaben stehen als Eingabetext,
  Lösungsweg und Denkfehler ebenso (`diag`, `FEHLER`). Vorwahl `#thema=binome,faktorisieren`. Selbsttest
  `scripts/verify_termtrainer.js` wertet alles in `python3` mit `Fraction` aus und prüft Unzerlegbarkeit.
- `werkzeuge/gesetzetrainer.html` (seit 11.10.2026): Potenz-, Wurzel- und Logarithmengesetze (GF 1.4, SF 1.2, 1.3),
  Bereiche wählbar (`#bereich=potenzen,wurzeln,rational,logarithmen`; `wurzeln` nur GF-1.4-Stoff mit
  ⁿ√x = x^{1/n}, m/n-Exponenten im Bereich `rational` (SF)). Antwort in Feldern einer Zielform (`ziel`, z.B.
  `x^{{n}}`, `{k}\sqrt{{r}}`); Potenzterme als Exponentenbäume, Denkfehler durch umgeschaltete Regeln
  (`expo(x, 'p1mal')` …), dazu «Regel prüfen» (`FALLEN`). Selbsttest `scripts/verify_gesetzetrainer.js` rechnet
  in `python3` unabhängig nach (Wurzeln als `(x**m)**(1/n)`, `math.log`).
- `werkzeuge/systemtrainer.html` (seit 11.10.2026): lineare Gleichungssysteme (GF 2.3) in vier Themen — 2×2 lösen,
  Sonderfälle 2×2, 3×3 lösen, Lösungsfall erkennen (`#thema=zwei,sonder,drei,lage`). Man wählt den Lösungsfall und gibt
  𝕃 ein: Zahlen bzw. bei unendlich vielen Lösungen \(y\) (und \(z\)) als Ausdruck in \(x\), Schreibweise
  \(\{(x \mid \ldots) : x \in \mathbb{R}\}\) wie in g2.3 und im Notationstrainer. Die Prüfung macht die Probe und
  erkennt vertauschte Werte, Vorzeichen, falschen Lösungsfall, Fehler beim Auflösen nach y. Lösungsweg nach Form
  (Einsetzen, Gleichsetzen, Addieren mit kleinerem kgV; 3×3: eliminieren, 2×2, zurück), bei 2×2 Skizze der Geraden (SVG).
  Selbsttest `scripts/verify_systemtrainer.js`: python3 löst jedes System selbst und prüft, dass jede Wegzeile aus dem
  System folgt (Zeilenraum der erweiterten Matrix); `STATISTIK.widerspruch` muss 0 bleiben, sonst verwirft der
  Erzeuger kaputte Wege still.
- `leitprogramme/` — 22 Seiten zum selbstständigen Durcharbeiten, je eine
  eigenständige Seite mit eigenem `<style>` (wie `clips/`, darum vom Skelett-Check
  ausgenommen). Schriften über `../schriften.css`, MathJax über
  `../vendor/mathjax/tex-svg.js` — **kein fremder Host**. Farben, Kopf, Fuss und
  Clip-Bühne werden von der Site *geerbt*, nicht kopiert. Die Übersicht
  `leitprogramme.html` wird von Hand gepflegt. **Seit dem 06.10.2026 sind dort nur die
  neuen Leitprogramme mit Clips, Animationen und Kontrollfragen sichtbar** — sechzehn
  (`quadratische-funktionen`, `lineare-funktionen`, `potenz-wurzelfunktionen`,
  `polynomfunktionen`, `exp-log-funktionen`, `trigonometrische-funktionen`,
  `betragsfunktionen`, `lineare-quadratische-gleichungen`, `dreiecke`, `vierecke`, `kreis-kreisteile`, `aehnlichkeit`,
  `trigonometrische-berechnungen`, `einheitskreis`, `trigonometrische-gleichungen`, `modellieren`). Die sechs älteren (`potenzen`, `quadratische-gleichungen`,
  `gleichungssysteme`, `uebungspruefung-1`, `trigo2` und seit 08.10.2026 `planimetrie`, abgelöst durch je ein
  Leitprogramm zu 5.2a–d) bleiben als Dateien bestehen, ihre
  Kärtchen stehen vorübergehend unter «Alte Leitprogramme (werden demnächst ersetzt)»
  am Ende von `leitprogramme.html`; sie tragen `noindex` und fehlen
  im Suchindex. Die Indexseite zeigt neben jeder Themenseite mit Leitprogramm eine
  kleine Pille «LP» (`.karte-lp`/`.lp-link` in `index.html`). Die zwei Arten:
  - *nach Thema* (20: `potenzen.html`, `quadratische-gleichungen.html`,
    `gleichungssysteme.html`, `quadratische-funktionen.html`, `lineare-funktionen.html`,
    `exp-log-funktionen.html`, `trigonometrische-funktionen.html`, `betragsfunktionen.html`,
    `potenz-wurzelfunktionen.html`, `polynomfunktionen.html`, `lineare-quadratische-gleichungen.html`
    (Umformer statt Regler), `planimetrie.html` (Geometrie-Arbeitsbereich), `trigonometrische-berechnungen.html`,
    `einheitskreis.html`, `trigonometrische-gleichungen.html` (GF 5.3–5.5, freigeschaltet 08.10.2026),
    `modellieren.html` (GF 2.M Textaufgaben, je Aufgabenart ein Kapitel, freigeschaltet 08.10.2026),
    `dreiecke.html`, `vierecke.html`, `kreis-kreisteile.html`, `aehnlichkeit.html` (GF 5.2a–d, je Themenseite ein
    Leitprogramm, freigeschaltet 08.10.2026))
    — Vorwissenstest, 4–5 Kapitel,
    Gesamttest. `quadratische-funktionen.html` ist das Vorbild für neue (Kapitelmuster mit
    Einführungs- und Kontrollclip, Animation mit Aufgabenleiste, Übungen mit Rückmeldung,
    Gesamttest und Bewertungspaket als PDF aus LaTeX unter `downloads/leitprogramme/`).
    Aufbau, Didaktik und Technik: **`HOWTO-leitprogramme.md`** (seit 02.10.2026 Gesamtfassung;
    Vorbild `quadratische-funktionen.html`, Bauskript unter `scripts/lp/quadratische-funktionen/`;
    `lineare-funktionen.html` ist nach demselben Muster gebaut, mit **bewegten Geraden** in
    den Clips und Fragen beider Typen — Bauskripte unter `scripts/lp/lineare-funktionen/`).
    Extern gebaute Datei hereinholen: dort §12, Punkt für Punkt.
    **Vor der Freischaltung** unabhängig prüfen: Skill `/lp-pruefung leitprogramme/<name>.html`
    (§15, drei Agenten gegen die Prüfliste, Befunde nach `TODO.md`); Prüfwerkzeuge
    `.claude/tools/pruef-uebungen.mjs`, `pruef-formelsatz.mjs`, `pruef-leiste.mjs`, `pruef-fragen.mjs`, `sprechzeiten.py`.
  - *nach Prüfungsbogen* (2: `uebungspruefung-1.html`, `trigo2.html`) — jede
    Teilaufgabe mit eigenem
    Clip, Musterlösung und Punktezeile. Der ganze Weg vom PDF zur Seite steht in
    **`HOWTO-uebungspruefung.md`**; er hat eigene Fallstricke (verlorene Hoch- und
    Überstriche in der PDF-Extraktion, `"probe": true` an den Clips).
  **Ein Leitprogramm hängt an fünf Stellen**: Pille «LP» auf der Indexseite, eine Kachel je Leitprogramm in `leitprogramme.html` (führt zum Leitprogramm; darauf je Themenseite ihr Titel und eine Pille mit der Nummer wie `g5.2a`, die zur Themenseite führt; nach Fach und Themenbereich gegliedert, nach Nummer sortiert), Eintrag
  in `scripts/build-seo.py` (Sitemap), in `scripts/build-suchindex.py` (Volltext­suche)
  und ein Kasten «🧭 Lieber geführt?» auf der Themenseite nach den Lernzielen.
  Fehlt eine, ist die Seite entweder unsichtbar oder unauffindbar. Die `"probe": true`
  an den Prüfungsclips bleibt davon unberührt — sie hält die Clips aus der Bibliothek,
  nicht die Seite aus der Site.

  Das Verbindliche für beide: STYLEGUIDE §6.5.
- `clips/` — 586 Drehbücher, alle vertont: **391 in `clips.json`** (363:01 min,
  56 Reihen, 255 Grundlagenfach / 136 Schwerpunktfach) und **195** Clips mit
  `"probe": true` (35 Prüfungsclips und 160 Clips der Leitprogramme nach Thema:
  je 10 «Parabel sehen», «Kurve sehen», «Polynom sehen», «Exponentialkurve sehen»,
  «Sinuskurve sehen», «Knick sehen», «Figuren sehen», «Gleichungen lösen», «Dreiecke berechnen»,
  «Einheitskreis sehen», 12 «Ansatz finden», je 8 «Gerade sehen», «Winkel finden», «Dreiecke sehen», «Vierecke sehen», «Kreisteile sehen», «Ähnlichkeit sehen»), die im zugehörigen Leitprogramm stehen und
  weder in `clips.json` noch auf einer Lektionsseite auftauchen. Die Clips der *sichtbaren* Leitprogramme zeigt
  `clips.html` seit 06.10.2026 trotzdem: je Themenseite eine Tabelle Animationen · Leitprogramm · Weitere Clips
  (`scripts/clips_bibliothek.py`, HOWTO-clips «Bibliotheksseite»). **46 der 47 Themenseiten tragen Clips** (ohne: `g4-0`). Von Hand geschrieben wird nur das Drehbuch `clips/<name>.json`;
  `.html`, `sprechertext-*.txt`, `clips.json` und die Blöcke auf den Lektionsseiten
  sind **generiert**. Der Bauer `scripts/build-clips.py` ist seit 07.10.2026 **derselbe Code wie in
  Physik**, verschieden sind nur Einstellungen am Dateianfang (HOWTO-clips «Ein Bauer für beide Fächer»);
  eine Korrektur daran gehört darum auch nach `TODO-schwesterprojekt.md`. Formeln stehen in LaTeX — Kleiner/Grösser als `\lt` und `\gt`,
  nicht als HTML-Entität. Vollständig in `HOWTO-clips.md`, das Verbindliche in
  STYLEGUIDE §6.4.
  **Animationsclips** (`animation`, Reihe «Animationen erklärt»): 223 Clips auf 46 Seiten
  (Stand 28.09.2026), je Animation einer, «▶ Clip» in ihrer Titelzeile. Wie in
  `HOWTO-clips.md`, «Bild einer Animation».
  **Rechner-Clips** (`werkzeug: true`, 22 Stück auf 14 Seiten) sind ein eigener Strang:
  keine eigene Reihe, sondern letzter Clip der Reihe, deren Stoff sie bedienen. **Jede
  Angabe zum TI-30X Pro MathPrint gehört nachgeschlagen**: zuerst in der TI-Online-Hilfe
  (Bildschirmfotos, Kapitel zu Lösern, Matrizen, Vektoren), dann im PDF-Handbuch — Links
  und Rezept in `HOWTO-clips.md` («Rechneranzeige»). Was in beiden nicht steht, kommt
  nicht in einen Clip, sondern nach `TODO-ti30x-am-geraet.md` (seit 30.09.2026 gelöscht,
  alle Fragen geklärt; bei der nächsten offenen Frage neu anlegen).
- `schriften.css` + `schriften/` — lokal ausgelieferte Schriften (Fontsource 5.3.0,
  OFL). `vendor/mathjax/` — MathJax 3.2.2 (Apache 2.0). **Keine Seite lädt etwas von
  einem fremden Host**; Details und Fallstricke in STYLEGUIDE §5.3.1. Umgestellt wird
  mit `scripts/schriften-lokal.py` und `scripts/mathjax-lokal.py`.
- `scripts/abgleich.py` — vergleicht das **geteilte Werkzeug** mit dem
  Schwesterrepo `tals-physik`. Physik und Mathe teilen rund 5200 Zeilen
  Build-Skripte und Prüfer; gepflegt werden sie zweimal, und sie laufen
  auseinander. Das Skript verhindert das nicht, es macht es sichtbar: drei
  Klassen (`GLEICH` Fremdgut — jeder Unterschied ist ein Befund; `KERN`
  geteiltes Werkzeug, gemessen gegen eine **Grundlinie**, die nur steigen
  darf — Seitenlisten darin, die mit jeder Seite wachsen, nennt `DATEN` und
  misst sie nicht mit; `FACH` bewusst verschieden, mit Begründung). `--check` gibt Exit 1
  bei neuer Drift, `--diff DATEI` zeigt sie, `--gegen PFAD` wählt das
  Gegenüber. Es schreibt nie etwas, und fehlt das Schwesterrepo, endet es
  mit Exit 0. Der Pre-Flight ruft es auf und meldet Drift als **[WARN]** —
  ein Hinweis, kein Blocker. Dieselbe Datei liegt in beiden Repos; wer eine
  Fassung angleicht, trägt die neue, höhere Grundlinie dort ein.
- `scripts/build-seo.py` — erzeugt Seiten-Metadaten (Beschreibung, canonical, Open
  Graph, JSON-LD nach schema.org/LearningResource), `sitemap.xml`, `robots.txt` und den
  **Footer** jeder Seite (zwischen `<!-- FUSS:ANFANG -->` und `<!-- FUSS:ENDE -->`; Ortszeile
  über `ort=` in `SEITEN`, Version über `VERSION`/`VERSION_STAND` — eine für das ganze Lehrmittel).
  Der Kopfblock zwischen `<!-- SEO:ANFANG -->` und `<!-- SEO:ENDE -->` ist
  **generiert** — gepflegt wird die Tabelle `SEITEN` im Skript. Neue Seite = dort
  eintragen, sonst fehlen ihr Beschreibung und Sitemap-Eintrag. Der Pre-Flight
  warnt, wenn die Metadaten veraltet sind.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og-bild.png` — Bild-Assets
  der Auffindbarkeit, erzeugt von `.claude/tools/build-bilder.mjs` (braucht einmalig
  Netz für die Google Fonts). Nur neu bauen, wenn Farben oder Wortlaut ändern.
- Skelett-Quelle: `TEMPLATE.html` + `HOWTO-neue-themenseite.md`.

## Inhaltliche Regeln (STYLEGUIDE §4)

- **Master-Schema je Seite vollständig:** eigener Einstieg, eigene Definition, eigene
  Aufgaben A1–A6 (optional A7 Vertiefung), eigene Zusammenfassung. **Keine Verweise auf
  die Schwesterseite** für fehlende Inhalte — jede Sub-Seite steht für sich.
- **Sub-Split-Namen:** Buchstaben-Suffix direkt an die RLP-Nummer (`g2-2a`, `g2-2b`);
  gemeinsames Numerik-Präfix, Unterschied nur im Suffix.
- Aufgaben-Markup: `aufg-nr-tag` (orange Pille, monospace), `aufg-titel-text`, optional
  `aufg-vertiefung`-Pille am Ende.
- **x-y-Skalierung aufgabenbezogen**, nicht zwingend 1:1, wenn die Achsen
  unterschiedliche Grössen/Einheiten tragen (STYLEGUIDE §… „keine 1:1-Forderung").
- Lernziele: aufklappbare „Ich kann …"-Liste direkt nach der RLP-Kompetenzen-Box,
  Blau-Familie, 4–6 Punkte.

## Skelett & Klassen — kopieren, nicht erfinden

- Neue Seite / neuer Block: Skelett aus `TEMPLATE.html` (oder einer Nachbar-Seite)
  **1:1 kopieren**, nur Inhalt anpassen. CSS und `nav.js` sind auf die *exakten*
  Klassennamen ausgerichtet.
- **Niemals eigene Klassennamen, Container-Hierarchien oder API-Signaturen erfinden.**
  Erfundene Klassen fallen still auf Block-Default zurück (Karten werden zu Listen,
  Sidebar überlappt).
- Jede Seite mit `onclick="toggleL(…)"` o.ä. **muss `mathlib.js` einbinden**. Mit
  `.anim-hinweis`-Markup → `anim-hinweise.js`. Mit `.minicheck`-Markup → `minicheck.js`.
- Slider-Farbkopplung: `akz-blau/akz-orange/akz-gruen` auf `.sl-grp`, und dieselben
  Farben in der Live-Formel via `.tx-…`-Spans bzw. `\textcolor{#1a4f8a|#b85c00|#1f6b3a}{…}`.

## Pre-Flight (verbindlich vor jedem Commit)

Nach jeder Änderung an Themenseiten, **bevor** committet wird:

```bash
python3 .claude/skills/preflight/preflight.py grundlagen/<datei>.html
# oder über alle: python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html
```

Erwartete Ausgabe: `ALLE CHECKS BESTANDEN`. Jede `[FEHLER]`-Meldung wird vor dem Commit
behoben (`[WARN]` ist kein Blocker). Zweistufig: (1) schnelle Eigen-Checks — div/details-
Bilanz, doppelte IDs, kein ß, Dezimalkomma in Body-Math, HTML im LaTeX, Skelett, Phantom-Klassen,
mathlib-Einbindung, Ressourcen-Marker; (2) Aufruf der vorhandenen Repo-Skripte
`verify_mathjax.js` (echte Render-Prüfung), `verify_js_runtime.js` (JS-Laufzeit) und
`check_identifier_collisions.py`. Stufe 2 braucht einmalig `npm install mathjax-full jsdom`
im Repo-Root; fehlen die Module, werden diese Checks als `[WARN]` übersprungen.
**Vom Repo-Root aufrufen.**

## Verifikations-Standard

- **Alle Zahlenwerte vor dem Einbau mit `python3` nachrechnen** — nie aus dem Gedächtnis.
- **Geometrie/Funktionsgraphen von Canvas-Animationen vorab in Python durchrechnen**
  (Stützpunkte, Schnittpunkte, Label-Positionen), bevor der Zeichencode geändert wird.
- `node --check` auf jedem Script-Block (der Pre-Flight macht das mit).
- Render-Check bei Graph-Änderungen, wenn ein Browser verfügbar ist: Playwright headless
  bei 1280 px **und** 360 px, Screenshots der Canvases sichten. `npm run render-check`
  (oder `node .claude/tools/render-check.mjs <seiten>`) meldet seitliches Scrollen und
  Formeln/Tabellen, die ein `overflow:hidden` abschneidet. Ob eine *Live-Anzeige* aus
  ihrem eigenen Kasten läuft, sieht er nicht — dafür bleibt `check-breite.mjs`.
- **Clips: Layout vor dem Commit prüfen** — `node .claude/tools/pruef-clip.mjs
  clips/<name>.html <sekunden…>` meldet überlappende Zeilen und Überlauf und legt je
  Zeitpunkt ein Bild ab. **Die Bilder trotzdem ansehen**: Der Prüfer sieht Überlappung,
  nicht Gestaltung.
- **MathJax im Browser prüfen, wenn an `vendor/mathjax/` etwas ändert** —
  `node .claude/tools/pruef-mathjax.mjs http://localhost:8899/<seite>` zählt die
  gesetzten Ausdrücke und meldet 404 auf nachgeladene Bausteine. `verify_mathjax.js`
  im Pre-Flight setzt mit `mathjax-full` aus `node_modules` und sieht nicht, ob unter
  `vendor/` etwas fehlt — ein fehlender Baustein lässt eine *ganze* Seite ohne
  Formelsatz, ohne Fehlermeldung im Bild.
- **Text aus einem PDF ist nicht der Text im PDF.** Die Extraktion verliert stumm
  Hoch- und Überstriche: aus \(3^2\) wird `32`, aus \(0.\overline{6}\) wird `0.6` — beides
  plausibel und falsch. Wo eine mitgelieferte Musterlösung der eigenen Rechnung
  widerspricht, ist meist die Extraktion schuld. Nachweisen lässt sich ein Überstrich
  am Inhaltsstrom (waagrechte Linie genau über der Ziffer), eine Hochstellung an der
  kleineren Schriftgrösse im `visitor_text`-Rückruf. Rezept in
  `HOWTO-uebungspruefung.md` Schritt 0.
- **Keine erfundenen Quellen, Zitate oder Lehrplan-Stellen.** Im Zweifel: „muss
  verifiziert werden" schreiben, nicht raten.

## Schwesterprojekt TALS Physik — Übertrag per Todo, nicht direkt

- **Lesen ja, schreiben nie.** Claude Code darf `../tals-physik` jederzeit *lesen* —
  zählen, vergleichen, Zahlen für einen Übertrag holen. Geschrieben wird ausschliesslich
  in diesem Repo. Kein Edit, kein `git`-Befehl, kein Skriptlauf, der dort hineinschreibt.
- **Warum die Trennung nicht Vorsicht, sondern Struktur ist:** Der Harness lädt
  `CLAUDE.md` und `.claude/settings.json` des *primären* Arbeitsverzeichnisses. Aus einer
  Mathe-Session heraus gälten in Physik also Mathes Konventionen, während Physiks eigene
  `CLAUDE.md` und `STYLEGUIDE.md` stumm blieben — und Physiks bewusst enge Allowlist
  (nur `preflight.py` und ein paar `git`-Unterbefehle, **kein** freies `python3`/`sed`)
  wäre umgangen. Dazu kommt: die Werkzeugskripte hier leiten ihr Wurzelverzeichnis aus
  dem eigenen Dateipfad ab und schreiben rekursiv — aus dem falschen Ordner aufgerufen
  patchen sie das falsche Repo, in `acceptEdits` ohne Rückfrage.
- **Auch `--root PFAD` ist Schreiben.** `build-suchindex.py` nimmt den Schalter und
  schreibt damit ins andere Repo. Erlaubt ist er nur zusammen mit `--dry-run`
  beziehungsweise `--check`.
- **`scripts/abgleich.py` liest nur** und ist darum ausdrücklich erlaubt. Sein `[WARN]`
  im Pre-Flight ist der Anlass für einen Eintrag in der Warteschlange `OFFEN` (Liste in
  derselben Datei), nicht für einen Quer-Edit. Die Datei ist in beiden Repos gleich und
  steht in ihrer eigenen KERN-Liste mit Grundlinie `1.000`: Wer einen Eintrag hinzufügt
  oder streicht, macht sie ungleich, und das Schwesterrepo sieht es beim nächsten
  Pre-Flight. `--diff scripts/abgleich.py` zeigt, was drüben neu ist.
  **Vor jedem Hinzufügen oder Streichen eines Eintrags zuerst
  `python3 scripts/abgleich.py --diff scripts/abgleich.py`.** Ist die Datei gedriftet,
  liegt drüben vielleicht eine neuere Fassung — dann zuerst diese übernehmen und ihre
  Einträge sichten, erst danach die eigene Änderung. Nie blind anhängen, nie blind
  überschreiben: Am 28.09.2026 hatten beide Repos die Datei geändert, und jede
  Übernahme der ganzen Datei hätte den Eintrag der anderen Seite gelöscht.
- Änderungen, die auch ins Schwesterprojekt gehören (gemeinsame CSS-Muster, didaktische
  Module, `mathlib`/`physiklib`-Helfer, Nav-Logik), werden **nicht** quer-editiert,
  sondern als Eintrag in **`TODO-schwesterprojekt.md`** vermerkt (was, wo, warum) und
  später in einer Physik-Session von Hand portiert. So bleibt jedes Repo sauber.
- **Ein guter Eintrag ist nachgezählt, nicht geschätzt.** Vor dem Schreiben im Physik-Repo
  nachsehen und die konkreten Zahlen aufnehmen: wie viele Dateien betroffen sind, welche
  Sonderfälle es dort gibt, was dort anders heisst. Ein Eintrag, aus dem sich die
  Portiersitzung direkt abarbeiten lässt, ist die halbe Arbeit; einer aus Vermutungen
  kostet sie doppelt.

## Externe Ressourcen

Anbieter-Reihenfolge, Negativ-Liste und Verifikation: STYLEGUIDE / `HOWTO-externe-ressourcen.md`.
Max. Slots je Sektion und Playlist-vor-Einzelvideo dort nachschlagen. YouTube-Verifikation
per `web_fetch` auf die Playlist-URL (liefert Owner) — Präfix-Heuristik ist unzuverlässig.

## Arbeitsweise

- **Bei klarem Auftrag direkt umsetzen**, keine Rückfrage. Annahme nötig → inline kurz
  erwähnen. Bei echter Mehrdeutigkeit max. 3 gebündelte Fragen, dann starten.
- **Keine ungebetene Verbesserungs-Initiative.** Was nicht Teil des Auftrags ist, wird
  nicht mit-gepatcht. Kein Refactoring „weil eleganter".
- Mehr als 3 gleichartige Edits → ein Skript (`sed`/`python`), nicht N Einzel-Edits.
- Vor gezielten Edits `grep -n` + enger `view`, um Whitespace/Sonderzeichen exakt zu treffen.

## Automatik: Diffs nicht bestätigen + Commit nach jedem Durchgang

Dieses Repo läuft im Modus `acceptEdits` (siehe `.claude/settings.json`): Datei-Edits
werden ohne einzelne Diff-Bestätigung übernommen. Das Sicherheitsnetz ist Git — darum:

**Nach jedem abgeschlossenen Auftrag (= ein „Durchgang") automatisch, ohne Rückfrage:**

1. Pre-Flight über die geänderten Seiten laufen lassen.
2. **Nur wenn `ALLE CHECKS BESTANDEN`:** `git add -A` und `git commit` mit aussagekräftiger
   Message (Seite + was geändert wurde).
3. Schlägt der Pre-Flight fehl: **nicht committen**, Fehler melden und beheben, dann 1.
4. **Niemals `git push`.** Der Push bleibt manuell beim Auftraggeber.

## Was die Sandbox-Werkstatt (Chat) übernimmt

Abgeleitete Artefakte mit Spezial-Werkzeug bleiben besser im Chat, falls lokal nicht
installiert: **Anki-APKG-Rebuilds** (ZIP+SQLite — lokal ok, wenn Python steht),
**xlsx-Recalc** (braucht LibreOffice), **docx-Generierung** (braucht docx-Skill/Libs).
Inhalts-Edit lokal machen, abgeleitetes Artefakt danach regenerieren.
