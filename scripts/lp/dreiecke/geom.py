"""Geometrie-Helfer der Bauskripte des Leitprogramms Dreiecke (clips.py, zahlen.py)."""
import math


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def richtung(p, q):
    """Richtung von p nach q in Grad, 0 … 360."""
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def abst(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def winkel(p, a, b):
    """Innenwinkel bei p zwischen pa und pb, Grad."""
    u, v = (a[0] - p[0], a[1] - p[1]), (b[0] - p[0], b[1] - p[1])
    return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))


def lot(p, a, b):
    """Fusspunkt des Lots von p auf die Gerade ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy)


def mitte(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def schnitt(p, d, q, e):
    """Schnitt der Geraden p + s d und q + t e."""
    det = d[0] * (-e[1]) - d[1] * (-e[0])
    s = ((q[0] - p[0]) * (-e[1]) - (q[1] - p[1]) * (-e[0])) / det
    return (p[0] + s * d[0], p[1] + s * d[1])


def punkte(A, B, C):
    """Höhenschnittpunkt, Schwerpunkt, Inkreis- und Umkreismittelpunkt mit Radien."""
    fa, fb = lot(A, B, C), lot(B, A, C)
    H = schnitt(A, (fa[0] - A[0], fa[1] - A[1]), B, (fb[0] - B[0], fb[1] - B[1]))
    S = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    a, b, c = abst(B, C), abst(C, A), abst(A, B)
    MI = ((a * A[0] + b * B[0] + c * C[0]) / (a + b + c), (a * A[1] + b * B[1] + c * C[1]) / (a + b + c))
    mc, mb = mitte(A, B), mitte(A, C)
    MU = schnitt(mc, (-(B[1] - A[1]), B[0] - A[0]), mb, (-(C[1] - A[1]), C[0] - A[0]))
    s_ = (a + b + c) / 2
    ri = math.sqrt(s_ * (s_ - a) * (s_ - b) * (s_ - c)) / s_
    return dict(H=H, S=S, MI=MI, MU=MU, ri=ri, ru=abst(MU, A))


def wfuss(C, A, B):
    """Fusspunkt der Winkelhalbierenden aus C auf AB (teilt AB im Verhältnis CA : CB)."""
    ca, cb = abst(C, A), abst(C, B)
    return (A[0] + (B[0] - A[0]) * ca / (ca + cb), A[1] + (B[1] - A[1]) * ca / (ca + cb))


def dritte_ecke(A, B, al, be):
    """C aus der Grundseite AB (A links, B rechts) und den Winkeln α bei A und β bei B."""
    w = richtung(A, B)
    return schnitt(A, (math.cos(math.radians(w + al)), math.sin(math.radians(w + al))),
                   B, (math.cos(math.radians(w + 180 - be)), math.sin(math.radians(w + 180 - be))))


