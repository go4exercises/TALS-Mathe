"""Baut leitprogramme/aehnlichkeit.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/aehnlichkeit/seite.py

Leitprogramm zur Themenseite GF 5.2d Zentrische Streckung und Ähnlichkeit, im Kapitelmuster und mit dem
Geometrie-Arbeitsbereich der Leitprogramme Planimetrie und Trigonometrische Berechnungen. Liest Kopf (inkl.
<style>) und Grundskript aus der bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die
Seite neu. Beim ersten Lauf kommt das Gerüst aus leitprogramme/planimetrie.html (mit leerem SEO-Block, noindex);
danach bleibt der SEO-Block der Seite, wie er ist — build-seo.py schreibt ihn, sobald die Seite eingetragen ist.
Wiederholbar. Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/aehnlichkeit.html'
NAME = 'Zentrische Streckung und Ähnlichkeit'
SCHLUESSEL = 'lp-aehnlichkeit-'
MARKE_CSS = '\n/* ════════ Zentrische Streckung und Ähnlichkeit'
MARKE_JS = '<script>\n/* Leitprogramm Zentrische Streckung und Ähnlichkeit —'
# Unverlinkt bis zur Freischaltung (HOWTO-leitprogramme §13/§15): nur beim ersten Lauf ein leerer Block mit noindex.
# Einen vorhandenen Block (später mit Beschreibung und JSON-LD aus build-seo.py) nie überschreiben.
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
assert SCHLUESSEL + 'thema' in alt and 'lp-planimetrie-' not in alt

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Planimetrie', MARKE_CSS):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
kopf = kopf.rstrip('\n') + '\n\n'                            # sonst kommt bei jedem Lauf eine Leerzeile dazu
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


TS = '../grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html'


def fig(daten, fenster, breite=220, hoehe=150, karo=False, achsen=False):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»). Fenster x0,x1,y0 — gleich geteilt."""
    k = (' data-karo="ja"' if karo else '') + (' data-achsen="ja"' if achsen else '')
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}"{k} '
            f'data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


def ecken(*e, cls='ecke'):
    return [['p', p] for p, _, _, _ in e] + [['t', p, n, cls, dx, dy] for p, n, dx, dy in e]


# ------------------------------------------------------------------ Kapitel 1
sim1 = bereich(1, 'Dreieck ABC und sein Bild bei einer zentrischen Streckung mit Zentrum Z(1 | 1) und Faktor k im Koordinatennetz',
               regler('s1', 'k', 'Streckfaktor k', -1.5, 2, 0.5, 1.5, 'orange'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zentrische Streckung</div>
          <p>Gegeben sind ein <b>Streckungszentrum</b> \(Z\) und ein <b>Streckfaktor</b> \(k \neq 0\). Jeder Punkt \(P\) geht auf einen Bildpunkt \(P'\) auf der Geraden durch \(Z\) und \(P\), und \(\overline{ZP'} = |k| \cdot \overline{ZP}\). Bei \(k \gt 0\) liegt \(P'\) auf derselben Seite von \(Z\) wie \(P\), bei \(k \lt 0\) auf der anderen.</p>
          <p>\(|k| \gt 1\) vergrössert, \(|k| \lt 1\) verkleinert, \(k = 1\) ändert nichts. Bei \(k \lt 0\) ist das Bild zusätzlich um \(Z\) um \(180°\) gedreht; \(k = -1\) ist die Punktspiegelung an \(Z\).</p>
          <p><b>Mit Koordinaten:</b> den Weg von \(Z\) nach \(P\) mit \(k\) multiplizieren und von \(Z\) aus abtragen. \(Z(1 \mid 1)\), \(C(5 \mid 4)\), \(k = 1.5\): Weg \(4\) nach rechts, \(3\) nach oben; mal \(1.5\): \(6\) und \(4.5\); also \(C'(7 \mid 5.5)\).</p>
          <p><b>Eigenschaften:</b> Winkel bleiben gleich (winkeltreu). Jede Bildseite ist parallel zu ihrer Originalseite — darum bleiben auch parallele Geraden parallel (parallelentreu). Jede Länge wird mit \(|k|\) multipliziert, Längenverhältnisse bleiben (verhältnistreu). Darum hat das Bild dieselbe Form wie das Original.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Koordinaten von \(P\) mit \(k\) multiplizieren: Das stimmt nur, wenn \(Z\) im Ursprung liegt. Gestreckt wird vom Zentrum aus.</p>
          <p>Bei negativem \(k\) eine negative Länge angeben: Längen werden mit dem Betrag \(|k|\) multipliziert.</p>
          <p>Den Abstand vom Originalpunkt aus abtragen statt vom Zentrum aus.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Strecke das Dreieck \(PQR\) im Bild vom Zentrum \(Z(4 \mid 2)\) aus mit \(k = -0.5\). Zeichne das Bild ins Karo und gib die Bildpunkte an.',
     r"<p>\(P'(6 \mid 3)\), \(Q'(4 \mid 3)\), \(R'(7 \mid 1)\). Zum Beispiel \(R\): Weg von \(Z\) nach \(R\) ist \(6\) nach links und \(2\) nach oben; mal \(-0.5\): \(3\) nach rechts und \(1\) nach unten. Das Bild liegt auf der anderen Seite von \(Z\), hat halb so lange Seiten und ist um \(180°\) gedreht.</p>",
     fig([['v', [[0, 0], [4, 0], [-2, 4]]], ['p', [4, 2]], ['t', [4, 2], 'Z', 'ecke', 8, -4]] + ecken(([0, 0], 'P', -7, 12), ([4, 0], 'Q', 9, -4), ([-2, 4], 'R', -7, -4)),     # Q über der Achse: unten stünde die Achsenzahl 4
         '-3.5,8.5,-1.5', 240, 140, karo=True, achsen=True)),
    ('1b', 3, r"Das Dreieck \(A(0 \mid 2)\), \(B(3 \mid 0)\), \(C(1 \mid 4)\) wird vom Zentrum \(Z(-2 \mid 1)\) aus mit \(k = 2.5\) gestreckt. Berechne \(A'\), \(B'\) und \(C'\).",
     r"<p>\(A'\): Weg \((2 \mid 1)\), mal \(2.5\): \((5 \mid 2.5)\), also \(A'(3 \mid 3.5)\). \(B'\): Weg \((5 \mid -1)\) → \((12.5 \mid -2.5)\), also \(B'(10.5 \mid -1.5)\). \(C'\): Weg \((3 \mid 3)\) → \((7.5 \mid 7.5)\), also \(C'(5.5 \mid 8.5)\).</p><p class='komm'>Wer \(2.5 \cdot A = (0 \mid 5)\) rechnet, streckt vom Ursprung aus statt von \(Z\).</p>", ''),
    ('1c', 2, r"Warum ist die zentrische Streckung mit \(k = -1\) eine Punktspiegelung an \(Z\)?",
     r"<p>\(P'\) liegt auf der Geraden durch \(Z\) und \(P\), auf der anderen Seite von \(Z\), und \(\overline{ZP'} = 1 \cdot \overline{ZP}\). Also ist \(Z\) die Mitte der Strecke \(PP'\) — genau das macht die Punktspiegelung an \(Z\).</p>", ''),
    ('1d', 2, r"Im Bild ist \(A'B'C'\) das Bild von \(ABC\) bei einer zentrischen Streckung. Finde das Zentrum \(Z\) durch Zeichnen und bestimme \(k\).",
     r"<p>Die Geraden \(AA'\), \(BB'\) und \(CC'\) schneiden sich im Zentrum \(Z(4 \mid 3)\). \(Z\) liegt zwischen Original und Bild, die Bildseiten sind halb so lang: \(k = -0.5\). (Zum Beispiel \(\overline{ZA} = \sqrt{20}\), \(\overline{ZA'} = \sqrt{5}\), Verhältnis \(0.5\).)</p>",
     fig([['v', [[0, 1], [2, 0], [1, 4]]], ['v', [[6, 4], [5, 4.5], [5.5, 2.5]], 'bild']]
         + ecken(([0, 1], 'A', -8, 4), ([2, 0], 'B', 10, -4), ([1, 4], 'C', -6, -5))     # B über der Achse (unten: Achsenzahl 2)
         + [['t', [6, 4], "A′", 'ecke', 9, -2], ['t', [5, 4.5], "B′", 'ecke', -6, -5], ['t', [5.5, 2.5], "C′", 'ecke', 7, 11]],
         '-1.5,8,-1.2', 230, 170, karo=True, achsen=True)),
    ('1e', 2, r"Tim schreibt: «Bei \(k = -2\) wird eine \(3\,\text{cm}\) lange Strecke \(-6\,\text{cm}\) lang, und weil das Bild gespiegelt ist, hat es andere Winkel.» Was ist falsch?",
     r"<p>Längen sind nie negativ: Die Bildstrecke ist \(|{-2}| \cdot 3 = 6\,\text{cm}\) lang. Und die Winkel bleiben bei jeder zentrischen Streckung gleich — bei \(k \lt 0\) ist das Bild um \(Z\) gedreht, die Form bleibt dieselbe.</p>", ''),
])
k1 = kapitel(1, 'zentrische-streckung', 'Zentrische Streckung', 40,
             r'Du führst eine zentrische Streckung mit Zentrum \(Z\) und Streckfaktor \(k\) aus — auch mit negativem \(k\) und mit Koordinaten — und nennst ihre Eigenschaften.',
             ('g5-2d-lp-streckung', 'Zentrische Streckung'), sim1, ('g5-2d-lp-kontrolle-streckung', 'Kontrollfragen zur zentrischen Streckung'),
             fest1, [uebung('bildpunkt', 'Bildpunkt berechnen', 'Koordinatennetz mit Zentrum Z und Punkt P'), uebung('streckfaktor', 'Streckfaktor und Längen')],
             auf1, f'<a href="{TS}#darstellungen">Themenseite 5.2d, Zentrische Streckung</a> (Animation 1 mit ziehbaren Punkten)', komp='K3')

