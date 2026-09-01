# HOWTO — Erklärclip bauen und einbauen

Ein Clip ist eine kurze, stumme Animation, die einen einzelnen Gedankengang Zeile für
Zeile aufbaut — kein Video, sondern eine HTML-Seite von rund 17 kB. Kein MP4, kein
Drittanbieter, scharf auf jedem Bildschirm.

Verwandte Dokumente: `STYLEGUIDE.md` (§5.3.1 keine Drittanbieter), `HOWTO-neue-themenseite.md`,
`CLAUDE.md` (Pre-Flight und Commit-Regel).

---

## Überblick

```
clips/
  <lektion>-<kurzname>.json          ← das Drehbuch. Die einzige Quelle.
  <lektion>-<kurzname>.html          ← generiert
  sprechertext-<lektion>-<kurzname>.txt   ← generiert, wird zum Transkript
  clips.json                         ← generierter Index
  themes/  begreifbar | heft | tafel | papier
  vorlage.json                       ← kommentierte Drehbuch-Vorlage
scripts/build-clips.py               ← Drehbuch  → Clip
scripts/build-clips-einbau.py        ← Clip      → Lektionsseite
```

Von Hand geschrieben wird **nur das Drehbuch**. Alles andere ist erzeugt und wird
mitversioniert, weil GitHub Pages nichts baut.

---

## Schritt 1 — Drehbuch schreiben

`clips/vorlage.json` kopieren nach `clips/<lektion>-<kurzname>.json` und ausfüllen. Alle
Felder, die mit `_` beginnen, sind Kommentare und werden ignoriert — sie dokumentieren
die Formelschreibweise, die Elementtypen und die Farbführung direkt in der Vorlage.

Drei Felder entscheiden über den Einbau:

| Feld | Bedeutung |
|---|---|
| `dateiname` | ohne Endung, ohne Umlaute — daraus werden `.html` und Sprechertext |
| `lektion` | **Liste** von Codes aus `nav.js`, z.B. `["g2-2b", "s2-2a"]`. Der **erste** Code ist die Heimatlektion: Dort steht der Clip in der Reihe, auf den übrigen Seiten hängt er als Gast hinten an. |
| `reihe` | didaktische Familie, z.B. `Parametergleichung` |
| `folge` | Platz in dieser Reihe: 1, 2, 3 … — weglassen bei Ergänzungen |
| `theme` | `begreifbar` ist Standard und übernimmt die Farben aus `style.css` |

### Titel: «Reihe: Fokus»

Ein Clip beantwortet **eine** Frage, und der Titel sagt welche:

```
Parametergleichung: nach x auflösen          folge 1
Parametergleichung: Bedingung für Lösung     folge 2
Lineare Gleichungen: Minus vor der Klammer   folge 1
```

Der Teil vor dem Doppelpunkt ist die `reihe`, der Teil danach der Fokus. In der
Bibliothek stehen Clips derselben Reihe beieinander und in der Reihenfolge ihrer
`folge` — die Nummer steht als Plakette vor dem Titel.

**Jede Reihe bekommt eine eigene Farbnuance**, in der Reihenfolge ihres Auftretens; bei
der nächsten Reihe wird weitergeschaltet, nach acht beginnt der Zyklus von vorn. Die Farbe
sitzt an der Plakette **und** an der linken Kante der Zeile — ein 19-px-Kreis allein
gruppiert zu schwach, die Kanten aufeinanderfolgender Clips bilden dagegen einen
durchgehenden Balken. Es sind bewusst nur Nuancen der Bereichsfarbe (blau im
Grundlagenfach, violett im Schwerpunktfach): Die didaktischen Farben aus §5.1 bedeuten
etwas, und sie für eine Gruppierung zu verwenden hiesse, sie umzudeuten. Alle Nuancen
tragen weisse Schrift mit mindestens 4.9 Kontrast, nachgerechnet.

**Innerhalb eines Lerngebiets steht zuerst der eine Zweig, dann der nächste** — im
Lerngebiet 1 also erst die Clips zur Arithmetik, dann die zur Algebra: Man rechnet mit
Zahlen, bevor man mit Buchstaben rechnet. Die Reihenfolge steht als Liste `ZWEIGE` in
`scripts/build-clips-einbau.py` und liest den Zweig aus dem Feld `themenbereich`. Was
dort nicht aufgeführt ist, kommt alphabetisch dahinter. Clips ohne `folge` sind
Ergänzungen und rutschen ans Ende ihrer Reihe; sie tragen einen Punkt statt einer Zahl.

Warum so und nicht «ein Clip für den ganzen Ablauf, dann Beispiel 1, Beispiel 2»: Eine
Minute reicht für einen Gedanken, nicht für ein Verfahren mit vier Schritten und drei
Fällen. Und «Beispiel 2» sagt niemandem, was darin zu holen ist, während «Bedingung für
Lösung» genau das sagt. Wer später doch einen Überblicks-Clip je Reihe will: `folge: 0`
ist frei und sortiert sich von selbst nach vorn.

**`lektion` ist eine Liste, auch bei nur einem Eintrag.** Ein Clip gehört oft auf mehrere
Seiten: die Bruchgleichung steht im Grundlagenfach unter `g2-2b` und im Schwerpunktfach
unter `s2-2a`. Ohne Liste müsste man ihn duplizieren, und zwei Kopien laufen auseinander.
Jeder Code muss zu einer `id` in `nav.js` passen — `build-clips-einbau.py` meldet einen
Tippfehler als `[FEHLER]`.

### Formelschreibweise — LaTeX

