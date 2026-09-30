# TODO — Prüfung Lerngebiet G2 (Stand 29.09.2026)

**Abgearbeitet am 29.09.2026.** Legende: `[x]` erledigt · `[–]` bewusst nicht geändert (Grund dahinter) · `[ ]` offen (keine mehr). 19 Clips sind neu vertont, alle Clips neu gebaut, die Laufzeiten in den Leitprogrammen und in `leitprogramme.html` nachgeführt.

Geprüft auf fachliche und didaktische Richtigkeit:

- **Themenseiten:** `g2-1`, `g2-2a`, `g2-2b`, `g2-3`, `g2-modellieren`, jeweils vollständig inkl. Lösungen, Mini-Checks und Canvas-JS.
- **Clips:** alle 57 Drehbücher dieser Seiten.
- **Leitprogramme:** `quadratische-gleichungen`, `gleichungssysteme` sowie `uebungspruefung-1` Teil C mit 9 Prüfungsclips, abgeglichen mit dem Original-PDF.

Alle Zahlenwerte sind mit `python3` (fractions/sympy) nachgerechnet. **Rechenfehler: keine gefunden.** Alle Lösungsmengen, Definitionsmengen, Parameterfälle, Proben, Canvas-Schnittpunkte und Punktsummen stimmen. Die Befunde betreffen falsche oder zu allgemeine *Aussagen*, Widersprüche zwischen Seite und Clip, didaktische Lücken und Konventionen.

Prio: **HOCH** = Lernende lernen Falsches · **MITTEL** = irreführend, widersprüchlich oder unvollständig · **NIEDRIG** = Kleinigkeit/Konvention.
Zeilennummern gelten für den Stand vom 29.09.2026 (Commit 4bce695).

---

## HOCH

- [x] **g2-1:646**, Fehlerkasten «Multiplizieren mit einem Term». Die Seite sagt, beim Multiplizieren mit \((x-3)\) könnten «echte Lösungen verloren» gehen. Das ist falsch: Multiplizieren kann nur Scheinlösungen *hinzufügen*, Lösungen gehen beim *Dividieren* durch einen Term verloren. Beispiel: \(x+1=5\) hat \(\mathbb{L}=\{4\}\), nach \(\cdot(x-3)\) ist \(\mathbb{L}=\{3,\,4\}\). Der Clip `g2-1-aequivalenzumformungen` (Szene 4) sagt es richtig.
- [x] **g2-3:896**, Fehlerkasten «Variable nur einmal einsetzen». Die Seite sagt, der gefundene Wert dürfe nicht in die umgeformte Gleichung eingesetzt werden, dort komme «nur 0 = 0» heraus. Das ist falsch: \(x=4\) in \(y = 7-2x\) liefert \(y\) korrekt. Die eigenen Widgets (Z. 1667) und der Clip `g2-3-einsetzverfahren` machen genau das. Der echte Fehler ist, den *Ausdruck* in dieselbe Gleichung zurückzusetzen, aus der er stammt; so steht es richtig im Clip, Szene 2. Titel und Text neu fassen.
- [–] **clips/g2-2b-ti30x-real-oder-i.json:136, 157**. Der Clip sagt, im Modus a+bi gebe \(\sqrt{-4}\) das Ergebnis `2i`. Das TI-Handbuch (Kapitel «Komplexe Zahlen») sagt dagegen: «Komplexe Ergebnisse werden nur nach der Eingabe von komplexen Zahlen angezeigt». Die Domain-Liste nennt \(\sqrt{x}\), \(x<0\) ohne Einschränkung auf einen Modus. Hängt das zusammen, fallen auch S4 («ein i im Ergebnis … verstellte Einstellung») und das Merkbild S6. **Am Gerät prüfen**, nach `TODO-ti30x-am-geraet.md` übertragen, bis dahin nicht als belegt behandeln. → **Nicht nötig: Das Handbuch belegt den Clip (Kap. Quadratwurzel: «Bei Modi für komplexe Zahlen wird mit a+bi … die Quadratwurzel eines negativen reellen Werts berechnet»). Der Hinweis «nur nach Eingabe komplexer Zahlen» im Kapitel Komplexe Zahlen gilt nicht für √.**

