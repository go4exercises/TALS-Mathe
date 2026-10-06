"""Erzeugt die zehn Drehbücher des Leitprogramms Betragsfunktionen (05.10.2026).

  python3 scripts/lp/betragsfunktionen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie beim Vorbild (Leitprogramm Exponential- und Logarithmusfunktionen): Bild rechts
(x 1010, y 175, 760 × 760), Formeln und Notizen links (x 150). Theme begreifbar-schlicht.

**Bewegte Kurven** (HOWTO-clips.md, «Betragskurven»): `vk([[t, a, u, v], …])` für
y = a·|x − u| + v, mit `knick` (Knickpunkt mit Live-Beschriftung) und `achse` (Symmetrieachse).
Für |f(x)| mit krummem f eine feste `formel` mit abs(…).

Farben — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15), gleich wie auf der Seite:
  1 blau   = die Betragskurve                          \\fa{…}
  2 orange = Waagrechte y = c und Lösungen             \\fb{…}
  3 grün   = die Äste als Geraden (abschnittsweise)    \\fc{…}
  4 rot    = Gegenbeispiel, falscher Weg               \\fd{…}
  5 Tinte  = neutral: die Funktion f vor dem Betrag, Symmetrieachse
"""
import json
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))   # scripts/lp/fragebild.py
from fragebild import anwenden as anwenden_fragebild   # noqa: E402
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150


