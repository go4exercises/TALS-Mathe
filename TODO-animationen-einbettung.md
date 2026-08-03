# Animations-Einbettung vereinheitlichen — **abgeschlossen (3. August 2026)**

Vereinheitlichung nach STYLEGUIDE §2.10. Vorgeschichte: `.widget`-CSS zentralisiert
(`b427df8`), 26 + 4 + 3 freistehende Animationen umgebaut (`d4846db`, `42f95d8`,
`589d70a`), kaputter Einstieg auf `g3-1` repariert (`a5673ad`).

Dieser Durchgang hat die fünf verbliebenen gemischten Seiten aufgelöst und alle
Animationen dieser Seiten mit dem Hinweispaar (👁 / 💡) versehen.

---

## A · Vereinheitlichung — erledigt

Verfahren wie bei `.velo-box`/`.diag-box` in `589d70a`: Klasse als Namensraum behalten,
ihr die Karten-Optik nehmen, das Ganze in `.widget > .widget-body` wickeln, Titel als
`<h3>` in die `.widget-titelzeile` im `.widget-header`.

Statt der Optik-Rücknahme je Seite steht die Regel jetzt **zentral** in `style.css`:

```css
.widget-body > .anim { background:none; border:0; border-radius:0; padding:0; margin:0; box-shadow:none; }
```

`.anim` behält damit seine 22 Nachfahren-Regeln, verliert aber den Rahmen im Rahmen.

- [x] `g1-2` · `cv-zahlmenge` (`.anim`)
- [x] `g1-2` · `cv-iv` (`.iv-anim`); `.iv-vis` gibt den Rahmen ab und bleibt getöntes
      Innenfeld — dieselbe Form wie `.slider-box` auf `g3-1`
- [x] `g1-3` · `cv-equiv` (`.anim`)
- [x] `g5-5` · `cv-rad` (`.anim`)

**Über den ursprünglichen Plan hinaus — `g1-3` ganz umgestellt.** Die Annahme
«die vier Karten stehen neben `.widget`-Karten» stimmte für `g1-3` nicht: die Seite hatte
**null** Widgets und vier `.anim`-Karten plus eine freistehende `.widget-titelzeile`
(Teilerpaar-Tabelle). Nur `cv-equiv` umzubauen hätte die Seite erst recht gemischt.
Deshalb zusätzlich:

- [x] `g1-3` · «Gleichartige Glieder zusammenfassen» (`.anim`)
- [x] `g1-3` · `cv-binomi` (`.anim`)
- [x] `g1-3` · «Begriffe am Polynom» (`.anim` ohne Titelzeile — Titelzeile und
      Hinweispaar neu)
- [x] `g1-3` · Teilerpaar-Tabelle (freistehende `.widget-titelzeile`, §2.10 «nicht
      zulässig»). `<h3>` neu, der bisherige Fliesstext-Titel ist Untertitel im Kopf.
      Der Behälter `.tp-box` trug nur Karten-Optik und ist ersatzlos weg.

Stand danach: `g1-2`, `g1-3`, `g5-5` haben je **5 Widgets und keine freistehende
`.anim`-Karte** mehr. `g3-1` und `s3-3` bleiben regelkonform gemischt — ihre Grafiken
gehören zu einem `.block` und stehen nach §2.10 zu Recht ohne Rahmen.

**Nicht angefasst:** die 53 `.anim`-Karten der übrigen 8 Seiten. Sie sind in sich stimmig,
und `.anim` bleibt nach §2.10 zulässig — nur für Neues nicht mehr zu verwenden.

## B · Hinweispaare — erledigt

- [x] `g1-3` · `cv-binomi` + `cv-binomi-rechts` — hatten das gemeinsame Paar bereits;
      die Umschaltung über `.bin-canvas-paar` ist die zweite Ansicht eines Widgets
- [x] `g3-1` · `darst-graph` — ein Paar über dem Block `.vier-darstellungen`; der Graph
      ist eine von vier Darstellungen und keine eigenständige Animation
- [x] `g3-1` · vier Quizkarten in `.fq-karte` — **ein** gemeinsames Paar über `#fq`;
      die vier Karten sind eine didaktische Einheit
- [x] `g3-1` · `ach2-canvas` und `schn2-canvas` — teilen nach AN-G01 das Paar ihres
      Partner-Canvas. Dabei ein echter Fehler aufgefallen: die Titelzeile lag **in
      Panel 1** und verschwand mit ihm beim Umschalten. Sie steht jetzt über dem
      `.bsp-tabs`-Umschalter und gilt für beide Ansichten. (Die Tab-Logik läuft über
      `nextElementSibling` ab dem Umschalter — eine Titelzeile davor stört sie nicht.)
- [x] `s3-3` · `ex-canvas` — Paar im `.block-bsp` vor dem `.cv-wrap`, Muster wie A2
      auf derselben Seite

---

## Nachgemessen

Playwright headless bei **1280 px und 360 px**, alle umgebauten Stellen: `.widget`
vorhanden, `widget-header`, `widget-body`, `<h3>` in der Titelzeile, zwei
`.anim-hinweis`, Canvas tatsächlich gezeichnet (Pixel-Scan), Titelzeile einzeilig bei
1280 px, keine JS-Fehler. Zusätzlich der Umschalt-Test auf `g3-1`: nach Klick auf
Beispiel 2 sind Panel, Titelzeile und beide Hinweise sichtbar und das Canvas gezeichnet.
Suchindex und SEO-Metadaten neu gebaut, Pre-Flight über alle 46 Themenseiten bestanden.
