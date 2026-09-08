# TODO — drei Fragen, die nur das Gerät beantwortet

**Stand: 8. September 2026 — offen.**

Die 22 Rechner-Clips stützen sich ausnahmslos auf das deutsche Handbuch von Texas
Instruments (68 Seiten, Link und Rezept in `HOWTO-clips.md`, Abschnitt
«Rechneranzeige»). Drei Dinge stehen dort **nicht**, und darum kommen sie in keinem
Clip vor — nach der Regel aus `CLAUDE.md`: nichts erfinden, was am Gerät nachgeschlagen
gehört.

Alle drei lassen sich mit dem TI-30X Pro MathPrint in der Hand in wenigen Minuten
klären. Wer das tut, trägt die Antwort hier ein und baut den jeweils genannten Clip
nach — jede Antwort ist genau einen Schritt von einem besseren Clip entfernt.

---

## 1. Wie sieht die Maske des numerischen Lösers aus, wenn er nach Grenzen fragt?

**Was belegt ist.** Die Fehlerliste des Handbuchs nennt zwei Meldungen, die es nur
geben kann, wenn `num-solv` eine untere und eine obere Grenze kennt:

> **Bad Guess** — «Dieser Fehler wird angezeigt, wenn der Variableneintrag für die
> Variable ‚solve for‘ im numerischen Gleichungslöser **ausserhalb der eingegebenen
> unteren und oberen Grenze** liegt.»
>
> **Bounds: Enter LOWER<UPPER** — «… wenn der Eintrag für die untere Grenze grösser ist
> als der für die obere bei: Normalcdf-Verteilungen · **begrenzte Lösungsfindung des
> numerischen Gleichungslösers**.»

**Was fehlt.** Das Handbuch hat **kein Kapitel zum Gleichungslöser** — weder zu
`num-solv` noch zu `poly-solv` oder `sys-solv`. Wie die Eingabemaske aussieht, in
welcher Zeile die Grenzen stehen, wie sie heissen und wie man dorthin kommt, steht
nirgends. Die bestehenden Clips zeigen darum nur `LEFT=`, `RIGHT=` und den Startwert.

**Nachsehen:** `2nd` → `num-solv`, eine Gleichung eintippen, mit den Pfeiltasten nach
unten blättern. Notieren: Zeilenbeschriftungen, Reihenfolge, Standardwerte.

**Was danach möglich wird.** `clips/g2-1-ti30x-num-solv-sachaufgabe.json` sagt heute
«Startwert zwischen die beiden Anfangstemperaturen». Mit der Maske liesse sich daraus
das Stärkere machen: die **Schranke setzen** statt den Startwert raten — genau das, was
die Physik der Aufgabe ohnehin hergibt. Eine zusätzliche Szene, kein neuer Clip.

---

## 2. Was steht im Konstanten-Menü neben dem Zeichen?

**Was belegt ist.** Es gibt zwanzig Konstanten in zwei Untermenüs:

> «Beide Untermenüs enthalten die gleichen 20 physikalischen Konstanten. … Das Menü
> **NAMES** zeigt neben dem Zeichen für die Konstante auch eine **Kurzbezeichnung** an.
> Das Menü **UNITS** enthält die gleichen Konstanten wie NAMES, es wird jedoch nur die
> **Masseinheit** angezeigt.»

Die Werte selbst stehen als Tabelle im Handbuch (NIST 2018) und sind in
`clips/g1-4-ti30x-konstanten.json` verwendet.

**Was fehlt.** Der **Wortlaut** der Kurzbezeichnungen (deutsch oder englisch?) und die
**Schreibweise der Einheiten** auf der Anzeige — `m/s`, `m/s^2`, `J*s`, `Js`? Der Clip
zeigt darum nur die Zeichen `c`, `g`, `h` untereinander, was auf dem Bildschirm etwas
leer wirkt.

**Nachsehen:** `2nd` → `constants`, mit `◀`/`▶` zwischen NAMES und UNITS wechseln, mit
`▲`/`▼` durch die Liste blättern. Drei bis vier Einträge abschreiben, genau wie sie
dastehen.

**Was danach möglich wird.** Die Menü-Szene in `clips/g1-4-ti30x-konstanten.json`
bekommt echten Inhalt statt drei einzelner Buchstaben — und die Aussage «in UNITS steht
die Einheit» wird sichtbar statt behauptet.

---

## 3. Kann dieses Modell Matrix und Vektor?

**Was belegt ist — und was daran unklar ist.** Beide Wörter kommen im PDF **nur in
Sammelaufzählungen** vor, nie als eigenes Thema:

- in der Rangfolge-Fussnote: «Editoren wie z. B. in Matrix, Vektor und Gleichungslöser
  ignorieren diese Operatoren …»
- unter `clear`: «Verlässt schnell die folgenden Anwendungen: … Vektor, Matrix,
  numerischer Gleichungslöser …»
- in der Fehlerliste: «**Singular matrix** — wenn versucht wird, den Kehrwert einer
  singulären Matrix zu berechnen.»

**Was dagegen spricht.** Es gibt **kein Kapitel** dazu, und im Inhaltsverzeichnis
fehlen beide. Das kann heissen: Der Text ist Vorlagentext, den TI über mehrere Modelle
hinweg verwendet — oder das Kapitel steht nur im Online-eGuide.

**Nachsehen:** Tastatur und `2nd`-Belegungen nach `matrix` / `vector` absuchen. Falls
vorhanden: welche Formate (2×2, 3×3?), welche Operationen (Determinante, Inverse,
Skalar- und Kreuzprodukt?).

**Was danach möglich wird.** Bei `s4-3a`–`s4-3d` (Vektorbegriff, Skalarprodukt,
Geraden, Ebenen) stehen heute **null Rechner-Clips**, obwohl es die einzigen Seiten
sind, auf denen sich Matrix- und Vektorrechnung am Gerät lohnen würde. Bei einem Ja
wären das drei bis vier weitere Clips; bei einem Nein ist die Frage endgültig erledigt
und gehört hier als «geklärt» vermerkt — das ist genauso wertvoll.

---

## Wenn eine Frage beantwortet ist

1. Antwort hier eintragen, Überschrift auf `— geklärt am TT.MM.JJJJ` ändern.
2. Den genannten Clip anpassen und nach `HOWTO-clips.md` neu bauen — erst
   `build-clip-ton.py`, dann `build-clips.py`, dann `build-clips-einbau.py`.
3. Die belegte Angabe in `HOWTO-clips.md` unter «Was am TI-30X Pro MathPrint belegt
   ist» ergänzen, damit sie beim nächsten Clip nicht wieder nachgeschlagen wird.
4. Sind alle drei geklärt, wandert die Datei nach dem Muster von
   `TODO-malpunkt-als-trennzeichen.md` auf «abgearbeitet» und bleibt als Beleg stehen.
