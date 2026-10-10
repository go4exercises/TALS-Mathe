"""Baut leitprogramme/dreiecke.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/dreiecke/seite.py

Leitprogramm zur Themenseite GF 5.2a Dreiecke, im Kapitelmuster und mit dem Geometrie-Arbeitsbereich der
Leitprogramme Planimetrie und Trigonometrische Berechnungen. Liest Kopf (inkl. <style>) und Grundskript aus der
bestehenden Seite, ersetzt Inhalt, eigenes CSS (seite.css) und Seitenskript (seite.js) und schreibt die Seite neu.
Beim ersten Lauf kommt das Gerüst aus leitprogramme/trigonometrische-berechnungen.html. Wiederholbar; ein
vorhandener SEO-Block (von build-seo.py, mit JSON-LD) bleibt unangetastet. Siehe README.md.
"""
import html
import json
import math
import os
import re
import sys

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegen seite.js, seite.css, geom.py
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
sys.path.insert(0, SP)
from geom import dritte_ecke, richtung, abst  # noqa: E402

ZIEL = R + 'leitprogramme/dreiecke.html'
NAME = 'Dreiecke'
SCHLUESSEL = 'lp-dreiecke-'
MARKE_CSS = '\n/* ════════ Dreiecke'
MARKE_JS = '<script>\n/* Leitprogramm Dreiecke —'
# Unverlinkt bis zur Freischaltung (HOWTO-leitprogramme §13/§15): build-seo.py schreibt den Block neu, sobald die Seite
# dort eingetragen ist. Nur beim ersten Lauf gesetzt — einen vorhandenen Block (mit JSON-LD) nie überschreiben.
SEO_LEER = ('<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
            '<meta name="robots" content="noindex, nofollow">\n<!-- SEO:ENDE -->')

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/trigonometrische-berechnungen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = alt[:a] + SEO_LEER + alt[b:]
    alt = alt.replace('<title>Leitprogramm Trigonometrische Berechnungen</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-trigonometrische-berechnungen-', SCHLUESSEL)

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Trigonometrische Berechnungen', MARKE_CSS):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
kopf = kopf.rstrip('\n') + '\n\n'
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Trigonometrische Berechnungen —'), alt.find(MARKE_JS)) if k > 0)
basis = alt[i:j]
# Footer erzeugt scripts/build-seo.py (seit 10.10.2026): hier nur leere FUSS-Marken; nach dem Bau
# `python3 scripts/build-seo.py` laufen lassen.
fuss = alt[alt.index('<!-- FUSS:ANFANG'):] if '<!-- FUSS:ANFANG' in alt else alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'<!-- FUSS:ANFANG.*?<!-- FUSS:ENDE -->|<footer class="site-footer">.*?</footer>',
              lambda _: '<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n<!-- FUSS:ENDE -->',
              fuss, count=1, flags=re.S)

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


def uebung(typ, titel, bild=None):
    svg = f'<svg class="geo-mini ue-bild" role="img" aria-label="{bild}"></svg>' if bild else ''
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          {svg}
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


TS = '../grundlagen/g5-2a-dreiecke.html'


def fig(daten, fenster, breite=220, hoehe=150, karo=False):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}"'
            f'{" data-karo=\"ja\"" if karo else ""} data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def ecken(*e):
    return [['p', r3(p)] for p, _, _, _ in e] + [['t', r3(p), nm, 'ecke', dx, dy] for p, nm, dx, dy in e]


