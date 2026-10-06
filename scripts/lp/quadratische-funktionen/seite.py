"""Baut leitprogramme/quadratische-funktionen.html aus einer Kapitelbeschreibung (seit 02.10.2026).

  python3 scripts/lp/quadratische-funktionen/seite.py

Liest Kopf (inkl. <style>) und Grundskript (Thema, Clip-Karten, Tests, Fortschritt) aus der
bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und
python3 scripts/build-seo.py (der SEO-Kopf wird mit übernommen). Siehe README.md.
"""
import re
import os
SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'   # Repo-Wurzel
alt = open(R + 'leitprogramme/quadratische-funktionen.html').read()
kopf = alt[:alt.index('</style>')]
if '/* ════════ Fassung 3' in kopf:
    kopf = kopf[:kopf.index('\n/* ════════ Fassung 3')]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Quadratische Funktionen — Simulationen'), alt.find('<script>\n/* Simulationen und Minigrafen')) if k > 0)
basis = alt[i:j].replace("' Selbsttests erledigt'", "' Aufgabenblöcken bearbeitet'")
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0', fuss).replace('Quadratische Funktionen (Probe)', 'Quadratische Funktionen')
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 2. Oktober 2026', fuss)

CSS = '''
/* ════════ Fassung 3 (02.10.2026): Aufgaben in der Animation, wenig Text ════════ */
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
.hilfs-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
/* Farben im ganzen LP wie Kapitel 1: blau = a, orange = x_s, grün = y_s (Scheitel grün).
   c lila, Nullstellen und b neutral. */