## MITTEL

### g2-1 Grundlagen

- [x] **Z. 600**, Typentabelle Wurzelgleichung. Es steht nur «\(P(x)\ge 0\)», es fehlt \(R(x)\ge 0\). Im eigenen Beispiel \(\sqrt{x+3}=x-1\) erfüllt der Kandidat \(x\approx-0.56\) die Bedingung \(P\ge0\), ist aber eine Scheinlösung.
- [x] **Z. 606, 654–655, 1301**. Die Definitionsmenge \(\mathbb{D}\) wird benutzt, auf der Seite aber nie eingeführt (nur die Grundmenge, Z. 328).
- [x] **clips/g2-1-textaufgabe-in-gleichung.json:170**. «Probe macht man am Text, nicht an der Gleichung» widerspricht Mini-Check Z. 665 und A5 (Z. 790). Ausserdem nennt der Clip 4 Schritte, die Seite 3 Fragen (Z. 356–365). Angleichen, etwa: «Probe an der Gleichung, Plausibilität am Text». → **Probe angeglichen; 4 Schritte gegen 3 Fragen belassen, kein Widerspruch (die Fragen ①–③ decken nur das Aufstellen ab).**
- [x] **clips/g2-1-aequivalenzumformungen.json:57**. «Alle drei lassen sich rückgängig machen», aufgezählt werden aber vier Umformungen (die Seite sagt vier, Z. 506).
- [x] **clips/g2-1-ti30x-num-solv-sachaufgabe.json:40, 57**. Der Clip behauptet, das Auflösen von \(3(T-15)=2(80-T)\) koste «eine halbe Seite». Es ist linear und in zwei Zeilen gelöst (\(T=41\)). Das untergräbt das Lernziel der Seite; ein Beispiel wählen, bei dem num-solv wirklich hilft, oder den Satz streichen.
- [x] **clips/g3-1-definitions-und-wertemenge.json** auf g2-1 (Z. 889). Der Clip setzt \(f(x)\), Wertemenge und Graph voraus, nichts davon ist auf g2-1 eingeführt. Aus `lektion` für g2-1 nehmen oder durch einen Clip «Definitionsmenge einer Gleichung» ersetzen. → **g2-1 aus `lektion` entfernt. D bleibt D, weil die g3-1-Seite durchgehend D schreibt.**
- [x] **clips/g3-1-definitions-und-wertemenge.json:120**. «Bei einer Wurzel muss stehen bleiben, was darunter steht» ist sinnentstellt. Gemeint: «Was unter der Wurzel steht, darf nicht negativ sein.»

### g2-2a Lineare Gleichungen

- [x] **Z. 314/321 vs. 462–481, 343, 894–896**. Die Normalform ist mit \(a\neq0\) definiert, die Fälle 2 und 3 haben aber \(a=0\). Der Mini-Check (343) nennt \(0\cdot x+b=0\) «keine Gleichung in x mehr», die Fälle behandeln sie doch als Gleichung. Fallunterscheidung an \(a\cdot x=c\) nach dem Umformen festmachen oder die Definition anpassen.
- [x] **Z. 654**. «In beiden Fällen … die kleinere Zahl bleibt die kleinere» gilt nur für den Seitentausch, nicht für \(\cdot(-1)\). Widerspricht der Animation direkt darunter (670) und dem Clip `zeichen-kippt`.
- [x] **clips/g2-2a-zeichen-kippt.json:13/29/39**. Hier steht «die einzige Regel» bzw. «eine einzige Stelle», das Merkbild und die Seite (648) sagen aber zwei Mal bzw. zwei Ausnahmen. Der Clip widerspricht sich selbst.
- [x] **clips/g2-2a-warum-a-ungleich-5.json:201**. Im Merkbild steht «\(x(a-5)=-5b\;(a\neq5)\)». Die Bedingung gehört zur Division bzw. zu \(x=\frac{5b}{5-a}\), nicht zur Gleichung, die für alle \(a\) gilt.
- [x] **Z. 598 vs. 323**. \(b\) ist in der Normalform das Absolutglied (\(x=-b/a\)), in der Parameterform die rechte Seite (\(x=b/a\)). Das führt zu Vorzeichenfehlern; Buchstaben entflechten.
- [x] **Z. 623**. «Drei Fälle:», aufgeführt sind nur zwei. Begründen, warum der Identitätsfall hier nicht auftritt.

