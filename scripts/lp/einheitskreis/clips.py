"""Erzeugt die zehn Drehbücher des Leitprogramms Einheitskreis (07.10.2026).

  python3 scripts/lp/einheitskreis/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich); nur für
Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie bei Planimetrie: Rechnung und Notizen links (x 150), das Kreisbild rechts (x 1010, y 175,
760 × 760, Fenster in x und y gleich geteilt, sonst wird der Kreis zur Ellipse). Der Einheitskreis ist
aus `figuren` gebaut (HOWTO-clips «Figuren im Graf», «Später einblenden, bewegen, mitlaufen»): Kreis,
Radius, Punkt P, die sin-Strecke (blau) und die cos-Strecke (grün), Winkelbogen, Tangente mit S. Dreht
sich P, rechnet `Lauf` alle Teile aus demselben Winkel θ(t) — dichte Stützpunkte alle 0.05 s, weich
zwischen den Stützwinkeln wie im Abspieler. So bleiben alle Teile beieinander; die Bewegung entlang des
Kreisbogens lässt sich mit linear übergeblendeten Koordinaten nicht anders zeigen.

Zeiten auf den Ton: `wann(clip, szene, wort, nr)` liest die Wortzeiten aus wortzeiten.json (gemessen
mit faster-whisper, scripts/lp/einheitskreis/wortzeiten.py); ohne Messung schätzt es aus der Lage des
Wortes im Sprechertext. Ablauf: clips.py → build-clip-ton.py → wortzeiten.py → clips.py → build-clips.py.

Fragebild (HOWTO-leitprogramme §15): Beim Erscheinen einer Frage zeigt das Bild nur das Gegebene
(Kreis, gegebene Punkte); die Auflösung erscheint ab 1.0 s.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Sinus (Höhe von P)                \\fa{…}
  2 orange = Tangens (Strecke RS, Punkt S)     \\fb{…}
  3 grün   = Cosinus (x-Koordinate von P)      \\fc{…}
  4 rot    = Gegenbeispiel, unmöglich          \\fd{…}
  5 Tinte  = neutral: Kreis, Radius, Punkt P, Winkel, Spiegelachsen, Referenzwinkel
"""
import json
import math
import os
import re
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-4-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


# Fenster: Einheitskreis (gleich geteilt) und Tangentenbild (rechts Platz für x = 1 und S)
# Die Achsenzahlen ±1 setzt graf() selbst als Text neben den Kreis (TICKS): Die Teilung des Bauers
# schriebe sie genau auf die Kreislinie. Darum hier eine Teilung ausserhalb des Fensters.
WK = dict(xbereich=[-1.45, 1.45], ybereich=[-1.45, 1.45], xteilung=[[9, '']], yteilung=[[9, '']])
WT = dict(xbereich=[-1.4, 2.0], ybereich=[-1.7, 1.7], xteilung=[[9, '']], yteilung=[[9, '']])


def cs(g):
    """cos und sin in Grad, auf den Achsen exakt."""
    m = g % 360
    if abs(m) < 1e-9 or abs(m - 360) < 1e-9:
        return 1.0, 0.0
    for w, p in ((90, (0.0, 1.0)), (180, (-1.0, 0.0)), (270, (0.0, -1.0))):
        if abs(m - w) < 1e-9:
            return p
    return math.cos(math.radians(g)), math.sin(math.radians(g))


def r3(v):
    return round(v, 4)


# ---------------------------------------------------------------- Zeit
def wann(clip, szene, wort, nr=1, dazu=0.0):
    """Sekunde ab Szenenbeginn, zu der `wort` (Anfang eines gesprochenen Wortes, klein) zum nr-ten Mal beginnt."""
    w = WZ.get(clip, {}).get(szene)
    if w:
        k = 0
        for wt, a, e in w['woerter']:
            if passt(wort, wt):
                k += 1
                if k == nr:
                    if os.environ.get('WANN'):
                        print('  %-28s %-20s %-10s → %-16s %6.2f' % (clip, szene, wort, wt, a))
                    return round(a + dazu, 2)
    FEHLT.append((clip, szene, wort))
    text = SPRECH.get((clip, szene), '')
    pos, k = -1, 0
    for m in re.finditer(r'\b' + re.escape(wort), text, re.I):
        k += 1
        if k == nr:
            pos = m.start()
            break
    d = DAUER.get((clip, szene)) or (len(text.split()) / 2.4 + 1.2)
    return round(0.4 + max(0, pos) / max(1, len(text)) * (d - 1.2) + dazu, 2)


SPRECH, DAUER = {}, {}
# Whisper schreibt Zahlen als Ziffern («90°») und verhört Fachwörter («Kozinus», «Tangents»): Zahlwörter
# werden in Ziffern übersetzt, längere Wörter ähnlich verglichen (difflib, Verhältnis ≥ 0.7).
ZAHL = {'null': '0', 'zwei': '2', 'vierzig': '40', 'neunzig': '90', 'hundertsieben': '107', 'hundertachtzig': '180',
        'zweihundertfünfundzwanzig': '225', 'zweihundertsiebzig': '270', 'dreihundert': '300',
        'dreihundertsechzig': '360', 'vierhundert': '400', 'dreiundzwanzig': '23'}


def passt(wort, gehoert):
    import difflib
    g = re.sub(r'[^\wäöü]', '', gehoert.lower())
    w_ = wort.lower()
    if not g:
        return False
    if w_ in ZAHL:
        return g == ZAHL[w_] or g.startswith(w_)
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    ck = lambda x: 'c' + x[1:] if x[:1] == 'k' else x
    return (len(w_) >= 5 and ck(w_)[0] == ck(g)[0] and abs(len(w_) - len(g)) <= 3
            and difflib.SequenceMatcher(None, ck(w_), ck(g)).ratio() >= 0.7)


def merke_text(clip, szenen):
    alt = R + 'clips/' + PRAEFIX + clip + '.json'
    frueher = {}
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
    for name, spr in szenen:
        SPRECH[(clip, name)] = spr
        DAUER[(clip, name)] = frueher.get((name, spr))


class Lauf:
    """Winkel θ(t) in Grad aus Stützwinkeln [[t, θ], …], weich (smoothstep) wie im Abspieler."""
    def __init__(self, stuetz):
        self.s = stuetz

    def th(self, t):
        s = self.s
        if t <= s[0][0]:
            return s[0][1]
        for (ta, wa), (tb, wb) in zip(s, s[1:]):
            if t <= tb:
                q = (t - ta) / (tb - ta) if tb > ta else 1.0
                q = q * q * (3 - 2 * q)
                return wa + (wb - wa) * q
        return s[-1][1]

    def zeiten(self):
        z = []
        for (ta, wa), (tb, wb) in zip(self.s, self.s[1:]):
            if abs(wa - wb) < 1e-12:
                z += [ta, tb]
            else:
                n = max(1, int(round((tb - ta) / 0.05)))
                z += [ta + (tb - ta) * i / n for i in range(n + 1)]
        if len(self.s) == 1:
            z = [self.s[0][0]]
        out = []
        for t in z:
            if not out or abs(t - out[-1]) > 1e-6:
                out.append(round(t, 3))
        return out


def bewegt(L, art, felder, **fest):
    """Figur, deren Felder aus θ(t) folgen: felder(θ) → dict. Ohne Bewegung (ein Stützwinkel) steht sie."""
    d = dict(art=art, **fest)
    d.update(felder(L.s[0][1]))
    if len(L.s) > 1:
        d['bewegung'] = [[t, felder(L.th(t))] for t in L.zeiten()]
    return d


def kreis(farbe=5, dicke=3):
    return dict(art='kreis', m=[0, 0], r=1, farbe=farbe, fuellung=0, dicke=dicke)


def T(x, y, text, farbe=5, anker='middle', g=30, kursiv=True, **kw):
    d = dict(art='text', bei=[x, y], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=kursiv)
    d.update(kw)
    return d


def S(a, b, farbe=5, dicke=4, gest=False, **kw):
    d = dict(art='strecke', von=list(a), bis=list(b), farbe=farbe, dicke=dicke)
    if gest:
        d['gestrichelt'] = True
    d.update(kw)
    return d


TICKS = [dict(art='text', bei=b, text=t, farbe=5, anker=a, groesse=24, kursiv=False)
         for b, t, a in (([1.06, -0.14], '1', 'start'), ([-1.06, -0.14], '−1', 'end'),
                         ([-0.06, 1.05], '1', 'end'), ([-0.06, -1.13], '−1', 'end'))]


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def name_rechts(w):
    """Bei P nahe (0 | ±1) stünde der Name auf der Achsenzahl ±1 links der y-Achse: weich nach rechts schieben."""
    return 0.1 * min(1.0, max(0.0, (abs(cs(w)[1]) - 0.85) / 0.15))


def P_teile(L, teile=('dreieck', 'winkel', 'radius', 'cos', 'sin', 'P', 'name'), name='P', farbe_p=5, name_dw=0):
    """Die Teile des Punktes P zum Winkel θ(t): Dreieck OQP, Winkelbogen (über 360° ein zweiter Bogen
    aussen), Radius, cos-Strecke (grün), sin-Strecke (blau), Punkt, Beschriftung."""
    aus = []

    def sichtbar(v):
        return 1 if abs(v) > 0.02 else 0
    if 'dreieck' in teile:
        aus.append(bewegt(L, 'vieleck', lambda w: {'punkte': [[0, 0], [r3(cs(w)[0]), 0], [r3(cs(w)[0]), r3(cs(w)[1])]]},
                          farbe=5, fuellung=0.07, dicke=0.1))
    if 'winkel' in teile:
        aus.append(bewegt(L, 'bogen', lambda w: {'von': r3(min(w, 0)), 'bis': r3(max(0, min(w, 359.9))) if w >= 0 else 0},
                          m=[0, 0], r=0.2, farbe=5, dicke=3))
        if max(abs(w) for _, w in L.s) > 360:
            aus.append(bewegt(L, 'bogen', lambda w: {'bis': r3(max(0.01, w - 360)), 'deckkraft': 1 if w > 360.5 else 0},
                              m=[0, 0], r=0.28, von=0, farbe=5, dicke=3))
    if 'radius' in teile:
        aus.append(bewegt(L, 'strecke', lambda w: {'von': [0, 0], 'bis': [r3(cs(w)[0]), r3(cs(w)[1])]}, farbe=5, dicke=4))
    if 'cos' in teile:
        aus.append(bewegt(L, 'strecke', lambda w: {'von': [0, 0], 'bis': [r3(cs(w)[0]), 0], 'deckkraft': sichtbar(cs(w)[0])}, farbe=3, dicke=9))
    if 'sin' in teile:
        aus.append(bewegt(L, 'strecke', lambda w: {'von': [r3(cs(w)[0]), 0], 'bis': [r3(cs(w)[0]), r3(cs(w)[1])], 'deckkraft': sichtbar(cs(w)[1])}, farbe=1, dicke=9))
    if 'P' in teile:
        aus.append(bewegt(L, 'kreis', lambda w: {'m': [r3(cs(w)[0]), r3(cs(w)[1])]}, r=0.04, farbe=farbe_p, fuellung=1, dicke=3))
    if 'name' in teile and name:
        aus.append(bewegt(L, 'text', lambda w: {'bei': [r3(1.17 * cs(w + name_dw)[0] + name_rechts(w + name_dw)), r3(1.17 * cs(w + name_dw)[1] - 0.05)]}, text=name, farbe=5, anker='middle', groesse=34, kursiv=True))
    return aus


def tan_teile(L, ytop=1.7, name_s=True):
    """Tangente x = 1, Gerade durch O und P bis S (im II./III. Quadranten von P durch O), Strecke RS, Punkt S."""
    def tt(w):
        c, s = cs(w)
        if abs(c) < 1e-6:
            return None
        return max(-60, min(60, s / c))

    def gerade(w):
        c, s = cs(w)
        t = tt(w)
        if t is None:
            return {'von': [0, -3], 'bis': [0, 3]}
        return {'von': [r3(c), r3(s)] if c < 0 else [0, 0], 'bis': [1, r3(t)]}
    aus = [S((1, -ytop), (1, ytop), 5, 3),
           bewegt(L, 'strecke', gerade, farbe=5, dicke=3, gestrichelt=True),
           bewegt(L, 'strecke', lambda w: {'von': [1, 0], 'bis': [1, r3(tt(w) if tt(w) is not None else 0)]}, farbe=2, dicke=9),
           bewegt(L, 'kreis', lambda w: {'m': [1, r3(tt(w) if tt(w) is not None else 99)]}, r=0.045, farbe=2, fuellung=1, dicke=3)]
    if name_s:
        aus.append(bewegt(L, 'text', lambda w: {'bei': [1.16, r3((tt(w) if tt(w) is not None else 99) - 0.03)]}, text='S', farbe=2, anker='start', groesse=34))
    return aus


def graf(W, figuren=(), punkte=(), ein=0.05, aus=None, **kw):
    """Ein Bild hat kein eigenes `aus` — es geht an jede Figur (HOWTO-clips, «ein/aus an einem Teil»)."""
    figuren = [mit(fg, aus=aus) if aus is not None and fg.get('aus') is None else fg for fg in figuren]
    if kw.get('achsen', True) is not False:
        figuren = TICKS + figuren
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def fest(g, teile=('dreieck', 'winkel', 'radius', 'cos', 'sin', 'P', 'name'), **kw):
    """P steht still beim Winkel g."""
    return P_teile(Lauf([[0, g]]), teile, **kw)