**Formeln stehen in LaTeX**, gesetzt von MathJax, genau wie auf den Lektionsseiten. Der
Grund ist nicht Schönheit, sondern Wegfall einer Übersetzung: Eine Formel lässt sich von
einer Seite ins Drehbuch kopieren, ohne sie in eine zweite Schreibweise zu übertragen —
und jede Übertragung war eine Gelegenheit für einen Fehler.

```
\dfrac{4}{11}          Bruch — \dfrac, nicht \frac: \frac wird in der Zeile klein
x^2   x_{1,2}          hoch- und tiefgestellt
\cdot \pm \neq \leq \geq \longrightarrow \Longrightarrow
\in \notin \setminus \cap \cup  \mathbb{R}  \sqrt{x}  \overline{36}
\quad                  sichtbarer Abstand innerhalb einer Zeile
```

**Zwei Dinge, die LaTeX anders will als die frühere eigene Schreibweise:**

**Prosa braucht `\text{…}`.** Die alte Schreibweise kursivierte nur *einzelne* Buchstaben,
darum durfte «es entstehen Faktoren» unmarkiert mitten in einer Formelzeile stehen. In
LaTeX wären das zwanzig kursive Variablen mit falschen Abständen. Also
`\text{es entstehen Faktoren}` — und **ein** `\text{}` um den ganzen Satz, nicht eines je
Wort, sonst setzt LaTeX zwischen die Wörter Mathe-Abstände.

**Einheiten gehören in `\mathrm{}`, mit `\,` davor.** `1.2\,\mathrm{m}` — ohne das `\,`
klebt die Einheit an der Zahl, weil LaTeX ein gewöhnliches Leerzeichen ignoriert.

### Koordinatenbild — `typ: "graf"`

Für Clips, die eine Gerade zeigen müssen. Kein Diagrammwerkzeug, nur so viel, wie ein
Clip braucht: Achsen mit Teilung, Geraden über Steigung und Achsenabschnitt, markierte
Punkte. Gezeichnet wird als SVG in den Theme-Farben.

```json
{"typ": "graf", "breite": 800, "hoehe": 620, "abstand": 650,
 "xbereich": [-1, 5], "ybereich": [-1, 8],
 "geraden": [{"m": -2, "q": 7, "farbe": 1, "beschriftung": "y = −2x + 7",
              "beschriftung_bei": [3.55, 1.15]},
             {"m": 2, "q": 1, "farbe": 2, "gestrichelt": true, "dicke": 9}],
 "punkte":  [{"x": 2, "y": 3, "farbe": 3, "beschriftung": "S(2 | 3)"}]}
```

Parabeln gehen genauso, als `parabeln` mit `a`, `b`, `c` für \(y = ax^2+bx+c\) —
gezeichnet als Streckenzug, der ausserhalb des Fensters abbricht und danach wieder
einsetzt.

Die Geraden werden **am Fenster** abgeschnitten, nicht an ihren Endpunkten — eine
Gerade, die aus dem Bild läuft, hört am Rand auf statt an einer willkürlichen Stelle
davor. `farbe` ist 1 bis 4 wie bei den Farbgruppen.

**Der senkrechte Strich `|` bricht im Fliesstext die Zeile.** Wer in einer Notiz
\(2|a|\) schreiben will, packt es in `@…@` — dort ist der Strich geschützt. Sonst steht
die Hälfte des Satzes auf einer neuen Zeile und die Betragsstriche sind weg.

**`abstand` von Hand setzen**, sonst überschreibt die nächste Zeile das Bild: Der
senkrechte Fluss nimmt ohne Angabe `hoehe` als Abstand, und dann beginnt die nächste
Zeile genau an der Unterkante. Faustregel: `hoehe` plus 30.

In einer Szene mit Merkschiene ist das Bild **nicht** zentriert (dort ist nichts
zentriert) — es steht bei `x`, standardmässig 680. Ein eigenes `x` richtet es an den
Formelzeilen darüber aus.

### Farbführung

`{1:x-2}` färbt einen Term ein — Text und weiche Fläche. Zweck ist ausschliesslich,
denselben Term über mehrere Zeilen hinweg wiedererkennbar zu machen: man sieht, was von
wo nach wo wandert.

**1 und 2 (Blau/Orange) sind das sichere Paar**, auch bei Rotgrünschwäche. Dass Orange
auf den Seiten „Aufgabe" markiert, ist hier kein Widerspruch: im Clip markiert Farbe
einen Term, nicht einen Blocktyp. Sparsam bleiben — ein Bild mit sechs Farben erklärt
nichts mehr.

---

## Schritt 2 — Clip bauen

```sh
python3 scripts/build-clips.py                      # alle
python3 scripts/build-clips.py g2-2b-bruchgleichungen
python3 scripts/build-clips.py g2-2b-bruchgleichungen --eigenstaendig
```

Braucht nur Python 3. Der Lauf gibt die Szenenzeiten aus — daran sieht man sofort, ob
eine Szene zu hetzt oder steht.

`clips.json` wird **fortgeschrieben**, nicht überschrieben: Ein Lauf für einen einzelnen
Clip lässt die übrigen Einträge stehen und entfernt nur solche, deren HTML-Datei nicht
mehr existiert.

Die eigenständige Fassung (rund 480 kB) bettet die Schriften ein und läuft ohne die
Site — für Moodle, zum Verschicken, fürs Archiv. Nicht routinemässig bauen und **nicht
committen**; die Web-Fassung ist die gepflegte.

---

## Schritt 3 — In die Lektionsseite einbauen

Einmal pro Seite die beiden Kommentarzeilen setzen, sinnvollerweise direkt vor
`<h2 id="ressourcen">` — erst die eigenen Clips, dann die fremden Links:

```html
<!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS:ENDE -->
```

Danach:

```sh
python3 scripts/build-clips-einbau.py               # Probelauf
python3 scripts/build-clips-einbau.py --schreiben
```

