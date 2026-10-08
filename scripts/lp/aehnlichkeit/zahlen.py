"""Rechnet alle Zahlen des Leitprogramms Zentrische Streckung und Ähnlichkeit nach (08.10.2026).

  python3 scripts/lp/aehnlichkeit/zahlen.py      # muss ohne AssertionError durchlaufen

Seite (Festhalten, Arbeitsbereiche, Aufgaben 0a–4e), Clips (Einführung und Kontrollfragen) und Gesamttest G1–G7
samt den Fehlerwerten der Raster und Rückmeldungen.
"""
import math

def ok(wert, soll, tol=0.006):
    assert abs(wert - soll) <= tol, (wert, soll)

def bild(Z, P, k):
    return (Z[0] + k * (P[0] - Z[0]), Z[1] + k * (P[1] - Z[1]))

r2 = lambda v: round(v + 1e-12, 2)

# ---------------- Vortest
ok(6 * 4 / 3, 8); ok(5 * 7 / 2, 17.5); ok(180 - 48 - 77, 55); ok(4.5 * 2, 9); ok(math.pi * 9, 28.27); ok(3 * 10000, 30000); ok(450000 / 100, 4500)

# ---------------- Kapitel 1: Z(1|1), A(2|3), B(3|1), C(5|4)
Z1, A, B, C = (1, 1), (2, 3), (3, 1), (5, 4)
assert bild(Z1, C, 1.5) == (7, 5.5)                         # Clip und Festhalten
assert bild(Z1, A, -2) == (-1, -3)                          # Arbeitsbereich A6
assert (-2 * A[0], -2 * A[1]) == (-4, -6) and (-2 * 1, -2 * 2) == (-2, -4)          # Fehler k·A, k·(A − Z)
assert (A[0] - 2 * 1, A[1] - 2 * 2) == (0, -1) and (1 + 2 * 1, 1 + 2 * 2) == (3, 5)  # von A aus; Vorzeichen vergessen
ok(1.5 * math.sqrt(10), 4.74, 0.011); ok(2.25 * math.sqrt(10), 7.11, 0.011); ok(math.sqrt(10) / 1.5, 2.11, 0.011)
# Bild bleibt im Fenster x −7.5 … 10.5, y −5.5 … 9 (k von −2 bis 2)
for k in (-2, -1.5, -1, -0.5, 0.5, 1.5, 2):
    for P in (A, B, C):
        x, y = bild(Z1, P, k); assert -7.5 < x < 10.5 and -5.5 < y < 9
# Aufgaben 1a, 1b, 1d
assert [bild((4, 2), P, -0.5) for P in ((0, 0), (4, 0), (-2, 4))] == [(6, 3), (4, 3), (7, 1)]
assert [bild((-2, 1), P, 2.5) for P in ((0, 2), (3, 0), (1, 4))] == [(3, 3.5), (10.5, -1.5), (5.5, 8.5)]
assert [bild((4, 3), P, -0.5) for P in ((0, 1), (2, 0), (1, 4))] == [(6, 4), (5, 4.5), (5.5, 2.5)]
ok(math.dist((4, 3), (0, 1)), math.sqrt(20)); ok(math.dist((4, 3), (6, 4)), math.sqrt(5))
# Kontrollclip 1
assert bild((-1, 0), (1, 1), -2) == (-5, -2) and bild((-1, 0), (1, 1), 2) == (3, 2) and bild((-1, 0), (1, 1), -1) == (-3, -1)
assert [bild((0, 1), P, 2) for P in ((2, 0), (3, 2), (1.5, 2.5))] == [(4, -1), (6, 3), (3, 4)]
ok(10 / 4, 2.5)
# Falle (6|−2) liegt auf AA′ (A(2|0), A′(4|−1)), nicht auf BB′
assert (6 - 2) * (-1 - 0) - (-2 - 0) * (4 - 2) == 0

