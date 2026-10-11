"""Erzeugt die zehn Drehbücher des Leitprogramms Lineare Gleichungen (GF 2.2a, 11.10.2026).

  python3 scripts/lp/lineare-gleichungen/clips.py

Clips `g2-2a-lp-*`, Reihe «Lineare Gleichungen lösen», Theme `begreifbar-schlicht`, alle `"probe": true`.
Je Kapitel ein Einführungsclip und ein Kontrollclip (HOWTO-leitprogramme §7).

Zeiten auf dem Ton: Einblendungen und Bewegungsstützpunkte stehen als Anker '@wort' (erstes Wort, das so
beginnt), '@wort#2' (zweites Vorkommen), '@wort+0.6' / '@wort-0.3' (versetzt) oder '@wort>' (Wortende).
`sz()` löst sie auf: mit den gemessenen Wortzeiten aus `wortzeiten.json` (scripts/lp/lineare-gleichungen/
wortzeiten.py, faster-whisper), solange der Sprechertext der Szene dort unverändert steht — sonst mit einer
Schätzung aus der Lage im Text (14 Zeichen je Sekunde ab 0.4 s). Anker nie auf Zahlwörter legen: Whisper
schreibt sie als Ziffern (HOWTO §15).

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich). Darum darf es
nach der Vertonung erneut laufen; nur Szenen mit neuem Text brauchen danach build-clip-ton.py --szenen.

Aufbau wie im Leitprogramm Lineare und quadratische Gleichungen: Umformungskette links (x 150), die
Operation rechts neben der Zeile wie im Heft («| −2x», x 700), ein Bild rechts (x 1010, y 175, 760 × 760).
Der Graph zeigt beide Seiten als Geraden (links blau, rechts orange): Jede Äquivalenzumformung verändert
beide, ihr Schnittpunkt — die Lösung — bleibt stehen. Er unterstützt, er ersetzt die Rechnung nicht.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Gleichung, linke Seite (Gerade)          \\fa{…}
  2 orange = die Umformung («| −2x»), Parameter k,      \\fb{…}
             rechte Seite einer Gleichung im Graph
  3 grün   = Lösungen, Lösungsmenge                    \\fc{…}
  4 rot    = Fehler                                     \\fd{…}
  5 Tinte  = neutral (Differenz links − rechts, Bezugslinien)

Fragebild (HOWTO §15): Beim Erscheinen einer Frage zeigt das Bild nur das Gegebene — in den Formel-Szenen
erscheint alles ab 1.0 s (nach der Antwort), in den Graf-Fragen nur die Geraden, die die Frage «im Bild» gibt.
"""
import difflib
import json
import os
import re
import zlib

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
PREFIX = 'g2-2a-lp-'
GX, GY, GB, GH, LX, OX = 1010, 175, 760, 760, 150, 700
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
CLIP = None          # Name des Clips, dessen Szenen gerade entstehen (für die Wortzeiten)
UNAUFGELOEST = []


def _norm(w):
    return re.sub(r'[^a-zäöüéè0-9]', '', w.lower())


