"""Baut leitprogramme/vierecke.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/vierecke/seite.py

Leitprogramm zur Themenseite GF 5.2b Vierecke, im Kapitelmuster und mit dem Geometrie-Arbeitsbereich des
Leitprogramms Planimetrie (in der Fassung von Trigonometrische Berechnungen). Liest Kopf (inkl. <style>) und
Grundskript aus der bestehenden Seite, ersetzt Inhalt, eigenen Stilblock (seite.css) und Seitenskript (seite.js)
und schreibt die Seite neu. Beim ersten Lauf kommt das Gerüst aus leitprogramme/planimetrie.html, mit leerem
SEO-Block und noindex; danach bleibt der SEO-Block, wie er ist (build-seo.py schreibt ihn). Wiederholbar.
Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegen seite.js und seite.css
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/vierecke.html'
NAME = 'Vierecke'
SCHLUESSEL = 'lp-vierecke-'
MARKE_CSS = '\n/* ════════ Vierecke'
MARKE_JS = '<script>\n/* Leitprogramm Vierecke —'
# Unverlinkt bis zur Freischaltung (HOWTO-leitprogramme §13/§15): Nur beim ersten Lauf wird ein leerer SEO-Block
# mit noindex gesetzt; einen vorhandenen Block (später mit JSON-LD aus build-seo.py) nie überschreiben.
SEO_LEER = ('<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
            '<meta name="robots" content="noindex, nofollow">\n<!-- SEO:ENDE -->')

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/planimetrie.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = alt[:a] + SEO_LEER + alt[b:]
    alt = alt.replace('<title>Leitprogramm Planimetrie</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-planimetrie-', SCHLUESSEL)

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Planimetrie', MARKE_CSS):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
kopf = kopf.rstrip('\n') + '\n\n'
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Planimetrie —'), alt.find(MARKE_JS)) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Planimetrie', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 8. Oktober 2026', fuss)

CSS = open(SP + 'seite.css').read()


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf), abgerundet (HOWTO §7)."""
    p = R + 'clips/' + name + '.json'
    if not os.path.exists(p):
        return '0:00'
    d = json.load(open(p))
    t = int(sum(s.get('dauer', 0) for s in d['szenen']))
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


def uebung(typ, titel):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(sim, p, label, mn, mx, st, val, akz='grau', einheit=''):
    return (f'<div class="sl-grp akz-{akz}"><label for="{sim}-{p}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>')


def bereich(nr, label, regler_):
    return f'''      <figure class="sim geo" id="sim{nr}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="{label}"></svg>
        <div class="g-eingabe" hidden></div>
        <div class="g-rueck" aria-live="polite"></div>
        <div class="sl-row">
          {regler_}
        </div>
      </figure>'''


def test(tid, titel, punkte, aufgaben, zwei=False):
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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 5.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TB = '../grundlagen/g5-2b-vierecke.html'
TA = '../grundlagen/g5-2a-dreiecke.html'


def fig(daten, fenster, breite=220, hoehe=150, karo=False, label='Figur zur Aufgabe'):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}"'
            f'{" data-karo=" + chr(34) + "ja" + chr(34) if karo else ""} aria-label="{label}" '
            f'data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


def ecken(*e):
    return [['p', p] for p, _, _, _ in e] + [['t', p, n, 'ecke', dx, dy] for p, n, dx, dy in e]