Das Skript liest `clips/clips.json`, holt die Zuordnung Lektion → Datei aus `nav.js` und
schreibt zwischen die Marker: eine `<h2 id="clips">`-Überschrift (die Seiten-Navigation
nimmt sie automatisch auf), darunter **dieselbe zweispaltige Auswahl wie in der
Bibliothek** und darunter die Transkripte in einem Aufklapper.

Es ist dieselbe Aufgabe wie dort, also dieselbe Form: eine Zeile aus Nummer, Titel und
Laufzeit; der Clip läuft **gross über dem Fenster**, nicht in der Zeile. Auch die Ordnung
ist dieselbe — Reihen alphabetisch, darin nach `folge`.

Die Transkripte stehen gesammelt unter der Auswahl, jedes mit seiner eigenen
`<h3 id="clip-…" class="clip-h">`. Diese Überschrift ist nicht Schmuck: An ihr schneidet
`build-suchindex.py` seine Abschnitte, und der Transkripttext ist das Einzige, was Suche
und Suchmaschine von einem animierten Clip überhaupt sehen. Wer den Aufklapper entfernt,
nimmt den Clips ihre Auffindbarkeit.

Damit ein Suchtreffer nicht in einem zugeklappten `<details>` verschwindet, öffnet
`mathlib.js` beim Laden alle `<details>` über dem Sprungziel aus `location.hash`.

Früher stand hier je Clip

```html
<h3 id="clip-<dateiname>" class="clip-h">Titel</h3>
<p class="clip-text">Kurzbeschrieb</p>
<div class="clip" data-clip="…" data-titel="…">
  <button class="clip-start" …>▶ 1:21</button>
</div>
<details class="clip-transkript">…</details>
```

**Die eigene `h3` je Clip ist nicht Schmuck.** `scripts/build-suchindex.py` schneidet an
`h3.clip-h[id]` einen eigenen Abschnitt. Ohne sie heisst in den Suchergebnissen jeder
Clip einer Seite „Clips" und alle führen auf dasselbe Sprungziel. Weil der Titel damit in
der Überschrift steht, trägt der Knopf nur noch das Dreieck und die Dauer — er ist rund
67 × 29 px gross statt einer Karte über die volle Breite. Im Inhaltsverzeichnis der Seite
taucht er nicht auf: `buildToC` nimmt nur `h2`.

**Der Clip wird nicht beim Seitenaufruf geladen.** Sichtbar ist zuerst nur der Knopf;
erst der Klick setzt das `<iframe>` ein (`clipStart` in `mathlib.js`). So läuft bei
mehreren Clips auf einer Seite keiner von selbst los, und die Seite lädt nicht N
zusätzliche Dokumente mit. Der Clip startet dann von selbst — er ist frisch eingesetzt,
sein Autostart ist genau richtig.

**In der Bibliothek läuft er gross.** Dort trägt die Karte `data-modus="gross"`, und
`clipStart` legt statt des Rahmens in der Zeile eine Bühne über das Fenster — rund 80 %
der Fensterfläche statt einer schmalen Spalte. Escape oder ein Klick auf den dunklen Rand
schliesst sie, der Clip hält an.

Warum kein neuer Tab: Er verlässt die Liste, und ein vergessener Tab spielt weiter. Fürs
Projizieren oder Verschicken führt im Kopf der Bühne trotzdem ein Link **eigener Tab ↗**
auf die Clipdatei.

**Auf der Lektionsseite läuft er weiterhin an Ort und Stelle** — dort gehört er zwischen
Theorie und Aufgaben, nicht über die Seite gelegt. Gesteuert wird das allein über
`data-modus`; ohne das Attribut bleibt es beim Rahmen in der Zeile.

**Und er lässt sich wieder einklappen.** Über dem Rahmen steht „✕ Clip schliessen"
(`clipStop`); das entfernt das `<iframe>`, der Clip hält an, gibt den Platz frei, und der
Knopf kommt zurück. Ein zweiter Klick startet ihn von vorn.

Jede Seite mit einem Clip-Block **muss `mathlib.js` einbinden.** Themenseiten tun das
ohnehin.

---

## Schritt 4 — Verifikation

0. **Layout prüfen** — `node .claude/tools/pruef-clip.mjs clips/<name>.html 10 22 34 …`
   springt in die genannten Sekunden, meldet überlappende Zeilen und alles, was über die
   Bühne hinausragt, und legt je Zeitpunkt ein Bild ab. **Die Bilder trotzdem ansehen:**
   Der Prüfer sieht Überlappung, nicht Gestaltung. Ein Bruchstrich macht eine Zeile
   doppelt hoch — Zeilen mit `[a|b]` brauchen `abstand` ≥ 200.
1. **Pre-Flight** über die geänderten Lektionsseiten, wie immer vor dem Commit.
2. **Im Browser bei 1280 und 360 px**: Karte sichtbar, Klick lädt den Clip, Rahmen im
   richtigen Verhältnis, Bedienleiste ohne Überlauf. Auf schmalen Schirmen blendet der
   Clip die Tastaturhinweise aus — dort gibt es weder Leertaste noch Pfeiltasten.
3. **Netzwerk-Tab**: keine Anfrage an einen fremden Host. Der Clip zieht die Schriften
   per `@import url("../schriften.css")` aus dem Repo.
4. **Transkript vorhanden und lesbar.** Fehlt der Sprechertext, meldet das
   Einbau-Skript `[WARN]` und lässt den Block weg.

---

## Häufige Stolpersteine

**Der Clip liegt eine Ebene unter der Wurzel — und das ist nicht frei wählbar.** Er zieht
die Schriften per `@import url("../schriften.css")`. Verschiebt man `clips/` tiefer, sind
die Schriften weg, ohne dass etwas bricht: die Seite fällt still auf Georgia zurück.

