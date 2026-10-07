"""Erzeugt die zehn Drehbücher des Leitprogramms Planimetrie (06.10.2026).

  python3 scripts/lp/planimetrie/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie bei den Funktionen- und Gleichungen-Leitprogrammen: Rechnung und Notizen links (x 150),
die Figur rechts (x 1010, y 175, 760 × 760). Figuren zeichnet `graf` mit "figuren" und
"achsen": false (HOWTO-clips.md, «Figuren im Graf»). Das Fenster ist in x und y gleich geteilt
(gleich lange Bereiche bei 760 × 760), sonst würden Kreise zu Ellipsen.

Fragebild (HOWTO-leitprogramme §15): Bei den Klickfragen ist die Figur das Gegebene (ab 0.05,
mit Achsen, damit die Lage ablesbar ist); das Gesuchte — Lot, Höhenfuss, Mittellinie,
Berührpunkt, Bildpunkt — erscheint erst ab 1.2 s.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = die Figur                                         \\fa{…}
  2 orange = Hilfslinie, Element (Höhe, Mittellinie …), Streckfaktor  \\fb{…}
  3 grün   = gesuchte Grösse, Ergebnis, Fläche                  \\fc{…}
  4 rot    = Fehler, Gegenbeispiel                              \\fd{…}
  5 Tinte  = neutral (Bezugslinien, Beschriftung)
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150


# ---------------------------------------------------------------- Fenster und Figuren
def geo(x0, y0, span):
    """Karo ohne Achsen, gleich geteilt."""
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], achsen=False)


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def ach(x0, y0, span, xt, yt_):
    """Mit Achsen (für Klickfragen: die Lage ist ablesbar), gleich geteilt."""
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], xteilung=yt(*xt), yteilung=yt(*yt_))


def V(pkte, farbe=1, fu=0.12, **kw):
    return dict(art='vieleck', punkte=[list(p) for p in pkte], farbe=farbe, fuellung=fu, **kw)


def S(a, b, farbe=2, gest=False, dicke=4):
    d = dict(art='strecke', von=list(a), bis=list(b), farbe=farbe, dicke=dicke)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=30, kursiv=True):
    return dict(art='text', bei=[x, y], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=kursiv)


def RW(x, y, r1, r2, farbe=2):
    return dict(art='rechts', bei=[x, y], r1=r1, r2=r2, farbe=farbe)


def WI(x, y, von, bis, farbe=2, r=40):
    return dict(art='winkel', bei=[x, y], von=von, bis=bis, farbe=farbe, r_px=r)


def ML(x, y, idx, upx, farbe=3, g=22):
    """«M» mit tiefgestelltem Index (M_I, M_U) — das SVG kennt kein LaTeX. upx: Fenstereinheiten je Pixel."""
    return [T(x, y, 'M', farbe, 'start', g),
            T(round(x + 0.95 * g * upx, 3), round(y - 0.3 * g * upx, 3), idx, farbe, 'start', int(g * 0.7))]


def KR(mx, my, r, farbe=1, fu=0.0, **kw):
    return dict(art='kreis', m=[mx, my], r=r, farbe=farbe, fuellung=fu, **kw)


def SEK(mx, my, r, von, bis, farbe=3, fu=0.25):
    return dict(art='sektor', m=[mx, my], r=r, von=von, bis=bis, farbe=farbe, fuellung=fu)


def BOG(mx, my, r, von, bis, farbe=2, dicke=7):
    return dict(art='bogen', m=[mx, my], r=r, von=von, bis=bis, farbe=farbe, dicke=dicke)


def mit(fg, **kw):
    """Figur mit eigenem ein/aus/bewegung (HOWTO-clips, «Später einblenden, bewegen, mitlaufen»)."""
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def weich(q):
    return q * q * (3 - 2 * q)


def dicht(t0, t1, felder, schritt=0.05):
    """Stützpunkte alle 0.05 s (ein Bild je Stützpunkt) für Bewegungen, die nicht linear in den
    Feldern sind (Drehung, Winkelbögen an einer gezogenen Ecke). felder(u) mit u = 0 … 1, weich."""
    n_ = max(1, int(round((t1 - t0) / schritt)))
    return [[round(t0 + (t1 - t0) * i / n_, 3), felder(weich(i / n_))] for i in range(n_ + 1)]


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def richtung(p, q):
    """Richtung von p nach q in Grad, 0 … 360."""
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def graf(W, figuren=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def pt(x, y, farbe=3, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = bei
    return d


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=56, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=46, ein=2.4):
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
          tol=0.5, bei=0.3):
    # Bewusst ohne "eingabe" (anders als die Funktionen-LPs): Die Figuren stehen ohne Achsen,
    # Koordinaten waeren hier keine Antwort, die man ablesen kann.
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'


def clip(name, titel_, kurz, schlag, lektion, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/g5-2-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 'g5-2-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Planimetrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': [lektion], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-06',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Figuren sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms planimetrie; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# Grunddreieck der Kapitel 1: A(1|1), B(8|1), C(3|6) — spitzwinklig.
W1 = geo(-0.5, -1, 10)
A1, B1, C1 = (1, 1), (8, 1), (3, 6)
TRI1 = V([A1, B1, C1])
ECKEN1 = [T(0.55, 0.35, 'A'), T(8.45, 0.35, 'B'), T(3, 6.55, 'C')]



def ziehC1(felder):
    """C auf der Parallelen y = 6: 3 → 6.5 → 1.5 → 3 (Szene «Winkelsumme», 1.0–3.6 s), Felder je Lage von C."""
    bew = []
    for t0, t1, x0, x1 in ((1.0, 1.9, 3, 6.5), (1.9, 2.9, 6.5, 1.5), (2.9, 3.6, 1.5, 3)):
        teil = dicht(t0, t1, lambda u: felder((x0 + (x1 - x0) * u, 6)))
        bew += teil[1:] if bew else teil
    return bew


# Kleine Bilder der Schnittpunkte (Szene «Schnittpunkte»), links unter der Notiz, gleich geteilt:
# spitz 8.4 × 6.3 auf 240 × 180 px, stumpf 9 × 7 auf 270 × 210 px.
WS1 = dict(xbereich=[0.3, 8.7], ybereich=[0.3, 6.6], achsen=False)
WS2 = dict(xbereich=[-2.5, 6.5], ybereich=[-3, 4], achsen=False)
TRI1K = V([A1, B1, C1], dicke=2.5)
TRI2K = V([(0, 0), (6, 0), (-1, 3)], dicke=2.5)
PAN1 = lambda x: dict(x=x, y=560, breite=240, hoehe=180)
PAN2 = lambda x: dict(x=x, y=770, breite=270, hoehe=210)

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('dreiecke', 'Figuren sehen: Dreiecke beschreiben',
     'Ecken, Seiten und Winkel benennen; die Innenwinkelsumme 180° mit Wechselwinkeln; spezielle Dreiecke; '
     'Höhe, Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte mit ihren Schnittpunkten.',
     ['Dreieck', 'Innenwinkelsumme', 'Höhe', 'Seitenhalbierende', 'Winkelhalbierende', 'Mittelsenkrechte'], 'g5-2a', [
         sz('Beschriften',
            'Ein Dreieck beschriftet man gegen den Uhrzeigersinn: Ecken A, B und C. Die Seite a liegt der Ecke A gegenüber, '
            'b liegt B gegenüber, c liegt C gegenüber. Der Winkel bei A heisst Alpha, bei B Beta, bei C Gamma.',
            f(r'A,\ B,\ C \ \text{gegen den Uhrzeigersinn}', 300, 46, ein=0.4),
            f(r'\text{Seite } \fb{a} \text{ gegenüber } A', 400, 50, ein=5.0),
            f(r'\text{Winkel } \fb{\alpha} \text{ bei } A', 500, 50, ein=10.4),
            graf(W1, [TRI1] + ECKEN1, ein=0.3),
            # Seiten und Winkel einzeln, je zu ihrem Wort (Ton: a 5.4, b 7.3, c 8.8; Alpha 10.4, Beta 12.3, Gamma 13.4)
            graf(W1, [T(5.95, 3.75, 'a', 2)], ein=5.0),
            graf(W1, [T(1.5, 3.75, 'b', 2)], ein=7.3, raster=False),
            graf(W1, [T(4.5, 0.25, 'c', 2)], ein=8.8, raster=False),
            graf(W1, [WI(1, 1, 0, 68.2, 2), T(2.15, 1.55, 'α', 2, g=26)], ein=10.4),
            graf(W1, [WI(8, 1, 135, 180, 3), T(6.95, 1.5, 'β', 3, g=26)], ein=12.3, raster=False),
            graf(W1, [WI(3, 6, 248.2, 315, 1), T(3.35, 4.9, 'γ', 1, g=26)], ein=13.4, raster=False)),
         sz('Winkelsumme',
            'Warum ergeben die drei Winkel immer hundertachtzig Grad? Zieh durch C die Parallele zu AB. Links und rechts von C '
            'entstehen Wechselwinkel, genau so gross wie Alpha und Beta. Zusammen mit Gamma liegen sie auf einer Geraden: '
            'hundertachtzig Grad.',
            f(r'\alpha + \beta + \gamma = 180^\circ', 300, 60, ein=0.4),
            n('Parallele durch @C@: Wechselwinkel', 420, 'blau', 44, ein=5.4),
            # «die drei Winkel immer hundertachtzig Grad» (Ton 1.2–2.8): C wandert auf der Höhe 6 nach rechts,
            # nach links und zurück (wie in sim1), die drei Bögen laufen mit; vor der Parallelen (5.4) wieder bei (3 | 6).
            graf(W1, [mit(TRI1, bewegung=ziehC1(lambda C: {'punkte': [list(A1), list(B1), r3(C)]})),
                      mit(WI(1, 1, 0, 68.2, 2), bewegung=ziehC1(lambda C: {'bis': round(richtung(A1, C), 2)})),
                      mit(WI(8, 1, 135, 180, 3), bewegung=ziehC1(lambda C: {'von': round(richtung(B1, C), 2)})),
                      mit(WI(3, 6, 248.2, 315, 1, 30),
                          bewegung=ziehC1(lambda C: {'bei': r3(C), 'von': round(richtung(C, A1), 2),
                                                     'bis': round(richtung(C, B1), 2)})),
                      ECKEN1[0], ECKEN1[1], mit(ECKEN1[2], bewegung=ziehC1(lambda C: {'bei': [round(C[0], 3), 6.55]}))],
                 ein=0.3),
            graf(W1, [S((-0.5, 6), (9.5, 6), 5, True, 2.5)], ein=5.4),
            graf(W1, [WI(3, 6, 180, 248.2, 2), WI(3, 6, 315, 360, 3)], ein=8.3)),
         sz('Vorgelöst',
            'Zum Beispiel Alpha gleich fünfzig Grad und Beta gleich sechzig Grad. Dann ist Gamma hundertachtzig minus fünfzig '
            'minus sechzig, also siebzig Grad.',
            f(r'\alpha = 50^\circ, \quad \beta = 60^\circ', 300, 54, ein=0.4),
            f(r'\gamma = 180^\circ - 50^\circ - 60^\circ = \fc{70^\circ}', 420, 50, ein=4.4),
            # A(1|1), B(8|1), alpha 50°, beta 60° -> C(5.147 | 5.942), gamma 70° (Bogen 230°..300°)
            graf(W1, [V([A1, B1, (5.147, 5.942)]), T(0.55, 0.35, 'A'), T(8.45, 0.35, 'B'), T(5.147, 6.5, 'C'),
                      WI(1, 1, 0, 50, 2), T(2.45, 1.45, '50°', 2, g=26, kursiv=False)], ein=1.2),
            graf(W1, [WI(8, 1, 120, 180, 3), T(6.6, 1.45, '60°', 3, g=26, kursiv=False)], ein=2.8, raster=False),
            graf(W1, [WI(5.147, 5.942, 230, 300, 1), T(5.03, 4.45, '70°', 1, g=26, kursiv=False)], ein=7.7, raster=False)),
         sz('Spezielle Dreiecke',
            'Drei Sonderfälle haben eigene Namen. Im gleichschenkligen Dreieck sind zwei Seiten gleich lang und die Basiswinkel '
            'gleich gross. Im gleichseitigen sind alle Seiten gleich und alle Winkel sechzig Grad. Das rechtwinklige hat einen '
            'rechten Winkel.',
            n('gleichschenklig: Basiswinkel gleich|gleichseitig: alle Winkel @60^\\circ@|rechtwinklig: ein Winkel @90^\\circ@',
              300, 'blau', 44, ein=1.0),
            # Je Dreieck zu seinem Satz (Ton: gleichschenklig 2.5, gleich lang 4.9, Basiswinkel 5.9; gleichseitig 7.7,
            # Seiten gleich 9.1, sechzig Grad 10.3; rechtwinklig 11.7, rechten Winkel 12.9). Striche: Mitte der Seite, quer.
            # Die Spitze zieht jedes Dreieck in seine Sonderform (wie «einstellen» in sim1), bevor die Zeichen kommen:
            # gleichschenklig (1.5 | 4) → (2.5 | 4) bei 2.9–4.2; gleichseitig Höhe 3.8 → 2.598 bei 8.0–8.9;
            # rechtwinklig (2.3 | 8) → (1 | 8) bei 12.0–12.8.
            graf(W1, [V([(0.5, 0), (4.5, 0), (1.5, 4)], bewegung=[[2.9, {}], [4.2, {'punkte': [[0.5, 0], [4.5, 0], [2.5, 4]]}]]),
                      T(2.5, -0.75, 'gleichschenklig', 5, g=24, kursiv=False)], ein=2.5),
            graf(W1, [S((1.303, 2.098), (1.697, 1.902), 2, dicke=3), S((3.303, 1.902), (3.697, 2.098), 2, dicke=3)], ein=4.9, raster=False),
            graf(W1, [WI(0.5, 0, 0, 63.4, 2, 34), WI(4.5, 0, 116.6, 180, 2, 34)], ein=5.9, raster=False),
            graf(W1, [V([(5.5, 0), (8.5, 0), (7, 3.8)], bewegung=[[8.0, {}], [8.9, {'punkte': [[5.5, 0], [8.5, 0], [7, 2.598]]}]]),
                      T(7, -0.75, 'gleichseitig', 5, g=24, kursiv=False)], ein=7.7, raster=False),
            graf(W1, [S((7, -0.22), (7, 0.22), 2, dicke=3), S((7.559, 1.189), (7.941, 1.409), 2, dicke=3),
                      S((6.059, 1.409), (6.441, 1.189), 2, dicke=3)], ein=9.1, raster=False),
            graf(W1, [WI(5.5, 0, 0, 60, 2, 28), WI(8.5, 0, 120, 180, 2, 28), WI(7, 2.598, 240, 300, 2, 28)], ein=10.3, raster=False),
            graf(W1, [V([(1, 5), (5, 5), (2.3, 8)], bewegung=[[12.0, {}], [12.8, {'punkte': [[1, 5], [5, 5], [1, 8]]}]]),
                      T(3, 4.25, 'rechtwinklig', 5, g=24, kursiv=False)], ein=11.7, raster=False),
            graf(W1, [RW(1, 5, 0, 90)], ein=12.9, raster=False)),
         sz('Die Höhe',
            'Die Höhe ist das Lot von einer Ecke auf die Gerade durch die Gegenseite. Hier ist das Dreieck stumpf: Der Fusspunkt '
            'der Höhe von C liegt ausserhalb der Seite c, auf ihrer Verlängerung.',
            f(r'\fb{h_c}: \ \text{Lot von } C \text{ auf die Gerade } AB', 300, 46, ein=0.4),
            n('Fusspunkt auch ausserhalb', 420, 'blau', 44, ein=7.0),
            # Brücke zu sim1 («Mach das Dreieck stumpfwinklig»): zuerst spitz mit C(3.5 | 5), die Höhe zum Wort «Lot»
            # (Ton 1.4); bei «Hier ist das Dreieck stumpf» (4.0–5.0) wandert C nach (8 | 5), die Höhe läuft mit.
            # Der Fusspunkt (x = C.x) passiert B(5 | 1) bei 4.53 s — dann erscheint die Verlängerung.
            graf(W1, [mit(V([(1, 1), (5, 1), (3.5, 5)]), bewegung=[[4.1, {}], [5.2, {'punkte': [[1, 1], [5, 1], [8, 5]]}]]),
                      T(0.55, 0.35, 'A'), T(5, 0.35, 'B'),
                      mit(T(3.85, 5.4, 'C'), bewegung=[[4.1, {}], [5.2, {'bei': [8.35, 5.4]}]]),
                      mit(S((5, 1), (9.3, 1), 5, True, 2.5), ein=4.45),
                      mit(S((3.5, 5), (3.5, 1), 2, True), ein=1.4,
                          bewegung=[[4.1, {}], [5.2, {'von': [8, 5], 'bis': [8, 1]}]]),
                      mit(RW(3.5, 1, 180, 90), ein=1.4, bewegung=[[4.1, {}], [5.2, {'bei': [8, 1]}]]),
                      mit(T(3.95, 3, 'h', 2, 'start'), ein=1.4, bewegung=[[4.1, {}], [5.2, {'bei': [8.45, 3]}]])],
                 ein=0.3)),
         sz('Drei weitere Linien',
            'Die Seitenhalbierende verbindet eine Ecke mit der Mitte der Gegenseite. Die Winkelhalbierende teilt den Winkel in '
            'zwei gleiche Hälften. Die Mittelsenkrechte steht in der Mitte einer Seite senkrecht auf ihr.',
            f(r'\fb{s_c}: \ C \to \text{Mitte von } c', 300, 48, ein=0.4),
            f(r'\fc{w_\gamma}: \ \text{halbiert } \gamma', 400, 48, ein=4.1),
            f(r'\text{Mittelsenkrechte}: \ \perp c \text{ in der Mitte}', 500, 46, ein=7.5),
            graf(W1, [TRI1] + ECKEN1, ein=0.3),
            graf(W1, [S(C1, (4.5, 1), 2), T(5.15, 0.25, 'M', 2, g=24)], ein=0.4),
            graf(W1, [S(C1, (4.026, 1), 3)], ein=4.1),
            graf(W1, [S((4.5, -0.6), (4.5, 8.5), 5, True, 2.5), RW(4.5, 1, 0, 90, 5)], ein=7.5)),
         sz('Schnittpunkte',
            'Je drei gleiche Linien treffen sich in einem Punkt. Die drei Seitenhalbierenden schneiden sich im Schwerpunkt S. '
            'Ebenso schneiden sich die Höhen, die Winkelhalbierenden und die Mittelsenkrechten je in einem Punkt. '
            'Beim stumpfen Dreieck liegen der Höhenschnittpunkt und der Umkreismittelpunkt aussen.',
            n('Seitenhalbierende: Schwerpunkt @S@|Höhen: Höhenschnittpunkt @H@|Winkelhalbierende: @M_I@|Mittelsenkrechte: @M_U@',
              300, 'blau', 44, ein=0.6),
            graf(W1, [TRI1] + ECKEN1 + [S(A1, (5.5, 3.5), 2, dicke=3), S(B1, (2, 3.5), 2, dicke=3), S(C1, (4.5, 1), 2, dicke=3)],
                 punkte=[pt(4, 8 / 3, 3, 'S', [4.3, 3.25])], ein=0.3),
            # Kleine Bilder unter der Notiz, je zu ihrem Wort (Ton: Höhen 7.6, Winkelhalbierenden 8.1,
            # Mittelsenkrechten 9.4; «Beim stumpfen» 11.2, «Umkreismittelpunkt» 14.2). Nachgerechnet:
            # spitz A(1|1) B(8|1) C(3|6): H(3|3), M_I(3.657|2.799), M_U(4.5|2.5);
            # stumpf A(0|0) B(6|0) C(−1|3): H(−1|−2.333), M_U(3|2.667) — beide ausserhalb.
            graf(WS1, [TRI1K, S(A1, (4.5, 4.5), 2, dicke=2.5), S(B1, (1.966, 3.414), 2, dicke=2.5), S(C1, (3, 1), 2, dicke=2.5),
                       T(3.2, 1.95, 'H', 3, 'start', 22)],
                 punkte=[pt(3, 3, 3)], ein=7.6, **PAN1(150)),
            graf(WS1, [TRI1K, S(A1, (5.174, 3.826), 2, dicke=2.5), S(B1, (1.995, 3.487), 2, dicke=2.5),
                       S(C1, (4.026, 1), 2, dicke=2.5)] + ML(4.2, 1.3, 'I', 0.0375),
                 punkte=[pt(3.657, 2.799, 3)], ein=8.1, **PAN1(420)),
            graf(WS1, [TRI1K, S((4.5, 0.3), (4.5, 6.6), 2, dicke=2.5), S((0, 4.3), (6, 1.9), 2, dicke=2.5),
                       S((3.5, 1.5), (6.3, 4.3), 2, dicke=2.5)] + ML(4.7, 1.15, 'U', 0.0375),
                 punkte=[pt(4.5, 2.5, 3)], ein=9.4, **PAN1(690)),
            graf(WS2, [TRI2K, S((0, 0), (-2.3, 0), 5, True, 2), S((0, 0), (0.75, -2.25), 5, True, 2),
                       S((-1, 3), (-1, -2.333), 2, dicke=2.5), S((6, 0), (-1, -2.333), 2, dicke=2.5),
                       S((0.931, 2.172), (-1, -2.333), 2, dicke=2.5), T(-1.4, -2.2, 'H', 3, 'end', 22),
                       T(4.6, 3.1, 'stumpf', 5, 'middle', 20, False)],
                 punkte=[pt(-1, -2.333, 3)], ein=11.2, **PAN2(150)),
            graf(WS2, [TRI2K, S((3, -0.8), (3, 3.6), 2, dicke=2.5), S((-1.55, 1.15), (3.875, 2.958), 2, dicke=2.5),
                       S((2.15, 0.683), (3.2, 3.133), 2, dicke=2.5)] + ML(3.45, 3.25, 'U', 0.0354),
                 punkte=[pt(3, 2.667, 3)], ein=14.2, **PAN2(450))),
         sz('Merke',
            'Zum Mitnehmen: Die Innenwinkel ergeben zusammen hundertachtzig Grad. Die Höhe ist das Lot auf die Gerade durch die '
            'Gegenseite, ihr Fusspunkt kann ausserhalb liegen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\alpha + \beta + \gamma = 180^\circ', 400, 56, ein=1.2),
            n('Höhe: Lot auf die Gerade der Gegenseite', 520, 'blau', 44, ein=4.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
WH = geo(-0.5, -4, 11.5)                       # stumpfes Dreieck mit H aussen
WK1 = ach(-4, -3, 10, (-3, -2, -1, 1, 2, 3, 4, 5), (-2, -1, 1, 2, 3, 4, 5, 6))
clip('kontrolle-dreiecke', 'Figuren sehen: Kontrollfragen zu Dreiecken',
     'Fünf Fragen zu Beschriftung, Winkelsumme, Schnittpunkten, gleichschenkligen Dreiecken und zum Fusspunkt einer Höhe.',
     ['Dreieck', 'Höhe', 'Kontrollfragen'], 'g5-2a', [
         sz('Frage 1',
            'Die Seite a liegt der Ecke A gegenüber. Sie verbindet B und C.',
            f(r'a = \overline{BC}', 300, 60, ein=1.0),
            graf(W1, [TRI1] + ECKEN1 + [S(B1, C1, 2, dicke=7), T(5.95, 3.75, 'a', 2)], ein=1.0)),
         sz('Frage 2',
            'Hundertachtzig minus achtundvierzig minus fünfundsiebzig ergibt siebenundfünfzig Grad.',
            f(r'\gamma = 180^\circ - 48^\circ - 75^\circ = \fc{57^\circ}', 300, 50, ein=1.0)),
         sz('Frage 3',
            'Im stumpfen Dreieck schneiden sich die Höhen ausserhalb. Schwerpunkt und Inkreismittelpunkt liegen immer innen.',
            f(r'\text{stumpf: } H \text{ aussen}', 300, 56, ein=1.0),
            graf(WH, [V([(1, 1), (5, 1), (7, 4)]), T(0.55, 0.35, 'A'), T(5.1, 0.35, 'B'), T(7.4, 4.35, 'C'),
                      S((7, 4), (7, -3.6), 2, True, 3), S((1, 1), (7.6, -3.4), 2, True, 3), S((5, 1), (7.3, -3.6), 2, True, 3)],
                 punkte=[pt(7, -3, 3, 'H', [7.4, -2.6])], ein=1.0)),
         sz('Frage 4',
            'Hundertachtzig minus dreissig sind hundertfünfzig Grad. Die zwei Basiswinkel teilen sich das: je fünfundsiebzig Grad.',
            f(r'(180^\circ - 30^\circ) : 2 = \fc{75^\circ}', 300, 54, ein=1.0)),
         sz('Frage 5',
            'Die Höhe steht senkrecht auf der Geraden durch A und B. Ihr Fusspunkt liegt bei minus zwei, null — '
            'auf der Verlängerung, ausserhalb der Seite.',
            f(r'\text{Fusspunkt } (\fc{-2} \mid 0)', 300, 56, ein=1.0),
            graf(WK1, [V([(0, 0), (4, 0), (-2, 3)]), T(0.3, -0.75, 'A'), T(4.25, 0.4, 'B', anker='start'), T(-2.3, 3.4, 'C')], ein=0.05),
            graf(WK1, [S((-3.5, 0), (0, 0), 5, True, 2.5), S((-2, 3), (-2, 0), 2, True), RW(-2, 0, 0, 90)],
                 punkte=[pt(-2, 0, 3, '(−2 | 0)', [-2.25, 0.45], 'end')], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Winkelsumme hundertachtzig Grad. Die Höhe ist ein Lot, auch ausserhalb.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\alpha + \\beta + \\gamma = 180^\\circ@|Höhe: Lot, Fusspunkt auch aussen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Welche Seite liegt der Ecke A gegenüber?', ['a', 'c', 'b'], 0,
              {0: 'Ja.', 1: 'c liegt C gegenüber. Und A?', 2: 'b liegt B gegenüber. Und A?'},
              sprich='Welche Seite liegt der Ecke A gegenüber?',
              rueck_sprich={1: 'c liegt C gegenüber. Und A?', 2: 'b liegt B gegenüber. Und A?'}),
         wahl('Frage 2', 'α = 48°, β = 75°: Wie gross ist γ?', ['57°', '123°', '47°'], 0,
              {0: 'Ja.', 1: 'Das ist α + β. Wie viel fehlt bis 180°?', 2: 'Rechne 180° − 48° − 75° nochmals.'},
              sprich='Alpha gleich achtundvierzig Grad, Beta gleich fünfundsiebzig Grad: Wie gross ist Gamma?',
              rueck_sprich={1: 'Das ist Alpha plus Beta. Wie viel fehlt bis hundertachtzig Grad?',
                            2: 'Rechne hundertachtzig minus achtundvierzig minus fünfundsiebzig nochmals.'}),
         wahl('Frage 3', 'Welcher Schnittpunkt kann ausserhalb des Dreiecks liegen?',
              ['der Höhenschnittpunkt H', 'der Schwerpunkt S', 'der Inkreismittelpunkt'], 0,
              {0: 'Ja.', 1: 'Die Seitenhalbierenden laufen alle durchs Innere. Welche Linien können hinausführen?',
               2: 'Die Winkelhalbierenden laufen alle durchs Innere. Welche Linien können hinausführen?'},
              sprich='Welcher Schnittpunkt kann ausserhalb des Dreiecks liegen?',
              rueck_sprich={1: 'Die Seitenhalbierenden laufen alle durchs Innere. Welche Linien können hinausführen?',
                            2: 'Die Winkelhalbierenden laufen alle durchs Innere. Welche Linien können hinausführen?'}),
         wahl('Frage 4', 'Gleichschenklig mit Spitzenwinkel 30°: Wie gross ist ein Basiswinkel?', ['75°', '150°', '30°'], 0,
              {0: 'Ja.', 1: 'Das sind beide Basiswinkel zusammen.', 2: 'Dann wäre die Summe 90°, nicht 180°.'},
              sprich='Gleichschenklig mit Spitzenwinkel dreissig Grad: Wie gross ist ein Basiswinkel?',
              rueck_sprich={1: 'Das sind beide Basiswinkel zusammen.', 2: 'Dann wäre die Summe neunzig Grad, nicht hundertachtzig.'}),
         klick('Frage 5', 'Tipp den Fusspunkt der Höhe von C ins Bild.', [-2, 0], 'Getroffen: (−2 | 0).',
               [{'bei': [0, 0], 'text': 'Das ist A. Die Höhe steht senkrecht auf der Geraden AB.',
                 'sprich': 'Das ist A. Die Höhe steht senkrecht auf der Geraden A B.'},
                {'bei': [2, 0], 'text': 'Das ist die Mitte von AB — die gehört zur Seitenhalbierenden.',
                 'sprich': 'Das ist die Mitte von A B. Die gehört zur Seitenhalbierenden.'}],
               FALSCH, sprich='Tipp den Fusspunkt der Höhe von C ins Bild.', falsch_sprich=FALSCH),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
W2 = geo(-0.5, -1, 10)
W2b = geo(-0.5, -2, 12)
clip('flaeche', 'Figuren sehen: Dreiecksfläche und zugehörige Höhe',
     'Zu jeder Grundseite gehört eine Höhe, der Abstand der Gegenecke zur Geraden der Grundseite. Zwei gleiche Dreiecke '
     'ergeben ein Parallelogramm: A = ½ · g · h. Vorgelöst am stumpfen Dreieck mit g = 8 cm und h = 3 cm.',
     ['Dreieck', 'Flächeninhalt', 'Höhe', 'Grundseite'], 'g5-2a', [
         sz('Grundseite und Höhe',
            'Jede Seite kann Grundseite sein. Die zugehörige Höhe ist der Abstand der gegenüberliegenden Ecke von der Geraden '
            'durch die Grundseite: senkrecht gemessen.',
            f(r'\text{Grundseite } g', 300, 52, ein=0.4),
            f(r'\text{Höhe } \fb{h} \perp g', 400, 52, ein=2.8),
            graf(W2, [V([(1, 1), (9, 1), (4, 4)]), T(5, 0.25, 'g', 5)], ein=0.3),
            graf(W2, [S((4, 4), (4, 1), 2, True), RW(4, 1, 0, 90), T(4.35, 2.4, 'h', 2, 'start')], ein=2.8)),
         sz('Warum die Hälfte',
            'Leg ein zweites, gleiches Dreieck gedreht daneben. Zusammen bilden sie ein Parallelogramm mit Grundseite g und '
            'Höhe h, also mit der Fläche g mal h. Das Dreieck ist genau die Hälfte.',
            f(r'A = \tfrac{1}{2} \cdot g \cdot h', 300, 62, ein=7.6),
            # «Leg ein zweites, gleiches Dreieck gedreht daneben» (Ton: zweites 1.25, gedreht 2.8, daneben 3.05–3.4):
            # die Kopie liegt ab 1.2 auf dem Original und dreht sich 1.9–3.3 um die Mitte von BC (4 | 2.5) um 180°
            # ("drehung" im Bauer: der Winkel wird übergeblendet, die Figur bleibt gleich gross);
            # der Bogen wächst mit. Drehzentrum, Bogen und «180°» sind ein Zwischenstand (aus 4.0).
            # Grundseite g (Ton 6.2) und Höhe h (6.8) zu ihrem Wort.
            graf(W2, [V([(0, 1), (6, 1), (2, 4)], 1, 0.2),
                      mit(V([(0, 1), (6, 1), (2, 4)], 2, 0.2), ein=1.2, um=[4, 2.5],
                          bewegung=[[1.9, {'drehung': 0}], [3.3, {'drehung': 180}]]),
                      mit(BOG(4, 2.5, 0.8, -36.9, -36.9, 2, 3), ein=1.9, aus=4.0,
                          bewegung=[[1.9, {}], [3.3, {'bis': 143.1}]]),
                      mit(T(4.9, 3.4, '180°', 2, 'start', 22, False), ein=3.2, aus=4.0),
                      mit(T(3, 0.25, 'g', 5), ein=6.1),
                      mit(S((2, 4), (2, 1), 5, True, 2.5), ein=6.7), mit(T(1.65, 2.5, 'h', 5, 'end'), ein=6.7)],
                 punkte=[dict(pt(4, 2.5, 5), ein=1.9, aus=4.0)], ein=0.3)),
         sz('Strategie',
            'Halt, bevor du rechnest: Grundseite wählen, die zugehörige Höhe bestimmen, die Einheiten angleichen, in die Formel '
            'einsetzen und das Ergebnis prüfen.',
            titel('Strategie', 260, 72),
            n('1. Grundseite wählen|2. zugehörige Höhe|3. Einheiten angleichen|4. Formel einsetzen|5. prüfen',
              380, 'blau', 46, ein=1.4)),
         sz('Stumpf vorgelöst',
            'Ein stumpfes Dreieck mit der Grundseite acht Zentimeter. Die Spitze liegt rechts ausserhalb. Die Höhe fällt auf die '
            'Verlängerung der Grundseite und ist drei Zentimeter lang. Also ist die Fläche ein Halb mal acht mal drei, gleich '
            'zwölf Quadratzentimeter. Probe: Das Rechteck acht mal drei hat vierundzwanzig, die Hälfte ist zwölf.',
            f(r'g = 8\,\text{cm}, \quad \fb{h} = 3\,\text{cm}', 300, 50, ein=0.4),
            f(r'A = \tfrac{1}{2} \cdot 8 \cdot 3 = \fc{12\,\text{cm}^2}', 410, 50, ein=9.3),
            n('Probe: Rechteck @8 \\cdot 3 = 24@, die Hälfte', 530, 'blau', 42, ein=13.4),
            graf(W2b, [V([(0, 1), (8, 1), (10, 4)]), T(4, 0.2, 'g = 8 cm', 5, kursiv=False)], ein=0.3),
            graf(W2b, [S((8, 1), (11, 1), 5, True, 2.5), S((10, 4), (10, 1), 2, True), RW(10, 1, 180, 90),
                      T(10.35, 2.4, 'h = 3', 2, 'start', g=26)], ein=5.0),
            # «Probe: Das Rechteck» (Ton 13.8): Rechteck 8 × 3 um Grundseite und Höhe
            graf(W2b, [V([(0, 1), (8, 1), (8, 4), (0, 4)], 3, 0.06, gestrichelt=True, dicke=3)], ein=13.8, raster=False)),
         sz('Spitze verschieben',
            'Schieb die Spitze parallel zur Grundseite. Die Form ändert sich, aber Grundseite und Höhe bleiben gleich. '
            'Darum bleibt auch die Fläche gleich: zwölf Quadratzentimeter.',
            f(r'g, \ h \text{ gleich} \;\Rightarrow\; A = 12\,\text{cm}^2', 300, 48, ein=5.6),
            # Brücke zu sim2 (Spitze t): «Schieb die Spitze …, die Form ändert sich» (Ton 0.5–3.6): C gleitet auf der
            # Parallelen von t = 2 nach t = 10. Die Höhe erscheint zum Wort «Höhe» (5.2) bei t = 10, mit Verlängerung;
            # bei «bleiben gleich … die Fläche gleich» (5.6–7.4) gleitet C zurück nach t = 2, die Höhe 3 läuft mit.
            # Der Fusspunkt passiert B(8 | 1) bei 6.19 s — dann geht die Verlängerung aus.
            graf(W2b, [S((-0.5, 4), (11.5, 4), 5, True, 2),
                       mit(V([(0, 1), (8, 1), (2, 4)]), bewegung=[[0.8, {}], [3.6, {'punkte': [[0, 1], [8, 1], [10, 4]]}],
                                                                  [5.6, {}], [7.4, {'punkte': [[0, 1], [8, 1], [2, 4]]}]]),
                       mit(S((8, 1), (10.8, 1), 5, True, 2.5), ein=5.1, aus=6.1),
                       mit(S((10, 4), (10, 1), 2, True, 3), ein=5.1, bewegung=[[5.6, {}], [7.4, {'von': [2, 4], 'bis': [2, 1]}]]),
                       mit(RW(10, 1, 180, 90), ein=5.1, bewegung=[[5.6, {}], [7.4, {'bei': [2, 1]}]]),
                       mit(T(10.35, 2.4, 'h = 3', 2, 'start', g=26), ein=5.1, bewegung=[[5.6, {}], [7.4, {'bei': [2.35, 2.4]}]])],
                 ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Fläche gleich ein Halb mal Grundseite mal zugehörige Höhe. Die Höhe misst den Abstand zur Geraden '
            'der Grundseite, auch ausserhalb.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'A = \tfrac{1}{2} \cdot g \cdot h', 400, 60, ein=1.2),
            n('@h@: Abstand zur Geraden durch @g@', 530, 'blau', 44, ein=4.6)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
WK2 = ach(-5, -3, 12, (-4, -3, -2, -1, 1, 2, 3, 4, 5, 6), (-2, -1, 1, 2, 3, 4, 5, 6, 7, 8))
clip('kontrolle-flaeche', 'Figuren sehen: Kontrollfragen zur Dreiecksfläche',
     'Fünf Fragen zur Lage der Höhe, zum Höhenfuss, zur Flächengleichheit und zu h aus A und g.',
     ['Dreieck', 'Flächeninhalt', 'Höhe', 'Kontrollfragen'], 'g5-2a', [
         sz('Frage 1',
            'Nein. Beim stumpfwinkligen Dreieck liegen zwei Höhen ausserhalb. Ihr Fusspunkt liegt auf der Verlängerung der Seite.',
            f(r'\text{stumpf: zwei Höhen aussen}', 300, 54, ein=1.0),
            graf(W2b, [V([(0, 1), (8, 1), (10, 4)]), S((8, 1), (11, 1), 5, True, 2.5), S((10, 4), (10, 1), 2, True),
                       RW(10, 1, 180, 90)], ein=1.0)),
         sz('Frage 2',
            'Eine Höhe steht senkrecht auf der Grundseite. Eine schräge Seite ist das nur im rechtwinkligen Dreieck.',
            f(r'\fb{h} \perp g', 300, 62, ein=1.0),
            graf(W2, [V([(1, 1), (9, 1), (4, 4)]), S((4, 4), (4, 1), 2, True), RW(4, 1, 0, 90), S((1, 1), (4, 4), 4, dicke=6)],
                 ein=1.0)),
         sz('Frage 3',
            'Die Höhe von C steht senkrecht auf der Geraden AB. Ihr Fusspunkt liegt bei minus drei, null.',
            f(r'\text{Fusspunkt } (\fc{-3} \mid 0)', 300, 56, ein=1.0),
            graf(WK2, [V([(0, 0), (6, 0), (-3, 4)]), T(0.3, -0.75, 'A'), T(6.25, 0.4, 'B', anker='start'), T(-3.35, 4.4, 'C')], ein=0.05),
            graf(WK2, [S((-4.5, 0), (0, 0), 5, True, 2.5), S((-3, 4), (-3, 0), 2, True), RW(-3, 0, 0, 90)],
                 punkte=[pt(-3, 0, 3, '(−3 | 0)', [-3.25, 0.5], 'end')], ein=1.2)),
         sz('Frage 4',
            'Die Spitze wandert auf einer Parallelen. Grundseite und Höhe bleiben gleich, also auch die Fläche.',
            f(r'g, \ h \text{ gleich} \;\Rightarrow\; A \text{ gleich}', 300, 50, ein=1.0),
            graf(W2b, [S((-0.5, 4), (11.5, 4), 5, True, 2), V([(0, 1), (8, 1), (2, 4)], 1, 0.08),
                       V([(0, 1), (8, 1), (6, 4)], 3, 0.08)], ein=1.0)),
         sz('Frage 5',
            'h gleich zwei mal Fläche durch Grundseite: zwei mal fünfzehn durch sechs, gleich fünf Zentimeter.',
            f(r'h = \dfrac{2A}{g} = \dfrac{2 \cdot 15}{6} = \fc{5\,\text{cm}}', 300, 50, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Die Höhe steht senkrecht auf der Geraden der Grundseite. Fläche gleich ein Halb mal g mal h.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'A = \tfrac{1}{2}\, g\, h \qquad h = \dfrac{2A}{g}', 400, 54, ein=1.2)),
     ], [
         wahl('Frage 1', 'Muss die Höhe innerhalb des Dreiecks liegen?',
              ['Nein — beim stumpfwinkligen Dreieck liegen zwei Höhen ausserhalb.', 'Ja, immer.', 'Nur im gleichseitigen Dreieck.'], 0,
              {0: 'Ja.', 1: 'Denk an ein stumpfes Dreieck: Wo trifft das Lot die Gerade der Grundseite?',
               2: 'Die Frage ist, ob sie innen liegen muss. Denk an ein stumpfes Dreieck.'},
              sprich='Muss die Höhe innerhalb des Dreiecks liegen?',
              rueck_sprich={1: 'Denk an ein stumpfes Dreieck. Wo trifft das Lot die Gerade der Grundseite?',
                            2: 'Die Frage ist, ob sie innen liegen muss. Denk an ein stumpfes Dreieck.'}),
         wahl('Frage 2', 'Ist jede schräge Seite eine Höhe?',
              ['Nein, eine Höhe steht senkrecht auf der Grundseite.', 'Ja.', 'Nur die längste Seite.'], 0,
              {0: 'Ja.', 1: 'Steht eine schräge Seite senkrecht auf der Grundseite?', 2: 'Was zeichnet eine Höhe aus?'},
              sprich='Ist jede schräge Seite eine Höhe?',
              rueck_sprich={1: 'Steht eine schräge Seite senkrecht auf der Grundseite?', 2: 'Was zeichnet eine Höhe aus?'}),
         klick('Frage 3', 'Tipp den Fusspunkt der Höhe zur Grundseite AB an.', [-3, 0], 'Getroffen: (−3 | 0).',
               [{'bei': [0, 0], 'text': 'Das ist A. Die Höhe steht senkrecht auf der Geraden AB, auch ausserhalb.',
                 'sprich': 'Das ist A. Die Höhe steht senkrecht auf der Geraden A B, auch ausserhalb.'},
                {'bei': [3, 0], 'text': 'Das ist die Mitte von AB. Gesucht ist das Lot von C.',
                 'sprich': 'Das ist die Mitte von A B. Gesucht ist das Lot von C.'}],
               FALSCH, sprich='Tipp den Fusspunkt der Höhe zur Grundseite A B an.', falsch_sprich=FALSCH),
         wahl('Frage 4', 'Die Spitze wandert parallel zur Grundseite. Warum bleibt die Fläche gleich?',
              ['g und h bleiben gleich.', 'Die Seiten bleiben gleich lang.', 'Sie bleibt nicht gleich.'], 0,
              {0: 'Ja.', 1: 'Die schrägen Seiten ändern sich. Was steht in der Formel?', 2: 'Was steht in der Flächenformel, und ändert es sich?'},
              sprich='Die Spitze wandert parallel zur Grundseite. Warum bleibt die Fläche gleich?',
              rueck_sprich={1: 'Die schrägen Seiten ändern sich. Was steht in der Formel?',
                            2: 'Was steht in der Flächenformel, und ändert es sich?'}),
         wahl('Frage 5', 'g = 6 cm, A = 15 cm²: Wie gross ist h?', ['5 cm', '2.5 cm', '45 cm'], 0,
              {0: 'Ja.', 1: 'Das ist A durch g. Denk an den Faktor ein Halb.', 2: 'Das wäre A mal g durch 2.'},
              sprich='g gleich sechs Zentimeter, A gleich fünfzehn Quadratzentimeter: Wie gross ist h?',
              rueck_sprich={1: 'Das ist A durch g. Denk an den Faktor ein Halb.', 2: 'Das wäre A mal g durch zwei.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
SCHUB_C = lambda felder: [[6.0, {}], [6.8, felder(2)], [7.6, felder(0)]]
W3 = geo(-0.5, -1, 10)
W3b = geo(-0.5, -1.5, 12)
clip('vierecke', 'Figuren sehen: Vierecke',
     'Die Vierecks-Familie; Flächen über das Rechteck: Parallelogramm a · h, Trapez mit Mittellinie, Raute und Drachen ½ e f; '
     'fehlende Längen mit Pythagoras.',
     ['Viereck', 'Parallelogramm', 'Trapez', 'Mittellinie', 'Raute', 'Drachen', 'Pythagoras'], 'g5-2b', [
         sz('Die Familie',
            'Die Vierecke sind eine Familie. Jedes Quadrat ist ein Rechteck, jedes Rechteck ein Parallelogramm, jedes '
            'Parallelogramm ein Trapez. Raute und Drachen haben gleich lange Seiten paarweise.',
            n('Quadrat @\\subset@ Rechteck @\\subset@|Parallelogramm @\\subset@ Trapez|dazu Raute und Drachen', 300, 'blau', 46, ein=0.6),
            graf(W3, [V([(0, 6), (2.5, 6), (2.5, 8.5), (0, 8.5)]), V([(4, 6), (8.5, 6), (8.5, 8.5), (4, 8.5)]),
                      V([(0, 2), (4, 2), (5, 4.5), (1, 4.5)]), V([(5.5, 2), (9.3, 2), (8.3, 4.5), (6.5, 4.5)]),
                      V([(2, -0.8), (3.5, 0.4), (2, 1.6), (0.5, 0.4)]), V([(7, -0.8), (8.2, 0.9), (7, 1.6), (5.8, 0.9)]),
                      T(1.25, 7.15, 'Quadrat', 5, g=22, kursiv=False), T(6.25, 7.15, 'Rechteck', 5, g=22, kursiv=False),
                      T(2.5, 3.15, 'Parallelogramm', 5, g=22, kursiv=False), T(7.4, 3.15, 'Trapez', 5, g=22, kursiv=False),
                      T(3.7, 0.3, 'Raute', 5, 'start', 22, False), T(8.35, 0.3, 'Drachen', 5, 'start', 22, False)]
                 # «Jedes Quadrat ist ein Rechteck, jedes Rechteck ein Parallelogramm, jedes Parallelogramm ein Trapez»
                 # (Ton 2.5 / 4.2–4.8 / 5.8–6.7): eine orange Kopie verformt sich je in die nächste Figur — eine
                 # Bedingung fällt weg (wie in sim3: aus dem Trapez wird mit c = 8 ein Parallelogramm).
                 + [mit(V(von_, 2, 0.06, gestrichelt=True, dicke=3), ein=t0 - 0.2, aus=t1 + 0.4,
                        bewegung=[[t0, {}], [t1, {'punkte': [list(p_) for p_ in nach]}]])
                    for von_, nach, t0, t1 in (
                        (((0, 6), (2.5, 6), (2.5, 8.5), (0, 8.5)), ((4, 6), (8.5, 6), (8.5, 8.5), (4, 8.5)), 2.6, 3.4),
                        (((4, 6), (8.5, 6), (8.5, 8.5), (4, 8.5)), ((0, 2), (4, 2), (5, 4.5), (1, 4.5)), 4.3, 5.2),
                        (((0, 2), (4, 2), (5, 4.5), (1, 4.5)), ((5.5, 2), (9.3, 2), (8.3, 4.5), (6.5, 4.5)), 5.9, 6.8))],
                 ein=0.3)),
         sz('Parallelogramm',
            'Schneid beim Parallelogramm links ein Dreieck ab und setz es rechts an: Es entsteht ein Rechteck mit der Grundseite '
            'a und der Höhe h. Also ist die Fläche a mal h.',
            f(r'A = a \cdot \fb{h}', 300, 62, ein=7.4),
            graf(W3, [V([(0, 1), (6, 1), (8, 4), (2, 4)]), S((2, 4), (2, 1), 2, True), RW(2, 1, 0, 90),
                      T(1.65, 2.4, 'h', 2, 'end'), T(3, 0.25, 'a', 5)], ein=0.3),
            # «links ein Dreieck ab und setz es rechts an» (Ton: Dreieck 2.4, setz 3.15–3.8): das grüne Stück liegt
            # zuerst links und wird um 6 nach rechts geschoben.
            graf(W3, [V([(0, 1), (2, 1), (2, 4)], 4, 0.18, gestrichelt=True, dicke=3),
                      mit(V([(0, 1), (2, 1), (2, 4)], 3, 0.25), bewegung=[[3.0, {}], [3.9, {'punkte': [[6, 1], [8, 1], [8, 4]]}]])],
                 ein=2.4),
            # «Es entsteht ein Rechteck» (Ton 4.5–5.2): Rechteck (2 | 1)–(8 | 4) umranden
            graf(W3, [V([(2, 1), (8, 1), (8, 4), (2, 4)], 3, 0.0, dicke=6)], ein=4.8, raster=False)),
         sz('Trapez',
            'Beim Trapez sind zwei Seiten parallel, a und c. Die Mittellinie m verbindet die Mitten der Schenkel. Sie ist das '
            'Mittel aus a und c. Fläche gleich Mittellinie mal Höhe.',
            f(r'\fb{m} = \tfrac{1}{2}(a + c)', 300, 56, ein=6.0),
            f(r'A = \fb{m} \cdot h', 410, 56, ein=8.0),
            # Brücke zu sim3, Aufgabe 1 («Verschieb die obere Seite mit d»): bei «Sie ist das Mittel aus a und c»
            # (Ton 5.9–7.5) gleitet c um 2 nach rechts und zurück; die Mittellinie verschiebt sich um die Hälfte,
            # ihre Länge ½(8 + 4) = 6 bleibt.
            graf(W3, [mit(V([(0, 1), (8, 1), (6, 4), (2, 4)]), bewegung=SCHUB_C(lambda s_: {'punkte': [[0, 1], [8, 1], [6 + s_, 4], [2 + s_, 4]]})),
                      T(4, 0.25, 'a', 5), mit(T(4, 4.45, 'c', 5), bewegung=SCHUB_C(lambda s_: {'bei': [4 + s_, 4.45]})),
                      mit(S((1, 2.5), (7, 2.5), 2), ein=3.7, bewegung=SCHUB_C(lambda s_: {'von': [1 + s_ / 2, 2.5], 'bis': [7 + s_ / 2, 2.5]})),
                      mit(T(4, 2.75, 'm', 2), ein=3.7, bewegung=SCHUB_C(lambda s_: {'bei': [4 + s_ / 2, 2.75]}))],
                 ein=0.3),
            # «mal Höhe» (Ton 9.2): Höhe h = 3 von D(2 | 4) auf a
            graf(W3, [S((2, 4), (2, 1), 2, True, 3), RW(2, 1, 0, 90), T(1.65, 1.6, 'h', 2, 'end')], ein=8.8, raster=False)),
         sz('Raute und Drachen',
            'Raute und Drachen füllen genau die Hälfte des Rechtecks um ihre Diagonalen e und f. Ihre Fläche ist ein Halb mal e mal f.',
            f(r'A = \tfrac{1}{2} \cdot e \cdot f', 300, 60, ein=5.5),
            graf(W3, [V([(1, 4), (7, 4), (7, 7), (1, 7)], 5, 0.0, gestrichelt=True, dicke=2.5),
                      V([(1, 5.5), (4, 7), (7, 5.5), (4, 4)]), S((1, 5.5), (7, 5.5), 2, dicke=3), S((4, 4), (4, 7), 2, dicke=3),
                      T(5.6, 5.85, 'e', 2), T(4.3, 6.2, 'f', 2, 'start')], ein=0.3),
            # «und Drachen» (Ton 1.2): Drachen (1 | 2), (4 | 3), (7 | 2), (4 | −0.5) im Rechteck 6 × 3.5, e = 6, f = 3.5
            graf(W3, [V([(1, -0.5), (7, -0.5), (7, 3), (1, 3)], 5, 0.0, gestrichelt=True, dicke=2.5),
                      V([(1, 2), (4, 3), (7, 2), (4, -0.5)]), S((1, 2), (7, 2), 2, dicke=3), S((4, 3), (4, -0.5), 2, dicke=3),
                      T(5.6, 2.3, 'e', 2), T(4.3, 0.4, 'f', 2, 'start'),
                      T(7.3, 5.4, 'Raute', 5, 'start', 22, False), T(7.3, 1.1, 'Drachen', 5, 'start', 22, False)],
                 ein=1.2, raster=False),
            # «die Hälfte» (Ton 2.6): die vier Eckdreiecke je Rechteck sind die Gegenstücke der vier Innendreiecke
            graf(W3, [V([(1, 4), (4, 4), (1, 5.5)], 3, 0.22, dicke=0), V([(4, 4), (7, 4), (7, 5.5)], 3, 0.22, dicke=0),
                      V([(7, 5.5), (7, 7), (4, 7)], 3, 0.22, dicke=0), V([(4, 7), (1, 7), (1, 5.5)], 3, 0.22, dicke=0),
                      V([(1, -0.5), (4, -0.5), (1, 2)], 3, 0.22, dicke=0), V([(4, -0.5), (7, -0.5), (7, 2)], 3, 0.22, dicke=0),
                      V([(7, 2), (7, 3), (4, 3)], 3, 0.22, dicke=0), V([(4, 3), (1, 3), (1, 2)], 3, 0.22, dicke=0)],
                 ein=2.6, raster=False)),
         sz('Fehlende Länge',
            'Oft fehlt die Höhe. Ein gleichschenkliges Trapez mit a gleich zehn, c gleich vier und Schenkeln von fünf Zentimetern: '
            'Links und rechts steht je drei Zentimeter über. Mit Pythagoras ist die Höhe die Wurzel aus fünf im Quadrat minus drei '
            'im Quadrat, also vier. Die Fläche ist ein Halb mal vierzehn mal vier, gleich achtundzwanzig Quadratzentimeter.',
            f(r'h = \sqrt{5^2 - 3^2} = 4\,\text{cm}', 300, 50, ein=9.6),
            f(r'A = \tfrac{1}{2}(10 + 4) \cdot 4 = \fc{28\,\text{cm}^2}', 410, 48, ein=15.0),
            graf(W3b, [V([(0, 1), (10, 1), (7, 5), (3, 5)]), T(5, 0.3, 'a = 10', 5, kursiv=False, g=26),
                       T(5, 5.45, 'c = 4', 5, kursiv=False, g=26)], ein=0.3),
            graf(W3b, [V([(0, 1), (3, 1), (3, 5)], 3, 0.25), S((3, 5), (3, 1), 2, True), RW(3, 1, 180, 90),
                       T(1.5, 0.3, '3', 3, g=26), T(1.1, 3.3, '5', 3, 'end', g=26), T(3.35, 3, 'h', 2, 'start')], ein=7.1),
            # «und rechts» (Ton 7.6): das gespiegelte Dreieck (7 | 1), (10 | 1), (7 | 5)
            graf(W3b, [V([(10, 1), (7, 1), (7, 5)], 3, 0.25), RW(7, 1, 0, 90), T(8.5, 0.3, '3', 3, g=26),
                       T(8.9, 3.3, '5', 3, 'start', g=26)], ein=7.6, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Jede Vierecksfläche kommt vom Rechteck. Parallelogramm a mal h, Trapez Mittellinie mal h, Raute und '
            'Drachen ein Halb mal e mal f.',
            titel('Zum Mitnehmen', 250, 76),
            n('Parallelogramm @a \\cdot h@|Trapez @m \\cdot h@, @m = \\tfrac12(a + c)@|Raute, Drachen @\\tfrac12\\, e f@',
              400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
WK3 = ach(-1, -3, 10, (1, 2, 3, 4, 5, 6, 7, 8), (-2, -1, 1, 2, 3, 4, 5, 6))
clip('kontrolle-vierecke', 'Figuren sehen: Kontrollfragen zu Vierecken',
     'Fünf Fragen zur Vierecks-Familie, zu Trapez, Raute, Rechteckdiagonale und zur Mittellinie.',
     ['Viereck', 'Trapez', 'Mittellinie', 'Kontrollfragen'], 'g5-2b', [
         sz('Frage 1',
            'Ja. Ein Quadrat hat vier rechte Winkel, wie jedes Rechteck. Es hat zusätzlich vier gleich lange Seiten.',
            n('Quadrat @\\subset@ Rechteck', 300, 'blau', 52, ein=1.0)),
         sz('Frage 2',
            'Mittellinie: neun plus fünf, durch zwei, gleich sieben. Mal vier ergibt achtundzwanzig Quadratzentimeter.',
            f(r'A = \tfrac{1}{2}(9 + 5) \cdot 4 = \fc{28\,\text{cm}^2}', 300, 50, ein=1.0)),
         sz('Frage 3',
            'Ein Halb mal sechs mal acht gleich vierundzwanzig Quadratzentimeter.',
            f(r'A = \tfrac{1}{2} \cdot 6 \cdot 8 = \fc{24\,\text{cm}^2}', 300, 52, ein=1.0)),
         sz('Frage 4',
            'Die Diagonale ist die Hypotenuse: Wurzel aus sechs im Quadrat plus acht im Quadrat, gleich zehn Zentimeter.',
            f(r'd = \sqrt{6^2 + 8^2} = \fc{10\,\text{cm}}', 300, 52, ein=1.0),
            graf(W3, [V([(0.5, 1), (8.5, 1), (8.5, 7), (0.5, 7)]), S((0.5, 1), (8.5, 7), 3, dicke=5),
                      T(4.5, 0.3, '8', 5, g=26), T(8.9, 4, '6', 5, 'start', g=26)], ein=1.0)),
         sz('Frage 5',
            'Die Mittellinie beginnt in der Mitte des Schenkels BC, bei sieben, zwei.',
            f(r'\text{Mitte von } BC: \ (\fc{7} \mid \fc{2})', 300, 52, ein=1.0),
            graf(WK3, [V([(0, 0), (8, 0), (6, 4), (2, 4)]), T(0, -0.75, 'A'), T(8.2, -0.75, 'B'), T(6.3, 4.4, 'C'), T(1.7, 4.4, 'D')],
                 ein=0.05),
            graf(WK3, [S((1, 2), (7, 2), 2)], punkte=[pt(7, 2, 3, '(7 | 2)', [7.35, 2.6])], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Trapez gleich Mittellinie mal Höhe. Fehlende Längen mit Pythagoras.',
            titel('Zum Mitnehmen', 250, 76),
            n('@A = m \\cdot h@|fehlende Längen: Pythagoras', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Ist jedes Quadrat ein Rechteck?', ['Ja', 'Nein', 'Nur manchmal'], 0,
              {0: 'Ja.', 1: 'Was braucht ein Rechteck? Hat das Quadrat das?', 2: 'Was braucht ein Rechteck? Hat jedes Quadrat das?'},
              sprich='Ist jedes Quadrat ein Rechteck?',
              rueck_sprich={1: 'Was braucht ein Rechteck? Hat das Quadrat das?', 2: 'Was braucht ein Rechteck? Hat jedes Quadrat das?'}),
         wahl('Frage 2', 'Trapez mit a = 9 cm, c = 5 cm, h = 4 cm: Wie gross ist A?', ['28 cm²', '56 cm²', '180 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist (a + c) · h. Es fehlt das ein Halb.', 2: 'Das ist a · c · h. Wo steht a + c?'},
              sprich='Trapez mit a gleich neun, c gleich fünf, h gleich vier Zentimeter: Wie gross ist A?',
              rueck_sprich={1: 'Das ist a plus c mal h. Es fehlt das ein Halb.', 2: 'Das ist a mal c mal h. Wo steht a plus c?'}),
         wahl('Frage 3', 'Raute mit e = 6 cm und f = 8 cm: Wie gross ist A?', ['24 cm²', '48 cm²', '14 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist das ganze Rechteck um die Diagonalen. Welchen Teil davon füllt die Raute?', 2: 'Das ist e + f. Die Fläche ist ein Produkt.'},
              sprich='Raute mit e gleich sechs und f gleich acht Zentimeter: Wie gross ist A?',
              rueck_sprich={1: 'Das ist das ganze Rechteck um die Diagonalen. Welchen Teil davon füllt die Raute?',
                            2: 'Das ist e plus f. Die Fläche ist ein Produkt.'}),
         wahl('Frage 4', 'Rechteck 6 cm × 8 cm: Wie lang ist die Diagonale?', ['10 cm', '14 cm', '48 cm'], 0,
              {0: 'Ja.', 1: 'Das ist der Weg aussen herum. Die Diagonale ist die Hypotenuse.', 2: 'Das ist die Fläche, keine Länge.'},
              sprich='Rechteck sechs mal acht Zentimeter: Wie lang ist die Diagonale?',
              rueck_sprich={1: 'Das ist der Weg aussen herum. Die Diagonale ist die Hypotenuse.', 2: 'Das ist die Fläche, keine Länge.'}),
         klick('Frage 5', 'Tipp den Endpunkt der Mittellinie auf dem Schenkel BC an.', [7, 2], 'Getroffen: (7 | 2).',
               [{'bei': [6, 4], 'text': 'Das ist C. Die Mittellinie beginnt in der Mitte des Schenkels.',
                 'sprich': 'Das ist C. Die Mittellinie beginnt in der Mitte des Schenkels.'},
                {'bei': [8, 0], 'text': 'Das ist B. Gesucht ist die Mitte zwischen B und C.',
                 'sprich': 'Das ist B. Gesucht ist die Mitte zwischen B und C.'},
                {'bei': [4, 2], 'text': 'Das ist die Mitte der Mittellinie. Gesucht ist ihr Ende auf BC.',
                 'sprich': 'Das ist die Mitte der Mittellinie. Gesucht ist ihr Ende auf B C.'}],
               FALSCH, sprich='Tipp den Endpunkt der Mittellinie auf dem Schenkel B C an.', falsch_sprich=FALSCH),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
W4 = geo(-0.5, -1, 11)
W4r = geo(-7.5, -7.5, 15)                      # Kreis r = 6 um (0 | 0)
PHI4 = lambda felder: [[3.6, {}], [4.1, felder(90)], [4.8, {}], [5.4, felder(180)], [6.3, {}], [7.0, felder(60)]]
clip('kreis', 'Figuren sehen: Kreis und Kreisteile',
     'Sehne, Sekante, Tangente und Passante; U = 2πr, A = πr²; Bogen und Sektor über den Anteil φ/360°; Segment = Sektor − Dreieck. '
     'Vorgelöst mit r = 6 cm und φ = 60°.',
     ['Kreis', 'Tangente', 'Sektor', 'Segment', 'Bogenlänge'], 'g5-2c', [
         sz('Linien am Kreis',
            'Eine Passante trifft den Kreis nicht. Eine Tangente berührt ihn in genau einem Punkt und steht dort senkrecht auf '
            'dem Radius. Eine Sekante schneidet ihn zweimal. Das Stück der Sekante im Kreis heisst Sehne.',
            n('Passante: kein Punkt|Tangente: ein Punkt, @\\perp@ Radius|Sekante: zwei Punkte|Sehne: Strecke im Kreis',
              300, 'blau', 44, ein=0.6),
            graf(W4, [KR(5, 4.5, 3), T(5, 4.15, 'M', 5, g=24)], punkte=[pt(5, 4.5, 5)], ein=0.3),
            graf(W4, [S((-0.5, 9.4), (10.5, 9.4), 5, True, 2.5), T(10.3, 9.65, 'Passante', 5, 'end', 22, False)], ein=0.6),
            graf(W4, [S((-0.5, 7.5), (10.5, 7.5), 2), S((5, 4.5), (5, 7.5), 5, dicke=2.5), RW(5, 7.5, 0, 270, 2),
                      T(10.3, 7.75, 'Tangente', 2, 'end', 22, False)], ein=2.4),
            graf(W4, [S((-0.5, 5.5), (10.5, 5.5), 1, dicke=2.5), T(10.3, 5.75, 'Sekante', 1, 'end', 22, False)], ein=7.1),
            graf(W4, [S((2.172, 5.5), (7.828, 5.5), 3, dicke=6), T(5, 5.85, 'Sehne', 3, 'middle', 22, False)], ein=9.0)),
         sz('Umfang und Fläche',
            'Der Umfang ist zwei Pi mal r, die Fläche Pi mal r im Quadrat.',
            f(r'U = 2\pi r = \pi d', 300, 60, ein=0.4),
            f(r'A = \pi r^2', 420, 60, ein=2.6),
            graf(W4r, [KR(0, 0, 6, 1, 0.08), S((0, 0), (6, 0), 2), T(3, 0.4, 'r', 2)], punkte=[pt(0, 0, 5)], ein=0.3)),
         sz('Bogen und Sektor',
            'Ein Sektor ist ein Tortenstück mit dem Mittelpunktswinkel Phi. Er ist der Anteil Phi durch dreihundertsechzig Grad '
            'vom ganzen Kreis. Das gilt für die Bogenlänge und für die Fläche.',
            f(r'b = \dfrac{\varphi}{360^\circ} \cdot 2\pi r', 290, 50, ein=3.6),
            f(r'A_S = \dfrac{\varphi}{360^\circ} \cdot \pi r^2', 430, 50, ein=7.7),
            # Brücke zu sim4, Aufgabe 1 («Zieh an φ. Welchen Anteil …?»): bei «Er ist der Anteil Phi durch 360 Grad
            # vom ganzen Kreis» (Ton 3.6–6.9) öffnet sich der Sektor auf 90° (¼) und 180° (½) und schliesst sich
            # wieder auf 60°. Der Winkelbogen φ = 60° geht solange aus; «¼», «½» sind Zwischenstände.
            graf(W4r, [KR(0, 0, 6, 5, 0, dicke=2.5), mit(SEK(0, 0, 6, 0, 60), bewegung=PHI4(lambda w: {'bis': w})),
                       mit(BOG(0, 0, 6, 0, 60), bewegung=PHI4(lambda w: {'bis': w})),
                       mit(WI(0, 0, 0, 60, 2, 60), aus=3.6), mit(WI(0, 0, 0, 60, 2, 60), ein=7.0),
                       T(1.6, 0.6, 'φ', 2, 'start', 28),
                       mit(T(0, -3.2, '90° : 360° = ¼', 5, 'middle', 30, False), ein=4.1, aus=4.7),
                       mit(T(0, -3.2, '180° : 360° = ½', 5, 'middle', 30, False), ein=5.4, aus=6.2)],
                 ein=0.3)),
         sz('Vorgelöst',
            'Zum Beispiel r gleich sechs Zentimeter und Phi gleich sechzig Grad. Sechzig Grad sind ein Sechstel des Kreises. '
            'Bogen: ein Sechstel von zwölf Pi, also zwei Pi, rund sechs Komma zwei acht Zentimeter. Sektor: ein Sechstel von '
            'sechsunddreissig Pi, also sechs Pi, rund achtzehn Komma acht fünf Quadratzentimeter.',
            f(r'\tfrac{60^\circ}{360^\circ} = \tfrac{1}{6}', 280, 50, ein=4.3),
            f(r'b = \tfrac{1}{6} \cdot 12\pi = 2\pi \approx \fc{6.28\,\text{cm}}', 390, 44, ein=6.9),
            f(r'A_S = \tfrac{1}{6} \cdot 36\pi = 6\pi \approx \fc{18.85\,\text{cm}^2}', 500, 44, ein=12.9),
            graf(W4r, [KR(0, 0, 6, 5, 0, dicke=2.5), SEK(0, 0, 6, 0, 60), BOG(0, 0, 6, 0, 60),
                       T(3.4, -0.6, 'r = 6', 5, 'middle', 26, False)], ein=0.3),
            # «ein Sechstel des Kreises» (Ton 4.2–5.4): die übrigen Radien im 60°-Abstand teilen den Kreis in Sechstel
            graf(W4r, [S((0, 0), (6 * math.cos(math.radians(w)), 6 * math.sin(math.radians(w))), 5, True, 2.5)
                       for w in (120, 180, 240, 300)], ein=4.2, raster=False)),
         sz('Segment',
            'Ein Segment liegt zwischen Sehne und Bogen. Man rechnet Sektor minus Dreieck. Bei sechzig Grad ist das Dreieck '
            'gleichseitig, alle Seiten sind sechs Zentimeter lang. Seine Höhe ist nach Pythagoras die Wurzel aus sechs im Quadrat '
            'minus drei im Quadrat, rund fünf Komma zwei null. Das Dreieck hat also ein Halb mal sechs mal fünf Komma zwei null, '
            'rund fünfzehn Komma fünf neun Quadratzentimeter. Das Segment hat rund drei Komma zwei sechs.',
            f(r'A_{\text{Seg}} = A_S - A_\Delta', 250, 46, ein=2.7),
            f(r'h = \sqrt{6^2 - 3^2} = \sqrt{27} \approx 5.20', 350, 44, ein=9.5),
            f(r'A_\Delta = \tfrac{1}{2} \cdot 6 \cdot \sqrt{27} \approx 15.59\,\text{cm}^2', 450, 42, ein=14.7),
            f(r'A_{\text{Seg}} \approx 18.85 - 15.59 = \fc{3.26\,\text{cm}^2}', 560, 42, ein=22.7),
            graf(W4r, [KR(0, 0, 6, 5, 0, dicke=2.5), SEK(0, 0, 6, 0, 60, 3, 0.35),
                       V([(0, 0), (6, 0), (3, 5.196)], 1, 0.12, dicke=3)], ein=0.3),
            # «Ein Segment liegt zwischen Sehne und Bogen» (Ton 0.7): das Segment allein, kräftig gefüllt und umrandet —
            # Vieleck aus der Sehne (3 | 5.196)–(6 | 0) und 31 Punkten auf dem Bogen 0°..60°
            graf(W4r, [V([(round(6 * math.cos(math.radians(2 * k)), 3), round(6 * math.sin(math.radians(2 * k)), 3))
                          for k in range(31)], 3, 0.45, dicke=4)], ein=0.8, raster=False),
            # «alle Seiten sind sechs Zentimeter» (Ton 7.5–8.4)
            graf(W4r, [T(1.1, 2.9, '6', 5, 'end', 26, False)], ein=7.8, raster=False),
            # «Seine Höhe» (Ton 9.5)
            graf(W4r, [S((3, 5.196), (3, 0), 2, True, 3), RW(3, 0, 180, 90), T(3.35, 2.4, 'h', 2, 'start'),
                       T(1.5, -0.6, '3', 5, 'middle', 26, False)], ein=9.5)),
         sz('Kreisring',
            'Ein Kreisring liegt zwischen zwei Kreisen um denselben Mittelpunkt. Seine Fläche ist die grosse Kreisfläche minus '
            'die kleine. Bei R gleich fünf und r gleich drei Zentimetern: Pi mal fünfundzwanzig minus neun, also sechzehn Pi, '
            'rund fünfzig Komma zwei sieben Quadratzentimeter.',
            f(r'A = \pi (R^2 - r^2)', 300, 56, ein=3.9),
            f(r'A = \pi (25 - 9) = 16\pi \approx \fc{50.27\,\text{cm}^2}', 420, 44, ein=9.7),
            graf(W4r, [KR(0, 0, 4, 3, 0, dicke=99, deckkraft=0.3), KR(0, 0, 5, 1, 0, dicke=3), KR(0, 0, 3, 1, 0, dicke=3),
                       S((0, 0), (5, 0), 2, dicke=3), S((0, 0), (0, 3), 2, dicke=3),
                       T(2.6, 0.4, 'R', 2), T(-0.45, 1.5, 'r', 2, 'end')], punkte=[pt(0, 0, 5)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Die Tangente steht senkrecht auf dem Radius. Bogen und Sektor sind der Anteil Phi durch '
            'dreihundertsechzig Grad. Segment gleich Sektor minus Dreieck.',
            titel('Zum Mitnehmen', 250, 76),
            n('Tangente @\\perp@ Radius|Anteil @\\varphi / 360^\\circ@|Segment = Sektor − Dreieck (@\\varphi \\lt 180^\\circ@)', 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
WK4 = ach(-5, -5, 10, (-4, -3, -2, -1, 1, 2, 3, 4), (-4, -3, -2, -1, 1, 2, 3, 4))
clip('kontrolle-kreis', 'Figuren sehen: Kontrollfragen zu Kreis und Kreisteilen',
     'Fünf Fragen zur Tangente, zum Umfang, zum Sektor als Anteil, zum Segment und zum Berührpunkt einer Tangente.',
     ['Kreis', 'Tangente', 'Sektor', 'Segment', 'Kontrollfragen'], 'g5-2c', [
         sz('Frage 1',
            'Eine Tangente berührt den Kreis in genau einem Punkt.',
            n('Tangente: genau ein Punkt', 300, 'blau', 52, ein=1.0),
            graf(W4, [KR(5, 4.5, 3), S((-0.5, 7.5), (10.5, 7.5), 2)], punkte=[pt(5, 7.5, 3)], ein=1.0)),
         sz('Frage 2',
            'Zwei Pi mal fünf ist zehn Pi, rund einunddreissig Komma vier zwei Zentimeter.',
            f(r'U = 2\pi \cdot 5 = 10\pi \approx \fc{31.42\,\text{cm}}', 300, 50, ein=1.0)),
         sz('Frage 3',
            'Neunzig durch dreihundertsechzig ist ein Viertel.',
            f(r'\tfrac{90^\circ}{360^\circ} = \fc{\tfrac{1}{4}}', 300, 56, ein=1.0),
            graf(W4r, [KR(0, 0, 6, 5, 0, dicke=2.5), SEK(0, 0, 6, 0, 90)], ein=1.0)),
         sz('Frage 4',
            'Vom Sektor zieht man das Dreieck ab. Übrig bleibt das Segment zwischen Sehne und Bogen.',
            f(r'A_{\text{Seg}} = A_S - A_\Delta', 300, 56, ein=1.0),
            graf(W4r, [KR(0, 0, 6, 5, 0, dicke=2.5), SEK(0, 0, 6, 0, 60, 3, 0.35),
                       V([(0, 0), (6, 0), (3, 5.196)], 1, 0.12, dicke=3)], ein=1.0)),
         sz('Frage 5',
            'Die Tangente steht senkrecht auf dem Radius. Der Berührpunkt liegt bei null, drei.',
            f(r'\text{Berührpunkt } (0 \mid \fc{3})', 300, 56, ein=1.0),
            graf(WK4, [KR(0, 0, 3), S((-5, 3), (5, 3), 2, True, 3)], ein=0.05),
            graf(WK4, [S((0, 0), (0, 3), 5, dicke=2.5), RW(0, 3, 0, 270)], punkte=[pt(0, 3, 3, '(0 | 3)', [0.4, 3.6])], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Tangente senkrecht auf dem Radius. Kreisteile über den Anteil Phi durch dreihundertsechzig Grad.',
            titel('Zum Mitnehmen', 250, 76),
            n('Tangente @\\perp@ Radius|Anteil @\\varphi / 360^\\circ@', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Wie viele Punkte hat eine Tangente mit dem Kreis gemeinsam?', ['genau einen', 'zwei', 'keinen'], 0,
              {0: 'Ja.', 1: 'Zwei Punkte hat eine Sekante.', 2: 'Keinen Punkt hat eine Passante.'},
              sprich='Wie viele Punkte hat eine Tangente mit dem Kreis gemeinsam?',
              rueck_sprich={1: 'Zwei Punkte hat eine Sekante.', 2: 'Keinen Punkt hat eine Passante.'}),
         wahl('Frage 2', 'r = 5 cm: Wie gross ist der Umfang?', ['≈ 31.42 cm', '≈ 78.54 cm', '≈ 15.71 cm'], 0,
              {0: 'Ja.', 1: 'Das ist die Fläche π r².', 2: 'Das ist π · r. Der Umfang ist 2 π r.'},
              sprich='r gleich fünf Zentimeter: Wie gross ist der Umfang?',
              rueck_sprich={1: 'Das ist die Fläche, Pi mal r im Quadrat.', 2: 'Das ist Pi mal r. Der Umfang ist zwei Pi r.'}),
         wahl('Frage 3', 'φ = 90°: Welcher Anteil der Kreisfläche ist der Sektor?', ['ein Viertel', 'ein Drittel', 'die Hälfte'], 0,
              {0: 'Ja.', 1: 'Rechne 90° : 360°.', 2: 'Die Hälfte wären 180°.'},
              sprich='Phi gleich neunzig Grad: Welcher Anteil der Kreisfläche ist der Sektor?',
              rueck_sprich={1: 'Rechne neunzig durch dreihundertsechzig.', 2: 'Die Hälfte wären hundertachtzig Grad.'}),
         wahl('Frage 4', 'Wie bekommt man die Fläche eines Segments?',
              ['Sektor minus Dreieck', 'Sektor plus Dreieck', 'Kreis minus Sektor'], 0,
              {0: 'Ja.', 1: 'Das Segment ist kleiner als der Sektor.', 2: 'Das ist der Rest des Kreises ohne den Sektor.'},
              sprich='Wie bekommt man die Fläche eines Segments?',
              rueck_sprich={1: 'Das Segment ist kleiner als der Sektor.', 2: 'Das ist der Rest des Kreises ohne den Sektor.'}),
         klick('Frage 5', 'Gestrichelt eine Tangente: Tipp ihren Berührpunkt mit dem Kreis an.', [0, 3], 'Getroffen: (0 | 3).',
               [{'bei': [3, 3], 'text': 'Dort ist die Tangente, aber nicht der Kreis.', 'sprich': 'Dort ist die Tangente, aber nicht der Kreis.'},
                {'bei': [0, 0], 'text': 'Das ist der Mittelpunkt. Gesucht ist der Punkt auf dem Kreis.',
                 'sprich': 'Das ist der Mittelpunkt. Gesucht ist der Punkt auf dem Kreis.'}],
               FALSCH, sprich='Gestrichelt eine Tangente: Tipp ihren Berührpunkt mit dem Kreis an.', falsch_sprich=FALSCH),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
W5 = geo(-0.5, -0.5, 10.5)
W5s = geo(-1, -2.8, 14)
W5n = geo(-5, -4.5, 11)                        # Streckung mit k = −1 um Z(0 | 0)
W5t = geo(-1, -1.5, 9.5)                       # Strahlensatz-Figur mit S(0 | 0)
clip('aehnlichkeit', 'Figuren sehen: Streckung und Ähnlichkeit',
     'Zentrische Streckung mit Zentrum Z und Faktor k: Winkel bleiben, Längen mal k, Flächen mal k². '
     'Strahlensatz am Schatten: Stab 1.5 m, Schatten 2 m; Baum mit 12 m Schatten ist 9 m hoch.',
     ['zentrische Streckung', 'Ähnlichkeit', 'Strahlensatz', 'Streckfaktor'], 'g5-2d', [
         sz('Zentrische Streckung',
            'Bei einer zentrischen Streckung geht jeder Punkt auf dem Strahl vom Zentrum Z weiter. Mit k gleich zwei wird sein '
            'Abstand zu Z doppelt so gross. So entsteht ein Bilddreieck.',
            f(r"\overline{ZP'} = |\fb{k}| \cdot \overline{ZP}", 300, 56, ein=0.4),
            f(r'\fb{k = 2}', 410, 56, ein=5.2),
            graf(W5, [V([(3, 2), (5, 2), (4, 4)]), T(1, 0.45, 'Z', 5)], punkte=[pt(1, 1, 5)], ein=0.3),
            graf(W5, [S((1, 1), (5, 3), 5, True, 2), S((1, 1), (9, 3), 5, True, 2), S((1, 1), (7, 7), 5, True, 2)], ein=2.4),
            # Brücke zu sim5 («Zieh an k»): «Mit k gleich zwei wird sein Abstand zu Z doppelt so gross» (Ton 5.1–7.9):
            # das Bild liegt bei k = 1 auf dem Original und wächst entlang der Strahlen bis k = 2 (Z + k·(P − Z)).
            graf(W5, [V([(3, 2), (5, 2), (4, 4)], 2, 0.1, bewegung=[[5.5, {}], [7.8, {'punkte': [[5, 3], [9, 3], [7, 7]]}]])],
                 ein=5.2)),
         sz('Was bleibt, was wächst',
            'Die Winkel bleiben gleich, die Figuren sind ähnlich. Jede Länge wird mit k multipliziert. Die Fläche aber mit k '
            'im Quadrat: Bei k gleich zwei passen vier Originaldreiecke ins Bild.',
            n('Winkel gleich|Längen @\\cdot\\, |k|@', 300, 'blau', 46, ein=0.6),
            f(r"A' = \fb{k}^2 \cdot A = 4A", 440, 54, ein=5.6),
            graf(W5, [V([(3, 2), (5, 2), (4, 4)]), V([(5, 3), (9, 3), (7, 7)], 2, 0.1)], ein=0.3),
            graf(W5, [V([(7, 3), (8, 5), (6, 5)], 2, 0.0, dicke=2.5)], ein=7.8),
            # «Die Winkel bleiben gleich» (Ton 0.9): gleiche Bögen in Original und Bild (63.4°, 63.4°, 53.1°)
            graf(W5, [WI(3, 2, 0, 63.4, 2, 22), WI(5, 2, 116.6, 180, 3, 22), WI(4, 4, 243.4, 296.6, 1, 22),
                      WI(5, 3, 0, 63.4, 2, 36), WI(9, 3, 116.6, 180, 3, 36), WI(7, 7, 243.4, 296.6, 1, 36)],
                 ein=0.9, raster=False)),
         sz('Negativer Faktor',
            'Ist k negativ, liegt das Bild auf der anderen Seite von Z. Bei k gleich minus eins ist es gleich gross, aber um Z '
            'gedreht. Längen werden mit dem Betrag von k multipliziert.',
            f(r'\fb{k = -1}', 300, 58, ein=0.4),
            n('Bild auf der anderen Seite von @Z@|Längen @\\cdot\\, |k|@', 420, 'blau', 44, ein=7.5),
            graf(W5n, [V([(1.5, 1), (3.5, 1), (2.5, 3)]), T(0.3, -0.5, 'Z', 5, 'start')], punkte=[pt(0, 0, 5)], ein=0.3),
            graf(W5n, [S((-2.1, -1.4), (5.25, 3.5), 5, True, 2), S((-4.2, -1.2), (4.9, 1.4), 5, True, 2),
                       S((-3.33, -4.0), (3.33, 4.0), 5, True, 2)], ein=1.0),
            # «liegt das Bild auf der anderen Seite von Z. Bei k gleich minus eins» (Ton 1.65–4.8): k läuft von 1
            # über 0 (das Bild schrumpft in Z) bis −1 (wie sim5 «auch unter null»); die Punkte sind linear in k.
            graf(W5n, [V([(1.5, 1), (3.5, 1), (2.5, 3)], 2, 0.1,
                         bewegung=[[2.0, {}], [4.6, {'punkte': [[-1.5, -1], [-3.5, -1], [-2.5, -3]]}]])], ein=1.7)),
         sz('Strahlensätze',
            'Zwei Strahlen gehen von S aus und werden von zwei Parallelen geschnitten. Dann stehen die Strecken im gleichen '
            'Verhältnis: S A zu S A Strich wie A B zu A Strich B Strich. Mit S A gleich vier, S A Strich gleich sechs und A B '
            'gleich drei ist A Strich B Strich gleich vier Komma fünf.',
            f(r"\overline{SA} : \overline{SA'} = \overline{AB} : \overline{A'B'}", 290, 46, ein=4.5),
            f(r"4 : 6 = 3 : \overline{A'B'}", 400, 50, ein=11.7),
            f(r"\overline{A'B'} = \fc{4.5}", 510, 50, ein=14.0),
            graf(W5t, [S((0, 0), (8, 0), 5, dicke=2.5), S((0, 0), (8, 6), 5, dicke=2.5),
                       S((4, 0), (4, 3), 1, dicke=5), S((6, 0), (6, 4.5), 2, dicke=5),
                       T(-0.35, -0.55, 'S', 5), T(4, -0.6, 'A', 1), T(6, -0.6, "A'", 2), T(3.6, 3.35, 'B', 1), T(5.6, 4.85, "B'", 2),
                       T(2, -0.6, '4', 5, kursiv=False, g=24), T(4.35, 1.5, '3', 1, 'start', 24, False)],
                 punkte=[pt(0, 0, 5)], ein=0.3),
            # «S A Strich gleich sechs» (Ton 11.7–12.6): Masslinie unter SA'
            graf(W5t, [S((0, -1.05), (2.65, -1.05), 2, dicke=2), S((3.35, -1.05), (6, -1.05), 2, dicke=2),
                       S((0, -1.25), (0, -0.85), 2, dicke=2), S((6, -1.25), (6, -0.85), 2, dicke=2),
                       T(3, -1.2, '6', 2, 'middle', 24, False)], ein=11.7, raster=False),
            # Ergebnis A'B' = 4.5 mit der Formelzeile (14.0)
            graf(W5t, [T(6.35, 2.25, '4.5', 2, 'start', 24, False)], ein=14.0, raster=False)),
         sz('Strahlensatz',
            'Ein Stab von eins Komma fünf Metern wirft zwei Meter Schatten. Ein Baum daneben wirft zwölf Meter Schatten. '
            'Die Sonnenstrahlen sind parallel, die Dreiecke ähnlich. Also h durch zwölf gleich eins Komma fünf durch zwei: '
            'Der Baum ist neun Meter hoch.',
            f(r'\dfrac{h}{12} = \dfrac{1.5}{2}', 300, 54, ein=9.0),
            f(r'h = 12 \cdot 0.75 = \fc{9\,\text{m}}', 460, 52, ein=11.9),
            graf(W5s, [S((-1, 0), (13, 0), 5, dicke=3), S((2, 0), (2, 1.5), 1, dicke=6), S((12, 0), (12, 9), 3, dicke=6),
                       S((0, 0), (12.8, 9.6), 2, True, 2.5), T(1, -0.75, '2 m', 5, g=24, kursiv=False),
                       S((0, -1.5), (12, -1.5), 5, dicke=2), S((0, -1.8), (0, -1.2), 5, dicke=2), S((12, -1.8), (12, -1.2), 5, dicke=2),
                       T(6, -2.25, '12 m', 5, g=24, kursiv=False), T(2.3, 0.9, '1.5 m', 1, 'start', 24, False),
                       T(12.3, 4.5, 'h', 3, 'start')], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Bei Ähnlichkeit bleiben die Winkel. Längen wachsen mit k, Flächen mit k im Quadrat. Die '
            'Strahlensätze sind Streckung in Gleichungsform.',
            titel('Zum Mitnehmen', 250, 76),
            n('Längen @\\cdot\\, |k|@, Flächen @\\cdot\\, k^2@|@SA : SA\' = AB : A\'B\'@', 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
WK5 = ach(-5, -3, 10, (-4, -2, 2, 4), (-2, -1, 1, 2, 3, 4, 5, 6))
clip('kontrolle-aehnlichkeit', 'Figuren sehen: Kontrollfragen zu Streckung und Ähnlichkeit',
     'Fünf Fragen zum Flächenfaktor, zu den Winkeln, zum Streckfaktor, zum Schatten und zum Bildpunkt einer Streckung.',
     ['zentrische Streckung', 'Ähnlichkeit', 'Strahlensatz', 'Kontrollfragen'], 'g5-2d', [
         sz('Frage 1',
            'Die Fläche wächst mit k im Quadrat. Drei im Quadrat ist neun.',
            f(r'k^2 = 3^2 = \fc{9}', 300, 60, ein=1.0)),
         sz('Frage 2',
            'Die Winkel bleiben gleich. Längen und Flächen ändern sich.',
            n('Winkel bleiben gleich', 300, 'blau', 52, ein=1.0)),
         sz('Frage 3',
            'S A Strich ist zwei plus vier, also sechs. Sechs durch zwei ist drei.',
            f(r"k = \dfrac{SA'}{SA} = \dfrac{2 + 4}{2} = \fc{3}", 300, 52, ein=1.0)),
         sz('Frage 4',
            'h durch fünfzehn gleich zwei durch drei. Also ist der Turm zehn Meter hoch.',
            f(r'\dfrac{h}{15} = \dfrac{2}{3} \;\Rightarrow\; h = \fc{10\,\text{m}}', 300, 50, ein=1.0)),
         sz('Frage 5',
            'Der Bildpunkt liegt auf dem Strahl von Z durch P, doppelt so weit von Z entfernt: bei vier, zwei.',
            f(r"P'(\fc{4} \mid \fc{2})", 300, 60, ein=1.0),
            graf(WK5, [T(0.35, -0.6, 'Z', 5, 'start'), T(2.25, 1.35, 'P', 1, 'start')], punkte=[pt(0, 0, 5), pt(2, 1, 1)], ein=0.05),
            graf(WK5, [S((0, 0), (5, 2.5), 2, True, 2.5)], punkte=[pt(4, 2, 3, 'P′(4 | 2)', [4.1, 2.65], 'end')], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Längen mal k, Flächen mal k im Quadrat, Winkel gleich.',
            titel('Zum Mitnehmen', 250, 76),
            n('Längen @\\cdot\\, |k|@|Flächen @\\cdot\\, k^2@|Winkel gleich', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Streckfaktor k = 3: Die Fläche des Bildes ist …', ['9-mal so gross', '3-mal so gross', '6-mal so gross'], 0,
              {0: 'Ja.', 1: 'So wachsen die Längen. Eine Fläche hat zwei Richtungen.', 2: 'Das ist 2 · 3. Gefragt ist k mal k.'},
              sprich='Streckfaktor k gleich drei: Die Fläche des Bildes ist …',
              rueck_sprich={1: 'So wachsen die Längen. Eine Fläche hat zwei Richtungen.', 2: 'Das ist zwei mal drei. Gefragt ist k mal k.'}),
         wahl('Frage 2', 'Was bleibt bei einer zentrischen Streckung gleich?', ['die Winkel', 'die Seitenlängen', 'die Fläche'], 0,
              {0: 'Ja.', 1: 'Die Seiten werden mit k multipliziert.', 2: 'Die Fläche wird mit k² multipliziert.'},
              sprich='Was bleibt bei einer zentrischen Streckung gleich?',
              rueck_sprich={1: 'Die Seiten werden mit k multipliziert.', 2: 'Die Fläche wird mit k im Quadrat multipliziert.'}),
         wahl('Frage 3', 'SA = 2 cm, AA′ = 4 cm: Wie gross ist k = SA′ : SA?', ['3', '2', '1.5'], 0,
              {0: 'Ja.', 1: 'Das ist AA′ : SA. SA′ geht von S bis A′.', 2: 'Wie lang ist SA′ ganz?'},
              sprich='S A gleich zwei, A A Strich gleich vier Zentimeter: Wie gross ist k gleich S A Strich durch S A?',
              rueck_sprich={1: 'Das ist A A Strich durch S A. S A Strich geht von S bis A Strich.', 2: 'Wie lang ist S A Strich ganz?'}),
         wahl('Frage 4', 'Ein 2 m hoher Stab wirft 3 m Schatten, ein Turm 15 m. Wie hoch ist der Turm?', ['10 m', '22.5 m', '14 m'], 0,
              {0: 'Ja.', 1: 'Dann wäre der Turm höher als sein Schatten lang — beim Stab ist es umgekehrt.', 2: 'Das ist 15 − 3 + 2. Verhältnisse, nicht Differenzen.'},
              sprich='Ein zwei Meter hoher Stab wirft drei Meter Schatten, ein Turm fünfzehn Meter. Wie hoch ist der Turm?',
              rueck_sprich={1: 'Dann wäre der Turm höher als sein Schatten lang. Beim Stab ist es umgekehrt.',
                            2: 'Das ist fünfzehn minus drei plus zwei. Rechne mit Verhältnissen, nicht mit Differenzen.'}),
         klick('Frage 5', 'Streckung von Z aus mit k = 2: Tipp den Bildpunkt P′ an.', [4, 2], 'Getroffen: P′(4 | 2).',
               [{'bei': [3, 1.5], 'text': 'Das ist k = 1.5. Der Abstand zu Z soll doppelt so gross werden.',
                 'sprich': 'Das ist k gleich eins Komma fünf. Der Abstand zu Z soll doppelt so gross werden.'},
                {'bei': [-4, -2], 'text': 'Das wäre k = −2, auf der anderen Seite von Z.',
                 'sprich': 'Das wäre k gleich minus zwei, auf der anderen Seite von Z.'},
                {'bei': [2, 1], 'text': 'Das ist P selbst.', 'sprich': 'Das ist P selbst.'}],
               FALSCH, sprich='Streckung von Z aus mit k gleich zwei: Tipp den Bildpunkt P Strich an.', falsch_sprich=FALSCH),
     ], art='Kontrollclip')
