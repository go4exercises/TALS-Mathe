"""Erzeugt die acht Drehbücher des Leitprogramms Zentrische Streckung und Ähnlichkeit (08.10.2026).

  python3 scripts/lp/aehnlichkeit/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich); nur für Szenen mit neuem
Text muss danach build-clip-ton.py laufen. Bewegungen und `ein` stehen auf den gemessenen Wortzeiten
(.claude/tools/sprechzeiten.py); nach einer Änderung hier das Skript laufen lassen und nur neu bauen.

Aufbau wie in den Leitprogrammen Planimetrie und Trigonometrische Berechnungen: Rechnung und Notizen links (x 150),
die Figur rechts (x 1010, y 175, 760 × 760). Figuren zeichnet `graf` mit "figuren"; das Fenster ist in x und y gleich
geteilt (sonst würden Kreise zu Ellipsen und rechte Winkel schief). Kapitel 1 steht im Koordinatennetz (Achsen mit
Pfeil), die übrigen ohne Achsen.

Fragebild (HOWTO-leitprogramme §15): Die Kontrollclips zeigen beim Erscheinen einer Frage nur das Gegebene;
Rechnung und Auflösung erscheinen ab 1.0 s (nach der Antwort). Gebaut wie in den Geometrie-Leitprogrammen von Hand
(je Szene ein Graf mit dem Gegebenen ab 0.05 s, ein zweiter mit der Auflösung ab 1.0 s) — scripts/lp/fragebild.py
ist für Kurven-Clips gemacht und wird hier nicht gebraucht.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite und der Themenseite:
  1 blau   = Original, Figur                                  \\fa{…}
  2 orange = Bild, Streckfaktor k, Hilfslinie                   \\fb{…}
  3 grün   = Gesuchtes, Ergebnis                                \\fc{…}
  4 rot    = Fehler, Gegenbeispiel                              \\fd{…}
  5 Tinte  = neutral (Zentrum, Strahlen, Beschriftung)
Alle Zahlen mit python3 nachgerechnet (hier im Skript und in zahlen.py).
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-2d-lp-'


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def richtung(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def plus(p, q, s=1):
    return (p[0] + s * q[0], p[1] + s * q[1])


def strecke_bild(Z, P, k):
    return (Z[0] + k * (P[0] - Z[0]), Z[1] + k * (P[1] - Z[1]))


# ---------------------------------------------------------------- Fenster und Figuren
def geo(x0, y0, span, hoehe=None):
    """Ohne Achsen, gleich geteilt; hoehe (Bildpixel) für ein flaches Fenster."""
    yspan = span if hoehe is None else span * hoehe / GB
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, round(y0 + yspan, 3)], achsen=False)


def ach(x0, y0, span, teil=2):
    """Mit Achsen und Teilung (Kapitel 1: Koordinaten), gleich geteilt."""
    xt = [w for w in range(math.ceil(x0), int(x0 + span) + 1) if w % teil == 0 and w != 0]
    yt = [w for w in range(math.ceil(y0), int(y0 + span) + 1) if w % teil == 0 and w != 0]
    t = lambda ws: [[w, str(w).replace('-', '−')] for w in ws]
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], xteilung=t(xt), yteilung=t(yt))


def V(pkte, farbe=1, fu=0.12, **kw):
    return dict(art='vieleck', punkte=[r3(p) for p in pkte], farbe=farbe, fuellung=fu, **kw)


def S(a, b, farbe=2, gest=False, dicke=4, **kw):
    d = dict(art='strecke', von=r3(a), bis=r3(b), farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def G(a, b, W, farbe=5, gest=True, dicke=2, **kw):
    """Ganze Gerade durch a und b, am Fenster W abgeschnitten (für Strahlen)."""
    (x0, x1), (y0, y1) = W['xbereich'], W['ybereich']
    dx, dy = b[0] - a[0], b[1] - a[1]
    ts = []
    for t_ in ([(x0 - a[0]) / dx, (x1 - a[0]) / dx] if dx else []) + ([(y0 - a[1]) / dy, (y1 - a[1]) / dy] if dy else []):
        p = (a[0] + t_ * dx, a[1] + t_ * dy)
        if x0 - 1e-9 <= p[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] <= y1 + 1e-9:
            ts.append(t_)
    return S((a[0] + min(ts) * dx, a[1] + min(ts) * dy), (a[0] + max(ts) * dx, a[1] + max(ts) * dy), farbe, gest, dicke, **kw)


def T(x, y, text, farbe=5, anker='middle', g=30, kursiv=False, **kw):
    return dict(art='text', bei=[round(x, 3), round(y, 3)], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=kursiv, **kw)


def RW(p, r1, r2, farbe=5, **kw):
    return dict(art='rechts', bei=r3(p), r1=r1, r2=r2, farbe=farbe, **kw)


def WI(p, a, b, farbe=2, r=44, **kw):
    """Winkel bei p von der Richtung zu a bis zur Richtung zu b (der kleinere Bogen)."""
    w0, w1 = richtung(p, a), richtung(p, b)
    if (w1 - w0) % 360 > 180:
        w0, w1 = w1, w0
    if w1 < w0:
        w1 += 360
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def KR(m, r, farbe=5, fu=0.0, **kw):
    return dict(art='kreis', m=r3(m), r=round(r, 3), farbe=farbe, fuellung=fu, **kw)


def PK(p, farbe=5, r=0.09):
    return KR(p, r, farbe, 1)


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def graf(W, figuren=(), punkte=(), ein=0.05, x=GX, y=GY, breite=GB, hoehe=GH, **kw):
    g = dict(typ='graf', x=x, y=y, breite=breite, hoehe=hoehe, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def pt(p, farbe=5, **kw):
    return dict(x=round(p[0], 3), y=round(p[1], 3), farbe=farbe, anker='start', **kw)


def ecken(namen_pkte, farbe=5, abst=0.45, mitte=None, g=30):
    """Eckennamen vom Schwerpunkt (oder mitte) weg."""
    pk = [p for _, p in namen_pkte]
    m = mitte or (sum(p[0] for p in pk) / len(pk), sum(p[1] for p in pk) / len(pk))
    aus = []
    for name, p in namen_pkte:
        d = (p[0] - m[0], p[1] - m[1]); l_ = math.hypot(*d) or 1
        aus.append(T(p[0] + d[0] / l_ * abst, p[1] + d[1] / l_ * abst - 0.12 * g / 30, name, farbe, g=g))
    return aus


def seitentext(p, q, text, weg, farbe=5, abst=0.45, g=28):
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    n_ = (-(q[1] - p[1]), q[0] - p[0]); l_ = math.hypot(*n_); n_ = (n_[0] / l_, n_[1] / l_)
    if n_[0] * (weg[0] - m[0]) + n_[1] * (weg[1] - m[1]) > 0:
        n_ = (-n_[0], -n_[1])
    return T(m[0] + n_[0] * abst, m[1] + n_[1] * abst - 0.1, text, farbe, g=g)


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
        d['eingabe'] = eingabe       # nur wo Achsen die Koordinaten ablesbar machen (Kapitel 1)
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'
FALSCH_LINIE = 'Nicht ganz. Die grüne Linie zeigt die Seite.'      # Ziel als Strecke: der Abspieler zieht sie grün nach


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(alt):
        szalt = json.load(open(alt))['szenen']
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in szalt}
        nach_name = {q['name']: q.get('dauer') for q in szalt}
        for nr, q in enumerate(szenen, 1):
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
            elif nach_name.get(q['name']):
                # Text geändert: alte Dauer behalten, damit build-clip-ton.py --szenen die bisherige Spur
                # noch zuordnen kann; die Szene muss neu vertont werden (misst die Dauer neu).
                q['dauer'] = nach_name[q['name']]
                print('  ! %s Szene %d «%s»: Text geändert — build-clip-ton.py %s --szenen %d' % (name, nr, q['name'], PRAEFIX + name, nr))
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Planimetrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-2d'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Ähnlichkeit sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms aehnlichkeit; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# Wie Arbeitsbereich 1: Z(1|1), A(2|3), B(3|1), C(5|4); k = 1.5 (Startwert), dann 0.5 und −1.5.
W1 = ach(-6.5, -5, 15)
Z1 = (1, 1)
E1 = [(2, 3), (3, 1), (5, 4)]
def bild1(k):
    return [strecke_bild(Z1, p, k) for p in E1]
B15, B05, Bm15 = bild1(1.5), bild1(0.5), bild1(-1.5)
# C′ bei k = 1.5: Weg Z → C = (4 | 3), mal 1.5 = (6 | 4.5), C′ = (7 | 5.5)
assert B15[2] == (7, 5.5) and B05[2] == (3, 2.5) and Bm15[2] == (-5, -3.5)
ORIG1 = [V(E1, 1, 0.14)] + ecken([('A', E1[0]), ('B', E1[1]), ('C', E1[2])], 1)
# Bild bei k = −1.5: A′(−0.5 | −2) liegt knapp links der y-Achse — der Name vom Schwerpunkt weg käme auf die
# Achsenzahl «−2» (bei x ≈ −0.3). Darum rechts unterhalb der Ecke, weg von Achse und Strahl ZA (bei y = −2.6: x = −0.8).
ECKEN_M15 = ecken([("A′", Bm15[0]), ("B′", Bm15[1]), ("C′", Bm15[2])], 2)
ECKEN_M15[0]['bei'] = [0.6, -2.62]
ZPT = [PK(Z1, 5, 0.12), T(0.55, 1.45, 'Z', 5, g=32)]
STRAHLEN1 = [G(Z1, p, W1, 5, True, 2) for p in E1]
def bildfig(pk, farbe=2, **kw):
    return V(pk, farbe, 0.12, gestrichelt=True, **kw)

clip('streckung', 1, 'Ähnlichkeit sehen: zentrische Streckung',
     'Zentrische Streckung mit Zentrum Z und Faktor k: Bildpunkt auf der Geraden durch Z, Abstand mal |k|; mit Koordinaten '
     '(Weg von Z mal k); 0 < k < 1 verkleinert, k < 0 auf die andere Seite; Winkel bleiben, Bildseiten parallel.',
     ['zentrische Streckung', 'Streckfaktor', 'Streckungszentrum', 'Koordinaten'], [
         sz('Zentrum und Faktor',
            'Eine zentrische Streckung braucht ein Zentrum Z und einen Streckfaktor k. Jeder Punkt wandert auf der Geraden '
            'durch Z und diesen Punkt, hier durch C.',
            f(r'\text{Zentrum } Z, \quad \text{Streckfaktor } \fb{k}', 300, 52, ein=0.4),
            f(r"C' \text{ liegt auf der Geraden } ZC", 420, 48, ein=5.3),
            graf(W1, ORIG1 + ZPT, ein=0.3),
            graf(W1, [G(Z1, E1[2], W1, 5, True, 2)], ein=6.4, raster=False)),
         sz('k gleich 1.5',
            'Mit k gleich eins Komma fünf wird der Abstand zu Z eins Komma fünf mal so gross. So wandern alle drei Ecken, '
            'und es entsteht das Bilddreieck.',
            f(r"\overline{ZC'} = |\fb{k}| \cdot \overline{ZC}", 300, 52, ein=0.4),
            f(r'\fb{k = 1.5}', 420, 52, ein=1.0),
            graf(W1, ORIG1 + ZPT + STRAHLEN1, ein=0.05),
            # das Bild wächst von k = 1 (deckungsgleich) bis k = 1.5 — Punkte linear in k; auf «So wandern alle drei
            # Ecken» (4.8 s, gemessen), nicht schon während «wird der Abstand …»
            graf(W1, [bildfig(E1, bewegung=[[4.8, {}], [6.8, {'punkte': [r3(p) for p in B15]}]])], ein=4.7, raster=False),
            graf(W1, ecken([("A′", B15[0]), ("B′", B15[1]), ("C′", B15[2])], 2), ein=7.1, raster=False)),
         sz('Mit Koordinaten',
            'Mit Koordinaten: Von Z nach C sind es vier nach rechts und drei nach oben. Mal eins Komma fünf gibt sechs und '
            'vier Komma fünf. Von Z aus abgetragen, liegt C Strich bei sieben und fünf Komma fünf.',
            f(r'Z \to C: \; 4 \text{ nach rechts}, \; 3 \text{ nach oben}', 300, 44, ein=1.9),
            f(r'\cdot\, \fb{1.5}: \; 6 \text{ und } 4.5', 410, 44, ein=5.2),
            f(r"C' = (1 + 6 \mid 1 + 4.5) = \fc{(7 \mid 5.5)}", 520, 46, ein=9.4),
            graf(W1, ORIG1 + ZPT + [bildfig(B15)] + ecken([("C′", B15[2])], 2), ein=0.05),
            graf(W1, [], ein=1.9, raster=False, strecken=[
                dict(von=[1, 1], bis=[5, 1], farbe=5, pfeil=True, dicke=4), dict(von=[5, 1], bis=[5, 4], farbe=5, pfeil=True, dicke=4)]),
            # mal 1.5: 6 nach rechts, 4.5 nach oben — von Z aus, genau bis C′ (der Weg 4 | 3 liegt darunter)
            graf(W1, [], ein=5.2, raster=False, strecken=[
                dict(von=[1, 1], bis=[7, 1], farbe=2, pfeil=True, dicke=5), dict(von=[7, 1], bis=[7, 5.5], farbe=2, pfeil=True, dicke=5)]),
            graf(W1, [PK(B15[2], 3, 0.16)], ein=9.4, raster=False)),
         sz('Kleiner',
            'Liegt k zwischen null und eins, wird das Bild kleiner. Bei k gleich null Komma fünf liegt jede Ecke nur halb so '
            'weit von Z entfernt.',
            # Zeiten gemessen (Neuvertonung 08.10.2026): «wird das Bild kleiner» 2.3 s, «Bei k gleich null Komma fünf» 3.7 s,
            # «liegt jede Ecke nur halb so weit» 5.2–7.2 s
            f(r'\fb{k = 0.5}', 300, 52, ein=3.8),
            n('@0 \\lt k \\lt 1@: verkleinert', 420, 'blau', 44, ein=2.3),
            graf(W1, ORIG1 + ZPT + STRAHLEN1, ein=0.05),
            graf(W1, [bildfig(B15, bewegung=[[4.6, {}], [6.8, {'punkte': [r3(p) for p in B05]}]])], ein=0.05, raster=False)),
         sz('Negativ',
            'Ist k negativ, liegt das Bild auf der anderen Seite von Z. Bei k gleich minus eins Komma fünf sind seine Seiten '
            'eins Komma fünf mal so lang, und es ist um Z gedreht.',
            f(r'\fb{k = -1.5}', 300, 52, ein=4.4),
            n('@k \\lt 0@: andere Seite von @Z@,|um @Z@ um @180°@ gedreht', 420, 'blau', 42, ein=8.4),   # «und es ist um Z gedreht» 8.3 s
            graf(W1, ORIG1 + ZPT + STRAHLEN1, ein=0.05),
            # k läuft von 0.5 über 0 (das Bild schrumpft in Z) bis −1.5, linear in k
            graf(W1, [bildfig(B05, bewegung=[[2.0, {}], [5.2, {'punkte': [r3(p) for p in Bm15]}]])], ein=0.05, raster=False),
            graf(W1, ECKEN_M15, ein=5.3, raster=False)),
         sz('Was bleibt',
            'Die Winkel bleiben gleich, und jede Bildseite ist parallel zu ihrer Originalseite. Jede Länge wird mit dem Betrag '
            'von k multipliziert. Darum hat das Bild dieselbe Form wie das Original.',
            n('Winkel gleich|Bildseite parallel zur Originalseite|Längen @\\cdot\\, |k|@', 300, 'blau', 44, ein=0.6),
            graf(W1, ORIG1 + ZPT + [bildfig(Bm15)] + ECKEN_M15, ein=0.05),
            graf(W1, [WI(E1[0], E1[1], E1[2], 1, 40), WI(Bm15[0], Bm15[1], Bm15[2], 2, 40)], ein=0.8, raster=False),
            graf(W1, [S(E1[0], E1[1], 1, dicke=9), S(Bm15[0], Bm15[1], 2, dicke=9)], ein=3.2, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Der Bildpunkt liegt auf der Geraden durch Z und den Punkt, sein Abstand zu Z ist der Betrag von k '
            'mal so gross. Bei negativem k liegt er auf der anderen Seite.',
            titel('Zum Mitnehmen', 250, 76),
            n("@P'@ auf der Geraden @ZP@|@\\overline{ZP'} = |k| \\cdot \\overline{ZP}@|@k \\lt 0@: andere Seite von @Z@", 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
# Frage 1: Z(−1|0), P(1|1), k = −2: Weg (2 | 1), mal −2 = (−4 | −2), P′(−5 | −2).
WK1 = ach(-6.5, -4.5, 10)
ZK1, PK1 = (-1, 0), (1, 1)
PK1b = strecke_bild(ZK1, PK1, -2)
assert PK1b == (-5, -2)
# Frage 5: Z(0|1), k = 2: A(2|0) → A′(4|−1), B(3|2) → B′(6|3), C(1.5|2.5) → C′(3|4).
WK5 = geo(-1.5, -2.5, 9)
Z5, E5 = (0, 1), [(2, 0), (3, 2), (1.5, 2.5)]
B5 = [strecke_bild(Z5, p, 2) for p in E5]
assert B5 == [(4, -1), (6, 3), (3, 4)]
clip('kontrolle-streckung', 2, 'Ähnlichkeit sehen: Kontrollfragen zur zentrischen Streckung',
     'Fünf Fragen: einen Bildpunkt mit negativem k finden, verkleinern, parallele Seiten, k aus Abständen und das Zentrum '
     'aus Original und Bild bestimmen.',
     ['zentrische Streckung', 'Streckfaktor', 'Kontrollfragen'], [
         sz('Frage 1',
            'P Strich liegt auf der Geraden durch Z und P, auf der anderen Seite von Z und doppelt so weit weg: bei minus '
            'fünf und minus zwei.',
            f(r"Z \to P: \; (2 \mid 1); \quad \cdot\,(\fb{-2}): \; (-4 \mid -2)", 300, 44, ein=1.0),
            f(r"P' = (-1 - 4 \mid 0 - 2) = \fc{(-5 \mid -2)}", 410, 46, ein=1.0),
            graf(WK1, [PK(ZK1, 5, 0.12), T(-1.25, 0.3, 'Z', 5, g=32), PK(PK1, 1, 0.12), T(1.35, 1.25, 'P', 1, g=32)], ein=0.05),
            graf(WK1, [G(ZK1, PK1, WK1, 5, True, 2), PK(PK1b, 3, 0.15), T(-5.0, -2.75, 'P′', 3, g=32)], ein=1.0, raster=False)),
         sz('Frage 2',
            'Null Komma zwei fünf ist positiv und kleiner als eins: Das Bild liegt auf derselben Seite von Z und ist '
            'verkleinert, jede Seite ein Viertel so lang.',
            f(r'0 \lt \fb{k} = 0.25 \lt 1', 300, 52, ein=1.0),
            n('gleiche Seite, Seiten ein Viertel so lang', 420, 'blau', 44, ein=1.0)),
         sz('Frage 3',
            'Jede Bildseite ist parallel zu ihrer Originalseite, auch bei negativem k. Das Bild ist um Z gedreht, nicht '
            'umgeklappt.',
            n("@A'B' \\parallel AB@, auch bei @k \\lt 0@", 300, 'blau', 48, ein=1.0)),
         sz('Frage 4',
            'Zehn durch vier ist zwei Komma fünf. Weil P Strich auf der anderen Seite von Z liegt, ist k minus zwei Komma '
            'fünf.',
            f(r"|k| = \dfrac{\overline{ZP'}}{\overline{ZP}} = \dfrac{10}{4} = 2.5", 300, 48, ein=1.0),
            f(r'\text{andere Seite: } \fc{k = -2.5}', 470, 48, ein=1.0)),
         sz('Frage 5',
            'Verlängere A A Strich, B B Strich und C C Strich. Die drei Geraden treffen sich im Zentrum Z. Die Bildseiten sind '
            'doppelt so lang, k ist zwei.',
            f(r"AA', \; BB', \; CC' \text{ treffen sich in } \fc{Z}", 300, 46, ein=1.0),
            f(r'\fb{k = 2}', 410, 50, ein=1.0),
            graf(WK5, [V(E5, 1, 0.14), V(B5, 2, 0.12, gestrichelt=True)]
                 + ecken([('A', E5[0]), ('B', E5[1]), ('C', E5[2])], 1, 0.4) + ecken([('A′', B5[0]), ('B′', B5[1]), ('C′', B5[2])], 2, 0.45), ein=0.05),
            graf(WK5, [G(E5[i], B5[i], WK5, 5, True, 2) for i in range(3)] + [PK(Z5, 3, 0.15), T(-0.45, 1.25, 'Z', 3, g=32)], ein=1.0, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Strecken vom Zentrum aus, Abstände mal Betrag von k, und das Vorzeichen von k wählt die Seite.',
            titel('Zum Mitnehmen', 250, 76),
            n('vom Zentrum @Z@ aus strecken|Abstände @\\cdot\\, |k|@|Vorzeichen von @k@: welche Seite', 400, 'blau', 44, ein=1.2)),
     ], [
         # Ziel P′(−5|−2); die Fallen liegen mindestens 1.4 Einheiten auseinander, Toleranz 0.6.
         klick('Frage 1', 'Streckung von Z aus mit k = −2: Tipp den Bildpunkt P′ an.', [-5, -2], 'Getroffen: P′(−5 | −2).',
               [{'bei': [3, 2], 'text': 'Das wäre k = 2. Bei negativem k liegt P′ auf der anderen Seite von Z.',
                 'sprich': 'Das wäre k gleich zwei. Bei negativem k liegt P Strich auf der anderen Seite von Z.'},
                {'bei': [-2, -2], 'text': 'Das ist −2 mal die Koordinaten von P — gestreckt wird aber vom Zentrum Z aus.',
                 'sprich': 'Das ist minus zwei mal die Koordinaten von P. Gestreckt wird aber vom Zentrum Z aus.'},
                {'bei': [-3, -1], 'text': 'Das ist gleich weit weg wie P (k = −1). Der Abstand soll doppelt so gross werden.',
                 'sprich': 'Das ist gleich weit weg wie P, also k gleich minus eins. Der Abstand soll doppelt so gross werden.'},
                {'bei': [1, 1], 'text': 'Das ist P selbst.', 'sprich': 'Das ist P selbst.'}],
               FALSCH, sprich='Streckung von Z aus mit k gleich minus zwei: Tipp den Bildpunkt P Strich an.', falsch_sprich=FALSCH,
               tol=0.6, eingabe=['x', 'y']),
         wahl('Frage 2', 'k = 0.25: Wie liegt das Bild?', ['gleiche Seite von Z, Seiten ein Viertel so lang', 'gleiche Seite von Z, Seiten viermal so lang',
                                                          'andere Seite von Z, Seiten ein Viertel so lang'], 0,
              {0: 'Ja.', 1: 'k liegt zwischen 0 und 1. Wird das Bild dann grösser oder kleiner?', 2: 'Ist k positiv oder negativ?'},
              sprich='k gleich null Komma zwei fünf: Wie liegt das Bild?',
              rueck_sprich={1: 'k liegt zwischen null und eins. Wird das Bild dann grösser oder kleiner?', 2: 'Ist k positiv oder negativ?'}),
         wahl('Frage 3', 'Bei k = −2: Wie liegt die Bildseite A′B′ zur Seite AB?', ['parallel zu AB', 'senkrecht zu AB', 'gespiegelt, also anders geneigt'], 0,
              {0: 'Ja.', 1: 'Eine Streckung dreht keine Seite um 90°. Wie ist es bei k = 2?', 2: 'Bei k < 0 wird die Figur um Z gedreht, nicht umgeklappt. Wie liegen die Seiten dann?'},
              sprich='Bei k gleich minus zwei: Wie liegt die Bildseite A Strich B Strich zur Seite A B?',
              rueck_sprich={1: 'Eine Streckung dreht keine Seite um neunzig Grad. Wie ist es bei k gleich zwei?',
                            2: 'Bei negativem k wird die Figur um Z gedreht, nicht umgeklappt. Wie liegen die Seiten dann?'}),
         wahl('Frage 4', 'ZP = 4 cm. P′ liegt auf der anderen Seite von Z, 10 cm von Z entfernt. Wie gross ist k?', ['k = −2.5', 'k = 2.5', 'k = −0.4'], 0,
              {0: 'Ja.', 1: 'Der Betrag stimmt. Auf welcher Seite von Z liegt P′?', 2: 'Das ist der Kehrwert. k ist Bildabstand durch Originalabstand.'},
              sprich='Z P gleich vier Zentimeter. P Strich liegt auf der anderen Seite von Z, zehn Zentimeter von Z entfernt. Wie gross ist k?',
              rueck_sprich={1: 'Der Betrag stimmt. Auf welcher Seite von Z liegt P Strich?', 2: 'Das ist der Kehrwert. k ist Bildabstand durch Originalabstand.'}),
         # Ziel Z(0|1). Falle (6|−2) liegt auf der Geraden AA′ (aber nicht auf BB′), Falle (3.3|1.6) zwischen den Dreiecken.
         klick('Frage 5', 'A′B′C′ ist das Bild von ABC. Tipp das Zentrum Z an.', [0, 1], 'Getroffen: Hier treffen sich die Geraden AA′, BB′ und CC′.',
               [{'bei': [6, -2], 'text': 'Dieser Punkt liegt auf der Geraden AA′, aber nicht auf BB′. Das Zentrum liegt auf allen drei.',
                 'sprich': 'Dieser Punkt liegt auf der Geraden A A Strich, aber nicht auf B B Strich. Das Zentrum liegt auf allen drei.'},
                {'bei': [3.3, 1.6], 'text': 'Das ist ungefähr die Mitte zwischen den Dreiecken. Verlängere die Geraden durch A und A′, B und B′.',
                 'sprich': 'Das ist ungefähr die Mitte zwischen den Dreiecken. Verlängere die Geraden durch A und A Strich, B und B Strich.'}],
               FALSCH, sprich='A Strich B Strich C Strich ist das Bild von A B C. Tipp das Zentrum Z an.', falsch_sprich=FALSCH, tol=0.6),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# Wie Arbeitsbereich 2: S(0|0), erster Strahl waagrecht, zweiter unter θ mit cos θ = 0.78125 (θ = 38.62°);
# SA = 4, SB = 3, AB = 2.5; k = 2.5 (Themenseite A2): SA′ = 10, SB′ = 7.5, A′B′ = 6.25; X-Figur k = −1.5.
TH2 = math.acos(0.78125)
V2 = (math.cos(TH2), math.sin(TH2))
S2 = (0, 0)
def fig2(k, sa=4, sb=3):
    A_, B_ = (sa, 0), (sb * V2[0], sb * V2[1])
    return A_, B_, (k * sa, 0), (k * sb * V2[0], k * sb * V2[1])
A2, B2, A22, B22 = fig2(2.5)
_, _, A2x, B2x = fig2(-1.5)
assert abs(math.dist(A2, B2) - 2.5) < 1e-9 and abs(math.dist(A22, B22) - 6.25) < 1e-9 and abs(math.dist(A2x, B2x) - 3.75) < 1e-9
W2 = geo(-7, -4.4, 18.5, 500)          # 18.5 × 12.17 Einheiten auf 760 × 500 px
GR2 = dict(y=300, hoehe=500)
STR2 = [G(S2, (1, 0), W2, 5, False, 2.5), G(S2, V2, W2, 5, False, 2.5)]
PKT2 = [PK(S2, 5, 0.13), T(-0.15, -0.75, 'S', 5, g=32)]
def ab_fig(A_, B_, A2_, B2_, mit_bild=True, namen=True):
    fg = [S(A_, B_, 1, dicke=5), PK(A_, 1, 0.11), PK(B_, 1, 0.11)]
    if namen:
        fg += [T(A_[0], A_[1] - 0.8, 'A', 1, g=32), T(B_[0] - 0.45, B_[1] + 0.35, 'B', 1, g=32)]
    if mit_bild:
        fg += [S(A2_, B2_, 2, dicke=5), PK(A2_, 2, 0.11), PK(B2_, 2, 0.11)]
        if namen:
            unten = A2_[0] < 0
            fg += [T(A2_[0], A2_[1] + (0.45 if unten else -0.8), 'A′', 2, g=32), T(B2_[0] + (0.6 if unten else -0.5), B2_[1] + (-0.4 if unten else 0.35), 'B′', 2, g=32)]
    return fg
def auf_strahl(s0, s1, v, d):
    """Strecke auf der Geraden mit Richtung v von s0 bis s1, um d Einheiten seitlich versetzt (Massbalken)."""
    n_ = (-v[1], v[0])
    return S((s0 * v[0] + d * n_[0], s0 * v[1] + d * n_[1]), (s1 * v[0] + d * n_[0], s1 * v[1] + d * n_[1]))
def massbalken(s0, s1, v, d, farbe, text, tdx=0.0, tdy=0.0):
    st = auf_strahl(s0, s1, v, d)
    st.update(farbe=farbe, dicke=6)
    m = ((st['von'][0] + st['bis'][0]) / 2, (st['von'][1] + st['bis'][1]) / 2)
    return [st, T(m[0] + tdx, m[1] + tdy, text, farbe, g=30)]
# gekippte Gerade durch A′ (15° gegen AB): Schnitt mit dem zweiten Strahl
def kipp(k, dl, sa=4, sb=3):
    A_, B_, A2_, _ = fig2(k, sa, sb)
    u = (B_[0] - A_[0], B_[1] - A_[1]); r = math.radians(dl)
    u = (u[0] * math.cos(r) - u[1] * math.sin(r), u[0] * math.sin(r) + u[1] * math.cos(r))
    det = -u[0] * V2[1] + u[1] * V2[0]
    s = (A2_[0] * V2[1] - A2_[1] * V2[0]) / det
    return (A2_[0] + s * u[0], A2_[1] + s * u[1])
B2k = kipp(2.5, 15)
SB2k = math.hypot(*B2k)           # ≈ 5.80 statt 7.5: 3 : 5.80 ≈ 0.52, aber 4 : 10 = 0.4
assert abs(SB2k - 5.8004) < 1e-3
clip('strahlensaetze', 3, 'Ähnlichkeit sehen: Strahlensätze',
     'Zwei Geraden durch S, zwei Parallelen: 1. Strahlensatz SA : SA′ = SB : SB′ (auch mit den Abschnitten), 2. Strahlensatz '
     'SA : SA′ = AB : A′B′ mit den ganzen Strecken ab S, X-Figur, nur mit Parallelen, Umkehrung.',
     ['Strahlensatz', 'Parallelen', 'X-Figur', 'Verhältnisgleichung'], [
         sz('Die Figur',
            'Zwei Geraden schneiden sich in S. Zwei Parallelen schneiden sie: die eine in A und B, die andere in A Strich und '
            'B Strich. Das ist eine zentrische Streckung mit dem Zentrum S.',
            f(r"AB \parallel A'B'", 300, 54, ein=4.6),
            n('Streckung mit Zentrum @S@', 420, 'blau', 46, ein=8.4),
            graf(W2, STR2 + PKT2, ein=0.3, **GR2),
            graf(W2, ab_fig(A2, B2, A22, B22), ein=4.6, raster=False, **GR2)),
         sz('1. Strahlensatz',
            'Auf den Strahlen gilt: S A zu S A Strich wie S B zu S B Strich. Mit S A gleich vier, S A Strich gleich zehn und '
            'S B gleich drei ist S B Strich gleich sieben Komma fünf.',
            f(r"\overline{SA} : \overline{SA'} = \overline{SB} : \overline{SB'}", 300, 46, ein=1.8),
            f(r"4 : 10 = 3 : \overline{SB'}", 410, 48, ein=5.1),
            f(r"\overline{SB'} = \dfrac{10 \cdot 3}{4} = \fc{7.5}", 530, 48, ein=10.0),
            graf(W2, STR2 + PKT2 + ab_fig(A2, B2, A22, B22), ein=0.05, **GR2),
            graf(W2, massbalken(0, 4, (1, 0), -0.55, 1, '4', 0, -0.75) + massbalken(0, 10, (1, 0), -1.45, 2, '10', 0, -0.75)
                 + massbalken(0, 3, V2, 0.55, 1, '3', -0.35, 0.45), ein=5.1, raster=False, **GR2),
            graf(W2, massbalken(0, 7.5, V2, 1.45, 3, '7.5', -0.45, 0.5), ein=10.0, raster=False, **GR2)),
         sz('Mit den Abschnitten',
            'Gleichwertig mit den Abschnitten: S A zu A A Strich wie S B zu B B Strich. Vier zu sechs wie drei zu vier Komma '
            'fünf.',
            f(r"\overline{SA} : \overline{AA'} = \overline{SB} : \overline{BB'}", 300, 46, ein=1.0),
            f(r'4 : 6 = 3 : \fc{4.5}', 410, 48, ein=6.6),
            graf(W2, STR2 + PKT2 + ab_fig(A2, B2, A22, B22), ein=0.05, **GR2),
            graf(W2, massbalken(0, 4, (1, 0), -0.55, 1, '4', 0, -0.75) + massbalken(4, 10, (1, 0), -0.55, 2, '6', 0, -0.75)
                 + massbalken(0, 3, V2, 0.55, 1, '3', -0.35, 0.45), ein=1.0, raster=False, **GR2),
            graf(W2, massbalken(3, 7.5, V2, 0.55, 3, '4.5', -0.45, 0.5), ein=6.6, raster=False, **GR2)),
         sz('2. Strahlensatz',
            'Im zweiten Strahlensatz kommen die Parallelen dazu: S A zu S A Strich wie A B zu A Strich B Strich. A B ist zwei '
            'Komma fünf, also ist A Strich B Strich sechs Komma zwei fünf. Dazu gehören die ganzen Strecken ab S, nicht A A '
            'Strich.',
            f(r"\overline{SA} : \overline{SA'} = \overline{AB} : \overline{A'B'}", 300, 46, ein=3.8),
            f(r"4 : 10 = 2.5 : \overline{A'B'}", 410, 46, ein=6.6),
            f(r"\overline{A'B'} = \fc{6.25}", 520, 46, ein=9.6),
            f(r"\fd{\text{nicht } \overline{SA} : \overline{AA'}}", 630, 44, ein=13.4),
            graf(W2, STR2 + PKT2 + ab_fig(A2, B2, A22, B22), ein=0.05, **GR2),
            graf(W2, [S(A2, B2, 1, dicke=10), S(A22, B22, 2, dicke=10), seitentext(A2, B2, '2.5', S2, 1, 0.55, 30)], ein=6.6, raster=False, **GR2),
            graf(W2, [T(8.6, 2.75, '6.25', 3, g=30)], ein=9.6, raster=False, **GR2)),
         sz('X-Figur',
            'Liegt S zwischen den Parallelen, entsteht eine X-Figur. Die Gleichungen bleiben dieselben, mit den Längen: Hier '
            'ist S A Strich sechs, also A Strich B Strich drei Komma sieben fünf.',
            f(r"4 : 6 = 2.5 : \overline{A'B'}", 300, 48, ein=7.0),
            f(r"\overline{A'B'} = \fc{3.75}", 410, 48, ein=9.4),
            graf(W2, STR2 + PKT2 + ab_fig(A2, B2, A22, B22, mit_bild=False), ein=0.05, **GR2),
            # die zweite Parallele wandert von k = 2.5 über S (k = 0) nach k = −1.5 — linear in k
            graf(W2, [S(A22, B22, 2, dicke=5, bewegung=[[0.8, {}], [3.6, {'von': r3(A2x), 'bis': r3(B2x)}]])], ein=0.05, raster=False, **GR2),
            graf(W2, [PK(A2x, 2, 0.11), PK(B2x, 2, 0.11), T(A2x[0], 0.45, 'A′', 2, g=32), T(B2x[0] + 0.55, B2x[1] - 0.45, 'B′', 2, g=32),
                      T(-3.0, -0.75, '6', 2, g=30)], ein=3.7, raster=False, **GR2)),
         sz('Nur mit Parallelen',
            'Ist die zweite Gerade nicht parallel, stimmen die Verhältnisse nicht mehr. Umgekehrt: Liegen A Strich und B Strich '
            'auf den Strahlen von S durch A und durch B, und sind die Verhältnisse gleich, dann sind die Geraden parallel.',
            # rot: die gekippte Gerade trifft den Strahl bei ≈ 5.80 (statt 7.5) — der Punkt heisst nicht B′, darum nur die Zahl
            f(r"\dfrac{\overline{SA}}{\overline{SA'}} = \dfrac{4}{10} = 0.4", 300, 46, ein=2.8),
            f(r"\fd{\dfrac{3}{%.2f} \approx %.2f \neq 0.4}" % (SB2k, 3 / SB2k), 480, 46, ein=2.8),
            n("Umkehrung: @A'@ auf dem Strahl @SA@,|@B'@ auf dem Strahl @SB@,|gleiche Verhältnisse @\\Rightarrow AB \\parallel A'B'@", 620, 'blau', 40, ein=4.5),
            # die Parallele (orange) steht von Anfang an; eine zweite Gerade durch A′ kippt um 15° weg und wird dabei rot
            # (Gegenbeispiel) — vorher liegt sie unsichtbar auf der Parallelen, sie erscheint erst mit dem Kippen.
            graf(W2, STR2 + PKT2 + ab_fig(A2, B2, A22, B22), ein=0.05, **GR2),
            graf(W2, [S(A22, B22, 4, dicke=5, bewegung=[[1.0, {}], [2.6, {'bis': r3(B2k)}]])], ein=0.9, raster=False, **GR2),
            graf(W2, [PK(B2k, 4, 0.11), T(B2k[0] - 0.75, B2k[1] + 0.3, '≈ 5.80', 4, g=28)], ein=2.6, raster=False, **GR2)),
         sz('Merke',
            'Zum Mitnehmen: Strahl mit Strahl, Parallele mit den ganzen Strecken ab S, und nur, wenn die Geraden parallel sind.',
            titel('Zum Mitnehmen', 250, 76),
            n("@\\overline{SA} : \\overline{SA'} = \\overline{SB} : \\overline{SB'}@|@\\overline{SA} : \\overline{SA'} = \\overline{AB} : \\overline{A'B'}@|nur mit @AB \\parallel A'B'@", 400, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
# Frage 1: Figur S(0|0), zweiter Strahl unter 50°, SA = 3, SB = 4, k = 2 (SA ≠ SB, damit «SA : SB = SB′ : SA′» falsch ist).
WK2 = geo(-1, -1.5, 10)
U50 = (math.cos(math.radians(50)), math.sin(math.radians(50)))
def figk(sa, sb, k, v=U50):
    return (sa, 0), (sb * v[0], sb * v[1]), (k * sa, 0), (k * sb * v[0], k * sb * v[1])
FA, FB, FA2, FB2 = figk(3, 4, 2)
STRK = [G((0, 0), (1, 0), WK2, 5, False, 2.5), G((0, 0), U50, WK2, 5, False, 2.5), PK((0, 0), 5, 0.12), T(-0.2, -0.65, 'S', 5, g=32)]
def namen(A_, B_, A2_, B2_):
    return [T(A_[0], -0.7, 'A', 1, g=32), T(B_[0] - 0.5, B_[1] + 0.2, 'B', 1, g=32), T(A2_[0], -0.7, 'A′', 2, g=32), T(B2_[0] - 0.55, B2_[1] + 0.2, 'B′', 2, g=32)]
# Frage 3: SA = 2, SA′ = 5, SB′ = 7.5 → SB = 3, B = 3 · (cos 50°, sin 50°) = (1.928 | 2.298); B′ = (4.821 | 5.745).
QA, QB, QA2, QB2 = figk(2, 3, 2.5)
assert abs(math.hypot(*QB2) - 7.5) < 1e-9
F45 = (4.5 * U50[0], 4.5 * U50[1])        # Falle: gleicher Unterschied (SB = 7.5 − 3)
assert abs(math.hypot(*QB) - 3) < 1e-9 and abs(math.dist(QB, F45) - 1.5) < 1e-9
clip('kontrolle-strahlensaetze', 4, 'Ähnlichkeit sehen: Kontrollfragen zu den Strahlensätzen',
     'Fünf Fragen: die richtige Gleichung, die Falle AA′, den Punkt B aus B′ finden, die X-Figur und wann die Strahlensätze '
     'nicht gelten.',
     ['Strahlensatz', 'Parallelen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Strahl mit Strahl: S A zu S A Strich wie S B zu S B Strich. Die anderen Gleichungen mischen Strecken, die nicht '
            'zueinander gehören.',
            f(r"\fc{\overline{SA} : \overline{SA'} = \overline{SB} : \overline{SB'}}", 300, 46, ein=1.0),
            graf(WK2, STRK + ab_fig(FA, FB, FA2, FB2, namen=False) + namen(FA, FB, FA2, FB2), ein=0.05)),
         sz('Frage 2',
            'S A Strich ist drei plus sechs, also neun. A Strich B Strich ist zwei mal neun Drittel, also sechs Zentimeter.',
            f(r"\overline{SA'} = 3 + 6 = 9", 300, 48, ein=1.0),
            f(r"\overline{A'B'} = 2 \cdot \dfrac{9}{3} = \fc{6\,\mathrm{cm}}", 420, 48, ein=1.0)),
         sz('Frage 3',
            'Die Parallele zu A Strich B Strich durch A trifft den zweiten Strahl in B. S B ist sieben Komma fünf mal zwei '
            'durch fünf, also drei.',
            f(r"\overline{SB} = 7.5 \cdot \dfrac{2}{5} = \fc{3}", 300, 48, ein=1.0),
            # gegeben: A, A′, B′ und die Gerade A′B′ (Abstände 2, 5, 7.5); gesucht B — erst nach der Antwort
            graf(WK2, STRK + [S(QA2, QB2, 2, dicke=5), PK(QA, 1, 0.11), PK(QA2, 2, 0.11), PK(QB2, 2, 0.11),
                              T(QA[0], -0.7, 'A', 1, g=32), T(QA2[0], -0.7, 'A′', 2, g=32), T(QB2[0] - 0.6, QB2[1] + 0.25, 'B′', 2, g=32),
                              T(1.0, 0.3, '2', 5, g=28), T(3.5, -1.25, 'SA′ = 5', 5, g=28), T(2.2, 3.55, 'SB′ = 7.5', 5, 'end', 28)], ein=0.05),
            graf(WK2, [S(QA, QB, 1, dicke=5), PK(QB, 3, 0.15), T(QB[0] - 0.5, QB[1] + 0.2, 'B', 3, g=32)], ein=1.0, raster=False)),
         sz('Frage 4',
            'In der X-Figur gilt dieselbe Gleichung: A Strich B Strich ist drei mal fünf Halbe, also sieben Komma fünf.',
            f(r"\overline{A'B'} = 3 \cdot \dfrac{5}{2} = \fc{7.5}", 300, 48, ein=1.0)),
         sz('Frage 5',
            'Die Strahlensätze brauchen parallele Geraden. Ob S zwischen ihnen liegt oder wie gross der Winkel bei S ist, '
            'spielt keine Rolle.',
            n("Voraussetzung: @AB \\parallel A'B'@", 300, 'blau', 48, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Erst die Parallelen suchen, dann Strecke zu Strecke vom selben Punkt S aus.',
            titel('Zum Mitnehmen', 250, 76),
            n('erst die Parallelen suchen|dann die ganzen Strecken ab @S@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'AB ∥ A′B′. Welche Gleichung stimmt?', ['SA : SA′ = SB : SB′', 'SA : AA′ = AB : A′B′', 'SA : SB = SB′ : SA′'], 0,
              {0: 'Ja.', 1: 'Zu den Parallelen gehören die ganzen Strecken ab S. Ist AA′ eine Strecke ab S?', 2: 'Schau, welche Strecke wohin gestreckt wird: SA wird zu SA′.'},
              sprich='A B ist parallel zu A Strich B Strich. Welche Gleichung stimmt?',
              rueck_sprich={1: 'Zu den Parallelen gehören die ganzen Strecken ab S. Ist A A Strich eine Strecke ab S?',
                            2: 'Schau, welche Strecke wohin gestreckt wird: S A wird zu S A Strich.'}),
         wahl('Frage 2', 'SA = 3 cm, AA′ = 6 cm, AB = 2 cm und AB ∥ A′B′. Wie lang ist A′B′?', ['6 cm', '4 cm', '8 cm'], 0,
              {0: 'Ja.', 1: 'Hast du mit AA′ gerechnet? Zu den Parallelen gehört SA′ = SA + AA′.', 2: 'Nicht addieren: Die Strecken stehen im gleichen Verhältnis.'},
              sprich='S A gleich drei, A A Strich gleich sechs, A B gleich zwei Zentimeter, A B parallel zu A Strich B Strich. Wie lang ist A Strich B Strich?',
              rueck_sprich={1: 'Hast du mit A A Strich gerechnet? Zu den Parallelen gehört S A Strich, also S A plus A A Strich.',
                            2: 'Nicht addieren. Die Strecken stehen im gleichen Verhältnis.'}),
         # Umgekehrt zur Themenseite A2 (dort SB′ aus SB): gegeben SB′, gesucht B. Ziel B auf dem Strahl bei 3; Fallen bei
         # 4.5 (gleicher Unterschied, BB′ = AA′ = 3) und bei B′ selbst (7.5); Abstand ≥ 1.5, Toleranz 0.6.
         klick('Frage 3', 'SA = 2, SA′ = 5, SB′ = 7.5. Tipp den Punkt B an, damit AB ∥ A′B′.', r3(QB), 'Getroffen: SB = 3.',
               [{'bei': r3(F45), 'text': 'Hier wäre BB′ = AA′ = 3. Die Strecken stehen aber im gleichen Verhältnis, nicht im gleichen Abstand.',
                 'sprich': 'Hier wäre B B Strich gleich A A Strich. Die Strecken stehen aber im gleichen Verhältnis, nicht im gleichen Abstand.'},
                {'bei': r3(QB2), 'text': 'Das ist B′ selbst. B liegt auf demselben Strahl, aber näher bei S — so wie A näher bei S liegt als A′.',
                 'sprich': 'Das ist B Strich selbst. B liegt auf demselben Strahl, aber näher bei S, so wie A näher bei S liegt als A Strich.'}],
               FALSCH, sprich='S A gleich zwei, S A Strich gleich fünf, S B Strich gleich sieben Komma fünf. Tipp den Punkt B an, damit A B parallel zu A Strich B Strich ist.',
               falsch_sprich=FALSCH, tol=0.6),
         wahl('Frage 4', 'S liegt zwischen den Parallelen: SA = 2, SA′ = 5, AB = 3. Wie lang ist A′B′?', ['7.5', '1.2', '6'], 0,
              {0: 'Ja.', 1: 'Das Verhältnis steht verkehrt: A′ liegt weiter von S weg als A.', 2: 'Nicht den Unterschied addieren: Die Strecken stehen im Verhältnis.'},
              sprich='S liegt zwischen den Parallelen: S A gleich zwei, S A Strich gleich fünf, A B gleich drei. Wie lang ist A Strich B Strich?',
              rueck_sprich={1: 'Das Verhältnis steht verkehrt. A Strich liegt weiter von S weg als A.', 2: 'Nicht den Unterschied addieren. Die Strecken stehen im Verhältnis.'}),
         wahl('Frage 5', 'Wann darfst du die Strahlensätze nicht anwenden?', ['wenn AB und A′B′ nicht parallel sind', 'wenn S zwischen den Parallelen liegt',
                                                                            'wenn die Geraden bei S einen stumpfen Winkel bilden'], 0,
              {0: 'Ja.', 1: 'Die X-Figur ist auch eine Streckung, mit k < 0.', 2: 'Der Winkel bei S spielt keine Rolle. Was muss für AB und A′B′ gelten?'},
              sprich='Wann darfst du die Strahlensätze nicht anwenden?',
              rueck_sprich={1: 'Die X-Figur ist auch eine Streckung, mit negativem k.', 2: 'Der Winkel bei S spielt keine Rolle. Was muss für A B und A Strich B Strich gelten?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Wie Arbeitsbereich 3: Rechteck 3 × 2 in der Ecke O(0|0), Bild 4.5 × 3 (k = 1.5); Gegenbeispiel 4.5 × 2.
W3 = geo(-0.8, -0.9, 10.6)
O = (0, 0)
def recht(b, h, x0=0, y0=0):
    return [(x0, y0), (x0 + b, y0), (x0 + b, y0 + h), (x0, y0 + h)]
DIAG = G(O, (3, 2), W3, 5, True, 2)
ORIG3 = [V(recht(3, 2), 1, 0.14), T(1.5, -0.6, '3', 1, g=30), T(3.3, 0.9, '2', 1, 'start', 30)]
clip('figuren', 5, 'Ähnlichkeit sehen: ähnliche Figuren, Längen und Flächen',
     'Ähnlich heisst gleiche Form: alle Seiten mit demselben k. Umfang mal k, Fläche mal k² (vier Kopien bei k = 2), Kreise '
     'sind immer ähnlich, Massstab 1 : 200, und k aus dem Flächenverhältnis.',
     ['ähnliche Figuren', 'Streckfaktor', 'Flächenfaktor', 'Massstab'], [
         sz('Ähnlich',
            'Ähnlich heisst: gleiche Form. Das Rechteck drei mal zwei und das Rechteck vier Komma fünf mal drei sind ähnlich: '
            'Beide Seiten wachsen mit k gleich eins Komma fünf.',
            f(r'\dfrac{4.5}{3} = \dfrac{3}{2} = \fb{1.5}', 300, 54, ein=7.9),
            graf(W3, [DIAG] + ORIG3, ein=0.3),
            graf(W3, [V(recht(3, 2), 2, 0.12, gestrichelt=True, bewegung=[[4.2, {}], [6.0, {'punkte': [r3(p) for p in recht(4.5, 3)]}]])], ein=0.3, raster=False),
            graf(W3, [T(2.25, 3.25, '4.5', 2, g=30), T(4.8, 2.0, '3', 2, 'start', 30)], ein=6.0, raster=False)),
         sz('Nicht ähnlich',
            'Das Rechteck vier Komma fünf mal zwei ist nicht ähnlich: Die Breite wächst mit eins Komma fünf, die Höhe gar nicht. '
            'Seine Ecke liegt nicht auf der Diagonalen.',
            f(r'\dfrac{4.5}{3} = 1.5, \quad \dfrac{2}{2} = 1', 300, 50, ein=3.5),
            n('nicht ähnlich', 430, 'rot', 46, ein=2.7),
            graf(W3, [DIAG] + ORIG3 + [V(recht(4.5, 2), 4, 0.08, gestrichelt=True), T(4.8, 1.2, '2', 4, 'start', 30), T(3.9, -0.6, '4.5', 4, g=30)], ein=0.3)),
         sz('Umfang',
            'Der Umfang ist eine Länge. Er wächst mit k: Aus zehn Zentimetern werden fünfzehn.',
            f(r'u = 2 \cdot (3 + 2) = 10', 300, 50, ein=1.0),
            f(r"u' = \fb{1.5} \cdot 10 = \fc{15}", 410, 50, ein=4.5),
            graf(W3, [DIAG] + ORIG3 + [V(recht(4.5, 3), 2, 0.12, gestrichelt=True)], ein=0.05)),
         sz('Fläche',
            'Bei der Fläche wachsen beide Seiten. Bei k gleich zwei passen vier Originale ins Bild. Allgemein wächst die Fläche '
            'mit k im Quadrat: Aus sechs werden zwei Komma zwei fünf mal sechs, also dreizehn Komma fünf Quadratzentimeter.',
            f(r"k = 2: \; A' = 4 \cdot A", 300, 50, ein=3.8),
            f(r"A' = \fb{k}^2 \cdot A", 410, 50, ein=6.8),
            f(r"A' = 1.5^2 \cdot 6 = \fc{13.5}\,\mathrm{cm}^2", 520, 48, ein=10.5),
            # erst k = 2 mit vier Originalen; auf «aus sechs werden zwei Komma zwei fünf mal sechs» (7.6 s, gemessen) schrumpft
            # das Bild auf k = 1.5 (4.5 × 3), damit Bild und Rechnung zusammenpassen
            graf(W3, [DIAG] + ORIG3 + [V(recht(6, 4), 2, 0.10, gestrichelt=True,
                                         bewegung=[[7.6, {}], [8.8, {'punkte': [r3(p) for p in recht(4.5, 3)]}]])], ein=0.05),
            graf(W3, [S((3, 0), (3, 4), 2, True, 2), S((0, 2), (6, 2), 2, True, 2)], ein=2.3, aus=7.6, raster=False),
            graf(W3, [T(x_, y_, z_, 3, g=40) for x_, y_, z_ in ((1.5, 0.75, '1'), (4.5, 0.75, '2'), (1.5, 2.75, '3'), (4.5, 2.75, '4'))], ein=3.8, aus=7.6, raster=False),
            graf(W3, [T(2.25, 3.25, '4.5', 2, g=30), T(4.8, 1.5, '3', 2, 'start', 30)], ein=8.8, raster=False)),
         sz('Kreis',
            'Alle Kreise sind ähnlich. Aus dem Radius zwei wird drei: k ist eins Komma fünf, die Fläche wird zwei Komma zwei '
            'fünf mal so gross.',
            f(r"k = \dfrac{r'}{r} = \dfrac{3}{2} = \fb{1.5}", 300, 50, ein=3.9),
            f(r"\dfrac{A'}{A} = 1.5^2 = \fc{2.25}", 430, 50, ein=6.0),
            graf(W3, [KR((4.5, 3.2), 2, 1, 0.12), KR((4.5, 3.2), 3, 2, 0.06, gestrichelt=True), PK((4.5, 3.2), 5, 0.1),
                      S((4.5, 3.2), (6.5, 3.2), 1, dicke=3), S((4.5, 3.2), (1.5, 3.2), 2, dicke=3), T(5.5, 3.45, 'r = 2', 1, g=28), T(3.0, 3.45, 'r′ = 3', 2, g=28)], ein=0.05)),
         sz('Massstab',
            'Ein Plan im Massstab eins zu zweihundert: Zwei Komma fünf Zentimeter auf dem Plan sind fünf Meter. Ein Quadrat von '
            'sechs Komma zwei fünf Quadratzentimetern ist aber vierzigtausend mal so gross: fünfundzwanzig Quadratmeter.',
            f(r'1 : 200', 300, 54, ein=2.0),
            f(r'2.5\,\mathrm{cm} \cdot 200 = 500\,\mathrm{cm} = \fc{5\,\mathrm{m}}', 410, 44, ein=5.4),
            f(r'6.25\,\mathrm{cm}^2 \cdot 200^2 = 250\,000\,\mathrm{cm}^2 = \fc{25\,\mathrm{m}^2}', 520, 40, ein=11.5),
            graf(W3, [V(recht(2.5, 2.5, 3, 1), 1, 0.12), T(4.25, 0.4, '2.5 cm', 1, g=28), T(4.25, 2.1, 'Plan', 5, g=30)], ein=0.05)),
         sz('Zurück zu k',
            'Umgekehrt: Ist die Fläche sechs Komma zwei fünf mal so gross, wachsen die Längen nur mit der Wurzel daraus. k ist '
            'zwei Komma fünf.',
            f(r"\dfrac{A'}{A} = 6.25", 300, 48, ein=1.0),
            f(r"k = \sqrt{6.25} = \fc{2.5}", 430, 48, ein=5.6),
            # Bühne nicht leer: das Original, das Bild wächst erst auf «k ist zwei Komma fünf» (5.5 s, gemessen) auf 7.5 × 5
            graf(W3, [DIAG] + ORIG3, ein=0.05),
            graf(W3, [V(recht(3, 2), 2, 0.12, gestrichelt=True, bewegung=[[5.6, {}], [6.6, {'punkte': [r3(p) for p in recht(7.5, 5)]}]])], ein=5.5, raster=False),
            graf(W3, [T(3.75, 5.25, '7.5', 2, g=30), T(7.8, 2.5, '5', 2, 'start', 30)], ein=6.6, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Ähnliche Figuren haben gleiche Winkel und alle Seiten im selben Verhältnis k. Längen wachsen mit k, '
            'Flächen mit k im Quadrat.',
            titel('Zum Mitnehmen', 250, 76),
            n("alle Seiten mit demselben @k@|Längen, Umfang @\\cdot\\, k@|Flächen @\\cdot\\, k^2@", 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
# Frage 5: rechtwinkliges Dreieck P(0|0), Q(3|0), R(0|2); Bild k = 1.5, um 90° gedreht: P′(8|0), Q′(8|4.5), R′(5|0).
WK3 = geo(-1, -1.5, 10.5)
P5, Q5, R5 = (0, 0), (3, 0), (0, 2)
P5b, Q5b, R5b = (8, 0), (8, 4.5), (5, 0)
assert abs(math.dist(P5b, Q5b) - 1.5 * 3) < 1e-9 and abs(math.dist(P5b, R5b) - 1.5 * 2) < 1e-9
clip('kontrolle-figuren', 6, 'Ähnlichkeit sehen: Kontrollfragen zu ähnlichen Figuren',
     'Fünf Fragen: zwei Rechtecke vergleichen, Umfang mit k, k aus dem Flächenverhältnis, Fläche im Massstab und die '
     'entsprechende Ecke einer gedrehten Figur.',
     ['ähnliche Figuren', 'Flächenfaktor', 'Massstab', 'Kontrollfragen'], [
         sz('Frage 1',
            'Vier durch drei ist nicht dasselbe wie sechs durch vier. Die Seiten wachsen nicht mit demselben Faktor: nicht '
            'ähnlich.',
            f(r'\dfrac{4}{3} \approx 1.33 \neq \dfrac{6}{4} = 1.5', 300, 50, ein=1.0),
            graf(geo(-0.5, -1, 8), [V(recht(4, 3), 1, 0.12), V(recht(6, 4), 2, 0.08, gestrichelt=True),
                                     T(2, -0.55, '4', 1, g=30), T(4.25, 1.5, '3', 1, 'start', 30), T(5.0, -0.55, '6', 2, g=30), T(6.25, 2.3, '4', 2, 'start', 30)], ein=0.05)),
         sz('Frage 2',
            'Der Umfang ist eine Länge: drei mal zwölf gibt sechsunddreissig Zentimeter.',
            f(r"u' = 3 \cdot 12 = \fc{36\,\mathrm{cm}}", 300, 52, ein=1.0)),
         sz('Frage 3',
            'Die Fläche wächst mit k im Quadrat. Sechzehn ist vier im Quadrat, also ist k gleich vier.',
            f(r'k^2 = 16 \;\Rightarrow\; \fc{k = 4}', 300, 52, ein=1.0)),
         sz('Frage 4',
            'Flächen wachsen mit eintausend im Quadrat: fünf Millionen Quadratzentimeter, das sind fünfhundert Quadratmeter.',
            f(r'5\,\mathrm{cm}^2 \cdot 1000^2 = 5\,000\,000\,\mathrm{cm}^2', 300, 44, ein=1.0),
            f(r'= \fc{500\,\mathrm{m}^2}', 410, 48, ein=1.0)),
         sz('Frage 5',
            'Q liegt am langen Schenkel des rechten Winkels. Im Bild ist der lange Schenkel der senkrechte: Q Strich liegt oben.',
            n('Ecke am langen Schenkel|des rechten Winkels', 300, 'blau', 46, ein=1.0),
            graf(WK3, [V([P5, Q5, R5], 1, 0.14), RW(P5, 0, 90, 1), V([P5b, Q5b, R5b], 2, 0.10, gestrichelt=True), RW(P5b, 90, 180, 2),
                       T(-0.4, -0.65, 'P', 1, g=30), T(3.3, -0.65, 'Q', 1, g=30), T(-0.45, 2.15, 'R', 1, g=30)], ein=0.05),
            graf(WK3, [PK(Q5b, 3, 0.15), T(8.5, 4.6, 'Q′', 3, 'start', 32)], ein=1.0, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Längen mal k, Flächen mal k im Quadrat. Und ähnlich ist nur, was in allen Seiten denselben Faktor '
            'hat.',
            titel('Zum Mitnehmen', 250, 76),
            n('Längen @\\cdot\\, k@, Flächen @\\cdot\\, k^2@|alle Seiten mit demselben @k@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Ein Rechteck 4 × 3 und ein Rechteck 6 × 4: Sind sie ähnlich?', ['nein', 'ja, k = 1.5', 'ja, k ≈ 1.33'], 0,
              {0: 'Ja.', 1: 'Die langen Seiten: 6 : 4 = 1.5. Und die kurzen Seiten, 4 : 3?', 2: 'Die kurzen Seiten: 4 : 3 ≈ 1.33. Und die langen Seiten, 6 : 4?'},
              sprich='Ein Rechteck vier mal drei und ein Rechteck sechs mal vier: Sind sie ähnlich?',
              rueck_sprich={1: 'Die langen Seiten: sechs durch vier ist eins Komma fünf. Und die kurzen Seiten, vier durch drei?',
                            2: 'Die kurzen Seiten: vier durch drei ist rund eins Komma drei drei. Und die langen Seiten, sechs durch vier?'}),
         wahl('Frage 2', 'k = 3, der Umfang des Originals ist 12 cm. Wie gross ist der Umfang des Bildes?', ['36 cm', '108 cm', '15 cm'], 0,
              {0: 'Ja.', 1: 'Das ist mit k² gerechnet. Ist der Umfang eine Länge oder eine Fläche?', 2: 'Strecken heisst multiplizieren.'},
              sprich='k gleich drei, der Umfang des Originals ist zwölf Zentimeter. Wie gross ist der Umfang des Bildes?',
              rueck_sprich={1: 'Das ist mit k im Quadrat gerechnet. Ist der Umfang eine Länge oder eine Fläche?', 2: 'Strecken heisst multiplizieren.'}),
         wahl('Frage 3', 'Die Fläche einer Figur wird 16-mal so gross, die Form bleibt. Mit welchem Faktor k wachsen die Längen?', ['k = 4', 'k = 16', 'k = 8'], 0,
              {0: 'Ja.', 1: '16 ist das Flächenverhältnis, also k². Wie gross ist dann k?', 2: 'k² heisst k mal k, nicht 2 mal k.'},
              sprich='Die Fläche einer Figur wird sechzehnmal so gross, die Form bleibt. Mit welchem Faktor k wachsen die Längen?',
              rueck_sprich={1: 'Sechzehn ist das Flächenverhältnis, also k im Quadrat. Wie gross ist dann k?', 2: 'k im Quadrat heisst k mal k, nicht zwei mal k.'}),
         wahl('Frage 4', 'Massstab 1 : 1000. Auf dem Plan hat ein Garten 5 cm². Wie gross ist er in Wirklichkeit?', ['500 m²', '0.5 m²', '50 000 m²'], 0,
              {0: 'Ja.', 1: 'Das ist mit 1000 statt 1000² gerechnet. Flächen wachsen mit dem Quadrat.', 2: 'Umrechnen: 1 m² sind 10 000 cm², nicht 100.'},
              sprich='Massstab eins zu tausend. Auf dem Plan hat ein Garten fünf Quadratzentimeter. Wie gross ist er in Wirklichkeit?',
              rueck_sprich={1: 'Das ist mit tausend statt tausend im Quadrat gerechnet. Flächen wachsen mit dem Quadrat.',
                            2: 'Umrechnen: Ein Quadratmeter sind zehntausend Quadratzentimeter, nicht hundert.'}),
         # Ziel Q′(8|4.5); Fallen R′(5|0) und P′(8|0), Abstand ≥ 3; Toleranz 0.8.
         klick('Frage 5', 'Das orange Dreieck ist das Bild des blauen, gestreckt und gedreht. Tipp die Ecke an, die zu Q gehört.', list(Q5b), 'Getroffen: Q′ liegt am langen Schenkel.',
               [{'bei': list(R5b), 'text': 'Diese Ecke liegt am kurzen Schenkel des rechten Winkels — sie gehört zu R.',
                 'sprich': 'Diese Ecke liegt am kurzen Schenkel des rechten Winkels. Sie gehört zu R.'},
                {'bei': list(P5b), 'text': 'Das ist die Ecke mit dem rechten Winkel — sie gehört zu P.',
                 'sprich': 'Das ist die Ecke mit dem rechten Winkel. Sie gehört zu P.'}],
               FALSCH, sprich='Das orange Dreieck ist das Bild des blauen, gestreckt und gedreht. Tipp die Ecke an, die zu Q gehört.', falsch_sprich=FALSCH, tol=0.8),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# ABC wie Arbeitsbereich 4 und Animation 5: α = 50°, β = 70°, γ = 60°, c = 4. PQR: P = 70°, Q = 60°, R = 50°, k = 1.5.
def dreieck(al, be, c, x0=0.0, y0=0.0):
    ga = 180 - al - be
    b = c * math.sin(math.radians(be)) / math.sin(math.radians(ga))
    return (x0, y0), (x0 + c, y0), (x0 + b * math.cos(math.radians(al)), y0 + b * math.sin(math.radians(al)))
A4, B4, C4 = dreieck(50, 70, 4, 0, 0)
a4 = math.dist(B4, C4); b4 = math.dist(A4, C4)            # 3.538, 4.340
# PQR: Ecke R ↔ A (50°), P ↔ B (70°), Q ↔ C (60°); Seiten mal 1.5, gedreht um 180° + 25°, verschoben
def dreh(p, w, s=1.0):
    r = math.radians(w)
    return (s * (p[0] * math.cos(r) - p[1] * math.sin(r)), s * (p[0] * math.sin(r) + p[1] * math.cos(r)))
_R, _P, _Q = [dreh(p, 155, 1.5) for p in (A4, B4, C4)]
mx = min(p[0] for p in (_R, _P, _Q)); my = min(p[1] for p in (_R, _P, _Q))
R4, P4, Q4 = [(p[0] - mx + 5.3, p[1] - my + 0.0) for p in (_R, _P, _Q)]
PR, PQ_, QR = math.dist(P4, R4), math.dist(P4, Q4), math.dist(Q4, R4)
assert abs(math.dist(R4, P4) - 6) < 1e-9          # RP ↔ AB (gegenüber 60° = Q)
assert abs(PQ_ - 1.5 * a4) < 1e-9                  # PQ ↔ BC (gegenüber 50° = R)
W4 = geo(-0.8, -1.6, 13.0, 640)
GR4 = dict(y=240, hoehe=640)
DR1 = [V([A4, B4, C4], 1, 0.14), WI(A4, B4, C4, 1, 40), WI(B4, C4, A4, 1, 40), WI(C4, A4, B4, 1, 40),
       T(1.15, 0.3, '50°', 1, g=26), T(2.95, 0.3, '70°', 1, g=26), T(2.75, 2.45, '60°', 1, g=26)] + ecken([('A', A4), ('B', B4), ('C', C4)], 1, 0.45)
def winkeltext(p, q, r_, text, farbe, abst=1.05, g=26):
    w = math.radians((richtung(p, q) + richtung(p, r_)) / 2 + (180 if abs(richtung(p, q) - richtung(p, r_)) > 180 else 0))
    return T(p[0] + abst * math.cos(w), p[1] + abst * math.sin(w) - 0.12, text, farbe, g=g)
DR2 = [V([P4, Q4, R4], 2, 0.10, gestrichelt=True), WI(P4, Q4, R4, 2, 40), WI(Q4, R4, P4, 2, 40), WI(R4, P4, Q4, 2, 40),
       winkeltext(P4, Q4, R4, '70°', 2), winkeltext(Q4, R4, P4, '60°', 2), winkeltext(R4, P4, Q4, '50°', 2)] + ecken([('P', P4), ('Q', Q4), ('R', R4)], 2, 0.5)
DR1_60, DR2_60 = DR1[6], DR2[5]
assert DR1_60['text'] == '60°' and DR2_60['text'] == '60°'
# Schatten (Themenseite A6): Stab 1.80 m, Schatten 1.20 m; Baumschatten 7.80 m → 11.70 m
W4s = geo(-1.0, -2.0, 14.0)
_l = math.hypot(7.8, 11.7)
STUMMEL = (4.7 + 2.2 * 7.8 / _l, 2.2 * 11.7 / _l)       # 2.2 Einheiten des Strahls vom Schattenende aus (zeigt den Winkel)
assert abs((STUMMEL[1] - 0) / (STUMMEL[0] - 4.7) - 1.5) < 1e-9
# Höhe im rechtwinkligen Dreieck: p = 1.8 (an a), q = 3.2 (an b), c = 5, h = 2.4, a = 3, b = 4 — massstäblich mal 2
HK = 2.0
A4h, B4h, H4h, C4h = (0, 0), (5 * HK, 0), (3.2 * HK, 0), (3.2 * HK, 2.4 * HK)
W4h = geo(-0.8, -2.0, 11.6)
clip('dreiecke', 7, 'Ähnlichkeit sehen: ähnliche Dreiecke',
     'Zwei gleiche Winkel genügen (WW). Entsprechende Seiten liegen gleichen Winkeln gegenüber; k aus einem Paar. sss als '
     'zweiter Weg, Schattenwurf und die Höhe im rechtwinkligen Dreieck: h² = p · q.',
     ['ähnliche Dreiecke', 'Hauptähnlichkeitssatz', 'Höhensatz', 'Schattenwurf'], [
         sz('Zwei Winkel',
            'Zwei Dreiecke mit den Winkeln fünfzig und siebzig Grad: Der dritte ist bei beiden sechzig Grad. Darum haben sie '
            'dieselbe Form, sie sind ähnlich. Zwei gleiche Winkel genügen.',
            f(r'180° - 50° - 70° = 60°', 300, 50, ein=4.2),
            n('zwei gleiche Winkel @\\Rightarrow@ ähnlich (WW)', 420, 'blau', 42, ein=8.1),
            # der dritte Winkel (60°) erst mit der Rechnung (4.2 s, «der Dritte ist bei beiden sechzig Grad», gemessen)
            graf(W4, [e for e in DR1 if e is not DR1_60], ein=0.3, **GR4),
            graf(W4, [e for e in DR2 if e is not DR2_60], ein=1.5, raster=False, **GR4),
            graf(W4, [DR1_60, DR2_60], ein=4.2, raster=False, **GR4)),
         sz('Zuordnen',
            'Entsprechende Seiten liegen gleichen Winkeln gegenüber. A B liegt sechzig Grad gegenüber, im zweiten Dreieck ist '
            'das R P.',
            n('gleichen Winkeln gegenüber', 300, 'blau', 44, ein=0.6),
            f(r'AB \;\leftrightarrow\; RP', 410, 50, ein=6.7),
            graf(W4, DR1 + DR2, ein=0.05, **GR4),
            graf(W4, [S(A4, B4, 3, dicke=9)], ein=3.6, raster=False, **GR4),
            graf(W4, [S(R4, P4, 3, dicke=9)], ein=6.7, raster=False, **GR4)),
         sz('Rechnen',
            'A B ist vier, R P ist sechs: k gleich eins Komma fünf. Die Seite B C gegenüber fünfzig Grad wird zu P Q, rund drei '
            'Komma fünf vier mal eins Komma fünf, also rund fünf Komma drei eins.',
            f(r'k = \dfrac{\overline{RP}}{\overline{AB}} = \dfrac{6}{4} = \fb{1.5}', 300, 48, ein=3.3),
            f(r'\overline{PQ} = 1.5 \cdot \overline{BC}', 460, 44, ein=7.2),
            f(r'\approx 1.5 \cdot 3.54 \approx \fc{5.31}', 570, 44, ein=10.8),
            graf(W4, DR1 + DR2 + [T(2.0, -0.75, '4', 1, g=30), seitentext(R4, P4, '6', Q4, 2, 0.55, 30)], ein=0.05, **GR4),
            graf(W4, [S(B4, C4, 3, dicke=9)], ein=4.8, raster=False, **GR4),
            graf(W4, [S(P4, Q4, 3, dicke=9)], ein=7.1, raster=False, **GR4)),
         sz('Seitenverhältnisse',
            'Statt der Winkel genügen auch die Seitenverhältnisse: vier, fünf, sechs und sechs, sieben Komma fünf, neun. Alle '
            'drei Verhältnisse sind eins Komma fünf, die Dreiecke sind ähnlich. Bei sechs, sieben Komma fünf, acht stimmt das '
            'dritte nicht.',
            f(r'4,\ 5,\ 6 \quad \text{und} \quad 6,\ 7.5,\ 9', 300, 46, ein=3.3),
            f(r'\dfrac{6}{4} = \dfrac{7.5}{5} = \dfrac{9}{6} = 1.5', 410, 48, ein=7.6),
            n('ähnlich (sss)', 540, 'blau', 44, ein=10.4),
            f(r'6,\ 7.5,\ \fd{8}: \; \fd{\dfrac{8}{6} \approx 1.33 \neq 1.5}', 640, 44, ein=13.7)),
         sz('Schatten',
            'Die Sonnenstrahlen sind parallel, Stab und Baum stehen senkrecht: Die Schattendreiecke stimmen in zwei Winkeln '
            'überein. Der Stab ist eins Komma acht Meter hoch, sein Schatten eins Komma zwei Meter lang. Der Baumschatten ist '
            'sieben Komma acht Meter lang, also ist der Baum elf Komma sieben Meter hoch.',
            f(r'\dfrac{h}{7.80} = \dfrac{1.80}{1.20}', 300, 50, ein=13.5),
            f(r'h = 7.80 \cdot 1.5 = \fc{11.70\,\mathrm{m}}', 430, 48, ein=15.2),
            # Ohne Karo, und der Baum steht erst mit dem Ergebnis (15.2 s, «also ist der Baum elf Komma sieben», gemessen) in
            # seiner Höhe da: vorher eine gestrichelte Senkrechte bis zum Bildrand und nur ein Stück des Sonnenstrahls (der
            # ganze Strahl träfe die Senkrechte bei 11.7 — massstäblich abzulesen).
            graf(W4s, [S((-1, 0), (13, 0), 5, dicke=3), S((1.2, 0), (1.2, 1.8), 1, dicke=7), S((12.5, 0), (12.5, 12.0), 5, True, 2),
                       S((0, 0), (1.2, 1.8), 2, True, 2.5), S((4.7, 0), STUMMEL, 2, True, 2.5),
                       RW((1.2, 0), 90, 180, 5), RW((12.5, 0), 90, 180, 5), WI((0, 0), (1, 0), (1.2, 1.8), 2, 50), WI((4.7, 0), (5.7, 0), (12.5, 11.7), 2, 50),
                       T(0.6, -0.75, '1.20', 5, g=26), T(8.6, -0.75, '7.80', 5, g=26), T(1.45, 0.8, '1.80', 1, 'start', 26)], ein=0.3, raster=False),
            graf(W4s, [T(12.15, 5.85, 'h = ?', 5, 'end', 30)], ein=0.3, aus=15.2, raster=False),
            graf(W4s, [S((4.7, 0), (12.5, 11.7), 2, True, 2.5), S((12.5, 0), (12.5, 11.7), 3, dicke=7), T(12.15, 5.85, 'h', 3, 'end', 32)], ein=15.2, raster=False)),
         sz('Höhe',
            'Im rechtwinkligen Dreieck teilt die Höhe die Hypotenuse in p und q. Die beiden Teildreiecke sind zum ganzen ähnlich. '
            'Daraus folgt: h im Quadrat gleich p mal q. Mit p gleich eins Komma acht und q gleich drei Komma zwei ist h gleich '
            'zwei Komma vier.',
            f(r'\dfrac{h}{p} = \dfrac{q}{h} \;\Rightarrow\; h^2 = p \cdot q', 300, 48, ein=7.8),
            f(r'h = \sqrt{1.8 \cdot 3.2} = \sqrt{5.76} = \fc{2.4}', 430, 46, ein=13.9),
            graf(W4h, [V([A4h, B4h, C4h], 1, 0.10), S(C4h, H4h, 2, dicke=5), RW(H4h, 0, 90, 2), RW(C4h, 216.87, 306.87, 5)]
                 + ecken([('A', A4h), ('B', B4h), ('C', C4h)], 1, 0.45) + [T(6.4, -0.75, 'H', 5, g=30)], ein=0.3, raster=False),   # ohne Karo: h nicht abzählbar
            # Teildreiecke orange und grau (Bilder des ganzen), gegebene p, q neutral — Grün bleibt dem Ergebnis h = 2.4
            graf(W4h, [V([A4h, H4h, C4h], 2, 0.18), V([H4h, B4h, C4h], 5, 0.14)], ein=4.8, raster=False),
            graf(W4h, [T(3.2, -1.35, 'q = 3.2', 5, g=28), T(8.2, -1.35, 'p = 1.8', 5, g=28), T(6.65, 2.4, 'h', 5, 'start', 32)], ein=3.6, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Zwei gleiche Winkel genügen. Entsprechende Seiten liegen gleichen Winkeln gegenüber, und k kommt aus '
            'einem Paar entsprechender Seiten.',
            titel('Zum Mitnehmen', 250, 76),
            n('zwei gleiche Winkel genügen (WW)|zuordnen über die Winkel|@k@ aus einem Paar entsprechender Seiten', 400, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
# Frage 2: ABC mit 45° bei A, 75° bei B, 60° bei C, c = 4; KLM ist das Bild, mal 1.25, gespiegelt und gedreht:
# K ↔ C (60°), L ↔ A (45°), M ↔ B (75°). Gesucht: die Seite, die BC (gegenüber 45°) entspricht → KM (gegenüber L).
A6, B6, C6 = dreieck(45, 75, 4, 0, 0)
def spiegeln_drehen(p, w, s):
    return dreh((p[0], -p[1]), w, s)
_L, _M, _K = [spiegeln_drehen(p, 100, 1.25) for p in (A6, B6, C6)]
mx = min(p[0] for p in (_L, _M, _K)); my = min(p[1] for p in (_L, _M, _K))
L6, M6, K6 = [(p[0] - mx + 5.8, p[1] - my + 0.3) for p in (_L, _M, _K)]
assert abs(math.dist(K6, M6) - 1.25 * math.dist(B6, C6)) < 1e-9
WK4 = geo(-0.8, -1.5, 12.5)
ZIEL6 = [r3(K6), r3(M6)]
def mitte(p, q):
    return [round((p[0] + q[0]) / 2, 3), round((p[1] + q[1]) / 2, 3)]
clip('kontrolle-dreiecke', 8, 'Ähnlichkeit sehen: Kontrollfragen zu ähnlichen Dreiecken',
     'Fünf Fragen: zwei Winkel vergleichen, die entsprechende Seite antippen, drei Seitenverhältnisse prüfen, eine '
     'Schattenlänge und der Höhensatz.',
     ['ähnliche Dreiecke', 'Höhensatz', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der dritte Winkel ist beim ersten Dreieck fünfundsechzig Grad, beim zweiten achtunddreissig Grad. Beide haben '
            'achtunddreissig, siebenundsiebzig und fünfundsechzig Grad: Sie sind ähnlich.',
            f(r'180° - 38° - 77° = 65°', 300, 50, ein=1.0),
            f(r'180° - 77° - 65° = 38°', 410, 50, ein=1.0),
            n('alle drei Winkel gleich: ähnlich', 530, 'blau', 44, ein=1.0)),
         sz('Frage 2',
            'B C liegt dem Winkel bei A gegenüber, fünfundvierzig Grad. Im zweiten Dreieck liegen fünfundvierzig Grad bei L, '
            'gegenüber liegt K M.',
            f(r'BC \;\leftrightarrow\; KM', 300, 52, ein=1.0),
            graf(WK4, [V([A6, B6, C6], 1, 0.14), S(B6, C6, 1, dicke=8), WI(A6, B6, C6, 1, 40), WI(B6, C6, A6, 1, 40), WI(C6, A6, B6, 1, 40),
                       winkeltext(A6, B6, C6, '45°', 1), winkeltext(B6, C6, A6, '75°', 1), winkeltext(C6, A6, B6, '60°', 1)]
                 + ecken([('A', A6), ('B', B6), ('C', C6)], 1, 0.45)
                 + [V([K6, L6, M6], 2, 0.10, gestrichelt=True), WI(K6, L6, M6, 2, 40), WI(L6, M6, K6, 2, 40), WI(M6, K6, L6, 2, 40),
                    winkeltext(K6, L6, M6, '60°', 2), winkeltext(L6, M6, K6, '45°', 2), winkeltext(M6, K6, L6, '75°', 2)]
                 + ecken([('K', K6), ('L', L6), ('M', M6)], 2, 0.5), ein=0.05),
            graf(WK4, [S(K6, M6, 3, dicke=9)], ein=1.0, raster=False)),
         sz('Frage 3',
            'Der Grösse nach: acht durch vier ist zwei, zwölf durch sechs ist zwei, aber fünfzehn durch sieben ist nicht zwei. '
            'Nicht ähnlich.',
            f(r'\dfrac{8}{4} = \dfrac{12}{6} = 2, \quad \fd{\dfrac{15}{7} \approx 2.14}', 300, 46, ein=1.0),
            n('nicht ähnlich', 420, 'rot', 44, ein=1.0)),
         sz('Frage 4',
            'Schatten durch Höhe ist bei Stab und Mast gleich: s durch fünfzehn gleich eins Komma sechs durch zwei. Der Schatten '
            'des Masts ist zwölf Meter lang.',
            f(r'\dfrac{s}{15} = \dfrac{1.6}{2} \;\Rightarrow\; s = \fc{12\,\mathrm{m}}', 300, 48, ein=1.0)),
         sz('Frage 5',
            'Höhensatz: h im Quadrat gleich p mal q, also sechsunddreissig. Die Höhe ist sechs Zentimeter.',
            f(r'h^2 = 4 \cdot 9 = 36 \;\Rightarrow\; h = \fc{6\,\mathrm{cm}}', 300, 48, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Erst prüfen, ob die Dreiecke ähnlich sind, dann über die Winkel zuordnen und mit einem Paar '
            'entsprechender Seiten rechnen.',
            titel('Zum Mitnehmen', 250, 76),
            n('ähnlich? @\\to@ zuordnen @\\to@ @k@ @\\to@ rechnen', 400, 'blau', 44, ein=1.2)),
     ], [
         # Nicht die Themenseite A4a (40°, 75°): andere Winkel, und der dritte Winkel ist bei beiden ein anderer.
         wahl('Frage 1', 'Dreieck 1 hat die Winkel 38° und 77°, Dreieck 2 die Winkel 77° und 65°. Sind sie ähnlich?',
              ['ja, alle drei Winkel stimmen überein', 'nein, nur ein Winkel stimmt überein', 'ohne Seitenlängen nicht zu entscheiden'], 0,
              {0: 'Ja.', 1: 'Rechne bei beiden den dritten Winkel aus.', 2: 'Bei Dreiecken genügen die Winkel. Wie gross ist jeweils der dritte?'},
              sprich='Dreieck eins hat die Winkel achtunddreissig und siebenundsiebzig Grad, Dreieck zwei die Winkel siebenundsiebzig und fünfundsechzig Grad. Sind sie ähnlich?',
              rueck_sprich={1: 'Rechne bei beiden den dritten Winkel aus.', 2: 'Bei Dreiecken genügen die Winkel. Wie gross ist jeweils der dritte?'}),
         # Ziel: die Strecke KM; Fallen: die beiden anderen Seiten (ihre Mitten). Toleranz 0.55 (Abstand der Seitenmitten zu KM ≥ 1.4).
         klick('Frage 2', 'Die Dreiecke sind ähnlich. Tipp die Seite des orangen Dreiecks an, die BC entspricht.', ZIEL6, 'Getroffen: KM liegt 45° gegenüber, wie BC.',
               [{'bei': [r3(K6), r3(L6)], 'text': 'Diese Seite liegt 75° gegenüber. BC liegt dem Winkel 45° gegenüber.',
                 'sprich': 'Diese Seite liegt fünfundsiebzig Grad gegenüber. B C liegt dem Winkel fünfundvierzig Grad gegenüber.'},
                {'bei': [r3(L6), r3(M6)], 'text': 'Diese Seite liegt 60° gegenüber. BC liegt dem Winkel 45° gegenüber.',
                 'sprich': 'Diese Seite liegt sechzig Grad gegenüber. B C liegt dem Winkel fünfundvierzig Grad gegenüber.'}],
               FALSCH_LINIE, sprich='Die Dreiecke sind ähnlich. Tipp die Seite des orangen Dreiecks an, die B C entspricht.', falsch_sprich=FALSCH_LINIE, tol=0.55),
         wahl('Frage 3', 'Seiten 4, 6, 7 und 8, 12, 15: Sind die Dreiecke ähnlich?', ['nein', 'ja, k = 2', 'ja, k ≈ 2.14'], 0,
              {0: 'Ja.', 1: 'Prüf alle drei Verhältnisse, auch das der längsten Seiten.', 2: 'Prüf alle drei Verhältnisse, auch das der kürzesten Seiten.'},
              sprich='Seiten vier, sechs, sieben und acht, zwölf, fünfzehn: Sind die Dreiecke ähnlich?',
              rueck_sprich={1: 'Prüf alle drei Verhältnisse, auch das der längsten Seiten.', 2: 'Prüf alle drei Verhältnisse, auch das der kürzesten Seiten.'}),
         # Umgekehrt zur Themenseite A6 (dort Höhe aus dem Schatten): gesucht ist der Schatten. 18.75 = 15 · 2 : 1.6 (verkehrt),
         # 14.6 = 15 − 0.4 (Unterschied übertragen).
         wahl('Frage 4', 'Ein 2 m hoher Stab wirft 1.6 m Schatten. Wie lang ist gleichzeitig der Schatten eines 15 m hohen Masts?', ['12 m', '18.75 m', '14.6 m'], 0,
              {0: 'Ja.', 1: 'Der Schatten des Stabs ist kürzer, als der Stab hoch ist. Gilt das auch für den Mast?', 2: 'Nicht subtrahieren: Höhe und Schatten stehen im gleichen Verhältnis.'},
              sprich='Ein zwei Meter hoher Stab wirft eins Komma sechs Meter Schatten. Wie lang ist gleichzeitig der Schatten eines fünfzehn Meter hohen Masts?',
              rueck_sprich={1: 'Der Schatten des Stabs ist kürzer, als der Stab hoch ist. Gilt das auch für den Mast?', 2: 'Nicht subtrahieren. Höhe und Schatten stehen im gleichen Verhältnis.'}),
         wahl('Frage 5', 'Rechtwinkliges Dreieck: Die Höhe teilt die Hypotenuse in p = 4 cm und q = 9 cm. Wie lang ist h?', ['6 cm', '6.5 cm', '36 cm'], 0,
              {0: 'Ja.', 1: 'Das ist der Mittelwert. Was sagt der Höhensatz?', 2: 'Das ist h². Noch die Wurzel ziehen.'},
              sprich='Rechtwinkliges Dreieck: Die Höhe teilt die Hypotenuse in p gleich vier und q gleich neun Zentimeter. Wie lang ist h?',
              rueck_sprich={1: 'Das ist der Mittelwert. Was sagt der Höhensatz?', 2: 'Das ist h im Quadrat. Noch die Wurzel ziehen.'}),
     ], art='Kontrollclip')
