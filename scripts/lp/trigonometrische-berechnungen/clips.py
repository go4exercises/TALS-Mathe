"""Erzeugt die zehn Drehbücher des Leitprogramms Trigonometrische Berechnungen (07.10.2026).

  python3 scripts/lp/trigonometrische-berechnungen/clips.py

Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext gleich);
nur für Szenen mit neuem Text muss danach build-clip-ton.py laufen. Nach der Vertonung Bewegungen
und `ein` direkt hier anpassen und das Skript erneut laufen lassen (die Dauern bleiben erhalten).

Aufbau wie im Leitprogramm Planimetrie (scripts/lp/planimetrie/clips.py): Rechnung und Notizen links
(x 150), die Figur rechts (x 1010, y 175, 760 × 760). Figuren zeichnet `graf` mit "figuren" und
"achsen": false (HOWTO-clips.md, «Figuren im Graf»). Das Fenster ist in x und y gleich geteilt.

Fragebild (HOWTO-leitprogramme §15): Die Kontrollclips zeigen beim Erscheinen einer Frage nur das
Gegebene; Rechnung und Hervorhebung erscheinen erst ab 1.0 s (nach der Antwort).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = die Figur                                              \\fa{…}
  2 orange = betrachteter Winkel, gegebene Stücke, Hilfslinie (Höhe) \\fb{…}
  3 grün   = gesuchte Grösse, Ergebnis                              \\fc{…}
  4 rot    = Fehler                                                 \\fd{…}
  5 Tinte  = neutral (Boden, Bezugslinien, Beschriftung)
Alle Zahlen mit python3 nachgerechnet (siehe die Kommentare bei den Szenen).
"""
import json
import math
import os
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'g5-3-lp-'


def rad(w):
    return math.radians(w)


def r3(p):
    return [round(p[0], 3), round(p[1], 3)]


def richtung(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


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
    return dict(art='rechts', bei=r3(p), r1=r1, r2=r2, farbe=farbe, **kw)


def WI(p, a, b, farbe=2, r=44, **kw):
    """Winkel bei p von der Richtung zu a bis zur Richtung zu b (gegen den Uhrzeigersinn)."""
    w0, w1 = richtung(p, a), richtung(p, b)
    if (w1 - w0) % 360 > 180:
        w0, w1 = w1, w0
    if w1 < w0:
        w1 += 360
    return dict(art='winkel', bei=r3(p), von=round(w0, 2), bis=round(w1, 2), farbe=farbe, r_px=r, **kw)


def KR(m, r, farbe=5, **kw):
    return dict(art='kreis', m=r3(m), r=round(r, 3), farbe=farbe, fuellung=0, **kw)


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def graf(W, figuren=(), punkte=(), ein=0.05, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=list(punkte), figuren=list(figuren), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def pt(p, farbe=5, **kw):
    return dict(x=round(p[0], 3), y=round(p[1], 3), farbe=farbe, anker='start', **kw)


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=54, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4):
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
              n('Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.', 430, 'blau', 50, ein=0.6))
