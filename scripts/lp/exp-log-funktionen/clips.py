"""Erzeugt die zehn Drehbücher des Leitprogramms Exponential- und Logarithmusfunktionen (04.10.2026).

  python3 scripts/lp/exp-log-funktionen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie beim Vorbild (Leitprogramm Polynomfunktionen): Bild rechts (x 1010, y 175,
760 × 760), Formeln und Notizen links (x 150), Theme begreifbar-schlicht.

**Bewegte Kurven** (HOWTO-clips.md, «Exponential- und Logarithmuskurven»): `ek([[t, c, a, v], …])`
für y = c·aˣ + v und `lk([[t, c, a, v], …])` für y = c·logₐ x + v. Wo eine Kurve nicht in diese
Form passt (Zinseszins-Folge), steht eine feste `formel`.

Farben — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15), gleich wie auf der Seite:
  1 blau   = die Exponentialkurve und ihre Basis a     \\fa{…}
  2 orange = Startwert und Faktor (N₀, A, Prozentsatz)  \\fb{…}
  3 grün   = Logarithmuskurve, Umkehrfunktion, e-Form   \\fc{…}
  4 rot    = Gegenbeispiel, verbotener Bereich          \\fd{…}
  5 Tinte  = neutral: Asymptote, Sättigungswert, y = x, Bezugskurve
"""
import json
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))   # scripts/lp/fragebild.py
from fragebild import anwenden as anwenden_fragebild   # noqa: E402
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
E = math.e


def graf(W, kurven=(), punkte=(), ein=0.05, **kw):
    # Ist die x-Achse eine Zeit (xname «t…»), gibt es keine negativen Zeiten: Kurven ab t = 0.
    if W.get('xname', '').startswith('t'):
        for kv in kurven:
            if kv.get('bewegung') and 'von' not in kv:
                kv['von'] = 0
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=[], punkte=list(punkte), pfeile=True, **W)
    g.update(kw)
    return g


def ueber(W, punkte=(), figuren=(), kurven=(), ein=0.05):
    """Deckblatt ueber einem Graf: gleiches Fenster, ohne Achsen und Karo — nur Punkte,
    Figuren oder Kurven, die spaeter dazukommen (ein je fester Punkt gibt es im graf nicht)."""
    return graf(W, kurven, punkte, ein=ein, raster=False, achsen=False, figuren=list(figuren))


def strecke(von, bis, farbe=5, gestrichelt=False, dicke=4):
    d = {'art': 'strecke', 'von': von, 'bis': bis, 'farbe': farbe, 'dicke': dicke}
    if gestrichelt:
        d['gestrichelt'] = True
    return d


def zins_tabelle(k):
    """Die Zinstabelle spaltenweise: k = 0 Kopf mit Linien, k = 1…4 je eine Spalte. Alle Teile
    haben dieselben Masse (\\phantom), damit sie deckungsgleich uebereinander liegen."""
    n_ = ['1', '2', '12', '10^6']
    w_ = ['2', '2.25', '2.61', '2.718']
    zeig = lambda i, t: t if i == k else r'\phantom{%s}' % t
    if k == 0:
        return (r'\begin{array}{c|cccc} n & ' + ' & '.join(zeig(-1, t) for t in n_)
                + r' \\ \hline & ' + ' & '.join(zeig(-1, t) for t in w_) + r' \end{array}')
    # Ohne Linien; was die Linien im Kopf an Platz brauchen (0.07em waagrecht und senkrecht),
    # ersetzen \kern und \\[…] — im Browser nachgemessen, die Ziffern liegen pixelgenau gleich.
    return (r'\begin{array}{ccccc} \phantom{n}\kern0.07em & ' + ' & '.join(zeig(i + 1, t) for i, t in enumerate(n_))
            + r' \\[0.07em] & ' + ' & '.join(zeig(i + 1, t) for i, t in enumerate(w_)) + r' \end{array}')


