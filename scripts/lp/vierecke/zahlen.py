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
D1e = (4 * math.cos(math.radians(50)), 4 * math.sin(math.radians(50))); C1e = (4 + D1e[0], D1e[1])
ok([round(v, 3) for v in D1e] == [2.571, 3.064] and [round(v, 3) for v in C1e] == [6.571, 3.064], '1e Figur: Rhombus mit Seite 4, α = 50°')
ok(gl(winkel((0, 0), (4, 0), (6.571, 3.064)), 25, 0.01) and gl(abst((4, 0), (6.571, 3.064)), 4, 0.001), '1e Figur: e unter 25°, BC = 4')
# 1f: gleich lange Diagonalen ohne Rechteck — das gleichschenklige Trapez von sim1 A6 (c 2, v 1.5, h 3)
ok(gl(abst((0, 0), (3.5, 3)), abst((5, 0), (1.5, 3))) and not gl(winkel((0, 0), (5, 0), (1.5, 3)), 90), '1f: gleichschenkliges Trapez, Diagonalen gleich, kein Rechteck')

# ════════════════════════════════════════════════ Kapitel 1 · Übungen (Prüfung 08.10.2026, V-H2, V-H3)
# Gegenbeispiel für «In jedem Trapez …»: das Start-Trapez von sim1 (a 5, c 3.5, v 1, h 3.5) widerlegt jede Eigenschaft
St = [(0, 0), (5, 0), (4.5, 3.5), (1, 3.5)]
eS, fS = abst(St[0], St[2]), abst(St[1], St[3])
ok(not gl(eS, fS), 'Ü familie: Start-Trapez, Diagonalen verschieden lang (dg)')
ok(not gl((St[2][0] - St[0][0]) * (St[3][0] - St[1][0]) + (St[2][1] - St[0][1]) * (St[3][1] - St[1][1]), 0), 'Ü familie: nicht senkrecht (ds)')
ok(all(not gl(winkel(St[i], St[i - 1], St[(i + 1) % 4]), 90, 1e-6) for i in range(4)), 'Ü familie: kein rechter Winkel (rw)')
ok(len({round(abst(St[i], St[(i + 1) % 4]), 6) for i in range(4)}) == 4, 'Ü familie: Seiten nicht gleich (gs)')
ok(not parallel(St[1], St[2], St[0], St[3]), 'Ü familie: nur ein Paar parallel (pp), Diagonalen halbieren sich nicht (dh)')
wS = [winkel(St[i], St[i - 1], St[(i + 1) % 4]) for i in range(4)]
ok(not gl(wS[0], wS[2]) and not gl(wS[1], wS[3]), 'Ü familie: gegenüberliegende Winkel verschieden (gw)')
# Die früheren Gegenbeispiel-Sätze sind beim Trapez nicht allgemein falsch (der Befund): rechtwinkliges Trapez,
# gleichschenkliges Trapez, Trapez c 3, v 1, h 4 mit senkrechten Diagonalen
ok(gl(winkel((0, 0), (5, 0), (0, 3)), 90), 'Befund: rechtwinkliges Trapez hat rechte Winkel')
U4 = [(0, 0), (5, 0), (4, 4), (1, 4)]
dAC, dBD = (U4[2][0] - U4[0][0], U4[2][1] - U4[0][1]), (U4[3][0] - U4[1][0], U4[3][1] - U4[1][1])
ok(gl(dAC[0] * dBD[0] + dAC[1] * dBD[1], 0) and gl(math.hypot(*dAC), math.hypot(*dBD)), 'Umkehrung: c 3, v 1, h 4 — Diagonalen senkrecht und gleich lang')
mAC, mBD = ((U4[0][0] + U4[2][0]) / 2, (U4[0][1] + U4[2][1]) / 2), ((U4[1][0] + U4[3][0]) / 2, (U4[1][1] + U4[3][1]) / 2)
ok(mAC != mBD and not parallel(U4[1], U4[2], U4[0], U4[3]), 'Umkehrung: … aber sie halbieren sich nicht, kein Rhombus/Quadrat')
ok(art1(3, 1, 4) == 'gleichschenklig', 'Umkehrung: in sim1 einstellbar (c 3, v 1, h 4 auf dem Raster)')
# viereck-winkel «um d° grösser»: d = 20 … 120 ohne 60 und 90; α = (180 − d)/2 ganz und positiv; Fehlerzahlen verschieden
for d in [x * 10 for x in range(2, 13) if x * 10 not in (60, 90)]:
    al_, be_ = (180 - d) / 2, (180 + d) / 2
    ok(al_ > 0 and al_ == int(al_) and gl(be_ - al_, d), 'Ü Differenz d = %d' % d)
    ok(len({al_, (360 - d) / 2, be_, 180 - d}) == 4, 'Ü Differenz d = %d: α-Fehler verschieden' % d)
    ok(len({be_, (360 + d) / 2, al_, 180 + d}) == 4, 'Ü Differenz d = %d: β-Fehler verschieden' % d)
