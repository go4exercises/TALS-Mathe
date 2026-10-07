"""Erzeugt die acht Drehbücher des Leitprogramms Lineare Funktionen (03.10.2026).

  python3 scripts/lp/lineare-funktionen/clips.py

**Nach der Vertonung nicht mehr laufen lassen** — dann sind die JSONs in clips/ die
Quelle und tragen die gemessenen `dauer` (HOWTO-clips.md, «Werkstatt»). Das Skript liegt
hier als Muster und als Nachweis, woher die Szenen kommen.

Aufbau wie beim Vorbild (scripts/lp/quadratische-funktionen/kontrollclips.py): Bild rechts
(x 1010, y 175, 760 × 760), Formeln und Notizen links (x 150), Theme begreifbar-schlicht.

**Bewegte Geraden** (seit 03.10.2026, HOWTO-clips.md «Bewegte Parabel und Gerade»):
Stützpunkte `[t, m, q]` ab Szenenbeginn, Begleiter `yachse`, `nullstelle` und `dreieck`
(mitlaufendes Steigungsdreieck; Stelle und Breite dürfen selbst einer Bahn folgen).
Was der Ton sagt, zeigt das Bild: b schiebt senkrecht, m kippt um (0 | b), das Dreieck
wird kleiner und der Quotient bleibt, die Gerade rastet auf dem gegebenen Punkt ein.

Farben im ganzen Leitprogramm — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15):
  1 blau   = m und die Gerade                    \\fa{…}
  2 orange = b und der Punkt (0 | b)              \\fb{…}
  3 grün   = «stimmt»: Nullstelle, Treffer, Probe \\fc{…}
  4 rot    = Gegenbeispiel, keine Funktion        \\fd{…}
  5 Tinte  = neutral: gegebener Punkt, Bezugsgerade, Steigungsdreieck

Fenster: Wo das Auge Schritte zählt oder ein rechter Winkel zu sehen sein muss, sind
x- und y-Spanne gleich — das Bild ist quadratisch (760 × 760).

Fragen: je Kontrollclip vier vom Typ `wahl` und eine vom Typ `klick`. Beim Erscheinen der
Frage zeigt das Bild **nur, was die Frage gibt** (Abnahme 06.10.2026): gegebene Punkte, eine
gegebene Gerade, sonst nur die Achsen — keine Startgerade, kein Steigungsdreieck, kein
Lösungspunkt. Das regelt `FRAGEBILD` unten; die Auflösungsgrafik der Szene erscheint erst
ab 1.0 s, nach der Antwort. Wo die Frage nach «der Geraden im Bild» fragt, ist diese Gerade
das Gegebene.
"""
import json
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/lp/grafgeom.py

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150

from grafgeom import achsenkisten, frei, kiste, masse       # Geometrie wie in build-clips.py


def stelle(text, x, y, geraden, punkte, W, belegt):
    """Freie Stelle für eine feste Beschriftung — gerechnet, nicht geschätzt."""
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


def graf(W, geraden=(), punkte=(), ein=0.05, **kw):
    # Nur feste Geraden zaehlen beim Freihalten der Beschriftungen; eine bewegte steht
    # nie lange an derselben Stelle, und ihre Begleiter setzen sich selbst.
    ger_l = [(g['m'], g['q']) for g in geraden if 'm' in g]
    pkt_l = [(p['x'], p['y']) for p in punkte]
    belegt = achsenkisten(dict(W, **{k: v for k, v in kw.items() if k in ('xname', 'yname')}))
    for p in punkte:
        if p.get('beschriftung') and 'beschriftung_bei' not in p:
            p['beschriftung_bei'], p['anker'] = stelle(p['beschriftung'], p['x'], p['y'],
                                                       ger_l, pkt_l, W, belegt)
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             geraden=list(geraden), punkte=list(punkte), pfeile=True, **W)
    g.update(kw)
    return g


def ueber(W, geraden=(), punkte=(), ein=0.05, **kw):
    """Zweites Bild deckungsgleich ueber dem ersten, nur Inhalt (ohne Achsen und Karo).

    Notbehelf, solange feste Punkte und Figuren im `graf` kein eigenes `ein` haben
    (TODO-lp-clips-visualisierung.md): Was erst beim zugehoerigen Wort erscheinen soll,
    steht in einem eigenen `graf` mit derselben Lage und demselben Fenster.
    """
    return graf(W, geraden, punkte, ein=ein, achsen=False, raster=False, **kw)


def ger(m, q, farbe=1, gestrichelt=False, dicke=None):
    """Feste Gerade."""
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    return d


