# Technischer Konsistenz-Bericht — TALS Mathe

> **Hinweis (Juli 2026):** Momentaufnahme vom 24.06.2026. Punkt C1 ist inzwischen erledigt — alle 13 Schwerpunkt-Teilgebiete wurden bis Juli 2026 vollständig ausgebaut (CHANGELOG [71]–[81]); es gibt keine Stub-Seiten mehr.

**Datum:** 2026-06-24 · **Umfang:** `grundlagen/*.html` (23), `schwerpunkt/*.html` (13),
geteilte Assets (`style.css`, `mathlib.js`, `nav.js`, `minicheck.js`, `anim-hinweise.js`),
`TEMPLATE.html`, Nachschlag-Seiten. **Methode:** Pre-Flight (alle Seiten) + vier
read-only Muster-Audits, alle Befunde danach manuell an den Dateien verifiziert.

## Gesamtbild

Das Projekt ist technisch **sauber und überwiegend konsistent**. Der Pre-Flight ist
vollständig grün (5698 MathJax-Ausdrücke / 0 Render-Fehler, JS-Runtime ok, keine
doppelten IDs, kein `ß`, kein Dezimalkomma in Body-Math, keine Phantom-Klassen, keine
Identifier-Kollisionen). Die Abweichungen sind eng begrenzt: **im Kern zwei Seiten
(`g1-3`, `g1-4`) aus einer älteren Template-Revision** plus einige kosmetische Punkte.

---

## A · Zu behebende Inkonsistenzen

### A1 — `g1-3` und `g1-4`: alte Template-Revision  ⚠ (Haupt-Befund)
Beide Seiten weichen gemeinsam in drei Punkten vom Repo-Standard ab:

1. **Seiten-Skripte im `<head>` statt am Body-Ende.** `nav.js`, `mathlib.js`,
   `minicheck.js`, `anim-hinweise.js` stehen in Zeile 17–20 (`<head>`); alle anderen
   34 Seiten laden sie vor `</body>`. Funktioniert (Pre-Flight grün), widerspricht aber
   `TEMPLATE.html` und `HOWTO-neue-themenseite.md` und blockiert das Parsing.
2. **`svg.scale: 1.0` statt `1.05`** (als einzige zwei Seiten) → Formeln rendern auf
   diesen Seiten **sichtbar kleiner** als auf allen anderen.
3. **Reduzierter MathJax-Block:** es fehlen `tex.packages:{'[+]':['boldsymbol']}` und
   `loader:{ load:['[tex]/boldsymbol'] }`. Aktuell harmlos (keine Seite nutzt
   `\boldsymbol`), aber inkonsistent und fragil, falls `\boldsymbol` je gebraucht wird.
   Zusätzlich abweichendes Format (Leerzeichen nach Doppelpunkten).

→ **Massnahme:** Den `<head>`- und Skript-Block beider Seiten 1:1 an eine
Standard-Nachbarseite (z. B. `g1-2`) angleichen. Grösster Konsistenzgewinn bei
kleinstem Risiko.

### A2 — MathJax-Package-Deklarationen vs. tatsächliche Nutzung  ◐
- `g1-1` deklariert das Paket `color`, `g3-3` deklariert `bbox`+`color` — **keines davon
  wird auf der jeweiligen Seite verwendet** (tote Deklaration).
- `g1-2` **nutzt** `\textcolor` (2×), **deklariert `color` aber nicht** — funktioniert nur,
  weil MathJax `color` bei erster Verwendung automatisch nachlädt (Autoload).

→ **Massnahme:** Vereinheitlichen — deklarieren, was genutzt wird; Ungenutztes entfernen.
Entweder konsequent auf Autoload verlassen (dann `color`/`bbox` aus `g1-1`/`g3-3`
streichen) **oder** überall explizit deklarieren (dann `color` in `g1-2` ergänzen).
Empfehlung: ungenutzte Deklarationen streichen, Autoload nutzen.

### A3 — `g4-0`: Titel-Wortlaut Kopf ≠ `<title>`  🟡
`<title>` = „4.0 Praxisbeispiel BM2-Klasse — TALS Mathematik", `<h1>` = „4.0
Praxisbeispiel — Datenerhebung in einer BM2-Klasse". Kleinere Wortlaut-Differenz; auf
einen einheitlichen Wortlaut bringen.

### A4 — Animations-Titel: drei Element-Varianten  ◐ (offene Entscheidung)
Titel von Animationen/Widgets sind mal `<h3>`, mal `<div class="anim-titel">`, vereinzelt
`<p>` — teils **innerhalb derselben Seite gemischt** (z. B. `g1-1`, `g1-3`, `g5-2a`).
Neuere Geometrie-Seiten (`g5-2*`) nutzen `.anim-titel`, ältere `<h3>`.

