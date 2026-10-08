"""Baut leitprogramme/trigonometrische-gleichungen.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/trigonometrische-gleichungen/seite.py

Leitprogramm zum Teilgebiet GF 5.5 Trigonometrische Gleichungen (Themenseite
g5-5-trigonometrische-gleichungen.html). Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden
Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf kommt das
Gerüst aus leitprogramme/einheitskreis.html (Grundlagenfach, Kapitelmuster, Kreisbild), mit eigenem
Titel und eigenen localStorage-Schlüsseln. Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei.
Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
NAME = 'Trigonometrische Gleichungen'
DATEI = 'trigonometrische-gleichungen'
ZIEL = R + 'leitprogramme/' + DATEI + '.html'
BESCHREIBUNG = ('Leitprogramm zu den trigonometrischen Gleichungen nach RLP GF 5.5: sin φ = c, cos φ = c und '
                'tan φ = c am Einheitskreis sehen, mit der Arkusfunktion und der Symmetrie lösen, alle Lösungen mit '
                'der Periode angeben — mit Clips, Simulationen, Übungen mit Rückmeldung und Gesamttest.')

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/einheitskreis.html').read()
    alt = alt.replace('<title>Leitprogramm Einheitskreis</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-einheitskreis-', 'lp-' + DATEI + '-')

# Kopfblock für Suchmaschinen: noch unverlinkt (HOWTO-leitprogramme §13, §15). build-seo.py ersetzt ihn,
# sobald die Seite in SEITEN steht — mit noindex=True, bis sie freigeschaltet ist.
SEO = ('<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
       '<meta name="description" content="' + html.escape(BESCHREIBUNG) + '">\n'
       '<meta name="robots" content="noindex, nofollow">\n'
       '<meta name="author" content="Raphael Arnold Kohler">\n'
       '<link rel="canonical" href="https://mathe.begreifbar.ch/leitprogramme/' + DATEI + '.html">\n'
       '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n'
       '<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">\n'
       '<link rel="apple-touch-icon" href="../apple-touch-icon.png">\n'
       '<!-- SEO:ENDE -->')
a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
if DATEI + '.html' not in alt[a:b]:                            # nur das Gerüst des Vorbilds ersetzen
    alt = alt[:a] + SEO + alt[b:]

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Einheitskreis', '\n/* ════════ Trigonometrische Gleichungen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Einheitskreis —'),
                    alt.find('<script>\n/* Leitprogramm Trigonometrische Gleichungen —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Einheitskreis', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 8. Oktober 2026', fuss)

CSS = '''
/* ════════ Trigonometrische Gleichungen (08.10.2026) — Kapitelmuster wie die anderen Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Festhalten, PDF-Weg) wie dort; Kreisbild wie im LP Einheitskreis.
   Eigen: die Gerade y = c bzw. x = c mit ihren Schnittpunkten, der Probepunkt P, das Kurvenbild in
   Kapitel 4. Farben: Sinus blau, Cosinus grün, Tangens orange, Gegenbeispiel rot, Tinte neutral. */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:360px}
.sim-breit{max-width:820px;margin:10px auto 6px}
/* Kindselektor: «.sim-breit svg» traf auch die Formeln, die MathJax in die Aufgabenleiste setzt (Prüfung 08.10.2026, H2) */
.sim-breit .kurven-rahmen > svg{display:block;width:100%;max-width:820px;margin:0 auto}
/* Kurvenbild auf dem Handy: nicht kleiner als 560 px, dafür im Rahmen seitlich verschiebbar; der Rahmen folgt
   den markierten Lösungen (seite.js, folgen), der Hinweis steht nur, wo verschoben werden kann */
.kurven-rahmen{overflow-x:auto;-webkit-overflow-scrolling:touch}
.kurven-hinweis{display:none;font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);text-align:center;margin:2px 0 6px}
@media(max-width:620px){.kurven-rahmen > svg{min-width:560px}.kurven-hinweis{display:block}}
/* Winkelregler über die ganze Breite: genug Pixel für ganze Grad (Prüfung 08.10.2026, H1) */
.sl-row:has(.sl-weit){flex-wrap:wrap}
.sl-grp.sl-weit{flex:1 1 100%;display:flex;align-items:center;gap:10px}
.sl-grp.sl-weit input[type=range]{flex:1;min-width:0;width:auto}
@media(max-width:620px){.sl-grp.sl-weit{flex-wrap:wrap;gap:2px 10px}.sl-grp.sl-weit label{flex:1 1 100%}}
#sim3 > svg{max-width:300px}
.sim .skala,svg.kv-mini .skala{stroke:var(--karte);stroke-width:3px;paint-order:stroke}
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
.sim .pfeil,svg.ek-mini .pfeil,svg.kv-mini .pfeil{fill:var(--tinte-2)}
.achsname{fill:var(--tinte);font-family:var(--serif);font-style:italic;font-size:12px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
svg.ek-mini .achsname,svg.kv-mini .achsname{font-size:10px;stroke-width:3px}
text.p-text{stroke:var(--karte);stroke-width:4px;paint-order:stroke;font-family:var(--serif);font-style:italic;font-size:13px;fill:var(--tinte)}
.sim-wahl{display:flex;flex-wrap:wrap;gap:6px 14px;justify-content:center;font-family:var(--sans);font-size:.86rem;margin:4px 0 10px}
.sim-wahl label{display:inline-flex;gap:5px;align-items:center;cursor:pointer;white-space:nowrap}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input.breit{width:min(16em,100%)}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sl-grp.gesperrt{opacity:.55}
.festhalten .merk ul{padding-left:1.3em;margin:6px 0 10px}
.festhalten .merk li{margin:3px 0}
.sim-formel{line-height:1.6;font-family:var(--sans);font-size:.9rem;text-align:center}
.nb{white-space:nowrap}
/* Kreisbild: Kreis, Radius und Gerade y = c in Tinte; Sinus blau, Cosinus grün, Tangens orange. */
.sim .einheitskreis,svg.ek-mini .einheitskreis{fill:none;stroke:var(--tinte-2);stroke-width:1.4}
svg.ek-mini .gitter,svg.kv-mini .gitter{stroke:var(--linie);stroke-width:.5}
svg.ek-mini .achse,svg.kv-mini .achse{stroke:var(--tinte-2);stroke-width:1}
svg.ek-mini .skala,svg.kv-mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:8px}
.sim .radius,svg.ek-mini .radius{stroke:var(--tinte);stroke-width:1.4}
.sim .radius.gestr{stroke-dasharray:4 3;stroke:var(--tinte-2)}
.sim .koord,svg.ek-mini .koord{stroke-width:3.4;stroke-linecap:round}
.koord.blau{stroke:var(--blau)} .koord.gruen{stroke:var(--gruen)} .koord.orange{stroke:var(--orange)}
.sim .winkelbogen{fill:none;stroke:var(--tinte);stroke-width:1.4}
.sim .tangente,svg.ek-mini .tangente{stroke:var(--tinte-2);stroke-width:1.3}
.sim .strahl,svg.ek-mini .strahl{stroke:var(--orange);stroke-width:1.3;stroke-dasharray:5 4}
.sim .waagrechte,svg.ek-mini .waagrechte,svg.kv-mini .waagrechte{stroke:var(--tinte);stroke-width:1.3;stroke-dasharray:6 4}
.sim .band{fill:none;stroke-width:9;opacity:.22;stroke-linecap:butt}
.band.blau{stroke:var(--blau)} .band.gruen{stroke:var(--gruen)} .band.orange{stroke:var(--orange)}
.sim .kurve,svg.kv-mini .kurve{fill:none;stroke-width:2.2}
.kurve.blau{stroke:var(--blau)} .kurve.gruen{stroke:var(--gruen)} .kurve.orange{stroke:var(--orange)}
.sim .pol,svg.kv-mini .pol{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:3 4}
.p-pkt{fill:var(--tinte)} .p-klein{fill:var(--tinte-2)}
.p-lauf{fill:var(--blau)} .p-lauf.blau{fill:var(--blau)} .p-lauf.gruen{fill:var(--gruen)} .p-lauf.orange{fill:var(--orange)}
.p-hohl{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.6}
.p-ziel{fill:none;stroke:var(--tinte-2);stroke-width:5;opacity:.45}
text.p-lauf.blau{fill:var(--blau)} text.p-lauf.gruen{fill:var(--gruen)} text.p-lauf.orange{fill:var(--orange)} text.p-pkt{fill:var(--tinte)}
svg.ek-mini{display:block;width:100%;max-width:220px;margin:6px 0;background:var(--karte);border:1px solid var(--linie);border-radius:8px}
svg.kv-mini{display:block;width:100%;max-width:440px;margin:6px 0;background:var(--karte);border:1px solid var(--linie);border-radius:8px}
svg.ek-mini text.p-text,svg.kv-mini text.p-text{font-size:11px}
.festhalten table.vz{border-collapse:collapse;font-family:var(--sans);font-size:.88rem;margin:6px 0 10px}
.festhalten table.vz td,.festhalten table.vz th{border:1px solid var(--blau-rand);padding:3px 9px;text-align:center}
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


def uebung(typ, titel):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(sim, p, label, mn, mx, st, val, akz='grau', einheit='', weit=False):
    return (f'<div class="sl-grp akz-{akz}{" sl-weit" if weit else ""}"><label for="{sim}-{p}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>')


def wahl(name, label, optionen):
    """Auswahlknöpfe in der Simulation; der erste ist der Startzustand (die Leiste setzt zurück)."""
    knoepfe = ''.join(f'<label><input type="radio" name="{name}" value="{w}"{" checked" if k == 0 else ""}> {t}</label>'
                      for k, (w, t) in enumerate(optionen))
    return f'<div class="sim-wahl" role="radiogroup" aria-label="{label}">{knoepfe}</div>'


def sim(nr, label, unten, klasse='sim-gross'):
    return f'''      <figure class="sim {klasse}" id="sim{nr}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        {'<div class="kurven-rahmen">' if klasse == 'sim-breit' else ''}<svg role="img" aria-label="{label}"></svg>{'</div>' if klasse == 'sim-breit' else ''}{'<p class="kurven-hinweis">Das Bild lässt sich seitlich verschieben; es folgt den markierten Lösungen.</p>' if klasse == 'sim-breit' else ''}
        {unten}
      </figure>'''


def ek(d, label):
    """Kreisbild zu einer Aufgabe; d wie in seite.js («Kreis- und Kurvenbilder zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="ek-mini" aria-label="{label}" '
            f'data-ek="{html.escape(json.dumps(d, ensure_ascii=False), quote=True)}"></svg></div>')


