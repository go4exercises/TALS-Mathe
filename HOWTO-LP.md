# HOWTO — Leitprogramme (Gesamtfassung, Probe)

**Status: Probefassung vom 30.09.2026.** Führt `HOWTO-leitprogramm-didaktik.md` (was
hineingehört) und `HOWTO-leitprogramme.md` (wie es ins Repo kommt) zu einer Datei
zusammen, löst ihre Widersprüche auf und ergänzt zwei Punkte, die in beiden fehlten:
die **Bindung an den RLP** (§1) und die **Nutzung der Bildschirmbreite** (§6). Erprobt an
`leitprogramme/quadratische-funktionen.html`. Wird die Fassung übernommen, ersetzt sie
beide Vorgänger; `HOWTO-uebungspruefung.md` bleibt für die Art «Übungsprüfung» zuständig.
Bei Widerspruch gilt `STYLEGUIDE.md` §6.5.

Wo diese Datei von einem Vorgänger abweicht, steht es als **⟂ Entscheid** dabei.

---

## 0 · Zwei Arten, ein Layout

| | gegliedert nach | Beispiele | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vorwissen, Kapitel, Gesamttest | `potenzen`, `quadratische-gleichungen`, `gleichungssysteme` | diese Datei |
| **Übungsprüfung** | dem Prüfungsbogen: je Teilaufgabe Clip, Musterlösung, Punktezeile | `uebungspruefung-1`, `trigo2` | `HOWTO-uebungspruefung.md` |

Layout, Kopf, Fuss, Farbtokens und Clip-Bühne sind bei beiden dieselben (§11–§12 gelten
für beide).

---

## 1 · Grundsatz: RLP → Themenseite → Leitprogramm

Drei Ebenen, jede begrenzt die nächste:

1. **Der RLP bestimmt, *was* gelernt wird.** Quelle: `../Math-GL.pdf` (Grundlagenfach,
   RLP-BM, Abschnitt 6.4.4.1, Gruppe 1) und `../Math-SP.pdf` (Schwerpunktfach, 7.4.4).
   Ein Leitprogramm deckt die **fachlichen Kompetenzen genau eines Teilgebiets** ab
   (z. B. GF 3.3) oder einer klar benannten Teilmenge davon — und **nichts darüber
   hinaus**.
2. **Die Themenseite bestimmt, *wie* es heisst und aussieht:** Begriffe, Notation,
   Vorzeichenkonventionen, Achsen, Konstanten, Merksätze, Beispiele. Das Leitprogramm
   erfindet nichts Eigenes.
3. **Das Leitprogramm bestimmt nur den Weg:** Reihenfolge, Umfang, Tests.

### 1.1 Bindung an den RLP (neu)

- **Kompetenzliste wörtlich übernehmen.** Die Kompetenzen des Teilgebiets stehen
  wörtlich (1:1 wie in der RLP-Box der Themenseite) als Kommentarblock im Kopf der
  Leitprogramm-Datei und nummeriert (K1, K2, …) in der Planung (§2).
- **Jedes Kapitelziel gehört zu mindestens einer Kompetenz**, und jede Kompetenz des
  Teilgebiets zu mindestens einem Kapitel. Ein Ziel ohne Kompetenz fliegt raus; eine
  Kompetenz ohne Kapitel wird im Kopf ausdrücklich ausgeschlossen («nicht in diesem
  Leitprogramm: … → eigenes Leitprogramm / Themenseite»).
- **Vorwissen darf aus früheren Teilgebieten stammen** (mit Nummer, z. B. «GF 2.2»),
  aber nicht aus späteren und nicht aus dem Schwerpunktfach, wenn das Leitprogramm im
  Grundlagenfach steht.
- **Was die Themenseite über den RLP hinaus bietet, bleibt dort** — Notationen anderer
  Lehrmittel, Zusatzverfahren, Exkurse. Im Leitprogramm höchstens als Satz «Mehr dazu auf
  der Themenseite».
