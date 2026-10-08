"""Bausteine für die Drehbücher des Leitprogramms Modellieren (08.10.2026) — von clips.py benutzt.

Layout der Kontrollclips (1920 × 1080, Fragekasten des Abspielers links unten ab y = 560):
  Kopfzeile y 150      Fahrplan «① Deklaration ② Ansatz ③ Grundform ④ Lösen ⑤ Antwort», der laufende Schritt blau
  rechts x 1000        Aufgabentext (y 200 bis rund 470), darunter die Auflösung des Schritts (ab y 500)
  links  x 150         das Gegebene aus den früheren Schritten (y 200 bis 540) — über dem Fragekasten
Beim Erscheinen der Frage (bei 0.3 s) steht nur das Gegebene da (HOWTO-leitprogramme §15, Fragebild);
die Auflösung kommt mit dem Satz, der sie nennt (`ein` als «@wort», aus den gemessenen Wortzeiten).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = erste Unbekannte (x, z, n, m, r, K) und ihre Sorte     \\fa{…}
  2 orange = zweite Unbekannte (y, e, p) und ihre Sorte              \\fb{…}
  3 grün   = Lösung, Ergebnis, Probe stimmt                          \\fc{…}
  4 rot    = Fehler, verworfene Lösung                               \\fd{…}
  5 Tinte  = neutral
"""
import difflib
import importlib.util
import json
import os
import re
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
PRAEFIX = 'g2-M-lp-'
LX, RX = 150, 1000
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []
NEU_TON = []       # (clip, Szenen-Nr. ab 1) mit neuem Sprechertext — für build-clip-ton.py --szenen
NEU_FRAGEN = []    # (clip, '3' oder '3:r1') mit neuem Fragetext — für build-clip-fragen-ton.py --fragen
NB = ' '           # schmales geschütztes Leerzeichen als Tausendertrenner im Klartext (Fragen)


# ---------------------------------------------------------------- Zahlen als Wörter (Sprechertext)
EINER = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'elf', 'zwölf',
         'dreizehn', 'vierzehn', 'fünfzehn', 'sechzehn', 'siebzehn', 'achtzehn', 'neunzehn']
ZEHNER = ['', '', 'zwanzig', 'dreissig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig']


def _unter100(n, ein=False):
    if n < 20:
        return 'ein' if (n == 1 and ein) else EINER[n]
    z, e = divmod(n, 10)
    return ZEHNER[z] if e == 0 else ('ein' if e == 1 else EINER[e]) + 'und' + ZEHNER[z]


def _unter1000(n, ein=False):
    h, r = divmod(n, 100)
    s = ('' if h == 0 else ('hundert' if h == 1 else EINER[h] + 'hundert'))
    if r:
        s += _unter100(r, ein=ein or bool(h))
    return s


def zw(n):
    """Ganze Zahl in Worten (Schweizer Schreibung, ss)."""
    n = int(n)
    if n < 0:
        return 'minus ' + zw(-n)
    if n == 0:
        return 'null'
    teile = []
    mio, r = divmod(n, 1000000)
    if mio:
        teile.append('eine Million' if mio == 1 else _unter1000(mio) + ' Millionen')
    tsd, r = divmod(r, 1000)
    s = ''
    if tsd:
        s += ('tausend' if tsd == 1 else _unter1000(tsd, ein=True) + 'tausend')
    if r:
        s += _unter1000(r)
    if s:
        teile.append(s)
    return ' '.join(teile)


def zk(s):
    """Dezimalzahl aus Text («0.015», «-2.42») in Worten: «null Komma null eins fünf»."""
    s = str(s)
    neg = s.startswith('-')
    s = s.lstrip('-')
    if '.' in s:
        g, d = s.split('.')
        t = zw(int(g)) + ' Komma ' + ' '.join(EINER[int(c)] for c in d)
    else:
        t = zw(int(s))
    return ('minus ' if neg else '') + t


# ---------------------------------------------------------------- Zeiten auf den Ton
SPRECH = {}
ZAHL = {}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower())
    w_ = wort.lower()
    if not g:
        return False
    if w_.isdigit():
        return g == w_
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    return (len(w_) >= 5 and w_[0] == g[0] and abs(len(w_) - len(g)) <= 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.7)


def wann(clip, szene, wort, nr=1, dazu=0.0):
    """Sekunde ab Szenenbeginn, zu der `wort` zum nr-ten Mal beginnt (Wortzeiten von faster-whisper,
    wortzeiten.py). Ohne Messung geschätzt aus der Lage des Wortes im Sprechertext."""
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
        # Whisper hat das Wort verhört («rober» für Probe): die Lage des Wortes im Sprechertext auf die
        # gemessenen Wörter übertragen (Zahlen schreibt Whisper als Ziffern, darum Wortanteil statt Zeichen).
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
    """Ersetzt `ein`/`aus` der Form «@wort», «@wort#2» oder «@wort+0.3» durch Sekunden."""
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
            for art in ('figuren', 'punkte', 'strecken', 'flaechen', 'texte', 'kurven', 'geraden'):
                for k in el.get(art) or []:
                    for z in ('ein', 'aus'):
                        if z in k:
                            k[z] = lös(q['name'], k[z])
                    if 'bewegung' in k:
                        k['bewegung'] = [[lös(q['name'], b[0])] + b[1:] for b in k['bewegung']]