def pkt(g, farbe=5, r=0.04, hohl=False, **kw):
    c, s = cs(g)
    d = dict(art='kreis', m=[r3(c), r3(s)], r=r, farbe=farbe, fuellung=0 if hohl else 1, dicke=3)
    d.update(kw)
    return d


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


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None,
          tol=0.2, bei=0.3, eingabe=('x', 'y')):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    if eingabe:
        d['eingabe'] = list(eingabe)   # Antwort ohne Zeigegerät: zwei Zahlfelder (build-clips.py)
    return d


JETZT_DU = ('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.')


def jetzt_du():
    return sz(*JETZT_DU, titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip', folge=None):
    pfad = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(pfad):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(pfad))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Einheitskreis',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-4'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Einheitskreis sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms einheitskreis; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if folge:
        d['folge'] = folge
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(pfad, 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
C = 'sinus-cosinus'
SP1 = [
    ('Radius eins', 'Im rechtwinkligen Dreieck ist der Sinus Gegenkathete durch Hypotenuse. Wir legen das Dreieck in einen Kreis '
                    'mit dem Radius eins. Dann ist die Hypotenuse eins, und der Sinus ist einfach die Höhe des Punktes P. '
                    'Der Cosinus ist seine x-Koordinate.'),
    ('Weiter drehen', 'Den Winkel phi misst man ab der positiven x-Achse, gegen den Uhrzeigersinn. Er darf über neunzig Grad '
                      'hinaus. Bei hundertvierzig Grad ist phi kein Winkel des Dreiecks mehr, aber der Punkt P hat weiterhin '
                      'Koordinaten: Cosinus und Sinus von hundertvierzig Grad.'),
    ('Vorzeichen', 'Weil es Koordinaten sind, haben sie Vorzeichen. Im zweiten Quadranten liegt P links der y-Achse: Der Cosinus '
                   'ist negativ, der Sinus positiv. Im dritten Quadranten sind beide negativ, im vierten nur der Sinus.'),
    ('Auf den Achsen', 'Auf den Achsen sind die Werte besonders einfach. Bei null Grad liegt P bei eins und null, bei neunzig Grad '
                       'bei null und eins, bei hundertachtzig Grad bei minus eins und null, bei zweihundertsiebzig Grad bei null '
                       'und minus eins. Höher als eins oder tiefer als minus eins kommt P nie.'),
    ('Negativ und mehr', 'Ein negativer Winkel dreht im Uhrzeigersinn. Minus sechzig Grad landet auf demselben Punkt wie '
                         'dreihundert Grad. Und vierhundert Grad sind eine volle Runde und noch vierzig Grad.'),
    ('Merke', 'Zum Mitnehmen: P hat die Koordinaten Cosinus phi und Sinus phi. Der Cosinus ist die x-Koordinate, der Sinus '
              'die Höhe. Ihre Vorzeichen zeigen den Quadranten, und beide liegen zwischen minus eins und eins.'),
]
merke_text(C, SP1)
w = lambda s, wort, nr=1, dazu=0.0: wann(C, s, wort, nr, dazu)
sp1 = dict(SP1)
t_hoehe, t_xk = w('Radius eins', 'höhe'), w('Radius eins', 'koordinate')
t_hinaus = w('Weiter drehen', 'hinaus')
t_ii, t_iii, t_iv = w('Vorzeichen', 'zweiten'), w('Vorzeichen', 'dritten'), w('Vorzeichen', 'vierten')
t_n0, t_n90, t_n180, t_n270, t_nie = (w('Auf den Achsen', 'null', 1), w('Auf den Achsen', 'neunzig'), w('Auf den Achsen', 'hundertachtzig'),
                                      w('Auf den Achsen', 'zweihundertsiebzig'), w('Auf den Achsen', 'höher'))
t_neg, t_300, t_400 = w('Negativ und mehr', 'negativer'), w('Negativ und mehr', 'dreihundert'), w('Negativ und mehr', 'vierhundert')
L2 = Lauf([[0, 50], [t_hinaus - 1.0, 50], [t_hinaus + 1.6, 140]])
L3 = Lauf([[0, 140], [t_iii - 0.3, 140], [t_iii + 1.0, 230], [t_iv - 0.3, 230], [t_iv + 1.0, 320]])
L4 = Lauf([[0, 320], [t_n0 - 0.6, 320], [t_n0 + 0.3, 360], [t_n90 - 0.6, 360], [t_n90 + 0.4, 450], [t_n180 - 0.6, 450],
           [t_n180 + 0.4, 540], [t_n270 - 0.6, 540], [t_n270 + 0.4, 630]])
L5a = Lauf([[0, 0], [t_neg + 0.2, 0], [t_neg + 1.6, -60]])
L5b = Lauf([[0, 0], [t_400 + 0.1, 0], [t_400 + 2.6, 400]])
clip(C, 'Einheitskreis sehen: Sinus und Cosinus als Koordinaten',
     'Vom Dreieck zum Kreis mit Radius 1: P(cos φ | sin φ), der Winkel ab der positiven x-Achse, Vorzeichen in den vier '
     'Quadranten, die Achsenpunkte, negative Winkel und Winkel über 360°.',
     ['Einheitskreis', 'Sinus', 'Cosinus', 'Quadrant', 'Vorzeichen'], [
         sz('Radius eins', sp1['Radius eins'],
            f(r'\sin\varphi = \dfrac{\text{Gegenkathete}}{\text{Hypotenuse}}', 280, 50, ein=0.4),
            f(r'\text{Hypotenuse} = 1', 420, 50, ein=w('Radius eins', 'hypotenuse', 2)),
            f(r'\fa{\sin\varphi} = y_P \qquad \fc{\cos\varphi} = x_P', 540, 54, ein=t_hoehe),
            graf(WK, [kreis()] + fest(50, ('dreieck', 'winkel', 'radius', 'P', 'name')) + [T(0.36, 0.08, 'φ', 5, g=32)], ein=0.3),
            graf(WK, [mit(f_, ein=None) for f_ in fest(50, ('sin',))], ein=t_hoehe, raster=False, achsen=False),
            graf(WK, fest(50, ('cos',)), ein=t_xk, raster=False, achsen=False)),
         sz('Weiter drehen', sp1['Weiter drehen'],
            f(r'P(\fc{\cos\varphi} \mid \fa{\sin\varphi})', 280, 64, ein=0.4),
            n('Winkel ab der positiven @x@-Achse,|gegen den Uhrzeigersinn', 400, 'blau', 42, ein=1.4),
            f(r'P \approx (\fc{-0.766} \mid \fa{0.643})', 580, 52, ein=w('Weiter drehen', 'koordinaten')),
            graf(WK, [kreis()] + P_teile(L2), ein=0.3)),
         sz('Vorzeichen', sp1['Vorzeichen'],
            f(r'\text{II}: \ \fc{\cos\varphi \lt 0}, \ \fa{\sin\varphi \gt 0}', 300, 46, ein=t_ii),
            f(r'\text{III}: \ \fc{\cos\varphi \lt 0}, \ \fa{\sin\varphi \lt 0}', 400, 46, ein=t_iii),
            f(r'\text{IV}: \ \fc{\cos\varphi \gt 0}, \ \fa{\sin\varphi \lt 0}', 500, 46, ein=t_iv),
            graf(WK, [kreis(), T(1.2, 1.25, 'I', 5, g=30, kursiv=False), T(-1.2, 1.25, 'II', 5, g=30, kursiv=False),
                      T(-1.2, -1.33, 'III', 5, g=30, kursiv=False), T(1.2, -1.33, 'IV', 5, g=30, kursiv=False)] + P_teile(L3), ein=0.3)),
         sz('Auf den Achsen', sp1['Auf den Achsen'],
            f(r'P(1 \mid 0), \ P(0 \mid 1), \ P(-1 \mid 0), \ P(0 \mid -1)', 300, 44, ein=t_n0),
            f(r'-1 \le \fa{\sin\varphi} \le 1, \qquad -1 \le \fc{\cos\varphi} \le 1', 440, 46, ein=t_nie),
            graf(WK, [kreis()] + P_teile(L4, ('radius', 'cos', 'sin', 'P'))
                 + [T(0.95, 0.1, '(1 | 0)', 5, 'end', 28, False, ein=t_n0 + 0.4),
                    T(0.1, 1.15, '(0 | 1)', 5, 'start', 28, False, ein=t_n90 + 0.4),
                    T(-0.95, 0.1, '(−1 | 0)', 5, 'start', 28, False, ein=t_n180 + 0.4),
                    T(0.1, -1.25, '(0 | −1)', 5, 'start', 28, False, ein=t_n270 + 0.4)], ein=0.3)),
         sz('Negativ und mehr', sp1['Negativ und mehr'],
            f(r'-60^\circ \ \text{und} \ 300^\circ: \ \text{derselbe Punkt}', 300, 46, ein=t_300),
            f(r'400^\circ = 360^\circ + 40^\circ', 440, 50, ein=t_400),
            graf(WK, [kreis()] + P_teile(L5a, ('winkel', 'radius', 'P', 'name')), ein=0.3, aus=t_400),
            graf(WK, [kreis()] + P_teile(L5b, ('winkel', 'radius', 'P', 'name')), ein=t_400)),
         sz('Merke', sp1['Merke'],
            titel('Zum Mitnehmen', 260, 76),
            n('@P(\\fc{\\cos\\varphi} \\mid \\fa{\\sin\\varphi})@|Sinus: Höhe; Cosinus: @x@-Koordinate|Werte zwischen @-1@ und @1@', 400, 'blau', 44, ein=1.2),
            graf(WK, [kreis()] + fest(50), ein=0.3)),
         jetzt_du(),
     ], folge=1)

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
C = 'kontrolle-sinus-cosinus'
SPK1 = [
    ('Frage 1', 'Der Cosinus ist die x-Koordinate: minus null Komma sechs. Null Komma acht ist die Höhe, der Sinus.'),
    ('Frage 2', 'Hundertfünfunddreissig Grad liegt zwischen neunzig und hundertachtzig Grad, im zweiten Quadranten, genau '
                'zwischen der y-Achse und der negativen x-Achse.'),
    ('Frage 3', 'Der Sinus ist negativ, also liegt P unter der x-Achse. Der Cosinus ist positiv, also rechts der y-Achse: '
                'im vierten Quadranten.'),
    ('Frage 4', 'Minus neunzig Grad ist eine Vierteldrehung im Uhrzeigersinn. P liegt ganz unten, bei null und minus eins.'),
    ('Frage 5', 'P liegt auf einem Kreis mit dem Radius eins. Höher als eins kommt er nie, also ist eins Komma zwei für den '
                'Sinus unmöglich.'),
    ('Merke', 'Zum Mitnehmen: P hat die Koordinaten Cosinus phi und Sinus phi. Der Winkel zählt ab der positiven x-Achse '
              'gegen den Uhrzeigersinn, ein negativer Winkel im Uhrzeigersinn.'),
]
merke_text(C, SPK1)
sk1 = dict(SPK1)
clip(C, 'Einheitskreis sehen: Kontrollfragen zu Sinus und Cosinus',
     'Fünf Fragen zu den Koordinaten von P, zum Winkel 135°, zu den Vorzeichen, zu −90° und zu den möglichen Werten des Sinus.',
     ['Einheitskreis', 'Sinus', 'Cosinus', 'Kontrollfragen'], [
         sz('Frage 1', sk1['Frage 1'],
            f(r'\fc{\cos\varphi} = -0.6, \quad \fa{\sin\varphi} = 0.8', 300, 54, ein=1.0),
            graf(WK, [kreis(), dict(art='kreis', m=[-0.6, 0.8], r=0.04, farbe=5, fuellung=1, dicke=3),
                      T(-0.72, 0.95, 'P(−0.6 | 0.8)', 5, 'middle', 30, False)], ein=0.05),
            graf(WK, [S((0, 0), (-0.6, 0), 3, 9), S((-0.6, 0), (-0.6, 0.8), 1, 9)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 2', sk1['Frage 2'],
            f(r'90^\circ \lt 135^\circ \lt 180^\circ', 300, 54, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, fest(135, ('winkel', 'radius', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Frage 3', sk1['Frage 3'],
            f(r'\fa{\sin\varphi \lt 0}, \ \fc{\cos\varphi \gt 0}: \ \text{IV}', 300, 52, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, [T(1.2, -1.33, 'IV', 5, g=34, kursiv=False)] + fest(315, ('radius', 'cos', 'sin', 'P', 'name')), ein=1.0,
                 raster=False, achsen=False)),
         sz('Frage 4', sk1['Frage 4'],
            f(r'-90^\circ: \ P(0 \mid -1)', 300, 56, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, P_teile(Lauf([[1.2, 0], [2.8, -90]]), ('winkel', 'radius', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Frage 5', sk1['Frage 5'],
            f(r'-1 \le \fa{\sin\varphi} \le 1', 300, 56, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, [S((-1.45, 1.2), (1.45, 1.2), 4, 4, True), T(-1.42, 1.27, 'y = 1.2', 4, 'start', 28, False),
                      T(1.42, 1.27, 'kein Kreispunkt', 4, 'end', 28, False),
                      S((-1.45, 1), (1.45, 1), 5, 2, True)], ein=1.0, raster=False, achsen=False)),
         sz('Merke', sk1['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('@P(\\fc{\\cos\\varphi} \\mid \\fa{\\sin\\varphi})@|Winkel gegen den Uhrzeigersinn,|negative im Uhrzeigersinn', 400, 'blau', 44, ein=1.2),
            graf(WK, [kreis()] + fest(-60, ('winkel', 'radius', 'cos', 'sin', 'P', 'name')), ein=0.3)),
     ], [
         wahl('Frage 1', 'P(−0.6 | 0.8) liegt auf dem Einheitskreis. Wie gross ist cos φ?', ['−0.6', '0.8', '0.6'], 0,
              {0: 'Ja.', 1: 'Das ist die Höhe von P. Welche Koordinate ist der Cosinus?',
               2: 'Liegt P rechts oder links der y-Achse?'},
              sprich='P mit den Koordinaten minus null Komma sechs und null Komma acht liegt auf dem Einheitskreis. Wie gross ist Cosinus phi?',
              rueck_sprich={1: 'Das ist die Höhe von P. Welche Koordinate ist der Cosinus?',
                            2: 'Liegt P rechts oder links der y-Achse?'}),
         klick('Frage 2', 'Tipp den Punkt P zum Winkel 135° auf den Kreis.', [-0.7071, 0.7071], 'Getroffen: zweiter Quadrant.',
               [{'bei': [0.7071, 0.7071], 'text': 'Das ist 45°. Gezählt wird ab der positiven x-Achse, gegen den Uhrzeigersinn.',
                 'sprich': 'Das ist fünfundvierzig Grad. Gezählt wird ab der positiven x-Achse, gegen den Uhrzeigersinn.'},
                {'bei': [-0.7071, -0.7071], 'text': 'Das ist 135° im Uhrzeigersinn gedreht. Positive Winkel drehen gegen den Uhrzeigersinn.',
                 'sprich': 'Das ist hundertfünfunddreissig Grad im Uhrzeigersinn gedreht. Positive Winkel drehen gegen den Uhrzeigersinn.'},
                {'bei': [0.7071, -0.7071], 'text': 'Das ist 315°, im vierten Quadranten. 135° liegt zwischen 90° und 180°.',
                 'sprich': 'Das ist dreihundertfünfzehn Grad, im vierten Quadranten. Hundertfünfunddreissig Grad liegt zwischen neunzig und hundertachtzig Grad.'}],
               FALSCH, sprich='Tipp den Punkt P zum Winkel hundertfünfunddreissig Grad auf den Kreis.', falsch_sprich=FALSCH),
         wahl('Frage 3', 'In welchem Quadranten ist sin φ negativ und cos φ positiv?', ['im vierten', 'im zweiten', 'im dritten'], 0,
              {0: 'Ja.', 1: 'Im zweiten Quadranten liegt P links oben. Welches Vorzeichen hat dort die Höhe?',
               2: 'Im dritten Quadranten sind beide Koordinaten negativ.'},
              sprich='In welchem Quadranten ist Sinus phi negativ und Cosinus phi positiv?',
              rueck_sprich={1: 'Im zweiten Quadranten liegt P links oben. Welches Vorzeichen hat dort die Höhe?',
                            2: 'Im dritten Quadranten sind beide Koordinaten negativ.'}),
         wahl('Frage 4', 'Welche Koordinaten hat P bei φ = −90°?', ['(0 | −1)', '(0 | 1)', '(−1 | 0)'], 0,
              {0: 'Ja.', 1: 'Das ist 90°. Ein negativer Winkel dreht im Uhrzeigersinn.',
               2: 'Das ist 180°. Eine Vierteldrehung im Uhrzeigersinn führt nach unten.'},
              sprich='Welche Koordinaten hat P bei phi gleich minus neunzig Grad?',
              rueck_sprich={1: 'Das ist neunzig Grad. Ein negativer Winkel dreht im Uhrzeigersinn.',
                            2: 'Das ist hundertachtzig Grad. Eine Vierteldrehung im Uhrzeigersinn führt nach unten.'}),
         wahl('Frage 5', 'Welchen Wert kann sin φ nie haben?', ['1.2', '−0.9', '1'], 0,
              {0: 'Ja.', 1: '−0.9 kommt vor: P liegt dann fast ganz unten.',
               2: '1 kommt vor: bei 90° liegt P ganz oben.'},
              sprich='Welchen Wert kann Sinus phi nie haben?',
              rueck_sprich={1: 'Minus null Komma neun kommt vor. P liegt dann fast ganz unten.',
                            2: 'Eins kommt vor. Bei neunzig Grad liegt P ganz oben.'}),
     ], art='Kontrollclip', folge=2)

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
C = 'besondere-winkel'
SP2 = [
    ('Fünfundvierzig Grad', 'Bei fünfundvierzig Grad liegt P genau in der Mitte zwischen den Achsen. Seine beiden Koordinaten '
                            'sind gleich gross, nennen wir sie x. Pythagoras gibt: x Quadrat plus x Quadrat gleich eins. Also ist '
                            'x die Wurzel aus einem Halb, und das ist Wurzel zwei durch zwei, ungefähr null Komma sieben null sieben.'),
    ('Sechzig Grad', 'Bei sechzig Grad bilden O, P und der Punkt eins null ein gleichseitiges Dreieck: Alle Seiten sind eins lang. '
                     'Die Höhe von P halbiert die Grundseite. Darum ist der Cosinus von sechzig Grad ein Halb. Die Höhe selbst gibt '
                     'Pythagoras: Wurzel aus eins minus ein Viertel, also Wurzel drei durch zwei.'),
    ('Dreissig Grad', 'Bei dreissig Grad ist es dasselbe Dreieck, nur liegend. Sinus und Cosinus tauschen die Rollen: Sinus '
                      'dreissig Grad ist ein Halb, Cosinus dreissig Grad ist Wurzel drei durch zwei.'),
    ('Die Tabelle', 'Zusammen ergibt das eine Tabelle, die man sich leicht merkt. Der Sinus ist Wurzel null, Wurzel eins, Wurzel '
                    'zwei, Wurzel drei und Wurzel vier, jeweils durch zwei. Der Cosinus hat dieselben Werte rückwärts.'),
    ('Referenzwinkel', 'Und die anderen Quadranten? Hundertfünfzig Grad ist das Spiegelbild von dreissig Grad an der y-Achse. '
                       'Der spitze Winkel zur x-Achse, der Referenzwinkel, ist dreissig Grad. Gleiche Höhe: Sinus hundertfünfzig '
                       'Grad ist ein Halb. Aber P liegt links: Der Cosinus ist minus Wurzel drei durch zwei.'),
    ('Unten', 'Genauso im dritten Quadranten: Zweihundertfünfundzwanzig Grad hat den Referenzwinkel fünfundvierzig Grad, beide '
              'Koordinaten sind negativ. Im vierten Quadranten hat dreihundert Grad den Referenzwinkel sechzig Grad: Der Cosinus '
              'ist ein Halb, der Sinus minus Wurzel drei durch zwei.'),
    ('Merke', 'Zum Mitnehmen: Referenzwinkel zur x-Achse bestimmen, den Betrag aus der Tabelle nehmen und das Vorzeichen aus '
              'dem Quadranten.'),
]
merke_text(C, SP2)
w = lambda s, wort, nr=1, dazu=0.0: wann(C, s, wort, nr, dazu)
sp2 = dict(SP2)
H = math.sqrt(2) / 2
D3 = math.sqrt(3) / 2
t_dreissig = w('Dreissig Grad', 'dasselbe')
L_30 = Lauf([[0, 60], [t_dreissig, 60], [t_dreissig + 1.4, 30]])
t_spiegel, t_ref, t_links = w('Referenzwinkel', 'spiegelbild'), w('Referenzwinkel', 'referenzwinkel'), w('Referenzwinkel', 'aber')
t_225, t_300 = w('Unten', 'zweihundertfünfundzwanzig'), w('Unten', 'dreihundert')
L_unten = Lauf([[0, 150], [t_225 - 0.2, 150], [t_225 + 1.2, 225], [t_300 - 0.3, 225], [t_300 + 1.0, 300]])


def refbogen(g, ein=None, aus=None):
    """Referenzwinkel als Bogen in Tinte (neutral, wie der Winkel φ) zwischen OP und der nächsten Hälfte der x-Achse.
    Orange ist dem Tangens vorbehalten (Prüfung 08.10.2026)."""
    m = g % 360
    von, bis = (m, 180) if 90 < m <= 180 else (180, m) if 180 < m <= 270 else (m, 360) if m > 270 else (0, m)
    return mit(dict(art='bogen', m=[0, 0], r=0.34, von=von, bis=bis, farbe=5, dicke=6), ein=ein, aus=aus)


def fahrt(a, b, t0, t1, name='P'):
    """P wandert von a geradlinig nach b (Spiegelung, keine Drehung — Prüfung 08.10.2026, M1), mit cos-Strecke
    (grün), sin-Strecke (blau), Punkt und Namen. Der Radius zu b erscheint erst, wenn P angekommen ist."""
    L = Lauf([[0, 0.0], [t0, 0.0], [t1, 1.0]])
    pos = lambda q: (r3(a[0] + (b[0] - a[0]) * q), r3(a[1] + (b[1] - a[1]) * q))
    return [bewegt(L, 'strecke', lambda q: {'von': [0, 0], 'bis': [pos(q)[0], 0], 'deckkraft': 1 if abs(pos(q)[0]) > 0.02 else 0}, farbe=3, dicke=9),
            bewegt(L, 'strecke', lambda q: {'von': [pos(q)[0], 0], 'bis': list(pos(q))}, farbe=1, dicke=9),
            S((0, 0), (r3(b[0]), r3(b[1])), 5, 4, ein=t1),
            bewegt(L, 'kreis', lambda q: {'m': list(pos(q))}, r=0.04, farbe=5, fuellung=1, dicke=3),
            bewegt(L, 'text', lambda q: {'bei': [r3(pos(q)[0] * 1.17), r3(pos(q)[1] * 1.17 - 0.05)]}, text=name, farbe=5, anker='middle', groesse=34, kursiv=True)]


clip(C, 'Einheitskreis sehen: die besonderen Winkel',
     'Exakte Werte bei 45°, 60° und 30° aus dem halben Quadrat und dem gleichseitigen Dreieck, die Tabelle mit den Wurzeln und '
     'der Referenzwinkel für die anderen Quadranten.',
     ['besondere Winkel', 'Referenzwinkel', 'Sinus', 'Cosinus', 'ohne Taschenrechner'], [
         sz('Fünfundvierzig Grad', sp2['Fünfundvierzig Grad'],
            f(r'x^2 + x^2 = 1', 280, 56, ein=w('Fünfundvierzig Grad', 'pythagoras')),
            f(r'x = \sqrt{\tfrac12} = \tfrac{\sqrt2}{2} \approx 0.707', 400, 52, ein=w('Fünfundvierzig Grad', 'wurzel')),
            f(r'\fa{\sin 45^\circ} = \fc{\cos 45^\circ} = \tfrac{\sqrt2}{2}', 540, 52, ein=w('Fünfundvierzig Grad', 'ungefähr')),
            graf(WK, [kreis()] + fest(45, ('dreieck', 'winkel', 'radius', 'cos', 'sin', 'P', 'name'))
                 + [T(0.35, -0.12, 'x', 3, g=34), T(0.8, 0.35, 'x', 1, 'start', 34), T(0.3, 0.42, '1', 5, 'end', 32, False)], ein=0.3)),
         sz('Sechzig Grad', sp2['Sechzig Grad'],
            f(r'\fc{\cos 60^\circ} = \tfrac12', 280, 56, ein=w('Sechzig Grad', 'darum')),
            f(r'\fa{\sin 60^\circ} = \sqrt{1 - \tfrac14} = \tfrac{\sqrt3}{2}', 420, 52, ein=w('Sechzig Grad', 'pythagoras')),
            graf(WK, [kreis(), dict(art='vieleck', punkte=[[0, 0], [1, 0], [0.5, r3(D3)]], farbe=5, fuellung=0.07, dicke=3)]
                 + fest(60, ('radius', 'P', 'name')) + [T(0.75, 0.5, '1', 5, 'start', 30, False), T(0.5, -0.13, '1', 5, 'middle', 30, False)], ein=0.3),
            graf(WK, [S((0.5, 0), (0.5, D3), 1, 9), S((0, 0), (0.5, 0), 3, 9), T(0.25, 0.08, '½', 3, 'middle', 34, False)],
                 ein=w('Sechzig Grad', 'höhe'), raster=False, achsen=False)),
         sz('Dreissig Grad', sp2['Dreissig Grad'],
            f(r'\fa{\sin 30^\circ} = \tfrac12, \quad \fc{\cos 30^\circ} = \tfrac{\sqrt3}{2}', 300, 52, ein=w('Dreissig Grad', 'sinus', 2)),
            graf(WK, [kreis()] + P_teile(L_30), ein=0.3)),
         sz('Die Tabelle', sp2['Die Tabelle'],
            f(r'\begin{array}{c|ccccc} \varphi & 0^\circ & 30^\circ & 45^\circ & 60^\circ & 90^\circ \\ \hline \fa{\sin\varphi} & \tfrac{\sqrt0}{2} & \tfrac{\sqrt1}{2} & \tfrac{\sqrt2}{2} & \tfrac{\sqrt3}{2} & \tfrac{\sqrt4}{2} \end{array}',
              300, 40, ein=w('Die Tabelle', 'sinus')),
            f(r'\begin{array}{c|ccccc} \varphi & 0^\circ & 30^\circ & 45^\circ & 60^\circ & 90^\circ \\ \hline \fc{\cos\varphi} & \tfrac{\sqrt4}{2} & \tfrac{\sqrt3}{2} & \tfrac{\sqrt2}{2} & \tfrac{\sqrt1}{2} & \tfrac{\sqrt0}{2} \end{array}',
              560, 40, ein=w('Die Tabelle', 'cosinus')),
            graf(WK, [kreis()] + [pkt(g) for g in (0, 30, 45, 60, 90)]
                 + [S((0, 0), (r3(cs(g)[0]), r3(cs(g)[1])), 5, 2) for g in (30, 45, 60)], ein=0.3)),
         sz('Referenzwinkel', sp2['Referenzwinkel'],
            f(r'\fa{\sin 150^\circ} = \sin 30^\circ = \tfrac12', 300, 50, ein=w('Referenzwinkel', 'gleiche')),
            f(r'\fc{\cos 150^\circ} = -\cos 30^\circ = -\tfrac{\sqrt3}{2}', 420, 50, ein=t_links),
            graf(WK, [kreis(), S((0, -1.45), (0, 1.45), 5, 3, True)] + fest(30, ('radius', 'P'), name='')
                 + fahrt(cs(30), cs(150), t_spiegel, t_spiegel + 1.6) + [refbogen(150, ein=t_ref)], ein=0.3)),
         sz('Unten', sp2['Unten'],
            f(r'225^\circ: \ (\fc{-\tfrac{\sqrt2}{2}} \mid \fa{-\tfrac{\sqrt2}{2}})', 300, 48, ein=w('Unten', 'beide')),
            f(r'300^\circ: \ (\fc{\tfrac12} \mid \fa{-\tfrac{\sqrt3}{2}})', 440, 48, ein=w('Unten', 'cosinus')),
            graf(WK, [kreis()] + P_teile(L_unten, ('radius', 'cos', 'sin', 'P', 'name'))
                 + [refbogen(225, ein=t_225 + 1.2, aus=t_300 - 0.3), refbogen(300, ein=t_300 + 1.0)], ein=0.3)),
         sz('Merke', sp2['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('Referenzwinkel zur @x@-Achse|Betrag aus der Tabelle|Vorzeichen aus dem Quadranten', 400, 'blau', 46, ein=1.2),
            graf(WK, [kreis()] + fest(150, ('radius', 'cos', 'sin', 'P', 'name')) + [refbogen(150)], ein=0.3)),
         jetzt_du(),
     ], folge=3)

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
C = 'kontrolle-besondere-winkel'
SPK2 = [
    ('Frage 1', 'Zweihundertvierzig Grad liegt im dritten Quadranten, der Referenzwinkel ist sechzig Grad. Cosinus sechzig Grad '
                'ist ein Halb, und links der y-Achse wird daraus minus ein Halb.'),
    ('Frage 2', 'Zweihundert Grad liegt zwanzig Grad hinter hundertachtzig Grad. Der Abstand zur x-Achse ist zwanzig Grad.'),
    ('Frage 3', 'Dreihundertdreissig Grad liegt im vierten Quadranten, dreissig Grad unter der x-Achse. P hat die Koordinaten '
                'Wurzel drei durch zwei und minus ein Halb.'),
    ('Frage 4', 'Die Koordinaten sind die Katheten, der Radius eins ist die Hypotenuse. Pythagoras: x Quadrat plus x Quadrat '
                'gleich eins.'),
    ('Frage 5', 'Bei zweihundertsiebzig Grad liegt P ganz unten, bei null und minus eins. Der Sinus ist minus eins.'),
    ('Merke', 'Zum Mitnehmen: erst der Quadrant, dann der Referenzwinkel, dann der Betrag aus der Tabelle und zuletzt das '
              'Vorzeichen.'),
]
merke_text(C, SPK2)
sk2 = dict(SPK2)
clip(C, 'Einheitskreis sehen: Kontrollfragen zu den besonderen Winkeln',
     'Fünf Fragen zu cos 240°, zum Referenzwinkel von 200°, zum Punkt bei 330°, zum halben Quadrat und zu sin 270°.',
     ['besondere Winkel', 'Referenzwinkel', 'Kontrollfragen'], [
         sz('Frage 1', sk2['Frage 1'],
            f(r'\fc{\cos 240^\circ} = -\cos 60^\circ = -\tfrac12', 300, 50, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, fest(240, ('radius', 'cos', 'sin', 'P', 'name')) + [refbogen(240)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 2', sk2['Frage 2'],
            f(r'200^\circ - 180^\circ = 20^\circ', 300, 56, ein=1.0),
            graf(WK, [kreis()] + fest(200, ('winkel', 'radius', 'P', 'name')), ein=0.05),
            graf(WK, [refbogen(200), T(-0.42, -0.15, '20°', 5, 'end', 28, False)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 3', sk2['Frage 3'],
            f(r'330^\circ: \ P\left(\fc{\tfrac{\sqrt3}{2}} \mid \fa{-\tfrac12}\right)', 300, 50, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, fest(330, ('radius', 'cos', 'sin', 'P', 'name')) + [refbogen(330)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 4', sk2['Frage 4'],
            f(r'x^2 + x^2 = 1', 300, 60, ein=1.0),
            graf(WK, [kreis()] + fest(45, ('dreieck', 'radius', 'cos', 'sin', 'P'), name='')
                 + [T(0.35, -0.12, 'x', 3, g=34), T(0.8, 0.35, 'x', 1, 'start', 34), T(0.3, 0.42, '1', 5, 'end', 32, False)], ein=0.05)),
         sz('Frage 5', sk2['Frage 5'],
            f(r'\fa{\sin 270^\circ} = -1', 300, 60, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, fest(270, ('winkel', 'radius', 'sin', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Merke', sk2['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('Quadrant → Referenzwinkel|→ Betrag aus der Tabelle → Vorzeichen', 400, 'blau', 44, ein=1.2),
            graf(WK, [kreis()] + fest(240, ('radius', 'cos', 'sin', 'P', 'name')) + [refbogen(240)], ein=0.3)),
     ], [
         wahl('Frage 1', 'Wie gross ist cos 240°?', ['−1/2', '1/2', '−√3/2'], 0,
              {0: 'Ja.', 1: '240° liegt im dritten Quadranten. Liegt P dort rechts oder links der y-Achse?',
               2: 'Der Referenzwinkel ist 60°, nicht 30°. Wie gross ist cos 60°?'},
              sprich='Wie gross ist Cosinus zweihundertvierzig Grad?',
              rueck_sprich={1: 'Zweihundertvierzig Grad liegt im dritten Quadranten. Liegt P dort rechts oder links der y-Achse?',
                            2: 'Der Referenzwinkel ist sechzig Grad, nicht dreissig. Wie gross ist Cosinus sechzig Grad?'}),
         wahl('Frage 2', 'Welcher Referenzwinkel gehört zu 200°?', ['20°', '160°', '70°'], 0,
              {0: 'Ja.', 1: '160° ist nicht spitz. Der Referenzwinkel ist der Abstand zur nächsten Hälfte der x-Achse.',
               2: '70° ist der Abstand zur y-Achse. Gemessen wird zur x-Achse.'},
              sprich='Welcher Referenzwinkel gehört zu zweihundert Grad?',
              rueck_sprich={1: 'Hundertsechzig Grad ist nicht spitz. Der Referenzwinkel ist der Abstand zur nächsten Hälfte der x-Achse.',
                            2: 'Siebzig Grad ist der Abstand zur y-Achse. Gemessen wird zur x-Achse.'}),
         klick('Frage 3', 'Tipp den Punkt P zum Winkel 330° auf den Kreis.', [round(D3, 4), -0.5], 'Getroffen: vierter Quadrant.',
               [{'bei': [0.5, round(-D3, 4)], 'text': 'Das ist 300°, Referenzwinkel 60°. Bei 330° ist er 30°: P liegt näher an der x-Achse.',
                 'sprich': 'Das ist dreihundert Grad, Referenzwinkel sechzig Grad. Bei dreihundertdreissig Grad ist er dreissig Grad: P liegt näher an der x-Achse.'},
                {'bei': [round(-D3, 4), -0.5], 'text': 'Das ist 210°. 330° liegt im vierten Quadranten, rechts unten.',
                 'sprich': 'Das ist zweihundertzehn Grad. Dreihundertdreissig Grad liegt im vierten Quadranten, rechts unten.'},
                {'bei': [round(D3, 4), 0.5], 'text': 'Das ist 30°. 330° liegt unter der x-Achse.',
                 'sprich': 'Das ist dreissig Grad. Dreihundertdreissig Grad liegt unter der x-Achse.'}],
               FALSCH, sprich='Tipp den Punkt P zum Winkel dreihundertdreissig Grad auf den Kreis.', falsch_sprich=FALSCH),
         wahl('Frage 4', 'Bei 45° sind beide Koordinaten von P gleich gross: x. Welche Gleichung liefert x?',
              ['x² + x² = 1', 'x + x = 1', 'x · x = 1'], 0,
              {0: 'Ja.', 1: 'Die Koordinaten sind Katheten. Was sagt Pythagoras über Katheten und Hypotenuse?',
               2: 'Pythagoras addiert die Quadrate der beiden Katheten.'},
              sprich='Bei fünfundvierzig Grad sind beide Koordinaten von P gleich gross, x. Welche Gleichung liefert x?',
              rueck_sprich={1: 'Die Koordinaten sind Katheten. Was sagt Pythagoras über Katheten und Hypotenuse?',
                            2: 'Pythagoras addiert die Quadrate der beiden Katheten.'}),
         wahl('Frage 5', 'Wie gross ist sin 270°?', ['−1', '0', '1'], 0,
              {0: 'Ja.', 1: '0 ist der Cosinus bei 270°. Wie hoch liegt P?',
               2: '1 ist der Sinus bei 90°. Bei 270° liegt P ganz unten.'},
              sprich='Wie gross ist Sinus zweihundertsiebzig Grad?',
              rueck_sprich={1: 'Null ist der Cosinus bei zweihundertsiebzig Grad. Wie hoch liegt P?',
                            2: 'Eins ist der Sinus bei neunzig Grad. Bei zweihundertsiebzig Grad liegt P ganz unten.'}),
     ], art='Kontrollclip', folge=4)

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
C = 'tangens-pythagoras'
SP3 = [
    ('Die Tangente', 'Rechts am Einheitskreis steht senkrecht die Tangente x gleich eins. Die Gerade durch O und P schneidet sie '
                     'im Punkt S. Die Höhe von S ist der Tangens von phi. Bei vierzig Grad ist das ungefähr null Komma acht vier.'),
    ('Sinus durch Cosinus', 'Die Dreiecke O Q P und O R S sind ähnlich: Beide haben den Winkel phi bei O und einen rechten '
                            'Winkel. Darum ist Tangens durch eins gleich Sinus durch Cosinus.'),
    ('Zweiter Quadrant', 'Im zweiten Quadranten zeigt P nach links. Erst die Verlängerung über O hinaus trifft die Tangente, '
                         'und zwar unter der x-Achse. Bei hundertdreissig Grad ist der Tangens negativ, etwa minus eins Komma eins '
                         'neun. Das passt: positiver Sinus durch negativen Cosinus.'),
    ('Kein Wert', 'Je näher P an neunzig Grad kommt, desto steiler die Gerade und desto höher S. Bei neunzig Grad ist die Gerade '
                  'parallel zur Tangente, es gibt keinen Schnittpunkt. Der Cosinus ist dort null, und durch null teilt man nicht: '
                  'Tangens neunzig Grad ist nicht definiert.'),
    ('Pythagoras', 'Noch eine Beziehung steckt im Dreieck O Q P. Die Katheten sind Cosinus und Sinus, die Hypotenuse ist eins. '
                   'Pythagoras gibt: Sinus Quadrat plus Cosinus Quadrat gleich eins, für jeden Winkel.'),
    ('Den anderen Wert', 'Ist Sinus phi gleich null Komma sechs und liegt phi im zweiten Quadranten, so ist Cosinus Quadrat gleich '
                         'null Komma sechs vier. Die Wurzel gibt null Komma acht, aber links der y-Achse ist der Cosinus negativ: '
                         'minus null Komma acht. Der Tangens ist dann minus null Komma sieben fünf.'),
    ('Merke', 'Zum Mitnehmen: Der Tangens ist die Höhe von S auf der Tangente und gleich Sinus durch Cosinus. Wo der Cosinus null '
              'ist, gibt es keinen Tangens. Und immer gilt: Sinus Quadrat plus Cosinus Quadrat gleich eins.'),
]
merke_text(C, SP3)
w = lambda s, wort, nr=1, dazu=0.0: wann(C, s, wort, nr, dazu)
sp3 = dict(SP3)
t_gerade, t_hoehe_s = w('Die Tangente', 'gerade'), w('Die Tangente', 'höhe')
t_zeigt, t_verl = w('Zweiter Quadrant', 'zeigt'), w('Zweiter Quadrant', 'verlängerung')
L_130 = Lauf([[0, 40], [t_zeigt, 40], [t_verl + 0.6, 130]])
t_steil, t_neunzig = w('Kein Wert', 'steiler'), w('Kein Wert', 'neunzig', 2)
L_90 = Lauf([[0, 50], [t_steil - 1.2, 50], [t_steil + 1.2, 82], [t_neunzig - 0.4, 82], [t_neunzig + 0.6, 90]])
ALPHA_06 = math.degrees(math.atan2(0.6, -0.8))     # 143.13°: sin 0.6 im II. Quadranten
WT_FIG = lambda L, **kw: [kreis()] + tan_teile(L, **kw)


def PARALLEL(ein=None):
    """Bei 90° (270°) liegt die Gerade durch O und P auf der y-Achse und wäre unsichtbar: rot hervorgehoben, mit
    Beschriftung (Prüfung 08.10.2026, M1)."""
    return [mit(S((0, -1.7), (0, 1.7), 4, 6), ein=ein), mit(T(-0.08, 1.48, 'parallel zu x = 1', 4, 'end', 28, False), ein=ein)]
clip(C, 'Einheitskreis sehen: Tangens und Pythagoras',
     'Der Tangens als Höhe von S auf der Tangente x = 1, tan φ = sin φ / cos φ aus ähnlichen Dreiecken, der II. Quadrant, '
     'kein Wert bei 90° und der trigonometrische Pythagoras mit einem Beispiel.',
     ['Tangens', 'Einheitskreis', 'trigonometrischer Pythagoras', 'ähnliche Dreiecke'], [
         sz('Die Tangente', sp3['Die Tangente'],
            f(r'\text{Tangente } x = 1', 280, 52, ein=0.4),
            f(r'S(1 \mid \fb{\tan\varphi})', 400, 60, ein=t_hoehe_s),
            f(r'\fb{\tan 40^\circ} \approx 0.84', 540, 52, ein=w('Die Tangente', 'vierzig')),
            graf(WT, [kreis(), S((1, -1.7), (1, 1.7), 5, 3)] + fest(40, ('winkel', 'radius', 'P', 'name'), name_dw=14), ein=0.3),
            graf(WT, tan_teile(Lauf([[0, 40]]))[1:], ein=t_gerade, raster=False, achsen=False)),
         sz('Sinus durch Cosinus', sp3['Sinus durch Cosinus'],
            f(r'\dfrac{\fb{\tan\varphi}}{1} = \dfrac{\fa{\sin\varphi}}{\fc{\cos\varphi}}', 330, 60, ein=w('Sinus durch Cosinus', 'darum')),
            graf(WT, WT_FIG(Lauf([[0, 40]])) + fest(40, ('winkel', 'radius', 'cos', 'sin', 'P', 'name'), name_dw=14)
                 + [dict(art='vieleck', punkte=[[0, 0], [1, 0], [1, r3(math.tan(math.radians(40)))]], farbe=2, fuellung=0.12, dicke=2, ein=w('Sinus durch Cosinus', 'dreiecke')),
                    dict(art='vieleck', punkte=[[0, 0], [r3(cs(40)[0]), 0], [r3(cs(40)[0]), r3(cs(40)[1])]], farbe=1, fuellung=0.15, dicke=2, ein=w('Sinus durch Cosinus', 'dreiecke')),
                    T(r3(cs(40)[0]) - 0.02, -0.14, 'Q', 5, 'middle', 30), T(1.1, 0.08, 'R', 5, 'start', 30), T(-0.12, -0.14, 'O', 5, 'middle', 30)], ein=0.3)),
         sz('Zweiter Quadrant', sp3['Zweiter Quadrant'],
            f(r'\fb{\tan 130^\circ} \approx -1.19', 300, 52, ein=w('Zweiter Quadrant', 'negativ')),
            f(r'\dfrac{\fa{+}}{\fc{-}} = \fb{-}', 450, 60, ein=w('Zweiter Quadrant', 'passt')),
            graf(WT, WT_FIG(L_130) + P_teile(L_130, ('radius', 'cos', 'sin', 'P', 'name'), name_dw=14), ein=0.3)),
         sz('Kein Wert', sp3['Kein Wert'],
            f(r'\fc{\cos 90^\circ} = 0', 300, 56, ein=w('Kein Wert', 'cosinus')),
            f(r'\Rightarrow \ \fb{\tan 90^\circ} \ \text{nicht definiert}', 420, 50, ein=w('Kein Wert', 'definiert')),
            graf(WT, WT_FIG(L_90) + P_teile(L_90, ('radius', 'P', 'name'), name_dw=14)
                 + PARALLEL(t_neunzig + 0.6), ein=0.3)),
         sz('Pythagoras', sp3['Pythagoras'],
            f(r'\fa{\sin^2\varphi} + \fc{\cos^2\varphi} = 1', 330, 62, ein=w('Pythagoras', 'quadrat')),
            graf(WK, [kreis()] + fest(40, ('dreieck', 'winkel', 'radius', 'cos', 'sin', 'P', 'name'))
                 + [T(0.38, -0.13, 'cos φ', 3, 'middle', 30), T(0.83, 0.3, 'sin φ', 1, 'start', 30), T(0.3, 0.4, '1', 5, 'end', 32, False)], ein=0.3)),
         sz('Den anderen Wert', sp3['Den anderen Wert'],
            f(r'\fc{\cos^2\varphi} = 1 - 0.6^2 = 0.64', 280, 50, ein=w('Den anderen Wert', 'cosinus')),
            f(r'\fc{\cos\varphi} = -0.8 \quad (\text{II. Quadrant})', 400, 50, ein=w('Den anderen Wert', 'minus')),
            f(r'\fb{\tan\varphi} = \tfrac{0.6}{-0.8} = -0.75', 520, 50, ein=w('Den anderen Wert', 'tangens')),
            graf(WK, [kreis(), S((-1.45, 0.6), (1.45, 0.6), 5, 3, True), T(1.42, 0.67, 'y = 0.6', 5, 'end', 28, False)], ein=0.3),
            graf(WK, fest(ALPHA_06, ('radius', 'cos', 'sin', 'P', 'name')), ein=w('Den anderen Wert', 'links'), raster=False, achsen=False)),
         sz('Merke', sp3['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('@\\fb{\\tan\\varphi} = \\dfrac{\\fa{\\sin\\varphi}}{\\fc{\\cos\\varphi}}@, nicht definiert bei @\\cos\\varphi = 0@|@\\fa{\\sin^2\\varphi} + \\fc{\\cos^2\\varphi} = 1@',
              400, 'blau', 42, ein=1.2),
            graf(WT, WT_FIG(Lauf([[0, 40]])) + fest(40, ('winkel', 'radius', 'cos', 'sin', 'P', 'name'), name_dw=14), ein=0.3)),
         jetzt_du(),
     ], folge=5)

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
C = 'kontrolle-tangens-pythagoras'
SPK3 = [
    ('Frage 1', 'Bei hundertfünfunddreissig Grad sind Sinus und Cosinus gleich gross, aber der Cosinus ist negativ. Ihr Quotient '
                'ist minus eins.'),
    ('Frage 2', 'Die Gerade durch P und O trifft die Tangente erst auf der anderen Seite, über der x-Achse. Tangens zweihundertzehn '
                'Grad ist positiv, ungefähr null Komma fünf acht.'),
    ('Frage 3', 'Bei zweihundertsiebzig Grad ist der Cosinus null. Die Gerade durch O und P ist dann parallel zur Tangente.'),
    ('Frage 4', 'Cosinus Quadrat ist eins minus null Komma sechs vier, also null Komma drei sechs. Die Wurzel gibt null Komma sechs, '
                'und im zweiten Quadranten ist der Cosinus negativ: minus null Komma sechs.'),
    ('Frage 5', 'Im Dreieck O Q P sind die Katheten so lang wie die Beträge von Sinus und Cosinus, die Hypotenuse ist der Radius '
                'eins. Das gilt in jedem Quadranten.'),
    ('Merke', 'Zum Mitnehmen: Tangens gleich Sinus durch Cosinus, nicht definiert, wo der Cosinus null ist. Nach dem Wurzelziehen '
              'entscheidet der Quadrant über das Vorzeichen.'),
]
merke_text(C, SPK3)
sk3 = dict(SPK3)
T210 = math.tan(math.radians(210))
clip(C, 'Einheitskreis sehen: Kontrollfragen zu Tangens und Pythagoras',
     'Fünf Fragen zu tan 135°, zum Punkt S bei 210°, zur Stelle ohne Tangens, zum Cosinus aus dem Sinus und zum Grund für sin² + cos² = 1.',
     ['Tangens', 'trigonometrischer Pythagoras', 'Kontrollfragen'], [
         sz('Frage 1', sk3['Frage 1'],
            f(r'\fb{\tan 135^\circ} = \dfrac{\fa{\frac{\sqrt2}{2}}}{\fc{-\frac{\sqrt2}{2}}} = -1', 320, 50, ein=1.0),
            graf(WT, [kreis(), S((1, -1.7), (1, 1.7), 5, 3)], ein=0.05),
            graf(WT, tan_teile(Lauf([[0, 135]]))[1:] + fest(135, ('radius', 'cos', 'sin', 'P', 'name'), name_dw=14), ein=1.0, raster=False, achsen=False)),
         sz('Frage 2', sk3['Frage 2'],
            f(r'\fb{\tan 210^\circ} \approx 0.58', 300, 54, ein=1.0),
            graf(WT, [kreis(), S((1, -1.7), (1, 1.7), 5, 3)] + fest(210, ('radius', 'P', 'name'), name_dw=14), ein=0.05),
            graf(WT, tan_teile(Lauf([[0, 210]]))[1:], ein=1.0, raster=False, achsen=False)),
         sz('Frage 3', sk3['Frage 3'],
            f(r'\fc{\cos 270^\circ} = 0', 300, 56, ein=1.0),
            graf(WT, [kreis(), S((1, -1.7), (1, 1.7), 5, 3)], ein=0.05),
            graf(WT, PARALLEL() + fest(270, ('radius', 'P', 'name'), name_dw=14), ein=1.0, raster=False, achsen=False)),
         sz('Frage 4', sk3['Frage 4'],
            f(r'\fc{\cos^2\varphi} = 1 - 0.64 = 0.36', 280, 50, ein=1.0),
            f(r'\fc{\cos\varphi} = -0.6', 400, 54, ein=1.0),
            graf(WK, [kreis(), S((-1.45, 0.8), (1.45, 0.8), 5, 3, True), T(1.42, 0.87, 'y = 0.8', 5, 'end', 28, False)], ein=0.05),
            graf(WK, fest(math.degrees(math.atan2(0.8, -0.6)), ('radius', 'cos', 'sin', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Frage 5', sk3['Frage 5'],
            f(r'\fa{\sin^2\varphi} + \fc{\cos^2\varphi} = 1^2', 300, 56, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, fest(220, ('dreieck', 'radius', 'cos', 'sin', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Merke', sk3['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('@\\fb{\\tan\\varphi} = \\dfrac{\\fa{\\sin\\varphi}}{\\fc{\\cos\\varphi}}@ für @\\cos\\varphi \\neq 0@|Vorzeichen nach dem Wurzelziehen: Quadrant', 400, 'blau', 42, ein=1.2)),
     ], [
         wahl('Frage 1', 'Wie gross ist tan 135°?', ['−1', '1', 'nicht definiert'], 0,
              {0: 'Ja.', 1: 'Sinus und Cosinus sind gleich gross — haben sie bei 135° dasselbe Vorzeichen?',
               2: 'Zwischen 0° und 360° ist der Tangens nur bei 90° und 270° nicht definiert. Bei 135° trifft die Gerade die Tangente.'},
              sprich='Wie gross ist Tangens hundertfünfunddreissig Grad?',
              rueck_sprich={1: 'Sinus und Cosinus sind gleich gross. Haben sie bei hundertfünfunddreissig Grad dasselbe Vorzeichen?',
                            2: 'Zwischen null und dreihundertsechzig Grad ist der Tangens nur bei neunzig und zweihundertsiebzig Grad nicht definiert. Bei hundertfünfunddreissig Grad trifft die Gerade die Tangente.'}),
         klick('Frage 2', 'Tipp den Punkt S auf der Tangente, der zu φ = 210° gehört.', [1, round(T210, 4)], 'Getroffen: S liegt über der x-Achse.',
               [{'bei': [1, round(-T210, 4)], 'text': 'Im dritten Quadranten sind Sinus und Cosinus beide negativ. Welches Vorzeichen hat ihr Quotient?',
                 'sprich': 'Im dritten Quadranten sind Sinus und Cosinus beide negativ. Welches Vorzeichen hat ihr Quotient?'},
                {'bei': [round(cs(210)[0], 4), -0.5], 'text': 'Das ist P selbst. Gesucht ist der Punkt auf der Tangente x = 1.',
                 'sprich': 'Das ist P selbst. Gesucht ist der Punkt auf der Tangente x gleich eins.'}],
               FALSCH, sprich='Tipp den Punkt S auf der Tangente, der zu phi gleich zweihundertzehn Grad gehört.', falsch_sprich=FALSCH),
         wahl('Frage 3', 'Für welchen Winkel gibt es keinen Tangens?', ['270°', '180°', '0°'], 0,
              {0: 'Ja.', 1: 'Bei 180° ist der Sinus 0: tan 180° = 0.',
               2: 'Bei 0° ist tan 0° = 0. Wo ist der Cosinus null?'},
              sprich='Für welchen Winkel gibt es keinen Tangens?',
              rueck_sprich={1: 'Bei hundertachtzig Grad ist der Sinus null. Tangens hundertachtzig Grad ist null.',
                            2: 'Bei null Grad ist der Tangens null. Wo ist der Cosinus null?'}),
         wahl('Frage 4', 'sin φ = 0.8, und φ liegt im zweiten Quadranten. Wie gross ist cos φ?', ['−0.6', '0.6', '0.2'], 0,
              {0: 'Ja.', 1: 'Die Wurzel gibt 0.6. Liegt P im zweiten Quadranten rechts oder links der y-Achse?',
               2: 'Nicht 1 − 0.8: Die Quadrate ergänzen sich zu 1.'},
              sprich='Sinus phi gleich null Komma acht, und phi liegt im zweiten Quadranten. Wie gross ist Cosinus phi?',
              rueck_sprich={1: 'Die Wurzel gibt null Komma sechs. Liegt P im zweiten Quadranten rechts oder links der y-Achse?',
                            2: 'Nicht eins minus null Komma acht. Die Quadrate ergänzen sich zu eins.'}),
         wahl('Frage 5', 'Warum gilt sin²φ + cos²φ = 1?',
              ['Pythagoras im Dreieck OQP, Hypotenuse 1', 'weil sin φ + cos φ = 1 ist', 'das gilt nur für spitze Winkel'], 0,
              {0: 'Ja.', 1: 'sin 45° + cos 45° ≈ 1.41. Es sind die Quadrate, die sich zu 1 ergänzen.',
               2: 'Das Dreieck OQP gibt es in jedem Quadranten — die Katheten sind |sin φ| und |cos φ|.'},
              sprich='Warum gilt Sinus Quadrat plus Cosinus Quadrat gleich eins?',
              rueck_sprich={1: 'Sinus fünfundvierzig Grad plus Cosinus fünfundvierzig Grad ist ungefähr eins Komma vier eins. Es sind die Quadrate, die sich zu eins ergänzen.',
                            2: 'Das Dreieck O Q P gibt es in jedem Quadranten. Die Katheten sind die Beträge von Sinus und Cosinus.'}),
     ], art='Kontrollclip', folge=6)

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
C = 'symmetrien'
SP4 = [
    ('An der y-Achse', 'Der Punkt A gehört zum Winkel alpha, hier fünfundzwanzig Grad. Spiegeln wir ihn an der y-Achse, entsteht '
                       'der Punkt zu hundertachtzig Grad minus alpha. Er liegt gleich hoch, aber links. Der Sinus bleibt, der '
                       'Cosinus wechselt das Vorzeichen.'),
    ('An der x-Achse', 'An der x-Achse gespiegelt, entsteht der Punkt zu minus alpha. Jetzt bleibt der Cosinus, und der Sinus '
                       'wechselt das Vorzeichen. Minus alpha und dreihundertsechzig Grad minus alpha sind derselbe Punkt.'),
    ('Am Ursprung', 'Spiegeln wir A am Ursprung, entsteht der Punkt zu hundertachtzig Grad plus alpha. Beide Koordinaten '
                    'wechseln das Vorzeichen. Der Tangens als Quotient bleibt darum gleich.'),
    ('Komplement', 'An der Geraden y gleich x gespiegelt, entsteht der Punkt zu neunzig Grad minus alpha. Hier wechselt kein '
                   'Vorzeichen, aber die Koordinaten tauschen die Plätze: Sinus von neunzig Grad minus alpha ist Cosinus alpha. '
                   'Im Bogenmass: Sinus von pi halbe minus phi ist Cosinus phi.'),
    ('Anwenden', 'So rechnet man ohne Taschenrechner, wenn ein Wert bekannt ist: Cosinus fünfundzwanzig Grad ist ungefähr '
                 'null Komma neun null sechs. Cosinus zweihundertfünf Grad ist Cosinus von hundertachtzig plus fünfundzwanzig Grad, '
                 'also minus Cosinus fünfundzwanzig Grad, ungefähr minus null Komma neun null sechs.'),
    ('Merke', 'Zum Mitnehmen: Jede Symmetrie ist eine Spiegelung. An der y-Achse kippt der Cosinus, an der x-Achse der Sinus, '
              'am Ursprung beide. An der Geraden y gleich x tauschen Sinus und Cosinus die Plätze.'),
]
merke_text(C, SP4)
w = lambda s, wort, nr=1, dazu=0.0: wann(C, s, wort, nr, dazu)
sp4 = dict(SP4)
A25 = cs(25)


def spiegelbild(t0, t1, ziel, name='B', ein=None):
    """B wandert von A (25°) geradlinig zu seinem Spiegelbild — so sieht man die Spiegelung, nicht eine Drehung.
    Dazu seine Koordinaten: cos-Strecke (grün) und sin-Strecke (blau), gestrichelt."""
    L = Lauf([[0, 0.0], [t0, 0.0], [t1, 1.0]])
    pos = lambda q: (r3(A25[0] + (ziel[0] - A25[0]) * q), r3(A25[1] + (ziel[1] - A25[1]) * q))
    teile = [bewegt(L, 'strecke', lambda q: {'von': [0, 0], 'bis': [pos(q)[0], 0], 'deckkraft': 1 if abs(pos(q)[0]) > 0.02 else 0}, farbe=3, dicke=7, gestrichelt=True),
             bewegt(L, 'strecke', lambda q: {'von': [pos(q)[0], 0], 'bis': list(pos(q)), 'deckkraft': 1 if abs(pos(q)[1]) > 0.02 else 0}, farbe=1, dicke=7, gestrichelt=True),
             bewegt(L, 'kreis', lambda q: {'m': list(pos(q))}, r=0.045, farbe=2, fuellung=1, dicke=3),
             bewegt(L, 'text', lambda q: {'bei': [r3(pos(q)[0] * 1.17), r3(pos(q)[1] * 1.17 - 0.05)]}, text=name, farbe=2, anker='middle', groesse=34)]
    return [mit(t_, ein=ein) for t_ in teile]


A_FIG = fest(25, ('radius', 'cos', 'sin', 'P', 'name'), name='A')
t_y, t_x, t_o, t_k = w('An der y-Achse', 'spiegeln'), w('An der x-Achse', 'gespiegelt'), w('Am Ursprung', 'spiegeln'), w('Komplement', 'gespiegelt')
clip(C, 'Einheitskreis sehen: Symmetrien',
     'Spiegelungen des Punktes zu α: an der y-Achse (180° − α), an der x-Achse (−α), am Ursprung (180° + α) und an der Geraden '
     'y = x (90° − α), dazu ein Wert ohne Taschenrechner.',
     ['Symmetrie', 'Einheitskreis', 'Komplement', 'ohne Taschenrechner'], [
         sz('An der y-Achse', sp4['An der y-Achse'],
            f(r'\sin(180^\circ - \alpha) = \fa{\sin\alpha}', 300, 50, ein=w('An der y-Achse', 'sinus')),
            f(r'\cos(180^\circ - \alpha) = \fc{-\cos\alpha}', 420, 50, ein=w('An der y-Achse', 'cosinus')),
            graf(WK, [kreis()] + A_FIG, ein=0.3),
            graf(WK, [S((0, -1.45), (0, 1.45), 5, 3, True)] + spiegelbild(t_y + 0.8, t_y + 2.6, (-A25[0], A25[1]), ein=t_y + 0.8), ein=t_y, raster=False, achsen=False)),
         sz('An der x-Achse', sp4['An der x-Achse'],
            f(r'\sin(-\alpha) = \fa{-\sin\alpha}', 300, 50, ein=w('An der x-Achse', 'sinus')),
            f(r'\cos(-\alpha) = \fc{\cos\alpha}', 420, 50, ein=w('An der x-Achse', 'cosinus')),
            f(r'-\alpha \ \text{und} \ 360^\circ - \alpha: \ \text{derselbe Punkt}', 540, 44, ein=w('An der x-Achse', 'dreihundertsechzig')),
            graf(WK, [kreis()] + A_FIG, ein=0.3),
            graf(WK, [S((-1.45, 0), (1.45, 0), 5, 3, True)] + spiegelbild(t_x + 0.4, t_x + 2.2, (A25[0], -A25[1]), ein=t_x + 0.4), ein=t_x, raster=False, achsen=False)),
         sz('Am Ursprung', sp4['Am Ursprung'],
            f(r'\sin(180^\circ + \alpha) = \fa{-\sin\alpha}', 280, 46, ein=w('Am Ursprung', 'beide')),
            f(r'\cos(180^\circ + \alpha) = \fc{-\cos\alpha}', 380, 46, ein=w('Am Ursprung', 'beide')),
            f(r'\tan(180^\circ + \alpha) = \fb{\tan\alpha}', 480, 46, ein=w('Am Ursprung', 'tangens')),
            graf(WK, [kreis()] + A_FIG, ein=0.3),
            graf(WK, [S((A25[0], A25[1]), (-A25[0], -A25[1]), 5, 3, True)] + spiegelbild(t_o + 0.6, t_o + 2.6, (-A25[0], -A25[1]), ein=t_o + 0.6), ein=t_o, raster=False, achsen=False)),
         sz('Komplement', sp4['Komplement'],
            f(r'\sin(90^\circ - \alpha) = \fc{\cos\alpha}', 280, 48, ein=w('Komplement', 'sinus')),
            f(r'\cos(90^\circ - \alpha) = \fa{\sin\alpha}', 380, 48, ein=w('Komplement', 'sinus')),
            f(r'\sin\left(\tfrac{\pi}{2} - \varphi\right) = \cos\varphi', 520, 50, ein=w('Komplement', 'bogenmass')),
            graf(WK, [kreis()] + A_FIG, ein=0.3),
            graf(WK, [S((-1.45, -1.45), (1.45, 1.45), 5, 3, True)] + spiegelbild(t_k + 0.6, t_k + 2.6, (A25[1], A25[0]), ein=t_k + 0.6), ein=t_k, raster=False, achsen=False)),
         sz('Anwenden', sp4['Anwenden'],
            f(r'\text{bekannt: } \fc{\cos 25^\circ} \approx 0.906', 280, 46, ein=w('Anwenden', 'cosinus')),
            f(r'\cos 205^\circ = \cos(180^\circ + 25^\circ)', 400, 48, ein=w('Anwenden', 'cosinus', 2)),
            f(r'= -\cos 25^\circ \approx \fc{-0.906}', 520, 50, ein=w('Anwenden', 'minus')),
            graf(WK, [kreis()] + A_FIG + [S((A25[0], A25[1]), (-A25[0], -A25[1]), 5, 3, True)]
                 + fest(205, ('radius', 'cos', 'sin', 'P', 'name'), name='B', farbe_p=2), ein=0.3)),
         sz('Merke', sp4['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('@y@-Achse: Cosinus kippt|@x@-Achse: Sinus kippt|Ursprung: beide kippen|@y = x@: Plätze tauschen', 380, 'blau', 42, ein=1.2),
            graf(WK, [kreis()] + A_FIG + [pkt(155, 2), pkt(-25, 2), pkt(205, 2), pkt(65, 2)]
                 + [T(r3(1.3 * cs(g)[0]), r3(1.3 * cs(g)[1] - 0.04), tx, 2, 'middle', 28, False)
                    for g, tx in ((155, '180°−α'), (-25, '−α'), (205, '180°+α'), (65, '90°−α'))], ein=0.3)),
         jetzt_du(),
     ], folge=7)

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
C = 'kontrolle-symmetrien'
SPK4 = [
    ('Frage 1', 'Hundertvierzig Grad ist hundertachtzig minus vierzig Grad. Die Spiegelung an der y-Achse lässt die Höhe gleich: '
                'Sinus hundertvierzig Grad ist ungefähr null Komma sechs vier drei.'),
    ('Frage 2', 'Minus siebzig Grad ist an der x-Achse gespiegelt. Die x-Koordinate bleibt: Cosinus von minus siebzig Grad ist '
                'Cosinus siebzig Grad.'),
    ('Frage 3', 'Hundertachtzig plus fünfzig Grad ist eine halbe Runde weiter als A. Der Punkt liegt A genau gegenüber, am '
                'Ursprung gespiegelt.'),
    ('Frage 4', 'Siebzig Grad ist neunzig minus zwanzig Grad. Beim Komplement tauschen Sinus und Cosinus die Plätze: Cosinus '
                'zwanzig Grad ist Sinus siebzig Grad.'),
    ('Frage 5', 'Zweihundertfünfzehn Grad ist hundertachtzig plus fünfunddreissig Grad. Sinus und Cosinus wechseln beide das '
                'Vorzeichen, ihr Quotient bleibt: ungefähr null Komma sieben.'),
    ('Merke', 'Zum Mitnehmen: Erst überlegen, an welcher Achse gespiegelt wird. Dann sieht man, welche Koordinate kippt.'),
]
merke_text(C, SPK4)
sk4 = dict(SPK4)


def AB(a, b, achse=None):
    fig = fest(a, ('radius', 'cos', 'sin', 'P', 'name'), name='A') + fest(b, ('radius', 'cos', 'sin', 'P', 'name'), name='B', farbe_p=2)
    if achse:
        fig = [S(*achse, 5, 3, True)] + fig
    return fig


clip(C, 'Einheitskreis sehen: Kontrollfragen zu den Symmetrien',
     'Fünf Fragen zu sin 140°, cos(−70°), zum Punkt bei 180° + 50°, zum Komplement von cos 20° und zu tan 215°.',
     ['Symmetrie', 'Komplement', 'Kontrollfragen'], [
         sz('Frage 1', sk4['Frage 1'],
            f(r'\fa{\sin 140^\circ} = \sin 40^\circ \approx 0.643', 300, 50, ein=1.0),
            graf(WK, [kreis()] + fest(40, ('radius', 'P', 'name'), name='A'), ein=0.05),
            graf(WK, AB(40, 140, ((0, -1.45), (0, 1.45))), ein=1.0, raster=False, achsen=False)),
         sz('Frage 2', sk4['Frage 2'],
            f(r'\fc{\cos(-70^\circ)} = \cos 70^\circ', 300, 54, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, AB(70, -70, ((-1.45, 0), (1.45, 0))), ein=1.0, raster=False, achsen=False)),
         sz('Frage 3', sk4['Frage 3'],
            f(r'180^\circ + 50^\circ = 230^\circ', 300, 54, ein=1.0),
            graf(WK, [kreis()] + fest(50, ('radius', 'P', 'name'), name='A'), ein=0.05),
            graf(WK, AB(50, 230, (cs(50), cs(230))), ein=1.0, raster=False, achsen=False)),
         sz('Frage 4', sk4['Frage 4'],
            f(r'\fc{\cos 20^\circ} = \sin(90^\circ - 20^\circ) = \sin 70^\circ', 300, 46, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, AB(20, 70, ((-1.45, -1.45), (1.45, 1.45))), ein=1.0, raster=False, achsen=False)),
         sz('Frage 5', sk4['Frage 5'],
            f(r'\fb{\tan 215^\circ} = \tan 35^\circ \approx 0.700', 300, 50, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, AB(35, 215, (cs(35), cs(215))), ein=1.0, raster=False, achsen=False)),
         sz('Merke', sk4['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('Spiegelachse finden|→ sehen, welche Koordinate kippt', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Es gilt sin 40° ≈ 0.643. Wie gross ist sin 140°?', ['≈ 0.643', '≈ −0.643', '≈ 0.766'], 0,
              {0: 'Ja.', 1: '140° = 180° − 40°: an der y-Achse gespiegelt. Ändert sich dabei die Höhe?',
               2: '0.766 ist cos 40°. Gefragt ist der Sinus, die Höhe.'},
              sprich='Es gilt: Sinus vierzig Grad ist ungefähr null Komma sechs vier drei. Wie gross ist Sinus hundertvierzig Grad?',
              rueck_sprich={1: 'Hundertvierzig Grad ist hundertachtzig minus vierzig Grad, an der y-Achse gespiegelt. Ändert sich dabei die Höhe?',
                            2: 'Null Komma sieben sechs sechs ist Cosinus vierzig Grad. Gefragt ist der Sinus, die Höhe.'}),
         wahl('Frage 2', 'Welcher Ausdruck ist gleich cos(−70°)?', ['cos 70°', '−cos 70°', 'sin 70°'], 0,
              {0: 'Ja.', 1: 'Spiegelung an der x-Achse: Ändert sich dabei die x-Koordinate?',
               2: 'Getauscht wird nur beim Komplement 90° − α.'},
              sprich='Welcher Ausdruck ist gleich Cosinus von minus siebzig Grad?',
              rueck_sprich={1: 'Spiegelung an der x-Achse. Ändert sich dabei die x-Koordinate?',
                            2: 'Getauscht wird nur beim Komplement, neunzig Grad minus alpha.'}),
         klick('Frage 3', 'A gehört zu 50°. Tipp den Punkt zu 180° + 50° auf den Kreis.', [round(cs(230)[0], 4), round(cs(230)[1], 4)],
               'Getroffen: A gegenüber.',
               [{'bei': [round(cs(130)[0], 4), round(cs(130)[1], 4)], 'text': 'Das ist 180° − 50°, an der y-Achse gespiegelt. 180° + 50° liegt A gegenüber.',
                 'sprich': 'Das ist hundertachtzig minus fünfzig Grad, an der y-Achse gespiegelt. Hundertachtzig plus fünfzig Grad liegt A gegenüber.'},
                {'bei': [round(cs(-50)[0], 4), round(cs(-50)[1], 4)], 'text': 'Das ist −50°, an der x-Achse gespiegelt.',
                 'sprich': 'Das ist minus fünfzig Grad, an der x-Achse gespiegelt.'},
                {'bei': [round(cs(40)[0], 4), round(cs(40)[1], 4)], 'text': 'Das ist 90° − 50°, an der Geraden y = x gespiegelt.',
                 'sprich': 'Das ist neunzig minus fünfzig Grad, an der Geraden y gleich x gespiegelt.'}],
               FALSCH, sprich='A gehört zu fünfzig Grad. Tipp den Punkt zu hundertachtzig plus fünfzig Grad auf den Kreis.', falsch_sprich=FALSCH),
         wahl('Frage 4', 'Welcher Wert ist gleich cos 20°?', ['sin 70°', 'sin 20°', '−sin 70°'], 0,
              {0: 'Ja.', 1: 'sin 20° ist die Höhe zu 20°. Beim Komplement 90° − 20° tauschen x und y die Plätze.',
               2: 'Beim Komplement kippt kein Vorzeichen.'},
              sprich='Welcher Wert ist gleich Cosinus zwanzig Grad?',
              rueck_sprich={1: 'Sinus zwanzig Grad ist die Höhe zu zwanzig Grad. Beim Komplement, neunzig minus zwanzig Grad, tauschen x und y die Plätze.',
                            2: 'Beim Komplement kippt kein Vorzeichen.'}),
         wahl('Frage 5', 'Es gilt tan 35° ≈ 0.700. Wie gross ist tan 215°?', ['≈ 0.700', '≈ −0.700', 'nicht definiert'], 0,
              {0: 'Ja.', 1: '215° = 180° + 35°: am Ursprung gespiegelt. Beide Koordinaten kippen — und ihr Quotient?',
               2: 'Zwischen 0° und 360° ist der Tangens nur bei 90° und 270° nicht definiert.'},
              sprich='Es gilt: Tangens fünfunddreissig Grad ist ungefähr null Komma sieben. Wie gross ist Tangens zweihundertfünfzehn Grad?',
              rueck_sprich={1: 'Zweihundertfünfzehn Grad ist hundertachtzig plus fünfunddreissig Grad, am Ursprung gespiegelt. Beide Koordinaten kippen. Und ihr Quotient?',
                            2: 'Zwischen null und dreihundertsechzig Grad ist der Tangens nur bei neunzig und zweihundertsiebzig Grad nicht definiert.'}),
     ], art='Kontrollclip', folge=8)

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
C = 'periode-umkehr'
SP5 = [
    ('Eine volle Runde', 'Dreht P eine volle Runde weiter, ist er wieder am selben Ort. Dreihundertneunzig Grad gibt denselben '
                         'Punkt wie dreissig Grad. Sinus und Cosinus wiederholen sich nach dreihundertsechzig Grad.'),
    ('Halbe Runde', 'Beim Tangens genügt eine halbe Runde. Der Punkt zu zweihundertzehn Grad liegt P gegenüber, auf derselben '
                    'Geraden durch O. Sie trifft die Tangente im selben Punkt S. Der Tangens wiederholt sich nach hundertachtzig Grad.'),
    ('Rückwärts', 'Jetzt rückwärts: Welcher Winkel hat den Sinus null Komma vier? Die Waagrechte in der Höhe null Komma vier '
                  'trifft den Kreis in zwei Punkten. Der Taschenrechner gibt mit Sinus hoch minus eins von null Komma vier nur '
                  'einen Winkel aus: dreiundzwanzig Komma sechs Grad.'),
    ('Hauptwert', 'Warum gerade diesen? Der Arkussinus liefert immer einen Winkel aus der rechten Kreishälfte, von minus neunzig '
                  'bis neunzig Grad: den Hauptwert. Der zweite Punkt liegt links, und dazu kommen alle Winkel, die volle Runden '
                  'daneben liegen.'),
    ('Arkuscosinus', 'Beim Cosinus ist es die obere Hälfte: Der Arkuscosinus liefert Winkel von null bis hundertachtzig Grad. '
                     'Zu minus null Komma drei gibt der Rechner hundertsieben Komma fünf Grad. Der Arkustangens liefert wie der '
                     'Arkussinus die rechte Hälfte, aber ohne die Endpunkte bei plus und minus neunzig Grad.'),
    ('Merke', 'Zum Mitnehmen: Sinus und Cosinus wiederholen sich nach dreihundertsechzig Grad, der Tangens nach hundertachtzig. '
              'Zu einem Wert gibt es viele Winkel. Der Rechner liefert nur den Hauptwert.'),
]
merke_text(C, SP5)
w = lambda s, wort, nr=1, dazu=0.0: wann(C, s, wort, nr, dazu)
sp5 = dict(SP5)
t_runde = w('Eine volle Runde', 'runde')
L_390 = Lauf([[0, 30], [t_runde - 0.4, 30], [t_runde + 2.6, 390]])
t_gegen = w('Halbe Runde', 'gegenüber')
L_210 = Lauf([[0, 30], [t_gegen - 1.4, 30], [t_gegen + 0.6, 210]])
P1 = math.degrees(math.asin(0.4))                    # 23.578°
P2 = 180 - P1                                        # 156.422°
PC = math.degrees(math.acos(-0.3))                   # 107.458°


def band(von, bis, farbe, ein=None, aus=None):
    """Hauptwertbereich als breiter, blasser Bogen auf dem Kreis."""
    return mit(dict(art='bogen', m=[0, 0], r=1, von=von, bis=bis, farbe=farbe, dicke=22, deckkraft=0.25), ein=ein, aus=aus)


clip(C, 'Einheitskreis sehen: Periode und Umkehroperationen',
     'Nach 360° derselbe Punkt, beim Tangens schon nach 180°; vom Wert zurück zum Winkel mit sin⁻¹, cos⁻¹, tan⁻¹ und warum der '
     'Rechner nur den Hauptwert liefert.',
     ['Periode', 'Umkehroperation', 'Arkussinus', 'Hauptwert', 'Taschenrechner'], [
         sz('Eine volle Runde', sp5['Eine volle Runde'],
            f(r'\fa{\sin(\varphi + 360^\circ)} = \fa{\sin\varphi}', 280, 50, ein=w('Eine volle Runde', 'sinus')),
            f(r'\fc{\cos(\varphi + 360^\circ)} = \fc{\cos\varphi}', 380, 50, ein=w('Eine volle Runde', 'sinus')),
            n('allgemein @+ k \\cdot 360^\\circ@, @k \\in \\mathbb{Z}@', 500, 'blau', 42, ein=w('Eine volle Runde', 'wiederholen')),
            graf(WK, [kreis()] + P_teile(L_390, ('winkel', 'radius', 'cos', 'sin', 'P', 'name')), ein=0.3)),
         sz('Halbe Runde', sp5['Halbe Runde'],
            f(r'\fb{\tan(\varphi + 180^\circ)} = \fb{\tan\varphi}', 330, 52, ein=w('Halbe Runde', 'wiederholt')),
            graf(WT, WT_FIG(Lauf([[0, 30]])) + fest(30, ('radius', 'P', 'name'), name_dw=14)
                 + [mit(t_, ein=t_gegen - 1.4) for t_ in P_teile(L_210, ('radius', 'P'), farbe_p=2)]
                 + [S((r3(cs(210)[0]), r3(cs(210)[1])), (0, 0), 5, 3, True, ein=t_gegen + 0.6)], ein=0.3)),
         sz('Rückwärts', sp5['Rückwärts'],
            f(r'\fa{\sin\varphi = 0.4}', 280, 54, ein=0.6),
            f(r'\sin^{-1}(0.4) \approx 23.6^\circ', 420, 54, ein=w('Rückwärts', 'dreiundzwanzig')),
            graf(WK, [kreis()], ein=0.3),
            graf(WK, [S((-1.45, 0.4), (1.45, 0.4), 5, 3, True), T(1.42, 0.47, 'y = 0.4', 5, 'end', 28, False)],
                 ein=w('Rückwärts', 'waagrechte'), raster=False, achsen=False),
            graf(WK, [pkt(P1, 1, 0.045), pkt(P2, 5, 0.045, hohl=True)], ein=w('Rückwärts', 'zwei'), raster=False, achsen=False),
            graf(WK, fest(P1, ('winkel', 'radius', 'P'), name='') + [T(0.55, 0.07, '23.6°', 5, 'start', 26, False)],
                 ein=w('Rückwärts', 'dreiundzwanzig'), raster=False, achsen=False)),
         sz('Hauptwert', sp5['Hauptwert'],
            f(r'\arcsin w \in [-90^\circ;\, 90^\circ]', 300, 52, ein=w('Hauptwert', 'rechten')),
            n('der zweite Punkt: links|und alle vollen Runden daneben', 440, 'blau', 42, ein=w('Hauptwert', 'zweite')),
            graf(WK, [kreis(), S((-1.45, 0.4), (1.45, 0.4), 5, 3, True), pkt(P2, 5, 0.045, hohl=True)] + fest(P1, ('winkel', 'radius', 'P'), name=''), ein=0.3),
            graf(WK, [band(-90, 90, 1)], ein=w('Hauptwert', 'rechten'), raster=False, achsen=False)),
         sz('Arkuscosinus', sp5['Arkuscosinus'],
            f(r'\arccos w \in [0^\circ;\, 180^\circ]', 260, 50, ein=w('Arkuscosinus', 'liefert')),
            f(r'\cos^{-1}(-0.3) \approx 107.5^\circ', 380, 50, ein=w('Arkuscosinus', 'hundertsieben')),
            f(r'\arctan w \in \,]{-90^\circ};\, 90^\circ[', 520, 50, ein=w('Arkuscosinus', 'tangens')),
            graf(WK, [kreis(), band(0, 180, 3), S((-0.3, -1.45), (-0.3, 1.45), 5, 3, True), T(-0.33, -1.38, 'x = −0.3', 5, 'end', 28, False)],
                 ein=0.3, aus=w('Arkuscosinus', 'tangens')),
            graf(WK, fest(PC, ('winkel', 'radius', 'P'), name='') + [pkt(-PC, 5, 0.045, hohl=True)], ein=w('Arkuscosinus', 'hundertsieben'),
                 raster=False, achsen=False, aus=w('Arkuscosinus', 'tangens')),
            graf(WK, [kreis(), band(-89, 89, 2), pkt(90, 2, 0.045, hohl=True), pkt(-90, 2, 0.045, hohl=True)], ein=w('Arkuscosinus', 'tangens'))),
         sz('Merke', sp5['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('Periode: @360^\\circ@ für @\\sin@ und @\\cos@, @180^\\circ@ für @\\tan@|Der Rechner liefert nur den Hauptwert.', 400, 'blau', 42, ein=1.2),
            graf(WK, [kreis(), band(-90, 90, 1), S((-1.45, 0.4), (1.45, 0.4), 5, 3, True), pkt(P2, 5, 0.045, hohl=True)] + fest(P1, ('winkel', 'radius', 'P'), name=''), ein=0.3)),
         jetzt_du(),
     ], folge=9)

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
C = 'kontrolle-periode-umkehr'
SPK5 = [
    ('Frage 1', 'Vierhundert Grad ist eine volle Runde und noch vierzig Grad. P liegt am selben Ort wie bei vierzig Grad.'),
    ('Frage 2', 'Minus hundertzwanzig Grad plus dreihundertsechzig Grad sind zweihundertvierzig Grad. Derselbe Punkt, im dritten '
                'Quadranten.'),
    ('Frage 3', 'Dreihundertdreissig Grad minus hundertachtzig Grad ergibt hundertfünfzig Grad. Der Punkt zu hundertfünfzig Grad '
                'liegt gegenüber, auf derselben Geraden durch O. Darum haben beide denselben Tangens.'),
    ('Frage 4', 'Die Senkrechte bei x gleich null Komma sechs trifft den Kreis ein zweites Mal, unten rechts. Diesen Punkt liefert '
                'der Rechner nicht, er liegt nicht in der oberen Hälfte.'),
    ('Frage 5', 'Zu null Komma vier gibt es viele Winkel: zwei Punkte am Kreis und dazu alle vollen Runden. Der Rechner nimmt den '
                'aus der rechten Hälfte, den Hauptwert.'),
    ('Merke', 'Zum Mitnehmen: Volle Runden ändern den Punkt nicht. Und der Winkel des Rechners ist nur einer von vielen.'),
]
merke_text(C, SPK5)
sk5 = dict(SPK5)
C06 = math.degrees(math.acos(0.6))                   # 53.13°
clip(C, 'Einheitskreis sehen: Kontrollfragen zu Periode und Umkehrung',
     'Fünf Fragen zu 400°, zu −120°, zur Periode des Tangens bei 330°, zum zweiten Punkt mit cos φ = 0.6 und zum Grund, warum der Rechner nur einen Winkel liefert.',
     ['Periode', 'Umkehroperation', 'Hauptwert', 'Kontrollfragen'], [
         sz('Frage 1', sk5['Frage 1'],
            f(r'400^\circ - 360^\circ = 40^\circ', 300, 54, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, P_teile(Lauf([[1.2, 0], [3.4, 400]]), ('winkel', 'radius', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Frage 2', sk5['Frage 2'],
            f(r'-120^\circ + 360^\circ = 240^\circ', 300, 54, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, P_teile(Lauf([[1.2, 0], [2.8, -120]]), ('winkel', 'radius', 'P', 'name')), ein=1.0, raster=False, achsen=False)),
         sz('Frage 3', sk5['Frage 3'],
            f(r'330^\circ - 180^\circ = 150^\circ', 300, 54, ein=1.0),
            f(r'\fb{\tan 150^\circ} = \fb{\tan 330^\circ}', 420, 50, ein=1.0),
            graf(WT, [kreis(), S((1, -1.7), (1, 1.7), 5, 3)] + fest(330, ('radius', 'P'), name='')
                 + [T(0.7, -0.66, '330°', 5, 'end', 28, False)], ein=0.05),
            graf(WT, tan_teile(Lauf([[0, 150]]))[1:] + fest(150, ('radius', 'P'), name='', farbe_p=2)
                 + [T(-0.95, 0.64, '150°', 2, 'end', 28, False)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 4', sk5['Frage 4'],
            f(r'\fc{\cos\varphi = 0.6}: \ (0.6 \mid 0.8) \ \text{und} \ (0.6 \mid -0.8)', 300, 44, ein=1.0),
            graf(WK, [kreis()] + fest(C06, ('winkel', 'radius', 'P'), name='') + [T(0.68, 0.92, '53.1°', 5, 'start', 28, False)], ein=0.05),
            graf(WK, [S((0.6, -1.45), (0.6, 1.45), 5, 3, True), band(0, 180, 3), pkt(-C06, 3, 0.05)], ein=1.0, raster=False, achsen=False)),
         sz('Frage 5', sk5['Frage 5'],
            f(r'\sin^{-1}(0.4) \approx 23.6^\circ \ \text{— der Hauptwert}', 300, 46, ein=1.0),
            graf(WK, [kreis()], ein=0.05),
            graf(WK, [band(-90, 90, 1), S((-1.45, 0.4), (1.45, 0.4), 5, 3, True), pkt(P2, 5, 0.045, hohl=True)] + fest(P1, ('radius', 'P'), name=''),
                 ein=1.0, raster=False, achsen=False)),
         sz('Merke', sk5['Merke'],
            titel('Zum Mitnehmen', 250, 76),
            n('volle Runden: derselbe Punkt|der Rechner: ein Winkel von vielen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Welcher Winkel zwischen 0° und 360° hat denselben Punkt P wie 400°?', ['40°', '220°', '140°'], 0,
              {0: 'Ja.', 1: '220° ist 400° − 180°: eine halbe Runde zurück, P läge gegenüber.',
               2: '400° ist eine volle Runde und noch etwas. Wie viel?'},
              sprich='Welcher Winkel zwischen null und dreihundertsechzig Grad hat denselben Punkt P wie vierhundert Grad?',
              rueck_sprich={1: 'Zweihundertzwanzig Grad ist vierhundert minus hundertachtzig Grad: eine halbe Runde zurück, P läge gegenüber.',
                            2: 'Vierhundert Grad ist eine volle Runde und noch etwas. Wie viel?'}),
         wahl('Frage 2', 'Derselbe Punkt wie bei −120°: Welcher Winkel zwischen 0° und 360° ist das?', ['240°', '120°', '60°'], 0,
              {0: 'Ja.', 1: '120° dreht gegen den Uhrzeigersinn, −120° im Uhrzeigersinn. Zähl 360° dazu.',
               2: 'Zähl 360° dazu: −120° + 360°.'},
              sprich='Derselbe Punkt wie bei minus hundertzwanzig Grad: Welcher Winkel zwischen null und dreihundertsechzig Grad ist das?',
              rueck_sprich={1: 'Hundertzwanzig Grad dreht gegen den Uhrzeigersinn, minus hundertzwanzig Grad im Uhrzeigersinn. Zähl dreihundertsechzig Grad dazu.',
                            2: 'Zähl dreihundertsechzig Grad dazu: minus hundertzwanzig plus dreihundertsechzig.'}),
         # Prüfung 08.10.2026 (M1): Frage 2 und die alte Frage 3 (sin⁻¹(−0.5) = −30° → 330°) prüften beide «+ 360°».
         # Jetzt die Periode des Tangens, die sonst keine Kontrollfrage prüft.
         wahl('Frage 3', 'Gleicher Tangens wie 330°: Welcher Winkel zwischen 0° und 180° ist das?',
              ['150°', '30°', 'keiner, der Tangens wiederholt sich erst nach 360°'], 0,
              {0: 'Ja.', 1: 'tan 30° ist positiv, tan 330° negativ. Der Punkt gegenüber liegt eine halbe Runde weiter: 330° − 180°.',
               2: 'Der Punkt gegenüber liegt auf derselben Geraden durch O. Der Tangens wiederholt sich schon nach 180°.'},
              sprich='Gleicher Tangens wie dreihundertdreissig Grad: Welcher Winkel zwischen null und hundertachtzig Grad ist das?',
              rueck_sprich={1: 'Tangens dreissig Grad ist positiv, Tangens dreihundertdreissig Grad negativ. Der Punkt gegenüber liegt eine halbe Runde weiter: dreihundertdreissig minus hundertachtzig Grad.',
                            2: 'Der Punkt gegenüber liegt auf derselben Geraden durch O. Der Tangens wiederholt sich schon nach hundertachtzig Grad.'}),
         klick('Frage 4', 'Der Rechner gibt cos⁻¹(0.6) ≈ 53.1°. Tipp den zweiten Kreispunkt mit cos φ = 0.6 an.', [0.6, -0.8],
               'Getroffen: unten rechts.',
               [{'bei': [-0.6, 0.8], 'text': 'Hier ist cos φ = −0.6. Gesucht ist dieselbe x-Koordinate 0.6.',
                 'sprich': 'Hier ist Cosinus phi gleich minus null Komma sechs. Gesucht ist dieselbe x-Koordinate, null Komma sechs.'},
                {'bei': [0.8, 0.6], 'text': 'Hier ist sin φ = 0.6. Der Cosinus ist die x-Koordinate.',
                 'sprich': 'Hier ist Sinus phi gleich null Komma sechs. Der Cosinus ist die x-Koordinate.'},
                {'bei': [0.6, 0.8], 'text': 'Das ist der Punkt des Rechners, 53.1°. Wo ist die x-Koordinate noch 0.6?',
                 'sprich': 'Das ist der Punkt des Rechners, dreiundfünfzig Komma eins Grad. Wo ist die x-Koordinate noch null Komma sechs?'}],
               FALSCH, sprich='Der Rechner gibt Cosinus hoch minus eins von null Komma sechs, ungefähr dreiundfünfzig Komma eins Grad. Tipp den zweiten Kreispunkt mit Cosinus phi gleich null Komma sechs an.',
               falsch_sprich=FALSCH),
         wahl('Frage 5', 'Warum liefert der Rechner zu sin φ = 0.4 nur einen Winkel?',
              ['Er gibt nur den Hauptwert aus.', 'Es gibt nur einen Winkel mit diesem Sinus.', 'Der zweite Winkel ist negativ.'], 0,
              {0: 'Ja.', 1: 'Die Waagrechte y = 0.4 trifft den Kreis zweimal, und nach jeder vollen Runde wieder.',
               2: 'Das ist nicht der Grund: Negative Winkel liefert der Rechner auch. Der zweite Kreispunkt liegt links, nicht in der rechten Hälfte.'},
              sprich='Warum liefert der Rechner zu Sinus phi gleich null Komma vier nur einen Winkel?',
              rueck_sprich={1: 'Die Waagrechte y gleich null Komma vier trifft den Kreis zweimal, und nach jeder vollen Runde wieder.',
                            2: 'Das ist nicht der Grund. Negative Winkel liefert der Rechner auch. Der zweite Kreispunkt liegt links, nicht in der rechten Hälfte.'}),
     ], art='Kontrollclip', folge=10)

if FEHLT and WZ:
    print('Ohne gemessene Wortzeit (geschätzt):', sorted(set(FEHLT)))
