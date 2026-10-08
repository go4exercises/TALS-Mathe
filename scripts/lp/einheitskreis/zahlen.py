"""Rechnet jede Zahl des Leitprogramms Einheitskreis nach (HOWTO-leitprogramme §14, Punkt 1).

  python3 scripts/lp/einheitskreis/zahlen.py

Seite (Vortest, Aufgaben 1a–5d, Festhalten), Clips (Einführung und Kontrollfragen), Simulationsziele,
Gesamttest und Bewertungspaket samt Folgefehler-Fällen. Gerundete Werte werden aus dem exakten Wert neu
gerundet (HOWTO §15). Endet mit «alle Zahlen stimmen» oder einer AssertionError.
"""
from fractions import Fraction as Fr
from math import acos, asin, atan, atan2, cos, degrees, radians, sin, sqrt, tan

S2, S3 = sqrt(2) / 2, sqrt(3) / 2


def c(g):
    return cos(radians(g))


def s(g):
    return sin(radians(g))


def t(g):
    return tan(radians(g))


def r(v, n=3):
    return round(v + 0.0, n)


def gleich(a, b, tol=1e-9):
    assert abs(a - b) < tol, (a, b)


# ---------------------------------------------------------------- Vortest
gleich(Fr(3, 5) ** 2 + Fr(4, 5) ** 2, 1)                       # 0a: 3-4-5-Dreieck
assert r(degrees(asin(0.75)), 1) == 48.6                         # 0b
gleich(sqrt(1 - 0.36), 0.8)                                      # 0d

# ---------------------------------------------------------------- Kapitel 1
assert (r(c(110)), r(s(110))) == (-0.342, 0.94)                  # 1a
assert (r(c(-30)), r(s(-30))) == (0.866, -0.5)
assert (r(c(160)), r(s(160))) == (-0.94, 0.342)                  # 1b
assert c(250) < 0 and s(250) < 0 and c(-20) > 0 and s(-20) < 0   # 1c
assert c(480) < 0 and s(480) > 0
gleich(0.28 ** 2 + 0.96 ** 2, 1)                                 # 1d
assert (r(c(50)), r(s(50))) == (0.643, 0.766)                    # Clip 1
assert (r(c(140)), r(s(140))) == (-0.766, 0.643)
gleich((-0.6) ** 2 + 0.8 ** 2, 1)                                # Kontrollclip 1, F1
assert r(c(135), 4) == -0.7071 and r(s(135), 4) == 0.7071        # F2
assert c(315) > 0 and s(315) < 0                                 # F3 (Auflösungsbild 315°)
assert (r(c(335)), r(s(335))) == (0.906, -0.423)                 # sim1, Zielpunkt (auch −25°, 695°)
gleich(c(-25), c(335)); gleich(s(695), s(335))

# ---------------------------------------------------------------- Kapitel 2
gleich(2 * S2 ** 2, 1)                                           # 45°: x² + x² = 1
gleich(sqrt(1 - 0.25), S3)                                       # 60°
for g, sv, cv in ((30, .5, S3), (45, S2, S2), (60, S3, .5), (150, .5, -S3), (225, -S2, -S2), (300, -S3, .5),
                  (240, -S3, -.5), (330, -.5, S3), (270, -1, 0), (135, S2, -S2), (210, -.5, -S3), (120, S3, -.5), (315, -S2, S2)):
    gleich(s(g), sv); gleich(c(g), cv)
gleich(c(135), -S2); gleich(s(-60), -S3); gleich(c(420), 0.5)    # 2a
gleich(sin(7 * 3.141592653589793 / 6), -0.5); gleich(cos(7 * 3.141592653589793 / 4), S2)   # 2b
gleich(s(45), s(135))

# ---------------------------------------------------------------- Kapitel 3
assert r(t(40)) == 0.839 and r(t(130)) == -1.192                 # Clip 3
assert r(t(80), 2) == 5.67 and r(t(85), 2) == 11.43
gleich(1 - 0.6 ** 2, 0.64); gleich(0.6 / -0.8, -0.75)            # Clip 3: sin 0.6 im II. Q.
assert r(degrees(atan2(0.6, -0.8)), 2) == 143.13
gleich(t(150), -sqrt(3) / 3); gleich(t(300), -sqrt(3))           # 3a
assert Fr(1) - Fr(5, 13) ** 2 == Fr(144, 169)                    # 3b
assert Fr(-12, 13) / Fr(-5, 13) == Fr(12, 5)
assert r(t(100)) == -5.671                                       # 3c
assert r(t(160), 2) == -0.36 and r(t(160)) == -0.364             # 3d
gleich(t(135), -1)                                               # Kontrollclip 3, F1
assert r(t(210)) == 0.577 and r(t(210), 2) == 0.58               # F2
gleich(1 - 0.64, 0.36); gleich(sqrt(0.36), 0.6)                  # F4
assert r(s(45) + c(45), 2) == 1.41                               # F5, Rückmeldung
gleich(t(225), 1); gleich(t(315), -1)                            # sim3-Ziele
assert r(t(40), 2) == 0.84 and r(t(130), 2) == -1.19            # Clip 3: Ton und Bild auf zwei Stellen
gleich(c(225), s(225)); assert s(225) < 0; gleich(c(-135), c(225)); gleich(s(585), s(225))   # sim1, Ziel «cos = sin, unter der x-Achse»
assert r(t(60), 2) == 1.73 and r(t(240), 2) == 1.73

