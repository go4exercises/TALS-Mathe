# TALS-Mathematik · Styleguide

**Version 1.1 · Stand: Mai 2026**

Dieser Styleguide ist die verbindliche Referenz für alle Themenseiten des Lehrmittels „TALS-Mathematik". Er sichert Konsistenz in Notation, Aufbau, Sprache und visuellem Design — kapitelübergreifend und chatübergreifend.

> **Verwendungshinweis:** Diese Datei liegt im Project-Knowledge des Claude-Projekts. In jedem neuen Chat wird sie automatisch berücksichtigt. Wer eine neue Themenseite baut, liest zuerst hier nach, bevor neue Konventionen erfunden werden.

---

## 1. Verbindliche Quellen

| Bereich | Quelle |
|---|---|
| Notation, Symbole, Begriffe | *Formeln, Tabellen, Begriffe* (Orell Füssli), kurz **FTB** |
| Lehrziele, Kompetenzen | **RLP 2030** (Rahmenlehrplan vom 13. Juni 2025, in Kraft ab 2030) |
| Hilfsmittel-Status | **Promath (SBFI)** — offizielle Formelsammlung der BM |

**Sprachregelung:**
- *„RLP 2030"* bezeichnet das aktuell gültige Rahmenlehrplan-Dokument (datiert 2025, ab 2030 für alle Klassen verbindlich). Zitate immer „RLP 2030", nie „RLP 2025" oder „RLP-BM 2026".
- *„Berufsmaturität Technik, Architektur, Life Sciences"* — Vollform; Kürzel **TALS** nur in Logos/Pills.
- *„Grundlagenfach"* / *„Schwerpunktfach"* — keine Abkürzungen wie „GLF" / „SPF".

---

## 2. Mathematische Notation (FTB-konform)

### 2.1 Multiplikation

- **Mit Multiplikationspunkt** (`·`) zwischen Zahl und Variable, wenn die Variable explizit gemeint ist:
  `f(x) = 2·x + 5` ✓
- **Ohne Punkt** in zusammengesetzten Termen ist toleriert, aber in Live-Anzeigen (interaktive Widgets) immer mit Punkt zur Eindeutigkeit.
- **In LaTeX:** `\cdot` für den Multiplikationspunkt; `*` ist verboten.
- **LaTeX-Display-Konvention:** Im LaTeX-Display ohne Punkt schreiben (z.B. `f(x) = 3x - 1`), weil MathJax `3x` ohnehin satztechnisch als Multiplikation rendert. Nur dort `\cdot` setzen, wo der Punkt didaktisch nötig ist (z.B. `m_1 \cdot m_2 = -1` bei senkrechten Geraden, oder bei Zahl-mal-Zahl wie `2 \cdot 3 = 6`). In Live-JS-Anzeigen dagegen IMMER mit `·` (siehe oben).

### 2.2 Funktionsschreibweise

```
f(x) = m·x + b           ← Funktionsterm
f : ℝ → ℝ, x ↦ m·x + b   ← Funktion mit Definitions-/Wertebereich
```

In LaTeX:
```latex
f : \mathbb{R} \longrightarrow \mathbb{R}, \quad x \longmapsto m \cdot x + b
```

### 2.3 Variablen und Konstanten

| Was | Schreibweise | Beispiel |
|---|---|---|
| Variablen | kursiv | $x$, $y$, $t$ |
| Funktionen | kursiv | $f$, $g$, $h$ |
| Punkte | grosser Buchstabe, kursiv, mit Koordinaten | $P(2 \mid 3)$ |
| Vektoren | mit Pfeil | $\vec{a}$ |
| Mengen | Doppelstrich | $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}$ |
| Zahlen | aufrecht (kein Kursiv) | 2, 5, 0.5 |

### 2.4 Punkt-Komma-Notation

- Koordinatenpaar: `P(2 | 3)` (mit senkrechtem Strich, **nicht** Komma) — FTB-Standard
- Zahlen: Dezimal**punkt** (Schweizer Schulkonvention), nicht Dezimalkomma: `0.5`, nicht `0,5`

### 2.5 Begriffe (verbindlich)

| Korrekt | Falsch |
|---|---|
| Graph | Graf |
| Gerade | Linie (im math. Sinn) |
| Steigung | Anstieg |
| Achsenabschnitt | Y-Achsenschnittpunkt |
| Nullstelle | x-Wert wo y=0 |
| kartesisches Koordinatensystem | XY-System |

### 2.6 LaTeX-Konventionen