# ------------------------------------------------------------------ Kapitel 2
sim2 = bereich(2, 'Zwei Strahlen von S aus, geschnitten von AB und einer zweiten Geraden durch A′, die man verschieben und kippen kann',
               regler('s2', 'k', 'Streckfaktor k', -1.5, 2.5, 0.5, 2.5, 'orange') + '\n          '
               + regler('s2', 'd', 'Kippen δ', -15, 15, 5, 0, einheit='°'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Strahlensätze</div>
          <p><b>Die Figur:</b> Zwei Geraden schneiden sich in \(S\) und werden von zwei Parallelen geschnitten, \(AB \parallel A'B'\). Das ist eine zentrische Streckung mit Zentrum \(S\): \(|k| = \overline{SA'} : \overline{SA}\).</p>
          <p><b>1. Strahlensatz</b> (Abschnitte auf den Strahlen): \(\overline{SA} : \overline{SA'} = \overline{SB} : \overline{SB'}\), gleichwertig \(\overline{SA} : \overline{AA'} = \overline{SB} : \overline{BB'}\).</p>
          <p><b>2. Strahlensatz</b> (mit den Parallelenabschnitten): \(\overline{SA} : \overline{SA'} = \overline{AB} : \overline{A'B'}\), ebenso \(\overline{SB} : \overline{SB'} = \overline{AB} : \overline{A'B'}\) — immer mit den ganzen Strecken ab \(S\).</p>
          <p>Liegt \(S\) zwischen den Parallelen (<b>X-Figur</b>, \(k \lt 0\)), gelten dieselben Gleichungen mit den Längen.</p>
          <p><b>Abstände:</b> Auch die Abstände von \(S\) zu den beiden Parallelen (senkrecht gemessen) stehen im Verhältnis \(|k|\): Die Streckung bildet das Lot von \(S\) auf \(AB\) auf das Lot von \(S\) auf \(A'B'\) ab. So rechnet man mit Abständen, wenn die Strecken auf den Strahlen nicht bekannt sind (Schatten einer Lampe an der Wand).</p>
          <p><b>Umkehrung des 1. Strahlensatzes:</b> Liegen \(A'\) auf dem Strahl \(SA\) und \(B'\) auf dem Strahl \(SB\) (oder beide auf den Gegenstrahlen, X-Figur) und gilt \(\overline{SA} : \overline{SA'} = \overline{SB} : \overline{SB'}\), dann ist \(AB \parallel A'B'\). Ohne diese Lagebedingung stimmt es nicht: Liegt nur \(B'\) jenseits von \(S\), sind die Verhältnisse gleich, aber die Geraden nicht parallel. Für den 2. Strahlensatz gilt die Umkehrung nicht.</p>
          <p>Beispiel (Themenseite, A2): \(\overline{SA} = 4\), \(\overline{SA'} = 10\), \(\overline{SB} = 3\): \(\tfrac{4}{10} = \tfrac{3}{\overline{SB'}}\), also \(\overline{SB'} = \tfrac{10 \cdot 3}{4} = 7.5\) und \(\overline{BB'} = 4.5\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(\overline{SA} : \overline{AA'} = \overline{AB} : \overline{A'B'}\) ansetzen: Beim 2. Strahlensatz gehören die ganzen Strecken ab \(S\) dazu, also \(\overline{SA'}\), nicht \(\overline{AA'}\).</p>
          <p>Die Strahlensätze ohne Parallelen anwenden: Sind \(AB\) und \(A'B'\) nicht parallel, stimmen die Verhältnisse nicht.</p>
          <p>Unterschiede übertragen statt Verhältnisse: Ist \(\overline{SA'}\) um \(3\) länger als \(\overline{SA}\), ist \(\overline{SB'}\) nicht auch um \(3\) länger.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 15, [
    ('2a', 3, r'Mia will wissen, wie breit der Fluss ist. Der Baum \(T\) steht am anderen Ufer genau gegenüber von \(P\). Sie geht dem Ufer entlang \(30\,\text{m}\) bis \(S\) und weitere \(10\,\text{m}\) bis \(Q\), dann rechtwinklig vom Fluss weg, bis sie \(T\) und \(S\) hintereinander sieht: Das ist nach \(8\,\text{m}\) im Punkt \(R\). Wie breit ist der Fluss?',
     r"<p>\(PT \parallel QR\) (beide senkrecht zum Ufer), \(S\) liegt zwischen ihnen: X-Figur. \(\overline{PT} : \overline{QR} = \overline{SP} : \overline{SQ}\), also \(\overline{PT} = 8 \cdot \tfrac{30}{10} = 24\,\text{m}\).</p>",
     fig([['s', [-4, 0], [44, 0], 'boden'], ['s', [-4, 24], [44, 24], 'boden'], ['t', [22, 19], 'Fluss', 'mass', 0, 4, 'start'],
          ['s', [0, 0], [0, 24], 'hilfe2'], ['s', [40, 0], [40, -8], 'figur-linie'], ['s', [0, 24], [40, -8], 'strahl'],
          ['r', [0, 0], [1, 0], [0, 1]], ['r', [40, 0], [-1, 0], [0, -1]]]
         + ecken(([0, 24], 'T', -8, -4), ([0, 0], 'P', -8, 12), ([30, 0], 'S', -2, -6), ([40, 0], 'Q', 8, -4), ([40, -8], 'R', 8, 10))
         + [['t', [15, 0], '30 m', 'mass', 0, 11], ['t', [35, 0], '10 m', 'mass', 0, -5], ['t', [40, -4], '8 m', 'mass', 6, 4, 'start']],
         '-6,47,-11', 240, 175)),
    ('2b', 3, r"Zwei Geraden schneiden sich in \(S\). \(\overline{SA} = 6\), \(\overline{SA'} = 9\), \(\overline{SB} = 4\), \(\overline{SB'} = 6.5\) (\(A\), \(A'\) auf der einen, \(B\), \(B'\) auf der anderen Geraden, auf derselben Seite von \(S\)). Sind \(AB\) und \(A'B'\) parallel? Wie lang müsste \(\overline{SB'}\) sein, damit sie es sind?",
     r"<p>\(\tfrac{6}{9} \approx 0.667\), aber \(\tfrac{4}{6.5} \approx 0.615\): Die Verhältnisse sind verschieden, also sind \(AB\) und \(A'B'\) <b>nicht</b> parallel. Parallel wären sie bei \(\overline{SB'} = 4 \cdot \tfrac{9}{6} = 6\) (Umkehrung des 1. Strahlensatzes).</p>", ''),
    ('2c', 2, r"Warum gilt \(\overline{AB} : \overline{A'B'} = \overline{SA} : \overline{SA'}\), aber im Allgemeinen nicht \(\overline{AB} : \overline{A'B'} = \overline{SA} : \overline{AA'}\)?",
     r"<p>Die Figur ist eine zentrische Streckung mit Zentrum \(S\): Sie bildet \(A\) auf \(A'\) und die Strecke \(AB\) auf \(A'B'\) ab, mit \(|k| = \tfrac{\overline{SA'}}{\overline{SA}}\). Darum ist \(\tfrac{\overline{A'B'}}{\overline{AB}} = \tfrac{\overline{SA'}}{\overline{SA}}\). \(\overline{AA'}\) ist kein Bild einer Strecke ab \(S\); das Verhältnis \(\overline{SA} : \overline{AA'}\) gehört nur zum 1. Strahlensatz (Strahl mit Strahl).</p>", ''),
    ('2d', 3, r"X-Figur im Bild: \(AB \parallel A'B'\), \(\overline{SA} = 2.4\), \(\overline{SB} = 3\), \(\overline{SA'} = 4\), \(\overline{A'B'} = 6\). Berechne \(\overline{SB'}\) und \(\overline{AB}\).",
     r"<p>\(|k| = \tfrac{4}{2.4} = \tfrac{5}{3}\). \(\overline{SB'} = 3 \cdot \tfrac{5}{3} = 5\); \(\overline{AB} = 6 \cdot \tfrac{2.4}{4} = 3.6\).</p>",
     fig([['g', [0, 0], [1, 0]], ['g', [0, 0], [0.125, 0.9922]], ['s', [2.4, 0], [0.375, 2.976], 'figur-linie'], ['s', [-4, 0], [-0.625, -4.961], 'bild-linie']]
         + ecken(([0, 0], 'S', 9, 12), ([2.4, 0], 'A', 6, 12), ([0.375, 2.976], 'B', 9, -2), ([-4, 0], "A′", -6, -5), ([-0.625, -4.961], "B′", 10, 4))
         + [['t', [1.2, 0], '2.4', 'mass', 0, -5], ['t', [0.19, 1.49], '3', 'mass', -7, 2, 'end'], ['t', [-2, 0], '4', 'mass', 0, 11], ['t', [-2.31, -2.48], '6', 'mass', -6, 4, 'end']],
         '-5.2,4,-5.8', 190, 210)),
    ('2e', 2, r"Eine Strassenlaterne ist \(6\,\text{m}\) hoch. Eine \(1.8\,\text{m}\) grosse Person steht \(4\,\text{m}\) vom Mast entfernt. Wie lang ist ihr Schatten?",
     r"<p>Vom Schattenende \(E\) aus: Mast und Person sind parallel, also \(\tfrac{s}{s + 4} = \tfrac{1.8}{6}\). Daraus \(6s = 1.8s + 7.2\), \(s = \tfrac{7.2}{4.2} \approx 1.71\,\text{m}\).</p><p class='komm'>Die Laterne der Themenseite (Einstieg) zeigt dieselbe Figur zum Ziehen.</p>",
     fig([['s', [-0.6, 0], [6.6, 0], 'boden'], ['s', [0, 0], [0, 6], 'baum'], ['s', [4, 0], [4, 1.8], 'person'], ['s', [0, 6], [5.714, 0], 'strahl'],
          ['t', [2, 0], '4 m', 'mass', 0, 11], ['t', [0, 3], '6 m', 'mass', -5, 4, 'end'], ['t', [4, 0.9], '1.8 m', 'mass', 5, 4, 'start'], ['t', [4.86, 0], 's', 'mass', 0, 11], ['t', [5.714, 0], 'E', 'ecke', 6, -4]],
         '-1.6,7.4,-0.9', 200, 175)),
    # 2f (Behebung 08.10.2026): Abstände statt Strecken auf den Strahlen — Vorbereitung auf die Lochkamera im Gesamttest
    # (dort X-Figur mit Abständen). L(0 | 0), Karte x = 30 von y = 4 bis 16, Wand x = 120, Schatten 16 … 64 (mal 4).
    ('2f', 2, r'Eine kleine Lampe \(L\) beleuchtet eine \(12\,\text{cm}\) hohe Karte. Die Karte steht parallel zur Wand, \(30\,\text{cm}\) von der Lampe entfernt, die Wand \(1.2\,\text{m}\) von der Lampe (beide Abstände senkrecht gemessen, Bild). Wie hoch ist der Schatten der Karte an der Wand? Warum darfst du mit den Abständen rechnen, obwohl die Lichtstrahlen schräg laufen?',
     r"<p>Die Lampe ist das Zentrum einer Streckung, die die Karte auf ihren Schatten abbildet (Karte und Wand sind parallel). Sie bildet auch das Lot von \(L\) auf die Kartenebene auf das Lot von \(L\) auf die Wand ab: Die Abstände stehen im selben Verhältnis, \(|k| = \tfrac{120}{30} = 4\). Schatten: \(4 \cdot 12 = 48\,\text{cm}\).</p><p class='komm'>Die Strecken auf den Lichtstrahlen kennst du nicht — die Abstände genügen.</p>",
     fig([['s', [120, -12], [120, 70], 'boden'], ['t', [120, 70], 'Wand', 'mass', -4, 10, 'end'],
          ['s', [0, 0], [120, 0], 'hilfe2'], ['s', [30, 0], [30, 4], 'hilfe2'], ['r', [30, 0], [-1, 0], [0, 1]], ['r', [120, 0], [-1, 0], [0, 1]],
          ['s', [0, 0], [120, 16], 'massl'], ['s', [0, 0], [120, 64], 'massl'],      # Lichtstrahlen dünn und voll, das Lot gestrichelt
          ['s', [30, 4], [30, 16], 'figur-linie'], ['s', [120, 16], [120, 64], 'bild-linie'], ['p', [0, 0]], ['t', [0, 0], 'L', 'ecke', -8, 4],
          ['t', [30, 10], '12 cm', 'mass', 4, 4, 'start'], ['t', [120, 40], '?', 'mass', 6, 4, 'start'],
          ['s', [0, -5], [30, -5], 'massl'], ['t', [15, -5], '30 cm', 'mass', 0, 11],
          ['s', [0, -12], [120, -12], 'massl'], ['t', [60, -12], '1.2 m', 'mass', 0, 11]],
         '-10,132,-25', 240, 165)),
])
k2 = kapitel(2, 'strahlensaetze', 'Strahlensätze', 50,
             r'Du erkennst die Strahlensatzfigur, stellst mit dem 1. oder 2. Strahlensatz die passende Verhältnisgleichung auf — auch in der X-Figur und mit den Abständen von \(S\) — und weisst, dass sie nur mit Parallelen gilt.',
             ('g5-2d-lp-strahlensaetze', 'Strahlensätze'), sim2, ('g5-2d-lp-kontrolle-strahlensaetze', 'Kontrollfragen zu den Strahlensätzen'),
             fest2, [uebung('strahlen1', '1. Strahlensatz', 'Strahlensatzfigur mit S, A, B, A′, B′'), uebung('strahlen2', '2. Strahlensatz', 'Strahlensatzfigur mit den Parallelen AB und A′B′')],
             auf2, f'<a href="{TS}#strahlensaetze">Themenseite 5.2d, Strahlensätze</a> und das <a href="{TS}#strahlensatz-labor">Strahlensatz-Labor</a>', komp='K3')

# ------------------------------------------------------------------ Kapitel 3
sim3 = bereich(3, 'Rechteck 3 cm mal 2 cm und ein zweites Rechteck mit veränderbarer Breite und Höhe in derselben Ecke',
               regler('s3', 'b', 'Breite b′', 1, 9, 0.5, 4.5, 'orange', ' cm') + '\n          '
               + regler('s3', 'h', 'Höhe h′', 1, 6, 0.5, 3, 'orange', ' cm'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ähnliche Figuren</div>
          <p>Zwei Figuren \(F_1\) und \(F_2\) heissen <b>ähnlich</b>, \(F_1 \sim F_2\), wenn eine zentrische Streckung — eventuell zusammen mit einer Verschiebung, Drehung oder Spiegelung — die eine in die andere überführt.</p>
          <p>Dann sind entsprechende Winkel gleich gross, und alle entsprechenden Seiten stehen im selben Verhältnis: \(\tfrac{a'}{a} = \tfrac{b'}{b} = \ldots = k\).</p>
          <p><b>Längen</b> — Seiten, Umfang, Radius, Höhen — wachsen mit \(k\), <b>Flächen</b> mit \(k^2\): \(\tfrac{A'}{A} = k^2\). Umgekehrt: \(k = \sqrt{\tfrac{A'}{A}}\) — oft keine «schöne» Zahl: Doppelte Fläche heisst \(k = \sqrt{2} \approx 1.41\), dreifache \(k = \sqrt{3} \approx 1.73\).</p>
          <p>Rechteck \(3 \times 2\) und \(4.5 \times 3\): \(k = 1.5\); Umfang \(10 \to 15\), Fläche \(6 \to 2.25 \cdot 6 = 13.5\). Alle Quadrate und alle Kreise sind ähnlich, Rechtecke nur bei gleichem Seitenverhältnis.</p>
          <p><b>Massstab \(1 : n\):</b> Längen sind in Wirklichkeit \(n\)-mal so lang, Flächen \(n^2\)-mal so gross. Plan \(1 : 200\) (Themenseite, A7): \(2.5\,\text{cm} \to 500\,\text{cm} = 5\,\text{m}\); \(6.25\,\text{cm}^2 \to 6.25 \cdot 40\,000\,\text{cm}^2 = 25\,\text{m}^2\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Flächen mit \(k\) statt mit \(k^2\) rechnen: Doppelte Seiten geben die <b>vierfache</b> Fläche.</p>
          <p>Das Flächenverhältnis für \(k\) halten: Neunfache Fläche heisst \(k = 3\).</p>
          <p>Nur eine Seite vergleichen: Ähnlich ist eine Figur erst, wenn <b>alle</b> Seiten mit demselben Faktor wachsen.</p>
          <p>\(\text{cm}^2\) in \(\text{m}^2\) mit \(100\) umrechnen: \(1\,\text{m}^2 = 10\,000\,\text{cm}^2\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Eine Pizza mit \(30\,\text{cm}\) Durchmesser kostet CHF 18, eine mit \(40\,\text{cm}\) CHF 30. Welche ist im Verhältnis zur Fläche günstiger? Rechne mit dem Streckfaktor.',
     r"<p>\(k = \tfrac{40}{30} = \tfrac{4}{3}\), die Fläche wächst mit \(k^2 = \tfrac{16}{9} \approx 1.78\). Der Preis wächst nur mit \(\tfrac{30}{18} \approx 1.67\): Die grosse Pizza ist im Verhältnis günstiger.</p><p class='komm'>Mit \(k = 1.33\) statt \(k^2\) wirkt die grosse Pizza teurer — der typische Fehler.</p>", ''),
    ('3b', 3, r'Ein A4-Blatt ist \(21\,\text{cm} \times 29.7\,\text{cm}\), ein A5-Blatt \(14.8\,\text{cm} \times 21\,\text{cm}\). Sind die beiden Rechtecke ähnlich? Wie verhalten sich die Flächen, und warum passt das zum Streckfaktor?',
     r"<p>\(\tfrac{29.7}{21} \approx 1.414\) und \(\tfrac{21}{14.8} \approx 1.419\): Die Verhältnisse unterscheiden sich erst in der dritten Dezimale — so viel machen die auf Millimeter gerundeten Masse aus. Die Blätter sind ähnlich mit \(k \approx 1.41\). Flächen: \(623.7\,\text{cm}^2\) und \(310.8\,\text{cm}^2\), Verhältnis \(\approx 2.01\). Das passt: \(k^2 \approx 1.414^2 \approx 2\). A5 ist ein halbes A4-Blatt, also ist \(k = \sqrt{2}\).</p>", ''),
    # 3c an der Figur (Behebung 08.10.2026: Kapitel 3 hatte keine Aufgabe an der Figur): Plan im Karo, abzulesen
    ('3c', 2, r'Im Bild ist ein Zimmer auf einem Plan im Massstab \(1 : 50\) gezeichnet (ein Häuschen ist \(1\,\text{cm}\)). Wie gross ist das Zimmer in Wirklichkeit? Rechne die Fläche auf zwei Arten: aus den wirklichen Seiten und mit \(n^2\).',
     r"<p>Abgelesen: \(8\,\text{cm} \times 6\,\text{cm}\). Seiten \(8 \cdot 50 = 400\,\text{cm} = 4\,\text{m}\) und \(6 \cdot 50 = 3\,\text{m}\): \(12\,\text{m}^2\). Mit \(n^2\): \(48\,\text{cm}^2 \cdot 2500 = 120\,000\,\text{cm}^2 = 12\,\text{m}^2\).</p>",
     fig([['v', [[0, 0], [8, 0], [8, 6], [0, 6]]], ['t', [4, 3], 'Zimmer', 'mass', 0, 4]], '-1,9,-1', 200, 160, karo=True)),
    ('3d', 2, r'Warum sind alle Kreise zueinander ähnlich, aber nicht alle Rechtecke?',
     r"<p>Ein Kreis ist durch seinen Radius bestimmt: Mit \(k = \tfrac{r'}{r}\) geht jeder Kreis in jeden anderen über (Streckung vom Mittelpunkt aus, dann verschieben). Ein Rechteck hat zwei Seiten; ähnlich sind zwei Rechtecke nur, wenn beide Seiten mit demselben Faktor wachsen, also bei gleichem Seitenverhältnis (\(3 \times 2\) und \(6 \times 2\) nicht).</p>", ''),
    ('3e', 2, r'Ein Logo mit \(20\,\text{cm}^2\) wird zu einem ähnlichen Logo mit \(45\,\text{cm}^2\) vergrössert. Lena sagt: «Also ist \(k = 2.25\).» Stimmt das? Wie lang wird eine \(4\,\text{cm}\) lange Kante?',
     r"<p>Nein: \(2.25\) ist das Flächenverhältnis \(\tfrac{45}{20} = k^2\). Also \(k = \sqrt{2.25} = 1.5\), und die Kante wird \(1.5 \cdot 4 = 6\,\text{cm}\) lang.</p>", ''),
])
k3 = kapitel(3, 'aehnliche-figuren', 'Ähnliche Figuren: Längen und Flächen', 40,
             r'Du erkennst ähnliche Figuren an gleichen Winkeln und gleichen Seitenverhältnissen, rechnest Längen und Umfang mit \(k\), Flächen mit \(k^2\) und arbeitest mit dem Massstab.',
             ('g5-2d-lp-figuren', 'Ähnliche Figuren: Längen und Flächen'), sim3, ('g5-2d-lp-kontrolle-figuren', 'Kontrollfragen zu ähnlichen Figuren'),
             fest3, [uebung('flaeche', 'Fläche und Umfang mit k'), uebung('massstab', 'Massstab')],
             auf3, f'<a href="{TS}#aehnlichkeit">Themenseite 5.2d, Ähnliche Figuren</a> (Animation 4 mit Dreieck, Rechteck und Kreis)', komp='K3 · K2 Umfang, Fläche')

# ------------------------------------------------------------------ Kapitel 4
sim4 = bereich(4, 'Dreieck ABC mit 50, 70 und 60 Grad und ein zweites Dreieck A′B′C′ aus zwei Winkeln und einer Seite',
               regler('s4', 'al', 'Winkel α′', 30, 90, 5, 70, 'orange', '°') + '\n          '
               + regler('s4', 'be', 'Winkel β′', 30, 90, 5, 60, 'orange', '°') + '\n          '
               + regler('s4', 'c', 'Seite c′', 2, 6.5, 0.5, 5.5, einheit=' cm'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ähnliche Dreiecke</div>
          <p><b>Hauptähnlichkeitssatz (WW):</b> Zwei Dreiecke sind ähnlich, wenn sie in zwei Winkeln übereinstimmen. Der dritte Winkel folgt aus der Winkelsumme \(180°\).</p>
          <p>Weitere Sätze — ähnlich bei Übereinstimmung im Verhältnis aller drei Seiten (<b>sss</b>), im Verhältnis zweier Seiten und dem eingeschlossenen Winkel (<b>sWs</b>) oder im Verhältnis zweier Seiten und dem Gegenwinkel der grösseren Seite (<b>SsW</b>). Das kleine s steht für ein Seitenverhältnis.</p>
          <p><b>Zuordnen:</b> Entsprechende Seiten liegen gleichen Winkeln gegenüber — nicht gleichen Buchstaben. Dann \(k\) aus einem Paar entsprechender Seiten und jede Seite mal \(k\).</p>
          <p><b>Schatten:</b> Die Sonnenstrahlen sind parallel, die Schattendreiecke haben gleiche Winkel (WW). Stab \(1.80\,\text{m}\), Schatten \(1.20\,\text{m}\); Baumschatten \(7.80\,\text{m}\): \(h = 7.80 \cdot \tfrac{1.80}{1.20} = 11.70\,\text{m}\) (Themenseite, A6).</p>
          <p><b>Rechtwinkliges Dreieck</b> (rechter Winkel bei \(C\)): Die Höhe \(h\) auf die Hypotenuse \(c\) (Fusspunkt \(H\)) teilt sie in \(p\) (an \(a\)) und \(q\) (an \(b\)). \(\triangle ABC \sim \triangle AHC \sim \triangle CHB\) — jedes Teildreieck hat einen rechten Winkel und einen spitzen Winkel mit dem ganzen gemeinsam. Daraus:</p>
          <p>\[ h^2 = p \cdot q \qquad a^2 = p \cdot c \qquad b^2 = q \cdot c \]</p>
          <p>(Höhensatz aus \(\tfrac{h}{p} = \tfrac{q}{h}\), Kathetensatz aus \(\tfrac{a}{p} = \tfrac{c}{a}\).) Beispiel \(p = 1.8\), \(q = 3.2\): \(h = \sqrt{5.76} = 2.4\), \(c = 5\), \(a = \sqrt{9} = 3\), \(b = \sqrt{16} = 4\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Seiten nach den Buchstaben statt nach den Winkeln zuordnen.</p>
          <p>Zwei passende Seitenverhältnisse für genug halten: Bei sss müssen alle drei stimmen (\(3, 4, 5\) und \(6, 8, 9\) sind nicht ähnlich).</p>
          <p>Im Kathetensatz den falschen Abschnitt nehmen: Zu \(a\) gehört \(p\), der Abschnitt, der an \(a\) anliegt.</p>
        </div>
      </div>'''
# Aufgabe 4a: ABC mit a = BC = 5, b = CA = 4, c = AB = 6 (Winkel 55.77°, 41.41°, 82.82°); PQR = 1.5-fach, Q ↔ A, R ↔ B, P ↔ C.
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 3, r'Im Bild sind gleich markierte Winkel gleich gross. \(\overline{AB} = 6\), \(\overline{BC} = 5\), \(\overline{CA} = 4\) und \(\overline{QR} = 9\). Begründe, warum die Dreiecke ähnlich sind, und berechne \(\overline{PQ}\) und \(\overline{RP}\).',
     r"<p>Zwei (sogar drei) Winkel stimmen überein: ähnlich (WW). Zuordnung nach den Winkeln: \(Q \leftrightarrow A\), \(R \leftrightarrow B\), \(P \leftrightarrow C\). \(QR\) entspricht \(AB\): \(k = \tfrac{9}{6} = 1.5\). \(PQ\) entspricht \(CA\): \(1.5 \cdot 4 = 6\); \(RP\) entspricht \(BC\): \(1.5 \cdot 5 = 7.5\).</p><p class='komm'>Wer \(PQ\) zu \(AB\) zuordnet (gleiche Stelle im Namen), bekommt falsche Werte.</p>",
     fig([['v', [[0, 0], [6, 0], [2.25, 3.307]]], ['v', [[11.089, 0], [15.957, 3.507], [7.5, 6.585]], 'bild'],
          ['w', [0, 0], [6, 0], [2.25, 3.307], None, 10, 1], ['w', [6, 0], [2.25, 3.307], [0, 0], None, 10, 2], ['w', [2.25, 3.307], [0, 0], [6, 0], None, 10, 3],
          ['w', [15.957, 3.507], [7.5, 6.585], [11.089, 0], None, 10, 1], ['w', [7.5, 6.585], [11.089, 0], [15.957, 3.507], None, 10, 2], ['w', [11.089, 0], [15.957, 3.507], [7.5, 6.585], None, 10, 3]]
         + ecken(([0, 0], 'A', -7, 11), ([6, 0], 'B', 7, 11), ([2.25, 3.307], 'C', 0, -7), ([11.089, 0], 'P', 2, 12), ([15.957, 3.507], 'Q', 8, 4), ([7.5, 6.585], 'R', -7, -4)),
         '-1,17,-1.3', 260, 135)),    # 135 statt 120 px: R (y = 6.585) samt Namen im Bild; unten Platz für P
    ('4b', 3, r'Dreieck 1 hat die Seiten \(5\), \(7\) und \(8\). (a) Ist Dreieck 2 mit den Seiten \(12\), \(7.5\) und \(10.5\) ähnlich dazu? (b) Und Dreieck 3 mit \(7.5\), \(10.5\) und \(13\)?',
     r"<p>Der Grösse nach ordnen. (a) \(\tfrac{7.5}{5} = \tfrac{10.5}{7} = \tfrac{12}{8} = 1.5\): ähnlich (sss), \(k = 1.5\). (b) \(\tfrac{7.5}{5} = \tfrac{10.5}{7} = 1.5\), aber \(\tfrac{13}{8} = 1.625\): nicht ähnlich — zwei passende Verhältnisse genügen nicht.</p>", ''),
    ('4c', 3, r'Eine \(1.65\,\text{m}\) grosse Person wirft einen \(2.2\,\text{m}\) langen Schatten. Gleichzeitig wirft ein Kirchturm einen \(36.8\,\text{m}\) langen Schatten. Skizziere die beiden Dreiecke und berechne die Höhe des Turms. Warum sind die Dreiecke ähnlich?',
     r"<p>Beide Dreiecke haben einen rechten Winkel am Boden und denselben Winkel der Sonnenstrahlen (parallel): WW. \(\tfrac{h}{36.8} = \tfrac{1.65}{2.2}\), also \(h = 36.8 \cdot 0.75 = 27.6\,\text{m}\).</p>", ''),
    ('4d', 3, r'Im rechtwinkligen Dreieck \(ABC\) (rechter Winkel bei \(C\)) teilt die Höhe die Hypotenuse in \(p = 5\,\text{cm}\) <span class="nb">(an \(a\))</span> und \(q = 7.2\,\text{cm}\) <span class="nb">(an \(b\)).</span> Berechne \(h\), \(a\) und \(b\).',
     r"<p>\(h = \sqrt{5 \cdot 7.2} = \sqrt{36} = 6\,\text{cm}\); \(c = 12.2\,\text{cm}\); \(a = \sqrt{5 \cdot 12.2} = \sqrt{61} \approx 7.81\,\text{cm}\); \(b = \sqrt{7.2 \cdot 12.2} = \sqrt{87.84} \approx 9.37\,\text{cm}\). Probe: \(61 + 87.84 = 148.84 = 12.2^2\).</p>",
     fig([['v', [[0, 0], [12.2, 0], [7.2, 6]]], ['s', [7.2, 6], [7.2, 0], 'hilfe'], ['r', [7.2, 0], [1, 0], [0, 1]]]
         + ecken(([0, 0], 'A', -7, 11), ([12.2, 0], 'B', 7, 11), ([7.2, 6], 'C', 0, -7)) + [['t', [7.2, 0], 'H', 'ecke', 0, 13],
         ['t', [3.6, 0], 'q = 7.2', 'mass', 0, 24], ['t', [9.7, 0], 'p = 5', 'mass', 0, 24], ['t', [7.2, 3], 'h', 'mass', 5, 4, 'start'], ['t', [3.4, 3.3], 'b', 'mass', -4, -3, 'end'], ['t', [9.9, 3.2], 'a', 'mass', 6, -3, 'start']],
         '-1.2,13.4,-1.7', 230, 150)),   # 150 statt 120 px: C (y = 6) samt Namen im Bild
    ('4e', 2, r'Warum genügen bei Dreiecken zwei gleiche Winkel für die Ähnlichkeit, bei Vierecken aber nicht?',
     r"<p>Im Dreieck legt die Winkelsumme den dritten Winkel fest; alle Winkel gleich heisst beim Dreieck schon gleiche Form (die Seiten sind dann proportional). Beim Viereck nicht: Ein Quadrat und ein Rechteck \(4 \times 1\) haben vier rechte Winkel, aber verschiedene Seitenverhältnisse — sie sind nicht ähnlich.</p>", ''),
    # 4f (Behebung 08.10.2026: sWs nur genannt): ineinanderliegende Dreiecke mit gemeinsamem Winkel, DE nicht parallel zu BC.
    # A(0 | 0), B(8 | 0), C mit AC = 6, BC = 7 (cos α = 51/96): C(3.1875 | 5.0833); D(3 | 0), E = 4/6 · C = (2.125 | 3.3889).
    ('4f', 2, r'Im Dreieck \(ABC\) ist \(\overline{AB} = 8\,\text{cm}\), \(\overline{AC} = 6\,\text{cm}\) und \(\overline{BC} = 7\,\text{cm}\). \(D\) liegt auf \(AB\) mit \(\overline{AD} = 3\,\text{cm}\), \(E\) auf \(AC\) mit \(\overline{AE} = 4\,\text{cm}\) (Bild). Begründe, warum die Dreiecke \(ADE\) und \(ACB\) ähnlich sind, und berechne \(\overline{DE}\).',
     r"<p>Beide Dreiecke haben den Winkel bei \(A\) gemeinsam, und \(\tfrac{\overline{AD}}{\overline{AC}} = \tfrac{3}{6} = 0.5 = \tfrac{4}{8} = \tfrac{\overline{AE}}{\overline{AB}}\): zwei Seiten im selben Verhältnis und der eingeschlossene Winkel gleich — ähnlich (sWs), mit \(D \leftrightarrow C\), \(E \leftrightarrow B\), \(k = 0.5\). \(DE\) entspricht \(CB\): \(\overline{DE} = 0.5 \cdot 7 = 3.5\,\text{cm}\).</p><p class='komm'>\(DE\) ist nicht parallel zu \(BC\) (\(\tfrac{3}{8} \neq \tfrac{4}{6}\)) — der Strahlensatz hilft hier nicht, die Ähnlichkeit schon. Wer \(D\) zu \(B\) zuordnet, findet zwei verschiedene Verhältnisse.</p>",
     fig([['v', [[0, 0], [8, 0], [3.1875, 5.0833]]], ['s', [3, 0], [2.125, 3.3889], 'hilfe'], ['p', [3, 0]], ['p', [2.125, 3.3889]],
          ['w', [0, 0], [8, 0], [3.1875, 5.0833], None, 16]]
         + ecken(([0, 0], 'A', -7, 11), ([8, 0], 'B', 7, 11), ([3.1875, 5.0833], 'C', 0, -7))
         + [['t', [3, 0], 'D', 'ecke', 0, 13], ['t', [2.125, 3.3889], 'E', 'ecke', -8, -2]],
         '-1,9,-1.2', 220, 165)),
])
k4 = kapitel(4, 'aehnliche-dreiecke', 'Ähnliche Dreiecke', 50,
             r'Du entscheidest, ob zwei Dreiecke ähnlich sind — vor allem mit zwei gleichen Winkeln (WW), daneben mit Seitenverhältnissen (sss, sWs, SsW) —, ordnest entsprechende Seiten über die Winkel zu und berechnest fehlende Längen — auch mit der Höhe im rechtwinkligen Dreieck.',
             ('g5-2d-lp-dreiecke', 'Ähnliche Dreiecke'), sim4, ('g5-2d-lp-kontrolle-dreiecke', 'Kontrollfragen zu ähnlichen Dreiecken'),
             fest4, [uebung('aehnlich', 'Ähnlich oder nicht?'), uebung('zuordnen', 'Seiten zuordnen', 'Zwei ähnliche Dreiecke mit gleich markierten Winkeln'),
                     uebung('hoehensatz', 'Höhe im rechtwinkligen Dreieck', 'Rechtwinkliges Dreieck mit der Höhe auf die Hypotenuse')],
             auf4, f'<a href="{TS}#aehnlichkeitssaetze">Themenseite 5.2d, Ähnlichkeitssätze</a> und <a href="{TS}#recht-dreieck">ähnliche Dreiecke im rechtwinkligen Dreieck</a>', komp='K3 · K1 Dreiecke')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 5.1 · 5.2a</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Verhältnisgleichungen, Winkelsumme, Koordinaten, Flächen und Einheiten. Wenn das wackelt: <a href="dreiecke.html">Leitprogramm Dreiecke</a> (Kapitel 1 und 3) und die <a href="../grundlagen/g5-2a-dreiecke.html">Themenseite 5.2a</a>.</p>
      ''' + clipkarte('g1-4-einheiten', 'Einheiten: Länge, Fläche, Volumen') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Löse: (a) \(\dfrac{x}{6} = \dfrac{4}{3}\) (b) \(\dfrac{5}{x} = \dfrac{2}{7}\)',
     r'<p>(a) \(x = 6 \cdot \tfrac{4}{3} = 8\). (b) Über Kreuz: \(2x = 35\), \(x = 17.5\).</p><p class="komm">Solche Verhältnisgleichungen brauchst du in jedem Kapitel.</p>', ''),
    ('0b', 2, r'(a) Ein Dreieck hat die Winkel \(48°\) und \(77°\). Wie gross ist der dritte? (b) Im Dreieck \(ABC\) liegt der rechte Winkel bei \(C\). Welche Seite ist die Hypotenuse?',
     r'<p>(a) \(180° - 48° - 77° = 55°\). (b) \(c = \overline{AB}\), die Seite gegenüber dem rechten Winkel.</p>', ''),
    ('0c', 2, r'Von \(Z(1 \mid 2)\) nach \(P(4 \mid 1)\): Wie weit nach rechts, wie weit nach oben? Und von \(P\) zurück nach \(Z\)?',
     r'<p>\(3\) nach rechts und \(-1\) nach oben (also \(1\) nach unten). Zurück: \(3\) nach links und \(1\) nach oben.</p>', ''),
    ('0d', 2, r'(a) Fläche eines Rechtecks \(4.5\,\text{cm} \times 2\,\text{cm}\)? (b) Fläche eines Kreises mit \(r = 3\,\text{cm}\)?',
     r'<p>(a) \(9\,\text{cm}^2\). (b) \(\pi \cdot 3^2 \approx 28.27\,\text{cm}^2\).</p>', ''),
    ('0e', 2, r'(a) Wie viele \(\text{cm}^2\) sind \(3\,\text{m}^2\)? (b) Wie viele \(\text{m}\) sind \(450\,000\,\text{cm}\)?',
     r'<p>(a) \(1\,\text{m}^2 = 100 \cdot 100\,\text{cm}^2\), also \(30\,000\,\text{cm}^2\). (b) \(4500\,\text{m}\).</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/aehnlichkeit/'
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
          <p>Aufgabe → Kapitel: G1 → 1; G2, G3 → 2; G4, G5 → 3; G6, G7 → 4</p>
        </div>
      </div>
    </section>

    <section class="kap" id="weiter">
      <h2 id="weiter-titel">Weiter</h2>
      <p>Als Nächstes: <a href="trigonometrische-berechnungen.html">Leitprogramm Trigonometrische Berechnungen</a> (Teilgebiet 5.3) — dort hängen Sinus, Cosinus und Tangens nur vom Winkel ab, weil alle rechtwinkligen Dreiecke mit demselben Winkel ähnlich sind.</p>
      <p>Nicht in diesem Leitprogramm, sondern auf der <a href="{TS}">Themenseite 5.2d</a>: das Strahlensatz-Labor mit ziehbaren Punkten, Volumen im Raum (\\(|k|^3\\)) und die Herleitung des Satzes von Pythagoras aus dem Kathetensatz. Die übrigen Teile von GF 5.2 — Dreiecke, Vierecke, Kreis und Kreisteile — stehen auf den Themenseiten 5.2a bis 5.2c.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Zentrische Streckung und Ähnlichkeit, Version 1.0 (08.10.2026). Gebaut aus scripts/lp/aehnlichkeit/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlage: HOWTO-leitprogramme.md, Vorbilder Planimetrie (Kapitel 5) und
     Trigonometrische Berechnungen (Geometrie-Arbeitsbereich).

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie, wörtlich (wie in der Kompetenzbox der Themenseite 5.2d):
       K1  geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke,
           Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
       K2  deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante,
           Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen
       K3  die Ähnlichkeit für Berechnungen in der Ebene nutzen
     Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Dieses Leitprogramm gehört zur Themenseite 5.2d und
     nimmt K3 ganz; von K1 und K2 nur, was die Ähnlichkeit betrifft (ähnliche Dreiecke, Rechtecke, Quadrate, Kreise
     beschreiben; Umfang, Fläche und Abstand zum Zentrum über k bzw. k² berechnen). Der Rest von K1/K2 → Leitprogramme
     Dreiecke, Vierecke, Kreis und Kreisteile (Themenseiten 5.2a–c).

     a) Kompetenzmatrix (Kompetenz | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest) — nachgeführt nach der Prüfung 08.10.2026:
       K3 Ähnlichkeit nutzen        | nein | 1, 2, 3, 4 | 1a–1e, 2a–2f, 3a–3e, 4a–4f | G1–G7
       K2 nur Umfang/Fläche/Abstand | nein | 1 (Abstand ZP′), 2 (Abstände von S, 2f), 3 (Umfang, Fläche) | 1e, 2f, 3a–3e | G1 (b), G3, G4, G5
       K1 nur ähnliche Figuren      | nein | 3, 4 | 3b, 3d, 4b, 4e, 4f | G6 (a)
       Teilkompetenzen der Themenseite (Lernziele) → Kapitel → Übung → Gesamttest:
         zentrische Streckung ausführen, Eigenschaften   → 1 → bildpunkt, streckfaktor → G1
         Strahlensätze anwenden (X-Figur, Abstände, Umkehrung) → 2 → strahlen1, strahlen2 → G2, G3 (X-Figur mit Abständen,
                                                                     vorher geübt in 2a/2d bzw. 2f)
         Ähnlichkeit erklären; k und k² unterscheiden      → 3 → flaeche (auch k = √q), massstab → G4, G5 (k = √3)
         Ähnlichkeitssätze anwenden; Höhe im rw. Dreieck   → 4 → aehnlich (WW, sss, sWs, SsW), zuordnen, hoehensatz → G6 (WW,
                                                                     Zuordnung, Fehler in einer fremden Lösung), G7
         sss, sWs, SsW: Clip, Übung «Ähnlich oder nicht?», 4b, 4f — im Gesamttest nicht eigens (G6 prüft den Entscheid mit WW).
       Gesamttest neu kombiniert, nicht wiederholt: G6 (Lara ordnet nach Buchstaben zu, k < 1) statt der Kopie von 4a; die
       Selbsteinschätzung verweist jede Aufgabe auf ein Kapitel.

     b) Planungstabelle (Kapitel | Lernziel | Clips | Erkundung | Beispiel (Quelle) | Häufiger Fehler | min):
       0 Vorwissen  | Verhältnisgleichung, Winkelsumme, Koordinaten, Flächen, Einheiten | g1-4-einheiten | — | — | — | 10
       1 Streckung  | ausführen, k < 0, Koordinaten, Eigenschaften | g5-2d-lp-streckung, -kontrolle-streckung | sim1 (k) |
         Z(1|1), Dreieck A(2|3) B(3|1) C(5|4), k = 1.5 (Anim 1: Start 1.5) | k·P statt Z + k(P − Z), negative Länge | 40
       2 Strahlensätze | 1. und 2. Satz, X-Figur, Abstände, nur mit Parallelen, Umkehrung (mit Lage) | g5-2d-lp-strahlensaetze,
         -kontrolle | sim2 (k, δ) | SA = 4, SA′ = 10, SB = 3 (A2) | SA : AA′ = AB : A′B′, Differenzen | 50
       3 Ähnliche Figuren | Definition, k für Längen, k² für Flächen, Massstab | g5-2d-lp-figuren, -kontrolle | sim3 (b′, h′) |
         Rechteck 3 × 2 → 4.5 × 3 (Anim 4: k = 1.5), Plan 1 : 200 (A7) | k statt k², k² für k, cm² → m² | 40
       4 Ähnliche Dreiecke | WW, sss, sWs, SsW, zuordnen, Schatten, Höhe im rw. Dreieck | g5-2d-lp-dreiecke, -kontrolle | sim4 (α′, β′, c′) |
         50°/70° (Anim 5), Schatten 1.80/1.20/7.80 (A6), p = 1.8, q = 3.2 | Zuordnung nach Buchstaben, nur zwei Verhältnisse | 50
       Gesamttest 30. Summe 220 min ≈ 4.9 Lektionen (vier Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest).

     c) Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.2d): das Strahlensatz-Labor mit ziehbaren Punkten (Link),
        Volumen im Raum (|k|³), Pythagoras aus dem Kathetensatz. Vorgezogen und kurz erklärt: «ähnlich» schon in Kapitel 1
        (gleiche Form), genau definiert in Kapitel 3.

     d) Konventionen wie auf der Themenseite: Z, k, P′; S, A, B, A′, B′, AB ∥ A′B′; F₁ ~ F₂; Sätze WW (Hauptähnlichkeitssatz),
        sss, sWs, SsW; rechter Winkel bei C, Höhe h, Fusspunkt H, p an a, q an b, a² = p·c, b² = q·c, h² = p·q. Längen mal |k|.
        Gemeldet, nicht übernommen (Themenseite): «Bei k < 0 ist die Abbildung gegensinnig» und die Live-Anzeige
        «Orientierung: gespiegelt» (Anim 1) — eine zentrische Streckung mit k < 0 ist eine Drehung um 180° mal |k|, der
        Umlaufsinn bleibt; «Quotient … gleich dem Streckfaktor k» (Verhältnistreue) und «Längen mit k multipliziert» (Fehler-
        kasten) statt |k|. Hier: «bei k < 0 zusätzlich um Z um 180° gedreht», Längen mal |k|.

     Farben: Original blau, Bild/Streckfaktor/Hilfslinie orange, Ergebnis grün, Fehler rot (wie Themenseite und Clips).
     Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus
     LaTeX (downloads/leitprogramme/aehnlichkeit/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Zentrische Streckung und Ähnlichkeit</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.2d</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Zentrische Streckung</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Strahlensätze</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Ähnliche Figuren</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Ähnliche Dreiecke</span></a></li>
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
          <li><b>② Tüfteln:</b> Im Arbeitsbereich veränderst du die Figur, tippst Geraden oder Seiten an und gibst Ergebnisse ein — er zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze, dann Lösung aufklappen und abhaken.</li>
        </ol>
        <p>Taschenrechner erlaubt. Gerundete Ergebnisse auf zwei Dezimalen, Zwischenresultate ungerundet weiterverwenden.</p>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie — Taschenrechner erlaubt. Dieses Leitprogramm gehört zur Themenseite 5.2d:</p>
        <ul>
          <li><b>K3</b> die Ähnlichkeit für Berechnungen in der Ebene nutzen — Kapitel 1–4.</li>
          <li><b>K1</b> geometrische Sachverhalte von elementaren Objekten beschreiben — hier nur: ähnliche Dreiecke, Rechtecke, Quadrate und Kreise (Kapitel 3 und 4).</li>
          <li><b>K2</b> Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen — hier nur über den Streckfaktor: Abstände zum Zentrum (Kapitel 1 und 2), Umfang und Fläche ähnlicher Figuren (Kapitel 3).</li>
        </ul>
        <p class="rlp-quelle">Der Rest von K1 und K2 — Dreiecke, Vierecke, Kreis und Kreisteile mit ihren Elementen — steht auf den <a href="../grundlagen/g5-2a-dreiecke.html">Themenseiten 5.2a bis 5.2c</a> und in den Leitprogrammen <a href="dreiecke.html">Dreiecke</a>, <a href="vierecke.html">Vierecke</a> und <a href="kreis-kreisteile.html">Kreis und Kreisteile</a>.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Zentrische Streckung und Ähnlichkeit · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (Behebung 08.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 50 (+ 2f) · K3 40 · K4 50 (+ 4f, sWs/SsW in der Übung) · Gesamttest 30 = 220 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
