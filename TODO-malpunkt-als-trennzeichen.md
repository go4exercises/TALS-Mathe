# TODO — Malpunkt `·` als Trennzeichen zwischen Termen

**Stand: 27. August 2026 — abgearbeitet.** Vollständige Suche über alle `*.html` und
`*.js` im Repo; alle Stellen sind behoben und im Browser nachgeprüft (siehe
«Ergebnis» am Ende). Die Regel steht jetzt in `STYLEGUIDE.md` §2.1.

## Das Problem

An vielen Stellen trennt ein Mittelpunkt `·` zwei **Aussagen** voneinander — dort, wo
links und rechts davon Mathematik steht, liest sich das als **Multiplikation**. Der
Auslöser dieses Audits, aus der Live-Anzeige von 1.2 «Betrag als Abstand»:

```
|−3| = 3  ·  |−3 − 2| = 5 = |2 − (−3)|
```

Gemeint ist «und ausserdem», gelesen wird «mal 3».

## Regel (freigegeben am 27.08.2026, jetzt STYLEGUIDE §2.1)

> **`·` ist in mathematischem Kontext ausschliesslich das Multiplikationszeichen.**
> Als Trennzeichen zwischen zwei Aussagen, Werten oder Formeln ist es unzulässig.

Ersatz je nach Kontext:

| Situation | Ersatz |
|---|---|
| Zwei/drei gleichrangige Ergebnisse in einer Live-Anzeige | Strichpunkt `;` — oder je Wert ein eigener `<span>`/eine eigene Zeile |
| Zwei aufeinanderfolgende Rechenschritte | Pfeil `→` (im Repo bereits verbreitet) |
| Aufzählung von Fällen in Tabelle oder Prosa | Strichpunkt `;` oder echte Aufzählungsliste |
| Label-Wert-Paare («Amplitude 1 · Periode p = 2π») | Strichpunkt `;` oder eigene Zeile |
| `·` als reiner Prosa-Trenner **ohne** Mathematik daneben (Fusszeile, Link-Untertitel, «Handout · A4 · Bereit zum Drucken») | bleibt unverändert |

**Nicht anfassen:** echte Malpunkte (`2 · 25`, `V = a·b·c`, `3.57·√300`) und das
Skalarprodukt `\vec a \cdot \vec b`. Die Suche unten ist bereits um diese Fälle bereinigt.

## Wie gesucht wurde

Drei Durchläufe über alle `*.html`/`*.js` (ohne `node_modules`, `_archiv` und das
generierte `suchindex.js`):

1. **Relation auf beiden Seiten** — steht sowohl links als auch rechts des `·` ein
   Relationszeichen (`=`, `≤`, `≥`, `≈`, `⇒`, `→`, `∈`), ist das `·` kein Faktor,
   sondern ein Trenner. 223 Treffer, alle einzeln durchgesehen.
2. **Zwei Math-Gruppen** — `\)` … `·` … `\(`. 5 Treffer.
3. **Anzeige-Kontexte** — dieselbe Suche, aber nur in `fl-eq`, `ll-val`, `lt-frage`,
   `zs-formel`, `fillText`, `beschriftung(…)`, und mit Relation auf **nur einer** Seite.
   Fand die Fälle vom Typ `5.00 m/s · 36.9°` und `Boden [−2; 3] · Minimum …`.

Falsch-Positive (echte Multiplikation) sind von Hand aussortiert. Nach dem Beheben
muss `python3 scripts/build-suchindex.py` neu laufen — der Suchindex spiegelt die
Seitentexte und enthält dieselben Stellen nochmals.

## Bestand

| | Anzahl |
|---|---:|
| Themenseiten (`grundlagen/`, `schwerpunkt/`) | **72** Stellen auf 25 Seiten |
| Druckseiten (`downloads/`) | **24** Stellen auf 17 Seiten |
| Reine JS-Kommentare (unsichtbar, kosmetisch) | 8 Stellen |

---

## 1. Themenseiten — sichtbar für Lernende

Live-Anzeigen stehen meist doppelt im Code: einmal als HTML-Startwert, einmal im JS,
das sie beim Bedienen neu schreibt. **Beide Stellen zusammen ändern**, sonst kippt die
Anzeige beim ersten Reglerzug zurück.

### `grundlagen/g1-2-zahlen-grundoperationen.html`

- [x] **Zeile 1587** — Live-Anzeige `#bt-eq` (Betrag als Abstand) — **der vom Auftraggeber genannte Fall; am 26.08.2026 behoben** (`·` → `;`). Zwei Aussagen mit `&nbsp;·&nbsp;` verkettet; HTML-Startwert steht in Zeile 625 (leer, wird vom JS gefüllt).
  ```
  `|<span class="tx-blau">${nz(a)}</span>| = ${nz(Math.abs(a))};&nbsp;&nbsp; ` +   ← neu
  ```

### `grundlagen/g1-3-algebraische-terme.html`

- [x] **Zeile 1798** — Canvas-Beschriftung im Äquivalenz-Widget — trennt zwei Wertaussagen.
  ```
  ctx.fillText(`Anna = Bruno = Cinzia = ${anna} · Dario = ${dario}`, W / 2, H - 6);
  ```

