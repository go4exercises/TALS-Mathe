# TALS-Mathematik · Styleguide

**Version 1.0 · Stand: Mai 2026**

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
9. Downloads              — Handout, Aufgabenserie, TesteDichSelbst, Ankideck, Formelauszug
10. Externe Ressourcen    — Videos, Aufgabensammlungen
```

Das Schema ist **didaktisch begründet**:
- Erst der Anker ins Anwendungswissen, dann die Abstraktion (nicht umgekehrt).
- Drei Darstellungen früh verknüpfen — das verhindert das „Symbol-Schubsen" ohne Verständnis.
- Spezialfälle sichtbar machen, bevor sie in Aufgaben auftauchen.
- Aufgabentypen steigern Selbstständigkeit.
- Downloads kommen **vor** den externen Links — denn das eigene Material ist primär.

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

---

## 6. Datei-Naming und Struktur

```
TALS-Mathe/
├── index.html                              ← Übersichtsseite
├── style.css                               ← gemeinsames Stylesheet
├── nav.js                                  ← Navigation (sticky header + breadcrumb + ToC)
├── README.md
├── STYLEGUIDE.md                           ← diese Datei
├── TEMPLATE.html                           ← Vorlage für neue Themen
├── grundlagen/
│   ├── g1-arithmetik-algebra.html
│   ├── g2-gleichungen.html
│   ├── g3-1-funktionen-grundlagen.html
│   ├── g3-2-lineare-funktionen.html        ← Referenz-Implementierung
│   ├── g3-3-quadratische-funktionen.html
│   ├── g3-4-…
│   ├── g4-datenanalyse.html
│   └── g5-geometrie.html
├── schwerpunkt/
│   ├── s1-arithmetik.html
│   ├── s2-gleichungen.html
│   ├── s3-1-funktionen-grundlagen.html
│   ├── s3-2-polynome.html
│   ├── …
│   └── s4-geometrie.html
└── downloads/
    ├── README.md
    ├── grundlagen/
    │   ├── g3-2-lineare-funktionen/
    │   │   ├── handout.pdf
    │   │   ├── aufgabenserie.pdf
    │   │   ├── teste-dich-selbst.pdf
    │   │   ├── ankideck.apkg
    │   │   └── formelauszug.pdf
    │   └── …
    └── schwerpunkt/
        └── …
```

**Naming-Regeln:**
- Bereichs-Präfix: `g` für Grundlagen, `s` für Schwerpunkt
- Lerngebiet-Nummer: `g3-2` = Grundlagen, Lerngebiet 3 (Funktionen), Thema 2 (Lineare)
- Dateinamen kleingeschrieben, mit Bindestrichen, ohne Umlaute (`-funktionen.html`, nicht `_Funktionen.html`)

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
- [ ] Downloads-Sektion vor externen Ressourcen
- [ ] Alle 5 Standard-Downloads verlinkt
- [ ] Footer korrekt: „Grundlagen <Thema>" oder „Schwerpunkt <Thema>"
- [ ] `nav.js` korrekt eingebunden mit prev/next
- [ ] ToC funktioniert (alle h2 haben `id`)

**Technisch**
- [ ] MathJax lädt
- [ ] Responsiv auf Mobile (≤500 px Viewport)
- [ ] Alle interaktiven Widgets funktionieren
- [ ] Lösungen zugeklappt by default

---

*Pflege dieses Dokuments: bei Konvention-Erweiterungen Version hochzählen, Datum aktualisieren.*
