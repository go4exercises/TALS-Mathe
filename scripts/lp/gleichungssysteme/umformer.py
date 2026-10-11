"""Aufgaben der System-Umformer (Kapitel 2, 3 und 5) — Daten und Prüfung (11.10.2026).

  python3 scripts/lp/gleichungssysteme/umformer.py      # prüft alle Knoten, druckt «ok»

seite.py liest UMFORMER und schreibt es als JSON in die Seite (umformerDaten in seite.js).

Ein Knoten:
  z     Zeile(n) wie im Heft: eine Gleichung (str) oder ein System (Liste); «@» trennt die Beschriftung
        («2x + y = 7 @(I)» → rechts \\text{(I)}). Jede Gleichung wird geprüft: Sie muss aus dem
        Ausgangssystem folgen (Zeilenraum der erweiterten Matrix, lgs.folgt_aus).
  w     Schritte [Knopf, Ziel, Umformung, Hinweis]; Ziel '!Text' = Fehler (rot), '?Text' = erlaubter
        Umweg (grau). Steht im Knopf eines Fehlers eine Gleichung, gehört sie in `falsch` — sie darf
        NICHT aus dem System folgen (sonst wäre der «Fehler» richtig).
  feld  Lücke {muster, soll, tipp, nach, fehler}
  L     Lösung: [x, y] bzw. [x, y, z] (ein Tupel) · [] (leer) — wird gegen das System gerechnet.
"""
from fractions import Fraction as F
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lgs import folgt_aus, system_loesung, erfuellt  # noqa: E402

ODER = r'\;\text{ und }\;'


def S(*zeilen):
    return list(zeilen)


def ein(var, wert, tipp, nach, fehler=None):
    d = {'feld': {'muster': r'\(%s = \) {%s}' % (var, var), 'soll': {var: wert}, 'tipp': tipp, 'nach': nach}}
    if fehler:
        d['feld']['fehler'] = fehler
    return d


def ende(werte, probe):
    namen = 'xyz'[:len(werte)]
    return {'z': [f'{n} = {fz(v)}' for n, v in zip(namen, werte)], 'L': list(werte), 'probe': probe}


def fz(v):
    return ('%g' % v)


TEILEN = '!Dann steht noch eine Zahl vor der Variablen. Um sie wegzubringen, teilst du durch sie.'
FRAGE_EIN = 'Mit welcher Gleichung rechnest du den zweiten Wert aus?'