# ------------------------------------------------------------------ Kapitel 1
sim1 = bereich(1, 'Trapez ABCD mit fester Grundseite a = 5 cm; obere Seite c, Höhe h und Versatz v der oberen Seite sind einstellbar',
               regler('s1', 'c', 'obere Seite c', 1, 6, 0.5, 3.5, einheit=' cm') + '\n          '
               + regler('s1', 'v', 'Versatz v', -3, 4, 0.5, 1, einheit=' cm') + '\n          '
               + regler('s1', 'h', 'Höhe h', 1, 5, 0.5, 3.5, einheit=' cm'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Vierecks-Familie</div>
          <p>Ecken \(A, B, C, D\) gegen den Uhrzeigersinn; Seiten \(a = AB\), \(b = BC\), \(c = CD\), \(d = DA\); Winkel \(\alpha\) bei \(A\) bis \(\delta\) bei \(D\); Diagonalen \(e = AC\) und \(f = BD\).</p>
          <p><b>Winkelsumme:</b> \(\alpha + \beta + \gamma + \delta = 360°\) — die Diagonale \(e\) zerlegt jedes Viereck in zwei Dreiecke mit je \(180°\).</p>
          <p><b>Winkel an Parallelen:</b> Liegen zwei Winkel an derselben Seite zwischen zwei parallelen Seiten, ergänzen sie sich zu \(180°\) — verlängert man die eine Parallele, ist der Nebenwinkel des einen ein Stufenwinkel zum anderen.</p>
          <table class="eig">
            <tr><th>Viereck</th><th>Bedingung</th><th>dazu gilt immer</th></tr>
            <tr><td>Trapez</td><td>ein Paar paralleler Gegenseiten, \(a \parallel c\)</td><td>Die zwei Winkel an einem Schenkel ergänzen sich zu \(180°\).</td></tr>
            <tr><td>Parallelogramm</td><td>beide Paare von Gegenseiten parallel</td><td>Gegenseiten gleich lang; gegenüberliegende Winkel gleich, benachbarte ergänzen sich zu \(180°\); die Diagonalen halbieren sich.</td></tr>
            <tr><td>Rechteck</td><td>Parallelogramm mit einem rechten Winkel</td><td>vier rechte Winkel; die Diagonalen sind gleich lang.</td></tr>
            <tr><td>Rhombus (Raute)</td><td>Parallelogramm mit vier gleich langen Seiten</td><td>Die Diagonalen stehen senkrecht aufeinander und halbieren die Winkel.</td></tr>
            <tr><td>Quadrat</td><td>Rechteck und Rhombus zugleich</td><td>alles oben</td></tr>
          </table>
          <p>Jede Bedingung macht spezieller, und alles Bisherige gilt weiter: Jedes Quadrat ist ein Rechteck und ein Rhombus, jedes Rechteck und jeder Rhombus ein Parallelogramm, jedes Parallelogramm ein Trapez. Ein Trapez hat dazu <em>mindestens</em> ein Paar paralleler Seiten (so auch die Themenseite).</p>
          <p>Das <b>gleichschenklige</b> Trapez ist achsensymmetrisch: Seine Symmetrieachse geht senkrecht durch die Mitten von \(a\) und \(c\). Darum ist \(b = d\), \(\alpha = \beta\) und \(\gamma = \delta\), und die Diagonalen sind gleich lang. \(b = d\) allein genügt nicht: Auch jedes Parallelogramm hat \(b = d\) und ist doch (ausser dem Rechteck) nicht symmetrisch.</p>
          <p><b>Umgekehrt — das Viereck an den Diagonalen erkennen:</b> Halbieren sich die Diagonalen gegenseitig, ist es ein Parallelogramm. Sind sie dazu gleich lang, ist es ein Rechteck; stehen sie dazu senkrecht, ein Rhombus; gilt beides, ein Quadrat. Ohne «halbieren» geht der Schluss nicht: Gleich lange Diagonalen hat auch das gleichschenklige Trapez, senkrechte auch das Trapez mit \(c = 3\), \(v = 1\), \(h = 4\) im Arbeitsbereich oben.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Ein Quadrat ist kein Rechteck.» Doch: Es hat vier rechte Winkel. Es hat nur noch mehr — vier gleiche Seiten.</p>
          <p>Gleich lange Diagonalen beim Rhombus: Sie stehen senkrecht, gleich lang sind sie nur beim Quadrat.</p>
          <p>Im Trapez gehören die Winkel am selben <b>Schenkel</b> zusammen (\(\alpha + \delta = 180°\)), nicht die gegenüberliegenden.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 2, r'Warum ist jedes Quadrat ein Rhombus, aber nicht jeder Rhombus ein Quadrat?',
     r'<p>Ein Rhombus braucht vier gleich lange Seiten — die hat jedes Quadrat. Ein Quadrat braucht zusätzlich vier rechte Winkel; ein schiefer Rhombus hat sie nicht.</p>', ''),
    ('1b', 3, r'Im Parallelogramm \(ABCD\) ist \(\alpha = 58°\). Berechne \(\beta\), \(\gamma\) und \(\delta\) und begründe mit den parallelen Seiten.',
     r'<p>\(\beta = 180° - 58° = 122°\) (benachbart an der Seite \(a\), zwischen den Parallelen \(AD\) und \(BC\)); \(\gamma = \alpha = 58°\) (gegenüber); \(\delta = \beta = 122°\). Probe: \(58° + 122° + 58° + 122° = 360°\).</p>', ''),
    ('1c', 3, r'Welches Viereck ist im Bild gezeichnet (1 Häuschen = 1 cm)? Begründe mit den Häuschen. Ist es ein Rhombus?',
     r'<p>\(AB\) und \(DC\) sind waagrecht und je \(4\,\text{cm}\) lang; \(AD\) und \(BC\) gehen beide 2 nach rechts und 3 nach oben, sind also parallel. Zwei Paare paralleler Gegenseiten: ein <b>Parallelogramm</b>. Kein Rhombus, denn \(AD = \sqrt{2^2 + 3^2} = \sqrt{13} \approx 3.61\,\text{cm} \neq 4\,\text{cm}\); kein Rechteck, denn bei \(A\) ist kein rechter Winkel.</p>',
     fig([['v', [[0, 0], [4, 0], [6, 3], [2, 3]]]] + ecken(([0, 0], 'A', -8, 12), ([4, 0], 'B', 8, 12), ([6, 3], 'C', 8, -4), ([2, 3], 'D', -8, -4)), '-0.8,7,-0.8', 220, 132, True,
         'Viereck ABCD auf Häuschenpapier: A(0|0), B(4|0), C(6|3), D(2|3)')),
    ('1d', 2, r'Trapez \(ABCD\) mit \(AB \parallel CD\), \(\alpha = 72°\) und \(\beta = 64°\). Berechne \(\gamma\) und \(\delta\).',
     r'<p>\(\delta = 180° - 72° = 108°\) (am Schenkel \(d\)); \(\gamma = 180° - 64° = 116°\) (am Schenkel \(b\)). Probe: \(72° + 64° + 116° + 108° = 360°\).</p><p class="komm">Wer \(\gamma = 72°\) schreibt, rechnet wie im Parallelogramm — im Trapez sind gegenüberliegende Winkel nicht gleich.</p>', ''),
    ('1e', 2, r'Im Rhombus im Bild ist \(\alpha = 50°\); die Diagonale \(e = AC\) ist eingezeichnet. Welche Winkel bildet sie bei \(A\) mit den Seiten \(a\) und \(d\)? Wie gross sind \(\beta\), \(\gamma\) und \(\delta\)?',
     r'<p>Die Diagonale halbiert \(\alpha\): je \(25°\). \(\beta = \delta = 130°\), \(\gamma = 50°\).</p>',
     # Rhombus mit Seite 4: D = 4(cos 50°|sin 50°) = (2.571|3.064), C = B + D = (6.571|3.064); e unter 25° (zahlen.py)
     fig([['v', [[0, 0], [4, 0], [6.571, 3.064], [2.571, 3.064]]], ['s', [0, 0], [6.571, 3.064], 'hilfe'], ['w', [0, 0], [4, 0], [2.571, 3.064], '50°', 30],
          ['t', [3.138, 1.849], 'e', 'seite', 0, 4]] + ecken(([0, 0], 'A', -8, 12), ([4, 0], 'B', 8, 12), ([6.571, 3.064], 'C', 8, -4), ([2.571, 3.064], 'D', -8, -4)),
         '-0.8,7.4,-0.8', 230, 125, False, 'Rhombus ABCD mit α = 50° bei A und eingezeichneter Diagonale e = AC')),
    ('1f', 2, r'Warum ist ein Viereck mit zwei gleich langen Diagonalen noch nicht sicher ein Rechteck? Was muss für die Diagonalen noch gelten?',
     r'<p>Auch ein gleichschenkliges Trapez, das kein Rechteck ist, hat gleich lange Diagonalen (sie sind Spiegelbilder an der Symmetrieachse). Die Diagonalen müssen sich zusätzlich gegenseitig halbieren: Dann ist das Viereck ein Parallelogramm, und ein Parallelogramm mit gleich langen Diagonalen ist ein Rechteck.</p>', ''),
])
k1 = kapitel(1, 'familie', 'Die Vierecks-Familie', 40,
             r'Du ordnest Trapez, Parallelogramm, Rechteck, Rhombus und Quadrat nach ihren Bedingungen, beschreibst ihre Seiten, Winkel und Diagonalen, erkennst ein Viereck an seinen Diagonalen und berechnest Winkel.',
             ('g5-2b-lp-familie', 'Die Vierecks-Familie'), sim1, ('g5-2b-lp-kontrolle-familie', 'Kontrollfragen zur Vierecks-Familie'),
             fest1, [uebung('familie', 'Wahr oder falsch?'), uebung('viereck-winkel', 'Winkel im Viereck')],
             auf1, f'<a href="{TB}#typen">Themenseite 5.2b, Vierecks-Hierarchie</a> und <a href="{TB}#definition">Definition</a>', komp='K1; K2')

