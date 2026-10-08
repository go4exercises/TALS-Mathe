"""Alle Zahlen des Leitprogramms Vierecke (GF 5.2b), mit python3 nachgerechnet (08.10.2026).

  python3 scripts/lp/vierecke/zahlen.py        → Exit 0, wenn alles stimmt

Jede Zahl, die in seite.py, seite.js, clips.py oder den LaTeX-Quellen steht, kommt hier vor:
Clips, Arbeitsbereiche (Startwerte, Ziele, Sollwerte, Fehlerwerte), Festhalten, Kapitelaufgaben,
Vortest, Gesamttest und Bewertungspaket (inkl. der Zahlen in den typischen Fehlern).
"""
import itertools
import math

FEHLER = []


def ok(bed, text):
    if not bed:
        FEHLER.append(text)


def gl(a, b, tol=1e-9):
    return abs(a - b) <= tol


def r2(x):
    return round(x + 1e-12, 2)


def winkel(p, a, b):
    """Innenwinkel bei p zwischen pa und pb in Grad."""
    u = (a[0] - p[0], a[1] - p[1]); v = (b[0] - p[0], b[1] - p[1])
    return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))


def abst(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def lot(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy), t


def parallel(p, q, r, s):
    return gl((q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0]), 0)


# ════════════════════════════════════════════════ Kapitel 0 · Vortest
ok(7 * 3 == 21 and 2 * (7 + 3) == 20, '0a')
ok(100 * 100 == 10000 and gl(3500 / 10000, 0.35), '0b')
ok(gl(math.hypot(8, 15), 17) and gl(math.sqrt(10 ** 2 - 6 ** 2), 8), '0c')
ok(10 * 4 / 2 == 20, '0d')
ok(180 - 65 == 115, '0e')

# ════════════════════════════════════════════════ Kapitel 1 · Clip «Familie» (a = 5, A(0.5|1), B(5.5|1))
A, B = (0.5, 1), (5.5, 1)
allg = [A, B, (6, 5.5), (1.5, 4.5)]
ok(not parallel(A, B, allg[3], allg[2]) and not parallel(B, allg[2], A, allg[3]), 'Clip1 allgemein ist kein Trapez')
trap = [A, B, (5, 4.5), (1.5, 4.5)]
ok(parallel(A, B, trap[3], trap[2]) and not parallel(B, trap[2], A, trap[3]), 'Clip1 Trapez')
para = [A, B, (6.5, 4.5), (1.5, 4.5)]
ok(parallel(A, B, para[3], para[2]) and parallel(B, para[2], A, para[3]) and gl(abst(para[3], para[2]), 5), 'Clip1 Parallelogramm')
recht = [A, B, (5.5, 4.5), (0.5, 4.5)]
ok(gl(winkel(A, B, recht[3]), 90) and gl(abst(A, recht[2]), abst(B, recht[3])), 'Clip1 Rechteck, Diagonalen gleich')
rhom = [A, B, (8.5, 5), (3.5, 5)]
ok(all(gl(abst(rhom[i], rhom[(i + 1) % 4]), 5) for i in range(4)), 'Clip1 Rhombus Seiten 5')
e_ = (rhom[2][0] - A[0], rhom[2][1] - A[1]); f_ = (rhom[3][0] - B[0], rhom[3][1] - B[1])
ok(gl(e_[0] * f_[0] + e_[1] * f_[1], 0), 'Clip1 Rhombus Diagonalen senkrecht')
ok(gl(winkel(A, B, rhom[2]), winkel(A, rhom[2], rhom[3])), 'Clip1 Rhombus: e halbiert alpha')
quad = [A, B, (5.5, 6), (0.5, 6)]
ok(all(gl(abst(quad[i], quad[(i + 1) % 4]), 5) for i in range(4)) and gl(winkel(A, B, quad[3]), 90), 'Clip1 Quadrat')
# Winkel vorgelöst: alpha = 70 (Mini-Check der Themenseite)
D70 = (0.5 + 4 * math.cos(math.radians(70)), 1 + 4 * math.sin(math.radians(70)))
C70 = (6 + D70[0] - 0.5, D70[1])
ok(gl(winkel((0.5, 1), (6, 1), D70), 70, 1e-6) and gl(winkel((6, 1), C70, (0.5, 1)), 110, 1e-6), 'Clip1 alpha 70, beta 110')
print('Clip1 D70 =', [round(v, 3) for v in D70], 'C70 =', [round(v, 3) for v in C70])
# Winkelsumme der allgemeinen Figur
ws = sum(winkel(allg[i], allg[i - 1], allg[(i + 1) % 4]) for i in range(4))
ok(gl(ws, 360, 1e-6), 'Clip1 Winkelsumme 360')