### g2-2b Quadratische Gleichungen (Seite)

- [x] **Z. 1142–1150**, A1 «Ordne … den passenden Weg zu». Die Spalte «Empfohlenes Verfahren» ist schon ausgefüllt, die Aufgabe verrät ihre Lösung. Spalte leeren oder als Auswahl gestalten.
- [x] **Z. 986–1012, 1044–1051, 1134**. «Parabel», «Scheitel» und \(S(t\mid-9)\) werden benutzt, eingeführt werden sie erst in g3-3. Kurz einführen oder umformulieren.
- [x] **Z. 1012**. «D > 0: Scheitel unterhalb …» gilt nur für \(a>0\) (\(y_S=-D/(4a)\)). Ergänzen.
- [x] **Z. 1292–1398**. A7 ist als «Vertiefung» markiert, danach folgen A8–A10 als normale Aufgaben. Reihenfolge oder Nummerierung ordnen (Master-Schema: Vertiefung am Ende).
- [x] **Z. 1306**. A7 multipliziert über Kreuz, ohne vorher \(\mathbb{D}=\mathbb{R}\setminus\{0,\,1\}\) anzugeben. Widerspricht dem eigenen Verfahren «Definitionsmenge zuerst» (661, 1419).
- [–] **Z. 1520–1533, 1703–1711, 1760–1769**. Der Clip «Quadratische Gleichungssysteme» behandelt Stoff ohne Abschnitt, Aufgabe oder Lernziel auf der Seite. Entweder den Stoff ergänzen oder den Clip zu g2-3 bzw. an eine passendere Stelle. → **Entscheid Auftraggeber 30.09.2026: Der Clip bleibt vorerst auf g2-2b. Das Leitprogramm Gleichungssysteme verweist in Kapitel 4 darauf; g2-3 behandelt nur lineare Systeme.**

### g2-2b Clips

- [x] **clips/g2-2b-ungleichung-vorzeichenmuster.json:72**. «Produkt minus acht, Summe zwei» für \(x^2+2x-8\). Die Summe der Nullstellen −4 und 2 ist −2. Das wechselt die Vieta-Konvention der Seite und der übrigen Clips (Summe der *Lösungen* = −p).
- [x] **clips/g2-2b-quadratisch-faktorisieren.json:71**. «Summe fünf … Zwei und drei … darum minus zwei und minus drei»: Die Zahlen −2 und −3 haben die Summe −5. Hier sind Lösungen und Klammerzahlen vermischt; eine Konvention durchziehen.
- [x] **clips/g2-2b-ti30x-poly-solv.json:39, 123, 302**. Menüzeilen, Masken, die Bruchanzeige `x1=5/2` und «kann exakt lösen» stehen nicht im Handbuch. «Exakt» ist in `TODO-ti30x-am-geraet.md` Z. 108 schon offen. Bis zur Klärung am Gerät vorsichtiger formulieren. Ausserdem: HOWTO-clips belegt die Taste `=`, der Clip zeigt `enter`. → **«exakt» → «direkt». Menü- und Anzeigedetails bleiben bis zur Klärung am Gerät (TODO-ti30x-am-geraet.md, Frage 4).** **Nachtrag 30.09.2026: jetzt belegt und im Clip wieder genannt, siehe Querschnitt unten.**
- [x] **clips/s2-2a-bruchgleichung-quadratisch.json:76, 111, 159, 220**. \(D\) steht im selben Clip für die Definitionsmenge und für die Diskriminante; die Notiz «erst D der Gleichung, dann D der Aufgabe» ist so kaum verständlich. Definitionsmenge als \(\mathbb{D}\) schreiben.
- [x] **clips/s2-2a-bruchgleichung-quadratisch.json:38, 204, 258**. Die Rückverweise «Bisher fiel das x² immer weg», «Folge eins», «drei Ausgänge der linearen Reihe» laufen auf g2-2b und im Leitprogramm ins Leere. Der erste stimmt nicht einmal für s2-2a, weil Folge 1 dort schon quadratisch wird. Neutral formulieren.

