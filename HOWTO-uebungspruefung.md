# HOWTO — eine Übungsprüfung Teilaufgabe für Teilaufgabe erklären

Aus einem Prüfungs-PDF wird eine Seite unter `leitprogramme/`, auf der **jede
Teilaufgabe** ihren eigenen vertonten Clip hat. Es ist ein Sonderfall des
Leitprogramms: gleiches Layout, gleicher Kopf, gleicher Fuss — aber die Gliederung
kommt nicht aus dem Stoff, sondern aus dem Prüfungsbogen.

Diese Datei ist aus dem ersten Durchgang entstanden (`uebungspruefung-1`, 06.09.2026:
26 Teilaufgaben, 26 Clips, 20:28 min). Jeder Punkt unten stand für ein Problem, das
tatsächlich aufgetreten ist.

Verwandte Dokumente: `HOWTO-leitprogramme.md` (das allgemeine Format),
`HOWTO-clips.md` (Drehbücher und Ton), `STYLEGUIDE.md` §6.4/§6.5, `CLAUDE.md`
(Pre-Flight und Commit-Regel).

---

## Was am Schluss dasteht

```
leitprogramme/uebungspruefung-<n>.html     die Seite
clips/pruefung<n>-<aufgabe>-<fokus>.json   je Teilaufgabe ein Drehbuch
clips/pruefung<n>-<aufgabe>-<fokus>.html   generiert
clips/ton/pruefung<n>-….mp3                generiert
clips/sprechertext-pruefung<n>-….txt       generiert
```

Aufbau der Seite, von oben nach unten:

1. **Anleitung** — wie man damit arbeitet. Der erste Punkt lautet immer: *zuerst
   schreiben, dann lesen.*
2. **Der Prüfungsbogen am Stück** — alle Teilaufgaben, ohne Lösungen, ohne Clips.
   Damit lässt sich die Prüfung unter Bedingungen schreiben, bevor irgendetwas
   verraten ist.
3. **Ein Abschnitt je Aufgabe** (A1, A2, … C7) mit den Teilaufgaben darin: Frage →
   Clip → Musterlösung → Punktezeile. Dazu Kästen mit typischen Fehlern.
4. **Auswertung** — Punkte je Teil, Selbsteinschätzung, die teuersten Fehler.

**Warum der Bogen doppelt dasteht.** Die Aufgabentexte stehen zweimal auf der Seite:
oben im Bogen und unten bei der Erklärung. Das ist Absicht und kein Versehen — wer beim
Erklärungsteil nachschlagen muss, was gefragt war, verliert den Faden, und wer den Bogen
schreiben will, darf die Lösung nicht im Augenwinkel haben.

---

## Schritt 0 — Das PDF lesen, und zwar misstrauisch

**Die Textextraktion verliert Hoch- und Überstriche.** Das ist der teuerste Fehler in
diesem ganzen Ablauf, weil er nicht auffällt: Es kommt ein plausibler Text heraus, nur
eben ein anderer als der gedruckte.

Im ersten Durchgang traf es zwei von 26 Teilaufgaben:

| im Extrakt | gedruckt | woran es auffiel |
|---|---|---|
| `0.6` | \(0.\overline{6}\) | Musterlösung sagt `= 2/3`, aber \(0.6 = \tfrac{3}{5}\) |
| `32 ·` | \(3^2 \cdot\) | Musterlösung rechnet `32 · 1/9 = 1`, was nur für \(3^2\) stimmt |

Beide Male war es die **Musterlösung**, die den Widerspruch aufdeckte. Darum:

> **Immer beide PDF lesen — Aufgaben *und* Lösungen — und jede Lösung nachrechnen.
> Wo Rechnung und Musterlösung auseinandergehen, ist meist die Extraktion schuld,
> nicht die Musterlösung.**

### Einen Überstrich am PDF selbst nachweisen

Raten reicht nicht. `\overline` ist in LaTeX kein Zeichen, sondern ein *gezeichneter
Strich* — im Textextrakt taucht er nie auf, im Inhaltsstrom dagegen als waagrechte
Linie. So findet man sie:

```python
from pypdf import PdfReader
import re
data = PdfReader(PDF).pages[0].get_contents().get_data().decode("latin-1")
for ox, oy, w, x1, y1, x2, y2 in re.findall(
        r"q\n1 0 0 1 ([\d.\-]+) ([\d.\-]+) cm\n\[\]0 d 0 J "
        r"([\d.\-]+) w ([\d.\-]+) ([\d.\-]+) m ([\d.\-]+) ([\d.\-]+) l S\n", data):
    ox, oy, x1, y1, x2, y2 = map(float, (ox, oy, x1, y1, x2, y2))
    if abs(y1 - y2) < 0.2:                       # waagrecht
        print(f"x {ox+x1:7.1f} → {ox+x2:7.1f}   y {oy+y1:7.1f}")
```

Die Glyphenpositionen holt man daneben mit dem `visitor_text`-Rückruf von
`extract_text`. Ein Strich, der **genau über einer Ziffer** liegt und **so breit wie
diese** ist, ist ein Überstrich; die Wurzelbalken derselben Zeile liegen auf ähnlicher
Höhe und sind länger.

Im ersten Durchgang: Strich bei `x 387.8 → 393.3, y 497.9`, Breite 5.5 pt, und die `6`
sass bei `x 387.8, y 489.3`. Eindeutig.

**Hochstellungen** verraten sich anders — im `visitor_text`-Rückruf haben sie eine
**kleinere Schriftgrösse** als die Grundzeile (im ersten Durchgang 6.0 gegen 10.9).

---

## Schritt 1 — Jede Lösung nachrechnen, keine ausgenommen

Bevor eine Zeile Drehbuch entsteht. Ohne `sympy` (steht hier nicht zur Verfügung) reicht
`fractions.Fraction` für alles Rationale und eine Stichprobe über einen Zahlenbereich für
alles Symbolische:

```python
from fractions import Fraction as F
# Identitaet: ueber einen Bereich pruefen, nicht an einer Stelle
assert all(3*x**4-48 == 3*(x-2)*(x+2)*(x*x+4) for x in range(-9, 10))
# Loesungsmenge: die Gleichung selbst pruefen, nicht die Umformung nachvollziehen
assert all((6*(x-2)-2*(2*x+1) == 3*(2*x-4)-2*(x+1)) == (x == 0) for x in range(-9, 10))
```

Bei Parameteraufgaben **jeden Fall einzeln** einsetzen, auch die Sonderfälle. Im ersten
Durchgang fiel dabei ein Vorzeichenfehler auf — in meiner Prüfzeile, nicht in der
Musterlösung. Genau dafür ist die Probe da.

---

## Schritt 2 — Die Drehbücher

Alles Übrige steht in `HOWTO-clips.md`; hier nur, was für Prüfungsclips gilt.

### Benennung

```
pruefung<n>-<teilaufgabe>-<fokus>
pruefung1-a3a-vorzeichen-und-potenzen
pruefung1-c7-parameter-drei-faelle
```

Die Teilaufgabe steht im Namen, sonst findet man unter 26 Dateien nichts wieder. Der
Fokus dahinter sagt, was der Clip zeigt — nicht «Loesung» oder «Teil 3».

### `"probe": true` — der Clip gehört zur Seite, nicht in die Bibliothek

**Jedes Prüfungs-Drehbuch bekommt `"probe": true`.** Das Feld war ursprünglich für
Versuchsclips gedacht und leistet hier genau das Richtige: Der Clip wird gebaut und
ausgeliefert, aber

- er kommt **nicht** in `clips/clips.json`,
- er erscheint **nicht** in der Bibliothek `clips.html`,
- er wird **nicht** auf eine Lektionsseite eingebaut,
- der Pre-Flight nimmt ihn von der Ablage-Konsistenzprüfung aus.

Das ist gewollt: 26 Prüfungsclips würden die Bibliothek fluten und auf acht
Lektionsseiten Blöcke erzeugen, die dort niemand bestellt hat. Nachgemessen im ersten
Durchgang: `clips.json` blieb Zeichen für Zeichen unverändert bei 62 Einträgen.

Weil das Feld hier etwas anderes bedeutet als «Versuch», gehört eine Zeile dazu:

```json
"probe": true,
"_probe": "Prueferklaerung — gehoert zum Leitprogramm uebungspruefung-1, nicht in die Clip-Bibliothek."
```

`lektion`, `reihe` und `folge` trotzdem sinnvoll ausfüllen. Sie werden heute nicht
ausgewertet, aber wer den Clip später doch in die Bibliothek heben will, soll nur ein
Feld löschen müssen.

### Szenenschema

Fünf Szenen tragen eine Teilaufgabe, sechs bis acht eine mehrteilige:

| Szene | Inhalt |
|---|---|
| 1 | **Aufgabe** — Nummer als `titel`, der Term als `formel`, die Leitfrage als rote `notiz` |
| 2…n−1 | **je ein Rechenschritt**, mit dem *Warum* als `notiz` daneben |
| n | **Merkbild** — der übertragbare Satz, nicht die Wiederholung des Resultats |

Das Resultat gehört in eine grüne `box`. Die Farbführung (`\fa{}`…`\fd{}`) zeigt, **was
von wo nach wo wandert** — etwa der Faktor, der sich wegkürzt. Sparsam bleiben: zwei
Farben je Clip reichen fast immer.

**`\lt` und `\gt`, nie `&lt;`/`&gt;`.** In Prüfungsclips stehen ständig Ungleichungen.
Warum die Entität hier bricht, steht in `HOWTO-clips.md` unter «Häufige Stolpersteine».

### Sprechertext

- **Zahlen als Wörter.** «zwei Drittel», nicht «2/3»; «minus zwölf», nicht «−12». Piper
  liest Ziffern unzuverlässig vor.
- Ein bis drei Sätze je Szene. Die Szenenlänge richtet sich später nach der gemessenen
  Sprechdauer, aber die Einblendungen kommen im Takt von 1.7 s — viel mehr Text als
  Zeilen führt dazu, dass die Stimme dem Bild davonläuft.
- **`"nachlauf": 4.0`** setzen, wie bei allen Clips.

---

## Schritt 3 — Bauen und vertonen

Die Reihenfolge ist zwingend: Ton misst die Dauern, Bau setzt sie ins HTML.

```sh
export PATH="$HOME/.local/bin:$PATH" \
       PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx

for f in clips/pruefung1-*.json; do n=$(basename $f .json)
  python3 scripts/build-clip-ton.py $n; done
for f in clips/pruefung1-*.json; do n=$(basename $f .json)
  python3 scripts/build-clips.py    $n; done
```

Rund 16 s je Clip; 26 Clips brauchen etwa sieben Minuten. Im Hintergrund laufen lassen
und derweil die Seite schreiben.

**Erst danach stimmen die Laufzeiten.** Vorher schätzt der Generator aus der Wortzahl und
liegt deutlich daneben — im ersten Durchgang 90 s geschätzt gegen 50 s gemessen.

---

## Schritt 4 — Layout aller Clips prüfen

Nicht am geschätzten Raster, sondern an den **echten Szenenenden**:

```python
import json, glob, os
for f in sorted(glob.glob('clips/pruefung1-*.json')):
    d = json.load(open(f)); t = 0.0; m = []
    for sz in d['szenen']:
        t += sz['dauer']; m.append(round(t - 1.0, 1))
    print(os.path.basename(f)[:-5], ' '.join(map(str, m)))
```

Die Ausgabe direkt an den Prüfer geben:

```sh
while read -r name rest; do
  node .claude/tools/pruef-clip.mjs "clips/$name.html" $rest
done < zeiten.txt
```

**Und die Bilder ansehen.** Der Prüfer sieht Überlappung und Überlauf, nicht Gestaltung.

---

## Schritt 5 — Die Seite

Skelett von `leitprogramme/uebungspruefung-1.html` kopieren; der `<style>`-Block stammt
seinerseits aus `leitprogramme/potenzen.html` und bleibt unverändert. Eigene Regeln nur
hinten anhängen.

### Was diese Seitenart zusätzlich braucht

