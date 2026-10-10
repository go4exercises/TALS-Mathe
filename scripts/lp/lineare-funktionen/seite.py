"""Baut leitprogramme/lineare-funktionen.html aus einer Kapitelbeschreibung (03.10.2026).

  python3 scripts/lp/lineare-funktionen/seite.py

Liest Kopf (inkl. <style>) und Grundskript (Thema, Clip-Karten, Tests, Fortschritt) aus der
bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu.
Beim ersten Lauf gibt es die Seite noch nicht — dann kommen Kopf, Grundskript und Fuss aus
leitprogramme/quadratische-funktionen.html, mit eigenem Titel und eigenen localStorage-
Schlüsseln (HOWTO-leitprogramme §5). Danach ist die eigene Seite die Quelle, damit der
SEO-Block von scripts/build-seo.py erhalten bleibt.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und
python3 scripts/build-seo.py. Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/lineare-funktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/quadratische-funktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Quadratische Funktionen</title>',
                      '<title>Leitprogramm Lineare Funktionen</title>')
    alt = alt.replace('lp-quadfunktionen-', 'lp-linfunktionen-')

kopf = alt[:alt.index('</style>')]
if '\n/* ════════ Lineare Funktionen' in kopf:
    kopf = kopf[:kopf.index('\n/* ════════ Lineare Funktionen')]
if '\n/* ════════ Fassung 3' in kopf:
    kopf = kopf[:kopf.index('\n/* ════════ Fassung 3')]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Quadratische Funktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Lineare Funktionen — Simulationen')) if k > 0)
basis = alt[i:j].replace("' Selbsttests erledigt'", "' Aufgabenblöcken bearbeitet'")
# Footer erzeugt scripts/build-seo.py (seit 10.10.2026): hier nur leere FUSS-Marken; nach dem Bau
# `python3 scripts/build-seo.py` laufen lassen.
fuss = alt[alt.index('<!-- FUSS:ANFANG'):] if '<!-- FUSS:ANFANG' in alt else alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'<!-- FUSS:ANFANG.*?<!-- FUSS:ENDE -->|<footer class="site-footer">.*?</footer>',
              lambda _: '<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n<!-- FUSS:ENDE -->',
              fuss, count=1, flags=re.S)

CSS = '''
/* ════════ Lineare Funktionen (03.10.2026) — Fassung 3 des Kapitelmusters ════════
   Das Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) ist dasselbe wie im
   Leitprogramm Quadratische Funktionen. Eigen sind nur die Farben der Geraden-Bausteine. */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:440px}
.leiste{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:0 0 10px;padding:9px 12px;border-radius:9px;
  background:var(--orange-hell);border:1px solid var(--orange-rand);font-family:var(--sans);font-size:.92rem}
.leiste .ls-nr{font-family:var(--mono);font-size:.78rem;color:var(--orange);font-weight:700}
.leiste .ls-text{flex:1 1 260px;min-width:0}
.leiste .ls-ok{color:var(--gruen);font-weight:700;font-size:1.1rem;min-width:1em}
.leiste .ls-weiter,.leiste .ls-neu{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;
  border:1px solid var(--linie);background:var(--karte);color:var(--tinte-2)}
.leiste.geloest{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.leiste.geloest .ls-weiter{border-color:var(--gruen-rand);color:var(--tinte);font-weight:700}
.leiste.fertig{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.kap-clip{max-width:640px}
.kompetenzen ul{margin:10px 0 0;padding-left:1.25em;font-family:var(--sans);font-size:.92rem}
.kompetenzen li{margin:5px 0}
.kompetenzen .rlp-quelle{font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);margin:8px 0 0}
.kompetenzen .ohm{font-size:.72rem;padding:1px 7px;border-radius:999px;background:var(--orange-hell);border:1px solid var(--orange-rand);white-space:nowrap}
.sim .pfeil{fill:var(--tinte-2)} svg.mini .pfeil{fill:var(--tinte-2)}
.achsname{fill:var(--tinte);font-family:var(--serif);font-style:italic;font-size:12px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
svg.mini .achsname{font-size:10px;stroke-width:3px}
text.p-text{stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.hilfs-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input:disabled{opacity:.35}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sim input[type=range]:disabled{opacity:.4}
/* Farben im ganzen Leitprogramm: blau = m und die Gerade, orange = b und (0 | b),
   grün = Nullstelle und Zielgerade, Tinte = gegebener Punkt. Dieselben Farben tragen
   die Clips (farbe 1/2/3/5) und die Regler (akz-blau, akz-orange). */
.sim .kurve.g2,svg.mini .kurve.g2{stroke:var(--tinte-2)}
.sim .normal{stroke-dasharray:5 4}
.sim .dreieck{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 3;fill:none}
.p-b{fill:var(--orange)} .p-null{fill:var(--gruen)} .p-pkt{fill:var(--tinte)}
.p-m{fill:var(--tinte-2);font-weight:600} .p-g1{fill:var(--blau)}
svg.mini .p-pkt{fill:var(--tinte)} svg.mini .p-b{fill:var(--orange)}
.mini-reihe svg.mini{background:var(--karte)}
/* Ein Punkt direkt hinter einer Formel landet sonst allein auf der naechsten Zeile. */
.nb{white-space:nowrap}
'''


def clipkarte(datei, titel, zeit):
    return f'''<div class="clipkarte kap-clip" data-clip="clips/{datei}.html" data-titel="{titel}">
        <button class="clip-start" type="button">
          <span class="clip-play" aria-hidden="true">▶</span>
          <span class="clip-txt"><span class="clip-titel">{titel}</span></span>
          <span class="clip-zeit">{zeit}</span>
        </button>
      </div>'''


def uebung(typ, titel, bild=False):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          {'<svg class="mini gross ue-bild" role="img" aria-label="Gerade zur Aufgabe"></svg>' if bild else ''}
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(name, var, label, mn, mx, st, val, akz):
    return (f'<div class="sl-grp akz-{akz}"><label for="{name}-{var}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{name}-{var}" data-p="{var}" min="{mn}" max="{mx}" step="{st}" value="{val}">'
            f'<span class="sl-val"></span></div>')


def test(tid, titel, punkte, aufgaben, zwei=True):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte, sum(a[1] for a in aufgaben))
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''


def kapitel(n, kid, titel, komp, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 3.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim}

      <p class="phase"><span>③</span> Kontrollfragen</p>
      {clipkarte(*clip2)}

      <h3>Festhalten</h3>
{festhalten}

      <p class="phase"><span>④</span> Üben mit Rückmeldung</p>
      <div class="duo">
        {ue}
      </div>

      <p class="phase"><span>⑤</span> Aufgaben mit Lösungen</p>
{aufgaben}
      <p class="ausf">Mehr dazu: {mehr}</p>
    </section>'''


TS = '../grundlagen/g3-2-lineare-funktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Gerade mit Steigung m und Achsenabschnitt b, Ursprungsgerade gestrichelt"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien (Ursprungsgerade \\(y = m\\,x\\) und Steigungsdreieck)</label>
        <div class="sl-row">
          {regler('s1', 'm', 'm', -3, 3, 0.5, 2, 'blau')}
          {regler('s1', 'b', 'b', -5, 5, 0.5, 1, 'orange')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Lineare Funktion</div>
          <p>\[ f(x) = m \cdot x + b, \qquad m,\, b \in \mathbb{R} \]</p>
          <p>\(b\) ist der \(y\)-Achsenabschnitt: \(f(0) = b\). Die Gerade schneidet die \(y\)-Achse im Punkt \((0 \mid b)\); \(b\) schiebt sie nur senkrecht — plus hinauf, minus hinunter.</p>
          <p>\(m\) ist die Steigung: ein Schritt nach rechts, \(m\) Schritte hinauf. \(m\) kippt die Gerade um den Punkt \((0 \mid b)\). \(m \gt 0\): steigt; \(m \lt 0\): fällt; \(m = 0\): waagrecht.</p>
          <p><b>Punktprobe:</b> Ob \(P(x_1 \mid y_1)\) auf dem Graphen liegt, entscheidet das Einsetzen: \(f(x_1)\) ausrechnen und mit \(y_1\) vergleichen.</p>
          <p>Definitionsmenge: \(D = \mathbb{R}\), wenn nichts anderes dasteht. In Anwendungen schränkt der Sachverhalt sie ein (etwa \(t \geq 0\)) — dann gehört sie in die Antwort.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(b\) ist nicht die Nullstelle. Bei \(f(x) = 2x - 6\) ist \(b = -6\) der \(y\)-Achsenabschnitt, die Gerade schneidet die \(y\)-Achse also in \((0 \mid -6)\); die Nullstelle liegt bei \(x_0 = 3\) auf der \(x\)-Achse.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 4, r'Welcher Graph gehört zu welcher Funktion? (1) \(f(x) = 2x - 3\) (2) \(g(x) = -x + 2\) (3) \(h(x) = 0.5x\) (4) \(k(x) = -2x - 1\)',
     r'<p>(1) → C, (2) → A, (3) → B, (4) → D.</p><p class="komm">Am schnellsten über \(b\): A schneidet die \(y\)-Achse über dem Ursprung, B genau im Ursprung, C und D darunter. Zwischen C und D entscheidet die Richtung: C steigt, D fällt.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-g="-1,2" data-titel="A"></svg><svg class="mini" data-g="0.5,0" data-titel="B"></svg><svg class="mini" data-g="2,-3" data-titel="C"></svg><svg class="mini" data-g="-2,-1" data-titel="D"></svg></div>'),
    ('1b', 3, 'Gleichung der Geraden? (Punkte auf Gitterpunkten)',
     r'<p>\(b = -1\); von \((0 \mid -1)\) zwei nach rechts und drei hinauf, also \(m = \dfrac{3}{2} = 1.5\): \(f(x) = 1.5x - 1\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-g="1.5,-1" data-fenster="-4,4,-4,4" data-punkte="0,-1;2,2"></svg></div>'),
    ('1c', 2, r'Liegen \(P(4 \mid 5)\) und \(Q(-2 \mid -3)\) auf \(f(x) = 1.5x - 1\)?',
     r'<p>\(f(4) = 5\): \(P\) liegt darauf. \(f(-2) = -4 \neq -3\): \(Q\) nicht.</p>', ''),
    ('1d', 2, r'Warum gehen alle Geraden \(f(x) = m \cdot x + 3\) — unabhängig von \(m\) — durch denselben Punkt?',
     r'<p>Bei \(x = 0\) fällt der ganze \(x\)-Teil weg: \(f(0) = 3\) für jedes \(m\). Alle gehen durch \((0 \mid 3)\); \(m\) kippt sie nur um diesen Punkt.</p>', ''),
    ('1e', 2, r'Zeichne die Graphen von \(f(x) = 1.5x - 2\) und \(g(x) = -x - 1\) in <em>ein</em> Koordinatensystem (Bereich \(-4\) bis \(5\)). Vorgehen: \(b\) auf der \(y\)-Achse eintragen, dann mit einem Steigungsdreieck einen zweiten Punkt suchen.',
     r'<p>\(f\): \((0 \mid -2)\), dann zwei nach rechts und drei hinauf zu \((2 \mid 1)\).</p><p>\(g\): \((0 \mid -1)\), dann einen nach rechts und einen hinunter zu \((1 \mid -2)\).</p><p class="komm">Zwei Punkte genügen — die Gerade durch sie über das ganze Fenster ziehen.</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-g="1.5,-2;-1,-1" data-fenster="-4,5,-4,5" data-punkte="0,-2;2,1;0,-1;1,-2"></svg></div>'),
], zwei=False)
k1 = kapitel(1, 'm-kippt-b-schiebt', 'Die Gerade bewegen: \\(m\\) und \\(b\\)', 'K1; K2', 40,
             r'Du liest aus \(f(x) = m \cdot x + b\) Steigung und Achsenabschnitt ab, zeichnest damit die Gerade — und liest umgekehrt die Gleichung aus dem Graphen.',
             ('g3-2-lp-m-und-b', 'Gerade sehen: m kippt, b schiebt', '1:37'),
             sim1, ('g3-2-lp-kontrolle-m-und-b', 'Kontrollfragen zu m und b', '1:03'),
             fest1, [uebung('mb-lesen', 'm und b ablesen'), uebung('beschreibung-g', 'Beschreibung → Gleichung'),
                     uebung('graf-mb', 'Graph → Gleichung', True)],
             auf1, f'<a href="{TS}#definition">Themenseite 3.2, Definition und Parameter</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Gerade mit Steigungsdreieck und Nullstelle"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien (Steigungsdreieck)</label>
        <div class="sl-row">
          {regler('s2', 'm', 'm', -3, 3, 0.5, 1, 'blau')}
          {regler('s2', 'b', 'b', -5, 5, 0.5, 1, 'orange')}
          {regler('s2', 'dx', '&Delta;x', 1, 6, 0.5, 2, 'grau')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Steigung und Nullstelle</div>
          <p>\[ m = \frac{\Delta y}{\Delta x} = \frac{y_2 - y_1}{x_2 - x_1} \qquad x_0 = -\frac{b}{m} \quad (m \neq 0) \]</p>
          <p>Jedes Steigungsdreieck derselben Geraden gibt dasselbe \(m\) — bei \(m \neq 0\) sind die Dreiecke ähnlich. Bei \(m = 0\) ist \(\Delta y = 0\) für jedes \(\Delta x \neq 0\), der Quotient also ebenfalls immer \(0\). Die Steigung ist ein Verhältnis, kein Abstand.</p>
          <p>Gelesen wird von links nach rechts, also mit <span class="nb">\(\Delta x \gt 0\).</span> Vertauscht man die Punkte, drehen \(\Delta y\) und \(\Delta x\) beide das Vorzeichen — \(m\) bleibt gleich.</p>
          <p>Die <b>Nullstelle</b> \(x_0\) ist die <em>Stelle</em> mit \(f(x_0) = 0\) — eine Zahl. Der zugehörige <em>Punkt</em> \((x_0 \mid 0)\) ist der Schnittpunkt des Graphen mit der \(x\)-Achse. Man findet sie aus \(0 = m x_0 + b\). Bei \(m = 0\) gibt es keine (oder, bei \(b = 0\), unendlich viele).</p>
          <p>Haben <b>zwei verschiedene</b> Punkte dieselbe \(x\)-Koordinate, ist \(\Delta x = 0\): \(m\) ist nicht definiert, die Gerade steht senkrecht und ist keine Funktion. Fallen beide Punkte zusammen, legen sie gar keine Gerade fest — durch einen einzelnen Punkt gehen unendlich viele.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Zähler und Nenner in derselben Reihenfolge abziehen. Für \(A(1 \mid 2)\) und \(B(5 \mid 10)\) ist \(m = \dfrac{10 - 2}{5 - 1} = 2\), nicht \(\dfrac{10 - 2}{1 - 5} = -2\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Steigung der Geraden durch (i) \(A(-4 \mid 5)\), \(B(2 \mid 2)\); (ii) \(A(-1 \mid -4)\), \(B(3 \mid 4)\); (iii) \(A(2 \mid 5)\), \(B(6 \mid 5)\)?',
     r'<p>(i) \(m = \dfrac{-3}{6} = -0.5\); (ii) \(m = \dfrac{8}{4} = 2\); (iii) \(m = \dfrac{0}{4} = 0\), eine waagrechte Gerade.</p>', ''),
    ('2b', 3, r'Nullstellen von \(f(x) = 4x - 6\), \(g(x) = -2x + 8\) und \(h(x) = 0.5x + 3\).',
     r'<p>\(1.5\), \(4\) und \(-6\).</p><p class="komm">Je aus \(0 = m x_0 + b\), also \(x_0 = -\dfrac{b}{m}\).</p>', ''),
    ('2c', 2, r'Lies \(m\), \(b\) und die Nullstelle ab. (Punkte auf Gitterpunkten)',
     r'<p>\(b = 3\), zwei nach rechts und drei hinunter: \(m = -1.5\). Nullstelle \(x_0 = 2\), also \(f(x) = -1.5x + 3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-g="-1.5,3" data-fenster="-3,5,-4,5" data-punkte="0,3;2,0"></svg></div>'),
    ('2d', 2, r'Warum liefert jedes Steigungsdreieck derselben Geraden dasselbe \(m\)?',
     r'<p>Bei \(m \neq 0\) sind alle diese Dreiecke ähnlich: Wird \(\Delta x\) verdoppelt, verdoppelt sich \(\Delta y\) mit. Das Verhältnis \(\Delta y : \Delta x\) bleibt dadurch gleich.</p><p class="komm">Bei \(m = 0\) gibt es kein Dreieck mehr — \(\Delta y\) ist null, und null geteilt durch jedes \(\Delta x \neq 0\) bleibt null.</p>', ''),
    ('2e', 2, r'Zwei <em>verschiedene</em> Punkte haben dieselbe \(x\)-Koordinate. Warum lässt sich keine Steigung angeben — und warum ist die Gerade durch sie keine Funktion? Und was gilt, wenn beide Punkte zusammenfallen?',
     r'<p>\(\Delta x = 0\), und durch null lässt sich nicht teilen: \(m\) ist nicht definiert. Die Gerade steht senkrecht; zu dieser einen Stelle gehören unendlich viele \(y\)-Werte, und eine Funktion ordnet jedem \(x\) genau einen zu.</p><p>Fallen beide Punkte zusammen, gibt es gar keine eindeutige Gerade: Durch einen einzelnen Punkt gehen unendlich viele.</p>', ''),
])
k2 = kapitel(2, 'steigung-messen', 'Die Steigung messen', 'K2', 40,
             r'Du bestimmst \(m\) aus einem Steigungsdreieck und aus zwei Punkten — und findest die Nullstelle.',
             ('g3-2-lp-steigungsdreieck', 'Gerade sehen: jedes Steigungsdreieck gibt dasselbe m', '1:44'),
             sim2, ('g3-2-lp-kontrolle-steigung', 'Kontrollfragen zur Steigung', '0:58'),
             fest2, [uebung('steigung-punkte', 'Steigung aus zwei Punkten'), uebung('nullstelle', 'Nullstelle bestimmen'),
                     uebung('punkt-pruefen', 'Liegt der Punkt auf der Geraden?')],
             auf2, f'<a href="{TS}#steigung">Themenseite 3.2, Steigung, Achsenabschnitt, Nullstelle</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Zwei Geraden: g fest, h über zwei Regler einstellbar"></svg>
        <div class="sl-row">
          {regler('s3', 'm2', 'm<sub>2</sub>', -3, 3, 0.25, 1, 'blau')}
          {regler('s3', 'b2', 'b<sub>2</sub>', -5, 5, 0.5, 2, 'orange')}
        </div>
      </figure>'''
fest3 = r'''      <div class="tabhuelle">
        <table class="gesetze formen">
          <thead><tr><th>Typ</th><th>Gleichung</th><th>Bedingung</th><th>Graph</th></tr></thead>
          <tbody>
            <tr><td>nicht konstante lineare Funktion</td><td>\(f(x) = m x + b\)</td><td>\(m \neq 0\)</td><td class="wort">schiefe Gerade</td></tr>
            <tr><td>proportionale Funktion</td><td>\(f(x) = m x\)</td><td>\(b = 0\)</td><td class="wort">Gerade durch den Ursprung</td></tr>
            <tr><td>Identität</td><td>\(f(x) = x\)</td><td>\(m = 1,\ b = 0\)</td><td class="wort">Winkelhalbierende des 1. und 3. Quadranten</td></tr>
            <tr><td>konstante Funktion</td><td>\(f(x) = b\)</td><td>\(m = 0\)</td><td class="wort">waagrechte Gerade</td></tr>
            <tr><td>senkrechte Gerade</td><td>\(x = k\)</td><td>kein \(m\)</td><td class="wort"><b>keine Funktion</b> — einem \(x\) sind unendlich viele \(y\) zugeordnet</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zwei Geraden zueinander</div>
          <p>\(g: y = m_1 x + b_1\) und \(h: y = m_2 x + b_2\):</p>
          <p>parallel: \(m_1 = m_2\) und \(b_1 \neq b_2\); identisch: \(m_1 = m_2\) und \(b_1 = b_2\); senkrecht: \(m_1 \cdot m_2 = -1\), also <span class="nb">\(m_2 = -\tfrac{1}{m_1}\).</span></p>
          <p>Warum \(-1\)? Dreht man das Steigungsdreieck um \(90^\circ\), tauschen \(\Delta x\) und \(\Delta y\) die Rolle und ein Vorzeichen kippt: aus \(\tfrac{2}{1}\) wird <span class="nb">\(\tfrac{-1}{2}\).</span></p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Produktregel gilt nur, wenn <em>beide</em> Geraden eine Steigung haben. Eine waagrechte Gerade (\(m = 0\)) steht senkrecht auf einer senkrechten Geraden \(x = k\) — ein Produkt gibt es dort nicht.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 4, r'Welcher Typ? (i) \(y = -0.5x\); (ii) \(y = 4\); (iii) \(x = -2\); (iv) \(y = x\)',
     r'<p>(i) proportionale Funktion (\(b = 0\)); (ii) konstante Funktion (\(m = 0\)); (iii) senkrechte Gerade — <b>keine Funktion</b>; (iv) Identität (\(m = 1\), \(b = 0\); auch proportional).</p>', ''),
    ('3b', 3, r'Gegeben \(g_1: y = 3x + 1\), \(g_2: y = -\tfrac{1}{3}x + 2\), \(g_3: y = 3x - 4\), \(g_4: y = \tfrac{1}{3}x\). Welche Paare sind parallel, welche senkrecht?',
     r'<p>Parallel: \(g_1 \parallel g_3\) (beide \(m = 3\)).</p><p>Senkrecht: \(g_1 \perp g_2\) und \(g_3 \perp g_2\), denn \(3 \cdot \left(-\tfrac{1}{3}\right) = -1\).</p><p class="komm">\(g_4\) steht zu keiner der anderen senkrecht: \(3 \cdot \tfrac{1}{3} = 1\) und \(-\tfrac{1}{3} \cdot \tfrac{1}{3} = -\tfrac{1}{9}\) — beides ist nicht \(-1\).</p>', ''),
    ('3c', 2, r'Liegen die beiden Geraden parallel, senkrecht oder keines von beidem?',
     r'<p>P: parallel (beide \(m = -1.5\)). Q: senkrecht, denn \(1 \cdot (-1) = -1\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-g="-1.5,3;-1.5,-2" data-titel="P"></svg><svg class="mini gross" data-g="1,-2;-1,3" data-titel="Q"></svg></div>'),
    ('3d', 2, r'Warum schneiden sich zwei Geraden mit gleichem \(m\) und verschiedenem \(b\) nie?',
     r'<p>Gleiches \(m\) heisst gleiche Richtung. Zu jeder Stelle \(x\) unterscheiden sich die beiden Werte um genau \(b_1 - b_2 \neq 0\) — dieser Abstand bleibt überall gleich und wird nie null.</p>', ''),
])
k3 = kapitel(3, 'typen-und-lage', 'Typen und Lagebeziehungen', 'K1 · K2', 35,
             'Du erkennst an \\(m\\) und \\(b\\), ob eine Funktion proportional, konstant oder die Identität ist, unterscheidest sie von der senkrechten Geraden \\(x = k\\) — und entscheidest, ob zwei Geraden parallel oder senkrecht sind.',
             ('g3-2-lp-typen', 'Gerade sehen: Typen und Lagebeziehungen', '1:44'),
             sim3, ('g3-2-lp-kontrolle-typen', 'Kontrollfragen zu Typen und Lage', '0:58'),
             fest3, [uebung('typ-erkennen', 'Typ erkennen'), uebung('parallel-senkrecht', 'parallel oder senkrecht')],
             auf3, f'<a href="{TS}#typen">Themenseite 3.2, Typen linearer Funktionen</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Gerade durch gegebene Punkte einstellen"></svg>
        <div class="sl-row">
          {regler('s4', 'm', 'm', -3, 3, 0.25, 1, 'blau')}
          {regler('s4', 'b', 'b', -5, 5, 0.5, 0, 'orange')}
        </div>
      </figure>'''
fest4 = r'''      <div class="tabhuelle">
        <table class="gesetze formen">
          <thead><tr><th>Gegeben</th><th>Ansatz</th><th>Dann</th></tr></thead>
          <tbody>
            <tr><td>\(m\) und ein Punkt \(P(x_1 \mid y_1)\)</td><td>\(y = m x + b\)</td><td class="wort">\(P\) einsetzen: \(b = y_1 - m\,x_1\)</td></tr>
            <tr><td>\(b\) und ein Punkt <span class="komm">(\(x_1 \neq 0\))</span></td><td>\(y = m x + b\)</td><td class="wort">\(P\) einsetzen, nach \(m\) auflösen</td></tr>
            <tr><td>zwei Punkte <span class="komm">(\(x_1 \neq x_2\))</span></td><td>\(y = m x + b\)</td><td class="wort">erst \(m = \dfrac{y_2 - y_1}{x_2 - x_1}\), dann \(b\)</td></tr>
            <tr><td>parallel zu \(g\) durch \(P\)</td><td>\(m = m_g\)</td><td class="wort">dann wie oben: \(P\) einsetzen</td></tr>
            <tr><td>senkrecht zu \(g\) durch \(P\) <span class="komm">(\(m_g \neq 0\))</span></td><td>\(m = -\dfrac{1}{m_g}\)</td><td class="wort">dann wie oben: \(P\) einsetzen</td></tr>
            <tr><td>Sachtext</td><td>«pro …» \(\to m\)</td><td class="wort">«Grundgebühr», «zu Beginn» \(\to b\); Variablen mit Einheit benennen und den zulässigen Bereich angeben</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk"><div class="titel">Immer gleich</div>
          <ol>
            <li>Ansatz \(y = m x + b\) hinschreiben.</li>
            <li>Was gegeben ist, einsetzen — bei zwei Punkten zuerst \(m\).</li>
            <li>Nach der fehlenden Zahl auflösen.</li>
            <li>Probe: den gegebenen Punkt einsetzen.</li>
          </ol>
          <p>Durch zwei verschiedene Punkte mit \(x_1 \neq x_2\) geht genau eine Gerade — zwei Punkte genügen also immer.</p></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div>
          <p>In \(b = y_1 - m\,x_1\) wird \(m\,x_1\) <em>abgezogen</em>. Für \(m = 3\) und \(P(4 \mid 2)\) ist \(b = 2 - 12 = -10\), nicht \(14\).</p></div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Gleichung der Geraden mit (i) \(m = -3\) durch \(P(2 \mid 1)\); (ii) \(b = 2\) durch \(P(4 \mid 10)\); (iii) durch \(A(-1 \mid 5)\) und \(B(3 \mid -3)\).',
     r'<p>(i) \(1 = -3 \cdot 2 + b\), \(b = 7\): \(f(x) = -3x + 7\).</p><p>(ii) \(10 = m \cdot 4 + 2\), \(m = 2\): \(f(x) = 2x + 2\).</p><p>(iii) \(m = \dfrac{-3 - 5}{3 - (-1)} = -2\), dann \(5 = -2 \cdot (-1) + b\), \(b = 3\): \(f(x) = -2x + 3\).</p>', ''),
    ('4b', 2, r'Eine Gerade hat die Nullstelle \(5\) und den \(y\)-Achsenabschnitt \(10\). Gleichung?',
     r'<p>Das sind zwei Punkte: \((5 \mid 0)\) und \((0 \mid 10)\). \(m = \dfrac{0 - 10}{5 - 0} = -2\), \(b = 10\): \(f(x) = -2x + 10\).</p>', ''),
    ('4c', 3, r'(i) Parallel zu \(g(x) = 3x - 1\) durch \(P(2 \mid 10)\). (ii) Senkrecht zu \(h(x) = 2x + 1\) durch \(Q(4 \mid 3)\).',
     r'<p>(i) \(m = 3\), \(10 = 3 \cdot 2 + b\), \(b = 4\): \(f(x) = 3x + 4\).</p><p>(ii) \(m = -\dfrac{1}{2} = -0.5\), \(3 = -0.5 \cdot 4 + b\), \(b = 5\): \(f(x) = -0.5x + 5\).</p>', ''),
    ('4d', 3, 'Ein Abo kostet 12 CHF im Monat, dazu 0.05 CHF je Minute. Stelle \\(K(t)\\) auf (\\(t\\) in Minuten, \\(K\\) in CHF), gib die Definitionsmenge an und rechne, bei welcher Minutenzahl 20 CHF erreicht sind.',
     r'<p>«je Minute» \(\to m = 0.05\), «im Monat» \(\to b = 12\): \(K(t) = 0.05\,t + 12\), zulässig \(t \geq 0\).</p><p>\(20 = 0.05\,t + 12\) gibt \(0.05\,t = 8\), also \(t = 160\) Minuten.</p>', ''),
    ('4e', 3, r'Gleichung der Geraden im Bild (Punkte auf Gitterpunkten)? Und: Warum genügen zwei Punkte, um sie festzulegen?',
     r'<p>\(b = 2\); von \((-2 \mid 1)\) nach \((4 \mid 4)\) sind es sechs nach rechts und drei hinauf: \(m = \dfrac{3}{6} = 0.5\). Also \(f(x) = 0.5x + 2\).</p><p>Gesucht sind die zwei Zahlen \(m\) und \(b\). Zwei Unbekannte brauchen zwei Bedingungen — und geometrisch geht durch zwei verschiedene Punkte mit \(x_1 \neq x_2\) genau eine Gerade.</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-g="0.5,2" data-fenster="-4,6,-3,6" data-punkte="-2,1;0,2;4,4"></svg></div>'),
])
k4 = kapitel(4, 'gleichung-aufstellen', 'Die Geradengleichung aufstellen', 'K3', 45,
             'Du stellst die Gleichung auf — aus Steigung und Punkt, aus zwei Punkten, aus einer Lagebeziehung und aus einem Sachtext.',
             ('g3-2-lp-aufstellen', 'Gerade sehen: die Geradengleichung aufstellen', '1:46'),
             sim4, ('g3-2-lp-kontrolle-aufstellen', 'Kontrollfragen zum Aufstellen', '1:00'),
             fest4, [uebung('aufstellen-m-punkt', 'Steigung + Punkt → b'), uebung('aufstellen-zwei-punkte', 'Zwei Punkte → Gleichung'),
                     uebung('aufstellen-lage', 'parallel/senkrecht durch einen Punkt')],
             auf4, f'<a href="{TS}#gleichung-aufstellen">Themenseite 3.2, Funktionsgleichung aufstellen</a>')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 1.3 · 2.2 · 3.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Einsetzen, eine lineare Gleichung lösen, Punkte im Koordinatensystem. Wenn das wackelt: <a href="../grundlagen/g3-1-grundlagen.html">Themenseite 3.1, Grundlagen der Funktionen</a>.</p>
      ''' + clipkarte('g3-1-tabelle-term-graph', 'Funktionen: Tabelle, Term und Graph sind dasselbe', '1:17') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'\(f(x) = -3x + 7\): Berechne \(f(-2)\) und \(f(0.5)\).',
     r'<p>\(f(-2) = -3 \cdot (-2) + 7 = 13\) und \(f(0.5) = -1.5 + 7 = 5.5\).</p><p class="komm">Falsch? Klammer um negative Zahlen. <a href="../grundlagen/g1-3-algebraische-terme.html#klammern">Themenseite 1.3, Klammern auflösen</a></p>', ''),
    ('0b', 3, r'Löse: \(4x - 7 = 2x + 5\); \(0.25x + 40 = 70\); \(-2x + 8 = 0\).',
     r'<p>\(\mathbb{L} = \{6\}\); \(\mathbb{L} = \{120\}\); \(\mathbb{L} = \{4\}\).</p><p class="komm">Falsch? <a href="../grundlagen/g2-2a-lineare-gleichungen.html">Themenseite 2.2a, Lineare Gleichungen</a></p>', ''),
    ('0c', 2, r'Welcher der Punkte \(A(0 \mid 3)\), \(B(3 \mid 0)\), \(C(-2 \mid -1)\) liegt auf der \(y\)-Achse, welcher auf der \(x\)-Achse?',
     r'<p>\(A\) liegt auf der \(y\)-Achse (erste Koordinate \(0\)), \(B\) auf der \(x\)-Achse (zweite Koordinate \(0\)). \(C\) liegt im dritten Quadranten.</p>', ''),
    ('0d', 3, r'Ergänze die Wertetabelle zu \(y = 2x - 1\) für \(x = -1,\ 0,\ 1,\ 2\) und zeichne die vier Punkte.',
     r'<p>\(-3\), \(-1\), \(1\), \(3\) — also \((-1 \mid -3)\), \((0 \mid -1)\), \((1 \mid 1)\), \((2 \mid 3)\). Die vier Punkte liegen auf einer Geraden.</p><p class="komm">Falsch? <a href="../grundlagen/g3-1-grundlagen.html#darstellungen">Themenseite 3.1, Darstellungsformen</a> und der Clip oben.</p>', ''),
]) + '''
      <div class="merk" style="margin-top:10px">
        <div class="titel">So zählst du deine Punkte</div>
        <p>Vergleich jede Teilantwort mit der Lösung und zähl <b>ganze Punkte</b>:</p>
        <ul>
          <li><b>Mehrere Werte in einer Aufgabe</b> (0a, 0b, 0d): Alle richtig → volle Punktzahl. Ein Wert falsch → ein Punkt weniger, mindestens 0. Bei 0d zählen die vier Tabellenwerte zusammen 2 P, das Einzeichnen 1 P.</li>
          <li><b>Rechenweg stimmt, Ergebnis nicht</b> (ein Vorzeichen, ein Zahlendreher): die Hälfte der Punkte dieser Teilaufgabe, aufgerundet.</li>
          <li><b>Ansatz fehlt</b> oder die Antwort beantwortet eine andere Frage: 0 Punkte für diese Teilaufgabe.</li>
          <li><b>Andere richtige Schreibweise</b> (Bruch statt Dezimalzahl, Terme in anderer Reihenfolge): zählt voll.</li>
        </ul>
      </div>
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. Ist 0b falsch, zuerst das <a href="../grundlagen/g2-2a-lineare-gleichungen.html">Lösen linearer Gleichungen</a> — ohne das geht Kapitel 4 nicht. Dieselbe Zählweise gilt für die Aufgaben der Kapitel; sie sind Übung, kein Test — entscheidend ist, ob du den Weg verstanden hast.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/lineare-funktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 3.2 · K1–K3</span><span class="zeit">≈ 25 min · 22 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Ganz ohne Taschenrechner: Alle drei Kompetenzen des Teilgebiets tragen im Lehrplan den Vermerk «auch ohne Hilfsmittel».<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — mit dem Punkteraster im Bewertungspaket selbst, zusammen mit einer Lehrperson, oder wahlweise von einer KI. Für den KI-Weg die Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Paket hochladen. Das Paket enthält die Musterlösung: erst nach dem Lösen öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>19 – 22 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>15 – 18 P</td><td>Den schwächsten Teil nochmals: Simulation und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>10 – 14 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 9 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1 (zeichnen) und 2 (Nullstelle); G2 → 1 und 2; G3 → 1 und 2; G4 → 3 (Lage) und 4 (aufstellen); G5 → 3; G6 → 2 (Steigung) und 4; G7, G8 → 4</p>
          <p><b>Noch gezielter — nach Fehlerart:</b> Fehler im Steigungsquotienten <i>&Delta;y</i> : <i>&Delta;x</i> (G2, G6) → Kapitel 2; Fehler beim Einsetzen in <i>b</i> = <i>y</i><sub>1</sub> − <i>m x</i><sub>1</sub> (G4, G6, G7, G8) → Kapitel 4; fehlende oder falsche Zeichnung (G1) → Kapitel 1; falsche Lagebeziehung (G4, G5) → Kapitel 3.</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Lineare Funktionen, Version 1.0 (03.10.2026). Gebaut aus
     scripts/lp/lineare-funktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     RLP-BM 2030, Grundlagenfach 3.2 «Lineare Funktionen», Kompetenzen wörtlich
     (Quelle ../Math-GL.pdf, Abschnitt 6.4.4.1; alle drei mit «auch ohne Hilfsmittel»):
       K1  den Graphen einer linearen Funktion als Gerade in der kartesischen Ebene darstellen
       K2  die Koeffizienten der Funktionsgleichung geometrisch interpretieren (Steigung, Achsenabschnitt)
       K3  die Funktionsgleichung einer Geraden aufstellen
     Kompetenz → Kapitel → Test: K1 → 1, 3 → G1, G2, G5; K2 → 1, 2, 3 → G2, G3, G4, G5 ·
     K3 → 4 → G4, G6, G7, G8. Kein Kapitelziel ohne Kompetenz.

     Nicht in diesem Leitprogramm, weil in anderen Teilgebieten: Schnittpunkte zweier
     Geraden rechnerisch und der Vergleich zweier Tarife (GF 3.1 «Schnittpunkte von
     Funktionsgraphen», GF 2.3 Gleichungssysteme), das Lösen linearer Gleichungen
     (GF 2.2) und der Funktionsbegriff selbst (GF 3.1) — Letzteres steht im Vorwissen.
     Alles davon auf Themenseite 3.2 bzw. 3.1.

     Muster je Kapitel: ① Einführungsclip (zeigt alles, Auftrag am Schluss) → ② Simulation
     mit Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit
     Rückmeldung → ⑤ Aufgaben mit Lösungen. Notation wie Themenseite 3.2: m, b, x₀.
     Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/lineare-funktionen/*.tex). Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Lineare Funktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest — zusammen rund 195 Minuten.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 3.2</span>
    </div>
  </div>
</header>

<div class="huelle">
<div class="raster">

  <nav class="schiene" aria-label="Kapitelnavigation">
    <h2 id="ablauf">Ablauf</h2>
    <p class="lekt">Vorab</p>
    <ol>
      <li><a href="#k0"><span class="nr">0</span><span>Vorwissen</span></a></li>
    </ol>
    <p class="lekt">Kapitel</p>
    <ol>
      <li><a href="#k1"><span class="nr">1</span><span>m und b</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Steigung messen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Typen und Lage</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Gleichung aufstellen</span></a></li>
    </ol>
    <p class="lekt">Abschluss</p>
    <ol>
      <li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li>
    </ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 5 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach 3.2</p>
        <ul>
          <li><b>K1</b> den Graphen einer linearen Funktion als Gerade in der kartesischen Ebene darstellen <span class="ohm">auch ohne Hilfsmittel</span></li>
          <li><b>K2</b> die Koeffizienten der Funktionsgleichung geometrisch interpretieren (Steigung, Achsenabschnitt) <span class="ohm">auch ohne Hilfsmittel</span></li>
          <li><b>K3</b> die Funktionsgleichung einer Geraden aufstellen <span class="ohm">auch ohne Hilfsmittel</span></li>
        </ul>
        <p class="rlp-quelle">Nicht hier, sondern auf <a href="../grundlagen/g3-1-grundlagen.html">Themenseite 3.1</a> bzw. <a href="../grundlagen/g2-3-lineare-gleichungssysteme.html">2.3</a>: der Schnittpunkt zweier Geraden und der Vergleich zweier Tarife.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Lineare Funktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Kapitel = Lektion: keine Lektionsbänder mehr (Abnahme 06.10.2026).
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (03.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 35 · K4 45 · Gesamttest 25 = 195 min
# Die vier Kapitel sind die vier Lektionen; Vorwissen und Gesamttest kommen davor und danach.
body = (oben + k0 + k1 + k2
        + k3 + k4
        + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
