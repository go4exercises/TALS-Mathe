"""Baut leitprogramme/exp-log-funktionen.html aus einer Kapitelbeschreibung (04.10.2026).

  python3 scripts/lp/exp-log-funktionen/seite.py

Leitprogramm zum Teilgebiet SP 3.4 (Themenseiten s3-4a-exponentialfunktionen.html und
s3-4b-logarithmusfunktionen.html), alle vier RLP-Kompetenzen. Liest Kopf (inkl. <style>) und
Grundskript aus der bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt
die Seite neu. Beim ersten Lauf kommt das Gerüst aus leitprogramme/polynomfunktionen.html, mit
eigenem Titel und eigenen localStorage-Schlüsseln. Wiederholbar: zweimal laufen lassen ergibt
dieselbe Datei. Danach Pre-Flight und python3 scripts/build-seo.py. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/exp-log-funktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/polynomfunktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Polynomfunktionen</title>',
                      '<title>Leitprogramm Exponential- und Logarithmusfunktionen</title>')
    alt = alt.replace('lp-polynom-', 'lp-explog-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Polynomfunktionen', '\n/* ════════ Exponential- und Logarithmusfunktionen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Polynomfunktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Exponential- und Logarithmusfunktionen — Simulationen')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Schwerpunktfach · Leitprogramm Polynomfunktionen', 'Schwerpunktfach · Leitprogramm Exponential- und Logarithmusfunktionen')
fuss = fuss.replace('Polynomfunktionen', 'Exponential- und Logarithmusfunktionen')
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 4. Oktober 2026', fuss)

CSS = '''
/* ════════ Exponential- und Logarithmusfunktionen (04.10.2026) — Kapitelmuster wie Polynomfunktionen ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Eigen sind die
   Farben: Exponentialkurve blau, Startwert orange, Logarithmuskurve und Umkehrfunktion grün. */
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
.hilfs-schalter,.sim-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--lila-hell);border:1px solid var(--lila-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sim input[type=range]:disabled{opacity:.4}
/* Farben im ganzen Leitprogramm: blau = Exponentialkurve und Basis a, orange = Startwert
   und Faktor, grün = Logarithmuskurve und Umkehrfunktion, rot = Gegenbeispiel, Tinte =
   neutral (Asymptote, Sättigungswert, y = x). Dieselben Farben tragen die Clips (farbe 1–5). */
.sim .normal{stroke-dasharray:5 4;stroke:var(--tinte-2);fill:none}
.sim .asym{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 3;fill:none}
.sim .zielkurve{stroke:var(--gruen);stroke-width:4;opacity:.38;fill:none}
.p-start{fill:var(--orange)} .p-pkt{fill:var(--tinte)} .p-lauf{fill:var(--tinte)}
svg.mini .p-pkt{fill:var(--tinte)}
.sim .kurve.gruen,svg.mini .kurve.gruen{stroke:var(--gruen)}
svg.mini .kurve.g2{stroke:var(--tinte-2);stroke-dasharray:4 3}
.sim .kurve.gestrichelt{stroke-dasharray:7 5}
.sim .rueckstand{stroke:var(--orange);stroke-width:2.2;stroke-dasharray:3 3}
.mini-reihe svg.mini{background:var(--karte)}
.sim-formel{line-height:1.6}
/* Ein Punkt direkt hinter einer Formel landet sonst allein auf der naechsten Zeile. */
.nb{white-space:nowrap}
'''


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf — so rechnet
    die Bibliothek), abgerundet auf Sekunden (HOWTO-leitprogramme §7)."""
    d = json.load(open(R + 'clips/' + name + '.json'))
    t = int(sum(s['dauer'] for s in d['szenen']))
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
          {'<svg class="mini gross ue-bild" role="img" aria-label="Graph zur Aufgabe"></svg>' if bild else ''}
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(name, var, label, mn, mx, st, val, akz):
    return (f'<div class="sl-grp akz-{akz}"><label for="{name}-{var}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{name}-{var}" data-p="{var}" min="{mn}" max="{mx}" step="{st}" value="{val}">'
            f'<span class="sl-val"></span></div>')


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