```css
/* Die Clipkarte sitzt zwischen Frage und Loesungsaufklapper, gleich
   eingerueckt — sonst zerreisst sie die Nummernspalte links. */
.clipkarte.zu-aufg{margin:9px 0 0 calc(5.8em + 11px)}
@media(max-width:600px){ .clipkarte.zu-aufg{margin-left:0} }

/* Punktezeile unter der Loesung: was der Korrektor zaehlt. */
.pkt-hinweis{font-family:var(--sans);font-size:.83rem;color:var(--tinte-2);
  border-left:2.5px solid var(--orange-rand);padding-left:11px;margin:9px 0 0}
```

Die Punktezeile ist **orange** und damit nach §5.1 „Aufgabe/Übung" — das ist die richtige
Bedeutung: Sie sagt, was in der Prüfung zählt.

### Ein Aufgabenblock

Ein `.test`-Block je *Aufgabe* (nicht je Teilaufgabe) — sein Hakenfeld speist den
Fortschrittsbalken, und man hakt eine Aufgabe ab, nicht eine halbe.

```html
<div class="test" data-test="c7">
  <div class="test-kopf">
    <h3>Aufgabe C7 <span class="summe">· 3 P</span></h3>
    <span class="werkz">
      <button type="button" class="alle-loesungen">alle Lösungen</button>
      <label><input type="checkbox" class="erledigt"> erledigt</label>
    </span>
  </div>
  <ol class="aufg">
    <li>
      <div class="frage"><span class="nr">C7</span><span class="pkt">(3 P)</span>
        <span class="txt">…Aufgabentext wörtlich…</span></div>
      <div class="clipkarte zu-aufg" data-clip="clips/pruefung1-c7-….html" data-titel="…">
        <button class="clip-start" type="button">…</button>
      </div>
      <details class="loes"><summary>Lösung</summary><div class="inhaltbox">
        <p>…Schritt…</p>
        <p class="komm">…warum…</p>
        <p class="pkt-hinweis">1 P für …, je 0.5 P für …</p>
      </div></details>
    </li>
  </ol>
</div>
```

### Laufzeiten eintragen

Die Karte zeigt die Dauer. Nicht abtippen — aus den Drehbüchern holen, nachdem der Ton
steht. Im Markup einen Platzhalter setzen (`data-zeit="<dateiname>"`) und danach füllen:

```python
sek = round(sum(sz['dauer'] for sz in json.load(open(pfad))['szenen']))
f'{sek//60}:{sek%60:02d}'
```

### Ein roter Faden je Teil

Was die Seite über eine Sammlung von Lösungen hebt, ist der Satz, der mehrere Aufgaben
zugleich erklärt. Im ersten Durchgang war das für Teil C die Tabelle zu \(k \cdot x = m\)
mit ihren drei Ausgängen — sie sagt C1a, C1b, C2b, C6 und C7 vorweg. Solche Tabelle in
einen `.merk`-Kasten **vor** den ersten Aufgabenblock des Teils.

---

## Schritt 6 — Eintragen, oder bewusst nicht

Eine Übungsprüfung ist oft **nicht** für die ganze Welt gedacht. Zwei Wege:

### a) Öffentlich, wie jedes Leitprogramm

`leitprogramme.html` (Karte), `scripts/build-seo.py` (`SEITEN`),
`scripts/build-suchindex.py` (Liste der Nachschlagewerke) — siehe
`HOWTO-leitprogramme.md` Punkt 9.

### b) Unverlinkt, nur über den Direktlink

**Alle drei Stellen zusammen, sonst wirkt es nicht:**

| | |
|---|---|
| `leitprogramme.html` | **keine** Karte |
| `scripts/build-suchindex.py` | **kein** Eintrag — sonst steht die Seite in der Volltextsuche |
| `scripts/build-seo.py` | Eintrag **mit `noindex=True`** — nicht weglassen, sonst fehlen Beschreibung und canonical |

`noindex=True` nimmt die Seite aus `sitemap.xml` **und** setzt
`<meta name="robots" content="noindex, nofollow">` in den generierten Kopfblock. Beides
zusammen ist nötig: Die Sitemap allein hält keine Suchmaschine ab, die die URL anderswoher
kennt — aus einem geteilten Link, einem Referrer, einer Browserleiste. Das `nofollow`
hält von der Seite aus auch die Clipdateien aus dem Index.

