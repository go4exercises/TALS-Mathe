"""Erzeugt die acht Drehbücher des Leitprogramms Vierecke (08.10.2026).

  python3 scripts/lp/vierecke/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich); nur für Szenen mit
neuem Text muss danach build-clip-ton.py laufen (Teilvertonung mit --szenen). Bewegungen und `ein` nach der
Vertonung hier anpassen (Wortzeiten mit faster-whisper, siehe README) und das Skript erneut laufen lassen.

Aufbau wie in den Leitprogrammen Planimetrie und Trigonometrische Berechnungen: Rechnung und Notizen links (x 150),
die Figur rechts (x 1010, y 175, 760 × 760). Figuren zeichnet `graf` mit "figuren" und "achsen": false
(HOWTO-clips.md, «Figuren im Graf»). Das Fenster ist in x und y gleich geteilt, die Figuren sind massstäblich.

Fragebild (HOWTO-leitprogramme §15): Die Kontrollclips zeigen beim Erscheinen einer Frage nur das Gegebene;
Rechnung, Lösung und Hervorhebung erscheinen erst ab 1.0 s (nach der Antwort).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = die Figur                                                  \\fa{…}
  2 orange = Element: Höhe, Diagonale, Mittellinie, Symmetrieachse      \\fb{…}
  3 grün   = gesuchte Grösse, Ergebnis, Teildreieck, Fläche             \\fc{…}
  4 rot    = Fehler, abgeschnittenes Stück                              \\fd{…}
  5 Tinte  = neutral (Beschriftung, Bezugslinien)
Alle Zahlen und Koordinaten mit python3 nachgerechnet (zahlen.py und die Kommentare bei den Szenen).
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-2b-lp-'


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def richtung(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def mitte(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


# ---------------------------------------------------------------- Fenster und Figuren
def geo(x0, y0, span):
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], achsen=False)


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def ach(x0, y0, span, xt, yt_):
    """Mit Achsen (für Klickfragen: die Lage ist ablesbar), gleich geteilt."""
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], xteilung=yt(*xt), yteilung=yt(*yt_))


def V(pkte, farbe=1, fu=0.12, **kw):
    return dict(art='vieleck', punkte=[r3(p) for p in pkte], farbe=farbe, fuellung=fu, **kw)


def S(a, b, farbe=2, gest=False, dicke=4, **kw):
    d = dict(art='strecke', von=r3(a), bis=r3(b), farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=30, kursiv=True, **kw):
    return dict(art='text', bei=[round(x, 3), round(y, 3)], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=kursiv, **kw)


def RW(p, r1, r2, farbe=5, **kw):
    return dict(art='rechts', bei=r3(p), r1=round(r1, 2), r2=round(r2, 2), farbe=farbe, **kw)


def WI(p, a, b, farbe=2, r=40, **kw):
    """Innenwinkel bei p von der Richtung zu a bis zur Richtung zu b (der kleinere Bogen)."""
    w0, w1 = richtung(p, a), richtung(p, b)
    if (w1 - w0) % 360 > 180:
        w0, w1 = w1, w0
    if w1 < w0:
        w1 += 360
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def graf(W, figuren=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def pt(p, farbe=5, **kw):
    return dict(x=round(p[0], 3), y=round(p[1], 3), farbe=farbe, anker='start', **kw)


def ecken(P, namen, d=0.5, farbe=5, g=30, **kw):
    """Eckennamen vom Schwerpunkt weg (wie ecken() in seite.js)."""
    sx, sy = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    aus = []
    for p, nm in zip(P, namen):
        dx, dy = p[0] - sx, p[1] - sy
        L = math.hypot(dx, dy) or 1
        aus.append(T(p[0] + d * dx / L, p[1] + d * dy / L - 0.15, nm, farbe, g=g, kursiv=False, **kw))
    return aus


def seite(p, q, text, farbe=5, d=0.42, g=30, kursiv=True, **kw):
    """Beschriftung einer Seite p→q aussen (Ecken gegen den Uhrzeigersinn: aussen ist rechts der Laufrichtung)."""
    m = mitte(p, q)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    return T(m[0] + d * dy / L, m[1] - d * dx / L - 0.15, text, farbe, g=g, kursiv=kursiv, **kw)


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=54, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=86):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))


def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3):
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie im Vorbild)."""
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % len(opt)
    dreh = lambda i: (i - k) % len(opt)
    opt = [opt[(i + k) % len(opt)] for i in range(len(opt))]
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': dreh(richtig), 'rueck': {str(dreh(i)): v for i, v in rueck.items()}}
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(dreh(i)): v for i, v in rueck_sprich.items()}
    return d


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.6, bei=0.3, eingabe=None):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if eingabe:
        d['eingabe'] = eingabe
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Planimetrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-2b'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Vierecke sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms vierecke; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def quad(P, farbe=1, fu=0.12, **kw):
    return V(P, farbe, fu, **kw)


def weg(t0, t1, P0, P1):
    """Bewegung eines Vielecks von P0 nach P1 zwischen t0 und t1."""
    return [[t0, {}], [t1, {'punkte': [r3(p) for p in P1]}]]


# ════════════════════════════════════════════════ Kapitel 1 · Einführung «Die Vierecks-Familie»
# a = 5: A(0.5|1), B(5.5|1). Allgemein C(6|5.5), D(1.5|4.5) → Trapez C(5|4.5) → Parallelogramm C(6.5|4.5)
# → Rechteck D(0.5|4.5), C(5.5|4.5) · Rhombus D(3.5|5), C(8.5|5) · Quadrat D(0.5|6), C(5.5|6). (zahlen.py)
W1 = geo(-0.5, -1.5, 10)
A1, B1 = (0.5, 1), (5.5, 1)
ALLG = [A1, B1, (6, 5.5), (1.5, 4.5)]
TRAP = [A1, B1, (5, 4.5), (1.5, 4.5)]
PARA = [A1, B1, (6.5, 4.5), (1.5, 4.5)]
RECHT = [A1, B1, (5.5, 4.5), (0.5, 4.5)]
RHOM = [A1, B1, (8.5, 5), (3.5, 5)]
QUAD = [A1, B1, (5.5, 6), (0.5, 6)]
ABCD = ['A', 'B', 'C', 'D']


def eckmarken(P0, P1=None, t0=None, t1=None):
    """Eckennamen, die mit einer Bewegung P0 → P1 mitlaufen."""
    e0 = ecken(P0, ABCD)
    if P1 is None:
        return e0
    e1 = ecken(P1, ABCD)
    return [mit(a, bewegung=[[t0, {}], [t1, {'bei': b['bei']}]]) if a['bei'] != b['bei'] else a for a, b in zip(e0, e1)]