- **«auch ohne Hilfsmittel» ist verbindlich.** Trägt eine Kompetenz den Vermerk, werden
  ihre Aufgaben im Gesamttest ohne Taschenrechner gestellt. Kompetenzen ohne Vermerk
  dürfen den Rechner verwenden; Rechner-Clips (`werkzeug: true`) gehören dann dazu. Die
  Hilfsmittel stehen im Kopf des Gesamttests, je Teil.
- **Zuordnung sichtbar machen.** Jedes Kapitel trägt in `.kap-meta` die RLP-Nummer
  (`GF 3.3`) und die Kompetenz-Kürzel (`K1 · K2`); die Selbsteinschätzung verweist von
  Testteil über Kapitel auf die Kompetenz.

⟂ Entscheid: Die Didaktik-Fassung sagte «keine Inhalte, die *weder* auf der Themenseite
*noch* im RLP stehen» — damit war alles erlaubt, was irgendwo auf der Themenseite steht.
Jetzt gilt: RLP **und** Themenseite.

### 1.2 Themenseite als fachliche Wahrheit

Variation zwischen den beiden Spuren ist erlaubt, wenn sie eine Funktion hat (anderes
Format, weniger Regler, anderer Kontext). Zufällige Abweichung ist ein Fehler.
**Prüfkriterium:** Lässt sich in einem Satz sagen, *warum* das Leitprogramm es anders
macht? Ja → bleibt, und der Satz steht als Kommentar im Code. Nein → angleichen.

| | Themenseite | Leitprogramm |
|---|---|---|
| Rolle | Referenz: nachschlagen, erkunden, im Unterricht zeigen | geführter Pfad: selbstständig erarbeiten, nachholen |
| Umfang | ganzes Teilgebiet, samt Exkursen | die RLP-Kompetenzen, ausdrücklich abgegrenzt |
| Reihenfolge | nach Sachlogik, springbar | linear, jeder Schritt baut auf dem vorigen auf |
| Animationen | offen, mehrere Regler | Erkundungsauftrag mit einer Frage |
| Übungen | Mini-Checks, Aufgaben A1–A7 | Vortest, Selbsttests mit Punkten, Gesamttest |

---

## 2 · Planung (Pflicht, vor dem HTML)

Aus RLP, Themenseite, Clips und Styleguide entstehen vier Dinge:

**a) Kompetenzmatrix**

```
Kompetenz (RLP, wörtlich gekürzt) | ohne HM? | Kapitel | Selbsttest-Aufg. | Gesamttest-Aufg.
```

**b) Planungstabelle**

```
Kapitel | Lernziel («Du …») | Kompetenz | Clip(s) | Erkundung (Anker) | Beispiel (Quelle) | Häufiger Fehler | min
```

**c) Kern / Vertiefung / bewusst weggelassen.** Was weggelassen wird, steht später im
Leitprogramm als «Nicht in diesem Leitprogramm → Themenseite, Abschnitt …».

**d) Konventionen und Widersprüche.** Liste der Begriffe, Notation, Vorzeichen, Achsen,
Einheiten der Themenseite — und alles, was sich **in der Themenseite selbst**
widerspricht (Text gegen eigene Clips, Tabelle gegen Mini-Check). Widersprüche werden
**nicht** ins Leitprogramm übernommen, sondern gemeldet und zuerst in der Themenseite
entschieden. Wo das Leitprogramm trotzdem schon entstehen soll: die Konvention der
Themenseite nehmen (nicht die des Clips) und die Abweichung im Text in einem Satz
benennen.

