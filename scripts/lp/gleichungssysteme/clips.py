"""Erzeugt die zehn Drehbücher des Leitprogramms Lineare Gleichungssysteme (11.10.2026), Reihe «Gleichungssysteme lösen».

  python3 scripts/lp/gleichungssysteme/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich) und nennt am Schluss
die Szenen und Fragetöne mit neuem Text («NEU VERTONEN»). Einblendungen und Bewegungen stehen auf dem Wort, das sie
nennt: `ein: "@wort"` (auch «@wort#2», «@wort+0.3»), aufgelöst mit den gemessenen Wortzeiten aus wortzeiten.json
(wortzeiten.py, faster-whisper); ohne Messung geschätzt. Bausteine wie im Leitprogramm Modellieren (clips_basis.py dort).

Layout (1920 × 1080): Formeln und Notizen links (x 150), das Bild rechts (x 1010, y 175, 760 × 760), Achsen 1 : 1.
Kontrollclips: Der Fragekasten des Abspielers steht links ab y = 560. Beim Erscheinen der Frage (0.3 s) zeigt die Szene
nur das Gegebene (HOWTO-leitprogramme §15, Fragebild); die Auflösung kommt ab 1.0 s mit dem Satz, der sie nennt.
Angebote länger als 18 Zeichen stehen als A, B, C im Bild (abc), die Knöpfe heissen nur A, B, C.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Gleichung (I) und ihre Gerade          \\fa{…}
  2 orange = Gleichung (II) und ihre Gerade         \\fb{…}
  3 grün   = Lösung, Schnittpunkt, Hilfslinie x = 2  \\fc{…}
  4 rot    = Fehler, Widerspruch                    \\fd{…}
  5 Tinte  = neutral (Umformungsschritte, Läufer)
"""
import difflib
import importlib.util
import json
import os
import re
import zlib

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
PRAEFIX = 'g2-3-lp-'
LX, OX, GX, GY, GB, GH, RX = 150, 620, 1010, 175, 760, 760, 1000
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT, NEU_TON, NEU_FRAGEN = [], [], []
SPRECH = {}


# ---------------------------------------------------------------- Zeiten auf den Ton (wie modellieren/clips_basis.py)
ZAHLWORT = {'null': 0, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5, 'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9,
            'zehn': 10, 'elf': 11, 'zwölf': 12, 'dreizehn': 13, 'vierzehn': 14, 'achtzehn': 18, 'neunzehn': 19,
            'fünfunddreissig': 35, 'siebenundfünfzig': 57, 'dreimal': 3}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower())
    w_ = wort.lower()
    if not g:
        return False
    if w_ in ZAHLWORT:
        # Whisper schreibt Zahlwörter als Ziffern («2», «2x», «3k.», «-1»): die führende Zahl vergleichen
        m = re.match(r'^-?(\d+)', gehoert.strip())
        if m:
            return int(m.group(1)) == ZAHLWORT[w_]
    if w_.isdigit():
        return g == w_
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    return (len(w_) >= 5 and w_[0] == g[0] and abs(len(w_) - len(g)) <= 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.7)


def wann(clip, szene, wort, nr=1, dazu=0.0):
    w = WZ.get(clip, {}).get(szene)
    if w and w.get('sprecher') == SPRECH.get((clip, szene)):
        k = 0
        for wt, a, e in w['woerter']:
            if passt(wort, wt):
                k += 1
                if k == nr:
                    return round(max(1.0, a + dazu), 2)
    FEHLT.append((clip, szene, wort))
    text = SPRECH.get((clip, szene), '')
    if w and w.get('sprecher') == text and w['woerter']:
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
            return round(max(1.0, w['woerter'][j][1] + dazu), 2)
    pos, k = -1, 0
    for m in re.finditer(r'(?<!\w)' + re.escape(wort), text, re.I):
        k += 1
        if k == nr:
            pos = m.start()
            break
    d = len(text.split()) / 2.5 + 1.0
    return round(max(1.0, 0.4 + max(0, pos) / max(1, len(text)) * (d - 1.0) + dazu), 2)


def zeiten(clip, szenen):
    def lös(sname, v):
        if isinstance(v, str) and v.startswith('@'):
            m = re.match(r'@([^#+]+)(?:#(\d+))?(?:\+([\d.]+))?$', v)
            return wann(clip, sname, m.group(1), int(m.group(2) or 1), float(m.group(3) or 0))
        return v

    for q in szenen:
        SPRECH[(clip, q['name'])] = q['sprecher']
    for q in szenen:
        for el in q['elemente']:
            for z in ('ein', 'aus'):
                if z in el:
                    el[z] = lös(q['name'], el[z])
            for art in ('punkte', 'strecken', 'texte', 'geraden', 'flaechen'):
                for k in el.get(art) or []:
                    for z in ('ein', 'aus'):
                        if z in k:
                            k[z] = lös(q['name'], k[z])
                    if 'bewegung' in k:
                        k['bewegung'] = [[lös(q['name'], b[0])] + b[1:] for b in k['bewegung']]
                    b_ = k.get('laeufer')
                    if isinstance(b_, dict) and 'bahn' in b_:
                        b_['bahn'] = [[lös(q['name'], b[0])] + b[1:] for b in b_['bahn']]
                        for z in ('ein', 'aus'):
                            if z in b_:
                                b_[z] = lös(q['name'], b_[z])
        # Bewegungen: Stützpunkte müssen in der Zeit aufsteigen (geschätzte Anker können sich überholen)
        for el in q['elemente']:
            for k in el.get('geraden') or []:
                if 'bewegung' in k:
                    t = -1
                    for b in k['bewegung']:
                        b[0] = max(b[0], round(t + 0.3, 2)) if t >= 0 else b[0]
                        t = b[0]


# ---------------------------------------------------------------- Elemente
def f(t, y, g=52, ein=0.05, x=LX, **kw):
    d = dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)
    d.update(kw)
    return d


def op(t, y, ein, g=46):
    """Der Umformungsschritt rechts neben der Zeile, neutral (wie im Heft)."""
    return f(r'\mid ' + t, y, g, ein, OX)


def n(t, y, farbe='blau', g=44, ein=0.05, x=LX, **kw):
    d = dict(typ='notiz', text=t, x=x, y=y, groesse=g, farbe=farbe, ein=ein)
    d.update(kw)
    return d


def tx(t, y, g=34, ein=0.05, x=LX, **kw):
    d = dict(typ='text', text=t, x=x, y=y, groesse=g, ein=ein, abstand=0)
    d.update(kw)
    return d


def titel(t, y=280, g=80):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=[e for e in el if e])


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def fenster(x0, x1, y0, y1, xt, yt_):
    assert x1 - x0 == y1 - y0, 'Achsen 1 : 1 (reine Mathematik, STYLEGUIDE §3.1)'
    return dict(xbereich=[x0, x1], ybereich=[y0, y1], xteilung=yt(*xt), yteilung=yt(*yt_))


