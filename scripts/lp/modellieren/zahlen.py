"""Rechnet jede Zahl des Leitprogramms Modellieren nach (08.10.2026).

  python3 scripts/lp/modellieren/zahlen.py

Exakt mit Brüchen (fractions), ohne Rundung. Geprüft werden: die 16 Aufgaben der Kontrollclips
(Ansatz, Grundform, Rechnerergebnis, verworfene Lösung, Probe am Text, falsche Angebote wirklich
falsch), die Beispiele der Einführungsclips, die Ziele der vier Aufgabenleisten, der Vortest, die
Kapitelaufgaben, der Gesamttest samt Fehlerbeispielen des Rasters. Bricht mit AssertionError ab,
sobald etwas nicht stimmt; sonst eine Liste der geprüften Werte.

Rechnerreihenfolge bei poly-solv: x1 = (−b + √D) / (2a), x2 = (−b − √D) / (2a) — so in den beiden
belegten Beispielen (Online-Hilfe: x1 = 1 + i, x2 = 1 − i; Clip g2-2b-ti30x-poly-solv: x1 = 5/2, x2 = 1).
"""
from fractions import Fraction as F
from math import isqrt

N = 0


def ok(bed, *was):
    global N
    assert bed, was
    N += 1


def wurzel(q):
    """Exakte Wurzel eines nichtnegativen Bruchs, sonst None."""
    q = F(q)
    if q < 0:
        return None
    a, b = q.numerator, q.denominator
    ra, rb = isqrt(a), isqrt(b)
    return F(ra, rb) if ra * ra == a and rb * rb == b else None


def poly(a, b, c):
    """Lösungen von a x² + b x + c = 0 in der Reihenfolge des Rechners (x1 mit +√D)."""
    a, b, c = F(a), F(b), F(c)
    D = b * b - 4 * a * c
    w = wurzel(D)
    assert w is not None, ('D keine Quadratzahl', a, b, c, D)
    return (-b + w) / (2 * a), (-b - w) / (2 * a)


def sys2(a1, b1, c1, a2, b2, c2):
    a1, b1, c1, a2, b2, c2 = map(F, (a1, b1, c1, a2, b2, c2))
    det = a1 * b2 - a2 * b1
    assert det != 0
    return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det


def gleich(a, b):
    return F(a) == F(b)


# ════════════════════════════════════════════════════════════ Kapitel 1 · Zahlenrätsel
# Einführungsclip: 47 → 74, Differenz 27 = 9 · (7 − 4); Beispiel der Themenseite: Quersumme 9, vertauscht um 45 kleiner → 72
ok(10 * 4 + 7 == 47 and 10 * 7 + 4 == 74 and 74 - 47 == 27 == 9 * (7 - 4))
z, e = sys2(1, 1, 9, 9, -9, 45)
ok((z, e) == (7, 2) and 72 - 27 == 45, 'E1 Beispiel 72')
# Einführung, quadratisch: Quersumme 9, Produkt 14 (Themenseite) → 27, 72
ok(set(poly(1, -9, 14)) == {7, 2})

# K1a-A1 linear: drei aufeinanderfolgende natürliche Zahlen, Summe 132
n = F(132 - 3, 3)
ok(n == 43 and 43 + 44 + 45 == 132, 'A1')
ok(F(132, 3) != n and F(135, 3) != n)                 # falsche Grundformen 3n = 132, 3n = 135
ok(1 + 2 + 3 == 6 and F(132, 6) == 22)                 # «n + 2n + 3n = 132» gäbe 22, 44, 66 — Summe 132, aber nicht aufeinanderfolgend
# K1a-A2 quadratisch: n² + (n + 1)² = 113 → 2n² + 2n − 112 = 0
x1, x2 = poly(2, 2, -112)
ok((x1, x2) == (7, -8) and 7 ** 2 + 8 ** 2 == 113, 'A2')
ok(wurzel(F(2 * 2) - 4 * 2 * (-112)) == 30)
# falsch: (n + n + 1)² = 113 hat keine ganze Lösung; n² + n² + 1 = 113 → n² = 56 keine ganze Lösung
ok(wurzel(113) is None and wurzel(56) is None)
# K1b-A3 LGS: Quersumme 12, vertauscht um 36 grösser → 9z − 9e = −36
z, e = sys2(1, 1, 12, 9, -9, -36)
ok((z, e) == (4, 8) and 84 - 48 == 36, 'A3')
# falsche Lesart z = 8, e = 4 (84): vertauscht 48, also kleiner
ok(48 - 84 == -36)
# K1b-A4 QGS: z = e + 2, (10z + e)(z + e) = 640 → 22e² + 62e − 600 = 0
x1, x2 = poly(22, 62, -600)
ok(x1 == 4 and x2 == F(-75, 11), 'A4', x1, x2)
ok((10 * 6 + 4) * (6 + 4) == 640)
for ee in range(10):                                   # einzige Ziffernlösung
    zz = ee + 2
    if zz <= 9 and (10 * zz + ee) * (zz + ee) == 640:
        ok(ee == 4)