# ---------------------------------------------------------------- Kapitel 4
assert (r(c(25)), r(s(25))) == (0.906, 0.423)                    # Clip 4 («Anwenden»: cos 25° ≈ 0.906 gegeben)
gleich(c(205), -c(25)); gleich(s(155), s(25)); gleich(c(155), -c(25))
gleich(s(65), c(25))
assert (r(s(15)), r(c(15))) == (0.259, 0.966)                    # 4a
gleich(s(165), s(15)); gleich(c(195), -c(15)); gleich(c(-15), c(15))
gleich(s(70), c(20)); gleich(c(10), s(80))                       # 4b
assert r(s(40)) == 0.643 and r(c(40)) == 0.766                   # Kontrollclip 4, F1
gleich(s(140), s(40)); gleich(c(-70), c(70)); gleich(c(20), s(70))
assert r(t(35)) == 0.7; gleich(t(215), t(35))                    # F5
gleich(180 - 70, 110); gleich(180 + 20, 200)                     # sim4-Ziele

# ---------------------------------------------------------------- Kapitel 5
assert r(degrees(asin(0.4)), 1) == 23.6                          # Clip 5
assert r(180 - degrees(asin(0.4)), 1) == 156.4
assert r(degrees(acos(-0.3)), 1) == 107.5
gleich(s(495), S2); gleich(c(-240), -0.5); gleich(t(585), 1)     # 5a
assert r(degrees(asin(-0.8)), 1) == -53.1 and r(degrees(acos(-0.8)), 1) == 143.1   # 5b
assert r(degrees(asin(0.9)), 1) == 64.2 and r(180 - degrees(asin(0.9)), 3) == 115.842   # 5c
assert r(asin(0.5)) == 0.524                                     # Festhalten 5, Häufiger Fehler (RAD)
assert r(acos(-0.5)) == 2.094 and r(degrees(acos(-0.5))) == 120   # 5d (Prüfung 08.10.2026)
gleich(s(210), -0.5); assert r(degrees(asin(-0.5))) == -30; gleich(180 - 210, -30)   # Festhalten 5: Hauptwert aus β = 210°
gleich(c(-45), c(315)); gleich(s(510), s(150))                  # Festhalten 2: volle Runden
gleich(t(330), t(150)); assert r(t(330)) == -0.577               # Kontrollclip 5, F3 (neu)
assert r(degrees(acos(0.6)), 1) == 53.1                          # Kontrollclip 5, F4
gleich(c(400), c(40)); gleich(s(-120), s(240)); gleich(s(-30), s(330))
assert r(degrees(acos(0.5))) == 60                               # sim5-Ziel

# ---------------------------------------------------------------- Gesamttest und Bewertungspaket
assert s(220) < 0 and c(220) < 0 and t(220) > 0                  # G1
assert (r(c(220), 2), r(s(220), 2), r(t(220), 2)) == (-0.77, -0.64, 0.84)
gleich(s(-135), -S2); gleich(c(690), S3); gleich(c(690), c(330)); gleich(t(120), -sqrt(3))      # G2 (Prüfung 08.10.2026)
gleich(cos(-2 * 3.141592653589793 / 3), -0.5); gleich(c(-120), c(240))
assert Fr(1) - Fr(8, 17) ** 2 == Fr(225, 289) and Fr(15, 17) ** 2 == Fr(225, 289)   # G3: sin 8/17, tan < 0 → II. Q.
assert Fr(8, 17) / Fr(-15, 17) == Fr(-8, 15)
gleich(s(180 - degrees(asin(8 / 17))), 8 / 17); assert c(180 - degrees(asin(8 / 17))) < 0
assert -(Fr(1) - Fr(8, 17)) == Fr(-9, 17) and Fr(8, 17) / Fr(-9, 17) == Fr(-8, 9)   # G3, Folgefehler ohne Quadrate
assert r(-15 / 17) == -0.882 and r(-8 / 15) == -0.533
assert (r(s(32)), r(c(32))) == (0.53, 0.848)                     # G4: α = 32°
gleich(s(328), -s(32)); gleich(c(148), -c(32)); gleich(c(58), s(32)); gleich(c(212), -c(32))
assert r(s(328), 4) == -0.5299
assert (r(c(235)), r(s(235))) == (-0.574, -0.819)                # G6
assert (r(cos(235)), r(sin(235))) == (-0.814, 0.581)             # G6, Rechner im Bogenmass
p7 = degrees(atan(-2))
assert r(p7, 1) == -63.4 and r(p7 + 180, 1) == 116.6 and r(p7 + 360, 1) == 296.6   # G7
assert r(180 - r(p7, 1), 1) == 243.4 and r(t(243.4)) == 1.997     # G7, Fehler «Regel des Sinus»: dort ist tan ≈ 2
assert (r(c(p7), 2), r(s(p7), 2)) == (0.45, -0.89)
p8 = degrees(acos(0.7))
assert r(p8, 1) == 45.6 and r(360 - p8, 1) == 314.4 and r(p8 + 360, 1) == 405.6     # G8
assert r(c(180 - r(p8, 1)), 2) == -0.7
assert r(c(-314.4), 2) == 0.7 and r(c(765.6), 2) == 0.7         # G8 (b), andere richtige Winkel
print('alle Zahlen stimmen')