# ------------------------------------------------------------------ Kapitel 0 · Vorwissen
# 0b: Parallelen g (y = 0) und h (y = 2.5), Querlinie durch P(2 | 0) unter 65°: Q(2 + 2.5/tan 65°, 2.5) = (3.166 | 2.5).
Q0 = (2 + 2.5 / math.tan(math.radians(65)), 2.5)
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · Sek I · GF 5.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Winkelarten, Neben- und Wechselwinkel, Rechteck, Flächeneinheiten und eine Formel umstellen. Wenn das wackelt: <a href="../grundlagen/g5-1-grundlagen.html#typen">Themenseite 5.1, Winkeltypen und Winkelpaare</a>.</p>
      ''' + clipkarte('g5-1-winkelarten', 'Winkel: die Arten und wie man sie erkennt') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Spitz, recht, stumpf oder gestreckt? \(35°\); \(90°\); \(140°\); \(180°\).',
     r'<p>spitz; recht; stumpf; gestreckt.</p>', ''),
    ('0b', 2, r'Die Geraden \(g\) und \(h\) im Bild sind parallel. Wie gross sind \(\beta\) und \(\gamma\)? Wie heissen die Winkelpaare?',
     r'<p>\(\beta = 180° - 65° = 115°\) (Nebenwinkel). \(\gamma = 65°\) (Wechselwinkel an Parallelen).</p><p class="komm">Wechselwinkel braucht Kapitel 1 für die Winkelsumme.</p>',
     fig([['s', [-0.5, 0], [7, 0], 'figur-linie'], ['s', [-0.5, 2.5], [7, 2.5], 'figur-linie'],
          ['s', r3((2 - 0.8 / math.tan(math.radians(65)), -0.8)), r3((Q0[0] + 0.8 / math.tan(math.radians(65)), 3.3)), 'hilfe2'],
          ['w', [2, 0], [4, 0], r3(Q0), '65°', 18], ['w', [2, 0], r3(Q0), [0, 0], 'β', 14], ['w', r3(Q0), [0, 2.5], [2, 0], 'γ', 18],
          ['t', [6.6, 0], 'g', 'seite', 0, -5], ['t', [6.6, 2.5], 'h', 'seite', 0, -5]], '-1,7.5,-1.2', 240, 135)),
    ('0c', 2, r'Ein Rechteck ist \(7\,\text{cm}\) lang und \(4\,\text{cm}\) breit. Berechne Fläche und Umfang.',
     r'<p>\(A = 7 \cdot 4 = 28\,\text{cm}^2\); \(U = 2 \cdot (7 + 4) = 22\,\text{cm}\).</p>', ''),
    ('0d', 2, r'Wie viele \(\text{cm}^2\) sind \(1\,\text{m}^2\)? Schreib \(450\,\text{cm}^2\) in \(\text{m}^2\).',
     r'<p>\(1\,\text{m}^2 = 100\,\text{cm} \cdot 100\,\text{cm} = 10\,000\,\text{cm}^2\); \(450\,\text{cm}^2 = 0.045\,\text{m}^2\).</p>', ''),
    ('0e', 2, r'(a) Löse \(15 = \tfrac{1}{2} \cdot 6 \cdot h\) nach \(h\) auf. (b) Berechne mit dem Rechner \(\sqrt{30.25}\).',
     r'<p>(a) \(15 = 3h\), also \(h = 5\). (b) \(5.5\).</p><p class="komm">Formeln umstellen braucht Kapitel 3, Wurzeln Kapitel 4.</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst den Clip oben und die verlinkte Stelle der Themenseite 5.1, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1 · Winkel im Dreieck
sim1 = bereich(1, 'Dreieck ABC aus den Winkeln alpha und beta über der Seite AB',
               regler('s1', 'al', 'Winkel α', 10, 150, 5, 50, 'orange', '°') + '\n          '
               + regler('s1', 'be', 'Winkel β', 10, 150, 5, 60, 'gruen', '°'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Winkel im Dreieck</div>
          <p><b>Beschriften:</b> Ecken \(A, B, C\) gegen den Uhrzeigersinn; die Seite \(a\) liegt der Ecke \(A\) gegenüber (ebenso \(b\), \(c\)); der Winkel \(\alpha\) liegt bei \(A\), \(\beta\) bei \(B\), \(\gamma\) bei \(C\).</p>
          <p>\[ \alpha + \beta + \gamma = 180° \]</p>
          <p><b>Warum:</b> Die Parallele zu \(AB\) durch \(C\) bildet mit \(b\) und \(a\) Wechselwinkel, gleich gross wie \(\alpha\) und \(\beta\). Zusammen mit \(\gamma\) liegen sie auf einer Geraden: ein gestreckter Winkel.</p>
          <p><b>Aussenwinkel</b> \(\alpha^{\prime}, \beta^{\prime}, \gamma^{\prime}\): der Nebenwinkel des Innenwinkels, \(\alpha^{\prime} = 180° - \alpha\). <b>Aussenwinkelsatz:</b> Jeder Aussenwinkel ist so gross wie die beiden nicht anliegenden Innenwinkel zusammen, \(\gamma^{\prime} = \alpha + \beta\).</p>
          <p><b>Nach Winkeln:</b> spitzwinklig (alle Winkel unter \(90°\)), rechtwinklig (ein Winkel \(90°\)), stumpfwinklig (ein Winkel über \(90°\)). Höchstens ein Winkel ist recht oder stumpf. Im rechtwinkligen Dreieck ergeben die beiden spitzen Winkel zusammen \(90°\).</p>
          <p><b>Nach Seiten:</b> gleichschenklig — zwei gleich lange Seiten (Schenkel), die Basiswinkel sind gleich gross; gleichseitig — drei gleich lange Seiten, alle Winkel \(60°\); ungleichseitig — alle drei Seiten verschieden lang. Gleiche Seiten und gleiche Winkel treten immer zusammen auf.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Mit \(360°\) statt \(180°\) rechnen — \(360°\) gilt im Viereck.</p>
          <p>Aussen- und Innenwinkel verwechseln: Der Aussenwinkel liegt an der <b>Verlängerung</b> einer Seite.</p>
          <p>Im gleichschenkligen Dreieck vergessen, dass es <b>zwei</b> Basiswinkel gibt.</p>
        </div>
      </div>'''
# 1b: A(0 | 0), B(6 | 0), α = 38°, β = 65° → C; Aussenwinkel bei B 115°.
C1b = dritte_ecke((0, 0), (6, 0), 38, 65)
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 2, r'Die Ecken im Bild sind gegen den Uhrzeigersinn mit \(A\), \(B\), \(C\) beschriftet. Schreib \(a\), \(b\), \(c\) und \(\alpha\), \(\beta\), \(\gamma\) an die richtigen Stellen.',
     r'<p>\(a\) ist die Seite \(BC\) (gegenüber \(A\)), \(b\) die Seite \(CA\), \(c\) die Seite \(AB\). \(\alpha\) liegt bei \(A\), \(\beta\) bei \(B\), \(\gamma\) bei \(C\).</p>',
     fig([['v', [[5.5, 4.5], [0.5, 3], [3.5, 0]]]] + ecken(((5.5, 4.5), 'A', 9, -2), ((0.5, 3), 'B', -9, -2), ((3.5, 0), 'C', 0, 14)), '-0.5,6.5,-1', 200, 175)),
    ('1b', 3, r'Im Bild ist \(\alpha = 38°\), und der Aussenwinkel bei \(B\) misst \(115°\). Berechne \(\beta\), \(\gamma\) und den Aussenwinkel \(\gamma^{\prime}\).',
     r'<p>\(\beta = 180° - 115° = 65°\) (Nebenwinkel); \(\gamma = 180° - 38° - 65° = 77°\); \(\gamma^{\prime} = \alpha + \beta = 103°\) (oder \(180° - 77°\)).</p>',
     fig([['v', [[0, 0], [6, 0], r3(C1b)]], ['s', [6, 0], [8, 0], 'verlaengerung'], ['w', [0, 0], [6, 0], r3(C1b), '38°', 22],
          ['w', [6, 0], [8, 0], r3(C1b), '115°', 18]] + ecken(((0, 0), 'A', -8, 13), ((6, 0), 'B', 2, 14), (C1b, 'C', 0, -7)), '-0.8,8.6,-1.2', 240, 160)),
    ('1c', 3, r'In einem gleichschenkligen Dreieck misst der Aussenwinkel an einer Basisecke \(116°\). Skizziere und berechne alle drei Innenwinkel.',
     r'<p>Basiswinkel \(180° - 116° = 64°\), der andere Basiswinkel ebenso \(64°\); Spitze \(180° - 2 \cdot 64° = 52°\).</p><p class="komm">Wer \(116° : 2 = 58°\) rechnet, verwechselt den Aussenwinkel an der Basis mit dem an der Spitze.</p>', ''),
    ('1d', 2, r'Begründe: Jeder Aussenwinkel ist so gross wie die beiden nicht anliegenden Innenwinkel zusammen.',
     r'<p>Zum Beispiel bei \(C\): \(\gamma^{\prime} = 180° - \gamma\) (Nebenwinkel). Aus der Winkelsumme folgt \(\alpha + \beta = 180° - \gamma\). Beide sind \(180° - \gamma\), also \(\gamma^{\prime} = \alpha + \beta\).</p>', ''),
    ('1e', 2, r'Kann ein rechtwinkliges Dreieck gleichschenklig sein? Kann es gleichseitig sein? Begründe mit den Winkeln.',
     r'<p>Gleichschenklig ja: Die beiden spitzen Winkel sind dann gleich, je \(90° : 2 = 45°\). Gleichseitig nein: Dort sind alle Winkel \(60°\), keiner ist \(90°\).</p>', ''),
])
k1 = kapitel(1, 'winkel', 'Winkel im Dreieck', 40,
             r'Du beschriftest Dreiecke normgerecht, begründest und nutzt die Winkelsumme \(180°\) und den Aussenwinkelsatz und teilst Dreiecke nach Winkeln und nach Seiten ein.',
             ('g5-2a-lp-winkel', 'Winkel im Dreieck'), sim1, ('g5-2a-lp-kontrolle-winkel', 'Kontrollfragen zu Winkeln im Dreieck'),
             fest1, [uebung('winkel', 'Winkel berechnen'), uebung('dreiecksart', 'Was für ein Dreieck?')],
             auf1, f'<a href="{TS}#definition">Themenseite 5.2a, Definition</a>, <a href="{TS}#darstellungen">Beweis der Innenwinkelsumme</a> und <a href="{TS}#spezielle-dreiecke">spezielle Dreiecke</a>', komp='K1; K2 Winkel')