# ------------------------------------------------------------------ Kapitel 2
sim2 = bereich(2, 'Parallelogramm ABCD; Grundseite a, Höhe h und Versatz v der oberen Seite sind einstellbar',
               regler('s2', 'a', 'Grundseite a', 2, 9, 0.5, 8, einheit=' cm') + '\n          '
               + regler('s2', 'h', 'Höhe h', 1, 5, 0.5, 3, einheit=' cm') + '\n          '
               + regler('s2', 'v', 'Versatz v', -3, 5, 0.5, 4, einheit=' cm'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fläche und Umfang</div>
          <table class="eig">
            <tr><th>Viereck</th><th>Fläche</th><th>Umfang</th></tr>
            <tr><td>Rechteck (Seiten \(a\), \(b\))</td><td>\(A = a \cdot b\)</td><td>\(U = 2(a + b)\)</td></tr>
            <tr><td>Quadrat (Seite \(a\))</td><td>\(A = a^2\)</td><td>\(U = 4a\)</td></tr>
            <tr><td>Parallelogramm</td><td>\(A = a \cdot h_a = b \cdot h_b\)</td><td>\(U = 2(a + b)\)</td></tr>
            <tr><td>Rhombus</td><td>\(A = a \cdot h = \tfrac{1}{2}\, e \cdot f\)</td><td>\(U = 4a\)</td></tr>
          </table>
          <p><b>Warum:</b> Beim Parallelogramm schneidest du auf einer Seite ein Dreieck ab und setzt es auf der anderen an — es entsteht ein Rechteck mit der Grundseite \(a\) und der Höhe \(h\). Der Rhombus füllt genau die Hälfte des Rechtecks \(e \times f\) um seine Diagonalen.</p>
          <p><b>Höhe = Abstand:</b> \(h_a\) ist der senkrechte Abstand der Seite \(a\) von ihrer Gegenseite \(c\), \(h_b\) der Abstand der Seiten \(b = \overline{BC}\) und \(\overline{AD}\). Die Fläche ist dieselbe, welche Seite auch Grundseite ist: \(h_b = \tfrac{A}{b}\).</p>
          <p>Verschiebst du die obere Seite (Scherung), bleiben \(a\), \(h\) und damit \(A\) gleich; der Umfang ändert sich in der Regel, weil \(b\) länger oder kürzer wird (gleich bleibt er etwa, wenn du \(v\) durch \(-v\) ersetzt).</p>
          <p>Einheiten zuerst angleichen: \(1\,\text{m}^2 = 10\,000\,\text{cm}^2\). Die Themenseite schreibt die Parallelogrammfläche auch \(g \cdot h\): Grundseite mal zugehörige Höhe.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die schräge Seite als Höhe nehmen: \(a \cdot b\) ist zu gross. Die Höhe steht senkrecht.</p>
          <p>Das \(\tfrac{1}{2}\) verwechseln: Beim Parallelogramm gibt es keins (das wäre das Dreieck), beim Rhombus mit den Diagonalen schon.</p>
          <p>Bei \(h_b\) wie beim Dreieck rechnen: \(\tfrac{2A}{b}\) ist doppelt so gross.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'Zeichne im Bild die Höhe zur Seite \(AB\) ein (1 Häuschen = 1 cm), lies ab, was du brauchst, und berechne die Fläche. Warum brauchst du die Länge der schrägen Seite nicht?',
     r'<p>Die Höhe ist das Lot von \(D\) (oder \(C\)) auf \(AB\): \(h = 3\,\text{cm}\); \(a = AB = 5\,\text{cm}\). \(A = 5 \cdot 3 = 15\,\text{cm}^2\). Die schräge Seite kommt in der Fläche nicht vor: Schneidet man das Dreieck links ab und setzt es rechts an, entsteht ein Rechteck \(5 \times 3\).</p>',
     fig([['v', [[0, 0], [5, 0], [7, 3], [2, 3]]]] + ecken(([0, 0], 'A', -8, 12), ([5, 0], 'B', 8, 12), ([7, 3], 'C', 8, -4), ([2, 3], 'D', -8, -4)), '-0.8,8,-0.8', 230, 128, True,
         'Parallelogramm ABCD auf Häuschenpapier: A(0|0), B(5|0), C(7|3), D(2|3)')),
    ('2b', 2, r'Ein Rhombus hat die Diagonalen \(e = 12\,\text{cm}\) und \(f = 9\,\text{cm}\). Berechne die Fläche und begründe die Formel.',
     r'<p>\(A = \tfrac{1}{2} \cdot 12 \cdot 9 = 54\,\text{cm}^2\). Die Diagonalen teilen den Rhombus in vier rechtwinklige Dreiecke; das Rechteck \(12 \times 9\) um die Diagonalen besteht aus acht solchen Dreiecken — der Rhombus ist die Hälfte.</p>', ''),
    ('2c', 3, r'Eine Tischplatte ist \(1.2\,\text{m}\) lang und \(80\,\text{cm}\) breit. Berechne die Fläche in \(\text{m}^2\) und in \(\text{cm}^2\) und den Umfang.',
     r'<p>\(A = 1.2\,\text{m} \cdot 0.8\,\text{m} = 0.96\,\text{m}^2 = 9600\,\text{cm}^2\); \(U = 2(1.2 + 0.8) = 4\,\text{m}\).</p><p class="komm">Wer \(1.2 \cdot 80 = 96\) rechnet, mischt m und cm.</p>', ''),
    ('2d', 3, r'Ein Parallelogramm hat \(a = 12\,\text{cm}\), \(b = 7.5\,\text{cm}\) und die Höhe \(h_a = 5\,\text{cm}\). Berechne Fläche, Umfang und den Abstand \(h_b\) der Seiten \(\overline{AD}\) und \(\overline{BC}\).',
     r'<p>\(A = 12 \cdot 5 = 60\,\text{cm}^2\); \(U = 2(12 + 7.5) = 39\,\text{cm}\); \(h_b = \tfrac{60}{7.5} = 8\,\text{cm}\).</p>', ''),
    ('2e', 2, r'Warum gilt für den Rhombus auch \(A = a \cdot h\)? Ein Rhombus hat \(e = 18\,\text{cm}\), \(f = 24\,\text{cm}\) und die Seite \(a = 15\,\text{cm}\). Wie gross ist seine Höhe?',
     r'<p>Jeder Rhombus ist ein Parallelogramm, also gilt \(A = a \cdot h\). Mit den Diagonalen: \(A = \tfrac{1}{2} \cdot 18 \cdot 24 = 216\,\text{cm}^2\), also \(h = \tfrac{216}{15} = 14.4\,\text{cm}\).</p>', ''),
])
k2 = kapitel(2, 'flaeche', 'Fläche und Umfang', 40,
             r'Du begründest \(A = a \cdot h\) für das Parallelogramm mit dem Rechteck, berechnest Umfang und Fläche von Rechteck, Quadrat, Parallelogramm und Rhombus und bestimmst eine Höhe als Abstand zweier paralleler Seiten.',
             ('g5-2b-lp-flaeche', 'Fläche und Umfang'), sim2, ('g5-2b-lp-kontrolle-flaeche', 'Kontrollfragen zu Fläche und Umfang'),
             fest2, [uebung('pa-flaeche', 'Fläche und Umfang'), uebung('raute-ef', 'Rhombus mit den Diagonalen'), uebung('abstand', 'Abstand zweier Seiten')],
             auf2, f'<a href="{TB}#theorie">Themenseite 5.2b, Umfang und Flächeninhalt</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = bereich(3, 'Trapez ABCD mit fester Grundseite a = 6 cm; obere Seite c, Höhe h und Versatz v sind einstellbar; die Mittellinie ist orange',
               regler('s3', 'c', 'obere Seite c', 1, 6, 0.5, 4, einheit=' cm') + '\n          '
               + regler('s3', 'h', 'Höhe h', 1, 5, 0.5, 3, einheit=' cm') + '\n          '
               + regler('s3', 'v', 'Versatz v', -2, 4, 0.5, 0.5, einheit=' cm'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Trapez und Mittellinie</div>
          <p>Im Trapez sind die Grundseiten \(a\) und \(c\) parallel; die <b>Schenkel</b> \(b\) und \(d\) verbinden sie. Die <b>Höhe</b> \(h\) ist der Abstand der beiden Parallelen.</p>
          <p>Die <b>Mittellinie</b> \(m\) verbindet die Mitten der Schenkel. Sie ist parallel zu \(a\) und \(c\), liegt auf halber Höhe und ist das Mittel der Parallelseiten:</p>
          <p>\[ m = \tfrac{1}{2}(a + c) \qquad A = \tfrac{1}{2}(a + c) \cdot h = m \cdot h \qquad U = a + b + c + d \]</p>
          <p><b>Warum:</b> Zwei gleiche Trapeze, das zweite um \(180°\) gedreht, ergeben ein Parallelogramm mit der Grundseite \(a + c\) und der Höhe \(h\). Ein Trapez ist die Hälfte davon.</p>
          <p><b>Rückwärts:</b> \(h = \tfrac{A}{m}\). Fehlt \(c\): \(m = \tfrac{A}{h}\), dann \(c = 2m - a\).</p>
          <p>Verschiebst du die obere Seite, bleiben \(a\), \(c\) und \(h\) — also auch \(m\) und \(A\). Nur der Umfang kann sich ändern.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Schenkel als Höhe nehmen: Die Höhe steht senkrecht auf \(a\) und \(c\) und ist kürzer als ein schräger Schenkel.</p>
          <p>Das \(\tfrac{1}{2}\) vergessen: \((a + c) \cdot h\) ist das Parallelogramm aus zwei Trapezen.</p>
          <p>Rückwärts \(c = \tfrac{2A}{h}\) schreiben: Das ist \(a + c\); es fehlt das \(-\,a\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 2, r'Trapez mit \(a = 11\,\text{cm}\), \(c = 7\,\text{cm}\) und \(h = 4.5\,\text{cm}\): Berechne die Mittellinie und die Fläche.',
     r'<p>\(m = \tfrac{1}{2}(11 + 7) = 9\,\text{cm}\); \(A = 9 \cdot 4.5 = 40.5\,\text{cm}^2\).</p>', ''),
    ('3b', 3, r'Zeichne im Bild die Mittellinie ein (1 Häuschen = 1 cm). Lies \(a\), \(c\) und \(h\) ab und berechne \(m\) und \(A\).',
     r'<p>\(a = 8\,\text{cm}\), \(c = 5\,\text{cm}\), \(h = 3\,\text{cm}\). Die Mittellinie verbindet die Mitten von \(AD\) und \(BC\), auf halber Höhe \(1.5\,\text{cm}\): \(m = \tfrac{1}{2}(8 + 5) = 6.5\,\text{cm}\); \(A = 6.5 \cdot 3 = 19.5\,\text{cm}^2\).</p>',
     fig([['v', [[0, 0], [8, 0], [6, 3], [1, 3]]]] + ecken(([0, 0], 'A', -8, 12), ([8, 0], 'B', 8, 12), ([6, 3], 'C', 8, -4), ([1, 3], 'D', -8, -4)), '-0.8,8.8,-0.8', 240, 118, True,
         'Trapez ABCD auf Häuschenpapier: A(0|0), B(8|0), C(6|3), D(1|3)')),
    ('3c', 3, r'Ein Wassergraben hat einen trapezförmigen Querschnitt: unten \(1.2\,\text{m}\), oben \(3\,\text{m}\) breit. Die Querschnittsfläche ist \(2.73\,\text{m}^2\). Wie tief ist der Graben? Skizziere den Querschnitt.',
     r'<p>\(m = \tfrac{1}{2}(3 + 1.2) = 2.1\,\text{m}\); \(h = \tfrac{2.73}{2.1} = 1.3\,\text{m}\).</p><p class="komm">\(2.73 : 4.2 = 0.65\) ist die halbe Tiefe: geteilt durch \(a + c\) statt durch \(m\).</p>', ''),
    ('3d', 2, r'Begründe mit zwei gleichen Trapezen, warum \(A = \tfrac{1}{2}(a + c) \cdot h\) gilt.',
     r'<p>Dreht man eine Kopie um \(180°\) und legt sie an einen Schenkel, ergänzen sich die Parallelseiten zu einer Strecke \(a + c\) unten und oben: Es entsteht ein Parallelogramm mit Grundseite \(a + c\) und Höhe \(h\), Fläche \((a + c) \cdot h\). Ein Trapez ist die Hälfte.</p>', ''),
    ('3e', 2, r'Lena rechnet für ein Trapez mit \(a = 10\,\text{cm}\), \(c = 4\,\text{cm}\) und zwei schrägen Schenkeln von je \(5\,\text{cm}\): «\(A = \tfrac{1}{2}(10 + 4) \cdot 5 = 35\,\text{cm}^2\).» Was ist falsch? Ist die richtige Fläche grösser oder kleiner?',
     r'<p>Sie setzt den Schenkel als Höhe ein. Die Höhe steht senkrecht und ist kürzer als ein schräger Schenkel — die richtige Fläche ist kleiner als \(35\,\text{cm}^2\). (Mit Kapitel 4: \(h = 4\,\text{cm}\), \(A = 28\,\text{cm}^2\).)</p>', ''),
])
k3 = kapitel(3, 'trapez', 'Trapez und Mittellinie', 35,
             r'Du erklärst die Mittellinie des Trapezes, begründest \(A = \tfrac{1}{2}(a + c) \cdot h = m \cdot h\) und berechnest Mittellinie und Fläche — auch rückwärts die Höhe oder eine Parallelseite.',
             ('g5-2b-lp-trapez', 'Trapez und Mittellinie'), sim3, ('g5-2b-lp-kontrolle-trapez', 'Kontrollfragen zum Trapez'),
             fest3, [uebung('trapez', 'Mittellinie und Fläche'), uebung('trapez-rueck', 'Höhe oder Seite rückwärts')],
             auf3, f'<a href="{TB}#scherung">Themenseite 5.2b, Scherung</a> und <a href="{TB}#theorie">Umfang und Flächeninhalt</a>', komp='K1; K2')

