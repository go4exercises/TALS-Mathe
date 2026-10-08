"""Alle Zahlen des Leitprogramms Kreis und Kreisteile, mit python3 nachgerechnet (08.10.2026).

  python3 scripts/lp/kreis-kreisteile/zahlen.py

Jede Zahl, die in Seite, Arbeitsbereich, Clips, Gesamttest oder Bewertungspaket steht, steht hier mit ihrem
gerundeten Wert (zwei Dezimalen, wo nichts anderes steht). Das Skript rechnet sie aus den Angaben neu und
bricht ab, wenn ein eingetragener Wert nicht stimmt. Typische Fehlwerte (für Rückmeldungen und das Raster)
stehen mit dabei, ebenso die Prüfung, dass kein Fehlwert zufällig gleich dem Sollwert ist.
"""
from math import pi, sqrt, isclose, cos, radians

FEHLER = []


def r2(v, st=2):
    f = 10 ** st
    return round(v * f + (1e-9 if v >= 0 else -1e-9)) / f


def soll(name, wert, eingetragen, st=2):
    if r2(wert, st) != eingetragen:
        FEHLER.append('%s: gerechnet %.6f → %s, eingetragen %s' % (name, wert, r2(wert, st), eingetragen))
    return wert


def verschieden(name, sollwert, *fehlwerte):
    """Kein typischer Fehlwert darf auf zwei Dezimalen gleich dem Sollwert sein (sonst gilt der Fehler als richtig)."""
    for f in fehlwerte:
        if abs(r2(f) - r2(sollwert)) < 0.015:
            FEHLER.append('%s: Fehlwert %.4f fällt mit dem Sollwert %.4f zusammen' % (name, f, sollwert))


def sehne(r, a):
    return 2 * sqrt(r * r - a * a)


def abstand(r, s):
    return sqrt(r * r - (s / 2) ** 2)


def tangente(r, mp):
    return sqrt(mp * mp - r * r)


def U(r):
    return 2 * pi * r


def A(r):
    return pi * r * r


def bogen(r, phi):
    return phi / 360 * 2 * pi * r


def sektor(r, phi):
    return phi / 360 * pi * r * r


def dreieck(r, phi):
    """Dreieck M P1 P2 ohne Trigonometrie: 90° (270°) rechtwinklig, 60° (300°) gleichseitig, 180° ohne Fläche."""
    if phi in (90, 270):
        return r * r / 2
    if phi in (60, 300):
        return r / 2 * sqrt(r * r - (r / 2) ** 2)
    if phi == 180:
        return 0
    raise ValueError(phi)


def segment(r, phi):
    return sektor(r, phi) - dreieck(r, phi) if phi <= 180 else sektor(r, phi) + dreieck(r, phi)


def ring(R, r):
    return pi * (R * R - r * r)


# ════════════════════════════════ Kapitel 1 · Linien am Kreis
soll('Clip 1: Sehne r = 5, a = 3', sehne(5, 3), 8)
soll('Clip 1: Tangente r = 5, MP = 13', tangente(5, 13), 12)
soll('AB1 A6: Sehne r = 6, a = 2.5', sehne(6, 2.5), 10.91)
verschieden('AB1 A6', sehne(6, 2.5), sehne(6, 2.5) / 2, 2 * sqrt(36 + 6.25), 2 * (6 - 2.5), sqrt(36 + 6.25))
soll('AB1 A7: Abstand r = 6, s = 8', abstand(6, 8), 4.47)
verschieden('AB1 A7', abstand(6, 8), sqrt(36 + 16), 6 - 4, sqrt(64 - 36))
soll('AB1 A8: Tangente r = 4, MP = 8.5', tangente(4, 8.5), 7.5)
verschieden('AB1 A8', tangente(4, 8.5), sqrt(8.5 ** 2 + 16), 8.5 - 4)
soll('AB1 A8 Fehler +', sqrt(8.5 ** 2 + 16), 9.39)
soll('AB1 A7 Fehler +', sqrt(36 + 16), 7.21)
soll('AB1 A7 Fehler s statt s/2', sqrt(64 - 36), 5.29)
soll('AB1 A6 Fehler +', 2 * sqrt(36 + 6.25), 13)
soll('AB1 A6 halbe', sehne(6, 2.5) / 2, 5.45)
soll('Aufgabe 1b: Abstand r = 6.5, s = 12', abstand(6.5, 12), 2.5)
soll('Aufgabe 1b: Pfeilhöhe', 6.5 - abstand(6.5, 12), 4)
soll('Aufgabe 1c: Tangente MP = 13, r = 5 — schon im Clip; hier MP = 10, r = 6', tangente(6, 10), 8)
soll('Aufgabe 1c: Abstand P zur Kreislinie', 10 - 6, 4)
soll('Kontrolle 1 F4: Sehne r = 10, a = 6', sehne(10, 6), 16)
soll('Kontrolle 1 F4 Fehler +', 2 * sqrt(100 + 36), 23.32)
soll('Kontrolle 1 F5: Tangente MP = 17, r = 8', tangente(8, 17), 15)
soll('Kontrolle 1 F5 Fehler +', sqrt(17 ** 2 + 64), 18.79)