### `grundlagen/g2-2a-lineare-gleichungen.html`

- [x] **Zeile 858** — Tabellenzelle «Drei Fälle» — drei Fallaussagen mit `·` verkettet.
  ```
  <tr><td class="li">Drei Fälle</td> <td>eindeutig (\(a \neq 0\)) · keine Lösung (\(a=0,\; b\neq 0\)) · Identität (\(a=b…
  ```

### `grundlagen/g2-3-lineare-gleichungssysteme.html`

- [x] **Zeile 1339** — Live-Anzeige LGS — `2·x + y = 4 &nbsp;·&nbsp; …`: das Trennzeichen steht direkt neben einem echten Malpunkt.
  ```
  eqEl.innerHTML = `2·x + y = 4 &nbsp;·&nbsp; ${g2links} = ${c} &nbsp; → &nbsp; D = 2 − ${m} = ${D.toFixed(2)} ≠ 0 → ` +
  ```
- [x] **Zeile 1344** — Wie Zeile 1339 (Zweig «identisch»).
  ```
  eqEl.innerHTML = `2·x + y = 4 &nbsp;·&nbsp; 2·x + y = 4 &nbsp; → &nbsp; D = 0 und beide Gleichungen sind gleich: ` +
  ```
- [x] **Zeile 1349** — Wie Zeile 1339 (Zweig «parallel»).
  ```
  eqEl.innerHTML = `2·x + y = 4 &nbsp;·&nbsp; 2·x + y = ${c} &nbsp; → &nbsp; D = 0, Subtraktion ergibt ` +
  ```

### `grundlagen/g3-1-grundlagen.html`

- [x] **Zeile 1209** — Tabellenzelle «Argument · Wert» → Inhalt `\(x\) · \(f(x) = y\)` liest sich als Produkt.
  ```
  <td>\(x\) · \(f(x) = y\)</td>
  ```

### `grundlagen/g3-2-lineare-funktionen.html`

- [x] **Zeile 939** — Preset-Beschreibung: `f(x) = x · Identität: m = 1, b = 0 · 45°-Gerade …`.
  ```
  {label:'Identität', desc:'f(x) = x · Identität: m = 1, b = 0 · 45°-Gerade durch Ursprung', m:1, b:0, vert:false, color…
  ```
- [x] **Zeile 940** — Preset-Beschreibung: `f(x) = 2 · Konstante Funktion …` — hier besonders heikel, weil `2 ·` wie ein Faktor aussieht.
  ```
  {label:'Konstant', desc:'f(x) = 2 · Konstante Funktion: m = 0 · waagrechte Gerade', m:0, b:2, vert:false, color:'#b85c…
  ```
- [x] **Zeile 944** — Preset-Beschreibung (senkrechte Geraden) — Mischung aus echtem Malpunkt und Trennzeichen in derselben Zeile.
  ```
  {label:'Senkrecht ⊥', desc:'Zwei senkrechte Geraden: m₁ · m₂ = 2 · (−0.5) = −1', m:null, b:null, vert:false, color:'#1…
  ```
- [x] **Zeile 1172** — Live-Anzeige Steigungsdreieck: `P(…), Q(…) &nbsp;·&nbsp; Δx = 0 → …`.
  ```
  eqEl.innerHTML = `P(${nz(x1)} | ${nz(y1)}), Q(${nz(x2)} | ${nz(y2)}) &nbsp;·&nbsp; Δx = 0 → ` +
  ```
