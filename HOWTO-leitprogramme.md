# HOWTO — Leitprogramme

**Gilt seit 02.10.2026.** Was in ein Leitprogramm gehört, in welcher Reihenfolge, und wie es
technisch ins Repo kommt — für die Art «nach Thema». Die Art «Übungsprüfung» hat ihre eigene
Anleitung (`HOWTO-uebungspruefung.md`); Layout, Gerüst und Eintragen (§6, §11–§13) gelten für
beide. Bei Widerspruch gilt `STYLEGUIDE.md` §6.5.

Entstanden am 30.09.–02.10.2026 aus der früheren technischen Anleitung (gleicher Dateiname)
und einer Didaktik-Anleitung, erprobt an `leitprogramme/quadratische-funktionen.html`. Wo die
Fassung bewusst von einem der Vorgänger abweicht, steht es als **⟂ Entscheid** dabei; die
Vorgänger stehen in der Git-Geschichte (bis Commit `9c1a4a5`).

**Vorbild für ein neues Leitprogramm:** `leitprogramme/quadratische-funktionen.html`, gebaut mit
`scripts/lp/quadratische-funktionen/seite.py` (siehe dortige README).
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

1. **Der RLP bestimmt, *was* gelernt wird — und wie die Begriffe heissen.** Quelle: `../Math-GL.pdf` (Grundlagenfach,
   RLP-BM, Abschnitt 6.4.4.1, Gruppe 1) und `../Math-SP.pdf` (Schwerpunktfach, 7.4.4).
   Ein Leitprogramm deckt die **fachlichen Kompetenzen genau eines Teilgebiets** ab
   (z. B. GF 3.3) oder einer klar benannten Teilmenge davon — und **nichts darüber
   hinaus**.
2. **Die Themenseite bestimmt, *wie* es aussieht:** Notation,
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
oder wenn eine RLP-Kompetenz sich nicht im Zeitrahmen von §3 unterbringen lässt.

---

## 3 · Umfang und Zeit

- **Eine Lektion = 45 Minuten.** Die Minuten der Kapitel (inkl. Vorwissen und
  Gesamttest) werden addiert; die Summe bestimmt die Lektionenzahl im Kopf. «Zwei
  Lektionen» bei 130 Minuten ist falsch.
- **Zielgrösse nach Format** (Entscheid Auftraggeber 03.10.2026):

  | Format | Kapitel | Gesamt |
  |---|---|---|
  | **Kapitelmuster** (§4; Einführungsclip → Animation → Kontrollclip → Übungen → Aufgaben; Vorbild *Quadratische Funktionen*) | 4–5 Kapitel, je 35–45 Minuten — ein Kapitel ≈ eine Lektion | bis 5 Lektionen plus Vorwissen und Gesamttest |
  | **klassisch** (Leitprogramme vor dem 02.10.2026) | 4–5 Kapitel, je höchstens 30 Minuten | 2–3 Lektionen plus Vorwissen und Gesamttest |

  Ein Kapitel = eine Idee, in beiden Formaten.
- **Clips:** rund 6–11 Clips, 8–12 Minuten Clipzeit (STYLEGUIDE §6.5).
- **Über der Zielgrösse (klassisch mehr als 4, Kapitelmuster mehr als 5 Lektionen ohne
  Gesamttest) oder deutlich mehr als 11 Clips → teilen**, jedes Teil mit
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
So arbeitest  ① Erfahren → ② Clip → ③ Verallgemeinern → ④ Üben (ohne Lösung) → abhaken
Kompetenzen   RLP-Liste des Teilgebiets, K1…Kn, mit «ohne HM»-Vermerk; Abgrenzung
Kapitel 0     Vorwissen: kurze Klärung + Vortest (Verweis auf Vorwissens-LP/Themenseite)
Kapitel 1…n   je: Lernziel · ① Erfahren (Simulation) · ② Clip · ③ Verallgemeinern
              (Regel, Definition, Beispiel, Häufiger Fehler) · Ausführlich-Link · ④ Üben