### g2-3 Lineare Gleichungssysteme

- [x] **Z. 906–911**, Strategie-Kasten. Er nennt als «die vier Verfahren» Einsetzen, Gleichsetzen, Addition und Gauss; Abschnitt Z. 427 und der Merksatz Z. 1204 nennen grafisch, Einsetzen, Gleichsetzen und Addition. Gauss ist fakultativ. Angleichen.
- [x] **clips/g2-3-anim-loesungsfaelle.json:76, 92**. «Andere Zahlen vor y: verschiedene Steigungen» ist falsch. Gegenbeispiel: \(x+y=1\) und \(2x+2y=3\) sind parallel. Das Kriterium ist die Proportionalität der Koeffizienten, so steht es richtig auf der Seite (Z. 621).
- [x] **clips/g2-3-ti30x-sys-solv.json:292, 329** (unsicher). Nicht im Handbuch belegt sind zwei Angaben: dass die Ergebnisse in `x`/`y` abgelegt werden, und dass der Rechner «unendlich viele» bzw. «keine» Lösungen meldet. Letzteres ist in `TODO-ti30x-am-geraet.md` offen, Ersteres nicht. Nachtragen. → **neutral gefasst, die Ablage in x/y ist gestrichen; die Klärung am Gerät steht in TODO-ti30x-am-geraet.md, Frage 4.** **Nachtrag 30.09.2026: jetzt belegt und im Clip wieder genannt, siehe Querschnitt unten.**

### g2-modellieren

- [x] **Z. 308 (und 280)**. Der Merksatz «Jede Aufgabe … ist eine Mengenbilanz plus eine Wertbilanz» trifft auf die Zahlenrätsel nicht zu (Bruchrätsel 439, \(n(n+1)=72\), A2.1, \(z\cdot e=14\)). Rätsel ausnehmen: «je eine Gleichung pro Aussage».

### Leitprogramme

- [x] **gleichungssysteme.html:762**. Die Warnbox sagt, `sys-solv` zeige bei nicht eindeutiger Lösung nichts an. Der Clip `g2-3-ti30x-sys-solv` sagt, er melde «unendlich viele» bzw. «keine». Nach der Klärung am Gerät (siehe oben) beide angleichen.
- [x] **quadratische-gleichungen.html:577/585/593/716/782/870**. Die Selbsttests 1a, 1c, 1e, 2c, 3b und 4a sind wörtlich die Beispiele aus dem Text (505, 530, 559, 685, 629, 819). Eigene Zahlen einsetzen; Z. 394 warnt selbst vor Wiedererkennen.
- [x] **gleichungssysteme.html:599–611/688/692/775**. Ebenso: 1a–1d, 2a/2b und 3a (5 P) sind die Textbeispiele.
- [x] **gleichungssysteme.html:471–493**. Das Kapitelziel «löst ein System grafisch» hat kein durchgerechnetes Beispiel, und weder Selbsttest noch Gesamttest enthält eine grafische Aufgabe.
- [x] **gleichungssysteme.html:915**. Die Selbsteinschätzung nennt als Stolperstein das «Additionsverfahren mit Vorbereitung», das im Gesamttest nicht vorkommt (G3 braucht keine Vorbereitung, Z. 883).
- [x] **quadratische-gleichungen.html:842–858, 882–883**. Bruchgleichungen werden nicht eingeführt (nur eine Warnbox, «über Kreuz» nie erklärt), 4d und G9 verlangen sie aber. Ein Beispiel ergänzen.
- [x] **quadratische-gleichungen.html:827–840**. Der Parameter-Abschnitt besteht nur aus Clip und einem Satz; 4c (4 P) und G10 verlangen die volle Fallunterscheidung. Ein Beispiel im Text ergänzen.
- [x] **Beide Leitprogramme**. Es gibt keinen einzigen Link auf die Themenseiten `g2-2b` bzw. `g2-3`. Bei wenigen Punkten fehlt der Weg zur ausführlichen Seite. Prüfen, ob §6.5 das zulässt, und dann ergänzen.