ok((360 - 90) / 2 == (180 + 90) / 2 and 180 - 60 == (180 + 60) / 2, 'Ü Differenz: d = 90 und d = 60 gäben Doppeldeutungen')

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
# A6 (Wahl h_b) seit der Prüfung mit a 6, h 4, v 3 (V-M2): Die Falle BD stand bei a 8, h 4, v 3 unter 88.2° auf AD
def wink(u, v):
    return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))
ok(abs(wink((3 - 8, 4), (3, 4)) - 88.21) < 0.01, 'sim2 alt: BD steht 88.2° auf AD (der Befund)')
BD6 = (3 - 6, 4)
ok(abs(wink(BD6, (3, 4)) - 90) > 15 and abs(wink(BD6, (3, 4)) - 73.74) < 0.01, 'sim2 A6: BD unter 73.7° zu AD und BC, wirkt nicht wie eine Höhe')
F6, t6 = lot((0, 0), (6, 0), (9, 4))
ok(gl(abst((0, 0), F6), 4.8) and t6 < 0 and gl(F6[0], 3.84) and gl(F6[1], -2.88), 'sim2 A6: h_b von A, Fuss (3.84|−2.88) ausserhalb')
ok(-2.88 > -4.7 + 0.3, 'sim2 A6: Fusspunkt im Fenster (y0 = −4.7)')
ok(abs(wink((9, 4), (3, 4)) - 29.17) < 0.01, 'sim2 A6: AC nicht senkrecht auf BC')
ok(abs(math.degrees(math.atan2(F6[1], F6[0])) - math.degrees(math.atan2(4, 9))) > 30, 'sim2 A6: h_b und e = AC getrennt')
# Wahl: Richtungen ab A von h_b (−36.87°) und e = AC (20.0°) — A7 (Frage) behält a 8, h 4, v 3
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
# K3 F2: Mittellinien durch die Schenkelmitten (Prüfung 08.10.2026, V-M4: rechts stand sie bei (7.5|2.5)–(11.5|2.5))
TL_, TR_ = [(0, 1), (5, 1), (4, 4), (1, 4)], [(6.5, 1), (11.5, 1), (12, 4), (9, 4)]
for T_, soll in ((TL_, ((0.5, 2.5), (4.5, 2.5))), (TR_, ((7.75, 2.5), (11.75, 2.5)))):
    ok(((T_[0][0] + T_[3][0]) / 2, (T_[0][1] + T_[3][1]) / 2) == soll[0] and ((T_[1][0] + T_[2][0]) / 2, (T_[1][1] + T_[2][1]) / 2) == soll[1]
       and gl(abst(*soll), 4), 'K3 F2 Mittellinie %s' % (soll,))

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
# K4 F5: Klickziel Hypotenuse (0|0)–(3|4) ohne die Ecken, Toleranz 0.3; je 200 Klickstellen (V-M4: vorher 19 % Fehltreffer)
def fuss_(p, z):
    (ax, ay), (bx, by) = z; dx, dy = bx - ax, by - ay; q = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - dx * q, p[1] - ay - dy * q)
def stellen(z, n=200):
    (ax, ay), (bx, by) = z; return [(ax + (bx - ax) * (i + 0.5) / n, ay + (by - ay) * (i + 0.5) / n) for i in range(n)]
ZH = ((0.3, 0.4), (2.7, 3.6))
ok(gl(abst((0, 0), ZH[0]), 0.5) and gl(abst((3, 4), ZH[1]), 0.5), 'K4 F5 Ziel: je 0.5 von A und D abgeschnitten')
treff = sum(fuss_(p, ZH) <= 0.3 for p in stellen(((0, 0), (3, 4)))) / 200
fehl_u = sum(fuss_(p, ZH) <= 0.3 for p in stellen(((0, 0), (3, 0)))) / 200
fehl_h = sum(fuss_(p, ZH) <= 0.3 for p in stellen(((3, 4), (3, 0)))) / 200
print('K4 F5 Hypotenuse getroffen', treff, ' Überstand als richtig', fehl_u, ' Höhe als richtig', fehl_h)
ok(treff >= 0.9 and fehl_u == 0 and fehl_h == 0, 'K4 F5 Klicktoleranz')
# Kapitel 1 Clip «Bezeichnungen»: e näher an AC als an BD, f näher an BD (V-M4: «f» stand auf e)
def dseg(p, a, b):
    return fuss_(p, (a, b))