# ════════════════════════════════════════════════════════════════════ Kapitel 2 · Einsetzen und Gleichsetzen
# Nicht die Beispiele des Clips (2x + y = 7, x − y = −1). Jede Aufgabe ein anderes Muster:
# y steht allein · x steht allein (Klammer!) · beide nach y · beide nach x · erst auflösen · Bruchlösung.
K2 = [
    dict(text=r'Löse mit dem Einsetzverfahren: \(y = 2x - 1\), \(3x + y = 14\).',
         sys=['y = 2x - 1', '3x + y = 14'], k={
        'a': {'z': ['y = 2x - 1 @(I)', '3x + y = 14 @(II)'], 'frage': 'In (I) steht \\(y\\) schon allein. Welcher Schritt?',
              'w': [[r'(I) in (II) einsetzen: \(3x + (2x - 1) = 14\)', 'b', r'\text{(I) in (II)}'],
                    [r'(I) in (I) einsetzen', r'!Dann steht \(2x - 1 = 2x - 1\) da — wahr für jedes \(x\), du hast nichts gewonnen. Der Term aus (I) gehört in die <b>andere</b> Gleichung.'],
                    [r'(II) nach \(x\) auflösen', r'?Erlaubt, aber ein Umweg: In (I) steht \(y\) schon allein. Setze diesen Term in (II) ein.']]},
        'b': {'z': '3x + (2x - 1) = 14',
              'w': [[r'Klammer auflösen: \(5x - 1 = 14\)', 'c'],
                    [r'Klammer auflösen: \(5x + 1 = 14\)', r'!Vor der Klammer steht ein Plus: Die Vorzeichen in der Klammer bleiben, \(+(2x - 1) = 2x - 1\).']],
              'falsch': ['5x + 1 = 14']},
        'c': {'z': '5x - 1 = 14', 'w': [[r'beidseitig \(+1\)', 'd', r'\mid +1'],
                                       [r'beidseitig \(-1\)', r'!Dann steht links \(5x - 2\). Die Gegenoperation zu \(-1\) ist \(+1\).']]},
        'd': {'z': '5x = 15', 'w': [[r'beidseitig \(:5\)', 'e', r'\mid :5'], [r'beidseitig \(-5\)', r'!\(5x\) heisst \(5 \cdot x\): Die Gegenoperation ist \(:5\).']]},
        'e': {'z': 'x = 3', 'frage': FRAGE_EIN,
              'w': [[r'\(x = 3\) in (I) einsetzen', 'f'], [r'\(x = 3\) in (II) einsetzen', 'f2']]},
        'f': ein('y', 5, r'\(y = 2 \cdot 3 - 1\)', 'g'),
        'f2': ein('y', 5, r'\(3 \cdot 3 + y = 14\)', 'g'),
        'g': ende([3, 5], r'3 \cdot 3 + 5 = 14\ \checkmark')}),
    dict(text=r'Löse mit dem Einsetzverfahren: \(x = 2y + 1\), \(3x - 4y = 7\).',
         sys=['x = 2y + 1', '3x - 4y = 7'], k={
        'a': {'z': ['x = 2y + 1 @(I)', '3x - 4y = 7 @(II)'],
              'w': [[r'(I) in (II) einsetzen: \(3(2y + 1) - 4y = 7\)', 'b', r'\text{(I) in (II)}'],
                    [r'(I) in (II) einsetzen: \(3 \cdot 2y + 1 - 4y = 7\)', r'!Der Term \(2y + 1\) ersetzt \(x\) als Ganzes — er gehört in Klammern: \(3 \cdot (2y + 1)\).'],
                    [r'(II) nach \(y\) auflösen', r'?Erlaubt, gibt aber Brüche. In (I) steht \(x\) schon allein: Setze diesen Term in (II) ein.']],
              'falsch': ['3 * 2y + 1 - 4y = 7']},
        'b': {'z': '3(2y + 1) - 4y = 7',
              'w': [[r'Klammer auflösen: \(6y + 3 - 4y = 7\)', 'c'],
                    [r'Klammer auflösen: \(6y + 1 - 4y = 7\)', r'!Die \(3\) multipliziert jedes Glied der Klammer, auch die \(1\): \(3 \cdot 1 = 3\).']],
              'falsch': ['6y + 1 - 4y = 7']},
        'c': {'z': '6y + 3 - 4y = 7', 'w': [[r'zusammenfassen: \(2y + 3 = 7\)', 'd']]},
        'd': {'z': '2y + 3 = 7', 'w': [[r'beidseitig \(-3\)', 'e', r'\mid -3'],
                                      [r'beidseitig \(:2\)', r'?Erlaubt, gibt aber \(y + 1.5 = 3.5\). Einfacher: zuerst \(-3\).']]},
        'e': {'z': '2y = 4', 'w': [[r'beidseitig \(:2\)', 'f', r'\mid :2']]},
        'f': {'z': 'y = 2', 'frage': FRAGE_EIN,
              'w': [[r'\(y = 2\) in (I) einsetzen', 'g'], [r'\(y = 2\) in (II) einsetzen', 'g2']]},
        'g': ein('x', 5, r'\(x = 2 \cdot 2 + 1\)', 'h', [[{'x': 4}, r'\(2 \cdot 2 = 4\), dazu kommt noch \(+1\).']]),
        'g2': ein('x', 5, r'\(3x - 4 \cdot 2 = 7\), also \(3x = 15\)', 'h'),
        'h': ende([5, 2], r'3 \cdot 5 - 4 \cdot 2 = 7\ \checkmark')}),
    dict(text=r'Löse mit dem Gleichsetzverfahren: \(y = 3x - 2\), \(y = -x + 6\).',
         sys=['y = 3x - 2', 'y = -x + 6'], k={
        'a': {'z': ['y = 3x - 2 @(I)', 'y = -x + 6 @(II)'], 'frage': 'Beide Gleichungen sind nach \\(y\\) aufgelöst. Welcher Schritt?',
              'w': [[r'gleichsetzen: \(3x - 2 = -x + 6\)', 'b', r'\text{(I) = (II)}'],
                    [r'gleichsetzen: \(3x - 2 = x + 6\)', r'!Rechts steht \(-x + 6\): Das Minus vor \(x\) gehört dazu.'],
                    [r'addieren: \(2y = 2x + 4\)', r'?Erlaubt, aber keine Variable fällt weg. Beide sind nach \(y\) aufgelöst — setze die rechten Seiten gleich.']],
              'falsch': ['3x - 2 = x + 6']},
        'b': {'z': '3x - 2 = -x + 6', 'w': [[r'beidseitig \(+x\)', 'c', r'\mid +x'],
                                           [r'beidseitig \(-x\)', r'!Dann steht rechts \(-2x + 6\). Um \(-x\) wegzubringen, rechnest du \(+x\).']]},
        'c': {'z': '4x - 2 = 6', 'w': [[r'beidseitig \(+2\)', 'd', r'\mid +2']]},
        'd': {'z': '4x = 8', 'w': [[r'beidseitig \(:4\)', 'e', r'\mid :4']]},
        'e': {'z': 'x = 2', 'frage': FRAGE_EIN, 'w': [[r'\(x = 2\) in (I) einsetzen', 'f'], [r'\(x = 2\) in (II) einsetzen', 'f2']]},
        'f': ein('y', 4, r'\(y = 3 \cdot 2 - 2\)', 'g'),
        'f2': ein('y', 4, r'\(y = -2 + 6\)', 'g', [[{'y': 8}, r'Vorzeichen: \(-x\) mit \(x = 2\) ist \(-2\).']]),
        'g': ende([2, 4], r'3 \cdot 2 - 2 = 4 \text{ und } -2 + 6 = 4\ \checkmark')}),
    dict(text=r'Löse: \(x = 2y + 3\), \(x = -y + 9\).',
         sys=['x = 2y + 3', 'x = -y + 9'], k={
        'a': {'z': ['x = 2y + 3 @(I)', 'x = -y + 9 @(II)'],
              'w': [[r'gleichsetzen: \(2y + 3 = -y + 9\)', 'b', r'\text{(I) = (II)}'],
                    [r'gleichsetzen: \(2y + 3 = y + 9\)', r'!Rechts steht \(-y + 9\): Das Minus vor \(y\) gehört dazu.'],
                    [r'beide nach \(y\) auflösen', r'?Erlaubt, aber unnötig: Beide Gleichungen sind schon nach \(x\) aufgelöst. Setze die rechten Seiten gleich.']],
              'falsch': ['2y + 3 = y + 9']},
        'b': {'z': '2y + 3 = -y + 9', 'w': [[r'beidseitig \(+y\)', 'c', r'\mid +y']]},
        'c': {'z': '3y + 3 = 9', 'w': [[r'beidseitig \(-3\)', 'd', r'\mid -3']]},
        'd': {'z': '3y = 6', 'w': [[r'beidseitig \(:3\)', 'e', r'\mid :3'], [r'beidseitig \(-3\)', TEILEN]]},
        'e': {'z': 'y = 2', 'frage': FRAGE_EIN, 'w': [[r'\(y = 2\) in (I) einsetzen', 'f'], [r'\(y = 2\) in (II) einsetzen', 'f2']]},
        'f': ein('x', 7, r'\(x = 2 \cdot 2 + 3\)', 'g'),
        'f2': ein('x', 7, r'\(x = -2 + 9\)', 'g'),
        'g': ende([7, 2], r'2 \cdot 2 + 3 = 7 \text{ und } -2 + 9 = 7\ \checkmark')}),
    dict(text=r'Löse: \(2x + y = 8\), \(3x - 2y = 5\).',
         sys=['2x + y = 8', '3x - 2y = 5'], k={
        'a': {'z': ['2x + y = 8 @(I)', '3x - 2y = 5 @(II)'], 'frage': 'Keine Variable steht allein. Was zuerst?',
              'w': [[r'(I) nach \(y\) auflösen: \(y = 8 - 2x\)', 'b', r'\text{(I) nach } y'],
                    [r'(I) nach \(y\) auflösen: \(y = 8 + 2x\)', r'!Beim Hinüberbringen dreht das Vorzeichen: \(2x + y = 8 \mid -2x\) gibt \(y = 8 - 2x\).'],
                    [r'(II) nach \(x\) auflösen', r'?Erlaubt, gibt aber Brüche: \(x = \tfrac{5 + 2y}{3}\). In (I) steht vor \(y\) keine Zahl — das geht glatter.']],
              'falsch': ['y = 8 + 2x']},
        'b': {'z': ['y = 8 - 2x @(I)', '3x - 2y = 5 @(II)'],
              'w': [[r'(I) in (II) einsetzen: \(3x - 2(8 - 2x) = 5\)', 'c', r'\text{(I) in (II)}'],
                    [r'(I) in (II) einsetzen: \(3x - 16 - 2x = 5\)', r'!Die \(-2\) multipliziert die ganze Klammer: \(-2 \cdot (-2x) = +4x\).']],
              'falsch': ['3x - 16 - 2x = 5']},
        'c': {'z': '3x - 2(8 - 2x) = 5', 'w': [[r'Klammer auflösen: \(3x - 16 + 4x = 5\)', 'd']]},
        'd': {'z': '3x - 16 + 4x = 5', 'w': [[r'zusammenfassen: \(7x - 16 = 5\)', 'e']]},
        'e': {'z': '7x - 16 = 5', 'w': [[r'beidseitig \(+16\)', 'f', r'\mid +16']]},
        'f': {'z': '7x = 21', 'w': [[r'beidseitig \(:7\)', 'g', r'\mid :7']]},
        'g': {'z': 'x = 3', 'frage': FRAGE_EIN,
              'w': [[r'\(x = 3\) in \(y = 8 - 2x\) einsetzen', 'h'], [r'\(x = 3\) in (II) einsetzen', 'h2']]},
        'h': ein('y', 2, r'\(y = 8 - 2 \cdot 3\)', 'i'),
        'h2': ein('y', 2, r'\(9 - 2y = 5\)', 'i'),
        'i': ende([3, 2], r'2 \cdot 3 + 2 = 8 \text{ und } 9 - 4 = 5\ \checkmark')}),
    dict(text=r'Löse: \(y = x + 1\), \(4x + 2y = 5\).',
         sys=['y = x + 1', '4x + 2y = 5'], k={
        'a': {'z': ['y = x + 1 @(I)', '4x + 2y = 5 @(II)'],
              'w': [[r'(I) in (II) einsetzen: \(4x + 2(x + 1) = 5\)', 'b', r'\text{(I) in (II)}'],
                    [r'(I) in (II) einsetzen: \(4x + 2x + 1 = 5\)', r'!Der Term \(x + 1\) ersetzt \(y\) als Ganzes: \(2 \cdot (x + 1) = 2x + 2\).'],
                    [r'gleichsetzen', r'?Dafür müsstest du zuerst auch (II) nach \(y\) auflösen. In (I) steht \(y\) schon allein — einsetzen ist kürzer.']],
              'falsch': ['4x + 2x + 1 = 5']},
        'b': {'z': '4x + 2(x + 1) = 5', 'w': [[r'Klammer auflösen und zusammenfassen: \(6x + 2 = 5\)', 'c']]},
        'c': {'z': '6x + 2 = 5', 'w': [[r'beidseitig \(-2\)', 'd', r'\mid -2']]},
        'd': {'z': '6x = 3', 'w': [[r'beidseitig \(:6\)', 'e', r'\mid :6'], [r'beidseitig \(:3\)', r'!Dann steht \(2x = 1\) da — noch nicht \(x\) allein. Teile durch die Zahl vor \(x\), also durch \(6\).']]},
        'e': {'z': 'x = 0.5', 'frage': FRAGE_EIN, 'w': [[r'\(x = 0.5\) in (I) einsetzen', 'f'], [r'\(x = 0.5\) in (II) einsetzen', 'f2']]},
        'f': ein('y', F(3, 2), r'\(y = 0.5 + 1\)', 'g'),
        'f2': ein('y', F(3, 2), r'\(2 + 2y = 5\)', 'g'),
        'g': ende([F(1, 2), F(3, 2)], r'1.5 = 0.5 + 1 \text{ und } 2 + 3 = 5\ \checkmark')}),
]

