# TODO — systemische Anpassungen auf TALS-Mathe übertragen

Diese Änderungen wurden in **TALS-Physik** gemacht und betreffen das gemeinsame Skelett
(CSS + Canvas-Bibliothek). Da TALS-Mathe dasselbe Skelett nutzt, sollten sie dort
1:1 nachgezogen werden — **aber nur die Layout-/Positions-Eigenschaften, nicht die Farben**:
Mathe hat Blau als Leitfarbe, Physik Bernstein. Beim Kopieren von CSS-Regeln die jeweils
eigenen Farb-Variablen (`--blau*` statt `--bernstein*`) der Mathe-Seite belassen.

> Vor dem Übertragen prüfen, ob die Klassennamen / Dateinamen in Mathe identisch sind
> (`style.css`, `physiklib.js` bzw. das dortige Pendant, `.live-box`, `.anim-hinweis`,
> `.widget-titelzeile`). Wo sie abweichen, Selektoren entsprechend anpassen.
> Nach jeder Änderung den Mathe-Pre-Flight laufen lassen (falls vorhanden) und – sobald
> ein Browser verfügbar ist – einen Render-Check bei 1280 px **und** 360 px machen
> (dieser steht in Physik noch aus: Playwright war lokal nicht installierbar).

---

## 1. Canvas-Beschriftungen: Mindestgrösse 13 px  (Lesbarkeit)

**Was:** Alle Canvas-Schriftgrössen (`ctx.font = '…px …'`) unter 13 px wurden auf 13 px
angehoben — über alle Themenseiten **und** in `physiklib.js` (dort u. a. Achsen-Zahlen
11→13, Achsen-Einheiten/Pfeil-Labels 12→13). `bold` bleibt erhalten, ≥ 13 px unverändert.
Die Hierarchie trägt danach `bold` vs. normal.

**Warum:** 10–11 px sind auf den dpi-skalierten Canvas zu klein gegenüber dem Fliesstext.

**Wie (Skript, im Mathe-Repo-Root ausführen, Dateinamen ggf. anpassen):**

```python
import re, glob
FLOOR = 13
pat = re.compile(r"(font\s*=\s*'(?:bold )?)(\d+(?:\.\d+)?)px")
def bump(m):
    pre, size = m.group(1), float(m.group(2))
    return f"{pre}{FLOOR}px" if size < FLOOR else m.group(0)
# 'physiklib.js' ggf. durch den Namen der Mathe-Canvas-Bibliothek ersetzen
for f in sorted(glob.glob('themen/*.html')) + ['physiklib.js']:
    s = open(f, encoding='utf-8').read()
    changed = sum(1 for m in pat.finditer(s) if float(m.group(2)) < FLOOR)
    if changed:
        open(f, 'w', encoding='utf-8').write(pat.sub(bump, s))
        print(f"{changed:3}  {f}")
```

**Prüfen:** danach `grep -rE "font\s*=\s*'(bold )?(7|8|9|10|11|12)px" themen/*.html <lib>.js`
darf nichts mehr finden. Lange Satz-Beschriftungen auf 360 px gegen Überlauf sichten
(in Physik der einzige Restpunkt).

- [x] Skript in Mathe ausgeführt (grundlagen + schwerpunkt + `mathlib.js`) — 21 HTML-Seiten
  und `mathlib.js` (Achsen-Zahlen 11→13, Achsen-Labels `bold 11`→`bold 13`).
- [x] keine `<13px`-Fonts mehr vorhanden (`grep` über grundlagen/schwerpunkt/mathlib.js leer)

---

## 2. Live-Box: grosszügiger Spaltenabstand  (`style.css`)

**Was:** Spaltenabstand der Wert-Boxen von `14px` auf **`14px 70px`** (Zeile/Spalte).
Dichte Boxen (≥ 4 Werte) bekommen den engen Abstand zurück.