Gesamttest    Teile A/B/C ↔ Kapitel ↔ Kompetenzen · Hilfsmittel je Teil · Punkte
Einschätzung  Punktebereiche → konkrete Rückverweise auf Kapitel
Weiter        nächstes Leitprogramm · Themenseite · bewusst Weggelassenes
```

### Innerhalb eines Kapitels: das Muster (Fassung 3, 02.10.2026)

Alle Kapitel von `leitprogramme/quadratische-funktionen.html` folgen diesem Muster; die Seite
entsteht aus einer Kapitelbeschreibung, damit es überall gleich bleibt. Phasen
(`<p class="phase">`) über den Abschnitten — **kein** Fahrplan unter dem Kapiteltitel
(Entscheid 02.10.2026). «So arbeitest du» und die RLP-Kompetenzen stehen oben, beide
eingeklappt (`details.anleitung`).

1. **① Clip.** Ein Einführungsclip zeigt **alles**, was das Kapitel bringt — in Bewegung —
   und endet mit dem allgemeinen Auftrag: «Erkunde diese Zusammenhänge in der nachfolgenden
   Animation und löse die Aufgaben.» Der erste Clip eines Themas führt die Grundform ein
   (hier: Normalparabel über die Wertetabelle).
2. **② Tüfteln.** Die Simulation (§8) trägt ihre Aufgaben **selbst**. Reihenfolge: zuerst
   **Erkunden** (frei an allen Reglern ziehen), dann **konkrete Funktionen zum Nachbauen** —
   nicht die Beispiele aus dem Clip —, dann Zielspiele. Hilfslinien (gestrichelte
   Bezugskurven) lassen sich in jeder Animation, die welche hat, mit einem Schalter aus- und einblenden
   (`<label class="hilfs-schalter">` in der Figur, Klasse `hilfslinie` am Element). Technik: eine Aufgabenleiste
   (`.leiste`) über dem Bild zeigt eine Aufgabe nach der anderen, setzt ✓, sobald der Zustand
   stimmt, und bietet «Nächste ▶» bzw. «überspringen». **Kein Text links daneben** — lange
   Aufträge schrecken ab. Eine Aufgabe = ein Satz. Zielspiele («Triff die grüne Parabel»)
   gehören als letzte Aufgaben dazu.
3. **③ Kontrollfragen.** Ein zweiter Clip mit **neuen** Beispielen — ohne Einleitungsszene, er
   beginnt direkt mit Frage 1 — hält an und fragt
   (Knöpfe oder Tippen ins Bild). Richtig → kurzes ✓, der Clip rollt sofort weiter; falsch →
   Erklärung (vorgelesen) und «Weiter». Danach **Festhalten**: ein Merkkasten (Definition im
   Wortlaut der Themenseite, kurz) und der Häufige Fehler in einem Satz.
4. **④ Üben mit Rückmeldung.** Zwei bis drei `.uebung`-Kästen (§9).
5. **⑤ Aufgaben mit Lösungen.** Drei bis vier Aufgaben auf Papier, Lösung aufklappbar.

**Text aufs Nötigste.** Clip-Karten nur mit Titel und Dauer (keine Unterzeile). Lernziel ein Satz, keine Einleitungsabsätze, keine Hinweise, die der
Clip schon gibt; «Mehr dazu» als eine Zeile mit Link.

Am Ende des Leitprogramms: **Gesamttest und Bewertungspaket als PDF** (§9) — kein HTML.

Zeit: 35–45 Minuten je Kapitel (zwei Clips à ~1 min, Tüfteln ~8–10, Übungen ~8, Selbsttest ~15–20)
— ein Kapitel ≈ eine Lektion (§3). Vorbild: 5 Kapitel + Vorwissen + Gesamttest ≈ 235 Minuten,
rund fünf Lektionen plus Gesamttest. Die Zeiten werden geschätzt, nicht aus der Planung übernommen.

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

- **Clips zeigen, sie erzählen nicht nur.** Wo es einen Graphen gibt, steht er im Clip
  (`graf` mit `parabeln`, `geraden`, `kurven`, `punkte`; HOWTO-clips.md). Bewegung
  entsteht aus einer Folge kurzer Szenen mit je einem Zustand und einem Satz — dieselbe
  Parabel an derselben Stelle, Szene für Szene verschoben, die Normalparabel gestrichelt
  als Bezug. Ein Clip, der «die Parabel wandert nach rechts» nur sagt, verfehlt sein Thema.
- **Je Kapitel zwei eigene Clips** (Entscheid 02.10.2026): Einführungsclip und Kontrollclip.
  Theme **`begreifbar-schlicht`** — ohne Häuschenpapier und roten Rand, weil sich Karo und
  Koordinatengitter stören. Notation wie im Leitprogramm (hier \(x_s\), \(y_s\); gesprochen
  «x s», «y s»).
- **Leitprogramm-eigene Clips sind erlaubt**, wenn sie eine Simulation *des
  Leitprogramms* beschreiben (Entscheid 30.09.2026). Dann: `"probe": true` mit
  `_probe`-Begründung (nicht in der Bibliothek, auf keiner Themenseite), Dateiname
  `<lektion>-lp-<name>`, eine eigene Reihe «<Thema> sehen», Startwert und Farben der
  Simulation. Layout, das sich bewährt hat: Bild rechts (`x` 1010, `y` 175, 760 × 760),
  Formeln und Notizen links (`x` 150), `anim: "fade"` am Bild.
  **Werkstatt:** Drehbücher per Skript erzeugen (gleiche Fenster und Farben in allen
  Szenen), zuerst ohne Ton bauen und mit `pruef-clip.mjs` Szene für Szene ansehen
  (Übersichtsbild), dann `build-clip-ton.py` → `build-clips.py`. **Nach der Vertonung
  das Erzeugerskript nicht mehr laufen lassen** — es überschreibt die gemessenen `dauer`;
  späte Layoutkorrekturen direkt im JSON und nur neu bauen.
- **Sonst nur bestehende Clips**, dieselben Dateien wie auf der Themenseite. Keine fast
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
  bei eigenen Clips die Tonlänge aus `build-clip-ton.py` (abgerundet auf Sekunden) —
  nicht aus dem Drehbuch summieren.
- Fehlt für einen Kernschritt ein Clip: melden, nicht ohne Auftrag bauen.

---

## 8 · Erkundungen und Simulationen

**Bei Funktionen ist die eingebettete Simulation (b) der Normalfall** (Fassung 2). Ein
Link in einen zweiten Tab reisst den Faden ab; wer erst suchen muss, wo er ist, erfährt
nichts. Der Link auf die Themenseite bleibt für die Vertiefung.

**Ist das zu nahe an der Themenseite?** Nein, solange die Rollen verschieden sind: Die
Themenseite ist der offene Spielplatz (alle Regler, alles gleichzeitig, kein Auftrag),
das Leitprogramm führt (ein bis drei Regler, eine Frage, Voraussage, Zielspiel, Treffer-
Rückmeldung). Gleich sein müssen Konventionen und Beispiele, nicht die Bedienung. Jede
Simulation trägt im Code einen Satz, worin sie sich von der Themenseiten-Animation
unterscheidet — lässt er sich nicht schreiben, ist sie überflüssig und der Link genügt.

Entscheid pro Kapitel:

**a) Die Animation der Themenseite passt genau so → Erkundungsauftrag, keine Code-Kopie.**
Kasten «🔍 Erkunden» mit Link auf den Anker (`../grundlagen/<seite>.html#anim-…`, neuer
Tab) und einem **konkreten Auftrag**: was einstellen, was beobachten, was notieren. Die
Frage kommt im Selbsttest wieder. Danach darf der passende `*-anim-*`-Clip folgen.
Höchstens eine Erkundung pro Kapitel.

