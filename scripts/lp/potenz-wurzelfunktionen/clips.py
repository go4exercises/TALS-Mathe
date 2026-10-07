"""Erzeugt die zehn Drehbücher des Leitprogramms Potenz- und Wurzelfunktionen (03.10.2026).

  python3 scripts/lp/potenz-wurzelfunktionen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie beim Vorbild: Bild rechts (x 1010, y 175, 760 × 760), Formeln und Notizen
links (x 150), Theme begreifbar-schlicht.

**Bewegte Kurven** (HOWTO-clips.md «Bewegte Parabel und Gerade»): Stützpunkte
`[t, a, p, u, v]` für y = a·(x−u)^p + v. Damit gehen Parabeln n-ter Ordnung, Hyperbeln
(p < 0) und Wurzelkurven (p = 1/n) mit demselben Schlüssel; `stufen` rundet p beim
Überblenden auf ganze Zahlen, `spiegel` zeigt die Kurve an y = x gespiegelt — die
Umkehrfunktion —, und `von`/`bis` schränken sie ein, damit sie überhaupt umkehrbar wird.

Farben — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15). Abgeleitet von beiden
Themenseiten, wo der Exponent orange gesetzt ist:
  1 blau   = die Potenzkurve und ihr Faktor a        \\fa{…}
  2 orange = der Exponent n                          \\fb{…}
  3 grün   = Wurzelkurve, Umkehrfunktion, Startpunkt \\fc{…}
  4 rot    = Gegenbeispiel, Polstelle, verbotener Bereich \\fd{…}
  5 Tinte  = neutral: gemeinsame Punkte, Asymptoten, Bezugskurve

Fenster: wo Spiegelung an y = x zu sehen ist, sind beide Spannen gleich — sonst sähe
die Winkelhalbierende nicht wie 45° aus und die Spiegelung wäre keine.
"""
import json
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))   # scripts/lp/fragebild.py
from fragebild import anwenden as anwenden_fragebild   # noqa: E402
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/lp/grafgeom.py

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150

from grafgeom import achsenkisten, frei, kiste, masse       # noqa: E402


def stelle(text, x, y, geraden, punkte, W, belegt):
    x0, x1, y0, y1, ex, ey = masse(W)
    dx, dy = 0.26 * (x1 - x0) / 9, 0.5 * (y1 - y0) / 9
    for k in (1, 1.6, 2.4, 3.4):
        for ax, ay, anker in ((1, -1, 'start'), (1, 1, 'start'), (-1, -1, 'end'), (-1, 1, 'end')):
            lx, ly = x + ax * dx, y + ay * dy * k
            kk = kiste(text, lx, ly, anker, ex, ey)
            if frei(kk, geraden, punkte, belegt, W, (x, y)):
                belegt.append(kk)
                return [round(lx, 3), round(ly, 3)], anker
    raise SystemExit('[FEHLER] keine freie Stelle fuer «%s» bei (%s | %s) im Fenster %s' % (text, x, y, W))


def graf(W, kurven=(), geraden=(), punkte=(), ein=0.05, **kw):
    ger_l = [(g['m'], g['q']) for g in geraden if 'm' in g]
    pkt_l = [(p['x'], p['y']) for p in punkte]
    belegt = achsenkisten(dict(W, **{k: v for k, v in kw.items() if k in ('xname', 'yname')}))
    for p in punkte:
        if p.get('beschriftung') and 'beschriftung_bei' not in p:
            p['beschriftung_bei'], p['anker'] = stelle(p['beschriftung'], p['x'], p['y'],
                                                       ger_l, pkt_l, W, belegt)
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=list(geraden), punkte=list(punkte), pfeile=True, **W)
    g.update(kw)
    return g


def kurve(stuetz, farbe=1, stufen=False, spiegel=None, startpunkt=None, asymptoten=None,
          marken=None, von=None, bis=None, gestrichelt=False, dicke=None):
    """Bewegte Potenz- oder Wurzelkurve: Stuetzpunkte [t, a, p, u, v] fuer a*(x-u)^p + v."""
    d = {'bewegung': stuetz, 'farbe': farbe}
    if stufen:
        d['stufen'] = True
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    for k, v in (('spiegel', spiegel), ('startpunkt', startpunkt), ('asymptoten', asymptoten),
                 ('marken', marken)):
        if v is not None:
            d[k] = v
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


def ger(m, q, farbe=5, gestrichelt=True, dicke=None):
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    return d


def pt(x, y, farbe=5, text=None):
    d = dict(x=x, y=y, farbe=farbe, anker='start')
    if text:
        d['beschriftung'] = text
    return d


def f(t, y, g=62, ein=0.8):
    return dict(typ='formel', text=t, x=LX, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=46, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=86):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))


def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3):
    """Die richtige Antwort steht nicht immer zuoberst.

    Stuende sie in jeder Wahlfrage an Position 0, liesse sich jede ohne Nachdenken
    ueber die erste Schaltflaeche loesen (Befund der externen Pruefung am Leitprogramm
    Lineare Funktionen, 03.10.2026). Die Drehung ist deterministisch aus Szene und
    Fragetext; Rueckmeldungen und Tondateien wandern mit, weil sie nach dem Drehen aus
    dem Drehbuch erzeugt werden.
    """
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % len(opt)
    dreh = lambda i: (i - k) % len(opt)                 # alter Index -> neuer Index
    opt = [opt[(i + k) % len(opt)] for i in range(len(opt))]
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': dreh(richtig), 'rueck': {str(dreh(i)): v for i, v in rueck.items()}}
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(dreh(i)): v for i, v in rueck_sprich.items()}
    return d


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None,
          tol=0.6, bei=0.3, eingabe=('x', 'y')):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    if eingabe:
        d['eingabe'] = list(eingabe)   # Antwort ohne Zeigegeraet: zwei Zahlfelder (build-clips.py)
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/s3-2-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 's3-2-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Potenz und Wurzel',
         'fach': 'Schwerpunktfach', 'lerngebiet': '3 · Funktionen',
         'lektion': ['s3-2a', 's3-2b'], 'stufe': ['BM2'], 'datum': '2026-10-03',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Kurve sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms potenz-wurzelfunktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    anwenden_fragebild(d)                               # beim Fragen nur das Gegebene
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# Fenster — überall quadratisch, damit die Spiegelung an y = x eine Spiegelung bleibt
W = dict(xbereich=[-3, 3], ybereich=[-3, 3])
W5 = dict(xbereich=[-4, 5], ybereich=[-4, 5])
W_SP = dict(xbereich=[-2, 5], ybereich=[-2, 5])
W_H = dict(xbereich=[-3, 6], ybereich=[-4, 5])