# ------------------------------------------------------------------ Kapitel 4
sim4 = bereich(4, 'Gleichschenkliges Trapez ABCD mit Grundseite a, oberer Seite c und Höhe h; das linke rechtwinklige Teildreieck ist grün',
               regler('s4', 'a', 'Grundseite a', 6, 12, 1, 12, einheit=' cm') + '\n          '
               + regler('s4', 'c', 'obere Seite c', 1, 10, 1, 4, einheit=' cm') + '\n          '
               + regler('s4', 'h', 'Höhe h', 1, 6, 0.5, 3, einheit=' cm'))
sim5 = bereich(5, 'Rhombus ABCD aus den Diagonalen e und f; ein rechtwinkliges Teildreieck aus den halben Diagonalen ist grün',
               regler('s5', 'e', 'Diagonale e', 2, 16, 1, 8, einheit=' cm') + '\n          '
               + regler('s5', 'f', 'Diagonale f', 2, 16, 1, 6, einheit=' cm'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fehlende Längen mit Pythagoras</div>
          <p><b>Vorgehen:</b> Skizze → rechtwinkliges Teildreieck suchen → Katheten und Hypotenuse benennen (die Hypotenuse liegt dem rechten Winkel gegenüber) → Pythagoras \(a^2 + b^2 = c^2\) → in die Formel für Umfang oder Fläche einsetzen.</p>
          <table class="eig">
            <tr><th>Viereck</th><th>rechtwinkliges Teildreieck und Formel</th></tr>
            <tr><td>Rechteck</td><td>die Seiten \(a\), \(b\); Hypotenuse: die Diagonale<br>\(d = \sqrt{a^2 + b^2}\)</td></tr>
            <tr><td>Quadrat</td><td>zweimal die Seite \(a\); Hypotenuse: die Diagonale<br>\(d = \sqrt{a^2 + a^2} = a\sqrt{2}\)</td></tr>
            <tr><td>Rhombus</td><td>die halben Diagonalen; Hypotenuse: die Seite<br>\(a = \sqrt{(\tfrac{e}{2})^2 + (\tfrac{f}{2})^2}\)</td></tr>
            <tr><td>Parallelogramm</td><td>Höhe \(h\) von \(D\) und das Stück \(\overline{AF}\) bis zum Fusspunkt \(F\); Hypotenuse: die Seite \(\overline{AD}\)<br>\(h = \sqrt{\overline{AD}^2 - \overline{AF}^2}\)</td></tr>
            <tr><td>gleichschenkliges Trapez</td><td>Höhe \(h\) und Überstand \(\text{ü} = \tfrac{a - c}{2}\); Hypotenuse: der Schenkel \(s\)<br>\(h = \sqrt{s^2 - \text{ü}^2}\)</td></tr>
          </table>
          <p>Im Rhombus stehen die Diagonalen senkrecht und halbieren sich — darum die Hälften. Im gleichschenkligen Trapez verteilt sich der Unterschied \(a - c\) auf zwei gleiche Überstände links und rechts.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(d = a\sqrt{2}\) gilt nur im Quadrat. Im Rechteck \(12 \times 5\) ist \(d = 13\), nicht \(12\sqrt{2} \approx 16.97\).</p>
          <p>Den ganzen Unterschied \(a - c\) als Überstand nehmen, beim Rhombus die ganzen Diagonalen statt der Hälften.</p>
          <p>Längen addieren statt Quadrate: \(\sqrt{3^2 + 4^2} = 5\), nicht \(3 + 4\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Ein Fernseher hat einen Bildschirm von \(89\,\text{cm}\) Breite und \(50\,\text{cm}\) Höhe. Wie lang ist die Diagonale in cm und in Zoll (\(1\,\text{Zoll} = 2.54\,\text{cm}\))?',
     r'<p>\(d = \sqrt{89^2 + 50^2} = \sqrt{10\,421} \approx 102.08\,\text{cm}\); \(102.08 : 2.54 \approx 40.19\,\text{Zoll}\).</p>', ''),
    ('4b', 3, r'Der Rhombus im Bild hat die Diagonalen \(e = 48\,\text{cm}\) und \(f = 14\,\text{cm}\) (verkleinert gezeichnet). Berechne die Seite, den Umfang und die Fläche.',
     r'<p>Halbe Diagonalen \(24\) und \(7\): \(a = \sqrt{24^2 + 7^2} = \sqrt{625} = 25\,\text{cm}\); \(U = 4 \cdot 25 = 100\,\text{cm}\); \(A = \tfrac{1}{2} \cdot 48 \cdot 14 = 336\,\text{cm}^2\).</p><p class="komm">\(\sqrt{48^2 + 14^2} = 50\) ist doppelt so lang: Die Katheten sind die Hälften.</p>',
     fig([['v', [[-24, 0], [0, -7], [24, 0], [0, 7]]], ['s', [-24, 0], [24, 0], 'hilfe'], ['s', [0, -7], [0, 7], 'hilfe'], ['r', [0, 0], [1, 0], [0, 1]],
          ['t', [12, 0], 'e = 48 cm', 'mass', 0, 13], ['t', [0, 3.5], 'f = 14 cm', 'mass', 5, 4, 'start']] + ecken(([-24, 0], 'A', -9, 4), ([0, -7], 'B', 0, 13), ([24, 0], 'C', 9, 4), ([0, 7], 'D', 0, -6)),
         '-27,27,-10.5', 270, 110, False, 'Rhombus mit waagrechter Diagonale e = AC = 48 cm und senkrechter Diagonale f = BD = 14 cm')),
    ('4c', 4, r'Gleichschenkliges Trapez mit \(a = 20\,\text{cm}\), \(c = 12\,\text{cm}\) und Schenkeln von \(8.5\,\text{cm}\). Berechne Höhe, Fläche und Umfang. Skizziere das Teildreieck.',
     r'<p>Überstand \(\tfrac{20 - 12}{2} = 4\,\text{cm}\); \(h = \sqrt{8.5^2 - 4^2} = \sqrt{56.25} = 7.5\,\text{cm}\). \(A = \tfrac{1}{2}(20 + 12) \cdot 7.5 = 120\,\text{cm}^2\); \(U = 20 + 12 + 2 \cdot 8.5 = 49\,\text{cm}\).</p>', ''),
    ('4d', 2, r'Warum gilt \(d = a\sqrt{2}\) nur im Quadrat? Was gilt im Rechteck?',
     r'<p>Im Quadrat sind beide Katheten des Teildreiecks gleich \(a\): \(d = \sqrt{a^2 + a^2} = \sqrt{2a^2} = a\sqrt{2}\). Im Rechteck sind sie verschieden: \(d = \sqrt{a^2 + b^2}\).</p>', ''),
    ('4e', 2, r'Ein Quadrat hat die Diagonale \(10\,\text{cm}\). Wie lang ist eine Seite, wie gross die Fläche? Tipp: Ein Quadrat ist auch ein Rhombus.',
     r'<p>\(a = \tfrac{10}{\sqrt{2}} \approx 7.07\,\text{cm}\). Fläche mit den Diagonalen: \(A = \tfrac{1}{2} \cdot 10 \cdot 10 = 50\,\text{cm}^2\) (Probe: \(7.07^2 \approx 50\)).</p>', ''),
])
k4 = kapitel(4, 'laengen', 'Fehlende Längen', 45,
             r'Du findest im Viereck das rechtwinklige Teildreieck, berechnest mit Pythagoras Diagonalen, Seiten und Höhen von Rechteck, Quadrat, Rhombus, Parallelogramm und gleichschenkligem Trapez und setzt sie in Umfang und Fläche ein.',
             ('g5-2b-lp-laengen', 'Fehlende Längen mit Pythagoras'), sim4 + '\n' + sim5, ('g5-2b-lp-kontrolle-laengen', 'Kontrollfragen zu fehlenden Längen'),
             fest4, [uebung('diagonale', 'Diagonale im Rechteck und Quadrat'), uebung('raute-seite', 'Seite und Diagonale im Rhombus'), uebung('trapez-hoehe', 'Höhe im Trapez und im Parallelogramm')],
             auf4, f'<a href="{TB}#theorie">Themenseite 5.2b, Häufige Fehler zur Diagonale und zur Trapezhöhe</a>', komp='K2')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · Sek I · GF 5.2a</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Rechteck, Flächeneinheiten, Satz des Pythagoras, Dreiecksfläche und Winkel. Wenn das wackelt: <a href="dreiecke.html">Leitprogramm Dreiecke</a> und <a href="''' + TA + '''#theorie">Themenseite 5.2a</a>.</p>
      ''' + clipkarte('g5-2a-pythagoras', 'Der Satz des Pythagoras') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Ein Rechteck ist \(7\,\text{cm}\) lang und \(3\,\text{cm}\) breit. Berechne Fläche und Umfang.',
     r'<p>\(A = 21\,\text{cm}^2\); \(U = 2(7 + 3) = 20\,\text{cm}\).</p>', ''),
    ('0b', 2, r'Wie viele \(\text{cm}^2\) sind \(1\,\text{m}^2\)? Schreib \(3500\,\text{cm}^2\) in \(\text{m}^2\).',
     r'<p>\(1\,\text{m}^2 = 100\,\text{cm} \cdot 100\,\text{cm} = 10\,000\,\text{cm}^2\); \(3500\,\text{cm}^2 = 0.35\,\text{m}^2\).</p><p class="komm">Zwischen benachbarten Flächeneinheiten liegt der Faktor \(100\), nicht \(10\).</p>', ''),
    ('0c', 2, r'Rechtwinkliges Dreieck: (a) Katheten \(8\,\text{cm}\) und \(15\,\text{cm}\) — Hypotenuse? (b) Hypotenuse \(10\,\text{cm}\), eine Kathete \(6\,\text{cm}\) — andere Kathete?',
     r'<p>(a) \(\sqrt{64 + 225} = \sqrt{289} = 17\,\text{cm}\). (b) \(\sqrt{100 - 36} = 8\,\text{cm}\).</p><p class="komm">Kapitel 4 braucht beides. Falsch? Der Clip oben erklärt den Satz.</p>', ''),
    ('0d', 2, r'Ein Dreieck hat die Grundseite \(10\,\text{cm}\) und die zugehörige Höhe \(4\,\text{cm}\). Wie gross ist seine Fläche?',
     r'<p>\(A = \tfrac{1}{2} \cdot 10 \cdot 4 = 20\,\text{cm}^2\).</p>', ''),
    ('0e', 2, r'(a) Wie gross ist der Nebenwinkel von \(65°\)? (b) Wie gross ist die Winkelsumme in einem Dreieck?',
     r'<p>(a) \(180° - 65° = 115°\). (b) \(180°\).</p><p class="komm">Beides braucht Kapitel 1.</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/vierecke/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.2 · Kapitel 1–4</span><span class="zeit">≈ 30 min · 24 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Skizze und Rechenweg; Taschenrechner erlaubt.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>21 – 24 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>16 – 20 P</td><td>Das schwächste Kapitel nochmals: Tüfteln und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 15 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 2 und 4; G3 → 4 und 2; G4 → 3 und 4; G5 → 3; G6 → 4 und 2</p>
        </div>
      </div>
    </section>

    <section class="kap" id="weiter">
      <h2 id="weiter-titel">Weiter</h2>
      <p>Als Nächstes: <a href="kreis-kreisteile.html">Leitprogramm Kreis und Kreisteile</a> (5.2c) — Sehne, Tangente, Bogen, Sektor und Segment.</p>
      <p>Nicht in diesem Leitprogramm, sondern auf der <a href="{TB}">Themenseite 5.2b</a>: der <a href="{TB}#drachen-widget">Drachen</a> (für ihn gilt ebenfalls \\(A = \\tfrac{{1}}{{2}}\\, e \\cdot f\\)), die <a href="{TB}#darstellungen">Winkelsumme im \\(n\\)-Eck</a>, <a href="{TB}#sehnen-tangenten">Sehnen- und Tangentenvierecke</a> und <a href="{TB}#regelmaessige-vielecke">regelmässige Vielecke</a> — sie stehen nicht in den Kompetenzen des Rahmenlehrplans.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Vierecke, Version 1.0 (08.10.2026). Gebaut aus scripts/lp/vierecke/seite.py — Änderungen dort,
     nicht in dieser Datei. Grundlage: HOWTO-leitprogramme.md; Gerüst und Arbeitsbereich vom Leitprogramm Planimetrie
     (Kapitel 3 dort war der Ausgangspunkt), Auftrag in scripts/lp/vierecke/AUFTRAG.md.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie (gedruckte Seite 44), wörtlich wie auf der Themenseite:
       K1  geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke,
           Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
       K2  deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante,
           Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen
       K3  die Ähnlichkeit für Berechnungen in der Ebene nutzen
     Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Dieses Leitprogramm nimmt die Teile zu den Vierecken:
       K1 (Vierecke)  Quadrat, Rechteck, Parallelogramm, Rhombus, Trapez beschreiben (Bedingungen, Familie, Seiten,
                      Winkel, Diagonalen, Symmetrie)
       K2 (Vierecke)  Höhen, Mittellinie im Trapez, Winkel und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen,
                      dazu Diagonalen und Seiten mit Pythagoras
     Nicht hier: Dreiecke und ihre Linien (→ Leitprogramm Dreiecke, 5.2a), Kreis und Kreisteile (→ 5.2c), K3 Ähnlichkeit
     (→ 5.2d).

     a) Kompetenzmatrix (Teilkompetenz | ohne HM? | Kapitel | Übungen / Kapitelaufgaben | Gesamttest):
       K1 Familie, Eigenschaften  | nein | 1    | Ü familie (Bedingungen, Eigenschaften,  | G1 (a)
          auch Umkehrung: Viereck |      |      | Umkehrung); sim1 A2–A7; 1a, 1c, 1e, 1f   |
          an den Diagonalen       |      |      |                                          |
       K2 Winkel                  | nein | 1    | Ü viereck-winkel (auch «um d° grösser»); | G1 (b)
                                  |      |      | sim1 A8–A9; 1b, 1d, 1e                   |
       K2 Fläche, Umfang (Re, Pa, | nein | 2    | Ü pa-flaeche, raute-ef; sim2; 2a–2c, 2e  | G2 (a), G3 (b), G6 (b)
          Rh)                     |      |      |                                          |
       K2 Abstand (h_b, Höhe Rh)  | nein | 2    | Ü abstand; sim2 A6–A7; 2d, 2e            | G2 (b), G3 (c)
       K2 Mittellinie, Trapez,    | nein | 3    | Ü trapez, trapez-rueck; sim3; 3a–3e      | G4 (a), G5
          auch rückwärts          |      |      |                                          |
       K2 fehlende Längen         | nein | 4    | Ü diagonale, raute-seite, trapez-hoehe   | G2 (a), G3 (a), G4 (b), G6
                                  |      |      | (auch Parallelogramm); sim4, sim5; 4a–4e |
     Kein Kapitelziel ohne Kompetenz; Pythagoras (Vorwissen aus 5.2a/Sek I) dient K2 «Zusammenhänge berechnen».
     Gesamttest (Fassung nach der Prüfung, 08.10.2026): Jede Aufgabe kombiniert Geübtes neu, keine wiederholt eine
     Kapitelaufgabe, Übung oder einen Clip — G1 (a) Diagonalen → Rhombus mit Längen (Übung prüft nur wahr/falsch),
     G1 (b) «um 40° grösser» im Trapez (geübt im Parallelogramm), G2 Höhe aus dem Teildreieck, dann A und h_b,
     G3 Rhombus aus Seite und Diagonale, dann A und Höhe, G4 Trapez rückwärts c, dann Schenkel, G5 die Mittellinie
     teilt das Trapez, G6 fremde Lösung (plus statt minus) und Quadrat aus der Diagonale. Nicht im Gesamttest:
     «begründen» der Flächenformeln (Kapitelaufgaben 2a, 2b, 3d, Kontrollclips).

     b) Planungstabelle (Kapitel | Lernziel | Clips | Erkundung | Beispiel (Quelle) | Häufiger Fehler | min):
       0 Vorwissen   | Rechteck, cm²/m², Pythagoras, Dreiecksfläche, Nebenwinkel | g5-2a-pythagoras | — | — | — | 10
       1 Familie     | Bedingungen, Hierarchie, Diagonalen, Symmetrie, Winkel | g5-2b-lp-familie, -kontrolle-familie |
         sim1 (Trapez a = 5: c, v, h; Start wie im Clip) | Parallelogramm α = 70° (Themenseite, Mini-Check) | Quadrat kein Rechteck,
         Rhombus-Diagonalen gleich, Trapezwinkel wie Parallelogramm | 40
       2 Fläche      | A = a·h, Rhombus ½ef, Umfang, h_b als Abstand | g5-2b-lp-flaeche, -kontrolle-flaeche |
         sim2 (Parallelogramm a, h, v) | Rechteck 5 × 3 (Themenseite, Anim 2), Parallelogramm a 8, b 5, h 3 |
         a·b, ½ beim Parallelogramm, 2A/b | 40
       3 Trapez      | Mittellinie, A = m·h, Scherung, rückwärts | g5-2b-lp-trapez, -kontrolle-trapez |
         sim3 (Trapez a = 6: c, h, v) | a 6, c 4, h 3 → A 15 (Themenseite, Mini-Check) | Schenkel als Höhe,
         ½ vergessen, c = 2A/h | 35
       4 Längen      | Rechteck-/Quadratdiagonale, Rhombusseite, Trapezhöhe | g5-2b-lp-laengen, -kontrolle-laengen |
         sim4 (gleichschenkliges Trapez a, c, h), sim5 (Rhombus e, f) | Rechteck 12 × 5, Rhombus e 8, f 6
         (Kapitel 2), Trapez a 12, c 4, s 5 | d = a√2 im Rechteck, ganzer Überstand, ganze Diagonalen | 45
       Gesamttest 30 (24 P). Summe 200 min ≈ 4.4 Lektionen (vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest).

     c) Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.2b): Drachen (steht nicht in K1), Winkelsumme im n-Eck,
        Sehnen- und Tangentenvierecke, regelmässige Vielecke; Konstruktionen.

     d) Konventionen wie auf der Themenseite: A, B, C, D gegen den Uhrzeigersinn; a = AB, b = BC, c = CD, d = DA;
        α … δ; e = AC, f = BD; Trapez mit Parallelseiten a, c, Höhe h, Mittellinie m = ½(a + c); Parallelogramm
        A = a · h (Tabelle; Merksatz und Anim 3 schreiben g · h — einmal genannt); Rhombus (Raute) mit A = ½ e f;
        Trapez-Schenkel s im Fehlerkasten der Themenseite, h = √(s² − ((a − c)/2)²). Inklusive Trapezdefinition.
        Abweichungen mit Grund: Versatz der oberen Seite heisst v (die Themenseite nennt ihn d, das ist schon die
        Seite DA); Überstand ü = (a − c)/2 bekommt einen Namen; Höhe zur Seite b heisst h_b.
        Widersprüche der Themenseite (gemeldet, nicht übernommen): Anim 4 «Trapez-Scherung» nennt die Schenkel e und f
        (U = a + c + e + f) — e und f sind laut Definition die Diagonalen, die Umfangtabelle schreibt U = a + b + c + d;
        A7 rechnet die Drachenfläche mit d₁, d₂ statt e, f; Verweise «Animation 4» (Sehnen-/Tangentenviereck, ist Anim 6)
        und «Animation 5» (regelmässige Vielecke, ist Anim 7) zeigen auf falsche Nummern; der Clip g5-2b-anim-umformung
        sagt, zwei Trapeze ergäben «das Rechteck a plus c mal h» — es ist ein Parallelogramm (erst die Umformung danach
        macht ein Rechteck daraus).

     Farben: Figur blau, Element (Höhe, Diagonale, Mittellinie, Symmetrieachse) orange, Teildreieck und Ergebnis grün,
     Fehler rot. Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste → ③ Kontrollclip
     mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur
     als PDF aus LaTeX (downloads/leitprogramme/vierecke/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Vierecke</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.2b</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Vierecks-Familie</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Fläche und Umfang</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Trapez, Mittellinie</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Fehlende Längen</span></a></li>
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
          <li><b>② Tüfteln:</b> Im Arbeitsbereich veränderst du die Figur, tippst Linien an und gibst Ergebnisse ein — er zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze, dann Lösung aufklappen und abhaken.</li>
        </ol>
        <p>Taschenrechner erlaubt. Längen auf zwei Dezimalen runden, Zwischenresultate ungerundet weiterverwenden.</p>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 — hier die Teile zu den Vierecken, Taschenrechner erlaubt:</p>
        <ul>
          <li><b>K1</b> geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke, Parallelogramm, Rhombus, Trapez, Kreis) beschreiben — hier Quadrat, Rechteck, Parallelogramm, Rhombus und Trapez: Kapitel 1 und 3</li>
          <li><b>K2</b> deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen — hier Winkel (Kapitel 1), Höhe als Abstand, Umfang und Fläche (Kapitel 2), Mittellinie im Trapez (Kapitel 3) und fehlende Längen mit Pythagoras (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Nicht hier: Dreiecke und ihre Linien (<a href="dreiecke.html">Leitprogramm Dreiecke</a>), Kreis und Kreisteile (<a href="kreis-kreisteile.html">Leitprogramm Kreis und Kreisteile</a>), K3 «die Ähnlichkeit für Berechnungen in der Ebene nutzen» (<a href="aehnlichkeit.html">Leitprogramm Ähnlichkeit</a>).</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Vierecke · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (08.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 35 · K4 45 · Gesamttest 30 = 200 min ≈ 4.4 Lektionen
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
