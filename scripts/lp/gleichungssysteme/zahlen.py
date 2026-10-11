"""Rechnet jede Zahl des Leitprogramms Lineare Gleichungssysteme nach (11.10.2026) und liefert die Sperrliste.

  python3 scripts/lp/gleichungssysteme/zahlen.py        # alle Prüfungen; Exit 1 bei einem Befund

FEST nennt jedes feste System des Leitprogramms (Clips, Kontrollfragen, Simulationen, Umformer, Festhalten,
Kapitelaufgaben, Vortest, Gesamttest) mit dem behaupteten Ergebnis: ein Tupel, 'keine' oder 'unendlich'.
Die Liste ist zugleich die Sperrliste der Zufallsübungen (sperre(): Normalform-Schlüssel wie sysSchl() in seite.js).
Dazu einzelne Rechnungen aus Texten, Rückmeldungen und Fehlerbeispielen (EINZELN).
"""
from fractions import Fraction as F
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lgs import gl, lin, system_loesung, folgt_aus, schl, norm, erfuellt  # noqa: E402
import umformer  # noqa: E402

h = F(1, 2)
# (Quelle, System, Ergebnis)
FEST = [
    # Kapitel 1
    ('Clip schnittpunkt / Festhalten 2, Clip einsetzen, Clip addition', ['2x + y = 7', 'x - y = -1'], (2, 3)),
    ('Kontrolle schnittpunkt F1 (nur (I) stimmt für (1 | 4))', ['3x + y = 7', 'x + y = 4'], (F(3, 2), F(5, 2))),
    ('Kontrolle schnittpunkt F4', ['x - y = 2', 'x + 2y = 8'], (4, 2)),
    ('Kontrolle schnittpunkt F5', ['x + 2y = 5', '3x - 2y = -1'], (1, 2)),
    ('Sim 1 System 1', ['x + y = 5', '2x - y = 4'], (3, 2)),
    ('Sim 1 System 2', ['x + 2y = 4', 'x - y = 1'], (2, 1)),
    ('Sim 1 System 3', ['x + y = 3', 'x - y = -2'], (h, F(5, 2))),
    ('Festhalten 1 Fehler ((5 | 1) nur auf (I))', ['x - y = 4', 'x + y = 4'], (4, 0)),
    ('1a', ['2x + 3y = 3', 'x - y = 4'], (3, -1)),
    ('1b', ['x + y = 7', 'x - 2y = 1'], (5, 2)),
    ('1c', ['2x - y = 5', 'x + y = 4'], (3, 1)),
    ('1d', ['x + y = 6', 'x - y = 2'], (4, 2)),
    ('1e', ['2x + y = 5', 'x - y = -1'], (F(4, 3), F(7, 3))),
    # Kapitel 2
    ('Festhalten 2 Klammer', ['x = 3y + 2', '2x - y = 9'], (5, 1)),
    ('Kontrolle einsetzen F1', ['y = 3x - 4', '2x + y = 6'], (2, 2)),
    ('Kontrolle einsetzen F2', ['x = 2y - 1', '3x + y = 11'], (3, 2)),
    ('Kontrolle einsetzen F3', ['y = 2x + 1', 'y = -x + 7'], (2, 5)),
    ('Kontrolle einsetzen F5', ['y = x + 2', 'y = -2x + 5'], (1, 3)),
    ('2a', ['y = 2x - 5', '4x - 3y = 9'], (3, 1)),
    ('2b', ['x = 3y + 4', 'x = -y + 8'], (7, 1)),
    ('2c', ['y = 5 - x', '3x + 2y = 13'], (3, 2)),
    ('2d', ['3x + y = 5', '5x - 2y = 12'], (2, -1)),
    ('2e', ['y = 2x - 1', 'y = -x + 4'], (F(5, 3), F(7, 3))),
    # Kapitel 3
    ('Clip addition / Festhalten 3', ['2x + 3y = 12', '5x - 2y = 11'], (3, 2)),
    ('Kontrolle addition F1', ['4x + 3y = 6', '2x - 3y = 12'], (3, -2)),
    ('Kontrolle addition F2', ['x + 4y = 9', '3x - 2y = 13'], (5, 1)),
    ('Kontrolle addition F3', ['5x + 2y = 9', '5x - 3y = -1'], (1, 2)),
    ('Kontrolle addition F4', ['y = 4x - 1', 'y = -2x + 5'], (1, 3)),
    ('Kontrolle addition F5', ['3x + 5y = 2', '-3x + 2y = 5'], (-1, 1)),
    ('3a', ['5x + 2y = 1', '3x - 2y = 7'], (1, -2)),
    ('3b', ['2x + 5y = 1', '4x + 3y = 9'], (3, -1)),
    ('3c', ['4x + 3y = 5', '3x - 2y = -9'], (-1, 3)),
    ('3d(a)', ['x = 4 - 2y', '3x + 5y = 13'], (6, -1)),
    ('3d(b)', ['y = 3x + 1', 'y = -x + 9'], (2, 7)),
    ('3d(c)', ['6x - 5y = 7', '4x + 5y = 13'], (2, 1)),
    ('3e', ['x + y = 5', 'x - y = 1'], (3, 2)),
    # Kapitel 4
    ('Clip faelle: parallel (Mini-Check der Themenseite)', ['x + y = 3', 'x + y = 5'], 'keine'),
    ('Clip faelle: identisch (Themenseite A5)', ['2x - y = 4', '-4x + 2y = -8'], 'unendlich'),
    ('Clip faelle / Festhalten 4: k = -3', ['3x - 6y = 9', '-x + 2y = -3'], 'unendlich'),
    ('Clip faelle: k = 1', ['3x - 6y = 9', '-x + 2y = 1'], 'keine'),
    ('Kontrolle faelle F2', ['6x + 3y = 9', '2x + y = 3'], 'unendlich'),
    ('Kontrolle faelle F3', ['y = 3x - 1', '6x - 2y = 2'], 'unendlich'),
    ('Kontrolle faelle F4', ['y = 2x + 1', 'y = 2x - 3'], 'keine'),
    ('Kontrolle faelle F5 (k = 2)', ['2x + y = 1', '4x + 2y = 2'], 'unendlich'),
    ('Sim 4 A, k = -6', ['2x - y = 3', '-4x + 2y = -6'], 'unendlich'),
    ('Sim 4 A, k = 1 (Start)', ['2x - y = 3', '-4x + 2y = 1'], 'keine'),
    ('Sim 4 B, k = 4', ['4x + 2y = 4', '2x + y = 3'], 'keine'),
    ('Sim 4 B, k = 2', ['2x + 2y = 4', '2x + y = 3'], (1, 1)),
    ('Sim 4 B, k = 1 (Start)', ['x + 2y = 4', '2x + y = 3'], (F(2, 3), F(5, 3))),
    ('Sim 4 C, k = 3', ['x + 3y = 3', '3x + 9y = 9'], 'unendlich'),
    ('Sim 4 C, k = -3', ['x - 3y = 3', '-3x + 9y = 9'], 'keine'),
    ('Sim 4 C, k = 1 (Start)', ['x + y = 3', 'x + 9y = 9'], (F(9, 4), F(3, 4))),
    ('Sim 4 C, k = 0', ['x = 3', '9y = 9'], (3, 1)),
    ('4a', ['3x - 2y = 4', '-6x + 4y = 5'], 'keine'),
    ('4b', ['3x - y = 2', '-6x + 2y = -4'], 'unendlich'),
    ('4c(a)', ['y = 3x - 1', 'y = 3x + 2'], 'keine'),
    ('4c(b)', ['2x + 4y = 6', 'x + 2y = 3'], 'unendlich'),
    ('4c(c)', ['x + y = 2', 'x - y = 4'], (3, -1)),
    ('4d, k = -3', ['6x - 3y = -3', '-4x + 2y = 2'], 'unendlich'),
    ('4d, k = 0', ['6x - 3y = 0', '-4x + 2y = 2'], 'keine'),
    ('4e, k = 6', ['6x + 2y = 6', '3x + y = 4'], 'keine'),
    ('4e, k = 0', ['2y = 6', '3x + y = 4'], (F(1, 3), 3)),
    # Kapitel 5
    ('Clip drei / Festhalten 5', ['x + y + z = 6', '2x - y + z = 3', 'x + 2y - z = 2'], (1, 2, 3)),
    ('Kontrolle drei F2', ['x + y + z = 4', '2x - y + 3z = 14', 'x + 2y - z = -3'], (2, -1, 3)),
    ('Kontrolle drei F5 ((1 | 0 | 2) erfüllt (III) nicht)', ['x + y + z = 3', 'x - y + z = 3', '2x + y - z = 1'], (F(4, 3), 0, F(5, 3))),
    ('Kontrolle drei F4', ['x + y + z = 1', 'x + y + z = 4', 'x - y = 0'], 'keine'),
    ('5a', ['x + y + z = 2', '2x + y - z = -2', 'x - 2y + z = 11'], (2, -3, 3)),
    ('5b', ['x + 2y = 7', 'y - z = 1', 'x + z = 4'], (3, 2, 1)),
    ('5c', ['2x - y + z = 5', '3y - z = 4', '2z = 4'], (F(5, 2), 2, 2)),
    ('5d', ['x + y - z = 1', '2x + y + z = 4', '3x + 2y = 7'], 'keine'),
    # Vortest (Gleichungen nach y): als Gleichungen in GL
    # Gesamttest
    ('G1', ['x + 2y = 6', 'x - y = 3'], (4, 1)),
    ('G2', ['0.5x + y = 4', '2x + 4y = 16'], 'unendlich'),
    ('G4', ['x = 4 - y', 'x = 2y - 5'], (1, 3)),
    ('G5', ['3y = 1 - 5x', '2x = 19 + 5y'], (2, -3)),
    ('G6', ['3x + 2y = 8', 'x - 2y = 0'], (2, 1)),
    ('G7, k = 2', ['2x + 4y = 8', 'x + 2y = 4'], 'unendlich'),
    ('G7, k = -2', ['-2x + 4y = 8', 'x - 2y = 4'], 'keine'),
    ('G7, k = 0', ['4y = 8', 'x = 4'], (4, 2)),
    ('G8(b), c = 10', ['x + y + z = 3', '2x - y + z = 8', '3x + 2z = 10'], 'keine'),
    ('G8(b), c = 11', ['x + y + z = 3', '2x - y + z = 8', '3x + 2z = 11'], 'unendlich'),
    ('4f, k = 2', ['2x + y = 2', '4x + 2y = 4'], 'unendlich'),
    ('4f, k = -2', ['-2x + y = 2', '4x - 2y = 4'], 'keine'),
    ('4f, k = 0', ['y = 2', '4x = 4'], (1, 2)),
    ('Clip addition: Subtrahieren', ['2x + 3y = 13', '2x - y = 1'], (2, 3)),
    ('G8', ['x + y + z = 3', '2x - y + z = 8', 'x + 3y = -5'], (1, -2, 4)),
]
# Systeme der Umformer
for sim, aufgaben in umformer.UMFORMER.items():
    for t, A in enumerate(aufgaben, 1):
        art, l_ = system_loesung(A['sys'])
        FEST.append((f'{sim} A{t}', A['sys'], l_ if art == 'eine' else art))