**Das Transkript ist nicht Beiwerk.** Von einem animierten Clip sieht eine Suchmaschine
gar nichts, und die Volltextsuche der Site ebenso wenig. Der Transkriptblock trägt darum
die Klasse `clip-transkript`, und die darf **nicht** in `SKIP_CLASSES` von
`scripts/build-suchindex.py` landen — sonst ist der Clip inhaltlich unsichtbar.

**Nach jedem Drehbuch-Edit beide Skripte laufen lassen**, erst `build-clips.py`, dann
`build-clips-einbau.py`. Das zweite liest nur `clips.json` und baut selbst nichts; ohne
den ersten Lauf steht in der Seite die alte Dauer und der alte Kurzbeschrieb.

**`build-seo.py` danach**, damit `dateModified` und die Sitemap stimmen. Der Pre-Flight
warnt, wenn es fehlt.

**Brüche funktionieren nur in Formel-Elementen, nicht in Prosa.** `formel`, `karte` und
`box` schicken ihren ganzen Text durch `formel()` — dort wird `[a|b]` zum Bruch. Die
Prosa-Typen `text`, `notiz`, `titel`, `untertitel`, `aussage` und `liste` gehen dagegen
durch `text_html`, und das ersetzt `|` **zuerst** durch einen Zeilenumbruch, bevor es die
`@…@`-Abschnitte auswertet. Aus `@x = [b|a]@` wird darum kein Bruch, sondern eine
umgebrochene eckige Klammer — ohne Fehlermeldung, es sieht nur falsch aus. Wer in einer
Merkzeile einen Bruch braucht, macht daraus ein eigenes `formel`-Element.

**Ein `display` in der Regel schlägt das `hidden`-Attribut.** Sobald eine Klasse
`display: grid` oder `display: flex` setzt, hört `hidden` auf zu wirken — die Gruppen
standen alle offen, ohne dass etwas gemeldet wurde. Es braucht dann ausdrücklich
`.klasse[hidden] { display: none; }`. Betrifft in diesem Projekt `.cl-body` und
`.clip-start`.

**`liste` wird nicht zentriert.** Der Typ bekommt die Klassen `l sans`, aber kein `mitte`
— der Block läuft über die volle Bühnenbreite und beginnt am linken Rand, auch im Layout
`zentriert`. In einer sonst mittigen Szene wirkt das wie ein Versehen. Für aufgezählte
Merkpunkte in der Mitte drei `formel`-Zeilen nehmen; die tragen `row` und sitzen zentriert.

**`<` und `>` werden in Formel und Prosa genau umgekehrt geschrieben.** `formel()`
escapt nicht — ein nacktes `<` landet roh im HTML. In `formel`, `karte` und `box` gehört
darum `&lt;` und `&gt;` hin. Die Prosa-Typen escapen dagegen selbst, dort schreibt man das
Zeichen direkt; ein `&lt;` würde als sichtbarer Text „&lt;" erscheinen:

| | `formel` / `karte` / `box` | `text` / `notiz` / `titel` / `untertitel` / `aussage` / `liste` |
|---|---|---|
| kleiner als | `x &lt; 3` | `Aus @x < 3@ folgt …` |
| grösser als | `x &gt; 3` | `Aus @x > 3@ folgt …` |

Für `≤` und `≥` gibt es keine Falle: `<=` und `>=` werden in beiden Fällen ersetzt.

**Vor `inf` braucht es ein echtes Minuszeichen.** `-inf` ergibt `-∞` mit ASCII-Bindestrich
statt `−∞`. Grund: Die Wortersetzung `inf` → `∞` läuft **vor** den Minus-Regeln, und `∞`
ist kein Wortzeichen — danach greift keine der Regeln mehr, die aus `-` ein `−` machen. Im
Drehbuch also `]−inf; -3[` schreiben, mit `−` (U+2212) an der ersten Stelle und dem
normalen `-` an der zweiten, wo die Ersetzung greift. Ergibt `]−∞; −3[`, wie es
STYLEGUIDE §2.7 verlangt.

**Eine gehaltene Ankerzeile belegt die oberste Zeile — Folgeszenen müssen tiefer
beginnen.** Steht auf einem Element `halten`, bleibt es über die folgenden Szenen stehen.
Deren `oben` muss dann unter der Ankerzeile liegen, sonst rendern beide übereinander und
die Formeln stehen ineinander. Bewährt: die einführende Szene auf `oben: 178`, alle
Folgeszenen auf `oben: 348`. Beide bestehenden Clips machen es so.

---

## Die Bühne ist geteilt

`clipBuehne(quelle, titel)` in `mathlib.js` ist nicht nur für Lektionsseiten da — die
Leitprogramme unter `leitprogramme/` binden dieselbe Funktion ein. Wer an ihr etwas
ändert, ändert es dort mit.

Seit dem 01.09.2026 tut sie zwei Dinge mehr, die vorher nur die Kopie im Leitprogramm
konnte: Sie **sperrt das Scrollen**, solange sie offen ist (sonst wandert die Seite
darunter weg, und beim Schliessen ist man woanders), und sie **gibt den Fokus zurück**
an den Knopf, der sie geöffnet hat (sonst landet er am Seitenanfang).

## Bibliotheksseite `clips.html`

**Unterteilt nach Lektion und Reihe.** Innerhalb eines Lerngebiets bekommt jede Reihe
eine Zwischenüberschrift mit der Lektionsnummer davor — `2.2a · Ungleichungen`. Ein
Lerngebiet hat schnell zwanzig Clips; ohne die Überschriften ist das eine Liste, durch
die man liest, statt einer, in der man etwas findet.