# ---------------- Kapitel 2
c = 0.78125; ok(math.sqrt(16 + 9 - 24 * c), 2.5)            # SA = 4, SB = 3, AB = 2.5
ok(3 * 10 / 4, 7.5); ok(7.5 - 3, 4.5); ok(2.5 * 10 / 4, 6.25); ok(2.5 * 6 / 4, 3.75)
assert 4 / 6 != 2.5 / 6.25                                    # SA : AA′ ≠ AB : A′B′
# gekippte Gerade (15°): SB″ ≈ 5.80
th = math.acos(c); v = (math.cos(th), math.sin(th)); u = (3 * v[0] - 4, 3 * v[1]); w = math.radians(15)
u = (u[0] * math.cos(w) - u[1] * math.sin(w), u[0] * math.sin(w) + u[1] * math.cos(w))
det = -u[0] * v[1] + u[1] * v[0]; s = (10 * v[1]) / det; ok(math.hypot(10 + s * u[0], s * u[1]), 5.80, 0.006)
# Arbeitsbereich 2: A5 Umkehrung (k = 2: SB′ = 6), A6–A8
ok(3 * 8 / 4, 6)
ok(math.degrees(math.acos((9 + 6.25 - 4) / 15)), 41.41, 0.01); ok(2 * 7.5 / 3, 5); ok(2 * 4.5 / 3, 3); ok(2 * 3 / 7.5, 0.8)
ok(4 * 8 / 5, 6.4); ok(6.4 - 4, 2.4); ok(4 * 5 / 8, 2.5)
ok((16 + 12.25 - 9) / 28, 0.6875); ok(4.5 * 4 / 6, 3); ok(4.5 * 6 / 4, 6.75)
# Aufgaben 2a–2e
ok(8 * 30 / 10, 24); assert (0 - 24) / (30 - 0) == (-8 - 0) / (40 - 30)       # T, S, R auf einer Geraden
assert abs(6 / 9 - 4 / 6.5) > 0.05; ok(4 * 9 / 6, 6)
ok(4 / 2.4 * 3, 5); ok(6 * 2.4 / 4, 3.6); ok((2.4 ** 2 + 9 - 3.6 ** 2) / (2 * 2.4 * 3), 0.125)
ok(1.8 * 4 / (6 - 1.8), 1.71, 0.006)
# Kontrollclip 2
ok(3 + 6, 9); ok(2 * 9 / 3, 6); ok(2 * 6 / 3, 4); ok(3 * 5 / 2, 7.5); ok(3 * 2 / 5, 1.2); ok(3 * 5 / 2, 7.5)
assert 3 / 4 != 4 * 2 / (3 * 2)                                # «SA : SB = SB′ : SA′» ist falsch (SA = 3, SB = 4, k = 2)

# ---------------- Kapitel 3
ok(4.5 / 3, 1.5); ok(3 / 2, 1.5); ok(2 * (3 + 2), 10); ok(1.5 * 10, 15); ok(1.5 ** 2 * 6, 13.5)
ok(1.5 ** 2, 2.25); ok(2.5 * 200, 500); ok(6.25 * 200 ** 2, 250000); ok(250000 / 10000, 25); ok(math.sqrt(6.25), 2.5)
# Arbeitsbereich 3
ok(math.sqrt(8.64 / 6) * 3, 3.6); ok(3 * 1.44, 4.32); ok(8.64 / 2, 4.32); ok(math.sqrt(8.64), 2.94, 0.006)
ok(0.5 * 10, 5); ok(0.25 * 6, 1.5); ok(0.25 * 10, 2.5); ok(0.5 * 6, 3)
assert all(abs(b * h - 12) > 1e-9 or abs(b / 3 - h / 2) > 1e-9 for b in [x / 2 for x in range(2, 19)] for h in [y / 2 for y in range(2, 13)])
# Aufgaben 3a–3e
ok((40 / 30) ** 2, 1.78, 0.006); ok(30 / 18, 1.67, 0.006); assert 18 / (math.pi * 225) > 30 / (math.pi * 400)
ok(29.7 / 21, 1.414, 0.001); ok(21 / 14.8, 1.419, 0.001); ok(21 * 29.7, 623.7); ok(14.8 * 21, 310.8); ok(623.7 / 310.8, 2.01, 0.006)
ok(8 * 50, 400); ok(6 * 50, 300); ok(48 * 2500, 120000); ok(45 / 20, 2.25); ok(1.5 * 4, 6)
# Kontrollclip 3
assert 4 / 3 != 6 / 4; ok(3 * 12, 36); ok(9 * 12, 108); ok(math.sqrt(16), 4)
ok(5 * 1000 ** 2 / 10000, 500); ok(5 * 1000 / 10000, 0.5); ok(5 * 1000 ** 2 / 100, 50000)
ok(math.dist((8, 0), (8, 4.5)), 4.5); ok(math.dist((8, 0), (5, 0)), 3)

