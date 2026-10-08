"""Erzeugt die acht Drehbücher des Leitprogramms Dreiecke (08.10.2026).

  python3 scripts/lp/dreiecke/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich); nur für
Szenen mit neuem Text muss danach build-clip-ton.py laufen. Nach der Vertonung Bewegungen und `ein`
hier anpassen (Zeiten aus .claude/tools/sprechzeiten.py) und das Skript erneut laufen lassen.

Aufbau wie in den Leitprogrammen Planimetrie und Trigonometrische Berechnungen: Rechnung und Notizen
links (x 150), die Figur rechts (x 1010, y 175, 760 × 760). Figuren zeichnet `graf` mit "figuren" und
"achsen": false (HOWTO-clips.md, «Figuren im Graf»). Fenster in x und y gleich geteilt, darum sind alle
Figuren massstäblich (1 Einheit = 1 cm, wo Längen genannt sind).

Fragebild (HOWTO-leitprogramme §15): Die Kontrollclips zeigen beim Erscheinen einer Frage nur das
Gegebene; Hervorhebung und Rechnung erscheinen erst ab 1.0 s (nach der Antwort).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = die Figur                                              \\fa{…}
  2 orange = Element (Höhe, Halbierende, Mittelsenkrechte), Hilfslinie; in Kapitel 1 der Winkel α
  3 grün   = gesuchte Grösse, Ergebnis, Schnittpunkt; in Kapitel 1 der Winkel β
  4 rot    = Fehler, Gegenbeispiel
  5 Tinte  = neutral (Bezugslinien, Beschriftung); in Kapitel 1 der Winkel γ
Kapitel 1 färbt die drei Winkel, damit man α und β im Beweis der Winkelsumme an der Parallelen
wiederfindet (Farbführung eines Terms, HOWTO-clips «Farbführung»); darum steht dort kein Ergebnis grün.
Alle Zahlen und Lagen werden unten aus den Ecken gerechnet; zahlen.py prüft die Ergebnisse.
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-2a-lp-'


import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import r3, richtung, abst, winkel, lot, mitte, schnitt, punkte, wfuss, dritte_ecke  # noqa: E402


# ---------------------------------------------------------------- Fenster und Figuren
def geo(x0, y0, span):
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], achsen=False)


def ach(x0, y0, span, xt, yt_):
    """Mit Achsen (für Klickfragen, deren Stelle ablesbar sein soll), gleich geteilt."""
    tt = lambda ws: [[w, ('%g' % w).replace('-', '−')] for w in ws]
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], xteilung=tt(xt), yteilung=tt(yt_))


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


def WI(p, a, b, farbe=2, r=44, **kw):
    """Winkel bei p von der Richtung zu a bis zur Richtung zu b (der kleinere, gegen den Uhrzeigersinn)."""
    w0, w1 = richtung(p, a), richtung(p, b)
    if (w1 - w0) % 360 > 180:
        w0, w1 = w1, w0
    if w1 < w0:
        w1 += 360
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def WR(p, w0, w1, farbe=2, r=44, **kw):
    """Winkel bei p von Richtung w0 bis w1 (Grad, gegen den Uhrzeigersinn)."""
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def wlabel(p, a, b, text, farbe=2, abst_=1.0, g=30, kursiv=True, **kw):
    """Beschriftung eines Winkels auf seiner Winkelhalbierenden, abst_ Einheiten vom Scheitel."""
    w0, w1 = richtung(p, a), richtung(p, b)
    d = (w1 - w0) % 360
    if d > 180:
        w0, d = w1, 360 - d
    wm = math.radians(w0 + d / 2)
    return T(p[0] + abst_ * math.cos(wm), p[1] + abst_ * math.sin(wm) - 0.17, text, farbe, g=g, kursiv=kursiv, **kw)


def KR(m, r, farbe=5, fu=0.0, **kw):
    return dict(art='kreis', m=r3(m), r=round(r, 3), farbe=farbe, fuellung=fu, **kw)


def PK(p, farbe=3, r=0.09, **kw):
    """Punkt als gefüllter kleiner Kreis (kann sich mit `bewegung` bewegen, anders als `punkte`)."""
    return KR(p, r, farbe, 1, **kw)


BREITE = {'M': 0.86, 'h': 0.56, 's': 0.44, 'w': 0.72}


def IDX(x, y, base, idx, farbe=3, g=26, span=10, **kw):
    """Buchstabe mit tiefgestelltem Index (h_c, M_U …) — das SVG kennt kein LaTeX. span: Fensterbreite (Einheiten)."""
    upx = span / 760
    return [T(x, y, base, farbe, 'start', g, **kw),
            T(round(x + BREITE.get(base, 0.6) * g * upx, 3), round(y - 0.3 * g * upx, 3), idx, farbe, 'start', int(g * 0.7), **kw)]


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def weich(q):
    return q * q * (3 - 2 * q)


def dicht(t0, t1, felder, schritt=0.05):
    """Stützpunkte alle 0.05 s für Bewegungen, die nicht linear in den Feldern sind; felder(u), u = 0 … 1 weich."""
    n_ = max(1, int(round((t1 - t0) / schritt)))
    return [[round(t0 + (t1 - t0) * i / n_, 3), felder(weich(i / n_))] for i in range(n_ + 1)]


def gerade(p, d, W, rand=0.15):
    """Strecke der Geraden p + t d, am Fenster W abgeschnitten (rand Einheiten innen)."""
    (x0, x1), (y0, y1) = W['xbereich'], W['ybereich']
    x0, x1, y0, y1 = x0 + rand, x1 - rand, y0 + rand, y1 - rand
    ts = []
    for k, lo, hi in ((0, x0, x1), (1, y0, y1)):
        if abs(d[k]) > 1e-12:
            ts += [(lo - p[k]) / d[k], (hi - p[k]) / d[k]]
    inn = [t for t in ts if x0 - 1e-9 <= p[0] + t * d[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] + t * d[1] <= y1 + 1e-9]
    t0, t1 = min(inn), max(inn)
    return (p[0] + t0 * d[0], p[1] + t0 * d[1]), (p[0] + t1 * d[0], p[1] + t1 * d[1])


def mittelsenkrechte(P, Q, W):
    m = mitte(P, Q)
    return gerade(m, (-(Q[1] - P[1]), Q[0] - P[0]), W)


def graf(W, figuren=(), punkte_=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte_), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def pt(p, farbe=3, text=None, bei=None, anker='start'):
    d = dict(x=round(p[0], 3), y=round(p[1], 3), farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = r3(bei)
    return d


def ecken(*e, g=34):
    """Ecken-Beschriftung: (Punkt, Name, dx, dy) in Fenstereinheiten."""
    return [T(p[0] + dx, p[1] + dy, nm, 5, g=g, kursiv=False) for p, nm, dx, dy in e]


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


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.5, bei=0.3, eingabe=None):
    # Ohne "eingabe" (wie in der Planimetrie): Die Figuren stehen meist ohne Achsen; wo Achsen stehen
    # (Fusspunkt der Höhe), ist die Stelle das Gesuchte, nicht ihre Koordinaten.
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    if eingabe:     # nur wo Achsen die Stelle ablesbar machen (HOWTO-leitprogramme §15)
        d['eingabe'] = eingabe
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'
FALSCH_LINIE = 'Nicht ganz. Die grüne Linie zeigt die Seite.'


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(alt):
        vorher = json.load(open(alt))['szenen']
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in vorher}
        # Szene mit neuem Text: die alte dauer behalten, bis build-clip-ton.py --szenen sie neu misst (sonst passt die
        # bisherige Tonspur nicht mehr zum Drehbuch und die Teilvertonung bricht ab)
        nur_name = {q['name']: q.get('dauer') for q in vorher}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher'])) or nur_name.get(q['name'])
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Planimetrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-2a'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Dreiecke sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms dreiecke; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# ════════════════════════════════════════════════ Kapitel 1 · Einführung «Winkel im Dreieck»
# Grunddreieck A(1 | 1.5), B(8.5 | 1.5), C(3.5 | 6.5): α = 63.43°, β = 45°, γ = 71.57° (spitzwinklig, ungleichseitig).
W1 = geo(-0.5, -1, 10)
A1, B1, C1 = (1, 1.5), (8.5, 1.5), (3.5, 6.5)
ECK1 = ecken((A1, 'A', -0.45, -0.65), (B1, 'B', 0.45, -0.65), (C1, 'C', 0, 0.45))


def winkelfig(A, B, C, mitC=True, lab=True):
    """Die drei Innenwinkel: α orange, β grün, γ Tinte (Kapitel 1)."""
    fg = [WI(A, B, C, 2), WI(B, C, A, 3), WI(C, A, B, 5, 36)]
    if lab:
        fg += [wlabel(A, B, C, 'α', 2, 0.95), wlabel(B, C, A, 'β', 3, 0.95), wlabel(C, A, B, 'γ', 5, 0.85)]
    return fg


def zieh_C(t_teile, felder, y=6.5):
    """C gleitet auf der Parallelen y: Liste von (t0, t1, x0, x1); felder(C) liefert die Felder je Lage."""
    bew = []
    for t0, t1, x0, x1 in t_teile:
        teil = dicht(t0, t1, lambda u: felder((x0 + (x1 - x0) * u, y)))
        bew += teil[1:] if bew else teil
    return bew


ZUG1 = ((1.2, 2.2, 3.5, 7.0), (2.2, 3.4, 7.0, 1.5), (3.4, 4.2, 1.5, 3.5))
WINKEL_MIT_C = [
    mit(V([A1, B1, C1]), bewegung=zieh_C(ZUG1, lambda C: {'punkte': [r3(A1), r3(B1), r3(C)]})),
    mit(WI(A1, B1, C1, 2), bewegung=zieh_C(ZUG1, lambda C: {'bis': round(richtung(A1, C), 2)})),
    mit(WI(B1, C1, A1, 3), bewegung=zieh_C(ZUG1, lambda C: {'von': round(richtung(B1, C), 2)})),
    mit(WI(C1, A1, B1, 5, 36), bewegung=zieh_C(ZUG1, lambda C: {'bei': r3(C), 'von': round(richtung(C, A1), 2),
                                                                 'bis': round(richtung(C, B1), 2)})),
    ECK1[0], ECK1[1], mit(ECK1[2], bewegung=zieh_C(ZUG1, lambda C: {'bei': [round(C[0], 3), 6.95]}))]

# Vorgelöst: α = 50°, β = 60° auf AB = 7.5 → C, γ = 70°; Aussenwinkel bei B: 120° = α + γ.
C1v = dritte_ecke(A1, B1, 50, 60)
# Nach Winkeln: Grundseite (1 | 1.5)–(6 | 1.5), C auf y = 5.5: (3 | 5.5) spitz (β = 53.13°), (6 | 5.5) rechts bei B, (8 | 5.5) stumpf (β = 116.57°).
A1w, B1w = (1, 1.5), (6, 1.5)
CW = [(3, 5.5), (6, 5.5), (8, 5.5)]
print('Kap. 1: Grunddreieck', [round(winkel(*x), 2) for x in ((A1, B1, C1), (B1, C1, A1), (C1, A1, B1))],
      '| vorgelöst C', r3(C1v), round(winkel(C1v, A1, B1), 2),
      '| nach Winkeln β', [round(winkel(B1w, A1w, c), 2) for c in CW])

clip('winkel', 1, 'Dreiecke sehen: Winkel im Dreieck',
     'Ecken, Seiten und Winkel normgerecht benennen; die Innenwinkelsumme 180° mit Wechselwinkeln begründen; der Aussenwinkel '
     'und der Aussenwinkelsatz; Dreiecke nach Winkeln und nach Seiten einteilen.',
     ['Dreieck', 'Innenwinkelsumme', 'Aussenwinkel', 'Wechselwinkel', 'gleichschenklig', 'stumpfwinklig'], [
         sz('Beschriften',
            'Ein Dreieck beschriftet man gegen den Uhrzeigersinn mit A, B und C. Die Seite a liegt der Ecke A gegenüber, '
            'b liegt B gegenüber und c liegt C gegenüber. Der Winkel bei A heisst Alpha, bei B Beta und bei C Gamma.',
            f(r'A,\ B,\ C \ \text{gegen den Uhrzeigersinn}', 300, 46, ein=0.4),
            f(r'\text{Seite } a \text{ gegenüber } A', 400, 50, ein=4.8),
            f(r'\text{Winkel } \fb{\alpha} \text{ bei } A', 500, 50, ein=11.1),
            graf(W1, [V([A1, B1, C1])] + ECK1, ein=0.3),
            graf(W1, [T(6.35, 4.25, 'a', 5)], ein=4.8, raster=False),
            graf(W1, [T(1.85, 4.2, 'b', 5)], ein=6.9, raster=False),
            graf(W1, [T(4.75, 0.85, 'c', 5)], ein=8.4, raster=False),
            graf(W1, [WI(A1, B1, C1, 2), wlabel(A1, B1, C1, 'α', 2, 0.95)], ein=11.1, raster=False),
            graf(W1, [WI(B1, C1, A1, 3), wlabel(B1, C1, A1, 'β', 3, 0.95)], ein=11.9, raster=False),
            graf(W1, [WI(C1, A1, B1, 5, 36), wlabel(C1, A1, B1, 'γ', 5, 0.85)], ein=13.2, raster=False)),
         sz('Winkelsumme',
            'Zieh die Ecke C hin und her: Die Winkel ändern sich, ihre Summe nicht. Warum? Zieh durch C die Parallele zu A B. '
            'Links und rechts von Gamma entstehen Wechselwinkel, genau so gross wie Alpha und Beta. Zusammen mit Gamma liegen '
            'sie auf einer Geraden: hundertachtzig Grad.',
            f(r'\fb{\alpha} + \fc{\beta} + \gamma = 180^\circ', 300, 60, ein=13.3),
            n('Parallele durch @C@: Wechselwinkel', 420, 'blau', 44, ein=5.6),
            graf(W1, WINKEL_MIT_C, ein=0.3),
            graf(W1, [S((-0.5, 6.5), (9.5, 6.5), 5, True, 2.5)], ein=5.6, raster=False),
            # Wechselwinkel an der Parallelen: links α (180° bis Richtung CA), rechts β (Richtung CB bis 360°)
            graf(W1, [WR(C1, 180, richtung(C1, A1), 2, 56), WR(C1, richtung(C1, B1), 360, 3, 56),
                      wlabel(C1, (C1[0] - 1, C1[1]), A1, 'α', 2, 1.15), wlabel(C1, B1, (C1[0] + 1, C1[1]), 'β', 3, 1.15)],
                 ein=8.8, raster=False)),
         sz('Aussenwinkel',
            'Verlängere die Seite c über B hinaus. Zwischen der Verlängerung und der Seite a liegt der Aussenwinkel Beta Strich. '
            'Er ergänzt Beta zu hundertachtzig Grad. Das tun auch Alpha und Gamma zusammen. Also ist Beta Strich gleich '
            'Alpha plus Gamma.',
            f(r"\fc{\beta'} = 180^\circ - \fc{\beta}", 300, 54, ein=6.4),
            f(r"\fb{\alpha} + \gamma = 180^\circ - \fc{\beta}", 410, 54, ein=9.6),
            f(r"\Rightarrow\ \fc{\beta'} = \fb{\alpha} + \gamma", 520, 54, ein=11.0),
            graf(W1, [V([A1, B1, C1])] + ECK1 + winkelfig(A1, B1, C1), ein=0.3),
            graf(W1, [S(B1, (9.6, 1.5), 5, True, 2.5)], ein=0.8, raster=False),
            graf(W1, [WR(B1, 0, richtung(B1, C1), 3, 30), T(9.15, 2.25, "β'", 3, g=30)], ein=4.8, raster=False)),
         sz('Vorgelöst',
            'Zum Beispiel Alpha gleich fünfzig Grad und Beta gleich sechzig Grad. Dann ist Gamma hundertachtzig minus fünfzig '
            'minus sechzig, also siebzig Grad. Der Aussenwinkel bei B ist hundertachtzig minus sechzig, also hundertzwanzig '
            'Grad. Und das ist genau Alpha plus Gamma.',
            f(r'\fb{\alpha} = 50^\circ, \quad \fc{\beta} = 60^\circ', 300, 54, ein=0.4),
            f(r'\gamma = 180^\circ - 50^\circ - 60^\circ = 70^\circ', 420, 48, ein=7.2),
            f(r"\fc{\beta'} = 180^\circ - 60^\circ = 120^\circ = 50^\circ + 70^\circ", 540, 44, ein=12.4),
            graf(W1, [V([A1, B1, C1v]), WI(A1, B1, C1v, 2), wlabel(A1, B1, C1v, '50°', 2, 1.2, kursiv=False),
                      WI(B1, C1v, A1, 3), wlabel(B1, C1v, A1, '60°', 3, 1.2, kursiv=False)]
                 + ecken((A1, 'A', -0.45, -0.65), (B1, 'B', 0.2, -0.7), (C1v, 'C', 0, 0.45)), ein=0.4),
            graf(W1, [WI(C1v, A1, B1, 5, 36), wlabel(C1v, A1, B1, '70°', 5, 1.15, kursiv=False)], ein=7.2, raster=False),
            graf(W1, [S(B1, (9.6, 1.5), 5, True, 2.5), WR(B1, 0, richtung(B1, C1v), 3, 30),
                      mit(T(9.25, 2.3, '120°', 3, g=26, kursiv=False), ein=12.4)], ein=9.2, raster=False)),
         sz('Nach Winkeln',
            'Nach den Winkeln unterscheidet man drei Arten. Spitzwinklig: Alle drei Winkel sind spitz. Rechtwinklig: Ein Winkel '
            'ist ein rechter. Stumpfwinklig: Ein Winkel ist stumpf. Mehr als einen rechten oder stumpfen Winkel hat kein '
            'Dreieck: Die Summe wäre schon zu gross.',
            n('spitzwinklig: alle Winkel spitz|rechtwinklig: ein Winkel @90^\\circ@|stumpfwinklig: ein Winkel über @90^\\circ@',
              300, 'blau', 44, ein=2.6),
            # C gleitet auf y = 5.5: spitz (3 | 5.5) → rechter Winkel bei B (6 | 5.5) → stumpf bei B (8 | 5.5),
            # der Winkel bei B wächst mit (53.13° → 90° → 116.57°).
            graf(W1, [mit(V([A1w, B1w, CW[0]]), bewegung=[[5.2, {}], [6.0, {'punkte': [r3(A1w), r3(B1w), r3(CW[1])]}],
                                                          [7.6, {}], [8.5, {'punkte': [r3(A1w), r3(B1w), r3(CW[2])]}]]),
                      mit(WR(B1w, richtung(B1w, CW[0]), 180, 3, 40),
                          bewegung=[[5.2, {}], [6.0, {'von': 90}], [7.6, {}], [8.5, {'von': round(richtung(B1w, CW[2]), 2)}]]),
                      T(0.55, 0.85, 'A', kursiv=False), T(6.4, 0.85, 'B', kursiv=False),
                      mit(T(3, 5.95, 'C', kursiv=False), bewegung=[[5.2, {}], [6.0, {'bei': [6, 5.95]}], [7.6, {}], [8.5, {'bei': [8, 5.95]}]]),
                      mit(T(3.5, -0.4, 'spitzwinklig', 5, g=26, kursiv=False), aus=5.2),
                      mit(T(3.5, -0.4, 'rechtwinklig', 5, g=26, kursiv=False), ein=6.0, aus=7.6),
                      mit(T(3.5, -0.4, 'stumpfwinklig', 5, g=26, kursiv=False), ein=8.5)], ein=0.3)),
         sz('Nach Seiten',
            'Nach den Seiten: Im gleichschenkligen Dreieck sind zwei Seiten gleich lang, die Schenkel. Die beiden Basiswinkel '
            'sind dann gleich gross. Im gleichseitigen Dreieck sind alle drei Seiten gleich lang und alle Winkel sechzig Grad.',
            n('gleichschenklig: Basiswinkel gleich|gleichseitig: alle Winkel @60^\\circ@', 300, 'blau', 44, ein=1.0),
            # gleichschenklig (0.5 | 1)–(4.5 | 1)–(2.5 | 5), Basiswinkel 63.43°; gleichseitig Seite 3.5 ab (5.5 | 1).
            graf(W1, [V([(0.5, 1), (4.5, 1), (2.5, 5)]), T(2.5, 0.25, 'gleichschenklig', 5, g=24, kursiv=False)], ein=1.0),
            graf(W1, [S((1.303, 3.098), (1.697, 2.902), 5, dicke=3), S((3.303, 2.902), (3.697, 3.098), 5, dicke=3)], ein=3.3, raster=False),
            graf(W1, [WI((0.5, 1), (4.5, 1), (2.5, 5), 5, 34), WI((4.5, 1), (2.5, 5), (0.5, 1), 5, 34)], ein=5.0, raster=False),
            graf(W1, [V([(5.5, 1), (9, 1), (7.25, 1 + 3.5 * math.sqrt(3) / 2)]), T(7.25, 0.25, 'gleichseitig', 5, g=24, kursiv=False)],
                 ein=7.4, raster=False),
            graf(W1, [WI((5.5, 1), (9, 1), (7.25, 4.031), 5, 28), WI((9, 1), (7.25, 4.031), (5.5, 1), 5, 28),
                      WI((7.25, 4.031), (5.5, 1), (9, 1), 5, 28), T(7.25, 2.05, '60°', 5, g=26, kursiv=False)], ein=10.8, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Die Innenwinkel ergeben zusammen hundertachtzig Grad. Ein Aussenwinkel ist so gross wie die beiden '
            'Innenwinkel, die nicht an ihm liegen, zusammen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\fb{\alpha} + \fc{\beta} + \gamma = 180^\circ', 400, 56, ein=1.2),
            f(r"\fc{\beta'} = \fb{\alpha} + \gamma", 520, 56, ein=4.0),
            graf(W1, [V([A1, B1, C1])] + ECK1 + winkelfig(A1, B1, C1), ein=0.3),
            graf(W1, [S(B1, (9.6, 1.5), 5, True, 2.5), WR(B1, 0, richtung(B1, C1), 3, 30), T(9.15, 2.3, "β'", 3, g=30)],
                 ein=4.0, raster=False)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
# Frage 1: gedrehtes Dreieck A(7.5 | 2), B(4 | 8), C(1 | 3) (gegen den Uhrzeigersinn), gesucht die Seite b = CA.
WK1 = geo(-0.5, -0.5, 10)
A1k, B1k, C1k = (7.5, 2), (4, 8), (1, 3)
# Frage 2: α = 35°, β = 80° auf AB = 7.5 → C; gegeben α und γ = 65°, gesucht β' = 100°.
C2k = dritte_ecke(A1, B1, 35, 80)
print('Kontrolle 1: Frage-2-Dreieck C', r3(C2k), 'γ', round(winkel(C2k, A1, B1), 2))
clip('kontrolle-winkel', 2, 'Dreiecke sehen: Kontrollfragen zu Winkeln im Dreieck',
     'Fünf Fragen: eine Seite normgerecht finden, den Aussenwinkel, die Art eines Dreiecks aus zwei Winkeln, den Winkel an der '
     'Spitze und warum kein Dreieck zwei rechte Winkel hat.',
     ['Dreieck', 'Aussenwinkel', 'Innenwinkelsumme', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Seite b liegt der Ecke B gegenüber. Sie verbindet A und C.',
            f(r'b = \overline{CA}', 300, 60, ein=1.0),
            graf(WK1, [V([A1k, B1k, C1k])] + ecken((A1k, 'A', 0.45, -0.55), (B1k, 'B', 0, 0.45), (C1k, 'C', -0.45, -0.55)), ein=0.05),
            graf(WK1, [S(C1k, A1k, 3, dicke=8), T(4.1, 1.95, 'b', 3)], ein=1.0, raster=False)),
         sz('Frage 2',
            'Zuerst Beta: hundertachtzig minus fünfunddreissig minus fünfundsechzig, gleich achtzig Grad. Der Aussenwinkel ist '
            'hundertachtzig minus achtzig, also hundert Grad. Schneller: Alpha plus Gamma.',
            f(r'\beta = 180^\circ - 35^\circ - 65^\circ = 80^\circ', 300, 46, ein=1.0),
            f(r"\beta' = 35^\circ + 65^\circ = \fc{100^\circ}", 410, 50, ein=8.9),
            graf(W1, [V([A1, B1, C2k]), WI(A1, B1, C2k, 2), wlabel(A1, B1, C2k, '35°', 2, 1.25, kursiv=False),
                      WI(C2k, A1, B1, 5, 36), wlabel(C2k, A1, B1, '65°', 5, 1.2, kursiv=False),
                      S(B1, (9.6, 1.5), 5, True, 2.5), WR(B1, 0, richtung(B1, C2k), 3, 30), mit(T(9.2, 2.3, '?', 3, g=36, kursiv=False), aus=8.9)]
                 + ecken((A1, 'A', -0.45, -0.65), (B1, 'B', 0.15, -0.7), (C2k, 'C', 0, 0.45)), ein=0.05),
            graf(W1, [T(9.2, 2.3, '100°', 3, g=24, kursiv=False)], ein=8.9, raster=False)),
         sz('Frage 3',
            'Der dritte Winkel ist hundertachtzig minus vierzig minus fünfzig, also neunzig Grad. Das Dreieck ist rechtwinklig.',
            f(r'180^\circ - 40^\circ - 50^\circ = 90^\circ', 300, 50, ein=1.0),
            n('rechtwinklig', 420, 'blau', 48, ein=5.2)),
         sz('Frage 4',
            'Die beiden Basiswinkel sind zusammen hundertvierundvierzig Grad. Für die Spitze bleiben sechsunddreissig Grad.',
            f(r'180^\circ - 2 \cdot 72^\circ = \fc{36^\circ}', 300, 54, ein=1.0)),
         sz('Frage 5',
            'Zwei rechte Winkel sind schon hundertachtzig Grad. Für den dritten Winkel bliebe nichts übrig.',
            f(r'90^\circ + 90^\circ = 180^\circ', 300, 56, ein=1.0),
            n('für den dritten Winkel: @0^\\circ@', 420, 'blau', 44, ein=3.0)),
         sz('Merke',
            'Zum Mitnehmen: Winkelsumme hundertachtzig Grad, Aussenwinkel gleich Summe der zwei anderen Innenwinkel.',
            titel('Zum Mitnehmen', 250, 76),
            n("@\\alpha + \\beta + \\gamma = 180^\\circ@|@\\beta' = \\alpha + \\gamma@", 400, 'blau', 46, ein=1.2)),
     ], [
         # Ziel ist die Strecke CA (HOWTO-clips «Dritte Runde»), die Fallen sind die beiden anderen Seiten. Toleranz 0.45:
         # Nachgezählt in zahlen.py — Tipps nahe einer Ecke liegen nahe an zwei Seiten (unvermeidlich).
         klick('Frage 1', 'Tipp die Seite b an.', [r3(C1k), r3(A1k)], 'Getroffen: b liegt der Ecke B gegenüber.',
               [{'bei': [r3(B1k), r3(C1k)], 'text': 'Das ist die Seite a: Sie liegt der Ecke A gegenüber.',
                 'sprich': 'Das ist die Seite a. Sie liegt der Ecke A gegenüber.'},
                {'bei': [r3(A1k), r3(B1k)], 'text': 'Das ist die Seite c: Sie liegt der Ecke C gegenüber.',
                 'sprich': 'Das ist die Seite c. Sie liegt der Ecke C gegenüber.'}],
               FALSCH_LINIE, sprich='Tipp die Seite b an.', falsch_sprich=FALSCH_LINIE, tol=0.45),
         wahl('Frage 2', 'α = 35°, γ = 65°: Wie gross ist der Aussenwinkel bei B?', ['100°', '80°', '145°'], 0,
              {0: 'Ja.', 1: 'Das ist der Innenwinkel β. Der Aussenwinkel ergänzt ihn zu 180°.',
               2: 'Das ist der Aussenwinkel bei A. Gesucht ist der bei B.'},
              sprich='Alpha gleich fünfunddreissig Grad, Gamma gleich fünfundsechzig Grad: Wie gross ist der Aussenwinkel bei B?',
              rueck_sprich={1: 'Das ist der Innenwinkel Beta. Der Aussenwinkel ergänzt ihn zu hundertachtzig Grad.',
                            2: 'Das ist der Aussenwinkel bei A. Gesucht ist der bei B.'}),
         wahl('Frage 3', 'Ein Dreieck hat die Winkel 40° und 50°. Was für ein Dreieck ist es?',
              ['rechtwinklig', 'spitzwinklig', 'stumpfwinklig'], 0,
              {0: 'Ja.', 1: 'Rechne zuerst den dritten Winkel aus.', 2: 'Rechne zuerst den dritten Winkel aus. Ist er grösser als 90°?'},
              sprich='Ein Dreieck hat die Winkel vierzig und fünfzig Grad. Was für ein Dreieck ist es?',
              rueck_sprich={1: 'Rechne zuerst den dritten Winkel aus.',
                            2: 'Rechne zuerst den dritten Winkel aus. Ist er grösser als neunzig Grad?'}),
         wahl('Frage 4', 'Gleichschenklig, ein Basiswinkel misst 72°. Wie gross ist der Winkel an der Spitze?',
              ['36°', '108°', '54°'], 0,
              {0: 'Ja.', 1: 'Das ist 180° − 72°. Es gibt zwei Basiswinkel.',
               2: 'So rechnet man den Basiswinkel aus der Spitze. Hier ist ein Basiswinkel gegeben.'},
              sprich='Gleichschenklig, ein Basiswinkel misst zweiundsiebzig Grad. Wie gross ist der Winkel an der Spitze?',
              rueck_sprich={1: 'Das ist hundertachtzig minus zweiundsiebzig. Es gibt zwei Basiswinkel.',
                            2: 'So rechnet man den Basiswinkel aus der Spitze. Hier ist ein Basiswinkel gegeben.'}),
         wahl('Frage 5', 'Warum hat kein Dreieck zwei rechte Winkel?',
              ['Für den dritten Winkel bliebe 0°.', 'Weil sonst zwei Seiten gleich lang wären.', 'Doch, das gibt es.'], 0,
              {0: 'Ja.', 1: 'Rechne mit der Winkelsumme: Wie viel bliebe für den dritten Winkel?',
               2: 'Rechne mit der Winkelsumme: Wie viel bliebe für den dritten Winkel?'},
              sprich='Warum hat kein Dreieck zwei rechte Winkel?',
              rueck_sprich={1: 'Rechne mit der Winkelsumme. Wie viel bliebe für den dritten Winkel?',
                            2: 'Rechne mit der Winkelsumme. Wie viel bliebe für den dritten Winkel?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung «Höhen, Halbierende, Mittelsenkrechte»
# Grunddreieck A(1 | 1), B(9 | 1), C(3 | 6.5): α = 70.02°, β = 42.51°, γ = 67.47° (spitzwinklig).
# Höhenfuss (3 | 1), Mitte von c M_c(5 | 1), Fuss von w_γ (4.346 | 1), H(3 | 3.182), S(4.333 | 2.833),
# M_I(3.856 | 3.001) mit r = 2.001, M_U(5 | 2.659) mit r = 4.33 — alles in punkte() gerechnet.
W2 = geo(-0.5, -2, 11)
A2, B2, C2 = (1, 1), (9, 1), (3, 6.5)
P2 = punkte(A2, B2, C2)
FH2, MC2, WF2 = lot(C2, A2, B2), mitte(A2, B2), wfuss(C2, A2, B2)
ECK2 = ecken((A2, 'A', -0.45, -0.6), (B2, 'B', 0.45, -0.6), (C2, 'C', 0, 0.45))
TRI2 = [V([A2, B2, C2])] + ECK2
# Punkt P auf der Mittelsenkrechten von c (x = 5) für «gleich weit»: P(5 | 2) im Dreieck, PA = PB = 4.123
P2m = (5, 2)
# Punkt Q auf w_γ: Q = C + 0.55 (Fuss − C); Lote auf b und a sind gleich lang
Q2 = (C2[0] + 0.55 * (WF2[0] - C2[0]), C2[1] + 0.55 * (WF2[1] - C2[1]))
Q2b, Q2a = lot(Q2, C2, A2), lot(Q2, C2, B2)
# Stumpf: Grundseite (1 | 1)–(6 | 1), C gleitet von (3 | 5) nach (7.5 | 3.5): β wird 120.96°, H(7.5 | −2.9), M_U(3.5 | 4.2).
W2s = geo(-1.5, -3.5, 11)
A2s, B2s = (1, 1), (6, 1)
C2s0, C2s1 = (3, 5), (7.5, 3.5)
print('Kap. 2: H', r3(P2['H']), 'S', r3(P2['S']), 'M_I', r3(P2['MI']), round(P2['ri'], 3), 'M_U', r3(P2['MU']), round(P2['ru'], 3),
      '| wfuss', r3(WF2), '| PA PB', round(abst(P2m, A2), 3), round(abst(P2m, B2), 3), '| QA QB', round(abst(Q2, Q2b), 3), round(abst(Q2, Q2a), 3))


def hoehen_stumpf(C):
    """Die drei Höhen als Strecken über Ecke, Fusspunkt und H (Prüfung 08.10.2026, D-M4): Liegt H hinter der Ecke
    (Höhe aus der stumpfen Ecke), reicht die Strecke von H über die Ecke bis zum Fusspunkt; liegt H hinter dem
    Fusspunkt (Höhen aus den spitzen Ecken), von der Ecke über den Fusspunkt bis H."""
    A, B = A2s, B2s
    P = punkte(A, B, C)
    out = []
    for e, (u, v) in ((A, (B, C)), (B, (A, C)), (C, (A, B))):
        fu = lot(e, u, v)
        d = (fu[0] - e[0], fu[1] - e[1])
        nn = d[0] * d[0] + d[1] * d[1]
        th = ((P['H'][0] - e[0]) * d[0] + (P['H'][1] - e[1]) * d[1]) / nn        # Lage von H auf der Geraden e + t d
        t0, t1 = min(0.0, 1.0, th), max(0.0, 1.0, th)
        out.append({'von': r3((e[0] + t0 * d[0], e[1] + t0 * d[1])), 'bis': r3((e[0] + t1 * d[0], e[1] + t1 * d[1]))})
    return P, out


def zug2(teile, felder):
    """C gleitet von C2s0 nach C2s1; teile: (t0, t1, u0, u1) — Zeit und Anteil des Wegs."""
    bew = []
    for t0, t1, u0, u1 in teile:
        st = dicht(t0, t1, lambda q: felder((C2s0[0] + (C2s1[0] - C2s0[0]) * (u0 + (u1 - u0) * q),
                                             C2s0[1] + (C2s1[1] - C2s0[1]) * (u0 + (u1 - u0) * q))))
        bew += st[1:] if bew else st
    return bew


# Ton (gemessen nach der Neuvertonung 08.10.2026, wortzeiten.json): «Schieb die Ecke C nach rechts» ab ZS = 0.56,
# «stumpf» bei ZST = 3.28, «Umkreismittelpunkt» 7.32 bis ZU ≈ 8.3 («Schwerpunkt» 8.58). Bis «stumpf» gleitet C bis kurz vor den rechten Winkel bei B (u = 0.6; 90° bei
# u = 2/3), danach weiter bis zum Ende (β = 121°): H und M_U treten hinaus, während der Satz es sagt.
ZS, ZST, ZU = 0.6, 3.3, 8.3
T_STUMPF = ((ZS, ZST, 0.0, 0.6), (ZST, ZU, 0.6, 1.0))
P2e = punkte(A2s, B2s, C2s1)
STUMPF = ([mit(V([A2s, B2s, C2s0]), bewegung=zug2(T_STUMPF, lambda C: {'punkte': [r3(A2s), r3(B2s), r3(C)]})),
           T(0.55, 0.4, 'A', kursiv=False), T(6.4, 0.4, 'B', kursiv=False),
           mit(T(3, 5.45, 'C', kursiv=False), bewegung=zug2(T_STUMPF, lambda C: {'bei': [round(C[0], 3), round(C[1] + 0.45, 3)]}))]
          + [mit(S(*[hoehen_stumpf(C2s0)[1][k][q] for q in ('von', 'bis')], 2, True, 3),
                 bewegung=zug2(T_STUMPF, lambda C, k=k: hoehen_stumpf(C)[1][k])) for k in range(3)]
          + [mit(PK(punkte(A2s, B2s, C2s0)[key], 3), bewegung=zug2(T_STUMPF, lambda C, key=key: {'m': r3(punkte(A2s, B2s, C)[key])}))
             for key in ('H', 'S', 'MI', 'MU')]
          # Namen erst in der Endlage (am Anfang liegen die vier Punkte zu dicht für vier Beschriftungen); Lagen in
          # zahlen.py nachgeprüft: keine Beschriftung auf einem anderen Punkt oder einer Höhe
          + [mit(fg, ein=ZU) for fg in
             [T(P2e['H'][0] + 0.25, P2e['H'][1] - 0.1, 'H', 3, 'start', 26),
              T(P2e['S'][0] - 0.25, P2e['S'][1] - 0.55, 'S', 3, 'end', 26),
              *IDX(P2e['MI'][0] + 0.45, P2e['MI'][1] + 0.3, 'M', 'I', 3, 26, 11),
              *IDX(P2e['MU'][0] + 0.2, P2e['MU'][1] - 0.6, 'M', 'U', 3, 26, 11)]])

clip('elemente', 3, 'Dreiecke sehen: Höhen, Halbierende und Mittelsenkrechte',
     'Höhe, Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte; ihre Schnittpunkte H, S, Inkreis- und '
     'Umkreismittelpunkt; gleich weit von den Seiten oder den Ecken; welche Punkte beim stumpfen Dreieck aussen liegen; '
     'der Schwerpunkt teilt 2 : 1.',
     ['Höhe', 'Seitenhalbierende', 'Winkelhalbierende', 'Mittelsenkrechte', 'Schwerpunkt', 'Umkreis', 'Inkreis'], [
         sz('Die Höhe',
            'Die Höhe ist das Lot von einer Ecke auf die Gerade durch die Gegenseite. Die Höhe h c geht durch C und steht '
            'senkrecht auf c.',
            f(r'\fb{h_c}: \ \text{durch } C, \ \perp c', 300, 50, ein=0.4),
            graf(W2, TRI2, ein=0.3),
            graf(W2, [S(C2, FH2, 2, dicke=5), RW(FH2, 0, 90, 2), *IDX(3.2, 3.4, 'h', 'c', 2, 32, 11)], ein=1.3, raster=False)),
         sz('Seitenhalbierende',
            'Die Seitenhalbierende verbindet eine Ecke mit der Mitte der Gegenseite. Die Seitenhalbierende s c endet in der '
            'Mitte von c.',
            f(r'\fb{s_c}: \ C \to \text{Mitte von } c', 300, 50, ein=0.4),
            graf(W2, TRI2, ein=0.3),
            graf(W2, [S(C2, MC2, 2, dicke=5), PK(MC2, 5), *IDX(5.2, 0.3, 'M', 'c', 5, 30, 11),
                      S((2.9, 0.78), (3.1, 1.22), 5, dicke=3), S((6.9, 0.78), (7.1, 1.22), 5, dicke=3)], ein=1.5, raster=False)),
         sz('Winkelhalbierende',
            'Die Winkelhalbierende teilt einen Winkel in zwei gleiche Hälften. Jeder ihrer Punkte ist von den beiden Schenkeln '
            'gleich weit entfernt.',
            f(r'\fb{w_\gamma}: \ \text{halbiert } \gamma', 300, 50, ein=0.4),
            n('gleich weit von den Schenkeln', 420, 'blau', 42, ein=4.6),
            graf(W2, TRI2, ein=0.3),
            graf(W2, [S(C2, WF2, 2, dicke=5), WI(C2, A2, WF2, 2, 50), WI(C2, WF2, B2, 2, 58)], ein=1.6, raster=False),
            graf(W2, [PK(Q2, 3), S(Q2, Q2b, 3, True, 3), S(Q2, Q2a, 3, True, 3),
                      RW(Q2b, richtung(Q2b, A2), richtung(Q2b, Q2), 3), RW(Q2a, richtung(Q2a, B2), richtung(Q2a, Q2), 3)],
                 ein=4.6, raster=False)),
         sz('Mittelsenkrechte',
            'Die Mittelsenkrechte steht in der Mitte einer Seite senkrecht auf ihr. Jeder ihrer Punkte ist von den beiden '
            'Endpunkten der Seite gleich weit entfernt.',
            f(r'\text{Mittelsenkrechte}: \ \perp c \text{ in der Mitte}', 300, 46, ein=0.4),
            n('gleich weit von @A@ und @B@', 420, 'blau', 42, ein=5.0),
            graf(W2, TRI2, ein=0.3),
            graf(W2, [S(*mittelsenkrechte(A2, B2, W2), 2, True, 4), RW(MC2, 0, 90, 2)], ein=1.2, raster=False),
            graf(W2, [PK(P2m, 3), S(P2m, A2, 3, True, 3), S(P2m, B2, 3, True, 3), T(5.25, 2.2, 'P', 3, 'start', 32)], ein=5.2, raster=False)),
         sz('Schnittpunkte',
            'Je drei gleiche Linien schneiden sich in einem Punkt. Die Höhen im Höhenschnittpunkt H, die Seitenhalbierenden im '
            'Schwerpunkt S, die Winkelhalbierenden im Inkreismittelpunkt und die Mittelsenkrechten im Umkreismittelpunkt.',
            n('Höhen: @H@|Seitenhalbierende: @S@|Winkelhalbierende: @M_I@|Mittelsenkrechte: @M_U@', 300, 'blau', 44, ein=0.6),
            graf(W2, TRI2, ein=0.3),
            # je Familie zu ihrem Wort, dann wieder aus (Ton nach der Vertonung nachgeführt)
            graf(W2, [S(A2, lot(A2, B2, C2), 2, dicke=3), S(B2, lot(B2, A2, C2), 2, dicke=3), S(C2, FH2, 2, dicke=3),
                      PK(P2['H'], 3), T(P2['H'][0] - 0.25, P2['H'][1] + 0.2, 'H', 3, 'end', 32)], ein=3.3, aus=5.0, raster=False),
            graf(W2, [S(A2, mitte(B2, C2), 2, dicke=3), S(B2, mitte(A2, C2), 2, dicke=3), S(C2, MC2, 2, dicke=3),
                      PK(P2['S'], 3), T(P2['S'][0] + 0.25, P2['S'][1] + 0.2, 'S', 3, 'start', 32)], ein=5.0, aus=7.1, raster=False),
            graf(W2, [S(A2, wfuss(A2, B2, C2), 2, dicke=3), S(B2, wfuss(B2, C2, A2), 2, dicke=3), S(C2, WF2, 2, dicke=3),
                      PK(P2['MI'], 3), *IDX(P2['MI'][0] + 0.25, P2['MI'][1] + 0.25, 'M', 'I', 3, 32, 11)], ein=7.1, aus=9.4, raster=False),
            graf(W2, [S(*mittelsenkrechte(A2, B2, W2), 2, True, 3), S(*mittelsenkrechte(B2, C2, W2), 2, True, 3),
                      S(*mittelsenkrechte(C2, A2, W2), 2, True, 3),
                      PK(P2['MU'], 3), *IDX(P2['MU'][0] + 0.25, P2['MU'][1] - 0.5, 'M', 'U', 3, 32, 11)], ein=9.4, raster=False)),
         sz('Umkreis und Inkreis',
            'Der Umkreismittelpunkt ist von allen drei Ecken gleich weit entfernt: Der Umkreis geht durch A, B und C. Der '
            'Inkreismittelpunkt ist von allen drei Seiten gleich weit entfernt: Der Inkreis berührt jede Seite.',
            n('@M_U@: gleich weit von den Ecken|@M_I@: gleich weit von den Seiten', 300, 'blau', 44, ein=0.6),
            graf(W2, TRI2, ein=0.3),
            graf(W2, [KR(P2['MU'], P2['ru'], 2, dicke=3), PK(P2['MU'], 3), *IDX(P2['MU'][0] + 0.25, P2['MU'][1] - 0.5, 'M', 'U', 3, 32, 11),
                      S(P2['MU'], A2, 3, True, 2.5), S(P2['MU'], B2, 3, True, 2.5), S(P2['MU'], C2, 3, True, 2.5)], ein=1.0, raster=False),
            graf(W2, [KR(P2['MI'], P2['ri'], 2, dicke=3), PK(P2['MI'], 3), *IDX(P2['MI'][0] - 0.75, P2['MI'][1] + 0.3, 'M', 'I', 3, 32, 11)],
                 ein=7.0, raster=False)),
         sz('Stumpfes Dreieck',
            'Schieb die Ecke C nach rechts. Sobald der Winkel bei B stumpf wird, wandert der Höhenschnittpunkt aus dem Dreieck '
            'hinaus, ebenso der Umkreismittelpunkt. Schwerpunkt und Inkreismittelpunkt bleiben immer innen.',
            n('stumpf: @H@ und @M_U@ aussen|@S@ und @M_I@ immer innen', 300, 'blau', 44, ein=ZU),
            graf(W2s, STUMPF, ein=0.3)),
         sz('Teilung 2 zu 1',
            'Der Schwerpunkt teilt jede Seitenhalbierende im Verhältnis zwei zu eins, vom Eckpunkt aus. Ist s c neun Zentimeter '
            'lang, liegt S sechs Zentimeter von C und drei Zentimeter von der Seitenmitte entfernt.',
            f(r'\overline{CS} : \overline{SM_c} = 2 : 1', 300, 54, ein=0.4),
            f(r's_c = 9\,\mathrm{cm}: \quad \overline{CS} = \fc{6\,\mathrm{cm}}, \ \overline{SM_c} = \fc{3\,\mathrm{cm}}', 420, 42, ein=7.8),
            graf(W2, TRI2 + [S(C2, MC2, 2, dicke=5), PK(MC2, 5), *IDX(5.2, 0.3, 'M', 'c', 5, 30, 11)], ein=0.3),
            graf(W2, [PK(P2['S'], 3), T(P2['S'][0] + 0.3, P2['S'][1] + 0.1, 'S', 3, 'start', 32),
                      T(4.15, 5.0, '2', 3, 'start', 26, False), T(4.95, 1.9, '1', 3, 'start', 26, False)], ein=1.6, raster=False),
            # s_c ist im Bild 5.85 Einheiten lang, nicht 9: Hinweis, sobald die 9 cm genannt werden (Prüfung 08.10.2026)
            graf(W2, [T(5, -1.3, 'nicht massstäblich', 5, g=24, kursiv=False)], ein=7.8, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Die Höhe geht durch die Ecke, die Mittelsenkrechte durch die Seitenmitte. Beide stehen senkrecht. '
            'Der Umkreismittelpunkt ist gleich weit von den Ecken, der Inkreismittelpunkt gleich weit von den Seiten.',
            titel('Zum Mitnehmen', 250, 76),
            n('Höhe: durch die Ecke, @\\perp@ zur Gegenseite|Mittelsenkrechte: durch die Seitenmitte', 380, 'blau', 42, ein=1.2),
            n('@M_U@: gleich weit von den Ecken|@M_I@: gleich weit von den Seiten', 580, 'orange', 42, ein=6.4),
            graf(W2, TRI2 + [S(C2, FH2, 2, dicke=4), RW(FH2, 0, 90, 2), S(*mittelsenkrechte(A2, B2, W2), 2, True, 3), RW(MC2, 0, 90, 2)],
                 ein=1.2),
            graf(W2, [KR(P2['MU'], P2['ru'], 2, dicke=3), PK(P2['MU'], 3), KR(P2['MI'], P2['ri'], 2, dicke=3), PK(P2['MI'], 3)],
                 ein=6.4, raster=False)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
# Frage 2 (neu 08.10.2026; vorher Fusspunkt ausserhalb — gleichartig wie Kontrollfrage 2 von Kapitel 3): rechtwinkliges
# Dreieck A(1 | 1), B(9 | 2), C(3 | 5), rechter Winkel bei C (CA · CB = 0). Gesucht H = C. Fallen: A, die Mitte der
# Hypotenuse M(5 | 1.5) (dort liegt M_U) und der Fusspunkt der Höhe aus C auf AB, F(3.462 | 1.308).
WK2 = geo(-0.5, -1, 10)
A2k, B2k, C2k2 = (1, 1), (9, 2), (3, 5)
M2k, F2k = mitte(A2k, B2k), lot(C2k2, A2k, B2k)
print('Kontrolle 2: CA·CB', (A2k[0] - C2k2[0]) * (B2k[0] - C2k2[0]) + (A2k[1] - C2k2[1]) * (B2k[1] - C2k2[1]), 'M', r3(M2k), 'F', r3(F2k),
      'H', r3(punkte(A2k, B2k, C2k2)['H']))
ECK2k = ecken((A2k, 'A', -0.45, -0.55), (B2k, 'B', 0.45, -0.5), (C2k2, 'C', -0.1, 0.45))
clip('kontrolle-elemente', 4, 'Dreiecke sehen: Kontrollfragen zu Höhen, Halbierenden und Mittelsenkrechten',
     'Fünf Fragen: eine Linie erkennen, den Höhenschnittpunkt im rechtwinkligen Dreieck, den Punkt gleich weit von den '
     'Seiten, die Teilung 2 : 1 und den halben Winkel.',
     ['Höhe', 'Mittelsenkrechte', 'Schwerpunkt', 'Inkreis', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Linie geht durch die Mitte von c und steht senkrecht darauf, aber nicht durch C. Das ist die Mittelsenkrechte.',
            f(r'\text{Mittelsenkrechte von } c', 300, 52, ein=1.0),
            graf(W2, TRI2 + [S(*mittelsenkrechte(A2, B2, W2), 2, True, 4), RW(MC2, 0, 90, 2),
                             S((2.9, 0.78), (3.1, 1.22), 5, dicke=3), S((6.9, 0.78), (7.1, 1.22), 5, dicke=3)], ein=0.05)),
         sz('Frage 2',
            'Im rechtwinkligen Dreieck sind die beiden Katheten selbst Höhen: Die Höhe aus A ist die Kathete A C, die Höhe '
            'aus B ist die Kathete B C. Sie schneiden sich in C. Also liegt H auf der Ecke mit dem rechten Winkel.',
            # Ton: «die Höhe aus A» 3.76, «die Höhe aus B» 6.12, «Sie schneiden sich in C» 8.46 (wortzeiten.json)
            f(r'H = C', 300, 60, ein=8.5),
            n('Höhe aus @A@: Kathete @AC@|Höhe aus @B@: Kathete @BC@', 420, 'blau', 42, ein=3.8),
            # Fragebild: Dreieck, rechter Winkel bei C, Namen; die Höhen und H erst nach der Antwort
            graf(WK2, [V([A2k, B2k, C2k2]), RW(C2k2, richtung(C2k2, B2k), richtung(C2k2, A2k), 5)] + ECK2k, ein=0.05),
            graf(WK2, [S(A2k, C2k2, 2, dicke=6)], ein=3.8, raster=False),
            graf(WK2, [S(B2k, C2k2, 2, dicke=6)], ein=6.1, raster=False),
            graf(WK2, [S(C2k2, F2k, 2, True, 3), RW(F2k, richtung(F2k, B2k), richtung(F2k, C2k2), 2), PK(C2k2, 3, 0.13),
                       T(C2k2[0] + 0.35, C2k2[1] + 0.1, 'H', 3, 'start', 32)], ein=8.5, raster=False)),
         sz('Frage 3',
            'Gleich weit von den drei Seiten ist der Inkreismittelpunkt. Er liegt auf allen drei Winkelhalbierenden.',
            f(r'M_I: \ \text{Winkelhalbierende}', 300, 52, ein=1.0)),
         sz('Frage 4',
            'S teilt die Seitenhalbierende zwei zu eins. Zwei Drittel von sieben Komma fünf sind fünf Zentimeter.',
            f(r'\overline{AS} = \tfrac{2}{3} \cdot 7.5 = \fc{5\,\mathrm{cm}}', 300, 52, ein=1.0)),
         sz('Frage 5',
            'Die Winkelhalbierende teilt Alpha in zwei gleiche Hälften: je zweiunddreissig Grad.',
            f(r'64^\circ : 2 = \fc{32^\circ}', 300, 56, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Höhe durch die Ecke, Mittelsenkrechte durch die Seitenmitte. Der Schwerpunkt teilt zwei zu eins.',
            titel('Zum Mitnehmen', 250, 76),
            n('Höhe: durch die Ecke|Mittelsenkrechte: durch die Seitenmitte|@S@ teilt @2 : 1@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Welche Linie ist im Bild orange gestrichelt?',
              ['die Mittelsenkrechte von c', 'die Höhe von C aus', 'die Seitenhalbierende von C aus'], 0,
              {0: 'Ja.', 1: 'Geht die Linie durch die Ecke C?', 2: 'Geht die Linie durch C? Und steht sie senkrecht?'},
              sprich='Welche Linie ist im Bild orange gestrichelt?',
              rueck_sprich={1: 'Geht die Linie durch die Ecke C?', 2: 'Geht die Linie durch C? Und steht sie senkrecht?'}),
         klick('Frage 2', 'Das Dreieck hat bei C einen rechten Winkel. Tipp den Höhenschnittpunkt H an.', list(C2k2), 'Getroffen: H liegt auf C.',
               [{'bei': list(A2k), 'text': 'Das ist die Ecke A. Welche Linien sind hier die Höhen aus A und aus B?',
                 'sprich': 'Das ist die Ecke A. Welche Linien sind hier die Höhen aus A und aus B?'},
                {'bei': list(B2k), 'text': 'Das ist die Ecke B. Welche Linien sind hier die Höhen aus A und aus B?',
                 'sprich': 'Das ist die Ecke B. Welche Linien sind hier die Höhen aus A und aus B?'},
                {'bei': r3(M2k), 'text': 'Das ist die Mitte der Hypotenuse. Dort liegt der Umkreismittelpunkt, nicht H.',
                 'sprich': 'Das ist die Mitte der Hypotenuse. Dort liegt der Umkreismittelpunkt, nicht H.'},
                {'bei': r3(F2k), 'text': 'Das ist der Fusspunkt der Höhe aus C. Wo schneiden sich alle drei Höhen?',
                 'sprich': 'Das ist der Fusspunkt der Höhe aus C. Wo schneiden sich alle drei Höhen?'}],
               FALSCH, sprich='Das Dreieck hat bei C einen rechten Winkel. Tipp den Höhenschnittpunkt H an.', falsch_sprich=FALSCH, tol=0.6),
         wahl('Frage 3', 'Welcher Punkt ist von allen drei Seiten gleich weit entfernt?',
              ['der Inkreismittelpunkt', 'der Umkreismittelpunkt', 'der Schwerpunkt'], 0,
              {0: 'Ja.', 1: 'Der ist gleich weit von den drei Ecken. Gefragt sind die Seiten.',
               2: 'Welche Linien halten gleichen Abstand zu zwei Seiten?'},
              sprich='Welcher Punkt ist von allen drei Seiten gleich weit entfernt?',
              rueck_sprich={1: 'Der ist gleich weit von den drei Ecken. Gefragt sind die Seiten.',
                            2: 'Welche Linien halten gleichen Abstand zu zwei Seiten?'}),
         wahl('Frage 4', 'Die Seitenhalbierende von A aus ist 7.5 cm lang. Wie weit ist S von A entfernt?',
              ['5 cm', '3.75 cm', '2.5 cm'], 0,
              {0: 'Ja.', 1: 'Das ist die Hälfte. S teilt im Verhältnis 2 : 1.',
               2: 'Das ist der kürzere Teil, von S bis zur Seitenmitte.'},
              sprich='Die Seitenhalbierende von A aus ist sieben Komma fünf Zentimeter lang. Wie weit ist S von A entfernt?',
              rueck_sprich={1: 'Das ist die Hälfte. S teilt im Verhältnis zwei zu eins.',
                            2: 'Das ist der kürzere Teil, von S bis zur Seitenmitte.'}),
         wahl('Frage 5', 'α = 64°. Welchen Winkel schliesst die Winkelhalbierende von α mit der Seite c ein?',
              ['32°', '64°', '26°'], 0,
              {0: 'Ja.', 1: 'Das ist der ganze Winkel α.', 2: 'Das ist 90° − 64°. Die Winkelhalbierende halbiert.'},
              sprich='Alpha gleich vierundsechzig Grad. Welchen Winkel schliesst die Winkelhalbierende von Alpha mit der Seite c ein?',
              rueck_sprich={1: 'Das ist der ganze Winkel Alpha.', 2: 'Das ist neunzig minus vierundsechzig. Die Winkelhalbierende halbiert.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung «Fläche und Umfang»
W3 = geo(-0.5, -1.5, 11)
# Grundseiten und Höhen: A(1 | 1), B(8 | 1), C(5 | 6), spitzwinklig — alle drei Höhenfüsse auf den Seiten.
A3, B3, C3 = (1, 1), (8, 1), (5, 6)
FA3, FB3, FC3 = lot(A3, B3, C3), lot(B3, A3, C3), lot(C3, A3, B3)
# Warum die Hälfte: A(0.5 | 1), B(6.5 | 1), C(2.5 | 5): g = 6, h = 4. Kopie um die Mitte von BC (4.5 | 3) um 180° gedreht
# → Parallelogramm A B A' C mit A'(8.5 | 5); das linke Stück (0.5 | 1)(2.5 | 1)(2.5 | 5) wandert um 6 nach rechts → Rechteck 6 × 4.
A3h, B3h, C3h = (0.5, 1), (6.5, 1), (2.5, 5)
M3h = mitte(B3h, C3h)
# Höhe aus der Fläche: B(1 | 1), C(7 | 1) (a = 6), A(3 | 6): h_a = 5, A = 15.
# Umfang: A(1 | 1), B(8 | 1), C mit b = 5, a = 6: C(3.714 | 5.199), U = 18.
C3u = (1 + 38 / 14, 1 + math.sqrt(25 - (38 / 14) ** 2))
print('Kap. 3: Höhenfüsse', r3(FA3), r3(FB3), r3(FC3), '| Umfang-C', r3(C3u), round(abst(C3u, (8, 1)), 3), round(abst(C3u, (1, 1)), 3))
SEITE = lambda p, q, farbe=2: S(p, q, farbe, dicke=9)
ECK3 = ecken((A3, 'A', -0.45, -0.6), (B3, 'B', 0.45, -0.6), (C3, 'C', 0, 0.45))

clip('flaeche', 5, 'Dreiecke sehen: Fläche und Umfang',
     'Jede Seite kann Grundseite sein, zu jeder gehört eine Höhe — der Abstand der Gegenecke von der Geraden der Grundseite. '
     'Zwei gleiche Dreiecke ergeben ein Parallelogramm und daraus ein Rechteck: A = ½ · g · h. Die Spitze parallel '
     'verschieben, h aus der Fläche, der Umfang.',
     ['Dreieck', 'Flächeninhalt', 'Höhe', 'Grundseite', 'Abstand', 'Umfang'], [
         sz('Grundseite und Höhe',
            'Jede der drei Seiten kann Grundseite sein. Zu jeder gehört eine eigene Höhe: der Abstand der gegenüberliegenden '
            'Ecke von der Geraden durch die Grundseite. Gemessen wird senkrecht.',
            f(r'\text{Grundseite } g, \ \text{Höhe } \fb{h} \perp g', 300, 46, ein=0.4),
            n('Höhe = Abstand der Ecke|von der Geraden der Grundseite', 420, 'blau', 42, ein=5.2),
            graf(W3, [V([A3, B3, C3])] + ECK3, ein=0.3),
            # je eine Grundseite mit ihrer Höhe (c, dann a, dann b), Ton nach der Vertonung nachgeführt
            graf(W3, [SEITE(A3, B3, 5), S(C3, FC3, 2, dicke=4), RW(FC3, 0, 90, 2)], ein=1.6, aus=3.6, raster=False),
            graf(W3, [SEITE(B3, C3, 5), S(A3, FA3, 2, dicke=4), RW(FA3, richtung(FA3, B3), richtung(FA3, A3), 2)], ein=3.6, aus=5.4, raster=False),
            graf(W3, [SEITE(C3, A3, 5), S(B3, FB3, 2, dicke=4), RW(FB3, richtung(FB3, A3), richtung(FB3, B3), 2)], ein=5.4, raster=False)),
         sz('Warum die Hälfte',
            'Leg ein zweites, gleiches Dreieck gedreht daneben. Zusammen bilden sie ein Parallelogramm. Schneid links ein '
            'Stück ab und setz es rechts an: Es entsteht ein Rechteck mit der Grundseite g und der Höhe h. Das Dreieck ist '
            'die Hälfte davon.',
            f(r'A = \tfrac{1}{2} \cdot g \cdot \fb{h}', 300, 62, ein=12.0),
            # Das Original verliert beim Abschneiden sein linkes Stück (Prüfung 08.10.2026, D-M4: es blieb stehen)
            graf(W3, [mit(V([A3h, B3h, C3h], 1, 0.2), aus=6.5), mit(V([(2.5, 1), B3h, C3h], 1, 0.2), ein=6.5),
                      mit(V([A3h, B3h, C3h], 2, 0.2), ein=1.0, um=r3(M3h), bewegung=[[1.9, {'drehung': 0}], [3.3, {'drehung': 180}]]),
                      mit(T(3.5, 0.3, 'g', 5), ein=9.6), mit(S((2.5, 5), (2.5, 1), 5, True, 2.5), ein=10.6), mit(T(2.2, 3, 'h', 5, 'end'), ein=10.6)], ein=0.3),
            # «Schneid links ein Stück ab» (Ton 5.35–6.6): das Stück erscheint; «und setz es rechts an» (6.65–7.6): es wandert
            # um 6 nach rechts (Wortzeiten aus wortzeiten.json)
            graf(W3, [mit(V([(0.5, 1), (2.5, 1), (2.5, 5)], 3, 0.3), bewegung=[[6.5, {}], [7.5, {'punkte': [[6.5, 1], [8.5, 1], [8.5, 5]]}]])],
                 ein=5.4, raster=False),
            graf(W3, [V([(2.5, 1), (8.5, 1), (8.5, 5), (2.5, 5)], 3, 0.0, dicke=6)], ein=8.4, raster=False)),
         sz('Vorgelöst',
            'Zum Beispiel: Grundseite sechs Zentimeter, Höhe vier Zentimeter. Die Fläche ist ein Halb mal sechs mal vier, gleich '
            'zwölf Quadratzentimeter.',
            f(r'g = 6\,\mathrm{cm}, \quad \fb{h} = 4\,\mathrm{cm}', 300, 50, ein=0.4),
            f(r'A = \tfrac{1}{2} \cdot 6 \cdot 4 = \fc{12\,\mathrm{cm}^2}', 420, 50, ein=6.4),
            graf(W3, [V([A3h, B3h, C3h]), S((2.5, 5), (2.5, 1), 2, True), RW((2.5, 1), 0, 90, 2),
                      T(3.5, 0.3, 'g = 6 cm', 5, g=28, kursiv=False), T(2.75, 2.2, 'h = 4 cm', 2, 'start', 28, False)], ein=0.3)),
         sz('Spitze verschieben',
            'Schieb die Spitze parallel zur Grundseite. Die Form ändert sich, Grundseite und Höhe bleiben gleich. Liegt die Spitze '
            'weit rechts, trifft die Höhe die Verlängerung der Grundseite. Die Fläche bleibt zwölf Quadratzentimeter.',
            f(r'g, \ h \text{ gleich} \;\Rightarrow\; A = 12\,\mathrm{cm}^2', 300, 48, ein=9.8),
            graf(W3, [S((-0.5, 5), (10.5, 5), 5, True, 2),
                      mit(V([A3h, B3h, C3h]), bewegung=[[0.8, {}], [4.4, {'punkte': [[0.5, 1], [6.5, 1], [9.5, 5]]}]]),
                      mit(S((6.5, 1), (10, 1), 5, True, 2.5), ein=7.8),
                      mit(S((2.5, 5), (2.5, 1), 2, True, 3), bewegung=[[0.8, {}], [4.4, {'von': [9.5, 5], 'bis': [9.5, 1]}]]),
                      mit(RW((2.5, 1), 0, 90, 2), bewegung=[[0.8, {}], [4.4, {'bei': [9.5, 1]}]]),
                      mit(T(2.3, 3, 'h', 2, 'end', 32), bewegung=[[0.8, {}], [4.4, {'bei': [9.3, 3]}]]),
                      T(3.5, 0.3, 'g = 6', 5, g=28, kursiv=False)], ein=0.3)),
         sz('Höhe aus der Fläche',
            'Umgekehrt: Kennst du die Fläche und eine Seite, ist die zugehörige Höhe zwei mal Fläche durch Seite. Ist a sechs '
            'Zentimeter und die Fläche fünfzehn Quadratzentimeter, ist h a gleich dreissig durch sechs, also fünf Zentimeter. '
            'So weit ist A von der Geraden durch B und C entfernt.',
            f(r'\fb{h} = \dfrac{2A}{g}', 290, 58, ein=3.4),
            f(r'\fb{h_a} = \dfrac{2 \cdot 15}{6} = \fc{5\,\mathrm{cm}}', 440, 50, ein=11.8),
            graf(W3, [V([(1, 1), (7, 1), (3, 6)]), T(4, 0.3, 'a = 6 cm', 5, g=28, kursiv=False), T(4.6, 2.2, 'Fläche 15 cm²', 5, g=26, kursiv=False)]
                 + ecken(((3, 6), 'A', 0, 0.45), ((1, 1), 'B', -0.45, -0.6), ((7, 1), 'C', 0.45, -0.6)), ein=0.3),
            graf(W3, [S((3, 6), (3, 1), 2, True), RW((3, 1), 0, 90, 2), *IDX(3.2, 4.4, 'h', 'a', 2, 30, 11)], ein=11.8, raster=False)),
         sz('Umfang',
            'Der Umfang ist die Summe der drei Seiten: sechs plus fünf plus sieben, gleich achtzehn Zentimeter.',
            f(r'U = a + b + c', 300, 58, ein=0.4),
            f(r'U = 6 + 5 + 7 = \fc{18\,\mathrm{cm}}', 420, 50, ein=4.6),
            graf(W3, [V([(1, 1), (8, 1), C3u])] + ecken(((1, 1), 'A', -0.45, -0.6), ((8, 1), 'B', 0.45, -0.6), (C3u, 'C', 0, 0.45))
                 + [T(4.5, 0.3, 'c = 7', 5, g=28, kursiv=False), T(1.6, 3.4, 'b = 5', 5, 'end', 28, False),
                    T(6.25, 3.4, 'a = 6', 5, 'start', 28, False)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Fläche gleich ein Halb mal Grundseite mal zugehörige Höhe. Die Höhe ist der Abstand der Ecke von der '
            'Geraden durch die Grundseite, auch ausserhalb des Dreiecks.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'A = \tfrac{1}{2} \cdot g \cdot \fb{h} \qquad \fb{h} = \dfrac{2A}{g}', 400, 54, ein=1.2),
            n('@h@: Abstand zur Geraden der Grundseite', 540, 'blau', 42, ein=4.5),
            graf(W3, [S((-0.5, 5), (10.5, 5), 5, True, 2), V([(0.5, 1), (6.5, 1), (9.5, 5)]), S((6.5, 1), (10, 1), 5, True, 2.5),
                      S((9.5, 5), (9.5, 1), 2, True, 3), RW((9.5, 1), 180, 90, 2), T(9.2, 3, 'h', 2, 'end', 32), T(3.5, 0.3, 'g', 5, g=32)],
                 ein=4.5)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
# Frage 2: Grundseite b = AC mit C(0 | 0), A(6 | 0), B(8 | 4) (gegen den Uhrzeigersinn A → B → C): Lot von B auf die Gerade AC
# trifft (8 | 0), rechts von A auf der Verlängerung.
WK3 = ach(-1.5, -3, 11, (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), (-2, -1, 1, 2, 3, 4, 5, 6, 7))
clip('kontrolle-flaeche', 6, 'Dreiecke sehen: Kontrollfragen zu Fläche und Umfang',
     'Fünf Fragen: die Fläche aus g und h, den Fusspunkt einer Höhe ausserhalb, h aus A und g, was beim Verschieben der Spitze '
     'gleich bleibt und eine zweite Höhe aus derselben Fläche.',
     ['Dreieck', 'Flächeninhalt', 'Höhe', 'Kontrollfragen'], [
         # Frage 1 mit g = 7, h = 4 (vorher 6 und 5 — dieselben Zahlen wie «Höhe aus der Fläche» im Einführungsclip)
         sz('Frage 1',
            'Ein Halb mal sieben mal vier ergibt vierzehn Quadratzentimeter.',
            f(r'A = \tfrac{1}{2} \cdot 7 \cdot 4 = \fc{14\,\mathrm{cm}^2}', 300, 54, ein=1.0),
            graf(W3, [V([(1, 1), (8, 1), (5.5, 5)]), S((5.5, 5), (5.5, 1), 2, True), RW((5.5, 1), 0, 90, 2),
                      T(4.5, 0.3, 'g = 7 cm', 5, g=28, kursiv=False), T(5.3, 2.8, 'h = 4 cm', 2, 'end', 28, False)], ein=0.05)),
         sz('Frage 2',
            'Die Höhe h b steht senkrecht auf der Geraden durch A und C. Ihr Fusspunkt liegt bei acht, null: auf der '
            'Verlängerung über A hinaus.',
            f(r'\text{Fusspunkt } (\fc{8} \mid 0)', 300, 56, ein=1.0),
            graf(WK3, [V([(6, 0), (8, 4), (0, 0)]), T(5.95, 0.45, 'A', kursiv=False), T(8.3, 4.35, 'B', kursiv=False),
                       T(-0.45, 0.3, 'C', kursiv=False)], ein=0.05),
            graf(WK3, [S((6, 0), (9, 0), 5, True, 2.5), S((8, 4), (8, 0), 2, True), RW((8, 0), 180, 90, 2)],
                 punkte_=[pt((8, 0), 3, '(8 | 0)', (8.25, -0.75))], ein=1.2)),
         sz('Frage 3',
            'Zwei mal zwanzig durch acht: Die Höhe ist fünf Zentimeter.',
            f(r'h = \dfrac{2 \cdot 20}{8} = \fc{5\,\mathrm{cm}}', 300, 54, ein=1.0)),
         sz('Frage 4',
            'Grundseite und Höhe bleiben gleich, also auch die Fläche. Die Seiten und die Winkel ändern sich.',
            f(r'g, \ h \text{ gleich} \;\Rightarrow\; A \text{ gleich}', 300, 50, ein=1.0)),
         sz('Frage 5',
            'Die Fläche ist ein Halb mal acht mal drei, gleich zwölf. Zur Seite b gehört h b gleich zwei mal zwölf durch sechs, '
            'also vier Zentimeter.',
            f(r'A = \tfrac{1}{2} \cdot 8 \cdot 3 = 12\,\mathrm{cm}^2', 300, 48, ein=1.0),
            f(r'h_b = \dfrac{2 \cdot 12}{6} = \fc{4\,\mathrm{cm}}', 420, 50, ein=7.2)),
         sz('Merke',
            'Zum Mitnehmen: Fläche gleich ein Halb mal g mal h. Jede Höhe gehört zu ihrer Grundseite.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'A = \tfrac{1}{2}\, g\, h \qquad h = \dfrac{2A}{g}', 400, 54, ein=1.2)),
     ], [
         wahl('Frage 1', 'g = 7 cm, h = 4 cm: Wie gross ist die Fläche?', ['14 cm²', '28 cm²', '11 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist g mal h: das Rechteck. Das Dreieck ist die Hälfte.', 2: 'Das ist g plus h. Eine Fläche ist ein Produkt.'},
              sprich='g gleich sieben Zentimeter, h gleich vier Zentimeter: Wie gross ist die Fläche?',
              rueck_sprich={1: 'Das ist g mal h: das Rechteck. Das Dreieck ist die Hälfte.', 2: 'Das ist g plus h. Eine Fläche ist ein Produkt.'}),
         klick('Frage 2', 'Die Grundseite ist b = AC. Tipp den Fusspunkt der Höhe von B an.', [8, 0], 'Getroffen: (8 | 0).',
               [{'bei': [6, 0], 'text': 'Das ist A. Die Höhe steht senkrecht auf der Geraden AC, auch ausserhalb der Seite.',
                 'sprich': 'Das ist A. Die Höhe steht senkrecht auf der Geraden A C, auch ausserhalb der Seite.'},
                {'bei': [3, 0], 'text': 'Das ist die Mitte von AC. Gesucht ist das Lot von B.',
                 'sprich': 'Das ist die Mitte von A C. Gesucht ist das Lot von B.'}],
               FALSCH, sprich='Die Grundseite ist b gleich A C. Tipp den Fusspunkt der Höhe von B an.', falsch_sprich=FALSCH,
               eingabe=['x', 'y']),
         wahl('Frage 3', 'A = 20 cm², g = 8 cm: Wie gross ist h?', ['5 cm', '2.5 cm', '160 cm'], 0,
              {0: 'Ja.', 1: 'Das ist A durch g. Denk an den Faktor ein Halb in der Formel.', 2: 'Teilen, nicht multiplizieren.'},
              sprich='A gleich zwanzig Quadratzentimeter, g gleich acht Zentimeter: Wie gross ist h?',
              rueck_sprich={1: 'Das ist A durch g. Denk an den Faktor ein Halb in der Formel.', 2: 'Teilen, nicht multiplizieren.'}),
         wahl('Frage 4', 'Die Spitze wandert parallel zur Grundseite. Was bleibt gleich?', ['die Fläche', 'der Umfang', 'die Winkel'], 0,
              {0: 'Ja.', 1: 'Die schrägen Seiten werden länger oder kürzer. Was steht in der Flächenformel?',
               2: 'Die Form ändert sich. Was steht in der Flächenformel?'},
              sprich='Die Spitze wandert parallel zur Grundseite. Was bleibt gleich?',
              rueck_sprich={1: 'Die schrägen Seiten werden länger oder kürzer. Was steht in der Flächenformel?',
                            2: 'Die Form ändert sich. Was steht in der Flächenformel?'}),
         wahl('Frage 5', 'a = 8 cm, die Höhe auf a ist 3 cm, b = 6 cm. Wie lang ist die Höhe auf b?', ['4 cm', '2.25 cm', '12 cm'], 0,
              {0: 'Ja.', 1: 'Zur kürzeren Seite gehört die längere Höhe. Rechne zuerst die Fläche.',
               2: 'Das ist die Fläche. Daraus folgt die Höhe: 2A durch b.'},
              sprich='a gleich acht Zentimeter, die Höhe auf a ist drei Zentimeter, b gleich sechs Zentimeter. Wie lang ist die Höhe auf b?',
              rueck_sprich={1: 'Zur kürzeren Seite gehört die längere Höhe. Rechne zuerst die Fläche.',
                            2: 'Das ist die Fläche. Daraus folgt die Höhe: zwei A durch b.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung «Rechtwinklige Dreiecke und Pythagoras»
# 3-4-5 mit dem rechten Winkel bei C(3 | 3): A(7 | 3), B(3 | 6). Quadrate nach aussen: auf b unten, auf a links,
# auf c oben rechts (A + (3 | 4), B + (3 | 4)). Karo = 1 cm: die Quadrate zählen 9, 16 und 25 Kästchen.
W4 = geo(-1, -1.5, 12)
C4, A4, B4 = (3, 3), (7, 3), (3, 6)
QA4 = [(3, 3), (3, 6), (0, 6), (0, 3)]          # Quadrat über a = BC
QB4 = [(3, 3), (7, 3), (7, -1), (3, -1)]        # Quadrat über b = CA
QC4 = [(7, 3), (3, 6), (6, 10), (10, 7)]        # Quadrat über c = AB
ECK4 = ecken((A4, 'A', 0.45, -0.1), (B4, 'B', -0.1, 0.45), (C4, 'C', -0.45, -0.55))
TRI4 = [V([A4, B4, C4]), RW(C4, 0, 90, 5)] + ECK4
W4g = geo(-1, -1.5, 15)
# Kathete: C(1 | 1), B(1 | 6) (a = 5), A(13 | 1) (b = 12), c = 13 (Themenseite A3).
# Gleichschenklig: Basis 12, Schenkel 10 → Höhe 8: (1 | 1), (13 | 1), (7 | 9).
# Gleichseitig: s = 8 → h = 4√3 ≈ 6.93: (2 | 1), (10 | 1), (6 | 7.928).
HG = 4 * math.sqrt(3)
# Nur rechtwinklig: a = 5, b = 7, γ = 80°: c ≈ 7.86, nicht √74 ≈ 8.60.
C4n = (2, 1.5)
A4n = (2 + 7, 1.5)
B4n = (2 + 5 * math.cos(math.radians(80)), 1.5 + 5 * math.sin(math.radians(80)))
print('Kap. 4: h gleichseitig', round(HG, 3), '| 80°-Dreieck c', round(abst(A4n, B4n), 3), 'statt', round(math.sqrt(74), 3))

clip('pythagoras', 7, 'Dreiecke sehen: Rechtwinklige Dreiecke und Pythagoras',
     'Katheten und Hypotenuse erkennen; der Satz des Pythagoras als Flächensatz; Hypotenuse und Kathete berechnen; die Höhe '
     'im gleichschenkligen und im gleichseitigen Dreieck; der Satz gilt nur mit rechtem Winkel.',
     ['Pythagoras', 'Kathete', 'Hypotenuse', 'gleichschenklig', 'gleichseitig', 'Höhe'], [
         sz('Katheten und Hypotenuse',
            'Im rechtwinkligen Dreieck heissen die beiden Seiten am rechten Winkel Katheten. Die Seite gegenüber dem rechten '
            'Winkel heisst Hypotenuse. Sie ist die längste Seite.',
            f(r'\text{Katheten: am rechten Winkel}', 300, 46, ein=4.0),
            f(r'\text{Hypotenuse: gegenüber, am längsten}', 400, 46, ein=6.9),
            graf(W4, TRI4, ein=0.3),
            graf(W4, [S(B4, C4, 2, dicke=7), S(C4, A4, 2, dicke=7), T(2.55, 4.5, 'a', 2, 'end', 32), T(5, 2.3, 'b', 2, g=32)], ein=4.0, raster=False),
            graf(W4, [S(A4, B4, 3, dicke=7), T(5.35, 4.9, 'c', 3, 'start', 32)], ein=6.9, raster=False)),
         sz('Der Satz',
            'Setz auf jede Seite ein Quadrat. Die Quadrate über den Katheten haben zusammen genau so viel Fläche wie das Quadrat '
            'über der Hypotenuse: a Quadrat plus b Quadrat gleich c Quadrat.',
            f(r'\fb{a^2} + \fb{b^2} = \fc{c^2}', 300, 66, ein=7.0),
            n('nur mit rechtem Winkel bei @C@', 430, 'blau', 42, ein=9.6),
            graf(W4, TRI4, ein=0.3),
            graf(W4, [V(QA4, 2, 0.18), V(QB4, 2, 0.18), T(1.5, 4.3, '9', 2, g=34, kursiv=False), T(5, 0.8, '16', 2, g=34, kursiv=False)],
                 ein=1.0, raster=False),
            graf(W4, [V(QC4, 3, 0.18), T(6.5, 6.3, '25', 3, g=34, kursiv=False)], ein=5.8, raster=False)),
         sz('Hypotenuse berechnen',
            'Zum Beispiel die Katheten drei und vier Zentimeter. Dann ist c Quadrat gleich neun plus sechzehn, also fünfundzwanzig, '
            'und c ist die Wurzel daraus: fünf Zentimeter.',
            f(r'c^2 = 3^2 + 4^2 = 25', 300, 56, ein=6.0),
            f(r'c = \sqrt{25} = \fc{5\,\mathrm{cm}}', 420, 56, ein=9.2),
            graf(W4, TRI4 + [T(2.55, 4.5, '3', 5, 'end', 32, False), T(5, 2.3, '4', 5, g=32, kursiv=False)], ein=0.3),
            graf(W4, [T(5.35, 4.9, '5', 3, 'start', 32, False)], ein=9.2, raster=False)),
         sz('Kathete berechnen',
            'Gesucht ist eine Kathete: Hypotenuse dreizehn, die andere Kathete fünf. Jetzt wird subtrahiert: b Quadrat gleich '
            'hundertneunundsechzig minus fünfundzwanzig, gleich hundertvierundvierzig. b ist zwölf Zentimeter.',
            f(r'b^2 = c^2 - a^2', 300, 56, ein=5.2),
            f(r'b^2 = 169 - 25 = 144', 410, 50, ein=9.3),
            f(r'b = \sqrt{144} = \fc{12\,\mathrm{cm}}', 520, 50, ein=11.0),
            graf(W4g, [V([(13, 1), (1, 6), (1, 1)]), RW((1, 1), 0, 90, 5), T(0.6, 3.5, 'a = 5', 5, 'end', 30, False),
                       T(7.5, 4.0, 'c = 13', 5, 'start', 30, False), mit(T(7, 0.1, 'b = ?', 3, g=30, kursiv=False), aus=11.0)], ein=0.3),
            graf(W4g, [T(7, 0.1, 'b = 12', 3, g=30, kursiv=False)], ein=11.0, raster=False)),
         sz('Gleichschenklig',
            'Im gleichschenkligen Dreieck halbiert die Höhe die Basis. Sie ist zugleich Seitenhalbierende, Winkelhalbierende und '
            'Mittelsenkrechte. So entstehen zwei rechtwinklige Hälften: Schenkel zehn, halbe Basis sechs, also Höhe acht.',
            f(r'h^2 = 10^2 - 6^2 = 64', 300, 52, ein=10.0),
            f(r'h = \fc{8}', 410, 56, ein=12.4),
            graf(W4g, [V([(1, 1), (13, 1), (7, 9)]), T(3.6, 5.3, '10', 5, 'end', 30, False), T(10.4, 5.3, '10', 5, 'start', 30, False)], ein=0.3),
            graf(W4g, [S((7, 9), (7, 1), 2, True, 4), RW((7, 1), 0, 90, 2),
                       S((3.9, 0.75), (4.1, 1.25), 5, dicke=3), S((9.9, 0.75), (10.1, 1.25), 5, dicke=3)], ein=1.9, raster=False),
            graf(W4g, [V([(7, 1), (13, 1), (7, 9)], 3, 0.2), T(10, 0.1, '6', 3, g=30, kursiv=False), T(6.7, 5, 'h', 3, 'end', 32)],
                 ein=7.8, raster=False)),
         sz('Gleichseitig',
            'Im gleichseitigen Dreieck mit der Seite s ist die halbe Seite eine Kathete. Bei s gleich acht: h Quadrat gleich '
            'vierundsechzig minus sechzehn, gleich achtundvierzig, h gleich Wurzel achtundvierzig, rund sechs Komma neun drei.',
            f(r'h^2 = 8^2 - 4^2 = 48', 300, 52, ein=6.6),
            f(r'h = \sqrt{48} \approx \fc{6.93}', 420, 52, ein=9.7),
            graf(W4g, [V([(2, 1), (10, 1), (6, 1 + HG)]), T(3.5, 4.6, 's = 8', 5, 'end', 30, False), S((6, 1 + HG), (6, 1), 2, True, 4),
                       RW((6, 1), 0, 90, 2), T(8, 0.1, '4', 3, g=30, kursiv=False)], ein=0.3),
            graf(W4g, [T(6.3, 3.4, 'h', 3, 'start', 34)], ein=8.0, raster=False)),
         sz('Nur rechtwinklig',
            'Achtung: Der Satz gilt nur im rechtwinkligen Dreieck. Hier ist Gamma achtzig Grad. Dann ist c Quadrat nicht a Quadrat '
            'plus b Quadrat.',
            f(r'\gamma = 80^\circ: \quad \fd{c^2 \neq a^2 + b^2}', 300, 52, ein=5.2),
            graf(W4, [V([A4n, B4n, C4n]), WI(C4n, A4n, B4n, 4, 40), wlabel(C4n, A4n, B4n, '80°', 4, 1.15, kursiv=False),
                      T(1.7, 4.0, 'a = 5', 5, 'end', 30, False), T(5.5, 0.8, 'b = 7', 5, g=30, kursiv=False)]
                 + ecken((A4n, 'A', 0.45, -0.2), (B4n, 'B', 0, 0.45), (C4n, 'C', -0.45, -0.5)), ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Nur im rechtwinkligen Dreieck gilt a Quadrat plus b Quadrat gleich c Quadrat, mit der Hypotenuse c '
            'gegenüber dem rechten Winkel. Für eine Kathete wird subtrahiert.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\fb{a^2} + \fb{b^2} = \fc{c^2}', 400, 60, ein=1.2),
            n('Hypotenuse @c@: gegenüber dem rechten Winkel|Kathete: @b = \\sqrt{c^2 - a^2}@', 520, 'blau', 42, ein=5.3),
            graf(W4, TRI4 + [V(QA4, 2, 0.18), V(QB4, 2, 0.18), V(QC4, 3, 0.18)], ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
# Frage 1: rechter Winkel bei R(2 | 2), P = R + 4.5 (cos 70°, sin 70°), Q = R + 5.5 (cos −20°, sin −20°); Hypotenuse PQ schräg.
WK4 = geo(0, -1, 9)
WK4b = geo(-0.5, -1, 10)
R4k = (2, 2)
P4k = (2 + 4.5 * math.cos(math.radians(70)), 2 + 4.5 * math.sin(math.radians(70)))
Q4k = (2 + 5.5 * math.cos(math.radians(-20)), 2 + 5.5 * math.sin(math.radians(-20)))
print('Kontrolle 4: P', r3(P4k), 'Q', r3(Q4k), 'PQ', round(abst(P4k, Q4k), 3))
clip('kontrolle-pythagoras', 8, 'Dreiecke sehen: Kontrollfragen zu Pythagoras',
     'Fünf Fragen: die Hypotenuse erkennen, Hypotenuse und Kathete berechnen, die Höhe im gleichschenkligen Dreieck und wann '
     'der Satz nicht gilt.',
     ['Pythagoras', 'Hypotenuse', 'Kathete', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Hypotenuse liegt dem rechten Winkel gegenüber: die Seite P Q.',
            f(r'\text{Hypotenuse} = \overline{PQ}', 300, 56, ein=1.0),
            graf(WK4, [V([P4k, Q4k, R4k]), RW(R4k, -20, 70, 5)]
                 + ecken((P4k, 'P', 0, 0.45), (Q4k, 'Q', 0.45, -0.3), (R4k, 'R', -0.45, -0.4)), ein=0.05),
            graf(WK4, [S(P4k, Q4k, 3, dicke=8)], ein=1.0, raster=False)),
         # Fragen 2 bis 5 mit eigenen Zahlen (Prüfung 08.10.2026, D-M4: vorher 6-8-10, 5-12-13 und a = 5, b = 7, γ = 80° wie im
         # Einführungsclip und in der Arbeitsfläche)
         sz('Frage 2',
            'c Quadrat gleich fünfundzwanzig plus sechsunddreissig, gleich einundsechzig. c ist die Wurzel daraus, rund sieben '
            'Komma acht eins Zentimeter.',
            f(r'c = \sqrt{25 + 36} = \sqrt{61} \approx \fc{7.81\,\mathrm{cm}}', 300, 50, ein=1.0),
            # Fragebild: nur die gegebenen Katheten (5 und 6, massstäblich); die Hypotenuse erst nach der Antwort.
            # Der Graf hält zugleich ein Fenster in der Szene: Ein verspäteter Start, der über Frage 1 springt, findet
            # sonst für die Klickfrage kein tippbares Bild (pruef-fragen, Fall B2).
            graf(WK4b, [V([(1, 1), (7, 1), (1, 6)]), RW((1, 1), 0, 90, 5), T(0.55, 3.5, '5', 5, 'end', 34, False),
                        T(4, 0.25, '6', 5, 'middle', 34, False)], ein=0.05),
            graf(WK4b, [S((7, 1), (1, 6), 3, dicke=7), T(4.35, 3.85, '≈ 7.81', 3, 'start', 34, False)], ein=1.0, raster=False)),
         sz('Frage 3',
            'Für eine Kathete wird subtrahiert: einundachtzig minus sechzehn, gleich fünfundsechzig. b ist die Wurzel daraus, '
            'rund acht Komma null sechs Zentimeter.',
            f(r'b = \sqrt{81 - 16} = \sqrt{65} \approx \fc{8.06\,\mathrm{cm}}', 300, 50, ein=1.0)),
         sz('Frage 4',
            'Die Höhe halbiert die Basis: halbe Basis drei. h Quadrat gleich vierundsechzig minus neun, gleich fünfundfünfzig. '
            'Die Höhe ist rund sieben Komma vier zwei Zentimeter.',
            f(r'h = \sqrt{8^2 - 3^2} = \sqrt{55} \approx \fc{7.42\,\mathrm{cm}}', 300, 48, ein=1.0)),
         sz('Frage 5',
            'Nein. Der Satz des Pythagoras braucht einen rechten Winkel zwischen a und b. Fünfundsiebzig Grad ist kein rechter '
            'Winkel.',
            f(r'\gamma = 75^\circ \neq 90^\circ', 300, 56, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Hypotenuse gegenüber dem rechten Winkel. Für die Hypotenuse addieren, für eine Kathete subtrahieren.',
            titel('Zum Mitnehmen', 250, 76),
            n('@c^2 = a^2 + b^2@|@b^2 = c^2 - a^2@', 400, 'blau', 46, ein=1.2)),
     ], [
         # Ziel ist die Strecke PQ, die Fallen sind die beiden Katheten (Toleranz 0.45, nachgezählt in zahlen.py).
         klick('Frage 1', 'Tipp die Hypotenuse an.', [r3(P4k), r3(Q4k)], 'Getroffen: PQ liegt dem rechten Winkel gegenüber.',
               [{'bei': [r3(R4k), r3(P4k)], 'text': 'Das ist eine Kathete: Sie liegt am rechten Winkel an.',
                 'sprich': 'Das ist eine Kathete. Sie liegt am rechten Winkel an.'},
                {'bei': [r3(R4k), r3(Q4k)], 'text': 'Das ist eine Kathete: Sie liegt am rechten Winkel an.',
                 'sprich': 'Das ist eine Kathete. Sie liegt am rechten Winkel an.'}],
               FALSCH_LINIE, sprich='Tipp die Hypotenuse an.', falsch_sprich=FALSCH_LINIE, tol=0.45),
         wahl('Frage 2', 'Die Katheten sind 5 cm und 6 cm lang. Wie lang ist die Hypotenuse?', ['≈ 7.81 cm', '11 cm', '61 cm'], 0,
              {0: 'Ja.', 1: 'Das ist 5 + 6. Addiert werden die Quadrate, danach die Wurzel.', 2: 'Das ist c². Zieh noch die Wurzel.'},
              sprich='Die Katheten sind fünf und sechs Zentimeter lang. Wie lang ist die Hypotenuse?',
              rueck_sprich={1: 'Das ist fünf plus sechs. Addiert werden die Quadrate, danach die Wurzel.',
                            2: 'Das ist c Quadrat. Zieh noch die Wurzel.'}),
         wahl('Frage 3', 'Hypotenuse 9 cm, eine Kathete 4 cm. Wie lang ist die andere Kathete?', ['≈ 8.06 cm', '≈ 9.85 cm', '5 cm'], 0,
              {0: 'Ja.', 1: 'Länger als die Hypotenuse? Für eine Kathete wird subtrahiert.', 2: 'Das ist 9 − 4. Subtrahiert werden die Quadrate.'},
              sprich='Hypotenuse neun Zentimeter, eine Kathete vier Zentimeter. Wie lang ist die andere Kathete?',
              rueck_sprich={1: 'Länger als die Hypotenuse? Für eine Kathete wird subtrahiert.',
                            2: 'Das ist neun minus vier. Subtrahiert werden die Quadrate.'}),
         wahl('Frage 4', 'Gleichschenkliges Dreieck: Basis 6 cm, Schenkel 8 cm. Wie hoch ist es?', ['≈ 7.42 cm', '≈ 5.29 cm', '≈ 8.54 cm'], 0,
              {0: 'Ja.', 1: 'Die Höhe halbiert die Basis. Rechne mit der halben Basis.',
               2: 'Höher als ein Schenkel? Der Schenkel ist hier die Hypotenuse.'},
              sprich='Gleichschenkliges Dreieck: Basis sechs Zentimeter, Schenkel acht Zentimeter. Wie hoch ist es?',
              rueck_sprich={1: 'Die Höhe halbiert die Basis. Rechne mit der halben Basis.',
                            2: 'Höher als ein Schenkel? Der Schenkel ist hier die Hypotenuse.'}),
         wahl('Frage 5', 'Ein Dreieck hat a = 4 cm, b = 9 cm und γ = 75°. Gilt c² = a² + b²?',
              ['Nein: γ ist kein rechter Winkel.', 'Ja, in jedem Dreieck.', 'Ja, weil c gegenüber von γ liegt.'], 0,
              {0: 'Ja.', 1: 'Was setzt der Satz des Pythagoras voraus?', 2: 'Was setzt der Satz des Pythagoras über γ voraus?'},
              sprich='Ein Dreieck hat a gleich vier, b gleich neun Zentimeter und Gamma gleich fünfundsiebzig Grad. Gilt c Quadrat gleich a Quadrat plus b Quadrat?',
              rueck_sprich={1: 'Was setzt der Satz des Pythagoras voraus?', 2: 'Was setzt der Satz des Pythagoras über Gamma voraus?'}),
     ], art='Kontrollclip')
