# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

## Offen

> **Empfohlene Reihenfolge für eine Physik-Portiersitzung** (die Einträge stehen
> darunter neuestes zuerst, die Abhängigkeiten laufen aber andersherum):
> 1. **`.widget` zentralisieren** — Fundament; ohne das greift die Einbettungsregel nicht.
> 2. **Einbettung vereinheitlichen** nach demselben Verfahren (Klasse als Namensraum
>    behalten, Karten-Optik abgeben, in `.widget` wickeln). `.anim` NICHT entfernen.
> 3. **Gedankenstrich vor Formeln in Titeln** — unabhängig, rein textlich, schnell.
> 4. **Intervallgrenzen als Klammer** — braucht den Helfer in `physiklib.js`.
> 5. **SEO-Generator nachbessern** (`tex_weg`) — unabhängig, betrifft nur Metadaten.
> 6. **`mjTypeset`** — der älteste Eintrag, unabhängig von allem oberen.
>
> Für jeden Punkt gilt: nach dem Umbau im Browser nachmessen, nicht nur den Pre-Flight
> laufen lassen. Der Pre-Flight prüft Struktur, JS und MathJax — eine still entkleidete
> Bedienspalte besteht alle Checks.

- **2026-09-14 · Marke «TALS Physik» → «Physik begreifbar» · ganzes Physik-Repo ·
  warum:** Letzter offener Punkt des Domain-Umzugs (Mathes `DOMAIN-UMZUG.md`, Phase 5).
  Mathe heisst seit dem 10.08.2026 «Mathe begreifbar» (Mathe-Commit `6e88526`), und
  Mathes Menü nennt Physik schon «Physik begreifbar». Live am 14.09.2026 gemessen:
  `physik.begreifbar.ch` liefert `<title>TALS Physik — RLP-BM 2030</title>` und
  `og:site_name` «TALS Physik». Den ausführlichen Auftrag zum Einfügen in eine
  Physik-Sitzung enthält der Abschnitt «Auftrag Markenname Physik» weiter unten.

- **2026-09-01 · ~~Leitprogramme als zweites Format~~ — ERLEDIGT, nachgesehen am
  07.09.2026:** Physik hat inzwischen **fünf eigene Leitprogramme**
  (`leitprogramm-heizen`, `-ideale-gase`, `-vorwissen`, `-waermeausdehnung`,
  `-waermemenge`), eine eigene `leitprogramme.html`, ein eigenes
  `HOWTO-leitprogramme.md` und sechs Einträge in `build-seo.py`. Der Umfang deckt sich
  mit Mathes Erfahrungswert: dort 7 bis 10 Clips je Programm, hier 6 bis 11. **Nichts
  mehr zu portieren** — der Eintrag unten ist Geschichte und bleibt nur als Beleg
  stehen. Was noch fehlt, steht im nächsten Punkt.
  Zwei Unterschiede, die beim Übertragen einzelner Bausteine zählen: Physik benennt die
  Dateien `leitprogramm-<thema>.html`, Mathe `<thema>.html`; und Physiks Programme haben
  keine `.kap`-Sektionen mit `data-test`, sondern eine flachere Gliederung.

  Ursprünglicher Eintrag: Mathe hat
  seit dem 1.9.2026 neben den Clips ein zweites Format: eine eigenstaendige Seite zum
  selbstaendigen Durcharbeiten, mit Vorwissenstest, Kapiteln, eingebetteten Clips und
  Gesamttest. Die Mechanik ist duenn — eine Uebersichtsseite, ein Ordner, drei
  Eintraege in Generatoren — und darum billig zu uebernehmen, sobald Physik ein
  Leitprogramm hat. **Der Wert liegt nicht im Code, sondern in
  `HOWTO-leitprogramme.md`:** neun Punkte, die beim ersten Uebertrag noetig waren, mit
  je der Beobachtung, woran man merkt, dass der Punkt fehlt. Drei davon fielen erst im
  Browser auf und in keiner Pruefung — zerfallene Umlaute wegen fehlendem
  `<meta charset>`, eine weisse Kopfleiste ueber dunkler Seite, ein Clip, der vom
  Live-Stand kam statt aus dem Arbeitsverzeichnis. Wer in Physik dasselbe tut, spart
  sich diese drei Runden.

- **2026-09-07 · Rechner-Clips als eigener Strang · `scripts/build-clips.py`
  (`rechner_svg`, Feld `werkzeug`) + Drehbuecher · warum:** Mathe hat inzwischen
  **19 Clips zum TI-30X Pro MathPrint**; Physik hat **null** — im Physik-Repo trägt
  keiner der 88 Drehbuecher `werkzeug: true`, und `scripts/build-clips.py` kennt
  weder den Elementtyp `rechner` noch das Feld. Nachgezählt am 07.09.2026:
  `grep -c rechner_svg scripts/build-clips.py` gibt 0 Treffer im Code (der eine
  Treffer auf «werkzeug» ist das Wort «Diagrammwerkzeug» in einem Kommentar).

  **Zwei Generator-Bausteine sind die Voraussetzung**, beide in Mathes
  `scripts/build-clips.py`:
  1. `rechner_svg(el, theme)` — zeichnet die Anzeige (vier Zeilen à 16 Zeichen,
     Ergebnis rechtsbuendig, `[a|b]` zweistoeckig, Tastenband unten). Rund 90 Zeilen,
     haengt nur an `theme` und `entschaerfen`, also ohne Anpassung uebertragbar.
     Plus der `elif typ == "rechner"`-Zweig im Element-Dispatch.
  2. Feld `werkzeug: true` — sortiert den Clip ans Ende seiner Reihe und faerbt die
     Zeile orange. Betrifft `build-clips.py` und `build-clips-einbau.py`.

  **Wofuer es sich in Physik lohnt** (aus Mathes 19 Clips uebertragbar, mit Zielseite):
  - **Konstanten-Menue** (`2nd constants`, 20 Werte, NIST 2018) — Mathe hat den Clip
    auf `g1-4` gebaut, weil dort die Zehnerpotenzen stehen. In Physik gehoert er
    inhaltlich hin: `g = 9.80665` fuer `p4-2`/`p4-3`, `R` und `k` und `atm` fuer
    `p5-1`/`p5-2`, `e` und `c` fuer `p6-2`. **Dort ist er mehr wert als in Mathe.**
  - **num-solv fuer Sachaufgaben** (Mathe `g2-1`): das Beispiel ist bereits eine
    Waermebilanz (Mischtemperatur, Startwert zwischen den beiden Temperaturen). Es
    gehoert eigentlich auf `p5-2-waerme` — in Mathe steht es nur, weil es dort um das
    Aufstellen von Gleichungen geht.
  - **`Expr=` / Auswerten von Ausdruecken** (Mathe `s4-2a`): eine Formel einmal
    eintippen, der Rechner fragt nach `x, y, z, …`. Fuer Physik der naheliegendste
    Griff ueberhaupt — jede Aufgabenserie rechnet dieselbe Formel mit anderen Zahlen.
  - **mode-Menue, EE/ENG, signifikante Stellen** (Mathe `g1-4`): Physik hat mit
    `p0-2-vorsilben-ee` schon einen Clip zum selben Stoff, aber ohne Rechneranzeige —
    er nennt die EE-Taste im Text und zeigt sie nicht. Der waere der erste Kandidat
    zum Nachruesten, sobald `rechner_svg` steht.

  **Nicht uebertragen:** die rein mathematischen (poly-solv, sys-solv, logBASE,
  Funktionstabelle, ggT/kgV, DMS, Haeufigkeiten, op1/op2) — die haben in Physik
  keine Seite.

  **Belegquelle fuer jede Rechnerangabe** ist das deutsche TI-Handbuch (68 Seiten,
  Text mit `pypdf`); Mathes `CLAUDE.md`-Regel «nichts erfinden, was am Geraet
  nachgeschlagen gehoert» gilt dort genauso. Was das Handbuch **nicht** hergibt und
  darum in keinen Clip kam: die Bildschirmmaske des numerischen Loesers mit unterer
  und oberer Grenze, die Kurzbezeichnungen im NAMES-Menue, die Einheiten-Glyphen im
  UNITS-Menue, und ob dieses Modell ueberhaupt Matrix und Vektor kann.

