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

## 9. Startseite straffen  (korrigiert 29.07.2026 — jetzt mechanisch)

> **Korrektur.** Die erste Fassung dieses Abschnitts behauptete, Mathe sei anders
> aufgebaut und ein CSS-Port sei nicht möglich. Das war falsch: gesucht wurde in
> `style.css`, die Startseiten-Regeln stehen aber in **beiden** Projekten im
> `<style>`-Block **innerhalb von `index.html`**. Mathes Startseite hat dieselbe
> Struktur wie Physik vor dem Umbau. Darum hier die konkreten Schritte.

**Ziel:** Die Kapitelliste beginnt im ersten Bildschirm. Gemessen bei 1280 px vor dem
Umbau: erste `.kap`-Zeile bei **y = 543 px** (Hero bis 330, `.stats` bei 362,
erster `.bereich` bei 451). Erwartung danach: rund 260–280 px.

**1 · Hero** (`index.html`, `<style>` und Markup)

```css
.hero    { padding: 16px 40px 28px; }        /* vorher 50px 40px 42px */
.hero-ew { letter-spacing: 1px; color: var(--tinte-2); }   /* text-transform: uppercase ENTFERNEN */
.hero-ew strong { font-weight: 700; color: var(--blau); }
```

```html
<!-- Text in EIN span: .hero-ew ist ein Flex-Container mit gap — einzelne <strong>
     würden sonst zu eigenen Flex-Items mit Lücken davor und danach. -->
<div class="hero-ew"><span>Berufsmaturität <strong>T</strong>echnik,
  <strong>A</strong>rchitektur, <strong>L</strong>ife <strong>S</strong>ciences —
  <strong>TALS</strong></span></div>
<h1>Mathematik <span>nach BM RLP 2030</span></h1>   <!-- vorher zwei Zeilen mit <br> -->
```

**2 · Ersatzlos löschen**

- `<div class="chips">…</div>` (drei Chips: „Grundlagenfach · 18 Teilgebiete",
  „Schwerpunktfach · 13 Teilgebiete", „📄 Formelsammlung SBFI"). Die ersten beiden
  wiederholen die Bereichsköpfe, der dritte doppelt den Menüpunkt.