# falsche Grundformen haben andere Lösungen
ok(wurzel(42 * 42 + 4 * 22 * 600) is None)            # 22e² + 42e − 600 = 0: keine rationale Lösung
ok(set(poly(22, 62, 40)) != {4})                       # 22e² + 62e + 40 = 0: e = −1 oder −20/11
ok(set(poly(22, 62, 40)) == {-1, F(-20, 11)})
# Richtung falsch: z + 2 = e → e = z + 2: (11z + 2)(2z + 2) = 640 → 22z² + 26z − 636 = 0 → z = ?
ok(poly(22, 26, -636) == (F(53, 11), -6))             # keine Ziffer: 46 wäre (4 + 6) · 46 = 460

# Leiste sim1: Ziele (Ziffern z 1..9, e 0..9)
L1 = {}
L1['50'] = [(5, 0)]
# (Prüfung 08.10.2026: «vertauscht um 45 grösser» und «e = 2z + 1» nahmen zusammen Aufgabe 1a (49) vorweg — ersetzt)
L1['-54'] = [(z, e) for z in range(1, 10) for e in range(10) if (10 * z + e) - (10 * e + z) == 54]
L1['qs13-27'] = [(z, e) for z in range(1, 10) for e in range(10) if z + e == 13 and (10 * z + e) - (10 * e + z) == 27]
L1['e2z2-qs11'] = [(z, e) for z in range(1, 10) for e in range(10) if e == 2 * z + 2 and z + e == 11]
L1['qs9-p20'] = [(z, e) for z in range(1, 10) for e in range(10) if z + e == 9 and z * e == 20]
ok(L1['-54'] == [(6, 0), (7, 1), (8, 2), (9, 3)] and L1['qs13-27'] == [(8, 5)] and L1['e2z2-qs11'] == [(3, 8)]
   and L1['qs9-p20'] == [(4, 5), (5, 4)])
ok((4, 9) not in L1['-54'] + L1['e2z2-qs11'])            # 1a (49) nicht in der Leiste
# Startwert 47 erfüllt kein Ziel
for k, v in L1.items():
    ok((4, 7) not in v, k)

# Kapitelaufgaben 1
# 1a: Einerziffer um 1 grösser als das Doppelte der Zehnerziffer, vertauscht um 45 grösser → 49
sol = [(z, e) for z in range(1, 10) for e in range(10) if e == 2 * z + 1 and (10 * e + z) - (10 * z + e) == 45]
ok(sol == [(4, 9)])
z, e = sys2(-2, 1, 1, -9, 9, 45)
ok((z, e) == (4, 9), '1a')
# 1b Übersetzen (nur Gleichungen, keine Lösung verlangt): (a) 10z + e = 10e + z + 18, (b) z · e = 10z + e − 2, (c) e = z/2.
# (a) passt zu 31 (Kontrollzahl der Lösung); (b) hat keine Ziffernlösung — verlangt ist nur das Übersetzen; (c) 21, 42, 63, 84.
ok((10 * 3 + 1) - (10 * 1 + 3) == 18)
ok([(z, e) for z in range(1, 10) for e in range(10) if z * e == 10 * z + e - 2] == [])
ok([10 * z + e for z in range(1, 10) for e in range(10) if 2 * e == z] == [21, 42, 63, 84])
# 1c: zwei aufeinanderfolgende gerade Zahlen, Produkt 168 → n(n + 2) = 168 → n = 12 oder −14
ok(poly(1, 2, -168) == (12, -14) and 12 * 14 == 168 and (-14) * (-12) == 168)
# 1d Bild: 3 Zehnerstangen, 6 Einer = 36; vertauscht 63; Differenz 27 = 9 · 3
ok(63 - 36 == 27 == 9 * (6 - 3))