_EINER = {'null': 0, 'ein': 1, 'eins': 1, 'eine': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5, 'sechs': 6, 'sieben': 7,
          'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12, 'sechzehn': 16, 'siebzehn': 17}
_ZEHNER = {'zwanzig': 20, 'dreissig': 30, 'vierzig': 40, 'fünfzig': 50, 'sechzig': 60, 'siebzig': 70, 'achtzig': 80,
           'neunzig': 90}


def _zahl(w):
    """Deutsches Zahlwort bis 999 → Ziffern (Whisper schreibt Zahlen als Ziffern), sonst None."""
    if w in _EINER:
        return _EINER[w]
    if w in _ZEHNER:
        return _ZEHNER[w]
    if w.startswith('hundert'):
        r = w[7:]
        return 100 if not r else (100 + _zahl(r) if _zahl(r) is not None else None)
    for e, v in _EINER.items():
        if w.startswith(e + 'hundert'):
            r = w[len(e) + 7:]
            return v * 100 if not r else (v * 100 + _zahl(r) if _zahl(r) is not None else None)
    if w.endswith('zehn') and w[:-4] in ('drei', 'vier', 'fünf', 'acht', 'neun'):
        return 10 + _EINER[w[:-4]]
    if 'und' in w:
        a, b = w.split('und', 1)
        if a in _EINER and b in _ZEHNER:
            return _ZEHNER[b] + _EINER[a]
    return None


def _token_s(w):
    n = _norm(w)
    z = _zahl(n)
    return [str(z)] if z is not None else [n]


def _token_w(w):
    n = _norm(w)
    return [t for t in re.split(r'(?<=\d)(?=[a-z])|(?<=[a-z])(?=\d)', n) if t]


def _anker(szene, spr, a):
    """'@wort#n+dt' → Sekunden ab Szenenbeginn. Gesucht wird das n-te Wort des Sprechertexts, das so beginnt;
    seine Zeit kommt aus den Wortzeiten über eine Zuordnung Sprechertext ↔ Whisper (difflib). Hat Whisper das
    Wort anders geschrieben («beizahdig», «2» für «zwei»), wird zwischen den Nachbarn interpoliert."""
    m = re.match(r'@([^#+\-<>]+)(?:#(\d+))?(>)?([+\-]\d+(?:\.\d+)?)?$', a)
    if not m:
        raise ValueError('Anker unlesbar: ' + a)
    wort, nr, ende, dt = _norm(m.group(1)), int(m.group(2) or 1), bool(m.group(3)), float(m.group(4) or 0)
    S = [_norm(w) for w in spr.split()]
    treffer = [i for i, w in enumerate(S) if w.startswith(wort)]
    if len(treffer) < nr:
        raise ValueError('%s / %s: Anker «%s» #%d nicht im Sprechertext' % (CLIP, szene, wort, nr))
    i = treffer[nr - 1]
    eintrag = WZ.get(CLIP, {}).get(szene)
    if eintrag and eintrag.get('sprecher') == spr and eintrag['woerter']:
        W0 = eintrag['woerter']
        # Token-Ebene: Zahlwörter als Ziffern, «2x» getrennt; je Token der Index des Worts
        St, Si, Wt, W = [], [], [], []
        for k, w in enumerate(spr.split()):
            for t in _token_s(w):
                St.append(t)
                Si.append(k)
        for w in W0:
            for t in _token_w(w[0]):
                Wt.append(t)
                W.append(w)
        zu = {}
        for blk in difflib.SequenceMatcher(None, St, Wt, autojunk=False).get_matching_blocks():
            for k in range(blk.size):
                zu.setdefault(Si[blk.a + k], blk.b + k)
        if i in zu:
            t0, t1 = W[zu[i]][1], W[zu[i]][2]
            return round((t1 if ende else t0) + dt, 2)
        vor = max([k for k in zu if k < i], default=None)
        nach = min([k for k in zu if k > i], default=None)
        if vor is not None and nach is not None:
            ta, tb = W[zu[vor]][2], W[zu[nach]][1]
            t = ta + (tb - ta) * (i - vor) / (nach - vor)
        elif vor is not None:
            t = W[zu[vor]][2] + 0.35 * (i - vor)
        elif nach is not None:
            t = max(0.3, W[zu[nach]][1] - 0.35 * (nach - i))
        else:
            t = None
        if t is not None:
            UNAUFGELOEST.append('%s / %s: «%s» #%d interpoliert (%.2f s)' % (CLIP, szene, wort, nr, t))
            return round(t + (0.35 if ende else 0) + dt, 2)
    # Schätzung aus der Lage im Text (vor der Vertonung)
    pos = sum(len(w) + 1 for w in spr.split()[:i])
    return round(0.4 + pos / 14.0 + (0.4 if ende else 0) + dt, 2)


def _aufloesen(o, szene, spr):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('ein', 'aus') and isinstance(v, str):
                o[k] = _anker(szene, spr, v)
            elif k in ('bewegung', 'bahn', 'farbwechsel') and isinstance(v, list):
                for st in v:
                    if isinstance(st, list) and st and isinstance(st[0], str):
                        st[0] = _anker(szene, spr, st[0])
                _aufloesen(v, szene, spr)
            else:
                _aufloesen(v, szene, spr)
    elif isinstance(o, list):
        for v in o:
            _aufloesen(v, szene, spr)


def graf(W, geraden=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             geraden=list(geraden), punkte=list(punkte), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def ger(m, q, farbe=1, gestrichelt=False, dicke=None, **kw):
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    d.update(kw)
    return d


def bew(stuetzen, farbe=1, **kw):
    d = {'bewegung': [list(s) for s in stuetzen], 'farbe': farbe}
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


def senkrecht(x, y0, y1, ein, farbe=3):
    """Gestrichelte Senkrechte bei der Lösung — dort bleibt der Schnittpunkt bei jeder Umformung."""
    return dict(von=[x, y0], bis=[x, y1], farbe=farbe, gestrichelt=True, ein=ein)


def f(t, y, g=52, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def op(t, y, ein, g=46, falsch=False):
    """Die Umformung rechts neben der Zeile, orange (wie im Heft); rot, wenn sie keine Äquivalenzumformung ist."""
    return f((r'\fd{\mid ' if falsch else r'\fb{\mid ') + t + '}', y, g, ein, OX)


def n(t, y, farbe='blau', g=44, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=80):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    s = dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))
    _aufloesen(s['elemente'], name, spr)
    if name.startswith('Frage'):
        # Fragebild (HOWTO §15): Die Frage steht bei 0.3 s; alle Formeln und Notizen links erscheinen erst nach der
        # Antwort (ab 1.0 s) und in der Reihenfolge des Drehbuchs, je mindestens 0.6 s nach der vorigen Zeile — sonst
        # stünde eine Ergebniszeile vor der Ausgangsgleichung (Prüfung 11.10.2026, H5/M4). Gegebene Bilder bleiben.
        vorher = None
        for e in s['elemente']:
            if e['typ'] in ('formel', 'notiz') and e.get('x') == LX:
                t = max(e.get('ein', 1.0), 1.0)
                if vorher is not None:
                    t = max(t, vorher + 0.6)
                e['ein'] = round(t, 2)
                vorher = t
            elif e['typ'] in ('formel',) and e.get('ein', 1.0) < 1.0:
                e['ein'] = 1.0
    return s


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


def jetzt_du(sim):
    if sim == 'umformer':
        return sz('Jetzt du', 'Jetzt du: Löse die Aufgaben im Umformer unter dem Clip.',
                  titel('Jetzt du', 280, 86),
                  n('Löse die Aufgaben|im Umformer unter dem Clip.', 430, 'blau', 50, ein=0.6))
    return sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der nachfolgenden Animation|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


FOLGE = {'umformen': 1, 'kontrolle-umformen': 2, 'klammern': 3, 'kontrolle-klammern': 4, 'faelle': 5,
         'kontrolle-faelle': 6, 'sichten': 7, 'kontrolle-sichten': 8, 'parameter': 9, 'kontrolle-parameter': 10}


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einführungsclip'):
    alt = R + 'clips/' + PREFIX + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': PREFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Lineare Gleichungen',
         'fach': 'Grundlagenfach', 'lerngebiet': '2 · Gleichungen, Ungleichungen und Gleichungssysteme',
         'lektion': ['g2-2a'], 'stufe': ['BM1'], 'datum': '2026-10-11',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Lineare Gleichungen lösen', 'folge': FOLGE[name],
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms lineare-gleichungen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def fenster(x0, x1, y0, y1, xt, yt_, **kw):
    d = dict(xbereich=[x0, x1], ybereich=[y0, y1], xteilung=yt(*xt), yteilung=yt(*yt_))
    d.update(kw)
    return d


MERKE = lambda spr, notiz, g=44: sz('Merke', spr, titel('Zum Mitnehmen', 250, 76), n(notiz, 390, 'blau', g, ein=1.2))

# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# 5x − 7 = 2x + 8 ist das Beispiel der Themenseite («Schrittweise», Abschnitt Lösungsverfahren).
CLIP = 'umformen'
W1 = fenster(-1, 8, -10, 26, (1, 2, 3, 4, 5, 6, 7), (-5, 5, 10, 15, 20, 25))
W1n = fenster(-2, 8, -8, 16, (2, 4, 6), (-5, 5, 10, 15))
clip('umformen', 'Lineare Gleichungen lösen: umformen wie an der Waage',
     'Äquivalenzumformungen an 5x − 7 = 2x + 8: x-Glieder sammeln, Zahlen hinüber, durch den Faktor teilen — '
     'dazu das Minus vor x, die Probe in der Ausgangsgleichung und warum «mal null» verboten ist.',
     ['lineare Gleichung', 'Äquivalenzumformung', 'Probe', 'Waage'], [
         sz('Gleich bleibt gleich',
            'Eine Gleichung ist wie eine Waage im Gleichgewicht: Links und rechts steht derselbe Wert. Was du links tust, '
            'tust du auch rechts. Dann ändert sich die Lösungsmenge nicht. '
            'So ein Schritt heisst Äquivalenzumformung.',
            titel('Gleich bleibt gleich', 280, 80),
            f(r'5x - 7 = 2x + 8', 420, 60, ein='@Links'),
            n('beidseitig dasselbe:|addieren oder subtrahieren,|mit einer Zahl @\\neq 0@ multiplizieren oder teilen', 540, 'blau', 44,
              ein='@tust')),
         sz('Sammeln und teilen',
            'Zuerst sammelst du die x-Glieder links: beidseitig minus zwei x. Es bleibt drei x minus sieben gleich acht. '
            'Dann holst du die Zahlen nach rechts: plus sieben. Übrig bleibt drei x gleich fünfzehn. '
            'Zum Schluss teilst du durch drei: x gleich fünf. Im Bild machen beide Seiten jede Umformung mit, '
            'und ihr Schnittpunkt bleibt bei x gleich fünf.',
            f(r'5x - 7 = 2x + 8', 260, 52, ein=0.2),
            op('-2x', 260, '@beidseitig'),
            f(r'3x - 7 = 8', 350, 52, ein='@bleibt'),
            op('+7', 350, '@plus'),
            f(r'3x = 15', 440, 52, ein='@Übrig'),
            op(':3', 440, '@teilst'),
            f(r'x = \fc{5}', 530, 52, ein='@durch+0.9'),
            # Beide Seiten werden gleich verändert («beidseitig minus zwei x», «plus sieben», «teilst durch drei»),
            # darum liegt der Schnittpunkt in jedem Zwischenstand bei x = 5 (nachgerechnet in pruefe_zahlen.py).
            graf(W1, geraden=[bew([[0, 5, -7], ['@beidseitig', 5, -7], ['@beidseitig+1.2', 3, -7], ['@plus', 3, -7],
                                   ['@plus+1.0', 3, 0], ['@teilst', 3, 0], ['@teilst+1.0', 1, 0]], 1),
                              bew([[0, 2, 8], ['@beidseitig', 2, 8], ['@beidseitig+1.2', 0, 8], ['@plus', 0, 8],
                                   ['@plus+1.0', 0, 15], ['@teilst', 0, 15], ['@teilst+1.0', 0, 5]], 2)],
                 strecken=[senkrecht(5, -10, 26, '@Bild')], ein=0.3)),
         sz('Minus vor x',
            'Vorsicht, wenn vor x ein Minus stehen bleibt. Zwei x gleich drei x minus sechs: beidseitig minus drei x. '
            'Es bleibt minus x gleich minus sechs. Das ist noch nicht die Lösung! Mal minus eins dreht beide Vorzeichen: '
            'x gleich sechs.',
            f(r'2x = 3x - 6', 260, 52, ein=0.3),
            op('-3x', 260, '@beidseitig'),
            f(r'-x = -6', 350, 52, ein='@bleibt#2'),
            n('noch nicht die Lösung', 440, 'rot', 42, ein='@noch'),
            op(r'\cdot (-1)', 350, '@Mal'),
            f(r'x = \fc{6}', 530, 52, ein='@dreht+1.0'),
            # 2x = 3x − 6 schneidet sich bei (6 | 12); nach −3x: y = −x und y = −6, nach ·(−1): y = x und y = 6.
            graf(W1n, geraden=[bew([[0, 2, 0], ['@beidseitig', 2, 0], ['@beidseitig+1.2', -1, 0], ['@Mal', -1, 0], ['@Mal+1.0', 1, 0]], 1),
                               bew([[0, 3, -6], ['@beidseitig', 3, -6], ['@beidseitig+1.2', 0, -6], ['@Mal', 0, -6], ['@Mal+1.0', 0, 6]], 2)],
                 strecken=[senkrecht(6, -8, 16, '@dreht')], ein=0.3)),
         sz('Die Probe',
            'Die Probe machst du in der Ausgangsgleichung, nicht in einer umgeformten Zeile: Nur so deckt sie einen Fehler '
            'in jedem Schritt auf. Setz fünf ein. Links: fünf mal fünf minus sieben, das ist achtzehn. Rechts: zwei mal '
            'fünf plus acht, auch achtzehn. Die Lösungsmenge enthält genau die Zahl fünf.',
            f(r'5x - 7 = 2x + 8', 260, 52, ein=0.3),
            f(r'5 \cdot 5 - 7 = 18', 360, 52, ein='@Links'),
            f(r'2 \cdot 5 + 8 = 18 \;\checkmark', 450, 52, ein='@Rechts'),
            f(r'\mathbb{L} = \{\fc{5}\}', 570, 56, ein='@Lösungsmenge'),
            graf(W1, geraden=[ger(5, -7, 1), ger(2, 8, 2)],
                 punkte=[pt(5, 18, 3, '(5 | 18)', [4.6, 20.5], 'end', ein='@Lösungsmenge')], ein=0.05)),
         sz('Nie mal null',
            'Mal null ist keine Äquivalenzumformung: Aus jeder Gleichung wird null gleich null, wahr für jedes x. '
            'Die Lösungsmenge ändert sich, und zurück geht es nicht, denn durch null kann man nicht teilen.',
            f(r'5x - 7 = 2x + 8', 280, 52, ein=0.3),
            op(r'\cdot 0', 280, '@Mal', falsch=True),
            f(r'0 = 0', 380, 52, ein='@wird+0.4'),
            n('Mit @0@ multiplizieren ist|keine Äquivalenzumformung.', 500, 'rot', 44, ein='@Lösungsmenge')),
         MERKE('Zum Mitnehmen: Sammle die x-Glieder auf einer Seite und die Zahlen auf der anderen, dann teile durch den '
               'Faktor vor x. Jede Umformung auf beiden Seiten, nie mal null. Und am Schluss die Probe in der Ausgangsgleichung.',
               '1. @x@-Glieder auf eine Seite|2. Zahlen auf die andere|3. durch den Faktor vor @x@ teilen|4. Probe in der Ausgangsgleichung|beidseitig gleich, nie mal @0@'),
         jetzt_du('umformer'),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
CLIP = 'kontrolle-umformen'
clip('kontrolle-umformen', 'Lineare Gleichungen lösen: Kontrollfragen zum Umformen',
     'Fünf Fragen: x-Glieder sammeln, durch einen negativen Faktor teilen, keine Äquivalenzumformung, Probe und −x = −4.',
     ['lineare Gleichung', 'Äquivalenzumformung', 'Probe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Minus x auf beiden Seiten: drei x minus drei gleich neun. Jetzt stehen alle x-Glieder links. '
            'Weiter mit plus drei und durch drei: x gleich vier.',
            f(r'4x - 3 = x + 9', 280, 56, ein=1.0),
            op('-x', 280, 1.0, g=50),
            f(r'3x - 3 = 9', 380, 56, ein='@Jetzt'),
            f(r'x = \fc{4}', 480, 56, ein='@Weiter+1.5')),
         sz('Frage 2',
            'Teile beide Seiten durch minus vier: x gleich minus fünf. Probe: minus vier mal minus fünf gibt zwanzig.',
            f(r'-4x = 20', 280, 56, ein=1.0),
            op(':(-4)', 280, '@Teile', g=50),
            f(r'x = \fc{-5}', 380, 56, ein='@Teile+1.6'),
            f(r'(-4) \cdot (-5) = 20 \;\checkmark', 480, 52, ein='@Probe')),
         sz('Frage 3',
            'Mal null lässt sich nicht rückgängig machen, denn durch null kann man nicht teilen. '
            'Die beiden anderen Umformungen lassen sich umkehren.',
            f(r'\fd{\cdot\, 0}: \quad 0 = 0', 300, 60, ein=1.0),
            n('Mit null multiplizieren ist|keine Äquivalenzumformung.', 430, 'rot', ein='@beiden')),
         sz('Frage 4',
            'Links: sieben minus zwei mal drei, das ist eins. Rechts: drei minus zwei, auch eins. '
            'Beide Seiten sind gleich, also ist drei eine Lösung.',
            f(r'7 - 2 \cdot 3 = 1', 300, 56, ein='@Links'),
            f(r'3 - 2 = 1 \;\checkmark', 400, 56, ein='@Rechts')),
         sz('Frage 5',
            'Minus x gleich minus vier heisst: Das Gegenteil von x ist minus vier. Mal minus eins dreht beide '
            'Vorzeichen, also x gleich vier. Probe: sechs minus vier gibt zwei.',
            f(r'6 - x = 2', 260, 56, ein=1.0),
            f(r'-x = -4', 360, 56, ein=1.0),
            op(r'\cdot (-1)', 360, '@Mal', g=50),
            f(r'x = \fc{4}', 460, 56, ein='@Vorzeichen'),
            f(r'6 - 4 = 2 \;\checkmark', 560, 52, ein='@Probe')),
         MERKE('Zum Mitnehmen: Gegenoperationen auf beiden Seiten, nie mal null. Bleibt minus x stehen, mit minus eins '
               'multiplizieren. Die Probe in der Ausgangsgleichung zeigt, ob alles stimmt.',
               'Gegenoperation auf beiden Seiten|@-x = c@: mal @(-1)@|Probe in der Ausgangsgleichung'),
     ], [
         wahl('Frage 1', '4x − 3 = x + 9: Welcher Schritt sammelt die x-Glieder links?',
              ['beidseitig − x', 'beidseitig + x', 'beidseitig : 4'], 0,
              {0: 'Ja.',
               1: 'Dann steht rechts 2x. Welche Umformung lässt rechts kein x übrig?',
               2: 'Das ist erlaubt, aber rechts bleibt x stehen. Welche Umformung holt es weg?'},
              sprich='Vier x minus drei gleich x plus neun: Welcher Schritt sammelt die x-Glieder links?',
              rueck_sprich={1: 'Dann steht rechts zwei x. Welche Umformung lässt rechts kein x übrig?',
                            2: 'Das ist erlaubt, aber rechts bleibt x stehen. Welche Umformung holt es weg?'}),
         wahl('Frage 2', '−4x = 20: Welche Lösung hat die Gleichung?',
              ['x = −5', 'x = 5', 'x = 16'], 0,
              {0: 'Ja.',
               1: 'Setz x = 5 ein: −4 · 5 = −20, nicht 20.',
               2: '−4x heisst −4 · x. Die Gegenoperation zum Multiplizieren ist das Teilen.'},
              sprich='Minus vier x gleich zwanzig: Welche Lösung hat die Gleichung?',
              rueck_sprich={1: 'Setz x gleich fünf ein. Minus vier mal fünf ist minus zwanzig, nicht zwanzig.',
                            2: 'Minus vier x heisst minus vier mal x. Die Gegenoperation zum Multiplizieren ist das Teilen.'}),
         wahl('Frage 3', 'Welche Umformung ist keine Äquivalenzumformung?',
              ['beidseitig · 0', 'beidseitig − 3x', 'beidseitig : (−2)'], 0,
              {0: 'Ja.',
               1: 'Minus 3x auf beiden Seiten lässt sich mit plus 3x rückgängig machen. Welche nicht?',
               2: 'Durch −2 teilen lässt sich mit · (−2) rückgängig machen. Welche nicht?'},
              sprich='Welche Umformung ist keine Äquivalenzumformung?',
              rueck_sprich={1: 'Minus drei x auf beiden Seiten lässt sich mit plus drei x rückgängig machen. Welche nicht?',
                            2: 'Durch minus zwei teilen lässt sich mit mal minus zwei rückgängig machen. Welche nicht?'}),
         wahl('Frage 4', 'Probe: Ist x = 3 eine Lösung von 7 − 2x = x − 2?',
              ['Ja, beide Seiten ergeben 1.', 'Nein, links steht 1, rechts −1.', 'Nein, links steht 13.'], 0,
              {0: 'Ja.',
               1: 'Rechts steht x − 2. Setz x = 3 ein.',
               2: '−2x heisst: zwei mal x abziehen. Links steht 7 − 2 · 3.'},
              sprich='Probe: Ist x gleich drei eine Lösung von sieben minus zwei x gleich x minus zwei?',
              rueck_sprich={1: 'Rechts steht x minus zwei. Setz x gleich drei ein.',
                            2: 'Minus zwei x heisst: zwei mal x abziehen. Links steht sieben minus zwei mal drei.'}),
         wahl('Frage 5', '6 − x = 2. Jemand rechnet: −x = −4, also x = −4. Was stimmt?',
              ['Aus −x = −4 folgt x = 4.', 'Richtig wäre −x = 8.', 'Die Rechnung stimmt.'], 0,
              {0: 'Ja.',
               1: 'Beidseitig − 6 gibt −x = 2 − 6. Prüf den letzten Schritt mit der Probe.',
               2: 'Probe mit x = −4: 6 − (−4) = 10, nicht 2. Wo liegt der Fehler?'},
              sprich='Sechs minus x gleich zwei. Jemand rechnet: minus x gleich minus vier, also x gleich minus vier. Was stimmt?',
              rueck_sprich={1: 'Beidseitig minus sechs gibt minus x gleich zwei minus sechs. Prüf den letzten Schritt mit der Probe.',
                            2: 'Probe mit x gleich minus vier: sechs minus minus vier ist zehn, nicht zwei. Wo liegt der Fehler?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# Beispiele der Themenseite: 4(x − 2) = 2x + 6 (Mini-Check), x/3 + 2 = x/2 − 1 (Beispiel «Mit Brüchen»).
CLIP = 'klammern'
W2 = fenster(-1, 9, -10, 26, (1, 2, 3, 4, 5, 6, 7, 8), (-5, 5, 10, 15, 20, 25))
clip('klammern', 'Lineare Gleichungen lösen: Klammern und Brüche',
     'Zuerst aufräumen: der Faktor vor der Klammer, das Minus vor der Klammer, Brüche mit dem Hauptnenner '
     'und der Bruchstrich, der wie eine Klammer wirkt.',
     ['lineare Gleichung', 'Klammer', 'Minus vor der Klammer', 'Hauptnenner', 'Bruch'], [
         sz('Zuerst aufräumen',
            'Steht in einer Gleichung eine Klammer oder ein Bruch, räumst du zuerst auf: Klammern auflösen, Brüche mit dem '
            'Hauptnenner wegschaffen. Erst dann sortierst du wie gewohnt.',
            titel('Zuerst aufräumen', 270, 80),
            n('1. aufräumen: Klammern auflösen,|Brüche mal den Hauptnenner|(ein Bruchstrich klammert)|2. sortieren und teilen|3. Probe', 410, 'blau', 46, ein='@Klammern')),
         sz('Faktor vor der Klammer',
            'Vier mal Klammer x minus zwei gleich zwei x plus sechs. Die Vier vor der Klammer multipliziert jedes Glied: '
            'vier x minus acht. Dann wie gewohnt: minus zwei x und '
            'plus acht gibt zwei x gleich vierzehn, also x gleich sieben.',
            f(r'4(x - 2) = 2x + 6', 260, 52, ein=0.3),
            f(r'4x - 8 = 2x + 6', 350, 52, ein='@multipliziert'),
            op('-2x + 8', 350, '@gewohnt'),
            f(r'2x = 14', 440, 52, ein='@gibt'),
            op(':2', 440, '@also'),
            f(r'x = \fc{7}', 530, 52, ein='@also+0.7'),
            graf(W2, geraden=[bew([[0, 4, -8], ['@gewohnt', 4, -8], ['@gewohnt+1.4', 2, 0], ['@also', 2, 0], ['@also+0.9', 1, 0]], 1),
                              bew([[0, 2, 6], ['@gewohnt', 2, 6], ['@gewohnt+1.4', 0, 14], ['@also', 0, 14], ['@also+0.9', 0, 7]], 2)],
                 strecken=[senkrecht(7, -10, 26, '@also+0.9')], ein=0.3)),
         sz('Minus vor der Klammer',
            'Steht vor der Klammer ein Minus, dreht es jedes Vorzeichen in der Klammer. Fünf minus zwei mal Klammer x plus eins: '
            'Minus zwei mal x gibt minus zwei x, minus zwei mal eins gibt minus zwei. Zusammengefasst: drei minus zwei x '
            'gleich x. Plus zwei x: drei gleich drei x, also x gleich eins.',
            f(r'5 - 2(x + 1) = x', 260, 52, ein=0.3),
            f(r'5 - 2x \fb{- 2} = x', 350, 52, ein='@gibt#2'),
            f(r'3 - 2x = x', 440, 52, ein='@Zusammengefasst'),
            op('+2x', 440, '@Plus#2'),
            f(r'3 = 3x', 530, 52, ein='@Plus#2+1.0'),
            f(r'x = \fc{1}', 620, 52, ein='@also')),
         sz('Brüche',
            'Bei Brüchen multiplizierst du beide Seiten mit dem Hauptnenner, hier sechs. Jedes Glied mal sechs: '
            'aus x Drittel wird zwei x, aus zwei wird zwölf, aus x Halbe wird drei x, aus minus eins wird minus sechs. '
            'Sortiert: achtzehn gleich x. Probe: sechs plus zwei ist acht, neun minus eins auch acht.',
            f(r'\dfrac{x}{3} + 2 = \dfrac{x}{2} - 1', 280, 52, ein=0.3),
            op(r'\cdot 6', 280, '@Hauptnenner'),
            f(r'2x + 12 = 3x - 6', 400, 52, ein='@Sortiert-1.2'),
            f(r'18 = x', 490, 52, ein='@Sortiert'),
            f(r'\tfrac{18}{3} + 2 = 8;\ \ \tfrac{18}{2} - 1 = 8 \;\checkmark', 590, 46, ein='@Probe')),
         sz('Bruchstrich als Klammer',
            'Ein Bruchstrich wirkt wie eine Klammer. Mal sechs gibt drei mal Klammer x minus eins, minus zwei mal Klammer '
            'x plus eins, gleich sechs. Das Minus vor dem zweiten Bruch gilt für den ganzen Zähler: minus zwei x minus zwei. '
            'Zusammengefasst: x minus fünf gleich sechs, also x gleich elf.',
            f(r'\dfrac{x - 1}{2} - \dfrac{x + 1}{3} = 1', 280, 52, ein=0.3),
            op(r'\cdot 6', 280, '@Mal'),
            f(r'3(x - 1) - 2(x + 1) = 6', 400, 52, ein='@Mal+0.9'),
            f(r'3x - 3 - 2x \fb{- 2} = 6', 490, 52, ein='@ganzen'),
            f(r'x - 5 = 6', 580, 52, ein='@Zusammengefasst'),
            f(r'x = \fc{11}', 670, 52, ein='@also')),
         MERKE('Zum Mitnehmen: Der Faktor vor einer Klammer gilt für jedes Glied, ein Minus davor dreht jedes Vorzeichen. '
               'Brüche verschwinden mit dem Hauptnenner: jedes Glied mal den Hauptnenner, auch die Zahlen ohne Bruch.',
               'Faktor vor der Klammer: jedes Glied|Minus vor der Klammer: jedes Vorzeichen dreht|Brüche: jedes Glied mal den Hauptnenner'),
         jetzt_du('umformer'),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
CLIP = 'kontrolle-klammern'
clip('kontrolle-klammern', 'Lineare Gleichungen lösen: Kontrollfragen zu Klammern und Brüchen',
     'Fünf Fragen: Faktor vor der Klammer, Minus vor der Klammer, Hauptnenner, jedes Glied mal den Nenner und −2(x − 4) = 6.',
     ['Klammer', 'Hauptnenner', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Drei multipliziert jedes Glied in der Klammer: drei x plus zwölf. Dann minus zwölf und durch drei: x gleich zwei.',
            f(r'3(x + 4) = 18', 280, 56, ein=1.0),
            f(r'3x + 12 = 18', 380, 56, ein='@multipliziert'),
            f(r'x = \fc{2}', 480, 56, ein='@Dann+1.5')),
         sz('Frage 2',
            'Das Minus dreht jedes Vorzeichen in der Klammer: minus zwei x plus drei. Sieben plus drei gibt zehn. '
            'Zehn minus zwei x gleich eins, also x gleich vier Komma fünf.',
            f(r'7 - (2x - 3) = 1', 280, 56, ein=1.0),
            f(r'7 - 2x + 3 = 1', 380, 56, ein='@dreht+1.0'),
            f(r'10 - 2x = 1', 480, 56, ein='@gibt'),
            f(r'x = \fc{4.5}', 580, 56, ein='@also')),
         sz('Frage 3',
            'Zwölf ist das kleinste gemeinsame Vielfache von vier und sechs: der Hauptnenner. Mal zwölf gibt drei x plus '
            'zwölf gleich zwei x, also x gleich minus zwölf.',
            f(r'\dfrac{x}{4} + 1 = \dfrac{x}{6}', 280, 52, ein=1.0),
            op(r'\cdot 12', 280, '@Hauptnenner', g=48),
            f(r'3x + 12 = 2x', 400, 52, ein='@Mal'),
            f(r'x = \fc{-12}', 490, 52, ein='@also')),
         sz('Frage 4',
            'Jedes Glied auf beiden Seiten mal zwei: x plus sechs gleich vierzehn. Also x gleich acht.',
            f(r'\dfrac{x}{2} + 3 = 7', 280, 52, ein=1.0),
            op(r'\cdot 2', 280, 1.0, g=48),
            f(r'x + 6 = 14', 400, 52, ein='@Glied'),
            f(r'x = \fc{8}', 490, 52, ein='@Also')),
         sz('Frage 5',
            'Klammer auflösen: minus zwei x plus acht gleich sechs, denn minus mal minus gibt plus. Minus acht: '
            'minus zwei x gleich minus zwei. Durch minus zwei: x gleich eins.',
            f(r'-2(x - 4) = 6', 260, 56, ein=1.0),
            f(r'-2x + 8 = 6', 360, 56, ein='@auflösen'),
            f(r'-2x = -2', 460, 56, ein='@gibt+1.2'),
            f(r'x = \fc{1}', 560, 56, ein='@Durch')),
         MERKE('Zum Mitnehmen: Der Faktor vor der Klammer trifft jedes Glied, ein Minus dreht jedes Vorzeichen. Mal den '
               'Hauptnenner heisst: jedes Glied auf beiden Seiten.',
               'jedes Glied in der Klammer|Minus dreht jedes Vorzeichen|mal Hauptnenner: jedes Glied'),
     ], [
         wahl('Frage 1', '3(x + 4) = 18: Was ist richtig aufgelöst?',
              ['3x + 12 = 18', '3x + 4 = 18', 'x + 12 = 18'], 0,
              {0: 'Ja.',
               1: 'Die 3 multipliziert auch die 4.',
               2: 'Die 3 multipliziert auch das x.'},
              sprich='Drei mal Klammer x plus vier gleich achtzehn: Was ist richtig aufgelöst?',
              rueck_sprich={1: 'Die Drei multipliziert auch die Vier.',
                            2: 'Die Drei multipliziert auch das x.'}),
         wahl('Frage 2', '7 − (2x − 3) = 1: Wie heisst die linke Seite ohne Klammer?',
              ['10 − 2x', '4 − 2x', '10 + 2x'], 0,
              {0: 'Ja.',
               1: 'Das Minus vor der Klammer dreht auch das Vorzeichen von −3.',
               2: 'Das Minus vor der Klammer dreht auch das Vorzeichen von 2x.'},
              sprich='Sieben minus Klammer zwei x minus drei gleich eins: Wie heisst die linke Seite ohne Klammer?',
              rueck_sprich={1: 'Das Minus vor der Klammer dreht auch das Vorzeichen von minus drei.',
                            2: 'Das Minus vor der Klammer dreht auch das Vorzeichen von zwei x.'}),
         wahl('Frage 3', 'x/4 + 1 = x/6: Mit welcher Zahl multiplizierst du, damit alle Brüche verschwinden?',
              ['mit 12', 'mit 10', 'mit 4'], 0,
              {0: 'Ja.',
               1: '10 ist 4 + 6. Gesucht ist eine Zahl, die durch 4 und durch 6 teilbar ist.',
               2: 'Mit 4 verschwindet x/4, aber x/6 bleibt ein Bruch.'},
              sprich='x Viertel plus eins gleich x Sechstel: Mit welcher Zahl multiplizierst du, damit alle Brüche verschwinden?',
              rueck_sprich={1: 'Zehn ist vier plus sechs. Gesucht ist eine Zahl, die durch vier und durch sechs teilbar ist.',
                            2: 'Mit vier verschwindet x Viertel, aber x Sechstel bleibt ein Bruch.'}),
         wahl('Frage 4', 'x/2 + 3 = 7: Was steht nach · 2 da?',
              ['x + 6 = 14', 'x + 3 = 14', 'x + 6 = 7'], 0,
              {0: 'Ja.',
               1: 'Mal 2 gilt für jedes Glied, auch für die 3.',
               2: 'Mal 2 gilt für beide Seiten, auch für die 7.'},
              sprich='x Halbe plus drei gleich sieben: Was steht nach mal zwei da?',
              rueck_sprich={1: 'Mal zwei gilt für jedes Glied, auch für die Drei.',
                            2: 'Mal zwei gilt für beide Seiten, auch für die Sieben.'}),
         wahl('Frage 5', '−2(x − 4) = 6: Welche Lösung hat die Gleichung?',
              ['x = 1', 'x = −7', 'x = −1'], 0,
              {0: 'Ja.',
               1: 'Prüf das Vorzeichen beim Auflösen der Klammer: Was ergibt −2 mal −4?',
               2: 'Aus −2x = −2 folgt nicht x = −1. Mach die Probe.'},
              sprich='Minus zwei mal Klammer x minus vier gleich sechs: Welche Lösung hat die Gleichung?',
              rueck_sprich={1: 'Prüf das Vorzeichen beim Auflösen der Klammer. Was ergibt minus zwei mal minus vier?',
                            2: 'Aus minus zwei x gleich minus zwei folgt nicht x gleich minus eins. Mach die Probe.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Beispiele der Themenseite: 3x + 2 = 11 (Fall 1), 2(x + 3) = 2x + 9 (Fall 2), 4x + 8 = 4(x + 2) (Fall 3).
CLIP = 'faelle'
W3a = fenster(-2, 6, -4, 14, (-1, 1, 2, 3, 4, 5), (-2, 2, 4, 6, 8, 10, 12))
W3b = fenster(-4, 4, -4, 16, (-3, -2, -1, 1, 2, 3), (4, 8, 12))
clip('faelle', 'Lineare Gleichungen lösen: drei Lösungsfälle',
     'Sortiert steht a · x = c da: Ist a nicht null, gibt es genau eine Lösung; ist a null, entscheidet c — '
     'keine Lösung oder jede Zahl. Dazu der Unterschied zwischen 𝕃 = {0} und 𝕃 = { }.',
     ['lineare Gleichung', 'Lösungsfälle', 'leere Menge', 'Lösungsmenge'], [
         sz('a mal x gleich c',
            'Hast du alle x-Glieder links und alle Zahlen rechts gesammelt, steht a mal x gleich c da. Bei drei x plus '
            'zwei gleich elf ist das drei x gleich neun. a ist drei, nicht null: Du darfst durch drei teilen, '
            'x gleich drei. Genau eine Lösung, und im Bild genau ein Schnittpunkt.',
            f(r'a \cdot x = c', 250, 58, ein=0.3),
            f(r'3x + 2 = 11', 350, 52, ein='@Bei'),
            op('-2', 350, '@das'),
            f(r'3x = 9', 440, 52, ein='@das+0.6'),
            f(r'x = \fc{3}', 530, 52, ein='@teilen'),
            n('@a \\neq 0@: genau eine Lösung', 630, 'blau', 42, ein='@Genau'),
            graf(W3a, geraden=[bew([[0, 3, 2], ['@das', 3, 2], ['@das+1.0', 3, 0], ['@teilen', 3, 0], ['@teilen+0.9', 1, 0]], 1),
                               bew([[0, 0, 11], ['@das', 0, 11], ['@das+1.0', 0, 9], ['@teilen', 0, 9], ['@teilen+0.9', 0, 3]], 2)],
                 strecken=[senkrecht(3, -4, 14, '@Schnittpunkt')], ein='@Bei')),
         sz('Keine Lösung',
            'Anders bei zwei mal Klammer x plus drei gleich zwei x plus neun. Ausmultipliziert: zwei x plus sechs gleich '
            'zwei x plus neun. Minus zwei x, und x ist weg. Es bleibt sechs gleich neun. Das ist falsch, egal welches x '
            'du einsetzt: Die Lösungsmenge ist leer. Im Bild sind die beiden Seiten parallele Geraden, sie schneiden sich nie.',
            f(r'2(x + 3) = 2x + 9', 260, 52, ein=0.3),
            f(r'2x + 6 = 2x + 9', 350, 52, ein='@Ausmultipliziert'),
            op('-2x', 350, '@Minus'),
            f(r'6 = 9 \quad \fd{\text{falsch}}', 440, 52, ein='@bleibt'),
            f(r'\mathbb{L} = \{\,\}', 560, 56, ein='@Lösungsmenge'),
            # «Minus zwei x»: beide Geraden werden waagrecht, y = 6 und y = 9 — parallel in jedem Zwischenstand.
            graf(W3b, geraden=[bew([[0, 2, 6], ['@Minus', 2, 6], ['@Minus+1.1', 0, 6]], 1),
                               bew([[0, 2, 9], ['@Minus', 2, 9], ['@Minus+1.1', 0, 9]], 2)], ein=0.3)),
         sz('Jede Zahl',
            'Und bei vier x plus acht gleich vier mal Klammer x plus zwei? Ausmultipliziert steht links und rechts dasselbe. '
            'Minus vier x: acht gleich acht. Das ist immer wahr. Jede Zahl ist Lösung, die Lösungsmenge sind alle reellen '
            'Zahlen. Die beiden Geraden liegen aufeinander.',
            f(r'4x + 8 = 4(x + 2)', 260, 52, ein=0.3),
            f(r'4x + 8 = 4x + 8', 350, 52, ein='@Ausmultipliziert'),
            op('-4x', 350, '@Minus'),
            f(r'8 = 8 \quad \fc{\text{wahr}}', 440, 52, ein='@Minus+1.4'),
            f(r'\mathbb{L} = \mathbb{R}', 560, 56, ein='@Lösungsmenge'),
            graf(W3b, geraden=[bew([[0, 4, 8], ['@Minus', 4, 8], ['@Minus+1.1', 0, 8]], 1, dicke=9),
                               bew([[0, 4, 8], ['@Minus', 4, 8], ['@Minus+1.1', 0, 8]], 2, gestrichelt=True, dicke=3)], ein=0.3)),
         sz('Null mal x',
            'Warum ist das so? Ist a null, steht null mal x gleich c da. Null mal x ist immer null. Ist c nicht null, '
            'passt kein x. Ist c null, passt jedes.',
            f(r'0 \cdot x = c', 290, 60, ein=0.3),
            n('@c \\neq 0@: kein @x@ passt, @\\mathbb{L} = \\{\\,\\}@', 420, 'blau', 44, ein='@kein'),
            n('@c = 0@: jedes @x@ passt, @\\mathbb{L} = \\mathbb{R}@', 510, 'blau', 44, ein='@jedes')),
         sz('Lösung null',
            'Verwechsle das nicht mit der Lösung null. Fünf x gleich null hat die Lösung x gleich null: Die Lösungsmenge '
            'enthält die Zahl null. Dagegen hat null mal x gleich fünf gar keine Lösung, die Lösungsmenge ist leer.',
            f(r'5x = 0 \;\Rightarrow\; \mathbb{L} = \{\fc{0}\}', 300, 54, ein='@Fünf'),
            f(r'0 \cdot x = 5 \;\Rightarrow\; \mathbb{L} = \{\,\}', 420, 54, ein='@Dagegen'),
            n('@\\{0\\}@ ist nicht leer: Es enthält die Null.', 540, 'rot', 42, ein='@leer')),
         MERKE('Zum Mitnehmen: Sortiere, bis a mal x gleich c dasteht. Ist a nicht null, gibt es genau eine Lösung. '
               'Ist a null, entscheidet c: Eine falsche Aussage heisst keine Lösung, eine wahre heisst: jede Zahl ist Lösung.',
               '@a \\cdot x = c@|@a \\neq 0@: genau eine Lösung|@a = 0,\\ c \\neq 0@: @\\mathbb{L} = \\{\\,\\}@|@a = 0,\\ c = 0@: @\\mathbb{L} = \\mathbb{R}@'),
         jetzt_du('umformer'),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
CLIP = 'kontrolle-faelle'
W3k = fenster(-4, 4, -4, 6, (-3, -2, -1, 1, 2, 3), (-2, 2, 4))
clip('kontrolle-faelle', 'Lineare Gleichungen lösen: Kontrollfragen zu den Lösungsfällen',
     'Fünf Fragen: 0 = 7, 5(x − 1) = 5x − 5, 3x = 0, zwei parallele Seitengeraden und die Zahl, die jede Zahl zur Lösung macht.',
     ['Lösungsfälle', 'leere Menge', 'Kontrollfragen'], [
         sz('Frage 1',
            'Null gleich sieben ist falsch, für jedes x. Keine Zahl erfüllt die Gleichung: Die Lösungsmenge ist leer.',
            f(r'0 = 7 \quad \fd{\text{falsch}}', 300, 60, ein=1.0),
            f(r'\mathbb{L} = \{\,\}', 420, 60, ein='@Lösungsmenge')),
         sz('Frage 2',
            'Links ausmultipliziert steht fünf x minus fünf, genau wie rechts. Die Gleichung ist für jedes x wahr.',
            f(r'5x - 5 = 5x - 5', 300, 58, ein=1.0),
            f(r'\mathbb{L} = \mathbb{R}', 420, 60, ein='@jedes')),
         sz('Frage 3',
            'Vor x steht drei, nicht null. Teilen durch drei gibt x gleich null. Die Lösungsmenge enthält genau die Zahl '
            'null, sie ist nicht leer.',
            f(r'3x = 0', 280, 58, ein=1.0),
            op(':3', 280, '@Teilen', g=50),
            f(r'x = 0', 380, 58, ein='@gibt'),
            f(r'\mathbb{L} = \{\fc{0}\}', 480, 60, ein='@Lösungsmenge')),
         sz('Frage 4',
            'Die beiden Geraden verlaufen parallel und schneiden sich nie. Kein x macht beide Seiten gleich: '
            'Die Gleichung hat keine Lösung. Umgeformt bleibt drei gleich minus eins.',
            f(r'0.5x + 3 = 0.5x - 1', 280, 52, ein='@Umgeformt-1.0'),
            f(r'3 = -1 \quad \fd{\text{falsch}}', 380, 52, ein='@bleibt'),
            graf(W3k, geraden=[ger(0.5, 3, 1), ger(0.5, -1, 2, gestrichelt=True)], ein=0.05)),
         sz('Frage 5',
            'Ausmultipliziert steht zwei x plus zwei gleich zwei x plus c. Nur bei c gleich zwei bleibt eine wahre Aussage: '
            'zwei gleich zwei.',
            f(r'2x + 2 = 2x + c', 300, 56, ein=1.0),
            f(r'c = 2: \quad 2 = 2 \;\; \fc{\text{wahr}}', 420, 52, ein='@Nur')),
         MERKE('Zum Mitnehmen: Verschwindet x, entscheidet die Aussage, die übrig bleibt: falsch heisst leere Lösungsmenge, '
               'wahr heisst alle reellen Zahlen. Bleibt x stehen, gibt es genau eine Lösung, auch wenn sie null ist.',
               'falsche Aussage: @\\mathbb{L} = \\{\\,\\}@|wahre Aussage: @\\mathbb{L} = \\mathbb{R}@|@a x = 0@ mit @a \\neq 0@: @\\mathbb{L} = \\{0\\}@'),
     ], [
         wahl('Frage 1', 'Nach dem Umformen bleibt 0 = 7. Welche Lösungsmenge?',
              ['𝕃 = { }', '𝕃 = ℝ', '𝕃 = {7}'], 0,
              {0: 'Ja.',
               1: 'Ist 0 = 7 für irgendein x wahr?',
               2: 'Im Rest steht kein x mehr. Kann x = 7 die Aussage wahr machen?'},
              sprich='Nach dem Umformen bleibt null gleich sieben. Welche Lösungsmenge?',
              rueck_sprich={1: 'Ist null gleich sieben für irgendein x wahr?',
                            2: 'Im Rest steht kein x mehr. Kann x gleich sieben die Aussage wahr machen?'}),
         wahl('Frage 2', '5(x − 1) = 5x − 5: Welche Lösungsmenge hat die Gleichung?',
              ['𝕃 = ℝ', '𝕃 = { }', '𝕃 = {1}'], 0,
              {0: 'Ja.',
               1: 'Multipliziere die linke Seite aus und vergleiche mit rechts.',
               2: 'Setz x = 4 ein. Stimmt die Gleichung auch dann?'},
              sprich='Fünf mal Klammer x minus eins gleich fünf x minus fünf: Welche Lösungsmenge hat die Gleichung?',
              rueck_sprich={1: 'Multipliziere die linke Seite aus und vergleiche mit rechts.',
                            2: 'Setz x gleich vier ein. Stimmt die Gleichung auch dann?'}),
         wahl('Frage 3', '3x = 0: Wie heisst die Lösungsmenge?',
              ['𝕃 = {0}', '𝕃 = { }', '𝕃 = ℝ'], 0,
              {0: 'Ja.',
               1: 'Vor x steht 3, nicht 0. Durch 3 teilen ist erlaubt. Was kommt heraus?',
               2: 'Setz x = 1 ein: 3 · 1 = 3, nicht 0. Ist wirklich jede Zahl Lösung?'},
              sprich='Drei x gleich null: Wie heisst die Lösungsmenge?',
              rueck_sprich={1: 'Vor x steht drei, nicht null. Durch drei teilen ist erlaubt. Was kommt heraus?',
                            2: 'Setz x gleich eins ein. Drei mal eins ist drei, nicht null. Ist wirklich jede Zahl Lösung?'}),
         wahl('Frage 4', 'Im Bild sind die beiden Seiten einer Gleichung als Geraden gezeichnet. Wie viele Lösungen hat sie?',
              ['keine', 'genau eine', 'unendlich viele'], 0,
              {0: 'Ja.',
               1: 'Wo schneiden sich die beiden Geraden?',
               2: 'Liegen die beiden Geraden aufeinander?'},
              sprich='Im Bild sind die beiden Seiten einer Gleichung als Geraden gezeichnet. Wie viele Lösungen hat sie?',
              rueck_sprich={1: 'Wo schneiden sich die beiden Geraden?',
                            2: 'Liegen die beiden Geraden aufeinander?'}),
         wahl('Frage 5', '2(x + 1) = 2x + c: Für welches c ist jede Zahl eine Lösung?',
              ['c = 2', 'c = 1', 'c = 0'], 0,
              {0: 'Ja.',
               1: 'Löse die Klammer auf: Welche Zahl steht dann neben 2x?',
               2: 'Bei c = 0 bleibt 2 = 0. Ist das wahr?'},
              sprich='Zwei mal Klammer x plus eins gleich zwei x plus c: Für welches c ist jede Zahl eine Lösung?',
              rueck_sprich={1: 'Löse die Klammer auf. Welche Zahl steht dann neben zwei x?',
                            2: 'Bei c gleich null bleibt zwei gleich null. Ist das wahr?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# Mietkosten K(x) = 12x + 45, Budget 117 — Einstieg der Themenseite; 3x − 1 = 1 für die Grenze von Tabelle und Graph.
CLIP = 'sichten'
W4 = fenster(-1, 10, -80, 180, (2, 4, 6, 8), (-50, 50, 100, 150), xname='x [h]', yname='K [CHF]')
W4g = fenster(-1, 3, -3, 4, (-1, 1, 2), (-2, -1, 1, 2, 3))
clip('sichten', 'Lineare Gleichungen lösen: Tabelle, Graph und Normalform',
     'Die Mietkosten-Gleichung 12x + 45 = 117 dreimal gesehen: in der Tabelle, im Graphen und über die Normalform '
     'a · x + b = 0 mit x = −b/a. Dazu, warum Tabelle und Graph die Lösung oft nur eingrenzen.',
     ['lineare Gleichung', 'Normalform', 'Wertetabelle', 'Graph', 'Schnittpunkt'], [
         sz('Mietkosten',
            'Eine Hebebühne kostet fünfundvierzig Franken Grundgebühr und zwölf Franken pro Stunde. Wie viele Stunden '
            'liegen mit hundertsiebzehn Franken drin? Für x Stunden kostet sie zwölf x plus fünfundvierzig, '
            'und das soll gleich dem Budget sein.',
            titel('Mietkosten', 260, 76),
            f(r'K(x) = 12x + 45, \;\; x \ge 0', 380, 54, ein='@kostet#2'),
            f(r'12x + 45 = 117', 480, 54, ein='@soll')),
         sz('Tabelle',
            'Erste Sicht: die Tabelle. Bei vier Stunden kostet es dreiundneunzig, weniger als das Budget. Bei fünf sind es '
            'hundertfünf. Bei sechs genau hundertsiebzehn. Bei sieben ist es schon zu viel. Die Lösung ist die Stelle, '
            'an der das Zeichen kippt: x gleich sechs.',
            f(r'12x + 45 = 117', 240, 50, ein=0.3),
            f(r'x = 4:\quad 93 \lt 117', 330, 48, ein='@Bei#1'),
            f(r'x = 5:\quad 105 \lt 117', 410, 48, ein='@Bei#2'),
            f(r'x = 6:\quad \fc{117 = 117}', 490, 48, ein='@Bei#3'),
            f(r'x = 7:\quad 129 \gt 117', 570, 48, ein='@Bei#4')),
         sz('Graph',
            'Zweite Sicht: der Graph. Die Kosten sind eine Gerade, das Budget eine Waagrechte. Sie schneiden sich bei '
            'x gleich sechs, wie in der Tabelle.',
            f(r'y = 12x + 45', 300, 50, ein='@Kosten'),
            f(r'y = 117', 390, 50, ein='@Budget'),
            f(r'x = \fc{6}', 500, 54, ein='@schneiden'),
            graf(W4, geraden=[dict(ger(12, 45, 1), ein='@Kosten'), dict(ger(0, 117, 2, gestrichelt=True), ein='@Budget')],
                 punkte=[pt(6, 117, 3, '(6 | 117)', [5.6, 135], 'end', ein='@schneiden')],
                 strecken=[senkrecht(6, -80, 117, '@schneiden')], ein=0.3)),
         sz('Normalform',
            'Dritte Sicht: die Rechnung über die Normalform. Bring alles auf eine Seite, minus hundertsiebzehn. '
            'Es entsteht zwölf x minus zweiundsiebzig gleich null, die Form a mal x plus b gleich null. Hier ist a zwölf '
            'und b minus zweiundsiebzig. Die Lösung ist x gleich minus b durch a, also zweiundsiebzig durch zwölf, sechs. '
            'Im Bild ist sie die Nullstelle der Geraden.',
            f(r'12x + 45 = 117', 250, 50, ein=0.3),
            op('-117', 250, '@Bring'),
            f(r'12x - 72 = 0', 340, 50, ein='@entsteht'),
            f(r'a \cdot x + b = 0', 430, 50, ein='@Form'),
            f(r'x = -\dfrac{b}{a} = \dfrac{72}{12} = \fc{6}', 550, 50, ein='@Lösung'),
            # «minus hundertsiebzehn»: beide Seiten sinken um 117 — rechts wird die x-Achse, links 12x − 72.
            graf(W4, geraden=[bew([[0, 12, 45], ['@Bring+0.6', 12, 45], ['@Bring+2.2', 12, -72]], 1),
                              bew([[0, 0, 117], ['@Bring+0.6', 0, 117], ['@Bring+2.2', 0, 0]], 2, gestrichelt=True, dicke=5)],
                 punkte=[pt(6, 0, 3, '(6 | 0)', [6.3, -22], ein='@Nullstelle')],
                 # Die rechte Seite liegt nach «− 117» auf der x-Achse — eigens beschriften, sonst ist sie unsichtbar.
                 texte=[dict(bei=[0.4, 14], text='rechts: y = 0', farbe=2, groesse=26, anker='start', ein='@entsteht')], ein=0.3)),
         sz('Grenzen',
            'Tabelle und Graph haben eine Grenze. Bei drei x minus eins gleich eins kippt das Zeichen zwischen null und eins, '
            'und im Bild liegt der Schnittpunkt irgendwo dazwischen. Erst die Rechnung liefert die Lösung genau: zwei Drittel.',
            f(r'3x - 1 = 1', 250, 52, ein=0.3),
            f(r'x = 0:\quad -1 \lt 1', 340, 46, ein='@kippt'),
            f(r'x = 1:\quad 2 \gt 1', 420, 46, ein='@kippt+0.8'),
            f(r'3x = 2 \;\Rightarrow\; x = \fc{\tfrac{2}{3}}', 530, 52, ein='@Rechnung'),
            graf(W4g, geraden=[ger(3, -1, 1), ger(0, 1, 2, gestrichelt=True)],
                 punkte=[pt(2 / 3, 1, 3, '(2/3 | 1)', [0.55, 1.45], 'end', ein='@Rechnung')], ein='@Bild')),
         MERKE('Zum Mitnehmen: Tabelle und Graph zeigen, wo beide Seiten gleich sind, oft nur ungefähr. Die Normalform '
               'a mal x plus b gleich null liefert die Lösung genau: x gleich minus b durch a, wenn a nicht null ist.',
               'Tabelle: wo das Zeichen kippt|Graph: Schnittpunkt der beiden Seiten|Normalform @a \\cdot x + b = 0@:|@x = -\\tfrac{b}{a}@ für @a \\neq 0@'),
         jetzt_du('animation'),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
CLIP = 'kontrolle-sichten'
W4k = fenster(-2, 6, -2, 6, (-1, 1, 2, 3, 4, 5), (-1, 1, 2, 3, 4, 5))
clip('kontrolle-sichten', 'Lineare Gleichungen lösen: Kontrollfragen zu Tabelle, Graph und Normalform',
     'Fünf Fragen: Normalform von 5x + 4 = 2x − 5, x = −b/a, Schnittpunkt im Bild antippen, Lösung aus der Tabelle eingrenzen '
     'und warum die Rechnung genau ist.',
     ['Normalform', 'Graph', 'Wertetabelle', 'Kontrollfragen'], [
         sz('Frage 1',
            'Beidseitig minus zwei x und plus fünf: drei x plus neun gleich null. a ist drei, b ist neun, also x gleich minus drei.',
            f(r'5x + 4 = 2x - 5', 280, 54, ein=1.0),
            op('-2x + 5', 280, 1.0, g=46),
            f(r'3x + 9 = 0', 380, 54, ein='@Beidseitig+1.6'),
            f(r'x = -\tfrac{9}{3} = \fc{-3}', 480, 54, ein='@also')),
         sz('Frage 2',
            'a ist vier, b ist minus zehn. Minus b durch a: zehn durch vier, zwei Komma fünf.',
            f(r'4x - 10 = 0', 280, 56, ein=1.0),
            f(r'x = -\dfrac{-10}{4} = \fc{2.5}', 400, 54, ein='@Minus#2')),
         sz('Frage 3',
            'Die Geraden schneiden sich im Punkt zwei, drei. Also löst x gleich zwei die Gleichung: links drei, '
            'rechts minus eins plus vier, auch drei.',
            f(r'x + 1 = -0.5x + 4', 280, 50, ein=1.0),
            f(r'1.5x = 3 \;\Rightarrow\; x = \fc{2}', 380, 50, ein='@Also'),
            graf(W4k, geraden=[bew([[0, 1, 1]], 1), bew([[0, -0.5, 4]], 2)],
                 punkte=[pt(2, 3, 3, '(2 | 3)', [2.3, 2.15], ein=1.0)], ein=0.05)),
         sz('Frage 4',
            'Das Zeichen kippt zwischen drei und vier, dort liegt die Lösung. Genau liefert sie nur die Rechnung: '
            'drei x gleich zehn, x gleich zehn Drittel.',
            f(r'x = 3:\ 7 \lt 8; \quad x = 4:\ 10 \gt 8', 280, 48, ein=1.0),
            f(r'3x = 10 \;\Rightarrow\; x = \fc{\tfrac{10}{3}}', 400, 52, ein='@Rechnung')),
         sz('Frage 5',
            'Die Tabelle prüft nur die x-Werte, die du einsetzt. Liegt die Lösung dazwischen, grenzt sie sie nur ein. '
            'Die Rechnung findet sie genau.',
            n('Tabelle: nur die eingesetzten @x@|Rechnung: genau', 340, 'blau', 46, ein=1.0)),
         MERKE('Zum Mitnehmen: Alles auf eine Seite bringen ergibt die Normalform a mal x plus b gleich null, die Lösung ist '
               'minus b durch a. Graph und Tabelle zeigen dieselbe Lösung, aber oft nur ungefähr.',
               '@a \\cdot x + b = 0 \\Rightarrow x = -\\tfrac{b}{a}@|Schnittpunkt der Seiten: Lösung|Tabelle grenzt ein'),
     ], [
         wahl('Frage 1', '5x + 4 = 2x − 5 in der Normalform a · x + b = 0: Welche ist richtig?',
              ['3x + 9 = 0', '3x − 1 = 0', '7x + 9 = 0'], 0,
              {0: 'Ja.',
               1: 'Bring alles nach links. Was wird dabei aus der Zahl −5 rechts?',
               2: 'Bring alles nach links: − 2x. Was bleibt von 5x?'},
              sprich='Fünf x plus vier gleich zwei x minus fünf, in der Normalform a mal x plus b gleich null: Welche ist richtig?',
              rueck_sprich={1: 'Bring alles nach links. Was wird dabei aus der Zahl minus fünf rechts?',
                            2: 'Bring alles nach links: minus zwei x. Was bleibt von fünf x?'}),
         wahl('Frage 2', '4x − 10 = 0: Welche Lösung liefert x = −b/a?',
              ['x = 2.5', 'x = −2.5', 'x = 6'], 0,
              {0: 'Ja.',
               1: 'b ist −10. Was ist dann −b?',
               2: '4x heisst 4 · x. Geteilt wird durch a = 4.'},
              sprich='Vier x minus zehn gleich null: Welche Lösung liefert x gleich minus b durch a?',
              rueck_sprich={1: 'b ist minus zehn. Was ist dann minus b?',
                            2: 'Vier x heisst vier mal x. Geteilt wird durch a gleich vier.'}),
         klick('Frage 3', 'y = x + 1 und y = −0.5x + 4 sind im Bild. Tipp den Punkt, dessen x die Gleichung x + 1 = −0.5x + 4 löst.',
               [2, 3], 'Getroffen: (2 | 3), also x = 2.',
               [{'bei': [0, 1], 'text': 'Das ist der Punkt der Geraden y = x + 1 auf der y-Achse. Gesucht ist die Stelle, an der beide Seiten gleich sind.',
                 'sprich': 'Das ist der Punkt der Geraden y gleich x plus eins auf der y-Achse. Gesucht ist die Stelle, an der beide Seiten gleich sind.'},
                {'bei': [0, 4], 'text': 'Das ist der Punkt der zweiten Geraden auf der y-Achse. Gesucht ist die Stelle, an der beide Seiten gleich sind.',
                 'sprich': 'Das ist der Punkt der zweiten Geraden auf der y-Achse. Gesucht ist die Stelle, an der beide Seiten gleich sind.'}],
               'Nicht ganz. Gesucht ist die Stelle, an der beide Seiten denselben Wert haben: wo sich die Geraden treffen.',
               sprich='y gleich x plus eins und y gleich minus null Komma fünf x plus vier sind im Bild. Tipp den Punkt, dessen x die Gleichung löst.',
               falsch_sprich='Nicht ganz. Gesucht ist die Stelle, an der beide Seiten denselben Wert haben: wo sich die Geraden treffen.'),
         wahl('Frage 4', 'Tabelle zu 3x − 2 = 8: x = 3 gibt 7 < 8, x = 4 gibt 10 > 8. Was folgt daraus?',
              ['Die Lösung liegt zwischen 3 und 4.', 'Es gibt keine Lösung.', 'Die Lösung ist 3.5.'], 0,
              {0: 'Ja.',
               1: 'Das Zeichen kippt von < zu >. Was heisst das für die beiden Seiten?',
               2: 'Setz 3.5 ein: 3 · 3.5 − 2 = 8.5, nicht 8. Die Tabelle grenzt nur ein.'},
              sprich='Tabelle zu drei x minus zwei gleich acht: x gleich drei gibt sieben, kleiner als acht. x gleich vier gibt zehn, grösser als acht. Was folgt daraus?',
              rueck_sprich={1: 'Das Zeichen kippt von kleiner zu grösser. Was heisst das für die beiden Seiten?',
                            2: 'Setz drei Komma fünf ein: Das gibt acht Komma fünf, nicht acht. Die Tabelle grenzt nur ein.'}),
         wahl('Frage 5', 'Warum liefert die Rechnung die Lösung genau, die Tabelle oft nicht?',
              ['Die Tabelle prüft nur die eingesetzten Werte.', 'Die Tabelle rechnet falsch.', 'Die Rechnung rundet anders.'], 0,
              {0: 'Ja.',
               1: 'Die Werte in der Tabelle stimmen. Welche x-Werte kommen darin vor?',
               2: 'Die Rechnung rundet gar nicht. Welche x-Werte prüft die Tabelle?'},
              sprich='Warum liefert die Rechnung die Lösung genau, die Tabelle oft nicht?',
              rueck_sprich={1: 'Die Werte in der Tabelle stimmen. Welche x-Werte kommen darin vor?',
                            2: 'Die Rechnung rundet gar nicht. Welche x-Werte prüft die Tabelle?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
# Beispiele der Themenseite: k·x + 6 = 2x + 3k und k·x + 1 = 2x + 3 (Abschnitt Parameterdiskussion).
# Das Bild zeigt wie die Simulation die Differenz links − rechts, y = a(k)·x − c(k) (Normalform aus Kapitel 4):
# Ihre Nullstelle ist die Lösung; bei a(k) = 0 wird sie waagrecht — auf der x-Achse (jede Zahl) oder daneben (keine).
CLIP = 'parameter'
W5 = fenster(-2, 6, -10, 10, (-1, 1, 2, 3, 4, 5), (-8, -4, 4, 8))
clip('parameter', 'Lineare Gleichungen lösen: Parameterdiskussion',
     'k · x + 6 = 2x + 3k sortiert auf (k − 2) · x = 3(k − 2): für k ≠ 2 ist x = 3, für k = 2 jede Zahl. '
     'Bei k · x + 1 = 2x + 3 gibt k = 2 dagegen keine Lösung.',
     ['Parameterdiskussion', 'Parameter', 'Lösungsfälle', 'kritischer Wert'], [
         sz('Ein zweiter Buchstabe',
            'In einer Parametergleichung steht neben x ein zweiter Buchstabe, hier k. Gesucht ist die Lösung für jeden Wert '
            'von k. Das heisst Parameterdiskussion.',
            titel('Parameter', 260, 80),
            f(r'\fb{k} \cdot x + 6 = 2x + 3\fb{k}', 400, 56, ein='@Buchstabe'),
            n('Lösung für jedes @k@', 520, 'blau', ein='@Gesucht')),
         sz('Sortieren',
            'Sortiere auf die Form a von k mal x gleich c von k: die x-Glieder links, den Rest rechts. Es entsteht k x minus '
            'zwei x gleich drei k minus sechs. Links klammerst du x aus: Klammer k minus zwei, mal x. Rechts lässt sich drei '
            'ausklammern: drei mal Klammer k minus zwei.',
            f(r'kx + 6 = 2x + 3k', 260, 52, ein=0.3),
            op('-2x - 6', 260, '@links'),
            f(r'kx - 2x = 3k - 6', 350, 52, ein='@entsteht'),
            f(r'(k - 2) \cdot x = 3k - 6', 440, 52, ein='@klammerst'),
            f(r'(k - 2) \cdot x = 3 \cdot (k - 2)', 530, 52, ein='@Rechts')),
         sz('Die Fälle',
            'Ist k nicht zwei, darfst du durch k minus zwei teilen: x ist drei, für jedes solche k. Bei k gleich zwei steht '
            'null mal x gleich null. Dann ist jede Zahl Lösung. Im Bild siehst du links minus rechts als Gerade, wie bei der '
            'Normalform. Für jedes k geht sie durch die Nullstelle drei, bei k gleich zwei liegt sie ganz auf der x-Achse.',
            f(r'(k - 2) \cdot x = 3 \cdot (k - 2)', 250, 50, ein=0.3),
            f(r'k \neq 2: \quad x = \fc{3}', 350, 52, ein='@teilen'),
            f(r'k = 2: \quad 0 \cdot x = 0, \;\; \mathbb{L} = \mathbb{R}', 450, 48, ein='@steht'),
            f(r'y = (k - 2) \cdot x - 3(k - 2)', 560, 40, ein='@Bild'),
            f(r'\fb{k = 5}', 640, 44, ein='@Bild'),
            f(r'\to\ \fb{k = 3}', 640, 44, ein='@Für#2', x=320),
            f(r'\to\ \fb{k = 2}', 640, 44, ein='@liegt', x=540),
            # m = k − 2, q = −3(k − 2): k = 5 → (3, −9), k = 3 → (1, −3), k = 2 → (0, 0); immer durch (3 | 0).
            graf(W5, geraden=[bew([[0, 3, -9], ['@Für#2', 3, -9], ['@Für#2+1.6', 1, -3], ['@liegt-0.4', 1, -3], ['@liegt+1.2', 0, 0]], 1,
                                  dicke=6, nullstelle={'farbe': 3})], ein='@Bild')),
         sz('Zweites Beispiel',
            'Anders bei k mal x plus eins gleich zwei x plus drei. Sortiert: Klammer k minus zwei, mal x, gleich zwei. '
            'Ist k nicht zwei, ist x gleich zwei durch Klammer k minus zwei. Bei k gleich zwei steht null mal x gleich zwei: '
            'falsch, die Lösungsmenge ist leer. Im Bild wird die Gerade waagrecht und trifft die x-Achse nie.',
            f(r'kx + 1 = 2x + 3', 240, 50, ein=0.3),
            f(r'(k - 2) \cdot x = 2', 330, 50, ein='@Sortiert'),
            f(r'k \neq 2: \quad x = \dfrac{2}{k - 2}', 440, 48, ein='@nicht'),
            f(r'k = 2: \quad 0 \cdot x = 2, \;\; \mathbb{L} = \{\,\}', 560, 46, ein='@steht'),
            f(r'\fb{k = 4}', 660, 44, ein='@nicht'),
            f(r'\to\ \fb{k = 2}', 660, 44, ein='@steht', x=320),
            # y = (k − 2)·x − 2: k = 4 → Nullstelle 1; «Bei k gleich zwei steht …» → k = 2, waagrecht y = −2, keine
            # Nullstelle. Kein Zwischenhalt bei k = 3, den der Ton nicht nennt (Prüfung 11.10.2026, H4).
            graf(W5, geraden=[bew([[0, 2, -2], ['@steht-0.6', 2, -2], ['@steht+1.4', 0, -2]], 1,
                                  dicke=6, nullstelle={'farbe': 3})], ein='@nicht')),
         sz('Probe der Formel',
            'Eine Probe zur Formel: Für k gleich vier gibt sie x gleich eins. Eingesetzt: vier mal eins plus eins ist fünf, '
            'zwei mal eins plus drei auch fünf.',
            f(r'k = 4: \quad x = \dfrac{2}{4 - 2} = 1', 280, 50, ein='@Formel'),
            f(r'4 \cdot 1 + 1 = 5; \quad 2 \cdot 1 + 3 = 5 \;\checkmark', 400, 48, ein='@Eingesetzt')),
         MERKE('Zum Mitnehmen: Sortiere auf a von k mal x gleich c von k. Suche den Wert, bei dem a von k null wird. Dort '
               'entscheidet c von k: null heisst jede Zahl, sonst keine Lösung. Für alle anderen k ist x gleich c von k durch a von k.',
               '@a(k) \\cdot x = c(k)@|kritisch: @a(k) = 0@, dort entscheidet @c(k)@|sonst @x = \\tfrac{c(k)}{a(k)}@', 42),
         jetzt_du('animation'),
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
CLIP = 'kontrolle-parameter'
clip('kontrolle-parameter', 'Lineare Gleichungen lösen: Kontrollfragen zur Parameterdiskussion',
     'Fünf Fragen: der kritische Wert von (k − 4) · x = 3, (k + 1) · x = k + 1 bei k = −1, Sortieren, Lösung für ein k '
     'und das k zu einer gegebenen Lösung.',
     ['Parameterdiskussion', 'kritischer Wert', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei k gleich vier steht null mal x gleich drei. Das ist für kein x wahr: keine Lösung.',
            f(r'k = 4: \quad 0 \cdot x = 3', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \{\,\}', 420, 56, ein='@keine')),
         sz('Frage 2',
            'Bei k gleich minus eins werden beide Seiten null: null mal x gleich null. Jede Zahl ist Lösung.',
            f(r'k = -1: \quad 0 \cdot x = 0', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \mathbb{R}', 420, 56, ein='@Jede')),
         sz('Frage 3',
            'Minus x und plus drei: k mal x minus x gleich zwei k plus drei. Links x ausklammern: Klammer k minus eins, mal x.',
            f(r'kx - 3 = x + 2k', 280, 54, ein=1.0),
            op('-x + 3', 280, 1.0, g=46),
            f(r'kx - x = 2k + 3', 380, 54, ein='@plus'),
            f(r'(k - 1) \cdot x = 2k + 3', 480, 54, ein='@ausklammern')),
         sz('Frage 4',
            'Bei k gleich zwei steht eins mal x gleich sieben: x gleich sieben.',
            f(r'k = 2: \quad 1 \cdot x = 7', 300, 56, ein=1.0),
            f(r'x = \fc{7}', 420, 56, ein='@gleich#3-0.3')),
         sz('Frage 5',
            'Setz x gleich drei ein: Klammer k minus zwei, mal drei, gleich sechs. Also k minus zwei gleich zwei, k gleich vier.',
            f(r'(k - 2) \cdot 3 = 6', 300, 54, ein=1.0),
            f(r'k - 2 = 2 \;\Rightarrow\; k = \fc{4}', 420, 54, ein='@Also')),
         MERKE('Zum Mitnehmen: Wird der Faktor vor x null, entscheidet die rechte Seite: null heisst jede Zahl, sonst keine. '
               'Sonst gibt es genau eine Lösung, x gleich c von k durch a von k.',
               '@0 \\cdot x = c@: @c \\neq 0@ keine, @c = 0@ jede Zahl|sonst @x = \\tfrac{c(k)}{a(k)}@', 42),
     ], [
         wahl('Frage 1', '(k − 4) · x = 3: Für welches k gibt es keine Lösung?',
              ['k = 4', 'k = −4', 'k = 3'], 0,
              {0: 'Ja.',
               1: 'Setz k = −4 ein: −8x = 3 hat eine Lösung. Wann wird der Faktor vor x null?',
               2: 'Setz k = 3 ein: −x = 3 hat eine Lösung. Wann wird der Faktor vor x null?'},
              sprich='Klammer k minus vier, mal x, gleich drei: Für welches k gibt es keine Lösung?',
              rueck_sprich={1: 'Setz k gleich minus vier ein. Minus acht x gleich drei hat eine Lösung. Wann wird der Faktor vor x null?',
                            2: 'Setz k gleich drei ein. Minus x gleich drei hat eine Lösung. Wann wird der Faktor vor x null?'}),
         wahl('Frage 2', '(k + 1) · x = k + 1: Was gilt bei k = −1?',
              ['𝕃 = ℝ', '𝕃 = { }', '𝕃 = {1}'], 0,
              {0: 'Ja.',
               1: 'Setz k = −1 ein. Steht rechts auch null?',
               2: 'x = 1 gilt für k ≠ −1. Setz k = −1 ein.'},
              sprich='Klammer k plus eins, mal x, gleich k plus eins: Was gilt bei k gleich minus eins?',
              rueck_sprich={1: 'Setz k gleich minus eins ein. Steht rechts auch null?',
                            2: 'x gleich eins gilt für k ungleich minus eins. Setz k gleich minus eins ein.'}),
         wahl('Frage 3', 'k · x − 3 = x + 2k, sortiert auf a(k) · x = c(k): Welche Form ist richtig?',
              ['(k − 1) · x = 2k + 3', '(k + 1) · x = 2k + 3', '(k − 1) · x = 2k − 3'], 0,
              {0: 'Ja.',
               1: 'Das x rechts kommt mit − x nach links.',
               2: 'Die −3 kommt mit + 3 nach rechts.'},
              sprich='k mal x minus drei gleich x plus zwei k, sortiert auf a von k mal x gleich c von k: Welche Form ist richtig?',
              rueck_sprich={1: 'Das x rechts kommt mit minus x nach links.',
                            2: 'Die minus drei kommt mit plus drei nach rechts.'}),
         wahl('Frage 4', '(k − 1) · x = 2k + 3 für k = 2: Welche Lösung?',
              ['x = 7', 'x = 1/7', 'x = 5'], 0,
              {0: 'Ja.',
               1: 'Teile die rechte Seite durch den Faktor vor x, nicht umgekehrt.',
               2: 'Rechts steht 2k + 3. Setz k = 2 ein: 2 · 2 + 3.'},
              sprich='Klammer k minus eins, mal x, gleich zwei k plus drei, für k gleich zwei: Welche Lösung?',
              rueck_sprich={1: 'Teile die rechte Seite durch den Faktor vor x, nicht umgekehrt.',
                            2: 'Rechts steht zwei k plus drei. Setz k gleich zwei ein: zwei mal zwei plus drei.'}),
         wahl('Frage 5', 'Für welches k hat (k − 2) · x = 6 die Lösung x = 3?',
              ['k = 4', 'k = 5', 'k = 2'], 0,
              {0: 'Ja.',
               1: 'Setz x = 3 und k = 5 ein: 3 · 3 = 9, nicht 6.',
               2: 'Bei k = 2 steht 0 · x = 6: keine Lösung.'},
              sprich='Für welches k hat Klammer k minus zwei, mal x, gleich sechs die Lösung x gleich drei?',
              rueck_sprich={1: 'Setz x gleich drei und k gleich fünf ein. Drei mal drei ist neun, nicht sechs.',
                            2: 'Bei k gleich zwei steht null mal x gleich sechs: keine Lösung.'}),
     ], art='Kontrollclip')

if UNAUFGELOEST:
    print('Anker ohne Wortzeit (geschätzt):')
    for u in UNAUFGELOEST:
        print('  ', u)