def bew(stuetz, farbe=1, yachse=None, nullstelle=None, dreieck=None, gestrichelt=False, dicke=None):
    """Bewegte Gerade: Stuetzpunkte [t, m, q] ab Szenenbeginn."""
    d = {'bewegung': stuetz, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if yachse is not None:
        d['yachse'] = yachse
    if nullstelle is not None:
        d['nullstelle'] = nullstelle
    if dreieck is not None:
        d['dreieck'] = dreieck
    return d


def dreieck(x, dx, bahn=None):
    return {'bahn': bahn, 'farbe': 5} if bahn else {'x': x, 'dx': dx, 'farbe': 5}


def pt(x, y, farbe=5, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
    if bei:
        d['beschriftung_bei'] = bei
    return d


def leiter(x, y0, y1, farbe=4):
    """Punktleiter bei x — so ist die senkrechte Gerade zu sehen, von der der Ton spricht."""
    return [pt(x, y, farbe) for y in range(y0, y1 + 1)]


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

    Stand sie in allen Wahlfragen an Position 0, liess sich jede ohne Nachdenken über
    die erste Schaltfläche lösen (externe Prüfung, 03.10.2026). Die Drehung ist
    deterministisch aus Szene und Fragetext — derselbe Lauf gibt dieselbe Reihenfolge,
    und Rückmeldungen wie Tondateien wandern mit, weil sie nach dem Drehen aus dem
    Drehbuch erzeugt werden.
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


# Was das Bild beim Erscheinen einer Frage zeigen darf: genau das Gegebene. Schluessel
# (Clip, Szene) -> (Fenster, feste Geraden, Punkte). Fehlt eine Szene, bleiben nur die Achsen.
def _fragebild_daten():
    W_KB_ = W_KB
    return {
        ('kontrolle-m-und-b', 'Frage 3'): (W_MB, [ger(-1, 3)], []),
        ('kontrolle-steigung', 'Frage 1'): (W_TAB, [], [pt(-2, -1, 5, 'A(−2 | −1)', [-2.3, -1.9], 'end'), pt(2, 7, 5, 'B(2 | 7)')]),
        ('kontrolle-steigung', 'Frage 2'): (dict(xbereich=[-4, 5], ybereich=[-6, 3], yteilung=[[-5, '−5'], [0, '0']]), [],
                                            [pt(-2, 3, 5, 'P(−2 | 3)'), pt(2, -5, 5, 'Q(2 | −5)')]),
        ('kontrolle-steigung', 'Frage 4'): (W_DREI, [ger(-0.5, 2)], []),
        ('kontrolle-typen', 'Frage 3'): (W_GL, [ger(3, 2)], []),
        ('kontrolle-typen', 'Frage 4'): (W_GL, [ger(4, -1)], []),
        ('kontrolle-typen', 'Frage 5'): (W_GL, [ger(0.5, 2), ger(-2, -1)], []),
        ('kontrolle-aufstellen', 'Frage 1'): (W_KB_, [], [pt(2, 1, 5, 'P(2 | 1)')]),
        ('kontrolle-aufstellen', 'Frage 2'): (W_GL, [], [pt(0, 4, 5, 'A(0 | 4)'), pt(2, 0, 5, 'B(2 | 0)')]),
        ('kontrolle-aufstellen', 'Frage 3'): (dict(xbereich=[-4, 6], ybereich=[-3, 7]), [], [pt(4, 1, 5, 'P(4 | 1)')]),
        ('kontrolle-aufstellen', 'Frage 4'): (dict(xbereich=[-2, 8], ybereich=[-2, 8]), [ger(-3, 2, 5, gestrichelt=True)],
                                              [pt(1, 4, 5, 'P(1 | 4)')]),
    }


def fragebild(name, szene):
    """Fuer jede Fragenszene: Auflösungsgrafik erst nach der Antwort, davor nur das Gegebene."""
    grafen = [e for e in szene['elemente'] if e.get('typ') == 'graf']
    if not grafen:
        return
    W, geraden, punkte = _fragebild_daten().get((name, szene['name']), (None, [], []))
    if W is None:
        W = {k: grafen[0][k] for k in ('xbereich', 'ybereich', 'xteilung', 'yteilung', 'xname', 'yname') if k in grafen[0]}
    for g in grafen:
        g['ein'] = max(g.get('ein', 0.05), 1.0)
    szene['elemente'].insert(0, graf(W, geraden, punkte, tippbar=True,
                                     **{k: grafen[0][k] for k in ('xname', 'yname') if k in grafen[0] and k not in W}))


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    if art == 'Kontrollclip':
        for q in szenen:
            if q['name'].startswith('Frage'):
                fragebild(name, q)
    # Gemessene Dauern retten: Wo Szenenname und Sprechertext gleich geblieben sind,
    # gilt die Zeit aus der vertonten Fassung weiter. Nur fuer Szenen mit neuem Text
    # muss danach build-clip-ton.py laufen. (Ohne das ueberschriebe jeder Lauf dieses
    # Skripts die Messung — HOWTO-clips.md, «Werkstatt».)
    alt = R + 'clips/g3-2-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer')
                   for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 'g3-2-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Funktionen · linear', 'fach': 'Grundlagenfach',
         'lerngebiet': '3 · Funktionen', 'lektion': ['g3-2'], 'stufe': ['BM1', 'BM2'],
         'datum': '2026-10-03', 'theme': 'begreifbar-schlicht', 'latex': True,
         'reihe': 'Gerade sehen', 'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms lineare-funktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# Fenster. Wo das Auge Schritte zaehlt oder ein rechter Winkel zu sehen ist, sind beide
# Spannen gleich — das Bild ist quadratisch.
W_TAB = dict(xbereich=[-5, 7], ybereich=[-4, 8])            # 12 / 12
W_MB = dict(xbereich=[-4, 5], ybereich=[-4, 5])             # 9 / 9
W_DREI = dict(xbereich=[-2, 7], ybereich=[-3, 6])           # 9 / 9
W_NULL = dict(xbereich=[-2, 7], ybereich=[-8, 1],           # 9 / 9, b = −6 ist im Bild
              yteilung=[[-6, '−6'], [-3, '−3'], [0, '0']])
W_GL = dict(xbereich=[-4, 5], ybereich=[-4, 5])             # 9 / 9
W_WEIT = dict(xbereich=[-1, 8], ybereich=[-2, 11],          # 9 / 13
              yteilung=[[0, '0'], [5, '5'], [10, '10']])
W_TAXI = dict(xbereich=[-0.5, 8.5], ybereich=[-3, 33],
              yteilung=[[0, '0'], [10, '10'], [20, '20'], [30, '30']])
W_KB = dict(xbereich=[-3, 6], ybereich=[-7, 11],            # Kontrolle «Aufstellen» F1: b = −5
            yteilung=[[-5, '−5'], [0, '0'], [5, '5'], [10, '10']])
W_TANK = dict(xbereich=[-2, 22], ybereich=[-20, 180],
              xteilung=[[0, '0'], [10, '10'], [20, '20']],
              yteilung=[[0, '0'], [80, '80'], [160, '160']])

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('m-und-b', 'Gerade sehen: m kippt, b schiebt',
     'Von der Wertetabelle zur Geraden — und wie b sie senkrecht schiebt und m sie kippt.',
     ['lineare Funktion', 'Steigung', 'y-Achsenabschnitt', 'Gerade', 'Wertetabelle'], [
         # Einblendzeiten nach sprechzeiten.py: der Satz zur Tabelle beginnt bei rund 5.9 s,
         # «Jedes Wertepaar wird ein Punkt» bei 15.3 s.
         sz('Wertetabelle',
            'Eine lineare Funktion ändert sich bei gleichen Schritten nach rechts immer um denselben Betrag — '
            'nach oben, nach unten oder gar nicht. Zum Beispiel y gleich zwei x plus eins. '
            'Die Wertetabelle: minus drei, minus eins, eins, drei, fünf, sieben. Jedes Wertepaar wird ein Punkt.',
            titel('Die Gerade', 280, 80),
            f(r'\begin{array}{c|cccccc} x & -2 & -1 & 0 & 1 & 2 & 3 \\ \hline y = 2x + 1 & -3 & -1 & 1 & 3 & 5 & 7 \end{array}',
              440, 40, ein=5.9),
            graf(W_TAB, punkte=[pt(x, 2 * x + 1, 1) for x in (-2, -1, 0, 1, 2, 3)], ein=15.3)),
         sz('Die Gerade',
            'Verbunden ergeben die Punkte eine Gerade. Von Punkt zu Punkt geht es einen nach rechts und '
            'zwei hinauf — jedes Mal gleich viel. Genau das macht den Graphen zur Geraden.',
            f(r'y = 2x + 1', 300, 70),
            n('gleicher Schritt nach rechts,|gleicher Zuwachs hinauf', 440, 'blau'),
            graf(W_TAB, [bew([[0.6, 2, 1]], dreieck=dreieck(None, None, [[2.4, -2, 1], [5.4, 2, 1]]))],
                 [pt(x, 2 * x + 1, 1) for x in (-2, -1, 0, 1, 2, 3)])),
         sz('Zwei Zahlen',
            'Jede nicht senkrechte Gerade steckt in zwei Zahlen: m und b. Schauen wir sie uns einzeln an.',
            titel('Zwei Zahlen', 300, 86),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 470, 66),
            graf(W_MB, [bew([[0, 2, 1]], yachse={'farbe': 2})])),
         sz('b schiebt hinauf',
            'Zuerst b. Plus drei hebt die ganze Gerade um drei nach oben. Sie schneidet die y-Achse bei drei, '
            'und ihre Richtung bleibt gleich.',
            f(r'y = \fa{2}x \fb{+ 3}', 300, 70),
            n('@\\fb{b}@ ist der @y@-Achsenabschnitt:|die Gerade schneidet die @y@-Achse bei @\\fb{3}@', 440, 'orange'),
            graf(W_MB, [ger(2, 0, 5, gestrichelt=True), bew([[0.9, 2, 0], [3.8, 2, 3]], yachse={'farbe': 2})])),
         sz('b schiebt hinunter',
            'Minus zwei senkt sie um zwei. Das Vorzeichen stimmt mit der Richtung überein: plus hinauf, minus hinunter. '
            'b schiebt nur senkrecht.',
            f(r'y = \fa{2}x \fb{- 2}', 300, 70),
            n('@\\fb{b}@ schiebt senkrecht —|plus hinauf, minus hinunter', 440, 'orange'),
            graf(W_MB, [ger(2, 0, 5, gestrichelt=True), bew([[0.9, 2, 3], [3.8, 2, -2]], yachse={'farbe': 2})])),
         sz('m kippt',
            'Jetzt m, die Steigung. Aus zwei wird null Komma fünf: Die Gerade wird flacher. '
            'Fest bleibt dabei nur ein Punkt — der auf der y-Achse.',
            f(r'y = \fa{0.5}x + \fb{1}', 300, 70),
            n('@\\fa{m}@ kippt die Gerade|um den Punkt @(0 \\mid \\fb{b})@', 440, 'blau'),
            graf(W_MB, [ger(2, 1, 5, gestrichelt=True), bew([[0.9, 2, 1], [3.8, 0.5, 1]], yachse={'farbe': 2}, dreieck=dreieck(1, 1))])),
         sz('m wird negativ',
            'Ein negatives m lässt die Gerade fallen. Bei minus eins Komma fünf geht es pro Schritt nach rechts '
            'um eins Komma fünf hinunter. Der Drehpunkt bleibt null und eins.',
            f(r'y = \fa{-1.5}x + \fb{1}', 300, 70),
            n('@\\fa{m} \\gt 0@: steigt; @\\fa{m} \\lt 0@: fällt|@\\fa{m} = 0@: waagrecht', 440, 'blau'),
            graf(W_MB, [ger(0.5, 1, 5, gestrichelt=True),
                        bew([[0.9, 0.5, 1], [2.6, 0, 1], [4.6, -1.5, 1]], yachse={'farbe': 2}, dreieck=dreieck(1, 1))])),
         sz('m als Schritt',
            'So liest man m am Graphen: einen Schritt nach rechts, dann m Schritte hinauf. '
            'Bei m gleich zwei führt das von null, eins nach eins, drei.',
            f(r'y = \fa{2}x + \fb{1}', 300, 70),
            n('1 nach rechts,|@\\fa{2}@ hinauf', 440, 'blau'),
            graf(W_MB, [bew([[0, 2, 1]], yachse={'farbe': 2, 'beschriftung': False}, dreieck=dreieck(0, 1))],
                 [pt(1, 3, 5, '(1 | 3)'), pt(0, 1, 2, '(0 | 1)', [-0.3, 1.45], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: b ist der Wert bei x gleich null und schiebt die Gerade senkrecht. '
            'm ist der Zuwachs pro Schritt nach rechts und kippt sie um den Punkt null, b. '
            'Positives m steigt, negatives fällt, m gleich null bleibt waagrecht.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 420, 66, ein=0.4),
            n('@\\fb{b}@: Wert bei @x = 0@, schiebt senkrecht|@\\fa{m}@: Zuwachs pro Schritt nach rechts,|kippt um @(0 \\mid \\fb{b})@',
              560, 'blau', 44, ein=1.2),
            graf(W_MB, [bew([[1.0, 2, 1], [3.4, -1, 1], [6.0, 2, 1]], yachse={'farbe': 2},
                            dreieck=dreieck(1, 1))])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-m-und-b', 'Gerade sehen: Kontrollfragen zu m und b',
     'Fünf Vorhersagen zu Steigung und y-Achsenabschnitt: Der Clip hält an, fragt und löst dann in Bewegung auf.',
     ['Steigung', 'y-Achsenabschnitt', 'Gerade', 'Kontrollfragen'], [
         # Frage 1 zum Tippen: Beim Fragen steht die Ursprungsgerade y = 0.5x im Bild;
         # die gesuchte Stelle (0 | −2) erreicht sie erst nach der Antwort.
         sz('Frage 1',
            'Bei x gleich null bleibt nur b übrig: minus zwei. Dort schneidet die Gerade die y-Achse.',
            f(r'y = \fa{0.5}x \fb{- 2}', 300, 70, ein=1.0),
            n('@f(0) = \\fb{b} = \\fb{-2}@', 440, 'orange', ein=2.4),
            graf(W_MB, [bew([[0.9, 0.5, 0], [3.4, 0.5, -2]], yachse={'farbe': 2})])),
         sz('Frage 2',
            'Gleiches m heisst gleiche Richtung: Die beiden sind parallel. Und weil b von plus eins auf minus vier '
            'fällt, liegt die zweite Gerade fünf tiefer.',
            f(r'y = \fa{3}x \fb{+ 1} \qquad y = \fa{3}x \fb{- 4}', 300, 52, ein=1.0),
            n('gleiches @\\fa{m}@, verschiedenes @\\fb{b}@:|parallel, 5 tiefer', 440, 'blau', ein=2.6),
            graf(dict(xbereich=[-4, 5], ybereich=[-7, 2], yteilung=[[-5, '−5'], [0, '0']]),
                 [ger(3, 1), bew([[1.0, 0, 1], [3.6, 3, -4]], yachse={'farbe': 2})],
                 [pt(0, 1, 2)])),
         sz('Frage 3',
            'Die Gerade schneidet die y-Achse bei drei, also b gleich drei. Und pro Schritt nach rechts geht es '
            'eins hinunter: m gleich minus eins. Also y gleich minus x plus drei.',
            f(r'y = \fa{-}x + \fb{3}', 300, 70, ein=1.6),
            n('erst @\\fb{b}@ ablesen,|dann @\\fa{m}@ über ein Dreieck', 440, 'blau', ein=2.8),
            graf(W_MB, [bew([[0, -1, 3]], yachse={'farbe': 2, 'beschriftung': False},
                            dreieck=dreieck(None, None, [[1.8, 1, 1], [3.4, 1, 1]]))])),
         sz('Frage 4',
            'Einsetzen entscheidet: f von eins ist minus zwei plus fünf, also drei. Der Punkt eins, drei liegt '
            'auf dem Graphen — eins, sieben und drei, eins liegen daneben.',
            f(r'f(1) = \fa{-2} \cdot 1 + \fb{5} = 3', 300, 60, ein=1.0),
            n('Punktprobe: @x@ einsetzen,|Ergebnis mit @y@ vergleichen', 440, 'blau', ein=2.8),
            graf(dict(xbereich=[-2, 7], ybereich=[-1, 8]),
                 [bew([[1.0, -2, 9], [3.4, -2, 5]], yachse={'farbe': 2, 'beschriftung': False})],
                 [pt(1, 3, 3, '(1 | 3)'), pt(1, 7, 4, '(1 | 7)'), pt(3, 1, 4, '(3 | 1)')])),
         sz('Frage 5',
            'Pro Schritt nach rechts zwei hinunter heisst m gleich minus zwei. Durch null, minus eins heisst '
            'b gleich minus eins. Also y gleich minus zwei x minus eins.',
            f(r'y = \fa{-2}x \fb{- 1}', 300, 70, ein=1.0),
            n('«fällt um 2 pro Schritt» @\\Longrightarrow \\fa{m} = -2@|«durch @(0 \\mid -1)@» @\\Longrightarrow \\fb{b} = -1@',
              440, 'blau', ein=2.6),
            graf(W_MB, [bew([[0.9, 0, -1], [3.6, -2, -1]], yachse={'farbe': 2, 'beschriftung': False}, dreieck=dreieck(0, 1))],
                 [pt(0, -1, 2, '(0 | −1)', [-0.3, -1.5], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: b liest man direkt auf der y-Achse ab, m über einen Schritt nach rechts. '
            'Gleiches m heisst parallel, solange b verschieden ist — bei gleichem b ist es dieselbe Gerade. '
            'Und ob ein Punkt auf der Geraden liegt, entscheidet nur das Einsetzen.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 420, 66, ein=0.4),
            n('@\\fb{b}@: auf der @y@-Achse ablesen|@\\fa{m}@: 1 nach rechts, @\\fa{m}@ hinauf|gleiches @\\fa{m}@, anderes @\\fb{b}@: parallel',
              560, 'blau', 44, ein=1.2),
            graf(W_MB, [bew([[0, -2, -1]], yachse={'farbe': 2}, dreieck=dreieck(0, 1))])),
     ], [
         klick('Frage 1', 'y = 0.5x − 2: Tipp den Schnittpunkt mit der y-Achse ins Bild.',
               [0, -2], 'Getroffen: (0 | −2).',
               [{'bei': [0, 2], 'text': 'Die Höhe stimmt, das Vorzeichen nicht. Welches Zeichen steht vor der 2?',
                 'sprich': 'Die Höhe stimmt, das Vorzeichen nicht. Welches Zeichen steht vor der zwei?'},
                {'bei': [4, 0], 'text': 'Das ist der Schnittpunkt mit der x-Achse. Gefragt ist die y-Achse.',
                 'sprich': 'Das ist der Schnittpunkt mit der x-Achse. Gefragt ist die y-Achse.'},
                {'bei': [0, 0.5], 'text': 'Das ist die Steigung. Was bleibt übrig, wenn du x = 0 einsetzt?',
                 'sprich': 'Das ist die Steigung. Was bleibt übrig, wenn du x gleich null einsetzt?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — setz x = 0 ein, dann bleibt nur b.',
               sprich='y gleich null Komma fünf x minus zwei: Tipp den Schnittpunkt mit der y-Achse ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Setz x gleich null ein, dann bleibt nur b.'),
         wahl('Frage 2', 'y = 3x + 1 und y = 3x − 4: Wie liegen die beiden Geraden zueinander?',
              ['parallel, die zweite 5 tiefer', 'senkrecht', 'sie schneiden sich bei x = 1'], 0,
              {0: 'Ja.',
               1: 'Senkrecht wäre etwas mit den Steigungen. Vergleich sie: beide 3.',
               2: 'Schau nur auf die Steigungen — und überleg, ob sich zwei Geraden mit gleicher Richtung treffen können.'},
              sprich='y gleich drei x plus eins und y gleich drei x minus vier: Wie liegen die beiden Geraden zueinander?',
              rueck_sprich={1: 'Senkrecht wäre etwas mit den Steigungen. Vergleich sie: beide drei.',
                            2: 'Schau nur auf die Steigungen. Und überleg, ob sich zwei Geraden mit gleicher Richtung treffen können.'}),
         wahl('Frage 3', 'Welche Gleichung gehört zur Geraden im Bild?',
              ['y = −x + 3', 'y = x + 3', 'y = −3x + 1'], 0,
              {0: 'Ja.',
               1: 'Die zweite Zahl stimmt. Aber steigt die Gerade im Bild, oder fällt sie?',
               2: 'Vergleich beide Zahlen mit dem Bild: Wo schneidet die Gerade die y-Achse?'},
              rueck_sprich={1: 'Die zweite Zahl stimmt. Aber steigt die Gerade im Bild, oder fällt sie?',
                            2: 'Vergleich beide Zahlen mit dem Bild: Wo schneidet die Gerade die y-Achse?'}),
         wahl('Frage 4', 'f(x) = −2x + 5: Welcher Punkt liegt auf dem Graphen?',
              ['(1 | 3)', '(1 | 7)', '(3 | 1)'], 0,
              {0: 'Ja.',
               1: 'Rechne f(1) nochmals — welches Vorzeichen hat −2 · 1?',
               2: 'Setz die erste Zahl für x ein und vergleich das Ergebnis mit der zweiten.'},
              sprich='f von x gleich minus zwei x plus fünf: Welcher Punkt liegt auf dem Graphen?',
              rueck_sprich={1: 'Rechne f von eins nochmals. Welches Vorzeichen hat minus zwei mal eins?',
                            2: 'Setz die erste Zahl für x ein und vergleich das Ergebnis mit der zweiten.'}),
         wahl('Frage 5', 'Eine Gerade geht durch (0 | −1) und fällt pro Schritt nach rechts um 2. Welche Gleichung?',
              ['y = −2x − 1', 'y = 2x − 1', 'y = −2x + 1'], 0,
              {0: 'Ja.',
               1: 'Die Gerade fällt. Welches Vorzeichen hat m dann?',
               2: 'Die Steigung stimmt. Vergleich jetzt die zweite Zahl mit dem gegebenen Punkt auf der y-Achse.'},
              sprich='Eine Gerade geht durch null, minus eins und fällt pro Schritt nach rechts um zwei. Welche Gleichung?',
              rueck_sprich={1: 'Die Gerade fällt. Welches Vorzeichen hat m dann?',
                            2: 'Die Steigung stimmt. Vergleich jetzt die zweite Zahl mit dem gegebenen Punkt auf der y-Achse.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
clip('steigungsdreieck', 'Gerade sehen: jedes Steigungsdreieck gibt dasselbe m',
     'Die Steigung als Verhältnis Δy zu Δx — gleich bei jedem Dreieck, und was bei Δx null passiert.',
     ['Steigung', 'Steigungsdreieck', 'Delta', 'Nullstelle', 'Gerade'], [
         sz('Zwei Punkte',
            'Auf dieser Geraden liegen die Punkte null, eins und fünf, fünf. Wie steil ist sie?',
            titel('Wie steil?', 300, 86),
            graf(W_DREI, [ger(0.8, 1)], [pt(0, 1, 5, 'P(0 | 1)'), pt(5, 5, 5, 'Q(5 | 5)')])),
         sz('Grosses Dreieck',
            'Von P nach Q sind es fünf nach rechts und vier hinauf. Die Steigung ist vier geteilt durch fünf, '
            'also null Komma acht.',
            f(r'\fa{m} = \dfrac{\Delta y}{\Delta x} = \dfrac{4}{5} = \fa{0.8}', 300, 62),
            n('@\\Delta x = 5@ nach rechts|@\\Delta y = 4@ hinauf', 460, 'blau'),
            graf(W_DREI, [bew([[0, 0.8, 1]], dreieck=dreieck(None, None, [[1.2, 0, 0], [3.6, 0, 5]]))],
                 [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')])),
         sz('Kleines Dreieck',
            'Jetzt ein kleineres Dreieck auf derselben Geraden — schau zu, wie es schrumpft. '
            'Zwei Komma fünf nach rechts, zwei hinauf. Zwei geteilt durch zwei Komma fünf — wieder null Komma acht.',
            f(r'\fa{m} = \dfrac{2}{2.5} = \fa{0.8}', 300, 62),
            n('anderes Dreieck,|dasselbe @\\fa{m}@ — bei @\\fa{m} \\neq 0@ sind sie ähnlich', 460, 'blau'),
            graf(W_DREI, [bew([[0, 0.8, 1]], dreieck=dreieck(None, None, [[1.4, 0, 5], [4.6, 0, 2.5]]))],
                 [pt(0, 1, 5, 'P')])),
         sz('Die Formel',
            'Allgemein: m ist y zwei minus y eins, geteilt durch x zwei minus x eins. '
            'Immer der Unterschied der Höhen durch den Unterschied der Stellen.',
            f(r'\fa{m} = \dfrac{y_2 - y_1}{x_2 - x_1}', 300, 66),
            n('Höhenunterschied|durch Stellenunterschied', 460, 'blau'),
            graf(W_DREI, [bew([[0, 0.8, 1]], dreieck=dreieck(0, 5))],
                 [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')])),
         sz('Ein Beispiel',
            'Ein Beispiel mit negativer Steigung: A liegt bei minus eins und vier, B bei drei und minus zwei. '
            'Minus zwei minus vier ist minus sechs, geteilt durch vier: m gleich minus eins Komma fünf.',
            f(r'\fa{m} = \dfrac{-2 - 4}{3 - (-1)} = \dfrac{-6}{4} = \fa{-1.5}', 300, 56),
            n('Die Gerade fällt:|@\\fa{m} \\lt 0@', 460, 'blau'),
            graf(W_GL, [bew([[0, -1.5, 2.5]], dreieck=dreieck(None, None, [[1.6, -1, 0], [4.2, -1, 4]]))],
                 [pt(-1, 4, 5, 'A(−1 | 4)'), pt(3, -2, 5, 'B(3 | −2)')])),
         sz('Leserichtung',
            'Am bequemsten liest man von links nach rechts, mit Delta x grösser als null. '
            'Wer die Punkte vertauscht, dreht beide Unterschiede — und erhält dasselbe m.',
            f(r'\dfrac{4 - (-2)}{-1 - 3} = \dfrac{6}{-4} = \fa{-1.5}', 300, 56),
            n('Punkte vertauscht:|beide Vorzeichen drehen,|@\\fa{m}@ bleibt gleich', 460, 'blau'),
            # Δx > 0 (1.2–3.6 s): das Dreieck waechst von A nach rechts; «vertauscht» (ab 4.7 s):
            # es zieht sich auf B zurueck und waechst von B nach links (Δx = −4, Δy = 6).
            graf(W_GL, [bew([[0, -1.5, 2.5]], dreieck=dreieck(None, None, [[1.2, -1, 0], [3.6, -1, 4], [4.0, -1, 4],
                                                                            [5.0, 3, 0], [7.6, 3, -4]]))],
                 [pt(-1, 4, 5, 'A'), pt(3, -2, 5, 'B')])),
         sz('Die Nullstelle',
            'Und noch eine Stelle lohnt den Blick: die Nullstelle. Dort schneidet die Gerade die x-Achse, '
            'dort ist y gleich null. Null gleich zwei x minus sechs gibt zwei x gleich sechs, also x gleich drei. '
            'Der Achsenabschnitt minus sechs liegt ganz woanders.',
            f(r'0 = \fa{2}x \fb{- 6} \;\Longrightarrow\; \fa{2}x = 6 \;\Longrightarrow\; x_0 = \fc{3}', 300, 44),
            n('kurz: @x_0 = -\\dfrac{\\fb{b}}{\\fa{m}}@, falls @\\fa{m} \\neq 0@|nicht verwechseln mit @\\fb{b}@',
              470, 'gruen'),
            graf(W_NULL, [bew([[0, 2, -6]], yachse={'farbe': 2}, nullstelle={'farbe': 3})])),
         sz('Delta x null',
            'Ein Fall bleibt übrig: zwei verschiedene Punkte mit derselben x-Koordinate. Dann ist Delta x null — '
            'und durch null lässt sich nicht teilen. Die Gerade durch diese Punkte steht senkrecht, '
            'sie hat keine Steigung und ist keine Funktion.',
            f(r'\Delta x = 0 \quad\Longrightarrow\quad \dfrac{\Delta y}{0}', 300, 60),
            n('@\\fd{m}@ ist nicht definiert.|Eine senkrechte Gerade|ist keine Funktion.', 460, 'rot'),
            graf(W_GL, punkte=[pt(2, -1, 4, '(2 | −1)'), pt(2, 3, 4, '(2 | 3)')], ein=2.0),
            ueber(W_GL, punkte=[pt(2, -1, 4), pt(2, 3, 4)], ein=8.0,
                  figuren=[{'art': 'strecke', 'von': [2, -4], 'bis': [2, 5], 'farbe': 4}])),
         sz('Merke',
            'Zum Mitnehmen: m ist hinauf geteilt durch nach rechts. Jedes Steigungsdreieck derselben Geraden '
            'gibt dasselbe m, weil die Dreiecke ähnlich sind. Und die Nullstelle ist minus b durch m, '
            'solange m nicht null ist.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fa{m} = \dfrac{\Delta y}{\Delta x} \qquad x_0 = -\dfrac{\fb{b}}{\fa{m}} \ (\fa{m} \neq 0)', 420, 54, ein=0.4),
            n('jedes Dreieck derselben Geraden:|dasselbe @\\fa{m}@|@\\Delta x = 0@: keine Steigung',
              560, 'blau', 44, ein=1.2),
            graf(W_DREI, [bew([[0, 0.8, 1]], dreieck=dreieck(None, None, [[1.0, 0, 5], [3.4, 0, 2.5], [5.8, 0, 5]]))],
                 [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')]),
            # x₀ = −b/m = −1/0.8 = −1.25; fester Punkt statt Begleiter, dessen Live-Zahl
            # eine Stelle hat («−1.2»). Beschriftung links über der Geraden, wo sie frei ist.
            ueber(W_DREI, punkte=[pt(-1.25, 0, 3, 'x₀', [-1.35, 0.3], 'end')], ein=8.0)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-steigung', 'Gerade sehen: Kontrollfragen zur Steigung',
     'Fünf Vorhersagen zu Δy durch Δx, zur Nullstelle und zum Fall Δx gleich null.',
     ['Steigung', 'Steigungsdreieck', 'Nullstelle', 'Kontrollfragen'], [
         sz('Frage 1',
            'Sieben minus minus eins ist acht, zwei minus minus zwei ist vier. Acht geteilt durch vier ist zwei.',
            f(r'\fa{m} = \dfrac{7 - (-1)}{2 - (-2)} = \dfrac{8}{4} = \fa{2}', 300, 54, ein=1.0),
            n('Höhenunterschied|durch Stellenunterschied', 460, 'blau', ein=2.6),
            graf(W_TAB, [bew([[1.0, 0, 3], [3.4, 2, 3]], dreieck=dreieck(None, None, [[3.6, -2, 0], [5.4, -2, 4]]))],
                 [pt(-2, -1, 5, 'A(−2 | −1)', [-2.3, -1.9], 'end'), pt(2, 7, 5, 'B(2 | 7)')])),
         sz('Frage 2',
            'Minus fünf minus drei ist minus acht. Zwei minus minus zwei ist vier. Minus acht durch vier '
            'ist minus zwei.',
            f(r'\fa{m} = \dfrac{-5 - 3}{2 - (-2)} = \dfrac{-8}{4} = \fa{-2}', 300, 54, ein=1.0),
            n('Beide Klammern sorgfältig:|minus minus zwei ist plus zwei', 460, 'blau', ein=2.6),
            graf(dict(xbereich=[-4, 5], ybereich=[-6, 3], yteilung=[[-5, '−5'], [0, '0']]),
                 [bew([[1.2, 0, 3], [3.6, -2, -1]], dreieck=dreieck(None, None, [[3.8, -2, 0], [5.6, -2, 4]]))],
                 [pt(-2, 3, 5, 'P(−2 | 3)'), pt(2, -5, 5, 'Q(2 | −5)')])),
         # Frage 3 zum Tippen: Beim Fragen steht die Ursprungsgerade y = 1.5x im Bild.
         sz('Frage 3',
            'Null gleich eins Komma fünf x minus sechs gibt eins Komma fünf x gleich sechs, also x gleich vier. '
            'Dort schneidet die Gerade die x-Achse.',
            f(r'0 = \fa{1.5}x \fb{- 6} \;\Longrightarrow\; \fa{1.5}x = 6 \;\Longrightarrow\; x_0 = \fc{4}', 300, 44, ein=1.2),
            n('kurz: @x_0 = -\\dfrac{\\fb{b}}{\\fa{m}} = -\\dfrac{-6}{1.5} = \\fc{4}@', 470, 'gruen', ein=2.8),
            graf(W_NULL, [bew([[0.9, 1.5, 0], [3.4, 1.5, -6]], yachse={'farbe': 2}, nullstelle={'farbe': 3})])),
         sz('Frage 4',
            'Die Gerade schneidet die y-Achse bei zwei und die x-Achse bei vier. Vier nach rechts, zwei hinunter: '
            'm gleich minus zwei geteilt durch vier, also minus null Komma fünf.',
            f(r'\fa{m} = \dfrac{-2}{4} = \fa{-0.5}', 300, 62, ein=1.6),
            n('4 nach rechts, 2 hinunter', 460, 'blau', ein=2.8),
            graf(W_DREI, [bew([[0, -0.5, 2]], yachse={'farbe': 2, 'beschriftung': False},
                              dreieck=dreieck(None, None, [[1.8, 0, 4], [3.4, 0, 4]]))])),
         sz('Frage 5',
            'Dieselbe x-Koordinate heisst Delta x gleich null. Teilen durch null geht nicht: m ist nicht definiert, '
            'und die Gerade durch diese Punkte steht senkrecht.',
            f(r'\Delta x = 0: \quad \dfrac{\Delta y}{0}', 300, 60, ein=1.0),
            n('@\\fd{m}@ ist nicht definiert —|die Gerade steht senkrecht', 460, 'rot', ein=2.4),
            graf(W_GL, punkte=leiter(-1, -4, 5), ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: erst die Höhen abziehen, dann die Stellen, dann teilen. Die Nullstelle ist minus b '
            'durch m, solange m nicht null ist — und der y-Achsenabschnitt ist etwas anderes. '
            'Bei Delta x gleich null gibt es keine Steigung.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fa{m} = \dfrac{y_2 - y_1}{x_2 - x_1}', 390, 50, ein=0.4),
            f(r'x_0 = -\dfrac{\fb{b}}{\fa{m}} \quad (\fa{m} \neq 0)', 520, 50, ein=0.7),
            n('@\\fc{x_0}@: Schnitt mit der @x@-Achse|@\\fb{b}@: Schnitt mit der @y@-Achse|@\\fd{\\Delta x = 0}@: kein @\\fa{m}@',
              660, 'blau', 42, ein=1.2),
            graf(W_DREI, [bew([[0, -0.5, 2]], yachse={'farbe': 2}, nullstelle={'farbe': 3})])),
     ], [
         wahl('Frage 1', 'A(−2 | −1) und B(2 | 7): Wie gross ist die Steigung m?',
              ['2', '8', '0.5'], 0,
              {0: 'Ja.',
               1: 'Das ist nur der Höhenunterschied Δy. Was fehlt im Bruch noch?',
               2: 'Vergleich, was oben und was unten im Bruch steht.'},
              sprich='A minus zwei, minus eins und B zwei, sieben: Wie gross ist die Steigung m?',
              rueck_sprich={1: 'Das ist nur der Höhenunterschied delta y. Was fehlt im Bruch noch?',
                            2: 'Vergleich, was oben und was unten im Bruch steht.'}),
         wahl('Frage 2', 'P(−2 | 3) und Q(2 | −5): Wie gross ist m?',
              ['−2', '2', '−8'], 0,
              {0: 'Ja.',
               1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
               2: 'Das ist Δy. Was fehlt im Bruch noch — und wie gross ist Δx bei −2 und 2?'},
              sprich='P minus zwei, drei und Q zwei, minus fünf: Wie gross ist m?',
              rueck_sprich={1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
                            2: 'Das ist delta y. Was fehlt im Bruch noch, und wie gross ist delta x bei minus zwei und zwei?'}),
         klick('Frage 3', 'f(x) = 1.5x − 6: Tipp die Nullstelle ins Bild.',
               [4, 0], 'Getroffen: (4 | 0).',
               [{'bei': [0, -6], 'text': 'Das wäre der y-Achsenabschnitt. Auf welcher Achse liegt die Nullstelle?',
                 'sprich': 'Das wäre der y-Achsenabschnitt. Auf welcher Achse liegt die Nullstelle?'},
                {'bei': [1.5, 0], 'text': 'Das ist die Steigung. Setz y = 0 und löse nach x auf.',
                 'sprich': 'Das ist die Steigung. Setz y gleich null und löse nach x auf.'},
                {'bei': [0, 0], 'text': 'Der Ursprung ist es nur, wenn b = 0 ist. Hier steht −6.',
                 'sprich': 'Der Ursprung ist es nur, wenn b gleich null ist. Hier steht minus sechs.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — setz y = 0 und löse nach x auf.',
               sprich='f von x gleich eins Komma fünf x minus sechs: Tipp die Nullstelle ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Setz y gleich null und löse nach x auf.'),
         wahl('Frage 4', 'Wie gross ist die Steigung der Geraden im Bild?',
              ['−0.5', '0.5', '−2'], 0,
              {0: 'Ja.',
               1: 'Der Betrag stimmt. Aber steigt die Gerade, oder fällt sie?',
               2: 'Zähl noch einmal: wie weit nach rechts, wie weit hinunter — und was kommt in den Nenner?'},
              rueck_sprich={1: 'Der Betrag stimmt. Aber steigt die Gerade, oder fällt sie?',
                            2: 'Zähl noch einmal: wie weit nach rechts, wie weit hinunter. Und was kommt in den Nenner?'}),
         wahl('Frage 5', 'Zwei Punkte haben dieselbe x-Koordinate. Was folgt für m?',
              ['m ist nicht definiert', 'm = 0', 'm = 1'], 0,
              {0: 'Ja.',
               1: 'Das wäre bei gleicher y-Koordinate so. Was ist hier gleich, Δx oder Δy?',
               2: 'Schreib Δy durch Δx hin und setz Δx = 0 ein.'},
              sprich='Zwei Punkte haben dieselbe x-Koordinate. Was folgt für m?',
              rueck_sprich={1: 'Das wäre bei gleicher y-Koordinate so. Was ist hier gleich, delta x oder delta y?',
                            2: 'Schreib delta y durch delta x hin und setz delta x gleich null ein.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
clip('typen', 'Gerade sehen: Typen und Lagebeziehungen',
     'Proportional, Identität, konstant, senkrecht — und wann zwei Geraden parallel oder senkrecht sind.',
     ['proportionale Funktion', 'Identität', 'konstante Funktion', 'parallel', 'senkrecht'], [
         sz('Vier Typen',
            'Vier Fälle lohnen einen genauen Blick. Drei davon unterscheiden sich nur in m und b — '
            'und einer fällt aus der Reihe: Er ist gar keine Funktion.',
            titel('Vier Fälle', 300, 86),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 470, 66),
            graf(W_GL, [bew([[0, 1.5, -2]], yachse={'farbe': 2})])),
         sz('Proportional',
            'Erster Fall: b gleich null. Dann geht die Gerade durch den Ursprung, und doppeltes x gibt '
            'doppeltes f von x. Das ist eine proportionale Funktion.',
            f(r'f(x) = \fa{1.5}\,x \qquad (\fb{b} = 0)', 300, 58),
            n('proportional:|durch den Ursprung', 460, 'orange'),
            graf(W_GL, [ger(1.5, -2, 5, gestrichelt=True),
                        bew([[0.9, 1.5, -2], [3.8, 1.5, 0]], yachse={'farbe': 2})]),
            ueber(W_GL, [dict(bew([[0, 1.5, 0]]), marken=[{'x': 1, 'text': 'f(1) = {y}', 'farbe': 5},
                                                          {'x': 2, 'text': 'f(2) = {y}', 'farbe': 5}])], ein=4.2)),
         sz('Identität',
            'Mit m gleich eins wird daraus die Identität: Jeder x-Wert wird auf sich selbst abgebildet. '
            'Ihre Gerade halbiert den Winkel zwischen der positiven x-Achse und der positiven y-Achse.',
            f(r'f(x) = x \qquad (\fa{m} = 1,\ \fb{b} = 0)', 300, 52),
            n('Identität:|@x \\longmapsto x@', 460, 'blau'),
            graf(W_GL, [ger(1.5, 0, 5, gestrichelt=True), bew([[0.9, 1.5, 0], [3.8, 1, 0]])],
                 [pt(2, 2, 5, '(2 | 2)'), pt(-1, -1, 5, '(−1 | −1)')]),
            ueber(W_GL, ein=5.6, figuren=[
                {'art': 'winkel', 'bei': [0, 0], 'von': 0, 'bis': 45, 'r_px': 72, 'farbe': 5},
                {'art': 'winkel', 'bei': [0, 0], 'von': 45, 'bis': 90, 'r_px': 72, 'farbe': 5},
                {'art': 'text', 'bei': [1.25, 0.42], 'text': '45°', 'farbe': 5, 'kursiv': False, 'groesse': 26},
                {'art': 'text', 'bei': [0.40, 1.22], 'text': '45°', 'farbe': 5, 'kursiv': False, 'groesse': 26}])),
         sz('Konstant',
            'Dritter Fall: m gleich null. Dann fällt der x-Teil weg, und übrig bleibt b. '
            'Der Graph ist eine waagrechte Gerade — die konstante Funktion.',
            f(r'f(x) = \fb{3} \qquad (\fa{m} = 0)', 300, 58),
            n('konstant:|waagrecht, @\\fa{m} = 0@', 460, 'blau'),
            graf(W_GL, [ger(1, 0, 5, gestrichelt=True),
                        bew([[0.9, 1, 0], [2.8, 0, 0], [4.6, 0, 3]], yachse={'farbe': 2})])),
         sz('Senkrecht',
            'Und der Fall, der keine Funktion ist: x gleich drei. Zur Stelle drei gehören unendlich viele y-Werte. '
            'Eine Funktion darf jedem x nur einen Wert zuordnen — darum ist das keine.',
            f(r'x = 3', 300, 70),
            n('@\\fd{keine\\ Funktion}@:|einem @x@ unendlich viele @y@', 460, 'rot'),
            graf(W_GL, punkte=leiter(3, -4, 5))),
         sz('Parallel',
            'Zwei Geraden mit gleichem m zeigen in dieselbe Richtung. Ist ihr b verschieden, sind sie '
            'parallel und treffen sich nie; ist auch b gleich, ist es dieselbe Gerade.',
            f(r'y = \fa{2}x \fb{+ 1} \qquad y = \fa{2}x \fb{- 3}', 300, 50),
            n('parallel:|@\\fa{m_1} = \\fa{m_2}@, @\\fb{b_1} \\neq \\fb{b_2}@', 460, 'blau'),
            graf(W_GL, [ger(2, 1), bew([[0.9, 2, 4], [3.8, 2, -3]], yachse={'farbe': 2})],
                 [pt(0, 1, 2)])),
         sz('Senkrecht zueinander',
            'Senkrecht ist überraschender: Das Produkt der beiden Steigungen ist minus eins. '
            'Zu m gleich zwei gehört also minus ein Halb. Schau, wie die zweite Gerade einrastet.',
            f(r'\fa{2} \cdot \fa{(-0.5)} = -1', 300, 62),
            n('senkrecht:|@\\fa{m_1} \\cdot \\fa{m_2} = -1@', 460, 'blau'),
            graf(W_GL, [ger(2, 1), bew([[5.0, 2, 1], [8.4, -0.5, 1]])],
                 [pt(0, 1, 5, '(0 | 1)')])),
         sz('Warum minus eins',
            'Der Grund steckt im Steigungsdreieck. Bei der ersten Geraden: eins nach rechts, zwei hinauf. '
            'Dreht man das Dreieck um neunzig Grad, tauschen hinauf und nach rechts die Rolle, und ein '
            'Vorzeichen kippt: aus zwei zu eins wird minus eins zu zwei.',
            f(r'\dfrac{2}{1} \;\longrightarrow\; \dfrac{-1}{2} = \fa{-0.5}', 300, 58),
            n('Dreieck um @90^\\circ@ gedreht:|@\\Delta x@ und @\\Delta y@ tauschen,|ein Vorzeichen kippt', 460, 'blau'),
            # Beide Dreiecke mit Abstand zu (0 | 1), wo sich die Geraden kreuzen: das erste bei
            # x = 1 (von (1 | 3) nach (2 | 5)), das zweite bei x = −3.5 (von (−3.5 | 2.75) nach (−1.5 | 1.75)).
            graf(W_GL, [bew([[0, 2, 1]], dreieck=dreieck(1, 1)),
                        bew([[0, -0.5, 1]], dreieck=dreieck(None, None, [[7.0, -3.5, 0], [10.8, -3.5, 2]]))],
                 [pt(0, 1, 5)])),
         sz('Merke',
            'Zum Mitnehmen: proportional heisst b gleich null, die Identität hat zusätzlich m gleich eins, '
            'konstant heisst m gleich null. Eine senkrechte Gerade ist keine Funktion. '
            'Parallel heisst gleiches m, senkrecht heisst Produkt der Steigungen minus eins.',
            titel('Zum Mitnehmen', 240, 76),
            f(r'\fb{b} = 0:\ \text{proportional}', 380, 48, ein=0.4),
            f(r'\fa{m} = 0:\ \text{konstant}', 460, 48, ein=0.7),
            n('@\\fa{m_1} = \\fa{m_2}@: parallel|@\\fa{m_1} \\cdot \\fa{m_2} = -1@: senkrecht|@x = k@: keine Funktion',
              570, 'blau', 44, ein=1.4),
            graf(W_GL, [ger(2, 1), bew([[0.9, 2, 1], [3.8, -0.5, 1]])], [pt(0, 1, 5)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-typen', 'Gerade sehen: Kontrollfragen zu Typen und Lage',
     'Fünf Vorhersagen zu proportional, konstant, senkrechter Gerade, parallel und senkrecht.',
     ['proportionale Funktion', 'konstante Funktion', 'parallel', 'senkrecht', 'Kontrollfragen'], [
         sz('Frage 1',
            'b ist null, also geht die Gerade durch den Ursprung: eine proportionale Funktion. '
            'Negativ darf sie dabei sein — proportional sagt nur, dass b null ist.',
            f(r'f(x) = \fa{-0.5}\,x \qquad (\fb{b} = 0)', 300, 56, ein=1.0),
            n('proportional:|durch @(0 \\mid 0)@', 460, 'orange', ein=2.4),
            graf(W_GL, [bew([[0.9, -0.5, 3], [3.4, -0.5, 0]], yachse={'farbe': 2})])),
         sz('Frage 2',
            'x gleich vier ist eine senkrechte Gerade. Sie ordnet der einen Stelle vier unendlich viele y-Werte zu '
            'und ist darum keine Funktion.',
            f(r'x = 4', 300, 70, ein=1.0),
            n('senkrecht —|@\\fd{keine\\ Funktion}@', 460, 'rot', ein=2.2),
            graf(W_GL, punkte=leiter(4, -4, 5), ein=1.2)),
         sz('Frage 3',
            'Parallel heisst gleiche Steigung. Drei x minus drei hat dasselbe m gleich drei, aber ein anderes b.',
            f(r'y = \fa{3}x \fb{+ 2} \qquad y = \fa{3}x \fb{- 3}', 300, 50, ein=1.0),
            n('gleiches @\\fa{m}@,|verschiedenes @\\fb{b}@', 460, 'blau', ein=2.4),
            graf(W_GL, [ger(3, 2), bew([[1.0, 0, 2], [3.6, 3, -3]], yachse={'farbe': 2})],
                 [pt(0, 2, 2)])),
         # Frage 4 zum Tippen: g steht im Bild, die senkrechte Gerade kommt erst nach der Antwort.
         sz('Frage 4',
            'Senkrecht zu g heisst negativer Kehrwert: minus ein Viertel. Mit dem y-Achsenabschnitt eins lautet '
            'sie minus null Komma zwei fünf x plus eins. Null gleich minus null Komma zwei fünf x plus eins '
            'gibt x gleich vier.',
            f(r'\fa{m_2} = -\dfrac{1}{4}: \quad y = \fa{-0.25}x + \fb{1}', 300, 50, ein=1.4),
            n('erst der negative Kehrwert,|dann @y = 0@ setzen', 460, 'blau', ein=3.2),
            graf(W_GL, [ger(4, -1), bew([[1.4, -0.25, 5], [3.8, -0.25, 1]], nullstelle={'farbe': 3})])),
         sz('Frage 5',
            'Null Komma fünf mal minus zwei ist minus eins. Die beiden Geraden stehen senkrecht aufeinander.',
            f(r'\fa{0.5} \cdot \fa{(-2)} = -1', 300, 62, ein=1.6),
            n('Produkt der Steigungen|ist @-1@: senkrecht', 460, 'blau', ein=2.8),
            graf(W_GL, [ger(0.5, 2), ger(-2, -1)], [pt(0, 2, 2), pt(0, -1, 2)])),
         sz('Merke',
            'Zum Mitnehmen: b gleich null heisst proportional, m gleich null heisst konstant. '
            'x gleich k ist keine Funktion. Gleiches m bei verschiedenem b heisst parallel, '
            'Produkt minus eins heisst senkrecht.',
            titel('Zum Mitnehmen', 240, 76),
            f(r'\fb{b} = 0:\ \text{proportional}', 380, 48, ein=0.4),
            f(r'\fa{m} = 0:\ \text{konstant}', 460, 48, ein=0.7),
            n('@\\fa{m_1} = \\fa{m_2}@: parallel|@\\fa{m_1} \\cdot \\fa{m_2} = -1@: senkrecht|@x = k@: keine Funktion',
              570, 'blau', 44, ein=1.4),
            graf(W_GL, [ger(0.5, 2), ger(-2, -1)], [pt(0, 2, 2), pt(0, -1, 2)])),
     ], [
         wahl('Frage 1', 'f(x) = −0.5x: Welcher Typ ist das?',
              ['eine proportionale Funktion', 'eine konstante Funktion', 'die Identität'], 0,
              {0: 'Ja.',
               1: 'Konstant wäre m = 0. Steht hier ein x in der Gleichung?',
               2: 'Die Identität ist f(x) = x. Vergleich die Steigungen.'},
              sprich='f von x gleich minus null Komma fünf x: Welcher Typ ist das?',
              rueck_sprich={1: 'Konstant wäre m gleich null. Steht hier ein x in der Gleichung?',
                            2: 'Die Identität ist f von x gleich x. Vergleich die Steigungen.'}),
         wahl('Frage 2', 'Was beschreibt x = 4?',
              ['eine senkrechte Gerade, keine Funktion', 'eine konstante Funktion',
               'die Nullstelle x₀ = 4 einer Geraden'], 0,
              {0: 'Ja.',
               1: 'Konstant ist y = 4 — waagrecht. Was ist hier festgelegt, die Stelle oder der Wert?',
               2: 'Eine Nullstelle ist eine einzelne Stelle auf der x-Achse. Wie viele Punkte erfüllen x = 4?'},
              sprich='Was beschreibt x gleich vier?',
              rueck_sprich={1: 'Konstant ist y gleich vier, waagrecht. Was ist hier festgelegt, die Stelle oder der Wert?',
                            2: 'Eine Nullstelle ist eine einzelne Stelle auf der x-Achse. Wie viele Punkte erfüllen x gleich vier?'}),
         wahl('Frage 3', 'g: y = 3x + 2. Welche Gerade ist parallel zu g?',
              ['y = 3x − 3', 'y = −3x + 2', 'y = 2x + 3'], 0,
              {0: 'Ja.',
               1: 'Dasselbe b, aber die Richtung ist gespiegelt. Woran erkennt man parallel?',
               2: 'Vergleich hier nur die Zahl vor dem x.'},
              sprich='g: y gleich drei x plus zwei. Welche Gerade ist parallel zu g?',
              rueck_sprich={1: 'Dasselbe b, aber die Richtung ist gespiegelt. Woran erkennt man parallel?',
                            2: 'Vergleich hier nur die Zahl vor dem x.'}),
         klick('Frage 4', 'g: y = 4x − 1 ist gezeichnet. Eine Gerade senkrecht zu g schneidet die y-Achse bei 1. '
                          'Tipp ihren Schnittpunkt mit der x-Achse ins Bild.',
               [4, 0], 'Getroffen: (4 | 0).',
               [{'bei': [-4, 0], 'text': 'Das Vorzeichen: Die senkrechte Gerade fällt und startet bei +1.',
                 'sprich': 'Das Vorzeichen: Die senkrechte Gerade fällt und startet bei plus eins.'},
                {'bei': [0.25, 0], 'text': 'Das ist der Kehrwert von \\(m_g = 4\\) — ohne das Minus. '
                                            'Senkrecht heisst \\(m_h = -\\tfrac14\\); gesucht ist aber die Nullstelle.',
                 'sprich': 'Das ist der Kehrwert von m g gleich vier, ohne das Minus. Senkrecht heisst '
                           'm h gleich minus ein Viertel. Gesucht ist aber die Nullstelle.'},
                {'bei': [0, 1], 'text': 'Das ist der y-Achsenabschnitt. Auf welcher Achse liegt der gesuchte Punkt?',
                 'sprich': 'Das ist der y-Achsenabschnitt. Auf welcher Achse liegt der gesuchte Punkt?'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — erst der negative Kehrwert, dann y = 0 setzen.',
               sprich='g: y gleich vier x minus eins ist gezeichnet. Eine Gerade senkrecht zu g schneidet die '
                      'y-Achse bei eins. Tipp ihren Schnittpunkt mit der x-Achse ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Erst der negative Kehrwert, '
                             'dann y gleich null setzen.'),
         wahl('Frage 5', 'Wie liegen die beiden Geraden im Bild zueinander?',
              ['senkrecht', 'parallel', 'identisch'], 0,
              {0: 'Ja.',
               1: 'Parallel wäre gleiche Richtung. Steigen beide, oder fällt eine?',
               2: 'Identisch wären sie nur als eine einzige Linie im Bild.'},
              rueck_sprich={1: 'Parallel wäre gleiche Richtung. Steigen beide, oder fällt eine?',
                            2: 'Identisch wären sie nur als eine einzige Linie im Bild.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
clip('aufstellen', 'Gerade sehen: die Geradengleichung aufstellen',
     'Aus Steigung und Punkt, aus zwei Punkten, aus einer Lagebeziehung — und aus einem Sachtext.',
     ['Geradengleichung', 'aufstellen', 'zwei Punkte', 'parallel', 'Sachaufgabe'], [
         sz('Der Ansatz',
            'Gesucht ist jetzt immer die Gleichung. Der Ansatz ist jedes Mal derselbe: y gleich m x plus b. '
            'Gegeben sind entweder m, oder b, oder Punkte — und was fehlt, wird ausgerechnet.',
            titel('Der Ansatz', 300, 86),
            f(r'y = \fa{m}\,x + \fb{b}', 470, 66),
            graf(W_GL, [bew([[0.8, 1, 2], [3.2, -1, -2], [5.8, 2, 1]], farbe=5, gestrichelt=True)],
                 [pt(2, -1, 5, 'P(2 | −1)')])),
         sz('m und ein Punkt',
            'Erster Fall: die Steigung minus zwei und der Punkt P zwei, minus eins. '
            'Das bekannte m kommt in den Ansatz. Offen bleibt nur b — die Gerade kann noch überall liegen.',
            f(r'y = \fa{-2}x + \fb{b}', 300, 70),
            n('@\\fa{m}@ einsetzen —|eine Unbekannte bleibt', 460, 'blau'),
            graf(W_GL, [bew([[0.8, -2, 7], [4.8, -2, -4]])], [pt(2, -1, 5, 'P(2 | −1)')])),
         sz('Punkt einsetzen',
            'Jetzt der Punkt: seine x-Koordinate für x, seine y-Koordinate für y. Minus eins gleich minus zwei '
            'mal zwei plus b — also b gleich drei. Damit rastet die Gerade auf P ein.',
            f(r'-1 = \fa{-2} \cdot 2 + \fb{b} \;\Longrightarrow\; \fb{b} = 3', 300, 52),
            n('Probe: @\\fa{-2} \\cdot 2 + \\fb{3} = -1@ ✓', 460, 'gruen', ein=10.9),
            graf(W_GL, [bew([[8.6, -2, -4], [10.9, -2, 3]], yachse={'farbe': 2})],
                 [pt(2, -1, 3, 'P(2 | −1)')])),
         sz('Zwei Punkte: erst m',
            'Zweiter Fall: zwei Punkte. A liegt bei minus zwei, minus zwei, B bei eins, vier. '
            'Zuerst die Steigung: vier minus minus zwei ist sechs, geteilt durch drei — m gleich zwei.',
            f(r'\fa{m} = \dfrac{4 - (-2)}{1 - (-2)} = \dfrac{6}{3} = \fa{2}', 300, 54),
            n('Schritt 1:|@\\fa{m}@ aus den beiden Punkten', 460, 'blau'),
            graf(W_GL, [bew([[0, 2, 2]], farbe=5, gestrichelt=True,
                            dreieck=dreieck(None, None, [[4.8, -2, 0], [7.6, -2, 3]]))],
                 [pt(-2, -2, 5, 'A(−2 | −2)'), pt(1, 4, 5, 'B(1 | 4)')])),
         sz('Zwei Punkte: dann b',
            'Dann b: Setz einen der beiden Punkte ein. Vier gleich zwei mal eins plus b gibt b gleich zwei. '
            'Die Gerade lautet y gleich zwei x plus zwei. Die Probe mit A bestätigt es.',
            f(r'4 = \fa{2} \cdot 1 + \fb{b} \;\Longrightarrow\; \fb{b} = 2', 300, 52),
            n('Probe mit @A@:|@\\fa{2} \\cdot (-2) + \\fb{2} = -2@ ✓', 460, 'gruen', ein=9.4),
            graf(W_GL, [bew([[2.6, 2, -3], [5.8, 2, 2]], yachse={'farbe': 2})],
                 [pt(-2, -2, 5, 'A'), pt(1, 4, 5, 'B')]),
            ueber(W_GL, punkte=[pt(-2, -2, 3), pt(1, 4, 3)], ein=9.4)),
         sz('Aus einer Lage',
            'Dritter Fall: Gesucht ist eine Gerade senkrecht zu y gleich zwei x plus zwei, durch den Punkt eins, eins. '
            'Senkrecht gibt m gleich minus null Komma fünf — die Gerade dreht sich. Und dann weiter wie vorher: '
            'Punkt einsetzen, b ausrechnen.',
            f(r'\fa{m} = \fa{-0.5}: \quad 1 = \fa{-0.5} \cdot 1 + \fb{b}', 300, 52),
            n('@\\fb{b} = 1.5@, also|@y = \\fa{-0.5}x + \\fb{1.5}@', 460, 'blau', ein=12.4),
            graf(W_GL, [ger(2, 2, 5, gestrichelt=True),
                        bew([[6.8, 2, 2], [9.4, -0.5, 2], [12.2, -0.5, 2], [14.2, -0.5, 1.5]])],
                 [pt(1, 1, 5, 'P(1 | 1)')])),
         sz('Aus einem Sachtext',
            'Vierter Fall: Auch in einem Text stecken m und b. Taxi: sechs Franken Grundtaxe und drei Franken '
            'pro Kilometer. Pro Kilometer ist die Steigung, die Grundtaxe der y-Achsenabschnitt. '
            'Gefahren wird ab null Kilometern — nur dort ist die Gerade sinnvoll.',
            f(r'K(x) = \fa{3}\,x + \fb{6}', 300, 66),
            n('«pro Kilometer» @\\to \\fa{m}@|«Grundtaxe» @\\to \\fb{b}@|sinnvoll nur für @x \\geq 0@', 460, 'blau'),
            graf(W_TAXI, [bew([[4.8, 0, 6], [7.6, 3, 6]], yachse={'farbe': 2})],
                 xname='x [km]', yname='K [CHF]')),
         sz('Merke',
            'Zum Mitnehmen: Der Ansatz ist immer y gleich m x plus b. Was gegeben ist, wird eingesetzt; '
            'zwei Punkte geben zuerst m, dann b. Und am Schluss immer die Probe.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'y = \fa{m}\,x + \fb{b} \qquad \fb{b} = y_1 - \fa{m}\,x_1', 420, 56, ein=0.4),
            n('@\\fa{m}@ gegeben: Punkt einsetzen|zwei Punkte: erst @\\fa{m}@, dann @\\fb{b}@|parallel oder senkrecht: zuerst @\\fa{m}@',
              560, 'blau', 44, ein=1.2),
            graf(W_GL, [bew([[4.4, 2, -3], [7.6, 2, 2]], yachse={'farbe': 2})],
                 [pt(-2, -2, 5), pt(1, 4, 5)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-aufstellen', 'Gerade sehen: Kontrollfragen zum Aufstellen',
     'Fünf Vorhersagen zum Aufstellen der Geradengleichung — aus m und Punkt, aus zwei Punkten, aus einer Lage und aus einem Text.',
     ['Geradengleichung', 'aufstellen', 'zwei Punkte', 'parallel', 'Kontrollfragen'], [
         # Frage 1 zum Tippen: Beim Fragen schwebt die Gerade über P; erst die Antwort lässt
         # sie einrasten, der gesuchte Punkt (0 | −5) ist vorher nicht im Bild.
         sz('Frage 1',
            'Punkt einsetzen: eins gleich drei mal zwei plus b. Sechs auf die andere Seite — b gleich minus fünf.',
            f(r'1 = \fa{3} \cdot 2 + \fb{b} \;\Longrightarrow\; \fb{b} = \fb{-5}', 300, 52, ein=1.2),
            n('@\\fb{b} = y_1 - \\fa{m}\\,x_1 = 1 - 6@', 460, 'orange', ein=2.6),
            graf(W_KB, [bew([[1.0, 3, 4], [3.8, 3, -5]], yachse={'farbe': 2})],
                 [pt(2, 1, 5, 'P(2 | 1)')])),
         sz('Frage 2',
            'Von A nach B: null minus vier ist minus vier, zwei minus null ist zwei. m gleich minus zwei. '
            'Und b steht schon da: A liegt auf der y-Achse, also vier.',
            f(r'\fa{m} = \dfrac{0 - 4}{2 - 0} = \fa{-2}, \quad \fb{b} = \fb{4}', 300, 50, ein=1.0),
            n('@A(0 \\mid 4)@ liegt auf der @y@-Achse:|@\\fb{b}@ ist direkt gegeben', 460, 'orange', ein=2.8),
            graf(W_GL, [bew([[1.0, 0, 4], [3.6, -2, 4]], yachse={'farbe': 2, 'beschriftung': False},
                            dreieck=dreieck(None, None, [[3.8, 0, 2], [5.6, 0, 2]]))],
                 [pt(2, 0, 5, 'B(2 | 0)')])),
         sz('Frage 3',
            'Punkt einsetzen und nach m auflösen: eins gleich m mal vier plus fünf gibt vier m gleich minus vier, '
            'also m gleich minus eins.',
            f(r'1 = \fa{m} \cdot 4 + \fb{5} \;\Longrightarrow\; \fa{m} = \fa{-1}', 300, 52, ein=1.0),
            n('Diesmal ist @\\fb{b}@ gegeben|und @\\fa{m}@ gesucht', 460, 'blau', ein=2.6),
            graf(dict(xbereich=[-4, 6], ybereich=[-3, 7]), [bew([[1.0, 0.5, 5], [3.6, -1, 5]], yachse={'farbe': 2})],
                 [pt(4, 1, 5, 'P(4 | 1)')])),
         sz('Frage 4',
            'Parallel heisst gleiches m, also minus drei. Punkt einsetzen: vier gleich minus drei mal eins plus b, '
            'also b gleich sieben.',
            f(r'4 = \fa{-3} \cdot 1 + \fb{b} \;\Longrightarrow\; \fb{b} = \fb{7}', 300, 52, ein=1.0),
            n('parallel: @\\fa{m}@ übernehmen,|dann Punkt einsetzen', 460, 'blau', ein=2.6),
            graf(dict(xbereich=[-2, 8], ybereich=[-2, 8]),
                 [ger(-3, 2, 5, gestrichelt=True), bew([[1.0, -3, 2], [3.6, -3, 7]], yachse={'farbe': 2})],
                 [pt(1, 4, 5, 'P(1 | 4)')])),
         sz('Frage 5',
            'Pro Minute vier Liter mehr: Das ist die Steigung. Achtzig Liter zu Beginn, also bei t gleich null: '
            'Das ist der y-Achsenabschnitt. V von t gleich vier t plus achtzig, sinnvoll ab t gleich null.',
            f(r'V(t) = \fa{4}\,t + \fb{80}', 300, 66, ein=1.0),
            n('«pro Minute» @\\to \\fa{m}@|«zu Beginn» @\\to \\fb{b}@|sinnvoll nur für @t \\geq 0@', 460, 'blau', ein=2.4),
            graf(W_TANK, [bew([[1.0, 0, 80], [3.6, 4, 80]], yachse={'farbe': 2})],
                 xname='t [min]', yname='V [l]')),
         sz('Merke',
            'Zum Mitnehmen: Immer derselbe Ansatz y gleich m x plus b. Zwei Punkte geben zuerst m, dann b. '
            'Parallel übernimmt m, senkrecht nimmt den negativen Kehrwert. Im Sachtext ist «pro» die Steigung.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fb{b} = y_1 - \fa{m}\,x_1', 420, 62, ein=0.4),
            n('zwei Punkte: erst @\\fa{m}@, dann @\\fb{b}@|parallel: gleiches @\\fa{m}@, anderes @\\fb{b}@|«pro …» @\\to \\fa{m}@, «zu Beginn» @\\to \\fb{b}@',
              560, 'blau', 44, ein=1.2),
            graf(dict(xbereich=[-2, 7], ybereich=[-2, 7]),
                 [bew([[0, -3, 7]], yachse={'farbe': 2})], [pt(1, 4, 5)])),
     ], [
         klick('Frage 1', 'm = 3 und P(2 | 1): Tipp den Schnittpunkt der Geraden mit der y-Achse ins Bild.',
               [0, -5], 'Getroffen: (0 | −5).',
               [{'bei': [0, 7], 'text': 'Das Vorzeichen: In b = y₁ − m·x₁ wird m·x₁ abgezogen.',
                 'sprich': 'Das Vorzeichen: In b gleich y eins minus m mal x eins wird m mal x eins abgezogen.'},
                {'bei': [0, 1], 'text': 'Das ist die Höhe von P. Gesucht ist der Wert der Geraden bei x = 0.',
                 'sprich': 'Das ist die Höhe von P. Gesucht ist der Wert der Geraden bei x gleich null.'},
                {'bei': [0, 3], 'text': 'Das ist die Steigung. Setz P in y = 3x + b ein.',
                 'sprich': 'Das ist die Steigung. Setz P in y gleich drei x plus b ein.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle — setz P in y = 3x + b ein und löse nach b auf.',
               sprich='m gleich drei und P zwei, eins: Tipp den Schnittpunkt der Geraden mit der y-Achse ins Bild.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle. Setz P in y gleich drei x plus b ein '
                             'und löse nach b auf.',
               tol=0.6),
         wahl('Frage 2', 'A(0 | 4) und B(2 | 0): Welche Gleichung gehört zur Geraden durch A und B?',
              ['y = −2x + 4', 'y = 2x + 4', 'y = −0.5x + 4'], 0,
              {0: 'Ja.',
               1: 'Die zweite Zahl stimmt. Aber geht es von A nach B hinauf oder hinunter?',
               2: 'Zähl noch einmal: 2 nach rechts, wie viel hinunter — und was kommt in den Nenner?'},
              sprich='A null, vier und B zwei, null: Welche Gleichung gehört zur Geraden durch A und B?',
              rueck_sprich={1: 'Die zweite Zahl stimmt. Aber geht es von A nach B hinauf oder hinunter?',
                            2: 'Zähl noch einmal: zwei nach rechts, wie viel hinunter. Und was kommt in den Nenner?'}),
         wahl('Frage 3', 'b = 5 und P(4 | 1): Wie gross ist m?',
              ['−1', '1', '−4'], 0,
              {0: 'Ja.',
               1: 'Von (0 | 5) nach (4 | 1) geht es hinunter. Welches Vorzeichen hat m dann?',
               2: 'Das ist Δy. Was fehlt im Bruch noch?'},
              sprich='b gleich fünf und P vier, eins: Wie gross ist m?',
              rueck_sprich={1: 'Von null, fünf nach vier, eins geht es hinunter. Welches Vorzeichen hat m dann?',
                            2: 'Das ist delta y. Was fehlt im Bruch noch?'}),
         wahl('Frage 4', 'Gesucht: die Gerade parallel zu y = −3x + 2 durch P(1 | 4).',
              ['y = −3x + 7', 'y = −3x + 4', 'y = −3x + 1'], 0,
              {0: 'Ja.',
               1: 'Die Steigung stimmt. Setz P ein und schau, ob die Gleichung aufgeht.',
               2: 'Die Steigung stimmt. Rechne b = y₁ − m·x₁ nochmals — mit welchem Vorzeichen?'},
              sprich='Gesucht ist die Gerade parallel zu y gleich minus drei x plus zwei, durch P eins, vier.',
              rueck_sprich={1: 'Die Steigung stimmt. Setz P ein und schau, ob die Gleichung aufgeht.',
                            2: 'Die Steigung stimmt. Rechne b gleich y eins minus m mal x eins nochmals. Mit welchem Vorzeichen?'}),
         wahl('Frage 5', 'Ein Behälter enthält 80 Liter; pro Minute fliessen 4 Liter zu. Welche Gleichung?',
              ['V(t) = 4t + 80', 'V(t) = 80t + 4', 'V(t) = −4t + 80'], 0,
              {0: 'Ja.',
               1: 'Welche der beiden Zahlen gehört zu «pro Minute»?',
               2: 'Es fliesst zu, nicht ab. Welches Vorzeichen hat m dann?'},
              sprich='Ein Behälter enthält achtzig Liter; pro Minute fliessen vier Liter zu. Welche Gleichung?',
              rueck_sprich={1: 'Welche der beiden Zahlen gehört zu «pro Minute»?',
                            2: 'Es fliesst zu, nicht ab. Welches Vorzeichen hat m dann?'}),
     ], art='Kontrollclip')
