# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

**Bereinigt am 28.09.2026:** Alle Einträge wurden gegen das Physik-Repo geprüft
(Stand `f115899`, nur gelesen). Erledigte und gegenstandslose sind entfernt —
ihr Wortlaut steht in der Git-Geschichte dieser Datei. Übrig waren danach drei; neue kommen unten dazu.
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

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
  **Stand 28.09.2026:** In Physik zeichnet derzeit keine Canvas eine Intervallgrenze
  als Punkt (die Zahlenstrahlen in p5-1/p5-2 sind Skalen) — der Helfer lohnt sich
  erst, wenn eine solche Grafik entsteht.

- **2026-09-07 · Clip-Generator: Bedingungsleiste `voraussetzung` · `scripts/build-clips.py` · warum:** (Zählungen vom 07.09.2026; die zwei übrigen Bausteine `boxplot` und `beschriftung_bei` entfallen für Physik.)

  Gezählt im Physik-Repo am 07.09.2026, nicht geschätzt. Physiks
  `scripts/build-clips.py` kennt die Elementtypen `aussage`, `box`, `formel`, `graf`,
  `karte`, `liste`, `notiz`, `strich`, `text`, `titel`, `untertitel` — und **79
  Drehbücher** stehen dort (heute rund 200). Die Bedingungsleiste fehlt ihm weiterhin.


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

- **2026-09-28 · Gedankenstrich an Formeln auch in `.cv-titel` beseitigen · Physik
  `themen/*`, Klasse `.cv-titel` · warum:** Entscheid des Auftraggebers vom 28.09.2026:
  Die Regel «Kein Gedankenstrich unmittelbar an einer Formel» (Mathe STYLEGUIDE §2.8,
  in Physik mit `3a16835` für h2/h3/anim-titel/block-titel/aufg-titel-text umgesetzt)
  gilt **auch für die Diagrammtitel `.cv-titel`**. Dort klebt noch 22-mal ein
  Gedankenstrich direkt an `\(` oder `\)`, z.B. `p0-1:374`, `p0-2:1195`, `p6-1a:290`
  (gezählt 28.09.2026, nur gelesen). Vorgehen wie in §2.8: **vor** der Formel
  Doppelpunkt statt Strich; **nach** der Formel umstellen (Tätigkeit nach vorn, Formel
  ans Ende) oder bei einem blossen Etikett Doppelpunkt; steht ein Wort zwischen Strich
  und Formel, bleibt der Titel. Vor dem Umbau neu zählen (`.cv-titel` samt `\(`/`\)`
  direkt am «—»), danach im Browser nachsehen, ob kein Titel umbricht. In Physiks
  STYLEGUIDE die Klasse in die Liste der Titel aufnehmen.