Die Reihenfolge macht `ordnung()` in `scripts/build-clips-einbau.py`: erst der Zweig
(Arithmetik vor Algebra, `ZWEIGE`), dann die Lektionsnummer, dann die Reihe. Reihen,
deren Folge didaktisch und nicht alphabetisch ist, stehen in `REIHEN` — dort steht
etwa, dass in 2.2a die Ungleichungen vor die Parametergleichungen gehören.

**Die Bibliothek setzt mehrspaltig, die Lektionsseiten rastern.** `.cl-body` benutzt
`columns: 2`, `.clip-auswahl` ein Raster. Mit einem Raster ginge die Unterteilung nicht:
Eine Zwischenüberschrift müsste dort wissen, in welcher Spalte sie steht. Mehrspaltiger
Satz lässt die Gruppen der Reihe nach in die Spalten laufen, `break-inside: avoid` hält
jede zusammen.



Die Übersicht über alle Clips, gruppiert nach Fach und darin nach Lerngebiet. Sie ist
**nicht** von Hand gepflegt: `build-clips-einbau.py` füllt auch dort einen Block,

```html
<!-- CLIPS-BIBLIOTHEK:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS-BIBLIOTHEK:ENDE -->
```

und baut daraus eine **aufklappbare Übersicht, nach Fach und Lerngebiet** — dieselbe
Gliederung wie die Startseite. Die Gruppen kommen aus dem Block `GROUPS` in `nav.js`, nicht
aus dem Freitextfeld `lerngebiet` im Drehbuch: Sonst ergäbe ein Tippfehler dort eine neue
Gruppe. Lerngebiete ohne Clips werden weggelassen.

Die Lerngebiete stehen über die ganze Breite untereinander. **Zweispaltig ist erst die
Clipauswahl darin** — und zwar spaltenweise gefüllt: erst die linke Spalte von oben nach
unten, dann die rechte. Zeilenweise gefüllt würde eine nummerierte Reihe über beide
Spalten zickzacken (1 links, 2 rechts, 3 wieder links). Die Zeilenzahl setzt der Generator
je Gruppe als Inline-Stil, weil sie an der Anzahl Clips hängt; unter 720 px wird sie
zurückgenommen und alles steht untereinander.

Jede Gruppe ist beim Laden **zu** und nennt in der Kopfzeile Anzahl und Gesamtlaufzeit;
darin steht je Clip eine Zeile mit **nur Titel und Laufzeit**. Kurzbeschrieb, Verweise und
Transkript stehen bewusst nicht dort — sie gehören auf die Lektionsseite, wo der Clip im
Zusammenhang steht. Bei hundert Clips wären hundert Transkripte auf einer Seite das Ende
der Übersicht, und für die Suche zählen sie ohnehin schon dort.

Ein Clip mit mehreren `lektion`-Codes erscheint in jeder Gruppe, zu der er gehört — man
findet ihn dort, wo man sucht. Innerhalb einer Gruppe wird er nur einmal gezeigt, auch
wenn zwei seiner Lektionen darin liegen.

Ein neuer Clip erscheint automatisch, sobald sein Drehbuch gebaut ist.

Angebunden ist die Seite an drei Stellen — die sind schon gesetzt und müssen für neue
Clips nicht angefasst werden:

| Datei | was |
|---|---|
| `nav.js` | Eintrag `▶ Clips` im Menü *Nachschlagen*, in der Kopfzeile und im Mobilmenü |
| `scripts/build-seo.py` | Zeile in der `SEITEN`-Tabelle — Beschreibung, canonical, Sitemap |
| `scripts/build-suchindex.py` | `clips.html` in der Liste der Nachschlagewerke |

Die Clip-Dateien selbst stehen bewusst **nicht** in der Sitemap: ohne Seitengerüst,
Navigation und Fussbereich wären sie als Landeseite aus einer Suche eine Sackgasse.
Indexiert werden `clips.html` und die Lektionsseite — beide tragen das Transkript.

---

## Pre-Flight

Clips werden mitgeprüft, wenn man sie übergibt:

```sh
python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html clips/*.html clips.html
```

Auf den Clip-Bühnen laufen nur die allgemeinen Checks (Tag-Bilanz, doppelte IDs, kein ß,
Dezimalpunkt, keine Fremdhosts) — Skelett-, nav- und Ressourcen-Checks gelten für sie
nicht, sie haben kein Seitengerüst.

Dazu kommt eine Konsistenzprüfung der Ablage, die immer läuft:

- jeder `clips.json`-Eintrag hat eine Datei → sonst `[FEHLER]` (toter Knopf in der Bibliothek)
- jede Datei steht in `clips.json` → sonst `[FEHLER]` (fehlt lautlos in der Bibliothek)
- jedes `lektion`-Kürzel existiert in `nav.js` → sonst `[FEHLER]` (landet auf keiner Seite)
- Sprechertext vorhanden → sonst `[WARN]` (die Seite bekommt kein Transkript)

---

## Ton

Alle vier Clips haben eine gesprochene Tonspur, lokal erzeugt.

### Warum es überhaupt passt

Der Sprechertext steht schon je Szene im Drehbuch. Bisher wurde daraus die Szenendauer nur
**geschätzt** (`Wörter / sprechtempo`). `scripts/build-clip-ton.py` misst stattdessen die
echte Länge und schreibt sie als Feld `dauer` ins Drehbuch zurück — danach stimmt Bild zu
Sprache exakt statt ungefähr.

### Und darum gehört `nachlauf` ins Drehbuch