# ════════════════════════════════════════════════════════════ Kapitel 2 · Mischen
# Einführung: Sirup 20 % und 50 % zu 30 kg mit 30 % (Mini-Check der Themenseite) → 20 kg, 10 kg
x, y = sys2(1, 1, 30, F(2, 10), F(5, 10), F('0.3') * 30)
ok((x, y) == (20, 10) and F('0.2') * 20 + F('0.5') * 10 == 9, 'E2')
# Verdünnen in der Einführung: 2 l Konzentrat mit 40 % auf 16 % (Themenseite A3.2) → 3 l Wasser
ok(F('0.4') * 2 == F('0.16') * (2 + 3))

# K2a-A1 linear: 12 l Sirup mit 25 %, Wasser dazu bis 10 % → 0.1w = 1.8 → w = 18
w = (F('0.25') * 12 - F('0.1') * 12) / F('0.1')
ok(w == 18 and F('0.25') * 12 == 3 and F(3, 30) == F('0.1'), 'K2 A1')
ok(F('0.25') * 12 / F('0.1') == 30)                     # Falle «Mischung = w»: w = 30
ok(F(3, 1) / F('0.1') != 18 and F('4.2') / F('0.1') == 42)  # falsche Grundformen 0.1w = 3 → 30, 0.1w = 4.2 → 42
# K2a-A2 quadratisch: Fass 40 l, zweimal x l durch Wasser ersetzt, 22.5 l Saft → (40 − x)²/40 = 22.5
x1, x2 = poly(1, -80, 700)
ok((x1, x2) == (70, 10), 'K2 A2')
ok((40 - 10) ** 2 / F(40) == F('22.5'))
ok(30 - F(10) * F(30, 40) == F('22.5'))                 # Probe am Text: 30 l Saft, 10 l Gemisch mit 3/4 Saft
ok(F(40 - 22.5) / 2 == F('8.75') and 40 - 2 * 10 == 20)  # Falle 40 − 2x = 22.5 → 8.75; Probe mit 10 gibt 20 ≠ 22.5
ok((40 - 30) == 10 and 40 - (-30) == 70)                # Wurzelweg: 40 − x = ±30
# K2b-A3 LGS: 60 % und 85 % Kupfer zu 50 kg mit 70 % → 30 kg, 20 kg
x, y = sys2(1, 1, 50, 60, 85, 3500)
ok((x, y) == (30, 20) and F('0.6') * 30 + F('0.85') * 20 == 35, 'K2 A3')
ok(F(35, 50) == F('0.7'))
# K2b-A4 QGS (neu 08.10.2026, Prüfung H4: 30 % Salz liegt über der Löslichkeit, rund 26 % bei 20 °C):
# m · p = 3, (m + 10)(p − 0.05) = 3 → p = 0.005 m + 0.05 → mal 200: m² + 10m − 600 = 0; 15 % → 10 %
x1, x2 = poly(1, 10, -600)
ok((x1, x2) == (20, -30), 'K2 A4')
p = F(3, 20)
ok(p == F('0.15') and (20 + 10) * (p - F('0.05')) == 3 and F(3, 30) == F('0.1'))
ok(F('0.005') * 20 + F('0.05') == p)                   # p = 0.005 m + 0.05
m_ = 20
ok(m_ * p - F('0.05') * m_ + 10 * p - F('0.5') == 3)    # ausmultipliziert
ok(200 * (F('0.005') * m_ ** 2 + F('0.05') * m_) == m_ ** 2 + 10 * m_ == 600)
ok(set(poly(1, -10, -600)) == {30, -20})               # Vorzeichenfehler gäbe m = 30
ok(10 ** 2 - 4 * 600 < 0)                              # c = +600: keine reelle Lösung
ok(p < F('0.264'))                                     # unter der Löslichkeit von Kochsalz

# Leiste sim2 (Sorte 1 und Sorte 2 mit Anteilen p1, p2; x, y in kg)
def misch(p1, p2, M, p):
    return sys2(1, 1, M, F(p1), F(p2), F(p) * M)
