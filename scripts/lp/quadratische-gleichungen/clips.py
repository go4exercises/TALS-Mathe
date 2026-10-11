"""Erzeugt die zehn Drehbücher des Leitprogramms Quadratische Gleichungen (GF 2.2b, 11.10.2026).

  python3 scripts/lp/quadratische-gleichungen/clips.py

Reihe «Quadratische Gleichungen lösen», Dateien clips/g2-2b-lp-*.json, alle "probe": true. Je Kapitel ein
Einführungsclip und ein Kontrollclip (HOWTO-leitprogramme §7). Ausgangsmaterial: die Clips g2-2-lp-* des
abgelösten Leitprogramms «Lineare und quadratische Gleichungen» (scripts/lp/lineare-quadratische-gleichungen/clips.py);
Aufbau, Helfer und Farben von dort, die Beispiele nach der Themenseite g2-2b, die Kontrollfragen neu.

Zeiten auf dem Ton: Ein `ein`, `aus` oder Stützpunkt einer `bewegung` darf statt einer Zahl ein Anker sein,
'~Wort' oder '~zwei Wörter', mit Versatz '~Wort+0.6', bei Wiederholung '~Wort#2'. Gibt es wortzeiten.json
(wortzeiten.py, faster-whisper auf der Tonspur), steht der Anker auf dem gesprochenen Wort; sonst wird er aus der
Lage im Sprechertext geschätzt (18 Zeichen je Sekunde — lieber zu früh als zu spät, sonst verlängert die Schätzung
die Szene bei der Vertonung). Anker nie auf Zahlwörter legen: Whisper schreibt Ziffern.

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich). Wer den Text einer
Szene ändert, vertont sie neu (build-clip-ton.py <clip> --szenen n), misst die Wortzeiten neu und lässt das Skript
noch einmal laufen. Ablauf und Farben: README.md.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Gleichung, Terme, Parabel                       \\fa{…}
  2 orange = Umformung («| −5x»), Parameter k, rechte Seite  \\fb{…}
  3 grün   = Lösungen, Lösungsmenge, Nullstellen, Ergänzung  \\fc{…}
  4 rot    = Fehler, verlorene Lösung                        \\fd{…}
  5 Tinte  = neutral
"""
import json
import os
import re
import sys
import zlib

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
GX, GY, GB, GH, LX, OX = 1010, 175, 760, 760, 150, 700
PRAEFIX = 'g2-2b-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
WARNUNGEN = []


# ────────────────────────────────────────────────────────────── Anker
def _norm(w):
    return re.sub(r'[^\wäöü]', '', w.lower().replace('ß', 'ss'))


ZAHLWOERTER = ('null', 'eins', 'ein', 'eine', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn',
               'elf', 'zwölf', 'zwanzig', 'dreissig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig',
               'hundert', 'tausend', 'komma', 'halb', 'viertel', 'drittel')


def _zahlwort(w):
    return any(z in w for z in ZAHLWOERTER) and len(w) > 2 or w in ('null', 'elf', 'acht', 'drei', 'vier', 'zwei', 'fünf', 'sechs', 'neun', 'zehn')


def _passt(sw, ww):
    """Passt ein Wort des Sprechertexts (sw) zu einem Whisper-Wort (ww)? Whisper schreibt Ziffern, x² und klebt
    Wörter zusammen («0a», «49x»)."""
    if not sw or not ww:
        return False
    if sw == ww:
        return True
    if any(c.isdigit() for c in ww) and (_zahlwort(sw) or sw in ('minus', 'plus')):
        return True
    if len(sw) >= 1 and (ww.startswith(sw) or ww.endswith(sw)) and (len(sw) > 2 or any(c.isdigit() for c in ww)):
        return True
    if len(sw) > 4 and len(ww) > 4 and sw[:5] == ww[:5]:
        return True
    return False


def _zeiten(szene, wz):
    """Ordnet jedem Wort des Sprechertexts eine Startzeit zu: Ausrichtung (Needleman-Wunsch) gegen die Whisper-Wörter;
    Wörter ohne Partner werden zwischen den Nachbarn nach Zeichen verteilt."""
    S = [_norm(w) for w in szene['sprecher'].split()]
    W = [(_norm(w), t0) for w, t0, _ in wz['woerter']]
    n_, m_ = len(S), len(W)
    INF = -10 ** 9
    H = [[0] * (m_ + 1) for _ in range(n_ + 1)]
    for i in range(1, n_ + 1):
        H[i][0] = -i
    for j in range(1, m_ + 1):
        H[0][j] = -j
    for i in range(1, n_ + 1):
        for j in range(1, m_ + 1):
            H[i][j] = max(H[i - 1][j - 1] + (2 if _passt(S[i - 1], W[j - 1][0]) else -1), H[i - 1][j] - 1, H[i][j - 1] - 1)
    zu = [None] * n_
    i, j = n_, m_
    while i > 0 and j > 0:
        if H[i][j] == H[i - 1][j - 1] + (2 if _passt(S[i - 1], W[j - 1][0]) else -1):
            if _passt(S[i - 1], W[j - 1][0]):
                zu[i - 1] = W[j - 1][1]
            i, j = i - 1, j - 1
        elif H[i][j] == H[i - 1][j] - 1:
            # zusammengeklebte Whisper-Wörter: dasselbe Wort passt auch zum vorigen Sprecherwort
            if _passt(S[i - 1], W[j - 1][0]) if j > 0 else False:
                zu[i - 1] = W[j - 1][1]
            i -= 1
        else:
            j -= 1
    # Lücken füllen
    bek = [k for k in range(n_) if zu[k] is not None]
    for k in range(n_):
        if zu[k] is None:
            vor = max([b for b in bek if b < k], default=None)
            nach = min([b for b in bek if b > k], default=None)
            if vor is not None and nach is not None:
                zu[k] = zu[vor] + (zu[nach] - zu[vor]) * (k - vor) / (nach - vor)
            elif vor is not None:
                zu[k] = zu[vor] + 0.35 * (k - vor)
            elif nach is not None:
                zu[k] = max(0.4, zu[nach] - 0.35 * (nach - k))
            else:
                zu[k] = 0.4 + 0.35 * k
    return zu, sum(1 for b in bek) / max(1, n_)


def anker(clip, szene, a):
    """'~Wort[ Wort][#n][±s]' → Sekunden ab Szenenbeginn."""
    m = re.match(r'~(.+?)(?:#(\d+))?([+-]\d+(?:\.\d+)?)?$', a)
    if not m:
        raise SystemExit('Anker unlesbar: %r' % a)
    woerter, nr, vers = m.group(1).split(), int(m.group(2) or 1), float(m.group(3) or 0)
    ziel = [_norm(w) for w in woerter]
    S = [_norm(w) for w in szene['sprecher'].split()]
    funde = [i for i in range(len(S) - len(ziel) + 1) if S[i:i + len(ziel)] == ziel]
    if len(funde) < nr:
        raise SystemExit('%s/%s: Anker %r steht nicht im Sprechertext' % (clip, szene['name'], a))
    k = funde[nr - 1]
    wz = (WZ.get(clip) or WZ.get(clip[len(PRAEFIX):], {})).get(szene['name'])
    if wz and wz.get('sprecher') == szene['sprecher']:
        zu, anteil = _zeiten(szene, wz)
        if anteil < 0.6:
            WARNUNGEN.append('%s/%s: nur %d %% der Wörter ausgerichtet' % (clip, szene['name'], 100 * anteil))
        return round(max(0.45, zu[k] + vers), 2)
    # Schätzung aus dem Sprechertext (vor der Vertonung)
    pos = len(' '.join(szene['sprecher'].split()[:k]))
    return round(max(0.05, 0.4 + pos / 18.0 + vers), 2)


def aufloesen(clip, szene, x):
    """Ersetzt alle Anker in einer Szene (ein, aus, Stützpunkte von bewegung/bahn/parameter)."""
    if isinstance(x, dict):
        for k, v in list(x.items()):
            if k in ('ein', 'aus') and isinstance(v, str) and v.startswith('~'):
                x[k] = anker(clip, szene, v)
            elif k in ('bewegung', 'bahn', 'parameter', 'farbwechsel', 'grenzen') and isinstance(v, list):
                for st in v:
                    if isinstance(st, list) and st and isinstance(st[0], str) and st[0].startswith('~'):
                        st[0] = anker(clip, szene, st[0])
            else:
                aufloesen(clip, szene, v)
    elif isinstance(x, list):
        for v in x:
            aufloesen(clip, szene, v)