**Kein `Disallow` in `robots.txt`.** Die Datei ist öffentlich lesbar; ein Eintrag dort
würde die URL gerade bekanntmachen, statt sie zu verbergen.

**Und die Grenze aussprechen:** Das ist Unauffindbarkeit, keine Zugangskontrolle. Wer den
Link hat, kommt hinein, und wer ihn weitergibt, gibt den Zugang weiter. Für echten Schutz
bräuchte es etwas anderes als GitHub Pages.

Danach in beiden Fällen:

```sh
python3 scripts/build-seo.py --schreiben
python3 scripts/build-suchindex.py
```

---

## Schritt 7 — Prüfen

```sh
python3 .claude/skills/preflight/preflight.py \
        leitprogramme/uebungspruefung-1.html leitprogramme.html clips/pruefung1-*.html

python3 -m http.server 8899 &        # zum Spulen im Ton reicht das nicht, siehe unten
node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/uebungspruefung-1.html
```

**Was keine Prüfung sieht** — dafür in den Browser, hell und dunkel, 1280 px und 360 px:

- **Waagrechter Überlauf.** Im ersten Durchgang 61 px auf 360 px, aus zwei Ursachen:
  eine Tabelle in einem `.bewertung`-Block erbte von dort
  `td:first-child { white-space:nowrap }`, und ein `.band` mit langem Text konnte wegen
  `white-space:nowrap` nicht umbrechen. Messen statt schauen:
  `document.documentElement.scrollWidth - document.documentElement.clientWidth`.
- **Zu stark verkleinerte Formeln.** `mjx-container { max-width:100% }` (aus dem
  geerbten Layout) *skaliert* eine zu breite Formel, statt sie scrollen zu lassen. Im
  ersten Durchgang schrumpften 22 Formeln unter 82 %, die schlimmste auf 51 % —
  unlesbar auf dem Telefon. Behoben durch **Zerlegen der Ketten in Zwischenschritte**,
  nicht durch eine Stiländerung; danach blieben 11 Formeln über 63 %, und das sind die
  wörtlichen Aufgabentexte, die man nicht umbrechen darf.
- **Der Schlusspunkt nach einer Formel.** `\(…\)` gefolgt von `.` bricht den Punkt allein
  auf die nächste Zeile. Repo-Konvention (siehe `potenzen.html`): nach einer
  schliessenden Formel steht kein Punkt.
- **Der Ton.** Zum Spulen braucht der lokale Server **Range-Requests**;
  `python3 -m http.server` kann das nicht, und der Klick auf den Fortschrittsbalken wirft
  den Ton dann an den Anfang zurück. Das sieht wie ein Fehler im Clip aus und ist keiner.

---

## Aufwand — was der erste Durchgang gekostet hat

| | |
|---|---|
| Teilaufgaben | 26 |
| Clips | 26, zusammen 20:28 min |
| Vertonung | rund 7 min Rechenzeit (16 s je Clip, Thorsten) |
| Tonspuren | 6.4 MB |
| Seite | rund 1 570 Zeilen, 421 gesetzte Ausdrücke |
| Suchabschnitte | 20 — bei Variante (b) allerdings 0, die Seite steht nicht im Index |
| Fehler aus der PDF-Extraktion | 2 von 26 Teilaufgaben |
| Fehler, die erst der Browser zeigte | 3 (Überlauf, Formelgrösse, Schlusspunkt) |

---

## Nicht tun

- **Die Aufgabentexte nicht umformulieren.** Sie stehen wörtlich da, samt Punktzahl.
  Wer sie glättet, erklärt eine andere Prüfung als die, die geschrieben wurde.
- **Den Prüfungsbogen nicht weglassen**, um Wiederholung zu sparen. Ohne ihn ist die
  Seite eine Lösungssammlung, und der erste Schritt — selber schreiben — fällt aus.
- **Die Clips nicht in die Bibliothek lassen.** Ohne `"probe": true` wachsen `clips.json`
  und acht Lektionsseiten mit, ungefragt.
- **Die Punktezeile nicht erfinden.** Sie kommt aus der Musterlösung. Steht dort keine
  Aufteilung, schreibt man keine hin.