# ---------------- Kapitel 4
s50, s70, s60 = (math.sin(math.radians(w)) for w in (50, 70, 60))
a4, b4 = 4 * s50 / s60, 4 * s70 / s60; ok(a4, 3.54, 0.006); ok(b4, 4.34, 0.006)
ok(1.5 * a4, 5.31, 0.006)                                       # Clip «Rechnen»
ok(6 / 4.34 * 4, 5.53, 0.011); ok(1.5 * 3.54, 5.31, 0.011); ok(6 / 4.34 * 3.54, 4.89, 0.011); ok(4 / (6 / 4.34), 2.89, 0.011)
ok(6 * s60 / s70, 5.53, 0.006)                                  # B′C′ direkt aus den Winkeln
ok(6 / 4, 1.5); ok(7.5 / 5, 1.5); ok(9 / 6, 1.5); ok(8 / 6, 1.33, 0.006)
ok(7.80 * 1.80 / 1.20, 11.70); ok(math.sqrt(1.8 * 3.2), 2.4); ok(math.sqrt(1.8 * 5), 3); ok(math.sqrt(3.2 * 5), 4)
# Aufgaben 4a–4e
ok(9 / 6 * 4, 6); ok(9 / 6 * 5, 7.5)
ok(math.degrees(math.acos(0.5625)), 55.77, 0.006); ok(math.degrees(math.acos(0.75)), 41.41, 0.006)
ok(7.5 / 5, 1.5); ok(10.5 / 7, 1.5); ok(12 / 8, 1.5); ok(13 / 8, 1.625)
ok(36.8 * 1.65 / 2.2, 27.6); ok(math.sqrt(5 * 7.2), 6); ok(math.sqrt(5 * 12.2), 7.81, 0.006); ok(math.sqrt(7.2 * 12.2), 9.37, 0.006)
ok(61 + 87.84, 12.2 ** 2)
# Kontrollclip 4
ok(180 - 40 - 75, 65); ok(8 / 4, 2); ok(12 / 6, 2); ok(15 / 7, 2.14, 0.006); ok(12 * 2 / 1.6, 15); ok(12 * 1.6 / 2, 9.6)
ok(math.sqrt(4 * 9), 6); ok((4 + 9) / 2, 6.5)