# Einzelne Gleichungen (Vortest, Rückmeldungen), die eine Übung «nach y auflösen» nicht würfeln soll
GL = ['3x + y = 8', '2x - 4y = 6', '4x + 2y = 6', '3x - y = 1']

# Parameterfamilien als Schlüssel der Übung «param-k» (wie T.pk in seite.js)
def pk_konst(a, b, c, t):
    return 'pk|K|' + '|'.join(str(v) for v in norm((a, b, 0, c), 2)) + '|' + ('%g' % t)


def pk_koeff(rd, c1, a2, d, c2):
    return 'pk|C|' + '|'.join('%g' % v for v in (rd, c1, a2, d, c2))


PK = [pk_konst(2, -1, 3, -2),      # Sim 4 A
      pk_koeff(2, 4, 2, 1, 3),     # Sim 4 B
      pk_konst(2, 1, 1, 2),        # Kontrolle faelle F5
      pk_konst(-4, 2, 2, -1.5),    # 4d (k in (I); als Familie mit (II) zuerst)
      pk_koeff(2, 6, 3, 1, 4),     # 4e
      pk_konst(3, -6, 9, F(-1, 3))]  # Clip faelle

# Einzelrechnungen: (Quelle, linke Seite, rechte Seite) — beide Seiten als Zahl auswerten
EINZELN = [
    ('Vortest 0a', '5*5 - 2*(5 + 3)', '9'),
    ('Vortest 0c (1 | 3)', '2*1 + 1', '3'),
    ('Vortest 0d', '-3*5', '-15'),
    ('1e Probe (1 | 2) in (I) ist falsch', '2*1 + 2', '4'),
    ('2c falsch: x = 1.5, y = 3.5 in (II)', '3*1.5 + 2*3.5', '11.5'),
    ('4a 2·(I)+(II) rechts', '2*4 + 5', '13'),
    ('4d 2·(I)+3·(II): 0 = 2k + 6 bei k = -3', '2*(-3) + 6', '0'),
    ('4e: (I) − 2·(II) rechts', '6 - 2*4', '-2'),
    ('Clip faelle: 0 = 9 + 3k bei k = -3', '9 + 3*(-3)', '0'),
    ('G6: Probe der falschen Lösung (4 | 2) in (I)', '3*4 + 2*2', '16'),
    ('Vortest 0c: (3 | −3) auf y = −2x + 3', '-2*3 + 3', '-3'),
    ('G8: Probe (III)', '1 + 3*(-2)', '-5'),
    ('G8: Probe (II)', '2*1 - (-2) + 4', '8'),
    ('Kontrolle drei F3: z aus x + y + z = 4 mit x = 2, y = -1', '4 - 2 - (-1)', '3'),
    ('Kontrolle drei F5: (III) für (1 | 0 | 2)', '2*1 + 0 - 2', '0'),
]
# Behauptete Paare/Tripel, die eine bestimmte Gleichung erfüllen oder nicht (Quelle, Gleichung, Punkt, erfüllt?)
PROBEN = [
    ('Festhalten 1: (5 | 1) erfüllt x − y = 4', 'x - y = 4', (5, 1), True),
    ('Festhalten 1: (5 | 1) erfüllt x + y = 4 nicht', 'x + y = 4', (5, 1), False),
    ('Kontrolle schnittpunkt F1: (1 | 4) erfüllt (I)', '3x + y = 7', (1, 4), True),
    ('Kontrolle schnittpunkt F1: (1 | 4) erfüllt (II) nicht', 'x + y = 4', (1, 4), False),
    ('1e: (1 | 2) auf (II)', 'x - y = -1', (1, 2), True),
    ('1e: (1 | 2) nicht auf (I)', '2x + y = 5', (1, 2), False),
    ('Vortest 0c: (−2 | 1) nicht auf y = 2x + 1', 'y = 2x + 1', (-2, 1), False),
    ('Kontrolle drei F5: (1 | 0 | 2) in (I)', 'x + y + z = 3', (1, 0, 2), True),
    ('Kontrolle drei F5: (1 | 0 | 2) in (II)', 'x - y + z = 3', (1, 0, 2), True),
    ('Kontrolle drei F5: (1 | 0 | 2) nicht in (III)', '2x + y - z = 1', (1, 0, 2), False),
    ('4b: (0 | −2) auf der Geraden', '3x - y = 2', (0, -2), True),
    ('4b: (1 | 1) auf der Geraden', '3x - y = 2', (1, 1), True),
]
# Abgeleitete Gleichungen, die aus einem System folgen müssen (Quelle, System, Gleichung)
FOLGT = [
    ('Clip einsetzen: (II) nach x', ['2x + y = 7', 'x - y = -1'], 'x = y - 1'),
    ('Clip einsetzen', ['2x + y = 7', 'x - y = -1'], '2(y - 1) + y = 7'),
    ('Clip einsetzen', ['2x + y = 7', 'x - y = -1'], '3y = 9'),
    ('Clip einsetzen: Gleichsetzen', ['2x + y = 7', 'x - y = -1'], '7 - 2x = x + 1'),
    ('Clip addition', ['2x + 3y = 12', '5x - 2y = 11'], '4x + 6y = 24'),
    ('Clip addition', ['2x + 3y = 12', '5x - 2y = 11'], '15x - 6y = 33'),
    ('Clip addition', ['2x + 3y = 12', '5x - 2y = 11'], '19x = 57'),
    ('Clip addition: 2x + y = 7, x − y = −1 addiert', ['2x + y = 7', 'x - y = -1'], '3x = 6'),
    ('Clip drei / Festhalten 5: (I) + (III)', ['x + y + z = 6', '2x - y + z = 3', 'x + 2y - z = 2'], '2x + 3y = 8'),
    ('Clip drei / Festhalten 5: (II) + (III)', ['x + y + z = 6', '2x - y + z = 3', 'x + 2y - z = 2'], '3x + y = 5'),
    ('Clip drei: (IV) − 3·(V)', ['x + y + z = 6', '2x - y + z = 3', 'x + 2y - z = 2'], '-7x = -7'),
    ('Clip faelle: (II) − (I)', ['x + y = 3', 'x + y = 5'], '0 = 2'),
    ('Clip faelle: 2·(I) + (II)', ['2x - y = 4', '-4x + 2y = -8'], '0 = 0'),
    ('Kontrolle addition F1: (I) + (II)', ['4x + 3y = 6', '2x - 3y = 12'], '6x = 18'),
    ('Kontrolle addition F2: (I) + 2·(II)', ['x + 4y = 9', '3x - 2y = 13'], '7x = 35'),
    ('Kontrolle addition F3: (I) − (II)', ['5x + 2y = 9', '5x - 3y = -1'], '5y = 10'),
    ('Kontrolle einsetzen F1', ['y = 3x - 4', '2x + y = 6'], '2x + 3x - 4 = 6'),
    ('Kontrolle einsetzen F2', ['x = 2y - 1', '3x + y = 11'], '3(2y - 1) + y = 11'),
    ('Kontrolle drei F1: (I) + (II)', ['x + y + z = 6', 'x - y + 2z = 5'], '2x + 3z = 11'),
    ('Kontrolle drei F2: (I) + (III)', ['x + y + z = 4', '2x - y + 3z = 14', 'x + 2y - z = -3'], '2x + 3y = 1'),
    ('Festhalten 3: 2·(I) + 3·(II)', ['2x + 3y = 12', '5x - 2y = 11'], '19x = 57'),
    ('Festhalten 3 Fehler: 2·(3x − y = 1)', ['3x - y = 1'], '6x - 2y = 2'),
    ('Festhalten 3 Fehler: (5x + 2y) − (5x − 3y)', ['5x + 2y = 9', '5x - 3y = -1'], '5y = 10'),
    ('Festhalten 4: (I) + 3·(II) bei k = -3', ['3x - 6y = 9', '-x + 2y = -3'], '0 = 0'),
    ('2a', ['y = 2x - 5', '4x - 3y = 9'], '4x - 3(2x - 5) = 9'),
    ('2a', ['y = 2x - 5', '4x - 3y = 9'], '-2x = -6'),
    ('2b', ['x = 3y + 4', 'x = -y + 8'], '4y = 4'),
    ('2d', ['3x + y = 5', '5x - 2y = 12'], '11x = 22'),
    ('3b: 2·(I) − (II)', ['2x + 5y = 1', '4x + 3y = 9'], '7y = -7'),
    ('3c: 2·(I) + 3·(II)', ['4x + 3y = 5', '3x - 2y = -9'], '17x = -17'),
    ('3e: (I) + (II)', ['x + y = 5', 'x - y = 1'], '2x = 6'),
    ('4a: 2·(I) + (II)', ['3x - 2y = 4', '-6x + 4y = 5'], '0 = 13'),
    ('4b', ['3x - y = 2', '-6x + 2y = -4'], '0 = 0'),
    ('4e: (I) − 2·(II) bei k = 6', ['6x + 2y = 6', '3x + y = 4'], '0 = -2'),
    ('5a: (I) + (II)', ['x + y + z = 2', '2x + y - z = -2', 'x - 2y + z = 11'], '3x + 2y = 0'),
    ('5a: (II) + (III)', ['x + y + z = 2', '2x + y - z = -2', 'x - 2y + z = 11'], '3x - y = 9'),
    ('5a: (IV) − (V)', ['x + y + z = 2', '2x + y - z = -2', 'x - 2y + z = 11'], '3y = -9'),
    ('5d: (I) + (II)', ['x + y - z = 1', '2x + y + z = 4', '3x + 2y = 7'], '3x + 2y = 5'),
    ('5d: Widerspruch', ['x + y - z = 1', '2x + y + z = 4', '3x + 2y = 7'], '0 = 2'),
    ('G1: Bestätigung, (I) − (II)', ['x + 2y = 6', 'x - y = 3'], '3y = 3'),
    ('G2: 0.5x + y = 4 mal 4 ist (II)', ['0.5x + y = 4', '2x + 4y = 16'], '0 = 0'),
    ('G2: Gerade', ['0.5x + y = 4', '2x + 4y = 16'], 'y = 4 - 0.5x'),
    ('G4: gleichsetzen', ['x = 4 - y', 'x = 2y - 5'], '4 - y = 2y - 5'),
    ('G4', ['x = 4 - y', 'x = 2y - 5'], '3y = 9'),
    ('G8(b): (I) + (II)', ['x + y + z = 3', '2x - y + z = 8'], '3x + 2z = 11'),
    ('4f: k·(I) − (II) bei k = -2', ['-2x + y = 2', '4x - 2y = 4'], '0 = -8'),
    ('Clip addition: (I) − (II)', ['2x + 3y = 13', '2x - y = 1'], '4y = 12'),
    ('G5: geordnet (I)', ['3y = 1 - 5x', '2x = 19 + 5y'], '5x + 3y = 1'),
    ('G5: geordnet (II)', ['3y = 1 - 5x', '2x = 19 + 5y'], '2x - 5y = 19'),
    ('G5: 5·(I) + 3·(II)', ['3y = 1 - 5x', '2x = 19 + 5y'], '31x = 62'),
    ('G6: (I) + (II)', ['3x + 2y = 8', 'x - 2y = 0'], '4x = 8'),
    ('G6: (I) − (II) (Fehlerbeispiel, richtig gerechnet)', ['3x + 2y = 8', 'x - 2y = 0'], '2x + 4y = 8'),
    ('G7: k·(II) − (I) bei k = -2', ['-2x + 4y = 8', 'x - 2y = 4'], '0 = -16'),
    ('G8: (II) − (I)', ['x + y + z = 3', '2x - y + z = 8', 'x + 3y = -5'], 'x - 2y = 5'),
    ('G8: (III) − (IV)', ['x + y + z = 3', '2x - y + z = 8', 'x + 3y = -5'], '5y = -10'),
]
# Gleichungen, die NICHT folgen dürfen (Fehlerbeispiele, falsche Angebote)
FALSCH = [
    ('2c Fehler', ['y = 5 - x', '3x + 2y = 13'], '3x + 10 - x = 13'),
    ('G6 Fehler «2x = 8»', ['3x + 2y = 8', 'x - 2y = 0'], '2x = 8'),
    ('G6 Fehler «x = 4, y = 2» in (I)', ['3x + 2y = 8'], '3*4 + 2*2 = 8'),
    ('Kontrolle einsetzen F2 falsch', ['x = 2y - 1', '3x + y = 11'], '6y - 1 + y = 11'),
    ('Kontrolle addition F3 falsch', ['5x + 2y = 9', '5x - 3y = -1'], '-y = 10'),
    ('Kontrolle addition F1 falsch', ['4x + 3y = 6', '2x - 3y = 12'], '2x = -6'),
]