W_ZK = dict(xbereich=[-3, 3], ybereich=[-9, 9],          # «Zwei Kurven»: (−2 | −8) muss ins Bild
            yteilung=[[-8, '−8'], [-6, '−6'], [-4, '−4'], [-2, '−2'], [2, '2'], [4, '4'], [6, '6'], [8, '8']])

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('exponent', 'Kurve sehen: der Exponent formt den Graphen',
     'Parabeln n-ter Ordnung — wie der Exponent die Form bestimmt und seine Parität die Symmetrie.',
     ['Potenzfunktion', 'Exponent', 'Parabel n-ter Ordnung', 'Symmetrie', 'gerade Funktion'], [
         sz('Zwei Kurven',
            'Zwei Potenzfunktionen, dieselbe Bauart: y gleich x Quadrat und y gleich x hoch drei. '
            'In der Wertetabelle sieht man den Unterschied sofort — bei minus zwei steht einmal vier, '
            'einmal minus acht.',
            titel('Zwei Kurven', 280, 80),
            f(r'\begin{array}{c|ccccc} x & -2 & -1 & 0 & 1 & 2 \\ \hline x^2 & 4 & 1 & 0 & 1 & 4 \\ x^3 & -8 & -1 & 0 & 1 & 8 \end{array}',
              430, 42, ein=5.6),
            # Bild zum Satz (Ton: «x Quadrat» 2.9, «x hoch drei» 4.3, «vier» 10.6, «minus acht» 11.5); y bis ±9,
            # damit (−2 | 4) und (−2 | −8) im Bild liegen
            graf(W_ZK, [kurve([[0, 1, 2, 0, 0]], farbe=1)], ein=2.9),
            graf(W_ZK, [kurve([[0, 1, 3, 0, 0]], farbe=1, gestrichelt=True)], ein=4.3, raster=False),
            # Beschriftung von Hand: rechts oberhalb bzw. unterhalb, wo die Kurven nicht verlaufen
            # (x² bei −1.8: 3.24; x³ bei −1.8: −5.83)
            graf(W_ZK, punkte=[dict(pt(-2, 4, 5, '(−2 | 4)'), beschriftung_bei=[-1.8, 4.9])], ein=10.6, raster=False),
            graf(W_ZK, punkte=[dict(pt(-2, -8, 5, '(−2 | −8)'), beschriftung_bei=[-1.8, -8.3])], ein=11.5, raster=False)),
         sz('n wächst',
            'Lassen wir den Exponenten wachsen: von zwei über drei und vier bis fünf. '
            'Zwischen minus eins und eins wird die Kurve flacher, aussen steiler. '
            'Und ein Punkt bleibt, wo er ist: eins, eins.',
            f(r'y = x^{\fb{n}}, \quad \fb{n} = 2 \to 5', 300, 62),
            n('grösseres @\\fb{n}@: innen flacher,|aussen steiler', 440, 'orange'),
            graf(W, [kurve([[0, 1, 2, 0, 0]], farbe=5, gestrichelt=True),      # Bezugskurve y = x², wie in sim1
                     kurve([[0.9, 1, 2, 0, 0], [4.4, 1, 5, 0, 0]], stufen=True,
                           marken=[{'x': 1, 'text': '(1 | {y})', 'farbe': 5}])])),
         sz('Gemeinsame Punkte',
            'Alle diese Kurven gehen durch null, null und durch eins, eins. '
            'Bei minus eins trennen sie sich: gerade Exponenten landen bei plus eins, ungerade bei minus eins.',
            f(r'(0 \mid 0), \quad (1 \mid 1)', 300, 62),
            n('bei @x = -1@:|gerades @\\fb{n} \\to +1@, ungerades @\\fb{n} \\to -1@', 440, 'blau'),
            graf(W, [kurve([[0, 1, 2, 0, 0]], farbe=1), kurve([[0, 1, 3, 0, 0]], farbe=1, gestrichelt=True)],
                 punkte=[pt(0, 0, 5, '(0 | 0)'), pt(1, 1, 5, '(1 | 1)'),
                         pt(-1, 1, 5, '(−1 | 1)'), pt(-1, -1, 5, '(−1 | −1)')])),
         sz('Gerade Funktion',
            'Gerades n heisst: f von minus x ist gleich f von x. Der Graph ist achsensymmetrisch zur y-Achse. '
            'Bei x hoch vier liegen minus eins und eins beide auf der Höhe eins.',
            f(r'f(-x) = f(x) \quad (\fb{n} \text{ gerade})', 300, 56),
            n('achsensymmetrisch|zur @y@-Achse', 440, 'blau'),
            # Sprung 2 → 4 in 0.08 s vor «heisst f von minus x» (Ton 1.0–1.7): x³ steht nie im Bild
            graf(W, [kurve([[0.8, 1, 2, 0, 0], [0.88, 1, 4, 0, 0]], stufen=True)],
                 punkte=[pt(-1, 1, 5, '(−1 | 1)'), pt(1, 1, 5, '(1 | 1)')])),
         sz('Ungerade Funktion',
            'Ungerades n heisst: f von minus x ist gleich minus f von x. Der Graph ist punktsymmetrisch zum Ursprung. '
            'Bei x hoch fünf liegt minus eins bei minus eins, eins bei plus eins.',
            f(r'f(-x) = -f(x) \quad (\fb{n} \text{ ungerade})', 300, 54),
            n('punktsymmetrisch|zum Ursprung', 440, 'blau'),
            # Sprung 3 → 5 in 0.08 s vor «f von minus x» (Ton 1.6): x⁴ steht nie im Bild
            graf(W, [kurve([[0.8, 1, 3, 0, 0], [0.88, 1, 5, 0, 0]], stufen=True)],
                 punkte=[pt(-1, -1, 5, '(−1 | −1)'), pt(1, 1, 5, '(1 | 1)')])),
         sz('a streckt',
            'Und a? a streckt die Kurve in y-Richtung. Zwei macht sie schmaler, null Komma fünf breiter. '
            'Ein negatives a klappt sie an der x-Achse um.',
            f(r'y = \fa{a} \cdot x^{\fb{3}}', 300, 66),
            n('@|\\fa{a}| \\gt 1@: schmaler; @|\\fa{a}| \\lt 1@: breiter|@\\fa{a} \\lt 0@: an der @x@-Achse gespiegelt',
              440, 'blau'),
            graf(W, [kurve([[3.4, 1, 3, 0, 0], [4.6, 2, 3, 0, 0], [5.9, 0.5, 3, 0, 0], [8.8, -1, 3, 0, 0]],
                           marken=[{'x': 1, 'text': '(1 | {y})', 'farbe': 5}])])),   # (1 | a): a ablesbar
         sz('Merke',
            'Zum Mitnehmen: Der Exponent n bestimmt die Form, seine Parität die Symmetrie — gerade heisst '
            'Achsensymmetrie, ungerade Punktsymmetrie. Alle Kurven gehen durch eins, eins. Und a streckt '
            'in y-Richtung; ein negatives a spiegelt an der x-Achse.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a} \cdot x^{\fb{n}}, \quad \fa{a},\, \fb{n} \neq 0', 410, 58, ein=0.4),
            n('@\\fb{n}@ gerade: Achsensymmetrie|@\\fb{n}@ ungerade: Punktsymmetrie|alle durch @(1 \\mid 1)@',
              540, 'blau', 44, ein=1.2),
            graf(W, [kurve([[0.8, 1, 2, 0, 0], [3.6, 1, 5, 0, 0]], stufen=True)],
                 punkte=[pt(1, 1, 5, '(1 | 1)')])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-exponent', 'Kurve sehen: Kontrollfragen zum Exponenten',
     'Fünf Vorhersagen zu Form, Symmetrie und gemeinsamen Punkten der Potenzfunktionen.',
     ['Potenzfunktion', 'Exponent', 'Symmetrie', 'Kontrollfragen'], [
         sz('Frage 1',
            'Vier ist gerade, also ist die Funktion gerade: achsensymmetrisch zur y-Achse. '
            'Minus zwei und zwei liefern denselben Wert, nämlich sechzehn.',
            f(r'(-2)^{\fb{4}} = 16 = 2^{\fb{4}}', 300, 62, ein=1.0),
            n('gerades @\\fb{n}@:|@f(-x) = f(x)@', 440, 'blau', ein=2.4),
            graf(dict(xbereich=[-3, 3], ybereich=[-2, 4]),
                 [kurve([[0.9, 1, 2, 0, 0], [3.4, 1, 4, 0, 0]], stufen=True)],
                 punkte=[pt(-1, 1, 5), pt(1, 1, 5)])),
         sz('Frage 2',
            'Minus zwei hoch fünf ist minus zweiunddreissig. Der Exponent ist ungerade, also bleibt das Minus stehen.',
            f(r'(-2)^{\fb{5}} = -32', 300, 66, ein=1.0),
            n('ungerades @\\fb{n}@:|das Minus bleibt', 440, 'blau', ein=2.2),
            graf(W, [kurve([[0.9, 1, 3, 0, 0], [3.4, 1, 5, 0, 0]], stufen=True)],
                 punkte=[pt(-1, -1, 5), pt(1, 1, 5)])),
         sz('Frage 3',
            'Alle Potenzfunktionen mit dem Faktor eins gehen durch eins, eins — ganz gleich, wie gross der Exponent ist. '
            'Eins hoch irgendetwas bleibt eins.',
            f(r'1^{\fb{n}} = 1 \quad \text{für jedes } \fb{n}', 300, 58, ein=1.2),
            n('@(1 \\mid 1)@ liegt auf|jeder dieser Kurven', 440, 'blau', ein=2.6),
            # Keine Marke: Sie schriebe «(1 | 1)» an — also genau das Klickziel (§15).
            graf(W, [kurve([[0.9, 1, 2, 0, 0], [3.8, 1, 5, 0, 0]], stufen=True)])),
         sz('Frage 4',
            'Das Minus steht vor der Potenz, nicht in der Klammer. Minus zwei hoch vier ist also minus sechzehn — '
            'erst potenzieren, dann das Vorzeichen.',
            f(r'-2^{\fb{4}} = -(2^{\fb{4}}) = \fd{-16}', 300, 56, ein=1.0),
            n('@(-2)^4 = 16@, aber @-2^4 = -16@|Die Klammer entscheidet.', 440, 'rot', ein=2.4),
            graf(dict(xbereich=[-3, 3], ybereich=[-4, 2]),
                 [kurve([[0, -1, 4, 0, 0]], farbe=1)], ein=1.2)),
         sz('Frage 5',
            'Minus eins Komma fünf mal x hoch drei: Das Minus klappt die Kurve an der x-Achse um, '
            'und eins Komma fünf macht sie schmaler. Sie fällt also von links oben nach rechts unten.',
            f(r'y = \fa{-1.5} \cdot x^{\fb{3}}', 300, 64, ein=1.4),
            n('@\\fa{a} \\lt 0@: an der @x@-Achse gespiegelt|@|\\fa{a}| \\gt 1@: schmaler', 440, 'blau', ein=2.8),
            graf(W, [kurve([[0, -1.5, 3, 0, 0]])])),
         sz('Merke',
            'Zum Mitnehmen: Die Parität des Exponenten entscheidet über die Symmetrie. Alle Kurven mit dem '
            'Faktor eins gehen durch eins, eins. Und die Klammer entscheidet, ob ein Minus mitpotenziert wird.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'(-x)^{\fb{n}} = (-1)^{\fb{n}} \cdot x^{\fb{n}}', 410, 58, ein=0.4),
            n('gerade: Achse; ungerade: Punkt|alle durch @(1 \\mid 1)@|@(-2)^4 \\neq -2^4@',
              540, 'blau', 44, ein=1.2),
            graf(W, [kurve([[0, 1, 4, 0, 0]], farbe=1)], punkte=[pt(1, 1, 5, '(1 | 1)')])),
     ], [
         wahl('Frage 1', 'f(x) = x⁴: Wie liegen f(−2) und f(2) zueinander?',
              ['beide 16 — der Graph ist achsensymmetrisch', 'f(−2) = −16, f(2) = 16',
               'f(−2) = 16, f(2) = −16'], 0,
              {0: 'Ja.',
               1: 'Wie viele Minuszeichen multiplizierst du bei (−2)⁴ miteinander?',
               2: 'Schau auf 2⁴ allein: Kann eine gerade Potenz einer positiven Zahl negativ sein?'},
              sprich='f von x gleich x hoch vier: Wie liegen f von minus zwei und f von zwei zueinander?',
              rueck_sprich={1: 'Wie viele Minuszeichen multiplizierst du bei minus zwei hoch vier miteinander?',
                            2: 'Schau auf zwei hoch vier allein: Kann eine gerade Potenz einer positiven Zahl negativ sein?'}),
         wahl('Frage 2', 'Wie gross ist (−2)⁵?',
              ['−32', '32', '−10'], 0,
              {0: 'Ja.',
               1: 'Zähl die Faktoren: Ist der Exponent gerade oder ungerade?',
               2: 'Potenzieren ist kein Multiplizieren mit dem Exponenten.'},
              sprich='Wie gross ist minus zwei in Klammern, hoch fünf?',
              rueck_sprich={1: 'Zähl die Faktoren: Ist der Exponent gerade oder ungerade?',
                            2: 'Potenzieren ist kein Multiplizieren mit dem Exponenten.'}),
         klick('Frage 3', 'Durch welchen Punkt gehen alle Kurven y = xⁿ gemeinsam — ausser dem Ursprung? '
                          'Tipp ihn ins Bild.',
               [1, 1], 'Getroffen: (1 | 1).',
               [{'bei': [-1, 1], 'text': 'Nur die geraden Exponenten treffen diesen Punkt, die ungeraden nicht.',
                 'sprich': 'Nur die geraden Exponenten treffen diesen Punkt, die ungeraden nicht.'},
                {'bei': [-1, -1], 'text': 'Nur die ungeraden Exponenten treffen diesen Punkt.',
                 'sprich': 'Nur die ungeraden Exponenten treffen diesen Punkt.'},
                {'bei': [2, 2], 'text': 'Rechne nach: Ist 2ⁿ für jedes n gleich 2?',
                 'sprich': 'Rechne nach: Ist zwei hoch n für jedes n gleich zwei?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — welche Zahl bleibt beim Potenzieren sie selbst?',
               sprich='Durch welchen Punkt gehen alle Kurven y gleich x hoch n gemeinsam, ausser dem Ursprung? '
                      'Tipp ihn ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Welche Zahl bleibt beim Potenzieren sie selbst?'),
         wahl('Frage 4', 'Wie gross ist −2⁴ (ohne Klammer um die −2)?',
              ['−16', '16', '−8'], 0,
              {0: 'Ja.',
               1: 'Steht das Minus innerhalb oder ausserhalb der Potenz?',
               2: 'Rechne 2⁴ zuerst aus, bevor du das Vorzeichen setzt.'},
              sprich='Wie gross ist minus zwei hoch vier, ohne Klammer um die minus zwei?',
              rueck_sprich={1: 'Steht das Minus innerhalb oder ausserhalb der Potenz?',
                            2: 'Rechne zwei hoch vier zuerst aus, bevor du das Vorzeichen setzt.'}),
         wahl('Frage 5', 'Welche Gleichung gehört zur Kurve im Bild?',
              ['y = −1.5x³', 'y = 1.5x³', 'y = −1.5x²'], 0,
              {0: 'Ja.',
               1: 'Steigt die Kurve von links nach rechts, oder fällt sie?',
               2: 'Schau auf die Symmetrie: Liegt der linke Ast oben oder unten?'},
              rueck_sprich={1: 'Steigt die Kurve von links nach rechts, oder fällt sie?',
                            2: 'Schau auf die Symmetrie: Liegt der linke Ast oben oder unten?'}),
     ], art='Kontrollclip')

W_HY = dict(xbereich=[-4, 4], ybereich=[-4, 4])

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
clip('hyperbel', 'Kurve sehen: negative Exponenten geben Hyperbeln',
     'Was bei n kleiner null geschieht — zwei Äste, eine Definitionslücke und zwei Asymptoten.',
     ['Hyperbel', 'negativer Exponent', 'Asymptote', 'Polstelle', 'Definitionsmenge'], [
         sz('Ein neuer Fall',
            'Was geschieht bei einem negativen Exponenten? x hoch minus eins ist eins durch x. '
            'Bei zwei ergibt das ein Halb, bei einem Halb zwei — je grösser x, desto kleiner y.',
            titel('Eins durch x', 280, 80),
            f(r'y = x^{\fb{-1}} = \dfrac{1}{x}', 440, 62, ein=4.6),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]])],
                 punkte=[pt(2, 0.5, 5, '(2 | 0.5)'), pt(0.5, 2, 5, '(0.5 | 2)')], ein=6.4)),
         sz('Bei null ist Schluss',
            'An der Stelle null gibt es keinen Wert — man müsste durch null teilen. '
            'Die Kurve zerfällt in zwei Äste, und die Definitionsmenge ist die reellen Zahlen ohne null.',
            f(r'D = \mathbb{R} \setminus \{0\}', 300, 64),
            n('@x = \\fd{0}@ ist eine Definitionslücke —|hier eine Polstelle', 440, 'rot'),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]], asymptoten={'farbe': 4})])),
         sz('Asymptoten',
            'Die beiden Achsen sind Asymptoten: Die Äste schmiegen sich an sie an, berühren sie aber nie. '
            'Eins durch x gleich null hat keine Lösung, so gross x auch wird.',
            f(r'x = 0 \quad \text{und} \quad y = 0', 300, 58),
            n('beliebig nahe,|aber nie erreicht', 440, 'blau'),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]], asymptoten={'farbe': 4},
                              marken=[{'x': 3.5, 'text': '{y}', 'farbe': 5}])])),
         sz('Die Ordnung wächst',
            'Jetzt wächst die Ordnung: von eins über zwei und drei bis vier — der Exponent geht dabei '
            'von minus eins auf minus vier. Die Äste springen zwischen diagonal und beide oben, '
            'und wieder entscheidet die Parität.',
            f(r'y = x^{-\fb{n}}, \quad \fb{n} = 1 \to 4', 300, 58),
            n('ungerade Ordnung: diagonal|gerade Ordnung: beide oben', 440, 'orange'),
            graf(W_HY, [kurve([[0.9, 1, -1, 0, 0], [4.6, 1, -4, 0, 0]], stufen=True)])),
         sz('Gerade Ordnung',
            'Bei gerader Ordnung, etwa eins durch x Quadrat, sind beide Äste oberhalb der x-Achse. '
            'Die Funktion ist gerade, der Graph achsensymmetrisch — und alle Werte sind positiv.',
            f(r'y = \dfrac{1}{x^{\fb{2}}}, \quad W = \mathbb{R}^+', 300, 58),
            n('achsensymmetrisch,|beide Äste oben', 440, 'blau'),
            graf(W_HY, [kurve([[0, 1, -2, 0, 0]], asymptoten={'farbe': 4})],   # rot wie sonst: Tinte deckt sich mit den Achsen
                 punkte=[pt(-1, 1, 5, '(−1 | 1)'), pt(1, 1, 5, '(1 | 1)')])),
         sz('Keine Nullstelle',
            'Eines haben alle Hyperbeln gemeinsam: Sie haben keine Nullstelle. Ein Bruch mit Zähler eins '
            'wird nie null. Und durch eins, eins gehen sie trotzdem alle.',
            f(r'\dfrac{1}{x^{\fb{n}}} = 0 \quad \text{hat keine Lösung}', 300, 52),
            n('keine Nullstelle —|aber alle durch @(1 \\mid 1)@', 440, 'blau'),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]], farbe=1), kurve([[0, 1, -2, 0, 0]], farbe=1, gestrichelt=True)],
                 punkte=[pt(1, 1, 5, '(1 | 1)')])),
         sz('Merke',
            'Zum Mitnehmen: Der Exponent minus n gibt eine Hyperbel n-ter Ordnung. Die Definitionsmenge ist die '
            'reellen Zahlen ohne null, die Achsen sind Asymptoten, eine Nullstelle gibt es nicht. '
            'Gerade Ordnung heisst beide Äste oben, ungerade heisst diagonal.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = x^{\fb{-n}} = \dfrac{1}{x^{\fb{n}}}, \quad D = \mathbb{R} \setminus \{0\}', 410, 54, ein=0.4),
            n('Asymptoten @x = 0@ und @y = 0@|keine Nullstelle|gerade: oben; ungerade: diagonal',
              540, 'blau', 44, ein=1.2),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]], asymptoten={'farbe': 4})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-hyperbel', 'Kurve sehen: Kontrollfragen zu den Hyperbeln',
     'Fünf Vorhersagen zu Definitionsmenge, Ästen, Asymptoten und Werten der Hyperbeln.',
     ['Hyperbel', 'Definitionsmenge', 'Asymptote', 'Kontrollfragen'], [
         sz('Frage 1',
            'x hoch minus zwei ist eins durch x Quadrat. Bei null müsste man durch null teilen — '
            'die Definitionsmenge ist die reellen Zahlen ohne null.',
            f(r'D = \mathbb{R} \setminus \{0\}', 300, 64, ein=1.0),
            n('nur die eine Stelle fehlt —|sonst ist alles erlaubt', 440, 'blau', ein=2.4),
            graf(W_HY, ein=1.0, kurven=[kurve([[0.9, 1, -1, 0, 0], [3.4, 1, -2, 0, 0]], stufen=True,
                              asymptoten={'farbe': 5})])),
         sz('Frage 2',
            'Drei ist ungerade, also liegen die Äste diagonal: einer rechts oben, einer links unten. '
            'Für negative x ist auch der Wert negativ.',
            f(r'y = \dfrac{1}{x^{\fb{3}}}', 300, 64, ein=1.0),
            n('ungerade Ordnung:|rechts oben, links unten', 500, 'blau', ein=2.4),
            graf(W_HY, [kurve([[0, 1, -3, 0, 0]], asymptoten={'farbe': 5})], ein=1.2)),
         sz('Frage 3',
            'Eingesetzt: eins durch minus zwei ist minus ein Halb. Der Punkt liegt auf dem linken Ast, '
            'unterhalb der x-Achse.',
            f(r'f(-2) = \dfrac{1}{-2} = -0.5', 300, 58, ein=1.2),
            n('negatives @x@, ungerade Ordnung:|negativer Wert', 440, 'blau', ein=2.8),
            # Der Punkt darf erst nach der Antwort stehen, und die Kurve ist die aus der
            # Frage — eine verschobene hiesse nicht mehr @y = 1/x@.
            graf(W_HY, [kurve([[0.9, 1, -1, 0, 0], [3.4, 1, -1, 0, 0]], asymptoten={'farbe': 5})])),
         sz('Frage 4',
            'Die Hyperbel erreicht die x-Achse nie: Eins durch x gleich null hat keine Lösung. '
            'Je grösser x wird, desto näher kommt der Wert der null — aber ein Abstand bleibt immer.',
            f(r'\dfrac{1}{x} = 0 \;\Longrightarrow\; \text{keine Lösung}', 300, 52, ein=1.0),
            n('beliebig nahe,|aber nie null', 440, 'blau', ein=2.4),
            graf(W_HY, [kurve([[0, 1, -1, 0, 0]], asymptoten={'farbe': 5},
                              marken=[{'x': 3.6, 'text': '{y}', 'farbe': 5}])], ein=1.2)),
         sz('Frage 5',
            'Beide Äste liegen oben, die Kurve ist achsensymmetrisch — das ist eine gerade Ordnung. '
            'Gezeichnet ist eins durch x Quadrat, also x hoch minus zwei.',
            f(r'y = x^{\fb{-2}} = \dfrac{1}{x^{\fb{2}}}', 300, 60, ein=1.6),
            n('beide Äste oben @\\Rightarrow@|gerade Ordnung', 440, 'blau', ein=2.8),
            graf(W_HY, [kurve([[0, 1, -2, 0, 0]], asymptoten={'farbe': 5})])),
         sz('Merke',
            'Zum Mitnehmen: Bei negativem Exponenten fehlt die Stelle null, die Achsen sind Asymptoten, '
            'und eine Nullstelle gibt es nicht. Die Parität der Ordnung sagt, wo die Äste liegen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'D = \mathbb{R} \setminus \{0\}, \quad \text{keine Nullstelle}', 410, 52, ein=0.4),
            n('gerade Ordnung: beide Äste oben|ungerade Ordnung: diagonal|@(1 \\mid 1)@ liegt auf jeder',
              540, 'blau', 44, ein=1.2),
            graf(W_HY, [kurve([[0, 1, -2, 0, 0]], asymptoten={'farbe': 5})],
                 punkte=[pt(1, 1, 5, '(1 | 1)')])),
     ], [
         wahl('Frage 1', 'f(x) = x⁻²: Welche Definitionsmenge hat die Funktion?',
              ['ℝ \\ {0}', 'ℝ', 'ℝ⁺'], 0,
              {0: 'Ja.',
               1: 'Schreib x⁻² als Bruch und schau, welche Zahl im Nenner verboten ist.',
               2: 'Darf x negativ sein? Rechne f(−2) aus.'},
              sprich='f von x gleich x hoch minus zwei: Welche Definitionsmenge hat die Funktion?',
              rueck_sprich={1: 'Schreib x hoch minus zwei als Bruch und schau, welche Zahl im Nenner verboten ist.',
                            2: 'Darf x negativ sein? Rechne f von minus zwei aus.'}),
         wahl('Frage 2', 'y = 1/x³: Wo liegen die beiden Äste?',
              ['rechts oben und links unten', 'beide oberhalb der x-Achse', 'beide unterhalb der x-Achse'], 0,
              {0: 'Ja.',
               1: 'Setz x = −1 ein: Welches Vorzeichen hat der Wert?',
               2: 'Setz x = 1 ein: Welches Vorzeichen hat der Wert?'},
              sprich='y gleich eins durch x hoch drei: Wo liegen die beiden Äste?',
              rueck_sprich={1: 'Setz x gleich minus eins ein: Welches Vorzeichen hat der Wert?',
                            2: 'Setz x gleich eins ein: Welches Vorzeichen hat der Wert?'}),
         klick('Frage 3', 'y = 1/x: Tipp den Punkt des Graphen bei x = −2 ins Bild.',
               [-2, -0.5], 'Getroffen: (−2 | −0.5).',
               [{'bei': [-2, 0.5], 'text': 'Die Höhe stimmt, das Vorzeichen nicht: 1 geteilt durch −2.',
                 'sprich': 'Die Höhe stimmt, das Vorzeichen nicht: eins geteilt durch minus zwei.'},
                {'bei': [-2, -2], 'text': 'Das wäre y = x. Hier ist y der Kehrwert von x.',
                 'sprich': 'Das wäre y gleich x. Hier ist y der Kehrwert von x.'},
                {'bei': [-0.5, -2], 'text': 'Koordinaten vertauscht: Gefragt ist die Stelle x = −2.',
                 'sprich': 'Die Koordinaten sind vertauscht: Gefragt ist die Stelle x gleich minus zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — rechne 1 geteilt durch −2.',
               sprich='y gleich eins durch x: Tipp den Punkt des Graphen bei x gleich minus zwei ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Rechne eins geteilt durch minus zwei.'),
         wahl('Frage 4', 'Warum erreicht y = 1/x die x-Achse nie?',
              ['weil 1/x = 0 keine Lösung hat', 'weil x nicht null sein darf',
               'weil die Kurve zu steil ist'], 0,
              {0: 'Ja.',
               1: 'Das stimmt, erklärt aber die andere Asymptote. Hier geht es um die Werte, nicht um die Stellen.',
               2: 'Die Steilheit entscheidet nicht. Setz y = 0 und schau, ob die Gleichung lösbar ist.'},
              sprich='Warum erreicht y gleich eins durch x die x-Achse nie?',
              rueck_sprich={1: 'Das stimmt, erklärt aber die andere Asymptote. Hier geht es um die Werte, nicht um die Stellen.',
                            2: 'Die Steilheit entscheidet nicht. Setz y gleich null und schau, ob die Gleichung lösbar ist.'}),
         wahl('Frage 5', 'Welche Gleichung gehört zur Kurve im Bild?',
              ['y = x⁻²', 'y = x⁻¹', 'y = x²'], 0,
              {0: 'Ja.',
               1: 'Dann läge ein Ast unterhalb der x-Achse. Vergleich mit dem Bild.',
               2: 'Dann gäbe es keine Lücke bei null. Schau, was bei x = 0 geschieht.'},
              rueck_sprich={1: 'Dann läge ein Ast unterhalb der x-Achse. Vergleich mit dem Bild.',
                            2: 'Dann gäbe es keine Lücke bei null. Schau, was bei x gleich null geschieht.'}),
     ], art='Kontrollclip')

W_TR = dict(xbereich=[-4, 5], ybereich=[-4, 5])
W_NS = dict(xbereich=[0, 6], ybereich=[-24, 24],
            xteilung=[[1, '1'], [3, '3'], [5, '5']],
            yteilung=[[-16, '−16'], [0, '0'], [16, '16']])

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
clip('verschieben', 'Kurve sehen: verschieben — und was die Asymptoten tun',
     'Das Schema a·(x−u)ⁿ + v — und wie bei der Hyperbel die Asymptoten mitwandern.',
     ['Transformation', 'Verschiebung', 'Streckung', 'Asymptote', 'Nullstellen'], [
         sz('Das Schema',
            'Jede Grundfunktion lässt sich nach demselben Schema verschieben und strecken: '
            'a mal Klammer x minus u, hoch n, plus v. Für Potenzfunktionen gilt es genauso wie für alle anderen.',
            titel('Ein Schema', 300, 86),
            f(r'y = \fa{a} \cdot (x - \fc{u})^{\fb{n}} + \fc{v}', 470, 62),
            graf(W_TR, [kurve([[0, 1, 3, 0, 0]])])),
         sz('u schiebt waagrecht',
            'u verschiebt waagrecht. Minus zwei in der Klammer schiebt die Kurve zwei nach rechts — '
            'mit umgekehrtem Vorzeichen, wie immer in der Klammer. Der ausgezeichnete Punkt, bei '
            'ungeradem n der Terrassenpunkt, wandert mit.',
            f(r'y = (x \fc{- 2})^{\fb{3}}', 300, 64),
            n('in der Klammer:|umgekehrtes Vorzeichen', 440, 'gruen'),
            graf(W_TR, [kurve([[0, 1, 3, 0, 0]], farbe=5, gestrichelt=True),
                        # 0.9–3.8 zu «schiebt die Kurve zwei nach rechts»; 6.6–10.8 hin und zurück zu
                        # «Der ausgezeichnete Punkt … wandert mit» (Ton 6.5–11.4): der Punkt fährt sichtbar mit
                        kurve([[0.9, 1, 3, 0, 0], [3.8, 1, 3, 2, 0], [6.6, 1, 3, 2, 0], [8.6, 1, 3, 0, 0],
                               [10.8, 1, 3, 2, 0]], startpunkt={'farbe': 5})])),
         sz('v schiebt senkrecht',
            'v verschiebt senkrecht, und zwar mit seinem eigenen Vorzeichen. Minus zwei hinter der Potenz '
            'senkt die ganze Kurve um zwei.',
            f(r'y = (x \fc{- 2})^{\fb{3}} \fc{- 2}', 300, 60, ein=4.2),   # mit «Minus zwei hinter der Potenz»
            n('hinter der Potenz:|eigenes Vorzeichen', 440, 'gruen'),
            graf(W_TR, [kurve([[0, 1, 3, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[4.4, 1, 3, 2, 0], [7.2, 1, 3, 2, -2]], startpunkt={'farbe': 5})])),
         sz('Die Asymptoten wandern mit',
            'Bei einer Hyperbel ist das besonders gut zu sehen: Die Polgerade wandert nach x gleich u, '
            'die waagrechte Asymptote nach y gleich v. Der Kreuzungspunkt der beiden ist das neue Zentrum.',
            f(r'y = \dfrac{1}{x - \fc{2}} \fc{- 1}', 300, 58),
            n('Polgerade @x = \\fc{u}@|Asymptote @y = \\fc{v}@', 440, 'gruen'),
            graf(W_TR, [kurve([[0.9, 1, -1, 0, 0], [4.6, 1, -1, 2, 0],
                               [5.2, 1, -1, 2, 0], [7.6, 1, -1, 2, -1]], asymptoten={'farbe': 5})]),
            # «Der Kreuzungspunkt … das neue Zentrum» (Ton 7.9)
            graf(W_TR, punkte=[pt(2, -1, 3, '(2 | −1)')], ein=7.9, raster=False)),
         sz('Nullstellen',
            'Und die Nullstellen? Man setzt y gleich null und löst auf. Null gleich Klammer x minus drei, '
            'hoch vier, minus sechzehn gibt Klammer hoch vier gleich sechzehn, also x minus drei gleich plus oder '
            'minus zwei — zwei Nullstellen: eins und fünf.',
            f(r'0 = (x-3)^{\fb{4}} - 16', 260, 48, ein=3.5),               # «Null gleich Klammer …» (Ton 3.5)
            f(r'(x-3)^{\fb{4}} = 16 \;\Longrightarrow\; x - 3 = \pm 2', 360, 48, ein=5.4),
            n('gerader Exponent:|beim Wurzelziehen @\\pm@ nicht vergessen|@x_1 = 1@, @x_2 = 5@', 470, 'blau',
              ein=11.0),
            # x⁴ ab «Man setzt y gleich null» (Ton 1.5), gleitet zur Gleichung «Klammer x minus drei, hoch vier,
            # minus sechzehn» (Ton 4.3–8.8): erst u = 3, dann v = −16 — Brücke zu den u/v-Reglern von sim3
            graf(W_NS, [kurve([[4.4, 1, 4, 0, 0], [5.9, 1, 4, 3, 0], [6.1, 1, 4, 3, 0], [8.2, 1, 4, 3, -16]])],
                 ein=1.5),
            graf(W_NS, punkte=[pt(1, 0, 5, '(1 | 0)'), pt(5, 0, 5, '(5 | 0)')], ein=11.0, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: u schiebt waagrecht und steht in der Klammer mit umgekehrtem Vorzeichen, '
            'v schiebt senkrecht mit eigenem. a streckt in y-Richtung. Bei Hyperbeln wandern die Asymptoten '
            'nach x gleich u und y gleich v mit.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a}\,(x - \fc{u})^{\fb{n}} + \fc{v}', 410, 60, ein=0.4),
            n('@\\fc{u}@: waagrecht, in der Klammer|@\\fc{v}@: senkrecht, dahinter|Asymptoten @x = \\fc{u}@, @y = \\fc{v}@',
              540, 'blau', 44, ein=1.2),
            graf(W_TR, [kurve([[0, 1, -1, 2, -1]], asymptoten={'farbe': 5})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-verschieben', 'Kurve sehen: Kontrollfragen zum Verschieben',
     'Fünf Vorhersagen zu u, v, den mitwandernden Asymptoten und den Nullstellen.',
     ['Transformation', 'Verschiebung', 'Asymptote', 'Nullstellen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Minus zwei in der Klammer schiebt zwei nach rechts. Der Terrassenpunkt liegt danach bei zwei und null.',
            f(r'y = (x \fc{- 2})^{\fb{3}}', 300, 64, ein=1.0),
            n('Klammer null bei @x = \\fc{2}@:|zwei nach rechts', 440, 'gruen', ein=2.4),
            graf(W_TR, [kurve([[0, 1, 3, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[0.9, 1, 3, 0, 0], [3.6, 1, 3, 2, 0]], startpunkt={'farbe': 5})])),
         sz('Frage 2',
            'Plus drei steht hinter der Potenz und schiebt senkrecht — drei nach oben.',
            f(r'y = x^{\fb{3}} \fc{+ 3}', 300, 64, ein=1.0),
            n('hinter der Potenz:|eigenes Vorzeichen', 440, 'gruen', ein=2.2),
            graf(W_TR, [kurve([[0, 1, 3, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[0.9, 1, 3, 0, 0], [3.6, 1, 3, 0, 3]], startpunkt={'farbe': 5})])),
         sz('Frage 3',
            'Die Polgerade liegt bei x gleich zwei, die waagrechte Asymptote bei y gleich eins. '
            'Sie kreuzen sich in zwei, eins — dem Zentrum der verschobenen Hyperbel.',
            f(r'y = \dfrac{1}{x - \fc{2}} + \fc{1}', 300, 58, ein=1.2),
            n('Asymptoten @x = \\fc{2}@ und @y = \\fc{1}@', 440, 'gruen', ein=2.8),
            graf(W_TR, [kurve([[1.0, 1, -1, 0, 0], [3.6, 1, -1, 2, 1]], asymptoten={'farbe': 5})])),
         sz('Frage 4',
            'Klammer hoch vier gleich sechzehn: Die vierte Wurzel aus sechzehn ist zwei — und weil der Exponent '
            'gerade ist, kommt das Plusminus dazu. x minus drei ist plus oder minus zwei, also eins und fünf.',
            f(r'x - 3 = \pm 2 \;\Longrightarrow\; x_1 = 1,\; x_2 = 5', 300, 50, ein=1.0),
            n('gerader Exponent:|@\\pm@ nicht vergessen', 440, 'blau', ein=2.6),
            graf(W_NS, [kurve([[0, 1, 4, 3, -16]])],
                 punkte=[pt(1, 0, 5, '(1 | 0)'), pt(5, 0, 5, '(5 | 0)')], ein=1.2)),
         sz('Frage 5',
            'Die Polgerade liegt bei minus eins, die waagrechte Asymptote bei zwei. Also x plus eins in der '
            'Klammer und plus zwei dahinter.',
            f(r'y = \dfrac{1}{x \fc{+ 1}} \fc{+ 2}', 300, 58, ein=1.6),
            n('Pol links vom Ursprung:|@\\fc{u} = -1@', 440, 'gruen', ein=2.8),
            graf(W_TR, [kurve([[0, 1, -1, -1, 2]], asymptoten={'farbe': 5})])),
         sz('Merke',
            'Zum Mitnehmen: u in der Klammer mit umgekehrtem Vorzeichen, v dahinter mit eigenem. '
            'Die Asymptoten einer Hyperbel wandern mit. Und beim Wurzelziehen mit geradem Exponenten '
            'gibt es zwei Lösungen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a}\,(x - \fc{u})^{\fb{n}} + \fc{v}', 410, 60, ein=0.4),
            n('Asymptoten @x = \\fc{u}@, @y = \\fc{v}@|gerader Exponent: @\\pm@ beim Wurzelziehen',
              540, 'blau', 44, ein=1.2),
            graf(W_TR, [kurve([[0, 1, -1, -1, 2]], asymptoten={'farbe': 5})])),
     ], [
         wahl('Frage 1', 'y = (x − 2)³: Wohin wandert der Terrassenpunkt?',
              ['nach (2 | 0)', 'nach (−2 | 0)', 'nach (0 | 2)'], 0,
              {0: 'Ja.',
               1: 'Bei welchem x wird die Klammer null? Setz ein.',
               2: 'Die 2 steht in der Klammer, also schiebt sie waagrecht. Nur wohin?'},
              sprich='y gleich x minus zwei in Klammern, hoch drei: Wohin wandert der Terrassenpunkt?',
              rueck_sprich={1: 'Bei welchem x wird die Klammer null? Setz ein.',
                            2: 'Die zwei steht in der Klammer, also schiebt sie waagrecht. Nur wohin?'}),
         wahl('Frage 2', 'y = x³ + 3: Wohin wandert die Kurve?',
              ['3 nach oben', '3 nach rechts', '3 nach links'], 0,
              {0: 'Ja.',
               1: 'Waagrecht schiebt nur eine Zahl in der Klammer. Wo steht die 3?',
               2: 'Vergleich: Steht die 3 in der Klammer oder dahinter?'},
              sprich='y gleich x hoch drei plus drei: Wohin wandert die Kurve?',
              rueck_sprich={1: 'Waagrecht schiebt nur eine Zahl in der Klammer. Wo steht die drei?',
                            2: 'Vergleich: Steht die drei in der Klammer oder dahinter?'}),
         klick('Frage 3', 'y = 1/(x − 2) + 1: Tipp den Schnittpunkt der beiden Asymptoten ins Bild.',
               [2, 1], 'Getroffen: (2 | 1).',
               [{'bei': [-2, 1], 'text': 'Das Vorzeichen in der Klammer: Bei welchem x wird x − 2 null?',
                 'sprich': 'Das Vorzeichen in der Klammer: Bei welchem x wird x minus zwei null?'},
                {'bei': [2, -1], 'text': 'Die Stelle stimmt. Aber plus 1 hinter dem Bruch heisst hinauf.',
                 'sprich': 'Die Stelle stimmt. Aber plus eins hinter dem Bruch heisst hinauf.'},
                {'bei': [1, 2], 'text': 'Koordinaten vertauscht: u steht in der Klammer, v dahinter.',
                 'sprich': 'Die Koordinaten sind vertauscht: u steht in der Klammer, v dahinter.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — die Asymptoten liegen bei x = u und y = v.',
               sprich='y gleich eins durch Klammer x minus zwei, plus eins: Tipp den Schnittpunkt der '
                      'beiden Asymptoten ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Die Asymptoten liegen bei '
                             'x gleich u und y gleich v.'),
         wahl('Frage 4', 'Wie viele Nullstellen hat f(x) = (x − 3)⁴ − 16, und welche?',
              ['zwei: 1 und 5', 'eine: 5', 'zwei: 3 und 5'], 0,
              {0: 'Ja.',
               1: 'Die vierte Wurzel aus 16 — gibt es da nur eine Möglichkeit?',
               2: 'Setz 3 ein und rechne f(3) aus. Ist das null?'},
              sprich='Wie viele Nullstellen hat f von x gleich Klammer x minus drei, hoch vier, minus sechzehn, '
                     'und welche?',
              rueck_sprich={1: 'Die vierte Wurzel aus sechzehn: Gibt es da nur eine Möglichkeit?',
                            2: 'Setz drei ein und rechne f von drei aus. Ist das null?'}),
         wahl('Frage 5', 'Welche Gleichung gehört zur Hyperbel im Bild?',
              ['y = 1/(x + 1) + 2', 'y = 1/(x − 1) + 2', 'y = 1/(x + 2) + 1'], 0,
              {0: 'Ja.',
               1: 'Lies ab, wo die senkrechte Asymptote liegt — links oder rechts vom Ursprung?',
               2: 'Vergleich beide Asymptoten mit dem Bild, die senkrechte und die waagrechte.'},
              rueck_sprich={1: 'Lies ab, wo die senkrechte Asymptote liegt: links oder rechts vom Ursprung?',
                            2: 'Vergleich beide Asymptoten mit dem Bild, die senkrechte und die waagrechte.'}),
     ], art='Kontrollclip')

DRITTEL = 1 / 3          # 1/p muss ganz und ungerade sein, sonst kennt der Abspieler
HALB = 1 / 2             # die Wurzel aus einer negativen Zahl nicht — genau richtig so
W_UM = dict(xbereich=[-2, 9], ybereich=[-2, 9],
            xteilung=[[2, '2'], [4, '4'], [6, '6'], [8, '8']],
            yteilung=[[2, '2'], [4, '4'], [6, '6'], [8, '8']])
WH = ger(1, 0)           # Winkelhalbierende y = x, die Spiegelachse

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
clip('umkehren', 'Kurve sehen: umkehren heisst spiegeln',
     'Die Umkehrfunktion als Spiegelbild an y = x — und warum gerade Exponenten eine Einschränkung brauchen.',
     ['Umkehrfunktion', 'Spiegelung', 'Winkelhalbierende', 'Wurzelfunktion', 'Einschränkung'], [
         sz('Die Frage umgekehrt',
            'y gleich x hoch drei rechnet aus x das y. Nun die Frage umgekehrt: Das y ist bekannt, '
            'gesucht ist x. Aus acht wird zwei — man zieht die dritte Wurzel.',
            titel('Rückwärts', 280, 86),
            f(r'y = x^{\fb{3}} \quad\longrightarrow\quad x = \sqrt[\fb{3}]{y}', 430, 54, ein=2.8),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]])], punkte=[pt(2, 8, 5, '(2 | 8)')])),
         sz('Spiegeln an y = x',
            'Diese Umkehrung hat ein Bild: Man spiegelt den Graphen an der Winkelhalbierenden '
            'y gleich x. Das grüne Spiegelbild ist der Graph der Umkehrfunktion.',
            f(r'y = \sqrt[\fb{3}]{x}', 300, 62),
            n('Spiegelachse: @y = x@|grün = Umkehrfunktion', 440, 'gruen'),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]], spiegel={'farbe': 3})], geraden=[WH])),
         sz('x und y tauschen',
            'Was beim Spiegeln geschieht, ist einfach gesagt: Aus dem Punkt zwei, acht wird der '
            'Punkt acht, zwei. x und y tauschen die Plätze — und ein Punkt bleibt, wo er ist: eins, eins.',
            f(r'(x \mid y) \;\longmapsto\; (y \mid x)', 300, 58),
            n('@(2 \\mid 8)@ wird @(8 \\mid 2)@|@(1 \\mid 1)@ bleibt liegen', 440, 'gruen'),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]], spiegel={'farbe': 3})], geraden=[WH],
                 punkte=[pt(2, 8, 5, '(2 | 8)'), pt(8, 2, 3, '(8 | 2)'), pt(1, 1, 5)])),
         sz('Gerader Exponent: es geht schief',
            'Bei y gleich x Quadrat geht das so nicht. Das Spiegelbild ist eine liegende Parabel — '
            'über einem x liegen zwei Punkte. Das ist kein Funktionsgraph.',
            f(r'y = x^{\fb{2}}', 300, 62),
            n('Spiegelbild: zu einem @x@|zwei @y@ — keine Funktion', 440, 'rot'),
            graf(W, [kurve([[0, 1, 2, 0, 0]], spiegel={'farbe': 4})], geraden=[WH]),
            # «über einem x liegen zwei Punkte» (Ton 5.7–7.1): x = 1 trifft das Spiegelbild x = y² in (1 | 1) und (1 | −1)
            graf(W, figuren=[{'art': 'strecke', 'von': [1, -3], 'bis': [1, 3], 'farbe': 5, 'dicke': 2.5,
                              'gestrichelt': True}],
                 punkte=[pt(1, 1, 4, '(1 | 1)'),     # (1 | −1) links unten: dort verläuft −√x bei −0.55 … −0.92
                         dict(pt(1, -1, 4, '(1 | −1)'), beschriftung_bei=[0.85, -1.35], anker='end')],
                 ein=5.8, raster=False)),
         sz('Einschränken',
            'Der Ausweg: Man schränkt die Potenzfunktion auf x grösser oder gleich null ein. '
            'Von diesem halben Ast ist das Spiegelbild wieder ein Funktionsgraph — die Quadratwurzel.',
            f(r'y = x^{\fb{2}},\ x \geq 0 \;\longrightarrow\; y = \sqrt{x}', 300, 50),
            n('nur der rechte Ast|wird umkehrbar', 440, 'gruen'),
            graf(W_SP, [kurve([[0, 1, 2, 0, 0]], von=0, spiegel={'farbe': 3})], geraden=[WH])),
         sz('Das Rezept',
            'Rechnerisch geht man in drei Schritten vor: nach x auflösen, x und y vertauschen, und '
            'zum Schluss die Definitionsmenge prüfen. Aus y gleich x hoch drei plus eins wird so '
            'y gleich dritte Wurzel aus x minus eins.',
            f(r'y = x^{\fb{3}} + 1 \;\longrightarrow\; y = \sqrt[\fb{3}]{x - 1}', 300, 48),
            n('1. nach @x@ auflösen|2. @x@ und @y@ vertauschen|3. Definitionsmenge prüfen',
              440, 'blau', 44),
            graf(W_UM, [kurve([[0, 1, 3, 0, 1]], spiegel={'farbe': 3})], geraden=[WH])),
         sz('Merke',
            'Zum Mitnehmen: Umkehren heisst spiegeln an y gleich x, dabei tauschen x und y. '
            'Bei geradem Exponenten muss man vorher einschränken, bei ungeradem nicht. '
            'Das Spiegelbild einer Potenzfunktion ist eine Wurzelfunktion.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = x^{\fb{n}} \;\longleftrightarrow\; y = \sqrt[\fb{n}]{x}', 410, 58, ein=0.4),
            n('spiegeln an @y = x@|@\\fb{n}@ gerade: vorher einschränken|@\\fb{n}@ ungerade: direkt umkehrbar',
              540, 'blau', 44, ein=1.2),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]], spiegel={'farbe': 3})], geraden=[WH])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-umkehren', 'Kurve sehen: Kontrollfragen zum Umkehren',
     'Fünf Fragen zur Umkehrfunktion: Spiegelachse, Einschränkung, Punkttausch und das Rezept.',
     ['Umkehrfunktion', 'Spiegelung', 'Einschränkung', 'Wurzelfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der Exponent fünf ist ungerade, also ist die Kurve ohne Einschränkung umkehrbar. '
            'Die Umkehrfunktion ist die fünfte Wurzel.',
            f(r'y = x^{\fb{5}} \;\longrightarrow\; y = \sqrt[\fb{5}]{x}', 300, 56, ein=1.0),
            n('ungerader Exponent:|direkt umkehrbar', 440, 'gruen', ein=2.6),
            graf(W, [kurve([[0, 1, 5, 0, 0]], spiegel={'farbe': 3})], geraden=[WH])),
         sz('Frage 2',
            'Nur x hoch vier hat einen geraden Exponenten. Sein Spiegelbild hätte über jedem x '
            'zwei Punkte — darum zuerst auf x grösser oder gleich null einschränken.',
            f(r'y = x^{\fb{4}} \;\Longrightarrow\; x \geq 0', 300, 58, ein=1.0),
            n('gerader Exponent:|einschränken, sonst keine Funktion', 440, 'rot', ein=2.8),
            graf(W, [kurve([[0, 1, 4, 0, 0]], spiegel={'farbe': 4})], geraden=[WH], ein=1.0)),
         sz('Frage 3',
            'Beim Spiegeln tauschen die Koordinaten: Zu acht, zwei auf der Wurzelkurve gehört '
            'zwei, acht auf der Potenzkurve.',
            f(r'(8 \mid 2) \;\longmapsto\; (2 \mid 8)', 300, 58, ein=1.2),
            n('Koordinaten tauschen', 440, 'gruen', ein=2.4),
            graf(W_UM, [kurve([[0.9, 1, 3, 0, 0], [3.0, 1, 3, 0, 0]], spiegel={'farbe': 3})],
                 geraden=[WH], punkte=[pt(8, 2, 3, '(8 | 2)')])),
         sz('Frage 4',
            'Gespiegelt wird an der Winkelhalbierenden y gleich x. Sie ist die einzige Gerade, '
            'bei der x und y die Plätze tauschen.',
            f(r'\text{Spiegelachse: } y = x', 300, 58, ein=1.0),
            n('nicht die @x@-Achse,|nicht die @y@-Achse', 440, 'gruen', ein=2.6),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]], spiegel={'farbe': 3})], geraden=[WH], ein=1.0)),
         sz('Frage 5',
            'Nach dem Rezept: y minus eins gleich x hoch drei, dritte Wurzel ziehen, dann x und y '
            'vertauschen. Es bleibt y gleich dritte Wurzel aus x minus eins.',
            f(r'y = \sqrt[\fb{3}]{x - 1}', 300, 58, ein=1.4),
            n('die @1@ landet|unter der Wurzel', 440, 'gruen', ein=2.8),
            # Das Spiegelbild geht sichtbar durch @(1 \\mid 0)@ und verriete damit,
            # welche der drei Gleichungen stimmt — darum erst nach der Antwort.
            graf(W_UM, [kurve([[0, 1, 3, 0, 1]], spiegel={'farbe': 3})], geraden=[WH], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: spiegeln an y gleich x, Koordinaten tauschen, bei geradem Exponenten '
            'vorher einschränken. Und im Rezept wandert alles, was beim Auflösen übrig bleibt, '
            'unter die Wurzel.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = x^{\fb{n}} \;\longleftrightarrow\; y = \sqrt[\fb{n}]{x}', 410, 58, ein=0.4),
            n('@(x \\mid y) \\mapsto (y \\mid x)@|@\\fb{n}@ gerade: einschränken',
              540, 'blau', 44, ein=1.2),
            graf(W_UM, [kurve([[0, 1, 3, 0, 0]], spiegel={'farbe': 3})], geraden=[WH])),
     ], [
         wahl('Frage 1', 'Was ist die Umkehrfunktion von f(x) = x⁵?',
              ['y = ⁵√x', 'y = x⁻⁵', 'y = 5·√x'], 0,
              {0: 'Ja.',
               1: 'Das wäre der Kehrwert, nicht die Umkehrung. Spiegeln ≠ Kehrwert bilden.',
               2: 'Die 5 gehört in den Wurzelexponenten, nicht als Faktor davor.'},
              sprich='Was ist die Umkehrfunktion von f von x gleich x hoch fünf?',
              rueck_sprich={1: 'Das wäre der Kehrwert, nicht die Umkehrung. Spiegeln ist nicht '
                               'Kehrwert bilden.',
                            2: 'Die fünf gehört in den Wurzelexponenten, nicht als Faktor davor.'}),
         wahl('Frage 2', 'Welche dieser Funktionen muss man einschränken, bevor man sie umkehrt?',
              ['y = x⁴', 'y = x³', 'y = x⁵'], 0,
              {0: 'Ja.',
               1: 'Spiegle sie im Kopf: Liegen über einem x zwei Punkte?',
               2: 'Schau auf die Parität des Exponenten — gerade oder ungerade?'},
              sprich='Welche dieser Funktionen muss man einschränken, bevor man sie umkehrt?',
              rueck_sprich={1: 'Spiegle sie im Kopf: Liegen über einem x zwei Punkte?',
                            2: 'Schau auf die Parität des Exponenten: gerade oder ungerade?'}),
         klick('Frage 3', 'Auf y = ³√x liegt (8 | 2). Tipp den Punkt, der ihm auf y = x³ entspricht.',
               [2, 8], 'Getroffen: (2 | 8).',
               [{'bei': [8, 2], 'text': 'Das ist der gegebene Punkt selbst — gesucht ist sein Spiegelbild.',
                 'sprich': 'Das ist der gegebene Punkt selbst. Gesucht ist sein Spiegelbild.'},
                {'bei': [1, 1], 'text': 'Der bleibt beim Spiegeln liegen. Tausch die Koordinaten von (8 | 2).',
                 'sprich': 'Der bleibt beim Spiegeln liegen. Tausch die Koordinaten von acht, zwei.'},
                {'bei': [8, 8], 'text': 'Auf der Spiegelachse selbst. Nur eine Koordinate tauschen genügt nicht.',
                 'sprich': 'Das liegt auf der Spiegelachse selbst. Nur eine Koordinate tauschen genügt nicht.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — beim Spiegeln tauschen x und y.',
               sprich='Auf y gleich dritte Wurzel aus x liegt der Punkt acht, zwei. Tipp den Punkt, '
                      'der ihm auf y gleich x hoch drei entspricht.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Beim Spiegeln tauschen '
                             'x und y die Plätze.'),
         wahl('Frage 4', 'An welcher Gerade wird gespiegelt?',
              ['y = x', 'an der x-Achse', 'an der y-Achse'], 0,
              {0: 'Ja.',
               1: 'Dabei würde nur das Vorzeichen von y kippen — x und y tauschen nicht.',
               2: 'Dabei würde nur das Vorzeichen von x kippen — x und y tauschen nicht.'},
              rueck_sprich={1: 'Dabei würde nur das Vorzeichen von y kippen. x und y tauschen nicht.',
                            2: 'Dabei würde nur das Vorzeichen von x kippen. x und y tauschen nicht.'}),
         wahl('Frage 5', 'f(x) = x³ + 1. Welches ist f⁻¹?',
              ['y = ³√(x − 1)', 'y = ³√x + 1', 'y = ³√(x + 1)'], 0,
              {0: 'Ja.',
               1: 'Setz x = 9 ein: f(2) = 9, also muss f⁻¹(9) = 2 herauskommen. Stimmt das?',
               2: 'Vorzeichen: Beim Auflösen wird die +1 subtrahiert, nicht addiert.'},
              sprich='f von x gleich x hoch drei plus eins. Welches ist die Umkehrfunktion?',
              rueck_sprich={1: 'Setz x gleich neun ein. Es ist f von zwei gleich neun, also muss '
                               'die Umkehrfunktion bei neun den Wert zwei liefern. Stimmt das?',
                            2: 'Vorzeichen: Beim Auflösen wird die eins subtrahiert, nicht addiert.'}),
     ], art='Kontrollclip')

W_WZ = dict(xbereich=[-3, 9], ybereich=[-5, 3],
            xteilung=[[-1, '−1'], [3, '3'], [5, '5'], [7, '7']],
            yteilung=[[-4, '−4'], [-2, '−2'], [2, '2']])
W_VG = dict(xbereich=[-1, 3], ybereich=[-1, 3])
W_DM = dict(xbereich=[-9, 9], ybereich=[-3, 3],
            xteilung=[[-8, '−8'], [-6, '−6'], [-4, '−4'], [-2, '−2'], [2, '2'], [4, '4'], [6, '6'], [8, '8']])
W_GL = dict(xbereich=[-4, 9], ybereich=[-3, 4],
            xteilung=[[-2, '−2'], [2, '2'], [4, '4'], [6, '6'], [8, '8']],
            yteilung=[[-2, '−2'], [2, '2']])

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
clip('wurzel', 'Kurve sehen: Wurzelfunktionen nutzen',
     'Wurzel als Potenz, Definitionsmenge nach Parität, verschobene Wurzelkurven und grafisches Lösen.',
     ['Wurzelfunktion', 'Definitionsmenge', 'Startpunkt', 'Grössenvergleich', 'grafisch lösen'], [
         sz('Die Wurzel ist eine Potenz',
            'Eine Wurzel ist nichts anderes als eine Potenz mit gebrochenem Exponenten: '
            'n-te Wurzel aus x gleich x hoch eins durch n. Damit gelten alle Potenzregeln weiter. '
            'Diese Schreibweise gilt für positives x — die Wurzel selbst reicht gleich noch weiter.',
            titel('Wurzel = Potenz', 280, 80),
            f(r'\sqrt[\fb{n}]{x} = x^{\frac{1}{\fb{n}}} \quad (x \gt 0)', 430, 62, ein=4.4),
            graf(W_SP, [kurve([[0, 1, HALB, 0, 0]], farbe=3)])),
         sz('Definitionsmenge',
            'Die Definitionsmenge hängt davon ab, ob der Wurzelexponent gerade oder ungerade ist. '
            'Die Quadratwurzel gibt es nur ab null. Die dritte Wurzel gibt es auch aus negativen '
            'Zahlen — dritte Wurzel aus minus acht ist minus zwei.',
            f(r'\sqrt{x}:\ D = \mathbb{R}_0^+', 280, 54, ein=4.6),
            f(r'\sqrt[3]{x}:\ D = \mathbb{R}', 380, 54, ein=7.0),
            n('@\\sqrt{x}@ ausgezogen, @\\sqrt[3]{x}@ gestrichelt|gerader Wurzelexponent: ab @0@|'
              'ungerader: ganz @\\mathbb{R}@', 500, 'gruen', 42, ein=9.6),
            # x bis ±9, damit (−8 | −2) im Bild liegt; ∛x erst mit ihrer Formel (7.0), der Punkt mit
            # «minus acht ist minus zwei» (Ton 10.9–11.9)
            graf(W_DM, [kurve([[0, 1, HALB, 0, 0]], farbe=3)]),
            # ∛x löst sich aus √x (p 1/2 → 1/3, ohne stufen): der linke Ast erscheint erst bei genau 1/3 (8.8),
            # zu «auch aus negativen Zahlen» (Ton bis 9.7) — wie «Zieh an n» in sim5
            graf(W_DM, [kurve([[7.0, 1, HALB, 0, 0], [8.8, 1, DRITTEL, 0, 0]], farbe=3, gestrichelt=True)],
                 ein=7.0, raster=False),
            graf(W_DM, punkte=[pt(-8, -2, 5, '(−8 | −2)')], ein=11.2, raster=False)),
         sz('Verschieben wie immer',
            'Verschoben wird nach demselben Schema wie überall. Bei y gleich zwei mal Wurzel aus '
            'x plus eins, minus vier, liegt der Startpunkt bei minus eins und minus vier — dort '
            'beginnt die Definitionsmenge. Der Ordinatenabschnitt ist minus zwei, die Nullstelle '
            'liegt bei drei.',
            f(r'y = 2\,\sqrt{x + \fc{1}} - \fc{4}', 300, 56, ein=3.2),
            n('Startpunkt @(-1 \\mid -4)@|@D = [-1;\\infty[@|Nullstelle bei @x = 3@',
              450, 'gruen', 44, ein=8.4),
            # √x gestrichelt als Bezug; die grüne Kurve gleitet zu «zwei mal Wurzel aus x plus eins, minus vier»
            # (Ton 3.0–6.0) auf a = 2, u = −1, v = −4. Die Punkte zu ihren Sätzen: (0 | −2) 12.0, (3 | 0) 14.3
            graf(W_WZ, [kurve([[0, 1, HALB, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[3.2, 1, HALB, 0, 0], [5.9, 2, HALB, -1, -4]], farbe=3,
                              startpunkt={'farbe': 3})], ein=0.6),
            graf(W_WZ, punkte=[pt(0, -2, 5, '(0 | −2)')], ein=12.0, raster=False),
            graf(W_WZ, punkte=[pt(3, 0, 5, '(3 | 0)')], ein=14.3, raster=False)),
         sz('Wer ist grösser?',
            'Drei Kurven zwischen null und eins: Dort liegt die Wurzel oben, x in der Mitte, '
            'x Quadrat unten. Bei einem schneiden sich alle drei — und rechts davon kehrt sich '
            'die Reihenfolge um.',
            f(r'0 \lt x \lt 1:\ \sqrt{x} \gt x \gt x^2', 300, 52, ein=2.5),
            n('bei @x = 0.25@:|@0.5 \\gt 0.25 \\gt 0.0625@|rechts von @1@ umgekehrt', 440, 'blau', 44, ein=6.0),
            graf(W_VG, [kurve([[0, 1, HALB, 0, 0]], farbe=3),
                        kurve([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[0, 1, 2, 0, 0]], farbe=1)],
                 punkte=[pt(1, 1, 5, '(1 | 1)')]),
            # mit der Notiz (6.0): bei x = 0.25 die drei Werte 0.5, 0.25, 0.0625 — Punkte ohne Text, die Zahlen
            # stehen in der Notiz (Live-Marken runden auf eine Stelle: 0.25 würde 0.3)
            graf(W_VG, figuren=[{'art': 'strecke', 'von': [0.25, 0], 'bis': [0.25, 0.5], 'farbe': 5, 'dicke': 2,
                                 'gestrichelt': True}],
                 punkte=[pt(0.25, 0.5, 3), pt(0.25, 0.25, 5), pt(0.25, 0.0625, 1)], ein=6.0, raster=False)),
         sz('Grafisch lösen',
            'Und damit lässt sich eine Wurzelgleichung grafisch lösen: Dritte Wurzel aus x plus zwei '
            'gleich zwei. Man zeichnet die Kurve und die waagrechte Gerade y gleich zwei und liest '
            'den Schnittpunkt ab — bei x gleich sechs. Die Probe: dritte Wurzel aus sechs plus zwei '
            'ist dritte Wurzel aus acht, also zwei.',
            f(r'\sqrt[\fb{3}]{x + 2} = 2', 300, 58, ein=3.6),
            n('Schnittpunkt @(6 \\mid 2)@|Probe: @\\sqrt[3]{6+2} = \\sqrt[3]{8} = 2@', 450, 'blau', 44, ein=9.8),
            # gestaffelt zum Ton: «die Kurve» 6.4–7.0, «waagrechte Gerade» 7.9, «Schnittpunkt» 10.5
            graf(W_GL, [kurve([[0, 1, DRITTEL, -2, 0]], farbe=3)], ein=6.2),
            graf(W_GL, geraden=[ger(0, 2, farbe=5)], ein=8.0, raster=False),
            graf(W_GL, punkte=[pt(6, 2, 5, '(6 | 2)')], ein=10.5, raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Die n-te Wurzel ist x hoch eins durch n. Bei geradem Wurzelexponenten '
            'beginnt die Definitionsmenge beim Startpunkt, bei ungeradem gibt es keine Schranke. '
            'Verschoben wird nach demselben Schema wie bei allen Grundfunktionen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a}\,\sqrt[\fb{n}]{x - \fc{u}} + \fc{v}', 410, 58, ein=0.4),
            n('@\\sqrt[\\fb{n}]{x} = x^{1/\\fb{n}}@|@\\fb{n}@ gerade: Startpunkt @(\\fc{u} \\mid \\fc{v})@, @D = [\\fc{u};\\infty[@|'
              '@\\fb{n}@ ungerade: @D = \\mathbb{R}@',
              540, 'blau', 42, ein=1.2),
            graf(W_WZ, [kurve([[0, 2, HALB, -1, -4]], farbe=3, startpunkt={'farbe': 3})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
clip('kontrolle-wurzel', 'Kurve sehen: Kontrollfragen zu den Wurzelfunktionen',
     'Fünf Fragen zu Definitionsmenge, Startpunkt, Nullstelle und Grössenvergleich.',
     ['Wurzelfunktion', 'Definitionsmenge', 'Startpunkt', 'Nullstelle', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Quadratwurzel braucht einen Radikanden grösser oder gleich null. x minus drei '
            'grösser oder gleich null heisst x grösser oder gleich drei — die Definitionsmenge '
            'ist das Intervall von drei bis unendlich, links geschlossen.',
            f(r'y = \sqrt{x - 3}: \ D = [3;\infty[', 300, 52, ein=1.0),
            n('Radikand @\\geq 0@:|@x - 3 \\geq 0@', 440, 'gruen', ein=2.8),
            graf(W_GL, [kurve([[0, 1, HALB, 3, 0]], farbe=3, startpunkt={'farbe': 3})], ein=1.0)),
         sz('Frage 2',
            'Der Wurzelexponent drei ist ungerade. Dann darf der Radikand auch negativ sein, '
            'und die Definitionsmenge ist ganz R.',
            f(r'y = \sqrt[\fb{3}]{x - 3}: \ D = \mathbb{R}', 300, 52, ein=1.0),
            n('ungerader Wurzelexponent:|keine Schranke', 440, 'gruen', ein=2.6),
            graf(W_GL, [kurve([[0, 1, DRITTEL, 3, 0]], farbe=3)], ein=1.0)),
         sz('Frage 3',
            'Der Startpunkt liegt dort, wo der Radikand null wird, und um v verschoben: '
            'bei minus eins und minus zwei.',
            f(r'y = \sqrt[\fb{4}]{x + \fc{1}} - \fc{2}', 300, 56, ein=1.2),
            n('Startpunkt @(\\fc{-1} \\mid \\fc{-2})@', 440, 'gruen', ein=2.8),
            # Erster Stuetzpunkt neutral: Beim Fragen steht die unverschobene Kurve da,
            # und der Startpunkt wandert erst mit der Antwort an seinen Platz.
            graf(W_WZ, [kurve([[0.9, 1, 0.25, 0, 0], [3.2, 1, 0.25, -1, -2]], farbe=3,
                              startpunkt={'farbe': 3, 'beschriftung': False})])),
         sz('Frage 4',
            'Null gleich zwei mal Wurzel aus x plus eins, minus vier. Also Wurzel gleich zwei, '
            'dann x plus eins gleich vier, also x gleich drei.',
            f(r'\sqrt{x+1} = 2 \;\Longrightarrow\; x = 3', 300, 52, ein=1.0),
            n('quadrieren:|@x + 1 = 4@', 440, 'blau', ein=2.8),
            graf(W_WZ, [kurve([[0, 2, HALB, -1, -4]], farbe=3, startpunkt={'farbe': 3})],
                 punkte=[pt(3, 0, 5, '(3 | 0)')], ein=1.4)),
         sz('Frage 5',
            'Zwischen null und eins liegt die Wurzel oben: Bei einem Viertel ist die Wurzel ein halb, '
            'x ein Viertel und x Quadrat ein Sechzehntel.',
            f(r'0 \lt x \lt 1:\ \sqrt{x} \gt x \gt x^2', 300, 52, ein=1.4),
            n('bei @x = 0.25@:|@0.5 \\gt 0.25 \\gt 0.0625@', 440, 'blau', ein=3.0),
            graf(W_VG, [kurve([[0, 1, HALB, 0, 0]], farbe=3),
                        kurve([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                        kurve([[0, 1, 2, 0, 0]], farbe=1)],
                 punkte=[pt(1, 1, 5, '(1 | 1)')], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Gerader Wurzelexponent heisst Radikand grösser oder gleich null, '
            'ungerader heisst keine Schranke und keinen Startpunkt. Bei geradem Exponenten liegt '
            'der Startpunkt bei u und v. Und zwischen null und eins liegt die Wurzel über x, '
            'rechts von eins darunter.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a}\,\sqrt[\fb{n}]{x - \fc{u}} + \fc{v}', 410, 58, ein=0.4),
            n('@\\fb{n}@ gerade: Startpunkt @(\\fc{u} \\mid \\fc{v})@, @D = [\\fc{u};\\infty[@|'
              '@\\fb{n}@ ungerade: @D = \\mathbb{R}@, kein Startpunkt',
              540, 'blau', 42, ein=1.2),
            graf(W_WZ, [kurve([[0, 2, HALB, -1, -4]], farbe=3, startpunkt={'farbe': 3})])),
     ], [
         wahl('Frage 1', 'Welche Definitionsmenge hat y = √(x − 3)?',
              ['[3; +∞[', ']−∞; 3]', 'ℝ'], 0,
              {0: 'Ja.',
               1: 'Setz x = 0 ein: Was steht dann unter der Wurzel?',
               2: 'Der Wurzelexponent ist 2, also gerade. Darf der Radikand negativ sein?'},
              sprich='Welche Definitionsmenge hat y gleich Wurzel aus x minus drei?',
              rueck_sprich={1: 'Setz x gleich null ein. Was steht dann unter der Wurzel?',
                            2: 'Der Wurzelexponent ist zwei, also gerade. Darf der Radikand negativ sein?'}),
         wahl('Frage 2', 'Und welche Definitionsmenge hat y = ³√(x − 3)?',
              ['ℝ', '[3; +∞[', '[−3; +∞['], 0,
              {0: 'Ja.',
               1: 'Das wäre die Antwort bei einem geraden Wurzelexponenten. Ist 3 gerade?',
               2: 'Rechne ³√(−8) aus — gibt es diesen Wert?'},
              sprich='Und welche Definitionsmenge hat y gleich dritte Wurzel aus x minus drei?',
              rueck_sprich={1: 'Das wäre die Antwort bei einem geraden Wurzelexponenten. Ist drei gerade?',
                            2: 'Rechne die dritte Wurzel aus minus acht aus. Gibt es diesen Wert?'}),
         klick('Frage 3', 'Tipp den Startpunkt von y = ⁴√(x + 1) − 2 ins Bild.',
               [-1, -2], 'Getroffen: (−1 | −2).',
               [{'bei': [1, -2], 'text': 'Vorzeichen: Bei welchem x wird x + 1 null?',
                 'sprich': 'Vorzeichen: Bei welchem x wird x plus eins null?'},
                {'bei': [-1, 2], 'text': 'Die Stelle stimmt. Aber −2 hinter der Wurzel heisst hinunter.',
                 'sprich': 'Die Stelle stimmt. Aber minus zwei hinter der Wurzel heisst hinunter.'},
                {'bei': [-2, -1], 'text': 'Koordinaten vertauscht: u steht unter der Wurzel, v dahinter.',
                 'sprich': 'Die Koordinaten sind vertauscht: u steht unter der Wurzel, v dahinter.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — der Startpunkt liegt bei (u | v).',
               sprich='Tipp den Startpunkt von y gleich vierte Wurzel aus x plus eins, minus zwei, ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Der Startpunkt liegt '
                             'bei u und v.'),
         wahl('Frage 4', 'Wo liegt die Nullstelle von y = 2·√(x + 1) − 4?',
              ['bei x = 3', 'bei x = 1', 'bei x = 7'], 0,
              {0: 'Ja.',
               1: 'Setz x = 1 ein: 2·√2 − 4 ist nicht null. Löse die Gleichung Schritt für Schritt.',
               2: 'Erst die 4 auf die andere Seite, dann durch 2 teilen, dann quadrieren.'},
              sprich='Wo liegt die Nullstelle von y gleich zwei mal Wurzel aus x plus eins, minus vier?',
              rueck_sprich={1: 'Setz x gleich eins ein: zwei mal Wurzel aus zwei, minus vier, '
                               'ist nicht null. Löse die Gleichung Schritt für Schritt.',
                            2: 'Erst die vier auf die andere Seite, dann durch zwei teilen, dann quadrieren.'}),
         wahl('Frage 5', 'Für 0 < x < 1 gilt:',
              ['√x > x > x²', 'x² > x > √x', 'x > √x > x²'], 0,
              {0: 'Ja.',
               1: 'Setz x = 0.25 ein und rechne alle drei Werte aus.',
               2: 'Setz x = 0.25 ein: Was ist grösser, 0.5 oder 0.25?'},
              sprich='Für x zwischen null und eins gilt:',
              rueck_sprich={1: 'Setz x gleich null Komma zwei fünf ein und rechne alle drei Werte aus.',
                            2: 'Setz x gleich null Komma zwei fünf ein. Was ist grösser, null Komma fünf '
                               'oder null Komma zwei fünf?'}),
     ], art='Kontrollclip')