Die alte Schätzung veranschlagte rund 1.5 s mehr, als die Stimme wirklich braucht. Diese
Dehnung war ein Fehler — aber sie leistete unbeabsichtigt etwas: Sie liess die letzte Zeile
einer Szene länger stehen. Als die Messung den Fehler entfernte, fiel die Standzeit überall
auf den Standard `nachlauf = 2.6 s` zusammen, im Merkbild von 5.3 s herunter.

**Darum setzen alle Clips `nachlauf: 4.0`.** Damit steht jede letzte Zeile vier Sekunden,
und der Wert ist eine Entscheidung statt ein Nebenprodukt einer Schätzformel. Wer einen
neuen Clip anlegt, setzt ihn mit — sonst läuft dieser eine schneller als die anderen.
Kontrollieren lässt sich das mit `dauer − letzte Einblendung` je Szene; bei allen vier
Clips ergibt das durchgehend 4.0 s.

### Einrichten

```sh
pip install piper-tts soundfile
# Stimme laden: rhasspy/piper-voices → de/de_DE/thorsten/high (rund 109 MB)
export PIPER_MODELL=/pfad/de_DE-thorsten-high.onnx
```

Beides gehört **nicht ins Repo** — nur die fertige MP3 wird versioniert.

### Bauen

```sh
python3 scripts/build-clip-ton.py <clip>     # spricht, misst, schreibt dauer + ton/<clip>.mp3
python3 scripts/build-clips.py    <clip>     # baut den Clip mit den neuen Dauern
```

Die Reihenfolge ist zwingend: Das erste Skript ändert nur das Drehbuch und legt den Ton ab.

### Wie es im Clip läuft

- **Eine Spur je Clip**, nicht eine je Szene. Die Sprache sitzt an `Szenenstart + 0.4 s`,
  dazwischen ist Stille. Mit einer einzigen Spur gibt es nichts zu verketten und kein
  Stolpern an den Szenengrenzen. Rund die Hälfte der Spur ist Stille, das kostet fast nichts.
- **Der Ton versucht hörbar zu starten.** Der Clip wird durch einen Klick geöffnet,
  darum lässt der Browser das meist zu; das `<iframe>` bekommt dafür `allow="autoplay"`.
  Wehrt der Browser sich, fällt es lautlos auf stumm zurück und der Knopf „🔇 Ton an"
  macht daraus die nötige Geste. Nie stumm *und* ohne Knopf — sonst wäre der Ton
  unerreichbar.
- **Sobald der Ton läuft, führt er die Uhr** (`t = ton.currentTime`). Tondrift fällt auf,
  Bilddrift nicht. Läuft kein Ton, zählt wie bisher `requestAnimationFrame`.
- Pause, Spulen, Neustart nehmen den Ton mit. Gemessene Abweichung Ton/Bild: 0.01–0.06 s.
- Ohne Tonspur ändert sich am Clip **nichts** — der Ton ist eine Zutat, keine Voraussetzung.

### Stolperstein beim lokalen Prüfen

**`python3 -m http.server` beherrscht keine Range-Requests.** Ohne die kann der Browser in
einer MP3 nicht springen: Der Klick auf den Fortschrittsbalken wirft den Ton an den Anfang
zurück, und es sieht nach einem Fehler im Clip aus. GitHub Pages beherrscht sie. Zum
lokalen Testen einen Server mit Range nehmen, sonst jagt man ein Phantom.

### Grösse und Qualität

Sprache als MP3 mono bei rund 50 kbit/s kostet etwa 3.3 kB je Sekunde — die vier Clips
zusammen **912 kB**. `--qualitaet` steuert das
(0.0 gross bis 1.0 klein). Die Spur bekommt Kopfraum auf 0.95, sonst übersteuert der
Encoder — Piper steuert einzelne Sätze bis an die Grenze aus.

Opus wäre kleiner, scheidet aber vorerst aus: libsndfile schreibt Opus nur bei 8/12/16/24/48 kHz,
Piper liefert 22.05 kHz. Ohne Resampling bleibt MP3 — das dafür überall abspielbar ist.

### Zweite Stimme

Ein Clip kann mehrere Tonspuren tragen; in der Bedienleiste erscheint dann ein Knopf
`🗣 <Name>`, der umschaltet. Die Spuren liegen als `ton/<name>-<stimme>.mp3` neben der
ersten, und der Generator findet sie von selbst — im Drehbuch ist nichts einzutragen.

```sh
export PIPER_MODELL=/pfad/de_DE-thorsten-high.onnx      # die erste, als Referenz
export PIPER_MODELL2=/pfad/eigene-stimme.onnx
python3 scripts/build-clip-ton.py <clip> --zweitstimme kohler
python3 scripts/build-clips.py    <clip>
```

**Die zweite Spur richtet sich nach der ersten, nicht umgekehrt.** Das Drehbuch und die
Animation stehen schon; also wird jeder Satz auf die Länge gebracht, die der Satz der
ersten Stimme hat, und die Lautheit auf deren Effektivwert gezogen. `--zweitstimme`
fasst das Drehbuch darum **nicht** an. Das Umschalten ändert nur den Klang — Zeit und
Zustand laufen weiter.

**Zwei Durchgänge je Satz, nicht einer.** `--length-scale` streckt die Phoneme, nicht die
feste Satzpause davor und dahinter; der erste Schuss liegt um fünf bis zehn Prozent
daneben. Der zweite rechnet den Rest heraus, danach liegt die Abweichung unter 0.2 s.

**Lautheit heisst Effektivwert, nicht Spitze.** Zwei Stimmen, beide auf 0.95 begrenzt,
klingen verschieden laut. Angeglichen wird der RMS der Sprachanteile (alles über 0.01),
danach greift der Kopfraum.

### Welche Stimme beim Öffnen läuft