⟂ Entscheid: Die Didaktik-Fassung verlangte, die Planungstabelle **vor** jeder Zeile
HTML vorzulegen; `CLAUDE.md` verlangt, klare Aufträge direkt umzusetzen. Jetzt: Die
Planung steht als HTML-Kommentar im Kopf der Datei und im Bericht (§14). **Vorgelegt und
abgewartet** wird nur, wenn (d) einen Widerspruch enthält, der ein Kernkapitel betrifft,
oder wenn eine RLP-Kompetenz sich nicht in 2–3 Lektionen unterbringen lässt.

---

## 3 · Umfang und Zeit

- **Eine Lektion = 45 Minuten.** Die Minuten der Kapitel (inkl. Vorwissen und
  Gesamttest) werden addiert; die Summe bestimmt die Lektionenzahl im Kopf. «Zwei
  Lektionen» bei 130 Minuten ist falsch.
- **Zielgrösse 2–3 Lektionen**, 4–5 Kapitel plus Vorwissen und Gesamttest, ein Kapitel =
  eine Idee, höchstens 30 Minuten.
- **Clips:** rund 6–11 Clips, 8–12 Minuten Clipzeit (STYLEGUIDE §6.5).
- **Mehr als 4 Lektionen oder deutlich mehr als 11 Clips → teilen**, jedes Teil mit
  eigenem Vorwissen und Gesamttest (Vorbild: *Quadratische Gleichungen* /
  *Gleichungssysteme*, 07.09.2026).
- Der Kern ist, was ohne Leitprogramm in der Prüfung fehlen würde. Parameter,
  Spezialfälle, zweite Methoden → «Vertiefung» oder Themenseite.

⟂ Entscheid: Didaktik «3–5 Kapitel», Styleguide «vier bis fünf» → **4–5**.

---

## 4 · Aufbau der Seite

```
Kopf          Titel · Standfirst · Fach + Teilgebiet (RLP) · Lektionen
Ablauf        Kapitelliste nach Lektionen, Fortschrittszähler      (Schiene links)
So arbeitest  Clip → Text mitrechnen → Selbsttest ohne Lösung → abhaken
Kompetenzen   RLP-Liste des Teilgebiets, K1…Kn, mit «ohne HM»-Vermerk; Abgrenzung
Kapitel 0     Vorwissen: kurze Klärung + Vortest (Verweis auf Vorwissens-LP/Themenseite)
Kapitel 1…n   je: Lernziel · Clip · Kerntext · Beispiel · Häufiger Fehler ·
              [Erkundung] · Ausführlich-Link · Selbsttest
Gesamttest    Teile A/B/C ↔ Kapitel ↔ Kompetenzen · Hilfsmittel je Teil · Punkte
Einschätzung  Punktebereiche → konkrete Rückverweise auf Kapitel
Weiter        nächstes Leitprogramm · Themenseite · bewusst Weggelassenes
```

### Innerhalb eines Kapitels

1. **Lernziel** in `<p class="ziel">`, ein Satz in Du-Form: «Du liest …, bestimmst …,
   begründest …».
2. **Clip zuerst** (Gedankengang), dann der Text, der ihn vollständig macht. Ein Clip
   allein ist keine Einführung: Wer ihn überspringt, muss das Verfahren im Text finden.
3. **Kerntext kurz.** Merkkasten mit **demselben Wortlaut** wie auf der Themenseite.
4. **Ein durchgerechnetes Beispiel** mit Zwischenschritten, möglichst dasselbe wie im
   Clip davor — sonst sagen, dass es ein anderes ist.
5. **Häufiger Fehler**, übernommen aus der Themenseite, wenn vorhanden.
6. **Erkundung** (optional, §8).
7. **«Ausführlich: …»** — ein Absatz mit Link auf den passenden Abschnitt oder Clip der
   Themenseite.
8. **Selbsttest** (§9).

⟂ Entscheid: Didaktik «Mehr dazu» *am Ende* des Kapitels, Technik «Ausführlich» *vor*
dem Selbsttest. Gilt jetzt **«Ausführlich:» vor dem Selbsttest** — so machen es die
bestehenden Leitprogramme, und der Selbsttest bleibt das Letzte, was man im Kapitel tut.

