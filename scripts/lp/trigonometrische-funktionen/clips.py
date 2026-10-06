"""Erzeugt die zehn Drehbücher des Leitprogramms Trigonometrische Funktionen (05.10.2026).

  python3 scripts/lp/trigonometrische-funktionen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau anders als bei den Vorbildern: Eine Sinuskurve braucht Breite, nicht Höhe. Darum
steht das Bild **unten über die ganze Bühne** (x 140, y 500, 1640 × 480), Formeln und Notizen
darüber (x 150, y 230 bis 440). Theme begreifbar-schlicht.

**Bewegte Kurven** (HOWTO-clips.md, «Sinus- und Tangenskurven»): `sk([[t, a, b, u, v], …])`
für y = a·sin(b(x − u)) + v, `tk(…)` für den Tangens. `kreis` zeichnet den Einheitskreis
links neben der Kurve, mit einem Punkt P, der der `bahn` [[t, Winkel], …] folgt; mit
`spur` entsteht die Kurve erst beim Abrollen.

Farben — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15), gleich wie auf der Seite:
  1 blau   = Sinuskurve und Sinuswert                 \\fa{…}
  2 orange = Tangenskurve und Tangenswert            \\fb{…}
  3 grün   = Cosinuskurve und Cosinuswert            \\fc{…}
  4 rot    = Gegenbeispiel, falscher Weg             \\fd{…}
  5 Tinte  = neutral: Einheitskreis, Mittellinie, Pole, Waagrechte y = c, Bezugskurve
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
GX, GY, GB, GH, LX = 140, 500, 1640, 480, 150
P = math.pi
H2 = P / 2


def graf(W, kurven=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=[], punkte=list(punkte), pfeile=True, **W)
    g.update(kw)
    return g


def _trig(typ, stuetz, farbe, linien, kreis, marken, von, bis, gestrichelt, dicke):
    d = {'bewegung': stuetz, 'trig': typ, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if linien:
        d['asymptoten'] = {'farbe': 5}
    if kreis is not None:
        d['kreis'] = kreis
    if marken is not None:
        d['marken'] = marken
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


def sk(stuetz, farbe=1, mittel=False, kreis=None, marken=None, von=None, bis=None, gestrichelt=False, dicke=None):
    """Bewegte Sinuskurve: Stützpunkte [t, a, b, u, v] für a·sin(b(x − u)) + v; mittel = Mittellinie y = v.
    Mit Einheitskreis beginnt die Kurve bei x = 0 — links der y-Achse steht der Kreis."""
    if kreis is not None and von is None:
        von = 0
    return _trig('sin', stuetz, farbe, mittel, kreis, marken, von, bis, gestrichelt, dicke)


def ck(farbe=3, **kw):
    """Die Cosinuskurve als Sinus, um π/2 nach links verschoben (cos x = sin(x + π/2))."""
    return sk([[0, 1, 1, -H2, 0]], farbe=farbe, **kw)


def tk(stuetz, farbe=2, pole=False, kreis=None, marken=None, von=None, bis=None, gestrichelt=False, dicke=None):
    """Bewegte Tangenskurve: Stützpunkte [t, a, b, u, v]; pole = die Polgeraden."""
    return _trig('tan', stuetz, farbe, pole, kreis, marken, von, bis, gestrichelt, dicke)


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


def f(t, y=240, g=60, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y=350, farbe='blau', g=44, ein=2.4, x=LX):
    return dict(typ='notiz', text=t, x=x, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=250, g=82):
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
          tol=0.3, bei=0.3, eingabe=('x', 'y')):
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
    alt = R + 'clips/s3-5-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 's3-5-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Trigonometrische Funktionen',
         'fach': 'Schwerpunktfach', 'lerngebiet': '3 · Funktionen',
         'lektion': ['s3-5'], 'stufe': ['BM2'], 'datum': '2026-10-05',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Sinuskurve sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms trigonometrische-funktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    anwenden_fragebild(d)                               # beim Fragen nur das Gegebene
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


NAMEN = {-8: '−4π', -6: '−3π', -4: '−2π', -3: '−3π/2', -2: '−π', -1: '−π/2', 1: 'π/2', 2: 'π', 3: '3π/2',
         4: '2π', 5: '5π/2', 6: '3π', 7: '7π/2', 8: '4π'}


def pit(*halbe):
    """Teilung der x-Achse in Vielfachen von π/2: pit(1, 2, 3, 4) → π/2, π, 3π/2, 2π."""
    return [[k * H2, NAMEN[k]] for k in halbe]


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


# Fenster. x im Bogenmass; der Einheitskreis steht links der y-Achse (Mittelpunkt x = −1.6).
WK = dict(xbereich=[-2.9, 6.9], ybereich=[-1.5, 1.5], xteilung=pit(1, 2, 3, 4), yteilung=yt(-1, 1))
WP = dict(xbereich=[-7.2, 13.4], ybereich=[-1.5, 1.5], xteilung=pit(-4, -2, 2, 4, 6, 8), yteilung=yt(-1, 1))
WS = dict(xbereich=[-4.6, 8.2], ybereich=[-1.5, 1.5], xteilung=pit(-2, -1, 1, 2, 3, 4), yteilung=yt(-1, 1))
WT = dict(xbereich=[-2.6, 7.2], ybereich=[-3, 3], xteilung=pit(1, 2, 3, 4), yteilung=yt(-2, -1, 1, 2))
WTP = dict(xbereich=[-5.6, 8.2], ybereich=[-3, 3], xteilung=pit(-3, -2, -1, 1, 2, 3, 4), yteilung=yt(-2, -1, 1, 2))
WA = dict(xbereich=[-0.8, 6.9], ybereich=[-3.4, 3.4], xteilung=pit(1, 2, 3, 4), yteilung=yt(-3, -2, -1, 1, 2, 3))
WG = dict(xbereich=[-0.8, 13.4], ybereich=[-1.5, 1.5], xteilung=pit(1, 2, 3, 4, 5, 6, 7, 8), yteilung=yt(-1, 1))
def KREIS(bahn, spur=True, projektion=True, cos=False):
    d = {'mx': -1.6, 'bahn': bahn, 'spur': spur, 'farbe': 3 if cos else 1}
    if not projektion:
        d['projektion'] = False
    if cos:
        d['art'] = 'cos'
    return d

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('kreis-kurve', 'Sinuskurve sehen: vom Einheitskreis zur Kurve',
     'Ein Punkt läuft auf dem Einheitskreis, seine Höhe wird zur Sinuskurve: Bogenmass, fünf Stützstellen und die Cosinuskurve.',
     ['Sinusfunktion', 'Cosinusfunktion', 'Einheitskreis', 'Bogenmass'], [
         sz('Bogenmass',
            'Am Einheitskreis misst man Winkel im Bogenmass: mit der Länge des Bogens. Der ganze Umfang ist zwei pi. '
            'Hundertachtzig Grad sind also pi, neunzig Grad pi halbe.',
            titel('Vom Kreis zur Kurve', 250, 80),
            f(r'360^\circ = 2\pi \qquad 180^\circ = \pi \qquad 90^\circ = \tfrac{\pi}{2}', 380, 54, ein=3.2),
            graf(WK, [sk([[0, 1, 1, 0, 0]], kreis=KREIS([[0, 0], [3.2, 0], [6.0, 2 * P], [6.4, 2 * P], [8.2, P], [8.7, P], [9.8, H2]], spur=False, projektion=False), von=9, bis=9)], ein=1.0)),
         sz('Abrollen',
            'Ein Punkt P läuft auf dem Einheitskreis. Seine Höhe ist der Sinus des Winkels x. Diese Höhe tragen wir über x ab. '
            'Bei pi halbe ist P ganz oben: Sinus gleich eins. Bei pi liegt er wieder auf der x-Achse, bei drei pi halbe ganz unten, '
            'und bei zwei pi ist er zurück am Start.',
            f(r'y = \fa{\sin x}', 240, 66),
            n('Höhe von @P@ über dem Winkel @x@', 350, 'blau', ein=2.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], kreis=KREIS([[0, 0], [4.0, 0], [8.4, H2], [8.8, H2], [10.8, P], [13.4, 3 * H2], [15.8, 2 * P]]))])),
         sz('Fünf Stützstellen',
            'Fünf Stellen genügen für eine Skizze: null, pi halbe, pi, drei pi halbe und zwei pi. Dort hat der Sinus die Werte '
            'null, eins, null, minus eins, null. Dazwischen zieht man einen weichen Bogen.',
            f(r'\begin{array}{c|ccccc} x & 0 & \tfrac{\pi}{2} & \pi & \tfrac{3\pi}{2} & 2\pi \\ \hline \sin x & 0 & 1 & 0 & -1 & 0 \end{array}',
              250, 40, ein=2.6),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P)], ein=0.3,
                 punkte=[pt(0, 0, 1), pt(H2, 1, 1), pt(P, 0, 1), pt(3 * H2, -1, 1), pt(2 * P, 0, 1)])),
         sz('Der Cosinus',
            'Der Cosinus ist die waagrechte Koordinate von P. Er startet bei eins, ist bei pi halbe null, bei pi minus eins, '
            'bei drei pi halbe wieder null und bei zwei pi wieder eins. Seine Kurve hat dieselbe Form, sie beginnt nur oben.',
            f(r'y = \fc{\cos x}', 240, 66),
            f(r'\begin{array}{c|ccccc} x & 0 & \tfrac{\pi}{2} & \pi & \tfrac{3\pi}{2} & 2\pi \\ \hline \cos x & 1 & 0 & -1 & 0 & 1 \end{array}',
              330, 36, ein=3.2, x=780),
            graf(WK, [ck(kreis=KREIS([[0, 0], [5.0, 0], [6.4, H2], [7.8, P], [9.4, 3 * H2], [11.6, 2 * P]], cos=True))], ein=0.6)),
         sz('Merke',
            'Zum Mitnehmen: P auf dem Einheitskreis hat die Koordinaten Cosinus x und Sinus x. Abgerollt über x ergibt die Höhe '
            'die Sinuskurve, die waagrechte Koordinate die Cosinuskurve. Beide bleiben zwischen minus eins und eins.',
            titel('Zum Mitnehmen', 240, 72),
            n('@P = (\\fc{\\cos x} \\mid \\fa{\\sin x})@|Werte zwischen @-1@ und @1@', 350, 'blau', 44, ein=1.4),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), ck(von=0, bis=2 * P)], ein=0.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-kreis-kurve', 'Sinuskurve sehen: Kontrollfragen zum Einheitskreis',
     'Fünf Vorhersagen zu Bogenmass, Sinus- und Cosinuswerten und zum Tiefpunkt der Sinuskurve.',
     ['Sinusfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zweihundertsiebzig Grad sind drei Viertel des Kreises. Drei Viertel von zwei pi sind drei pi halbe.',
            f(r'270^\circ = \tfrac{270}{180}\,\pi = \tfrac{3\pi}{2}', 240, 56, ein=1.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], kreis=KREIS([[0, 3 * H2]], spur=False, projektion=False), von=9, bis=9)], ein=1.2)),
         sz('Frage 2',
            'Bei pi liegt der Punkt P links auf der x-Achse. Seine Höhe ist null: Sinus von pi gleich null.',
            f(r'\sin \pi = 0', 240, 62, ein=1.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], kreis=KREIS([[0, P]]))], ein=1.2)),
         sz('Frage 3',
            'Der Tiefpunkt liegt bei drei pi halbe. Dort ist P ganz unten, der Sinus ist minus eins.',
            f(r'\sin \tfrac{3\pi}{2} = -1', 240, 60, ein=1.4),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P)]),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P)], ein=1.4,
                 punkte=[pt(3 * H2, -1, 1, '(3π/2 | −1)', [3 * H2 + 0.25, -1.15])])),
         sz('Frage 4',
            'Der Cosinus ist die waagrechte Koordinate. Ganz links auf dem Kreis ist sie minus eins: bei pi.',
            f(r'\cos \pi = -1', 240, 62, ein=1.0),
            graf(WK, [ck(von=0, bis=2 * P)], ein=1.2, punkte=[pt(P, -1, 3, '(π | −1)', [P + 0.2, -1.2])])),
         sz('Frage 5',
            'Der Sinus ist die Höhe, also die zweite Koordinate: null Komma acht. Die erste, null Komma sechs, ist der Cosinus.',
            f(r'P = (\fc{0.6} \mid \fa{0.8}) \;\Rightarrow\; \sin x = \fa{0.8}', 240, 52, ein=1.0),
            n('erste Koordinate: @\\cos x@; zweite: @\\sin x@', 350, 'blau', ein=3.6)),
         sz('Merke',
            'Zum Mitnehmen: pi ist hundertachtzig Grad. Der Sinus ist die Höhe von P, der Cosinus die waagrechte Koordinate. '
            'Die Sinuskurve hat bei pi halbe ihren Hochpunkt und bei drei pi halbe ihren Tiefpunkt.',
            titel('Zum Mitnehmen', 240, 72),
            n('@\\pi = 180^\\circ@|Hochpunkt @\\left(\\tfrac{\\pi}{2} \\mid 1\\right)@, Tiefpunkt @\\left(\\tfrac{3\\pi}{2} \\mid -1\\right)@',
              350, 'blau', 44, ein=1.2),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P)], ein=0.3)),
     ], [
         wahl('Frage 1', 'Wie viel sind 270° im Bogenmass?',
              ['3π/2', '3π/4', '2π/3'], 0,
              {0: 'Ja.',
               1: '180° sind π. Wie viele Mal π sind 270°?',
               2: 'Das wären 120°. 180° sind π — und 270°?'},
              sprich='Wie viel sind zweihundertsiebzig Grad im Bogenmass?',
              rueck_sprich={1: 'Hundertachtzig Grad sind pi. Wie viele Mal pi sind zweihundertsiebzig Grad?',
                            2: 'Das wären hundertzwanzig Grad. Hundertachtzig Grad sind pi, und zweihundertsiebzig Grad?'}),
         wahl('Frage 2', 'Welchen Wert hat sin π?',
              ['0', '1', '−1'], 0,
              {0: 'Ja.',
               1: 'Bei π liegt P links auf der x-Achse. Wie hoch liegt er?',
               2: '−1 ist der tiefste Punkt, bei 3π/2. Wo liegt P bei π?'},
              sprich='Welchen Wert hat Sinus von pi?',
              rueck_sprich={1: 'Bei pi liegt P links auf der x-Achse. Wie hoch liegt er?',
                            2: 'Minus eins ist der tiefste Punkt, bei drei pi halbe. Wo liegt P bei pi?'}),
         klick('Frage 3', 'Tipp den Tiefpunkt der Sinuskurve zwischen 0 und 2π ins Bild.',
               [3 * H2, -1], 'Getroffen: (3π/2 | −1).',
               [{'bei': [H2, 1], 'text': 'Das ist der Hochpunkt. Gesucht ist der tiefste Punkt.',
                 'sprich': 'Das ist der Hochpunkt. Gesucht ist der tiefste Punkt.'},
                {'bei': [P, 0], 'text': 'Hier schneidet die Kurve die x-Achse. Wo ist sie am tiefsten?',
                 'sprich': 'Hier schneidet die Kurve die x-Achse. Wo ist sie am tiefsten?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp den Tiefpunkt der Sinuskurve zwischen null und zwei pi ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 4', 'Wo hat cos x zwischen 0 und 2π den Wert −1?',
              ['bei π', 'bei 3π/2', 'bei 0'], 0,
              {0: 'Ja.',
               1: 'Bei 3π/2 ist P ganz unten: Das ist der Sinus. Der Cosinus ist die waagrechte Koordinate.',
               2: 'Bei 0 ist cos x = 1. Wo liegt P ganz links?'},
              sprich='Wo hat Cosinus x zwischen null und zwei pi den Wert minus eins?',
              rueck_sprich={1: 'Bei drei pi halbe ist P ganz unten. Das ist der Sinus. Der Cosinus ist die waagrechte Koordinate.',
                            2: 'Bei null ist Cosinus x gleich eins. Wo liegt P ganz links?'}),
         wahl('Frage 5', 'P = (0.6 | 0.8) liegt auf dem Einheitskreis. Wie gross ist sin x?',
              ['0.8', '0.6', '1.4'], 0,
              {0: 'Ja.',
               1: 'Das ist die erste Koordinate, der Cosinus. Der Sinus ist die Höhe.',
               2: 'Nicht addieren: Der Sinus ist eine der beiden Koordinaten.'},
              sprich='P mit den Koordinaten null Komma sechs und null Komma acht liegt auf dem Einheitskreis. Wie gross ist Sinus x?',
              rueck_sprich={1: 'Das ist die erste Koordinate, der Cosinus. Der Sinus ist die Höhe.',
                            2: 'Nicht addieren. Der Sinus ist eine der beiden Koordinaten.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
clip('periode-symmetrie', 'Sinuskurve sehen: Periode und Symmetrie',
     'Nach 2π wiederholt sich alles: Periode, Nullstellen, Hoch- und Tiefpunkte, die Symmetrien von Sinus und Cosinus und der Versatz um π/2.',
     ['Periode', 'Symmetrie', 'Nullstellen', 'Sinusfunktion', 'Cosinusfunktion'], [
         sz('Periode',
            'Nach einer vollen Umdrehung ist P wieder am selben Ort. Darum wiederholt sich die Sinuskurve nach zwei pi, '
            'nach links wie nach rechts. Zwei pi ist die Periodenlänge.',
            f(r'\sin(x + 2\pi) = \sin x', 240, 60),
            n('Periodenlänge @p = 2\\pi@', 350, 'blau', ein=3.6),
            graf(WP, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P, dicke=7), sk([[0, 1, 1, 0, 0]], gestrichelt=True)], ein=0.3)),
         sz('Nullstellen',
            'Die Sinuskurve schneidet die x-Achse bei null, pi, zwei pi und so weiter, auch bei minus pi: bei allen ganzzahligen '
            'Vielfachen von pi. Man schreibt x null gleich k mal pi. Die Werte bleiben zwischen minus eins und eins.',
            f(r'x_0 = k\pi, \quad k \in \mathbb{Z}', 240, 58, ein=8.5),
            n('Wertemenge @W = [-1;\\, 1]@', 350, 'blau', ein=10.8),
            graf(WP, [sk([[0, 1, 1, 0, 0]])], ein=0.3,
                 punkte=[pt(k * P, 0, 1) for k in range(-2, 5)])),
         sz('Symmetrie',
            'Die Sinuskurve ist punktsymmetrisch zum Ursprung: Sinus von minus x ist minus Sinus von x. '
            'Die Cosinuskurve dagegen ist achsensymmetrisch zur y-Achse: Cosinus von minus x ist Cosinus von x.',
            f(r'\fa{\sin(-x) = -\sin x}', 240, 50),
            f(r'\fc{\cos(-x) = \cos x}', 240, 50, ein=6.0, x=980),
            graf(WS, [sk([[0, 1, 1, 0, 0]])], ein=0.3,
                 punkte=[pt(P / 6, 0.5, 1, '(π/6 | 0.5)', [P / 6 + 0.15, 0.75]),
                         pt(-P / 6, -0.5, 1, '(−π/6 | −0.5)', [-P / 6 - 0.15, -0.85], 'end')]),
            graf(WS, [ck()], ein=6.0)),
         sz('Versetzt',
            'Die Cosinuskurve ist eine Sinuskurve, nur verschoben. Schieben wir die Sinuskurve um pi halbe nach links, '
            'liegt sie genau auf der Cosinuskurve. Cosinus x ist Sinus von x plus pi halbe.',
            f(r'\fc{\cos x} = \fa{\sin\!\left(x + \tfrac{\pi}{2}\right)}', 240, 56, ein=8.7),
            graf(WS, [ck(gestrichelt=True), sk([[0, 1, 1, 0, 0], [3.8, 1, 1, 0, 0], [6.3, 1, 1, -H2, 0]])], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Sinus und Cosinus haben die Periode zwei pi und die Wertemenge minus eins bis eins. '
            'Der Sinus ist punktsymmetrisch, der Cosinus achsensymmetrisch. Und die Cosinuskurve ist die um pi halbe '
            'nach links verschobene Sinuskurve.',
            titel('Zum Mitnehmen', 240, 72),
            n('@p = 2\\pi@, @W = [-1;\\, 1]@|@\\sin(-x) = -\\sin x@; @\\cos(-x) = \\cos x@', 350, 'blau', 42, ein=1.2),
            graf(WS, [sk([[0, 1, 1, 0, 0]]), ck()], ein=0.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-periode-symmetrie', 'Sinuskurve sehen: Kontrollfragen zu Periode und Symmetrie',
     'Fünf Vorhersagen zu Periode, Nullstellen, Symmetrie und zum Versatz von Sinus und Cosinus.',
     ['Periode', 'Symmetrie', 'Kontrollfragen'], [
         sz('Frage 1',
            'Auch der Cosinus wiederholt sich nach einer vollen Umdrehung: nach zwei pi.',
            f(r'\cos(x + 2\pi) = \cos x', 240, 58, ein=1.0),
            graf(WP, [ck(), ck(von=0, bis=2 * P, dicke=7)], ein=1.2)),
         sz('Frage 2',
            'Die Sinuskurve schneidet die x-Achse bei allen Vielfachen von pi, auch bei pi selbst. Also k mal pi.',
            f(r'x_0 = k\pi', 240, 62, ein=1.0),
            graf(WP, [sk([[0, 1, 1, 0, 0]])], ein=1.2, punkte=[pt(k * P, 0, 1) for k in range(-2, 5)])),
         sz('Frage 3',
            'Punktsymmetrie: Sinus von minus null Komma fünf ist minus Sinus von null Komma fünf, also ungefähr minus null Komma vier acht.',
            f(r'\sin(-0.5) = -\sin 0.5 \approx -0.479', 240, 54, ein=1.0),
            graf(WS, [sk([[0, 1, 1, 0, 0]])], ein=1.2,
                 punkte=[pt(0.5, math.sin(0.5), 1), pt(-0.5, -math.sin(0.5), 1)])),
         sz('Frage 4',
            'Die Cosinuskurve hat ihren Hochpunkt bei null, die Sinuskurve erst bei pi halbe. Also muss die Sinuskurve '
            'um pi halbe nach links.',
            f(r'\cos x = \sin\!\left(x + \tfrac{\pi}{2}\right)', 240, 54, ein=1.0),
            graf(WS, [ck(gestrichelt=True), sk([[0, 1, 1, 0, 0], [5.0, 1, 1, 0, 0], [7.2, 1, 1, -H2, 0]])], ein=0.6)),
         sz('Frage 5',
            'Rechts der y-Achse liegt der nächste Hochpunkt der Cosinuskurve eine Periode weiter: bei zwei pi.',
            f(r'\cos 2\pi = 1', 240, 62, ein=1.4),
            graf(WS, [ck()]),
            graf(WS, [ck()], ein=1.4, punkte=[pt(2 * P, 1, 3, '(2π | 1)', [2 * P - 0.2, 1.22], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: Periode zwei pi, Nullstellen des Sinus bei k pi, des Cosinus bei pi halbe plus k pi. '
            'Der Sinus ist punktsymmetrisch, der Cosinus achsensymmetrisch.',
            titel('Zum Mitnehmen', 240, 72),
            n('Sinus: @x_0 = k\\pi@; Cosinus: @x_0 = \\tfrac{\\pi}{2} + k\\pi@', 350, 'blau', 42, ein=1.2),
            graf(WS, [sk([[0, 1, 1, 0, 0]]), ck()], ein=0.3)),
     ], [
         wahl('Frage 1', 'Welche Periodenlänge hat y = cos x?',
              ['2π', 'π', 'π/2'], 0,
              {0: 'Ja.',
               1: 'Nach π ist P genau gegenüber — dort ist cos x = −1, nicht 1.',
               2: 'Nach π/2 ist erst eine Vierteldrehung geschafft.'},
              sprich='Welche Periodenlänge hat y gleich Cosinus x?',
              rueck_sprich={1: 'Nach pi ist P genau gegenüber. Dort ist Cosinus x gleich minus eins, nicht eins.',
                            2: 'Nach pi halbe ist erst eine Vierteldrehung geschafft.'}),
         wahl('Frage 2', 'Wo hat y = sin x ihre Nullstellen?',
              ['x = kπ', 'x = π/2 + kπ', 'x = 2kπ'], 0,
              {0: 'Ja.',
               1: 'Das sind die Nullstellen des Cosinus. Wo liegt P auf der waagrechten Achse?',
               2: 'Dann fehlte π. Ist sin π = 0?'},
              sprich='Wo hat y gleich Sinus x ihre Nullstellen?',
              rueck_sprich={1: 'Das sind die Nullstellen des Cosinus. Wo liegt P auf der waagrechten Achse?',
                            2: 'Dann fehlte pi. Ist Sinus von pi gleich null?'}),
         wahl('Frage 3', 'Es gilt sin 0.5 ≈ 0.479. Wie gross ist sin(−0.5)?',
              ['≈ −0.479', '≈ 0.479', '≈ 0.521'], 0,
              {0: 'Ja.',
               1: 'Das gilt beim Cosinus. Die Sinuskurve ist punktsymmetrisch zum Ursprung.',
               2: 'Nicht von 1 abziehen: Die Sinuskurve ist punktsymmetrisch zum Ursprung.'},
              sprich='Es gilt: Sinus von null Komma fünf ist ungefähr null Komma vier sieben neun. Wie gross ist Sinus von minus null Komma fünf?',
              rueck_sprich={1: 'Das gilt beim Cosinus. Die Sinuskurve ist punktsymmetrisch zum Ursprung.',
                            2: 'Nicht von eins abziehen. Die Sinuskurve ist punktsymmetrisch zum Ursprung.'}),
         wahl('Frage 4', 'Um wie viel muss man die Sinuskurve schieben, damit sie auf der Cosinuskurve liegt?',
              ['π/2 nach links', 'π/2 nach rechts', 'π nach links'], 0,
              {0: 'Ja.',
               1: 'Der Hochpunkt des Sinus liegt bei π/2, der des Cosinus bei 0. Wohin muss er also?',
               2: 'Um π verschoben wird aus sin x die Kurve −sin x.'},
              sprich='Um wie viel muss man die Sinuskurve schieben, damit sie auf der Cosinuskurve liegt?',
              rueck_sprich={1: 'Der Hochpunkt des Sinus liegt bei pi halbe, der des Cosinus bei null. Wohin muss er also?',
                            2: 'Um pi verschoben wird aus Sinus x die Kurve minus Sinus x.'}),
         klick('Frage 5', 'Tipp den nächsten Hochpunkt der Cosinuskurve rechts der y-Achse ins Bild.',
               [2 * P, 1], 'Getroffen: (2π | 1).',
               [{'bei': [P, -1], 'text': 'Das ist ein Tiefpunkt. Wann ist cos x wieder 1?',
                 'sprich': 'Das ist ein Tiefpunkt. Wann ist Cosinus x wieder eins?'},
                {'bei': [0, 1], 'text': 'Das ist der Hochpunkt auf der y-Achse. Gesucht ist der nächste rechts davon.',
                 'sprich': 'Das ist der Hochpunkt auf der y-Achse. Gesucht ist der nächste rechts davon.'},
                {'bei': [H2, 0], 'text': 'Hier ist eine Nullstelle. Gesucht ist der höchste Punkt.',
                 'sprich': 'Hier ist eine Nullstelle. Gesucht ist der höchste Punkt.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — eine Periode nach (0 | 1).',
               sprich='Tipp den nächsten Hochpunkt der Cosinuskurve rechts der y-Achse ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle, eine Periode nach null, eins.'),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
clip('tangens', 'Sinuskurve sehen: die Tangenskurve',
     'Tangens als Sinus durch Cosinus: die Strecke an der Tangente des Einheitskreises, die Pole, die Periode π und die Punktsymmetrie.',
     ['Tangensfunktion', 'Pol', 'Periode', 'Einheitskreis'], [
         sz('Sinus durch Cosinus',
            'Der Tangens ist Sinus durch Cosinus. Wo der Cosinus null ist, bei pi halbe, darf man nicht teilen. '
            'Dort ist der Tangens nicht definiert.',
            f(r'\fb{\tan x} = \dfrac{\fa{\sin x}}{\fc{\cos x}}', 250, 56),
            n('nicht definiert, wo @\\cos x = 0@: @x = \\tfrac{\\pi}{2} + k\\pi@', 400, 'rot', ein=4.6)),
         sz('Am Einheitskreis',
            'Am Einheitskreis ist der Tangens eine Strecke: auf der senkrechten Tangente rechts am Kreis, bis zur Geraden durch den Mittelpunkt und P. '
            'Bei null ist sie null, bei pi viertel genau eins. Je näher P an pi halbe kommt, desto steiler der Strahl, '
            'und die Strecke wächst über alle Grenzen.',
            f(r'\tan \tfrac{\pi}{4} = 1', 240, 56, ein=10.4),
            graf(WT, [tk([[0, 1, 1, 0, 0]], von=0,
                         kreis={'mx': -2.0, 'bahn': [[0, 0], [9.0, 0], [10.4, P / 4], [11.0, P / 4], [15.4, 1.2]],
                                'spur': True, 'farbe': 2})], ein=0.3)),
         sz('Pole und Periode',
            'An jeder Stelle pi halbe plus k pi hat die Tangenskurve einen Pol: Links davon wächst sie über alle Grenzen, rechts davon kommt sie von ganz unten. '
            'Schon nach pi wiederholt sie sich. Die Periodenlänge ist pi, nicht zwei pi.',
            f(r'\tan(x + \pi) = \tan x', 240, 56),
            n('Pole bei @x = \\tfrac{\\pi}{2} + k\\pi@; Periode @p = \\pi@', 350, 'orange', ein=8.4),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=0.3)),
         sz('Nullstellen und Symmetrie',
            'Nullstellen hat der Tangens dort, wo der Sinus null ist: bei k mal pi. Und die Kurve ist punktsymmetrisch '
            'zum Ursprung: Tangens von minus x ist minus Tangens von x. Alle Zahlen kommen als Wert vor.',
            f(r'\tan(-x) = -\tan x', 240, 56, ein=4.9),
            n('@x_0 = k\\pi@; @W = \\mathbb{R}@', 350, 'orange', ein=7.6),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=0.3,
                 punkte=[pt(k * P, 0, 2) for k in (-1, 0, 1, 2)])),
         sz('Merke',
            'Zum Mitnehmen: Tangens ist Sinus durch Cosinus. Pole bei pi halbe plus k pi, Nullstellen bei k pi, '
            'Periode pi, punktsymmetrisch zum Ursprung.',
            titel('Zum Mitnehmen', 240, 72),
            n('@D = \\mathbb{R} \\setminus \\left\\{\\tfrac{\\pi}{2} + k\\pi\\right\\}@; @p = \\pi@', 350, 'orange', 42, ein=1.2),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=0.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-tangens', 'Sinuskurve sehen: Kontrollfragen zur Tangenskurve',
     'Fünf Vorhersagen zu Polen, Werten, Periode und Nullstellen der Tangensfunktion.',
     ['Tangensfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei pi halbe ist der Cosinus null. Durch null kann man nicht teilen: Dort ist der Tangens nicht definiert.',
            f(r'\cos \tfrac{\pi}{2} = 0', 240, 58, ein=1.0),
            graf(WT, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=1.2)),
         sz('Frage 2',
            'Bei pi viertel sind Sinus und Cosinus gleich gross. Ihr Quotient ist eins.',
            f(r'\tan \tfrac{\pi}{4} = \dfrac{\sin \frac{\pi}{4}}{\cos \frac{\pi}{4}} = 1', 250, 50, ein=1.0),
            graf(WT, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=1.2, punkte=[pt(P / 4, 1, 2, '(π/4 | 1)', [P / 4 + 0.2, 1.4])])),
         sz('Frage 3',
            'Nach pi liegt P genau gegenüber. Sinus und Cosinus wechseln beide das Vorzeichen, ihr Quotient bleibt gleich. '
            'Die Periode ist pi.',
            f(r'\tan(x + \pi) = \tan x', 240, 56, ein=1.0),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=1.2)),
         sz('Frage 4',
            'Die Nullstelle rechts der y-Achse liegt bei pi. Bei pi halbe ist ein Pol, keine Nullstelle.',
            f(r'\tan \pi = 0', 240, 62, ein=1.4),
            graf(WT, [tk([[0, 1, 1, 0, 0]])]),
            graf(WT, [tk([[0, 1, 1, 0, 0]])], ein=1.4, punkte=[pt(P, 0, 2, '(π | 0)', [P + 0.2, 0.35])])),
         sz('Frage 5',
            'Die Periode ist pi. Also hat Tangens von eins plus pi denselben Wert wie Tangens von eins.',
            f(r'\tan(1 + \pi) = \tan 1 \approx 1.557', 240, 54, ein=1.0),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=1.2,
                 punkte=[pt(1, math.tan(1), 2), pt(1 + P, math.tan(1), 2)])),
         sz('Merke',
            'Zum Mitnehmen: Der Tangens hat Pole, wo der Cosinus null ist, und Nullstellen, wo der Sinus null ist. '
            'Seine Periode ist pi.',
            titel('Zum Mitnehmen', 240, 72),
            n('Pole: @\\cos x = 0@; Nullstellen: @\\sin x = 0@; @p = \\pi@', 350, 'orange', 42, ein=1.2),
            graf(WTP, [tk([[0, 1, 1, 0, 0]], pole=True)], ein=0.3)),
     ], [
         wahl('Frage 1', 'Bei welchem x ist tan x nicht definiert?',
              ['x = π/2', 'x = π', 'x = 0'], 0,
              {0: 'Ja.',
               1: 'tan π = 0 : (−1) = 0 — das geht. Wo ist der Cosinus null?',
               2: 'tan 0 = 0 : 1 = 0 — das geht. Wo ist der Cosinus null?'},
              sprich='Bei welchem x ist Tangens x nicht definiert?',
              rueck_sprich={1: 'Tangens von pi ist null durch minus eins, also null. Das geht. Wo ist der Cosinus null?',
                            2: 'Tangens von null ist null durch eins, also null. Das geht. Wo ist der Cosinus null?'}),
         wahl('Frage 2', 'Wie gross ist tan(π/4)?',
              ['1', '0', 'nicht definiert'], 0,
              {0: 'Ja.',
               1: 'Null ist der Tangens bei 0. Bei π/4 sind Sinus und Cosinus gleich gross.',
               2: 'Nicht definiert ist er bei π/2. Bei π/4 sind Sinus und Cosinus gleich gross.'},
              sprich='Wie gross ist Tangens von pi viertel?',
              rueck_sprich={1: 'Null ist der Tangens bei null. Bei pi viertel sind Sinus und Cosinus gleich gross.',
                            2: 'Nicht definiert ist er bei pi halbe. Bei pi viertel sind Sinus und Cosinus gleich gross.'}),
         wahl('Frage 3', 'Nach welcher Länge wiederholt sich y = tan x?',
              ['π', '2π', 'π/2'], 0,
              {0: 'Ja.',
               1: 'Schon früher: Nach π wechseln Sinus und Cosinus beide das Vorzeichen.',
               2: 'Nach π/2 kommt erst der Pol.'},
              sprich='Nach welcher Länge wiederholt sich y gleich Tangens x?',
              rueck_sprich={1: 'Schon früher. Nach pi wechseln Sinus und Cosinus beide das Vorzeichen.',
                            2: 'Nach pi halbe kommt erst der Pol.'}),
         klick('Frage 4', 'Tipp die erste Nullstelle der Tangenskurve rechts der y-Achse ins Bild.',
               [P, 0], 'Getroffen: (π | 0).',
               [{'bei': [H2, 0], 'text': 'Bei π/2 ist ein Pol — dort gibt es gar keinen Wert.',
                 'sprich': 'Bei pi halbe ist ein Pol. Dort gibt es gar keinen Wert.'},
                {'bei': [2 * P, 0], 'text': 'Das ist eine Nullstelle, aber nicht die erste.',
                 'sprich': 'Das ist eine Nullstelle, aber nicht die erste.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp die erste Nullstelle der Tangenskurve rechts der y-Achse ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 5', 'Es gilt tan 1 ≈ 1.557. Wie gross ist tan(1 + π)?',
              ['≈ 1.557', '≈ −1.557', '≈ 0'], 0,
              {0: 'Ja.',
               1: 'Ein Minus gäbe es bei tan(−1). Um π verschoben: Was sagt die Periode?',
               2: 'Null ist der Tangens bei π. Was sagt die Periode?'},
              sprich='Es gilt: Tangens von eins ist ungefähr eins Komma fünf fünf sieben. Wie gross ist Tangens von eins plus pi?',
              rueck_sprich={1: 'Ein Minus gäbe es bei Tangens von minus eins. Um pi verschoben: Was sagt die Periode?',
                            2: 'Null ist der Tangens bei pi. Was sagt die Periode?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
clip('parameter', 'Sinuskurve sehen: Strecken und Verschieben',
     'Was a, b, u und v in y = a · sin(b(x − u)) + v bewirken: Amplitude, Periodenlänge 2π/b, Verschiebung und Mittellage.',
     ['Amplitude', 'Periode', 'Verschiebung', 'Sinusfunktion'], [
         sz('Amplitude',
            'Der Faktor a vor dem Sinus streckt die Kurve in y-Richtung. Bei a gleich zwei schwankt sie zwischen minus zwei '
            'und zwei, bei a gleich ein Halb nur zwischen minus ein Halb und ein Halb. a heisst Amplitude.',
            f(r'y = \fa{a} \cdot \sin x', 240, 62),
            n('Amplitude @a@: grösste Abweichung von der Mittellinie', 350, 'blau', ein=9.7),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                      sk([[0, 1, 1, 0, 0], [3.0, 1, 1, 0, 0], [4.6, 2, 1, 0, 0], [7.2, 2, 1, 0, 0], [8.6, 0.5, 1, 0, 0]],
                         marken=[{'x': H2, 'text': '{y}', 'farbe': 1}])], ein=0.3)),
         sz('Periode',
            'Der Faktor b im Argument staucht die Kurve in x-Richtung. Bei b gleich zwei läuft sie doppelt so schnell: '
            'Die Periode wird halb so lang, nur noch pi. Allgemein ist die Periodenlänge zwei pi durch b.',
            f(r'y = \sin(\fa{b}\,x) \qquad p = \dfrac{2\pi}{\fa{b}}', 250, 54),
            n('grösseres @b@ → kürzere Periode', 395, 'blau', ein=8.9),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                      sk([[0, 1, 1, 0, 0], [3.8, 1, 1, 0, 0], [5.8, 1, 2, 0, 0]])], ein=0.3)),
         sz('Mittellage',
            'Der Summand v hebt die ganze Kurve an. Bei v gleich eins schwankt sie um die Mittellinie y gleich eins, '
            'zwischen null und zwei.',
            f(r'y = \sin x + \fa{v}', 240, 62),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                      sk([[0, 1, 1, 0, 0], [2.4, 1, 1, 0, 0], [4.4, 1, 1, 0, 1]], mittel=True)], ein=0.3)),
         sz('Verschiebung',
            'Mit u wird die Kurve nach rechts geschoben: x minus u. Bei u gleich pi drittel geht sie erst bei pi drittel steigend durch null. '
            'Achtung: Minus im Argument heisst nach rechts.',
            f(r'y = \sin(x - \fa{u})', 240, 62),
            n('@x - u@: um @u@ nach rechts', 350, 'blau', ein=6.6),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                      sk([[0, 1, 1, 0, 0], [2.5, 1, 1, 0, 0], [4.5, 1, 1, P / 3, 0]])], ein=0.3)),
         sz('Alles zusammen',
            'Alles zusammen: y gleich zwei mal Sinus von zwei mal Klammer x minus pi viertel plus eins. Schritt für Schritt '
            'aus der Sinuskurve: zuerst die Periode pi, dann die Amplitude zwei, dann um pi viertel nach rechts, '
            'zuletzt die Mittellinie y gleich eins.',
            f(r'y = \fa{2}\sin\!\big(\fa{2}\,(x - \fa{\tfrac{\pi}{4}})\big) + \fa{1}', 240, 54),
            n('@p = \\pi@; @a = 2@; @u = \\tfrac{\\pi}{4}@; @v = 1@', 350, 'blau', ein=8.6),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True),
                      sk([[0, 1, 1, 0, 0], [8.6, 1, 1, 0, 0], [9.8, 1, 2, 0, 0], [10.2, 1, 2, 0, 0], [11.4, 2, 2, 0, 0], [11.7, 2, 2, 0, 0],
                          [13.2, 2, 2, P / 4, 0], [13.6, 2, 2, P / 4, 0], [15.2, 2, 2, P / 4, 1]], mittel=True)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: a ist die Amplitude, zwei pi durch b die Periode, u schiebt nach rechts, v hebt die Mittellinie.',
            titel('Zum Mitnehmen', 240, 72),
            n('@y = a \\sin\\big(b(x - u)\\big) + v@ (@a, b \\gt 0@)|@p = \\tfrac{2\\pi}{b}@', 350, 'blau', 44, ein=1.2),
            graf(WA, [sk([[0, 2, 2, P / 4, 1]], mittel=True)], ein=0.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-parameter', 'Sinuskurve sehen: Kontrollfragen zu den Parametern',
     'Fünf Vorhersagen zu Amplitude, Periode, Wertemenge und Verschiebung einer Sinuskurve.',
     ['Amplitude', 'Periode', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Amplitude ist der Faktor vor dem Sinus: drei. Die eins hebt nur die Mittellinie.',
            f(r'y = \fa{3}\sin x + 1', 240, 60, ein=1.0),
            graf(dict(WA, ybereich=[-2.6, 4.6], yteilung=yt(-2, -1, 1, 2, 3, 4)), [sk([[0, 3, 1, 0, 1]], mittel=True)], ein=1.2)),
         sz('Frage 2',
            'Periodenlänge zwei pi durch b, also zwei pi durch drei: zwei pi drittel.',
            f(r'p = \dfrac{2\pi}{3}', 250, 56, ein=1.0),
            graf(WA, [sk([[0, 1, 3, 0, 0]])], ein=1.2)),
         sz('Frage 3',
            'Zwei mal Sinus schwankt zwischen minus zwei und zwei. Minus eins verschiebt nach unten: von minus drei bis eins.',
            f(r'W = [-3;\, 1]', 240, 62, ein=1.0),
            graf(WA, [sk([[0, 2, 1, 0, -1]], mittel=True)], ein=1.2)),
         sz('Frage 4',
            'Die Kurve wird um pi drittel nach rechts geschoben. Der Hochpunkt wandert von pi halbe nach pi halbe plus pi drittel, '
            'also fünf pi sechstel.',
            f(r'\tfrac{\pi}{2} + \tfrac{\pi}{3} = \tfrac{5\pi}{6}', 240, 56, ein=1.4),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True)]),
            graf(WA, [sk([[0, 1, 1, 0, 0]], farbe=5, gestrichelt=True), sk([[0, 1, 1, P / 3, 0]])], ein=1.4,
                 punkte=[pt(5 * P / 6, 1, 1, '(5π/6 | 1)', [5 * P / 6 + 0.2, 1.45])])),
         sz('Frage 5',
            'Die Kurve reicht bis zwei: Amplitude zwei. Sie wiederholt sich nach pi, also b gleich zwei pi durch pi gleich zwei.',
            f(r'y = 2\sin(2x)', 240, 62, ein=1.0),
            graf(WA, [sk([[0, 2, 2, 0, 0]])], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Amplitude ablesen, Periode zwei pi durch b, Wertemenge von v minus a bis v plus a.',
            titel('Zum Mitnehmen', 240, 72),
            n('@W = [v - a;\\, v + a]@ (@a \\gt 0@); @p = \\tfrac{2\\pi}{b}@', 350, 'blau', 44, ein=1.2),
            graf(WA, [sk([[0, 2, 1, 0, -1]], mittel=True)], ein=0.3)),
     ], [
         wahl('Frage 1', 'y = 3 sin x + 1: Wie gross ist die Amplitude?',
              ['3', '1', '4'], 0,
              {0: 'Ja.',
               1: 'Die 1 hebt die Mittellinie. Die Amplitude steht vor dem Sinus.',
               2: 'Nicht addieren: Die Amplitude ist die grösste Abweichung von der Mittellinie.'},
              sprich='y gleich drei Sinus x plus eins: Wie gross ist die Amplitude?',
              rueck_sprich={1: 'Die eins hebt die Mittellinie. Die Amplitude steht vor dem Sinus.',
                            2: 'Nicht addieren. Die Amplitude ist die grösste Abweichung von der Mittellinie.'}),
         wahl('Frage 2', 'Welche Periodenlänge hat y = sin(3x)?',
              ['2π/3', '6π', '3'], 0,
              {0: 'Ja.',
               1: 'Grösseres b heisst kürzere Periode: 2π durch b, nicht mal b.',
               2: 'Die Periode ist 2π durch b.'},
              sprich='Welche Periodenlänge hat y gleich Sinus von drei x?',
              rueck_sprich={1: 'Grösseres b heisst kürzere Periode. Zwei pi durch b, nicht mal b.',
                            2: 'Die Periode ist zwei pi durch b.'}),
         wahl('Frage 3', 'Zwischen welchen Werten schwankt y = 2 sin x − 1?',
              ['−3 und 1', '−2 und 2', '−1 und 1'], 0,
              {0: 'Ja.',
               1: 'Das wäre 2 sin x. Die −1 schiebt alles nach unten.',
               2: 'Die Amplitude ist 2, nicht 1.'},
              sprich='Zwischen welchen Werten schwankt y gleich zwei Sinus x minus eins?',
              rueck_sprich={1: 'Das wäre zwei Sinus x. Die minus eins schiebt alles nach unten.',
                            2: 'Die Amplitude ist zwei, nicht eins.'}),
         klick('Frage 4', 'Gestrichelt: y = sin x. Tipp den Hochpunkt von y = sin(x − π/3) ins Bild.',
               [5 * P / 6, 1], 'Getroffen: (5π/6 | 1).',
               [{'bei': [H2, 1], 'text': 'Das ist der Hochpunkt von sin x. Die Kurve wird um π/3 geschoben.',
                 'sprich': 'Das ist der Hochpunkt von Sinus x. Die Kurve wird um pi drittel geschoben.'},
                {'bei': [P / 6, 1], 'text': 'Falsche Richtung: x − π/3 schiebt nach rechts.',
                 'sprich': 'Falsche Richtung. x minus pi drittel schiebt nach rechts.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Gestrichelt ist y gleich Sinus x. Tipp den Hochpunkt von y gleich Sinus von x minus pi drittel ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 5', 'Welche Gleichung hat die abgebildete Kurve?',
              ['y = 2 sin(2x)', 'y = 2 sin(x/2)', 'y = sin(2x) + 2'], 0,
              {0: 'Ja.',
               1: 'Dann wäre die Periode 4π. Lies die Periode ab: b = 2π : p.',
               2: 'Dann läge die Mittellinie bei y = 2. Die Kurve schwankt um 0.'},
              sprich='Welche Gleichung hat die abgebildete Kurve?',
              rueck_sprich={1: 'Dann wäre die Periode vier pi. Lies die Periode ab: b gleich zwei pi durch p.',
                            2: 'Dann läge die Mittellinie bei y gleich zwei. Die Kurve schwankt um null.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
X1 = math.asin(0.6)
C1 = math.acos(0.6)
clip('gleichungen', 'Sinuskurve sehen: Symmetrie nutzen',
     'Eine Waagrechte schneidet die Sinuskurve zweimal pro Periode: die erste Lösung vom Rechner, die zweite über die Symmetrie, weitere über die Periode.',
     ['Gleichung', 'Symmetrie', 'Periode', 'Taschenrechner'], [
         sz('Eine Waagrechte',
            'Für welche x ist Sinus x gleich null Komma sechs? Im Bild: wo die Waagrechte y gleich null Komma sechs die Kurve schneidet. '
            'Zwischen null und zwei pi sind es zwei Stellen.',
            f(r'\sin x = 0.6', 240, 62),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.6', farbe=5)], ein=0.3)),
         sz('Der Rechner',
            'Der Taschenrechner liefert mit der Umkehrfunktion Sinus hoch minus eins nur eine Lösung: ungefähr null Komma sechs vier vier. '
            'Er muss dafür im Bogenmass rechnen, im Modus RAD.',
            f(r'x_1 = \sin^{-1}(0.6) \approx 0.644', 240, 56),
            n('Rechner im Bogenmass (RAD); @\\sin^{-1}@ heisst auch @\\arcsin@', 350, 'rot', ein=7.6),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.6', farbe=5)], ein=0.3,
                 punkte=[pt(X1, 0.6, 1, 'x₁', [X1 - 0.15, 0.85], 'end')])),
         sz('Symmetrie',
            'Die zweite Lösung liefert die Symmetrie. Die Sinuskurve ist achsensymmetrisch zur Geraden x gleich pi halbe. '
            'Darum liegt die zweite Stelle gleich weit vor pi wie die erste nach null: x zwei gleich pi minus x eins, '
            'ungefähr zwei Komma vier neun acht.',
            f(r'x_2 = \pi - x_1 \approx 2.498', 240, 56, ein=9.8),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.6', farbe=5)], ein=0.3,
                 punkte=[pt(X1, 0.6, 1, 'x₁', [X1 - 0.15, 0.85], 'end')]),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.6', farbe=5)], ein=9.8,
                 punkte=[pt(X1, 0.6, 1, 'x₁', [X1 - 0.15, 0.85], 'end'),
                         pt(P - X1, 0.6, 1, 'x₂', [P - X1 + 0.15, 0.85])])),
         sz('Beim Cosinus',
            'Beim Cosinus liegt die Symmetrieachse bei pi. Aus x eins wird x zwei gleich zwei pi minus x eins. '
            'Für Cosinus x gleich null Komma sechs: null Komma neun zwei sieben und fünf Komma drei fünf sechs.',
            f(r'\fc{\cos x = 0.6}: \quad x_2 = 2\pi - x_1', 240, 54),
            n('@x_1 \\approx 0.927@, @x_2 \\approx 5.356@', 350, 'gruen', ein=8.9),
            graf(WK, [ck(von=0, bis=2 * P), fest('0.6', farbe=5)], ein=0.3,
                 punkte=[pt(C1, 0.6, 3), pt(2 * P - C1, 0.6, 3)])),
         sz('Periode',
            'Weitere Lösungen liegen jeweils eine Periode weiter: Zu jeder Lösung kommt plus zwei pi dazu. '
            'Zwischen null und vier pi hat Sinus x gleich null Komma sechs also vier Lösungen.',
            f(r'x_1 + 2\pi, \quad x_2 + 2\pi, \;\ldots', 240, 56),
            graf(WG, [sk([[0, 1, 1, 0, 0]], von=0, bis=4 * P), fest('0.6', farbe=5)], ein=0.3,
                 punkte=[pt(X1, 0.6, 1), pt(P - X1, 0.6, 1), pt(X1 + 2 * P, 0.6, 1), pt(3 * P - X1, 0.6, 1)])),
         sz('Faktor im Argument',
            'Und bei Sinus von zwei x gleich ein Halb? Man ersetzt zwei x durch z. Sinus z gleich ein Halb gilt bei pi sechstel '
            'und fünf pi sechstel. Durch zwei geteilt: x gleich pi zwölftel und fünf pi zwölftel. Weil die Periode jetzt nur pi ist, '
            'kommen zwischen null und zwei pi noch zwei dazu.',
            f(r'z = 2x: \; \sin z = \tfrac12 \;\Rightarrow\; z = \tfrac{\pi}{6},\ \tfrac{5\pi}{6}', 240, 50, ein=4.4),
            n('@x = \\tfrac{\\pi}{12}@, @\\tfrac{5\\pi}{12}@ und eine Periode @\\pi@ weiter', 350, 'blau', ein=10.0),
            graf(WK, [sk([[0, 1, 2, 0, 0]], von=0, bis=2 * P), fest('0.5', farbe=5)], ein=0.3),
            graf(WK, [sk([[0, 1, 2, 0, 0]], von=0, bis=2 * P), fest('0.5', farbe=5)], ein=10.0,
                 punkte=[pt(P / 12, 0.5, 1), pt(5 * P / 12, 0.5, 1)]),
            graf(WK, [sk([[0, 1, 2, 0, 0]], von=0, bis=2 * P), fest('0.5', farbe=5)], ein=15.0,
                 punkte=[pt(P / 12, 0.5, 1), pt(5 * P / 12, 0.5, 1), pt(13 * P / 12, 0.5, 1), pt(17 * P / 12, 0.5, 1)])),
         sz('Merke',
            'Zum Mitnehmen: Sinus: x zwei gleich pi minus x eins. Cosinus: x zwei gleich zwei pi minus x eins. '
            'Und jede Lösung wiederholt sich nach zwei pi.',
            titel('Zum Mitnehmen', 240, 72),
            n('@\\sin@: @x_2 = \\pi - x_1@; @\\cos@: @x_2 = 2\\pi - x_1@|weitere: @+\\,2k\\pi@', 350, 'blau', 42, ein=1.2),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.6', farbe=5)], ein=0.3)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
X8 = math.asin(0.8)
C8 = math.acos(0.8)
clip('kontrolle-gleichungen', 'Sinuskurve sehen: Kontrollfragen zum Symmetrie-Nutzen',
     'Fünf Vorhersagen zur Anzahl und Lage der Lösungen von sin x = c und cos x = c.',
     ['Gleichung', 'Symmetrie', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Waagrechte y gleich null Komma drei schneidet die Sinuskurve zwischen null und zwei pi zweimal.',
            f(r'\sin x = 0.3: \; 2 \text{ Lösungen}', 240, 54, ein=1.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.3', farbe=5)], ein=1.2,
                 punkte=[pt(math.asin(0.3), 0.3, 1), pt(P - math.asin(0.3), 0.3, 1)])),
         sz('Frage 2',
            'Beim Sinus: x zwei gleich pi minus x eins. Pi minus null Komma neun zwei sieben ist ungefähr zwei Komma zwei eins vier.',
            f(r'x_2 = \pi - 0.927 \approx 2.214', 240, 56, ein=1.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.8', farbe=5)], ein=1.2,
                 punkte=[pt(X8, 0.8, 1), pt(P - X8, 0.8, 1)])),
         sz('Frage 3',
            'Beim Cosinus liegt die Symmetrieachse bei pi: x zwei gleich zwei pi minus x eins, ungefähr fünf Komma sechs vier null.',
            f(r'x_2 = 2\pi - 0.644 \approx 5.640', 240, 56, ein=1.0),
            graf(WK, [ck(von=0, bis=2 * P), fest('0.8', farbe=5)], ein=1.2,
                 punkte=[pt(C8, 0.8, 3), pt(2 * P - C8, 0.8, 3)])),
         sz('Frage 4',
            'Sinus x gleich ein Halb gilt bei pi sechstel und bei pi minus pi sechstel, also fünf pi sechstel. '
            'Die zweite liegt zwischen pi halbe und pi.',
            f(r'x_2 = \pi - \tfrac{\pi}{6} = \tfrac{5\pi}{6}', 240, 56, ein=1.4),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.5', farbe=5)]),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('0.5', farbe=5)], ein=1.4,
                 punkte=[pt(5 * P / 6, 0.5, 1, '(5π/6 | 0.5)', [5 * P / 6 + 0.2, 0.85])])),
         sz('Frage 5',
            'Der Sinus bleibt zwischen minus eins und eins. Eins Komma zwei erreicht er nie: keine Lösung.',
            f(r'\sin x = 1.2: \; L = \{\,\}', 240, 58, ein=1.0),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P), fest('1.2', farbe=4)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Zwei Lösungen pro Periode, wenn c zwischen minus eins und eins liegt. Die zweite über die Symmetrie. '
            'Bei c gleich plus oder minus eins nur eine, und liegt c ausserhalb, gibt es keine.',
            titel('Zum Mitnehmen', 240, 72),
            n('pro Periode: @|c| \\lt 1@ zwei Lösungen; @|c| = 1@ eine; @|c| \\gt 1@ keine', 350, 'blau', 42, ein=1.2),
            graf(WK, [sk([[0, 1, 1, 0, 0]], von=0, bis=2 * P)], ein=0.3)),
     ], [
         wahl('Frage 1', 'Wie viele Lösungen hat sin x = 0.3 im Intervall [0; 2π]?',
              ['2', '1', '0'], 0,
              {0: 'Ja.',
               1: 'Der Rechner liefert eine — aber die Waagrechte schneidet die Kurve öfter.',
               2: '0.3 liegt zwischen −1 und 1. Wie oft schneidet die Waagrechte die Kurve?'},
              sprich='Wie viele Lösungen hat Sinus x gleich null Komma drei im Intervall von null bis zwei pi?',
              rueck_sprich={1: 'Der Rechner liefert eine. Aber die Waagrechte schneidet die Kurve öfter.',
                            2: 'Null Komma drei liegt zwischen minus eins und eins. Wie oft schneidet die Waagrechte die Kurve?'}),
         wahl('Frage 2', 'Eine Lösung von sin x = 0.8 ist x ≈ 0.927. Welches ist die zweite in [0; 2π]?',
              ['≈ 2.214', '≈ 5.356', '≈ 4.069'], 0,
              {0: 'Ja.',
               1: 'Das wäre 2π − x₁, die Regel beim Cosinus. Beim Sinus liegt die Symmetrieachse bei π/2.',
               2: 'Das wäre π + x₁ — dort ist der Sinus negativ.'},
              sprich='Eine Lösung von Sinus x gleich null Komma acht ist x gleich ungefähr null Komma neun zwei sieben. '
                     'Welches ist die zweite zwischen null und zwei pi?',
              rueck_sprich={1: 'Das wäre zwei pi minus x eins, die Regel beim Cosinus. Beim Sinus liegt die Symmetrieachse bei pi halbe.',
                            2: 'Das wäre pi plus x eins. Dort ist der Sinus negativ.'}),
         wahl('Frage 3', 'cos x = 0.8 hat die Lösung x ≈ 0.644. Welches ist die zweite in [0; 2π]?',
              ['≈ 5.640', '≈ 2.498', '≈ 3.785'], 0,
              {0: 'Ja.',
               1: 'Das wäre π − x₁, die Regel beim Sinus. Die Cosinuskurve ist symmetrisch zu x = π.',
               2: 'Das wäre π + x₁ — dort ist der Cosinus negativ.'},
              sprich='Cosinus x gleich null Komma acht hat die Lösung x gleich ungefähr null Komma sechs vier vier. '
                     'Welches ist die zweite zwischen null und zwei pi?',
              rueck_sprich={1: 'Das wäre pi minus x eins, die Regel beim Sinus. Die Cosinuskurve ist symmetrisch zu x gleich pi.',
                            2: 'Das wäre pi plus x eins. Dort ist der Cosinus negativ.'}),
         klick('Frage 4', 'sin(π/6) = 0.5. Tipp die zweite Lösung von sin x = 0.5 ins Bild.',
               [5 * P / 6, 0.5], 'Getroffen: (5π/6 | 0.5).',
               [{'bei': [P / 6, 0.5], 'text': 'Das ist die erste Lösung, π/6. Gesucht ist die zweite.',
                 'sprich': 'Das ist die erste Lösung, pi sechstel. Gesucht ist die zweite.'},
                {'bei': [7 * P / 6, -0.5], 'text': 'Dort ist sin x = −0.5. Die Waagrechte liegt bei +0.5.',
                 'sprich': 'Dort ist Sinus x gleich minus null Komma fünf. Die Waagrechte liegt bei plus null Komma fünf.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle: π − π/6.',
               sprich='Sinus von pi sechstel ist null Komma fünf. Tipp die zweite Lösung von Sinus x gleich null Komma fünf ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle: pi minus pi sechstel.'),
         wahl('Frage 5', 'Wie viele Lösungen hat sin x = 1.2?',
              ['keine', 'eine', 'zwei'], 0,
              {0: 'Ja.',
               1: 'Wie hoch kommt die Sinuskurve höchstens?',
               2: 'Wie hoch kommt die Sinuskurve höchstens?'},
              sprich='Wie viele Lösungen hat Sinus x gleich eins Komma zwei?',
              rueck_sprich={1: 'Wie hoch kommt die Sinuskurve höchstens?',
                            2: 'Wie hoch kommt die Sinuskurve höchstens?'}),
     ], art='Kontrollclip')