# ---------------------------------------------------------------- Elemente
def f(t, y, g=46, ein=0.05, x=LX, **kw):
    d = dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein, abstand=0)
    d.update(kw)
    return d


def tx(t, y, g=34, ein=0.05, x=LX, **kw):
    d = dict(typ='text', text=t, x=x, y=y, groesse=g, ein=ein, abstand=0)
    d.update(kw)
    return d


def n(t, y, farbe='blau', g=38, ein=0.05, x=LX, **kw):
    d = dict(typ='notiz', text=t, x=x, y=y, groesse=g, farbe=farbe, ein=ein, abstand=0)
    d.update(kw)
    return d


def titel(t, y=280, g=80, ein=0.05):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g, ein=ein, abstand=0)


def rechner(zeilen, tasten, y, ein, x=RX, breite=560, **kw):
    d = dict(typ='rechner', breite=breite, zeilen=zeilen, tasten=tasten, x=x, y=y, ein=ein, anim='fade', abstand=0)
    d.update(kw)
    return d


def stapel(schirme, y, ein0, schritt=1.1, x=RX, breite=560):
    """Tastenfolge: mehrere Anzeigen an derselben Stelle, jede verdeckt die vorige (HOWTO-clips)."""
    n_ = max(len(z) for z, _ in schirme)
    aus = []
    for i, (zeilen, tasten) in enumerate(schirme):
        zl = list(zeilen) + [''] * (n_ - len(zeilen))
        if isinstance(ein0, str):
            wort, _, dazu = ein0.partition('+')
            ein = wort + '+%.2f' % (float(dazu or 0) + i * schritt)
        else:
            ein = ein0 + i * schritt
        aus.append(rechner(zl, tasten, y, ein, x, breite))
    return aus


def sz(name, spr, *el, **kw):
    d = dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=[e for e in el if e])
    d.update(kw)
    return d


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


_BC = []