---

## 5 · Entstehung: im Repo, nicht extern

**Der Normalfall ist: eine bestehende Leitprogramm-Seite kopieren** und nur den Inhalt
ersetzen — Kopf, Schiene, Anleitung, Kapitel, Fuss. Dann stehen Dokumentrahmen,
Hosts, Stylesheets, Tokens, Dunkelmodus und Skripte schon richtig (§11). **Nicht
vergessen:** die `localStorage`-Schlüssel (`lp-<name>-thema`, `lp-<name>-stand`), sonst
teilen zwei Leitprogramme einen Fortschrittsstand.

Kommt eine Datei von aussen, gilt die Übertragsliste in §12.

---

## 6 · Layout und Bildschirmbreite (neu)

### Befund

Das Raster der bestehenden Leitprogramme: `.huelle` max. 1180 px, Schiene 236 px,
Abstand 52 px, und `.inhalt` **max. 70ch** — bei 17 px Serif rund 620 px. Auf einem
1280-px-Schirm bleiben rechts vom Text rund 230 px leer, ab 1440 px wächst der leere Rand
auf beiden Seiten. Beispiele, Tabellen und Tests sind dadurch schmaler als nötig, und
ein Graph lässt sich nicht neben den Text stellen, der ihn erklärt.

### Regel: Fliesstext schmal, Arbeitsflächen breit

- **Fliesstext bleibt lesbar schmal:** Absätze, Lernziel, Überschriften höchstens
  **68ch**. Das ist die Zeilenlänge, bei der man am Stück lesen kann — sie wird nicht
  geopfert.
- **Arbeitsflächen nutzen die ganze Spalte:** Beispiel-Tabellen, Selbsttests,
  Gesamttest, Erkundungen, Simulationen, Merk-/Warnkästen. Dafür bekommt `.inhalt`
  **kein** `max-width` mehr; die Begrenzung sitzt auf den Textelementen.
- **Hülle breiter:** `.huelle` max. **1440 px**. Ab 1000 px Schiene links wie bisher.
- **Nebeneinander ab 1180 px:** Der Baustein `.duo` stellt zwei zusammengehörige Teile
  nebeneinander — Beispiel neben Graph, Clip + Merkkasten neben Häufigem Fehler,
  Simulation neben ihrer Anleitung. Darunter stapeln sie sich in Lesereihenfolge (erst
  links, dann rechts). **Die Reihenfolge im Quelltext ist die Lesereihenfolge auf dem
  Handy.**
- **Selbsttests zweispaltig ab 1180 px** (`.aufg.zwei`), wenn die Aufgaben kurz sind;
  jede Aufgabe samt aufklappbarer Lösung bleibt eine Zelle (`break-inside: avoid`).
- **Nicht alles verbreitern.** `.duo` nur, wo die beiden Hälften wirklich zusammen
  angeschaut werden. Zwei unabhängige Kästen nebeneinander zwingen das Auge zum
  Pendeln.
- **Prüfen bei 360, 1280 und 1600 px** (§14); `npm run render-check` meldet seitliches
  Scrollen.

```css
.huelle{max-width:1440px}
.inhalt{min-width:0}                        /* kein max-width mehr */
.kap>p,.kap>h2,.kap>h3,.ziel,.anleitung ol{max-width:68ch}
.duo{display:grid;gap:22px}
@media(min-width:1180px){
  .duo{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}
  .aufg.zwei{columns:2;column-gap:34px}
  .aufg.zwei>li{break-inside:avoid}
}
```

---

## 7 · Clips

- **Nur bestehende Clips**, dieselben Dateien wie auf der Themenseite. Keine fast
  gleichen Varianten mit anderen Zahlen.