ok(misch('0.2', '0.5', 24, '0.4') == (8, 16))           # 24 kg mit 40 %
ok(misch('0.2', '0.5', 24, '0.25') == (20, 4))          # 6 kg Zucker und 25 %: 24 kg
ok(F('0.2') * 20 + F('0.5') * 4 == 6)
ok(F('0.1') * 15 == F('0.06') * (15 + 10))               # 15 kg 10-%-Lösung mit 10 kg Wasser → 6 %
ok(misch('0.2', '0.5', 30, '0.32') == (18, 12))         # Zielspiel 30 kg mit 32 %
ok(F('0.2') * 10 + F('0.5') * 10 == F('0.35') * 20)     # gleich viel von beiden: 35 %
# Startzustand der Simulation: x = 20, y = 10 (20 %, 50 %): 30 kg mit 9 kg Zucker — erfüllt kein Ziel
# (Ziele: 24 kg mit 9.6 kg; 24 kg mit 6 kg; 30 kg mit 9.6 kg; gleich viel von beiden; Verdünnen mit eigenen Sorten)
ok(F('0.2') * 20 + F('0.5') * 10 == 9 and 20 + 10 == 30 and 9 != F('9.6'))

# Kapitelaufgaben 2
ok(sys2(1, 1, 6, 40, 64, 48 * 6) == (4, 2))              # 2a Tee
ok(sys2(1, 1, 70, F('0.035'), F('0.35'), F('0.08') * 70) == (60, 10))  # 2b Milch/Rahm 8 %: rechts 5.6
ok(F('0.08') * 70 == F('5.6'))
# 2c (neu 08.10.2026, Prüfung M4: «zweimal gleich viel» wiederholte den Kontrollclip): 50 l, erst x l, dann 2x l abgelassen, 24 l
ok(poly(1, -75, 650) == (65, 10) and (50 - 10) * (50 - 20) == 1200 and F(1200, 50) == 24)
ok(poly(2, -150, 1300) == (65, 10))
ok(40 - 20 * F(40, 50) == 24)                            # Probe am Text: 40 l Mittel, 20 l Gemisch mit 80 % Mittel
ok(2 * 65 > 50)                                          # x = 65 verworfen: mehr, als im Behälter ist
ok(wurzel(75 ** 2 + 4 * 650) is None)                    # Vorzeichenfehler c: keine rationale Lösung
ok(F(6 + 6, 40) == F('0.3') and F('0.2') * 30 == 6 and F('0.6') * 10 == 6)   # 2d Bild
ok((F('0.2') + F('0.6')) / 2 == F('0.4'))

# ════════════════════════════════════════════════════════════ Kapitel 3 · Verteilen
# Einführung: Kieswerk (Themenseite A4): 12 Fahrten, 18 t und 14 t, 188 t → 5 und 7
ok(sys2(1, 1, 12, 18, 14, 188) == (5, 7), 'E3')
ok(F(190 - 14 * 12, 4) == F(22, 4))                     # 190 t: 4x = 22, x = 5.5 — nicht möglich
# Set (Themenseite): 21 Stöcke, 17 Brillen, 2215 CHF → z = 6
for zz in range(18):
    if 45 * (21 - zz) + 80 * (17 - zz) + 110 * zz == 2215:
        ok(zz == 6)

