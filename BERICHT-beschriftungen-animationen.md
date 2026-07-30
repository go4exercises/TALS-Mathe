# Beschriftungs-Konflikte in den Canvas-Animationen

Prüflauf vom **30.07.2026** über **alle 46 Themenseiten** (`grundlagen/` + `schwerpunkt/`),
jede Animation in ihrer **Startposition**, ohne jede Interaktion. **An den Seiten wurde
nichts geändert** — dieser Bericht ist reine Bestandsaufnahme.

Die Links zeigen auf den lokalen Server: `python3 -m http.server 8001` im Repo-Root starten,
dann sind sie klickbar. Der Anker ist die Canvas-ID, der Browser springt direkt auf die Grafik.

---

## 1. Was gemessen wurde

Für jeden Aufruf von `fillText`/`strokeText` auf einem 2D-Canvas wurde protokolliert:
das Textfeld (aus `measureText` samt `textAlign`/`textBaseline` und der aktiven
Transformationsmatrix) und die Canvas-Pixel im Feld unmittelbar **vor** und **nach**
dem Zeichnen, dazu der Endzustand nach dem Rendern. Daraus vier Befundarten:

| Art | Bedeutung |
|---|---|
| **Text über Text** | Zwei Beschriftungen, die am Ende **beide sichtbar** sind, überdecken sich zu ≥ 25 % der kleineren Fläche. |
| **Text auf Grafikelement** | ≥ 25 % der Glyphenpixel liegen auf Nicht-Hintergrund — Linie, Kurve, Fläche, Punkt. |
| **ausserhalb des Canvas** | Das Textfeld reicht > 1.5 px über den Rand; die Beschriftung ist angeschnitten oder ganz weg. |
| **Rest einer überdeckten Beschriftung** | Von einer absichtlich abgedeckten Beschriftung bleiben 3–45 % stehen (siehe §2.2). |

Ausgewertet wird immer der **letzte Zeichendurchgang** — also das, was am Ende dasteht.
Beschriftungen, die absichtlich vollständig überdeckt werden, zählen **nicht** als Konflikt.

**Umfang:** 205 Canvas mit 2573 messbaren Beschriftungen. Auffällig: **55 Canvas auf 27 Seiten** mit 228 Einzelbefunden.

**Jeder der aufgeführten Canvas wurde einzeln am Bild nachgesehen** (Kontrollbilder mit
markierten Textfeldern bei 1280 px). Fehlalarme sind dabei keine übrig geblieben.

---

## 2. Zwei systematische Ursachen

Der grösste Teil der schweren Fälle geht auf zwei Muster zurück, nicht auf Einzelfehler.

### 2.1 Anwendungsgraphen mit Nullpunkt in der Ecke verlieren **alle** Achsenzahlen

`mathlib.js` → `drawGrid()` setzt die Achsenzahlen relativ zum Nullpunkt:

```js
for (…) ctx.fillText(gx, cx(gx), cy(0) + 14);   // x-Zahlen: 14 px UNTER der x-Achse
for (…) ctx.fillText(gy, cx(0) - 5,  cy(gy) + 4);  // y-Zahlen: 5 px LINKS der y-Achse
```

Bei einem Achsenkreuz in der Bildmitte stimmt das. Bei Anwendungsgraphen mit
`xMin = 0` und/oder `yMin = 0` liegt der Nullpunkt aber am Canvasrand: `cy(0)` ist die
Unterkante, `cx(0)` die linke Kante. Damit landen die x-Zahlen **unterhalb** und die
y-Zahlen **links ausserhalb** der Zeichenfläche — sie sind ersatzlos weg. Betroffen
sind fünf Canvas; die Skalierung steht jeweils in der eigenen `xMin/yMin`-Zeile der Seite.

### 2.2 Der dokumentierte Abdeck-Trick für Achsen-Captions lässt einen Rest stehen