# ════════════════════════════════════════════════ Kapitel 1 · Kontrollclip
ok(180 - 65 == 115 and 360 - 65 == 295, 'K1 F2')
A4, B4, C4 = (1, 1), (6, 1), (8, 4)
D4 = (A4[0] + C4[0] - B4[0], A4[1] + C4[1] - B4[1])
ok(D4 == (3, 4), 'K1 F4 D = (3|4)')
ok(abst(D4, (1, 4)) >= 1.5 and abst(D4, (6, 4)) >= 1.5, 'K1 F4 Fallen weit genug weg')
ok(gl(abst((6, 4), (8, 4)), 2), 'K1 F4 Falle (6|4): CD = 2')
ok(360 - 85 - 110 - 75 == 90 and 85 + 110 + 75 == 270, 'K1 F5')

# ════════════════════════════════════════════════ Kapitel 1 · Arbeitsbereich sim1
# A(0|0), B(5|0), D(v|h), C(v + c|h). Regler c 1..6, v −3..4, h 1..5 (Schritt 0.5). Start c 2, v 1, h 3.
def sim1(c, v, h):
    A_, B_, C_, D_ = (0, 0), (5, 0), (v + c, h), (v, h)
    return A_, B_, C_, D_


def art1(c, v, h):
    if c == 5:
        if v == 0:
            return 'Quadrat' if h == 5 else 'Rechteck'
        return 'Rhombus' if gl(v * v + h * h, 25) else 'Parallelogramm'
    return 'gleichschenklig' if gl(v, (5 - c) / 2) else 'Trapez'


RASTER = lambda a, b: [a + 0.5 * i for i in range(int(round((b - a) / 0.5)) + 1)]
start1 = (3.5, 1, 3.5)                      # wie das Trapez im Einführungsclip (a 5, c 3.5, v 1, h 3.5)
ok(art1(*start1) == 'Trapez', 'sim1 Start ist allgemeines Trapez')
rh = [(c, v, h) for c in RASTER(1, 6) for v in RASTER(-3, 4) for h in RASTER(1, 5) if art1(c, v, h) == 'Rhombus']
print('sim1 Rhombus-Lösungen:', rh)
ok(len(rh) >= 2, 'sim1 Rhombus erreichbar')
ok(art1(5, 0, 5) == 'Quadrat', 'sim1 Quadrat erreichbar')
# Aufgabe Symmetrieachse: c 2, v 1.5, h 3 → gleichschenklig, Achse x = 2.5; Höhe aus D bei x = 1.5
ok(art1(2, 1.5, 3) == 'gleichschenklig', 'sim1 Symmetrie-Aufgabe gleichschenklig')
s1 = 320 / 14.2
ok(abs(2.5 - 1.5) * s1 > 16, 'sim1 Achse und Höhe auseinander (px)')
# Aufgabe Diagonale im Rhombus c 5, v 3, h 4
A_, B_, C_, D_ = sim1(5, 3, 4)
ok(gl(winkel(A_, B_, C_), winkel(A_, C_, D_)), 'sim1 e halbiert alpha')
ok(not gl(winkel(B_, A_, D_), 2 * winkel(B_, A_, C_)), 'sim1 f halbiert beta, nicht durch A')
print('sim1 Rhombus alpha =', round(winkel(A_, B_, D_), 2), ' alpha/2 =', round(winkel(A_, B_, D_) / 2, 2))
# Aufgabe α = 45°: c 5, v 3, h 3
A_, B_, C_, D_ = sim1(5, 3, 3)
ok(gl(winkel(A_, B_, D_), 45) and gl(winkel(B_, C_, A_), 135) and gl(winkel(C_, D_, B_), 45), 'sim1 alpha 45, beta 135, gamma 45')
# Aufgabe Trapez α 45, β 90: c 3, v 2, h 2
A_, B_, C_, D_ = sim1(3, 2, 2)
ok(gl(winkel(A_, B_, D_), 45) and gl(winkel(B_, C_, A_), 90) and gl(winkel(C_, D_, B_), 90) and gl(winkel(D_, A_, C_), 135), 'sim1 Trapez 45/90/90/135')
ok(360 - 45 - 90 == 225, 'sim1 Falle 225')
# keine Leistenaufgabe ist im Startzustand gelöst (Ziele): c == 5? v == 0? gleichschenklig?
ok(start1[0] != 5 and not gl(start1[1], (5 - start1[0]) / 2), 'sim1 Start löst keine Zielaufgabe')

