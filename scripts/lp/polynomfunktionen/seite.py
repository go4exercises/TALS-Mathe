"""Baut leitprogramme/polynomfunktionen.html aus einer Kapitelbeschreibung (04.10.2026).

  python3 scripts/lp/polynomfunktionen/seite.py

Leitprogramm zum Teilgebiet SP 3.3 (Themenseite s3-3-polynomfunktionen.html), alle drei
RLP-Kompetenzen. Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden Seite,
ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf
kommt das Gerüst aus leitprogramme/potenz-wurzelfunktionen.html, mit eigenem Titel und
eigenen localStorage-Schlüsseln. Wiederholbar: zweimal laufen lassen ergibt dieselbe
Datei. Danach Pre-Flight und python3 scripts/build-seo.py. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/polynomfunktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/potenz-wurzelfunktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Potenz- und Wurzelfunktionen</title>',
                      '<title>Leitprogramm Polynomfunktionen</title>')
    alt = alt.replace('lp-potwurzel-', 'lp-polynom-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Potenz- und Wurzelfunktionen', '\n/* ════════ Polynomfunktionen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Potenz- und Wurzelfunktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Polynomfunktionen — Simulationen')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Potenz- und Wurzelfunktionen', 'Polynomfunktionen')
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 4. Oktober 2026', fuss)

CSS = '''
/* ════════ Polynomfunktionen (04.10.2026) — Kapitelmuster wie Potenz- und Wurzelfunktionen ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Eigen sind die
   Farben der Polynom-Bausteine: Nullstellen orange, Hoch- und Tiefpunkte grün. */
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
.hilfs-schalter,.sim-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--lila-hell);border:1px solid var(--lila-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sim input[type=range]:disabled{opacity:.4}
/* Farben im ganzen Leitprogramm: blau = die Kurve und ihr Leitkoeffizient a, orange =
   Nullstellen und Linearfaktoren, grün = Hoch- und Tiefpunkte, rot = Gegenbeispiel,
   Tinte = neutral. Dieselben Farben tragen die Clips (farbe 1/2/3/4/5). */
.sim .normal{stroke-dasharray:5 4;stroke:var(--tinte-2);fill:none}
.sim .asym{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 3;fill:none}
.sim .zielkurve{stroke:var(--gruen);stroke-width:4;opacity:.38;fill:none}
.p-ns{fill:var(--orange)} .p-ex{fill:var(--gruen)} .p-pkt{fill:var(--tinte)} .p-lauf{fill:var(--tinte)}
svg.mini .p-pkt{fill:var(--tinte)} svg.mini .p-ns{fill:var(--orange)}
.mini-reihe svg.mini{background:var(--karte)}
.sim-formel{line-height:1.6}
/* Ein Punkt direkt hinter einer Formel landet sonst allein auf der naechsten Zeile. */
.nb{white-space:nowrap}
'''


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf — so rechnet
    die Bibliothek), abgerundet auf Sekunden (HOWTO-leitprogramme §7)."""
    d = json.load(open(R + 'clips/' + name + '.json'))
    t = int(sum(s['dauer'] for s in d['szenen']))
    return '%d:%02d' % (t // 60, t % 60)


def clipkarte(datei, titel, zeit=None):
    zeit = zeit or dauer(datei)
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
          {'<svg class="mini gross ue-bild" role="img" aria-label="Graph zur Aufgabe"></svg>' if bild else ''}
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-sf">SP 3.3 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TS = '../schwerpunkt/s3-3-polynomfunktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Polynom dritten Grades a mal x minus x1, mal x minus x2, mal x minus x3, mit seinen Nullstellen"></svg>
        <div class="sl-row">
          {regler('s1', 'a', 'a', -2, 2, 0.5, 0.5, 'blau')}
          {regler('s1', 'x1', 'x<sub>1</sub>', -3, 3, 1, -2, 'orange')}
          {regler('s1', 'x2', 'x<sub>2</sub>', -3, 3, 1, 1, 'orange')}
          {regler('s1', 'x3', 'x<sub>3</sub>', -3, 3, 1, 3, 'orange')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Polynomfunktion</div>
          <p>\[ f(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0, \qquad n \in \mathbb{N} \]</p>
          <p>mit \(a_k \in \mathbb{R}\) und \(a_n \neq 0\). \(n\) heisst <b>Grad</b>, \(a_n\) <b>Leitkoeffizient</b>. Die Darstellung als Summe heisst auch <b>Summenform</b>.</p>
          <p><b>Linearfaktordarstellung:</b> Sind \(x_1, \dots, x_n\) die Nullstellen, so ist</p>
          <p>\[ f(x) = a_n \cdot (x - x_1)(x - x_2) \cdots (x - x_n) \]</p>
          <p><b>Satz vom Nullprodukt:</b> Ein Produkt ist genau dann null, wenn ein Faktor null ist. Jeder Linearfaktor \((x - x_k)\) wird genau bei \(x_k\) null — die Nullstellen stehen in den Klammern, <b>mit umgekehrtem Vorzeichen</b>.</p>
          <p>Der Faktor vor den Klammern ist der <b>Leitkoeffizient</b>. Er streckt den Graphen in \(y\)-Richtung und ändert die Nullstellen nicht.</p>
          <p><b>Gleichung aus Nullstellen:</b> Ansatz \(f(x) = a\,(x - x_1)(x - x_2)(x - x_3)\), dann einen weiteren Punkt einsetzen — meist \((0 \mid f(0))\) — und nach \(a\) auflösen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Zahl in der Klammer ist <em>nicht</em> die Nullstelle: \((x + 2)\) wird null bei \(x = -2\), nicht bei \(2\).</p>
          <p>Und der Faktor vorne liefert keine Nullstelle: \(0.5\,(x - 1)\) ist bei \(x = 0.5\) nicht null.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 3, r'Polynomfunktion oder nicht? Wenn ja: Grad und Leitkoeffizient. (1) \(f(x) = 3x^4 - x + 7\) (2) \(g(x) = 2x^3 - \dfrac{5}{x}\) (3) \(h(x) = -(x-2)(x+1)(x+5)\)',
     r'<p>(1) ja, Grad 4, Leitkoeffizient 3. (2) nein: \(\frac{5}{x} = 5x^{-1}\) hat einen negativen Exponenten. (3) ja, Grad 3, Leitkoeffizient \(-1\).</p><p class="komm">Bei (3) nur die \(x\)-Terme ausmultiplizieren: \(-1 \cdot x \cdot x \cdot x = -x^3\).</p>', ''),
    ('1b', 3, r'\(f(x) = 2\,(x+1)(x-3)\): Gib die Nullstellen an und schreib \(f\) in Summenform. Warum ändert der Faktor \(2\) nichts an den Nullstellen?',
     r'<p>Nullstellen \(-1\) und \(3\). Summenform: \(2\,(x^2 - 2x - 3) = 2x^2 - 4x - 6\).</p><p>Ein Produkt ist nur null, wenn ein Faktor null ist — und \(2\) ist nie null. Der Faktor streckt nur in \(y\)-Richtung.</p>', ''),
    ('1c', 4, r'Gesucht ist die Polynomfunktion dritten Grades mit den Nullstellen \(-3\), \(1\) und \(2\), deren Graph die \(y\)-Achse bei \(-3\) schneidet.',
     r'<p>Ansatz: \(f(x) = a\,(x+3)(x-1)(x-2)\).</p><p>\(f(0) = a \cdot 3 \cdot (-1) \cdot (-2) = 6a = -3 \;\Rightarrow\; a = -0.5\).</p><p>\(f(x) = -0.5\,(x+3)(x-1)(x-2)\).</p><p class="komm">Typischer Fehler: \(f(0) = a \cdot (-3) \cdot 1 \cdot 2\) — die Nullstellen statt der Klammerwerte bei \(x = 0\) eingesetzt.</p>', ''),
    ('1d', 3, r'Der Graph gehört zu einem Polynom dritten Grades. Bestimme seine Gleichung in Linearfaktordarstellung. (Die markierten Punkte liegen auf Gitterpunkten.)',
     r'<p>Nullstellen \(-1\), \(1\), \(3\); Ansatz \(f(x) = a\,(x+1)(x-1)(x-3)\).</p><p>Der Graph geht durch \((0 \mid 3)\): \(f(0) = a \cdot 1 \cdot (-1) \cdot (-3) = 3a = 3 \;\Rightarrow\; a = 1\).</p><p>\(f(x) = (x+1)(x-1)(x-3)\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-p="1;-1,1,3" data-fenster="-3,5,-6,8" data-punkte="-1,0;1,0;3,0;0,3"></svg></div>'),
], zwei=False)
k1 = kapitel(1, 'linearfaktoren', 'Linearfaktoren und Nullstellen', 'K1', 40,
             r'Du erkennst eine Polynomfunktion mit Grad und Leitkoeffizient, liest die Nullstellen aus den Linearfaktoren ab und stellst umgekehrt aus Nullstellen und einem Punkt die Gleichung auf.',
             ('s3-3-lp-linearfaktoren', 'Linearfaktoren und Nullstellen'),
             sim1, ('s3-3-lp-kontrolle-linearfaktoren', 'Kontrollfragen zu den Linearfaktoren'),
             fest1, [uebung('nullstellen-ablesen', 'Nullstellen ablesen'), uebung('grad-leitkoeff', 'Grad und Leitkoeffizient'),
                     uebung('a-bestimmen', 'Den Faktor a bestimmen')],
             auf1, f'<a href="{TS}#darstellungen">Themenseite 3.3, Linearfaktoren und Nullstellen</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Polynom a mal x minus p hoch k, mal x minus q hoch m, mit seinen Nullstellen"></svg>
        <div class="sl-row">
          {regler('s2', 'a', 'a', -2, 2, 0.5, 0.5, 'blau')}
          {regler('s2', 'p', 'p', -3, 3, 1, 1, 'orange')}
          {regler('s2', 'k', 'k', 1, 3, 1, 2, 'grau')}
          {regler('s2', 'q', 'q', -3, 3, 1, -2, 'orange')}
          {regler('s2', 'm', 'm', 1, 3, 1, 1, 'grau')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Mehrfache Nullstellen</div>
          <p>Kommt ein Linearfaktor mehrfach vor, fasst man ihn zur Potenz zusammen:</p>
          <p>\[ f(x) = a\,(x - x_1)^{k} \cdots \]</p>
          <p>Der Exponent \(k\) heisst <b>Vielfachheit</b> der Nullstelle \(x_1\).</p>
          <ul>
            <li><b>einfach</b>, \((x - x_1)^1\): Der Graph <b>schneidet</b> die \(x\)-Achse (Vorzeichenwechsel).</li>
            <li><b>doppelt</b>, \((x - x_1)^2\): Der Graph <b>berührt</b> die \(x\)-Achse — Hoch- oder Tiefpunkt auf der Achse, kein Vorzeichenwechsel.</li>
            <li><b>dreifach</b>, \((x - x_1)^3\): Der Graph <b>schneidet terrassenförmig abgeflacht</b> (Vorzeichenwechsel, waagrechte Tangente).</li>
          </ul>
          <p>Allgemein: <b>ungerade</b> Vielfachheit — Vorzeichenwechsel, <b>gerade</b> — keiner. Denn eine gerade Potenz ist nie negativ.</p>
          <p>Die Vielfachheiten zusammen ergeben höchstens den Grad.</p>
          <p><b>Gleichung am Graphen ablesen:</b> Wo er schneidet, ein einfacher Faktor; wo er berührt, ein quadrierter; mit einem weiteren Punkt \(a\) bestimmen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Grad = Anzahl Nullstellen». Der Grad ist nur die <em>Höchstzahl</em>: \(f(x) = (x-1)^2\,(x+2)\) hat Grad 3, aber nur zwei verschiedene Nullstellen.</p>
          <p>Und beim Einsetzen das Quadrat nicht vergessen: \(f(0)\) von \(a\,(x+2)^2\) ist \(4a\), nicht \(2a\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'\(f(x) = (x+2)^2\,(x-1)^3\,(x-4)\): Welchen Grad hat \(f\)? Gib alle Nullstellen mit Vielfachheit an und beschreib, was der Graph an jeder tut.',
     r'<p>Grad \(2 + 3 + 1 = 6\).</p><p>\(-2\): doppelt, der Graph berührt die \(x\)-Achse. \(1\): dreifach, er schneidet mit Terrasse. \(4\): einfach, er schneidet.</p>', ''),
    ('2b', 3, r'Der Graph gehört zu einem Polynom dritten Grades. Bestimme seine Gleichung. (Die markierten Punkte liegen auf Gitterpunkten.)',
     r'<p>Bei \(2\) berührt er (doppelt), bei \(-1\) schneidet er (einfach): \(f(x) = a\,(x-2)^2\,(x+1)\).</p><p>\(f(0) = a \cdot 4 \cdot 1 = 4a = -2 \;\Rightarrow\; a = -0.5\).</p><p>\(f(x) = -0.5\,(x-2)^2\,(x+1)\).</p><p class="komm">Kontrolle: \(a \lt 0\), also geht der Graph rechts nach unten — wie im Bild.</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-p="-0.5;2,2,-1" data-fenster="-3,4,-5,5" data-punkte="-1,0;2,0;0,-2"></svg></div>'),
    ('2c', 2, r'Warum wechselt \(f(x) = (x-3)^2\,(x+1)\) an der Stelle \(3\) das Vorzeichen <em>nicht</em>?',
     r'<p>\((x-3)^2\) ist als Quadrat links und rechts von \(3\) positiv. Der andere Faktor \((x+1)\) ist in der Nähe von \(3\) ebenfalls positiv. Das Produkt hat also auf beiden Seiten dasselbe Vorzeichen — der Graph berührt die \(x\)-Achse nur.</p>', ''),
    ('2d', 4, r'Gesucht ist die Polynomfunktion dritten Grades mit der doppelten Nullstelle \(-1\), der einfachen Nullstelle \(3\) und \(f(0) = 6\). Skizziere den Graphen.',
     r'<p>Ansatz \(f(x) = a\,(x+1)^2\,(x-3)\); \(f(0) = a \cdot 1 \cdot (-3) = -3a = 6 \;\Rightarrow\; a = -2\).</p><p>\(f(x) = -2\,(x+1)^2\,(x-3)\).</p><p>Skizze: kommt von links oben (\(a \lt 0\), Grad 3), berührt die \(x\)-Achse bei \(-1\), steigt durch \((0 \mid 6)\), schneidet bei \(3\) und läuft nach rechts unten.</p>'
     # Das Bild ist die Lösungsskizze — es steht darum in der Lösung, nicht bei der Aufgabe.
     '<div class="mini-reihe"><svg class="mini gross" data-p="-2;-1,-1,3" data-fenster="-3,5,-10,20" data-punkte="-1,0;3,0;0,6"></svg></div>', ''),
], zwei=False)
k2 = kapitel(2, 'mehrfache-nullstellen', 'Mehrfache Nullstellen', 'K1 · K2', 40,
             r'Du unterscheidest einfache, doppelte und dreifache Nullstellen am Term und am Graphen (schneiden, berühren, Terrasse) und liest eine Gleichung mit mehrfacher Nullstelle am Graphen ab.',
             ('s3-3-lp-vielfachheit', 'Mehrfache Nullstellen'),
             sim2, ('s3-3-lp-kontrolle-vielfachheit', 'Kontrollfragen zu mehrfachen Nullstellen'),
             fest2, [uebung('vielfachheit', 'Schneiden oder berühren?'), uebung('graf-vielfachheit', 'Am Graphen ablesen', True),
                     uebung('gleichung-mehrfach', 'Gleichung mit doppelter Nullstelle')],
             auf2, f'<a href="{TS}#theorie">Themenseite 3.3, Mehrfache Nullstellen</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Polynom a mal x hoch n plus c mal x hoch n minus 2 plus d, mit dem Leitterm gestrichelt"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Leitterm \\(a\\,x^n\\) (gestrichelt)</label>
        <label class="sim-schalter"><input type="checkbox"> von weitem (Fenster ×10)</label>
        <div class="sl-row">
          {regler('s3', 'n', 'n', 2, 5, 1, 3, 'grau')}
          {regler('s3', 'a', 'a', -2, 2, 0.5, 1, 'blau')}
          {regler('s3', 'c', 'c', -4, 4, 1, -4, 'grau')}
          {regler('s3', 'd', 'd', -3, 3, 1, 0, 'grau')}
        </div>
        <figcaption class="sim-legende">\\(f(x) = a\\,x^n + c\\,x^{{n-2}} + d\\)</figcaption>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Globalverlauf</div>
          <p>Für grosse \(|x|\) dominiert der <b>Leitterm</b> \(a_n x^n\). Grad und Vorzeichen des Leitkoeffizienten legen den Globalverlauf fest:</p>
          <ul>
            <li>\(n\) <b>ungerade</b>, \(a_n \gt 0\): von links unten nach rechts oben; \(a_n \lt 0\): von links oben nach rechts unten.</li>
            <li>\(n\) <b>gerade</b>, \(a_n \gt 0\): beide Enden nach oben; \(a_n \lt 0\): beide Enden nach unten.</li>
          </ul>
          <p>Eine Polynomfunktion \(n\)-ten Grades hat <b>höchstens \(n\) Nullstellen</b> und <b>höchstens \(n - 1\) lokale Extremstellen</b>. Bei <b>ungeradem</b> Grad gibt es immer mindestens eine Nullstelle.</p>
          <p><b>Symmetrie-Schnellcheck</b> über die Exponenten:</p>
          <ul>
            <li>nur gerade Exponenten (das konstante Glied \(a_0 = a_0 x^0\) zählt als gerade): <b>gerade Funktion</b>, achsensymmetrisch zur \(y\)-Achse;</li>
            <li>nur ungerade Exponenten (also auch \(a_0 = 0\)): <b>ungerade Funktion</b>, punktsymmetrisch zum Ursprung;</li>
            <li>gemischt: weder noch.</li>
          </ul>
          <p>Nachweis mit \(f(-x) = f(x)\) bzw. \(f(-x) = -f(x)\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Leitkoeffizienten vorne suchen: Bei \(f(x) = 3 + 2x - x^4\) ist er \(-1\), nicht \(3\) — er gehört zum <em>höchsten</em> Exponenten.</p>
          <p>Und das konstante Glied übersehen: \(x^3 + x + 1\) ist <em>nicht</em> punktsymmetrisch, denn \(1 = 1 \cdot x^0\) hat einen geraden Exponenten.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 3, r'Beschreib den Globalverlauf: (1) \(f(x) = -3x^5 + 4x^2 - 1\) (2) \(g(x) = 0.5x^4 - 3x^3\) (3) \(h(x) = 7 - x^2\)',
     r'<p>(1) Grad 5, \(a_5 = -3 \lt 0\): von links oben nach rechts unten. (2) Grad 4, \(a_4 = 0.5 \gt 0\): beide Enden oben. (3) Grad 2, \(a_2 = -1 \lt 0\): beide Enden unten.</p>', ''),
    ('3b', 2, r'Wie viele Nullstellen und wie viele lokale Extremstellen kann eine Polynomfunktion vierten Grades höchstens haben? Skizziere den Graphen eines Polynoms vierten Grades mit \(a_4 \gt 0\), das genau <em>zwei</em> Nullstellen und <em>drei</em> Extremstellen hat.',
     r'<p>Höchstens 4 Nullstellen und 3 Extremstellen.</p><p>Skizze: ein «W», dessen mittlerer Hochpunkt <em>unter</em> der \(x\)-Achse liegt — dann schneiden nur die beiden äusseren Äste. Etwa \(f(x) = x^4 - 2x^2 - 3\).</p>', ''),
    ('3c', 3, r'Gerade, ungerade oder weder noch? (1) \(f(x) = x^4 - 3x^2 + 2\) (2) \(g(x) = x^5 - x\) (3) \(h(x) = x^3 + x^2\). Weise das Ergebnis bei (2) mit \(g(-x)\) nach.',
     r'<p>(1) nur gerade Exponenten (4, 2, 0): gerade. (2) nur ungerade (5, 1): ungerade. (3) gemischt (3, 2): weder noch.</p><p>\(g(-x) = (-x)^5 - (-x) = -x^5 + x = -(x^5 - x) = -g(x)\) ✓</p>', ''),
    ('3d', 3, r'Begründe, warum jede Polynomfunktion <em>ungeraden</em> Grades mindestens eine Nullstelle hat — und gib ein Polynom vierten Grades ohne Nullstelle an.',
     r'<p>Bei ungeradem Grad zeigen die beiden Enden in entgegengesetzte Richtungen: eines nach unten, eines nach oben. Der Graph ist eine durchgehende Kurve ohne Sprünge, also muss er die \(x\)-Achse mindestens einmal kreuzen.</p><p>Ohne Nullstelle, Grad 4: zum Beispiel \(f(x) = x^4 + 1\), denn \(x^4 \geq 0\).</p>', ''),
], zwei=False)
k3 = kapitel(3, 'globalverlauf', 'Der Globalverlauf', 'K2', 40,
             r'Du sagst aus Grad und Leitkoeffizient voraus, wohin die Enden des Graphen zeigen, gibst die Höchstzahl der Nullstellen und Extremstellen an und erkennst die Symmetrie an den Exponenten.',
             ('s3-3-lp-globalverlauf', 'Der Globalverlauf'),
             sim3, ('s3-3-lp-kontrolle-globalverlauf', 'Kontrollfragen zum Globalverlauf'),
             fest3, [uebung('enden', 'Wohin zeigen die Enden?'), uebung('hoechstzahl', 'Höchstens wie viele?'),
                     uebung('symmetrie-poly', 'Symmetrie erkennen')],
             auf3, f'<a href="{TS}#typen">Themenseite 3.3, Verlauf qualitativ</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Polynom dritten Grades mit einer verschiebbaren Probestelle r"></svg>
        <div class="sl-row">
          {regler('s4', 'r', 'Probestelle r', -6, 6, 1, 0, 'orange')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Nullstellen berechnen</div>
          <p>Gegeben ist meist die Summenform. Ziel ist die Linearfaktordarstellung — dann stehen die Nullstellen da.</p>
          <ol>
            <li><b>Ausklammern</b>, wenn das konstante Glied fehlt: \(x^3 - 9x = x\,(x^2 - 9) = x\,(x-3)(x+3)\).</li>
            <li><b>Satz vom Nullprodukt</b>: jeden Faktor null setzen.</li>
            <li>Sonst eine Nullstelle <b>raten</b>: Bei ganzzahligen Koeffizienten und \(a_n = 1\) ist jede ganzzahlige Nullstelle ein <b>Teiler von \(a_0\)</b>. Probe: \(f(x_1) = 0\)?</li>
            <li>Den Linearfaktor \((x - x_1)\) <b>abspalten</b> (Polynomdivision): Der Rest ist \(0\), der Quotient hat einen Grad weniger.</li>
            <li>Den quadratischen Rest faktorisieren oder mit der Lösungsformel lösen.</li>
          </ol>
          <p>Beispiel: \(f(1) = 1 - 2 - 5 + 6 = 0\), also</p>
          <p>\[ (x^3 - 2x^2 - 5x + 6) : (x - 1) = x^2 - x - 6 = (x-3)(x+2) \]</p>
          <p>Probe einer Division: zurückmultiplizieren.</p>
          <p>Mit dem Taschenrechner lassen sich Nullstellen auch über eine Wertetabelle oder den Gleichungslöser finden — zur Kontrolle.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Durch \(x\) teilen statt ausklammern: Aus \(x^3 = 9x\) wird dann \(x^2 = 9\) — und die Lösung \(x = 0\) ist verloren.</p>
          <p>Und beim Raten das Minus vergessen: Auch \(-1, -2, -3, \dots\) sind Teiler.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Berechne alle Nullstellen von \(f(x) = x^3 + 2x^2 - 8x\).',
     r'<p>\(x^3 + 2x^2 - 8x = x\,(x^2 + 2x - 8) = x\,(x+4)(x-2)\).</p><p>Nullstellen: \(0\), \(-4\), \(2\).</p>', ''),
    ('4b', 4, r'Berechne alle Nullstellen von \(f(x) = x^3 - 6x^2 + 11x - 6\): Rate eine, spalte den Linearfaktor ab und löse den Rest.',
     r'<p>Teiler von \(-6\) probieren: \(f(1) = 1 - 6 + 11 - 6 = 0\).</p><p>\((x^3 - 6x^2 + 11x - 6) : (x - 1) = x^2 - 5x + 6 = (x-2)(x-3)\).</p><p>Nullstellen \(1\), \(2\), \(3\); \(f(x) = (x-1)(x-2)(x-3)\).</p>', ''),
    ('4c', 4, r'\(f(x) = x^3 + x^2 - 5x + 3\): Bestimme alle Nullstellen samt Vielfachheit und sag, was der Graph an jeder tut.',
     r'<p>\(f(1) = 1 + 1 - 5 + 3 = 0\). \((x^3 + x^2 - 5x + 3) : (x - 1) = x^2 + 2x - 3 = (x+3)(x-1)\).</p><p>Also \(f(x) = (x-1)^2\,(x+3)\): \(1\) ist doppelt (berühren), \(-3\) einfach (schneiden).</p>', ''),
    ('4d', 3, r'Jemand löst \(x^3 = 4x\) so: «durch \(x\) teilen, \(x^2 = 4\), also \(x = \pm 2\).» Was ist falsch? Löse richtig.',
     r'<p>Durch \(x\) teilen ist nur erlaubt, wenn \(x \neq 0\) — dabei geht die Lösung \(0\) verloren.</p><p>Richtig: \(x^3 - 4x = x\,(x-2)(x+2) = 0\), also \(\mathbb{L} = \{-2;\ 0;\ 2\}\).</p>', ''),
], zwei=False)
k4 = kapitel(4, 'nullstellen-berechnen', 'Nullstellen berechnen', 'K1 · K3', 40,
             r'Du berechnest die Nullstellen einer Polynomfunktion in Summenform: durch Ausklammern, oder indem du eine Nullstelle rätst, den Linearfaktor abspaltest und den Rest löst.',
             ('s3-3-lp-nullstellen-berechnen', 'Nullstellen berechnen'),
             sim4, ('s3-3-lp-kontrolle-nullstellen', 'Kontrollfragen zum Nullstellen berechnen'),
             fest4, [uebung('ausklammern', 'Ausklammern'), uebung('probe-teiler', 'Einen Teiler prüfen'),
                     uebung('abspalten', 'Linearfaktor abspalten')],
             auf4, f'<a href="{TS}#darstellungen">Themenseite 3.3, Polynomdivision</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Graph von x hoch drei minus drei x mit einem Läufer und einschränkbarer Definitionsmenge"></svg>
        <label class="sim-schalter"><input type="checkbox"> \\(D\\) einschränken</label>
        <div class="sl-row">
          {regler('s5', 'x', 'Läufer x', -3, 3, 0.05, 0, 'grau')}
        </div>
        <div class="sl-row d-regler">
          {regler('s5', 'l', 'D von', -3, 0, 0.5, -3, 'grau')}
          {regler('s5', 'r', 'D bis', 0, 3, 0.5, 3, 'grau')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Hoch- und Tiefpunkte</div>
          <p>Ein <b>Hochpunkt</b> \(H\) ist ein lokal höchster Punkt des Graphen: Dort wechselt er von steigend zu fallend. Seine \(y\)-Koordinate ist ein <b>lokales (relatives) Maximum</b>. Entsprechend ist ein <b>Tiefpunkt</b> \(T\) ein lokal tiefster Punkt — ein <b>lokales Minimum</b>.</p>
          <p>Ein <b>absolutes (globales) Maximum</b> ist der grösste Funktionswert überhaupt. Viele Polynomfunktionen haben keines, weil sie für grosse \(|x|\) über alle Grenzen wachsen.</p>
          <p><b>Auf einem Intervall</b> \(D = [u;\, v]\) gibt es immer einen grössten und einen kleinsten Wert. Er liegt in einem Hoch- bzw. Tiefpunkt <b>oder am Rand</b> — also beide vergleichen.</p>
          <p><b>Grad 2 exakt</b> (quadratische Funktion \(f(x) = ax^2 + bx + c\)):</p>
          <p>\[ x_s = -\frac{b}{2a}, \qquad y_s = f(x_s) \]</p>
          <p>Bei \(a \gt 0\) ein Tiefpunkt, bei \(a \lt 0\) ein Hochpunkt.</p>
          <p><b>Ab Grad 3</b> liest man Hoch- und Tiefpunkte grafisch ab — am Graphen oder mit dem Rechner in einer feinen Wertetabelle. Exakt geht es später mit der Ableitung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die \(y\)-Koordinate eines Hochpunkts als grössten Funktionswert ausgeben. Sie ist nur <em>lokal</em> maximal — bei \(x^3 - 3x\) ist \(f(3) = 18 \gt 2\).</p>
          <p>Und bei Anwendungen die Ränder vergessen: Das absolute Maximum kann am Rand von \(D\) liegen.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 4, r'Lies Hochpunkt und Tiefpunkt des abgebildeten Graphen ab (sie liegen auf Gitterpunkten). Ist der Hochpunkt ein absolutes Maximum? Begründe.',
     r'<p>\(H(0 \mid 3)\), \(T(2 \mid -1)\).</p><p>Nein: Der Graph steigt rechts über alle Grenzen (\(f(4) = 19 \gt 3\)) — das Maximum bei \(H\) ist nur lokal.</p><p class="komm">Gezeichnet ist \(f(x) = x^3 - 3x^2 + 3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-c="1,-3,0,3" data-fenster="-2,4,-3,5" data-punkte="0,3;2,-1"></svg></div>'),
    ('5b', 3, r'Berechne den Extrempunkt von \(f(x) = 2x^2 - 8x + 5\) exakt. Ist er ein Hoch- oder ein Tiefpunkt?',
     r'<p>\(x_s = -\frac{-8}{2 \cdot 2} = 2\), \(y_s = f(2) = 8 - 16 + 5 = -3\).</p><p>\(a = 2 \gt 0\): Tiefpunkt \(T(2 \mid -3)\).</p>', ''),
    ('5c', 4, r'Aus einem quadratischen Blech mit 12 cm Seitenlänge entsteht eine offene Schachtel: In jeder Ecke wird ein Quadrat der Seite \(x\) (in cm) ausgeschnitten. Ihr Volumen ist \(V(x) = x\,(12 - 2x)^2\). Gib die sinnvolle Definitionsmenge an, berechne \(V(1)\) und bestimme mit einer Wertetabelle (Rechner erlaubt), für welches \(x\) das Volumen am grössten ist.',
     r'<p>\(D = \,]0;\, 6[\) — bei \(x = 6\) bliebe kein Boden.</p><p>\(V(1) = 1 \cdot 10^2 = 100\) cm³.</p><p>Wertetabelle: \(V(1.5) = 121.5\), \(V(2) = 128\), \(V(2.5) = 122.5\). Grösstes Volumen bei \(x = 2\) cm mit \(128\) cm³ — der Hochpunkt, und weil \(V\) an beiden Rändern gegen \(0\) geht, auch das absolute Maximum auf \(D\).</p>', ''),
    ('5d', 3, r'\(f(x) = x^3 - 3x^2\) hat \(H(0 \mid 0)\) und \(T(2 \mid -4)\). Bestimme das absolute Maximum und das absolute Minimum auf \(D = [-0.5;\, 4]\).',
     r'<p>Randwerte: \(f(-0.5) = -0.125 - 0.75 = -0.875\), \(f(4) = 64 - 48 = 16\).</p><p>Absolutes Maximum \(16\) am Rand \(x = 4\); absolutes Minimum \(-4\) im Tiefpunkt \(x = 2\).</p>', ''),
], zwei=False)
k5 = kapitel(5, 'hoch-und-tiefpunkte', 'Hoch- und Tiefpunkte', 'K3', 45,
             r'Du liest Hoch- und Tiefpunkte am Graphen ab, unterscheidest lokale von absoluten Extremwerten — auch auf einem Intervall — und berechnest den Extrempunkt beim Grad 2 exakt.',
             ('s3-3-lp-extrema', 'Hoch- und Tiefpunkte'),
             sim5, ('s3-3-lp-kontrolle-extrema', 'Kontrollfragen zu Hoch- und Tiefpunkten'),
             fest5, [uebung('extrem-ablesen', 'Hoch- und Tiefpunkt ablesen', True), uebung('scheitel-extrem', 'Grad 2: exakt berechnen'),
                     uebung('lokal-global', 'Lokal oder absolut?')],
             auf5, f'<a href="{TS}#theorie">Themenseite 3.3, Extremalstellen</a>')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-sf">Vorwissen · GF 1.3 · GF 2.2 · SP 3.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Satz vom Nullprodukt, Ausmultiplizieren und Faktorisieren, Potenzfunktionen. Wenn das wackelt: <a href="../grundlagen/g1-3-algebraische-terme.html">GF 1.3</a>, <a href="../grundlagen/g2-2b-quadratische-gleichungen.html">GF 2.2</a> und <a href="../schwerpunkt/s3-2a-potenzfunktionen.html">SP 3.2</a>.</p>
      ''' + clipkarte('g2-2b-quadratisch-faktorisieren', 'Quadratische Gleichungen: faktorisieren statt rechnen', '1:03') + '''
      ''' + clipkarte('s3-2a-potenzfunktionen', 'Potenzfunktionen: der Exponent formt den Graphen', '0:49') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Löse: \((x-3)(x+5) = 0\) und \(x\,(2x-1) = 0\).',
     r'<p>\(\mathbb{L} = \{-5;\ 3\}\) und \(\mathbb{L} = \{0;\ 0.5\}\).</p><p class="komm">Falsch? Ein Produkt ist null, wenn ein Faktor null ist — jeden Faktor einzeln null setzen. Genau das trägt Kapitel 1. <a href="../grundlagen/g2-2b-quadratische-gleichungen.html">GF 2.2, Quadratische Gleichungen</a></p>', ''),
    ('0b', 3, r'Multipliziere aus: \((x+1)(x-2)(x+3)\).',
     r'<p>\((x+1)(x-2) = x^2 - x - 2\); mal \((x+3)\): \(x^3 + 3x^2 - x^2 - 3x - 2x - 6 = x^3 + 2x^2 - 5x - 6\).</p><p class="komm">Falsch? Erst zwei Klammern, dann das Ergebnis mit der dritten — jeder Term mit jedem. <a href="../grundlagen/g1-3-algebraische-terme.html">GF 1.3, Algebraische Terme</a></p>', ''),
    ('0c', 3, r'Faktorisiere: \(x^2 - x - 12\) · \(x^2 - 9\) · \(x^2 + 6x + 9\).',
     r'<p>\((x-4)(x+3)\) · \((x-3)(x+3)\) · \((x+3)^2\).</p><p class="komm">Falsch? Zwei Zahlen mit Produkt \(-12\) und Summe \(-1\); dann die binomischen Formeln. Der Clip oben zeigt das Verfahren.</p>', ''),
    ('0d', 2, r'Wie verlaufen die Graphen von \(y = x^3\) und \(y = x^4\)? Symmetrie und die beiden Enden.',
     r'<p>\(y = x^3\): punktsymmetrisch zum Ursprung, von links unten nach rechts oben. \(y = x^4\): achsensymmetrisch zur \(y\)-Achse, beide Enden oben.</p><p class="komm">Falsch? <a href="../schwerpunkt/s3-2a-potenzfunktionen.html">SP 3.2, Potenzfunktionen</a> — der Leitterm einer Polynomfunktion verhält sich für grosse \(|x|\) genau so (Kapitel 3).</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. Sind 0a oder 0c falsch, zuerst dorthin — ohne Nullprodukt und Faktorisieren gehen Kapitel 1 und 4 nicht.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/polynomfunktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-sf">SP 3.3 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Teil A ohne Hilfsmittel (die beiden Kompetenzen tragen im Lehrplan den Vermerk «auch ohne Hilfsmittel»), Teil B mit Taschenrechner.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Simulation und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1, 2 · G2 → 2 · G3, G4 → 3 · G5 → 4 · G6, G7 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Polynomfunktionen, Version 1.0 (04.10.2026). Gebaut aus
     scripts/lp/polynomfunktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     RLP-BM 2030, Schwerpunktfach 3.3 «Polynomfunktionen», die Kompetenzen wörtlich
     (Quelle ../Math-SP.pdf, Lerngebiet 3 «Funktionen»; gleich wie in der RLP-Box der
     Themenseite s3-3-polynomfunktionen.html):
       K1  den Zusammenhang zwischen Linearfaktoren und Nullstellen einer Polynomfunktion
           algebraisch und grafisch herstellen (mehrfache Nullstellen) (auch ohne Hilfsmittel)
       K2  den Verlauf des Graphen einer Polynomfunktion qualitativ charakterisieren
           (auch ohne Hilfsmittel)
       K3  ausgezeichnete Stellen (Nullstellen, lokale und globale Extremwerte) grafisch
           bestimmen und berechnen

     Kompetenzmatrix (Kompetenz | ohne HM | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | ja   | 1, 2, 4 | 1a–1d, 2a, 2b, 2d, 4c | G1, G2
       K2 | ja   | 2, 3    | 2a, 2c, 3a–3d          | G1, G3, G4
       K3 | nein | 4, 5    | 4a–4d, 5a–5d           | G5, G6, G7
     Kein Kapitelziel ohne Kompetenz. Teil A des Gesamttests (K1, K2) ohne Hilfsmittel,
     Teil B (K3) mit Taschenrechner.

     Bewusst weggelassen (→ Themenseite): der Leitterm-Zoom als eigene Animation (hier im
     Clip und als Schalter in Simulation 3), die Anwendungen A4–A6 der Themenseite (Truthahn,
     Temperatur, Tank) und die Vertiefung A7. Die exakte Berechnung von Extremstellen ab
     Grad 3 gehört zur Differentialrechnung und ist nicht Teil von SP 3.3.

     Konventionen wie auf der Themenseite: Grad n, Leitkoeffizient aₙ, Linearfaktor­
     darstellung a·(x − x₁)(x − x₂)…, H und T, lokales/absolutes Maximum. Abweichung mit
     Grund: Die Themenseite schreibt beim Scheitel x_S, das Leitprogramm wie die anderen
     Leitprogramme x_s; und «Summenform» steht auf der Themenseite nur in der Animation —
     hier ist es der Name der ausmultiplizierten Darstellung.

     Muster je Kapitel: ① Einführungsclip (zeigt alles, Auftrag am Schluss) → ② Simulation
     mit Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit
     Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus
     LaTeX (downloads/leitprogramme/polynomfunktionen/*.tex). Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Polynomfunktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel und Gesamttest, rund fünf Lektionen.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Schwerpunktfach 3.3</span>
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
    <p class="lekt">Lektion 1</p>
    <ol>
      <li><a href="#k1"><span class="nr">1</span><span>Linearfaktoren</span></a></li>
    </ol>
    <p class="lekt">Lektion 2</p>
    <ol>
      <li><a href="#k2"><span class="nr">2</span><span>Mehrfache Nullstellen</span></a></li>
    </ol>
    <p class="lekt">Lektion 3</p>
    <ol>
      <li><a href="#k3"><span class="nr">3</span><span>Globalverlauf</span></a></li>
    </ol>
    <p class="lekt">Lektion 4</p>
    <ol>
      <li><a href="#k4"><span class="nr">4</span><span>Nullstellen berechnen</span></a></li>
    </ol>
    <p class="lekt">Lektion 5</p>
    <ol>
      <li><a href="#k5"><span class="nr">5</span><span>Hoch- und Tiefpunkte</span></a></li>
    </ol>
    <p class="lekt">Abschluss</p>
    <ol>
      <li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li>
    </ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 6 Aufgabenblöcken bearbeitet</p>
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
        <p class="rlp-quelle">RLP-BM 2030, Schwerpunktfach 3.3 — alle drei Kompetenzen des Teilgebiets.</p>
        <ul>
          <li><b>K1</b> den Zusammenhang zwischen Linearfaktoren und Nullstellen einer Polynomfunktion algebraisch und grafisch herstellen (mehrfache Nullstellen) <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1, 2, 4</li>
          <li><b>K2</b> den Verlauf des Graphen einer Polynomfunktion qualitativ charakterisieren <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 2, 3</li>
          <li><b>K3</b> ausgezeichnete Stellen (Nullstellen, lokale und globale Extremwerte) grafisch bestimmen und berechnen — Kapitel 4, 5</li>
        </ul>
        <p class="rlp-quelle">Nicht hier, sondern auf der <a href="../schwerpunkt/s3-3-polynomfunktionen.html">Themenseite 3.3</a>: die Anwendungsaufgaben A4–A7. Die exakte Berechnung von Extremstellen ab Grad 3 kommt mit der Differentialrechnung.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Polynomfunktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (04.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 40 · K4 40 · K5 45 · Gesamttest 30 = 245 min
# Die fünf Kapitel sind die fünf Lektionen; Vorwissen und Gesamttest kommen davor und danach.
body = (oben + band('Vorab', 'Vorwissen') + k0 + band(1, 'Linearfaktoren und Nullstellen') + k1
        + band(2, 'Mehrfache Nullstellen') + k2 + band(3, 'Der Globalverlauf') + k3
        + band(4, 'Nullstellen berechnen') + k4 + band(5, 'Hoch- und Tiefpunkte') + k5
        + band('Abschluss', 'Gesamttest') + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
