"""Rechnet alle Zahlen des Leitprogramms Dreiecke nach (08.10.2026): Vortest, Arbeitsbereiche, Clips, Kontrollfragen,
Kapitelaufgaben, Gesamttest samt typischen Fehlern des Bewertungsrasters, Klickflächen der Strecken-Klickfragen.

  python3 scripts/lp/dreiecke/zahlen.py        → «ALLE ZAHLEN STIMMEN» oder AssertionError
"""
import json
import math
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
sys.path.insert(0, SP)
from geom import punkte, lot, abst, winkel, wfuss, dritte_ecke, mitte  # noqa: E402

n = 0


def ist(a, b, tol=0.005, was=''):
    global n
    n += 1
    assert abs(a - b) <= tol, (was, a, b)


def r2(x):
    return round(x + 1e-12, 2)


sq = math.sqrt
# ---------------------------------------------------------------- Vortest
ist(180 - 65, 115, was='0b Nebenwinkel'); ist(7 * 4, 28); ist(2 * (7 + 4), 22)
ist(450 / 10000, 0.045, 1e-12, '0d'); ist(15 / 3, 5); ist(sq(30.25), 5.5)
Q0 = (2 + 2.5 / math.tan(math.radians(65)), 2.5)
ist(winkel(Q0, (0, 2.5), (2, 0)), 65, 1e-6, '0b Wechselwinkel im Bild')

# ---------------------------------------------------------------- Kapitel 1
ist(180 - 50 - 60, 70, was='Clip vorgelöst'); ist(180 - 60, 50 + 70)
C = dritte_ecke((1, 1.5), (8.5, 1.5), 50, 60); ist(winkel(C, (1, 1.5), (8.5, 1.5)), 70, 1e-6)
ist(winkel((1, 1.5), (8.5, 1.5), (3.5, 6.5)) + winkel((8.5, 1.5), (3.5, 6.5), (1, 1.5)), 180 - winkel((3.5, 6.5), (1, 1.5), (8.5, 1.5)), 1e-9)
# Kontrollfragen 1: 35 + 65 = 100 (β = 80), 180 − 40 − 50 = 90, 180 − 2·72 = 36
ist(180 - 35 - 65, 80); ist(35 + 65, 100); ist(180 - 40 - 50, 90); ist(180 - 144, 36)
# sim1: γ′ = 35 + 75 = 110; Fehler 70, 145, 105; gleichschenklig γ′ = 100 → α = 50, γ = 80
ist(35 + 75, 110); ist(180 - 110, 70); ist(180 - 35, 145); ist(180 - 75, 105); ist(100 / 2, 50); ist(180 - 100, 80)
ist((180 - 100) / 2, 40, was='Fehler γ = 100 angenommen')
# Ziel «β möglichst gross bei α = 120°»: Schritt 5°, α + β < 180 → 55
assert max(b for b in range(10, 151, 5) if 120 + b < 180) == 55
# Aufgaben 1b, 1c, 1e
ist(180 - 115, 65); ist(180 - 38 - 65, 77); ist(38 + 65, 103); ist(180 - 77, 103)
C1b = dritte_ecke((0, 0), (6, 0), 38, 65); ist(winkel((6, 0), (8, 0), C1b), 115, 1e-6, '1b Bild')
ist(180 - 116, 64); ist(180 - 2 * 64, 52); ist(116 / 2, 58, was='1c typischer Fehler'); ist(90 / 2, 45)

# ---------------------------------------------------------------- Kapitel 2
P = punkte((1, 1), (9, 1), (3, 6.5))
ist(P['H'][0], 3, 1e-9); ist(P['MU'][0], 5, 1e-9)
for e in ((1, 1), (9, 1), (3, 6.5)):
    ist(abst(P['MU'], e), P['ru'], 1e-9, 'M_U gleich weit')