# K3a-A1 linear: 24 Billette, 18 und 12 CHF, 312 CHF → x = 4
ok(F(312 - 12 * 24, 18 - 12) == 4 and 18 * 4 + 12 * 20 == 312, 'K3 A1')
ok(F(312 - 288, 30) != 4 and F(312, 6) == 52)            # falsche Grundformen 30x = 24, 6x = 312
# K3a-A2 quadratisch: r(r + 6) = 216 → r = 12
ok(poly(1, 6, -216) == (12, -18) and 12 * 18 == 216, 'K3 A2')
ok(poly(1, 6, 216) is not None if wurzel(36 - 4 * 216) else True)  # c = +216: D < 0, keine Lösung
ok(36 - 4 * 216 < 0)
# K3b-A3 LGS: Fähre 70 Fahrzeuge, 30 und 55 CHF, 2600 CHF → 50 und 20
ok(sys2(1, 1, 70, 30, 55, 2600) == (50, 20) and 1500 + 1100 == 2600, 'K3 A3')
# K3b-A4 QGS: x · y = 360, (x − 3)(y + 6) = 360 → 2x² − 6x − 360 = 0
ok(poly(2, -6, -360) == (15, -12), 'K3 A4')
ok(15 * 24 == 360 and 12 * 30 == 360 and 2 * 15 - 6 == 24)
ok(set(poly(2, 6, -360)) == {12, -15})                   # Vorzeichenfehler y = 2x + 6 gäbe 12
# Leiste sim3
ok(sys2(1, 1, 10, 18, 14, 160) == (5, 5))
sol = [(x, y) for x in range(0, 31) for y in range(0, 31) if 18 * x + 14 * y == 200]
ok(sol == [(1, 13), (8, 4)] and min(sum(s) for s in sol) == 12)
ok(sys2(1, 1, 30, 16, 9, 382) == (16, 14))
# Startwert 6, 6: 12 Fahrten, 192 t — kein Ziel (160 t bei 10 Fahrten; 200 t; 382 CHF)
ok(18 * 6 + 14 * 6 == 192)
# Kapitelaufgaben 3
ok(sys2(1, 1, 150, 17, 11, 2190) == (90, 60))            # 3a Kino
# 3b Set: Kappen 25, Schals 30, Set 45; 20 Kappen, 14 Schals, Einnahmen → z gesucht (nur aufstellen)
for zz in range(15):
    if 25 * (20 - zz) + 30 * (14 - zz) + 45 * zz == 820:
        ok(zz == 10)
ok(25 * 10 + 30 * 4 + 45 * 10 == 820)
ok(25 * 20 + 30 * 14 == 920 and 920 - 10 * 10 == 820)       # 3b Kommentar: x = 20 − z, y = 14 − z → 920 − 10z = 820
# 3c (neu, Prüfung M4: T-Shirts wiederholten den Bus-Clip): 120 Stühle, 3 Reihen weg, je Reihe 2 weniger, 70 Stühle
ok(poly(1, -28, 180) == (18, 10) and 10 * 12 == 120 and 7 * 10 == 70)
ok(poly(2, -56, 360) == (18, 10))
ok(F(120, 18) == F(20, 3) and F(56 - 2 * 18, 3) == F(20, 3))    # r = 18: 20/3 Stühle pro Reihe — keine ganze Zahl
ok(set(poly(1, 28, 180)) == {-10, -18})                  # Vorzeichenfehler b: beide negativ
ok(4 * 18 + 8 * 7 == 128)                                # 3d Bild
ok(F(100 - 7 * 12, 18 - 7) == F(16, 11))                 # 3d: 12 Stück zu 18 und 7 CHF, 100 CHF nicht möglich