# ════════════════════════════════ Kapitel 2 · Umfang, Fläche und π
soll('Clip 3: U r = 3', U(3), 18.85)
soll('Clip 3: A r = 3', A(3), 28.27)
soll('Clip 3: r aus U = 40', 40 / (2 * pi), 6.37)
soll('Clip 3: r aus A = 50', sqrt(50 / pi), 3.99)
soll('AB2 A4: U r = 3.5', U(3.5), 21.99)
soll('AB2 A4: A r = 3.5', A(3.5), 38.48)
soll('AB2 A4 Fehler pi r', pi * 3.5, 11.0)
soll('AB2 A4 Fehler pi d^2', pi * 49, 153.94)
soll('AB2 A5: r aus U = 30', 30 / (2 * pi), 4.77)
soll('AB2 A5 Fehler d', 30 / pi, 9.55)
soll('AB2 A5 Fehler Wurzel', sqrt(30 / pi), 3.09)
soll('AB2 A6: r aus A = 80', sqrt(80 / pi), 5.05)
soll('AB2 A6 Fehler ohne Wurzel', 80 / pi, 25.46)
soll('AB2 A6 Fehler 2 pi', 80 / (2 * pi), 12.73)
soll('Aufgabe 2a: U d = 26', pi * 26, 81.68)
soll('Aufgabe 2a: A d = 26', A(13), 530.93)
soll('Aufgabe 2b: d aus U = 200 cm', 200 / pi, 63.66)
soll('Aufgabe 2b: Querschnitt', A(100 / pi), 3183.10)
soll('Aufgabe 2c: r aus A = 1.5 m²', sqrt(1.5 / pi), 0.69)
soll('Aufgabe 2c: d', 2 * sqrt(1.5 / pi), 1.38)
soll('Aufgabe 2c: U', U(sqrt(1.5 / pi)), 4.34)
soll('Aufgabe 2c: je Person', U(sqrt(1.5 / pi)) / 6, 0.72)
soll('Kontrolle 2 F2: U d = 8', pi * 8, 25.13)
soll('Kontrolle 2 F2 Fehler 2 pi d', 2 * pi * 8, 50.27)
soll('Kontrolle 2 F2 Fehler pi r', pi * 4, 12.57)
soll('Kontrolle 2 F3: A r = 6', A(6), 113.10)
soll('Kontrolle 2 F3 Fehler U', U(6), 37.70)
soll('Kontrolle 2 F3 Fehler d', A(12), 452.39)
soll('Kontrolle 2 F5: r aus U = 50', 50 / (2 * pi), 7.96)
soll('Kontrolle 2 F5 Fehler d', 50 / pi, 15.92)
soll('Kontrolle 2 F5 Fehler Wurzel', sqrt(50 / pi), 3.99)