**Warum:** Mehr horizontaler Abstand liest sich deutlich besser; getrennter Zeilen-/
Spaltenabstand hält die Werte beim Umbruch (Mobile) trotzdem eng beieinander.

**Diff (nur die `gap`-Zeile ändern + eine neue Regel; Farben/Übriges der Mathe-Box lassen):**

```css
/* vorher: .live-box { … gap:14px … } */
.live-box { … gap:14px 70px … }
/* NEU direkt darunter: dichte Boxen (4+ Werte) wieder eng */
.live-box:has(> .lb-item:nth-child(4)) { column-gap:14px; }
```

**Hinweis:** `:has()` ist seit Ende 2023 Baseline (alle aktuellen Browser) — für GitHub
Pages unkritisch.

> **NICHT ÜBERTRAGBAR (2026-06-24):** TALS-Mathe hat keine `.live-box`/`.lb-item`-Struktur.
> Live-Werte werden hier nicht als horizontale Flex-Zeile, sondern als vertikale Legende
> (`.legende` / `.legende-zeile`) bzw. inline als `.wert`-Spans in der Formel dargestellt.
> Es gibt also keinen `column-gap` zwischen nebeneinanderliegenden Wert-Boxen, der sich
> vergrössern liesse — kein passendes Pendant. Punkt entfällt für Mathe.

- [~] `gap:14px 70px` gesetzt — entfällt (kein `.live-box` in Mathe, s. o.)
- [~] `:has()`-Ausnahme für 4+-Werte-Boxen ergänzt — entfällt (s. o.)

---

## 3. Animations-Hinweise: Rollover öffnet nach links, kein Abschneiden  (`style.css`)

**Was:** „Worauf achten?" und „Erkenntnis" stehen jetzt **beide am rechten Zeilenende**
und ihre Rollover öffnen **nach links** (vorher öffnete „Worauf achten?" nach rechts und
wurde bei schmalem Fenster abgeschnitten).

**Warum:** Das nach rechts öffnende Rollover lief aus dem Rahmen; rechtsbündig + nach
links öffnend passt auf jeder Breite.

**Diff (4 Stellen im `.anim-hinweis`/`.widget-titelzeile`-Block):**

```css
/* a) Titelzeile wird Bezugsrahmen + schiebt die Hinweise nach rechts */
.widget-titelzeile { position:relative; … }            /* position:relative ergänzen   */
.widget-titelzeile h3 { margin:0; margin-right:auto; }  /* margin-right:auto ergänzen    */

/* b) ENTFERNEN:  .anim-hinweis.rechts { margin-left:auto; }
      (wird durch h3{margin-right:auto} ersetzt; sonst entsteht eine Lücke) */

/* c) „Worauf achten?" (links) am rechten Rand der Titelzeile verankern */
.anim-hinweis.links { position:static; }

/* d) beide Rollover öffnen nach links */
.anim-hinweis.rechts .ah-pop,
.anim-hinweis.links  .ah-pop { left:auto; right:0; }    /* die .rechts-Regel gab es schon */
```

**Wirkung:** Beide Hinweise sitzen am rechten Titelende; das `.ah-pop` der linken
Variante richtet sich (über `position:static`) an der `.widget-titelzeile` aus und passt
mit `width:min(440px,86vw)` auf jeder Breite.

- [x] `.widget-titelzeile` → `position:relative`
- [x] `.widget-titelzeile h3` → `margin-right:auto`
- [x] `.anim-hinweis.rechts { margin-left:auto }` entfernt
- [x] `.anim-hinweis.links { position:static }` ergänzt
- [x] `.anim-hinweis.links .ah-pop` zur `left:auto; right:0`-Regel hinzugefügt

---

## 4. Optional / prüfen — Muster, kein Pflicht-Port

Diese Punkte wurden in Physik pro Animation umgesetzt; in Mathe nur übernehmen, wo es
inhaltlich passt:

- [ ] **Play-/Pause-Knöpfe entfernen, wo unnötig** — Animationen starten ohnehin per
  IntersectionObserver-Autostart (`makeLoop(canvasId, null, tick)` statt Button-ID).
- [ ] **Auswahl-Knöpfe + Regler in einer `.sl-row`** (Knöpfe zuerst, dann Regler-`.sl-grp`)
  als einheitliches Bedienmuster.
- [ ] **Texte auf Schweizer Hochdeutsch / Punkt als Dezimaltrennzeichen** gegenprüfen
  (gilt in Mathe ohnehin, aber bei kopierten Snippets kontrollieren).

---

## 5. Stilcheck-Regelwerk

> Nicht in diese Kopie übernommen — §5 wird über `scripts/port_stilcheck_von_physik.py`
> abgewickelt (siehe Physik-Kopie dieser Datei). Nummerierung bleibt zur Deckungsgleichheit
> mit der Absenderliste erhalten.

---

## 6. Header bleibt beim Scrollen stehen  (`style.css`, 1 Zeile + 1 Regel)

**Was:** `#nav-root` wird selbst `sticky`. Dazu bekommt `.mobile-nav` eine Höhenbegrenzung
mit eigenem Scrolling.

```css
#nav-root { position: sticky; top: 0; z-index: 200; }

.mobile-nav {
  /* … bestehende Regeln … */
  max-height: calc(100vh - 54px); overflow-y: auto;
}
```

**Warum:** `.site-hdr` trägt zwar `position: sticky; top: 0`, klebt aber nie — der Header
liegt in `<div id="nav-root">`, und ein klebendes Element klebt nur innerhalb der Box
seines Containers. Der ist 54 px hoch und scrollt weg. In Physik gemessen: bei
Scrollposition 2500 lag die Header-Oberkante bei −2500, auf allen Breiten und Seiten.
Zweiter Effekt: das Burger-Menü liegt im Textfluss direkt unter dem Header und ging beim
Scrollen **ausserhalb des Bildschirms** auf (bei 360 px gemessen: Menü bei −4029, und die
eingefügten 1083 px schoben die Seite zusätzlich weiter). Ohne `max-height` ist das offene
Menü höher als der Schirm und die unteren Einträge sind unerreichbar.

**Mathe-Stand (29.07.2026 geprüft):** identischer Fehler. `style.css:53` setzt
`position: sticky` auf `.site-hdr`, eine Regel für `#nav-root` gibt es nicht;
`.mobile-nav` ist vorhanden. Der Port ist 1:1 möglich, keine Farbfrage.

**Dazu gehört:** Sprungziele nicht unter den Header rutschen lassen —

```css
.content h2[id], .content h3[id] { scroll-margin-top: 66px; }
```

Betrifft die Sprünge aus dem Inhaltsverzeichnis und (nach §7) aus der Suche. Mathe hat
heute kein `scroll-margin` im `style.css`.

- [x] `#nav-root` sticky gesetzt (`style.css`, vor `.site-hdr`) — Playwright gemessen:
  Header-Oberkante bei `scrollY=2500` liegt auf **0** statt −2500, bei 1280 px **und** 360 px.
- [x] `.mobile-nav` mit `max-height: calc(100vh - 54px)` + `overflow-y: auto` — Burger-Menü
  öffnet bei 360 px an Oberkante 54 mit 686 px Höhe (Viewport 740) und eigener Scrollleiste.
- [x] `scroll-margin-top: 66px` für `.content h2[id]`/`h3[id]` — Sprungziel landet gemessen
  bei 66 px, also unter dem 54-px-Header.

---

## 7. Volltextsuche über die ganze Site  (neu: 3 Dateien + Header-Feld)

**Was:** Suchfeld oben rechts im Header, Trefferpanel mit Kapitelnummer, Abschnittstitel
und markiertem Textausschnitt, Sprung auf den `<h2>`-Anker. Rein statisch, kein Server,
keine Fremdbibliothek.

**Dateien aus Physik (in dieser Reihenfolge übernehmen):**