- **2026-09-28 · Wassermodell des Stromkreises als neue Animation · Physik
  `themen/p6-2-elektrizitaet.html`, Abschnitt «Grundbegriffe» · warum:** Auf Wunsch
  des Auftraggebers in einer Mathe-Session gebaut, gehört aber nach Physik. Vorlage:
  **`_intern/uebertrag-physik-wassermodell/wassermodell.html`** (nur lokal —
  `_intern/` steht in `.gitignore`; eigenständige Seite, auch
  als Artifact veröffentlicht: https://claude.ai/artifact/BoaXnQU8i1qbWzLwyArboE).
  Inhalt: Wasserkreis und Stromkreis in **derselben Anordnung**, umschaltbar
  (Überblendung, Bauteile bleiben am Platz) oder nebeneinander; ein Widerstand / Reihe
  / parallel; Hahn–Schalter; Durchflussmesser ↔ Amperemeter, U-Rohr-Manometer ↔
  Voltmeter mit Live-Werten; Druck bzw. Potenzial als Farbe der Leitung; Punkte für
  Wasser/Ladung mit Tempo ∝ Stromstärke; Tabellen «Grössen» und «Bauteile» mit
  Hervorhebung im Bild; fünf Aufträge, Merksatz, «Wo das Modell hinkt». Massstab
  1 V ↔ 10 kPa, 1 A ↔ 100 mL/s (dann stimmen die Leistungen in W überein).

  **Nachgesehen im Physik-Repo (Stand `9f88611`, nur gelesen):**
  - p6-2 hat 4518 Zeilen und **12 Animationen**, im Titel nummeriert
    «Animation 1 · …» bis «Animation 12 · …», plus die unnummerierte
    «Einstieg-Animation · Einfacher Stromkreis». Ein Wassermodell gibt es nicht; der
    Wasservergleich steht nur als Transfer-Frage im Mini-Check nach «Grundbegriffe»
    («Im Vergleich mit einem Wasserkreislauf: Was entspricht der elektrischen
    Spannung, was der Stromstärke?»).
  - **Vorschlag Platz:** nach dem Block «📘 Stromstärke und Spannung», vor diesem
    Mini-Check — die Frage übt dann, was die Animation zeigt. Dann rutschen
    «Animation 1–12» um eins; keines der 24 p6-2-Drehbücher nennt eine
    Animationsnummer (geprüft), die 11 `p6-2-anim-*`-Clips bleiben also gültig.
    Alternativ unnummeriert wie die Einstieg-Animation.
  - **Physik schreibt «Amperemeter»** (33 Treffer auf p6-2, «Ampèremeter» nirgends
    in `themen/`). Die Vorlage ist seit 28.09.2026 angeglichen.
  - **«Potenzial» kommt auf p6-2 nicht vor.** Legende und Bauteiltabelle der Vorlage
    sprechen davon; entweder dort kurz einführen oder umformulieren
    («Spannung gegenüber dem Minuspol»).
  - **Stromrichtung:** Die Einstieg-Animation zeigt **Elektronen** (− → +), die
    Vorlage standardmässig die technische Stromrichtung (+ → −, wie das Wasser) mit
    Schalter «Elektronen zeigen». Beim Einbau entscheiden, ob der Standard kippen soll.

  **Umbau fürs Physik-Skelett** (die Vorlage ist eine freie Seite, keine
  Themenseiten-Struktur): Markup auf `widget` / `widget-header` /
  `widget-titelzeile` / `widget-body`, Regler als `sl-row` + `sl-val`, Knöpfe als
  `typ-btn` bzw. `play-btn`, Leinwand in `cv-wrap` mit `cv-titel`; Hinweispaar
  `anim-hinweis links` («💡 Worauf achten?») und `rechts` («✓ Erkenntnis») statt der
  aufklappbaren Aufträge; die Tabellen und «Wo das Modell hinkt» als Blöcke im
  Fliesstext (`block-def` bzw. Rot-Block). Farben aus Physiks `style.css` statt der
  eigenen Tokens; Google-Fonts- und jsDelivr-MathJax-Link **entfernen** (Physik lädt
  nichts von fremden Hosts). Canvas-Code (≈ 300 Zeilen, IIFE, keine globalen Namen)
  kann weitgehend bleiben; auf Kollisionen mit den übrigen Seitenskripten prüfen.
  Danach Pre-Flight.

  **Der Animationsclip ist schon gebaut** — mit Physiks eigenem Werkzeug, aus
  einer Kopie von `scripts/build-clips.py`, `build-clip-ton.py`, `clips/themes`,
  `schriften*` und `vendor/mathjax` im Scratchpad (Physik-Repo nur gelesen).
  Alles liegt unter `_intern/uebertrag-physik-wassermodell/clips/`, in Physiks
  Ordnerstruktur, also 1:1 nach `clips/` kopierbar: Drehbuch
  `p6-2-anim-wassermodell.json`, gebaute Web-Fassung `.html`, Sprechertext,
  `ton/p6-2-anim-wassermodell.mp3` (Thorsten, Physiks Aussprache-Tabellen) und
  vier Aufnahmen `bilder/p6-2-anim-wassermodell-1…4.jpg`; der Aufnahmeplan
  liegt daneben in `aufnahme/aufnahme.mjs`. Reihe «Animationen erklärt», 86.0 s,
  Titel · 4 Schritte · Merksatz; `pruef-clip.mjs` an 29 Zeitmarken ohne Befund,
  Bilder angesehen, Beschriftung im Bild rund 20 px auf der 1920er-Bühne.
  Inhalt: Pumpe ↔ Quelle (60 kPa ↔ 6.0 V), Strom vor = nach dem Widerstand
  (0.60 A ↔ 60 mL/s, Fehlvorstellung «Widerstand verbraucht Strom»), Widerstand
  verdoppelt (20 Ω → 0.30 A ↔ 30 mL/s), Schalter offen ↔ Hahn zu, Merksatz mit
  Modellgrenze Elektronenrichtung. Beim Einbau noch offen:
  - `"probe": true` entfernen und `folge` setzen (Nummer der Animation; das Feld
    fehlt bewusst, `_folge` im Drehbuch erklärt es). Der Anker ist schon
    `"animation": "anim-wassermodell"` — das `h3` der Animation muss ihn tragen.
  - **Wird die Animation beim Umbau aufs Physik-Skelett optisch verändert**
    (Farben aus `style.css`, andere Schrift), die vier Bilder mit dem
    Aufnahmeplan neu aufnehmen — er setzt die Zustände über `#sl-u`, `#sl-r1`,
    `#seg-kreis` und `#btn-schalter`, die IDs also mitnehmen oder den Plan
    anpassen. Die Bilder sind bei 390 px Fensterbreite aufgenommen, weil die
    Animation dort grössere Schrift setzt (Faktor bis 1.35).
  - Danach die üblichen vier: `build-clips.py` → `build-clips-einbau.py
    --schreiben` → `build-suchindex.py` → `build-seo.py`; Sprechertext
    unverändert, also keine neue Vertonung nötig.