# ------------------------------------------------------------------ Kapitel 2 · Höhen, Halbierende, Mittelsenkrechte
sim2 = bereich(2, 'Dreieck ABC mit verschiebbarer Ecke C, dazu Höhen, Seitenhalbierende, Winkelhalbierende oder Mittelsenkrechte',
               regler('s2', 'cx', 'C: waagrecht', -2, 8, 0.5, 2, einheit=' cm') + '\n          '
               + regler('s2', 'cy', 'C: senkrecht', 1, 5.5, 0.5, 3.5, einheit=' cm'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Höhen, Halbierende, Mittelsenkrechte</div>
          <ul>
            <li><b>Höhe</b> \(h_c\): das Lot von \(C\) auf die <b>Gerade</b> durch \(c\). Die drei Höhen schneiden sich im <b>Höhenschnittpunkt</b> \(H\).</li>
            <li><b>Seitenhalbierende</b> \(s_c\): von \(C\) zur Mitte \(M_c\) von \(c\). Die drei schneiden sich im <b>Schwerpunkt</b> \(S\); er teilt jede Seitenhalbierende im Verhältnis \(2 : 1\), vom Eckpunkt aus: \(\overline{CS} = \tfrac{2}{3}\, s_c\).</li>
            <li><b>Winkelhalbierende</b> \(w_\gamma\): teilt \(\gamma\) in zwei gleiche Teile; jeder ihrer Punkte ist von den beiden Schenkeln gleich weit entfernt. Schnittpunkt: <b>Inkreismittelpunkt</b> \(M_I\), gleich weit von allen drei Seiten.</li>
            <li><b>Mittelsenkrechte</b> von \(c\): steht in der Mitte von \(c\) senkrecht; jeder ihrer Punkte ist von \(A\) und \(B\) gleich weit entfernt. Schnittpunkt: <b>Umkreismittelpunkt</b> \(M_U\), gleich weit von allen drei Ecken.</li>
          </ul>
          <p><b>Abstand</b> eines Punkts von einer Geraden heisst: senkrecht gemessen, also das Lot. Die Höhe \(h_c\) ist der Abstand der Ecke \(C\) von der Geraden \(AB\).</p>
          <p><b>Lage:</b> \(S\) und \(M_I\) liegen immer innen. Im spitzwinkligen Dreieck liegen auch \(H\) und \(M_U\) innen; im rechtwinkligen liegt \(H\) auf der Ecke mit dem rechten Winkel und \(M_U\) in der Mitte der Hypotenuse; im stumpfwinkligen liegen \(H\) und \(M_U\) aussen — die beiden Höhen aus den spitzen Ecken treffen die Verlängerung der Gegenseite.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Höhe und Mittelsenkrechte verwechseln: Beide stehen senkrecht — die Höhe geht durch die Ecke, die Mittelsenkrechte durch die Seitenmitte.</p>
          <p>Inkreis- und Umkreismittelpunkt verwechseln: \(M_I\) ist gleich weit von den <b>Seiten</b>, \(M_U\) gleich weit von den <b>Ecken</b>.</p>
          <p>Die Teilung \(2 : 1\) verkehrt: Der längere Teil liegt bei der Ecke.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Zeichne im Bild (Kästchen \(1\,\text{cm}\)) die drei Seitenhalbierenden ein. Gib den Schwerpunkt \(S\) als Punkt an und prüf an \(s_c\) die Teilung \(2 : 1\).',
     r'<p>Seitenmitten \(M_a(4.5 \mid 3)\), \(M_b(0.5 \mid 3)\), \(M_c(4 \mid 0)\); \(S(3 \mid 2)\). Auf \(s_c\): \(\overline{CS} = \sqrt{2^2 + 4^2} \approx 4.47\,\text{cm}\), \(\overline{SM_c} = \sqrt{1^2 + 2^2} \approx 2.24\,\text{cm}\) — doppelt so lang.</p><p class="komm">Ohne Wurzeln: Von \(C\) nach \(S\) geht es 2 nach rechts und 4 nach unten, von \(S\) nach \(M_c\) 1 nach rechts und 2 nach unten — halb so weit.</p>',
     fig([['v', [[0, 0], [8, 0], [1, 6]]]] + ecken(((0, 0), 'A', -8, 13), ((8, 0), 'B', 8, 13), ((1, 6), 'C', 0, -7)), '-1,9,-1', 230, 192, karo=True)),
    ('2b', 3, r'Im Dreieck ist \(\alpha = 70°\) und \(\beta = 50°\). Die Winkelhalbierende \(w_\gamma\) trifft \(c\) in \(D\). Berechne \(\angle ACD\), \(\angle ADC\) und \(\angle BDC\).',
     r'<p>\(\gamma = 60°\), also \(\angle ACD = 30°\). Im Dreieck \(ADC\): \(\angle ADC = 180° - 70° - 30° = 80°\). \(\angle BDC = 180° - 80° = 100°\) (Nebenwinkel; oder im Dreieck \(DBC\): \(180° - 50° - 30°\)).</p>', ''),
    ('2c', 2, r'Im Bild stehen die Linien 1 und 2 beide senkrecht auf \(c\). Welche ist die Höhe \(h_c\), welche die Mittelsenkrechte von \(c\)? Woran erkennst du es?',
     r'<p>Linie 1 ist \(h_c\): Sie geht durch die Ecke \(C\). Linie 2 ist die Mittelsenkrechte: Sie geht durch die Mitte von \(c\) (\(4\,\text{cm}\) von \(A\) und von \(B\)), aber nicht durch \(C\).</p>',
     fig([['v', [[0, 0], [8, 0], [2.5, 5]]], ['s', [2.5, 5], [2.5, 0], 'kandidat-linie'], ['g', [4, -1], [4, 6], 'kandidat-linie'],
          ['t', [2.5, 2.2], '1', 'nummer', -8, 0, 'end'], ['t', [4, 6.2], '2', 'nummer', 8, 4, 'start']]
         + ecken(((0, 0), 'A', -8, 13), ((8, 0), 'B', 8, 13), ((2.5, 5), 'C', 0, -7)), '-1,9,-1.2', 230, 190)),
    ('2d', 2, r'Warum ist der Umkreismittelpunkt \(M_U\) von allen drei Ecken gleich weit entfernt?',
     r'<p>Jeder Punkt der Mittelsenkrechten von \(c\) ist von \(A\) und \(B\) gleich weit entfernt, jeder Punkt der Mittelsenkrechten von \(a\) von \(B\) und \(C\). \(M_U\) liegt auf beiden: \(\overline{M_UA} = \overline{M_UB} = \overline{M_UC}\). Darum liegt er auch auf der dritten Mittelsenkrechten, und der Kreis um \(M_U\) geht durch alle drei Ecken.</p>', ''),
    ('2e', 2, r'Ein Dreieck hat einen Winkel von \(120°\). Welche der Punkte \(H\), \(S\), \(M_I\), \(M_U\) liegen ausserhalb? Begründe für \(H\).',
     r'<p>\(H\) und \(M_U\) liegen ausserhalb, \(S\) und \(M_I\) innen. Das Dreieck ist stumpfwinklig: Die Höhen aus den beiden spitzen Ecken treffen die Verlängerung der Gegenseite, also verlaufen sie ausserhalb, und ihr Schnittpunkt \(H\) liegt ausserhalb.</p>', ''),
])
k2 = kapitel(2, 'elemente', 'Höhen, Halbierende, Mittelsenkrechte', 45,
             r'Du unterscheidest Höhe, Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte, kennst ihre Schnittpunkte mit Lage und Eigenschaft (gleich weit von den Seiten oder den Ecken, Teilung \(2 : 1\)) und berechnest damit Winkel und Strecken.',
             ('g5-2a-lp-elemente', 'Höhen, Halbierende und Mittelsenkrechte'), sim2, ('g5-2a-lp-kontrolle-elemente', 'Kontrollfragen zu Höhen, Halbierenden und Mittelsenkrechten'),
             fest2, [uebung('element', 'Wie heisst sie, wie heisst er?'), uebung('linie-figur', 'Welche Linie ist es?', 'Dreieck mit markierter Seite und drei nummerierten Linien aus der Ecke'),
                     uebung('elem-rechnen', 'Rechnen mit den Linien')],
             auf2, f'<a href="{TS}#typen">Themenseite 5.2a, Dreieckselemente</a> (mit der Animation, die alle vier Linien-Familien zeigt)', komp='K1; K2 Elemente, Abstand')