# ════════════════════════════════════════════════ Kapitel 1 · Aufgaben
ok((180 - 58, 58, 180 - 58) == (122, 58, 122), '1b')
P = [(0, 0), (4, 0), (6, 3), (2, 3)]
ok(parallel(P[0], P[1], P[3], P[2]) and parallel(P[1], P[2], P[0], P[3]), '1c Parallelogramm')
ok(gl(abst(P[0], P[3]), math.sqrt(13)) and not gl(math.sqrt(13), 4), '1c kein Rhombus')
print('1c AD =', round(math.sqrt(13), 2))
ok(180 - 72 == 108 and 180 - 64 == 116, '1d')
ok(50 / 2 == 25 and 180 - 50 == 130, '1e')

# ════════════════════════════════════════════════ Kapitel 2 · Clip «Fläche»
ok(5 * 3 == 15 and 2 * (5 + 3) == 16, 'Clip2 Rechteck 5 × 3')
ok(7 * 3 == 21, 'Clip2 Parallelogramm a 7, h 3 (Figur)')
# Vorgelöst: A(0|1) B(8|1) C(12|4) D(4|4): a 8, b 5, h 3
ok(gl(abst((0, 1), (4, 4)), 5), 'Clip2 b = 5')
ok(8 * 3 == 24 and 2 * (8 + 5) == 26 and gl(24 / 5, 4.8), 'Clip2 A 24, U 26, h_b 4.8')
F_, t_ = lot((4, 4), (8, 1), (12, 4))
ok(gl(abst((4, 4), F_), 4.8) and t_ < 0, 'Clip2 h_b von D aus, Fusspunkt auf der Verlängerung von CB')
print('Clip2 Fusspunkt h_b von D:', [round(v, 3) for v in F_])
ok(8 * 6 / 2 == 24, 'Clip2 Rhombus e 8, f 6: 24')

# ════════════════════════════════════════════════ Kapitel 2 · Kontrollclip
ok(9 * 4 == 36 and 9 * 6 == 54 and 9 * 4 / 2 == 18, 'K2 F1')
ok(10 * 7 / 2 == 35 and 10 * 7 == 70 and 10 + 7 == 17, 'K2 F3')
ok(10 * 3 / 5 == 6 and 5 * 3 / 10 == 1.5 and 2 * 30 / 5 == 12, 'K2 F5')
ok(3 <= 5 and 6 <= 10, 'K2 F5 möglich (h_a ≤ b, h_b ≤ a)')