# ════════════════════════════════════════════════════════════════════ Kapitel 3 · Addition und Verfahrenswahl
# Nicht die Beispiele des Clips (2x + y = 7, x − y = −1 und 2x + 3y = 12, 5x − 2y = 11).
K3 = [
    dict(text=r'Löse mit dem Additionsverfahren: \(3x + y = 10\), \(x - y = 2\).',
         sys=['3x + y = 10', 'x - y = 2'], k={
        'a': {'z': ['3x + y = 10 @(I)', 'x - y = 2 @(II)'], 'frage': 'Vor \\(y\\) stehen \\(+1\\) und \\(-1\\). Welcher Schritt?',
              'w': [[r'(I) + (II): \(4x = 12\)', 'b', r'\text{(I) + (II)}'],
                    [r'(I) − (II): \(2x + 2y = 8\)', r'?Erlaubt, aber \(y\) fällt nicht weg: \(y - (-y) = 2y\). Bei \(+y\) und \(-y\) addierst du.'],
                    [r'(I) + (II): \(4x + 2y = 12\)', r'!\(y + (-y) = 0\): Beim Addieren fällt \(y\) weg.']],
              'falsch': ['4x + 2y = 12']},
        'b': {'z': '4x = 12', 'w': [[r'beidseitig \(:4\)', 'c', r'\mid :4']]},
        'c': {'z': 'x = 3', 'frage': FRAGE_EIN, 'w': [[r'\(x = 3\) in (I) einsetzen', 'd'], [r'\(x = 3\) in (II) einsetzen', 'd2']]},
        'd': ein('y', 1, r'\(9 + y = 10\)', 'e'),
        'd2': ein('y', 1, r'\(3 - y = 2\)', 'e', [[{'y': -1}, r'Aus \(3 - y = 2\) folgt \(-y = -1\), also \(y = 1\).']]),
        'e': ende([3, 1], r'9 + 1 = 10 \text{ und } 3 - 1 = 2\ \checkmark')}),
    dict(text=r'Löse: \(2x + 3y = 16\), \(2x - y = 4\).',
         sys=['2x + 3y = 16', '2x - y = 4'], k={
        'a': {'z': ['2x + 3y = 16 @(I)', '2x - y = 4 @(II)'], 'frage': 'Vor \\(x\\) steht beide Male \\(2\\). Welcher Schritt?',
              'w': [[r'(I) − (II): \(4y = 12\)', 'b', r'\text{(I) − (II)}'],
                    [r'(I) − (II): \(2y = 12\)', r'!Vorzeichen: \(3y - (-y) = 3y + y = 4y\).'],
                    [r'(I) + (II): \(4x + 2y = 20\)', r'?Erlaubt, aber keine Variable fällt weg. Bei gleichen Zahlen vor \(x\) subtrahierst du.']],
              'falsch': ['2y = 12']},
        'b': {'z': '4y = 12', 'w': [[r'beidseitig \(:4\)', 'c', r'\mid :4']]},
        'c': {'z': 'y = 3', 'frage': FRAGE_EIN, 'w': [[r'\(y = 3\) in (II) einsetzen', 'd'], [r'\(y = 3\) in (I) einsetzen', 'd2']]},
        'd': ein('x', F(7, 2), r'\(2x - 3 = 4\), also \(2x = 7\)', 'e', [[{'x': F(1, 2)}, r'Aus \(2x - 3 = 4\) folgt \(2x = 7\) — die \(3\) kommt dazu, nicht weg.']]),
        'd2': ein('x', F(7, 2), r'\(2x + 9 = 16\), also \(2x = 7\)', 'e'),
        'e': ende([F(7, 2), 3], r'7 + 9 = 16 \text{ und } 7 - 3 = 4\ \checkmark')}),
    dict(text=r'Löse: \(x + 2y = 5\), \(3x - y = 1\).',
         sys=['x + 2y = 5', '3x - y = 1'], k={
        'a': {'z': ['x + 2y = 5 @(I)', '3x - y = 1 @(II)'], 'frage': 'Noch fällt beim Addieren nichts weg. Was tust du?',
              'w': [[r'(II) mal \(2\): \(6x - 2y = 2\)', 'b', r'\mid \cdot 2 \text{ in (II)}'],
                    [r'(II) mal \(2\): \(6x - 2y = 1\)', r'!Mal \(2\) heisst: <b>beide</b> Seiten, auch die rechte: \(1 \cdot 2 = 2\).'],
                    [r'(I) mal \(3\): \(3x + 6y = 15\)', 'b2', r'\mid \cdot 3 \text{ in (I)}']],
              'falsch': ['6x - 2y = 1']},
        'b': {'z': ['x + 2y = 5 @(I)', r'6x - 2y = 2 @2 \cdot \text{(II)}'],
              'w': [[r'(I) + 2·(II): \(7x = 7\)', 'c', r'\text{(I)} + 2 \cdot \text{(II)}'],
                    [r'(I) − 2·(II): \(-5x + 4y = 3\)', r'?Erlaubt, aber keine Variable fällt weg: \(2y - (-2y) = 4y\). Bei \(+2y\) und \(-2y\) addierst du.']]},
        'b2': {'z': [r'3x + 6y = 15 @3 \cdot \text{(I)}', '3x - y = 1 @(II)'],
               'w': [[r'3·(I) − (II): \(7y = 14\)', 'c2', r'3 \cdot \text{(I)} - \text{(II)}'],
                     [r'3·(I) + (II): \(6x + 5y = 16\)', r'?Erlaubt, aber keine Variable fällt weg. Vor \(x\) steht beide Male \(3\): subtrahieren.']]},
        'c': {'z': '7x = 7', 'w': [[r'beidseitig \(:7\)', 'd', r'\mid :7']]},
        'd': {'z': 'x = 1', 'frage': FRAGE_EIN, 'w': [[r'\(x = 1\) in (I) einsetzen', 'e'], [r'\(x = 1\) in (II) einsetzen', 'e2']]},
        'e': ein('y', 2, r'\(1 + 2y = 5\)', 'f'),
        'e2': ein('y', 2, r'\(3 - y = 1\)', 'f'),
        'c2': {'z': '7y = 14', 'w': [[r'beidseitig \(:7\)', 'd2', r'\mid :7']]},
        'd2': {'z': 'y = 2', 'frage': FRAGE_EIN, 'w': [[r'\(y = 2\) in (I) einsetzen', 'e3'], [r'\(y = 2\) in (II) einsetzen', 'e4']]},
        'e3': ein('x', 1, r'\(x + 4 = 5\)', 'f'),
        'e4': ein('x', 1, r'\(3x - 2 = 1\)', 'f'),
        'f': ende([1, 2], r'1 + 4 = 5 \text{ und } 3 - 2 = 1\ \checkmark')}),
    dict(text=r'Löse: \(3x + 2y = 4\), \(2x - 3y = 7\).',
         sys=['3x + 2y = 4', '2x - 3y = 7'], k={
        'a': {'z': ['3x + 2y = 4 @(I)', '2x - 3y = 7 @(II)'], 'frage': 'Hier musst du beide Gleichungen vervielfachen. Womit?',
              'w': [[r'(I) mal \(3\), (II) mal \(2\) — für \(y\)', 'b', r'\cdot 3,\ \cdot 2'],
                    [r'(I) mal \(2\), (II) mal \(3\) — für \(x\)', 'b2', r'\cdot 2,\ \cdot 3'],
                    [r'(I) mal \(2\), (II) mal \(2\)', r'!Dann stehen \(4y\) und \(-6y\) da — keine Variable fällt weg. Für \(y\) brauchst du ein gemeinsames Vielfaches von \(2\) und \(3\): \(6\).']]},
        'b': {'z': [r'9x + 6y = 12 @3 \cdot \text{(I)}', r'4x - 6y = 14 @2 \cdot \text{(II)}'],
              'w': [[r'addieren: \(13x = 26\)', 'c', r'+'],
                    [r'subtrahieren: \(5x + 12y = -2\)', r'?Erlaubt, aber \(y\) fällt nicht weg: \(6y - (-6y) = 12y\). Bei \(+6y\) und \(-6y\) addierst du.']]},
        'b2': {'z': [r'6x + 4y = 8 @2 \cdot \text{(I)}', r'6x - 9y = 21 @3 \cdot \text{(II)}'],
               'w': [[r'subtrahieren: \(13y = -13\)', 'c2', r'-'],
                     [r'addieren: \(12x - 5y = 29\)', r'?Erlaubt, aber \(x\) fällt nicht weg. Vor \(x\) steht beide Male \(6\): subtrahieren.'],
                     [r'subtrahieren: \(-5y = -13\)', r'!Vorzeichen: \(4y - (-9y) = 4y + 9y = 13y\).']],
               'falsch': ['-5y = -13']},
        'c': {'z': '13x = 26', 'w': [[r'beidseitig \(:13\)', 'd', r'\mid :13']]},
        'd': {'z': 'x = 2', 'frage': FRAGE_EIN, 'w': [[r'\(x = 2\) in (I) einsetzen', 'e'], [r'\(x = 2\) in (II) einsetzen', 'e2']]},
        'e': ein('y', -1, r'\(6 + 2y = 4\), also \(2y = -2\)', 'f', [[{'y': 1}, r'Vorzeichen: \(2y = 4 - 6 = -2\).']]),
        'e2': ein('y', -1, r'\(4 - 3y = 7\), also \(-3y = 3\)', 'f', [[{'y': 1}, r'Vorzeichen: \(-3y = 3\) gibt \(y = -1\).']]),
        'c2': {'z': '13y = -13', 'w': [[r'beidseitig \(:13\)', 'd2', r'\mid :13']]},
        'd2': {'z': 'y = -1', 'frage': FRAGE_EIN, 'w': [[r'\(y = -1\) in (I) einsetzen', 'e3'], [r'\(y = -1\) in (II) einsetzen', 'e4']]},
        'e3': ein('x', 2, r'\(3x - 2 = 4\)', 'f'),
        'e4': ein('x', 2, r'\(2x + 3 = 7\)', 'f'),
        'f': ende([2, -1], r'6 - 2 = 4 \text{ und } 4 + 3 = 7\ \checkmark')}),
    dict(text=r'Löse: \(2y = 11 - 3x\), \(x + y = 5\).',
         sys=['2y = 11 - 3x', 'x + y = 5'], k={
        'a': {'z': ['2y = 11 - 3x @(I)', 'x + y = 5 @(II)'], 'frage': 'Für das Additionsverfahren: Was zuerst?',
              'w': [[r'(I) ordnen: \(3x + 2y = 11\)', 'b', r'\mid +3x \text{ in (I)}'],
                    [r'(I) ordnen: \(-3x + 2y = 11\)', r'!Beim Hinüberbringen dreht das Vorzeichen: \(2y = 11 - 3x \mid +3x\) gibt \(3x + 2y = 11\).'],
                    [r'(I) und (II) gleich addieren', r'?Erlaubt, aber unübersichtlich: In (I) stehen \(x\) und \(y\) auf verschiedenen Seiten. Ordne zuerst, dann stehen gleiche Glieder untereinander.']],
              'falsch': ['-3x + 2y = 11']},
        'b': {'z': ['3x + 2y = 11 @(I)', 'x + y = 5 @(II)'], 'frage': 'Womit vervielfachst du (II)?',
              'w': [[r'(II) mal \(2\): \(2x + 2y = 10\)', 'c', r'\mid \cdot 2 \text{ in (II)}'],
                    [r'(II) mal \(3\): \(3x + 3y = 15\)', 'c2', r'\mid \cdot 3 \text{ in (II)}']]},
        'c': {'z': ['3x + 2y = 11 @(I)', r'2x + 2y = 10 @2 \cdot \text{(II)}'],
              'w': [[r'(I) − 2·(II): \(x = 1\)', 'd', r'\text{(I)} - 2 \cdot \text{(II)}'],
                    [r'(I) + 2·(II): \(5x + 4y = 21\)', r'?Erlaubt, aber \(y\) fällt nicht weg. Vor \(y\) steht beide Male \(2\): subtrahieren.']]},
        'c2': {'z': ['3x + 2y = 11 @(I)', r'3x + 3y = 15 @3 \cdot \text{(II)}'],
               'w': [[r'3·(II) − (I): \(y = 4\)', 'd2', r'3 \cdot \text{(II)} - \text{(I)}']]},
        'd': {'z': 'x = 1', 'frage': FRAGE_EIN, 'w': [[r'\(x = 1\) in (II) einsetzen', 'e']]},
        'e': ein('y', 4, r'\(1 + y = 5\)', 'f'),
        'd2': {'z': 'y = 4', 'frage': FRAGE_EIN, 'w': [[r'\(y = 4\) in (II) einsetzen', 'e2']]},
        'e2': ein('x', 1, r'\(x + 4 = 5\)', 'f'),
        'f': ende([1, 4], r'2 \cdot 4 = 8 = 11 - 3 \text{ und } 1 + 4 = 5\ \checkmark')}),
    dict(text=r'Wähle ein Verfahren und löse: \(y = 2x - 3\), \(y = -x + 9\).',
         sys=['y = 2x - 3', 'y = -x + 9'], k={
        'a': {'z': ['y = 2x - 3 @(I)', 'y = -x + 9 @(II)'], 'frage': 'Welches Verfahren passt hier am besten?',
              'w': [[r'Gleichsetzen: \(2x - 3 = -x + 9\)', 'b', r'\text{(I) = (II)}'],
                    [r'Additionsverfahren', r'?Geht, aber zuerst müsstest du beide Gleichungen ordnen. Beide sind schon nach \(y\) aufgelöst — setze gleich.'],
                    [r'grafisch', r'?Ein Bild hilft zum Überblick, liefert aber nur eine Schätzung. Rechne exakt: Beide sind nach \(y\) aufgelöst.']]},
        'b': {'z': '2x - 3 = -x + 9', 'w': [[r'beidseitig \(+x\)', 'c', r'\mid +x'], [r'beidseitig \(-x\)', r'!Dann steht rechts \(-2x + 9\). Um \(-x\) wegzubringen, rechnest du \(+x\).']]},
        'c': {'z': '3x - 3 = 9', 'w': [[r'beidseitig \(+3\)', 'd', r'\mid +3']]},
        'd': {'z': '3x = 12', 'w': [[r'beidseitig \(:3\)', 'e', r'\mid :3']]},
        'e': {'z': 'x = 4', 'frage': FRAGE_EIN, 'w': [[r'\(x = 4\) in (I) einsetzen', 'f'], [r'\(x = 4\) in (II) einsetzen', 'f2']]},
        'f': ein('y', 5, r'\(y = 2 \cdot 4 - 3\)', 'g'),
        'f2': ein('y', 5, r'\(y = -4 + 9\)', 'g'),
        'g': ende([4, 5], r'8 - 3 = 5 \text{ und } -4 + 9 = 5\ \checkmark')}),
]