# ════════════════════════════════ Kapitel 3 · Bogen und Sektor
soll('Clip 5: b r = 4, φ = 45', bogen(4, 45), 3.14)
soll('Clip 5: A r = 4, φ = 45', sektor(4, 45), 6.28)
soll('Clip 5: ½ b r', bogen(4, 45) * 4 / 2, 6.28)
soll('Clip 5: φ aus b = 6, r = 4', 6 / U(4) * 360, 85.94)
soll('AB3 A5: b r = 4.5, φ = 100', bogen(4.5, 100), 7.85)
soll('AB3 A5 Fehler U', U(4.5), 28.27)
soll('AB3 A5 Fehler Fläche', sektor(4.5, 100), 17.67)
soll('AB3 A5 Fehler ohne 2', 100 / 360 * pi * 4.5, 3.93)
soll('AB3 A6: A r = 3.5, φ = 150', sektor(3.5, 150), 16.04)
soll('AB3 A6 Fehler Kreis', A(3.5), 38.48)
soll('AB3 A6 Fehler Bogen', bogen(3.5, 150), 9.16)
soll('AB3 A7: φ aus A = 20, r = 4.5', 20 / A(4.5) * 360, 113.18)
soll('AB3 A7 Fehler Anteil', 20 / A(4.5), 0.31)
soll('AB3 A7 Fehler Prozent', 20 / A(4.5) * 100, 31.44)
soll('AB3 A7 Fehler mit 2 pi r', 20 / U(4.5) * 360, 254.65)
soll('AB3 A8: Sektorumfang r = 5, φ = 90', bogen(5, 90) + 10, 17.85)
soll('AB3 A8 Fehler nur Bogen', bogen(5, 90), 7.85)
soll('AB3 A8 Fehler ein Radius', bogen(5, 90) + 5, 12.85)
soll('Aufgabe 3a: Bogen r = 9, 120°', bogen(9, 120), 18.85)
soll('Aufgabe 3a: Fläche', sektor(9, 120), 84.82)
soll('Aufgabe 3b: φ aus b = 10, r = 6', 10 / U(6) * 360, 95.49)
soll('Aufgabe 3b: A = ½ b r', 10 * 6 / 2, 30)
soll('Aufgabe 3d: falsch (Umfangformel)', bogen(7, 50), 6.11)
soll('Aufgabe 3d: richtig', sektor(7, 50), 21.38)
soll('Kontrolle 3 F2: b r = 10, φ = 54', bogen(10, 54), 9.42)
soll('Kontrolle 3 F2 Fehler Fläche', sektor(10, 54), 47.12)
soll('Kontrolle 3 F2 Fehler U', U(10), 62.83)
soll('Kontrolle 3 F3: ½ b r, b = 8, r = 5', 8 * 5 / 2, 20)
soll('Kontrolle 3 F5: Rand r = 9, φ = 20', bogen(9, 20) + 18, 21.14)
soll('Kontrolle 3 F5 Fehler', bogen(9, 20), 3.14)
soll('Kontrolle 3 F5 Fehler ein Radius', bogen(9, 20) + 9, 12.14)