`STANDARDSTIMME` in `scripts/build-clips.py` nennt den Namenszusatz, der beim Öffnen
laufen soll — aktuell `"kohler"`. Gibt es zu einem Clip die Spur
`ton/<clip>-kohler.mp3`, startet der Clip mit ihr; sonst mit der ersten. Ein leerer
String heisst: immer die erste. Eine Zeile, keine Änderung an den Drehbüchern.

Die Dehnung der Standardstimme gilt dabei von Anfang an — sonst liefe die Animation die
ersten Sekunden im falschen Tempo.

### Die eingestellte Zweitstimme

Für `de_CH-kohler-medium` sind die Werte in drei Hörtests festgelegt worden
(31.08./01.09.2026, `stimmtest.py`, `stimmklang.py`, `stimmtempo.py` im Home):

```sh
python3 scripts/build-clip-ton.py <clip> --zweitstimme kohler \
        --noise-scale 0.30 --noise-w 0.25 --tempo 0.80 --klang
```

| Regler | Wert | warum |
|---|---|---|
| `--noise-w` | 0.25 | Streuung der Phonemlängen — **der Regler gegen das Zittern** |
| `--noise-scale` | 0.30 | Streuung im Klang; zusammen mit dem obigen die Fassung «E» aus dem ersten Hörtest |
| `--klang` | an | gleicht das mittlere Spektrum an die erste Stimme an: **+6 dB** unter 300 Hz, **−6 dB** um 3 kHz, **−9 dB** bei 6–8 kHz. Die Stimme hatte zu wenig Körper und zu viel Zischeln |
| `--tempo` | 0.80 | das Sprechtempo, das im dritten Hörtest getragen hat. Voll angeglichen (0.62) klang es gehetzt |

**`--klang` misst, statt zu raten.** Die Kurve entsteht aus den mittleren Spektren
beider Stimmen über *alle* Sätze des Clips, in Terzen geglättet, auf ±9 dB begrenzt,
unter 80 Hz unangetastet. Sie steht nirgends als Zahlenreihe — sie wird bei jedem Bau
neu gerechnet und passt sich damit auch einer neu trainierten Stimme an.

### Wenn die Stimme dafür zu schnell wird

`de_CH-kohler-medium` spricht von Haus aus rund die Hälfte langsamer als Thorsten. Um
in dessen Zeitspur zu passen, bräuchte sie Tempo 0.58 bis 0.62 — 1.6-fach beschleunigt.
Das trägt nicht.

Darum gibt es `--tempo`: Die Stimme spricht in ihrem eigenen Tempo, und **die Animation
läuft entsprechend langsamer**, während diese Spur spielt.

```sh
python3 scripts/build-clip-ton.py <clip> --zweitstimme kohler-normal --tempo 1.0
python3 scripts/build-clip-ton.py <clip> --zweitstimme kohler-mittel --tempo 0.80
python3 scripts/build-clip-ton.py <clip> --zweitstimme kohler-schnell
```

Das Skript misst dabei, um wie viel länger die Spur wird, und legt den Faktor als
`ton/<name>-<stimme>.json` daneben. **Gemessen wird an den Szenendauern, nicht an den
Sätzen der ersten Stimme:** Ein Satz hat das k-Fache seiner Szene Zeit, nicht das
k-Fache des Referenzsatzes. Am Satzverhältnis gemessen fiele der Faktor unnötig gross
aus, weil die Referenzstimme von Lauf zu Lauf schwankt — im Testclip 1.40 statt 1.24. Der Generator schreibt ihn in die Stimmenliste, und
der Player rechnet `Szenenzeit = Tonzeit ÷ Dehnung`. Die Einsätze werden mit demselben
Faktor gedehnt platziert — deshalb stimmt es nicht nur am Anfang, sondern überall.

**Nachgemessen** am Testclip (Sprachanfänge, zurückgerechnet auf die Szenenzeit):

| Szene | soll | Thorsten | Normal ÷1.55 | Mittel ÷1.37 | Schnell |
|---|---|---|---|---|---|
| 1 | 0.40 | 0.64 | 0.53 | 0.54 | 0.56 |
| 2 | 9.90 | 9.96 | 9.95 | 10.03 | 10.04 |
| 3 | 17.70 | 17.76 | 17.75 | 17.74 | 17.72 |
| 4 | 26.95 | 27.02 | 27.02 | 27.07 | 27.10 |
| 5 | 39.97 | 39.98 | 40.09 | 40.09 | 40.08 |

Alle vier Spuren liegen innerhalb von 0.15 s auf derselben Zeitspur. Der Knopf zeigt die
Dehnung mit an: `🗣 Kohler Normal (1.55×)`.

Die Spuren stehen in der Leiste von der langsamsten zur schnellsten — beim Durchklicken
hört man eine Reihe und nicht eine Namensliste.

Der dritte Weg bleibt: den Sprechertext kürzen. Dann passt er beiden Stimmen bequem, und
es braucht gar keine Dehnung.

**Das Stimmmodell gehört nicht ins Repo.** Auf der Modellkarte von
`de_CH-kohler-medium` steht: «Nicht weitergeben: wer diese Datei hat, spricht mit dieser
Stimme.» Versioniert wird nur die fertige MP3.

### Lizenzlage (geprüft am 30.08.2026)

| | |
|---|---|
| Piper, aktuell (`OHF-Voice/piper1-gpl`) | **GPL-3.0** |
| Piper, alt (`rhasspy/piper`) | MIT, am 06.10.2025 archiviert |
| Stimme `de_DE-thorsten` (Datensatz Thorsten-Voice) | **CC0-1.0** |