# ---------------- Gesamttest
assert bild((2, -1), (4, 0), -1.5) == (-1, -2.5) and bild((2, -1), (6, 3), -1.5) == (-4, -7) and bild((2, -1), (3, 2), -1.5) == (0.5, -5.5)
ok(1.5 * math.sqrt(13), 5.41, 0.006); ok(2.25 * math.sqrt(13), 8.11, 0.006)
assert bild((2, -1), (4, 0), 1.5) == (5, 0.5) and bild((2, -1), (6, 3), 1.5) == (8, 5)
ok(3 * 3.5 / 2.5, 4.2); ok(2 * 6 / 2.5, 4.8); ok(2 * 3.5 / 2.5, 2.8); ok(3 * 2.5 / 3.5, 2.14, 0.006); ok(2 * 2.5 / 6, 0.83, 0.006)
ok(math.degrees(math.acos((6.25 + 9 - 4) / 15)), 41.41, 0.006)
ok(1.8 * 0.15 / 6, 0.045); ok(1.8 * 0.15 / 0.03, 9)
ok(18.4 * 25000 / 100000, 4.6); ok(3.2 * 25000 ** 2 / 1e10, 0.2); ok(3.2 / 4, 0.8); ok(3.2 * 25000 / 10000, 8)
ok(1.6 * math.sqrt(3), 2.77, 0.006)
# G6 (neu 08.10.2026): DEF mit D = 41°, E = 76°, DE = 8; XYZ mit X = 63°, Z = 41°, YZ = 6
sd = lambda w: math.sin(math.radians(w))
assert 180 - 41 - 76 == 63 and 180 - 63 - 41 == 76
EF, FD = 8 * sd(41) / sd(63), 8 * sd(76) / sd(63)
ok(EF, 5.89, 0.006); ok(FD, 8.71, 0.006)
ok(6 / 8, 0.75); ok(0.75 * EF, 4.42, 0.006); ok(0.75 * 5.89, 4.42, 0.006)        # XY ↔ EF (beide 41° gegenüber)
ok(8 * 6 / 5.89, 8.15, 0.006); ok(8 * 6 / EF, 8.15, 0.006)                       # Laras Zuordnung nach Buchstaben
ok(5.89 * 8 / 6, 7.85, 0.006); ok(0.75 * 8.71, 6.53, 0.006); ok(0.75 * FD, 6.53, 0.006)   # verkehrt; FD statt EF
# G3 (4 P): Ansatz b : 1.8 = 0.15 : 6; gemischte Einheiten 1.8 · 15 / 6 = 4.5 (als Meter), 1.8 · 0.15 / 3 = 0.09, verkehrt 72
ok(1.8 * 15 / 6, 4.5); ok(1.8 * 0.15 / 3, 0.09); ok(1.8 * 6 / 0.15, 72)
# G4: Umrechnungen in den typischen Fehlern
ok(3.2 * 25000 ** 2, 2e9); ok(2e9 / 1e4, 200000); ok(18.4 * 25000, 460000); ok(460000 / 100, 4600); ok(3.2 / 2, 1.6); ok(0.2e10 / 50000 ** 2, 0.8)
ok(7.5 ** 2 / 12.5, 4.5); ok(12.5 - 4.5, 8); ok(math.sqrt(4.5 * 8), 6); ok(math.sqrt(7.5 ** 2 - 4.5 ** 2), 6)
ok(math.sqrt(0.6 * 11.9), 2.67, 0.006)
# ---------------- Behebung 08.10.2026: neue und geänderte Zahlen
# Clip strahlensaetze «Nur mit Parallelen»: 3 : 5.80 ≈ 0.52 ≠ 0.4 = 4 : 10
ok(3 / 5.8004, 0.52, 0.006); ok(4 / 10, 0.4)
# Kontrollclip 2 F3 (umgekehrt): SA = 2, SA′ = 5, SB′ = 7.5 → SB = 7.5 · 2 / 5 = 3; Falle 4.5 (BB′ = AA′ = 3)
ok(7.5 * 2 / 5, 3); ok(7.5 - 3, 4.5); ok(7.5 - 4.5, 5 - 2)
u50 = (math.cos(math.radians(50)), math.sin(math.radians(50)))
ok(3 * u50[0], 1.928, 0.001); ok(3 * u50[1], 2.298, 0.001); ok(4.5 * u50[0], 2.893, 0.001); ok(7.5 * u50[0], 4.821, 0.001)
# Clip figuren: «Fläche» schrumpft von 6 × 4 (k = 2) auf 4.5 × 3 (k = 1.5); «Zurück zu k»: 3 × 2 → 7.5 × 5 (k = 2.5)
ok(4.5 * 3, 13.5); ok(7.5 / 3, 2.5); ok(5 / 2, 2.5); ok(7.5 * 5 / 6, 6.25)
# Clip dreiecke «Schatten»: Stummel des Sonnenstrahls hat die Steigung 11.7 / 7.8 = 1.5
ok(11.7 / 7.8, 1.5)
# Kontrollclip 4: F1 38° + 77° → 65°, 77° + 65° → 38°; F4 Schatten s = 15 · 1.6 / 2 = 12, verkehrt 18.75, Unterschied 14.6
assert 180 - 38 - 77 == 65 and 180 - 77 - 65 == 38
ok(15 * 1.6 / 2, 12); ok(15 * 2 / 1.6, 18.75); ok(15 - (2 - 1.6), 14.6)
# Aufgabe 2f: Lampe – Karte 30 cm – Wand 120 cm, Karte 12 cm (Figur: Karte 4 … 16, Schatten 16 … 64)
ok(120 / 30, 4); ok(4 * 12, 48); ok(4 * 4, 16); ok(4 * 16, 64); ok(64 - 16, 48)
# Aufgabe 3c: Plan 8 × 6 im Karo (Massstab 1 : 50) wie bisher
# Aufgabe 4f: AB = 8, AC = 6, BC = 7, AD = 3, AE = 4 → ADE ~ ACB (sWs), k = 0.5, DE = 3.5; AD : AB ≠ AE : AC
ca = (64 + 36 - 49) / 96; ok(ca, 51 / 96); C4f = (6 * ca, 6 * math.sqrt(1 - ca * ca)); E4f = (4 * ca, 4 * math.sqrt(1 - ca * ca))
ok(C4f[0], 3.1875, 0.0001); ok(C4f[1], 5.0833, 0.0001); ok(E4f[0], 2.125, 0.0001); ok(E4f[1], 3.3889, 0.0001)
ok(3 / 6, 4 / 8); ok(0.5 * 7, 3.5); ok(math.dist((3, 0), E4f), 3.5, 1e-9); ok(math.dist((8, 0), C4f), 7, 1e-9); assert abs(3 / 8 - 4 / 6) > 0.1
# Festhalten 3: √2 ≈ 1.41, √3 ≈ 1.73; Übung «flaeche», k aus Flächenverhältnis 2, 3, 5, 6, 8, 10
ok(math.sqrt(2), 1.41, 0.006); ok(math.sqrt(3), 1.73, 0.006)
for q2 in (2, 3, 5, 6, 8, 10):
    assert abs(math.sqrt(q2) - q2 / 2) > 0.07 or q2 == 4      # «halb» bleibt eine eigene Diagnose