- **2026-09-01 · Clip-Buehne: Scrollsperre und Fokusrueckgabe · `physiklib.js`
  (`clipBuehne`/`clipZu`) · warum:** In Mathe scrollte die Seite unter dem offenen
  Overlay weiter — beim Schliessen war man an einer anderen Stelle als vorher —, und der
  Fokus landete am Seitenanfang statt auf dem Knopf, der die Buehne geoeffnet hat. Zwei
  kleine Ergaenzungen: `document.body.style.overflow = 'hidden'` beim Oeffnen und
  zuruecksetzen beim Schliessen, dazu `document.activeElement` merken und wieder
  fokussieren. **Nur relevant, sobald Physik Clips hat** — dort gibt es die Buehne
  heute nicht.

- **2026-08-31 · MathJax-Erweiterungen vollstaendig mitliefern · `vendor/mathjax/input/tex/extensions/`
  · warum:** In Physik liegt dort **genau eine** Datei (`boldsymbol.js`) — dieselbe Luecke,
  die in Mathe eine ganze Seite lahmgelegt hat. MathJax laedt TeX-Erweiterungen erst bei
  Bedarf nach; faellt eine aus, bleibt **die komplette Seite** ohne Formelsatz, ohne
  Fehlermeldung im Bild. In Mathe traf es `g1-2`: ein einziges `\textcolor` forderte
  `color.js` an, das fehlte, und alle 329 Ausdruecke der Seite standen als roher
  LaTeX-Text da.
  **Nachgezaehlt am 31.8.2026:** Physik hat 23 Seiten, und **keine einzige** benutzt
  derzeit `\textcolor`, `\cancel`, `\bbox`, `\class`, `\enclose`, `\unicode` oder `\ce`.
  Der Fehler ist dort also **noch nicht aktiv** — aber ein einziges `\textcolor` in einer
  Live-Anzeige genuegt, und die Seite ist stumm. In Mathe stand die Farbkopplung per
  `\textcolor` sogar in der CLAUDE.md als Empfehlung.
  **So beheben** (aus dem Mathe-Repo heraus, aber im Physik-Repo ausfuehren):
  `cp node_modules/mathjax-full/es5/input/tex/extensions/*.js vendor/mathjax/input/tex/extensions/`
  und `all-packages.js` wieder loeschen — das ist ein Sammelbuendel von 212 kB, das der
  Autoload nie anfordert. Es bleiben 34 Dateien, 340 kB, alle nur bei Bedarf geladen.
  **Pruefen** mit `.claude/tools/pruef-mathjax.mjs` (siehe naechster Eintrag): Die Zahl
  der `mjx-container` muss zur Zahl der Ausdruecke passen und es darf keine 404 geben.
  `verify_mathjax.js` im Pre-Flight sieht das **nicht** — es setzt mit `mathjax-full` aus
  `node_modules` und schaut nie in `vendor/`.

- **2026-08-31 · Zwei Pruefwerkzeuge mitnehmen · `.claude/tools/pruef-mathjax.mjs`,
  `.claude/tools/pruef-clip.mjs` · warum:** Beide sind projektunabhaengig.
  `pruef-mathjax.mjs` laedt eine ausgelieferte Seite im Browser, zaehlt die gesetzten
  Ausdruecke und meldet jede fehlgeschlagene Anfrage — genau die Luecke, die der
  Pre-Flight strukturell nicht sehen kann. `pruef-clip.mjs` ist nur noetig, wenn Physik
  Clips bekommt. Beide brauchen Playwright, das in Mathe schon installiert ist.