ist(9 * 2 / 3, 6, was='Clip 2:1'); ist(9 / 3, 3)
# sim2: s_c von C(0 | 4) nach M_c(3 | 0) = 5, CS = 10/3; Umkreis bei C(1 | 4): r ≈ 3.30
ist(abst((0, 4), (3, 0)), 5, 1e-12); ist(5 * 2 / 3, 3.33, 0.006, 'CS'); ist(5 / 3, 1.67, 0.004)
Pm = punkte((0, 0), (6, 0), (1, 4)); ist(Pm['ru'], 3.30, 0.006, 'M_U A'); ist(abst(Pm['MU'], (1, 4)), Pm['ru'], 1e-9)
ist(2 * Pm['ru'], 6.6, 0.011)
# Arbeitsbereich 2: H ausserhalb ⇔ stumpf, H auf Ecke ⇔ rechtwinklig — Start C(2 | 3.5) spitz
ist(2 * (2 - 6) + 3.5 ** 2, 4.25)
assert [(x / 2, y / 2) for x in range(-4, 17) for y in range(2, 12) if abs(x / 2 * (x / 2 - 6) + (y / 2) ** 2) < 1e-9] == [(3.0, 3.0)]
# Kontrollfragen 2: (neu 08.10.2026) Frage 2 H im rechtwinkligen Dreieck A(1 | 1), B(9 | 2), C(3 | 5) = C; 7.5 · 2/3 = 5, 64/2 = 32
A2k, B2k, C2k = (1, 1), (9, 2), (3, 5)
ist((A2k[0] - C2k[0]) * (B2k[0] - C2k[0]) + (A2k[1] - C2k[1]) * (B2k[1] - C2k[1]), 0, 1e-12, 'K2 F2 rechter Winkel bei C')
ist(abst(punkte(A2k, B2k, C2k)['H'], C2k), 0, 1e-9, 'K2 F2 H = C')
F2 = json.load(open(R + 'clips/g5-2a-lp-kontrolle-elemente.json'))['fragen'][1]
for f_ in F2['fallen']:                       # keine Falle im Toleranzkreis des Ziels, Fallen untereinander getrennt
    assert abst(f_['bei'], F2['ziel']) > 2 * F2['toleranz'], f_
ist(abst(F2['fallen'][3]['bei'], lot(C2k, A2k, B2k)), 0, 0.001, 'K2 F2 Falle Fusspunkt'); ist(abst(F2['fallen'][2]['bei'], mitte(A2k, B2k)), 0, 1e-9)
ist(7.5 * 2 / 3, 5); ist(7.5 / 2, 3.75); ist(7.5 / 3, 2.5); ist(64 / 2, 32); ist(90 - 64, 26)
# Clip «Stumpfes Dreieck»: Höhen reichen über Ecke, Fusspunkt und H; Namen in der Endlage nicht auf einem anderen Punkt
A2s, B2s, C2e = (1, 1), (6, 1), (7.5, 3.5)
Pe = punkte(A2s, B2s, C2e)
ist(winkel(B2s, A2s, C2e), 120.96, 0.01, 'stumpf bei B'); ist(winkel(B2s, A2s, (6, 4)), 90, 1e-9, 'rechter Winkel bei u = 2/3')
lab = {'H': (Pe['H'][0] + 0.25, Pe['H'][1] - 0.1), 'S': (Pe['S'][0] - 0.25 - 0.3, Pe['S'][1] - 0.55),
       'MI': (Pe['MI'][0] + 0.45, Pe['MI'][1] + 0.3), 'MU': (Pe['MU'][0] + 0.2, Pe['MU'][1] - 0.6)}
for k, q in lab.items():
    for k2 in ('H', 'S', 'MI', 'MU'):
        if k2 != k:
            assert abst(q, Pe[k2]) > 0.45, ('Beschriftung', k, 'auf', k2)
# … und M_I (Textmitte rund 0.25 rechts vom Anker) nicht auf der Höhe aus B (von H über B bis zum Fusspunkt auf AC)
fB = lot(B2s, A2s, C2e)
def _seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; q = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - q * dx, p[1] - a[1] - q * dy)
assert _seg((lab['MI'][0] + 0.25, lab['MI'][1] + 0.1), Pe['H'], fB) > 0.3, 'M_I-Beschriftung auf der Höhe aus B'
# Aufgaben 2a, 2b
S2a = ((0 + 8 + 1) / 3, (0 + 0 + 6) / 3); ist(S2a[0], 3, 1e-12); ist(S2a[1], 2, 1e-12)
ist(abst((1, 6), S2a), sq(20), 1e-12); ist(abst(S2a, (4, 0)), sq(5), 1e-12); ist(sq(20), 4.47, 0.005); ist(sq(5), 2.24, 0.005)
ist(180 - 70 - 50, 60); ist(60 / 2, 30); ist(180 - 70 - 30, 80); ist(180 - 80, 100); ist(180 - 50 - 30, 100)
D = wfuss(dritte_ecke((0, 0), (8, 0), 70, 50), (0, 0), (8, 0)); ist(winkel(D, (0, 0), dritte_ecke((0, 0), (8, 0), 70, 50)), 80, 1e-6, '2b geometrisch')

