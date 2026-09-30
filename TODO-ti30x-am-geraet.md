# TODO — was nur das Gerät beantwortet

**Stand: 30. September 2026 — drei von vier Fragen geklärt, von Frage 4 ist ein Rest offen.**

Die Rechner-Clips stützen sich auf das deutsche Handbuch von Texas Instruments (PDF,
68 Seiten) und seit dem 30.09.2026 zusätzlich auf die **Online-Hilfe von TI** zum selben
Gerät. Die Online-Hilfe hat Kapitel, die im PDF fehlen: Gleichungslöser, Matrizen,
Vektoren, Konstanten — **mit Bildschirmfotos der Anzeige**. Link und Rezept in
`HOWTO-clips.md`, Abschnitt «Rechneranzeige». Was auch dort nicht steht, kommt in keinen
Clip — nach der Regel aus `CLAUDE.md`: nichts erfinden, was am Gerät nachgeschlagen
gehört.

---

## 1. Wie sieht die Maske des numerischen Lösers aus? — geklärt am 30.09.2026

**Antwort (Online-Hilfe, Kapitel «Gleichungslöser», mit Bildschirmfotos).** `num-solv`
führt durch fünf Schirme:

1. `□=□` und «Enter equation to solve.» — die Gleichung wird als Ganzes eingetippt,
   links die linke Seite, mit `▶` in das rechte Kästchen.
2. «EDIT VARIABLE IF NEEDED» — für jede Variable der Gleichung ein Wert (`x=…`); der
   Wert der gesuchten Variablen ist der Startwert.
3. «SELECT SOLUTION VAR» — «SOLVE FOR: x a b»: Der Löser löst nach jeder der
   vorkommenden Variablen auf, nicht nur nach `x`.
4. «ENTER SOLUTION BOUNDS» — «SOLVE ON [LOWER,UPPER]:», darunter `LOWER=-1E99` und
   `UPPER=1E99` als Vorgabe, unten die Schaltfläche `SOLVE`.
5. «NUMERIC SOLVER SOLUTION» — z. B. `b=6.208333333`, darunter `LEFT-RIGHT=0`; die
   Umschalttaste macht daraus `b=149/24`.

**Umgesetzt.** `clips/g2-1-ti30x-num-solv-sachaufgabe.json` zeigt diese Abfolge und setzt
die Grenzen 15 und 80 aus der Sache; die erfundene Anzeige `LEFT=`/`RIGHT=` ist weg, ebenso
die falsche Aussage «Der Löser kennt nur x». `clips/s2-2c-ti30x-num-solv.json` zeigt die
Eingabe jetzt ebenfalls als `□=□`.

---

## 2. Was steht im Konstanten-Menü neben dem Zeichen? — geklärt am 30.09.2026

**Antwort (Online-Hilfe, Kapitel «Konstanten», zwei Bildschirmfotos).** Die
Kurzbezeichnungen sind **englisch**, die Einheiten stehen mit Schrägstrich und
hochgestellter Potenz:

| NAMES | UNITS |
|---|---|
| `1:c Speed Light` | `1:c m/s` |
| `2:g GravityAccel` | `2:g m/s²` |
| `3↓h Planck Const` | `3↓h J s` |

Kopfzeile `NAMES UNITS`, das aktive Untermenü invers. Die Werte der Tabelle im
PDF-Handbuch gelten unverändert.

**Umgesetzt.** Die Menü-Szene in `clips/g1-4-ti30x-konstanten.json` zeigt beide
Ansichten.

---

## 3. Kann dieses Modell Matrix und Vektor? — geklärt am 30.09.2026: **Ja**

**Antwort (Online-Hilfe, Kapitel «Matrizen» und «Vektoren», mit Bildschirmfotos).**

- **Matrizen** `[A]`, `[B]`, `[C]`, Zeilen und Spalten je 1 bis 3, dazu `[Ans]`, `[I2]`,
  `[I3]`. Menüs NAMES · MATH · EDIT; MATH enthält `Determinant`, `ᵀ Transpose`,
  `Inverse`, `ref`, `rref`. Erlaubt sind Matrix ± Matrix, Matrix × Matrix,
  Skalar × Matrix, Matrix × Vektor. Editor «MATRIX [A]», «ROWS: 1 2 3», «COLUMNS: 1 2 3».
- **Vektoren** `[u]`, `[v]`, `[w]`, Dimension 1 bis 3. MATH enthält `DotProduct`
  (`DotP(`), `CrossProduct` (`CrossP(`), `norm` (Betrag). Editor «VECTOR [u]»,
  «DIMENSION: 1 2 3».
- Fehlermeldungen dazu: «Invalid Dimension», «Singular matrix».