.p-c{fill:var(--lila)} .p-null{fill:var(--tinte)}
.sl-grp.akz-lila{--akz:var(--lila)} .sl-grp.akz-grau{--akz:var(--tinte-2)}
.formen-live button[data-form="g"].aktiv{border-color:var(--lila-rand);background:var(--lila-hell)}
.formen-live button[data-form="p"].aktiv{border-color:var(--tinte-2);background:var(--papier-2)}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input:disabled{opacity:.35}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
'''

def clipkarte(datei, titel, art, zeit):
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
          {'<svg class="mini gross ue-bild" role="img" aria-label="Parabel zur Aufgabe"></svg>' if bild else ''}
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''

def regler(name, var, label, mn, mx, st, val, akz):
    return f'<div class="sl-grp akz-{akz}"><label for="{name}-{var}"><span class="var">{label}</span></label><input type="range" id="{name}-{var}" data-p="{var}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>'

def test(tid, titel, punkte, aufgaben, zwei=True):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte)
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''

FAHRPLAN = '<div class="fahrplan" aria-label="Ablauf"><span>① Clip</span><span>② Tüfteln</span><span>③ Kontrollfragen</span><span>④ Üben mit Rückmeldung</span><span>⑤ Aufgaben</span></div>'

def kapitel(n, kid, titel, komp, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 3.3 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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

TS = '../grundlagen/g3-3-quadratische-funktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Parabel in Scheitelform, Normalparabel gestrichelt"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien (Normalparabel)</label>
        <div class="sl-row">
          {regler('s1', 'a', 'a', -2, 2, 0.25, 1, 'blau')}
          {regler('s1', 'xs', 'x<sub>s</sub>', -5, 5, 0.5, 0, 'orange')}
          {regler('s1', 'ys', 'y<sub>s</sub>', -5, 5, 0.5, 0, 'gruen')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Scheitelform</div>
          <p>\[ f(x) = a\,(x - x_s)^2 + y_s \quad\Longrightarrow\quad S(x_s \mid y_s) \]</p>
          <p>\(x_s\) steht in der Klammer mit umgekehrtem Vorzeichen, \(y_s\) dahinter mit eigenem. \(a\) verschiebt nichts: \(a \gt 0\) nach oben geöffnet, \(a \lt 0\) nach unten geöffnet. Streckfaktor \(|a| \gt 1\): schmaler als die Normalparabel, \(|a| \lt 1\): breiter.</p>
          <p>Wertemenge: \(W = \left[y_s;\, +\infty\right[\) bei \(a \gt 0\), \(W = \left]-\infty;\, y_s\right]\) bei \(a \lt 0\). Beispiel: \((x + 4)^2 - 1\) hat \(W = \left[-1;\, +\infty\right[\).</p>
          <p class="komm">Auf der Themenseite heissen \(x_s\) und \(y_s\) auch \(u\) und \(v\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(f(x) = (x + 4)^2 - 1\) hat den Scheitel \(S(-4 \mid -1)\), nicht \(S(4 \mid -1)\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 4, r'Welcher Graph gehört zu welcher Gleichung? (1) \((x-1)^2 + 2\) (2) \(-(x+2)^2 + 1\) (3) \(2x^2 - 3\) (4) \(0.5(x-3)^2\)',
     r'<p>(1) → C, (2) → A, (3) → D, (4) → B.</p><p class="komm">Am schnellsten über den Scheitel; A ist die einzige nach unten geöffnete.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-f="-1,-2,1" data-titel="A"></svg><svg class="mini" data-f="0.5,3,0" data-titel="B"></svg><svg class="mini" data-f="1,1,2" data-titel="C"></svg><svg class="mini" data-f="2,0,-3" data-titel="D"></svg></div>'),
    ('1b', 3, 'Scheitelform der Parabel? (Punkte auf Gitterpunkten)',
     r'<p>\(S(-2 \mid -3)\); ein Schritt rechts geht es 2 hinauf, also \(a = 2\): \(f(x) = 2(x+2)^2 - 3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-f="2,-2,-3" data-fenster="-5,2,-4,4" data-punkte="-2,-3;-1,-1"></svg></div>'),
    ('1c', 2, r'Wertemenge von \(f(x) = -2(x-1)^2 + 6\)?',
     r'<p>Nach unten geöffnet, höchster Wert \(6\): \(W = \left]-\infty;\, 6\right]\).</p>', ''),
    ('1d', 2, r'Warum hat \(f(x) = (x-3)^2 - 2\) bei \(x = 1\) und bei \(x = 5\) denselben Wert?',
     r'<p>Beide liegen \(2\) neben \(x_s = 3\): \((1-3)^2 = (5-3)^2 = 4\), also \(f(1) = f(5) = 2\). Die Parabel ist symmetrisch zur Symmetrieachse \(x = 3\).</p>', ''),
], zwei=False)
k1 = kapitel(1, 'die-parabel-bewegen', 'Die Parabel bewegen', 'K2', 35,
    r'Du liest aus \(f(x) = a(x - x_s)^2 + y_s\) Scheitel, Öffnung und Streckung ab — und umgekehrt die Gleichung aus dem Graphen.',
    ('g3-3-lp-verschieben', 'Parabel sehen: von der Normalparabel zur Scheitelform', 'Einführung', '1:41'),
    sim1, ('g3-3-lp-kontrolle-scheitelform', 'Kontrollfragen zur Scheitelform', '', '0:50'),
    fest1, [uebung('scheitel-lesen', 'Scheitel ablesen'), uebung('beschreibung', 'Beschreibung → Gleichung'),
            uebung('graf-scheitelform', 'Graph → Gleichung', True)],
    auf1, f'<a href="{TS}#definition">Themenseite 3.3, Definition und Parameter</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="formen-live">
          <button type="button" data-form="g"><span class="fl-name">Grundform</span><span data-rolle="g"></span></button>
          <button type="button" data-form="s"><span class="fl-name">Scheitelform</span><span data-rolle="s"></span></button>
          <button type="button" data-form="p"><span class="fl-name">Produktform</span><span data-rolle="p"></span></button>
        </div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Parabel mit y-Achsenabschnitt, Scheitel und Nullstellen"></svg>
        <div class="sl-row">
          {regler('s2', 'a', 'a', -2, 2, 0.25, 1, 'blau')}
          {regler('s2', 'xs', 'x<sub>s</sub>', -5, 5, 0.5, 2, 'orange')}
          {regler('s2', 'ys', 'y<sub>s</sub>', -5, 5, 0.5, -1, 'gruen')}
        </div>
      </figure>'''
