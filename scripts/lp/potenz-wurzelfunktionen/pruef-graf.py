"""Prüft die Koordinatenbilder der Clips s3-2-lp-* rechnerisch, vor dem Bau.

  python3 scripts/lp/potenz-wurzelfunktionen/pruef-graf.py

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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/lp/grafgeom.py
from grafgeom import achsenkisten, kiste, masse                     # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
befunde = []


def pot(b, p):
    """Wie BEWEGUNG_JS rechnet: ungerader Wurzelexponent darf eine negative Basis haben,
    gerader nicht — sonst sieht der Pruefer die linke Haelfte einer Kubikwurzel nicht."""
    if b >= 0 or float(p).is_integer():
        return b ** p
    q = round(1 / p)
    return -((-b) ** p) if abs(1 / p - q) < 1e-9 and q % 2 else None


def pruefe(datei):
    d = json.load(open(datei))
    name = d['dateiname']
    for sz in d['szenen']:
        for el in sz['elemente']:
            if el.get('typ') != 'graf':
                continue
            x0, x1, y0, y1, ex, ey = masse(el)
            ger = [(g['m'], g['q']) for g in el.get('geraden', []) if 'm' in g]
            pkt = [(p['x'], p['y']) for p in el.get('punkte', [])]

            def melde(t):
                befunde.append(f'{name} · {sz["name"]}: {t}')

            for m, q in ger:
                ys = [m * x0 + q, m * x1 + q]
                if not (any(y0 <= y <= y1 for y in ys) or (min(ys) < y0 and max(ys) > y1)):
                    melde(f'Gerade y = {m}x + {q} liegt ausserhalb des Fensters')

            # Bewegte Kurven y = a*(x-u)^p + v: in jedem Stuetzpunkt muss ein Stueck
            # der Kurve im Fenster liegen, sonst zeigt die Szene nichts.
            for kv in el.get('kurven', []):
                if not kv.get('bewegung'):
                    continue
                vx, bx = max(x0, kv.get('von', x0)), min(x1, kv.get('bis', x1))
                for st in kv['bewegung']:
                    t, a_, p_, u_, v_ = st
                    sicht = 0
                    for i in range(241):
                        x = vx + (bx - vx) * i / 240
                        try:
                            y = a_ * pot(x - u_, p_) + v_
                        except Exception:
                            continue
                        if y is None or isinstance(y, complex) or y != y:
                            continue
                        if y0 <= y <= y1:
                            sicht += 1
                    if sicht < 5:
                        melde(f'bewegte Kurve bei t = {t}: y = {a_}·(x−{u_})^{p_}+{v_} ist (fast) nicht im Bild')

            # Bewegte Geraden: jeder Stuetzpunkt muss ein Bild ergeben, und das
            # mitlaufende Steigungsdreieck muss zu jeder Zeit im Fenster liegen —
            # sonst blendet der Abspieler es einfach aus, und die Szene zeigt nichts.
            for g in el.get('geraden', []):
                if not g.get('bewegung'):
                    continue
                for t, m, q in g['bewegung']:
                    ys = [m * x0 + q, m * x1 + q]
                    if not (any(y0 <= y <= y1 for y in ys) or (min(ys) < y0 and max(ys) > y1)):
                        melde(f'bewegte Gerade bei t = {t}: y = {m}x + {q} ist nicht im Bild')
                dr = g.get('dreieck')
                if not dr:
                    continue
                ecken = dr['bahn'] if dr.get('bahn') else [[0, dr['x'], dr['dx']]]
                for _, m, q in g['bewegung']:
                    for _, xa, dxx in ecken:
                        for x in (xa, xa + dxx):
                            y = m * x + q
                            if not (x0 <= x <= x1 and y0 <= y <= y1):
                                melde(f'Steigungsdreieck: Ecke ({x} | {y:g}) bei y = {m}x + {q} '
                                      f'liegt ausserhalb des Fensters')
            for x, y in pkt:
                if not (x0 <= x <= x1 and y0 <= y <= y1):
                    melde(f'Punkt ({x} | {y}) liegt ausserhalb des Fensters')

            achsen = achsenkisten(el)
            # Begleiter bewegter Kurven (startpunkt, marken) schreiben ihre Koordinaten an.
            # Der Abspieler setzt sie zur Laufzeit, darum stehen sie in keiner punkte-Liste —
            # und bis zum 03.10.2026 sah der Pruefer sie nicht. Sie koennen auf einer
            # Achsenmarke landen, und in einer klick-Frage verraten sie das Ziel.
            def bewzahl(x):
                """Wie bewZahl() im Abspieler: eine Nachkommastelle, echtes Minus."""
                r = round(x * 10) / 10
                return ('\u2212' if r < 0 else '') + ('%g' % abs(r))

            begleiter = {}
            for kv in el.get('kurven', []):
                b = kv.get('bewegung')
                if not b:
                    continue
                for st in b:
                    _, a_, p_, u_, v_ = st
                    if kv.get('startpunkt') and kv['startpunkt'].get('beschriftung', True) is not False:
                        t_ = '(%s | %s)' % (bewzahl(u_), bewzahl(v_))
                        begleiter[(t_, u_, v_)] = True
                    for mk in kv.get('marken', []):
                        y_ = pot(mk['x'] - u_, p_)
                        if y_ is None:
                            continue
                        y_ = a_ * y_ + v_
                        txt = str(mk.get('text', '')).replace('{x}', bewzahl(mk['x'])).replace('{y}', bewzahl(y_))
                        if txt:
                            begleiter[(txt, mk['x'], y_)] = True
            begleiter = list(begleiter)

            achsen = achsen
            texte = []
            for g in el.get('geraden', []) + el.get('punkte', []):
                if not g.get('beschriftung'):
                    continue
                bei = g.get('beschriftung_bei')
                if bei is None:
                    bei = [g.get('x', 0) + 18 * ex, g.get('y', 0) - 16 * ey]
                texte.append((g['beschriftung'], bei, g.get('anker', 'start'), g.get('x'), g.get('y')))
            kisten = [(t, kiste(t, b[0], b[1], ank, ex, ey), px_, py_) for t, b, ank, px_, py_ in texte]
            # Der Abspieler setzt den Begleitertext 18 px rechts und 44 px unter den Punkt
            # (bei a > 0; siehe beschrifte() in BEWEGUNG_JS) — dieselbe Lage hier nachbauen.
            for txt, bx, by in begleiter:
                if not (x0 <= bx <= x1 and y0 <= by <= y1):
                    melde(f'Begleiter «{txt}» sitzt bei ({bx:g} | {by:g}) ausserhalb des Fensters')
                    continue
                # beschrifte() in BEWEGUNG_JS: im rechten Drittel linksbuendig ans Zeichen,
                # sonst rechts daneben; senkrecht 44 px darunter (a > 0) bzw. 18 px darueber.
                rechts = bx > x1 - (x1 - x0) * 0.3
                lx = bx + (-18 if rechts else 18) * ex
                # Sitzt der Begleiter auf der x-Achse, weicht der Abspieler nach oben aus
                # (dort stehen die x-Marken) — dieselbe Regel wie in beschrifte().
                nah = abs(by) < 40 * ey
                a_, b_, u_, o_ = kiste(txt, lx, by + (18 if nah else -44) * ey,
                                       'end' if rechts else 'start', ex, ey)
                # Saum von 4 px: Der Abspieler setzt den Begleiter zur Laufzeit, und
                # Klammern reichen tiefer als das pauschale TIEF-Mass. Ohne den Saum
                # verfehlte der Pruefer «(2 | 0)» auf der Achsenmarke «3» um einen Pixel.
                kisten.append((txt, (a_ - 4 * ex, b_ + 4 * ex, u_ - 4 * ey, o_ + 4 * ey), bx, by))
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


def pruefe_fragen(datei):
    """Ziel und Fallen einer klick-Frage muessen im Fenster ihrer Szene liegen —
    sonst kann niemand sie treffen."""
    d = json.load(open(datei))
    for F in d.get('fragen', []):
        if F.get('typ') != 'klick':
            continue
        sz = next((q for q in d['szenen'] if q['name'] == F['szene']), None)
        if sz is None:
            befunde.append(f"{d['dateiname']}: Frage verweist auf unbekannte Szene {F['szene']}")
            continue
        el = next((e for e in sz['elemente'] if e.get('typ') == 'graf'), None)
        if el is None:
            befunde.append(f"{d['dateiname']} · {F['szene']}: klick-Frage ohne graf")
            continue
        if not (any(g.get('bewegung') for g in el.get('geraden', []))
                or any(k.get('bewegung') for k in el.get('kurven', []))):
            befunde.append(f"{d['dateiname']} · {F['szene']}: klick-Frage ohne bewegte Gerade oder Kurve "
                           f"(der Abspieler braucht deren data-fenster)")
        if el.get('ein', 0.05) > F.get('bei', 0.3):
            befunde.append(f"{d['dateiname']} · {F['szene']}: Bild erscheint erst bei "
                           f"{el.get('ein')} s, die klick-Frage steht schon bei {F.get('bei')} s")
        x0, x1 = el['xbereich']
        y0, y1 = el['ybereich']
        for name, p in [('Ziel', F['ziel'])] + [('Falle', f_['bei']) for f_ in F.get('fallen', [])]:
            if not (x0 <= p[0] <= x1 and y0 <= p[1] <= y1):
                befunde.append(f"{d['dateiname']} · {F['szene']}: {name} {p} liegt ausserhalb des Fensters")
        tol = F.get('toleranz', 0.5)
        for f_ in F.get('fallen', []):
            d_ = ((f_['bei'][0] - F['ziel'][0]) ** 2 + (f_['bei'][1] - F['ziel'][1]) ** 2) ** 0.5
            if d_ <= tol:
                befunde.append(f"{d['dateiname']} · {F['szene']}: Falle {f_['bei']} liegt innerhalb "
                               f"der Toleranz {tol} um das Ziel — sie wird nie erreicht")


for datei in sorted(glob.glob(R + 'clips/s3-2-lp-*.json')):
    pruefe(datei)
    pruefe_fragen(datei)

for b in befunde:
    print('[BEFUND]', b)
print(f'\n{len(befunde)} Befund(e).' if befunde else '\nALLE BILDER BESTANDEN')
sys.exit(1 if befunde else 0)