# ════════════════════════════════════════════════ Kapitel 2 · Arbeitsbereich sim2
# A(0|0), B(a|0), C(a + v|h), D(v|h). Regler a 2..9, h 1..5, v −3..5. Start a 8, h 3, v 4 (Clipbeispiel, b = 5).
ok(gl(math.hypot(4, 3), 5), 'sim2 Start b = 5')
b6 = math.hypot(2, 3)
ok(gl(6 * 3, 18) and r2(2 * (6 + b6)) == 19.21 and r2(6 * b6) == 21.63 and r2(b6) == 3.61, 'sim2 A 18, U 19.21')
ok(abs(2 * (6 + 3.61) - 19.21) <= 0.011, 'sim2 U mit gerundetem b in der Toleranz')
print('sim2 b =', b6, ' U =', 2 * (6 + b6))
# Ziel A = 20, kein Rechteck
lsg20 = [(a, h) for a in RASTER(2, 9) for h in RASTER(1, 5) if gl(a * h, 20)]
print('sim2 A = 20:', lsg20)
ok(len(lsg20) >= 2 and 8 * 3 != 20, 'sim2 A = 20 erreichbar, Start nicht')
rh2 = [(a, v, h) for a in RASTER(2, 9) for v in RASTER(-3, 5) for h in RASTER(1, 5) if v != 0 and gl(math.hypot(v, h), a)]
print('sim2 Rhombus:', rh2)
ok(len(rh2) >= 2 and not gl(math.hypot(4, 3), 8), 'sim2 Rhombus erreichbar, Start nicht')
# h_b: a 8, h 4, v 3 → b 5, A 32, h_b 6.4; Lot von A auf die Gerade BC
F_, t_ = lot((0, 0), (8, 0), (11, 4))
ok(gl(abst((0, 0), F_), 6.4) and t_ < 0, 'sim2 h_b = 6.4, Fuss ausserhalb')
print('sim2 Fusspunkt h_b:', [round(v, 3) for v in F_])
ok(gl(5 * 4 / 8, 2.5) and gl(2 * 32 / 5, 12.8), 'sim2 Fehlerwerte h_b')
# Wahl: Richtungen ab A von h_b (−36.87°) und e = AC (20.0°)
ok(abs(math.degrees(math.atan2(F_[1], F_[0])) - math.degrees(math.atan2(4, 11))) > 30, 'sim2 Kandidaten getrennt')

# ════════════════════════════════════════════════ Kapitel 2 · Aufgaben
ok(5 * 3 == 15, '2a')
ok(12 * 9 / 2 == 54, '2b')
ok(gl(1.2 * 0.8, 0.96) and 0.96 * 10000 == 9600 and gl(2 * (1.2 + 0.8), 4), '2c')
ok(12 * 5 == 60 and 2 * (12 + 7.5) == 39 and 60 / 7.5 == 8, '2d')
ok(5 <= 7.5 and 8 <= 12, '2d möglich')
ok(gl(math.hypot(9, 12), 15) and 18 * 24 / 2 == 216 and gl(216 / 15, 14.4), '2e')
ok(gl(math.hypot(12, 5), 13) and r2(12 * math.sqrt(2)) == 16.97, 'Festhalten 4: Rechteck 12 × 5')

# ════════════════════════════════════════════════ Kapitel 3 · Clip «Trapez» (a 6, c 4, h 3)
A3, B3, C3, D3 = (1, 1), (7, 1), (5.5, 4), (1.5, 4)
M1, M2 = ((A3[0] + D3[0]) / 2, 2.5), ((B3[0] + C3[0]) / 2, 2.5)
ok(gl(abst(M1, M2), 5) and gl(abst(D3, C3), 4), 'Clip3 m = 5')
# gedrehte Kopie um die Mitte von BC
Mb = M2
kop = [(2 * Mb[0] - p[0], 2 * Mb[1] - p[1]) for p in (A3, B3, C3, D3)]
print('Clip3 Kopie:', kop)
ok(gl(abst(A3, kop[3]), 10) and gl(kop[3][1], 1) and gl(abst(D3, kop[0]), 10), 'Clip3 Parallelogramm mit Grundseite a + c = 10')
ok((6 + 4) / 2 * 3 == 15, 'Clip3 A 15')
ok(2 * 12 / (6 + 2) == 3 and (6 + 2) / 2 == 4, 'Clip3 rückwärts: A 12, a 6, c 2 → m 4, h 3')

# ════════════════════════════════════════════════ Kapitel 3 · Kontrollclip
ok((12 + 8) / 2 == 10, 'K3 F1')
ok((9 + 5) / 2 * 6 == 42 and (9 + 5) * 6 == 84 and 9 * 5 * 6 == 270, 'K3 F3')
ok(40 / 8 == 5 and 40 * 8 == 320 and 40 / 16 == 2.5, 'K3 F4')
ok(((0 + 2) / 2, (0 + 4) / 2) == (1, 2), 'K3 F5 Mitte von AD')
ok((5 + 3) / 2 * 3 == 12, 'K3 F2 beide Trapeze 12')