ALLG_ = [(0.5, 1), (5.5, 1), (6, 5.5), (1.5, 4.5)]
ok(dseg((4.6, 3.69 + 0.15), ALLG_[0], ALLG_[2]) < 0.5 < dseg((4.6, 3.69 + 0.15), ALLG_[1], ALLG_[3]), 'Clip1 Beschriftung e bei AC')
ok(dseg((4.76, 2.03 + 0.15), ALLG_[1], ALLG_[3]) < 0.5 < dseg((4.76, 2.03 + 0.15), ALLG_[0], ALLG_[2]), 'Clip1 Beschriftung f bei BD')

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

# trapez-hoehe, Variante Parallelogramm: nur exakte Tripel (ü, h, s); GT G2 (2.5, 6, 6.5) gesperrt
TRI = [[3, 4, 5], [4, 3, 5], [5, 12, 13], [12, 5, 13], [8, 6, 10], [6, 8, 10], [1.5, 2, 2.5], [2, 1.5, 2.5], [2.5, 6, 6.5], [4.5, 6, 7.5], [6, 4.5, 7.5]]
ok(all(gl(math.hypot(t[0], t[1]), t[2]) for t in TRI), 'Ü trapez-hoehe: Tripel exakt')
ok(all(r2(math.hypot(t[2], t[0])) != t[1] and not gl(t[2] - t[0], t[1]) for t in TRI), 'Ü Parallelogramm: Fehler ≠ Sollwert')

# ════════════════════════════════════════════════ Kapitel 4 · Aufgaben
d_tv = math.hypot(89, 50)
ok(r2(d_tv) == 102.08 and r2(d_tv / 2.54) == 40.19, '4a Fernseher')
print('4a d =', d_tv, ' Zoll =', d_tv / 2.54)
ok(gl(math.hypot(24, 7), 25) and 4 * 25 == 100 and 48 * 14 / 2 == 336 and gl(math.hypot(48, 14), 50), '4b Rhombus e 48, f 14')
ue_c = (20 - 12) / 2
ok(ue_c == 4 and gl(math.sqrt(8.5 ** 2 - 16), 7.5) and (20 + 12) / 2 * 7.5 == 120 and 20 + 12 + 17 == 49, '4c')
ok(r2(10 / math.sqrt(2)) == 7.07 and 10 * 10 / 2 == 50, '4e')