| Datei | Rolle | Anpassung für Mathe |
|---|---|---|
| `scripts/build-suchindex.py` | erzeugt den Index aus den Seiten | Seitenliste, Skip-Listen, Pfade |
| `suche.js` | Suchlogik + Panel | nur Pfad-/Textkosmetik |
| `suchindex.js` | **generiert** — nie von Hand ändern | entsteht beim ersten Lauf |
| `nav.js` | Suchfeld ins Header-Markup | 1:1 (Markup ist farbfrei) |
| `style.css` | Feld + Panel + Mobile-Lupe | `--bernstein*` → `--blau*` |

**Der Generator ist seit 29.07.2026 projektübergreifend — nichts umzubauen.**
`scripts/build-suchindex.py` erkennt das Projekt an der Canvas-Bibliothek im Repo-Root
(`physiklib.js` / `mathlib.js`), liest **alle** Listen aus dem `const SITE = {…}`-Block
(Physik: `themen`; Mathe: `grundlagen` + `schwerpunkt`) und hängt Glossar und
Formelsammlung an, sofern vorhanden. Projektabhängig ist nur ein Feld:

```python
PROJEKTE = [
    {'name': 'TALS Physik', 'kennung': 'physiklib.js',
     'skip_classes': {'widget-body'}},
    {'name': 'TALS Mathe',  'kennung': 'mathlib.js',
     'skip_classes': {'regler', 'legende', 'formel', 'wert', 'val', 'lab', …}},
]
```

Mathe hat kein `.widget-body`; die Bedienung liegt in `.bedien`, wo neben Reglern und
Legenden auch die `.erklaerung` steht — darum sind dort die Kinder einzeln ausgeschlossen
und `.bedien` selbst bleibt drin, sonst ginge der Erklärtext verloren. Die
Abschnittsnamen (`aufgaben`, `downloads`, `ressourcen`), das Glossar-Markup
(`.glossar-eintrag`/`.ge-begriff`/`.ge-quer`) und der `<h3>`-Aufbau der Formelsammlung
sind in beiden Projekten identisch — geprüft, nichts anzupassen.

**Datei einfach übernehmen und laufen lassen:**

```bash
cp /home/paps/tals-physik/scripts/build-suchindex.py scripts/
python3 scripts/build-suchindex.py --dry-run   # baut, schreibt nichts
python3 scripts/build-suchindex.py             # schreibt suchindex.js
```

Der Trockenlauf gegen das Mathe-Repo ist am 29.07.2026 gelaufen: **48 Seiten,
398 Abschnitte, 558 KB** (Physik: 208 / 247 KB). Stichproben bestanden — Mini-Check-Fragen,
Lösungen, Aufgaben-Marker und Legendenwerte fehlen im Index, die `.erklaerung`-Texte sind
drin. Ändert sich das Markup, wird nur `PROJEKTE` angefasst, nicht der Parser.

**Grösse:** Physik hat 507 KB Rohtext → 208 Abschnitte → `suchindex.js` 250 KB
(~45 KB über die Leitung). Mathe hat **1086 KB Rohtext über 48 Seiten**, also grob das
Doppelte. Der Index wird erst beim ersten Tastendruck im Suchfeld nachgeladen, das ist
verkraftbar — wenn er unangenehm gross wird, den Abschnittstext im Generator kappen
(z.B. 1500 Zeichen) statt Seiten wegzulassen.

**Warum `.js` statt `.json`:** `fetch()` auf eine JSON-Datei scheitert unter `file://` an
CORS. Als `window.SUCHINDEX = {…}` funktioniert die Suche auch, wenn jemand die Seiten
lokal öffnet.

**Pflege:** Nach jeder inhaltlichen Änderung `python3 scripts/build-suchindex.py`. In
Physik prüft der Pre-Flight das mit (`--check`, Exit 1 = veraltet) und meldet `[WARN]` —
denselben Aufruf in den Mathe-Pre-Flight aufnehmen. Der Fingerabdruck geht über den
*indexierten Inhalt*, nicht über die Rohdateien; Änderungen an Skripten oder Aufgaben
lösen also keine Fehlalarme aus.

