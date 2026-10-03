"""ARCHIV — hat am 02.10.2026 die fünf Kontrollclips erzeugt. NICHT erneut laufen lassen:
Die Drehbücher clips/g3-3-lp-kontrolle-*.json sind seither die Quelle und wurden danach von Hand
geändert (Einleitungsszene entfernt, Pfeile/Achsennamen, Beschriftungen, vertonte Dauern).
Ein neuer Lauf würde all das überschreiben. Liegt hier als Muster für weitere Kontrollclips."""
import json
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
def graf(par, W, punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             punkte=list(punkte), parabeln=par, **W); g.update(kw); return g
def bew(k, **kw): d = {'bewegung': k, 'farbe': 1}; d.update(kw); return d
N = {"a": 1, "gestrichelt": True, "dicke": 3}
def f(t, y, g=62, ein=0.8): return dict(typ='formel', text=t, x=LX, y=y, groesse=g, ein=ein)
def n(t, y, farbe='blau', g=46, ein=2.4): return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)
def titel(t, y=280, g=86): return dict(typ='titel', text=t, x=LX, y=y, groesse=g)
def sz(name, spr, *el): return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))
def pt(x, y, farbe, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text: d['beschriftung'] = text
    if bei: d['beschriftung_bei'] = bei
    return d
def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.35):
    d = {"szene": szene, "bei": bei, "typ": "wahl", "text": text, "optionen": opt, "richtig": richtig,
         "rueck": {str(k): v for k, v in rueck.items()}}
    if sprich: d["sprich"] = sprich
    if rueck_sprich: d["rueck_sprich"] = {str(k): v for k, v in rueck_sprich.items()}
    return d
def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.6, bei=0.35):
    d = {"szene": szene, "bei": bei, "typ": "klick", "text": text, "ziel": ziel, "toleranz": tol,
         "richtig_text": richtig_text, "fallen": fallen, "falsch_text": falsch_text}
    if sprich: d["sprich"] = sprich
    if falsch_sprich: d["falsch_sprich"] = falsch_sprich
    return d