# ════════════════════════════════════════════════════════════════════ Kapitel 5 · drei Variablen
# Nicht das Beispiel des Clips (x + y + z = 6, 2x − y + z = 3, x + 2y − z = 2).
K5 = [
    dict(text=r'Löse das System in Stufenform: \(x + y + z = 7\), \(y - z = 1\), \(z = 2\).',
         sys=['x + y + z = 7', 'y - z = 1', 'z = 2'], k={
        'a': {'z': ['x + y + z = 7 @(I)', 'y - z = 1 @(II)', 'z = 2 @(III)'], 'frage': 'Unten steht nur noch \\(z\\). Womit beginnst du?',
              'w': [[r'\(z = 2\) in (II) einsetzen: \(y - 2 = 1\)', 'b', r'\text{in (II)}'],
                    [r'\(z = 2\) in (I) einsetzen: \(x + y + 2 = 7\)', r'?Erlaubt, aber dann stehen noch zwei Unbekannte da. In (II) fehlt \(x\) — dort bekommst du sofort \(y\).'],
                    [r'(I) + (II): \(x + 2y = 8\)', r'?Erlaubt, aber unnötig: \(z\) ist schon bekannt. Setze von unten nach oben ein.']]},
        'b': {'z': 'y - 2 = 1', 'w': [[r'beidseitig \(+2\)', 'c', r'\mid +2'], [r'beidseitig \(-2\)', r'!Dann steht links \(y - 4\). Die Gegenoperation zu \(-2\) ist \(+2\).']]},
        'c': {'z': 'y = 3', 'frage': 'Jetzt kennst du \\(y\\) und \\(z\\). Wohin damit?',
              'w': [[r'in (I) einsetzen: \(x + 3 + 2 = 7\)', 'd', r'\text{in (I)}'],
                    [r'in (II) einsetzen', r'?Erlaubt, gibt aber nur \(3 - 2 = 1\) — das weisst du schon. In (II) kommt \(x\) nicht vor; nur (I) enthält noch \(x\).']]},
        'd': {'z': 'x + 3 + 2 = 7', 'w': [[r'beidseitig \(-5\)', 'e', r'\mid -5']]},
        'e': ende([2, 3, 2], r'2 + 3 + 2 = 7;\ \ 3 - 2 = 1;\ \ z = 2\ \checkmark')}),
    dict(text=r'Löse: \(x + y + z = 6\), \(x - y + z = 4\), \(2x + y - z = 2\).',
         sys=['x + y + z = 6', 'x - y + z = 4', '2x + y - z = 2'], k={
        'a': {'z': ['x + y + z = 6 @(I)', 'x - y + z = 4 @(II)', '2x + y - z = 2 @(III)'], 'frage': 'Welchen ersten Schritt wählst du?',
              'w': [[r'(I) − (II): \(2y = 2\) — \(x\) und \(z\) fallen zugleich weg', 'b', r'\text{(I) − (II)}'],
                    [r'(I) + (III): \(3x + 2y = 8\) — \(z\) fällt weg', 'b2', r'\text{(I) + (III)}'],
                    [r'(I) + (II): \(2x + 2z = 10\)', r'?Erlaubt: \(y\) fällt weg. Schneller geht es mit (I) − (II) — dann fallen \(x\) und \(z\) zugleich weg.']]},
        'b': {'z': '2y = 2', 'w': [[r'beidseitig \(:2\)', 'c', r'\mid :2']]},
        'c': {'z': 'y = 1', 'frage': 'Wohin mit \\(y = 1\\)?',
              'w': [[r'in (I) und (III): \(x + z = 5\) und \(2x - z = 1\)', 'd', r'\text{in (I), (III)}'],
                    [r'nur in (I): \(x + z = 5\)', r'?Erlaubt, aber eine Gleichung mit zwei Unbekannten reicht nicht. Setze \(y = 1\) auch in (III) ein — dann hast du ein 2×2-System.']]},
        'd': {'z': ['x + z = 5 @(IV)', '2x - z = 1 @(V)'],
              'w': [[r'(IV) + (V): \(3x = 6\)', 'e', r'\text{(IV) + (V)}'],
                    [r'(IV) − (V): \(-x + 2z = 4\)', r'?Erlaubt, aber \(x\) fällt nicht weg. Vor \(z\) stehen \(+1\) und \(-1\): addieren.']]},
        'e': {'z': '3x = 6', 'w': [[r'beidseitig \(:3\)', 'f', r'\mid :3']]},
        'f': {'z': 'x = 2', 'frage': 'Noch fehlt \\(z\\).', 'w': [[r'\(x = 2\) in (IV) einsetzen', 'g']]},
        'g': ein('z', 3, r'\(2 + z = 5\)', 'h'),
        'b2': {'z': ['3x + 2y = 8 @(IV)'], 'frage': 'Für ein 2×2-System brauchst du eine zweite Gleichung ohne \\(z\\).',
               'w': [[r'(II) + (III): \(3x = 6\)', 'b3', r'\text{(II) + (III)}'],
                     [r'(I) + (II): \(2x + 2z = 10\)', r'!Hier bleibt \(z\) stehen. Gesucht ist eine Gleichung, in der \(z\) wegfällt: Vor \(z\) stehen in (II) \(+1\) und in (III) \(-1\).']],
               'falsch': []},
        'b3': {'z': ['3x + 2y = 8 @(IV)', '3x = 6 @(V)'], 'w': [[r'(V) durch \(3\): \(x = 2\)', 'b4', r'\mid :3 \text{ in (V)}']]},
        'b4': {'z': 'x = 2', 'w': [[r'\(x = 2\) in (IV) einsetzen', 'b5']]},
        'b5': ein('y', 1, r'\(6 + 2y = 8\)', 'b6'),
        'b6': ein('z', 3, r'in (I): \(2 + 1 + z = 6\)', 'h'),
        'h': ende([2, 1, 3], r'2 + 1 + 3 = 6;\ \ 2 - 1 + 3 = 4;\ \ 4 + 1 - 3 = 2\ \checkmark')}),
    dict(text=r'Löse: \(2x + y - z = 3\), \(x - y + 2z = 8\), \(x + 2y + z = 3\).',
         sys=['2x + y - z = 3', 'x - y + 2z = 8', 'x + 2y + z = 3'], k={
        'a': {'z': ['2x + y - z = 3 @(I)', 'x - y + 2z = 8 @(II)', 'x + 2y + z = 3 @(III)'], 'frage': 'Welche Variable eliminierst du?',
              'w': [[r'\(z\): \(2 \cdot\)(I) + (II) und (I) + (III)', 'b', r'z \text{ weg}'],
                    [r'\(y\): (I) + (II) und \(2 \cdot\)(II) + (III)', 'c', r'y \text{ weg}'],
                    [r'\(z\): (I) + (II) und (I) + (III)', r'!Vor \(z\) stehen in (I) \(-1\) und in (II) \(+2\): (I) + (II) gibt \(3x + z = 11\) — \(z\) bleibt. Nimm \(2 \cdot\)(I) + (II).']],
              'falsch': []},
        'b': {'z': ['5x + y = 14 @(IV)', '3x + 3y = 6 @(V)'],
              'w': [[r'(V) durch \(3\): \(x + y = 2\)', 'b1', r'\mid :3 \text{ in (V)}'],
                    [r'\(3 \cdot\)(IV) − (V): \(12x = 36\)', 'b2', r'3 \cdot \text{(IV)} - \text{(V)}']]},
        'b1': {'z': ['5x + y = 14 @(IV)', 'x + y = 2 @(V)'],
               'w': [[r'(IV) − (V): \(4x = 12\)', 'b3', r'\text{(IV) − (V)}'],
                     [r'(IV) + (V): \(6x + 2y = 16\)', r'?Erlaubt, aber \(y\) fällt nicht weg. Vor \(y\) steht beide Male \(1\): subtrahieren.']]},
        'b3': {'z': '4x = 12', 'w': [[r'beidseitig \(:4\)', 'x3', r'\mid :4']]},
        'b2': {'z': '12x = 36', 'w': [[r'beidseitig \(:12\)', 'x3', r'\mid :12']]},
        'x3': {'z': 'x = 3', 'frage': 'Jetzt \\(y\\), dann \\(z\\).', 'w': [[r'\(x = 3\) in (IV) einsetzen', 'y1']]},
        'y1': ein('y', -1, r'\(15 + y = 14\)', 'z1', [[{'y': 1}, r'\(y = 14 - 15 = -1\).']]),
        'z1': ein('z', 2, r'in (III): \(3 - 2 + z = 3\)', 'e'),
        'c': {'z': ['3x + z = 11 @(IV)', '3x + 5z = 19 @(V)'],
              'w': [[r'(V) − (IV): \(4z = 8\)', 'c1', r'\text{(V) − (IV)}'],
                    [r'(V) + (IV): \(6x + 6z = 30\)', r'?Erlaubt, aber nichts fällt weg. Vor \(x\) steht beide Male \(3\): subtrahieren.']]},
        'c1': {'z': '4z = 8', 'w': [[r'beidseitig \(:4\)', 'c2', r'\mid :4']]},
        'c2': {'z': 'z = 2', 'frage': 'Jetzt \\(x\\), dann \\(y\\).', 'w': [[r'\(z = 2\) in (IV) einsetzen', 'c3']]},
        'c3': ein('x', 3, r'\(3x + 2 = 11\)', 'c4'),
        'c4': ein('y', -1, r'in (I): \(6 + y - 2 = 3\)', 'e'),
        'e': ende([3, -1, 2], r'6 - 1 - 2 = 3;\ \ 3 + 1 + 4 = 8;\ \ 3 - 2 + 2 = 3\ \checkmark')}),
    dict(text=r'Löse: \(x + y + z = 4\), \(x - y + z = 2\), \(2x + 2z = 5\).',
         sys=['x + y + z = 4', 'x - y + z = 2', '2x + 2z = 5'], k={
        'a': {'z': ['x + y + z = 4 @(I)', 'x - y + z = 2 @(II)', '2x + 2z = 5 @(III)'], 'frage': 'In (III) fehlt \\(y\\). Welcher Schritt?',
              'w': [[r'(I) + (II): \(2x + 2z = 6\) — \(y\) fällt weg', 'b', r'\text{(I) + (II)}'],
                    [r'(I) − (II): \(2y = 2\)', 'b2', r'\text{(I) − (II)}'],
                    [r'(I) + (II): \(2x + 2y + 2z = 6\)', r'!\(y + (-y) = 0\): Beim Addieren fällt \(y\) weg.']],
              'falsch': []},
        'b': {'z': ['2x + 2z = 6 @(IV)', '2x + 2z = 5 @(III)'],
              'w': [[r'(IV) − (III): \(0 = 1\)', 'c', r'\text{(IV) − (III)}'],
                    [r'(IV) + (III): \(4x + 4z = 11\)', r'?Erlaubt, aber nichts fällt weg. Links steht zweimal dasselbe: subtrahieren.']]},
        'b2': {'z': '2y = 2', 'w': [[r'beidseitig \(:2\)', 'b3', r'\mid :2']]},
        'b3': {'z': 'y = 1', 'w': [[r'\(y = 1\) in (I) einsetzen: \(x + z = 3\)', 'b4', r'\text{in (I)}']]},
        'b4': {'z': ['x + z = 3 @(IV)', '2x + 2z = 5 @(III)'],
               'w': [[r'\(2 \cdot\)(IV) − (III): \(0 = 1\)', 'c', r'2 \cdot \text{(IV)} - \text{(III)}']]},
        'c': {'z': '0 = 1', 'frage': 'Alle Variablen sind weg. Was bedeutet das?',
              'w': [[r'Widerspruch: keine Lösung', 'd'],
                    [r'immer wahr: unendlich viele Lösungen', r'!\(0 = 1\) ist falsch, egal welche Zahlen man einsetzt.'],
                    [r'\(x = 0\) und \(z = 1\)', r'!In \(0 = 1\) steht keine Variable mehr — es ist eine Aussage, und sie ist falsch.']]},
        'd': {'L': [], 'frage': 'Gib die Lösungsmenge an:'}}),
]

