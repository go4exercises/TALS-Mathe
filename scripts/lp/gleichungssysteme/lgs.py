"""Rechenkern für das Leitprogramm Lineare Gleichungssysteme (11.10.2026) — nur Python-Standardbibliothek.

  from lgs import lin, gl, system_loesung, folgt_aus, schl2, schl3

- lin('2(y - 1) + y')        → lineare Form {'x': Fraction, 'y': …, '': Konstante}
- gl('2x + y = 7')           → Gleichung als Form «links − rechts = 0»
- system_loesung([...])      → ('eine', (x, y[, z])) | ('keine', None) | ('unendlich', None)
- folgt_aus(system, glg)     → True, wenn die Gleichung eine Linearkombination des Systems ist
                                (Zeilenraum der erweiterten Matrix) — so wird jede Zeile der Umformer geprüft
- schl2 / schl3              → Normalform-Schlüssel eines Systems (dieselbe Rechnung wie sysSchl() in seite.js)

Schreibweise der Gleichungen wie im Heft und im LaTeX der Seite: «2x + y = 7», «x = y - 1»,
«3(2y - 1) + y = 11», «2 \\cdot 2 + y = 7», Dezimalzahlen mit Punkt, Brüche «\\tfrac{7}{3}».
"""
from fractions import Fraction as F
import re

VARS = ('x', 'y', 'z')


class _P:
    """Rekursiver Abstieg: Summe aus Produkten; ein Produkt darf höchstens einen nicht konstanten Faktor haben."""

    def __init__(self, s):
        s = s.replace('\\cdot', '*').replace('\\,', '').replace('\\left', '').replace('\\right', '')
        s = re.sub(r'\\[td]?frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', s)
        s = s.replace('−', '-').replace('·', '*').replace(' ', '')
        self.t = re.findall(r'\d+(?:\.\d+)?|[xyz]|[-+*/()]', s)
        if ''.join(self.t) != s:
            raise ValueError('unbekanntes Zeichen in ' + repr(s))
        self.i = 0

    def sieh(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def nimm(self):
        self.i += 1
        return self.t[self.i - 1]

    def summe(self):
        f = {}
        vz = 1
        if self.sieh() in ('+', '-'):
            vz = -1 if self.nimm() == '-' else 1
        f = _add(f, self.produkt(), vz)
        while self.sieh() in ('+', '-'):
            vz = -1 if self.nimm() == '-' else 1
            f = _add(f, self.produkt(), vz)
        return f

    def produkt(self):
        f = self.faktor()
        while True:
            c = self.sieh()
            if c == '*':
                self.nimm()
                f = _mul(f, self.faktor())
            elif c == '/':
                self.nimm()
                g = self.faktor()
                if set(k for k, v in g.items() if v and k) :
                    raise ValueError('Division durch Variable')
                f = {k: v / g.get('', F(0)) for k, v in f.items()}
            elif c is not None and (c in VARS or c == '(' or re.match(r'\d', c)):
                f = _mul(f, self.faktor())          # implizites Mal: 2x, 2(…), x(…) nur mit Konstante
            else:
                return f

    def faktor(self):
        c = self.nimm()
        if c == '(':
            f = self.summe()
            assert self.nimm() == ')'
            return f
        if c == '-':
            return {k: -v for k, v in self.faktor().items()}
        if c in VARS:
            return {c: F(1)}
        return {'': F(c)}


def _add(a, b, vz=1):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, F(0)) + vz * v
    return r


def _mul(a, b):
    va = [k for k, v in a.items() if k and v]
    vb = [k for k, v in b.items() if k and v]
    if va and vb:
        raise ValueError('nicht linear')
    if vb:
        a, b = b, a
    c = b.get('', F(0))
    return {k: v * c for k, v in a.items()}


def lin(s):
    p = _P(s)
    f = p.summe()
    if p.i != len(p.t):
        raise ValueError('Rest in ' + repr(s))
    return {k: f.get(k, F(0)) for k in VARS + ('',)}


def gl(s):
    """«links = rechts» → Vektor (a_x, a_y, a_z, c) für a_x x + a_y y + a_z z = c."""
    if s.count('=') != 1:
        raise ValueError('keine Gleichung: ' + s)
    l, r = s.split('=')
    a, b = lin(l), lin(r)
    return tuple(a[v] - b[v] for v in VARS) + (b[''] - a[''],)


def _rang(zeilen):
    m = [list(z) for z in zeilen]
    r = 0
    for c in range(len(m[0]) if m else 0):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def folgt_aus(system, glg):
    """Ist glg (String oder Vektor) eine Linearkombination der Gleichungen von system?"""
    S = [gl(s) if isinstance(s, str) else s for s in system]
    g = gl(glg) if isinstance(glg, str) else glg
    return _rang(S) == _rang(S + [g])


def nvar(system):
    S = [gl(s) if isinstance(s, str) else s for s in system]
    return 3 if any(z[2] for z in S) else 2


def system_loesung(system, n=None):
    S = [gl(s) if isinstance(s, str) else s for s in system]
    n = n or nvar(S)
    A = [list(z[:n]) for z in S]
    Ab = [list(z[:n]) + [z[3]] for z in S]
    ra, rab = _rang(A), _rang(Ab)
    if ra < rab:
        return ('keine', None)
    if ra < n:
        return ('unendlich', None)
    # eindeutig: Gauss
    m = [r[:] for r in Ab]
    sol = [None] * n
    r = 0
    piv = []
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(r)
        r += 1
    for c in range(n):
        sol[c] = m[c][n] / m[c][c]
    return ('eine', tuple(sol))


def erfuellt(system, punkt):
    S = [gl(s) if isinstance(s, str) else s for s in system]
    p = list(punkt) + [0] * (3 - len(punkt))
    return all(z[0] * p[0] + z[1] * p[1] + z[2] * p[2] == z[3] for z in S)


def _ggt(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def norm(z, n):
    """Gleichung ganzzahlig, gekürzt, erste von null verschiedene Zahl positiv → Tupel (wie normGl in seite.js)."""
    v = [F(c) for c in list(z[:n]) + [z[3] if len(z) == 4 else z[n]]]
    nenner = 1
    for c in v:
        nenner = nenner * c.denominator // _ggt(nenner, c.denominator)
    w = [int(c * nenner) for c in v]
    g = 0
    for c in w:
        g = _ggt(g, c)
    g = g or 1
    w = [c // g for c in w]
    erst = next((c for c in w if c), 1)
    if erst < 0:
        w = [-c for c in w]
    return tuple(w)


def schl(system, n=None):
    """Schlüssel eines Systems: normierte Gleichungen, sortiert, mit «|» und «;» — wie sysSchl() in seite.js."""
    S = [gl(s) if isinstance(s, str) else s for s in system]
    n = n or nvar(S)
    teile = sorted(norm(z, n) for z in S)
    return ';'.join('|'.join(str(c) for c in t) for t in teile)


def tex_zahl(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    if v.denominator in (2, 4, 5, 8, 10, 20, 25):
        s = ('%.6f' % float(v)).rstrip('0')
        return s
    return ('-' if v < 0 else '') + '\\tfrac{%d}{%d}' % (abs(v.numerator), v.denominator)


def tex_paar(p):
    return '(' + ' \\mid '.join(tex_zahl(c) for c in p) + ')'
