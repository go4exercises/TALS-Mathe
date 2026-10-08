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
# Kontrollfragen 2: Fusspunkt (7 | 0), 7.5 · 2/3 = 5, 64/2 = 32
ist(lot((7, 3), (0, 0), (5, 0))[0], 7, 1e-12); ist(7.5 * 2 / 3, 5); ist(7.5 / 2, 3.75); ist(7.5 / 3, 2.5); ist(64 / 2, 32); ist(90 - 64, 26)
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
# Kontrollfragen 3: 15; Fusspunkt (8 | 0); 40/8 = 5; h_b = 2·12/6 = 4 (Fehler 3·6/8 = 2.25)
ist(6 * 5 / 2, 15); ist(lot((8, 4), (6, 0), (0, 0))[0], 8, 1e-12); ist(2 * 20 / 8, 5); ist(20 / 8, 2.5); ist(8 * 3 / 2 * 2 / 6, 4); ist(3 * 6 / 8, 2.25)
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
# Kontrollfragen 4: 10, 8, 12 (Fehler √(169 − 100) ≈ 8.31, √(169 + 25) ≈ 13.93)
ist(sq(36 + 64), 10); ist(sq(100 - 36), 8); ist(sq(100 + 36), 11.66, 0.006); ist(sq(169 - 25), 12); ist(sq(169 - 100), 8.31, 0.006); ist(sq(169 + 25), 13.93, 0.006)
# Aufgaben 4a–4e
ist(sq(625 - 49), 24); ist(sq(75), 8.66, 0.005); ist(10 * sq(75) / 2, 43.30, 0.005); ist(sq(4.5 ** 2 - 1.2 ** 2), 4.34, 0.005)
ist(sq(81 + 144), 15); ist(9 * 12 / 2, 54); ist(108 / 15, 7.2, 1e-12); ist(sq(25 + 49), 8.60, 0.005)
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
# G4: c = 9, BC = 5, h = 4, Fusspunkt 3 cm hinter B → C(12 | 4)
ist(abst((9, 0), (12, 4)), 5, 1e-12); ist(9 * 4 / 2, 18); ist(9 * 5 / 2, 22.5); ist(sq(12 ** 2 + 4 ** 2), 12.65, 0.005)
ist(9 + 5 + sq(160), 26.65, 0.005, 'G4 Umfang')
# G5: KM = 8.5 (Hypotenuse), KL = 4 → LM = 7.5; Fläche 15
ist(sq(8.5 ** 2 - 16), 7.5); ist(4 * 7.5 / 2, 15); ist(sq(8.5 ** 2 + 16), 9.39, 0.005)
# G6: Giebel 9.6 breit, 3.6 hoch → Schräge 6; Fläche 17.28; Umfang 21.6
ist(sq(4.8 ** 2 + 3.6 ** 2), 6); ist(9.6 * 3.6 / 2, 17.28); ist(9.6 + 12, 21.6); ist(sq(9.6 ** 2 + 3.6 ** 2), 10.25, 0.005)
# G7: Katheten 2.5 und 6 → 6.5 (Jonas: 8.5)
ist(sq(2.5 ** 2 + 36), 6.5); ist(2.5 + 6, 8.5)

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