def ergebnis(sys_):
    art, l_ = system_loesung(sys_)
    return l_ if art == 'eine' else art


def pruefen():
    b = []
    for q, s, soll in FEST:
        ist = ergebnis(s)
        if isinstance(soll, tuple):
            soll = tuple(F(v) for v in soll)
        if ist != soll:
            b.append(f'{q}: behauptet {soll}, gerechnet {ist}')
    for q, l, r in EINZELN:
        if lin(l)[''] != lin(r)['']:
            b.append(f'{q}: {l} = {lin(l)[""]}, nicht {r}')
    for q, g, p, soll in PROBEN:
        if erfuellt([g], p) != soll:
            b.append(f'{q}: falsch')
    for q, s, g in FOLGT:
        if not folgt_aus(s, g):
            b.append(f'{q}: «{g}» folgt nicht')
    for q, s, g in FALSCH:
        if folgt_aus(s, g):
            b.append(f'{q}: «{g}» folgt doch — kein Fehler')
    return b


def sperre():
    sysk = set()
    glk = set(GL)
    for _, s, _ in FEST:
        sysk.add(schl(s))
        n = 3 if any(gl(e)[2] for e in s) else 2
        if n == 3:
            for i in range(len(s)):
                for j in range(i + 1, len(s)):
                    sysk.add(schl([s[i], s[j]], 3))
        else:
            for e in s:
                glk.add(e)
    glk2 = set()
    for e in glk:
        v = gl(e)
        if v[1] != 0:                       # nur Gleichungen, in denen y vorkommt
            glk2.add('|'.join(str(c) for c in norm(v, 2)))
    return {'sys': sorted(sysk), 'gl': sorted(glk2), 'pk': PK}


if __name__ == '__main__':
    b = pruefen()
    b += umformer.pruefen()
    print('\n'.join(b) if b else 'ok: %d Systeme, %d Rechnungen, %d Proben, %d Folgerungen, %d Fehlerbeispiele; Umformer ok'
          % (len(FEST), len(EINZELN), len(PROBEN), len(FOLGT), len(FALSCH)))
    sys.exit(1 if b else 0)
