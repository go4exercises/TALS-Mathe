"""Erzeugt die zwölf Drehbücher des Leitprogramms Modellieren (08.10.2026).

  python3 scripts/lp/modellieren/clips.py

Je Kapitel (Aufgabenart) drei Clips: ein Einführungsclip mit der Grundgleichung der Aufgabenart und
zwei Kontrollclips — «eine Unbekannte» (lineare und quadratische Gleichung) und «zwei Unbekannte»
(lineares und quadratisches Gleichungssystem). Jede Aufgabe läuft in fünf Schritten: Deklaration →
Ansatz → Grundform → Lösen → Antwort, an jedem Schritt eine Kontrollfrage. Bausteine und Layout:
clips_basis.py. Das Skript rettet beim Neulauf die gemessenen `dauer` (Szenenname und Sprechertext
gleich); `ein` der Auflösungen steht auf dem Wort, das sie nennt («@wort», wortzeiten.json).
Zahlen: zahlen.py.

Rechner (TI-30X Pro MultiView, in Europa TI-30X Pro MathPrint): Anzeigen wie in den Clips
g2-2b-ti30x-poly-solv und g2-3-ti30x-sys-solv, belegt in der TI-Online-Hilfe «Gleichungslöser»
(mt_solvers): poly-solv fragt a, b, c einzeln ab und zeigt x1, x2 je auf einem Schirm, exakt als Bruch;
sys-solv nimmt die Zeilen als (a)x+(b)y=c, das Zeichen vor dem y-Glied mit + oder −, negative Zahl mit
(−); Ergebnis x =, y =; die Taste ↔ (in der Online-Hilfe [r]) schaltet Bruch ↔ Dezimalzahl.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clips_basis import *          # noqa: F401,F403
from clips_basis import FEHLT, WZ, clip, kontrolle, sz, f, tx, n, titel, rechner, stapel, G_text, G_formel, \
    LX, RX, JETZT_DU, NB  # noqa: E402

PM = 'POLY SOLVER'
POLY_MENU = ([PM, '1:ax²+bx+c=0', '2:ax³+bx²+cx+d=0'], ['2nd', 'poly-solv'])
SYS_MENU = (['SYSTEM SOLVER', '1:2x2 Linear EQs', '2:3x3 Linear Sys'], ['2nd', 'sys-solv'])


def poly_eingabe(a, b, c, y, ein, x=LX, breite=520):
    """poly-solv aufrufen und a, b, c eingeben (je ein Schirm, wie am Gerät)."""
    neg = lambda v: ('⁻' + str(v)[1:]) if str(v).startswith('-') else str(v)
    taste = lambda v: (['(−)', str(v)[1:]] if str(v).startswith('-') else [str(v)])
    return stapel([POLY_MENU, (['a=' + neg(a), '', ''], ['enter'] + taste(a)), (['b=' + neg(b), '', ''], ['enter'] + taste(b)),
                   (['c=' + neg(c), '', ''], ['enter'] + taste(c))], y, ein, 1.3, x, breite)


def zeile(a, b, c):
    """Eine Zeile der sys-solv-Maske wie am Gerät: (a)x+(b)y=c; Zeichen vor dem y-Glied mit + oder −,
    negative Zahl rechts mit (−) — so in der Online-Hilfe und im Clip g2-3-ti30x-sys-solv."""
    assert a > 0
    anz = '(%s)x%s(%s)y=%s' % (a, '-' if b < 0 else '+', abs(b), ('⁻%s' % -c) if c < 0 else c)
    assert len(anz) <= 16, anz
    tasten = [str(a), 'enter'] + (['−'] if b < 0 else []) + [str(abs(b)), 'enter'] + (['(−)', str(-c)] if c < 0 else [str(c)])
    return anz, tasten


def sys_eingabe(r1, r2, y, ein, x=LX, breite=520):
    z1, t1 = zeile(*r1)
    z2, t2 = zeile(*r2)
    return stapel([SYS_MENU, ([z1, ''], ['enter'] + t1), ([z1, z2], ['enter'] + t2)], y, ein, 1.8, x, breite)


def ergebnis(l, r, y=515, ein=0.05):
    """Zwei Ergebnisschirme nebeneinander (x1, x2 bzw. x, y), je ein Schirm wie am Gerät; gegeben, wenn die Frage kommt."""
    return [dict(rechner([l, ''], ['enter'], y, ein, RX, 400), _gegeben=True),
            dict(rechner([r, ''], ['enter'], y, ein, RX + 420, 400), _gegeben=True)]


def merke(spr, zeilen):
    return sz('Merke', spr, titel('Zum Mitnehmen', 250, 76), n(zeilen, 390, 'blau', 46, ein=1.2))


# ════════════════════════════════════════════════ Kapitel 1 · Einführung
def stangen(x0, anzahl, farbe, ein=None):
    """Zehnerstangen: Rechteck 0.9 × 10 mit neun Teilstrichen."""
    out = []
    for i in range(anzahl):
        x = x0 + i * 1.1
        r = {'art': 'vieleck', 'punkte': [[x, 0], [x + 0.9, 0], [x + 0.9, 10], [x, 10]], 'farbe': farbe, 'fuellung': 0.28, 'dicke': 3}
        out.append(r)
        for k in range(1, 10):
            out.append({'art': 'strecke', 'von': [x, k], 'bis': [x + 0.9, k], 'farbe': farbe, 'dicke': 1.5})
    if ein is not None:
        for o in out:
            o['ein'] = ein
    return out


def einer(x, anzahl, farbe, ein=None):
    out = [{'art': 'vieleck', 'punkte': [[x, k * 1.0], [x + 0.9, k * 1.0], [x + 0.9, k * 1.0 + 0.9], [x, k * 1.0 + 0.9]],
            'farbe': farbe, 'fuellung': 0.28, 'dicke': 3} for k in range(anzahl)]
    if ein is not None:
        for o in out:
            o['ein'] = ein
    return out


def zbild(zweite=False, ein2=None, ein=0.3):
    fig = stangen(0.5, 4, 1) + einer(5.1, 7, 2) + [{'art': 'text', 'bei': [2.8, -1.4], 'text': '47', 'farbe': 5, 'groesse': 44, 'kursiv': False}]
    if zweite:
        fig += stangen(7.3, 7, 2, ein2) + einer(15.2, 4, 1, ein2) + [{'art': 'text', 'bei': [11.6, -1.4], 'text': '74', 'farbe': 5, 'groesse': 44, 'kursiv': False, 'ein': ein2}]
    return dict(typ='graf', x=RX, y=200, breite=820, hoehe=600, abstand=0, anim='fade', ein=ein, achsen=False, raster=False,
                xbereich=[0, 18.6], ybereich=[-2.4, 11.2], figuren=fig)


clip('zahlenraetsel', 'Ansatz finden: Zahlen- und Ziffernrätsel',
     'Stellenwert 10 · z + e, vertauschte Ziffern 10 · e + z, jede Aussage eine Gleichung — linear oder, mit einem Produkt der Ziffern, quadratisch.',
     ['Zahlenrätsel', 'Ziffernrätsel', 'Stellenwert', 'Gleichungssystem', 'sys-solv', 'poly-solv'], [
         sz('Stellenwert',
            'Siebenundvierzig heisst nicht vier plus sieben. Es sind vier Zehner und sieben Einer: zehn mal vier plus sieben.',
            zbild(),
            f(r'47 = 10 \cdot \fa{4} + \fb{7}', 400, 58, ein='@Zehner')),
         sz('Die Unbekannten',
            'In einem Zahlenrätsel sind die Ziffern unbekannt. Heisst die Zehnerziffer z und die Einerziffer e, dann ist die Zahl '
            'zehn mal z plus e. Die Zehnerziffer ist eine Ziffer von eins bis neun, die Einerziffer von null bis neun.',
            zbild(ein=0.05),
            tx(r'@\fa{z}@: Zehnerziffer, @\fb{e}@: Einerziffer', 260, 42, ein='@Zehnerziffer'),
            f(r'\text{Zahl} = 10 \cdot \fa{z} + \fb{e}', 370, 52, ein='@zehn'),
            f(r'z \in \{1;\ 2;\ \ldots;\ 9\} \qquad e \in \{0;\ 1;\ \ldots;\ 9\}', 480, 36, ein='@eins'),
            n('nicht @z \\cdot e@ — das wäre das Produkt der Ziffern', 600, 'rot', 38, ein=8)),
         sz('Vertauschen',
            'Vertauscht man die Ziffern, entstehen sieben Zehner und vier Einer: vierundsiebzig, allgemein zehn mal e plus z. '
            'Die Differenz ist siebenundzwanzig, also neun mal Klammer sieben minus vier. Bei jeder zweistelligen Zahl ist sie '
            'ein Vielfaches von neun.',
            zbild(True, '@Ziffern+0.3', ein=0.05),
            f(r'74 = 10 \cdot \fb{7} + \fa{4}', 260, 48, ein='@Zehner'),
            f(r'\text{vertauscht} = 10 \cdot \fb{e} + \fa{z}', 360, 48, ein='@allgemein'),
            f(r'74 - 47 = 27 = 9 \cdot (7 - 4)', 470, 44, ein='@Differenz'),
            n('Die Differenz ist immer ein Vielfaches von 9.', 580, 'blau', 38, ein='@Vielfaches')),
         sz('Übersetzen',
            'Jede Aussage des Textes wird eine Gleichung. Dabei zählt jedes Wort: um drei grösser heisst plus drei, '
            'dreimal so gross heisst mal drei. Die Quersumme ist z plus e. Und aufeinanderfolgende Zahlen heissen n, '
            'n plus eins, n plus zwei: Dafür genügt eine Unbekannte.',
            titel('Jede Aussage eine Gleichung', 250, 66),
            f(r'\text{um 3 grösser als } a: \quad a + 3', 380, 44, ein='@grösser'),
            f(r'\text{3-mal so gross wie } a: \quad 3 \cdot a', 470, 44, ein='@dreimal'),
            f(r'\text{Quersumme}: \quad z + e', 560, 44, ein='@Quersumme'),
            f(r'\text{aufeinanderfolgend}: \quad n,\ \ n + 1,\ \ n + 2', 650, 44, ein='@aufeinanderfolgende'),
            n('Kontrolle mit einer Zahl: Bei @a = 2@ heisst «um 3 grösser» 5.', 770, 'rot', 38, ein='@Unbekannte')),
         sz('Ein System',
            'Ein Beispiel von der Themenseite: Quersumme neun, und vertauscht wird die Zahl um fünfundvierzig kleiner. '
            'Zwei Aussagen, zwei Gleichungen. Geordnet für den Rechner: z plus e gleich neun, und neun z minus neun e gleich '
            'fünfundvierzig. sys-solv liefert z gleich sieben und e gleich zwei: Die Zahl heisst zweiundsiebzig.',
            tx('Quersumme 9; vertauscht um 45 kleiner.', 220, 40, ein=0.3),
            f(r'\begin{cases} z + e = 9 \\ 10 \cdot e + z = 10 \cdot z + e - 45 \end{cases}', 310, 44, ein='@Aussagen'),
            f(r'\begin{cases} z + e = 9 \\ 9 \cdot z - 9 \cdot e = 45 \end{cases}', 520, 44, ein='@Geordnet'),
            rechner(['(1)x+(1)y=9', '(9)x-(9)y=45'], ['enter'], 220, '@Rechner', RX, 640),
            rechner(['x=7', ''], ['enter'], 560, '@liefert', RX, 400),
            rechner(['y=2', ''], ['enter'], 560, '@liefert+0.8', RX + 420, 400),
            f(r'\text{Zahl } \fc{72}', 760, 50, ein='@zweiundsiebzig', x=RX),
            n('Der Rechner nennt die Unbekannten @x@ und @y@:|hier @x = z@, @y = e@.', 760, 'blau', 36, ein='@liefert+1.5')),
         sz('Quadratisch',
            'Heisst die zweite Aussage: Das Produkt der Ziffern ist vierzehn, dann steht z mal e gleich vierzehn. '
            'Setzt man e gleich neun minus z ein, entsteht eine quadratische Gleichung. In Grundform: z Quadrat minus neun z plus '
            'vierzehn gleich null. poly-solv liefert sieben und zwei. Beide sind Ziffern: Es gibt zwei Zahlen, zweiundsiebzig und '
            'siebenundzwanzig.',
            tx('Quersumme 9; Produkt der Ziffern 14.', 220, 40, ein=0.3),
            f(r'\begin{cases} z + e = 9 \\ z \cdot e = 14 \end{cases}', 310, 44, ein='@mal'),
            f(r'z \cdot (9 - z) = 14', 520, 44, ein='@Setzt'),
            f(r'z^2 - 9 \cdot z + 14 = 0', 610, 44, ein='@Grundform'),
            rechner(['x1=7', ''], ['enter'], 220, '@liefert', RX, 400),
            rechner(['x2=2', ''], ['enter'], 220, '@liefert+0.8', RX + 420, 400),
            f(r'\text{Zahlen } \fc{72} \text{ und } \fc{27}', 460, 50, ein='@zwei#3', x=RX),
            n('Ein Produkt der Unbekannten macht|das System quadratisch.', 740, 'rot', 40, ein='@Beide')),
         sz('Merke',
            'Zum Mitnehmen: Die Zahl ist zehn z plus e, vertauscht zehn e plus z. Jede Aussage des Textes wird eine Gleichung. '
            'Ein Produkt der Unbekannten macht das System quadratisch.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'\text{Zahl} = 10 \cdot z + e \qquad \text{vertauscht} = 10 \cdot e + z', 390, 46, ein=1.2),
            n('jede Aussage eine Gleichung|Produkt der Unbekannten: quadratisch', 500, 'blau', 46, ein='@Aussage')),
         JETZT_DU,
     ], folge=1)

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle, eine Unbekannte
DK1 = r'@\fa{n}@: kleinste der drei Zahlen'
kontrolle('kontrolle-zahlen-1', 'Ansatz finden: Zahlenrätsel mit einer Unbekannten',
          'Zwei Rätsel Schritt für Schritt: aufeinanderfolgende Zahlen (linear, von Hand) und die Summe zweier Quadrate (quadratisch, mit poly-solv).',
          ['Zahlenrätsel', 'lineare Gleichung', 'quadratische Gleichung', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Zahlenrätsel',
         text='Drei aufeinanderfolgende natürliche|Zahlen haben zusammen die Summe 132.|Wie heissen die drei Zahlen?',
         spr='Drei aufeinanderfolgende natürliche Zahlen haben zusammen die Summe hundertzweiunddreissig. Wie heissen die drei Zahlen?',
         schritte=[
             dict(frage=dict(text='Mit einer Unbekannten: Wofür steht n?', sprich='Mit einer Unbekannten: Wofür steht n?',
                             opt=['n: kleinste der drei Zahlen', 'n: Summe der drei Zahlen', 'n, m, k: die drei Zahlen'],
                             rueck={1: 'Die Summe ist gegeben: 132. Unbekannt sind die Zahlen selbst.',
                                    2: 'Das sind drei Unbekannte. Wie schreibst du die beiden anderen Zahlen mit der kleinsten?'},
                             rueck_sprich={1: 'Die Summe ist gegeben: hundertzweiunddreissig. Unbekannt sind die Zahlen selbst.',
                                           2: 'Das sind drei Unbekannte. Wie schreibst du die beiden anderen Zahlen mit der kleinsten?'}),
                  spr='n ist die kleinste der drei Zahlen. Die nächsten sind n plus eins und n plus zwei. So genügt eine Unbekannte.',
                  el=[tx(DK1, 520, 40, x=RX, ein='@kleinste'),
                      tx(r'die anderen: @n + 1@ und @n + 2@', 600, 40, x=RX, ein='@nächsten'),
                      n('aufeinanderfolgend: jede um 1 grösser', 700, 'blau', 38, x=RX, ein='@genügt')]),
             dict(gegeben=[G_text(DK1), G_text(r'die anderen: @n + 1@, @n + 2@')],
                  frage=dict(text='Welche Gleichung übersetzt den Text?', sprich='Welche Gleichung übersetzt den Text?',
                             opt=['n + (n + 1) + (n + 2) = 132', 'n + 2·n + 3·n = 132', '3·n = 132'],
                             rueck={1: 'Aufeinanderfolgend heisst: jede Zahl um eins grösser, nicht doppelt oder dreimal so gross.',
                                    2: 'Dann wären alle drei Zahlen gleich gross. Wie heissen die beiden anderen?'}),
                  spr='Zusammen ergeben die drei Zahlen hundertzweiunddreissig: n plus Klammer n plus eins plus Klammer n plus zwei '
                      'gleich hundertzweiunddreissig.',
                  el=[f(r'n + (n + 1) + (n + 2) = 132', 520, 44, x=RX, ein='@Zusammen'),
                      n('Summe der drei Zahlen', 610, 'blau', 38, x=RX, ein='@Klammer')]),
             dict(gegeben=[G_text(DK1), G_formel(r'n + (n + 1) + (n + 2) = 132')],
                  frage=dict(text='Zusammengefasst und geordnet: Wie heisst die Gleichung?',
                             sprich='Zusammengefasst und geordnet: Wie heisst die Gleichung?',
                             opt=['3·n = 129', '3·n = 135', 'n = 129'],
                             rueck={1: 'Prüfe das Vorzeichen: Wie bringst du das + 3 von links weg?',
                                    2: 'Wie viele n stehen links?'},
                             rueck_sprich={1: 'Prüfe das Vorzeichen: Wie bringst du das plus drei von links weg?'}),
                  spr='Zusammengefasst: drei n plus drei gleich hundertzweiunddreissig. Minus drei auf beiden Seiten: '
                      'drei n gleich hundertneunundzwanzig.',
                  el=[f(r'3 \cdot n + 3 = 132 \qquad \fb{\mid -3}', 520, 44, x=RX, ein='@Zusammengefasst'),
                      f(r'3 \cdot n = 129', 610, 44, x=RX, ein='@beiden')]),
             dict(gegeben=[G_text(DK1), G_formel(r'3 \cdot n = 129')],
                  frage=dict(text='Welcher Typ ist das, und wie löst du?', sprich='Welcher Typ ist das, und wie löst du?',
                             opt=['linear: von Hand durch 3 teilen', 'quadratisch: mit poly-solv', 'System: mit sys-solv'],
                             rueck={1: 'Kommt n im Quadrat vor?', 2: 'Wie viele Unbekannte und wie viele Gleichungen hast du?'},
                             rueck_sprich={1: 'Kommt n im Quadrat vor?'}),
                  spr='Eine Unbekannte und kein Quadrat: Die Gleichung ist linear. Von Hand durch drei teilen: n gleich dreiundvierzig.',
                  el=[n('linear: von Hand lösen', 520, 'blau', 40, x=RX, ein='@linear'),
                      f(r'n = 129 : 3 = \fc{43}', 610, 48, x=RX, ein='@teilen')]),
             dict(gegeben=[G_text(DK1), G_formel(r'n = 43')],
                  frage=dict(text='Wie lautet die Antwort auf die Frage im Text?', sprich='Wie lautet die Antwort auf die Frage im Text?',
                             opt=['Die Zahlen sind 43, 44 und 45.', 'Die Zahl ist 43.', 'n = 43'],
                             rueck={1: 'Gefragt sind alle drei Zahlen.', 2: 'Ein Antwortsatz beantwortet die Frage des Textes in Worten.'}),
                  spr='Gefragt sind alle drei Zahlen: dreiundvierzig, vierundvierzig und fünfundvierzig. Probe am Text: '
                      'Sie folgen aufeinander, und zusammen sind es hundertzweiunddreissig.',
                  el=[tx(r'Die Zahlen sind @\fc{43}@, @\fc{44}@ und @\fc{45}@.', 520, 40, x=RX, ein='@Gefragt'),
                      f(r'43 + 44 + 45 = 132 \;\checkmark', 610, 44, x=RX, ein='@Probe')]),
         ]),
    dict(nr=2, kurz='Zahlenrätsel',
         text='Die Summe der Quadrate zweier|aufeinanderfolgender natürlicher|Zahlen ist 113. Wie heissen die Zahlen?',
         spr='Die Summe der Quadrate zweier aufeinanderfolgender natürlicher Zahlen ist hundertdreizehn. Wie heissen die Zahlen?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration passt?', sprich='Welche Deklaration passt?',
                             opt=['n: kleinere Zahl, n + 1: grössere', 'n: Summe der beiden Zahlen', 'n: Quadrat der kleineren Zahl'],
                             rueck={1: 'Die Summe der Zahlen steht nicht im Text. Gesucht sind die Zahlen selbst.',
                                    2: 'Dann lässt sich die grössere Zahl nicht einfach schreiben. Deklariere die Zahl selbst.'}),
                  spr='n ist die kleinere Zahl, die grössere ist n plus eins. Beide sind natürliche Zahlen.',
                  el=[tx(r'@\fa{n}@: kleinere Zahl, @n + 1@: grössere', 520, 40, x=RX, ein='@kleinere'),
                      n('n ist eine natürliche Zahl.', 610, 'blau', 38, x=RX, ein='@natürliche')]),
             dict(gegeben=[G_text(r'@\fa{n}@: kleinere Zahl, @n + 1@: grössere')],
                  frage=dict(text='Welche Gleichung stimmt?', sprich='Welche Gleichung stimmt?',
                             opt=['n² + (n + 1)² = 113', '(n + n + 1)² = 113', 'n² + n² + 1 = 113'],
                             rueck={1: 'Das ist das Quadrat der Summe. Gefragt ist die Summe der Quadrate.',
                                    2: 'Prüfe (n + 1)² mit n = 2: 3² = 9, aber 2² + 1 = 5.'},
                             rueck_sprich={2: 'Prüfe n plus eins im Quadrat mit n gleich zwei: drei im Quadrat ist neun, aber zwei im Quadrat plus eins ist fünf.'}),
                  spr='Erst quadrieren, dann addieren: n Quadrat plus Klammer n plus eins im Quadrat gleich hundertdreizehn.',
                  el=[f(r'n^2 + (n + 1)^2 = 113', 520, 48, x=RX, ein='@quadrieren')]),
             dict(gegeben=[G_text(r'@\fa{n}@: kleinere Zahl, @n + 1@: grössere'), G_formel(r'n^2 + (n + 1)^2 = 113')],
                  frage=dict(text='In Grundform a·n² + b·n + c = 0: Was tippst du in poly-solv?',
                             sprich='In Grundform a n Quadrat plus b n plus c gleich null: Was tippst du in poly-solv ein?',
                             opt=['a = 2, b = 2, c = −112', 'a = 2, b = 1, c = −112', 'a = 2, b = 2, c = 112'],
                             rueck={1: '(n + 1)² hat ein Mittelglied. Welches?', 2: 'Die 113 kommt nach links. Welches Vorzeichen hat sie dort?'},
                             rueck_sprich={1: 'Klammer n plus eins im Quadrat hat ein Mittelglied. Welches?',
                                           2: 'Die hundertdreizehn kommt nach links. Welches Vorzeichen hat sie dort?'}),
                  spr='Das Binom auflösen: n Quadrat plus zwei n plus eins. Zusammen zwei n Quadrat plus zwei n plus eins gleich '
                      'hundertdreizehn. Minus hundertdreizehn: zwei n Quadrat plus zwei n minus hundertzwölf gleich null. '
                      'In poly-solv: a gleich zwei, b gleich zwei, c gleich minus hundertzwölf.',
                  el=[f(r'n^2 + n^2 + 2 \cdot n + 1 = 113', 520, 42, x=RX, ein='@Binom'),
                      f(r'2 \cdot n^2 + 2 \cdot n - 112 = 0', 610, 46, x=RX, ein='@hundertzwölf'),
                      ] + poly_eingabe(2, 2, -112, 640, '@poly')),
             dict(gegeben=[G_text(r'@\fa{n}@: kleinere Zahl, @n + 1@: grössere'), G_formel(r'2 \cdot n^2 + 2 \cdot n - 112 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 7 und x2 = −8. Was gilt für n?',
                             sprich='poly-solv zeigt x eins gleich sieben und x zwei gleich minus acht. Was gilt für n?',
                             opt=['n = 7', 'n = 7 oder n = −8', 'n = −8'],
                             rueck={1: 'Gesucht sind natürliche Zahlen. Ist −8 eine?', 2: 'Ist −8 eine natürliche Zahl?'},
                             rueck_sprich={1: 'Gesucht sind natürliche Zahlen. Ist minus acht eine?', 2: 'Ist minus acht eine natürliche Zahl?'}),
                  spr='Der Rechner liefert beide Lösungen der Gleichung. Zum Text passt nur n gleich sieben. '
                      'Minus acht ist keine natürliche Zahl: Diese Lösung fällt weg.',
                  el=ergebnis('x1=7', 'x2=⁻8') + [
                      f(r'n = \fc{7}', 740, 48, x=RX, ein='@passt'),
                      tx(r'@\fd{n = -8}@: keine natürliche Zahl', 830, 36, x=RX, ein='@keine')]),
             dict(gegeben=[G_text(r'@\fa{n}@: kleinere Zahl, @n + 1@: grössere'), G_formel(r'n = 7')],
                  frage=dict(text='Welche Probe prüft den Text?', sprich='Welche Probe prüft den Text?',
                             opt=['7² + 8² = 49 + 64 = 113', '2·7² + 2·7 − 112 = 0', '7 + 8 = 15'],
                             rueck={1: 'Das prüft nur die eigene Gleichung. Ein Fehler im Ansatz bliebe unentdeckt.',
                                    2: 'Im Text geht es um die Summe der Quadrate.'}),
                  spr='Die Probe gehört an den Text: sieben im Quadrat plus acht im Quadrat, neunundvierzig plus vierundsechzig, '
                      'gibt hundertdreizehn. Die Zahlen sind sieben und acht.',
                  el=[f(r'7^2 + 8^2 = 49 + 64 = 113 \;\checkmark', 520, 44, x=RX, ein='@Probe'),
                      tx(r'Die Zahlen sind @\fc{7}@ und @\fc{8}@.', 610, 40, x=RX, ein='@Zahlen')]),
         ]),
], merke('Zum Mitnehmen: Mit einer Unbekannten schreibst du die anderen Grössen als Term, etwa n plus eins. '
         'Eine lineare Gleichung löst du von Hand. Kommt die Unbekannte im Quadrat vor, bringst du die Gleichung auf die Grundform '
         'und löst sie mit poly-solv. Jede Lösung prüfst du am Text.',
         'die anderen Grössen als Term: @n + 1@, @n + 2@|linear: von Hand lösen|quadratisch: Grundform, poly-solv|jede Lösung am Text prüfen'),
   folge=2)

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle, zwei Unbekannte
DZ = r'@\fa{z}@: Zehnerziffer, @\fb{e}@: Einerziffer'
kontrolle('kontrolle-zahlen-2', 'Ansatz finden: Zahlenrätsel mit zwei Unbekannten',
          'Zwei Ziffernrätsel Schritt für Schritt: vertauschte Ziffern (lineares System, sys-solv) und die Zahl mal ihre Quersumme (quadratisches System, poly-solv).',
          ['Ziffernrätsel', 'lineares Gleichungssystem', 'quadratisches Gleichungssystem', 'sys-solv', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Ziffernrätsel',
         text='Eine zweistellige Zahl hat die|Quersumme 12. Vertauscht man ihre|Ziffern, wird die Zahl um 36 grösser.|Wie heisst die Zahl?',
         spr='Eine zweistellige Zahl hat die Quersumme zwölf. Vertauscht man ihre Ziffern, wird die Zahl um sechsunddreissig grösser. '
             'Wie heisst die Zahl?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration führt zum Ziel?', sprich='Welche Deklaration führt zum Ziel?',
                             opt=['z: Zehnerziffer, e: Einerziffer', 'x: die Zahl, y: die vertauschte', 'z, e: Ziffern; Zahl = z · e'],
                             rueck={1: 'Damit lässt sich die Quersumme nicht schreiben. Was steckt in einer zweistelligen Zahl?',
                                    2: 'z · e ist das Produkt der Ziffern. Wie setzt sich die Zahl aus ihren Ziffern zusammen?'},
                             rueck_sprich={1: 'Damit lässt sich die Quersumme nicht schreiben. Was steckt in einer zweistelligen Zahl?',
                                           2: 'z mal e ist das Produkt der Ziffern. Wie setzt sich die Zahl aus ihren Ziffern zusammen?'}),
                  spr='Unbekannt sind die beiden Ziffern: z ist die Zehnerziffer, e die Einerziffer. Die Zahl ist zehn z plus e, '
                      'vertauscht zehn e plus z.',
                  el=[tx(DZ, 520, 40, x=RX, ein='@Ziffern'),
                      f(r'\text{Zahl } 10 \cdot z + e \qquad \text{vertauscht } 10 \cdot e + z', 610, 36, x=RX, ein='@Zahl')]),
             dict(gegeben=[G_text(DZ), G_formel(r'\text{Zahl } 10 \cdot z + e', 36)],
                  frage=dict(text='«Vertauscht um 36 grösser»: Welche Gleichung?',
                             sprich='Vertauscht um sechsunddreissig grösser: Welche Gleichung passt?',
                             opt=['10·e + z = 10·z + e + 36', '10·e + z + 36 = 10·z + e', 'e + z = z + e + 36'],
                             rueck={1: 'Die vertauschte Zahl ist die grössere. Zu welcher Seite gehört die 36?',
                                    2: 'Der Stellenwert fehlt: Die Zehnerziffer zählt zehnfach.'},
                             rueck_sprich={1: 'Die vertauschte Zahl ist die grössere. Zu welcher Seite gehört die sechsunddreissig?'}),
                  spr='Zwei Aussagen, zwei Gleichungen. Die Quersumme: z plus e gleich zwölf. Die vertauschte Zahl ist um '
                      'sechsunddreissig grösser: zehn e plus z gleich zehn z plus e plus sechsunddreissig.',
                  el=[f(r'\begin{cases} z + e = 12 \\ 10 \cdot e + z = 10 \cdot z + e + 36 \end{cases}', 520, 40, x=RX, ein='@Quersumme'),
                      n('Die 36 kommt zur kleineren Zahl.', 700, 'blau', 38, x=RX, ein='@vertauschte')]),
             dict(gegeben=[G_text(DZ), G_formel(r'\begin{cases} z + e = 12 \\ 10 \cdot e + z = 10 \cdot z + e + 36 \end{cases}', 38, 120)],
                  frage=dict(text='Zweite Gleichung als a·z + b·e = c: Was tippst du ein?',
                             sprich='Die zweite Gleichung in der Form a z plus b e gleich c: Was tippst du ein?',
                             opt=['9·z − 9·e = −36', '9·z − 9·e = 36', '11·z + 11·e = 36'],
                             rueck={1: 'Prüfe das Vorzeichen der 36: Auf welcher Seite steht sie, wenn z und e links stehen?',
                                    2: 'Wer einen Term auf die andere Seite bringt, wechselt sein Vorzeichen.'},
                             rueck_sprich={1: 'Prüfe das Vorzeichen der sechsunddreissig: Auf welcher Seite steht sie, wenn z und e links stehen?'}),
                  spr='Ordnen: alle Terme mit z und e nach links, die Zahl nach rechts. Aus der zweiten Gleichung wird neun z minus '
                      'neun e gleich minus sechsunddreissig. In sys-solv: erste Zeile eins, eins, zwölf, zweite Zeile neun, minus neun, '
                      'minus sechsunddreissig.',
                  el=[f(r'\begin{cases} z + e = 12 \\ 9 \cdot z - 9 \cdot e = -36 \end{cases}', 520, 44, x=RX, ein='@Ordnen'),
                      n('gleichwertig: @-9 \\cdot z + 9 \\cdot e = 36@', 690, 'blau', 36, x=RX, ein='@zweiten'),
                      ] + sys_eingabe((1, 1, 12), (9, -9, -36), 640, '@sys')),
             dict(gegeben=[G_text(DZ), G_formel(r'\begin{cases} z + e = 12 \\ 9 \cdot z - 9 \cdot e = -36 \end{cases}', 40, 120)],
                  frage=dict(text='sys-solv zeigt x = 4 und y = 8. Wie heisst die Zahl?',
                             sprich='sys-solv zeigt x gleich vier und y gleich acht. Wie heisst die Zahl?',
                             opt=['48', '84', '32'],
                             rueck={1: 'In der ersten Spalte stand z. Welche Ziffer ist also x?',
                                    2: 'Die Zahl ist nicht das Produkt ihrer Ziffern.'}),
                  spr='In der Eingabe stand z an der Stelle von x und e an der Stelle von y. Also z gleich vier und e gleich acht: '
                      'Die Zahl heisst achtundvierzig. Beides sind Ziffern, das passt.',
                  el=ergebnis('x=4', 'y=8') + [
                      f(r'z = \fc{4},\ e = \fc{8}', 740, 46, x=RX, ein='@Also'),
                      tx(r'Zahl @\fc{48}@', 830, 40, x=RX, ein='@heisst')]),
             dict(gegeben=[G_text(DZ), G_formel(r'z = 4,\ e = 8: \ 48')],
                  frage=dict(text='Welche Probe prüft beide Aussagen?', sprich='Welche Probe prüft beide Aussagen des Textes?',
                             opt=['4 + 8 = 12 und 84 − 48 = 36', '4 + 8 = 12 und 9·4 − 9·8 = −36', '48 − 36 = 12'],
                             rueck={1: 'Die zweite Rechnung prüft die eigene Gleichung, nicht den Text.',
                                    2: 'Was sagt der Text über die vertauschte Zahl?'}),
                  spr='Probe am Text: Die Quersumme ist vier plus acht gleich zwölf. Vertauscht entsteht vierundachtzig, und '
                      'vierundachtzig minus achtundvierzig ist sechsunddreissig. Die Zahl heisst achtundvierzig.',
                  el=[f(r'4 + 8 = 12 \;\checkmark', 520, 44, x=RX, ein='@Quersumme'),
                      f(r'84 - 48 = 36 \;\checkmark', 600, 44, x=RX, ein='@Vertauscht'),
                      tx(r'Die Zahl heisst @\fc{48}@.', 690, 40, x=RX, ein='@heisst')]),
         ]),
    dict(nr=2, kurz='Ziffernrätsel',
         text='Bei einer zweistelligen Zahl ist die|Zehnerziffer um 2 grösser als die|Einerziffer. Die Zahl mal ihre Quersumme|ergibt 640. Wie heisst die Zahl?',
         spr='Bei einer zweistelligen Zahl ist die Zehnerziffer um zwei grösser als die Einerziffer. Die Zahl mal ihre Quersumme '
             'ergibt sechshundertvierzig. Wie heisst die Zahl?',
         schritte=[
             dict(frage=dict(text='z: Zehnerziffer, e: Einerziffer. Welche Werte sind möglich?',
                             sprich='z ist die Zehnerziffer, e die Einerziffer. Welche Werte sind möglich?',
                             opt=['z von 1 bis 9, e von 0 bis 9', 'z und e: beliebige Zahlen', 'z und e von 1 bis 9'],
                             rueck={1: 'Ziffern sind ganze Zahlen von 0 bis 9.', 2: 'Kann die Einerziffer 0 sein? Denk an 40.'},
                             rueck_sprich={1: 'Ziffern sind ganze Zahlen von null bis neun.', 2: 'Kann die Einerziffer null sein? Denk an vierzig.'}),
                  spr='Wieder sind die Ziffern unbekannt. Sie sind ganze Zahlen von null bis neun, und die Zehnerziffer ist nicht null. '
                      'Das brauchst du am Schluss, um Lösungen zu prüfen.',
                  el=[tx(DZ, 520, 40, x=RX, ein='@Ziffern'),
                      f(r'z \in \{1;\ 2;\ \ldots;\ 9\},\quad e \in \{0;\ 1;\ \ldots;\ 9\}', 610, 36, x=RX, ein='@ganze')]),
             dict(gegeben=[G_text(DZ), G_formel(r'z \in \{1;\ \ldots;\ 9\},\ e \in \{0;\ \ldots;\ 9\}', 36)],
                  frage=dict(text='Welches System übersetzt den Text?', sprich='Welches System übersetzt den Text?',
                             opt=['z = e + 2 und (10·z + e)·(z + e) = 640', 'z + 2 = e und (10·z + e)·(z + e) = 640',
                                  'z = e + 2 und (10·z + e) + (z + e) = 640'],
                             rueck={1: 'Welche Ziffer ist die grössere? Die 2 kommt zur kleineren.',
                                    2: '«Die Zahl mal ihre Quersumme» heisst: mal, nicht plus.'},
                             rueck_sprich={1: 'Welche Ziffer ist die grössere? Die Zwei kommt zur kleineren.',
                                           2: 'Die Zahl mal ihre Quersumme heisst: mal, nicht plus.'}),
                  spr='Erste Aussage: Die Zehnerziffer ist um zwei grösser, z gleich e plus zwei. Zweite Aussage: die Zahl mal ihre '
                      'Quersumme, Klammer zehn z plus e mal Klammer z plus e gleich sechshundertvierzig. Ein Produkt der Unbekannten: '
                      'Das System ist quadratisch.',
                  el=[f(r'\begin{cases} z = e + 2 \\ (10 \cdot z + e) \cdot (z + e) = 640 \end{cases}', 520, 40, x=RX, ein='@Erste'),
                      n('Produkt der Unbekannten: quadratisch', 700, 'rot', 38, x=RX, ein='@Produkt')]),
             dict(gegeben=[G_text(DZ), G_formel(r'\begin{cases} z = e + 2 \\ (10 \cdot z + e) \cdot (z + e) = 640 \end{cases}', 38, 120)],
                  frage=dict(text='z = e + 2 eingesetzt: Welche Grundform entsteht?',
                             sprich='z gleich e plus zwei eingesetzt und geordnet: Welche Grundform entsteht?',
                             opt=['22·e² + 62·e − 600 = 0', '22·e² + 42·e − 600 = 0', '22·e² + 62·e + 40 = 0'],
                             rueck={1: 'Rechne das gemischte Glied nach: (11·e + 20)·(2·e + 2).', 2: 'Die 640 muss auch nach links.'},
                             rueck_sprich={1: 'Rechne das gemischte Glied nach: elf e plus zwanzig, mal zwei e plus zwei.',
                                           2: 'Die sechshundertvierzig muss auch nach links.'}),
                  spr='Für z setzt du e plus zwei ein. Die Zahl wird elf e plus zwanzig, die Quersumme zwei e plus zwei. '
                      'Ausmultipliziert: zweiundzwanzig e Quadrat plus zweiundsechzig e plus vierzig gleich sechshundertvierzig. '
                      'Minus sechshundertvierzig gibt die Grundform für poly-solv.',
                  el=[f(r'(11 \cdot e + 20) \cdot (2 \cdot e + 2) = 640', 520, 40, x=RX, ein='@Zahl'),
                      f(r'22 \cdot e^2 + 62 \cdot e + 40 = 640', 600, 40, x=RX, ein='@Ausmultipliziert'),
                      f(r'22 \cdot e^2 + 62 \cdot e - 600 = 0', 680, 44, x=RX, ein='@Grundform'),
                      ] + poly_eingabe(22, 62, -600, 640, '@poly')),
             dict(gegeben=[G_text(DZ), G_formel(r'22 \cdot e^2 + 62 \cdot e - 600 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 4 und x2 = −75/11. Was gilt?',
                             sprich='poly-solv zeigt x eins gleich vier und x zwei gleich minus fünfundsiebzig Elftel. Was gilt?',
                             opt=['Nur e = 4 passt.', 'Beide Lösungen passen.', 'Keine Lösung passt.'],
                             rueck={1: 'Ist −75/11 eine Ziffer?', 2: 'Ist 4 eine Ziffer? Prüfe die möglichen Werte.'},
                             rueck_sprich={1: 'Ist minus fünfundsiebzig Elftel eine Ziffer?', 2: 'Ist vier eine Ziffer? Prüfe die möglichen Werte.'}),
                  spr='Minus fünfundsiebzig Elftel ist keine Ziffer, diese Lösung fällt weg. Es bleibt e gleich vier, und damit '
                      'z gleich vier plus zwei gleich sechs.',
                  el=ergebnis('x1=4', 'x2=⁻[75|11]') + [
                      tx(r'@\fd{e = -\tfrac{75}{11}}@: keine Ziffer', 760, 36, x=RX, ein='@keine'),
                      f(r'e = \fc{4},\ \ z = 4 + 2 = \fc{6}', 850, 44, x=RX, ein='@bleibt')]),
             dict(gegeben=[G_text(DZ), G_formel(r'e = 4,\ z = 6')],
                  frage=dict(text='Wie heisst die gesuchte Zahl?', sprich='Wie heisst die gesuchte Zahl?',
                             opt=['64', '46', '4'],
                             rueck={1: 'Die Zehnerziffer steht vorn. Welche der beiden ist es?', 2: '4 ist erst die Einerziffer. Wie heisst die Zehnerziffer?'},
                             rueck_sprich={2: 'Vier ist erst die Einerziffer. Wie heisst die Zehnerziffer?'}),
                  spr='Zehnerziffer sechs, Einerziffer vier: Die Zahl heisst vierundsechzig. Probe am Text: Sechs ist um zwei grösser '
                      'als vier, und vierundsechzig mal die Quersumme zehn gibt sechshundertvierzig.',
                  el=[tx(r'Die Zahl heisst @\fc{64}@.', 520, 40, x=RX, ein='@Zehnerziffer'),
                      f(r'6 = 4 + 2 \;\checkmark \qquad 64 \cdot 10 = 640 \;\checkmark', 610, 40, x=RX, ein='@Probe')]),
         ]),
], merke('Zum Mitnehmen: Bei Ziffernrätseln sind die Ziffern die Unbekannten, die Zahl ist zehn z plus e. Ein lineares System '
         'ordnest du zeilenweise und löst es mit sys-solv. Ein Produkt der Unbekannten macht das System quadratisch: einsetzen, '
         'Grundform, poly-solv. Lösungen, die keine Ziffern sind, fallen weg.',
         'lineares System: ordnen, sys-solv|Produkt: einsetzen, Grundform, poly-solv|Lösungen müssen Ziffern sein'),
   folge=3)


# ════════════════════════════════════════════════ Kapitel 2 · Einführung
def becher(x0, menge, stoff, farbe, text, ein=0.3, ein_menge=None, ein_stoff=None, stoff_farbe=None):
    """Ein Gefäss (Umriss bis 31 kg), Füllung bis `menge` (hell), Stoffanteil unten (kräftig)."""
    fig = [{'art': 'vieleck', 'punkte': [[x0, 0], [x0 + 8, 0], [x0 + 8, 31], [x0, 31]], 'farbe': 5, 'dicke': 3, 'fuellung': 0},
           {'art': 'text', 'bei': [x0 + 4, -2.6], 'text': text, 'farbe': 5, 'groesse': 34, 'kursiv': False}]
    if menge:
        m = {'art': 'vieleck', 'punkte': [[x0, 0], [x0 + 8, 0], [x0 + 8, menge], [x0, menge]], 'farbe': farbe, 'dicke': 2, 'fuellung': 0.18}
        if ein_menge is not None:
            m['ein'] = ein_menge
        fig.append(m)
    if stoff:
        s = {'art': 'vieleck', 'punkte': [[x0, 0], [x0 + 8, 0], [x0 + 8, stoff], [x0, stoff]], 'farbe': stoff_farbe or farbe,
             'dicke': 2, 'fuellung': 0.6}
        if ein_stoff is not None:
            s['ein'] = ein_stoff
        fig.append(s)
    return fig


def mischbild(menge=False, stoff=False, ein=0.05, ein_menge=None, ein_stoff=None, mischung=True, ein_misch=None):
    fig = (becher(1, 20 if menge else 0, 4 if stoff else 0, 1, 'A: 20 %', ein_menge=ein_menge, ein_stoff=ein_stoff)
           + becher(12.8, 10 if menge else 0, 5 if stoff else 0, 2, 'B: 50 %', ein_menge=ein_menge, ein_stoff=ein_stoff))
    if mischung:
        mb = becher(24.6, 30 if menge else 0, 9 if stoff else 0, 3, 'Mischung: 30 %', ein_menge=ein_misch or ein_menge,
                    ein_stoff=ein_stoff)
        fig += mb
    texte = []
    if menge:
        texte += [{'art': 'text', 'bei': [5, 21.6], 'text': 'x kg', 'farbe': 1, 'groesse': 32, 'ein': ein_menge or 0.05},
                  {'art': 'text', 'bei': [16.8, 11.6], 'text': 'y kg', 'farbe': 2, 'groesse': 32, 'ein': ein_menge or 0.05}]
        if mischung:
            texte.append({'art': 'text', 'bei': [28.6, 32.4], 'text': '30 kg', 'farbe': 3, 'groesse': 32, 'kursiv': False,
                          'ein': ein_misch or ein_menge or 0.05})
    if stoff:
        texte += [{'art': 'text', 'bei': [5, 1.4], 'text': '0.2·x', 'farbe': 5, 'groesse': 28, 'ein': ein_stoff or 0.05},
                  {'art': 'text', 'bei': [16.8, 1.9], 'text': '0.5·y', 'farbe': 5, 'groesse': 28, 'ein': ein_stoff or 0.05},
                  {'art': 'text', 'bei': [28.6, 4.0], 'text': '9 kg', 'farbe': 5, 'groesse': 28, 'kursiv': False, 'ein': ein_stoff or 0.05}]
    return dict(typ='graf', x=RX, y=170, breite=800, hoehe=780, abstand=0, anim='fade', ein=ein, achsen=False, raster=False,
                xbereich=[-2.2, 36.2], ybereich=[-4.5, 34.2], figuren=fig + texte)


clip('mischen', 'Ansatz finden: Mischen',
     'Mengenbilanz und Stoffbilanz an zwei Sirupen: Menge mal Anteil ist Stoff, und Prozente addieren sich nie. Dazu Verdünnen mit Wasser und wann es quadratisch wird.',
     ['Mischungsaufgabe', 'Mengenbilanz', 'Stoffbilanz', 'Verdünnen', 'sys-solv'], [
         sz('Zwei Sorten',
            'Aus Sirup A mit zwanzig Prozent Zucker und Sirup B mit fünfzig Prozent Zucker sollen dreissig Kilogramm Sirup mit '
            'dreissig Prozent Zucker entstehen. Wie viel braucht es von jeder Sorte?',
            mischbild(ein=0.3),
            tx('Sirup A: 20 % Zucker|Sirup B: 50 % Zucker|Mischung: 30 kg mit 30 % Zucker', 260, 42, ein=0.6)),
         sz('Deklarieren',
            'Gesucht sind Mengen. x ist die Masse von Sirup A in Kilogramm, y die Masse von Sirup B. Die Prozente sind gegeben, '
            'sie gehören nicht in die Deklaration.',
            mischbild(menge=True, mischung=False, ein=0.05, ein_menge='@Masse'),
            tx(r'@\fa{x}@: Masse Sirup A in kg', 280, 44, ein='@Masse'),
            tx(r'@\fb{y}@: Masse Sirup B in kg', 360, 44, ein='@Sirup#2'),
            n('Mengen deklarieren, nicht Prozente', 480, 'rot', 40, ein='@Prozente')),
         sz('Mengenbilanz',
            'Beim Mischen addieren sich die Mengen: x plus y gleich dreissig. Gezählt werden Kilogramm Sirup, links wie rechts.',
            mischbild(menge=True, ein=0.05, ein_misch='@addieren'),
            f(r'\fa{x} + \fb{y} = 30', 300, 56, ein='@addieren'),
            n('Mengenbilanz: kg Sirup', 420, 'blau', 42, ein='@Gezählt')),
         sz('Stoffbilanz',
            'Auch der Zucker addiert sich. In x Kilogramm Sirup A stecken null Komma zwei mal x Kilogramm Zucker, in Sirup B '
            'null Komma fünf mal y. Die Mischung enthält null Komma drei mal dreissig, also neun Kilogramm Zucker. Anteil mal Menge '
            'gibt den Stoff.',
            mischbild(menge=True, stoff=True, ein=0.05, ein_stoff='@stecken'),
            f(r'0.2 \cdot \fa{x} + 0.5 \cdot \fb{y} = 0.3 \cdot 30 = 9', 300, 48, ein='@Mischung'),
            n('Stoffbilanz: kg Zucker', 410, 'blau', 42, ein='@Mischung'),
            f(r'\text{Anteil} \cdot \text{Menge} = \text{Stoff}', 520, 44, ein='@Anteil')),
         sz('Die Falle',
            'Prozente addieren sich nie. Wer rechts null Komma drei schreibt, setzt einen Anteil gleich einer Masse. '
            'Prüfe jede Gleichung: Links und rechts muss dieselbe Grösse stehen, hier Kilogramm Zucker.',
            titel('Prozente addieren sich nie', 250, 64),
            f(r'\fd{0.2 \cdot x + 0.5 \cdot y = 0.3}', 400, 48, ein='@rechts'),
            f(r'\fd{20\,\% + 50\,\% = 70\,\%}', 500, 48, ein=1.0),
            n('links und rechts dieselbe Grösse: kg Zucker', 640, 'rot', 44, ein='@Prüfe')),
         sz('Lösen',
            'Für sys-solv die Stoffbilanz mal zehn: zwei x plus fünf y gleich neunzig. Der Rechner liefert x gleich zwanzig und '
            'y gleich zehn. Probe am Text: vier plus fünf gleich neun Kilogramm Zucker, und neun durch dreissig sind dreissig Prozent.',
            f(r'\begin{cases} x + y = 30 \\ 2 \cdot x + 5 \cdot y = 90 \end{cases}', 240, 48, ein=0.5),
            rechner(['(1)x+(1)y=30', '(2)x+(5)y=90'], ['enter'], 220, '@Rechner', RX, 640),
            rechner(['x=20', ''], ['enter'], 560, '@liefert', RX, 400),
            rechner(['y=10', ''], ['enter'], 560, '@liefert+0.8', RX + 420, 400),
            f(r'0.2 \cdot 20 + 0.5 \cdot 10 = 4 + 5 = 9 \;\checkmark', 470, 42, ein='@Probe'),
            f(r'9 : 30 = 0.3 = 30\,\% \;\checkmark', 560, 42, ein='@durch')),
         sz('Verdünnen',
            'Wird mit Wasser verdünnt, ist Wasser eine Sorte mit dem Anteil null. Zwei Liter Konzentrat mit vierzig Prozent '
            'Wirkstoff sollen sechzehn Prozent haben: null Komma vier mal zwei gleich null Komma eins sechs mal Klammer zwei plus w. '
            'Eine Unbekannte, eine lineare Gleichung: w gleich drei Liter Wasser.',
            tx('2 l Konzentrat mit 40 % auf 16 % verdünnen', 240, 42, ein=0.3),
            tx(r'@\fb{w}@: Menge Wasser in l', 330, 42, ein='@Wasser'),
            f(r'0.4 \cdot 2 + 0 \cdot \fb{w} = 0.16 \cdot (2 + \fb{w})', 430, 48, ein='@null#2'),
            f(r'0.8 = 0.32 + 0.16 \cdot w \quad \Rightarrow \quad w = \fc{3}', 540, 46, ein='@lineare'),
            n('Wasser: Anteil 0', 660, 'blau', 42, ein='@Sorte')),
         sz('Quadratisch',
            'Sind Menge und Anteil beide unbekannt, steht in der Stoffbilanz ein Produkt zweier Unbekannter: Menge mal Anteil. '
            'Dann wird das System quadratisch, und am Schluss hilft poly-solv.',
            titel('Wann quadratisch?', 250, 66),
            f(r'\text{Stoff} = \fa{m} \cdot \fb{p} \qquad \text{Menge und Anteil unbekannt}', 400, 46, ein='@Produkt'),
            n('Produkt zweier Unbekannter: quadratisch', 520, 'rot', 44, ein='@quadratisch')),
         sz('Merke',
            'Zum Mitnehmen: Deklariere Mengen. Die Mengen addieren sich zur Gesamtmenge, der Stoff, Anteil mal Menge, zum Stoff der '
            'Mischung. Prozente addieren sich nie.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x + y = M \qquad p_1 \cdot x + p_2 \cdot y = p \cdot M', 390, 50, ein=1.2),
            n('Anteile als Dezimalzahl|links und rechts dieselbe Grösse', 500, 'blau', 46, ein='@Stoff')),
         JETZT_DU,
     ], folge=4)

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle, eine Unbekannte
DW = r'@\fb{w}@: Menge des Wassers in l'
DF = r'@\fa{x}@: jedes Mal abgezapfte Menge in l'
kontrolle('kontrolle-mischen-1', 'Ansatz finden: Mischen mit einer Unbekannten',
          'Zwei Mischaufgaben Schritt für Schritt: Sirup mit Wasser verdünnen (linear) und zweimal Gemisch abzapfen (quadratisch, poly-solv).',
          ['Mischungsaufgabe', 'Verdünnen', 'lineare Gleichung', 'quadratische Gleichung', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Mischen',
         text='12 l Sirup enthalten 25 % Zucker.|Wie viel Wasser muss man dazugiessen,|damit die Mischung nur noch|10 % Zucker enthält?',
         spr='Zwölf Liter Sirup enthalten fünfundzwanzig Prozent Zucker. Wie viel Wasser muss man dazugiessen, damit die Mischung '
             'nur noch zehn Prozent Zucker enthält?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration ist vollständig?', sprich='Welche Deklaration ist vollständig?',
                             opt=['w: Menge des Wassers in l', 'w: Wasser', 'w: Zuckeranteil der Mischung in %'],
                             rueck={1: 'Was vom Wasser: Menge, Anteil? Und in welcher Einheit?',
                                    2: 'Der Anteil ist gegeben: 10 %. Gesucht ist eine Menge.'},
                             rueck_sprich={2: 'Der Anteil ist gegeben: zehn Prozent. Gesucht ist eine Menge.'}),
                  spr='w ist die Menge Wasser in Liter: Grösse, Bezug und Einheit.',
                  el=[tx(DW, 520, 40, x=RX, ein='@Menge'), n('Grösse, Bezug, Einheit', 610, 'blau', 38, x=RX, ein='@Grösse')]),
             dict(gegeben=[G_text(DW)],
                  frage=dict(text='Welche Zuckerbilanz stimmt?', sprich='Welche Zuckerbilanz stimmt?',
                             opt=['0.25 · 12 = 0.1 · (12 + w)', '0.25 · 12 = 0.1 · w', '0.25 · 12 + w = 0.1 · (12 + w)'],
                             rueck={1: 'Wie viele Liter hat die fertige Mischung?', 2: 'Wasser bringt keinen Zucker mit. Welchen Anteil hat es?'}),
                  spr='Der Zucker bleibt gleich. Vorher null Komma zwei fünf mal zwölf Liter. Nachher null Komma eins mal die ganze '
                      'Mischung, zwölf plus w Liter. Das Wasser hat den Anteil null.',
                  el=[f(r'0.25 \cdot 12 + 0 \cdot \fb{w} = 0.1 \cdot (12 + \fb{w})', 520, 42, x=RX, ein='@Vorher'),
                      n('Zucker vorher = Zucker nachher', 610, 'blau', 38, x=RX, ein='@bleibt')]),
             dict(gegeben=[G_text(DW), G_formel(r'0.25 \cdot 12 = 0.1 \cdot (12 + w)')],
                  frage=dict(text='Ausmultipliziert und geordnet: Was bleibt?', sprich='Ausmultipliziert und geordnet: Was bleibt?',
                             opt=['0.1 · w = 1.8', '0.1 · w = 3', '0.1 · w = 4.2'],
                             rueck={1: 'Rechts steht auch 0.1 · 12 = 1.2. Was passiert damit?',
                                    2: 'Beim Hinüberbringen wechselt das Vorzeichen: 1.2 addieren oder subtrahieren?'},
                             rueck_sprich={1: 'Rechts steht auch null Komma eins mal zwölf, also eins Komma zwei. Was passiert damit?',
                                           2: 'Beim Hinüberbringen wechselt das Vorzeichen. Eins Komma zwei addieren oder subtrahieren?'}),
                  spr='Links stehen drei Liter Zucker, rechts eins Komma zwei plus null Komma eins w. Minus eins Komma zwei: '
                      'null Komma eins w gleich eins Komma acht.',
                  el=[f(r'3 = 1.2 + 0.1 \cdot w \qquad \fb{\mid -1.2}', 520, 44, x=RX, ein='@Links'),
                      f(r'0.1 \cdot w = 1.8', 610, 44, x=RX, ein='@Minus')]),
             dict(gegeben=[G_text(DW), G_formel(r'0.1 \cdot w = 1.8')],
                  frage=dict(text='Welcher Typ, und was ergibt sich für w?', sprich='Welcher Typ ist das, und was ergibt sich für w?',
                             opt=['linear: w = 1.8 : 0.1 = 18', 'linear: w = 1.8 · 0.1 = 0.18', 'quadratisch: mit poly-solv'],
                             rueck={1: 'Damit w allein steht: mal 0.1 oder durch 0.1?', 2: 'Kommt w im Quadrat vor?'},
                             rueck_sprich={1: 'Damit w allein steht: mal null Komma eins oder durch null Komma eins?'}),
                  spr='Eine Unbekannte und kein Quadrat: linear. Durch null Komma eins teilen: w gleich achtzehn.',
                  el=[n('linear: von Hand lösen', 520, 'blau', 40, x=RX, ein='@linear'),
                      f(r'w = 1.8 : 0.1 = \fc{18}', 610, 48, x=RX, ein='@teilen')]),
             dict(gegeben=[G_text(DW), G_formel(r'w = 18')],
                  frage=dict(text='Welche Probe prüft den Text?', sprich='Welche Probe prüft den Text?',
                             opt=['30 l mit 3 l Zucker: 3 : 30 = 0.1', '0.1 · 18 = 1.8', '12 + 18 = 30'],
                             rueck={1: 'Das prüft die eigene Gleichung, nicht den Text.',
                                    2: 'Das prüft nur die Menge. Was sagt der Text über den Zucker?'}),
                  spr='Probe am Text: Die Mischung hat dreissig Liter und enthält drei Liter Zucker. Drei durch dreissig ist null Komma '
                      'eins, also zehn Prozent. Es braucht achtzehn Liter Wasser.',
                  el=[f(r'12 + 18 = 30\ \mathrm{l}, \quad 3 : 30 = 0.1 = 10\,\% \;\checkmark', 520, 40, x=RX, ein='@Probe'),
                      tx(r'Es braucht @\fc{18}@ l Wasser.', 610, 40, x=RX, ein='@braucht')]),
         ]),
    dict(nr=2, kurz='Mischen',
         text='Ein Fass enthält 40 l reinen Apfelsaft.|Man zapft eine Menge ab, füllt mit Wasser|auf und rührt um. Dann zapft man gleich viel|ab und füllt wieder mit Wasser auf. Jetzt|sind noch 22.5 l Saft im Fass. Wie viel|wurde jedes Mal abgezapft?',
         spr='Ein Fass enthält vierzig Liter reinen Apfelsaft. Man zapft eine Menge ab, füllt mit Wasser auf und rührt um. Dann '
             'zapft man gleich viel ab und füllt wieder mit Wasser auf. Jetzt sind noch zweiundzwanzig Komma fünf Liter Saft im Fass. '
             'Wie viel wurde jedes Mal abgezapft?',
         schritte=[
             dict(frage=dict(text='Wofür steht die Unbekannte x?', sprich='Wofür steht die Unbekannte x?',
                             opt=['x: jedes Mal abgezapfte Menge in l', 'x: Saft im Fass am Schluss in l', 'x: Saftanteil am Schluss'],
                             rueck={1: 'Die Saftmenge am Schluss ist gegeben: 22.5 l.',
                                    2: 'Den Anteil rechnest du sofort aus: 22.5 : 40. Gefragt ist etwas anderes.'},
                             rueck_sprich={1: 'Die Saftmenge am Schluss ist gegeben: zweiundzwanzig Komma fünf Liter.',
                                           2: 'Den Anteil rechnest du sofort aus: zweiundzwanzig Komma fünf durch vierzig. Gefragt ist etwas anderes.'}),
                  spr='x ist die Menge, die jedes Mal abgezapft wird, in Liter. Sie liegt zwischen null und vierzig.',
                  el=[tx(DF, 520, 40, x=RX, ein='@Menge'), f(r'0 \lt x \lt 40', 610, 44, x=RX, ein='@zwischen')]),
             dict(gegeben=[G_text(DF), G_formel(r'0 \lt x \lt 40')],
                  frage=dict(text='Welche Gleichung beschreibt den Saft am Schluss?',
                             sprich='Welche Gleichung beschreibt den Saft am Schluss?',
                             opt=['(40 − x) · (40 − x) : 40 = 22.5', '40 − 2·x = 22.5', '40 − x = 22.5'],
                             rueck={1: 'Beim zweiten Mal ist nicht mehr reiner Saft im Fass. Gehen dann x Liter Saft weg?',
                                    2: 'Es wurde zweimal abgezapft.'}),
                  spr='Nach dem ersten Mal sind vierzig minus x Liter Saft im Fass, der Saftanteil ist vierzig minus x durch vierzig. '
                      'Beim zweiten Mal gehen x Liter Gemisch weg, darin nur x mal dieser Anteil an Saft. Übrig bleibt vierzig minus x '
                      'mal vierzig minus x durch vierzig.',
                  el=[f(r'\text{nach dem 1. Mal: } 40 - x \text{ l Saft, Anteil } \dfrac{40 - x}{40}', 520, 34, x=RX, ein='@ersten'),
                      f(r'(40 - x) - x \cdot \dfrac{40 - x}{40} = \dfrac{(40 - x)^2}{40} = 22.5', 650, 36, x=RX, ein='@zweiten'),
                      n('Saft vorher − Saft weg = Saft nachher', 790, 'blau', 36, x=RX, ein='@Übrig')]),
             dict(gegeben=[G_text(DF), G_formel(r'\dfrac{(40 - x)^2}{40} = 22.5', 40, 130)],
                  frage=dict(text='Mal 40, ausmultipliziert, auf null: Was tippst du ein?',
                             sprich='Mal vierzig, ausmultipliziert und auf null gebracht: Was tippst du in poly-solv ein?',
                             opt=['a = 1, b = −80, c = 700', 'a = 1, b = −80, c = 1600', 'a = 1, b = −40, c = 700'],
                             rueck={1: 'Die 900 von rechts gehört auch nach links: 1600 − 900.',
                                    2: 'Prüfe das Mittelglied von (40 − x)²: 2 · 40 · x.'},
                             rueck_sprich={1: 'Die neunhundert von rechts gehört auch nach links: tausendsechshundert minus neunhundert.',
                                           2: 'Prüfe das Mittelglied von Klammer vierzig minus x im Quadrat: zwei mal vierzig mal x.'}),
                  spr='Mal vierzig: Klammer vierzig minus x im Quadrat gleich neunhundert. Ausmultipliziert x Quadrat minus achtzig x plus '
                      'tausendsechshundert gleich neunhundert. Minus neunhundert gibt die Grundform: x Quadrat minus achtzig x plus '
                      'siebenhundert gleich null. Für poly-solv: a gleich eins, b gleich minus achtzig, c gleich siebenhundert.',
                  el=[f(r'(40 - x)^2 = 900', 520, 42, x=RX, ein='@Mal'),
                      f(r'x^2 - 80 \cdot x + 1600 = 900', 600, 42, x=RX, ein='@Ausmultipliziert'),
                      f(r'x^2 - 80 \cdot x + 700 = 0', 680, 46, x=RX, ein='@Grundform'),
                      ] + poly_eingabe(1, -80, 700, 640, '@poly')),
             dict(gegeben=[G_text(DF), G_formel(r'x^2 - 80 \cdot x + 700 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 70 und x2 = 10. Was gilt?',
                             sprich='poly-solv zeigt x eins gleich siebzig und x zwei gleich zehn. Was gilt?',
                             opt=['Nur x = 10 passt.', 'Beide passen.', 'Nur x = 70 passt.'],
                             rueck={1: 'Lassen sich aus einem Fass mit 40 l zweimal 70 l abzapfen?', 2: 'Prüfe die Bedingung 0 < x < 40.'},
                             rueck_sprich={1: 'Lassen sich aus einem Fass mit vierzig Litern zweimal siebzig Liter abzapfen?',
                                           2: 'Prüfe die Bedingung: x liegt zwischen null und vierzig.'}),
                  spr='Siebzig Liter lassen sich aus vierzig Litern nicht abzapfen. Diese Lösung fällt weg. Es bleibt x gleich zehn.',
                  el=ergebnis('x1=70', 'x2=10') + [
                      tx(r'@\fd{x = 70}@: mehr als im Fass', 760, 36, x=RX, ein='@abzapfen'),
                      f(r'x = \fc{10}', 850, 48, x=RX, ein='@bleibt')]),
             dict(gegeben=[G_text(DF), G_formel(r'x = 10')],
                  frage=dict(text='Welche Probe am Text stimmt?', sprich='Welche Probe am Text stimmt?',
                             opt=['30 l Saft; 10 l Gemisch mit ¾ Saft: 30 − 7.5 = 22.5', '40 − 2 · 10 = 20, also falsch', '10² − 80 · 10 + 700 = 0'],
                             rueck={1: 'Das ist der falsche Ansatz: Beim zweiten Mal gehen nicht 10 l Saft weg.',
                                    2: 'Das prüft die eigene Gleichung, nicht den Text.'},
                             rueck_sprich={1: 'Das ist der falsche Ansatz: Beim zweiten Mal gehen nicht zehn Liter Saft weg.'}),
                  spr='Probe am Text: Nach dem ersten Mal sind dreissig Liter Saft im Fass, drei Viertel des Inhalts. Die zehn Liter Gemisch '
                      'enthalten sieben Komma fünf Liter Saft. Es bleiben zweiundzwanzig Komma fünf Liter. Jedes Mal wurden zehn Liter abgezapft.',
                  el=[f(r'30 - 10 \cdot \tfrac{3}{4} = 30 - 7.5 = 22.5 \;\checkmark', 520, 42, x=RX, ein='@Probe'),
                      tx(r'Jedes Mal @\fc{10}@ l abgezapft.', 610, 40, x=RX, ein='@Jedes')]),
         ]),
], merke('Zum Mitnehmen: In der Stoffbilanz bleibt der Stoff erhalten, vorher gleich nachher. Wasser hat den Anteil null. Wird zweimal '
         'Gemisch entnommen, nimmt der zweite Zug weniger Stoff mit, und die Gleichung wird quadratisch. Lösungen, die mehr '
         'entnehmen, als da ist, fallen weg.',
         'Stoff vorher = Stoff nachher|Wasser: Anteil 0|zweimal Gemisch entnommen: quadratisch|unmögliche Lösungen verwerfen'),
   folge=5)

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle, zwei Unbekannte
DL = [G_text(r'@\fa{x}@: Masse der 60-%-Legierung in kg', 34), G_text(r'@\fb{y}@: Masse der 85-%-Legierung in kg', 34)]
DS = [G_text(r'@\fa{m}@: Masse der Lösung in kg', 34), G_text(r'@\fb{p}@: Salzanteil (Dezimalzahl)', 34)]
kontrolle('kontrolle-mischen-2', 'Ansatz finden: Mischen mit zwei Unbekannten',
          'Zwei Mischaufgaben Schritt für Schritt: zwei Legierungen (lineares System, sys-solv) und eine Salzlösung mit unbekannter Masse und unbekanntem Anteil (quadratisches System, poly-solv).',
          ['Mischungsaufgabe', 'Legierung', 'lineares Gleichungssystem', 'quadratisches Gleichungssystem', 'sys-solv', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Mischen',
         text='Eine Giesserei mischt eine Legierung mit|60 % Kupfer und eine mit 85 % Kupfer zu|50 kg einer Legierung mit 70 % Kupfer.|Wie viel kg braucht sie von jeder?',
         spr='Eine Giesserei mischt eine Legierung mit sechzig Prozent Kupfer und eine mit fünfundachtzig Prozent Kupfer zu fünfzig '
             'Kilogramm einer Legierung mit siebzig Prozent Kupfer. Wie viel Kilogramm braucht sie von jeder?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration passt zur Frage?', sprich='Welche Deklaration passt zur Frage?',
                             opt=['x, y: Masse der 60-%- und der 85-%-Legierung in kg', 'x: 60 %, y: 85 %', 'x: Kupfer in kg, y: Zink in kg'],
                             rueck={1: 'Die Anteile sind gegeben. Gesucht sind Massen.',
                                    2: 'Gefragt ist, wie viel von jeder Legierung. Die Zusammensetzung kennst du schon.'}),
                  spr='x ist die Masse der Legierung mit sechzig Prozent Kupfer, y die Masse der Legierung mit fünfundachtzig Prozent, '
                      'beide in Kilogramm.',
                  el=[tx(r'@\fa{x}@: Masse der 60-%-Legierung in kg', 520, 38, x=RX, ein='@Masse'),
                      tx(r'@\fb{y}@: Masse der 85-%-Legierung in kg', 590, 38, x=RX, ein='@Masse#2')]),
             dict(gegeben=DL,
                  frage=dict(text='Welche Kupferbilanz stimmt?', sprich='Welche Kupferbilanz stimmt?',
                             opt=['0.6·x + 0.85·y = 0.7·50', '0.6·x + 0.85·y = 0.7', '60·x + 85·y = 70'],
                             rueck={1: 'Links stehen kg Kupfer, rechts ein Anteil. Was gehört rechts hin?',
                                    2: 'Links Prozent mal kg, rechts nur Prozent: Die Einheiten passen nicht.'}),
                  spr='Mengenbilanz: x plus y gleich fünfzig Kilogramm. Kupferbilanz: null Komma sechs x plus null Komma acht fünf y '
                      'gleich null Komma sieben mal fünfzig, also fünfunddreissig Kilogramm Kupfer.',
                  el=[f(r'\begin{cases} x + y = 50 \\ 0.6 \cdot x + 0.85 \cdot y = 0.7 \cdot 50 = 35 \end{cases}', 520, 40, x=RX, ein='@Mengenbilanz'),
                      n('links und rechts: kg Kupfer', 700, 'blau', 38, x=RX, ein='@Kupferbilanz')]),
             dict(gegeben=DL + [G_formel(r'\begin{cases} x + y = 50 \\ 0.6 \cdot x + 0.85 \cdot y = 35 \end{cases}', 36, 110)],
                  frage=dict(text='Mal 100 für sys-solv: Wie heisst Zeile 2?', sprich='Mal hundert für sys-solv: Wie heisst Zeile zwei?',
                             opt=['60·x + 85·y = 3500', '60·x + 85·y = 35', '60·x + 85·y = 70'],
                             rueck={1: 'Mit 100 multipliziert wird auch die rechte Seite.', 2: 'Rechts gehört die Kupfermasse hin, nicht der Anteil.'},
                             rueck_sprich={1: 'Mit hundert multipliziert wird auch die rechte Seite.'}),
                  spr='Damit ganze Zahlen dastehen, die Kupferbilanz mal hundert: sechzig x plus fünfundachtzig y gleich '
                      'dreitausendfünfhundert. Zeile eins bleibt eins, eins, fünfzig.',
                  el=[f(r'\begin{cases} x + y = 50 \\ 60 \cdot x + 85 \cdot y = 3500 \end{cases}', 520, 44, x=RX, ein='@ganze'),
                      ] + sys_eingabe((1, 1, 50), (60, 85, 3500), 640, '@Zeile')),
             dict(gegeben=DL + [G_formel(r'60 \cdot x + 85 \cdot y = 3500', 38)],
                  frage=dict(text='sys-solv zeigt x = 30 und y = 20. Ist das plausibel?',
                             sprich='sys-solv zeigt x gleich dreissig und y gleich zwanzig. Ist das plausibel?',
                             opt=['Ja: 70 % liegt näher bei 60 %.', 'Nein: es müsste mehr 85 % sein.', 'Ja, denn 30 + 20 = 50 genügt.'],
                             rueck={1: '70 % liegt näher bei 60 % als bei 85 %. Von welcher Sorte braucht es mehr?',
                                    2: 'Die Mengenbilanz allein prüft den Kupferanteil nicht.'},
                             rueck_sprich={1: 'Siebzig Prozent liegt näher bei sechzig als bei fünfundachtzig Prozent. Von welcher Sorte braucht es mehr?'}),
                  spr='Plausibel: Siebzig Prozent liegt näher bei sechzig als bei fünfundachtzig Prozent. Also braucht es mehr von der '
                      'Legierung mit sechzig Prozent: dreissig Kilogramm, und zwanzig von der anderen.',
                  el=ergebnis('x=30', 'y=20') + [
                      tx('mehr von der 60-%-Legierung: plausibel', 760, 36, x=RX, ein='@Plausibel')]),
             dict(gegeben=DL + [G_formel(r'x = 30,\ y = 20')],
                  frage=dict(text='Welche Probe prüft den Kupferanteil?', sprich='Welche Probe prüft den Kupferanteil?',
                             opt=['18 + 17 = 35 kg; 35 : 50 = 0.7', '30 + 20 = 50 kg', '0.6 + 0.85 = 1.45'],
                             rueck={1: 'Das prüft nur die Menge.', 2: 'Anteile addieren sich nie.'}),
                  spr='Probe am Text: null Komma sechs mal dreissig gleich achtzehn, null Komma acht fünf mal zwanzig gleich siebzehn, '
                      'zusammen fünfunddreissig Kilogramm Kupfer. Fünfunddreissig durch fünfzig ist null Komma sieben, siebzig Prozent. '
                      'Es braucht dreissig Kilogramm der einen und zwanzig Kilogramm der anderen Legierung.',
                  el=[f(r'0.6 \cdot 30 + 0.85 \cdot 20 = 18 + 17 = 35 \;\checkmark', 520, 40, x=RX, ein='@Probe'),
                      f(r'35 : 50 = 0.7 = 70\,\% \;\checkmark', 600, 40, x=RX, ein='@durch'),
                      tx(r'@\fc{30}@ kg mit 60 %, @\fc{20}@ kg mit 85 %', 690, 38, x=RX, ein='@braucht')]),
         ]),
    dict(nr=2, kurz='Mischen',
         text='Eine Salzlösung enthält 6 kg Salz. Gibt man|10 kg Wasser dazu, sinkt ihr Salzanteil um|10 Prozentpunkte. Wie schwer war die Lösung,|und welchen Salzanteil hatte sie?',
         spr='Eine Salzlösung enthält sechs Kilogramm Salz. Gibt man zehn Kilogramm Wasser dazu, sinkt ihr Salzanteil um zehn '
             'Prozentpunkte. Wie schwer war die Lösung, und welchen Salzanteil hatte sie?',
         schritte=[
             dict(frage=dict(text='Was ist unbekannt? Wähle die Deklaration.', sprich='Was ist unbekannt? Wähle die Deklaration.',
                             opt=['m: Masse der Lösung in kg, p: Salzanteil', 'm: Masse des Salzes in kg, p: Salzanteil', 'm: Masse des Wassers in kg'],
                             rueck={1: 'Das Salz ist gegeben: 6 kg.', 2: 'Das Wasser ist gegeben: 10 kg. Was ist unbekannt?'},
                             rueck_sprich={1: 'Das Salz ist gegeben: sechs Kilogramm.', 2: 'Das Wasser ist gegeben: zehn Kilogramm. Was ist unbekannt?'}),
                  spr='m ist die Masse der Lösung in Kilogramm, p ihr Salzanteil als Dezimalzahl. Zehn Prozentpunkte weniger heisst: '
                      'p minus null Komma eins.',
                  el=[tx(r'@\fa{m}@: Masse der Lösung in kg', 520, 38, x=RX, ein='@Masse'),
                      tx(r'@\fb{p}@: Salzanteil (Dezimalzahl)', 590, 38, x=RX, ein='@Salzanteil'),
                      n('10 Prozentpunkte weniger: @p - 0.1@', 690, 'blau', 38, x=RX, ein='@Prozentpunkte')]),
             dict(gegeben=DS,
                  frage=dict(text='Welches System stimmt?', sprich='Welches System stimmt?',
                             opt=['m·p = 6 und (m + 10)·(p − 0.1) = 6', 'm·p = 6 und (m + 10)·p = 6 − 0.1', 'm·p = 6 und (m + 10)·(p − 10) = 6'],
                             rueck={1: 'Der Salzanteil sinkt um 0.1, nicht die Salzmenge.', 2: '10 Prozentpunkte sind als Dezimalzahl 0.1.'},
                             rueck_sprich={1: 'Der Salzanteil sinkt um null Komma eins, nicht die Salzmenge.',
                                           2: 'Zehn Prozentpunkte sind als Dezimalzahl null Komma eins.'}),
                  spr='Salz gleich Masse mal Anteil. Vorher: m mal p gleich sechs. Nachher ist die Masse m plus zehn, der Anteil p minus '
                      'null Komma eins, und das Salz ist immer noch sechs Kilogramm. Zwei Unbekannte werden multipliziert: Das System ist quadratisch.',
                  el=[f(r'\begin{cases} m \cdot p = 6 \\ (m + 10) \cdot (p - 0.1) = 6 \end{cases}', 520, 42, x=RX, ein='@Vorher'),
                      n('Produkt der Unbekannten: quadratisch', 700, 'rot', 38, x=RX, ein='@multipliziert')]),
             dict(gegeben=DS + [G_formel(r'\begin{cases} m \cdot p = 6 \\ (m + 10) \cdot (p - 0.1) = 6 \end{cases}', 36, 110)],
                  frage=dict(text='Nach dem Einsetzen: Welche Grundform entsteht?', sprich='Nach dem Einsetzen: Welche Grundform entsteht?',
                             opt=['m² + 10·m − 600 = 0', 'm² + 10·m + 600 = 0', 'm² − 10·m − 600 = 0'],
                             rueck={1: 'Prüfe das Vorzeichen der 600.', 2: 'Prüfe das Vorzeichen in p = 0.01·m + 0.1.'},
                             rueck_sprich={1: 'Prüfe das Vorzeichen der sechshundert.',
                                           2: 'Prüfe das Vorzeichen in p gleich null Komma null eins m plus null Komma eins.'}),
                  spr='Ausmultipliziert: m p minus null Komma eins m plus zehn p minus eins gleich sechs. Mit m p gleich sechs bleibt '
                      'zehn p gleich null Komma eins m plus eins, also p gleich null Komma null eins m plus null Komma eins. Eingesetzt in '
                      'm mal p gleich sechs und mal hundert: m Quadrat plus zehn m minus sechshundert gleich null.',
                  el=[f(r'm p - 0.1 \cdot m + 10 \cdot p - 1 = 6', 520, 38, x=RX, ein='@Ausmultipliziert'),
                      f(r'p = 0.01 \cdot m + 0.1', 590, 38, x=RX, ein='@also'),
                      f(r'm \cdot (0.01 \cdot m + 0.1) = 6', 660, 38, x=RX, ein='@Eingesetzt'),
                      f(r'm^2 + 10 \cdot m - 600 = 0', 740, 44, x=RX, ein='@hundert'),
                      ] + poly_eingabe(1, 10, -600, 640, '@hundert+1')),
             dict(gegeben=DS + [G_formel(r'm^2 + 10 \cdot m - 600 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 20 und x2 = −30. Was folgt?',
                             sprich='poly-solv zeigt x eins gleich zwanzig und x zwei gleich minus dreissig. Was folgt?',
                             opt=['m = 20, dann p = 0.3', 'm = 20 oder m = −30', 'm = −30, dann p = −0.2'],
                             rueck={1: 'Kann eine Masse negativ sein?', 2: 'Eine Masse ist nie negativ.'}),
                  spr='Eine Masse ist nie negativ, minus dreissig fällt weg. Also m gleich zwanzig Kilogramm, und p gleich sechs durch '
                      'zwanzig gleich null Komma drei.',
                  el=ergebnis('x1=20', 'x2=⁻30') + [
                      tx(r'@\fd{m = -30}@: keine Masse', 760, 36, x=RX, ein='@negativ'),
                      f(r'm = \fc{20}, \quad p = 6 : 20 = \fc{0.3}', 850, 44, x=RX, ein='@Also')]),
             dict(gegeben=DS + [G_formel(r'm = 20,\ p = 0.3')],
                  frage=dict(text='Wie lautet die Antwort auf die Frage?', sprich='Wie lautet die Antwort auf die Frage?',
                             opt=['20 kg Lösung mit 30 % Salz', '20 kg Lösung mit 0.3 % Salz', '30 kg Lösung mit 20 % Salz'],
                             rueck={1: '0.3 als Prozent: Wie viel ist das?', 2: 'Das ist die Lösung nach dem Verdünnen. Gefragt ist die ursprüngliche.'},
                             rueck_sprich={1: 'Null Komma drei als Prozent: Wie viel ist das?'}),
                  spr='Die Lösung wog zwanzig Kilogramm und hatte dreissig Prozent Salz. Probe am Text: null Komma drei mal zwanzig gleich '
                      'sechs Kilogramm Salz. Mit dem Wasser sind es dreissig Kilogramm, sechs durch dreissig ist zwanzig Prozent: zehn '
                      'Prozentpunkte weniger.',
                  el=[tx(r'@\fc{20}@ kg Lösung mit @\fc{30\,\%}@ Salz', 520, 40, x=RX, ein='@wog'),
                      f(r'0.3 \cdot 20 = 6 \;\checkmark \qquad 6 : 30 = 0.2 = 20\,\% \;\checkmark', 610, 38, x=RX, ein='@Probe')]),
         ]),
], merke('Zum Mitnehmen: Zwei Sorten mit bekanntem Anteil geben ein lineares System, Mengenbilanz und Stoffbilanz. Für sys-solv '
         'darf die Stoffbilanz mit hundert multipliziert werden. Sind Menge und Anteil beide unbekannt, steht ein Produkt im System: '
         'einsetzen, Grundform, poly-solv, und negative Massen verwerfen.',
         'Mengenbilanz + Stoffbilanz: sys-solv|Menge und Anteil unbekannt: quadratisch|negative Massen verwerfen'),
   folge=6)


# ════════════════════════════════════════════════ Kapitel 3 · Einführung
def rechteckbild(ein=0.05, flaeche=True, breite=False, ein_fl=None, ein_br=None, fuenf=False, ein5=None):
    """Rechteckmodell: Breite = Anzahl Fahrten, Höhe = Tonnen pro Fahrt, Fläche = Tonnen."""
    fl = [{'punkte': [[0, 0], [5, 0], [5, 18], [0, 18]], 'farbe': 1, 'deckung': 0.3},
          {'punkte': [[5, 0], [12, 0], [12, 14], [5, 14]], 'farbe': 2, 'deckung': 0.3}]
    tx_ = [{'bei': [2.5, -1.6], 'text': 'x', 'farbe': 1, 'groesse': 34},
           {'bei': [8.5, -1.6], 'text': 'y', 'farbe': 2, 'groesse': 34}]
    if flaeche:
        tx_ += [{'bei': [2.5, 9], 'text': '18 · x', 'farbe': 1, 'groesse': 34, 'ein': ein_fl or 0.05},
                {'bei': [8.5, 7], 'text': '14 · y', 'farbe': 2, 'groesse': 34, 'ein': ein_fl or 0.05}]
    st = []
    if breite:
        st = [{'von': [0, 19.6], 'bis': [12, 19.6], 'farbe': 3, 'dicke': 4, 'ein': ein_br or 0.05}]
        tx_.append({'bei': [6, 20.5], 'text': 'x + y = 12', 'farbe': 3, 'groesse': 32, 'ein': ein_br or 0.05})
    xt = [[12, '12']] + ([[5, '5']] if fuenf else [])
    g = dict(typ='graf', x=RX, y=180, breite=820, hoehe=700, abstand=0, anim='fade', ein=ein, pfeile=True,
             xname='Fahrten', yname='t pro Fahrt', xbereich=[-0.8, 13.6], ybereich=[-3, 22.5],
             xteilung=xt, yteilung=[[14, '14'], [18, '18']], flaechen=fl, texte=tx_, strecken=st)
    return g


clip('verteilen', 'Ansatz finden: Verteilen',
     'Stückbilanz und Wertbilanz am Kieswerk: Anzahl mal Wert pro Stück, im Rechteckmodell als Breite und Fläche. Dazu Sets, die in zwei Stückbilanzen zählen, und ganze Zahlen.',
     ['Verteilungsaufgabe', 'Stückbilanz', 'Wertbilanz', 'Rechteckmodell', 'sys-solv'], [
         sz('Fahrten',
            'Ein Kieswerk liefert mit zwei Lastwagen Kies. Lastwagen A lädt pro Fahrt achtzehn Tonnen, Lastwagen B vierzehn Tonnen, '
            'beide immer voll. In zwölf Fahrten werden hundertachtundachtzig Tonnen geliefert. Wie viele Fahrten hat jeder gemacht?',
            tx('A: 18 t pro Fahrt|B: 14 t pro Fahrt|12 Fahrten, zusammen 188 t', 260, 42, ein=0.6),
            rechteckbild(ein=0.6, flaeche=False)),
         sz('Deklarieren',
            'Unbekannt sind die Anzahlen: x Fahrten von Lastwagen A, y Fahrten von Lastwagen B. Anzahlen sind ganze Zahlen und nicht negativ.',
            tx(r'@\fa{x}@: Anzahl Fahrten Lastwagen A', 280, 40, ein='@Anzahlen'),
            tx(r'@\fb{y}@: Anzahl Fahrten Lastwagen B', 350, 40, ein='@Lastwagen#2'),
            n('ganze Zahlen, nicht negativ', 460, 'blau', 40, ein='@ganze'),
            rechteckbild(flaeche=False)),
         sz('Stückbilanz',
            'Im Bild ist jede Fahrt ein Streifen. Die Breite zählt die Fahrten: x plus y gleich zwölf. Das ist die Stückbilanz.',
            f(r'\fa{x} + \fb{y} = 12', 300, 56, ein='@Breite'),
            n('Stückbilanz: Anzahl Fahrten', 420, 'blau', 42, ein='@Stückbilanz'),
            rechteckbild(flaeche=False, breite=True, ein_br='@Breite')),
         sz('Wertbilanz',
            'Jeder Streifen ist so hoch wie die Ladung einer Fahrt. Die Fläche ist Anzahl mal Tonnen pro Fahrt: achtzehn x plus '
            'vierzehn y gleich hundertachtundachtzig. Das ist die Wertbilanz.',
            f(r'18 \cdot \fa{x} + 14 \cdot \fb{y} = 188', 300, 52, ein='@Fläche'),
            n('Wertbilanz: Tonnen Kies', 420, 'blau', 42, ein='@Wertbilanz'),
            f(r'\text{Anzahl} \cdot \text{Wert pro Stück} = \text{Wert}', 520, 40, ein='@Anzahl'),
            rechteckbild(breite=True, ein_fl='@Fläche')),
         sz('Lösen',
            'Beide Gleichungen sind schon geordnet. sys-solv liefert x gleich fünf und y gleich sieben. Probe am Text: neunzig plus '
            'achtundneunzig gleich hundertachtundachtzig Tonnen, und fünf plus sieben gleich zwölf Fahrten.',
            rechner(['(1)x+(1)y=12', '(18)x+(14)y=188'], ['enter'], 230, '@geordnet', LX, 700),
            rechner(['x=5', ''], ['enter'], 560, '@liefert', LX, 400),
            rechner(['y=7', ''], ['enter'], 560, '@liefert+0.8', LX + 420, 400),
            f(r'18 \cdot 5 + 14 \cdot 7 = 90 + 98 = 188 \;\checkmark', 800, 40, ein='@Probe'),
            rechteckbild(breite=True, fuenf=True)),
         sz('Sets',
            'Vorsicht bei Sets. Ein Set Stöcke und Brille enthält zwei Artikel. Es zählt in beiden Stückbilanzen: einmal bei den '
            'Stöcken, einmal bei den Brillen. Darum gibt es eine Stückbilanz pro Artikel.',
            titel('Ein Set zählt doppelt', 250, 66),
            tx(r'@x@: einzelne Stöcke, @y@: einzelne Brillen, @\fc{z}@: Sets', 380, 40, ein='@Set'),
            f(r'\begin{cases} x + \fc{z} = 21 & \text{(Stöcke)} \\ y + \fc{z} = 17 & \text{(Brillen)} \end{cases}', 470, 46, ein='@beiden'),
            n('eine Stückbilanz pro Artikel', 660, 'rot', 42, ein='@Darum')),
         sz('Ganze Zahlen',
            'Und wenn das Ergebnis nicht ganz ist? Mit hundertneunzig Tonnen statt hundertachtundachtzig ergibt sich x gleich fünf '
            'Komma fünf. Eine halbe Fahrt gibt es nicht: Mit zwölf vollen Fahrten sind hundertneunzig Tonnen nicht möglich.',
            f(r'18 \cdot x + 14 \cdot (12 - x) = 190 \;\Rightarrow\; 4 \cdot x = 22', 300, 46, ein='@Tonnen'),
            f(r'x = 5.5 \quad \fd{\text{keine ganze Zahl}}', 400, 46, ein='@ergibt'),
            n('Die Probe am Text entscheidet: nicht möglich.', 530, 'rot', 42, ein='@halbe')),
         sz('Quadratisch',
            'Sind Anzahl und Wert pro Stück beide unbekannt, etwa die Anzahl Personen und der Betrag pro Person, steht ein Produkt '
            'zweier Unbekannter. Dann wird das System quadratisch.',
            titel('Wann quadratisch?', 250, 66),
            f(r'\fa{\text{Anzahl}} \cdot \fb{\text{Betrag pro Person}} = \text{Kosten}', 400, 44, ein='@Produkt'),
            n('beide unbekannt: Produkt, quadratisch', 520, 'rot', 44, ein='@quadratisch')),
         sz('Merke',
            'Zum Mitnehmen: Die Stückbilanz zählt die Stücke, die Wertbilanz Anzahl mal Wert pro Stück. Ein Set zählt in jeder '
            'Stückbilanz seiner Artikel. Stückzahlen müssen ganz und nicht negativ sein.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x + y = N \qquad a \cdot x + b \cdot y = W', 390, 50, ein=1.2),
            n('Set: in beiden Stückbilanzen|Stückzahlen ganz, nicht negativ', 500, 'blau', 46, ein='@Set')),
         JETZT_DU,
     ], folge=7)

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle, eine Unbekannte
DB = r'@\fa{x}@: Anzahl Erwachsenenbillette; Rest @24 - x@'
DR = r'@\fa{r}@: Anzahl Reihen; Stühle pro Reihe @r + 6@'
kontrolle('kontrolle-verteilen-1', 'Ansatz finden: Verteilen mit einer Unbekannten',
          'Zwei Verteilaufgaben Schritt für Schritt: Billette zu zwei Preisen (linear) und Stühle in Reihen (quadratisch, poly-solv).',
          ['Verteilungsaufgabe', 'lineare Gleichung', 'quadratische Gleichung', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Verteilen',
         text='Für einen Klassenausflug kauft eine Lehrerin|24 Billette: für Erwachsene zu 18 CHF, für|Jugendliche zu 12 CHF. Zusammen bezahlt sie|312 CHF. Wie viele Erwachsenenbillette sind es?',
         spr='Für einen Klassenausflug kauft eine Lehrerin vierundzwanzig Billette: für Erwachsene zu achtzehn Franken, für '
             'Jugendliche zu zwölf Franken. Zusammen bezahlt sie dreihundertzwölf Franken. Wie viele Erwachsenenbillette sind es?',
         schritte=[
             dict(frage=dict(text='Mit einer Unbekannten: Was ist x, was der Rest?',
                             sprich='Mit einer Unbekannten: Was ist x, und was ist der Rest?',
                             opt=['x: Erwachsenenbillette (Stück), Rest 24 − x', 'x: Preis eines Erwachsenenbilletts',
                                  'x: Erwachsenenbillette (Stück), Rest x − 24'],
                             rueck={1: 'Der Preis ist gegeben: 18 CHF.', 2: 'Bei x = 4 wäre der Rest negativ. Wie viele Billette bleiben?'},
                             rueck_sprich={1: 'Der Preis ist gegeben: achtzehn Franken.',
                                           2: 'Bei x gleich vier wäre der Rest negativ. Wie viele Billette bleiben?'}),
                  spr='x ist die Anzahl Erwachsenenbillette. Die übrigen vierundzwanzig minus x Billette sind für Jugendliche.',
                  el=[tx(r'@\fa{x}@: Anzahl Erwachsenenbillette', 520, 40, x=RX, ein='@Anzahl'),
                      tx(r'Jugendbillette: @24 - x@', 600, 40, x=RX, ein='@übrigen')]),
             dict(gegeben=[G_text(DB, 34)],
                  frage=dict(text='Welche Wertbilanz stimmt?', sprich='Welche Wertbilanz stimmt?',
                             opt=['18·x + 12·(24 − x) = 312', '18·x + 12·x = 312', 'x + (24 − x) = 312'],
                             rueck={1: 'Wie viele Jugendbillette sind es: auch x?', 2: 'Hier werden Stück gezählt, rechts stehen aber Franken.'}),
                  spr='Die Beträge ergeben zusammen dreihundertzwölf Franken: achtzehn mal x plus zwölf mal Klammer vierundzwanzig minus x '
                      'gleich dreihundertzwölf. Die Stückbilanz steckt schon im Term vierundzwanzig minus x.',
                  el=[f(r'18 \cdot x + 12 \cdot (24 - x) = 312', 520, 44, x=RX, ein='@Beträge'),
                      n('Stückbilanz im Term @24 - x@', 610, 'blau', 38, x=RX, ein='@Stückbilanz')]),
             dict(gegeben=[G_text(DB, 34), G_formel(r'18 \cdot x + 12 \cdot (24 - x) = 312')],
                  frage=dict(text='Ausmultipliziert und zusammengefasst: Was bleibt?',
                             sprich='Ausmultipliziert und zusammengefasst: Was bleibt?',
                             opt=['6·x = 24', '30·x = 24', '6·x = 312'],
                             rueck={1: 'Das Minus vor 12·x: 18·x − 12·x = ?', 2: 'Was ist mit 12 · 24 = 288 passiert?'},
                             rueck_sprich={1: 'Das Minus vor zwölf x: achtzehn x minus zwölf x gleich?',
                                           2: 'Was ist mit zwölf mal vierundzwanzig gleich zweihundertachtundachtzig passiert?'}),
                  spr='Ausmultipliziert: achtzehn x plus zweihundertachtundachtzig minus zwölf x gleich dreihundertzwölf. Zusammengefasst '
                      'sechs x plus zweihundertachtundachtzig gleich dreihundertzwölf, also sechs x gleich vierundzwanzig.',
                  el=[f(r'18 \cdot x + 288 - 12 \cdot x = 312', 520, 42, x=RX, ein='@Ausmultipliziert'),
                      f(r'6 \cdot x + 288 = 312 \qquad \fb{\mid -288}', 600, 42, x=RX, ein='@Zusammengefasst'),
                      f(r'6 \cdot x = 24', 680, 44, x=RX, ein='@also')]),
             dict(gegeben=[G_text(DB, 34), G_formel(r'6 \cdot x = 24')],
                  frage=dict(text='Welcher Typ, und was ergibt sich für x?', sprich='Welcher Typ, und was ergibt sich für x?',
                             opt=['linear: x = 24 : 6 = 4', 'linear: x = 24 · 6 = 144', 'quadratisch: poly-solv'],
                             rueck={1: '144 Billette bei 24 insgesamt?', 2: 'Kommt x im Quadrat vor?'},
                             rueck_sprich={1: 'Hundertvierundvierzig Billette bei vierundzwanzig insgesamt?'}),
                  spr='Eine Unbekannte und kein Quadrat: linear. Durch sechs teilen: x gleich vier.',
                  el=[n('linear: von Hand lösen', 520, 'blau', 40, x=RX, ein='@linear'),
                      f(r'x = 24 : 6 = \fc{4}', 610, 48, x=RX, ein='@teilen')]),
             dict(gegeben=[G_text(DB, 34), G_formel(r'x = 4')],
                  frage=dict(text='Wie lautet der Antwortsatz?', sprich='Wie lautet der Antwortsatz?',
                             opt=['Es sind 4 Erwachsenenbillette.', 'Es sind 4 Franken.', 'Es sind 20 Erwachsenenbillette.'],
                             rueck={1: 'x zählt Billette, nicht Franken.', 2: '20 ist der Rest: 24 − x.'},
                             rueck_sprich={2: 'Zwanzig ist der Rest: vierundzwanzig minus x.'}),
                  spr='Es sind vier Erwachsenenbillette und zwanzig Jugendbillette. Probe am Text: vier mal achtzehn plus zwanzig mal zwölf, '
                      'zweiundsiebzig plus zweihundertvierzig, gibt dreihundertzwölf Franken.',
                  el=[tx(r'@\fc{4}@ Erwachsenenbillette, @20@ Jugendbillette', 520, 40, x=RX, ein='@Erwachsenenbillette'),
                      f(r'4 \cdot 18 + 20 \cdot 12 = 72 + 240 = 312 \;\checkmark', 610, 40, x=RX, ein='@Probe')]),
         ]),
    dict(nr=2, kurz='Verteilen',
         text='In einem Saal stehen 216 Stühle in Reihen|mit gleich vielen Stühlen. Jede Reihe hat|6 Stühle mehr, als es Reihen gibt.|Wie viele Reihen sind es?',
         spr='In einem Saal stehen zweihundertsechzehn Stühle in Reihen mit gleich vielen Stühlen. Jede Reihe hat sechs Stühle mehr, '
             'als es Reihen gibt. Wie viele Reihen sind es?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration passt zum Text?', sprich='Welche Deklaration passt zum Text?',
                             opt=['r: Anzahl Reihen; pro Reihe r + 6 Stühle', 'r: Anzahl Reihen; pro Reihe 6·r Stühle', 'r: Anzahl Stühle'],
                             rueck={1: '«6 mehr» heisst plus 6, nicht 6-mal so viele.', 2: 'Die Anzahl Stühle ist gegeben: 216.'},
                             rueck_sprich={1: 'Sechs mehr heisst plus sechs, nicht sechsmal so viele.',
                                           2: 'Die Anzahl Stühle ist gegeben: zweihundertsechzehn.'}),
                  spr='r ist die Anzahl Reihen. Jede Reihe hat sechs Stühle mehr: r plus sechs.',
                  el=[tx(r'@\fa{r}@: Anzahl Reihen', 520, 40, x=RX, ein='@Anzahl'),
                      tx(r'Stühle pro Reihe: @r + 6@', 600, 40, x=RX, ein='@Jede')]),
             dict(gegeben=[G_text(DR, 34)],
                  frage=dict(text='Welche Gleichung gibt die Anzahl Stühle?', sprich='Welche Gleichung gibt die Anzahl Stühle?',
                             opt=['r·(r + 6) = 216', 'r + (r + 6) = 216', 'r·6 = 216'],
                             rueck={1: 'Reihen mal Stühle pro Reihe gibt alle Stühle, nicht die Summe.', 2: 'Stühle pro Reihe sind r + 6, nicht 6.'},
                             rueck_sprich={2: 'Stühle pro Reihe sind r plus sechs, nicht sechs.'}),
                  spr='Anzahl Reihen mal Stühle pro Reihe gibt alle Stühle: r mal Klammer r plus sechs gleich zweihundertsechzehn. '
                      'Die Unbekannte steht in beiden Faktoren: Die Gleichung ist quadratisch.',
                  el=[f(r'r \cdot (r + 6) = 216', 520, 48, x=RX, ein='@Anzahl'),
                      n('r in beiden Faktoren: quadratisch', 610, 'rot', 38, x=RX, ein='@Faktoren')]),
             dict(gegeben=[G_text(DR, 34), G_formel(r'r \cdot (r + 6) = 216')],
                  frage=dict(text='In Grundform: Was tippst du in poly-solv ein?', sprich='In Grundform: Was tippst du in poly-solv ein?',
                             opt=['a = 1, b = 6, c = −216', 'a = 1, b = 6, c = 216', 'a = 2, b = 6, c = −216'],
                             rueck={1: 'Die 216 kommt nach links. Welches Vorzeichen hat sie dort?', 2: 'r · r = r², also a = ?'},
                             rueck_sprich={1: 'Die zweihundertsechzehn kommt nach links. Welches Vorzeichen hat sie dort?',
                                           2: 'r mal r ist r Quadrat. Also ist a gleich?'}),
                  spr='Ausmultipliziert: r Quadrat plus sechs r gleich zweihundertsechzehn. Minus zweihundertsechzehn: r Quadrat plus sechs r '
                      'minus zweihundertsechzehn gleich null. Für poly-solv: a gleich eins, b gleich sechs, c gleich minus zweihundertsechzehn.',
                  el=[f(r'r^2 + 6 \cdot r = 216', 520, 44, x=RX, ein='@Ausmultipliziert'),
                      f(r'r^2 + 6 \cdot r - 216 = 0', 610, 46, x=RX, ein='@Minus'),
                      ] + poly_eingabe(1, 6, -216, 640, '@poly')),
             dict(gegeben=[G_text(DR, 34), G_formel(r'r^2 + 6 \cdot r - 216 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 12 und x2 = −18. Wie viele Reihen?',
                             sprich='poly-solv zeigt x eins gleich zwölf und x zwei gleich minus achtzehn. Wie viele Reihen sind es?',
                             opt=['12 Reihen', '12 oder −18 Reihen', '18 Reihen'],
                             rueck={1: 'Eine Anzahl Reihen ist nie negativ.', 2: '18 sind die Stühle pro Reihe.'},
                             rueck_sprich={2: 'Achtzehn sind die Stühle pro Reihe.'}),
                  spr='Eine Anzahl ist nie negativ, minus achtzehn fällt weg. Es sind zwölf Reihen mit je achtzehn Stühlen.',
                  el=ergebnis('x1=12', 'x2=⁻18') + [
                      tx(r'@\fd{r = -18}@: keine Anzahl', 760, 36, x=RX, ein='@negativ'),
                      f(r'r = \fc{12}', 850, 48, x=RX, ein='@Reihen')]),
             dict(gegeben=[G_text(DR, 34), G_formel(r'r = 12')],
                  frage=dict(text='Welche Probe prüft den Text?', sprich='Welche Probe prüft hier den Text?',
                             opt=['12 Reihen zu 18 Stühlen: 12 · 18 = 216', '12² + 6 · 12 − 216 = 0', '12 + 18 = 30'],
                             rueck={1: 'Das prüft die eigene Gleichung, nicht den Text.', 2: 'Im Text steht die Anzahl Stühle, keine Summe.'}),
                  spr='Probe am Text: zwölf Reihen, jede mit sechs Stühlen mehr, also achtzehn. Zwölf mal achtzehn gibt zweihundertsechzehn '
                      'Stühle. Es sind zwölf Reihen.',
                  el=[f(r'12 \cdot 18 = 216 \;\checkmark', 520, 44, x=RX, ein='@Probe'),
                      tx(r'Es sind @\fc{12}@ Reihen.', 610, 40, x=RX, ein='@sind#2')]),
         ]),
], merke('Zum Mitnehmen: Mit einer Unbekannten steckt die Stückbilanz im Term, etwa vierundzwanzig minus x. Steht die Unbekannte '
         'in beiden Faktoren von Anzahl mal Wert pro Stück, wird die Gleichung quadratisch. Negative Anzahlen fallen weg.',
         'Rest als Term: @24 - x@|Unbekannte in beiden Faktoren: quadratisch|negative Anzahlen verwerfen'),
   folge=8)

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle, zwei Unbekannte
DFW = [G_text(r'@\fa{x}@: Anzahl Personenwagen', 34), G_text(r'@\fb{y}@: Anzahl Lieferwagen', 34)]
DBU = [G_text(r'@\fa{x}@: Anzahl Angemeldete', 34), G_text(r'@\fb{y}@: geplanter Betrag pro Person in CHF', 34)]
kontrolle('kontrolle-verteilen-2', 'Ansatz finden: Verteilen mit zwei Unbekannten',
          'Zwei Verteilaufgaben Schritt für Schritt: Fahrzeuge auf der Fähre (lineares System, sys-solv) und Buskosten, die sich auf weniger Personen verteilen (quadratisches System, poly-solv).',
          ['Verteilungsaufgabe', 'lineares Gleichungssystem', 'quadratisches Gleichungssystem', 'sys-solv', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Verteilen',
         text='Eine Fähre bringt an einem Tag 70 Fahrzeuge|über den See: Personenwagen zu 30 CHF und|Lieferwagen zu 55 CHF. Die Einnahmen betragen|2600 CHF. Wie viele Lieferwagen waren es?',
         spr='Eine Fähre bringt an einem Tag siebzig Fahrzeuge über den See: Personenwagen zu dreissig Franken und Lieferwagen zu '
             'fünfundfünfzig Franken. Die Einnahmen betragen zweitausendsechshundert Franken. Wie viele Lieferwagen waren es?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration ist vollständig?', sprich='Welche Deklaration ist hier vollständig?',
                             opt=['x: Anzahl Personenwagen, y: Anzahl Lieferwagen', 'x: Personenwagen, y: Lieferwagen',
                                  'x, y: Preis je Personenwagen und Lieferwagen'],
                             rueck={1: 'Was von den Personenwagen: Anzahl, Preis, Einnahmen?', 2: 'Die Preise sind gegeben.'}),
                  spr='x ist die Anzahl Personenwagen, y die Anzahl Lieferwagen. Beides sind Stückzahlen.',
                  el=[tx(r'@\fa{x}@: Anzahl Personenwagen', 520, 40, x=RX, ein='@Anzahl'),
                      tx(r'@\fb{y}@: Anzahl Lieferwagen', 590, 40, x=RX, ein='@Anzahl#2')]),
             dict(gegeben=DFW,
                  frage=dict(text='Welches System übersetzt den Text?', sprich='Welches System übersetzt hier den Text?',
                             opt=['x + y = 70 und 30·x + 55·y = 2600', 'x + y = 2600 und 30·x + 55·y = 70', 'x + y = 70 und 55·x + 30·y = 2600'],
                             rueck={1: 'Was zählt die Stückbilanz: Fahrzeuge oder Franken?', 2: 'x zählt die Personenwagen. Welcher Preis gehört zu x?'}),
                  spr='Stückbilanz: x plus y gleich siebzig Fahrzeuge. Wertbilanz: dreissig x plus fünfundfünfzig y gleich '
                      'zweitausendsechshundert Franken.',
                  el=[f(r'\begin{cases} x + y = 70 & \text{(Fahrzeuge)} \\ 30 \cdot x + 55 \cdot y = 2600 & \text{(CHF)} \end{cases}', 520, 40, x=RX, ein='@Stückbilanz')]),
             dict(gegeben=DFW + [G_formel(r'\begin{cases} x + y = 70 \\ 30 \cdot x + 55 \cdot y = 2600 \end{cases}', 36, 110)],
                  frage=dict(text='Was tippst du in sys-solv ein?', sprich='Was tippst du in sys-solv ein?',
                             opt=['1, 1, 70 und 30, 55, 2600', '1, 1, 2600 und 30, 55, 70', '1, 1, 70 und 55, 30, 2600'],
                             rueck={1: 'Welche Zahl steht rechts in der Stückbilanz?', 2: 'In jeder Zeile zuerst der Faktor vor x, dann der vor y.'}),
                  spr='Beide Gleichungen sind schon geordnet: x, dann y, dann die Zahl. Erste Zeile eins, eins, siebzig. Zweite Zeile '
                      'dreissig, fünfundfünfzig, zweitausendsechshundert.',
                  el=[n('schon geordnet: x, y, Zahl', 520, 'blau', 40, x=RX, ein='@geordnet'),
                      ] + sys_eingabe((1, 1, 70), (30, 55, 2600), 640, '@Erste')),
             dict(gegeben=DFW + [G_formel(r'\begin{cases} x + y = 70 \\ 30 \cdot x + 55 \cdot y = 2600 \end{cases}', 36, 110)],
                  frage=dict(text='sys-solv zeigt x = 50 und y = 20. Was ist gefragt?',
                             sprich='sys-solv zeigt x gleich fünfzig und y gleich zwanzig. Was ist gefragt?',
                             opt=['20 Lieferwagen', '50 Lieferwagen', '70 Lieferwagen'],
                             rueck={1: 'x steht für die Personenwagen.', 2: '70 sind alle Fahrzeuge zusammen.'},
                             rueck_sprich={2: 'Siebzig sind alle Fahrzeuge zusammen.'}),
                  spr='y zählt die Lieferwagen: Es waren zwanzig Lieferwagen und fünfzig Personenwagen.',
                  el=ergebnis('x=50', 'y=20') + [
                      tx(r'@y = \fc{20}@ Lieferwagen', 760, 40, x=RX, ein='@zählt')]),
             dict(gegeben=DFW + [G_formel(r'x = 50,\ y = 20')],
                  frage=dict(text='Welche Probe prüft beide Angaben?', sprich='Welche Probe prüft beide Angaben?',
                             opt=['50 + 20 = 70; 1500 + 1100 = 2600', '50 + 20 = 70 genügt', '30 · 55 = 1650'],
                             rueck={1: 'Die Einnahmen gehören auch geprüft.', 2: 'Was hat das Produkt der Preise mit dem Text zu tun?'}),
                  spr='Probe am Text: fünfzig plus zwanzig gleich siebzig Fahrzeuge. Einnahmen: tausendfünfhundert plus tausendeinhundert '
                      'gleich zweitausendsechshundert Franken. Es waren zwanzig Lieferwagen.',
                  el=[f(r'50 + 20 = 70 \;\checkmark', 520, 42, x=RX, ein='@Probe'),
                      f(r'30 \cdot 50 + 55 \cdot 20 = 1500 + 1100 = 2600 \;\checkmark', 600, 38, x=RX, ein='@Einnahmen'),
                      tx(r'Es waren @\fc{20}@ Lieferwagen.', 690, 40, x=RX, ein='@waren')]),
         ]),
    dict(nr=2, kurz='Verteilen',
         text='Eine Gruppe mietet einen Bus für 360 CHF und|teilt die Kosten gleichmässig. Weil 3 Personen|absagen, muss jede andere Person 6 CHF mehr|bezahlen. Wie viele Personen waren angemeldet?',
         spr='Eine Gruppe mietet einen Bus für dreihundertsechzig Franken und teilt die Kosten gleichmässig. Weil drei Personen '
             'absagen, muss jede andere Person sechs Franken mehr bezahlen. Wie viele Personen waren angemeldet?',
         schritte=[
             dict(frage=dict(text='Was ist hier unbekannt?', sprich='Was ist hier unbekannt?',
                             opt=['x: Angemeldete (Anzahl), y: CHF pro Person', 'x: Anzahl Personen, y: Gesamtkosten in CHF', 'x: Anzahl, die absagen'],
                             rueck={1: 'Die Gesamtkosten sind gegeben: 360 CHF.', 2: 'Wie viele absagen, steht im Text: 3.'},
                             rueck_sprich={1: 'Die Gesamtkosten sind gegeben: dreihundertsechzig Franken.',
                                           2: 'Wie viele absagen, steht im Text: drei.'}),
                  spr='x ist die Anzahl Angemeldete, y der Betrag, den jede Person ursprünglich bezahlen sollte, in Franken.',
                  el=[tx(r'@\fa{x}@: Anzahl Angemeldete', 520, 40, x=RX, ein='@Anzahl'),
                      tx(r'@\fb{y}@: geplanter Betrag pro Person in CHF', 590, 40, x=RX, ein='@Betrag')]),
             dict(gegeben=DBU,
                  frage=dict(text='Welches System beschreibt die Kosten?', sprich='Welches System beschreibt die Kosten?',
                             opt=['x·y = 360 und (x − 3)·(y + 6) = 360', 'x·y = 360 und (x + 3)·(y − 6) = 360', 'x + y = 360 und (x − 3) + (y + 6) = 360'],
                             rueck={1: 'Es kommen weniger Personen, und jede zahlt mehr.', 2: 'Anzahl mal Betrag pro Person gibt die Kosten.'}),
                  spr='Anzahl mal Betrag pro Person gibt die Kosten: x mal y gleich dreihundertsechzig. Nach den Absagen: x minus drei '
                      'Personen zahlen je y plus sechs Franken, wieder dreihundertsechzig. Ein Produkt der Unbekannten: quadratisch.',
                  el=[f(r'\begin{cases} x \cdot y = 360 \\ (x - 3) \cdot (y + 6) = 360 \end{cases}', 520, 42, x=RX, ein='@Kosten'),
                      n('Produkt der Unbekannten: quadratisch', 700, 'rot', 38, x=RX, ein='@Produkt')]),
             dict(gegeben=DBU + [G_formel(r'\begin{cases} x \cdot y = 360 \\ (x - 3) \cdot (y + 6) = 360 \end{cases}', 36, 110)],
                  frage=dict(text='y = 2·x − 6 eingesetzt: Welche Grundform entsteht?',
                             sprich='y gleich zwei x minus sechs eingesetzt: Welche Grundform entsteht?',
                             opt=['2·x² − 6·x − 360 = 0', '2·x² − 6·x + 360 = 0', '2·x² + 6·x − 360 = 0'],
                             rueck={1: 'Prüfe das Vorzeichen der 360.', 2: 'Prüfe das Vorzeichen in y = 2·x − 6.'},
                             rueck_sprich={1: 'Prüfe das Vorzeichen der dreihundertsechzig.', 2: 'Prüfe das Vorzeichen in y gleich zwei x minus sechs.'}),
                  spr='Ausmultipliziert: x y plus sechs x minus drei y minus achtzehn gleich dreihundertsechzig. Mit x y gleich '
                      'dreihundertsechzig bleibt sechs x minus drei y gleich achtzehn, also y gleich zwei x minus sechs. Eingesetzt: zwei x '
                      'Quadrat minus sechs x minus dreihundertsechzig gleich null.',
                  el=[f(r'x y + 6 \cdot x - 3 \cdot y - 18 = 360', 520, 38, x=RX, ein='@Ausmultipliziert'),
                      f(r'6 \cdot x - 3 \cdot y = 18 \;\Rightarrow\; y = 2 \cdot x - 6', 590, 38, x=RX, ein='@bleibt'),
                      f(r'x \cdot (2 \cdot x - 6) = 360', 660, 38, x=RX, ein='@Eingesetzt'),
                      f(r'2 \cdot x^2 - 6 \cdot x - 360 = 0', 740, 44, x=RX, ein='@Quadrat'),
                      ] + poly_eingabe(2, -6, -360, 640, '@Quadrat+1')),
             dict(gegeben=DBU + [G_formel(r'2 \cdot x^2 - 6 \cdot x - 360 = 0')],
                  frage=dict(text='poly-solv zeigt x1 = 15 und x2 = −12. Was folgt?',
                             sprich='poly-solv zeigt x eins gleich fünfzehn und x zwei gleich minus zwölf. Was folgt daraus?',
                             opt=['15 Personen', '15 oder −12 Personen', '12 Personen'],
                             rueck={1: 'Eine Anzahl Personen ist nie negativ.', 2: '12 fahren nach den Absagen mit. Gefragt sind die Angemeldeten.'},
                             rueck_sprich={2: 'Zwölf fahren nach den Absagen mit. Gefragt sind die Angemeldeten.'}),
                  spr='Eine Anzahl ist nie negativ, minus zwölf fällt weg. Angemeldet waren fünfzehn Personen, und y gleich zwei mal '
                      'fünfzehn minus sechs gleich vierundzwanzig Franken.',
                  el=ergebnis('x1=15', 'x2=⁻12') + [
                      tx(r'@\fd{x = -12}@: keine Anzahl', 760, 36, x=RX, ein='@negativ'),
                      f(r'x = \fc{15}, \quad y = 2 \cdot 15 - 6 = 24', 850, 42, x=RX, ein='@Angemeldet')]),
             dict(gegeben=DBU + [G_formel(r'x = 15,\ y = 24')],
                  frage=dict(text='Probe: Was prüft vor und nach den Absagen?', sprich='Probe: Was prüft die Kosten vor und nach den Absagen?',
                             opt=['15 · 24 = 360 und 12 · 30 = 360', '15 · 24 = 360 genügt', '15 − 3 = 12'],
                             rueck={1: 'Und nach den Absagen? Prüfe beide Aussagen.', 2: 'Das prüft die Kosten nicht.'}),
                  spr='Probe am Text: fünfzehn mal vierundzwanzig gleich dreihundertsechzig. Nach drei Absagen zahlen zwölf Personen je '
                      'dreissig Franken, sechs mehr, und zwölf mal dreissig ist wieder dreihundertsechzig. Angemeldet waren fünfzehn Personen.',
                  el=[f(r'15 \cdot 24 = 360 \;\checkmark \qquad 12 \cdot 30 = 360 \;\checkmark', 520, 40, x=RX, ein='@Probe'),
                      tx(r'Angemeldet waren @\fc{15}@ Personen.', 610, 40, x=RX, ein='@Angemeldet')]),
         ]),
], merke('Zum Mitnehmen: Stückbilanz und Wertbilanz mit festen Preisen geben ein lineares System für sys-solv. Sind Anzahl und Betrag '
         'pro Stück beide unbekannt, entsteht ein Produkt: ausmultiplizieren, eine Unbekannte durch die andere ausdrücken, einsetzen, '
         'Grundform, poly-solv.',
         'feste Preise: lineares System, sys-solv|Anzahl und Betrag unbekannt: quadratisch|negative Anzahlen verwerfen'),
   folge=9)


# ════════════════════════════════════════════════ Kapitel 4 · Einführung
def zinsbild(ein=0.05, zins=False, ein_z=None):
    """Kapital (in tausend CHF) und Zins (1 Einheit = 15 CHF) als Säulen; x blau, y orange."""
    fig = [{'art': 'vieleck', 'punkte': [[2, 0], [7, 0], [7, 14], [2, 14]], 'farbe': 1, 'fuellung': 0.3, 'dicke': 3},
           {'art': 'vieleck', 'punkte': [[2, 14], [7, 14], [7, 30], [2, 30]], 'farbe': 2, 'fuellung': 0.3, 'dicke': 3},
           {'art': 'text', 'bei': [4.5, 7], 'text': 'x', 'farbe': 1, 'groesse': 40},
           {'art': 'text', 'bei': [4.5, 22], 'text': 'y', 'farbe': 2, 'groesse': 40},
           {'art': 'text', 'bei': [4.5, -2.4], 'text': 'Kapital 30 000', 'farbe': 5, 'groesse': 30, 'kursiv': False}]
    if zins:
        e = ein_z or 0.05
        fig += [{'art': 'vieleck', 'punkte': [[13, 0], [18, 0], [18, 7], [13, 7]], 'farbe': 1, 'fuellung': 0.55, 'dicke': 3, 'ein': e},
                {'art': 'vieleck', 'punkte': [[13, 7], [18, 7], [18, 28.33], [13, 28.33]], 'farbe': 2, 'fuellung': 0.55, 'dicke': 3, 'ein': e},
                {'art': 'text', 'bei': [15.5, 3.2], 'text': '0.0075·x', 'farbe': 5, 'groesse': 26, 'ein': e},
                {'art': 'text', 'bei': [15.5, 17.5], 'text': '0.02·y', 'farbe': 5, 'groesse': 26, 'ein': e},
                {'art': 'text', 'bei': [15.5, -2.4], 'text': 'Zins 425', 'farbe': 5, 'groesse': 30, 'kursiv': False, 'ein': e}]
    return dict(typ='graf', x=RX + 60, y=170, breite=600, hoehe=780, abstand=0, anim='fade', ein=ein, achsen=False, raster=False,
                xbereich=[0, 20.5], ybereich=[-4.6, 32], figuren=fig)


clip('zins', 'Ansatz finden: Zins',
     'Kapitalgleichung und Zinsgleichung an zwei Anlagen: Zins ist Zinssatz mal Zeit mal Kapital. Dazu der Zeitanteil, der Zinseszins und wann es quadratisch wird.',
     ['Zinsaufgabe', 'Kapitalgleichung', 'Zinsgleichung', 'Zeitanteil', 'Zinseszins', 'poly-solv'], [
         sz('Zins',
            'Der Zins ist Zinssatz mal Zeit mal Kapital. Der Zinssatz steht als Dezimalzahl: zwei Prozent sind null Komma null zwei. '
            'Die Zeit zählt in Jahren: ein halbes Jahr ist ein halb, vier Monate sind ein Drittel.',
            titel('Zins', 250, 70),
            f(r'\text{Zins} = p \cdot t \cdot \text{Kapital}', 380, 54, ein='@Zinssatz'),
            f(r'2\,\% \;\to\; p = 0.02', 490, 44, ein='@Dezimalzahl'),
            f(r'\tfrac{1}{2}\ \text{Jahr} \;\to\; t = \tfrac{1}{2} \qquad 4\ \text{Monate} \;\to\; t = \tfrac{4}{12} = \tfrac{1}{3}', 580, 44, ein='@Jahren')),
         sz('Zwei Anlagen',
            'Herr Keller legt dreissigtausend Franken an: einen Teil auf ein Sparkonto zu null Komma sieben fünf Prozent, den Rest in '
            'eine Kassenobligation zu zwei Prozent. Nach einem Jahr erhält er vierhundertfünfundzwanzig Franken Zins. x und y sind die '
            'beiden Kapitalien in Franken.',
            tx('30 000 CHF: Sparkonto 0.75 %, Rest 2 %;|Zins nach einem Jahr 425 CHF', 240, 40, ein=0.4),
            tx(r'@\fa{x}@: Kapital auf dem Sparkonto in CHF', 360, 38, ein='@Kapitalien'),
            tx(r'@\fb{y}@: Kapital in der Obligation in CHF', 430, 38, ein='@Kapitalien+0.6'),
            zinsbild(ein=0.6)),
         sz('Kapital und Zins',
            'Die Kapitalgleichung zählt Franken Kapital: x plus y gleich dreissigtausend. Die Zinsgleichung zählt Franken Zins: '
            'null Komma null null sieben fünf x plus null Komma null zwei y gleich vierhundertfünfundzwanzig. Links und rechts steht '
            'jedes Mal dieselbe Grösse.',
            f(r'\fa{x} + \fb{y} = 30\,000', 280, 50, ein='@Kapitalgleichung'),
            n('Kapitalgleichung: CHF Kapital', 370, 'blau', 38, ein='@Kapitalgleichung'),
            f(r'0.0075 \cdot \fa{x} + 0.02 \cdot \fb{y} = 425', 470, 46, ein='@Zinsgleichung'),
            n('Zinsgleichung: CHF Zins', 560, 'blau', 38, ein='@Zinsgleichung'),
            zinsbild(zins=True, ein_z='@Zinsgleichung')),
         sz('Lösen',
            'Hier geht es auch von Hand, mit Einsetzen: x gleich dreissigtausend minus y. Dann bleibt zweihundertfünfundzwanzig plus '
            'null Komma null eins zwei fünf y gleich vierhundertfünfundzwanzig, also y gleich sechzehntausend und x gleich vierzehntausend. '
            'Probe: hundertfünf plus dreihundertzwanzig gleich vierhundertfünfundzwanzig Franken.',
            f(r'x = 30\,000 - y', 260, 46, ein='@Einsetzen'),
            f(r'225 + 0.0125 \cdot y = 425', 350, 46, ein='@bleibt'),
            f(r'y = \fc{16\,000}, \quad x = \fc{14\,000}', 440, 46, ein='@sechzehntausend'),
            f(r'0.0075 \cdot 14\,000 + 0.02 \cdot 16\,000 = 105 + 320 = 425 \;\checkmark', 560, 38, ein='@Probe'),
            zinsbild(zins=True)),
         sz('Zeitanteil',
            'Liegt ein Teil nur ein halbes Jahr, kommt der Zeitanteil dazu. Ein Beispiel von der Themenseite: null Komma acht Prozent ein '
            'ganzes Jahr und zwei Komma vier Prozent ein halbes Jahr. In der Zinsgleichung steht dann null Komma null zwei vier mal '
            'ein halb, also null Komma null eins zwei.',
            tx('20 000 CHF: Teil 1 ein Jahr zu 0.8 %,|Teil 2 ein halbes Jahr zu 2.4 %; Zins 212 CHF', 240, 40, ein=0.4),
            f(r'0.008 \cdot 1 \cdot x + 0.024 \cdot \tfrac{1}{2} \cdot y = 212', 400, 46, ein='@Zinsgleichung'),
            f(r'0.024 \cdot \tfrac{1}{2} = 0.012', 500, 46, ein='@also'),
            n('Zeitanteil nie vergessen', 620, 'rot', 42, ein='@Zeitanteil')),
         sz('Zinseszins',
            'Wird der Zins gutgeschrieben und im nächsten Jahr mitverzinst, wächst das Kapital jedes Jahr mit dem Faktor eins plus p. '
            'Nach zwei Jahren steht das Kapital mal eins plus p im Quadrat da. Bei drei Prozent werden aus fünftausend Franken '
            'fünftausendhundertfünfzig und dann fünftausenddreihundertvier Franken fünfzig.',
            titel('Zinseszins', 250, 66),
            f(r'K \;\to\; K \cdot (1 + p) \;\to\; K \cdot (1 + p)^2', 390, 50, ein='@wächst'),
            f(r'5000 \;\to\; 5150 \;\to\; 5304.50 \qquad (p = 0.03)', 500, 44, ein='@drei'),
            n('Faktor @1 + p@ mit @p@ als Dezimalzahl', 620, 'blau', 40, ein='@Faktor')),
         sz('Quadratisch',
            'Ist der Zinssatz gesucht, steht p im Quadrat. Aus fünftausend mal Klammer eins plus p im Quadrat gleich fünftausenddreihundertvier '
            'Komma fünf wird die Grundform fünftausend p Quadrat plus zehntausend p minus dreihundertvier Komma fünf gleich null. '
            'poly-solv liefert drei Hundertstel und minus zweihundertdrei Hundertstel. Nur p gleich null Komma null drei passt: drei Prozent.',
            f(r'5000 \cdot (1 + p)^2 = 5304.50', 260, 46, ein='@Klammer'),
            f(r'5000 \cdot p^2 + 10\,000 \cdot p - 304.5 = 0', 360, 46, ein='@Grundform'),
            rechner(['x1=[3|100]', ''], ['enter'], 470, '@liefert', LX, 400),
            rechner(['x2=⁻[203|100]', ''], ['enter'], 470, '@liefert+0.8', LX + 420, 400),
            tx(r'@p = \fc{0.03} = 3\,\%@; @\fd{p = -2.03}@ verworfen', 770, 40, ein='@passt'),
            n('Auch Kapital mal Zinssatz,|beide unbekannt, ist ein Produkt:|quadratisch.', 470, 'rot', 40, ein='@Prozent#2', x=RX)),
         sz('Merke',
            'Zum Mitnehmen: Kapitalgleichung und Zinsgleichung, beide in Franken. Der Zinssatz als Dezimalzahl, die Zeit in Jahren. '
            'Mit Zinseszins wächst das Kapital mit dem Faktor eins plus p pro Jahr.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'x + y = K \qquad p_1 \cdot t_1 \cdot x + p_2 \cdot t_2 \cdot y = Z', 390, 48, ein=1.2),
            n('Zinssatz als Dezimalzahl, Zeit in Jahren|Zinseszins: Faktor @1 + p@ pro Jahr', 500, 'blau', 46, ein='@Dezimalzahl')),
         JETZT_DU,
     ], folge=10)

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle, eine Unbekannte
DZ1 = r'@\fa{x}@: Kapital zu 1.5 % in CHF; Rest @12\,000 - x@'
DZ2 = r'@\fb{p}@: Jahreszinssatz als Dezimalzahl'
kontrolle('kontrolle-zins-1', 'Ansatz finden: Zins mit einer Unbekannten',
          'Zwei Zinsaufgaben Schritt für Schritt: zwei Anlagen mit Zeitanteil (linear) und Zinseszins mit einer Einzahlung (quadratisch, poly-solv).',
          ['Zinsaufgabe', 'Zeitanteil', 'Zinseszins', 'lineare Gleichung', 'quadratische Gleichung', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Zins',
         text='Lea teilt 12 000 CHF auf. Einen Teil legt sie|ein ganzes Jahr zu 1.5 % an, den Rest nur ein|halbes Jahr zu 2 %. Zusammen erhält sie|160 CHF Zins. Wie viel legt sie zu 1.5 % an?',
         spr='Lea teilt zwölftausend Franken auf. Einen Teil legt sie ein ganzes Jahr zu eins Komma fünf Prozent an, den Rest nur ein '
             'halbes Jahr zu zwei Prozent. Zusammen erhält sie hundertsechzig Franken Zins. Wie viel legt sie zu eins Komma fünf Prozent an?',
         schritte=[
             dict(frage=dict(text='Mit einer Unbekannten: Welche Deklaration?', sprich='Mit einer Unbekannten: Welche Deklaration passt?',
                             opt=['x: Kapital zu 1.5 % in CHF; Rest 12' + NB + '000 − x', 'x: Zins in CHF', 'x: Zinssatz des Rests'],
                             rueck={1: 'Der Zins ist gegeben: 160 CHF.', 2: 'Die Zinssätze sind gegeben.'},
                             rueck_sprich={1: 'Der Zins ist gegeben: hundertsechzig Franken.'}),
                  spr='x ist das Kapital zu eins Komma fünf Prozent in Franken. Der Rest, zwölftausend minus x, liegt zu zwei Prozent.',
                  el=[tx(r'@\fa{x}@: Kapital zu 1.5 % in CHF', 520, 40, x=RX, ein='@Kapital'),
                      tx(r'Rest: @12\,000 - x@', 600, 40, x=RX, ein='@Rest')]),
             dict(gegeben=[G_text(DZ1, 34)],
                  frage=dict(text='Welche Zinsgleichung stimmt?', sprich='Welche Zinsgleichung stimmt?',
                             opt=['0.015·x + 0.02·½·(12' + NB + '000 − x) = 160', '0.015·x + 0.02·(12' + NB + '000 − x) = 160',
                                  '1.5·x + 2·½·(12' + NB + '000 − x) = 160'],
                             rueck={1: 'Der Rest liegt nur ein halbes Jahr. Was fehlt?', 2: 'Zinssätze als Dezimalzahl: 1.5 % sind 0.015.'},
                             rueck_sprich={2: 'Zinssätze als Dezimalzahl: eins Komma fünf Prozent sind null Komma null eins fünf.'}),
                  spr='Zins gleich Zinssatz mal Zeit mal Kapital. Das erste Kapital ein Jahr zu null Komma null eins fünf, der Rest ein '
                      'halbes Jahr zu null Komma null zwei. Zusammen hundertsechzig Franken.',
                  el=[f(r'0.015 \cdot 1 \cdot x + 0.02 \cdot \tfrac{1}{2} \cdot (12\,000 - x) = 160', 520, 38, x=RX, ein='@Zinssatz'),
                      n('Zeitanteil: @t = \\tfrac{1}{2}@', 610, 'blau', 38, x=RX, ein='@halbes')]),
             dict(gegeben=[G_text(DZ1, 34), G_formel(r'0.015 \cdot x + 0.01 \cdot (12\,000 - x) = 160', 36)],
                  frage=dict(text='Ausmultipliziert und geordnet: Was bleibt?', sprich='Ausmultipliziert und geordnet: Was bleibt übrig?',
                             opt=['0.005·x = 40', '0.005·x = 160', '0.025·x = 40'],
                             rueck={1: 'Was ist mit 0.01 · 12 000 = 120 passiert?', 2: 'Das Minus vor 0.01·x: 0.015·x − 0.01·x = ?'},
                             rueck_sprich={1: 'Was ist mit null Komma null eins mal zwölftausend, also hundertzwanzig, passiert?',
                                           2: 'Das Minus vor null Komma null eins x: null Komma null eins fünf x minus null Komma null eins x gleich?'}),
                  spr='Der Faktor des Rests: null Komma null zwei mal ein halb gleich null Komma null eins. Ausmultipliziert null Komma null '
                      'eins fünf x plus hundertzwanzig minus null Komma null eins x gleich hundertsechzig. Also null Komma null null fünf x '
                      'gleich vierzig.',
                  el=[f(r'0.015 \cdot x + 120 - 0.01 \cdot x = 160', 520, 42, x=RX, ein='@Ausmultipliziert'),
                      f(r'0.005 \cdot x = 40', 610, 44, x=RX, ein='@Also')]),
             dict(gegeben=[G_text(DZ1, 34), G_formel(r'0.005 \cdot x = 40')],
                  frage=dict(text='Welcher Typ, und was ergibt sich daraus?', sprich='Welcher Typ, und was ergibt sich daraus?',
                             opt=['linear: x = 40 : 0.005 = 8000', 'linear: x = 40 · 0.005 = 0.2', 'quadratisch: poly-solv'],
                             rueck={1: 'Damit x allein steht: mal 0.005 oder durch 0.005?', 2: 'Kommt x im Quadrat vor?'},
                             rueck_sprich={1: 'Damit x allein steht: mal null Komma null null fünf oder durch null Komma null null fünf?'}),
                  spr='Eine Unbekannte und kein Quadrat: linear. Durch null Komma null null fünf teilen: x gleich achttausend.',
                  el=[n('linear: von Hand lösen', 520, 'blau', 40, x=RX, ein='@linear'),
                      f(r'x = 40 : 0.005 = \fc{8000}', 610, 48, x=RX, ein='@teilen')]),
             dict(gegeben=[G_text(DZ1, 34), G_formel(r'x = 8000')],
                  frage=dict(text='Wie lautet die Antwort mit Probe?', sprich='Wie lautet die Antwort?',
                             opt=['8000 CHF zu 1.5 %, 4000 CHF zu 2 %', '8000 CHF Zins', '4000 CHF zu 1.5 %'],
                             rueck={1: 'x ist ein Kapital, kein Zins.', 2: '4000 ist der Rest.'},
                             rueck_sprich={2: 'Viertausend ist der Rest.'}),
                  spr='Lea legt achttausend Franken zu eins Komma fünf Prozent an und viertausend zu zwei Prozent. Probe am Text: '
                      'hundertzwanzig Franken plus vierzig Franken für das halbe Jahr gibt hundertsechzig Franken.',
                  el=[tx(r'@\fc{8000}@ CHF zu 1.5 %, @4000@ CHF zu 2 %', 520, 40, x=RX, ein='@legt'),
                      f(r'0.015 \cdot 8000 + 0.02 \cdot \tfrac{1}{2} \cdot 4000 = 120 + 40 = 160 \;\checkmark', 610, 36, x=RX, ein='@Probe')]),
         ]),
    dict(nr=2, kurz='Zins',
         text='Mia zahlt 5000 CHF auf ein Konto ein und nach|einem Jahr nochmals 2000 CHF. Der Zins wird|jährlich gutgeschrieben und mitverzinst; der|Zinssatz bleibt gleich. Nach zwei Jahren sind es|7242 CHF. Wie hoch ist der Zinssatz?',
         spr='Mia zahlt fünftausend Franken auf ein Konto ein und nach einem Jahr nochmals zweitausend Franken. Der Zins wird jährlich '
             'gutgeschrieben und mitverzinst, der Zinssatz bleibt gleich. Nach zwei Jahren sind es siebentausendzweihundertzweiundvierzig '
             'Franken. Wie hoch ist der Zinssatz?',
         schritte=[
             dict(frage=dict(text='Was ist hier die Unbekannte?', sprich='Was ist hier die Unbekannte?',
                             opt=['p: Jahreszinssatz als Dezimalzahl', 'p: Zins nach zwei Jahren in CHF', 'p: Kapital nach einem Jahr in CHF'],
                             rueck={1: 'Gefragt ist der Zinssatz, nicht der Zins.', 2: 'Das Kapital nach einem Jahr ist ein Zwischenwert. Gefragt ist der Zinssatz.'}),
                  spr='p ist der Jahreszinssatz als Dezimalzahl. Mit Zinseszins wächst jedes Kapital pro Jahr mit dem Faktor eins plus p.',
                  el=[tx(DZ2, 520, 40, x=RX, ein='@Jahreszinssatz'),
                      n('pro Jahr: Faktor @1 + p@', 610, 'blau', 38, x=RX, ein='@Faktor')]),
             dict(gegeben=[G_text(DZ2, 34)],
                  frage=dict(text='Welche Gleichung beschreibt das Konto?', sprich='Welche Gleichung beschreibt das Konto?',
                             opt=['5000·(1 + p)² + 2000·(1 + p) = 7242', '7000·(1 + p)² = 7242', '5000·(1 + 2·p) + 2000·(1 + p) = 7242'],
                             rueck={1: 'Die 2000 CHF liegen nur ein Jahr auf dem Konto.', 2: 'Der Zins wird mitverzinst: Zinseszins, nicht einfacher Zins.'},
                             rueck_sprich={1: 'Die zweitausend Franken liegen nur ein Jahr auf dem Konto.'}),
                  spr='Die fünftausend Franken wachsen zwei Jahre lang, die zweitausend nur ein Jahr: fünftausend mal Klammer eins plus p '
                      'im Quadrat plus zweitausend mal Klammer eins plus p gleich siebentausendzweihundertzweiundvierzig.',
                  el=[f(r'5000 \cdot (1 + p)^2 + 2000 \cdot (1 + p) = 7242', 520, 40, x=RX, ein='@wachsen'),
                      n('5000 zwei Jahre, 2000 ein Jahr', 610, 'blau', 38, x=RX, ein='@zweitausend')]),
             dict(gegeben=[G_text(DZ2, 34), G_formel(r'5000 \cdot (1 + p)^2 + 2000 \cdot (1 + p) = 7242', 36)],
                  frage=dict(text='Ausmultipliziert, auf null: Was tippst du ein?', sprich='Ausmultipliziert und auf null gebracht: Was tippst du ein?',
                             opt=['a = 5000, b = 12' + NB + '000, c = −242', 'a = 5000, b = 10' + NB + '000, c = −242', 'a = 5000, b = 12' + NB + '000, c = 7242'],
                             rueck={1: 'Auch 2000·(1 + p) liefert ein Glied mit p.', 2: 'Die 7242 kommt nach links, zusammen mit 5000 + 2000.'},
                             rueck_sprich={1: 'Auch zweitausend mal Klammer eins plus p liefert ein Glied mit p.',
                                           2: 'Die siebentausendzweihundertzweiundvierzig kommt nach links, zusammen mit fünftausend plus zweitausend.'}),
                  spr='Ausmultipliziert: fünftausend p Quadrat plus zehntausend p plus fünftausend, dazu zweitausend p plus zweitausend. '
                      'Zusammen fünftausend p Quadrat plus zwölftausend p plus siebentausend. Minus siebentausendzweihundertzweiundvierzig: '
                      'c gleich minus zweihundertzweiundvierzig.',
                  el=[f(r'5000 \cdot p^2 + 10\,000 \cdot p + 5000 + 2000 \cdot p + 2000 = 7242', 520, 34, x=RX, ein='@Ausmultipliziert'),
                      f(r'5000 \cdot p^2 + 12\,000 \cdot p - 242 = 0', 610, 42, x=RX, ein='@Minus'),
                      ] + poly_eingabe(5000, 12000, -242, 640, '@Minus+1')),
             dict(gegeben=[G_text(DZ2, 34), G_formel(r'5000 \cdot p^2 + 12\,000 \cdot p - 242 = 0', 38)],
                  frage=dict(text='poly-solv zeigt x1 = 1/50 und x2 = −121/50. Was gilt?',
                             sprich='poly-solv zeigt x eins gleich ein Fünfzigstel und x zwei gleich minus hunderteinundzwanzig Fünfzigstel. Was gilt?',
                             opt=['p = 0.02, also 2 %', 'p = 0.02 %', 'p = −2.42'],
                             rueck={1: '0.02 als Prozent: mal 100.', 2: 'Ein Zinssatz von −242 % würde das Konto mehr als leeren.'},
                             rueck_sprich={1: 'Null Komma null zwei als Prozent: mal hundert.',
                                           2: 'Ein Zinssatz von minus zweihundertzweiundvierzig Prozent würde das Konto mehr als leeren.'}),
                  spr='Mit der Umschalttaste zeigt der Rechner Dezimalzahlen: null Komma null zwei und minus zwei Komma vier zwei. Ein Zinssatz '
                      'von minus zweihundertzweiundvierzig Prozent passt nicht. Also p gleich null Komma null zwei: zwei Prozent.',
                  el=ergebnis('x1=[1|50]', 'x2=⁻[121|50]') + [
                      rechner(['x1=0.02', '', ''], ['↔'], 515, '@Umschalttaste', RX, 400),
                      rechner(['x2=⁻2.42', '', ''], ['↔'], 515, '@Umschalttaste+0.6', RX + 420, 400),
                      tx(r'@\fd{p = -2.42}@: kein Zinssatz', 760, 36, x=RX, ein='@passt'),
                      f(r'p = \fc{0.02} = 2\,\%', 850, 46, x=RX, ein='@Also')]),
             dict(gegeben=[G_text(DZ2, 34), G_formel(r'p = 0.02')],
                  frage=dict(text='Welche Probe am Text stimmt?', sprich='Welche Probe am Text stimmt?',
                             opt=['5000 → 5100; + 2000 → 7100 → 7242', '5000 · 1.02 = 5100', '2000 · 1.02 = 2040'],
                             rueck={1: 'Das ist erst das erste Jahr.', 2: 'Das ist nur die zweite Einzahlung.'}),
                  spr='Probe am Text: Nach einem Jahr sind es fünftausendeinhundert Franken, mit der Einzahlung siebentausendeinhundert. Im '
                      'zweiten Jahr kommen zwei Prozent dazu: siebentausendzweihundertzweiundvierzig. Der Zinssatz beträgt zwei Prozent.',
                  el=[f(r'5000 \cdot 1.02 = 5100;\quad 7100 \cdot 1.02 = 7242 \;\checkmark', 520, 40, x=RX, ein='@Probe'),
                      tx(r'Der Zinssatz beträgt @\fc{2\,\%}@.', 610, 40, x=RX, ein='@beträgt')]),
         ]),
], merke('Zum Mitnehmen: Mit einer Unbekannten steht der Rest als Term, etwa zwölftausend minus x. Zinssatz als Dezimalzahl, Zeit in '
         'Jahren. Mit Zinseszins wächst jedes Kapital mit dem Faktor eins plus p pro Jahr; ist p gesucht, wird die Gleichung quadratisch. '
         'Die Umschalttaste zeigt Brüche als Dezimalzahl.',
         'Rest als Term|Zinseszins, @p@ gesucht: quadratisch|Umschalttaste ↔: Bruch oder Dezimalzahl'),
   folge=11)

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle, zwei Unbekannte
DV = [G_text(r'@\fa{x}@: Kapital zu 2 % in CHF', 34), G_text(r'@\fb{y}@: Kapital zu 3 % in CHF', 34)]
DK = [G_text(r'@\fa{K}@: Kapital in CHF', 34), G_text(r'@\fb{p}@: Zinssatz (Dezimalzahl)', 34)]
kontrolle('kontrolle-zins-2', 'Ansatz finden: Zins mit zwei Unbekannten',
          'Zwei Zinsaufgaben Schritt für Schritt: vertauschte Zinssätze (lineares System, sys-solv) und Kapital und Zinssatz zugleich unbekannt (quadratisches System, poly-solv).',
          ['Zinsaufgabe', 'lineares Gleichungssystem', 'quadratisches Gleichungssystem', 'sys-solv', 'poly-solv', 'Kontrollfragen'], [
    dict(nr=1, kurz='Zins',
         text='Zwei Kapitalien bringen in einem Jahr zu 2 %|und zu 3 % zusammen 540 CHF Zins. Wären die|Zinssätze vertauscht, gäbe es 510 CHF Zins.|Wie gross sind die beiden Kapitalien?',
         spr='Zwei Kapitalien bringen in einem Jahr zu zwei Prozent und zu drei Prozent zusammen fünfhundertvierzig Franken Zins. Wären '
             'die Zinssätze vertauscht, gäbe es fünfhundertzehn Franken Zins. Wie gross sind die beiden Kapitalien?',
         schritte=[
             dict(frage=dict(text='Welche Deklaration führt hier zum Ziel?', sprich='Welche Deklaration führt hier zum Ziel?',
                             opt=['x: Kapital zu 2 %, y: Kapital zu 3 % (CHF)', 'x: Zins zu 2 %, y: Zins zu 3 %', 'x: Kapital, y: Zinssatz'],
                             rueck={1: 'Gefragt sind die Kapitalien, nicht die Zinsen.', 2: 'Die Zinssätze sind gegeben: 2 % und 3 %.'},
                             rueck_sprich={2: 'Die Zinssätze sind gegeben: zwei und drei Prozent.'}),
                  spr='x ist das Kapital, das zu zwei Prozent angelegt ist, y das Kapital zu drei Prozent, beide in Franken.',
                  el=[tx(r'@\fa{x}@: Kapital zu 2 % in CHF', 520, 40, x=RX, ein='@Kapital'),
                      tx(r'@\fb{y}@: Kapital zu 3 % in CHF', 590, 40, x=RX, ein='@Kapital#2')]),
             dict(gegeben=DV + [G_formel(r'0.02 \cdot x + 0.03 \cdot y = 540', 36)],
                  frage=dict(text='Welche Gleichung beschreibt «vertauscht»?', sprich='Welche Gleichung beschreibt: Zinssätze vertauscht?',
                             opt=['0.03·x + 0.02·y = 510', '0.02·x + 0.03·y = 510', '0.03·y + 0.02·x = 510'],
                             rueck={1: 'Das sind die ursprünglichen Zinssätze.', 2: 'Das ist dieselbe Verteilung wie im ersten Satz, nur anders geordnet.'}),
                  spr='Die erste Aussage steht schon da. Vertauscht bekommt x drei Prozent und y zwei Prozent: null Komma null drei x plus '
                      'null Komma null zwei y gleich fünfhundertzehn. Zwei Zinsgleichungen, keine Kapitalgleichung.',
                  el=[f(r'\begin{cases} 0.02 \cdot x + 0.03 \cdot y = 540 \\ 0.03 \cdot x + 0.02 \cdot y = 510 \end{cases}', 520, 40, x=RX, ein='@Vertauscht'),
                      n('zwei Zinsgleichungen', 700, 'blau', 38, x=RX, ein='@Zinsgleichungen')]),
             dict(gegeben=DV + [G_formel(r'\begin{cases} 0.02 \cdot x + 0.03 \cdot y = 540 \\ 0.03 \cdot x + 0.02 \cdot y = 510 \end{cases}', 34, 110)],
                  frage=dict(text='Mit 100 multipliziert: Was tippst du ein?', sprich='Mit hundert multipliziert: Was tippst du ein?',
                             opt=['2, 3, 54' + NB + '000 und 3, 2, 51' + NB + '000', '2, 3, 540 und 3, 2, 510', '200, 300, 540 und 300, 200, 510'],
                             rueck={1: 'Mit 100 multipliziert wird auch die rechte Seite.', 2: 'Mal 100: Aus 0.02 wird 2, nicht 200.'},
                             rueck_sprich={1: 'Mit hundert multipliziert wird auch die rechte Seite.',
                                           2: 'Mal hundert: Aus null Komma null zwei wird zwei, nicht zweihundert.'}),
                  spr='Beide Gleichungen mal hundert: zwei x plus drei y gleich vierundfünfzigtausend, drei x plus zwei y gleich '
                      'einundfünfzigtausend. Ganze Zahlen tippen sich sicherer.',
                  el=[f(r'\begin{cases} 2 \cdot x + 3 \cdot y = 54\,000 \\ 3 \cdot x + 2 \cdot y = 51\,000 \end{cases}', 520, 44, x=RX, ein='@hundert'),
                      ] + sys_eingabe((2, 3, 54000), (3, 2, 51000), 640, '@Ganze')),
             dict(gegeben=DV + [G_formel(r'\begin{cases} 2 \cdot x + 3 \cdot y = 54\,000 \\ 3 \cdot x + 2 \cdot y = 51\,000 \end{cases}', 36, 110)],
                  frage=dict(text='sys-solv zeigt x = 9000 und y = 12 000. Was heisst das?',
                             sprich='sys-solv zeigt x gleich neuntausend und y gleich zwölftausend. Was heisst das?',
                             opt=['9000 CHF zu 2 %, 12' + NB + '000 CHF zu 3 %', '12' + NB + '000 CHF zu 2 %, 9000 CHF zu 3 %', '9000 CHF und 12' + NB + '000 CHF Zins'],
                             rueck={1: 'x war das Kapital zu 2 %.', 2: 'x und y sind Kapitalien, nicht Zinsen.'},
                             rueck_sprich={1: 'x war das Kapital zu zwei Prozent.'}),
                  spr='x ist das Kapital zu zwei Prozent: neuntausend Franken. y, das Kapital zu drei Prozent, beträgt zwölftausend Franken.',
                  el=ergebnis('x=9000', 'y=12000') + [
                      tx(r'@\fc{9000}@ CHF zu 2 %, @\fc{12\,000}@ CHF zu 3 %', 760, 38, x=RX, ein='@neuntausend')]),
             dict(gegeben=DV + [G_formel(r'x = 9000,\ y = 12\,000')],
                  frage=dict(text='Mit welcher Probe prüfst du beide Aussagen?', sprich='Mit welcher Probe prüfst du beide Aussagen?',
                             opt=['180 + 360 = 540 und 270 + 240 = 510', '180 + 360 = 540 genügt', '9000 + 12' + NB + '000 = 21' + NB + '000'],
                             rueck={1: 'Der Text macht zwei Aussagen.', 2: 'Die Summe der Kapitalien steht nicht im Text.'}),
                  spr='Probe am Text: hundertachtzig plus dreihundertsechzig gleich fünfhundertvierzig. Vertauscht: zweihundertsiebzig plus '
                      'zweihundertvierzig gleich fünfhundertzehn. Die Kapitalien sind neuntausend und zwölftausend Franken.',
                  el=[f(r'180 + 360 = 540 \;\checkmark \qquad 270 + 240 = 510 \;\checkmark', 520, 40, x=RX, ein='@Probe'),
                      tx(r'@\fc{9000}@ CHF und @\fc{12\,000}@ CHF', 610, 40, x=RX, ein='@Kapitalien')]),
         ]),
    dict(nr=2, kurz='Zins',
         text='Ein Kapital bringt in einem Jahr 480 CHF Zins.|Wäre es um 4000 CHF kleiner und der Zinssatz|um 0.4 Prozentpunkte höher, ergäbe es gleich|viel Zins. Wie gross sind Kapital und Zinssatz?',
         spr='Ein Kapital bringt in einem Jahr vierhundertachtzig Franken Zins. Wäre es um viertausend Franken kleiner und der Zinssatz '
             'um null Komma vier Prozentpunkte höher, ergäbe es gleich viel Zins. Wie gross sind Kapital und Zinssatz?',
         schritte=[
             dict(frage=dict(text='Zwei Unbekannte: Welche Deklaration?', sprich='Zwei Unbekannte: Welche Deklaration passt?',
                             opt=['K: Kapital in CHF, p: Zinssatz (Dezimalzahl)', 'K: Zins in CHF, p: Zinssatz', 'K: Kapital in CHF, p: Zins in CHF'],
                             rueck={1: 'Der Zins ist gegeben: 480 CHF.', 2: 'Der Zins ist gegeben. Was ist neben dem Kapital unbekannt?'},
                             rueck_sprich={1: 'Der Zins ist gegeben: vierhundertachtzig Franken.'}),
                  spr='K ist das Kapital in Franken, p der Zinssatz als Dezimalzahl. Null Komma vier Prozentpunkte mehr heisst p plus null '
                      'Komma null null vier.',
                  el=[tx(r'@\fa{K}@: Kapital in CHF', 520, 40, x=RX, ein='@Kapital'),
                      tx(r'@\fb{p}@: Zinssatz (Dezimalzahl)', 590, 40, x=RX, ein='@Zinssatz'),
                      n('0.4 Prozentpunkte mehr: @p + 0.004@', 690, 'blau', 38, x=RX, ein='@Prozentpunkte')]),
             dict(gegeben=DK,
                  frage=dict(text='Welches System übersetzt die Aussagen?', sprich='Welches System übersetzt die Aussagen?',
                             opt=['K·p = 480 und (K − 4000)·(p + 0.004) = 480', 'K·p = 480 und (K − 4000)·(p + 0.4) = 480',
                                  'K·p = 480 und (K − 4000)·p + 0.004 = 480'],
                             rueck={1: '0.4 Prozentpunkte als Dezimalzahl?', 2: 'Der neue Zinssatz multipliziert das ganze neue Kapital: Klammer.'},
                             rueck_sprich={1: 'Null Komma vier Prozentpunkte als Dezimalzahl?'}),
                  spr='Zins gleich Kapital mal Zinssatz: K mal p gleich vierhundertachtzig. Mit viertausend Franken weniger und dem höheren '
                      'Zinssatz: Klammer K minus viertausend mal Klammer p plus null Komma null null vier, wieder vierhundertachtzig. '
                      'Ein Produkt der Unbekannten: quadratisch.',
                  el=[f(r'\begin{cases} K \cdot p = 480 \\ (K - 4000) \cdot (p + 0.004) = 480 \end{cases}', 520, 40, x=RX, ein='@Kapital'),
                      n('Produkt der Unbekannten: quadratisch', 700, 'rot', 38, x=RX, ein='@Produkt')]),
             dict(gegeben=DK + [G_formel(r'\begin{cases} K \cdot p = 480 \\ (K - 4000) \cdot (p + 0.004) = 480 \end{cases}', 34, 110)],
                  frage=dict(text='K durch p ausgedrückt, eingesetzt: Welche Grundform?',
                             sprich='K durch p ausgedrückt und eingesetzt: Welche Grundform entsteht?',
                             opt=['1' + NB + '000' + NB + '000·p² + 4000·p − 480 = 0', '1' + NB + '000' + NB + '000·p² − 4000·p − 480 = 0',
                                  '1' + NB + '000' + NB + '000·p² + 4000·p + 480 = 0'],
                             rueck={1: 'Prüfe das Vorzeichen in K = 4000 + 1 000 000·p.', 2: 'Prüfe das Vorzeichen der 480.'},
                             rueck_sprich={1: 'Prüfe das Vorzeichen in K gleich viertausend plus eine Million mal p.',
                                           2: 'Prüfe das Vorzeichen der vierhundertachtzig.'}),
                  spr='Ausmultipliziert: K p plus null Komma null null vier K minus viertausend p minus sechzehn gleich vierhundertachtzig. '
                      'Mit K p gleich vierhundertachtzig bleibt null Komma null null vier K gleich viertausend p plus sechzehn, also K gleich '
                      'viertausend plus eine Million mal p. Eingesetzt: eine Million p Quadrat plus viertausend p minus vierhundertachtzig gleich null.',
                  el=[f(r'K p + 0.004 \cdot K - 4000 \cdot p - 16 = 480', 520, 36, x=RX, ein='@Ausmultipliziert'),
                      f(r'K = 4000 + 1\,000\,000 \cdot p', 590, 38, x=RX, ein='@also'),
                      f(r'(4000 + 1\,000\,000 \cdot p) \cdot p = 480', 660, 38, x=RX, ein='@Eingesetzt'),
                      f(r'1\,000\,000 \cdot p^2 + 4000 \cdot p - 480 = 0', 740, 40, x=RX, ein='@Quadrat'),
                      ] + poly_eingabe(1000000, 4000, -480, 640, '@Quadrat+1')),
             dict(gegeben=DK + [G_formel(r'1\,000\,000 \cdot p^2 + 4000 \cdot p - 480 = 0', 36)],
                  frage=dict(text='poly-solv zeigt x1 = 1/50 und x2 = −3/125. Was folgt?',
                             sprich='poly-solv zeigt x eins gleich ein Fünfzigstel und x zwei gleich minus drei Hundertfünfundzwanzigstel. Was folgt?',
                             opt=['p = 0.02 und K = 24' + NB + '000', 'p = 0.02 oder p = −0.024', 'p = 1/50 %'],
                             rueck={1: 'Rechne K = 480 : p für beide Werte. Ist jedes Kapital möglich?', 2: '1/50 als Dezimalzahl ist 0.02, als Prozent 2 %.'},
                             rueck_sprich={1: 'Rechne K gleich vierhundertachtzig durch p für beide Werte. Ist jedes Kapital möglich?',
                                           2: 'Ein Fünfzigstel als Dezimalzahl ist null Komma null zwei, als Prozent zwei Prozent.'}),
                  spr='Als Dezimalzahl null Komma null zwei und minus null Komma null zwei vier. Mit dem negativen Wert wäre K gleich '
                      'vierhundertachtzig durch p negativ, minus zwanzigtausend Franken: unmöglich. Also p gleich null Komma null zwei und K '
                      'gleich vierhundertachtzig durch null Komma null zwei, vierundzwanzigtausend Franken.',
                  el=ergebnis('x1=[1|50]', 'x2=⁻[3|125]') + [
                      rechner(['x1=0.02', '', ''], ['↔'], 515, '@Dezimalzahl', RX, 400),
                      rechner(['x2=⁻0.024', '', ''], ['↔'], 515, '@Dezimalzahl+0.6', RX + 420, 400),
                      tx(r'@\fd{p = -0.024}@: @K = -20\,000@, unmöglich', 760, 34, x=RX, ein='@negativen'),
                      f(r'p = \fc{0.02}, \quad K = 480 : 0.02 = \fc{24\,000}', 850, 40, x=RX, ein='@Also')]),
             dict(gegeben=DK + [G_formel(r'K = 24\,000,\ p = 0.02')],
                  frage=dict(text='Welche Probe prüft beide Aussagen?', sprich='Welche Probe prüft beide Aussagen?',
                             opt=['24' + NB + '000 · 0.02 = 480 und 20' + NB + '000 · 0.024 = 480', '24' + NB + '000 · 0.02 = 480 genügt',
                                  '24' + NB + '000 − 4000 = 20' + NB + '000'],
                             rueck={1: 'Prüfe auch die zweite Aussage.', 2: 'Das prüft den Zins nicht.'}),
                  spr='Probe am Text: vierundzwanzigtausend mal null Komma null zwei gleich vierhundertachtzig. Viertausend weniger sind '
                      'zwanzigtausend, zu zwei Komma vier Prozent gibt das wieder vierhundertachtzig Franken. Das Kapital beträgt '
                      'vierundzwanzigtausend Franken, der Zinssatz zwei Prozent.',
                  el=[f(r'24\,000 \cdot 0.02 = 480 \;\checkmark \qquad 20\,000 \cdot 0.024 = 480 \;\checkmark', 520, 36, x=RX, ein='@Probe'),
                      tx(r'Kapital @\fc{24\,000}@ CHF, Zinssatz @\fc{2\,\%}@', 610, 40, x=RX, ein='@beträgt')]),
         ]),
], merke('Zum Mitnehmen: Zwei Zinsgleichungen mit bekannten Zinssätzen geben ein lineares System, mal hundert für sys-solv. Sind Kapital '
         'und Zinssatz beide unbekannt, steht das Produkt K mal p im System: ausmultiplizieren, eine Unbekannte ausdrücken, einsetzen, '
         'Grundform, poly-solv. Negative Kapitalien fallen weg.',
         'bekannte Zinssätze: lineares System|Kapital und Zinssatz unbekannt: quadratisch|negative Kapitalien verwerfen'),
   folge=12)

if FEHLT and WZ:
    print('Ohne gemessene Wortzeit (geschätzt):', len(FEHLT))
