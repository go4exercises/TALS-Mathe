"""Prüft die Koordinatenbilder der Clips g3-2-lp-* rechnerisch, vor dem Bau.

  python3 scripts/lp/lineare-funktionen/pruef-graf.py

Szene für Szene (HOWTO-clips.md, «Die freie Stelle ausrechnen, nicht schätzen»):
  1. Jeder Punkt liegt im Fenster.
  2. Jede Gerade ist im Fenster sichtbar.
  3. Keine Beschriftung liegt auf einer Geraden, auf einem Punkt, auf einer anderen
     Beschriftung oder auf einer Achsenmarke — und keine ragt aus dem Fenster.
Die Geometrie steht in grafgeom.py und ist dieselbe, mit der clips.py die Stellen setzt.
Exit 1 bei einem Befund.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafgeom import achsenkisten, kiste, masse                     # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
befunde = []


def pruefe(datei):
    d = json.load(open(datei))
    name = d['dateiname']
    for sz in d['szenen']:
        for el in sz['elemente']:
            if el.get('typ') != 'graf':
                continue
            x0, x1, y0, y1, ex, ey = masse(el)
            ger = [(g['m'], g['q']) for g in el.get('geraden', [])]
            pkt = [(p['x'], p['y']) for p in el.get('punkte', [])]

            def melde(t):
                befunde.append(f'{name} · {sz["name"]}: {t}')

            for m, q in ger:
                ys = [m * x0 + q, m * x1 + q]
                if not (any(y0 <= y <= y1 for y in ys) or (min(ys) < y0 and max(ys) > y1)):
                    melde(f'Gerade y = {m}x + {q} liegt ausserhalb des Fensters')
            for x, y in pkt:
                if not (x0 <= x <= x1 and y0 <= y <= y1):
                    melde(f'Punkt ({x} | {y}) liegt ausserhalb des Fensters')

            achsen = achsenkisten(el)
            texte = []
            for g in el.get('geraden', []) + el.get('punkte', []):
                if not g.get('beschriftung'):
                    continue
                bei = g.get('beschriftung_bei')
                if bei is None:
                    bei = [g.get('x', 0) + 18 * ex, g.get('y', 0) - 16 * ey]
                texte.append((g['beschriftung'], bei, g.get('anker', 'start'), g.get('x'), g.get('y')))
            kisten = [(t, kiste(t, b[0], b[1], ank, ex, ey), px_, py_) for t, b, ank, px_, py_ in texte]
            for i, (text, (a, b, u, o), px_, py_) in enumerate(kisten):
                wo = f'«{text}» (Kiste x {a:.2f}…{b:.2f}, y {u:.2f}…{o:.2f})'
                if not (x0 <= a and b <= x1 and y0 <= u and o <= y1):
                    melde(f'Beschriftung {wo} ragt aus dem Fenster')
                for m, q in ger:
                    if max(m * a + q, m * b + q) >= u and min(m * a + q, m * b + q) <= o:
                        melde(f'Beschriftung {wo} liegt auf y = {m}x + {q}')
                for x, y in pkt:
                    if (x, y) != (px_, py_) and a - 0.2 <= x <= b + 0.2 and u - 0.2 <= y <= o + 0.2:
                        melde(f'Beschriftung {wo} liegt auf dem Punkt ({x} | {y})')
                for a2, b2, u2, o2 in achsen:
                    if a < b2 and a2 < b and u < o2 and u2 < o:
                        melde(f'Beschriftung {wo} liegt auf einer Achsenmarke '
                              f'(x {a2:.2f}…{b2:.2f}, y {u2:.2f}…{o2:.2f})')
                for t2, (a2, b2, u2, o2), _, _ in kisten[i + 1:]:
                    if a < b2 and a2 < b and u < o2 and u2 < o:
                        melde(f'Beschriftungen «{text}» und «{t2}» überlappen')


for datei in sorted(glob.glob(R + 'clips/g3-2-lp-*.json')):
    pruefe(datei)

for b in befunde:
    print('[BEFUND]', b)
print(f'\n{len(befunde)} Befund(e).' if befunde else '\nALLE BILDER BESTANDEN')
sys.exit(1 if befunde else 0)