Die GPL regelt die Weitergabe des **Programms**, nicht das, was es erzeugt — und Piper
kommt ohnehin nicht ins Repo. Die Stimme steht unter CC0: keine Einschränkung auf
nicht-kommerzielle Nutzung, keine Namensnennung nötig. Der Autor Thorsten Müller freut
sich über eine Nennung.

**Nicht geprüft:** Die deutsche Thorsten-Stimme wurde nicht von Grund auf trainiert,
sondern aus der englischen Lessac-Stimme feinabgestimmt. Ob deren Herkunftsdaten
Bedingungen mitbringen, die ins abgeleitete Modell hineinreichen, ist offen. Ebenso
ungeprüft: die Lizenzen der übrigen sieben deutschen Stimmen.

---

## Die Umstellung auf LaTeX (31.08.2026)

Alle 28 Drehbücher wurden umgestellt — 371 Formelzeilen. `scripts/clip-nach-latex.py`
hat das gemacht und bleibt im Repo: als Beleg, was mit den Zeilen geschehen ist, und
falls irgendwo noch ein Drehbuch in der alten Schreibweise auftaucht.

`"latex": false` schaltet ein einzelnes Drehbuch auf die alte Schreibweise zurück;
`formel()` in `scripts/build-clips.py` ist unangetastet.

### Was die Umstellung gekostet hat

| | |
|---|---|
| Drehbücher | 28 |
| übersetzte Zeilen | 371 |
| davon rein mechanisch | 279 |
| davon mit Prosa dazwischen | 102 — hier musste die Grenze Mathematik/Text gezogen werden |
| Ton | **unverändert.** Es wurde kein Wort neu gesprochen: der Umbau betraf die Formeln, nicht den Sprechertext, und damit auch keine Dauer |
| Lektionsseiten, `clips.json`, Suchindex | **unverändert** — Titel und Längen sind dieselben |
| Layout | eine einzige Kollision (`g1-2-zahlformen`, 5 px), behoben mit 40 px mehr `abstand` |

### Fehler, die der Umbau selbst produziert hat

Alle vier fielen erst in der Prüfung auf, keiner im Augenschein:

1. **`A \ B` verlor das Zeichen.** Der Backslash der Mengendifferenz wurde in LaTeX zu
   einem Abstandsbefehl — die Differenz sah aus wie ein Produkt. 6 Zeilen.
2. **`\%` wurde zur Mengendifferenz.** Dieselbe Regel, eine Rekursion zu spät angewandt:
   sie traf den Backslash eines schon gesetzten `\%`.
3. **`x_{1,2}` und `\tan^{-1}`** bekamen Mengenklammern: die geschweiften Klammern einer
   Hoch- oder Tiefstellung wurden escaped wie die einer Menge.
4. **`√(1+8)`** verlor die Wurzel: der Radikand steht in der alten Schreibweise *neben*
   dem Zeichen, in LaTeX gehört er *hinein*.

### Wie geprüft wurde

Nicht durch Ansehen — 28 Clips mit rund 150 Szenen sah damals niemand vollständig durch, und heute sind es 50.

**Textvergleich.** `.claude/tools/clip-text.mjs` liest den sichtbaren Text jeder Zeile.
Einmal vor dem Umbau, einmal danach, dann Zeile gegen Zeile. Von 719 Zeilen blieben 31
Abweichungen übrig, alle derselben Art: MathJax zählt bei ä, ö, ü, ✓, ✗, ‰ und µ eine
Ersatzglyphe doppelt in die Textauslese — **im Bild steht sie nicht**, an drei Stellen
mit Screenshots bestätigt.

**Layoutvergleich.** `.claude/tools/pruef-clip.mjs` zum Ende jeder Szene über alle 28
Clips: Überlappungen und Überlauf. LaTeX setzt Brüche etwas höher als der alte Satz —
darum war das der eigentliche Risikopunkt, und es blieb bei der einen Kollision.

### Was bleibt

**Zwei Serifenschriften in einem Bild.** Die Prosa steht in der Schrift des Clips, die
Formeln in der TeX-Schrift. Am deutlichsten in den roten Handnotizen, wenn dort ein
Formelstück steht. Ändern lässt sich das nicht: MathJax bringt eigene Glyphen mit.

**2 MB `tex-svg.js`.** Wer den Clip von einer Lektionsseite aus öffnet, hat die Datei im
Cache. Wer ihn direkt aufruft, lädt sie — gemessen 2190 statt 531 kB, 191 statt 119 ms.

---

## Noch offen

Die Mechanik steht. Was noch fehlt, ist Inhalt und der Übertrag:

- **Mehr Clips.** Es sind 50 (52:54 min), alle im Grundlagenfach; das Schwerpunktfach hat
  bis auf den geteilten Bruchgleichungs-Clip noch keine eigenen. Am dichtesten sind
  Lerngebiet 1 und 2, in 3, 4 und 5 steht je einer. Als Referenz für ein Drehbuch:
  `g2-2b-mitternachtsformel-herleitung` für eine Herleitung Schritt für Schritt,
  `g2-2a-warum-a-ungleich-5` für eine Rechnung mit Bedingung, `g2-3-anzahl-loesungen`
  für eine Fallunterscheidung mit Bild.
- **Urteil über die Stimme.** Alle Clips sind synthetisch vertont. Ob die Stimme im
  Unterricht trägt, ist noch nicht entschieden; falls nicht, ist der Wechsel auf eine
  eigene Aufnahme nur ein Dateiaustausch — das Verfahren bleibt dasselbe.
- **Untertitel.** Text und Zeitmarken liegen vor; eine WebVTT-Spur wäre fast geschenkt und
  funktioniert im Schulzimmer besser als Ton: lautlos abspielbar, an der Wand mitlesbar.
- **Übertrag nach TALS Physik** — vermerkt in `TODO-schwesterprojekt.md`.