def graf(W, kurven=(), punkte=(), ein=0.05, geraden=(), **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=list(geraden), punkte=list(punkte), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def vk(stuetz, farbe=1, knick=False, achse=False, marken=None, von=None, bis=None, gestrichelt=False, dicke=None):
    """Bewegte Betragskurve: Stützpunkte [t, a, u, v] für a·|x − u| + v."""
    d = {'bewegung': stuetz, 'betrag': True, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if knick:
        d['startpunkt'] = {'farbe': 5}
    if achse:
        d['asymptoten'] = {'farbe': 5}
    if marken is not None:
        d['marken'] = marken
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


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
    alt = R + 'clips/s3-6-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 's3-6-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Betragsfunktionen',
         'fach': 'Schwerpunktfach', 'lerngebiet': '3 · Funktionen',
         'lektion': ['s3-6'], 'stufe': ['BM2'], 'datum': '2026-10-05',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Knick sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms betragsfunktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    anwenden_fragebild(d)                               # beim Fragen nur das Gegebene
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


W1 = dict(xbereich=[-6, 6], ybereich=[-2, 8], xteilung=yt(-4, -2, 2, 4), yteilung=yt(2, 4, 6))
W2 = dict(xbereich=[-6, 6], ybereich=[-5, 7], xteilung=yt(-4, -2, 2, 4), yteilung=yt(-4, -2, 2, 4, 6))
WU = dict(xbereich=[-4.5, 4.5], ybereich=[-5, 6], xteilung=yt(-4, -2, 2, 4), yteilung=yt(-4, -2, 2, 4))
WW = dict(xbereich=[-4, 6], ybereich=[-1, 9], xteilung=yt(-2, 2, 4), yteilung=yt(2, 4, 6, 8))

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('betragsfunktion', 'Knick sehen: die Betragsfunktion',
     'Der Betrag als Abstand zur Null: abschnittsweise definiert, zwei gerade Äste, ein Knick in (0 | 0).',
     ['Betragsfunktion', 'Betrag', 'Abstand', 'abschnittsweise'], [
         sz('Abstand zur Null',
            'Der Betrag einer Zahl ist ihr Abstand zur Null. Drei und minus drei sind beide drei vom Nullpunkt entfernt: '
            'Der Betrag ist in beiden Fällen drei. Ein Betrag ist nie negativ.',
            titel('Abstand zur Null', 280, 80),
            f(r'|3| = 3 \qquad |-3| = 3', 430, 58, ein=3.4),
            n('Beträge sind nie negativ', 560, 'blau', ein=7.6)),
         sz('Zwei Äste',
            'Für positive x ist der Betrag einfach x: Die Kurve ist die Gerade y gleich x. Für negative x dreht der Betrag das '
            'Vorzeichen um: Dort ist die Kurve die Gerade y gleich minus x. Zusammen entsteht ein V.',
            f(r'|x| = \begin{cases} \fc{x} & x \ge 0 \\ \fc{-x} & x \lt 0 \end{cases}', 330, 54, ein=0.6),
            graf(W1, [fest('x', farbe=3, von=0), fest('-x', farbe=3, bis=0)], ein=0.4),
            graf(W1, [vk([[0, 1, 0, 0]])], ein=11.6)),
         sz('Der Knick',
            'Im Nullpunkt treffen sich die beiden Äste. Dort hat das V einen Knick: Links fällt die Kurve mit Steigung minus eins, '
            'rechts steigt sie mit Steigung eins. Das V ist symmetrisch zur y-Achse.',
            f(r'\text{Knick } (0 \mid 0)', 300, 58),
            n('Steigung @-1@ links, @+1@ rechts|symmetrisch: @|-x| = |x|@', 430, 'blau', ein=4.0),
            graf(W1, [vk([[0, 1, 0, 0]], knick=True, achse=True)], ein=0.3,
                 punkte=[pt(-3, 3, 1, '(−3 | 3)', [-3.3, 2.0], 'end'), pt(3, 3, 1, '(3 | 3)', [3.3, 2.0])])),
         sz('Merke',
            'Zum Mitnehmen: Der Betrag ist der Abstand zur Null. Die Betragsfunktion ist abschnittsweise linear, mit einem Knick '
            'im Nullpunkt. Ihre Werte sind nie negativ.',
            titel('Zum Mitnehmen', 250, 76),
            n('@|x| = x@ für @x \\ge 0@, @-x@ für @x \\lt 0@|Knick @(0 \\mid 0)@; @W = \\mathbb{R}_0^+@', 400, 'blau', 44, ein=1.2),
            graf(W1, [vk([[0, 1, 0, 0]], knick=True)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-betragsfunktion', 'Knick sehen: Kontrollfragen zur Betragsfunktion',
     'Fünf Vorhersagen zu Betrag, Wertemenge, den zwei Ästen und zur Gleichung |x| = 5.',
     ['Betragsfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Minus sieben ist sieben vom Nullpunkt entfernt. Der Betrag ist sieben.',
            f(r'|-7| = 7', 300, 66, ein=1.0)),
         sz('Frage 2',
            'Beträge sind nie negativ, und null wird bei x gleich null erreicht. Die Wertemenge sind die positiven Zahlen mit der Null.',
            f(r'W = \mathbb{R}_0^+', 300, 66, ein=1.0),
            graf(W1, [vk([[0, 1, 0, 0]], knick=True)], ein=1.2)),
         sz('Frage 3',
            'Bei x gleich minus drei ist der Betrag drei. Der Punkt liegt bei minus drei, drei, auf dem linken Ast.',
            f(r'|-3| = 3', 300, 62, ein=1.4),
            graf(W1, [vk([[0, 1, 0, 0]])]),
            graf(W1, [vk([[0, 1, 0, 0]])], ein=1.4, punkte=[pt(-3, 3, 1, '(−3 | 3)', [-3.3, 2.0], 'end')])),
         sz('Frage 4',
            'Für negative x dreht der Betrag das Vorzeichen: Betrag von x ist minus x. Minus x ist dann positiv.',
            f(r'x \lt 0: \; |x| = -x', 300, 58, ein=1.0),
            n('z. B. @|-4| = -(-4) = 4@', 430, 'blau', ein=2.4)),
         sz('Frage 5',
            'Zwei Zahlen haben den Abstand fünf zur Null: fünf und minus fünf.',
            f(r'|x| = 5 \;\Rightarrow\; x = 5 \text{ oder } x = -5', 300, 50, ein=1.0),
            graf(W1, [vk([[0, 1, 0, 0]]), fest('5', farbe=2)], ein=1.2,
                 punkte=[pt(-5, 5, 2), pt(5, 5, 2)])),
         sz('Merke',
            'Zum Mitnehmen: Ein Betrag ist ein Abstand, nie negativ. Für negative x ist der Betrag minus x.',
            titel('Zum Mitnehmen', 250, 76),
            n('@|x| \\ge 0@; für @x \\lt 0@: @|x| = -x@', 400, 'blau', 44, ein=1.2),
            graf(W1, [vk([[0, 1, 0, 0]], knick=True)])),
     ], [
         wahl('Frage 1', 'Wie gross ist |−7|?',
              ['7', '−7', '0'], 0,
              {0: 'Ja.',
               1: 'Ein Betrag ist ein Abstand — kann er negativ sein?',
               2: 'Wie weit ist −7 von der Null entfernt?'},
              sprich='Wie gross ist der Betrag von minus sieben?',
              rueck_sprich={1: 'Ein Betrag ist ein Abstand. Kann er negativ sein?',
                            2: 'Wie weit ist minus sieben von der Null entfernt?'}),
         wahl('Frage 2', 'Welche Wertemenge hat y = |x|?',
              ['ℝ₀⁺ (null und positiv)', 'ℝ (alle Zahlen)', 'ℝ⁺ (nur positiv)'], 0,
              {0: 'Ja.',
               1: 'Kann |x| negativ werden?',
               2: 'Und bei x = 0? Wie gross ist |0|?'},
              sprich='Welche Wertemenge hat y gleich Betrag von x?',
              rueck_sprich={1: 'Kann der Betrag von x negativ werden?',
                            2: 'Und bei x gleich null? Wie gross ist der Betrag von null?'}),
         klick('Frage 3', 'Tipp den Punkt der Kurve y = |x| ins Bild, der bei x = −3 liegt.',
               [-3, 3], 'Getroffen: (−3 | 3).',
               [{'bei': [3, 3], 'text': 'Das ist x = 3. Gesucht ist x = −3, links der y-Achse.',
                 'sprich': 'Das ist x gleich drei. Gesucht ist x gleich minus drei, links der y-Achse.'},
                {'bei': [-3, 0], 'text': 'Das ist die Stelle x = −3 auf der x-Achse. Wie hoch liegt die Kurve dort?',
                 'sprich': 'Das ist die Stelle x gleich minus drei auf der x-Achse. Wie hoch liegt die Kurve dort?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp den Punkt der Kurve y gleich Betrag von x ins Bild, der bei x gleich minus drei liegt.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 4', 'Für x < 0 ist |x| gleich …',
              ['−x', 'x', '0'], 0,
              {0: 'Ja.',
               1: 'x ist negativ — der Betrag aber nicht. Was macht das Vorzeichen positiv?',
               2: 'Null ist der Betrag nur bei x = 0.'},
              sprich='Für x kleiner als null ist der Betrag von x gleich …',
              rueck_sprich={1: 'x ist negativ, der Betrag aber nicht. Was macht das Vorzeichen positiv?',
                            2: 'Null ist der Betrag nur bei x gleich null.'}),
         wahl('Frage 5', 'Für welche x gilt |x| = 5?',
              ['x = 5 und x = −5', 'nur x = 5', 'für kein x'], 0,
              {0: 'Ja.',
               1: 'Wie weit ist −5 von der Null entfernt?',
               2: 'Die Waagrechte y = 5 trifft das V — wie oft?'},
              sprich='Für welche x gilt: Betrag von x gleich fünf?',
              rueck_sprich={1: 'Wie weit ist minus fünf von der Null entfernt?',
                            2: 'Die Waagrechte y gleich fünf trifft das V. Wie oft?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
clip('verschieben', 'Knick sehen: das V verschieben und strecken',
     'y = a · |x − u| + v: Der Knick wandert nach (u | v), die Äste haben die Steigungen ±a, und bei a < 0 wird das V zum Dach.',
     ['Betragsfunktion', 'Verschiebung', 'Streckung', 'Knickpunkt'], [
         sz('Den Knick verschieben',
            'Verschieben geht wie bei jeder Funktion. Mit x minus u wandert der Knick um u nach rechts, mit plus v nach oben. '
            'Der Knickpunkt liegt bei u, v.',
            f(r'y = |x - u| + v', 300, 62),
            n('Knickpunkt @(u \\mid v)@', 430, 'blau', ein=6.0),
            graf(W2, [vk([[0, 1, 0, 0], [2.2, 1, 0, 0], [4.0, 1, 2, 0], [4.6, 1, 2, 0], [6.0, 1, 2, 3]], knick=True)], ein=0.3)),
         sz('Die Steigung',
            'Der Faktor a vor dem Betrag bestimmt die Steigung der Äste. Bei a gleich zwei steigt der rechte Ast mit zwei, '
            'der linke fällt mit minus zwei: das V wird enger. Bei a gleich ein Halb wird es weiter.',
            f(r'y = \fa{a} \cdot |x|', 300, 62),
            n('Äste mit Steigung @\\pm a@', 430, 'blau', ein=5.6),
            graf(W2, [vk([[0, 1, 0, 0]], farbe=5, gestrichelt=True),
                      vk([[0, 1, 0, 0], [4.0, 1, 0, 0], [5.6, 2, 0, 0], [8.6, 2, 0, 0], [9.9, 0.5, 0, 0]])], ein=0.3)),
         sz('Das Dach',
            'Ist a negativ, klappt das V nach unten: ein Dach. Der Knickpunkt ist dann der höchste Punkt.',
            f(r'a \lt 0: \text{ Dach}', 300, 58),
            graf(W2, [vk([[0, 1, 0, 2], [1.4, 1, 0, 2], [3.4, -1, 0, 2]], knick=True)], ein=0.3)),
         sz('Alles zusammen',
            'Zum Beispiel y gleich zwei mal Betrag von x minus eins, minus drei. Knick bei eins, minus drei, Äste mit Steigung '
            'plus und minus zwei. Die Kurve geht von minus drei aus steil nach oben.',
            f(r'y = 2\,|x - 1| - 3', 300, 60),
            n('Knick @(1 \\mid -3)@; Steigung @\\pm 2@', 430, 'blau', ein=4.6),
            graf(W2, [vk([[0, 1, 0, 0], [4.2, 1, 0, 0], [5.8, 1, 1, -3], [6.9, 1, 1, -3], [8.5, 2, 1, -3]], knick=True)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Bei a mal Betrag von x minus u plus v liegt der Knick bei u, v. Die Äste haben die Steigungen plus a '
            'und minus a. Ist a negativ, entsteht ein Dach.',
            titel('Zum Mitnehmen', 250, 76),
            n('@y = a\\,|x - u| + v@|Knick @(u \\mid v)@; Steigung @\\pm a@|@a \\lt 0@: Dach', 400, 'blau', 44, ein=1.2),
            graf(W2, [vk([[0, 2, 1, -3]], knick=True)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-verschieben', 'Knick sehen: Kontrollfragen zum Verschieben',
     'Fünf Vorhersagen zu Knickpunkt, Steigung, Öffnung und Wertemenge von y = a · |x − u| + v.',
     ['Betragsfunktion', 'Knickpunkt', 'Kontrollfragen'], [
         sz('Frage 1',
            'Plus drei im Betrag heisst: um drei nach links. Minus zwei dahinter: um zwei nach unten. Knick bei minus drei, minus zwei.',
            f(r'|x + 3| - 2 = |x - (-3)| - 2', 300, 52, ein=1.0),
            graf(W2, [vk([[0, 1, -3, -2]], knick=True)], ein=1.2)),
         sz('Frage 2',
            'Der Faktor vor dem Betrag ist drei. Rechts vom Knick steigt die Kurve mit Steigung drei.',
            f(r'y = \fa{3}\,|x - 1|', 300, 60, ein=1.0),
            graf(W2, [vk([[0, 3, 1, 0]], knick=True)], ein=1.2)),
         sz('Frage 3',
            'Minus vor dem Betrag: ein Dach. Der höchste Punkt liegt bei zwei, vier.',
            f(r'y = -|x - 2| + 4', 300, 60, ein=1.4),
            graf(W2, []),
            graf(W2, [vk([[0, -1, 2, 4]], knick=True)], ein=1.4)),
         sz('Frage 4',
            'Der Faktor ist minus zwei, also negativ: Das V ist nach unten geöffnet, ein Dach mit Spitze bei null, eins.',
            f(r'a = -2 \lt 0', 300, 62, ein=1.0),
            graf(W2, [vk([[0, -2, 0, 1]], knick=True)], ein=1.2)),
         sz('Frage 5',
            'Der tiefste Punkt ist der Knick bei minus drei. Nach oben geht es unbegrenzt: Wertemenge ab minus drei.',
            f(r'W = [-3;\, \infty[', 300, 62, ein=1.0),
            graf(W2, [vk([[0, 2, 1, -3]], knick=True)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Die Zahl im Betrag steht mit umgekehrtem Vorzeichen, v liest man direkt ab. a gibt Steigung und Öffnung.',
            titel('Zum Mitnehmen', 250, 76),
            n('@|x + 3|@: Knick bei @x = -3@|@a \\gt 0@: V; @a \\lt 0@: Dach', 400, 'blau', 44, ein=1.2),
            graf(W2, [vk([[0, 1, -3, -2]], knick=True)])),
     ], [
         wahl('Frage 1', 'Wo liegt der Knickpunkt von y = |x + 3| − 2?',
              ['(−3 | −2)', '(3 | −2)', '(−2 | 3)'], 0,
              {0: 'Ja.',
               1: 'Vorzeichen: |x + 3| = |x − (−3)|. Wo wird das Argument null?',
               2: 'Zuerst die x-Koordinate: Wo wird x + 3 null?'},
              sprich='Wo liegt der Knickpunkt von y gleich Betrag von x plus drei, minus zwei?',
              rueck_sprich={1: 'Vorzeichen. Wo wird das Argument x plus drei null?',
                            2: 'Zuerst die x-Koordinate. Wo wird x plus drei null?'}),
         wahl('Frage 2', 'Welche Steigung hat der rechte Ast von y = 3|x − 1|?',
              ['3', '−3', '1'], 0,
              {0: 'Ja.',
               1: 'Das ist der linke Ast. Rechts steigt die Kurve.',
               2: 'Die 1 verschiebt nur den Knick. Was steht vor dem Betrag?'},
              sprich='Welche Steigung hat der rechte Ast von y gleich drei mal Betrag von x minus eins?',
              rueck_sprich={1: 'Das ist der linke Ast. Rechts steigt die Kurve.',
                            2: 'Die eins verschiebt nur den Knick. Was steht vor dem Betrag?'}),
         klick('Frage 3', 'Tipp den Knickpunkt von y = −|x − 2| + 4 ins Bild.',
               [2, 4], 'Getroffen: (2 | 4).',
               [{'bei': [-2, 4], 'text': 'Vorzeichen: x − 2 wird bei x = 2 null, nicht bei −2.',
                 'sprich': 'Vorzeichen. x minus zwei wird bei x gleich zwei null, nicht bei minus zwei.'},
                {'bei': [2, -4], 'text': 'Das Minus vor dem Betrag klappt die Kurve, nicht das + 4.',
                 'sprich': 'Das Minus vor dem Betrag klappt die Kurve, nicht das plus vier.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp den Knickpunkt von y gleich minus Betrag von x minus zwei, plus vier, ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 4', 'Wie ist der Graph von y = −2|x| + 1 geöffnet?',
              ['nach unten (Dach)', 'nach oben (V)', 'gar nicht, er ist eine Gerade'], 0,
              {0: 'Ja.',
               1: 'Achte auf das Vorzeichen vor dem Betrag.',
               2: 'Bei x = 0 hat −2|x| einen Knick — wohin zeigen die Äste?'},
              sprich='Wie ist der Graph von y gleich minus zwei mal Betrag von x, plus eins, geöffnet?',
              rueck_sprich={1: 'Achte auf das Vorzeichen vor dem Betrag.',
                            2: 'Bei x gleich null hat minus zwei mal Betrag von x einen Knick. Wohin zeigen die Äste?'}),
         wahl('Frage 5', 'Welche Wertemenge hat y = 2|x − 1| − 3?',
              ['[−3; ∞[', 'ℝ', '[−1; ∞['], 0,
              {0: 'Ja.',
               1: 'Der Betrag ist nie negativ — wie tief kommt die Kurve also höchstens?',
               2: 'Die tiefste Stelle ist der Knick. Wie hoch liegt er?'},
              sprich='Welche Wertemenge hat y gleich zwei mal Betrag von x minus eins, minus drei?',
              rueck_sprich={1: 'Der Betrag ist nie negativ. Wie tief kommt die Kurve also höchstens?',
                            2: 'Die tiefste Stelle ist der Knick. Wie hoch liegt er?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
clip('umklappen', 'Knick sehen: das Umklapp-Prinzip',
     'Vom Graphen von f zum Graphen von |f|: Was unter der x-Achse liegt, klappt nach oben — an den Nullstellen entstehen Knicke.',
     ['Betragsfunktion', 'Umklappen', 'Knick', 'Nullstelle'], [
         sz('Eine Gerade',
            'Was macht der Betrag mit einer ganzen Funktion? Nehmen wir f von x gleich x minus zwei. Rechts von zwei ist f positiv, '
            'da ändert sich nichts. Links von zwei ist f negativ: Der Betrag macht diese Werte positiv, das Stück klappt nach oben.',
            f(r'y = |\,x - 2\,|', 300, 62),
            graf(WU, [fest('x-2', farbe=5)], ein=0.3),
            graf(WU, [fest('x-2', farbe=5), fest('abs(x-2)', farbe=1, gestrichelt=False)], ein=11.4,
                 punkte=[pt(2, 0, 1, '(2 | 0)', [2.3, -0.8])])),
         sz('Eine Parabel',
            'Bei der Parabel x hoch zwei minus vier liegt das Stück zwischen minus zwei und zwei unter der x-Achse. Es klappt hoch: '
            'Aus dem Scheitel null, minus vier wird ein Buckel bei null, vier. Es entsteht ein W.',
            f(r'y = |\,x^2 - 4\,|', 300, 62),
            n('Scheitel @(0 \\mid -4) \\to (0 \\mid 4)@', 430, 'blau', ein=8.8),
            graf(WU, [fest('x**2-4', farbe=5)], ein=0.3),
            graf(WU, [fest('x**2-4', farbe=5), fest('abs(x**2-4)', farbe=1, gestrichelt=False)], ein=7.0)),
         sz('Knicke',
            'Wo f die x-Achse schneidet, also das Vorzeichen wechselt, entstehen Knicke: bei der Geraden einer, bei der Parabel zwei. '
            'Der Graph von Betrag f liegt nie unter der x-Achse.',
            f(r'\text{Knicke, wo } f \text{ das Vorzeichen wechselt}', 300, 46),
            graf(WU, [fest('abs(x**2-4)', farbe=1, gestrichelt=False)], ein=0.3,
                 punkte=[pt(-2, 0, 1, '(−2 | 0)', [-2.2, -0.8], 'end'), pt(2, 0, 1, '(2 | 0)', [2.2, -0.8])])),
         sz('Nicht alles spiegeln',
            'Achtung: Betrag f ist nicht minus f. Gespiegelt wird nur, was unten liegt. Wer die ganze Kurve spiegelt, '
            'erhält minus f, und das liegt teilweise unter der Achse.',
            f(r'|f(x)| \ne -f(x)', 300, 62),
            n('nur die Teile unter der @x@-Achse', 430, 'rot', ein=3.4),
            graf(WU, [fest('-(x**2-4)', farbe=4), fest('abs(x**2-4)', farbe=1, gestrichelt=False)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Für den Graphen von Betrag f zeichnet man f und klappt alle Teile unter der x-Achse nach oben. '
            'Wo f die x-Achse schneidet, entstehen Knicke.',
            titel('Zum Mitnehmen', 250, 76),
            n('unten → hochklappen|oben → bleibt|Knicke, wo @f@ die @x@-Achse schneidet', 400, 'blau', 44, ein=1.2),
            graf(WU, [fest('x**2-4', farbe=5), fest('abs(x**2-4)', farbe=1, gestrichelt=False)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-umklappen', 'Knick sehen: Kontrollfragen zum Umklappen',
     'Fünf Vorhersagen zu Knicken, umgeklappten Scheiteln und Funktionen, an denen der Betrag nichts ändert.',
     ['Umklappen', 'Kontrollfragen'], [
         sz('Frage 1',
            'x hoch zwei minus neun hat zwei Nullstellen, bei minus drei und drei. Dort entstehen die zwei Knicke.',
            f(r'x^2 - 9 = 0 \;\Rightarrow\; x = \pm 3', 300, 54, ein=1.0),
            graf(dict(xbereich=[-5, 5], ybereich=[-10, 12], xteilung=yt(-4, -2, 2, 4), yteilung=yt(-8, -4, 4, 8)),
                 [fest('x**2-9', farbe=5), fest('abs(x**2-9)', farbe=1, gestrichelt=False)], ein=1.2,
                 punkte=[pt(-3, 0, 1), pt(3, 0, 1)])),
         sz('Frage 2',
            'Der Scheitel null, minus eins liegt unter der Achse. Er klappt hoch nach null, eins.',
            f(r'(0 \mid -1) \to (0 \mid 1)', 300, 58, ein=1.0),
            graf(WU, [fest('x**2-1', farbe=5), fest('abs(x**2-1)', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 3',
            'x hoch zwei plus zwei ist immer mindestens zwei, also nie negativ. Es gibt nichts umzuklappen: Der Graph bleibt gleich.',
            f(r'x^2 + 2 \ge 2 \gt 0', 300, 58, ein=1.0),
            graf(WU, [fest('x**2+2', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 4',
            'Zwei x plus vier ist null bei x gleich minus zwei. Dort liegt der Knick, auf der x-Achse.',
            f(r'2x + 4 = 0 \;\Rightarrow\; x = -2', 300, 54, ein=1.4),
            graf(WU, [fest('2*x+4', farbe=5)]),
            graf(WU, [fest('2*x+4', farbe=5), fest('abs(2*x+4)', farbe=1, gestrichelt=False)], ein=1.4,
                 punkte=[pt(-2, 0, 1, '(−2 | 0)', [-2.2, -0.8], 'end')])),
         sz('Frage 5',
            'Ein Betrag ist nie negativ. Der Graph von Betrag f liegt nie unter der x-Achse, er berührt sie höchstens.',
            f(r'|f(x)| \ge 0', 300, 62, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Knicke, wo f die x-Achse schneidet. Was unten liegt, klappt hoch, was oben liegt, bleibt.',
            titel('Zum Mitnehmen', 250, 76),
            n('Vorzeichenwechsel von @f@ → Knick von @|f|@|@f \\ge 0@ überall: nichts zu tun', 400, 'blau', 44, ein=1.2),
            graf(WU, [fest('x**2-4', farbe=5), fest('abs(x**2-4)', farbe=1, gestrichelt=False)])),
     ], [
         wahl('Frage 1', 'Wie viele Knicke hat der Graph von y = |x² − 9|?',
              ['2', '1', '0'], 0,
              {0: 'Ja.',
               1: 'Wie viele Nullstellen hat x² − 9?',
               2: 'Wo x² − 9 das Vorzeichen wechselt, entsteht ein Knick. Wie oft?'},
              sprich='Wie viele Knicke hat der Graph von y gleich Betrag von x hoch zwei minus neun?',
              rueck_sprich={1: 'Wie viele Nullstellen hat x hoch zwei minus neun?',
                            2: 'Wo x hoch zwei minus neun das Vorzeichen wechselt, entsteht ein Knick. Wie oft?'}),
         wahl('Frage 2', 'Wohin kommt der Scheitel (0 | −1) von y = x² − 1, wenn man |x² − 1| zeichnet?',
              ['(0 | 1)', '(0 | −1)', '(1 | 0)'], 0,
              {0: 'Ja.',
               1: 'Er liegt unter der x-Achse — bleibt er dort?',
               2: 'Umgeklappt wird an der x-Achse: Die x-Koordinate bleibt.'},
              sprich='Wohin kommt der Scheitel null, minus eins von y gleich x hoch zwei minus eins, wenn man den Betrag zeichnet?',
              rueck_sprich={1: 'Er liegt unter der x-Achse. Bleibt er dort?',
                            2: 'Umgeklappt wird an der x-Achse. Die x-Koordinate bleibt.'}),
         wahl('Frage 3', 'Was ändert der Betrag an y = x² + 2?',
              ['nichts', 'er klappt den Scheitel hoch', 'zwei Knicke entstehen'], 0,
              {0: 'Ja.',
               1: 'Liegt der Scheitel (0 | 2) unter der x-Achse?',
               2: 'Knicke entstehen an Nullstellen. Hat x² + 2 welche?'},
              sprich='Was ändert der Betrag an y gleich x hoch zwei plus zwei?',
              rueck_sprich={1: 'Liegt der Scheitel null, zwei unter der x-Achse?',
                            2: 'Knicke entstehen an Nullstellen. Hat x hoch zwei plus zwei welche?'}),
         klick('Frage 4', 'Gestrichelt: f(x) = 2x + 4. Tipp den Knick von y = |2x + 4| ins Bild.',
               [-2, 0], 'Getroffen: (−2 | 0).',
               [{'bei': [0, 4], 'text': 'Dort schneidet f die y-Achse. Der Knick liegt, wo f null wird.',
                 'sprich': 'Dort schneidet f die y-Achse. Der Knick liegt, wo f null wird.'},
                {'bei': [2, 0], 'text': 'Vorzeichen: 2x + 4 = 0 heisst x = −2.',
                 'sprich': 'Vorzeichen. Zwei x plus vier gleich null heisst x gleich minus zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Gestrichelt ist f von x gleich zwei x plus vier. Tipp den Knick von y gleich Betrag von zwei x plus vier ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 5', 'Kann der Graph von y = |f(x)| unter der x-Achse liegen?',
              ['nein, nie', 'ja, wo f negativ ist', 'ja, links der y-Achse'], 0,
              {0: 'Ja.',
               1: 'Genau dort wirkt der Betrag. Was macht er mit negativen Werten?',
               2: 'Es zählt das Vorzeichen der Werte, nicht die Seite.'},
              sprich='Kann der Graph von y gleich Betrag von f von x unter der x-Achse liegen?',
              rueck_sprich={1: 'Genau dort wirkt der Betrag. Was macht er mit negativen Werten?',
                            2: 'Es zählt das Vorzeichen der Werte, nicht die Seite.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
clip('abschnittsweise', 'Knick sehen: abschnittsweise schreiben',
     'Betragsterme ohne Betragsstriche: Fallunterscheidung an der Nullstelle des Arguments — und die Wanne aus zwei Beträgen.',
     ['abschnittsweise', 'Fallunterscheidung', 'Betragsterm', 'Wanne'], [
         sz('Die Grenze',
            'Betrag von zwei x minus sechs. Wo wird das Argument null? Zwei x minus sechs gleich null bei x gleich drei. '
            'Das ist die Grenze zwischen den beiden Fällen und die Stelle des Knicks.',
            f(r'2x - 6 = 0 \;\Rightarrow\; x = 3', 300, 56),
            graf(dict(xbereich=[-2, 7], ybereich=[-2, 8], xteilung=yt(2, 4, 6), yteilung=yt(2, 4, 6)),
                 [vk([[0, 2, 3, 0]], knick=True)], ein=0.3)),
         sz('Zwei Fälle',
            'Rechts von drei ist zwei x minus sechs positiv: Der Betrag ändert nichts. Links von drei ist es negativ: '
            'Das Vorzeichen des ganzen Terms wird gedreht, minus zwei x plus sechs.',
            f(r'|2x - 6| = \begin{cases} \fc{2x - 6} & x \ge 3 \\ \fc{-2x + 6} & x \lt 3 \end{cases}', 330, 50, ein=0.6),
            graf(dict(xbereich=[-2, 7], ybereich=[-2, 8], xteilung=yt(2, 4, 6), yteilung=yt(2, 4, 6)),
                 [fest('2*x-6', farbe=3, von=3), fest('-2*x+6', farbe=3, bis=3)], ein=0.4)),
         sz('Die Wanne',
            'Addiert man zwei Beträge, etwa Betrag von x plus eins plus Betrag von x minus drei, entstehen zwei Grenzen: '
            'minus eins und drei. Dazwischen ist die Summe konstant vier, so gross wie der Abstand der beiden Stellen. '
            'Der Graph sieht aus wie eine Wanne.',
            f(r'y = |x + 1| + |x - 3|', 300, 56),
            n('Boden: @y = 4@ von @-1@ bis @3@', 430, 'blau', ein=9.4),
            graf(WW, [fest('abs(x+1)+abs(x-3)', farbe=1, gestrichelt=False)], ein=0.3,
                 punkte=[pt(-1, 4, 1, '(−1 | 4)', [-1.2, 4.7], 'end'), pt(3, 4, 1, '(3 | 4)', [3.2, 4.7])])),
         sz('Drei Abschnitte',
            'Abschnittsweise geschrieben hat die Wanne drei Teile: links minus zwei x plus zwei, in der Mitte vier, '
            'rechts zwei x minus zwei.',
            f(r'y = \begin{cases} \fc{-2x + 2} & x \lt -1 \\ \fc{4} & -1 \le x \le 3 \\ \fc{2x - 2} & x \gt 3 \end{cases}', 340, 46, ein=0.6),
            graf(WW, [fest('-2*x+2', farbe=3, bis=-1), fest('4', farbe=3, von=-1, bis=3), fest('2*x-2', farbe=3, von=3)], ein=0.4)),
         sz('Merke',
            'Zum Mitnehmen: Betragsstriche loswerden heisst Fälle unterscheiden, an der Nullstelle des Arguments. '
            'Wo das Argument negativ ist, dreht man das Vorzeichen des ganzen Terms.',
            titel('Zum Mitnehmen', 250, 76),
            n('Grenze: Argument @= 0@|negativ → ganzes Vorzeichen drehen', 400, 'blau', 44, ein=1.2),
            graf(dict(xbereich=[-2, 7], ybereich=[-2, 8], xteilung=yt(2, 4, 6), yteilung=yt(2, 4, 6)),
                 [vk([[0, 2, 3, 0]], knick=True)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-abschnittsweise', 'Knick sehen: Kontrollfragen zum abschnittsweisen Schreiben',
     'Fünf Vorhersagen zu Grenzen, Fällen und zur Wanne aus zwei Beträgen.',
     ['abschnittsweise', 'Kontrollfragen'], [
         sz('Frage 1',
            'Drei x plus sechs ist null bei x gleich minus zwei. Dort liegt die Grenze.',
            f(r'3x + 6 = 0 \;\Rightarrow\; x = -2', 300, 54, ein=1.0)),
         sz('Frage 2',
            'Für x kleiner als zwei ist x minus zwei negativ. Also dreht man das Vorzeichen: zwei minus x.',
            f(r'x \lt 2: \; |x - 2| = -(x - 2) = 2 - x', 300, 46, ein=1.0)),
         sz('Frage 3',
            'Zwischen null und vier ist die Summe der Abstände zu null und zu vier immer vier.',
            f(r'|x| + |x - 4| = 4 \quad (0 \le x \le 4)', 300, 46, ein=1.0),
            graf(WW, [fest('abs(x)+abs(x-4)', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 4',
            'Der Boden reicht von minus zwei bis eins. Sein rechtes Ende liegt bei eins, drei.',
            f(r'|x + 2| + |x - 1|: \text{ Boden } y = 3', 300, 46, ein=1.4),
            graf(WW, [fest('abs(x+2)+abs(x-1)', farbe=1, gestrichelt=False)]),
            graf(WW, [fest('abs(x+2)+abs(x-1)', farbe=1, gestrichelt=False)], ein=1.4,
                 punkte=[pt(1, 3, 1, '(1 | 3)', [1.3, 2.2])])),
         sz('Frage 5',
            'Links des Bodens fallen beide Beträge: Steigung minus eins plus minus eins, also minus zwei.',
            f(r'-1 + (-1) = -2', 300, 62, ein=1.0),
            graf(WW, [fest('abs(x+1)+abs(x-3)', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Grenze an der Nullstelle des Arguments. Wo das Argument negativ ist, das Vorzeichen drehen. Zwei Beträge ergeben drei Abschnitte.',
            titel('Zum Mitnehmen', 250, 76),
            n('Argument negativ → Vorzeichen drehen|@|x - 2| = 2 - x@ für @x \\lt 2@|Wanne: drei Abschnitte', 400, 'blau', 44, ein=1.2),
            graf(WW, [fest('abs(x+1)+abs(x-3)', farbe=1, gestrichelt=False)])),
     ], [
         wahl('Frage 1', 'Bei welchem x liegt die Grenze der Fälle von |3x + 6|?',
              ['x = −2', 'x = 2', 'x = −6'], 0,
              {0: 'Ja.',
               1: 'Vorzeichen: Setz das Argument 3x + 6 gleich null.',
               2: 'Nicht −6 ablesen: 3x + 6 = 0 auflösen.'},
              sprich='Bei welchem x liegt die Grenze der Fälle vom Betrag von drei x plus sechs?',
              rueck_sprich={1: 'Vorzeichen. Setz das Argument drei x plus sechs gleich null.',
                            2: 'Nicht minus sechs ablesen. Drei x plus sechs gleich null auflösen.'}),
         wahl('Frage 2', 'Für x < 2 ist |x − 2| gleich …',
              ['2 − x', 'x − 2', 'x + 2'], 0,
              {0: 'Ja.',
               1: 'Für x < 2 ist x − 2 negativ. Was macht der Betrag damit?',
               2: 'Das Vorzeichen des ganzen Terms drehen, nicht nur der Zahl.'},
              sprich='Für x kleiner als zwei ist der Betrag von x minus zwei gleich …',
              rueck_sprich={1: 'Für x kleiner als zwei ist x minus zwei negativ. Was macht der Betrag damit?',
                            2: 'Das Vorzeichen des ganzen Terms drehen, nicht nur der Zahl.'}),
         wahl('Frage 3', 'Welchen Wert hat y = |x| + |x − 4| für x zwischen 0 und 4?',
              ['immer 4', 'immer 0', 'er wächst von 0 bis 8'], 0,
              {0: 'Ja.',
               1: 'Setz x = 2 ein: |2| + |−2| = ?',
               2: 'Setz x = 1 und x = 3 ein und vergleiche.'},
              sprich='Welchen Wert hat y gleich Betrag von x plus Betrag von x minus vier, für x zwischen null und vier?',
              rueck_sprich={1: 'Setz x gleich zwei ein. Betrag von zwei plus Betrag von minus zwei gleich?',
                            2: 'Setz x gleich eins und x gleich drei ein und vergleiche.'}),
         klick('Frage 4', 'Tipp das rechte Ende des flachen Bodens von y = |x + 2| + |x − 1| ins Bild.',
               [1, 3], 'Getroffen: (1 | 3).',
               [{'bei': [-2, 3], 'text': 'Das ist das linke Ende. Gesucht ist das rechte.',
                 'sprich': 'Das ist das linke Ende. Gesucht ist das rechte.'},
                {'bei': [1, 0], 'text': 'Die Wanne liegt höher: Wie gross ist die Summe bei x = 1?',
                 'sprich': 'Die Wanne liegt höher. Wie gross ist die Summe bei x gleich eins?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp das rechte Ende des flachen Bodens von y gleich Betrag von x plus zwei plus Betrag von x minus eins ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 5', 'Welche Steigung hat y = |x + 1| + |x − 3| links des Bodens (x < −1)?',
              ['−2', '−1', '0'], 0,
              {0: 'Ja.',
               1: 'Beide Beträge fallen dort — wie viel zusammen?',
               2: 'Flach ist nur der Boden zwischen −1 und 3.'},
              sprich='Welche Steigung hat y gleich Betrag von x plus eins plus Betrag von x minus drei, links des Bodens, also für x kleiner als minus eins?',
              rueck_sprich={1: 'Beide Beträge fallen dort. Wie viel zusammen?',
                            2: 'Flach ist nur der Boden zwischen minus eins und drei.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
clip('gleichungen', 'Knick sehen: Betragsgleichungen und -ungleichungen',
     'Gleichungen und Ungleichungen mit Beträgen am Graphen lösen und rechnerisch bestätigen: zwei Fälle, vier Lösungen beim W.',
     ['Betragsgleichung', 'Betragsungleichung', 'Fallunterscheidung'], [
         sz('Am Graphen',
            'Betrag von x minus eins gleich drei. Im Bild: Wo trifft die Waagrechte y gleich drei das V? Zweimal, '
            'bei minus zwei und bei vier.',
            f(r'|x - 1| = 3', 300, 62),
            graf(W2, [vk([[0, 1, 1, 0]], knick=True), fest('3', farbe=2)], ein=0.3),
            graf(W2, [vk([[0, 1, 1, 0]], knick=True), fest('3', farbe=2)], ein=6.0,
                 punkte=[pt(-2, 3, 2, '−2', [-2.2, 3.6], 'end'), pt(4, 3, 2, '4', [4.2, 3.6])])),
         sz('Rechnen',
            'Rechnerisch heisst das: x minus eins ist drei oder minus drei. Also x gleich vier oder x gleich minus zwei. '
            'Die Skizze zeigt, dass es genau zwei Lösungen sind.',
            f(r'x - 1 = 3 \;\vee\; x - 1 = -3', 300, 52),
            f(r'L = \{-2;\, 4\}', 420, 58, ein=6.2)),
         sz('Ungleichung',
            'Und wo ist der Betrag kleiner oder gleich drei? Dort, wo das V unter der Waagrechten liegt: zwischen den Schnittstellen.',
            f(r'|x - 1| \le 3 \;\Rightarrow\; -2 \le x \le 4', 300, 48, ein=3.6),
            graf(W2, [vk([[0, 1, 1, 0]], knick=True), fest('3', farbe=2)], ein=0.3),
            graf(W2, [vk([[0, 1, 1, 0]], knick=True), vk([[0, 1, 1, 0]], farbe=2, von=-2, bis=4, dicke=9), fest('3', farbe=2)], ein=3.7)),
         sz('Das W',
            'Beim W von Betrag von x hoch zwei minus vier kann es vier Lösungen geben. Betrag gleich drei: x hoch zwei minus vier ist drei '
            'oder minus drei. Das gibt plus minus Wurzel sieben und plus minus eins.',
            f(r'|x^2 - 4| = 3', 300, 58),
            f(r'L = \{-\sqrt7;\, -1;\, 1;\, \sqrt7\}', 420, 50, ein=9.3),
            graf(WU, [fest('abs(x**2-4)', farbe=1, gestrichelt=False), fest('3', farbe=2)], ein=0.3),
            graf(WU, [fest('abs(x**2-4)', farbe=1, gestrichelt=False), fest('3', farbe=2)], ein=9.3,
                 punkte=[pt(-7 ** 0.5, 3, 2), pt(-1, 3, 2), pt(1, 3, 2), pt(7 ** 0.5, 3, 2)])),
         sz('Wie viele?',
            'Wie viele Lösungen es gibt, zeigt die Höhe der Waagrechten. Unter null keine, bei null zwei, zwischen null und vier vier, '
            'auf dem Buckel vier genau drei, darüber nur noch zwei.',
            f(r'|x^2 - 4| = c', 300, 58),
            n('@c \\lt 0@: keine; @c = 0@: zwei|@0 \\lt c \\lt 4@: vier; @c = 4@: drei|@c \\gt 4@: zwei', 430, 'orange', ein=4.0),
            graf(WU, [fest('abs(x**2-4)', farbe=1, gestrichelt=False), fest('4', farbe=2)], ein=0.3,
                 punkte=[pt(-8 ** 0.5, 4, 2), pt(0, 4, 2), pt(8 ** 0.5, 4, 2)])),
         sz('Merke',
            'Zum Mitnehmen: Erst skizzieren und zählen, dann rechnen. Betrag von A gleich c heisst A gleich c oder A gleich minus c.',
            titel('Zum Mitnehmen', 250, 76),
            n('@|A| = c@ @(c \\ge 0)@: @A = c \\;\\vee\\; A = -c@|Skizze zählt die Lösungen', 400, 'blau', 44, ein=1.2),
            graf(W2, [vk([[0, 1, 1, 0]], knick=True), fest('3', farbe=2)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
clip('kontrolle-gleichungen', 'Knick sehen: Kontrollfragen zu Gleichungen und Ungleichungen',
     'Fünf Vorhersagen zu Lösungen von Betragsgleichungen und -ungleichungen.',
     ['Betragsgleichung', 'Kontrollfragen'], [
         sz('Frage 1',
            'x plus zwei ist fünf oder minus fünf. Also x gleich drei oder x gleich minus sieben.',
            f(r'x + 2 = \pm 5 \;\Rightarrow\; L = \{-7;\, 3\}', 300, 50, ein=1.0),
            graf(W2, [vk([[0, 1, -2, 0]]), fest('5', farbe=2)], ein=1.2, punkte=[pt(-7, 5, 2), pt(3, 5, 2)])),
         sz('Frage 2',
            'Ein Betrag ist nie negativ. Betrag gleich minus eins hat keine Lösung.',
            f(r'|x - 3| = -1: \; L = \{\,\}', 300, 56, ein=1.0),
            graf(W2, [vk([[0, 1, 3, 0]]), fest('-1', farbe=4)], ein=1.2)),
         sz('Frage 3',
            'Betrag von x kleiner als zwei: Der Abstand zur Null ist kleiner als zwei. Also liegt x zwischen minus zwei und zwei.',
            f(r'|x| \lt 2 \;\Rightarrow\; -2 \lt x \lt 2', 300, 50, ein=1.0),
            graf(W2, [vk([[0, 1, 0, 0]]), vk([[0, 1, 0, 0]], farbe=2, von=-2, bis=2, dicke=9), fest('2', farbe=2)], ein=1.2)),
         sz('Frage 4',
            'Die rechte Lösung von Betrag von x minus eins gleich zwei ist drei.',
            f(r'x - 1 = 2 \;\Rightarrow\; x = 3', 300, 54, ein=1.4),
            graf(W2, [vk([[0, 1, 1, 0]]), fest('2', farbe=2)]),
            graf(W2, [vk([[0, 1, 1, 0]]), fest('2', farbe=2)], ein=1.4, punkte=[pt(3, 2, 2, '(3 | 2)', [3.3, 1.2])])),
         sz('Frage 5',
            'Die Waagrechte y gleich vier berührt den Buckel und schneidet die beiden äusseren Äste: drei Lösungen.',
            f(r'|x^2 - 4| = 4: \; 3 \text{ Lösungen}', 300, 50, ein=1.0),
            graf(WU, [fest('abs(x**2-4)', farbe=1, gestrichelt=False), fest('4', farbe=2)], ein=1.2,
                 punkte=[pt(-8 ** 0.5, 4, 2), pt(0, 4, 2), pt(8 ** 0.5, 4, 2)])),
         sz('Merke',
            'Zum Mitnehmen: Betrag gleich c hat zwei Fälle. Betrag gleich einer negativen Zahl hat keine Lösung. Ungleichungen liest man am Graphen ab.',
            titel('Zum Mitnehmen', 250, 76),
            n('@|A| = c@: @A = \\pm c@; @c \\lt 0@: @L = \\{\\,\\}@|@|A| \\lt c@: zwischen den Schnittstellen', 400, 'blau', 42, ein=1.2),
            graf(W2, [vk([[0, 1, 1, 0]]), fest('2', farbe=2)])),
     ], [
         wahl('Frage 1', 'Löse |x + 2| = 5.',
              ['x = 3 oder x = −7', 'x = 3', 'x = 7 oder x = −3'], 0,
              {0: 'Ja.',
               1: 'Es gibt zwei Fälle: x + 2 = 5 und x + 2 = −5.',
               2: 'Vorzeichen: x + 2 = 5 heisst x = 3.'},
              sprich='Löse: Betrag von x plus zwei gleich fünf.',
              rueck_sprich={1: 'Es gibt zwei Fälle: x plus zwei gleich fünf und x plus zwei gleich minus fünf.',
                            2: 'Vorzeichen. x plus zwei gleich fünf heisst x gleich drei.'}),
         wahl('Frage 2', 'Welche Lösungsmenge hat |x − 3| = −1?',
              ['keine Lösung', '{2; 4}', '{2}'], 0,
              {0: 'Ja.',
               1: 'Setz x = 2 ein: Ist |2 − 3| = −1?',
               2: 'Kann ein Betrag negativ sein?'},
              sprich='Welche Lösungsmenge hat: Betrag von x minus drei gleich minus eins?',
              rueck_sprich={1: 'Setz x gleich zwei ein. Ist der Betrag von zwei minus drei gleich minus eins?',
                            2: 'Kann ein Betrag negativ sein?'}),
         wahl('Frage 3', 'Für welche x gilt |x| < 2?',
              ['−2 < x < 2', 'x < 2', 'x < −2 oder x > 2'], 0,
              {0: 'Ja.',
               1: 'Und x = −5? Ist |−5| < 2?',
               2: 'Das ist |x| > 2. Wo liegt das V unter der Waagrechten?'},
              sprich='Für welche x gilt: Betrag von x kleiner als zwei?',
              rueck_sprich={1: 'Und x gleich minus fünf? Ist der Betrag von minus fünf kleiner als zwei?',
                            2: 'Das ist Betrag von x grösser als zwei. Wo liegt das V unter der Waagrechten?'}),
         klick('Frage 4', 'Tipp die rechte Lösung von |x − 1| = 2 ins Bild (Schnittpunkt mit y = 2).',
               [3, 2], 'Getroffen: (3 | 2).',
               [{'bei': [-1, 2], 'text': 'Das ist die linke Lösung.',
                 'sprich': 'Das ist die linke Lösung.'},
                {'bei': [1, 0], 'text': 'Das ist der Knick. Gesucht ist der Schnittpunkt mit y = 2.',
                 'sprich': 'Das ist der Knick. Gesucht ist der Schnittpunkt mit y gleich zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Tipp die rechte Lösung von Betrag von x minus eins gleich zwei ins Bild, den Schnittpunkt mit y gleich zwei.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
         wahl('Frage 5', 'Wie viele Lösungen hat |x² − 4| = 4?',
              ['3', '4', '2'], 0,
              {0: 'Ja.',
               1: 'Der Buckel ist genau 4 hoch — wie oft trifft ihn die Waagrechte?',
               2: 'Und der Buckel bei (0 | 4)?'},
              sprich='Wie viele Lösungen hat: Betrag von x hoch zwei minus vier gleich vier?',
              rueck_sprich={1: 'Der Buckel ist genau vier hoch. Wie oft trifft ihn die Waagrechte?',
                            2: 'Und der Buckel bei null, vier?'}),
     ], art='Kontrollclip')