# ════════════════════════════════════════════════ Kapitel 3 · Arbeitsbereich sim3
# A(0|0), B(6|0), D(v|h), C(v + c|h). Regler c 1..6, h 1..5, v −2..4. Start c 4, h 3, v 0.5.
ok((6 + 4) / 2 == 5 and 5 * 3 == 15, 'sim3 Start m 5, A 15')
ok(not gl(0.5, (6 - 4) / 2), 'sim3 Start nicht gleichschenklig')
ok((6 + 3) / 2 == 4.5 and (6 + 4) / 2 != 4.5, 'sim3 m = 4.5 bei c = 3, Start nicht')
lsg = [(c, h) for c in RASTER(1, 6) for h in RASTER(1, 5) if gl((6 + c) / 2 * h, 20)]
print('sim3 A = 20:', lsg)
ok(len(lsg) >= 2 and (6 + 4) / 2 * 3 != 20, 'sim3 A = 20 erreichbar, Start nicht')
ok((6 + 5) / 2 == 5.5 and 5.5 * 2.5 == 13.75 and 11 * 2.5 == 27.5 and 6 * 5 * 2.5 == 75, 'sim3 Frage m, A')
ok(14 / ((6 + 1) / 2) == 4 and 14 / 7 == 2 and r2(14 / 6) == 2.33, 'sim3 Frage h = 4')

# ════════════════════════════════════════════════ Kapitel 3 · Aufgaben
ok((11 + 7) / 2 == 9 and 9 * 4.5 == 40.5, '3a')
Tz = [(0, 0), (8, 0), (6, 3), (1, 3)]
ok(gl(abst(Tz[3], Tz[2]), 5) and (8 + 5) / 2 == 6.5 and 6.5 * 3 == 19.5, '3b')
ok(gl((((0 + 1) / 2) - ((8 + 6) / 2)), -6.5), '3b Mittellinie von (0.5|1.5) bis (7|1.5)')
ok(gl((1.2 + 3) / 2, 2.1) and gl(2.73 / 2.1, 1.3), '3c Graben')
ok((10 + 4) / 2 * 5 == 35 and gl(math.sqrt(25 - 9), 4) and (10 + 4) / 2 * 4 == 28, '3e (Lösung nennt 28 nicht als Pflicht)')

# ════════════════════════════════════════════════ Kapitel 4 · Clip «Längen»
ok(gl(math.hypot(12, 5), 13), 'Clip4 Rechteck 12 × 5: d 13')
ok(r2(5 * math.sqrt(2)) == 7.07, 'Clip4 Quadrat 5: d ≈ 7.07')
ok(gl(math.hypot(4, 3), 5), 'Clip4 Rhombus e 8, f 6: a 5')
ue = (12 - 4) / 2
ok(ue == 4 and gl(math.sqrt(25 - 16), 3), 'Clip4 Trapez a 12, c 4, s 5: ü 4, h 3')
ok((12 + 4) / 2 * 3 == 24 and 12 + 4 + 2 * 5 == 26, 'Clip4 A 24, U 26')

# ════════════════════════════════════════════════ Kapitel 4 · Kontrollclip
ok(gl(math.hypot(9, 12), 15) and r2(9 * math.sqrt(2)) == 12.73, 'K4 F1')
ok(r2(6 * math.sqrt(2)) == 8.49, 'K4 F2')
ok((14 - 8) / 2 == 3 and (14 + 8) / 2 == 11, 'K4 F3')
ok(gl(math.hypot(12, 5), 13) and gl(math.hypot(24, 10), 26) and 12 + 5 == 17, 'K4 F4')