# ════════════════════════════════ Kapitel 4 · Segment und Kreisring
soll('Clip 7: Sektor r = 5, 90°', sektor(5, 90), 19.63)
soll('Clip 7: Segment r = 5, 90°', segment(5, 90), 7.13)
soll('Clip 7: Höhe 60°, r = 5', sqrt(25 - 6.25), 4.33)
soll('Clip 7: Sektor r = 5, 60°', sektor(5, 60), 13.09)
soll('Clip 7: Dreieck r = 5, 60°', dreieck(5, 60), 10.83)
soll('Clip 7: Segment r = 5, 60°', segment(5, 60), 2.26)
soll('Clip 7: Ring R = 6, r = 4', ring(6, 4), 62.83)
soll('Clip 7: 2 pi r_m b', 2 * pi * 5 * 2, 62.83)
soll('AB4 A4: Segment r = 3.5, 90°', segment(3.5, 90), 3.50)
soll('AB4 A4 Fehler Sektor', sektor(3.5, 90), 9.62)
soll('AB4 A4 Fehler plus', sektor(3.5, 90) + dreieck(3.5, 90), 15.75)
soll('AB4 A4 Fehler Dreieck', dreieck(3.5, 90), 6.13)
soll('AB4 A4 Fehler ohne ½', sektor(3.5, 90) - 3.5 ** 2, -2.63)
soll('AB4 A5: Segment r = 4.5, 60°', segment(4.5, 60), 1.83)
soll('AB4 A5 Höhe', sqrt(4.5 ** 2 - 2.25 ** 2), 3.90)
soll('AB4 A5 Dreieck', dreieck(4.5, 60), 8.77)
soll('AB4 A5 Fehler Sektor', sektor(4.5, 60), 10.60)
soll('AB4 A5 Fehler rechtwinklig', sektor(4.5, 60) - 4.5 ** 2 / 2, 0.48)
soll('AB4 A5 Fehler plus', sektor(4.5, 60) + dreieck(4.5, 60), 19.37)
soll('AB4 A6: Segment r = 4, 270°', segment(4, 270), 45.70)
soll('AB4 A6 Fehler minus', sektor(4, 270) - 8, 29.70)
soll('AB4 A6 Fehler Sektor', sektor(4, 270), 37.70)
soll('AB5 A4: Ring R = 5.5, r = 2.5', ring(5.5, 2.5), 75.40)
soll('AB5 A4 Fehler (R − r)²', pi * 3 ** 2, 28.27)
soll('AB5 A4 Fehler plus', pi * (5.5 ** 2 + 2.5 ** 2), 114.67)
soll('AB5 A4 Fehler R statt r_m', 2 * pi * 5.5 * 3, 103.67)
soll('AB5 A5: Ring b = 2, r_m = 4.5', 2 * pi * 4.5 * 2, 56.55)
soll('AB5 A5 Kontrolle über R, r', ring(5.5, 3.5), 56.55)
soll('AB5 A5 Fehler ohne b', 2 * pi * 4.5, 28.27)
soll('AB5 A5 Fehler pi b²', pi * 4, 12.57)
soll('Aufgabe 4a: Fenster Fläche', 1.2 * 1.5 + A(0.6) / 2, 2.37)
soll('Aufgabe 4a: Fenster Umfang', 1.2 + 2 * 1.5 + pi * 0.6, 6.08)
soll('Aufgabe 4b: Tisch 300°', segment(0.6, 300), 1.10)
soll('Aufgabe 4b: Tisch über Kreis − Segment', A(0.6) - segment(0.6, 60), 1.10)
soll('Aufgabe 4b: kleines Segment', segment(0.6, 60), 0.03)
soll('Aufgabe 4c: CD', ring(5.8, 2.3), 89.06)
soll('Aufgabe 4c: 2 pi r_m b', 2 * pi * 4.05 * 3.5, 89.06)
soll('Kontrolle 4 F2: Dreieck r = 10, 90°', dreieck(10, 90), 50)
soll('Kontrolle 4 F4: Ring R = 7, r = 3', ring(7, 3), 125.66)
soll('Kontrolle 4 F4 Fehler (R − r)²', pi * 16, 50.27)
soll('Kontrolle 4 F4 Fehler pi (R − r)', pi * 4, 12.57)

# ════════════════════════════════ Vorwissen
soll('0a Hypotenuse 5, 12', sqrt(25 + 144), 13)
soll('0a Kathete 10, 6', sqrt(100 - 36), 8)
soll('0b gleichseitig 8: Höhe', sqrt(64 - 16), 6.93)
soll('0b gleichseitig 8: Fläche', 8 * sqrt(48) / 2, 27.71)
soll('0d x² = 20', sqrt(20), 4.47)