- `<div class="stats">…</div>` (Zählzeile „46 Themenseiten fertig · 31 RLP-Teilgebiete
  + 2 TALS-Ergänzungen · ▼ Lerngebiet anklicken zum Aufklappen").
- die **beiden** `<div class="b-desc">…</div>` (lange FH-Fachbereichs-Sätze in
  `#gl` und `#sp`).

**Nicht löschen:** die beiden `.bereich`-Köpfe selbst (`.bh` mit `.b-badge` und
`.b-titel`). Sie trennen Grundlagen- und Schwerpunktfach — das ist Inhalt, keine Deko.
Weil sie bleiben, entfällt der Physik-Zusatz `.kap:first-of-type { border-top … }`:
die Bereichsköpfe tragen den oberen Rahmen weiter.

**3 · Farbcode-Legende und Kapitelzeilen** (dieselbe Datei)

```css
/* feste Spaltenzahl statt auto-fill — Mathe hat FÜNF Kacheln, Physik sechs */
.ds-grid { grid-template-columns: repeat(5, 1fr); }

@media (max-width: 900px) { .ds-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 600px) {
  .hero { padding: 16px 16px 22px; }          /* vorher 28px 16px 24px */
  .ds-grid { grid-template-columns: repeat(2, 1fr); }
  /* Lektionsangabe darf umbrechen, sonst läuft die Kapitelzeile rechts aus dem Bild */
  .kap-hdr { align-items: flex-start; }
  .k-lek   { white-space: normal; text-align: right; line-height: 1.4; }
  .k-nr, .k-name { padding-top: 1px; }
}
```

**4 · Abstände unter dem Titel** (nachgezogen 30.07.2026)

Nach dem Entfernen der Chips steht der Titel als letztes Element im Hero — seine
`margin-bottom` ist dann toter Raum, und die alten Polsterwerte sind auf einen Hero mit
drei Elementen ausgelegt. Vier Werte, in Physik gemessen und übernommen:

```css
.hero    { padding: 16px 40px 18px; }   /* Unterkante 28 → 18 */
.hero h1 { margin-bottom: 0; }          /* vorher 12px — nur richtig, wenn .chips weg ist */
.page    { padding: 18px 22px 80px; }   /* Oberkante 32 → 18 */

@media (max-width: 600px) {
  .hero { padding: 16px 16px 14px; }    /* Unterkante 22 → 14 */
  .page { padding: 12px 12px 60px; }    /* Oberkante 18 → 12 */
}
```

**Mathe-Stand (30.07.2026 nachgesehen):** `.hero { padding: 16px 40px 28px }`,
`.hero h1 { margin-bottom: 12px }`, `.page { padding: 32px 22px 80px }` und mobil
`16px 16px 22px` / `18px 12px 60px` — also genau die Physik-Werte vor dieser Änderung.
Der Diff passt damit wörtlich, sobald Schritt 2 (`.chips` entfernt) erledigt ist.

**Wirkung in Physik**, gemessen als Abstand von der Titel-Unterkante bis zur ersten
Kapitelzeile:

| Breite | vorher | nachher |
|---|---:|---:|
| 1280 px | 73 px | **37 px** |
| 360 px | 53 px | **27 px** |

**Prüfen:** bei 1280 px die Position der ersten `.kap`-Zeile vorher/nachher vergleichen,
bei 360 px `document.body.scrollWidth === document.documentElement.clientWidth`
(kein Horizontalscroll) und die fett gesetzten T·A·L·S auf Lesbarkeit sichten.

- [x] Hero gestrafft, Kopfzeile gemischt in **einem** `<span>` mit `<strong>`-Initialen
  und abschliessendem **TALS**, `text-transform: uppercase` entfernt, Titel einzeilig.
- [x] `.chips`, `.stats` und **beide** `.b-desc` aus dem Markup entfernt; die zwei
  `.bereich`-Köpfe (`#gl`, `#sp`) stehen unverändert, `.kap:first-of-type` daher **nicht**
  übernommen — gemessen sitzt die erste `.kap`-Zeile nahtlos unter dem Kopf, kein
  doppelter Rahmen und keine Lücke. Die verwaisten CSS-Regeln (`.chips`, `.chip`, `.c-*`,
  `.stats`, `.st*`, `.b-desc`) bleiben stehen — in Physik ebenso, damit die Dateien
  vergleichbar bleiben.
- [x] `.ds-grid` auf `repeat(5, 1fr)`, gestuft 3 Spalten ab 900 px und 2 ab 600 px.
  Gemessen 1280/900/600/360 px: 5/3/2/2 Spalten, nirgends abgeschnittener Text.
- [x] `.k-lek` bricht unter 600 px um. Vorher liefen bei 360 px **5 von 9** Kapitelköpfen
  rechts aus dem Bild (bis 112 px Überstand), jetzt **0 von 9**.
- [x] Abstände unter dem Titel nach Schritt 4 — die vier Werte passten wörtlich:
  `.hero` 28 → 18, `.hero h1` `margin-bottom` 12 → 0, `.page` 32 → 18, mobil `.hero`
  22 → 14 und `.page` 18 → 12.
  **Ein fünfter Wert kam dazu, der in §9 fehlt:** `.hero-ew { margin-bottom }` stand in
  Mathe auf **14 px**, in Physik schon vor Schritt 4 auf **10 px**. Die Aussage
  „Mathes Startseite steht heute genau auf den Physik-Werten vor dieser Änderung" trifft
  also für die vier Werte zu, für `.hero-ew` nicht. Mit den 10 px ist die Hero-Höhe bei
  1280 px in beiden Projekten identisch: **123 px**.
- [x] Render-Check 1280 / 900 / 600 / 360 px: kein Horizontalscroll auf allen Breiten
  (`body.scrollWidth − documentElement.clientWidth = 0`), keine JS-Fehler,
  T·A·L·S lesbar, `.k-lek` überall im Rahmen.

> **Messung Mathe gegen Physik**, beide am 30.07.2026:
>
> | | Mathe 1280 | Physik 1280 | Mathe 360 | Physik 360 |
> |---|---:|---:|---:|---:|
> | Hero-Höhe | **123** | **123** | 144 | 111 |
> | Titel-Unterkante → erste `.kap` | 142 | 37 | 195 | 27 |
> | erste `.kap` bei y | 300 | 195 | 379 | 177 |
>
> Die Hero-Höhe ist bei 1280 px auf das Pixel gleich — die Abstände sind vollständig
> übertragen. Die beiden verbleibenden Unterschiede sind **kein** Abstandsproblem:
>
> 1. **105 px** Titel→`.kap` gehen auf den Bereichskopf, den Mathe absichtlich behält
>    (`margin-top: 40px` + 65 px Eigenhöhe). Physik hat ihn gelöscht. Zieht man ihn ab,
>    bleiben 37 px — genau der Physik-Wert.
>    **Nachtrag 30.07.2026:** Davon sind 40 px zurückgeholt. Der Bereichskopf startet
>    jetzt auf **derselben Höhe wie in Physik die Kapitelliste** — beide bei y = 195 px
>    (1280 px). Dazu eine Zeile:
>    `.page > .bereich:first-child { margin-top: 0; }`
>    Die 40 px trennen Grundlagen- von Schwerpunktfach; über dem ersten Block gibt es
>    nichts zu trennen, und `.page` bringt schon 18 px `padding-top` mit. `#sp` behält
>    seine 40 px, der Trenner zwischen den Fächern bleibt also unangetastet.
>    Damit liegt die erste `.kap`-Zeile bei **260 px** — im Zielkorridor 260–280 aus §9.
>    Gemessen 1280/900/600/360 px: Bereichskopf startet exakt am Inhaltsanfang von
>    `.page` (195/185/167/210), `margin-top` `#gl` = 0, `#sp` = 40 px.
> 2. Bei 360 px ist Mathes Hero 33 px höher, weil „Mathematik nach BM RLP 2030" dort auf
>    zwei Zeilen umbricht und „Physik nach BM RLP 2030" nicht. Das ist die Wortlänge des
>    Fachnamens, keine Polsterung.
>
> Verglichen mit dem Stand vor §9 liegt die erste `.kap`-Zeile bei 1280 px damit bei
> **260 statt 543 px** (−283 px).
>
> **Eine Abweichung bleibt bewusst offen:** `.ds` (Kasten der Farbcode-Legende, *unter*
> der Kapitelliste) — Physik `margin-top: 50px; padding: 14px 18px`, Mathe
> `margin-top: 44px; padding: 18px 22px`. Betrifft den ersten Bildschirm nicht und steht
> in keinem §9-Schritt; angleichen wäre eine reine Geschmacksentscheidung.

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

---

## 11. Mobilmenü als Spiegel der Kopfzeile  (`nav.js` + `style.css`, 04.08.2026)

Quelle: Physik-Commit `f592eb8`. Anlass: bei starkem Browser-Zoom klappt die Kopfzeile
in den Burger — und das Burger-Menü war die schwächste Stelle des ganzen Lehrmittels.

**Was:** Das Mobilmenü listet nicht mehr alle Seiten flach untereinander, sondern
spiegelt die Kopfzeile als Klapp-Sektionen: *← Übersicht · Grundlagenfach ·
Schwerpunktfach · Nachschlagen · Physik ↗ · Über dieses Lehrmittel · Kontakt & Feedback*.
Zweite Klappebene sind die Lerngebiete je Bereich. Beim Öffnen ist genau der Bereich der
aktuellen Seite offen und darin ihr Lerngebiet.

**Warum:** In Mathe stehen 55 Links und 2641 px Inhalt in einem 745 px hohen Fenster —
dreieinhalb Bildschirme Scrollen, ohne erkennbare Hierarchie (Lerngebiets-Überschriften
0.58 rem Mono gegen 0.85 rem Links). Genau dieses Menü braucht man bei starkem Zoom.
Gemessen nach dem Umbau (Playwright, 360 px, auf einer Kopie des Repos gefahren):

| Seite | vorher | nachher | offen beim Öffnen |
|---|---|---|---|
| `index.html` | 2641 px | 575 px | Grundlagenfach |
| `grundlagen/g5-2a-dreiecke.html` | 2641 px | 879 px | Grundlagenfach › 5 · Geometrie |
| `schwerpunkt/s3-1-grundlagen.html` | 2641 px | 818 px | Schwerpunktfach › 3 · Funktionen |
| `glossar.html` | 2641 px | 475 px | Nachschlagen |

Sichtbare Links beim Öffnen: 3 auf der Startseite, 11 auf einer Kapitelseite (vorher 55).

**Nicht übertragen — bewusst:** Physik hat im selben Commit den Burger-Breakpoint von
1024 px auf 880 px gesenkt und das «Über»-Dropdown ab 1000 px auf die Spaltenvariante
gestellt. **Beides gehört nicht nach Mathe.** Die Mathe-Kopfzeile hat sechs statt fünf
Einträge mit längeren Labels und braucht real 1009 px (Logo 94 + Nav 633 + Suche 190 +
Polsterung/Gaps 112); der erste Überlauf wurde bei 1009 px gemessen. Die dortigen 1024 px
sind also bereits die richtige Kante — auch mit gekürzten Buttons («Grundlagen» /
«Schwerpunkt») läge sie erst bei 961 px. Und Mathes `.dd-menu-ueber` öffnet mit
`right: 0` rechtsbündig, ragt also nirgends hinaus; die Physik-Korrektur war dort nur
nötig, weil das Menü mit `left: 0` am Button klebt.

**Wie:** Ein fertiges Skript liegt unter
`_intern/uebertrag-physik-nav/transfer-mathe-mobilnav.py` (gitignoriert, mit `--dry-run`;
es prüft jeden Ankertext auf genau ein Vorkommen und bricht sonst ab):

```bash
python3 _intern/uebertrag-physik-nav/transfer-mathe-mobilnav.py --root . --dry-run
python3 _intern/uebertrag-physik-nav/transfer-mathe-mobilnav.py --root .
```

Fehlt das Skript, sind es vier Ersetzungen von Hand:

**(a) `nav.js` — `renderMobileGroup(bereich)`:** statt `<div class="mn-untergruppe">`
je Lerngebiet ein `<details class="mn-lg">`; offen ist es, wenn es die aktuelle Seite
enthält. Die Lerngebietsnummern wiederholen sich zwischen den Bereichen, darum
entscheidet die ID-Liste, nicht `g.nr`:

```js
      return `<details class="mn-lg"${g.ids.indexOf(cfg.id) !== -1 ? ' open' : ''}>
        <summary>${g.nr} · ${g.titel}</summary>
        <div class="mn-lg-body">${items}</div>
      </details>`;
```

**(b) `nav.js` — direkt darunter die Aufklapp-Logik.** Achtung: die Startseite ruft
`buildNav({ bereich:'index', homepage:true })`, deshalb wird gegen `'schwerpunkt'`
geprüft und nicht auf ein fehlendes `cfg.bereich` — sonst bleibt auf `index.html`
alles zu:

```js
  const refAktiv = (cfg.id === 'glossar' || cfg.id === 'formeln');
  const spOffen  = (cfg.bereich === 'schwerpunkt');
  const glOffen  = !spOffen && !refAktiv;
```

**(c) `nav.js` — das `<div class="mobile-nav">`-Markup** in Sektionen fassen (Reihenfolge
wie in der Kopfzeile, „Physik ↗" rückt dabei hinter „Nachschlagen"):

```html
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}" class="mn-direkt">← Übersicht</a>
  <details class="mn-sektion"${glOffen ? ' open' : ''}>
    <summary>Grundlagenfach</summary>
    <div class="mn-sektion-body">${renderMobileGroup('grundlagen')}</div>
  </details>
  <details class="mn-sektion"${spOffen ? ' open' : ''}>
    <summary>Schwerpunktfach</summary>
    <div class="mn-sektion-body">${renderMobileGroup('schwerpunkt')}</div>
  </details>
  <details class="mn-sektion"${refAktiv ? ' open' : ''}>
    <summary>Nachschlagen</summary>
    <div class="mn-sektion-body">… die drei bisherigen Nachschlage-Links …</div>
  </details>
  <a href="https://go4exercises.github.io/TALS-Physik/" target="_blank" rel="noopener" class="mn-direkt">Physik ↗</a>
  <details class="mn-sektion">
    <summary>Über dieses Lehrmittel</summary>
    <div class="mn-sektion-body">… die drei bisherigen &lt;details class="mn-meta"&gt; …</div>
  </details>
  <a href="${prefix}feedback.html" class="mn-direkt">Kontakt &amp; Feedback</a>
</div>
```

**(d) `style.css` — `.mn-gruppe` und `.mn-untergruppe` ersetzen** (beide werden danach
nirgends mehr benutzt) durch `.mn-direkt`, `.mn-sektion`(+`-body`) und `.mn-lg`(+`-body`).
Der vollständige Block steht im Skript; Farbe ist `--blau` (in Physik `--bernstein`),
Schriftgrössen bewusst grösser als die alten Mono-Versalien — 0.9 rem für die Sektionen,
0.78 rem für die Lerngebiete statt 0.58 rem —, weil das Menü gerade bei starkem Zoom
gebraucht wird.

**Verifikation:** zusätzlich zur Liste oben den Burger bei 360 px auf `index.html`, je
einer Grundlagen- und einer Schwerpunktseite sowie auf `glossar.html` öffnen und prüfen,
welche Sektion aufgeklappt ist.

**Commit-Message:**
`Nav: Mobilmenue als Spiegel der Kopfzeile mit Klapp-Sektionen (Uebertrag aus Physik f592eb8)`

**[x] Umgesetzt am 04.08.2026** — per Skript (alle vier Ankertexte genau 1× gefunden).
`node --check nav.js` sauber, CSS-Klammerbilanz ausgeglichen, keine Restvorkommen von
`.mn-gruppe`/`.mn-untergruppe` mehr im Repo. Pre-Flight über alle 46 Themenseiten:
`ALLE CHECKS BESTANDEN`. Gegenprobe im Repo selbst (Playwright, 360 px, Burger geöffnet)
reproduziert die Tabelle oben exakt — 575 / 879 / 818 / 475 px, offen jeweils
Grundlagenfach · Grundlagenfach › 5 · Geometrie · Schwerpunktfach › 3 · Funktionen ·
Nachschlagen; sichtbare Links 3 / 11 / 11 / 6 (`checkVisibility`), kein Querüberlauf.

---

## 12. Über-Panel: Autorenbild und kürzerer Reiter  (`nav.js` + `style.css` + 1 Bild, 04.08.2026)

Quelle: Physik-Commits `640a52a` (Bild) und `2dddb9d` (Reiter). Betrifft dasselbe
Über-Panel wie Punkt 11 und ist unabhängig davon anwendbar.

### 12a — Rundes Autorenbild

**Was:** Im Über-Panel steht links oben ein rundes Porträt, um das der Text herumläuft —
Optik eines Benutzerbildes, aber rund zehnmal so viel Fläche (112 px Durchmesser gegen
die üblichen ~36 px; 9852 px² gegen 1018 px²). Auf schmalen Menüs fällt es auf 88 px.

**Warum:** Das Panel war reiner Fliesstext; ein Gesicht macht die Autorenangabe
persönlicher, ohne Platz zu kosten. Es ist derselbe Autor wie in Physik, das Bild
lässt sich also unverändert übernehmen.

**Bild:** `autor.jpg` aus dem Physik-Repo-Root kopieren — 256 × 256 px, 12 KB, JPEG
Qualität 82, **ohne Exif**. Wichtig: nicht das Originalfoto einchecken; das Original
war 2323 × 3001 px, 1.09 MB und trug GPS-Koordinaten sowie Aufnahmedatum im Exif — das
Repo ist die veröffentlichte Website. Der Zuschnitt entstand mit Pillow aus dem
Original (`crop((150, 60, 2250, 2160))`, danach `resize((256,256), LANCZOS)` und
`save(..., quality=82, optimize=True, progressive=True)`; das Neuspeichern wirft die
Exif-Daten weg).

```bash
cp /home/paps/tals-physik/autor.jpg .
```

**`nav.js` — in `metaAutorHTML` direkt nach der `meta-titel`-Zeile einfügen:**

```js
    <img class="meta-portrait" src="${prefix}autor.jpg" width="112" height="112" loading="lazy"
         alt="Porträt von Raphael Arnold Kohler (Aquarell)">
```

**`style.css` — neuer Block, sinnvoll direkt nach `.ueber-panel .meta-link:hover`:**

```css
/* Autorenbild im Ueber-Panel: rund wie ein Benutzerbild, aber rund zehnmal so
   viel Flaeche (112px Durchmesser gegen die ueblichen ~36px). Der Text laeuft
   um das Bild herum; auf schmalen Menues faellt es auf 88px zurueck. */
.meta-portrait {
  float: left; width: 112px; height: 112px;
  margin: 2px 14px 6px 0;
  border-radius: 50%; object-fit: cover;
  border: 1.5px solid var(--blau-rand);      /* Physik: --bernstein-rand */
  box-shadow: var(--s);
}
```

**Und die Verkleinerung in den bestehenden `@media (max-width: 720px)`-Block**
(`style.css:216`) — **nicht** in einen 1000-px-Block wie in Physik: dort war die Grenze
wegen des tieferen Burger-Breakpoints hochgezogen worden, den Mathe nicht übernimmt
(siehe Punkt 11). In Mathe deckt die 720-px-Kante den relevanten Fall ab, weil das
Desktop-Dropdown mit 400 px Panelbreite für 112 px reicht und das Burger-Menü ohnehin
schmaler als 720 px ist:

```css
  .meta-portrait { width: 88px; height: 88px; margin-right: 11px; }
```

### 12b — Reiter heisst nur noch «Autor»

**Was:** «Autor & Intention» → «Autor», an drei Stellen in `nav.js`. Die Tab-ID
`ueber-autor` und das `data-target` bleiben unverändert.

**Wie:**

```bash
python3 - <<'PY'
import pathlib
p = pathlib.Path('nav.js'); s = p.read_text(encoding='utf-8')
print(s.count('Autor &amp; Intention'), 'Stellen')      # erwartet: 3
p.write_text(s.replace('Autor &amp; Intention', 'Autor'), encoding='utf-8')
PY
```

Betroffen sind in Mathes `nav.js` die Panel-Überschrift (Zeile 135), der Reiter-Button
(237) und die Klappe im Burger-Menü (280).

**Verifikation:** `node --check nav.js`; Über-Panel bei 1280 px öffnen (Bild rund,
112 px, Text läuft herum, Reiter «Autor») und bei 360 px im Burger unter
«Über dieses Lehrmittel → Autor» (Bild 88 px).

**Commit-Message:**
`Ueber-Panel: rundes Autorenbild und Reiter «Autor» (Uebertrag aus Physik 640a52a, 2dddb9d)`

**[x] Umgesetzt am 04.08.2026** — `autor.jpg` übernommen (256 × 256, 12 KB, 0 Exif-Bytes
gegengeprüft), `.meta-portrait` in `metaAutorHTML`, CSS-Block nach
`.ueber-panel .meta-link:hover` und die 88-px-Regel im bestehenden 720-px-Block.
«Autor &amp; Intention» an genau 3 Stellen ersetzt (Panel-Überschrift, Reiter-Button,
Burger-Klappe); `ueber-autor`/`data-target` unverändert. `node --check nav.js` sauber,
CSS-Klammerbilanz ausgeglichen, Pre-Flight über alle 46 Themenseiten bestanden.
Gemessen (Playwright): 1280 px → 112 × 112 px, `border-radius: 50%`, `float: left`,
Text läuft herum, Reiter «Autor · Ausblick · Lizenz»; 360 px im Burger → 88 × 88 px,
innerhalb der Menübreite. Screenshots beider Breiten gesichtet.