# ════════════════════════════════════════════════ Gesamttest (Fassung nach der Prüfung, 08.10.2026: 24 P)
# G1 (a): Diagonalen halbieren sich, senkrecht, 7 und 10 lang → Rhombus, kein Quadrat
e1, f1 = 7, 10
ok(e1 != f1, 'G1 a: verschieden lang, also kein Quadrat')
ok(gl(math.hypot(e1 / 2, f1 / 2), math.hypot(3.5, 5)), 'G1 a: Rhombus existiert (Seite √(3.5² + 5²))')
# G1 (b): Trapez AB ∥ CD, β = 80, δ − α = 40 → α 70, δ 110, γ 100
al, de = (180 - 40) / 2, (180 + 40) / 2
ok((al, de, 180 - 80) == (70, 110, 100) and al + 80 + 100 + de == 360, 'G1 b')
ok(((360 - 40) / 2, (360 + 40) / 2) == (160, 200) and ((180 - 40) / 2 + 40 == 110), 'BP G1 b: mit 360 → 160/200')
ok((180 - 80, 180 - 80 + 40) == (100, 140), 'BP G1 b: α mit β gepaart → α 100, δ 140')
# Figur zu G1 (b) möglich: A(0|0), B(b|0), D unter α = 70°, C unter β = 80° auf derselben Höhe
hG = 3
DG = (hG / math.tan(math.radians(70)), hG); CG = (8 - hG / math.tan(math.radians(80)), hG)
ok(CG[0] > DG[0], 'G1 b: Trapez mit α 70, β 80 existiert (c > 0)')
# G2: a 9.5, AD 6.5, AF 2.5 → h 6, A 57, h_b 57/6.5
hG2 = math.sqrt(6.5 ** 2 - 2.5 ** 2)
ok(gl(hG2, 6) and gl(9.5 * hG2, 57) and r2(57 / 6.5) == 8.77, 'G2')
ok(57 / 6.5 <= 9.5 and hG2 <= 6.5, 'G2 widerspruchsfrei: h_b ≤ a, h ≤ AD')
ok(gl(hG2 / 6.5, (57 / 6.5) / 9.5), 'G2: sin α aus beiden Höhen gleich')
ok(r2(math.hypot(6.5, 2.5)) == 6.96 and math.hypot(6.5, 2.5) > 6.5, 'BP G2: plus statt minus → 6.96 > 6.5 unmöglich')
ok(gl(9.5 * 6.5, 61.75) and gl(61.75 / 6.5, 9.5), 'BP G2: Seite als Höhe → 61.75, 9.5')
ok(r2(2 * 57 / 6.5) == 17.54 and gl(57 / 9.5, 6), 'BP G2: 2A/b 17.54, A/a 6')
# G3: Rhombus a 8.5, e 15 → f/2 4, f 8, A 60, h 60/8.5
f2 = math.sqrt(8.5 ** 2 - 7.5 ** 2)
ok(gl(f2, 4) and gl(15 * 2 * f2 / 2, 60) and r2(60 / 8.5) == 7.06, 'G3')
ok(2 * f2 < 15, 'G3: 15 ist die längere Diagonale')
ok(gl(15 * 4 / 2, 30) and r2(30 / 8.5) == 3.53, 'BP G3: f nicht verdoppelt → 30, 3.53')
ok(r2(math.hypot(8.5, 7.5)) == 11.34 and math.hypot(8.5, 7.5) > 8.5, 'BP G3: plus → 11.34 > 8.5 unmöglich')
ok(15 * 8 == 120 and r2(120 / 8.5) == 14.12 and r2(2 * 60 / 8.5) == 14.12 and 120 / 8.5 > 8.5, 'BP G3: 120 → 14.12 > 8.5; 2A/a 14.12')
# G4: Walmdach a 12, A 38.25, h 4.5 → m 8.5, c 5, ü 3.5, s √32.5
mG4 = 38.25 / 4.5; cG4 = 2 * mG4 - 12; uG4 = (12 - cG4) / 2; sG4 = math.hypot(uG4, 4.5)
ok(gl(mG4, 8.5) and gl(cG4, 5) and gl(uG4, 3.5) and gl(sG4 ** 2, 32.5) and r2(sG4) == 5.70, 'G4')
ok(gl(2 * 38.25 / 4.5, 17) and gl(38.25 / 4.5 - 12, -3.5) and (12 - 17) / 2 < 0, 'BP G4: 17 (Überstand negativ), −3.5')
ok(r2(math.hypot(7, 4.5)) == 8.32 and 3.5 + 4.5 == 8 and r2(math.sqrt(4.5 ** 2 - 3.5 ** 2)) == 2.83, 'BP G4: 8.32, 8, 2.83')
ok(not gl(math.hypot(abs(12 - 17) / 2, 4.5), sG4), 'G4: Fehler «c = 17» gibt nicht zufällig denselben Grat')
print('G4 Dachneigung (Seitenfläche) ≈', round(math.degrees(math.acos(uG4 / 4.5)), 1), '° — realistisch')
# G5: a 11, c 5, h 4 → m 8, Teile 19 und 13
mG5 = (11 + 5) / 2
ok(mG5 == 8 and (11 + 8) / 2 * 2 == 19 and (8 + 5) / 2 * 2 == 13 and 19 + 13 == mG5 * 4, 'G5')
ok((11 + 8) / 2 * 4 == 38 and (8 + 5) / 2 * 4 == 26 and 11 + 5 == 16 and (11 - 5) / 2 == 3, 'BP G5: 38/26, 16, 3')
# G6: Rechteck b 56, d 65 → h 33, U 178; Quadrat d 65 → a 65/√2
ok(gl(math.sqrt(65 ** 2 - 56 ** 2), 33) and 2 * (56 + 33) == 178 and r2(65 / math.sqrt(2)) == 45.96, 'G6')
ok(r2(math.hypot(65, 56)) == 85.80 and r2(2 * (56 + 85.80)) == 283.60 and 56 + 33 == 89, 'BP G6: 85.80, 283.60, 89')
ok(65 / 2 == 32.5 and r2(65 * math.sqrt(2)) == 91.92, 'BP G6: 32.5, 91.92')
print('G6 Seitenverhältnis 56 : 33 =', round(56 / 33, 3), '(16 : 9 =', round(16 / 9, 3), '), Diagonale', round(65 / 2.54, 1), 'Zoll')
# Punkte und Zeit
ok(4 + 4 + 4 + 4 + 4 + 4 == 24, 'GT Summe 24 P')

# Figuren im Gesamttest absichtlich nicht massstäblich (das Gesuchte soll gerechnet, nicht gemessen werden)
ok(not gl(5, hG2) and not gl(5.5, f2) and not gl(6, cG4) and not gl(4, 5), 'GT-Figuren verzerrt: h 5 ≠ 6, f/2 5.5 ≠ 4, First 6 ≠ 5, c 4 ≠ 5')
ok(((0 + 3.5) / 2, (11 + 7.5) / 2) == (1.75, 9.25), 'GT G5-Figur: Mittellinie durch die Schenkelmitten')


# ════════════════════════════════════════════════ Ergebnis
if FEHLER:
    print('\nFEHLER:')
    for f in FEHLER:
        print('  ', f)
    raise SystemExit(1)
print('\nALLE ZAHLEN STIMMEN')