# ════════════════════════════════════════════════════════════ Kapitel 4 · Zins
# Einführung: Herr Keller (Themenseite) 30 000, 0.75 % und 2 %, 425 CHF → 14 000 und 16 000
ok(sys2(1, 1, 30000, F('0.0075'), F('0.02'), 425) == (14000, 16000), 'E4')
ok(F('0.0075') * 14000 == 105 and F('0.02') * 16000 == 320)
ok(5000 * F('1.03') ** 2 == F('5304.5'))                # Zinseszins (Themenseite A7)
ok(poly(5000, 10000, F('-304.5')) == (F(3, 100), F(-203, 100)))
ok(poly(10000, 20000, -609) == (F(3, 100), F(-203, 100)))   # Einführung: Grundform mal 2, ganzzahlig für poly-solv (M6)
ok(5000 * F('1.03') == 5150)
ok(F('0.008') * 7000 + F('0.024') * F(1, 2) * 13000 == 212)        # Zeitanteil (Themenseite)
# K4a-A1 linear: 12 000, 1.5 % ein Jahr, 2 % ein halbes Jahr, 160 CHF → 8000
x = (160 - F('0.01') * 12000) / (F('0.015') - F('0.01'))
ok(x == 8000 and F('0.015') * 8000 + F('0.02') * F(1, 2) * 4000 == 160, 'K4 A1')
ok((160 - F('0.02') * 12000) / (F('0.015') - F('0.02')) == 16000)   # ohne Zeitanteil: 16 000 > 12 000
ok(F(160, F('0.005')) == 32000 and F(40, F('0.025')) == 1600)        # falsche Grundformen
# K4a-A2 quadratisch: 5000(1 + p)² + 2000(1 + p) = 7242 → 5000p² + 12000p − 242 = 0
x1, x2 = poly(5000, 12000, -242)
ok(x1 == F(1, 50) and x2 == F(-121, 50), 'K4 A2')
ok(5000 * F('1.02') ** 2 + 2000 * F('1.02') == 7242)
ok(5000 * F('1.02') == 5100 and (5100 + 2000) * F('1.02') == 7242)
ok((7242 - 7000) / F(12000) == F(121, 6000))              # Falle einfacher Zins: p ≈ 0.0202
ok(wurzel(F(7242, 7000)) is None)                        # Falle 7000(1 + p)² = 7242: keine schöne Zahl
# K4b-A3 LGS: 2 % und 3 %, 540 CHF; vertauscht 510 CHF → 9000 und 12 000
ok(sys2(2, 3, 54000, 3, 2, 51000) == (9000, 12000), 'K4 A3')
ok(F('0.02') * 9000 + F('0.03') * 12000 == 540 and F('0.03') * 9000 + F('0.02') * 12000 == 510)
# K4b-A4 QGS: K · p = 480, (K − 4000)(p + 0.004) = 480 → 1 000 000p² + 4000p − 480 = 0
x1, x2 = poly(1000000, 4000, -480)
ok(x1 == F(1, 50) and x2 == F(-3, 125), 'K4 A4')
ok(F(480) / x1 == 24000 and F(480) / x2 == -20000 and 4000 + 1000000 * x1 == 24000)
ok(20000 * F('0.024') == 480)
ok(set(poly(1000000, -4000, -480)) == {F(3, 125), F(-1, 50)})   # Vorzeichenfehler gäbe p = 0.024
# Leiste sim4
ok((500 - F('0.02') * 30000) / (F('0.0075') - F('0.02')) == 8000)
ok((260 - F('0.01') * 30000) / (F('0.0075') - F('0.01')) == 16000)
ok(5000 * F('1.02') ** 2 == 5202 and 5000 * F('1.04') ** 2 - 5000 == 408)
# Startwert 15 000: 0.0075 · 15 000 + 0.02 · 15 000 = 412.50 — kein Ziel (500; 260 im Halbjahr: 112.5 + 150 = 262.5)
ok(F('0.0075') * 15000 + F('0.02') * 15000 == F('412.5') and F('0.0075') * 15000 + F('0.01') * 15000 == F('262.5'))
# Kapitelaufgaben 4
ok(sys2(1, 1, 16000, F('0.015'), F('0.025'), 300) == (10000, 6000))    # 4a
ok(F('0.018') * F(8, 12) == F('0.012') and F('0.009') * F(1, 4) == F('0.00225') and F('0.024') * F(5, 12) == F('0.01'))  # 4b
# 4c (neu, Prüfung M4/M6: 8000 · (1 + p)² wiederholte die Leiste, Grundform mit −241.8 ohne belegte Anzeige):
# 10 000 CHF, im zweiten Jahr 0.5 Prozentpunkte mehr, 10 353 CHF → 10 000p² + 20 050p − 303 = 0 (ganzzahlig)
ok(10000 * (1 + F('0.015')) * (1 + F('0.015') + F('0.005')) == 10353)
ok(10000 * F('1.015') == 10150 and 10150 * F('1.02') == 10353)
ok(poly(10000, 20050, -303) == (F(3, 200), F(-101, 50)))
ok(F(-101, 50) == F('-2.02'))
ok(wurzel(20000 ** 2 + 4 * 10000 * 353) is None)         # Fehler «+ 0.005 im zweiten Jahr vergessen»: 10 000p² + 20 000p − 353 = 0, keine glatte Lösung
ok(abs((10353 / 10000) ** 0.5 - 1 - 0.0175) < 0.0001)
ok(F('0.01') * 12000 + F('0.025') * 8000 == 320 and F('0.0175') * 20000 == 350)   # 4d

# ════════════════════════════════════════════════════════════ Vortest
ok(F(18) / F('3.6') == 5)
ok((1, -8, 8) == (1, -6 - 2, 9 - 1))                     # (x − 3)² = 2x + 1
ok(sys2(1, 1, 9, 3, 1, 21) == (6, 3))
ok(sys2(2, -1, 3, 3, 2, 12) == (F(18, 7), F(15, 7)))     # 0d nur ordnen; Lösung nicht verlangt