# ════════════════════════════════ Gesamttest
soll('G1: r = 4 (d = 8), a = 2.5: Sehne', sehne(4, 2.5), 6.24)
soll('G1 Fehler r = 8', sehne(8, 2.5), 15.20)
soll('G2: Horizont 50 m', tangente(6371, 6371.05), 25.24)
soll('G3: r aus U = 25', 25 / (2 * pi), 3.98)
soll('G3: A Teich', A(25 / (2 * pi)), 49.74)
soll('G3: A mit r = 3.98', A(3.98), 49.76)
soll('G3: Weg (Ring b = 1.5)', ring(25 / (2 * pi) + 1.5, 25 / (2 * pi)), 44.57)
soll('G3: Weg über 2 pi r_m b', 2 * pi * (25 / (2 * pi) + 0.75) * 1.5, 44.57)
soll('G3: Weg mit gerundetem r', ring(5.48, 3.98), 44.58)
soll('G3 Fehler pi b²', pi * 1.5 ** 2, 7.07)
soll('G3 Fehler d statt r', ring(25 / pi + 1.5, 25 / pi), 82.07)
soll('G4: φ aus A = 50, r = 7.5', 50 / A(7.5) * 360, 101.86)
soll('G4: b = 2A / r', 2 * 50 / 7.5, 13.33)
soll('G4: b über φ', bogen(7.5, 50 / A(7.5) * 360), 13.33)
soll('G4: Sektorumfang', 2 * 50 / 7.5 + 15, 28.33)
soll('G4 Fehler φ mit 2 pi r', 50 / U(7.5) * 360, 381.97)
soll('G7: Laufbahn U', 200 + pi * 64, 401.06)
soll('G7: Feld A', 6400 + A(32), 9616.99)
soll('G7 Fehler pi d²', 6400 + pi * 64 ** 2, 19267.96)
soll('G7 Fehler ein Halbkreis', 200 + pi * 32, 300.53)
soll('G7 Fehler nur ein Halbkreis Fläche', 6400 + A(32) / 2, 8008.50)

soll('G2 Fehler 50 m nicht umgerechnet', tangente(6371, 6421), 799.75)
soll('G2 Fehler plus', sqrt(6371.05 ** 2 + 6371 ** 2), 9009.99)
soll('G3 Fehler d als r: Fläche', A(25 / pi), 198.94)
soll('G5: r', sqrt(50), 7.07)
soll('G5: Sektor 90°', sektor(sqrt(50), 90), 39.27)
soll('G5: Segment', segment(sqrt(50), 90), 14.27)
soll('G5 Fehler plus', sektor(sqrt(50), 90) + 25, 64.27)
soll('G5 Fehler r = 5: Sektor', sektor(5, 90), 19.63)
soll('G7 Fehler Schmalseiten mitgezählt', 200 + 128 + pi * 64, 529.06)
soll('G7 Fehler π = 3.14: Rand', 200 + 3.14 * 64, 400.96)
soll('G7 Fehler π = 3.14: Fläche', 6400 + 3.14 * 1024, 9615.36)
soll('G1 Fehler r = 8', sehne(8, 2.5), 15.20)
soll('G1 halbe Sehne', sehne(4, 2.5) / 2, 3.12)
soll('G4 Anteil', 50 / A(7.5), 0.28)
soll('G4 Rand mit einem Radius', 2 * 50 / 7.5 + 7.5, 20.83)
soll('G3 r_m', 25 / (2 * pi) + 0.75, 4.73)
soll('Aufgabe 2b: Querschnitt mit gerundetem r', A(31.83), 3182.90)
soll('Aufgabe 2b: r', 100 / pi, 31.83)
soll('Aufgabe 3e: d', 63 / pi, 20.05)
soll('Aufgabe 4a: Rechteck + Halbkreis (Teile)', A(0.6) / 2, 0.57)
soll('Aufgabe 4b: Sektor 300°', sektor(0.6, 300), 0.9425, 4)
soll('Aufgabe 4b: Dreieck', dreieck(0.6, 60), 0.1559, 4)
soll('Aufgabe 4b: Höhe', sqrt(0.36 - 0.09), 0.520, 3)
soll('Aufgabe 4b: kleines Segment', segment(0.6, 60), 0.0326, 4)
soll('Aufgabe 4b: Sektor 60°', sektor(0.6, 60), 0.1885, 4)
soll('Aufgabe 3b: Probe', sektor(6, 10 / U(6) * 360), 30)
soll('Kontrolle 4 F3: Höhe s = 8', sqrt(64 - 16), 6.93)
soll('Kontrolle 4 F3 Fehler plus', sqrt(64 + 16), 8.94)
soll('Kontrolle 4 F2 Fehler Sektor', sektor(10, 90), 78.54)
soll('Kontrolle 3 F3 Zeichnung: φ', 8 / U(5) * 360, 91.67)
soll('Clip 1 Kontrolle F1: Sehne von 60° bis 160°, Abstand zu M', 5 * cos(radians(50)), 3.21)
soll('AB2 A4 Fehler π = 3: U', 2 * 3 * 3.5, 21)
soll('AB2 A4 Fehler π = 3: A', 3 * 3.5 ** 2, 36.75)
soll('AB2 A5 Fehler π = 3', 30 / 6, 5)
soll('AB2 A6 Fehler d', 2 * sqrt(80 / pi), 10.09)
soll('AB3 A5 Fehler r·φ', 4.5 * 100, 450)
soll('AB3 A8 Fehler Kreisumfang', U(5), 31.42)
soll('AB5 A4 r_m', (5.5 + 2.5) / 2, 4)
soll('Clip 7 Tangente B: Winkel', __import__('math').degrees(__import__('math').acos(5 / 13)), 67.38)
soll('Kontrolle 1 F5 B: Winkel', __import__('math').degrees(__import__('math').acos(8 / 17)), 61.93)

