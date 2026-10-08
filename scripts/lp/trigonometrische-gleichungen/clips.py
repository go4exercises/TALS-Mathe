"""Erzeugt die acht Drehbücher des Leitprogramms Trigonometrische Gleichungen (07.10.2026).

  python3 scripts/lp/trigonometrische-gleichungen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie in Planimetrie: Rechnung und Notizen links (x 150), das Bild rechts — der Einheitskreis
in einem gleich geteilten Fenster (x 1010, y 175, 760 × 760; beim Tangens ein hohes Fenster
500 × 860, weil S(1 | c) über den Kreis hinausragt). Kapitel 4 braucht Breite für die Kurve: dort
steht das Bild unten über die ganze Bühne (x 140, y 500, 1640 × 480) wie in trigonometrische-
funktionen/clips.py.

Winkel in Grad (Themenseite 5.5). Der Einheitskreis mit dem laufenden Punkt P ist der Begleiter
`kreis` einer Sinus- bzw. Tangenskurve (HOWTO-clips «Sinus- und Tangenskurven»); die Kurve selbst
ist in den Kreis-Clips ausgeblendet (`von` = `bis` ausserhalb des Fensters), `bahn` ist im
Bogenmass. Die Kurven von Kapitel 4 rechnen intern im Bogenmass, die x-Achse ist in Grad
beschriftet (`xteilung`) — Behelf, weil der Kreis-Begleiter sein P in Bogenmass-Einheiten auf die
Kurve projiziert. Die Klickfrage in Kapitel 4 zeichnet dagegen sin(x·π/180) in Grad, damit die
Eingabe ohne Zeigegerät Grad verlangt.

Fragebild (HOWTO-leitprogramme §15): Beim Erscheinen einer Frage zeigt das Bild nur das Gegebene
(erster `graf` der Szene, ab 0.05 s, `tippbar`); die Auflösung kommt ab 1.0 s. Gebaut hier mit
`frage_bild()`, nicht über scripts/lp/fragebild.py (gemeinsame Datei, nicht anfassen).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Sinus (Höhe von P), Lösungen von sin φ = c      \\fa{…}
  2 orange = Tangens (Punkt S auf der Tangente), Lösungen von tan φ = c   \\fb{…}
  3 grün   = Cosinus (waagrechte Koordinate), Lösungen von cos φ = c    \\fc{…}
  4 rot    = Gegenbeispiel, falscher Weg                          \\fd{…}
  5 Tinte  = neutral: Einheitskreis, Gerade y = c bzw. x = c, Tangente x = 1
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
P = math.pi
H2 = P / 2
LX = 150
GX, GY, GB, GH = 1010, 175, 760, 760          # Kreisbild rechts
TX, TY, TB, TH = 1240, 180, 500, 860          # hohes Bild beim Tangens
KX, KY, KB, KH = 140, 500, 1640, 480          # Kurvenbild unten (Kapitel 4)
rad = math.radians


def c3(w):
    """Punkt auf dem Einheitskreis zum Winkel w (Grad), gerundet."""
    return [round(math.cos(rad(w)), 4), round(math.sin(rad(w)), 4)]


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


# Fenster: Einheitskreis gleich geteilt (2.9 × 2.9 auf 760 × 760)
WK = dict(xbereich=[-1.45, 1.45], ybereich=[-1.45, 1.45], xteilung=yt(-1, 1), yteilung=yt(-1, 1),
          xname='x', yname='y')
WK5 = dict(WK, xteilung=yt(-1, -0.5, 0.5, 1), yteilung=yt(-1, -0.5, 0.5, 1))
# Kontrollfrage y = 1.4: weiteres Fenster, sonst läuft die Gerade durch Pfeil und «y» (Prüfung 08.10.2026)
WK7 = dict(WK, xbereich=[-1.7, 1.7], ybereich=[-1.7, 1.7])
# Tangens: 3.2 × 5.5 auf 500 × 860 (gleich geteilt bis auf die 8 px Rand)
WT = dict(xbereich=[-1.6, 1.6], ybereich=[-2.75, 2.75], xteilung=yt(-1, 1), yteilung=yt(-2, -1, 1, 2),
          xname='x', yname='y')
# Kurve in Grad beschriftet, intern Bogenmass; Kreis bei mx = −1.8 links der y-Achse
GRAD = {k: '%d°' % (k * 90) for k in range(-8, 9)}


def gt(*viertel):
    return [[k * H2, GRAD[k].replace('-', '−')] for k in viertel]


WKK = dict(xbereich=[-3.6, 13.0], ybereich=[-1.5, 1.5], xteilung=gt(1, 2, 3, 4, 5, 6, 7, 8), yteilung=yt(-1, 1),
           xname='φ', yname='y')
WKN = dict(xbereich=[-6.9, 6.9], ybereich=[-1.5, 1.5], xteilung=gt(-4, -3, -2, -1, 1, 2, 3, 4), yteilung=yt(-1, 1),
           xname='φ', yname='y')
WKT = dict(xbereich=[-0.8, 13.0], ybereich=[-3, 3], xteilung=gt(1, 2, 3, 4, 5, 6, 7, 8), yteilung=yt(-2, -1, 1, 2),
           xname='φ', yname='y')


def graf(W, kurven=(), punkte=(), figuren=(), ein=0.05, gross='kreis', **kw):
    lage = {'kreis': (GX, GY, GB, GH), 'tan': (TX, TY, TB, TH), 'kurve': (KX, KY, KB, KH)}[gross]
    g = dict(typ='graf', x=lage[0], y=lage[1], breite=lage[2], hoehe=lage[3], abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, **W)
    g.update(kw)
    return g


def KR(farbe=5, dicke=3):
    return dict(art='kreis', m=[0, 0], r=1, farbe=farbe, dicke=dicke)


def S(a, b, farbe=5, gest=False, dicke=4, **kw):
    d = dict(art='strecke', von=list(a), bis=list(b), farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=30, **kw):
    return dict(art='text', bei=[x, y], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=False, **kw)


def WI(von, bis, farbe=1, r=60, **kw):
    return dict(art='winkel', bei=[0, 0], von=von, bis=bis, farbe=farbe, r_px=r, **kw)


def pt(x, y, farbe=1, text=None, bei=None, anker='start', **kw):
    d = dict(x=round(x, 4), y=round(y, 4), farbe=farbe, anker=anker, **kw)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = [round(bei[0], 3), round(bei[1], 3)]
    return d


def kp(w, farbe=1, text=None, aussen=1.22, **kw):
    """Punkt auf dem Kreis beim Winkel w (Grad), Beschriftung radial aussen."""
    x, y = c3(w)
    if text is None:
        return pt(x, y, farbe, **kw)
    bx, by = aussen * math.cos(rad(w)), aussen * math.sin(rad(w))
    anker = 'start' if bx > 0.15 else ('end' if bx < -0.15 else 'middle')
    return pt(x, y, farbe, text, [bx, by - 0.06], anker, **kw)


def kpb(w, farbe, text, bei, anker='end', **kw):
    """Punkt auf dem Kreis mit frei gesetzter Beschriftung — wo die radiale Lage mit S zusammenstösst."""
    x, y = c3(w)
    return pt(x, y, farbe, text, bei, anker, **kw)


def kpt(w, farbe, text, dreh=-16, r_=1.3, **kw):
    """Punkt auf der Geraden durch O (Tangens): Beschriftung neben der Geraden statt radial auf ihr
    (Prüfung 08.10.2026: radiale Beschriftungen wurden von der Geraden durchkreuzt)."""
    x, y = c3(w)
    bx, by = r_ * math.cos(rad(w + dreh)), r_ * math.sin(rad(w + dreh))
    anker = 'start' if bx > 0.15 else ('end' if bx < -0.15 else 'middle')
    return pt(x, y, farbe, text, [bx, by - 0.06], anker, **kw)


def p_name(w, ein, aus=None, r_=1.17):
    """Name «P» am laufenden Punkt — Behelf: der Kreis-Begleiter beschriftet P nicht (Wunsch an den Clip-Bauer)."""
    d = T(r_ * math.cos(rad(w)) + 0.02, r_ * math.sin(rad(w)) + 0.06, 'P', 5, 'start' if math.cos(rad(w)) > -0.2 else 'end', 32, ein=ein)
    d['kursiv'] = True
    if aus is not None:
        d['aus'] = aus
    return d


def lauf(bahn, art='sin', farbe=1, ein=None):
    """Der laufende Punkt P mit Radius und Bogen: Kreis-Begleiter einer ausgeblendeten Kurve.
    bahn: [[t, Winkel in Grad], …]."""
    kr = {'mx': 0, 'bahn': [[t, round(rad(w), 5)] for t, w in bahn], 'spur': False, 'projektion': False, 'farbe': farbe}
    if art == 'cos':
        kr['art'] = 'cos'
    d = {'bewegung': [[0, 1, 1, 0, 0]], 'trig': 'tan' if art == 'tan' else 'sin', 'farbe': farbe,
         'von': 99, 'bis': 99, 'kreis': kr}
    if ein is not None:
        d['ein'] = ein
    return d


def halbkreise():
    """Obere und untere Kreishälfte als Formelkurven — Ziel der mitlaufenden Schnittpunkte."""
    return [dict(formel='sqrt(1-x**2)', farbe=5, dicke=3), dict(formel='-sqrt(1-x**2)', farbe=5, dicke=3)]


def waagrechte_bewegt(stuetz, farbe=1, ein=None):
    """Bewegte Waagrechte y = c ([t, c], …) mit ihren Schnittpunkten auf beiden Kreishälften
    (kurven 0 und 1 des graf müssen die Halbkreise sein)."""
    out = []
    for k in (0, 1):
        g = {'bewegung': [[t, 0, c] for t, c in stuetz], 'farbe': 5, 'gestrichelt': True, 'dicke': 3,
             'schnitte': {'kurve': k, 'farbe': farbe, 'beschriftung': False, 'anzahl': 2}}
        if ein is not None:
            g['ein'] = ein
        out.append(g)
    return out


def f(t, y, g=54, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4, x=LX):
    return dict(typ='notiz', text=t, x=x, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=82):
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
          tol=0.18, bei=0.3, eingabe=('x', 'y')):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    if eingabe:
        d['eingabe'] = list(eingabe)   # Antwort ohne Zeigegeraet: zwei Zahlfelder (build-clips.py)
    return d


def frage_bild(g):
    """Fragebild: das Gegebene ab 0.05 s, tippbar für Klickfragen (HOWTO-leitprogramme §15)."""
    g = dict(g)
    g['ein'] = 0.05
    g['tippbar'] = True
    return g


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'
FALSCH_SPR = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/g5-5-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 'g5-5-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Trigonometrische Gleichungen',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-5'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Winkel finden',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms trigonometrische-gleichungen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


FOLGE = {}
# Polgeraden des Tangens anders als die Waagrechte y = c (beide waren Tinte gestrichelt): rot wie «nicht definiert»
# im Clip tangens (90°, 270°). Der Bauer kennt für asymptoten nur die Farbe, keine eigene Strichart.
POLE = {'farbe': 4}
# Szene «Besondere Werte» (einheitskreis), neu vertont 08.10.2026 — Zeiten nach sprechzeiten.py: «Sinus von 30°» 3.8–5.8,
# «von 45°» 6.1–8.6, «von 60°» 8.8–10.9, «Beim Cosinus» 11.2
TAB_SIN, TAB_COS = 3.8, 11.2
BW_30, BW_45, BW_60 = 4.6, 6.4, 9.1


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# Beispiele der Themenseite: sin φ = 1/2 (30°, 150°; Abschnitt «Lösungsmenge angeben», Häufiger Fehler)
# und cos φ = −1/2 (120°, 240°; Tabelle «Spezialfälle»).
clip('einheitskreis', 'Winkel finden: Gleichungen am Einheitskreis',
     'Sinus ist die Höhe, Cosinus die waagrechte Koordinate von P: sin φ = c heisst Waagrechte y = c, cos φ = c '
     'Senkrechte x = c. Die Schnittpunkte mit dem Kreis sind die Lösungen — zwei, eine oder keine.',
     ['Trigonometrische Gleichung', 'Einheitskreis', 'Sinus', 'Cosinus', 'Lösungsmenge'], [
         sz('Die Frage',
            'Für welche Winkel Phi ist Sinus von Phi gleich ein Halb? Am Einheitskreis ist der Sinus die Höhe des Punktes P. '
            'Gesucht sind also die Punkte des Kreises auf der Höhe ein Halb.',
            f(r'\fa{\sin\varphi} = \tfrac{1}{2}', 300, 66, ein=0.4),
            # Wortzeiten (faster-whisper): «Höhe des Punktes P» 5.8–6.6, «auf der Höhe ein Halb» 9.3–9.8
            n('Sinus = Höhe von @P@', 420, 'blau', 46, ein=4.8),
            graf(WK, [lauf([[0, 0], [4.8, 0], [6.6, 60], [7.4, 60], [9.6, 30]])], ein=0.3,
                 figuren=[KR(), p_name(0, 0.3, 4.8), p_name(60, 6.6, 7.4), p_name(30, 9.6)],
                 geraden=[dict(m=0, q=0.5, farbe=5, gestrichelt=True, dicke=3, ein=9.3)])),
         sz('Zwei Punkte',
            'Die Waagrechte y gleich ein Halb schneidet den Kreis in zwei Punkten. Rechts liegt P eins bei dreissig Grad. '
            'Links liegt P zwei, das Spiegelbild an der y-Achse: hundertachtzig minus dreissig, also hundertfünfzig Grad.',
            # «zwei Punkten» 3.6, «P eins bei 30°» 4.9–5.6, «P zwei» 7.1, «Spiegelbild» 8.0, «180» 10.1, «150°» 12.2
            f(r'\varphi_1 = 30^\circ', 300, 56, ein=5.6),
            f(r'\varphi_2 = 180^\circ - 30^\circ = 150^\circ', 400, 56, ein=12.0),   # «150» erst bei 12.0 gesprochen
            n('Spiegelbild an der @y@-Achse', 500, 'blau', 44, ein=8.0),
            graf(WK, [lauf([[0, 30], [6.5, 30], [7.6, 150]])], ein=0.05,
                 figuren=[KR(), S((-1.45, 0.5), (1.45, 0.5), 5, True, 3),
                          WI(0, 30, 1, 64, ein=5.6), T(0.42, 0.11, '30°', 1, 'start', 28, ein=5.6),
                          S((0, -1.4), (0, 1.4), 1, True, 2, ein=8.0)],
                 punkte=[kp(30, 5, ein=3.6), kp(150, 5, ein=3.6), kp(30, 1, 'P₁', ein=4.9), kp(150, 1, 'P₂', ein=7.1)])),
         sz('Beim Cosinus',
            'Beim Cosinus zählt die waagrechte Koordinate. Cosinus von Phi gleich minus ein Halb heisst: Die Senkrechte '
            'x gleich minus ein Halb schneidet den Kreis. Oben bei hundertzwanzig Grad, unten bei zweihundertvierzig Grad. '
            'Die beiden Punkte sind Spiegelbilder an der x-Achse.',
            # «Cosinus von Phi gleich minus ein Halb» 3.1, «Senkrechte» 5.6, «120°» 8.8, «240°» 10.5, «Spiegelbilder» 13.0
            f(r'\fc{\cos\varphi} = -\tfrac{1}{2}', 300, 62, ein=3.1),
            f(r'\varphi_1 = 120^\circ, \quad \varphi_2 = 240^\circ', 420, 54, ein=10.5),
            n('Spiegelbild an der @x@-Achse', 520, 'gruen', 44, ein=13.0),
            graf(WK, [lauf([[0, 0], [7.4, 0], [8.8, 120], [9.6, 120], [10.6, 240]], 'cos', 3)], ein=0.05,
                 figuren=[KR(), S((-0.5, -1.45), (-0.5, 1.45), 5, True, 3, ein=5.6),
                          S((-1.4, 0), (1.4, 0), 3, True, 2, ein=13.0)],
                 punkte=[kp(120, 3, '120°', ein=8.8), kp(240, 3, '240°', ein=10.6)])),
         sz('Wie viele?',
            'Wie viele Lösungen es gibt, hängt von c ab. Schiebt man die Waagrechte nach oben, rücken die beiden Punkte '
            'zusammen. Bei c gleich eins berühren sie sich: nur noch eine Lösung, neunzig Grad. Darüber trifft die '
            'Waagrechte den Kreis nicht mehr. Die Lösungsmenge ist leer.',
            # «schiebt man die Waagrechte nach oben» 3.3–4.4, «c gleich eins» 6.8–7.3, «eine Lösung, 90°» 8.7–9.2,
            # «Darüber» 10.4, «Die Lösungsmenge ist leer» 12.4–13.8
            n('@c = 1@: eine Lösung, @90^\\circ@', 300, 'blau', 44, ein=8.7),
            n('@c \\gt 1@: @\\mathbb{L} = \\{\\,\\}@', 400, 'rot', 44, ein=12.9),
            f(r'\text{lösbar für } -1 \leq c \leq 1', 510, 50, ein=13.8),
            graf(WK, halbkreise(), ein=0.05, figuren=[KR()],
                 geraden=waagrechte_bewegt([[0, 0.5], [3.3, 0.5], [7.0, 1.0], [10.4, 1.0], [11.8, 1.3]]))),
         sz('Besondere Werte',
            'Für besondere Werte kennst du die Winkel vom Einheitskreis: Sinus von dreissig Grad ist ein Halb, '
            'von fünfundvierzig Grad Wurzel zwei halbe, von sechzig Grad Wurzel drei halbe. '
            'Beim Cosinus ist es umgekehrt. Die übrigen Lösungen holst du über die Spiegelung.',
            # Zwei deckungsgleiche Tabellen (\phantom hält die Masse gleich): die Sinuszeile mit dem Ton, die Cosinuszeile
            # bei «Beim Cosinus» — vorher stand die ganze Tabelle ab 0.6 s (Prüfung 08.10.2026). Zeiten: TAB_SIN, TAB_COS.
            f(r'\begin{array}{c|ccc} \varphi & 30^\circ & 45^\circ & 60^\circ \\ \hline '
              r'\fa{\sin\varphi} & \tfrac{1}{2} & \tfrac{\sqrt{2}}{2} & \tfrac{\sqrt{3}}{2} \\[4pt] '
              r'\phantom{\fc{\cos\varphi}} & \phantom{\tfrac{\sqrt{3}}{2}} & \phantom{\tfrac{\sqrt{2}}{2}} & \phantom{\tfrac{1}{2}} \end{array}', 300, 46, ein=TAB_SIN),
            f(r'\begin{array}{c|ccc} \phantom{\varphi} & \phantom{30^\circ} & \phantom{45^\circ} & \phantom{60^\circ} \\ \phantom{\fa{\sin\varphi}} & \phantom{\tfrac{1}{2}} & \phantom{\tfrac{\sqrt{2}}{2}} & \phantom{\tfrac{\sqrt{3}}{2}} \\[4pt] '
              r'\fc{\cos\varphi} & \tfrac{\sqrt{3}}{2} & \tfrac{\sqrt{2}}{2} & \tfrac{1}{2} \end{array}', 300, 46, ein=TAB_COS),
            graf(WK, [], ein=0.05,
                 figuren=[KR(), S(c3(30), (c3(30)[0], 0), 1, False, 4, ein=BW_30), S(c3(45), (c3(45)[0], 0), 1, False, 4, ein=BW_45),
                          S(c3(60), (c3(60)[0], 0), 1, False, 4, ein=BW_60)],
                 punkte=[kp(30, 1, '30°', ein=BW_30), kp(45, 1, '45°', ein=BW_45), kp(60, 1, '60°', ein=BW_60)])),
         sz('Merke',
            'Zum Mitnehmen: Sinus von Phi gleich c heisst Waagrechte y gleich c, Cosinus von Phi gleich c heisst Senkrechte '
            'x gleich c. Die Schnittpunkte mit dem Kreis sind die Lösungen: zwei, eine oder keine. Die zweite ist das '
            'Spiegelbild: beim Sinus hundertachtzig Grad minus Phi eins, beim Cosinus dreihundertsechzig Grad minus Phi eins.',
            titel('Zum Mitnehmen', 260, 72),
            n('@\\fa{\\sin\\varphi = c}@: Waagrechte @y = c@|@\\fc{\\cos\\varphi = c}@: Senkrechte @x = c@', 360, 'blau', 42, ein=1.4),
            n('@\\fa{\\varphi_2 = 180^\\circ - \\varphi_1}@|@\\fc{\\varphi_2 = 360^\\circ - \\varphi_1}@', 560, 'blau', 42, ein=11.2),
            graf(WK, [], ein=0.3, figuren=[KR(), S((-1.45, 0.5), (1.45, 0.5), 5, True, 3)],
                 punkte=[kp(30, 1), kp(150, 1)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-einheitskreis', 'Winkel finden: Kontrollfragen am Einheitskreis',
     'Fünf Fragen: welche Gleichung zu einer Geraden gehört, wo eine Lösung liegt, wie viele es gibt.',
     ['Trigonometrische Gleichung', 'Einheitskreis', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Waagrechte liegt auf der Höhe minus null Komma vier. Die Höhe ist der Sinus: Das Bild zeigt Sinus von Phi '
            'gleich minus null Komma vier.',
            f(r'\fa{\sin\varphi} = -0.4', 300, 60, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR(), S((-1.45, -0.4), (1.45, -0.4), 5, True, 3)])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-1.45, -0.4), (1.45, -0.4), 5, True, 3),
                                           S(c3(-23.58), (c3(-23.58)[0], 0), 1, False, 4),
                                           S(c3(203.58), (c3(203.58)[0], 0), 1, False, 4)],
                 punkte=[kp(-23.58, 1), kp(203.58, 1)])),
         sz('Frage 2',
            'Cosinus ist die waagrechte Koordinate: Die Senkrechte x gleich null Komma sechs trifft den Kreis oben und unten. '
            'Im vierten Quadranten liegt der Punkt null Komma sechs, minus null Komma acht.',
            f(r'\fc{\cos\varphi} = 0.6', 300, 60, ein=1.0),
            n('IV. Quadrant: @(0.6 \\mid -0.8)@', 410, 'gruen', 44, ein=1.2),
            frage_bild(graf(WK5, [], figuren=[KR()])),
            graf(WK5, [], ein=1.0, figuren=[KR(), S((0.6, -1.45), (0.6, 1.45), 5, True, 3)],
                 punkte=[pt(0.6, 0.8, 3), pt(0.6, -0.8, 3, '(0.6 | −0.8)', [0.68, -1.0])])),
         sz('Frage 3',
            'Die Senkrechte x gleich minus eins berührt den Kreis nur in einem Punkt, bei hundertachtzig Grad: eine Lösung.',
            f(r'\fc{\cos\varphi} = -1\colon \; \mathbb{L} = \{180^\circ\}', 300, 56, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-1, -1.45), (-1, 1.45), 5, True, 3)],
                 punkte=[kp(180, 3, '180°', aussen=1.15)])),
         sz('Frage 4',
            'Sinus von fünfundvierzig Grad ist Wurzel zwei halbe. Das Spiegelbild an der y-Achse liegt bei hundertfünfunddreissig '
            'Grad. Beide liegen über der x-Achse.',
            f(r'\mathbb{L} = \{45^\circ;\ 135^\circ\}', 300, 58, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-1.45, 0.7071), (1.45, 0.7071), 5, True, 3)],
                 # falsche Angebote rot (HOWTO §15): 315° und 225° liegen unter der x-Achse
                 punkte=[kp(45, 1, '45°'), kp(135, 1, '135°'), kp(225, 4, '225°'), kp(315, 4, '315°')])),
         sz('Frage 5',
            'Der Kreis hat den Radius eins. Die Waagrechte y gleich eins Komma vier liegt über ihm und trifft ihn nie: '
            'Die Lösungsmenge ist leer.',
            f(r'\fa{\sin\varphi} = 1.4\colon \; \mathbb{L} = \{\,\}', 300, 58, ein=1.0),
            frage_bild(graf(WK7, [], figuren=[KR()])),
            graf(WK7, [], ein=1.0, figuren=[KR(), S((-1.7, 1.4), (1.7, 1.4), 4, True, 3)])),
         sz('Merke',
            'Zum Mitnehmen: Erst die Gerade zeichnen, waagrecht beim Sinus, senkrecht beim Cosinus. Dann die Schnittpunkte '
            'mit dem Kreis suchen und ihre Winkel bestimmen.',
            titel('Zum Mitnehmen', 260, 72),
            n('@\\fa{\\sin}@: waagrecht @y = c@|@\\fc{\\cos}@: senkrecht @x = c@|Schnittpunkte = Lösungen', 360, 'blau', 42, ein=1.0),
            graf(WK, [], ein=0.3, figuren=[KR()])),
     ], [
         wahl('Frage 1', 'Die gestrichelte Waagrechte liegt bei y = −0.4. Welche Gleichung zeigt das Bild?',
              ['sin φ = −0.4', 'cos φ = −0.4', 'tan φ = −0.4'], 0,
              {0: 'Ja.',
               1: 'Der Cosinus ist die waagrechte Koordinate. Eine Waagrechte hält aber die Höhe fest.',
               2: 'Der Tangens ist die Höhe auf der Tangente x = 1. Hier ist die Höhe der Kreispunkte festgehalten.'},
              sprich='Die gestrichelte Waagrechte liegt bei y gleich minus null Komma vier. Welche Gleichung zeigt das Bild?',
              rueck_sprich={1: 'Der Cosinus ist die waagrechte Koordinate. Eine Waagrechte hält aber die Höhe fest.',
                            2: 'Der Tangens ist die Höhe auf der Tangente x gleich eins. Hier ist die Höhe der Kreispunkte festgehalten.'}),
         klick('Frage 2', 'cos φ = 0.6: Tipp die Lösung im vierten Quadranten ins Bild.',
               [0.6, -0.8], 'Getroffen: (0.6 | −0.8).',
               [{'bei': [0.6, 0.8], 'text': 'Richtige Senkrechte, aber das ist der Punkt im ersten Quadranten. Der vierte liegt unten rechts.',
                 'sprich': 'Richtige Senkrechte, aber das ist der Punkt im ersten Quadranten. Der vierte liegt unten rechts.'},
                {'bei': [0.8, -0.6], 'text': 'Dort ist die Höhe −0.6. Der Cosinus ist die waagrechte Koordinate: x = 0.6.',
                 'sprich': 'Dort ist die Höhe minus null Komma sechs. Der Cosinus ist die waagrechte Koordinate: x gleich null Komma sechs.'},
                {'bei': [-0.6, -0.8], 'text': 'Dort ist x = −0.6. Gesucht ist x = +0.6.',
                 'sprich': 'Dort ist x gleich minus null Komma sechs. Gesucht ist x gleich plus null Komma sechs.'}],
               FALSCH, sprich='Cosinus von Phi gleich null Komma sechs: Tipp die Lösung im vierten Quadranten ins Bild.',
               falsch_sprich=FALSCH_SPR),
         wahl('Frage 3', 'Wie viele Lösungen hat cos φ = −1 im Intervall [0°; 360°[?',
              ['eine', 'zwei', 'keine'], 0,
              {0: 'Ja.',
               1: 'Zeichne die Senkrechte x = −1. Wie oft trifft sie den Kreis?',
               2: '−1 liegt noch zwischen −1 und 1. Die Senkrechte x = −1 berührt den Kreis.'},
              sprich='Wie viele Lösungen hat Cosinus von Phi gleich minus eins im Intervall von null bis dreihundertsechzig Grad?',
              rueck_sprich={1: 'Zeichne die Senkrechte x gleich minus eins. Wie oft trifft sie den Kreis?',
                            2: 'Minus eins liegt noch zwischen minus eins und eins. Die Senkrechte x gleich minus eins berührt den Kreis.'}),
         wahl('Frage 4', 'sin φ = √2/2: Welche Lösungsmenge gilt im Intervall [0°; 360°[?',
              ['𝕃 = {45°; 135°}', '𝕃 = {45°; 315°}', '𝕃 = {135°; 225°}'], 0,
              {0: 'Ja.',
               1: 'Bei 315° liegt P unter der x-Achse — dort ist der Sinus negativ. Spiegle an der y-Achse, nicht an der x-Achse.',
               2: 'Bei 225° liegt P unter der x-Achse, der Sinus ist dort negativ. Wo liegt die Waagrechte y = √2/2?'},
              sprich='Sinus von Phi gleich Wurzel zwei halbe: Welche Lösungsmenge gilt im Intervall von null bis dreihundertsechzig Grad?',
              rueck_sprich={1: 'Bei dreihundertfünfzehn Grad liegt P unter der x-Achse. Dort ist der Sinus negativ. Spiegle an der y-Achse, nicht an der x-Achse.',
                            2: 'Bei zweihundertfünfundzwanzig Grad liegt P unter der x-Achse, der Sinus ist dort negativ. Wo liegt die Waagrechte y gleich Wurzel zwei halbe?'}),
         wahl('Frage 5', 'Warum hat sin φ = 1.4 keine Lösung?',
              ['Die Waagrechte y = 1.4 trifft den Kreis nicht.', 'Die Lösung liegt ausserhalb von [0°; 360°[.',
               'Weil 1.4 keine besondere Zahl ist.'], 0,
              {0: 'Ja.',
               1: 'Auch nach weiteren Umdrehungen kommt P nicht höher. Wie hoch kommt ein Punkt des Einheitskreises?',
               2: 'Auch sin φ = 0.4 ist kein besonderer Wert und hat Lösungen. Wie hoch kommt ein Punkt des Einheitskreises?'},
              sprich='Warum hat Sinus von Phi gleich eins Komma vier keine Lösung?',
              rueck_sprich={1: 'Auch nach weiteren Umdrehungen kommt P nicht höher. Wie hoch kommt ein Punkt des Einheitskreises?',
                            2: 'Auch Sinus von Phi gleich null Komma vier ist kein besonderer Wert und hat Lösungen. Wie hoch kommt ein Punkt des Einheitskreises?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# Beispiele der Themenseite: Aufgabe A2 (sin φ = 0.4, cos φ = −0.7) und Mini-Check (sin x = −0.4).
A04 = math.degrees(math.asin(0.4))     # 23.578
C07 = math.degrees(math.acos(-0.7))    # 134.427
clip('arkus', 'Winkel finden: mit der Arkusfunktion',
     'Der Taschenrechner liefert mit der Arkusfunktion nur den Hauptwert. Die zweite Lösung kommt aus der Spiegelung '
     'am Einheitskreis, ein negativer Hauptwert bekommt 360° dazu.',
     ['Trigonometrische Gleichung', 'Arkusfunktion', 'Taschenrechner', 'Hauptwert'], [
         sz('Der Rechner',
            'Sinus von Phi gleich null Komma vier. Das ist kein besonderer Wert, hier hilft der Taschenrechner. Die '
            'Arkusfunktion, auf dem Rechner Sinus hoch minus eins, liefert ungefähr dreiundzwanzig Komma sechs Grad. '
            'Der Rechner muss dafür im Gradmass stehen.',
            f(r'\fa{\sin\varphi} = 0.4', 290, 60, ein=0.4),
            # Wortzeiten: «null Komma vier» 1.4–1.7, «liefert ungefähr» 8.6–9.3, «23,6 Grad» 9.8–11.1, «Gradmass» 12.8
            f(r'\varphi_1 = \arcsin(0.4) \approx 23.6^\circ', 400, 54, ein=9.8),
            n('Rechner im Gradmass; @\\sin^{-1}@ heisst @\\arcsin@', 510, 'rot', 40, ein=12.6),
            graf(WK, [lauf([[0, 0], [8.6, 0], [9.9, A04]])], ein=0.05,
                 figuren=[KR(), S((-1.45, 0.4), (1.45, 0.4), 5, True, 3, ein=1.6)],
                 punkte=[kp(A04, 1, '23.6°', ein=9.9)])),
         sz('Nur ein Wert',
            'Der Rechner liefert immer nur einen Winkel, den Hauptwert. Beim Arkussinus liegt er zwischen minus neunzig und '
            'neunzig Grad, auf der rechten Kreishälfte. Den zweiten Schnittpunkt musst du selbst finden.',
            # «zwischen minus 90 und 90 Grad» 4.4–6.4, «Den zweiten Schnittpunkt» 8.6
            f(r'\arcsin\colon \; -90^\circ \leq \varphi_1 \leq 90^\circ', 300, 50, ein=4.4),
            graf(WK, [], ein=0.05,
                 figuren=[dict(art='sektor', m=[0, 0], r=1, von=-90, bis=90, farbe=1, fuellung=0.12, ein=4.4),
                          KR(), S((-1.45, 0.4), (1.45, 0.4), 5, True, 3)],
                 punkte=[kp(A04, 1, '23.6°'), dict(kp(180 - A04, 5), ein=8.6)])),
         sz('Spiegeln',
            'Spiegle an der y-Achse: Phi zwei gleich hundertachtzig Grad minus dreiundzwanzig Komma sechs Grad, ungefähr '
            'hundertsechsundfünfzig Komma vier Grad. Im Intervall von null bis dreihundertsechzig Grad hat die Lösungsmenge '
            'also zwei Elemente.',
            # «Spiegle an der y-Achse» 0.4–1.5, «180 Grad minus 23,6» 3.0–5.8, «156,4 Grad» 6.9–8.6, «Lösungsmenge» 12.4
            f(r'\varphi_2 = 180^\circ - 23.6^\circ \approx 156.4^\circ', 300, 50, ein=6.9),
            f(r'\mathbb{L} = \{23.6^\circ;\ 156.4^\circ\}', 410, 54, ein=12.4),
            graf(WK, [lauf([[0, A04], [3.0, A04], [6.9, 180 - A04]])], ein=0.05,
                 figuren=[KR(), S((-1.45, 0.4), (1.45, 0.4), 5, True, 3), S((0, -1.4), (0, 1.4), 1, True, 2, ein=0.4)],
                 punkte=[kp(A04, 1, '23.6°'), dict(kp(180 - A04, 1, '156.4°'), ein=6.9)])),
         sz('Beim Cosinus',
            'Beim Cosinus liegt der Hauptwert zwischen null und hundertachtzig Grad, auf der oberen Kreishälfte. Cosinus von '
            'Phi gleich minus null Komma sieben: Der Rechner liefert ungefähr hundertvierunddreissig Komma vier Grad. Gespiegelt '
            'an der x-Achse: dreihundertsechzig minus hundertvierunddreissig Komma vier, ungefähr zweihundertfünfundzwanzig '
            'Komma sechs Grad.',
            # «zwischen null und 180 Grad» 2.1–3.8, «Cosinus von Phi gleich minus 0,7» 6.1–8.0, «134,4 Grad» 10.2–11.8,
            # «Gespiegelt an der x-Achse» 12.4–13.5, «225,6 Grad» 17.6–19.4
            f(r'\fc{\cos\varphi} = -0.7', 280, 58, ein=6.1),
            f(r'\varphi_1 = \arccos(-0.7) \approx 134.4^\circ', 380, 48, ein=10.2),
            f(r'\varphi_2 = 360^\circ - 134.4^\circ \approx 225.6^\circ', 480, 48, ein=17.6),
            graf(WK, [lauf([[0, 0], [8.8, 0], [10.2, C07], [13.8, C07], [17.6, 360 - C07]], 'cos', 3)], ein=0.05,
                 figuren=[dict(art='sektor', m=[0, 0], r=1, von=0, bis=180, farbe=3, fuellung=0.12, ein=2.1, aus=12.4),
                          KR(), S((-0.7, -1.45), (-0.7, 1.45), 5, True, 3, ein=6.1), S((-1.4, 0), (1.4, 0), 3, True, 2, ein=12.4)],
                 punkte=[dict(kp(C07, 3, '134.4°'), ein=10.2), dict(kp(360 - C07, 3, '225.6°'), ein=17.6)])),
         sz('Negativer Hauptwert',
            'Sinus von Phi gleich minus null Komma vier. Jetzt liefert der Rechner minus dreiundzwanzig Komma sechs Grad, einen '
            'Winkel unter null. Eine volle Drehung weiter ist es derselbe Punkt: plus dreihundertsechzig gibt dreihundertsechsunddreissig '
            'Komma vier Grad. Die zweite Lösung: hundertachtzig minus minus dreiundzwanzig Komma sechs, also zweihundertdrei Komma '
            'sechs Grad.',
            # «minus 0,4» 1.6–2.2, «liefert der Rechner minus 23,6 Grad» 3.5–6.0, «Plus 360 gibt 336,4» 10.5–13.6,
            # «die zweite Lösung, 180 minus minus 23,6» 14.0–17.4, «also 203,6 Grad» 18.1–20.1
            f(r'\varphi_1 = \arcsin(-0.4) \approx -23.6^\circ', 270, 46, ein=4.7),
            f(r'-23.6^\circ + 360^\circ \approx 336.4^\circ', 370, 46, ein=11.9),
            f(r'180^\circ - (-23.6^\circ) \approx 203.6^\circ', 470, 46, ein=18.6),
            graf(WK, [lauf([[0, 0], [3.5, 0], [4.7, -A04], [10.5, -A04], [11.9, 360 - A04], [15.0, 360 - A04], [18.6, 180 + A04]])],
                 ein=0.05, figuren=[KR(), S((-1.45, -0.4), (1.45, -0.4), 5, True, 3, ein=1.6)],
                 punkte=[dict(kp(-A04, 1, '−23.6°', aussen=1.25), ein=4.7, aus=11.7),
                         dict(kp(360 - A04, 1, '336.4°', aussen=1.25), ein=11.9), dict(kp(180 + A04, 1, '203.6°'), ein=18.6)])),
         sz('Probe',
            'Prüfe am Kreis: Beide Punkte liegen unter der x-Achse, denn der Sinus ist negativ. In der Lösungsmenge stehen '
            'die Winkel aufsteigend: zweihundertdrei Komma sechs und dreihundertsechsunddreissig Komma vier Grad.',
            # «unter der x-Achse» 2.2–2.8, «aufsteigend 203,6 und 336,4» 6.8–11.0
            f(r'\mathbb{L} = \{203.6^\circ;\ 336.4^\circ\}', 300, 54, ein=7.4),
            n('Probe: unter der @x@-Achse, @\\sin\\varphi \\lt 0@', 410, 'blau', 42, ein=2.2),
            graf(WK, [], ein=0.05, figuren=[KR(), S((-1.45, -0.4), (1.45, -0.4), 5, True, 3),
                                            S(c3(180 + A04), (c3(180 + A04)[0], 0), 1, False, 4, ein=2.2),
                                            S(c3(-A04), (c3(-A04)[0], 0), 1, False, 4, ein=2.2)],
                 punkte=[kp(180 + A04, 1, '203.6°'), kp(360 - A04, 1, '336.4°', aussen=1.25)])),
         sz('Merke',
            'Zum Mitnehmen: Der Rechner liefert Phi eins. Beim Sinus ist Phi zwei gleich hundertachtzig Grad minus Phi eins, '
            'beim Cosinus dreihundertsechzig Grad minus Phi eins. Ein negativer Winkel bekommt plus dreihundertsechzig Grad.',
            titel('Zum Mitnehmen', 260, 72),
            n('Rechner: @\\varphi_1@ (Hauptwert)|@\\fa{\\sin}@: @\\varphi_2 = 180^\\circ - \\varphi_1@|'
              '@\\fc{\\cos}@: @\\varphi_2 = 360^\\circ - \\varphi_1@|negativ: @+\\,360^\\circ@', 360, 'blau', 40, ein=1.0),
            graf(WK, [], ein=0.3, figuren=[KR()])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
A06 = math.degrees(math.asin(0.6))     # 36.87
clip('kontrolle-arkus', 'Winkel finden: Kontrollfragen zur Arkusfunktion',
     'Fünf Fragen zur zweiten Lösung, zum negativen Hauptwert und zur Probe am Kreis.',
     ['Trigonometrische Gleichung', 'Arkusfunktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Beim Sinus spiegelt man an der y-Achse: hundertachtzig minus vierundsechzig Komma zwei gibt hundertfünfzehn Komma '
            'acht Grad.',
            f(r'\varphi_2 = 180^\circ - 64.2^\circ \approx 115.8^\circ', 300, 50, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()], punkte=[kp(64.158, 1, '64.2°')])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-1.45, 0.9), (1.45, 0.9), 5, True, 3)],
                 punkte=[kp(64.158, 1, '64.2°'), kp(115.842, 1, '115.8°'), kp(295.842, 4, '295.8°'), kp(244.158, 4, '244.2°')])),
         sz('Frage 2',
            'Beim Cosinus spiegelt man an der x-Achse: dreihundertsechzig minus hundertsechzehn Komma sieben gibt '
            'zweihundertdreiundvierzig Komma drei Grad.',
            f(r'\varphi_2 = 360^\circ - 116.7^\circ \approx 243.3^\circ', 300, 50, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()], punkte=[kp(116.744, 3, '116.7°')])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-0.45, -1.45), (-0.45, 1.45), 5, True, 3)],
                 punkte=[kp(116.744, 3, '116.7°'), kp(243.256, 3, '243.3°'), kp(63.256, 4, '63.3°'), kp(296.744, 4, '296.7°')])),
         sz('Frage 3',
            'Minus sechsunddreissig Komma neun Grad heisst: im Uhrzeigersinn drehen. P liegt rechts unten, bei null Komma acht, '
            'minus null Komma sechs.',
            f(r'\varphi_1 = \arcsin(-0.6) \approx -36.9^\circ', 300, 48, ein=1.0),
            frage_bild(graf(WK5, [], figuren=[KR()])),
            graf(WK5, [], ein=1.0, figuren=[KR(), WI(-A06, 0, 1, 70)],
                 punkte=[pt(0.8, -0.6, 1, '(0.8 | −0.6)', [0.62, -0.95])])),
         sz('Frage 4',
            'Minus sechsunddreissig Komma neun plus dreihundertsechzig gibt dreihundertdreiundzwanzig Komma eins. Die zweite Lösung: '
            'hundertachtzig plus sechsunddreissig Komma neun, also zweihundertsechzehn Komma neun Grad.',
            f(r'\mathbb{L} = \{216.9^\circ;\ 323.1^\circ\}', 300, 54, ein=1.0),
            n('@-36.9^\\circ@ ist derselbe Punkt wie @323.1^\\circ@,|liegt aber nicht in @[0^\\circ;\\, 360^\\circ[@', 410, 'rot', 40, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((-1.45, -0.6), (1.45, -0.6), 5, True, 3)],
                 punkte=[kp(180 + A06, 1, '216.9°'), kp(360 - A06, 1, '323.1°', aussen=1.25), kp(180 - A06, 4, '143.1°')])),
         sz('Frage 5',
            'Bei hundertvier Komma fünf Grad liegt P links der y-Achse, dort ist der Cosinus negativ. Richtig ist '
            'dreihundertsechzig minus fünfundsiebzig Komma fünf, also zweihundertvierundachtzig Komma fünf Grad.',
            f(r'\varphi_2 = 360^\circ - 75.5^\circ \approx 284.5^\circ', 300, 50, ein=1.0),
            frage_bild(graf(WK, [], figuren=[KR()])),
            graf(WK, [], ein=1.0, figuren=[KR(), S((0.25, -1.45), (0.25, 1.45), 5, True, 3)],
                 punkte=[kp(75.523, 3, '75.5°'), kp(284.477, 3, '284.5°'), kp(104.477, 4, '104.5°')])),
         sz('Merke',
            'Zum Mitnehmen: Die Probe am Kreis ist schnell. Liegt der Punkt auf der richtigen Seite der Achse, stimmt das '
            'Vorzeichen.',
            titel('Zum Mitnehmen', 260, 72),
            n('Probe: Vorzeichen von @\\fa{\\sin}@ und @\\fc{\\cos}@|im Quadranten des Punktes', 360, 'blau', 42, ein=1.0),
            graf(WK, [], ein=0.3, figuren=[KR()])),
     ], [
         wahl('Frage 1', 'Der Rechner liefert für sin φ = 0.9 den Wert φ₁ ≈ 64.2°. Welches ist die zweite Lösung in [0°; 360°[?',
              ['≈ 115.8°', '≈ 295.8°', '≈ 244.2°'], 0,
              {0: 'Ja.',
               1: 'Das wäre 360° − φ₁, die Regel beim Cosinus. Wo liegt der zweite Punkt auf der Höhe 0.9?',
               2: 'Das wäre 180° + φ₁. Dort liegt P unter der x-Achse, der Sinus ist negativ.'},
              sprich='Der Rechner liefert für Sinus von Phi gleich null Komma neun den Wert Phi eins gleich ungefähr vierundsechzig Komma zwei Grad. '
                     'Welches ist die zweite Lösung zwischen null und dreihundertsechzig Grad?',
              rueck_sprich={1: 'Das wäre dreihundertsechzig Grad minus Phi eins, die Regel beim Cosinus. Wo liegt der zweite Punkt auf der Höhe null Komma neun?',
                            2: 'Das wäre hundertachtzig Grad plus Phi eins. Dort liegt P unter der x-Achse, der Sinus ist negativ.'}),
         wahl('Frage 2', 'Für cos φ = −0.45 liefert der Rechner φ₁ ≈ 116.7°. Welches ist die zweite Lösung in [0°; 360°[?',
              ['≈ 243.3°', '≈ 63.3°', '≈ 296.7°'], 0,
              {0: 'Ja.',
               1: 'Das wäre 180° − φ₁, die Regel beim Sinus. Bei 63.3° ist der Cosinus positiv.',
               2: 'Das wäre 180° + φ₁. Dort liegt P rechts der y-Achse, der Cosinus ist positiv.'},
              sprich='Für Cosinus von Phi gleich minus null Komma vier fünf liefert der Rechner Phi eins gleich ungefähr hundertsechzehn Komma sieben Grad. '
                     'Welches ist die zweite Lösung zwischen null und dreihundertsechzig Grad?',
              rueck_sprich={1: 'Das wäre hundertachtzig Grad minus Phi eins, die Regel beim Sinus. Bei dreiundsechzig Komma drei Grad ist der Cosinus positiv.',
                            2: 'Das wäre hundertachtzig Grad plus Phi eins. Dort liegt P rechts der y-Achse, der Cosinus ist positiv.'}),
         klick('Frage 3', 'Der Rechner zeigt arcsin(−0.6) ≈ −36.9°. Tipp den Punkt P zu diesem Winkel ins Bild.',
               [0.8, -0.6], 'Getroffen: (0.8 | −0.6).',
               [{'bei': [0.8, 0.6], 'text': 'Das ist +36.9°. Ein negativer Winkel dreht im Uhrzeigersinn, nach unten.',
                 'sprich': 'Das ist plus sechsunddreissig Komma neun Grad. Ein negativer Winkel dreht im Uhrzeigersinn, nach unten.'},
                {'bei': [-0.8, -0.6], 'text': 'Auch dort ist der Sinus −0.6 — aber der Rechner liefert einen Winkel zwischen −90° und 90°, rechts der y-Achse.',
                 'sprich': 'Auch dort ist der Sinus minus null Komma sechs. Aber der Rechner liefert einen Winkel zwischen minus neunzig und neunzig Grad, rechts der y-Achse.'},
                {'bei': [0.6, -0.8], 'text': 'Dort ist die Höhe −0.8. Gesucht ist die Höhe −0.6.',
                 'sprich': 'Dort ist die Höhe minus null Komma acht. Gesucht ist die Höhe minus null Komma sechs.'}],
               FALSCH, sprich='Der Rechner zeigt Arkussinus von minus null Komma sechs gleich ungefähr minus sechsunddreissig Komma neun Grad. '
                              'Tipp den Punkt P zu diesem Winkel ins Bild.',
               falsch_sprich=FALSCH_SPR),
         wahl('Frage 4', 'Welche Lösungsmenge hat sin φ = −0.6 im Intervall [0°; 360°[?',
              ['𝕃 = {216.9°; 323.1°}', '𝕃 = {143.1°; 323.1°}', '𝕃 = {−36.9°; 216.9°}'], 0,
              {0: 'Ja.',
               1: 'Bei 143.1° liegt P über der x-Achse, der Sinus ist dort positiv. Rechne 180° − φ₁ mit φ₁ = −36.9°.',
               2: '−36.9° liegt nicht im Intervall von 0° bis 360°. Eine volle Drehung weiter ist es derselbe Punkt.'},
              sprich='Welche Lösungsmenge hat Sinus von Phi gleich minus null Komma sechs im Intervall von null bis dreihundertsechzig Grad?',
              rueck_sprich={1: 'Bei hundertdreiundvierzig Komma eins Grad liegt P über der x-Achse, der Sinus ist dort positiv. Rechne hundertachtzig Grad minus Phi eins, mit Phi eins gleich minus sechsunddreissig Komma neun Grad.',
                            2: 'Minus sechsunddreissig Komma neun Grad liegt nicht im Intervall von null bis dreihundertsechzig Grad. Eine volle Drehung weiter ist es derselbe Punkt.'}),
         wahl('Frage 5', 'Lena löst cos φ = 0.25 und schreibt 𝕃 = {75.5°; 104.5°}. Was stimmt?',
              ['104.5° ist falsch: Dort ist der Cosinus negativ.', 'Beide Winkel stimmen.', '75.5° ist falsch: Der Rechner irrt.'], 0,
              {0: 'Ja.',
               1: 'Mach die Probe: Liegt der Punkt bei 104.5° rechts oder links der y-Achse?',
               2: '75.5° ist der Hauptwert des Rechners und stimmt. Prüfe den zweiten Winkel am Kreis.'},
              sprich='Lena löst Cosinus von Phi gleich null Komma zwei fünf und schreibt: Lösungsmenge fünfundsiebzig Komma fünf Grad und hundertvier Komma fünf Grad. Was stimmt?',
              rueck_sprich={1: 'Mach die Probe: Liegt der Punkt bei hundertvier Komma fünf Grad rechts oder links der y-Achse?',
                            2: 'Fünfundsiebzig Komma fünf Grad ist der Hauptwert des Rechners und stimmt. Prüfe den zweiten Winkel am Kreis.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Beispiele der Themenseite: tan φ = 1 (45°, 225°; Tabelle), tan φ = 2.5 (Aufgabe A2), tan φ = −1 (Tabelle).
T25 = math.degrees(math.atan(2.5))     # 68.199
TANLINIE = lambda w: S((-1.6 * 1.0, -1.6 * math.tan(rad(w))), (1.6, 1.6 * math.tan(rad(w))), 2, True, 3)


def _dreh_senkrecht(t0=7.4, t1=8.8, w0=math.degrees(math.atan(2.6))):
    """Stützpunkte [t, m, 0] für die Drehung von w0 über 90° bis 180° − w0."""
    out, w = [], w0
    ws = [w0 + k * 2 for k in range(int((90 - w0) // 2) + 1)] + [89.0]
    ws = ws + [180 - x for x in reversed(ws)]
    n_ = len(ws)
    for i, w in enumerate(ws):
        t = t0 + (t1 - t0) * i / (n_ - 1)
        if w == 180 - 89.0:
            t = max(t, out[-1][0] + 0.02)
        out.append([round(t, 3), round(math.tan(rad(w)), 3), 0])
    return out[1:]


DREH_SENKRECHT = _dreh_senkrecht()


def tangente(**kw):
    return S((1, -2.75), (1, 2.75), 5, False, 3, **kw)


clip('tangens', 'Winkel finden: Tangensgleichungen',
     'tan φ = c heisst: Der Punkt S(1 | c) liegt auf der Tangente x = 1. Die Gerade durch O und S trifft den Kreis in '
     'zwei Gegenpunkten, 180° auseinander — für jedes c.',
     ['Trigonometrische Gleichung', 'Tangens', 'Einheitskreis', 'Periode'], [
         sz('Tangens am Kreis',
            'Der Tangens ist am Einheitskreis eine Höhe auf der Tangente x gleich eins. Die Gerade durch den Ursprung und P '
            'trifft die Tangente im Punkt S. Tangens von Phi gleich c heisst also: S liegt auf der Höhe c.',
            f(r'\fb{\tan\varphi} = c', 300, 62, ein=0.4),
            # «Gerade durch den Ursprung und P trifft die Tangente im Punkt S» 5.1–8.2, «auf der Höhe c» 11.3–12.1
            n('@S(1 \\mid c)@ auf der Tangente @x = 1@', 410, 'orange', 42, ein=11.3),
            graf(WT, [lauf([[0, 0], [5.0, 0], [7.4, 50]], 'tan', 2)], ein=0.05, gross='tan',
                 figuren=[KR(), tangente(), T(1.12, round(math.tan(rad(50)), 3), 'S', 2, 'start', 30, ein=7.4),
                          p_name(0, 0.05, 5.0), p_name(50, 7.4, r_=1.2)])),
         sz('Gegenpunkte',
            'Tangens von Phi gleich eins: S liegt auf der Höhe eins. Die Gerade durch O und S trifft den Kreis zweimal, '
            'bei fünfundvierzig Grad und gegenüber bei zweihundertfünfundzwanzig Grad. Die beiden Punkte liegen sich am '
            'Ursprung gegenüber, hundertachtzig Grad auseinander.',
            f(r'\fb{\tan\varphi} = 1', 300, 60, ein=0.4),
            # «S liegt auf der Höhe eins» 2.3–3.2, «Gerade durch O und S» 3.9–5.3, «45°» 7.2, «225°» 9.2, «180° auseinander» 13.7
            f(r'\varphi_1 = 45^\circ, \quad \varphi_2 = 225^\circ', 410, 54, ein=9.2),
            n('@\\varphi_2 = \\varphi_1 + 180^\\circ@', 510, 'orange', 44, ein=13.7),
            graf(WT, [], ein=0.05, gross='tan',
                 figuren=[KR(), tangente(), dict(TANLINIE(45), ein=3.9), T(1.12, 1.0, 'S', 2, 'start', 30, ein=2.3)],
                 punkte=[pt(1, 1, 2, ein=2.3), dict(kpb(45, 2, '45°', [0.56, 0.86]), ein=7.2),
                         dict(kpb(225, 2, '225°', [-1.05, -0.62]), ein=9.2)])),   # neben der Geraden, nicht auf ihr
         sz('Mit dem Rechner',
            'Tangens von Phi gleich zwei Komma fünf: Der Arkustangens liefert ungefähr achtundsechzig Komma zwei Grad. '
            'Die zweite Lösung liegt hundertachtzig Grad weiter: zweihundertachtundvierzig Komma zwei Grad.',
            # «68,2 Grad» 4.4–5.1, «248,2 Grad» 9.4–10.7
            f(r'\fb{\tan\varphi} = 2.5', 300, 56, ein=0.6),
            f(r'\varphi_1 = \arctan(2.5) \approx 68.2^\circ', 400, 48, ein=4.4),
            f(r'\varphi_2 = 68.2^\circ + 180^\circ \approx 248.2^\circ', 500, 46, ein=9.4),
            graf(WT, [], ein=0.05, gross='tan',
                 figuren=[KR(), tangente(), TANLINIE(T25), T(1.12, 2.5, 'S', 2, 'start', 30)],
                 punkte=[pt(1, 2.5, 2), dict(kp(T25, 2, '68.2°', aussen=1.32), ein=4.4),
                         dict(kp(180 + T25, 2, '248.2°', aussen=1.32), ein=9.4)])),
         sz('Negativ',
            'Tangens von Phi gleich minus eins: Der Rechner liefert minus fünfundvierzig Grad. Plus hundertachtzig gibt '
            'hundertfünfunddreissig Grad, plus dreihundertsechzig gibt dreihundertfünfzehn Grad. Beide liegen zwischen null '
            'und dreihundertsechzig Grad.',
            # «minus 45°» 3.7–4.0, «135°» 6.6, «315°» 9.8
            f(r'\varphi_1 = \arctan(-1) = -45^\circ', 280, 50, ein=3.7),
            f(r'-45^\circ + 180^\circ = 135^\circ', 380, 48, ein=6.6),
            f(r'-45^\circ + 360^\circ = 315^\circ', 470, 48, ein=9.8),
            graf(WT, [], ein=0.05, gross='tan',
                 figuren=[KR(), tangente(), TANLINIE(-45), T(1.12, -1.0, 'S', 2, 'start', 30)],
                 punkte=[pt(1, -1, 2), dict(kp(135, 2, '135°', aussen=1.3), ein=6.6),
                         dict(kpb(315, 2, '315°', [0.58, -0.98]), ein=9.8)])),
         sz('Immer lösbar',
            'Anders als beim Sinus gibt es beim Tangens für jedes c Lösungen: Wie hoch S auch liegt, die Gerade durch O und S '
            'trifft den Kreis immer. Nur bei neunzig und zweihundertsiebzig Grad trifft sie die Tangente nie. Dort ist der '
            'Tangens nicht definiert.',
            # «für jedes c» 2.9–3.8, «wie hoch S auch liegt» 4.7–5.4, «trifft den Kreis immer» 7.6–8.4,
            # «90°» 9.5, «270°» 10.4, «nicht definiert» 14.3
            f(r'\fb{\tan\varphi} = c \; \text{für jedes } c', 300, 52, ein=2.9),
            n('bei @90^\\circ@ und @270^\\circ@ nicht definiert', 410, 'rot', 42, ein=14.3),
            graf(WT, halbkreise(), ein=0.05, gross='tan', figuren=[KR(), tangente()],
                 # Die Gerade dreht über die Senkrechte (Winkel 69° → 111°), nicht über die Waagrechte: Stützpunkte nach
                 # dem Winkel, bei 90° ein Sprung von +57 auf −57 in 0.02 s (Prüfung 08.10.2026, M5).
                 geraden=[{'bewegung': [[0, 1, 0], [4.6, 1, 0], [6.6, 2.6, 0], [7.4, 2.6, 0]] + DREH_SENKRECHT, 'farbe': 2,
                           'gestrichelt': True, 'dicke': 3, 'schnitte': {'kurve': k, 'farbe': 2, 'beschriftung': False, 'anzahl': 2},
                           'marken': [{'x': 1, 'text': 'S', 'farbe': 2}] if k == 0 else []} for k in (0, 1)],
                 punkte=[dict(kpb(90, 4, '90°', [0.12, 1.12], 'start'), ein=9.5), dict(kpb(270, 4, '270°', [0.12, -1.24], 'start'), ein=10.4)])),
         sz('Merke',
            'Zum Mitnehmen: Tangens von Phi gleich c hat für jedes c Lösungen. Der Rechner liefert Phi eins zwischen minus '
            'neunzig und neunzig Grad, die zweite Lösung ist Phi eins plus hundertachtzig Grad.',
            titel('Zum Mitnehmen', 260, 72),
            n('Rechner: @-90^\\circ \\lt \\varphi_1 \\lt 90^\\circ@|@\\fb{\\varphi_2 = \\varphi_1 + 180^\\circ}@|'
              'negativ: @+180^\\circ@ und @+360^\\circ@', 360, 'blau', 40, ein=1.0),
            graf(WT, [], ein=0.3, gross='tan', figuren=[KR(), tangente()])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
T06 = math.degrees(math.atan(0.6))     # 30.964
clip('kontrolle-tangens', 'Winkel finden: Kontrollfragen zum Tangens',
     'Fünf Fragen zum Punkt S auf der Tangente, zum Hauptwert des Arkustangens und zur zweiten Lösung.',
     ['Trigonometrische Gleichung', 'Tangens', 'Kontrollfragen'], [
         sz('Frage 1',
            'Beim Tangens liegt die zweite Lösung hundertachtzig Grad weiter: einunddreissig plus hundertachtzig gibt '
            'zweihundertelf Grad.',
            f(r'\varphi_2 = 31.0^\circ + 180^\circ = 211.0^\circ', 300, 48, ein=1.0),
            frage_bild(graf(WT, [], gross='tan', figuren=[KR(), tangente()], punkte=[kpb(T06, 2, '31.0°', [0.72, 0.76])])),
            graf(WT, [], ein=1.0, gross='tan', figuren=[KR(), tangente(), TANLINIE(T06)],
                 punkte=[pt(1, 0.6, 2), kpb(T06, 2, '31.0°', [0.72, 0.76]), kpb(180 + T06, 2, '211.0°', [-1.0, -0.38]),
                         kp(180 - T06, 4, '149.0°'), kp(360 - T06, 4, '329.0°')])),   # falsche Angebote rot
         sz('Frage 2',
            'Der Tangens ist die Höhe auf der Tangente x gleich eins: S liegt bei eins, zwei.',
            f(r'S(1 \mid 2)', 300, 60, ein=1.0),
            frage_bild(graf(WT, [], gross='tan', figuren=[KR(), tangente()])),
            graf(WT, [], ein=1.0, gross='tan', figuren=[KR(), tangente(), TANLINIE(math.degrees(math.atan(2)))],
                 punkte=[pt(1, 2, 2, '(1 | 2)', [1.1, 2.25], 'start')])),
         sz('Frage 3',
            'Der Arkustangens liefert einen Winkel zwischen minus neunzig und neunzig Grad. Für negatives c liegt er zwischen '
            'minus neunzig und null Grad, hier bei etwa minus achtundsiebzig Komma sieben Grad.',
            f(r'\arctan(-5) \approx -78.7^\circ', 300, 54, ein=1.0),
            frage_bild(graf(WT, [], gross='tan', figuren=[KR(), tangente()])),
            graf(WT, [], ein=1.0, gross='tan', figuren=[KR(), tangente(), TANLINIE(-78.69)],
                 punkte=[kp(-78.69, 2, '−78.7°', aussen=1.3)])),
         sz('Frage 4',
            'Auch für tausend gibt es einen Punkt S, sehr weit oben auf der Tangente. Die Gerade durch O und S ist fast '
            'senkrecht und trifft den Kreis zweimal.',
            f(r'\fb{\tan\varphi} = 1000\colon \; 2 \text{ Lösungen}', 300, 52, ein=1.0),
            frage_bild(graf(WT, [], gross='tan', figuren=[KR(), tangente()])),
            graf(WT, [], ein=1.0, gross='tan', figuren=[KR(), tangente(), S((-0.0027, -2.7), (0.0027, 2.7), 2, True, 3)],
                 punkte=[kpt(89.943, 2, '89.9°', -14), kpt(269.943, 2, '269.9°', 14)])),
         sz('Frage 5',
            'Der Rechner liefert ungefähr minus einunddreissig Grad. Plus hundertachtzig gibt hundertneunundvierzig, plus '
            'dreihundertsechzig gibt dreihundertneunundzwanzig Grad.',
            f(r'\mathbb{L} = \{149.0^\circ;\ 329.0^\circ\}', 300, 54, ein=1.0),
            n('@-31.0^\\circ@ liegt nicht in @[0^\\circ;\\, 360^\\circ[@', 410, 'rot', 40, ein=1.0),
            frage_bild(graf(WT, [], gross='tan', figuren=[KR(), tangente()])),
            graf(WT, [], ein=1.0, gross='tan', figuren=[KR(), tangente(), TANLINIE(-T06)],
                 punkte=[pt(1, -0.6, 2), kpb(180 - T06, 2, '149.0°', [-1.0, 0.25]), kpb(360 - T06, 2, '329.0°', [1.06, -0.40], 'start'),
                         kpt(T06, 4, '31.0°', 22), kp(180 + T06, 4, '211.0°')])),   # falsche Angebote rot
         sz('Merke',
            'Zum Mitnehmen: Beim Tangens zwei Gegenpunkte, hundertachtzig Grad auseinander. Nie hundertachtzig minus Phi eins '
            'wie beim Sinus.',
            titel('Zum Mitnehmen', 260, 72),
            n('@\\fb{\\varphi_2 = \\varphi_1 + 180^\\circ}@|nicht @180^\\circ - \\varphi_1@', 360, 'blau', 42, ein=1.0),
            graf(WT, [], ein=0.3, gross='tan', figuren=[KR(), tangente()])),
     ], [
         wahl('Frage 1', 'tan φ = 0.6: Der Rechner liefert φ₁ ≈ 31.0°. Welches ist die zweite Lösung in [0°; 360°[?',
              ['≈ 211.0°', '≈ 149.0°', '≈ 329.0°'], 0,
              {0: 'Ja.',
               1: 'Das wäre 180° − φ₁, die Regel beim Sinus. Die Gerade durch O und S trifft den Kreis im Gegenpunkt.',
               2: 'Das wäre 360° − φ₁, die Regel beim Cosinus. Dort ist der Tangens negativ.'},
              sprich='Tangens von Phi gleich null Komma sechs: Der Rechner liefert Phi eins gleich ungefähr einunddreissig Grad. '
                     'Welches ist die zweite Lösung zwischen null und dreihundertsechzig Grad?',
              rueck_sprich={1: 'Das wäre hundertachtzig Grad minus Phi eins, die Regel beim Sinus. Die Gerade durch O und S trifft den Kreis im Gegenpunkt.',
                            2: 'Das wäre dreihundertsechzig Grad minus Phi eins, die Regel beim Cosinus. Dort ist der Tangens negativ.'}),
         klick('Frage 2', 'tan φ = 2: Tipp den Punkt S auf der Tangente x = 1 ins Bild.',
               [1, 2], 'Getroffen: S(1 | 2).',
               [{'bei': [1, -2], 'text': 'Dort ist die Höhe −2. Gesucht ist +2.',
                 'sprich': 'Dort ist die Höhe minus zwei. Gesucht ist plus zwei.'},
                {'bei': [0.447, 0.894], 'text': 'Das ist der Punkt P auf dem Kreis. S liegt auf der Tangente x = 1.',
                 'sprich': 'Das ist der Punkt P auf dem Kreis. S liegt auf der Tangente x gleich eins.'}],
               FALSCH, sprich='Tangens von Phi gleich zwei: Tipp den Punkt S auf der Tangente x gleich eins ins Bild.',
               falsch_sprich=FALSCH_SPR, tol=0.25),
         wahl('Frage 3', 'Für tan φ = −5: Wo liegt der Wert, den der Rechner liefert?',
              ['zwischen −90° und 0°', 'zwischen 90° und 180°', 'zwischen 0° und 90°'], 0,
              {0: 'Ja.',
               1: 'Auch dort ist der Tangens negativ — aber der Rechner liefert nur Winkel zwischen −90° und 90°.',
               2: 'Dort ist der Tangens positiv. Gesucht ist ein negativer Wert.'},
              sprich='Für Tangens von Phi gleich minus fünf: Wo liegt der Wert, den der Rechner liefert?',
              rueck_sprich={1: 'Auch dort ist der Tangens negativ. Aber der Rechner liefert nur Winkel zwischen minus neunzig und neunzig Grad.',
                            2: 'Dort ist der Tangens positiv. Gesucht ist ein negativer Wert.'}),
         wahl('Frage 4', 'Wie viele Lösungen hat tan φ = 1000 im Intervall [0°; 360°[?',
              ['zwei', 'eine', 'keine'], 0,
              {0: 'Ja.',
               1: 'Die Gerade durch O und S geht durch den Ursprung. Wie oft trifft sie den Kreis?',
               2: 'Beim Sinus gibt es für grosse c keine Lösung. Gilt das auch für die Höhe auf der Tangente?'},
              sprich='Wie viele Lösungen hat Tangens von Phi gleich tausend im Intervall von null bis dreihundertsechzig Grad?',
              rueck_sprich={1: 'Die Gerade durch O und S geht durch den Ursprung. Wie oft trifft sie den Kreis?',
                            2: 'Beim Sinus gibt es für grosse c keine Lösung. Gilt das auch für die Höhe auf der Tangente?'}),
         wahl('Frage 5', 'Welche Lösungsmenge hat tan φ = −0.6 im Intervall [0°; 360°[?',
              ['𝕃 = {149.0°; 329.0°}', '𝕃 = {31.0°; 211.0°}', '𝕃 = {−31.0°; 149.0°}'], 0,
              {0: 'Ja.',
               1: 'Dort ist der Tangens positiv. Der Rechner liefert hier einen negativen Winkel.',
               2: '−31.0° liegt nicht im Intervall. Wie viel addierst du, damit es derselbe Punkt bleibt?'},
              sprich='Welche Lösungsmenge hat Tangens von Phi gleich minus null Komma sechs im Intervall von null bis dreihundertsechzig Grad?',
              rueck_sprich={1: 'Dort ist der Tangens positiv. Der Rechner liefert hier einen negativen Winkel.',
                            2: 'Minus einunddreissig Grad liegt nicht im Intervall. Wie viel addierst du, damit es derselbe Punkt bleibt?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# Beispiel der Themenseite: sin φ = 1/2 mit Lösungen 30°, 150°, 390°, 510° (Animation «Kurven», Aufgabe A5),
# allgemeine Lösung im Wortlaut des Abschnitts «Lösungsmenge angeben»; tan φ = 1 (Tabelle «Spezialfälle»).
P6 = P / 6
KRE = lambda bahn, spur=True: {'mx': -1.8, 'bahn': bahn, 'spur': spur, 'farbe': 1}


def gk(W, kurven=(), punkte=(), ein=0.05, **kw):
    return graf(W, kurven, punkte, ein=ein, gross='kurve', **kw)


def sinus(kreis=None, von=None, bis=None, farbe=1, **kw):
    d = {'bewegung': [[0, 1, 1, 0, 0]], 'trig': 'sin', 'farbe': farbe}
    if kreis:
        d['kreis'] = kreis
        d['von'] = 0
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    d.update(kw)
    return d


def waag(c, farbe=5, von=None, bis=None, **kw):
    d = dict(formel=str(c), farbe=farbe, gestrichelt=True, dicke=3)
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    d.update(kw)
    return d


def gp(w, y, farbe=1, text=None, oben=True, **kw):
    """Punkt auf der Kurve bei w Grad; Beschriftung darüber oder darunter."""
    x = rad(w)
    if text is None:
        return pt(x, y, farbe, **kw)
    return pt(x, y, farbe, text, [x, y + (0.28 if oben else -0.38)], 'middle', **kw)


clip('loesungsmenge', 'Winkel finden: alle Lösungen und die Lösungsmenge',
     'Nach 360° beginnt alles von vorn: zu jeder Lösung gehören alle, die k ganze Umdrehungen daneben liegen. '
     'Allgemeine Lösung mit k ∈ ℤ, Lösungen in einem Intervall, Tangens mit 180°, Sonderfälle.',
     ['Trigonometrische Gleichung', 'Periode', 'Lösungsmenge', 'Intervall'], [
         sz('Weiter drehen',
            'Dreht sich P über dreihundertsechzig Grad hinaus, kommt er wieder an dieselben Stellen. Bei dreihundertneunzig Grad '
            'liegt er genau dort, wo er bei dreissig Grad lag. Darum wiederholen sich auch die Lösungen: Sinus von Phi gleich '
            'ein Halb gilt auch bei dreihundertneunzig und fünfhundertzehn Grad.',
            f(r'\fa{\sin\varphi} = \tfrac{1}{2}', 250, 58, ein=0.4),
            # P läuft 0 → 390° (0.9–6.6 s), «Bei 390 Grad … wo er bei 30 Grad lag» 5.2–9.1; dann 390° → 720° (13.0–16.6),
            # «auch bei 390» 13.9, «und 510 Grad» 15.2. Die Punkte 30°/150° erscheinen, wenn P sie überfährt.
            n('@390^\\circ = 30^\\circ + 360^\\circ@', 360, 'blau', 42, ein=5.2),
            gk(WKK, [sinus(KRE([[0, 0], [0.9, 0], [6.6, 2 * P + P6], [13.0, 2 * P + P6], [16.6, 4 * P]])), waag(0.5, von=0, bis=4 * P)],
               ein=0.05,
               # P erreicht 30° bei 1.87 s und 150° bei 3.31 s (Bahn geglättet, Prüfung 08.10.2026)
               punkte=[gp(30, 0.5, 1, '30°', ein=1.9), gp(150, 0.5, 1, '150°', ein=3.35),
                       gp(390, 0.5, 1, '390°', ein=13.9), gp(510, 0.5, 1, '510°', ein=15.2)])),
         sz('Alle Lösungen',
            'Alle Lösungen schreibt man mit einer ganzen Zahl k: Phi gleich dreissig Grad plus k mal dreihundertsechzig Grad, '
            'oder Phi gleich hundertfünfzig Grad plus k mal dreihundertsechzig Grad. k darf jede ganze Zahl sein, auch null '
            'und negative.',
            # «Phi gleich 30 Grad plus k mal 360» 2.9–4.9, «oder Phi gleich 150» 5.1–8.3
            f(r'\varphi = 30^\circ + k \cdot 360^\circ', 240, 50, ein=2.9),
            f(r'\text{oder} \quad \varphi = 150^\circ + k \cdot 360^\circ, \quad k \in \mathbb{Z}', 340, 50, ein=5.1),
            gk(WKK, [sinus(von=0, bis=4 * P), waag(0.5, von=0, bis=4 * P)],
               punkte=[gp(30, 0.5), gp(150, 0.5), gp(390, 0.5), gp(510, 0.5)])),
         sz('Im Intervall',
            'Ist ein Intervall vorgegeben, setzt du für k nacheinander ganze Zahlen ein und behältst nur die Werte im Intervall. '
            'Von null bis siebenhundertzwanzig Grad sind es k gleich null und k gleich eins. Die Lösungsmenge hat vier Elemente, '
            'aufsteigend geordnet.',
            # «Von 0 bis 720 Grad» 7.0–8.4, «k gleich 0 und k gleich 1» 9.4–11.1, «Die Lösungsmenge» 11.8
            f(r'0^\circ \leq \varphi \lt 720^\circ\colon \; k = 0,\ 1', 240, 50, ein=9.4),
            f(r'\mathbb{L} = \{30^\circ;\ 150^\circ;\ 390^\circ;\ 510^\circ\}', 340, 50, ein=11.8),
            gk(WKK, [sinus(von=0, bis=4 * P), waag(0.5, von=0, bis=4 * P)],
               flaechen=[dict(punkte=[[0, -1.45], [4 * P, -1.45], [4 * P, 1.45], [0, 1.45]], farbe=1, deckung=0.08, ein=7.0)],
               punkte=[gp(30, 0.5, 1, '30°'), gp(150, 0.5, 1, '150°'), gp(390, 0.5, 1, '390°'), gp(510, 0.5, 1, '510°')])),
         sz('Negative Winkel',
            'Von minus dreihundertsechzig bis null Grad nimmt man k gleich minus eins: dreissig minus dreihundertsechzig gibt '
            'minus dreihundertdreissig Grad, hundertfünfzig minus dreihundertsechzig gibt minus zweihundertzehn Grad.',
            # «k gleich minus eins» 2.9–3.6, «minus 330 Grad» 6.4–7.4, «minus 210 Grad» 10.3–11.1
            f(r'-360^\circ \leq \varphi \lt 0^\circ\colon \; k = -1', 240, 50, ein=2.9),
            f(r'\mathbb{L} = \{-330^\circ;\ {-210^\circ}\}', 340, 50, ein=10.4),
            gk(WKN, [sinus(), waag(0.5)],
               flaechen=[dict(punkte=[[-2 * P, -1.45], [0, -1.45], [0, 1.45], [-2 * P, 1.45]], farbe=1, deckung=0.08)],
               punkte=[gp(30, 0.5, 1, '30°'), gp(150, 0.5, 1, '150°'),
                       gp(-330, 0.5, 1, '−330°', ein=6.6), gp(-210, 0.5, 1, '−210°', ein=10.4)])),
         sz('Tangens',
            'Beim Tangens ist die Periode hundertachtzig Grad. Tangens von Phi gleich eins: Phi gleich fünfundvierzig Grad plus '
            'k mal hundertachtzig Grad. Eine einzige Formel genügt, denn hundertachtzig Grad weiter liegt schon die zweite Lösung.',
            # «Periode 180 Grad» 1.8–2.8, «Phi gleich 45 Grad plus k mal 180 Grad» 5.3–7.9
            f(r'\fb{\tan\varphi} = 1\colon \; \varphi = 45^\circ + k \cdot 180^\circ', 240, 50, ein=5.3),
            gk(WKT, [dict(bewegung=[[0, 1, 1, 0, 0]], trig='tan', farbe=2, von=0, bis=4 * P, asymptoten=POLE),
                     waag(1, von=0, bis=4 * P, ein=3.5)],
               punkte=[dict(pt(rad(w), 1, 2), ein=e) for w, e in ((45, 5.6), (225, 7.3), (405, 7.3), (585, 7.3))])),
         sz('Sonderfälle',
            'Bei c gleich null, eins oder minus eins genügt beim Sinus ebenfalls eine Formel. Sinus von Phi gleich null: Phi '
            'gleich k mal hundertachtzig Grad. Sinus von Phi gleich eins: Phi gleich neunzig Grad plus k mal dreihundertsechzig Grad.',
            # «Sinus von Phi gleich 0» 5.3–6.4, «Phi gleich k mal 180 Grad» 7.1–8.4, «Sinus von Phi gleich 1» 9.1–10.1,
            # «Phi gleich 90 Grad plus k mal 360 Grad» 10.9–13.5
            f(r'\fa{\sin\varphi} = 0\colon \; \varphi = k \cdot 180^\circ', 240, 48, ein=7.1),
            f(r'\fa{\sin\varphi} = 1\colon \; \varphi = 90^\circ + k \cdot 360^\circ', 340, 48, ein=10.9),
            gk(WKK, [sinus(von=0, bis=4 * P), waag(1, von=0, bis=4 * P, ein=9.1)],
               punkte=[dict(gp(w, 0, 1), ein=7.1) for w in (0, 180, 360, 540, 720)]
               + [dict(gp(w, 1, 1), ein=10.9) for w in (90, 450)])),
         sz('Merke',
            'Zum Mitnehmen: Alle Lösungen sind die Grundlösungen plus k mal dreihundertsechzig Grad, beim Tangens plus k mal '
            'hundertachtzig Grad. Im Intervall setzt du k ein, behältst die passenden Werte und ordnest sie aufsteigend.',
            titel('Zum Mitnehmen', 240, 72),
            n('@\\fa{\\sin}@, @\\fc{\\cos}@: @+\\,k \\cdot 360^\\circ@; @\\fb{\\tan}@: @+\\,k \\cdot 180^\\circ@, @k \\in \\mathbb{Z}@|'
              'Intervall: @k@ einsetzen, aufsteigend ordnen', 340, 'blau', 40, ein=1.0),
            gk(WKK, [sinus(von=0, bis=4 * P), waag(0.5, von=0, bis=4 * P)], ein=0.3,
               punkte=[gp(30, 0.5), gp(150, 0.5), gp(390, 0.5), gp(510, 0.5)])),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
# Die Klickfrage zeichnet sin(φ) mit φ in Grad (Formel sin(x*pi/180)), damit die Eingabe Grad verlangt.
WGRAD = dict(xbereich=[-60, 780], ybereich=[-1.5, 1.5], xteilung=[[w, '%d°' % w] for w in (90, 180, 270, 360, 450, 540, 630, 720)],
             yteilung=yt(-1, 1), xname='φ', yname='y')
clip('kontrolle-loesungsmenge', 'Winkel finden: Kontrollfragen zur Lösungsmenge',
     'Fünf Fragen zur allgemeinen Lösung, zur Periode des Tangens und zur Lösungsmenge in einem Intervall.',
     ['Trigonometrische Gleichung', 'Periode', 'Lösungsmenge', 'Kontrollfragen'], [
         sz('Frage 1',
            'Cosinus von Phi gleich ein Halb hat zwei Grundlösungen, sechzig und dreihundert Grad. Beide wiederholen sich nach '
            'dreihundertsechzig Grad.',
            f(r'\varphi = 60^\circ + k \cdot 360^\circ \;\text{ oder }\; \varphi = 300^\circ + k \cdot 360^\circ', 300, 40, ein=1.0),
            frage_bild(gk(WKK, [])),
            gk(WKK, [sinus(von=0, bis=4 * P, farbe=3, bewegung=[[0, 1, 1, -H2, 0]]), waag(0.5, von=0, bis=4 * P)], ein=1.0,
               punkte=[gp(w, 0.5, 3, '%d°' % w) for w in (60, 300, 420, 660)])),
         sz('Frage 2',
            'Plus dreihundertsechzig: zweihundertzehn wird fünfhundertsiebzig, dreihundertdreissig wird sechshundertneunzig Grad.',
            f(r'\mathbb{L} = \{570^\circ;\ 690^\circ\}', 300, 54, ein=1.0),
            frage_bild(gk(WKK, [])),
            gk(WKK, [sinus(von=0, bis=4 * P), waag(-0.5, von=0, bis=4 * P)], ein=1.0,
               flaechen=[dict(punkte=[[2 * P, -1.45], [4 * P, -1.45], [4 * P, 1.45], [2 * P, 1.45]], farbe=1, deckung=0.08)],
               punkte=[gp(w, -0.5, 1, '%d°' % w, oben=False) for w in (210, 330, 570, 690)]
               + [gp(w, 0.5, 4, '%d°' % w) for w in (390, 510)])),   # falsches Angebot rot: dort ist der Sinus +0.5
         sz('Frage 3',
            'Der Tangens wiederholt sich schon nach hundertachtzig Grad: Phi gleich minus fünfundvierzig Grad plus k mal '
            'hundertachtzig Grad.',
            f(r'\varphi = -45^\circ + k \cdot 180^\circ', 300, 54, ein=1.0),
            frage_bild(gk(WKT, [])),
            gk(WKT, [dict(bewegung=[[0, 1, 1, 0, 0]], trig='tan', farbe=2, von=0, bis=4 * P, asymptoten=POLE),
                     waag(-1, von=0, bis=4 * P)], ein=1.0,
               punkte=[pt(rad(w), -1, 2) for w in (135, 315, 495, 675)])),
         sz('Frage 4',
            'Eine Periode weiter heisst plus dreihundertsechzig Grad: sechzig plus dreihundertsechzig gibt vierhundertzwanzig Grad.',
            f(r'60^\circ + 360^\circ = 420^\circ', 300, 54, ein=1.0),
            frage_bild(gk(WGRAD, [dict(formel='sin(x*pi/180)', farbe=1, dicke=5)],
                          punkte=[pt(60, 0.866, 1, '60°', [60, 1.2], 'middle')])),
            gk(WGRAD, [dict(formel='sin(x*pi/180)', farbe=1, dicke=5), waag(0.866)], ein=1.0,
               punkte=[pt(60, 0.866, 1, '60°', [60, 1.2], 'middle'), pt(120, 0.866, 1),
                       pt(420, 0.866, 1, '420°', [420, 1.2], 'middle'), pt(480, 0.866, 1)])),   # auch Lösungen: blau
         sz('Frage 5',
            'Hundertzwanzig und zweihundertvierzig Grad, dazu dieselben plus dreihundertsechzig: vierhundertachtzig und '
            'sechshundert Grad. Aufsteigend in die Lösungsmenge.',
            f(r'\mathbb{L} = \{120^\circ;\ 240^\circ;\ 480^\circ;\ 600^\circ\}', 300, 48, ein=1.0),
            frage_bild(gk(WKK, [])),
            gk(WKK, [sinus(von=0, bis=4 * P, farbe=3, bewegung=[[0, 1, 1, -H2, 0]]), waag(-0.5, von=0, bis=4 * P)], ein=1.0,
               punkte=[gp(w, -0.5, 3, '%d°' % w, oben=False) for w in (120, 240, 480, 600)])),
         sz('Merke',
            'Zum Mitnehmen: Erst die Grundlösungen, dann die Periode. Und am Schluss nur die Werte im Intervall, aufsteigend.',
            titel('Zum Mitnehmen', 240, 72),
            n('Grundlösungen @\\to@ @+\\,k \\cdot 360^\\circ@ bzw. @+\\,k \\cdot 180^\\circ@ @\\to@ Intervall', 340, 'blau', 40, ein=1.0),
            gk(WKK, [sinus(von=0, bis=4 * P)], ein=0.3)),
     ], [
         wahl('Frage 1', 'Welche Lösung beschreibt alle Lösungen von cos φ = 0.5?',
              ['φ = 60° + k · 360° oder φ = 300° + k · 360°', 'φ = 60° + k · 180°', 'φ = 60° + k · 360°'], 0,
              {0: 'Ja.',
               1: 'Dann wäre auch 240° eine Lösung. Prüfe: Ist cos 240° positiv?',
               2: 'Das ist nur die eine Hälfte. Wo liegt das Spiegelbild von 60° an der x-Achse?'},
              sprich='Welche Lösung beschreibt alle Lösungen von Cosinus von Phi gleich null Komma fünf?',
              rueck_sprich={1: 'Dann wäre auch zweihundertvierzig Grad eine Lösung. Prüfe: Ist Cosinus von zweihundertvierzig Grad positiv?',
                            2: 'Das ist nur die eine Hälfte. Wo liegt das Spiegelbild von sechzig Grad an der x-Achse?'}),
         wahl('Frage 2', 'sin φ = −0.5 hat die Lösungen 210° und 330°. Welche Lösungen liegen in [360°; 720°[?',
              ['570° und 690°', '210° und 330°', '390° und 510°'], 0,
              {0: 'Ja.',
               1: 'Die liegen unter 360°, also nicht im Intervall. Wie viel kommt für eine Umdrehung dazu?',
               2: 'Das sind 30° + 360° und 150° + 360°. Dort ist der Sinus positiv.'},
              sprich='Sinus von Phi gleich minus null Komma fünf hat die Lösungen zweihundertzehn und dreihundertdreissig Grad. '
                     'Welche Lösungen liegen zwischen dreihundertsechzig und siebenhundertzwanzig Grad?',
              rueck_sprich={1: 'Die liegen unter dreihundertsechzig Grad, also nicht im Intervall. Wie viel kommt für eine Umdrehung dazu?',
                            2: 'Das sind dreissig plus dreihundertsechzig und hundertfünfzig plus dreihundertsechzig Grad. Dort ist der Sinus positiv.'}),
         wahl('Frage 3', 'tan φ = −1: Welche Periode gehört in die allgemeine Lösung φ = −45° + k · …?',
              ['180°', '360°', '90°'], 0,
              {0: 'Ja.',
               1: 'Mit 360° fehlt jede zweite Lösung. Wie weit liegen die Gegenpunkte am Kreis auseinander?',
               2: 'Dann wäre auch 45° eine Lösung — dort ist der Tangens +1.'},
              sprich='Tangens von Phi gleich minus eins: Welche Periode gehört in die allgemeine Lösung Phi gleich minus fünfundvierzig Grad plus k mal …?',
              rueck_sprich={1: 'Mit dreihundertsechzig Grad fehlt jede zweite Lösung. Wie weit liegen die Gegenpunkte am Kreis auseinander?',
                            2: 'Dann wäre auch fünfundvierzig Grad eine Lösung. Dort ist der Tangens plus eins.'}),
         klick('Frage 4', 'sin φ = √3/2 hat die Lösung 60°. Tipp die Lösung, die eine Periode weiter rechts liegt.',
               [420, 0.866], 'Getroffen: 420°.',
               [{'bei': [120, 0.866], 'text': 'Das ist die zweite Grundlösung, 180° − 60°. Gesucht ist 60° eine Periode weiter.',
                 'sprich': 'Das ist die zweite Grundlösung, hundertachtzig minus sechzig Grad. Gesucht ist sechzig Grad eine Periode weiter.'},
                {'bei': [480, 0.866], 'text': 'Das ist 120° + 360°. Gesucht ist 60° + 360°.',
                 'sprich': 'Das ist hundertzwanzig plus dreihundertsechzig Grad. Gesucht ist sechzig plus dreihundertsechzig Grad.'},
                {'bei': [240, -0.866], 'text': '60° + 180° — dort ist der Sinus negativ. Die Periode des Sinus ist 360°.',
                 'sprich': 'Sechzig plus hundertachtzig Grad. Dort ist der Sinus negativ. Die Periode des Sinus ist dreihundertsechzig Grad.'}],
               FALSCH, sprich='Sinus von Phi gleich Wurzel drei halbe hat die Lösung sechzig Grad. Tipp die Lösung, die eine Periode weiter rechts liegt.',
               falsch_sprich=FALSCH_SPR, tol=[25, 0.3], eingabe=('φ', 'y')),
         wahl('Frage 5', 'Welche Lösungsmenge hat cos φ = −0.5 im Intervall [0°; 720°[?',
              ['𝕃 = {120°; 240°; 480°; 600°}', '𝕃 = {120°; 240°}', '𝕃 = {120°; 480°}'], 0,
              {0: 'Ja.',
               1: 'Das ist nur die erste Umdrehung. Das Intervall reicht bis 720°.',
               2: 'Der zweite Punkt jeder Umdrehung fehlt: das Spiegelbild an der x-Achse.'},
              sprich='Welche Lösungsmenge hat Cosinus von Phi gleich minus null Komma fünf im Intervall von null bis siebenhundertzwanzig Grad?',
              rueck_sprich={1: 'Das ist nur die erste Umdrehung. Das Intervall reicht bis siebenhundertzwanzig Grad.',
                            2: 'Der zweite Punkt jeder Umdrehung fehlt: das Spiegelbild an der x-Achse.'}),
     ], art='Kontrollclip')