# Figurenfenster: 4a 260 × 135 px über x −1 … 17 (unten −1 vor, −1.3 nach der Bildmessung) → oben 8.35 bzw. 8.05 > R (6.585)
ok(-1 + 135 * 18 / 260, 8.35, 0.01); assert -1 + 135 * 18 / 260 - 6.585 > 1.2
# 4d 230 × 150 px über x −1.2 … 13.4 → oben y = −1.7 + 150 · 14.6 / 230 = 7.82 > C (6)
ok(-1.7 + 150 * 14.6 / 230, 7.82, 0.01)
# 4f 220 × 165 px über x −1 … 9 → oben y = −1.2 + 165 · 10 / 220 = 6.3 > C (5.08); 2f 240 × 165 über −10 … 132, unten −25 → oben 72.6 > Wand (70);
# 4a mit unten −1.3 → oben 8.05
ok(-1.2 + 165 * 10 / 220, 6.3); ok(-25 + 165 * 142 / 240, 72.63, 0.01); ok(-1.3 + 135 * 18 / 260, 8.05, 0.01)

# Punkte und Minuten
assert sum([3, 4, 4, 4, 3, 4, 3]) == 25                       # G1 3 (nur P′), G3 4 (Ansatz dazu), G6 4 (neu)
assert sum([3, 3, 2, 3, 2, 2]) == 15 and sum([3, 3, 3, 3, 2, 2]) == 16          # Kapitel 2 (mit 2f), Kapitel 4 (mit 4f)
assert 10 + 40 + 50 + 40 + 50 + 30 == 220
print('alle Zahlen stimmen')