# ════════════════════════════════════════════════ Kapitel 4 · Arbeitsbereich sim4 (gleichschenkliges Trapez)
# A(0|0), B(a|0), D(ü|h), C(a − ü|h), ü = (a − c)/2. Regler a 6..12, c 1..10, h 1..6. Start a 12, c 4, h 3.
ok(gl(math.hypot((12 - 4) / 2, 3), 5), 'sim4 Start: Schenkel 5 (Clipbeispiel)')
z43 = [(a, c, h) for a in range(6, 13) for c in range(1, 11) for h in RASTER(1, 6) if h == 4 and gl(abs(a - c), 6)]
print('sim4 Ziel s 5, h 4:', len(z43), 'Lösungen, z. B.', z43[:3])
ok(len(z43) >= 2 and not (3 == 4), 'sim4 Ziel erreichbar, Start (h 3) nicht')
ue4 = (10 - 5) / 2
ok(gl(math.sqrt(6.5 ** 2 - ue4 ** 2), 6) and (10 + 5) / 2 * 6 == 45, 'sim4 Frage 1: h 6, A 45')
ok(r2(math.sqrt(6.5 ** 2 - 25)) == 4.15 and r2(math.hypot(6.5, 2.5)) == 6.96 and 6.5 - 2.5 == 4, 'sim4 Frage 1 Fehlerwerte')
ok((10 + 5) * 6 == 90 and 7.5 * 6.5 == 48.75, 'sim4 Frage 1 Fehlerwerte A')
ue5 = (7 - 4) / 2
ok(gl(math.hypot(ue5, 2), 2.5) and 7 + 4 + 2 * 2.5 == 16, 'sim4 Frage 2: s 2.5, U 16')
ok(ue5 + 2 == 3.5 and r2(math.hypot(3, 2)) == 3.61 and 7 + 4 + 2.5 == 13.5, 'sim4 Frage 2 Fehlerwerte')
# Wahl: Richtungen ab A von AD (36.87°) und AC (20.56°)
ok(abs(math.degrees(math.atan2(3, 4)) - math.degrees(math.atan2(3, 8))) > 10, 'sim4 AD und AC getrennt')

# ════════════════════════════════════════════════ Kapitel 4 · Arbeitsbereich sim5 (Rhombus aus Diagonalen)
# Regler e, f 2..16 (Schritt 1). Start e 8, f 6 (Clip: a 5).
ok(gl(math.hypot(4, 3), 5) and 8 * 6 / 2 == 24, 'sim5 Start a 5, A 24')
z65 = [(e, f) for e in range(2, 17) for f in range(2, 17) if gl(math.hypot(e / 2, f / 2), 6.5)]
print('sim5 a = 6.5:', z65)
ok(len(z65) >= 2, 'sim5 a = 6.5 erreichbar')
ok(gl(2 * math.sqrt(100 - 36), 16) and 12 * 16 / 2 == 96, 'sim5 Frage: f 16, A 96')
ok(gl(math.sqrt(100 - 36), 8) and r2(2 * math.sqrt(100 + 36) / 1) == 23.32 and 12 * 16 == 192, 'sim5 Fehlerwerte')

# ════════════════════════════════════════════════ Kapitel 4 · Aufgaben
d_tv = math.hypot(89, 50)
ok(r2(d_tv) == 102.08 and r2(d_tv / 2.54) == 40.19, '4a Fernseher')
print('4a d =', d_tv, ' Zoll =', d_tv / 2.54)
ok(gl(math.hypot(24, 7), 25) and 4 * 25 == 100 and 48 * 14 / 2 == 336 and gl(math.hypot(48, 14), 50), '4b Rhombus e 48, f 14')
ue_c = (20 - 12) / 2
ok(ue_c == 4 and gl(math.sqrt(8.5 ** 2 - 16), 7.5) and (20 + 12) / 2 * 7.5 == 120 and 20 + 12 + 17 == 49, '4c')
ok(r2(10 / math.sqrt(2)) == 7.07 and 10 * 10 / 2 == 50, '4e')

