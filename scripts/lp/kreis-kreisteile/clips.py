"""Erzeugt die acht Drehbücher des Leitprogramms Kreis und Kreisteile (08.10.2026).

  python3 scripts/lp/kreis-kreisteile/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich); nur Szenen mit neuem Text
müssen danach vertont werden (build-clip-ton.py --szenen). Einblendungen und Bewegungen stehen als «@wort» auf dem Wort,
das sie nennen: wortzeiten.py misst die Wortzeiten der vertonten Clips mit faster-whisper (wortzeiten.json), dieses
Skript setzt daraus die Sekunden ein. Ohne Messung wird aus der Lage des Wortes im Sprechertext geschätzt.

Aufbau wie in den Leitprogrammen Planimetrie und Trigonometrische Berechnungen: Rechnung und Notizen links (x 150), die
Figur rechts (x 1010, y 175, 760 × 760), gezeichnet mit `graf` und "figuren", "achsen": false. Das Fenster ist in x und y
gleich geteilt — alle Figuren sind massstäblich.

Fragebild (HOWTO-leitprogramme §15): Die Kontrollclips zeigen beim Erscheinen einer Frage nur das Gegebene (bei Fragen
ohne Bild nichts); Rechnung und Auflösung erscheinen erst ab 1.0 s (nach der Antwort). scripts/lp/fragebild.py ist für
Funktionsgraphen gebaut; hier wird das Fragebild direkt so angelegt (wie in Planimetrie und Trigonometrische Berechnungen).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = die Figur (Kreis, Geraden)                                    \\fa{…}
  2 orange = Element: Sehne, Bogen, Lot, Dreieck M P1 P2, Hilfslinie      \\fb{…}
  3 grün   = Fläche (Sektor, Segment, Ring), Ergebnis                       \\fc{…}
  4 rot    = Fehler                                                        \\fd{…}
  5 Tinte  = neutral (Radius, Beschriftung)
Alle Zahlen in zahlen.py nachgerechnet.
"""
import difflib
import json
import math
import os
import re
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-2c-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []


def rad(w):
    return math.radians(w)


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def pol(m, r, w):
    return (m[0] + r * math.cos(rad(w)), m[1] + r * math.sin(rad(w)))


def richtung(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


# ---------------------------------------------------------------- Zeiten auf den Ton (wie Leitprogramm Modellieren)
SPRECH = {}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower())
    w_ = wort.lower()
    if not g:
        return False
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    return (len(w_) >= 5 and w_[0] == g[0] and abs(len(w_) - len(g)) <= 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.7)


def wann(clip_, szene, wort, nr=1, dazu=0.0):
    """Sekunde ab Szenenbeginn, zu der `wort` zum nr-ten Mal beginnt (Wortzeiten von faster-whisper,
    wortzeiten.py). Ohne Messung geschätzt aus der Lage des Wortes im Sprechertext."""
    w = WZ.get(clip_.replace(PRAEFIX, ''), {}).get(szene)
    text = SPRECH.get((clip_, szene), '')
    if w and w.get('sprecher') == text:
        k = 0
        for wt, a, e in w['woerter']:
            if passt(wort, wt):
                k += 1
                if k == nr:
                    return round(max(0.3, a + dazu), 2)
    FEHLT.append((clip_, szene, wort))
    if w and w.get('sprecher') == text and w['woerter']:
        # Whisper hat das Wort anders geschrieben (Zahlen als Ziffern): die Lage des Wortes im Sprechertext auf die
        # gemessenen Wörter übertragen.
        ws = text.split()
        k, idx = 0, None
        for i, t in enumerate(ws):
            if re.sub(r'[^\wäöü]', '', t.lower()).startswith(wort.lower()):
                k += 1
                if k == nr:
                    idx = i
                    break
        if idx is not None:
            j = min(len(w['woerter']) - 1, round(idx / len(ws) * len(w['woerter'])))
            return round(max(0.3, w['woerter'][j][1] + dazu), 2)
    pos, k = -1, 0
    for m in re.finditer(r'(?<!\w)' + re.escape(wort), text, re.I):
        k += 1
        if k == nr:
            pos = m.start()
            break
    d = len(text.split()) / 2.5 + 1.0
    return round(max(0.3, 0.4 + max(0, pos) / max(1, len(text)) * (d - 1.0) + dazu), 2)


def zeiten(clip_, szenen):
    """Ersetzt `ein`/`aus` und Zeiten von `bewegung`/`parameter` der Form «@wort», «@wort#2», «@wort+0.3»
    oder «@wort-0.3» durch Sekunden."""
    def los(sname, v):
        if isinstance(v, str) and v.startswith('@'):
            m = re.match(r'@([^#+\-]+)(?:#(\d+))?(?:([+\-])([\d.]+))?$', v)
            dazu = float(m.group(4) or 0) * (-1 if m.group(3) == '-' else 1)
            return wann(clip_, sname, m.group(1), int(m.group(2) or 1), dazu)
        return v
    for q in szenen:
        SPRECH[(clip_, q['name'])] = q['sprecher']
    for q in szenen:
        for el in q['elemente']:
            for z in ('ein', 'aus'):
                if z in el:
                    el[z] = los(q['name'], el[z])
            for art in ('figuren', 'punkte'):
                for k in el.get(art) or []:
                    for z in ('ein', 'aus'):
                        if z in k:
                            k[z] = los(q['name'], k[z])
                    for zf in ('bewegung', 'parameter'):
                        if zf in k:
                            k[zf] = [[los(q['name'], b[0])] + b[1:] for b in k[zf]]


# ---------------------------------------------------------------- Fenster und Figuren
def geo(x0, y0, span):
    return dict(xbereich=[x0, x0 + span], ybereich=[y0, y0 + span], achsen=False)


def V(pkte, farbe=1, fu=0.12, **kw):
    return dict(art='vieleck', punkte=[r3(p) for p in pkte], farbe=farbe, fuellung=fu, **kw)


def S(a, b, farbe=2, gest=False, dicke=4, **kw):
    d = dict(art='strecke', von=r3(a), bis=r3(b), farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=30, kursiv=True, **kw):
    return dict(art='text', bei=[round(x, 3), round(y, 3)], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=kursiv, **kw)


def RW(p, r1, r2, farbe=5, **kw):
    return dict(art='rechts', bei=r3(p), r1=round(r1, 2), r2=round(r2, 2), farbe=farbe, **kw)


def WI(p, w0, w1, farbe=2, r=44, **kw):
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def KR(m, r, farbe=1, fu=0.0, dicke=4, **kw):
    return dict(art='kreis', m=r3(m), r=round(r, 3), farbe=farbe, fuellung=fu, dicke=dicke, **kw)


def SEK(m, r, w0, w1, farbe=3, fu=0.25, dicke=3, **kw):
    return dict(art='sektor', m=r3(m), r=round(r, 3), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, fuellung=fu, dicke=dicke, **kw)


def BOG(m, r, w0, w1, farbe=2, dicke=8, **kw):
    return dict(art='bogen', m=r3(m), r=round(r, 3), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, dicke=dicke, **kw)


def PKT(p, farbe=5, r=0.12, **kw):
    """Punkt als kleiner gefüllter Kreis (in Fenstereinheiten)."""
    return dict(art='kreis', m=r3(p), r=r, farbe=farbe, fuellung=1, dicke=2, **kw)


def SEG(m, r, w0, w1, farbe=3, fu=0.45, dicke=3, n=40, **kw):
    """Segment: Vieleck aus den Bogenpunkten von w0 bis w1, durch die Sehne geschlossen."""
    return V([pol(m, r, w0 + (w1 - w0) * k / n) for k in range(n + 1)], farbe, fu, dicke=dicke, **kw)


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def graf(W, figuren=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def weich(q):
    return q * q * (3 - 2 * q)


def dicht(t0, t1, felder, schritt=0.05):
    """Stützpunkte alle 0.05 s für Bewegungen, die nicht linear in den Feldern sind (starre Drehung und
    Verschiebung eines Sektors). felder(u) mit u = 0 … 1, weich."""
    n_ = max(1, int(round((t1 - t0) / schritt)))
    return [[round(t0 + (t1 - t0) * i / n_, 3), felder(weich(i / n_))] for i in range(n_ + 1)]


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=50, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=86):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))