# ------------------------------------------------------------------ Kapitel 3 · Fläche und Umfang
sim3 = bereich(3, 'Dreieck ABC mit Grundseite AB von 6 cm und einer Spitze C, die parallel zu AB wandert',
               regler('s3', 't', 'Spitze C: t', -3, 10, 0.5, 2, einheit=' cm'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fläche und Umfang</div>
          <p>Jede Seite kann <b>Grundseite</b> \(g\) sein. Die zugehörige <b>Höhe</b> \(h\) ist der Abstand der gegenüberliegenden Ecke von der <b>Geraden</b> durch \(g\) — senkrecht gemessen, auch ausserhalb des Dreiecks.</p>
          <p>\[ A = \tfrac{1}{2}\, g \cdot h \qquad h = \frac{2A}{g} \qquad U = a + b + c \]</p>
          <p><b>Warum die Hälfte:</b> Zwei gleiche Dreiecke ergeben ein Parallelogramm; ein Stück abschneiden und anfügen gibt ein Rechteck mit \(g\) und \(h\). Das Dreieck ist die Hälfte davon.</p>
          <p>Alle drei Paare gehören zur selben Fläche: \(A = \tfrac{1}{2}\, a \cdot h_a = \tfrac{1}{2}\, b \cdot h_b = \tfrac{1}{2}\, c \cdot h_c\). Zur kürzeren Seite gehört die längere Höhe.</p>
          <p>Wandert die Spitze parallel zur Grundseite, bleiben \(g\) und \(h\) und damit die Fläche gleich. Im rechtwinkligen Dreieck ist die eine Kathete die Höhe zur anderen.</p>
          <p><b>Vorgehen:</b> Grundseite wählen → zugehörige Höhe bestimmen → Einheiten angleichen → einsetzen → prüfen (Skizze, Grössenordnung, Einheit).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Eine schräge Seite als Höhe nehmen. Die Höhe steht senkrecht auf der Grundseite.</p>
          <p>Das \(\tfrac{1}{2}\) vergessen: \(g \cdot h\) ist das Rechteck.</p>
          <p>Einheiten mischen: \(0.45\,\text{m}\) und \(18\,\text{cm}\) zuerst angleichen.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Zeichne im Bild (Kästchen \(1\,\text{cm}\)) die Höhe zur Grundseite \(c = AB\) ein. Wo liegt ihr Fusspunkt? Berechne die Fläche.',
     r'<p>Die Höhe ist das Lot von \(C\) auf die Gerade \(AB\); ihr Fusspunkt liegt bei \((6 \mid 0)\), \(2\,\text{cm}\) rechts von \(B\) auf der Verlängerung. \(c = 4\,\text{cm}\), \(h_c = 3\,\text{cm}\): \(A = \tfrac{1}{2} \cdot 4 \cdot 3 = 6\,\text{cm}^2\).</p>',
     fig([['v', [[0, 0], [4, 0], [6, 3]]]] + ecken(((0, 0), 'A', -8, 13), ((4, 0), 'B', 0, 14), ((6, 3), 'C', 0, -7)), '-1,8,-1', 220, 120, karo=True)),
    ('3b', 3, r'Im Dreieck ist \(a = 9\,\text{cm}\), die Höhe \(h_a = 4\,\text{cm}\) und \(b = 6\,\text{cm}\). Berechne die Fläche. Wie weit ist die Ecke \(B\) von der Geraden \(AC\) entfernt?',
     r'<p>\(A = \tfrac{1}{2} \cdot 9 \cdot 4 = 18\,\text{cm}^2\). Der Abstand von \(B\) zur Geraden \(AC\) ist die Höhe \(h_b\): \(h_b = \tfrac{2A}{b} = \tfrac{36}{6} = 6\,\text{cm}\).</p><p class="komm">Zur kürzeren Seite \(b\) gehört die längere Höhe.</p>', ''),
    ('3c', 2, r'Grundseite \(g = 0.45\,\text{m}\), Höhe \(h = 18\,\text{cm}\). Berechne die Fläche in \(\text{cm}^2\) und in \(\text{m}^2\).',
     r'<p>\(A = \tfrac{1}{2} \cdot 45\,\text{cm} \cdot 18\,\text{cm} = 405\,\text{cm}^2 = 0.0405\,\text{m}^2\).</p><p class="komm">Wer \(0.45 \cdot 18 : 2 = 4.05\) rechnet, mischt m und cm.</p>', ''),
    ('3d', 2, r'Warum ist die Fläche eines Dreiecks \(\tfrac{1}{2}\, g \cdot h\)? Begründe mit einer Skizze.',
     r'<p>Ein zweites, gleiches Dreieck gedreht daneben gibt ein Parallelogramm mit Grundseite \(g\) und Höhe \(h\). Schneidet man auf einer Seite ein Dreieck ab und setzt es auf der anderen an, entsteht ein Rechteck \(g \times h\). Das Dreieck ist die Hälfte davon.</p>', ''),
    ('3e', 2, r'Ein gleichschenkliges Dreieck hat die Basis \(7\,\text{cm}\) und den Umfang \(25\,\text{cm}\). Wie lang ist ein Schenkel?',
     r'<p>Für die beiden Schenkel bleiben \(25 - 7 = 18\,\text{cm}\), einer ist \(9\,\text{cm}\) lang.</p>', ''),
])
k3 = kapitel(3, 'flaeche', 'Fläche und Umfang', 40,
             r'Du findest zu einer Grundseite die richtige Höhe — auch ausserhalb des Dreiecks —, begründest \(A = \tfrac{1}{2}\, g \cdot h\), berechnest Fläche, Umfang und eine Höhe als Abstand einer Ecke von einer Geraden.',
             ('g5-2a-lp-flaeche', 'Fläche und Umfang'), sim3, ('g5-2a-lp-kontrolle-flaeche', 'Kontrollfragen zu Fläche und Umfang'),
             fest3, [uebung('hoehe-figur', 'Welche Linie ist die Höhe?', 'Dreieck mit markierter Grundseite und drei nummerierten Linien'), uebung('flaeche', 'Fläche, Höhe, Umfang')],
             auf3, f'<a href="{TS}#theorie">Themenseite 5.2a, Berechnung — Umfang und Fläche</a>', komp='K2 Umfang, Fläche, Abstand')