def _fragen_texte(F):
    # dieselbe Liste wie fragen_texte() in build-clips.py (dort geholt, nicht nachgebaut)
    if not _BC:
        spec = importlib.util.spec_from_file_location('bc', R + 'scripts/build-clips.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _BC.append(m)
    return [(k, g) for k, _, g in _BC[0].fragen_texte(F)]


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip', folge=None):
    zeiten(name, szenen)
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
                # Text geändert: die alte dauer bleibt stehen, bis build-clip-ton.py --szenen neu misst (das Skript
                # braucht die alten Dauern, um die übrigen Szenen aus der bisherigen Spur zu schneiden).
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
         'schlagworte': schlag, 'themenbereich': 'Algebra · Textaufgaben',
         'fach': 'Grundlagenfach', 'lerngebiet': '2 · Gleichungen, Ungleichungen und Gleichungssysteme',
         'lektion': ['g2-M'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Ansatz finden',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms modellieren; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if folge:
        d['folge'] = folge
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(pfad, 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der Animation unter dem Clip und löse die Aufgaben.',
              titel('Jetzt du', 300, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 450, 'blau', 50, ein=0.6))


# ---------------------------------------------------------------- Kontrollclips: Aufgabe in fünf Schritten
SCHRITTE = ['Deklaration', 'Ansatz', 'Grundform', 'Lösen', 'Antwort']
KREIS = ['①', '②', '③', '④', '⑤']


def fahrplan(k, nr):
    """Kopfzeile: Aufgabe und die fünf Schritte; erledigte normal, der laufende blau, kommende blass."""
    t = []
    for i, s in enumerate(SCHRITTE, 1):
        w = KREIS[i - 1] + ' ' + s
        t.append('{1:' + w + '}' if i == k else ('~' + w + '~' if i > k else w))
    return tx('Aufgabe %d   ' % nr + '   '.join(t), 140, 30)


def gegeben(zeilen, y0=210):
    """Das Gegebene links oben: Liste von Elementfabriken (y) → Elemente; Höhen je Typ."""
    out, y = [], y0
    for z in zeilen:
        el, h = z(y)
        out.append(el)
        y += h
    assert y <= 560, ('Gegebenes reicht in den Fragekasten', y)
    return out


def G_text(t, g=36):
    return lambda y: (tx(t, y, g), int(g * 1.75))


def G_formel(t, g=40, h=None):
    return lambda y: (f(t, y, g), h or int(g * 1.9))


def aufgabe_text(t, g=36):
    return tx(t, 200, g, x=RX)


def auto_tex(o):
    """Ein Angebot, das eine Gleichung ist («22·e² + 62·e − 600 = 0», «… und …»), im Bild mit Formelsatz;
    Prosa bleibt Text."""
    woerter = [w for w in re.findall(r'[A-Za-zÄÖÜäöü]{3,}', o) if w != 'und']
    if '=' not in o or woerter:
        return o
    t = o.replace('·', ' \\cdot ').replace('²', '^2').replace('−', '-').replace('\u202f', '\\,').replace('½', '\\tfrac{1}{2}').replace(' %', '\\,\\%')
    t = ' \\text{ und } '.join(t.split(' und '))
    # Einheiten aufrecht und mit Abstand (Prüfung 08.10.2026: «35 kg» stand kursiv als Produkt k · g)
    t = re.sub(r'(?<=\d) (kg|l|CHF)\b', r'\\,\\text{\1}', t)
    return '@' + t + '@'


def abc(szene, q, kopf):
    """Wahlfrage mit den Angeboten im Bild (rechts, ab y = q['y'] oder 540), gedreht wie wahl()."""
    opt, n_ = q['opt'], len(q['opt'])
    k = zlib.crc32((szene + '|' + q['text']).encode('utf-8')) % n_
    reihe = [(j + k) % n_ for j in range(n_)]          # angezeigte Stelle j → ursprüngliches Angebot
    marken = 'ABCD'[:n_]
    y0 = q.get('y', 540)
    bild = []
    for j, i in enumerate(reihe):
        zeigen = ('@' + q['tex'][i] + '@') if q.get('tex') else auto_tex(opt[i])
        g = q.get('g', 38 if max(len(o) for o in opt) <= 28 else 34)
        bild.append(tx('{2:' + marken[j] + '}\u2003' + zeigen, y0 + j * 84, g, x=RX, ein=0.05, aus=0.9))
    richtig = q.get('richtig', 0)
    d = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'kopf': kopf, 'text': q['text'], 'optionen': list(marken),
         'richtig': reihe.index(richtig),
         'rueck': {str(j): q['rueck'][i] for j, i in enumerate(reihe) if i != richtig},
         'sprich': (q.get('sprich') or q['text']) + ' A, B oder C?'}
    if q.get('rueck_sprich'):
        d['rueck_sprich'] = {str(j): q['rueck_sprich'].get(i, q['rueck'][i]) for j, i in enumerate(reihe) if i != richtig}
    return d, bild


def kontrolle(name, titel_, kurz, schlag, aufgaben, merke, folge=None):
    """aufgaben: Liste von dict(nr, kurz (Kopf), text (Anzeige, | bricht), spr (gesprochen), schritte=[5 dict]).
    Schritt: gegeben (Liste G_…), frage (text, sprich, optionen, richtig, rueck {i: text}, rueck_sprich),
             spr (Auflösung, gesprochen), el (Auflösung, Elemente mit ein ≥ 1 oder «@wort»)."""
    szenen, fragen = [], []
    for A in aufgaben:
        szenen.append(sz('A%d Text' % A['nr'], A['spr'],
                         fahrplan(0, A['nr']),
                         titel('Aufgabe %d' % A['nr'], 300, 80),
                         n(A['kurz'], 420, 'blau', 46, ein=0.4),
                         aufgabe_text(A['text'])))
        for k, S in enumerate(A['schritte'], 1):
            sname = 'A%d %s' % (A['nr'], SCHRITTE[k - 1])
            el = [fahrplan(k, A['nr']), aufgabe_text(A['text'])] + gegeben(S.get('gegeben', [])) + S['el']
            for e in S['el']:
                ein = e.get('ein', 0)
                assert isinstance(ein, str) or ein >= 1.0 or e.get('_gegeben'), (sname, 'Auflösung vor der Antwort', e)
            szenen.append(sz(sname, S['spr'], *el))
            q = S['frage']
            kopf = 'Schritt %s %s' % (KREIS[k - 1], SCHRITTE[k - 1])
            if max(len(o) for o in q['opt']) > 18 or q.get('tex'):
                # Lange Angebote stehen als A, B, C im Bild (mit Formelsatz), die Knöpfe heissen nur A, B, C:
                # So bleibt der Fragekasten einzeilig und ragt auch mit Rückmeldung nicht über die Bühne.
                q.setdefault('y', 770 if any(e.get('_gegeben') for e in S['el']) else 540)
                fr, angebote = abc(sname, q, kopf)
                szenen[-1]["elemente"][2:2] = angebote
                fragen.append(fr)
            else:
                fragen.append(wahl(sname, q['text'], q['opt'], q.get('richtig', 0), q['rueck'], q.get('sprich'),
                                   q.get('rueck_sprich'), kopf=kopf))
    szenen.append(merke)
    texte = [F_['text'][:20] for F_ in fragen]
    assert len(set(texte)) == len(texte), ('Fragen beginnen gleich (pruef-fragen erkennt sie an 20 Zeichen)',
                                           [t for t in texte if texte.count(t) > 1])
    clip(name, titel_, kurz, schlag, szenen, fragen, art='Kontrollclip', folge=folge)