# ---------------------------------------------------------------- Kapitel 3
ist(6 * 4 / 2, 12, was='Clip/sim'); ist(2 * 15 / 6, 5); ist(6 + 5 + 7, 18)
C3u = (1 + 38 / 14, 1 + sq(25 - (38 / 14) ** 2)); ist(abst(C3u, (8, 1)), 6, 1e-9); ist(abst(C3u, (1, 1)), 5, 1e-9)
ist(abst((6, 0), (9, 4)), 5, 1e-12, 'sim3 BC'); ist(6 * 5 / 2, 15, was='Fehler schräge Seite'); ist(6 * 5, 30)
fa = lot((0, 0), (6, 0), (9, 4)); ist(abst((0, 0), fa), 4.8, 1e-9, 'h_a'); ist(24 / 5, 4.8); ist(12 / 5, 2.4)
assert ((fa[0] - 6) * 3 + fa[1] * 4) / 25 < 0, 'Fusspunkt von h_a auf der Verlängerung über B hinaus'
# Kontrollfragen 3: (neu) 7 · 4 / 2 = 14 (Fehler 28, 11); Fusspunkt (8 | 0); 40/8 = 5; h_b = 2·12/6 = 4 (Fehler 3·6/8 = 2.25)
ist(7 * 4 / 2, 14); ist(7 * 4, 28); ist(7 + 4, 11); ist(6 * 5 / 2, 15, was='Einführung: h_a aus 15 und 6'); ist(lot((8, 4), (6, 0), (0, 0))[0], 8, 1e-12); ist(2 * 20 / 8, 5); ist(20 / 8, 2.5); ist(8 * 3 / 2 * 2 / 6, 4); ist(3 * 6 / 8, 2.25)
# Aufgaben 3a–3e
ist(4 * 3 / 2, 6); ist(lot((6, 3), (0, 0), (4, 0))[0], 6, 1e-12); ist(9 * 4 / 2, 18); ist(2 * 18 / 6, 6)
ist(45 * 18 / 2, 405); ist(405 / 10000, 0.0405, 1e-12); ist(0.45 * 18 / 2, 4.05); ist((25 - 7) / 2, 9)

