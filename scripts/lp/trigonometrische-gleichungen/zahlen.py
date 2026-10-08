"""Rechnet jede Zahl des Leitprogramms Trigonometrische Gleichungen nach (HOWTO-leitprogramme §14, Punkt 1).

  python3 scripts/lp/trigonometrische-gleichungen/zahlen.py

Seite (Vortest, Aufgaben 1a–4e, Festhalten), Clips (Einführung und Kontrollfragen), Simulationsziele,
Gesamttest und Bewertungspaket samt Folgefehler-Fällen. Gerundete Werte werden aus dem exakten Wert neu
gerundet (HOWTO §15). Endet mit «alle Zahlen stimmen» oder einer AssertionError.
"""
from math import acos, asin, atan, cos, degrees, radians, sin, sqrt, tan

S2, S3 = sqrt(2) / 2, sqrt(3) / 2


def r1(v):
    return round(v + 1e-12, 1)


def L(f, c):
    """Lösungen in [0°; 360°[, aufsteigend, auf 0.1° gerundet."""
    if f == 'tan':
        t = degrees(atan(c))
        l = [t % 360, (t + 180) % 360]
    else:
        a = degrees(asin(c)) if f == 'sin' else degrees(acos(c))
        l = [a % 360, ((180 - a) if f == 'sin' else (360 - a)) % 360]
    l = sorted(set(round(x, 9) % 360 for x in l))
    return [r1(x) for x in l]


def im(l, p, lo, hi):
    aus = sorted({round(x + k * p, 6) for x in l for k in range(-5, 6) if lo - 1e-9 <= x + k * p < hi - 1e-9})
    return [r1(x) for x in aus]


def ex(f, c):
    return [round(x) for x in L(f, c)]


# ---------------------------------------------------------------- Vortest
assert (round(cos(radians(150)), 6), round(sin(radians(150)), 6)) == (round(-S3, 6), 0.5)        # 0a
assert round(sin(radians(210)), 9) == -0.5 and round(cos(radians(300)), 9) == 0.5                # 0b
assert r1(degrees(asin(0.6))) == 36.9 and r1(degrees(acos(-0.3))) == 107.5                       # 0c
assert r1(degrees(asin(0.6) * 1)) == 36.9 and round(asin(0.6), 3) == 0.644                       # 0c Kommentar RAD
assert abs(sin(radians(400)) - sin(radians(40))) < 1e-12 and abs(cos(radians(-30)) - cos(radians(330))) < 1e-12  # 0e

# ---------------------------------------------------------------- Kapitel 1
assert ex('sin', 0.5) == [30, 150] and ex('cos', -0.5) == [120, 240]                            # Clip, Festhalten
assert L('sin', 0.8) == [53.1, 126.9] and L('cos', -0.3) == [107.5, 252.5]                       # 1a, 1b
assert ex('sin', S3) == [60, 120] and ex('cos', 0) == [90, 270] and ex('cos', -S2) == [135, 225]  # 1c
assert ex('sin', -1) == [270] and ex('sin', 0) == [0, 180] and len(L('cos', -0.999)) == 2         # 1d
assert ex('cos', 1) == [0]                                                                        # 1e
# Kontrollclip 1
r = degrees(asin(-0.4)); assert r1(r) == -23.6 and r1(180 - r) == 203.6                        # F1-Bild
assert abs(0.6 ** 2 + 0.8 ** 2 - 1) < 1e-12                                                       # F2 (0.6 | −0.8)
assert ex('cos', -1) == [180] and ex('sin', S2) == [45, 135]                                      # F3, F4
# Simulation 1: sin −0.5 → 210°, 330°; cos 0 → 90°, 270°; Zielspiel cos 0.5 → 60°, 300°
assert ex('sin', -0.5) == [210, 330] and ex('cos', 0.5) == [60, 300]
assert ex('sin', 0.5) != [60, 300]

# ---------------------------------------------------------------- Kapitel 2
assert L('sin', 0.4) == [23.6, 156.4] and L('cos', -0.7) == [134.4, 225.6]                       # Clip
assert r1(degrees(asin(-0.4))) == -23.6 and L('sin', -0.4) == [203.6, 336.4]                     # Clip, Festhalten
assert L('sin', 0.9) == [64.2, 115.8] and L('cos', -0.45) == [116.7, 243.3]                      # Kontrollclip F1, F2
assert r1(degrees(asin(-0.6))) == -36.9 and L('sin', -0.6) == [216.9, 323.1]                     # F3, F4
assert L('cos', 0.25) == [75.5, 284.5] and r1(180 - degrees(acos(0.25))) == 104.5                # F5 Lena
assert cos(radians(104.5)) < 0
assert L('sin', 0.7) == [44.4, 135.6] and L('cos', -0.2) == [101.5, 258.5]                       # 2a, 2b
assert r1(degrees(asin(-0.45))) == -26.7 and L('sin', -0.45) == [206.7, 333.3]                   # 2c
assert r1(degrees(asin(0.3))) == 17.5 and r1(360 - degrees(asin(0.3))) == 342.5                  # 2d
assert round(sin(radians(342.5)), 2) == -0.3 and r1(180 - degrees(asin(0.3))) == 162.5
# Simulation 2 (Reglerschritt 0.5, Toleranz 0.3)
for f, c, ziel in (('sin', 0.6, 143.13), ('sin', -0.25, 194.48), ('sin', -0.25, 345.52), ('cos', -0.35, 249.51), ('cos', 0.8, 323.13)):
    exakt = [x for x in ([180 - degrees(asin(c)), (degrees(asin(c)) + 360) % 360] if f == 'sin' else [360 - degrees(acos(c))]) if abs(x - ziel) < 0.01]
    assert exakt, (f, c, ziel)
    assert abs(round(ziel * 2) / 2 - exakt[0]) <= 0.3

