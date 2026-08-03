# TODO — Animations-Einbettung vereinheitlichen (Restarbeit)

**Stand: 3. August 2026.** Fortsetzung der Vereinheitlichung nach STYLEGUIDE §2.10.
Erledigt sind bereits: `.widget`-CSS zentralisiert (Commit `b427df8`), 26 + 4 + 3
freistehende Animationen umgebaut (`d4846db`, `42f95d8`, `589d70a`), der kaputte
Einstieg auf g3-1 repariert (`a5673ad`).

**Auftrag des Auftraggebers (03.08.):** die fünf noch gemischten Seiten
vereinheitlichen — auf den ersten oder zweiten Standardtyp, je nachdem was
einfacher geht — und **alle Animationen dieser Seiten mit dem Hinweispaar
(👁 Worauf achten? / 💡 Erkenntnis) versehen.**

---

## A · Vereinheitlichung — 4 Canvas

Alle vier sind `.anim`-Karten, die auf ihrer Seite neben `.widget`-Karten stehen.
Erprobtes Verfahren (bei `.velo-box` und `.diag-box` in Commit `589d70a` gemacht):
Klasse als Namensraum behalten, ihr die Karten-Optik nehmen
(`background`, `border`, `border-radius`, `box-shadow`), das Ganze in
`.widget > .widget-body` wickeln, `.anim-titel` als `<h3>` in die
`.widget-titelzeile` im `.widget-header` heben.

**Achtung:** `.anim` trägt 22 Nachfahren-Regeln in `style.css` plus 20–32 lokale
je Geometrieseite. Die Klasse darf **nicht** entfernt werden — sonst verliert das
Bedienfeld still seine Gestaltung, und der Pre-Flight merkt das nicht.
Deshalb hier nur die vier Karten auf den drei Seiten anfassen, **nicht** die
53 `.anim`-Karten der übrigen 8 Seiten (die sind in sich stimmig).

- [ ] `grundlagen/g1-2-zahlen-grundoperationen.html` · `cv-zahlmenge` (`.anim`)
- [ ] `grundlagen/g1-2-zahlen-grundoperationen.html` · `cv-iv` (`.iv-anim`, zweispaltiges
      Raster Tabelle | Vis; `.iv-vis` ist selbst eine Karte → Optik dort abgeben)
- [ ] `grundlagen/g1-3-algebraische-terme.html` · `cv-equiv` (`.anim`)
- [ ] `grundlagen/g5-5-trigonometrische-gleichungen.html` · `cv-rad` (`.anim`)

## B · Fehlende Hinweispaare — 9 Canvas

- [ ] `g1-3` · `cv-binomi` + `cv-binomi-rechts` — ein Paar Canvas (Umschaltung über
      `.bin-canvas-paar`), braucht **ein** gemeinsames Hinweispaar
- [ ] `g3-1` · `darst-graph` (im Vier-Darstellungen-Block)
- [ ] `g3-1` · vier Quizkarten in `.fq-karte` (Canvas ohne id)
- [ ] `g3-1` · `ach2-canvas` und `schn2-canvas` (zweite Ansicht eines
      `.bsp-panel`-Umschalters; `ach1`/`schn1` haben je ein Paar)
- [ ] `s3-3-polynomfunktionen.html` · `ex-canvas` (Grafik in einem `.block-bsp`)

**Vorab zu entscheiden (didaktisch, nicht mechanisch):** ob `ach2`/`schn2` und die
vier Quizkarten je ein eigenes Paar bekommen oder mit ihrem Partner-Canvas eines
teilen. Bisherige Praxis laut AN-G01: «die zweite Ansicht eines Widgets teilt das
Paar des Widgets». Danach bräuchten `ach2`/`schn2` keines — dann bleiben noch
`darst-graph`, die vier Quizkarten (falls eigenständig) und `ex-canvas`.

---

## Arbeitsweise (aus den bisherigen Durchgängen gelernt)

- Blockgrenzen **immer** über die `<div>`-Bilanz bestimmen, nicht über Zeilenzahlen
  im Kopf. Zweimal ist eine `</div>` zu viel entstanden, weil das schliessende
  `</div>` der Titelzeile mitkopiert wurde — der Pre-Flight fängt das
  (`<div>-Bilanz: n offen, n+1 geschlossen`), aber es kostet einen Durchgang.
  Bei einem Fehlschlag: `git checkout -- <datei>` und sauber neu bauen.
- Nach jedem Umbau im Browser nachmessen: `.widget` vorhanden, `widget-header`,
  `widget-body`, `<h3>` in der Titelzeile, **zwei** `.anim-hinweis`, Canvas
  tatsächlich gezeichnet (Pixel-Scan), Titelzeile einzeilig bei 1280 px.
- Danach `python3 scripts/build-suchindex.py`, `python3 scripts/build-seo.py`,
  Pre-Flight über alle 46 Seiten — erst dann committen.