# ────────────────────────────────────────────────────────────── Bausteine (wie Vorgänger)
def graf(W, kurven=(), punkte=(), ein=0.05, geraden=(), parabeln=(), **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=list(geraden), parabeln=list(parabeln), punkte=list(punkte),
             pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def auflage(W, ein, **kw):
    """Zweite Lage über einem graf mit demselben Fenster: ohne Karo und Achsen, nur die eigenen Elemente."""
    return graf(W, ein=ein, achsen=False, raster=False, tippbar=False, **kw)


def par(a, u, v, farbe=1, null=True, beschr=True, bew=None):
    """Parabel y = a(x − u)² + v, mit grünen Nullstellen; bew = Liste [t, a, u, v] statt fest."""
    d = {'bewegung': bew or [[0, a, u, v]], 'farbe': farbe}
    if null:
        d['nullstellen'] = {'farbe': 3, 'beschriftung': beschr}
    return d


def ger(m, q, farbe=1, gestrichelt=False, dicke=None):
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    return d


def pt(x, y, farbe=3, text=None, bei=None, anker_='start', ein=None):
    d = dict(x=x, y=y, farbe=farbe, anker=anker_)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = bei
    if ein is not None:
        d['ein'] = ein
    return d


def f(t, y, g=56, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def op(t, y, ein, g=50):
    """Die Umformung rechts neben der Zeile, orange (wie im Heft)."""
    return f(r'\fb{\mid ' + t + '}', y, g, ein, OX)


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
        d['eingabe'] = list(eingabe)   # Antwort ohne Zeigegerät: zwei Zahlfelder (build-clips.py)
    return d


NICHT_GANZ = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'
JETZT_DU = sz('Jetzt du', 'Jetzt du: Löse die Aufgaben im Umformer unter dem Clip.',
              titel('Jetzt du', 280, 86),
              n('Löse die Aufgaben|im Umformer unter dem Clip.', 430, 'blau', 50, ein=0.6))
JETZT_DU_ANIM = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
                   titel('Jetzt du', 280, 86),
                   n('Erkunde diese Zusammenhänge|in der nachfolgenden Animation|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))

FERTIG = []


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip', folge=None):
    voll = PRAEFIX + name
    for q in szenen:
        aufloesen(voll, q, q['elemente'])
    alt = R + 'clips/' + voll + '.json'
    if os.path.exists(alt):
        alte = json.load(open(alt))['szenen']
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in alte}
        nach_name = {q['name']: q.get('dauer') for q in alte}
        for i, q in enumerate(szenen):
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
            elif nach_name.get(q['name']):
                # Text geändert: alte dauer behalten, damit build-clip-ton.py --szenen die übrigen Szenen aus der
                # bisherigen Spur schneiden kann; die Szene muss neu vertont werden.
                q['dauer'] = nach_name[q['name']]
                WARNUNGEN.append('%s: Szene %d «%s» hat neuen Text — build-clip-ton.py %s --szenen %d' % (voll, i + 1, q['name'], voll, i + 1))
    d = {'titel': titel_, 'dateiname': voll, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Gleichungen · quadratisch',
         'fach': 'Grundlagenfach', 'lerngebiet': '2 · Gleichungen, Ungleichungen und Gleichungssysteme',
         'lektion': ['g2-2b'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-11',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Quadratische Gleichungen lösen',
         'folge': folge, 'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms quadratische-gleichungen (GF 2.2b); gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    # Sprechertexte der Fragen-Szenen beginnen erst nach der Frage — die Elemente dürfen nicht vorher erscheinen
    for fr in fragen or []:
        sc = next(s for s in szenen if s['name'] == fr['szene'])
        for el in sc['elemente']:
            if el.get('ein', 1) <= fr['bei'] + 0.05 and el.get('typ') != 'graf':
                raise SystemExit('%s/%s: Element vor der Antwort sichtbar (ein %s)' % (voll, sc['name'], el.get('ein')))
    json.dump(d, open(alt, 'w'), ensure_ascii=False, indent=1)
    FERTIG.append(voll)
    print(voll, len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def fenster(x0, x1, y0, y1, xt, yt_):
    return dict(xbereich=[x0, x1], ybereich=[y0, y1], xteilung=yt(*xt), yteilung=yt(*yt_))


ODER = r'\;\;\text{oder}\;\;'

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
W1a = fenster(-5, 5, -3, 12, (-4, -3, -2, -1, 1, 2, 3, 4), (3, 6, 9))
W1b = fenster(-3, 7, -3, 12, (-2, -1, 1, 2, 3, 4, 5, 6), (3, 6, 9))
clip('wurzel', 'Quadratische Gleichungen lösen: erkennen und Wurzel ziehen',
     'Was eine quadratische Gleichung ist, wie man sie auf die Normalform bringt — und wie man x² = r und (x − 2)² = 9 '
     'mit der Wurzel löst: zwei, eine oder keine Lösung.',
     ['quadratische Gleichung', 'Normalform', 'Wurzelziehen', 'reinquadratisch'], [
         sz('Quadratisch',
            'Eine quadratische Gleichung hat die Form a x Quadrat plus b x plus c gleich null, mit a ungleich null. '
            'a x Quadrat ist das quadratische Glied, b x das lineare und c das konstante Glied.',
            titel('Quadratische Gleichung', 270, 80),
            f(r'a x^2 + b x + c = 0 \quad (a \neq 0)', 410, 60, ein='~Form'),
            n('@a x^2@: quadratisches Glied|@b x@: lineares Glied|@c@: konstantes Glied', 530, 'blau', 46, ein='~ist das')),
         sz('Normalform',
            'Teilt man durch a, steht vorne nur noch x Quadrat: Das ist die Normalform. Zum Beispiel zwei x Quadrat '
            'plus acht x minus zehn gleich null. Geteilt durch zwei: x Quadrat plus vier x minus fünf gleich null. '
            'Die Lösungen bleiben dieselben.',
            f(r'x^2 + p x + q = 0', 280, 60, ein='~Normalform'),
            f(r'2x^2 + 8x - 10 = 0', 420, 54, ein='~Zum Beispiel'),
            op(':2', 420, '~Geteilt'),
            f(r'x^2 + 4x - 5 = 0', 520, 54, ein='~Geteilt+1.2'),
            n('Die Lösungen bleiben dieselben.', 640, 'blau', 44, ein='~Lösungen')),
         sz('Wurzel ziehen',
            'Fehlt das lineare Glied, hilft die Wurzel. x Quadrat gleich neun: Welche Zahlen haben das Quadrat neun? '
            'Drei und minus drei. Beide gehören dazu. Im Bild trifft die Waagrechte y gleich neun die Parabel zweimal.',
            f(r'x^2 = 9', 280, 64, ein=0.3),
            f(r'x = \pm 3', 400, 60, ein='~Beide-1.4'),
            f(r'\mathbb{L} = \{\fc{-3};\ \fc{3}\}', 520, 56, ein='~Beide'),
            graf(W1a, kurven=[dict(formel='9', farbe=2, gestrichelt=True, dicke=3)], parabeln=[par(1, 0, 0, null=False)], ein=0.3),
            auflage(W1a, '~trifft', punkte=[pt(-3, 9, 3, '(−3 | 9)', [-3.3, 10.4], 'end'), pt(3, 9, 3, '(3 | 9)', [3.3, 10.4])])),
         sz('Zwei, eine, keine',
            'Allgemein bei x Quadrat gleich r: Ist r positiv, gibt es zwei Lösungen. Ist r null, gibt es nur eine, '
            'nämlich null. Ist r negativ, gibt es keine, denn ein Quadrat ist nie negativ.',
            f(r'x^2 = \fb{r}', 270, 60, ein=0.3),
            n('@r \\gt 0@: zwei Lösungen, @x = \\pm\\sqrt{r}@', 390, 'blau', 44, ein='~positiv'),
            n('@r = 0@: eine Lösung, @x = 0@', 480, 'blau', 44, ein='~nämlich'),
            n('@r \\lt 0@: keine Lösung, @\\mathbb{L} = \\{\\,\\}@', 570, 'blau', 44, ein='~negativ'),
            # Die Waagrechte y = r sinkt mit dem Satz: r = 4 (zwei Schnittpunkte), «Ist r null» → 0 (berührt im
            # Scheitel), «Ist r negativ» → −2 (kein Schnittpunkt).
            graf(W1a, kurven=[dict(formel='x**2', farbe=1)],
                 geraden=[{'bewegung': [[0, 0, 4], ['~gibt es nur', 0, 4], ['~gibt es nur+1.2', 0, 0], ['~negativ', 0, 0],
                                        ['~negativ+1.2', 0, -2]],
                           'farbe': 2, 'gestrichelt': True, 'dicke': 3,
                           'schnitte': {'kurve': 0, 'farbe': 3, 'beschriftung': False}}], ein=0.3)),
         sz('Mit Klammer',
            'Steht ein Quadrat mit Klammer da, geht es genauso. Klammer x minus zwei, im Quadrat, gleich neun. '
            'Die Klammer ist drei oder minus drei. Also ist x gleich fünf oder x gleich minus eins.',
            f(r'(x - 2)^2 = 9', 280, 60, ein=0.3),
            f(r'x - 2 = \pm 3', 400, 58, ein='~Die Klammer'),
            f(r'x = \fc{5}' + ODER + r'x = \fc{-1}', 520, 52, ein='~Also'),
            # Die Parabel rückt um 2 nach rechts, während «Klammer x minus zwei, im Quadrat» gesprochen wird.
            graf(W1b, kurven=[dict(formel='9', farbe=2, gestrichelt=True, dicke=3)],
                 parabeln=[par(1, 0, 0, null=False, bew=[[0, 1, 0, 0], ['~Klammer#2', 1, 0, 0], ['~Klammer#2+2.2', 1, 2, 0]])], ein=0.3),
            auflage(W1b, '~Also', punkte=[pt(-1, 9, 3, '(−1 | 9)', [-1.35, 7.6], 'end'), pt(5, 9, 3, '(5 | 9)', [5.35, 7.6])])),
         sz('Der Fehler',
            'Der häufigste Fehler: nur die positive Wurzel. Wer bei x Quadrat gleich neun nur drei schreibt, verliert '
            'minus drei. Und aus einer Summe zieht man nie gliedweise die Wurzel. Erst x Quadrat allein auf eine Seite bringen.',
            f(r'x^2 = 9 \;\Rightarrow\; x = 3 \quad \fd{\text{unvollständig}}', 290, 54, ein='~Wer'),
            n('Auch @(-3)^2 = 9@.', 400, 'rot', 44, ein='~verliert'),
            n('Erst @x^2@ allein auf eine Seite,|dann die Wurzel ziehen.', 520, 'blau', 44, ein='~Erst')),
         sz('Merke',
            'Zum Mitnehmen: Erst x Quadrat oder die Klammer im Quadrat allein auf eine Seite. Dann die Wurzel mit plus und minus. '
            'Ist die rechte Seite negativ, ist die Lösungsmenge leer.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x^2 = r \;\Rightarrow\; x = \pm\sqrt{r} \quad (r \ge 0)', 400, 54, ein='~Dann'),
            f(r'r \lt 0: \;\; \mathbb{L} = \{\,\}', 520, 54, ein='~Ist die')),
         JETZT_DU,
     ], folge=1)

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
W1k = fenster(-6, 4, -3, 12, (-5, -4, -3, -2, -1, 1, 2, 3), (3, 6, 9))
clip('kontrolle-wurzel', 'Quadratische Gleichungen lösen: Kontrollfragen zum Wurzelziehen',
     'Fünf Fragen: Ist die Gleichung quadratisch? Wie heisst die Normalform? x² = 64, x² + 25 = 0 und (x + 1)² = 9.',
     ['quadratische Gleichung', 'Normalform', 'Wurzelziehen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Ausmultipliziert steht x Quadrat plus zwei x gleich fünf da: quadratisch. Bei der zweiten heben sich die '
            'x Quadrat weg, sie ist linear.',
            f(r'x(x + 2) = 5 \;\Rightarrow\; x^2 + 2x = 5', 300, 52, ein='~Ausmultipliziert'),
            f(r'x^2 + 4x = x^2 - 1 \;\Rightarrow\; 4x = -1', 420, 52, ein='~zweiten'),
            n('linear: @x^2@ hebt sich weg', 540, 'blau', 44, ein='~linear')),
         sz('Frage 2',
            'Jedes Glied wird durch drei geteilt: x Quadrat minus drei x plus zwei gleich null.',
            f(r'3x^2 - 9x + 6 = 0', 300, 56, ein='~Jedes'),
            op(':3', 300, '~geteilt'),
            f(r'x^2 - 3x + 2 = 0', 420, 56, ein='~geteilt+0.8')),
         sz('Frage 3',
            'Acht mal acht ist vierundsechzig, minus acht mal minus acht auch. Beide gehören dazu.',
            f(r'x = \pm 8', 300, 60, ein='~Acht'),
            f(r'\mathbb{L} = \{-8;\ 8\}', 420, 56, ein='~Beide')),
         sz('Frage 4',
            'Es bleibt x Quadrat gleich minus fünfundzwanzig. Ein Quadrat ist nie negativ: Die Lösungsmenge ist leer.',
            f(r'x^2 = -25', 300, 60, ein='~Es bleibt'),
            f(r'\mathbb{L} = \{\,\}', 420, 60, ein='~Lösungsmenge')),
         sz('Frage 5',
            'Die Klammer ist drei oder minus drei. Also ist x gleich zwei oder minus vier. Die positive Lösung ist zwei.',
            f(r'x + 1 = \pm 3', 300, 58, ein='~Die Klammer'),
            f(r'x = \fc{2}' + ODER + r'x = \fc{-4}', 420, 52, ein='~Also'),
            graf(W1k, ein=0.05),
            auflage(W1k, '~Die Klammer', kurven=[dict(formel='9', farbe=2, gestrichelt=True, dicke=3)], parabeln=[par(1, -1, 0, null=False)]),
            auflage(W1k, '~positive', punkte=[pt(-4, 9, 3, '(−4 | 9)', [-4.35, 7.6], 'end'), pt(2, 9, 3, '(2 | 9)', [2.35, 7.6])])),
         sz('Merke',
            'Zum Mitnehmen: Erst ordnen, dann den Typ bestimmen. Die Wurzel gibt plus und minus. '
            'Eine negative rechte Seite heisst: keine Lösung.',
            titel('Zum Mitnehmen', 250, 76),
            n('erst ordnen, dann den Typ bestimmen|@\\pm@ beim Wurzelziehen|@x^2 = r \\lt 0@: @\\mathbb{L} = \\{\\,\\}@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Welche Gleichung ist quadratisch?',
              ['x(x + 2) = 5', 'x² + 4x = x² − 1', '3x + 7 = 0'], 0,
              {0: 'Ja.',
               1: 'Ordne zuerst: Was geschieht mit x², wenn du beidseitig x² abziehst?',
               2: 'Kommt hier überhaupt ein x² vor?'},
              sprich='Welche Gleichung ist quadratisch?',
              rueck_sprich={1: 'Ordne zuerst: Was geschieht mit x Quadrat, wenn du beidseitig x Quadrat abziehst?',
                            2: 'Kommt hier überhaupt ein x Quadrat vor?'}),
         wahl('Frage 2', '3x² − 9x + 6 = 0: Wie heisst die Normalform?',
              ['x² − 3x + 2 = 0', 'x² − 9x + 6 = 0', 'x² − 3x + 6 = 0'], 0,
              {0: 'Ja.',
               1: 'Durch 3 teilen heisst: jedes Glied durch 3.',
               2: 'Auch die 6 wird durch 3 geteilt.'},
              sprich='Drei x Quadrat minus neun x plus sechs gleich null: Wie heisst die Normalform?',
              rueck_sprich={1: 'Durch drei teilen heisst: jedes Glied durch drei.',
                            2: 'Auch die Sechs wird durch drei geteilt.'}),
         wahl('Frage 3', 'x² = 64: Welche Lösungsmenge?',
              ['𝕃 = {−8; 8}', '𝕃 = {8}', '𝕃 = {32}'], 0,
              {0: 'Ja.',
               1: 'Was ist (−8)²?',
               2: 'Gesucht ist die Zahl, deren Quadrat 64 ist — nicht die Hälfte von 64.'},
              sprich='x Quadrat gleich vierundsechzig: Welche Lösungsmenge?',
              rueck_sprich={1: 'Was ist minus acht im Quadrat?',
                            2: 'Gesucht ist die Zahl, deren Quadrat vierundsechzig ist, nicht die Hälfte von vierundsechzig.'}),
         wahl('Frage 4', 'x² + 25 = 0: Welche Lösungsmenge?',
              ['𝕃 = { }', '𝕃 = {−5; 5}', '𝕃 = {5}'], 0,
              {0: 'Ja.',
               1: 'Setz 5 ein: 25 + 25 ist nicht 0. Bring die 25 auf die andere Seite — was steht dann rechts?',
               2: 'Setz 5 ein: 25 + 25 ist nicht 0. Bring die 25 auf die andere Seite — was steht dann rechts?'},
              sprich='x Quadrat plus fünfundzwanzig gleich null: Welche Lösungsmenge?',
              rueck_sprich={1: 'Setz fünf ein: fünfundzwanzig plus fünfundzwanzig ist nicht null. Bring die fünfundzwanzig auf die andere Seite. Was steht dann rechts?',
                            2: 'Setz fünf ein: fünfundzwanzig plus fünfundzwanzig ist nicht null. Bring die fünfundzwanzig auf die andere Seite. Was steht dann rechts?'}),
         klick('Frage 5', '(x + 1)² = 9: Tipp die positive Lösung auf der x-Achse an.',
               [2, 0], 'Getroffen: x = 2.',
               [{'bei': [4, 0], 'text': 'Vorzeichen: x + 1 = 3 heisst x = 3 − 1.',
                 'sprich': 'Vorzeichen. x plus eins gleich drei heisst x gleich drei minus eins.'},
                {'bei': [3, 0], 'text': 'Die Klammer ist 3, nicht x. Zieh noch 1 ab.',
                 'sprich': 'Die Klammer ist drei, nicht x. Zieh noch eins ab.'},
                {'bei': [-4, 0], 'text': 'Das ist die negative Lösung.',
                 'sprich': 'Das ist die negative Lösung.'}],
               NICHT_GANZ,
               sprich='Klammer x plus eins, im Quadrat, gleich neun: Tipp die positive Lösung auf der x-Achse an.',
               falsch_sprich=NICHT_GANZ),
     ], art='Kontrollclip', folge=2)

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
W2v = fenster(-2, 7, -8, 27, (-1, 1, 2, 3, 4, 5, 6), (-5, 5, 10, 15, 20, 25))
W2 = fenster(-2, 7, -8, 6, (-1, 1, 2, 3, 4, 5, 6), (-6, -4, -2, 2, 4))
W2b = fenster(-1, 6, -2, 6, (1, 2, 3, 4, 5), (-1, 2, 4))
clip('faktorisieren', 'Quadratische Gleichungen lösen: ausklammern und faktorisieren',
     'Der Satz vom Nullprodukt: ausklammern bei x² = 5x, ein Binom bei x² − 6x + 9 = 0, der Zweiklammersatz bei '
     'x² − 7x + 12 = 0 — und der Satz von Vieta dahinter. Und warum man nicht durch x teilt.',
     ['quadratische Gleichung', 'Nullprodukt', 'ausklammern', 'Binom', 'Zweiklammersatz', 'Vieta'], [
         sz('Nullprodukt',
            'Ein Produkt ist genau dann null, wenn mindestens ein Faktor null ist. Darauf beruht das Faktorisieren: '
            'Steht rechts null und links ein Produkt, setzt man jeden Faktor null.',
            titel('Nullprodukt', 260, 80),
            f(r'a \cdot b = 0 \iff a = 0 \;\text{oder}\; b = 0', 400, 52, ein='~genau'),
            n('rechts @0@, links ein Produkt:|jeden Faktor null setzen', 520, 'blau', 44, ein='~Steht')),
         sz('Ausklammern',
            'Fehlt das konstante Glied, klammere x aus. x Quadrat gleich fünf x: Minus fünf x gibt x Quadrat minus fünf x '
            'gleich null. Ausgeklammert: x mal Klammer x minus fünf. Also ist x gleich null oder x gleich fünf.',
            f(r'x^2 = 5x', 260, 52, ein=0.3),
            op('-5x', 260, '~Minus'),
            f(r'x^2 - 5x = 0', 350, 52, ein='~gibt'),
            f(r'\fa{x} \cdot (x - 5) = 0', 440, 52, ein='~Ausgeklammert'),
            f(r'x = \fc{0}' + ODER + r'x = \fc{5}', 530, 50, ein='~Also'),
            # Beide Seiten minus 5x: y = x² wird zu x·(x − 5), die Gerade y = 5x zur x-Achse — die Schnittstellen
            # bleiben in jedem Zwischenstand 0 und 5. Die Nullstellen kommen mit «Also».
            graf(W2v, kurven=[{'bewegung': [[0, 1, 0, 0], ['~Minus', 1, 0, 0], ['~Minus+2.4', 1, 0, 5]], 'polynom': True, 'farbe': 1}],
                 geraden=[{'bewegung': [[0, 5, 0], ['~Minus', 5, 0], ['~Minus+2.4', 0, 0]], 'farbe': 2}], ein=0.3),
            auflage(W2v, '~Also', parabeln=[par(1, 2.5, -6.25)])),
         sz('Nicht teilen',
            'Wer durch x teilt, erhält nur x gleich fünf. Die Lösung null geht verloren, denn Teilen durch x setzt voraus, '
            'dass x nicht null ist.',
            f(r'x^2 = 5x', 280, 56, ein=0.3),
            op(':x', 280, '~teilt', g=54),
            f(r'x = 5', 380, 56, ein='~erhält'),
            f(r'\fd{x = 0 \text{ fehlt}}', 480, 56, ein='~verloren'),
            n('Teilen durch @x@ setzt @x \\neq 0@ voraus.', 600, 'rot', 44, ein='~setzt'),
            graf(W2, parabeln=[par(1, 2.5, -6.25, null=False)], ein=0.6),
            auflage(W2, '~erhält', punkte=[pt(5, 0, 3, '(5 | 0)', [5.3, -1.6])]),
            auflage(W2, '~verloren', punkte=[pt(0, 0, 4, '(0 | 0) verloren', [0.3, 0.6])])),
         sz('Binom',
            'Manchmal steht ein Binom da. x Quadrat minus sechs x plus neun ist Klammer x minus drei, im Quadrat. '
            'Die Gleichung hat nur eine Lösung: drei. Die Parabel berührt die x-Achse.',
            f(r'x^2 - 6x + 9 = 0', 290, 54, ein=0.3),
            f(r'(x - 3)^2 = 0', 400, 54, ein='~ist Klammer'),
            f(r'\mathbb{L} = \{\fc{3}\}', 510, 56, ein='~nur'),
            graf(W2b, parabeln=[par(1, 3, 0, null=False)], ein='~ist Klammer'),
            auflage(W2b, '~berührt', punkte=[pt(3, 0, 3, '(3 | 0)', [3.2, -1.0])])),
         sz('Zweiklammersatz',
            'Sonst hilft oft der Zweiklammersatz. Bei x Quadrat minus sieben x plus zwölf suchst du die beiden Lösungen: '
            'Ihr Produkt ist zwölf, ihre Summe sieben, das Gegenteil von minus sieben. Das sind drei und vier. Also Klammer '
            'x minus drei mal Klammer x minus vier gleich null.',
            f(r'x^2 - 7x + 12 = 0', 260, 54, ein=0.3),
            n('Lösungen: Produkt @12@, Summe @7 = -p@', 360, 'blau', 44, ein='~Produkt'),
            n('@3 \\cdot 4 = 12@; @3 + 4 = 7@', 450, 'blau', 44, ein='~Das sind'),
            f(r'(x - 3)(x - 4) = 0', 560, 54, ein='~Also'),
            f(r'\mathbb{L} = \{\fc{3};\ \fc{4}\}', 670, 54, ein='~Also+2.6'),
            graf(W2b, parabeln=[par(1, 3.5, -0.25, beschr=False)], ein='~Also',
                 punkte=[pt(3, 0, 3, '3', [2.8, 0.6], 'end'), pt(4, 0, 3, '4', [4.2, 0.6])])),
         sz('Vieta',
            'Dahinter steckt der Satz von Vieta. Für x Quadrat plus p x plus q gleich null gilt: Die Summe der Lösungen '
            'ist minus p, ihr Produkt ist q. Damit kannst du jede Lösung auch kontrollieren.',
            f(r'x^2 + p x + q = 0', 280, 56, ein='~Für'),
            f(r'x_1 + x_2 = -p, \qquad x_1 \cdot x_2 = q', 400, 54, ein='~Summe'),
            n('hier: @3 + 4 = 7 = -p@; @3 \\cdot 4 = 12 = q@', 530, 'blau', 44, ein='~kontrollieren-1.0')),
         sz('Merke',
            'Zum Mitnehmen: Rechts muss null stehen. Dann ausklammern, ein Binom erkennen oder die beiden Lösungen über ihr '
            'Produkt und ihre Summe finden. Nie durch x teilen.',
            titel('Zum Mitnehmen', 240, 76),
            n('rechts @0@|ausklammern, Binom oder Zweiklammersatz|nie durch @x@ teilen', 380, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ], folge=3)

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
W2k = fenster(-7, 4, -14, 6, (-6, -5, -4, -3, -2, -1, 1, 2, 3), (-12, -8, -4, 4))
clip('kontrolle-faktorisieren', 'Quadratische Gleichungen lösen: Kontrollfragen zum Faktorisieren',
     'Fünf Fragen zum Nullprodukt, zur verlorenen Lösung, zu einem Binom, zum Zweiklammersatz und zu x² + 3x − 10 = 0.',
     ['Nullprodukt', 'Binom', 'Zweiklammersatz', 'Kontrollfragen'], [
         sz('Frage 1',
            'Ein Faktor null genügt: x gleich null oder x minus sechs gleich null. Beide Lösungen gehören dazu.',
            f(r'x = 0' + ODER + r'x - 6 = 0', 300, 52, ein='~Ein Faktor'),
            f(r'\mathbb{L} = \{0;\ 6\}', 420, 56, ein='~Beide')),
         sz('Frage 2',
            'Teilen durch x setzt x ungleich null voraus. So geht die Lösung null verloren. Richtig: drei x mal Klammer '
            'x minus vier gleich null.',
            f(r'3x^2 = 12x \;\Rightarrow\; 3x\,(x - 4) = 0', 300, 52, ein='~Richtig'),
            f(r'\mathbb{L} = \{\fd{0};\ 4\}', 420, 56, ein='~Richtig+2.4')),
         sz('Frage 3',
            'Klammer x minus fünf, im Quadrat, gibt x Quadrat minus zehn x plus fünfundzwanzig. Die einzige Lösung ist fünf.',
            f(r'(x - 5)^2 = x^2 - 10x + 25', 300, 52, ein='~Klammer'),
            f(r'\mathbb{L} = \{5\}', 420, 56, ein='~einzige')),
         sz('Frage 4',
            'Die Lösungen sind minus zwei und sieben: Produkt minus vierzehn, Summe fünf. Also Klammer x minus sieben.',
            f(r'(x + 2)(x - \fc{7})', 300, 58, ein='~Also'),
            n('@-2 \\cdot 7 = -14@; @-2 + 7 = 5@', 430, 'blau', 44, ein='~Produkt')),
         sz('Frage 5',
            'Die beiden Lösungen haben das Produkt minus zehn und die Summe minus drei: minus fünf und zwei. Klammer x plus '
            'fünf mal Klammer x minus zwei. Die negative Lösung ist minus fünf.',
            n('Lösungen: Produkt @-10@, Summe @-3@', 280, 'blau', 44, ein='~Die beiden'),
            f(r'(x + 5)(x - 2) = 0', 390, 56, ein='~Klammer'),
            f(r'x = \fc{-5}' + ODER + r'x = \fc{2}', 500, 52, ein='~negative'),
            graf(W2k, ein=0.05),
            auflage(W2k, '~Klammer', parabeln=[par(1, -1.5, -12.25)])),
         sz('Merke',
            'Zum Mitnehmen: Ein Faktor null genügt. Aus Klammer x plus fünf wird x gleich minus fünf. Und nie durch x teilen.',
            titel('Zum Mitnehmen', 250, 76),
            n('ein Faktor @= 0@ genügt|@(x + 5) = 0 \\Rightarrow x = -5@|nie durch @x@ teilen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'x(x − 6) = 0: Welche Lösungsmenge?',
              ['{0; 6}', '{6}', '{−6; 0}'], 0,
              {0: 'Ja.',
               1: 'Auch der Faktor x kann null sein.',
               2: 'Setz −6 ein: Ist (−6) · (−12) null?'},
              sprich='x mal Klammer x minus sechs gleich null: Welche Lösungsmenge?',
              rueck_sprich={1: 'Auch der Faktor x kann null sein.',
                            2: 'Setz minus sechs ein. Ist minus sechs mal minus zwölf null?'}),
         wahl('Frage 2', 'Aus 3x² = 12x wird durch x geteilt 3x = 12. Welche Lösung fehlt?',
              ['x = 0', 'x = −4', 'keine'], 0,
              {0: 'Ja.',
               1: 'Setz −4 ein: Stimmt 3 · 16 = 12 · (−4)?',
               2: 'Teilen durch x setzt etwas voraus. Welcher Wert ist damit ausgeschlossen?'},
              sprich='Aus drei x Quadrat gleich zwölf x wird durch x geteilt drei x gleich zwölf. Welche Lösung fehlt?',
              rueck_sprich={1: 'Setz minus vier ein. Stimmt drei mal sechzehn gleich zwölf mal minus vier?',
                            2: 'Teilen durch x setzt etwas voraus. Welcher Wert ist damit ausgeschlossen?'}),
         wahl('Frage 3', 'x² − 10x + 25 = 0 ist ein Binom. Welches?',
              ['(x − 5)² = 0', '(x + 5)² = 0', '(x − 25)² = 0'], 0,
              {0: 'Ja.',
               1: '(x + 5)² gibt +10x. Hier steht −10x.',
               2: 'Multipliziere (x − 25)² aus: Gibt das −10x?'},
              sprich='x Quadrat minus zehn x plus fünfundzwanzig gleich null ist ein Binom. Welches?',
              rueck_sprich={1: 'Klammer x plus fünf, im Quadrat, gibt plus zehn x. Hier steht minus zehn x.',
                            2: 'Multipliziere Klammer x minus fünfundzwanzig, im Quadrat, aus. Gibt das minus zehn x?'}),
         wahl('Frage 4', 'x² − 5x − 14 = (x + 2)(x − □). Welche Zahl fehlt?',
              ['7', '−7', '12'], 0,
              {0: 'Ja.',
               1: '(x + 2)(x + 7) gibt +14. Gesucht ist −14.',
               2: 'Multipliziere aus: 2 · (−12) ist nicht −14.'},
              sprich='x Quadrat minus fünf x minus vierzehn gleich Klammer x plus zwei mal Klammer x minus Kästchen. Welche Zahl fehlt?',
              rueck_sprich={1: 'Klammer x plus zwei mal Klammer x plus sieben gibt plus vierzehn. Gesucht ist minus vierzehn.',
                            2: 'Multipliziere aus: zwei mal minus zwölf ist nicht minus vierzehn.'}),
         klick('Frage 5', 'x² + 3x − 10 = 0: Tipp die negative Lösung auf der x-Achse an.',
               [-5, 0], 'Getroffen: x = −5.',
               [{'bei': [5, 0], 'text': 'Prüf 5: 25 + 15 − 10 ist nicht 0. Achte auf das Vorzeichen.',
                 'sprich': 'Prüf fünf: fünfundzwanzig plus fünfzehn minus zehn ist nicht null. Achte auf das Vorzeichen.'},
                {'bei': [2, 0], 'text': 'Das ist die positive Lösung.',
                 'sprich': 'Das ist die positive Lösung.'},
                {'bei': [-2, 0], 'text': 'Prüf −2: 4 − 6 − 10 ist nicht 0.',
                 'sprich': 'Prüf minus zwei: vier minus sechs minus zehn ist nicht null.'}],
               NICHT_GANZ,
               sprich='x Quadrat plus drei x minus zehn gleich null: Tipp die negative Lösung auf der x-Achse an.',
               falsch_sprich=NICHT_GANZ),
     ], art='Kontrollclip', folge=4)

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
WF = fenster(-2, 11, -2, 11, (), ())
WE = fenster(-10, 4, -28, 28, (-8, -6, -4, -2, 2), (-20, -10, 10, 20))
WB = fenster(-2, 5, -7, 7, (-1, 1, 2, 3, 4), (-6, -4, -2, 2, 4, 6))
WD = fenster(-1, 7, -5, 7, (1, 2, 3, 4, 5, 6), (-4, -2, 2, 4, 6))
UM = [3.5, 0.5]          # Drehpunkt: die rechte Hälfte des Rechtecks landet auf dem Quadrat
fl = [
    {'art': 'vieleck', 'punkte': [[0, 0], [4, 0], [4, 4], [0, 4]], 'farbe': 1, 'fuellung': 0.15, 'ein': '~Quadrat mit'},
    {'art': 'text', 'bei': [2, 2], 'text': 'x²', 'farbe': 1, 'groesse': 40, 'ein': '~Quadrat mit'},
    {'art': 'text', 'bei': [2, -0.75], 'text': 'x', 'farbe': 1, 'groesse': 36, 'ein': '~Quadrat mit'},
    {'art': 'text', 'bei': [-0.7, 2], 'text': 'x', 'farbe': 1, 'groesse': 36, 'ein': '~Quadrat mit'},
    {'art': 'vieleck', 'punkte': [[4, 0], [7, 0], [7, 4], [4, 4]], 'farbe': 2, 'fuellung': 0.15, 'ein': '~Rechteck aus'},
    {'art': 'text', 'bei': [5.5, 2], 'text': '3x', 'farbe': 2, 'groesse': 36, 'ein': '~Halbiert'},
    {'art': 'text', 'bei': [5.5, -0.75], 'text': '3', 'farbe': 2, 'groesse': 36, 'kursiv': False, 'ein': '~Halbiert'},
    {'art': 'vieleck', 'punkte': [[7, 0], [10, 0], [10, 4], [7, 4]], 'farbe': 2, 'fuellung': 0.15, 'ein': '~Rechteck aus',
     'um': UM, 'drehung': 0, 'bewegung': [['~legt', {'drehung': 0}], ['~legt+2.6', {'drehung': 90}]]},
    {'art': 'text', 'bei': [8.5, 2], 'text': '3x', 'farbe': 2, 'groesse': 36, 'ein': '~Halbiert',
     'um': UM, 'drehung': 0, 'bewegung': [['~legt', {'drehung': 0}], ['~legt+2.6', {'drehung': 90}]]},
    {'art': 'text', 'bei': [8.5, 4.7], 'text': '3', 'farbe': 2, 'groesse': 36, 'kursiv': False, 'ein': '~Halbiert',
     'um': UM, 'drehung': 0, 'bewegung': [['~legt', {'drehung': 0}], ['~legt+2.6', {'drehung': 90}]]},
    {'art': 'text', 'bei': [7, -0.75], 'text': '6', 'farbe': 2, 'groesse': 36, 'kursiv': False, 'ein': '~Rechteck aus', 'aus': '~Halbiert'},
    {'art': 'text', 'bei': [10.5, 2], 'text': 'x', 'farbe': 2, 'groesse': 36, 'ein': '~Rechteck aus', 'aus': '~Halbiert'},
    {'art': 'vieleck', 'punkte': [[4, 4], [7, 4], [7, 7], [4, 7]], 'farbe': 3, 'fuellung': 0.0, 'gestrichelt': True, 'ein': '~Ecke'},
    {'art': 'vieleck', 'punkte': [[4, 4], [7, 4], [7, 7], [4, 7]], 'farbe': 3, 'fuellung': 0.3, 'ein': '~also'},
    {'art': 'text', 'bei': [5.5, 5.5], 'text': '9', 'farbe': 3, 'groesse': 40, 'kursiv': False, 'ein': '~also'},
]
clip('formel', 'Quadratische Gleichungen lösen: quadratisch ergänzen und Mitternachtsformel',
     'Die fehlende Ecke (6/2)² als Fläche, die quadratische Ergänzung an x² + 6x − 16 = 0, die Herleitung der '
     'Mitternachtsformel, ein Beispiel und was die Diskriminante über die Anzahl der Lösungen sagt.',
     ['quadratische Ergänzung', 'Mitternachtsformel', 'Diskriminante', 'Herleitung'], [
         sz('Die fehlende Ecke',
            'Ergänzen heisst: ein Quadrat vollständig machen. x Quadrat plus sechs x als Fläche: ein Quadrat mit der Seite x, '
            'dazu ein Rechteck aus sechs mal x. Halbiert man das Rechteck und legt die Hälften an zwei Seiten, fehlt zum '
            'grossen Quadrat nur die Ecke: drei mal drei, also neun.',
            f(r'x^2 + 6x', 300, 60, ein='~als Fläche'),
            f(r'x^2 + 6x + \fc{9} = (x + 3)^2', 430, 56, ein='~also'),
            graf(WF, achsen=False, raster=False, tippbar=False, pfeile=False, figuren=fl, ein=0.3)),
         sz('Ergänzen',
            'So löst man x Quadrat plus sechs x minus sechzehn gleich null. Plus sechzehn: x Quadrat plus sechs x gleich '
            'sechzehn. Die Ecke neun auf beiden Seiten addieren: Klammer x plus drei, im Quadrat, gleich fünfundzwanzig. '
            'Wurzel ziehen: x plus drei ist fünf oder minus fünf. Also ist x gleich zwei oder minus acht.',
            f(r'x^2 + 6x - 16 = 0', 240, 50, ein=0.3),
            op('+16', 240, '~Plus sechzehn'),
            f(r'x^2 + 6x = 16', 325, 50, ein='~Plus sechzehn+0.9'),
            op('+9', 325, '~Ecke'),
            f(r'(x + 3)^2 = 25', 410, 50, ein='~Klammer'),
            f(r'x + 3 = \pm 5', 495, 50, ein='~Wurzel'),
            f(r'\mathbb{L} = \{\fc{-8};\ \fc{2}\}', 600, 52, ein='~Also'),
            # Bild rechnet mit: Parabel und rechte Seite (zuerst y = 0) steigen gleich viel, +16 und +9; die
            # Schnittstellen bleiben −8 und 2, am Schluss (x + 3)² und y = 25.
            graf(WE, parabeln=[par(1, -3, -25, null=False, bew=[[0, 1, -3, -25], ['~Plus sechzehn', 1, -3, -25], ['~Plus sechzehn+1.0', 1, -3, -9],
                                                                ['~beiden', 1, -3, -9], ['~beiden+1.0', 1, -3, 0]])],
                 geraden=[{'bewegung': [[0, 0, 0], ['~Plus sechzehn', 0, 0], ['~Plus sechzehn+1.0', 0, 16], ['~beiden', 0, 16], ['~beiden+1.0', 0, 25]],
                           'farbe': 2, 'gestrichelt': True, 'dicke': 3}], ein=0.3),
            auflage(WE, '~Also', punkte=[pt(-8, 25, 3, '(−8 | 25)', [-7.7, 21.5]), pt(2, 25, 3, '(2 | 25)', [1.7, 21.5], 'end')])),
         sz('Herleitung',
            'Allgemein geht es genauso. Durch a teilen und c durch a hinüberbringen. Dann das Quadrat der halben Zahl vor x '
            'ergänzen. Links steht ein Quadrat, rechts b Quadrat minus vier a c, durch vier a Quadrat. Wurzel ziehen und '
            'auflösen.',
            f(r'a x^2 + b x + c = 0 \quad (a \neq 0)', 230, 46, ein=0.3),
            f(r'x^2 + \tfrac{b}{a}\,x = -\tfrac{c}{a}', 320, 46, ein='~Durch'),
            op(r'+\left(\tfrac{b}{2a}\right)^2', 320, '~Quadrat der', g=42),
            f(r'\left(x + \tfrac{b}{2a}\right)^2 = \dfrac{b^2 - 4ac}{4a^2}', 430, 46, ein='~Links'),
            f(r'x + \tfrac{b}{2a} = \pm\dfrac{\sqrt{b^2 - 4ac}}{2a}', 560, 46, ein='~Wurzel')),
         sz('Die Formel',
            'Das ist die Mitternachtsformel. Sie gilt für jede quadratische Gleichung mit a ungleich null. Unter der Wurzel '
            'steht die Diskriminante D gleich b Quadrat minus vier a c. Ist D negativ, gibt es keine Lösung.',
            f(r'x_{1,2} = \dfrac{-b \pm \sqrt{D}}{2a}', 300, 62, ein='~Mitternachtsformel'),
            f(r'D = b^2 - 4ac', 480, 58, ein='~Diskriminante'),
            n('@D \\lt 0@: keine Lösung', 590, 'blau', 46, ein='~Ist D')),
         sz('Beispiel',
            'Zum Beispiel zwei x Quadrat minus fünf x minus drei gleich null. a ist zwei, b minus fünf, c minus drei. '
            'D ist fünfundzwanzig plus vierundzwanzig, also neunundvierzig. x ist fünf plus oder minus sieben, durch vier. '
            'Die Lösungen sind drei und minus null Komma fünf.',
            f(r'2x^2 - 5x - 3 = 0', 240, 50, ein=0.3),
            f(r'a = 2,\ b = -5,\ c = -3', 325, 46, ein='~ist zwei'),
            f(r'D = 25 + 24 = 49', 410, 48, ein='~D ist'),
            f(r'x_{1,2} = \dfrac{5 \pm 7}{4}', 515, 50, ein='~x ist'),
            f(r'\mathbb{L} = \{\fc{-0.5};\ \fc{3}\}', 650, 50, ein='~Die Lösungen'),
            graf(WB, parabeln=[par(2, 1.25, -6.125)], ein='~Die Lösungen')),
         sz('Was D verrät',
            'Die Diskriminante zählt die Lösungen. Bei x Quadrat minus sechs x plus c: Für c gleich fünf ist D sechzehn, '
            'positiv: zwei Lösungen. Für c gleich neun ist D null: eine Lösung. Für c gleich zehn ist D negativ: keine.',
            f(r'x^2 - 6x + \fb{c} = 0', 240, 50, ein=0.3),
            n('@c = 5@: @D = 16 \\gt 0@, zwei Lösungen', 350, 'blau', 42, ein='~positiv'),
            n('@c = 9@: @D = 0@, eine Lösung', 440, 'blau', 42, ein='~eine Lösung'),
            n('@c = 10@: @D = -4 \\lt 0@, keine', 530, 'blau', 42, ein='~keine'),
            # c läuft mit dem Satz: 5 → 9 → 10, die Parabel y = (x − 3)² + c − 9 hebt sich; die Nullstellen rücken
            # zusammen, berühren und verschwinden.
            graf(WD, parabeln=[par(1, 3, -4, beschr=False,
                                   bew=[[0, 1, 3, -4], ['~Für c#2', 1, 3, -4], ['~Für c#2+1.2', 1, 3, 0], ['~Für c#3', 1, 3, 0],
                                        ['~Für c#3+1.2', 1, 3, 1]])], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Die quadratische Ergänzung macht aus jeder quadratischen Gleichung ein Quadrat. Allgemein ergibt '
            'das die Mitternachtsformel. Und D sagt, wie viele Lösungen es gibt.',
            titel('Zum Mitnehmen', 240, 76),
            f(r'x_{1,2} = \dfrac{-b \pm \sqrt{D}}{2a}, \quad D = b^2 - 4ac', 400, 50, ein='~Mitternachtsformel'),
            n('@D \\gt 0@: zwei; @D = 0@: eine; @D \\lt 0@: keine Lösung', 560, 'blau', 44, ein='~sagt')),
         JETZT_DU,
     ], folge=5)

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W3k = fenster(-5, 6, -3, 8, (-4, -3, -2, -1, 1, 2, 3, 4, 5), (-2, 2, 4, 6))
clip('kontrolle-formel', 'Quadratische Gleichungen lösen: Kontrollfragen zu Ergänzung und Formel',
     'Fünf Fragen: die Ergänzung zu x² + 8x, die Lösungen von (x − 3)² = 16, D und die Lösungen von 2x² − 3x − 5 = 0 '
     'und die kleinere Lösung von x² − 6x + 8 = 0.',
     ['quadratische Ergänzung', 'Mitternachtsformel', 'Diskriminante', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Hälfte von acht ist vier, im Quadrat sechzehn. x Quadrat plus acht x plus sechzehn ist Klammer x plus vier, im Quadrat.',
            f(r'\left(\tfrac{8}{2}\right)^2 = 16', 300, 56, ein='~Hälfte'),
            f(r'x^2 + 8x + 16 = (x + 4)^2', 420, 52, ein='~ist Klammer')),
         sz('Frage 2',
            'Die Klammer ist vier oder minus vier. Also ist x gleich sieben oder minus eins.',
            f(r'x - 3 = \pm 4', 300, 58, ein='~Die Klammer'),
            f(r'\mathbb{L} = \{-1;\ 7\}', 420, 56, ein='~Also')),
         sz('Frage 3',
            'b Quadrat ist neun. Minus vier mal zwei mal minus fünf ist plus vierzig. D ist neunundvierzig.',
            f(r'D = (-3)^2 - 4 \cdot 2 \cdot (-5)', 300, 50, ein='~Quadrat'),
            f(r'D = 9 + 40 = 49', 420, 54, ein='~D ist')),
         sz('Frage 4',
            'Vorne steht minus b, also drei. x ist drei plus oder minus sieben, durch vier. Die Lösungen sind zwei Komma fünf und minus eins.',
            f(r'x_{1,2} = \dfrac{3 \pm 7}{4}', 300, 56, ein='~Vorne'),
            f(r'\mathbb{L} = \{-1;\ 2.5\}', 450, 56, ein='~Die Lösungen')),
         sz('Frage 5',
            'D ist sechsunddreissig minus zweiunddreissig, also vier. x ist sechs plus oder minus zwei, durch zwei: vier oder '
            'zwei. Die kleinere Lösung ist zwei.',
            f(r'D = 36 - 32 = 4', 290, 52, ein='~D ist'),
            f(r'x_{1,2} = \dfrac{6 \pm 2}{2}', 390, 54, ein='~x ist'),
            f(r'x = \fc{2}' + ODER + r'x = \fc{4}', 530, 50, ein='~kleinere'),
            graf(W3k, ein=0.05),
            auflage(W3k, '~x ist', parabeln=[par(1, 3, -1)])),
         sz('Merke',
            'Zum Mitnehmen: Ergänzt wird das Quadrat der halben Zahl vor x. In der Formel steht vorne minus b und unten zwei a. '
            'Bei negativem c wird minus vier a c positiv.',
            titel('Zum Mitnehmen', 250, 76),
            n('@x^2 + px@: ergänzen mit @\\left(\\tfrac{p}{2}\\right)^2@|vorne @-b@, unten @2a@|@c \\lt 0@: @-4ac \\gt 0@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'x² + 8x: Welche Zahl ergänzt zum vollständigen Quadrat?',
              ['16', '64', '8'], 0,
              {0: 'Ja.',
               1: 'Nimm zuerst die Hälfte von 8, dann ins Quadrat.',
               2: 'Ergänzt wird ein Quadrat: die Hälfte von 8, im Quadrat.'},
              sprich='x Quadrat plus acht x: Welche Zahl ergänzt zum vollständigen Quadrat?',
              rueck_sprich={1: 'Nimm zuerst die Hälfte von acht, dann ins Quadrat.',
                            2: 'Ergänzt wird ein Quadrat: die Hälfte von acht, im Quadrat.'}),
         wahl('Frage 2', 'Nach dem Ergänzen steht (x − 3)² = 16. Welche Lösungsmenge?',
              ['{−1; 7}', '{7}', '{−7; 1}'], 0,
              {0: 'Ja.',
               1: 'Die Klammer kann auch −4 sein.',
               2: 'Prüf x = 1: (1 − 3)² ist 4, nicht 16.'},
              sprich='Nach dem Ergänzen steht Klammer x minus drei, im Quadrat, gleich sechzehn. Welche Lösungsmenge?',
              rueck_sprich={1: 'Die Klammer kann auch minus vier sein.',
                            2: 'Prüf x gleich eins. Minus zwei im Quadrat ist vier, nicht sechzehn.'}),
         wahl('Frage 3', '2x² − 3x − 5 = 0: Wie gross ist D?',
              ['49', '−31', '31'], 0,
              {0: 'Ja.',
               1: '−4 · 2 · (−5) ist positiv.',
               2: '(−3)² ist +9, nicht −9.'},
              sprich='Zwei x Quadrat minus drei x minus fünf gleich null: Wie gross ist D?',
              rueck_sprich={1: 'Minus vier mal zwei mal minus fünf ist positiv.',
                            2: 'Minus drei im Quadrat ist plus neun, nicht minus neun.'}),
         wahl('Frage 4', 'Mit D = 49: Welche Lösungen hat 2x² − 3x − 5 = 0?',
              ['{−1; 2.5}', '{−2.5; 1}', '{−2; 5}'], 0,
              {0: 'Ja.',
               1: 'Vorne steht −b, und b ist −3.',
               2: 'Der Nenner ist 2a, also 4.'},
              sprich='Mit D gleich neunundvierzig: Welche Lösungen hat zwei x Quadrat minus drei x minus fünf gleich null?',
              rueck_sprich={1: 'Vorne steht minus b, und b ist minus drei.',
                            2: 'Der Nenner ist zwei a, also vier.'}),
         klick('Frage 5', 'x² − 6x + 8 = 0: Tipp die kleinere Lösung auf der x-Achse an.',
               [2, 0], 'Getroffen: x = 2.',
               [{'bei': [4, 0], 'text': 'Das ist die grössere Lösung.',
                 'sprich': 'Das ist die grössere Lösung.'},
                {'bei': [-2, 0], 'text': 'Vorzeichen: Vorne steht −b, und b ist −6.',
                 'sprich': 'Vorzeichen. Vorne steht minus b, und b ist minus sechs.'},
                {'bei': [-4, 0], 'text': 'Vorzeichen: Vorne steht −b, und b ist −6.',
                 'sprich': 'Vorzeichen. Vorne steht minus b, und b ist minus sechs.'}],
               NICHT_GANZ,
               sprich='x Quadrat minus sechs x plus acht gleich null: Tipp die kleinere Lösung auf der x-Achse an.',
               falsch_sprich=NICHT_GANZ),
     ], art='Kontrollclip', folge=6)

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
W4a = fenster(-6, 4, -2, 20, (-5, -4, -3, -2, -1, 1, 2, 3), (4, 8, 12, 16))
W4b = fenster(-1, 7, -2, 6, (1, 2, 3, 4, 5, 6), (-1, 2, 4))
W4c = fenster(-8, 4, -6, 16, (-7, -6, -5, -4, -3, -2, -1, 1, 2, 3), (-4, 4, 8, 12))
clip('verfahren', 'Quadratische Gleichungen lösen: das passende Verfahren',
     'Erst ordnen und den Typ bestimmen, dann wählen: Wurzel ziehen, ausklammern, faktorisieren oder die '
     'Mitternachtsformel — und am Schluss mit dem Satz von Vieta kontrollieren.',
     ['quadratische Gleichung', 'Verfahrenswahl', 'Typ', 'Vieta', 'Probe'], [
         sz('Erst ordnen',
            'Bevor du ein Verfahren wählst: ausmultiplizieren und alles auf eine Seite. Erst dann siehst du den Typ. '
            'Klammer x minus eins, im Quadrat, gleich x Quadrat plus sieben. Ausmultipliziert heben sich die x Quadrat weg. '
            'Es bleibt minus zwei x plus eins gleich sieben, eine lineare Gleichung. x ist minus drei.',
            f(r'(x - 1)^2 = x^2 + 7', 250, 50, ein=0.3),
            f(r'x^2 - 2x + 1 = x^2 + 7', 340, 46, ein='~Ausmultipliziert'),
            op('-x^2', 340, '~heben', g=44),
            f(r'-2x + 1 = 7', 430, 50, ein='~Es bleibt'),
            f(r'x = \fc{-3}', 520, 50, ein='~ist minus'),
            # «heben sich die x Quadrat weg»: auf beiden Seiten verschwindet das x² stetig (Normalform, a 1 → 0);
            # in jedem Zwischenstand (1 − s)x² − 2x + 1 = (1 − s)x² + 7 bleibt der Schnitt bei x = −3.
            graf(W4a, parabeln=[{'normalform': True, 'farbe': 1, 'bewegung': [[0, 1, -2, 1], ['~heben', 1, -2, 1], ['~heben+1.6', 0, -2, 1]]},
                                {'normalform': True, 'farbe': 2, 'bewegung': [[0, 1, 0, 7], ['~heben', 1, 0, 7], ['~heben+1.6', 0, 0, 7]]}], ein=0.3),
            auflage(W4a, '~ist minus', punkte=[pt(-3, 7, 3, '(−3 | 7)', [-3.3, 5.6], 'end')])),
         sz('Die Form entscheidet',
            'Steht rechts null, entscheidet die Form. Fehlt b, zieh die Wurzel. Fehlt c, klammere aus. Hat die Normalform zwei '
            'ganzzahlige Lösungen, die du über Produkt und Summe findest, faktorisiere. Sonst nimm die Mitternachtsformel. Sie '
            'geht immer; ist D negativ, zeigt sie, dass es keine Lösung gibt.',
            f(r'3x^2 - 48 = 0', 260, 48, ein='~Fehlt b'),
            f(r'\to\ \text{Wurzel ziehen}', 260, 44, ein='~Fehlt b+0.8', x=640),
            f(r'x^2 + 9x = 0', 360, 48, ein='~Fehlt c'),
            f(r'\to\ \text{ausklammern}', 360, 44, ein='~Fehlt c+0.8', x=640),
            f(r'x^2 - 8x + 15 = 0', 460, 48, ein='~Hat die'),
            f(r'\to\ \text{faktorisieren}', 460, 44, ein='~faktorisiere', x=640),
            f(r'3x^2 + 2x - 2 = 0', 560, 48, ein='~Sonst'),
            f(r'\to\ \text{Formel}', 560, 44, ein='~Mitternachtsformel', x=640),
            n('Die Formel geht immer — bei @D \\lt 0@ zeigt sie: keine Lösung.', 680, 'blau', 42, ein='~geht')),
         sz('Kontrolle',
            'Kontrolliere am Schluss. Bei x Quadrat minus acht x plus fünfzehn sind die Lösungen drei und fünf. Summe acht, '
            'das ist minus p. Produkt fünfzehn, das ist q. Beides stimmt. Das ist der Satz von Vieta.',
            f(r'x^2 - 8x + 15 = (x - 3)(x - 5)', 260, 48, ein=0.3),
            n('@3 + 5 = 8 = -p@ ✓', 380, 'blau', 46, ein='~Summe'),
            n('@3 \\cdot 5 = 15 = q@ ✓', 470, 'blau', 46, ein='~Produkt'),
            graf(W4b, parabeln=[par(1, 4, -1)], ein=0.3)),
         sz('Erst auf null',
            'Und nie ein Verfahren, bevor rechts null steht. x mal Klammer x plus vier gleich zwölf ist kein Nullprodukt. '
            'Ausmultiplizieren und minus zwölf: x Quadrat plus vier x minus zwölf gleich null. Faktorisiert: Klammer x plus '
            'sechs mal Klammer x minus zwei. Die Lösungen sind minus sechs und zwei.',
            f(r'x(x + 4) = 12', 250, 50, ein=0.3),
            n('kein Nullprodukt: rechts steht @12@', 340, 'rot', 42, ein='~kein'),
            f(r'x^2 + 4x - 12 = 0', 430, 50, ein='~Ausmultiplizieren'),
            f(r'(x + 6)(x - 2) = 0', 520, 50, ein='~Faktorisiert'),
            f(r'\mathbb{L} = \{\fc{-6};\ \fc{2}\}', 620, 50, ein='~Die Lösungen'),
            graf(W4c, parabeln=[par(1, -2, -4, null=False)], kurven=[dict(formel='12', farbe=2, gestrichelt=True, dicke=3)], ein=0.3),
            auflage(W4c, '~Die Lösungen', punkte=[pt(-6, 12, 3, '(−6 | 12)', [-5.7, 13.6]), pt(2, 12, 3, '(2 | 12)', [1.7, 13.6], 'end')])),
         sz('Merke',
            'Zum Mitnehmen: Ordnen, den Typ bestimmen, dann das kürzeste passende Verfahren. Am Schluss die Probe oder Vieta.',
            titel('Zum Mitnehmen', 240, 76),
            n('ordnen, Typ bestimmen|@b = 0@: Wurzel; @c = 0@: ausklammern|zerlegbar: faktorisieren; sonst: Formel|Probe oder Vieta',
              380, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ], folge=7)

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
W4k = fenster(-5, 6, -10, 8, (-4, -3, -2, -1, 1, 2, 3, 4, 5), (-8, -4, 4))
clip('kontrolle-verfahren', 'Quadratische Gleichungen lösen: Kontrollfragen zur Verfahrenswahl',
     'Fünf Fragen: welches Verfahren wann, der Typ nach dem Ordnen, eine Kontrolle mit Vieta und x(x − 2) = 8.',
     ['Verfahrenswahl', 'Typ', 'Vieta', 'Kontrollfragen'], [
         sz('Frage 1',
            'Es fehlt das lineare Glied. Plus zwanzig, durch fünf: x Quadrat gleich vier, x gleich plus oder minus zwei.',
            f(r'5x^2 = 20 \;\Rightarrow\; x^2 = 4', 300, 54, ein='~Plus'),
            f(r'x = \pm 2', 420, 56, ein='~plus oder')),
         sz('Frage 2',
            'Alle drei Glieder sind da, vor x Quadrat steht drei. D ist sechzehn plus vierundzwanzig, also vierzig, keine '
            'Quadratzahl. Die Formel ist der sichere Weg.',
            f(r'D = 16 + 24 = 40', 300, 54, ein='~D ist'),
            n('keine Quadratzahl: Formel', 420, 'blau', 44, ein='~keine')),
         sz('Frage 3',
            'Ausmultipliziert: x Quadrat minus acht x plus sechzehn gleich x Quadrat plus acht. Die x Quadrat heben sich weg: '
            'minus acht x gleich minus acht, also x gleich eins.',
            f(r'x^2 - 8x + 16 = x^2 + 8', 300, 50, ein='~Ausmultipliziert'),
            f(r'-8x = -8 \;\Rightarrow\; x = 1', 420, 54, ein='~heben')),
         sz('Frage 4',
            'Drei plus minus sieben ist minus vier, das ist minus p. Drei mal minus sieben ist minus einundzwanzig, das ist q. '
            'Beide stimmen.',
            n('@3 + (-7) = -4 = -p@ ✓', 300, 'blau', 46, ein='~Drei plus'),
            n('@3 \\cdot (-7) = -21 = q@ ✓', 400, 'blau', 46, ein='~Drei mal')),
         sz('Frage 5',
            'Erst auf null: x Quadrat minus zwei x minus acht gleich null. Klammer x minus vier mal Klammer x plus zwei. '
            'Die positive Lösung ist vier.',
            f(r'x^2 - 2x - 8 = 0', 290, 52, ein='~Erst'),
            f(r'(x - 4)(x + 2) = 0', 400, 52, ein='~Klammer'),
            f(r'x = \fc{4}' + ODER + r'x = \fc{-2}', 510, 50, ein='~positive'),
            graf(W4k, ein=0.05),
            auflage(W4k, '~Klammer', parabeln=[par(1, 1, -9)])),
         sz('Merke',
            'Zum Mitnehmen: Zuerst ordnen, dann wählen. Die Formel geht immer, bei negativem D zeigt sie: keine Lösung. '
            'Die Probe oder Vieta zeigen, ob es stimmt.',
            titel('Zum Mitnehmen', 250, 76),
            n('ordnen|kürzestes passendes Verfahren|Probe oder Vieta', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', '5x² − 20 = 0: Welches Verfahren ist am schnellsten?',
              ['Wurzelziehen', 'Mitternachtsformel', 'Zweiklammersatz'], 0,
              {0: 'Ja.',
               1: 'Geht, aber es fehlt das lineare Glied. Was ist kürzer?',
               2: 'Vor x² steht 5, und es fehlt das lineare Glied. Was ist kürzer?'},
              sprich='Fünf x Quadrat minus zwanzig gleich null: Welches Verfahren ist am schnellsten?',
              rueck_sprich={1: 'Geht, aber es fehlt das lineare Glied. Was ist kürzer?',
                            2: 'Vor x Quadrat steht fünf, und es fehlt das lineare Glied. Was ist kürzer?'}),
         wahl('Frage 2', '3x² + 4x − 2 = 0: Welches Verfahren passt?',
              ['Mitternachtsformel', 'Zweiklammersatz', 'Ausklammern'], 0,
              {0: 'Ja.',
               1: 'Der Zweiklammersatz braucht 1 vor x² und schöne Lösungen. Hier steht 3.',
               2: 'Hier steht eine Zahl ohne x: −2.'},
              sprich='Drei x Quadrat plus vier x minus zwei gleich null: Welches Verfahren passt?',
              rueck_sprich={1: 'Der Zweiklammersatz braucht eins vor x Quadrat und schöne Lösungen. Hier steht drei.',
                            2: 'Hier steht eine Zahl ohne x: minus zwei.'}),
         wahl('Frage 3', '(x − 4)² = x² + 8: Was für eine Gleichung bleibt nach dem Ordnen?',
              ['eine lineare, mit x = 1', 'eine quadratische', 'eine lineare, mit x = −1'], 0,
              {0: 'Ja.',
               1: 'Multipliziere links aus. Was geschieht mit x²?',
               2: 'Multipliziere aus und ordne. Setz dann deine Lösung in die Gleichung ein.'},
              sprich='Klammer x minus vier, im Quadrat, gleich x Quadrat plus acht: Was für eine Gleichung bleibt nach dem Ordnen?',
              rueck_sprich={1: 'Multipliziere links aus. Was geschieht mit x Quadrat?',
                            2: 'Multipliziere aus und ordne. Setz dann deine Lösung in die Gleichung ein.'}),
         wahl('Frage 4', 'Sind 3 und −7 die Lösungen von x² + 4x − 21 = 0?',
              ['Ja: Summe −4, Produkt −21', 'Nein: Die Summe müsste 4 sein.', 'Nein: Das Produkt müsste 21 sein.'], 0,
              {0: 'Ja.',
               1: 'Nach Vieta ist die Summe −p. Was ist p?',
               2: 'Nach Vieta ist das Produkt q. Was ist q?'},
              sprich='Sind drei und minus sieben die Lösungen von x Quadrat plus vier x minus einundzwanzig gleich null?',
              rueck_sprich={1: 'Nach Vieta ist die Summe minus p. Was ist p?',
                            2: 'Nach Vieta ist das Produkt q. Was ist q?'}),
         klick('Frage 5', 'x(x − 2) = 8: Tipp die positive Lösung auf der x-Achse an.',
               [4, 0], 'Getroffen: x = 4.',
               [{'bei': [2, 0], 'text': 'Prüf 2: 2 · 0 ist 0, nicht 8.',
                 'sprich': 'Prüf zwei: zwei mal null ist null, nicht acht.'},
                {'bei': [-2, 0], 'text': 'Das ist die negative Lösung.',
                 'sprich': 'Das ist die negative Lösung.'},
                {'bei': [-4, 0], 'text': 'Prüf −4: (−4) · (−6) ist 24, nicht 8.',
                 'sprich': 'Prüf minus vier: minus vier mal minus sechs ist vierundzwanzig, nicht acht.'}],
               NICHT_GANZ,
               sprich='x mal Klammer x minus zwei gleich acht: Tipp die positive Lösung auf der x-Achse an.',
               falsch_sprich=NICHT_GANZ),
     ], art='Kontrollclip', folge=8)

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
W5b = fenster(-1, 7, -5, 8, (1, 2, 3, 4, 5, 6), (-4, -2, 2, 4, 6))
W5k = fenster(-5, 5, -4, 10, (-4, -3, -2, -1, 1, 2, 3, 4), (-2, 2, 4, 6, 8))
W5c = fenster(-4, 5, -8, 4, (-3, -2, -1, 1, 2, 3, 4), (-6, -4, -2, 2))
clip('parameter', 'Quadratische Gleichungen lösen: Parameterdiskussion',
     'x² − 6x + k = 0 mit D(k) = 36 − 4k; x² + kx + 4 = 0 mit zwei kritischen Werten; und warum man bei m x² − 4x − 3 = 0 '
     'zuerst prüft, ob der Faktor vor x² null werden kann.',
     ['Parameter', 'Parameterdiskussion', 'Diskriminante', 'Lösungsfälle'], [
         sz('Ein Parameter',
            'In einer Parametergleichung steht neben x ein zweiter Buchstabe, hier k. Für welche k hat x Quadrat minus sechs x '
            'plus k gleich null zwei, eine oder keine Lösung? Die Diskriminante entscheidet.',
            titel('Parameter', 260, 80),
            f(r'x^2 - 6x + \fb{k} = 0', 400, 60, ein='~Für welche'),
            n('zwei, eine oder keine Lösung?', 520, 'blau', 46, ein='~zwei')),
         sz('D von k',
            'a ist eins, b minus sechs, c ist k. D von k ist sechsunddreissig minus vier k. Für k kleiner als neun ist D positiv: '
            'zwei Lösungen. Bei k gleich neun ist D null: eine Lösung, x gleich drei. Für k grösser als neun gibt es keine.',
            f(r'x^2 - 6x + \fb{k} = 0', 240, 50, ein=0.3),
            f(r'D(k) = 36 - 4k', 340, 52, ein='~D von'),
            n('@k \\lt 9@: zwei Lösungen', 440, 'blau', 42, ein='~kleiner'),
            n('@k = 9@: eine, @x = 3@', 520, 'blau', 42, ein='~Bei k'),
            n('@k \\gt 9@: keine', 600, 'blau', 42, ein='~grösser'),
            f(r'\fb{k = 5}', 690, 46, ein=0.3),
            f(r'\to\ \fb{k = 8}', 690, 46, ein='~kleiner', x=300),
            f(r'\to\ \fb{k = 9}', 690, 46, ein='~Bei k', x=528),
            f(r'\to\ \fb{k = 11}', 690, 46, ein='~grösser', x=756),
            # k läuft mit dem Satz: 5 → 8 (zwei Nullstellen rücken zusammen), → 9 (berührt), → 11 (abgehoben).
            graf(W5b, parabeln=[par(1, 3, -4, beschr=False,
                                    bew=[[0, 1, 3, -4], ['~kleiner', 1, 3, -4], ['~kleiner+1.5', 1, 3, -1], ['~Bei k', 1, 3, -1],
                                         ['~Bei k+1.2', 1, 3, 0], ['~grösser', 1, 3, 0], ['~grösser+1.2', 1, 3, 2]])], ein=0.3)),
         sz('Zwei kritische Werte',
            'Steht k vor x, wie bei x Quadrat plus k x plus vier, wird D zu k Quadrat minus sechzehn. D ist null bei k gleich vier '
            'und bei k gleich minus vier. Dazwischen ist D negativ: keine Lösung. Ausserhalb gibt es zwei.',
            f(r'x^2 + \fb{k}\,x + 4 = 0', 240, 52, ein=0.3),
            f(r'D(k) = k^2 - 16', 340, 52, ein='~wird D'),
            n('@D = 0@: @k = 4@ oder @k = -4@', 440, 'blau', 42, ein='~D ist null'),
            n('@-4 \\lt k \\lt 4@: keine Lösung', 520, 'blau', 42, ein='~Dazwischen'),
            n('@k \\lt -4@ oder @k \\gt 4@: zwei', 600, 'blau', 42, ein='~Ausserhalb'),
            f(r'\fb{k = 5}', 690, 46, ein=0.3),
            f(r'\to\ \fb{4}', 690, 46, ein='~D ist null', x=300),
            f(r'\to\ \fb{{-4}}', 690, 46, ein='~und bei', x=430),
            f(r'\to\ \fb{{-5}}', 690, 46, ein='~Ausserhalb', x=610),
            # k läuft: 5 (zwei), «D ist null bei k gleich vier» → 4 (berührt bei −2), «und bei k gleich minus vier» → −4
            # (berührt bei 2) über 0 (keine), «Ausserhalb» → −5 (zwei).
            graf(W5k, parabeln=[{'normalform': True, 'farbe': 1, 'nullstellen': {'farbe': 3, 'beschriftung': False},
                                 'bewegung': [[0, 1, 5, 4], ['~D ist null', 1, 5, 4], ['~D ist null+1.0', 1, 4, 4],
                                              ['~und bei', 1, 4, 4], ['~und bei+2.0', 1, -4, 4],
                                              ['~Ausserhalb', 1, -4, 4], ['~Ausserhalb+1.0', 1, -5, 4]]}], ein=0.3)),
         sz('Zuerst a prüfen',
            'Steht der Parameter vor x Quadrat, prüfe zuerst, ob er null sein kann. m x Quadrat minus vier x minus drei: '
            'Bei m gleich null ist die Gleichung linear, x ist minus drei Viertel. Erst für m ungleich null gilt die Diskriminante, '
            'sechzehn plus zwölf m. Sie ist null bei m gleich minus vier Drittel: eine Lösung. Für grössere m gibt es zwei, '
            'ausser bei m gleich null. Für kleinere m gibt es keine.',
            f(r'\fb{m}\,x^2 - 4x - 3 = 0', 250, 50, ein=0.3),
            f(r'm = 0: \;\; -4x - 3 = 0 \;\Rightarrow\; x = -\tfrac{3}{4}', 345, 44, ein='~Bei m'),
            f(r'm \neq 0: \;\; D(m) = 16 + 12m', 440, 44, ein='~Erst für'),
            n('@m = -\\tfrac{4}{3}@: eine; @m \\gt -\\tfrac{4}{3}@ (@m \\neq 0@): zwei|@m \\lt -\\tfrac{4}{3}@: keine', 540, 'blau', 40, ein='~Sie ist'),
            f(r'\fb{m = 1}', 690, 40, ein=0.3),
            f(r'\to\ \fb{0}', 690, 40, ein='~Bei m', x=300),
            f(r'\to\ \fb{{-\tfrac{4}{3}}}', 690, 40, ein='~Sie ist', x=420),
            f(r'\to\ \fb{{-1}}', 690, 40, ein='~grössere', x=600),
            f(r'\to\ \fb{{-2}}', 690, 40, ein='~kleinere', x=750),
            # m läuft stetig durch 0 (Normalform [t, a, b, c]): m = 1 (zwei Nullstellen 2 ± √7), «Bei m gleich null» → 0,
            # die Gerade −4x − 3 mit der Nullstelle −0.75; «Sie ist null bei m gleich minus vier Drittel» → −4/3, berührt bei
            # (−1.5 | 0); «grössere m … zwei» → −1 (Nullstellen −3, −1); «kleinere keine» → −2.
            graf(W5c, parabeln=[{'normalform': True, 'farbe': 1, 'nullstellen': {'farbe': 3, 'beschriftung': False},
                                 'bewegung': [[0, 1, -4, -3], ['~Bei m', 1, -4, -3], ['~Bei m+1.4', 0, -4, -3], ['~Sie ist', 0, -4, -3],
                                              ['~Sie ist+1.4', -4 / 3, -4, -3], ['~grössere', -4 / 3, -4, -3], ['~grössere+0.9', -1, -4, -3],
                                              ['~kleinere', -1, -4, -3], ['~kleinere+0.7', -2, -4, -3]]}],
                 punkte=[dict(pt(-0.75, 0, 3, '(−0.75 | 0)', [-1.15, 0.45], 'end'), ein='~linear+0.8', aus='~Erst für'),
                         dict(pt(-1.5, 0, 3, '(−1.5 | 0)', [-1.75, 0.45], 'end'), ein='~eine Lösung', aus='~grössere')],
                 ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: D in Abhängigkeit von k aufschreiben und die Werte suchen, bei denen D null ist. Steht der Parameter '
            'vor x Quadrat, zuerst prüfen, wann er null ist: Dann ist die Gleichung linear.',
            titel('Zum Mitnehmen', 250, 76),
            n('@D(k)@ aufschreiben, @D(k) = 0@ lösen|Parameter vor @x^2@: zuerst den Fall @0@ prüfen', 390, 'blau', 42, ein=1.2)),
         JETZT_DU_ANIM,
     ], folge=9)

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
W10a = fenster(-7, 2, -3, 8, (-6, -5, -4, -3, -2, -1, 1), (-2, 2, 4, 6))
W10b = fenster(-7, 7, -2, 12, (-6, -4, -2, 2, 4, 6), (3, 6, 9))
W10c = fenster(-5, 3, -6, 6, (-4, -3, -2, -1, 1, 2), (-4, -2, 2, 4))
clip('kontrolle-parameter', 'Quadratische Gleichungen lösen: Kontrollfragen zur Parameterdiskussion',
     'Fünf Fragen: D(k) bei x² + 6x + k = 0, der Wert mit genau einer Lösung, zwei kritische Werte bei x² + kx + 16 = 0, '
     'der Fall k = 0 und eine Gleichung, die immer zwei Lösungen hat.',
     ['Parameterdiskussion', 'Diskriminante', 'Kontrollfragen'], [
         sz('Frage 1',
            'a ist eins, b sechs, c ist k. D ist sechs im Quadrat minus vier mal eins mal k: sechsunddreissig minus vier k.',
            f(r'D = 6^2 - 4 \cdot 1 \cdot k = 36 - 4k', 300, 52, ein='~D ist')),
         sz('Frage 2',
            'Genau eine Lösung gibt es bei D gleich null: sechsunddreissig minus vier k gleich null, also k gleich neun. '
            'Dann ist x gleich minus drei.',
            f(r'36 - 4k = 0 \;\Rightarrow\; k = 9', 300, 54, ein='~bei D'),
            f(r'x^2 + 6x + 9 = (x + 3)^2', 420, 50, ein='~Dann'),
            graf(W10a, parabeln=[par(1, -3, 0)], ein='~Dann')),
         sz('Frage 3',
            'D ist k Quadrat minus vierundsechzig. Null wird es bei k gleich acht und bei k gleich minus acht.',
            f(r'D(k) = k^2 - 64', 300, 54, ein='~D ist'),
            f(r'k = 8 \;\text{oder}\; k = -8', 420, 54, ein='~Null'),
            graf(W10b, parabeln=[par(1, -4, 0, farbe=1), par(1, 4, 0, farbe=1)], ein='~Null'),
            auflage(W10b, '~Null', texte=[{'bei': [-4, 9.4], 'text': 'k = 8', 'farbe': 2, 'groesse': 30, 'anker': 'middle'},
                                          {'bei': [4, 9.4], 'text': 'k = −8', 'farbe': 2, 'groesse': 30, 'anker': 'middle'}])),
         sz('Frage 4',
            'Bei k gleich null fällt x Quadrat weg. Es bleibt minus vier x plus eins gleich null, eine lineare Gleichung mit '
            'x gleich null Komma zwei fünf.',
            f(r'k = 0: \quad -4x + 1 = 0', 300, 54, ein='~Es bleibt'),
            f(r'x = 0.25', 420, 56, ein='~lineare')),
         sz('Frage 5',
            'D ist vier plus vier k Quadrat. Das ist für jedes k positiv: Es gibt immer zwei Lösungen.',
            f(r'D = 4 + 4k^2 \gt 0', 300, 56, ein='~D ist'),
            n('für jedes @k@ zwei Lösungen', 420, 'blau', 46, ein='~immer'),
            # k läuft 0 → 1 → 2: Die Parabel y = x² + 2x − k² sinkt, hat aber immer zwei Nullstellen.
            graf(W10c, parabeln=[{'normalform': True, 'farbe': 1, 'nullstellen': {'farbe': 3, 'beschriftung': False},
                                  'bewegung': [[0, 1, 2, 0], ['~Das ist', 1, 2, 0], ['~Das ist+0.8', 1, 2, -1], ['~Es gibt', 1, 2, -1],
                                               ['~Es gibt+1.0', 1, 2, -4]]}], ein='~D ist')),
         sz('Merke',
            'Zum Mitnehmen: D von k gleich null setzen gibt die kritischen Werte. Steht k vor x Quadrat, zuerst den Fall '
            'k gleich null prüfen.',
            titel('Zum Mitnehmen', 250, 76),
            n('@D(k) = 0@: die kritischen Werte|Parameter vor @x^2@: zuerst @k = 0@ prüfen', 400, 'blau', 42, ein=1.2)),
     ], [
         wahl('Frage 1', 'x² + 6x + k = 0: Wie lautet D(k)?',
              ['36 − 4k', '36 − k', '6 − 4k'], 0,
              {0: 'Ja.',
               1: 'D = b² − 4ac. Was ist 4 · a · c?',
               2: 'b ist 6. Was ist b²?'},
              sprich='x Quadrat plus sechs x plus k gleich null: Wie lautet D von k?',
              rueck_sprich={1: 'D gleich b Quadrat minus vier a c. Was ist vier mal a mal c?',
                            2: 'b ist sechs. Was ist b Quadrat?'}),
         wahl('Frage 2', 'Für welches k hat x² + 6x + k = 0 genau eine Lösung?',
              ['k = 9', 'k = −9', 'k = 36'], 0,
              {0: 'Ja.',
               1: 'Rechne D(−9) = 36 + 36. Wie viele Lösungen sind das?',
               2: 'Rechne D(36) = 36 − 144. Wie viele Lösungen sind das?'},
              sprich='Für welches k hat x Quadrat plus sechs x plus k gleich null genau eine Lösung?',
              rueck_sprich={1: 'Rechne D von minus neun: sechsunddreissig plus sechsunddreissig. Wie viele Lösungen sind das?',
                            2: 'Rechne D von sechsunddreissig: sechsunddreissig minus hundertvierundvierzig. Wie viele Lösungen sind das?'}),
         wahl('Frage 3', 'x² + kx + 16 = 0: Für welche k gibt es genau eine Lösung?',
              ['k = 8 oder k = −8', 'nur k = 8', 'k = 4 oder k = −4'], 0,
              {0: 'Ja.',
               1: 'Auch (−8)² ist 64.',
               2: 'D = k² − 4 · 16. Wann ist das null?'},
              sprich='x Quadrat plus k x plus sechzehn gleich null: Für welche k gibt es genau eine Lösung?',
              rueck_sprich={1: 'Auch minus acht im Quadrat ist vierundsechzig.',
                            2: 'D gleich k Quadrat minus vier mal sechzehn. Wann ist das null?'}),
         wahl('Frage 4', 'k · x² − 4x + 1 = 0 bei k = 0: Was gilt?',
              ['linear, x = 0.25', 'D = 16 > 0, also zwei Lösungen', 'keine Lösung'], 0,
              {0: 'Ja.',
               1: 'D gehört zu quadratischen Gleichungen. Was bleibt bei k = 0 stehen?',
               2: 'Setz k = 0 ein. Was bleibt stehen?'},
              sprich='k mal x Quadrat minus vier x plus eins gleich null, bei k gleich null: Was gilt?',
              rueck_sprich={1: 'D gehört zu quadratischen Gleichungen. Was bleibt bei k gleich null stehen?',
                            2: 'Setz k gleich null ein. Was bleibt stehen?'}),
         wahl('Frage 5', 'x² + 2x − k² = 0: Wie viele Lösungen gibt es?',
              ['für jedes k zwei', 'für k = 0 nur eine', 'für grosse k keine'], 0,
              {0: 'Ja.',
               1: 'Rechne D bei k = 0: 4 − 0. Wie viele Lösungen sind das?',
               2: 'D = 4 + 4k². Kann das negativ werden?'},
              sprich='x Quadrat plus zwei x minus k Quadrat gleich null: Wie viele Lösungen gibt es?',
              rueck_sprich={1: 'Rechne D bei k gleich null: vier minus null. Wie viele Lösungen sind das?',
                            2: 'D gleich vier plus vier k Quadrat. Kann das negativ werden?'}),
     ], art='Kontrollclip', folge=10)

for w in WARNUNGEN:
    print('WARNUNG', w)
if not WZ:
    print('(keine wortzeiten.json — alle Anker geschätzt)')