def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3):
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie in den Vorbildern)."""
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


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.8, bei=0.3):
    # Ohne "eingabe": Die Figuren stehen ohne Achsen (wie in der Planimetrie).
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|im Arbeitsbereich unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    dname = PRAEFIX + name
    zeiten(dname, szenen)
    alt = R + 'clips/' + dname + '.json'
    if os.path.exists(alt):
        # dauer nach Szenenname retten: build-clip-ton.py --szenen braucht die Planung der bisherigen Spur. Eine Szene mit
        # neuem Sprechertext behält ihre alte dauer, bis sie neu vertont ist (Hinweis unten).
        frueher = {q['name']: (q.get('sprecher'), q.get('dauer')) for q in json.load(open(alt))['szenen']}
        for k, q in enumerate(szenen):
            spr, d_ = frueher.get(q['name'], (None, None))
            if d_:
                q['dauer'] = d_
            if spr is not None and spr != q['sprecher']:
                print('  neu zu vertonen:', dname, 'Szene', k + 1, q['name'])
    d = {'titel': titel_, 'dateiname': dname, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Planimetrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-2c'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Kreisteile sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms kreis-kreisteile; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')


FALSCH = 'Nicht ganz. Grün siehst du die gesuchte Linie.'
M0 = (0, 0)

# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Linien am Kreis
# Kreis r = 5 um M(0 | 0) im Fenster −7.5 … 7.5. Gerade waagrecht im Abstand a: 6.5 (Passante), 5 (Tangente), 3 (Sekante).
# Sehne bei a = 3: (±4 | 3), halbe Sehne √(25 − 9) = 4, Sehne 8 cm (zahlen.py).
W1 = geo(-7.5, -7.5, 15)
KREIS1 = KR(M0, 5, 1, 0.06)
LAUF = [[0.6, {'w': 0}], [4.2, {'w': 359.5}]]       # 359.5: ein Bogen bis 360° wäre leer
clip('linien', 1, 'Kreisteile sehen: Linien am Kreis',
     'Der Kreis als Punktmenge, Radius und Durchmesser; Passante, Tangente und Sekante nach dem Abstand a der Geraden von M; '
     'Tangente senkrecht zum Radius; Sehne und Tangentenstrecke mit Pythagoras (r = 5, a = 3: Sehne 8; MP = 13: Tangente 12).',
     ['Kreis', 'Sehne', 'Sekante', 'Tangente', 'Passante', 'Abstand'], [
         sz('Der Kreis',
            'Ein Kreis ist die Menge aller Punkte, die vom Mittelpunkt M denselben Abstand r haben. Dieser Abstand heisst Radius. '
            'Der Durchmesser geht durch M und ist doppelt so lang.',
            f(r'\text{alle Punkte mit Abstand } r \text{ von } M', 300, 44, ein='@Menge'),
            f(r'd = 2r', 440, 56, ein='@doppelt'),
            # Ein Punkt läuft einmal um M und zeichnet den Kreis («Menge aller Punkte»), der Radius läuft mit.
            graf(W1, [mit(BOG(M0, 5, 0, 0, 1, 4), parameter=LAUF, bis='w', aus=4.3), mit(KR(M0, 5, 1, 0.06), ein=4.2),
                      mit(S(M0, (5, 0), 5, dicke=3), parameter=LAUF, bis=['5*cosd(w)', '5*sind(w)']),
                      mit(PKT((5, 0), 2, 0.16), parameter=LAUF, m=['5*cosd(w)', '5*sind(w)']),
                      PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False)], ein=0.3),
            graf(W1, [T(2.4, 1.2, 'r', 5)], ein='@Radius', raster=False),
            graf(W1, [S((-5, 0), (5, 0), 2, dicke=5), T(-2.5, 0.5, 'd', 2)], ein='@Durchmesser', raster=False)),
         sz('Abstand',
            'Eine Gerade kann den Kreis verfehlen, berühren oder schneiden. Entscheidend ist ihr Abstand a vom Mittelpunkt: '
            'die Länge des Lots von M auf die Gerade.',
            n('verfehlen, berühren oder schneiden?', 300, 'blau', 44, ein='@verfehlen'),
            f(r'\fb{a} = \text{Länge des Lots von } M', 430, 46, ein='@Abstand'),
            graf(W1, [KREIS1, PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False), S((-7.5, 6.5), (7.5, 6.5), 1, dicke=4)], ein=0.3),
            graf(W1, [S(M0, (0, 6.5), 2, True, 3), RW((0, 6.5), 0, 270, 2), T(-0.4, 3.3, 'a', 2, 'end')], ein='@Länge', raster=False)),
         sz('Vergleich',
            'Ist a grösser als r, ist die Gerade eine Passante, ohne gemeinsamen Punkt. Ist a gleich r, berührt sie den Kreis in '
            'genau einem Punkt: eine Tangente. Ist a kleiner als r, schneidet sie ihn zweimal: eine Sekante.',
            f(r'\fb{a} \gt r\!: \text{ Passante}', 290, 48, ein='@Passante'),
            f(r'\fb{a} = r\!: \text{ Tangente}', 400, 48, ein='@Tangente'),
            f(r'\fb{a} \lt r\!: \text{ Sekante}', 510, 48, ein='@Sekante'),
            # Die Gerade sinkt von a = 6.5 auf a = 5 («Ist a gleich r») und auf a = 3 («Ist a kleiner»).
            graf(W1, [KREIS1, PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False),
                      mit(S((-7.5, 6.5), (7.5, 6.5), 1, dicke=4), parameter=[[0.3, {'y': 6.5}], ['@gleich-0.3', {'y': 6.5}], ['@gleich+0.9', {'y': 5}],
                                                                              ['@kleiner-0.3', {'y': 5}], ['@kleiner+0.9', {'y': 3}]],
                          von=[-7.5, 'y'], bis=[7.5, 'y']),
                      mit(S(M0, (0, 6.5), 2, True, 3), parameter=[[0.3, {'y': 6.5}], ['@gleich-0.3', {'y': 6.5}], ['@gleich+0.9', {'y': 5}],
                                                                 ['@kleiner-0.3', {'y': 5}], ['@kleiner+0.9', {'y': 3}]], bis=[0, 'y']),
                      mit(T(-0.4, 3.3, 'a', 2, 'end'), parameter=[[0.3, {'y': 6.5}], ['@gleich-0.3', {'y': 6.5}], ['@gleich+0.9', {'y': 5}],
                                                                  ['@kleiner-0.3', {'y': 5}], ['@kleiner+0.9', {'y': 3}]], bei=[-0.4, 'y/2']),
                      mit(PKT((0, 5), 2, 0.2), ein='@Punkt#2', aus='@kleiner'),
                      mit(PKT((-4, 3), 2, 0.2), ein='@zweimal'), mit(PKT((4, 3), 2, 0.2), ein='@zweimal')], ein=0.3)),
         sz('Senkrecht',
            'Die Tangente steht im Berührpunkt senkrecht auf dem Radius. Denn der Berührpunkt ist ihr Punkt, der M am nächsten '
            'liegt, und der kürzeste Weg von M zu einer Geraden ist das Lot.',
            f(r'\text{Tangente} \perp \text{Radius}', 310, 54, ein='@senkrecht'),
            n('Der Berührpunkt liegt @M@ am nächsten:|Der kürzeste Weg ist das Lot.', 450, 'blau', 42, ein='@nächsten'),
            graf(W1, [KREIS1, PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False), S((-7.5, 5), (7.5, 5), 1, dicke=4), PKT((0, 5), 2, 0.2)], ein=0.3),
            graf(W1, [S(M0, (0, 5), 2, dicke=5), RW((0, 5), 0, 270, 2, px=26), T(0.4, 2.5, 'r', 2, 'start')], ein='@Radius', raster=False),
            # «am nächsten»: zwei schräge Strecken zu anderen Punkten der Tangente sind länger als r
            graf(W1, [S(M0, (3, 5), 5, True, 2), S(M0, (-4.5, 5), 5, True, 2)], ein='@nächsten', raster=False)),
         sz('Sehne',
            'Das Stück der Sekante innerhalb des Kreises heisst Sehne. Die längste Sehne geht durch M: der Durchmesser.',
            n('Sehne: Strecke zwischen zwei Kreispunkten', 300, 'blau', 42, ein='@Sehne'),
            n('längste Sehne: der Durchmesser', 420, 'blau', 42, ein='@längste'),
            graf(W1, [KREIS1, PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False), S((-7.5, 3), (7.5, 3), 1, dicke=3)], ein=0.3),
            graf(W1, [S((-4, 3), (4, 3), 2, dicke=7), PKT((-4, 3), 2, 0.2), PKT((4, 3), 2, 0.2), T(0, 3.5, 's', 2)], ein='@Sehne', raster=False),
            graf(W1, [S((-5, 0), (5, 0), 2, True, 4), T(2.5, -0.9, 'd', 2)], ein='@Durchmesser', raster=False)),
         sz('Sehne berechnen',
            'Wie lang ist die Sehne, wenn r fünf und a drei Zentimeter ist? Das Lot von M halbiert die Sehne. Es entsteht ein '
            'rechtwinkliges Dreieck mit der Hypotenuse r. Die halbe Sehne ist die Wurzel aus fünf Quadrat minus drei Quadrat, '
            'also vier. Die ganze Sehne ist acht Zentimeter lang.',
            f(r'r = 5\,\mathrm{cm}, \quad \fb{a = 3\,\mathrm{cm}}', 270, 46, ein='@wenn'),
            f(r'\left(\tfrac{s}{2}\right)^2 + a^2 = r^2', 380, 46, ein='@rechtwinkliges'),
            f(r'\tfrac{s}{2} = \sqrt{5^2 - 3^2} = \fc{4}', 490, 46, ein='@Wurzel'),
            f(r's = 2 \cdot 4 = \fc{8\,\mathrm{cm}}', 600, 46, ein='@ganze'),
            graf(W1, [KREIS1, PKT(M0), T(-0.5, -0.8, 'M', 5, 'end', 30, False), S((-4, 3), (4, 3), 2, dicke=6),
                      PKT((-4, 3), 2, 0.2), PKT((4, 3), 2, 0.2), S(M0, (0, 3), 2, True, 3), T(-0.4, 1.5, 'a = 3', 2, 'end', 28, False)], ein=0.3),
            graf(W1, [RW((0, 3), 0, 270, 5), V([M0, (0, 3), (4, 3)], 1, 0.15, dicke=2), S(M0, (4, 3), 5, dicke=3),
                      T(2.5, 1.1, 'r = 5', 5, 'start', 28, False)], ein='@halbiert', raster=False),
            graf(W1, [T(2, 3.45, '4', 3, 'middle', 32, False)], ein='@also', raster=False),
            graf(W1, [T(0, 3.95, 's = 8 cm', 3, 'middle', 30, False)], ein='@ganze', raster=False)),
         sz('Tangente von aussen',
            'Von einem Punkt P ausserhalb führen zwei Tangenten zum Kreis. Wir nehmen die obere. Mit dem Radius zum Berührpunkt B '
            'entsteht ein rechter Winkel bei B. Darum ist M P die Hypotenuse. Bei r gleich fünf und M P gleich dreizehn Zentimeter ist die '
            'Tangentenstrecke die Wurzel aus dreizehn Quadrat minus fünf Quadrat, also zwölf Zentimeter.',
            f(r'\overline{PB}^2 + r^2 = \overline{MP}^2', 300, 46, ein='@Hypotenuse'),
            f(r'\overline{PB} = \sqrt{13^2 - 5^2} = \fc{12\,\mathrm{cm}}', 420, 44, ein='@also'),
            # M(0 | 0), r = 5, P(13 | 0); cos θ = 5/13 → B(1.923 | 4.615)
            graf(geo(-6, -8, 20), [KR(M0, 5, 1, 0.06), PKT(M0), T(-0.5, -1.0, 'M', 5, 'end', 30, False),
                                   PKT((13, 0)), T(13, -1.1, 'P', 5, 'middle', 30, False),
                                   S((13, 0), pol((13, 0), 14, 180 - 22.62 + 0.0), 1, dicke=3),
                                   PKT(pol(M0, 5, 67.38), 2, 0.2), T(1.5, 5.6, 'B', 2, 'middle', 30, False)], ein=0.3),
            # die zweite Tangente (unten, Berührpunkt bei −67.38°), symmetrisch zur Geraden MP — erscheint mit «Tangenten»
            graf(geo(-6, -8, 20), [S((13, 0), pol((13, 0), 14, 180 + 22.62), 1, True, 2), PKT(pol(M0, 5, -67.38), 1, 0.14)],
                 ein='@Tangenten', raster=False),
            graf(geo(-6, -8, 20), [S(M0, pol(M0, 5, 67.38), 2, dicke=4), RW(pol(M0, 5, 67.38), 247.38, 337.38, 2, px=24),
                                   T(0.3, 2.8, 'r = 5', 2, 'end', 28, False)], ein='@Radius', raster=False),
            graf(geo(-6, -8, 20), [S(M0, (13, 0), 5, True, 3), T(6.5, -1.1, 'MP = 13', 5, 'middle', 28, False)], ein='@Hypotenuse', raster=False),
            graf(geo(-6, -8, 20), [S(pol(M0, 5, 67.38), (13, 0), 3, dicke=6), T(8.2, 3.2, '12', 3, 'middle', 32, False)], ein='@also', raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Der Abstand a entscheidet, ob eine Gerade Passante, Tangente oder Sekante ist. Die Tangente steht '
            'senkrecht auf dem Radius. Und mit dem Lot oder dem Berührradius entstehen rechtwinklige Dreiecke für Pythagoras.',
            titel('Zum Mitnehmen', 250, 76),
            n('@a \\gt r@ Passante, @a = r@ Tangente, @a \\lt r@ Sekante|Tangente @\\perp@ Radius|Lot halbiert die Sehne: Pythagoras', 380, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
# Frage 1: Kreis r = 5. Passante y = −6, Tangente x = 5, Radius zu 225°, Sehne von 60° nach 160°:
# A(2.5 | 4.330), B(−4.698 | 1.710). Keine Sekante: Ihr Stück im Kreis wäre selbst eine Sehne (Prüfung 08.10.2026).
# Abstände der Sehne: zur Passante ≥ 7.71, zur Tangente ≥ 2.5, zum Radius ≥ 3.2 — Toleranz 1.0 für Ziel und Fallen,
# keine Überschneidung zwischen Sehne und den anderen Linien.
SA, SB = pol(M0, 5, 60), pol(M0, 5, 160)
RAD225 = pol(M0, 5, 225)
clip('kontrolle-linien', 2, 'Kreisteile sehen: Kontrollfragen zu den Linien am Kreis',
     'Fünf Fragen: die Sehne antippen, die Lage einer Geraden aus Abstand und Radius (auch mit dem Durchmesser gegeben), '
     'eine Sehne und eine Tangentenstrecke mit Pythagoras.',
     ['Sehne', 'Tangente', 'Passante', 'Abstand', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Sehne verbindet zwei Punkte der Kreislinie und endet dort.',
            n('Sehne: endet an der Kreislinie', 300, 'blau', 46, ein=1.0),
            graf(W1, [KREIS1, PKT(M0), T(0.5, 0.3, 'M', 5, 'start', 30, False), S((-7.5, -6), (7.5, -6), 1, dicke=3),
                      S((5, -7.5), (5, 7.5), 1, dicke=3), S(M0, RAD225, 5, dicke=3), S(SA, SB, 1, dicke=3), PKT(SA, 1), PKT(SB, 1)], ein=0.05),
            graf(W1, [S(SA, SB, 3, dicke=8)], ein=1.0, raster=False)),
         sz('Frage 2',
            'Der Abstand ist gleich dem Radius. Die Gerade berührt den Kreis in einem Punkt: eine Tangente.',
            f(r'a = r = 4\,\mathrm{cm} \;\Rightarrow\; \fc{\text{Tangente}}', 300, 46, ein=1.0),
            graf(geo(-6, -6, 12), [KR(M0, 4, 1, 0.06), PKT(M0), S((-6, 4), (6, 4), 1, dicke=4), S(M0, (0, 4), 2, True, 3), PKT((0, 4), 3, 0.18),
                                   T(-0.4, 2, 'a = 4', 2, 'end', 28, False)], ein=1.0)),
         sz('Frage 3',
            'Der Radius ist die Hälfte des Durchmessers, fünf Zentimeter. Der Abstand sechs ist grösser: eine Passante.',
            f(r'r = \tfrac{10}{2} = 5\,\mathrm{cm} \lt 6\,\mathrm{cm} = a', 300, 46, ein=1.0),
            f(r'\Rightarrow\; \fc{\text{Passante}}', 410, 46, ein=1.0),
            graf(geo(-7.5, -7.5, 15), [KR(M0, 5, 1, 0.06), PKT(M0), S((-7.5, 6), (7.5, 6), 1, dicke=4), S(M0, (0, 6), 2, True, 3),
                                       T(-0.4, 3, 'a = 6', 2, 'end', 28, False), S(M0, pol(M0, 5, 215), 5, dicke=3), T(-2.6, -0.9, 'r = 5', 5, 'end', 28, False)], ein=1.0)),
         sz('Frage 4',
            'Die halbe Sehne ist die Wurzel aus hundert minus sechsunddreissig, also acht. Die Sehne ist sechzehn Zentimeter lang.',
            f(r'\tfrac{s}{2} = \sqrt{10^2 - 6^2} = 8', 300, 48, ein=1.0),
            f(r's = \fc{16\,\mathrm{cm}}', 410, 48, ein=1.0),
            graf(geo(-12, -12, 24), [KR(M0, 10, 1, 0.06), PKT(M0, 5, 0.2), S((-8, 6), (8, 6), 2, dicke=6), S(M0, (0, 6), 2, True, 3),
                                     S(M0, (8, 6), 5, dicke=3), RW((0, 6), 0, 270, 5), T(-0.6, 3, 'a = 6', 2, 'end', 28, False),
                                     T(4.6, 2.4, 'r = 10', 5, 'start', 28, False), T(4, 6.8, '8', 3, 'middle', 30, False)], ein=1.0)),
         sz('Frage 5',
            'Der rechte Winkel liegt bei B, M P ist die Hypotenuse. Die Wurzel aus siebzehn Quadrat minus acht Quadrat ist fünfzehn.',
            f(r'\overline{PB} = \sqrt{17^2 - 8^2} = \fc{15\,\mathrm{cm}}', 300, 46, ein=1.0),
            # M(0 | 0), r = 8, P(17 | 0), cos θ = 8/17 → θ = 61.93°, B(3.765 | 7.059)
            graf(geo(-9.5, -11, 28), [KR(M0, 8, 1, 0.06), PKT(M0, 5, 0.22), PKT((17, 0), 5, 0.22), T(17, -1.6, 'P', 5, 'middle', 32, False),
                                      S(M0, (17, 0), 5, True, 3), S(M0, pol(M0, 8, 61.93), 2, dicke=4), S(pol(M0, 8, 61.93), (17, 0), 3, dicke=6),
                                      RW(pol(M0, 8, 61.93), 241.93, 331.93, 2, px=24), T(3.7, 8.2, 'B', 2, 'middle', 32, False),
                                      T(8.5, -1.6, 'MP = 17', 5, 'middle', 28, False), T(1.3, 4.5, 'r = 8', 2, 'end', 28, False),
                                      T(11.2, 4.9, '15', 3, 'middle', 32, False)], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: a mit r vergleichen, nicht mit d. Das Lot halbiert die Sehne, und die Tangente steht senkrecht auf dem '
            'Radius.',
            titel('Zum Mitnehmen', 250, 76),
            n('@a@ mit @r@ vergleichen|Lot halbiert die Sehne|Tangente @\\perp@ Radius', 400, 'blau', 44, ein=1.2)),
     ], [
         klick('Frage 1', 'Tipp die Sehne an.', [r3(SA), r3(SB)], 'Getroffen: Sie verbindet zwei Punkte der Kreislinie.',
               [{'bei': [[-7.5, -6], [7.5, -6]], 'text': 'Das ist eine Passante: eine Gerade ohne gemeinsamen Punkt mit dem Kreis.',
                 'sprich': 'Das ist eine Passante: eine Gerade ohne gemeinsamen Punkt mit dem Kreis.'},
                {'bei': [[5, -7.5], [5, 7.5]], 'text': 'Das ist eine Tangente: Sie berührt den Kreis nur in einem Punkt.',
                 'sprich': 'Das ist eine Tangente: Sie berührt den Kreis nur in einem Punkt.'},
                {'bei': [[0, 0], r3(RAD225)], 'text': 'Das ist ein Radius: Er beginnt im Mittelpunkt.',
                 'sprich': 'Das ist ein Radius: Er beginnt im Mittelpunkt.'}],
               FALSCH, sprich='Tipp die Sehne an.', falsch_sprich=FALSCH, tol=1.0),
         wahl('Frage 2', 'Kreis mit r = 4 cm, Gerade im Abstand a = 4 cm von M. Was für eine Gerade ist das?', ['Tangente', 'Passante', 'Sekante'], 0,
              {0: 'Ja.', 1: 'Eine Passante braucht einen Abstand grösser als r. Ist das hier so?', 2: 'Eine Sekante braucht einen Abstand kleiner als r. Ist das hier so?'},
              sprich='Kreis mit r gleich vier Zentimeter, Gerade im Abstand a gleich vier Zentimeter von M. Was für eine Gerade ist das?',
              rueck_sprich={1: 'Eine Passante braucht einen Abstand grösser als r. Ist das hier so?', 2: 'Eine Sekante braucht einen Abstand kleiner als r. Ist das hier so?'}),
         wahl('Frage 3', 'Durchmesser 10 cm, Abstand der Geraden von M: 6 cm. Was für eine Gerade ist das?', ['Passante', 'Sekante', 'Tangente'], 0,
              {0: 'Ja.', 1: 'Womit hast du a verglichen — mit d oder mit r?', 2: 'Bei einer Tangente ist a gleich r. Wie gross ist r?'},
              sprich='Durchmesser zehn Zentimeter, Abstand der Geraden von M: sechs Zentimeter. Was für eine Gerade ist das?',
              rueck_sprich={1: 'Womit hast du a verglichen, mit d oder mit r?', 2: 'Bei einer Tangente ist a gleich r. Wie gross ist r?'}),
         wahl('Frage 4', 'r = 10 cm, eine Sehne hat von M den Abstand 6 cm. Wie lang ist sie?', ['16 cm', '8 cm', '≈ 23.32 cm'], 0,
              {0: 'Ja.', 1: 'Das Lot halbiert die Sehne. Welches Stück hast du berechnet?', 2: 'Welche Seite des Dreiecks ist die Hypotenuse?'},
              sprich='r gleich zehn Zentimeter, eine Sehne hat von M den Abstand sechs Zentimeter. Wie lang ist sie?',
              rueck_sprich={1: 'Das Lot halbiert die Sehne. Welches Stück hast du berechnet?', 2: 'Welche Seite des Dreiecks ist die Hypotenuse?'}),
         wahl('Frage 5', 'P liegt 17 cm von M entfernt, r = 8 cm. Wie lang ist die Tangentenstrecke PB?', ['15 cm', '≈ 18.79 cm', '9 cm'], 0,
              {0: 'Ja.', 1: 'Wo liegt der rechte Winkel? Welche Strecke ist die Hypotenuse?', 2: 'Das ist der Abstand von P zur Kreislinie, nicht die Strecke bis zum Berührpunkt.'},
              sprich='P liegt siebzehn Zentimeter von M entfernt, r gleich acht Zentimeter. Wie lang ist die Tangentenstrecke P B?',
              rueck_sprich={1: 'Wo liegt der rechte Winkel? Welche Strecke ist die Hypotenuse?', 2: 'Das ist der Abstand von P zur Kreislinie, nicht die Strecke bis zum Berührpunkt.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Umfang, Fläche und π
# Abrollen: Kreis d = 2 (r = 1) um (x | 1), rollt von x = 0 bis x = 2π = 6.283; Randpunkt auf der Zykloide.
W2a = geo(-1.2, -3.5, 9.6)
ROLL = [[0.6, {'s': 0}], ['@Durchmesser-0.6', {'s': 2 * math.pi}]]   # «x» ist im Bauer vergeben
# Sektoren zum Streifen: r = 3, n = 8, Kreis um C(0 | 3.9), Streifen auf y = −3.4 (wie seite.js, Fenster −6.5 … 6.5, −5 … 8)
W2 = geo(-6.5, -5, 13)
C2, YB2, R2, N2 = (0, 3.9), -3.4, 3, 8


def sektor_lage(k, r, n, u, C, yb, eben=12):
    """Punkte von Sektor k (Kreis um C) bei Fortschritt u: starr gedreht und verschoben vom Kreis in den Streifen."""
    w0 = 360 * k / n                                   # Lage im Kreis: Spitze in C, Mitte bei w0 + 180/n
    c, h = r * math.sin(math.pi / n), r * math.cos(math.pi / n)
    xs = -(n - 1) * c / 2
    j, oben = k // 2, k % 2 == 1
    ziel_sp = (xs + (2 * j + 1) * c, yb + h) if oben else (xs + 2 * j * c, yb)
    ziel_mw = -90 if oben else 90
    sp = (C[0] + (ziel_sp[0] - C[0]) * u, C[1] + (ziel_sp[1] - C[1]) * u)
    mw0 = w0 + 180 / n
    d = (ziel_mw - mw0 + 180) % 360 - 180               # kürzeste Drehung
    mw = mw0 + d * u
    return [r3(sp)] + [r3(pol(sp, r, mw - 180 / n + 360 / n * q / eben)) for q in range(eben + 1)]


def sektoren(r, n, C, yb, start=None, dauer=2.4, fertig=False):
    """n Sektoren im Kreis (oder fertig im Streifen); mit start («@wort») wandern sie in `dauer` Sekunden starr in den
    Streifen — Stützpunkte alle 0.05 s als «@wort+t», damit die Bewegung auf dem Wort beginnt."""
    aus = []
    for k in range(n):
        fg = V(sektor_lage(k, r, n, 1 if fertig else 0, C, yb), 1, 0.35 if k % 2 else 0.12, dicke=3)
        if start is not None:
            fg['bewegung'] = [[start + '+%.2f' % t, z] for t, z in dicht(0, dauer, lambda u, k=k: {'punkte': sektor_lage(k, r, n, u, C, yb)})]
        aus.append(fg)
    return aus


c8 = R2 * math.sin(math.pi / N2)
XS8 = -(N2 - 1) * c8 / 2
c24 = R2 * math.sin(math.pi / 24)
XS24 = -(24 - 1) * c24 / 2
clip('umfang', 3, 'Kreisteile sehen: Umfang, Fläche und π',
     'Abrollen: Der Umfang ist gut drei Durchmesser, π = U : d; U = 2πr = πd. Sektoren zum Streifen umgelegt: Höhe r, Breite πr, '
     'also A = πr². Vorgelöst mit r = 3 cm; rückwärts aus U = 40 cm und A = 50 cm².',
     ['Kreiszahl', 'Pi', 'Umfang', 'Kreisfläche', 'Radius'], [
         sz('Abrollen',
            'Rollt ein Kreis genau einmal ab, legt er seinen Umfang zurück. Mit dem Durchmesser als Massstab: Er passt etwas '
            'mehr als dreimal hinein.',
            f(r'\text{eine Umdrehung} = U', 300, 48, ein='@Umfang'),
            n('@d@ passt gut dreimal in @U@', 420, 'blau', 44, ein='@passt'),
            # Der Kreis rollt (Mitte (x | 1)), der Randpunkt läuft auf der Zykloide, die Strecke wächst mit.
            graf(W2a, [S((-1.2, 0), (8.4, 0), 5, dicke=2),
                       mit(KR((0, 1), 1, 1, 0.08), parameter=ROLL, m=['s', 1]),
                       mit(S((0, 0), (0, 0), 2, dicke=6), parameter=ROLL, bis=['s', 0]),
                       mit(PKT((0, 0), 2, 0.12), parameter=ROLL, m=['s - sin(s)', '1 - cos(s)']),
                       mit(S((0, 1), (0, 0), 5, dicke=2), parameter=ROLL, von=['s', 1], bis=['s - sin(s)', '1 - cos(s)'])], ein=0.3),
            graf(W2a, [S((0, -0.5), (2, -0.5), 1, dicke=5), S((2, -0.9), (4, -0.9), 1, dicke=5), S((4, -0.5), (6, -0.5), 1, dicke=5),
                       S((6, -0.9), (2 * math.pi, -0.9), 3, dicke=5), T(1, -1.4, 'd', 1), T(3, -1.8, 'd', 1), T(5, -1.4, 'd', 1)],
                 ein='@Massstab', raster=False)),
         sz('Pi',
            'Dieses Verhältnis Umfang durch Durchmesser ist bei jedem Kreis gleich. Es ist die Kreiszahl Pi, rund drei Komma eins '
            'vier eins sechs. Darum ist der Umfang Pi mal d, oder zwei Pi mal r.',
            f(r'\pi = \dfrac{U}{d} \approx 3.1416', 300, 54, ein='@Kreiszahl'),
            f(r'U = \pi d = 2\pi r', 440, 56, ein='@Darum'),
            graf(W2a, [S((-1.2, 0), (8.4, 0), 5, dicke=2), KR((2 * math.pi, 1), 1, 1, 0.08), S((0, 0), (2 * math.pi, 0), 2, dicke=6),
                       S((0, -0.5), (2, -0.5), 1, dicke=5), S((2, -0.9), (4, -0.9), 1, dicke=5), S((4, -0.5), (6, -0.5), 1, dicke=5),
                       S((6, -0.9), (2 * math.pi, -0.9), 3, dicke=5), T(3.14, 0.4, 'U', 2), T(1, -1.4, 'd', 1), T(3, -1.8, 'd', 1), T(5, -1.4, 'd', 1)],
                 ein=0.3)),
         sz('Sektoren',
            'Für die Fläche zerschneidet man den Kreis in gleiche Sektoren und legt sie abwechselnd nebeneinander. Es entsteht '
            'fast ein Rechteck: so hoch wie der Radius und so breit wie der halbe Umfang, Pi mal r.',
            n('Sektoren abwechselnd nebeneinander', 300, 'blau', 42, ein='@abwechselnd'),
            f(r'\text{Höhe } \fb{r}, \quad \text{Breite } \fc{\pi r}', 430, 48, ein='@hoch'),
            graf(W2, sektoren(R2, N2, C2, YB2, '@abwechselnd', 2.6), ein=0.3),
            graf(W2, [S((XS8 - c8 - 0.4, YB2), (XS8 - c8 - 0.4, YB2 + R2), 2, dicke=5), T(XS8 - c8 - 0.6, YB2 + 1.5, 'r', 2, 'end')], ein='@Radius', raster=False),
            graf(W2, [S((XS8, YB2 - 0.6), (XS8 + N2 * c8, YB2 - 0.6), 3, dicke=5), T(0, YB2 - 1.4, 'π · r', 3, 'middle', 32, False)], ein='@halbe', raster=False)),
         sz('Fläche',
            'Beim Umlegen bleibt die Fläche gleich. Mit mehr Sektoren wird der Streifen ein Rechteck, und seine Fläche ist Pi r mal '
            'r, also Pi r Quadrat.',
            f(r'A = \pi r \cdot r = \fc{\pi r^2}', 330, 56, ein='@also'),
            graf(W2, sektoren(R2, N2, C2, YB2, fertig=True), ein=0.3, aus='@mehr+0.6'),
            graf(W2, sektoren(R2, 24, C2, YB2, fertig=True) + [S((XS24 - c24 - 0.4, YB2), (XS24 - c24 - 0.4, YB2 + R2), 2, dicke=5),
                                                                T(XS24 - c24 - 0.6, YB2 + 1.5, 'r', 2, 'end'),
                                                                S((XS24, YB2 - 0.5), (XS24 + 24 * c24, YB2 - 0.5), 3, dicke=5),
                                                                T(0, YB2 - 1.3, 'π · r', 3, 'middle', 32, False)], ein='@mehr+0.6')),
         sz('Vorgelöst',
            'Zum Beispiel r gleich drei Zentimeter. Der Umfang ist zwei Pi mal drei, also sechs Pi, rund achtzehn Komma acht fünf '
            'Zentimeter. Die Fläche ist Pi mal drei Quadrat, also neun Pi, rund achtundzwanzig Komma zwei sieben Quadratzentimeter.',
            f(r'r = 3\,\mathrm{cm}', 270, 50, ein='@Beispiel'),
            f(r'U = 2\pi \cdot 3 = 6\pi \approx \fc{18.85\,\mathrm{cm}}', 390, 46, ein='@also'),
            f(r'A = \pi \cdot 3^2 = 9\pi \approx \fc{28.27\,\mathrm{cm}^2}', 510, 46, ein='@also#2'),
            graf(geo(-5, -5, 10), [KR(M0, 3, 1, 0.1), PKT(M0), S(M0, pol(M0, 3, 30), 2, dicke=4), T(1.2, 1.25, 'r = 3', 2, 'end', 30, False)], ein=0.3)),
         sz('Rückwärts',
            'Umgekehrt: Ist der Umfang vierzig Zentimeter, teilt man durch zwei Pi. Der Radius ist rund sechs Komma drei sieben '
            'Zentimeter. Ist die Fläche fünfzig Quadratzentimeter, teilt man durch Pi und zieht die Wurzel: rund drei Komma neun '
            'neun Zentimeter.',
            f(r'U = 40\,\mathrm{cm}\!: \; r = \dfrac{40}{2\pi} \approx \fc{6.37\,\mathrm{cm}}', 320, 46, ein='@Radius'),
            f(r'A = 50\,\mathrm{cm}^2\!: \; r = \sqrt{\dfrac{50}{\pi}} \approx \fc{3.99\,\mathrm{cm}}', 470, 46, ein='@Wurzel')),
         sz('Merke',
            'Zum Mitnehmen: Pi ist Umfang durch Durchmesser. Der Umfang hat r, die Fläche r Quadrat. Doppelter Radius heisst '
            'doppelter Umfang, aber vierfache Fläche.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'U = 2\pi r \qquad A = \pi r^2', 390, 54, ein=1.2),
            n('doppelter Radius: doppelter Umfang, vierfache Fläche', 520, 'blau', 42, ein='@Doppelter')),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-umfang', 4, 'Kreisteile sehen: Kontrollfragen zu Umfang und Fläche',
     'Fünf Fragen: was π ist, Umfang aus dem Durchmesser, Fläche aus dem Radius, doppelter Radius und der Radius aus dem Umfang.',
     ['Pi', 'Umfang', 'Kreisfläche', 'Kontrollfragen'], [
         sz('Frage 1',
            'Pi ist Umfang durch Durchmesser, für jeden Kreis dieselbe Zahl.',
            f(r'\pi = \dfrac{U}{d}', 300, 60, ein=1.0)),
         sz('Frage 2',
            'Der Umfang ist Pi mal d: Pi mal acht, rund fünfundzwanzig Komma eins drei Zentimeter.',
            f(r'U = \pi \cdot 8 \approx \fc{25.13\,\mathrm{cm}}', 300, 52, ein=1.0),
            graf(geo(-6, -6, 12), [KR(M0, 4, 1, 0.06), BOG(M0, 4, 0, 359.5, 3, 7), S((-4, 0), (4, 0), 2, dicke=4), PKT(M0),
                                   T(0, 0.5, 'd = 8', 2, 'middle', 30, False), T(3.3, 3.6, 'U', 3, 'start')], ein=1.0)),
         sz('Frage 3',
            'Die Fläche ist Pi mal r Quadrat: Pi mal sechsunddreissig, rund hundertdreizehn Komma eins null Quadratzentimeter.',
            f(r'A = \pi \cdot 6^2 = 36\pi \approx \fc{113.10\,\mathrm{cm}^2}', 300, 48, ein=1.0),
            graf(geo(-8, -8, 16), [KR(M0, 6, 3, 0.3, 3), PKT(M0), S(M0, pol(M0, 6, 30), 2, dicke=4), T(2.2, 0.6, 'r = 6', 2, 'start', 30, False)], ein=1.0)),
         sz('Frage 4',
            'In der Fläche steht r im Quadrat. Doppelter Radius gibt zwei Quadrat, also viermal so viel Fläche.',
            f(r'\pi (2r)^2 = 4 \cdot \pi r^2', 300, 56, ein=1.0),
            # kleiner Kreis r = 2 und grosser r = 4: vier kleine Kreisflächen passen der Fläche nach hinein
            graf(geo(-7, -7.25, 14.5), [KR((-4.5, 0), 2, 3, 0.3, 3), PKT((-4.5, 0)), S((-4.5, 0), (-2.5, 0), 2, dicke=4), T(-3.5, 0.4, 'r', 2),
                                        KR((2.5, 0), 4, 3, 0.3, 3), PKT((2.5, 0)), S((2.5, 0), (6.5, 0), 2, dicke=4), T(4.5, 0.4, '2r', 2)], ein=1.0)),
         sz('Frage 5',
            'Aus U gleich zwei Pi r folgt r gleich fünfzig durch zwei Pi, rund sieben Komma neun sechs Zentimeter.',
            f(r'r = \dfrac{50}{2\pi} \approx \fc{7.96\,\mathrm{cm}}', 300, 54, ein=1.0),
            graf(geo(-10, -10, 20), [KR(M0, 7.96, 1, 0.06), BOG(M0, 7.96, 0, 359.5, 2, 7), PKT(M0), S(M0, pol(M0, 7.96, 30), 3, dicke=4),
                                     T(3.4, 1.4, 'r ≈ 7.96', 3, 'start', 30, False), T(6.2, 6.4, 'U = 50', 2, 'start', 30, False)], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Umfang zwei Pi r, Fläche Pi r Quadrat. Rückwärts teilen, bei der Fläche zusätzlich die Wurzel.',
            titel('Zum Mitnehmen', 250, 76),
            n('@U = 2\\pi r@, @A = \\pi r^2@|rückwärts: teilen, bei @A@ die Wurzel', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'π ist das Verhältnis …', ['Umfang : Durchmesser', 'Umfang : Radius', 'Fläche : Radius'], 0,
              {0: 'Ja.', 1: 'Beim Abrollen war der Massstab nicht der Radius. Welche Strecke war es?', 2: 'π vergleicht zwei Längen.'},
              sprich='Pi ist das Verhältnis von …',
              rueck_sprich={1: 'Beim Abrollen war der Massstab nicht der Radius. Welche Strecke war es?', 2: 'Pi vergleicht zwei Längen.'}),
         wahl('Frage 2', 'd = 8 cm: Wie lang ist der Umfang?', ['≈ 25.13 cm', '≈ 50.27 cm', '≈ 12.57 cm'], 0,
              {0: 'Ja.', 1: 'Hast du 8 cm als Radius genommen?', 2: 'Das ist nur der halbe Umfang. Wie viele Radien gehören in den Umfang?'},
              sprich='d gleich acht Zentimeter: Wie lang ist der Umfang?',
              rueck_sprich={1: 'Hast du acht Zentimeter als Radius genommen?', 2: 'Das ist nur der halbe Umfang. Wie viele Radien gehören in den Umfang?'}),
         wahl('Frage 3', 'r = 6 cm: Wie gross ist die Fläche?', ['≈ 113.10 cm²', '≈ 37.70 cm²', '≈ 452.39 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist eine Länge: der Umfang.', 2: 'Hast du den Durchmesser quadriert?'},
              sprich='r gleich sechs Zentimeter: Wie gross ist die Fläche?',
              rueck_sprich={1: 'Das ist eine Länge, der Umfang.', 2: 'Hast du den Durchmesser quadriert?'}),
         wahl('Frage 4', 'Der Radius wird verdoppelt. Was geschieht mit der Fläche?', ['Sie vervierfacht sich.', 'Sie verdoppelt sich.', 'Sie bleibt gleich.'], 0,
              {0: 'Ja.', 1: 'Das gilt für den Umfang. Wie oft steht r in der Flächenformel?', 2: 'Ein grösserer Kreis hat mehr Fläche. Um welchen Faktor?'},
              sprich='Der Radius wird verdoppelt. Was geschieht mit der Fläche?',
              rueck_sprich={1: 'Das gilt für den Umfang. Wie oft steht r in der Flächenformel?', 2: 'Ein grösserer Kreis hat mehr Fläche. Um welchen Faktor?'}),
         wahl('Frage 5', 'U = 50 cm: Wie gross ist der Radius?', ['≈ 7.96 cm', '≈ 15.92 cm', '≈ 3.99 cm'], 0,
              {0: 'Ja.', 1: 'U : π ist eine andere Strecke. Welche?', 2: 'Eine Wurzel gehört zur Fläche, nicht zum Umfang.'},
              sprich='U gleich fünfzig Zentimeter: Wie gross ist der Radius?',
              rueck_sprich={1: 'U durch Pi ist eine andere Strecke. Welche?', 2: 'Eine Wurzel gehört zur Fläche, nicht zum Umfang.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Bogen und Sektor
# r = 4, φ = 45° (Startwert Arbeitsbereich 3): b = π ≈ 3.14 cm, A_SK = 2π ≈ 6.28 cm²; rückwärts b = 6 → φ ≈ 85.94°.
W3 = geo(-5.5, -5.5, 11)
K3 = KR(M0, 4, 1, 0.05)
PHI = lambda: [[0.3, {'w': 45}], ['@Bei-0.2', {'w': 45}], ['@Bei+0.8', {'w': 90}], ['@bei#2-0.2', {'w': 90}],
               ['@bei#2+0.9', {'w': 180}]]                     # bleibt bei 180° bis zum Szenenende
P3 = 360 * 6 / (8 * math.pi)                                    # 85.94°
clip('sektor', 5, 'Kreisteile sehen: Bogen und Sektor',
     'Zentriwinkel φ, Bogen b und Sektor als Anteil φ/360° des Kreises; b = φ/360° · 2πr, A = φ/360° · πr² = ½ b r; vorgelöst '
     'mit r = 4 cm und φ = 45°; rückwärts der Winkel aus dem Bogen; Rand = b + 2r.',
     ['Sektor', 'Bogenlänge', 'Zentriwinkel', 'Kreisausschnitt'], [
         sz('Sektor',
            'Zwei Radien schneiden aus dem Kreis einen Sektor, wie ein Tortenstück. Der Winkel zwischen ihnen heisst Zentriwinkel '
            'Phi. Das Stück der Kreislinie dazwischen ist der Bogen b.',
            n('Sektor: Kreisausschnitt', 300, 'blau', 44, ein='@Sektor'),
            f(r'\text{Zentriwinkel } \fb{\varphi}, \quad \text{Bogen } \fb{b}', 420, 46, ein='@heisst+0.2'),
            graf(W3, [K3, PKT(M0), T(-0.4, -0.7, 'M', 5, 'end', 30, False), S(M0, (4, 0), 5, dicke=3), S(M0, pol(M0, 4, 45), 5, dicke=3)], ein=0.3),
            graf(W3, [SEK(M0, 4, 0, 45)], ein='@Sektor', raster=False),
            graf(W3, [WI(M0, 0, 45, 2, 50), T(1.6, 0.6, 'φ', 2)], ein='@heisst+0.2', raster=False),
            graf(W3, [BOG(M0, 4, 0, 45), T(4.3, 2.0, 'b', 2, 'start')], ein='@Bogen', raster=False)),
         sz('Anteil',
            'Der Sektor ist ein Anteil des ganzen Kreises: Phi durch dreihundertsechzig Grad. Bei neunzig Grad ist es ein Viertel, '
            'bei hundertachtzig Grad die Hälfte.',
            f(r'\text{Anteil } \dfrac{\varphi}{360^\circ}', 300, 52, ein='@Anteil'),
            n('@90^\\circ@: ein Viertel|@180^\\circ@: die Hälfte', 450, 'blau', 44, ein='@Bei'),
            graf(W3, [K3, PKT(M0), mit(SEK(M0, 4, 0, 45), parameter=PHI(), bis='w'), mit(BOG(M0, 4, 0, 45), parameter=PHI(), bis='w'),
                      # «Viertel» nicht als Anker: Whisper hört «Phi» als «viel» — und das passt zu «Viertel» (Prüfung 08.10.2026)
                      mit(T(0, -2.6, '90° : 360° = ¼', 5, 'middle', 32, False), ein='@Bei+0.9', aus='@bei#2'),
                      mit(T(0, -2.6, '180° : 360° = ½', 5, 'middle', 32, False), ein='@Hälfte')], ein=0.3)),
         sz('Formeln',
            'Derselbe Anteil gilt für die Bogenlänge und für die Fläche. Der Bogen ist der Anteil vom Umfang, die Sektorfläche der '
            'Anteil von der Kreisfläche.',
            f(r'b = \dfrac{\varphi}{360^\circ} \cdot 2\pi r', 290, 50, ein='@Bogen'),
            f(r'A_{SK} = \dfrac{\varphi}{360^\circ} \cdot \pi r^2', 440, 50, ein='@Sektorfläche'),
            graf(W3, [K3, PKT(M0), SEK(M0, 4, 0, 45), BOG(M0, 4, 0, 45), WI(M0, 0, 45, 2, 50), T(1.6, 0.6, 'φ', 2)], ein=0.3)),
         sz('Vorgelöst',
            'Zum Beispiel r gleich vier Zentimeter und Phi gleich fünfundvierzig Grad. Das ist ein Achtel des Kreises. Der Bogen ist '
            'ein Achtel von acht Pi, also Pi, rund drei Komma eins vier Zentimeter. Die Fläche ist ein Achtel von sechzehn Pi, also '
            'zwei Pi, rund sechs Komma zwei acht Quadratzentimeter.',
            f(r'\dfrac{45^\circ}{360^\circ} = \dfrac{1}{8}', 250, 48, ein='@Achtel'),
            f(r'b = \tfrac{1}{8} \cdot 8\pi = \pi \approx \fc{3.14\,\mathrm{cm}}', 410, 44, ein='@also'),
            f(r'A_{SK} = \tfrac{1}{8} \cdot 16\pi = 2\pi \approx \fc{6.28\,\mathrm{cm}^2}', 530, 44, ein='@also#2'),
            graf(W3, [K3, PKT(M0), SEK(M0, 4, 0, 45), BOG(M0, 4, 0, 45), T(2, -0.6, 'r = 4', 5, 'middle', 28, False), T(1.6, 0.6, '45°', 2, 'start', 26, False)], ein=0.3),
            graf(W3, [S(M0, pol(M0, 4, w), 5, True, 2) for w in (90, 135, 180, 225, 270, 315)], ein='@Achtel', raster=False)),
         sz('Halb b mal r',
            'Kürzer geht es mit dem Bogen. Denn Pi r Quadrat ist zwei Pi r mal r halbe: Die Kreisfläche ist der Umfang mal r halbe, '
            'und derselbe Anteil davon gibt die Sektorfläche, ein Halb mal b mal r. Wie beim Dreieck mit der Grundseite b und der '
            'Höhe r. Ein Halb mal Pi mal vier gibt wieder zwei Pi.',
            f(r'\pi r^2 = 2\pi r \cdot \tfrac{r}{2}', 250, 46, ein='@Denn'),
            f(r'A_{SK} = \dfrac{\varphi}{360^\circ} \cdot 2\pi r \cdot \tfrac{r}{2} = \tfrac{1}{2}\, b \cdot r', 370, 44, ein='@Anteil'),
            f(r'\tfrac{1}{2} \cdot \pi \cdot 4 = \fc{2\pi}', 500, 48, ein='@wieder-1.2'),
            # das schmale «Dreieck» mit Grundseite b (orange) und Höhe r
            graf(W3, [K3, PKT(M0), SEK(M0, 4, 0, 45), BOG(M0, 4, 0, 45), T(4.25, 1.9, 'b', 2, 'start'), T(1.3, -0.6, 'r', 5)], ein=0.3)),
         sz('Rückwärts',
            'Kennt man den Bogen, findet man den Winkel. Bei r gleich vier und b gleich sechs Zentimeter: Bogen durch Umfang ist der '
            'Anteil, sechs durch acht Pi. Mal dreihundertsechzig Grad gibt rund fünfundachtzig Komma neun vier Grad.',
            f(r'\text{Anteil} = \dfrac{b}{2\pi r} = \dfrac{6}{8\pi}', 300, 48, ein='@Anteil'),
            f(r'\varphi = \dfrac{6}{8\pi} \cdot 360^\circ \approx \fc{85.94^\circ}', 450, 48, ein='@gibt'),
            graf(W3, [K3, PKT(M0), SEK(M0, 4, 0, P3), BOG(M0, 4, 0, P3), T(3.6, 3.3, 'b = 6', 2, 'start', 28, False), T(2, -0.6, 'r = 4', 5, 'middle', 28, False),
                      WI(M0, 0, P3, 2, 44)], ein=0.3),
            graf(W3, [T(1.3, 1.5, 'φ = ?', 2, 'middle', 26)], ein=0.3, aus='@gibt', raster=False),
            graf(W3, [T(1.4, 1.5, '85.94°', 3, 'middle', 26, False)], ein='@gibt', raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Erst den Anteil Phi durch dreihundertsechzig Grad. Er gilt für Bogen und Fläche. Und der Rand des Sektors '
            'ist der Bogen plus zwei Radien.',
            titel('Zum Mitnehmen', 250, 76),
            n('Anteil @\\tfrac{\\varphi}{360^\\circ}@ für Bogen und Fläche|Rand: @b + 2r@', 400, 'blau', 46, ein=1.2),
            graf(W3, [K3, PKT(M0), SEK(M0, 4, 0, 45), BOG(M0, 4, 0, 45)], ein=0.3),
            graf(W3, [S(M0, (4, 0), 2, dicke=8), S(M0, pol(M0, 4, 45), 2, dicke=8)], ein='@Rand', raster=False)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-sektor', 6, 'Kreisteile sehen: Kontrollfragen zu Bogen und Sektor',
     'Fünf Fragen: der Anteil zu 120°, eine Bogenlänge, die Sektorfläche aus Bogen und Radius, der Winkel zu einem Viertel des '
     'Umfangs und der Rand eines Sektors.',
     ['Sektor', 'Bogenlänge', 'Zentriwinkel', 'Kontrollfragen'], [
         sz('Frage 1',
            'Hundertzwanzig durch dreihundertsechzig ist ein Drittel.',
            f(r'\dfrac{120^\circ}{360^\circ} = \fc{\dfrac{1}{3}}', 300, 56, ein=1.0),
            graf(W3, [K3, SEK(M0, 4, 0, 120), BOG(M0, 4, 0, 120)], ein=1.0)),
         sz('Frage 2',
            'Der Anteil ist vierundfünfzig durch dreihundertsechzig, der Umfang zwanzig Pi. Der Bogen ist rund neun Komma vier zwei '
            'Zentimeter.',
            f(r'b = \tfrac{54^\circ}{360^\circ} \cdot 20\pi = 3\pi \approx \fc{9.42\,\mathrm{cm}}', 300, 46, ein=1.0),
            graf(geo(-11, -11, 22), [KR(M0, 10, 1, 0.04), SEK(M0, 10, 0, 54, 3, 0.15), BOG(M0, 10, 0, 54), PKT(M0), WI(M0, 0, 54, 2, 50),
                                     T(5, -1.2, 'r = 10', 5, 'middle', 30, False), T(2.6, 1.2, '54°', 2, 'start', 28, False),
                                     T(6.3, 9.0, 'b ≈ 9.42', 3, 'start', 30, False)], ein=1.0)),
         sz('Frage 3',
            'Die Sektorfläche ist ein Halb mal Bogen mal Radius: ein Halb mal acht mal fünf, also zwanzig Quadratzentimeter.',
            f(r'A_{SK} = \tfrac{1}{2} \cdot 8 \cdot 5 = \fc{20\,\mathrm{cm}^2}', 300, 50, ein=1.0),
            # b = 8, r = 5 → φ = 8 / (10π) · 360° ≈ 91.67° (nur für die Zeichnung)
            graf(geo(-6.5, -6.5, 13), [KR(M0, 5, 1, 0.04), SEK(M0, 5, 0, 91.67, 3, 0.3), BOG(M0, 5, 0, 91.67), PKT(M0),
                                       T(2.5, -0.8, 'r = 5', 5, 'middle', 30, False), T(3.9, 3.9, 'b = 8', 2, 'start', 30, False),
                                       T(1.9, 1.9, 'A = 20', 3, 'middle', 30, False)], ein=1.0)),
         sz('Frage 4',
            'Ein Viertel des Umfangs gehört zu einem Viertel des Vollwinkels: neunzig Grad.',
            f(r'\tfrac{1}{4} \cdot 360^\circ = \fc{90^\circ}', 300, 56, ein=1.0),
            graf(W3, [K3, SEK(M0, 4, 0, 90, 3, 0.2), BOG(M0, 4, 0, 90), PKT(M0), WI(M0, 0, 90, 2, 46), T(0.9, 0.9, '90°', 2, 'start', 28, False)], ein=1.0)),
         sz('Frage 5',
            'Der Bogen ist zwanzig durch dreihundertsechzig mal achtzehn Pi, also Pi. Dazu zwei Radien, achtzehn Zentimeter: zusammen '
            'rund einundzwanzig Komma eins vier Zentimeter.',
            f(r'U_S = \pi + 2 \cdot 9 \approx \fc{21.14\,\mathrm{cm}}', 300, 50, ein=1.0),
            graf(geo(-10.5, -10.5, 21), [KR(M0, 9, 1, 0.04), SEK(M0, 9, 0, 20), BOG(M0, 9, 0, 20, 2, 8), S(M0, (9, 0), 2, dicke=8),
                                         S(M0, pol(M0, 9, 20), 2, dicke=8)], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Bogen und Fläche über den Anteil, die Fläche auch als ein Halb mal b mal r. Zum Rand gehören zwei Radien.',
            titel('Zum Mitnehmen', 250, 76),
            n('Anteil @\\tfrac{\\varphi}{360^\\circ}@|@A_{SK} = \\tfrac{1}{2}\\, b \\cdot r@|Rand @b + 2r@', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'φ = 120°: Welcher Anteil des Kreises ist der Sektor?', ['ein Drittel', 'ein Viertel', 'ein Sechstel'], 0,
              {0: 'Ja.', 1: 'Ein Viertel wären 90°.', 2: 'Ein Sechstel wären 60°.'},
              sprich='Phi gleich hundertzwanzig Grad: Welcher Anteil des Kreises ist der Sektor?',
              rueck_sprich={1: 'Ein Viertel wären neunzig Grad.', 2: 'Ein Sechstel wären sechzig Grad.'}),
         wahl('Frage 2', 'r = 10 cm, φ = 54°: Wie lang ist der Bogen?', ['≈ 9.42 cm', '≈ 47.12 cm', '≈ 62.83 cm'], 0,
              {0: 'Ja.', 1: 'Ist das eine Länge oder eine Fläche?', 2: 'Das ist der ganze Umfang. Wo bleibt der Anteil?'},
              sprich='r gleich zehn Zentimeter, Phi gleich vierundfünfzig Grad: Wie lang ist der Bogen?',
              rueck_sprich={1: 'Ist das eine Länge oder eine Fläche?', 2: 'Das ist der ganze Umfang. Wo bleibt der Anteil?'}),
         wahl('Frage 3', 'Ein Sektor hat den Bogen 8 cm und den Radius 5 cm. Wie gross ist seine Fläche?', ['20 cm²', '40 cm²', 'ohne φ nicht lösbar'], 0,
              {0: 'Ja.', 1: 'Denk an die Dreiecksformel: Es fehlt ein Faktor.', 2: 'Es geht ohne Winkel. Denk an ein Dreieck mit der Grundseite b und der Höhe r.'},
              sprich='Ein Sektor hat den Bogen acht Zentimeter und den Radius fünf Zentimeter. Wie gross ist seine Fläche?',
              rueck_sprich={1: 'Denk an die Dreiecksformel: Es fehlt ein Faktor.', 2: 'Es geht ohne Winkel. Denk an ein Dreieck mit der Grundseite b und der Höhe r.'}),
         wahl('Frage 4', 'Der Bogen ist ein Viertel des Umfangs. Wie gross ist der Zentriwinkel?', ['90°', '0.25°', '45°'], 0,
              {0: 'Ja.', 1: 'Ein Viertel ist ein Anteil, kein Winkel. Wie viele Grad hat der Vollwinkel?', 2: '45° sind ein Achtel des Vollwinkels.'},
              sprich='Der Bogen ist ein Viertel des Umfangs. Wie gross ist der Zentriwinkel?',
              rueck_sprich={1: 'Ein Viertel ist ein Anteil, kein Winkel. Wie viele Grad hat der Vollwinkel?', 2: 'Fünfundvierzig Grad sind ein Achtel des Vollwinkels.'}),
         wahl('Frage 5', 'r = 9 cm, φ = 20°: Wie lang ist der ganze Rand des Sektors?', ['≈ 21.14 cm', '≈ 3.14 cm', '≈ 12.14 cm'], 0,
              {0: 'Ja.', 1: 'Das ist nur der Bogen. Was gehört noch zum Rand?', 2: 'Wie viele Radien begrenzen den Sektor?'},
              sprich='r gleich neun Zentimeter, Phi gleich zwanzig Grad: Wie lang ist der ganze Rand des Sektors?',
              rueck_sprich={1: 'Das ist nur der Bogen. Was gehört noch zum Rand?', 2: 'Wie viele Radien begrenzen den Sektor?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Segment und Kreisring
# r = 5 (Startwert Arbeitsbereich 4): 90° → Sektor 19.63, Dreieck 12.5, Segment 7.13; 60° → h_Δ 4.33, Dreieck 10.83,
# Sektor 13.09, Segment 2.26. Ring R = 6, r = 4: 20π ≈ 62.83 (zahlen.py).
W4 = geo(-6.5, -6.5, 13)
K4 = KR(M0, 5, 1, 0.05)
P90, P60 = (0, 5), pol(M0, 5, 60)
SEGW = lambda: [[0.3, {'w': 60}], ['@grösser-0.2', {'w': 60}], ['@liegt+0.5', {'w': 300}]]
W4r = geo(-7, -7, 14)
DR = 2 * 760 / 14                                               # Ringbreite 2 in Pixeln (dicker Kreis bei r_m = 5)
clip('segment', 7, 'Kreisteile sehen: Segment und Kreisring',
     'Segment = Sektor − Dreieck M P₁ P₂, bei 90° rechtwinklig, bei 60° gleichseitig (Höhe mit Pythagoras); über 180° Sektor + '
     'Dreieck. Kreisring π(R² − r²) = 2π r_m · b, vorgelöst mit R = 6 cm und r = 4 cm.',
     ['Kreissegment', 'Kreisabschnitt', 'Kreisring', 'mittlerer Radius'], [
         sz('Segment',
            'Eine Sehne schneidet vom Kreis ein Segment ab: die Fläche zwischen Sehne und Bogen. Man rechnet Sektor minus Dreieck. '
            'Das Dreieck hat die Ecken M, P eins und P zwei.',
            n('Segment: zwischen Sehne und Bogen', 300, 'blau', 44, ein='@Segment'),
            f(r'A_{SG} = A_{SK} - A_\Delta', 430, 52, ein='@minus'),
            graf(W4, [K4, PKT(M0), T(-0.4, -0.8, 'M', 5, 'end', 30, False), SEK(M0, 5, 0, 90, 3, 0.08, 2), S((5, 0), P90, 2, dicke=5),
                      PKT((5, 0)), PKT(P90), T(5.3, -0.8, 'P₁', 5, 'start', 30, False), T(0.4, 5.4, 'P₂', 5, 'start', 30, False)], ein=0.3),
            graf(W4, [SEG(M0, 5, 0, 90)], ein='@Fläche', raster=False),
            graf(W4, [V([M0, (5, 0), P90], 2, 0.15, dicke=3, gestrichelt=True)], ein='@Dreieck', raster=False)),
         sz('Bei 90 Grad',
            'Bei neunzig Grad ist das Dreieck rechtwinklig, die beiden Radien sind seine Katheten. Bei r gleich fünf Zentimeter ist '
            'der Sektor ein Viertel von fünfundzwanzig Pi, rund neunzehn Komma sechs drei. Das Dreieck hat ein Halb mal fünf mal '
            'fünf, also zwölf Komma fünf. Das Segment hat rund sieben Komma eins drei Quadratzentimeter.',
            f(r'A_{SK} = \tfrac{1}{4} \cdot 25\pi \approx 19.63', 270, 44, ein='@Viertel'),
            f(r'A_\Delta = \tfrac{1}{2} \cdot 5 \cdot 5 = 12.5', 380, 44, ein='@Halb'),
            f(r'A_{SG} \approx 19.63 - 12.5 \approx \fc{7.13\,\mathrm{cm}^2}', 490, 44, ein='@Segment'),
            graf(W4, [K4, PKT(M0), SEK(M0, 5, 0, 90, 3, 0.08, 2), SEG(M0, 5, 0, 90), V([M0, (5, 0), P90], 2, 0.15, dicke=3, gestrichelt=True),
                      S((5, 0), P90, 2, dicke=5), RW(M0, 0, 90, 2, px=26), T(2.5, -0.8, 'r = 5', 5, 'middle', 28, False),
                      T(-0.4, 2.5, 'r = 5', 5, 'end', 28, False)], ein=0.3)),
         sz('Bei 60 Grad',
            'Bei sechzig Grad ist das Dreieck gleichseitig, alle Seiten sind fünf Zentimeter lang. Seine Höhe kommt aus dem Satz des '
            'Pythagoras: die Wurzel aus fünf Quadrat minus zwei Komma fünf Quadrat, rund vier Komma drei drei. Das Dreieck hat rund '
            'zehn Komma acht drei, der Sektor dreizehn Komma null neun. Das Segment hat rund zwei Komma zwei sechs '
            'Quadratzentimeter.',
            f(r'h_\Delta = \sqrt{5^2 - 2.5^2} \approx 4.33', 250, 44, ein='@Wurzel'),
            f(r'A_\Delta = \tfrac{1}{2} \cdot 5 \cdot 4.33 \approx 10.83', 350, 42, ein='@Dreieck#2'),
            f(r'A_{SK} = \tfrac{1}{6} \cdot 25\pi \approx 13.09', 450, 42, ein='@Sektor'),
            f(r'A_{SG} \approx 13.09 - 10.83 \approx \fc{2.26\,\mathrm{cm}^2}', 560, 42, ein='@Segment'),
            graf(W4, [K4, PKT(M0), SEK(M0, 5, 0, 60, 3, 0.08, 2), SEG(M0, 5, 0, 60), V([M0, (5, 0), P60], 2, 0.15, dicke=3, gestrichelt=True),
                      S((5, 0), P60, 2, dicke=5), T(1.0, 2.6, '5', 5, 'end', 28, False)], ein=0.3),
            graf(W4, [S((2.5, 0), P60, 2, True, 3), RW((2.5, 0), 0, 90, 2, px=22), T(2.8, 2.0, 'hΔ', 2, 'start', 28),
                      T(1.25, -0.8, '2.5', 2, 'middle', 26, False)], ein='@Höhe', raster=False)),
         sz('Über 180 Grad',
            'Ist Phi grösser als hundertachtzig Grad, liegt das Dreieck im Segment. Dann wird es addiert: Sektor plus Dreieck.',
            f(r'\varphi \gt 180^\circ\!: \; A_{SG} = A_{SK} + A_\Delta', 320, 46, ein='@addiert'),
            # φ wächst von 60° auf 300°: Segment, Sehne und Dreieck laufen mit (Bogenpunkte als Formeln in w).
            graf(W4, [K4, PKT(M0), T(-0.4, -0.8, 'M', 5, 'end', 30, False),
                      mit(dict(art='vieleck', punkte=[['5*cosd(w*%d/40)' % k, '5*sind(w*%d/40)' % k] for k in range(41)], farbe=3,
                               fuellung=0.45, dicke=3), parameter=SEGW()),
                      mit(dict(art='vieleck', punkte=[[0, 0], [5, 0], ['5*cosd(w)', '5*sind(w)']], farbe=2, fuellung=0.15, dicke=3,
                               gestrichelt=True), parameter=SEGW()),
                      mit(S((5, 0), P60, 2, dicke=5), parameter=SEGW(), bis=['5*cosd(w)', '5*sind(w)'])], ein=0.3)),
         sz('Kreisring',
            'Ein Kreisring liegt zwischen zwei Kreisen um denselben Mittelpunkt. Seine Fläche ist die grosse Kreisfläche minus die '
            'kleine: Pi mal Aussenradius Quadrat minus Pi mal Innenradius Quadrat.',
            f(r'A = \pi R^2 - \pi r^2 = \pi (R^2 - r^2)', 320, 46, ein='@minus'),
            graf(W4r, [KR(M0, 5, 3, 0, dicke=round(DR, 1), deckkraft=0.3), KR(M0, 6, 1, 0, dicke=3), KR(M0, 4, 1, 0, dicke=3), PKT(M0),
                       S(M0, pol(M0, 6, 60), 5, dicke=3), T(1.4, 3.2, 'R', 5, 'end'), S(M0, (-4, 0), 5, dicke=3), T(-2, 0.4, 'r', 5)], ein=0.3)),
         sz('Mittlerer Umfang',
            'Mit der Ringbreite b, Aussenradius minus Innenradius, und dem mittleren Radius r m gilt auch: zwei Pi r m mal b, '
            'mittlerer Umfang mal Breite. Bei einem Aussenradius von sechs und einem Innenradius von vier Zentimetern: Pi mal die '
            'Differenz aus sechsunddreissig und sechzehn, also zwanzig Pi, rund zweiundsechzig Komma acht drei Quadratzentimeter. '
            'Zwei Pi mal fünf mal zwei gibt dasselbe.',
            f(r'A = 2\pi r_m \cdot b', 250, 50, ein='@mittlerer'),
            f(r'\pi (36 - 16) = 20\pi \approx \fc{62.83\,\mathrm{cm}^2}', 380, 44, ein='@Differenz'),
            f(r'2\pi \cdot 5 \cdot 2 = 20\pi', 490, 44, ein='@gibt-1.5'),
            graf(W4r, [KR(M0, 5, 3, 0, dicke=round(DR, 1), deckkraft=0.3), KR(M0, 6, 1, 0, dicke=3), KR(M0, 4, 1, 0, dicke=3), PKT(M0),
                       S(M0, pol(M0, 6, 60), 5, dicke=3), T(1.4, 3.2, 'R = 6', 5, 'end', 28, False), S(M0, (-4, 0), 5, dicke=3),
                       T(-2, 0.4, 'r = 4', 5, 'middle', 28, False)], ein=0.3),
            graf(W4r, [S(pol(M0, 4, 300), pol(M0, 6, 300), 2, dicke=6), T(3.4, -5.75, 'b = 2', 2, 'start', 28, False)], ein='@Ringbreite', raster=False),
            graf(W4r, [KR(M0, 5, 2, 0, dicke=3, gestrichelt=True), T(-4.6, 4.9, 'rₘ = 5', 2, 'end', 28, False)], ein='@mittleren', raster=False)),
         sz('Merke',
            'Zum Mitnehmen: Segment gleich Sektor minus Dreieck, über hundertachtzig Grad plus Dreieck. Der Ring ist die grosse minus '
            'die kleine Kreisfläche.',
            titel('Zum Mitnehmen', 250, 76),
            n('Segment: Sektor @-@ Dreieck (über @180^\\circ@: @+@)|Ring: @\\pi (R^2 - r^2) = 2\\pi r_m \\cdot b@', 400, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-segment', 8, 'Kreisteile sehen: Kontrollfragen zu Segment und Kreisring',
     'Fünf Fragen: das Segment über 180°, das Dreieck bei 90°, die Höhe des gleichseitigen Dreiecks, eine Ringfläche und zwei '
     'gleich breite Ringe.',
     ['Kreissegment', 'Kreisring', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei zweihundertvierzig Grad liegt das Dreieck im Segment. Es wird zum Sektor addiert.',
            f(r'A_{SG} = A_{SK} + A_\Delta', 300, 54, ein=1.0),
            graf(W4, [K4, PKT(M0), S((5, 0), pol(M0, 5, 240), 2, dicke=5), PKT((5, 0)), PKT(pol(M0, 5, 240))], ein=0.05),
            graf(W4, [SEG(M0, 5, 0, 240), V([M0, (5, 0), pol(M0, 5, 240)], 2, 0.15, dicke=3, gestrichelt=True)], ein=1.0, raster=False)),
         sz('Frage 2',
            'Die beiden Radien sind die Katheten. Ein Halb mal zehn mal zehn ist fünfzig Quadratzentimeter.',
            f(r'A_\Delta = \tfrac{1}{2} \cdot 10 \cdot 10 = \fc{50\,\mathrm{cm}^2}', 300, 50, ein=1.0),
            graf(geo(-12, -12, 24), [KR(M0, 10, 1, 0.04), V([M0, (10, 0), (0, 10)], 2, 0.2, dicke=3), RW(M0, 0, 90, 2, px=26), PKT(M0),
                                     T(5, -1.4, '10', 5, 'middle', 30, False), T(-0.8, 5, '10', 5, 'end', 30, False)], ein=1.0)),
         sz('Frage 3',
            'Die Höhe teilt das gleichseitige Dreieck in zwei rechtwinklige Hälften. Die Wurzel aus acht Quadrat minus vier Quadrat ist '
            'rund sechs Komma neun drei.',
            f(r'h_\Delta = \sqrt{8^2 - 4^2} = \sqrt{48} \approx \fc{6.93\,\mathrm{cm}}', 300, 46, ein=1.0),
            graf(geo(-1, -1.5, 10), [V([(0, 0), (8, 0), (4, 6.928)], 2, 0.15, dicke=3), S((4, 0), (4, 6.928), 3, True, 4), RW((4, 0), 0, 90, 5),
                                     T(2, -0.7, '4', 5, 'middle', 30, False), T(1.6, 3.8, '8', 5, 'end', 30, False), T(4.3, 3.2, 'hΔ', 3, 'start', 30)], ein=1.0)),
         sz('Frage 4',
            'Pi mal die Differenz aus neunundvierzig und neun, also vierzig Pi, rund hundertfünfundzwanzig Komma sechs sechs '
            'Quadratzentimeter.',
            f(r'A = \pi (7^2 - 3^2) = 40\pi \approx \fc{125.66\,\mathrm{cm}^2}', 300, 46, ein=1.0),
            graf(geo(-8, -8, 16), [KR(M0, 5, 3, 0, dicke=round(4 * 760 / 16, 1), deckkraft=0.3), KR(M0, 7, 1, 0, dicke=3), KR(M0, 3, 1, 0, dicke=3), PKT(M0),
                                   S(M0, pol(M0, 7, 50), 5, dicke=3), T(2.6, 3.6, 'R = 7', 5, 'end', 28, False), S(M0, (-3, 0), 5, dicke=3),
                                   T(-1.5, 0.4, 'r = 3', 5, 'middle', 28, False)], ein=1.0)),
         sz('Frage 5',
            'Bei gleicher Breite zählt der mittlere Umfang. Der äussere Ring hat den doppelten mittleren Radius, also doppelt so viel '
            'Fläche.',
            f(r'A = 2\pi r_m \cdot b', 300, 56, ein=1.0),
            # zwei Ringe, je 1 cm breit: mittlere Radien 3 (Ring A) und 6 (Ring B)
            graf(geo(-7.5, -7.5, 15), [KR(M0, 3, 3, 0, dicke=round(760 / 15, 1), deckkraft=0.3), KR(M0, 6, 3, 0, dicke=round(760 / 15, 1), deckkraft=0.3),
                                       KR(M0, 3, 2, 0, dicke=2, gestrichelt=True), KR(M0, 6, 2, 0, dicke=2, gestrichelt=True), PKT(M0),
                                       T(0, 3.9, 'A', 3, 'middle', 32, False), T(0, 6.9, 'B', 3, 'middle', 32, False)], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Unter hundertachtzig Grad minus, darüber plus Dreieck. Ring gleich grosse minus kleine Kreisfläche.',
            titel('Zum Mitnehmen', 250, 76),
            n('Segment: Sektor @-@ Dreieck,|über @180^\\circ@: Sektor @+@ Dreieck|Ring: @\\pi (R^2 - r^2)@', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Zentriwinkel 240°: Wie berechnet man das Segment?', ['Sektor + Dreieck', 'Sektor − Dreieck', 'Kreis − Sektor'], 0,
              {0: 'Ja.', 1: 'Wo liegt das Dreieck MP₁P₂ bei 240° — im Segment oder ausserhalb?', 2: 'Das ist der Rest des Kreises ohne den Sektor, nicht das Segment.'},
              sprich='Zentriwinkel zweihundertvierzig Grad: Wie berechnet man das Segment?',
              rueck_sprich={1: 'Wo liegt das Dreieck M P eins P zwei bei zweihundertvierzig Grad, im Segment oder ausserhalb?', 2: 'Das ist der Rest des Kreises ohne den Sektor, nicht das Segment.'}),
         wahl('Frage 2', 'r = 10 cm, φ = 90°: Wie gross ist das Dreieck MP₁P₂?', ['50 cm²', '100 cm²', '≈ 78.54 cm²'], 0,
              {0: 'Ja.', 1: 'Ist das Dreieck ein Quadrat?', 2: 'Das ist der Sektor. Gefragt ist das Dreieck.'},
              sprich='r gleich zehn Zentimeter, Phi gleich neunzig Grad: Wie gross ist das Dreieck M P eins P zwei?',
              rueck_sprich={1: 'Ist das Dreieck ein Quadrat?', 2: 'Das ist der Sektor. Gefragt ist das Dreieck.'}),
         wahl('Frage 3', 'Gleichseitiges Dreieck mit der Seite 8 cm (φ = 60°): Wie hoch ist es?', ['≈ 6.93 cm', '8 cm', '≈ 8.94 cm'], 0,
              {0: 'Ja.', 1: 'Die Höhe ist kürzer als die Seite.', 2: 'Im halben Dreieck ist die Seite die Hypotenuse.'},
              sprich='Gleichseitiges Dreieck mit der Seite acht Zentimeter, Phi gleich sechzig Grad: Wie hoch ist es?',
              rueck_sprich={1: 'Die Höhe ist kürzer als die Seite.', 2: 'Im halben Dreieck ist die Seite die Hypotenuse.'}),
         wahl('Frage 4', 'R = 7 cm, r = 3 cm: Wie gross ist die Ringfläche?', ['≈ 125.66 cm²', '≈ 50.27 cm²', '≈ 12.57 cm²'], 0,
              {0: 'Ja.', 1: 'Ist das der Ring — oder ein Kreis mit der Ringbreite R − r als Radius?', 2: 'Ist das eine Fläche? Wo sind die Quadrate?'},
              sprich='Aussenradius sieben, Innenradius drei Zentimeter: Wie gross ist die Ringfläche?',
              rueck_sprich={1: 'Ist das der Ring, oder ein Kreis mit der Ringbreite als Radius?', 2: 'Ist das eine Fläche? Wo sind die Quadrate?'}),
         wahl('Frage 5', 'Zwei Ringe sind 1 cm breit. Ring A hat den mittleren Radius 3 cm, Ring B 6 cm. Was gilt?',
              ['B hat doppelt so viel Fläche.', 'Beide haben gleich viel Fläche.', 'B hat viermal so viel Fläche.'], 0,
              {0: 'Ja.', 1: 'Gleich breit — aber ist der äussere Ring auch gleich lang?', 2: 'Quadriert wird hier nichts: mittlerer Umfang mal Breite.'},
              sprich='Zwei Ringe sind einen Zentimeter breit. Ring A hat den mittleren Radius drei Zentimeter, Ring B sechs Zentimeter. Was gilt?',
              rueck_sprich={1: 'Gleich breit, aber ist der äussere Ring auch gleich lang?', 2: 'Quadriert wird hier nichts: mittlerer Umfang mal Breite.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT))
