"""Baut leitprogramme/planimetrie.html aus einer Kapitelbeschreibung (06.10.2026).

  python3 scripts/lp/planimetrie/seite.py

Leitprogramm zum Teilgebiet GF 5.2 Planimetrie (Themenseiten g5-2a bis g5-2d), nach dem Leitfaden
des Auftraggebers ~/HOWTO-PlaniLP.md. Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden
Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf kommt
das Gerüst aus leitprogramme/lineare-quadratische-gleichungen.html. Wiederholbar. Danach Pre-Flight und
python3 scripts/build-seo.py. Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/planimetrie.html'
NAME = 'Planimetrie'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/lineare-quadratische-gleichungen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Lineare und quadratische Gleichungen</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-gleichungen-', 'lp-planimetrie-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Gleichungen', '\n/* ════════ Planimetrie'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Lineare und quadratische Gleichungen —'),
                    alt.find('<script>\n/* Leitprogramm Planimetrie —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Lineare und quadratische Gleichungen', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 6. Oktober 2026', fuss)

CSS = '''
/* ════════ Planimetrie (06.10.2026) — Kapitelmuster wie die Funktionen- und Gleichungen-Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Festhalten, PDF-Weg) wie dort. Neu ist der Geometrie-Arbeitsbereich:
   Figur verändern, Hilfslinie antippen, Grösse eingeben. Farben: Figur blau, Hilfslinie orange,
   Fläche und Ergebnis grün, Fehler rot. */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:440px}
.leiste{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:0 0 10px;padding:9px 12px;border-radius:9px;
  background:var(--orange-hell);border:1px solid var(--orange-rand);font-family:var(--sans);font-size:.92rem}
.leiste .ls-nr{font-family:var(--mono);font-size:.78rem;color:var(--orange);font-weight:700}
.leiste .ls-text{flex:1 1 260px;min-width:0}
.leiste .ls-ok{color:var(--gruen);font-weight:700;font-size:1.1rem;min-width:1em}
.leiste .ls-weiter,.leiste .ls-neu{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;
  border:1px solid var(--linie);background:var(--karte);color:var(--tinte-2)}
.leiste.geloest{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.leiste.geloest .ls-weiter{border-color:var(--gruen-rand);color:var(--tinte);font-weight:700}
.leiste.fertig{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.kap-clip{max-width:640px}
.kompetenzen ul{margin:10px 0 0;padding-left:1.25em;font-family:var(--sans);font-size:.92rem}
.kompetenzen li{margin:5px 0}
.kompetenzen .rlp-quelle{font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);margin:8px 0 0}
.kompetenzen .ohm{font-size:.72rem;padding:1px 7px;border-radius:999px;background:var(--orange-hell);border:1px solid var(--orange-rand);white-space:nowrap}
.sim .pfeil{fill:var(--tinte-2)} svg.mini .pfeil{fill:var(--tinte-2)}
.achsname{fill:var(--tinte);font-family:var(--serif);font-style:italic;font-size:12px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
svg.mini .achsname{font-size:10px;stroke-width:3px}
text.p-text{stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.sim-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input.menge{width:9em}
.sim-formel{line-height:1.6}
.sim .kurve.rechts{stroke:var(--orange);stroke-dasharray:6 4}
.p-loes{fill:var(--gruen)}
svg.mini .kurve.k1{stroke:var(--orange)} svg.mini .kurve.k2{stroke:var(--gruen)}
.nb{white-space:nowrap}
/* Geometrie-Arbeitsbereich: Figur (blau), Hilfslinien und Kandidaten (orange), Fläche/Ergebnis (grün). */
.geo{max-width:680px;margin:10px auto 6px}
.geo > svg{display:block;width:100%;max-width:560px;margin:0 auto;background:var(--karte);border:1px solid var(--linie);border-radius:9px;touch-action:manipulation}
.geo .figur{fill:var(--blau);fill-opacity:.12;stroke:var(--blau);stroke-width:2;stroke-linejoin:round}
.geo .figur.kreis,svg.geo-mini .figur.kreis{fill-opacity:.06}
.geo .verlaengerung,svg.geo-mini .verlaengerung{stroke:var(--tinte-2);stroke-width:1.2;stroke-dasharray:4 3}
.geo .parallele{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:2 4}
.geo .strahl{stroke:var(--tinte-2);stroke-width:.8;stroke-dasharray:3 4}
.geo .hilfe,svg.geo-mini .hilfe{stroke:var(--orange);stroke-width:2.2;fill:none}
.geo .hilfe2{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 3}
.geo text.hilfe{fill:var(--orange);stroke:var(--karte);stroke-width:3;paint-order:stroke}
.geo .g-rechts{fill:none;stroke-width:1.4}
.geo .sektor,svg.geo-mini .sektor{fill:var(--gruen);fill-opacity:.22;stroke:var(--gruen);stroke-width:1.5}
.geo .sektor.blass{fill-opacity:.08}
.geo .bogen{fill:none;stroke:var(--orange);stroke-width:3}
.geo .dreieck-seg{fill:var(--paper,transparent);fill-opacity:0;stroke:var(--gruen);stroke-width:1.5;stroke-dasharray:4 3}
.g-pkt{fill:var(--tinte)} .g-pkt.hilfe{fill:var(--orange)}
.g-text{font-family:var(--serif);font-size:12px;fill:var(--tinte);stroke:var(--karte);stroke-width:3;paint-order:stroke}
.g-text.ecke{font-weight:600;font-style:normal} .g-text.seite{font-style:italic} .g-text.klein{font-size:10px} .g-text.bild{fill:var(--orange)}
.g-text.mass{font-family:var(--sans);font-size:10px;fill:var(--tinte-2)}
.kandidat{cursor:pointer;outline:none}
.kandidat .k-sicht{stroke:var(--orange);stroke-width:2;stroke-dasharray:5 3}
.kandidat .k-treffer{stroke:transparent;stroke-width:16}
.kandidat:hover .k-sicht,.kandidat:focus-visible .k-sicht{stroke-width:3.5;stroke-dasharray:none}
.g-eingabe{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;justify-content:center;margin:10px 0 0;font-family:var(--sans);font-size:.92rem}
.g-eingabe[hidden]{display:none}
.g-feld{display:inline-flex;gap:6px;align-items:center}
.g-feld input{width:5.2em;font-family:var(--mono);font-size:.95rem;padding:4px 6px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.g-feld input:focus{outline:none;border-color:var(--orange-rand)}
.g-pruefen{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;border:1px solid var(--orange-rand);background:var(--karte);color:var(--tinte)}
.g-rueck{font-family:var(--sans);font-size:.9rem;margin-top:10px;border-radius:7px}
.g-rueck:empty{display:none}
.g-rueck.richtig{background:var(--gruen-hell);border-left:4px solid var(--gruen-rand);padding:8px 12px}
.g-rueck.falsch{background:var(--rot-hell);border-left:4px solid var(--rot-rand);padding:8px 12px}
.g-rueck.hinweis{background:var(--papier-2);padding:8px 12px}
.geo input[type=range]:disabled{opacity:.4}
svg.geo-mini{display:block;width:100%;max-width:300px;margin:6px 0;background:var(--karte);border:1px solid var(--linie);border-radius:8px}
svg.geo-mini .figur{fill:var(--blau);fill-opacity:.12;stroke:var(--blau);stroke-width:1.8;stroke-linejoin:round}
.mini-reihe{display:flex;flex-wrap:wrap;gap:10px}
svg.geo-mini .gitter{stroke:var(--linie);stroke-width:.5}
.geo polygon.bild{fill:var(--orange);fill-opacity:.12;stroke:var(--orange);stroke-width:2;stroke-dasharray:6 3}
.geo .figur-linie{stroke:var(--blau);stroke-width:2.2} .geo .bild-linie{stroke:var(--orange);stroke-width:2.2}
svg.geo-mini .grundseite{stroke:var(--orange);stroke-width:3.5;stroke-linecap:round}
svg.geo-mini .kandidat-linie{stroke:var(--tinte);stroke-width:1.6;stroke-dasharray:5 3}
svg.geo-mini .nummer{font-family:var(--sans);font-weight:700;font-size:12px;font-style:normal}
svg.geo-mini.ue-bild{max-width:260px;margin:4px auto 8px}
'''


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf — so rechnet
    die Bibliothek), abgerundet auf Sekunden (HOWTO-leitprogramme §7)."""
    p = R + 'clips/' + name + '.json'
    if not os.path.exists(p):
        return '0:00'
    d = json.load(open(p))
    t = int(sum(s.get('dauer', 0) for s in d['szenen']))
    return '%d:%02d' % (t // 60, t % 60)


def clipkarte(datei, titel, zeit=None):
    zeit = zeit or dauer(datei)
    return f'''<div class="clipkarte kap-clip" data-clip="clips/{datei}.html" data-titel="{titel}">
        <button class="clip-start" type="button">
          <span class="clip-play" aria-hidden="true">▶</span>
          <span class="clip-txt"><span class="clip-titel">{titel}</span></span>
          <span class="clip-zeit">{zeit}</span>
        </button>
      </div>'''


def uebung(typ, titel, bild=False):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          {'<svg class="geo-mini ue-bild" role="img" aria-label="Dreieck mit markierter Grundseite und drei nummerierten Linien"></svg>' if bild else ''}
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(sim, p, label, mn, mx, st, val, akz='grau', einheit=''):
    return (f'<div class="sl-grp akz-{akz}"><label for="{sim}-{p}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>')


def bereich(nr, label, regler_):
    """Geometrie-Arbeitsbereich: Aufgabenleiste, Live-Zeile, Figur, Eingabefelder, Rückmeldung, Regler."""
    return f'''      <figure class="sim geo" id="sim{nr}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="{label}"></svg>
        <div class="g-eingabe" hidden></div>
        <div class="g-rueck" aria-live="polite"></div>
        <div class="sl-row">
          {regler_}
        </div>
      </figure>'''


def test(tid, titel, punkte, aufgaben, zwei=True):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte, sum(a[1] for a in aufgaben))
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 5.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim}

      <p class="phase"><span>③</span> Kontrollfragen</p>
      {clipkarte(*clip2)}

      <h3>Festhalten</h3>
{festhalten}

      <p class="phase"><span>④</span> Üben mit Rückmeldung</p>
      <div class="duo">
        {ue}
      </div>

      <p class="phase"><span>⑤</span> Aufgaben mit Lösungen</p>
{aufgaben}
      <p class="ausf">Mehr dazu: {mehr}</p>
    </section>'''




TA = '../grundlagen/g5-2a-dreiecke.html'
TB = '../grundlagen/g5-2b-vierecke.html'
TC = '../grundlagen/g5-2c-kreis-und-kreisteile.html'
TD = '../grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html'


def fig(daten, fenster, breite=220, hoehe=150):
    """Figur zu einer Aufgabe; daten: Liste wie in seite.js («Figuren zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="geo-mini" data-fenster="{fenster}" data-breite="{breite}" data-hoehe="{hoehe}" '
            f'data-fig="{html.escape(json.dumps(daten, ensure_ascii=False), quote=True)}"></svg></div>')


# ------------------------------------------------------------------ Kapitel 1
sim1 = bereich(1, 'Dreieck ABC mit verschiebbarer Ecke C und den Linien aus C',
               regler('s1', 'cx', 'C: waagrecht', -2, 8, 0.5, 2) + '\n          ' + regler('s1', 'cy', 'C: senkrecht', 1, 5, 0.5, 3))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Dreiecke beschreiben</div>
          <p>Ecken \(A, B, C\) gegen den Uhrzeigersinn; die Seite \(a\) liegt der Ecke \(A\) gegenüber, der Winkel \(\alpha\) liegt bei \(A\).</p>
          <p><b>Innenwinkelsumme:</b> \(\alpha + \beta + \gamma = 180°\) — die Parallele durch \(C\) zu \(AB\) bildet mit \(\alpha\) und \(\beta\) Wechselwinkel.</p>
          <p>Gleichschenklig: zwei gleiche Seiten, die Basiswinkel sind gleich. Gleichseitig: drei gleiche Seiten, alle Winkel \(60°\). Rechtwinklig: ein Winkel \(90°\).</p>
          <ul>
            <li><b>Höhe</b> \(h_c\): Lot von \(C\) auf die <b>Gerade</b> \(AB\). Die drei Höhen schneiden sich im <b>Höhenschnittpunkt</b> \(H\).</li>
            <li><b>Seitenhalbierende</b> \(s_c\): von \(C\) zur Mitte von \(AB\) — Schwerpunkt \(S\).</li>
            <li><b>Winkelhalbierende</b> \(w_\gamma\): halbiert \(\gamma\) — Inkreismittelpunkt \(M_I\).</li>
            <li><b>Mittelsenkrechte</b> von \(c\): senkrecht durch die Mitte von \(AB\) — Umkreismittelpunkt \(M_U\).</li>
          </ul>
          <p>Im stumpfwinkligen Dreieck liegen die beiden Höhen aus den spitzen Ecken ausserhalb (ihr Fusspunkt auf der Verlängerung der Gegenseite), mit ihnen \(H\); auch \(M_U\) liegt ausserhalb. Die Höhe aus der stumpfen Ecke liegt innen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Höhe und Mittelsenkrechte verwechseln: Beide stehen senkrecht — die Höhe geht durch die Ecke, die Mittelsenkrechte durch die Seitenmitte.</p>
          <p>Die Höhe immer innerhalb suchen: Im stumpfwinkligen Dreieck liegt der Fusspunkt von zwei Höhen auf der Verlängerung der Seite.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 2, r'Skizziere ein Dreieck und beschrifte Ecken, Seiten und Winkel normgerecht.',
     r'<p>Ecken \(A, B, C\) gegen den Uhrzeigersinn; \(a\) gegenüber \(A\) (also \(a = BC\)), \(b = CA\), \(c = AB\); \(\alpha\) bei \(A\), \(\beta\) bei \(B\), \(\gamma\) bei \(C\).</p>', ''),
    ('1b', 3, r'Berechne den fehlenden Winkel: (a) \(\alpha = 35°\), \(\gamma = 90°\); (b) gleichschenklig, Basiswinkel \(52°\) — Winkel an der Spitze; (c) gleichseitig — jeder Winkel.',
     r'<p>(a) \(\beta = 180° - 35° - 90° = 55°\). (b) \(180° - 2 \cdot 52° = 76°\). (c) \(180° : 3 = 60°\).</p>', ''),
    ('1c', 2, r'Welche Linie ist im Bild orange eingezeichnet? Woran erkennst du sie?',
     r'<p>Die Seitenhalbierende \(s_c\): Sie geht von \(C\) zur Mitte von \(AB\) (\(3\,\text{cm}\) von \(A\) und von \(B\)) und steht nicht senkrecht.</p>',
     fig([['v', [[0, 0], [6, 0], [1.5, 3.5]]], ['s', [1.5, 3.5], [3, 0]], ['p', [3, 0]], ['t', [0, 0], 'A', 'ecke', -8, 12], ['t', [6, 0], 'B', 'ecke', 8, 12], ['t', [1.5, 3.5], 'C', 'ecke', 0, -8]], '-1,7,-1')),
    ('1d', 3, r'In welchen Dreiecken liegt der Fusspunkt der Höhe \(h_c\) ausserhalb der Seite \(c\)? Skizziere ein Beispiel mit eingezeichneter Höhe.',
     r'<p>Wenn \(\alpha\) oder \(\beta\) stumpf ist. Dann trifft das Lot von \(C\) die Gerade \(AB\) auf ihrer Verlängerung; die Höhe liegt ausserhalb des Dreiecks.</p>', ''),
    ('1e', 2, r'Warum ist die Innenwinkelsumme jedes Dreiecks \(180°\)?',
     r'<p>Zieh durch \(C\) die Parallele zu \(AB\). Die Winkel links und rechts von \(\gamma\) an dieser Parallelen sind Wechselwinkel zu \(\alpha\) und \(\beta\), also gleich gross. Zusammen mit \(\gamma\) bilden die drei Winkel einen gestreckten Winkel: \(180°\).</p>', ''),
], zwei=False)
k1 = kapitel(1, 'dreiecke', 'Dreiecke beschreiben', 35,
             r'Du beschriftest Dreiecke normgerecht, nutzt die Innenwinkelsumme, erkennst spezielle Dreiecke und unterscheidest Höhe, Seitenhalbierende, Winkelhalbierende und Mittelsenkrechte.',
             ('g5-2-lp-dreiecke', 'Dreiecke beschreiben'), sim1, ('g5-2-lp-kontrolle-dreiecke', 'Kontrollfragen zu Dreiecken'),
             fest1, [uebung('winkelsumme', 'Winkel berechnen'), uebung('element', 'Welche Linie ist gemeint?')],
             auf1, f'<a href="{TA}#typen">Themenseite 5.2a, Spezielle Dreiecke und Dreieckselemente</a>', komp='K1; K2')

# ------------------------------------------------------------------ Kapitel 2
sim2 = bereich(2, 'Dreieck ABC mit Grundseite AB von 8 cm und einer Spitze C, die parallel zu AB wandert',
               regler('s2', 't', 'Spitze C: t', -2, 11, 0.5, 4))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Dreiecksfläche und zugehörige Höhe</div>
          <p>Zu jeder Seite als <b>Grundseite</b> \(g\) gehört eine <b>Höhe</b> \(h\): der senkrechte Abstand des gegenüberliegenden Eckpunkts zur <b>Geraden</b> durch \(g\).</p>
          <p>\[ A = \tfrac{1}{2}\, g \cdot h \qquad h = \tfrac{2A}{g} \]</p>
          <p>Zwei gleiche Dreiecke ergeben ein Parallelogramm mit der Fläche \(g \cdot h\) (ein Dreieck abschneiden und anfügen gibt ein Rechteck \(g \times h\), mehr dazu in Kapitel 3) — das Dreieck ist die Hälfte.</p>
          <p><b>Vorgehen:</b> Grundseite wählen → zugehörige Höhe bestimmen → Einheiten angleichen → Formel einsetzen → prüfen (Skizze, Grössenordnung, Einheit).</p>
          <p>Wandert die Spitze parallel zur Grundseite, bleiben \(g\) und \(h\) gleich — und damit die Fläche.</p>
          <p>Umfang: \(U = a + b + c\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Eine schräge Seite als Höhe nehmen. Die Höhe steht senkrecht auf der Grundseite — im stumpfwinkligen Dreieck liegt sie zu den beiden Seiten am stumpfen Winkel ausserhalb.</p>
          <p>Das \(\tfrac{1}{2}\) vergessen: \(g \cdot h\) ist das Parallelogramm.</p>
          <p>Einheiten mischen: \(0.6\,\text{m}\) und \(40\,\text{cm}\) zuerst angleichen.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Im Bild ist \(g = AB = 10\,\text{cm}\) und \(h = 4\,\text{cm}\). Zeichne die Höhe zu \(g\) ein und berechne die Fläche.',
     r'<p>Die Höhe ist das Lot von \(C\) auf die Gerade \(AB\); ihr Fusspunkt liegt rechts von \(B\) auf der Verlängerung. \(A = \tfrac{1}{2} \cdot 10 \cdot 4 = 20\,\text{cm}^2\).</p>',
     fig([['v', [[0, 0], [10, 0], [12.5, 4]]], ['t', [0, 0], 'A', 'ecke', -8, 12], ['t', [10, 0], 'B', 'ecke', 0, 13], ['t', [12.5, 4], 'C', 'ecke', 0, -7], ['t', [5, 0], 'g = 10 cm', 'mass', 0, 13]], '-1,14,-1.2', 260, 110)),
    ('2b', 2, r'Ein Dreieck hat die Grundseite \(g = 8\,\text{cm}\) und die Fläche \(A = 20\,\text{cm}^2\). Wie lang ist die zugehörige Höhe?',
     r'<p>\(h = \tfrac{2A}{g} = \tfrac{40}{8} = 5\,\text{cm}\).</p>', ''),
    ('2c', 3, r'Grundseite \(g = 0.6\,\text{m}\), Höhe \(h = 40\,\text{cm}\). Berechne die Fläche in \(\text{m}^2\) und in \(\text{cm}^2\).',
     r'<p>\(A = \tfrac{1}{2} \cdot 0.6\,\text{m} \cdot 0.4\,\text{m} = 0.12\,\text{m}^2 = 1200\,\text{cm}^2\) (\(1\,\text{m}^2 = 10\,000\,\text{cm}^2\)).</p><p class="komm">Wer \(0.6 \cdot 40 : 2 = 12\) rechnet, mischt m und cm.</p>', ''),
    ('2d', 2, r'Die beiden Dreiecke im Bild sehen verschieden aus. Begründe ohne zu messen, dass sie gleich gross sind.',
     r'<p>Beide haben dieselbe Grundseite (\(6\,\text{cm}\)) und dieselbe Höhe (\(3\,\text{cm}\)): Die Spitzen liegen auf einer Parallelen zur Grundseite. \(A = \tfrac{1}{2} \cdot 6 \cdot 3 = 9\,\text{cm}^2\) für beide.</p>',
     fig([['v', [[0, 0], [6, 0], [1, 3]]], ['v', [[8, 0], [14, 0], [16.5, 3]]], ['s', [-0.5, 3], [17, 3], 'verlaengerung']], '-1,18,-1', 280, 90)),
    ('2e', 2, r'Ein rechtwinkliges Dreieck hat die Seiten \(6\,\text{cm}\), \(8\,\text{cm}\) und \(10\,\text{cm}\). Berechne Umfang und Fläche.',
     r'<p>\(U = 24\,\text{cm}\). Die Katheten \(6\) und \(8\) stehen senkrecht aufeinander — die eine ist die Höhe zur anderen: \(A = \tfrac{1}{2} \cdot 6 \cdot 8 = 24\,\text{cm}^2\).</p>', ''),
], zwei=False)
k2 = kapitel(2, 'flaeche', 'Dreiecksfläche und zugehörige Höhe', 40,
             r'Du findest zu einer Grundseite die richtige Höhe — auch ausserhalb des Dreiecks —, begründest \(A = \tfrac{1}{2}\, g \cdot h\) und berechnest Fläche, Höhe und Umfang mit passenden Einheiten.',
             ('g5-2-lp-flaeche', 'Dreiecksfläche und Höhe'), sim2, ('g5-2-lp-kontrolle-flaeche', 'Kontrollfragen zur Dreiecksfläche'),
             fest2, [uebung('zuordnen', 'Welche Linie ist die Höhe?', True), uebung('dreieck-flaeche', 'Fläche berechnen'), uebung('hoehe', 'Höhe aus der Fläche')],
             auf2, f'<a href="{TA}#theorie">Themenseite 5.2a, Berechnung</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = bereich(3, 'Trapez ABCD mit Parallelseiten a = 8 cm und c, Höhe h und Versatz d',
               regler('s3', 'c', 'Seite c', 1, 8, 0.5, 4, einheit=' cm') + '\n          ' + regler('s3', 'h', 'Höhe h', 1, 5, 0.5, 3, einheit=' cm')
               + '\n          ' + regler('s3', 'd', 'Versatz d', -2, 6, 0.5, 1, einheit=' cm'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Vierecke</div>
          <p>Quadrat \(\subset\) Rechteck \(\subset\) Parallelogramm \(\subset\) Trapez; die Raute (Rhombus) ist ein Parallelogramm mit vier gleichen Seiten; der Drachen hat zwei Paare gleich langer Nachbarseiten.</p>
          <ul>
            <li>Rechteck \(A = a \cdot b\); Quadrat \(A = a^2\).</li>
            <li>Parallelogramm \(A = a \cdot h\) (abschneiden, anfügen: ein Rechteck).</li>
            <li>Trapez \(A = \tfrac{1}{2}(a + c) \cdot h = m \cdot h\) mit der <b>Mittellinie</b> \(m = \tfrac{1}{2}(a + c)\) — sie verbindet die Mitten der Schenkel.</li>
            <li>Raute und Drachen \(A = \tfrac{1}{2}\, e \cdot f\) (die Hälfte des Rechtecks aus den Diagonalen).</li>
          </ul>
          <p><b>Fehlende Länge:</b> mit Pythagoras \(a^2 + b^2 = c^2\) in einem rechtwinkligen Teildreieck. Gleichschenkliges Trapez mit \(a = 10\), \(c = 4\), Schenkel \(5\): Überstand \(\tfrac{10 - 4}{2} = 3\), \(h = \sqrt{5^2 - 3^2} = 4\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beim Parallelogramm die schräge Seite statt der Höhe nehmen.</p>
          <p>Beim gleichschenkligen Trapez den ganzen Unterschied \(a - c\) als Überstand nehmen — er verteilt sich auf zwei Seiten.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Parallelogramm mit \(a = 7\,\text{cm}\), \(b = 5\,\text{cm}\) und der Höhe \(h = 4\,\text{cm}\) auf \(a\). Berechne Fläche und Umfang.',
     r'<p>\(A = a \cdot h = 28\,\text{cm}^2\); \(U = 2(a + b) = 24\,\text{cm}\).</p><p class="komm">\(a \cdot b = 35\) wäre ein Rechteck — die schräge Seite ist keine Höhe.</p>', ''),
    ('3b', 3, r'Trapez mit den Parallelseiten \(a = 12\,\text{cm}\), \(c = 6\,\text{cm}\) und \(h = 5\,\text{cm}\). Berechne die Mittellinie und die Fläche.',
     r'<p>\(m = \tfrac{1}{2}(12 + 6) = 9\,\text{cm}\); \(A = m \cdot h = 45\,\text{cm}^2\).</p>', ''),
    ('3c', 2, r'Ein Drachen hat die Diagonalen \(e = 10\,\text{cm}\) und \(f = 6\,\text{cm}\). Wie gross ist seine Fläche?',
     r'<p>\(A = \tfrac{1}{2} \cdot 10 \cdot 6 = 30\,\text{cm}^2\).</p>', ''),
    ('3d', 4, r'Gleichschenkliges Trapez: \(a = 14\,\text{cm}\), \(c = 8\,\text{cm}\), Schenkel \(5\,\text{cm}\). Berechne Höhe, Fläche und Umfang.',
     r'<p>Überstand \(\tfrac{14 - 8}{2} = 3\,\text{cm}\); \(h = \sqrt{5^2 - 3^2} = 4\,\text{cm}\). \(A = \tfrac{1}{2}(14 + 8) \cdot 4 = 44\,\text{cm}^2\); \(U = 14 + 8 + 2 \cdot 5 = 32\,\text{cm}\).</p>',
     fig([['v', [[0, 0], [14, 0], [11, 4], [3, 4]]], ['s', [3, 4], [3, 0], 'hilfe'], ['r', [3, 0], [1, 0], [0, 1]], ['t', [7, 0], 'a = 14 cm', 'mass', 0, 13], ['t', [7, 4], 'c = 8 cm', 'mass', 0, -6], ['t', [12.5, 2], '5 cm', 'mass', 8, 0, 'start']], '-1,15.5,-1.2', 260, 110)),
    ('3e', 2, r'Warum ist jedes Rechteck ein Parallelogramm, aber nicht jedes Parallelogramm ein Rechteck?',
     r'<p>Ein Parallelogramm braucht nur zwei Paare paralleler Seiten — das hat jedes Rechteck. Ein Rechteck verlangt zusätzlich vier rechte Winkel; ein schiefes Parallelogramm hat sie nicht.</p>', ''),
], zwei=False)
k3 = kapitel(3, 'vierecke', 'Vierecke', 40,
             r'Du ordnest Vierecke in ihre Familie ein, berechnest Umfang und Fläche von Parallelogramm, Trapez (mit Mittellinie), Raute und Drachen und bestimmst fehlende Längen mit Pythagoras.',
             ('g5-2-lp-vierecke', 'Vierecke: Familie, Fläche, fehlende Längen'), sim3, ('g5-2-lp-kontrolle-vierecke', 'Kontrollfragen zu Vierecken'),
             fest3, [uebung('viereck', 'Viereck-Fläche'), uebung('pythagoras', 'Fehlende Seite mit Pythagoras')],
             auf3, f'<a href="{TB}#theorie">Themenseite 5.2b, Umfang und Flächeninhalt</a>', komp='K1; K2')

# ------------------------------------------------------------------ Kapitel 4
sim4 = bereich(4, 'Kreis mit Mittelpunkt M, Radius r und einem Sektor mit Mittelpunktswinkel phi',
               regler('s4', 'r', 'Radius r', 1, 5, 0.5, 3, einheit=' cm') + '\n          ' + regler('s4', 'phi', 'Winkel φ', 0, 360, 1, 60, 'gruen', einheit='°'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Kreis und Kreisteile</div>
          <p><b>Sehne:</b> Strecke zwischen zwei Kreispunkten (die längste ist der Durchmesser). <b>Sekante:</b> Gerade mit zwei Schnittpunkten. <b>Tangente:</b> Gerade mit genau einem Berührpunkt — sie steht dort senkrecht auf dem Radius. <b>Passante:</b> kein gemeinsamer Punkt.</p>
          <p>\[ U = 2\pi r = \pi d \qquad A = \pi r^2 \]</p>
          <p>Kreisteile über den Anteil \(\tfrac{\varphi}{360°}\) des Vollkreises:</p>
          <p>\[ b = \tfrac{\varphi}{360°} \cdot 2\pi r \qquad A_S = \tfrac{\varphi}{360°} \cdot \pi r^2 \]</p>
          <p><b>Segment</b> (zwischen Sehne und Bogen) \(=\) Sektor \(-\) Dreieck \(M\,P_1\,P_2\), für \(\varphi \lt 180°\) (darüber kommt das Dreieck dazu). Bei \(\varphi = 90°\) ist das Dreieck rechtwinklig: \(\tfrac{1}{2}\, r^2\). Bei \(\varphi = 60°\) ist es gleichseitig: Höhe \(\sqrt{r^2 - (\tfrac{r}{2})^2}\) mit Pythagoras.</p><p><b>Kreisring:</b> \(A = \pi(R^2 - r^2)\). Die Themenseite schreibt die Sektorfläche \(A_{SK}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Durchmesser in \(\pi r^2\) einsetzen: Bei \(d = 12\,\text{cm}\) ist \(r = 6\,\text{cm}\).</p>
          <p>Beim Sektor den Anteil vergessen — und Bogen (Länge) mit Sektor (Fläche) verwechseln.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 2, r'Ein Kreis hat den Radius \(r = 7.5\,\text{cm}\). Berechne Umfang und Fläche.',
     r'<p>\(U = 2\pi \cdot 7.5 \approx 47.12\,\text{cm}\); \(A = \pi \cdot 7.5^2 \approx 176.71\,\text{cm}^2\).</p>', ''),
    ('4b', 2, r'Ein Kreis hat den Durchmesser \(d = 12\,\text{cm}\). Berechne Umfang und Fläche.',
     r'<p>\(r = 6\,\text{cm}\): \(U = 12\pi \approx 37.70\,\text{cm}\); \(A = 36\pi \approx 113.10\,\text{cm}^2\).</p>', ''),
    ('4c', 3, r'Kreissektor mit \(r = 10\,\text{cm}\) und \(\varphi = 36°\): Welcher Anteil des Kreises ist das? Berechne Bogenlänge und Sektorfläche.',
     r'<p>Anteil \(\tfrac{36°}{360°} = \tfrac{1}{10}\). \(b = \tfrac{1}{10} \cdot 20\pi \approx 6.28\,\text{cm}\); \(A_S = \tfrac{1}{10} \cdot 100\pi \approx 31.42\,\text{cm}^2\).</p>', ''),
    ('4d', 3, r'Berechne die Fläche des grün markierten Segments: \(r = 6\,\text{cm}\), \(\varphi = 90°\).',
     r'<p>Sektor \(\tfrac{1}{4} \cdot 36\pi = 9\pi \approx 28.27\,\text{cm}^2\); Dreieck \(\tfrac{1}{2} \cdot 6 \cdot 6 = 18\,\text{cm}^2\) (rechtwinklig bei \(M\)). Segment \(\approx 10.27\,\text{cm}^2\).</p>',
     fig([['k', [0, 0], 6], ['sek', [0, 0], 6, 0, 90], ['v', [[0, 0], [6, 0], [0, 6]], 'figur'], ['p', [0, 0]], ['t', [0, 0], 'M', 'ecke', -9, 12]], '-7,7,-7', 180, 180)),
    ('4e', 2, r'Warum steht die Tangente im Berührpunkt senkrecht auf dem Radius?',
     r'<p>Der Berührpunkt ist der Punkt der Tangente, der \(M\) am nächsten liegt (Abstand \(r\)); alle anderen liegen ausserhalb des Kreises. Der kürzeste Abstand eines Punkts zu einer Geraden ist das Lot — also steht der Radius senkrecht auf der Tangente.</p>', ''),
    ('4g', 2, r'Berechne die Fläche des Segments zu \(r = 4\,\text{cm}\) und \(\varphi = 60°\).',
     r'<p>Sektor \(\tfrac{1}{6} \cdot 16\pi \approx 8.38\,\text{cm}^2\). Das Dreieck ist gleichseitig (Seite \(4\,\text{cm}\)), Höhe \(\sqrt{4^2 - 2^2} = \sqrt{12} \approx 3.46\,\text{cm}\), Fläche \(\tfrac{1}{2} \cdot 4 \cdot \sqrt{12} \approx 6.93\,\text{cm}^2\). Segment \(\approx 1.45\,\text{cm}^2\).</p>', ''),
    ('4f', 2, r'Ein Kreisring hat den Aussenradius \(5\,\text{cm}\) und den Innenradius \(3\,\text{cm}\). Wie gross ist seine Fläche?',
     r'<p>\(A = \pi(5^2 - 3^2) = 16\pi \approx 50.27\,\text{cm}^2\).</p><p class="komm">\(\pi \cdot (5 - 3)^2 = 4\pi\) ist falsch: Differenz der Kreisflächen, nicht Kreis aus der Differenz.</p>', ''),
], zwei=False)
k4 = kapitel(4, 'kreis', 'Kreis und Kreisteile', 40,
             r'Du unterscheidest Sehne, Sekante, Tangente und Passante und berechnest Umfang und Fläche von Kreis, Bogen, Sektor, Segment und Ring.',
             ('g5-2-lp-kreis', 'Kreis und Kreisteile'), sim4, ('g5-2-lp-kontrolle-kreis', 'Kontrollfragen zum Kreis'),
             fest4, [uebung('kreis', 'Umfang und Fläche'), uebung('sektor', 'Bogen und Sektor')],
             auf4, f'<a href="{TC}#theorie">Themenseite 5.2c, Umfang und Fläche</a>', komp='K1; K2')

# ------------------------------------------------------------------ Kapitel 5
sim5 = bereich(5, 'Dreieck ABC und sein Bild bei einer zentrischen Streckung mit Zentrum Z und Faktor k',
               regler('s5', 'k', 'Streckfaktor k', -2, 3, 0.5, 1, 'orange'))
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zentrische Streckung und Ähnlichkeit</div>
          <p>Zentrum \(Z\), Faktor \(k\): Der Bildpunkt \(P'\) liegt auf der Geraden \(ZP\), \(\overline{ZP'} = |k| \cdot \overline{ZP}\); bei \(k \lt 0\) auf der anderen Seite von \(Z\).</p>
          <ul>
            <li>Winkel bleiben gleich, Parallelen bleiben parallel.</li>
            <li>Längen werden mit \(|k|\) multipliziert, <b>Flächen mit \(k^2\)</b>.</li>
          </ul>
          <p><b>Ähnliche Figuren</b> (\(F_1 \sim F_2\)): gleiche Winkel, Seitenverhältnisse \(\tfrac{a'}{a} = \tfrac{b'}{b} = k\).</p>
          <p><b>Strahlensätze</b> (\(AB \parallel A'B'\)): \(\overline{SA} : \overline{SA'} = \overline{SB} : \overline{SB'} = \overline{AB} : \overline{A'B'}\).</p>
          <p>Schatten: Stab \(1.5\,\text{m}\), Schatten \(2\,\text{m}\); Baumschatten \(12\,\text{m}\) → \(h = 12 \cdot \tfrac{1.5}{2} = 9\,\text{m}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Flächen mit \(k\) statt mit \(k^2\) strecken: Doppelte Seiten geben die vierfache Fläche.</p>
          <p>Beim Strahlensatz mit den Parallelen \(AB\) und \(A'B'\) gehören die ganzen Strecken ab \(S\) dazu: \(\overline{AB} : \overline{A'B'} = \overline{SA} : \overline{SA'}\), nicht \(\overline{SA} : \overline{AA'}\).</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Ein Dreieck mit den Seiten \(4\,\text{cm}\), \(6\,\text{cm}\) und \(8\,\text{cm}\) wird mit \(k = 1.5\) gestreckt. Wie lang sind die Bildseiten? Mit welchem Faktor ändert sich die Fläche?',
     r'<p>\(6\,\text{cm}\), \(9\,\text{cm}\), \(12\,\text{cm}\); die Fläche mit \(k^2 = 2.25\).</p>', ''),
    ('5b', 3, r"Im Bild ist \(AB \parallel A'B'\), \(\overline{SA} = 3\,\text{cm}\), \(\overline{AA'} = 2\,\text{cm}\) und \(\overline{AB} = 4.2\,\text{cm}\). Wie lang ist \(\overline{A'B'}\)?",
     r"<p>\(\overline{SA'} = 5\,\text{cm}\); \(\overline{A'B'} = 4.2 \cdot \tfrac{5}{3} = 7\,\text{cm}\).</p><p class=\"komm\">Mit \(\tfrac{2}{3}\) statt \(\tfrac{5}{3}\) gerechnet? Zu den Parallelen gehören die ganzen Strahlenabschnitte ab \(S\).</p>",
     fig([['s', [0, 0], [6.5, 0], 'verlaengerung'], ['s', [0, 0], [6.5, 9.1], 'verlaengerung'], ['s', [3, 0], [3, 4.2], 'hilfe'], ['s', [5, 0], [5, 7], 'hilfe'], ['p', [0, 0]], ['t', [0, 0], 'S', 'ecke', -8, 4], ['t', [3, 0], 'A', 'ecke', 0, 13], ['t', [5, 0], "A'", 'ecke', 0, 13], ['t', [3, 4.2], 'B', 'ecke', -8, -2], ['t', [5, 7], "B'", 'ecke', -8, -2]], '-0.8,7,-0.9', 200, 230)),
    ('5c', 2, r'Auf einer Karte im Massstab \(1 : 25\,000\) hat ein Wald die Fläche \(8\,\text{cm}^2\). Wie gross ist er in Wirklichkeit?',
     r'<p>Längenfaktor \(25\,000\), Flächenfaktor \(25\,000^2\): \(8 \cdot 625\,000\,000\,\text{cm}^2 = 5\,000\,000\,000\,\text{cm}^2 = 500\,000\,\text{m}^2 = 0.5\,\text{km}^2\).</p>', ''),
    ('5d', 2, r'Warum wächst die Fläche einer Figur mit \(k^2\), wenn alle Längen mit \(k\) wachsen?',
     r'<p>Eine Fläche ist Länge mal Länge (z. B. \(a \cdot h\)). Werden beide mit \(k\) multipliziert, wird das Produkt mit \(k \cdot k = k^2\) multipliziert. Bei \(k = 2\) passen vier Original-Kopien in das Bild.</p>', ''),
    ('5e', 2, r'Eine \(1.6\,\text{m}\) grosse Person wirft einen \(2\,\text{m}\) langen Schatten, ein Turm gleichzeitig einen \(30\,\text{m}\) langen. Wie hoch ist der Turm? Skizziere die ähnlichen Dreiecke.',
     r'<p>\(\tfrac{h}{30} = \tfrac{1.6}{2}\), also \(h = 24\,\text{m}\).</p>', ''),
], zwei=False)
k5 = kapitel(5, 'aehnlichkeit', 'Ähnlichkeit', 40,
             r'Du führst eine zentrische Streckung aus, nutzt Ähnlichkeit und Strahlensätze für Berechnungen und unterscheidest den Faktor \(k\) für Längen vom Faktor \(k^2\) für Flächen.',
             ('g5-2-lp-aehnlichkeit', 'Streckung und Ähnlichkeit'), sim5, ('g5-2-lp-kontrolle-aehnlichkeit', 'Kontrollfragen zur Ähnlichkeit'),
             fest5, [uebung('streckung', 'Längen und Flächen strecken'), uebung('strahlensatz', 'Schatten und Strahlensatz')],
             auf5, f'<a href="{TD}#strahlensaetze">Themenseite 5.2d, Strahlensätze</a> und <a href="{TD}#aehnlichkeit">ähnliche Figuren</a>', komp='K3')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · Sek I · GF 5.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Rechteck, Einheiten, Winkelarten, Verhältnisse und der Satz des Pythagoras. Wenn das wackelt: <a href="''' + TA + '''#theorie">Themenseite 5.2a, Pythagoras</a> und <a href="''' + TB + '''#theorie">5.2b, Rechteck</a>.</p>
      ''' + clipkarte('g5-2a-pythagoras', 'Der Satz des Pythagoras') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Ein Rechteck ist \(6\,\text{cm}\) lang und \(4\,\text{cm}\) breit. Berechne Fläche und Umfang.',
     r'<p>\(A = 24\,\text{cm}^2\); \(U = 20\,\text{cm}\).</p>', ''),
    ('0b', 2, r'Wie viele \(\text{cm}^2\) sind \(1\,\text{m}^2\)? Schreib \(250\,\text{cm}^2\) in \(\text{m}^2\).',
     r'<p>\(1\,\text{m}^2 = 100\,\text{cm} \cdot 100\,\text{cm} = 10\,000\,\text{cm}^2\); \(250\,\text{cm}^2 = 0.025\,\text{m}^2\).</p><p class="komm">Zwischen benachbarten Flächeneinheiten (\(\text{cm}^2\), \(\text{dm}^2\), \(\text{m}^2\)) liegt der Faktor \(100\), nicht \(10\).</p>', ''),
    ('0c', 2, r'Ein rechtwinkliges Dreieck hat die Katheten \(5\,\text{cm}\) und \(12\,\text{cm}\). Wie lang ist die Hypotenuse?',
     r'<p>\(\sqrt{25 + 144} = \sqrt{169} = 13\,\text{cm}\).</p><p class="komm">Falsch? Der Clip oben erklärt den Satz; Kapitel 3 braucht ihn.</p>', ''),
    ('0d', 2, r'Löse \(\dfrac{x}{4} = \dfrac{6}{8}\).',
     r'<p>\(x = 4 \cdot \tfrac{6}{8} = 3\).</p><p class="komm">Verhältnisgleichungen braucht Kapitel 5.</p>', ''),
    ('0e', 2, r'Spitz, recht oder stumpf? \(95°\); \(90°\); \(30°\); \(179°\).',
     r'<p>stumpf; recht; spitz; stumpf.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/planimetrie/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.2 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Skizze und Rechenweg; Taschenrechner erlaubt.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Tüfteln und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 2; G3 → 3; G4, G5 → 4; G6, G7 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Planimetrie, Version 1.0 (06.10.2026). Gebaut aus scripts/lp/planimetrie/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlage: Leitfaden des Auftraggebers (HOWTO-PlaniLP.md,
     06.10.2026) und HOWTO-leitprogramme.md.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 Planimetrie (gedruckte Seite 44), wörtlich:
       K1  geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und
           spezielle Dreiecke, Parallelogramm, Rhombus, Trapez, Kreis) beschreiben
       K2  deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez,
           Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge
           (Umfang, Flächeninhalt, Abstand) berechnen
       K3  die Ähnlichkeit für Berechnungen in der Ebene nutzen
     Kein Vermerk «auch ohne Hilfsmittel»: Taschenrechner erlaubt. Unterstützend 5.1: Skizzen zur
     Abschätzung der Plausibilität.

     Kompetenzmatrix (Kompetenz | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | 1, 3, 4 | 1a, 1b, 1d, 1e, 3e, 4e | G1, G3
       K2 | 1–4     | 1c, 2a–2e, 3a–3d, 4a–4g | G1–G5
           (berechnet: Höhe, Winkel, Mittellinie, Bogen, Sektor, Segment; erkannt/gezeichnet: Seiten-,
            Winkelhalbierende, Mittelsenkrechte, Sehne, Sekante, Tangente; Abstand als Höhe; Grad)
       K3 | 5       | 5a–5e | G6, G7
     Kein Kapitelziel ohne Kompetenz.

     Bewusst weggelassen (→ Themenseiten 5.2a–d): Kongruenzsätze und Konstruktionen, Dreiecks-
     ungleichung, Katheten- und Höhensatz, Sehnen- und Tangentenvierecke, regelmässige Vielecke,
     die Herleitung von π, Ähnlichkeitssätze als eigenes Thema. Trigonometrische Berechnungen: 5.3.

     Konventionen wie auf den Themenseiten: A, B, C gegen den Uhrzeigersinn, a gegenüber A, h_a, s_a,
     w_α, m_c; A = ½ g h; Mittellinie m = ½(a + c); φ, b, A_S; Z, k. Farben: Figur blau, Hilfslinie und
     Element orange, Fläche und Ergebnis grün, Fehler rot.

     Muster je Kapitel: ① Einführungsclip → ② Geometrie-Arbeitsbereich mit Aufgabenleiste (Figur
     verändern, Hilfslinie antippen, Grösse eingeben) → ③ Kontrollclip mit Fragen → Festhalten →
     ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als
     PDF aus LaTeX (downloads/leitprogramme/planimetrie/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Planimetrie</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.2</span>
    </div>
  </div>
</header>

<div class="huelle">
<div class="raster">

  <nav class="schiene" aria-label="Kapitelnavigation">
    <h2 id="ablauf">Ablauf</h2>
    <p class="lekt">Vorab</p>
    <ol>
      <li><a href="#k0"><span class="nr">0</span><span>Vorwissen</span></a></li>
    </ol>
    <p class="lekt">Kapitel</p>
    <ol>
      <li><a href="#k1"><span class="nr">1</span><span>Dreiecke</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Dreiecksfläche</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Vierecke</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Kreis</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Ähnlichkeit</span></a></li>
    </ol>
    <p class="lekt">Abschluss</p>
    <ol>
      <li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li>
    </ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 6 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Im Arbeitsbereich veränderst du die Figur, tippst Hilfslinien an und gibst Ergebnisse ein — er zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.2 — Taschenrechner erlaubt:</p>
        <ul>
          <li><b>K1</b> geometrische Sachverhalte von elementaren Objekten (Quadrat, Rechteck, allgemeine und spezielle Dreiecke, Parallelogramm, Rhombus, Trapez, Kreis) beschreiben — Kapitel 1, 3, 4</li>
          <li><b>K2</b> deren Elemente (Höhen, Seiten- und Winkelhalbierende, Mittelsenkrechte, Mittellinie im Trapez, Sehne, Sekante, Tangente, Sektor, Segment, Winkel und Winkelmass) und Zusammenhänge (Umfang, Flächeninhalt, Abstand) berechnen — Kapitel 1–4. Berechnet werden Höhe, Winkel, Mittellinie, Bogen, Sektor und Segment; Seiten- und Winkelhalbierende, Mittelsenkrechte, Sehne, Sekante und Tangente werden erkannt und gezeichnet; der Abstand kommt als Höhe (Lot) vor; Winkel nur in Grad (Bogenmass: Teilgebiet 5.4).</li>
          <li><b>K3</b> die Ähnlichkeit für Berechnungen in der Ebene nutzen — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Nicht hier, sondern auf den Themenseiten <a href="''' + TA + '''">5.2a</a>–<a href="''' + TD + '''">5.2d</a>: Kongruenzsätze und Konstruktionen, Katheten- und Höhensatz, regelmässige Vielecke. Trigonometrie: Teilgebiet 5.3.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Planimetrie · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (06.10.2026): Vorwissen 10 (vorab) · K1 35 · K2 40 · K3 40 · K4 40 · K5 40 · Gesamttest 30 = 235 min
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
