# TODO — übergrosse Animationen (Stand 03.10.2026)

Gemessen am 03.10.2026 mit Physiks Kriterium aus dessen `STYLEGUIDE.md` §5.11
«Bild neben Bedienung»: **Bedienung und Zeichnung zusammen (Hüllkasten) bei 1280 × 720
höher als rund 650 px** — dann sieht man beim Bedienen die Zeichnung nicht mehr.
Gemessen wurden alle 135 Animationen mit Zeichnung auf den 47 Themenseiten;
**13 liegen darüber**, 20 weitere liegen zwischen 560 und 650 px.

Die Liste ist zur **Direktbeurteilung** da: Jeder Eintrag springt auf die Animation.
Reihenfolge nach Höhe, die schwersten zuerst. Beurteilt wird am besten in einem Fenster
von 1280 × 720 — bei einem höheren Fenster fällt nichts auf.

Noch nichts entschieden und nichts geändert. Mathes `style.css` kennt `anim-layout` an
2 Stellen (Rudiment), Physiks an 22.

---

## A · Zwei verschiedene Probleme

**A1 — «Drei Darstellungen»-Widgets (5 Stück, die schwersten).** Wertetabelle *neben*
Graph, darüber Regler und Formelzeile. Die Breite ist schon verbraucht; die Bedienung
nach rechts zu schieben spart rund 60 px und bringt 814 px nicht unter 650.
Was dort hilft, ist ein anderer Schnitt — etwa die Wertetabelle auf wenige Zeilen kürzen
oder scrollbar machen. **Physiks `.anim-layout` ist hier nicht die Antwort.**

**A2 — eine Zeichnung mit Reglerzeile darüber (8 Stück).** Genau Physiks Fall.
`.anim-layout` aus `tals-physik/style.css` übernehmen (22 Treffer dort), Markup nach
dessen §5.11, Umbruch unter 1100 px einspaltig.

---

## B · Über der Schwelle (13)

1. **814 px** · Interaktive Darstellungen f(x)=a⋅(x−u)2+v · alle drei Darstellun  
   https://mathe.begreifbar.ch/grundlagen/g3-3-quadratische-funktionen.html#anim-darstellungen  
   Zeichnung 438 px · 3 Regler · Form: Drei Darstellungen