**b) Geführte Variante** (ein bis drei Regler, eine Aussage, eingebettet) → kleine
SVG-Simulation. Bewährte Muster: Regler + Bezugskurve (gestrichelt) · Zielspiel mit
Treffer-Rückmeldung · Knöpfe, die je ein Merkmal hervorheben · fester Punkt, der
«eingefangen» werden muss · Spiegelpunkt, der eine Symmetrie verrät. Verbindlich:
- Achsen, Variablennamen, Einheiten, Konstanten, **Reglerfarben** (`akz-blau/orange/
  gruen`) identisch zur Themenseiten-Animation
- **Startwert = Beispiel im Text bzw. Clip** desselben Kapitels
- Merksatz in der Bildlegende gleichlautend wie in der «Erkenntnis» der Themenseite
- der Unterschied zur Themenseiten-Animation als Ein-Satz-Kommentar im Code
- Reglerenden und Sichtfenster vorab mit `python3` durchrechnen (bleibt der Scheitel
  im Bild? wo stehen Beschriftungen?)
- trägt ihre Aufträge selbst: Aufgabenleiste `.leiste` mit `Leiste(fig, aufgaben, sim)` —
  je Aufgabe ein Satz (`text`), eine Prüfbedingung auf den Zustand (`ok`) und optional
  `setup` (Ziel einblenden, Modus wechseln); ✓ erscheint von selbst (§4)
