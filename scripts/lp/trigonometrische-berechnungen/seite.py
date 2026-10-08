"""Baut leitprogramme/trigonometrische-berechnungen.html aus einer Kapitelbeschreibung (07.10.2026).

  python3 scripts/lp/trigonometrische-berechnungen/seite.py

Leitprogramm zum Teilgebiet GF 5.3 Trigonometrische Berechnungen (Themenseite g5-3), im Kapitelmuster und mit
dem Geometrie-Arbeitsbereich des Leitprogramms Planimetrie. Liest Kopf (inkl. <style>) und Grundskript aus der
bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf
kommt das Gerüst aus leitprogramme/planimetrie.html. Wiederholbar. Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/trigonometrische-berechnungen.html'
NAME = 'Trigonometrische Berechnungen'
SCHLUESSEL = 'lp-trigonometrische-berechnungen-'
MARKE_CSS = '\n/* ════════ Trigonometrische Berechnungen'
MARKE_JS = '<script>\n/* Leitprogramm Trigonometrische Berechnungen —'
# Unverlinkt bis zur Freischaltung (HOWTO-leitprogramme §13/§15): build-seo.py schreibt den Block neu,
# sobald die Seite dort eingetragen ist (bis zur Freischaltung mit noindex=True).
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
kopf = kopf.rstrip('\n') + '\n\n'                            # sonst kommt bei jedem Lauf eine Leerzeile dazu
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Planimetrie —'), alt.find(MARKE_JS)) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Planimetrie', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 7. Oktober 2026', fuss)

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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 5.3 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TS = '../grundlagen/g5-3-trigonometrische-berechnungen.html'


def fig(daten, fenster, breite=220, hoehe=150):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}" '
            f'data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


def ecken(*e):
    return [['p', p] for p, _, _, _ in e] + [['t', p, n, 'ecke', dx, dy] for p, n, dx, dy in e]


# ------------------------------------------------------------------ Kapitel 1
sim1 = bereich(1, 'Rechtwinkliges Dreieck ABC mit dem Winkel x und der Hypotenuse H',
               regler('s1', 'x', 'Winkel x', 15, 75, 5, 35, 'orange', '°') + '\n          '
               + regler('s1', 'H', 'Hypotenuse H', 4, 10, 0.5, 10, einheit=' cm'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sinus, Cosinus und Tangens</div>
          <p>Im rechtwinkligen Dreieck benennt man die Seiten <b>vom betrachteten spitzen Winkel \(x\) aus</b>: Die <b>Hypotenuse</b> \(H\) liegt dem rechten Winkel gegenüber (die längste Seite), die <b>Gegenkathete</b> \(GK\) liegt \(x\) gegenüber, die <b>Ankathete</b> \(AK\) liegt an \(x\) an.</p>
          <p>\[ \sin x = \frac{GK}{H} \qquad \cos x = \frac{AK}{H} \qquad \tan x = \frac{GK}{AK} \]</p>
          <p>Alle rechtwinkligen Dreiecke mit demselben Winkel \(x\) sind ähnlich: Die Verhältnisse hängen nur von \(x\) ab, nicht von der Grösse des Dreiecks.</p>
          <p><b>Seite berechnen:</b> Seiten vom Winkel aus benennen → die Funktion wählen, die gegebene und gesuchte Seite verbindet → umstellen. Steht die gesuchte Seite oben im Bruch, wird multipliziert (\(GK = H \cdot \sin x\)), steht sie unten, wird geteilt (\(H = \tfrac{AK}{\cos x}\)).</p>
          <p>Im Standarddreieck mit dem rechten Winkel bei \(C\): \(\sin\alpha = \tfrac{a}{c}\), \(\cos\alpha = \tfrac{b}{c}\), \(\tan\alpha = \tfrac{a}{b}\). Liegt der Winkel bei \(B\), tauschen Gegen- und Ankathete die Rollen. Rechner im Gradmodus (DEG).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Gegen- und Ankathete vom falschen Winkel aus benennen.</p>
          <p>Multiplizieren statt teilen: Die Hypotenuse ist die längste Seite. Ist dein \(H\) kürzer als eine Kathete, hast du falsch umgestellt.</p>
          <p>Rechner im Bogenmass (RAD): \(\sin 40\) gibt dann \(0.745\) statt \(\sin 40° \approx 0.643\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 2, r'Im Bild liegt der rechte Winkel bei \(R\). Benenne Gegenkathete, Ankathete und Hypotenuse des Winkels \(\varphi\) bei \(P\). Welche Rolle hat die Seite \(PR\) für den Winkel bei \(Q\)?',
     r'<p>Von \(\varphi\) aus: \(GK = QR\), \(AK = PR\), \(H = PQ\). Für den Winkel bei \(Q\) liegt \(PR\) gegenüber: Sie ist dort die Gegenkathete.</p>',
     fig([['v', [[0, 0], [5, 0], [0, 3]]], ['r', [0, 0], [1, 0], [0, 1]], ['w', [5, 0], [0, 3], [0, 0], 'φ', 26]] + ecken(([0, 0], 'R', -9, 13), ([5, 0], 'P', 9, 13), ([0, 3], 'Q', -9, -4)), '-1.2,6.5,-0.9', 220, 140)),
    ('1b', 3, r'Rechtwinkliges Dreieck mit \(\gamma = 90°\), \(\alpha = 28°\) und \(c = 15\,\text{cm}\). Berechne \(a\) und \(b\) und mach die Probe mit Pythagoras.',
     r'<p>\(a = 15 \cdot \sin 28° \approx 7.04\,\text{cm}\); \(b = 15 \cdot \cos 28° \approx 13.24\,\text{cm}\). Probe: \(7.04^2 + 13.24^2 \approx 225 = 15^2\).</p>', ''),
    ('1c', 3, r'Rechtwinkliges Dreieck mit \(\gamma = 90°\), \(\beta = 62°\) und \(a = 9\,\text{cm}\). Berechne \(c\) und \(b\).',
     r'<p>Von \(\beta\) aus ist \(a\) die Ankathete und \(b\) die Gegenkathete. \(c = \tfrac{9}{\cos 62°} \approx 19.17\,\text{cm}\); \(b = 9 \cdot \tan 62° \approx 16.93\,\text{cm}\).</p><p class="komm">Wer \(a\) als Gegenkathete nimmt, hat die Seiten vom Winkel \(\alpha\) aus benannt.</p>', ''),
    ('1d', 2, r'Warum hängt \(\sin x\) nur vom Winkel \(x\) ab und nicht von der Grösse des Dreiecks?',
     r'<p>Alle rechtwinkligen Dreiecke mit demselben Winkel \(x\) haben dieselben Winkel, sind also ähnlich. Ihre Seiten sind mit demselben Faktor gestreckt; der Bruch \(\tfrac{GK}{H}\) bleibt gleich.</p>', ''),
    ('1e', 2, r'Was ist an dieser Lösung falsch? «\(x = 50°\), \(GK = 6\,\text{cm}\), gesucht \(H\): \(H = 6 \cdot \sin 50° \approx 4.60\,\text{cm}\).» Rechne richtig.',
     r'<p>Die Hypotenuse kann nicht kürzer sein als die Gegenkathete. Aus \(\sin x = \tfrac{GK}{H}\) folgt \(H = \tfrac{6}{\sin 50°} \approx 7.83\,\text{cm}\) — teilen, nicht multiplizieren.</p>', ''),
])
k1 = kapitel(1, 'sin-cos-tan', 'Sinus, Cosinus und Tangens', 40,
             r'Du benennst die Seiten eines rechtwinkligen Dreiecks vom Winkel aus, kennst Sinus, Cosinus und Tangens als Seitenverhältnisse und berechnest damit eine fehlende Seite.',
             ('g5-3-lp-seiten', 'Sinus, Cosinus und Tangens'), sim1, ('g5-3-lp-kontrolle-seiten', 'Kontrollfragen zu Sinus, Cosinus und Tangens'),
             fest1, [uebung('benennen', 'Seiten benennen', 'Rechtwinkliges Dreieck mit markiertem Winkel'), uebung('seite-rw', 'Seite berechnen')],
             auf1, f'<a href="{TS}#definition">Themenseite 5.3, Definition</a> und <a href="{TS}#recht-dreieck">Ähnlichkeit</a>', komp='K1 rechtwinklig')

# ------------------------------------------------------------------ Kapitel 2
sim2 = bereich(2, 'Rechtwinkliges Dreieck mit veränderbarer Gegenkathete und Ankathete',
               regler('s2', 'gk', 'Gegenkathete GK', 1, 8, 0.5, 5, einheit=' cm') + '\n          '
               + regler('s2', 'ak', 'Ankathete AK', 2, 12, 0.5, 12, einheit=' cm'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Winkel berechnen</div>
          <p>Ist das Verhältnis bekannt, liefert die <b>Umkehrung</b> den Winkel — die Arcusfunktionen, auf dem Rechner \(\sin^{-1}\), \(\cos^{-1}\), \(\tan^{-1}\) (im Gradmodus DEG):</p>
          <p>\[ x = \arcsin\frac{GK}{H} \qquad x = \arccos\frac{AK}{H} \qquad x = \arctan\frac{GK}{AK} \]</p>
          <p>Hoch minus eins heisst hier <b>Umkehrung</b>, nicht Kehrwert. Probe: \(\tan(\arctan v) = v\). Der andere spitze Winkel ist \(90° - x\).</p>
          <p><b>Steigung</b> = Höhe : waagrechte Strecke \(= \tan x\); in Prozent mal \(100\). Aus \(8\,\%\) wird \(\tan x = 0.08\), also \(x \approx 4.57°\).</p>
          <p>Im rechtwinkligen Dreieck liefert der Rechner genau den gesuchten spitzen Winkel. Dass \(\sin^{-1}\) sonst nur einen von mehreren Winkeln zeigt, kommt im Sinussatz (Kapitel 4) und im Teilgebiet 5.4.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Das Verhältnis als Winkel stehen lassen: \(\tan x \approx 0.417\) ist noch nicht \(x\).</p>
          <p>Prozent mit Grad verwechseln: \(12\,\%\) Steigung sind \(\tan x = 0.12\), nicht \(12°\).</p>
          <p>\(\tan^{-1}\) als Kehrwert \(\tfrac{1}{\tan}\) lesen.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Rechtwinkliges Dreieck mit \(\gamma = 90°\), \(a = 9\,\text{cm}\) und \(b = 14\,\text{cm}\). Berechne \(\alpha\), \(\beta\) und \(c\).',
     r'<p>\(\tan\alpha = \tfrac{9}{14}\), \(\alpha = \arctan\tfrac{9}{14} \approx 32.74°\); \(\beta = 90° - \alpha \approx 57.26°\); \(c = \sqrt{9^2 + 14^2} = \sqrt{277} \approx 16.64\,\text{cm}\).</p>',
     fig([['v', [[0, 0], [7, 0], [0, 4.5]]], ['r', [0, 0], [1, 0], [0, 1]], ['w', [7, 0], [0, 4.5], [0, 0], 'α', 26], ['w', [0, 4.5], [0, 0], [7, 0], 'β', 22]]
         + ecken(([0, 0], 'C', -9, 13), ([7, 0], 'A', 9, 13), ([0, 4.5], 'B', -9, -4)) + [['t', [3.5, 0], 'b = 14 cm', 'mass', 0, 15], ['t', [0, 2.25], 'a = 9 cm', 'mass', -6, 4, 'end']],
         '-3.2,8.2,-1', 220, 140)),
    ('2b', 2, r'Im rechtwinkligen Dreieck ist die Hypotenuse \(9.5\,\text{cm}\) und die Gegenkathete von \(x\) \(4\,\text{cm}\) lang. Wie gross ist \(x\)?',
     r'<p>\(\sin x = \tfrac{4}{9.5}\), \(x = \arcsin\tfrac{4}{9.5} \approx 24.90°\).</p>', ''),
    ('2c', 3, r'Eine Bergbahn überwindet auf \(800\,\text{m}\) waagrechter Strecke \(300\,\text{m}\) Höhe. Wie viel Prozent Steigung sind das, wie gross ist der Steigungswinkel, und wie lang ist die Strecke entlang der Bahn?',
     r'<p>Steigung \(\tfrac{300}{800} = 0.375 = 37.5\,\%\); \(x = \arctan 0.375 \approx 20.56°\); Strecke \(\sqrt{800^2 + 300^2} \approx 854.40\,\text{m}\) (oder \(\tfrac{800}{\cos x}\)).</p>', ''),
    ('2d', 2, r'Warum ist \(\sin^{-1}(0.6)\) nicht dasselbe wie \(\tfrac{1}{\sin(0.6°)}\)?',
     r'<p>\(\sin^{-1}(0.6)\) ist der Winkel, dessen Sinus \(0.6\) ist: \(\approx 36.87°\). \(\tfrac{1}{\sin(0.6°)} \approx 95.49\) ist der Kehrwert eines Sinuswerts — eine Zahl, kein Winkel.</p>', ''),
    ('2e', 2, r'Warum gibt es im rechtwinkligen Dreieck keinen Winkel mit \(\sin x = 1.2\)?',
     r'<p>\(\sin x = \tfrac{GK}{H}\), und die Gegenkathete ist kürzer als die Hypotenuse. Der Bruch ist darum kleiner als \(1\). (Der Rechner meldet einen Fehler.)</p>', ''),
])
k2 = kapitel(2, 'winkel', 'Winkel berechnen', 35,
             r'Du berechnest aus zwei Seiten eines rechtwinkligen Dreiecks den Winkel mit der Umkehrung (\(\arcsin\), \(\arccos\), \(\arctan\)) und rechnest Steigungen in Winkel um.',
             ('g5-3-lp-winkel', 'Den Winkel zurückrechnen'), sim2, ('g5-3-lp-kontrolle-winkel', 'Kontrollfragen zum Winkel'),
             fest2, [uebung('winkel-rw', 'Winkel berechnen'), uebung('steigung', 'Steigung und Winkel')],
             auf2, f'<a href="{TS}#arcus">Themenseite 5.3, Winkel berechnen — Arcusfunktionen</a>', komp='K1 rechtwinklig')

# ------------------------------------------------------------------ Kapitel 3
sim3 = bereich(3, 'Baum im Abstand d, Sehstrahl zur Spitze unter dem Höhenwinkel alpha',
               regler('s3', 'd', 'Abstand d', 5, 20, 0.5, 15, einheit=' m') + '\n          '
               + regler('s3', 'alpha', 'Höhenwinkel α', 15, 55, 1, 52, 'orange', '°'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Höhen und Distanzen</div>
          <p><b>Vorgehen:</b> Skizze → rechtwinkliges Dreieck suchen → Seiten vom Winkel aus benennen → Funktion wählen und rechnen → prüfen (Grössenordnung, Einheit).</p>
          <p>Der <b>Höhenwinkel</b> wird von der Waagrechten nach oben gemessen, der <b>Tiefenwinkel</b> von der Waagrechten nach unten. Der Tiefenwinkel, unter dem du von oben ein Ziel siehst, ist gleich gross wie der Höhenwinkel, unter dem man vom Ziel aus zu dir hinaufschaut (Wechselwinkel an den beiden Waagrechten).</p>
          <p>Baum: \(h = d \cdot \tan\alpha\). Bei \(d = 15\,\text{m}\) und \(\alpha = 52°\) ist \(h \approx 19.20\,\text{m}\). Misst du mit dem Auge, kommt die Augenhöhe dazu.</p>
          <p><b>Plausibel?</b> Bei \(\alpha \lt 45°\) ist \(h \lt d\), bei \(\alpha \gt 45°\) ist \(h \gt d\).</p>
          <p><b>Fuss unerreichbar:</b> Zwei Höhenwinkel \(\alpha\) und \(\beta\) von zwei Standorten im Abstand \(s\) geben zwei Gleichungen: \(\tan\beta = \tfrac{h}{d}\) und \(\tan\alpha = \tfrac{h}{d + s}\). Setze \(h = d \cdot \tan\beta\) in die zweite ein und löse nach \(d\) auf.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Abstand am Boden als Hypotenuse nehmen — er ist die Ankathete.</p>
          <p>Die Augenhöhe vergessen, wenn die Aufgabe sie nennt.</p>
          <p>Den Tiefenwinkel gegen die Senkrechte messen statt gegen die Waagrechte.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Eine \(6\,\text{m}\) lange Leiter lehnt an einer Wand und bildet mit dem Boden \(70°\). Skizziere. Wie hoch reicht sie, und wie weit steht ihr Fuss von der Wand?',
     r'<p>Die Leiter ist die Hypotenuse. Höhe \(6 \cdot \sin 70° \approx 5.64\,\text{m}\); Abstand \(6 \cdot \cos 70° \approx 2.05\,\text{m}\).</p>', ''),
    ('3b', 3, r'Von einem \(45\,\text{m}\) hohen Leuchtturm siehst du ein Boot unter dem Tiefenwinkel \(12°\). Wie weit ist das Boot vom Fuss des Turms entfernt?',
     r'<p>Am Boot ist der Höhenwinkel ebenfalls \(12°\) (Wechselwinkel). \(\tan 12° = \tfrac{45}{d}\), also \(d = \tfrac{45}{\tan 12°} \approx 211.71\,\text{m}\).</p><p class="komm">Wer \(45 \cdot \tan 12°\) rechnet, hat Gegen- und Ankathete vertauscht.</p>', ''),
    ('3c', 4, r'Der Fuss eines Bergs ist unerreichbar. Von \(A\) aus siehst du die Spitze unter \(25°\), von \(B\) aus, \(120\,\text{m}\) näher, unter \(38°\). Wie hoch ist der Berg über der Beobachtungsebene?',
     r'<p>\(h = d \cdot \tan 38°\) und \(h = (d + 120) \cdot \tan 25°\). Gleichsetzen: \(d\,(\tan 38° - \tan 25°) = 120 \cdot \tan 25°\), also \(d \approx 177.65\,\text{m}\) und \(h = d \cdot \tan 38° \approx 138.80\,\text{m}\).</p>',
     fig([['s', [-1, 0], [10.5, 0], 'boden'], ['s', [10, 0], [10, 4.66], 'baum'], ['s', [0, 0], [10, 4.66], 'hilfe2'], ['s', [4.03, 0], [10, 4.66], 'hilfe2'],
          ['w', [0, 0], [10, 0], [10, 4.66], '25°', 34], ['w', [4.03, 0], [10, 0], [10, 4.66], '38°', 26], ['p', [0, 0]], ['p', [4.03, 0]],
          ['t', [0, 0], 'A', 'ecke', -2, 14], ['t', [4.03, 0], 'B', 'ecke', 0, 14], ['t', [2.01, 0], '120 m', 'mass', 0, 26], ['t', [10, 2.33], 'h', 'seite', 8, 4, 'start']],
         '-1.2,11.5,-1.6', 260, 150)),
    ('3d', 2, r'Warum braucht es beim Berg mit unerreichbarem Fuss zwei Messungen?',
     r'<p>Unbekannt sind die Höhe \(h\) und der Abstand \(d\) zum Fuss. Eine Messung gibt nur eine Gleichung \(\tan\alpha = \tfrac{h}{d}\); für zwei Unbekannte braucht es zwei Gleichungen.</p>', ''),
    ('3e', 2, r'Jemand berechnet für einen Turm in \(30\,\text{m}\) Abstand bei einem Höhenwinkel von \(20°\) eine Höhe von \(82.42\,\text{m}\). Woran siehst du ohne Rechnen, dass das nicht stimmt? Was wurde falsch gerechnet?',
     r'<p>Bei \(\alpha \lt 45°\) ist der Turm niedriger, als man entfernt steht: \(h \lt 30\,\text{m}\). Gerechnet wurde \(\tfrac{30}{\tan 20°}\); richtig ist \(30 \cdot \tan 20° \approx 10.92\,\text{m}\).</p>', ''),
])
k3 = kapitel(3, 'anwendungen', 'Höhen und Distanzen', 40,
             r'Du übersetzt eine Sachaufgabe in eine Skizze, findest das rechtwinklige Dreieck mit Höhen- oder Tiefenwinkel, berechnest Höhen und Distanzen und prüfst das Ergebnis auf Plausibilität.',
             ('g5-3-lp-hoehen', 'Höhen und Distanzen'), sim3, ('g5-3-lp-kontrolle-hoehen', 'Kontrollfragen zu Höhen und Distanzen'),
             fest3, [uebung('hoehe', 'Höhenwinkel'), uebung('leiter-tiefe', 'Leiter, Schnur, Tiefenwinkel')],
             auf3, f'<a href="{TS}#einstieg">Themenseite 5.3, Einstieg (Baumhöhe)</a> und <a href="{TS}#aufgaben">Aufgaben A5</a>', komp='K1 rechtwinklig')

# ------------------------------------------------------------------ Kapitel 4
sim4 = bereich(4, 'Winkel alpha = 35 Grad bei A, Seite c = 6, Kreis um B mit Radius a',
               regler('s4', 'a', 'Seite a', 2, 9, 0.5, 4.5))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sinussatz</div>
          <p>Im allgemeinen Dreieck liegt die Seite \(a\) der Ecke \(A\) gegenüber, \(\alpha\) liegt bei \(A\) (ebenso \(b\), \(\beta\) und \(c\), \(\gamma\)); \(\alpha + \beta + \gamma = 180°\).</p>
          <p>Die Höhe von \(C\) auf \(c\) ist \(h_c = b \cdot \sin\alpha = a \cdot \sin\beta\). Daraus folgt der <b>Sinussatz</b>:</p>
          <p>\[ \frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma} \]</p>
          <p>Über dem Bruchstrich die Seite, darunter der Sinus ihres <b>Gegenwinkels</b>. Er braucht ein vollständiges <b>Paar</b> aus Seite und Gegenwinkel und eine weitere Angabe: zwei Winkel und eine Seite (WSW, WWS; zuerst den dritten Winkel) oder zwei Seiten und den Gegenwinkel einer davon (SSW).</p>
          <p><b>SSW:</b> Der Rechner liefert nur den spitzen Winkel \(\gamma_1\). Auch \(\gamma_2 = 180° - \gamma_1\) hat denselben Sinus (\(\sin(180° - \gamma) = \sin\gamma\); warum, zeigt der Einheitskreis in 5.4). \(\gamma_2\) gibt ein zweites Dreieck, wenn \(\alpha + \gamma_2 \lt 180°\). Bei <b>spitzem</b> \(\alpha\) entscheidet die Höhe von \(B\) auf den Schenkel von \(\alpha\), \(h = c \cdot \sin\alpha\): \(a \lt h\) kein Dreieck, \(a = h\) eines (rechtwinklig), \(h \lt a \lt c\) zwei, \(a \geq c\) eines. Bei stumpfem oder rechtem \(\alpha\) ist die Gegenseite die längste: \(a \gt c\) eines, sonst keines.</p>
          <p>Der Rechner kennt Sinus und Cosinus auch für stumpfe Winkel. Die Themenseite begründet den Sinussatz zusätzlich über den Umkreis: Jeder Quotient ist der Durchmesser \(2r\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Seite und Winkel falsch paaren: Zu \(a\) gehört \(\alpha\), der Winkel <b>gegenüber</b>.</p>
          <p>Bei SSW nur den Rechnerwert nehmen und das zweite Dreieck übersehen — oder umgekehrt einen stumpfen Kandidaten behalten, der mit \(\alpha\) zusammen über \(180°\) kommt.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Ein Punkt \(P\) am anderen Flussufer wird von \(A\) und \(B\) aus angepeilt. \(\overline{AB} = 120\,\text{m}\), \(\angle PAB = 58°\), \(\angle PBA = 75°\). Wie weit ist \(P\) von \(A\) und von \(B\) entfernt?',
     r'<p>Winkel bei \(P\): \(180° - 58° - 75° = 47°\). \(\overline{AP} = \tfrac{120 \cdot \sin 75°}{\sin 47°} \approx 158.49\,\text{m}\); \(\overline{BP} = \tfrac{120 \cdot \sin 58°}{\sin 47°} \approx 139.15\,\text{m}\).</p><p class="komm">\(\overline{AP}\) liegt dem Winkel bei \(B\) gegenüber — darum \(\sin 75°\).</p>',
     fig([['v', [[0, 0], [6, 0], [4.2, 6.72]]], ['w', [0, 0], [6, 0], [4.2, 6.72], '58°', 22], ['w', [6, 0], [4.2, 6.72], [0, 0], '75°', 22]]
         + ecken(([0, 0], 'A', -9, 13), ([6, 0], 'B', 9, 13), ([4.2, 6.72], 'P', 0, -8)) + [['t', [3, 0], '120 m', 'mass', 0, 15]], '-1,7.5,-1', 190, 190)),
    ('4b', 3, r'Dreieck mit \(\alpha = 40°\), \(\beta = 65°\) und \(a = 8\,\text{cm}\). Berechne \(\gamma\), \(b\) und \(c\).',
     r'<p>\(\gamma = 75°\); \(b = \tfrac{8 \cdot \sin 65°}{\sin 40°} \approx 11.28\,\text{cm}\); \(c = \tfrac{8 \cdot \sin 75°}{\sin 40°} \approx 12.02\,\text{cm}\).</p>', ''),
    ('4c', 4, r'Dreieck mit \(a = 6\,\text{cm}\), \(c = 9\,\text{cm}\) und \(\alpha = 34°\). Wie viele Dreiecke gibt es? Berechne alle möglichen Winkel \(\gamma\) und je die Seite \(b\).',
     r'<p>\(\sin\gamma = \tfrac{9 \cdot \sin 34°}{6} \approx 0.8388\): \(\gamma_1 \approx 57.01°\), \(\gamma_2 = 180° - \gamma_1 \approx 122.99°\). Beide passen (\(34° + 122.99° \lt 180°\)): zwei Dreiecke. Dann \(\beta_1 \approx 88.99°\), \(b_1 = \tfrac{6 \cdot \sin\beta_1}{\sin 34°} \approx 10.73\,\text{cm}\); \(\beta_2 \approx 23.01°\), \(b_2 \approx 4.19\,\text{cm}\).</p><p class="komm">Kontrolle mit der Höhe: \(h = 9 \cdot \sin 34° \approx 5.03 \lt 6 \lt 9\) — zwei Dreiecke.</p>', ''),
    ('4d', 2, r'Warum braucht der Sinussatz ein vollständiges Paar aus einer Seite und ihrem Gegenwinkel?',
     r'<p>Er setzt zwei Brüche «Seite durch Sinus des Gegenwinkels» gleich. Ist kein Bruch vollständig bekannt, enthält jede Gleichung zwei Unbekannte.</p>', ''),
    ('4e', 2, r'Fest sind \(\alpha = 40°\) und \(c = 10\,\text{cm}\) (Bild). Für welche Längen der Gegenseite \(a\) gibt es zwei Dreiecke?',
     r'<p>Höhe \(h = 10 \cdot \sin 40° \approx 6.43\,\text{cm}\). Zwei Dreiecke für \(6.43\,\text{cm} \lt a \lt 10\,\text{cm}\).</p>',
     fig([['s', [0, 0], [9.2, 7.72], 'strahl'], ['s', [0, 0], [10, 0], 'figur-linie'], ['w', [0, 0], [10, 0], [9.2, 7.72], '40°', 26]]
         + ecken(([0, 0], 'A', -9, 13), ([10, 0], 'B', 9, 13)) + [['t', [5, 0], 'c = 10 cm', 'mass', 0, 15]], '-1,11.5,-1.3', 230, 190)),
])
k4 = kapitel(4, 'sinussatz', 'Der Sinussatz', 45,
             r'Du wendest den Sinussatz im allgemeinen Dreieck an, wenn zwei Winkel und eine Seite oder zwei Seiten und ein Gegenwinkel gegeben sind, und entscheidest im Fall SSW, ob es kein, ein oder zwei Dreiecke gibt.',
             ('g5-3-lp-sinussatz', 'Der Sinussatz'), sim4, ('g5-3-lp-kontrolle-sinussatz', 'Kontrollfragen zum Sinussatz'),
             fest4, [uebung('sinussatz', 'Sinussatz: Seite berechnen'), uebung('ssw', 'SSW: wie viele Dreiecke?')],
             auf4, f'<a href="{TS}#sinussatz">Themenseite 5.3, Sinussatz</a> (mit der Animation zum Fall SSW)', komp='K1 allgemein')

# ------------------------------------------------------------------ Kapitel 5
sim5 = bereich(5, 'Dreieck ABC mit den Seiten b und c und dem Zwischenwinkel alpha',
               regler('s5', 'b', 'Seite b', 3, 8, 0.5, 7) + '\n          ' + regler('s5', 'c', 'Seite c', 3, 10, 0.5, 10)
               + '\n          ' + regler('s5', 'alpha', 'Winkel α', 20, 150, 5, 55, 'orange', '°'))
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Cosinussatz und Dreiecksfläche</div>
          <p>Ohne Paar aus Seite und Gegenwinkel — zwei Seiten und der Winkel dazwischen (SWS) oder drei Seiten (SSS) — hilft der <b>Cosinussatz</b>:</p>
          <p>\[ a^2 = b^2 + c^2 - 2bc \cdot \cos\alpha \]</p>
          <p>ebenso \(b^2 = a^2 + c^2 - 2ac \cdot \cos\beta\) und \(c^2 = a^2 + b^2 - 2ab \cdot \cos\gamma\). Links die gesuchte Seite, im Cosinus ihr Gegenwinkel. Bei \(\alpha = 90°\) ist \(\cos\alpha = 0\): der Satz des Pythagoras. Bei stumpfem \(\alpha\) ist \(\cos\alpha \lt 0\), und \(a\) wird länger als beim rechten Winkel.</p>
          <p><b>Drei Seiten:</b> \(\cos\alpha = \tfrac{b^2 + c^2 - a^2}{2bc}\), dann \(\arccos\). Ein negativer Cosinus heisst: \(\alpha\) ist stumpf — das ist genau dann so, wenn \(a^2 \gt b^2 + c^2\).</p>
          <p><b>Fläche</b> aus zwei Seiten und dem Winkel dazwischen: Die Höhe auf \(c\) ist \(h = b \cdot \sin\alpha\), also \(A = \tfrac{b \cdot c}{2} \cdot \sin\alpha\). Die Themenseite schreibt allgemein \(A = \tfrac{p \cdot q}{2}\sin\varphi\).</p>
          <p><b>Welcher Satz?</b> Paar aus Seite und Gegenwinkel vorhanden: Sinussatz. Kein Paar: Cosinussatz — danach ist oft ein Paar vollständig, und der Rest geht mit dem Sinussatz.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Das Korrekturglied \(-2bc \cdot \cos\alpha\) vergessen oder mit falschem Vorzeichen rechnen; die Wurzel am Schluss vergessen.</p>
          <p>Einen negativen Cosinus für einen Rechenfehler halten: Er zeigt einen stumpfen Winkel.</p>
          <p>Für die Fläche einen Winkel nehmen, der nicht zwischen den beiden Seiten liegt.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 3, r'Von einer Weggabelung führen zwei gerade Wege weg, \(4.2\,\text{km}\) und \(3.5\,\text{km}\) lang, unter dem Winkel \(48°\). Wie weit liegen die beiden Wegenden auseinander?',
     r'<p>SWS: \(d^2 = 4.2^2 + 3.5^2 - 2 \cdot 4.2 \cdot 3.5 \cdot \cos 48° \approx 10.22\), \(d \approx 3.20\,\text{km}\).</p>', ''),
    ('5b', 4, r'Dreieck mit \(a = 7\), \(b = 9\), \(c = 12\). Wie gross ist der grösste Winkel? Ist er spitz oder stumpf? Begründe es zusätzlich ohne den Winkel, mit einem Vergleich von \(c^2\) und \(a^2 + b^2\).',
     r'<p>Er liegt der längsten Seite \(c\) gegenüber: \(\cos\gamma = \tfrac{49 + 81 - 144}{2 \cdot 7 \cdot 9} = -\tfrac{14}{126} \approx -0.1111\), \(\gamma \approx 96.38°\) — stumpf, weil der Cosinus negativ ist.</p><p>Ohne Winkel: \(c^2 = 144 \gt a^2 + b^2 = 130\). Die Seite gegenüber \(\gamma\) ist länger als beim rechten Winkel (dort wäre \(c^2 = a^2 + b^2\)), also ist \(\gamma\) stumpf.</p>', ''),
    ('5c', 3, r'Ein dreieckiges Grundstück hat zwei Seiten von \(32\,\text{m}\) und \(45\,\text{m}\), die einen Winkel von \(110°\) einschliessen. Wie gross ist es?',
     r'<p>\(A = \tfrac{32 \cdot 45}{2} \cdot \sin 110° \approx 676.58\,\text{m}^2\).</p>',
     fig([['v', [[0, 0], [9, 0], [-2.19, 6.01]]], ['w', [0, 0], [9, 0], [-2.19, 6.01], '110°', 18], ['t', [4.5, 0], '45 m', 'mass', 0, 14], ['t', [-1.1, 3], '32 m', 'mass', -6, 0, 'end']],
         '-4.5,10,-1.2', 220, 135)),
    ('5d', 2, r'Warum wird der Cosinussatz \(c^2 = a^2 + b^2 - 2ab \cdot \cos\gamma\) bei \(\gamma = 90°\) zum Satz des Pythagoras?',
     r'<p>Weil \(\cos 90° = 0\) ist: Das Korrekturglied \(-2ab \cdot \cos\gamma\) fällt weg, es bleibt \(c^2 = a^2 + b^2\) mit der Hypotenuse \(c\) gegenüber dem rechten Winkel.</p>', ''),
    ('5e', 2, r'Mit welchem Satz beginnst du? (a) \(a\), \(b\), \(\gamma\) · (b) \(\alpha\), \(\beta\), \(c\) · (c) \(a\), \(b\), \(c\) · (d) \(a\), \(b\), \(\beta\). Begründe kurz.',
     r'<p>(a) Cosinussatz — \(\gamma\) liegt zwischen \(a\) und \(b\), kein Paar. (b) Sinussatz — zuerst \(\gamma\), dann ist \(c\), \(\gamma\) ein Paar. (c) Cosinussatz — kein Winkel bekannt. (d) Sinussatz — \(b\), \(\beta\) ist ein Paar (SSW: an die zweite Lösung denken).</p>', ''),
])
k5 = kapitel(5, 'cosinussatz', 'Cosinussatz und Dreiecksfläche', 45,
             r'Du berechnest mit dem Cosinussatz eine Seite (zwei Seiten und Zwischenwinkel) oder einen Winkel (drei Seiten), berechnest die Fläche aus zwei Seiten und dem Zwischenwinkel und wählst den passenden Satz.',
             ('g5-3-lp-cosinussatz', 'Cosinussatz und Fläche'), sim5, ('g5-3-lp-kontrolle-cosinussatz', 'Kontrollfragen zu Cosinussatz und Fläche'),
             fest5, [uebung('cosinussatz', 'Cosinussatz'), uebung('flaeche', 'Dreiecksfläche'), uebung('welcher-satz', 'Welcher Satz?')],
             auf5, f'<a href="{TS}#cosinussatz">Themenseite 5.3, Cosinussatz</a>, <a href="{TS}#strategie">Welcher Satz wann?</a> und <a href="{TS}#dreiecksflaeche">Dreiecksfläche</a>', komp='K1 allgemein')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 5.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Satz des Pythagoras, ähnliche Dreiecke, Winkelsumme, Beschriftung und einfache Verhältnisgleichungen. Wenn das wackelt: Leitprogramme <a href="dreiecke.html">Dreiecke</a>, <a href="vierecke.html">Vierecke</a> und <a href="aehnlichkeit.html">Zentrische Streckung und Ähnlichkeit</a>.</p>
      ''' + clipkarte('g5-2a-pythagoras', 'Der Satz des Pythagoras') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Rechtwinkliges Dreieck: (a) Katheten \(9\,\text{cm}\) und \(12\,\text{cm}\) — Hypotenuse? (b) Hypotenuse \(13\,\text{cm}\), eine Kathete \(5\,\text{cm}\) — andere Kathete?',
     r'<p>(a) \(\sqrt{81 + 144} = 15\,\text{cm}\). (b) \(\sqrt{169 - 25} = 12\,\text{cm}\).</p>', ''),
    ('0b', 2, r'Ein Dreieck mit den Seiten \(3\), \(4\) und \(5\,\text{cm}\) wird mit \(k = 2.5\) vergrössert. Wie lang sind die Bildseiten? Wie gross ist im Bild das Verhältnis der kürzesten zur längsten Seite?',
     r'<p>\(7.5\), \(10\), \(12.5\,\text{cm}\). \(\tfrac{7.5}{12.5} = 0.6 = \tfrac{3}{5}\) — dasselbe wie im Original.</p><p class="komm">Ähnliche Figuren haben dieselben Seitenverhältnisse: Darauf baut Kapitel 1.</p>', ''),
    ('0c', 2, r'(a) In einem rechtwinkligen Dreieck ist ein spitzer Winkel \(34°\). Wie gross ist der andere? (b) \(\alpha = 47°\), \(\beta = 68°\): \(\gamma = {?}\)',
     r'<p>(a) \(90° - 34° = 56°\). (b) \(180° - 47° - 68° = 65°\).</p>', ''),
    ('0d', 2, r'Löse: (a) \(\dfrac{x}{7} = 0.6\) (b) \(\dfrac{5}{x} = 0.4\)',
     r'<p>(a) \(x = 7 \cdot 0.6 = 4.2\). (b) \(x = \tfrac{5}{0.4} = 12.5\).</p><p class="komm">Steht \(x\) unten im Bruch, wird geteilt — genau das braucht Kapitel 1.</p>', ''),
    ('0e', 2, r'Im Dreieck \(ABC\): Welche Seite liegt der Ecke \(A\) gegenüber? Bei welcher Ecke liegt \(\beta\)?',
     r'<p>Die Seite \(a = \overline{BC}\); \(\beta\) liegt bei \(B\).</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen im Leitprogramm Planimetrie, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/trigonometrische-berechnungen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.3 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 2; G3 → 3; G4 (a) → 4, G4 (b) → 1; G5 → 4; G6, G7 → 5</p>
        </div>
      </div>
    </section>

    <section class="kap" id="weiter">
      <h2 id="weiter-titel">Weiter</h2>
      <p>Als Nächstes: <a href="einheitskreis.html">Leitprogramm Einheitskreis</a> (Teilgebiet 5.4) — Sinus und Cosinus für jeden Winkel, die besonderen Winkel ohne Rechner und warum \\(\\sin(180° - \\gamma) = \\sin\\gamma\\) gilt.</p>
      <p>Nicht in diesem Leitprogramm, sondern auf der <a href="{TS}">Themenseite 5.3</a>: die exakten Werte bei \\(30°\\), \\(45°\\), \\(60°\\) (<a href="{TS}#spezialwinkel">Spezialwinkel</a>, dazu Teilgebiet 5.4), die <a href="{TS}#beziehungen">Beziehungen unter den Winkelfunktionen</a>, die Herleitung des Sinussatzes über den Umkreis und das Eintippen von Grad, Minuten und Sekunden.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Trigonometrische Berechnungen, Version 1.0 (07.10.2026). Gebaut aus
     scripts/lp/trigonometrische-berechnungen/seite.py — Änderungen dort, nicht in dieser Datei. Grundlage:
     HOWTO-leitprogramme.md, Vorbild Planimetrie (Geometrie-Arbeitsbereich, ~/HOWTO-PlaniLP.md).

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.3 Trigonometrische Berechnungen, wörtlich (wie auf der Themenseite):
       K1  Berechnungen im rechtwinkligen und im allgemeinen Dreieck mithilfe der trigonometrischen Funktionen
           durchführen
     Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Die eine Kompetenz ist für die Zuordnung in
     zwei Teile gegliedert: K1 rechtwinklig (Kapitel 1–3), K1 allgemein (Kapitel 4–5).

     a) Kompetenzmatrix (Kompetenz | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 rechtwinklig | nein | 1, 2, 3 | 1a–1e, 2a–2e, 3a–3e | G1, G2, G3, G4 (Abstand)
       K1 allgemein    | nein | 4, 5    | 4a–4e, 5a–5e       | G4, G5, G6, G7

     b) Planungstabelle (Kapitel | Lernziel | Clips | Erkundung | Beispiel (Quelle) | Häufiger Fehler | min):
       0 Vorwissen   | Pythagoras, Ähnlichkeit, Winkelsumme, x/7 = 0.6 | g5-2a-pythagoras | — | — | — | 10
       1 sin/cos/tan | Seiten benennen, Verhältnisse, Seite berechnen | g5-3-lp-seiten, -kontrolle-seiten | sim1
         (H und x, Seiten antippen) | x = 35°, H = 10 (Themenseite, Anim 2) | GK/AK vertauscht, mal statt geteilt, RAD | 40
       2 Winkel      | arcsin/arccos/arctan, Steigung | g5-3-lp-winkel, -kontrolle-winkel | sim2 (GK, AK) |
         GK = 5, AK = 12 (Themenseite A3a) | Verhältnis statt Winkel, % als Grad, Kehrwert | 35
       3 Anwendungen | Skizze, Höhen-/Tiefenwinkel, Augenhöhe, zwei Standorte | g5-3-lp-hoehen, -kontrolle-hoehen |
         sim3 (d, α) | Baum 15 m, 52° (Themenseite, Einstieg) | d als Hypotenuse, Augenhöhe vergessen | 40
       4 Sinussatz   | Paar, WSW/WWS, SSW mit zwei Lösungen | g5-3-lp-sinussatz, -kontrolle-sinussatz | sim4 (a) |
         α = 42°, β = 71°, c = 9 (A4a); SSW α = 35°, c = 6, a = 4.5 (Anim SSW) | falsches Paar, 2. Lösung | 45
       5 Cosinussatz | SWS, SSS, Fläche, welcher Satz | g5-3-lp-cosinussatz, -kontrolle-cosinussatz | sim5 (b, c, α) |
         b = 7, c = 10, α = 55° (A4b) | Korrekturglied, Vorzeichen, negativer Cosinus | 45
       Gesamttest 30. Summe 245 min ≈ 5.4 Lektionen (fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest).

     c) Kern: alles oben. Bewusst weggelassen (→ Themenseite bzw. LP Einheitskreis 5.4): exakte Spezialwerte
        30°/45°/60° ohne Hilfsmittel und die Beziehungen sin α = cos(90° − α) (Kern von 5.4), Einheitskreis und
        Bogenmass, die Umkreis-Herleitung des Sinussatzes (2r), Grad/Minuten/Sekunden am Rechner.
        Vorgezogen und kurz erklärt (Kapitel 4/5): Der Rechner liefert sin und cos auch für stumpfe Winkel,
        sin(180° − γ) = sin γ und cos < 0 bei stumpfem Winkel — begründet erst in 5.4.

     d) Konventionen wie auf der Themenseite: rechter Winkel bei C, betrachteter Winkel x, Seiten GK, AK, H;
        a gegenüber A, α bei A; arcsin/arccos/arctan, Rechner sin⁻¹, cos⁻¹, tan⁻¹; Cosinus (nicht Kosinus);
        Fläche A = ½ b c sin α (Themenseite: A = (p·q)/2 sin φ, einmal genannt); Winkel in Grad, Ergebnisse auf
        zwei Dezimalen. Fälle gross geschrieben (WSW, WWS, SSW, SWS, SSS) wie auf 5.2a.
        Widersprüche der Themenseite (gemeldet, nicht übernommen): Fälle mal klein (wsw, ssw — Tipp, Strategie-
        Grafik), mal gross (SSW, WSW — Anim, Fehlerkasten, Zusammenfassung); Seitennamen GK/AK/H (Definition,
        Anim) gegen Geg/An/Hyp und SOH-CAH-TOA (Zusammenfassung) und GAGA/«HY» (Mini-Check, Clip
        welche-winkelfunktion); «Arcus» im Text gegen «Arkus» in den Clips; sin x gegen sin(α) mit Klammern;
        Cosinus stumpfer Winkel (cos 110°, arccos(−0.05)) wird benutzt, bevor er definiert ist (5.4);
        Merkkasten Dreiecksfläche nennt φ = 90° «Pythagoras-Spezialfall» (es ist der rechtwinklige Fall).

     Farben: Figur blau, betrachteter Winkel und gegebene Stücke orange, Gesuchtes und Ergebnis grün, Fehler rot.
     Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste → ③ Kontrollclip mit
     Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket
     nur als PDF aus LaTeX (downloads/leitprogramme/trigonometrische-berechnungen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Trigonometrische Berechnungen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.3</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Sinus, Cosinus, Tangens</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Winkel berechnen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Höhen und Distanzen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Sinussatz</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Cosinussatz, Fläche</span></a></li>
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
          <li><b>② Tüfteln:</b> Im Arbeitsbereich veränderst du die Figur, tippst Seiten oder Hilfslinien an und gibst Ergebnisse ein — er zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze, dann Lösung aufklappen und abhaken.</li>
        </ol>
        <p>Taschenrechner im Gradmodus (DEG). Längen und Winkel auf zwei Dezimalen runden, Zwischenresultate ungerundet weiterverwenden.</p>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.3 — Taschenrechner erlaubt:</p>
        <ul>
          <li><b>K1</b> Berechnungen im rechtwinkligen und im allgemeinen Dreieck mithilfe der trigonometrischen Funktionen durchführen — im rechtwinkligen Dreieck Kapitel 1–3, im allgemeinen Dreieck Kapitel 4–5. Winkel in Grad.</li>
        </ul>
        <p class="rlp-quelle">Nicht hier: Einheitskreis, besondere Winkel ohne Rechner und Bogenmass — <a href="einheitskreis.html">Leitprogramm Einheitskreis</a> (5.4); Spezialwinkel, Beziehungen und die Umkreis-Herleitung — <a href="''' + TS + '''">Themenseite 5.3</a>.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Trigonometrische Berechnungen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (07.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 35 · K3 40 · K4 45 · K5 45 · Gesamttest 30 = 245 min
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