# ---------------------------------------------------------------- Kapitel 3
assert ex('tan', 1) == [45, 225] and L('tan', 2.5) == [68.2, 248.2] and ex('tan', -1) == [135, 315]   # Clip
assert L('tan', 0.6) == [31.0, 211.0] and r1(degrees(atan(-5))) == -78.7                          # Kontrollclip F1, F3
assert L('tan', 1000) == [89.9, 269.9] and L('tan', -0.6) == [149.0, 329.0]                       # F4, F5
assert L('tan', 1.2) == [50.2, 230.2] and L('tan', -3.2) == [107.4, 287.4]                        # 3a, 3b
assert r1(degrees(atan(-3.2))) == -72.6
assert ex('tan', sqrt(3) / 3) == [30, 210] and ex('tan', 0) == [0, 180]                           # 3c
assert r1(degrees(atan(-0.5))) == -26.6 and L('tan', -0.5) == [153.4, 333.4]                      # 3d
for c, ziel in ((0.5, 206.57), (-1.5, 123.69), (-1.5, 303.69)):                                  # Simulation 3
    t = degrees(atan(c))
    assert min(abs((t + k * 180) - ziel) for k in range(3)) < 0.01 and abs(round(ziel * 2) / 2 - ziel) <= 0.3
assert round(degrees(atan(2)) + 180) == 243                                                       # Sim 3, A6

# ---------------------------------------------------------------- Kapitel 4
assert im([30, 150], 360, 0, 720) == [30, 150, 390, 510] and im([30, 150], 360, -360, 0) == [-330, -210]   # Clip
assert ex('cos', 0.5) == [60, 300] and im([210, 330], 360, 360, 720) == [570, 690]               # Kontrollclip F1, F2
assert im([60, 120], 360, 0, 720) == [60, 120, 420, 480] and im([120, 240], 360, 0, 720) == [120, 240, 480, 600]  # F4, F5
assert L('sin', 0.25) == [14.5, 165.5]                                                           # 4a
assert im([degrees(acos(-0.9)), 360 - degrees(acos(-0.9))], 360, 0, 720) == [154.2, 205.8, 514.2, 565.8]   # 4b
assert im([degrees(atan(0.8))], 180, -180, 360) == [-141.3, 38.7, 218.7]                          # 4c
# Simulation 4: cos −0.8 → 143.1°, 216.9° (k = 1: 503.1°, 576.9°; k = −1: −216.9°, −143.1°); tan −0.7 → −35.0° + k · 180°
c8 = [degrees(acos(-0.8)), 360 - degrees(acos(-0.8))]
assert [r1(x + 360) for x in c8] == [503.1, 576.9] and [r1(x - 360) for x in c8] == [-216.9, -143.1]
t7 = degrees(atan(-0.7)); assert r1(t7) == -35.0 and 0 < t7 + 180 < 180 and 360 < t7 + 540 < 540

# ---------------------------------------------------------------- Gesamttest
assert ex('cos', S3) == [30, 330] and round(S3, 2) == 0.87                                       # G1
assert ex('cos', 1) == [0] and L('tan', -50) == [91.1, 271.1]                                    # G2
assert round(degrees(atan(-sqrt(3)))) == -60 and ex('tan', -sqrt(3)) == [120, 300]               # G3a
assert ex('cos', S2) == [45, 315]                                                                # G3b
assert r1(degrees(asin(-0.35))) == -20.5 and L('sin', -0.35) == [200.5, 339.5]                  # G4
a = degrees(acos(0.42)); assert r1(a) == 65.2 and im([a, 360 - a], 360, 0, 720) == [65.2, 294.8, 425.2, 654.8]   # G5
t = degrees(atan(-2.4)); assert r1(t) == -67.4 and im([t], 180, -180, 180) == [-67.4, 112.6]     # G6
assert r1(degrees(acos(-0.6))) == 126.9 and r1(180 - degrees(acos(-0.6))) == 53.1                # G7 (Tims Fehler)
assert L('cos', -0.6) == [126.9, 233.1] and cos(radians(53.1)) > 0
# Folgefehler-Fälle im Bewertungspaket
assert L('sin', 0.35) == [20.5, 159.5]                                   # G4: Vorzeichen übersehen
assert r1(360 + degrees(asin(-0.35))) == 339.5 and r1(360 - (-20.5)) == 380.5   # G4: 360° − φ₁ gerechnet
assert r1(180 + 20.5) == 200.5                                           # G4: gleichwertiger Weg 180° + |φ₁|
assert r1(180 - a) == 114.8 and r1(180 - a + 360) == 474.8               # G5: Sinusregel, Folgefehler
assert im([t], 360, -180, 180) == [-67.4]                                # G6: Periode 360° → nur eine
assert r1(t + 360) == 292.6                                              # G6: ausserhalb des Intervalls
print('alle Zahlen stimmen')