- Werte im Text mit Dezimalpunkt und echtem Minus, gerundete mit «≈»

**c) Reine Rechentechnik → keine Animation.** Nur, wo sich wirklich nichts zeigen lässt.

---

## 9 · Selbsttests und Gesamttest

- **Vortest** prüft nur Voraussetzungen, 8–13 Punkte, mit Verweis bei Lücken.
- **Selbsttest je Kapitel**, 7–16 Punkte, 3–6 Aufgaben à 2–5 Punkte. Mischung:
  Rechnen · Erkennen/Entscheiden · Begründen (mindestens eine «Warum»-Frage).
- **Üben mit Rückmeldung vor dem Selbsttest** (Prototyp 02.10.2026, Kapitel 1 und 3 in
  `quadratische-funktionen.html`): `<div class="uebung" data-typ="…">` — jede Aufgabe
  würfelt neue Zahlen, die Eingabe wird im Browser geprüft (echtes Minus, `0.5`, `1/2`;
  Komma wird verstanden, aber angemerkt), und **jedes bekannte Fehlermuster hat eine eigene
  Rückmeldung** (Vorzeichen in der Klammer, \(c\) statt \(v\), vertauschte Koordinaten,
  Minus in \(-\frac{b}{2a}\) vergessen). Die Lösung erscheint erst nach dem zweiten
  Fehlversuch. Zähler «auf Anhieb richtig in Folge»; nichts wird gespeichert. Neue
  Aufgabentypen stehen als Objekt in `TYPEN` (Felder, Eingabemuster, `neu`, `pruefen`,
  `loesung`). Der Selbsttest mit Papier bleibt danach — er prüft das Aufschreiben.
- **Clips, die fragen**: Wo ein eigener Clip eine Voraussage zulässt, hält er an und
  fragt (HOWTO-clips, «Fragen im Clip»).
- **Mindestens eine Aufgabe am Graphen je Kapitel**, wo es einen gibt: zuordnen
  (Graph ↔ Gleichung), ablesen (Gleichung aus dem Graphen), skizzieren, am Bild
  entscheiden (Vorzeichen von \(D\)). Minigrafen als `<svg class="mini" data-f="a,xs,ys"
  data-fenster="…" data-punkte="…">`, gezeichnet vom Seitenskript — Punkte auf
  Gitterpunkte legen, sonst ist nichts ablesbar. Eine Aufgabe nimmt die Voraussage aus
  ① wieder auf.
