"""Rechnet alle festen Zahlen des Leitprogramms Quadratische Gleichungen nach (11.10.2026).

  python3 scripts/lp/quadratische-gleichungen/zahlen.py [--schreiben]

Mit --schreiben wird zuerst die Sperrliste FESTE_Q in seite.js aus den festen Gleichungen neu geschrieben.

Prüft je feste Gleichung (Clips, Kontrollfragen, Umformer, Festhalten, Kapitelaufgaben, Vortest, Gesamttest)
die behauptete Lösungsmenge, Diskriminanten, Fehlerwerte der Rückmeldungen und Parameterfälle — exakt mit
Brüchen, Wurzeln als (p, q, r) für (p ± q·√r). Dazu: Keine feste quadratische Gleichung kommt an zwei Orten vor
(gleiche gekürzte Normalform), ausser in der Liste ERLAUBT_DOPPELT, und jede steht in der Sperrliste FESTE_Q
von seite.js. Muss mit «ALLE ZAHLEN STIMMEN» enden.
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as F

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
FEHLER = []


def pruef(bed, text):
    if not bed:
        FEHLER.append(text)
        print('  FEHLER:', text)


def loes(a, b, c):
    """Reelle Lösungen von a x² + b x + c = 0 (a ≠ 0) als sortierte Liste: rationale als Fraction,
    irrationale als float. Dazu D."""
    a, b, c = F(a), F(b), F(c)
    D = b * b - 4 * a * c
    if D < 0:
        return [], D
    if D == 0:
        return [-b / (2 * a)], D
    w = math.isqrt(D.numerator * D.denominator)
    if w * w == D.numerator * D.denominator:     # D Quadrat einer rationalen Zahl
        s = F(w, D.denominator)
        return sorted([(-b - s) / (2 * a), (-b + s) / (2 * a)]), D
    s = math.sqrt(D)
    return sorted([(-b - s) / (2 * a), (-b + s) / (2 * a)]), D


def gleich(L, soll):
    if len(L) != len(soll):
        return False
    return all(abs(float(x) - float(y)) < 1e-9 for x, y in zip(sorted(L, key=float), sorted(soll, key=float)))


def schl(q):
    a, b, c = (F(v) for v in q)
    if a < 0:
        a, b, c = -a, -b, -c
    # gekürzt auf ganze, teilerfremde Zahlen
    nenner = math.lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = (int(v * nenner) for v in (a, b, c))
    g = math.gcd(math.gcd(a, b), c) or 1
    return (a // g, b // g, c // g)


ORTE = {}          # Normalform -> [Orte]
QUAD = []          # alle festen quadratischen Gleichungen als [a, b, c]


def q(ort, a, b, c, soll=None, D=None, sperren=True):
    """Feste quadratische Gleichung a x² + b x + c = 0 mit behaupteter Lösungsmenge soll."""
    L, d = loes(a, b, c)
    if soll is not None:
        pruef(gleich(L, soll), f'{ort}: {a}x² + {b}x + {c} = 0 hat {[str(x) for x in L]}, behauptet {soll}')
    if D is not None:
        pruef(d == D, f'{ort}: D = {d}, behauptet {D}')
    k = schl((a, b, c))
    ORTE.setdefault(k, []).append(ort)
    if sperren:
        QUAD.append(k)
    return L, d


def wert(a, b, c, x):
    return F(a) * F(x) ** 2 + F(b) * F(x) + F(c)


# ════════════════════════════════════════════════════════════════ Clips
print('Clips')
# Kapitel 1 · wurzel
q('Clip wurzel Normalform', 2, 8, -10)            # 2x² + 8x − 10 = 0 → x² + 4x − 5 = 0
pruef(schl((2, 8, -10)) == (1, 4, -5), 'Clip wurzel: Normalform x² + 4x − 5')
q('Clip wurzel x² = 9', 1, 0, -9, [-3, 3])
q('Clip wurzel (x − 2)² = 9', 1, -4, 4 - 9, [-1, 5])
# kontrolle-wurzel
q('Kontr. wurzel F1 x(x + 2) = 5', 1, 2, -5)
pruef(schl((3, -9, 6)) == (1, -3, 2), 'Kontr. wurzel F2: Normalform x² − 3x + 2')
q('Kontr. wurzel F2', 3, -9, 6, [1, 2])
q('Kontr. wurzel F3 x² = 64', 1, 0, -64, [-8, 8])
q('Kontr. wurzel F4 x² + 25 = 0', 1, 0, 25, [])
q('Kontr. wurzel F5 (x + 1)² = 9', 1, 2, 1 - 9, [-4, 2])
# Fallen F5: 4 (Vorzeichen, (x − 1)² = 9 gäbe −2 und 4), 3 (Klammer = 3 genommen), −4 (die negative)
pruef(gleich(loes(1, -2, 1 - 9)[0], [-2, 4]), 'Kontr. wurzel F5 Falle: (x − 1)² = 9 hat 4')
# Kapitel 2 · faktorisieren
q('Clip fakt. x² = 5x', 1, -5, 0, [0, 5])
q('Clip fakt. Binom x² − 6x + 9', 1, -6, 9, [3])
q('Clip fakt. Zweiklammer x² − 7x + 12', 1, -7, 12, [3, 4])
# kontrolle-faktorisieren
q('Kontr. fakt. F1 x(x − 6) = 0', 1, -6, 0, [0, 6])
q('Kontr. fakt. F2 3x² = 12x', 3, -12, 0, [0, 4])
pruef(wert(3, -12, 0, -4) != 0, 'Kontr. fakt. F2: −4 ist keine Lösung (Rückmeldung «Setz −4 ein»)')
q('Kontr. fakt. F3 x² − 10x + 25', 1, -10, 25, [5])
pruef((-2) * 7 == -14 and -2 + 7 == 5, 'Kontr. fakt. F4: (x + 2)(x − 7) = x² − 5x − 14')
q('Kontr. fakt. F4 x² − 5x − 14', 1, -5, -14, [-2, 7])
pruef(2 * 7 == 14 and 2 * -12 == -24, 'Kontr. fakt. F4 Fallen: −7 gibt +14, 12 gibt −24')
q('Kontr. fakt. F5 x² + 3x − 10', 1, 3, -10, [-5, 2])
pruef(wert(1, 3, -10, 5) == 30 and wert(1, 3, -10, -2) == -12, 'Kontr. fakt. F5 Fallen: 25 + 15 − 10 = 30; 4 − 6 − 10 = −12')
# Kapitel 3 · formel
pruef((F(6, 2)) ** 2 == 9, 'Clip formel Ecke (6/2)² = 9')
q('Clip formel x² + 6x − 16', 1, 6, -16, [-8, 2])
pruef(16 + 9 == 25, 'Clip formel 16 + 9 = 25')
q('Clip formel 2x² − 5x − 3', 2, -5, -3, [F(-1, 2), 3], D=49)
for c, d in ((5, 16), (9, 0), (10, -4)):
    q(f'Clip formel x² − 6x + {c}', 1, -6, c, D=d)
# kontrolle-formel
pruef((F(8, 2)) ** 2 == 16, 'Kontr. formel F1: (8/2)² = 16')
q('Kontr. formel F2 (x − 3)² = 16', 1, -6, 9 - 16, [-1, 7])
q('Kontr. formel F3/F4 2x² − 3x − 5', 2, -3, -5, [-1, F(5, 2)], D=49)
pruef(F(-3 + 7, 4) == 1 and F(-3 - 7, 4) == F(-5, 2), 'Kontr. formel F4 Falle −b falsch: {1; −2.5}')
pruef(F(3 + 7, 2) == 5 and F(3 - 7, 2) == -2, 'Kontr. formel F4 Falle Nenner a: {−2; 5}')
pruef(9 - 40 == -31 and -9 + 40 == 31, 'Kontr. formel F3 Fallen −31, 31')
q('Kontr. formel F5 x² − 6x + 8', 1, -6, 8, [2, 4], D=4)
# Kapitel 4 · verfahren
pruef(all(F(x - 1) ** 2 == x * x + 7 for x in [F(-3)]), 'Clip verfahren (x − 1)² = x² + 7 bei x = −3')
q('Clip verfahren 3x² − 48', 3, 0, -48, [-4, 4])
q('Clip verfahren x² + 9x', 1, 9, 0, [-9, 0])
q('Clip verfahren x² − 8x + 15', 1, -8, 15, [3, 5])
q('Clip verfahren 3x² + 2x − 2', 3, 2, -2, D=28)
q('Clip verfahren x(x + 4) = 12', 1, 4, -12, [-6, 2])
# kontrolle-verfahren
q('Kontr. verf. F1 5x² − 20', 5, 0, -20, [-2, 2])
q('Kontr. verf. F2 3x² + 4x − 2', 3, 4, -2, D=40)
pruef(all((x - 4) ** 2 == x * x + 8 for x in [F(1)]) and (F(-1) - 4) ** 2 != 1 + 8, 'Kontr. verf. F3: x = 1, nicht −1')
q('Kontr. verf. F4 x² + 4x − 21', 1, 4, -21, [-7, 3])
q('Kontr. verf. F5 x(x − 2) = 8', 1, -2, -8, [-2, 4])
pruef(2 * 0 != 8 and (-4) * (-6) == 24, 'Kontr. verf. F5 Fallen: 2 · 0 = 0; (−4)(−6) = 24')
# Kapitel 5 · parameter
for k, n in ((5, 2), (8, 2), (9, 1), (11, 0)):
    L, d = loes(1, -6, k)
    pruef(len(L) == n and d == 36 - 4 * k, f'Clip parameter x² − 6x + {k}: {n} Lösungen')
for k, n in ((5, 2), (4, 1), (0, 0), (-4, 1), (-5, 2)):
    L, d = loes(1, k, 4)
    pruef(len(L) == n and d == k * k - 16, f'Clip parameter x² + {k}x + 4: {n} Lösungen')
pruef(loes(1, 4, 4)[0] == [-2] and loes(1, -4, 4)[0] == [2], 'Clip parameter: doppelte Lösungen −2 und 2')
for m, n in ((1, 2), (F(-4, 3), 1), (-1, 2), (-2, 0)):
    L, d = loes(m, -4, -3)
    pruef(len(L) == n and d == 16 + 12 * F(m), f'Clip parameter m x² − 4x − 3, m = {m}: {n}')
pruef(loes(F(-4, 3), -4, -3)[0] == [F(-3, 2)], 'Clip parameter m = −4/3: x = −1.5')
pruef(gleich(loes(-1, -4, -3)[0], [-3, -1]), 'Clip parameter m = −1: Nullstellen −3, −1')
# kontrolle-parameter
pruef(loes(1, 6, 9)[0] == [-3], 'Kontr. param. F2: k = 9, x = −3')
pruef(36 + 36 == 72 and 36 - 144 == -108, 'Kontr. param. F2 Rückmeldungen D(−9), D(36)')
pruef(loes(1, 8, 16)[1] == 0 and loes(1, -8, 16)[1] == 0 and loes(1, 4, 16)[1] != 0, 'Kontr. param. F3: k = ±8')
pruef(F(1, 4) == F(-1, -4), 'Kontr. param. F4: −4x + 1 = 0 → x = 0.25')
pruef(all(loes(1, 2, -k * k)[1] == 4 + 4 * k * k > 0 for k in range(-5, 6)), 'Kontr. param. F5: D = 4 + 4k² > 0')

# ════════════════════════════════════════════════════════════════ Umformer
print('Umformer')
q('Umformer 1.1 3x² − 75', 3, 0, -75, [-5, 5])
q('Umformer 1.2 x² + 7 = 3', 1, 0, 4, [])
pruef((-2) ** 2 + 7 == 11, 'Umformer 1.2 Rückmeldung (−2)² + 7 = 11')
q('Umformer 1.3 (x − 1)² = 25', 1, -2, 1 - 25, [-4, 6])
q('Umformer 1.4 4x² = 9', 4, 0, -9, [F(-3, 2), F(3, 2)])
q('Umformer 1.5 2(x + 4)² − 50', 2, 16, 32 - 50, [-9, 1])
q('Umformer 1.6 (x + 2)² = 0', 1, 4, 4, [-2])
q('Umformer 2.1 2x² = 7x', 2, -7, 0, [0, F(7, 2)])
q('Umformer 2.2 x² + 8x + 16', 1, 8, 16, [-4])
q('Umformer 2.3 x² − 2x − 15', 1, -2, -15, [-3, 5])
q('Umformer 2.4 x² − 36', 1, 0, -36, [-6, 6])
q('Umformer 2.5 (x − 3)(x + 5)', 1, 2, -15, [-5, 3])
q('Umformer 2.6 x² + 10x + 21', 1, 10, 21, [-7, -3])
q('Umformer 3.1 x² − 10x + 21', 1, -10, 21, [3, 7])
pruef(F(10, 2) ** 2 == 25 and 25 - 21 == 4, 'Umformer 3.1: +25, rechts 4')
q('Umformer 3.2 2x² + 12x + 10', 2, 12, 10, [-5, -1])
pruef(9 - 5 == 4, 'Umformer 3.2: rechts −5 + 9 = 4')
q('Umformer 3.3 3x² + 5x − 2', 3, 5, -2, [-2, F(1, 3)], D=49)
q('Umformer 3.4 x² − 3x + 4', 1, -3, 4, [], D=-7)
q('Umformer 3.5 4x² + 4x + 1', 4, 4, 1, [F(-1, 2)], D=0)
q('Umformer 3.6 −x² + 3x + 4', -1, 3, 4, [-1, 4], D=25)
pruef(F(-3 + 5, -2) == -1 and F(-3 - 5, -2) == 4, 'Umformer 3.6: (−3 ± 5) : (−2)')
q('Umformer 4.1 x² − 11x + 30', 1, -11, 30, [5, 6], D=1)
q('Umformer 4.2 2x² = 98', 2, 0, -98, [-7, 7])
pruef((3 + 2) ** 2 == 9 + 16, 'Umformer 4.3 (x + 2)² = x² + 16 bei x = 3')
q('Umformer 4.4 x(x − 3) = 10', 1, -3, -10, [-2, 5])
q('Umformer 4.5 5x² − 3x − 2', 5, -3, -2, [F(-2, 5), 1], D=49)
q('Umformer 4.6 2x² + 6x', 2, 6, 0, [-3, 0])

# ════════════════════════════════════════════════════════════════ Kapitelaufgaben, Vortest
print('Kapitelaufgaben')
pruef(schl((1, -4, -7)) == (1, -4, -7), '1a')
q('1a x(x − 4) = 7', 1, -4, -7)
q('1a 3 − x² = 0', -1, 0, 3)
q('1b −2x² + 10x − 8', -2, 10, -8, [1, 4])
pruef(schl((-2, 10, -8)) == (1, -5, 4), '1b: p = −5, q = 4')
q('1c 2x² = 162', 2, 0, -162, [-9, 9])
q('1c x² + 9 = 0', 1, 0, 9, [])
q('1d (x − 5)² = 36', 1, -10, 25 - 36, [-1, 11])
q('1e x² + 25 = 169', 1, 0, 25 - 169, [-12, 12])
pruef(8 * 8 + 25 != 169, '1e: x = 8 aus «x + 5 = 13» ist falsch')
q('1f (x − 1)² = 4', 1, -2, -3, [-1, 3])
q('2a 4x² + 20x', 4, 20, 0, [-5, 0])
q('2b x² − 14x + 49', 1, -14, 49, [7])
q('2c x² + 3x − 28', 1, 3, -28, [-7, 4])
q('2d (x − 1)(x − 4) = 10', 1, -5, 4 - 10, [-1, 6])
pruef((11 - 1) * (11 - 4) == 70 and (14 - 1) * (14 - 4) == 130, '2d: die falschen Werte 11 und 14')
q('2e x² + 2x − 3', 1, 2, -3, [-3, 1])
q('2f Lösungen 1 und −6', 1, 5, -6, [-6, 1])
L, d = q('3a x² − 8x + 13', 1, -8, 13)
pruef(gleich(L, [4 - math.sqrt(3), 4 + math.sqrt(3)]) and -13 + 16 == 3, '3a: (x − 4)² = 3, 4 ± √3')
pruef(round(4 - math.sqrt(3), 2) == 2.27 and round(4 + math.sqrt(3), 2) == 5.73, '3a: ≈ 2.27 und 5.73')
q('3b 2x² + x − 6', 2, 1, -6, [-2, F(3, 2)], D=49)
L, d = q('3c x² − 2x − 4', 1, -2, -4, D=20)
pruef(gleich(L, [1 - math.sqrt(5), 1 + math.sqrt(5)]), '3c: 1 ± √5')
q('3d(a) x² + 5x + 7', 1, 5, 7, [], D=-3)
q('3d(b) 4x² − 20x + 25', 4, -20, 25, [F(5, 2)], D=0)
q('3d(c) 3x² − x − 1', 3, -1, -1, D=13)
pruef(True, '3e allgemein (x + p/2)² = (p/2)² − q: keine Zahlen')
for c, d, n in ((3, 4, 2), (4, 0, 1), (6, -8, 0)):
    L, dd = q(f'3f x² − 4x + {c}', 1, -4, c, D=d)
    pruef(len(L) == n, f'3f c = {c}: {n} Nullstellen')
q('4a(a) 9x² − 4', 9, 0, -4, [F(-2, 3), F(2, 3)])
q('4a(b) x² − 13x', 1, -13, 0, [0, 13])
q('4a(c) x² + 2x − 24', 1, 2, -24, [-6, 4])
L, d = q('4a(d) 2x² − 3x − 1', 2, -3, -1, D=17)
pruef(gleich(L, [(3 - math.sqrt(17)) / 4, (3 + math.sqrt(17)) / 4]), '4a(d): (3 ± √17)/4')
pruef((3 * F(-1) - 1) ** 2 == 9 * 1 + 7, '4b: x = −1')
q('4c (x − 2)(x + 3) = 2x', 1, -1, -6, [-2, 3])
pruef((3 - 2) * (3 + 3) == 6 and (-2 - 2) * (-2 + 3) == -4, '4c Probe')
q('4d x² + x − 20', 1, 1, -20, [-5, 4])
q('4e x² − 4x = 12', 1, -4, -12, [-2, 6])
L, d = loes(1, 10, 25)
pruef(L == [-5], '5a: k = 25, x = −5')
pruef(loes(1, 6, 9)[0] == [-3] and loes(1, -6, 9)[0] == [3], '5b: k = ±6, x = ∓3')
pruef(loes(1, -4, 1 - (-3))[1] == 0 and loes(1, -4, 1 - (-3))[0] == [2], '5c: k = −3, Scheitel (2 | −3)')
pruef(16 - 4 * (1 - F(-3)) == 0, '5c: D(k) = 12 + 4k = 0 bei k = −3')
pruef(F(-4, 8) == F(-1, 2) and loes(5 - 1, 8, 4)[0] == [-1] and 80 - 16 * 5 == 0, '5d: m = 1 → x = −0.5; m = 5 → x = −1')
for m, nn in ((0, 2), (3, 2), (6, 0), (-2, 2)):
    pruef(len(loes(m - 1, 8, 4)[0]) == nn and loes(m - 1, 8, 4)[1] == 80 - 16 * m, f'5d m = {m}: {nn} Lösungen, D = 80 − 16m')
pruef(F(1, 3) == F(-(-1), 3) and 9 > 0, '5e: k = 0 → 3x − 1 = 0, x = 1/3; D(0) = 9')
for t in (-3, 0, 2, 5):
    pruef(gleich(loes(1, -4 * t, 4 * t * t - 1)[0], [2 * t - 1, 2 * t + 1]) and loes(1, -4 * t, 4 * t * t - 1)[1] == 4, f'5f: t = {t}: x = 2t ± 1, D = 4')
pruef(gleich(loes(1, -4, 3)[0], [1, 3]), '5f Probe t = 1')
print('Vortest')
pruef([1, -8, 16] == [1, -8, 16], '0a (x − 4)²')
pruef((1, -1, -12) == (1, 3 - 4, 3 * -4), '0a (x + 3)(x − 4) = x² − x − 12')
for k, v in (((1, -8, 16), 'Vortest (x − 4)²'), ((1, -1, -12), 'Vortest (x + 3)(x − 4)'), ((6, -9, 0), 'Vortest 6x² − 9x'),
             ((1, 7, 0), 'Vortest x² + 7x'), ((1, 12, 36), 'Vortest x² + 12x + 36'), ((1, 0, -100), 'Vortest x² − 100'),
             ((1, 1, -6), 'Vortest x² + x − 6')):
    q(v, *k)
pruef(5 * 4 - 3 == 2 * 4 + 9, '0e: 5x − 3 = 2x + 9, x = 4')

# ════════════════════════════════════════════════════════════════ Gesamttest
print('Gesamttest')
q('G1 x² + 10x + 25 = 9', 1, 10, 25 - 9, [-8, -2])
q('G1(b) x² + 10x + 25 = −1', 1, 10, 26, [], D=-4)
pruef(gleich(loes(1, -10, 16)[0], [2, 8]), 'G1 Fehler (x − 5)² = 9: {2; 8}')
q('G2(a) (x − 4)² = 3(x − 4)', 1, -11, 28, [4, 7])
pruef((7 - 4) ** 2 == 3 * (7 - 4) and (4 - 4) ** 2 == 0, 'G2(a) Probe; durch (x − 4) geteilt bleibt nur 7')
q('G2(b) x² − x = 30', 1, -1, -30, [-5, 6])
L, d = q('G3 x(x + 6) = −2', 1, 6, 2, D=28)
pruef(gleich(L, [-3 - math.sqrt(7), -3 + math.sqrt(7)]), 'G3: −3 ± √7')
pruef(-2 * (-2 + 6) != -2 and -8 * (-8 + 6) != -2, 'G3 Fehler Nullprodukt: −2 und −8 sind falsch')
q('G4 (2x + 1)(x − 1) = 2', 2, -1, -3, [-1, F(3, 2)], D=25)
q('G5(a)(i) x² − 16x + 64', 1, -16, 64, [8])
pruef((1 + 2) ** 2 == 1 + 8, 'G5(a)(ii) (x + 2)² = x² + 8: linear, 4x + 4 = 8, x = 1')
q('G5(a)(iii) 3x² + x − 5', 3, 1, -5, D=61)
q('G5(b) x² − 4x − 21', 1, -4, -21, [-3, 7], D=100)
pruef(16 - 84 == -68, 'G5(b): falsche D = −68')
for k, n in ((-1, 2), (0, 1), (2, 0), (4, 1), (5, 2)):
    L, d = loes(1, k, k)
    pruef(len(L) == n and d == k * k - 4 * k, f'G6 k = {k}: {n} Lösungen, D = k(k − 4)')
pruef(loes(1, 0, 0)[0] == [0] and loes(1, 4, 4)[0] == [-2], 'G6: k = 0 → x = 0; k = 4 → x = −2')
pruef(F(0) == F(0, 4), 'G7 k = 0: 4x = 0, x = 0')
for k, n in ((1, 2), (-1, 2), (2, 1), (-2, 1), (3, 0), (-3, 0)):
    L, d = loes(k, 4, k)
    pruef(len(L) == n and d == 16 - 4 * k * k, f'G7 k = {k}: {n} Lösungen, D = 16 − 4k²')
pruef(loes(2, 4, 2)[0] == [-1] and loes(-2, 4, -2)[0] == [1], 'G7: k = 2 → x = −1; k = −2 → x = 1')
print('Simulation Kapitel 5')
q('Sim 5 A k = 1', 1, -2, 1, [1])
q('Sim 5 A k = 0', 1, -2, 0, [0, 2])
q('Sim 5 B k = −0.5', 2, -1, -6, [F(-3, 2), 2])
for k in [x / 2 for x in range(-6, 13)]:
    L, d = loes(1, k, -3)
    pruef(len(L) == 2 and min(L) > -8 and max(L) < 5 and -3 - k * k / 4 > -13, f'Sim 5 B k = {k}: zwei Lösungen im Fenster')
    L, d = loes(1, -2, k)
    pruef(all(-3 < x < 5 for x in L) and k - 1 > -5, f'Sim 5 A k = {k}: im Fenster')
print('Raster (Fehlerwerte)')
pruef(loes(1, -6, 13)[1] == -16, 'G1(b) gleichwertig: D = 36 − 52 = −16')
pruef(loes(1, -1, -30)[1] == 121 and gleich(loes(1, 1, -30)[0], [-6, 5]), 'G2(b): D = 121; Vorzeichenfehler gibt {−6; 5}')
pruef((2 * F(1, 2) + 1) * (F(1, 2) - 1) != 2 and (2 * 3 + 1) * (3 - 1) != 2, 'G4: 0.5 und 3 aus dem Nullprodukt sind falsch')
pruef(loes(2, -1, -1)[1] == 9 and loes(2, 0, -3)[1] == 24, 'G4 Fehler: D = 9 bzw. 24')
pruef(gleich([F(-1 + 5, 4), F(-1 - 5, 4)], [1, F(-3, 2)]), 'G4 −b falsch: {−1.5; 1}')
pruef(round(-3 - math.sqrt(7), 2) == -5.65 and round(-3 + math.sqrt(7), 2) == -0.35, 'G3 gerundet')
pruef(loes(1, 6, -2)[0] != [] and (6 / 2) ** 2 == 9, 'G3: +9')

# ════════════════════════════════════════════════════════════════ Doppelte und Sperrliste
print('Doppelte Normalformen')
ERLAUBT_DOPPELT = {
    (1, -6, 9): 'Themenseiten-Beispiel x² − 6x + 9: Binom im Clip faktorisieren, Fall c = 9 der Familie im Clip formel',
}
for k, orte in ORTE.items():
    if len(orte) > 1 and k not in ERLAUBT_DOPPELT:
        pruef(False, f'Normalform {k} doppelt: {orte}')
js = open(HIER + 'seite.js').read() if os.path.exists(HIER + 'seite.js') else ''
if '--schreiben' in sys.argv and js:
    # Sperrliste in seite.js aus den festen Gleichungen neu schreiben (danach seite.py laufen lassen)
    quad = sorted(set(k for k in QUAD if not (k[1] == 0 and k[2] == 0)))
    zeilen = ['      ' + ', '.join('[%d, %d, %d]' % k for k in quad[i:i + 10]) for i in range(0, len(quad), 10)]
    js = re.sub(r'var FESTE_Q = \[.*?\n    \];', lambda _: 'var FESTE_Q = [\n' + ',\n'.join(zeilen) + '\n    ];', js, count=1, flags=re.S)
    open(HIER + 'seite.js', 'w').write(js)
    print('  FESTE_Q in seite.js neu geschrieben:', len(quad), 'Normalformen')
m = re.search(r'var FESTE_Q = \[(.*?)\];', js, re.S)
if m:
    feste = {schl(tuple(int(x) for x in t.split(','))) for t in re.findall(r'\[(-?\d+,\s*-?\d+,\s*-?\d+)\]', m.group(1))}
    for k in set(QUAD):
        if k[1] == 0 and k[2] == 0:
            continue
        pruef(k in feste, f'FESTE_Q fehlt {k} ({ORTE[k]})')
else:
    print('  (seite.js noch ohne FESTE_Q — Sperrliste nicht geprüft)')

print()
if FEHLER:
    print(len(FEHLER), 'FEHLER')
    sys.exit(1)
print('ALLE ZAHLEN STIMMEN')