- **Themenclips** (Alltagsfrage, Verfahren, «Zum Mitnehmen») passen ins Leitprogramm.
- **Animations-Clips** (`*-anim-*`, «In der Animation hast du …») setzen voraus, dass
  die Animation bedient wurde — nur nach einer Erkundung (§8a).
- **Rechner-Clips** (`werkzeug: true`) nur bei Kompetenzen **ohne** «auch ohne
  Hilfsmittel» im Kern, sonst als «Kontrolle mit dem Rechner» nach dem Handverfahren.
- **Clips anderer Themenseiten** sind im Vorwissen erwünscht.
- **Zahlen im Clip = Zahlen im Text direkt danach.** Widerspricht eine Simulation ihrem
  Clip, wird die Simulation angepasst, nicht der Clip (neu vertonen ist teuer).
- **Dauer** von der Themenseite übernehmen (`cl-zeit` bzw. aria-label des «▶ Clip»),
  nicht aus dem Drehbuch summieren.
- Fehlt für einen Kernschritt ein Clip: melden, nicht ohne Auftrag bauen.

---

## 8 · Erkundungen und Simulationen

Entscheid pro Kapitel, in dieser Reihenfolge:

**a) Eine Animation der Themenseite passt → Erkundungsauftrag, keine Code-Kopie.**
Kasten «🔍 Erkunden» mit Link auf den Anker (`../grundlagen/<seite>.html#anim-…`, neuer
Tab) und einem **konkreten Auftrag**: was einstellen, was beobachten, was notieren. Die
Frage kommt im Selbsttest wieder. Danach darf der passende `*-anim-*`-Clip folgen.
Höchstens eine Erkundung pro Kapitel.

**b) Das Leitprogramm braucht eine geführte Variante** (ein bis drei Regler, eine
Aussage, eingebettet) → kleine SVG-Simulation. Verbindlich:
- Achsen, Variablennamen, Einheiten, Konstanten, **Reglerfarben** (`akz-blau/orange/
  gruen`) identisch zur Themenseiten-Animation
- **Startwert = Beispiel im Text bzw. Clip** desselben Kapitels
- Merksatz in der Bildlegende gleichlautend wie in der «Erkenntnis» der Themenseite
- der Unterschied zur Themenseiten-Animation als Ein-Satz-Kommentar im Code
- Reglerenden und Sichtfenster vorab mit `python3` durchrechnen (bleibt der Scheitel
  im Bild? wo stehen Beschriftungen?)
- steht in einem `.duo` neben dem Text, der sie erklärt (§6)

**c) Reine Rechentechnik → keine Animation.** Erlaubt, aber mindestens das Kernkapitel
hat eine Erkundung.

---

## 9 · Selbsttests und Gesamttest

- **Vortest** prüft nur Voraussetzungen, 8–13 Punkte, mit Verweis bei Lücken.
- **Selbsttest je Kapitel**, 7–16 Punkte, 3–6 Aufgaben à 2–5 Punkte. Mischung:
  Rechnen · Erkennen/Entscheiden · Begründen (mindestens eine «Warum»-Frage).
- **Kein Selbsttest wiederholt ein Beispiel** (gleicher Typ, andere Zahlen), **kein
  Gesamttest einen Selbsttest.**
- **Jedes Kapitelziel wird geprüft; nichts wird geprüft, was nicht eingeführt ist.**
- **Lösung aufklappbar**, darunter optional eine Zeile `.komm` zur typischen
  Fehlerquelle.
- **Gesamttest** 20–25 Punkte, rund 20 Minuten, Teile = Kapitel = Kompetenzen, Hilfsmittel
  je Teil nach RLP-Vermerk (§1.1).
- **Selbsteinschätzung** mit Punktebereichen, die auf **bestimmte Kapitel** zurückverweisen.
- Punkte summieren (Kopf = Summe der Aufgaben), Minuten summieren (§3).

---

## 10 · Notation und Fachsprache

Immer nach `STYLEGUIDE.md`. Beim Vergleich schiefgegangen:

| Was | Regel |
|---|---|
| Lösungsmenge | `\mathbb{L}`, nie ein einfaches L (§2.11) |
| leere Menge | `\mathbb{L} = \{\,\}` |
| Elemente einer Menge | Strichpunkt: `\{-3;\ 3\}` (§2.11, seit 29.09.2026) |
| Lösung eines Systems | als Menge: `\mathbb{L} = \{(2 \mid 3)\}` |
| Parametrisierte Menge | Doppelpunkt: `\{(x \mid 2x-3) : x \in \mathbb{R}\}` |
| Intervalle | `]a;\, b[` |
| Zahlen | Dezimalpunkt; Brüche, wo die Themenseite Brüche verwendet |
| Fachbegriffe | der Begriff der Themenseite **und**, wo er abweicht, der des RLP in Klammern (z. B. «allgemeine Form (Grundform)») |
| Methodenwahl | andere Hauptmethode als die Themenseite → beide nennen, Wahl in einem Satz begründen |

Sprache: Du-Form, kurze Sätze, Schweizer Rechtschreibung (ss), kein «wir».

---

## 11 · Technisches Gerüst (gilt immer)

Steht in jeder kopierten Vorlage schon richtig; bei einer Datei von aussen §12.

- Datei unter `leitprogramme/<name>.html`, **genau eine Ebene** unter der Wurzel.
- `<!DOCTYPE html>`, `<html lang="de-CH">`, `<meta charset="UTF-8">`, Viewport.
- **Kein fremder Host:** `../schriften.css`, `../vendor/mathjax/tex-svg.js`.
- **`../style.css` vor dem eigenen `<style>`** — der eigene gewinnt bei gleichem Gewicht.
- **Tokens erben:** im eigenen `:root` nur Übersetzungen (`--karte:var(--weiss)`) und
  der Dunkelmodus; dieser setzt `--weiss` mit und behandelt `.site-footer` eigens.
- **Kopf und Fuss der Site:** `<div id="nav-root">`, `.site-footer` nach STYLEGUIDE §7,
  am Schluss `../mathlib.js`, `../nav.js`, `buildNav({ id: 'leitprogramme' })`.
- **Clip-Bühne aus `mathlib.js`** (`clipBuehne(quelle, titel)`), `BASIS = '../'`.
- **`h2` mit `id`** (Suche schneidet an `h2[id]`); keine `id` doppelt zwischen
  `<section>` und Überschrift.
- **Nicht in `page-wrap` + `main.content` pressen.**

---

## 12 · Übertragsliste für extern gebaute Dateien

Der Reihe nach; in Klammern, woran man merkt, dass der Punkt fehlt.

1. Nach `leitprogramme/<name>.html` verschieben.
2. Google-Fonts-/CDN-Zeilen samt `preconnect` streichen, lokale Pfade setzen (Pre-Flight
   meldet Hosts; ohne Netz Georgia).
3. Dokumentrahmen und Zeichensatz ergänzen (Umlaute zerfallen, erst im Browser).
4. `id` an alle Kapitel-`h2` (Suche findet nur einen Treffer).
5. `BASIS` relativ (Vorschau zeigt Live-Clips).
6. `style.css`, Kopf, Fuss, Skripte einbauen; mitgelieferte Bühne löschen (Sackgasse).
7. Mitgelieferte Palette löschen, soweit mit `style.css` gleich (läuft auseinander).
8. Dunkelmodus: `--weiss` mitsetzen, `.site-footer` eigens (weisse Kopfleiste, weisser Fuss).
9. Eintragen (§13).
10. Layout nach §6 nachziehen.

---

## 13 · Verknüpfen und Eintragen

**Vier Stellen** — fehlt eine, ist die Seite unsichtbar, unauffindbar oder einseitig:

| Datei | was |
|---|---|
| `leitprogramme.html` | Karte im passenden Abschnitt (*nach Thema* / *nach Prüfungsbogen*) |
| `scripts/build-seo.py` | Eintrag in `SEITEN` (Beschreibung, Sitemap) |
| `scripts/build-suchindex.py` | Eintrag in der Liste der Nachschlagewerke |
| Themenseite | Kasten nach den Lernzielen: «🧭 Lieber geführt? Leitprogramm *…* (≈ n Lektionen)» |

Danach `python3 scripts/build-seo.py` und `python3 scripts/build-suchindex.py` (beide schreiben ohne Schalter; `--schreiben` aus der alten Fassung gibt es nicht).

Im Leitprogramm selbst: «Ausführlich»-Link je Kapitel (§4), Vorwissen verweist auf das
vorausgehende Leitprogramm, der Schluss auf das folgende und auf das bewusst
Weggelassene.

⟂ Entscheid: Die Technik-Fassung kannte drei Stellen, die Didaktik-Fassung forderte den
Themenseiten-Kasten zusätzlich. Jetzt sind es vier.

**Unverlinkt veröffentlichen** (Probe, Übungsprüfung per Link): keine Karte, kein
Suchindex, Themenseite ohne Kasten, aber `build-seo.py` **mit `noindex=True`** (nicht
weglassen). Kein `Disallow` in `robots.txt`. Es ist Unauffindbarkeit, keine
Zugangskontrolle. Prüfen:

```sh
grep -c "<dateiname>" sitemap.xml suchindex.js leitprogramme.html   # dreimal 0
grep 'name="robots"' leitprogramme/<name>.html                      # noindex, nofollow
```

---

## 14 · Abnahme vor dem Commit

1. **Jede Lösung nachrechnen** mit einem kurzen `python3`-Skript. Keine Zahl ungeprüft.
2. **Kompetenzmatrix vollständig:** jede Kompetenz ↔ Kapitel ↔ Test; kein Ziel ohne
   Kompetenz; Hilfsmittel im Gesamttest stimmen mit den RLP-Vermerken.
3. Punkte- und Minutensummen stimmen mit Kopf, Ablauf und Testköpfen überein.
4. Konventions-Grep gegen die Themenseite: Fachbegriffe, `\mathbb{L}`, Strichpunkt in
   Mengen, Scheitel-/Parameterbuchstaben, Achsen.
5. Clip-Zahlen gegen Text und Simulationsstartwerte desselben Kapitels.
6. Links in beide Richtungen; Anker der Erkundungen existieren
   (`grep -o 'id="anim-…"'` auf der Themenseite).
7. Kein Selbsttest wiederholt ein Beispiel, kein Gesamttest einen Selbsttest.
8. Technik:
   ```bash
   python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html leitprogramme.html
   python3 -m http.server 8899 &
   node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/<name>.html
   node .claude/tools/render-check.mjs leitprogramme/<name>.html
   ```
   und **hinschauen**: hell und dunkel, 360 / 1280 / 1600 px. Keine Prüfung sieht
   zerfallene Umlaute, eine weisse Kopfleiste über dunkler Seite oder einen Clip vom
   Live-Stand.
9. **Bericht** an den Auftraggeber: Planung (§2), was bewusst anders ist als auf der
   Themenseite und warum, welche Widersprüche in der Themenseite gefunden wurden, welche
   Clips fehlen.

---

## Nicht tun

- Keine Inhalte jenseits der RLP-Kompetenzen des Teilgebiets.
- Keine Animation der Themenseite kopieren — verlinken (§8a) oder bewusst reduziert
  nachbauen (§8b).
- Keine neuen Beispiele erfinden, wenn die Themenseite ein passendes hat.
- Nicht still angleichen, wenn die Themenseite widersprüchlich ist. Melden.
- Keine Bühne, keine Palette doppelt halten.
- Rechnerangaben nur mit Beleg (`HOWTO-clips.md`, «Rechneranzeige»).