- **2026-08-31 · Clip-Eintrag unten aktualisiert sich mit:** Die Mechanik ist seit dem
  30.8. deutlich gewachsen — 50 Clips (52:54 min), Formelsatz in LaTeX statt eigener
  Schreibweise, Elementtyp `graf` fuer Koordinatenbilder, Bibliothek nach Lektion und
  Reihe unterteilt, Vertonung mit Piper. Wer portiert, nimmt den Stand von heute, nicht
  den vom 30.8.
  **Nachtrag 07.09.2026 — beide Clip-Eintraege sind ueberholt.** Physik hat inzwischen
  **79 Drehbuecher**, ein eigenes `HOWTO-clips.md` und einen eigenen `pruef-clip.mjs`,
  der Mathes Fassung an einer Stelle *voraus* war (siehe „Rueckuebertrag" unten). Der
  Port ist also nicht mehr die Frage; was bleibt, sind einzelne Bausteine, die nur eine
  Seite hat. Die stehen unten im Abschnitt „Clip-Generator: drei Bausteine".

- **2026-08-30 · Clips: Verfahren uebernehmen, sobald Physik welche hat · `clips/`,
  `scripts/build-clips*.py`, `style.css`, `physiklib.js`, `nav.js`, `clips.html` ·
  warum:** In Mathe steht seit dem 30.8.2026 die vollstaendige Mechanik fuer kurze,
  HTML-Animationen (inzwischen vertont). Sie ist projektunabhaengig gebaut und laesst sich uebernehmen,
  ohne etwas neu zu erfinden. ~~Physik hat derzeit keine Clips~~ — **ueberholt: am
  07.09.2026 sind es dort 79 Drehbuecher.** Der Eintrag ist damit Geschichte, kein
  offener Rueckstand; die fuenf Punkte darunter bleiben als Fallstrick-Liste lesenswert.
  **Was zu uebertragen waere:** `clips/` samt `themes/` und `vorlage.json`,
  `scripts/build-clips.py` (Drehbuch → Clip) und `scripts/build-clips-einbau.py`
  (Clip → Lektionsseite und Bibliothek), die Abschnitte `.clip-*` aus `style.css`, der
  Helfer `clipStart` (in Mathe in `mathlib.js`, in Physik nach `physiklib.js`), der
  Nav-Eintrag im Menue *Nachschlagen*, je eine Zeile in `build-seo.py` und
  `build-suchindex.py`, sowie die Clip-Checks im Pre-Flight. Dazu `HOWTO-clips.md` und
  STYLEGUIDE §6.4.
  Fuenf Punkte, die in Mathe Arbeit gekostet haben:
  1. **`clips/` muss genau eine Ebene unter der Wurzel liegen.** Die Clips ziehen die
     Schriften per `@import url("../schriften.css")`. Tiefer verschoben faellt die Buehne
     still auf Georgia zurueck, ohne dass etwas bricht.
  2. **`lektion` ist eine Liste.** Ein Clip gehoert oft auf mehrere Seiten. Der erste
     Mathe-Clip steht auf `g2-2b` und `s2-2a`. Mit Einzelwert muesste man ihn
     duplizieren, und zwei Kopien laufen auseinander.
  3. **Kein `<iframe>` beim Seitenaufruf** — nur eine Startkarte, der Klick setzt den
     Rahmen ein. Sonst laufen bei mehreren Clips alle gleichzeitig los. Der Rahmen
     braucht `padding-bottom: calc(56.25% + 60px)`: 16:9 plus die 60 px hohe
     Bedienleiste des Clips, sonst schrumpft die Buehne.
  4. **Das Transkript entscheidet ueber die Auffindbarkeit.** Von einer Animation sieht
     eine Suchmaschine gar nichts. Die Klasse `clip-transkript` darf nicht in
     `SKIP_CLASSES` von `build-suchindex.py` landen — in Mathe nachgeprueft: danach ist
     der Sprechertext ueber die Volltextsuche auffindbar.
  5. **`verify_js_runtime.js` verträgt keine Wurzelseiten.** Es ersetzt
     Bibliotheks-Einbindungen der Form `src="../nav.js"`, rechnet also mit Seiten genau
     eine Ebene tief. `clips.html` — und uebrigens auch `glossar.html` und
     `formelsammlung.html` — erzeugen dort einen falschen `[FEHLER]`. In Mathe bekommt
     das Skript darum nur noch Themenseiten zu sehen; derselbe Filter gehoert in Physiks
     Pre-Flight. Ebenso die Erkennung von `src="nav.js"` ohne `../` im Skelett-Check.

- **2026-08-10 · Umzug auf `physik.begreifbar.ch` · ganzes Physik-Repo · warum:**
  Mathe liegt seit dem 10.8.2026 auf `mathe.begreifbar.ch`. Die DNS-Seite ist für
  Physik **bereits erledigt**: `physik` steht als CNAME auf `go4exercises.github.io.`
  (TTL 300), und die Domain ist auf GitHub verifiziert — der TXT-Record
  `_github-pages-challenge-go4exercises` deckt die Subdomains mit ab. Es fehlt nur
  noch die Repo-Seite. **Bis dahin zeigen die drei Physik-Querlinks aus Mathe
  (`nav.js`) sowie die Verweise in Mathes `glossar.html` und `formelsammlung.html`
  auf eine Adresse, die noch nicht ausliefert.**
  **Massnahme in Physik:** `CNAME` im Repo-Root mit `physik.begreifbar.ch` (eine
  Zeile, LF, kein BOM), pushen, Settings → Pages prüfen, **Enforce HTTPS** setzen.
  Danach die Basis-URL im dortigen SEO-Skript umstellen und den Generator laufen
  lassen, die Rück-Querlinks auf `https://mathe.begreifbar.ch/` setzen (Kopfzeile,
  Mobilmenü, Über-Panel, Glossar, Formelsammlung) und die Namensnennung im
  Lizenzblock nachziehen. Reihenfolge und Begründung stehen in Mathes
  `DOMAIN-UMZUG.md`, Phase 5.
  **Prüfen nach dem Port:** `https://physik.begreifbar.ch/` liefert über HTTPS aus,
  `canonical` zeigt auf die neue Domain, `sitemap.xml` erreichbar, und die
  Querlinks in **beide** Richtungen landen auf einer Seite statt auf einem 404.

- **2026-08-10 · ToC markiert den aktiven Abschnitt sofort · `nav.js`,
  `buildToC()` · warum:** Die Markierung lief allein über einen
  `IntersectionObserver` mit `rootMargin: '-20% 0px -70% 0px'`. Der meldet nur,
  wenn eine Überschrift dieses schmale Band durchquert — beim Laden, nach einer
  Sprungmarke und nach schnellem Scrollen blieb im ToC darum gar nichts markiert.
  In Physik steht dieselbe Konstruktion (gleicher `rootMargin`), der Fehler ist
  also derselbe.
  **Massnahme in Physik:** Observer ersetzen durch `markiereTocAktiv()` — die
  letzte Überschrift, deren `getBoundingClientRect().top` unter 30 % der
  Fensterhöhe liegt, sonst die erste — und diese Funktion am Ende von
  `buildToC()`, bei `scroll` (auf `requestAnimationFrame` gedrosselt) und bei
  `hashchange` aufrufen. Die Horcher vor dem Binden je einmal abmelden, damit ein
  zweiter `buildToC()`-Aufruf sie nicht doppelt registriert. Die bestehende
  Klick-Markierung auf den `.toc-link` bleibt unverändert.
  **Prüfen nach dem Port:** beim Laden ist ein Eintrag markiert; Sprung auf einen
  Anker markiert dessen Abschnitt; beim Rollen wandert die Markierung lückenlos
  durch alle Überschriften. Seiten ohne ToC (Startseite) dürfen nicht brechen.

- **2026-08-03 · Animations-Karte `.widget` zentralisieren und Einbettung
  vereinheitlichen · `style.css` + Themenseiten · warum:** In Mathe lagen
  `.widget`, `.widget-header`, `.widget-header h3/p` und `.widget-body` als
  wortgleiche Kopie in 35 von 45 Themenseiten statt in `style.css` — `TEMPLATE.html`
  benutzte die Klassen, ohne sie zu definieren. Dazu standen 26 Animationen ganz
  ohne Rahmen im Textfluss, mit einer freistehenden `.widget-titelzeile`; auf
  Seiten mit gerahmten Nachbarn fiel das als Stilbruch auf, und das Hinweispaar
  brach dort auf eine zweite Zeile um.
  **Massnahme in Physik:** prüfen, ob `.widget` dort ebenfalls lokal kopiert ist
  (`grep -c '^\.widget {' themen/*.html`), zentralisieren und die lokalen Kopien
  entfernen. Achtung auf die Kaskade: die lokale Kopie überstimmt
  `.widget-titelzeile h3 { margin:0 }`; zentral gewinnt die Titelzeilen-Regel, was
  die Kopfzeile um 3 px kürzt (richtig so). Danach freistehende Animationen in die
  Widget-Form bringen. Regel dazu in STYLEGUIDE §2.10 (Mathe).
  **Nachtrag 2026-08-03 (Mathe fertig):** Statt die Karten-Optik je Behälterklasse
  einzeln zurückzunehmen, steht in Mathe jetzt eine zentrale Regel in `style.css`:
  `.widget-body > .anim { background:none; border:0; border-radius:0; padding:0;
  margin:0; box-shadow:none; }`. Sie löst das Rahmen-im-Rahmen-Problem für alle
  `.anim`-Karten auf einmal, ohne `.anim` und seine Nachfahren-Regeln anzutasten —
  in Physik dieselbe Regel setzen, bevor die erste `.anim`-Karte gewickelt wird.
  Zweiter Fallstrick aus dem Mathe-Durchgang: liegt die Titelzeile mit dem
  Hinweispaar **in einem Panel eines Tab-Umschalters**, verschwindet das Paar beim
  Umschalten. Titelzeile über den Umschalter heben, nicht in ein Panel.

- **2026-08-03 · Gedankenstrich an Formeln in Titeln beseitigen ·
  alle Themenseiten · warum:** Gerendert klebt der Gedankenstrich an der Formel und
  liest sich als Vorzeichen — aus «Labor — \(x^2 + c\)» wird optisch
  \(-x^2 + c\). In Mathe in 75 Titeln ersetzt (h2, h3, `.anim-titel`,
  `.block-titel`, `.aufg-titel-text`), Regel in STYLEGUIDE §2.8.
  **Massnahme in Physik:** dasselbe Muster suchen und ersetzen —
  `[—–]\s*\\(` in Titel-Zeilen, Ersatz `: \(`; nach `?`/`!` entfällt der
  Strich ersatzlos. **Fliesstext nicht anfassen:** dort ist der Strich ein
  Satzzeichen mit grammatischer Funktion.
  **Nachtrag 2026-08-03:** Die Regel deckte anfangs nur den Strich *vor* der Formel
  ab. Der umgekehrte Fall `\\)\s*[—–]` wirkt genauso und hängt das Minus ans
  Formelende — in Physik **beide** Muster suchen. Dort hilft kein Ersatzzeichen:
  die Tätigkeit wandert an den Anfang, die Formel ans Ende («Gerade \(f(x)=ax+b\)
  — Achsenschnitte erkunden» → «Achsenschnitte erkunden: Gerade \(f(x)=ax+b\)»).
  Ist der erste Teil nur ein Etikett (`⚠ Wichtig`, `🟢 Beispiel 2`), nicht
  umstellen, sondern Doppelpunkt. **Nur direkter Kontakt zählt:** steht zwischen
  Formel und Strich noch ein Wort, klärt es die Lesart und der Titel bleibt —
  ein weiter gefasster Suchlauf produziert Fehltreffer.

- **2026-08-02 · Intervallgrenzen am Zahlenstrahl als Klammer statt als Punkt ·
  `physiklib.js` + betroffene Themenseiten · warum:** In Mathe markieren Canvas
  eine Intervall- oder Lösungsmengengrenze neu mit derselben Klammer wie die
  Intervallschreibweise daneben (`[`, `]`) statt mit gefülltem/hohlem Punkt —
  Bild und Schreibweise sagen damit dasselbe. Neuer Helfer `intervallKlammer(ctx,
  x, y, oeffnetRechts, opt)` in `mathlib.js`, dokumentiert in STYLEGUIDE §2.7.
  Die Klammer steht immer symmetrisch zur Achse und wird weiss unterlegt; wo
  `drawGrid` Achsenzahlen setzt, gehört sie **nach** die Zahlen gezeichnet.
  **Massnahme in Physik:** Helfer 1:1 nach `physiklib.js` übernehmen (farbneutral,
  Standardfarbe `#374151`), dann die Seiten prüfen, die eine Grenze auf einer
  Achse zeichnen — in Mathe waren es drei (`g1-2 cv-iv`, `g2-1 cv-ungl`,
  `s2-2b ld-canvas`), gefunden über `.arc(` im Umfeld von «Strahl / Zahlengerade /
  Lösungsmenge / Randpunkt / Grenze».
  **Nicht umstellen**, wo es keine Intervallgrenze ist: einzelner ausgeschlossener
  Wert (Polstelle), Lösungspunkte, Wertemarken — dort bleibt der Punkt richtig.
  **Begleittexte mitziehen:** Erklärzeilen und Hinweispaare, die von «gefülltem»
  oder «hohlem Punkt» sprechen, werden sonst falsch.

- **2026-08-02 · Drei Verbesserungen am SEO-Generator zurück nach Physik ·
  `scripts/build-seo.py` · warum:** Mathe hat den Generator aus Physik (Commit
  `fc4ed40`) übernommen und dabei drei Dinge nachgebessert, die in Physik
  ebenfalls greifen würden:
  1. **`tex_weg` verstümmelt Formeln in der `teaches`-Liste.** Die alte Fassung
     löscht `^` und `_` mit weg, aus `a^x` wird «ax» und aus `\log_a(b)` wird
     «a(b)» — in Metadaten schlicht falsch. Mathe entfernt jetzt nur `{}$` und
     den Backslash und lässt `^`/`_` stehen; dazu die Makros `log`, `ln`, `lg`,
     `sin`, `cos`, `tan`, `setminus`. In Physik betrifft das u.a. die
     Kompetenzen mit Formelanteil (`v = \Delta s / \Delta t` u.ä.) — nachprüfen.
  2. **Breadcrumb vierstufig.** Mathe hat zwei Fachbereiche, deshalb
     Site → Fach → Lerngebiet → Teilgebiet. Für Physik reicht dreistufig wie
     bisher — nur übernehmen, falls dort je eine zweite Ebene dazukommt.
  3. **Bild-Assets reproduzierbar.** `.claude/tools/build-bilder.mjs` erzeugt
     `favicon-32.png`, `apple-touch-icon.png` und `og-bild.png` aus `favicon.svg`
     bzw. einer HTML-Vorlage (Playwright, Google Fonts). In Physik entstanden
     die PNGs von Hand; mit dem Skript liessen sie sich nach einer Farb- oder
     Wortlautänderung ohne Handarbeit neu bauen. Vorlage 1:1 übernehmen, nur
     Farbe (`#1a4f8a` → Bernstein) und Wortlaut tauschen.

- **2026-06-24 · MathJax-Re-Typeset serialisieren (zentraler Helfer `mjTypeset`) ·
  `physiklib.js` + alle Themenseiten · warum:** Einzelne Formeln rendern sporadisch
  leer — aber nur beim **Hard-Refresh**, nicht beim Zurückblättern aus dem bfcache.
  Ursache: seiten-eigene `MathJax.typesetPromise(…)`-Aufrufe beim Laden kollidieren
  mit MathJax' initialem Seiten-Render (Race), zusätzlich überlappen sich Re-Typesets
  auf denselben Elementen — verstärkt durch `svg.fontCache:'global'`.
  **Massnahme (in Mathe umgesetzt):**
  1. In `mathlib.js` (Physik: `physiklib.js`) den Helfer `mjTypeset(els)` ergänzen —
     serialisiert alle Durchläufe über eine Promise-Kette, deren erste Stufe auf
     `MathJax.startup.promise` wartet (läuft also nach dem Initial-Render). Code 1:1
     aus `mathlib.js` (Abschnitt „MathJax: serialisiertes … Typesetting") übernehmen,
     ist farb-/projektneutral.
  2. Alle direkten `[window.]MathJax.typesetPromise(args)`-Aufrufe (inkl. ihrer
     redundanten `if (window.MathJax && …typesetPromise)`-Guards) durch
     `mjTypeset(args)` ersetzen; `mjTypeset()` ohne Argument = ganze Seite.
     Guard-Tokens (`!MathJax.typesetPromise` in Early-Returns) bleiben unverändert.
  3. Nur bei dynamisch (per `innerHTML`) geänderter Mathematik aufrufen — statische
     HTML-Formeln rendert MathJax beim Laden selbst (kein erneutes Typeset).
  Doku-Stellen, die in Physik analog nachzuziehen sind: `TEMPLATE.html` (Helfer-Liste)
  und `HOWTO-neue-themenseite.md` (Troubleshooting „Formeln rendern sporadisch leer").
  Verifikation in Mathe: Pre-Flight-Tiefencheck `verify_mathjax` 5698 Ausdrücke / 0
  Fehler, `verify_js_runtime` ok. Render-Check 1280/360 px ist in Mathe seither
  laufend erfolgt (Playwright lokal, `npm run shots`); in Physik vor dem Abschluss
  analog nachholen.

- **Slider-Wert-Farbkopplung (CSS-Muster, aus Audit-Paket 4).**
  Auf mehreren Seiten färbt die seiten-lokale Regel `.sl-val { color: var(--blau) }`
  **alle** Slider-Werte blau — auch die von orange/grünen Reglern (akz-orange/-gruen).
  Der Wert passt dann nicht zu Reglerfarbe und (falls vorhanden) zur farbcodierten
  Live-Formel. **Massnahme (in Mathe umgesetzt auf g3-1, s1-2, s1-3, s2-2c, s3-5):**
  je Seite zwei Regeln nachziehen —
  `.sl-grp.akz-orange .sl-val, .sl-row.akz-orange .sl-val { color: var(--orange); }`
  und analog für `.akz-gruen`. Farbneutral, kein JS. In Physik dort prüfen, wo ein
  Widget mehrere Regler mit unterschiedlichen akz-Farben hat (Amber/Bernstein-Palette
  entsprechend). Verwandt: Live-Formel-Werte via `.tx-…`-Spans an dieselben Farben koppeln.

## Auftrag Markenname Physik (2026-09-14) — zum Einfügen in eine Physik-Sitzung

> Nachgezählt am 14.09.2026 im Physik-Repo, Stand `86a7206`, nur lesend.

**Ziel:** Die Marke «TALS Physik» heisst überall, wo sie als Name des Lehrmittels steht,
**«Physik begreifbar»** — passend zur Domain `physik.begreifbar.ch` und zu «Mathe
begreifbar». Vorbild ist Mathe-Commit `6e88526` (891 Stellen, ein Commit).

**Bestand:** 349 × «TALS Physik» in 102 Dateien.

| Ort | Stellen | Art |
|---|---|---|
| `themen/*.html` (18 Seiten) | 125 | je 7–8: `<title>`, `og:site_name`, `og:title`, JSON-LD (3×), Fusszeile — der Kopf ist SEO-Block, generiert |
| `downloads/themen/*/` (Handout, Aufgabenserie, Teste-dich-selbst) | 64 | Titel, Kopf- und Fusszeile der Druckseiten |
| `scripts/` | 44 | `build-seo.py` 9 (Tabelle `SEITEN`, WebSite-Name Z. 370/379), `gen_stubs.py` 2, 10 × `build_apkg_*.py` je 3, `build-suchindex.py` 1, `check_identifier_collisions.py` 1, `abgleich.py` 1 |
| `.quellen/formelsammlung/` | 40 | `formelsammlung.tex` 7, 8 Prüfdateien je 4, `README-Build.md` |
| Wurzel | ≈ 50 | `rechtliches` 7, `index` 6, `feedback` 5, `glossar`/`formelsammlung`/`clips`/`leitprogramme` je 4, `nav.js` 3, `sonnenfinsternis-12-08-2026.html` 2, je 1: `suche.js`, `suchindex.js`, `style.css`, `physiklib.js`, `robots.txt`, `favicon.svg` (`aria-label`), `LICENSE` |
| Doku | 6 | `README`, `CLAUDE`, `SETUP`, `STYLEGUIDE`, `HOWTO-neue-themenseite` je 1 |

Dazu nennt Physik **Mathe noch beim alten Namen**: `nav.js:141` Linktext «TALS
Mathematik» (→ «Mathe begreifbar»), `README.md:5`, `style.css:4` (Kommentar).

**Vorgehen**

1. Ersetzen per Skript, nicht von Hand. Vorher `grep -rIc "TALS Physik"` als Liste
   sichern, nachher dieselbe Zählung: 0 ausserhalb der Ausnahmen unten.
2. **«TALS» bleibt, wo es die Zielgruppe benennt, nicht die Marke** (wie in Mathe):
   - Fusszeile: nur der fette Name wechselt, «— Lernmaterial für die Berufsmaturität
     Technik, Architektur, Life Sciences» bleibt.
   - OG-Bild: die Vorspann-Zeile `ew` («… — TALS») bleibt.
   - `feedback.html`: `<title>Kontakt &amp; Feedback — TALS</title>` und die
     Projekterkennung «TALS-Mathe UND TALS-Physik» bleiben (gemeinsame Seite beider Fächer).
   - Der Repo-Name **«TALS-Physik»** (54 Stellen, mit Bindestrich) bleibt.
3. **Nicht umbenennen:**
   - **Anki-Decks.** Die 10 `downloads/themen/*/ankideck.apkg` heissen «TALS Physik::…».
     `build_apkg_*.py` erzeugt die GUIDs mit `random.seed(hash(deck_name))`: Ein neuer
     Deckname gibt beim Import **Dubletten statt Umbenennung**, und `hash()` ist pro
     Prozess gesalzen. Decknamen in den Skripten und die `.apkg` bleiben — genau wie in
     Mathe. (Docstrings dürfen mit.)
   - **Geteiltes Werkzeug:** `build-suchindex.py` (Kopfkommentar im Suchindex),
     `check_identifier_collisions.py`, `abgleich.py`. Diese Dateien werden mit Mathe
     abgeglichen; eine einseitige Änderung erzeugt Drift. `abgleich.py` Z. 130 zitiert
     ausserdem den Abschnittstitel «Schwesterprojekt TALS Physik» aus *Mathes*
     `CLAUDE.md` — der ist kein Physik-Text. Soll das Werkzeug mit, gehört es als
     Eintrag in die Warteschlange `OFFEN` in `abgleich.py`.
   - Historie (Changelog-Einträge, Protokolle): dokumentiert den damaligen Stand.
4. **Formelsammlung-Quelle:** Die `.tex`-Dateien nur umbenennen, wenn das PDF danach nach
   `README-Build.md` neu gebaut wird — sonst weichen Quelle und ausgeliefertes PDF
   voneinander ab. Beides oder nichts; Entscheidung im Commit nennen. (Nebenbei:
   `formelsammlung.tex` Z. 5 und 54 zeigen noch auf `go4exercises.github.io/TALS-Physik`.)
5. **Generiertes neu erzeugen:** `scripts/build-seo.py` (danach `--check` sauber, zwei
   Durchgänge wie in Mathe), `scripts/build-suchindex.py`. `gen_stubs.py` mitziehen,
   damit neue Seiten den neuen Namen bekommen.
6. **Bilder:** `.claude/tools/build-bilder.mjs` — `<h1>Physik <span>…</span></h1>` wird
   `<h1>Physik begreifbar <span>…</span></h1>`; Mathe brauchte dafür
   `h1 span { display:block }`, weil der Name länger ist. `og-bild.png`,
   `favicon-32.png`, `apple-touch-icon.png` neu bauen (einmalig Netz für die Schriften)
   und **das Bild ansehen**.
7. **Prüfen:** Pre-Flight über alle Themenseiten; Zählung aus Schritt 1; Druckseite und
   Startseite im Browser bei 1280 und 360 px (längerer Name im Kopf). Nach dem Push
   (Cache 600 s): `<title>`, `og:site_name`, JSON-LD `name` und `og-bild.png` live.
8. Committen, **nicht pushen**. Wenn es live ist, in Mathe `DOMAIN-UMZUG.md` Phase 5
   abhaken (Mathe-Sitzung) und diesen Abschnitt nach «Erledigt» verschieben.

## Erledigt / portiert

### Drittanbieter entfernen (Eintrag vom 30.08.2026) — **in Physik erledigt**

Nachgemessen im Physik-Repo am 31.08.2026, Stand `e7745c2` (nur gelesen):

| | |
|---|---|
| HTML-Dateien | 53 |
| mit `googleapis` | **0** |
| mit `jsdelivr` | **0** |
| mit `schriften.css` | 52 |
| mit `vendor/mathjax` | 50 |
| `schriften/`, `vendor/` | vorhanden |
| `check_keine_fremdhosts` im Pre-Flight | vorhanden |

Live geprüft: `physik.begreifbar.ch` liefert `schriften.css` aus, kein `googleapis`, kein
`jsdelivr`. `rechtliches.html` ist nachgezogen — die Erwähnung von Google Fonts steht dort
in einer Verneinung („werden von dieser Website selbst ausgeliefert, nicht über Google
Fonts oder ein CDN").

Auch der Sonderfall aus dem Eintrag ist entschieden: `downloads/wellenexperimente-standalone.html`
gibt es nicht mehr — die Datei hing an einem `physiklib.js`, das im `downloads`-Ordner gar
nicht lag, und war von keiner Seite verlinkt.

**Damit ist die ganze Domain drittanbieterfrei**: `begreifbar.ch` (seit 31.08.),
`mathe.begreifbar.ch` und `physik.begreifbar.ch`.

<details>
<summary>Der ursprüngliche Eintrag, zur Nachvollziehbarkeit</summary>

- **2026-08-30 · Drittanbieter entfernen: Schriften und MathJax lokal ausliefern ·
  alle Physik-Seiten · warum:** In Mathe geht seit dem 30.8.2026 keine Anfrage mehr aus
  dem Haus. Physik hat exakt dasselbe Muster und denselben Fussbereich, der
  «Keine Cookies · Kein Tracking» verspricht. Solange Google Fonts und das MathJax-CDN
  drinstehen, stimmt die Aussage dort nicht.

  **Umfang, im Physik-Repo nachgezaehlt (nur gelesen, nichts angefasst):** 54 HTML-Dateien,
  davon **53 mit `fonts.googleapis.com`** (17 `themen/`, 31 `downloads/`, 5 im Wurzel-
  verzeichnis) und **50 mit `cdn.jsdelivr.net/npm/mathjax@3`**. Die Schriftanforderung ist
  zeichengleich mit der in Mathe: dieselben drei Familien, dieselben Schnitte, dieselben
  drei Varianten der Link-Zeile. `node_modules/mathjax-full` liegt dort in **3.2.2** —
  dieselbe Version, die das CDN liefert, `vendor/mathjax/` laesst sich also genauso
  aus node_modules bauen.

  **Massnahme:** `schriften/`, `schriften.css`, `vendor/mathjax/` sowie
  `scripts/schriften-lokal.py` und `scripts/mathjax-lokal.py` aus Mathe uebernehmen. Die
  beiden Skripte sind repo-agnostisch, sie leiten die Wurzel aus dem eigenen Pfad ab.
  Fuenf Punkte, an denen es sonst klemmt:

  1. **Griechisch mitnehmen.** Im Physik-Repo stehen **105 griechische Zeichen ausserhalb
     von MathJax** in 18 Dateien: Ω 27x, Δ 21x, ϑ 11x, α 11x, λ 9x, π 9x, ρ 4x, μ 4x, dazu
     φ, γ, ω, η, Π, ν. Alle im Grundblock U+0370–03FF — der `greek`-Subset von Fontsource
     reicht, `greek-ext` (polytonisch) kommt nicht vor, kyrillisch auch nicht. Ohne den
     Subset fallen die 105 Stellen auf eine Systemschrift zurueck.
  2. **`boldsymbol` mitkopieren.** **20 der 50 Seiten** setzen
     `loader: { load:['[tex]/boldsymbol'] }`. MathJax laedt Erweiterungen relativ zum Pfad
     der Startdatei nach, also muss `vendor/mathjax/input/tex/extensions/boldsymbol.js`
     daneben liegen, sonst bricht der Formelsatz auf diesen 20 Seiten.
  3. **Das Kontextmenue vollstaendig bedienen.** Rechtsklick auf eine Formel bietet
     *Math Settings → Math Renderer → CHTML* und *Accessibility*. Fehlt `output/chtml.js`
     samt `output/chtml/`, scheitert der Wechsel still — aber MathJax merkt sich die Wahl
     in `localStorage`, und ab dem naechsten Aufruf steht auf **allen** Seiten roher
     LaTeX-Quelltext; ohne gerenderte Formel gibt es dann auch kein Kontextmenue mehr, um
     es zurueckzustellen. Fuer die Sprachausgabe braucht es zusaetzlich `input/mml.js` samt
     `input/mml/`, `a11y/` und `sre/mathmaps/` (in Mathe `base`, `de`, `en`). Zusammen
     rund 2.3 MB, die fuer normale Besucher 0 Byte kosten — sie werden nur geholt, wenn
     jemand im Menue wirklich etwas umstellt. **Nichts davon faellt beim Laden oder im
     Pre-Flight auf**; in Mathe kam beides erst heraus, als die Menuepunkte im Browser
     wirklich angestossen wurden.
  4. **`downloads/wellenexperimente-standalone.html` von Hand anschauen.** Die Datei liegt
     eine Ebene tief, heisst «standalone» und haengt an genau drei externen Dingen:
     Google Fonts, dem MathJax-CDN und `src="physiklib.js"` — wobei `downloads/physiklib.js`
     gar nicht existiert und die Datei von keiner Themenseite verlinkt ist. Sie ist also
     schon heute halb kaputt. Bevor ein Skript blind `../schriften.css` hineinschreibt:
     klaeren, ob sie ueberhaupt bleiben soll und ob sie je einzeln weitergegeben wird
     (dann muessten die Schriften eingebettet werden statt verlinkt). In Mathe war
     `apex-startseite/` der vergleichbare Fall; dort war die Loesung eine eigene, kleine
     Schriftkopie im Ordner. Ein Apex-Pendant hat Physik nicht.
  5. **Die Datenschutzseite nachziehen.** `rechtliches.html` nennt in
     «Datenschutz beim Seitenaufruf» Google Fonts und jsDelivr ausdruecklich beim Namen;
     nach der Umstellung ist der Absatz falsch. Dazu einen Abschnitt
     «Verwendete Fremdsoftware» mit OFL 1.1 fuer die Schriften und Apache 2.0 fuer MathJax.
     Der Cookie-Absatz ist in Physik guenstiger formuliert als er es in Mathe war
     («setzt keine Cookies und uebermittelt keine Nutzungsdaten»), und die
     «Ausnahme im Browser» fuer den Einheitentrainer steht schon da — dort laesst sich der
     Satz zu den MathJax-Menueeinstellungen mit einem Halbsatz anhaengen.

  **Absicherung:** Der Mathe-Pre-Flight hat neu `check_keine_fremdhosts` (meldet
  `fonts.googleapis.com`, `fonts.gstatic.com`, `cdn.jsdelivr.net` in einer HTML-Datei als
  `[FEHLER]`). Physiks `preflight.py` hat denselben Aufbau — Funktion daneben stellen und
  in `run_light` aufrufen, fertig. Ohne das kommt der CDN-Aufruf beim naechsten Kopieren
  einer alten Vorlage zurueck.

  **Pruefen wie in Mathe:** Playwright bei 1280 und 360 px ueber Seiten aller Typen, dabei
  auf Fremdhosts, HTTP-Fehler und JS-Fehler achten — und die Menuepunkte einmal von Hand
  ausloesen. Zum Vergleich Mathe: 233 Dateien Schriften, 230 MathJax, Repo +4.5 MB,
  ausgeliefert gleich viel wie vorher.

</details>

- (noch leer)

## Mobile-Overflow-Fix (TALS Mathe [97], 2026-07-10) — auch für Physik prüfen

**Was:** Auf 360 px war `body.scrollWidth` auf fast allen Seiten grösser als der Viewport.
**Wo:** `style.css` (Ende) + `.page-wrap`/`.anim-layout`-Media-Queries.
**Warum:** Drei Ursachen, die in TALS Physik sehr wahrscheinlich identisch vorliegen:

1. `mjx-assistive-mml` (MathJax-Screenreader-Kopie, `position:absolute`) zählt zur Scrollbreite.
   Gegenregel braucht `body mjx-assistive-mml { width:1px !important; … }` — MathJax setzt selbst
   `width:100% !important` und injiziert sein CSS nach `style.css`.
2. Grid-Tracks `1fr` (= `minmax(auto,1fr)`) übernehmen die min-content-Breite des Canvas
   (dessen `width`-Attribut die Canvas-Helfer auf Buffer-Pixel setzen) → `minmax(0,1fr)`.
3. Tabellen/Canvas/Formeln brauchen `max-width:100%` bzw. eigenen horizontalen Scroll.
   Achtung: seitenlokale Tabellenklassen mit `overflow:hidden` würden sonst Inhalt abschneiden.

**Prüfbefehl** (Playwright, 360 px): `document.body.scrollWidth` gegen `clientWidth` je Seite;
zusätzlich prüfen, dass keine Tabelle `scrollWidth > clientWidth` bei `overflow-x: hidden` hat.

## TEMPLATE.html: relative Footer-Links (Rückmeldung aus dem §§6–10-Port, 2026-07-29)

**Was:** In `tals-physik/TEMPLATE.html` zeigt der neue Footer auf `feedback.html` und
`rechtliches.html` **ohne** `../`.

**Warum das nicht stimmt:** Die Vorlage ist das Skelett für Themenseiten in `themen/`
und bindet konsequenterweise selbst `../nav.js` und `../style.css` ein. Wer sie kopiert,
erbt zwei Footer-Links, die von `themen/` aus ins Leere zeigen (`themen/feedback.html`).

**Massnahme in Physik:** Im Footer von `TEMPLATE.html` auf `../feedback.html` und
`../rechtliches.html` ändern — die 14 bestehenden Themenseiten sind korrekt, nur die
Vorlage nicht. In Mathe ist das beim Port bereits so gesetzt.

## Startseite: Lektionsangabe unter den Titel (TALS Mathe, 2026-07-30) — für Physik empfohlen

**Was in Mathe gemacht wurde** (`index.html`, eigener `<style>`-Block — nicht `style.css`):
drei Änderungen an der Startseite. Für Physik ist **eine davon** relevant, die zwei
anderen entfallen. Farben spielen keine Rolle: alle drei Änderungen sind reine
Layout-Eigenschaften, es gibt nichts von `--blau`/`--lila` auf `--bernstein*` umzustellen.

### 1. Lektionsangabe von rechts nach links unter den Titel — **portieren**

Bisher steht `.k-lek` per `margin-left: auto` am rechten Zeilenende und konkurriert dort
mit dem Titel um die Breite. Neu sitzt sie linksbündig unter dem Titel.

**Markup** — `.k-name` und `.k-lek` in einen gemeinsamen Block packen:

```html
<div class="kap-hdr" onclick="tog('p4')">
  <span class="k-nr">4</span>
  <span class="k-txt">
    <span class="k-name">Mechanik</span>
    <span class="k-lek">100 Lektionen · 5 Teilgebiete</span>
  </span>
  <span class="k-tog" id="tg-p4">▼</span>
</div>
```

**CSS** — die Zeilenhöhe bleibt gleich, weil die Polsterung sinkt und die
`line-height`-Werte knapp gesetzt sind:

```css
.kap-hdr { padding: 9px 16px; align-items: center; gap: 10px; }   /* vorher 12px 18px */
.k-txt   { display: flex; flex-direction: column; gap: 1px; min-width: 0; flex: 1; }
.k-name  { line-height: 1.2; }
.k-lek   { margin-left: 0; font-size: 0.6rem; line-height: 1.25; white-space: normal; }

/* Die Regel aus §9 richtet .k-lek unter 600px rechts aus — richtig, solange die
   Angabe am rechten Zeilenende sitzt. Unter dem Titel muss sie mit ihm
   linksbündig sein, und align-items/padding-top von dort werden hinfällig. */
@media (max-width: 600px) {
  .kap-hdr { align-items: center; }
  .k-lek   { text-align: left; }
  .k-nr, .k-name { padding-top: 0; }
}
```

**Warum es sich in Physik besonders lohnt** — Physiks `.k-lek`-Texte sind lang
(„Sek-I-Auffrischung · 3 Seiten · kein RLP-Lerngebiet", „30 Lektionen · 2 Teilgebiete
+ 1 Vertiefung"). Gemessen am 30.07.2026 im Physik-Repo:

| Breite | Zeilenhöhen | `.k-lek` bricht um |
|---|---|---|
| 1280 px | 51 px durchgehend | 1 Zeile |
| 600 px | 52 / 52 / 52 / **78** px | bis 2 Zeilen |
| 360 px | **67** / 53 / 53 / **104** px | bis 3 Zeilen |

Bei 360 px ist die Zeile „Einführung in andere Bereiche der Physik" doppelt so hoch wie
die anderen. Unter dem Titel bekommt die Angabe die volle Zeilenbreite. In Mathe sind
die Kapitelzeilen nach dem Umbau **50 px** hoch, also 1 px flacher als vorher (51 px),
und bei 360 px bleiben 50–69 px statt vorher 53–104 px.

### 2. Bereichskopf auf ein Wort kürzen — **entfällt**

Mathe hatte zwei `.bereich`-Köpfe mit Badge + langem Titel („Mathematik —
Grundlagenbereich"), jetzt nur noch „Grundlagenfach" / „Schwerpunktfach", Polsterung
`17px 20px 15px` → `11px 18px 10px`, Kopfhöhe 65 → 51 px. **Physik hat kein `.bereich`**
(nachgesehen: 0 Vorkommen) — der Kopf wurde dort in §9 ersatzlos gelöscht. Nichts zu tun.

### 3. Bereiche nebeneinander — **nicht empfohlen**

In Mathe stehen Grundlagen- und Schwerpunktfach nebeneinander
(`.spalten { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start }`,
unter 900 px zurück auf eine Spalte). Das trägt, weil es **zwei unabhängige Fachbereiche**
mit eigener Farbe und eigener Nummerierung sind.

Physik hat **eine** flache Liste aus vier Lerngebieten (0, 4, 5, 6). Zwei Spalten hätten
dort kein Gegenstück in der Sache, sondern wären eine willkürliche 2+2-Teilung. Dazu
kommt: die vier `.kap`-Zeilen teilen sich ihren Rahmen über
`.kap:first-of-type { border-top … }` und `.kap:last-of-type { border-radius … }` — die
Regeln müssten pro Spalte neu greifen. Und der Gewinn wäre gering: Physiks Liste endet
bei 1280 px schon bei y = 404 px, steht also längst im ersten Bildschirm.
**Empfehlung: einspaltig lassen.**

**Prüfen nach dem Port:** Zeilenhöhen bei 1280 / 600 / 360 px vergleichen,
`.k-lek` linksbündig zum Titel (Versatz 0 px), `document.body.scrollWidth ===
document.documentElement.clientWidth`.

## ~~Clip-Drehbücher: `\lt` / `\gt` statt `&lt;` / `&gt;`~~ (TALS Mathe, 2026-09-06) — **erledigt am 07.09.2026, nichts zu tun**

**Was.** In einem LaTeX-Drehbuch (`"latex": true`, Standard) darf ein Kleiner- oder
Grösserzeichen **nicht** als HTML-Entität geschrieben werden. `tex()` in
`scripts/build-clips.py` maskiert selbst — aus `&lt;` wird `&amp;lt;`, im Bild steht der
sichtbare Text „&lt;", MathJax bricht ab, und `verify_mathjax.js` meldet **Misplaced &**.
Richtig sind die LaTeX-Makros `\lt` und `\gt`; sie enthalten kein HTML-Sonderzeichen und
sind unter beiden Schreibweisen korrekt. Betrifft auch Formeln in `@…@` innerhalb von
Prosa-Elementen — die gehen ebenfalls durch `tex()`.

**Wo in Physik.** Zweimal nachgesehen — und der zweite Blick hat den Eintrag erledigt:

| | Stand 06.09.2026 | Stand 07.09.2026 |
|---|---|---|
| Drehbücher in `clips/` | 13 | **79** |
| davon mit `&lt;` / `&gt;` | 0 | **0** |
| `HOWTO-clips.md` | existiert dort nicht | **existiert, Z. 281** |

**Physik hat die Regel unabhängig selbst gefunden.** In `HOWTO-clips.md` steht dort
wörtlich: „**`<` und `>` gehören als `\lt` und `\gt` ins Drehbuch.**" — mit derselben
Begründung (der Formelsatz maskiert selbst) und dem Zusatz, den Mathe nicht notiert
hatte: für `≤` und `≥` schreibt man `\le` und `\ge`. Kein Drehbuch ist betroffen.
**Nichts zu portieren, nichts zu patchen, Eintrag geschlossen.**

Die Lehre daraus für diese Datei: Zahlen in einem Eintrag altern. Zwischen den beiden
Blicken lagen 24 Stunden und 66 neue Drehbücher. Wer einen Eintrag abarbeitet, zählt
zuerst nach, statt der Tabelle zu glauben.

**In Mathe erledigt:** `HOWTO-clips.md`, Abschnitt „Häufige Stolpersteine" — die alte
Regel `&lt;` / `&gt;` stammte aus der eigenen Schreibweise (`"latex": false`) und war
seit der LaTeX-Umstellung vom 31.08.2026 falsch. Nachgemessen an den 26 Drehbüchern der
Übungsprüfung: 8 Ausdrücke in 6 Dateien fielen als **Misplaced &** durch, nach der
Umstellung auf `\lt` / `\gt` 0 von 765.

**Prüfen nach dem Port:** ein Testdrehbuch mit `T \gt 0` bauen und
`python3 .claude/skills/preflight/preflight.py clips/<name>.html` laufen lassen —
`fehler=0` erwartet.

## Leitprogramme: Selbsttest je Kapitel und Fortschrittsbalken (2026-09-07)

**Was Physik hat** — nachgezählt in den fünf Leitprogrammen am 07.09.2026: Vortest,
Gesamttest und aufklappbare Lösungen (`<details>`) in allen fünf. Die Didaktik steht
also.

**Was fehlt:** ein **Selbsttest nach jedem Kapitel** mit Hakenfeld und ein
**Fortschrittsbalken** in der Seitenschiene. Die Zählung ist eindeutig:

| in Physiks Leitprogrammen | |
|---|---|
| `Gesamttest` | 4 von 5 |
| `<details>` / «Lösung» | 5 von 5 |
| `Selbsttest` | **0** |
| `fortschritt` | **0** |
| `erledigt` (Hakenfeld) | **0** |

**Warum das mehr ist als Zierrat.** Der Gesamttest kommt am Schluss — wer dort scheitert,
weiss nicht, wo es gekippt ist. Der Selbsttest je Kapitel fängt das ab, und das Hakenfeld
gibt dem selbstständigen Durcharbeiten einen sichtbaren Stand. In Mathes drei
Themen-Leitprogrammen trägt jedes **fünf** Selbsttests.

**Was zu übertragen ist:** die Blöcke `.test`, `.test-kopf`, `.aufg`, `details.loes` und
`.fortschritt` aus dem `<style>` einer Mathe-Seite, dazu die Abschnitte «Lösungen: alle
auf/zu» und «Fortschritt» aus dem Seitenskript. **Nachgemessen an
`quadratische-gleichungen.html`: 30 Zeilen CSS für den Testblock, 5 weitere für Balken
und Zähler, 54 Zeilen JS** — ohne Abhängigkeit ausserhalb der Seite. Das aktive Kapitel
in der Schiene (`IntersectionObserver`) hängt im selben Skript und kommt gratis mit.

**Der Fallstrick, in den Mathe getreten ist:** Die `localStorage`-Schlüssel
(`lp-<name>-thema`, `lp-<name>-stand`) **müssen je Seite eigen sein**. Wer eine Seite als
Vorlage kopiert und sie vergisst, lässt zwei Leitprogramme denselben Fortschritt teilen —
das Häkchen im einen erscheint im anderen. In Physik kommt `localStorage` in den
Leitprogrammen bisher **gar nicht** vor; wer die Mechanik holt, vergibt die Schlüssel
also von Anfang an sauber.

**Und eine Leitplanke, die Mathe teuer gelernt hat:** Wird ein Thema deutlich grösser als
rund elf Clips, gehört es geteilt. Am 07.09.2026 wurde ein Entwurf mit 19 Clips in zwei
Programme zerlegt, jedes mit eigenem Vorwissenstest und Gesamttest. Physiks Programme
liegen mit 7 bis 10 Clips genau im richtigen Band — das ist keine Warnung, sondern eine
Bestätigung von beiden Seiten.


## Clip-Generator: drei Bausteine, die nur Mathe hat (2026-09-07)

Gezählt im Physik-Repo am 07.09.2026, nicht geschätzt. Physiks
`scripts/build-clips.py` kennt die Elementtypen `aussage`, `box`, `formel`, `graf`,
`karte`, `liste`, `notiz`, `strich`, `text`, `titel`, `untertitel` — und **79
Drehbücher** stehen dort. Die drei Bausteine unten fehlen ihm.

### 1. Bedingungsleiste — `"voraussetzung"` im Drehbuchkopf · **lohnt sich dort am meisten**

**Was.** Ein Drehbuch bekommt neben `titel` ein Feld `voraussetzung`. Der Generator
legt daraus eine schmale Leiste unter den Kopf, die **den ganzen Clip über stehen
bleibt** — dort steht die Bedingung, auf der alles Folgende ruht (`a \neq 0`,
`x \gt 0`, „nur im rechtwinkligen Dreieck"). Sie ist keine Szene, sie verschwindet nie.

**Warum das didaktisch zählt.** Der Anlass war eine Beobachtung des Autors: Im Verlauf
eines Clips wird oft auf eine Voraussetzung aufgebaut, die längst aus dem Bild gescrollt
ist. Wer bei Minute zwei einsteigt, sieht die Rechnung, aber nicht, wofür sie gilt.

**Abgrenzung, damit sie nicht verwässert.** Die Leiste trägt nur, was **von Anfang an
gilt**. Was der Clip erst *herleitet*, gehört nicht hinein — sonst steht die Antwort
schon in der Kopfzeile, bevor die Frage gestellt ist.

**Wo in Physik.** `voraussetzung` kommt in `scripts/build-clips.py` **0-mal** vor.
Dafür benutzen dort **77 von 79 Drehbüchern** `halten`, und das HOWTO warnt: „Eine
gehaltene Zeile belegt das Band oben." `halten` und `voraussetzung` lösen **verwandte,
aber verschiedene** Probleme — `halten` trägt eine Zeile *aus einer Szene* weiter,
`voraussetzung` steht über dem *ganzen* Clip. Dass 77 von 79 Clips zum Halten greifen,
ist der beste Beleg dafür, dass der Bedarf in Physik gross ist.

**Was zu übertragen ist.** Die Emission nach dem Fussbereich in `build-clips.py`, das
CSS `#vorleiste` / `.vor`, und die Schutzregel — Mathe bricht den Bau ab, wenn eine
Szene mit `oben < 170` in die Leiste liefe:

```python
if dreh.get("voraussetzung") and sz.get("oben", oben) < 170:
    raise SystemExit("Szene %r beginnt bei oben=%d und liefe in die Bedingungsleiste …")
```

Physik braucht dort eine **eigene Zahl**, weil das Band von `halten` bereits Platz
belegt: dort beginnen Folgeszenen laut HOWTO bei `oben: 430`. Wer beides kombiniert,
prüft die Schwelle im Browser nach, statt 170 zu übernehmen.

### 2. `typ: "boxplot"` · **in Physik vermutlich ohne Anwendung**

Zeichnet Minimum, Q1, Median, Q3, Maximum nach der Konvention der Mathe-Themenseite 4.3
(Antennen bis zu den Extremwerten, **keine** Ausreisser-Regel; Quartile nach Tukey).
`boxplot_svg` kommt in Physiks `build-clips.py` 0-mal vor — und **kein** Physik-Drehbuch
enthält das Wort. Ehrlich gesagt: Physik hat keine Datenanalyse im Lehrplan, der
Baustein läuft dort wahrscheinlich leer. **Nur portieren, wenn Messreihen-Auswertung
tatsächlich Thema wird** — sonst ist es toter Code.

### 3. `beschriftung_bei` für `punkte` im `graf` · **dort schon vorhanden, nichts zu tun**

Setzt die Beschriftung eines Punktes an eine frei gewählte Stelle statt an den
Standardversatz `(+18|−16)`, damit sie nicht auf einer Achsenzahl landet.
**Nachgesehen:** Physiks `build-clips.py` kennt `beschriftung_bei` bereits — Z. 323 für
`graf`, Z. 352 für Pfeile. Der Mathe-Zusatz betrifft nur den Zweig `punkte`. Ob der dort
fehlt, entscheidet sich am Tag, an dem Physik den ersten `graf` baut: **0 von 79
Drehbüchern** benutzen ihn heute. Bis dahin: nichts zu tun.

**Die Lehre, die unabhängig vom Code gilt:** Die vier Kollisionen, die den Zusatz nötig
machten, hat **kein Prüfskript** gefunden — sie standen nur in den Bildern. Wer Punkte
beschriftet, rechnet die freie Stelle aus und schaut sie an.

## Rückübertrag Physik → Mathe: `pruef-clip.mjs` misst den Inhalt (2026-09-07) — **erledigt**

Zum ersten Mal lief der Übertrag in die andere Richtung.

**Was Physik gefunden hat.** Bis zum 07.09.2026 mass `pruef-clip.mjs` in beiden Repos
nur den *Container* einer Zeile. Eine Formelzeile trägt aber `white-space: nowrap`: Sie
bricht nicht um, sondern läuft über ihren Container hinaus — und der bleibt dabei
unverändert breit. Die Prüfung sah davon nichts. Physik hat auf Inhaltsmessung
umgestellt, und dabei kamen **zehn abgeschnittene Zeilen in fünf Clips** zum Vorschein.

**In Mathe übernommen** — dieselbe `.map()`, die Container *und* Kinder misst.

**Und dann nachgemessen, statt es zu glauben:** Alle 177 Mathe-Clips einmal mit der alten
und einmal mit der neuen Messung durchgefahren, an jeder Szenenmitte.

| | |
|---|---|
| Zusätzliche Funde durch die neue Messung | **0 von 177 Clips** |
| Echter Fund (beide Messungen, vorher übersehen) | 1 — `s2-2c-ti30x-num-solv`, 38 px bei t=28 s, behoben mit `abstand: 370` |

**Warum Mathe verschont blieb** — das ist die eigentlich interessante Zahl: Mathes Clips
laufen nicht über, weil die Zeilen dort schmaler gesetzt sind. Der blinde Fleck war
trotzdem echt; er hatte in Mathe nur nichts zu verdecken. **Die Umstellung ist damit
Vorsorge, keine Reparatur** — und die Layout-Freigaben der 177 Clips bleiben gültig.

**Was das für diese Datei heisst.** Der Übertrag ist keine Einbahnstrasse mehr. Wer hier
einen Eintrag schreibt, schaut auch, ob das Schwesterprojekt inzwischen etwas hat, das
hier fehlt.

## Physik-`CLAUDE.md`: Satz über `trigo2` streichen (2026-09-13)

**Was.** In `../tals-physik/CLAUDE.md` (Abschnitt `build-clip-ton.py`, «Zahlen im
`sprecher`-Text ausschreiben», Z. 142–143 am 13.09.2026) steht: «Die Reihe `trigo2`
hält sich als einzige nicht daran (18 Szenen, Stand 13.09.2026).»

**Warum.** Seit Commit `e0ba120` stimmt das nicht mehr: Die 18 Szenen in sechs Clips
sind ausgeschrieben und neu vertont. In allen 197 Mathe-Drehbüchern stehen Ziffern im
`sprecher` jetzt nur noch als Namen — `TI-30X` (1 Szene) und `L1`/`L2`/`L3` (4 Szenen,
`g4-3-ti30x-*`). Der Rest des Absatzes («Mathes 162 Clips», die Ausnahmen) bleibt
richtig.

**Wie.** Den letzten Satz ab «Die Reihe `trigo2` …» löschen. Sonst nichts.

## Clip-Bühne: «✕ Schliessen» bei schmalem Bildschirm abgeschnitten (2026-09-15)

**Was.** Unter 720 px teilt sich der Kopf der Clip-Bühne (`.cb-kopf`) eine Zeile mit
Titel, «eigener Tab ↗» und «✕ Schliessen». Weil `.cb-tab`/`.cb-zu` nicht umbrechen und
der Titel nicht unter die Breite seines längsten Worts schrumpft, ragt der
Schliessen-Knopf über den rechten Rand. In Mathe gemessen: bei 360 px 81 von 177
Titeln, bei 320 px 170, bei 400 px 11.

**Wo in Physik.** `../tals-physik/style.css`, `@media (max-width: 720px)` direkt nach
`.cb-rahmen iframe` (Z. 1359–1363 am 15.09.2026) — wortgleich mit dem Mathe-Block vor
der Korrektur. Die Bühne öffnet `physiklib.js` (Z. ~347); `clips.html` hat 91 Einträge
mit `data-modus="gross"`, der längste der 100 Drehbuch-Titel hat 80 Zeichen.

**Wie.** Im Media-Block nach `.cb-kopf, .cb-rahmen { width: 100%; }` ergänzen:

```css
  .cb-kopf { flex-wrap: wrap; gap: 4px 12px; }
  .cb-titel { flex: 1 1 100%; }
```

Der Titel nimmt dann die erste Zeile, Tab und Schliessen stehen darunter rechts
(`.cb-tab` hat schon `margin-left: auto`). In Mathe danach alle Titel bei 320/360/400/720
und 1280 px nachgemessen: Knopf überall innerhalb des Rands, 1280 px unverändert.