# ════════════════════════════════════════════════ Gesamttest
# G1 (b): α − β = 40, α + β = 180
ok((110 - 70, 110 + 70) == (40, 180), 'G1 b')
# G2: a 7.5, b 5, h_a 4
ok(7.5 * 4 == 30 and 2 * (7.5 + 5) == 25 and 30 / 5 == 6, 'G2')
ok(gl(4 / 5, 6 / 7.5), 'G2 widerspruchsfrei (sin α = 0.8)')
ok(7.5 * 5 == 37.5 and 7.5 * 4 / 2 == 15 and 2 * (7.5 + 4) == 23 and 30 / 7.5 == 4 and gl(5 * 4 / 7.5, 2.67, 0.01), 'G2 Fehlerwerte')
# G3: Rhombus 70 cm × 40 cm
aG3 = math.hypot(35, 20)
ok(70 * 40 / 2 == 1400 and gl(1400 / 10000, 0.14) and r2(aG3) == 40.31 and r2(4 * aG3) == 161.25, 'G3')
ok(r2(4 * 40.31) == 161.24, 'G3 mit gerundeter Seite 161.24')
ok(r2(math.hypot(70, 40)) == 80.62 and r2(4 * math.hypot(70, 40)) == 322.49 and 70 * 40 == 2800, 'G3 Fehlerwerte')
print('G3 a =', aG3, ' U =', 4 * aG3)
# G4: Dachfläche
ok((12 + 7) / 2 == 9.5 and 9.5 * 4.5 == 42.75 and 42.75 * 15 == 641.25, 'G4')
ok((12 + 7) * 4.5 == 85.5 and 85.5 * 15 == 1282.5, 'G4 Fehlerwerte')
# G5: c aus A, h, a
ok(60 / 6 == 10 and 2 * 10 - 13 == 7, 'G5')
ok(60 / 6 - 13 == -3 and 2 * 60 / 6 == 20, 'G5 Fehlerwerte')
# G6: gleichschenkliges Trapez a 18, c 8, Schenkel 13
ue6 = (18 - 8) / 2
ok(ue6 == 5 and gl(math.sqrt(169 - 25), 12) and (18 + 8) / 2 * 12 == 156 and 18 + 8 + 26 == 52, 'G6')
ok(r2(math.sqrt(169 - 100)) == 8.31 and r2(13 * 13) == 169 and (18 + 8) / 2 * 13 == 169, 'G6 Fehlerwerte')
print('G6 Fehler ganzer Unterschied: h =', math.sqrt(169 - 100), ' A =', 13 * math.sqrt(69))
ok(r2(13 * math.sqrt(69)) == 107.99, 'G6 Folgewert 107.99')
# G7: Rechteck 6 × 8
ok(gl(math.hypot(6, 8), 10) and r2(6 * math.sqrt(2)) == 8.49, 'G7')


# ════════════════════════════════════════════════ Bewertungspaket: Zahlen in den typischen Fehlern
ok((200 - 160, 200 + 160) == (40, 360), 'BP G1: mit 360 gerechnet → α 200, β 160')
ok(7.5 * 5 == 37.5 and 37.5 / 5 == 7.5 and r2(5 * 4 / 7.5) == 2.67 and 2 * 30 / 5 == 12 and 2 * (7.5 + 4) == 23, 'BP G2')
ok(70 * 40 == 2800 and gl(2800 / 10000, 0.28) and r2(math.hypot(70, 40)) == 80.62 and r2(4 * math.hypot(70, 40)) == 322.49 and 35 + 20 == 55, 'BP G3')
ok((12 + 7) * 4.5 == 85.5 and 85.5 * 15 == 1282.5 and 12 + 7 == 19 and (12 - 7) / 2 == 2.5 and math.ceil(641.25) == 642, 'BP G4')
ok(2 * 60 / 6 == 20 and 60 / 6 - 13 == -3, 'BP G5')
ok(r2(math.sqrt(69)) == 8.31 and r2(13 * math.sqrt(69)) == 107.99 and 13 * 13 == 169 and r2(math.hypot(13, 5)) == 13.93
   and r2(13 * math.hypot(13, 5)) == 181.07 and 18 + 8 + 13 == 39, 'BP G6')
ok(r2(8 * math.sqrt(2)) == 11.31 and 6 + 8 == 14, 'BP G7')

# ════════════════════════════════════════════════ Ergebnis
if FEHLER:
    print('\nFEHLER:')
    for f in FEHLER:
        print('  ', f)
    raise SystemExit(1)
print('\nALLE ZAHLEN STIMMEN')