TITEL_SPR = 'Fünf Kontrollfragen. Der Clip hält jedes Mal an: Antworte zuerst — dann zeigt er die Lösung.'
def clip(name, titel_, kurz, schlag, szenen, fragen):
    d = {"titel": titel_, "dateiname": "g3-3-lp-" + name, "kurzbeschrieb": kurz, "schlagworte": schlag,
         "themenbereich": "Funktionen · quadratisch", "fach": "Grundlagenfach", "lerngebiet": "3 · Funktionen",
         "lektion": ["g3-3"], "stufe": ["BM1", "BM2"], "datum": "2026-10-02", "theme": "begreifbar-schlicht",
         "latex": True, "reihe": "Parabel sehen", "nachlauf": 2.6, "probe": True,
         "_probe": "Kontrollclip des Leitprogramms quadratische-funktionen; gehoert dorthin, nicht in die Clip-Bibliothek.",
         "szenen": szenen, "fragen": fragen}
    json.dump(d, open('/home/paps/tals-mathe/clips/' + d["dateiname"] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d["dateiname"], len(szenen), len(fragen))
def anfang(W, par):
    return sz('Titel', TITEL_SPR, titel('Kontrollfragen'), n('Der Clip hält an.|Erst antworten, dann weiterschauen.', 430, ein=0.6), graf(par, W))

# ================================================================ Kapitel 1
W = dict(xbereich=[-5, 4], ybereich=[-4, 6])
clip('kontrolle-scheitelform', 'Parabel sehen: Kontrollfragen zur Scheitelform',
 'Fünf Vorhersagen zu a, xₛ und yₛ: Der Clip hält an, fragt und zeigt dann die Lösung in Bewegung.',
 ['Scheitelform', 'Scheitelpunkt', 'verschieben', 'strecken', 'Kontrollfragen'], [
 anfang(W, [bew([[0, 1, 0, 0]])]),
 sz('Frage 1', 'Plus drei hinter dem Quadrat: drei nach oben. Der Scheitel liegt bei null und drei.',
    f('y = x^2 \\fc{+ 3}', 300, 70), n('@\\fc{y_s}@ hinter der Klammer:|senkrecht, eigenes Vorzeichen', 440, 'gruen', ein=2.2),
    graf([N, bew([[0.8, 1, 0, 0], [3.2, 1, 0, 3]], scheitel={'farbe': 3})], W)),
 sz('Frage 2', 'Die Klammer wird bei minus drei null. Also drei nach links. Der Scheitel liegt bei minus drei und null.',
    f('y = (x \\fb{+ 3})^2', 300, 70), n('Klammer null bei @x = \\fb{-3}@:|drei nach links', 440, ein=2.2),
    graf([N, bew([[0.8, 1, 0, 0], [3.4, 1, -3, 0]], scheitel={'farbe': 3})], W)),
 sz('Frage 3', 'Das Minus klappt die Parabel nach unten. Und null Komma fünf macht sie breiter. Der Scheitel bleibt im Ursprung.',
    f('y = \\fa{-0.5}\\,x^2', 300, 70), n('@\\fa{a} \\lt 0@: nach unten · @|\\fa{a}| \\lt 1@: breiter', 440),
    graf([N, bew([[0.8, 1, 0, 0], [3.6, -0.5, 0, 0]], scheitel={'farbe': 3})], W)),
 sz('Frage 4', 'Die Klammer wird bei minus eins null, hinter der Klammer steht minus drei. Der Scheitel liegt bei minus eins und minus drei. Die Zwei macht die Parabel schmaler.',
    f('y = \\fa{2}(x \\fb{+ 1})^2 \\fc{- 3}', 300, 64), n('@S(\\fb{-1} \\mid \\fc{-3})@, schmaler', 440, ein=3.0),
    graf([N, bew([[0.8, 1, 0, 0], [3.6, 1, -1, -3], [5.4, 2, -1, -3]], scheitel={'farbe': 3})], W)),
 sz('Frage 5', 'Scheitel bei eins und zwei, nach unten geöffnet, so breit wie die Normalparabel. Also minus, Klammer x minus eins zum Quadrat, plus zwei.',
    f('y = \\fa{-}(x \\fb{- 1})^2 \\fc{+ 2}', 300, 66), n('vom Bild zum Term:|Scheitel, Öffnung, Breite', 440, ein=3.0),
    graf([bew([[0, -1, 1, 2]], scheitel={'farbe': 3})], W, ein=0.0)),
 sz('Merke', 'Zum Mitnehmen: x s steht in der Klammer mit umgekehrtem Vorzeichen, y s dahinter mit seinem eigenen. Und a formt: Vorzeichen für die Öffnung, Betrag für die Breite.',
    titel('Zum Mitnehmen', 260, 76), f('f(x) = \\fa{a}(x - \\fb{x_s})^2 + \\fc{y_s}', 420, 62, ein=0.4),
    n('@\\fb{x_s}@: in der Klammer, umgekehrtes Vorzeichen|@\\fc{y_s}@: dahinter, eigenes Vorzeichen|@\\fa{a}@: Vorzeichen = Öffnung, Betrag = Breite', 560, g=42, ein=1.2),
    graf([N, bew([[0, -1, 1, 2], [2.0, 1, 0, 0]], scheitel={'farbe': 3})], W)),
], [
 wahl('Frage 1', 'y = x² + 3: Wohin wandert die Normalparabel?', ['3 nach oben', '3 nach unten', '3 nach rechts'], 0,
      {0: 'Ja.', 1: 'Plus heisst hier hinauf: yₛ behält sein Vorzeichen. Schau hin.', 2: 'Waagrecht schiebt nur eine Zahl in der Klammer. Die 3 steht dahinter.'},
      sprich='y gleich x Quadrat plus drei: Wohin wandert die Normalparabel?',
      rueck_sprich={1: 'Plus heisst hier hinauf: y s behält sein Vorzeichen. Schau hin.'}),
 wahl('Frage 2', 'y = (x + 3)²: Wohin wandert sie?', ['3 nach rechts', '3 nach links', '3 nach oben'], 1,
      {0: 'Das Plus verführt. Wo wird die Klammer null? Schau, wo die Parabel landet.', 1: 'Ja.', 2: 'Die 3 steht in der Klammer, also schiebt sie waagrecht. Nur wohin?'},
      sprich='y gleich x plus drei in Klammern, zum Quadrat: Wohin wandert sie?'),
 wahl('Frage 3', 'y = −0.5x²: Wie sieht die Parabel aus?', ['nach unten, breiter', 'nach unten, schmaler', 'nach oben, breiter'], 0,
      {0: 'Ja.', 1: 'Die Öffnung stimmt. Aber 0.5 ist kleiner als 1: Jeder Wert halbiert sich.', 2: 'Die Breite stimmt. Aber das Minus vor 0.5 klappt die Parabel um.'},
      sprich='y gleich minus null Komma fünf x Quadrat: Wie sieht die Parabel aus?',
      rueck_sprich={1: 'Die Öffnung stimmt. Aber null Komma fünf ist kleiner als eins: Jeder Wert halbiert sich.',
                    2: 'Die Breite stimmt. Aber das Minus vor null Komma fünf klappt die Parabel um.'}),
 klick('Frage 4', 'y = 2(x + 1)² − 3: Wo liegt der Scheitel? Tipp die Stelle ins Bild.', [-1, -3], 'Getroffen: S(−1 | −3).',
       [{"bei": [1, -3], "text": "Die Höhe stimmt. Aber (x + 1) wird bei x = −1 null — der Scheitel liegt links.",
         "sprich": "Die Höhe stimmt. Aber x plus eins wird bei x gleich minus eins null. Der Scheitel liegt links."},
        {"bei": [-1, 3], "text": "Die Stelle stimmt. Aber −3 hinter der Klammer heisst hinunter.",
         "sprich": "Die Stelle stimmt. Aber minus drei hinter der Klammer heisst hinunter."},
        {"bei": [1, 3], "text": "Beide Vorzeichen gedreht. Nur xₛ in der Klammer dreht sich, yₛ nicht.",
         "sprich": "Beide Vorzeichen sind gedreht. Nur x s in der Klammer dreht sich, y s nicht."}],
       'Nicht ganz. Der grüne Kreis zeigt S(−1 | −3): Klammer null bei −1, dahinter −3.',
       sprich='y gleich zwei mal x plus eins in Klammern, zum Quadrat, minus drei: Wo liegt der Scheitel? Tipp die Stelle ins Bild.',
       falsch_sprich='Nicht ganz. Der grüne Kreis zeigt den Scheitel bei minus eins und minus drei.'),
 wahl('Frage 5', 'Welche Gleichung gehört zur Parabel im Bild?', ['y = −(x − 1)² + 2', 'y = −(x + 1)² + 2', 'y = (x − 1)² + 2'], 0,
      {0: 'Ja.', 1: 'Der Scheitel liegt bei x = 1. Dazu gehört die Klammer (x − 1), nicht (x + 1).',
       2: 'Die Parabel ist nach unten geöffnet — dafür braucht es ein Minus vor der Klammer.'},
      rueck_sprich={1: 'Der Scheitel liegt bei x gleich eins. Dazu gehört die Klammer x minus eins, nicht x plus eins.',
                    2: 'Die Parabel ist nach unten geöffnet. Dafür braucht es ein Minus vor der Klammer.'}, bei=0.38),
])

# ================================================================ Kapitel 2
W = dict(xbereich=[-5, 6], ybereich=[-6, 8])
P0 = bew([[0, 1, 0, 0]])
clip('kontrolle-formen', 'Parabel sehen: Kontrollfragen zu den drei Formen',
 'Fünf Vorhersagen zu Grund-, Scheitel- und Produktform — was jede im Bild zeigt und wie man umformt.',
 ['Grundform', 'Scheitelform', 'Produktform', 'umformen', 'Kontrollfragen'], [
 anfang(W, [P0]),
 sz('Frage 1', 'Ein Produkt ist null, wenn eine Klammer null ist: bei eins und bei minus drei. Das sind die Nullstellen.',
    f('f(x) = 0.5(x \\fb{- 1})(x \\fb{+ 3})', 300, 60), n('Produktform: Nullstellen @\\fb{1}@ und @\\fb{-3}@', 440, ein=2.6),
    graf([bew([[0.8, 1, 0, 0], [3.4, 0.5, -1, -2]], nullstellen={'farbe': 2})], W)),
 sz('Frage 2', 'Bei x gleich null bleibt nur c übrig: minus drei. Die Grundform zeigt den y-Achsenabschnitt direkt.',
    f('f(x) = x^2 - 2x \\fa{- 3}', 300, 64), n('@f(0) = c = \\fa{-3}@', 440, ein=2.2),
    graf([bew([[0, 1, 1, -4]], yachse={'farbe': 1})], W, ein=0.0)),
 sz('Frage 3', 'x minus eins zum Quadrat ist x Quadrat minus zwei x plus eins. Minus vier dazu: x Quadrat minus zwei x minus drei — dieselbe Parabel wie eben.',
    f('(x - 1)^2 - 4 = x^2 - 2x + 1 - 4', 300, 54), f('= x^2 - 2x - 3', 410, 54, ein=3.0), n('ausquadrieren, dann zusammenfassen', 540, ein=4.0),
    graf([bew([[0, 1, 1, -4]], scheitel={'farbe': 3}, yachse={'farbe': 1})], W, ein=0.0)),
 sz('Frage 4', 'Der Scheitel liegt bei minus zwei und eins, über der Achse, und die Parabel ist nach oben geöffnet. Sie trifft die x-Achse nie — ohne Nullstellen keine Produktform.',
    f('f(x) = (x + 2)^2 + 1', 300, 64), n('keine Nullstellen —|keine Produktform', 440, 'rot', ein=3.0),
    graf([bew([[0.8, 1, 0, 0], [3.6, 1, -2, 1]], scheitel={'farbe': 3}, nullstellen={'farbe': 2})], W)),
 sz('Frage 5', 'Der Scheitel liegt genau zwischen den Nullstellen eins und fünf: bei drei. f von drei ist minus vier.',
    f('x^2 - 6x + 5 = (x - 1)(x - 5)', 300, 54), f('S(3 \\mid -4)', 410, 58, ein=3.0),
    graf([bew([[0, 1, 3, -4]], nullstellen={'farbe': 2}), ], W, ein=0.0)),
 sz('Merke', 'Zum Mitnehmen: Die Grundform zeigt den y-Achsenabschnitt, die Scheitelform den Scheitel, die Produktform die Nullstellen — wenn es welche gibt.',
    titel('Zum Mitnehmen', 260, 76),
    f('\\text{Grundform} \\ \\longrightarrow \\ \\fa{(0 \\mid c)}', 400, 50, ein=0.6),
    f('\\text{Scheitelform} \\ \\longrightarrow \\ \\fc{S(x_s \\mid y_s)}', 500, 50, ein=1.4),
    f('\\text{Produktform} \\ \\longrightarrow \\ \\fb{x_1,\\ x_2}', 600, 50, ein=2.2),
    graf([bew([[0, 1, 1, -4]], scheitel={'farbe': 3}, nullstellen={'farbe': 2}, yachse={'farbe': 1})], W)),
], [
 wahl('Frage 1', 'f(x) = 0.5(x − 1)(x + 3): Wo schneidet die Parabel die x-Achse?', ['bei 1 und −3', 'bei −1 und 3', 'bei 0.5 und 1'], 0,
      {0: 'Ja.', 1: 'Vorzeichen: (x − 1) wird bei x = 1 null, (x + 3) bei x = −3.', 2: 'Der Faktor 0.5 streckt nur. Die Nullstellen stehen in den Klammern.'},
      sprich='f von x gleich null Komma fünf mal x minus eins mal x plus drei: Wo schneidet die Parabel die x-Achse?',
      rueck_sprich={1: 'Vorzeichen: x minus eins wird bei x gleich eins null, x plus drei bei x gleich minus drei.',
                    2: 'Der Faktor null Komma fünf streckt nur. Die Nullstellen stehen in den Klammern.'}),
 klick('Frage 2', 'f(x) = x² − 2x − 3: Tipp den Schnittpunkt mit der y-Achse.', [0, -3], 'Getroffen: (0 | −3).',
       [{"bei": [0, 3], "text": "Das Vorzeichen gehört dazu: c = −3, also (0 | −3).", "sprich": "Das Vorzeichen gehört dazu: c ist minus drei."},
        {"bei": [-1, 0], "text": "Das ist eine Nullstelle. Der y-Achsenabschnitt liegt bei x = 0.", "sprich": "Das ist eine Nullstelle. Der y-Achsenabschnitt liegt bei x gleich null."},
        {"bei": [3, 0], "text": "Das ist eine Nullstelle. Der y-Achsenabschnitt liegt bei x = 0.", "sprich": "Das ist eine Nullstelle. Der y-Achsenabschnitt liegt bei x gleich null."}],
       'Nicht ganz. Setz x = 0 ein: Es bleibt c = −3.',
       sprich='f von x gleich x Quadrat minus zwei x minus drei: Tipp den Schnittpunkt mit der y-Achse.',
       falsch_sprich='Nicht ganz. Setz x gleich null ein: Es bleibt c gleich minus drei.'),
 wahl('Frage 3', '(x − 1)² − 4 in der Grundform?', ['x² − 2x − 3', 'x² − 5', 'x² + 2x − 3'], 0,
      {0: 'Ja.', 1: 'Die Klammer muss ausquadriert werden: (x − 1)² = x² − 2x + 1.', 2: 'Vorzeichen: (x − 1)² gibt −2x.'},
      sprich='x minus eins in Klammern, zum Quadrat, minus vier: Wie lautet die Grundform?',
      rueck_sprich={1: 'Die Klammer muss ausquadriert werden: x minus eins zum Quadrat ist x Quadrat minus zwei x plus eins.',
                    2: 'Vorzeichen: x minus eins zum Quadrat gibt minus zwei x.'}),
 wahl('Frage 4', 'f(x) = (x + 2)² + 1: Wie lautet die Produktform?', ['(x + 2)(x + 2) + 1', '(x + 3)(x + 1)', 'gibt es nicht'], 2,
      {0: 'Das ist keine Produktform — da steht noch + 1.', 1: 'Ausmultipliziert gibt das x² + 4x + 3, nicht x² + 4x + 5.', 2: 'Ja.'},
      sprich='f von x gleich x plus zwei in Klammern, zum Quadrat, plus eins: Wie lautet die Produktform?',
      rueck_sprich={0: 'Das ist keine Produktform. Da steht noch plus eins.', 1: 'Ausmultipliziert gibt das x Quadrat plus vier x plus drei, nicht plus fünf.'}),
 klick('Frage 5', 'x² − 6x + 5 = (x − 1)(x − 5): Tipp den Scheitel.', [3, -4], 'Getroffen: S(3 | −4).',
       [{"bei": [-3, -4], "text": "Der Scheitel liegt zwischen den Nullstellen 1 und 5 — rechts der y-Achse.", "sprich": "Der Scheitel liegt zwischen den Nullstellen eins und fünf, rechts der y-Achse."},
        {"bei": [3, 5], "text": "Die Stelle stimmt. Die Höhe ist f(3) = 9 − 18 + 5 = −4, nicht c.", "sprich": "Die Stelle stimmt. Die Höhe ist f von drei, also minus vier, nicht c."}],
       'Nicht ganz. Mitte der Nullstellen: x = 3, Höhe f(3) = −4.',
       sprich='x Quadrat minus sechs x plus fünf ist x minus eins mal x minus fünf: Tipp den Scheitel.',
       falsch_sprich='Nicht ganz. Die Mitte der Nullstellen ist drei, die Höhe f von drei ist minus vier.'),
])

# ================================================================ Kapitel 3
W = dict(xbereich=[-5, 6], ybereich=[-10, 8])
clip('kontrolle-nullstellen', 'Parabel sehen: Kontrollfragen zu Nullstellen und Scheitel',
 'Fünf Vorhersagen zu Diskriminante, Symmetrieachse und Scheitel: Der Clip hält an, fragt und zeigt die Lösung.',
 ['Diskriminante', 'Nullstellen', 'Scheitelpunkt', 'Symmetrieachse', 'Kontrollfragen'], [
 anfang(W, [bew([[0, 1, 0, 0]])]),
 sz('Frage 1', 'D ist sechsunddreissig minus vier mal neun, also null. Die Parabel berührt die Achse — eine doppelte Nullstelle bei drei.',
    f('x^2 - 6x + \\fa{9}', 300, 64), f('D = 36 - 36 = 0', 410, 58, ein=2.0),
    graf([bew([[0.8, 1, 3, -4], [3.4, 1, 3, 0]], nullstellen={'farbe': 2})], W)),
 sz('Frage 2', 'x s ist minus b durch zwei a, also minus zwei. f von minus zwei ist vier minus acht plus eins: minus drei.',
    f('x_s = -\\dfrac{4}{2} = -2', 300, 58), f('y_s = f(-2) = -3', 430, 58, ein=3.0),
    graf([bew([[0, 1, -2, -3]], nullstellen={'farbe': 2})], W, ein=0.0)),
 sz('Frage 3', 'Nach unten geöffnet, der Scheitel unter der Achse: Die Parabel trifft die x-Achse nie. D ist negativ.',
    f('D \\lt 0', 300, 70, ein=2.4), n('keine Nullstelle', 430, 'rot', ein=3.0),
    graf([bew([[0, -1, 1, -2]], scheitel={'farbe': 3})], W, ein=0.0)),
 sz('Frage 4', 'Zwei Zahlen mit Produkt minus acht und Summe minus zwei: minus vier und zwei. Also x minus vier mal x plus zwei — Nullstellen minus zwei und vier. Ihre Mitte ist eins.',
    f('x^2 - 2x - 8 = (x - 4)(x + 2)', 300, 54), n('Nullstellen @-2@ und @4@, Mitte @1@', 440, ein=3.4),
    graf([bew([[0, 1, 1, -9]], nullstellen={'farbe': 2}, scheitel={'farbe': 3})], W, ein=0.0)),
 sz('Frage 5', 'c hebt die ganze Parabel senkrecht. Die Achse bei minus b durch zwei a hängt gar nicht von c ab.',
    f('x^2 - 2x + \\fa{c}', 300, 64), n('@c@ hebt — die Achse bleibt', 440, ein=2.6),
    graf([bew([[0.8, 1, 1, -9], [4.0, 1, 1, 2]], nullstellen={'farbe': 2})], W,
         kurven=[dict(formel='10000*(x-1)', von=0.999, bis=1.001, n=600, farbe=1, gestrichelt=True, dicke=3)])),
 sz('Merke', 'Zum Mitnehmen: x s ist minus b durch zwei a, y s ist f von x s. Die Nullstellen liegen spiegelbildlich zur Achse, und D sagt, wie viele es gibt.',
    titel('Zum Mitnehmen', 260, 76), f('x_s = -\\dfrac{b}{2a} \\qquad y_s = f(x_s)', 420, 54, ein=0.6),
    f('D = b^2 - 4ac', 540, 54, ein=1.6), n('@D \\gt 0@: zwei · @D = 0@: eine · @D \\lt 0@: keine', 660, g=44, ein=2.4),
    graf([bew([[0, 1, 1, -4]], nullstellen={'farbe': 2}, scheitel={'farbe': 3})], W)),
], [
 wahl('Frage 1', 'x² − 6x + 9: Wie viele Nullstellen hat die Parabel?', ['zwei', 'eine', 'keine'], 1,
      {0: 'Rechne D = b² − 4ac = 36 − 36. Schau, was passiert.', 1: 'Ja.', 2: 'Rechne D = b² − 4ac = 36 − 36. Schau, was passiert.'},
      sprich='x Quadrat minus sechs x plus neun: Wie viele Nullstellen hat die Parabel?',
      rueck_sprich={0: 'Rechne D gleich b Quadrat minus vier a c. Schau, was passiert.', 2: 'Rechne D gleich b Quadrat minus vier a c. Schau, was passiert.'}),
 klick('Frage 2', 'f(x) = x² + 4x + 1: Tipp den Scheitel.', [-2, -3], 'Getroffen: S(−2 | −3).',
       [{"bei": [2, -3], "text": "xₛ = −b/(2a) = −4/2 = −2: das Minus vor dem Bruch.", "sprich": "x s ist minus b durch zwei a, also minus zwei. Das Minus vor dem Bruch."},
        {"bei": [-2, 1], "text": "Die Stelle stimmt. Die Höhe ist f(−2) = −3, nicht c.", "sprich": "Die Stelle stimmt. Die Höhe ist f von minus zwei, nicht c."}],
       'Nicht ganz. xₛ = −b/(2a) = −2, yₛ = f(−2) = −3.',
       sprich='f von x gleich x Quadrat plus vier x plus eins: Tipp den Scheitel.',
       falsch_sprich='Nicht ganz. x s ist minus zwei, y s ist f von minus zwei, also minus drei.'),
 wahl('Frage 3', 'Ist D bei dieser Parabel positiv, null oder negativ?', ['positiv', 'null', 'negativ'], 2,
      {0: 'D > 0 hiesse zwei Schnittpunkte mit der x-Achse. Siehst du welche?', 1: 'D = 0 hiesse: Der Scheitel liegt auf der Achse. Liegt er dort?', 2: 'Ja.'},
      sprich='Ist D bei dieser Parabel positiv, null oder negativ?',
      rueck_sprich={0: 'D grösser null hiesse zwei Schnittpunkte mit der x-Achse. Siehst du welche?', 1: 'D gleich null hiesse: Der Scheitel liegt auf der Achse. Liegt er dort?'}, bei=0.38),
 wahl('Frage 4', 'x² − 2x − 8: Wo liegen die Nullstellen?', ['bei −2 und 4', 'bei 2 und −4', 'bei −8 und 1'], 0,
      {0: 'Ja.', 1: 'Vorzeichen: Die Summe muss +2 ergeben (−b), also 4 und −2.', 2: 'Das sind c und a, keine Nullstellen.'},
      sprich='x Quadrat minus zwei x minus acht: Wo liegen die Nullstellen?',
      rueck_sprich={1: 'Vorzeichen: Die Summe der Nullstellen muss plus zwei ergeben.', 2: 'Das sind c und a, keine Nullstellen.'}),
 wahl('Frage 5', 'Nur c wird grösser. Was macht die Symmetrieachse?', ['sie bleibt stehen', 'sie wandert nach rechts', 'sie wandert nach oben'], 0,
      {0: 'Ja.', 1: 'Die Achse liegt bei xₛ = −b/(2a). Kommt c darin vor?', 2: 'Eine senkrechte Achse kann nicht nach oben wandern — die Parabel schon.'},
      rueck_sprich={1: 'Die Achse liegt bei x s gleich minus b durch zwei a. Kommt c darin vor?', 2: 'Eine senkrechte Achse kann nicht nach oben wandern. Die Parabel schon.'}),
])

# ================================================================ Kapitel 4
W = dict(xbereich=[-3, 6], ybereich=[-6, 7])
clip('kontrolle-aufstellen', 'Parabel sehen: Kontrollfragen zum Aufstellen',
 'Fünf Vorhersagen: welcher Ansatz, welches a — der Clip hält an, fragt und zeigt die Parabel, die passt.',
 ['Funktionsgleichung aufstellen', 'Scheitelform', 'Produktform', 'Grundform', 'Kontrollfragen'], [
 anfang(W, [bew([[0, 1, 0, 0]])]),
 sz('Frage 1', 'Ansatz a mal x minus eins zum Quadrat plus drei. P einsetzen: eins gleich a plus drei, also a gleich minus zwei.',
    f('f(x) = \\fa{a}(x - 1)^2 + 3', 300, 60), f('1 = \\fa{a} + 3 \\ \\Rightarrow\\ \\fa{a} = -2', 420, 56, ein=2.6),
    graf([bew([[0.8, -0.25, 1, 3], [3.6, -2, 1, 3]])], W, punkte=[pt(1, 3, 3, 'S(1 | 3)', [1.3, 3.45]), pt(2, 1, 2, 'P(2 | 1)', [2.3, 1.45])])),
 sz('Frage 2', 'Ansatz a mal x mal x minus vier. P einsetzen: minus vier gleich a mal zwei mal minus zwei. Also a gleich eins.',
    f('f(x) = \\fa{a}\\,x(x - 4)', 300, 60), f('-4 = \\fa{a} \\cdot 2 \\cdot (-2) \\ \\Rightarrow\\ \\fa{a} = 1', 420, 52, ein=2.6),
    graf([bew([[0.8, 0.3, 2, -1.2], [3.6, 1, 2, -4]])], W, punkte=[pt(0, 0, 2), pt(4, 0, 2), pt(2, -4, 2, 'P(2 | −4)', [2.3, -4.6])])),
 sz('Frage 3', 'Der Scheitel steht direkt im Ansatz: x s gleich minus eins gibt x plus eins in der Klammer, y s gleich zwei steht dahinter.',
    f('\\fa{a}(x \\fb{+ 1})^2 \\fc{+ 2}', 300, 64), n('@S(\\fb{-1} \\mid \\fc{2})@ steht im Ansatz', 440, ein=2.6),
    graf([bew([[0.8, 1, 0, 0], [3.4, -1, -1, 2]], scheitel={'farbe': 3})], W)),
 sz('Frage 4', 'Drei beliebige Punkte: die Grundform ansetzen und jeden Punkt einsetzen — drei Gleichungen für a, b und c.',
    f('y = ax^2 + bx + c', 300, 60), n('drei Punkte → drei Gleichungen', 440, ein=2.4),
    graf([bew([[0.8, 1, 0, 0], [3.6, 2, 0.75, -0.125]])], W,
         punkte=[pt(-1, 6, 2, '(−1 | 6)', [-0.75, 6.2]), pt(0, 1, 2, '(0 | 1)', [0.25, 1.4]), pt(2, 3, 2, '(2 | 3)', [2.25, 3.4])])),
 sz('Frage 5', 'Ein Schritt nach rechts vom Scheitel: a mal eins Quadrat, also eins hinauf. Der Punkt liegt bei drei und null.',
    f('f(3) = 1 \\cdot (3 - 2)^2 - 1 = 0', 300, 56, ein=2.4),
    graf([bew([[0, 1, 2, -1]], scheitel={'farbe': 3}, marken=[{'x': 3, 'farbe': 2, 'text': 'f(3) = {y}'}])], W, ein=0.0)),
 sz('Merke', 'Zum Mitnehmen: Wähl die Form, in der das Gegebene schon steht. Scheitel und Punkt: Scheitelform. Nullstellen und Punkt: Produktform. Drei Punkte: Grundform.',
    titel('Zum Mitnehmen', 260, 76),
    n('Scheitel + Punkt:', 390, 'tinte', 44, ein=0.6), f('\\fa{a}(x - x_s)^2 + y_s', 450, 50, ein=0.8),
    n('Nullstellen + Punkt:', 560, 'tinte', 44, ein=1.6), f('\\fa{a}(x - x_1)(x - x_2)', 620, 50, ein=1.8),
    n('drei Punkte: @ax^2 + bx + c@', 730, 'tinte', 44, ein=2.6),
    graf([bew([[0, -2, 1, 3]], scheitel={'farbe': 3})], W)),
], [
 wahl('Frage 1', 'Scheitel S(1 | 3), Punkt P(2 | 1). Wie gross ist a?', ['a = −2', 'a = 2', 'a = −4'], 0,
      {0: 'Ja.', 1: 'P liegt tiefer als der Scheitel — die Parabel ist nach unten geöffnet, a < 0.', 2: 'Setz P ein: 1 = a · (2 − 1)² + 3, also 1 = a + 3.'},
      sprich='Scheitel bei eins und drei, Punkt P bei zwei und eins. Wie gross ist a?',
      rueck_sprich={1: 'P liegt tiefer als der Scheitel. Die Parabel ist nach unten geöffnet, a ist negativ.', 2: 'Setz P ein: eins gleich a plus drei.'}),
 wahl('Frage 2', 'Nullstellen 0 und 4, Punkt P(2 | −4): Wie gross ist a?', ['a = 1', 'a = −1', 'a = 4'], 0,
      {0: 'Ja.', 1: 'P liegt unter der Achse zwischen den Nullstellen — die Parabel ist nach oben geöffnet.', 2: 'Setz P ein: −4 = a · 2 · (2 − 4) = −4a.'},
      sprich='Nullstellen null und vier, Punkt P bei zwei und minus vier: Wie gross ist a?',
      rueck_sprich={1: 'P liegt unter der Achse zwischen den Nullstellen. Die Parabel ist nach oben geöffnet.', 2: 'Setz P ein: minus vier gleich a mal zwei mal minus zwei.'}),
 wahl('Frage 3', 'Scheitel S(−1 | 2) und ein weiterer Punkt: welcher Ansatz?', ['a(x + 1)² + 2', 'a(x − 1)² + 2', 'a(x + 1)² − 2'], 0,
      {0: 'Ja.', 1: 'xₛ = −1: Die Klammer wird bei x = −1 null — also (x + 1).', 2: 'yₛ = 2 steht mit eigenem Vorzeichen dahinter: + 2.'},
      sprich='Scheitel bei minus eins und zwei und ein weiterer Punkt: Welcher Ansatz passt?',
      rueck_sprich={1: 'x s ist minus eins. Die Klammer wird bei x gleich minus eins null, also x plus eins.', 2: 'y s ist zwei und steht mit eigenem Vorzeichen dahinter.'}),
 wahl('Frage 4', 'Drei Punkte, keiner davon Scheitel oder Nullstelle. Welche Form setzt du an?', ['Grundform', 'Scheitelform', 'Produktform'], 0,
      {0: 'Ja.', 1: 'Dafür müsstest du den Scheitel kennen.', 2: 'Dafür müsstest du die Nullstellen kennen.'}),
 klick('Frage 5', 'Scheitel S(2 | −1), a = 1. Tipp, wo die Parabel bei x = 3 ist.', [3, 0], 'Getroffen: (3 | 0).',
       [{"bei": [3, -2], "text": "a = 1 > 0: Vom Scheitel aus geht es hinauf, nicht hinunter.", "sprich": "a ist positiv: Vom Scheitel aus geht es hinauf, nicht hinunter."},
        {"bei": [3, 3], "text": "Ein Schritt rechts: a · 1² = 1 hinauf, nicht 4.", "sprich": "Ein Schritt nach rechts: a mal eins Quadrat, also eins hinauf."}],
       'Nicht ganz: f(3) = (3 − 2)² − 1 = 0.',
       sprich='Scheitel bei zwei und minus eins, a gleich eins. Tipp, wo die Parabel bei x gleich drei ist.',
       falsch_sprich='Nicht ganz. f von drei ist eins minus eins, also null.'),
])

# ================================================================ Kapitel 5
W = dict(xbereich=[-1, 11], ybereich=[-3, 28], yteilung=[[5, '5'], [10, '10'], [15, '15'], [20, '20'], [25, '25']],
         xteilung=[[2, '2'], [5, '5'], [8, '8'], [10, '10']])
W2 = dict(xbereich=[-1, 11], ybereich=[-5, 55], yteilung=[[10, '10'], [20, '20'], [30, '30'], [40, '40'], [50, '50']],
          xteilung=[[5, '5'], [10, '10']])
Z = [[0, -1, 5, 25]]
clip('kontrolle-extremwert', 'Parabel sehen: Kontrollfragen zu Extremwerten',
 'Fünf Vorhersagen zum Maximum: Mitte der Nullstellen, Spiegelpunkte, Antwort mit Stelle und Wert.',
 ['Extremwertaufgabe', 'Maximum', 'Scheitelpunkt', 'Symmetrie', 'Kontrollfragen'], [
 anfang(W, [bew(Z)]),
 sz('Frage 1', 'Die Nullstellen sind null und zehn. Der Scheitel liegt in ihrer Mitte: bei fünf.',
    f('A(x) = x\\,(10 - x)', 300, 60), n('Nullstellen @0@ und @10@ → Mitte @5@', 440, ein=2.0),
    graf([bew(Z, laeufer={'bahn': [[0.8, 1], [3.4, 5]], 'farbe': 2, 'text': 'A = {y}'})], W)),
 sz('Frage 2', 'A von fünf ist fünf mal fünf, also fünfundzwanzig. Das ist die grösste Fläche.',
    f('A(5) = 5 \\cdot 5 = 25', 300, 60, ein=1.4),
    graf([bew(Z, laeufer={'bahn': [[0, 5]], 'farbe': 3, 'text': 'A = {y}'})], W, ein=0.0)),
 sz('Frage 3', 'Gleich hohe Punkte liegen spiegelbildlich zur Achse. Die Mitte von zwei und acht ist fünf — dort liegt das Maximum.',
    f('A(2) = A(8) = 16', 300, 58, ein=0.6), f('\\dfrac{2 + 8}{2} = 5', 420, 58, ein=2.4),
    graf([bew(Z, laeufer={'bahn': [[0, 2], [0.8, 2], [3.6, 5]], 'farbe': 2, 'text': 'A = {y}', 'spiegel': True})], W, ein=0.0)),
 sz('Frage 4', 'Die Nullstellen sind null und zehn, die Mitte ist fünf. A von fünf ist fünf mal zehn, also fünfzig Quadratmeter.',
    f('A(x) = x\\,(20 - 2x)', 300, 58), f('A(5) = 5 \\cdot 10 = 50', 420, 56, ein=3.0),
    graf([bew([[0, -2, 5, 50]], laeufer={'bahn': [[0.8, 1], [3.4, 5]], 'farbe': 2, 'text': 'A = {y}'})], W2)),
 sz('Frage 5', 'Ausmultipliziert steht vorne minus zwei x Quadrat. a ist negativ, die Parabel nach unten geöffnet — ihr Scheitel ist der höchste Punkt.',
    f('A(x) = \\fa{-2}x^2 + 20x', 300, 58, ein=1.6), n('@\\fa{a} \\lt 0@: nach unten — Maximum', 440, ein=2.8),
    graf([bew([[0, -2, 5, 50]], scheitel={'farbe': 3})], W2, ein=0.0)),
 sz('Merke', 'Zum Mitnehmen: Nullstellen ablesen, ihre Mitte nehmen, den Wert einsetzen. Und die Antwort nennt beides — Stelle und Wert.',
    titel('Zum Mitnehmen', 260, 76),
    n('1. Nullstellen ablesen|2. Mitte nehmen|3. Wert einsetzen|4. Antwort: Stelle und Wert', 420, g=46, ein=0.6),
    graf([bew(Z, scheitel={'farbe': 3})], W)),
], [
 wahl('Frage 1', 'A(x) = x(10 − x): Bei welchem x ist A am grössten?', ['x = 5', 'x = 10', 'x = 2.5'], 0,
      {0: 'Ja.', 1: 'Bei x = 10 ist A(10) = 0 — das ist eine Nullstelle.', 2: 'Die Mitte zwischen den Nullstellen 0 und 10 ist nicht 2.5.'},
      sprich='A von x gleich x mal zehn minus x: Bei welchem x ist A am grössten?',
      rueck_sprich={1: 'Bei x gleich zehn ist A null. Das ist eine Nullstelle.', 2: 'Die Mitte zwischen den Nullstellen null und zehn ist nicht zwei Komma fünf.'}),
 wahl('Frage 2', 'Und wie gross ist A dann?', ['A = 25', 'A = 5', 'A = 50'], 0,
      {0: 'Ja.', 1: '5 ist die Stelle, nicht der Wert. Setz ein: A(5) = 5 · (10 − 5).', 2: 'Setz ein: A(5) = 5 · (10 − 5) = 5 · 5.'},
      rueck_sprich={1: 'Fünf ist die Stelle, nicht der Wert. Setz ein: fünf mal zehn minus fünf.', 2: 'Setz ein: fünf mal zehn minus fünf, also fünf mal fünf.'}),
 klick('Frage 3', 'A(2) = A(8) = 16. Tipp ins Bild, wo das Maximum liegt.', [5, 25], 'Getroffen: (5 | 25).',
       [], 'Nicht ganz: Das Maximum liegt in der Mitte von 2 und 8, bei x = 5.', tol=1.2,
       sprich='A von zwei und A von acht sind beide sechzehn. Tipp ins Bild, wo das Maximum liegt.',
       falsch_sprich='Nicht ganz. Das Maximum liegt in der Mitte von zwei und acht, bei x gleich fünf.'),
 wahl('Frage 4', 'Beet an einer Mauer, 20 m Zaun für drei Seiten: A(x) = x(20 − 2x). Wo liegt das Maximum?', ['x = 5', 'x = 10', 'x = 2.5'], 0,
      {0: 'Ja.', 1: 'Bei x = 10 ist 20 − 2x = 0: Das ist eine Nullstelle.', 2: 'Die Nullstellen sind 0 und 10 — ihre Mitte ist 5.'},
      sprich='Ein Beet an einer Mauer, zwanzig Meter Zaun für drei Seiten: A von x gleich x mal zwanzig minus zwei x. Wo liegt das Maximum?',
      rueck_sprich={1: 'Bei x gleich zehn ist zwanzig minus zwei x gleich null. Das ist eine Nullstelle.', 2: 'Die Nullstellen sind null und zehn, ihre Mitte ist fünf.'}),
 wahl('Frage 5', 'Warum ist der Scheitel hier ein Maximum?', ['weil a negativ ist', 'weil c = 0 ist', 'weil b positiv ist'], 0,
      {0: 'Ja.', 1: 'c bestimmt nur, wo die Parabel die y-Achse schneidet.', 2: 'b allein entscheidet nichts über die Öffnung.'},
      rueck_sprich={1: 'c bestimmt nur, wo die Parabel die y-Achse schneidet.', 2: 'b allein entscheidet nichts über die Öffnung.'}),
])
