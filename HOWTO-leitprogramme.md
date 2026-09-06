# HOWTO — ein Leitprogramm ins Repo holen

Ein Leitprogramm ist eine eigenständige Seite unter `leitprogramme/`: ein Thema zum
selbstständigen Durcharbeiten, mit Vorwissenstest, Kapiteln und Gesamttest. Es ist
**keine Themenseite** — es bringt sein eigenes Layout mit (Ablaufspalte,
Fortschrittszähler, Testköpfe) und darum auch seinen eigenen `<style>`.

Diese Datei ist die Anleitung für den häufigen Fall: Das Leitprogramm entsteht
**ausserhalb** des Repos, als einzelne HTML-Datei, und wird danach hereingeholt.
Sie ist aus dem ersten Übertrag entstanden (`leitprogramm-potenzen_4.html` →
`leitprogramme/potenzen.html`, 31.08./01.09.2026) und listet, was dabei nötig war —
jeder Punkt stand für ein Problem, das erst im Browser sichtbar wurde.

## Zwei Arten von Leitprogramm

| | gegliedert nach | Beispiel | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vorwissenstest, Kapitel, Gesamttest | `potenzen.html` | diese Datei |
| **Übungsprüfung** | dem Prüfungsbogen: je Teilaufgabe ein Clip, Musterlösung, Punktezeile | `uebungspruefung-1.html` | **`HOWTO-uebungspruefung.md`** |

Layout, Kopf, Fuss, Farbtokens und Clip-Bühne sind bei beiden dieselben — der
`<style>`-Block der zweiten Art ist aus `potenzen.html` übernommen. Die Übertragsliste
unten gilt darum für beide. Was nur die Prüfungsart betrifft (PDF auslesen, `"probe"`
an den Clips, Punktezeile, unverlinkt veröffentlichen), steht in der eigenen Datei.

---

## Die Übertragsliste

Der Reihe nach abarbeiten. Nach jedem Punkt steht, woran man merkt, dass er fehlt.

### 1. Datei nach `leitprogramme/<name>.html`

Genau **eine Ebene** unter der Wurzel, wie `clips/`. Alle relativen Pfade unten setzen
das voraus.

### 2. Fremde Hosts entfernen

Extern gebaute Dateien ziehen Schriften und MathJax typischerweise von Google und einem
CDN. Im Repo gilt: **keine Seite lädt etwas von einem fremden Host** (STYLEGUIDE §5.3.1).

```html
<link rel="stylesheet" href="../schriften.css">
<script src="../vendor/mathjax/tex-svg.js"></script>
```

Die `<link>`-Zeilen auf `fonts.googleapis.com`, `fonts.gstatic.com` und den
`preconnect` ersatzlos streichen. **Merkt man daran:** Der Pre-Flight meldet die Hosts,
und ohne Netz fällt die Seite auf Georgia zurück.

### 3. Dokumentrahmen und Zeichensatz

Von Hand gebaute Dateien beginnen gern direkt mit `<title>`. Ohne `<meta charset>` rät
der Browser die Kodierung, und über HTTP rät er falsch:

```
natÃ¼rlichen · fÃ¼nf · â€"
```

Darum immer:

```html
<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
…
</head>
<body>
```

**Merkt man daran:** Umlaute zerfallen — aber erst im Browser, nicht im Editor, und
nicht in irgendeiner Prüfung. Ohne Viewport ist zusätzlich die Mobilansicht kaputt.

### 4. Anker an die Kapitel

Die Volltextsuche schneidet ihre Abschnitte an `h2[id]`. Ohne `id` ist die ganze Seite
**ein** Treffer. Anker in derselben Schreibweise wie sonst im Repo: klein, ohne Umlaute,
Bindestriche statt Leerzeichen.

**Achtung auf Kollisionen:** Trägt die umgebende `<section>` schon die `id`, die auch das
Sprungziel der Ablaufspalte ist, darf die Überschrift sie nicht ein zweites Mal
bekommen. Der Pre-Flight meldet doppelte IDs — im Potenzen-Leitprogramm traf es
`gesamttest`; die Überschrift heisst dort jetzt `gesamttest-titel`.

### 5. Relative Basis für eingebettete Clips

Steht im Skript eine absolute Adresse

```js
var BASIS = 'https://mathe.begreifbar.ch/';
```

dann kommen die eingebetteten Clips vom **Live-Stand**, nicht aus dem
Arbeitsverzeichnis. Eine lokale Vorschau zeigt dann den alten Clip, und ohne Netz gar
keinen. Ersetzen durch `'../'`.