- [x] **Zeile 1181** — Live-Anzeige Steigungsdreieck, zweiter Zweig.
  ```
  ` &nbsp;·&nbsp; y ${ungefaehr ? '≈' : '='} ${m.toFixed(2).replace('-', '−')}·x ${b >= 0 ? '+' : '−'} ${Math.abs(b).toF…
  ```

### `grundlagen/g3-3-quadratische-funktionen.html`

- [x] **Zeile 1521** — Preset-Beschreibung: `f(x) = x² · Normalparabel: a=1 …`.
  ```
  {label:'Normalparabel', desc:'f(x) = x² · Normalparabel: a=1, Scheitelpunkt im Ursprung', a:1, b:0, c:0, color:'#1a4f8…
  ```
- [x] **Zeile 1527** — Preset-Beschreibung: `f(x) = x² − 3 · b = 0: …`.
  ```
  {label:'reine quadratische', desc:'f(x) = x² − 3 · b = 0: Symmetrieachse ist y-Achse', a:1, b:0, c:-3, color:'#7c3aed'…
  ```

### `grundlagen/g4-3-masszahlen.html`

- [x] **Zeile 945** — Canvas-Beschriftung: `MW = … · Spannweite = …`.
  ```
  beschriftung(ctx, 'MW = ' + meanA.toFixed(2) + ' · Spannweite = ' + spanA.toFixed(1),
  ```
- [x] **Zeile 948** — Wie Zeile 945 (zweiter Datensatz).
  ```
  beschriftung(ctx, 'MW = ' + meanB.toFixed(2) + ' · Spannweite = ' + spanB.toFixed(1),
  ```

### `grundlagen/g5-1-grundlagen.html`

- [x] **Zeile 775** — SVG-Text: `Scheitel: α = α · Neben: α + β = 180°`.
  ```
  <text x="110" y="155" font-size="11" fill="#5a5040" text-anchor="middle">Scheitel: α = α · Neben: α + β = 180°</text>
  ```

### `grundlagen/g5-5-trigonometrische-gleichungen.html`

- [x] **Zeile 379** — Live-Anzeige `#gl-val` (HTML-Startwert): `φ₁ = 30° · φ₂ = 150°`.
  ```
  <div class="ll-val" id="gl-val">φ₁ = 30° · φ₂ = 150°</div>
  ```
- [x] **Zeile 544** — Live-Anzeige `#kk-val` (HTML-Startwert).
  ```
  <div class="ll-val" id="kk-val">φ₁ = 30° · φ₂ = 150° (= 180° − φ₁)</div>
  ```
- [x] **Zeile 556** — Live-Anzeige `#lt-frage`: `Gleichung: sin φ = 0.5 · Rechner: φ₁ = 30°` — `0.5 · Rechner` liest sich als Produkt.
  ```
  <div class="lt-frage" id="lt-frage">Gleichung: sin φ = 0.5 · Rechner: φ₁ = 30°</div>
  ```
- [x] **Zeile 963** — JS-Partner zu Zeile 379.
  ```
  valOut.textContent = `φ₁ = ${fmt(arr[0])} · φ₂ = ${fmt(arr[1])}`;
  ```
- [x] **Zeile 994** — JS-Partner zu Zeile 544.
  ```
  valOut.textContent = `φ₁ = ${fmt(arr[0])} · φ₂ = ${fmt(arr[1])}`;
  ```
- [x] **Zeile 1013** — Dritte Stelle mit `φ₁ = … · φ₂ = …`.
  ```
  valOut.textContent = `φ₁ = ${fmt(arr[0])} · φ₂ = ${fmt(arr[1])}`;
  ```
- [x] **Zeile 1535** — Live-Anzeige Spiegelachse: `φ₁ = … · φ₂ = … — spiegelbildlich …`.
  ```
  val.textContent = `φ₁ = ${sol[0].toFixed(1)}° · φ₂ = ${sol[1].toFixed(1)}° — spiegelbildlich zur ${achse} Achse`;
  ```
- [x] **Zeile 1576** — JS-Partner zu Zeile 556.
  ```
  `Gleichung: ${a.typ} φ = ${nz(a.c)} · Rechner: ${a.typ === 'sin' ? 'arcsin' : 'arccos'}(${nz(a.c)}) = ${nz(a.tr)}°${hi…
  ```

### `schwerpunkt/s1-1-grundlagen.html`

- [x] **Zeile 774** — Live-Anzeige: `(a+b)² = … · a²+b² = … · Differenz = …` — drei Aussagen in einer Zeile.
  ```
  `(a+b)² = ${fmt2(links)} · a²+b² = ${fmt2(rechts)} · Differenz = ${fmt2(links - rechts)} = 2ab`;
  ```

### `schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html`

- [x] **Zeile 377** — Live-Anzeige `#sc-eq` (HTML-Startwert): `… ⇒ x = 3 · Probe: √25 = 5 ✓ · L = {3}`.
  ```
  <div class="fl-eq" id="sc-eq">6x + 7 = 25 ⇒ x = 3 · Probe: √25 = 5 ✓ · L = {3}</div>
  ```
- [x] **Zeile 416** — Live-Anzeige `#br-eq` (HTML-Startwert): `D = ℝ \ {3} · Kandidat x = 2 ∈ D ⇒ L = {2}`.
  ```
  <div class="fl-eq" id="br-eq">D = ℝ \ {3} · Kandidat x = 2 ∈ D ⇒ L = {2}</div>
  ```
- [x] **Zeile 908** — JS-Partner zu Zeile 377.
  ```
  {c: 5, eq: '6x + 7 = 25 ⇒ x = 3 · Probe: √25 = 5 ✓ · L = {3}'},
  ```
- [x] **Zeile 909** — JS-Partner zu Zeile 377 (Scheinlösungs-Zweig).
  ```
  {c: -5, eq: '6x + 7 = 25 ⇒ x = 3 · Probe: √25 = 5 ≠ −5 ✗ · L = { } (Scheinlösung!)'},
  ```
- [x] **Zeile 1017** — JS-Partner zu Zeile 416 (Pol-Zweig).
  ```
  ? `D = ℝ \\ {2} · Kandidat x = 2 ∉ D (Pol!) ⇒ <span class="tx-orange">L = { }</span>`
  ```
- [x] **Zeile 1018** — JS-Partner zu Zeile 416.
  ```
  : `D = ℝ \\ {${n.toFixed(1)}} · Kandidat x = 2 ∈ D ⇒ L = {2}`;
  ```

### `schwerpunkt/s2-2b-exponential-logarithmische-gleichungen.html`

- [x] **Zeile 389** — Live-Anzeige `#gl-eq` (HTML-Startwert): `x = log₃(8) = … ≈ 1.89 · L = {1.89}`.
  ```
  <div class="fl-eq" id="gl-eq">x = log₃(8) = ln 8 / ln 3 ≈ 1.89 · L = {1.89}</div>
  ```
- [x] **Zeile 495** — Live-Anzeige `#ld-eq` (HTML-Startwert): vier Aussagen mit `·` verkettet.
  ```
  <div class="fl-eq" id="ld-eq">D: x &gt; 3 · x₁ = 5 ∈ D ✓ · x₂ = −2 ∉ D (Scheinlösung) · L = {5}</div>
  ```
- [x] **Zeile 906** — JS-Partner zu Zeile 389.
  ```
  {lhs: x => Math.pow(3, x), rhs: x => 8, eq: 'x = log₃(8) = ln 8 / ln 3 ≈ 1.89 · L = {1.89}',
  ```
- [x] **Zeile 1011** — JS-Partner zu Zeile 495.
  ```
  `D: x &gt; ${fmtU} · x₁ = ${xg.toFixed(2)} ∈ D ✓ · x₂ = ${xs.toFixed(2)} ∉ D (Scheinlösung) · L = {${xg.toFixed(2)}}`;
  ```

### `schwerpunkt/s3-1-grundlagen.html`

- [x] **Zeile 498** — Bildlegende: `Parabel \(f(x)=x^2+c\) violett · Gerade \(g(x)=x+1\) blau · …` (niedrige Prio: Prosa, aber Math direkt links des Punktes).
  ```
  <p>Parabel \(f(x)=x^2+c\) violett · Gerade \(g(x)=x+1\) blau · Schnittstellen rot · Lösung grün auf der \(x\)-Achse, b…
  ```

### `schwerpunkt/s3-2a-potenzfunktionen.html`

- [x] **Zeile 492** — Live-Anzeige `#pa-eq` (HTML-Startwert): `gerade · f(−x) = +f(x) · achsensymmetrisch …`; JS dazu ab Zeile 1300.
  ```
  <div class="fl-eq" id="pa-eq">gerade · f(−x) = +f(x) · achsensymmetrisch zur y-Achse</div>
  ```
- [x] **Zeile 565** — Live-Anzeige `#hy-asym` (HTML-Startwert): `Polgerade: x = 1 · Asymptote: y = −1`.
  ```
  <div class="fl-eq" id="hy-asym" style="font-size:0.95rem;margin-top:4px">Polgerade: x = <span class="tx-blau">1</span>…
  ```
- [x] **Zeile 1149** — JS-Partner zu Zeile 565.
  ```
  `Polgerade: x = ${T('blau', uD)} · Asymptote: y = ${T('orange', vD)}`;
  ```

### `schwerpunkt/s3-2b-wurzelfunktionen.html`

- [x] **Zeile 499** — Live-Anzeige `#tf-eq` (HTML-Startwert): `y = √x · D = [0; ∞[`.
  ```
  <div class="fl-eq" id="tf-eq">y = √x · D = [0; ∞[</div>
  ```
- [x] **Zeile 1219** — JS-Partner zu Zeile 499.
  ```
  document.getElementById('tf-eq').innerHTML = `y = ${aStr}${wSym}${arg}${vStr} · ${dom}`;
  ```

### `schwerpunkt/s3-4a-exponentialfunktionen.html`

- [x] **Zeile 1086** — Preset-Beschreibung: `y = eˣ · natürliche Exponentialfunktion …`.
  ```
  {label:'eˣ', f: x => Math.exp(x), desc:'y = eˣ · natürliche Exponentialfunktion, e ≈ 2.718 — zwischen 2ˣ und 3ˣ', colo…
  ```
- [x] **Zeile 1135** — Live-Anzeige: `Asymptote: y = … · Ordinatenabschnitt: y₀ = …`.
  ```
  `Asymptote: y = ${T('orange', String(v).replace('-', '−'))} · Ordinatenabschnitt: y₀ = ${fmt2(b.f(-u) + v).replace('-'…
  ```
- [x] **Zeile 1235** — Live-Anzeige e-Grenzwert: `n = … &nbsp;·&nbsp; (1 + 1/n)ⁿ = …`.
  ```
  `n = ${n.toLocaleString('de-CH')} &nbsp;·&nbsp; (1 + 1/n)<sup>n</sup> = <strong>${wert.toFixed(6)}</strong>` +
  ```

### `schwerpunkt/s3-4b-logarithmusfunktionen.html`

- [x] **Zeile 356** — Live-Anzeige `#sp-eq`: `y = 2ˣ · y = log₂(x)` — zwei Funktionsgleichungen.
  ```
  <div class="fl-eq" id="sp-eq"><span class="tx-blau">y = 2ˣ</span> · <span style="color:#5b2d8e">y = log₂(x)</span></di…
  ```
- [x] **Zeile 436** — Bildlegende: `… · Zeiger bei \(x\) · \(\lg x\) als Abstand`.
  ```
  <p>Oben lineare Achse (0…1000) · unten log-Achse (10⁰…10³) · Zeiger bei \(x\) · \(\lg x\) als Abstand</p>
  ```
- [x] **Zeile 452** — Live-Anzeige `#ll-eq`: `x = 100 · lg(100) = 2` — liest sich exakt wie das Produkt \(100 \cdot \lg 100\).
  ```
  <div class="fl-eq" id="ll-eq">x = 100 · lg(100) = 2</div>
  ```
- [x] **Zeile 530** — Live-Anzeige `#tr-info`: `Asymptote: x = 0 · Nullstelle: x₀ = 0.5`.
  ```
  <div class="fl-eq" id="tr-info" style="font-size:0.95rem;margin-top:4px">Asymptote: x = <span class="tx-blau">0</span>…
  ```
- [x] **Zeile 1078** — Preset-Beschreibung: `y = ln(x) · natürlicher Logarithmus …`.
  ```
  {label:'ln(x)', f: x => Math.log(x), desc:'y = ln(x) · natürlicher Logarithmus, Basis e ≈ 2.718 — zwischen log₂ und lo…
  ```
- [x] **Zeile 1132** — JS-Partner zu Zeile 530.
  ```
  `Asymptote: x = ${T('blau', String(u).replace('-', '−'))} · Nullstelle: x₀ = ${fmt2(x0).replace('-', '−')}`;
  ```
- [x] **Zeile 1231** — JS-Partner zu Zeile 452.
  ```
  `x = ${x >= 100 ? Math.round(x) : x.toFixed(2)} · lg(x) = ${L.toFixed(2)}`;
  ```

### `schwerpunkt/s3-5-trigonometrische-funktionen.html`

- [x] **Zeile 356** — Live-Anzeige `#ek-eq`: `sin(7π/12) ≈ 0.97 · x ≈ 105°`.
  ```
  <div class="fl-eq" id="ek-eq">sin(7π/12) ≈ 0.97 · x ≈ 105°</div>
  ```
- [x] **Zeile 494** — Live-Anzeige `#tr-info`: `Amplitude 1 · Periode p = 2π · Mittellinie y = 0`.
  ```
  <div class="fl-eq" id="tr-info" style="font-size:0.95rem;margin-top:4px">Amplitude 1 · Periode p = 2π · Mittellinie y …
  ```
- [x] **Zeile 1188** — JS-Partner zu Zeile 494.
  ```
  `Amplitude ${T('blau', fmt(a))} · Periode p = ${T('orange', pStr)} · Mittellinie y = ${T('orange', String(v).replace('…
  ```

### `schwerpunkt/s3-6-betragsfunktionen.html`

- [x] **Zeile 562** — Live-Anzeige `#wa-eq` (HTML-Startwert): `Boden [−2; 3] · Minimum |a−b| = 5`.
  ```
  <div class="fl-eq" id="wa-eq">Boden [−2; 3] · Minimum |a−b| = 5</div>
  ```
- [x] **Zeile 1162** — JS-Partner zu Zeile 562 (Zweig «Punkt»).
  ```
  ? `Boden zu einem Punkt · Minimum = 0 · reines V bei x = ${a}`
  ```
- [x] **Zeile 1163** — JS-Partner zu Zeile 562 (Zweig «Intervall»).
  ```
  : `Boden [${lo}; ${hi}] · Minimum |a−b| = ${boden}`;
  ```

### `schwerpunkt/s4-2a-prismen-zylinder.html`

- [x] **Zeile 859** — Live-Anzeige: `V = … cm³ · O = … cm² · d = … cm`.
  ```
  `V = ${fmt2(V)} cm³ · O = ${fmt2(O)} cm² · d = ${d.toFixed(2)} cm`;
  ```
- [x] **Zeile 912** — Live-Anzeige: `V = … · M = … · O = …`.
  ```
  `V = ${V.toFixed(1)} cm³ · M = ${M.toFixed(1)} cm² · O = ${O.toFixed(1)} cm²`;
  ```

### `schwerpunkt/s4-2b-pyramiden-kegel-stuempfe.html`

- [x] **Zeile 854** — Live-Anzeige: `m = … · V = … · M = … · w = …°` — vier Werte.
  ```
  `m = ${m.toFixed(2)} · V = ${V.toFixed(1)} cm³ · M = ${M.toFixed(1)} cm² · w = ${w.toFixed(1)}°`;
  ```

### `schwerpunkt/s4-2c-kugel.html`

- [x] **Zeile 391** — Live-Anzeige `#ku-eq` (HTML-Startwert): `A = 62.83 cm² · V_Segment = … · V_Sektor = …`.
  ```
  <div class="formel-live"><div class="fl-label">Kappe · Segment · Sektor</div><div class="fl-eq" id="ku-eq">A = 62.83 c…
  ```
- [x] **Zeile 758** — Live-Anzeige Kugel/Zylinder: `V_Kugel = … · V_Zylinder = … · Verhältnis = …`.
  ```
  `V_Kugel = ${VK.toFixed(1)} · V_Zylinder = ${VZ.toFixed(1)} · Verhältnis = ${(VK / VZ * 3).toFixed(0)} : 3`;
  ```
- [x] **Zeile 848** — JS-Partner zu Zeile 391.
  ```
  `A = ${Akap.toFixed(2)} cm² · V_Segment = ${Vseg.toFixed(2)} cm³ · V_Sektor = ${Vsek.toFixed(2)} cm³`;
  ```

### `schwerpunkt/s4-3a-vektorbegriff-komponenten.html`

- [x] **Zeile 287** — Live-Anzeige `#fl-eq` (HTML-Startwert): `… = 5.00 m/s · 36.9° zur Querrichtung` — Zahl · Zahl, der schlimmste Fall.
  ```
  <div class="fl-eq" id="fl-eq">|v| = √(3.0² + 4.0²) = 5.00 m/s · 36.9° zur Querrichtung</div>
  ```
- [x] **Zeile 407** — Live-Anzeige `#ad-eq` (HTML-Startwert): `a + b = (4 | 3) · |a + b| = 5.00`.
  ```
  <div class="fl-eq" id="ad-eq">a + b = (4 | 3) · |a + b| = 5.00</div>
  ```
- [x] **Zeile 864** — JS-Partner zu Zeile 287.
  ```
  document.getElementById('fl-eq').innerHTML =
  ```
- [x] **Zeile 905** — JS-Partner zu Zeile 407.
  ```
  `a + b = (${String(s1).replace('-', '−')} | ${String(s2).replace('-', '−')}) · |a + b| = ${betrag.toFixed(2)}`;
  ```
- [x] **Zeile 1018** — Live-Anzeige Richtungswinkel: `r = … &nbsp;·&nbsp; a₁ = 0: …`.
  ```
  eqEl.innerHTML = `r = ${nz(r)} &nbsp;·&nbsp; a₁ = 0: der Quotient a₂/a₁ ist <strong>nicht definiert</strong> &nbsp;→&n…
  ```
- [x] **Zeile 1024** — Live-Anzeige Richtungswinkel: `r = … &nbsp;·&nbsp; arctan(…) = …°`.
  ```
  eqEl.innerHTML = `r = ${nz(r)} &nbsp;·&nbsp; arctan(${kl(a2)}/${kl(a1)}) = <span class="tx-orange">${nz(tr)}°</span>` …
  ```

### `schwerpunkt/s4-3b-skalarprodukt.html`

- [x] **Zeile 276** — Bildlegende: `F = 50 N · s = 8 m · Projektion der Kraft grün` — auf einer Seite, die `·` gleichzeitig als Skalarprodukt-Zeichen verwendet.
  ```
  <p>F = 50 N · s = 8 m · Projektion der Kraft grün</p>
  ```
- [x] **Zeile 382** — Bildlegende: `\(\vec a = …\) fest (blau) · \(\vec b\) drehbar … · Projektion …` (gleiche Seite, gleiche Verwechslungsgefahr).
  ```
  <p>\(\vec{a} = \binom{4}{1}\) fest (blau) · \(\vec{b}\) drehbar mit \(|\vec{b}| = 3\) (orange) · Projektion \(\vec{b}_…
  ```

---

## 2. Druckseiten `downloads/` — niedrigere Prio

Gleiche Regel, aber nur beim Drucken sichtbar. Die Lösungszeilen der «Teste dich
selbst»-Seiten folgen alle demselben Muster `(a) … · (b) … · (c) …`; dort genügt ein
Strichpunkt oder eine echte Liste.

### `downloads/grundlagen/g4-3-masszahlen/formelauszug.html`

- [x] **Zeile 86** — Fünf-Punkte-Zusammenfassung `min · \(Q_1\) · \(\tilde x\) · \(Q_3\) · max`.
  ```
  <p>min · \(Q_1\) · \(\tilde{x}\) · \(Q_3\) · max</p>
  ```

### `downloads/grundlagen/g5-3-trigonometrische-berechnungen/handout.html`

- [x] **Zeile 47** — `Sinus = … · Cosinus = … · Tangens = …`.
  ```
  <p><strong>SOH-CAH-TOA</strong> — Sinus = Opposite/Hypotenuse · Cosinus = Adjacent/Hypotenuse · Tangens = Opposite/Adj…
  ```

### `downloads/schwerpunkt/s2-1-grundlagen/formelauszug.html`

- [x] **Zeile 47** — `Nenner \(\neq 0\) · Radikand \(\geq 0\) · Log-Argument \(> 0\)`.
  ```
  <tr><td class="li" style="width:35%">Definitionsmenge \(D\)</td><td class="li">Nenner \( \neq 0 \) · Radikand \( \geq …
  ```

### `downloads/schwerpunkt/s2-1-grundlagen/teste-dich-selbst.html`

- [x] **Zeile 193** — Lösungszeile `(a) … · (b) …`.
  ```
  <p>(a) allgemeingültig: \( L = \mathbb{R} \) (Identität) · (b) unlösbar: \( L = \{\,\} \).</p>
  ```
- [x] **Zeile 207** — Lösungszeile `(a) … · (b) …`.
  ```
  <p>(a) \( D = \mathbb{R} \setminus \{3\} \) · (b) \( 2x - 8 \geq 0 \Rightarrow x \geq 4 \) ·
  ```

### `downloads/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen/teste-dich-selbst.html`

- [x] **Zeile 186** — Lösungszeile `(a) … · (b) …`.
  ```
  <p>(a) \( L = \{-3\} \) (ungerader Exponent) · (b) \( L = \{-3;\ 3\} \) ·
  ```

### `downloads/schwerpunkt/s2-2b-exponential-logarithmische-gleichungen/teste-dich-selbst.html`

- [x] **Zeile 187** — Lösungszeile.
  ```
  <p>(a) \( x = 4 \) · (b) \( 3^x = 3^{-3} \Rightarrow x = -3 \) ·
  ```
- [x] **Zeile 216** — Lösungszeile.
  ```
  <p>(a) \( x = 10^4 \) · (b) \( x = e^{-1} \approx 0.37 \) ·
  ```

### `downloads/schwerpunkt/s2-2c-betrag-polynom-ungleichungen/teste-dich-selbst.html`

- [x] **Zeile 182** — Lösungszeile.
  ```
  <p>(a) \(7\) · (b) \( |-5| = 5 \) · (c) \( \pi > 3 \), also \( \pi - 3 \approx 0.14 \).</p>
  ```

### `downloads/schwerpunkt/s3-1-grundlagen/formelauszug.html`

- [x] **Zeile 89** — `\(a < 0\): Maximum \(v\) · \(a > 0\): Minimum \(v\)`.
  ```
  <tr><td class="li">Maximum / Minimum</td><td>\( a < 0 \): Maximum \(v\) · \( a > 0 \): Minimum \(v\)</td></tr>
  ```

### `downloads/schwerpunkt/s3-1-grundlagen/teste-dich-selbst.html`

- [x] **Zeile 188** — Lösungszeile.
  ```
  <p>(a) \( D = \mathbb{R}_0^+ \) · (b) \( D = \mathbb{R} \setminus \{0\} \) ·
  ```
- [x] **Zeile 193** — Lösungszeile.
  ```
  <p>(a) \( (0 \mid 1) \), denn \( a^0 = 1 \) · (b) \( (1 \mid 0) \), denn \( \log_a 1 = 0 \) ·
  ```

### `downloads/schwerpunkt/s3-2a-potenzfunktionen/teste-dich-selbst.html`

- [x] **Zeile 197** — Lösungszeile.
  ```
  <p>(a) gerade → achsensymmetrisch zur \(y\)-Achse · (b) ungerade → punktsymmetrisch zum Ursprung ·
  ```
- [x] **Zeile 198** — Lösungszeile.
  ```
  (c) ungerade (Exponent \(-3\)) → punktsymmetrisch · (d) gerade (Exponent \(-4\)) → achsensymmetrisch.</p>
  ```

### `downloads/schwerpunkt/s3-2b-wurzelfunktionen/teste-dich-selbst.html`

- [x] **Zeile 197** — Lösungszeile.
  ```
  <p>(a) \( y = \sqrt[4]{x} \) · (b) \( y = \sqrt[5]{x} \).</p>
  ```

### `downloads/schwerpunkt/s3-4a-exponentialfunktionen/teste-dich-selbst.html`

- [x] **Zeile 198** — Lösungszeile.
  ```
  <p>(a) steigend (\( a = 3 > 1 \)) · (b) fallend (\( a = \tfrac{1}{4} < 1 \)) ·
  ```
- [x] **Zeile 199** — Lösungszeile.
  ```
  (c) fallend (\( a = 0.9 < 1 \)) · (d) steigend (\( a = \tfrac{5}{2} > 1 \)).</p>
  ```

### `downloads/schwerpunkt/s3-4b-logarithmusfunktionen/teste-dich-selbst.html`

- [x] **Zeile 192** — Lösungszeile.
  ```
  <p>(a) \( 2^5 = 32 \Rightarrow 5 \) · (b) \( 3^{-2} = \tfrac{1}{9} \Rightarrow -2 \) ·
  ```
- [x] **Zeile 193** — Lösungszeile.
  ```
  (c) \( 10^4 \Rightarrow 4 \) · (d) \( e^1 = e \Rightarrow 1 \).</p>
  ```
- [x] **Zeile 197** — Lösungszeile.
  ```
  <p>(a) \( y = \log_4 x \) · (b) \( y = 10^x \) — die Umkehrfunktion der Logarithmusfunktion
  ```

### `downloads/schwerpunkt/s3-6-betragsfunktionen/teste-dich-selbst.html`

- [x] **Zeile 185** — Lösungszeile.
  ```
  <p>(a) \( 4 \) · (b) \( |{-4}| = 4 \) · (c) \( |-3| + 2 = 5 \).</p>
  ```

### `downloads/schwerpunkt/s4-3a-vektorbegriff-komponenten/handout.html`

- [x] **Zeile 62** — Zwei Formeln in einer Tabellenzelle mit `·` getrennt.
  ```
  <tr><td class="li">Mittelpunkt / Schwerpunkt</td><td>\( \vec{r}_M = \tfrac{1}{2}(\vec{r}_A + \vec{r}_B) \) · \( \vec{r…
  ```

### `downloads/schwerpunkt/s4-3c-geraden/handout.html`

- [x] **Zeile 65** — `… = 0 \) → \(t\) · (3) Abstand …` — Schrittzähler mit `·` getrennt.
  ```
  \( \vec{PF} \cdot \vec{u} = 0 \) → \(t\) · (3) Abstand \( d = |\vec{PF}| \).</p>
  ```

### `downloads/schwerpunkt/s4-3d-ebenen/formelauszug.html`

- [x] **Zeile 64** — `1 Lösung = Durchstosspunkt · 0 = parallel · ∞ = enthalten`.
  ```
  <tr><td class="li" style="width:35%">Gerade–Ebene</td><td class="li">gleichsetzen (\(r\), \(s\), \(t\)): 1 Lösung = Du…
  ```

---

## 3. Nur JS-Kommentare — kosmetisch, kein Blocker

Unsichtbar für Lernende; der Vollständigkeit halber erfasst.

- [x] `grundlagen/g1-2-zahlen-grundoperationen.html` — Zeile 1576
- [x] `grundlagen/g1-3-algebraische-terme.html` — Zeile 2909
- [x] `grundlagen/g2-3-lineare-gleichungssysteme.html` — Zeile 1315, 1317
- [x] `grundlagen/g4-0-praxisbeispiel-bm2-klasse.html` — Zeile 957
- [x] `schwerpunkt/s1-2-potenzen.html` — Zeile 949
- [x] `schwerpunkt/s2-1-grundlagen.html` — Zeile 800
- [x] `schwerpunkt/s4-3a-vektorbegriff-komponenten.html` — Zeile 993

---

## Abschluss

Nach dem Beheben:

1. `python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html`
2. `python3 scripts/build-suchindex.py`
3. Die Regel in `STYLEGUIDE.md` verankern, damit sie nicht zurückkommt.

---

## Ergebnis

**112 Stellen geändert** in 42 Dateien:

| | Anzahl |
|---|---:|
| Themenseiten, statisch gefunden | 72 |
| Themenseiten, **erst im Browser sichtbar** | 10 |
| Druckseiten `downloads/` | 24 |
| JS-Kommentare | 6 |

### Zwei Nachträge zur Liste oben

- **`grundlagen/g3-2-lineare-funktionen.html` Zeile 944** (`m₁ · m₂ = 2 · (−0.5) = −1`)
  war ein Falsch-Positiv — echte Multiplikation, unverändert geblieben.
- **`grundlagen/g2-2b-quadratische-gleichungen.html` Zeilen 741–743**
  (`Faktorisieren · x ausklammern`) kamen dazu: dort steht jetzt `→`, weil das `·`
  eine Methode von ihrem konkreten Schritt trennte.

### Was der statische Blick nicht fand

Zehn Stellen erzeugt das JS erst beim Bedienen — sie stehen in Code-Zweigen, deren
Zeile kein Relationszeichen auf beiden Seiten trägt, oder sie überschreiben den
HTML-Startwert mit einer anderen Zeichenkette:

| Seite | Anzeige |
|---|---|
| `g3-1` | `y = 0.5·x + 1 · Testgerade und Kurve: …` |
| `g3-2` | `P(−2 \| −1), Q(3 \| 3) · m = Δy/Δx = …` |
| `g3-3` | `U = … = 40 m · A = 10.0 · 10.0 = …` |
| `s3-4a` | `(1 + 1/n)ⁿ = 2.676990 · e − Wert = …` |
| `s3-4b` | `y = 2ˣ · y = log₂(x)` (JS überschrieb den bereits korrigierten Startwert) |
| `s3-5` | `sin(7π/12) ≈ 0.97 · x = 105°` |
| `s3-6` | `Knick (0\|0) · Ast-Steigungen ±1` |
| `s4-2b` | `1.0 Füllungen · Prisma zu 33 % voll` |
| `s4-3b` | `a · b = 8.60 — positiv (spitz) · Zwischenwinkel 46.0°` |

**Lehre daraus:** Live-Anzeigen müssen im Browser geprüft werden, nicht im Quelltext.
Dafür gibt es jetzt `.claude/tools/scan-live.mjs`.

### Womit geprüft wurde

| Werkzeug | Ergebnis |
|---|---|
| `python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html` | ALLE CHECKS BESTANDEN |
| `node scripts/verify_mathjax.js` über die 17 geänderten Druckseiten | 794 Ausdrücke, 0 Fehler |
| `node .claude/tools/scan-live.mjs grundlagen/*.html schwerpunkt/*.html` (neu) | 106 Anzeigen mit `·` — alle echte Multiplikation, kein Trenner mehr |
| `node .claude/tools/check-anzeigen.mjs …` (neu) | 46 Seiten, 0 JS-Fehler, keine tote Anzeige |
| `node .claude/tools/check-breite.mjs …` (neu) | kein Überlauf bei 360 px |

Die drei Skripte liegen unter `.claude/tools/` und lassen sich für den nächsten
Audit dieser Art wiederverwenden.