**Was danach möglich wird.** Rechner-Clips für `s4-3a`–`s4-3d` (Skalarprodukt, Betrag,
Kreuzprodukt, Determinante bei Gleichungssystemen). Das ist ein eigener Auftrag, keine
Gerätefrage mehr.

---

## 4. Was zeigen `poly-solv` und `sys-solv`, wenn es nicht glatt aufgeht? — zum grössten Teil geklärt am 30.09.2026

**`sys-solv`: geklärt.** Die Online-Hilfe sagt: «x, y, and z results are automatically
stored in the x, y, and z variables» und «The system solver solves for a unique solution
or infinite solutions in closed form, or it indicates no solution.» Ihr Bildschirmfoto
zum 3×3-System mit unendlich vielen Lösungen zeigt `INFINITE SOLUTIONS`, danach
`x=4-2y-3z`, `y=y`, `z=z`. Menü: `SYSTEM SOLVER` · `1:2x2 Linear EQs` ·
`2:3x3 Linear Sys`; Ergebnisse unter dem Kopf «LINEAR SYSTEM SOLUTION», je eines pro
Schirm. Eine Anleitung aus Schleswig-Holstein (lernnetz.de, «Taschenrechner im MSA»)
zeigt die 2×2-Maske als `(2)x+(3)y= 12` mit dem Hinweis «Press [+] or [-]»: Das Zeichen
zwischen x- und y-Glied wird mit `+` oder `−` gewählt.
Den Wortlaut der Meldung «keine Lösung» belegt nur das Handbuch des baugleichen
Lösers im TI-36X Pro: «No Solution Found». Er steht darum in keinem Clip.

**`poly-solv`: fast geklärt.** Menü `POLY SOLVER` · `1:ax²+bx+c=0` ·
`2:ax³+bx²+cx+d=0`; die Koeffizienten einzeln (`a=`, `b=`, `c=`), negative Zahlen
hochgestellt (`b=⁻2`); danach `x1=…` und `x2=…` je auf einem Schirm, auf Wunsch
Speichern und die Scheitelform `a(x-h)²+k=0`. **Komplexe Lösungen zeigt er an**:
Beispiel der Online-Hilfe \(x^2 - 2x + 2 = 0\) ergibt `x1=1+i`, `x2=1-i`; ein Forumsfall
(mathelounge.de) zeigt für \(x^2 + x + 1 = 0\) `x1=-1/2+0.8660254038i`. Die Umschalttaste
«toggle[s] the number format of the solutions».

**Noch offen — am Gerät nachsehen:**
1. Zeigt `poly-solv` bei \(x^2 - 4x - 1 = 0\) die Wurzelform \(2 \pm \sqrt{5}\) oder nur
   \(4.236\ldots\)? (Die Online-Hilfe zeigt nur ganzzahlige und komplexe Beispiele; das
   Forumsbeispiel mit \(0.866\ldots\) statt \(\sqrt{3}/2\) spricht eher für Dezimalzahlen.)
2. Erscheinen die komplexen Lösungen auch im Modus REAL, oder nur in a+bi? Beide Quellen
   nennen den Modus nicht. Die Clips sagen darum nur: Bei \(D < 0\) zeigt der Löser
   Lösungen mit \(i\).

**Umgesetzt.** `clips/g2-3-ti30x-sys-solv.json` nennt wieder die Ablage in `x`/`y` und
die Meldung `INFINITE SOLUTIONS`, Menü und Maske nach den Fotos.
`clips/g2-2b-ti30x-poly-solv.json` zeigt Menü und Einzelabfrage nach den Fotos und sagt,
dass bei \(D < 0\) Lösungen mit \(i\) erscheinen. `clips/g2-2b-ti30x-real-oder-i.json`
schränkt «ein i heisst falscher Modus» aufs Wurzelziehen ein. Die Warnkästen in
`leitprogramme/gleichungssysteme.html` und `leitprogramme/quadratische-gleichungen.html`
sind nachgeführt.

---

## Wenn eine Frage beantwortet ist

1. Antwort hier eintragen, Überschrift auf `— geklärt am TT.MM.JJJJ` ändern.
2. Den genannten Clip anpassen und nach `HOWTO-clips.md` neu bauen — erst
   `build-clip-ton.py`, dann `build-clips.py`, dann `build-clips-einbau.py`.
3. Die belegte Angabe in `HOWTO-clips.md` unter «Was am TI-30X Pro MathPrint belegt
   ist» ergänzen, damit sie beim nächsten Clip nicht wieder nachgeschlagen wird.
4. Ist auch der Rest von Frage 4 geklärt, wird die Datei gelöscht — der Beleg steht dann in
   `HOWTO-clips.md` und in der Git-Geschichte.