- [x] `scripts/build-suchindex.py` aus Physik kopiert — **1:1, kein Umbau**. Trockenlauf
  bestätigt die Erwartung exakt: **48 Seiten, 398 Abschnitte, 558 KB** (fp `708a2a5c…`).
- [x] Stichprobe nach dem ersten Lauf bestanden: Mini-Check-Kopf („Mini-Check — Steigung,
  Achsenabschnitt") und zwei Aufgaben-Titel („Funktionsgleichung aus dem Graphen ablesen",
  „ziehe P1 und P2 auf die Gerade") **nicht** im Index; Einstiegstext von g3-2 und eine
  `.erklaerung` aus g1-1 **schon**.
- [x] `suche.js` übernommen (nur Kopf-/Kommentarkosmetik: Projektname, Pfade
  `grundlagen/`+`schwerpunkt/`, Mathe-Beispiele statt „Wärme"), `suchindex.js` gebaut.
- [x] Suchfeld in `nav.js` (Header rechts, Lupe ab 640 px) + CSS in `style.css`
  mit `--blau`/`--blau-hell`/`--blau-rand` statt `--bernstein*`.
- [x] `<script src="…/suche.js">` auf allen 50 Seiten eingebunden (46 Themenseiten,
  `index.html`, `glossar.html`, `formelsammlung.html`, `TEMPLATE.html`) — ein Skriptlauf
  gemeinsam mit dem Footer aus §8, direkt nach der `nav.js`-Zeile, idempotent.
- [x] Pre-Flight um den `--check`-Aufruf ergänzt (`[WARN]` bei veraltetem Index,
  kein Blocker) — analog Physik.
- [x] Render-Check 1280 px + 360 px: Suche „Steigung" liefert je 20 Treffer, Panel liegt
  vollständig im Viewport (1280: 788–1248 px; 360: 10–350 px, Lupe klappt das Feld auf).
  Tastatur (`/`, Strg/Cmd+K, ↑ ↓, ⏎, Esc) ist unverändert aus Physik übernommen —
  die Pfad-/Farbanpassungen berühren die `keydown`-Verdrahtung nicht.

---

## 8. Rechtliches, Footer und «Kontakt & Feedback»

**Was:** Autor, Lizenz, Haftung und Datenschutz sind belegt und von jeder Seite aus
erreichbar; Kontakt läuft ausschliesslich über das Feedbackformular, es gibt **keine**
veröffentlichte E-Mail-Adresse.

**Teile:**

1. **`rechtliches.html`** (neu, Root, kein eigener Headerpunkt): Verantwortlich · Haftung ·
   Datenschutz beim Seitenaufruf · Datenschutz beim Feedback · Betroffenenrechte · keine
   Cookies. Verlinkt aus Footer und Formular. **Pflicht, sobald `feedback.html` portiert
   ist** — die Physik-Fassung des Formulars verlinkt relativ auf `rechtliches.html`, in
   Mathe liefe der Link sonst ins Leere.
2. **`feedback.html`**: Die Datei ist in beiden Projekten dieselbe und erkennt das Projekt
   selbst aus der URL. Die Physik-Fassung kann **1:1** übernommen werden; sie enthält den
   Datenschutzhinweis unter dem Senden-Knopf (erscheint erst mit ihm), den kleinen Fuss und
   die entschärften Platzhalter („freiwillig — kann leer bleiben" statt „leer lassen =
   anonym"; „anonym" lässt sich bei Übermittlung über einen externen Dienst nicht
   absolut versprechen).
3. **Header-Beschriftung**: aus „Feedback" wird „Kontakt & Feedback" — in Mathe heisst der
   Punkt heute `FEEDBACK` (eigener `.nav-btn nav-meta`-Eintrag, Desktop und Mobil).
4. **Über-Panel** (`nav.js`): Autor namentlich, Unabhängigkeit von SBFI/Kanton/Schule,
   KI-Einsatz mit redaktioneller Verantwortung, CC BY-NC 4.0 mit empfohlener Namensnennung.
   Die Physik-Texte sind wörtlich übertragbar, nur „TALS Physik" → „TALS Mathematik".
5. **Einheitlicher Footer** auf allen Seiten:

```html
<footer class="site-footer">
  <p><strong>TALS Mathematik</strong> — Lernmaterial für die Berufsmaturität …</p>
  <p>Mathematik · 3.2 Lineare Funktionen</p>          <!-- seitenspezifisch -->
  <p>© 2026 Raphael Arnold Kohler · <a href="…by-nc/4.0/deed.de">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version X · Stand …</p>
</footer>
```

   **Kein GitHub-Link im Footer.** Er steht genau einmal, im Über-Panel unter „Lizenz"
   („→ Quelltext und Inhalte des Lehrmittels (GitHub)"). Begründung: für Lernende ist
   „GitHub" Fachjargon und eine Dateiliste wirkt wie ein Fehler; wer das Repo sucht, liest
   es ohnehin aus der Domain `go4exercises.github.io/…`. Mathes heutiger Footer nennt
   „GitHub Pages" in Zeile 2 — der fällt weg.

**Vor dem Behaupten prüfen:** Die Aussage „keine Cookies" gilt nur, solange nichts im
Browser gespeichert wird. In Physik geprüft: kein `document.cookie`, kein
`localStorage`/`sessionStorage`/`indexedDB` im ganzen Projekt. In Mathe vor der
Veröffentlichung derselbe Grep. Ebenso die Löschfrist im Datenschutztext (12 Monate) —
sie muss zur tatsächlichen Praxis im Apps Script und im Postfach passen.

- [x] `rechtliches.html` erstellt (Texte aus Physik; Fach und Projektname angepasst, der
  Physik-Absatz zur Experimentsicherheit ersetzt durch die Haftung für externe Links).
  Wird **vor** `feedback.html` angelegt, damit der Datenschutzlink des Formulars trägt.
- [~] `feedback.html` aus Physik übernommen — **1:1, `diff` leer**. Endpunkt ist derselbe
  Apps-Script-URL wie bisher in Mathe (unverändert), Projekt wird aus der URL erkannt
  („TALS-Mathe"), Seite lädt bei 1280 px und 360 px ohne JS-Fehler.
  **Offen: ein echter Testversand** — der geht an das produktive Postfach und bleibt
  darum beim Auftraggeber.
- [x] Headerpunkt „Kontakt & Feedback" statt `FEEDBACK` (Desktop **und** Mobil).
  `rechtliches.html` bekommt bewusst *keinen* Headerpunkt — Verlinkung nur aus Footer
  und Formular, wie in Physik.
- [x] Über-Panel nachgeführt: Autor namentlich, Unabhängigkeit von SBFI/Kanton/Schule,
  KI-Einsatz mit redaktioneller Verantwortung; Ausblick auf den tatsächlichen Stand
  (beide Fächer vollständig, 23 + 23 Seiten); Lizenz mit empfohlener Namensnennung und
  GitHub-Link. Der GitHub-Link steht jetzt **genau einmal** — hier.
- [x] Footer auf allen 48 Seiten + `index.html` + `TEMPLATE.html` vereinheitlicht:
  Copyright-Zeile, „Kontakt & Feedback · Rechtliches & Datenschutz", „Keine Cookies ·
  Kein Tracking · Version 1.0 · Stand Juli 2026". Die Bereichszeile trennt neu
  einheitlich mit `·` („Grundlagenfach · 3.2 Lineare Funktionen").
  Der GitHub-Link in `index.html` Zeile 2 ist entfallen.
- [x] Cookie-Grep verifiziert: `document.cookie`, `localStorage`, `sessionStorage`,
  `indexedDB` kommen im ganzen Repo **nicht** vor. Extern geladen werden nur Google Fonts
  (49 ×) und MathJax über jsDelivr (48 ×); YouTube/Serlo/sos-mathe sind reine Links,
  **kein einziges `<iframe>`** — das steht so auch im Datenschutztext.
  Die Löschfrist (12 Monate) ist aus Physik übernommen und muss vom Auftraggeber gegen
  die tatsächliche Praxis im Apps Script und im Postfach gehalten werden.

---

## 9. Startseite straffen  — nur als Muster, nicht 1:1

**Was in Physik gemacht wurde:** Der Kopfbereich der Startseite hat rund 380 px verloren.
Die Kopfzeile rückt direkt unter den Header und schreibt sich gemischt
(„Berufsmaturität **T**echnik, **A**rchitektur, **L**ife **S**ciences — **TALS**", die
Anfangsbuchstaben und das abschliessende TALS in der Leitfarbe und fett); Titel und
Untertitel sind zu einer Zeile zusammengefasst; Chip-Reihe, Statuszeile („16 fertig · 0 in
Arbeit") und die Bereichs-Kopfzeile samt Fachbereichs-Zeile sind ersatzlos entfernt.
Die Kapitelliste steht damit ohne Scrollen im ersten Bildschirm.

**Mathe-Stand (29.07.2026 im Repo nachgesehen — KORREKTUR zur Absenderliste):**
Die Behauptung „`.hero-ew`, `.kap-hdr`, `.k-lek` und `.ds-grid` gibt es dort nicht" ist
**falsch**. Alle vier existieren in `index.html`: `.hero-ew` 3 ×, `.kap-hdr` 15 ×,
`.k-lek` 10 ×, `.ds-grid` 2 ×. Was zutrifft: keine davon steht in `style.css` — die
Startseite bringt ihr CSS in einem eigenen `<style>`-Block mit (Zeilen 9–125).
Daher stimmt nur die Schlussfolgerung, nicht die Begründung: es ist kein Port *nach
`style.css`*, sondern eine Änderung *in `index.html`* — und dort sind die Selektoren
dieselben wie in Physik.

Die eigentliche Frage bleibt: Was steht über der ersten Kapitelzeile, und wie viel davon
liest tatsächlich jemand?

**Mitgehende Kleinigkeiten aus demselben Durchgang** — beide Strukturen existieren in
Mathe, darum nachgemessen statt geschätzt:

- **Lange Statuszeilen in Kapitelköpfen** (`.k-lek`, `white-space: nowrap` +
  `margin-left: auto`): **trifft zu und ist ein echter Defekt.** Bei 360 px laufen
  **5 von 9** Kapitelköpfen rechts aus dem Bild, am schlimmsten „20 Lektionen ·
  3 Teilgebiete + Praxisbeispiel" mit 112 px Überstand. Bei 600 px und 1280 px passt alles.
  Gegenregel wie in Physik, im `<style>`-Block von `index.html`:
  `@media (max-width: 600px) { .k-lek { white-space: normal; text-align: right; } }`
- **Legenden-Kacheln auf feste Spaltenzahl statt `auto-fill`** (`.ds-grid`):
  **entfällt für Mathe.** `repeat(auto-fill, minmax(170px, 1fr))` ergibt gemessen
  5 Spalten für 5 Kacheln bei 1280 px (also bereits eine Reihe), 3 bei 600 px, 1 bei
  360 px — und in keiner Breite wird ein Wortbeispiel abgeschnitten. Nichts zu tun.

- [x] Startseite gesichtet (Playwright, gemessene Höhen bis zur ersten Kapitelzeile):
  **1280 px: 543 px** (Viewport 900) · **360 px: 715 px** (Viewport 740) — auf dem Handy
  ist damit von der Kapitelliste nichts zu sehen. Aufschlüsselung 1280 / 360 px:
  `.hero` 276 / 279 (davon `.chips` 27 / 97), `.stats` 49 / 105,
  `.bereich.b-gl` samt `.b-desc` 92 / 219.
  Die Kandidaten heissen `.chips`, `.stats` und `.bereich.b-gl`; sie stehen im
  `<style>`-Block von `index.html`, nicht in `style.css`.
- [~] **Entscheid: noch offen, bewusst nicht automatisch umgesetzt.** Empfehlung für den
  nächsten Durchgang, nach erwartetem Gewinn geordnet:
  1. `.bereich.b-gl` samt `.b-desc` (−92 / −219 px) — die Zeile „Mathematik —
     Grundlagenbereich" wiederholt, was das Kapitel-Badge daneben schon sagt.
  2. `.chips` (−27 / −97 px) — „18 Teilgebiete" / „13 Teilgebiete" steht redundant zur
     Statuszeile; der SBFI-Link gehört ins Dropdown „Nachschlagen", wo er bereits steht.
  3. `.stats` (−49 / −105 px) — **nur die Zahlenkachel.** Der Hinweis „▼ Lerngebiet
     anklicken zum Aufklappen" ist eine echte Bedienanleitung (die Kapitel sind
     zugeklappt) und muss bleiben, sonst findet niemand die Liste.
  Zusammen wären das rund **170 px auf dem Desktop und 420 px auf dem Handy** — genug,
  damit die Kapitelliste auf beiden Breiten ohne Scrollen beginnt.
  4. **Unabhängig vom Straffen und ohne Entscheidungsbedarf:** die `.k-lek`-Regel oben
     (5 von 9 Kapitelköpfen laufen bei 360 px rechts aus dem Bild). Das ist ein Fehler,
     keine Geschmacksfrage — steht hier nur, weil §9 als „nur Entscheid" beauftragt war.

---

## 10. Kleinteiliges aus demselben Durchgang

- [x] **Links im Über-Panel bleiben inline.** `.ueber-panel .meta-link { display:inline;
  padding:0; }` ergänzt. Gegengeprüft: der neue Schwesterprojekt-Link im Ausblick rendert
  mit `display: inline` und bleibt im Satz.
- [x] **`TOC_KURZ` für Nachschlagewerke gefüllt.** Formelsammlung hat `lg1`…`lg5`
  („Lerngebiet 1 · Arithmetik / Algebra" → „1 Arithmetik/Algebra" usw.), dazu die zwei
  Anker aus `rechtliches.html`. Gemessen: kein ToC-Label wird mehr abgeschnitten.
  Das Glossar braucht nichts — seine `<h2 id>` sind einzelne Buchstaben.
- [x] **Version und Datum zentral gesetzt.** Mathes Seiten trugen bisher *gar keine*
  Versions-/Standzeile; mit dem neuen Footer stehen jetzt alle einheitlich auf
  **Version 1.0 · Stand Juli 2026** (gleich wie Physik). `nav.js` behält seine eigene
  „Version 2.0" — das ist die Version der Navigationsstruktur, nicht des Lehrmittels.

**Bereits erledigt, nichts zu tun:** Die Regel `mjx-container[display="true"]
{ overflow-x:auto }` aus dem Physik-Durchgang vom 28.07.2026 steht in Mathes `style.css`
bereits (Zeile 1099).

### Verifikation pro Port
1. Mathe-Pre-Flight: `ALLE CHECKS BESTANDEN`.
2. `node --check` auf geänderte Inline-Scripts (macht der Pre-Flight i. d. R. mit).
3. Render-Check 1280 px + 360 px — in Mathe mit `.claude/tools/screenshot-widgets.mjs`,
   in Physik mit einem Playwright-Skript (Chromium liegt unter `~/.cache/ms-playwright/`).
4. CSS-Klammerbilanz: `python3 -c "s=open('style.css').read(); print(s.count('{')==s.count('}'))"`.