fest2 = r'''      <div class="merk"><div class="titel">Quadratische Funktion</div><p>\(f(x) = ax^2 + bx + c\) mit \(a \neq 0\). Ihr Graph ist eine Parabel.</p></div>
      <div class="tabhuelle">
        <table class="gesetze formen">
          <thead><tr><th>Form</th><th>Gleichung</th><th>Im Bild direkt</th></tr></thead>
          <tbody>
            <tr><td>Grundform <span class="komm">(allgemeine Form)</span></td><td>\(ax^2 + bx + c\)</td><td class="wort">\(y\)-Achsenabschnitt \((0 \mid c)\)</td></tr>
            <tr><td>Scheitelform</td><td>\(a(x - x_s)^2 + y_s\)</td><td class="wort">Scheitel \(S(x_s \mid y_s)\)</td></tr>
            <tr><td>Produktform <span class="komm">(reelle Linearfaktoren)</span></td><td>\(a(x - x_1)(x - x_2)\)</td><td class="wort">Nullstellen \(x_1,\ x_2\) — nur bei \(D \geq 0\); bei \(D = 0\): \(a(x - x_1)^2\)</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk"><div class="titel">Umformen</div><p>Zur Grundform: ausmultiplizieren. Zur Produktform: Nullstellen bestimmen (Kapitel 3). \(a\) bleibt überall gleich.</p>
          <p>Zur Scheitelform: quadratisch ergänzen — die halbe Zahl vor \(x\) quadrieren, dazuzählen und wieder abziehen:</p>
          <p>\[ \begin{aligned} x^2 - 8x + 10 &= x^2 - 8x + 16 - 16 + 10 \\ &= (x - 4)^2 - 6 \end{aligned} \]</p>
          <p>Bei \(a \neq 1\) zuerst \(a\) ausklammern:</p>
          <p>\[ \begin{aligned} 2x^2 + 8x + 3 &= 2(x^2 + 4x + 4 - 4) + 3 \\ &= 2(x + 2)^2 - 5 \end{aligned} \]</p></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>\((x - 3)^2 + 2\) ist nicht \(x^2 - 3x + 2\), sondern \(x^2 - 6x + 11\).</p></div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'In die Grundform: \(-(x+3)^2 + 4\) und \(2(x-1)(x+4)\).', r'<p>\(-x^2 - 6x - 5\) und \(2x^2 + 6x - 8\).</p>', ''),
    ('2b', 3, r'Scheitelform von \(x^2 + 6x + 5\)?', r'<p>\(x^2 + 6x + 9 - 9 + 5 = (x+3)^2 - 4\), \(S(-3 \mid -4)\).</p>', ''),
    ('2c', 2, r'Produktform von \(x^2 + x - 12\)?', r'<p>\((x+4)(x-3)\).</p>', ''),
    ('2d', 2, r'Warum hat \(x^2 + 2x + 5\) keine Produktform (mit reellen Linearfaktoren)?', r'<p>\((x+1)^2 + 4 \geq 4\): keine reellen Nullstellen, also keine Faktoren \((x - x_1)\).</p>', ''),
    ('2e', 3, r'Lies Scheitel, Nullstellen und \(y\)-Achsenabschnitt ab und gib alle drei Formen an. (Punkte auf Gitterpunkten)',
     r'<p>\(S(1 \mid -4)\), Nullstellen \(-1\) und \(3\), \(y\)-Achsenabschnitt \(-3\); ein Schritt neben dem Scheitel 1 hinauf: \(a = 1\).</p><p>\(f(x) = (x-1)^2 - 4\) \(= (x+1)(x-3)\) \(= x^2 - 2x - 3\)</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-f="1,1,-4" data-fenster="-3,5,-5,3" data-punkte="1,-4;-1,0;3,0;0,-3"></svg></div>'),
])
k2 = kapitel(2, 'drei-formen-eine-parabel', 'Drei Formen, eine Parabel', 'K1 · K2', 40,
    'Du erklärst, was Grund-, Scheitel- und Produktform im Bild zeigen, und formst ohne Rechner um.',
    ('g3-3-lp-drei-formen', 'Parabel sehen: drei Formen, drei Blicke', 'Einführung', '1:01'),
    sim2, ('g3-3-lp-kontrolle-formen', 'Kontrollfragen zu den drei Formen', '', '0:51'),
    fest2, [uebung('scheitel-grund', 'Scheitelform → Grundform'), uebung('produkt-grund', 'Produktform → Grundform'),
            uebung('grund-scheitelform', 'Grundform → Scheitelform')],
    auf2, f'<a href="{TS}#darstellungen">Themenseite 3.3, Die drei Darstellungen</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Parabel mit Symmetrieachse und Nullstellen"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien (Symmetrieachse)</label>
        <div class="sl-row">
          {regler('s3', 'b', 'b', -4, 4, 1, -4, 'grau')}
          {regler('s3', 'c', 'c', -3, 7, 0.5, 3, 'lila')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Scheitel und Nullstellen</div>
          <p>\[ x_s = -\frac{b}{2a}, \qquad y_s = f(x_s), \qquad D = b^2 - 4ac \]</p>
          <p>\[ x_{1,2} = \frac{-b \pm \sqrt{D}}{2a} \quad (D \geq 0) \]</p>
          <p>Die Diskriminante \(D\) zählt die Nullstellen: \(D \gt 0\): zwei; \(D = 0\): eine; \(D \lt 0\): keine. Die Nullstellen liegen spiegelbildlich zur Symmetrieachse \(x = x_s\).</p>
        </div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>Bei \(a = 1,\ b = -4\) ist \(x_s = -\frac{-4}{2 \cdot 1} = +2\). Das Minus vor dem Bruch nicht vergessen.</p></div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Achsenschnittpunkte und Scheitel von \(x^2 - 6x + 8\).', r'<p>\((2 \mid 0)\), \((4 \mid 0)\), \((0 \mid 8)\); \(S(3 \mid -1)\).</p>', ''),
    ('3b', 3, r'Scheitel und Nullstellen von \(-2x^2 + 8x - 6\).', r'<p>\(S(2 \mid 2)\), Maximum; \(-2(x-1)(x-3)\): Nullstellen \(1\) und \(3\).</p>', ''),
    ('3c', 2, r'Anzahl Nullstellen, ohne die Nullstellen zu berechnen: \(x^2 + 4x + 5\) und \(4x^2 - 4x + 1\).', r'<p>\(D = -4\): keine. \(D = 0\): eine, bei \(x = 0.5\).</p>', ''),
    ('3d', 2, r'Ist \(D\) positiv, null oder negativ?', r'<p>P: \(D \gt 0\). Q: \(D = 0\). R: \(D \lt 0\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-f="1,1,-4" data-titel="P"></svg><svg class="mini" data-f="1,1,0" data-titel="Q"></svg><svg class="mini" data-f="-1,1,-2" data-titel="R"></svg></div>'),
    ('3e', 2, r'Warum hat \(f(x) = x^2 + bx - 3\) für jedes \(b\) zwei Nullstellen?',
     r'<p>\(D = b^2 + 12 \gt 0\), weil \(b^2 \geq 0\).</p><p class="komm">Oder am Graphen: nach oben geöffnet und \(f(0) = -3 \lt 0\).</p>', ''),
])
k3 = kapitel(3, 'nullstellen-und-scheitel', 'Nullstellen und Scheitel berechnen', 'K1 · K2', 40,
    'Du bestimmst aus der Grundform Scheitel und Nullstellen und sagst mit der Diskriminante \\(D = b^2 - 4ac\\) voraus, wie viele es gibt.',
    ('g3-3-lp-achse-bleibt', 'Parabel sehen: c hebt, die Symmetrieachse bleibt', 'Einführung', '1:07'),
    sim3, ('g3-3-lp-kontrolle-nullstellen', 'Kontrollfragen zu Nullstellen und Scheitel', '', '0:52'),
    fest3, [uebung('grund-scheitel', 'Scheitel aus der Grundform'), uebung('nullstellen', 'Nullstellen bestimmen')],
    auf3, f'<a href="{TS}#diskriminante">Themenseite 3.3, Diskriminante</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Parabel durch festen Scheitel oder feste Nullstellen, Streckfaktor einstellbar"></svg>
        <div class="sl-row">
          {regler('s4', 'a', 'a', -1, -0.05, 0.05, -0.5, 'blau')}
        </div>
      </figure>'''