`drawGrid()` schreibt immer die generischen Labels `x` und `y`. Der Kopfkommentar von
`mathlib.js` beschreibt, wie eine Seite sie durch eigene mit Einheit ersetzt: Bereich mit
`fillRect` weiss übermalen, dann neu schreiben. Die Rechtecke sind aber mit festen
Pixelwerten hinterlegt (`fillRect(W-30, cy(0)-22, 30, 18)`) und treffen den Glyphen nicht
in jeder Skalierung ganz. Übrig bleibt ein Strichrest direkt neben der neuen Caption.
Messbar als 3–45 % verbliebene Glyphenfläche — im Bericht als *Rest einer überdeckten
Beschriftung* geführt.

---

## 3. Schwer — Beschriftung fehlt, ist angeschnitten oder unlesbar

Hier geht Information verloren oder zwei Texte machen sich gegenseitig unlesbar. — **20 Animationen**.

### `cv-equiv` — g1-3-algebraische-terme

[→ http://localhost:8001/grundlagen/g1-3-algebraische-terme.html#cv-equiv](http://localhost:8001/grundlagen/g1-3-algebraische-terme.html#cv-equiv)

«nicht äquivalent» und «+490 zu viel» liegen zu 30 % übereinander.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `nicht äquivalent  ⇄  +490 zu viel` | 0.3 |

### `uf-canvas` — g2-1-grundlagen

[→ http://localhost:8001/grundlagen/g2-1-grundlagen.html#uf-canvas](http://localhost:8001/grundlagen/g2-1-grundlagen.html#uf-canvas)

«4·x + 3 (= 15 bei x=3)» ragt 27 px über den linken Rand hinaus.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `4·x + 3 (= 15 bei x=3)` | links 27px |

### `velo-canvas` — g2-2b-quadratische-gleichungen

[→ http://localhost:8001/grundlagen/g2-2b-quadratische-gleichungen.html#velo-canvas](http://localhost:8001/grundlagen/g2-2b-quadratische-gleichungen.html#velo-canvas)

«Hinweg →» (7 px) und «← Rückweg» (14 px) sind links abgeschnitten.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `Hinweg →` | links 7px |
| ausserhalb des Canvas | `← Rückweg` | links 14px |

### `cv-kino` — g2-3-lineare-gleichungssysteme

[→ http://localhost:8001/grundlagen/g2-3-lineare-gleichungssysteme.html#cv-kino](http://localhost:8001/grundlagen/g2-3-lineare-gleichungssysteme.html#cv-kino)

Alle Achsenzahlen fehlen (14 von 21 ausserhalb). Vom generischen «y» bleibt ein Rest neben «y [Kinder]» stehen.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `1` | links 12px |
| ausserhalb des Canvas | `3` | links 13px |
| ausserhalb des Canvas | `5` | links 13px |
| ausserhalb des Canvas | `7` | links 13px |
| ausserhalb des Canvas | `9` | links 13px |
| ausserhalb des Canvas | `11` | links 20px |
| ausserhalb des Canvas | … weitere 8 gleichartige | |

### `cv-lbuschel` — g2-3-lineare-gleichungssysteme

[→ http://localhost:8001/grundlagen/g2-3-lineare-gleichungssysteme.html#cv-lbuschel](http://localhost:8001/grundlagen/g2-3-lineare-gleichungssysteme.html#cv-lbuschel)

«S(0.00 | 4.00)» liegt auf der y-Achsenzahl 5.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `5  ⇄  S(0.00 \| 4.00)` | 0.29 |

### `einstieg-glas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#einstieg-glas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#einstieg-glas)

Die zweistelligen Skalenzahlen 15/20/25/30 stehen 2–8 px über den rechten Canvasrand hinaus und sind angeschnitten; 5 und 10 passen.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `15` | rechts 2px |
| ausserhalb des Canvas | `20` | rechts 4px |
| ausserhalb des Canvas | `25` | rechts 6px |
| ausserhalb des Canvas | `30` | rechts 8px |

### `par-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#par-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#par-canvas)

*Widget: 📈 Gerade f(x)=a⋅x+b — Achsenschnitte erkunden*

Fünf Überlappungen: «y» unter «g(x) = …», und «x = −0.41»/«x = 2.41» liegen auf den x-Achsenzahlen −1 … 4.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `1  ⇄  x = −0.41` | 0.8 |
| Text über Text | `2  ⇄  x = −0.41` | 0.8 |
| Text über Text | `3  ⇄  x = 2.41` | 0.82 |
| Text über Text | `4  ⇄  x = 2.41` | 0.8 |
| Text über Text | `y  ⇄  g(x) = (x − 1)² + −2` | 0.91 |

### `schn1-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#schn1-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#schn1-canvas)

«g(x) = −x + 5» ragt 46 px links hinaus, «f(x) = 2·x − 4» 3 px oben.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `f(x) = 2·x − 4` | oben 3px |
| ausserhalb des Canvas | `g(x) = −x + 5` | links 46px |
| Text auf Grafikelement | `1` | 0.34 |

### `ks-canvas` — g3-2-lineare-funktionen

[→ http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#ks-canvas](http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#ks-canvas)

Alle Achsenzahlen fehlen: 24 von 29 Beschriftungen liegen ausserhalb des Canvas (y-Zahlen 12–13 px links, x-Zahlen unterhalb). Ursache unten §2.1. Zusätzlich bleibt vom generischen «y» ein Rest neben «K [CHF]» stehen.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `1` | links 12px |
| ausserhalb des Canvas | `3` | links 13px |
| ausserhalb des Canvas | `5` | links 13px |
| ausserhalb des Canvas | `7` | links 13px |
| ausserhalb des Canvas | `9` | links 13px |
| ausserhalb des Canvas | `11` | links 20px |
| ausserhalb des Canvas | … weitere 18 gleichartige | |
| Rest einer überdeckten Beschriftung | `x` | 0.08 |
| Rest einer überdeckten Beschriftung | `y` | 0.07 |
| Text über Text | `1  ⇄  0` | 0.43 |
| Text über Text | `5  ⇄  5` | 0.86 |
| Text über Text | `9  ⇄  10` | 0.43 |
| Text über Text | `11  ⇄  10` | 0.4 |
| Text über Text | `15  ⇄  15` | 0.93 |
| Text über Text | `19  ⇄  20` | 0.43 |
| Text über Text | … weitere 4 gleichartige | |

### `dr-canvas` — g3-3-quadratische-funktionen

[→ http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#dr-canvas](http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#dr-canvas)

«S(1 | -2)» und «(0 | -1.5)» liegen übereinander.

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `-1` | 0.37 |
| Text über Text | `S(1 \| -2)  ⇄  (0 \| -1.5)` | 0.31 |

### `ws-canvas` — g3-3-quadratische-funktionen

[→ http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#ws-canvas](http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#ws-canvas)

Alle Achsenzahlen fehlen (8 von 14 ausserhalb). «h [m]»/«x [m]» tragen je einen Rest des generischen Labels.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `1` | links 12px |
| ausserhalb des Canvas | `3` | links 13px |
| ausserhalb des Canvas | `5` | links 13px |
| ausserhalb des Canvas | `1` | links 11px |
| ausserhalb des Canvas | `2` | links 12px |
| ausserhalb des Canvas | `3` | links 12px |
| ausserhalb des Canvas | … weitere 2 gleichartige | |
| Rest einer überdeckten Beschriftung | `x` | 0.05 |
| Rest einer überdeckten Beschriftung | `y` | 0.09 |
| Text über Text | `1  ⇄  1` | 0.83 |
| Text über Text | `3  ⇄  3` | 0.86 |
| Text über Text | `5  ⇄  5` | 0.86 |

### `sl-canvas` — g4-3-masszahlen

[→ http://localhost:8001/grundlagen/g4-3-masszahlen.html#sl-canvas](http://localhost:8001/grundlagen/g4-3-masszahlen.html#sl-canvas)

«Klasse A» und «Klasse B» sind links um 13 px abgeschnitten, die zwei «MW = 4.50 · Spannweite …»-Zeilen rechts um 10 px. Die untere kollidiert zusätzlich mit der Achsenbeschriftung «Note».

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `Klasse A` | links 13px |
| ausserhalb des Canvas | `Klasse B` | links 13px |
| ausserhalb des Canvas | `MW = 4.50  ·  Spannweite = 1.0` | rechts 10px |
| ausserhalb des Canvas | `MW = 4.50  ·  Spannweite = 4.0` | rechts 10px |
| Text über Text | `Note  ⇄  MW = 4.50  ·  Spannweite = 4.0` | 0.67 |

### `cv-umfang` — g5-2c-kreis-und-kreisteile

[→ http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#cv-umfang](http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#cv-umfang)

«3·d» und «π·d» liegen übereinander.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `3·d  ⇄  π·d` | 0.27 |

### `cv-cossatz` — g5-3-trigonometrische-berechnungen

[→ http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-cossatz](http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-cossatz)

«α=60°» ragt 27 px über den linken Rand hinaus — nur «0°» bleibt sichtbar.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `α=60°` | links 26px |

### `cv-flaeche` — g5-3-trigonometrische-berechnungen

[→ http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-flaeche](http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-flaeche)

«φ=55°» ragt 21 px über den linken Rand hinaus.

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `φ=55°` | links 21px |

### `cv-schiff` — g5-4-einheitskreis

[→ http://localhost:8001/grundlagen/g5-4-einheitskreis.html#cv-schiff](http://localhost:8001/grundlagen/g5-4-einheitskreis.html#cv-schiff)

«φ» und «+0.71» liegen übereinander, ebenso «S» und «Quadrant I».

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `S  ⇄  Quadrant I` | 0.94 |
| Text über Text | `φ  ⇄  +0.71` | 0.6 |

### `a1-canvas` — s2-2a-potenz-wurzel-rationale-gleichungen

[→ http://localhost:8001/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html#a1-canvas](http://localhost:8001/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html#a1-canvas)

Schwerster Fall: die x-Achse trägt bei dieser Skalierung so viele Ticks, dass die Zahlen zu einem unlesbaren Band verschmelzen (60 Überlappungspaare).

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `-27` | links 2px |
| Text auf Grafikelement | `-22` | 0.25 |
| Text auf Grafikelement | `-21` | 0.31 |
| Text auf Grafikelement | `-17` | 0.28 |
| Text auf Grafikelement | `-14` | 0.26 |
| Text auf Grafikelement | `1` | 0.35 |
| Text auf Grafikelement | `12` | 0.27 |
| Text auf Grafikelement | … weitere 2 gleichartige | |
| Text über Text | `-27  ⇄  -26` | 0.64 |
| Text über Text | `-27  ⇄  -25` | 0.28 |
| Text über Text | `-26  ⇄  -25` | 0.64 |
| Text über Text | `-26  ⇄  -24` | 0.28 |
| Text über Text | `-25  ⇄  -24` | 0.64 |
| Text über Text | `-25  ⇄  -23` | 0.28 |
| Text über Text | … weitere 54 gleichartige | |

### `sw-canvas` — s2-2a-potenz-wurzel-rationale-gleichungen

[→ http://localhost:8001/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html#sw-canvas](http://localhost:8001/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html#sw-canvas)

«s [km]» und «100 km» liegen übereinander.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `s [km]  ⇄  100 km` | 0.36 |

### `ba-canvas` — s3-2a-potenzfunktionen

[→ http://localhost:8001/schwerpunkt/s3-2a-potenzfunktionen.html#ba-canvas](http://localhost:8001/schwerpunkt/s3-2a-potenzfunktionen.html#ba-canvas)

«V [dm³]» und «platzt (150 dm³)» liegen zu 73 % übereinander.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `V [dm³]  ⇄  platzt (150 dm³)` | 0.73 |

### `wa-canvas` — s3-6-betragsfunktionen

[→ http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#wa-canvas](http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#wa-canvas)

«Boden = 5» liegt auf der y-Achsenzahl 6.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `6  ⇄  Boden = 5` | 0.32 |

---

## 4. Mittel — Beschriftung liegt störend auf einem Grafikelement

Lesbar, aber die Beschriftung sitzt auf einer Linie, Kurve oder Fläche. — **29 Animationen**.

### `cv-binomi` — g1-3-algebraische-terme

[→ http://localhost:8001/grundlagen/g1-3-algebraische-terme.html#cv-binomi](http://localhost:8001/grundlagen/g1-3-algebraische-terme.html#cv-binomi)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `a·b = 10` | 0.31 |

### `cv-ungl` — g2-1-grundlagen

[→ http://localhost:8001/grundlagen/g2-1-grundlagen.html#cv-ungl](http://localhost:8001/grundlagen/g2-1-grundlagen.html#cv-ungl)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `0` | 0.53 |
| Text auf Grafikelement | `30` | 0.58 |

### `cv-faelle` — g2-2a-lineare-gleichungen

[→ http://localhost:8001/grundlagen/g2-2a-lineare-gleichungen.html#cv-faelle](http://localhost:8001/grundlagen/g2-2a-lineare-gleichungen.html#cv-faelle)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `S(3 \| 11)` | 0.34 |

### `cv-pk` — g2-2b-quadratische-gleichungen

[→ http://localhost:8001/grundlagen/g2-2b-quadratische-gleichungen.html#cv-pk](http://localhost:8001/grundlagen/g2-2b-quadratische-gleichungen.html#cv-pk)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `-20` | 0.36 |
| Text auf Grafikelement | `0` | 0.47 |
| Text auf Grafikelement | `20` | 0.47 |
| Text auf Grafikelement | `40` | 0.44 |

### `ach1-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#ach1-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#ach1-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| ausserhalb des Canvas | `f(x) = 2·x − 6` | oben 3px |
| Text über Text | `4  ⇄  (3 \| 0)` | 0.41 |

### `einstieg-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#einstieg-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#einstieg-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `10` | 0.27 |
| Text über Text | `t [s]  ⇄  10` | 0.68 |

### `lin-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#lin-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#lin-canvas)

*Widget: 📈 Gerade f(x)=a⋅x+b — Achsenschnitte erkunden*

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `3  ⇄  x₀ = 2` | 0.82 |

### `schn-canvas` — g3-1-grundlagen

[→ http://localhost:8001/grundlagen/g3-1-grundlagen.html#schn-canvas](http://localhost:8001/grundlagen/g3-1-grundlagen.html#schn-canvas)

*Widget: 📈 Gerade f(x)=a⋅x+b — Achsenschnitte erkunden*

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `1` | 0.34 |

### `cv-steig` — g3-2-lineare-funktionen

[→ http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#cv-steig](http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#cv-steig)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `P` | 0.44 |
| Text auf Grafikelement | `Q` | 0.35 |
| Rest einer überdeckten Beschriftung | `3` | 0.28 |
| Rest einer überdeckten Beschriftung | `-1` | 0.27 |

### `disk-canvas` — g3-3-quadratische-funktionen

[→ http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#disk-canvas](http://localhost:8001/grundlagen/g3-3-quadratische-funktionen.html#disk-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `-1` | 0.39 |
| Rest einer überdeckten Beschriftung | `-1` | 0.4 |

### `cv-anw` — g5-2a-dreiecke

[→ http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-anw](http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-anw)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `30°` | 0.44 |

### `cv-elem` — g5-2a-dreiecke

[→ http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-elem](http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-elem)

A, B, C und H liegen auf den Höhenlinien bzw. auf dem Höhenschnittpunkt.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `A` | 0.42 |
| Text auf Grafikelement | `B` | 0.25 |
| Text auf Grafikelement | `C` | 0.26 |
| Text auf Grafikelement | `H` | 0.47 |

### `cv-pyth` — g5-2a-dreiecke

[→ http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-pyth](http://localhost:8001/grundlagen/g5-2a-dreiecke.html#cv-pyth)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `F` | 0.38 |
| Rest einer überdeckten Beschriftung | `a²` | 0.43 |

### `cv-reg` — g5-2b-vierecke

[→ http://localhost:8001/grundlagen/g5-2b-vierecke.html#cv-reg](http://localhost:8001/grundlagen/g5-2b-vierecke.html#cv-reg)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `M` | 0.4 |

### `cv-ring` — g5-2c-kreis-und-kreisteile

[→ http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#cv-ring](http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#cv-ring)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `b` | 0.37 |

### `pizza-canvas` — g5-2c-kreis-und-kreisteile

[→ http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#pizza-canvas](http://localhost:8001/grundlagen/g5-2c-kreis-und-kreisteile.html#pizza-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `r = 15 cm` | 0.3 |

### `cv-strahl` — g5-2d-zentrische-streckung-aehnlichkeit

[→ http://localhost:8001/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html#cv-strahl](http://localhost:8001/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html#cv-strahl)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `A'` | 0.32 |
| Text auf Grafikelement | `B'` | 0.26 |

### `cv-streck` — g5-2d-zentrische-streckung-aehnlichkeit

[→ http://localhost:8001/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html#cv-streck](http://localhost:8001/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html#cv-streck)

A, A', B und C' liegen auf den Dreieckskanten; C' zu 67 %.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `A` | 0.29 |
| Text auf Grafikelement | `B` | 0.26 |
| Text auf Grafikelement | `C` | 0.67 |
| Text auf Grafikelement | `C'` | 0.54 |

### `cv-sinussatz` — g5-3-trigonometrische-berechnungen

[→ http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-sinussatz](http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-sinussatz)

Die Seitenbeschriftungen a, b, c liegen mit 53–76 % ihrer Glyphenfläche direkt auf den Dreiecksseiten.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `a` | 0.76 |
| Text auf Grafikelement | `b` | 0.7 |
| Text auf Grafikelement | `c` | 0.53 |

### `cv-spez` — g5-3-trigonometrische-berechnungen

[→ http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-spez](http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-spez)

«c = √2» liegt zu 58 % auf der Hypotenuse.

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `c = √2` | 0.58 |

### `cv-ssw` — g5-3-trigonometrische-berechnungen

[→ http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-ssw](http://localhost:8001/grundlagen/g5-3-trigonometrische-berechnungen.html#cv-ssw)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `C₂` | 0.45 |

### `cv-sincos` — g5-4-einheitskreis

[→ http://localhost:8001/grundlagen/g5-4-einheitskreis.html#cv-sincos](http://localhost:8001/grundlagen/g5-4-einheitskreis.html#cv-sincos)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `1` | 0.56 |
| Text auf Grafikelement | `1` | 0.33 |
| Rest einer überdeckten Beschriftung | `r = 1` | 0.45 |

### `cv-rechenschieber` — s1-3-logarithmen

[→ http://localhost:8001/schwerpunkt/s1-3-logarithmen.html#cv-rechenschieber](http://localhost:8001/schwerpunkt/s1-3-logarithmen.html#cv-rechenschieber)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `1` | 0.35 |

### `ld-canvas` — s2-2b-exponential-logarithmische-gleichungen

[→ http://localhost:8001/schwerpunkt/s2-2b-exponential-logarithmische-gleichungen.html#ld-canvas](http://localhost:8001/schwerpunkt/s2-2b-exponential-logarithmische-gleichungen.html#ld-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `12` | 0.5 |

### `sp-canvas` — s3-4b-logarithmusfunktionen

[→ http://localhost:8001/schwerpunkt/s3-4b-logarithmusfunktionen.html#sp-canvas](http://localhost:8001/schwerpunkt/s3-4b-logarithmusfunktionen.html#sp-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text über Text | `2  ⇄  (1\|0)` | 0.89 |

### `zy-canvas` — s4-2a-prismen-zylinder

[→ http://localhost:8001/schwerpunkt/s4-2a-prismen-zylinder.html#zy-canvas](http://localhost:8001/schwerpunkt/s4-2a-prismen-zylinder.html#zy-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `r` | 0.3 |

### `ad-canvas` — s4-3a-vektorbegriff-komponenten

[→ http://localhost:8001/schwerpunkt/s4-3a-vektorbegriff-komponenten.html#ad-canvas](http://localhost:8001/schwerpunkt/s4-3a-vektorbegriff-komponenten.html#ad-canvas)

Die Vektornamen a und b liegen auf den Vektorpfeilen (b zu 75 %).

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `a` | 0.44 |
| Text auf Grafikelement | `b` | 0.75 |

### `cv-lot` — s4-3c-geraden

[→ http://localhost:8001/schwerpunkt/s4-3c-geraden.html#cv-lot](http://localhost:8001/schwerpunkt/s4-3c-geraden.html#cv-lot)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `P` | 0.25 |
| Text auf Grafikelement | `F` | 0.45 |

### `dr-canvas` — s4-3c-geraden

[→ http://localhost:8001/schwerpunkt/s4-3c-geraden.html#dr-canvas](http://localhost:8001/schwerpunkt/s4-3c-geraden.html#dr-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Text auf Grafikelement | `1` | 0.35 |

---

## 5. Leicht — Rest einer überdeckten Beschriftung

Kleiner Artefakt-Strich neben einer ersetzten Beschriftung (§2.2). — **6 Animationen**.

### `a2-canvas` — g3-2-lineare-funktionen

[→ http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#a2-canvas](http://localhost:8001/grundlagen/g3-2-lineare-funktionen.html#a2-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `2` | 0.42 |

### `to-canvas` — s2-2c-betrag-polynom-ungleichungen

[→ http://localhost:8001/schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html#to-canvas](http://localhost:8001/schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html#to-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `-5` | 0.11 |
| Rest einer überdeckten Beschriftung | `5` | 0.37 |

### `ug-canvas` — s3-1-grundlagen

[→ http://localhost:8001/schwerpunkt/s3-1-grundlagen.html#ug-canvas](http://localhost:8001/schwerpunkt/s3-1-grundlagen.html#ug-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `2` | 0.45 |

### `tf-canvas` — s3-2b-wurzelfunktionen

[→ http://localhost:8001/schwerpunkt/s3-2b-wurzelfunktionen.html#tf-canvas](http://localhost:8001/schwerpunkt/s3-2b-wurzelfunktionen.html#tf-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `-3` | 0.29 |
| Rest einer überdeckten Beschriftung | `-2` | 0.27 |
| Rest einer überdeckten Beschriftung | `-1` | 0.27 |
| Rest einer überdeckten Beschriftung | `-3` | 0.27 |
| Rest einer überdeckten Beschriftung | `3` | 0.21 |

### `cw-canvas` — s3-6-betragsfunktionen

[→ http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#cw-canvas](http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#cw-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `4` | 0.44 |

### `tr-canvas` — s3-6-betragsfunktionen

[→ http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#tr-canvas](http://localhost:8001/schwerpunkt/s3-6-betragsfunktionen.html#tr-canvas)

| Befund | Beschriftung | Mass |
|---|---|---|
| Rest einer überdeckten Beschriftung | `1` | 0.38 |

---

## 6. Methodenkritik — was dieser Bericht nicht abdeckt

- **Nur die Startposition.** Wer einen Regler zieht oder einen Knopf drückt, kann neue
  Kollisionen erzeugen; geprüft ist ausschliesslich der Zustand nach dem Laden.
- **Nur 1280 px.** Bei 360 px skalieren die Canvas neu, die Verhältnisse verschieben sich.
  Ein zweiter Lauf bei 360 px wäre ein eigener Durchgang.
- **Nur Canvas-Text.** Beschriftungen als HTML/MathJax neben der Grafik sind nicht erfasst.
- Die Grenzwerte (25 % Überdeckung, 1.5 px Rand) sind gesetzt, nicht hergeleitet. Die
  Zahl der auffälligen Canvas ist gegen sie robust: zwischen 20 % und 35 % Schwelle
  ändert sich das Ergebnis um wenige Fälle.
- `4` Canvas zeichnen laufend neu (Animation). Dort ist «Startposition» der erste
  Ruhezustand nach dem Laden, nicht zwingend das erste Bild.