def _kurve(art, stuetz, farbe, asymptote, startpunkt, marken, spiegel, von, bis, gestrichelt, dicke):
    d = {'bewegung': stuetz, art: True, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if asymptote:
        d['asymptoten'] = {'farbe': 5}
    if startpunkt is not None:
        d['startpunkt'] = startpunkt
    if marken is not None:
        d['marken'] = marken
    if spiegel is not None:
        d['spiegel'] = spiegel
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


def ek(stuetz, farbe=1, asymptote=False, startpunkt=None, marken=None, spiegel=None, von=None, bis=None,
       gestrichelt=False, dicke=None):
    """Bewegte Exponentialkurve: Stuetzpunkte [t, c, a, v] fuer c·a^x + v."""
    return _kurve('exponential', stuetz, farbe, asymptote, startpunkt, marken, spiegel, von, bis, gestrichelt, dicke)


def lk(stuetz, farbe=3, asymptote=False, startpunkt=None, marken=None, von=None, bis=None,
       gestrichelt=False, dicke=None):
    """Bewegte Logarithmuskurve: Stuetzpunkte [t, c, a, v] fuer c·log_a(x) + v."""
    return _kurve('logarithmus', stuetz, farbe, asymptote, startpunkt, marken, None, von, bis, gestrichelt, dicke)


def fest(formel, farbe=5, gestrichelt=True, dicke=None, von=None, bis=None):
    d = dict(formel=formel, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


def pt(x, y, farbe=5, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = bei
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
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie im Vorbild)."""
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % len(opt)
    dreh = lambda i: (i - k) % len(opt)
    opt = [opt[(i + k) % len(opt)] for i in range(len(opt))]
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': dreh(richtig), 'rueck': {str(dreh(i)): v for i, v in rueck.items()}}
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(dreh(i)): v for i, v in rueck_sprich.items()}
    return d


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None,
          tol=0.45, bei=0.3, eingabe=('x', 'y')):
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
    alt = R + 'clips/s3-4-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 's3-4-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Exponential und Logarithmus',
         'fach': 'Schwerpunktfach', 'lerngebiet': '3 · Funktionen',
         'lektion': ['s3-4a', 's3-4b'], 'stufe': ['BM2'], 'datum': '2026-10-04',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Exponentialkurve sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms exp-log-funktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    anwenden_fragebild(d)                               # beim Fragen nur das Gegebene
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


# Fenster. Die Achsen tragen verschiedene Spannen, wo die Kurve es verlangt.
W1 = dict(xbereich=[-3, 3], ybereich=[-1, 9], yteilung=yt(2, 4, 6, 8), xteilung=yt(-2, -1, 1, 2))

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# Beispiel: f(x) = 2^x — Startwert der Simulation 1.
clip('exponentialfunktion', 'Exponentialkurve sehen: die Exponentialfunktion',
     'Gleicher Faktor je Schritt: wie die Basis a den Verlauf von aˣ bestimmt, der Punkt (0 | 1) und die Asymptote.',
     ['Exponentialfunktion', 'Basis', 'Asymptote', 'Wachstum', 'Zerfall'], [
         sz('Gleicher Faktor',
            'Bei der Exponentialfunktion steht x im Exponenten: y gleich zwei hoch x. Geht x um eins weiter, '
            'wird y mit zwei multipliziert: ein Viertel, ein Halb, eins, zwei, vier, acht.',
            titel('Gleicher Faktor', 280, 80),
            f(r'\begin{array}{c|cccccc} x & -2 & -1 & 0 & 1 & 2 & 3 \\ \hline 2^x & \tfrac14 & \tfrac12 & 1 & 2 & 4 & 8 \end{array}',
              430, 42, ein=3.0),
            n('je Schritt: mal @\\fa{2}@', 560, 'blau', ein=3.7),
            # Punkte einzeln zum Wort (ein je Punkt, seit 07.10.2026): «ein Viertel» 8.7, «ein Halb» 9.3, «eins» 9.9,
            # «zwei» 10.3, «vier» 10.9, «acht» 11.3 s. Mit den drei grossen Punkten die Treppe: einen Schritt
            # nach rechts (gestrichelt), dann mal 2 hinauf (Pfeil) — bei 1/4 → 1/2 → 1 wäre sie zu klein.
            graf(W1, [ek([[0, 1, 2, 0]])], ein=3.0,
                 punkte=[dict(pt(x_, 2.0 ** x_, 5), ein=e_) for x_, e_ in
                         ((-2, 8.7), (-1, 9.3), (0, 9.9), (1, 10.3), (2, 10.9), (3, 11.3))],
                 strecken=[dict(st_, ein=e_) for e_, (x_, y_) in ((10.3, (0, 1)), (10.9, (1, 2)), (11.3, (2, 4))) for st_ in (
                     {'von': [x_, y_], 'bis': [x_ + 1, y_], 'farbe': 1, 'gestrichelt': True},
                     dict({'von': [x_ + 1, y_], 'bis': [x_ + 1, 2 * y_], 'farbe': 1, 'pfeil': True, 'dicke': 4,
                           'beschriftung': '·2'},
                          **({'beschriftung_bei': [x_ + 0.9, y_ + 0.45], 'anker': 'end'} if x_ == 2 else {})))])),
         sz('Die Basis',
            'Die Basis a bestimmt, wie stark die Kurve steigt. Drei hoch x ist steiler, eins Komma fünf hoch x flacher. '
            'Ein Punkt bleibt immer gleich: null, eins. Denn a hoch null ist eins.',
            f(r'y = \fa{a}^{\,x}', 300, 66),
            n('alle Kurven durch @(0 \\mid 1)@|bei @x = 1@ steht die Basis: @(1 \\mid \\fa{a})@', 440, 'blau', ein=8.4),
            graf(W1, [ek([[3.4, 1, 2, 0], [4.8, 1, 3, 0], [5.0, 1, 3, 0], [6.4, 1, 1.5, 0]],
                          startpunkt={'farbe': 5}, marken=[{'x': 1, 'text': '(1 | {y})', 'farbe': 1}])])),
         sz('Zerfall',
            'Ist die Basis kleiner als eins, zum Beispiel ein Halb, fällt die Kurve: In jedem Schritt wird halbiert. '
            'Das beschreibt einen Zerfall.',
            f(r'y = \left(\fa{\tfrac{1}{2}}\right)^{x}', 300, 62),
            n('@0 \\lt \\fa{a} \\lt 1@: Zerfall, die Kurve fällt|@\\fa{a} \\gt 1@: Wachstum, sie steigt', 440, 'blau', ein=3.7),
            graf(W1, [ek([[2.2, 1, 2, 0], [3.6, 1, 0.5, 0]], startpunkt={'farbe': 5})])),
         sz('Spiegelbild',
            'Zwei hoch x und ein Halb hoch x sind Spiegelbilder an der y-Achse. Denn ein Halb hoch x ist dasselbe wie '
            'zwei hoch minus x.',
            f(r'\left(\tfrac{1}{2}\right)^{x} = 2^{-x}', 300, 62),
            n('Basis @\\fa{a}@ und @\\fa{\\tfrac{1}{a}}@:|gespiegelt an der @y@-Achse', 440, 'blau', ein=4.0),
            graf(W1, [ek([[0, 1, 2, 0]]), ek([[0, 1, 0.5, 0]], gestrichelt=True)])),
         sz('Nie null',
            'Und die x-Achse? Die Kurve kommt ihr beliebig nahe, erreicht sie aber nie. a hoch x ist immer positiv. '
            'Die x-Achse ist Asymptote, eine Nullstelle gibt es nicht.',
            f(r'a^x \gt 0 \quad \text{für alle } x', 300, 58),
            n('Asymptote @y = 0@|keine Nullstelle, @W = \\mathbb{R}^+@', 440, 'blau', ein=6.5),
            graf(W1, [ek([[0, 1, 2, 0]], asymptote=True, marken=[{'x': -3, 'text': '(−3 | 0.125)', 'farbe': 5}])])),
         sz('Basis aus einem Punkt',
            'Geht eine Exponentialkurve durch zwei, neun, dann gilt a Quadrat gleich neun. Also ist a gleich drei, '
            'denn die Basis ist positiv.',
            f(r'\fa{a}^2 = 9 \;\Rightarrow\; \fa{a} = 3', 300, 60),
            n('@\\fa{a} \\gt 0@: nur die positive Lösung', 440, 'blau', ein=5.4),
            graf(dict(xbereich=[-3, 3], ybereich=[-1, 11], yteilung=yt(2, 4, 6, 8, 10), xteilung=yt(-2, -1, 1, 2)),
                 # mit a = 2 beginnen (durch (2 | 4), neben dem Punkt); «Also ist a gleich drei» (5.4–7.0 s):
                 # a 2 → 3, die Kurve läuft in (2 | 9) — jeder Zwischenstand geht durch (0 | 1)
                 [ek([[5.4, 1, 2, 0], [7.0, 1, 3, 0]])], ein=0.4, punkte=[pt(2, 9, 5, '(2 | 9)', [1.25, 9.9], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: Bei a hoch x wird in jedem Schritt mit a multipliziert. Alle Kurven gehen durch null, eins, '
            'die x-Achse ist Asymptote. Basis grösser als eins heisst Wachstum, zwischen null und eins Zerfall.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = \fa{a}^{\,x}, \quad \fa{a} \gt 0,\ \fa{a} \neq 1', 410, 54, ein=0.4),
            n('durch @(0 \\mid 1)@ und @(1 \\mid \\fa{a})@|Asymptote @y = 0@|@\\fa{a} \\gt 1@ Wachstum; @\\fa{a} \\lt 1@ Zerfall',
              540, 'blau', 44, ein=1.2),
            graf(W1, [ek([[0, 1, 2, 0]], asymptote=True, startpunkt={'farbe': 5})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
W1k = dict(xbereich=[-3, 3], ybereich=[-1, 7], yteilung=yt(2, 4, 6), xteilung=yt(-2, -1, 1, 2))
clip('kontrolle-exponentialfunktion', 'Exponentialkurve sehen: Kontrollfragen zur Exponentialfunktion',
     'Fünf Vorhersagen zu Funktionswerten, Basis, gemeinsamem Punkt und Spiegelbild.',
     ['Exponentialfunktion', 'Basis', 'Kontrollfragen'], [
         sz('Frage 1',
            'Fünf hoch minus eins ist der Kehrwert von fünf, also ein Fünftel, null Komma zwei. Ein negativer Exponent macht nichts negativ.',
            f(r'5^{-1} = \tfrac{1}{5} = 0.2', 300, 62, ein=1.0),
            n('negativer Exponent:|Kehrwert, nicht negativ', 440, 'blau', ein=2.4),
            graf(W1k, [ek([[0, 1, 5, 0]], marken=[{'x': -1, 'text': '(−1 | 0.2)', 'farbe': 5}])], ein=1.2)),
         sz('Frage 2',
            'Null Komma vier ist kleiner als eins: Diese Kurve fällt. Eins Komma vier ist grösser als eins, sie steigt.',
            f(r'\fa{0.4} \lt 1 \;\Rightarrow\; \text{fällt}', 300, 58, ein=1.0),
            n('Basis kleiner als 1:|Zerfall', 440, 'blau', ein=2.4),
            graf(W1k, [ek([[0, 1, 0.4, 0]]), ek([[0, 1, 1.4, 0]], gestrichelt=True)], ein=1.2)),
         sz('Frage 3',
            'Jede Basis hoch null ist eins. Darum gehen alle diese Kurven durch null, eins.',
            f(r'a^0 = 1', 300, 66, ein=1.0),
            n('gemeinsamer Punkt @(0 \\mid 1)@', 440, 'blau', ein=2.4),
            graf(W1k, [ek([[0.6, 1, 2, 0], [2.6, 1, 4, 0], [4.6, 1, 0.5, 0]])])),
         sz('Frage 4',
            'a hoch drei gleich acht. Die dritte Wurzel aus acht ist zwei: Die Basis ist zwei.',
            f(r'\fa{a}^3 = 8 \;\Rightarrow\; \fa{a} = \sqrt[3]{8} = 2', 300, 54, ein=1.0),
            n('Probe: @2^3 = 8@', 440, 'blau', ein=2.4),
            graf(dict(xbereich=[-2, 4], ybereich=[-1, 10], yteilung=yt(2, 4, 6, 8), xteilung=yt(-1, 1, 2, 3)),
                 [ek([[0, 1, 2, 0]])], ein=1.2, punkte=[pt(3, 8, 5, '(3 | 8)', [2.75, 8.9], 'end')])),
         sz('Frage 5',
            'Spiegeln an der y-Achse heisst x durch minus x ersetzen: drei hoch minus x, und das ist ein Drittel hoch x.',
            f(r'3^{-x} = \left(\tfrac{1}{3}\right)^{x}', 300, 60, ein=1.0),
            n('Basis @\\fa{a}@ wird @\\fa{\\tfrac{1}{a}}@', 440, 'blau', ein=2.4),
            graf(W1k, [ek([[0, 1, 3, 0]]), ek([[0, 1, 1 / 3, 0]], gestrichelt=True)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Negativer Exponent heisst Kehrwert. Die Basis entscheidet über Wachstum oder Zerfall. '
            'Alle Kurven gehen durch null, eins.',
            titel('Zum Mitnehmen', 250, 76),
            n('@a^{-x} = \\left(\\tfrac{1}{a}\\right)^x@|@\\fa{a} \\gt 1@ steigt, @\\fa{a} \\lt 1@ fällt|alle durch @(0 \\mid 1)@',
              400, 'blau', 44, ein=1.2),
            graf(W1, [ek([[0, 1, 2, 0]], asymptote=True, startpunkt={'farbe': 5})])),
     ], [
         wahl('Frage 1', 'f(x) = 5ˣ: Wie gross ist f(−1)?',
              ['0.2', '−5', '−0.2'], 0,
              {0: 'Ja.',
               1: 'Ein negativer Exponent bedeutet den Kehrwert, nicht ein negatives Ergebnis.',
               2: 'Kann eine Potenz mit positiver Basis negativ sein?'},
              sprich='f von x gleich fünf hoch x: Wie gross ist f von minus eins?',
              rueck_sprich={1: 'Ein negativer Exponent bedeutet den Kehrwert, nicht ein negatives Ergebnis.',
                            2: 'Kann eine Potenz mit positiver Basis negativ sein?'}),
         wahl('Frage 2', 'Welche der beiden Kurven fällt: y = 0.4ˣ oder y = 1.4ˣ?',
              ['y = 0.4ˣ', 'y = 1.4ˣ', 'beide'], 0,
              {0: 'Ja.',
               1: 'Rechne den Wert bei x = 1 und x = 2 aus.',
               2: 'Eine Basis grösser als 1 lässt die Werte wachsen.'},
              sprich='Welche der beiden Kurven fällt: y gleich null Komma vier hoch x, oder y gleich eins Komma vier hoch x?',
              rueck_sprich={1: 'Rechne den Wert bei x gleich eins und x gleich zwei aus.',
                            2: 'Eine Basis grösser als eins lässt die Werte wachsen.'}),
         klick('Frage 3', 'Durch welchen Punkt gehen alle Kurven y = aˣ? Tipp ihn ins Bild.',
               [0, 1], 'Getroffen: (0 | 1).',
               [{'bei': [1, 0], 'text': 'Koordinaten vertauscht: Die Kurven treffen die x-Achse nie.',
                 'sprich': 'Koordinaten vertauscht: Die Kurven treffen die x-Achse nie.'},
                {'bei': [0, 0], 'text': 'Der Ursprung liegt auf keiner dieser Kurven: aˣ ist nie null.',
                 'sprich': 'Der Ursprung liegt auf keiner dieser Kurven. a hoch x ist nie null.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — was ergibt a⁰?',
               sprich='Durch welchen Punkt gehen alle Kurven y gleich a hoch x? Tipp ihn ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Was ergibt a hoch null?'),
         wahl('Frage 4', 'y = aˣ geht durch (3 | 8). Wie gross ist a?',
              ['2', '8/3', '4'], 0,
              {0: 'Ja.',
               1: 'Nicht teilen: Gesucht ist die Zahl, die dreimal mit sich multipliziert 8 ergibt.',
               2: 'Rechne 4³ aus — ist das 8?'},
              sprich='y gleich a hoch x geht durch drei, acht. Wie gross ist a?',
              rueck_sprich={1: 'Nicht teilen. Gesucht ist die Zahl, die dreimal mit sich multipliziert acht ergibt.',
                            2: 'Rechne vier hoch drei aus. Ist das acht?'}),
         wahl('Frage 5', 'Spiegelt man y = 3ˣ an der y-Achse, entsteht …',
              ['y = (1/3)ˣ', 'y = −3ˣ', 'y = 3⁻ˣ + 1'], 0,
              {0: 'Ja.',
               1: 'Das wäre die Spiegelung an der x-Achse — alle Werte negativ.',
               2: 'Spiegeln verschiebt nicht. Ersetze nur x durch −x.'},
              sprich='Spiegelt man y gleich drei hoch x an der y-Achse, entsteht …',
              rueck_sprich={1: 'Das wäre die Spiegelung an der x-Achse, alle Werte negativ.',
                            2: 'Spiegeln verschiebt nicht. Ersetze nur x durch minus x.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# Beispiel: N(t) = 200 · 1.5^t — Startwert der Simulation 2.
W2 = dict(xbereich=[-0.9, 5], ybereich=[-60, 1100], yteilung=yt(200, 400, 600, 800, 1000),
          xteilung=yt(1, 2, 3, 4), xname='t', yname='N')
clip('wachstum-zerfall', 'Exponentialkurve sehen: Wachstum und Zerfall',
     'Startwert und Wachstumsfaktor, Prozent und Faktor, Verdopplungszeit und Halbwertszeit.',
     ['Wachstum', 'Zerfall', 'Wachstumsfaktor', 'Verdopplungszeit', 'Halbwertszeit'], [
         sz('Startwert und Faktor',
            'Eine Population von zweihundert Tieren wächst jedes Jahr um fünfzig Prozent. Jedes Jahr wird mit eins Komma fünf '
            'multipliziert: dreihundert, vierhundertfünfzig, sechshundertfünfundsiebzig.',
            titel('Wachstum', 280, 80),
            f(r'N(t) = \fb{200} \cdot \fa{1.5}^{\,t}', 430, 58, ein=3.0),
            n('Startwert @\\fb{N_0} = 200@|Wachstumsfaktor @\\fa{a} = 1.5@', 560, 'blau', 44, ein=5.0),
            # Läufer wie in sim2 (seit 07.10.2026): je Jahr ein Schritt, «mal eins Komma fünf» (6.6 s) bis
            # «dreihundert» (7.5 s), «vierhundertfünfzig» (8.6 s), «sechshundertfünfundsiebzig» (9.9 s);
            # die Punkte bleiben als Spur stehen.
            graf(W2, [dict(ek([[0, 200, 1.5, 0]], startpunkt={'farbe': 2}),
                           laeufer={'bahn': [[6.6, 0], [7.5, 1], [7.8, 1], [8.6, 2], [9.1, 2], [9.9, 3]],
                                    'text': '({x} | {y})', 'farbe': 2})], ein=2.0,
                 punkte=[dict(pt(1, 300, 5), ein=7.5), dict(pt(2, 450, 5), ein=8.6), dict(pt(3, 675, 5), ein=9.9)])),
         sz('Prozent und Faktor',
            'Plus fünfzig Prozent heisst mal eins Komma fünf. Ein Zuwachs von p Prozent gibt den Faktor eins plus p Hundertstel. '
            'Eine Abnahme von zwanzig Prozent gibt den Faktor null Komma acht: Es bleiben achtzig Prozent.',
            f(r'+p\,\% \;\to\; \fa{a} = 1 + \tfrac{p}{100}', 300, 52),
            f(r'-p\,\% \;\to\; \fa{a} = 1 - \tfrac{p}{100}', 390, 52, ein=7.2),
            n('@+50\\,\\%@: @\\fa{1.5}@; @-20\\,\\%@: @\\fa{0.8}@', 490, 'blau', ein=8.0),
            graf(W2, [ek([[0.4, 200, 1.5, 0], [7.2, 200, 1.5, 0], [9.2, 200, 0.8, 0]], startpunkt={'farbe': 2})])),
         sz('Verdopplungszeit',
            'Verdoppelt sich eine Grösse alle drei Stunden, schreibt man zwei hoch t durch drei. Nach drei Stunden das '
            'Doppelte, nach sechs das Vierfache, nach neun das Achtfache.',
            f(r'N(t) = \fb{1000} \cdot \fa{2}^{\,t/3}', 300, 56),
            f(r'N(6) = 1000 \cdot 2^{2} = 4000', 390, 50, ein=6.0),
            n('alle 3 Stunden mal @\\fa{2}@', 490, 'blau', ein=4.7),
            graf(dict(xbereich=[-1.8, 10], ybereich=[-400, 9000], yteilung=yt(2000, 4000, 6000, 8000),
                      xteilung=yt(3, 6, 9), xname='t [h]', yname='N'),
                 [ek([[0, 1000, 2 ** (1 / 3), 0]], startpunkt={'farbe': 2})], ein=1.0,
                 # «nach drei» 4.9, «nach sechs» 6.5, «nach neun» 7.9 s (ein je Punkt, seit 07.10.2026)
                 punkte=[dict(pt(3, 2000, 5), ein=4.9), dict(pt(6, 4000, 5, '(6 | 4000)', [5.6, 4700], 'end'), ein=6.5),
                         dict(pt(9, 8000, 5), ein=7.9)])),
         sz('Halbwertszeit',
            'Umgekehrt beim Zerfall: Ein Medikament mit achtzig Milligramm hat eine Halbwertszeit von vier Stunden. '
            'Nach vier Stunden sind es vierzig, nach acht zwanzig, nach zwölf zehn Milligramm.',
            f(r'm(t) = \fb{80} \cdot \left(\fa{\tfrac{1}{2}}\right)^{t/4}', 300, 54),
            n('alle 4 Stunden halbiert', 440, 'blau', ein=5.8),
            graf(dict(xbereich=[-1.2, 14], ybereich=[-4, 90], yteilung=yt(20, 40, 60, 80),
                      xteilung=yt(4, 8, 12), xname='t [h]', yname='m [mg]'),
                 [ek([[0, 80, 0.5 ** 0.25, 0]], asymptote=True, startpunkt={'farbe': 2})], ein=1.0,
                 # «nach vier» 6.1, «nach acht» 8.0, «nach zwölf» 9.2 s (ein je Punkt, seit 07.10.2026)
                 punkte=[dict(pt(4, 40, 5), ein=6.1), dict(pt(8, 20, 5), ein=8.0), dict(pt(12, 10, 5), ein=9.2)])),
         sz('Exponentiell oder linear',
            'Woran erkennt man exponentielles Wachstum in einer Tabelle? Der Quotient aufeinanderfolgender Werte ist gleich, '
            'hier immer eins Komma zwei. Bei linearem Wachstum wäre die Differenz gleich.',
            f(r'\begin{array}{c|cccc} t & 0 & 1 & 2 & 3 \\ \hline N & 50 & 60 & 72 & 86.4 \end{array}', 300, 46),
            n('Quotient konstant: @\\fa{1.2}@ → exponentiell|Differenz konstant → linear', 460, 'blau', ein=3.8),
            graf(dict(xbereich=[-0.5, 4], ybereich=[-6, 110], yteilung=yt(20, 40, 60, 80, 100), xteilung=yt(1, 2, 3),
                      xname='t', yname='N'),
                 [ek([[0, 50, 1.2, 0]])], ein=3.0, punkte=[pt(0, 50, 2), pt(1, 60, 5), pt(2, 72, 5), pt(3, 86.4, 5)]),
            # «Bei linearem Wachstum wäre die Differenz gleich» (7.96 s): die lineare Reihe +10 zum Vergleich
            ueber(dict(xbereich=[-0.5, 4], ybereich=[-6, 110]),
                  kurven=[dict(fest('50+10*x', von=0, bis=4), beschriftung='linear', beschriftung_bei=[3.0, 68])],
                  ein=8.0)),
         sz('Merke',
            'Zum Mitnehmen: N von t gleich Startwert mal Faktor hoch t. Ein Zuwachs von p Prozent gibt den Faktor eins plus p Hundertstel, '
            'eine Abnahme eins minus p Hundertstel. Verdopplungszeit und Halbwertszeit stehen im Exponenten: t durch T.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'N(t) = \fb{N_0} \cdot \fa{a}^{\,t}', 410, 56, ein=0.4),
            n('@\\fa{a} = 1 \\pm \\tfrac{p}{100}@|Verdopplung: @\\fb{N_0} \\cdot 2^{t/T}@|Halbierung: @\\fb{N_0} \\cdot \\left(\\tfrac12\\right)^{t/T}@',
              540, 'blau', 44, ein=1.2),
            graf(W2, [ek([[0, 200, 1.5, 0]], startpunkt={'farbe': 2})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-wachstum', 'Exponentialkurve sehen: Kontrollfragen zu Wachstum und Zerfall',
     'Fünf Vorhersagen zu Faktor, Prozent, Halbwertszeit und Modellwahl.',
     ['Wachstum', 'Zerfall', 'Halbwertszeit', 'Kontrollfragen'], [
         sz('Frage 1',
            'Plus dreissig Prozent: Zu hundert Prozent kommen dreissig dazu. Der Faktor ist eins Komma drei.',
            f(r'1 + 0.3 = \fa{1.3}', 300, 64, ein=1.0),
            n('Faktor, nicht Summand', 440, 'blau', ein=2.4),
            graf(W2, [ek([[0, 200, 1.3, 0]], startpunkt={'farbe': 2})], ein=1.2)),
         sz('Frage 2',
            'Minus zehn Prozent: Es bleiben neunzig Prozent. Der Faktor ist null Komma neun.',
            f(r'1 - 0.1 = \fa{0.9}', 300, 64, ein=1.0),
            n('es bleibt, was nicht abnimmt', 440, 'blau', ein=2.4),
            graf(W2, [ek([[0, 800, 0.9, 0]], startpunkt={'farbe': 2})], ein=1.2)),
         sz('Frage 3',
            'Fünfzehn Jahre sind drei Halbwertszeiten. Dreimal halbieren: vierundsechzig, zweiunddreissig, sechzehn, acht Gramm.',
            f(r'64 \cdot \left(\tfrac12\right)^{3} = 8', 300, 60, ein=1.0),
            n('@15 : 5 = 3@ Halbwertszeiten', 440, 'blau', ein=2.4),
            graf(dict(xbereich=[-1, 20], ybereich=[-3, 70], yteilung=yt(16, 32, 48, 64), xteilung=yt(5, 10, 15),
                      xname='t [a]', yname='m [g]'),
                 [ek([[0, 64, 0.5 ** 0.2, 0]], startpunkt={'farbe': 2})], ein=1.2,
                 punkte=[pt(5, 32, 5), pt(10, 16, 5), pt(15, 8, 5)])),
         sz('Frage 4',
            'Hundert mal zwei hoch t halbe: Nach vier Zeiteinheiten ist zweimal verdoppelt, also vierhundert.',
            f(r'N(4) = 100 \cdot 2^{4/2} = 400', 300, 56, ein=1.0),
            n('alle 2 Einheiten verdoppelt', 440, 'blau', ein=2.4),
            graf(dict(xbereich=[-0.9, 6], ybereich=[-40, 900], yteilung=yt(200, 400, 600, 800), xteilung=yt(1, 2, 3, 4, 5),
                      xname='t', yname='N'),
                 [ek([[0, 100, 2 ** 0.5, 0]], marken=[{'x': 4, 'text': '(4 | 400)', 'farbe': 5}])], ein=1.2)),
         sz('Frage 5',
            'Zwanzig, dreissig, fünfundvierzig: Die Differenz wächst, der Quotient bleibt eins Komma fünf. Das ist exponentiell.',
            f(r'\tfrac{30}{20} = \tfrac{45}{30} = 1.5', 300, 56, ein=1.0),
            n('gleicher Quotient → exponentiell', 440, 'blau', ein=2.4),
            graf(dict(xbereich=[-0.5, 4], ybereich=[-6, 110], yteilung=yt(20, 40, 60, 80, 100), xteilung=yt(1, 2, 3),
                      xname='t', yname='N'),
                 [ek([[0, 20, 1.5, 0]])], ein=1.2, punkte=[pt(0, 20, 5), pt(1, 30, 5), pt(2, 45, 5)])),
         sz('Merke',
            'Zum Mitnehmen: Prozent werden zum Faktor eins plus oder minus p Hundertstel. Halbwertszeiten zählt man ab. '
            'Und exponentiell erkennt man am gleichen Quotienten.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\pm p\\,\\% \\to 1 \\pm \\tfrac{p}{100}@|@t : T@ Halbierungen|gleicher Quotient: exponentiell',
              400, 'blau', 44, ein=1.2),
            graf(W2, [ek([[0, 200, 1.5, 0]], startpunkt={'farbe': 2})])),
     ], [
         wahl('Frage 1', 'Eine Grösse wächst jedes Jahr um 30 %. Mit welchem Faktor wird jährlich multipliziert?',
              ['1.3', '0.3', '30'], 0,
              {0: 'Ja.',
               1: '0.3 ist nur der Zuwachs. Was ist mit den 100 %, die schon da sind?',
               2: 'Prozent heisst Hundertstel: 30 % = 0.3.'},
              sprich='Eine Grösse wächst jedes Jahr um dreissig Prozent. Mit welchem Faktor wird jährlich multipliziert?',
              rueck_sprich={1: 'Null Komma drei ist nur der Zuwachs. Was ist mit den hundert Prozent, die schon da sind?',
                            2: 'Prozent heisst Hundertstel: dreissig Prozent sind null Komma drei.'}),
         wahl('Frage 2', 'Ein Bestand nimmt jedes Jahr um 10 % ab. Welcher Faktor?',
              ['0.9', '−0.1', '1.1'], 0,
              {0: 'Ja.',
               1: 'Mit einem negativen Faktor würden die Werte das Vorzeichen wechseln. Was bleibt übrig?',
               2: 'Das wäre ein Zuwachs von 10 %.'},
              sprich='Ein Bestand nimmt jedes Jahr um zehn Prozent ab. Welcher Faktor?',
              rueck_sprich={1: 'Mit einem negativen Faktor würden die Werte das Vorzeichen wechseln. Was bleibt übrig?',
                            2: 'Das wäre ein Zuwachs von zehn Prozent.'}),
         wahl('Frage 3', 'Halbwertszeit 5 Jahre, Start 64 g. Wie viel ist nach 15 Jahren übrig?',
              ['8 g', '16 g', '21.3 g'], 0,
              {0: 'Ja.',
               1: 'Wie viele Halbwertszeiten passen in 15 Jahre?',
               2: 'Nicht durch 3 teilen: Dreimal halbieren.'},
              sprich='Halbwertszeit fünf Jahre, Start vierundsechzig Gramm. Wie viel ist nach fünfzehn Jahren übrig?',
              rueck_sprich={1: 'Wie viele Halbwertszeiten passen in fünfzehn Jahre?',
                            2: 'Nicht durch drei teilen. Dreimal halbieren.'}),
         # Wahl statt Klick: Im Fenster bis 900 wäre eine Klicktoleranz in Dateneinheiten kaum zu treffen.
         wahl('Frage 4', 'N(t) = 100 · 2^(t/2): Wie gross ist N(4)?',
              ['400', '200', '800'], 0,
              {0: 'Ja.',
               1: 'Das wäre nach einer Verdopplung. Wie viele Verdopplungen sind es in 4 Einheiten?',
               2: 'Zu viel: Verdoppelt wird nur alle 2 Einheiten.'},
              sprich='N von t gleich hundert mal zwei hoch t halbe: Wie gross ist N von vier?',
              rueck_sprich={1: 'Das wäre nach einer Verdopplung. Wie viele Verdopplungen sind es in vier Einheiten?',
                            2: 'Zu viel. Verdoppelt wird nur alle zwei Einheiten.'}),
         wahl('Frage 5', 'Die Werte 20, 30, 45 (je ein Jahr später): Welches Modell passt?',
              ['exponentiell, Faktor 1.5', 'linear, +10 pro Jahr', 'exponentiell, Faktor 10'], 0,
              {0: 'Ja.',
               1: 'Rechne beide Differenzen aus: 30 − 20 und 45 − 30.',
               2: 'Der Faktor ist ein Quotient, keine Differenz.'},
              sprich='Die Werte zwanzig, dreissig, fünfundvierzig, je ein Jahr später: Welches Modell passt?',
              rueck_sprich={1: 'Rechne beide Differenzen aus: dreissig minus zwanzig und fünfundvierzig minus dreissig.',
                            2: 'Der Faktor ist ein Quotient, keine Differenz.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Beispiel: 2^x und 8^x = 2^(3x); e^x zwischen 2^x und 3^x — Startwert der Simulation 3 ist 4^x mit Basis 2.
W3 = dict(xbereich=[-2, 2], ybereich=[-0.5, 8], yteilung=yt(2, 4, 6, 8), xteilung=yt(-1, 1))
clip('e-funktion', 'Exponentialkurve sehen: die e-Funktion und der Basiswechsel',
     'Woher die Zahl e kommt, wie e^x zwischen 2^x und 3^x liegt und wie man jede Basis in eine andere umschreibt.',
     ['e-Funktion', 'Eulersche Zahl', 'Basiswechsel', 'natürlicher Logarithmus'], [
         sz('Die Zahl e',
            'Ein Franken zu hundert Prozent Zins wird nach einem Jahr zu zwei Franken. Halbjährlich verzinst zu zwei Komma '
            'zwei fünf, monatlich zu zwei Komma sechs eins. Je feiner, desto näher an einer festen Zahl: e, '
            'ungefähr zwei Komma sieben eins acht.',
            titel('Die Zahl e', 280, 80),
            f(r'\left(1 + \tfrac{1}{n}\right)^{n} \;\to\; e \approx 2.718', 430, 52, ein=12.0),
            # Tabelle spaltenweise zum Wort: «zwei Franken» 3.4, «zwei Komma zwei fünf» 5.8,
            # «zwei Komma sechs eins» 7.8, «zwei Komma sieben eins acht» 12.3
            f(zins_tabelle(0), 560, 40, ein=2.9),
            f(zins_tabelle(1), 560, 40, ein=3.4),
            f(zins_tabelle(2), 560, 40, ein=5.8),
            f(zins_tabelle(3), 560, 40, ein=7.8),
            f(zins_tabelle(4), 560, 40, ein=12.3)),
         sz('Zwischen 2 und 3',
            'Die e-Funktion e hoch x liegt zwischen zwei hoch x und drei hoch x. Auch sie geht durch null, eins, '
            'und bei x gleich eins steht e.',
            f(r'y = \fc{e}^{\,x}', 300, 66),
            n('@2 \\lt e \\lt 3@|durch @(0 \\mid 1)@ und @(1 \\mid e)@', 440, 'gruen', ein=5.9),
            graf(W3, [ek([[0, 1, 2, 0]], gestrichelt=True), ek([[0, 1, 3, 0]], gestrichelt=True),
                      ek([[0, 1, E, 0]], farbe=3, marken=[{'x': 1, 'text': '(1 | 2.718)', 'farbe': 3}])])),
         sz('Basiswechsel',
            'Jede Basis lässt sich als Potenz einer anderen schreiben. Acht ist zwei hoch drei, also ist acht hoch x '
            'gleich zwei hoch drei x. Im Bild: Die Kurve von zwei hoch x, in x-Richtung auf ein Drittel gestaucht.',
            f(r'8^{x} = \left(2^{3}\right)^{x} = 2^{\fb{3}x}', 300, 54),
            n('@c^x = a^{\\fb{b}x}@ mit @c = a^{\\fb{b}}@', 440, 'orange', ein=5.7),
            graf(W3, [ek([[0, 1, 2, 0]], gestrichelt=True), ek([[9.4, 1, 2, 0], [12.0, 1, 8, 0]])])),
         sz('Zur Basis e',
            'Mit der Basis e geht das immer. Zwei ist e hoch ln zwei, also ist zwei hoch x gleich e hoch ln zwei mal x. '
            'ln zwei ist ungefähr null Komma sechs neun.',
            f(r'2 = e^{\ln 2} \;\Rightarrow\; 2^{x} = e^{(\ln 2)\,x}', 300, 50),
            f(r'\ln 2 \approx 0.69', 400, 50, ein=8.0),
            n('@a^x = e^{\\fb{b}x}@ mit @\\fb{b} = \\ln a@', 500, 'orange', 44, ein=6.0),
            # e^(bx) beginnt mit b = 1 (e^x) und landet bei «gleich e hoch ln zwei mal x» (5.6–7.3 s)
            # auf 2^x: a = e^b von e nach 2, jeder Zwischenstand ist ein e^(bx) mit b = ln a
            graf(W3, [ek([[0, 1, 2, 0]]), ek([[5.6, 1, E, 0], [7.3, 1, 2, 0]], farbe=3, gestrichelt=True)], ein=1.0)),
         sz('Vorzeichen von b',
            'Ist die Basis kleiner als eins, ist ihr Logarithmus negativ. Ein Halb hoch x ist ungefähr e hoch minus null Komma '
            'sechs neun x. Positives b heisst Wachstum, negatives b Zerfall.',
            f(r'\left(\tfrac12\right)^{x} = e^{(\ln 0.5)\,x} \approx e^{-0.69\,x}', 300, 46),
            n('@\\fb{b} \\gt 0@: Wachstum; @\\fb{b} \\lt 0@: Zerfall', 440, 'orange', ein=9.0),
            graf(W3, [ek([[4.3, 1, 2, 0], [6.3, 1, 0.5, 0]], farbe=3)])),
         sz('Merke',
            'Zum Mitnehmen: e ist ungefähr zwei Komma sieben eins acht. Jede Exponentialfunktion lässt sich zur Basis e '
            'schreiben, a hoch x gleich e hoch b x mit b gleich ln a, und genauso zu jeder anderen Basis.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'a^{x} = e^{\fb{b}x}, \quad \fb{b} = \ln a', 410, 56, ein=0.4),
            n('@8^x = 2^{3x}@, @9^x = 3^{2x}@|@\\fb{b} \\gt 0@ Wachstum, @\\fb{b} \\lt 0@ Zerfall',
              540, 'blau', 44, ein=1.2),
            graf(W3, [ek([[0, 1, E, 0]], farbe=3, startpunkt={'farbe': 5})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-e-funktion', 'Exponentialkurve sehen: Kontrollfragen zur e-Funktion',
     'Fünf Vorhersagen zu e, Basiswechsel und Vorzeichen des Exponenten.',
     ['e-Funktion', 'Basiswechsel', 'Kontrollfragen'], [
         sz('Frage 1',
            'e ist ungefähr zwei Komma sieben eins acht, also zwischen zwei und drei.',
            f(r'e \approx 2.718', 300, 66, ein=1.0),
            n('nicht @\\pi@: das ist @3.14@', 440, 'rot', ein=2.4),
            graf(W3, [ek([[0, 1, E, 0]], farbe=3)], ein=1.2)),
         sz('Frage 2',
            'Neun ist drei Quadrat. Also ist neun hoch x gleich drei hoch zwei x.',
            f(r'9^{x} = \left(3^{2}\right)^{x} = 3^{\fb{2}x}', 300, 56, ein=1.0),
            n('@9 = 3^{\\fb{2}}@', 440, 'orange', ein=2.4),
            graf(W3, [ek([[0, 1, 9, 0]])], ein=1.2)),
         sz('Frage 3',
            'Der Exponent minus x macht aus dem Wachstum einen Zerfall: e hoch minus x fällt.',
            f(r'e^{-x} = \left(\tfrac{1}{e}\right)^{x}', 300, 58, ein=1.0),
            n('@\\fb{b} = -1 \\lt 0@: Zerfall', 440, 'orange', ein=2.4),
            graf(W3, [ek([[0, 1, 1 / E, 0]], farbe=3)], ein=1.2)),
         sz('Frage 4',
            'b ist ln zwei, ungefähr null Komma sechs neun. Denn e hoch ln zwei ist zwei.',
            f(r'b = \ln 2 \approx 0.69', 300, 62, ein=1.0),
            n('@e^{\\ln 2} = 2@', 440, 'orange', ein=2.4),
            graf(W3, [ek([[0, 1, 2, 0]]), ek([[0, 1, 2, 0]], farbe=3, gestrichelt=True)], ein=1.2)),
         sz('Frage 5',
            'Bei x gleich eins steht die Basis: e hoch eins ist e, ungefähr zwei Komma sieben.',
            f(r'e^{1} = e \approx 2.72', 300, 62, ein=1.0),
            n('der Punkt @(1 \\mid e)@', 440, 'gruen', ein=2.4),
            graf(W3, [ek([[0, 1, E, 0]], farbe=3)])),
         sz('Merke',
            'Zum Mitnehmen: e ist ungefähr zwei Komma sieben eins acht. Basiswechsel heisst: Basis als Potenz schreiben. '
            'Ein negativer Faktor im Exponenten bedeutet Zerfall.',
            titel('Zum Mitnehmen', 250, 76),
            n('@c^x = a^{bx}@ mit @c = a^b@|@a^x = e^{(\\ln a)\\,x}@|@b \\lt 0@: Zerfall',
              400, 'blau', 44, ein=1.2),
            graf(W3, [ek([[0, 1, E, 0]], farbe=3, startpunkt={'farbe': 5})])),
     ], [
         wahl('Frage 1', 'Welche Zahl ist e ungefähr?',
              ['2.718', '3.142', '2.5'], 0,
              {0: 'Ja.',
               1: 'Das ist π. e ist eine andere Zahl, zwischen 2 und 3.',
               2: 'Zu ungenau: Die Zinseszins-Folge geht über 2.7 hinaus.'},
              sprich='Welche Zahl ist e ungefähr?',
              rueck_sprich={1: 'Das ist pi. e ist eine andere Zahl, zwischen zwei und drei.',
                            2: 'Zu ungenau. Die Zinseszins-Folge geht über zwei Komma sieben hinaus.'}),
         wahl('Frage 2', '9ˣ = 3^(b·x): Wie gross ist b?',
              ['2', '3', '1/2'], 0,
              {0: 'Ja.',
               1: 'Welche Potenz von 3 ergibt 9?',
               2: 'Andersherum: 3 hoch b soll 9 sein, nicht 9 hoch b gleich 3.'},
              sprich='Neun hoch x ist gleich drei hoch b mal x. Wie gross ist b?',
              rueck_sprich={1: 'Welche Potenz von drei ergibt neun?',
                            2: 'Andersherum: Drei hoch b soll neun sein, nicht neun hoch b gleich drei.'}),
         wahl('Frage 3', 'Ist y = e^(−x) ein Wachstum oder ein Zerfall?',
              ['ein Zerfall', 'ein Wachstum', 'keines von beiden'], 0,
              {0: 'Ja.',
               1: 'Setz x = 1 und x = 2 ein: Werden die Werte grösser oder kleiner?',
               2: 'Es ist eine Exponentialfunktion mit der Basis 1/e.'},
              sprich='Ist y gleich e hoch minus x ein Wachstum oder ein Zerfall?',
              rueck_sprich={1: 'Setz x gleich eins und x gleich zwei ein. Werden die Werte grösser oder kleiner?',
                            2: 'Es ist eine Exponentialfunktion mit der Basis eins durch e.'}),
         wahl('Frage 4', '2ˣ = e^(b·x): Wie gross ist b?',
              ['ln 2 ≈ 0.69', '2/e ≈ 0.74', 'e/2 ≈ 1.36'], 0,
              {0: 'Ja.',
               1: 'Gesucht ist der Exponent b mit e^b = 2 — das ist ein Logarithmus.',
               2: 'Gesucht ist der Exponent b mit e^b = 2 — das ist ein Logarithmus.'},
              sprich='Zwei hoch x ist gleich e hoch b mal x. Wie gross ist b?',
              rueck_sprich={1: 'Gesucht ist der Exponent b mit e hoch b gleich zwei. Das ist ein Logarithmus.',
                            2: 'Gesucht ist der Exponent b mit e hoch b gleich zwei. Das ist ein Logarithmus.'}),
         klick('Frage 5', 'y = eˣ: Tipp den Punkt des Graphen bei x = 1 ins Bild.',
               [1, E], 'Getroffen: (1 | e) ≈ (1 | 2.72).',
               [{'bei': [1, 1], 'text': 'Das ist die Höhe bei x = 0. Bei x = 1 steht die Basis.',
                 'sprich': 'Das ist die Höhe bei x gleich null. Bei x gleich eins steht die Basis.'},
                {'bei': [1, 2], 'text': 'Etwas zu tief: e ist grösser als 2.',
                 'sprich': 'Etwas zu tief. e ist grösser als zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — bei x = 1 steht die Basis e.',
               sprich='y gleich e hoch x: Tipp den Punkt des Graphen bei x gleich eins ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Bei x gleich eins steht die Basis e.',
               tol=0.4),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# Beispiel: Kaffee f(t) = 20 + 60 e^(−kt) mit e^(−10k) = 1/2 (wie auf der Themenseite) — Startwert der Simulation 4.
WK = dict(xbereich=[-2, 45], ybereich=[-5, 95], yteilung=yt(20, 40, 60, 80), xteilung=yt(10, 20, 30, 40),
          xname='t [min]', yname='T [°C]')
Q = 0.5 ** 0.1      # e^(−k) mit k = ln 2 / 10
clip('saettigung', 'Exponentialkurve sehen: Sättigung',
     'Beschränktes Wachstum: Startwert, Sättigungswert und der Abstand dazwischen, der exponentiell abnimmt.',
     ['Sättigung', 'beschränktes Wachstum', 'Sättigungswert', 'Asymptote'], [
         sz('Ein Kaffee kühlt ab',
            'Ein Kaffee hat achtzig Grad und steht in einem Raum mit zwanzig Grad. Er kühlt ab, erst schnell, dann immer '
            'langsamer, und nähert sich der Raumtemperatur.',
            titel('Sättigung', 280, 80),
            f(r'f(t) = 20 + 60\,e^{-kt}', 430, 56, ein=4.0),
            # «erst schnell, dann immer langsamer» (5.4–8.8 s): ein Läufer fährt t = 0 → 40 (seit 07.10.2026);
            # ohne Text — eine Beschriftung rechts unten läge auf der Asymptote. Orange wie der Startpunkt,
            # den er verlässt.
            graf(WK, [dict(ek([[0, 60, Q, 20]], asymptote=True, startpunkt={'farbe': 2}),
                           laeufer={'bahn': [[5.3, 0], [8.8, 40]], 'farbe': 2})], ein=1.0)),
         sz('Startwert und Sättigungswert',
            'Zwanzig ist der Sättigungswert S, die waagrechte Asymptote. Achtzig ist der Startwert A. Dazwischen liegt '
            'der Rückstand: sechzig Grad am Anfang.',
            f(r'f(t) = 20 + 60\,e^{-kt}', 300, 56),
            n('Startwert @\\fb{A} = f(0) = 80@|Sättigungswert @S = 20@', 450, 'orange', ein=3.8),
            graf(WK, [ek([[0, 60, Q, 20]], asymptote=True, startpunkt={'farbe': 2})]),
            # «Dazwischen liegt der Rückstand» (5.8 s), «sechzig Grad» (7.2 s); endet am Rand des Startpunkts
            ueber(WK, figuren=[strecke([0, 20], [0, 78], 2, dicke=6)], ein=5.8),
            ueber(WK, figuren=[{'art': 'text', 'bei': [1.0, 47], 'text': '60', 'farbe': 2, 'kursiv': False, 'anker': 'start'}], ein=7.2)),
         sz('Der Rückstand zerfällt',
            'Der Abstand zur Raumtemperatur zerfällt exponentiell. Hier halbiert er sich alle zehn Minuten: sechzig, '
            'dreissig, fünfzehn, sieben Komma fünf Grad. Also fünfzig, fünfunddreissig, siebenundzwanzig Komma fünf Grad.',
            f(r'e^{-10k} = \tfrac12', 300, 56),
            n('Rückstand @60 \\to 30 \\to 15 \\to 7.5@', 440, 'orange', ein=4.0),
            # Abstand zur Asymptote einzeln zum Wort: «sechzig» 5.8, «dreissig» 6.45, «fünfzehn» 7.3, «sieben Komma fünf» 8.05;
            # die Temperaturen einzeln (ein je Teil, seit 07.10.2026): «fünfzig» 9.6, «fünfunddreissig» 10.4,
            # «siebenundzwanzig Komma fünf» 11.5 s — vorher standen alle drei ab 11.6 s.
            graf(WK, [ek([[0, 60, Q, 20]], asymptote=True)], ein=0.05,
                 strecken=[{'von': v_, 'bis': b_, 'farbe': 2, 'dicke': 6, 'ein': e_} for v_, b_, e_ in
                           (([0, 20], [0, 80], 5.8), ([10, 20], [10, 50], 6.45), ([20, 20], [20, 35], 7.3),
                            ([30, 20], [30, 27.5], 8.05))],
                 punkte=[dict(pt(10, 50, 5, '(10 | 50)', [11, 57]), ein=9.6),
                         dict(pt(20, 35, 5, '(20 | 35)', [21, 42]), ein=10.4),
                         dict(pt(30, 27.5, 5), ein=11.5)])),
         sz('Allgemein',
            'Allgemein: f von t gleich S minus Klammer S minus A, mal e hoch minus k t. Für grosse t geht e hoch minus k t '
            'gegen null, und f gegen S.',
            f(r'f(t) = S - (S - \fb{A})\,e^{-kt}, \quad k \gt 0', 300, 48),
            n('@t \\to \\infty@: @f(t) \\to S@|nie erreicht: Asymptote', 440, 'blau', ein=5.8),
            graf(WK, [ek([[0, 60, Q, 20]], asymptote=True)])),
         sz('Erwärmen',
            'Liegt der Startwert unter dem Sättigungswert, steigt die Kurve: zum Beispiel ein Akku, der von zwanzig auf '
            'hundert Prozent lädt. Die Form ist dieselbe, nur gespiegelt.',
            f(r'f(t) = 100 - 80\,e^{-kt}', 300, 54),
            n('@\\fb{A} \\lt S@: steigt; @\\fb{A} \\gt S@: fällt', 440, 'blau', ein=7.7),
            graf(dict(xbereich=[-0.3, 5], ybereich=[-5, 115], yteilung=yt(20, 40, 60, 80), xteilung=yt(1, 2, 3, 4),
                      xname='t [h]', yname='Ladung [%]'),
                 # «Liegt der Startwert unter dem Sättigungswert, steigt die Kurve» (1.2–3.2 s):
                 # A sinkt von S = 100 (waagrecht) auf 20, die Kurve biegt sich nach oben (wie A in sim4)
                 [ek([[1.2, 0, 0.5, 100], [3.2, -80, 0.5, 100]], asymptote=True, startpunkt={'farbe': 2})], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Bei der Sättigung nähert sich die Grösse dem Sättigungswert S, ohne ihn zu erreichen. '
            'Der Abstand zu S zerfällt exponentiell, und je grösser k, desto schneller. Startwert A, Sättigungswert S und k bestimmen den Verlauf.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'f(t) = S - (S - \fb{A})\,e^{-kt}', 410, 52, ein=0.4),
            n('@f(0) = \\fb{A}@; Asymptote @y = S@|Abstand @|S - f(t)|@ zerfällt',
              540, 'blau', 44, ein=1.2),
            # «je grösser k, desto schneller» (7.9–9.6 s): e^(−k) von 0.933 (k ≈ 0.07) auf 0.80 (k ≈ 0.22)
            graf(WK, [ek([[7.9, 60, Q, 20], [9.6, 60, 0.8, 20]], asymptote=True, startpunkt={'farbe': 2})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
WS = dict(xbereich=[-1.6, 12], ybereich=[-5, 115], yteilung=yt(20, 40, 60, 80, 100), xteilung=yt(2, 4, 6, 8, 10),
          xname='t', yname='y')
clip('kontrolle-saettigung', 'Exponentialkurve sehen: Kontrollfragen zur Sättigung',
     'Fünf Vorhersagen zu Startwert, Sättigungswert, Asymptote und Rückstand.',
     ['Sättigung', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei t gleich null ist e hoch null gleich eins: hundert minus achtzig ist zwanzig. Der Startwert ist zwanzig.',
            f(r'f(0) = 100 - 80 \cdot 1 = \fb{20}', 300, 56, ein=1.0),
            n('@e^0 = 1@', 440, 'orange', ein=2.4),
            graf(WS, [ek([[0, -80, math.exp(-0.5), 100]], startpunkt={'farbe': 2})], ein=1.2)),
         sz('Frage 2',
            'Für grosse t verschwindet der zweite Summand. Übrig bleibt hundert: der Sättigungswert.',
            f(r'e^{-0.5t} \to 0 \;\Rightarrow\; f(t) \to 100', 300, 52, ein=1.0),
            n('Asymptote @y = 100@', 440, 'blau', ein=2.4),
            graf(WS, [ek([[0, -80, math.exp(-0.5), 100]], asymptote=True)], ein=1.2)),
         sz('Frage 3',
            'Der Startwert achtzig liegt über dem Sättigungswert dreissig: Die Kurve fällt, wie ein abkühlender Körper.',
            f(r'f(t) = 30 + 50\,e^{-0.3t}', 300, 56, ein=1.0),
            n('@\\fb{A} = 80 \\gt S = 30@: fällt', 440, 'blau', ein=2.4),
            graf(WS, [ek([[0, 50, math.exp(-0.3), 30]], asymptote=True, startpunkt={'farbe': 2})], ein=1.2)),
         sz('Frage 4',
            'Halbiert sich der Rückstand alle zwei Minuten, ist er nach vier Minuten auf einen Viertel gesunken: '
            'achtzig geteilt durch vier ist zwanzig. f von vier ist also achtzig.',
            f(r'100 - 80 \cdot \tfrac14 = 80', 300, 56, ein=1.0),
            n('Rückstand @80 \\to 40 \\to 20@', 440, 'orange', ein=2.4),
            graf(WS, [ek([[0, -80, 0.5 ** 0.5, 100]], asymptote=True)], ein=1.2,
                 punkte=[pt(2, 60, 5), pt(4, 80, 5)])),
         sz('Frage 5',
            'Die Asymptote ist die Waagrechte auf der Höhe des Sättigungswerts, hier y gleich hundert.',
            f(r'y = S = 100', 300, 62, ein=1.0),
            n('nie erreicht, beliebig nahe', 440, 'blau', ein=2.4),
            graf(WS, [ek([[0, -80, math.exp(-0.5), 100]])])),
         sz('Merke',
            'Zum Mitnehmen: f von null ist der Startwert, die Asymptote liegt beim Sättigungswert, und der Rückstand zerfällt '
            'exponentiell.',
            titel('Zum Mitnehmen', 250, 76),
            n('@f(0) = \\fb{A}@|@y = S@ Asymptote|Rückstand: in gleichen Zeiten halbiert',
              400, 'blau', 44, ein=1.2),
            graf(WS, [ek([[0, -80, math.exp(-0.5), 100]], asymptote=True, startpunkt={'farbe': 2})])),
     ], [
         wahl('Frage 1', 'f(t) = 100 − 80·e^(−0.5t): Wie gross ist der Startwert f(0)?',
              ['20', '100', '−80'], 0,
              {0: 'Ja.',
               1: 'Das ist der Sättigungswert. Setz t = 0 ein: Was ist e⁰?',
               2: 'Setz t = 0 ein: 100 − 80 · e⁰.'},
              sprich='f von t gleich hundert minus achtzig mal e hoch minus null Komma fünf t: Wie gross ist der Startwert f von null?',
              rueck_sprich={1: 'Das ist der Sättigungswert. Setz t gleich null ein: Was ist e hoch null?',
                            2: 'Setz t gleich null ein: hundert minus achtzig mal e hoch null.'}),
         wahl('Frage 2', 'Gegen welchen Wert strebt f(t) = 100 − 80·e^(−0.5t) für grosse t?',
              ['100', '20', '0'], 0,
              {0: 'Ja.',
               1: 'Das ist der Startwert. Was geschieht mit e^(−0.5t), wenn t gross wird?',
               2: 'Nur der zweite Summand verschwindet, die 100 bleibt.'},
              sprich='Gegen welchen Wert strebt f von t gleich hundert minus achtzig mal e hoch minus null Komma fünf t für grosse t?',
              rueck_sprich={1: 'Das ist der Startwert. Was geschieht mit e hoch minus null Komma fünf t, wenn t gross wird?',
                            2: 'Nur der zweite Summand verschwindet, die hundert bleibt.'}),
         wahl('Frage 3', 'f(t) = 30 + 50·e^(−0.3t): Steigt oder fällt die Kurve?',
              ['Sie fällt — von 80 auf 30 zu.', 'Sie steigt — von 30 auf 80 zu.', 'Sie steigt ohne Grenze.'], 0,
              {0: 'Ja.',
               1: 'Rechne den Startwert f(0) aus.',
               2: 'e^(−0.3t) wird kleiner. Gibt es eine Asymptote?'},
              sprich='f von t gleich dreissig plus fünfzig mal e hoch minus null Komma drei t: Steigt oder fällt die Kurve?',
              rueck_sprich={1: 'Rechne den Startwert f von null aus.',
                            2: 'e hoch minus null Komma drei t wird kleiner. Gibt es eine Asymptote?'}),
         wahl('Frage 4', 'Der Rückstand halbiert sich alle 2 Minuten, f(t) = 100 − 80·e^(−kt). Wie gross ist f(4)?',
              ['80', '60', '90'], 0,
              {0: 'Ja.',
               1: 'Das ist f(2). Nach 4 Minuten ist zweimal halbiert.',
               2: 'Rechne den Rückstand: 80, dann 40, dann …'},
              sprich='Der Rückstand halbiert sich alle zwei Minuten, f von t gleich hundert minus achtzig mal e hoch minus k t. '
                     'Wie gross ist f von vier?',
              rueck_sprich={1: 'Das ist f von zwei. Nach vier Minuten ist zweimal halbiert.',
                            2: 'Rechne den Rückstand: achtzig, dann vierzig, dann …'}),
         # Bei t = 2 liegt die Kurve bei 70.6 — weit genug unter der Asymptote, dass ein Tipp auf
         # die Kurve nicht als Treffer gilt (bei t = 8 läge sie nur 1.5 darunter).
         klick('Frage 5', 'Tipp die Stelle der waagrechten Asymptote dieser Kurve bei t = 2 ins Bild.',
               [2, 100], 'Getroffen: Die Asymptote ist y = 100.',
               [{'bei': [2, 70.6], 'text': 'Das ist die Kurve selbst. Die Asymptote liegt dort, wohin die Kurve strebt.',
                 'sprich': 'Das ist die Kurve selbst. Die Asymptote liegt dort, wohin die Kurve strebt.'},
                {'bei': [2, 20], 'text': 'Das ist die Höhe des Startwerts. Die Asymptote liegt dort, wohin die Kurve strebt.',
                 'sprich': 'Das ist die Höhe des Startwerts. Die Asymptote liegt dort, wohin die Kurve strebt.'},
                {'bei': [2, 0], 'text': 'Die x-Achse ist hier keine Asymptote: Die Kurve ist um 100 verschoben.',
                 'sprich': 'Die x-Achse ist hier keine Asymptote. Die Kurve ist um hundert verschoben.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — wohin strebt die Kurve?',
               sprich='Tipp die Stelle der waagrechten Asymptote dieser Kurve bei t gleich zwei ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Wohin strebt die Kurve?',
               # y-Einheiten sind hier klein (120 auf 744 px): 4 Einheiten ≈ 25 px.
               tol=4, eingabe=('t', 'y')),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
# Beispiel: 2^x und log₂ x — Startwert der Simulation 5.
WL = dict(xbereich=[-3, 9], ybereich=[-3, 9], yteilung=yt(-2, 2, 4, 6, 8), xteilung=yt(-2, 2, 4, 6, 8))
clip('logarithmusfunktion', 'Exponentialkurve sehen: die Logarithmusfunktion',
     'Die Logarithmusfunktion als Umkehrfunktion: Spiegelung an y = x, (1 | 0), die y-Achse als Asymptote, Gleichungen mit x im Exponenten.',
     ['Logarithmusfunktion', 'Umkehrfunktion', 'Spiegelung', 'Logarithmus'], [
         sz('Die Umkehrfrage',
            'Zwei hoch x beantwortet: Was kommt nach x Schritten heraus? Die Umkehrfrage lautet: Wie viele Schritte '
            'braucht es bis acht? Die Antwort ist drei, der Logarithmus von acht zur Basis zwei.',
            titel('Die Umkehrfrage', 280, 80),
            f(r'2^{x} = 8 \;\Leftrightarrow\; x = \log_2 8 = 3', 430, 52, ein=7.2),
            graf(WL, [ek([[0, 1, 2, 0]])], ein=1.0),
            # Leserichtung: «bis acht» (4.3 s) waagrecht von y = 8 zur Kurve, «drei» (6.3 s) hinunter zu x = 3
            ueber(WL, figuren=[strecke([0, 8], [3, 8], 5, True, 3)], ein=4.3),
            ueber(WL, figuren=[strecke([3, 8], [3, 0], 5, True, 3),
                               {'art': 'text', 'bei': [3, -0.55], 'text': '3', 'farbe': 5, 'kursiv': False,
                                'groesse': 24}], ein=6.3),
            graf(WL, [ek([[0, 1, 2, 0]], marken=[{'x': 3, 'text': '(3 | 8)', 'farbe': 1}])], ein=6.0)),
         sz('Spiegeln',
            'Die Logarithmusfunktion ist die Umkehrfunktion. Ihr Graph ist das Spiegelbild der Exponentialkurve an der '
            'Winkelhalbierenden y gleich x. Aus drei, acht wird acht, drei.',
            f(r'y = \fc{\log_2 x}', 300, 62),
            n('Spiegelung an @y = x@:|@(x \\mid y) \\to (y \\mid x)@', 440, 'gruen', ein=3.0),
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})], ein=0.05),
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})], ein=8.8,
                 punkte=[pt(3, 8, 1, '(3 | 8)', [3.4, 8.3]), pt(8, 3, 3, '(8 | 3)', [7.6, 3.9], 'end')])),
         sz('Was sich vertauscht',
            'Beim Spiegeln tauschen die Rollen. Aus null, eins wird eins, null: die Nullstelle. Aus der x-Achse als '
            'Asymptote wird die y-Achse. Und die Definitionsmenge sind nur die positiven Zahlen.',
            f(r'(0 \mid 1) \to (1 \mid 0)', 300, 56),
            # Notiz zeilenweise zum Ton: «die Nullstelle» 3.8, «Asymptote» 6.5, «Definitionsmenge» 8.9
            n('Nullstelle @x_0 = 1@', 420, 'gruen', ein=3.8),
            n('Asymptote @x = 0@', 477, 'gruen', ein=6.5),
            n('@D = \\mathbb{R}^+@, @W = \\mathbb{R}@', 534, 'gruen', ein=8.9),
            # Beschriftung (1 | 0) unter die Achse, rechts — sonst sitzt sie auf der Achszahl 2
            # Läufer wie in sim5 (seit 07.10.2026), Start bei x = 4: «Asymptote … wird die y-Achse» (6.3–8.2 s)
            # fährt er hinunter an die y-Achse, durch die Nullstelle ins Negative.
            graf(WL, [dict(lk([[0, 1, 2, 0]], asymptote=True),
                           laeufer={'bahn': [[6.3, 4], [8.2, 0.25]], 'text': '({x} | {y})', 'farbe': 3})],
                 punkte=[pt(1, 0, 3, '(1 | 0)', [1.3, -1.0])])),
         sz('Die Basis',
            'Wie bei der Exponentialfunktion entscheidet die Basis. Bei Basis grösser als eins steigt die Kurve, immer '
            'flacher, aber ohne Grenze. Bei Basis kleiner als eins fällt sie.',
            f(r'y = \log_{\fa{a}} x', 300, 62),
            n('@\\fa{a} \\gt 1@ steigt; @\\fa{a} \\lt 1@ fällt|alle durch @(1 \\mid 0)@', 440, 'gruen', ein=3.4),
            graf(WL, [lk([[0.4, 1, 2, 0], [3.2, 1, 10, 0], [7.8, 1, 10, 0], [9.6, 1, 0.5, 0]], startpunkt={'farbe': 5})])),
         sz('Gleichungen lösen',
            'Und so löst man eine Gleichung mit x im Exponenten: drei mal zwei hoch t gleich sechsundneunzig. '
            'Erst teilen: zwei hoch t gleich zweiunddreissig. Dann logarithmieren: t gleich fünf.',
            f(r'3 \cdot 2^{t} = 96', 300, 56),
            f(r'2^{t} = 32 \;\Rightarrow\; t = \log_2 32 = 5', 390, 50, ein=5.8),
            n('erst die Potenz freistellen,|dann logarithmieren', 500, 'blau', 44, ein=8.8),
            graf(dict(xbereich=[-0.5, 6.5], ybereich=[-5, 110], yteilung=yt(20, 40, 60, 80, 100), xteilung=yt(1, 2, 3, 4, 5, 6),
                      xname='t', yname='y'),
                 [ek([[0, 3, 2, 0]]), fest('96', farbe=5)], ein=1.0),
            graf(dict(xbereich=[-0.5, 6.5], ybereich=[-5, 110], yteilung=yt(20, 40, 60, 80, 100), xteilung=yt(1, 2, 3, 4, 5, 6),
                      xname='t', yname='y'),
                 [ek([[0, 3, 2, 0]]), fest('96', farbe=5)], ein=8.6, punkte=[pt(5, 96, 3, '(5 | 96)', [4.6, 104], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: Die Logarithmusfunktion ist die Umkehrfunktion der Exponentialfunktion, gespiegelt an y gleich x. '
            'Sie geht durch eins, null, hat die y-Achse als Asymptote und ist nur für positive x definiert.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'y = a^x \;\Leftrightarrow\; x = \log_a y', 410, 54, ein=0.4),
            n('@(1 \\mid 0)@; Asymptote @x = 0@|@D = \\mathbb{R}^+@|Gleichung: Potenz freistellen, logarithmieren',
              540, 'blau', 44, ein=1.2),
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})]),
            # «Sie geht durch eins, null» (7.6 s), «hat die y-Achse als Asymptote» (9.3 s)
            ueber(WL, [pt(1, 0, 3, '(1 | 0)', [1.3, -1.0])], ein=7.6),
            ueber(WL, figuren=[strecke([0, -3], [0, 9], 3, True, 5),
                               {'art': 'text', 'bei': [0.3, 7.0], 'text': 'x = 0', 'farbe': 3, 'anker': 'start'}],
                  ein=9.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
clip('kontrolle-logarithmus', 'Exponentialkurve sehen: Kontrollfragen zur Logarithmusfunktion',
     'Fünf Vorhersagen zu Logarithmen, Definitionsmenge, Spiegelpunkten und Gleichungen.',
     ['Logarithmusfunktion', 'Umkehrfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zwei hoch fünf ist zweiunddreissig. Also ist der Logarithmus von zweiunddreissig zur Basis zwei gleich fünf.',
            f(r'2^{5} = 32 \;\Rightarrow\; \log_2 32 = 5', 300, 54, ein=1.0),
            n('der gesuchte Exponent', 440, 'gruen', ein=2.4),
            graf(WL, [lk([[0, 1, 2, 0]], marken=[{'x': 8, 'text': '(8 | 3)', 'farbe': 3}])], ein=1.2)),
         sz('Frage 2',
            'Nur positive Zahlen haben einen Logarithmus, denn a hoch y ist immer positiv. Die Definitionsmenge ist R plus.',
            f(r'D = \mathbb{R}^+', 300, 66, ein=1.0),
            n('@\\log_2 0@, @\\log_2(-4)@: gibt es nicht', 440, 'rot', ein=2.4),
            graf(WL, [lk([[0, 1, 2, 0]], asymptote=True)], ein=1.2)),
         sz('Frage 3',
            'Spiegeln an y gleich x vertauscht die Koordinaten: Aus zwei, vier wird vier, zwei.',
            f(r'(2 \mid 4) \to (4 \mid 2)', 300, 58, ein=1.0),
            n('@\\log_2 4 = 2@', 440, 'gruen', ein=2.4),
            # Ohne Punkte beim Erscheinen der Frage (§15): sie kämen erst danach.
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})]),
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})], ein=2.4,
                 punkte=[pt(2, 4, 1, '(2 | 4)', [1.6, 4.9], 'end'), pt(4, 2, 3, '(4 | 2)', [4.4, 1.2])])),
         sz('Frage 4',
            'Umkehrfunktion: nach x auflösen, dann tauschen. y plus eins gleich drei hoch x, also x gleich log drei von '
            'Klammer y plus eins. Getauscht: y gleich log drei von Klammer x plus eins.',
            f(r'y = 3^{x} - 1 \;\Rightarrow\; x = \log_3(y + 1)', 300, 48, ein=1.0),
            f(r'f^{-1}(x) = \fc{\log_3(x + 1)}', 400, 50, ein=6.0),
            graf(dict(xbereich=[-3, 6], ybereich=[-3, 6], yteilung=yt(-2, 2, 4), xteilung=yt(-2, 2, 4)),
                 [fest('x', farbe=5), ek([[0, 1, 3, -1]], spiegel={'farbe': 3})], ein=1.2)),
         sz('Frage 5',
            'Zwei hoch t gleich vierundsechzig. Vierundsechzig ist zwei hoch sechs: t gleich sechs.',
            f(r'2^{t} = 64 = 2^{6} \;\Rightarrow\; t = 6', 300, 52, ein=1.0),
            n('@t = \\log_2 64@', 440, 'gruen', ein=2.4),
            graf(WL, [lk([[0, 1, 2, 0]])], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Der Logarithmus ist der gesuchte Exponent. Definiert nur für positive Zahlen. Und die Umkehrfunktion '
            'bekommt man durch Auflösen und Tauschen.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\log_a y@ = gesuchter Exponent|@D = \\mathbb{R}^+@|auflösen, dann @x@ und @y@ tauschen',
              400, 'blau', 44, ein=1.2),
            graf(WL, [fest('x', farbe=5), ek([[0, 1, 2, 0]], spiegel={'farbe': 3})])),
     ], [
         wahl('Frage 1', 'Wie gross ist log₂ 32?',
              ['5', '16', '6'], 0,
              {0: 'Ja.',
               1: 'Der Logarithmus ist ein Exponent, kein Quotient. 2 hoch wie viel ist 32?',
               2: 'Rechne 2⁶ aus — ist das 32?'},
              sprich='Wie gross ist der Logarithmus von zweiunddreissig zur Basis zwei?',
              rueck_sprich={1: 'Der Logarithmus ist ein Exponent, kein Quotient. Zwei hoch wie viel ist zweiunddreissig?',
                            2: 'Rechne zwei hoch sechs aus. Ist das zweiunddreissig?'}),
         wahl('Frage 2', 'Welche Definitionsmenge hat y = log₂ x?',
              ['ℝ⁺ (nur positive x)', 'ℝ (alle x)', 'ℝ ∖ {0}'], 0,
              {0: 'Ja.',
               1: 'Gibt es einen Exponenten y mit 2^y = −4?',
               2: 'Und die negativen Zahlen? Gibt es 2^y = −4?'},
              sprich='Welche Definitionsmenge hat y gleich Logarithmus zur Basis zwei von x?',
              rueck_sprich={1: 'Gibt es einen Exponenten y mit zwei hoch y gleich minus vier?',
                            2: 'Und die negativen Zahlen? Gibt es zwei hoch y gleich minus vier?'}),
         klick('Frage 3', '(2 | 4) liegt auf y = 2ˣ. Tipp den Spiegelpunkt auf y = log₂ x ins Bild.',
               [4, 2], 'Getroffen: (4 | 2).',
               [{'bei': [2, 4], 'text': 'Das ist der Punkt selbst. Beim Spiegeln an y = x tauschen die Koordinaten.',
                 'sprich': 'Das ist der Punkt selbst. Beim Spiegeln an y gleich x tauschen die Koordinaten.'},
                {'bei': [-2, -4], 'text': 'Kein Vorzeichenwechsel: Gespiegelt wird an y = x, nicht am Ursprung.',
                 'sprich': 'Kein Vorzeichenwechsel. Gespiegelt wird an y gleich x, nicht am Ursprung.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — aus (x | y) wird (y | x).',
               sprich='Zwei, vier liegt auf y gleich zwei hoch x. Tipp den Spiegelpunkt auf y gleich Logarithmus zur Basis zwei von x ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Aus x, y wird y, x.'),
         wahl('Frage 4', 'Welche Umkehrfunktion hat f(x) = 3ˣ − 1?',
              ['log₃(x + 1)', 'log₃(x) + 1', 'log₃(x − 1)'], 0,
              {0: 'Ja.',
               1: 'Löse y = 3ˣ − 1 zuerst nach 3ˣ auf, dann logarithmieren.',
               2: 'Vorzeichen: Die −1 wandert auf die andere Seite.'},
              sprich='Welche Umkehrfunktion hat f von x gleich drei hoch x minus eins?',
              rueck_sprich={1: 'Löse y gleich drei hoch x minus eins zuerst nach drei hoch x auf, dann logarithmieren.',
                            2: 'Vorzeichen: Die minus eins wandert auf die andere Seite.'}),
         wahl('Frage 5', 'Löse 2ᵗ = 64.',
              ['t = 6', 't = 32', 't = 8'], 0,
              {0: 'Ja.',
               1: 'Nicht teilen: 2 hoch wie viel ist 64?',
               2: '8 ist die Wurzel von 64, nicht der Exponent zur Basis 2.'},
              sprich='Löse zwei hoch t gleich vierundsechzig.',
              rueck_sprich={1: 'Nicht teilen. Zwei hoch wie viel ist vierundsechzig?',
                            2: 'Acht ist die Wurzel von vierundsechzig, nicht der Exponent zur Basis zwei.'}),
     ], art='Kontrollclip')