# ════════════════════════════════ Behebung nach der Prüfung (08.10.2026)
soll('Aufgabe 1f: r aus s = 9, a = 6', sqrt(4.5 ** 2 + 6 ** 2), 7.5)
verschieden('Aufgabe 1f', sqrt(4.5 ** 2 + 36), sqrt(81 + 36), 4.5 + 6, sqrt(36 - 4.5 ** 2))
soll('Aufgabe 1g: MP = 1.2 + 0.3 m', 1.2 + 0.3, 1.5)
soll('Aufgabe 1g: PB', tangente(1.2, 1.5), 0.9)
soll('Aufgabe 2f: Dose', 22.9 / 7.3, 3.14)
soll('Aufgabe 2f: Velorad', 207.5 / 66, 3.14)
soll('Aufgabe 2f: Münze', 7.2 / 2.3, 3.13)
soll('Aufgabe 3e: Stücke', 360 / 40, 9)
soll('G5 (d): grosses Segment 270°', segment(sqrt(50), 270), 142.81)
soll('G5 (d): Kreis − kleines Segment', A(sqrt(50)) - segment(sqrt(50), 90), 142.81)
soll('G5 (d) Fehler minus Dreieck', sektor(sqrt(50), 270) - 25, 92.81)
soll('G5 (d) Fehler nur Sektor', sektor(sqrt(50), 270), 117.81)
soll('G5 Fehler ganze Sehne als Kathete: r', sqrt(125), 11.18)
soll('G5 Fehler ganze Sehne als Kathete: Sektor', sektor(sqrt(125), 90), 98.17)
soll('G6: Faktor', (2 * 2 ** 2), 8)
# Übung sehne, Art h (P liegt h ausserhalb): √(r² + h²) ist bei r = 2h zufällig richtig — darum nicht gewürfelt
assert isclose(sqrt(4 ** 2 + 2 ** 2), tangente(4, 6)), 'r = 2h'
for r_ in (4, 5, 6, 6.5, 7.5, 8, 9, 10, 12):
    for h_ in (0.5, 1, 1.5, 2, 2.5, 3, 4, 5):
        if isclose(r_, 2 * h_):
            continue
        verschieden('Übung sehne h r=%s h=%s' % (r_, h_), tangente(r_, r_ + h_), sqrt((r_ + h_) ** 2 + r_ ** 2), sqrt(r_ ** 2 + h_ ** 2),
                    h_, tangente(r_, r_ + 10 * h_))
# Übung sehne, Art r (Radius aus Sehne s und Abstand a)
for s_ in (6, 8, 9, 10, 12, 14, 16):
    for a_ in (2, 2.5, 3, 4, 5, 6, 7.5):
        rr = sqrt(s_ ** 2 / 4 + a_ ** 2)
        verschieden('Übung sehne r s=%s a=%s' % (s_, a_), rr, sqrt(s_ ** 2 + a_ ** 2), s_ / 2 + a_, 2 * rr,
                    *([sqrt(abs(s_ ** 2 / 4 - a_ ** 2))] if abs(s_ ** 2 / 4 - a_ ** 2) > 1e-9 else []))

if FEHLER:
    print('\n'.join(FEHLER))
    raise SystemExit('%d Zahl(en) stimmen nicht.' % len(FEHLER))
print('Alle Zahlen stimmen.')