# ---------------------------------------------------------------- Kapitel 4
ist(sq(9 + 16), 5); ist(sq(169 - 25), 12); ist(sq(100 - 36), 8); ist(sq(10 ** 2 - 6 ** 2), 8)
ist(sq(64 - 16), 6.93, 0.005, 'gleichseitig s = 8'); ist(4 * sq(3), sq(48), 1e-12)
A4n, B4n, C4n = (9, 1.5), (2 + 5 * math.cos(math.radians(80)), 1.5 + 5 * math.sin(math.radians(80))), (2, 1.5)
ist(abst(A4n, B4n) ** 2, 74 - 70 * math.cos(math.radians(80)), 1e-9); assert abs(abst(A4n, B4n) - sq(74)) > 0.5
# sim4: c = 10 ⇔ (6, 8), (8, 6) auf dem Raster; b = √(64 − 12.25) ≈ 7.19; gs 6/5 → 4; gls 6 → √27
assert sorted((a / 2, b / 2) for a in range(2, 17) for b in range(2, 17) if (a / 2) ** 2 + (b / 2) ** 2 == 100) == [(6, 8), (8, 6)]
ist(sq(64 - 12.25), 7.19, 0.006); ist(sq(64 + 12.25), 8.73, 0.006); ist(sq(25 - 9), 4); ist(sq(25 + 9), 5.83, 0.006); ist(sq(27), 5.20, 0.006); ist(sq(36 + 9), 6.71, 0.006)
# Kontrollfragen 4 (neu 08.10.2026): Katheten 5, 6 → √61 ≈ 7.81 (Fehler 11, 61); Hypotenuse 9, Kathete 4 → √65 ≈ 8.06
# (Fehler √97 ≈ 9.85, 5); Basis 6, Schenkel 8 → √55 ≈ 7.42 (Fehler √28 ≈ 5.29, √73 ≈ 8.54); a = 4, b = 9, γ = 75°
ist(sq(25 + 36), 7.81, 0.005); ist(5 + 6, 11); ist(25 + 36, 61); ist(sq(81 - 16), 8.06, 0.005); ist(sq(81 + 16), 9.85, 0.005); ist(9 - 4, 5)
ist(sq(64 - 9), 7.42, 0.005); ist(sq(64 - 36), 5.29, 0.005); ist(sq(64 + 9), 8.54, 0.005)
assert abs(sq(16 + 81 - 72 * math.cos(math.radians(75))) - sq(97)) > 0.5, 'K4 F5: c ist nicht √(a² + b²)'
# Aufgaben 4a–4e
ist(sq(625 - 49), 24); ist(sq(75), 8.66, 0.005); ist(10 * sq(75) / 2, 43.30, 0.005); ist(sq(4.5 ** 2 - 1.2 ** 2), 4.34, 0.005)
ist(sq(81 + 144), 15); ist(9 * 12 / 2, 54); ist(108 / 15, 7.2, 1e-12)
ist(sq(36 + 16), 7.21, 0.005, '4e Lea'); assert 36 + 16 - 2 * 6 * 4 * math.cos(math.radians(110)) > 52, '4e: c länger als bei 90°'
# 4f: c = 5, BF = 2, h_c = 3.5 → a = √16.25 ≈ 4.03, b = √61.25 ≈ 7.83, U ≈ 16.86 (Fehler b = √(25 + 12.25) ≈ 6.10)
ist(sq(4 + 12.25), 4.03, 0.005); ist(sq(49 + 12.25), 7.83, 0.005); ist(5 + sq(16.25) + sq(61.25), 16.86, 0.005); ist(sq(25 + 12.25), 6.10, 0.005)
ist(abst((5, 0), (7, 3.5)), sq(16.25), 1e-12, '4f Bild'); ist(abst((0, 0), (7, 3.5)), sq(61.25), 1e-12)
_t, _s = math.radians(20), 0.16
Q4a = (7 * _s * math.cos(_t), 7 * _s * math.sin(_t)); R4a = (Q4a[0] - 24 * _s * math.sin(_t), Q4a[1] + 24 * _s * math.cos(_t))
ist(abst((0, 0), R4a) / _s, 25, 1e-9, '4a Bild massstäblich')