→ **Massnahme:** Wartet auf deine Entscheidung (kompakter `.anim-titel`-Label-Look
beibehalten **oder** alles auf den Serif-`<h3>`-Look vereinheitlichen). Danach in einem
Durchgang angleichen. *(Dieser Punkt stammt aus der vorherigen Diskussion.)*

---

## B · Beobachtungen ohne Handlungsdruck

- **B1 — Event-Handler-Stil gemischt.** In `grundlagen/` Mix aus inline `onclick`
  (~287) und `addEventListener` (~255); geteilte Module rein `addEventListener`. Kein
  Regelverstoss, pragmatisch (kleine Callbacks inline, komplexe Logik per Listener).
  Eine Vereinheitlichung ist optional und nicht dringend.
- **B2 — Fehlende Sektions-`id`s.** Einzelne Seiten (`g1-4`, `g5-2d`, `g5-5`) haben eine
  Definitions-Sektion ohne `id="definition"`. Nur relevant für Deep-Links/ToC-Anker.

---

## C · Projektstatus (kein Konsistenz-Bug, nur zur Einordnung)

- **C1 — Alle 13 Schwerpunkt-Seiten sind Stubs** („In Vorbereitung", Stand Mai 2026):
  je 2–7 MathJax-Ausdrücke, keine `block-*`-Inhalte, keine Aufgaben A1–A6, **keine
  Lernziele**. Das ist gewollt (Gerüst steht, Inhalt folgt) — die fehlenden Lernziele
  und Aufgaben sind also **Inhaltsarbeit**, kein technischer Defekt.
- **C2 — `g4-0` hat bewusst 0 klassische Aufgaben** (interaktives Praxisbeispiel mit
  Daten-Dashboard statt A1–A6).

---

## D · Verifiziert konsistent (Stärken)

- Pre-Flight komplett grün über alle 36 Seiten.
- **Notation:** kein `ß`; keine `$…$`-Delimiter; Dezimalpunkt durchgängig (auch in
  JS-Ausgaben); `\(…\)`/`\[…\]` überall identisch konfiguriert.
- **Navigation:** `nav.js`-IDs ↔ Dateien 36:36 exakt; prev/next-Kette lückenlos und
  bidirektional; keine toten Links.
- **Markup:** `.anim-hinweis` immer als `links`+`rechts`-Paar und immer in
  `.widget-titelzeile`; alle `block-*`-Klassen in `style.css` definiert (keine
  Phantome); Aufgaben-Markup (`aufg-nr-tag`/`aufg-titel-text`/`aufg-liste`) einheitlich.
- **Assets:** jede Seite bindet die für ihre Features nötigen Skripte ein; `mathlib.js`
  überall vorhanden; Schwerpunkt-Seiten in MathJax-Konfig 100 % identisch.

---

## TODO

Priorisiert. Nach jeder Code-Änderung: Pre-Flight, dann Commit (siehe CLAUDE.md).

- [ ] **A1** `g1-3` + `g1-4` an Standard-Template angleichen: Skripte ans Body-Ende,
      `svg.scale:1.05`, `tex.packages` + `loader` (boldsymbol) ergänzen, Konfig-Format
      angleichen. *(hoher Nutzen, geringes Risiko)*
- [ ] **A2** MathJax-Packages harmonisieren: ungenutztes `color`/`bbox` aus `g1-1`/`g3-3`
      entfernen (Autoload genügt); `g1-2` (nutzt `\textcolor`) belassen oder explizit
      `color` ergänzen — eine Linie für alle wählen.
- [ ] **A3** `g4-0`: Wortlaut von `<title>` und `<h1>` vereinheitlichen.
- [ ] **A4** Animations-Titel vereinheitlichen — **erst Look-Entscheidung** (kompakter
      `.anim-titel` vs. Serif-`<h3>`), dann projektweit angleichen.
- [ ] **B1** *(optional)* Event-Handler-Stil in `grundlagen/` schrittweise vereinheitlichen.
- [ ] **B2** *(optional)* Fehlende `id="definition"` in `g1-4`, `g5-2d`, `g5-5` ergänzen.
- [ ] **C1** *(Inhaltsarbeit, separat)* Schwerpunkt-Seiten ausarbeiten: Lernziele +
      Aufgaben A1–A6 je Seite (13 Stubs).
</content>
</invoke>
