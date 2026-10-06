"""Erzeugt die zehn Drehbücher des Leitprogramms Lineare und quadratische Gleichungen (06.10.2026).

  python3 scripts/lp/lineare-quadratische-gleichungen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen.

Aufbau wie bei den Funktionen-Leitprogrammen (Vorbild Betragsfunktionen): Formeln und Notizen links
(x 150), ein unterstützendes Bild rechts (x 1010, y 175, 760 × 760). Bei Gleichungen steht die
Umformungskette im Vordergrund — die Operation rechts neben der Zeile wie im Heft («| −2x»). Der Graph
unterstützt nur (Schnittpunkt zweier Seiten, Nullstellen einer Parabel), er ersetzt die Rechnung nicht.

Fragebild (HOWTO-leitprogramme §15): Klickfragen zeigen beim Erscheinen nur die Achsen (leerer Graf,
`tippbar`), die Auflösung mit Parabel und Nullstellen erst ab 1.0 s.

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = Gleichung, Terme, Parabel/Graph        \\fa{…}
  2 orange = die Umformung («| −2x»), Parameter k    \\fb{…}
  3 grün   = Lösungen, Lösungsmenge, Nullstellen     \\fc{…}
  4 rot    = Fehler, verlorene Lösung                \\fd{…}
  5 Tinte  = neutral (zweite Seite einer Gleichung, Bezugslinien)
"""
import json
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX, OX = 1010, 175, 760, 760, 150, 700


def graf(W, kurven=(), punkte=(), ein=0.05, geraden=(), parabeln=(), **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=list(kurven), geraden=list(geraden), parabeln=list(parabeln), punkte=list(punkte),
             pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def par(a, u, v, farbe=1, null=True, beschr=True, bew=None):
    """Parabel y = a(x − u)^2 + v, mit grünen Nullstellen; bew = Liste [t, a, u, v] statt fest."""
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


def pt(x, y, farbe=3, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
        if bei:
            d['beschriftung_bei'] = bei
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
          tol=0.45, bei=0.3):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


JETZT_DU = sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))