def kapitel(n, kid, titel, komp, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-sf">SP 3.4 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TA = '../schwerpunkt/s3-4a-exponentialfunktionen.html'
TB = '../schwerpunkt/s3-4b-logarithmusfunktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Exponentialkurve y gleich a hoch x mit den Punkten bei x gleich minus eins, null und eins"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Asymptote \\(y = 0\\) (gestrichelt)</label>
        <div class="sl-row">
          {regler('s1', 'a', 'Basis a', 0.2, 4, 0.05, 2, 'blau')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Exponentialfunktion</div>
          <p>\[ y = f(x) = a^x, \qquad a \in \mathbb{R}^+,\ a \neq 1 \]</p>
          <p>heisst <b>Exponentialfunktion</b> mit der <b>Basis</b> \(a\). Die Variable \(x\) steht im Exponenten: Geht \(x\) um \(1\) weiter, wird \(y\) mit \(a\) multipliziert.</p>
          <ul>
            <li>\(D = \mathbb{R}\), \(W = \mathbb{R}^+\) — \(a^x\) ist immer positiv, es gibt <b>keine Nullstelle</b>.</li>
            <li>Alle Kurven gehen durch \((0 \mid 1)\), denn \(a^0 = 1\); bei \(x = 1\) steht die Basis: \((1 \mid a)\).</li>
            <li><b>Asymptote</b> ist die \(x\)-Achse \((y = 0)\).</li>
            <li>\(a \gt 1\): die Kurve steigt (<b>Wachstum</b>); \(0 \lt a \lt 1\): sie fällt (<b>Zerfall</b>).</li>
            <li>\(y = a^{-x} = \left(\frac{1}{a}\right)^{x}\): Die Basen \(a\) und \(\frac{1}{a}\) gehören zu Kurven, die an der \(y\)-Achse gespiegelt sind.</li>
          </ul>
          <p><b>Basis aus einem Punkt:</b> Geht die Kurve durch \((2 \mid 9)\), ist \(a^2 = 9\), also \(a = 3\) — nur die positive Lösung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(2^x\) und \(x^2\) verwechseln: Bei \(2^x\) steht die Variable im Exponenten. Und der Exponent ist kein Faktor: \(2^3 = 8\), nicht \(6\).</p>
          <p>Ein negativer Exponent macht nichts negativ: \(5^{-1} = \frac{1}{5}\), nicht \(-5\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Ordne zu: (1) \(y = 3^x\) (2) \(y = \left(\tfrac13\right)^x\) (3) \(y = 1.5^x\) (4) \(y = \left(\tfrac23\right)^x\)',
     r'<p>(1) → C, (2) → A, (3) → D, (4) → B.</p><p class="komm">Zuerst die Richtung: Steigende Kurven haben eine Basis grösser als 1. Dann die Steilheit: Bei \(x = 1\) steht die Basis — \(3\) liegt höher als \(1.5\), \(\tfrac13\) tiefer als \(\tfrac23\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-e="1,0.3333333333333333,0" data-fenster="-3,3,-1,5" data-titel="A"></svg><svg class="mini" data-e="1,0.6666666666666666,0" data-fenster="-3,3,-1,5" data-titel="B"></svg><svg class="mini" data-e="1,3,0" data-fenster="-3,3,-1,5" data-titel="C"></svg><svg class="mini" data-e="1,1.5,0" data-fenster="-3,3,-1,5" data-titel="D"></svg></div>'),
    ('1b', 3, r'\(f(x) = 4^x\): Berechne ohne Taschenrechner \(f(-1)\), \(f(0.5)\) und \(f(1.5)\).',
     r'<p>\(f(-1) = \tfrac14\) · \(f(0.5) = \sqrt{4} = 2\) · \(f(1.5) = \left(\sqrt{4}\right)^3 = 8\).</p><p class="komm">Ein halber Exponent ist eine Quadratwurzel (Teilgebiet 1.2).</p>', ''),
    ('1c', 3, r'Bestimme die Basis \(a\) so, dass \(y = a^x\) durch den Punkt geht: \(P(2 \mid 25)\) · \(Q(-2 \mid 16)\) · \(R(3 \mid 0.001)\).',
     r'<p>\(a^2 = 25 \Rightarrow a = 5\) · \(a^{-2} = 16 \Rightarrow a^2 = \tfrac{1}{16} \Rightarrow a = \tfrac14\) · \(a^3 = 0.001 \Rightarrow a = 0.1\).</p><p class="komm">Immer nur die positive Lösung: Die Basis ist positiv.</p>', ''),
    ('1d', 3, r'Begründe: (a) Warum hat \(y = a^x\) keine Nullstelle? (b) Warum schliesst man die Basen \(a = 1\) und \(a \lt 0\) aus?',
     r'<p>(a) Eine positive Zahl, beliebig oft mit sich multipliziert, als Kehrwert oder Wurzel genommen, bleibt positiv: \(a^x \gt 0\) für alle \(x\).</p><p>(b) \(a = 1\) gibt die konstante Funktion \(y = 1\) — kein Wachstum, kein Zerfall. Bei \(a \lt 0\) gibt es Ausdrücke wie \((-2)^{0.5}\) nicht.</p>', ''),
], zwei=False)
k1 = kapitel(1, 'exponentialfunktion', 'Die Exponentialfunktion', 'K1', 40,
             r'Du zeichnest und erkennst Graphen von \(y = a^x\), sagst an der Basis, ob die Kurve steigt oder fällt, und bestimmst die Basis aus einem Punkt.',
             ('s3-4-lp-exponentialfunktion', 'Die Exponentialfunktion'),
             sim1, ('s3-4-lp-kontrolle-exponentialfunktion', 'Kontrollfragen zur Exponentialfunktion'),
             fest1, [uebung('exp-wert', 'Funktionswert berechnen'), uebung('basis-punkt', 'Basis aus einem Punkt'),
                     uebung('graf-basis', 'Basis am Graphen ablesen', True)],
             auf1, f'<a href="{TA}#definition">Themenseite 3.4a, Definition und Eigenschaften</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Wachstumskurve N von t gleich N null mal a hoch t, mit einem Läufer"></svg>
        <div class="sl-row">
          {regler('s2', 'n0', 'N₀', 50, 500, 50, 200, 'orange')}
          {regler('s2', 'p', 'Änderung % je Schritt', -50, 100, 5, 50, 'blau')}
          {regler('s2', 't', 'Läufer t', 0, 6, 1, 0, 'grau')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wachstum und Zerfall</div>
          <p>\[ N(t) = N_0 \cdot a^{t} \]</p>
          <p>\(N_0 = N(0)\) ist der <b>Startwert</b>, \(a\) der <b>Wachstumsfaktor</b> je Zeitschritt.</p>
          <ul>
            <li>Zunahme um \(p\,\%\): \(a = 1 + \frac{p}{100}\) — zum Beispiel \(+5\,\%\) gibt \(a = 1.05\).</li>
            <li>Abnahme um \(p\,\%\): \(a = 1 - \frac{p}{100}\) — zum Beispiel \(-20\,\%\) gibt \(a = 0.8\).</li>
          </ul>
          <p><b>Verdopplungszeit</b> \(T\): \(N(t) = N_0 \cdot 2^{t/T}\). <b>Halbwertszeit</b> \(T\): \(N(t) = N_0 \cdot \left(\tfrac12\right)^{t/T}\). Nach \(j\) solchen Zeiten ist \(j\)-mal verdoppelt bzw. halbiert.</p>
          <p><b>Exponentiell oder linear?</b> Bei gleichen Zeitschritten ist bei exponentiellem Wachstum der <b>Quotient</b> aufeinanderfolgender Werte gleich, bei linearem die <b>Differenz</b>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Prozentsatz statt des Faktors einsetzen: \(+30\,\%\) heisst mal \(1.3\), nicht mal \(0.3\).</p>
          <p>Und linear rechnen: Drei Halbwertszeiten sind \(\left(\tfrac12\right)^3 = \tfrac18\), nicht \(\tfrac13\) oder \(\tfrac16\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'Gib den Wachstumsfaktor an: Zunahme um \(8\,\%\) · Abnahme um \(15\,\%\). Und umgekehrt: Um wie viel Prozent ändert sich eine Grösse mit dem Faktor \(0.97\)?',
     r'<p>\(1.08\) · \(0.85\) · Abnahme um \(3\,\%\).</p>', ''),
    ('2b', 4, r'Ein Kapital von \(2000\) CHF wird zu \(5\,\%\) Jahreszins angelegt, der Zins wird mitverzinst. (a) Stell das Modell \(K(n)\) auf. (b) Berechne \(K(2)\). (c) Begründe, warum der Zinsbetrag jedes Jahr grösser wird.',
     r'<p>(a) \(K(n) = 2000 \cdot 1.05^{n}\). (b) \(K(2) = 2000 \cdot 1.1025 = 2205\) CHF.</p><p>(c) Verzinst wird immer das ganze Kapital samt den bisherigen Zinsen — \(5\,\%\) einer grösseren Zahl sind mehr.</p>', ''),
    ('2c', 3, r'Iod-131 hat eine Halbwertszeit von \(8\) Tagen. Stell das Modell für \(120\) mg auf und berechne, wie viel nach \(24\) Tagen übrig ist.',
     r'<p>\(m(t) = 120 \cdot \left(\tfrac12\right)^{t/8}\); \(m(24) = 120 \cdot \left(\tfrac12\right)^{3} = 15\) mg.</p>', ''),
    ('2d', 3, r'Eine Messreihe (je ein Jahr Abstand): \(40,\ 60,\ 90,\ 135\). Ist das Wachstum linear oder exponentiell? Begründe und stell das Modell auf.',
     r'<p>Die Differenzen \(20, 30, 45\) sind nicht gleich, die Quotienten schon: \(\tfrac{60}{40} = \tfrac{90}{60} = \tfrac{135}{90} = 1.5\). Exponentiell: \(N(t) = 40 \cdot 1.5^{t}\).</p>', ''),
], zwei=False)
k2 = kapitel(2, 'wachstum-und-zerfall', 'Wachstum und Zerfall', 'K2', 45,
             r'Du stellst ein Modell \(N(t) = N_0 \cdot a^t\) auf, übersetzt Prozente in Faktoren, rechnest mit Verdopplungs- und Halbwertszeit und erkennst exponentielles Wachstum in einer Tabelle.',
             ('s3-4-lp-wachstum-zerfall', 'Wachstum und Zerfall'),
             sim2, ('s3-4-lp-kontrolle-wachstum', 'Kontrollfragen zu Wachstum und Zerfall'),
             fest2, [uebung('prozent-faktor', 'Prozent und Faktor'), uebung('wachstum-wert', 'Modell auswerten'),
                     uebung('halbwertszeit', 'Halbwerts- und Verdopplungszeit')],
             auf2, f'<a href="{TA}#aufgaben">Themenseite 3.4a, Aufgaben A4–A6</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Zielkurve c hoch x und gestrichelt die nachgebaute Kurve a hoch b mal x"></svg>
        <label class="sim-schalter"><input type="checkbox"> Basis \\(e\\) statt \\(2\\)</label>
        <div class="sl-row">
          {regler('s3', 'c', 'Ziel cˣ, c =', 0, 6, 1, 4, 'blau')}
          {regler('s3', 'b', 'b', -3, 3, 0.05, 1, 'orange')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">e-Funktion und Basiswechsel</div>
          <p>Die <b>Eulersche Zahl</b> \(e \approx 2.71828\) ist der Grenzwert von \(\left(1 + \frac1n\right)^n\) für immer grössere \(n\). Die <b>natürliche Exponentialfunktion</b> ist</p>
          <p>\[ y = e^{x} \]</p>
          <p>Sie liegt für \(x \gt 0\) zwischen \(2^x\) und \(3^x\) und geht durch \((0 \mid 1)\) und \((1 \mid e)\).</p>
          <p><b>Basiswechsel:</b> Eine Basis lässt sich als Potenz einer anderen schreiben:</p>
          <p>\[ c^{x} = \left(a^{b}\right)^{x} = a^{b\,x} \quad \text{mit } c = a^{b} \]</p>
          <p>Beispiele: \(8^x = 2^{3x}\), \(9^x = 3^{2x}\), \(\left(\tfrac14\right)^x = 2^{-2x}\). Im Bild: Die Kurve von \(a^x\), in \(x\)-Richtung gestaucht oder gestreckt.</p>
          <p><b>Zur Basis \(e\)</b> geht es immer, mit dem natürlichen Logarithmus \(\ln\) (Teilgebiet 1.3):</p>
          <p>\[ a^{x} = e^{b\,x} \quad \text{mit } b = \ln a \]</p>
          <p>\(b \gt 0\) (also \(a \gt 1\)): Wachstum; \(b \lt 0\) (also \(0 \lt a \lt 1\)): Zerfall.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Basiswechsel als Division rechnen: \(8^x = 2^{3x}\), weil \(2^3 = 8\) — nicht \(2^{4x}\), weil \(8 : 2 = 4\).</p>
          <p>Und das Minus vergessen: \(\left(\tfrac12\right)^x = e^{-0.69\,x}\), denn \(\ln \tfrac12 \lt 0\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 3, r'Schreib zur Basis \(2\): \(16^x\) · \(\left(\tfrac18\right)^x\) · \(\left(\sqrt{2}\right)^x\).',
     r'<p>\(2^{4x}\) · \(2^{-3x}\) · \(2^{0.5x}\).</p><p class="komm">Immer die Basis als Potenz von 2 schreiben: \(16 = 2^4\), \(\tfrac18 = 2^{-3}\), \(\sqrt2 = 2^{1/2}\).</p>', ''),
    ('3b', 3, r'Schreib als \(c^x\): \(e^{(\ln 5)\,x}\) · \(e^{-x}\) · \(e^{3x}\).',
     r'<p>\(5^x\) · \(\left(\tfrac{1}{e}\right)^x\) · \(\left(e^{3}\right)^x\).</p><p class="komm">\(e^{\ln 5} = 5\): Die Exponentialfunktion und der natürliche Logarithmus heben sich auf.</p>', ''),
    ('3c', 2, r'Wachstum oder Zerfall? \(N(t) = 20 \cdot e^{-0.3t}\) · \(N(t) = 5 \cdot e^{0.05t}\) · \(N(t) = 8 \cdot 0.8^{-t}\).',
     r'<p>Zerfall · Wachstum · Wachstum, denn \(0.8^{-t} = 1.25^{t}\).</p>', ''),
    ('3d', 3, r'Warum liegt \(e^x\) für \(x \gt 0\) zwischen \(2^x\) und \(3^x\) — und wie ist es für \(x \lt 0\)?',
     r'<p>Für \(x \gt 0\) wächst \(a^x\) mit der Basis: \(2 \lt e \lt 3\), also \(2^x \lt e^x \lt 3^x\).</p><p>Für \(x \lt 0\) kehrt sich die Reihenfolge um, denn dort ist \(a^x = \frac{1}{a^{-x}}\): \(3^x \lt e^x \lt 2^x\). Bei \(x = 0\) gehen alle durch \((0 \mid 1)\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-e="1,2.718281828459045,0;1,2,0;1,3,0" data-fenster="-2,2,-0.5,5" data-punkte="0,1"></svg></div>'),
], zwei=False)
k3 = kapitel(3, 'e-funktion', 'Die e-Funktion und der Basiswechsel', 'K3', 40,
             r'Du kennst die Zahl \(e\) und die e-Funktion, schreibst eine Exponentialfunktion zu einer anderen Basis um — auch zur Basis \(e\) — und erkennst am Exponenten Wachstum und Zerfall.',
             ('s3-4-lp-e-funktion', 'Die e-Funktion und der Basiswechsel'),
             sim3, ('s3-4-lp-kontrolle-e-funktion', 'Kontrollfragen zur e-Funktion'),
             fest3, [uebung('basiswechsel', 'Basis wechseln'), uebung('e-form', 'Von der e-Form zurück'),
                     uebung('wachstum-zerfall', 'Wachstum oder Zerfall?')],
             auf3, f'<a href="{TA}#theorie">Themenseite 3.4a, e-Funktion und Basiswechsel</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Sättigungskurve f von t gleich S minus Klammer S minus A mal e hoch minus k t, mit der Asymptote y gleich S"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Asymptote \\(y = S\\) und Rückstand bei \\(t = 10\\)</label>
        <div class="sl-row">
          {regler('s4', 'A', 'Startwert A', 0, 100, 5, 80, 'orange')}
          {regler('s4', 'S', 'Sättigung S', 0, 100, 5, 20, 'grau')}
          {regler('s4', 'k', 'k', 0.05, 1, 0.01, 0.07, 'grau')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sättigung — beschränktes Wachstum</div>
          <p>Viele Vorgänge streben nicht ins Unendliche, sondern auf einen <b>Sättigungswert</b> \(S\) zu:</p>
          <p>\[ f(t) = S - (S - A)\,e^{-k t}, \qquad k \gt 0 \]</p>
          <p>mit <b>Startwert</b> \(A = f(0)\). Für \(t \to \infty\) geht \(e^{-kt} \to 0\), also \(f(t) \to S\): Die Waagrechte \(y = S\) ist <b>Asymptote</b>.</p>
          <ul>
            <li>\(A \lt S\): Die Kurve steigt gegen \(S\) (Erwärmen, Aufladen).</li>
            <li>\(A \gt S\): Die Kurve fällt gegen \(S\) (Abkühlen).</li>
          </ul>
          <p>Der <b>Rückstand</b> \(S - f(t) = (S - A)\,e^{-kt}\) ist eine reine Zerfallsfunktion. Halbiert er sich alle \(T\) Minuten, ist er nach \(2T\) auf einen Viertel gesunken.</p>
          <p>Beispiel Kaffee: \(f(t) = 20 + 60\,e^{-kt}\) mit halbiertem Rückstand alle 10 min: \(80 \to 50 \to 35 \to 27.5\) °C.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Wert statt des Rückstands halbieren: Nach 10 min hat der Kaffee \(50\) °C, nicht \(40\) °C — halbiert wird der Abstand \(60\) zur Raumtemperatur.</p>
          <p>Und den Sättigungswert mit dem Startwert verwechseln: \(f(0) = S - (S - A) = A\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'\(f(t) = 30 - 20\,e^{-0.5t}\): Gib Startwert, Sättigungswert und Asymptote an. Steigt oder fällt die Kurve?',
     r'<p>\(A = f(0) = 30 - 20 = 10\), \(S = 30\), Asymptote \(y = 30\). Sie steigt, denn \(A \lt S\).</p>', ''),
    ('4b', 4, r'Ein Akku wird von \(20\,\%\) auf \(100\,\%\) geladen; der Rückstand zur vollen Ladung halbiert sich jede Stunde. (a) Stell das Modell auf. (b) Berechne die Ladung nach \(1\), \(2\) und \(3\) Stunden.',
     r'<p>(a) \(f(t) = 100 - 80\,e^{-kt}\) mit \(e^{-k} = \tfrac12\), also \(f(t) = 100 - 80 \cdot \left(\tfrac12\right)^{t}\).</p><p>(b) \(60\,\%\), \(80\,\%\), \(90\,\%\).</p>', ''),
    ('4c', 2, r'Skizziere je einen Sättigungsprozess mit \(A \lt S\) und mit \(A \gt S\) und zeichne die Asymptote ein.',
     r'<p>\(A \lt S\): steigende Kurve, anfangs steil, dann immer flacher unter der Asymptote \(y = S\). \(A \gt S\): fallende Kurve über der Asymptote.</p>',
     ''),
    ('4d', 3, r'Begründe: (a) Warum erreicht \(f(t) = S - (S-A)\,e^{-kt}\) den Wert \(S\) nie? (b) Warum ist der Rückstand \(S - f(t)\) eine Zerfallsfunktion?',
     r'<p>(a) \(e^{-kt}\) ist für jedes \(t\) positiv, also bleibt ein Rückstand \((S - A)\,e^{-kt} \neq 0\).</p><p>(b) \(S - f(t) = (S - A)\,e^{-kt} = (S - A) \cdot \left(e^{-k}\right)^{t}\) mit der Basis \(e^{-k} \lt 1\) — ein Zerfall.</p>', ''),
], zwei=False)
k4 = kapitel(4, 'saettigung', 'Sättigung', 'K2', 35,
             r'Du liest aus einem Sättigungsmodell Startwert, Sättigungswert und Asymptote ab, berechnest Werte über den halbierten Rückstand und unterscheidest Erwärmen von Abkühlen.',
             ('s3-4-lp-saettigung', 'Sättigung'),
             sim4, ('s3-4-lp-kontrolle-saettigung', 'Kontrollfragen zur Sättigung'),
             fest4, [uebung('saettigung-lesen', 'Startwert und Sättigungswert'), uebung('saettigung-wert', 'Mit dem Rückstand rechnen'),
                     uebung('saettigung-art', 'Steigt oder fällt?')],
             auf4, f'<a href="{TA}#saettigung">Themenseite 3.4a, Sättigungsprozesse</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Logarithmuskurve und die gespiegelte Exponentialkurve, mit einem Läufer"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Exponentialkurve und \\(y = x\\) (gestrichelt)</label>
        <div class="sl-row">
          {regler('s5', 'a', 'Basis a', 0, 4, 1, 1, 'blau')}
          {regler('s5', 'x', 'Läufer x', 0.1, 10, 0.1, 4, 'grau')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Logarithmusfunktion</div>
          <p>\[ y = f(x) = \log_a x, \qquad a \in \mathbb{R}^+,\ a \neq 1 \]</p>
          <p>ist die <b>Umkehrfunktion</b> der Exponentialfunktion \(y = a^x\): \(\log_a x\) ist der Exponent, mit dem man \(a\) potenzieren muss, um \(x\) zu erhalten.</p>
          <p>Ihr Graph ist die an der Winkelhalbierenden \(y = x\) <b>gespiegelte</b> Exponentialkurve — dabei tauschen die Rollen:</p>
          <ul>
            <li>\(D = \mathbb{R}^+\), \(W = \mathbb{R}\);</li>
            <li>Nullstelle \(x_0 = 1\): alle Kurven gehen durch \((1 \mid 0)\);</li>
            <li>Asymptote ist die \(y\)-Achse \((x = 0)\);</li>
            <li>\(a \gt 1\): steigt, immer flacher, aber ohne Grenze; \(0 \lt a \lt 1\): fällt.</li>
          </ul>
          <p>Spezialfälle: \(\ln x = \log_e x\) und \(\lg x = \log_{10} x\).</p>
          <p><b>Umkehrfunktion bestimmen:</b> nach \(x\) auflösen, dann \(x\) und \(y\) tauschen. Aus \(y = 2^x + 1\) wird \(x = \log_2(y - 1)\), also \(f^{-1}(x) = \log_2(x - 1)\).</p>
          <p><b>Gleichung mit \(x\) im Exponenten:</b> erst die Potenz freistellen, dann logarithmieren: \(3 \cdot 2^t = 96 \Rightarrow 2^t = 32 \Rightarrow t = \log_2 32 = 5\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Logarithmus als Division lesen: \(\log_2 32 = 5\), nicht \(16\) — gesucht ist der Exponent.</p>
          <p>Und die Definitionsmenge vergessen: \(\log_2 0\) und \(\log_2(-4)\) gibt es nicht. Bei \(\log_2(x - 1)\) muss \(x \gt 1\) sein.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 3, r'Berechne ohne Taschenrechner: \(\log_2 \tfrac18\) · \(\lg 1000\) · \(\log_5 \sqrt{5}\).',
     r'<p>\(-3\) · \(3\) · \(\tfrac12\).</p><p class="komm">\(2^{-3} = \tfrac18\), \(10^3 = 1000\), \(5^{1/2} = \sqrt5\).</p>', ''),
    ('5b', 4, r'Bestimme die Umkehrfunktion von \(f(x) = 3^x + 1\). Gib ihre Definitionsmenge, ihre Asymptote und ihre Nullstelle an.',
     r'<p>\(y = 3^x + 1 \Rightarrow 3^x = y - 1 \Rightarrow x = \log_3(y - 1)\); getauscht: \(f^{-1}(x) = \log_3(x - 1)\).</p><p>\(D = \,]1;\, \infty[\), Asymptote \(x = 1\), Nullstelle: \(x - 1 = 1 \Rightarrow x_0 = 2\).</p>', ''),
    ('5c', 4, r'Löse ohne Taschenrechner: (a) \(5 \cdot 2^{t} = 160\) (b) \(100 \cdot \left(\tfrac12\right)^{t/3} = 12.5\).',
     r'<p>(a) \(2^t = 32 \Rightarrow t = 5\). (b) \(\left(\tfrac12\right)^{t/3} = 0.125 = \left(\tfrac12\right)^{3} \Rightarrow \tfrac{t}{3} = 3 \Rightarrow t = 9\).</p>', ''),
    ('5d', 3, r'Abgebildet ist \(y = \log_2 x\). Lies \(\log_2 4\) und \(\log_2 0.5\) ab. Welcher Punkt liegt dann auf dem Graphen von \(y = 2^x\)?',
     r'<p>\(\log_2 4 = 2\), \(\log_2 0.5 = -1\).</p><p>Gespiegelt an \(y = x\): \((2 \mid 4)\) und \((-1 \mid 0.5)\) liegen auf \(y = 2^x\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-l="1,2,0" data-fenster="-1,7,-3,4" data-punkte="4,2;0.5,-1;1,0"></svg></div>'),
], zwei=False)
k5 = kapitel(5, 'logarithmusfunktion', 'Die Logarithmusfunktion', 'K4', 45,
             r'Du deutest die Logarithmusfunktion als Umkehrfunktion der Exponentialfunktion, zeichnest sie durch Spiegeln an \(y = x\), berechnest Logarithmen und Umkehrfunktionen und löst Gleichungen mit der Unbekannten im Exponenten.',
             ('s3-4-lp-logarithmusfunktion', 'Die Logarithmusfunktion'),
             sim5, ('s3-4-lp-kontrolle-logarithmus', 'Kontrollfragen zur Logarithmusfunktion'),
             fest5, [uebung('log-wert', 'Logarithmus berechnen'), uebung('umkehr-exp', 'Umkehrfunktion bestimmen'),
                     uebung('exp-gleichung', 'Gleichung lösen')],
             auf5, f'<a href="{TB}#definition">Themenseite 3.4b, Logarithmusfunktion</a>')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-sf">Vorwissen · SP 1.2 · 1.3 · 3.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Potenzen mit ganzen und gebrochenen Exponenten, der Logarithmus als gesuchter Exponent, Prozentrechnen und die Umkehrfunktion. Wenn das wackelt: <a href="../schwerpunkt/s1-2-potenzen.html">Teilgebiet 1.2</a>, <a href="../schwerpunkt/s1-3-logarithmen.html">Teilgebiet 1.3</a> und <a href="potenz-wurzelfunktionen.html#umkehren">Leitprogramm Potenz- und Wurzelfunktionen, Kapitel 4</a>.</p>
      ''' + clipkarte('s1-3-logarithmus-begriff', 'Logarithmen: der gesuchte Exponent', '0:59') + '''
      ''' + clipkarte('s3-2b-anim-spiegelung', 'Spiegeln an y = x: die Koordinaten tauschen', '0:53') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Berechne ohne Taschenrechner: \(2^{-3}\) · \(8^{2/3}\) · \(\left(2^{3}\right)^{2}\).',
     r'<p>\(\tfrac18\) · \(\left(\sqrt[3]{8}\right)^2 = 4\) · \(2^6 = 64\).</p><p class="komm">Falsch? Negativer Exponent = Kehrwert, gebrochener Exponent = Wurzel. <a href="../schwerpunkt/s1-2-potenzen.html">Teilgebiet 1.2, Potenzen</a></p>', ''),
    ('0b', 3, r'Berechne: \(\log_2 16\) · \(\lg 0.001\) · \(\log_3 1\).',
     r'<p>\(4\) · \(-3\) · \(0\).</p><p class="komm">Falsch? Der Logarithmus ist der gesuchte Exponent: \(2^{?} = 16\). Der Clip oben zeigt es. <a href="../schwerpunkt/s1-3-logarithmen.html">Teilgebiet 1.3, Logarithmen</a></p>', ''),
    ('0c', 2, r'Ein Preis von \(80\) CHF steigt um \(25\,\%\). Wie hoch ist er danach? Und wie hoch wäre er nach einer Senkung um \(25\,\%\)?',
     r'<p>\(80 \cdot 1.25 = 100\) CHF · \(80 \cdot 0.75 = 60\) CHF.</p><p class="komm">Prozentuale Änderung heisst: mit einem Faktor multiplizieren — genau das trägt Kapitel 2.</p>', ''),
    ('0d', 2, r'Der Punkt \((2 \mid 5)\) liegt auf dem Graphen einer umkehrbaren Funktion \(f\). Welcher Punkt liegt auf dem Graphen von \(f^{-1}\)?',
     r'<p>\((5 \mid 2)\) — beim Spiegeln an \(y = x\) tauschen die Koordinaten.</p><p class="komm">Falsch? Der zweite Clip oben. Genau diese Spiegelung trägt Kapitel 5.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. Ist 0b falsch, zuerst den Logarithmus wiederholen — ohne ihn gehen Kapitel 3 und 5 nicht.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/exp-log-funktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-sf">SP 3.4 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg, ganz ohne Taschenrechner: Alle vier Kompetenzen des Teilgebiets tragen im Lehrplan den Vermerk «auch ohne Hilfsmittel».<br>
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Simulation und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G2 → 1 · G3, G4 → 2 · G5 → 3 · G6 → 4 · G7, G8 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Exponential- und Logarithmusfunktionen, Version 1.0 (04.10.2026). Gebaut aus
     scripts/lp/exp-log-funktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     RLP-BM 2030, Schwerpunktfach 3.4 «Exponential- und Logarithmusfunktionen», die Kompetenzen
     wörtlich (Quelle ../Math-SP.pdf, Lerngebiet 3 «Funktionen»; gleich wie in den RLP-Boxen der
     Themenseiten s3-4a und s3-4b):
       K1  Exponentialfunktionen f: x ⟼ aˣ mit a ∈ ℝ⁺, a ≠ 1 grafisch darstellen (auch ohne Hilfsmittel)
       K2  Wachstums-, Zerfalls- und Sättigungsprozesse mit Hilfe von Exponentialfunktionen
           interpretieren, modellieren, visualisieren und berechnen (auch ohne Hilfsmittel)
       K3  die natürliche Exponentialfunktion (e-Funktion) visualisieren, Basiswechsel zu
           beliebiger Basis durchführen (auch ohne Hilfsmittel)
       K4  die Logarithmusfunktion als Umkehrfunktion der Exponentialfunktion berechnen und
           visualisieren (auch ohne Hilfsmittel)
     Ein Leitprogramm für beide Themenseiten (3.4a, 3.4b): K4 verlangt die Logarithmusfunktion
     ausdrücklich als Umkehrfunktion der Exponentialfunktion.

     Kompetenzmatrix (Kompetenz | ohne HM | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | ja | 1    | 1a–1d       | G1, G2
       K2 | ja | 2, 4 | 2a–2d, 4a–4d | G3, G4, G6
       K3 | ja | 3    | 3a–3d       | G5
       K4 | ja | 5    | 5a–5d       | G7, G8
     Kein Kapitelziel ohne Kompetenz. Der ganze Gesamttest ohne Taschenrechner.

     Bewusst weggelassen (→ Themenseiten): Transformationen y = k·a^(x−u) + v im Allgemeinen
     (Teilgebiet 3.1; hier nur die Verschiebung im Sättigungsmodell und bei der Umkehrfunktion),
     die log-Leiter, Radiokarbon, Dezibel und pH (Anwendungen von 3.4b), der Grenzwert von e als
     Animation (im Clip). Rechnen mit dem Taschenrechner (ln-Taste) nur in Beispielen —
     die Aufgaben sind ohne Hilfsmittel lösbar.

     Konventionen wie auf den Themenseiten: Basis a, Startwert N₀, b = ln a beim Basiswechsel,
     Sättigung f(t) = S − (S − A)·e^(−kt). Widerspruch auf Themenseite 3.4a: k heisst dort einmal
     Streckfaktor (k·a^(x−u) + v) und einmal Rate (e^(−kt)). Das Leitprogramm braucht nur die Rate
     und schreibt den Startwert eines Wachstums N₀ statt k.

     Muster je Kapitel: ① Einführungsclip → ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit
     Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF aus LaTeX (downloads/leitprogramme/exp-log-funktionen/*.tex).
     Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Exponential- und Logarithmusfunktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Schwerpunktfach 3.4</span>
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
    <p class="lekt">Lektion 1</p>
    <ol>
      <li><a href="#k1"><span class="nr">1</span><span>Exponentialfunktion</span></a></li>
    </ol>
    <p class="lekt">Lektion 2</p>
    <ol>
      <li><a href="#k2"><span class="nr">2</span><span>Wachstum und Zerfall</span></a></li>
    </ol>
    <p class="lekt">Lektion 3</p>
    <ol>
      <li><a href="#k3"><span class="nr">3</span><span>e-Funktion</span></a></li>
    </ol>
    <p class="lekt">Lektion 4</p>
    <ol>
      <li><a href="#k4"><span class="nr">4</span><span>Sättigung</span></a></li>
    </ol>
    <p class="lekt">Lektion 5</p>
    <ol>
      <li><a href="#k5"><span class="nr">5</span><span>Logarithmusfunktion</span></a></li>
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
          <li><b>② Tüfteln:</b> Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Schwerpunktfach 3.4 — alle vier Kompetenzen des Teilgebiets.</p>
        <ul>
          <li><b>K1</b> Exponentialfunktionen \\(f : x \\longmapsto a^x\\) mit \\(a \\in \\mathbb{R}^+,\\ a \\neq 1\\) grafisch darstellen <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1</li>
          <li><b>K2</b> Wachstums-, Zerfalls- und Sättigungsprozesse mit Hilfe von Exponentialfunktionen interpretieren, modellieren, visualisieren und berechnen <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 2, 4</li>
          <li><b>K3</b> die natürliche Exponentialfunktion (e-Funktion) visualisieren, Basiswechsel zu beliebiger Basis durchführen <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 3</li>
          <li><b>K4</b> die Logarithmusfunktion als Umkehrfunktion der Exponentialfunktion berechnen und visualisieren <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Ein Leitprogramm für beide Themenseiten <a href="../schwerpunkt/s3-4a-exponentialfunktionen.html">3.4a</a> und <a href="../schwerpunkt/s3-4b-logarithmusfunktionen.html">3.4b</a>, weil K4 die Logarithmusfunktion als Umkehrfunktion der Exponentialfunktion verlangt. Nicht hier, sondern auf den Themenseiten: Verschieben und Strecken im Allgemeinen (Teilgebiet 3.1) und die Anwendungen Dezibel, pH und Radiokarbon.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Exponential- und Logarithmusfunktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (04.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 45 · K3 40 · K4 35 · K5 45 · Gesamttest 30 = 245 min
body = (oben + band('Vorab', 'Vorwissen') + k0 + band(1, 'Die Exponentialfunktion') + k1
        + band(2, 'Wachstum und Zerfall') + k2 + band(3, 'e-Funktion und Basiswechsel') + k3
        + band(4, 'Sättigung') + k4 + band(5, 'Die Logarithmusfunktion') + k5
        + band('Abschluss', 'Gesamttest') + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