## NIEDRIG

### g2-1
- [x] Z. 421: «\(n\le23.61\)» ist als Schranke falsch gerundet (425/18 = 23.6111…); «≈» oder \(23.6\overline{1}\) schreiben.
- [x] Z. 598, 1293: Beim quadratischen Typ fehlt \(a\neq0\), beim linearen steht es.
- [x] Z. 632, 1343: Das Probe-Widget schreibt «5·2 − 7 = 2·2 + 8» mit echtem «=»; \(\stackrel{?}{=}\) verwenden wie Z. 861.
- [x] clips/g2-1-aequivalenzumformungen.json:
  - «Probe» steht für das Umkehren eines Schritts statt für das Einsetzen.
  - Die Notiz «Vertauschen ist erlaubt» ist rot gefärbt (Rot heisst Fehler).
  - Es steht \(L\) statt \(\mathbb{L}\).
  - \(\mathbb{D}\) wird benutzt, ohne auf der Seite eingeführt zu sein.
- [x] clips/g3-1-definitions-und-wertemenge.json:62: Mengenschreibweise mit «:» statt «|».
- [x] Z. 889–892: In der Clip-Liste steht die Folgenummer «2» doppelt (1, 2, 3, 2), weil der g3-1-Clip seine Nummer mitbringt.

### g2-2a
- [x] Z. 619: «folgendes System», es ist aber eine einzelne Gleichung.
- [x] Z. 670, 1692, clips/g2-2a-anim-vorzeichenkipp.json:21/146: «spiegelt am Nullpunkt» gilt exakt nur für k = −1; «spiegelt (und streckt)».
- [x] Z. 1744/1749: Die Punkte heissen a, b und der Faktor k, das kollidiert mit a, b der Normalform und k als Parameter. → **Punkte heissen u, v; der Faktor k bleibt (Regler, Hinweise und Clip).**
- [x] clips/g2-2a-drei-ausgaenge.json:265: «Nie ‹keine Lösung› schreiben», die Seite nutzt es aber als Knopf (A1, 1624) und im Mini-Check 638.
- [x] Z. 724, 834: Die Mini-Check-Optionen und das Ende von A6 geben \(x>-3\) bzw. \(t>200\) statt \(\mathbb{L}\) als Intervall.
- [x] Z. 861, 834: «Erst ab 10 h lohnt sich …», bei genau 10 h verdient man gleich viel; «bei mehr als».
- [x] Z. 694–697: In der Frage fehlt die Einheit für x.
- [–] Z. 867: Die Seite hat A1–A8, das Master-Schema sieht A1–A6 plus optional A7 vor. → **Nicht nötig: A7 und A8 sind beide Vertiefung und stehen am Ende.**

### g2-2b Seite
- [x] Z. 1166: Der Titel von A2 lautet «Ausklammern und Wurzelziehen», die Aufgabe braucht nur Ausklammern.
- [x] Z. 682: «Vieta» wird verwendet, bevor es in Z. 702 definiert ist.
- [x] Z. 1912: «Mittelstück passt nicht zum Quadrat von 8» ist unklar; der Grund ist, dass 8 keine Quadratzahl ist.
- [x] Z. 1850 (JS `loesungstext`): gerundete Werte stehen als exakte Lösungsmenge («𝕃 = { 0.27, 3.73 }»); «≈» ergänzen.
- [x] Z. 1308, 1313: φ ≈ 0.618 als «Goldener Schnitt», φ steht üblicherweise für 1.618. Z. 1297: «Standardgleichung» ist nie eingeführt.
- [x] Z. 496: \(a\) steht doppelt (u² = a und Leitkoeffizient); in der pq-Herleitung fehlt der Fall \((p/2)^2-q<0\).
- [x] Z. 395, 1111: \(x=\pm\sqrt{c}\) ohne die Bedingung \(c\ge0\) (Z. 1413 hat sie).
- [x] Z. 833: Beim Verfahren für Ungleichungen fehlt der Hinweis auf \(D<0\) (\(\mathbb{L}=\mathbb{R}\) oder \(\{\,\}\)).
- [x] Z. 1025, 2047, 1947: Die Live-Anzeigen trennen «x₁ = 5, x₂ = 1» mit Komma, nach STYLEGUIDE §2.1 gehört ein Strichpunkt hin.