def clip(name, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/g2-2-lp-' + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': 'g2-2-lp-' + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Gleichungen · linear und quadratisch',
         'fach': 'Grundlagenfach', 'lerngebiet': '2 · Gleichungen, Ungleichungen und Gleichungssysteme',
         'lektion': ['g2-2a', 'g2-2b'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-06',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Gleichungen lösen',
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms lineare-quadratische-gleichungen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def yt(*werte):
    return [[w, ('%g' % w).replace('-', '−')] for w in werte]


def fenster(x0, x1, y0, y1, xt, yt_):
    return dict(xbereich=[x0, x1], ybereich=[y0, y1], xteilung=yt(*xt), yteilung=yt(*yt_))


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
W1 = fenster(-2, 9, -10, 26, (2, 4, 6, 8), (-10, 10, 20))
W1b = fenster(-4, 4, -4, 16, (-2, 2), (4, 8, 12))
clip('umformen', 'Gleichungen lösen: umformen und die drei Lösungsfälle',
     'Äquivalenzumformungen an 4(x − 2) = 2x + 6 mit Probe — und die Fälle, in denen x verschwindet: keine Lösung oder alle Zahlen.',
     ['lineare Gleichung', 'Äquivalenzumformung', 'Probe', 'Lösungsfälle'], [
         sz('Gleich bleibt gleich',
            'Eine Gleichung ist wie eine Waage: Links und rechts steht derselbe Wert. Was du links tust, tust du auch rechts. '
            'Dann bleibt die Lösungsmenge gleich. Das heisst Äquivalenzumformung.',
            titel('Gleich bleibt gleich', 280, 80),
            f(r'4(x - 2) = 2x + 6', 420, 60, ein=1.5),
            n('beidseitig dasselbe tun:|addieren, subtrahieren,|mit einer Zahl @\\neq 0@ multiplizieren oder teilen', 540, 'blau', 44, ein=4.5)),
         sz('Vorgelöst',
            'Zuerst die Klammer auflösen: vier x minus acht gleich zwei x plus sechs. Jetzt die x auf eine Seite: minus zwei x. '
            'Es bleibt zwei x minus acht gleich sechs. Plus acht: zwei x gleich vierzehn. Durch zwei: x gleich sieben.',
            f(r'4(x - 2) = 2x + 6', 260, 52, ein=0.2),
            f(r'4x - 8 = 2x + 6', 350, 52, ein=2.1),
            op('-2x', 350, 6.2),
            f(r'2x - 8 = 6', 440, 52, ein=7.4),
            op('+8', 440, 9.6),
            f(r'2x = 14', 530, 52, ein=10.4),
            op(':2', 530, 11.8),
            f(r'x = \fc{7}', 620, 52, ein=12.7),
            graf(W1, geraden=[ger(4, -8, 1), ger(2, 6, 5)], ein=0.3)),
         sz('Die Probe',
            'Die Probe macht man in der Ausgangsgleichung. Links: vier mal Klammer sieben minus zwei, das ist zwanzig. '
            'Rechts: zwei mal sieben plus sechs, auch zwanzig. Im Bild schneiden sich die beiden Seiten bei x gleich sieben.',
            f(r'4 \cdot (7 - 2) = 20', 280, 52, ein=3.0),
            f(r'2 \cdot 7 + 6 = 20 \;\checkmark', 370, 52, ein=6.3),
            f(r'\mathbb{L} = \{\fc{7}\}', 500, 56, ein=8.5),
            graf(W1, geraden=[ger(4, -8, 1), ger(2, 6, 5)], ein=0.05),
            graf(W1, geraden=[ger(4, -8, 1), ger(2, 6, 5)], ein=9.2, punkte=[pt(7, 20, 3, '(7 | 20)', [6.6, 22.5], 'end')])),
         sz('Wenn x verschwindet',
            'Manchmal fällt x beim Umformen ganz weg. Zwei mal Klammer x plus drei gleich zwei x plus neun gibt '
            'zwei x plus sechs gleich zwei x plus neun. Minus zwei x: sechs gleich neun. Das ist falsch, für jedes x. '
            'Es gibt keine Lösung. Die beiden Geraden sind parallel.',
            f(r'2(x + 3) = 2x + 9', 260, 52, ein=0.3),
            f(r'2x + 6 = 2x + 9', 350, 52, ein=5.8),
            op('-2x', 350, 8.7),
            f(r'6 = 9 \quad \fd{\text{falsch}}', 440, 52, ein=9.6),
            f(r'\mathbb{L} = \{\,\}', 560, 56, ein=12.8),
            graf(W1b, geraden=[ger(2, 6, 1), ger(2, 9, 5)], ein=0.3)),
         sz('Alles ist Lösung',
            'Anders bei vier x plus acht gleich vier mal Klammer x plus zwei. Ausmultipliziert steht links und rechts dasselbe. '
            'Minus vier x: acht gleich acht. Das ist immer wahr. Jede Zahl ist Lösung: Die Lösungsmenge sind alle reellen Zahlen. '
            'Die beiden Geraden liegen aufeinander.',
            f(r'4x + 8 = 4(x + 2)', 260, 52, ein=0.3),
            f(r'4x + 8 = 4x + 8', 350, 52, ein=3.7),
            op('-4x', 350, 6.4),
            f(r'8 = 8 \quad \fc{\text{wahr}}', 440, 52, ein=7.4),
            f(r'\mathbb{L} = \mathbb{R}', 560, 56, ein=9.7),
            graf(W1b, geraden=[ger(4, 8, 1, dicke=9), ger(4, 8, 5, gestrichelt=True)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Forme auf beiden Seiten gleich um, bis a mal x gleich c dasteht. Ist a nicht null, gibt es genau '
            'eine Lösung. Ist a null, entscheidet c: keine Lösung oder alle Zahlen. Und am Schluss die Probe.',
            titel('Zum Mitnehmen', 250, 76),
            n('@a \\cdot x = c@|@a \\neq 0@: genau eine Lösung|@a = 0,\\ c \\neq 0@: @\\mathbb{L} = \\{\\,\\}@|@a = 0,\\ c = 0@: @\\mathbb{L} = \\mathbb{R}@',
              390, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-umformen', 'Gleichungen lösen: Kontrollfragen zum Umformen',
     'Fünf Fragen zu Äquivalenzumformungen, Klammern, den drei Lösungsfällen und zur Probe.',
     ['lineare Gleichung', 'Äquivalenzumformung', 'Kontrollfragen'], [
         sz('Frage 1',
            'Mal null macht aus jeder Gleichung null gleich null. Die Lösungsmenge ändert sich: Das ist keine Äquivalenzumformung.',
            f(r'\fd{\cdot\, 0}: \quad 0 = 0', 300, 60, ein=1.0),
            n('Mit null multiplizieren ist verboten.', 430, 'rot', ein=3.0)),
         sz('Frage 2',
            'Die Zwei vor der Klammer multipliziert jedes Glied: zwei mal x und zwei mal minus drei. Das gibt zwei x minus sechs.',
            f(r'2(x - 3) = 2x - 6', 300, 60, ein=1.0),
            n('jedes Glied in der Klammer', 430, 'blau', ein=3.0)),
         sz('Frage 3',
            'Null gleich vier ist falsch, egal welches x man einsetzt. Es gibt keine Lösung.',
            f(r'0 = 4 \quad \fd{\text{falsch}}', 300, 60, ein=1.0),
            f(r'\mathbb{L} = \{\,\}', 420, 60, ein=2.8)),
         sz('Frage 4',
            'Rechts ausmultipliziert steht drei x plus drei, genau dasselbe wie links. Jede Zahl ist Lösung.',
            f(r'3x + 3 = 3x + 3', 300, 60, ein=1.0),
            f(r'\mathbb{L} = \mathbb{R}', 420, 60, ein=3.6)),
         sz('Frage 5',
            'Einsetzen in beide Seiten: Links fünf mal zwei minus vier, also sechs. Rechts drei mal zwei, auch sechs. Zwei ist eine Lösung.',
            f(r'5 \cdot 2 - 4 = 6', 300, 56, ein=1.0),
            f(r'3 \cdot 2 = 6 \;\checkmark', 400, 56, ein=4.0)),
         sz('Merke',
            'Zum Mitnehmen: Beide Seiten gleich umformen, nie mit null multiplizieren. Verschwindet x, entscheidet die Aussage, '
            'die übrig bleibt.',
            titel('Zum Mitnehmen', 250, 76),
            n('falsche Aussage: @\\mathbb{L} = \\{\\,\\}@|wahre Aussage: @\\mathbb{L} = \\mathbb{R}@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Welche Umformung ist keine Äquivalenzumformung?',
              ['beidseitig · 0', 'beidseitig − 5', 'beidseitig : (−2)'], 0,
              {0: 'Ja.',
               1: 'Minus fünf auf beiden Seiten lässt sich rückgängig machen. Welche nicht?',
               2: 'Durch −2 teilen lässt sich mit · (−2) rückgängig machen. Welche nicht?'},
              sprich='Welche Umformung ist keine Äquivalenzumformung?',
              rueck_sprich={1: 'Minus fünf auf beiden Seiten lässt sich rückgängig machen. Welche nicht?',
                            2: 'Durch minus zwei teilen lässt sich mit mal minus zwei rückgängig machen. Welche nicht?'}),
         wahl('Frage 2', '2(x − 3) = 8: Was ist richtig ausmultipliziert?',
              ['2x − 6 = 8', '2x − 3 = 8', 'x − 6 = 8'], 0,
              {0: 'Ja.',
               1: 'Die 2 multipliziert auch die 3.',
               2: 'Die 2 multipliziert auch das x.'},
              sprich='Zwei mal Klammer x minus drei gleich acht: Was ist richtig ausmultipliziert?',
              rueck_sprich={1: 'Die Zwei multipliziert auch die Drei.',
                            2: 'Die Zwei multipliziert auch das x.'}),
         wahl('Frage 3', 'Nach dem Umformen bleibt 0 = 4. Welche Lösungsmenge?',
              ['𝕃 = { }', '𝕃 = ℝ', '𝕃 = {4}'], 0,
              {0: 'Ja.',
               1: 'Ist 0 = 4 für irgendein x wahr?',
               2: 'Im Rest steht kein x mehr. Kann x = 4 die Aussage wahr machen?'},
              sprich='Nach dem Umformen bleibt null gleich vier. Welche Lösungsmenge?',
              rueck_sprich={1: 'Ist null gleich vier für irgendein x wahr?',
                            2: 'Im Rest steht kein x mehr. Kann x gleich vier die Aussage wahr machen?'}),
         wahl('Frage 4', '3x + 3 = 3(x + 1): Wie heisst die Lösungsmenge?',
              ['𝕃 = ℝ', '𝕃 = { }', '𝕃 = {1}'], 0,
              {0: 'Ja.',
               1: 'Multipliziere die rechte Seite aus und vergleiche.',
               2: 'Setz x = 5 ein. Stimmt die Gleichung auch dann?'},
              sprich='Drei x plus drei gleich drei mal Klammer x plus eins: Wie heisst die Lösungsmenge?',
              rueck_sprich={1: 'Multipliziere die rechte Seite aus und vergleiche.',
                            2: 'Setz x gleich fünf ein. Stimmt die Gleichung auch dann?'}),
         wahl('Frage 5', 'Probe: Ist x = 2 eine Lösung von 5x − 4 = 3x?',
              ['Ja, beide Seiten ergeben 6.', 'Nein, links steht 6, rechts 2.', 'Nein, x = 2 macht beide Seiten null.'], 0,
              {0: 'Ja.',
               1: 'Rechts steht 3x. Setz x = 2 ein.',
               2: 'Setz x = 2 in jede Seite einzeln ein.'},
              sprich='Probe: Ist x gleich zwei eine Lösung von fünf x minus vier gleich drei x?',
              rueck_sprich={1: 'Rechts steht drei x. Setz x gleich zwei ein.',
                            2: 'Setz x gleich zwei in jede Seite einzeln ein.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
W2 = fenster(-2, 7, -8, 6, (-1, 1, 2, 3, 4, 5, 6), (-6, -4, -2, 2, 4))
clip('nullprodukt', 'Gleichungen lösen: Ausklammern und Nullprodukt',
     'Der Satz vom Nullprodukt an x² = 5x: auf null bringen, ausklammern, jeden Faktor null setzen, prüfen — und warum man nie durch x teilt.',
     ['quadratische Gleichung', 'Nullprodukt', 'ausklammern', 'Probe'], [
         sz('Der Satz vom Nullprodukt',
            'Ein Produkt ist genau dann null, wenn mindestens ein Faktor null ist. Drei mal null ist null. Drei mal zwei ist nie null. '
            'Darauf baut ein ganzes Lösungsverfahren.',
            titel('Nullprodukt', 260, 80),
            f(r'a \cdot b = 0 \iff a = 0 \;\text{oder}\; b = 0', 400, 50, ein=0.5),
            n('@3 \\cdot 0 = 0@, aber @3 \\cdot 2 \\neq 0@', 520, 'blau', ein=4.3)),
         sz('Das Problem',
            'Gesucht sind alle x mit x Quadrat gleich fünf x. Die Strategie hat vier Schritte: auf null bringen, ausklammern, '
            'jeden Faktor null setzen, prüfen.',
            f(r'x^2 = 5x', 280, 66, ein=0.3),
            n('1. auf null bringen|2. ausklammern|3. jeden Faktor null setzen|4. prüfen', 420, 'blau', 46, ein=2.9)),
         sz('Vorgelöst',
            'Minus fünf x: x Quadrat minus fünf x gleich null. In beiden Gliedern steckt ein x. Ausgeklammert: x mal Klammer '
            'x minus fünf gleich null. Ein Faktor muss null sein: x gleich null oder x minus fünf gleich null, also x gleich fünf.',
            f(r'x^2 = 5x', 260, 52, ein=0.2),
            op('-5x', 260, 0.6),
            f(r'x^2 - 5x = 0', 350, 52, ein=1.2),
            f(r'\fa{x} \cdot (x - 5) = 0', 440, 52, ein=5.2),
            f(r'\fa{x} = 0 \;\;\text{oder}\;\; x - 5 = 0', 530, 50, ein=8.5),
            f(r'x = \fc{0} \;\;\text{oder}\;\; x = \fc{5}', 620, 50, ein=12.9),
            graf(W2, parabeln=[par(1, 2.5, -6.25)], ein=12.9)),
         sz('Die Probe',
            'Probe in der Ausgangsgleichung. Null eingesetzt: null gleich null. Fünf eingesetzt: fünfundzwanzig gleich '
            'fünfundzwanzig. Beide stimmen. Im Bild sind das die Nullstellen der Parabel y gleich x Quadrat minus fünf x.',
            f(r'x = 0: \quad 0^2 = 5 \cdot 0 \;\checkmark', 280, 50, ein=2.5),
            f(r'x = 5: \quad 5^2 = 5 \cdot 5 \;\checkmark', 370, 50, ein=4.8),
            f(r'\mathbb{L} = \{\fc{0};\ \fc{5}\}', 490, 56, ein=8.6),
            graf(W2, parabeln=[par(1, 2.5, -6.25)], ein=0.05)),
         sz('Der teure Fehler',
            'Und der teure Fehler: Wer durch x teilt, erhält nur x gleich fünf. Die Null ist verloren. Durch x teilen setzt voraus, '
            'dass x nicht null ist. Genau diesen Fall wirft man so weg.',
            f(r'x^2 = 5x', 280, 56, ein=0.3),
            op(':x', 280, 1.8, g=54),
            f(r'x = 5', 380, 56, ein=3.0),
            f(r'\fd{x = 0 \text{ fehlt}}', 480, 56, ein=4.4),
            n('Teilen durch @x@ setzt @x \\neq 0@ voraus.', 600, 'rot', 44, ein=6.0)),
         sz('Merke',
            'Zum Mitnehmen: Erst auf null bringen, dann ausklammern. Ein Produkt ist null, wenn ein Faktor null ist. Nie durch x teilen.',
            titel('Zum Mitnehmen', 250, 76),
            n('@a x^2 + b x = 0 \\Rightarrow x\\,(a x + b) = 0@|@x = 0@ oder @a x + b = 0@|nie durch @x@ teilen',
              390, 'blau', 44, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
W2k = fenster(-5, 3, -4, 6, (-4, -3, -2, -1, 1, 2), (-2, 2, 4))
clip('kontrolle-nullprodukt', 'Gleichungen lösen: Kontrollfragen zum Nullprodukt',
     'Fünf Fragen zum Satz vom Nullprodukt, zum «oder», zur verlorenen Lösung und zu x² + 3x = 0.',
     ['Nullprodukt', 'ausklammern', 'Kontrollfragen'], [
         sz('Frage 1',
            'Nur bei null folgt aus dem Produkt etwas über einen Faktor. Zwei mal drei ist sechs, aber auch eins mal sechs. '
            'Erst rechts null zwingt einen Faktor auf null.',
            f(r'a \cdot b = 6 \quad \fd{?}', 300, 56, ein=1.0),
            f(r'a \cdot b = 0 \;\Rightarrow\; a = 0 \text{ oder } b = 0', 420, 48, ein=6.0)),
         sz('Frage 2',
            'Ein Faktor null genügt schon, damit das Produkt null ist. Darum heisst es oder. Beide Lösungen gehören dazu.',
            f(r'x = \fc{0} \;\;\text{oder}\;\; x = \fc{5}', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \{0;\ 5\}', 420, 56, ein=4.4)),
         sz('Frage 3',
            'Durch x teilen setzt x ungleich null voraus. Die Lösung null ist dabei verloren gegangen.',
            f(r'x^2 = 4x \;\Rightarrow\; x(x - 4) = 0', 300, 50, ein=1.0),
            f(r'\mathbb{L} = \{\fd{0};\ 4\}', 420, 56, ein=3.6)),
         sz('Frage 4',
            'Rechts steht sechs, nicht null. Zuerst ausmultiplizieren und auf null bringen. Das Nullprodukt gilt nur mit null rechts.',
            f(r'x(x - 5) = \fd{6}', 300, 60, ein=1.0),
            f(r'x^2 - 5x - 6 = 0', 420, 56, ein=4.0)),
         sz('Frage 5',
            'Ausklammern: x mal Klammer x plus drei gleich null. Also x gleich null oder x gleich minus drei. '
            'Die Lösung, die nicht null ist, liegt bei minus drei.',
            f(r'x \cdot (x + 3) = 0', 300, 56, ein=1.0),
            f(r'x = 0 \;\;\text{oder}\;\; x = \fc{-3}', 420, 50, ein=3.6),
            graf(W2k, ein=0.05),
            graf(W2k, parabeln=[par(1, -1.5, -2.25)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Das Nullprodukt braucht rechts eine Null. Ein Faktor null genügt. Nie durch x teilen.',
            titel('Zum Mitnehmen', 250, 76),
            n('rechts @0@|ein Faktor @= 0@ genügt|nicht durch @x@ teilen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Warum muss beim Nullprodukt rechts null stehen?',
              ['Nur bei null muss ein Faktor null sein.', 'Sonst darf man nicht ausklammern.', 'Weil die Mitternachtsformel es verlangt.'], 0,
              {0: 'Ja.',
               1: 'Ausklammern geht immer. Was folgt aus a · b = 6 über a?',
               2: 'Hier geht es nicht um eine Formel. Was folgt aus a · b = 6 über a?'},
              sprich='Warum muss beim Nullprodukt rechts null stehen?',
              rueck_sprich={1: 'Ausklammern geht immer. Was folgt aus a mal b gleich sechs über a?',
                            2: 'Hier geht es nicht um eine Formel. Was folgt aus a mal b gleich sechs über a?'}),
         wahl('Frage 2', 'x(x − 5) = 0: Warum heisst es «x = 0 oder x = 5»?',
              ['Ein Faktor null genügt.', 'Beide Faktoren müssen null sein.', 'Es gibt nur eine Lösung.'], 0,
              {0: 'Ja.',
               1: 'Ist 0 · (−5) schon null?',
               2: 'Setz x = 0 und x = 5 ein. Stimmen beide?'},
              sprich='x mal Klammer x minus fünf gleich null: Warum heisst es x gleich null oder x gleich fünf?',
              rueck_sprich={1: 'Ist null mal minus fünf schon null?',
                            2: 'Setz x gleich null und x gleich fünf ein. Stimmen beide?'}),
         wahl('Frage 3', 'Aus x² = 4x wird durch x geteilt x = 4. Welche Lösung fehlt?',
              ['x = 0', 'x = −4', 'keine'], 0,
              {0: 'Ja.',
               1: 'Setz x = −4 in x² = 4x ein. Stimmt das?',
               2: 'Setz x = 0 in x² = 4x ein.'},
              sprich='Aus x Quadrat gleich vier x wird durch x geteilt x gleich vier. Welche Lösung fehlt?',
              rueck_sprich={1: 'Setz x gleich minus vier in x Quadrat gleich vier x ein. Stimmt das?',
                            2: 'Setz x gleich null in x Quadrat gleich vier x ein.'}),
         wahl('Frage 4', 'Ist x(x − 5) = 6 schon ein Fall für das Nullprodukt?',
              ['Nein, rechts steht nicht 0.', 'Ja: x = 6 oder x − 5 = 6.', 'Ja: x = 0 oder x = 5.'], 0,
              {0: 'Ja.',
               1: 'Prüf x = 6: 6 · 1 = 6. Und x = 11? Was folgt aus einem Produkt 6 wirklich?',
               2: 'Setz x = 0 ein: 0 · (−5) = 0, nicht 6.'},
              sprich='Ist x mal Klammer x minus fünf gleich sechs schon ein Fall für das Nullprodukt?',
              rueck_sprich={1: 'Prüf x gleich elf. Elf mal sechs ist nicht sechs. Was folgt aus einem Produkt sechs wirklich?',
                            2: 'Setz x gleich null ein. Null mal minus fünf ist null, nicht sechs.'}),
         klick('Frage 5', 'x² + 3x = 0: Tipp die Lösung, die nicht null ist, auf der x-Achse an.',
               [-3, 0], 'Getroffen: x = −3.',
               [{'bei': [3, 0], 'text': 'Vorzeichen: x + 3 = 0 heisst x = −3.',
                 'sprich': 'Vorzeichen. x plus drei gleich null heisst x gleich minus drei.'},
                {'bei': [0, 0], 'text': 'Das ist die Lösung x = 0. Gesucht ist die andere.',
                 'sprich': 'Das ist die Lösung x gleich null. Gesucht ist die andere.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='x Quadrat plus drei x gleich null: Tipp die Lösung, die nicht null ist, auf der x-Achse an.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
W3a = fenster(-5, 5, -2, 12, (-4, -3, -2, 2, 3, 4), (3, 6, 9))
W3b = fenster(-3, 7, -10, 8, (-2, -1, 1, 2, 3, 4, 5, 6), (-8, -4, 4))
W3c = fenster(-4, 3, -5, 6, (-3, -2, -1, 1, 2), (-4, -2, 2, 4))
W3d = fenster(-3, 5, -5, 7, (-2, -1, 1, 2, 3, 4), (-4, -2, 2, 4, 6))
clip('ergaenzen', 'Gleichungen lösen: Wurzelziehen, Ergänzen, Mitternachtsformel',
     'x² = 9 hat zwei Lösungen; (x − 2)² = 9 genauso; mit der quadratischen Ergänzung wird jede Gleichung zu einem Quadrat — '
     'allgemein ergibt das die Mitternachtsformel. Die Diskriminante zählt die Lösungen.',
     ['quadratische Gleichung', 'Wurzelziehen', 'quadratische Ergänzung', 'Mitternachtsformel', 'Diskriminante'], [
         sz('Wurzelziehen',
            'x Quadrat gleich neun: Welche Zahlen haben das Quadrat neun? Drei und minus drei. Beim Wurzelziehen gehören beide '
            'Vorzeichen dazu. Im Bild trifft die Waagrechte y gleich neun die Parabel zweimal.',
            f(r'x^2 = 9', 280, 62, ein=0.3),
            f(r'x = \pm 3', 390, 60, ein=4.4),
            f(r'\mathbb{L} = \{\fc{-3};\ \fc{3}\}', 500, 56, ein=5.8),
            graf(W3a, kurven=[dict(formel='9', farbe=5, gestrichelt=True, dicke=3)], parabeln=[par(1, 0, 0, null=False)], ein=0.3),
            graf(W3a, punkte=[pt(-3, 9, 3, '(−3 | 9)', [-3.3, 10.4], 'end'), pt(3, 9, 3, '(3 | 9)', [3.3, 10.4])], ein=8.9)),
         sz('Ein Quadrat mit Klammer',
            'Genauso bei Klammer x minus zwei, im Quadrat, gleich neun. Die Klammer ist drei oder minus drei. '
            'Also x gleich fünf oder x gleich minus eins.',
            f(r'(x - 2)^2 = 9', 280, 60, ein=0.3),
            f(r'x - 2 = \pm 3', 390, 58, ein=3.8),
            f(r'x = \fc{5} \;\;\text{oder}\;\; x = \fc{-1}', 500, 50, ein=6.0)),
         sz('Quadratisch ergänzen',
            'Und wenn die Gleichung so aussieht: x Quadrat minus vier x minus fünf gleich null? Zuerst plus fünf. '
            'Dann die Hälfte von vier ins Quadrat, also vier, auf beiden Seiten addieren. Links steht jetzt ein Binom: '
            'Klammer x minus zwei, im Quadrat. Rechts neun. Das kennst du schon.',
            f(r'x^2 - 4x - 5 = 0', 260, 50, ein=0.3),
            op('+5', 260, 4.8),
            f(r'x^2 - 4x = 5', 350, 50, ein=5.2),
            op(r'+\left(\tfrac{4}{2}\right)^2', 350, 5.9, g=44),
            f(r'x^2 - 4x + 4 = 9', 440, 50, ein=8.5),
            f(r'(x - 2)^2 = 9', 530, 50, ein=11.6),
            f(r'\mathbb{L} = \{\fc{-1};\ \fc{5}\}', 640, 52, ein=14.1),
            graf(W3b, parabeln=[par(1, 2, -9)], ein=0.3)),
         sz('Die Mitternachtsformel',
            'Führt man die Ergänzung allgemein durch, entsteht die Mitternachtsformel. Unter der Wurzel steht die Diskriminante: '
            'D gleich b Quadrat minus vier a c.',
            f(r'a x^2 + b x + c = 0', 260, 52, ein=0.3),
            f(r'x_{1,2} = \dfrac{-b \pm \sqrt{D}}{2a}', 380, 58, ein=2.0),
            f(r'D = b^2 - 4ac', 570, 56, ein=5.0)),
         sz('Ein Beispiel',
            'Zum Beispiel zwei x Quadrat plus drei x minus zwei gleich null. a ist zwei, b drei, c minus zwei. '
            'D ist neun plus sechzehn, also fünfundzwanzig. x ist minus drei plus oder minus fünf, durch vier. '
            'Das gibt null Komma fünf und minus zwei.',
            f(r'2x^2 + 3x - 2 = 0', 250, 50, ein=0.3),
            f(r'a = 2,\ b = 3,\ c = -2', 335, 46, ein=4.0),
            f(r'D = 9 + 16 = 25', 420, 48, ein=6.4),
            f(r'x_{1,2} = \dfrac{-3 \pm 5}{4}', 525, 50, ein=9.7),
            f(r'\mathbb{L} = \{\fc{-2};\ \fc{0.5}\}', 675, 50, ein=13.3),
            graf(W3c, parabeln=[par(2, -0.75, -3.125)], ein=13.3)),
         sz('Was D verrät',
            'Die Diskriminante entscheidet über die Anzahl der Lösungen. Ist D positiv, gibt es zwei: Die Parabel schneidet die '
            'x-Achse zweimal. Ist D null, gibt es eine: Sie berührt die Achse. Ist D negativ, gibt es keine.',
            n('@D \\gt 0@: zwei Lösungen', 300, 'blau', 46, ein=3.7),
            n('@D = 0@: eine Lösung', 400, 'blau', 46, ein=8.2),
            n('@D \\lt 0@: keine Lösung', 500, 'blau', 46, ein=11.4),
            graf(W3d, parabeln=[par(1, 1, -4, beschr=False,
                                    bew=[[0, 1, 1, -4], [7.4, 1, 1, -4], [8.6, 1, 1, 0], [10.8, 1, 1, 0], [11.9, 1, 1, 2.5]])], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Beim Wurzelziehen gibt es plus und minus. Die quadratische Ergänzung macht aus jeder Gleichung ein Quadrat. '
            'Die Mitternachtsformel geht immer, und D sagt, wie viele Lösungen es gibt.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x^2 = r \;\Rightarrow\; x = \pm\sqrt{r} \quad (r \ge 0)', 400, 52, ein=1.2),
            f(r'x_{1,2} = \dfrac{-b \pm \sqrt{D}}{2a}, \qquad D = b^2 - 4ac', 560, 52, ein=4.6)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W3k = fenster(-3, 5, -5, 6, (-2, -1, 1, 2, 3, 4), (-4, -2, 2, 4))
clip('kontrolle-ergaenzen', 'Gleichungen lösen: Kontrollfragen zu Wurzel, Ergänzung und Formel',
     'Fünf Fragen zu x² = 25, zu (x − 3)² = 4, zur Ergänzung, zur Diskriminante und zu x² − 2x − 3 = 0.',
     ['Wurzelziehen', 'quadratische Ergänzung', 'Diskriminante', 'Kontrollfragen'], [
         sz('Frage 1',
            'Fünf mal fünf ist fünfundzwanzig, minus fünf mal minus fünf auch. Beide sind Lösungen.',
            f(r'x = \pm 5', 300, 60, ein=1.0),
            f(r'\mathbb{L} = \{-5;\ 5\}', 420, 56, ein=3.4)),
         sz('Frage 2',
            'Die Klammer ist zwei oder minus zwei. x ist drei plus zwei oder drei minus zwei.',
            f(r'x - 3 = \pm 2', 300, 58, ein=1.0),
            f(r'\mathbb{L} = \{1;\ 5\}', 420, 56, ein=4.0)),
         sz('Frage 3',
            'Die Hälfte von zehn ist fünf, ins Quadrat fünfundzwanzig. x Quadrat plus zehn x plus fünfundzwanzig ist Klammer x plus fünf, im Quadrat.',
            f(r'\left(\tfrac{10}{2}\right)^2 = 25', 300, 56, ein=1.0),
            f(r'x^2 + 10x + 25 = (x + 5)^2', 420, 50, ein=4.6)),
         sz('Frage 4',
            'Ist D negativ, steht unter der Wurzel eine negative Zahl. Es gibt keine reelle Lösung.',
            f(r'\sqrt{-8} \;\fd{\text{gibt es nicht}}', 300, 54, ein=1.0),
            f(r'\mathbb{L} = \{\,\}', 420, 56, ein=3.6)),
         sz('Frage 5',
            'x ist zwei plus oder minus vier, durch zwei. Das gibt drei und minus eins. Die grössere Lösung ist drei.',
            f(r'x_{1,2} = \dfrac{2 \pm 4}{2}', 300, 54, ein=1.0),
            f(r'x = \fc{-1} \;\;\text{oder}\;\; x = \fc{3}', 470, 50, ein=4.4),
            graf(W3k, ein=0.05),
            graf(W3k, parabeln=[par(1, 1, -4)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Wurzelziehen gibt plus und minus. Ergänzt wird das Quadrat der halben Zahl vor x. '
            'Ein negatives D heisst: keine Lösung.',
            titel('Zum Mitnehmen', 250, 76),
            n('@\\pm@ beim Wurzelziehen|ergänzen: @\\left(\\tfrac{b}{2}\\right)^2@|@D \\lt 0@: @\\mathbb{L} = \\{\\,\\}@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'x² = 25: Welche Lösungsmenge?',
              ['{−5; 5}', '{5}', '{25}'], 0,
              {0: 'Ja.',
               1: 'Was ist (−5)²?',
               2: 'Gesucht ist x, nicht x². Welche Zahl hat das Quadrat 25?'},
              sprich='x Quadrat gleich fünfundzwanzig: Welche Lösungsmenge?',
              rueck_sprich={1: 'Was ist minus fünf im Quadrat?',
                            2: 'Gesucht ist x, nicht x Quadrat. Welche Zahl hat das Quadrat fünfundzwanzig?'}),
         wahl('Frage 2', 'Löse (x − 3)² = 4.',
              ['{1; 5}', '{−1; 5}', '{5}'], 0,
              {0: 'Ja.',
               1: 'Prüf x = −1: (−1 − 3)² = 16, nicht 4.',
               2: 'Die Klammer kann auch −2 sein.'},
              sprich='Löse: Klammer x minus drei, im Quadrat, gleich vier.',
              rueck_sprich={1: 'Prüf x gleich minus eins. Minus vier im Quadrat ist sechzehn, nicht vier.',
                            2: 'Die Klammer kann auch minus zwei sein.'}),
         wahl('Frage 3', 'x² + 10x: Welche Zahl ergänzt zum vollständigen Quadrat?',
              ['25', '100', '10'], 0,
              {0: 'Ja.',
               1: 'Nimm die Hälfte von 10, dann erst ins Quadrat.',
               2: 'Ergänzt wird ein Quadrat: die Hälfte von 10, im Quadrat.'},
              sprich='x Quadrat plus zehn x: Welche Zahl ergänzt zum vollständigen Quadrat?',
              rueck_sprich={1: 'Nimm die Hälfte von zehn, dann erst ins Quadrat.',
                            2: 'Ergänzt wird ein Quadrat: die Hälfte von zehn, im Quadrat.'}),
         wahl('Frage 4', 'Die Diskriminante ist D = −8. Wie viele Lösungen?',
              ['keine', 'zwei', 'eine'], 0,
              {0: 'Ja.',
               1: 'Was steht dann unter der Wurzel?',
               2: 'Eine Lösung gibt es bei D = 0.'},
              sprich='Die Diskriminante ist minus acht. Wie viele Lösungen gibt es?',
              rueck_sprich={1: 'Was steht dann unter der Wurzel?',
                            2: 'Eine Lösung gibt es bei D gleich null.'}),
         klick('Frage 5', 'x² − 2x − 3 = 0 hat D = 16. Tipp die grössere Lösung auf der x-Achse an.',
               [3, 0], 'Getroffen: x = 3.',
               [{'bei': [-1, 0], 'text': 'Das ist die kleinere Lösung.',
                 'sprich': 'Das ist die kleinere Lösung.'},
                {'bei': [-3, 0], 'text': 'Vorzeichen: Vor der Formel steht −b, und b ist −2.',
                 'sprich': 'Vorzeichen. Vor der Formel steht minus b, und b ist minus zwei.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='x Quadrat minus zwei x minus drei gleich null hat D gleich sechzehn. Tipp die grössere Lösung auf der x-Achse an.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
W4a = fenster(-4, 5, -1, 14, (-3, -2, -1, 1, 2, 3, 4), (3, 6, 9, 12))
W4b = fenster(-1, 6, -2, 6, (1, 2, 3, 4, 5), (-1, 2, 4))
clip('verfahren', 'Gleichungen lösen: das passende Verfahren wählen',
     'Erst ordnen und den Typ bestimmen, dann wählen: Wurzelziehen, Ausklammern, Faktorisieren mit dem Zweiklammeransatz oder die '
     'Mitternachtsformel — und am Schluss die Probe.',
     ['quadratische Gleichung', 'Verfahrenswahl', 'Faktorisieren', 'Zweiklammeransatz', 'Typ'], [
         sz('Erst ordnen',
            'Bevor du ein Verfahren wählst: alles ausmultiplizieren und ordnen. Erst dann siehst du den Typ. Klammer x plus eins, '
            'im Quadrat, gleich x Quadrat plus fünf. Ausmultipliziert heben sich die x Quadrat weg. Es bleibt zwei x plus eins '
            'gleich fünf, eine lineare Gleichung. x ist zwei.',
            f(r'(x + 1)^2 = x^2 + 5', 260, 50, ein=0.3),
            f(r'x^2 + 2x + 1 = x^2 + 5', 350, 46, ein=10.1),
            op('-x^2', 350, 10.8, g=44),
            f(r'2x + 1 = 5', 440, 50, ein=12.8),
            f(r'x = \fc{2}', 530, 50, ein=16.4),
            graf(W4a, parabeln=[par(1, -1, 0, null=False), par(1, 0, 5, farbe=5, null=False)], ein=0.3),
            graf(W4a, punkte=[pt(2, 9, 3, '(2 | 9)', [2.3, 7.6])], ein=16.4)),
         sz('Wenn b fehlt',
            'Fehlt das Glied mit x, zieh die Wurzel. Drei x Quadrat gleich siebenundzwanzig: x Quadrat ist neun, x ist plus oder minus drei.',
            n('kein @x@-Glied: Wurzelziehen', 260, 'blau', 46, ein=0.3),
            f(r'3x^2 = 27', 380, 56, ein=2.8),
            op(':3', 380, 3.8),
            f(r'x^2 = 9 \;\Rightarrow\; x = \fc{\pm 3}', 480, 52, ein=5.2)),
         sz('Wenn c fehlt',
            'Fehlt die Zahl ohne x, klammere aus. x Quadrat plus vier x gleich null: x mal Klammer x plus vier. Die Lösungen sind null und minus vier.',
            n('keine Zahl ohne @x@: Ausklammern', 260, 'blau', 46, ein=0.3),
            f(r'x^2 + 4x = 0', 380, 56, ein=2.6),
            f(r'x \cdot (x + 4) = 0', 480, 52, ein=4.5),
            f(r'\mathbb{L} = \{\fc{-4};\ \fc{0}\}', 590, 52, ein=6.3)),
         sz('Faktorisieren',
            'Lässt sich die Gleichung zerlegen, faktorisiere mit dem Zweiklammeransatz. x Quadrat minus sieben x plus zwölf: '
            'Gesucht sind zwei Zahlen mit dem Produkt zwölf und der Summe minus sieben. Das sind minus drei und minus vier. '
            'Also Klammer x minus drei mal Klammer x minus vier gleich null. Die Lösungen sind drei und vier.',
            f(r'x^2 - 7x + 12 = 0', 260, 52, ein=0.3),
            n('Produkt @12@, Summe @-7@:|@(-3) \\cdot (-4) = 12@; @(-3) + (-4) = -7@', 350, 'blau', 42, ein=6.6),
            f(r'(x - 3)(x - 4) = 0', 510, 52, ein=12.8),
            f(r'\mathbb{L} = \{\fc{3};\ \fc{4}\}', 620, 52, ein=16.1),
            graf(W4b, parabeln=[par(1, 3.5, -0.25, beschr=False)], ein=16.1,
                 punkte=[pt(3, 0, 3, '3', [2.8, 0.6], 'end'), pt(4, 0, 3, '4', [4.2, 0.6])])),
         sz('Ein Binom',
            'Manchmal ist es ein Binom: x Quadrat minus sechs x plus neun ist Klammer x minus drei, im Quadrat. Es gibt nur eine Lösung: drei.',
            f(r'x^2 - 6x + 9 = (x - 3)^2 = 0', 300, 48, ein=0.3),
            f(r'\mathbb{L} = \{\fc{3}\}', 420, 56, ein=5.7)),
         sz('Sonst die Formel',
            'Geht nichts davon, hilft die Mitternachtsformel. Sie funktioniert immer. Zwei x Quadrat plus x minus vier: '
            'D ist eins plus zweiunddreissig, also dreiunddreissig. Die Lösungen sind minus eins plus oder minus Wurzel aus dreiunddreissig, durch vier.',
            f(r'2x^2 + x - 4 = 0', 260, 52, ein=0.3),
            f(r'D = 1 + 32 = 33', 370, 50, ein=6.9),
            f(r'x_{1,2} = \dfrac{-1 \pm \sqrt{33}}{4}', 490, 52, ein=10.3)),
         sz('Merke',
            'Zum Mitnehmen: Ordnen, Typ bestimmen, dann wählen. Fehlt b, Wurzel ziehen. Fehlt c, ausklammern. Lässt es sich zerlegen, '
            'faktorisieren. Sonst die Mitternachtsformel. Und am Schluss die Probe.',
            titel('Zum Mitnehmen', 240, 76),
            n('ordnen, Typ bestimmen|@b = 0@: Wurzelziehen; @c = 0@: Ausklammern|zerlegbar: Faktorisieren; sonst: Mitternachtsformel|Probe',
              380, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
W4k = fenster(-6, 5, -14, 6, (-5, -4, -3, -2, -1, 1, 2, 3, 4), (-12, -8, -4, 4))
clip('kontrolle-verfahren', 'Gleichungen lösen: Kontrollfragen zur Verfahrenswahl',
     'Fünf Fragen: welches Verfahren wann, eine Lücke im Zweiklammeransatz, der Typ nach dem Ordnen und x² + x − 12 = 0.',
     ['Verfahrenswahl', 'Faktorisieren', 'Kontrollfragen'], [
         sz('Frage 1',
            'Es fehlt das Glied mit x. x Quadrat ist sechzehn, x plus oder minus vier. Die Formel ginge auch, aber länger.',
            f(r'x^2 = 16 \;\Rightarrow\; x = \pm 4', 300, 54, ein=1.0)),
         sz('Frage 2',
            'Es fehlt die Zahl ohne x. Ausklammern: x mal Klammer x plus sieben.',
            f(r'x \cdot (x + 7) = 0', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \{-7;\ 0\}', 420, 56, ein=3.4)),
         sz('Frage 3',
            'Das Produkt der beiden Zahlen muss zehn sein: minus zwei mal minus fünf. Die Summe minus sieben stimmt auch.',
            f(r'(x - 2)(x - \fc{5})', 300, 58, ein=1.0),
            n('@(-2) \\cdot (-5) = 10@; @(-2) + (-5) = -7@', 430, 'blau', 42, ein=3.4)),
         sz('Frage 4',
            'Ausmultipliziert: x Quadrat plus sechs x plus neun gleich x Quadrat plus fünfzehn. Die x Quadrat heben sich weg. '
            'Es bleibt sechs x gleich sechs, also x gleich eins.',
            f(r'x^2 + 6x + 9 = x^2 + 15', 300, 48, ein=1.0),
            f(r'6x = 6 \;\Rightarrow\; x = 1', 420, 54, ein=7.0)),
         sz('Frage 5',
            'Gesucht sind zwei Zahlen mit dem Produkt minus zwölf und der Summe eins: vier und minus drei. '
            'Klammer x plus vier mal Klammer x minus drei. Die negative Lösung ist minus vier.',
            f(r'(x + 4)(x - 3) = 0', 300, 56, ein=1.0),
            f(r'x = \fc{-4} \;\;\text{oder}\;\; x = \fc{3}', 420, 50, ein=6.0),
            graf(W4k, ein=0.05),
            graf(W4k, parabeln=[par(1, -0.5, -12.25)], ein=1.2)),
         sz('Merke',
            'Zum Mitnehmen: Zuerst ordnen und den Typ bestimmen. Dann das kürzeste Verfahren, das passt. Die Formel geht immer.',
            titel('Zum Mitnehmen', 250, 76),
            n('ordnen|Typ bestimmen|kürzestes passendes Verfahren', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'x² − 16 = 0: Welches Verfahren ist am schnellsten?',
              ['Wurzelziehen', 'Mitternachtsformel', 'Ausklammern'], 0,
              {0: 'Ja.',
               1: 'Geht, aber es fehlt das Glied mit x. Was ist kürzer?',
               2: 'Nicht jedes Glied enthält ein x. Was ist kürzer?'},
              sprich='x Quadrat minus sechzehn gleich null: Welches Verfahren ist am schnellsten?',
              rueck_sprich={1: 'Geht, aber es fehlt das Glied mit x. Was ist kürzer?',
                            2: 'Nicht jedes Glied enthält ein x. Was ist kürzer?'}),
         wahl('Frage 2', 'Welches Verfahren passt zu x² + 7x = 0?',
              ['Ausklammern', 'Wurzelziehen', 'quadratische Ergänzung'], 0,
              {0: 'Ja.',
               1: 'Es gibt ein Glied mit x. Was steckt in beiden Gliedern?',
               2: 'Geht, aber es fehlt die Zahl ohne x. Was ist kürzer?'},
              sprich='Welches Verfahren passt zu x Quadrat plus sieben x gleich null?',
              rueck_sprich={1: 'Es gibt ein Glied mit x. Was steckt in beiden Gliedern?',
                            2: 'Geht, aber es fehlt die Zahl ohne x. Was ist kürzer?'}),
         wahl('Frage 3', 'x² − 7x + 10 = (x − 2)(x − □). Welche Zahl fehlt?',
              ['5', '−5', '8'], 0,
              {0: 'Ja.',
               1: 'Multipliziere aus: Das Produkt der Zahlen muss +10 sein.',
               2: 'Das Produkt der Zahlen muss 10 sein, nicht die Summe.'},
              sprich='x Quadrat minus sieben x plus zehn gleich Klammer x minus zwei mal Klammer x minus Kästchen. Welche Zahl fehlt?',
              rueck_sprich={1: 'Multipliziere aus. Das Produkt der Zahlen muss plus zehn sein.',
                            2: 'Das Produkt der Zahlen muss zehn sein, nicht die Summe.'}),
         wahl('Frage 4', '(x + 3)² = x² + 15: Was für eine Gleichung bleibt nach dem Ordnen?',
              ['eine lineare, mit x = 1', 'eine quadratische', 'gar keine'], 0,
              {0: 'Ja.',
               1: 'Multipliziere links aus. Was geschieht mit x²?',
               2: 'Multipliziere aus und ordne. Bleibt ein x?'},
              sprich='Klammer x plus drei, im Quadrat, gleich x Quadrat plus fünfzehn: Was für eine Gleichung bleibt nach dem Ordnen?',
              rueck_sprich={1: 'Multipliziere links aus. Was geschieht mit x Quadrat?',
                            2: 'Multipliziere aus und ordne. Bleibt ein x?'}),
         klick('Frage 5', 'Faktorisiere x² + x − 12 = 0 im Kopf und tipp die negative Lösung an.',
               [-4, 0], 'Getroffen: x = −4.',
               [{'bei': [4, 0], 'text': 'Vorzeichen: Aus (x + 4) folgt x = −4.',
                 'sprich': 'Vorzeichen. Aus x plus vier folgt x gleich minus vier.'},
                {'bei': [3, 0], 'text': 'Das ist die positive Lösung.',
                 'sprich': 'Das ist die positive Lösung.'},
                {'bei': [-3, 0], 'text': 'Prüf: (−3)² − 3 − 12 = −6, nicht 0.',
                 'sprich': 'Prüf: minus drei im Quadrat, minus drei, minus zwölf gibt minus sechs, nicht null.'}],
               'Nicht ganz. Der grüne Kreis zeigt die Stelle.',
               sprich='Faktorisiere x Quadrat plus x minus zwölf gleich null im Kopf und tipp die negative Lösung an.',
               falsch_sprich='Nicht ganz. Der grüne Kreis zeigt die Stelle.'),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
W5a = fenster(-2, 6, -4, 12, (-1, 1, 2, 3, 4, 5), (3, 6, 9))
W5b = fenster(-1, 7, -5, 8, (1, 2, 3, 4, 5, 6), (-4, -2, 2, 4, 6))
clip('parameter', 'Gleichungen lösen: Parameterdiskussion',
     'k · x + 6 = 2x + 3k für jedes k; x² − 6x + k = 0 mit der Diskriminante D(k) = 36 − 4k; und warum man zuerst prüft, '
     'ob der Leitkoeffizient null werden kann.',
     ['Parameter', 'Parameterdiskussion', 'Diskriminante', 'Lösungsfälle'], [
         sz('Ein zweiter Buchstabe',
            'In einer Parametergleichung steht neben x ein zweiter Buchstabe, hier k. Gesucht ist die Lösung für jedes k.',
            titel('Parameter', 260, 80),
            f(r'\fb{k} \cdot x + 6 = 2x + 3\fb{k}', 400, 56, ein=1.0),
            n('Lösung für jedes @k@', 520, 'blau', ein=5.0)),
         sz('Sortieren',
            'Sortiere auf die Form a mal x gleich c: die x-Glieder links, der Rest rechts. Klammer k minus zwei, mal x, gleich '
            'drei k minus sechs. Rechts lässt sich drei ausklammern: drei mal Klammer k minus zwei.',
            f(r'kx + 6 = 2x + 3k', 260, 52, ein=0.3),
            op('-2x - 6', 260, 2.6, g=44),
            f(r'(k - 2) \cdot x = 3k - 6', 350, 52, ein=5.3),
            f(r'(k - 2) \cdot x = 3 \cdot (k - 2)', 450, 52, ein=10.7)),
         sz('Die Fälle',
            'Ist k nicht zwei, darf man durch k minus zwei teilen: x ist drei. Bei k gleich zwei steht null gleich null. Dann ist '
            'jede Zahl Lösung. Im Bild schneiden sich die beiden Seiten immer bei x gleich drei. Bei k gleich zwei liegen beide '
            'auf der x-Achse.',
            f(r'k \neq 2: \quad x = \fc{3}', 280, 52, ein=0.3),
            f(r'k = 2: \quad 0 = 0, \;\; \mathbb{L} = \mathbb{R}', 390, 50, ein=4.5),
            graf(W5a, geraden=[{'bewegung': [[0, 3, 0], [8.4, 3, 0], [10.2, 1, 0], [11.6, 1, 0], [13.4, 0, 0]], 'farbe': 1},
                               {'bewegung': [[0, 0, 9], [8.4, 0, 9], [10.2, 0, 3], [11.6, 0, 3], [13.4, 0, 0]], 'farbe': 2}],
                 punkte=[pt(3, 0, 3, 'x = 3', [3.2, -1.6])], ein=0.3)),
         sz('Quadratisch',
            'Bei x Quadrat minus sechs x plus k entscheidet die Diskriminante. D von k ist sechsunddreissig minus vier k. '
            'Für k kleiner als neun ist D positiv: zwei Lösungen. Bei k gleich neun ist D null: genau eine Lösung, x gleich drei. '
            'Für k grösser als neun gibt es keine.',
            f(r'x^2 - 6x + \fb{k} = 0', 250, 52, ein=0.3),
            f(r'D(k) = 36 - 4k', 350, 52, ein=4.1),
            n('@k \\lt 9@: zwei Lösungen', 450, 'blau', 42, ein=6.5),
            n('@k = 9@: eine, @x = 3@', 530, 'blau', 42, ein=9.9),
            n('@k \\gt 9@: keine', 610, 'blau', 42, ein=14.1),
            graf(W5b, parabeln=[par(1, 3, -4, beschr=False,
                                    bew=[[0, 1, 3, -4], [9.6, 1, 3, -4], [11.4, 1, 3, 0], [13.8, 1, 3, 0], [15.2, 1, 3, 2]])], ein=0.3)),
         sz('Zuerst a prüfen',
            'Steht der Parameter vor x Quadrat, prüfe zuerst, ob er null sein kann. m x Quadrat minus vier x minus drei: '
            'Bei m gleich null ist die Gleichung linear, x ist minus drei Viertel. Erst für m ungleich null gilt die Diskriminante, '
            'sechzehn plus zwölf m.',
            f(r'\fb{m}\,x^2 - 4x - 3 = 0', 260, 52, ein=0.3),
            f(r'm = 0: \;\; -4x - 3 = 0 \;\Rightarrow\; x = -\tfrac{3}{4}', 370, 46, ein=5.9),
            f(r'm \neq 0: \;\; D(m) = 16 + 12m', 480, 46, ein=9.7)),
         sz('Merke',
            'Zum Mitnehmen: Linear auf die Form a mal x gleich c bringen und den Wert suchen, bei dem a null wird. Quadratisch '
            'zuerst prüfen, ob der Leitkoeffizient null wird, dann D von k untersuchen.',
            titel('Zum Mitnehmen', 250, 76),
            n('linear: @a(k) \\cdot x = c(k)@, Fall @a(k) = 0@|quadratisch: zuerst @a = 0@?, dann @D(k)@', 390, 'blau', 42, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
clip('kontrolle-parameter', 'Gleichungen lösen: Kontrollfragen zur Parameterdiskussion',
     'Fünf Fragen zu (k − 3) · x = 5, zu (k − 3) · x = k − 3, zu D(k) bei x² + 2x + k = 0 und zum Fall k = 0.',
     ['Parameterdiskussion', 'Diskriminante', 'Kontrollfragen'], [
         sz('Frage 1',
            'Bei k gleich drei steht null mal x gleich fünf. Das ist für kein x wahr.',
            f(r'k = 3: \quad 0 \cdot x = 5', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \{\,\}', 420, 56, ein=3.4)),
         sz('Frage 2',
            'Bei k gleich drei werden beide Seiten null: null gleich null. Jede Zahl ist Lösung.',
            f(r'k = 3: \quad 0 \cdot x = 0', 300, 56, ein=1.0),
            f(r'\mathbb{L} = \mathbb{R}', 420, 56, ein=4.0)),
         sz('Frage 3',
            'a ist eins, b zwei, c ist k. D ist zwei im Quadrat minus vier mal eins mal k, also vier minus vier k.',
            f(r'D = 2^2 - 4 \cdot 1 \cdot k = 4 - 4k', 300, 50, ein=1.0)),
         sz('Frage 4',
            'Genau eine Lösung bei D gleich null: vier minus vier k gleich null, also k gleich eins.',
            f(r'4 - 4k = 0 \;\Rightarrow\; k = 1', 300, 54, ein=1.0),
            f(r'x^2 + 2x + 1 = (x + 1)^2', 420, 50, ein=4.4)),
         sz('Frage 5',
            'Bei k gleich null fällt x Quadrat weg. Es bleibt drei x plus eins gleich null, eine lineare Gleichung mit x gleich minus ein Drittel.',
            f(r'k = 0: \quad 3x + 1 = 0', 300, 54, ein=1.0),
            f(r'x = -\tfrac{1}{3}', 420, 56, ein=5.0)),
         sz('Merke',
            'Zum Mitnehmen: Wird der Faktor vor x null, entscheidet die rechte Seite. Steht der Parameter vor x Quadrat, '
            'zuerst den linearen Fall prüfen.',
            titel('Zum Mitnehmen', 250, 76),
            n('@0 \\cdot x = c@: @c \\neq 0@ keine, @c = 0@ alle|Parameter vor @x^2@: zuerst @= 0@ prüfen', 400, 'blau', 42, ein=1.2)),
     ], [
         wahl('Frage 1', '(k − 3) · x = 5: Für welches k gibt es keine Lösung?',
              ['k = 3', 'k = −3', 'k = 5'], 0,
              {0: 'Ja.',
               1: 'Setz k = −3 ein: −6x = 5 hat eine Lösung. Wann wird der Faktor vor x null?',
               2: 'Setz k = 5 ein: 2x = 5 hat eine Lösung. Wann wird der Faktor vor x null?'},
              sprich='Klammer k minus drei, mal x, gleich fünf: Für welches k gibt es keine Lösung?',
              rueck_sprich={1: 'Setz k gleich minus drei ein. Minus sechs x gleich fünf hat eine Lösung. Wann wird der Faktor vor x null?',
                            2: 'Setz k gleich fünf ein. Zwei x gleich fünf hat eine Lösung. Wann wird der Faktor vor x null?'}),
         wahl('Frage 2', 'Bei k = 3: Welche Lösungsmenge hat (k − 3) · x = k − 3?',
              ['𝕃 = ℝ', '𝕃 = { }', '𝕃 = {1}'], 0,
              {0: 'Ja.',
               1: 'Setz k = 3 ein. Steht rechts auch null?',
               2: 'x = 1 gilt für k ≠ 3. Setz k = 3 ein.'},
              sprich='Bei k gleich drei: Welche Lösungsmenge hat Klammer k minus drei, mal x, gleich k minus drei?',
              rueck_sprich={1: 'Setz k gleich drei ein. Steht rechts auch null?',
                            2: 'x gleich eins gilt für k ungleich drei. Setz k gleich drei ein.'}),
         wahl('Frage 3', 'x² + 2x + k = 0: Wie lautet D(k)?',
              ['4 − 4k', '4 − k', '2 − 4k'], 0,
              {0: 'Ja.',
               1: 'D = b² − 4ac. Was ist 4 · a · c?',
               2: 'b ist 2. Was ist b²?'},
              sprich='x Quadrat plus zwei x plus k gleich null: Wie lautet D von k?',
              rueck_sprich={1: 'D gleich b Quadrat minus vier a c. Was ist vier mal a mal c?',
                            2: 'b ist zwei. Was ist b Quadrat?'}),
         wahl('Frage 4', 'Für welches k hat x² + 2x + k = 0 genau eine Lösung?',
              ['k = 1', 'k = 4', 'k = −1'], 0,
              {0: 'Ja.',
               1: 'Rechne D(4) = 4 − 16. Wie viele Lösungen sind das?',
               2: 'Rechne D(−1) = 4 + 4. Wie viele Lösungen sind das?'},
              sprich='Für welches k hat x Quadrat plus zwei x plus k gleich null genau eine Lösung?',
              rueck_sprich={1: 'Rechne D von vier: vier minus sechzehn. Wie viele Lösungen sind das?',
                            2: 'Rechne D von minus eins: vier plus vier. Wie viele Lösungen sind das?'}),
         wahl('Frage 5', 'k · x² + 3x + 1 = 0 bei k = 0: Was gilt?',
              ['linear, x = −1/3', 'D = 9 > 0, also zwei Lösungen', 'keine Gleichung mehr'], 0,
              {0: 'Ja.',
               1: 'D gehört zu quadratischen Gleichungen. Was bleibt bei k = 0 stehen?',
               2: 'Setz k = 0 ein. Was bleibt stehen?'},
              sprich='k mal x Quadrat plus drei x plus eins gleich null, bei k gleich null: Was gilt?',
              rueck_sprich={1: 'D gehört zu quadratischen Gleichungen. Was bleibt bei k gleich null stehen?',
                            2: 'Setz k gleich null ein. Was bleibt stehen?'}),
     ], art='Kontrollclip')