# ------------------------------------------------------------------ Kapitel 4 · Pythagoras
sim4 = bereich(4, 'Rechtwinkliges Dreieck mit den Katheten a und b',
               regler('s4', 'a', 'Kathete a', 1, 8, 0.5, 3, einheit=' cm') + '\n          '
               + regler('s4', 'b', 'Kathete b', 1, 8, 0.5, 4, einheit=' cm'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Rechtwinklige Dreiecke</div>
          <p>Die beiden Seiten am rechten Winkel heissen <b>Katheten</b>, die Seite gegenüber dem rechten Winkel <b>Hypotenuse</b> — die längste Seite.</p>
          <p><b>Satz des Pythagoras</b> (rechter Winkel bei \(C\)):</p>
          <p>\[ a^2 + b^2 = c^2 \qquad c = \sqrt{a^2 + b^2} \qquad b = \sqrt{c^2 - a^2} \]</p>
          <p>Als Flächen: Die Quadrate über den Katheten haben zusammen so viel Fläche wie das Quadrat über der Hypotenuse.</p>
          <p><b>Gleichschenklig:</b> Die Höhe auf die Basis halbiert die Basis; sie ist zugleich Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte. Jede Hälfte ist rechtwinklig mit dem Schenkel als Hypotenuse: \(h = \sqrt{s^2 - (\tfrac{g}{2})^2}\).</p>
          <p><b>Gleichseitig</b> mit der Seite \(s\): \(h = \sqrt{s^2 - (\tfrac{s}{2})^2} = \tfrac{s}{2}\sqrt{3}\).</p>
          <p><b>Hilfsdreieck:</b> Die Höhe zerlegt jedes Dreieck in rechtwinklige Teile. Liegt ihr Fusspunkt \(F\) auf der Verlängerung von \(c\) hinter \(B\), sind \(BFC\) und \(AFC\) rechtwinklig bei \(F\): \(a = \sqrt{\overline{BF}^2 + h_c^2}\), \(b = \sqrt{(c + \overline{BF})^2 + h_c^2}\).</p>
          <p><b>Prüfen:</b> Die Hypotenuse ist länger als jede Kathete.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Pythagoras ohne rechten Winkel anwenden — er gilt nur im rechtwinkligen Dreieck, mit \(c\) gegenüber dem rechten Winkel.</p>
          <p>Bei einer gesuchten Kathete addieren statt subtrahieren (dann wird sie länger als die Hypotenuse).</p>
          <p>Die Längen statt der Quadrate addieren, oder die Wurzel vergessen.</p>
        </div>
      </div>'''
# 4a: 7-24-25, massstäblich verkleinert (1 cm ≙ 0.16 Einheiten), rechter Winkel bei Q, PQ unter 20° geneigt.
_t, _s = math.radians(20), 0.16
P4a = [0, 0]
Q4a = r3((7 * _s * math.cos(_t), 7 * _s * math.sin(_t)))
R4a = r3((Q4a[0] - 24 * _s * math.sin(_t), Q4a[1] + 24 * _s * math.cos(_t)))
# 4f: Hilfsdreieck mit dem Fusspunkt ausserhalb — A(0 | 0), B(5 | 0), C(7 | 3.5), F(7 | 0): BF = 2, h_c = 3.5, AF = 7.
A4f, B4f, C4f, F4f = (0, 0), (5, 0), (7, 3.5), (7, 0)
auf4 = test('t4', 'Aufgaben · Kapitel 4', 15, [
    ('4a', 2, r'Im Bild (verkleinert) liegt der rechte Winkel bei \(Q\); \(\overline{PQ} = 7\,\text{cm}\), \(\overline{PR} = 25\,\text{cm}\). Welche Seite ist die Hypotenuse? Berechne \(x = \overline{QR}\).',
     r'<p>Die Hypotenuse ist \(\overline{PR}\) (gegenüber dem rechten Winkel bei \(Q\)). \(x = \sqrt{25^2 - 7^2} = \sqrt{576} = 24\,\text{cm}\).</p>',
     fig([['v', [P4a, Q4a, R4a]], ['r', Q4a, [P4a[0] - Q4a[0], P4a[1] - Q4a[1]], [R4a[0] - Q4a[0], R4a[1] - Q4a[1]]],
          ['t', r3(((P4a[0] + Q4a[0]) / 2, (P4a[1] + Q4a[1]) / 2)), '7 cm', 'mass', 6, 12, 'start'],
          ['t', r3(((P4a[0] + R4a[0]) / 2, (P4a[1] + R4a[1]) / 2)), '25 cm', 'mass', -7, 0, 'end'],
          ['t', r3(((Q4a[0] + R4a[0]) / 2, (Q4a[1] + R4a[1]) / 2)), 'x', 'mass gesucht', 8, 0, 'start']]
         + ecken((P4a, 'P', -8, 10), (Q4a, 'Q', 9, 10), (R4a, 'R', 0, -7)), '-1.6,3.6,-0.7', 170, 175)),
    ('4b', 3, r'Ein gleichseitiges Dreieck hat die Seite \(10\,\text{cm}\). Berechne die Höhe und die Fläche. Welche anderen Linien fallen mit der Höhe zusammen?',
     r'<p>\(h = \sqrt{10^2 - 5^2} = \sqrt{75} \approx 8.66\,\text{cm}\); \(A = \tfrac{1}{2} \cdot 10 \cdot \sqrt{75} \approx 43.30\,\text{cm}^2\). Die Höhe ist zugleich Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte (das Dreieck ist symmetrisch).</p>', ''),
    ('4c', 2, r'Eine \(4.5\,\text{m}\) lange Leiter lehnt an einer senkrechten Wand, ihr Fuss steht \(1.2\,\text{m}\) von der Wand entfernt. Wie hoch reicht sie? Skizziere.',
     r'<p>Die Leiter ist die Hypotenuse: \(h = \sqrt{4.5^2 - 1.2^2} = \sqrt{18.81} \approx 4.34\,\text{m}\).</p>', ''),
    ('4d', 3, r'Ein rechtwinkliges Dreieck hat die Katheten \(9\,\text{cm}\) und \(12\,\text{cm}\). Berechne die Hypotenuse, die Fläche und die Höhe auf die Hypotenuse.',
     r'<p>\(c = \sqrt{81 + 144} = 15\,\text{cm}\). \(A = \tfrac{1}{2} \cdot 9 \cdot 12 = 54\,\text{cm}^2\) (die eine Kathete ist die Höhe zur anderen). Höhe auf \(c\): \(h_c = \tfrac{2A}{c} = \tfrac{108}{15} = 7.2\,\text{cm}\).</p>', ''),
    ('4e', 2, r'Lea rechnet im Dreieck mit \(a = 6\,\text{cm}\), \(b = 4\,\text{cm}\) und \(\gamma = 110°\): «\(c = \sqrt{36 + 16} \approx 7.21\,\text{cm}\).» Was ist falsch?',
     r'<p>Der Satz des Pythagoras gilt nur, wenn zwischen \(a\) und \(b\) ein rechter Winkel liegt. Hier ist \(\gamma = 110°\): \(c^2\) ist nicht \(a^2 + b^2\) — mit \(90°\) wäre \(c \approx 7.21\,\text{cm}\); öffnet sich der Winkel weiter, wird \(c\) länger. (Wie man \(c\) dann berechnet, zeigt Teilgebiet 5.3.)</p>', ''),
    ('4f', 3, r'Im Bild ist \(c = \overline{AB} = 5\,\text{cm}\). Die Höhe \(h_c = 3.5\,\text{cm}\) trifft die Verlängerung von \(c\) im Fusspunkt \(F\), \(2\,\text{cm}\) hinter \(B\). Berechne die Seiten \(a\) und \(b\) und den Umfang.',
     r'<p>Die Höhe bildet zwei rechtwinklige Dreiecke mit dem rechten Winkel bei \(F\). Im Dreieck \(BFC\): \(a = \sqrt{2^2 + 3.5^2} = \sqrt{16.25} \approx 4.03\,\text{cm}\). Im Dreieck \(AFC\) ist \(\overline{AF} = 5 + 2 = 7\,\text{cm}\): \(b = \sqrt{7^2 + 3.5^2} = \sqrt{61.25} \approx 7.83\,\text{cm}\). \(U = 5 + \sqrt{16.25} + \sqrt{61.25} \approx 16.86\,\text{cm}\).</p><p class="komm">Wer \(b = \sqrt{5^2 + 3.5^2}\) rechnet, nimmt \(c\) als Kathete — die Kathete reicht aber von \(A\) bis zum Fusspunkt \(F\).</p>',
     fig([['v', [list(A4f), list(B4f), list(C4f)]], ['s', list(B4f), list(F4f), 'verlaengerung'], ['s', list(C4f), list(F4f), 'hilfe'], ['r', list(F4f), [-1, 0], [0, 1]],
          ['t', [2.5, 0], '5 cm', 'mass', 0, 13], ['t', [6, 0], '2 cm', 'mass', 0, 13], ['t', [7, 1.75], '3.5 cm', 'mass', 5, 4, 'start'],
          ['p', list(F4f)], ['t', list(F4f), 'F', 'ecke', 9, 12]]
         + ecken((A4f, 'A', -8, 13), (B4f, 'B', -2, 13), (C4f, 'C', 0, -7)), '-0.8,9,-1', 230, 125)),
])
k4 = kapitel(4, 'pythagoras', 'Rechtwinklige Dreiecke und Pythagoras', 45,
             r'Du erkennst Katheten und Hypotenuse, berechnest mit dem Satz des Pythagoras fehlende Seiten, die Höhe im gleichschenkligen und gleichseitigen Dreieck, Abstände und Seiten in Hilfsdreiecken — auch wenn der Fusspunkt der Höhe ausserhalb liegt — und erkennst, wann der Satz nicht gilt.',
             ('g5-2a-lp-pythagoras', 'Rechtwinklige Dreiecke und Pythagoras'), sim4, ('g5-2a-lp-kontrolle-pythagoras', 'Kontrollfragen zu Pythagoras'),
             fest4, [uebung('pyth-figur', 'Pythagoras an der Figur', 'Rechtwinkliges Dreieck mit zwei gegebenen Seiten und der gesuchten Seite x'), uebung('pyth-anwendung', 'Höhen und Längen')],
             auf4, f'<a href="{TS}#pythagoras">Themenseite 5.2a, Satzgruppe Pythagoras</a> und <a href="{TS}#halbes-dreieck">halbe Dreiecke</a>', komp='K1; K2 Seiten, Höhe, Abstand')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/dreiecke/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.2 · Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
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
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Das schwächste Kapitel nochmals: Tüfteln und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1; G2, G3 → 2; G4 → 3 (Seite \\(b\\) mit 4); G5, G6 → 4 (Fläche und Umfang mit 3); G7 → 2 und 4</p>
        </div>
      </div>
    </section>

    <section class="kap" id="weiter">
      <h2 id="weiter-titel">Weiter</h2>
      <p>Als Nächstes: <a href="vierecke.html">Leitprogramm Vierecke</a> (Themenseite 5.2b) — Quadrat, Rechteck, Parallelogramm, Rhombus und Trapez mit Mittellinie; viele Flächen führen dort auf Dreiecke zurück.</p>
      <p>Nicht in diesem Leitprogramm, sondern auf der <a href="{TS}">Themenseite 5.2a</a>: die <a href="{TS}#definition">Dreiecksungleichung</a>, die <a href="{TS}#kongruenz">Kongruenzsätze</a> (wann ein Dreieck eindeutig konstruierbar ist), Kathetensatz und Höhensatz (<a href="{TS}#pythagoras">Satzgruppe Pythagoras</a>) und die Seitenverhältnisse der <a href="{TS}#halbes-dreieck">halben Dreiecke</a>. Ähnliche Dreiecke: <a href="aehnlichkeit.html">Leitprogramm Ähnlichkeit</a> (5.2d); Sinus, Cosinus und Tangens: <a href="trigonometrische-berechnungen.html">Leitprogramm Trigonometrische Berechnungen</a> (5.3).</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Dreiecke, Version 1.0 (08.10.2026). Gebaut aus scripts/lp/dreiecke/seite.py — Änderungen dort, nicht in
     dieser Datei. Grundlage: HOWTO-leitprogramme.md; Bauweise wie die Leitprogramme Planimetrie und Trigonometrische
     Berechnungen (Geometrie-Arbeitsbereich). Auftrag: scripts/lp/dreiecke/AUFTRAG.md.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie (gedruckte Seite 44), wörtlich wie in der Box der Themenseite:
       K1  geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke,
           Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
       K2  deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante,
           Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen
       K3  die Ähnlichkeit für Berechnungen in der Ebene nutzen
     Dieses Leitprogramm nimmt die Teile zu den Dreiecken: K1 für allgemeine und spezielle Dreiecke; K2 für Höhen, Seiten-
     und Winkelhalbierende, Mittelsenkrechte, Winkel (Winkelmass: Grad) und Umfang, Flächeninhalt, Abstand. Nicht hier:
     Vierecke, Kreis (→ Leitprogramme Vierecke, Kreis und Kreisteile), K3 Ähnlichkeit (→ Leitprogramm Ähnlichkeit),
     Radiant (5.1/5.4). Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Unterstützend 5.1: Skizzen.

     a) Kompetenzmatrix (Teilkompetenz | ohne HM? | Kapitel | Arbeitsbereich/Übung | Kapitelaufgaben | Gesamttest),
        nachgeführt nach der Prüfung vom 08.10.2026:
       K1 beschriften, Dreiecke nach Winkeln/Seiten einteilen | nein | 1 | sim1 A2–A4, dreiecksart | 1a, 1e | G1(b)
       K1 spezielle Dreiecke (gleichschenklig, gleichseitig, rechtwinklig) | nein | 1, 4 | sim1, sim4 A6–A7, pyth-anwendung | 1c, 1e, 4b | G1(b), G6
       K2 Winkel berechnen (Winkelsumme, Aussenwinkel) | nein | 1 | sim1 A6–A8, winkel | 1b–1d | G1(a)
       K2 Höhe, Winkelhalbierende erkennen und Winkel daran berechnen | nein | 2 | sim2 A1–A2, element, linie-figur,
          elem-rechnen (hw, adc, wh) | 2b, 2c | G3
       K2 Seitenhalbierende, Schwerpunkt, Teilung 2 : 1 | nein | 2 | sim2 A7, elem-rechnen (sp) | 2a | G7 (mit Pythagoras)
       K2 Mittelsenkrechte, Winkelhalbierende: «gleich weit», M_U, M_I und ihre Lage | nein | 2 | sim2 A3–A6, A8, element | 2d, 2e | G2
       K2 Flächeninhalt; Höhe auch ausserhalb; Höhe als Abstand h = 2A/g | nein | 3 | sim3, hoehe-figur, flaeche | 3a–3d | G4(a), G4(c)
       K2 Umfang | nein | 3 | flaeche (umfang) | 3e, 4f | G6(b)
       K2 fehlende Seiten und Höhen (Pythagoras), Hilfsdreieck mit dem Fusspunkt ausserhalb | nein | 4 | sim4, pyth-figur,
          pyth-anwendung (au) | 4a–4d, 4f | G4(b), G5, G6(a), G7
       K2 Pythagoras nur mit rechtem Winkel | nein | 4 | Kontrollclip 4 F5 | 4e | G4(b) (Raster: Pythagoras im Dreieck ABC)
     Kein Kapitelziel ohne Kompetenz, keines ohne Gesamttestaufgabe. Berechnet werden Winkel, Höhen (Lage und Länge), die
     Teilung 2 : 1 des Schwerpunkts, halbe Winkel; Mittelsenkrechte und Winkelhalbierende werden vor allem erkannt und über
     «gleich weit» begründet (Um- und Inkreisradius werden nicht berechnet — die Themenseite tut es auch nicht). Die
     Umkehrung des Satzes von Pythagoras steht weder auf der Themenseite noch im Leitprogramm (Ziel von Kapitel 4 am
     08.10.2026 entsprechend gestrichen).

     b) Planungstabelle (Kapitel | Lernziel | Clips | Erkundung | Beispiel (Quelle) | Häufiger Fehler | min):
       0 Vorwissen    | Winkelarten, Neben-/Wechselwinkel, Rechteck, m²/cm², umstellen | g5-1-winkelarten | — | — | — | 10
       1 Winkel       | beschriften, Winkelsumme, Aussenwinkel, Arten | g5-2a-lp-winkel, -kontrolle-winkel | sim1 (α, β) |
                        α = 50°, β = 60° (Themenseite Mini-Check) | 360° statt 180°, Aussen-/Innenwinkel, ein Basiswinkel | 40
       2 Elemente     | h, s, w, Mittelsenkrechte, H, S, M_I, M_U, Lage, 2 : 1 | g5-2a-lp-elemente, -kontrolle-elemente |
                        sim2 (C) | Dreieck A(1|1), B(9|1), C(3|6.5); s_c = 9 | Höhe ↔ Mittelsenkrechte, M_I ↔ M_U | 45
       3 Fläche       | Grundseite–Höhe auch aussen, ½ g h begründen, h = 2A/g, Umfang | g5-2a-lp-flaeche, -kontrolle-flaeche |
                        sim3 (Spitze t) | g = 6, h = 4 (Themenseite Mini-Check), Umfang 5 + 6 + 7 | schräge Seite, ½ vergessen | 40
       4 Pythagoras   | Katheten/Hypotenuse, a² + b² = c², Höhe gleichschenklig/gleichseitig | g5-2a-lp-pythagoras,
                        -kontrolle-pythagoras | sim4 (a, b) | 3-4-5 (Mini-Check), 13/5/12 (A3), s = 8 (A2) | ohne rechten
                        Winkel, addieren statt subtrahieren; Hilfsdreieck mit Fusspunkt ausserhalb (4f, Übung) | 45
       Gesamttest 30. Summe 210 min ≈ 4.7 Lektionen (vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest).
     Sperrliste der Übungen (seite.js, SPERRE) nach der Prüfung nachgeführt: G1(b) da|42|54|84, G7 ph|6|7 (Hilfsdreieck
     ACM_a), 4f und G4 au|…, die neuen Zahlen der Kontrollfragen (ph|5|6, pk|9|4, gsh|6|8).

     c) Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.2a): Dreiecksungleichung, Kongruenzsätze und Konstruktionen,
        Kathetensatz und Höhensatz, Seitenverhältnisse 1 : √3 : 2 und 1 : 1 : √2 als Merkregel (die Höhe im gleichseitigen
        Dreieck kommt in Kapitel 4 über Pythagoras), Aussenwinkelsumme 360°, Pythagoras im Raum.

     d) Konventionen wie auf der Themenseite: A, B, C gegen den Uhrzeigersinn, a gegenüber A, α bei A, Aussenwinkel α′
        (Nebenwinkel); h_a, w_α, M_a, M_I, M_U, H, S; A = ½ g h; rechter Winkel bei C, a² + b² = c². Die Seitenhalbierende
        heisst s_c (die Themenseite gibt kein Zeichen; wie Leitprogramm Planimetrie). Grad, Dezimalpunkt, zwei Dezimalen.
        Widersprüche und Ungenauigkeiten der Themenseite (gemeldet, nicht übernommen): Tabelle Dreieckselemente und
        Merkkasten Flächenformel «Lot … auf die Gegenseite / auf die Grundseite» statt auf die Gerade durch die Seite
        (im stumpfwinkligen Dreieck liegt der Fusspunkt auf der Verlängerung); A7 «Vergleiche mit 5√5 m» (Einheit);
        «Waagerechte» (A6) statt «Waagrechte»; Kongruenzfälle «SsW/sSW» gegen «SSW» in Teilgebiet 5.3.

     Farben: Figur blau, Element und Hilfslinie orange, Gesuchtes, Ergebnis und Schnittpunkt grün, Fehler rot; in Kapitel 1
     die drei Winkel α orange, β grün, γ Tinte (Farbführung für den Beweis der Winkelsumme).
     Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus
     LaTeX (downloads/leitprogramme/dreiecke/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Dreiecke</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.2a</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Winkel im Dreieck</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Höhen, Halbierende</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Fläche und Umfang</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Pythagoras</span></a></li>
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
        <p>Taschenrechner erlaubt. Winkel in Grad, Längen auf zwei Dezimalen runden, Zwischenresultate ungerundet weiterverwenden.</p>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 — hier für die Dreiecke, Taschenrechner erlaubt:</p>
        <ul>
          <li><b>K1</b> geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke, Parallelogramm, Rhombus, Trapez, Kreis) beschreiben — hier: allgemeine und spezielle Dreiecke, Kapitel 1, 2 und 4</li>
          <li><b>K2</b> deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen — hier: Winkel (Kapitel 1), Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte (Kapitel 2), Umfang, Flächeninhalt und Abstand (Kapitel 3), fehlende Seiten und Höhen mit Pythagoras (Kapitel 4). Winkel in Grad (Bogenmass: Teilgebiet 5.4). Seiten-, Winkelhalbierende und Mittelsenkrechte werden vor allem erkannt und über «gleich weit» begründet; berechnet werden Winkel und die Teilung \\(2 : 1\\).</li>
          <li><b>K3</b> die Ähnlichkeit für Berechnungen in der Ebene nutzen — nicht hier, sondern im <a href="aehnlichkeit.html">Leitprogramm Ähnlichkeit</a> (5.2d)</li>
        </ul>
        <p class="rlp-quelle">Vierecke und Kreis: eigene Leitprogramme (5.2b, 5.2c). Dreiecksungleichung, Kongruenzsätze, Kathetensatz und Höhensatz: <a href="''' + TS + '''">Themenseite 5.2a</a>.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Dreiecke · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (08.10.2026), geschätzt aus den Teilen: Vorwissen 10 · K1 40 · K2 45 · K3 40 · K4 45 (mit 4f) · Gesamttest 30 = 210 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
