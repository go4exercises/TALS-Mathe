"""Erzeugt die zehn Drehbücher des Leitprogramms Polynomfunktionen (04.10.2026).

  python3 scripts/lp/polynomfunktionen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie beim Vorbild (Leitprogramm Potenz- und Wurzelfunktionen): Bild rechts
(x 1010, y 175, 760 × 760), Formeln und Notizen links (x 150), Theme begreifbar-schlicht.

**Bewegte Polynome** (HOWTO-clips.md, «Polynome in Linearfaktordarstellung»): Stützpunkte
`[t, a, x1, x2, …]` für y = a·(x−x1)·(x−x2)·…, mit den Begleitern `nullstellen` und
`extrema`. Wo das Polynom keine reellen Linearfaktoren hat (x² + 1, verschobene
Quartik), steht eine feste `formel`.

Farben — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15), gleich wie auf der Seite:
  1 blau   = die Kurve und ihr Leitkoeffizient a       \\fa{…}
  2 orange = Nullstellen und Linearfaktoren            \\fb{…}
  3 grün   = Hoch- und Tiefpunkte                      \\fc{…}
  4 rot    = Gegenbeispiel, Fehler                     \\fd{…}
  5 Tinte  = neutral: Leitterm, Bezugskurve, Hilfspunkte
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


def graf(W, kurven=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=[], punkte=list(punkte), pfeile=True, **W)
    g.update(kw)
    return g


def ueber(W, punkte=(), figuren=(), kurven=(), ein=0.05):
    """Deckblatt ueber einem Graf: gleiches Fenster, ohne Achsen und Karo — nur Punkte,
    Figuren oder Kurven, die spaeter dazukommen (ein je fester Punkt gibt es im graf nicht)."""
    return graf(W, kurven, punkte, ein=ein, raster=False, achsen=False, figuren=list(figuren))


def poly(stuetz, farbe=1, nullstellen=None, extrema=None, marken=None, von=None, bis=None,
         gestrichelt=False, dicke=None):
    """Bewegtes Polynom: Stuetzpunkte [t, a, x1, x2, …] fuer a·(x−x1)(x−x2)…"""
    d = {'bewegung': stuetz, 'polynom': True, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if nullstellen is not None:
        d['nullstellen'] = nullstellen
    if extrema is not None:
        d['extrema'] = extrema
    if marken is not None:
        d['marken'] = marken
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    return d


def fest(formel, farbe=5, gestrichelt=True, dicke=None):
    """Feste Kurve aus einer Formel — fuer Polynome ohne reelle Linearfaktoren."""
    d = dict(formel=formel, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
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
    alt = R + 'clips/s3-3-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 's3-3-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Polynomfunktionen',
         'fach': 'Schwerpunktfach', 'lerngebiet': '3 · Funktionen',
         'lektion': ['s3-3'], 'stufe': ['BM2'], 'datum': '2026-10-04',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Polynom sehen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms polynomfunktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    anwenden_fragebild(d)                               # beim Fragen nur das Gegebene
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, str(w).replace('-', '−')] for w in werte]


# Fenster. Die Achsen tragen verschiedene Spannen, wo die Kurve es verlangt
# (STYLEGUIDE: keine 1:1-Forderung); geteilt wird dann in Zweierschritten.
W1 = dict(xbereich=[-4, 5], ybereich=[-8, 10], yteilung=yt(-8, -6, -4, -2, 2, 4, 6, 8, 10))
W2 = dict(xbereich=[-4, 4], ybereich=[-6, 6], yteilung=yt(-6, -4, -2, 2, 4, 6))
W3 = dict(xbereich=[-3, 3], ybereich=[-6, 6], yteilung=yt(-6, -4, -2, 2, 4, 6))

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# Beispiel: f(x) = 0.5(x+2)(x−1)(x−3) = 0.5x³ − x² − 2.5x + 3 — der Startwert der Simulation
# und des Linearfaktor-Baukastens auf der Themenseite.
B1 = [0.5, -2, 1, 3]
clip('linearfaktoren', 'Polynom sehen: Linearfaktoren und Nullstellen',
     'Was eine Polynomfunktion ist, was Grad und Leitkoeffizient sagen — und wie die Nullstellen in den Linearfaktoren stehen.',
     ['Polynomfunktion', 'Grad', 'Leitkoeffizient', 'Linearfaktor', 'Nullstelle'], [
         sz('Polynomfunktion',
            'Eine Polynomfunktion ist eine Summe von Potenzen von x mit natürlichen Exponenten, jede mit einem Faktor. '
            'Der höchste Exponent heisst Grad, sein Faktor heisst Leitkoeffizient. Hier: Grad drei, Leitkoeffizient null Komma fünf.',
            titel('Polynomfunktion', 280, 80),
            f(r'f(x) = \fa{0.5}x^3 - x^2 - 2.5x + 3', 430, 54, ein=1.0),
            n('Grad @3@ — der höchste Exponent|Leitkoeffizient @\\fa{0.5}@ — sein Faktor', 560, 'blau', 44, ein=8.0),
            graf(W1, [poly([[0] + B1])], ein=3.0)),
         sz('Produktform',
            'Dieselbe Funktion lässt sich als Produkt schreiben: null Komma fünf mal Klammer x plus zwei, '
            'mal Klammer x minus eins, mal Klammer x minus drei. Jede Klammer heisst Linearfaktor.',
            f(r'f(x) = \fa{0.5}\,(x \fb{+ 2})(x \fb{- 1})(x \fb{- 3})', 300, 50),
            n('drei Linearfaktoren —|ausmultipliziert wieder die Summenform', 440, 'orange'),
            graf(W1, [poly([[0] + B1])])),
         sz('Nullprodukt',
            'Ein Produkt ist null, sobald ein Faktor null ist. x minus eins wird null bei eins, x minus drei bei drei, '
            'x plus zwei bei minus zwei. Genau dort schneidet der Graph die x-Achse.',
            f(r'x \fb{- 1} = 0 \;\Rightarrow\; x = \fb{1}', 290, 50, ein=3.3),
            f(r'x \fb{- 3} = 0 \;\Rightarrow\; x = \fb{3}', 370, 50, ein=5.2),
            f(r'x \fb{+ 2} = 0 \;\Rightarrow\; x = \fb{-2}', 450, 50, ein=6.8),
            n('in der Klammer steht die Nullstelle|mit umgekehrtem Vorzeichen', 560, 'orange', ein=3.0),
            graf(W1, [poly([[0] + B1])]),
            # Nullstellen einzeln zum Wort (1.9–8.3 s): «bei eins», «bei drei», «bei minus zwei»
            ueber(W1, [pt(1, 0, 2, '(1 | 0)', [1.15, 0.45])], ein=4.4),
            ueber(W1, [pt(3, 0, 2, '(3 | 0)', [3.2, -1.45])], ein=6.0),
            ueber(W1, [pt(-2, 0, 2, '(−2 | 0)', [-2.15, 0.45], 'end')], ein=7.6)),
         sz('Eine Nullstelle wandert',
            'Ändert man einen Linearfaktor, wandert seine Nullstelle mit. Aus x minus drei wird x minus vier, '
            'dann x minus zwei — der Graph folgt, die anderen Nullstellen bleiben stehen.',
            f(r'f(x) = \fa{0.5}\,(x + 2)(x - 1)(x \fb{- x_3})', 300, 50),
            n('jeder Faktor gehört|zu genau einer Nullstelle', 440, 'orange'),
            graf(W1, [poly([[3.6, 0.5, -2, 1, 3], [5.6, 0.5, -2, 1, 4], [5.9, 0.5, -2, 1, 4], [7.4, 0.5, -2, 1, 2]],
                           nullstellen={'farbe': 2})])),
         sz('a streckt',
            'Und der Faktor vorne? Er streckt den Graphen in y-Richtung: Eins macht ihn doppelt so hoch, '
            'minus null Komma fünf spiegelt ihn an der x-Achse. Die Nullstellen bleiben, wo sie sind. '
            'Ausmultipliziert ist dieser Faktor der Leitkoeffizient.',
            f(r'f(x) = \fa{a}\,(x + 2)(x - 1)(x - 3)', 300, 52),
            n('@\\fa{a}@ ändert die Höhe, nicht die Nullstellen|@\\fa{a}@ = Leitkoeffizient', 440, 'blau', ein=8.1),
            graf(W1, [poly([[3.9, 0.5, -2, 1, 3], [5.3, 1, -2, 1, 3], [5.5, 1, -2, 1, 3], [7.6, -0.5, -2, 1, 3]],
                           nullstellen={'farbe': 2, 'beschriftung': False})])),
         sz('Gleichung aus Nullstellen',
            'Umgekehrt geht es auch: Gesucht ist ein Polynom dritten Grades mit den Nullstellen minus zwei, eins und drei, '
            'das durch null, sechs geht. Ansatz mit den drei Linearfaktoren, dann x gleich null einsetzen: '
            'sechs a gleich sechs, also a gleich eins.',
            f(r'f(x) = \fa{a}\,(x+2)(x-1)(x-3)', 300, 50),
            f(r'f(0) = \fa{a} \cdot 2 \cdot (-1) \cdot (-3) = 6\fa{a} = 6', 400, 46, ein=8.4),
            n('@\\Rightarrow \\fa{a} = 1@', 500, 'blau', 52, ein=13.4),
            # mit a = 0.5 beginnen: (0 | 3) statt (0 | 6). «sechs a gleich sechs, also a gleich eins»
            # (12.1–14.3 s): a 0.5 → 1, die Kurve läuft in den Punkt (f(0) = 6a, monoton 3 → 6)
            graf(W1, [poly([[12.1, 0.5, -2, 1, 3], [14.3, 1, -2, 1, 3]],
                           nullstellen={'farbe': 2, 'beschriftung': False})], ein=1.8,
                 punkte=[pt(0, 6, 5, '(0 | 6)', [0.35, 6.9])])),
         sz('Merke',
            'Zum Mitnehmen: Grad ist der höchste Exponent, der Leitkoeffizient sein Faktor. In der Produktform '
            'stehen die Nullstellen in den Linearfaktoren, mit umgekehrtem Vorzeichen. Der Faktor a ist der '
            'Leitkoeffizient und ändert die Nullstellen nicht.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'f(x) = \fa{a}\,(x - \fb{x_1})(x - \fb{x_2})(x - \fb{x_3})', 410, 50, ein=0.4),
            n('Nullstellen @\\fb{x_1},\\ \\fb{x_2},\\ \\fb{x_3}@|@\\fa{a}@ = Leitkoeffizient|ein Punkt mehr bestimmt @\\fa{a}@',
              540, 'blau', 44, ein=1.2),
            graf(W1, [poly([[0] + B1], nullstellen={'farbe': 2})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
WK1 = dict(xbereich=[-5, 6], ybereich=[-12, 12], yteilung=yt(-12, -8, -4, 4, 8, 12))
WK3 = dict(xbereich=[-4, 4], ybereich=[-8, 8], yteilung=yt(-8, -6, -4, -2, 2, 4, 6, 8))
WK4 = dict(xbereich=[-3, 5], ybereich=[-6, 8], yteilung=yt(-6, -4, -2, 2, 4, 6, 8))
clip('kontrolle-linearfaktoren', 'Polynom sehen: Kontrollfragen zu den Linearfaktoren',
     'Fünf Vorhersagen zu Nullstellen, Grad, Leitkoeffizient und dem Faktor a.',
     ['Linearfaktor', 'Nullstelle', 'Grad', 'Leitkoeffizient', 'Kontrollfragen'], [
         sz('Frage 1',
            'Jede Klammer wird bei der Zahl null, die mit umgekehrtem Vorzeichen in ihr steht: vier, minus eins und minus drei.',
            f(r'f(x) = \fa{0.5}\,(x \fb{- 4})(x \fb{+ 1})(x \fb{+ 3})', 300, 50, ein=1.0),
            n('Nullstellen @\\fb{4},\\ \\fb{-1},\\ \\fb{-3}@', 440, 'orange', ein=2.4),
            graf(WK1, [poly([[0, 0.5, 4, -1, -3]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Frage 2',
            'Zwei Linearfaktoren, also Grad zwei. Ausmultipliziert beginnt der Term mit minus drei x Quadrat — '
            'der Leitkoeffizient ist minus drei.',
            f(r'-3\,(x-1)(x+2) = \fa{-3}x^2 - 3x + 6', 300, 50, ein=1.0),
            n('Grad @2@, Leitkoeffizient @\\fa{-3}@', 440, 'blau', ein=2.4),
            graf(W2, [poly([[0, -3, 1, -2]], nullstellen={'farbe': 2, 'beschriftung': False})], ein=1.2)),
         sz('Frage 3',
            'x plus drei wird null bei minus drei. Dort schneidet der Graph die x-Achse.',
            f(r'x \fb{+ 3} = 0 \;\Rightarrow\; x = \fb{-3}', 300, 56, ein=1.0),
            n('Klammer null setzen —|nicht die Zahl abschreiben', 440, 'orange', ein=2.4),
            # Ohne Nullstellen-Punkte: Sie zeigten die Antwort, bevor gefragt ist (§15).
            graf(WK3, [poly([[0, -0.5, -3, 1, 2]])])),
         sz('Frage 4',
            'Ansatz mit den drei Linearfaktoren, dann x gleich null: a mal eins mal minus zwei mal minus vier '
            'ist acht a. Acht a gleich vier gibt a gleich null Komma fünf.',
            f(r'f(0) = \fa{a} \cdot 1 \cdot (-2) \cdot (-4) = 8\fa{a} = 4', 300, 46, ein=1.0),
            n('@\\Rightarrow \\fa{a} = 0.5@', 440, 'blau', 52, ein=3.0),
            graf(WK4, [poly([[0, 0.5, -1, 2, 4]], nullstellen={'farbe': 2, 'beschriftung': False})], ein=3.0,
                 punkte=[pt(0, 4, 5, '(0 | 4)', [0.3, 4.9])])),
         sz('Frage 5',
            'a streckt nur in y-Richtung. Wo ein Faktor null ist, bleibt das Produkt null — egal, wie gross a ist. '
            'Die Nullstellen bleiben also stehen.',
            f(r'\fa{a} \cdot 0 = 0', 300, 66, ein=1.0),
            n('@\\fa{a}@ streckt —|die Nullstellen bleiben', 440, 'blau', ein=2.4),
            graf(W1, [poly([[0.4, 0.5, -2, 1, 3], [2.6, 1, -2, 1, 3], [4.8, -0.5, -2, 1, 3]],
                           nullstellen={'farbe': 2, 'beschriftung': False})])),
         sz('Merke',
            'Zum Mitnehmen: Die Nullstellen stehen in den Linearfaktoren, mit umgekehrtem Vorzeichen. Die Anzahl '
            'der Faktoren ist der Grad, der Faktor vorne der Leitkoeffizient. Einen Punkt braucht es, um ihn zu bestimmen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'(x \fb{+ 3}) \;\to\; x = \fb{-3}', 410, 58, ein=0.4),
            n('Anzahl Faktoren = Grad|Faktor vorne = Leitkoeffizient|ein Punkt bestimmt @\\fa{a}@',
              540, 'blau', 44, ein=1.2),
            graf(W1, [poly([[0] + B1], nullstellen={'farbe': 2})])),
     ], [
         wahl('Frage 1', 'f(x) = 0.5(x − 4)(x + 1)(x + 3): Welche Nullstellen hat f?',
              ['4, −1 und −3', '−4, 1 und 3', '0.5, 4, −1 und −3'], 0,
              {0: 'Ja.',
               1: 'Setz x = −4 in die erste Klammer ein: Wird sie null?',
               2: 'Der Faktor 0.5 wird nie null. Nur die Klammern liefern Nullstellen.'},
              sprich='f von x gleich null Komma fünf, mal x minus vier, mal x plus eins, mal x plus drei: Welche Nullstellen hat f?',
              rueck_sprich={1: 'Setz x gleich minus vier in die erste Klammer ein: Wird sie null?',
                            2: 'Der Faktor null Komma fünf wird nie null. Nur die Klammern liefern Nullstellen.'}),
         wahl('Frage 2', 'f(x) = −3(x − 1)(x + 2): Grad und Leitkoeffizient?',
              ['Grad 2, Leitkoeffizient −3', 'Grad 3, Leitkoeffizient −3', 'Grad 2, Leitkoeffizient 1'], 0,
              {0: 'Ja.',
               1: 'Zähl die Klammern mit x: Wie oft wird x mit x multipliziert?',
               2: 'Welcher Faktor steht vor den Klammern?'},
              sprich='f von x gleich minus drei, mal x minus eins, mal x plus zwei: Grad und Leitkoeffizient?',
              rueck_sprich={1: 'Zähl die Klammern mit x: Wie oft wird x mit x multipliziert?',
                            2: 'Welcher Faktor steht vor den Klammern?'}),
         klick('Frage 3', 'f(x) = −0.5(x + 3)(x − 1)(x − 2): Tipp die Nullstelle des Faktors (x + 3) ins Bild.',
               [-3, 0], 'Getroffen: (−3 | 0).',
               [{'bei': [3, 0], 'text': 'Vorzeichen: Bei welchem x wird x + 3 null?',
                 'sprich': 'Vorzeichen: Bei welchem x wird x plus drei null?'},
                {'bei': [1, 0], 'text': 'Das ist die Nullstelle des Faktors (x − 1).',
                 'sprich': 'Das ist die Nullstelle des Faktors x minus eins.'},
                {'bei': [2, 0], 'text': 'Das ist die Nullstelle des Faktors (x − 2).',
                 'sprich': 'Das ist die Nullstelle des Faktors x minus zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — setz x + 3 = 0.',
               sprich='f von x gleich minus null Komma fünf, mal x plus drei, mal x minus eins, mal x minus zwei: '
                      'Tipp die Nullstelle des Faktors x plus drei ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Setz x plus drei gleich null.'),
         wahl('Frage 4', 'Nullstellen −1, 2 und 4, und f(0) = 4. Wie gross ist a in f(x) = a(x + 1)(x − 2)(x − 4)?',
              ['a = 0.5', 'a = 2', 'a = −0.5'], 0,
              {0: 'Ja.',
               1: 'Rechne f(0) = a · 1 · (−2) · (−4) aus und setz es gleich 4.',
               2: 'Zähl die Minuszeichen: (−2) · (−4) ist positiv.'},
              sprich='Nullstellen minus eins, zwei und vier, und f von null gleich vier. '
                     'Wie gross ist a in f von x gleich a mal x plus eins, mal x minus zwei, mal x minus vier?',
              rueck_sprich={1: 'Rechne f von null gleich a mal eins mal minus zwei mal minus vier aus, und setz es gleich vier.',
                            2: 'Zähl die Minuszeichen: minus zwei mal minus vier ist positiv.'}),
         wahl('Frage 5', 'Was geschieht mit den Nullstellen, wenn man a verdoppelt?',
              ['Sie bleiben, wo sie sind.', 'Sie rücken doppelt so weit nach aussen.', 'Sie halbieren sich.'], 0,
              {0: 'Ja.',
               1: 'Setz eine Nullstelle ein: Ist das Produkt mit doppeltem a noch null?',
               2: 'a steht vor den Klammern, nicht in ihnen. Welche Klammer ändert sich?'},
              sprich='Was geschieht mit den Nullstellen, wenn man a verdoppelt?',
              rueck_sprich={1: 'Setz eine Nullstelle ein: Ist das Produkt mit doppeltem a noch null?',
                            2: 'a steht vor den Klammern, nicht in ihnen. Welche Klammer ändert sich?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# Beispiel: f(x) = 0.5(x+2)(x−1)² — Startwert der Simulation 2.
clip('vielfachheit', 'Polynom sehen: mehrfache Nullstellen',
     'Was geschieht, wenn Nullstellen zusammenfallen: schneiden, berühren, Terrassenpunkt.',
     ['Vielfachheit', 'doppelte Nullstelle', 'dreifache Nullstelle', 'Terrassenpunkt', 'Vorzeichenwechsel'], [
         sz('Drei einfache',
            'Wieder null Komma fünf mal Klammer x plus zwei, mal x minus eins, mal x minus drei. An jeder der drei '
            'Nullstellen schneidet der Graph die x-Achse: Das Vorzeichen wechselt.',
            titel('Schneiden', 280, 80),
            f(r'f(x) = \fa{0.5}\,(x+2)(x-1)(x-3)', 430, 50, ein=1.0),
            graf(W1, [poly([[0] + B1], nullstellen={'farbe': 2})], ein=3.0)),
         sz('Doppelt',
            'Jetzt rückt die Nullstelle drei nach links, bis auf die eins. Zwei gleiche Faktoren: Klammer x minus eins '
            'im Quadrat. Der Graph schneidet dort nicht mehr — er berührt die x-Achse und kehrt um.',
            f(r'f(x) = \fa{0.5}\,(x+2)(x \fb{- 1})^{\fb{2}}', 300, 52, ein=3.5),
            n('doppelte Nullstelle:|berühren, kein Vorzeichenwechsel', 440, 'orange', ein=5.1),
            graf(W1, [poly([[0.5, 0.5, -2, 1, 3], [3.3, 0.5, -2, 1, 1]], nullstellen={'farbe': 2})])),
         sz('Warum kein Wechsel',
            'Warum? Ein Quadrat ist nie negativ. Links und rechts von der eins hat Klammer x minus eins im Quadrat '
            'dasselbe Vorzeichen, nämlich plus, und auch x plus zwei bleibt dort positiv. Darum hat f auf beiden Seiten '
            'dasselbe Vorzeichen, und der Graph bleibt auf derselben Seite.',
            f(r'(x - 1)^2 \geq 0', 300, 66),
            n('@f(0)@ und @f(2)@:|beide positiv', 440, 'orange', ein=10.5),
            graf(W1, [poly([[0, 0.5, -2, 1, 1]], nullstellen={'farbe': 2},
                           marken=[{'x': 0, 'text': '(0 | {y})', 'farbe': 5}, {'x': 2, 'text': '(2 | {y})', 'farbe': 5}])],
                 ein=2.9)),
         sz('Dreifach',
            'Und wenn auch die minus zwei auf die eins rückt? Klammer x minus eins hoch drei. Der Graph schneidet '
            'wieder, wird aber an der Stelle ganz flach: ein Terrassenpunkt.',
            f(r'f(x) = \fa{0.5}\,(x \fb{- 1})^{\fb{3}}', 300, 56, ein=3.6),
            n('dreifache Nullstelle:|schneiden mit Terrasse', 440, 'orange', ein=4.8),
            graf(W1, [poly([[0.5, 0.5, -2, 1, 1], [3.6, 0.5, 1, 1, 1]], nullstellen={'farbe': 2})])),
         sz('Vielfachheit',
            'Der Exponent eines Linearfaktors heisst Vielfachheit der Nullstelle. Ungerade Vielfachheit: Der Graph '
            'wechselt die Seite. Gerade Vielfachheit: Er berührt nur.',
            f(r'(x - \fb{x_1})^{\fb{k}}', 300, 66),
            n('@\\fb{k}@ ungerade: schneiden|@\\fb{k}@ gerade: berühren|@\\fb{k} = 3@: mit Terrasse', 440, 'orange', ein=3.0),
            graf(W1, [poly([[0, 0.5, -2, 1, 1]], nullstellen={'farbe': 2})])),
         sz('Vom Graphen zur Gleichung',
            'So liest man eine Gleichung am Graphen ab. Hier berührt er bei minus eins, also doppelt, und schneidet '
            'bei zwei, also einfach. Ansatz: a mal Klammer x plus eins im Quadrat, mal x minus zwei. Der Graph geht '
            'durch null, minus zwei: minus zwei a gleich minus zwei, also a gleich eins.',
            f(r'f(x) = \fa{a}\,(x \fb{+ 1})^{\fb{2}}(x \fb{- 2})', 300, 50, ein=7.0),
            f(r'f(0) = \fa{a} \cdot 1 \cdot (-2) = -2 \;\Rightarrow\; \fa{a} = 1', 400, 44, ein=13.8),
            n('Vielfachheiten @2 + 1 = 3@ = Grad', 500, 'orange', 44, ein=15.8),
            graf(W2, [poly([[0, 1, -1, -1, 2]], nullstellen={'farbe': 2})],
                 punkte=[pt(0, -2, 5, '(0 | −2)', [0.3, -2.9])])),
         sz('Merke',
            'Zum Mitnehmen: Einfache Nullstelle: schneiden. Doppelte: berühren, ohne Vorzeichenwechsel. Dreifache: '
            'schneiden mit Terrasse. Die Vielfachheiten zusammen ergeben höchstens den Grad.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'(x - \fb{x_1})^{\fb{1}},\ (x - \fb{x_1})^{\fb{2}},\ (x - \fb{x_1})^{\fb{3}}', 410, 46, ein=0.4),
            n('schneiden; berühren; Terrasse|gerade Vielfachheit: kein Vorzeichenwechsel',
              540, 'blau', 44, ein=1.2),
            # im Takt der Satzteile: «Einfache» (1.5 s) drei Nullstellen, «Doppelte: berühren» (3.3–4.9 s)
            # 3 → 1, «Dreifache: … Terrasse» (5.8–7.4 s) −2 → 1
            graf(W1, [poly([[3.3] + B1, [4.9, 0.5, -2, 1, 1], [5.8, 0.5, -2, 1, 1], [7.4, 0.5, 1, 1, 1]],
                           nullstellen={'farbe': 2})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
WV = dict(xbereich=[-3, 4], ybereich=[-6, 6], yteilung=yt(-6, -4, -2, 2, 4, 6))
clip('kontrolle-vielfachheit', 'Polynom sehen: Kontrollfragen zu mehrfachen Nullstellen',
     'Fünf Vorhersagen: schneiden oder berühren, Terrassenpunkt, Gleichung zum Graphen.',
     ['Vielfachheit', 'doppelte Nullstelle', 'Terrassenpunkt', 'Kontrollfragen'], [
         sz('Frage 1',
            'Klammer x minus zwei steht im Quadrat: doppelte Nullstelle. Bei zwei berührt der Graph die x-Achse '
            'und kehrt um — bei minus eins schneidet er.',
            f(r'f(x) = (x \fb{- 2})^{\fb{2}}(x + 1)', 300, 56, ein=1.0),
            n('gerade Vielfachheit:|berühren', 440, 'orange', ein=2.4),
            graf(WV, [poly([[0, 1, 2, 2, -1]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Frage 2',
            'Hoch drei: dreifache Nullstelle. Der Graph wechselt die Seite, wird bei minus eins aber flach — ein Terrassenpunkt.',
            f(r'f(x) = (x \fb{+ 1})^{\fb{3}}', 300, 62, ein=1.0),
            n('ungerade Vielfachheit, @\\fb{3}@:|schneiden mit Terrasse', 440, 'orange', ein=2.4),
            graf(WV, [poly([[0, 1, -1, -1, -1]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Frage 3',
            'Bei eins steht der Faktor im Quadrat. Dort berührt der Graph die x-Achse; bei minus zwei schneidet er sie.',
            f(r'f(x) = -(x+2)(x \fb{- 1})^{\fb{2}}', 300, 56, ein=1.0),
            n('berühren bei @\\fb{1}@|schneiden bei @-2@', 440, 'orange', ein=2.4),
            graf(WV, [poly([[0, -1, -2, 1, 1]])])),
         sz('Frage 4',
            'Berühren bei drei heisst Klammer x minus drei im Quadrat, schneiden bei minus eins heisst x plus eins einfach. '
            'Rechts geht der Graph nach oben, a ist also positiv.',
            f(r'f(x) = \fa{0.5}\,(x \fb{+ 1})(x \fb{- 3})^{\fb{2}}', 300, 50, ein=1.6),
            n('berühren → Quadrat|schneiden → einfach', 440, 'orange', ein=3.0),
            graf(dict(xbereich=[-3, 5], ybereich=[-6, 6], yteilung=yt(-6, -4, -2, 2, 4, 6)),
                 [poly([[0, 0.5, -1, 3, 3]])])),
         sz('Frage 5',
            'Zwei Nullstellen, die beide berühren, sind beide doppelt: zwei plus zwei gibt vier, genau der Grad. '
            'Etwa x Quadrat mal Klammer x minus zwei im Quadrat.',
            f(r'x^{\fb{2}}\,(x - 2)^{\fb{2}}', 300, 62, ein=1.0),
            n('@\\fb{2} + \\fb{2} = 4@ = Grad', 440, 'orange', ein=2.4),
            graf(dict(xbereich=[-2, 4], ybereich=[-3, 5], yteilung=yt(-2, 2, 4)),
                 [poly([[0, 1, 0, 0, 2, 2]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Am Graphen zeigt sich die Vielfachheit. Schneiden heisst ungerade, berühren gerade, '
            'Terrasse dreifach. Und die Summe der Vielfachheiten ist höchstens der Grad.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\text{berühren} \;\Rightarrow\; (x - \fb{x_1})^{\fb{2}}', 410, 50, ein=0.4),
            n('schneiden: ungerade|berühren: gerade|Summe der Vielfachheiten @\\leq@ Grad',
              540, 'blau', 44, ein=1.2),
            graf(W2, [poly([[0, 1, -1, -1, 2]], nullstellen={'farbe': 2})])),
     ], [
         wahl('Frage 1', 'f(x) = (x − 2)²(x + 1): Was tut der Graph bei x = 2?',
              ['Er berührt die x-Achse.', 'Er schneidet die x-Achse.', 'Er schneidet mit einer Terrasse.'], 0,
              {0: 'Ja.',
               1: 'Schau auf den Exponenten der Klammer (x − 2): gerade oder ungerade?',
               2: 'Eine Terrasse gibt es bei der Vielfachheit 3. Welcher Exponent steht hier?'},
              sprich='f von x gleich x minus zwei im Quadrat, mal x plus eins: Was tut der Graph bei x gleich zwei?',
              rueck_sprich={1: 'Schau auf den Exponenten der Klammer x minus zwei: gerade oder ungerade?',
                            2: 'Eine Terrasse gibt es bei der Vielfachheit drei. Welcher Exponent steht hier?'}),
         wahl('Frage 2', 'f(x) = (x + 1)³: Was tut der Graph bei x = −1?',
              ['Er schneidet und ist dort flach (Terrassenpunkt).', 'Er berührt nur.', 'Er schneidet steil, ohne abzuflachen.'], 0,
              {0: 'Ja.',
               1: 'Ist 3 gerade? Wechselt (x + 1)³ das Vorzeichen bei −1?',
               2: 'Bei einfacher Nullstelle ja — hier ist sie dreifach.'},
              sprich='f von x gleich x plus eins hoch drei: Was tut der Graph bei x gleich minus eins?',
              rueck_sprich={1: 'Ist drei gerade? Wechselt x plus eins hoch drei das Vorzeichen bei minus eins?',
                            2: 'Bei einfacher Nullstelle ja. Hier ist sie dreifach.'}),
         klick('Frage 3', 'f(x) = −(x + 2)(x − 1)²: Tipp die Stelle, an der der Graph die x-Achse nur berührt.',
               [1, 0], 'Getroffen: (1 | 0).',
               [{'bei': [-2, 0], 'text': 'Dort schneidet er: Der Faktor (x + 2) ist einfach.',
                 'sprich': 'Dort schneidet er: Der Faktor x plus zwei ist einfach.'},
                {'bei': [-1, 0], 'text': 'Vorzeichen: Bei welchem x wird x − 1 null?',
                 'sprich': 'Vorzeichen: Bei welchem x wird x minus eins null?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — welcher Faktor steht im Quadrat?',
               sprich='f von x gleich minus, x plus zwei, mal x minus eins im Quadrat: '
                      'Tipp die Stelle, an der der Graph die x-Achse nur berührt.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Welcher Faktor steht im Quadrat?'),
         wahl('Frage 4', 'Der Graph schneidet bei −1, berührt bei 3, rechts geht er nach oben. Welche Gleichung passt?',
              ['f(x) = 0.5(x + 1)(x − 3)²', 'f(x) = 0.5(x + 1)²(x − 3)', 'f(x) = −0.5(x + 1)(x − 3)²'], 0,
              {0: 'Ja.',
               1: 'Wo berührt der Graph? Dort gehört das Quadrat hin.',
               2: 'Mit negativem a ginge der Graph rechts nach unten.'},
              sprich='Der Graph schneidet bei minus eins, berührt bei drei, rechts geht er nach oben. Welche Gleichung passt?',
              rueck_sprich={1: 'Wo berührt der Graph? Dort gehört das Quadrat hin.',
                            2: 'Mit negativem a ginge der Graph rechts nach unten.'}),
         wahl('Frage 5', 'Grad 4, nur die Nullstellen 0 und 2, und an beiden berührt der Graph. Welche Vielfachheiten?',
              ['beide doppelt', '0 einfach, 2 dreifach', 'beide einfach'], 0,
              {0: 'Ja.',
               1: 'Bei einfacher und dreifacher Nullstelle schneidet der Graph. Hier berührt er.',
               2: 'Dann käme man nur auf Grad 2 — und der Graph würde schneiden.'},
              sprich='Grad vier, nur die Nullstellen null und zwei, und an beiden berührt der Graph. Welche Vielfachheiten?',
              rueck_sprich={1: 'Bei einfacher und dreifacher Nullstelle schneidet der Graph. Hier berührt er.',
                            2: 'Dann käme man nur auf Grad zwei, und der Graph würde schneiden.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Beispiel: f(x) = x³ − 4x = x(x+2)(x−2), der Leitterm x³ gestrichelt — Startwert der Simulation 3.
Z1 = dict(xbereich=[-3, 3], ybereich=[-30, 30], yteilung=yt(-20, -10, 10, 20))
Z2 = dict(xbereich=[-6, 6], ybereich=[-240, 240], yteilung=yt(-200, -100, 100, 200), xteilung=yt(-4, -2, 2, 4))
Z3 = dict(xbereich=[-12, 12], ybereich=[-1800, 1800], yteilung=yt(-1500, -1000, -500, 500, 1000, 1500),
          xteilung=yt(-10, -5, 5, 10))
W4 = dict(xbereich=[-3, 3], ybereich=[-3, 3], yteilung=yt(-2, -1, 1, 2), xteilung=yt(-2, -1, 1, 2))
clip('globalverlauf', 'Polynom sehen: der Globalverlauf',
     'Von weitem zählt nur der Leitterm: Grad und Leitkoeffizient bestimmen die Enden, der Grad begrenzt Nullstellen und Extremstellen.',
     ['Globalverlauf', 'Leitterm', 'Grad', 'Leitkoeffizient', 'Symmetrie'], [
         sz('Nah dran',
            'f von x gleich x hoch drei minus vier x, dazu gestrichelt der Leitterm x hoch drei. Nah am Ursprung sind die '
            'beiden deutlich verschieden: f hat drei Nullstellen, x hoch drei nur eine.',
            titel('Nah dran', 280, 80),
            f(r'f(x) = x^3 - 4x', 430, 58, ein=1.0),
            graf(Z1, [fest('x**3'), poly([[0, 1, -2, 0, 2]])], ein=3.0),
            # «f hat drei Nullstellen» (8.4 s), «x hoch drei nur eine» (9.8 s): Ring um (0 | 0)
            ueber(Z1, [pt(-2, 0, 2), pt(0, 0, 2), pt(2, 0, 2)], ein=8.5),
            ueber(Z1, figuren=[{'art': 'kreis', 'm': [0, 0], 'r': 0.28, 'farbe': 5, 'dicke': 3}], ein=9.8)),
         sz('Weiter weg',
            'Jetzt zoomen wir hinaus, bis x gleich sechs. Die beiden Kurven rücken zusammen.',
            f(r'x \in [-6;\, 6]', 300, 62),
            graf(Z2, [fest('x**3'), poly([[0, 1, -2, 0, 2]])], ein=1.0)),
         sz('Ganz weit',
            'Bis x gleich zwölf sind sie kaum noch zu unterscheiden. Für grosse x ist minus vier x neben x hoch drei '
            'bedeutungslos. Von weitem zählt nur der Leitterm.',
            f(r'x \in [-12;\, 12]', 300, 62),
            n('von weitem zählt|nur der Leitterm @\\fa{a_n x^n}@', 440, 'blau', ein=4.0),
            graf(Z3, [fest('x**3'), poly([[0, 1, -2, 0, 2]])], ein=1.0)),
         sz('Ungerader Grad',
            'Ungerader Grad: Die Enden zeigen in entgegengesetzte Richtungen. Bei positivem Leitkoeffizienten von '
            'links unten nach rechts oben, bei negativem umgekehrt.',
            f(r'n \text{ ungerade}', 300, 62),
            n('@\\fa{a_n} \\gt 0@: links unten → rechts oben|@\\fa{a_n} \\lt 0@: links oben → rechts unten', 440, 'blau', ein=2.0),
            graf(W4, [poly([[0, 0.5, -2, 0, 2], [8.0, 0.5, -2, 0, 2], [9.4, -0.5, -2, 0, 2]])])),
         sz('Gerader Grad',
            'Gerader Grad: Beide Enden zeigen in dieselbe Richtung. Positiver Leitkoeffizient: beide nach oben. '
            'Negativer: beide nach unten.',
            f(r'n \text{ gerade}', 300, 62),
            n('@\\fa{a_n} \\gt 0@: beide Enden oben|@\\fa{a_n} \\lt 0@: beide Enden unten', 440, 'blau', ein=2.0),
            graf(W4, [poly([[0, 0.25, -2, -1, 1, 2], [6.4, 0.25, -2, -1, 1, 2], [7.9, -0.25, -2, -1, 1, 2]])])),
         sz('Höchstens',
            'Grad vier heisst: höchstens vier Nullstellen und höchstens drei Hoch- und Tiefpunkte. Hier sind es '
            'genau so viele. Allgemein: höchstens n Nullstellen und höchstens n minus eins Extremstellen.',
            f(r'\le n \text{ Nullstellen}', 300, 52),
            f(r'\le n-1 \text{ Extremstellen}', 390, 52),
            n('Grad @4@: hier @4@ Nullstellen,|@3@ Extremstellen', 500, 'blau', ein=5.0),
            graf(W4, [poly([[0, 0.25, -2, -1, 1, 2]], nullstellen={'farbe': 2, 'beschriftung': False},
                           extrema={'farbe': 3, 'beschriftung': False})], ein=1.0)),
         sz('Nur höchstens',
            'Aber nur höchstens: x Quadrat plus eins hat Grad zwei und gar keine Nullstelle. Bei ungeradem Grad '
            'dagegen gibt es immer mindestens eine — die Enden liegen auf verschiedenen Seiten der x-Achse.',
            f(r'x^2 + 1 \;\text{— keine Nullstelle}', 300, 50),
            n('Grad ungerade:|mindestens eine Nullstelle', 440, 'blau', ein=5.2),
            graf(W4, [fest('x**2+1', farbe=4, gestrichelt=False)], ein=1.0),
            # «Bei ungeradem Grad dagegen … mindestens eine» (5.3 s): eine kubische Kurve dazu
            ueber(W4, [pt(-1, 0, 2, '(−1 | 0)', [-1.15, 0.35], 'end')],
                  kurven=[dict(fest('x**3+1', farbe=1, gestrichelt=False),
                               beschriftung='x³ + 1', beschriftung_bei=[-1.0, -1.6])], ein=5.3)),
         sz('Symmetrie',
            'Und die Symmetrie? Nur ungerade Exponenten, wie bei x hoch drei minus vier x: punktsymmetrisch zum Ursprung. '
            'Nur gerade Exponenten: achsensymmetrisch zur y-Achse. Das konstante Glied zählt dabei als gerade. Gemischt: keine dieser Symmetrien.',
            f(r'x^{3} - 4x^{1} \;\to\; \text{punktsymmetrisch}', 300, 46),
            n('nur gerade Exponenten: @y@-Achse|nur ungerade: Ursprung|gemischt: keine der beiden', 440, 'blau', ein=7.0),
            # «Gemischt: keine dieser Symmetrien» (12.5–14.0 s): konstantes Glied 0 → 1 wie Regler d in sim3,
            # 0.5x³ − 2x + 1 hat die Nullstellen −2.214, 0.539, 1.675 (numpy); dazwischen bleibt x² weg
            graf(W4, [poly([[12.5, 0.5, -2, 0, 2], [14.0, 0.5, -2.2143, 0.5392, 1.6751]])], ein=1.0),
            # «Nur gerade Exponenten: achsensymmetrisch zur y-Achse» (6.8 s): eine gerade Quartik gestrichelt
            ueber(W4, kurven=[dict(fest('0.25*(x**2-1)*(x**2-4)'), beschriftung='nur gerade',
                                   beschriftung_bei=[-1.75, -1.4])], ein=6.8)),
         sz('Merke',
            'Zum Mitnehmen: Von weitem zählt nur der Leitterm. Grad gerade: Enden gleich, ungerade: Enden '
            'entgegengesetzt, der Leitkoeffizient sagt, wohin. Höchstens n Nullstellen, höchstens n minus eins Extremstellen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\fa{a_n} x^n + \dots \;\approx\; \fa{a_n} x^n \text{ für grosse } |x|', 410, 46, ein=0.4),
            n('gerade: Enden gleich; ungerade: entgegengesetzt|@\\le n@ Nullstellen, @\\le n-1@ Extremstellen',
              540, 'blau', 44, ein=1.2),
            graf(W4, [poly([[0, 0.25, -2, -1, 1, 2]])])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-globalverlauf', 'Polynom sehen: Kontrollfragen zum Globalverlauf',
     'Fünf Vorhersagen zu Enden, Höchstzahlen und Symmetrie.',
     ['Globalverlauf', 'Leitkoeffizient', 'Symmetrie', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der Leitterm ist minus x hoch vier: gerader Grad, negativer Leitkoeffizient. Beide Enden zeigen nach unten.',
            f(r'f(x) = \fa{-x^4} + 3x', 300, 60, ein=1.0),
            n('gerade, @\\fa{a_n} \\lt 0@:|beide Enden unten', 440, 'blau', ein=2.4),
            graf(W4, [fest('-x**4+3*x', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 2',
            'Grad fünf: höchstens fünf minus eins, also vier Extremstellen.',
            f(r'n - 1 = 5 - 1 = 4', 300, 62, ein=1.0),
            n('höchstens @n - 1@ Extremstellen', 440, 'blau', ein=2.4),
            graf(W4, [poly([[0, 0.1, -2.5, -1.5, 0, 1.5, 2.5]], extrema={'farbe': 3, 'beschriftung': False})], ein=1.2)),
         sz('Frage 3',
            'Beide Enden zeigen nach oben: Der Grad ist gerade, der Leitkoeffizient positiv.',
            f(r'\text{beide Enden oben}', 300, 56, ein=1.4),
            n('@\\Rightarrow@ Grad gerade, @\\fa{a_n} \\gt 0@', 440, 'blau', ein=2.8),
            graf(W4, [poly([[0, 0.5, -2, -0.5, 1, 2]])])),
         sz('Frage 4',
            'Exponenten vier und zwei, und die Konstante drei zählt als x hoch null — alles gerade. '
            'Darum ist der Graph achsensymmetrisch zur y-Achse.',
            f(r'2x^{4} - x^{2} + 3x^{0}', 300, 58, ein=1.0),
            n('nur gerade Exponenten:|achsensymmetrisch zur @y@-Achse', 440, 'blau', ein=2.4),
            # Minimum 2.875 — das Fenster muss hoch genug reichen, sonst sieht man nichts.
            graf(dict(xbereich=[-3, 3], ybereich=[-1, 7], yteilung=yt(2, 4, 6), xteilung=yt(-2, -1, 1, 2)),
                 [fest('2*x**4-x**2+3', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 5',
            'x hoch drei und x sind ungerade, das konstante Glied eins zählt als gerade. Gemischt: weder '
            'achsensymmetrisch zur y-Achse noch punktsymmetrisch zum Ursprung.',
            f(r'x^{3} + x^{1} + 1 \cdot x^{0}', 300, 54, ein=1.0),
            n('gemischt: weder zur @y@-Achse|noch zum Ursprung symmetrisch', 440, 'rot', ein=2.4),
            graf(W4, [fest('x**3+x+1', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Der Leitterm bestimmt die Enden, der Grad die Höchstzahlen. Und die Symmetrie liest man an den Exponenten ab — die Konstante zählt mit.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\text{Enden: } \fa{a_n} x^n', 410, 58, ein=0.4),
            n('@\\le n@ Nullstellen; @\\le n - 1@ Extremstellen|Konstante = gerader Exponent',
              540, 'blau', 44, ein=1.2),
            graf(W4, [poly([[0, 0.5, -2, 0, 2]])])),
     ], [
         wahl('Frage 1', 'f(x) = −x⁴ + 3x: Wohin zeigen die Enden des Graphen?',
              ['beide nach unten', 'beide nach oben', 'links oben, rechts unten'], 0,
              {0: 'Ja.',
               1: 'Schau auf das Vorzeichen des Leitkoeffizienten.',
               2: 'Bei geradem Grad zeigen die Enden in dieselbe Richtung.'},
              sprich='f von x gleich minus x hoch vier plus drei x: Wohin zeigen die Enden des Graphen?',
              rueck_sprich={1: 'Schau auf das Vorzeichen des Leitkoeffizienten.',
                            2: 'Bei geradem Grad zeigen die Enden in dieselbe Richtung.'}),
         wahl('Frage 2', 'Eine Polynomfunktion hat Grad 5. Wie viele lokale Extremstellen hat sie höchstens?',
              ['4', '5', '6'], 0,
              {0: 'Ja.',
               1: 'Fünf ist die Höchstzahl der Nullstellen. Bei den Extremstellen ist es eine weniger.',
               2: 'Es sind weniger als der Grad, nicht mehr.'},
              sprich='Eine Polynomfunktion hat Grad fünf. Wie viele lokale Extremstellen hat sie höchstens?',
              rueck_sprich={1: 'Fünf ist die Höchstzahl der Nullstellen. Bei den Extremstellen ist es eine weniger.',
                            2: 'Es sind weniger als der Grad, nicht mehr.'}),
         wahl('Frage 3', 'Was verrät der Graph im Bild über Grad und Leitkoeffizient?',
              ['Grad gerade, Leitkoeffizient positiv', 'Grad ungerade, Leitkoeffizient positiv',
               'Grad gerade, Leitkoeffizient negativ'], 0,
              {0: 'Ja.',
               1: 'Bei ungeradem Grad zeigten die Enden in verschiedene Richtungen.',
               2: 'Negativ hiesse: beide Enden unten.'},
              sprich='Was verrät der Graph im Bild über Grad und Leitkoeffizient?',
              rueck_sprich={1: 'Bei ungeradem Grad zeigten die Enden in verschiedene Richtungen.',
                            2: 'Negativ hiesse: beide Enden unten.'}),
         wahl('Frage 4', 'f(x) = 2x⁴ − x² + 3: Welche Symmetrie hat der Graph?',
              ['achsensymmetrisch zur y-Achse', 'punktsymmetrisch zum Ursprung', 'keine dieser Symmetrien'], 0,
              {0: 'Ja.',
               1: 'Punktsymmetrie braucht nur ungerade Exponenten. Welche Exponenten stehen hier?',
               2: 'Die 3 ist 3 · x⁰ — und 0 ist gerade.'},
              sprich='f von x gleich zwei x hoch vier minus x Quadrat plus drei: Welche Symmetrie hat der Graph?',
              rueck_sprich={1: 'Punktsymmetrie braucht nur ungerade Exponenten. Welche Exponenten stehen hier?',
                            2: 'Die drei ist drei mal x hoch null. Und null ist gerade.'}),
         wahl('Frage 5', 'f(x) = x³ + x + 1: Welche Symmetrie hat der Graph?',
              ['keine dieser Symmetrien', 'punktsymmetrisch zum Ursprung', 'achsensymmetrisch zur y-Achse'], 0,
              {0: 'Ja.',
               1: 'Fast — aber die 1 ist ein Glied mit geradem Exponenten.',
               2: 'Es kommen ungerade Exponenten vor.'},
              sprich='f von x gleich x hoch drei plus x plus eins: Welche Symmetrie hat der Graph?',
              rueck_sprich={1: 'Fast. Aber die eins ist ein Glied mit geradem Exponenten.',
                            2: 'Es kommen ungerade Exponenten vor.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# Beispiel: x³ − 9x (Ausklammern) und x³ − 2x² − 5x + 6 (Raten, Abspalten) — beide wie auf
# der Themenseite; das zweite ist das Polynom aus Kapitel 1, ohne die Faktoren.
W9 = dict(xbereich=[-4, 4], ybereich=[-12, 12], yteilung=yt(-12, -8, -4, 4, 8, 12))
WD = dict(xbereich=[-3, 4], ybereich=[-8, 10], yteilung=yt(-8, -6, -4, -2, 2, 4, 6, 8, 10))
clip('nullstellen-berechnen', 'Polynom sehen: Nullstellen berechnen',
     'Ausklammern, eine Nullstelle raten, einen Linearfaktor mit Ansatz und Koeffizientenvergleich abspalten — bis die Produktform dasteht.',
     ['Nullstelle', 'Ausklammern', 'Satz vom Nullprodukt', 'Koeffizientenvergleich', 'Linearfaktor'], [
         sz('Ausklammern',
            'Meist ist die Summenform gegeben. Fehlt das konstante Glied, klammert man x aus: x hoch drei minus neun x '
            'ist x mal Klammer x Quadrat minus neun, und das ist x mal x minus drei mal x plus drei.',
            titel('Ausklammern', 280, 80),
            f(r'x^3 - 9x = x\,(x^2 - 9) = x\,(x \fb{- 3})(x \fb{+ 3})', 430, 44, ein=4.0),
            graf(W9, [poly([[0, 1, -3, 0, 3]])], ein=1.0)),
         sz('Nullprodukt',
            'Nach dem Satz vom Nullprodukt sind die Nullstellen null, drei und minus drei. Nicht durch x teilen — '
            'sonst geht die Nullstelle null verloren.',
            f(r'x_1 = \fb{0},\ x_2 = \fb{3},\ x_3 = \fb{-3}', 300, 52),
            n('nie durch @x@ teilen:|@x = 0@ ginge verloren', 440, 'rot', ein=5.0),
            graf(W9, [poly([[0, 1, -3, 0, 3]], nullstellen={'farbe': 2})], ein=1.0)),
         sz('Raten',
            'Bei x hoch drei minus zwei x Quadrat minus fünf x plus sechs geht das nicht. Hier hilft Raten: '
            'Ganzzahlige Nullstellen sind Teiler von sechs. Probe mit eins: eins minus zwei minus fünf plus sechs ist null.',
            f(r'f(x) = x^3 - 2x^2 - 5x + 6', 300, 50),
            f(r'f(\fb{1}) = 1 - 2 - 5 + 6 = 0', 400, 50, ein=10.6),
            n('Kandidaten: Teiler von @6@|@\\pm 1,\\ \\pm 2,\\ \\pm 3,\\ \\pm 6@', 500, 'orange', 44, ein=7.0),
            # Probestelle wie in sim4 (Läufer, seit 07.10.2026): erscheint mit den Kandidaten (7.0 s) bei −1,
            # f(−1) = 8; «Probe mit eins» (9.3 s) fährt sie nach 1, f(1) = 0. Zweite, deckungsgleiche Kurve,
            # weil der Läufer kein eigenes ein hat.
            graf(WD, [poly([[0, 1, 1, 3, -2]]),
                      dict(poly([[0, 1, 1, 3, -2]]), ein=7.0,
                           laeufer={'bahn': [[9.3, -1], [10.5, 1]], 'text': 'f({x}) = {y}', 'farbe': 2})], ein=1.0)),
         sz('Abspalten',
            'Eine Nullstelle liefert einen Linearfaktor: x minus eins. Also ist f gleich Klammer x minus eins, '
            'mal einem quadratischen Quotienten x Quadrat plus p x plus q. Ausmultipliziert gibt das '
            'x hoch drei plus p minus eins mal x Quadrat, plus q minus p mal x, minus q.',
            f(r'f(x) = (x \fb{- 1})(x^2 + px + q)', 300, 46, ein=0.4),
            f(r'= x^3 + (p - 1)\,x^2 + (q - p)\,x - q', 390, 46, ein=10.9),
            graf(WD, [poly([[0, 1, 1, 3, -2]])], ein=1.0,
                 punkte=[pt(1, 0, 2, '(1 | 0)', [1.25, 0.9])])),
         sz('Vergleichen',
            'Jetzt die Koeffizienten vergleichen. Vor x Quadrat: p minus eins gleich minus zwei, also p gleich minus eins. '
            'Am Schluss: minus q gleich sechs, also q gleich minus sechs. Kontrolle beim x: q minus p ist minus fünf, stimmt. '
            'Der Quotient ist x Quadrat minus x minus sechs.',
            f(r'f(x) = x^3 - 2x^2 - 5x + 6', 260, 46, ein=0.3),
            f(r'= x^3 + (p - 1)\,x^2 + (q - p)\,x - q', 335, 46, ein=0.3),
            f(r'p - 1 = -2 \Rightarrow p = -1', 440, 46, ein=3.4),
            f(r'-q = 6 \Rightarrow q = -6', 515, 46, ein=7.7),
            n('Kontrolle: @q - p = -5@ ✓|Quotient @x^2 - x - 6@', 600, 'orange', 44, ein=11.5),
            graf(WD, [poly([[0, 1, 1, 3, -2]])], ein=0.05,
                 punkte=[pt(1, 0, 2, '(1 | 0)', [1.25, 0.9])])),
         sz('Faktorisieren',
            'Der Quotient lässt sich faktorisieren: x minus drei mal x plus zwei. Damit steht die ganze Produktform '
            'da, und mit ihr alle drei Nullstellen: eins, drei und minus zwei.',
            f(r'x^2 - x - 6 = (x \fb{- 3})(x \fb{+ 2})', 300, 48),
            f(r'f(x) = (x \fb{- 1})(x \fb{- 3})(x \fb{+ 2})', 400, 48, ein=4.9),
            graf(WD, [poly([[0, 1, 1, 3, -2]])], ein=0.05),
            graf(WD, [poly([[0, 1, 1, 3, -2]], nullstellen={'farbe': 2})], ein=9.8)),
         sz('Kontrolle',
            'Und die Kontrolle am Graphen: Er schneidet die x-Achse genau dreimal, bei minus zwei, eins und drei. '
            'Mit dem Rechner geht das auch: Wertetabelle oder Gleichungslöser.',
            f(r'\mathbb{L} = \{\fb{-2};\ \fb{1};\ \fb{3}\}', 300, 56),
            n('am Graphen: drei Schnittstellen|mit der @x@-Achse', 440, 'blau', ein=3.0),
            graf(WD, [poly([[0, 1, 1, 3, -2]], nullstellen={'farbe': 2})])),
         sz('Merke',
            'Zum Mitnehmen: Erst ausklammern, wenn es geht. Sonst eine Nullstelle unter den Teilern des konstanten Glieds '
            'raten, den Linearfaktor abspalten, und den quadratischen Quotienten faktorisieren oder mit der Lösungsformel lösen.',
            titel('Zum Mitnehmen', 250, 76),
            n('1  ausklammern|2  Nullstelle raten (Teiler von @a_0@)|3  Linearfaktor abspalten (Ansatz)|4  Quotient lösen',
              400, 'blau', 44, ein=1.2),
            graf(WD, [poly([[0, 1, 1, 3, -2]], nullstellen={'farbe': 2})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
WK4b = dict(xbereich=[-3, 3], ybereich=[-8, 4], yteilung=yt(-8, -6, -4, -2, 2, 4))
clip('kontrolle-nullstellen', 'Polynom sehen: Kontrollfragen zum Nullstellen berechnen',
     'Fünf Vorhersagen zu Ausklammern, Raten und Abspalten.',
     ['Nullstelle', 'Ausklammern', 'Koeffizientenvergleich', 'Kontrollfragen'], [
         sz('Frage 1',
            'x Quadrat ausklammern: x Quadrat mal Klammer x minus vier. Null ist doppelte Nullstelle, vier einfache.',
            f(r'x^3 - 4x^2 = x^{\fb{2}}\,(x \fb{- 4})', 300, 56, ein=1.0),
            n('@\\fb{0}@ doppelt, @\\fb{4}@ einfach', 440, 'orange', ein=2.4),
            graf(dict(xbereich=[-2, 5], ybereich=[-12, 6], yteilung=yt(-12, -8, -4, 4)),
                 [poly([[0, 1, 0, 0, 4]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Frage 2',
            'Probe mit minus eins: minus eins plus eins plus vier minus vier ist null. Minus eins ist eine Nullstelle.',
            f(r'f(\fb{-1}) = -1 + 1 + 4 - 4 = 0', 300, 52, ein=1.0),
            n('Teiler von @-4@ probieren', 440, 'orange', ein=2.4),
            graf(WK4b, [poly([[0, 1, -1, -2, 2]])], ein=1.2)),
         sz('Frage 3',
            'Der Quotient ist x Quadrat minus vier. Probe: Klammer x plus eins mal x Quadrat minus vier '
            'gibt wieder x hoch drei plus x Quadrat minus vier x minus vier.',
            f(r'(x \fb{+ 1})(x^2 - 4) = x^3 + x^2 - 4x - 4', 300, 44, ein=1.0),
            n('Probe: zurückmultiplizieren', 440, 'orange', ein=3.0),
            # Erst nach der Antwort: Am Graphen wären die Nullstellen ±2 abzulesen (§15).
            graf(WK4b, [poly([[0, 1, -1, -2, 2]])], ein=1.2)),
         sz('Frage 4',
            'x Quadrat minus vier ist null bei plus zwei und minus zwei. Zusammen mit der geratenen minus eins '
            'sind es drei Nullstellen.',
            f(r'x^2 - 4 = 0 \;\Rightarrow\; x = \pm 2', 300, 52, ein=1.0),
            n('alle Nullstellen: @\\fb{-2},\\ \\fb{-1},\\ \\fb{2}@', 440, 'orange', ein=2.4),
            # Erst nach der Antwort: sonst stünde die Antwort im Bild (§15).
            graf(WK4b, [poly([[0, 1, -1, -2, 2]], nullstellen={'farbe': 2})], ein=3.0)),
         sz('Frage 5',
            'Wer durch x teilt, verliert die Lösung null. Richtig ist: alles auf eine Seite, x ausklammern, '
            'Nullprodukt. Dann sind es drei Lösungen: null, drei und minus drei.',
            f(r'x^3 = 9x \;\Rightarrow\; x\,(x^2 - 9) = 0', 300, 48, ein=1.0),
            n('nicht durch @x@ teilen —|@x = \\fd{0}@ ginge verloren', 440, 'rot', ein=2.4),
            graf(W9, [poly([[0, 1, -3, 0, 3]], nullstellen={'farbe': 2})], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Ausklammern, raten, abspalten, den Quotienten lösen. Und nie durch x teilen.',
            titel('Zum Mitnehmen', 250, 76),
            n('ausklammern; raten; abspalten|Probe: ausmultiplizieren|nie durch @x@ teilen',
              400, 'blau', 44, ein=1.2),
            graf(WK4b, [poly([[0, 1, -1, -2, 2]], nullstellen={'farbe': 2})])),
     ], [
         wahl('Frage 1', 'Welche Nullstellen hat f(x) = x³ − 4x²?',
              ['0 (doppelt) und 4', '0 und −4', 'nur 4'], 0,
              {0: 'Ja.',
               1: 'Klammere x² aus und setz die Klammer null: Welches Vorzeichen hat die Lösung?',
               2: 'Und der Faktor x²? Auch er wird null.'},
              sprich='Welche Nullstellen hat f von x gleich x hoch drei minus vier x Quadrat?',
              rueck_sprich={1: 'Klammere x Quadrat aus und setz die Klammer null: Welches Vorzeichen hat die Lösung?',
                            2: 'Und der Faktor x Quadrat? Auch er wird null.'}),
         wahl('Frage 2', 'f(x) = x³ + x² − 4x − 4: Welche Zahl ist eine Nullstelle?',
              ['−1', '1', '4'], 0,
              {0: 'Ja.',
               1: 'Rechne f(1) = 1 + 1 − 4 − 4 aus.',
               2: 'Rechne f(4) aus: 64 + 16 − 16 − 4.'},
              sprich='f von x gleich x hoch drei plus x Quadrat minus vier x minus vier: Welche Zahl ist eine Nullstelle?',
              rueck_sprich={1: 'Rechne f von eins aus: eins plus eins minus vier minus vier.',
                            2: 'Rechne f von vier aus: vierundsechzig plus sechzehn minus sechzehn minus vier.'}),
         wahl('Frage 3', 'x³ + x² − 4x − 4 = (x + 1)(x² + px + q): Welcher Quotient x² + px + q?',
              ['x² − 4', 'x² + 2x − 4', 'x² − 4x'], 0,
              {0: 'Ja.',
               1: 'Multiplizier zur Probe aus: Kommt x³ + x² − 4x − 4 heraus?',
               2: 'Multiplizier zur Probe aus: Wo bleibt die −4 am Schluss?'},
              sprich='x hoch drei plus x Quadrat minus vier x minus vier ist gleich Klammer x plus eins, mal x Quadrat '
                     'plus p x plus q. Welcher Quotient?',
              rueck_sprich={1: 'Multiplizier zur Probe aus: Kommt x hoch drei plus x Quadrat minus vier x minus vier heraus?',
                            2: 'Multiplizier zur Probe aus: Wo bleibt die minus vier am Schluss?'}),
         wahl('Frage 4', 'Alle zusammen: Welche Nullstellen hat f(x) = x³ + x² − 4x − 4?',
              ['−2, −1 und 2', '−1 und 2', '−1 und 4'], 0,
              {0: 'Ja.',
               1: 'x² − 4 = 0 hat zwei Lösungen. Welche fehlt?',
               2: 'Die Nullstellen des Quotienten sind die Lösungen von x² − 4 = 0, nicht die Zahl 4.'},
              sprich='Alle zusammen: Welche Nullstellen hat f von x gleich x hoch drei plus x Quadrat minus vier x minus vier?',
              rueck_sprich={1: 'x Quadrat minus vier gleich null hat zwei Lösungen. Welche fehlt?',
                            2: 'Die Nullstellen des Quotienten sind die Lösungen von x Quadrat minus vier gleich null, nicht die Zahl vier.'}),
         wahl('Frage 5', 'Jemand löst x³ = 9x, indem er durch x teilt: x² = 9, also x = ±3. Was fehlt?',
              ['die Lösung x = 0', 'nichts', 'die Lösung x = 9'], 0,
              {0: 'Ja.',
               1: 'Setz x = 0 in die Gleichung ein: Stimmt sie?',
               2: 'Setz x = 9 ein: 729 gegen 81.'},
              sprich='Jemand löst x hoch drei gleich neun x, indem er durch x teilt: x Quadrat gleich neun, '
                     'also x gleich plus minus drei. Was fehlt?',
              rueck_sprich={1: 'Setz x gleich null in die Gleichung ein: Stimmt sie?',
                            2: 'Setz x gleich neun ein: siebenhundertneunundzwanzig gegen einundachtzig.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
# Beispiel: f(x) = x³ − 3x mit H(−1 | 2) und T(1 | −2) — Startwert der Simulation 5.
S3 = 3 ** 0.5
B5 = [1, -S3, 0, S3]
W5 = dict(xbereich=[-3, 3], ybereich=[-4, 6], yteilung=yt(-4, -2, 2, 4, 6), xteilung=yt(-2, -1, 1, 2))
W5r = dict(xbereich=[-2, 3], ybereich=[-4, 10], yteilung=yt(-4, -2, 2, 4, 6, 8, 10))
WQ = dict(xbereich=[-1, 5], ybereich=[-4, 4], yteilung=yt(-4, -2, 2, 4))
WS = dict(xbereich=[-0.8, 8], ybereich=[-45, 450], yteilung=yt(100, 200, 300, 400), xteilung=yt(2, 4, 6),
          xname='x [cm]', yname='V [cm³]')
XS = 2.83
NETZ = ([{'art': 'vieleck', 'punkte': q, 'farbe': 5, 'fuellung': 0.22, 'dicke': 2.5} for q in (
            [[0, 0], [XS, 0], [XS, XS], [0, XS]], [[20 - XS, 0], [20, 0], [20, XS], [20 - XS, XS]],
            [[0, 15 - XS], [XS, 15 - XS], [XS, 15], [0, 15]], [[20 - XS, 15 - XS], [20, 15 - XS], [20, 15], [20 - XS, 15]])]
        + [{'art': 'vieleck', 'punkte': [[XS, XS], [20 - XS, XS], [20 - XS, 15 - XS], [XS, 15 - XS]], 'farbe': 1,
            'fuellung': 0.10, 'dicke': 2.5, 'gestrichelt': True},
           {'art': 'vieleck', 'punkte': [[0, 0], [20, 0], [20, 15], [0, 15]], 'farbe': 5, 'dicke': 3},
           {'art': 'text', 'bei': [10, -2.2], 'text': '20 cm', 'farbe': 5, 'kursiv': False, 'groesse': 26},
           {'art': 'text', 'bei': [-0.6, 7.0], 'text': '15 cm', 'farbe': 5, 'kursiv': False, 'groesse': 26,
            'anker': 'end'},
           {'art': 'text', 'bei': [XS / 2, 15.5], 'text': 'x', 'farbe': 5, 'groesse': 26}])
clip('extrema', 'Polynom sehen: Hoch- und Tiefpunkte',
     'Hoch- und Tiefpunkte ablesen, lokal und absolut unterscheiden, beim Grad 2 exakt berechnen.',
     ['Hochpunkt', 'Tiefpunkt', 'lokales Maximum', 'absolutes Maximum', 'Extremwert'], [
         sz('Hoch und tief',
            'f von x gleich x hoch drei minus drei x. Bei minus eins hört der Graph auf zu steigen und beginnt zu fallen: '
            'ein Hochpunkt, H minus eins, zwei. Bei eins wechselt er von fallend zu steigend: ein Tiefpunkt, T eins, minus zwei.',
            titel('Hoch und tief', 280, 80),
            f(r'f(x) = x^3 - 3x', 430, 58, ein=1.0),
            # Läufer (seit 07.10.2026) zum Vorgang: steigt bis −1 und hält («hört … auf zu steigen», 3.1–4.8 s),
            # fällt («beginnt zu fallen», 5.1–6.0 s); fällt bis 1 («von fallend», 8.7–9.9 s), steigt
            # («zu steigend», 10.0–10.8 s). H und T zum Wort («Hochpunkt» 6.7 s, «Tiefpunkt» 11.1 s).
            graf(W5, [dict(poly([[0] + B5]), laeufer={'bahn': [[3.1, -2], [4.8, -1], [5.1, -1], [6.0, 0], [8.7, 0],
                                                               [9.9, 1], [10.0, 1], [10.8, 2]], 'farbe': 5})], ein=3.0,
                 punkte=[dict(pt(-1, 2, 3, 'H(−1 | 2)', [-1, 2.6], 'middle'), ein=6.7),
                         dict(pt(1, -2, 3, 'T(1 | −2)', [1, -2.85], 'middle'), ein=11.1)])),
         sz('Lokal',
            'Ist zwei der grösste Funktionswert? Nein: Bei x gleich zweieinhalb ist f schon über acht, '
            'und weiter rechts wächst es ohne Grenze. Das Maximum bei H gilt nur in seiner Umgebung — es ist lokal.',
            f(r'f(2.5) = 8.125 \gt 2', 300, 56, ein=3.0),
            n('Hochpunkt = lokales Maximum|kein absolutes Maximum auf @\\mathbb{R}@', 440, 'gruen', ein=8.0),
            graf(W5r, [poly([[0] + B5], extrema={'farbe': 3, 'beschriftung': False},
                           marken=[{'x': 2.5, 'text': '(2.5 | 8.125)', 'farbe': 5}])], ein=1.0),
            # «Das Maximum bei H» (8.0 s): H benennen
            ueber(W5r, [pt(-1, 2, 3, 'H(−1 | 2)', [-1, 2.6], 'middle')], ein=8.0)),
         sz('Am Rand',
            'Anders auf einem Intervall, etwa von minus eins Komma fünf bis zwei Komma fünf. Dann gibt es einen grössten '
            'Wert: am rechten Rand, acht Komma eins zwei fünf. Der kleinste ist der Tiefpunkt, minus zwei. '
            'Absolute Extremwerte liegen in einem Hoch- oder Tiefpunkt — oder am Rand.',
            f(r'D = [-1.5;\, 2.5]', 300, 58),
            n('absolutes Maximum: am Rand|absolutes Minimum: im Tiefpunkt', 440, 'gruen', ein=7.8),
            # Das Intervall zieht sich zum Ton zusammen (grenzen, seit 07.10.2026): links bei «minus eins Komma fünf»
            # (2.2–3.2 s), rechts bei «zwei Komma fünf» (3.6–4.4 s); die Randpunkte erscheinen, wenn der Rand
            # dort ankommt, der Wert am rechten Rand mit «acht Komma eins zwei fünf» (7.7 s).
            graf(W5r, [fest('x**3-3*x'), dict(poly([[0] + B5], extrema={'farbe': 3, 'beschriftung': False}),
                                              grenzen=[[2.2, -2, 3], [3.2, -1.5, 3], [3.6, -1.5, 3], [4.4, -1.5, 2.5]])],
                 ein=1.0,
                 punkte=[dict(pt(-1.5, 1.125, 5), ein=3.2), dict(pt(2.5, 8.125, 5), ein=4.4),
                         dict(pt(2.5, 8.125, 5, '(2.5 | 8.125)', [2.38, 8.46], 'end'), ein=7.7)])),
         sz('Grad 2 exakt',
            'Beim Grad zwei lässt sich der Extrempunkt exakt berechnen. Minus x Quadrat plus vier x minus eins: '
            'x s gleich minus b durch zwei a, also minus vier durch minus zwei, gleich zwei. f von zwei ist drei. '
            'Weil a negativ ist, ist es ein Hochpunkt.',
            f(r'f(x) = \fa{-}x^2 + 4x - 1', 300, 52),
            f(r'x_s = -\dfrac{b}{2a} = -\dfrac{4}{-2} = 2', 400, 46, ein=3.7),
            n('@f(2) = 3@: @\\fc{H(2 \\mid 3)}@|@\\fa{a} \\lt 0@: Hochpunkt', 520, 'gruen', 44, ein=12.3),
            graf(WQ, [fest('-x**2+4*x-1', farbe=1, gestrichelt=False)], ein=1.0),
            graf(WQ, [fest('-x**2+4*x-1', farbe=1, gestrichelt=False)], ein=12.3,
                 punkte=[pt(2, 3, 3, 'H(2 | 3)', [2.25, 3.55])])),
         sz('Höherer Grad',
            'Ab Grad drei geht das so nicht mehr. Hoch- und Tiefpunkte liest man am Graphen ab — oder mit dem Rechner, '
            'in einer feinen Wertetabelle. Exakt rechnet man sie später mit der Ableitung.',
            f(r'\text{Grad} \geq 3: \text{grafisch}', 300, 52),
            n('Wertetabelle mit kleiner Schrittweite|oder Funktionsplotter', 440, 'blau', ein=5.0),
            graf(W5, [poly([[0] + B5], extrema={'farbe': 3})], ein=1.0)),
         sz('Anwendung',
            'Bei Anwendungen schränkt der Sachverhalt die Definitionsmenge ein. Die offene Schachtel aus einem Karton '
            'von zwanzig mal fünfzehn Zentimetern: Volumen x mal zwanzig minus zwei x mal fünfzehn minus zwei x, sinnvoll '
            'nur für x zwischen null und sieben Komma fünf. Der Hochpunkt liegt bei rund zwei Komma acht drei, '
            'mit rund dreihundertneunundsiebzig Kubikzentimetern.',
            f(r'V(x) = x\,(20 - 2x)(15 - 2x)', 300, 46),
            n('@D = \\, ]0;\\, 7.5[@|@\\fc{H \\approx (2.83 \\mid 379)}@ — hier auch absolut', 420, 'gruen', 44, ein=14.4),
            # Das Netz der Schachtel (4.0 s, «Die offene Schachtel aus einem Karton …»): 20 × 15,
            # Eckquadrate x = 2.83 (die Lösung), gestrichelt die Faltkanten
            graf(dict(xbereich=[-5.5, 21.5], ybereich=[-3, 16.5], raster=False, achsen=False), ein=4.0,
                 x=LX, y=580, breite=448, hoehe=328, figuren=NETZ),
            graf(WS, [poly([[0, 4, 0, 7.5, 10]], von=0, bis=7.5)], ein=1.0),
            # «Der Hochpunkt liegt bei rund zwei Komma acht drei …» (14.4 s)
            ueber(WS, [pt(2.83, 379, 3, 'H ≈ (2.83 | 379)', [3.1, 420])], ein=14.4)),
         sz('Merke',
            'Zum Mitnehmen: Hoch- und Tiefpunkte sind lokale Extrema. Absolut grösste und kleinste Werte gibt es oft '
            'nur auf einem Intervall — im Hoch- oder Tiefpunkt oder am Rand. Beim Grad zwei rechnet man exakt, '
            'sonst liest man ab.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\fc{H}@, @\\fc{T}@: lokal|absolut: Extrempunkt oder Rand|Grad 2: @x_s = -\\frac{b}{2a}@',
              400, 'blau', 44, ein=1.2),
            graf(W5, [poly([[0] + B5], extrema={'farbe': 3})])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
import numpy as _np                                    # noqa: E402
R6 = sorted(float(r.real) for r in _np.roots([-1, 0, 3, 1]))      # −x³ + 3x + 1
W6 = dict(xbereich=[-3, 3], ybereich=[-4, 6], yteilung=yt(-4, -2, 2, 4, 6), xteilung=yt(-2, -1, 1, 2))
clip('kontrolle-extrema', 'Polynom sehen: Kontrollfragen zu Hoch- und Tiefpunkten',
     'Fünf Vorhersagen zu Hoch- und Tiefpunkten, lokal und absolut.',
     ['Hochpunkt', 'Tiefpunkt', 'absolutes Maximum', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei minus eins wechselt der Graph von fallend zu steigend: Dort liegt der Tiefpunkt, T minus eins, minus eins.',
            f(r'f(x) = -x^3 + 3x + 1', 300, 56, ein=1.0),
            n('@\\fc{T(-1 \\mid -1)}@, @\\fc{H(1 \\mid 3)}@', 440, 'gruen', ein=2.4),
            graf(W6, [poly([[0, -1] + [round(r, 6) for r in R6]])]),
            graf(W6, [poly([[0, -1] + [round(r, 6) for r in R6]], extrema={'farbe': 3})], ein=2.4)),
         sz('Frage 2',
            'Nach links wächst minus x hoch drei ohne Grenze. Es gibt grössere Werte als drei — ein absolutes Maximum '
            'hat f auf ganz R nicht.',
            f(r'f(-3) = 27 - 9 + 1 = 19 \gt 3', 300, 50, ein=1.0),
            n('Hochpunkt = nur lokal', 440, 'gruen', ein=2.4),
            graf(dict(xbereich=[-3, 3], ybereich=[-4, 20], yteilung=yt(-4, 4, 8, 12, 16, 20), xteilung=yt(-2, -1, 1, 2)),
                 [poly([[0, -1] + [round(r, 6) for r in R6]], extrema={'farbe': 3, 'beschriftung': False},
                       marken=[{'x': -3, 'text': '(−3 | {y})', 'farbe': 5}])], ein=1.2)),
         sz('Frage 3',
            'x s gleich minus b durch zwei a: minus minus sechs durch zwei, also drei. f von drei ist neun minus achtzehn '
            'plus fünf, gleich minus vier. a ist positiv: ein Tiefpunkt.',
            f(r'x_s = -\dfrac{-6}{2 \cdot 1} = 3, \quad f(3) = -4', 300, 46, ein=1.0),
            n('@\\fa{a} \\gt 0@: @\\fc{T(3 \\mid -4)}@', 440, 'gruen', ein=2.4),
            graf(dict(xbereich=[-1, 7], ybereich=[-5, 6], yteilung=yt(-4, -2, 2, 4, 6)),
                 [poly([[0, 1, 1, 5]], extrema={'farbe': 3})], ein=3.0)),
         sz('Frage 4',
            'Bei einer Polynomfunktion zweiten Grades mit negativem a ist die Parabel nach unten geöffnet. Ihr Scheitel '
            'ist ein Hochpunkt — und hier sogar das absolute Maximum.',
            f(r'\fa{a} \lt 0: \text{nach unten geöffnet}', 300, 52, ein=1.0),
            n('Scheitel = Hochpunkt|= absolutes Maximum', 440, 'gruen', ein=2.4),
            graf(WQ, [fest('-x**2+4*x-1', farbe=1, gestrichelt=False)], ein=1.2)),
         sz('Frage 5',
            'Auf dem Intervall von null bis vier ist f von vier gleich vierundsechzig minus zwölf, also zweiundfünfzig. '
            'Das ist viel mehr als jeder andere Wert: Das absolute Maximum liegt am rechten Rand.',
            f(r'f(4) = 64 - 12 = 52', 300, 56, ein=1.0),
            n('absolutes Maximum am Rand @x = 4@', 440, 'gruen', ein=2.4),
            graf(dict(xbereich=[-0.5, 4.5], ybereich=[-6, 56], yteilung=yt(10, 20, 30, 40, 50), xteilung=yt(1, 2, 3, 4)),
                 [poly([[0] + B5], von=0, bis=4, extrema={'farbe': 3, 'beschriftung': False},
                       marken=[{'x': 4, 'text': '(4 | {y})', 'farbe': 5}])], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Hoch- und Tiefpunkte sind lokal. Absolute Extrema gibt es oft nur auf einem Intervall, '
            'und dann liegen sie im Hoch- oder Tiefpunkt oder am Rand.',
            titel('Zum Mitnehmen', 250, 76),
            n('lokal: Hoch- und Tiefpunkt|absolut: auch die Ränder prüfen|Grad 2: @x_s = -\\frac{b}{2a}@',
              400, 'blau', 44, ein=1.2),
            graf(W6, [poly([[0, -1] + [round(r, 6) for r in R6]], extrema={'farbe': 3})])),
     ], [
         klick('Frage 1', 'f(x) = −x³ + 3x + 1: Tipp den Tiefpunkt ins Bild.',
               [-1, -1], 'Getroffen: T(−1 | −1).',
               [{'bei': [1, 3], 'text': 'Das ist der Hochpunkt: Dort wechselt der Graph von steigend zu fallend.',
                 'sprich': 'Das ist der Hochpunkt. Dort wechselt der Graph von steigend zu fallend.'},
                {'bei': [0, 1], 'text': 'Das ist der Schnittpunkt mit der y-Achse. Wo wechselt der Graph von fallend zu steigend?',
                 'sprich': 'Das ist der Schnittpunkt mit der y-Achse. Wo wechselt der Graph von fallend zu steigend?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — wo ist der Graph lokal am tiefsten?',
               sprich='f von x gleich minus x hoch drei plus drei x plus eins: Tipp den Tiefpunkt ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Wo ist der Graph lokal am tiefsten?'),
         wahl('Frage 2', 'f hat den Hochpunkt H(1 | 3). Ist 3 der grösste Funktionswert von f auf ganz ℝ?',
              ['Nein, links wird f beliebig gross.', 'Ja, ein Hochpunkt ist immer das Maximum.', 'Ja, weil der Grad ungerade ist.'], 0,
              {0: 'Ja.',
               1: 'Rechne f(−3) aus und vergleich mit 3.',
               2: 'Gerade bei ungeradem Grad wächst f auf einer Seite ohne Grenze.'},
              sprich='f hat den Hochpunkt H eins, drei. Ist drei der grösste Funktionswert von f auf ganz R?',
              rueck_sprich={1: 'Rechne f von minus drei aus und vergleich mit drei.',
                            2: 'Gerade bei ungeradem Grad wächst f auf einer Seite ohne Grenze.'}),
         wahl('Frage 3', 'f(x) = x² − 6x + 5: Wo liegt der Extrempunkt?',
              ['T(3 | −4)', 'H(3 | −4)', 'T(−3 | 32)'], 0,
              {0: 'Ja.',
               1: 'Ist a positiv oder negativ? Dann ist die Parabel nach oben oder nach unten geöffnet.',
               2: 'Vorzeichen: xₛ = −b/(2a), und b ist −6.'},
              sprich='f von x gleich x Quadrat minus sechs x plus fünf: Wo liegt der Extrempunkt?',
              rueck_sprich={1: 'Ist a positiv oder negativ? Dann ist die Parabel nach oben oder nach unten geöffnet.',
                            2: 'Vorzeichen: x s ist minus b durch zwei a, und b ist minus sechs.'}),
         wahl('Frage 4', 'f(x) = −x² + 4x − 1: Ist der Extrempunkt ein Hoch- oder ein Tiefpunkt?',
              ['Hochpunkt', 'Tiefpunkt', 'Das lässt sich ohne Graph nicht sagen.'], 0,
              {0: 'Ja.',
               1: 'Schau auf das Vorzeichen von a.',
               2: 'Das Vorzeichen von a genügt.'},
              sprich='f von x gleich minus x Quadrat plus vier x minus eins: Ist der Extrempunkt ein Hoch- oder ein Tiefpunkt?',
              rueck_sprich={1: 'Schau auf das Vorzeichen von a.',
                            2: 'Das Vorzeichen von a genügt.'}),
         wahl('Frage 5', 'f(x) = x³ − 3x auf D = [0; 4]: Wo liegt das absolute Maximum?',
              ['am Rand, bei x = 4', 'im Hochpunkt H(−1 | 2)', 'im Tiefpunkt T(1 | −2)'], 0,
              {0: 'Ja.',
               1: 'Liegt x = −1 überhaupt in D?',
               2: 'Der Tiefpunkt ist der kleinste Wert, nicht der grösste.'},
              sprich='f von x gleich x hoch drei minus drei x, auf D von null bis vier: Wo liegt das absolute Maximum?',
              rueck_sprich={1: 'Liegt x gleich minus eins überhaupt in D?',
                            2: 'Der Tiefpunkt ist der kleinste Wert, nicht der grösste.'}),
     ], art='Kontrollclip')