fest4 = r'''      <div class="tabhuelle">
        <table class="gesetze formen">
          <thead><tr><th>Gegeben</th><th>Ansatz</th><th>Dann</th></tr></thead>
          <tbody>
            <tr><td>Scheitel + Punkt <span class="komm">(\(x_P \neq x_s\))</span></td><td>\(a(x - x_s)^2 + y_s\)</td><td class="wort">Punkt einsetzen → \(a\)</td></tr>
            <tr><td>Nullstellen + Punkt <span class="komm">(Punkt keine Nullstelle)</span></td><td>\(a(x - x_1)(x - x_2)\)</td><td class="wort">Punkt einsetzen → \(a\)</td></tr>
            <tr><td>drei Punkte</td><td>\(ax^2 + bx + c\)</td><td class="wort">drei Gleichungen → \(a, b, c\)</td></tr>
          </tbody>
        </table>
      </div>
      <div class="warn"><div class="titel">Häufiger Fehler</div><p>Zu \(S(-1 \mid 4)\) gehört \(a(x+1)^2 + 4\), nicht \(a(x-1)^2 + 4\).</p></div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 3, r'Scheitel \(S(-2 \mid 3)\), Punkt \(P(0 \mid -5)\).', r'<p>\(-5 = 4a + 3\), \(a = -2\): \(f(x) = -2(x+2)^2 + 3\).</p>', ''),
    ('4b', 3, r'Nullstellen \(-3\) und \(1\), \(y\)-Achsenabschnitt \(6\).', r'<p>\(6 = a \cdot 3 \cdot (-1)\), \(a = -2\): \(f(x) = -2(x+3)(x-1)\).</p>', ''),
    ('4c', 3, 'Parabelförmiger Torbogen: unten 6 m breit, in der Mitte 4.5 m hoch. Ursprung in der Mitte am Boden. Gleichung und Höhe 2 m neben der Mitte?',
     r'<p>\(f(x) = -0.5x^2 + 4.5\) für \(-3 \leq x \leq 3\) (nur der Bogen), \(f(2) = 2.5\) m.</p>', ''),
    ('4d', 3, 'Gleichung der Parabel? (Punkte auf Gitterpunkten)', r'<p>\(S(1 \mid 4)\), mit \((3 \mid 0)\): \(a = -1\). \(f(x) = -(x-1)^2 + 4\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-f="-1,1,4" data-fenster="-3,5,-2,5" data-punkte="1,4;-1,0;3,0"></svg></div>'),
    ('4e', 4, r'Parabel durch \((0 \mid 4)\), \((1 \mid 3)\) und \((2 \mid -2)\): Gleichung? Warum braucht es hier drei Punkte, bei bekanntem Scheitel aber nur einen?',
     r'<p>\(c = 4\); \(a + b + 4 = 3\) und \(4a + 2b + 4 = -2\) ergeben \(a = -2\), \(b = 1\): \(f(x) = -2x^2 + x + 4\).</p><p>In der Grundform sind \(a\), \(b\), \(c\) unbekannt: drei Unbekannte brauchen drei Gleichungen. Der Scheitel liefert \(x_s\) und \(y_s\), offen bleibt nur \(a\).</p>', ''),
])
k4 = kapitel(4, 'die-gleichung-aufstellen', 'Die Funktionsgleichung aufstellen', 'K3', 40,
    'Du wählst den passenden Ansatz und bestimmst \\(a\\) mit einem Punkt.',
    ('g3-3-lp-a-finden', 'Parabel sehen: a finden', 'Einführung', '0:56'),
    sim4, ('g3-3-lp-kontrolle-aufstellen', 'Kontrollfragen zum Aufstellen', '', '0:49'),
    fest4, [uebung('aufstellen-scheitel', 'Scheitel + Punkt → a'), uebung('aufstellen-nullstellen', 'Nullstellen + Punkt → a')],
    auf4, f'<a href="{TS}#aufstellen">Themenseite 3.3, Funktionsgleichung aufstellen</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 230" role="img" aria-label="Rechteck mit 36 m Umfang und seine Fläche als Parabel"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien (Rahmen 18 m × 18 m)</label>
        <div class="sl-row">
          {regler('s5', 'x', 'x', 0.5, 17.5, 0.5, 4, 'orange')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk"><div class="titel">Extremwertaufgabe — Vorgehen</div>
          <ol>
            <li>Variable festlegen (was ist \(x\)?), Zielgrösse als Funktion aufstellen.</li>
            <li>Zulässigen Bereich angeben, z. B. \(0 \lt x \lt 30\).</li>
            <li>Scheitel bestimmen: \(x_s = -\frac{b}{2a}\) oder Scheitelform. Abkürzung, wenn die Nullstellen leicht ablesbar sind: \(x_s\) liegt in ihrer Mitte.</li>
            <li>Art aus dem Vorzeichen: \(a \lt 0\) Maximum, \(a \gt 0\) Minimum. Der Scheitel muss im zulässigen Bereich liegen — sonst liegt das Extremum am Rand.</li>
            <li>Antwort mit Stelle <em>und</em> Wert, mit Einheit.</li>
          </ol></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>\(x = 10\) ist nicht die grösste Fläche. Gefragt ist \(A(10) = 100\) m².</p></div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 20, [
    ('5a', 4, r'Beet an einer Mauer, 60 m Zaun für die drei anderen Seiten, \(x\) = Seite senkrecht zur Mauer. Grösste Fläche?', r'<p>\(A(x) = x(60 - 2x)\), zulässig \(0 \lt x \lt 30\). Mitte der Nullstellen \(x = 15\): 15 m × 30 m, 450 m².</p>', ''),
    ('5b', 4, '30 CHF Eintritt, 200 Besucher; jeder Franken mehr kostet 5 Besucher. Bester Preis, grösste Einnahme?', r'<p>\(x\) = Preiserhöhung in CHF, zulässig \(-30 \lt x \lt 40\) (Preis und Besucherzahl positiv). Einnahme \(E(x) = (30 + x)(200 - 5x)\) — nicht Gewinn, die Kosten sind unbekannt. Nullstellen \(-30\) und \(40\), Mitte \(5\): 35 CHF, 6125 CHF.</p>', ''),
    ('5c', 2, 'Zwei Zahlen mit Summe 14: Wann ist ihr Produkt am grössten?', r'<p>\(x(14 - x)\), \(x\) beliebig reell: beide 7, Produkt 49.</p>', ''),
    ('5d', 2, r'Der Graph zeigt die Fläche \(A\) eines Rechtecks mit der Seite \(x\). Bei welchem \(x\) ist sie am grössten, wie gross ist sie, und welchen Umfang hat das Rechteck? (Punkte auf Gitterpunkten)',
     r'<p>Nullstellen \(0\) und \(6\), zulässig \(0 \lt x \lt 6\). Mitte \(x = 3\) m, \(A = 9\) m². \(A(x) = x(6 - x)\): Die andere Seite ist \(6 - x\), der Umfang \(2 \cdot 6 = 12\) m.</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-f="-1,3,9" data-fenster="-1,7,-1,10" data-punkte="0,0;3,9;6,0" data-xname="x [m]" data-yname="A [m²]"></svg></div>'),
    ('5e', 2, r'Warum liegt das Maximum von \(A(x) = x(30 - x)\) genau in der Mitte der Nullstellen?',
     r'<p>Die Parabel ist symmetrisch zur Symmetrieachse durch den Scheitel. Die Nullstellen \(0\) und \(30\) liegen spiegelbildlich dazu, also liegt der Scheitel bei \(x = 15\).</p>', ''),
    ('5f', 3, r'Ein Ball fliegt nach \(h(t) = -5t^2 + 15t + 2\) (\(t\) in s, \(h\) in m). Wann ist er am höchsten, und wie hoch?',
     r'<p>Die Nullstellen sind nicht ablesbar, also \(t_s = -\dfrac{15}{2 \cdot (-5)} = 1.5\) s. \(a = -5 \lt 0\): Maximum, \(h(1.5) = 13.25\) m. Zulässig von \(t = 0\) bis zur Landung (\(t \approx 3.13\) s), \(1.5\) liegt darin.</p>', ''),
    ('5g', 3, r'Ein Seil hängt näherungsweise parabelförmig zwischen zwei Masten: \(h(x) = 0.02x^2 - 1.2x + 25\) für \(0 \leq x \leq 50\) (\(x\), \(h\) in m). Wo hängt es am tiefsten, wie hoch über Boden? Wo ist es am höchsten?',
     r'<p>\(a = 0.02 \gt 0\): Der Scheitel ist ein Minimum. \(x_s = -\dfrac{-1.2}{2 \cdot 0.02} = 30\) m, \(h(30) = 7\) m. (\(D = -0.56 \lt 0\): keine Nullstellen, die Mitte-Abkürzung geht nicht.)</p><p>Am höchsten am Rand: \(h(0) = 25\) m, \(h(50) = 15\) m — also beim linken Mast, 25 m.</p>', ''),
])
k5 = kapitel(5, 'extremwertaufgaben', 'Extremwertaufgaben', 'K4', 45,
    'Du findest Maximum oder Minimum einer Sachaufgabe ohne Rechner — und nennst Stelle, Wert und zulässigen Bereich.',
    ('g3-3-lp-mitte', 'Parabel sehen: die grösste Fläche liegt in der Mitte', 'Einführung', '1:00'),
    sim5, ('g3-3-lp-kontrolle-extremwert', 'Kontrollfragen zu Extremwerten', '', '0:59'),
    fest5, [uebung('zaun', 'Zaun: grösste Fläche'), uebung('mauer', 'Beet an der Mauer'), uebung('extremwert', 'Extremwert aus der Grundform')],
    auf5, f'<a href="{TS}#extremwert">Themenseite 3.3, Extremwertaufgabe</a>')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 1.3 · 2.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Einsetzen, Klammer quadrieren, quadratische Gleichung lösen. Wenn das wackelt: <a href="../grundlagen/g2-2b-quadratische-gleichungen.html">Themenseite 2.2b, Quadratische Gleichungen</a>.</p>
      ''' + clipkarte('g1-3-binome-erkennen', 'Binomische Formeln erkennen', 'Themenseite 1.3', '0:44') + r'''
      <p class="komm">Im Clip heissen die Binomglieder \(a\) und \(b\) — nicht zu verwechseln mit den Koeffizienten \(a\), \(b\) der Parabel.</p>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'\(f(x) = 2x^2 - 3x + 1\): \(f(-2)\) und \(f(0.5)\)?', r'<p>\(15\) und \(0\).</p><p class="komm">Falsch? Klammer um negative Zahlen: \(2 \cdot (-2)^2 = 8\). <a href="../grundlagen/g1-3-algebraische-terme.html#klammern">Themenseite 1.3, Klammern auflösen</a></p>', ''),
    ('0b', 3, r'Ausmultiplizieren: \((x-3)^2\), \(2(x+1)^2 - 5\), \((x+2)(x-5)\).', r'<p>\(x^2 - 6x + 9\), \(2x^2 + 4x - 3\), \(x^2 - 3x - 10\).</p><p class="komm">Falsch? <a href="../grundlagen/g1-3-algebraische-terme.html#binomi">Themenseite 1.3, Binomische Formeln</a> und der Clip oben.</p>', ''),
    ('0c', 3, r'Löse \(x^2 - 2x - 8 = 0\).', r'<p>\((x-4)(x+2) = 0\): \(\mathbb{L} = \{-2;\ 4\}\).</p><p class="komm">Falsch? <a href="../grundlagen/g2-2b-quadratische-gleichungen.html#faktorisieren">Themenseite 2.2b, Faktorisieren</a></p>', ''),
    ('0d', 2, r'Löse \(2x^2 + 3x - 2 = 0\).', r'<p>\(x_{1,2} = \dfrac{-3 \pm 5}{4}\): \(\mathbb{L} = \{-2;\ 0.5\}\).</p><p class="komm">Falsch? <a href="../grundlagen/g2-2b-quadratische-gleichungen.html#verfahren">Themenseite 2.2b, Lösungsverfahren (Mitternachtsformel)</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. 0c und 0d beide falsch: zuerst die <a href="../grundlagen/g2-2b-quadratische-gleichungen.html">Themenseite 2.2b, Quadratische Gleichungen</a>.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/quadratische-funktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 3.3 · K1–K4</span><span class="zeit">≈ 25 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Teile A und C ohne Taschenrechner.<br>
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
          <p>Aufgabe → Kapitel: G1 → 1 und 2; G2 → 2; G3 → 1; G4 → 3; G5, G6 → 4; G7, G8 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Quadratische Funktionen, Version 1.0 (02.10.2026). Muster je Kapitel: ① Einführungsclip
     (zeigt alles, Auftrag am Schluss) → ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Notation x_s, y_s (Entscheid
     Auftraggeber; Themenseite: u, v). Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/quadratische-funktionen/*.tex). Planung, RLP: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Quadratische Funktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 3.3</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Die Parabel bewegen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Drei Formen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Nullstellen und Scheitel</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Gleichung aufstellen</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Extremwerte</span></a></li>
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
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach 3.3</p>
        <ul>
          <li><b>K1</b> Darstellungsformen (Grund-, Scheitel-, Produktform) erläutern und ineinander überführen <span class="ohm">auch ohne Hilfsmittel</span></li>
          <li><b>K2</b> die Darstellungsformen geometrisch interpretieren (Öffnung, Nullstellen, Scheitelpunkt, Achsenabschnitte) <span class="ohm">auch ohne Hilfsmittel</span></li>
          <li><b>K3</b> die Funktionsgleichung aufstellen</li>
          <li><b>K4</b> Extremwertaufgaben lösen <span class="ohm">auch ohne Hilfsmittel</span></li>
        </ul>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Quadratische Funktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (03.10.2026): K0 10 · K1 35 · K2 40 · K3 40 · K4 40 · K5 45 · Gesamttest 25 = 235 min
# Kapitel = Lektion: keine Lektionsbänder mehr; Vorwissen und Gesamttest kommen davor und danach.
body = (oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(R + 'leitprogramme/quadratische-funktionen.html', 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
