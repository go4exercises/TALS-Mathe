"""Baut leitprogramme/potenz-wurzelfunktionen.html aus einer Kapitelbeschreibung (03.10.2026).

  python3 scripts/lp/potenz-wurzelfunktionen/seite.py

Deckt beide Themenseiten des Teilgebiets SP 3.2 ab (s3-2a und s3-2b): Die einzige
RLP-Kompetenz des Teilgebiets nennt die Wurzelfunktion ausdrücklich «als Umkehrfunktion
der Potenzfunktion», und das ist nur zusammen lernbar.

Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden Seite, ersetzt Inhalt und
Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf kommt das Gerüst aus
leitprogramme/lineare-funktionen.html, mit eigenem Titel und eigenen localStorage-Schlüsseln.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und
python3 scripts/build-seo.py. Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/potenz-wurzelfunktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/lineare-funktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Lineare Funktionen</title>',
                      '<title>Leitprogramm Potenz- und Wurzelfunktionen</title>')
    alt = alt.replace('lp-linfunktionen-', 'lp-potwurzel-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Lineare Funktionen', '\n/* ════════ Potenz- und Wurzelfunktionen', '\n/* ════════ Fassung 3'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Lineare Funktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Potenz- und Wurzelfunktionen — Simulationen')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Lineare Funktionen', 'Potenz- und Wurzelfunktionen')
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 3. Oktober 2026', fuss)

CSS = '''
/* ════════ Potenz- und Wurzelfunktionen (03.10.2026) — Fassung 4 des Kapitelmusters ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie im Leitprogramm
   Lineare Funktionen. Eigen sind die Farben der Kurven-Bausteine, die Spiegelkurve und
   die zwei Schreibweisen (Bruch, Wurzel) in der Live-Anzeige. */
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
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input:disabled{opacity:.35}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sim input[type=range]:disabled{opacity:.4}
/* Farben im ganzen Leitprogramm: blau = die Potenzkurve und ihr Faktor a, orange = der
   Exponent n, grün = Wurzelkurve, Umkehrfunktion und Startpunkt, rot = Gegenbeispiel und
   Polstelle, Tinte = neutral. Dieselben Farben tragen die Clips (farbe 1/2/3/4/5). */
.sim .kurve.g2,svg.mini .kurve.g2{stroke:var(--tinte-2)}
.sim .kurve.gruen,svg.mini .kurve.gruen{stroke:var(--gruen)}
.sim .normal{stroke-dasharray:5 4;stroke:var(--tinte-2);fill:none}
.sim .asym{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 3;fill:none}
.sim .umkehr{stroke:var(--gruen);stroke-width:2.4;fill:none}
.sim .umkehr.falsch{stroke:var(--rot)}
.sim .zielkurve{stroke:var(--gruen);stroke-width:4;opacity:.38;fill:none}
.p-b{fill:var(--orange)} .p-null{fill:var(--gruen)} .p-pkt{fill:var(--tinte)}
.p-m{fill:var(--tinte-2);font-weight:600}
svg.mini .p-pkt{fill:var(--tinte)} svg.mini .p-null{fill:var(--gruen)}
.mini-reihe svg.mini{background:var(--karte)}
.sim-formel .rot{color:var(--rot)}
/* Bruch und Wurzel in der Live-Anzeige — ohne MathJax, damit sie bei jedem Reglerzug
   sofort steht (ein typesetPromise pro Pixel wäre zu langsam). */
.br{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.1;margin:0 .15em}
.br > span:first-child{border-bottom:1.5px solid currentColor;padding:0 .25em}
.wz{white-space:nowrap} .wz > sup{font-size:.7em;margin-right:-.15em}
.wz .rad{border-top:1.5px solid currentColor;padding:0 .18em 0 .1em;margin-left:-.05em}
/* Ein Punkt direkt hinter einer Formel landet sonst allein auf der naechsten Zeile. */
.nb{white-space:nowrap}
'''


def clipkarte(datei, titel, zeit):
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
          {'<svg class="mini gross ue-bild" role="img" aria-label="Kurve zur Aufgabe"></svg>' if bild else ''}
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-sf">SP 3.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TA = '../schwerpunkt/s3-2a-potenzfunktionen.html'
TB = '../schwerpunkt/s3-2b-wurzelfunktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Potenzkurve y = a mal x hoch n, mit der Bezugskurve y = x Quadrat gestrichelt"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Bezugskurve \\(y = x^2\\) (gestrichelt)</label>
        <div class="sl-row">
          {regler('s1', 'a', 'a', -3, 3, 0.5, 1, 'blau')}
          {regler('s1', 'n', 'n', 2, 7, 1, 2, 'orange')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Potenzfunktion</div>
          <p>\[ f(x) = a \cdot x^{n}, \qquad a \in \mathbb{R}\setminus\{0\},\ n \in \mathbb{Z}\setminus\{0\} \]</p>
          <p>Für \(n \geq 2\) heisst der Graph <b>Parabel \(n\)-ter Ordnung</b>. \(D = \mathbb{R}\).</p>
          <p><b>Der Exponent \(n\) bestimmt die Form</b>, seine <b>Parität die Symmetrie</b>:</p>
          <ul>
            <li>\(n\) gerade \(\Rightarrow f(-x) = f(x)\): <b>gerade Funktion</b>, Graph achsensymmetrisch zur \(y\)-Achse.</li>
            <li>\(n\) ungerade \(\Rightarrow f(-x) = -f(x)\): <b>ungerade Funktion</b>, Graph punktsymmetrisch zum Ursprung.</li>
          </ul>
          <p><b>Feste Punkte:</b> Alle \(y = x^{n}\) mit \(n \geq 1\) gehen durch \((0 \mid 0)\) und \((1 \mid 1)\) — für \(n \lt 0\) fehlt die Stelle \(0\) in \(D\), \((1 \mid 1)\) bleibt. Bei \(x = -1\) trennen sie sich: gerades \(n\) gibt \(+1\), ungerades \(-1\).</p>
          <p><b>\(a\) streckt in \(y\)-Richtung:</b> \(|a| \gt 1\) schmaler, \(|a| \lt 1\) breiter, \(a \lt 0\) spiegelt an der \(x\)-Achse. Es gilt immer \(f(1) = a\).</p>
          <p>Zwischen \(-1\) und \(1\) wird die Kurve mit wachsendem \(n\) <em>flacher</em>, ausserhalb <em>steiler</em>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Der Exponent ist <em>kein Faktor</em>: \(x^{3}\) heisst \(x \cdot x \cdot x\), nicht \(3x\). Bei \(x = 2\) ist \(x^3 = 8\), nicht \(6\).</p>
          <p>Und \(a\) steht <em>ausserhalb</em> der Potenz: \(2x^{3}\) ist \(2 \cdot (x^3)\), nicht \((2x)^3\). Bei \(x = 2\) also \(16\), nicht \(64\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 4, r'Welche Kurve gehört zu welcher Funktion? (1) \(f(x) = x^4\) (2) \(g(x) = -x^3\) (3) \(h(x) = 2x^2\) (4) \(k(x) = x^5\)',
     r'<p>(1) → B, (2) → C, (3) → A, (4) → D.</p><p class="komm">Zuerst die Symmetrie: A und B sind achsensymmetrisch, also gerade Exponenten; C und D punktsymmetrisch, also ungerade. Zwischen A und B entscheidet der Wert bei \(x = 1\) \((2\) bzw. \(1)\), zwischen C und D die Richtung — \(g\) fällt, \(k\) steigt.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-k="2,2" data-fenster="-2,2,-8,8" data-titel="A"></svg><svg class="mini" data-k="1,4" data-fenster="-2,2,-8,8" data-titel="B"></svg><svg class="mini" data-k="-1,3" data-fenster="-2,2,-8,8" data-titel="C"></svg><svg class="mini" data-k="1,5" data-fenster="-2,2,-8,8" data-titel="D"></svg></div>'),
    ('1b', 3, r'\(f(x) = -2x^{3}\): Berechne \(f(-2)\), \(f(0.5)\) und \(f(3)\).',
     r'<p>\(f(-2) = -2 \cdot (-8) = 16\) · \(f(0.5) = -2 \cdot 0.125 = -0.25\) · \(f(3) = -2 \cdot 27 = -54\).</p><p class="komm">Immer zuerst die Potenz, dann mal \(a\). Die Klammer um die negative Zahl nicht vergessen.</p>', ''),
    ('1c', 2, r'Welche Symmetrie haben die Graphen von \(g(x) = 3x^{6}\) und \(h(x) = -x^{7}\)? Weise sie mit \(f(-x)\) nach.',
     r'<p>\(g(-x) = 3(-x)^6 = 3x^6 = g(x)\): gerade Funktion, Graph achsensymmetrisch zur \(y\)-Achse.</p><p>\(h(-x) = -(-x)^7 = x^7 = -h(x)\): ungerade Funktion, Graph punktsymmetrisch zum Ursprung.</p>', ''),
    ('1d', 2, r'Durch welche Punkte gehen <em>alle</em> Graphen von \(y = x^{n}\) mit \(n \in \mathbb{N}\setminus\{0\}\)? Und was geschieht bei \(x = -1\)?',
     r'<p>Durch \((0 \mid 0)\) und \((1 \mid 1)\): \(0^n = 0\) und \(1^n = 1\) für jedes \(n\).</p><p>Bei \(x = -1\) trennen sie sich: gerades \(n\) gibt \((-1 \mid 1)\), ungerades \(n\) gibt \((-1 \mid -1)\).</p>', ''),
    ('1e', 2, r'Skizziere \(y = x^{2}\) und \(y = x^{4}\) in <em>ein</em> Koordinatensystem für \(-1.5 \leq x \leq 1.5\). Wo liegt \(x^{4}\) unter \(x^{2}\), wo darüber?',
     r'<p>Beide gehen durch \((0 \mid 0)\), \((1 \mid 1)\) und \((-1 \mid 1)\).</p><p>Für \(0 \lt |x| \lt 1\) liegt \(x^4\) <em>unter</em> \(x^2\) (bei \(0.5\): \(0.0625 \lt 0.25\)), für \(|x| \gt 1\) <em>darüber</em> (bei \(1.5\): \(5.0625 \gt 2.25\)).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="1,2;1,4" data-fenster="-1.5,1.5,-0.5,2.5" data-punkte="1,1;-1,1"></svg></div>'),
], zwei=False)
k1 = kapitel(1, 'der-exponent', 'Der Exponent formt den Graphen', 'Potenzfunktionen', 40,
             r'Du erkennst an \(n\) die Form und an seiner Parität die Symmetrie, berechnest Funktionswerte von \(a \cdot x^{n}\) und liest umgekehrt die Gleichung aus einer Kurve.',
             ('s3-2-lp-exponent', 'Der Exponent formt den Graphen', '1:30'),
             sim1, ('s3-2-lp-kontrolle-exponent', 'Kontrollfragen zum Exponenten', '0:56'),
             fest1, [uebung('potenz-wert', 'Funktionswert berechnen'), uebung('symmetrie', 'Symmetrie erkennen'),
                     uebung('graf-potenz', 'Kurve → Gleichung', True)],
             auf1, f'<a href="{TA}#definition">Themenseite 3.2a, Potenzfunktionen</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Hyperbel y = a mal x hoch n mit negativem n, mit den Achsen als Asymptoten"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Asymptoten (die beiden Achsen)</label>
        <div class="sl-row">
          {regler('s2', 'a', 'a', -3, 3, 0.5, 1, 'blau')}
          {regler('s2', 'n', 'n', -4, -1, 1, -1, 'orange')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Negative Exponenten: Hyperbeln</div>
          <p>\[ f(x) = a \cdot x^{-n} = \frac{a}{x^{n}}, \qquad n \in \mathbb{N}\setminus\{0\} \]</p>
          <p>Der Graph heisst <b>Hyperbel \(n\)-ter Ordnung</b>. An der Stelle \(0\) müsste man durch null teilen — sie fehlt:</p>
          <p>\[ D = \mathbb{R}\setminus\{0\} \]</p>
          <p>Die Kurve zerfällt dort in zwei <b>Äste</b>. Die Stelle \(x = 0\) heisst <b>Polstelle</b>, die \(y\)-Achse <b>Polgerade</b>.</p>
          <p><b>Asymptoten:</b> Beide Achsen. Die Äste kommen ihnen beliebig nahe, erreichen sie aber nie.</p>
          <p><b>Wieder entscheidet die Parität von \(n\):</b></p>
          <ul>
            <li>\(n\) gerade (also \(y = \frac{a}{x^{2}}\), \(\frac{a}{x^{4}}\), …): gerade Funktion, beide Äste auf <em>derselben</em> Seite — bei \(a \gt 0\) oben, bei \(a \lt 0\) unten.</li>
            <li>\(n\) ungerade: ungerade Funktion, die Äste liegen <b>diagonal</b> in gegenüberliegenden Quadranten.</li>
          </ul>
          <p><b>Keine Nullstelle:</b> Ein Bruch ist nur null, wenn sein Zähler null ist — und \(a \neq 0\). Durch \((1 \mid a)\) gehen aber alle.</p>
          <p><b>Wertemenge \(W\)</b> — die Menge aller Werte, die \(f\) überhaupt annimmt: Bei <em>ungeradem</em> \(n\) ist \(W = \mathbb{R}\setminus\{0\}\) (jeder Wert ausser null kommt vor), bei <em>geradem</em> \(n\) nur die eine Hälfte — \(W = \mathbb{R}^{+}\) für \(a \gt 0\), \(W = \mathbb{R}^{-}\) für \(a \lt 0\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(x^{-2}\) ist nicht \(-x^{2}\). Das Minus im Exponenten heisst <em>Kehrwert</em>, nicht Vorzeichenwechsel: \(2^{-2} = \frac{1}{4}\), nicht \(-4\).</p>
          <p>Und \(x = 0\) gehört nicht zur Definitionsmenge — in jeder Antwort mit angeben.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'\(f(x) = \dfrac{4}{x}\): Berechne \(f(2)\), \(f(-0.5)\) und \(f(8)\).',
     r'<p>\(f(2) = 2\) · \(f(-0.5) = -8\) · \(f(8) = 0.5\).</p><p class="komm">Je grösser \(|x|\), desto näher liegt der Wert bei null — die \(x\)-Achse ist Asymptote.</p>', ''),
    ('2b', 3, r'Gegeben ist \(g(x) = \dfrac{3}{x^{2}}\). Gib Definitionsmenge, Wertemenge und die beiden Asymptoten an, und sag, wo die Äste liegen.',
     r'<p>\(D = \mathbb{R}\setminus\{0\}\), \(W = \mathbb{R}^{+}\) (nur positive Werte, denn \(x^2 \gt 0\) und \(3 \gt 0\)).</p><p>Asymptoten: \(x = 0\) und \(y = 0\). Der Exponent \(2\) ist gerade und \(a = 3 \gt 0\): <b>beide Äste oben</b>.</p>', ''),
    ('2c', 2, r'Begründe: Keine Funktion \(f(x) = \dfrac{a}{x^{n}}\) mit \(a \neq 0\) hat eine Nullstelle.',
     r'<p>Ein Bruch ist genau dann null, wenn sein <em>Zähler</em> null ist. Hier ist der Zähler die feste Zahl \(a \neq 0\), also wird \(f(x)\) nie null.</p><p class="komm">Grafisch: Die \(x\)-Achse ist Asymptote — die Kurve nähert sich ihr beliebig, trifft sie aber nie.</p>', ''),
    ('2d', 2, r'Ordne zu: (1) \(y = \dfrac{1}{x}\) (2) \(y = \dfrac{1}{x^{2}}\) (3) \(y = -\dfrac{1}{x}\) (4) \(y = -\dfrac{1}{x^{2}}\)',
     r'<p>(1) → B, (2) → A, (3) → D, (4) → C.</p><p class="komm">Erst die Parität: A und C haben beide Äste auf derselben Seite, also gerade Ordnung. Dann das Vorzeichen von \(a\): bei \(a \gt 0\) liegen sie oben.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-k="1,-2" data-fenster="-3,3,-3,3" data-titel="A"></svg><svg class="mini" data-k="1,-1" data-fenster="-3,3,-3,3" data-titel="B"></svg><svg class="mini" data-k="-1,-2" data-fenster="-3,3,-3,3" data-titel="C"></svg><svg class="mini" data-k="-1,-1" data-fenster="-3,3,-3,3" data-titel="D"></svg></div>'),
    ('2e', 2, r'Warum ist die Wertemenge von \(y = \dfrac{1}{x^{2}}\) nur \(\mathbb{R}^{+}\), die von \(y = \dfrac{1}{x}\) aber \(\mathbb{R}\setminus\{0\}\)?',
     r'<p>\(x^{2}\) ist für jedes \(x \neq 0\) positiv, also ist auch \(\frac{1}{x^{2}}\) immer positiv — negative Werte kommen nicht vor.</p><p>Bei \(\frac{1}{x}\) hat der Wert dasselbe Vorzeichen wie \(x\): jeder Wert ausser null wird erreicht.</p>', ''),
], zwei=False)
k2 = kapitel(2, 'negative-exponenten', 'Negative Exponenten: Hyperbeln', 'Potenzfunktionen', 40,
             r'Du deutest \(x^{-n}\) als Kehrwert, gibst Definitionsmenge und Asymptoten an und sagst an der Parität von \(n\), wo die beiden Äste liegen.',
             ('s3-2-lp-hyperbel', 'Negative Exponenten geben Hyperbeln', '1:24'),
             sim2, ('s3-2-lp-kontrolle-hyperbel', 'Kontrollfragen zu den Hyperbeln', '0:55'),
             fest2, [uebung('hyperbel-wert', 'Funktionswert berechnen'), uebung('aeste', 'Wo liegen die Äste?'),
                     uebung('def-hyperbel', 'Definitionslücke finden')],
             auf2, f'<a href="{TA}#typen">Themenseite 3.2a, Hyperbeln</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Verschobene Potenzkurve a mal Klammer x minus u hoch n plus v, mit mitwandernden Asymptoten"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Grundkurve \\(a \\cdot x^{{n}}\\) (gestrichelt)</label>
        <div class="sl-row">
          {regler('s3', 'a', 'a', -2, 2, 0.5, 1, 'blau')}
          {regler('s3', 'n', 'n', -3, 4, 1, 3, 'orange')}
          {regler('s3', 'u', 'u', -3, 3, 1, 0, 'gruen')}
          {regler('s3', 'v', 'v', -3, 3, 1, 0, 'gruen')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ein Schema für alle</div>
          <p>\[ f(x) = a \cdot (x - u)^{n} + v \]</p>
          <p>Dasselbe Schema wie bei jeder Grundfunktion (<a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1</a>):</p>
          <ul>
            <li>\(u\) verschiebt <b>waagrecht</b> und steht <em>in der Klammer</em> mit <b>umgekehrtem</b> Vorzeichen: \((x - 2)^3\) ist \(2\) nach rechts.</li>
            <li>\(v\) verschiebt <b>senkrecht</b> und steht <em>hinter</em> der Potenz mit seinem <b>eigenen</b> Vorzeichen.</li>
            <li>\(a\) streckt in \(y\)-Richtung; \(a \lt 0\) spiegelt an der Waagrechten \(y = v\).</li>
          </ul>
          <p><b>Bei \(n \geq 2\)</b> wandert der ausgezeichnete Punkt des Graphen nach \((u \mid v)\). Er heisst bei \(n = 2\) <b>Scheitel</b>, bei grösserem geradem \(n\) <b>Flachpunkt</b> und bei ungeradem \(n\) <b>Terrassenpunkt</b> (so auch auf <a href="../schwerpunkt/s3-2a-potenzfunktionen.html#paritaet">Themenseite 3.2a</a>).</p>
          <p><b>Bei \(n \lt 0\)</b> wandern die <b>Asymptoten mit</b>:</p>
          <p>\[ x = u \qquad \text{und} \qquad y = v, \qquad D = \mathbb{R}\setminus\{u\} \]</p>
          <p><b>Nullstellen</b> berechnet man mit \(f(x) = 0\):</p>
          <p>\[ a\,(x-u)^{n} = -v \;\Longrightarrow\; (x-u)^{n} = -\tfrac{v}{a} \]</p>
          <p>Bei <b>geradem</b> \(n\) hängt es an der rechten Seite: ist sie positiv, gibt das Wurzelziehen <b>zwei</b> Lösungen \((\pm)\); ist sie null, genau eine; ist sie negativ, keine — dann ist \(\mathbb{L} = \{\,\}\). Bei <b>ungeradem</b> \(n\) gibt es immer genau eine.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Das \(\pm\) beim geraden Exponenten vergessen. Aus \((x-3)^4 = 16\) folgt \(x - 3 = \pm 2\), also \(x_1 = 1\) <em>und</em> \(x_2 = 5\) — nicht nur \(5\).</p>
          <p>Und das Vorzeichen von \(u\): \((x + 1)^3\) ist \(1\) nach <em>links</em>, denn die Klammer wird bei \(x = -1\) null.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 13, [
    ('3a', 3, r'\(f(x) = (x+1)^{3} - 2\): Wie ist der Graph gegenüber \(y = x^{3}\) verschoben, wo liegt der Terrassenpunkt, und wie gross sind \(f(0)\) und \(f(1)\)?',
     r'<p>\(1\) nach links und \(2\) nach unten; Terrassenpunkt \((-1 \mid -2)\).</p><p>\(f(0) = 1^3 - 2 = -1\) · \(f(1) = 2^3 - 2 = 6\).</p>', ''),
    ('3b', 3, r'\(g(x) = \dfrac{2}{x-3} + 1\): Gib Definitionsmenge und beide Asymptoten an und berechne \(g(5)\).',
     r'<p>\(D = \mathbb{R}\setminus\{3\}\); Asymptoten \(x = 3\) und \(y = 1\).</p><p>\(g(5) = \dfrac{2}{2} + 1 = 2\).</p>', ''),
    ('3c', 3, r'Berechne die Nullstellen von \(h(x) = (x+2)^{4} - 81\).',
     r'<p>\((x+2)^4 = 81 \Rightarrow x + 2 = \pm 3 \Rightarrow x_1 = -5,\ x_2 = 1\).</p><p class="komm">Probe: \((-5+2)^4 = (-3)^4 = 81\) ✓ und \((1+2)^4 = 3^4 = 81\) ✓. Der Exponent ist gerade — darum zwei Lösungen.</p>', ''),
    ('3d', 2, r'Berechne die Nullstellen von \(k(x) = (x-1)^{3} + 8\). Wie viele sind es, und warum?',
     r'<p>\((x-1)^3 = -8 \Rightarrow x - 1 = -2 \Rightarrow x = -1\). Nur <b>eine</b>.</p><p class="komm">Der Exponent \(3\) ist ungerade: Die dritte Wurzel aus einer Zahl ist eindeutig, es gibt kein \(\pm\).</p>', ''),
    ('3e', 2, r'Welche Gleichung gehört zur abgebildeten Hyperbel? Lies die beiden Asymptoten ab.',
     r'<p>Asymptoten \(x = -2\) und \(y = 3\), also \(y = \dfrac{1}{x+2} + 3\).</p><p class="komm">Die Polgerade liegt links vom Ursprung, also ist \(u = -2\) und in der Klammer steht \(x + 2\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="1,-1,-2,3" data-fenster="-6,2,-1,7"></svg></div>'),
], zwei=False)
k3 = kapitel(3, 'verschieben', 'Verschieben und strecken', 'Transformationen (SP 3.1)', 40,
             r'Du liest aus \(a \cdot (x-u)^{n} + v\) ab, wohin die Kurve wandert, gibst die mitgewanderten Asymptoten an und berechnest Nullstellen — mit dem \(\pm\), wo es hingehört.',
             ('s3-2-lp-verschieben', 'Verschieben — und was die Asymptoten tun', '1:18'),
             sim3, ('s3-2-lp-kontrolle-verschieben', 'Kontrollfragen zum Verschieben', '0:52'),
             fest3, [uebung('transformation-lesen', 'Verschiebung ablesen'), uebung('asymptoten', 'Asymptoten angeben'),
                     uebung('nullstelle-potenz', 'Nullstellen berechnen')],
             auf3, f'<a href="{TA}#theorie">Themenseite 3.2a, Transformationen</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Potenzkurve und ihr Spiegelbild an der Winkelhalbierenden y gleich x"></svg>
        <label class="sim-schalter"><input type="checkbox"> nur \\(x \\geq 0\\) (einschränken)</label>
        <div class="sl-row">
          {regler('s4', 'n', 'n', 2, 6, 1, 2, 'orange')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Umkehren heisst spiegeln</div>
          <p>Die <b>Umkehrfunktion</b> \(f^{-1}\) macht rückgängig, was \(f\) tut: Aus dem bekannten \(y\) wird das gesuchte \(x\).</p>
          <p>Im Bild ist das eine <b>Spiegelung an der Winkelhalbierenden \(y = x\)</b>:</p>
          <p>\[ (x \mid y) \;\longmapsto\; (y \mid x) \]</p>
          <p>Punkte auf \(y = x\) bleiben liegen, etwa \((1 \mid 1)\). Definitions- und Wertemenge tauschen die Rollen.</p>
          <p><b>Das Rezept</b> — drei Schritte:</p>
          <ol>
            <li>Nach \(x\) auflösen.</li>
            <li>\(x\) und \(y\) vertauschen.</li>
            <li>Definitionsmenge prüfen.</li>
          </ol>
          <p>Beispiel: \(y = x^{3} + 1 \Rightarrow x^{3} = y - 1 \Rightarrow x = \sqrt[3]{y-1}\), vertauscht: \(f^{-1}(x) = \sqrt[3]{x-1}\).</p>
          <p><b>Die Parität entscheidet wieder:</b></p>
          <ul>
            <li>\(n\) <b>ungerade</b>: \(f\) steigt überall, jedem \(y\) gehört genau ein \(x\) — direkt umkehrbar, \(f^{-1}(x) = \sqrt[n]{x}\) mit \(D = \mathbb{R}\).</li>
            <li>\(n\) <b>gerade</b>: \(f(-x) = f(x)\), zu einem \(y\) gäbe es zwei \(x\). Erst auf \(x \geq 0\) <b>einschränken</b>, dann ist \(f^{-1}(x) = \sqrt[n]{x}\) mit \(D = \mathbb{R}_0^{+}\).</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(f^{-1}\) ist <em>nicht</em> der Kehrwert \(\dfrac{1}{f}\). Die Umkehrfunktion von \(x^{5}\) ist \(\sqrt[5]{x}\), nicht \(x^{-5}\).</p>
          <p>Und gespiegelt wird an \(y = x\), nicht an einer Achse — dabei <em>tauschen</em> die Koordinaten, sie wechseln nicht das Vorzeichen.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Bestimme die Umkehrfunktion von \(f(x) = x^{5} - 3\). Schreib den Rechenweg auf und mach die Probe mit \(x = 2\).',
     r'<p>\(y = x^5 - 3 \Rightarrow x^5 = y + 3 \Rightarrow x = \sqrt[5]{y+3}\), vertauscht: \(f^{-1}(x) = \sqrt[5]{x+3}\).</p><p>Probe: \(f(2) = 32 - 3 = 29\) und \(f^{-1}(29) = \sqrt[5]{32} = 2\) ✓</p>', ''),
    ('4b', 2, r'Warum muss man \(y = x^{6}\) vor dem Umkehren einschränken, \(y = x^{7}\) aber nicht?',
     r'<p>\(6\) ist gerade: \(f(-x) = f(x)\), also haben \(-2\) und \(2\) denselben Funktionswert \(64\). Beim Spiegeln lägen über \(x = 64\) zwei Punkte — kein Funktionsgraph. Erst \(x \geq 0\) macht die Zuordnung eindeutig.</p><p>\(7\) ist ungerade: Die Kurve steigt überall, jeder Wert kommt genau einmal vor.</p>', ''),
    ('4c', 3, r'Auf dem Graphen von \(f(x) = x^{4}\) mit \(x \geq 0\) liegt \(P(3 \mid 81)\). Welcher Punkt liegt dann auf \(f^{-1}\), und wie lautet \(f^{-1}\)?',
     r'<p>\(3^4 = 81\) ✓. Beim Spiegeln tauschen die Koordinaten: \(P\,\'(81 \mid 3)\).</p><p>\(f^{-1}(x) = \sqrt[4]{x}\) mit \(D = \mathbb{R}_0^{+}\).</p>', ''),
    ('4d', 2, r'Zeichne \(y = x^{3}\), die Winkelhalbierende \(y = x\) und die Umkehrfunktion in <em>ein</em> Koordinatensystem \((-2\) bis \(2)\).',
     r'<p>Die Umkehrfunktion ist \(y = \sqrt[3]{x}\). Sie geht ebenfalls durch \((0 \mid 0)\), \((1 \mid 1)\) und \((-1 \mid -1)\) und ist das Spiegelbild von \(y = x^3\) an der gestrichelten Winkelhalbierenden.</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="1,3;1,0.3333333333333333" data-diagonale="1" data-fenster="-2,2,-2,2" data-punkte="1,1;-1,-1"></svg></div>'),
    ('4e', 2, r'Gegeben \(f(x) = x^{3} + 1\) und \(g(x) = \sqrt[3]{x-1}\). Zeige an der Stelle \(x = 9\), dass \(f(g(x)) = x\) gilt.',
     r'<p>\(g(9) = \sqrt[3]{8} = 2\), dann \(f(2) = 2^3 + 1 = 9\) ✓</p><p class="komm">Genau das heisst «Umkehrfunktion»: Erst \(g\), dann \(f\) — und man ist wieder am Anfang.</p>', ''),
], zwei=False)
k4 = kapitel(4, 'umkehren', 'Umkehren: spiegeln an \\(y = x\\)', 'Umkehrfunktion · RLP-Kern', 45,
             r'Du deutest die Umkehrfunktion als Spiegelung an \(y = x\), bestimmst sie rechnerisch in drei Schritten und begründest, wann eine Potenzfunktion vorher eingeschränkt werden muss.',
             ('s3-2-lp-umkehren', 'Umkehren heisst spiegeln', '1:28'),
             sim4, ('s3-2-lp-kontrolle-umkehren', 'Kontrollfragen zum Umkehren', '0:57'),
             fest4, [uebung('einschraenken', 'Einschränken nötig?'), uebung('spiegelpunkt', 'Punkt spiegeln'),
                     uebung('umkehrfunktion', 'Umkehrfunktion bestimmen')],
             auf4, f'<a href="{TB}#theorie">Themenseite 3.2b, Umkehrfunktion</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Wurzelfunktion a mal n-te Wurzel aus x minus u plus v, mit Startpunkt und Nullstelle"></svg>
        <div class="sl-row">
          {regler('s5', 'a', 'a', -2, 2, 0.5, 1, 'blau')}
          {regler('s5', 'n', 'n', 2, 5, 1, 2, 'orange')}
          {regler('s5', 'u', 'u', -4, 4, 1, 0, 'gruen')}
          {regler('s5', 'v', 'v', -4, 4, 1, 0, 'gruen')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wurzelfunktionen</div>
          <p>\[ \sqrt[n]{x} = x^{\frac{1}{n}} \]</p>
          <p>Eine Wurzel ist eine Potenz mit gebrochenem Exponenten — alle Potenzregeln gelten weiter.</p>
          <p><b>Definitionsmenge</b>, wieder nach der Parität:</p>
          <ul>
            <li>\(n\) <b>gerade</b>: Der Radikand muss \(\geq 0\) sein. \(D = \mathbb{R}_0^{+}\), bei \(\sqrt[n]{x-u}\) also \(D = [u;\infty[\).</li>
            <li>\(n\) <b>ungerade</b>: keine Schranke, \(D = \mathbb{R}\) — es ist \(\sqrt[3]{-8} = -2\).</li>
          </ul>
          <p><b>Verschoben</b> nach demselben Schema wie in Kapitel 3:</p>
          <p>\[ f(x) = a \cdot \sqrt[n]{x - u} + v \]</p>
          <p>Bei <b>geradem</b> \(n\) beginnt die Kurve im <b>Startpunkt \((u \mid v)\)</b>, und dort beginnt auch die Definitionsmenge. Bei ungeradem \(n\) gibt es keinen Startpunkt — die Kurve läuft nach links weiter.</p>
          <p class="komm"><b>Eine Abweichung, die du kennen musst:</b> <a href="../schwerpunkt/s3-2b-wurzelfunktionen.html">Themenseite 3.2b</a> beschränkt der Einheitlichkeit halber <em>alle</em> Wurzelfunktionen auf \(D = \mathbb{R}_0^+\), auch die dritte. Hier nutzen wir, dass ungerade Wurzeln auch negative Radikanden haben: \(\sqrt[3]{-8} = -2\). In einer Prüfung sagt die Aufgabe, welche Lesart gilt — im Zweifel die Definitionsmenge dazuschreiben.</p>
          <p><b>Ordinatenabschnitt</b> ist der \(y\)-Wert bei \(x = 0\), also \(f(0)\) — sofern \(0\) überhaupt in \(D\) liegt.</p>
          <p><b>Nullstelle:</b> \(f(x) = 0\) nach der Wurzel auflösen, dann beide Seiten hoch \(n\). Bei geradem \(n\) muss der freigestellte Wurzelwert \(\geq 0\) sein — sonst gibt es keine Nullstelle.</p>
          <p><b>Grössenvergleich</b> für \(x \gt 0\):</p>
          <p>\[ 0 \lt x \lt 1:\ \sqrt{x} \gt x \gt x^{2} \qquad x \gt 1:\ \sqrt{x} \lt x \lt x^{2} \]</p>
          <p>Bei \(x = 1\) schneiden sich alle drei.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Einen <b>Startpunkt</b> hat nur die Kurve mit <em>geradem</em> Wurzelexponenten. \(y = \sqrt[3]{x+1} - 4\) beginnt nirgends — sie läuft nach links weiter, \(D = \mathbb{R}\).</p>
          <p>Und beim Quadrieren einer Wurzelgleichung können <b>Scheinlösungen</b> entstehen: Die Probe gehört dazu.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 3, r'Gib die maximale Definitionsmenge an: \(\sqrt{x-5}\) · \(\sqrt[3]{x+1}\) · \(\sqrt[4]{x+2} - 1\).',
     r'<p>\([5;\infty[\) · \(\mathbb{R}\) · \([-2;\infty[\).</p><p class="komm">Nur der <em>Radikand</em> zählt. Die \(-1\) hinter der Wurzel ändert die Definitionsmenge nicht, und der ungerade Wurzelexponent \(3\) setzt gar keine Schranke.</p>', ''),
    ('5b', 3, r'\(f(x) = 3\sqrt{x+1} - 6\): Gib Definitionsmenge und Startpunkt an und berechne Ordinatenabschnitt und Nullstelle.',
     r'<p>\(D = [-1;\infty[\), Startpunkt \((-1 \mid -6)\).</p><p>Ordinatenabschnitt: \(f(0) = 3 \cdot 1 - 6 = -3\).</p><p>Nullstelle: \(3\sqrt{x+1} = 6 \Rightarrow \sqrt{x+1} = 2 \Rightarrow x + 1 = 4 \Rightarrow x_0 = 3\).</p>', ''),
    ('5c', 3, r'Löse \(\sqrt[3]{x-1} = 2\) rechnerisch und beschreib, wie man die Lösung am Graphen abliest.',
     r'<p>Beide Seiten hoch \(3\): \(x - 1 = 8 \Rightarrow x = 9\). Probe: \(\sqrt[3]{8} = 2\) ✓ · \(\mathbb{L} = \{9\}\).</p><p>Grafisch: Man zeichnet \(y = \sqrt[3]{x-1}\) und die waagrechte Gerade \(y = 2\) und liest die \(x\)-Koordinate des Schnittpunkts ab.</p>', ''),
    ('5d', 2, r'Ordne \(\sqrt{x}\), \(x\) und \(x^{2}\) der Grösse nach — einmal für \(x = 0.09\), einmal für \(x = 16\).',
     r'<p>\(x = 0.09\): \(\sqrt{0.09} = 0.3 \gt 0.09 \gt 0.0081\), also \(\sqrt{x} \gt x \gt x^2\).</p><p>\(x = 16\): \(4 \lt 16 \lt 256\), also \(\sqrt{x} \lt x \lt x^2\) — die Reihenfolge kippt bei \(x = 1\).</p>', ''),
    ('5e', 3, r'Die abgebildete Wurzelkurve hat den Startpunkt \((2 \mid -1)\) und geht durch \((6 \mid 1)\). Bestimme \(a\) in \(f(x) = a\sqrt{x-2} - 1\) und gib die Definitionsmenge an.',
     r'<p>Einsetzen von \((6 \mid 1)\): \(a\sqrt{4} - 1 = 1 \Rightarrow 2a = 2 \Rightarrow a = 1\).</p><p>Also \(f(x) = \sqrt{x-2} - 1\) mit \(D = [2;\infty[\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="1,2,2,-1" data-wurzel="1" data-fenster="-1,8,-2,3" data-punkte="2,-1;6,1"></svg></div>'),
], zwei=False)
k5 = kapitel(5, 'wurzelfunktionen', 'Wurzelfunktionen nutzen', 'Wurzelfunktionen · RLP-Kern', 45,
             r'Du bestimmst Definitionsmenge, Startpunkt und Nullstelle einer verschobenen Wurzelfunktion, vergleichst \(\sqrt{x}\), \(x\) und \(x^{2}\) und löst eine Wurzelgleichung grafisch wie rechnerisch.',
             ('s3-2-lp-wurzel', 'Wurzelfunktionen nutzen', '1:30'),
             sim5, ('s3-2-lp-kontrolle-wurzel', 'Kontrollfragen zu den Wurzelfunktionen', '1:02'),
             fest5, [uebung('wurzel-def', 'Definitionsmenge bestimmen'), uebung('wurzel-startpunkt', 'Startpunkt angeben'),
                     uebung('wurzel-nullstelle', 'Nullstelle berechnen'), uebung('wurzelgleichung', 'Wurzelgleichung lösen'),
                     uebung('vergleich', 'Der Grösse nach')],
             auf5, f'<a href="{TB}#definition">Themenseite 3.2b, Wurzelfunktionen</a>')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-sf">Vorwissen · SP 1.2 · 3.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Potenzregeln, Wurzeln als Potenzen, Transformationen einer Grundfunktion. Wenn das wackelt: <a href="../schwerpunkt/s1-2-potenzen.html">Teilgebiet 1.2</a> und <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1</a>.</p>
      ''' + clipkarte('s1-2-anim-exponenten-treppe', 'Exponenten-Treppe: Wurzeln sind die halben Schritte', '0:51') + '''
      ''' + clipkarte('s3-1-anim-transformationen', 'Transformationen: ein Schema für alle Grundfunktionen', '0:49') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Berechne ohne Rechner: \((-2)^{3}\) · \((-2)^{4}\) · \(2^{-3}\) · \(\left(\tfrac{1}{2}\right)^{-2}\).',
     r'<p>\(-8\) · \(16\) · \(\tfrac{1}{8} = 0.125\) · \(4\).</p><p class="komm">Falsch? Ein <em>gerader</em> Exponent macht jede Basis positiv, ein negativer Exponent bedeutet den Kehrwert. <a href="../schwerpunkt/s1-2-potenzen.html#definition">Teilgebiet 1.2, Potenzen</a></p>', ''),
    ('0b', 3, r'Vereinfache: \(x^{3} \cdot x^{5}\) · \(\left(x^{3}\right)^{4}\) · \(\dfrac{x^{7}}{x^{3}}\).',
     r'<p>\(x^{8}\) · \(x^{12}\) · \(x^{4}\).</p><p class="komm">Falsch? Beim Multiplizieren werden die Exponenten addiert, beim Potenzieren multipliziert, beim Dividieren subtrahiert. <a href="../schwerpunkt/s1-2-potenzen.html#potenzgesetze">Teilgebiet 1.2, Potenzgesetze</a></p>', ''),
    ('0c', 2, r'Berechne: \(\sqrt{49}\) · \(\sqrt[3]{27}\) · \(\sqrt[4]{16}\) · \(\sqrt[3]{-8}\).',
     r'<p>\(7\) · \(3\) · \(2\) · \(-2\).</p><p class="komm">Die dritte Wurzel aus einer negativen Zahl gibt es — die Quadratwurzel aus einer negativen nicht. Genau dieser Unterschied trägt Kapitel 4 und 5.</p>', ''),
    ('0d', 3, r'Der Graph von \(y = (x-2)^{2} + 1\) entsteht aus der Normalparabel \(y = x^{2}\). Wie ist er verschoben, und wo liegt sein Scheitel?',
     r'<p>\(2\) nach rechts und \(1\) nach oben; Scheitel \(S(2 \mid 1)\).</p><p class="komm">Falsch? Die Zahl <em>in der Klammer</em> schiebt waagrecht, mit umgekehrtem Vorzeichen; die Zahl dahinter senkrecht, mit eigenem. Genau dieses Schema gilt in Kapitel 3 für jeden Exponenten. <a href="../schwerpunkt/s3-1-grundlagen.html#theorie">Teilgebiet 3.1, Transformationen</a> und der Clip oben.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. Ist 0c falsch, zuerst die <a href="../schwerpunkt/s1-2-potenzen.html#rationale-exponenten">Wurzeln</a> — ohne sie gehen Kapitel 4 und 5 nicht.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/potenz-wurzelfunktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-sf">SP 3.2 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 26 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Ganz ohne Taschenrechner: Die Kompetenz des Teilgebiets trägt im Lehrplan den Vermerk «auch ohne Hilfsmittel» — und die Aufgaben aus Kapitel 3, das zu Teilgebiet 3.1 gehört, sind ebenfalls ohne Rechner lösbar.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>23 – 26 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>18 – 22 P</td><td>Den schwächsten Teil nochmals: Simulation und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>12 – 17 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 11 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G2 → 1 · G3 → 2 · G4 → 3 (Nullstellen und Asymptoten) · G5, G6 → 4 · G7 → 5 (beide Paritäten) · G8 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Potenz- und Wurzelfunktionen, Version 1.0 (03.10.2026). Gebaut aus
     scripts/lp/potenz-wurzelfunktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     RLP-BM 2030, Schwerpunktfach 3.2 «Potenz- und Wurzelfunktionen», die einzige
     Kompetenz des Teilgebiets wörtlich (Quelle ../Math-SP.pdf, Schwerpunktbereich,
     Lerngebiet 3 «Funktionen»):
       K1  die Wurzelfunktionen als Umkehrfunktion der Potenzfunktion mit ganzzahligen
           Exponenten berechnen, interpretieren und grafisch darstellen
           (auch ohne Hilfsmittel)
     Weil sie die Wurzelfunktion ausdrücklich «als Umkehrfunktion der Potenzfunktion»
     verlangt, deckt dieses Leitprogramm beide Themenseiten des Teilgebiets ab —
     s3-2a (Potenzfunktionen) und s3-2b (Wurzelfunktionen). Getrennt wäre der Kern
     der Kompetenz in keinem von beiden ganz enthalten.

     Kompetenz → Kapitel → Test: «berechnen» → 1, 2, 3, 5 → G1, G3, G4, G7 ·
     «interpretieren» → 1, 2, 4 → G2, G3, G6, G8 · «grafisch darstellen» → 1, 3, 4, 5
     → G1, G2, G5. Kein Kapitelziel ohne Kompetenz.

     Kapitel 3 (Verschieben und strecken) gehört dem Lehrplan nach zu SP 3.1
     («Funktionstransformationen … algebraisch und grafisch durchführen, Parameter
     interpretieren»); es steht hier, weil Kapitel 5 die verschobene Wurzelkurve braucht
     und das Schema für Potenz- und Wurzelkurven dasselbe ist. Der Kapitelkopf sagt das.

     Nicht in diesem Leitprogramm, weil in anderen Teilgebieten: das Rechnen mit Potenzen
     und Wurzeln selbst (SP 1.2 — steht im Vorwissen), das Lösen von Wurzelgleichungen
     mit quadratischer Folgegleichung samt Scheinlösungen (SP 2.2) und der Funktionsbegriff
     (SP 3.1).

     Muster je Kapitel: ① Einführungsclip (zeigt alles, Auftrag am Schluss) → ② Simulation
     mit Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit
     Rückmeldung → ⑤ Aufgaben mit Lösungen. Notation wie die Themenseiten 3.2a/3.2b.
     Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/potenz-wurzelfunktionen/*.tex). Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Potenz- und Wurzelfunktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel und Gesamttest, rund fünf Lektionen.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Schwerpunktfach 3.2</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Der Exponent</span></a></li>
    </ol>
    <p class="lekt">Lektion 2</p>
    <ol>
      <li><a href="#k2"><span class="nr">2</span><span>Hyperbeln</span></a></li>
    </ol>
    <p class="lekt">Lektion 3</p>
    <ol>
      <li><a href="#k3"><span class="nr">3</span><span>Verschieben</span></a></li>
    </ol>
    <p class="lekt">Lektion 4</p>
    <ol>
      <li><a href="#k4"><span class="nr">4</span><span>Umkehren</span></a></li>
    </ol>
    <p class="lekt">Lektion 5</p>
    <ol>
      <li><a href="#k5"><span class="nr">5</span><span>Wurzelfunktionen</span></a></li>
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
        <p class="rlp-quelle">RLP-BM 2030, Schwerpunktfach 3.2 — das Teilgebiet hat genau eine Kompetenz.</p>
        <ul>
          <li><b>K1</b> die Wurzelfunktionen als Umkehrfunktion der Potenzfunktion mit ganzzahligen Exponenten berechnen, interpretieren und grafisch darstellen <span class="ohm">auch ohne Hilfsmittel</span></li>
        </ul>
        <p class="rlp-quelle">Weil diese Kompetenz die Wurzelfunktion ausdrücklich <em>als Umkehrfunktion der Potenzfunktion</em> verlangt, deckt dieses Leitprogramm beide Themenseiten des Teilgebiets ab: <a href="../schwerpunkt/s3-2a-potenzfunktionen.html">3.2a</a> und <a href="../schwerpunkt/s3-2b-wurzelfunktionen.html">3.2b</a>.</p>
        <p class="rlp-quelle">Kapitel 3 (Verschieben und strecken) gehört zu <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1</a> und steht hier, weil Kapitel 5 die verschobene Wurzelkurve braucht.</p>
        <p class="rlp-quelle">Nicht hier, sondern in <a href="../schwerpunkt/s1-2-potenzen.html">1.2</a> bzw. <a href="../schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html">2.2</a>: das Rechnen mit Potenzen und Wurzeln und das Lösen von Wurzelgleichungen mit quadratischer Folgegleichung.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Potenz- und Wurzelfunktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (03.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 40 · K4 45 · K5 45 · Gesamttest 30 = 250 min
# Die fünf Kapitel sind die fünf Lektionen; Vorwissen und Gesamttest kommen davor und danach.
body = (oben + band('Vorab', 'Vorwissen') + k0 + band(1, 'Der Exponent formt') + k1
        + band(2, 'Negative Exponenten') + k2 + band(3, 'Verschieben und strecken') + k3
        + band(4, 'Umkehren') + k4 + band(5, 'Wurzelfunktionen nutzen') + k5
        + band('Abschluss', 'Gesamttest') + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