- **Inline-Formeln:** `\(...\)` — z.B. `\(f(x) = m \cdot x + b\)`
- **Display-Formeln:** `\[...\]` — eigene Zeile
- **Fraktionen:** `\frac{Zähler}{Nenner}`, in Tabellen `\displaystyle\frac{...}{...}` für volle Höhe
- **Bedingung am Ende:** `\quad (m \neq 0)`
- **Symbole:** `\parallel`, `\perp`, `\Longrightarrow` (kein einfacher Pfeil)
- **Mengen:** `\mathbb{R}`, `\mathbb{N}`

---

## 3. Achsenskalierung (verbindlich)

> **Diese Regel kommt direkt aus den Projekt-Instructions und gilt unbedingt.**

### 3.1 Reine Mathematik-Aufgaben → 1:1
Alle Diagramme, in denen $x$ und $y$ abstrakte Variablen sind (Beispiele: „Zeichne $f(x) = 2x − 3$"), müssen **kartesisch quadratisch** dargestellt werden — eine Einheit auf der x-Achse hat dieselbe Pixellänge wie eine Einheit auf der y-Achse.

**Code-Konvention:** im Canvas-Helper das Argument `square: true` setzen:
```js
const {ctx, W, H} = initCanvas('canvas-id', 280, true);  // square = true
```

### 3.2 Anwendungsaufgaben → aufgabenbezogen
Wenn $x$ und $y$ unterschiedliche physikalische Grössen mit unterschiedlichen Einheiten sind (Kilogramm und Franken, Sekunden und Meter), wird die Skalierung **aufgabenbezogen** gewählt — also so, dass die relevante Information klar lesbar ist. **Keine 1:1-Forderung.**

**Beispiel — Kartoffeln (Kostenfunktion):**
- x-Achse: 0 bis 15 kg
- y-Achse: 0 bis 35 CHF
- Achsenbeschriftung mit Einheit: `x [kg]`, `K [CHF]` (siehe 3.3)

### 3.3 Achsenbeschriftung mit Einheit

Bei Anwendungsaufgaben **immer** Achsen mit Grösse und Einheit beschriften, in eckigen Klammern:
- `x [kg]`, `K [CHF]`, `t [s]`, `s [m]`, `T [°C]`, `F [°F]` …

Bei reiner Mathematik genügt `x` und `y` ohne Einheit.

---

## 4. Didaktischer Aufbau (Master-Schema)

Jede Themenseite folgt diesem Schema in genau dieser Reihenfolge:

```
1. Titel + RLP-Header (Kompetenzen-Liste mit „mit/ohne Hilfsmittel"-Hinweis)
2. Einstieg               — konkretes Anwendungsbeispiel, motivierend, erlebbar
3. Definition             — formal, sauber, FTB-konform
4. Verknüpfung der Darstellungen — Gleichung ↔ Tabelle ↔ Graph (interaktiv)
5. Spezialfälle / Typen   — Übersichtstabelle + Klick-Visualisierung
6. Weitere Theorie        — z.B. Aufstellen der Gleichung, Schnittpunkte, …
7. Aufgaben               — A1 → A6, mit zunehmender Selbstständigkeit:
      • A1: Erkennen / Ablesen
      • A2: Konstruieren / Zeichnen
      • A3: Rechnen (mehrere Teilaufgaben)
      • A4–A6: Anwendung in Realsituation
8. Zusammenfassung        — kompakte Tabelle, Merksatz
9. Zusatzmaterial         — fünf Einträge in fester Reihenfolge:
      • Handout (HTML-Druckseite, neuer Tab) — Theorie ohne Beispiele und ohne Aufgaben
      • Formelauszug (HTML-Druckseite, neuer Tab) — kompakte Formelsammlung, FTB-konform
      • Anki-Deck (Download `.apkg`)
      • Teste dich selbst (HTML-Druckseite, neuer Tab) — Grundlagenaufgaben mit Lösungen
      • Aufgabenserie (HTML-Druckseite, neuer Tab) — Anwendungsaufgaben mit Lösungen
10. Externe Ressourcen    — Videos, Aufgabensammlungen
```

Das Schema ist **didaktisch begründet**:
- Erst der Anker ins Anwendungswissen, dann die Abstraktion (nicht umgekehrt).
- Drei Darstellungen früh verknüpfen — das verhindert das „Symbol-Schubsen" ohne Verständnis.
- Spezialfälle sichtbar machen, bevor sie in Aufgaben auftauchen.
- Aufgabentypen steigern Selbstständigkeit.
- Zusatzmaterial kommt **vor** den externen Links — denn das eigene Material ist primär.

**Trennung Handout ↔ Aufgaben:** Das Handout enthält nur Theorie (Definitionen, Sätze, Tabellen, Übersichts-SVGs wie eine Geradenschar). **Beispiele** stehen in der Themenseite und in „Teste dich selbst", **Aufgaben** in „Teste dich selbst" (rein-mathematisch) und in der „Aufgabenserie" (Anwendungen). So bleibt das Handout als knapper Theorie-Auszug zum Mitnehmen brauchbar.

**Druckseiten-Anforderungen:** Jede HTML-Druckseite hat oben einen sticky „Seite drucken"-Knopf (`window.print()`) und einen Rück-Link zur Themenseite. Druck-CSS (`@page A4 portrait`, 14 mm Rand, `@media print`) sorgt für saubere Ausnutzung und gute Seitenwechsel. Druckseiten öffnen von der Themenseite immer in einem neuen Tab (`target="_blank" rel="noopener"`).

---

## 5. Visuelles Design

### 5.1 Farbsemantik (verbindlich, in `style.css` zentral definiert)

| Farbe | Bedeutung | Verwendung |
|---|---|---|
| 🔵 Blau | Definition, Theorie | `block-def`, „📘"-Blöcke |
| 🟢 Grün | Beispiel, Lösung | `block-bsp`, „🟢"-Blöcke |
| 🟠 Orange | Aufgabe, Übung | `block-aufg`, „🟠"-Blöcke |
| 🔴 Rot | Häufiger Fehler, Warnung | `block-fehler`, „⚠"-Blöcke |
| 🟣 Violett | Beweis, Herleitung | `block-beweis`, „🔷"-Blöcke |

Die Farben sind kapitelübergreifend identisch — das schafft ein konsistentes mentales Modell beim Schüler.

### 5.2 Bereichsfarben

- **Grundlagenfach:** Blau (`--blau`, `--blau-hell`)
- **Schwerpunktfach:** Violett (`--lila`, `--lila-hell`)

### 5.3 Schriften

- **Serif** (`Source Serif 4`): Überschriften, Titel
- **Sans** (`Source Sans 3`): Fliesstext
- **Mono** (`JetBrains Mono`): Code, Formeln in Live-Anzeigen, Slider-Werte, Chip-Labels

### 5.4 Zusatzmaterial- und Ressourcen-Sektion (zentrale Klassen)

Die zwei Schluss-Sektionen jeder Themenseite (Schritt 9 und 10 im Master-Schema) verwenden ausschliesslich Klassen, die zentral in `style.css` definiert sind. **Lokale Style-Definitionen dieser Klassen sind verboten** — Konsistenz über alle Themen ist Pflicht und das Erscheinungsbild muss exakt mit der Referenz übereinstimmen.

**Klassen-Übersicht:**

| Klasse | Verwendung |
|---|---|
| `.dl-grid` | Container für die 5 Download-Kacheln (Auto-Wrap-Grid, min. 200 px) |
| `.dl` | Einzelne Download-Kachel — weisser Hintergrund, blauer Linksbalken, Hover-Lift |
| `.dl-ic`, `.dl-t`, `.dl-s`, `.dl-fmt` | Icon, Titel, Untertitel, Format-Label (z.B. „Druckseite", „APKG") |
| `.links-grid` | Container für externe Link-Kacheln (zweispaltig, einspaltig <520 px) |
| `.lk` | Externe Link-Kachel — ohne blauen Linksbalken, roter Hover-Rand |
| `.lk.aufg` | Variante für Aufgabensammlungen — oranger Hover-Rand statt rot |
| `.lk-ic`, `.lk-t`, `.lk-s` | Icon, Titel, Untertitel |
| `.ressourcen-subtitel` | Mono-Caps-Label für Untergruppen wie „🎬 ERKLÄRVIDEOS" |

**Markup-Vorgaben:**

```html
<h2 id="downloads">Zusatzmaterial</h2>
<p>Materialien zum Mitnehmen, Üben und Wiederholen. Druckseiten öffnen in neuem Tab.</p>
<div class="dl-grid">
  <a href="../downloads/<bereich>/<datei-id>/handout.html" target="_blank" rel="noopener" class="dl">
    <span class="dl-ic">📄</span>
    <div><div class="dl-t">Handout</div><div class="dl-s">Theorie-Zusammenfassung</div><div class="dl-fmt">Druckseite</div></div>
  </a>
  <!-- weitere Kacheln in fester Reihenfolge: Formelauszug, Anki-Deck, Teste dich selbst, Aufgabenserie -->
</div>

<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>
<div class="ressourcen-subtitel">🎬 Erklärvideos</div>
<div class="links-grid">
  <a href="https://..." target="_blank" rel="noopener" class="lk">
    <span class="lk-ic">▶️</span>
    <div><div class="lk-t">Titel</div><div class="lk-s">Kanal · Hinweis</div></div>
  </a>
</div>
<div class="ressourcen-subtitel">📝 Aufgabensammlungen</div>
<div class="links-grid">
  <a href="https://..." target="_blank" rel="noopener" class="lk aufg">
    <span class="lk-ic">📝</span>
    <div><div class="lk-t">Quelle — Thema</div><div class="lk-s">Beschreibung</div></div>
  </a>
</div>
```

**Reihenfolge der Download-Kacheln** (verbindlich, damit das visuelle Layout zwischen den Themenseiten austauschbar bleibt): Handout · Formelauszug · Anki-Deck · Teste dich selbst · Aufgabenserie. Die Druckseiten-Kacheln haben das Format-Label „Druckseite", das Anki-Deck „APKG".

---

## 6. Datei-Naming und Struktur

```
TALS-Mathe/
├── index.html                              ← Übersichtsseite
├── style.css                               ← gemeinsames Stylesheet
├── nav.js                                  ← Navigation (sticky header + breadcrumb + ToC)
├── mathlib.js                              ← Canvas-Helper, Formatter, Parser, Lösungs-Toggle
├── README.md
├── STYLEGUIDE.md                           ← diese Datei
├── TEMPLATE.html                           ← Vorlage für neue Themen (nutzt ../-Pfade)
├── grundlagen/                             ← 18 Themenseiten
│   ├── g1-1-grundlagen.html
│   ├── g1-2-zahlen-grundoperationen.html
│   ├── g1-3-algebraische-terme.html
│   ├── g1-4-zehnerpotenzen-quadratwurzeln.html
│   ├── g2-1-grundlagen.html
│   ├── g2-2-lineare-quadratische-gleichungen.html
│   ├── g2-3-lineare-gleichungssysteme.html
│   ├── g3-1-grundlagen.html
│   ├── g3-2-lineare-funktionen.html        ← Referenz-Implementierung
│   ├── g3-3-quadratische-funktionen.html
│   ├── g4-1-grundlagen.html
│   ├── g4-2-diagramme.html
│   ├── g4-3-masszahlen.html
│   ├── g5-1-grundlagen.html
│   ├── g5-2-planimetrie.html
│   ├── g5-3-trigonometrische-berechnungen.html
│   ├── g5-4-einheitskreis.html
│   └── g5-5-trigonometrische-gleichungen.html
├── schwerpunkt/                            ← 13 Themenseiten
│   ├── s1-1-grundlagen.html
│   ├── s1-2-potenzen.html
│   ├── s1-3-logarithmen.html
│   ├── s2-1-grundlagen.html
│   ├── s2-2-gleichungstypen.html
│   ├── s3-1-grundlagen.html
│   ├── s3-2-potenz-wurzelfunktionen.html
│   ├── s3-3-polynomfunktionen.html
│   ├── s3-4-exponential-logarithmusfunktionen.html
│   ├── s3-5-trigonometrische-funktionen.html
│   ├── s4-1-grundlagen.html
│   ├── s4-2-stereometrie.html
│   └── s4-3-vektorgeometrie.html
└── downloads/
    ├── README.md
    ├── print.css                              ← gemeinsames Druck-Stylesheet (A4)
    ├── diagram.js                             ← SVG-Helper für Achsenkreuze in Druckseiten
    ├── grundlagen/
    │   ├── g3-2-lineare-funktionen/
    │   │   ├── handout.html                   ← Druckseite (Theorie, ohne Beispiele/Aufgaben)
    │   │   ├── formelauszug.html              ← Druckseite (kompakte Formelübersicht)
    │   │   ├── ankideck.apkg                  ← Anki-Karteikarten (Download)
    │   │   ├── teste-dich-selbst.html         ← Druckseite (Grundlagenaufgaben + Lösungen)
    │   │   └── aufgabenserie.html             ← Druckseite (Anwendungsaufgaben + Lösungen)
    │   └── …
    └── schwerpunkt/
        └── …
```

**Naming-Regeln:**
- Bereichs-Präfix: `g` für Grundlagen, `s` für Schwerpunkt
- Lerngebiet-Nummer: `g3-2` = Grundlagen, Lerngebiet 3 (Funktionen), Thema 2 (Lineare)
- Dateinamen kleingeschrieben, mit Bindestrichen, ohne Umlaute (`-funktionen.html`, nicht `_Funktionen.html`)
- **Druckseiten-Dateinamen** sind über alle Themen hinweg identisch: `handout.html`, `formelauszug.html`, `teste-dich-selbst.html`, `aufgabenserie.html` (plus `ankideck.apkg`). Das erleichtert Verlinkung, Kopiervorlagen und Suche.

---

## 7. Footer-Konvention

| Seite | Footer-Inhalt |
|---|---|
| **`index.html`** | Zeile 1: „**TALS Mathematik** — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences"<br>Zeile 2: GitHub Pages-Link |
| **Themenseiten** | Zeile 1: „**TALS Mathematik** — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences"<br>Zeile 2: „<Bereich> <Themenname>" — z.B. „Grundlagen Lineare Funktionen", „Schwerpunkt Logarithmusfunktionen" |

**Format Bereich/Thema:** Ohne Trennzeichen, ohne Kapitelnummer. Nur „Grundlagen" oder „Schwerpunkt", Leerzeichen, Themenname.

---

## 8. Qualitäts-Checkliste vor Veröffentlichung

Bevor eine Themenseite live geht, prüfe:

**Inhalt**
- [ ] Alle RLP-Kompetenzen des Themas abgedeckt
- [ ] „mit/ohne Hilfsmittel"-Hinweise gemäss RLP gesetzt
- [ ] Mindestens ein Anwendungsbeispiel im Einstieg
- [ ] Drei Darstellungen (Gleichung/Tabelle/Graph) verknüpft
- [ ] Spezialfälle visualisiert
- [ ] 6 Aufgaben mit zunehmender Selbstständigkeit
- [ ] Zusammenfassung als kompakte Tabelle

**Notation**
- [ ] Multiplikationspunkt in Live-Anzeigen (`2·x`, nicht `2x`)
- [ ] Punkt-Komma-Notation: `(2 | 3)`, nicht `(2, 3)`
- [ ] Dezimal**punkt**, nicht Komma
- [ ] „Graph" geschrieben, nicht „Graf"
- [ ] LaTeX für alle Formeln (kein Unicode-Improvising)

**Grafik**
- [ ] Reine Mathematik: 1:1-Skalierung (`square: true`)
- [ ] Anwendung: aufgabenbezogene Skalierung
- [ ] Anwendung: Achsenbeschriftung mit Einheit (`x [kg]`)
- [ ] Mathematik: Achsenbeschriftung `x` und `y` ohne Einheit

**Struktur & Konventionen**
- [ ] Zusatzmaterial-Sektion vor externen Ressourcen
- [ ] Alle 5 Einträge in fester Reihenfolge: Handout · Formelauszug · Anki-Deck · Teste dich selbst · Aufgabenserie
- [ ] Druckseiten öffnen in neuem Tab (`target="_blank" rel="noopener"`)
- [ ] Anki-Deck als Download verlinkt (`.apkg`), die anderen vier als HTML-Druckseiten
- [ ] Footer korrekt: „Grundlagen <Thema>" oder „Schwerpunkt <Thema>"
- [ ] `nav.js` korrekt eingebunden mit prev/next
- [ ] ToC funktioniert (alle h2 haben `id`)

**Druckseiten (`downloads/.../*.html`)**
- [ ] Handout enthält ausschliesslich Theorie — keine Beispiele, keine Aufgaben
- [ ] „Seite drucken"-Knopf oben (sticky), Rück-Link zur Themenseite
- [ ] `print.css` und (falls Diagramme) `diagram.js` eingebunden
- [ ] Saubere A4-Seitenwechsel (`page-break-inside: avoid` für Aufgaben/Lösungs-Blöcke)
- [ ] Diagramme: reine Mathematik 1:1, Anwendungen mit Achsenbeschriftung und Einheit

**Technisch**
- [ ] MathJax lädt
- [ ] Responsiv auf Mobile (≤500 px Viewport)
- [ ] Alle interaktiven Widgets funktionieren
- [ ] Lösungen zugeklappt by default

---

*Pflege dieses Dokuments: bei Konvention-Erweiterungen Version hochzählen, Datum aktualisieren.*