# ---------------------------------------------------------------- Gesamttest
# G1: β = 2α, γ′ = 126 → 3α = 126
al = 126 / 3; ist(al, 42); ist(2 * al, 84); ist(180 - 3 * al, 54); assert max(42, 84, 54) < 90
ist(126 / 2, 63, was='G1 Fehler (β = α)'); ist(180 - 126, 54)
# G3: α = 74, β = 46 → γ = 60; ∠ACF = 16, ∠ACD = 30, Winkel 14
ist(180 - 74 - 46, 60); ist(90 - 74, 16); ist(60 / 2, 30); ist(30 - 16, 14)
A, B = (0, 0), (8, 0); Cg = dritte_ecke(A, B, 74, 46)
F_, D_ = lot(Cg, A, B), wfuss(Cg, A, B)
ist(winkel(Cg, (F_[0], F_[1]), D_), 14, 1e-6, 'G3 geometrisch')
ist(90 - 46, 44, was='G3 Fehler: Höhe vom Winkel bei B aus'); ist(44 - 30, 14, was='G3 Fehler ergibt zufällig 14?')
# G4 (neu 08.10.2026): c = 7, BF = 4, h_c = 4.2 → a = 5.8 (20-21-29 · 0.2), A = 14.7, b = √138.64, h_b = 29.4 / b
ist(sq(4 ** 2 + 4.2 ** 2), 5.8, 1e-12, 'G4 a'); ist(abst((7, 0), (11, 4.2)), 5.8, 1e-12, 'G4 Bild')
ist(7 * 4.2 / 2, 14.7); ist(7 * 5.8 / 2, 20.3, was='Mia'); bG4 = sq(11 ** 2 + 4.2 ** 2); ist(bG4, 11.77, 0.005); ist(11 ** 2 + 4.2 ** 2, 138.64, 1e-9)
ist(29.4 / bG4, 2.50, 0.005, 'G4 h_b'); assert 29.4 / bG4 < 5.8
ist(29.4 / sq(66.64), 3.60, 0.005); ist(sq(49 + 17.64), 8.16, 0.005, 'G4 Fehler AF = c')
ist(sq(49 + 5.8 ** 2), 9.09, 0.005); ist(29.4 / sq(49 + 5.8 ** 2), 3.23, 0.005, 'G4 Fehler Pythagoras in ABC')
ist(2 * 20.3 / bG4, 3.45, 0.005, 'G4 Mias Fläche'); ist(2 * 29.4 / bG4, 4.99, 0.005, 'G4 ohne ½'); assert 2 * 29.4 / bG4 < 5.8
ist(14.7 / bG4, 1.25, 0.005, 'G4 ohne 2')
# G5: KM = 8.5 (Hypotenuse), KL = 4 → LM = 7.5; Fläche 15; Fehler √88.25 ≈ 9.39 > 8.5 (unmöglich, kein Folgepunkt)
ist(sq(8.5 ** 2 - 16), 7.5); ist(4 * 7.5 / 2, 15); ist(sq(8.5 ** 2 + 16), 9.39, 0.005); assert sq(8.5 ** 2 + 16) > 8.5
# G6: Giebel 9.6 breit, 3.6 hoch → Schräge 6; Fläche 17.28; Umfang 21.6; Fehler ganze Breite: Folgewert aus ungerundet 30.11
ist(sq(4.8 ** 2 + 3.6 ** 2), 6); ist(9.6 * 3.6 / 2, 17.28); ist(9.6 + 12, 21.6); ist(sq(9.6 ** 2 + 3.6 ** 2), 10.25, 0.005)
ist(9.6 + 2 * sq(9.6 ** 2 + 3.6 ** 2), 30.11, 0.005, 'G6 Folgewert'); ist(9.6 * 3.6, 34.56)
# G7 (neu): rechter Winkel bei C, CA = 7, CB = 12 → CM_a = 6, s_a = √85 ≈ 9.22, AS = ⅔ s_a ≈ 6.15
ist(sq(49 + 36), 9.22, 0.005); ist(2 / 3 * sq(85), 6.15, 0.005); ist(2 / 3 * 9.22, 6.15, 0.005, 'G7 aus gerundetem s_a')
ist(sq(49 + 144), 13.89, 0.005); ist(2 / 3 * sq(193), 9.26, 0.005); ist(sq(85) / 3, 3.07, 0.005); ist(sq(85) / 2, 4.61, 0.005)
S7 = ((0 + 12 + 0) / 3, (7 + 0 + 0) / 3); ist(abst((0, 7), S7), 2 / 3 * sq(85), 1e-9, 'G7 Schwerpunkt geometrisch')

# ---------------------------------------------------------------- Sperrliste der Übungen (seite.js)
import re as _re
_sp = _re.search(r'var SPERRE = \[(.*?)\];', open(SP + 'seite.js').read(), _re.S).group(1)
SPERRE = set(_re.findall(r"'([^']+)'", _sp))
for k in ('da|42|54|84', 'wv|2|54', 'hw|74', 'gss|9.6|3.6', 'pk|8.5|4', 'ph|6|7', 'au|7|4|4.2|b', 'au|5|2|3.5|a', 'au|5|2|3.5|b',
          'ph|5|6', 'pk|9|4', 'gsh|6|8', 'fa|7|4', 'fh|20|8', 'fz|8|3|6', 'da|40|50|90', 'wa|35|65', 'gb|72', 'sp|s|7.5', 'wh|64'):
    assert k in SPERRE, ('Sperrliste', k)

# ---------------------------------------------------------------- Klickflächen der Strecken-Klickfragen
def fuss(p, z):
    (ax, ay), (bx, by) = z
    dx, dy = bx - ax, by - ay
    q = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return (ax + dx * q, ay + dy * q)


for clip in ('g5-2a-lp-kontrolle-winkel', 'g5-2a-lp-kontrolle-pythagoras'):
    F = json.load(open(R + 'clips/' + clip + '.json'))['fragen'][0]
    tol = F['toleranz']
    for name, sg in [('ziel', F['ziel'])] + [('falle', f['bei']) for f in F['fallen']]:
        treffer = 0
        for i in range(200):
            t = (i + 0.5) / 200
            p = (sg[0][0] + t * (sg[1][0] - sg[0][0]), sg[0][1] + t * (sg[1][1] - sg[0][1]))
            treffer += abst(p, fuss(p, F['ziel'])) <= tol
        anteil = treffer / 200
        if name == 'ziel':
            assert anteil == 1, (clip, anteil)
        else:
            assert anteil <= 0.15, (clip, 'falsche Seite zählt zu oft als richtig', anteil)

print('ALLE ZAHLEN STIMMEN (%d Prüfungen)' % n)