# ════════════════════════════════════════════════════════════ Gesamttest (neu 08.10.2026, Prüfung H1, M3, M4)
# Teil A ohne Taschenrechner: G1 Ziffern (LGS), G2 Ansätze vergleichen (LGS / linear), G3 Set (drei Unbekannte → linear)
# Teil B mit Taschenrechner: G4 Mischung mit Wasser (LGS, sys-solv), G5 Eindampfen (QGS, poly-solv),
#                            G6 Zinseszins mit Abhebung (quadratisch), G7 gleich viel Zins mit Zeitanteil (LGS)
# G1: Zahl um 9 grösser als das Vierfache der Quersumme, vertauscht um 27 grösser → 69
sol = [(z, e) for z in range(1, 10) for e in range(10) if 10 * z + e == 4 * (z + e) + 9 and (10 * e + z) - (10 * z + e) == 27]
ok(sol == [(6, 9)] and sys2(6, -3, 9, -9, 9, 27) == (6, 9))
ok(sys2(2, -1, 3, -1, 1, 3) == (6, 9))
ok(4 * 15 + 9 == 69 and 96 - 69 == 27)
ok(sys2(-6, 3, 9, -1, 1, 3) == (0, 3))                    # «+ 9 auf der falschen Seite»: z = 0, keine zweistellige Zahl
# G2: Theater 300 Plätze, 22 und 30 CHF, 7400 CHF → 200 Parkett, 100 Balkon
ok(sys2(1, 1, 300, 22, 30, 7400) == (200, 100))
ok(22 * 200 + 30 * 100 == 7400 and 22 * 200 + 9000 - 30 * 200 == 7400)
ok(F(7400 - 6600, 8) == 100)                              # Preise vertauscht: x = 100
ok(F(7400 - 9000, 52) < 0)                                # Minus vor der Klammer vergessen: 52x = −1600
xa, ya = sys2(1, 1, 7400, 22, 30, 300)                  # Ansatz A gäbe negative Anzahlen
ok(ya < 0 and xa > 7400)
# G3: Kiosk — Sandwich 6 CHF, Getränk 3 CHF, Menü 8 CHF; 50 Sandwiches, 70 Getränke, 476 CHF
z_ = F(6 * 50 + 3 * 70 - 476, 6 + 3 - 8)
ok(z_ == 34 and 50 - 34 == 16 and 70 - 34 == 36)
ok(6 * 16 + 3 * 36 + 8 * 34 == 476 and 96 + 108 + 272 == 476)
ok(6 * (50 - 34) + 3 * (70 - 34) + 8 * 34 == 476 and 300 + 210 - 34 == 476)
ok(F(476 - 6 * 50 - 3 * 70, 8 - 6) < 0)                   # Menü nur bei den Sandwiches gezählt (y = 70): z = −17
ok(F(476 - 300 - 3 * 70, 8 - 6) == -17)
# G4: 10 %, 30 % und 10 kg Wasser → 50 kg mit 14 %
ok(sys2(1, 1, 40, F('0.1'), F('0.3'), F('0.14') * 50) == (25, 15))
ok(sys2(1, 1, 40, 1, 3, 70) == (25, 15) and F('0.14') * 50 == 7)
ok(F('0.1') * 25 + F('0.3') * 15 == 7 and 25 + 15 + 10 == 50 and F(7, 50) == F('0.14'))
ok(sys2(1, 1, 50, 1, 3, 70) == (40, 10) and 40 + 10 + 10 == 60)    # Wasser in der Mengenbilanz vergessen: 60 kg
ok(sys2(1, 1, 40, 1, 3, F('0.14') * 40 * 10) == (32, 8))          # Stoff aus 40 statt 50 kg (0.14 · 40): 32, 8
# G5: Eindampfen — 6 kg Zucker, 10 kg Wasser verdunsten, Anteil + 5 Prozentpunkte → m = 40, p = 0.15
x1, x2 = poly(1, -10, -1200)
ok((x1, x2) == (40, -30), 'G5')
p = F(6, 40)
ok(p == F('0.15') and (40 - 10) * (p + F('0.05')) == 6 and F(6, 30) == F('0.2'))
ok(F('0.005') * 40 - F('0.05') == p)                    # p = 0.005 m − 0.05
ok(40 * p + F('0.05') * 40 - 10 * p - F('0.5') == 6)     # ausmultipliziert
ok(200 * (F('0.005') * 40 ** 2 - F('0.05') * 40) == 40 ** 2 - 10 * 40 == 1200)
ok(set(poly(1, 10, -1200)) == {30, -40})                 # Vorzeichenfehler b: m = 30, p = 0.2 — Probe (20 kg, 25 %) deckt auf
ok(20 * (F('0.2') + F('0.05')) == 5)
ok(10 ** 2 - 4 * 1200 < 0)                             # c = +1200: keine reelle Lösung
ok(F(6, 40) < F('0.6'))                                  # Zuckerlösung, gut löslich
ok(poly(200, 10, -6) == (F(3, 20), F(-1, 5)) and 200 * F(3, 20) + 10 == 40)   # Weg über p: m = 200p + 10
ok(poly(F('0.005'), F('-0.05'), -6) == (40, -30))           # ohne mal 200
r5 = sorted([5 + 37 ** 0.5, 5 - 37 ** 0.5])                # Fehler «+ 5 statt + 0.05»: m² − 10m − 12 = 0
ok(abs(r5[1] - 11.08) < 0.01 and r5[0] < 0)
ok(10 ** 2 - 4 * 1200 < 0)                                  # Fehler «m + 10 statt m − 10»: m² + 10m + 1200 = 0, keine Lösung
# G6: 6000 CHF, nach einem Jahr 1000 abgehoben, nach zwei Jahren 5110.60 → p = 0.01
ok((6000 * F('1.01') - 1000) * F('1.01') == F('5110.6'))
x1, x2 = poly(6000, 11000, F('-110.6'))
ok(x1 == F(1, 100) and x2 == F(-553, 300), 'G6', x2)
ok(poly(30000, 55000, -553) == (F(1, 100), F(-553, 300)))   # mal 5: ganzzahlig
ok(set(poly(6000, -1000, F('-5110.6'))) == {F('1.01'), F(-5060, 6000)})   # Weg über q = 1 + p
ok(F(-5060, 6000) == F(-253, 300))
ok(set(poly(F('0.6'), 110, F('-110.6'))) == {1, F(-553, 3)})            # p in Prozent: 0.6p² + 110p − 110.6 = 0
# Fehler «Abhebung nicht mitverzinst» und «− 1000 · p beim Ausmultiplizieren verloren»: beide b = 12 000 — gleiche Zahlen
ok(abs((6110.6 / 6000) ** 0.5 - 1 - 0.0092) < 0.0001)
r12 = sorted(float(v) for v in [(-12000 + (12000 ** 2 + 4 * 6000 * 110.6) ** 0.5) / 12000])
ok(abs(r12[0] - 0.0092) < 0.0001)
# Fehler «Mittelglied 2 · 6000 · p vergessen»: b = −1000 → p ≈ 0.243
rb = (1000 + (1000 ** 2 + 4 * 6000 * 110.6) ** 0.5) / 12000
ok(abs(rb - 0.2426) < 0.0001)
# G7: 18 000 CHF, A 9 Monate zu 2 %, B ein Jahr zu 1.2 %, gleich viel Zins
ok(F('0.02') * F(9, 12) == F('0.015'))
ok(sys2(1, 1, 18000, F('0.015'), F('-0.012'), 0) == (8000, 10000))
ok(sys2(1, 1, 18000, 5, -4, 0) == (8000, 10000) and sys2(1, 1, 18000, 15, -12, 0) == (8000, 10000))
ok(F('0.015') * 8000 == 120 == F('0.012') * 10000)
ok(sys2(1, 1, 18000, F('0.02'), F('-0.012'), 0) == (6750, 11250))   # Zeitanteil vergessen
ok(F('0.02') * 6750 == 135 and F('0.012') * 11250 == 135)          # … und die Probe ohne Zeitanteil stimmt scheinbar
ok(sys2(1, 1, 18000, F('0.012'), F('-0.015'), 0) == (10000, 8000))  # Zinssätze vertauscht zugeordnet
ok(sys2(1, 1, 18000, F('0.18'), F('-0.012'), 0) == (1125, 16875))     # 9 statt 9/12
ok(F(216, F('0.027')) == 8000)                                       # mit einer Unbekannten: 0.027x = 216

print('zahlen.py: alle', N, 'Prüfungen bestanden')
