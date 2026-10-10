"""Baut leitprogramme/kreis-kreisteile.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/kreis-kreisteile/seite.py

Leitprogramm zur Themenseite GF 5.2c Kreis und Kreisteile, im Kapitelmuster und mit dem Geometrie-Arbeitsbereich der
Leitprogramme Planimetrie und Trigonometrische Berechnungen. Liest Kopf (inkl. <style>) und Grundskript aus der
bestehenden Seite, ersetzt eigenes CSS (seite.css), Inhalt und Seitenskript (seite.js) und schreibt die Seite neu.
Beim ersten Lauf kommt das Gerüst aus leitprogramme/trigonometrische-berechnungen.html; der SEO-Block wird dabei
durch einen leeren mit noindex ersetzt. Danach bleibt der SEO-Block, wie er ist (build-seo.py schreibt ihn).
Wiederholbar. Siehe README.md; alle Zahlen in zahlen.py.
"""
import html
import json
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegen seite.js und seite.css
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/kreis-kreisteile.html'
NAME = 'Kreis und Kreisteile'
SCHLUESSEL = 'lp-kreis-kreisteile-'
MARKE_CSS = '\n/* ════════ Kreis und Kreisteile'
MARKE_JS = '<script>\n/* Leitprogramm Kreis und Kreisteile —'
# Unverlinkt bis zur Freischaltung (HOWTO-leitprogramme §13/§15): build-seo.py schreibt den Block neu,
# sobald die Seite dort eingetragen ist (bis zur Freischaltung mit noindex=True).
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
assert SCHLUESSEL + 'thema' in alt and SCHLUESSEL + 'stand' in alt, 'localStorage-Schlüssel fehlen'

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Planimetrie', '\n/* ════════ Trigonometrische Berechnungen', MARKE_CSS):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
kopf = kopf.rstrip('\n') + '\n\n'                            # sonst kommt bei jedem Lauf eine Leerzeile dazu
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


TS = '../grundlagen/g5-2c-kreis-und-kreisteile.html'
TA = '../grundlagen/g5-2a-dreiecke.html'


def fig(daten, fenster, breite=220, hoehe=150):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}" '
            f'data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


def p3(p):
    return [round(p[0], 3), round(p[1], 3)]


def pol(r, w):
    return p3((r * math.cos(math.radians(w)), r * math.sin(math.radians(w))))


# ------------------------------------------------------------------ Kapitel 1
sim1 = bereich(1, 'Kreis mit Mittelpunkt M und Radius r, eine Gerade im Abstand a von M',
               regler('s1', 'r', 'Radius r', 2, 6, 0.5, 5, einheit=' cm') + '\n          '
               + regler('s1', 'a', 'Abstand a', 0, 7, 0.5, 3, 'orange', ' cm'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Kreis und Linien am Kreis</div>
          <p>Ein <b>Kreis</b> mit Mittelpunkt \(M\) und Radius \(r\) ist die Menge aller Punkte der Ebene, die von \(M\) den Abstand \(r\) haben. Der <b>Durchmesser</b> ist \(d = 2r\).</p>
          <p><b>Strecken</b> (sie enden am Kreis): Radius, Durchmesser, <b>Sehne</b> — sie verbindet zwei Punkte der Kreislinie; die längste Sehne ist der Durchmesser. <b>Geraden</b>: <b>Sekante</b> (zwei Schnittpunkte), <b>Tangente</b> (genau ein Berührpunkt), <b>Passante</b> (kein gemeinsamer Punkt). Die Sehne ist das Stück der Sekante im Kreis.</p>
          <p>Der <b>Abstand</b> \(a\) einer Geraden von \(M\) ist die Länge des Lots von \(M\) auf die Gerade. Er entscheidet: \(a \gt r\) Passante, \(a = r\) Tangente, \(a \lt r\) Sekante.</p>
          <p>Die Tangente steht im Berührpunkt <b>senkrecht auf dem Radius</b>: Der Berührpunkt ist ihr Punkt, der \(M\) am nächsten liegt (alle anderen liegen ausserhalb des Kreises), und der kürzeste Weg von \(M\) zu einer Geraden ist das Lot.</p>
          <p><b>Pythagoras am Kreis.</b> Das Lot von \(M\) halbiert jede Sehne, also \(\left(\tfrac{s}{2}\right)^2 + a^2 = r^2\). Für die Tangente von einem Punkt \(P\) aus mit dem Berührpunkt \(B\): \(\overline{PB}^2 + r^2 = \overline{MP}^2\) — der rechte Winkel liegt bei \(B\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Abstand mit dem Durchmesser vergleichen statt mit dem Radius.</p>
          <p>Die halbe Sehne aus dem Dreieck als ganze Sehne angeben.</p>
          <p>Bei der Tangente \(\overline{MP}\) als Kathete nehmen: \(\overline{MP}\) liegt dem rechten Winkel bei \(B\) gegenüber, ist also die Hypotenuse.</p>
        </div>
      </div>'''
A1 = 6.5
f1b = fig([['k', [0, 0], A1], ['seg', [0, 0], A1, 22.62, 157.38], ['s', [-6, 2.5], [6, 2.5], 'sehne'], ['s', [0, 0], [0, 2.5], 'lot'],
           ['s', [0, 0], [6, 2.5], 'radius'], ['r', [0, 2.5], [1, 0], [0, -1]], ['s', [0, 2.5], [0, 6.5], 'hilfe'], ['p', [0, 0]],
           ['t', [0, 0], 'M', 'ecke', -2, 13, 'end'], ['t', [-3, 2.5], 's = 12 cm', 'mass', 0, 13], ['t', [3, 1.25], 'r = 6.5 cm', 'mass', 6, 12, 'start'],
           ['t', [0, 1.25], 'a = ?', 'mass', -5, 4, 'end'], ['t', [0, 4.5], 'h = ?', 'mass', 5, 4, 'start']], '-7.5,7.5,-7.5', 200, 200)
B1c = pol(6, math.degrees(math.acos(0.6)))                     # (3.6 | 4.8)
f1c = fig([['k', [0, 0], 6], ['g', B1c, [10, 0], 'gerade-linie'], ['s', [0, 0], [10, 0], 'lot'], ['s', [0, 0], B1c, 'radius'], ['s', B1c, [10, 0], 'hilfe'],
           ['r', B1c, [-3.6, -4.8], [6.4, -4.8]], ['p', [0, 0]], ['p', [10, 0]], ['p', B1c], ['t', [0, 0], 'M', 'ecke', -8, 13],
           ['t', [10, 0], 'P', 'ecke', 0, 14], ['t', B1c, 'B', 'ecke', -3, -8], ['t', [5, 0], 'MP = 10 cm', 'mass', 0, 13],
           ['t', [1.8, 2.4], 'r = 6 cm', 'mass', -5, 0, 'end']], '-6.8,11,-6.6', 240, 175)
auf1 = test('t1', 'Aufgaben · Kapitel 1', 16, [
    ('1a', 2, r'Wahr oder falsch? Begründe je in einem Satz. (i) Jede Sehne liegt auf einer Sekante. (ii) Eine Gerade durch \(M\) ist immer eine Sekante. (iii) Zu einer Tangente gibt es genau eine zweite Tangente, die zu ihr parallel ist. (iv) Eine Sehne kann länger sein als der Durchmesser.',
     r'<p>(i) Wahr: Verlängert man eine Sehne, entsteht eine Gerade mit zwei Schnittpunkten. (ii) Wahr: Ihr Abstand ist \(a = 0 \lt r\). (iii) Wahr: die Tangente auf der anderen Seite, am Ende des Durchmessers durch den ersten Berührpunkt — beide stehen senkrecht auf demselben Durchmesser. (iv) Falsch: Der Durchmesser ist die längste Sehne.</p>', ''),
    ('1b', 3, r'Ein Kreis hat den Radius \(r = 6.5\,\text{cm}\), eine Sehne ist \(12\,\text{cm}\) lang (Bild). Wie weit ist die Sehne vom Mittelpunkt entfernt? Wie hoch ist der Bogen über der Sehne (Segmenthöhe \(h = r - a\))?',
     r'<p>Das Lot halbiert die Sehne: \(a = \sqrt{6.5^2 - 6^2} = \sqrt{6.25} = 2.5\,\text{cm}\). Segmenthöhe \(h = 6.5 - 2.5 = 4\,\text{cm}\).</p><p class="komm">Wer \(\sqrt{6.5^2 - 12^2}\) rechnen will, merkt es: Unter der Wurzel steht etwas Negatives — im Dreieck liegt die halbe Sehne.</p>', f1b),
    ('1c', 3, r'Ein Punkt \(P\) ist \(10\,\text{cm}\) vom Mittelpunkt eines Kreises mit \(r = 6\,\text{cm}\) entfernt (Bild). (a) Wie lang ist die Tangentenstrecke \(\overline{PB}\)? (b) Wie weit ist \(P\) von der Kreislinie entfernt?',
     r'<p>(a) Rechter Winkel bei \(B\), \(\overline{MP}\) ist die Hypotenuse: \(\overline{PB} = \sqrt{10^2 - 6^2} = 8\,\text{cm}\). (b) Der kürzeste Weg geht auf der Geraden \(MP\): \(10 - 6 = 4\,\text{cm}\).</p>', f1c),
    ('1d', 2, r'Warum halbiert das Lot von \(M\) auf eine Sehne die Sehne?',
     r'<p>Die Radien zu den beiden Sehnenenden sind gleich lang: Das Dreieck aus \(M\) und den Sehnenenden ist gleichschenklig, und seine Höhe auf die Basis halbiert die Basis (Symmetrieachse). Ebenso mit Pythagoras: Beide Teilstücke sind \(\sqrt{r^2 - a^2}\) lang.</p>', ''),
    ('1e', 2, r'Ein Kreis hat den Durchmesser \(9\,\text{cm}\). Eine Gerade hat vom Mittelpunkt den Abstand \(4.6\,\text{cm}\). Mia sagt: «Das ist eine Sekante, denn \(4.6 \lt 9\).» Stimmt das?',
     r'<p>Nein. Zu vergleichen ist mit dem Radius \(r = 4.5\,\text{cm}\): \(4.6 \gt 4.5\), also eine Passante. Mia hat mit dem Durchmesser verglichen.</p>', ''),
    ('1f', 2, r'Eine Sehne ist \(9\,\text{cm}\) lang und hat vom Mittelpunkt den Abstand \(6\,\text{cm}\). Wie gross ist der Radius des Kreises? Mach eine Skizze mit dem rechtwinkligen Dreieck.',
     r'<p>Das Lot halbiert die Sehne: Katheten \(4.5\,\text{cm}\) (halbe Sehne) und \(6\,\text{cm}\) (Abstand), der Radius zum Sehnenende ist die Hypotenuse. \(r = \sqrt{4.5^2 + 6^2} = \sqrt{56.25} = 7.5\,\text{cm}\).</p><p class="komm">Hier wird addiert: Gesucht ist die Hypotenuse.</p>', ''),
    ('1g', 2, r'Ein Kreis hat den Radius \(1.2\,\text{m}\). Ein Punkt \(P\) liegt \(30\,\text{cm}\) ausserhalb der Kreislinie — so weit ist er von ihr entfernt. Wie lang ist die Tangentenstrecke von \(P\) zum Berührpunkt \(B\)?',
     r'<p>Einheiten angleichen: \(30\,\text{cm} = 0.3\,\text{m}\). Der Abstand zur Kreislinie liegt auf der Geraden \(MP\): \(\overline{MP} = 1.2 + 0.3 = 1.5\,\text{m}\), die Hypotenuse. \(\overline{PB} = \sqrt{1.5^2 - 1.2^2} = \sqrt{0.81} = 0.9\,\text{m}\).</p><p class="komm">\(\overline{MP}\) ist nicht \(30\,\text{cm}\): Das ist nur das Stück ausserhalb des Kreises.</p>', ''),
])
k1 = kapitel(1, 'linien', 'Linien am Kreis', 45,
             r'Du beschreibst den Kreis und unterscheidest Radius, Durchmesser und Sehne von Sekante, Tangente und Passante, entscheidest mit dem Abstand \(a\), wie eine Gerade zum Kreis liegt, und berechnest mit Pythagoras Sehne, Abstand, Radius und Tangentenstrecke — auch von einem Punkt in gegebenem Abstand von der Kreislinie aus.',
             ('g5-2c-lp-linien', 'Linien am Kreis'), sim1, ('g5-2c-lp-kontrolle-linien', 'Kontrollfragen zu den Linien am Kreis'),
             fest1, [uebung('linie', 'Linie benennen', 'Kreis mit einer markierten Linie'), uebung('lage', 'Gerade und Kreis'),
                     uebung('sehne', 'Pythagoras am Kreis', 'Kreis mit Sehne oder Tangente')],
             auf1, f'<a href="{TS}#definition">Themenseite 5.2c, Kreis und seine Linien</a> (mit der <a href="{TS}#anim-geraden-kreis">Animation zu Geraden und Strecken</a>)', komp='K1 · K2')

# ------------------------------------------------------------------ Kapitel 2
sim2 = bereich(2, 'Kreis in n Sektoren, darunter die Sektoren abwechselnd zu einem Streifen gelegt',
               regler('s2', 'r', 'Radius r', 1, 3.5, 0.5, 3, einheit=' cm') + '\n          '
               + regler('s2', 'n', 'Sektoren n', 8, 32, 4, 8, 'orange'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Umfang, Fläche und π</div>
          <p>Bei jedem Kreis ist das Verhältnis von Umfang zu Durchmesser dieselbe Zahl, die <b>Kreiszahl</b> \(\pi = \tfrac{U}{d} \approx 3.14159\) (alle Kreise sind ähnlich). \(\pi\) ist irrational — gerechnet wird mit der \(\pi\)-Taste.</p>
          <p>\[ U = 2\pi r = \pi d \qquad A = \pi r^2 = \frac{\pi d^2}{4} \]</p>
          <p><b>Warum \(\pi r^2\)?</b> Zerschneidet man den Kreis in viele gleiche Sektoren und legt sie abwechselnd nebeneinander, entsteht fast ein Rechteck: so hoch wie der Radius, so breit wie der halbe Umfang \(\pi r\). Die Fläche bleibt beim Umlegen gleich: \(A = \pi r \cdot r = \pi r^2\).</p>
          <p><b>Rückwärts:</b> \(r = \tfrac{U}{2\pi}\) und \(r = \sqrt{\tfrac{A}{\pi}}\). Zum Beispiel \(U = 40\,\text{cm}\): \(r = \tfrac{40}{2\pi} \approx 6.37\,\text{cm}\); \(A = 50\,\text{cm}^2\): \(r = \sqrt{\tfrac{50}{\pi}} \approx 3.99\,\text{cm}\).</p>
          <p>Doppelter Radius: doppelter Umfang, aber <b>vierfache</b> Fläche — der Umfang enthält \(r\) einmal, die Fläche \(r^2\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(2\pi r\) und \(\pi r^2\) verwechseln. Die Einheit hilft: Ein Umfang ist eine Länge (cm), eine Fläche hat cm².</p>
          <p>Den Durchmesser in \(\pi r^2\) einsetzen.</p>
          <p>Beim Rückwärtsrechnen aus der Fläche die Wurzel vergessen.</p>
          <p>Mit \(\pi = 3.14\) rechnen und vier Dezimalen angeben: Die Genauigkeit stimmt dann nicht mehr.</p>
        </div>
      </div>'''


def streifen_fig(r, n):
    """Sektoren eines Kreises mit Radius r, abwechselnd zum Streifen gelegt (wie streifen() in seite.js, YB = 0)."""
    c, h = r * math.sin(math.pi / n), r * math.cos(math.pi / n)
    xs, aus = -(n - 1) * c / 2, []
    for k in range(n):
        jj, oben = k // 2, k % 2 == 1
        sp = (xs + (2 * jj + 1) * c, h) if oben else (xs + 2 * jj * c, 0)
        mw = -90 if oben else 90
        pts = [p3(sp)] + [p3((sp[0] + r * math.cos(math.radians(mw - 180 / n + 360 / n * q / 8)),
                               sp[1] + r * math.sin(math.radians(mw - 180 / n + 360 / n * q / 8)))) for q in range(9)]
        aus.append(['v', pts, 'figur satt' if oben else 'figur'])
    return aus, xs, c


st2, xs2, c2 = streifen_fig(2, 12)
f2e = fig(st2 + [['s', [xs2 - c2 - 0.3, 0], [xs2 - c2 - 0.3, 2], 'hilfe'], ['t', [xs2 - c2 - 0.3, 1], 'r', 'seite', -5, 4, 'end'],
                 ['s', [xs2, -0.45], [xs2 + 12 * c2, -0.45], 'hilfe'], ['t', [0, -0.45], 'Breite = ?', 'mass', 0, 13]],
          '-4.2,4.2,-1.4', 250, 110)
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'Ein Teller hat den Durchmesser \(26\,\text{cm}\). Berechne Umfang und Fläche.',
     r'<p>\(r = 13\,\text{cm}\). \(U = 26\pi \approx 81.68\,\text{cm}\); \(A = \pi \cdot 13^2 = 169\pi \approx 530.93\,\text{cm}^2\).</p>', ''),
    ('2b', 3, r'Mit einem Messband misst du den Umfang eines Baumstamms: \(2\,\text{m}\). Nimm den Stamm als kreisrund an. Wie dick ist er (Durchmesser)? Wie gross ist die Schnittfläche, wenn man ihn fällt?',
     r'<p>\(d = \tfrac{U}{\pi} = \tfrac{200}{\pi} \approx 63.66\,\text{cm}\). \(r = \tfrac{100}{\pi} \approx 31.83\,\text{cm}\), \(A = \pi r^2 = \tfrac{10\,000}{\pi} \approx 3183.10\,\text{cm}^2 \approx 0.32\,\text{m}^2\).</p><p class="komm">Mit dem gerundeten \(r = 31.83\) gibt es \(3182.90\) — darum Zwischenresultate im Rechner lassen.</p>', ''),
    ('2c', 3, r'Ein runder Tisch soll \(1.5\,\text{m}^2\) Fläche haben. Welchen Durchmesser braucht er? Wie viel Platz am Rand hat jede von sechs Personen?',
     r'<p>\(r = \sqrt{\tfrac{1.5}{\pi}} \approx 0.69\,\text{m}\), \(d \approx 1.38\,\text{m}\). Umfang \(U = 2\pi r \approx 4.34\,\text{m}\), je Person \(\tfrac{4.34}{6} \approx 0.72\,\text{m}\).</p>', ''),
    ('2d', 2, r'Verdoppelt man den Radius, verdoppelt sich der Umfang, die Fläche aber vervierfacht sich. Warum?',
     r'<p>\(U = 2\pi \cdot (2r) = 2 \cdot 2\pi r\): \(r\) kommt einmal vor. \(A = \pi (2r)^2 = 4\pi r^2\): \(r\) steht im Quadrat, der Faktor \(2\) also auch.</p>', ''),
    ('2e', 2, r'Der Kreis wurde in zwölf gleiche Sektoren geschnitten und abwechselnd zu diesem Streifen gelegt (Bild). Warum ist er so hoch wie der Radius und fast so breit wie der halbe Umfang? Was folgt daraus für die Kreisfläche?',
     r'<p>Die Kanten der Sektoren sind Radien — darum ist der Streifen \(r\) hoch. Unten liegen die Bögen von sechs der zwölf Sektoren, also die Hälfte des Umfangs: \(\tfrac{1}{2} \cdot 2\pi r = \pi r\). Mit mehr Sektoren wird der Streifen ein Rechteck; beim Umlegen bleibt die Fläche gleich, also \(A = \pi r \cdot r = \pi r^2\).</p>', f2e),
    ('2f', 2, r'Mia misst Durchmesser und Umfang von drei runden Dingen: Dose \(7.3\,\text{cm}\) und \(22.9\,\text{cm}\), Velorad \(66\,\text{cm}\) und \(207.5\,\text{cm}\), Münze \(2.3\,\text{cm}\) und \(7.2\,\text{cm}\). Berechne je \(U : d\) auf zwei Dezimalen. Was fällt auf? Warum kommt nicht genau \(\pi\) heraus?',
     r'<p>\(\tfrac{22.9}{7.3} \approx 3.14\), \(\tfrac{207.5}{66} \approx 3.14\), \(\tfrac{7.2}{2.3} \approx 3.13\). Bei jedem Kreis, ob klein oder gross, ist \(U : d\) ungefähr dieselbe Zahl, \(\pi \approx 3.14\). Die Abweichungen kommen vom Messen: Auf einen Millimeter genau gemessen, ändert sich das Verhältnis bei der kleinen Münze am stärksten.</p>', ''),
])
k2 = kapitel(2, 'umfang-flaeche', 'Umfang, Fläche und π', 45,
             r'Du kennst \(\pi\) als festes Verhältnis von Umfang zu Durchmesser, berechnest Umfang und Fläche aus \(r\) oder \(d\) und rechnest aus Umfang oder Fläche den Radius zurück. Warum \(A = \pi r^2\) gilt, zeigen die umgelegten Sektoren.',
             ('g5-2c-lp-umfang', 'Umfang, Fläche und π'), sim2, ('g5-2c-lp-kontrolle-umfang', 'Kontrollfragen zu Umfang und Fläche'),
             fest2, [uebung('kreis', 'Umfang und Fläche'), uebung('zurueck', 'Radius zurückrechnen'), uebung('rad', 'Rad und Umdrehungen')],
             auf2, f'<a href="{TS}#typen">Themenseite 5.2c, Pi</a> und <a href="{TS}#theorie">Umfang und Fläche</a> (mit den Animationen <a href="{TS}#anim-umfang-abrollen">Abrollen</a> und <a href="{TS}#anim-flaeche-sektoren">Sektoren zum Rechteck</a>)', komp='K1 · K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = bereich(3, 'Kreis mit einem Sektor: Radius r, Zentriwinkel phi, Bogen orange',
               regler('s3', 'r', 'Radius r', 1, 5, 0.5, 4, einheit=' cm') + '\n          '
               + regler('s3', 'phi', 'Winkel φ', 0, 360, 15, 45, 'orange', '°'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Bogen und Sektor</div>
          <p>Zwei Radien schneiden aus dem Kreis einen <b>Sektor</b> (Kreisausschnitt). Der Winkel zwischen ihnen ist der <b>Zentriwinkel</b> \(\varphi\) (Mittelpunktswinkel), das Stück der Kreislinie der <b>Bogen</b> \(b\). Winkel in Grad, der Vollwinkel hat \(360°\).</p>
          <p>Bogen und Sektorfläche sind derselbe <b>Anteil</b> \(\tfrac{\varphi}{360°}\) von Umfang und Kreisfläche:</p>
          <p>\[ b = \frac{\varphi}{360°} \cdot 2\pi r \qquad A_{SK} = \frac{\varphi}{360°} \cdot \pi r^2 = \tfrac{1}{2}\, b \cdot r \]</p>
          <p>\(A_{SK} = \tfrac{1}{2}\, b \cdot r\) gleicht der Dreiecksformel: der Bogen als «Grundseite», der Radius als «Höhe». Der <b>Rand</b> des Sektors ist \(U_S = b + 2r\).</p>
          <p><b>Rückwärts:</b> Anteil \(= \tfrac{b}{2\pi r}\) oder \(\tfrac{A_{SK}}{\pi r^2}\), dann \(\varphi = \text{Anteil} \cdot 360°\). Beispiel \(r = 4\,\text{cm}\), \(b = 6\,\text{cm}\): \(\varphi = \tfrac{6}{8\pi} \cdot 360° \approx 85.94°\).</p>
          <p>Die Themenseite schreibt auch \(b = \tfrac{r \pi \varphi}{180°}\) — dasselbe, gekürzt. Steht \(\varphi\) im Bogenmass (GF 5.1), ist einfach \(b = r \cdot \varphi\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bogen (eine Länge, \(2\pi r\)) und Sektor (eine Fläche, \(\pi r^2\)) verwechseln.</p>
          <p>Den Anteil vergessen und den ganzen Umfang oder die ganze Fläche angeben.</p>
          <p>Beim Rand des Sektors die zwei Radien vergessen.</p>
          <p>Beim Rückwärtsrechnen den Anteil als Winkel stehen lassen: \(0.25\) ist nicht \(\varphi\), sondern \(\tfrac{\varphi}{360°}\).</p>
        </div>
      </div>'''
W3b = 10 / (12 * math.pi) * 360                                 # 95.49°
f3b = fig([['sek', [0, 0], 6, 0, round(W3b, 2), 'sektor'], ['bog', [0, 0], 6, 0, round(W3b, 2)], ['p', [0, 0]], ['t', [0, 0], 'M', 'ecke', -8, 12],
           ['t', [3, 0], 'r = 6 cm', 'mass', 0, 13], ['t', pol(6.4, W3b / 2), 'b = 10 cm', 'mass', 4, 0, 'start'], ['t', pol(1.7, W3b / 2), 'φ', 'winkel', 0, 4],
           ['w', [0, 0], [1, 0], pol(1, W3b), '', 16]], '-2.5,9,-1.4', 200, 160)
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Der Minutenzeiger einer Wanduhr ist \(9\,\text{cm}\) lang. Die Zeit läuft \(20\) Minuten. (a) Um welchen Winkel dreht sich der Zeiger? (b) Welchen Weg legt seine Spitze zurück? (c) Welche Fläche überstreicht er?',
     r'<p>(a) \(20\) von \(60\) Minuten sind ein Drittel: \(\varphi = 120°\). (b) \(b = \tfrac{1}{3} \cdot 2\pi \cdot 9 = 6\pi \approx 18.85\,\text{cm}\). (c) \(A_{SK} = \tfrac{1}{3} \cdot \pi \cdot 9^2 = 27\pi \approx 84.82\,\text{cm}^2\).</p>', ''),
    ('3b', 3, r'Ein Sektor hat den Radius \(6\,\text{cm}\) und den Bogen \(10\,\text{cm}\) (Bild). Wie gross ist sein Zentriwinkel? Wie gross ist seine Fläche — berechne sie ohne den Winkel.',
     r'<p>\(\varphi = \tfrac{10}{2\pi \cdot 6} \cdot 360° \approx 95.49°\). \(A_{SK} = \tfrac{1}{2}\, b \cdot r = \tfrac{1}{2} \cdot 10 \cdot 6 = 30\,\text{cm}^2\) (Probe: \(\tfrac{95.49°}{360°} \cdot 36\pi \approx 30\)).</p>', f3b),
    ('3c', 2, r'Warum gilt derselbe Anteil \(\tfrac{\varphi}{360°}\) für den Bogen und für die Fläche?',
     r'<p>Ein Sektor mit doppeltem Winkel besteht aus zwei gleichen Sektoren, die durch Drehen um \(M\) aufeinanderpassen: doppelter Bogen und doppelte Fläche. Bogen und Fläche wachsen also beide proportional zu \(\varphi\), und bei \(360°\) sind sie der Umfang und die Kreisfläche.</p>', ''),
    ('3d', 2, r'Lena berechnet für \(r = 7\,\text{cm}\) und \(\varphi = 50°\) die Sektorfläche: «\(A_{SK} = \tfrac{50°}{360°} \cdot 2\pi \cdot 7 \approx 6.11\,\text{cm}^2\)». Was ist falsch? Rechne richtig.',
     r'<p>Sie hat den Anteil vom Umfang genommen — das ist die Bogenlänge in cm, keine Fläche. Richtig: \(A_{SK} = \tfrac{50°}{360°} \cdot \pi \cdot 7^2 \approx 21.38\,\text{cm}^2\).</p>', ''),
    ('3e', 2, r'Ein runder Kuchen wird in gleiche Stücke mit dem Zentriwinkel \(40°\) geschnitten. Wie viele Stücke gibt es? Der Bogen eines Stücks ist \(7\,\text{cm}\) lang. Welchen Durchmesser hat der Kuchen?',
     r'<p>\(\tfrac{360°}{40°} = 9\) Stücke. Umfang \(U = 9 \cdot 7 = 63\,\text{cm}\), also \(d = \tfrac{63}{\pi} \approx 20.05\,\text{cm}\).</p>', ''),
])
k3 = kapitel(3, 'bogen-sektor', 'Bogen und Sektor', 40,
             r'Du bestimmst den Anteil \(\tfrac{\varphi}{360°}\) eines Zentriwinkels, berechnest damit Bogenlänge, Sektorfläche (auch als \(\tfrac{1}{2}\, b \cdot r\)) und den Rand eines Sektors und rechnest aus Bogen oder Fläche den Zentriwinkel zurück.',
             ('g5-2c-lp-sektor', 'Bogen und Sektor'), sim3, ('g5-2c-lp-kontrolle-sektor', 'Kontrollfragen zu Bogen und Sektor'),
             fest3, [uebung('sektor', 'Bogen und Sektorfläche'), uebung('winkel-zurueck', 'Zentriwinkel zurückrechnen'), uebung('sektor-rand', 'Rand und Fläche des Sektors')],
             auf3, f'<a href="{TS}#kreissektor-h3">Themenseite 5.2c, Kreisbogen und Kreissektor</a> und die <a href="{TS}#aufgaben">Aufgaben A4 und A7</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 4
sim4 = bereich(4, 'Kreis mit Sektor, Dreieck M P1 P2 und dem Segment zwischen Sehne und Bogen',
               regler('s4', 'r', 'Radius r', 2, 6, 0.5, 5, einheit=' cm') + '\n          '
               + regler('s4', 'phi', 'Winkel φ', 0, 360, 15, 90, 'orange', '°'))
sim5 = bereich(5, 'Kreisring zwischen zwei Kreisen um M mit den Radien R und r, gestrichelt der mittlere Kreis',
               regler('s5', 'R', 'Aussenradius R', 1, 6, 0.5, 6, einheit=' cm') + '\n          '
               + regler('s5', 'r', 'Innenradius r', 0.5, 5.5, 0.5, 4, 'orange', ' cm'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Segment, Kreisring, zusammengesetzte Flächen</div>
          <p>Eine Sehne \(P_1P_2\) schneidet ein <b>Segment</b> (Kreisabschnitt) ab: die Fläche zwischen Sehne und Bogen. Mit dem Dreieck \(MP_1P_2\) aus den beiden Radien und der Sehne:</p>
          <p>\[ \varphi \lt 180°\!: \; A_{SG} = A_{SK} - A_\Delta \qquad \varphi \gt 180°\!: \; A_{SG} = A_{SK} + A_\Delta \]</p>
          <p>Bei \(\varphi = 180°\) hat das Dreieck keine Fläche, das Segment ist der Halbkreis. Über \(180°\) liegt das Dreieck <b>im</b> Segment.</p>
          <p><b>Das Dreieck ohne Trigonometrie:</b> Bei \(90°\) (und \(270°\)) ist es rechtwinklig mit den Katheten \(r\): \(A_\Delta = \tfrac{1}{2}\, r^2\). Bei \(60°\) (und \(300°\)) ist es gleichseitig mit der Seite \(r\): Höhe \(h_\Delta = \sqrt{r^2 - \left(\tfrac{r}{2}\right)^2}\), \(A_\Delta = \tfrac{1}{2}\, r \cdot h_\Delta\). Für andere Winkel braucht es die Trigonometrie (GF 5.3).</p>
          <p><b>Kreisring</b> zwischen zwei Kreisen um \(M\) mit Aussenradius \(R\) und Innenradius \(r\):</p>
          <p>\[ A = \pi R^2 - \pi r^2 = \pi (R^2 - r^2) = 2\pi r_m \cdot b \]</p>
          <p>mit der Ringbreite \(b = R - r\) und dem mittleren Radius \(r_m = \tfrac{R + r}{2}\): mittlerer Umfang mal Breite. (Hier heisst \(b\) die Ringbreite, wie auf der Themenseite — nicht die Bogenlänge aus Kapitel 3.)</p>
          <p><b>Zusammengesetzte Flächen</b> zerlegst du in bekannte Teile (Rechteck, Halbkreis, Sektor, Dreieck) und addierst oder ziehst ab.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Über \(180°\) das Dreieck abziehen statt addieren.</p>
          <p>Bei \(60°\) das Dreieck als rechtwinklig rechnen (\(\tfrac{1}{2}\, r^2\)) — es ist gleichseitig.</p>
          <p>\(\pi (R - r)^2\) statt \(\pi (R^2 - r^2)\): Das ist ein Kreis mit dem Radius \(b\), nicht der Ring.</p>
        </div>
      </div>'''
f4a = fig([['v', [[0, 0], [1.2, 0], [1.2, 1.5], [0, 1.5]], 'figur'], ['sek', [0.6, 1.5], 0.6, 0, 180, 'figur'], ['s', [0, 1.5], [1.2, 1.5], 'lot'],
           ['t', [0.6, 0], '1.2 m', 'mass', 0, 13], ['t', [1.2, 0.75], '1.5 m', 'mass', 5, 4, 'start']], '-0.35,1.75,-0.3', 170, 205)
P4b = pol(0.6, 60)
f4b = fig([['seg', [0, 0], 0.6, 60, 360, 'figur'], ['bog', [0, 0], 0.6, 0, 60, 'lot'], ['s', [0.6, 0], P4b, 'sehne'], ['s', [0, 0], [-0.6, 0], 'radius'],
           ['p', [0, 0]], ['t', [0, 0], 'M', 'ecke', 4, -5, 'start'], ['t', [-0.3, 0], 'r = 60 cm', 'mass', 0, 12],
           ['t', [0.45, 0.26], 's = r', 'mass', 7, 2, 'start']], '-0.75,1.15,-0.72', 190, 150)
auf4 = test('t4', 'Aufgaben · Kapitel 4', 13, [
    ('4a', 3, r'Ein Rundbogenfenster besteht aus einem Rechteck, \(1.2\,\text{m}\) breit und \(1.5\,\text{m}\) hoch, mit einem Halbkreis obendrauf (Bild). Wie gross ist die Glasfläche? Wie lang ist der Rand des Fensters?',
     r'<p>Fläche \(1.2 \cdot 1.5 + \tfrac{1}{2} \cdot \pi \cdot 0.6^2 \approx 1.80 + 0.57 = 2.37\,\text{m}^2\). Rand: unten \(1.2\), zwei Seiten \(2 \cdot 1.5\), oben der halbe Kreisumfang \(\pi \cdot 0.6\): \(4.2 + 0.6\pi \approx 6.08\,\text{m}\).</p><p class="komm">Die obere Rechteckseite gehört nicht zum Rand — dort sitzt der Halbkreis.</p>', f4a),
    ('4b', 3, r'Ein runder Tisch mit dem Radius \(60\,\text{cm}\) wird an einer Seite gerade abgeschnitten; die Schnittkante ist so lang wie der Radius (Bild). Wie gross ist die Tischfläche, die bleibt (in m²)?',
     r'<p>Sehne \(= r\): Das Dreieck aus \(M\) und den Enden der Schnittkante ist gleichseitig, der Zentriwinkel \(60°\). Der Tisch ist das Segment zu \(300°\): Sektor plus Dreieck. Sektor \(\tfrac{300°}{360°} \cdot \pi \cdot 0.6^2 \approx 0.9425\,\text{m}^2\); Dreieck \(h_\Delta = \sqrt{0.6^2 - 0.3^2} \approx 0.520\), \(A_\Delta = \tfrac{1}{2} \cdot 0.6 \cdot 0.520 \approx 0.1559\,\text{m}^2\). Tisch \(\approx 1.10\,\text{m}^2\).</p><p class="komm">Ebenso: ganzer Kreis minus das kleine Segment (\(0.1885 - 0.1559 \approx 0.0326\,\text{m}^2\)).</p>', f4b),
    ('4c', 3, r'Eine CD ist zwischen den Radien \(2.3\,\text{cm}\) und \(5.8\,\text{cm}\) bespielt. Wie gross ist die bespielte Fläche? Rechne auf beide Arten.',
     r'<p>\(\pi (5.8^2 - 2.3^2) = 28.35\pi \approx 89.06\,\text{cm}^2\). Oder \(b = 3.5\,\text{cm}\), \(r_m = 4.05\,\text{cm}\): \(2\pi \cdot 4.05 \cdot 3.5 = 28.35\pi\) — dasselbe.</p>', ''),
    ('4d', 2, r'Warum gilt «Segment = Sektor − Dreieck» nur für \(\varphi \lt 180°\)? Was gilt bei \(180°\) und darüber?',
     r'<p>Unter \(180°\) liegt das Dreieck \(MP_1P_2\) im Sektor, aber ausserhalb des Segments: Man zieht es ab. Bei \(180°\) liegen \(P_1\), \(M\), \(P_2\) auf einer Geraden, das Dreieck hat keine Fläche, das Segment ist der Halbkreis. Darüber liegt das Dreieck im Segment: Sektor plus Dreieck.</p>', ''),
    ('4e', 2, r'Zwei Kreisringe sind beide \(1\,\text{cm}\) breit, der eine liegt weiter aussen. Warum hat er mehr Fläche?',
     r'<p>\(A = 2\pi r_m \cdot b\): Bei gleicher Breite \(b\) wächst die Fläche mit dem mittleren Radius \(r_m\) — der äussere Ring ist länger.</p>', ''),
])
k4 = kapitel(4, 'segment-ring', 'Segment und Kreisring', 45,
             r'Du berechnest die Fläche eines Segments als Sektor minus Dreieck (über \(180°\) plus Dreieck) bei \(60°\), \(90°\) und ihren Ergänzungen, die Fläche eines Kreisrings auf zwei Arten und zusammengesetzte Flächen in Sachaufgaben.',
             ('g5-2c-lp-segment', 'Segment und Kreisring'), sim4 + '\n' + sim5, ('g5-2c-lp-kontrolle-segment', 'Kontrollfragen zu Segment und Kreisring'),
             fest4, [uebung('segment', 'Segmentfläche', 'Kreis mit grünem Segment'), uebung('ring', 'Kreisring')],
             auf4, f'<a href="{TS}#kreissegment-h3">Themenseite 5.2c, Kreissegment</a> und <a href="{TS}#kreisring-h3">Kreisring</a> (mit der Animation zum <a href="{TS}#anim-ring-aufrollen">Aufrollen des Rings</a>)', komp='K2')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 5.1, 5.2a</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Satz des Pythagoras, das gleichseitige Dreieck, Bruchteile des Vollwinkels, Gleichungen mit \\(x^2\\) und Flächeneinheiten. Wenn das wackelt: <a href="''' + TA + '''#pythagoras">Themenseite 5.2a, Pythagoras</a> und das <a href="dreiecke.html">Leitprogramm Dreiecke</a> (Kapitel 3–4).</p>
      ''' + clipkarte('g5-2a-pythagoras', 'Der Satz des Pythagoras') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Rechtwinkliges Dreieck: (a) Katheten \(5\,\text{cm}\) und \(12\,\text{cm}\) — Hypotenuse? (b) Hypotenuse \(10\,\text{cm}\), eine Kathete \(6\,\text{cm}\) — andere Kathete?',
     r'<p>(a) \(\sqrt{25 + 144} = 13\,\text{cm}\). (b) \(\sqrt{100 - 36} = 8\,\text{cm}\).</p><p class="komm">Kapitel 1 rechnet so Sehnen und Tangenten aus.</p>', ''),
    ('0b', 2, r'Ein gleichseitiges Dreieck hat die Seite \(8\,\text{cm}\). Wie hoch ist es, und wie gross ist seine Fläche?',
     r'<p>Die Höhe halbiert die Grundseite: \(h = \sqrt{8^2 - 4^2} = \sqrt{48} \approx 6.93\,\text{cm}\). \(A = \tfrac{1}{2} \cdot 8 \cdot \sqrt{48} \approx 27.71\,\text{cm}^2\).</p><p class="komm">Genau dieses Dreieck steckt in Kapitel 4 im Segment zu \(60°\).</p>', ''),
    ('0c', 2, r'Welcher Bruchteil des Vollwinkels sind \(90°\), \(45°\) und \(240°\)? Wie viele Grad ist ein Sechstel des Vollwinkels?',
     r'<p>\(\tfrac{90}{360} = \tfrac{1}{4}\), \(\tfrac{45}{360} = \tfrac{1}{8}\), \(\tfrac{240}{360} = \tfrac{2}{3}\). Ein Sechstel: \(60°\).</p>', ''),
    ('0d', 2, r'Löse: (a) \(3x = 24\) (b) \(5x^2 = 100\) mit \(x \gt 0\) (auf zwei Dezimalen)',
     r'<p>(a) \(x = 8\). (b) \(x^2 = 20\), \(x = \sqrt{20} \approx 4.47\).</p><p class="komm">So rechnest du in Kapitel 2 aus der Fläche den Radius zurück.</p>', ''),
    ('0e', 2, r'Wie viele \(\text{cm}^2\) sind \(1\,\text{m}^2\)? Wie viele \(\text{cm}^2\) sind \(0.35\,\text{m}^2\)?',
     r'<p>\(1\,\text{m}^2 = 100\,\text{cm} \cdot 100\,\text{cm} = 10\,000\,\text{cm}^2\); \(0.35\,\text{m}^2 = 3500\,\text{cm}^2\).</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/kreis-kreisteile/'
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
          <p>Aufgabe → Kapitel: G1, G2 → 1; G3 (a) → 2, G3 (b) → 4; G4 → 3; G5 (a) → 1, G5 (b)–(d) → 4; G6 → 3; G7 → 2 und 4</p>
        </div>
      </div>
    </section>

    <section class="kap" id="weiter">
      <h2 id="weiter-titel">Weiter</h2>
      <p>Als Nächstes in der Planimetrie: <a href="../grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html">Themenseite 5.2d, Zentrische Streckung und Ähnlichkeit</a> — dort steckt auch, warum \\(\\pi\\) für alle Kreise gleich ist. Danach die <a href="trigonometrische-berechnungen.html">Trigonometrischen Berechnungen</a> (5.3): Mit ihnen geht das Dreieck im Segment bei jedem Winkel.</p>
      <p>Nicht in diesem Leitprogramm, sondern auf der <a href="{TS}">Themenseite 5.2c</a>: die Annäherung von \\(\\pi\\) mit Vielecken nach Archimedes (<a href="{TS}#typen">Pi — die Kreiszahl</a>, Aufgabe A3), die Segmentformel mit Sehne und Segmenthöhe \\(A_{{SG}} = \\tfrac{{r^2 \\pi \\varphi}}{{360°}} - \\tfrac{{s\\,(r - h)}}{{2}}\\) für beliebige Winkel (sie braucht Sinus und Cosinus) und der Ring als aufgerolltes Trapez.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Kreis und Kreisteile, Version 1.0 (08.10.2026). Gebaut aus scripts/lp/kreis-kreisteile/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlage: HOWTO-leitprogramme.md, Auftrag scripts/lp/kreis-kreisteile/AUFTRAG.md,
     Vorbilder Planimetrie (Kapitel 4) und Trigonometrische Berechnungen (Geometrie-Arbeitsbereich). Alle Zahlen: zahlen.py.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie (Math-GL.pdf S. 5, gedruckt 44), wörtlich wie auf der Themenseite:
       K1  geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke,
           Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
       K2  deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante,
           Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen
       K3  die Ähnlichkeit für Berechnungen in der Ebene nutzen
     Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Dieses Leitprogramm nimmt aus K1 und K2 die Teile zum
     Kreis (Kreis beschreiben; Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass; Umfang, Flächeninhalt,
     Abstand). Nicht hier: die übrigen Objekte und Elemente (Leitprogramme zu 5.2a und 5.2b) und K3 (5.2d).

     a) Kompetenzmatrix (Teilkompetenz | ohne HM? | Kapitel | Arbeitsbereich, Übung | Kapitelaufgaben | Gesamttest):
       K1 Kreis beschreiben (Definition, Linien, Lage)       | nein | 1, 2 | AB1 A1–A5; linie, lage | 1a, 1e, 2e      | G1 (a)
       K1 π als Verhältnis U : d (Kapitelziel «kennen»)      | nein | 2    | Kontrolle 2 F1         | 2f (Messung)    | G7 (a) (U = πd)
       Herleitung A = πr² (Streifen, AB2 A1–A3, 2e) ist Einsicht, kein Kapitelziel: nicht im Gesamttest (RLP verlangt sie nicht).
       K2 Sehne, Sekante, Abstand berechnen                 | nein | 1    | AB1 A6–A7; sehne (s, a) | 1b, 1d         | G1 (b)
       K2 Radius aus Sehne und Abstand                       | nein | 1    | sehne (r)             | 1f              | G5 (a)
       K2 Tangente berechnen (auch P in Abstand h, Einheiten)| nein | 1    | AB1 A8; sehne (t, h)  | 1c, 1g          | G2
       K2 Umfang, Flächeninhalt (Kreis), rückwärts          | nein | 2    | AB2; kreis, zurueck, rad | 2a–2d        | G3 (a), G7
       K2 Sektor, Bogen, Winkel und Winkelmass              | nein | 3    | AB3; sektor, winkel-zurueck, sektor-rand | 3a–3e | G4, G6
       K2 Segment unter und über 180°                        | nein | 4    | AB4; segment          | 4b (300°), 4d   | G5 (b)–(d), (d) über 180°
       K2 Flächeninhalt: Kreisring, zusammengesetzt          | nein | 4    | AB5; ring             | 4a, 4c, 4e      | G3 (b), G7
       Gesamttest kombiniert neu (HOWTO §9): G2 Tangente vom Punkt in Höhe h mit m/km (geübt in 1g und sehne h mit mm/cm,
       neu: Erdkugel), G5 Radius aus Sehne und Abstand → Zentriwinkel begründen → beide Segmente (geübt: 1f, 4b), G6 Radius
       und Winkel zugleich verdoppelt (geübt je einzeln: 2d, 3c, Kontrolle 2 F4).
       Winkelmass: Grad (Vollwinkel 360°, Anteil φ/360°). Bogenmass nur als Satz im Festhalten 3 (GF 5.1; die Themenseite
       verschiebt es auf 5.4), nicht geübt. Abstand: Abstand Gerade–Mittelpunkt, Sehne–Mittelpunkt, Punkt–Kreislinie.
       Tangentenstrecke von einem äusseren Punkt: steht nicht als Aufgabe auf der Themenseite, folgt aber aus «Tangente ⟂
       Radius» (Themenseite) und Pythagoras (5.2a) und ist das, was «Tangente berechnen» im RLP verlangen kann.

     b) Planungstabelle (Kapitel | Lernziel | Clips | Erkundung | Beispiel (Quelle) | Häufiger Fehler | min):
       0 Vorwissen | Pythagoras, gleichseitiges Dreieck, Anteile von 360°, x² = c, m²/cm² | g5-2a-pythagoras | — | — | — | 10
       1 Linien    | Begriffe, Abstand a, Tangente ⟂ Radius, Sehne/Abstand/Radius/Tangente mit Pythagoras | g5-2c-lp-linien,
                     -kontrolle-linien | AB1 (r, a; antippen; drei Grössen) | r = 5, a = 3 → s = 8 (eigen; Themenseite Anim 1:
                     r = 3, a = 3.6/3/1.8) | a mit d vergleichen, halbe Sehne, MP als Kathete | 45
       2 Umfang    | π = U/d, U, A, rückwärts, Sektoren zum Rechteck | g5-2c-lp-umfang, -kontrolle-umfang | AB2 (r, n; Breite
                     antippen) | r = 3 (eigen; Themenseite r = 5, r = 6) | 2πr/πr², d in πr², Wurzel vergessen | 45
       3 Sektor    | Anteil φ/360°, b, A_SK = ½ b r, Rand, rückwärts | g5-2c-lp-sektor, -kontrolle-sektor | AB3 (r, φ; Bogen
                     antippen) | r = 4, φ = 45° (eigen; Themenseite r = 12, φ = 135°) | b/A verwechselt, Anteil vergessen | 40
       4 Segment, Ring | Sektor − Dreieck, über 180° + Dreieck (60°, 90°, 270°, 300°), Ring auf zwei Arten, zusammengesetzt | g5-2c-lp-segment,
                     -kontrolle-segment | AB4 (r, φ; Höhe antippen), AB5 (R, r; Breite antippen) | r = 5 bei 90° und 60°;
                     R = 6, r = 4 (eigen) | über 180° abziehen, 60° rechtwinklig, π(R − r)² | 45
       Gesamttest 30. Summe 215 min ≈ 4.8 Lektionen (vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest).

     c) Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.2c): π-Schranken nach Archimedes (A3), Segmentformel
        A_SG = r²πφ/360° − s(r − h)/2 mit s = 2r sin(φ/2) für beliebige Winkel (braucht 5.3), Ring als aufgerolltes Trapez,
        «π ist transzendent». Vertiefung im Festhalten: b = rπφ/180° und b = r·φ im Bogenmass (nicht geübt).

     d) Konventionen wie auf der Themenseite: M, r, d, s, a (Abstand), φ Zentriwinkel (auch «Mittelpunktswinkel»), b Bogen,
        A_SK Sektor, A_SG Segment, h Segmenthöhe; Kreisring R, r, b = R − r, r_m. Eigen: h_Δ für die Höhe des Dreiecks
        M P1 P2 (die Themenseite braucht h für die Segmenthöhe), P1, P2 für die Sehnenenden, B für den Berührpunkt.
        Widersprüche der Themenseite (gemeldet, nicht übernommen): b zugleich Bogenlänge und Ringbreite (hier übernommen und
        im Festhalten 4 benannt); Umfang einmal klein u (Abschnitt Pi: «u = π·d», neben u_n für das einbeschriebene Vieleck),
        sonst U; «Mittelpunktswinkel» (Strategie) neben «Zentriwinkel» (Animationen, Tabellen); Merksatz Zusammenfassung:
        Bogenmass «lernst du in 5.4 kennen», GF 5.1 führt Radiant schon ein; Aufgabe A3: «Einheitskreis (d = 1, also r = 1/2)» —
        der Einheitskreis hat r = 1; Merkkasten Umfang und Fläche: «der Einheitskreis nimmt das π-fache davon ein» (gemeint
        ist der Kreis mit Radius r); Aufgabe A1.4 «Diese Eigenschaft definiert die Tangente sogar» (definiert ist sie über den
        einen gemeinsamen Punkt); Tabelle φ ∈ [0°; 360°[ gegen Regler bis 360°.

     Farben: Figur blau, Element/Hilfslinie/Kandidat orange (Bogen, Sehne, Dreieck M P1 P2, Lot), Fläche und Ergebnis grün, Fehler
     rot. Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/kreis-kreisteile/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Kreis und Kreisteile</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.2c</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Linien am Kreis</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Umfang, Fläche, π</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Bogen und Sektor</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Segment und Kreisring</span></a></li>
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
        <p>Taschenrechner erlaubt; rechne mit der \\(\\pi\\)-Taste. Längen, Flächen und Winkel auf zwei Dezimalen runden, Zwischenresultate ungerundet weiterverwenden.</p>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie — Taschenrechner erlaubt. Hier die Teile zum Kreis:</p>
        <ul>
          <li><b>K1</b> geometrische Sachverhalte von elementaren Objekten (… Kreis) beschreiben — Kapitel 1 und 2.</li>
          <li><b>K2</b> deren Elemente (… Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen — Sehne, Abstand und Tangente in Kapitel 1, Umfang und Fläche in Kapitel 2, Bogen, Sektor und Winkel in Kapitel 3, Segment, Kreisring und zusammengesetzte Flächen in Kapitel 4. Winkel in Grad.</li>
        </ul>
        <p class="rlp-quelle">Nicht hier: Dreiecke und Vierecke mit ihren Elementen (Themenseiten <a href="''' + TA + '''">5.2a</a> und <a href="../grundlagen/g5-2b-vierecke.html">5.2b</a>), «die Ähnlichkeit für Berechnungen in der Ebene nutzen» (<a href="../grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html">5.2d</a>), das Bogenmass (GF 5.1; hier nur im Festhalten 3 erwähnt) und Segmente bei beliebigen Winkeln (braucht die <a href="trigonometrische-berechnungen.html">Trigonometrie, 5.3</a>).</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Kreis und Kreisteile · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (08.10.2026, nach der Prüfung): Vorwissen 10 (vorab) · K1 45 · K2 45 · K3 40 · K4 45 · Gesamttest 30 = 215 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