UMFORMER = {'sim2': K2, 'sim3': K3, 'sim5': K5}


def _gleichungen(z):
    zs = z if isinstance(z, list) else [z]
    return [s.split('@')[0].strip() for s in zs]


def pruefen():
    befunde = []
    for sim, aufgaben in UMFORMER.items():
        for t, A in enumerate(aufgaben, 1):
            sys_ = A['sys']
            art, loes = system_loesung(sys_)
            for kid, K in A['k'].items():
                if 'z' in K:
                    for g in _gleichungen(K['z']):
                        if not folgt_aus(sys_, g):
                            befunde.append(f'{sim} A{t} {kid}: «{g}» folgt nicht aus dem System')
                for g in K.get('falsch', []):
                    if folgt_aus(sys_, g):
                        befunde.append(f'{sim} A{t} {kid}: Fehler «{g}» ist in Wahrheit richtig')
                if 'L' in K:
                    if K['L'] == []:
                        if art != 'keine':
                            befunde.append(f'{sim} A{t}: L leer, System hat {art}')
                    else:
                        if art != 'eine' or tuple(F(v) for v in K['L']) != loes:
                            befunde.append(f'{sim} A{t}: L {K["L"]} ≠ {art} {loes}')
                if 'feld' in K:
                    # Lücke: der Sollwert muss zur Lösung passen
                    for var, v in K['feld']['soll'].items():
                        if art == 'eine' and loes['xyz'.index(var)] != F(v):
                            befunde.append(f'{sim} A{t} {kid}: Lücke {var} = {v}, Lösung {loes}')
    return befunde