### g2-2b Clips
- [x] clips/g2-2b-quadratisch-b-null.json:128: «Potenzreihe» ist ein Fachbegriff; «Reihe zu den Potenzen».
- [x] clips/g2-2b-anim-velo.json:168: «mit der Lösung v ≈ 18.2»; die zweite Lösung 1.754 und der Grund für ihren Ausschluss fehlen.
- [x] clips/g2-2b-quadratische-ungleichungen.json:241: «eckige Klammer», auch ] [ sind eckig; «Klammer nach innen».
- [x] clips/g2-2b-mitternachtsformel-herleitung.json: «Rechnung aus Folge vier» läuft im Leitprogramm ins Leere.

### g2-3
- [x] Z. 1623–1628, 1738: Das Fenster y ∈ [−3; 8], bei x = −1 ist y₁ = 9, der Punkt liegt dann ausserhalb der Canvas. Der Kommentar «1:1» stimmt nicht (8 gegen 11 Einheiten). → **y-Fenster [−4; 10]. Bei 360 px kreuzt die gestrichelte x = 2 weiterhin das Label «2x + y = 7» (unverändert).**
- [x] Z. 352: «die zwei Gleichungen sind dann äquivalent» gilt nur für 2×2.
- [x] Z. 721: «𝕃 ist eine Gerade»; besser: die Menge aller Punkte einer Geraden.
- [x] Z. 657, clips/g2-3-anim-bueschel.json Szene 3: «parallel» schliesst dort «identisch» ein, anderswo nicht.
- [x] clips/g2-3-anzahl-loesungen.json:228: «Immer beide nach y auflösen» versagt bei senkrechten Geraden (Beispiel 2, k = 0).
- [x] Z. 1096–1100: «Massenbilanz» gegen «Mengenbilanz», obwohl beide Masse bilanzieren; «Gesamtmasse» und «Zinnmasse».
- [x] Z. 1110–1198: Substitution und Parameter (Lernziele 4 und 5) nur in A8/A9 nach der Vertiefung A7. In A1–A6 fehlt Gleichsetzen ganz. → **Reihenfolge erledigt (Vertiefung jetzt A9). Am 30.09.2026 neue A3 «Gleichsetzverfahren anwenden» (𝕃 = {(3 | 4)}), die folgenden Aufgaben sind jetzt A4–A10 (Vertiefung A10). Der Kontrollauftrag in A2 ist wieder entfernt.**
- [x] Z. 8 (SEO): Die Beschreibung nennt Gauss als Inhalt; in `scripts/build-seo.py` (Tabelle `SEITEN`) ändern.
- [x] Die Begriffe schwanken: Einsetzmethode, Einsetzungsverfahren, Einsetzverfahren und Einsetzung (Z. 474, 498, 908, Clips).
- [x] clips/g2-3-anim-verfahren.json:40: «Drei Verfahren», gezeigt werden nur zwei.
- [x] clips/g2-3-additionsverfahren.json:26: Tippfehler «faellt».
- [x] clips/g2-3-drei-variablen.json:178: «zurücksetzen» durch «rückwärts einsetzen» ersetzen.

### g2-modellieren
- [x] Z. 440, 779: Die Definitionsmenge ist unvollständig, es fehlen \(z\neq-4\) bzw. \(z\neq-5\) (Nenner des Originalbruchs).
- [x] Z. 880: «(je mal c in kJ/kg)», die Einheit von c ist kJ/(kg·K).
- [x] Z. 881: «dieselbe Gleichung wie die Stoffbilanz» gilt nur zusammen mit der Mengenbilanz.
- [x] Z. 1124 (Trainer, Aufgabe 5): «Anteile der beiden Sorten» sollte «Massen» heissen, weil «Anteil» auf der Seite den Prozentwert meint.
- [x] clips/g2-M-anim-ansatz-trainer.json Szene 1: Gesprochen heisst es «zu neunundzwanzig Franken», es fehlt «pro Kilogramm».

### Leitprogramme
- [x] quadratische-gleichungen.html:565: «ganzzahlig oder einfache Brüche». Bei a = 1 mit ganzen b, c sind rationale Lösungen immer ganzzahlig.
- [x] quadratische-gleichungen.html:782 (unsicher): 3b erwartet Dezimalwerte, der poly-solv-Clip verspricht exakte Ergebnisse. Hängt an der Klärung am Gerät.
- [x] quadratische-gleichungen.html:397 (unsicher): «drei von vier Gleichungen» ist eine Quote ohne Beleg.
- [x] gleichungssysteme.html:810, quadratische-gleichungen.html:952: Die Verweise auf das jeweils andere Leitprogramm haben keinen Link.
- [x] gleichungssysteme.html:831: Der Text empfiehlt, y aus der linearen Gleichung zu holen, der Clip setzt in die Parabel ein. Vereinheitlichen.
- [x] uebungspruefung-1.html:1165 und clips/pruefung1-c2a-ungleichung-zeichen-drehen.json:166: «Links steht immer eine offene Klammer» gilt nur bei \(-\infty\).
- [x] clips/pruefung1-c2a-ungleichung-zeichen-drehen.json:120: Gesprochen wird «durch minus eins», im Bild steht \(\cdot(-1)\).
- [x] clips/pruefung1-c5 :154, -c6 :183, -c7 :193/228: `\text{— …}` setzt einen Gedankenstrich direkt an die Formel (STYLEGUIDE §2.8).
- [–] uebungspruefung-1.html:426–429 (Entscheid): Die sichtbare Navigation verrät «Scheinlösung» und «zwei/drei Fälle» beim Schreiben des Bogens. → **Entscheid: belassen.**

## Querschnitt (mehrere Dateien, besser per Skript)

- [x] **\(L\) statt \(\mathbb{L}\) in älteren Clips.** Betroffen sind die Nicht-Anim-Clips von g2-1, g2-2a, g2-2b und g2-3 sowie s2-2a (dort auch \(D\) statt \(\mathbb{D}\)). STYLEGUIDE Z. 309 verlangt \(\mathbb{L}\) auch in Clips. Dazu `L = \{ \}` statt `\{\,\}` in `g2-2a-loesungsmenge-intervall.json:148` und `g2-2a-warum-a-ungleich-5.json:147`. Umstellen, danach Clips neu bauen.
- [x] **Trennzeichen in Mengen uneinheitlich**, \(\{0;\,5\}\) gegen \(\{0,\,5\}\) (g2-2b:561, Clip g2-1-aequivalenzumformungen). Der STYLEGUIDE regelt Intervalle (§2.7: `;`), nicht aber aufzählende Mengen. **Entscheid nötig**, dann vereinheitlichen. → **Entscheid: Strichpunkt (STYLEGUIDE §2.1, Z. 40–42, Mehrheit der Site). Umgesetzt nur auf g2-Seiten, g2-Clips und in den beiden Leitprogrammen; der Rest der Site ist nicht geprüft.**
- [x] **Vertiefung A7 mitten in der Aufgabenreihe** auf g2-2b (A8–A10 danach), g2-3 (A8–A9 danach) und g2-2a (bis A8). Einheitliche Regel festlegen.
- [x] **TI-30X-Angaben ohne Handbuchbeleg** (real-oder-i, poly-solv, sys-solv) nach `TODO-ti30x-am-geraet.md` übertragen, soweit nicht schon dort. → **Nachtrag 30.09.2026: Alle Fragen geklärt (TI-Online-Hilfe und Auftraggeber am Gerät), die Datei ist gelöscht. Belegt sind jetzt: sys-solv legt die Ergebnisse in x/y ab und meldet INFINITE SOLUTIONS; poly-solv zeigt Wurzelformen und bei D < 0 Lösungen mit i, auch im Modus REAL. Die Clips sagen das wieder bzw. neu; die neutrale Fassung vom 29.09. ist überholt.**