### 6. Kopf, Fuss und Bühne von der Site erben

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">   <!-- VOR dem eigenen <style> -->
…
<style> … eigenes Layout … </style>
```

**Die Reihenfolge ist der ganze Trick:** Der eigene `<style>` steht danach und gewinnt
bei gleichem Gewicht — das Layout des Leitprogramms bleibt unverändert. Nachgemessen,
warum das gefahrlos ist: `style.css` hat auf oberster Ebene nur drei `body`-, eine
`table`-, eine `code`- und eine `a`-Regel, alles andere ist klassengebunden.

Dazu im Körper:

```html
<body>
<div id="nav-root"></div>
…
<footer class="site-footer"> … nach STYLEGUIDE §7 … </footer>
<script src="../mathlib.js"></script>
<script src="../nav.js"></script>
<script>buildNav({ id: 'leitprogramme' });</script>
</body>
```

`mathlib.js` bringt die Clip-Bühne mit (`clipBuehne(quelle, titel)`). Eine mitgelieferte
Kopie davon **löschen** — die Bühne ist überall dieselbe. Die *Karten*stile dürfen
bleiben, die sehen im Leitprogramm anders aus als auf einer Themenseite.

**Merkt man daran:** Ohne Kopf und Fuss ist die Seite eine Sackgasse — man kommt nur mit
dem Zurück-Knopf heraus.

### 7. Farbtokens erben, nicht kopieren

Extern gebaute Dateien tragen die Palette als eigenen `:root`-Block. Wenn sie mit
`style.css` übereinstimmt: **löschen**. Was übrig bleibt, ist die Übersetzung
abweichender Namen:

```css
:root{ --karte: var(--weiss); }
```

Beim Potenzen-Leitprogramm waren 20 von 26 Tokens Wert für Wert identisch und fünf
weitere kosmetisch verschieden (`.08` gegen `0.08`, längere Fallback-Ketten). Nach dem
Löschen: 4 von 2 816 000 Pixel anders, reine Kantenglättung.

### 8. Dunkelmodus, falls die Datei einen hat

`style.css` kennt **keinen** — die Site hat keinen. Ein Leitprogramm darf einen haben
(man liest es am Stück), muss dann aber die geerbten Bausteine mitfärben. Der Weg dazu
ist **ein Token, nicht eine Liste von Klassen**:

```css
:root[data-theme="dark"]{ … --karte:#211e19; --weiss:#211e19; … }
```

`style.css` färbt seine Flächen 20× mit `--weiss`. Ist das Token dunkel, färben sich
Kopfleiste, Menü, Suchfeld und Über-Panel von selbst.

**Eine Ausnahme bleibt:** `.site-footer` benutzt `--tinte` als *Fläche*. Im Dunkelmodus
kippt `--tinte` mit dem Text nach hell — der Fuss würde weiss. Drei Zeilen dafür:

```css
:root[data-theme="dark"] .site-footer{
  background:var(--papier-2); color:var(--tinte-2); border-top:1px solid var(--linie);
}
:root[data-theme="dark"] .site-footer a{ color:var(--blau); }
```

### 9. Eintragen

| Datei | was |
|---|---|
| `leitprogramme.html` | Karte im Block zwischen den `LEITPROGRAMME`-Markern |
| `scripts/build-seo.py` | Zeile in `SEITEN` — sonst fehlen Beschreibung und Sitemap |
| `scripts/build-suchindex.py` | Zeile in der Liste der Nachschlagewerke |
| `nav.js` | nur beim **ersten** Leitprogramm nötig, der Menüeintrag steht schon |

Danach `python3 scripts/build-seo.py --schreiben` und
`python3 scripts/build-suchindex.py`.

#### Oder bewusst *nicht* eintragen — unverlinkt veröffentlichen

Manches soll ausgeliefert, aber nicht gefunden werden: eine Übungsprüfung, die eine
Klasse per Link bekommt. Dann **alle drei Stellen zusammen**, sonst wirkt es nicht:

| Datei | |
|---|---|
| `leitprogramme.html` | **keine** Karte |
| `scripts/build-suchindex.py` | **kein** Eintrag — sonst steht die Seite in der Volltextsuche |
| `scripts/build-seo.py` | Eintrag **mit `noindex=True`** — nicht weglassen, sonst fehlen Beschreibung und canonical |

`noindex=True` nimmt die Seite aus `sitemap.xml` **und** lässt `block()` ein
`<meta name="robots" content="noindex, nofollow">` in den generierten Kopfblock setzen.
Beides zusammen ist nötig: Die Sitemap allein hält keine Suchmaschine ab, die die URL
anderswoher kennt — aus einem geteilten Link, einem Referrer, einer Browserleiste. Das
`nofollow` hält von der Seite aus auch die eingebetteten Clipdateien aus dem Index.

**Kein `Disallow` in `robots.txt`.** Die Datei ist öffentlich lesbar; ein Eintrag dort
würde die URL gerade bekanntmachen, statt sie zu verbergen.

**Und die Grenze aussprechen:** Das ist Unauffindbarkeit, keine Zugangskontrolle. Wer den
Link hat, kommt hinein, und wer ihn weitergibt, gibt den Zugang weiter. Für echten Schutz
bräuchte es etwas anderes als GitHub Pages.

Prüfen lässt es sich in drei Griffen:

```sh
grep -c "<dateiname>" sitemap.xml suchindex.js leitprogramme.html   # dreimal 0
grep 'name="robots"' leitprogramme/<name>.html                      # noindex, nofollow
```

---

## Prüfen

```bash
python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html leitprogramme.html
python3 -m http.server 8899 &
node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/<name>.html
```

Der Pre-Flight behandelt `leitprogramme/` wie `clips/`: eigenes Skelett, eigener
`<style>`, kein `page-wrap`, keine `nav.js`-Pflicht. Ohne diese Ausnahme meldet er
Phantom-Klassen, die in Wahrheit im Kopf der Datei stehen.

**Was keine Prüfung sieht** — dafür in den Browser schauen, hell und dunkel, 1280 px und
360 px:

- zerfallene Umlaute (Punkt 3)
- eine weisse Kopfleiste über dunkler Seite (Punkt 8)
- ein Clip, der vom Live-Stand kommt statt aus `clips/` (Punkt 5)

Beim ersten Übertrag ist jeder dieser drei erst im Bild aufgefallen.

---

## Nicht tun

- **Das Leitprogramm nicht in `page-wrap` + `main.content` pressen.** Es ist ein anderes
  Format als eine Themenseite; das hiesse, sein Layout neu zu bauen.
- **Die Bühne nicht doppelt halten.** Sie steht in `mathlib.js` und `style.css`.
- **Die Palette nicht kopieren.** Sie stimmt heute und läuft morgen auseinander.