P70 = [(0.5, 1), (6, 1), (7.368, 4.759), (1.868, 4.759)]      # Parallelogramm mit α = 70° (Seite 4 schräg)
clip('familie', 1, 'Vierecke sehen: die Vierecks-Familie',
     'Ecken, Seiten, Winkel und Diagonalen benennen; Winkelsumme 360°; Trapez, Parallelogramm, Rechteck, Rhombus und '
     'Quadrat entstehen Bedingung um Bedingung, mit ihren Diagonalen; Winkel im Parallelogramm.',
     ['Viereck', 'Trapez', 'Parallelogramm', 'Rechteck', 'Rhombus', 'Quadrat', 'Winkelsumme'], [
         sz('Bezeichnungen',
            'Ein Viereck beschriftet man gegen den Uhrzeigersinn: Ecken A, B, C und D. Die Seite a führt von A nach B, dann '
            'folgen b, c und d. Die Winkel heissen Alpha, Beta, Gamma und Delta. Die Diagonale e verbindet A mit C, die '
            'Diagonale f verbindet B mit D.',
            f(r'A,\ B,\ C,\ D \ \text{gegen den Uhrzeigersinn}', 300, 46, ein=0.4),
            f(r'a = \overline{AB},\ b = \overline{BC},\ c,\ d', 400, 48, ein=5.4),
            f(r'\alpha,\ \beta,\ \gamma,\ \delta', 500, 50, ein=9.4),
            f(r'\fb{e} = \overline{AC}, \quad \fb{f} = \overline{BD}', 600, 50, ein=13.2),
            graf(W1, [quad(ALLG)] + ecken(ALLG, ABCD), ein=0.3),
            graf(W1, [seite(ALLG[0], ALLG[1], 'a', 2), seite(ALLG[1], ALLG[2], 'b', 2), seite(ALLG[2], ALLG[3], 'c', 2), seite(ALLG[3], ALLG[0], 'd', 2)],
                 ein=5.4, raster=False),
            graf(W1, [WI(ALLG[0], ALLG[1], ALLG[3], 2), WI(ALLG[1], ALLG[2], ALLG[0], 2), WI(ALLG[2], ALLG[3], ALLG[1], 2), WI(ALLG[3], ALLG[0], ALLG[2], 2)],
                 ein=9.4, raster=False),
            graf(W1, [S(ALLG[0], ALLG[2], 2, True, 3), S(ALLG[1], ALLG[3], 2, True, 3),
                      T(4.4, 3.95, 'e', 2), T(2.6, 2.3, 'f', 2)], ein=13.2, raster=False)),
         sz('Winkelsumme',
            'Die Diagonale e zerlegt das Viereck in zwei Dreiecke. Jedes hat die Winkelsumme hundertachtzig Grad. Zusammen '
            'ergeben die vier Winkel des Vierecks darum dreihundertsechzig Grad.',
            f(r'\alpha + \beta + \gamma + \delta = 2 \cdot 180^\circ = \fc{360^\circ}', 300, 50, ein=8.8),
            graf(W1, [quad(ALLG), S(ALLG[0], ALLG[2], 2, False, 3)] + ecken(ALLG, ABCD), ein=0.3),
            graf(W1, [V([ALLG[0], ALLG[1], ALLG[2]], 3, 0.25, dicke=0)], ein=2.6, raster=False),
            graf(W1, [V([ALLG[0], ALLG[2], ALLG[3]], 2, 0.2, dicke=0), T(3.9, 2.2, '180°', 3, g=26, kursiv=False),
                      T(2.4, 4.0, '180°', 2, g=26, kursiv=False)], ein=3.4, raster=False)),
         sz('Trapez',
            'Schieb die Ecke C, bis die Seite c parallel zu a liegt. Ein Paar paralleler Gegenseiten genügt: Das Viereck ist ein '
            'Trapez.',
            n('Trapez: @a \\parallel c@', 300, 'blau', 52, ein=5.6),
            graf(W1, [mit(quad(ALLG), bewegung=weg(0.6, 2.6, ALLG, TRAP))] + eckmarken(ALLG, TRAP, 0.6, 2.6), ein=0.3),
            graf(W1, [S(TRAP[0], TRAP[1], 2, dicke=6), S(TRAP[3], TRAP[2], 2, dicke=6)], ein=3.4, raster=False)),
         sz('Parallelogramm',
            'Zieh die Seite c so lang wie a. Dann sind auch b und d parallel: ein Parallelogramm. Gegenseiten sind gleich lang, '
            'gegenüberliegende Winkel gleich gross, und die Diagonalen halbieren sich.',
            n('Parallelogramm:|beide Paare parallel', 300, 'blau', 48, ein=4.2),
            n('Diagonalen halbieren sich', 470, 'blau', 44, ein=9.0),
            graf(W1, [mit(quad(TRAP), bewegung=weg(0.4, 2.0, TRAP, PARA))] + eckmarken(TRAP, PARA, 0.4, 2.0), ein=0.3),
            graf(W1, [S(PARA[0], PARA[3], 2, dicke=6), S(PARA[1], PARA[2], 2, dicke=6)], ein=2.6, raster=False),
            # Diagonalen AC (0.5|1)–(6.5|4.5), BD (5.5|1)–(1.5|4.5), Mitte beider (3.5|2.75)
            graf(W1, [S(PARA[0], PARA[2], 3, False, 3), S(PARA[1], PARA[3], 3, False, 3)], punkte=[pt((3.5, 2.75), 3)], ein=9.0, raster=False)),
         sz('Rechteck',
            'Stellst du die Seiten b und d senkrecht, entsteht ein Rechteck. Alle vier Winkel sind rechte Winkel, und die '
            'Diagonalen sind gleich lang.',
            n('Rechteck: vier rechte Winkel|Diagonalen gleich lang', 300, 'blau', 46, ein=3.0),
            graf(W1, [mit(quad(PARA), bewegung=weg(0.4, 2.0, PARA, RECHT))] + eckmarken(PARA, RECHT, 0.4, 2.0), ein=0.3),
            graf(W1, [RW(RECHT[0], 0, 90), RW(RECHT[1], 90, 180), RW(RECHT[2], 180, 270), RW(RECHT[3], 270, 360)], ein=4.0, raster=False),
            graf(W1, [S(RECHT[0], RECHT[2], 3, False, 3), S(RECHT[1], RECHT[3], 3, False, 3)], ein=6.1, raster=False)),
         sz('Rhombus',
            'Vom Parallelogramm aus geht es auch anders: Werden alle vier Seiten gleich lang, entsteht ein Rhombus, auch Raute '
            'genannt. Seine Diagonalen stehen senkrecht aufeinander und halbieren die Winkel.',
            n('Rhombus (Raute):|vier gleich lange Seiten', 300, 'blau', 46, ein=5.0),
            n('Diagonalen senkrecht,|halbieren die Winkel', 470, 'blau', 44, ein=7.2),
            graf(W1, [mit(quad(PARA), bewegung=weg(2.9, 4.4, PARA, RHOM))] + eckmarken(PARA, RHOM, 2.9, 4.4), ein=0.3),
            # Diagonalen AC (0.5|1)–(8.5|5) und BD (5.5|1)–(3.5|5), Schnitt (4.5|3); Richtungen 26.57° und 116.57°
            graf(W1, [S(RHOM[0], RHOM[2], 2, False, 3), S(RHOM[1], RHOM[3], 2, False, 3), RW((4.5, 3), 26.57, 116.57, 2)], ein=7.2, raster=False),
            # «halbieren die Winkel» (Ton 9.6): die zwei Hälften von α
            graf(W1, [WI(RHOM[0], RHOM[1], RHOM[2], 3, 70), WI(RHOM[0], RHOM[2], RHOM[3], 3, 56)], ein=9.6, raster=False)),
         sz('Quadrat',
            'Ein Quadrat ist beides zugleich, ein Rechteck und ein Rhombus. Darum ist jedes Quadrat auch ein Parallelogramm und ein '
            'Trapez. Jede Bedingung macht die Figur spezieller.',
            n('Trapez|@\\supset@ Parallelogramm|@\\supset@ Rechteck und Rhombus|@\\supset@ Quadrat', 300, 'blau', 44, ein=4.2),
            graf(W1, [mit(quad(RHOM), bewegung=weg(0.4, 2.2, RHOM, QUAD))] + eckmarken(RHOM, QUAD, 0.4, 2.2), ein=0.3),
            graf(W1, [S(QUAD[0], QUAD[2], 2, False, 3), S(QUAD[1], QUAD[3], 2, False, 3), RW((3, 3.5), 45, 135, 2)], ein=2.6, raster=False)),
         sz('Winkel',
            'Im Parallelogramm sind gegenüberliegende Winkel gleich gross, benachbarte ergänzen sich zu hundertachtzig Grad. '
            'Ist Alpha siebzig Grad, dann ist Beta hundertzehn Grad, Gamma siebzig und Delta hundertzehn Grad.',
            f(r'\alpha + \beta = 180^\circ', 300, 54, ein=4.4),
            f(r'\alpha = 70^\circ \;\Rightarrow\; \beta = \fc{110^\circ}', 410, 50, ein=8.7),
            f(r'\gamma = \fc{70^\circ}, \quad \delta = \fc{110^\circ}', 510, 50, ein=10.0),
            graf(W1, [quad(P70)] + ecken(P70, ABCD), ein=0.3),
            graf(W1, [WI(P70[0], P70[1], P70[3], 2, 46), T(1.75, 1.55, '70°', 2, g=24, kursiv=False)], ein=6.9, raster=False),
            graf(W1, [WI(P70[1], P70[2], P70[0], 3, 40), T(5.75, 1.75, '110°', 3, g=24, kursiv=False)], ein=8.8, raster=False),
            graf(W1, [WI(P70[2], P70[3], P70[1], 3, 46), T(6.1, 4.2, '70°', 3, g=24, kursiv=False),
                      WI(P70[3], P70[0], P70[2], 3, 40), T(2.65, 4.05, '110°', 3, g=24, kursiv=False)], ein=10.0, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Die vier Winkel ergeben dreihundertsechzig Grad. Jedes Quadrat ist ein Rechteck und ein Rhombus, '
            'beide sind Parallelogramme, und jedes Parallelogramm ist ein Trapez.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\alpha + \beta + \gamma + \delta = 360^\circ', 400, 56, ein=1.2),
            n('Quadrat @\\subset@ Rechteck, Rhombus|@\\subset@ Parallelogramm @\\subset@ Trapez', 520, 'blau', 44, ein=4.0)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
WK1 = ach(-1, -1, 10, (1, 2, 3, 4, 5, 6, 7, 8), (1, 2, 3, 4, 5, 6, 7, 8))
W1k = geo(-0.5, -1.5, 12)
RH1 = [(0.5, 1), (5.5, 1), (8.5, 5), (3.5, 5)]          # Rhombus 5, 3, 4
QU1 = [(7, 6.5), (10.5, 6.5), (10.5, 10), (7, 10)]
P65 = [(0.5, 1), (7, 1), (7 + 4.5 * math.cos(math.radians(65)), 1 + 4.5 * math.sin(math.radians(65))),
       (0.5 + 4.5 * math.cos(math.radians(65)), 1 + 4.5 * math.sin(math.radians(65)))]
REK = [(1, 1.5), (10, 1.5), (10, 6.5), (1, 6.5)]
clip('kontrolle-familie', 2, 'Vierecke sehen: Kontrollfragen zur Vierecks-Familie',
     'Fünf Fragen zu Rhombus und Quadrat, zu Winkeln im Parallelogramm, zu gleich langen Diagonalen, zur vierten Ecke eines '
     'Parallelogramms und zur Winkelsumme.',
     ['Viereck', 'Rhombus', 'Parallelogramm', 'Kontrollfragen'], [
         sz('Frage 1',
            'Nein, nicht jeder. Ein Rhombus hat vier gleich lange Seiten, aber nicht unbedingt rechte Winkel. Erst mit rechten '
            'Winkeln wird er zum Quadrat.',
            n('Rhombus: vier gleiche Seiten|Quadrat: dazu vier rechte Winkel', 300, 'blau', 46, ein=1.0),
            graf(W1k, [quad(RH1), T(4.5, 0.2, 'Rhombus', 5, g=26, kursiv=False), quad(QU1, 3, 0.15),
                       T(8.75, 5.7, 'Quadrat', 5, g=26, kursiv=False), RW(QU1[0], 0, 90, 3)], ein=1.0)),
         sz('Frage 2',
            'Benachbarte Winkel ergänzen sich zu hundertachtzig Grad: Beta ist hundertachtzig minus fünfundsechzig, also '
            'hundertfünfzehn Grad.',
            f(r'\beta = 180^\circ - 65^\circ = \fc{115^\circ}', 300, 52, ein=1.0),
            graf(W1k, [quad(P65)] + ecken(P65, ABCD) + [WI(P65[0], P65[1], P65[3], 2, 46), T(1.85, 1.55, '65°', 2, g=24, kursiv=False),
                                                       WI(P65[1], P65[2], P65[0], 3, 40), T(6.7, 1.75, '115°', 3, g=24, kursiv=False)], ein=1.0)),
         sz('Frage 3',
            'Das Rechteck. Seine Diagonalen sind immer gleich lang. Beim Rhombus stehen sie senkrecht, im Parallelogramm halbieren '
            'sie sich nur.',
            n('Rechteck: Diagonalen gleich lang', 300, 'blau', 48, ein=1.0),
            graf(W1k, [quad(REK), S(REK[0], REK[2], 3, False, 5), S(REK[1], REK[3], 3, False, 5)] + ecken(REK, ABCD), ein=1.0)),
         sz('Frage 4',
            'D liegt bei drei, vier. Dann ist A D parallel zu B C, und C D ist so lang wie A B.',
            f(r'D(\fc{3} \mid \fc{4})', 300, 60, ein=1.0),
            # A(1|1), B(6|1), C(8|4) gegeben; D = A + C − B = (3|4)
            graf(WK1, [S((1, 1), (6, 1), 1, dicke=4), S((6, 1), (8, 4), 1, dicke=4), T(0.7, 0.35, 'A', kursiv=False),
                       T(6.2, 0.35, 'B', kursiv=False), T(8.4, 4.35, 'C', kursiv=False)],
                 punkte=[pt((1, 1)), pt((6, 1)), pt((8, 4))], ein=0.05),
            graf(WK1, [V([(1, 1), (6, 1), (8, 4), (3, 4)], 3, 0.15, dicke=3), T(2.65, 4.4, 'D', 3, kursiv=False)],
                 punkte=[pt((3, 4), 3)], ein=1.2, raster=False)),
         sz('Frage 5',
            'Dreihundertsechzig minus fünfundachtzig minus hundertzehn minus fünfundsiebzig ergibt neunzig Grad.',
            f(r'\delta = 360^\circ - 85^\circ - 110^\circ - 75^\circ = \fc{90^\circ}', 300, 46, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Winkelsumme dreihundertsechzig Grad. Im Parallelogramm ergänzen sich benachbarte Winkel zu '
            'hundertachtzig Grad.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\alpha + \\beta + \\gamma + \\delta = 360^\\circ@|Parallelogramm: @\\alpha + \\beta = 180^\\circ@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Ist jeder Rhombus ein Quadrat?', ['Nein, nicht jeder', 'Ja, jeder', 'Nein, keiner'], 0,
              {0: 'Ja.', 1: 'Was braucht ein Quadrat ausser vier gleichen Seiten? Hat das jeder Rhombus?',
               2: 'Ein Quadrat hat vier gleich lange Seiten. Ist es damit ein Rhombus?'},
              sprich='Ist jeder Rhombus ein Quadrat?',
              rueck_sprich={1: 'Was braucht ein Quadrat ausser vier gleichen Seiten? Hat das jeder Rhombus?',
                            2: 'Ein Quadrat hat vier gleich lange Seiten. Ist es damit ein Rhombus?'}),
         wahl('Frage 2', 'Ein Parallelogramm hat α = 65°. Wie gross ist β?', ['115°', '65°', '295°'], 0,
              {0: 'Ja.', 1: 'Gleich gross sind gegenüberliegende Winkel. β liegt neben α.',
               2: 'Das ist 360° − 65°. Was gilt für zwei Winkel an derselben Seite zwischen zwei Parallelen?'},
              sprich='Ein Parallelogramm hat Alpha gleich fünfundsechzig Grad. Wie gross ist Beta?',
              rueck_sprich={1: 'Gleich gross sind gegenüberliegende Winkel. Beta liegt neben Alpha.',
                            2: 'Das ist dreihundertsechzig minus fünfundsechzig Grad. Was gilt für zwei Winkel an derselben Seite zwischen zwei Parallelen?'}),
         wahl('Frage 3', 'Welches Viereck hat immer gleich lange Diagonalen?', ['das Rechteck', 'der Rhombus', 'das Parallelogramm'], 0,
              {0: 'Ja.', 1: 'Die Diagonalen des Rhombus stehen senkrecht. Sind sie auch bei einem schiefen Rhombus gleich lang?',
               2: 'Die Diagonalen des Parallelogramms halbieren sich. Sind sie auch bei einem schiefen Parallelogramm gleich lang?'},
              sprich='Welches Viereck hat immer gleich lange Diagonalen?',
              rueck_sprich={1: 'Die Diagonalen des Rhombus stehen senkrecht. Sind sie auch bei einem schiefen Rhombus gleich lang?',
                            2: 'Die Diagonalen des Parallelogramms halbieren sich. Sind sie auch bei einem schiefen Parallelogramm gleich lang?'}),
         klick('Frage 4', 'Tipp die vierte Ecke D an, so dass ABCD ein Parallelogramm wird.', [3, 4], 'Getroffen: D(3 | 4).',
               [{'bei': [1, 4], 'text': 'Dann wäre AD senkrecht. AD muss parallel zu BC sein.',
                 'sprich': 'Dann wäre A D senkrecht. A D muss parallel zu B C sein.'},
                {'bei': [6, 4], 'text': 'Dann wäre CD nur 2 lang. Im Parallelogramm ist CD so lang wie AB.',
                 'sprich': 'Dann wäre C D nur zwei lang. Im Parallelogramm ist C D so lang wie A B.'}],
               FALSCH, sprich='Tipp die vierte Ecke D an, so dass A B C D ein Parallelogramm wird.', falsch_sprich=FALSCH,
               eingabe=['x', 'y']),
         wahl('Frage 5', 'Drei Winkel eines Vierecks sind 85°, 110° und 75°. Wie gross ist der vierte?', ['90°', '270°', '−90°'], 0,
              {0: 'Ja.', 1: 'Das ist die Summe der drei. Wie viel fehlt noch bis zur Winkelsumme?',
               2: 'Ein Winkel ist nie negativ. Wie gross ist die Winkelsumme im Viereck?'},
              sprich='Drei Winkel eines Vierecks sind fünfundachtzig, hundertzehn und fünfundsiebzig Grad. Wie gross ist der vierte?',
              rueck_sprich={1: 'Das ist die Summe der drei. Wie viel fehlt noch bis zur Winkelsumme?',
                            2: 'Ein Winkel ist nie negativ. Wie gross ist die Winkelsumme im Viereck?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung «Fläche und Umfang»
W2 = geo(-0.5, -3.5, 13)
RE5 = [(1, 1), (6, 1), (6, 4), (1, 4)]
PA7 = [(1, 1), (8, 1), (10, 4), (3, 4)]                  # a 7, v 2, h 3
PA7s = [(1, 1), (8, 1), (12, 4), (5, 4)]                 # geschert, v 4
PA8 = [(0, 1), (8, 1), (12, 4), (4, 4)]                  # a 8, b 5, h 3 (Startwert sim2)
FB = (6.88, 0.16)                                        # Fusspunkt des Lots von D(4|4) auf die Gerade BC (zahlen.py)
RH8 = [(2, 4), (6, 1), (10, 4), (6, 7)]                  # Rhombus e 8, f 6
clip('flaeche', 3, 'Vierecke sehen: Fläche und Umfang',
     'Rechteck a · b über Einheitsquadrate; Parallelogramm a · h durch Abschneiden und Anlegen; Scherung: Fläche bleibt, '
     'Umfang nicht; die zweite Höhe als Abstand; Rhombus ½ · e · f.',
     ['Viereck', 'Flächeninhalt', 'Umfang', 'Parallelogramm', 'Rhombus', 'Höhe'], [
         sz('Rechteck',
            'Die Fläche eines Rechtecks zählt Einheitsquadrate. Bei a gleich fünf und b gleich drei Zentimeter sind es drei Reihen '
            'zu je fünf Quadraten: fünf mal drei gleich fünfzehn Quadratzentimeter. Der Umfang ist zwei mal fünf plus drei, gleich '
            'sechzehn Zentimeter.',
            f(r'A = a \cdot b = 5 \cdot 3 = \fc{15\,\mathrm{cm}^2}', 300, 50, ein=8.8),
            f(r'U = 2(a + b) = \fc{16\,\mathrm{cm}}', 410, 50, ein=13.4),
            graf(W2, [quad(RE5), seite(RE5[0], RE5[1], 'a = 5', 5, kursiv=False, g=26), seite(RE5[1], RE5[2], 'b = 3', 5, d=0.9, kursiv=False, g=26)], ein=0.3),
            # «drei Reihen zu je fünf Quadraten» (Ton ≈ 6.0–7.6): die Reihen nacheinander grün
            graf(W2, [V([(1, 1 + i), (6, 1 + i), (6, 2 + i), (1, 2 + i)], 3, 0.18, dicke=1.5) for i in range(1)]
                 + [S((x, 1), (x, 2), 3, dicke=1.5) for x in (2, 3, 4, 5)], ein=6.0, raster=False),
            graf(W2, [V([(1, 2), (6, 2), (6, 3), (1, 3)], 3, 0.18, dicke=1.5)] + [S((x, 2), (x, 3), 3, dicke=1.5) for x in (2, 3, 4, 5)], ein=6.4, raster=False),
            graf(W2, [V([(1, 3), (6, 3), (6, 4), (1, 4)], 3, 0.18, dicke=1.5)] + [S((x, 3), (x, 4), 3, dicke=1.5) for x in (2, 3, 4, 5)], ein=6.8, raster=False)),
         sz('Parallelogramm',
            'Beim Parallelogramm schneidest du links ein Dreieck ab und setzt es rechts an. Es entsteht ein Rechteck mit derselben '
            'Grundseite a und der Höhe h. Die Fläche ist also a mal h; die schräge Seite b zählt nicht.',
            f(r'A = a \cdot \fb{h}', 300, 62, ein=8.6),
            graf(W2, [quad(PA7), S((3, 4), (3, 1), 2, True, 3), RW((3, 1), 0, 90, 2), T(2.7, 2.35, 'h', 2, 'end'),
                      seite(PA7[0], PA7[1], 'a', 5), seite(PA7[3], PA7[0], 'b', 5)], ein=0.3),
            # «links ein Dreieck ab und setzt es rechts an» (≈ 1.6–3.4): Stück (1|1), (3|1), (3|4) wandert um 7 nach rechts
            graf(W2, [V([(1, 1), (3, 1), (3, 4)], 4, 0.15, gestrichelt=True, dicke=3),
                      mit(V([(1, 1), (3, 1), (3, 4)], 3, 0.25), bewegung=[[3.1, {}], [4.0, {'punkte': [[8, 1], [10, 1], [10, 4]]}]])],
                 ein=2.2, raster=False),
            graf(W2, [V([(3, 1), (10, 1), (10, 4), (3, 4)], 3, 0.0, dicke=6)], ein=5.0, raster=False)),
         sz('Scherung',
            'Schiebst du die obere Seite zur Seite, bleiben a und h gleich, also auch die Fläche. Der Umfang zwei mal a plus b wächst '
            'aber, weil die Seite b länger wird.',
            n('@a@, @h@ gleich: @A@ gleich|@b@ länger: @U@ grösser', 300, 'blau', 48, ein=4.4),
            graf(W2, [mit(quad(PA7), bewegung=weg(0.4, 2.2, PA7, PA7s)),
                      mit(S((3, 4), (3, 1), 2, True, 3), bewegung=[[0.4, {}], [2.2, {'von': [5, 4], 'bis': [5, 1]}]]),
                      mit(RW((3, 1), 0, 90, 2), bewegung=[[0.4, {}], [2.2, {'bei': [5, 1]}]]),
                      mit(T(2.7, 2.35, 'h', 2, 'end'), bewegung=[[0.4, {}], [2.2, {'bei': [4.7, 2.35]}]]),
                      seite(PA7[0], PA7[1], 'a', 5),
                      mit(S((1, 1), (3, 4), 3, dicke=6), ein=8.0, bewegung=[[0.4, {}], [2.2, {'bis': [5, 4]}]])], ein=0.3)),
         sz('Vorgelöst',
            'Ein Parallelogramm mit a gleich acht, b gleich fünf und der Höhe drei Zentimeter auf a. Die Fläche ist acht mal drei, '
            'gleich vierundzwanzig Quadratzentimeter. Der Umfang ist zwei mal acht plus fünf, gleich sechsundzwanzig Zentimeter.',
            f(r'a = 8, \ b = 5, \ \fb{h} = 3 \ (\mathrm{cm})', 300, 48, ein=0.4),
            f(r'A = 8 \cdot 3 = \fc{24\,\mathrm{cm}^2}', 410, 52, ein=7.4),
            f(r'U = 2(8 + 5) = \fc{26\,\mathrm{cm}}', 520, 52, ein=12.3),
            graf(W2, [quad(PA8), S((4, 4), (4, 1), 2, True, 3), RW((4, 1), 0, 90, 2), T(3.7, 2.35, 'h = 3', 2, 'end', g=26, kursiv=False),
                      seite(PA8[0], PA8[1], 'a = 8', 5, kursiv=False, g=26), seite(PA8[3], PA8[0], 'b = 5', 5, d=0.75, kursiv=False, g=26)]
                 + ecken(PA8, ABCD), ein=0.3)),
         sz('Zweite Höhe',
            'Jede Seite kann Grundseite sein. Mit b als Grundseite ist die Fläche b mal h b. Also ist h b gleich vierundzwanzig durch '
            'fünf, gleich vier Komma acht Zentimeter: der Abstand der Seiten A D und B C.',
            f(r'A = b \cdot \fc{h_b}', 300, 60, ein=4.2),
            f(r'h_b = \tfrac{24}{5} = \fc{4.8\,\mathrm{cm}}', 410, 54, ein=8.6),
            graf(W2, [quad(PA8), seite(PA8[3], PA8[0], 'b = 5', 5, d=0.75, kursiv=False, g=26)] + ecken(PA8, ABCD), ein=0.3),
            # Gerade BC verlängert; Lot von D(4|4) auf BC mit Fusspunkt (6.88|0.16), Richtungen 36.87° (BC) und 126.87° (zu D)
            graf(W2, [S((5.6, -0.8), (12.4, 4.3), 5, True, 2.5), S((4, 4), FB, 3, False, 4), RW(FB, 36.87, 126.87, 3),
                      T(5.85, 2.3, 'h', 3, 'end')], ein=4.4, raster=False)),
         sz('Rhombus',
            'Ein Rhombus, auch Raute genannt, ist ein Parallelogramm mit vier gleich langen Seiten. Seine Diagonalen e und f stehen '
            'senkrecht aufeinander. Er füllt genau die Hälfte des Rechtecks e mal f. Mit e gleich acht und f gleich sechs ist die '
            'Fläche ein Halb mal acht mal sechs, gleich vierundzwanzig Quadratzentimeter.',
            f(r'A = \tfrac{1}{2} \cdot e \cdot f', 300, 60, ein=10.6),
            f(r'A = \tfrac{1}{2} \cdot 8 \cdot 6 = \fc{24\,\mathrm{cm}^2}', 420, 52, ein=16.0),
            graf(W2, [quad(RH8)] + ecken(RH8, ABCD), ein=0.3),
            graf(W2, [S((2, 4), (10, 4), 2, False, 3), S((6, 1), (6, 7), 2, False, 3), RW((6, 4), 0, 90, 2),
                      T(8, 4.25, 'e', 2), T(6.3, 5.5, 'f', 2, 'start')], ein=5.3, raster=False),
            # «die Hälfte des Rechtecks e mal f» (≈ 10–12): Rechteck (2|1)–(10|7) und die vier Eckdreiecke
            graf(W2, [V([(2, 1), (10, 1), (10, 7), (2, 7)], 5, 0.0, gestrichelt=True, dicke=2.5),
                      V([(2, 1), (6, 1), (2, 4)], 3, 0.22, dicke=0), V([(6, 1), (10, 1), (10, 4)], 3, 0.22, dicke=0),
                      V([(10, 4), (10, 7), (6, 7)], 3, 0.22, dicke=0), V([(6, 7), (2, 7), (2, 4)], 3, 0.22, dicke=0)], ein=9.6, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Rechteck a mal b, Parallelogramm Grundseite mal zugehörige Höhe, Rhombus ein Halb mal e mal f. Die Höhe '
            'ist der Abstand der parallelen Seiten.',
            titel('Zum Mitnehmen', 250, 76),
            n('Rechteck @a \\cdot b@|Parallelogramm @a \\cdot h_a = b \\cdot h_b@|Rhombus @\\tfrac12\\, e \\cdot f@', 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
W2k = geo(-0.5, -2.5, 12)
PK = [(1, 1), (7, 1), (9, 5), (3, 5)]                     # a 6, h 4: Linie 1 D→(4|1), Linie 2 D→(3|1), Linie 3 B→D
PSa = [(0.5, 1), (5, 1), (6, 4), (1.5, 4)]                 # Scherung: a 4.5, h 3
PSb = [(0.5, 1), (5, 1), (9, 4), (4.5, 4)]
clip('kontrolle-flaeche', 4, 'Vierecke sehen: Kontrollfragen zu Fläche und Umfang',
     'Fünf Fragen zur Parallelogrammfläche, zur Höhe im Bild, zum Rhombus, zur Scherung und zum Abstand h_b.',
     ['Viereck', 'Flächeninhalt', 'Höhe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Grundseite mal Höhe: neun mal vier gleich sechsunddreissig Quadratzentimeter. Die schräge Seite zählt nicht.',
            f(r'A = a \cdot h = 9 \cdot 4 = \fc{36\,\mathrm{cm}^2}', 300, 50, ein=1.0)),
         sz('Frage 2',
            'Linie zwei. Sie steht senkrecht auf A B. Linie eins endet schräg in der Mitte von A B, Linie drei ist die Diagonale.',
            f(r'h \perp \overline{AB}', 300, 60, ein=1.0),
            graf(W2k, [quad(PK), S((3, 5), (4, 1), 5, True, 2.5), S((3, 5), (3, 1), 5, True, 2.5), S((7, 1), (3, 5), 5, True, 2.5),
                       T(3.95, 2.0, '1', 5, 'start', 26, False), T(2.7, 2.0, '2', 5, 'end', 26, False), T(5.55, 3.3, '3', 5, 'start', 26, False)]
                 + ecken(PK, ABCD), ein=0.05),
            graf(W2k, [S((3, 5), (3, 1), 2, False, 6), RW((3, 1), 0, 90, 2)], ein=1.0, raster=False)),
         sz('Frage 3',
            'Ein Halb mal zehn mal sieben gleich fünfunddreissig Quadratzentimeter.',
            f(r'A = \tfrac{1}{2} \cdot 10 \cdot 7 = \fc{35\,\mathrm{cm}^2}', 300, 50, ein=1.0)),
         sz('Frage 4',
            'Die Fläche bleibt gleich, denn a und h bleiben. Der Umfang ändert sich, weil die schräge Seite länger oder kürzer wird.',
            n('@A = a \\cdot h@ bleibt|@U@ ändert sich', 300, 'blau', 50, ein=1.0),
            graf(W2k, [quad(PSa), mit(V(PSb, 3, 0.12, gestrichelt=True, dicke=3), ein=1.0),
                       S((1.5, 4), (1.5, 1), 2, True, 2.5), mit(S((4.5, 4), (4.5, 1), 2, True, 2.5), ein=1.0)], ein=1.0)),
         sz('Frage 5',
            'Die Fläche ist zehn mal drei gleich dreissig. Geteilt durch b gleich fünf ergibt h b gleich sechs Zentimeter.',
            f(r'A = 10 \cdot 3 = 30', 300, 52, ein=1.0),
            f(r'h_b = \tfrac{30}{5} = \fc{6\,\mathrm{cm}}', 410, 52, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Grundseite mal zugehörige Höhe. Die Höhe steht senkrecht und misst den Abstand der Parallelseiten.',
            titel('Zum Mitnehmen', 250, 76),
            n('@A = a \\cdot h_a = b \\cdot h_b@|Höhe: senkrechter Abstand', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Parallelogramm mit a = 9 cm, b = 6 cm und h = 4 cm auf a: Wie gross ist A?', ['36 cm²', '54 cm²', '18 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist a · b. Ist die schräge Seite b eine Höhe?', 2: 'Das ist die Hälfte. Rechnest du hier mit einem Dreieck?'},
              sprich='Parallelogramm mit a gleich neun, b gleich sechs und h gleich vier Zentimeter auf a: Wie gross ist A?',
              rueck_sprich={1: 'Das ist a mal b. Ist die schräge Seite b eine Höhe?', 2: 'Das ist die Hälfte. Rechnest du hier mit einem Dreieck?'}),
         wahl('Frage 2', 'Welche Linie ist die Höhe zur Grundseite AB?', ['Linie 2', 'Linie 1', 'Linie 3'], 0,
              {0: 'Ja.', 1: 'Linie 1 endet in der Mitte von AB. Steht sie senkrecht auf AB?', 2: 'Linie 3 verbindet B und D. Steht sie senkrecht auf AB?'},
              sprich='Welche Linie ist die Höhe zur Grundseite A B?',
              rueck_sprich={1: 'Linie eins endet in der Mitte von A B. Steht sie senkrecht auf A B?', 2: 'Linie drei verbindet B und D. Steht sie senkrecht auf A B?'}),
         wahl('Frage 3', 'Rhombus mit e = 10 cm und f = 7 cm: Wie gross ist die Fläche?', ['35 cm²', '70 cm²', '17 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist das ganze Rechteck um die Diagonalen. Welchen Teil davon füllt der Rhombus?', 2: 'Das ist e + f. Eine Fläche ist ein Produkt.'},
              sprich='Rhombus mit e gleich zehn und f gleich sieben Zentimeter: Wie gross ist die Fläche?',
              rueck_sprich={1: 'Das ist das ganze Rechteck um die Diagonalen. Welchen Teil davon füllt der Rhombus?', 2: 'Das ist e plus f. Eine Fläche ist ein Produkt.'}),
         wahl('Frage 4', 'Die obere Seite eines Parallelogramms wird verschoben, a und h bleiben. Was gilt?',
              ['A bleibt gleich, U ändert sich', 'A und U bleiben gleich', 'A ändert sich, U bleibt gleich'], 0,
              {0: 'Ja.', 1: 'Die Fläche hängt nur von a und h ab. Gilt das auch für den Umfang?', 2: 'Von welchen Längen hängt A = a · h ab? Ändern die sich?'},
              sprich='Die obere Seite eines Parallelogramms wird verschoben, a und h bleiben. Was gilt?',
              rueck_sprich={1: 'Die Fläche hängt nur von a und h ab. Gilt das auch für den Umfang?', 2: 'Von welchen Längen hängt A gleich a mal h ab? Ändern die sich?'}),
         wahl('Frage 5', 'Parallelogramm: a = 10 cm, h_a = 3 cm, b = 5 cm. Wie gross ist h_b?', ['6 cm', '1.5 cm', '12 cm'], 0,
              {0: 'Ja.', 1: 'Umgekehrt gerechnet. Wie gross ist zuerst die Fläche?', 2: 'Das ist 2A durch b, wie beim Dreieck. Gilt hier A = b · h_b?'},
              sprich='Parallelogramm: a gleich zehn, h a gleich drei, b gleich fünf Zentimeter. Wie gross ist h b?',
              rueck_sprich={1: 'Umgekehrt gerechnet. Wie gross ist zuerst die Fläche?', 2: 'Das ist zwei A durch b, wie beim Dreieck. Gilt hier A gleich b mal h b?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung «Trapez und Mittellinie»
W3 = geo(0, -1.75, 8.5)                                   # Trapez gross; die gedrehte Kopie braucht W3b
W3b = geo(0.5, -3.5, 12)
TZ = [(1, 1), (7, 1), (5.5, 4), (1.5, 4)]                 # a 6, c 4, h 3, v 0.5 (Startwert sim3)
M1, M2 = (1.25, 2.5), (6.25, 2.5)
KOPIE = [(2 * M2[0] - p[0], 2 * M2[1] - p[1]) for p in TZ]   # (11.5|4), (5.5|4), (7|1), (11|1)
TZs = [(1, 1), (7, 1), (7.5, 4), (3.5, 4)]                # geschert, v 2.5
TZr = [(1, 1), (7, 1), (5, 4), (3, 4)]                    # rückwärts: a 6, c 2, h 3
clip('trapez', 5, 'Vierecke sehen: Trapez und Mittellinie',
     'Grundseiten, Schenkel und Höhe; die Mittellinie m = ½(a + c) auf halber Höhe; zwei Trapeze bilden ein Parallelogramm: '
     'A = m · h; Scherung; rückwärts die Höhe aus der Fläche.',
     ['Trapez', 'Mittellinie', 'Flächeninhalt', 'Höhe'], [
         sz('Trapez',
            'Im Trapez sind die Grundseiten a und c parallel. Die Schenkel b und d verbinden sie. Die Höhe h ist der Abstand der '
            'beiden Parallelen.',
            f(r'a \parallel c', 300, 60, ein=0.4),
            f(r'\fb{h}: \ \text{Abstand von } a \text{ und } c', 410, 48, ein=6.0),
            graf(W3, [quad(TZ), seite(TZ[0], TZ[1], 'a'), seite(TZ[2], TZ[3], 'c')] + ecken(TZ, ABCD), ein=0.3),
            graf(W3, [seite(TZ[1], TZ[2], 'b'), seite(TZ[3], TZ[0], 'd')], ein=3.6, raster=False),
            graf(W3, [S((5.5, 4), (5.5, 1), 2, True, 3), RW((5.5, 1), 90, 180, 2), T(5.2, 2.0, 'h', 2, 'end')], ein=6.0, raster=False)),
         sz('Mittellinie',
            'Die Mittellinie m verbindet die Mitten der beiden Schenkel. Sie liegt parallel zu a und c, genau auf halber Höhe. Ihre '
            'Länge ist der Mittelwert der Parallelseiten: m gleich a plus c, durch zwei.',
            f(r'\fb{m} = \tfrac{1}{2}(a + c)', 300, 60, ein=9.1),
            graf(W3, [quad(TZ), seite(TZ[0], TZ[1], 'a'), seite(TZ[2], TZ[3], 'c')] + ecken(TZ, ABCD), ein=0.3),
            graf(W3, [S(M1, M2, 2, False, 5), T(3.75, 2.75, 'm', 2)], punkte=[pt(M1, 2), pt(M2, 2)], ein=1.2, raster=False)),
         sz('Warum die Hälfte',
            'Dreh eine Kopie des Trapezes um hundertachtzig Grad und leg sie an den Schenkel b. Zusammen entsteht ein '
            'Parallelogramm mit der Grundseite a plus c und der Höhe h. Ein Trapez ist die Hälfte davon: A gleich ein Halb mal a '
            'plus c mal h, also m mal h.',
            f(r'A = \tfrac{1}{2}(a + c) \cdot h = \fb{m} \cdot h', 300, 52, ein=11.6),
            graf(W3b, [quad(TZ, 1, 0.2),
                      # Kopie dreht sich um die Mitte von BC (6.25|2.5) um 180° und landet auf (5.5|4), (7|1), (11|1), (11.5|4)
                      mit(V(TZ, 2, 0.2), ein=0.8, um=[6.25, 2.5], bewegung=[[1.0, {'drehung': 0}], [3.0, {'drehung': 180}]]),
                      mit(T(6, 0.45, 'a + c', 5, kursiv=False, g=28), ein=7.4), mit(S((1, 0.75), (11, 0.75), 5, False, 2), ein=7.4),
                      mit(S((1.5, 4), (1.5, 1), 5, True, 2.5), ein=8.6), mit(T(1.85, 2.0, 'h', 5, 'start'), ein=8.6)], ein=0.3)),
         sz('Vorgelöst',
            'Zum Beispiel a gleich sechs, c gleich vier und h gleich drei Zentimeter. Die Mittellinie ist sechs plus vier, durch zwei, '
            'gleich fünf. Die Fläche ist fünf mal drei, gleich fünfzehn Quadratzentimeter.',
            f(r'a = 6, \ c = 4, \ h = 3 \ (\mathrm{cm})', 300, 48, ein=0.4),
            f(r'm = \tfrac{1}{2}(6 + 4) = \fb{5\,\mathrm{cm}}', 410, 50, ein=7.5),
            f(r'A = 5 \cdot 3 = \fc{15\,\mathrm{cm}^2}', 520, 52, ein=9.9),
            graf(W3, [quad(TZ), seite(TZ[0], TZ[1], 'a = 6', 5, kursiv=False, g=26), seite(TZ[2], TZ[3], 'c = 4', 5, kursiv=False, g=26),
                      S((5.5, 4), (5.5, 1), 5, True, 2.5), T(5.2, 1.6, 'h = 3', 5, 'end', g=24, kursiv=False)], ein=0.3),
            graf(W3, [S(M1, M2, 2, False, 5), T(3.75, 2.75, 'm = 5', 2, g=26, kursiv=False)], ein=7.5, raster=False)),
         sz('Scherung',
            'Schiebst du die obere Seite zur Seite, bleiben a, c und h gleich. Darum bleiben auch die Mittellinie und die Fläche gleich. '
            'Nur der Umfang ändert sich.',
            n('@a@, @c@, @h@ gleich:|@m@ und @A@ gleich, @U@ nicht', 300, 'blau', 48, ein=5.0),
            graf(W3, [mit(quad(TZ), bewegung=[[0.6, {}], [2.4, {'punkte': [r3(p) for p in TZs]}], [4.4, {}], [6.0, {'punkte': [r3(p) for p in TZ]}]]),
                      mit(S(M1, M2, 2, False, 5), bewegung=[[0.6, {}], [2.4, {'von': [2.25, 2.5], 'bis': [7.25, 2.5]}], [4.4, {}], [6.0, {'von': list(M1), 'bis': list(M2)}]]),
                      mit(T(3.75, 2.75, 'm', 2), bewegung=[[0.6, {}], [2.4, {'bei': [4.75, 2.75]}], [4.4, {}], [6.0, {'bei': [3.75, 2.75]}]])], ein=0.3)),
         sz('Rückwärts',
            'Es geht auch rückwärts. Ein Trapez hat die Fläche zwölf Quadratzentimeter, a ist sechs und c zwei Zentimeter. Dann ist '
            'die Mittellinie vier, und die Höhe ist zwölf durch vier, gleich drei Zentimeter.',
            f(r'A = 12\,\mathrm{cm}^2, \ a = 6, \ c = 2', 300, 48, ein=0.4),
            f(r'm = 4 \;\Rightarrow\; h = \tfrac{12}{4} = \fc{3\,\mathrm{cm}}', 420, 50, ein=10.4),
            graf(W3, [quad(TZr), seite(TZr[0], TZr[1], 'a = 6', 5, kursiv=False, g=26), seite(TZr[2], TZr[3], 'c = 2', 5, kursiv=False, g=26),
                      S((3, 4), (3, 1), 2, True, 3), mit(T(3.35, 2.4, 'h = ?', 2, 'start', g=26, kursiv=False), aus=10.4),
                      mit(T(3.35, 2.4, 'h = 3', 3, 'start', g=26, kursiv=False), ein=10.4)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Die Mittellinie ist das Mittel von a und c. Die Fläche des Trapezes ist Mittellinie mal Höhe.',
            titel('Zum Mitnehmen', 250, 76),
            n('@m = \\tfrac12(a + c)@|@A = m \\cdot h@', 400, 'blau', 50, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W3k = geo(-0.5, -3.5, 13)
TL = [(0, 1), (5, 1), (4, 4), (1, 4)]                     # a 5, c 3, h 3, gleichschenklig
TRr = [(6.5, 1), (11.5, 1), (12, 4), (9, 4)]              # a 5, c 3, h 3, geschert
WK3 = ach(-1, -1, 11, (1, 2, 3, 4, 5, 6, 7, 8, 9), (1, 2, 3, 4, 5, 6, 7, 8, 9))
clip('kontrolle-trapez', 6, 'Vierecke sehen: Kontrollfragen zum Trapez',
     'Fünf Fragen zur Mittellinie, zu zwei verschieden schiefen Trapezen, zur Fläche, zur Höhe aus Fläche und Mittellinie und zur '
     'Mitte eines Schenkels.',
     ['Trapez', 'Mittellinie', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zwölf plus acht gleich zwanzig, durch zwei gleich zehn Zentimeter.',
            f(r'm = \tfrac{1}{2}(12 + 8) = \fc{10\,\mathrm{cm}}', 300, 52, ein=1.0)),
         sz('Frage 2',
            'Beide sind gleich gross. Sie haben dieselben Parallelseiten und dieselbe Höhe: Mittellinie vier mal Höhe drei, gleich '
            'zwölf Quadratzentimeter.',
            f(r'A = \tfrac{1}{2}(5 + 3) \cdot 3 = \fc{12\,\mathrm{cm}^2}', 300, 48, ein=1.0),
            graf(W3k, [quad(TL), quad(TRr), seite(TL[0], TL[1], 'a = 5', 5, kursiv=False, g=24), seite(TL[2], TL[3], 'c = 3', 5, kursiv=False, g=24),
                       seite(TRr[0], TRr[1], 'a = 5', 5, kursiv=False, g=24), seite(TRr[2], TRr[3], 'c = 3', 5, kursiv=False, g=24),
                       S((1, 4), (1, 1), 2, True, 2.5), T(1.3, 2.2, 'h = 3', 2, 'start', g=22, kursiv=False),
                       S((9, 4), (9, 1), 2, True, 2.5), T(9.3, 2.2, 'h = 3', 2, 'start', g=22, kursiv=False)], ein=0.05),
            graf(W3k, [S((0.5, 2.5), (4.5, 2.5), 3, False, 4), S((7.5, 2.5), (11.5, 2.5), 3, False, 4)], ein=1.0, raster=False)),
         sz('Frage 3',
            'Die Mittellinie ist neun plus fünf, durch zwei, gleich sieben. Sieben mal sechs gleich zweiundvierzig Quadratzentimeter.',
            f(r'A = \tfrac{1}{2}(9 + 5) \cdot 6 = 7 \cdot 6 = \fc{42\,\mathrm{cm}^2}', 300, 46, ein=1.0)),
         sz('Frage 4',
            'Aus A gleich m mal h folgt h gleich vierzig durch acht, gleich fünf Zentimeter.',
            f(r'h = \tfrac{A}{m} = \tfrac{40}{8} = \fc{5\,\mathrm{cm}}', 300, 52, ein=1.0)),
         sz('Frage 5',
            'Die Mitte des Schenkels A D liegt bei eins, zwei — auf halber Höhe.',
            f(r'\text{Mitte von } \overline{AD}: \ (\fc{1} \mid \fc{2})', 300, 50, ein=1.0),
            graf(WK3, [quad([(0, 0), (9, 0), (6, 4), (2, 4)]), T(-0.35, -0.6, 'A', kursiv=False), T(9.3, -0.6, 'B', kursiv=False),
                       T(6.3, 4.45, 'C', kursiv=False), T(1.7, 4.45, 'D', kursiv=False)], ein=0.05),
            graf(WK3, [S((1, 2), (7.5, 2), 2, False, 4)], punkte=[pt((1, 2), 3)], ein=1.2, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Mittellinie gleich Mittelwert von a und c. Fläche gleich Mittellinie mal Höhe — auch rückwärts.',
            titel('Zum Mitnehmen', 250, 76),
            n('@m = \\tfrac12(a + c)@|@A = m \\cdot h@, @h = \\tfrac{A}{m}@', 400, 'blau', 48, ein=1.2)),
     ], [
         wahl('Frage 1', 'Trapez mit a = 12 cm und c = 8 cm: Wie lang ist die Mittellinie?', ['10 cm', '20 cm', '2 cm'], 0,
              {0: 'Ja.', 1: 'Das ist a + c. Ist die Mittellinie so lang wie beide zusammen?', 2: 'Das ist die halbe Differenz. Die Mittellinie liegt zwischen a und c.'},
              sprich='Trapez mit a gleich zwölf und c gleich acht Zentimeter: Wie lang ist die Mittellinie?',
              rueck_sprich={1: 'Das ist a plus c. Ist die Mittellinie so lang wie beide zusammen?', 2: 'Das ist die halbe Differenz. Die Mittellinie liegt zwischen a und c.'}),
         wahl('Frage 2', 'Welches der beiden Trapeze hat die grössere Fläche?', ['beide gleich', 'das linke', 'das rechte'], 0,
              {0: 'Ja.', 1: 'Vergleich a, c und h der beiden. Wovon hängt die Fläche ab?', 2: 'Es sieht grösser aus. Vergleich a, c und h der beiden.'},
              sprich='Welches der beiden Trapeze hat die grössere Fläche?',
              rueck_sprich={1: 'Vergleich a, c und h der beiden. Wovon hängt die Fläche ab?', 2: 'Es sieht grösser aus. Vergleich a, c und h der beiden.'}),
         wahl('Frage 3', 'Wie gross ist die Fläche des Trapezes mit a = 9 cm, c = 5 cm und h = 6 cm?', ['42 cm²', '84 cm²', '270 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist (a + c) · h, das Parallelogramm aus zwei Trapezen.', 2: 'Das ist a · c · h. Wo steht in der Formel a + c?'},
              sprich='Wie gross ist die Fläche des Trapezes mit a gleich neun, c gleich fünf und h gleich sechs Zentimeter?',
              rueck_sprich={1: 'Das ist a plus c mal h, das Parallelogramm aus zwei Trapezen.', 2: 'Das ist a mal c mal h. Wo steht in der Formel a plus c?'}),
         wahl('Frage 4', 'Ein Trapez hat A = 40 cm² und m = 8 cm. Wie hoch ist es?', ['5 cm', '320 cm', '2.5 cm'], 0,
              {0: 'Ja.', 1: 'Das ist A · m. Wie stellst du A = m · h nach h um?', 2: 'Die Formel A = m · h hat kein ½ mehr — das steckt schon in m.'},
              sprich='Ein Trapez hat A gleich vierzig Quadratzentimeter und m gleich acht Zentimeter. Wie hoch ist es?',
              rueck_sprich={1: 'Das ist A mal m. Wie stellst du A gleich m mal h nach h um?', 2: 'Die Formel A gleich m mal h hat kein ein Halb mehr. Das steckt schon in m.'}),
         klick('Frage 5', 'Tipp den Punkt an, in dem die Mittellinie den Schenkel AD trifft.', [1, 2], 'Getroffen: (1 | 2).',
               [{'bei': [2, 4], 'text': 'Das ist D. Die Mittellinie liegt auf halber Höhe.', 'sprich': 'Das ist D. Die Mittellinie liegt auf halber Höhe.'},
                {'bei': [4.5, 0], 'text': 'Das ist die Mitte von AB. Gesucht ist die Mitte des Schenkels AD.', 'sprich': 'Das ist die Mitte von A B. Gesucht ist die Mitte des Schenkels A D.'},
                {'bei': [0, 0], 'text': 'Das ist A. Gesucht ist die Mitte zwischen A und D.', 'sprich': 'Das ist A. Gesucht ist die Mitte zwischen A und D.'}],
               FALSCH, sprich='Tipp den Punkt an, in dem die Mittellinie den Schenkel A D trifft.', falsch_sprich=FALSCH, eingabe=['x', 'y']),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung «Fehlende Längen»
W4 = geo(-1.5, -4.5, 16)
RE12 = [(0.5, 1), (12.5, 1), (12.5, 6), (0.5, 6)]
QU5 = [(4, 1), (9, 1), (9, 6), (4, 6)]
RH4 = [(2.5, 3.5), (6.5, 0.5), (10.5, 3.5), (6.5, 6.5)]   # e 8, f 6, Mitte (6.5|3.5)
TG = [(0.5, 1), (12.5, 1), (8.5, 4), (4.5, 4)]            # a 12, c 4, h 3, Schenkel 5, Überstand 4
clip('laengen', 7, 'Vierecke sehen: fehlende Längen mit Pythagoras',
     'Das rechtwinklige Teildreieck finden: Diagonale im Rechteck und im Quadrat, Seite des Rhombus aus den halben Diagonalen, '
     'Höhe des gleichschenkligen Trapezes aus Schenkel und Überstand; dann Fläche und Umfang.',
     ['Viereck', 'Pythagoras', 'Diagonale', 'Rhombus', 'Trapez', 'Höhe'], [
         sz('Rechteck',
            'Die Diagonale teilt das Rechteck in zwei rechtwinklige Dreiecke, sie ist ihre Hypotenuse. Bei a gleich zwölf und b '
            'gleich fünf Zentimeter ist d die Wurzel aus zwölf im Quadrat plus fünf im Quadrat, gleich dreizehn Zentimeter.',
            f(r'd = \sqrt{a^2 + b^2}', 300, 58, ein=3.8),
            f(r'd = \sqrt{12^2 + 5^2} = \fc{13\,\mathrm{cm}}', 420, 50, ein=10.8),
            graf(W4, [quad(RE12), seite(RE12[0], RE12[1], 'a = 12', 5, kursiv=False, g=26), seite(RE12[1], RE12[2], 'b = 5', 5, d=0.9, kursiv=False, g=26)], ein=0.3),
            graf(W4, [V([RE12[0], RE12[1], RE12[2]], 3, 0.22, dicke=0), S(RE12[0], RE12[2], 2, False, 5), RW(RE12[1], 90, 180, 5),
                      T(6.2, 4.0, 'd', 2)], ein=1.6, raster=False)),
         sz('Quadrat',
            'Im Quadrat sind beide Katheten gleich lang. Darum ist d gleich a mal Wurzel aus zwei. Bei a gleich fünf sind das etwa '
            'sieben Komma null sieben Zentimeter. Diese Abkürzung gilt nur im Quadrat.',
            f(r'd = \sqrt{a^2 + a^2} = a\sqrt{2}', 300, 54, ein=3.0),
            f(r'd = 5\sqrt{2} \approx \fc{7.07\,\mathrm{cm}}', 420, 52, ein=7.0),
            n('nur im Quadrat!', 540, 'rot', 46, ein=9.8),
            graf(W4, [quad(QU5), seite(QU5[0], QU5[1], 'a = 5', 5, kursiv=False, g=26), seite(QU5[1], QU5[2], 'a = 5', 5, d=0.9, kursiv=False, g=26),
                      V([QU5[0], QU5[1], QU5[2]], 3, 0.22, dicke=0), S(QU5[0], QU5[2], 2, False, 5), RW(QU5[1], 90, 180, 5)], ein=0.3)),
         sz('Rhombus',
            'Im Rhombus stehen die Diagonalen senkrecht und halbieren sich. Es entstehen vier rechtwinklige Dreiecke mit den Katheten '
            'e halbe und f halbe. Beim Rhombus mit e gleich acht und f gleich sechs ist die Seite die Wurzel aus vier im Quadrat plus '
            'drei im Quadrat, gleich fünf Zentimeter.',
            f(r'a = \sqrt{(\tfrac{e}{2})^2 + (\tfrac{f}{2})^2}', 300, 54, ein=6.6),
            f(r'a = \sqrt{4^2 + 3^2} = \fc{5\,\mathrm{cm}}', 430, 52, ein=15.2),
            graf(W4, [quad(RH4), S(RH4[0], RH4[2], 2, False, 3), S(RH4[1], RH4[3], 2, False, 3), RW((6.5, 3.5), 0, 90, 2)] + ecken(RH4, ABCD), ein=0.3),
            graf(W4, [V([(6.5, 3.5), RH4[2], RH4[3]], 3, 0.25, dicke=0), T(8.5, 3.0, '4', 3, g=26, kursiv=False), T(6.1, 5.0, '3', 3, 'end', g=26, kursiv=False),
                      T(8.8, 5.4, 'a', 3)], ein=4.6, raster=False)),
         sz('Trapez',
            'Im gleichschenkligen Trapez fällt die Höhe von D und von C auf a. Links und rechts bleibt je ein Überstand: a minus c, '
            'durch zwei. Mit a gleich zwölf, c gleich vier und Schenkeln von fünf Zentimetern ist der Überstand vier, und die Höhe '
            'ist die Wurzel aus fünf im Quadrat minus vier im Quadrat, gleich drei Zentimeter.',
            f(r'\text{Überstand } \tfrac{a - c}{2} = \tfrac{12 - 4}{2} = 4', 300, 46, ein=12.4),
            f(r'h = \sqrt{5^2 - 4^2} = \fc{3\,\mathrm{cm}}', 420, 52, ein=16.6),
            graf(W4, [quad(TG), seite(TG[0], TG[1], 'a = 12', 5, kursiv=False, g=26), seite(TG[2], TG[3], 'c = 4', 5, kursiv=False, g=26),
                      seite(TG[3], TG[0], 's = 5', 5, d=0.6, kursiv=False, g=26)] + ecken(TG, ABCD), ein=0.3),
            graf(W4, [S((4.5, 4), (4.5, 1), 2, True, 3), RW((4.5, 1), 90, 180, 2), S((8.5, 4), (8.5, 1), 2, True, 3), RW((8.5, 1), 0, 90, 2)], ein=2.2, raster=False),
            graf(W4, [V([TG[0], (4.5, 1), TG[3]], 3, 0.25, dicke=0), V([(8.5, 1), TG[1], TG[2]], 3, 0.25, dicke=0),
                      mit(T(2.5, 0.2, '4', 3, g=26, kursiv=False), ein=12.6), mit(T(10.5, 0.2, '4', 3, g=26, kursiv=False), ein=12.6)], ein=5.0, raster=False),
            graf(W4, [T(4.85, 2.4, 'h = 3', 3, 'start', g=26, kursiv=False)], ein=16.6, raster=False)),
         sz('Einsetzen',
            'Erst die fehlende Länge, dann die Formel. Die Mittellinie ist acht, die Fläche also acht mal drei, gleich vierundzwanzig '
            'Quadratzentimeter. Der Umfang ist zwölf plus vier plus zweimal fünf, gleich sechsundzwanzig Zentimeter.',
            f(r'A = \tfrac{1}{2}(12 + 4) \cdot 3 = 8 \cdot 3 = \fc{24\,\mathrm{cm}^2}', 300, 44, ein=6.1),
            f(r'U = 12 + 4 + 2 \cdot 5 = \fc{26\,\mathrm{cm}}', 410, 48, ein=11.6),
            graf(W4, [quad(TG), S((4.5, 4), (4.5, 1), 2, True, 3), T(4.85, 1.5, 'h = 3', 5, 'start', g=26, kursiv=False),
                      seite(TG[0], TG[1], 'a = 12', 5, kursiv=False, g=26), seite(TG[2], TG[3], 'c = 4', 5, kursiv=False, g=26),
                      seite(TG[3], TG[0], 's = 5', 5, d=0.6, kursiv=False, g=26), seite(TG[1], TG[2], 's = 5', 5, d=0.6, kursiv=False, g=26)], ein=0.3),
            graf(W4, [S((2.5, 2.5), (10.5, 2.5), 2, False, 4), T(7.2, 2.7, 'm = 8', 2, g=24, kursiv=False)], ein=3.0, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Such das rechtwinklige Dreieck. Im Rechteck die Diagonale, im Rhombus die halben Diagonalen, im Trapez '
            'Höhe und Überstand. Dann Pythagoras.',
            titel('Zum Mitnehmen', 250, 76),
            n('rechtwinkliges Teildreieck suchen|Rechteck: Diagonale|Rhombus: halbe Diagonalen|Trapez: Höhe und Überstand', 390, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
W4k = geo(-0.5, -3, 14)
R912 = [(1, 1), (13, 1), (13, 10), (1, 10)]
W4t = geo(-1, -5, 16)
T148 = [(0, 1), (14, 1), (11, 5), (3, 5)]                  # a 14, c 8, Überstand 3 (Höhe 4 nur zum Zeichnen)
W5 = geo(-1, -4, 12)
T5 = [(0, 0), (10, 0), (7, 4), (3, 4)]                     # Teildreieck A, (3|0), D: Hypotenuse AD
clip('kontrolle-laengen', 8, 'Vierecke sehen: Kontrollfragen zu fehlenden Längen',
     'Fünf Fragen zur Rechteckdiagonale, zur Quadratdiagonale, zum Überstand im gleichschenkligen Trapez, zur Rhombusseite und '
     'zur Hypotenuse im Teildreieck.',
     ['Pythagoras', 'Diagonale', 'Trapez', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Diagonale ist die Hypotenuse: Wurzel aus neun im Quadrat plus zwölf im Quadrat, gleich fünfzehn Zentimeter.',
            f(r'd = \sqrt{9^2 + 12^2} = \fc{15\,\mathrm{cm}}', 300, 52, ein=1.0),
            graf(W4k, [quad(R912), V([R912[0], R912[1], R912[2]], 3, 0.2, dicke=0), S(R912[0], R912[2], 2, False, 5),
                       seite(R912[0], R912[1], '12', 5, kursiv=False, g=28), seite(R912[3], R912[0], '9', 5, d=0.6, kursiv=False, g=28)], ein=1.0)),
         sz('Frage 2',
            'Im Quadrat ist d gleich a mal Wurzel aus zwei: sechs mal Wurzel aus zwei, etwa acht Komma vier neun Zentimeter.',
            f(r'd = 6\sqrt{2} \approx \fc{8.49\,\mathrm{cm}}', 300, 54, ein=1.0)),
         sz('Frage 3',
            'Vierzehn minus acht gleich sechs. Das verteilt sich auf zwei Seiten: je drei Zentimeter.',
            f(r'\tfrac{14 - 8}{2} = \fc{3\,\mathrm{cm}}', 300, 56, ein=1.0),
            graf(W4t, [quad(T148), seite(T148[0], T148[1], 'a = 14', 5, kursiv=False, g=26), seite(T148[2], T148[3], 'c = 8', 5, kursiv=False, g=26),
                       S((3, 5), (3, 1), 2, True, 2.5), S((11, 5), (11, 1), 2, True, 2.5),
                       S((0, 1), (3, 1), 3, False, 7), S((11, 1), (14, 1), 3, False, 7),
                       T(1.5, 0.2, '3', 3, g=28, kursiv=False), T(12.5, 0.2, '3', 3, g=28, kursiv=False)], ein=1.0)),
         sz('Frage 4',
            'Die Katheten sind die halben Diagonalen, zwölf und fünf. Wurzel aus zwölf im Quadrat plus fünf im Quadrat gleich '
            'dreizehn Zentimeter.',
            f(r'a = \sqrt{12^2 + 5^2} = \fc{13\,\mathrm{cm}}', 300, 52, ein=1.0)),
         sz('Frage 5',
            'Der Schenkel A D liegt dem rechten Winkel gegenüber: Er ist die Hypotenuse.',
            n('Hypotenuse: gegenüber dem rechten Winkel', 300, 'blau', 44, ein=1.0),
            graf(W5, [quad(T5), V([(0, 0), (3, 0), (3, 4)], 3, 0.25, dicke=0), S((3, 4), (3, 0), 5, True, 2.5), RW((3, 0), 90, 180, 5)]
                 + ecken(T5, ABCD), ein=0.05),
            graf(W5, [S((0, 0), (3, 4), 2, False, 7), T(1.0, 2.4, 's', 2, 'end')], ein=1.2, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Erst das rechtwinklige Dreieck, dann Pythagoras. Die Hypotenuse liegt dem rechten Winkel gegenüber.',
            titel('Zum Mitnehmen', 250, 76),
            n('rechtwinkliges Dreieck suchen|Hypotenuse gegenüber dem rechten Winkel', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Rechteck 9 cm × 12 cm: Wie lang ist die Diagonale?', ['15 cm', '21 cm', '≈ 12.73 cm'], 0,
              {0: 'Ja.', 1: 'Das ist a + b. Pythagoras addiert die Quadrate.', 2: 'Das ist 9 · √2. Gilt diese Abkürzung im Rechteck?'},
              sprich='Rechteck neun mal zwölf Zentimeter: Wie lang ist die Diagonale?',
              rueck_sprich={1: 'Das ist a plus b. Pythagoras addiert die Quadrate.', 2: 'Das ist neun mal Wurzel aus zwei. Gilt diese Abkürzung im Rechteck?'}),
         wahl('Frage 2', 'Ein Quadrat hat die Seite 6 cm. Wie lang ist seine Diagonale?', ['≈ 8.49 cm', '12 cm', '36 cm'], 0,
              {0: 'Ja.', 1: 'Das ist der Weg über zwei Seiten. Die Diagonale ist kürzer.', 2: 'Das ist die Fläche, keine Länge.'},
              sprich='Ein Quadrat hat die Seite sechs Zentimeter. Wie lang ist seine Diagonale?',
              rueck_sprich={1: 'Das ist der Weg über zwei Seiten. Die Diagonale ist kürzer.', 2: 'Das ist die Fläche, keine Länge.'}),
         wahl('Frage 3', 'Gleichschenkliges Trapez, a = 14 cm, c = 8 cm: Wie lang ist der Überstand auf jeder Seite?', ['3 cm', '6 cm', '11 cm'], 0,
              {0: 'Ja.', 1: 'Das ist der ganze Unterschied a − c. Auf wie viele Seiten verteilt er sich?', 2: 'Das ist die Mittellinie. Gesucht ist das Stück links und rechts.'},
              sprich='Gleichschenkliges Trapez, a gleich vierzehn, c gleich acht Zentimeter: Wie lang ist der Überstand auf jeder Seite?',
              rueck_sprich={1: 'Das ist der ganze Unterschied a minus c. Auf wie viele Seiten verteilt er sich?', 2: 'Das ist die Mittellinie. Gesucht ist das Stück links und rechts.'}),
         wahl('Frage 4', 'Rhombus mit e = 24 cm und f = 10 cm: Wie lang ist eine Seite?', ['13 cm', '17 cm', '26 cm'], 0,
              {0: 'Ja.', 1: 'Das ist 12 + 5. Pythagoras addiert die Quadrate.', 2: 'Mit den ganzen Diagonalen gerechnet. Wie lang sind die Katheten im Teildreieck?'},
              sprich='Rhombus mit e gleich vierundzwanzig und f gleich zehn Zentimeter: Wie lang ist eine Seite?',
              rueck_sprich={1: 'Das ist zwölf plus fünf. Pythagoras addiert die Quadrate.', 2: 'Mit den ganzen Diagonalen gerechnet. Wie lang sind die Katheten im Teildreieck?'}),
         klick('Frage 5', 'Tipp die Hypotenuse des grünen Teildreiecks an.', [[0, 0], [3, 4]], 'Getroffen: der Schenkel AD.',
               [{'bei': [[3, 4], [3, 0]], 'text': 'Das ist die Höhe, eine Kathete. Die Hypotenuse liegt dem rechten Winkel gegenüber.',
                 'sprich': 'Das ist die Höhe, eine Kathete. Die Hypotenuse liegt dem rechten Winkel gegenüber.'},
                {'bei': [[0, 0], [3, 0]], 'text': 'Das ist der Überstand, eine Kathete. Die Hypotenuse liegt dem rechten Winkel gegenüber.',
                 'sprich': 'Das ist der Überstand, eine Kathete. Die Hypotenuse liegt dem rechten Winkel gegenüber.'}],
               'Nicht ganz. Die grüne Linie zeigt die Hypotenuse.', sprich='Tipp die Hypotenuse des grünen Teildreiecks an.',
               falsch_sprich='Nicht ganz. Die grüne Linie zeigt die Hypotenuse.', tol=0.45),
     ], art='Kontrollclip')