2. **783 px** · Drei analytische Verfahren am Beispiel {2⋅x+y=7x−y=−1  
   https://mathe.begreifbar.ch/grundlagen/g2-3-lineare-gleichungssysteme.html#anim-verfahren  
   Zeichnung 464 px · 0 Regler · Form: Drei Darstellungen
3. **778 px** · Interaktive Darstellungen: f(x)=a⋅xn  
   https://mathe.begreifbar.ch/schwerpunkt/s3-2a-potenzfunktionen.html#anim-darstellungen  
   Zeichnung 463 px · 3 Regler · Form: Drei Darstellungen
4. **767 px** · Interaktive Darstellungen  
   https://mathe.begreifbar.ch/grundlagen/g3-2-lineare-funktionen.html#anim-darstellungen  
   Zeichnung 463 px · 3 Regler · Form: Drei Darstellungen
5. **762 px** · Linearfaktor-Baukasten: f(x)=a(x−x1)(x−x2)(x−x3)  
   https://mathe.begreifbar.ch/schwerpunkt/s3-3-polynomfunktionen.html#anim-linearfaktoren  
   Zeichnung 418 px · 4 Regler · Form: Drei Darstellungen
6. **745 px** · Verschobene Hyperbel: y=1(x−u)p+v  
   https://mathe.begreifbar.ch/schwerpunkt/s3-2a-potenzfunktionen.html#anim-hyperbel  
   Zeichnung 418 px · 2 Regler · Form: eine Zeichnung
7. **716 px** · Die drei Lösungsfälle im Geradenbüschel  
   https://mathe.begreifbar.ch/grundlagen/g2-3-lineare-gleichungssysteme.html#anim-bueschel  
   Zeichnung 300 px · 3 Regler · Form: eine Zeichnung
8. **710 px** · 📊 Vorzeichentabellen-Labor: (x−a)(x−b)≷0  
   https://mathe.begreifbar.ch/schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html#anim-vorzeichentabelle  
   Zeichnung 200 px · 2 Regler · Form: eine Zeichnung
9. **709 px** · Spiegelung an der Winkelhalbierenden: y=xn ↔ y=xn  
   https://mathe.begreifbar.ch/schwerpunkt/s3-2b-wurzelfunktionen.html#anim-spiegelung  
   Zeichnung 418 px · 1 Regler · Form: eine Zeichnung
10. **706 px** · Vertikaltest: Funktion oder nicht?  
   https://mathe.begreifbar.ch/grundlagen/g3-1-grundlagen.html#anim-vertikaltest  
   Zeichnung 460 px · 1 Regler · Form: eine Zeichnung
11. **687 px** · 📐 Diskriminante visualisieren  
   https://mathe.begreifbar.ch/grundlagen/g3-3-quadratische-funktionen.html#anim-diskriminante  
   Zeichnung 463 px · 1 Regler · Form: eine Zeichnung
12. **668 px** · Wurzelgleichung grafisch: x+23=c  
   https://mathe.begreifbar.ch/schwerpunkt/s3-2b-wurzelfunktionen.html#anim-wurzelgleichung  
   Zeichnung 418 px · 1 Regler · Form: eine Zeichnung
13. **653 px** · Steigungsdreieck zum Ziehen  
   https://mathe.begreifbar.ch/grundlagen/g3-2-lineare-funktionen.html#anim-steigungsdreieck  
   Zeichnung 458 px · 0 Regler · Form: eine Zeichnung

---

## C · Zwischen 560 und 650 px — mitbeurteilen, wenn A2 angefasst wird (20)

- **648 px** · Spiegelung an der Winkelhalbierenden: ax↔loga⁡x  
   https://mathe.begreifbar.ch/schwerpunkt/s3-4b-logarithmusfunktionen.html#anim-spiegelung  
   Zeichnung 418 px · 0 Regler · Form: eine Zeichnung
- **636 px** · Beispiel: x2−6⋅x+k=0  
   https://mathe.begreifbar.ch/grundlagen/g2-2b-quadratische-gleichungen.html#anim-parameter-k  
   Zeichnung 240 px · 1 Regler · Form: eine Zeichnung
- **630 px** · Drei Darstellungen: 2⋅x−3=5 Schiebe x. Die Wertetabelle zeigt li  
   https://mathe.begreifbar.ch/grundlagen/g2-2a-lineare-gleichungen.html#anim-darstellungen  
   Zeichnung 240 px · 1 Regler · Form: Drei Darstellungen
- **616 px** · Winkel-Labor — Skalarprodukt live  
   https://mathe.begreifbar.ch/schwerpunkt/s4-3b-skalarprodukt.html#anim-winkel-labor  
   Zeichnung 240 px · 1 Regler · Form: eine Zeichnung
- **604 px** · Polarform in allen vier Quadranten  
   https://mathe.begreifbar.ch/schwerpunkt/s4-3a-vektorbegriff-komponenten.html#anim-polarform  
   Zeichnung 300 px · 2 Regler · Form: eine Zeichnung
- **592 px** · Raumwinkel am Würfel  
   https://mathe.begreifbar.ch/schwerpunkt/s4-1-grundlagen.html#anim-raumwinkel  
   Zeichnung 300 px · 1 Regler · Form: eine Zeichnung
- **591 px** · Einheitskreis-Abrollung: x↦sin⁡x, cos⁡x, tan⁡x  
   https://mathe.begreifbar.ch/schwerpunkt/s3-5-trigonometrische-funktionen.html#anim-einheitskreis  
   Zeichnung 300 px · 1 Regler · Form: eine Zeichnung
- **584 px** · Drei Lösungsfälle · Lagebeziehung zweier Geraden  
   https://mathe.begreifbar.ch/grundlagen/g2-3-lineare-gleichungssysteme.html#anim-loesungsfaelle  
   Zeichnung 558 px · 0 Regler · Form: eine Zeichnung
- **583 px** · Pultdach im Schrägbild  
   https://mathe.begreifbar.ch/schwerpunkt/s4-3d-ebenen.html#anim-pultdach-schraegbild  
   Zeichnung 300 px · 1 Regler · Form: eine Zeichnung
- **581 px** · Transformations-Baukasten: y=a⋅sin⁡(b(x−u))+v  
   https://mathe.begreifbar.ch/schwerpunkt/s3-5-trigonometrische-funktionen.html#anim-baukasten  
   Zeichnung 240 px · 4 Regler · Form: Drei Darstellungen
- **579 px** · Faktor-Kacheln: Potenzgesetze P1 und P2  
   https://mathe.begreifbar.ch/grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html#anim-faktor-kacheln  
   Zeichnung 242 px · 2 Regler · Form: eine Zeichnung
- **576 px** · Pol-Falle bei Bruchgleichungen: 6x−n=3xx−n  
   https://mathe.begreifbar.ch/schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html#anim-pol-falle  
   Zeichnung 280 px · 1 Regler · Form: eine Zeichnung
- **575 px** · Interaktive Darstellungen: f(x)=ax  
   https://mathe.begreifbar.ch/schwerpunkt/s3-4a-exponentialfunktionen.html#anim-darstellungen  
   Zeichnung 260 px · 2 Regler · Form: Drei Darstellungen
- **572 px** · Betrags-Explorer  
   https://mathe.begreifbar.ch/schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html#anim-betrags-explorer  
   Zeichnung 280 px · 1 Regler · Form: eine Zeichnung
- **564 px** · Verschobene Exponentialkurve: y=ax−u+v  
   https://mathe.begreifbar.ch/schwerpunkt/s3-4a-exponentialfunktionen.html#anim-verschiebung  
   Zeichnung 240 px · 2 Regler · Form: eine Zeichnung
- **562 px** · Kugelteil im Querschnitt  
   https://mathe.begreifbar.ch/schwerpunkt/s4-2c-kugel.html#anim-kugelteil  
   Zeichnung 270 px · 1 Regler · Form: eine Zeichnung
- **561 px** · Flächenmodell: quadratische Ergänzung von x2+p⋅x  
   https://mathe.begreifbar.ch/grundlagen/g2-2b-quadratische-gleichungen.html#anim-flaechenmodell  
   Zeichnung 362 px · 2 Regler · Form: eine Zeichnung
- **561 px** · Verschobene Logarithmuskurve: y=loga⁡(x−u)+v  
   https://mathe.begreifbar.ch/schwerpunkt/s3-4b-logarithmusfunktionen.html#anim-verschiebung  
   Zeichnung 240 px · 2 Regler · Form: eine Zeichnung

---

## D · Wie gemessen wurde

Playwright, 1280 × 720, je `.widget`: Hüllkasten aus allen sichtbaren Zeichnungen
(`canvas`/`svg` ab 80 px Höhe) **und** allen Bedienelementen ausserhalb von `<details>`
(`.sl-row`, `.graf-btn-row`, `.typ-btn`, `.eingabe-row`, Regler, Knöpfe, Eingaben).
Die aufklappbaren Kästen «Worauf achten?» und «Erkenntnis» zählen **nicht** mit — eine
erste Messung tat es und kam auf zu hohe Werte.

Gesamtbild: 135 Animationen mit Zeichnung, Median 496 px,
höchste 814 px, niedrigste 262 px.

Das Messwerkzeug war Wegwerf und ist gelöscht; die Messung lässt sich mit einem
Playwright-Skript nach dieser Beschreibung in wenigen Minuten wiederholen.