def als_json():
    def wandle(o):
        if isinstance(o, F):
            return float(o)
        if isinstance(o, dict):
            return {k: wandle(v) for k, v in o.items() if k not in ('falsch',)}
        if isinstance(o, list):
            return [wandle(v) for v in o]
        return o

    aus = {}
    for sim, aufgaben in UMFORMER.items():
        L = []
        for A in aufgaben:
            k = {}
            for kid, K in A['k'].items():
                K2_ = dict(K)
                if 'z' in K2_:
                    K2_['z'] = tex_zeile(K2_['z'])
                k[kid] = wandle(K2_)
            L.append({'text': A['text'], 'k': k})
        aus[sim] = L
    return json.dumps(aus, ensure_ascii=False)


def tex_zeile(z):
    def eine(s):
        g, _, lab = s.partition('@')
        g = g.strip().replace('*', r'\cdot ')
        if lab.strip():
            l_ = lab.strip()
            l_ = l_ if '\\' in l_ else r'\text{' + l_ + '}'
            return g + r' & ' + l_
        return g
    if isinstance(z, list):
        if len(z) == 1:
            return eine(z[0]).replace(' & ', r' \qquad ')
        return r'\begin{cases} ' + r' \\ '.join(eine(s) for s in z) + r' \end{cases}'
    return eine(z)


if __name__ == '__main__':
    b = pruefen()
    print('\n'.join(b) if b else 'ok: alle Umformer-Knoten folgen aus ihrem System, Lösungen stimmen')
    sys.exit(1 if b else 0)