def graf(W, geraden=(), punkte=(), strecken=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             geraden=list(geraden), punkte=list(punkte), strecken=list(strecken), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def G(m, q, farbe=1, **kw):
    """Gerade y = m·x + q (als «bewegte» Gerade mit einem Stützpunkt — dann gehen Läufer und Klickfragen)."""
    d = dict(bewegung=[[0, m, q]], farbe=farbe)
    d.update(kw)
    return d


def senk(x, W, farbe=3, gestrichelt=True, **kw):
    d = dict(von=[x, W['ybereich'][0]], bis=[x, W['ybereich'][1]], farbe=farbe, gestrichelt=gestrichelt)
    d.update(kw)
    return d


def pt(x, y, farbe=3, text=None, bei=None, anker='start', **kw):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = bei
    d.update(kw)
    return d


def system(*z, lab=('I', 'II', 'III')):
    return r'\begin{cases} ' + r' \\ '.join(g + r' & \text{(' + lab[i] + ')}' for i, g in enumerate(z)) + r' \end{cases}'


# ---------------------------------------------------------------- Fragen
def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3, kopf=None):
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie in den Vorbildern)."""
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % len(opt)
    dreh = lambda i: (i - k) % len(opt)
    opt = [opt[(i + k) % len(opt)] for i in range(len(opt))]
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': dreh(richtig), 'rueck': {str(dreh(i)): v for i, v in rueck.items()}}
    if kopf:
        d['kopf'] = kopf
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(dreh(i)): v for i, v in rueck_sprich.items()}
    return d


def abc(szene, text, opt, tex, richtig, rueck, sprich=None, rueck_sprich=None, y0=560):
    """Wahlfrage mit den Angeboten im Bild (rechts), Knöpfe A, B, C; gedreht wie wahl()."""
    n_ = len(opt)
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % n_
    reihe = [(j + k) % n_ for j in range(n_)]
    marken = 'ABCD'[:n_]
    bild = [tx('{2:' + marken[j] + '} @' + tex[i] + '@', y0 + j * 90, 40, x=RX, ein=0.05, aus=0.9) for j, i in enumerate(reihe)]
    d = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': list(marken),
         'richtig': reihe.index(richtig),
         'rueck': {str(j): rueck[i] for j, i in enumerate(reihe) if i != richtig},
         'sprich': (sprich or text) + ' A, B oder C?'}
    if rueck_sprich:
        d['rueck_sprich'] = {str(j): rueck_sprich.get(i, rueck[i]) for j, i in enumerate(reihe) if i != richtig}
    return d, bild


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.45, bei=0.3):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text, 'eingabe': ['x', 'y']}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


_BC = []


def _fragen_texte(F_):
    if not _BC:
        spec = importlib.util.spec_from_file_location('bc', R + 'scripts/build-clips.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _BC.append(m)
    return [(k, g) for k, _, g in _BC[0].fragen_texte(F_)]


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip', folge=None):
    zeiten(name, szenen)
    for q in szenen:   # Auflösung erst nach der Antwort (HOWTO §15), Kontrollclips
        pass
    pfad = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(pfad):
        alt = json.load(open(pfad))
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in alt['szenen']}
        nach_name = {q['name']: q.get('dauer') for q in alt['szenen']}
        for i, q in enumerate(szenen, 1):
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
            elif nach_name.get(q['name']):
                q['dauer'] = nach_name[q['name']]
                NEU_TON.append((PRAEFIX + name, i))
        alt_f = alt.get('fragen', [])
        for i, F_ in enumerate(fragen or [], 1):
            neu_t = dict(_fragen_texte(F_))
            alt_t = dict(_fragen_texte(alt_f[i - 1])) if i <= len(alt_f) else {}
            if set(neu_t) != set(alt_t):
                NEU_FRAGEN.append((PRAEFIX + name, str(i)))
            else:
                for k_, g_ in neu_t.items():
                    if alt_t.get(k_) != g_:
                        NEU_FRAGEN.append((PRAEFIX + name, '%d:%s' % (i, k_)))
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Gleichungssysteme',
         'fach': 'Grundlagenfach', 'lerngebiet': '2 · Gleichungen, Ungleichungen und Gleichungssysteme',
         'lektion': ['g2-3'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-11',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Gleichungssysteme lösen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms gleichungssysteme; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if folge:
        d['folge'] = folge
    if fragen:
        texte = [F_['text'][:20] for F_ in fragen]
        assert len(set(texte)) == len(texte), ('Fragen beginnen gleich', texte)
        for F_ in fragen:   # Fragebild: nichts aus der Auflösung vor 1.0 s
            sc = next(q for q in szenen if q['name'] == F_['szene'])
            for e in sc['elemente']:
                assert e.get('_gegeben') or e.get('typ') == 'text' or (isinstance(e.get('ein'), (int, float)) and e['ein'] >= 1.0), \
                    (name, F_['szene'], 'Auflösung vor der Antwort', e.get('text', e.get('typ')))
        d['fragen'] = fragen
    for q in szenen:
        for e in q['elemente']:
            e.pop('_gegeben', None)
    json.dump(d, open(pfad, 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def gegeben(e):
    """Markiert ein Element als Gegebenes der Frage (darf schon beim Erscheinen der Frage stehen)."""
    e['_gegeben'] = True
    return e


JETZT_DU_ANIM = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der Animation unter dem Clip und löse die Aufgaben.',
                   titel('Jetzt du', 300, 86),
                   n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 450, 'blau', 50, ein=0.6))
JETZT_DU_UF = sz('Jetzt du', 'Jetzt du: Löse die Aufgaben im System-Umformer unter dem Clip.',
                 titel('Jetzt du', 300, 86),
                 n('Löse die Aufgaben|im System-Umformer unter dem Clip.', 450, 'blau', 50, ein=0.6))

SYS0 = system('2x + y = 7', 'x - y = -1')

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
W1 = fenster(-3, 6, -1, 8, (-2, -1, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6, 7))
LI = G(-2, 7, 1)
LII = G(1, 1, 2)
# Namen der Geraden, freie Stellen nachgerechnet: (I) y = −2x + 7 läuft bei y = 0.6 durch x = 3.2, (II) y = x + 1 bei x = 5.5 durch 6.5
NAMEN1 = [dict(bei=[3.65, 0.55], text='(I)', farbe=1, groesse=30, anker='start'), dict(bei=[4.9, 5.2], text='(II)', farbe=2, groesse=30, anker='start')]
clip('schnittpunkt', 'Gleichungssysteme lösen: Lösung und Schnittpunkt',
     'Was eine Lösung eines Systems ist, warum jede Gleichung eine Gerade ist und weshalb der Schnittpunkt die Lösung ist — mit Probe.',
     ['Gleichungssystem', 'Lösung', 'Gerade', 'Schnittpunkt', 'Probe'], [
         sz('Zwei Bedingungen',
            'Gesucht sind zwei Zahlen x und y. Zwei mal x plus y soll sieben ergeben, und x minus y soll minus eins ergeben. '
            'Beide Bedingungen gleichzeitig: Das ist ein lineares Gleichungssystem.',
            titel('Zwei Gleichungen', 260, 76),
            f(SYS0, 420, 60, ein='@Zwei#1'),
            n('Eine Lösung ist ein Zahlenpaar @(x \\mid y)@,|das beide Gleichungen erfüllt.', 640, 'blau', 44, ein='@gleichzeitig')),
         sz('Viele Lösungen',
            'Die erste Gleichung allein hat viele Lösungen: null und sieben, eins und fünf, zwei und drei, drei und eins. '
            'Zu jedem x gibt es ein passendes y. Alle diese Paare liegen auf einer Geraden.',
            f(r'\fa{2x + y = 7}', 260, 56, ein=0.3),
            f(r'(0 \mid 7)', 380, 48, ein='@null'),
            f(r'(1 \mid 5)', 460, 48, ein='@eins'),
            f(r'(2 \mid 3)', 540, 48, ein='@zwei'),
            f(r'(3 \mid 1)', 620, 48, ein='@drei'),
            n('unendlich viele Paare:|eine Gerade', 760, 'blau', 44, ein='@Geraden'),
            graf(W1, punkte=[pt(0, 7, 1, ein='@null'), pt(1, 5, 1, ein='@eins'), pt(2, 3, 1, ein='@zwei'), pt(3, 1, 1, ein='@drei')],
                 geraden=[dict(G(-2, 7, 1), ein='@Geraden')], ein=0.3)),
         sz('Nach y auflösen',
            'Zum Zeichnen löst man nach y auf: y gleich minus zwei x plus sieben. Zwei Punkte genügen für die Gerade. '
            'Genauso die zweite Gleichung: y gleich x plus eins, durch null und eins und durch drei und vier.',
            f(r'\fa{2x + y = 7} \;\Rightarrow\; \fa{y = -2x + 7}', 300, 52, ein='@minus'),
            f(r'\fb{x - y = -1} \;\Rightarrow\; \fb{y = x + 1}', 420, 52, ein='@zweite'),
            graf(W1, geraden=[LI, dict(LII, ein='@zweite')], texte=NAMEN1,
                 punkte=[pt(0, 1, 2, ein='@null'), pt(3, 4, 2, ein='@vier')], ein=0.3)),
         sz('Der Schnittpunkt',
            'Ein Punkt liegt auf beiden Geraden: der Schnittpunkt zwei und drei. Nur dieses Paar erfüllt beide Gleichungen. '
            'Die Lösungsmenge enthält genau dieses Paar.',
            f(SYS0, 300, 56, ein=0.3),
            f(r'\mathbb{L} = \{(\fc{2} \mid \fc{3})\}', 500, 60, ein='@Lösungsmenge'),
            graf(W1, geraden=[LI, LII], texte=NAMEN1, punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.7], ein='@Schnittpunkt')], ein=0.05)),
         sz('Die Probe',
            'Abgelesene Werte sind Schätzungen. Darum die Probe in beiden Gleichungen: Zwei mal zwei plus drei gibt sieben. '
            'Zwei minus drei gibt minus eins. Beide stimmen.',
            n('Ablesen ist eine Schätzung.', 280, 'blau', 44, ein=0.4),
            f(r'\text{(I)}\;\; 2 \cdot 2 + 3 = 7 \;\fc{\checkmark}', 400, 52, ein='@sieben'),
            f(r'\text{(II)}\;\; 2 - 3 = -1 \;\fc{\checkmark}', 500, 52, ein='@minus'),
            graf(W1, geraden=[LI, LII], texte=NAMEN1, punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.7])], ein=0.05)),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Jede Gleichung ist eine Gerade. Die Lösung des Systems ist der Schnittpunkt, bestätigt mit der Probe in beiden Gleichungen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Jede Gleichung: eine Gerade.|Lösung des Systems: der Schnittpunkt.|Probe in beiden Gleichungen.', 400, 'blau', 46, ein=1.2)),
         JETZT_DU_ANIM,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
W1k = fenster(-2, 7, -2, 7, (-1, 1, 2, 3, 4, 5, 6), (-1, 1, 2, 3, 4, 5, 6))
W1f = fenster(-2, 9, -3, 8, (-1, 1, 2, 3, 4, 5, 6, 7, 8), (-2, -1, 1, 2, 3, 4, 5, 6, 7))
d11, b11 = abc('Frage 1', 'Ist (1 | 4) eine Lösung von (I) 3x + y = 7 und (II) x + y = 4?',
               ['(I) stimmt', '(II) nicht', 'beide'],
               [r'\text{Ja, (I) stimmt.}', r'\text{Nein, (II) stimmt nicht.}', r'\text{Ja, beide stimmen.}'], 1,
               {0: 'Eine Gleichung reicht nicht. Setz auch in (II) ein.', 1: 'Ja.', 2: 'Setz in (II) ein: 1 + 4 = ?'},
               sprich='Ist eins und vier eine Lösung der ersten Gleichung drei x plus y gleich sieben und der zweiten Gleichung x plus y gleich vier?',
               rueck_sprich={0: 'Eine Gleichung reicht nicht. Setz auch in die zweite ein.', 2: 'Setz in die zweite Gleichung ein: eins plus vier gibt?'})
d3, b3 = abc('Frage 5', 'Abgelesen: etwa (1 | 2). Das System heisst x + 2y = 5 und 3x − 2y = −1. Was zeigt die Probe?',
             ['beide stimmen', 'nur (I) stimmt', 'keine Probe nötig'],
             [r'\text{beide stimmen: } \mathbb{L} = \{(1 \mid 2)\}', r'\text{nur (I) stimmt}', r'\text{Ablesen genügt, keine Probe nötig}'], 0,
             {0: 'Ja.', 1: 'Setz (1 | 2) auch in (II) ein: 3 · 1 − 2 · 2 = ?', 2: 'Abgelesen ist nur ungefähr. Was zeigt das Einsetzen?'},
             sprich='Abgelesen: etwa eins und zwei. Das System heisst x plus zwei y gleich fünf und drei x minus zwei y gleich minus eins. Was zeigt die Probe?',
             rueck_sprich={1: 'Setz eins und zwei auch in die zweite Gleichung ein: drei mal eins minus zwei mal zwei gibt?',
                           2: 'Abgelesen ist nur ungefähr. Was zeigt das Einsetzen?'})
clip('kontrolle-schnittpunkt', 'Gleichungssysteme lösen: Kontrollfragen zu Lösung und Schnittpunkt',
     'Fünf Fragen: Ist ein Paar eine Lösung? Wie viele Lösungen hat eine Gleichung allein? Nach y auflösen, Schnittpunkt antippen, Probe.',
     ['Gleichungssystem', 'Schnittpunkt', 'Probe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Einsetzen in die erste Gleichung: drei plus vier gibt sieben, das stimmt. In die zweite: eins plus vier gibt fünf, nicht vier. '
            'Eine Lösung muss beide Gleichungen erfüllen. Eins und vier ist keine Lösung.',
            *b11,
            f(r'\text{(I)}\;\; 3 \cdot 1 + 4 = 7 \;\fc{\checkmark}', 300, 52, ein='@stimmt'),
            f(r'\text{(II)}\;\; 1 + 4 = 5 \fd{\;\neq 4}', 400, 52, ein='@nicht'),
            n('Eine Lösung erfüllt|beide Gleichungen.', 520, 'blau', 44, ein='@beide'),
            graf(W1k, geraden=[G(-3, 7, 1), G(-1, 4, 2)], punkte=[pt(1, 4, 5, '(1 | 4)', [1.3, 4.6])], ein='@beide')),
         sz('Frage 2',
            'Zu jedem x passt ein y, nämlich sechs minus x: null und sechs, zwei und vier, fünf und eins. Unendlich viele Paare, im Bild eine ganze Gerade.',
            f(r'y = 6 - x', 300, 56, ein='@nämlich'),
            f(r'(0 \mid 6),\ (2 \mid 4),\ (5 \mid 1),\ \ldots', 420, 48, ein='@und'),
            graf(W1k, geraden=[G(-1, 6, 1, laeufer={'bahn': [['@und', 0], ['@Unendlich', 5]], 'text': '({x} | {y})', 'farbe': 5})], ein='@und')),
         sz('Frage 3',
            'Minus vier x auf beiden Seiten: zwei y gleich minus vier x plus sechs. Durch zwei: y gleich minus zwei x plus drei.',
            f(r'4x + 2y = 6', 300, 52, ein=1.0),
            op('-4x', 300, '@Minus'),
            f(r'2y = -4x + 6', 400, 52, ein='@zwei'),
            op(':2', 400, '@Durch'),
            f(r'y = -2x + 3', 500, 52, ein='@Durch+0.8')),
         sz('Frage 4',
            'Die Geraden schneiden sich bei vier und zwei. Probe: vier minus zwei gibt zwei, vier plus zwei mal zwei gibt acht.',
            gegeben(f(system('x - y = 2', 'x + 2y = 8'), 300, 52, ein=0.05)),
            f(r'4 - 2 = 2 \;\fc{\checkmark}', 490, 50, ein='@Probe'),
            f(r'4 + 2 \cdot 2 = 8 \;\fc{\checkmark}', 580, 50, ein='@acht'),
            f(r'\mathbb{L} = \{(\fc{4} \mid \fc{2})\}', 700, 56, ein='@acht+0.6'),
            gegeben(graf(W1f, geraden=[G(1, -2, 1), G(-0.5, 4, 2)], ein=0.05,
                         texte=[dict(bei=[6.6, 3.7], text='(I)', farbe=1, groesse=30, anker='start'), dict(bei=[-1.7, 3.9], text='(II)', farbe=2, groesse=30, anker='start')])),
            graf(W1f, achsen=False, raster=False, tippbar=False, punkte=[pt(4, 2, 3, '(4 | 2)', [4.3, 1.1])], ein='@schneiden')),
         sz('Frage 5',
            'Eins plus zwei mal zwei gibt fünf. Drei minus zwei mal zwei gibt minus eins. Beide stimmen: Die Lösungsmenge enthält das Paar eins und zwei.',
            *b3,
            f(r'\text{(I)}\;\; 1 + 2 \cdot 2 = 5 \;\fc{\checkmark}', 300, 50, ein='@fünf'),
            f(r'\text{(II)}\;\; 3 - 2 \cdot 2 = -1 \;\fc{\checkmark}', 400, 50, ein='@minus'),
            f(r'\mathbb{L} = \{(\fc{1} \mid \fc{2})\}', 520, 56, ein='@Lösungsmenge')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Eine Lösung erfüllt alle Gleichungen. Im Bild ist sie der Schnittpunkt, und erst die Probe bestätigt sie.',
            titel('Zum Mitnehmen', 250, 76),
            n('Lösung: erfüllt alle Gleichungen.|Im Bild: der Schnittpunkt.|Bestätigt durch die Probe.', 400, 'blau', 46, ein=1.2)),
     ], [
         d11,
         wahl('Frage 2', 'Die Gleichung x + y = 6 allein: Wie viele Zahlenpaare erfüllen sie?',
              ['unendlich viele', 'genau eines', 'keines'], 0,
              {0: 'Ja.', 1: 'Probier x = 0 und x = 1. Passt beide Male ein y?', 2: 'Probier x = 0: Welches y passt?'},
              sprich='Die Gleichung x plus y gleich sechs allein: Wie viele Zahlenpaare erfüllen sie?',
              rueck_sprich={1: 'Probier x gleich null und x gleich eins. Passt beide Male ein y?', 2: 'Probier x gleich null: Welches y passt?'}),
         wahl('Frage 3', 'Nach y aufgelöst: 4x + 2y = 6 wird zu …',
              ['y = −2x + 3', 'y = 2x + 3', 'y = −4x + 6'], 0,
              {0: 'Ja.', 1: 'Vorzeichen: Bringst du 4x auf die andere Seite, wird daraus −4x.', 2: 'Danach steht noch 2y da. Teile durch 2.'},
              sprich='Nach y aufgelöst: vier x plus zwei y gleich sechs wird zu?',
              rueck_sprich={1: 'Vorzeichen: Bringst du vier x auf die andere Seite, wird daraus minus vier x.', 2: 'Danach steht noch zwei y da. Teile durch zwei.'}),
         klick('Frage 4', 'Die Geraden gehören zu x − y = 2 und x + 2y = 8. Tipp die Lösung an.', [4, 2],
               'Getroffen: (4 | 2) liegt auf beiden Geraden.',
               [{'bei': [2, 0], 'text': 'Das ist der Schnitt der blauen Geraden mit der x-Achse.',
                 'sprich': 'Das ist der Schnitt der blauen Geraden mit der x-Achse.'},
                {'bei': [0, 4], 'text': 'Das ist der Schnitt der orangen Geraden mit der y-Achse.',
                 'sprich': 'Das ist der Schnitt der orangen Geraden mit der y-Achse.'}],
               'Gesucht ist der Punkt auf beiden Geraden.',
               sprich='Die Geraden gehören zu x minus y gleich zwei und x plus zwei y gleich acht. Tipp die Lösung an.'),
         d3,
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
clip('einsetzen', 'Gleichungssysteme lösen: Einsetzen und Gleichsetzen',
     'Einsetzverfahren und Gleichsetzverfahren an 2x + y = 7, x − y = −1: eine Variable eliminieren, lösen, zurück einsetzen — und der häufigste Fehler.',
     ['Gleichungssystem', 'Einsetzverfahren', 'Gleichsetzverfahren', 'eliminieren'], [
         sz('Eine Variable allein',
            'Beim Einsetzverfahren stellt man eine Variable frei. In der zweiten Gleichung geht das schnell: x gleich y minus eins.',
            titel('Einsetzen', 250, 76),
            f(SYS0, 400, 56, ein=0.4),
            f(r'\text{(II)}\;\; \fb{x = y - 1}', 600, 52, ein='@gleich')),
         sz('Einsetzen',
            'Diesen Term setzt man in die andere Gleichung ein, in Klammern: zwei mal Klammer y minus eins plus y gleich sieben. '
            'Jetzt fehlt x: Es bleibt eine Gleichung mit einer Variablen.',
            f(r'\fb{x = y - 1} \;\text{ in (I)}', 280, 50, ein=0.3),
            f(r'2\,\fb{(y - 1)} + y = 7', 400, 56, ein='@zwei'),
            n('@x@ ist eliminiert.', 540, 'blau', 44, ein='@fehlt')),
         sz('Lösen',
            'Klammer auflösen: zwei y minus zwei plus y gleich sieben. Zusammenfassen und plus zwei: drei y gleich neun. '
            'Durch drei: y gleich drei. Zurück in x gleich y minus eins: x gleich zwei.',
            f(r'2y - 2 + y = 7', 260, 50, ein=0.4),
            op('+2', 260, '@Zusammenfassen'),
            f(r'3y = 9', 350, 50, ein='@neun'),
            op(':3', 350, '@Durch'),
            f(r'y = \fc{3}', 440, 50, ein='@Durch+0.7'),
            f(r'x = 3 - 1 = \fc{2}', 530, 50, ein='@eins+0.8'),
            graf(W1, texte=NAMEN1, geraden=[LI, LII, G(0, 3, 3, dicke=3, gestrichelt=True, ein='@Durch+0.7')],
                 punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.7], ein='@eins+0.8')], ein=0.3)),
         sz('Gleichsetzen',
            'Sind beide Gleichungen nach derselben Variablen aufgelöst, setzt man gleich: y gleich sieben minus zwei x und y gleich x plus eins. '
            'Also sieben minus zwei x gleich x plus eins. Das gibt drei x gleich sechs, x gleich zwei, und y gleich drei.',
            titel('Gleichsetzen', 220, 64),
            f(r'\fa{y = 7 - 2x}, \quad \fb{y = x + 1}', 340, 50, ein='@sieben'),
            f(r'\fa{7 - 2x} = \fb{x + 1}', 440, 52, ein='@Also'),
            f(r'3x = 6', 540, 50, ein='@gibt'),
            f(r'x = \fc{2}', 630, 50, ein='@sechs+0.6'),
            f(r'y = \fc{3}', 630, 50, ein='@drei#2', x=LX + 260),
            graf(W1, geraden=[LI, LII], texte=NAMEN1, strecken=[senk(2, W1, ein='@sechs+0.6', dicke=3)],
                 punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.7], ein='@drei#2')], ein=0.3)),
         sz('Der Fehler',
            'Ein häufiger Fehler: den Term in dieselbe Gleichung zurücksetzen. Aus zwei x plus y gleich sieben wird y gleich sieben minus zwei x. '
            'In dieselbe Gleichung eingesetzt bleibt sieben gleich sieben. Wahr, aber nutzlos.',
            f(r'\fa{2x + y = 7} \;\Rightarrow\; y = 7 - 2x', 300, 50, ein='@zwei'),
            f(r'2x + (7 - 2x) = 7', 420, 52, ein='@dieselbe#2'),
            f(r'\fd{7 = 7}', 520, 56, ein='@bleibt'),
            n('Der Term gehört in die|andere Gleichung.', 650, 'rot', 44, ein='@nutzlos+0.6')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Eine Variable freistellen, den Term in Klammern in die andere Gleichung einsetzen, lösen, zurück einsetzen, Probe. '
            'Sind beide Gleichungen gleich aufgelöst: gleichsetzen.',
            titel('Zum Mitnehmen', 250, 76),
            n('freistellen → in Klammern einsetzen|→ lösen → zurück einsetzen → Probe', 400, 'blau', 46, ein=1.2),
            n('beide gleich aufgelöst: gleichsetzen', 560, 'blau', 46, ein='@gleich')),
         JETZT_DU_UF,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
W2k = fenster(-2, 5, -1, 6, (-1, 1, 2, 3, 4), (1, 2, 3, 4, 5))
d22, b22 = abc('Frage 2', 'x = 2y − 1 in 3x + y = 11 einsetzen: Was ist richtig?',
               ['3(2y − 1) + y = 11', '6y − 1 + y = 11', '3x + 2y − 1 = 11'],
               [r'3\,(2y - 1) + y = 11', r'6y - 1 + y = 11', r'3x + 2y - 1 = 11'], 0,
               {0: 'Ja.', 1: 'Die 3 multipliziert den ganzen Term, auch die −1.', 2: 'Ersetzt wird x, nicht y.'},
               sprich='x gleich zwei y minus eins in drei x plus y gleich elf einsetzen: Was ist richtig?',
               rueck_sprich={1: 'Die Drei multipliziert den ganzen Term, auch die minus eins.', 2: 'Ersetzt wird x, nicht y.'})
d24, b24 = abc('Frage 4', 'Jemand setzt y = 7 − 2x in 2x + y = 7 ein und erhält 7 = 7. Was ist passiert?',
               ['dieselbe Gleichung', 'unendlich viele', 'keine Lösung'],
               [r'\text{in dieselbe Gleichung eingesetzt}', r'\text{unendlich viele Lösungen}', r'\text{keine Lösung}'], 0,
               {0: 'Ja.', 1: 'Woher stammt der Term y = 7 − 2x?', 2: '7 = 7 ist wahr, kein Widerspruch. Woher stammt der Term?'},
               sprich='Jemand setzt y gleich sieben minus zwei x in zwei x plus y gleich sieben ein und erhält sieben gleich sieben. Was ist passiert?',
               rueck_sprich={1: 'Woher stammt der Term y gleich sieben minus zwei x?', 2: 'Sieben gleich sieben ist wahr, kein Widerspruch. Woher stammt der Term?'})
clip('kontrolle-einsetzen', 'Gleichungssysteme lösen: Kontrollfragen zum Einsetzen und Gleichsetzen',
     'Fünf Fragen: Term einsetzen, Klammer setzen, gleichsetzen, der Fehler «7 = 7» und eine Lösung ins Bild tippen.',
     ['Einsetzverfahren', 'Gleichsetzverfahren', 'Kontrollfragen'], [
         sz('Frage 1',
            'y wird durch den ganzen Term ersetzt: zwei x plus drei x minus vier gleich sechs. Dann fünf x gleich zehn, x gleich zwei, und y gleich zwei.',
            f(r'2x + (3x - 4) = 6', 300, 52, ein='@ganzen'),
            f(r'5x = 10', 420, 50, ein='@dann'),
            f(r'x = \fc{2}', 510, 50, ein='@dann+1.3'),
            f(r'y = \fc{2}', 510, 50, ein='@und', x=LX + 260)),
         sz('Frage 2',
            'Der Term ersetzt x als Ganzes, also in Klammern: drei mal Klammer zwei y minus eins. Ausmultipliziert: sechs y minus drei plus y gleich elf. '
            'Sieben y gleich vierzehn, y gleich zwei, und x gleich drei.',
            *b22,
            f(r'3\,(2y - 1) + y = 11', 300, 52, ein='@Klammern'),
            f(r'6y - 3 + y = 11', 400, 50, ein='@Ausmultipliziert'),
            f(r'7y = 14', 500, 50, ein='@Sieben'),
            f(r'y = \fc{2}', 590, 50, ein='@zwei#2'),
            f(r'x = \fc{3}', 590, 50, ein='@und', x=LX + 260)),
         sz('Frage 3',
            'Zwei x plus eins gleich minus x plus sieben. Plus x und minus eins: drei x gleich sechs, also x gleich zwei. Dann ist y gleich fünf.',
            f(r'2x + 1 = -x + 7', 300, 52, ein=1.0),
            f(r'3x = 6 \;\Rightarrow\; x = \fc{2}', 400, 52, ein='@drei'),
            f(r'y = 2 \cdot 2 + 1 = \fc{5}', 500, 50, ein='@fünf')),
         sz('Frage 4',
            'Der Term stammt aus derselben Gleichung. Eingesetzt sagt sie nur, was sie schon weiss. Der Term gehört in die andere Gleichung.',
            *b24,
            f(r'2x + (7 - 2x) = 7 \;\Rightarrow\; 7 = 7', 300, 50, ein=1.0),
            n('Der Term gehört in|die andere Gleichung.', 430, 'rot', 44, ein='@andere')),
         sz('Frage 5',
            'Gleichsetzen: x plus zwei gleich minus zwei x plus fünf, also drei x gleich drei und x gleich eins. Dann y gleich drei. Der Schnittpunkt ist eins und drei.',
            f(r'x + 2 = -2x + 5', 300, 52, ein=1.0),
            f(r'3x = 3', 400, 50, ein='@drei'),
            f(r'x = \fc{1}', 490, 50, ein='@eins'),
            f(r'y = \fc{3}', 490, 50, ein='@dann', x=LX + 260),
            gegeben(graf(W2k, geraden=[], ein=0.05)),
            graf(W2k, geraden=[G(1, 2, 1), G(-2, 5, 2)], punkte=[pt(1, 3, 3, '(1 | 3)', [1.3, 3.5], ein='@Schnittpunkt')], ein='@Gleich')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Der Term ersetzt eine Variable als Ganzes, in Klammern, und gehört in die andere Gleichung.',
            titel('Zum Mitnehmen', 250, 76),
            n('Term in Klammern|in die andere Gleichung einsetzen.', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'y = 3x − 4 in 2x + y = 6 einsetzen: Was entsteht?',
              ['2x + (3x − 4) = 6', '2x + 3x = 6', '2(3x − 4) = 6'], 0,
              {0: 'Ja.', 1: 'Der ganze Term ersetzt y, auch die −4.', 2: 'Ersetzt wird y, nicht das 2x.'},
              sprich='y gleich drei x minus vier in zwei x plus y gleich sechs einsetzen: Was entsteht?',
              rueck_sprich={1: 'Der ganze Term ersetzt y, auch die minus vier.', 2: 'Ersetzt wird y, nicht das zwei x.'}),
         d22,
         wahl('Frage 3', 'y = 2x + 1 und y = −x + 7 gleichsetzen: Welches x?',
              ['x = 2', 'x = 6', 'x = 8/3'], 0,
              {0: 'Ja.', 1: 'Um −x wegzubringen, rechnest du auf beiden Seiten +x.', 2: 'Um +1 wegzubringen, rechnest du auf beiden Seiten −1.'},
              sprich='y gleich zwei x plus eins und y gleich minus x plus sieben gleichsetzen: Welches x?',
              rueck_sprich={1: 'Um minus x wegzubringen, rechnest du auf beiden Seiten plus x.', 2: 'Um plus eins wegzubringen, rechnest du auf beiden Seiten minus eins.'}),
         d24,
         klick('Frage 5', 'y = x + 2 und y = −2x + 5: Rechne, dann tipp die Lösung an.', [1, 3],
               'Getroffen: (1 | 3).',
               [{'bei': [3, 1], 'text': 'Koordinaten vertauscht: zuerst x, dann y.', 'sprich': 'Koordinaten vertauscht: zuerst x, dann y.'}],
               'Setz die rechten Seiten gleich, rechne x aus, dann y.',
               sprich='y gleich x plus zwei und y gleich minus zwei x plus fünf: Rechne, dann tipp die Lösung an.'),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
W3 = fenster(-3, 6, -1, 8, (-2, -1, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6, 7))
clip('addition', 'Gleichungssysteme lösen: Additionsverfahren und Verfahrenswahl',
     'Gleichungen addieren, bis eine Variable wegfällt — auch nach dem Vervielfachen beider Gleichungen; dazu, welches Verfahren wann am kürzesten ist.',
     ['Gleichungssystem', 'Additionsverfahren', 'Verfahrenswahl'], [
         sz('Addieren',
            'Beim Additionsverfahren addiert man die Gleichungen. Zwei x plus y gleich sieben, x minus y gleich minus eins. '
            'Plus y und minus y heben sich weg: drei x gleich sechs, also x gleich zwei.',
            titel('Addieren', 230, 70),
            f(SYS0, 370, 56, ein='@Zwei'),
            f(r'\text{(I)} + \text{(II)}:\;\; 3x = 6', 560, 52, ein='@heben'),
            f(r'x = \fc{2}', 650, 52, ein='@also'),
            graf(W3, geraden=[LI, LII], texte=NAMEN1, strecken=[senk(2, W3, ein='@sechs', dicke=3)], ein=0.3)),
         sz('Durch den Schnittpunkt',
            'Die Summe ist wieder eine Gerade: x gleich zwei, eine Senkrechte. Sie geht durch den Schnittpunkt, denn er erfüllt beide Gleichungen, also auch ihre Summe. '
            'In die erste eingesetzt: vier plus y gleich sieben, also y gleich drei.',
            f(r'\fc{x = 2}', 300, 56, ein=0.4),
            f(r'2 \cdot 2 + y = 7', 440, 50, ein='@vier'),
            f(r'y = \fc{3}', 530, 50, ein='@also#2'),
            graf(W3, geraden=[LI, LII], texte=NAMEN1, strecken=[senk(2, W3, dicke=3)], punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.7], ein='@Schnittpunkt')], ein=0.05)),
         sz('Passend machen',
            'Meist fällt nichts von selbst weg: zwei x plus drei y gleich zwölf und fünf x minus zwei y gleich elf. '
            'Die erste mal zwei, die zweite mal drei: Dann stehen plus sechs y und minus sechs y da. Mit der Zahl multipliziert man immer beide Seiten.',
            f(system('2x + 3y = 12', '5x - 2y = 11'), 280, 54, ein=0.4),
            f(r'4x + \fa{6y} = 24 \qquad 2 \cdot \text{(I)}', 480, 50, ein='@erste'),
            f(r'15x \fb{\;- 6y} = 33 \qquad 3 \cdot \text{(II)}', 570, 50, ein='@zweite'),
            n('beide Seiten multiplizieren', 690, 'blau', 44, ein='@beide')),
         sz('Addieren und lösen',
            'Addiert: neunzehn x gleich siebenundfünfzig, also x gleich drei. Eingesetzt in die erste: sechs plus drei y gleich zwölf, y gleich zwei. '
            'Probe in der zweiten: fünfzehn minus vier gibt elf.',
            f(r'19x = 57', 300, 52, ein='@neunzehn'),
            f(r'x = \fc{3}', 300, 52, ein='@also', x=LX + 380),
            f(r'6 + 3y = 12', 400, 52, ein='@sechs'),
            f(r'y = \fc{2}', 400, 52, ein='@zwei', x=LX + 380),
            f(r'\text{Probe (II): } 15 - 4 = 11 \;\fc{\checkmark}', 500, 50, ein='@Probe'),
            f(r'\mathbb{L} = \{(\fc{3} \mid \fc{2})\}', 620, 56, ein='@elf')),
         sz('Subtrahieren',
            'Stehen vor einer Variablen gleiche Zahlen, subtrahiert man. Zwei x plus drei y gleich dreizehn und zwei x minus y gleich eins. '
            'Die erste minus die zweite: Zwei x minus zwei x ist null, drei y minus minus y ist vier y. Rechts dreizehn minus eins ist zwölf. '
            'Also vier y gleich zwölf, y gleich drei, und x gleich zwei.',
            f(system('2x + 3y = 13', '2x - y = 1'), 280, 54, ein='@Zwei'),
            f(r'\text{(I)} - \text{(II)}:\;\; 3y - (-y) = 4y', 470, 48, ein='@vier'),
            f(r'13 - 1 = 12', 560, 48, ein='@Rechts'),
            f(r'4y = 12', 650, 50, ein='@Also'),
            f(r'y = \fc{3},\ x = \fc{2}', 740, 50, ein='@drei#3'),
            graf(W3, geraden=[G(-2 / 3, 13 / 3, 1), G(2, -1, 2), G(0, 3, 3, dicke=3, gestrichelt=True, ein='@Also')],
                 punkte=[pt(2, 3, 3, '(2 | 3)', [2.45, 2.2], ein='@drei#3')], ein='@Zwei')),
         sz('Welches Verfahren?',
            'Welches Verfahren ist am kürzesten? Steht eine Variable allein: einsetzen. Sind beide nach derselben aufgelöst: gleichsetzen. '
            'Stehen vor einer Variablen entgegengesetzte Zahlen: addieren. Stehen gleiche Zahlen davor: subtrahieren.',
            titel('Welches Verfahren?', 230, 64),
            f(r'y = 2x + 3 \;\;\longrightarrow\;\; \text{Einsetzen}', 370, 48, ein='@allein'),
            f(r'y = \ldots,\; y = \ldots \;\;\longrightarrow\;\; \text{Gleichsetzen}', 470, 48, ein='@gleichsetzen'),
            f(r'3x + 2y = 7,\; 3x - 2y = 1 \;\;\longrightarrow\;\; \text{Addition}', 570, 48, ein='@entgegengesetzte'),
            f(r'2x + 3y = 13,\; 2x - y = 1 \;\;\longrightarrow\;\; \text{Subtraktion}', 670, 48, ein='@subtrahieren')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Vervielfachen, immer beide Seiten, bis eine Variable beim Addieren oder Subtrahieren wegfällt. Dann lösen, zurück einsetzen, Probe.',
            titel('Zum Mitnehmen', 250, 76),
            n('vervielfachen (beide Seiten)|→ addieren oder subtrahieren|→ lösen → einsetzen → Probe', 400, 'blau', 46, ein=1.2)),
         JETZT_DU_UF,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-addition', 'Gleichungssysteme lösen: Kontrollfragen zum Additionsverfahren',
     'Fünf Fragen: addieren, den passenden Faktor finden, subtrahieren mit Vorzeichen, und zweimal das kürzeste Verfahren wählen.',
     ['Additionsverfahren', 'Verfahrenswahl', 'Kontrollfragen'], [
         sz('Frage 1',
            'Plus drei y und minus drei y heben sich weg: sechs x gleich achtzehn, x gleich drei. In die erste: zwölf plus drei y gleich sechs, also y gleich minus zwei.',
            f(r'6x = 18', 300, 52, ein='@sechs'),
            f(r'x = \fc{3}', 300, 52, ein='@drei#3', x=LX + 380),
            f(r'12 + 3y = 6', 400, 52, ein='@zwölf'),
            f(r'y = \fc{-2}', 400, 52, ein='@also', x=LX + 380)),
         sz('Frage 2',
            'Vor y stehen plus vier und minus zwei. Mal zwei wird daraus minus vier y, und beim Addieren fällt y weg: sieben x gleich fünfunddreissig. '
            'Also x gleich fünf und y gleich eins.',
            f(r'6x - 4y = 26 \qquad 2 \cdot \text{(II)}', 300, 50, ein='@zwei#2'),
            f(r'7x = 35', 420, 50, ein='@sieben'),
            f(r'x = \fc{5}', 510, 50, ein='@also'),
            f(r'y = \fc{1}', 510, 50, ein='@also+1.3', x=LX + 260)),
         sz('Frage 3',
            'Fünf x minus fünf x ist null. Zwei y minus minus drei y ist fünf y. Rechts neun minus minus eins ist zehn. Also fünf y gleich zehn und y gleich zwei.',
            f(r'2y - (-3y) = 5y', 300, 52, ein='@Zwei'),
            f(r'9 - (-1) = 10', 400, 52, ein='@Rechts'),
            f(r'5y = 10', 500, 52, ein='@Also'),
            f(r'y = \fc{2}', 500, 52, ein='@und', x=LX + 380)),
         sz('Frage 4',
            'Beide Gleichungen sind nach y aufgelöst: gleichsetzen. Vier x minus eins gleich minus zwei x plus fünf, also x gleich eins und y gleich drei.',
            f(r'4x - 1 = -2x + 5', 300, 52, ein='@Vier'),
            f(r'6x = 6 \;\Rightarrow\; x = \fc{1},\ y = \fc{3}', 400, 50, ein='@also')),
         sz('Frage 5',
            'Vor x stehen drei und minus drei: addieren. Sieben y gleich sieben, y gleich eins, und x gleich minus eins.',
            f(r'7y = 7', 300, 52, ein='@Sieben'),
            f(r'y = \fc{1}', 300, 52, ein='@eins', x=LX + 380),
            f(r'3x + 5 = 2 \;\Rightarrow\; x = \fc{-1}', 400, 52, ein='@minus#2')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Beim Vervielfachen beide Seiten, beim Subtrahieren auf jedes Vorzeichen achten — und vorher fünf Sekunden hinschauen, welches Verfahren am kürzesten ist.',
            titel('Zum Mitnehmen', 250, 76),
            n('beide Seiten vervielfachen|beim Subtrahieren: Vorzeichen|erst hinschauen, dann rechnen', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', '4x + 3y = 6 und 2x − 3y = 12 addiert ergibt …',
              ['6x = 18', '6x + 6y = 18', '2x = −6'], 0,
              {0: 'Ja.', 1: '3y + (−3y) = ?', 2: 'Addieren, nicht subtrahieren: 4x + 2x.'},
              sprich='Vier x plus drei y gleich sechs und zwei x minus drei y gleich zwölf addiert ergibt?',
              rueck_sprich={1: 'Drei y plus minus drei y gibt?', 2: 'Addieren, nicht subtrahieren: vier x plus zwei x.'}),
         wahl('Frage 2', 'x + 4y = 9, 3x − 2y = 13: Womit (II) multiplizieren, damit y beim Addieren wegfällt?',
              ['mit 2', 'mit −2', 'mit 4'], 0,
              {0: 'Ja.', 1: 'Dann steht zweimal +4y — beim Addieren bleibt y.', 2: 'Dann stehen +4y und −8y da.'},
              sprich='x plus vier y gleich neun und drei x minus zwei y gleich dreizehn: Womit die zweite Gleichung multiplizieren, damit y beim Addieren wegfällt?',
              rueck_sprich={1: 'Dann steht zweimal plus vier y. Beim Addieren bleibt y.', 2: 'Dann stehen plus vier y und minus acht y da.'}),
         wahl('Frage 3', '(5x + 2y = 9) minus (5x − 3y = −1) ergibt …',
              ['5y = 10', '−y = 10', '−y = 8'], 0,
              {0: 'Ja.', 1: '2y − (−3y): Minus mal minus gibt plus.', 2: 'Vorzeichen bei y und rechts: 2y − (−3y) und 9 − (−1).'},
              sprich='Die Gleichung fünf x plus zwei y gleich neun minus die Gleichung fünf x minus drei y gleich minus eins ergibt?',
              rueck_sprich={1: 'Zwei y minus minus drei y: Minus mal minus gibt plus.', 2: 'Vorzeichen bei y und rechts: zwei y minus minus drei y, und neun minus minus eins.'}),
         wahl('Frage 4', 'y = 4x − 1 und y = −2x + 5: Welches Verfahren ist am kürzesten?',
              ['Gleichsetzen', 'Addition', 'grafisch'], 0,
              {0: 'Ja.', 1: 'Dafür müsstest du zuerst beide Gleichungen ordnen.', 2: 'Ein Bild gibt nur eine Schätzung.'},
              sprich='y gleich vier x minus eins und y gleich minus zwei x plus fünf: Welches Verfahren ist am kürzesten?'),
         wahl('Frage 5', '3x + 5y = 2 und −3x + 2y = 5: Welches Verfahren ist am kürzesten?',
              ['Addition', 'Gleichsetzen', 'Einsetzen'], 0,
              {0: 'Ja.', 1: 'Keine Gleichung ist aufgelöst. Schau auf die Zahlen vor x.', 2: 'Keine Variable steht allein. Schau auf die Zahlen vor x.'},
              sprich='Drei x plus fünf y gleich zwei und minus drei x plus zwei y gleich fünf: Welches Verfahren ist am kürzesten?',
              rueck_sprich={1: 'Keine Gleichung ist aufgelöst. Schau auf die Zahlen vor x.', 2: 'Keine Variable steht allein. Schau auf die Zahlen vor x.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
W4 = fenster(-3, 6, -3, 6, (-2, -1, 1, 2, 3, 4, 5), (-2, -1, 1, 2, 3, 4, 5))
W4p = fenster(-4, 6, -5, 5, (-3, -2, -1, 1, 2, 3, 4, 5), (-4, -3, -2, -1, 1, 2, 3, 4))
clip('faelle', 'Gleichungssysteme lösen: keine oder unendlich viele Lösungen',
     'Wenn beim Eliminieren 0 = 2 oder 0 = 0 übrig bleibt: parallele und identische Geraden, die Lösungsmenge in beiden Fällen und ein Parameter k, der zwischen ihnen entscheidet.',
     ['Lösungsfälle', 'parallel', 'identisch', 'Parameter'], [
         sz('Ein Widerspruch',
            'Nicht jedes System hat genau eine Lösung. x plus y gleich drei und x plus y gleich fünf. Die zweite minus die erste: null gleich zwei. '
            'Das ist falsch, egal welche Zahlen man einsetzt. Die Lösungsmenge ist leer.',
            f(system('x + y = 3', 'x + y = 5'), 280, 54, ein='@drei'),
            f(r'\text{(II)} - \text{(I)}:\;\; 0 = 2 \quad \fd{\text{falsch}}', 470, 50, ein='@gleich#3'),
            f(r'\mathbb{L} = \{\,\}', 580, 56, ein='@leer'),
            graf(W4, geraden=[G(-1, 3, 1), G(-1, 5, 2)], ein='@drei')),
         sz('Parallel',
            'Im Bild sind die Geraden parallel. Nach y aufgelöst haben beide die Steigung minus eins, aber verschiedene Achsenabschnitte. Sie schneiden sich nie.',
            f(r'\fa{y = -x + 3}', 300, 52, ein='@aufgelöst'),
            f(r'\fb{y = -x + 5}', 400, 52, ein='@aufgelöst+0.4'),
            n('gleiche Steigung,|verschiedene Achsenabschnitte', 530, 'blau', 44, ein='@Steigung'),
            graf(W4, geraden=[G(-1, 3, 1, yachse={'farbe': 1}), G(-1, 5, 2, yachse={'farbe': 2})], ein=0.05)),
         sz('Immer wahr',
            'Anders bei zwei x minus y gleich vier und minus vier x plus zwei y gleich minus acht. Zweimal die erste plus die zweite: null gleich null. Das ist immer wahr.',
            f(system('2x - y = 4', '-4x + 2y = -8'), 280, 54, ein='@Anders'),
            f(r'2 \cdot \text{(I)} + \text{(II)}:\;\; 0 = 0 \quad \fc{\text{wahr}}', 470, 50, ein='@null'),
            graf(W4, geraden=[G(2, -4, 1, dicke=9), G(2, -4, 2, gestrichelt=True, dicke=3)], ein='@Anders')),
         sz('Unendlich viele',
            'Die zweite Gleichung ist das minus Zweifache der ersten: Beide Geraden sind identisch. Jeder Punkt dieser Geraden ist eine Lösung: x beliebig, y gleich zwei x minus vier.',
            f(r'\text{(II)} = -2 \cdot \text{(I)}', 280, 50, ein='@Zweifache'),
            f(r'\mathbb{L} = \{(x \mid 2x - 4) : x \in \mathbb{R}\}', 420, 52, ein='@beliebig'),
            # Läufer ohne Live-Beschriftung: gerundetes x und y passten bei Steigung 2 nicht zusammen (Prüfung 12.10.2026, M7)
            graf(W4, geraden=[G(2, -4, 1, dicke=9, laeufer={'bahn': [['@Jeder', 0.5], ['@beliebig+1.5', 4]], 'farbe': 5}),
                              G(2, -4, 2, gestrichelt=True, dicke=3)], ein=0.05)),
         sz('Mit Parameter',
            'Steht ein Parameter k im System, hängt der Fall von k ab. Drei x minus sechs y gleich neun und minus x plus zwei y gleich k. '
            'Die erste plus dreimal die zweite: null gleich neun plus drei k.',
            f(system('3x - 6y = 9', '-x + 2y = k'), 280, 54, ein='@Drei'),
            f(r'\text{(I)} + 3 \cdot \text{(II)}:\;\; 0 = 9 + 3k', 470, 50, ein='@gleich#3'),
            graf(W4p, geraden=[G(0.5, -1.5, 1), G(0.5, 0.5, 2)], ein='@Drei')),
         sz('Der kritische Wert',
            'Für k gleich minus drei steht null gleich null: Die Geraden fallen zusammen. Für jedes andere k ein Widerspruch: parallele Geraden. '
            'Genau eine Lösung gibt es nie, denn beide Geraden haben die Steigung ein Halb.',
            f(r'k = -3:\;\; 0 = 0 \quad \text{identisch}', 300, 50, ein='@null'),
            f(r'k \neq -3:\;\; \fd{0 \neq 9 + 3k} \quad \text{parallel}', 400, 50, ein='@Widerspruch'),
            f(r'\text{Steigung beider Geraden: } \tfrac{1}{2}', 520, 48, ein='@Steigung'),
            graf(W4p, geraden=[G(0.5, -1.5, 1, dicke=8),
                               dict(G(0.5, 0.5, 2), bewegung=[[0, 0.5, 0.5], ['@minus', 0.5, 0.5], ['@zusammen', 0.5, -1.5],
                                                               ['@anderen', 0.5, -1.5], ['@Widerspruch', 0.5, -3]])], ein=0.05)),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Bleibt ein Widerspruch wie null gleich zwei, ist die Lösungsmenge leer, die Geraden sind parallel. Bleibt null gleich null, gibt es unendlich viele Lösungen, die Geraden sind identisch.',
            titel('Zum Mitnehmen', 250, 76),
            n('Widerspruch wie @0 = 2@: @\\mathbb{L} = \\{\\,\\}@, parallel|@0 = 0@: unendlich viele, identisch', 400, 'blau', 46, ein=1.2)),
         JETZT_DU_ANIM,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
d43, b43 = abc('Frage 3', 'y = 3x − 1 und 6x − 2y = 2 ergeben 0 = 0. Wie heisst die Lösungsmenge?',
               ['Paare auf der Geraden', 'alle Zahlen', 'ein Punkt'],
               [r'\mathbb{L} = \{(x \mid 3x - 1) : x \in \mathbb{R}\}', r'\mathbb{L} = \mathbb{R}', r'\mathbb{L} = \{(0 \mid -1)\}'], 0,
               {0: 'Ja.', 1: 'Lösungen sind Zahlenpaare, und nur die auf der gemeinsamen Geraden.',
                2: '(0 | −1) ist eine Lösung, aber nicht die einzige: Setz x = 1 ein.'},
               sprich='y gleich drei x minus eins und sechs x minus zwei y gleich zwei ergeben null gleich null. Wie heisst die Lösungsmenge?',
               rueck_sprich={1: 'Lösungen sind Zahlenpaare, und nur die auf der gemeinsamen Geraden.',
                             2: 'Null und minus eins ist eine Lösung, aber nicht die einzige. Setz x gleich eins ein.'})
clip('kontrolle-faelle', 'Gleichungssysteme lösen: Kontrollfragen zu den Lösungsfällen',
     'Fünf Fragen: 0 = 7 deuten, identische und parallele Geraden erkennen, die Lösungsmenge bei 0 = 0 und ein Parameter k.',
     ['Lösungsfälle', 'Parameter', 'Kontrollfragen'], [
         sz('Frage 1',
            'Null gleich sieben ist falsch, für jedes Paar. Es gibt keine Lösung: Die Lösungsmenge ist leer, die Geraden sind parallel.',
            f(r'0 = 7 \quad \fd{\text{falsch}}', 300, 56, ein='@falsch'),
            f(r'\mathbb{L} = \{\,\}', 420, 56, ein='@leer')),
         sz('Frage 2',
            'Die erste Gleichung ist das Dreifache der zweiten, auch rechts: drei mal drei ist neun. Dieselbe Gerade, unendlich viele Lösungen.',
            f(r'6x + 3y = 9 \;\text{ ist } 3 \cdot (2x + y = 3)', 300, 50, ein='@Dreifache'),
            f(r'\text{identisch: unendlich viele Lösungen}', 420, 48, ein='@Dieselbe'),
            graf(W4, geraden=[G(-2, 3, 1, dicke=9), G(-2, 3, 2, gestrichelt=True, dicke=3)], ein='@Dieselbe')),
         sz('Frage 3',
            'Lösungen sind die Paare auf der gemeinsamen Geraden: x beliebig, y gleich drei x minus eins. Nicht alle Zahlen und nicht nur ein Punkt.',
            *b43,
            f(r'\mathbb{L} = \{(x \mid 3x - 1) : x \in \mathbb{R}\}', 300, 52, ein='@Paare'),
            graf(W4, geraden=[G(3, -1, 1, dicke=9, laeufer={'bahn': [['@beliebig', 0], ['@Punkt', 1.5]], 'farbe': 5}),
                              G(3, -1, 2, gestrichelt=True, dicke=3)], ein='@Paare')),
         sz('Frage 4',
            'Gleiche Steigung zwei, verschiedene Achsenabschnitte: parallele Geraden, keine Lösung.',
            f(r'\text{Steigung } 2 \text{ und } 2', 300, 50, ein='@Steigung'),
            f(r'\text{parallel: } \mathbb{L} = \{\,\}', 420, 50, ein='@parallele'),
            graf(W4, geraden=[G(2, 1, 1), G(2, -3, 2)], ein='@Steigung')),
         sz('Frage 5',
            'Links ist die zweite Gleichung das Doppelte der ersten. Rechts muss dann auch das Doppelte stehen: k gleich zwei.',
            f(r'4x + 2y = 2 \cdot (2x + y)', 300, 50, ein='@Doppelte'),
            f(r'k = 2 \cdot 1 = \fc{2}', 420, 52, ein='@Rechts'),
            graf(W4, geraden=[G(-2, 1, 1, dicke=9), G(-2, 1, 2, gestrichelt=True, dicke=3)], ein='@Rechts')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Ist eine Gleichung links ein Vielfaches der anderen, sind die Geraden parallel oder identisch. Dann entscheidet die rechte Seite.',
            titel('Zum Mitnehmen', 250, 76),
            n('links ein Vielfaches: parallel oder identisch|die rechte Seite entscheidet', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Beim Eliminieren bleibt 0 = 7. Welche Lösungsmenge?',
              ['𝕃 = { }', '𝕃 = {(0 | 7)}', '𝕃 = ℝ'], 0,
              {0: 'Ja.', 1: 'In 0 = 7 kommt weder x noch y vor. Ist die Aussage wahr?', 2: 'Ist 0 = 7 wahr oder falsch?'},
              sprich='Beim Eliminieren bleibt null gleich sieben. Welche Lösungsmenge?',
              rueck_sprich={1: 'In null gleich sieben kommt weder x noch y vor. Ist die Aussage wahr?', 2: 'Ist null gleich sieben wahr oder falsch?'}),
         wahl('Frage 2', '6x + 3y = 9 und 2x + y = 3: Wie viele Lösungen?',
              ['unendlich viele', 'keine', 'genau eine'], 0,
              {0: 'Ja.', 1: 'Rechne die rechte Seite mit: 3 · 3 = ?', 2: 'Vergleiche die Zahlen vor x und y: Ist (I) ein Vielfaches von (II)?'},
              sprich='Sechs x plus drei y gleich neun und zwei x plus y gleich drei: Wie viele Lösungen?',
              rueck_sprich={1: 'Rechne die rechte Seite mit: drei mal drei gibt?', 2: 'Vergleiche die Zahlen vor x und y: Ist die erste ein Vielfaches der zweiten?'}),
         d43,
         wahl('Frage 4', 'y = 2x + 1 und y = 2x − 3: Wie viele Lösungen, ohne das System zu lösen?',
              ['keine', 'genau eine', 'unendlich viele'], 0,
              {0: 'Ja.', 1: 'Vergleiche die Steigungen.', 2: 'Vergleiche die Achsenabschnitte.'},
              sprich='y gleich zwei x plus eins und y gleich zwei x minus drei: Wie viele Lösungen, ohne das System zu lösen?'),
         wahl('Frage 5', '2x + y = 1 und 4x + 2y = k: Für welches k sind die Geraden identisch?',
              ['k = 2', 'k = 1', 'k = 4'], 0,
              {0: 'Ja.', 1: 'Links steht in (II) das Doppelte von (I). Rechts auch?', 2: 'Das Doppelte von 1 ist nicht 4.'},
              sprich='Zwei x plus y gleich eins und vier x plus zwei y gleich k: Für welches k sind die Geraden identisch?',
              rueck_sprich={1: 'Links steht in der zweiten Gleichung das Doppelte der ersten. Rechts auch?', 2: 'Das Doppelte von eins ist nicht vier.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
SYS3 = system('x + y + z = 6', '2x - y + z = 3', 'x + 2y - z = 2')
clip('drei', 'Gleichungssysteme lösen: drei Variablen, zurück auf zwei',
     'Ein System mit drei Variablen: zweimal dieselbe Variable eliminieren, das 2×2-System lösen, zurück einsetzen, Probe — und was 0 = 5 bedeutet.',
     ['Gleichungssystem', 'drei Variablen', 'eliminieren'], [
         sz('Drei Gleichungen',
            'Drei Variablen, drei Gleichungen: x plus y plus z gleich sechs, zwei x minus y plus z gleich drei, x plus zwei y minus z gleich zwei. '
            'Die Idee: eine Variable eliminieren, bis ein System mit zwei Variablen bleibt.',
            titel('Drei Variablen', 230, 70),
            f(SYS3, 420, 54, ein='@Drei'),
            n('3 Variablen @\\rightarrow@ 2 Variablen', 700, 'blau', 46, ein='@Idee')),
         sz('z eliminieren',
            'Vor z steht in der dritten Gleichung minus eins. Die erste plus die dritte: zwei x plus drei y gleich acht. '
            'Die zweite plus die dritte: drei x plus y gleich fünf. Beide Male fällt z weg.',
            f(SYS3, 280, 50, ein=0.3),
            f(r'\text{(I)} + \text{(III)}:\;\; 2x + 3y = 8 \qquad \text{(IV)}', 520, 48, ein='@erste'),
            f(r'\text{(II)} + \text{(III)}:\;\; 3x + y = 5 \qquad \text{(V)}', 610, 48, ein='@zweite'),
            n('Beide Male fällt @z@ weg.', 730, 'blau', 44, ein='@Beide')),
         sz('Das 2×2-System',
            'Jetzt bleibt ein System mit x und y. Die vierte minus dreimal die fünfte: minus sieben x gleich minus sieben, also x gleich eins. '
            'In die fünfte eingesetzt: drei plus y gleich fünf, y gleich zwei.',
            f(system('2x + 3y = 8', '3x + y = 5', lab=('IV', 'V')), 280, 52, ein=0.3),
            f(r'\text{(IV)} - 3 \cdot \text{(V)}:\;\; -7x = -7', 480, 46, ein='@minus'),
            f(r'x = \fc{1}', 480, 46, ein='@also', x=LX + 620),
            f(r'3 + y = 5', 580, 48, ein='@eingesetzt'),
            f(r'y = \fc{2}', 580, 48, ein='@zwei', x=LX + 380)),
         sz('Zurück einsetzen',
            'x und y in die erste Gleichung: eins plus zwei plus z gleich sechs, also z gleich drei. Die Lösung ist ein Tripel: eins, zwei, drei.',
            f(r'1 + 2 + z = 6', 300, 52, ein='@eins'),
            f(r'z = \fc{3}', 300, 52, ein='@also', x=LX + 380),
            f(r'\mathbb{L} = \{(\fc{1} \mid \fc{2} \mid \fc{3})\}', 440, 58, ein='@Tripel')),
         sz('Die Probe',
            'Probe in allen drei Gleichungen: Eins plus zwei plus drei gibt sechs. Zwei minus zwei plus drei gibt drei. Und eins plus vier minus drei gibt zwei.',
            f(r'\text{(I)}\;\; 1 + 2 + 3 = 6 \;\fc{\checkmark}', 300, 50, ein='@gibt'),
            f(r'\text{(II)}\;\; 2 - 2 + 3 = 3 \;\fc{\checkmark}', 400, 50, ein='@gibt#2'),
            f(r'\text{(III)}\;\; 1 + 4 - 3 = 2 \;\fc{\checkmark}', 500, 50, ein='@gibt#3')),
         sz('Wenn nichts übrig bleibt',
            'Fällt beim Eliminieren alles weg, entscheidet die Aussage, die bleibt. Null gleich fünf: Widerspruch, keine Lösung. '
            'Null gleich null sagt nichts Neues. Entsteht nirgends ein Widerspruch, gibt es unendlich viele Lösungen.',
            f(r'0 = 5:\;\; \fd{\text{Widerspruch}},\ \mathbb{L} = \{\,\}', 320, 50, ein='@Widerspruch'),
            f(r'0 = 0:\;\; \text{sagt nichts Neues}', 440, 50, ein='@Neues'),
            n('nirgends ein Widerspruch:|unendlich viele Lösungen', 560, 'blau', 44, ein='@nirgends')),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Zweimal dieselbe Variable eliminieren, das System mit zwei Variablen lösen, zurück einsetzen und die Probe in allen drei Gleichungen.',
            titel('Zum Mitnehmen', 250, 76),
            n('zweimal dieselbe Variable eliminieren|→ 2×2 lösen → zurück einsetzen|→ Probe in allen drei Gleichungen', 400, 'blau', 46, ein=1.2)),
         JETZT_DU_UF,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
d52, b52 = abc('Frage 2', 'Welche zwei Gleichungen addierst du, damit z wegfällt?',
               ['(I) + (III)', '(I) + (II)', '(II) + (III)'],
               [r'\text{(I)} + \text{(III)}', r'\text{(I)} + \text{(II)}', r'\text{(II)} + \text{(III)}'], 0,
               {0: 'Ja.', 1: 'Vor z stehen in (I) und (II) +1 und +3 — beim Addieren bleibt z.', 2: 'Vor z stehen +3 und −1 — beim Addieren bleibt z.'},
               rueck_sprich={1: 'Vor z stehen in der ersten und zweiten Gleichung plus eins und plus drei. Beim Addieren bleibt z.',
                             2: 'Vor z stehen plus drei und minus eins. Beim Addieren bleibt z.'}, y0=700)
d55, b55 = abc('Frage 5', 'Ist (1 | 0 | 2) eine Lösung dieses Systems?',
               ['Nein, (III) nicht', 'Ja, alle stimmen', 'Nein, (I) nicht'],
               [r'\text{Nein, (III) stimmt nicht.}', r'\text{Ja, alle drei stimmen.}', r'\text{Nein, (I) stimmt nicht.}'], 0,
               {0: 'Ja.', 1: 'Setz auch in (III) ein: 2 · 1 + 0 − 2 = ?', 2: 'Setz nochmals in (I) ein: 1 + 0 + 2 = ?'},
               sprich='Ist eins, null, zwei eine Lösung dieses Systems?',
               rueck_sprich={1: 'Setz auch in die dritte Gleichung ein: zwei mal eins plus null minus zwei gibt?', 2: 'Setz nochmals in die erste Gleichung ein: eins plus null plus zwei gibt?'}, y0=700)
clip('kontrolle-drei', 'Gleichungssysteme lösen: Kontrollfragen zu drei Variablen',
     'Fünf Fragen: zwei Gleichungen addieren, das passende Paar zum Eliminieren wählen, zurück einsetzen, 0 = 3 deuten, Probe mit einem Tripel.',
     ['drei Variablen', 'eliminieren', 'Kontrollfragen'], [
         sz('Frage 1',
            'x plus x ist zwei x. y minus y ist null. z plus zwei z ist drei z. Rechts sechs plus fünf ist elf. Also zwei x plus drei z gleich elf.',
            f(r'2x + 0y + 3z = 11', 300, 52, ein='@null'),
            f(r'2x + 3z = 11', 400, 52, ein='@Also')),
         sz('Frage 2',
            'Vor z stehen in der ersten Gleichung plus eins und in der dritten minus eins. Die erste plus die dritte: zwei x plus drei y gleich eins.',
            *b52,
            gegeben(f(system('x + y + z = 4', '2x - y + 3z = 14', 'x + 2y - z = -3'), 330, 50, ein=0.05)),
            f(r'\text{(I)} + \text{(III)}:\;\; 2x + 3y = 1', 300, 50, ein='@erste#2', x=RX)),
         sz('Frage 3',
            'Zwei plus minus eins plus z gleich vier: eins plus z gleich vier, also z gleich drei.',
            f(r'2 + (-1) + z = 4', 300, 52, ein=1.0),
            f(r'z = \fc{3}', 400, 52, ein=4.5)),   # Whisper bricht hier ab (Energie des Tons: Sprache bis 5.5 s)
         sz('Frage 4',
            'Null gleich drei ist falsch, egal welche Zahlen man einsetzt. Das System hat keine Lösung.',
            f(r'0 = 3 \quad \fd{\text{falsch}}', 300, 56, ein='@falsch'),
            f(r'\mathbb{L} = \{\,\}', 420, 56, ein='@keine')),
         sz('Frage 5',
            'Erste Gleichung: eins plus null plus zwei gibt drei. Zweite: auch drei. Dritte: zwei plus null minus zwei gibt null, nicht eins. Keine Lösung des Systems.',
            *b55,
            gegeben(f(system('x + y + z = 3', 'x - y + z = 3', '2x + y - z = 1'), 330, 50, ein=0.05)),
            f(r'\text{(III)}\;\; 2 + 0 - 2 = 0 \fd{\;\neq 1}', 300, 48, ein='@Dritte', x=RX)),
         sz('Zum Mitnehmen',
            'Zum Mitnehmen: Wähle die Gleichungen so, dass dieselbe Variable wegfällt, und prüfe ein Tripel in allen drei Gleichungen.',
            titel('Zum Mitnehmen', 250, 76),
            n('dieselbe Variable eliminieren|Probe in allen drei Gleichungen', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', '(x + y + z = 6) plus (x − y + 2z = 5) ergibt …',
              ['2x + 3z = 11', '2x + 2y + 3z = 11', '2x + 3z = 1'], 0,
              {0: 'Ja.', 1: 'y + (−y) = ?', 2: 'Rechts wird addiert: 6 + 5.'},
              sprich='Die Gleichung x plus y plus z gleich sechs plus die Gleichung x minus y plus zwei z gleich fünf ergibt?',
              rueck_sprich={1: 'y plus minus y gibt?', 2: 'Rechts wird addiert: sechs plus fünf.'}),
         d52,
         wahl('Frage 3', 'Gefunden: x = 2 und y = −1. Mit x + y + z = 4 ist z gleich …',
              ['3', '1', '5'], 0,
              {0: 'Ja.', 1: 'Vorzeichen bei y: z = 4 − 2 − (−1), und −(−1) = +1.', 2: 'Vorzeichen beim Freistellen: z = 4 − 2 − (−1), nicht 4 + 2 − 1.'},
              sprich='Gefunden: x gleich zwei und y gleich minus eins. Mit x plus y plus z gleich vier ist z gleich?',
              rueck_sprich={1: 'Vorzeichen bei y: z gleich vier minus zwei minus minus eins, und minus minus eins ist plus eins.', 2: 'Vorzeichen beim Freistellen: z gleich vier minus zwei minus minus eins, nicht vier plus zwei minus eins.'}),
         wahl('Frage 4', 'Beim Eliminieren bleibt 0 = 3. Wie viele Lösungen hat das System?',
              ['keine', 'genau eine', 'unendlich viele'], 0,
              {0: 'Ja.', 1: 'In 0 = 3 kommt keine Variable vor. Ist die Aussage wahr?', 2: 'Ist 0 = 3 wahr oder falsch?'},
              sprich='Beim Eliminieren bleibt null gleich drei. Wie viele Lösungen hat das System?',
              rueck_sprich={1: 'In null gleich drei kommt keine Variable vor. Ist die Aussage wahr?', 2: 'Ist null gleich drei wahr oder falsch?'}),
         d55,
     ], art='Kontrollclip')

if NEU_TON or NEU_FRAGEN:
    print('NEU VERTONEN — Szenen:', NEU_TON, '— Fragetöne:', NEU_FRAGEN)
if FEHLT:
    print('geschätzte Zeiten (kein gemessenes Wort):', len(FEHLT))
