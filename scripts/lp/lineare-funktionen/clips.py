"""Erzeugt die acht Drehbücher des Leitprogramms Lineare Funktionen (03.10.2026).

  python3 scripts/lp/lineare-funktionen/clips.py

**Nach der Vertonung nicht mehr laufen lassen** — dann sind die JSONs in clips/ die
Quelle und tragen die gemessenen `dauer`. Ein neuer Lauf überschreibt sie (HOWTO-clips.md,
«Werkstatt»). Das Skript liegt hier als Muster und als Nachweis, woher die Szenen kommen.

Aufbau wie beim Vorbild (scripts/lp/quadratische-funktionen/kontrollclips.py): Bild rechts
(x 1010, y 175, 760 × 760), Formeln und Notizen links (x 150), Theme begreifbar-schlicht.

Farben im ganzen Leitprogramm — eine Farbe, eine Bedeutung (HOWTO-leitprogramme §15):
  1 blau  = m (Steigung)          \\fa{…}
  2 orange = b (y-Achsenabschnitt) \\fb{…}
  3 grün  = Nullstelle, Zielpunkt  \\fc{…}
  4 rot   = Fehler, Gegenbeispiel  \\fd{…}
  5 Tinte = neutral (gegebener Punkt, Bezugsgerade)

Keine bewegten Geraden: `bewegung` in build-clips.py kennt nur Parabeln
(HOWTO-clips.md, «Bewegte Parabel»). Bewegung entsteht hier wie in HOWTO-leitprogramme §7
beschrieben — Szene für Szene ein Zustand, die vorige Gerade gestrichelt als Bezug.
Darum auch nur Fragen vom Typ `wahl` (`klick` braucht ein bewegtes Bild).

Damit die Antwort einer Frage nicht schon im Bild steht (§15): Die Frage steht bei 0.3 s,
das Bild der Auflösung blendet erst bei `ein` ≈ 1.2 s ein. Solange der Clip an der Frage
hält, läuft die Szenenzeit nicht weiter — das Bild erscheint erst nach der Antwort.
Fragen, die nach der *Gleichung zum Bild* fragen, haben es umgekehrt: Bild früh, Formel spät.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150


# ── Bausteine ────────────────────────────────────────────────────────────────
# Beschriftungen werden gerechnet, nicht geschaetzt (HOWTO-clips.md, «Die freie Stelle
# ausrechnen»): Der Abspieler setzt sie mit font-size 29 ohne Hof, eine Gerade darunter
# ist also nicht zu lesen. stelle() probiert Kandidaten rings um den Punkt und nimmt den
# ersten, dessen Textkiste im Fenster liegt und keine Gerade, keinen Punkt und keine
# andere Beschriftung schneidet. Geprueft wird dasselbe nochmals von
# scripts/lp/lineare-funktionen/pruef-graf.py.
from grafgeom import achsenkisten, frei, kiste, masse       # Geometrie wie in build-clips.py


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


def graf(W, geraden=(), punkte=(), ein=0.05, **kw):
    ger_l = [(g['m'], g['q']) for g in geraden]
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


def ger(m, q, farbe=1, gestrichelt=False, dicke=None, text=None, bei=None, anker='start'):
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    if text:
        d['beschriftung'] = text
        d['anker'] = anker
        if bei:
            d['beschriftung_bei'] = bei
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
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': richtig, 'rueck': {str(k): v for k, v in rueck.items()}}
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(k): v for k, v in rueck_sprich.items()}
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
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


# Fenster. Wo eine Senkrechte senkrecht aussehen muss, sind beide Spannen gleich
# (760 × 760 Pixel): x[-4,5] und y[-4,5] sind je 9 Einheiten.
W_TAB = dict(xbereich=[-3, 4], ybereich=[-4, 8])
W_MB = dict(xbereich=[-4, 5], ybereich=[-5, 6])
W_DREI = dict(xbereich=[-2, 7], ybereich=[-3, 6])
W_GLEICH = dict(xbereich=[-4, 5], ybereich=[-4, 5])
W_KF1 = dict(xbereich=[-3, 6], ybereich=[-6, 8])          # C8 Frage 1: b = −5 muss ins Bild
W_SF1 = dict(xbereich=[-1, 6], ybereich=[-2, 12])         # C4 Frage 1: B(5 | 10) muss ins Bild
W_TAXI = dict(xbereich=[-1, 8], ybereich=[-4, 32], yteilung=[[0, '0'], [10, '10'], [20, '20'], [30, '30']])

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
clip('m-und-b', 'Gerade sehen: m kippt, b schiebt',
     'Von der Wertetabelle zur Geraden — und was die beiden Zahlen m und b mit ihr machen.',
     ['lineare Funktion', 'Steigung', 'y-Achsenabschnitt', 'Gerade', 'Wertetabelle'], [
         sz('Wertetabelle',
            'Eine lineare Funktion wächst in gleichen Schritten. Zum Beispiel y gleich zwei x plus eins. '
            'Die Wertetabelle: minus drei, minus eins, eins, drei, fünf, sieben. Jedes Wertepaar wird ein Punkt.',
            titel('Die Gerade', 280, 80),
            f(r'\begin{array}{c|cccccc} x & -2 & -1 & 0 & 1 & 2 & 3 \\ \hline y = 2x + 1 & -3 & -1 & 1 & 3 & 5 & 7 \end{array}',
              440, 40),
            graf(W_TAB, punkte=[pt(x, 2 * x + 1, 1) for x in (-2, -1, 0, 1, 2, 3)])),
         sz('Die Gerade',
            'Verbunden ergeben die Punkte eine Gerade. Von Punkt zu Punkt geht es einen nach rechts und '
            'zwei hinauf — jedes Mal gleich viel. Genau das macht den Graphen zur Geraden.',
            f(r'y = 2x + 1', 300, 70),
            n('gleicher Schritt nach rechts,|gleicher Zuwachs hinauf', 440, 'blau'),
            graf(W_TAB, [ger(2, 1)], [pt(x, 2 * x + 1, 1) for x in (-2, -1, 0, 1, 2, 3)])),
         sz('Zwei Zahlen',
            'Jede Gerade steckt in zwei Zahlen: m und b. Schauen wir sie uns einzeln an.',
            titel('Zwei Zahlen', 300, 86),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 470, 66),
            graf(W_MB, [ger(2, 1)], [pt(0, 1, 2)])),
         sz('b schiebt hinauf',
            'Zuerst b. Plus drei hebt die ganze Gerade um drei nach oben. Sie schneidet die y-Achse bei drei, '
            'und ihre Richtung bleibt gleich.',
            f(r'y = \fa{2}x \fb{+ 3}', 300, 70),
            n('@\\fb{b}@ ist der @y@-Achsenabschnitt:|die Gerade schneidet die @y@-Achse bei @\\fb{3}@', 440, 'orange'),
            graf(W_MB, [ger(2, 0, 5, gestrichelt=True), ger(2, 3)], [pt(0, 3, 2, '(0 | 3)')])),
         sz('b schiebt hinunter',
            'Minus zwei senkt sie um zwei. Das Vorzeichen stimmt mit der Richtung überein: plus hinauf, minus hinunter. '
            'b schiebt nur senkrecht.',
            f(r'y = \fa{2}x \fb{- 2}', 300, 70),
            n('@\\fb{b}@ schiebt senkrecht —|plus hinauf, minus hinunter', 440, 'orange'),
            graf(W_MB, [ger(2, 0, 5, gestrichelt=True), ger(2, -2)], [pt(0, -2, 2, '(0 | −2)')])),
         sz('m kippt',
            'Jetzt m, die Steigung. Aus zwei wird null Komma fünf: Die Gerade wird flacher. '
            'Fest bleibt dabei nur ein Punkt — der auf der y-Achse.',
            f(r'y = \fa{0.5}x + \fb{1}', 300, 70),
            n('@\\fa{m}@ kippt die Gerade|um den Punkt @(0 \\mid \\fb{b})@', 440, 'blau'),
            graf(W_MB, [ger(2, 1, 5, gestrichelt=True), ger(0.5, 1)], [pt(0, 1, 2, '(0 | 1)')])),
         sz('m wird negativ',
            'Ein negatives m lässt die Gerade fallen. Bei minus eins Komma fünf geht es pro Schritt nach rechts '
            'um eins Komma fünf hinunter. Der Drehpunkt bleibt null und eins.',
            f(r'y = \fa{-1.5}x + \fb{1}', 300, 70),
            n('@\\fa{m} \\gt 0@: steigt · @\\fa{m} \\lt 0@: fällt|@\\fa{m} = 0@: waagrecht', 440, 'blau'),
            graf(W_MB, [ger(0.5, 1, 5, gestrichelt=True), ger(-1.5, 1)], [pt(0, 1, 2, '(0 | 1)')])),
         sz('m als Schritt',
            'So liest man m am Graphen: einen Schritt nach rechts, dann m Schritte hinauf. '
            'Bei m gleich zwei führt das von null, eins nach eins, drei.',
            f(r'y = \fa{2}x + \fb{1}', 300, 70),
            n('1 nach rechts,|@\\fa{2}@ hinauf', 440, 'blau'),
            graf(W_MB, [ger(2, 1)], [pt(0, 1, 2, '(0 | 1)'), pt(1, 3, 5, '(1 | 3)')])),
         sz('Merke',
            'Zum Mitnehmen: b ist der Wert bei x gleich null und schiebt die Gerade senkrecht. '
            'm ist der Zuwachs pro Schritt nach rechts und kippt sie um den Punkt null, b. '
            'Positives m steigt, negatives fällt, m gleich null bleibt waagrecht.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 420, 66, ein=0.4),
            n('@\\fb{b}@: Wert bei @x = 0@, schiebt senkrecht|@\\fa{m}@: Zuwachs pro Schritt nach rechts,|kippt um @(0 \\mid \\fb{b})@',
              560, 'blau', 44, ein=1.2),
            graf(W_MB, [ger(2, 1)], [pt(0, 1, 2, '(0 | 1)')])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-m-und-b', 'Gerade sehen: Kontrollfragen zu m und b',
     'Fünf Vorhersagen zu Steigung und Achsenabschnitt: Der Clip hält an, fragt und löst dann auf.',
     ['Steigung', 'y-Achsenabschnitt', 'Gerade', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei x gleich null bleibt nur b übrig: minus zwei. Dort schneidet die Gerade die y-Achse.',
            f(r'y = \fa{0.5}x \fb{- 2}', 300, 70),
            n('@f(0) = \\fb{b} = \\fb{-2}@', 440, 'orange', ein=2.0),
            graf(W_MB, [ger(0.5, -2)], [pt(0, -2, 2, '(0 | −2)')], ein=1.2)),
         sz('Frage 2',
            'Gleiches m heisst gleiche Richtung: Die beiden sind parallel. Und weil b von plus eins auf minus vier '
            'fällt, liegt die zweite Gerade fünf tiefer.',
            f(r'y = \fa{3}x \fb{+ 1} \qquad y = \fa{3}x \fb{- 4}', 300, 52),
            n('gleiches @\\fa{m}@, verschiedenes @\\fb{b}@:|parallel, 5 tiefer', 440, 'orange', ein=2.0),
            graf(W_MB, [ger(3, 1), ger(3, -4, 2)], [pt(0, 1, 2), pt(0, -4, 2)], ein=1.2)),
         sz('Frage 3',
            'Die Gerade schneidet die y-Achse bei drei, also b gleich drei. Und pro Schritt nach rechts geht es '
            'eins hinunter: m gleich minus eins. Also y gleich minus x plus drei.',
            f(r'y = \fa{-1}x + \fb{3}', 300, 70, ein=1.4),
            n('erst @\\fb{b}@ ablesen,|dann @\\fa{m}@ über ein Dreieck', 440, 'blau', ein=2.6),
            graf(W_MB, [ger(-1, 3)], [pt(0, 3, 2), pt(3, 0, 5)])),
         sz('Frage 4',
            'Einsetzen entscheidet: f von eins ist minus zwei plus fünf, also drei. Der Punkt eins, drei liegt '
            'auf dem Graphen — eins, sieben und drei, eins liegen daneben.',
            f(r'f(1) = \fa{-2} \cdot 1 + \fb{5} = 3', 300, 60),
            n('Punktprobe: @x@ einsetzen,|Ergebnis mit @y@ vergleichen', 440, 'blau', ein=2.6),
            graf(W_MB, [ger(-2, 5)], [pt(1, 3, 3, '(1 | 3)')], ein=1.2)),
         sz('Frage 5',
            'Pro Schritt nach rechts zwei hinunter heisst m gleich minus zwei. Durch null, minus eins heisst '
            'b gleich minus eins. Also y gleich minus zwei x minus eins.',
            f(r'y = \fa{-2}x \fb{- 1}', 300, 70),
            n('«fällt um 2 pro Schritt» @\\Rightarrow \\fa{m} = -2@|«durch @(0 \\mid -1)@» @\\Rightarrow \\fb{b} = -1@',
              440, 'blau', ein=2.4),
            graf(W_MB, [ger(-2, -1)], [pt(0, -1, 2, '(0 | −1)')], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: b liest man direkt auf der y-Achse ab, m über einen Schritt nach rechts. '
            'Gleiches m heisst parallel. Und ob ein Punkt auf der Geraden liegt, entscheidet nur das Einsetzen.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 420, 66, ein=0.4),
            n('@\\fb{b}@: auf der @y@-Achse ablesen|@\\fa{m}@: 1 nach rechts, @\\fa{m}@ hinauf|gleiches @\\fa{m}@: parallel',
              560, 'blau', 44, ein=1.2),
            graf(W_MB, [ger(-2, -1)], [pt(0, -1, 2)])),
     ], [
         wahl('Frage 1', 'y = 0.5x − 2: Wo schneidet die Gerade die y-Achse?',
              ['bei −2', 'bei 0.5', 'bei 2'], 0,
              {0: 'Ja.',
               1: 'Das ist die Steigung. Gesucht ist der Wert bei x = 0 — setz 0 ein.',
               2: 'Das Vorzeichen fehlt: In der Gleichung steht −2.'},
              sprich='y gleich null Komma fünf x minus zwei: Wo schneidet die Gerade die y-Achse?',
              rueck_sprich={1: 'Das ist die Steigung. Gesucht ist der Wert bei x gleich null. Setz null ein.',
                            2: 'Das Vorzeichen fehlt: In der Gleichung steht minus zwei.'}),
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
               1: 'Der Achsenabschnitt stimmt. Aber steigt die Gerade im Bild, oder fällt sie?',
               2: 'Vertauscht: Die Gerade schneidet die y-Achse bei 3, nicht bei 1.'},
              rueck_sprich={1: 'Der Achsenabschnitt stimmt. Aber steigt die Gerade im Bild, oder fällt sie?',
                            2: 'Vertauscht: Die Gerade schneidet die y-Achse bei drei, nicht bei eins.'}),
         wahl('Frage 4', 'f(x) = −2x + 5: Welcher Punkt liegt auf dem Graphen?',
              ['(1 | 3)', '(1 | 7)', '(3 | 1)'], 0,
              {0: 'Ja.',
               1: 'Das Vorzeichen von m: −2 · 1 ist nicht +2. Rechne f(1) nochmals.',
               2: 'Koordinaten vertauscht? Setz die erste Zahl für x ein und vergleich mit der zweiten.'},
              sprich='f von x gleich minus zwei x plus fünf: Welcher Punkt liegt auf dem Graphen?',
              rueck_sprich={1: 'Das Vorzeichen von m: minus zwei mal eins ist nicht plus zwei. Rechne f von eins nochmals.',
                            2: 'Sind die Koordinaten vertauscht? Setz die erste Zahl für x ein und vergleich mit der zweiten.'}),
         wahl('Frage 5', 'Eine Gerade geht durch (0 | −1) und fällt pro Schritt nach rechts um 2. Welche Gleichung?',
              ['y = −2x − 1', 'y = 2x − 1', 'y = −2x + 1'], 0,
              {0: 'Ja.',
               1: 'Die Gerade fällt. Welches Vorzeichen hat m dann?',
               2: 'Die Steigung stimmt. Aber (0 | −1) heisst b = −1.'},
              sprich='Eine Gerade geht durch null, minus eins und fällt pro Schritt nach rechts um zwei. Welche Gleichung?',
              rueck_sprich={1: 'Die Gerade fällt. Welches Vorzeichen hat m dann?',
                            2: 'Die Steigung stimmt. Aber null, minus eins heisst b gleich minus eins.'}),
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
            f(r'\fa{m} = \frac{\Delta y}{\Delta x} = \frac{4}{5} = \fa{0.8}', 300, 62),
            n('@\\Delta x = 5@ nach rechts|@\\Delta y = 4@ hinauf', 460, 'blau'),
            graf(W_DREI, [ger(0.8, 1)], [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')])),
         sz('Kleines Dreieck',
            'Jetzt ein kleineres Dreieck auf derselben Geraden: zwei Komma fünf nach rechts, zwei hinauf. '
            'Zwei geteilt durch zwei Komma fünf — wieder null Komma acht.',
            f(r'\fa{m} = \frac{2}{2.5} = \fa{0.8}', 300, 62),
            n('anderes Dreieck,|dasselbe @\\fa{m}@ — die Dreiecke sind ähnlich', 460, 'blau'),
            graf(W_DREI, [ger(0.8, 1)], [pt(0, 1, 5, 'P'), pt(2.5, 3, 5, 'R(2.5 | 3)')])),
         sz('Die Formel',
            'Allgemein: m ist y zwei minus y eins, geteilt durch x zwei minus x eins. '
            'Immer der Unterschied der Höhen durch den Unterschied der Stellen.',
            f(r'\fa{m} = \frac{y_2 - y_1}{x_2 - x_1}', 300, 66),
            n('Höhenunterschied|durch Stellenunterschied', 460, 'blau'),
            graf(W_DREI, [ger(0.8, 1)], [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')])),
         sz('Ein Beispiel',
            'Ein Beispiel mit negativer Steigung: A liegt bei minus eins und vier, B bei drei und minus zwei. '
            'Minus zwei minus vier ist minus sechs, geteilt durch vier: m gleich minus eins Komma fünf.',
            f(r'\fa{m} = \frac{-2 - 4}{3 - (-1)} = \frac{-6}{4} = \fa{-1.5}', 300, 56),
            n('Die Gerade fällt:|@\\fa{m} \\lt 0@', 460, 'blau'),
            graf(W_GLEICH, [ger(-1.5, 2.5)], [pt(-1, 4, 5, 'A(−1 | 4)'), pt(3, -2, 5, 'B(3 | −2)')])),
         sz('Leserichtung',
            'Gelesen wird immer von links nach rechts, also mit Delta x grösser als null. '
            'Wer die Punkte vertauscht, dreht beide Unterschiede — und erhält dasselbe m.',
            f(r'\frac{4 - (-2)}{-1 - 3} = \frac{6}{-4} = \fa{-1.5}', 300, 56),
            n('Punkte vertauscht:|beide Vorzeichen drehen,|@\\fa{m}@ bleibt gleich', 460, 'blau'),
            graf(W_GLEICH, [ger(-1.5, 2.5)], [pt(-1, 4, 5, 'A'), pt(3, -2, 5, 'B')])),
         sz('Die Nullstelle',
            'Und noch eine Stelle lohnt den Blick: die Nullstelle. Dort schneidet die Gerade die x-Achse, '
            'dort ist y gleich null. Bei zwei x minus sechs: null gleich zwei x minus sechs, also x gleich drei.',
            f(r'0 = \fa{2}x \fb{- 6} \quad\Longrightarrow\quad x_0 = -\frac{\fb{b}}{\fa{m}} = \fc{3}', 300, 50),
            n('Nullstelle: Schnitt mit der @x@-Achse|nicht verwechseln mit @\\fb{b}@', 460, 'gruen'),
            graf(W_DREI, [ger(2, -6)], [pt(3, 0, 3, '(3 | 0)')])),
         sz('Delta x null',
            'Ein Fall bleibt übrig: Zwei Punkte mit derselben x-Koordinate. Dann ist Delta x null — '
            'und durch null lässt sich nicht teilen. Die Gerade durch diese zwei Punkte steht senkrecht, '
            'sie hat keine Steigung und ist keine Funktion.',
            f(r'\Delta x = 0 \quad\Longrightarrow\quad \frac{\Delta y}{0}', 300, 60),
            n('@\\fd{m}@ ist nicht definiert.|Eine senkrechte Gerade|ist keine Funktion.', 460, 'rot'),
            graf(W_GLEICH, punkte=[pt(2, -1, 4, '(2 | −1)'), pt(2, 3, 4, '(2 | 3)')])),
         sz('Merke',
            'Zum Mitnehmen: m ist hinauf geteilt durch nach rechts. Jedes Steigungsdreieck derselben Geraden '
            'gibt dasselbe m, weil die Dreiecke ähnlich sind. Und die Nullstelle ist minus b durch m.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fa{m} = \frac{\Delta y}{\Delta x} \qquad x_0 = -\frac{\fb{b}}{\fa{m}}', 420, 62, ein=0.4),
            n('jedes Dreieck derselben Geraden:|dasselbe @\\fa{m}@|@\\Delta x = 0@: keine Steigung',
              560, 'blau', 44, ein=1.2),
            graf(W_DREI, [ger(0.8, 1)], [pt(0, 1, 5, 'P'), pt(5, 5, 5, 'Q')])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-steigung', 'Gerade sehen: Kontrollfragen zur Steigung',
     'Fünf Vorhersagen zu Δy durch Δx, zur Nullstelle und zum Fall Δx gleich null.',
     ['Steigung', 'Steigungsdreieck', 'Nullstelle', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zehn minus zwei ist acht, fünf minus eins ist vier. Acht geteilt durch vier ist zwei.',
            f(r'\fa{m} = \frac{10 - 2}{5 - 1} = \frac{8}{4} = \fa{2}', 300, 58),
            n('Höhenunterschied|durch Stellenunterschied', 460, 'blau', ein=2.4),
            graf(W_SF1, [ger(2, 0)], [pt(1, 2, 5, 'A(1 | 2)'), pt(5, 10, 5, 'B(5 | 10)')], ein=1.2)),
         sz('Frage 2',
            'Minus zwei minus vier ist minus sechs. Eins minus minus drei ist vier. Minus sechs durch vier '
            'ist minus eins Komma fünf.',
            f(r'\fa{m} = \frac{-2 - 4}{1 - (-3)} = \frac{-6}{4} = \fa{-1.5}', 300, 54),
            n('Beide Klammern sorgfältig:|minus minus drei ist plus drei', 460, 'blau', ein=2.4),
            graf(W_GLEICH, [ger(-1.5, -0.5)], [pt(-3, 4, 5, 'P(−3 | 4)'), pt(1, -2, 5, 'Q(1 | −2)')], ein=1.2)),
         sz('Frage 3',
            'Null gleich drei x minus zwölf gibt drei x gleich zwölf, also x gleich vier. Dort schneidet die '
            'Gerade die x-Achse.',
            f(r'0 = \fa{3}x \fb{- 12} \quad\Longrightarrow\quad x_0 = \fc{4}', 300, 54),
            n('@x_0 = -\\dfrac{\\fb{b}}{\\fa{m}} = -\\dfrac{-12}{3} = \\fc{4}@', 460, 'gruen', ein=2.4),
            graf(dict(xbereich=[-2, 7], ybereich=[-14, 10], yteilung=[[0, '0'], [-10, '−10'], [5, '5']]),
                 [ger(3, -12)], [pt(4, 0, 3, '(4 | 0)')], ein=1.2)),
         sz('Frage 4',
            'Die Gerade schneidet die y-Achse bei zwei und die x-Achse bei vier. Vier nach rechts, zwei hinunter: '
            'm gleich minus zwei geteilt durch vier, also minus null Komma fünf.',
            f(r'\fa{m} = \frac{-2}{4} = \fa{-0.5}', 300, 62, ein=1.4),
            n('4 nach rechts, 2 hinunter', 460, 'blau', ein=2.6),
            graf(W_DREI, [ger(-0.5, 2)], [pt(0, 2, 2), pt(4, 0, 3)])),
         sz('Frage 5',
            'Dieselbe x-Koordinate heisst Delta x gleich null. Teilen durch null geht nicht: m ist nicht definiert.',
            f(r'\Delta x = 0: \quad \frac{\Delta y}{0}', 300, 60),
            n('@\\fd{m}@ ist nicht definiert —|die Gerade steht senkrecht', 460, 'rot', ein=2.2),
            graf(W_GLEICH, punkte=[pt(-1, -2, 4, '(−1 | −2)'), pt(-1, 3, 4, '(−1 | 3)')], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: erst die Höhen abziehen, dann die Stellen, dann teilen. Die Nullstelle ist minus b '
            'durch m, und der y-Achsenabschnitt ist etwas anderes. Bei Delta x gleich null gibt es keine Steigung.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fa{m} = \frac{y_2 - y_1}{x_2 - x_1} \qquad x_0 = -\frac{\fb{b}}{\fa{m}}', 420, 58, ein=0.4),
            n('@\\fc{x_0}@: Schnitt mit der @x@-Achse|@\\fb{b}@: Schnitt mit der @y@-Achse|@\\Delta x = 0@: kein @\\fa{m}@',
              560, 'blau', 44, ein=1.2),
            graf(W_DREI, [ger(-0.5, 2)], [pt(0, 2, 2), pt(4, 0, 3)])),
     ], [
         wahl('Frage 1', 'A(1 | 2) und B(5 | 10): Wie gross ist die Steigung m?',
              ['2', '8', '0.5'], 0,
              {0: 'Ja.',
               1: 'Das ist nur der Höhenunterschied Δy. Es fehlt das Teilen durch Δx.',
               2: 'Bruch verkehrt: oben der Höhenunterschied, unten der Stellenunterschied.'},
              sprich='A eins, zwei und B fünf, zehn: Wie gross ist die Steigung m?',
              rueck_sprich={1: 'Das ist nur der Höhenunterschied delta y. Es fehlt das Teilen durch delta x.',
                            2: 'Der Bruch ist verkehrt: oben der Höhenunterschied, unten der Stellenunterschied.'}),
         wahl('Frage 2', 'P(−3 | 4) und Q(1 | −2): Wie gross ist m?',
              ['−1.5', '1.5', '−6'], 0,
              {0: 'Ja.',
               1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
               2: 'Das ist Δy. Teile noch durch Δx — und achte auf die Klammer bei −3.'},
              sprich='P minus drei, vier und Q eins, minus zwei: Wie gross ist m?',
              rueck_sprich={1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
                            2: 'Das ist delta y. Teile noch durch delta x. Und achte auf die Klammer bei minus drei.'}),
         wahl('Frage 3', 'f(x) = 3x − 12: Wo liegt die Nullstelle?',
              ['bei 4', 'bei −12', 'bei −4'], 0,
              {0: 'Ja.',
               1: 'Das ist b, der Schnittpunkt mit der y-Achse. Gesucht ist die Stelle mit y = 0.',
               2: 'Vorzeichen: x₀ = −b/m = −(−12)/3.'},
              sprich='f von x gleich drei x minus zwölf: Wo liegt die Nullstelle?',
              rueck_sprich={1: 'Das ist b, der Schnittpunkt mit der y-Achse. Gesucht ist die Stelle mit y gleich null.',
                            2: 'Das Vorzeichen: x null ist minus b durch m, also minus, minus zwölf, durch drei.'}),
         wahl('Frage 4', 'Wie gross ist die Steigung der Geraden im Bild?',
              ['−0.5', '0.5', '−2'], 0,
              {0: 'Ja.',
               1: 'Der Betrag stimmt. Aber steigt die Gerade, oder fällt sie?',
               2: 'Bruch verkehrt: 4 nach rechts, 2 hinunter — nicht umgekehrt.'},
              rueck_sprich={1: 'Der Betrag stimmt. Aber steigt die Gerade, oder fällt sie?',
                            2: 'Der Bruch ist verkehrt: vier nach rechts, zwei hinunter. Nicht umgekehrt.'}),
         wahl('Frage 5', 'Zwei Punkte haben dieselbe x-Koordinate. Was folgt für m?',
              ['m ist nicht definiert', 'm = 0', 'm = 1'], 0,
              {0: 'Ja.',
               1: 'Das wäre bei gleicher y-Koordinate so — eine waagrechte Gerade. Hier ist Δx = 0.',
               2: 'Schreib Δy durch Δx hin und setz Δx = 0 ein.'},
              sprich='Zwei Punkte haben dieselbe x-Koordinate. Was folgt für m?',
              rueck_sprich={1: 'Das wäre bei gleicher y-Koordinate so, eine waagrechte Gerade. Hier ist delta x null.',
                            2: 'Schreib delta y durch delta x hin und setz delta x gleich null ein.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
clip('typen', 'Gerade sehen: Typen und Lagebeziehungen',
     'Proportional, Identität, konstant, senkrecht — und wann zwei Geraden parallel oder senkrecht sind.',
     ['proportionale Funktion', 'Identität', 'konstante Funktion', 'parallel', 'senkrecht'], [
         sz('Vier Typen',
            'Alle linearen Funktionen haben dieselbe Form. Trotzdem lohnen sich vier Fälle einzeln — '
            'sie unterscheiden sich nur in m und b.',
            titel('Vier Fälle', 300, 86),
            f(r'f(x) = \fa{m}\,x + \fb{b}', 470, 66),
            graf(W_GLEICH, [ger(1.5, -2)], [pt(0, -2, 2)])),
         sz('Proportional',
            'Erster Fall: b gleich null. Dann geht die Gerade durch den Ursprung, und doppeltes x gibt '
            'doppeltes f von x. Das ist eine proportionale Funktion.',
            f(r'f(x) = \fa{1.5}\,x \qquad (\fb{b} = 0)', 300, 58),
            n('proportional:|durch den Ursprung', 460, 'blau'),
            graf(W_GLEICH, [ger(1.5, -2, 5, gestrichelt=True), ger(1.5, 0)], [pt(0, 0, 2, '(0 | 0)')])),
         sz('Identität',
            'Mit m gleich eins wird daraus die Identität: Jeder x-Wert wird auf sich selbst abgebildet. '
            'Die Gerade halbiert den rechten Winkel zwischen den Achsen.',
            f(r'f(x) = x \qquad (\fa{m} = 1,\ \fb{b} = 0)', 300, 52),
            n('Identität:|@x \\longmapsto x@', 460, 'blau'),
            graf(W_GLEICH, [ger(1.5, 0, 5, gestrichelt=True), ger(1, 0)],
                 [pt(2, 2, 5, '(2 | 2)'), pt(-1, -1, 5, '(−1 | −1)')])),
         sz('Konstant',
            'Dritter Fall: m gleich null. Dann fällt der x-Teil weg, und übrig bleibt b. '
            'Der Graph ist eine waagrechte Gerade — die konstante Funktion.',
            f(r'f(x) = \fb{3} \qquad (\fa{m} = 0)', 300, 58),
            n('konstant:|waagrecht, @\\fa{m} = 0@', 460, 'orange'),
            graf(W_GLEICH, [ger(1, 0, 5, gestrichelt=True), ger(0, 3)], [pt(0, 3, 2, '(0 | 3)')])),
         sz('Senkrecht',
            'Und der Fall, der keine Funktion ist: x gleich drei. Zur Stelle drei gehören unendlich viele y-Werte. '
            'Eine Funktion darf jedem x nur einen Wert zuordnen — darum ist das keine.',
            f(r'x = 3', 300, 70),
            n('@\\fd{keine\\ Funktion}@:|einem @x@ unendlich viele @y@', 460, 'rot'),
            graf(W_GLEICH, punkte=[pt(3, y, 4) for y in (-3, -2, -1, 0, 1, 2, 3, 4)])),
         sz('Parallel',
            'Zwei Geraden mit gleichem m zeigen in dieselbe Richtung: Sie sind parallel und treffen sich nie. '
            'Verschieden ist nur ihr b.',
            f(r'y = \fa{2}x \fb{+ 1} \qquad y = \fa{2}x \fb{- 3}', 300, 50),
            n('parallel:|@\\fa{m_1} = \\fa{m_2}@, @\\fb{b_1} \\neq \\fb{b_2}@', 460, 'blau'),
            graf(W_GLEICH, [ger(2, 1), ger(2, -3)], [pt(0, 1, 2), pt(0, -3, 2)])),
         sz('Senkrecht zueinander',
            'Senkrecht ist überraschender: Das Produkt der beiden Steigungen ist minus eins. '
            'Zu m gleich zwei gehört also minus ein Halb.',
            f(r'\fa{2} \cdot \fa{(-0.5)} = -1', 300, 62),
            n('senkrecht:|@\\fa{m_1} \\cdot \\fa{m_2} = -1@', 460, 'blau'),
            graf(W_GLEICH, [ger(2, 1), ger(-0.5, 1)], [pt(0, 1, 5, '(0 | 1)')])),
         sz('Warum minus eins',
            'Der Grund steckt im Steigungsdreieck. Dreht man es um neunzig Grad, tauschen hinauf und nach rechts '
            'die Rolle, und die Richtung kippt: aus zwei zu eins wird eins zu minus zwei.',
            f(r'\frac{2}{1} \;\longrightarrow\; \frac{-1}{2} = \fa{-0.5}', 300, 58),
            n('Dreieck um @90^\\circ@ gedreht:|@\\Delta x@ und @\\Delta y@ tauschen,|ein Vorzeichen kippt', 460, 'blau'),
            graf(W_GLEICH, [ger(2, 1), ger(-0.5, 1)],
                 [pt(0, 1, 5), pt(1, 3, 5, '(1 | 3)'), pt(2, 0, 5, '(2 | 0)')])),
         sz('Merke',
            'Zum Mitnehmen: proportional heisst b gleich null, die Identität hat zusätzlich m gleich eins, '
            'konstant heisst m gleich null. Eine senkrechte Gerade ist keine Funktion. '
            'Parallel heisst gleiches m, senkrecht heisst Produkt der Steigungen minus eins.',
            titel('Zum Mitnehmen', 240, 76),
            f(r'\fb{b} = 0:\ \text{proportional}', 380, 48, ein=0.4),
            f(r'\fa{m} = 0:\ \text{konstant}', 460, 48, ein=0.7),
            n('@\\fa{m_1} = \\fa{m_2}@: parallel|@\\fa{m_1} \\cdot \\fa{m_2} = -1@: senkrecht|@x = k@: keine Funktion',
              570, 'blau', 44, ein=1.4),
            graf(W_GLEICH, [ger(2, 1), ger(-0.5, 1)], [pt(0, 1, 5)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-typen', 'Gerade sehen: Kontrollfragen zu Typen und Lage',
     'Fünf Vorhersagen zu proportional, konstant, senkrechter Gerade, parallel und senkrecht.',
     ['proportionale Funktion', 'konstante Funktion', 'parallel', 'senkrecht', 'Kontrollfragen'], [
         sz('Frage 1',
            'b ist null, also geht die Gerade durch den Ursprung: eine proportionale Funktion. '
            'Negativ darf sie dabei sein — proportional sagt nur, dass b null ist.',
            f(r'f(x) = \fa{-0.5}\,x \qquad (\fb{b} = 0)', 300, 56),
            n('proportional:|durch @(0 \\mid 0)@', 460, 'blau', ein=2.2),
            graf(W_GLEICH, [ger(-0.5, 0)], [pt(0, 0, 2, '(0 | 0)')], ein=1.2)),
         sz('Frage 2',
            'x gleich vier ist eine senkrechte Gerade. Sie ordnet der einen Stelle vier unendlich viele y-Werte zu '
            'und ist darum keine Funktion.',
            f(r'x = 4', 300, 70),
            n('senkrecht —|@\\fd{keine\\ Funktion}@', 460, 'rot', ein=2.0),
            graf(W_GLEICH, punkte=[pt(4, y, 4) for y in (-3, -2, -1, 0, 1, 2, 3, 4)], ein=1.2)),
         sz('Frage 3',
            'Parallel heisst gleiche Steigung. Drei x minus drei hat dasselbe m gleich drei, aber ein anderes b.',
            f(r'y = \fa{3}x \fb{+ 2} \qquad y = \fa{3}x \fb{- 3}', 300, 50),
            n('gleiches @\\fa{m}@,|verschiedenes @\\fb{b}@', 460, 'blau', ein=2.2),
            graf(W_GLEICH, [ger(3, 2), ger(3, -3)], [pt(0, 2, 2), pt(0, -3, 2)], ein=1.2)),
         sz('Frage 4',
            'Senkrecht heisst Produkt minus eins. Zu vier gehört der negative Kehrwert: minus ein Viertel, '
            'also minus null Komma zwei fünf.',
            f(r'\fa{4} \cdot \fa{m_2} = -1 \;\Longrightarrow\; \fa{m_2} = \fa{-0.25}', 300, 52),
            n('negativer Kehrwert:|@-\\dfrac{1}{4}@', 460, 'blau', ein=2.2),
            graf(W_GLEICH, [ger(4, 1), ger(-0.25, 1)], [pt(0, 1, 5)], ein=1.2)),
         sz('Frage 5',
            'Null Komma fünf mal minus zwei ist minus eins. Die beiden Geraden stehen senkrecht aufeinander.',
            f(r'\fa{0.5} \cdot \fa{(-2)} = -1', 300, 62, ein=1.4),
            n('Produkt der Steigungen|ist @-1@: senkrecht', 460, 'blau', ein=2.6),
            graf(W_GLEICH, [ger(0.5, 2), ger(-2, -1)], [pt(0, 2, 2), pt(0, -1, 2)])),
         sz('Merke',
            'Zum Mitnehmen: b gleich null heisst proportional, m gleich null heisst konstant. '
            'x gleich k ist keine Funktion. Gleiches m heisst parallel, Produkt minus eins heisst senkrecht.',
            titel('Zum Mitnehmen', 240, 76),
            f(r'\fb{b} = 0:\ \text{proportional}', 380, 48, ein=0.4),
            f(r'\fa{m} = 0:\ \text{konstant}', 460, 48, ein=0.7),
            n('@\\fa{m_1} = \\fa{m_2}@: parallel|@\\fa{m_1} \\cdot \\fa{m_2} = -1@: senkrecht|@x = k@: keine Funktion',
              570, 'blau', 44, ein=1.4),
            graf(W_GLEICH, [ger(0.5, 2), ger(-2, -1)], [pt(0, 2, 2), pt(0, -1, 2)])),
     ], [
         wahl('Frage 1', 'f(x) = −0.5x: Welcher Typ ist das?',
              ['eine proportionale Funktion', 'eine konstante Funktion', 'die Identität'], 0,
              {0: 'Ja.',
               1: 'Konstant wäre m = 0. Hier steht ein x in der Gleichung — schau auf b.',
               2: 'Die Identität ist f(x) = x. Vergleich die Steigungen.'},
              sprich='f von x gleich minus null Komma fünf x: Welcher Typ ist das?',
              rueck_sprich={1: 'Konstant wäre m gleich null. Hier steht ein x in der Gleichung. Schau auf b.',
                            2: 'Die Identität ist f von x gleich x. Vergleich die Steigungen.'}),
         wahl('Frage 2', 'Was beschreibt x = 4?',
              ['eine senkrechte Gerade, keine Funktion', 'eine konstante Funktion', 'die Nullstelle einer Geraden'], 0,
              {0: 'Ja.',
               1: 'Konstant ist y = 4 — waagrecht. Hier ist die Stelle festgelegt, nicht der Wert.',
               2: 'Eine Nullstelle ist ein einzelner Punkt. x = 4 beschreibt alle Punkte mit dieser Stelle.'},
              sprich='Was beschreibt x gleich vier?',
              rueck_sprich={1: 'Konstant ist y gleich vier, waagrecht. Hier ist die Stelle festgelegt, nicht der Wert.',
                            2: 'Eine Nullstelle ist ein einzelner Punkt. x gleich vier beschreibt alle Punkte mit dieser Stelle.'}),
         wahl('Frage 3', 'g: y = 3x + 2. Welche Gerade ist parallel zu g?',
              ['y = 3x − 3', 'y = −3x + 2', 'y = 2x + 3'], 0,
              {0: 'Ja.',
               1: 'Dasselbe b, aber die Richtung ist gespiegelt. Parallel heisst gleiche Steigung.',
               2: 'Hier sind m und b vertauscht. Vergleich nur die Steigungen.'},
              sprich='g: y gleich drei x plus zwei. Welche Gerade ist parallel zu g?',
              rueck_sprich={1: 'Dasselbe b, aber die Richtung ist gespiegelt. Parallel heisst gleiche Steigung.',
                            2: 'Hier sind m und b vertauscht. Vergleich nur die Steigungen.'}),
         wahl('Frage 4', 'g: y = 4x − 1. Welche Steigung hat eine Gerade senkrecht zu g?',
              ['−0.25', '0.25', '−4'], 0,
              {0: 'Ja.',
               1: 'Der Kehrwert stimmt. Aber was sagt die Bedingung m₁ · m₂ = −1 über das Vorzeichen?',
               2: 'Nur das Vorzeichen gedreht — der Kehrwert fehlt.'},
              sprich='g: y gleich vier x minus eins. Welche Steigung hat eine Gerade senkrecht zu g?',
              rueck_sprich={1: 'Der Kehrwert stimmt. Aber was sagt die Bedingung m eins mal m zwei gleich minus eins über das Vorzeichen?',
                            2: 'Nur das Vorzeichen ist gedreht. Der Kehrwert fehlt.'}),
         wahl('Frage 5', 'Wie liegen die beiden Geraden im Bild zueinander?',
              ['senkrecht', 'parallel', 'identisch'], 0,
              {0: 'Ja.',
               1: 'Parallel wäre gleiche Richtung. Die eine steigt, die andere fällt — rechne m₁ · m₂.',
               2: 'Identisch wären sie nur als eine einzige Linie im Bild.'},
              rueck_sprich={1: 'Parallel wäre gleiche Richtung. Die eine steigt, die andere fällt. Rechne m eins mal m zwei.',
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
            graf(W_GLEICH, [ger(-2, 3)], [pt(2, -1, 5, 'P(2 | −1)')])),
         sz('m und ein Punkt',
            'Erster Fall: die Steigung minus zwei und der Punkt P zwei, minus eins. '
            'Das bekannte m kommt in den Ansatz, offen bleibt nur b.',
            f(r'y = \fa{-2}x + \fb{b}', 300, 70),
            n('@\\fa{m}@ einsetzen —|eine Unbekannte bleibt', 460, 'blau'),
            graf(W_GLEICH, [ger(-2, 3)], [pt(2, -1, 5, 'P(2 | −1)')])),
         sz('Punkt einsetzen',
            'Jetzt der Punkt: seine x-Koordinate für x, seine y-Koordinate für y. Minus eins gleich minus zwei '
            'mal zwei plus b — also b gleich drei. Die Gerade lautet y gleich minus zwei x plus drei.',
            f(r'-1 = \fa{-2} \cdot 2 + \fb{b} \;\Longrightarrow\; \fb{b} = 3', 300, 52),
            n('Probe: @\\fa{-2} \\cdot 2 + \\fb{3} = -1@ ✓', 460, 'gruen'),
            graf(W_GLEICH, [ger(-2, 3)], [pt(2, -1, 5, 'P'), pt(0, 3, 2, '(0 | 3)')])),
         sz('Zwei Punkte: erst m',
            'Zweiter Fall: zwei Punkte. A liegt bei minus zwei, minus zwei, B bei eins, vier. '
            'Zuerst die Steigung: vier minus minus zwei ist sechs, geteilt durch drei — m gleich zwei.',
            f(r'\fa{m} = \frac{4 - (-2)}{1 - (-2)} = \frac{6}{3} = \fa{2}', 300, 54),
            n('Schritt 1:|@\\fa{m}@ aus den beiden Punkten', 460, 'blau'),
            graf(W_GLEICH, [ger(2, 2)], [pt(-2, -2, 5, 'A(−2 | −2)'), pt(1, 4, 5, 'B(1 | 4)')])),
         sz('Zwei Punkte: dann b',
            'Dann b: Setz einen der beiden Punkte ein. Vier gleich zwei mal eins plus b gibt b gleich zwei. '
            'Die Gerade lautet y gleich zwei x plus zwei. Die Probe mit A bestätigt es.',
            f(r'4 = \fa{2} \cdot 1 + \fb{b} \;\Longrightarrow\; \fb{b} = 2', 300, 52),
            n('Probe mit @A@:|@\\fa{2} \\cdot (-2) + \\fb{2} = -2@ ✓', 460, 'gruen'),
            graf(W_GLEICH, [ger(2, 2)], [pt(-2, -2, 5, 'A'), pt(1, 4, 5, 'B'),
                                         pt(0, 2, 2, '(0 | 2)')])),
         sz('Aus einer Lage',
            'Dritter Fall: Gesucht ist eine Gerade senkrecht zu y gleich zwei x plus zwei, durch den Punkt eins, eins. '
            'Senkrecht gibt m gleich minus ein Halb — und dann weiter wie vorher: Punkt einsetzen, b ausrechnen.',
            f(r'\fa{m} = -\frac{1}{2}: \quad 1 = \fa{-0.5} \cdot 1 + \fb{b}', 300, 50),
            n('@\\fb{b} = 1.5@, also|@y = \\fa{-0.5}x + \\fb{1.5}@', 460, 'blau'),
            graf(W_GLEICH, [ger(2, 2, 5, gestrichelt=True), ger(-0.5, 1.5)],
                 [pt(1, 1, 5, 'P(1 | 1)')])),
         sz('Aus einem Sachtext',
            'Vierter Fall: Auch in einem Text stecken m und b. Taxi: sechs Franken Grundtaxe und drei Franken '
            'pro Kilometer. Pro Kilometer ist die Steigung, die Grundtaxe der Achsenabschnitt.',
            f(r'K(x) = \fa{3}\,x + \fb{6}', 300, 66),
            n('«pro Kilometer» @\\to \\fa{m}@|«Grundtaxe» @\\to \\fb{b}@', 460, 'blau'),
            graf(W_TAXI, [ger(3, 6)], [pt(0, 6, 2, '(0 | 6)')], xname='x [km]', yname='K [CHF]')),
         sz('Merke',
            'Zum Mitnehmen: Der Ansatz ist immer y gleich m x plus b. Was gegeben ist, wird eingesetzt; '
            'zwei Punkte geben zuerst m, dann b. Und am Schluss immer die Probe.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'y = \fa{m}\,x + \fb{b} \qquad \fb{b} = y_1 - \fa{m}\,x_1', 420, 56, ein=0.4),
            n('@\\fa{m}@ gegeben: Punkt einsetzen|zwei Punkte: erst @\\fa{m}@, dann @\\fb{b}@|parallel oder senkrecht: zuerst @\\fa{m}@',
              560, 'blau', 44, ein=1.2),
            graf(W_GLEICH, [ger(2, 2)], [pt(-2, -2, 5), pt(1, 4, 5), pt(0, 2, 2)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-aufstellen', 'Gerade sehen: Kontrollfragen zum Aufstellen',
     'Fünf Vorhersagen zum Aufstellen der Geradengleichung — aus m und Punkt, aus zwei Punkten, aus einer Lage und aus einem Text.',
     ['Geradengleichung', 'aufstellen', 'zwei Punkte', 'parallel', 'Kontrollfragen'], [
         sz('Frage 1',
            'Punkt einsetzen: eins gleich drei mal zwei plus b. Sechs auf die andere Seite — b gleich minus fünf.',
            f(r'1 = \fa{3} \cdot 2 + \fb{b} \;\Longrightarrow\; \fb{b} = \fb{-5}', 300, 52),
            n('@\\fb{b} = y_1 - \\fa{m}\\,x_1 = 1 - 6@', 460, 'orange', ein=2.2),
            graf(W_KF1, [ger(3, -5)], [pt(2, 1, 5, 'P(2 | 1)'), pt(0, -5, 2, '(0 | −5)')], ein=1.2)),
         sz('Frage 2',
            'Von A nach B: null minus vier ist minus vier, zwei minus null ist zwei. m gleich minus zwei. '
            'Und b steht schon da: A liegt auf der y-Achse, also vier.',
            f(r'\fa{m} = \frac{0 - 4}{2 - 0} = \fa{-2}, \quad \fb{b} = \fb{4}', 300, 50),
            n('@A(0 \\mid 4)@ liegt auf der @y@-Achse:|@\\fb{b}@ ist direkt gegeben', 460, 'orange', ein=2.4),
            graf(W_GLEICH, [ger(-2, 4)], [pt(0, 4, 2, 'A(0 | 4)'), pt(2, 0, 5, 'B(2 | 0)')], ein=1.2)),
         sz('Frage 3',
            'Punkt einsetzen und nach m auflösen: eins gleich m mal vier plus fünf gibt vier m gleich minus vier, '
            'also m gleich minus eins.',
            f(r'1 = \fa{m} \cdot 4 + \fb{5} \;\Longrightarrow\; \fa{m} = \fa{-1}', 300, 52),
            n('Diesmal ist @\\fb{b}@ gegeben|und @\\fa{m}@ gesucht', 460, 'blau', ein=2.2),
            graf(W_GLEICH, [ger(-1, 5)], [pt(4, 1, 5, 'P(4 | 1)'), pt(0, 5, 2)], ein=1.2)),
         sz('Frage 4',
            'Parallel heisst gleiches m, also minus drei. Punkt einsetzen: vier gleich minus drei mal eins plus b, '
            'also b gleich sieben.',
            f(r'4 = \fa{-3} \cdot 1 + \fb{b} \;\Longrightarrow\; \fb{b} = \fb{7}', 300, 52),
            n('parallel: @\\fa{m}@ übernehmen,|dann Punkt einsetzen', 460, 'blau', ein=2.2),
            graf(W_GLEICH, [ger(-3, 2, 5, gestrichelt=True), ger(-3, 7)], [pt(1, 4, 5, 'P(1 | 4)')], ein=1.2)),
         sz('Frage 5',
            'Pro Minute vier Liter mehr: Das ist die Steigung. Achtzig Liter zu Beginn, also bei t gleich null: '
            'Das ist der Achsenabschnitt. V von t gleich vier t plus achtzig.',
            f(r'V(t) = \fa{4}\,t + \fb{80}', 300, 66),
            n('«pro Minute» @\\to \\fa{m}@|«zu Beginn» @\\to \\fb{b}@', 460, 'blau', ein=2.2),
            graf(dict(xbereich=[-2, 22], ybereich=[-20, 180],
                      xteilung=[[0, '0'], [10, '10'], [20, '20']],
                      yteilung=[[0, '0'], [80, '80'], [160, '160']]),
                 [ger(4, 80)], [pt(0, 80, 2, '(0 | 80)')], xname='t [min]', yname='V [l]', ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Immer derselbe Ansatz y gleich m x plus b. Zwei Punkte geben zuerst m, dann b. '
            'Parallel übernimmt m, senkrecht nimmt den negativen Kehrwert. Im Sachtext ist «pro» die Steigung.',
            titel('Zum Mitnehmen', 260, 76),
            f(r'\fb{b} = y_1 - \fa{m}\,x_1', 420, 62, ein=0.4),
            n('zwei Punkte: erst @\\fa{m}@, dann @\\fb{b}@|parallel: gleiches @\\fa{m}@|«pro …» @\\to \\fa{m}@, «zu Beginn» @\\to \\fb{b}@',
              560, 'blau', 44, ein=1.2),
            graf(W_GLEICH, [ger(-3, 7)], [pt(1, 4, 5)])),
     ], [
         wahl('Frage 1', 'm = 3 und P(2 | 1): Wie gross ist b?',
              ['−5', '7', '5'], 0,
              {0: 'Ja.',
               1: 'Vorzeichen: b = y₁ − m·x₁, also 1 − 6 — nicht 1 + 6.',
               2: 'Der Betrag stimmt. Zieh m·x₁ ab, statt es dazuzuzählen.'},
              sprich='m gleich drei und P zwei, eins: Wie gross ist b?',
              rueck_sprich={1: 'Das Vorzeichen: b ist y eins minus m mal x eins, also eins minus sechs. Nicht eins plus sechs.',
                            2: 'Der Betrag stimmt. Zieh m mal x eins ab, statt es dazuzuzählen.'}),
         wahl('Frage 2', 'A(0 | 4) und B(2 | 0): Welche Gleichung gehört zur Geraden durch A und B?',
              ['y = −2x + 4', 'y = 2x + 4', 'y = −0.5x + 4'], 0,
              {0: 'Ja.',
               1: 'Der Achsenabschnitt stimmt. Aber von A nach B geht es hinauf oder hinunter?',
               2: 'Bruch verkehrt: 2 nach rechts, 4 hinunter.'},
              sprich='A null, vier und B zwei, null: Welche Gleichung gehört zur Geraden durch A und B?',
              rueck_sprich={1: 'Der Achsenabschnitt stimmt. Aber geht es von A nach B hinauf oder hinunter?',
                            2: 'Der Bruch ist verkehrt: zwei nach rechts, vier hinunter.'}),
         wahl('Frage 3', 'b = 5 und P(4 | 1): Wie gross ist m?',
              ['−1', '1', '−0.25'], 0,
              {0: 'Ja.',
               1: 'Von (0 | 5) nach (4 | 1) geht es hinunter. Welches Vorzeichen hat m dann?',
               2: 'Bruch verkehrt: Δy = −4 geteilt durch Δx = 4.'},
              sprich='b gleich fünf und P vier, eins: Wie gross ist m?',
              rueck_sprich={1: 'Von null, fünf nach vier, eins geht es hinunter. Welches Vorzeichen hat m dann?',
                            2: 'Der Bruch ist verkehrt: delta y gleich minus vier, geteilt durch delta x gleich vier.'}),
         wahl('Frage 4', 'Gesucht: die Gerade parallel zu y = −3x + 2 durch P(1 | 4).',
              ['y = −3x + 7', 'y = −3x + 4', 'y = ⅓x + 4'], 0,
              {0: 'Ja.',
               1: 'Die Steigung stimmt. Aber liegt P(1 | 4) wirklich auf y = −3x + 4? Setz ein.',
               2: 'Das wäre etwas anderes als parallel — und b ist auch nicht einfach die y-Koordinate von P.'},
              sprich='Gesucht ist die Gerade parallel zu y gleich minus drei x plus zwei, durch P eins, vier.',
              rueck_sprich={1: 'Die Steigung stimmt. Aber liegt P eins, vier wirklich auf y gleich minus drei x plus vier? Setz ein.',
                            2: 'Das wäre etwas anderes als parallel. Und b ist auch nicht einfach die y-Koordinate von P.'}),
         wahl('Frage 5', 'Ein Behälter enthält 80 Liter; pro Minute fliessen 4 Liter zu. Welche Gleichung?',
              ['V(t) = 4t + 80', 'V(t) = 80t + 4', 'V(t) = −4t + 80'], 0,
              {0: 'Ja.',
               1: 'Vertauscht: Welche der beiden Zahlen gehört zu «pro Minute»?',
               2: 'Es fliesst zu, nicht ab. Welches Vorzeichen hat m dann?'},
              sprich='Ein Behälter enthält achtzig Liter; pro Minute fliessen vier Liter zu. Welche Gleichung?',
              rueck_sprich={1: 'Vertauscht: Welche der beiden Zahlen gehört zu «pro Minute»?',
                            2: 'Es fliesst zu, nicht ab. Welches Vorzeichen hat m dann?'}),
     ], art='Kontrollclip')
