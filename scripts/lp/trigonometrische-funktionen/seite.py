"""Baut leitprogramme/trigonometrische-funktionen.html aus einer Kapitelbeschreibung (05.10.2026).

  python3 scripts/lp/trigonometrische-funktionen/seite.py

Leitprogramm zum Teilgebiet SP 3.5 (Themenseite s3-5-trigonometrische-funktionen.html), die eine
RLP-Kompetenz des Teilgebiets. Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden
Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf
kommt das Gerüst aus leitprogramme/exp-log-funktionen.html, mit eigenem Titel und eigenen
localStorage-Schlüsseln. Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach
Pre-Flight und python3 scripts/build-seo.py. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/trigonometrische-funktionen.html'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/exp-log-funktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Exponential- und Logarithmusfunktionen</title>',
                      '<title>Leitprogramm Trigonometrische Funktionen</title>')
    alt = alt.replace('lp-explog-', 'lp-trigo-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Exponential- und Logarithmusfunktionen', '\n/* ════════ Trigonometrische Funktionen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Exponential- und Logarithmusfunktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Trigonometrische Funktionen — Simulationen')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Schwerpunktfach · Leitprogramm Exponential- und Logarithmusfunktionen', 'Schwerpunktfach · Leitprogramm Trigonometrische Funktionen')
fuss = fuss.replace('Exponential- und Logarithmusfunktionen', 'Trigonometrische Funktionen')
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 5. Oktober 2026', fuss)

CSS = '''
/* ════════ Trigonometrische Funktionen (05.10.2026) — Kapitelmuster wie Exponential- und Logarithmusfunktionen ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Eigen sind der
   Einheitskreis links neben der Kurve und die Farben: Sinus blau, Cosinus grün, Tangens orange. */
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
/* Farben im ganzen Leitprogramm: blau = Sinus, grün = Cosinus, orange = Tangens, rot =
   Gegenbeispiel, Tinte = neutral (Einheitskreis, Mittellinie, Pole, Waagrechte y = c).
   Dieselben Farben tragen die Clips (farbe 1 blau, 3 grün, 2 orange, 5 Tinte). */
.sim .normal{stroke-dasharray:5 4;stroke:var(--tinte-2);fill:none;stroke-width:1.4}
.sim .normal.gruen{stroke:var(--gruen);stroke-width:2}
.sim .asym,svg.mini .asym{stroke:var(--tinte-2);stroke-width:1.2;stroke-dasharray:4 3;fill:none}
.sim .zielkurve{stroke:var(--tinte-2);stroke-width:5;opacity:.3;fill:none;stroke-dasharray:none}
.p-pkt{fill:var(--tinte)} .p-lauf{fill:var(--blau)} .p-lauf.gruen{fill:var(--gruen)} .p-lauf.orange{fill:var(--orange)}
svg.mini .p-pkt{fill:var(--tinte)}
.sim .kurve.gruen,svg.mini .kurve.gruen{stroke:var(--gruen)}
.sim .kurve.orange,svg.mini .kurve.orange{stroke:var(--orange)}
.sim .kurve.orange.hell{opacity:.22}
svg.mini .kurve.gestrichelt{stroke-dasharray:4 3}
.sim .einheitskreis{fill:none;stroke:var(--tinte-2);stroke-width:1.2}
.sim .radius,.sim .tangente{stroke:var(--tinte-2);stroke-width:1.1}
.sim .strahl{stroke:var(--tinte-2);stroke-width:1.1;stroke-dasharray:3 2}
.sim .bogen{fill:none;stroke-width:4.5;opacity:.4;stroke-linecap:round}
.sim .bogen.blau{stroke:var(--blau)} .sim .bogen.gruen{stroke:var(--gruen)} .sim .bogen.orange{stroke:var(--orange)}
.sim .koord{stroke-width:3.2;stroke-linecap:round}
.sim .koord.blau{stroke:var(--blau)} .sim .koord.gruen{stroke:var(--gruen)} .sim .koord.orange{stroke:var(--orange)}
.sim .projektion{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:4 3}
.sim .waagrechte,svg.mini .waagrechte{stroke:var(--tinte);stroke-width:1.3;stroke-dasharray:6 4}
.mini-reihe svg.mini{background:var(--karte)}
svg.mini[data-t]{width:300px;max-width:100%}
.uebung[data-typ="aus-graph"] svg.ue-bild{width:300px;max-width:100%}
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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, hm=False):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-sf">SP 3.5 · {'mit Hilfsmittel' if hm else 'ohne Hilfsmittel'}</span><span class="zeit">≈ {zeit} min</span></div>
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


TS = '../schwerpunkt/s3-5-trigonometrische-funktionen.html'
EK = '../grundlagen/g5-4-einheitskreis.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 140" role="img" aria-label="Einheitskreis mit dem Punkt P und daneben die Sinuskurve bis zum eingestellten Winkel"></svg>
        <label class="sim-schalter"><input type="checkbox"> Cosinus statt Sinus</label>
        <div class="sl-row">
          {regler('s1', 'x', 'Winkel x', 0, 24, 1, 2, 'blau', pi=12)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sinus und Cosinus am Einheitskreis</div>
          <p>Zum Winkel \(x\) gehört auf dem Einheitskreis der Punkt</p>
          <p>\[ P = (\cos x \mid \sin x) \]</p>
          <p>Der <b>Sinus</b> ist seine Höhe, der <b>Cosinus</b> seine waagrechte Koordinate. Beide liegen darum zwischen \(-1\) und \(1\).</p>
          <p><b>Bogenmass:</b> Der Winkel wird mit der Länge des Bogens gemessen. \(360^\circ = 2\pi\), \(180^\circ = \pi\), also</p>
          <p>\[ x = \frac{\alpha}{180^\circ} \cdot \pi \qquad \text{zum Beispiel } 135^\circ = \tfrac{3\pi}{4} \]</p>
          <p><b>Die Kurven:</b> Trägt man \(\sin x\) über \(x\) ab, entsteht die <b>Sinuskurve</b>, mit \(\cos x\) die <b>Cosinuskurve</b>. Fünf Stützstellen genügen für eine Skizze:</p>
          <p>\[ \begin{array}{c|ccccc} x & 0 & \tfrac{\pi}{2} & \pi & \tfrac{3\pi}{2} & 2\pi \\ \hline \sin x & 0 & 1 & 0 & -1 & 0 \\ \cos x & 1 & 0 & -1 & 0 & 1 \end{array} \]</p>
          <p>Dazu die Werte \(\tfrac12\) und \(-\tfrac12\): \(\sin \tfrac{\pi}{6} = \tfrac12\), \(\cos \tfrac{\pi}{3} = \tfrac12\) — am Einheitskreis mit Vorzeichen in die anderen Quadranten übertragen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Sinus und Cosinus vertauschen: Der Sinus ist die <em>Höhe</em>, die zweite Koordinate von \(P\).</p>
          <p>Den Rechner im Gradmodus lassen: Bei Funktionsgraphen ist \(x\) im Bogenmass. Im Modus DEG gibt \(\sin \pi\) nicht \(0\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Rechne um: \(225^\circ\) ins Bogenmass; \(\tfrac{5\pi}{6}\) in Grad; \(x = 1\) (Bogenmass) in Grad, exakt. Etwa wie viel Grad sind das?',
     r'<p>\(225^\circ = \tfrac{225}{180}\,\pi = \tfrac{5\pi}{4}\); \(\tfrac{5\pi}{6} = \tfrac56 \cdot 180^\circ = 150^\circ\); \(1 = \tfrac{180^\circ}{\pi}\), mit \(\pi \approx 3\) also knapp \(60^\circ\) (genau \(57.3^\circ\)).</p>', ''),
    ('1b', 2, r'Gib ohne Taschenrechner an: \(\sin \tfrac{3\pi}{2}\); \(\cos \pi\); \(\cos \tfrac{3\pi}{2}\); \(\sin \tfrac{7\pi}{6}\).',
     r'<p>\(-1\); \(-1\); \(0\); \(-\tfrac12\).</p><p class="komm">\(\tfrac{7\pi}{6}\) liegt im dritten Quadranten, \(\tfrac{\pi}{6}\) nach \(\pi\): gleiche Höhe wie bei \(\tfrac{\pi}{6}\), aber unter der Achse.</p>', ''),
    ('1c', 2, r'Der Punkt \(P(-0.6 \mid 0.8)\) liegt auf dem Einheitskreis. Gib \(\sin x\) und \(\cos x\) an. In welchem Quadranten liegt \(x\)?',
     r'<p>\(\sin x = 0.8\), \(\cos x = -0.6\). Zweiter Quadrant: \(\tfrac{\pi}{2} \lt x \lt \pi\).</p>', ''),
    ('1d', 3, r'Skizziere \(y = \sin x\) und \(y = \cos x\) für \(0 \le x \le 2\pi\) in <em>ein</em> Koordinatensystem — mit je fünf Stützpunkten.',
     r'<p>Sinus durch \((0 \mid 0)\), \(\left(\tfrac{\pi}{2} \mid 1\right)\), \((\pi \mid 0)\), \(\left(\tfrac{3\pi}{2} \mid -1\right)\), \((2\pi \mid 0)\); Cosinus durch \((0 \mid 1)\), \(\left(\tfrac{\pi}{2} \mid 0\right)\), \((\pi \mid -1)\), \(\left(\tfrac{3\pi}{2} \mid 0\right)\), \((2\pi \mid 1)\). Im Bild: Sinus durchgezogen, Cosinus gestrichelt.</p>'
     '<div class="mini-reihe"><svg class="mini" data-t="s,1,1,0,0;c,1,1,0,0" data-fenster="-0.5,6.9,-1.5,1.5" data-xpi="1"></svg></div>', ''),
    ('1e', 2, r'Warum liegen alle Werte von \(\sin x\) zwischen \(-1\) und \(1\) — für jedes noch so grosse \(x\)?',
     r'<p>\(\sin x\) ist die Höhe eines Punktes auf dem Einheitskreis. Der Kreis hat den Radius \(1\): Kein Punkt liegt höher als \(1\) oder tiefer als \(-1\). Ein grosses \(x\) heisst nur, dass \(P\) öfter herumläuft.</p>', ''),
], zwei=False)
k1 = kapitel(1, 'kreis-kurve', 'Vom Einheitskreis zur Kurve', 40,
             r'Du liest Sinus und Cosinus am Einheitskreis ab, rechnest zwischen Grad und Bogenmass um und skizzierst die Sinus- und die Cosinuskurve über eine Periode — ohne Hilfsmittel.',
             ('s3-5-lp-kreis-kurve', 'Vom Einheitskreis zur Kurve'),
             sim1, ('s3-5-lp-kontrolle-kreis-kurve', 'Kontrollfragen zum Einheitskreis'),
             fest1, [uebung('grad-bogen', 'Grad und Bogenmass'), uebung('sin-cos-wert', 'Werte am Einheitskreis')],
             auf1, f'<a href="{TS}#definition">Themenseite 3.5, Definition</a> und <a href="{EK}">Einheitskreis (GF 5.4)</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 150" role="img" aria-label="Verschobene Sinuskurve, gestrichelt die Cosinuskurve"></svg>
        <div class="sl-row">
          {regler('s2', 'u', 'Verschiebung u', -8, 8, 1, 0, 'blau', pi=4)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Periode und Symmetrie</div>
          <p><b>Periode:</b> Nach einer vollen Umdrehung wiederholt sich alles. Sinus und Cosinus haben die <b>Periodenlänge</b> \(p = 2\pi\):</p>
          <p>\[ \sin(x + 2\pi) = \sin x, \qquad \cos(x + 2\pi) = \cos x \]</p>
          <p>\[ \begin{array}{l|c|c} & \sin x & \cos x \\ \hline \text{Wertemenge} & [-1;\, 1] & [-1;\, 1] \\ \text{Nullstellen} & k\pi & \tfrac{\pi}{2} + k\pi \\ \text{Hochstellen} & \tfrac{\pi}{2} + 2k\pi & 2k\pi \\ \text{Tiefstellen} & \tfrac{3\pi}{2} + 2k\pi & \pi + 2k\pi \end{array} \qquad (k \in \mathbb{Z}) \]</p>
          <p><b>Symmetrie:</b> Die Sinuskurve ist <b>punktsymmetrisch</b> zum Ursprung, die Cosinuskurve <b>achsensymmetrisch</b> zur \(y\)-Achse:</p>
          <p>\[ \sin(-x) = -\sin x, \qquad \cos(-x) = \cos x \]</p>
          <p>Zudem ist die Sinuskurve achsensymmetrisch zur Geraden \(x = \tfrac{\pi}{2}\) durch ihren Hochpunkt: \(\sin(\pi - x) = \sin x\).</p>
          <p><b>Versatz:</b> Die Cosinuskurve ist die um \(\tfrac{\pi}{2}\) nach <em>links</em> verschobene Sinuskurve: \(\cos x = \sin\left(x + \tfrac{\pi}{2}\right)\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur die Nullstellen zwischen \(0\) und \(2\pi\) nennen. «Alle Nullstellen» heisst: \(x_0 = k\pi\) mit \(k \in \mathbb{Z}\) — auch \(-\pi\), \(-2\pi\), …</p>
          <p>Die Richtung beim Verschieben: \(\sin\left(x + \tfrac{\pi}{2}\right)\) ist nach <em>links</em> verschoben, nicht nach rechts.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'Gib für \(y = \cos x\) an: Wertemenge, Periodenlänge und <em>alle</em> Nullstellen.',
     r'<p>\(W = [-1;\, 1]\), \(p = 2\pi\), \(x_0 = \tfrac{\pi}{2} + k\pi\) mit \(k \in \mathbb{Z}\).</p>', ''),
    ('2b', 2, r'Gib alle Hochstellen von \(y = \sin x\) im Intervall \([-2\pi;\, 4\pi]\) an.',
     r'<p>\(-\tfrac{3\pi}{2}\), \(\tfrac{\pi}{2}\), \(\tfrac{5\pi}{2}\) — von \(\tfrac{\pi}{2}\) aus je eine Periode \(2\pi\) weiter oder zurück.</p>', ''),
    ('2c', 3, r'Es gilt \(\sin 0.6 \approx 0.565\) und \(\cos 0.6 \approx 0.825\). Gib ohne Taschenrechner an: \(\sin(-0.6)\); \(\cos(-0.6)\); \(\sin(0.6 + 2\pi)\).',
     r'<p>\(\approx -0.565\) (punktsymmetrisch); \(\approx 0.825\) (achsensymmetrisch); \(\approx 0.565\) (Periode \(2\pi\)).</p>', ''),
    ('2d', 3, r'Die gestrichelte Kurve ist die um \(\tfrac{\pi}{2}\) nach rechts verschobene Sinuskurve. Gib ihre Gleichung einmal mit Sinus und einmal mit Cosinus an.',
     r'<p>\(y = \sin\left(x - \tfrac{\pi}{2}\right)\). Sie hat ihren Tiefpunkt bei \(0\) und ihren Hochpunkt bei \(\pi\) — wie die an der \(x\)-Achse gespiegelte Cosinuskurve: \(y = -\cos x\). Gleichwertig, als verschobene Cosinuskurve: \(y = \cos(x - \pi)\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-t="s,1,1,0,0;s,1,1,1.5707963267948966,0" data-fenster="-0.5,6.9,-1.5,1.5" data-xpi="1"></svg></div>'),
    ('2e', 2, r'Begründe am Einheitskreis, warum \(\cos(-x) = \cos x\) gilt.',
     r'<p>Zum Winkel \(-x\) dreht \(P\) gleich weit, aber im Uhrzeigersinn: Der Punkt ist das Spiegelbild an der waagrechten Achse, \((\cos x \mid -\sin x)\). Die waagrechte Koordinate bleibt gleich, nur die Höhe wechselt das Vorzeichen.</p>', ''),
], zwei=False)
k2 = kapitel(2, 'periode-symmetrie', 'Periode und Symmetrie', 40,
             r'Du gibst Wertemenge, Periodenlänge, Nullstellen und Extremstellen von Sinus und Cosinus an, nutzt ihre Symmetrien und weisst, dass die Cosinuskurve eine verschobene Sinuskurve ist.',
             ('s3-5-lp-periode-symmetrie', 'Periode und Symmetrie'),
             sim2, ('s3-5-lp-kontrolle-periode-symmetrie', 'Kontrollfragen zu Periode und Symmetrie'),
             fest2, [uebung('stelle', 'Null-, Hoch- und Tiefstellen'), uebung('symmetrie-wert', 'Werte über Symmetrie')],
             auf2, f'<a href="{TS}#typen">Themenseite 3.5, Eigenschaften</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 220" role="img" aria-label="Einheitskreis mit Tangente und daneben die Tangenskurve bis zum eingestellten Winkel"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Polgeraden (gestrichelt)</label>
        <div class="sl-row">
          {regler('s3', 'x', 'Winkel x', 0, 24, 1, 2, 'orange', pi=12)}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Tangensfunktion</div>
          <p>\[ \tan x = \frac{\sin x}{\cos x} \]</p>
          <p>Am Einheitskreis ist \(\tan x\) die Höhe, in der die Gerade durch den Mittelpunkt und \(P\) die senkrechte Tangente rechts am Kreis trifft (im 2. und 3. Quadranten ihre Verlängerung über den Mittelpunkt hinaus).</p>
          <ul>
            <li>\(D = \mathbb{R} \setminus \left\{\tfrac{\pi}{2} + k\pi\right\}\): Wo \(\cos x = 0\) ist, gibt es keinen Wert. Dort hat die Kurve <b>Pole</b>: Links davon wächst sie über alle Grenzen, rechts davon kommt sie von beliebig weit unten.</li>
            <li>\(W = \mathbb{R}\): Jede Zahl kommt als Wert vor.</li>
            <li><b>Periodenlänge</b> \(p = \pi\): \(\tan(x + \pi) = \tan x\) — nach einer halben Umdrehung wechseln Sinus und Cosinus beide das Vorzeichen.</li>
            <li><b>Nullstellen</b> \(x_0 = k\pi\), wo \(\sin x = 0\) ist.</li>
            <li><b>Punktsymmetrisch</b> zum Ursprung: \(\tan(-x) = -\tan x\).</li>
          </ul>
          <p>Werte: \(\tan 0 = 0\), \(\tan \tfrac{\pi}{4} = 1\) (Sinus und Cosinus gleich gross), \(\tan \tfrac{3\pi}{4} = -1\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Pole und Nullstellen vertauschen: Pole liegen, wo der <em>Cosinus</em> null ist, Nullstellen, wo der <em>Sinus</em> null ist.</p>
          <p>Die Periode \(2\pi\) übernehmen: Der Tangens wiederholt sich schon nach \(\pi\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 3, r'Gib für \(y = \tan x\) an: Definitionsmenge, Wertemenge, Periodenlänge und alle Nullstellen.',
     r'<p>\(D = \mathbb{R} \setminus \left\{\tfrac{\pi}{2} + k\pi\right\}\), \(W = \mathbb{R}\), \(p = \pi\), \(x_0 = k\pi\) mit \(k \in \mathbb{Z}\).</p>', ''),
    ('3b', 2, r'Gib ohne Taschenrechner an: \(\tan \tfrac{3\pi}{4}\); \(\tan \pi\); \(\tan\left(-\tfrac{\pi}{4}\right)\).',
     r'<p>\(-1\); \(0\); \(-1\).</p><p class="komm">\(\tfrac{3\pi}{4}\): Sinus positiv, Cosinus negativ, gleich gross — Quotient \(-1\). \(-\tfrac{\pi}{4}\): Punktsymmetrie, \(-\tan\tfrac{\pi}{4}\).</p>', ''),
    ('3c', 2, r'Es gilt \(\tan 1.2 \approx 2.572\). Gib ohne Taschenrechner an: \(\tan(1.2 - \pi)\) und \(\tan(-1.2)\).',
     r'<p>\(\approx 2.572\) (Periode \(\pi\)); \(\approx -2.572\) (punktsymmetrisch).</p>', ''),
    ('3d', 2, r'Skizziere \(y = \tan x\) für \(-\pi \lt x \lt 2\pi\) mit allen Polgeraden und Nullstellen.',
     r'<p>Pole bei \(-\tfrac{\pi}{2}\), \(\tfrac{\pi}{2}\), \(\tfrac{3\pi}{2}\); Nullstellen bei \(0\) und \(\pi\). Zwischen zwei Polen steigt die Kurve von \(-\infty\) nach \(+\infty\), durch die Nullstelle in der Mitte.</p>'
     '<div class="mini-reihe"><svg class="mini" data-t="t,1,1,0,0" data-fenster="-3.3,6.4,-3,3" data-ym="-2,-1,1,2" data-punkte="0,0;3.141592653589793,0" data-senkrecht="-1.5707963267948966,1.5707963267948966,4.71238898038469"></svg></div>', ''),
    ('3e', 2, r'Warum hat die Tangensfunktion bei \(\tfrac{\pi}{2}\) einen Pol, die Sinusfunktion aber nicht?',
     r'<p>Der Quotient wäre \(\tfrac{\sin(\pi/2)}{\cos(\pi/2)} = \tfrac{1}{0}\): Durch null kann man nicht teilen, und nahe bei \(\tfrac{\pi}{2}\) wird der Quotient beliebig gross. \(\sin \tfrac{\pi}{2} = 1\) ist dagegen einfach die Höhe von \(P\) — sie gibt es für jeden Winkel.</p>', ''),
], zwei=False)
k3 = kapitel(3, 'tangens', 'Die Tangensfunktion', 35,
             r'Du deutest \(\tan x = \frac{\sin x}{\cos x}\) am Einheitskreis, skizzierst die Tangenskurve mit ihren Polen und gibst Definitionsmenge, Periode, Nullstellen und Symmetrie an.',
             ('s3-5-lp-tangens', 'Die Tangenskurve'),
             sim3, ('s3-5-lp-kontrolle-tangens', 'Kontrollfragen zur Tangenskurve'),
             fest3, [uebung('tan-wert', 'Tangenswerte'), uebung('tan-stelle', 'Pole und Nullstellen')],
             auf3, f'<a href="{TS}#typen">Themenseite 3.5, Eigenschaften</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 220" role="img" aria-label="Sinuskurve mit den Parametern a, b, u und v, gestrichelt die Ausgangskurve sin x"></svg>
        <label class="hilfs-schalter"><input type="checkbox" checked> Mittellinie (gestrichelt)</label>
        <div class="sl-row">
          {regler('s4', 'a', 'Amplitude a', 0.5, 3, 0.5, 1, 'grau')}
          {regler('s4', 'b', 'b', 0.5, 4, 0.5, 1, 'grau')}
          {regler('s4', 'u', 'Verschiebung u', -6, 6, 1, 0, 'grau', pi=6)}
          {regler('s4', 'v', 'Mittellinie v', -2, 2, 0.5, 0, 'grau')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Strecken und Verschieben</div>
          <p>\[ y = a \cdot \sin\big(b\,(x - u)\big) + v \qquad (a, b \gt 0) \]</p>
          <ul>
            <li>\(a\) — <b>Amplitude</b>: grösste Abweichung von der Mittellinie (Streckung in \(y\)-Richtung).</li>
            <li>\(b\) — Streckung in \(x\)-Richtung mit Faktor \(\tfrac{1}{b}\): <b>Periodenlänge</b> \(p = \dfrac{2\pi}{b}\).</li>
            <li>\(u\) — Verschiebung in \(x\)-Richtung: \(x - u\) schiebt um \(u\) nach <b>rechts</b>.</li>
            <li>\(v\) — Verschiebung in \(y\)-Richtung: <b>Mittellinie</b> \(y = v\), Wertemenge \(W = [v - a;\, v + a]\).</li>
          </ul>
          <p><b>Schrittweise skizzieren</b>, wie auf der Themenseite: (1) Periode aus \(b\), (2) Amplitude \(a\), (3) um \(u\) schieben, (4) um \(v\) heben. Steht \(\sin(bx + c)\) da, zuerst \(b\) ausklammern: \(\sin\left(2x - \tfrac{\pi}{2}\right) = \sin\left(2\left(x - \tfrac{\pi}{4}\right)\right)\), also \(u = \tfrac{\pi}{4}\).</p>
          <p>Für \(y = a \cos\big(b(x - u)\big) + v\) gilt alles genauso — der Cosinus ist eine verschobene Sinuskurve. Ein <b>Minus vor dem Faktor</b> spiegelt die Kurve an der Mittellinie; die Amplitude ist dann der Betrag: \(y = 25 - 20\cos(\ldots)\) hat die Amplitude \(20\) und startet unten.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Grosses \(b\), lange Periode»: Umgekehrt. Bei \(b = 2\) läuft die Kurve doppelt so schnell, \(p = \pi\).</p>
          <p>Die Verschiebung aus \(\sin(bx + c)\) direkt ablesen: \(\sin\left(2x - \tfrac{\pi}{2}\right)\) ist um \(\tfrac{\pi}{4}\) verschoben, nicht um \(\tfrac{\pi}{2}\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Gib Amplitude, Periodenlänge und Wertemenge an: (a) \(y = 3\sin(2x) - 1\) (b) \(y = 0.5\sin\left(\tfrac{x}{2}\right) + 2\).',
     r'<p>(a) \(a = 3\), \(p = \pi\), \(W = [-4;\, 2]\). (b) \(a = 0.5\), \(p = 4\pi\), \(W = [1.5;\, 2.5]\).</p>', ''),
    ('4b', 3, r'Skizziere \(y = 2\sin\left(x - \tfrac{\pi}{3}\right) + 1\) für \(0 \le x \le 2\pi\). Gib Hoch- und Tiefpunkt in diesem Bereich an.',
     r'<p>Mittellinie \(y = 1\), Amplitude \(2\), um \(\tfrac{\pi}{3}\) nach rechts. Hochpunkt \(\left(\tfrac{\pi}{3} + \tfrac{\pi}{2} \mid 3\right) = \left(\tfrac{5\pi}{6} \mid 3\right)\), Tiefpunkt \(\left(\tfrac{11\pi}{6} \mid -1\right)\).</p>'
     '<div class="mini-reihe"><svg class="mini" data-t="s,2,1,1.0471975511965976,1;s,1,1,0,0" data-fenster="-0.5,6.9,-1.5,3.5" data-xpi="1" data-ym="-1,1,2,3" data-punkte="2.6179938779914944,3;5.759586531581287,-1"></svg></div>', ''),
    ('4c', 3, r'Bestimme die Gleichung der abgebildeten Kurve in der Form \(y = a \sin(bx) + v\).',
     r'<p>Mittellinie \(y = 0\), höchster Wert \(1.5\): \(a = 1.5\), \(v = 0\). Periode \(4\pi\) (von \(0\) bis zur nächsten Nullstelle mit gleicher Steigung): \(b = \tfrac{2\pi}{4\pi} = 0.5\). Also \(y = 1.5\sin(0.5x)\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-t="s,1.5,0.5,0,0" data-fenster="-0.5,13,-2,2" data-ym="-1.5,-1,1,1.5" data-sy="0.5"></svg></div>'),
    ('4d', 3, r'Die Höhe einer Kabine im Riesenrad ist \(h(t) = 25 - 20\cos\left(\tfrac{\pi}{4}\,t\right)\) (\(h\) in m, \(t\) in min). (a) Wie hoch liegen tiefster und höchster Punkt? (b) Wie lange dauert eine Umdrehung? (c) Wie hoch ist die Kabine nach \(2\) und nach \(4\) Minuten?',
     r'<p>Das Minus vor der \(20\) spiegelt die Cosinuskurve: Die Kabine startet bei \(t = 0\) unten. (a) \(25 - 20 = 5\) m und \(25 + 20 = 45\) m. (b) \(p = \tfrac{2\pi}{\pi/4} = 8\) min. (c) \(h(2) = 25 - 20\cos\tfrac{\pi}{2} = 25\) m, \(h(4) = 25 - 20\cos\pi = 45\) m.</p>', ''),
    ('4e', 2, r'Warum macht ein grösseres \(b\) die Periode kürzer?',
     r'<p>Die Kurve wiederholt sich, wenn das Argument \(bx\) um \(2\pi\) gewachsen ist. Bei grossem \(b\) wächst \(bx\) schnell — das geschieht schon nach \(x = \tfrac{2\pi}{b}\).</p>', ''),
], zwei=False)
k4 = kapitel(4, 'parameter', 'Strecken und Verschieben', 45,
             r'Du beschreibst die Wirkung von \(a\), \(b\), \(u\) und \(v\) in \(y = a \sin\big(b(x - u)\big) + v\), liest Amplitude, Periodenlänge, Verschiebung und Mittellinie ab und skizzierst den Graphen schrittweise.',
             ('s3-5-lp-parameter', 'Strecken und Verschieben'),
             sim4, ('s3-5-lp-kontrolle-parameter', 'Kontrollfragen zu den Parametern'),
             fest4, [uebung('kenngroessen', 'Kenngrössen ablesen'), uebung('aus-graph', 'Gleichung aus dem Graphen', True)],
             auf4, f'<a href="{TS}#theorie">Themenseite 3.5, Transformationen und allgemeine Sinusfunktion</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 440 170" role="img" aria-label="Sinuskurve oder Cosinuskurve mit einer Waagrechten y gleich c und den Schnittstellen"></svg>
        <label class="sim-schalter"><input type="checkbox"> Cosinus statt Sinus</label>
        <div class="sl-row">
          {regler('s5', 'c', 'Waagrechte y = c', -1.5, 1.5, 0.1, 0.4, 'grau')}
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Symmetrie nutzen: alle Lösungen</div>
          <p>Die Gleichung \(\sin x = c\) fragt: Wo schneidet die Waagrechte \(y = c\) die Sinuskurve? Für \(-1 \lt c \lt 1\) sind es <b>zwei Stellen pro Periode</b>.</p>
          <p><b>Sinus:</b> Der Rechner (im Bogenmass, RAD) liefert \(x_1 = \sin^{-1}(c)\) — die Umkehrfunktion, auch \(\arcsin c\) geschrieben (nicht \(\tfrac{1}{\sin c}\)). Die Kurve ist symmetrisch zur Geraden \(x = \tfrac{\pi}{2}\), also</p>
          <p>\[ x_2 = \pi - x_1 \]</p>
          <p><b>Cosinus:</b> Der Rechner liefert \(x_1 = \cos^{-1}(c)\). Die Kurve ist symmetrisch zur Geraden \(x = \pi\), also</p>
          <p>\[ x_2 = 2\pi - x_1 \]</p>
          <p><b>Periode:</b> Alle weiteren Lösungen liegen \(2\pi\) daneben: \(x_1 + 2k\pi\), \(x_2 + 2k\pi\).</p>
          <p>Liefert der Rechner beim Sinus ein negatives \(x_1\) (bei \(c \lt 0\)), liegt \(x_1 + 2\pi\) in \([0;\, 2\pi]\). Bei \(c = \pm 1\) berührt die Waagrechte nur Hoch- oder Tiefpunkte: eine Stelle pro Periode. Bei \(|c| \gt 1\) gibt es <b>keine</b> Lösung.</p>
          <p><b>Faktor im Argument:</b> Bei \(\sin(bx) = c\) zuerst \(z = bx\) setzen, \(\sin z = c\) lösen, dann durch \(b\) teilen. Beispiel \(\sin(2x) = \tfrac12\) für \(0 \le x \le 2\pi\): \(z\) läuft von \(0\) bis \(4\pi\), also \(z = \tfrac{\pi}{6}, \tfrac{5\pi}{6}, \tfrac{13\pi}{6}, \tfrac{17\pi}{6}\) und \(x = \tfrac{\pi}{12}, \tfrac{5\pi}{12}, \tfrac{13\pi}{12}, \tfrac{17\pi}{12}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur die eine Lösung des Rechners angeben: \(\sin x = 0.6\) hat in \([0;\, 2\pi]\) <em>zwei</em> Lösungen, \(0.644\) und \(2.498\).</p>
          <p>Die Regeln vertauschen: \(\pi - x_1\) gilt beim Sinus, \(2\pi - x_1\) beim Cosinus. Eine Skizze zeigt, welche stimmt.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 3, r'Löse \(\sin x = -0.3\) im Intervall \([0;\, 2\pi]\), auf drei Dezimalen.',
     r'<p>Der Rechner gibt \(x_1 = \sin^{-1}(-0.3) \approx -0.305\) — nicht im Intervall. Eine Periode weiter: \(-0.305 + 2\pi \approx 5.978\). Die zweite: \(\pi - (-0.305) \approx 3.446\).</p><p class="komm">Kontrolle an der Skizze: Beide liegen unter der \(x\)-Achse, zwischen \(\pi\) und \(2\pi\), symmetrisch zu \(\tfrac{3\pi}{2}\).</p>', ''),
    ('5b', 3, r'Löse \(\cos x = -0.5\) im Intervall \([0;\, 2\pi]\) — exakt, als Vielfache von \(\pi\).',
     r'<p>\(\cos \tfrac{\pi}{3} = \tfrac12\), also liegt \(x_1\) im zweiten Quadranten: \(x_1 = \pi - \tfrac{\pi}{3} = \tfrac{2\pi}{3}\) (der Rechner gibt \(2.094\)). \(x_2 = 2\pi - \tfrac{2\pi}{3} = \tfrac{4\pi}{3}\).</p>', ''),
    ('5c', 2, r'Wie viele Lösungen hat \(\sin x = 0.7\) im Intervall \([0;\, 4\pi]\)? Gib sie auf drei Dezimalen an.',
     r'<p>Vier: \(0.775\), \(2.366\), \(7.059\), \(8.649\) — die beiden aus \([0;\, 2\pi]\) und dieselben plus \(2\pi\).</p>', ''),
    ('5d', 2, r'Lies am Graphen ab (Gitter alle \(\tfrac{\pi}{6}\)): Wo ist \(\sin x = -\tfrac12\) im Intervall \([0;\, 2\pi]\)? Kontrolliere mit der Symmetrie.',
     r'<p>\(x_1 = \tfrac{7\pi}{6}\), \(x_2 = \tfrac{11\pi}{6}\). Kontrolle: Symmetrieachse ist hier die Gerade \(x = \tfrac{3\pi}{2}\) durch den Tiefpunkt, und \(\tfrac{7\pi}{6}\) und \(\tfrac{11\pi}{6}\) liegen gleich weit davon.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-t="s,1,1,0,0" data-fenster="-0.5,6.9,-1.5,1.5" data-xpi="1" data-xteil="6" data-waagrecht="-0.5"></svg></div>'),
    ('5e', 2, r'Warum hat \(\sin x = c\) für \(|c| \gt 1\) keine Lösung, für \(-1 \lt c \lt 1\) aber in jeder Periode genau zwei?',
     r'<p>Die Sinuskurve bleibt zwischen \(-1\) und \(1\); eine Waagrechte darüber oder darunter trifft sie nie. Dazwischen schneidet die Waagrechte jeden Bogen: einmal beim Hinauf- oder Hinuntergehen und einmal beim Zurückkommen — zwei Stellen pro Periode.</p>', ''),
    ('5f', 2, r'Die Kabine aus Aufgabe 4d: \(h(t) = 25 - 20\cos\left(\tfrac{\pi}{4}\,t\right)\). Wann ist sie während der ersten Umdrehung (\(0 \le t \le 8\)) genau \(35\) m hoch? Exakt.',
     r'<p>\(25 - 20\cos\left(\tfrac{\pi}{4}t\right) = 35 \Rightarrow \cos\left(\tfrac{\pi}{4}t\right) = -\tfrac12\). Mit \(z = \tfrac{\pi}{4}t\), \(0 \le z \le 2\pi\): \(z = \tfrac{2\pi}{3}\) oder \(z = 2\pi - \tfrac{2\pi}{3} = \tfrac{4\pi}{3}\). Zurück: \(t = \tfrac{4}{\pi} z = \tfrac83 \approx 2.67\) min und \(t = \tfrac{16}{3} \approx 5.33\) min.</p>', ''),
], zwei=False)
k5 = kapitel(5, 'symmetrie-nutzen', 'Symmetrie nutzen', 40,
             r'Du löst Gleichungen wie \(\sin x = 0.4\) oder \(\sin(2x) = c\) mit dem Taschenrechner und findest alle Lösungen in einem Intervall über Symmetrie und Periode — mit der Skizze als Kontrolle.',
             ('s3-5-lp-gleichungen', 'Symmetrie nutzen'),
             sim5, ('s3-5-lp-kontrolle-gleichungen', 'Kontrollfragen zum Symmetrie-Nutzen'),
             fest5, [uebung('zweite-loesung', 'Die zweite Lösung'), uebung('anzahl-loesungen', 'Wie viele Lösungen?')],
             auf5, f'<a href="{TS}#aufgaben">Themenseite 3.5, Aufgabe A3 e</a> und <a href="../grundlagen/g5-5-trigonometrische-gleichungen.html">Trigonometrische Gleichungen (GF 5.5)</a>', hm=True)

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-sf">Vorwissen · GF 5.4 · SP 3.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Der Einheitskreis, Grad- und Bogenmass, Verschieben von Graphen und Symmetrie. Wenn das wackelt: <a href="../grundlagen/g5-4-einheitskreis.html">Einheitskreis (GF 5.4)</a> und <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1, Grundlagen der Funktionen</a>.</p>
      ''' + clipkarte('g5-4-gradmass-bogenmass', 'Einheitskreis: Gradmass und Bogenmass') + '''
      ''' + clipkarte('g5-4-einheitskreis', 'Einheitskreis: Sinus und Cosinus als Koordinaten') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Rechne ins Bogenmass um: \(60^\circ\); \(30^\circ\); \(360^\circ\).',
     r'<p>\(\tfrac{\pi}{3}\); \(\tfrac{\pi}{6}\); \(2\pi\).</p><p class="komm">Falsch? \(180^\circ = \pi\) — der erste Clip oben.</p>', ''),
    ('0b', 3, r'Gib die Koordinaten des Punktes auf dem Einheitskreis an, der zum Winkel \(90^\circ\) gehört, und zu \(180^\circ\). Wie gross ist \(\sin 30^\circ\)?',
     r'<p>\((0 \mid 1)\); \((-1 \mid 0)\); \(\sin 30^\circ = \tfrac12\).</p><p class="komm">Falsch? Der Punkt hat die Koordinaten \((\cos \alpha \mid \sin \alpha)\) — der zweite Clip oben. <a href="../grundlagen/g5-4-einheitskreis.html">GF 5.4</a></p>', ''),
    ('0c', 2, r'Der Graph von \(f(x) = x^2\) wird um \(2\) nach rechts und um \(1\) nach oben verschoben. Wie heisst die neue Gleichung?',
     r'<p>\(y = (x - 2)^2 + 1\).</p><p class="komm">Nach rechts heisst: \(x - 2\) einsetzen. Genau so verschiebt Kapitel 4 die Sinuskurve. <a href="../schwerpunkt/s3-1-grundlagen.html">Teilgebiet 3.1</a></p>', ''),
    ('0d', 2, r'Ist der Graph von \(f(x) = x^3 - x\) achsensymmetrisch zur \(y\)-Achse, punktsymmetrisch zum Ursprung oder keines von beiden? Begründe mit \(f(-x)\).',
     r'<p>\(f(-x) = -x^3 + x = -f(x)\): punktsymmetrisch zum Ursprung.</p><p class="komm">\(f(-x) = f(x)\) heisst achsensymmetrisch, \(f(-x) = -f(x)\) punktsymmetrisch — beides braucht Kapitel 2.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1. Sind 0a oder 0b falsch, zuerst den Einheitskreis wiederholen — ohne ihn gehen alle Kapitel nicht.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/trigonometrische-funktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-sf">SP 3.5 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Teil A ohne, Teil B mit Taschenrechner: Die Kompetenz des Teilgebiets trägt im Lehrplan den Vermerk «mit und ohne Hilfsmittel».<br>
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
          <p>Aufgabe → Kapitel: G1 → 1, 2; G2 → 1, 3; G3 → 2; G4 → 3; G5, G6 → 4; G7 → 5; G8 → 4, 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Trigonometrische Funktionen, Version 1.0 (05.10.2026). Gebaut aus
     scripts/lp/trigonometrische-funktionen/seite.py — Änderungen dort, nicht in dieser Datei.

     RLP-BM 2030, Schwerpunktfach 3.5 «Trigonometrische Funktionen», die Kompetenz wörtlich
     (Quelle ../Math-SP.pdf, Lerngebiet 3 «Funktionen»; gleich wie in der RLP-Box der Themenseite s3-5):
       K1  den Funktionsverlauf der Sinus-, Kosinus- und Tangensfunktion visualisieren sowie die
           elementaren Eigenschaften kennen (Periodizität, Symmetrien) (mit und ohne Hilfsmittel.)
     Das Teilgebiet hat nur diese eine Kompetenz; sie tragen Kapitel 1–3 (ohne Hilfsmittel). Kapitel 4
     und 5 wenden sie an und stützen sich dabei auf andere Teilgebiete (Prüfung 05.10.2026, M1):
       Kapitel 4  Transformationen y = a·sin(b(x − u)) + v — SP 3.1 «Funktionstransformationen»
       Kapitel 5  alle Lösungen von sin x = c, auch sin(bx) = c, mit dem Rechner — GF 5.5
                  «elementare trigonometrische Gleichungen … mithilfe der Arkusfunktion lösen»

     Kompetenzmatrix (Teil | Hilfsmittel | Kapitel | Kapitelaufgaben | Gesamttest):
       Funktionsverlauf visualisieren  | ohne | 1, 3, 4 | 1d, 3d, 4b, 4c | G1, G4, G5, G6
       Periodizität                    | ohne | 2, 3    | 2a, 2b, 3a, 3c | G4, G5
       Symmetrien, Versatz sin/cos     | ohne | 2, 3    | 2c–2e, 3c      | G1, G3
       Eigenschaften nutzen (GF 5.5)   | mit  | 5       | 5a–5f          | G7, G8
     Kein Kapitelziel ohne Kompetenz. Teil A des Gesamttests ohne, Teil B mit Taschenrechner.

     Bewusst weggelassen (→ Themenseite): die harmonische Schwingung mit ω, Frequenz und Phase
     (Physik-Anwendung, hier nur das Riesenrad in 4d und die Gezeiten im Gesamttest), die Beziehungen
     cos(π − x), tan(π − x) usw. als Tabelle (hier nur sin(π − x), weil Kapitel 5 sie braucht), die
     Form y = a·sin(bx + c) mit x₀ = −c/b (hier: b ausklammern) und Altgrad-Graphen.

     Konventionen wie auf der Themenseite: x im Bogenmass, P = (cos x | sin x), Periodenlänge p,
     k ∈ ℤ, y = a·sin(b(x − u)) + v mit a, b > 0. Farben: Sinus blau, Cosinus grün, Tangens orange;
     die Zielkurve der Simulationen ist darum grau statt grün wie in den anderen Leitprogrammen.

     Muster je Kapitel: ① Einführungsclip → ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit
     Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF aus LaTeX (downloads/leitprogramme/trigonometrische-funktionen/*.tex).
     Verfahren: HOWTO-leitprogramme.md. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Trigonometrische Funktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Schwerpunktfach 3.5</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Vom Kreis zur Kurve</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Periode und Symmetrie</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Tangensfunktion</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Strecken und Verschieben</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Symmetrie nutzen</span></a></li>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Vielfache von \\(\\pi\\) tippst du als <code>3π/4</code> oder <code>3pi/4</code>.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Schwerpunktfach 3.5 — die Kompetenz des Teilgebiets.</p>
        <ul>
          <li>den Funktionsverlauf der Sinus-, Kosinus- und Tangensfunktion visualisieren sowie die elementaren Eigenschaften kennen (Periodizität, Symmetrien) <span class="ohm">mit und ohne Hilfsmittel</span> — Kapitel 1 bis 3 ohne Taschenrechner</li>
        </ul>
        <p class="rlp-quelle">Dazu zwei Anwendungen aus anderen Teilgebieten: Kapitel 4 verschiebt und streckt die Kurven (Funktionstransformationen, SP 3.1), Kapitel 5 nutzt Symmetrie und Periode, um trigonometrische Gleichungen mit dem Taschenrechner vollständig zu lösen (GF 5.5 «elementare trigonometrische Gleichungen … mithilfe der Arkusfunktion lösen», SP 3.1).</p>
        <p class="rlp-quelle">Nicht hier, sondern auf der <a href="../schwerpunkt/s3-5-trigonometrische-funktionen.html">Themenseite 3.5</a>: harmonische Schwingungen mit Kreisfrequenz und Phase und die vollständige Tabelle der Beziehungen aus Periodizität und Symmetrie.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Trigonometrische Funktionen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Kapitel = Lektion: keine Lektionsbänder mehr (Abnahme 06.10.2026).
band = lambda n, t: f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'
# Zeiten (05.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 35 · K4 45 · K5 40 · Gesamttest 30 = 240 min
body = (oben + k0 + k1
        + k2 + k3
        + k4 + k5
        + gt + unten)
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