- **Kein Selbsttest wiederholt ein Beispiel** (gleicher Typ, andere Zahlen), **kein
  Gesamttest einen Selbsttest.**
- **Jedes Kapitelziel wird geprüft; nichts wird geprüft, was nicht eingeführt ist.**
- **Lösung aufklappbar**, darunter optional eine Zeile `.komm` zur typischen
  Fehlerquelle.
- **Gesamttest und Bewertungspaket nur als PDF aus LaTeX** (Entscheid 02.10.2026, keine
  HTML-Ansicht). Quellen `downloads/leitprogramme/<name>/{gesamttest,bewertungspaket}.tex`,
  gemeinsame Gestaltung `downloads/leitprogramme/lp-druck.sty` (pdfLaTeX, Palatino über
  `mathpazo`, Graphen mit pgfplots). Bauen: `python3 scripts/build-lp-pdf.py [filter]` —
  übersetzt in einem temporären Ordner und legt nur das PDF neben die Quelle. Im Leitprogramm
  steht nur ein Dreischritt mit den beiden Downloads und die Selbsteinschätzung.
  - *Gesamttest-Blatt:* Feld «Code (kein Name)», Anleitung mit Zeit und Hilfsmitteln je Teil,
    Schreibflächen, Hinweis auf das Bewertungspaket.
  - *Bewertungspaket:* (1) So gehst du vor — erst lösen, fotografieren ohne Namen; ob und
    welche KI, entscheiden die Lernenden **selbst und in eigener Verantwortung** nach dem, was
    ihnen aufgrund von Alter und persönlicher Situation erlaubt ist (Altersgrenzen,
    Nutzungsbedingungen, allenfalls Einverständnis der Eltern) — die Seite ist frei
    zugänglich, nicht an eine Schule gebunden; ohne KI Selbstbewertung nach dem Raster;
    Lesung der KI prüfen; (2) **Auftrag an die KI**
    zum Kopieren — erst abschreiben, was sie liest, `[unsicher]` statt raten, Punkte nach
    Raster, Folgefehler nur einmal abziehen, andere Wege voll, jeden Abzug begründen,
    Musterlösung nicht abschreiben, Tabelle und Rückverweis aufs Kapitel, keine Note;
    (3) **Musterlösung und Punkteraster** je Aufgabe (Teilschritt · Punkt · Lösung) mit
    typischen Fehlern und Abzug; (4) Selbsteinschätzung.
  - Ganze Punkte je Teilschritt — halbe Punkte machen die KI-Bewertung unzuverlässig.
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
| Koordinatensysteme | Achsen mit **Pfeil in positiver Richtung** und Namen am Pfeil (\(x\), \(y\)); bei Anwendungen **Grösse und Einheit** («x [m]», «h [m]», «A [m²]»). Gilt für Simulationen, Minigrafen, Übungsbilder, Clips (`pfeile`, `xname`, `yname`) und PDFs (pgfplots `axis lines=middle`) |
| Scheitel | im Leitprogramm \(S(x_s \mid y_s)\), \(f(x) = a(x - x_s)^2 + y_s\) (Entscheid 02.10.2026); einmal vermerken, dass die Themenseite \(u, v\) schreibt |
| Fachbegriffe | **der Begriff aus den RLP-Kompetenzen** (z. B. Grund-, Scheitel-, Produktform); weicht die Themenseite oder ein Clip ab, deren Namen einmal in Klammern nennen (z. B. «Produktform (Linearfaktorform)»). Die Synonyme stehen auf der Themenseite beim Begriff |
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

**Unverlinkt veröffentlichen** (Erprobung, Übungsprüfung per Link): keine Karte, kein
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
