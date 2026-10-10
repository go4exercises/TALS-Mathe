"""Baut leitprogramme/betragsfunktionen.html aus einer Kapitelbeschreibung (05.10.2026).

  python3 scripts/lp/betragsfunktionen/seite.py

Leitprogramm zum Teilgebiet SP 3.6 (Themenseite s3-6-betragsfunktionen.html) — eine Ergänzung des
TALS-Lehrmittels, kein RLP-Teilgebiet; die fünf Kompetenzen der Themenseite. Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden
Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf
kommt das Gerüst aus leitprogramme/trigonometrische-funktionen.html, mit eigenem Titel und eigenen
localStorage-Schlüsseln. Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach
Pre-Flight und python3 scripts/build-seo.py. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/betragsfunktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/trigonometrische-funktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Trigonometrische Funktionen</title>',
                      '<title>Leitprogramm Betragsfunktionen</title>')
    alt = alt.replace('lp-trigo-', 'lp-betrag-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Trigonometrische Funktionen', '\n/* ════════ Betragsfunktionen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Trigonometrische Funktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Betragsfunktionen — Simulationen')) if k > 0)
basis = alt[i:j]
# Footer erzeugt scripts/build-seo.py (seit 10.10.2026): hier nur leere FUSS-Marken; nach dem Bau
# `python3 scripts/build-seo.py` laufen lassen.
fuss = alt[alt.index('<!-- FUSS:ANFANG'):] if '<!-- FUSS:ANFANG' in alt else alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'<!-- FUSS:ANFANG.*?<!-- FUSS:ENDE -->|<footer class="site-footer">.*?</footer>',
              lambda _: '<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n<!-- FUSS:ENDE -->',
              fuss, count=1, flags=re.S)

CSS = '''
/* ════════ Betragsfunktionen (05.10.2026) — Kapitelmuster wie Trigonometrische Funktionen ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Eigen sind die
   Farben: Betragskurve blau, Waagrechte und Lösungen orange, Äste als Geraden grün. */
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
/* Farben im ganzen Leitprogramm: blau = Betragskurve, orange = Waagrechte y = c und Lösungen,
   grün = die Äste als Geraden (abschnittsweise Terme), rot = Gegenbeispiel, Tinte = f vor dem
   Betrag, Symmetrieachse. Dieselben Farben tragen die Clips (farbe 1 blau, 2 orange, 3 grün, 5 Tinte). */
.sim .normal{stroke-dasharray:5 4;stroke:var(--tinte-2);fill:none;stroke-width:1.4}
.sim .asym{stroke:var(--tinte-2);stroke-width:1.2;stroke-dasharray:4 3;fill:none}
.sim .ast{stroke:var(--gruen);stroke-width:1.6;stroke-dasharray:5 4;fill:none}
.sim .zielkurve{stroke:var(--tinte-2);stroke-width:5;opacity:.3;fill:none}
.sim .abstand{stroke:var(--blau);stroke-width:5;stroke-linecap:round;opacity:.6}
.sim .loesung{stroke:var(--orange);stroke-width:5;stroke-linecap:round;opacity:.75}
.sim .waagrechte,svg.mini .waagrechte{stroke:var(--orange);stroke-width:1.4;stroke-dasharray:6 4}
.p-pkt{fill:var(--tinte)} .p-lauf{fill:var(--blau)} .p-lauf.orange{fill:var(--orange)}
svg.mini .p-pkt{fill:var(--tinte)}
svg.mini .kurve.g2{stroke:var(--tinte-2);stroke-dasharray:4 3}
.mini-reihe svg.mini{background:var(--karte)}
.sim input[type=range]:disabled{opacity:.4}
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


def regler(name, var, label, mn, mx, st, val, akz, pi=0):
    """pi = Nenner: Der Regler läuft über ganze Zahlen k, der Wert ist k·π/pi (Winkel in Schritten von π/pi)."""
    zus = f' data-pi="{pi}"' if pi else ''
    return (f'<div class="sl-grp akz-{akz}"><label for="{name}-{var}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{name}-{var}" data-p="{var}"{zus} min="{mn}" max="{mx}" step="{st}" value="{val}">'
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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp='K1'):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-sf">SP 3.6 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TS = '../schwerpunkt/s3-6-betragsfunktionen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 260" role="img" aria-label="Betragskurve y gleich Betrag von x minus m mit einem Läufer und dem Abstand auf der x-Achse"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Äste als ganze Geraden (gestrichelt)</label>
        <div class="sl-row">
          {regler('s1', 'm', 'Bezugspunkt u', -3, 3, 1, 0, 'grau')}
          {regler('s1', 'x', 'Läufer x', -6, 6, 0.5, 2.5, 'blau')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Betragsfunktion</div>
          <p>Der <b>Betrag</b> \(|x|\) ist der Abstand von \(x\) zur Null. Er ist nie negativ: \(|3| = 3\), \(|-3| = 3\).</p>
          <p>\[ y = |x| = \begin{cases} x & \text{für } x \ge 0 \\ -x & \text{für } x \lt 0 \end{cases} \]</p>
          <ul>
            <li>\(D = \mathbb{R}\), \(W = \mathbb{R}_0^+\), Nullstelle \(x_0 = 0\).</li>
            <li>Der Graph ist ein <b>V</b> aus zwei Geraden: links \(y = -x\) (Steigung \(-1\)), rechts \(y = x\) (Steigung \(+1\)).</li>
            <li><b>Knickpunkt</b> \((0 \mid 0)\); achsensymmetrisch zur \(y\)-Achse, denn \(|-x| = |x|\).</li>
          </ul>
          <p>Allgemein ist \(|x - u|\) der Abstand von \(x\) zu \(u\): \(|x - u| = x - u\) für \(x \ge u\), \(-(x - u)\) für \(x \lt u\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«\(-x\) ist negativ»: Für \(x \lt 0\) ist \(-x\) positiv, zum Beispiel \(-(-4) = 4\). Darum ist \(|x| = -x\) dort richtig.</p>
          <p>Den Betrag vor dem Rechnen nehmen: \(|2 - 9| = |-7| = 7\), nicht \(2 + 9\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Berechne: \(|-8| + |3|\); \(|2 - 9|\); \(-|-4|\).',
     r'<p>\(8 + 3 = 11\); \(|-7| = 7\); \(-4\).</p><p class="komm">Das Minus vor dem Betrag steht ausserhalb: Erst \(|-4| = 4\), dann das Vorzeichen.</p>', ''),
    ('1b', 3, r'Schreib \(|x|\) für \(x = -2.5\) und für \(x = 4\) mit der Fallunterscheidung aus. Welcher Fall gilt bei \(x = 0\)?',
     r'<p>\(x = -2.5 \lt 0\): \(|x| = -x = -(-2.5) = 2.5\). \(x = 4 \ge 0\): \(|x| = x = 4\). Bei \(x = 0\) gilt der Fall \(x \ge 0\): \(|0| = 0\).</p>', ''),
    ('1c', 2, r'Für welche \(x\) gilt \(|x| = 6\)? \(|x| = 0\)? \(|x| = -1\)?',
     r'<p>\(x = 6\) oder \(x = -6\); nur \(x = 0\); für kein \(x\): \(L = \{\,\}\), denn ein Betrag ist nie negativ.</p>', ''),
    ('1d', 2, r'Warum gilt \(|-x| = |x|\)? Was bedeutet das für den Graphen von \(y = |x|\)?',
     r'<p>\(x\) und \(-x\) sind gleich weit von der Null entfernt. Im Graphen: Die Punkte bei \(x\) und \(-x\) liegen gleich hoch — das V ist achsensymmetrisch zur \(y\)-Achse.</p>', ''),
    ('1e', 2, r'Lies am Graphen von \(y = |x|\) ab: Für welche \(x\) liegt das V unter der Waagrechten \(y = 3\) oder auf ihr?',
     r'<p>Zwischen \(x = -3\) und \(x = 3\), die Ränder eingeschlossen: \(-3 \le x \le 3\). Genau dort ist der Abstand zur Null höchstens \(3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="v,1,0,0" data-fenster="-5,5,-1,6" data-waagrecht="3" data-ym="1,2,3,4,5" data-xm="-4,-3,-2,-1,1,2,3,4"></svg></div>'),
    ('1f', 2, r'Skizziere \(y = |x|\) für \(-4 \le x \le 4\) und zeichne die beiden Äste als ganze Geraden gestrichelt dazu. Wie heissen ihre Gleichungen?',
     r'<p>Rechter Ast: \(y = x\) (für \(x \ge 0\)), linker Ast: \(y = -x\) (für \(x \lt 0\)). Die gestrichelten Verlängerungen liegen unter der \(x\)-Achse — dort gehört nur das V nicht hin.</p>'
     '<div class="mini-reihe"><svg class="mini gross" data-k="v,1,0,0;g,1,0;g,-1,0" data-fenster="-4.5,4.5,-4.5,4.5" data-ym="-4,-2,2,4"></svg></div>', ''),
], zwei=False)
k1 = kapitel(1, 'betragsfunktion', 'Die Betragsfunktion', 35,
             r'Du deutest den Betrag als Abstand, schreibst \(|x|\) abschnittsweise, skizzierst das V und beschreibst es mit Knickpunkt, Ast-Steigungen und Symmetrie.',
             ('s3-6-lp-betragsfunktion', 'Die Betragsfunktion'),
             sim1, ('s3-6-lp-kontrolle-betragsfunktion', 'Kontrollfragen zur Betragsfunktion'),
             fest1, [uebung('betrag-wert', 'Betrag berechnen'), uebung('fall', 'Welcher Fall gilt?')],
             auf1, f'<a href="{TS}#definition">Themenseite 3.6, Definition</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="V-Kurve y gleich a mal Betrag von x minus u plus v, gestrichelt die Ausgangskurve Betrag von x"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Symmetrieachse \\(x = u\\) (gestrichelt)</label>
        <div class="sl-row">
          {regler('s2', 'a', 'Faktor a', -3, 3, 0.5, 1, 'blau')}
          {regler('s2', 'u', 'u', -4, 4, 0.5, 0, 'grau')}
          {regler('s2', 'v', 'v', -4, 4, 0.5, 0, 'grau')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Verschieben und Strecken</div>
          <p>\[ y = a \cdot |x - u| + v \qquad (a \neq 0) \]</p>
          <ul>
            <li><b>Knickpunkt</b> \((u \mid v)\), <b>Symmetrieachse</b> \(x = u\).</li>
            <li>Die Äste sind Geraden mit den Steigungen \(-a\) (links) und \(+a\) (rechts).</li>
            <li>\(a \gt 0\): ein V, der Knick ist der tiefste Punkt, \(W = [v;\, \infty[\). \(a \lt 0\): ein <b>Dach</b>, der Knick ist der höchste Punkt, \(W = \,]-\infty;\, v]\).</li>
          </ul>
          <p><b>Skizzieren ohne Wertetabelle:</b> Knick setzen, von dort eine Einheit nach rechts und \(a\) nach oben (bzw. unten), symmetrisch nach links.</p>
          <p>Steht \(|x + 3|\) da, ist \(u = -3\): \(|x + 3| = |x - (-3)|\).</p>
          <p><b>Nullstellen:</b> \(a\,|x - u| + v = 0 \Rightarrow |x - u| = -\tfrac{v}{a}\) — die beiden Stellen, die von \(u\) den Abstand \(-\tfrac{v}{a}\) haben (nur wenn \(-\tfrac{v}{a} \ge 0\)). Beispiel: \(-|x - 2| + 1 = 0 \Rightarrow |x - 2| = 1 \Rightarrow x = 1\) oder \(x = 3\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Das Vorzeichen von \(u\) direkt abschreiben: Der Knick von \(|x + 3|\) liegt bei \(x = -3\), wo das Argument null wird.</p>
          <p>Das Minus vor dem Betrag mit dem Summanden verwechseln: \(-|x| + 2\) ist ein Dach mit Spitze \((0 \mid 2)\), kein nach unten verschobenes V.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'Gib Knickpunkt, die Steigungen der Äste und die Öffnung an: (a) \(y = -3\,|x + 1| + 2\) (b) \(y = 0.5\,|x - 4|\).',
     r'<p>(a) \((-1 \mid 2)\), links \(+3\), rechts \(-3\), Dach. (b) \((4 \mid 0)\), links \(-0.5\), rechts \(+0.5\), V.</p>', ''),
    ('2b', 3, r'Skizziere \(y = 2\,|x + 1| - 4\) ohne Wertetabelle und berechne die Nullstellen.',
     r'<p>Knick \((-1 \mid -4)\), Äste mit Steigung \(\pm 2\). Nullstellen: \(2|x + 1| = 4 \Rightarrow |x + 1| = 2 \Rightarrow x = 1\) oder \(x = -3\).</p>'
     '<div class="mini-reihe"><svg class="mini gross" data-k="v,2,-1,-4" data-fenster="-5,4,-5,4" data-punkte="-1,-4;1,0;-3,0" data-xm="-3,-1,1,3" data-ym="-4,-2,2"></svg></div>', ''),
    ('2c', 3, r'Bestimme die Gleichung der abgebildeten Kurve in der Form \(y = a\,|x - u| + v\).',
     r'<p>Knick \((-1 \mid 3)\), also \(u = -1\), \(v = 3\). Nach unten geöffnet, eine Einheit nach rechts geht es \(0.5\) hinunter: \(a = -0.5\). Also \(y = -0.5\,|x + 1| + 3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="v,-0.5,-1,3" data-fenster="-5,5,-1,5" data-punkte="-1,3;1,2;3,1" data-xm="-4,-3,-2,-1,1,2,3,4" data-ym="1,2,3,4"></svg></div>'),
    ('2d', 2, r'Gib die Wertemenge an: \(y = 3\,|x - 2| - 1\); \(y = -|x| + 5\).',
     r'<p>\(W = [-1;\, \infty[\) (V, Knick unten bei \(-1\)); \(W = \,]-\infty;\, 5]\) (Dach, Spitze bei \(5\)).</p>', ''),
    ('2e', 2, r'Warum ist bei \(a \lt 0\) der Knickpunkt der höchste Punkt des Graphen?',
     r'<p>\(|x - u| \ge 0\), mal einer negativen Zahl \(a\) also \(\le 0\). Der Term \(a\,|x - u|\) ist darum höchstens \(0\), und das genau bei \(x = u\). Also ist \(y \le v\), mit \(y = v\) nur im Knick.</p>', ''),
], zwei=False)
k2 = kapitel(2, 'verschieben', 'Verschieben und Strecken', 45,
             r'Du skizzierst \(y = a\,|x - u| + v\) ohne Wertetabelle, liest Knickpunkt, Ast-Steigungen und Öffnung ab und bestimmst die Gleichung aus dem Graphen.',
             ('s3-6-lp-verschieben', 'Das V verschieben und strecken'),
             sim2, ('s3-6-lp-kontrolle-verschieben', 'Kontrollfragen zum Verschieben'),
             fest2, [uebung('knick-steigung', 'Knick und Steigung ablesen'), uebung('v-aus-graph', 'Gleichung aus dem Graphen', True)],
             auf2, f'<a href="{TS}#darstellungen">Themenseite 3.6, Transformationen</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Funktion f gestrichelt und ihr Betrag als Kurve, mit den Knicken an den Nullstellen"></svg>
        <label class="sim-schalter"><input type="checkbox"> Parabel \\(f(x) = x^2 + q\\) statt Gerade</label>
        <div class="sl-row">
          {regler('s3', 'm', 'Steigung m', -2, 2, 0.5, 1, 'grau')}
          {regler('s3', 'q', 'q', -4, 4, 0.5, 1, 'grau')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Das Umklapp-Prinzip</div>
          <p>Der Betrag wirkt auf die <b>Funktionswerte</b>: Wo \(f(x) \ge 0\), bleibt alles; wo \(f(x) \lt 0\), wird das Vorzeichen gedreht.</p>
          <ol>
            <li>Graph von \(f\) zeichnen.</li>
            <li>Alle Teile <b>unterhalb</b> der \(x\)-Achse an der \(x\)-Achse nach oben spiegeln.</li>
            <li>Teile oberhalb bleiben. Wo \(f\) die \(x\)-Achse <b>schneidet</b> (das Vorzeichen wechselt), entstehen Knicke. Berührt \(f\) die Achse nur, wie \(x^2\) bei \(0\), entsteht keiner.</li>
          </ol>
          <p>Beispiele: \(|x - 2|\) — ein Knick bei \(2\). \(|x^2 - 4|\) — Knicke bei \(\pm 2\), der Scheitel \((0 \mid -4)\) wird zum Buckel \((0 \mid 4)\), ein W. \(|x^2 + 1| = x^2 + 1\) — nichts zu tun.</p>
          <p><b>Parabel mit linearem Glied:</b> erst Nullstellen und Scheitel von \(f\). \(f(x) = x^2 - 2x - 8 = (x + 2)(x - 4)\): Nullstellen \(-2\) und \(4\), Scheitel in der Mitte bei \(x = 1\), \(f(1) = -9\). Bei \(|f|\): Knicke \((-2 \mid 0)\), \((4 \mid 0)\), Buckel \((1 \mid 9)\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die ganze Kurve spiegeln: \(|f(x)| \neq -f(x)\). Nur was unten liegt, klappt hoch. Kontrolle: \(|f|\) verläuft nie unter der \(x\)-Achse.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Skizziere \(f(x) = 2x - 6\) und \(y = |f(x)|\) in ein Koordinatensystem. Wo liegt der Knick, und welchen Wert hat \(|f|\) bei \(x = 0\)?',
     r'<p>Knick an der Nullstelle von \(f\): \((3 \mid 0)\). \(|f(0)| = |-6| = 6\). Links von \(3\) liegt \(f\) unten und klappt hoch: Dort ist \(|f(x)| = -2x + 6\).</p>'
     '<div class="mini-reihe"><svg class="mini gross" data-k="g,2,-6;G,2,-6" data-fenster="-2,6,-6,8" data-punkte="3,0;0,6" data-xm="-1,1,3,5" data-ym="-4,2,6"></svg></div>', ''),
    ('3b', 3, r'Wo liegen die Knicke, und wohin kommt der Scheitel? (a) \(y = |x^2 - 1|\) (b) \(y = |x^2 + 1|\) (c) \(y = |x^2 - 4x|\)',
     r'<p>(a) Knicke bei \(\pm 1\), Scheitel \((0 \mid -1) \to (0 \mid 1)\). (b) keine Knicke, \(x^2 + 1 \gt 0\): unverändert. (c) \(x^2 - 4x = x(x - 4)\): Knicke bei \(0\) und \(4\), Scheitel \((2 \mid -4) \to (2 \mid 4)\).</p>', ''),
    ('3c', 2, r'Abgebildet ist \(y = |f(x)|\) mit \(f(x) = x^2 + q\). Bestimme \(q\).',
     r'<p>Die Knicke liegen bei \(\pm 1.5\), der Buckel bei \((0 \mid 2.25)\): Der Scheitel von \(f\) war \((0 \mid -2.25)\). Also \(q = -2.25\) — Kontrolle: \(1.5^2 = 2.25\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="Q,1,0,-2.25" data-fenster="-3,3,-1,5" data-xm="-1.5,1.5" data-ym="2.25,4"></svg></div>'),
    ('3d', 2, r'Warum hat \(y = |x^2 + 1|\) keinen Knick, \(y = |x^2 - 1|\) aber zwei?',
     r'<p>Knicke entstehen, wo \(f\) das Vorzeichen wechselt — an den Schnittstellen mit der \(x\)-Achse. \(x^2 + 1 \ge 1\) hat keine, \(x^2 - 1\) schneidet die Achse zweimal (\(\pm 1\)).</p>', ''),
    ('3e', 2, r'Jemand zeichnet für \(y = |x - 2|\) überall die Gerade \(y = -x + 2\). Was ist falsch?',
     r'<p>\(-x + 2\) ist \(-f(x)\), die ganz gespiegelte Gerade. Für \(x \gt 2\) ist sie negativ — ein Betrag nie. Richtig: \(-x + 2\) nur für \(x \lt 2\), sonst \(x - 2\).</p>', ''),
], zwei=False)
k3 = kapitel(3, 'umklappen', 'Das Umklapp-Prinzip', 40,
             r'Du konstruierst den Graphen von \(y = |f(x)|\) aus dem Graphen einer linearen oder quadratischen Funktion \(f\) und gibst die Knicke an.',
             ('s3-6-lp-umklappen', 'Das Umklapp-Prinzip'),
             sim3, ('s3-6-lp-kontrolle-umklappen', 'Kontrollfragen zum Umklappen'),
             fest3, [uebung('umklapp-gerade', 'Betrag einer Geraden'), uebung('umklapp-parabel', 'Betrag einer Parabel')],
             auf3, f'<a href="{TS}#typen">Themenseite 3.6, Umklapp-Prinzip</a>', komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Wanne y gleich Betrag von x minus a plus Betrag von x minus b, gestrichelt die beiden einzelnen Beträge"></svg>
        <div class="sl-row">
          {regler('s4', 'a', 'Stelle a', -3, 3, 0.5, -2, 'grau')}
          {regler('s4', 'b', 'Stelle b', -3, 5, 0.5, 2, 'grau')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Abschnittsweise schreiben</div>
          <p>Jeden Betragsterm kann man ohne Betragsstriche schreiben — mit einer <b>Fallunterscheidung an der Nullstelle des Arguments</b>:</p>
          <p>\[ |2x - 6| = \begin{cases} 2x - 6 & \text{für } x \ge 3 \\ -2x + 6 & \text{für } x \lt 3 \end{cases} \]</p>
          <p>Wo das Argument negativ ist, wird das Vorzeichen des <em>ganzen</em> Terms gedreht — links oder rechts der Grenze, je nach Vorzeichen von \(x\) im Argument: \(|4 - 2x| = 4 - 2x\) für \(x \le 2\). Probe mit einer Stelle: \(x = 1\): \(|2 - 6| = 4\) und \(-2 + 6 = 4\).</p>
          <p><b>Die Wanne:</b> \(y = |x - a| + |x - b|\) (mit \(a \lt b\)) hat zwei Grenzen und drei Abschnitte. Zwischen \(a\) und \(b\) ist \(y = b - a\) konstant — ein flacher Boden; aussen haben die Äste die Steigungen \(-2\) (links) und \(+2\) (rechts).</p>
          <p>\[ |x + 1| + |x - 3| = \begin{cases} -2x + 2 & x \lt -1 \\ 4 & -1 \le x \le 3 \\ 2x - 2 & x \gt 3 \end{cases} \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Grenze falsch ablesen: \(|2x - 6|\) knickt bei \(x = 3\), nicht bei \(6\). Immer das Argument gleich null setzen.</p>
          <p>Nur eine Zahl umdrehen: Links der Grenze ist \(|2x - 6| = -(2x - 6) = -2x + 6\), nicht \(2x + 6\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Schreib abschnittsweise: \(|3x + 9|\); \(|4 - 2x|\).',
     r'<p>\(|3x + 9| = 3x + 9\) für \(x \ge -3\), \(-3x - 9\) für \(x \lt -3\).; \(|4 - 2x| = 4 - 2x\) für \(x \le 2\), \(2x - 4\) für \(x \gt 2\).</p>', ''),
    ('4b', 3, r'Schreib \(y = |x + 2| + |x - 2|\) abschnittsweise und gib den Wert bei \(x = 3\) an.',
     r'<p>\(y = -2x\) für \(x \lt -2\), \(y = 4\) für \(-2 \le x \le 2\), \(y = 2x\) für \(x \gt 2\). \(y(3) = 6\).</p>', ''),
    ('4c', 2, r'Abgebildet ist \(y = |x - a| + |x - b|\). Lies \(a\), \(b\) und die Höhe des Bodens ab.',
     r'<p>Der Boden reicht von \(-3\) bis \(1\): \(a = -3\), \(b = 1\) (oder umgekehrt), Höhe \(1 - (-3) = 4\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="w,-3,1" data-fenster="-5,3,-1,9" data-xm="-4,-3,-2,-1,1,2" data-ym="2,4,6,8"></svg></div>'),
    ('4d', 2, r'Schreib mit Betrag: \(f(x) = \begin{cases} x - 2 & x \ge 2 \\ 2 - x & x \lt 2 \end{cases}\).',
     r'<p>\(f(x) = |x - 2|\): rechts der Grenze \(2\) das Argument selbst, links sein Gegenteil.</p>', ''),
    ('4e', 2, r'Warum ist der Boden der Wanne \(y = |x - a| + |x - b|\) flach?',
     r'<p>Für \(a \le x \le b\) ist \(|x - a|\) der Abstand zu \(a\) und \(|x - b|\) der Abstand zu \(b\). Zusammen ist das immer die ganze Strecke von \(a\) bis \(b\), also \(b - a\) — egal, wo \(x\) dazwischen liegt.</p>', ''),
], zwei=False)
k4 = kapitel(4, 'abschnittsweise', 'Abschnittsweise schreiben', 40,
             r'Du schreibst Betragsterme ohne Betragsstriche, liest abschnittsweise definierte Funktionen und zerlegst die Wanne \(|x - a| + |x - b|\) in ihre drei Abschnitte.',
             ('s3-6-lp-abschnittsweise', 'Abschnittsweise schreiben'),
             sim4, ('s3-6-lp-kontrolle-abschnittsweise', 'Kontrollfragen zum abschnittsweisen Schreiben'),
             fest4, [uebung('abschnittsweise', 'Ohne Betragsstriche'), uebung('wanne', 'Die Wanne')],
             auf4, f'<a href="{TS}#theorie">Themenseite 3.6, Abschnittsweise schreiben</a>', komp='K4')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 260" role="img" aria-label="V-Kurve oder W-Kurve mit einer Waagrechten y gleich c und den Schnittstellen"></svg>
        <label class="sim-schalter"><input type="checkbox"> W: \\(y = |x^2 - 4|\\) statt V</label>
        <label class="sim-schalter"><input type="checkbox"> Ungleichung «≤» (nur beim V)</label>
        <div class="sl-row">
          {regler('s5', 'u', 'u (Knick des V)', -3, 3, 1, 0, 'grau')}
          {regler('s5', 'c', 'Waagrechte y = c', -1, 6, 0.5, 1.5, 'orange')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Betragsgleichungen und -ungleichungen</div>
          <p><b>Erst skizzieren, dann rechnen:</b> Die Lösungen von \(|A| = c\) sind die Stellen, an denen die Waagrechte \(y = c\) den Graphen schneidet. Die Skizze zeigt, wie viele es sind.</p>
          <p><b>Rechnen:</b> Für \(c \gt 0\) gilt \(|A| = c \iff A = c \;\vee\; A = -c\). Für \(c = 0\): \(A = 0\). Für \(c \lt 0\): \(L = \{\,\}\).</p>
          <p>\[ |x - 1| = 3 \;\Rightarrow\; x - 1 = 3 \;\vee\; x - 1 = -3 \;\Rightarrow\; L = \{-2;\, 4\} \]</p>
          <p><b>Ungleichungen</b> liest man am Graphen ab: \(|x - 1| \le 3\) gilt, wo das V unter der Waagrechten liegt — <em>zwischen</em> den Schnittstellen, \(-2 \le x \le 4\). \(|x - 1| \ge 3\) gilt <em>ausserhalb</em>: \(x \le -2 \;\vee\; x \ge 4\).</p>
          <p><b>Beim W</b> \(y = |x^2 - 4|\) gibt es bis zu vier Lösungen: \(|x^2 - 4| = 3 \Rightarrow x^2 = 7 \;\vee\; x^2 = 1\), \(L = \{-\sqrt7;\, -1;\, 1;\, \sqrt7\}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur den Fall \(A = c\) rechnen und eine Lösung verlieren — die Skizze zeigt, dass es meist zwei sind.</p>
          <p>Bei \(|x| \le 2\) «\(x \le 2\)» schreiben: Auch \(x = -5\) erfüllt \(x \le 2\), aber \(|-5| = 5\).</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 13, [
    ('5a', 3, r'Löse: \(|x - 4| = 6\); \(|2x + 1| = 5\).',
     r'<p>\(x - 4 = \pm 6\): \(L = \{-2;\, 10\}\).; \(2x + 1 = 5 \Rightarrow x = 2\); \(2x + 1 = -5 \Rightarrow x = -3\): \(L = \{-3;\, 2\}\).</p>', ''),
    ('5b', 3, r'Löse: \(|x + 1| \le 4\); \(|x - 2| \gt 1\).',
     r'<p>Schnittstellen \(-5\) und \(3\), dazwischen: \(-5 \le x \le 3\).; Schnittstellen \(1\) und \(3\), ausserhalb: \(x \lt 1 \;\vee\; x \gt 3\).</p>', ''),
    ('5c', 3, r'Löse \(|x^2 - 9| = 5\). Wie viele Lösungen hat \(|x^2 - 9| = 9\)?',
     r'<p>\(x^2 - 9 = 5 \Rightarrow x = \pm\sqrt{14}\); \(x^2 - 9 = -5 \Rightarrow x = \pm 2\). \(L = \{-\sqrt{14};\, -2;\, 2;\, \sqrt{14}\}\).; Bei \(c = 9\) berührt die Waagrechte den Buckel \((0 \mid 9)\): drei Lösungen (\(0\) und \(\pm\sqrt{18}\)).</p>', ''),
    ('5d', 2, r'Lies am Graphen von \(y = |x + 1| - 2\) ab: Wo ist \(y = 1\)? Bestätige rechnerisch.',
     r'<p>Die Waagrechte \(y = 1\) schneidet bei \(x = -4\) und \(x = 2\). Rechnung: \(|x + 1| = 3 \Rightarrow x + 1 = \pm 3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="v,1,-1,-2" data-fenster="-5,4,-3,4" data-waagrecht="1" data-xm="-4,-2,2" data-ym="-2,1,3"></svg></div>'),
    ('5e', 2, r'Warum hat \(|x - 3| = -2\) keine Lösung, \(|x - 3| = 0\) genau eine und \(|x - 3| = 2\) zwei?',
     r'<p>Das V von \(|x - 3|\) liegt nie unter der \(x\)-Achse: Die Waagrechte \(y = -2\) trifft es nicht. \(y = 0\) berührt es nur im Knick \((3 \mid 0)\). Jede Waagrechte darüber schneidet beide Äste.</p>', ''),
], zwei=False)
k5 = kapitel(5, 'gleichungen', 'Gleichungen und Ungleichungen', 40,
             r'Du löst Betragsgleichungen und -ungleichungen am Graphen und rechnerisch mit zwei Fällen, zählst die Lösungen an der Skizze und vergleichst beide Wege.',
             ('s3-6-lp-gleichungen', 'Gleichungen und Ungleichungen'),
             sim5, ('s3-6-lp-kontrolle-gleichungen', 'Kontrollfragen zu Gleichungen und Ungleichungen'),
             fest5, [uebung('betrag-gleichung', 'Betragsgleichung lösen'), uebung('betrag-ungleichung', 'Betragsungleichung lösen')],
             auf5, f'<a href="{TS}#theorie">Themenseite 3.6, grafisch lösen</a> und <a href="../schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html">Teilgebiet 2.2c, Betragsgleichungen</a>', komp='K5')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-sf">Vorwissen · SP 2.2c · 3.1 · 3.3</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Lineare Gleichungen, Geraden, das Verschieben von Graphen und die Zahlengerade. Wenn das wackelt: <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1, Grundlagen der Funktionen</a> und <a href="../schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html">Teilgebiet 2.2c</a>.</p>
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Löse \(2x - 6 = 0\) und \(-x + 4 = 0\). Welche Steigung hat \(y = -2x + 1\)?',
     r'<p>\(x = 3\); \(x = 4\); Steigung \(-2\).</p><p class="komm">Nullstellen von linearen Termen braucht jedes Kapitel: Dort liegt der Knick.</p>', ''),
    ('0b', 3, r'Der Graph von \(y = x^2\) wird um \(2\) nach rechts und \(1\) nach oben verschoben. Wie heisst die Gleichung, und wo liegt der Scheitel?',
     r'<p>\(y = (x - 2)^2 + 1\), Scheitel \((2 \mid 1)\).</p><p class="komm">Falsch? Nach rechts heisst \(x - 2\). Genau so verschiebt Kapitel 2 das V. <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1</a></p>', ''),
    ('0c', 2, r'Wie weit sind \(-3\) und \(4\) auf der Zahlengeraden voneinander entfernt? Und \(-3\) und \(-7\)?',
     r'<p>\(7\); \(4\).</p><p class="komm">Abstände sind nie negativ — genau das ist der Betrag.</p>', ''),
    ('0d', 2, r'Bestimme die Nullstellen und den Scheitel von \(f(x) = x^2 - 4x - 5\).',
     r'<p>\(x^2 - 4x - 5 = (x + 1)(x - 5)\): Nullstellen \(-1\) und \(5\). Scheitel in der Mitte, \(x = 2\): \((2 \mid -9)\).</p><p class="komm">Falsch? Nullstellen und Scheitel einer Parabel braucht Kapitel 3 beim Umklappen. <a href="quadratische-funktionen.html">Leitprogramm Quadratische Funktionen</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/betragsfunktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-sf">SP 3.6 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg, ohne Taschenrechner.<br>
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
          <p>Aufgabe → Kapitel: G1 → 1; G2, G3 → 2; G4 → 3; G5 → 4; G6 → 5; G7 → 3, 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Betragsfunktionen, Version 1.0 (05.10.2026). Gebaut aus
     scripts/lp/betragsfunktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     Teilgebiet 3.6 ist eine Ergänzung des TALS-Lehrmittels, kein RLP-2030-Teilgebiet. Es verbindet
     SP 2.2 «elementare Betragsgleichungen lösen (auch ohne Hilfsmittel)» mit der Funktionssicht
     aus SP 3.1. Die Kompetenzen sind die der Themenseite s3-6 (Box «Ergänzung TALS»):
       K1  die Betragsfunktion f(x) = |x| abschnittsweise definieren und ihren Graphen skizzieren
           (auch ohne Hilfsmittel)
       K2  Betragsfunktionen der Form y = a·|x − u| + v skizzieren und die Parameter interpretieren
           (auch ohne Hilfsmittel)
       K3  den Betrag linearer und quadratischer Funktionen y = |f(x)| mit dem Umklapp-Prinzip
           grafisch darstellen
       K4  Betragsterme abschnittsweise (ohne Betragsstriche) schreiben und abschnittsweise
           definierte Funktionen lesen
       K5  Betragsgleichungen und -ungleichungen grafisch lösen und mit der algebraischen Lösung
           vergleichen

     Kompetenzmatrix (Kompetenz | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | 1 | 1a–1f | G1
       K2 | 2 | 2a–2e | G2, G3
       K3 | 3 | 3a–3e | G4, G7
       K4 | 4 | 4a–4e | G5
       K5 | 5 | 5a–5e | G6, G7
     Kein Kapitelziel ohne Kompetenz. Der ganze Gesamttest ohne Taschenrechner.

     Bewusst weggelassen (→ Themenseite): die Anwendungen Abfüllanlage, Standort und Fräse
     (Aufgaben A4–A6), Betragsfunktionen mit anderen Grundfunktionen (|sin x| u. ä.).

     Konventionen wie auf der Themenseite: Knickpunkt (u | v), y = a·|x − u| + v, Umklapp-Prinzip,
     Wanne |x − a| + |x − b|, W = ℝ₀⁺. Farben: Betragskurve blau, Waagrechte und Lösungen orange,
     Äste als Geraden grün; die Zielkurve der Simulationen ist grau, weil grün die Äste sind.

     Muster je Kapitel: ① Einführungsclip → ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit
     Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF aus LaTeX (downloads/leitprogramme/betragsfunktionen/*.tex).
     Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Betragsfunktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Schwerpunktfach 3.6</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Die Betragsfunktion</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Verschieben und Strecken</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Umklappen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Abschnittsweise schreiben</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Gleichungen</span></a></li>
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
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Teilgebiet 3.6 ist eine Ergänzung des TALS-Lehrmittels, kein Teilgebiet des RLP-BM 2030. Es verbindet «elementare Betragsgleichungen lösen» (SP 2.2) mit der Funktionssicht aus SP 3.1. Die Kompetenzen der Themenseite:</p>
        <ul>
          <li><b>K1</b> die Betragsfunktion \\(f(x) = |x|\\) abschnittsweise definieren und ihren Graphen skizzieren <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1</li>
          <li><b>K2</b> Betragsfunktionen der Form \\(y = a \\cdot |x - u| + v\\) skizzieren und die Parameter interpretieren <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 2</li>
          <li><b>K3</b> den Betrag linearer und quadratischer Funktionen \\(y = |f(x)|\\) mit dem Umklapp-Prinzip grafisch darstellen — Kapitel 3</li>
          <li><b>K4</b> Betragsterme abschnittsweise (ohne Betragsstriche) schreiben und abschnittsweise definierte Funktionen lesen — Kapitel 4</li>
          <li><b>K5</b> Betragsgleichungen und -ungleichungen grafisch lösen und mit der algebraischen Lösung vergleichen — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Nicht hier, sondern auf der <a href="../schwerpunkt/s3-6-betragsfunktionen.html">Themenseite 3.6</a>: die Anwendungen Abfüllanlage, Standort und Fräse.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Betragsfunktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Kapitel = Lektion: keine Lektionsbänder mehr (Abnahme 06.10.2026).
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (05.10.2026): Vorwissen 10 (vorab) · K1 35 · K2 45 · K3 40 · K4 40 · K5 40 · Gesamttest 30 = 240 min
body = (oben + k0 + k1
        + k2 + k3
        + k4 + k5
        + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