FALSCH = 'Nicht ganz. Der grüne Kreis zeigt die Stelle.'


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    alt = R + 'clips/' + PRAEFIX + name + '.json'
    if os.path.exists(alt):
        frueher = {(q['name'], q['sprecher']): q.get('dauer') for q in json.load(open(alt))['szenen']}
        for q in szenen:
            d_ = frueher.get((q['name'], q['sprecher']))
            if d_:
                q['dauer'] = d_
    d = {'titel': titel_, 'dateiname': PRAEFIX + name, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Trigonometrie',
         'fach': 'Grundlagenfach', 'lerngebiet': '5 · Geometrie',
         'lektion': ['g5-3'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Dreiecke berechnen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms trigonometrische-berechnungen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + d['dateiname'] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(d['dateiname'], len(szenen), 'Szenen', len(fragen or []), 'Fragen')


# ---------------------------------------------------------------- das rechtwinklige Dreieck (wie sim1)
def rw(gk, ak, beiB=False):
    """C(0|0) rechter Winkel, A(b|0) unten rechts, B(0|a) oben. x bei A: a = GK, b = AK; bei B umgekehrt."""
    a, b = (ak, gk) if beiB else (gk, ak)
    return (0, 0), (b, 0), (0, a)


def rw_figur(C, A, B, beiB=False, farbe_x=2, ecken=True, fu=0.12):
    fg = [V([A, B, C], 1, fu), RW(C, 0, 90)]
    fg.append(WI(B, C, A, farbe_x) if beiB else WI(A, B, C, farbe_x))
    if ecken:
        fg += [T(A[0] + 0.45, A[1] - 0.65, 'A', kursiv=False), T(B[0] - 0.45, B[1] + 0.25, 'B', kursiv=False),
               T(C[0] - 0.45, C[1] - 0.65, 'C', kursiv=False)]
    return fg


def x_text(C, A, B, beiB=False, farbe=2, abst=1.25):
    p, q, r_ = (B, C, A) if beiB else (A, B, C)
    w = math.radians((richtung(p, q) + richtung(p, r_)) / 2 + (180 if abs(richtung(p, q) - richtung(p, r_)) > 180 else 0))
    return T(p[0] + abst * math.cos(w), p[1] + abst * math.sin(w) - 0.2, 'x', farbe, g=30)


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
# x = 35°, H = 10 cm (Themenseite, Animation «Definition»): GK = 10 sin 35° = 5.736, AK = 10 cos 35° = 8.192.
W1 = geo(-1.6, -1.6, 12.5)
X1, H1 = 35, 10
GK1, AK1 = H1 * math.sin(rad(X1)), H1 * math.cos(rad(X1))
C1, A1, B1 = rw(GK1, AK1)
# kleines Dreieck H = 6 (Szene «Gleiches Verhältnis»): GK 3.441, AK 4.915
Ck, Ak, Bk = rw(6 * math.sin(rad(X1)), 6 * math.cos(rad(X1)))
FIG1 = rw_figur(C1, A1, B1) + [x_text(C1, A1, B1)]
# Teilen statt mal: x = 40°, AK = 8 → H = 8 / cos 40° = 10.443, GK = 8 tan 40° = 6.713
C1b, A1b, B1b = rw(8 * math.tan(rad(40)), 8)

clip('seiten', 1, 'Dreiecke berechnen: Sinus, Cosinus und Tangens',
     'Die Seiten vom Winkel x aus benennen; ähnliche Dreiecke haben dieselben Seitenverhältnisse — Sinus, Cosinus und '
     'Tangens; eine Seite aus Winkel und Seite berechnen, mal oder geteilt; der Winkel wechselt die Ecke.',
     ['Sinus', 'Cosinus', 'Tangens', 'Gegenkathete', 'Ankathete', 'Hypotenuse'], [
         sz('Seiten benennen',
            'Im rechtwinkligen Dreieck benennt man die Seiten vom betrachteten Winkel x aus. Die Hypotenuse liegt dem rechten '
            'Winkel gegenüber. Die Gegenkathete liegt dem Winkel x gegenüber. Die Ankathete liegt am Winkel x an.',
            f(r'\text{vom Winkel } \fb{x} \text{ aus}', 300, 50, ein=0.4),
            f(r'H\!: \text{ gegenüber dem rechten Winkel}', 410, 44, ein=4.9),
            f(r'GK\!: \text{ gegenüber } \fb{x}', 500, 44, ein=7.6),
            f(r'AK\!: \text{ liegt an } \fb{x} \text{ an}', 590, 44, ein=10.2),
            # je Seite zu ihrem Wort (Ton nach der Vertonung nachgeführt); die Beschriftung bleibt, die Hervorhebung wandert
            graf(W1, FIG1 + [mit(S(A1, B1, 2, dicke=8), ein=4.9, aus=7.5), mit(T(5.0, 3.6, 'H', 2), ein=4.9),
                             mit(S(B1, C1, 2, dicke=8), ein=7.6, aus=10.1), mit(T(-0.65, GK1 / 2, 'GK', 2, 'end'), ein=7.6),
                             mit(S(C1, A1, 2, dicke=8), ein=10.2), mit(T(AK1 / 2, -0.75, 'AK', 2), ein=10.2)], ein=0.3)),
         sz('Gleiches Verhältnis',
            'Vergrössert man das Dreieck, ohne den Winkel zu ändern, wachsen alle Seiten um denselben Faktor. Das Verhältnis '
            'Gegenkathete durch Hypotenuse bleibt gleich. Es hängt nur vom Winkel ab.',
            f(r'\dfrac{GK}{H} \approx 0.574', 320, 56, ein=6.0),
            n('gleicher Winkel: ähnliche Dreiecke', 470, 'blau', 42, ein=8.7),
            # H wächst von 6 auf 10 (Ton «Vergrössert … Faktor» 0.4–4.4); Winkel bei A wandert mit.
            graf(W1, [mit(V([Ak, Bk, Ck]), bewegung=[[0.8, {}], [3.6, {'punkte': [r3(A1), r3(B1), r3(C1)]}]]),
                      RW(C1, 0, 90),
                      mit(WI(Ak, Bk, Ck), bewegung=[[0.8, {}], [3.6, {'bei': r3(A1)}]]),
                      mit(T(Ak[0] - 1.25, 0.3, 'x', 2), bewegung=[[0.8, {}], [3.6, {'bei': [round(A1[0] - 1.25, 3), 0.3]}]])],
                 ein=0.3)),
         sz('Definition',
            'Diese festen Verhältnisse heissen Sinus, Cosinus und Tangens. Sinus x ist Gegenkathete durch Hypotenuse. '
            'Cosinus x ist Ankathete durch Hypotenuse. Tangens x ist Gegenkathete durch Ankathete.',
            f(r'\sin x = \dfrac{GK}{H}', 290, 52, ein=4.5),
            f(r'\cos x = \dfrac{AK}{H}', 440, 52, ein=7.2),
            f(r'\tan x = \dfrac{GK}{AK}', 590, 52, ein=9.8),
            graf(W1, FIG1 + [T(5.0, 3.6, 'H', 5), T(-0.65, GK1 / 2, 'GK', 5, 'end'), T(AK1 / 2, -0.75, 'AK', 5)], ein=0.3)),
         sz('Vorgelöst',
            'Zum Beispiel x gleich fünfunddreissig Grad und H gleich zehn Zentimeter. Gesucht ist die Gegenkathete. Beteiligt '
            'sind Gegenkathete und Hypotenuse, also Sinus. Die Gegenkathete ist zehn mal Sinus fünfunddreissig Grad, rund fünf '
            'Komma sieben vier Zentimeter. Ebenso die Ankathete: zehn mal Cosinus fünfunddreissig Grad, rund acht Komma eins neun.',
            f(r'\fb{x = 35^\circ}, \quad \fb{H = 10\,\mathrm{cm}}', 280, 46, ein=0.4),
            f(r'\sin 35^\circ = \dfrac{GK}{10}', 400, 46, ein=9.4),
            f(r'GK = 10 \cdot \sin 35^\circ \approx \fc{5.74\,\mathrm{cm}}', 540, 44, ein=12.9),
            f(r'AK = 10 \cdot \cos 35^\circ \approx \fc{8.19\,\mathrm{cm}}', 640, 44, ein=18.9),
            graf(W1, rw_figur(C1, A1, B1) + [x_text(C1, A1, B1), T(5.0, 3.6, 'H = 10', 2, 'start', 28, False)], ein=0.3),
            graf(W1, [T(-0.5, GK1 / 2, '≈ 5.74', 3, 'end', 28, False)], ein=12.9, raster=False),
            graf(W1, [T(AK1 / 2, -0.8, '≈ 8.19', 3, 'middle', 28, False)], ein=18.9, raster=False)),
         sz('Teilen statt mal',
            'Steht die gesuchte Seite unten im Bruch, wird geteilt. Ist die Ankathete acht Zentimeter und x gleich vierzig Grad, '
            'dann ist die Hypotenuse acht durch Cosinus vierzig Grad, rund zehn Komma vier vier Zentimeter. Die Hypotenuse ist '
            'die längste Seite — das passt.',
            f(r'\cos 40^\circ = \dfrac{8}{H}', 300, 50, ein=7.7),
            f(r'H = \dfrac{8}{\cos 40^\circ} \approx \fc{10.44\,\mathrm{cm}}', 440, 46, ein=9.9),
            n('Probe: @H@ ist die längste Seite.', 580, 'blau', 42, ein=12.1),
            graf(W1, rw_figur(C1b, A1b, B1b) + [x_text(C1b, A1b, B1b), T(4.0, -0.8, 'AK = 8', 2, 'middle', 28, False)], ein=3.6),
            graf(W1, [T(4.6, 4.1, 'H ≈ 10.44', 3, 'start', 28, False)], ein=9.9, raster=False)),
         sz('Winkel bei B',
            'Wandert der betrachtete Winkel zur Ecke B, tauschen Gegenkathete und Ankathete die Rollen. Die Hypotenuse bleibt.',
            n('@x@ bei @B@: @GK@ und @AK@ tauschen', 300, 'blau', 44, ein=0.6),
            # x wechselt die Ecke zum Wort «Ecke B» (Ton nach der Vertonung nachgeführt), danach tauschen die Namen
            graf(W1, rw_figur(C1, A1, B1)[:2] + rw_figur(C1, A1, B1)[3:] + [T(5.0, 3.6, 'H', 5),
                      mit(WI(A1, B1, C1, 2), aus=2.3), mit(x_text(C1, A1, B1), aus=2.3),
                      mit(T(-0.65, GK1 / 2, 'GK', 5, 'end'), aus=2.3), mit(T(AK1 / 2, -0.75, 'AK', 5), aus=2.3),
                      mit(WI(B1, C1, A1, 2), ein=2.3), mit(T(0.75, GK1 - 1.6, 'x', 2), ein=2.3),
                      mit(T(-0.65, GK1 / 2, 'AK', 2, 'end'), ein=3.3), mit(T(AK1 / 2, -0.75, 'GK', 2), ein=3.3)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Erst die Seiten vom Winkel aus benennen, dann die Funktion wählen, die genau diese zwei Seiten '
            'verbindet. Und der Rechner muss auf Grad stehen, D E G.',
            titel('Zum Mitnehmen', 250, 76),
            n('1. Seiten vom Winkel aus benennen|2. Funktion mit den zwei Seiten|3. umstellen: mal oder geteilt', 380, 'blau', 44, ein=1.2),
            n('Rechner auf Grad: @\\mathrm{DEG}@', 640, 'orange', 42, ein=7.0)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
# Frage 1: x bei B im Dreieck GK 5, AK 7? — hier: b = 8, a = 5 (C(0|0), A(8|0), B(0|5)); x bei B.
CK1, AK1_, BK1 = (0, 0), (8, 0), (0, 5)
WK1 = geo(-1.8, -2.4, 11.5)
clip('kontrolle-seiten', 2, 'Dreiecke berechnen: Kontrollfragen zu Sinus, Cosinus und Tangens',
     'Fünf Fragen: die Ankathete finden, den Bruch zum Cosinus, eine Seite mal oder geteilt und warum die Grösse des '
     'Dreiecks keine Rolle spielt.',
     ['Sinus', 'Cosinus', 'Tangens', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der Winkel x liegt bei B. Die Seite B C liegt an ihm an: Sie ist die Ankathete.',
            f(r'AK = \overline{BC}', 300, 56, ein=1.0),
            graf(WK1, [V([AK1_, BK1, CK1]), RW(CK1, 0, 90), WI(BK1, CK1, AK1_, 2), T(0.7, 3.2, 'x', 2),
                       T(8.45, -0.65, 'A', kursiv=False), T(-0.45, 5.25, 'B', kursiv=False), T(-0.45, -0.65, 'C', kursiv=False)], ein=0.05),
            graf(WK1, [S(BK1, CK1, 3, dicke=8), T(-0.6, 2.5, 'AK', 3, 'end')], ein=1.0, raster=False)),
         sz('Frage 2',
            'Cosinus x ist Ankathete durch Hypotenuse.',
            f(r'\cos x = \dfrac{AK}{H}', 300, 58, ein=1.0)),
         sz('Frage 3',
            'Gegenkathete und Hypotenuse: Sinus. Zwölf mal Sinus vierzig Grad ist rund sieben Komma sieben eins Zentimeter.',
            f(r'GK = 12 \cdot \sin 40^\circ \approx \fc{7.71\,\mathrm{cm}}', 300, 48, ein=1.0)),
         sz('Frage 4',
            'Die Hypotenuse steht unten im Bruch: Sinus fünfundzwanzig Grad gleich sechs durch H. Also H gleich sechs durch Sinus '
            'fünfundzwanzig Grad, rund vierzehn Komma zwei null Zentimeter.',
            f(r'H = \dfrac{6}{\sin 25^\circ} \approx \fc{14.20\,\mathrm{cm}}', 300, 50, ein=1.0)),
         sz('Frage 5',
            'Bei gleichem Winkel sind die Dreiecke ähnlich. Beide Seiten wachsen mit demselben Faktor, der Bruch bleibt gleich.',
            n('ähnlich: @\\sin x@ bleibt gleich', 300, 'blau', 50, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Seiten vom Winkel aus benennen. Steht die gesuchte Seite oben im Bruch, multiplizieren, steht sie '
            'unten, teilen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Seiten vom Winkel aus benennen|gesucht oben: mal; unten: geteilt', 400, 'blau', 44, ein=1.2)),
     ], [
         # Ziel (0 | 2.5) auf BC; Toleranz 1.8 deckt BC von y = 0.7 bis 4.3 und bleibt unter dem Abstand zu AB (2.12)
         # und zu CA (2.5). Die Fallen liegen auf CA und AB (gleiche Toleranz; das Ziel wird zuerst geprüft) und so,
         # dass kein Klick auf eine Seite die Meldung einer anderen bekommt (nachgezählt: 200 Stellen je Seite).
         klick('Frage 1', 'x liegt bei B. Tipp die Ankathete von x an.', [0, 2.5], 'Getroffen: BC liegt am Winkel x an.',
               [{'bei': [4, 0], 'text': 'Das ist die Gegenkathete: Sie liegt dem Winkel bei B gegenüber.',
                 'sprich': 'Das ist die Gegenkathete. Sie liegt dem Winkel bei B gegenüber.'},
                {'bei': [4, 2.5], 'text': 'Das ist die Hypotenuse: Sie liegt dem rechten Winkel gegenüber.',
                 'sprich': 'Das ist die Hypotenuse. Sie liegt dem rechten Winkel gegenüber.'},
                {'bei': [2.4, 3.5], 'text': 'Das ist die Hypotenuse: Sie liegt dem rechten Winkel gegenüber.',
                 'sprich': 'Das ist die Hypotenuse. Sie liegt dem rechten Winkel gegenüber.'}],
               FALSCH, sprich='x liegt bei B. Tipp die Ankathete von x an.', falsch_sprich=FALSCH, tol=1.8),
         wahl('Frage 2', 'Welcher Bruch ist cos x?', ['AK : H', 'GK : H', 'GK : AK'], 0,
              {0: 'Ja.', 1: 'Das ist der Sinus. Welche Seite liegt am Winkel an?', 2: 'Das ist der Tangens. Wo kommt die Hypotenuse vor?'},
              sprich='Welcher Bruch ist Cosinus x?',
              rueck_sprich={1: 'Das ist der Sinus. Welche Seite liegt am Winkel an?', 2: 'Das ist der Tangens. Wo kommt die Hypotenuse vor?'}),
         wahl('Frage 3', 'x = 40°, H = 12 cm. Wie lang ist die Gegenkathete?', ['≈ 7.71 cm', '≈ 9.19 cm', '≈ 18.67 cm'], 0,
              {0: 'Ja.', 1: 'Das ist die Ankathete. Welche Funktion verbindet GK und H?',
               2: 'Die Gegenkathete ist kürzer als die Hypotenuse. Mal oder geteilt?'},
              sprich='x gleich vierzig Grad, H gleich zwölf Zentimeter. Wie lang ist die Gegenkathete?',
              rueck_sprich={1: 'Das ist die Ankathete. Welche Funktion verbindet G K und H?',
                            2: 'Die Gegenkathete ist kürzer als die Hypotenuse. Mal oder geteilt?'}),
         wahl('Frage 4', 'x = 25°, GK = 6 cm. Wie lang ist die Hypotenuse?', ['≈ 14.20 cm', '≈ 2.54 cm', '≈ 6.62 cm'], 0,
              {0: 'Ja.', 1: 'Die Hypotenuse ist die längste Seite. Steht H oben oder unten im Bruch?',
               2: 'Das wäre richtig, wenn 6 cm die Ankathete wären. Welche Funktion verbindet GK und H?'},
              sprich='x gleich fünfundzwanzig Grad, G K gleich sechs Zentimeter. Wie lang ist die Hypotenuse?',
              rueck_sprich={1: 'Die Hypotenuse ist die längste Seite. Steht H oben oder unten im Bruch?',
                            2: 'Das wäre richtig, wenn sechs Zentimeter die Ankathete wären. Welche Funktion verbindet G K und H?'}),
         wahl('Frage 5', 'Bei gleichem x werden alle Seiten doppelt so lang. Was macht sin x?',
              ['bleibt gleich', 'verdoppelt sich', 'halbiert sich'], 0,
              {0: 'Ja.', 1: 'Auch die Hypotenuse verdoppelt sich. Was macht dann der Bruch?', 2: 'Beide Seiten wachsen. Was macht der Bruch?'},
              sprich='Bei gleichem x werden alle Seiten doppelt so lang. Was macht Sinus x?',
              rueck_sprich={1: 'Auch die Hypotenuse verdoppelt sich. Was macht dann der Bruch?', 2: 'Beide Seiten wachsen. Was macht der Bruch?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung
# GK = 5, AK = 12 (Themenseite A3a): tan x = 5/12 = 0.417, x = 22.62°, der andere Winkel 67.38°.
W2 = geo(-1.6, -3.6, 14.5)
C2, A2, B2 = rw(5, 12)
# Steigung 8 %: GK 0.96 auf AK 12 → arctan 0.08 = 4.57°
C2s, A2s, B2s = rw(0.96, 12)
clip('winkel', 3, 'Dreiecke berechnen: den Winkel zurückrechnen',
     'Aus zwei Seiten den Winkel: das Verhältnis bilden, dann die Umkehrung arctan, arcsin oder arccos (Rechner: tan⁻¹, '
     'sin⁻¹, cos⁻¹); hoch minus eins heisst Umkehrung, nicht Kehrwert; Steigung in Prozent als Tangens.',
     ['Arcusfunktion', 'Umkehrfunktion', 'Winkel berechnen', 'Steigung'], [
         sz('Umgekehrt',
            'Bisher war der Winkel gegeben. Jetzt kennst du zwei Seiten und suchst den Winkel: Gegenkathete fünf, Ankathete '
            'zwölf Zentimeter.',
            f(r'GK = 5, \quad AK = 12, \quad x = \fc{?}', 300, 48, ein=2.9),
            graf(W2, rw_figur(C2, A2, B2, farbe_x=3) + [T(9.6, 0.35, 'x', 3), T(-0.5, 2.5, '5', 2, 'end', 30, False), T(6, -0.85, '12', 2, 'middle', 30, False)], ein=0.3)),
         sz('Verhältnis',
            'Beteiligt sind die beiden Katheten, also Tangens: Tangens x gleich fünf Zwölftel, rund null Komma vier eins sieben.',
            f(r'\tan x = \dfrac{5}{12} \approx 0.417', 300, 54, ein=3.6),
            graf(W2, rw_figur(C2, A2, B2, farbe_x=3) + [T(9.6, 0.35, 'x', 3), T(-0.5, 2.5, '5', 2, 'end', 30, False), T(6, -0.85, '12', 2, 'middle', 30, False)], ein=0.3)),
         sz('Umkehrung',
            'Den Winkel liefert die Umkehrung, der Arcustangens. Auf dem Rechner ist es die Taste tan hoch minus eins. x gleich '
            'Arcustangens von fünf Zwölfteln, rund zweiundzwanzig Komma sechs zwei Grad.',
            f(r'x = \arctan\dfrac{5}{12}', 300, 54, ein=0.4),
            n('Rechner: @\\tan^{-1}@', 440, 'blau', 44, ein=5.2),
            f(r'x \approx \fc{22.62^\circ}', 560, 54, ein=8.6),
            graf(W2, rw_figur(C2, A2, B2, farbe_x=3) + [T(-0.5, 2.5, '5', 2, 'end', 30, False), T(6, -0.85, '12', 2, 'middle', 30, False)], ein=0.3),
            graf(W2, [T(8.9, 0.35, '22.62°', 3, 'end', 28, False)], ein=8.6, raster=False)),
         sz('Nicht Kehrwert',
            'Achtung: Hoch minus eins heisst hier Umkehrung, nicht Kehrwert. Eins durch Tangens ist etwas anderes.',
            f(r'\tan^{-1} \;\neq\; \dfrac{1}{\tan}', 320, 60, ein=1.1),
            n('@\\tan^{-1}@: Verhältnis rein, Winkel raus', 480, 'blau', 42, ein=4.3)),
         sz('Probe',
            'Probe: Tangens zweiundzwanzig Komma sechs zwei Grad gibt wieder rund null Komma vier eins sieben. Der andere spitze '
            'Winkel ist neunzig minus zweiundzwanzig Komma sechs zwei, also siebenundsechzig Komma drei acht Grad.',
            f(r'\tan 22.62^\circ \approx 0.417 \;\checkmark', 300, 50, ein=0.4),
            f(r'90^\circ - x = 90^\circ - 22.62^\circ = \fc{67.38^\circ}', 430, 46, ein=7.7),
            graf(W2, rw_figur(C2, A2, B2, farbe_x=3) + [T(8.9, 0.35, '22.62°', 3, 'end', 28, False)], ein=0.3),
            graf(W2, [WI(B2, C2, A2, 3), T(0.25, 3.4, '67.38°', 3, 'start', 26, False)], ein=7.7, raster=False)),
         sz('Steigung',
            'Steigung ist dasselbe Verhältnis: Höhe durch waagrechte Strecke. Acht Prozent heisst null Komma null acht. Der '
            'Steigungswinkel ist Arcustangens von null Komma null acht, rund vier Komma fünf sieben Grad.',
            f(r'8\,\% = \dfrac{8}{100} = 0.08', 300, 50, ein=3.9),
            f(r'x = \arctan 0.08 \approx \fc{4.57^\circ}', 430, 48, ein=9.8),
            graf(W2, [V([A2s, B2s, C2s]), RW(C2s, 0, 90, px=14), WI(A2s, B2s, C2s, 2, 90), T(6, -0.85, '100 m', 5, 'middle', 28, False),
                      T(-0.4, 0.5, '8 m', 5, 'end', 28, False), T(4.9, 1.35, 'Höhe : Strecke', 5, 'middle', 26, False),
                      T(10.4, 0.5, 'x', 2, 'end', 28)], ein=0.3)),
         sz('Merke',
            'Zum Mitnehmen: Verhältnis bilden, dann die Umkehrtaste. Der Rechner gibt den Winkel in Grad, wenn er auf D E G steht. '
            'Und Probe machen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x = \arcsin\tfrac{GK}{H} = \arccos\tfrac{AK}{H} = \arctan\tfrac{GK}{AK}', 390, 42, ein=1.2),
            n('Rechner: @\\sin^{-1}@, @\\cos^{-1}@, @\\tan^{-1}@ im Modus @\\mathrm{DEG}@', 510, 'blau', 40, ein=3.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-winkel', 4, 'Dreiecke berechnen: Kontrollfragen zum Winkel',
     'Fünf Fragen: die richtige Umkehrtaste, ein Winkel aus zwei Katheten und aus Ankathete und Hypotenuse, was sin⁻¹ heisst '
     'und ein Steigungswinkel.',
     ['Arcusfunktion', 'Winkel berechnen', 'Steigung', 'Kontrollfragen'], [
         sz('Frage 1',
            'Gegenkathete und Hypotenuse gehören zum Sinus. Den Winkel liefert also Sinus hoch minus eins.',
            f(r'x = \arcsin\dfrac{GK}{H}', 300, 56, ein=1.0)),
         sz('Frage 2',
            'Gleich lange Katheten: Tangens x ist eins. Der Winkel ist fünfundvierzig Grad.',
            f(r'\tan x = \dfrac{7}{7} = 1 \;\Rightarrow\; x = \fc{45^\circ}', 300, 52, ein=1.0)),
         sz('Frage 3',
            'Ankathete und Hypotenuse: Cosinus. Arcuscosinus von vier Neunteln ist rund dreiundsechzig Komma sechs eins Grad.',
            f(r'x = \arccos\dfrac{4}{9} \approx \fc{63.61^\circ}', 300, 52, ein=1.0)),
         sz('Frage 4',
            'Sinus hoch minus eins von null Komma fünf ist der Winkel, dessen Sinus null Komma fünf ist.',
            n('@\\sin^{-1}(0.5)@: der Winkel mit @\\sin x = 0.5@', 300, 'blau', 46, ein=1.0)),
         sz('Frage 5',
            'Zwanzig Prozent heisst null Komma zwei. Arcustangens null Komma zwei ist rund elf Komma drei eins Grad.',
            f(r'x = \arctan 0.2 \approx \fc{11.31^\circ}', 300, 54, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Zwei Seiten bestimmen die Funktion, die Umkehrtaste den Winkel.',
            titel('Zum Mitnehmen', 250, 76),
            n('zwei Seiten → Funktion|Umkehrtaste → Winkel', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'GK und H sind bekannt. Welche Taste liefert x?', ['sin⁻¹', 'cos⁻¹', 'tan⁻¹'], 0,
              {0: 'Ja.', 1: 'cos braucht die Ankathete. Welche Seiten hast du?', 2: 'tan braucht die zwei Katheten. Welche Seiten hast du?'},
              sprich='G K und H sind bekannt. Welche Taste liefert x?',
              rueck_sprich={1: 'Cosinus braucht die Ankathete. Welche Seiten hast du?', 2: 'Tangens braucht die zwei Katheten. Welche Seiten hast du?'}),
         wahl('Frage 2', 'GK = 7 cm, AK = 7 cm. Wie gross ist x?', ['45°', '1°', '90°'], 0,
              {0: 'Ja.', 1: 'Eins ist tan x, nicht x. Was macht die Umkehrtaste daraus?', 2: '90° hat schon der rechte Winkel.'},
              sprich='G K gleich sieben, A K gleich sieben Zentimeter. Wie gross ist x?',
              rueck_sprich={1: 'Eins ist Tangens x, nicht x. Was macht die Umkehrtaste daraus?', 2: 'Neunzig Grad hat schon der rechte Winkel.'}),
         wahl('Frage 3', 'AK = 4 cm, H = 9 cm. Wie gross ist x?', ['≈ 63.61°', '≈ 26.39°', '≈ 23.96°'], 0,
              {0: 'Ja.', 1: 'Das wäre arcsin. Welche Funktion gehört zu AK und H?', 2: 'Das wäre arctan. Ist H eine Kathete?'},
              sprich='A K gleich vier, H gleich neun Zentimeter. Wie gross ist x?',
              rueck_sprich={1: 'Das wäre Arcussinus. Welche Funktion gehört zu A K und H?', 2: 'Das wäre Arcustangens. Ist H eine Kathete?'}),
         wahl('Frage 4', 'Was bedeutet sin⁻¹(0.5)?', ['der Winkel mit Sinus 0.5', '1 : sin(0.5)', '0.5 hoch minus eins'], 0,
              {0: 'Ja.', 1: 'Hoch minus eins heisst hier nicht Kehrwert.', 2: 'Das Hoch minus eins gehört zur Taste, nicht zur Zahl.'},
              sprich='Was bedeutet Sinus hoch minus eins von null Komma fünf?',
              rueck_sprich={1: 'Hoch minus eins heisst hier nicht Kehrwert.', 2: 'Das Hoch minus eins gehört zur Taste, nicht zur Zahl.'}),
         wahl('Frage 5', 'Eine Strasse steigt 20 %. Wie gross ist der Steigungswinkel?', ['≈ 11.31°', '20°', '≈ 87.14°'], 0,
              {0: 'Ja.', 1: 'Prozent sind keine Grad. Was ist tan x?', 2: 'Wie schreibt man 20 % als Zahl?'},
              sprich='Eine Strasse steigt zwanzig Prozent. Wie gross ist der Steigungswinkel?',
              rueck_sprich={1: 'Prozent sind keine Grad. Was ist Tangens x?', 2: 'Wie schreibt man zwanzig Prozent als Zahl?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung
# Baum: d = 15 m, α = 52° (Themenseite, Animation «Baumhöhe»): h = 15 tan 52° = 19.199 → 19.20 m;
# mit Augenhöhe 1.6 m: 20.80 m.
W3 = geo(-3, -3, 26.5)
D3, AL3 = 15, 52
H3 = D3 * math.tan(rad(AL3))
P3, F3, T3 = (0, 0), (D3, 0), (D3, H3)
BAUM = [S((-3, 0), (21, 0), 5, dicke=3), S(F3, (D3, H3), 5, dicke=7), KR((D3, H3 - 1.6), 1.6, 5, dicke=3)]
DREIECK3 = [V([P3, F3, T3], 1, 0.10), RW(F3, 180, 90)]
# Tiefenwinkel: Turm 12 m hoch bei x = 2, Boot bei x = 18 (nur Bild)
TT, TB = (2, 12), (18, 0)
clip('hoehen', 5, 'Dreiecke berechnen: Höhen und Distanzen',
     'Zuerst die Skizze: das rechtwinklige Dreieck aus Boden, Objekt und Sehstrahl. Höhenwinkel, Baumhöhe mit dem Tangens, '
     'Plausibilität, Augenhöhe, Tiefenwinkel und zwei Standorte.',
     ['Höhenwinkel', 'Tiefenwinkel', 'Sachaufgabe', 'Tangens'], [
         sz('Skizze zuerst',
            'Wie hoch ist der Baum? Du stehst fünfzehn Meter vom Stamm entfernt und siehst die Spitze unter dem Höhenwinkel '
            'zweiundfünfzig Grad. Zuerst die Skizze: Boden, Baum und Sehstrahl bilden ein rechtwinkliges Dreieck.',
            f(r'd = 15\,\mathrm{m}, \quad \fb{\alpha = 52^\circ}', 300, 48, ein=2.1),
            n('Skizze: Boden, Baum, Sehstrahl', 420, 'blau', 42, ein=7.4),
            graf(W3, BAUM + [T(7.5, -1.4, 'd = 15 m', 5, 'middle', 28, False)], punkte=[pt(P3)], ein=0.3),
            graf(W3, [S(P3, T3, 2, True, 3), WI(P3, F3, T3, 2, 60), T(3.2, 1.2, 'α', 2)], ein=5.7, raster=False),
            graf(W3, DREIECK3, ein=8.6, raster=False)),
         sz('Benennen',
            'Vom Höhenwinkel aus ist der Abstand am Boden die Ankathete und der Baum die Gegenkathete. Beteiligt sind die beiden '
            'Katheten, also Tangens.',
            f(r'\tan 52^\circ = \dfrac{h}{15}', 320, 54, ein=7.5),
            graf(W3, BAUM + DREIECK3 + [S(P3, T3, 2, True, 3), WI(P3, F3, T3, 2, 60), T(3.2, 1.2, 'α', 2)], punkte=[pt(P3)], ein=0.3),
            # Ton (sprechzeiten.py): «Ankathete» ≈ 3.1 s, «Gegenkathete» ≈ 4.6 s
            graf(W3, [mit(T(7.5, -1.4, 'AK', 2, 'middle', 30), ein=3.0), mit(T(16.4, H3 / 2, 'GK = h', 2, 'start', 30), ein=4.6)], ein=0.3, raster=False)),
         sz('Rechnen',
            'h gleich fünfzehn mal Tangens zweiundfünfzig Grad, rund neunzehn Komma zwei null Meter.',
            f(r'h = 15 \cdot \tan 52^\circ \approx \fc{19.20\,\mathrm{m}}', 320, 48, ein=0.4),
            graf(W3, BAUM + DREIECK3 + [S(P3, T3, 2, True, 3), WI(P3, F3, T3, 2, 60), T(3.2, 1.2, 'α', 2), T(7.5, -1.4, 'd = 15 m', 5, 'middle', 28, False)], punkte=[pt(P3)], ein=0.3),
            graf(W3, [T(16.4, H3 / 2, 'h ≈ 19.20 m', 3, 'start', 28, False)], ein=3.3, raster=False)),
         sz('Plausibel',
            'Plausibel? Der Winkel ist grösser als fünfundvierzig Grad. Darum ist der Baum höher, als du entfernt stehst. Das passt.',
            n('@\\alpha \\gt 45^\\circ@ heisst @h \\gt d@', 320, 'blau', 46, ein=3.7),
            graf(W3, BAUM + DREIECK3 + [S(P3, T3, 2, True, 3), WI(P3, F3, T3, 2, 60), T(3.2, 1.2, 'α', 2),
                                        S(P3, (15, 15), 5, True, 2.5), T(10.2, 11.6, '45°', 5, 'middle', 26, False)], punkte=[pt(P3)], ein=0.3)),
         sz('Augenhöhe',
            'Misst du mit dem Auge, beginnt das Dreieck auf Augenhöhe. Bei eins Komma sechs Metern kommt diese Höhe dazu: '
            'rund zwanzig Komma acht null Meter.',
            f(r'19.20\,\mathrm{m} + 1.6\,\mathrm{m} \approx \fc{20.80\,\mathrm{m}}', 320, 46, ein=5.9),
            graf(W3, [S((-3, 0), (21, 0), 5, dicke=3), S(F3, (D3, H3 + 1.6), 5, dicke=7), KR((D3, H3), 1.6, 5, dicke=3),
                      S((0, 0), (0, 1.6), 5, dicke=6), V([(0, 1.6), (D3, 1.6), (D3, H3 + 1.6)], 1, 0.10), RW((D3, 1.6), 180, 90),
                      WI((0, 1.6), (D3, 1.6), (D3, H3 + 1.6), 2, 60), T(-0.4, 0.5, '1.6 m', 2, 'end', 26, False)], ein=0.3)),
         sz('Tiefenwinkel',
            'Schaust du von oben hinunter, misst du den Tiefenwinkel gegen die Waagrechte. Er ist gleich gross wie der '
            'Höhenwinkel von unten: Wechselwinkel an Parallelen.',
            n('Tiefenwinkel = Höhenwinkel|(Wechselwinkel)', 300, 'blau', 44, ein=4.4),
            graf(W3, [S((-3, 0), (21, 0), 5, dicke=3), S((2, 0), TT, 5, dicke=7), S(TT, (19, 12), 5, True, 2.5),
                      S(TT, TB, 2, True, 3), V([(2, 0), TB, TT], 1, 0.08), RW((2, 0), 0, 90), T(18, -1.3, 'Boot', 5, 'middle', 26, False)],
                 punkte=[pt(TB)], ein=0.3),
            graf(W3, [WI(TT, TB, (19, 12), 2, 70), T(9.0, 11.0, 'β', 2)], ein=2.7, raster=False),
            graf(W3, [WI(TB, (-3, 0), TT, 2, 70), T(13.3, 0.8, 'β', 2)], ein=5.7, raster=False)),
         sz('Zwei Standorte',
            'Ist der Fuss unerreichbar, misst du von zwei Standorten mit bekanntem Abstand. Zwei Unbekannte, Höhe und Abstand, '
            'und zwei Gleichungen mit dem Tangens.',
            f(r'\tan\beta = \dfrac{h}{d}', 300, 48, ein=6.9),
            f(r'\tan\alpha = \dfrac{h}{d + s}', 420, 48, ein=7.4),
            graf(W3, [S((-3, 0), (21, 0), 5, dicke=3), S((18, 0), (18, 12), 5, dicke=7), S((0, 0), (18, 12), 2, True, 3), S((8, 0), (18, 12), 2, True, 3),
                      WI((0, 0), (18, 0), (18, 12), 2, 70), WI((8, 0), (18, 0), (18, 12), 2, 50), T(3.5, 0.8, 'α', 2), T(10.2, 0.9, 'β', 2),
                      T(4, -1.3, 's', 5), T(13, -1.3, 'd', 5), T(18.6, 6, 'h', 5, 'start')], punkte=[pt((0, 0)), pt((8, 0))], ein=0.3)),
         sz('Strategie',
            'Das Vorgehen: Skizze zeichnen, das rechtwinklige Dreieck suchen, die Seiten vom Winkel aus benennen, die Funktion '
            'wählen, rechnen und das Ergebnis prüfen.',
            titel('Vorgehen', 260, 72),
            n('1. Skizze|2. rechtwinkliges Dreieck suchen|3. Seiten vom Winkel aus benennen|4. Funktion wählen, rechnen|5. prüfen',
              380, 'blau', 44, ein=1.4)),
         sz('Merke',
            'Zum Mitnehmen: In der Sachaufgabe steckt ein rechtwinkliges Dreieck. Zuerst die Skizze, dann rechnen, dann prüfen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Skizze → Dreieck → Funktion → prüfen', 400, 'blau', 46, ein=1.2)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-hoehen', 6, 'Dreiecke berechnen: Kontrollfragen zu Höhen und Distanzen',
     'Fünf Fragen: die richtige Rechnung zur Turmhöhe, eine Abschätzung ohne Rechnen, der Tiefenwinkel, eine Leiter und '
     'zwei Standorte.',
     ['Höhenwinkel', 'Tiefenwinkel', 'Sachaufgabe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der Abstand ist die Ankathete, die Höhe die Gegenkathete: h gleich dreissig mal Tangens zwanzig Grad.',
            f(r'h = 30 \cdot \tan 20^\circ', 300, 56, ein=1.0)),
         sz('Frage 2',
            'Über fünfundvierzig Grad ist die Gegenkathete länger als die Ankathete. Der Turm ist höher als zehn Meter.',
            n('@\\alpha \\gt 45^\\circ@: @h \\gt d@', 300, 'blau', 50, ein=1.0)),
         sz('Frage 3',
            'Tiefenwinkel und Höhenwinkel sind Wechselwinkel an Parallelen. Der Höhenwinkel ist ebenfalls fünfzehn Grad.',
            n('Wechselwinkel: @15^\\circ@', 300, 'blau', 50, ein=1.0)),
         sz('Frage 4',
            'Die Leiter ist die Hypotenuse, die Höhe liegt dem Winkel gegenüber: fünf mal Sinus siebzig Grad, rund vier Komma '
            'sieben null Meter.',
            f(r'h = 5 \cdot \sin 70^\circ \approx \fc{4.70\,\mathrm{m}}', 300, 50, ein=1.0)),
         sz('Frage 5',
            'Höhe und Abstand sind unbekannt. Es braucht zwei Gleichungen: zwei Höhenwinkel von zwei Standorten mit bekanntem Abstand.',
            n('zwei Unbekannte: zwei Gleichungen', 300, 'blau', 46, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Skizze, rechtwinkliges Dreieck, Funktion — und das Ergebnis mit der Skizze vergleichen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Skizze → Dreieck → Funktion → prüfen', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Du stehst 30 m vor einem Turm und siehst die Spitze unter 20° (Augenhöhe vernachlässigt). Welche Rechnung gibt die Höhe?',
              ['30 · tan 20°', '30 · sin 20°', '30 : tan 20°'], 0,
              {0: 'Ja.', 1: 'sin braucht die Hypotenuse. Ist der Abstand die Hypotenuse?', 2: 'tan 20° = h : 30. Wie stellst du nach h um?'},
              sprich='Du stehst dreissig Meter vor einem Turm und siehst die Spitze unter zwanzig Grad. Die Augenhöhe ist vernachlässigt. Welche Rechnung gibt die Höhe?',
              rueck_sprich={1: 'Sinus braucht die Hypotenuse. Ist der Abstand die Hypotenuse?', 2: 'Tangens zwanzig Grad ist h durch dreissig. Wie stellst du nach h um?'}),
         wahl('Frage 2', 'Ohne Rechnen: Abstand 10 m, Höhenwinkel 60°. Der Turm ist …', ['höher als 10 m', 'genau 10 m hoch', 'niedriger als 10 m'], 0,
              {0: 'Ja.', 1: 'Genau 10 m wären es bei 45°. Liegt 60° darüber oder darunter?', 2: 'Bei 45° wären es genau 10 m. Was ändert ein grösserer Winkel?'},
              sprich='Ohne Rechnen: Abstand zehn Meter, Höhenwinkel sechzig Grad. Der Turm ist …',
              rueck_sprich={1: 'Genau zehn Meter wären es bei fünfundvierzig Grad. Liegt sechzig Grad darüber oder darunter?',
                            2: 'Bei fünfundvierzig Grad wären es genau zehn Meter. Was ändert ein grösserer Winkel?'}),
         wahl('Frage 3', 'Von der Turmspitze aus siehst du ein Boot unter dem Tiefenwinkel 15°. Unter welchem Höhenwinkel sieht man vom Boot die Turmspitze?',
              ['15°', '75°', '165°'], 0,
              {0: 'Ja.', 1: '75° ergänzt auf 90°. Wo liegen die beiden Winkel an den Parallelen?', 2: 'Der Höhenwinkel ist spitz. Vergleiche die Winkel an den beiden Waagrechten.'},
              sprich='Von der Turmspitze aus siehst du ein Boot unter dem Tiefenwinkel fünfzehn Grad. Unter welchem Höhenwinkel sieht man vom Boot die Turmspitze?',
              rueck_sprich={1: 'Fünfundsiebzig Grad ergänzt auf neunzig Grad. Wo liegen die beiden Winkel an den Parallelen?',
                            2: 'Der Höhenwinkel ist spitz. Vergleiche die Winkel an den beiden Waagrechten.'}),
         wahl('Frage 4', 'Eine 5 m lange Leiter bildet mit dem Boden 70°. Wie hoch reicht sie?', ['≈ 4.70 m', '≈ 1.71 m', '≈ 13.74 m'], 0,
              {0: 'Ja.', 1: 'Das ist der Abstand am Boden. Liegt die Höhe am Winkel an oder gegenüber?', 2: 'Höher als die Leiter lang ist? Welche Seite ist die Leiter?'},
              sprich='Eine fünf Meter lange Leiter bildet mit dem Boden siebzig Grad. Wie hoch reicht sie?',
              rueck_sprich={1: 'Das ist der Abstand am Boden. Liegt die Höhe am Winkel an oder gegenüber?', 2: 'Höher als die Leiter lang ist? Welche Seite ist die Leiter?'}),
         wahl('Frage 5', 'Der Fuss eines Bergs ist unerreichbar. Was brauchst du mindestens?',
              ['zwei Höhenwinkel und den Abstand der Standorte', 'einen Höhenwinkel', 'drei Höhenwinkel'], 0,
              {0: 'Ja.', 1: 'Ohne Abstand zum Fuss: Wie viele Unbekannte hat das Dreieck?', 2: 'Zwei Unbekannte brauchen zwei Gleichungen. Und was verbindet die Standorte?'},
              sprich='Der Fuss eines Bergs ist unerreichbar. Was brauchst du mindestens?',
              rueck_sprich={1: 'Ohne Abstand zum Fuss: Wie viele Unbekannte hat das Dreieck?', 2: 'Zwei Unbekannte brauchen zwei Gleichungen. Und was verbindet die Standorte?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung
# WSW (Themenseite A4a): α = 42°, β = 71°, c = 9 → γ = 67°, a = 9 sin 42°/sin 67° = 6.542, b = 9.244.
# C liegt bei b·(cos 42°, sin 42°) = (6.870 | 6.186); Höhe h_c: Fusspunkt (6.870 | 0).
W4 = geo(-1.2, -2.0, 11.5)
A4, B4 = (0, 0), (9, 0)
b4 = 9 * math.sin(rad(71)) / math.sin(rad(67))
C4 = (b4 * math.cos(rad(42)), b4 * math.sin(rad(42)))
FIG4 = [V([A4, B4, C4]), T(-0.4, -0.7, 'A', kursiv=False), T(9.4, -0.7, 'B', kursiv=False), T(C4[0], C4[1] + 0.45, 'C', kursiv=False)]
# SSW (Themenseite, Animation «SSW»): α = 35°, c = 6, a = 4.5 → sin γ = 0.7648, γ1 = 49.89°, γ2 = 130.11°.
W4s = geo(-1.0, -2.5, 11)
h4 = 6 * math.sin(rad(35))
t0, q4 = 6 * math.cos(rad(35)), math.sqrt(4.5 ** 2 - h4 ** 2)
C4a = ((t0 - q4) * math.cos(rad(35)), (t0 - q4) * math.sin(rad(35)))
C4b = ((t0 + q4) * math.cos(rad(35)), (t0 + q4) * math.sin(rad(35)))
STRAHL = (10 * math.cos(rad(35)), 10 * math.sin(rad(35)))
clip('sinussatz', 7, 'Dreiecke berechnen: der Sinussatz',
     'Die Höhe zerlegt das Dreieck in zwei rechtwinklige — daraus folgt a : sin α = b : sin β = c : sin γ. Ein Paar aus Seite '
     'und Gegenwinkel; vorgelöst mit zwei Winkeln und einer Seite; bei zwei Seiten und einem Gegenwinkel (SSW) zwei Dreiecke.',
     ['Sinussatz', 'allgemeines Dreieck', 'SSW', 'Gegenwinkel'], [
         sz('Die Höhe hilft',
            'Ohne rechten Winkel hilft die Höhe von C. Sie zerlegt das Dreieck in zwei rechtwinklige. Links ist h gleich b mal '
            'Sinus Alpha, rechts ist h gleich a mal Sinus Beta.',
            f(r'h = b \cdot \sin\alpha', 320, 52, ein=6.4),
            f(r'h = a \cdot \sin\beta', 430, 52, ein=8.7),
            graf(W4, FIG4 + [T(C4[0] / 2 - 0.5, C4[1] / 2 + 0.2, 'b', 5, 'end'), T((C4[0] + 9) / 2 + 0.4, C4[1] / 2 + 0.2, 'a', 5, 'start'),
                             T(4.5, -0.75, 'c', 5), WI(A4, B4, C4, 2, 40), WI(B4, C4, A4, 2, 40),
                             T(1.4, 0.45, 'α', 2), T(8.15, 0.6, 'β', 2)], ein=0.3),
            graf(W4, [S(C4, (C4[0], 0), 2, True, 3), RW((C4[0], 0), 0, 90, 2), T(C4[0] - 0.25, 2.6, 'h', 2, 'end')], ein=2.1, raster=False)),
         sz('Gleichsetzen',
            'Beides ist dieselbe Höhe. Also b mal Sinus Alpha gleich a mal Sinus Beta. Umgeformt: a durch Sinus Alpha gleich b '
            'durch Sinus Beta. Mit der Höhe von A kommt c durch Sinus Gamma dazu. Das ist der Sinussatz.',
            f(r'b \cdot \sin\alpha = a \cdot \sin\beta', 300, 48, ein=2.2),
            f(r'\dfrac{a}{\sin\alpha} = \dfrac{b}{\sin\beta} = \dfrac{c}{\sin\gamma}', 450, 52, ein=11.2),
            graf(W4, FIG4 + [S(C4, (C4[0], 0), 2, True, 3), RW((C4[0], 0), 0, 90, 2)], ein=0.3)),
         sz('Ein Paar',
            'Über dem Bruchstrich steht eine Seite, darunter der Sinus ihres Gegenwinkels. Du brauchst ein vollständiges Paar und '
            'eine weitere Angabe.',
            f(r'\dfrac{\fb{a}}{\sin\fb{\alpha}}', 320, 64, ein=2.7),
            n('Seite und ihr Gegenwinkel: ein Paar', 470, 'blau', 42, ein=4.7),
            graf(W4, FIG4 + [S(B4, C4, 2, dicke=8), WI(A4, B4, C4, 2, 40), T(1.4, 0.45, 'α', 2), T((C4[0] + 9) / 2 + 0.4, C4[1] / 2 + 0.2, 'a', 2, 'start')], ein=0.3)),
         sz('Vorgelöst',
            'Beispiel: Alpha zweiundvierzig Grad, Beta einundsiebzig Grad, c gleich neun Zentimeter. Zuerst Gamma: hundertachtzig '
            'minus zweiundvierzig minus einundsiebzig gleich siebenundsechzig Grad. Jetzt ist das Paar c und Gamma vollständig. '
            'a gleich neun mal Sinus zweiundvierzig Grad durch Sinus siebenundsechzig Grad, rund sechs Komma fünf vier Zentimeter.',
            f(r'\fb{\alpha = 42^\circ}, \ \fb{\beta = 71^\circ}, \ \fb{c = 9\,\mathrm{cm}}', 290, 44, ein=0.4),
            f(r'\gamma = 180^\circ - 42^\circ - 71^\circ = 67^\circ', 390, 44, ein=9.9),
            f(r'a = \dfrac{9 \cdot \sin 42^\circ}{\sin 67^\circ} \approx \fc{6.54\,\mathrm{cm}}', 510, 46, ein=18.4),
            graf(W4, FIG4 + [WI(A4, B4, C4, 2, 40), WI(B4, C4, A4, 2, 40), T(1.6, 0.45, '42°', 2, 'start', 26, False),
                             T(7.95, 0.6, '71°', 2, 'end', 26, False), T(4.5, -0.8, 'c = 9', 2, 'middle', 28, False)], ein=0.3),
            graf(W4, [WI(C4, A4, B4, 1, 40), T(C4[0], C4[1] - 1.25, '67°', 1, 'middle', 26, False)], ein=9.9, raster=False),
            graf(W4, [T((C4[0] + 9) / 2 + 0.4, C4[1] / 2 + 0.2, 'a ≈ 6.54', 3, 'start', 28, False)], ein=18.4, raster=False)),
         sz('Zwei Dreiecke',
            'Sind zwei Seiten und der Gegenwinkel einer davon gegeben, wird es heikel. Alpha fünfunddreissig Grad, c gleich sechs, '
            'a gleich vier Komma fünf. Der Kreis um B mit dem Radius a trifft den Schenkel zweimal: Es gibt zwei Dreiecke.',
            f(r'\fb{\alpha = 35^\circ}, \ \fb{c = 6}, \ \fb{a = 4.5}', 290, 46, ein=4.2),
            n('SSW: zwei Dreiecke möglich', 410, 'blau', 42, ein=11.6),
            graf(W4s, [S((0, 0), STRAHL, 5, dicke=2.5), S((0, 0), (6, 0), 1, dicke=4), WI((0, 0), (6, 0), STRAHL, 2, 50),
                       # «35°» dicht am Bogen bei A, nicht unter C₂; c gegeben, also orange
                       T(0.85, 0.1, '35°', 2, 'start', 24, False), T(3, -0.75, 'c = 6', 2, 'middle', 28, False),
                       T(-0.35, -0.65, 'A', kursiv=False), T(6.3, -0.65, 'B', kursiv=False)], punkte=[pt((0, 0)), pt((6, 0))], ein=0.3),
            graf(W4s, [KR((6, 0), 4.5, 2, gestrichelt=True, dicke=2.5)], ein=8.7, raster=False),
            graf(W4s, [V([(0, 0), (6, 0), C4a], 1, 0.15), V([(0, 0), (6, 0), C4b], 1, 0.06),
                       T(C4a[0] - 0.3, C4a[1] + 0.35, 'C₂', 1, 'end', 28, False), T(C4b[0] - 0.3, C4b[1] + 0.35, 'C₁', 1, 'end', 28, False)],
                 punkte=[pt(C4a, 1), pt(C4b, 1)], ein=10.6, raster=False)),
         sz('Zweite Lösung',
            'Der Sinussatz gibt Sinus Gamma gleich sechs mal Sinus fünfunddreissig Grad durch vier Komma fünf, rund null Komma '
            'sieben sechs fünf. Der Rechner liefert nur den spitzen Winkel, rund neunundvierzig Komma acht neun Grad. Der '
            'zweite ist hundertachtzig Grad minus diesem Winkel, rund hundertdreissig Komma eins eins Grad. Beide haben denselben '
            'Sinus.',
            f(r'\sin\gamma = \dfrac{6 \cdot \sin 35^\circ}{4.5} \approx 0.765', 290, 44, ein=0.4),
            f(r'\gamma_1 \approx \fc{49.89^\circ}', 410, 46, ein=9.6),
            f(r'\gamma_2 = 180^\circ - \gamma_1 \approx \fc{130.11^\circ}', 510, 44, ein=14.9),
            n('@\\sin(180^\\circ - \\gamma) = \\sin\\gamma@ — warum: Einheitskreis (5.4)', 620, 'blau', 36, ein=17.7),
            graf(W4s, [S((0, 0), STRAHL, 5, dicke=2.5), S((0, 0), (6, 0), 1, dicke=4), KR((6, 0), 4.5, 2, gestrichelt=True, dicke=2.5),
                       V([(0, 0), (6, 0), C4a], 1, 0.15), V([(0, 0), (6, 0), C4b], 1, 0.06),
                       T(C4a[0] - 0.3, C4a[1] + 0.35, 'C₂', 1, 'end', 28, False), T(C4b[0] - 0.3, C4b[1] + 0.35, 'C₁', 1, 'end', 28, False),
                       T(-0.35, -0.65, 'A', kursiv=False), T(6.3, -0.65, 'B', kursiv=False)], punkte=[pt((0, 0)), pt((6, 0)), pt(C4a, 1), pt(C4b, 1)], ein=0.3),
            # γ₁ (spitz) liegt beim fernen Schnittpunkt C₁, γ₂ (stumpf) beim nahen C₂
            graf(W4s, [WI(C4b, (0, 0), (6, 0), 3, 40)], ein=9.6, raster=False),
            graf(W4s, [WI(C4a, (0, 0), (6, 0), 3, 40)], ein=14.9, raster=False)),
         sz('Prüfen',
            'Prüfe jeden Kandidaten: Ist Alpha plus Gamma kleiner als hundertachtzig Grad, gibt es das Dreieck. Hier gilt es für '
            'beide.',
            f(r'35^\circ + 130.11^\circ \lt 180^\circ \;\checkmark', 320, 50, ein=1.6),
            n('Beide Dreiecke gibt es.', 460, 'blau', 44, ein=5.5)),
         sz('Merke',
            'Zum Mitnehmen: Seite durch Sinus des Gegenwinkels, in jedem Dreieck gleich. Bei SSW an den stumpfen zweiten Winkel '
            'denken.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\dfrac{a}{\sin\alpha} = \dfrac{b}{\sin\beta} = \dfrac{c}{\sin\gamma}', 400, 48, ein=1.2),
            n('SSW: auch @180^\\circ - \\gamma_1@ prüfen', 560, 'blau', 42, ein=5.1)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-sinussatz', 8, 'Dreiecke berechnen: Kontrollfragen zum Sinussatz',
     'Fünf Fragen: die richtige Gleichung, was zuerst kommt, der zweite Winkel mit demselben Sinus und wie viele Dreiecke '
     'es im Fall SSW gibt.',
     ['Sinussatz', 'SSW', 'Kontrollfragen'], [
         sz('Frage 1',
            'Jede Seite steht über dem Sinus ihres Gegenwinkels: b durch Sinus sechzig Grad gleich sieben durch Sinus fünfzig Grad.',
            f(r'\dfrac{b}{\sin 60^\circ} = \dfrac{7}{\sin 50^\circ}', 300, 54, ein=1.0)),
         sz('Frage 2',
            'Das Paar zu c fehlt noch: Zuerst Gamma, hundertachtzig minus dreissig minus fünfundvierzig gleich hundertfünf Grad.',
            f(r'\gamma = 180^\circ - 30^\circ - 45^\circ = \fc{105^\circ}', 300, 50, ein=1.0)),
         sz('Frage 3',
            'Hundertachtzig minus vierzig ist hundertvierzig Grad. Dieser Winkel hat denselben Sinus.',
            f(r'180^\circ - 40^\circ = \fc{140^\circ}', 300, 56, ein=1.0)),
         sz('Frage 4',
            'Die Höhe ist sechs mal Sinus fünfunddreissig Grad, rund drei Komma vier vier. a ist kürzer: Der Kreis um B erreicht den '
            'Schenkel nicht. Kein Dreieck.',
            f(r'h = 6 \cdot \sin 35^\circ \approx 3.44 \gt 2.5', 300, 48, ein=1.0)),
         sz('Frage 5',
            'Achtzig plus hundertfünfzig ist mehr als hundertachtzig Grad. Den stumpfen Kandidaten gibt es hier nicht.',
            f(r'80^\circ + 150^\circ \gt 180^\circ', 300, 54, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Paar aus Seite und Gegenwinkel suchen. Bei SSW den stumpfen Kandidaten prüfen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Paar suchen|SSW: @180^\\circ - \\gamma_1@ prüfen', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'a = 7, α = 50°, β = 60°. Welche Gleichung stimmt?',
              ['b : sin 60° = 7 : sin 50°', 'b : sin 50° = 7 : sin 60°', 'b · sin 60° = 7 · sin 50°'], 0,
              {0: 'Ja.', 1: 'Zu b gehört sein Gegenwinkel. Welcher ist das?', 2: 'Seite durch Sinus, nicht Seite mal Sinus.'},
              sprich='a gleich sieben, Alpha gleich fünfzig Grad, Beta gleich sechzig Grad. Welche Gleichung stimmt?',
              rueck_sprich={1: 'Zu b gehört sein Gegenwinkel. Welcher ist das?', 2: 'Seite durch Sinus, nicht Seite mal Sinus.'}),
         wahl('Frage 2', 'α = 30°, β = 45°, c = 10. Was rechnest du zuerst?', ['γ aus der Winkelsumme', 'a = 10 · sin 30°', 'c : sin 30°'], 0,
              {0: 'Ja.', 1: 'Das gilt nur im rechtwinkligen Dreieck. Welches Paar ist vollständig?', 2: 'c und α sind kein Paar. Was fehlt zu c?'},
              sprich='Alpha gleich dreissig Grad, Beta gleich fünfundvierzig Grad, c gleich zehn. Was rechnest du zuerst?',
              rueck_sprich={1: 'Das gilt nur im rechtwinkligen Dreieck. Welches Paar ist vollständig?', 2: 'c und Alpha sind kein Paar. Was fehlt zu c?'}),
         wahl('Frage 3', 'Der Rechner gibt γ = 40°. Welcher zweite Winkel im Dreieck hat denselben Sinus?', ['140°', '50°', '220°'], 0,
              {0: 'Ja.', 1: 'Das ergänzt auf 90°. Wo liegt der zweite Schnittpunkt?', 2: 'Ein Dreieckswinkel ist kleiner als 180°.'},
              sprich='Der Rechner gibt Gamma gleich vierzig Grad. Welcher zweite Winkel im Dreieck hat denselben Sinus?',
              rueck_sprich={1: 'Das ergänzt auf neunzig Grad. Wo liegt der zweite Schnittpunkt?', 2: 'Ein Dreieckswinkel ist kleiner als hundertachtzig Grad.'}),
         wahl('Frage 4', 'α = 35°, c = 6, a = 2.5. Wie viele Dreiecke gibt es?', ['keines', 'eines', 'zwei'], 0,
              {0: 'Ja.', 1: 'Vergleiche a mit der Höhe c · sin α.', 2: 'Vergleiche a mit der Höhe c · sin α.'},
              sprich='Alpha gleich fünfunddreissig Grad, c gleich sechs, a gleich zwei Komma fünf. Wie viele Dreiecke gibt es?',
              rueck_sprich={1: 'Vergleiche a mit der Höhe c mal Sinus Alpha.', 2: 'Vergleiche a mit der Höhe c mal Sinus Alpha.'}),
         wahl('Frage 5', 'α = 80°. Aus dem Sinussatz folgt γ₁ = 30°. Gibt es auch γ₂ = 150°?', ['nein', 'ja', 'nur bei a = c'], 0,
              {0: 'Ja.', 1: 'Rechne α + γ₂. Passt das in ein Dreieck?', 2: 'Rechne α + γ₂. Passt das in ein Dreieck?'},
              sprich='Alpha gleich achtzig Grad. Aus dem Sinussatz folgt Gamma eins gleich dreissig Grad. Gibt es auch Gamma zwei gleich hundertfünfzig Grad?',
              rueck_sprich={1: 'Rechne Alpha plus Gamma zwei. Passt das in ein Dreieck?', 2: 'Rechne Alpha plus Gamma zwei. Passt das in ein Dreieck?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 5 · Einführung
# SWS (Themenseite A4b): b = 7, c = 10, α = 55° → a² = 149 − 140 cos 55° = 68.70, a = 8.29; A = 35 sin 55° = 28.67.
W5 = geo(-4.5, -3.5, 15.5)
def tri5(al, b=7, c=10):
    return [(0, 0), (c, 0), (b * math.cos(rad(al)), b * math.sin(rad(al)))]
P5 = tri5(55)
def tri5_bew(t0, t1, al0, al1):
    """Dreieck, dessen Winkel α von al0 nach al1 läuft (dichte Stützpunkte, weil C auf einem Kreis wandert)."""
    k = 12
    bew = [[round(t0 + (t1 - t0) * i / k, 3), {'punkte': [r3(p) for p in tri5(al0 + (al1 - al0) * (i / k) ** 2 * (3 - 2 * i / k))]}] for i in range(k + 1)]
    return bew
def wi5_bew(t0, t1, al0, al1):
    k = 12
    return [[round(t0 + (t1 - t0) * i / k, 3), {'bis': round(al0 + (al1 - al0) * (i / k) ** 2 * (3 - 2 * i / k), 2)}] for i in range(k + 1)]
def a5_bew(t0, t1, al0, al1):
    """Seite a = BC grün hervorgehoben, läuft mit dem Dreieck mit; dazu ihr Name «a» an der Mitte."""
    k = 12
    def C(i):
        return tri5(al0 + (al1 - al0) * (i / k) ** 2 * (3 - 2 * i / k))[2]
    def L(i):   # Name «a» neben der Mitte von BC, auf der von A abgewandten Seite (0.7 Einheiten)
        c = C(i)
        m, d = ((c[0] + 10) / 2, c[1] / 2), (c[0] - 10, c[1])
        nx, ny = d[1], -d[0]
        if nx * m[0] + ny * m[1] < 0:
            nx, ny = -nx, -ny
        n_ = math.hypot(nx, ny)
        return [round(m[0] + 0.7 * nx / n_, 3), round(m[1] + 0.7 * ny / n_ - 0.2, 3)]
    strecke = mit(S((10, 0), C(0), 3, dicke=8), bewegung=[[round(t0 + (t1 - t0) * i / k, 3), {'bis': r3(C(i))}] for i in range(k + 1)])
    name = mit(T(L(0)[0], L(0)[1], 'a', 3), bewegung=[[round(t0 + (t1 - t0) * i / k, 3), {'bei': L(i)}] for i in range(k + 1)])
    return [strecke, name]
FIG5 = [V(P5), T(-0.45, -0.7, 'A', kursiv=False), T(10.4, -0.7, 'B', kursiv=False), T(P5[2][0], P5[2][1] + 0.45, 'C', kursiv=False)]
clip('cosinussatz', 9, 'Dreiecke berechnen: Cosinussatz und Fläche',
     'Ohne Paar aus Seite und Gegenwinkel: a² = b² + c² − 2bc · cos α, bei 90° Pythagoras, bei stumpfem Winkel wird a länger; '
     'drei Seiten geben den Winkel; Fläche ½ · b · c · sin α; welcher Satz wann.',
     ['Cosinussatz', 'Dreiecksfläche', 'SWS', 'SSS'], [
         sz('Kein Paar',
            'Kennst du zwei Seiten und den Winkel dazwischen, fehlt jedes Paar aus Seite und Gegenwinkel. Dann hilft der '
            'Cosinussatz.',
            f(r'\fb{b = 7}, \ \fb{c = 10}, \ \fb{\alpha = 55^\circ}', 300, 46, ein=0.4),
            graf(W5, FIG5 + [WI((0, 0), (10, 0), P5[2], 2, 44), T(1.5, 0.55, 'α', 2), T(P5[2][0] / 2 - 0.4, P5[2][1] / 2 + 0.2, 'b', 2, 'end'),
                             T(5, -0.8, 'c', 2), T((P5[2][0] + 10) / 2 + 0.4, P5[2][1] / 2 + 0.2, 'a = ?', 3, 'start')], ein=0.3)),
         sz('Formel',
            'a Quadrat gleich b Quadrat plus c Quadrat minus zwei b c mal Cosinus Alpha. Links steht die gesuchte Seite, im Cosinus '
            'ihr Gegenwinkel.',
            f(r'a^2 = b^2 + c^2 - 2bc \cdot \cos\alpha', 320, 52, ein=0.4),
            graf(W5, FIG5 + [WI((0, 0), (10, 0), P5[2], 2, 44), T(1.5, 0.55, 'α', 2), S((10, 0), P5[2], 3, dicke=8)], ein=0.3)),
         sz('Pythagoras',
            'Bei neunzig Grad ist der Cosinus null. Übrig bleibt der Satz des Pythagoras. Der Cosinussatz ist Pythagoras mit einem '
            'Korrekturglied.',
            f(r'\cos 90^\circ = 0 \;\Rightarrow\; a^2 = b^2 + c^2', 320, 48, ein=2.4),
            n('Korrekturglied @-2bc \\cdot \\cos\\alpha@', 450, 'blau', 42, ein=5.2),
            graf(W5, [mit(V(P5), bewegung=tri5_bew(0.5, 2.4, 55, 90)), T(-0.45, -0.7, 'A', kursiv=False), T(10.4, -0.7, 'B', kursiv=False),
                      mit(WI((0, 0), (10, 0), P5[2], 2, 44), bewegung=wi5_bew(0.5, 2.4, 55, 90))] + a5_bew(0.5, 2.4, 55, 90), ein=0.3),
            graf(W5, [RW((0, 0), 0, 90, 2)], ein=2.4, raster=False)),
         sz('Stumpf',
            'Ist Alpha stumpf, ist der Cosinus negativ. Das Korrekturglied wird positiv, und a wird länger als beim rechten Winkel. '
            'Der Rechner kennt den Cosinus auch für stumpfe Winkel.',
            f(r'\alpha \gt 90^\circ: \ \cos\alpha \lt 0', 300, 50, ein=0.4),
            n('@-2bc \\cdot \\cos\\alpha \\gt 0@: @a@ länger als bei @90^\\circ@', 420, 'blau', 42, ein=2.9),
            n('warum @\\cos\\alpha \\lt 0@: Einheitskreis (5.4)', 540, 'blau', 36, ein=7.4),
            graf(W5, [mit(V(tri5(90)), bewegung=tri5_bew(0.5, 2.6, 90, 125)), T(-0.45, -0.7, 'A', kursiv=False), T(10.4, -0.7, 'B', kursiv=False),
                      mit(WI((0, 0), (10, 0), tri5(90)[2], 2, 44), bewegung=wi5_bew(0.5, 2.6, 90, 125)),
                      S((10, 0), tri5(90)[2], 5, True, 3)] + a5_bew(0.5, 2.6, 90, 125), ein=0.3)),
         sz('Vorgelöst',
            'Beispiel: b gleich sieben, c gleich zehn, Alpha fünfundfünfzig Grad. a Quadrat gleich neunundvierzig plus hundert '
            'minus hundertvierzig mal Cosinus fünfundfünfzig Grad, rund achtundsechzig Komma sieben. a ist rund acht Komma zwei '
            'neun.',
            f(r'a^2 = 49 + 100 - 140 \cdot \cos 55^\circ \approx 68.70', 300, 42, ein=4.2),
            f(r'a \approx \fc{8.29}', 420, 54, ein=10.8),
            graf(W5, FIG5 + [WI((0, 0), (10, 0), P5[2], 2, 44), T(1.4, 0.55, '55°', 2, 'start', 26, False),
                             T(P5[2][0] / 2 - 0.4, P5[2][1] / 2 + 0.2, '7', 2, 'end', 28, False), T(5, -0.8, '10', 2, 'middle', 28, False)], ein=0.3),
            graf(W5, [T((P5[2][0] + 10) / 2 + 0.4, P5[2][1] / 2 + 0.2, 'a ≈ 8.29', 3, 'start', 28, False)], ein=10.8, raster=False)),
         sz('Drei Seiten',
            'Sind drei Seiten bekannt, stellst du nach dem Cosinus um und nimmst den Arcuscosinus. Ein negativer Cosinus heisst: '
            'Der Winkel ist stumpf.',
            f(r'\cos\alpha = \dfrac{b^2 + c^2 - a^2}{2bc}', 320, 52, ein=0.4),
            n('negativ: @\\alpha@ ist stumpf', 470, 'blau', 42, ein=4.9)),
         sz('Fläche',
            'Die Fläche braucht dieselben drei Stücke. Die Höhe auf c ist b mal Sinus Alpha. Also ist A gleich ein Halb mal b mal c '
            'mal Sinus Alpha, hier rund achtundzwanzig Komma sechs sieben.',
            f(r'h = b \cdot \sin\alpha', 290, 46, ein=2.6),
            f(r'A = \dfrac{b \cdot c}{2} \cdot \sin\alpha \approx \fc{28.67}', 410, 46, ein=7.7),
            graf(W5, FIG5 + [WI((0, 0), (10, 0), P5[2], 2, 44), T(1.4, 0.55, '55°', 2, 'start', 26, False), V(P5, 3, 0.18, dicke=0)], ein=0.3),
            graf(W5, [S(P5[2], (P5[2][0], 0), 2, True, 3), RW((P5[2][0], 0), 0, 90, 2), T(P5[2][0] + 0.3, 2.6, 'h', 2, 'start')], ein=2.6, raster=False)),
         sz('Welcher Satz',
            'Und welcher Satz wann? Suche ein Paar aus Seite und Gegenwinkel. Findest du eines, nimm den Sinussatz, sonst den '
            'Cosinussatz.',
            titel('Welcher Satz?', 260, 72),
            n('Paar aus Seite und Gegenwinkel?|ja: Sinussatz (WSW, WWS, SSW)|nein: Cosinussatz (SWS, SSS)', 380, 'blau', 44, ein=1.9)),
         sz('Merke',
            'Zum Mitnehmen: Cosinussatz ist Pythagoras mit Korrekturglied. Die Fläche ist ein Halb mal zwei Seiten mal Sinus des '
            'Winkels dazwischen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'a^2 = b^2 + c^2 - 2bc \cdot \cos\alpha', 390, 46, ein=1.2),
            f(r'A = \tfrac{1}{2} \cdot b \cdot c \cdot \sin\alpha', 500, 46, ein=3.6)),
         JETZT_DU,
     ])

# ════════════════════════════════════════════════ Kapitel 5 · Kontrolle
clip('kontrolle-cosinussatz', 10, 'Dreiecke berechnen: Kontrollfragen zu Cosinussatz und Fläche',
     'Fünf Fragen: welcher Satz, was bei 90° übrig bleibt, eine Seite, ein negativer Cosinus und eine Fläche.',
     ['Cosinussatz', 'Dreiecksfläche', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zwei Seiten und der Winkel dazwischen: Es gibt kein Paar. Das ist der Fall für den Cosinussatz.',
            n('SWS: Cosinussatz', 300, 'blau', 52, ein=1.0)),
         sz('Frage 2',
            'Cosinus neunzig Grad ist null. Es bleibt a Quadrat gleich b Quadrat plus c Quadrat.',
            f(r'a^2 = b^2 + c^2', 300, 60, ein=1.0)),
         sz('Frage 3',
            'Neun plus fünfundzwanzig minus dreissig mal Cosinus sechzig Grad, das ist neunzehn. Die Wurzel ist rund vier Komma '
            'drei sechs.',
            f(r'a = \sqrt{9 + 25 - 30 \cdot \cos 60^\circ} \approx \fc{4.36}', 300, 46, ein=1.0)),
         sz('Frage 4',
            'Ein negativer Cosinus gehört zu einem stumpfen Winkel. Kein Rechenfehler.',
            n('@\\cos\\gamma \\lt 0@: @\\gamma@ stumpf', 300, 'blau', 50, ein=1.0)),
         sz('Frage 5',
            'Ein Halb mal sechs mal vier mal Sinus dreissig Grad: zwölf mal null Komma fünf, also sechs.',
            f(r'A = \dfrac{6 \cdot 4}{2} \cdot \sin 30^\circ = \fc{6}', 300, 52, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Kein Paar, dann Cosinussatz. Fläche mit dem Sinus des Zwischenwinkels.',
            titel('Zum Mitnehmen', 250, 76),
            n('kein Paar: Cosinussatz|Fläche: @\\tfrac{1}{2}\\, b c \\sin\\alpha@', 400, 'blau', 46, ein=1.2)),
     ], [
         wahl('Frage 1', 'Gegeben sind b, c und der Winkel α dazwischen. Womit beginnst du?', ['Cosinussatz', 'Sinussatz', 'Pythagoras'], 0,
              {0: 'Ja.', 1: 'Gibt es ein Paar aus Seite und Gegenwinkel?', 2: 'Ist das Dreieck rechtwinklig?'},
              sprich='Gegeben sind b, c und der Winkel Alpha dazwischen. Womit beginnst du?',
              rueck_sprich={1: 'Gibt es ein Paar aus Seite und Gegenwinkel?', 2: 'Ist das Dreieck rechtwinklig?'}),
         wahl('Frage 2', 'Was wird aus dem Cosinussatz bei α = 90°?', ['a² = b² + c²', 'a² = b² + c² − 2bc', 'a = b + c'], 0,
              {0: 'Ja.', 1: 'Wie gross ist cos 90°?', 2: 'Wie gross ist cos 90°? Und wo bleiben die Quadrate?'},
              sprich='Was wird aus dem Cosinussatz bei Alpha gleich neunzig Grad?',
              rueck_sprich={1: 'Wie gross ist Cosinus neunzig Grad?', 2: 'Wie gross ist Cosinus neunzig Grad? Und wo bleiben die Quadrate?'}),
         wahl('Frage 3', 'b = 3, c = 5, α = 60°. Wie lang ist a?', ['≈ 4.36', '≈ 5.83', '7'], 0,
              {0: 'Ja.', 1: 'Das ist die Wurzel aus b² + c². Wo bleibt das Korrekturglied?', 2: 'Vorzeichen: Das Korrekturglied wird abgezogen.'},
              sprich='b gleich drei, c gleich fünf, Alpha gleich sechzig Grad. Wie lang ist a?',
              rueck_sprich={1: 'Das ist die Wurzel aus b Quadrat plus c Quadrat. Wo bleibt das Korrekturglied?', 2: 'Vorzeichen: Das Korrekturglied wird abgezogen.'}),
         wahl('Frage 4', 'Aus drei Seiten folgt cos γ = −0.2. Was heisst das?', ['γ ist stumpf', 'verrechnet', 'γ ist spitz'], 0,
              {0: 'Ja.', 1: 'Der Cosinus darf negativ sein. Bei welchen Winkeln?', 2: 'Welche Winkel haben einen negativen Cosinus?'},
              sprich='Aus drei Seiten folgt Cosinus Gamma gleich minus null Komma zwei. Was heisst das?',
              rueck_sprich={1: 'Der Cosinus darf negativ sein. Bei welchen Winkeln?', 2: 'Welche Winkel haben einen negativen Cosinus?'}),
         wahl('Frage 5', 'b = 6, c = 4, α = 30° dazwischen. Wie gross ist die Fläche?', ['6', '12', '≈ 10.39'], 0,
              {0: 'Ja.', 1: 'Das wäre der rechte Winkel. Wo bleibt der Sinus?', 2: 'Die Höhe kommt mit dem Sinus, nicht mit dem Cosinus.'},
              sprich='b gleich sechs, c gleich vier, Alpha gleich dreissig Grad dazwischen. Wie gross ist die Fläche?',
              rueck_sprich={1: 'Das wäre der rechte Winkel. Wo bleibt der Sinus?', 2: 'Die Höhe kommt mit dem Sinus, nicht mit dem Cosinus.'}),
     ], art='Kontrollclip')