def kv(d, label):
    return (f'\n            <div class="mini-reihe"><svg class="kv-mini" aria-label="{label}" '
            f'data-kv="{html.escape(json.dumps(d, ensure_ascii=False), quote=True)}"></svg></div>')


def test(tid, titel, punkte, aufgaben, zwei=False):
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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim_, clip2, festhalten, uebungen, aufgaben, mehr, hm):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 5.5 · K1 · {hm}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim_}

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


TS = '../grundlagen/g5-5-trigonometrische-gleichungen.html'

# ------------------------------------------------------------------ Kapitel 1
sim1 = sim(1, 'Einheitskreis mit der Geraden y = c (Sinus) oder x = c (Cosinus) und ihren Schnittpunkten mit dem Kreis',
           wahl('s1-fn', 'Gleichung', [('sin', 'sin φ = c'), ('cos', 'cos φ = c')])
           + '\n        <div class="sl-row">\n          ' + regler('s1', 'c', 'Wert c', -1.5, 1.5, 0.05, 0.5) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Gleichung am Einheitskreis</div>
          <p>Eine <b>elementare trigonometrische Gleichung</b> hat eine der Formen \(\sin\varphi = c\), \(\cos\varphi = c\), \(\tan\varphi = c\) mit einer gegebenen Zahl \(c\). Gesucht sind die Winkel \(\varphi\).</p>
          <p>Am Einheitskreis ist \(\sin\varphi\) die <b>Höhe</b> (\(y\)-Koordinate) und \(\cos\varphi\) die <b>waagrechte Koordinate</b> (\(x\)-Koordinate) des Punktes \(P\). Darum:</p>
          <ul>
            <li>\(\sin\varphi = c\): Zeichne die <b>Waagrechte</b> \(y = c\).</li>
            <li>\(\cos\varphi = c\): Zeichne die <b>Senkrechte</b> \(x = c\).</li>
          </ul>
          <p>Ihre Schnittpunkte mit dem Kreis sind die Lösungen. Im Intervall \([0^\circ;\, 360^\circ[\) sind es <b>zwei</b> für \(-1 \lt c \lt 1\), <b>eine</b> für \(c = \pm 1\) (die Gerade berührt den Kreis) und <b>keine</b> für \(c \lt -1\) oder \(c \gt 1\): dann ist \(\mathbb{L} = \{\,\}\).</p>
          <p>Die beiden Punkte sind Spiegelbilder: beim Sinus an der \(y\)-Achse (gleiche Höhe), beim Cosinus an der \(x\)-Achse (gleiche \(x\)-Koordinate).</p>
          <p><b>Besondere Werte</b> ohne Taschenrechner (LP Einheitskreis): \(\sin 30^\circ = \tfrac{1}{2}\), \(\sin 45^\circ = \tfrac{\sqrt{2}}{2}\), \(\sin 60^\circ = \tfrac{\sqrt{3}}{2}\); beim Cosinus dieselben Zahlen in umgekehrter Reihenfolge. Beispiele aus dem Clip: \(\sin\varphi = \tfrac{1}{2}\): \(\mathbb{L} = \{30^\circ;\ 150^\circ\}\); \(\cos\varphi = -\tfrac{1}{2}\): \(\mathbb{L} = \{120^\circ;\ 240^\circ\}\).</p>
          <p>Die Lösungen stehen in der Lösungsmenge \(\mathbb{L}\) <b>aufsteigend</b>, mit Strichpunkt getrennt.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beim Cosinus eine Waagrechte zeichnen: \(\cos\varphi\) ist die \(x\)-Koordinate, die Gerade steht senkrecht.</p>
          <p>Bei \(c = \pm 1\) zwei Lösungen angeben: Die Gerade berührt den Kreis nur. Bei \(\cos\varphi = 1\) ist es nur \(0^\circ\); \(360^\circ\) gehört nicht mehr zu \([0^\circ;\, 360^\circ[\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 2, r'Zeichne in einen Einheitskreis die Gerade, deren Schnittpunkte die Lösungen von \(\sin\varphi = 0.8\) sind, und markiere die Lösungspunkte. In welchen Quadranten liegen sie?',
     r'<p>Die Waagrechte \(y = 0.8\) schneidet den Kreis rechts und links der \(y\)-Achse: Die Lösungen liegen im I. und im II. Quadranten (mit dem Rechner: \(\approx 53.1^\circ\) und \(\approx 126.9^\circ\)).</p>'
     + ek({'p': [53.1301, 126.8699], 'h': 0.8, 'farbe': 'blau'}, 'Einheitskreis mit der Waagrechten y = 0.8 und zwei Lösungspunkten im ersten und zweiten Quadranten'), ''),
    ('1b', 2, r'Ebenso für \(\cos\varphi = -0.3\): Gerade zeichnen, Lösungspunkte markieren, Quadranten angeben.',
     r'<p>Die Senkrechte \(x = -0.3\) schneidet den Kreis über und unter der \(x\)-Achse: Die Lösungen liegen im II. und im III. Quadranten (mit dem Rechner: \(\approx 107.5^\circ\) und \(\approx 252.5^\circ\)).</p>'
     + ek({'p': [107.4576, 252.5424], 'v': -0.3, 'farbe': 'gruen'}, 'Einheitskreis mit der Senkrechten x = −0.3 und zwei Lösungspunkten im zweiten und dritten Quadranten'), ''),
    ('1c', 3, r'Löse ohne Taschenrechner im Intervall \([0^\circ;\, 360^\circ[\): (a) \(\sin\varphi = \tfrac{\sqrt{3}}{2}\) (b) \(\cos\varphi = 0\) (c) \(\cos\varphi = -\tfrac{\sqrt{2}}{2}\)',
     r'<p>(a) \(\sin 60^\circ = \tfrac{\sqrt{3}}{2}\); Spiegelbild an der \(y\)-Achse: \(180^\circ - 60^\circ = 120^\circ\). \(\mathbb{L} = \{60^\circ;\ 120^\circ\}\).<br>(b) Die Senkrechte \(x = 0\) ist die \(y\)-Achse; sie trifft den Kreis oben und unten. \(\mathbb{L} = \{90^\circ;\ 270^\circ\}\).<br>(c) \(\cos 45^\circ = \tfrac{\sqrt{2}}{2}\); \(-\tfrac{\sqrt{2}}{2}\) links der \(y\)-Achse: \(180^\circ - 45^\circ = 135^\circ\), Spiegelbild an der \(x\)-Achse: \(360^\circ - 135^\circ = 225^\circ\). \(\mathbb{L} = \{135^\circ;\ 225^\circ\}\).</p>', ''),
    ('1d', 2, r'Wie viele Lösungen haben die Gleichungen im Intervall \([0^\circ;\, 360^\circ[\)? (a) \(\sin\varphi = -1\) (b) \(\cos\varphi = 1.01\) (c) \(\sin\varphi = 0\) (d) \(\cos\varphi = -0.999\)',
     r'<p>(a) eine: Die Waagrechte \(y = -1\) berührt den Kreis unten, bei \(270^\circ\). (b) keine: \(1.01 \gt 1\), \(\mathbb{L} = \{\,\}\). (c) zwei: Die \(x\)-Achse trifft den Kreis bei \(0^\circ\) und \(180^\circ\). (d) zwei: \(-0.999\) liegt noch zwischen \(-1\) und \(1\); die Senkrechte schneidet den Kreis knapp rechts von \((-1 \mid 0)\) zweimal.</p>', ''),
    ('1e', 2, r'Warum hat \(\cos\varphi = c\) im Intervall \([0^\circ;\, 360^\circ[\) für \(-1 \lt c \lt 1\) genau zwei Lösungen, für \(c = 1\) aber nur eine?',
     r'<p>Die Senkrechte \(x = c\) mit \(-1 \lt c \lt 1\) schneidet den Kreis in zwei Punkten, einem über und einem unter der \(x\)-Achse. Bei \(c = 1\) berührt sie den Kreis nur in \((1 \mid 0)\) — das ist der Winkel \(0^\circ\) (oder \(360^\circ\), der nicht mehr zum Intervall gehört).</p>', ''),
])
k1 = kapitel(1, 'am-einheitskreis', 'Gleichungen am Einheitskreis', 40,
             r'Du übersetzt \(\sin\varphi = c\) in eine Waagrechte und \(\cos\varphi = c\) in eine Senkrechte, liest am Einheitskreis ab, ob es zwei, eine oder keine Lösung gibt, und gibst die Lösungen für besondere Werte exakt an — ohne Taschenrechner.',
             ('g5-5-lp-einheitskreis', 'Gleichungen am Einheitskreis'),
             sim1, ('g5-5-lp-kontrolle-einheitskreis', 'Kontrollfragen am Einheitskreis'),
             fest1, [uebung('anzahl', 'Wie viele Lösungen?'), uebung('spezial', 'Besondere Werte, ohne Rechner')],
             auf1, f'<a href="{TS}#visualisierung">Themenseite 5.5, Visualisierung am Einheitskreis</a> und <a href="{TS}#spezial">Spezialfälle ohne Taschenrechner</a>',
             'besondere Werte ohne Taschenrechner')

# ------------------------------------------------------------------ Kapitel 2
sim2 = sim(2, 'Einheitskreis mit der Geraden zum Wert c, dem Punkt des Rechners und einem Punkt P zum eingestellten Winkel',
           wahl('s2-fn', 'Gleichung', [('sin', 'sin φ = c'), ('cos', 'cos φ = c')])
           + '\n        <div class="sl-row">\n          ' + regler('s2', 'c', 'Wert c', -1, 1, 0.05, 0.4)
           + '\n          ' + regler('s2', 'phi', 'Winkel von P', 0, 360, 1, 0, 'grau', '°', True) + '\n        </div>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Mit der Arkusfunktion lösen</div>
          <p>Für einen beliebigen Wert \(c\) liefert der Taschenrechner (Modus Grad, DEG) mit der <b>Arkusfunktion</b> einen Winkel, den <b>Hauptwert</b> \(\varphi_1\). Auf dem Rechner heisst \(\arcsin\) \(\sin^{-1}\), \(\arccos\) \(\cos^{-1}\).</p>
          <ul>
            <li>\(\varphi_1 = \arcsin(c)\) liegt in \([-90^\circ;\, 90^\circ]\) — rechte Kreishälfte.</li>
            <li>\(\varphi_1 = \arccos(c)\) liegt in \([0^\circ;\, 180^\circ]\) — obere Kreishälfte.</li>
          </ul>
          <p>Die <b>zweite Lösung</b> liefert der Rechner nie. Sie kommt aus der Spiegelung:</p>
          <p>\[ \sin\varphi = c:\ \ \varphi_2 = 180^\circ - \varphi_1 \qquad \cos\varphi = c:\ \ \varphi_2 = 360^\circ - \varphi_1 \]</p>
          <p>Ist \(\varphi_1\) negativ, bringt \(+\,360^\circ\) den Winkel ins Intervall \([0^\circ;\, 360^\circ[\) — es ist derselbe Punkt.</p>
          <p>Beispiel aus dem Clip: \(\sin\varphi = -0.4\). Rechner: \(\varphi_1 \approx -23.6^\circ\), also \(-23.6^\circ + 360^\circ = 336.4^\circ\); zweite Lösung \(180^\circ - (-23.6^\circ) = 203.6^\circ\). \(\mathbb{L} = \{203.6^\circ;\ 336.4^\circ\}\), auf \(0.1^\circ\) gerundet.</p>
          <p><b>Probe am Kreis:</b> Liegt jeder Lösungspunkt auf der richtigen Seite der Achse? Beim Sinus zählt die Seite der \(x\)-Achse, beim Cosinus die der \(y\)-Achse.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur den Wert des Rechners angeben — im Intervall \([0^\circ;\, 360^\circ[\) gibt es fast immer zwei Lösungen.</p>
          <p>Die Regeln vertauschen: \(180^\circ - \varphi_1\) gehört zum Sinus, \(360^\circ - \varphi_1\) zum Cosinus. Die Probe am Kreis deckt es auf.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Löse \(\sin\varphi = 0.7\) im Intervall \([0^\circ;\, 360^\circ[\) (Taschenrechner, auf \(0.1^\circ\)). Mach die Probe am Einheitskreis.',
     r'<p>\(\varphi_1 = \arcsin(0.7) \approx 44.4^\circ\); \(\varphi_2 = 180^\circ - 44.4^\circ = 135.6^\circ\). \(\mathbb{L} = \{44.4^\circ;\ 135.6^\circ\}\). Probe: Beide Punkte liegen über der \(x\)-Achse, der Sinus ist positiv ✓.</p>', ''),
    ('2b', 3, r'Löse \(\cos\varphi = -0.2\) im Intervall \([0^\circ;\, 360^\circ[\) (Taschenrechner, auf \(0.1^\circ\)). Mach die Probe am Einheitskreis.',
     r'<p>\(\varphi_1 = \arccos(-0.2) \approx 101.5^\circ\); \(\varphi_2 = 360^\circ - 101.5^\circ = 258.5^\circ\). \(\mathbb{L} = \{101.5^\circ;\ 258.5^\circ\}\). Probe: Beide Punkte liegen links der \(y\)-Achse, der Cosinus ist negativ ✓.</p>', ''),
    ('2c', 2, r'Der Rechner zeigt für \(\sin\varphi = -0.45\) den Wert \(\sin^{-1}(-0.45) \approx -26.7^\circ\). Zeichne beide Lösungspunkte in einen Einheitskreis und gib \(\mathbb{L}\) im Intervall \([0^\circ;\, 360^\circ[\) an.',
     r'<p>\(-26.7^\circ + 360^\circ = 333.3^\circ\) und \(180^\circ - (-26.7^\circ) = 206.7^\circ\). \(\mathbb{L} = \{206.7^\circ;\ 333.3^\circ\}\) — beide unter der \(x\)-Achse.</p>'
     + ek({'p': [206.7436, 333.2564], 'h': -0.45, 'farbe': 'blau', 'namen': ['206.7°', '333.3°'], 'fenster': [-1.9, 1.9, -1.4, 1.4]}, 'Einheitskreis mit der Waagrechten y = −0.45 und den Lösungspunkten bei 206.7 und 333.3 Grad'), ''),
    ('2d', 2, r'Ana löst \(\sin\varphi = 0.3\): «\(\varphi_1 \approx 17.5^\circ\), \(\varphi_2 = 360^\circ - 17.5^\circ = 342.5^\circ\).» Was ist falsch? Gib die richtige zweite Lösung an.',
     r'<p>Ana hat die Regel des Cosinus benutzt. Bei \(342.5^\circ\) liegt \(P\) unter der \(x\)-Achse, dort ist der Sinus negativ (\(\sin 342.5^\circ \approx -0.30\)). Richtig ist die Spiegelung an der \(y\)-Achse: \(\varphi_2 = 180^\circ - 17.5^\circ = 162.5^\circ\).</p>', ''),
    ('2e', 2, r'Warum gilt beim Sinus \(\varphi_2 = 180^\circ - \varphi_1\), beim Cosinus aber \(\varphi_2 = 360^\circ - \varphi_1\)? Begründe am Einheitskreis.',
     r'<p>Beim Sinus haben beide Punkte dieselbe Höhe: Der zweite ist das Spiegelbild des ersten an der \(y\)-Achse, und die Spiegelung an der \(y\)-Achse macht aus dem Winkel \(\varphi_1\) den Winkel \(180^\circ - \varphi_1\). Beim Cosinus haben beide dieselbe \(x\)-Koordinate: Spiegelung an der \(x\)-Achse, aus \(\varphi_1\) wird \(-\varphi_1\), im Intervall also \(360^\circ - \varphi_1\).</p>', ''),
])
k2 = kapitel(2, 'arkusfunktion', 'Mit der Arkusfunktion: die zweite Lösung', 40,
             r'Du bestimmst bei \(\sin\varphi = c\) und \(\cos\varphi = c\) mit dem Taschenrechner den Hauptwert, findest über die Spiegelung am Einheitskreis die zweite Lösung, bringst negative Winkel ins Intervall \([0^\circ;\, 360^\circ[\) und prüfst das Ergebnis am Kreis.',
             ('g5-5-lp-arkus', 'Mit der Arkusfunktion'),
             sim2, ('g5-5-lp-kontrolle-arkus', 'Kontrollfragen zur Arkusfunktion'),
             fest2, [uebung('quadranten', 'In welchen Quadranten?'), uebung('zweite', 'Die zweite Lösung')],
             auf2, f'<a href="{TS}#schemata">Themenseite 5.5, Lösungsschemata</a> und <a href="{TS}#kopplung">Kreis und Kurve nebeneinander</a>',
             'Taschenrechner erlaubt')

# ------------------------------------------------------------------ Kapitel 3
sim3 = sim(3, 'Einheitskreis mit der Tangente x = 1, dem Punkt S(1 | c), der Geraden durch O und S, dem Punkt des Rechners und einem Punkt P',
           '<div class="sl-row">\n          ' + regler('s3', 'c', 'Wert c', -2.4, 2.4, 0.1, 1)
           + '\n          ' + regler('s3', 'phi', 'Winkel von P', 0, 360, 1, 0, 'grau', '°', True) + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Tangensgleichungen</div>
          <p>Am Einheitskreis ist \(\tan\varphi\) die Höhe des Punktes \(S(1 \mid \tan\varphi)\) auf der Tangente \(x = 1\) (LP Einheitskreis). \(\tan\varphi = c\) heisst also: \(S(1 \mid c)\). Die <b>Gerade durch \(O\) und \(S\)</b> trifft den Kreis in zwei Punkten, die sich am Ursprung gegenüberliegen — für <b>jedes</b> \(c\). Eine Tangensgleichung ist immer lösbar.</p>
          <p>Der Rechner liefert \(\varphi_1 = \arctan(c)\) (auf dem Rechner \(\tan^{-1}\)) aus \(]{-90^\circ};\, 90^\circ[\), rechte Kreishälfte. Die zweite Lösung liegt gegenüber:</p>
          <p>\[ \tan\varphi = c:\ \ \varphi_2 = \varphi_1 + 180^\circ \]</p>
          <p>Ist \(\varphi_1\) negativ, liegen die Lösungen in \([0^\circ;\, 360^\circ[\) bei \(\varphi_1 + 180^\circ\) und \(\varphi_1 + 360^\circ\). Beispiel aus dem Clip: \(\tan\varphi = -1\): \(-45^\circ + 180^\circ = 135^\circ\) und \(-45^\circ + 360^\circ = 315^\circ\), \(\mathbb{L} = \{135^\circ;\ 315^\circ\}\).</p>
          <p>Besondere Werte: \(\tan 0^\circ = 0\), \(\tan 30^\circ = \tfrac{\sqrt{3}}{3}\), \(\tan 45^\circ = 1\), \(\tan 60^\circ = \sqrt{3}\). Bei \(90^\circ\) und \(270^\circ\) ist der Tangens nicht definiert.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Regel des Sinus oder des Cosinus nehmen (\(180^\circ - \varphi_1\), \(360^\circ - \varphi_1\)): Beim Tangens liegen die beiden Punkte nicht gespiegelt, sondern <em>gegenüber</em>.</p>
          <p>Den negativen Wert des Rechners in die Lösungsmenge schreiben: \(-45^\circ\) liegt nicht in \([0^\circ;\, 360^\circ[\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Löse \(\tan\varphi = 1.2\) im Intervall \([0^\circ;\, 360^\circ[\) (Taschenrechner, auf \(0.1^\circ\)).',
     r'<p>\(\varphi_1 = \arctan(1.2) \approx 50.2^\circ\); \(\varphi_2 = 50.2^\circ + 180^\circ = 230.2^\circ\). \(\mathbb{L} = \{50.2^\circ;\ 230.2^\circ\}\).</p>', ''),
    ('3b', 3, r'Löse \(\tan\varphi = -3.2\) im Intervall \([0^\circ;\, 360^\circ[\) (Taschenrechner, auf \(0.1^\circ\)).',
     r'<p>\(\arctan(-3.2) \approx -72.6^\circ\) liegt nicht im Intervall. \(-72.6^\circ + 180^\circ = 107.4^\circ\) und \(-72.6^\circ + 360^\circ = 287.4^\circ\). \(\mathbb{L} = \{107.4^\circ;\ 287.4^\circ\}\).</p>', ''),
    ('3c', 2, r'Löse ohne Taschenrechner im Intervall \([0^\circ;\, 360^\circ[\): (a) \(\tan\varphi = \tfrac{\sqrt{3}}{3}\) (b) \(\tan\varphi = 0\)',
     r'<p>(a) \(\tan 30^\circ = \tfrac{\sqrt{3}}{3}\): \(\mathbb{L} = \{30^\circ;\ 210^\circ\}\). (b) \(S(1 \mid 0)\), die Gerade ist die \(x\)-Achse: \(\mathbb{L} = \{0^\circ;\ 180^\circ\}\).</p>', ''),
    ('3d', 2, r'Zeichne für \(\tan\varphi = -0.5\) in einen Einheitskreis die Tangente \(x = 1\), den Punkt \(S\), die Gerade durch \(O\) und \(S\) und die beiden Lösungspunkte. Gib die Lösungen in \([0^\circ;\, 360^\circ[\) an (Taschenrechner).',
     r'<p>\(S(1 \mid -0.5)\). Die Gerade durch \(O\) und \(S\) trifft den Kreis im II. und IV. Quadranten. \(\arctan(-0.5) \approx -26.6^\circ\): \(\mathbb{L} = \{153.4^\circ;\ 333.4^\circ\}\).</p>'
     + ek({'p': [153.4349, 333.4349], 'tan': -0.5, 'farbe': 'orange', 'fenster': [-1.9, 1.9, -1.4, 1.4], 'breite': 240,
           'namen': ['153.4°', '333.4°'], 'lagen': [None, [-6, 15, 'end']]}, 'Einheitskreis mit Tangente, S(1 | −0.5) und den Lösungspunkten bei 153.4 und 333.4 Grad'), ''),
    ('3e', 2, r'Warum hat \(\tan\varphi = c\) für jedes \(c\) zwei Lösungen in \([0^\circ;\, 360^\circ[\), und warum liegen sie genau \(180^\circ\) auseinander?',
     r'<p>Zu jedem \(c\) gibt es auf der Tangente \(x = 1\) den Punkt \(S(1 \mid c)\), und die Gerade durch \(O\) und \(S\) geht durch den Mittelpunkt des Kreises — sie trifft ihn immer in zwei Punkten. Diese liegen sich am Ursprung gegenüber; von einem zum anderen ist es eine halbe Drehung, also \(180^\circ\).</p>', ''),
])
k3 = kapitel(3, 'tangens', 'Tangensgleichungen', 35,
             r'Du siehst \(\tan\varphi = c\) als Punkt \(S(1 \mid c)\) auf der Tangente, begründest, warum es für jedes \(c\) Lösungen gibt, und findest mit dem Hauptwert des Rechners beide Lösungen in \([0^\circ;\, 360^\circ[\) — sie liegen \(180^\circ\) auseinander.',
             ('g5-5-lp-tangens', 'Tangensgleichungen'),
             sim3, ('g5-5-lp-kontrolle-tangens', 'Kontrollfragen zum Tangens'),
             fest3, [uebung('tan-loesen', 'Mit dem Rechner'), uebung('tan-spezial', 'Besondere Werte, ohne Rechner')],
             auf3, f'<a href="{TS}#schemata">Themenseite 5.5, Lösungsschemata (Typ 3)</a>',
             'Taschenrechner erlaubt, 3c ohne')

# ------------------------------------------------------------------ Kapitel 4
sim4 = sim(4, 'Sinus-, Cosinus- oder Tangenskurve von −360 bis 720 Grad mit der Waagrechten y = c und den Lösungen; das Paar zum gewählten k ist hervorgehoben',
           wahl('s4-fn', 'Gleichung', [('sin', 'sin φ = c'), ('cos', 'cos φ = c'), ('tan', 'tan φ = c')])
           + '\n        <div class="sl-row">\n          ' + regler('s4', 'c', 'Wert c', -1.5, 1.5, 0.05, 0.5)
           + '\n          ' + regler('s4', 'k', 'k', -2, 3, 1, 0) + '\n        </div>', 'sim-breit')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Alle Lösungen und die Lösungsmenge</div>
          <p>Nach einer vollen Drehung liegt \(P\) wieder am selben Ort: Sinus und Cosinus haben die <b>Periode \(360^\circ\)</b>, der Tangens schon \(180^\circ\). Darum gehören zu jeder Lösung alle, die \(k\) Perioden daneben liegen (\(k \in \mathbb{Z}\), auch \(0\) und negativ).</p>
          <p><b>Alle Lösungen</b> (Beispiel aus dem Clip):</p>
          <p>\[ \sin\varphi = \tfrac{1}{2}:\quad \varphi = 30^\circ + k \cdot 360^\circ \ \ \text{oder}\ \ \varphi = 150^\circ + k \cdot 360^\circ,\ k \in \mathbb{Z} \]</p>
          <p>\[ \tan\varphi = 1:\quad \varphi = 45^\circ + k \cdot 180^\circ,\ k \in \mathbb{Z} \]</p>
          <p>Beim Tangens genügt eine Formel: \(180^\circ\) weiter liegt schon die zweite Lösung. Ebenso bei den Sonderfällen \(\sin\varphi = \pm 1\), \(\cos\varphi = \pm 1\) (eine Lösung je Periode) und <span class="nb">\(\sin\varphi = 0\): \(\varphi = k \cdot 180^\circ\);</span> <span class="nb">\(\cos\varphi = 0\): \(\varphi = 90^\circ + k \cdot 180^\circ\)</span>. Die Themenseite schreibt beim Cosinus kurz \(\varphi = \pm\varphi_1 + k \cdot 360^\circ\) — dasselbe, denn \(-\varphi_1 + 360^\circ = 360^\circ - \varphi_1\).</p>
          <p><b>Lösungen in einem Intervall:</b> In die allgemeine Lösung für \(k\) der Reihe nach ganze Zahlen einsetzen, nur die Werte im Intervall behalten und aufsteigend in \(\mathbb{L}\) schreiben: \(0^\circ \le \varphi \lt 720^\circ\): \(\mathbb{L} = \{30^\circ;\ 150^\circ;\ 390^\circ;\ 510^\circ\}\) (\(k = 0\) und \(k = 1\)).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beim Tangens \(+\,k \cdot 360^\circ\) schreiben: Dann fehlt jede zweite Lösung.</p>
          <p>Bei Sinus und Cosinus nur eine Grundlösung mit der Periode versehen: Die zweite Familie fehlt.</p>
          <p>Die rechte Grenze mitnehmen: In \([0^\circ;\, 720^\circ[\) gehört \(720^\circ\) nicht dazu.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Gib alle Lösungen von \(\sin\varphi = 0.25\) an (Taschenrechner, auf \(0.1^\circ\)).',
     r'<p>\(\varphi_1 = \arcsin(0.25) \approx 14.5^\circ\), \(\varphi_2 = 180^\circ - 14.5^\circ = 165.5^\circ\). Alle Lösungen: \(\varphi = 14.5^\circ + k \cdot 360^\circ\) oder \(\varphi = 165.5^\circ + k \cdot 360^\circ\), \(k \in \mathbb{Z}\).</p>', ''),
    ('4b', 3, r'Im Bild sind \(y = \cos\varphi\) und \(y = -0.9\) gezeichnet. Bestimme alle Lösungen von \(\cos\varphi = -0.9\) im Intervall \([0^\circ;\, 720^\circ[\) (Taschenrechner, auf \(0.1^\circ\)) und zeige sie am Bild.',
     r'<p>\(\arccos(-0.9) \approx 154.2^\circ\), \(360^\circ - 154.2^\circ = 205.8^\circ\); mit \(k = 1\): \(514.2^\circ\), \(565.8^\circ\). \(\mathbb{L} = \{154.2^\circ;\ 205.8^\circ;\ 514.2^\circ;\ 565.8^\circ\}\) — je zwei Schnittpunkte nahe den Tiefpunkten bei \(180^\circ\) und \(540^\circ\).</p>'
     + kv({'f': 'cos', 'c': -0.9, 'von': 0, 'bis': 720, 'punkte': [[154.1581, '154.2°'], [205.8419, '205.8°'], [514.1581, '514.2°'], [565.8419, '565.8°']]},
          'Cosinuskurve von 0 bis 720 Grad mit der Waagrechten y = −0.9 und vier Lösungspunkten'),
     kv({'f': 'cos', 'c': -0.9, 'von': 0, 'bis': 720}, 'Cosinuskurve von 0 bis 720 Grad mit der Waagrechten y = −0.9')),
    ('4c', 2, r'Bestimme alle Lösungen von \(\tan\varphi = 0.8\) im Intervall \([-180^\circ;\, 360^\circ[\) (Taschenrechner, auf \(0.1^\circ\)).',
     r'<p>\(\arctan(0.8) \approx 38.7^\circ\); alle Lösungen \(\varphi = 38.7^\circ + k \cdot 180^\circ\). Im Intervall: \(k = -1, 0, 1\). \(\mathbb{L} = \{-141.3^\circ;\ 38.7^\circ;\ 218.7^\circ\}\).</p>', ''),
    ('4d', 2, r'Gib ohne Taschenrechner alle Lösungen an: (a) \(\sin\varphi = -1\) (b) \(\cos\varphi = 1\)',
     r'<p>(a) Nur der tiefste Punkt des Kreises: \(\varphi = 270^\circ + k \cdot 360^\circ\), \(k \in \mathbb{Z}\). (b) Nur der Punkt \((1 \mid 0)\): \(\varphi = k \cdot 360^\circ\), \(k \in \mathbb{Z}\).</p>', ''),
    ('4e', 2, r'Warum genügt beim Tangens eine Formel \(\varphi = \varphi_1 + k \cdot 180^\circ\), während man beim Sinus in der Regel zwei braucht?',
     r'<p>Beim Tangens folgen die Lösungen in <b>gleichen</b> Abständen: Die zweite liegt \(180^\circ\) nach der ersten, die nächste wieder \(180^\circ\) weiter. Ein einziger Schritt \(+\,k \cdot 180^\circ\) trifft darum alle. Beim Sinus sind die Abstände <b>ungleich</b>: Bei \(\sin\varphi = \tfrac{1}{2}\) folgen \(30^\circ\), \(150^\circ\), \(390^\circ\), \(510^\circ\), also abwechselnd \(120^\circ\) und \(240^\circ\) weiter. Kein gleicher Schritt trifft alle — darum zwei Formeln mit je \(+\,k \cdot 360^\circ\). Nur bei \(c = 0\) (Abstand immer \(180^\circ\)) und bei \(c = \pm 1\) (eine Lösung je Runde) genügt eine.</p>', ''),
])
k4 = kapitel(4, 'loesungsmenge', 'Alle Lösungen: Periode und Lösungsmenge', 40,
             r'Du gibst alle Lösungen mit der Periode an (\(+\,k \cdot 360^\circ\) bei Sinus und Cosinus, \(+\,k \cdot 180^\circ\) beim Tangens, \(k \in \mathbb{Z}\)) und schreibst die Lösungsmenge in einem vorgegebenen Intervall auf.',
             ('g5-5-lp-loesungsmenge', 'Alle Lösungen und die Lösungsmenge'),
             sim4, ('g5-5-lp-kontrolle-loesungsmenge', 'Kontrollfragen zur Lösungsmenge'),
             fest4, [uebung('allgemein', 'Alle Lösungen mit k'), uebung('intervall', 'Lösungen im Intervall')],
             auf4, f'<a href="{TS}#loesungsmenge">Themenseite 5.5, Lösungsmenge angeben</a> und <a href="{TS}#kurve">Lösungen entlang der Sinus-Kurve</a>',
             'Taschenrechner erlaubt, 4d ohne')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 5.4</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Sinus und Cosinus als Koordinaten am Einheitskreis, der Tangens auf der Tangente, die besonderen Werte, die Umkehrtaste des Rechners und die Periode. Wenn das wackelt: Leitprogramm <a href="einheitskreis.html">Einheitskreis</a> (GF 5.4), besonders <a href="einheitskreis.html#besondere-winkel">Kapitel 2</a>, <a href="einheitskreis.html#tangens-pythagoras">Kapitel 3</a> (Tangens) und <a href="einheitskreis.html#periode-umkehr">Kapitel 5</a>.</p>
      ''' + clipkarte('g5-4-einheitskreis', 'Einheitskreis: Sinus und Cosinus als Koordinaten', '1:04') + '''
      ''' + clipkarte('g5-4-spezialwinkel', 'Einheitskreis: die Werte der Spezialwinkel', '0:58') + '''
''' + test('t0', 'Vortest', 12, [
    ('0a', 2, r'Gib die Koordinaten des Punktes \(P\) auf dem Einheitskreis zu \(\varphi = 150^\circ\) exakt an.',
     r'<p>\(P(\cos 150^\circ \mid \sin 150^\circ) = P\left(-\tfrac{\sqrt{3}}{2} \mid \tfrac{1}{2}\right)\).</p><p class="komm">II. Quadrant, Referenzwinkel \(30^\circ\) — LP Einheitskreis, Kapitel 2.</p>', ''),
    ('0b', 2, r'Gib ohne Taschenrechner exakt an: \(\sin 210^\circ\) und \(\cos 300^\circ\).',
     r'<p>\(\sin 210^\circ = -\tfrac{1}{2}\) (III. Quadrant, Referenzwinkel \(30^\circ\)); \(\cos 300^\circ = \tfrac{1}{2}\) (IV. Quadrant, Referenzwinkel \(60^\circ\)).</p><p class="komm">Die besonderen Werte braucht Kapitel 1 — der zweite Clip oben.</p>', ''),
    ('0c', 2, r'Berechne mit dem Taschenrechner (Modus DEG) auf \(0.1^\circ\): \(\sin^{-1}(0.6)\) und \(\cos^{-1}(-0.3)\).',
     r'<p>\(\sin^{-1}(0.6) \approx 36.9^\circ\); \(\cos^{-1}(-0.3) \approx 107.5^\circ\).</p><p class="komm">Zeigt der Rechner \(0.644\), steht er im Bogenmass (RAD).</p>', ''),
    ('0d', 2, r'Aus welchem Bereich stammen die Winkel, die der Rechner für \(\sin^{-1}\) und für \(\cos^{-1}\) liefert?',
     r'<p>\(\sin^{-1}\): aus \([-90^\circ;\, 90^\circ]\), rechte Kreishälfte. \(\cos^{-1}\): aus \([0^\circ;\, 180^\circ]\), obere Kreishälfte.</p><p class="komm">LP Einheitskreis, Kapitel 5 — darauf baut Kapitel 2 auf.</p>', ''),
    ('0e', 2, r'Ergänze mit einem Winkel zwischen \(0^\circ\) und \(360^\circ\): \(\sin 400^\circ = \sin\,\)? und \(\cos(-30^\circ) = \cos\,\)?',
     r'<p>\(\sin 400^\circ = \sin 40^\circ\) (\(400^\circ - 360^\circ\)); \(\cos(-30^\circ) = \cos 330^\circ\) (\(-30^\circ + 360^\circ\)).</p><p class="komm">Die Periode \(360^\circ\) — Kapitel 2 und 4 brauchen sie.</p>', ''),
    # Tangens-Vorwissen für Kapitel 3 (Prüfung 08.10.2026, M8): S(1 | tan φ) und die besonderen Werte √3/3, √3
    ('0f', 2, r'Gib ohne Taschenrechner exakt an: \(\tan 30^\circ\) und \(\tan 120^\circ\). Welcher Punkt auf der Tangente \(x = 1\) zeigt am Einheitskreis den Wert \(\tan 30^\circ\)?',
     r'<p>\(\tan 30^\circ = \tfrac{\sqrt{3}}{3}\); \(\tan 120^\circ = -\sqrt{3}\) (II. Quadrant, Referenzwinkel \(60^\circ\), der Tangens ist dort negativ). Die Gerade durch \(O\) und den Kreispunkt zu \(30^\circ\) trifft die Tangente \(x = 1\) in \(S\left(1 \mid \tfrac{\sqrt{3}}{3}\right)\): Seine Höhe ist \(\tan 30^\circ\).</p><p class="komm">LP Einheitskreis, <a href="einheitskreis.html#tangens-pythagoras">Kapitel 3</a> — darauf baut Kapitel 3 auf.</p>', ''),
]) + '''
      <p class="komm">Weniger als 8 von 12 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/' + DATEI + '/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.5 · Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Skizze am Einheitskreis und Rechenweg. Teil A ohne Taschenrechner (besondere Werte, exakt), Teil B mit Taschenrechner.<br>
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
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 1, 3, 4; G3 → 1, 3, 4; G4 → 2, 4; G5 → 2, 4; G6 → 3, 4; G7 → 2</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Trigonometrische Gleichungen, Version 1.0 (08.10.2026). Gebaut aus
     scripts/lp/trigonometrische-gleichungen/seite.py — Änderungen dort, nicht in dieser Datei.
     Verfahren: HOWTO-leitprogramme.md (Kapitelmuster).

     RLP-BM 2030, Grundlagenfach, Lerngebiet 5 Geometrie, Teilgebiet 5.5 Trigonometrische Gleichungen,
     wörtlich nach dem Lehrplan (Math-GL.pdf; die RLP-Box der Themenseite schreibt «Arcusfunktion»):
       K1  elementare trigonometrische Gleichungen am Einheitskreis visualisieren und mithilfe der
           Arkusfunktion lösen
     Kein Vermerk «ohne Hilfsmittel»: Taschenrechner erlaubt. Die besonderen Werte (Kapitel 1, Aufgabe 3c,
     4d, Gesamttest Teil A) werden trotzdem exakt und ohne Rechner verlangt — sie stammen aus GF 5.4, wo
     sie «auch ohne Hilfsmittel» gelten, und die Themenseite stellt sie so (A1, «Spezialfälle»).

     Kompetenzmatrix (Teil von K1 | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 visualisieren (Gerade y = c, x = c, S(1 | c); Anzahl Lösungen) | —             | 1, 3    | 1a, 1b, 1d, 1e, 2c, 3d, 3e | G1, G2
       K1 lösen, besondere Werte                                      | ohne TR       | 1, 3, 4 | 1c, 3c, 4d                 | G1, G3
       K1 lösen mit der Arkusfunktion, zweite Lösung                  | mit TR        | 2, 3    | 2a–2e, 3a, 3b              | G4, G5, G6, G7
       K1 alle Lösungen (Periode), Lösungsmenge im Intervall           | mit/ohne TR   | 4       | 4a–4e                      | G2, G3, G4, G5, G6
     Kein Kapitelziel ohne Kompetenz. Gesamttest: Teil A (G1–G3, 10 P) ohne, Teil B (G4–G7, 15 P) mit Rechner.

     Planung (Kapitel | Lernziel | Clips | Tüfteln | Beispiel | Häufiger Fehler | min):
       0 Vorwissen   | P(cos φ | sin φ), S(1 | tan φ), besondere Werte, sin⁻¹/cos⁻¹, Periode | g5-4-einheitskreis, g5-4-spezialwinkel | — | 150°, 210°, 300° | — | 10
       1 Am Kreis    | Waagrechte/Senkrechte, 2/1/0 Lösungen, besondere Werte exakt | lp-einheitskreis + Kontrolle | sim1 Gerade und Kreis | sin φ = 1/2, cos φ = −1/2 | Senkrechte statt Waagrechte; c = ±1 | 40
       2 Arkus       | Hauptwert, φ₂ = 180° − φ₁ bzw. 360° − φ₁, +360°, Probe | lp-arkus + Kontrolle | sim2 Rechnerpunkt und P | sin φ = 0.4, cos φ = −0.7, sin φ = −0.4 | Regeln vertauscht; nur ein Wert | 40
       3 Tangens     | S(1 | c), immer lösbar, φ₂ = φ₁ + 180° | lp-tangens + Kontrolle | sim3 Tangente und P | tan φ = 1, 2.5, −1 | Sinus-/Cosinusregel; negativer Wert | 35
       4 Lösungsmenge| + k · 360°, + k · 180°, k ∈ ℤ; Intervall, aufsteigend | lp-loesungsmenge + Kontrolle | sim4 Kurve mit Regler k | sin φ = 1/2 in [0°; 720°[ | tan mit 360°; Grenze | 40
       Gesamttest 30 — Summe 195 min ≈ vier Lektionen plus Gesamttest. Clips: 8 eigene, 10:32 min.

     Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.5): Gleichungen mit ersetztem Argument
     (Riesenrad A6 cos(90° · t) = 0, Gezeiten A7) — sie verlangen eine Substitution, die das Leitprogramm
     nicht übt (HOWTO §15: wer sin x = c übt, kann noch nicht sin(bx) = c); der Einstieg mit dem Riesenrad;
     das Bogenmass als Lösung (die Themenseite rechnet durchgehend in Grad); die Sinus- und Cosinuskurven als
     Funktionen (SP 3.5) — hier nur als Bild der Periode in Kapitel 4.

     Konventionen wie auf der Themenseite: Winkel φ in Grad (die Mini-Checks schreiben x); Grundgleichungen
     sin φ = c, cos φ = c, tan φ = c; Hauptwert φ₁ aus arcsin, arccos, arctan (Rechner sin⁻¹ …), zweite Lösung
     φ₂ = 180° − φ₁ (sin), 360° − φ₁ (cos), φ₁ + 180° (tan); alle Lösungen «φ = φ₁ + k · 360° oder
     φ = φ₂ + k · 360°, k ∈ ℤ» (Definitionsblock «Drei typische Aufgabenstellungen»); Lösungsmenge 𝕃
     aufsteigend; Intervalle [0°; 360°[. Tangens als S(1 | tan φ) auf x = 1 wie im LP Einheitskreis.
     Farben: Sinus blau, Cosinus grün, Tangens orange, rot = Gegenbeispiel, Tinte = neutral.

     Bewusst anders als die Themenseite:
       – Elemente einer Menge mit Strichpunkt (STYLEGUIDE §2.11), Themenseite mit Komma.
       – Gerundete Lösungsmengen «𝕃 = {23.6°; 156.4°}» mit dem Vermerk «auf 0.1° gerundet» statt «𝕃 ≈ {…}».
       – Cosinus: zweite Lösung als 360° − φ₁ (im Intervall); ±φ₁ + k · 360° einmal als gleichwertig genannt.

     Widersprüche in der Themenseite (gemeldet, nicht übernommen):
       – RLP-Box «mithilfe der Arcusfunktion lösen», der Lehrplan schreibt «Arkusfunktion»; die Box ist als
         wörtliches Zitat ausgewiesen.
       – Alle Lösungen in drei Schreibweisen: «φ = 30° + k · 360° oder …» (Definitionsblock), «𝕃 = {30° + k · 360°}
         ∪ {150° + k · 360°}» (Mini-Check), «30° + k · 360°; 150° + k · 360°» (Tabelle Spezialfälle).
       – Mengen mit Komma «{60°, 120°}», «{30°,\\ 150°}» und «𝕃 ≈ {…}» neben STYLEGUIDE §2.11 (Strichpunkt).
       – Hauptwertbereich des arctan als «(−90°; 90°)» statt «]−90°; 90°[» (HOWTO §10, LP Einheitskreis).
       – Tangens, Hinweis bei Typ 3 und «Häufiger Fehler»: «im Hauptintervall … den Taschenrechner-Wert φ₁ und
         φ₁ + 180°» — für negatives c liegt φ₁ nicht in [0°; 360°[ (tan φ = −1: 135° und 315°, nicht −45°).
       – Mini-Check «Lösungsmenge», Transfer: «Riesenrad: Die Gondelhöhe erfüllt sin x = 0.5» — im Einstieg ist
         die halbe Höhe die Höhe des Mittelpunkts, also der Wert 0, nicht 0.5.
       – «Lösungen im Bereich 0° ≤ φ ≤ 720°» (Definitionsblock, Punkt 3, rechts geschlossen) neben
         «0° ≤ φ < 720°» und [0°; 720°[ (A5). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Trigonometrische Gleichungen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.5</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Am Einheitskreis</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Arkusfunktion</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Tangens</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Lösungsmenge</span></a></li>
    </ol>
    <p class="lekt">Abschluss</p>
    <ol>
      <li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li>
    </ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 5 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Aufgaben in der Simulation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze am Einheitskreis, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.5 Trigonometrische Gleichungen:</p>
        <ul>
          <li><b>K1</b> elementare trigonometrische Gleichungen am Einheitskreis visualisieren und mithilfe der Arkusfunktion lösen — Kapitel 1–4, mit Taschenrechner; die besonderen Werte (aus GF 5.4) ohne</li>
        </ul>
        <p class="rlp-quelle">Auf der <a href="''' + TS + '''">Themenseite 5.5</a>, nicht hier: Gleichungen mit einem Term im Argument wie beim Riesenrad \\(\\cos(90^\\circ \\cdot t) = 0\\) und bei den Gezeiten.</p>
      </details>
    </div>
'''
unten = '''
    <div class="duo">
      <div>
        <h3 id="weiter">Weiter</h3>
        <p>Zum Nachschlagen: <a href="''' + TS + '''">Themenseite 5.5 Trigonometrische Gleichungen</a> — mit dem Riesenrad und den Gezeiten als Anwendungen. Im Schwerpunktfach geht es weiter mit den <a href="trigonometrische-funktionen.html">trigonometrischen Funktionen</a> (SP 3.5): Sinus und Cosinus als Kurven im Bogenmass, mit Parametern.</p>
      </div>
    </div>

    <div class="fuss">
      <span>Leitprogramm Trigonometrische Gleichungen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (08.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 35 · K4 40 · Gesamttest 30 = 195 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
