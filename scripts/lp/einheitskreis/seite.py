"""Baut leitprogramme/einheitskreis.html aus einer Kapitelbeschreibung (07.10.2026).

  python3 scripts/lp/einheitskreis/seite.py

Leitprogramm zum Teilgebiet GF 5.4 Einheitskreis (Themenseite g5-4-einheitskreis.html). Liest Kopf
(inkl. <style>) und Grundskript aus der bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js)
und schreibt die Seite neu. Beim ersten Lauf kommt das Gerüst aus leitprogramme/planimetrie.html
(Grundlagenfach, Kapitelmuster), mit eigenem Titel und eigenen localStorage-Schlüsseln. Wiederholbar:
zweimal laufen lassen ergibt dieselbe Datei. Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/einheitskreis.html'
NAME = 'Einheitskreis'
BESCHREIBUNG = ('Leitprogramm zum Einheitskreis nach RLP GF 5.4: Sinus und Cosinus als Koordinaten, besondere Winkel '
                'ohne Taschenrechner, Tangens und trigonometrischer Pythagoras, Symmetrien, Periode und '
                'Umkehroperationen — mit Clips, Simulationen am Einheitskreis, Übungen mit Rückmeldung und Gesamttest.')

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/planimetrie.html').read()
    alt = alt.replace('<title>Leitprogramm Planimetrie</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-planimetrie-', 'lp-einheitskreis-')

# Kopfblock für Suchmaschinen: noch unverlinkt (HOWTO-leitprogramme §13, §15). build-seo.py ersetzt ihn,
# sobald die Seite in SEITEN steht — mit noindex=True, bis sie freigeschaltet ist.
SEO = ('<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
       '<meta name="description" content="' + html.escape(BESCHREIBUNG) + '">\n'
       '<meta name="robots" content="noindex, nofollow">\n'
       '<meta name="author" content="Raphael Arnold Kohler">\n'
       '<link rel="canonical" href="https://mathe.begreifbar.ch/leitprogramme/einheitskreis.html">\n'
       '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n'
       '<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">\n'
       '<link rel="apple-touch-icon" href="../apple-touch-icon.png">\n'
       '<!-- SEO:ENDE -->')
# Nach der Freischaltung steht der volle Block von build-seo.py da (ohne robots, mit JSON-LD): nicht überschreiben.
if 'name="robots"' not in alt[:alt.index('<!-- SEO:ENDE -->')] and 'application/ld+json' not in alt[:alt.index('<!-- SEO:ENDE -->')]:
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = alt[:a] + SEO + alt[b:]

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Planimetrie', '\n/* ════════ Einheitskreis'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Planimetrie —'),
                    alt.find('<script>\n/* Leitprogramm Einheitskreis —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Planimetrie', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 8. Oktober 2026', fuss)

CSS = '''
/* ════════ Einheitskreis (07.10.2026) — Kapitelmuster wie die anderen Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Festhalten, PDF-Weg) wie dort. Eigen ist das Kreisbild: gleich geteilte
   Achsen, Einheitskreis, Punkt P mit seinen Koordinaten. Farben: Sinus blau, Cosinus grün, Tangens
   orange, Gegenbeispiel rot, Tinte neutral (Kreis, Radius, Winkel, Spiegelachsen). */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:360px}
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
.sim .pfeil,svg.ek-mini .pfeil{fill:var(--tinte-2)}
.achsname{fill:var(--tinte);font-family:var(--serif);font-style:italic;font-size:12px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
svg.ek-mini .achsname{font-size:10px;stroke-width:3px}
text.p-text{stroke:var(--karte);stroke-width:4px;paint-order:stroke;font-family:var(--serif);font-style:italic;font-size:13px;fill:var(--tinte)}
.hilfs-schalter,.sim-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
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
.sl-grp.akz-grau{--akz:var(--tinte-2)}
.sim-formel{line-height:1.6;font-family:var(--sans);font-size:.9rem;text-align:center}
.nb{white-space:nowrap}
/* Kreisbild: Kreis, Radius und Winkel in Tinte; Sinus blau, Cosinus grün, Tangens orange. */
.sim .einheitskreis,svg.ek-mini .einheitskreis{fill:none;stroke:var(--tinte-2);stroke-width:1.4}
svg.ek-mini .gitter{stroke:var(--linie);stroke-width:.5}
svg.ek-mini .achse{stroke:var(--tinte-2);stroke-width:1}
svg.ek-mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:8px}
.sim .radius,svg.ek-mini .radius{stroke:var(--tinte);stroke-width:1.6}
.sim .radius.gestr,svg.ek-mini .radius.gestr{stroke-dasharray:4 3;stroke:var(--tinte-2)}
.sim .koord,svg.ek-mini .koord{stroke-width:3.4;stroke-linecap:round}
.sim .koord.duenn{stroke-width:1.8}
.sim .koord.gestr{stroke-dasharray:5 4;stroke-width:2.6}
.koord.blau{stroke:var(--blau)} .koord.gruen{stroke:var(--gruen)} .koord.orange{stroke:var(--orange)}
.sim .dreieck{fill:var(--blau);fill-opacity:.1;stroke:none}
.sim .dreieck.orange{fill:var(--orange);fill-opacity:.12;stroke:var(--orange);stroke-width:.8;stroke-opacity:.6}
.sim .winkelbogen{fill:none;stroke:var(--tinte);stroke-width:1.4}
.sim .w-text{font-family:var(--serif);font-style:italic;font-size:12px;fill:var(--tinte)}
.sim .q-text{font-family:var(--sans);font-size:11px;font-weight:700;fill:var(--tinte-2);opacity:.75}
.sim .s-text{font-family:var(--sans);font-size:10px;fill:var(--tinte-2)} .sim .s-text.orange{fill:var(--orange)}
.sim .spiegel{stroke:var(--tinte-2);stroke-width:1.3;stroke-dasharray:4 3}
.sim .spiegelachse{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:7 5}
.sim .tangente,svg.ek-mini .tangente{stroke:var(--tinte-2);stroke-width:1.3}
.sim .strahl,svg.ek-mini .strahl{stroke:var(--tinte-2);stroke-width:1.2;stroke-dasharray:3 3}
.sim .waagrechte,svg.ek-mini .waagrechte{stroke:var(--tinte);stroke-width:1.3;stroke-dasharray:6 4}
.sim .band{fill:none;stroke-width:9;opacity:.22;stroke-linecap:butt}
.band.blau{stroke:var(--blau)} .band.gruen{stroke:var(--gruen)} .band.orange{stroke:var(--orange)}
.p-pkt{fill:var(--tinte)} .p-klein{fill:var(--tinte-2)}
.p-lauf{fill:var(--blau)} .p-lauf.gruen{fill:var(--gruen)} .p-lauf.orange{fill:var(--orange)} .p-lauf.b{fill:var(--orange)}
.p-hohl{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.6}
.p-ziel{fill:none;stroke:var(--tinte-2);stroke-width:5;opacity:.45}
text.p-lauf.orange,text.p-lauf.b{fill:var(--orange)} text.p-pkt{fill:var(--tinte)}
svg.ek-mini{display:block;width:100%;max-width:220px;margin:6px 0;background:var(--karte);border:1px solid var(--linie);border-radius:8px}
svg.ek-mini text.p-text{font-size:11px}
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


def regler(sim, p, label, mn, mx, st, val, akz='grau', einheit='°'):
    return (f'<div class="sl-grp akz-{akz}"><label for="{sim}-{p}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>')


def wahl(name, label, optionen):
    """Auswahlknöpfe in der Simulation; der erste ist der Startzustand (die Leiste setzt zurück)."""
    knoepfe = ''.join(f'<label><input type="radio" name="{name}" value="{w}"{" checked" if k == 0 else ""}> {t}</label>'
                      for k, (w, t) in enumerate(optionen))
    return f'<div class="sim-wahl" role="radiogroup" aria-label="{label}">{knoepfe}</div>'


def sim(nr, label, unten, schalter=''):
    return f'''      <figure class="sim sim-gross" id="sim{nr}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="{label}"></svg>
        {schalter}
        {unten}
      </figure>'''


def ek(d, label='Einheitskreis'):
    """Kreisbild zu einer Aufgabe; d wie in seite.js («Kreisbilder zu den Aufgaben»)."""
    return (f'\n            <div class="mini-reihe"><svg class="ek-mini" aria-label="{label}" '
            f'data-ek="{html.escape(json.dumps(d, ensure_ascii=False), quote=True)}"></svg></div>')


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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim_, clip2, festhalten, uebungen, aufgaben, mehr, komp, hm):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 5.4 · {komp} · {hm}</span><span class="zeit">≈ {zeit} min</span></div>
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


TS = '../grundlagen/g5-4-einheitskreis.html'
VZ = '<table class="vz"><tr><th>Quadrant</th><th>I</th><th>II</th><th>III</th><th>IV</th></tr>' \
     '<tr><td>\\(\\sin\\varphi\\)</td><td>\\(+\\)</td><td>\\(+\\)</td><td>\\(-\\)</td><td>\\(-\\)</td></tr>' \
     '<tr><td>\\(\\cos\\varphi\\)</td><td>\\(+\\)</td><td>\\(-\\)</td><td>\\(-\\)</td><td>\\(+\\)</td></tr></table>'

# ------------------------------------------------------------------ Kapitel 1
sim1 = sim(1, 'Einheitskreis mit dem Punkt P zum eingestellten Winkel, seinem Cosinus (grün, waagrecht) und Sinus (blau, senkrecht)',
           '<div class="sl-row">\n          ' + regler('s1', 'phi', 'Winkel φ', -360, 720, 5, 50) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sinus und Cosinus am Einheitskreis</div>
          <p>Der <b>Einheitskreis</b> hat den Mittelpunkt \(O(0 \mid 0)\) und den Radius \(1\). Der Winkel \(\varphi\) wird ab der positiven \(x\)-Achse <b>gegen den Uhrzeigersinn</b> gemessen. Ein negativer Winkel dreht im Uhrzeigersinn, ein Winkel über \(360^\circ\) mehr als eine Runde.</p>
          <p>Zum Winkel \(\varphi\) gehört der Punkt \(P\) auf dem Kreis. Seine \(y\)-Koordinate ist der Sinuswert, seine \(x\)-Koordinate der Cosinuswert:</p>
          <p>\[ P(\cos\varphi \mid \sin\varphi) \]</p>
          <p>Für \(0^\circ \lt \varphi \lt 90^\circ\) ist das die Definition aus dem Dreieck (GF 5.3): Die Hypotenuse \(OP\) ist \(1\) lang, also \(\sin\varphi = \tfrac{\text{Gegenkathete}}{1}\), \(\cos\varphi = \tfrac{\text{Ankathete}}{1}\).</p>
          <p><b>Vorzeichen</b> — sie folgen aus der Lage von \(P\):</p>
          ''' + VZ + r'''
          <p><b>Auf den Achsen:</b> \(P(1 \mid 0)\) bei \(0^\circ\), \(P(0 \mid 1)\) bei \(90^\circ\), \(P(-1 \mid 0)\) bei \(180^\circ\), \(P(0 \mid -1)\) bei \(270^\circ\). Alle Werte von \(\sin\varphi\) und \(\cos\varphi\) liegen zwischen \(-1\) und \(1\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Sinus und Cosinus vertauschen: \(P\) nennt zuerst den Cosinus (\(x\)), dann den Sinus (\(y\)). Der Sinus ist die <em>Höhe</em> von \(P\).</p>
          <p>Das Vorzeichen übergehen: \(\cos 140^\circ\) ist negativ, weil \(P\) links der \(y\)-Achse liegt.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 2, r'Zeichne einen Einheitskreis (\(1\) Einheit \(= 5\,\text{cm}\)) und darin die Punkte zu \(\varphi = 110^\circ\) und \(\varphi = -30^\circ\). Markiere jeweils \(\sin\varphi\) und \(\cos\varphi\) als Strecken.',
     r'<p>\(110^\circ\): \(P\) im II. Quadranten, links oben — \(\cos 110^\circ \approx -0.342\) (rund \(1.7\,\text{cm}\) links), \(\sin 110^\circ \approx 0.940\) (rund \(4.7\,\text{cm}\) hoch). \(-30^\circ\): im Uhrzeigersinn, IV. Quadrant — \(\cos(-30^\circ) \approx 0.866\), \(\sin(-30^\circ) = -0.5\).</p>'
     + ek({'p': [110, -30], 'sc': True, 'namen': ['110°', '−30°']}, 'Einheitskreis mit den Punkten zu 110° und −30° und ihren Koordinaten'), ''),
    ('1b', 2, r'Bestimme mit dem Taschenrechner die Koordinaten von \(P\) zu \(\varphi = 160^\circ\), auf drei Dezimalen. Passen die Vorzeichen zum Quadranten?',
     r'<p>\(P(\cos 160^\circ \mid \sin 160^\circ) \approx P(-0.940 \mid 0.342)\). \(160^\circ\) liegt im II. Quadranten: links der \(y\)-Achse (Cosinus negativ), über der \(x\)-Achse (Sinus positiv) ✓.</p>', ''),
    ('1c', 3, r'In welchem Quadranten liegt \(P\), und welche Vorzeichen haben \(\sin\varphi\) und \(\cos\varphi\)? (a) \(\varphi = 250^\circ\) (b) \(\varphi = -20^\circ\) (c) \(\varphi = 480^\circ\)',
     r'<p>(a) III. Quadrant: \(\sin\varphi \lt 0\), \(\cos\varphi \lt 0\). (b) \(-20^\circ\) dreht im Uhrzeigersinn unter die \(x\)-Achse: IV. Quadrant, \(\sin\varphi \lt 0\), \(\cos\varphi \gt 0\). (c) \(480^\circ = 360^\circ + 120^\circ\): derselbe Punkt wie bei \(120^\circ\), II. Quadrant, \(\sin\varphi \gt 0\), \(\cos\varphi \lt 0\).</p>', ''),
    ('1d', 2, r'Der Punkt \(P(0.28 \mid -0.96)\) gehört zu einem Winkel \(\varphi\). Zeige mit dem Satz des Pythagoras, dass \(P\) auf dem Einheitskreis liegt. Gib \(\sin\varphi\), \(\cos\varphi\) und den Quadranten an.',
     r'<p>Abstand von \(O\): \(\sqrt{0.28^2 + 0.96^2} = \sqrt{0.0784 + 0.9216} = \sqrt{1} = 1\) ✓. \(\cos\varphi = 0.28\), \(\sin\varphi = -0.96\); IV. Quadrant.</p>', ''),
    ('1e', 2, r'Für spitze Winkel gilt im rechtwinkligen Dreieck \(\sin\varphi = \tfrac{\text{Gegenkathete}}{\text{Hypotenuse}}\). Warum ist das am Einheitskreis genau die \(y\)-Koordinate von \(P\)?',
     r'<p>Das Dreieck aus \(O\), \(P\) und dem Fusspunkt \(Q\) auf der \(x\)-Achse ist rechtwinklig. Seine Hypotenuse \(OP\) ist der Radius, also \(1\). Die Gegenkathete von \(\varphi\) ist die senkrechte Strecke \(QP\) — die Höhe von \(P\), seine \(y\)-Koordinate. Geteilt durch \(1\) bleibt sie, wie sie ist.</p>', ''),
], zwei=False)
k1 = kapitel(1, 'sinus-cosinus', 'Sinus und Cosinus am Einheitskreis', 40,
             r'Du liest Sinus und Cosinus als Koordinaten des Punktes \(P\) auf dem Einheitskreis ab — für jeden Winkel, auch über \(90^\circ\) und negativ — und bestimmst ihre Vorzeichen in den vier Quadranten.',
             ('g5-4-lp-sinus-cosinus', 'Sinus und Cosinus als Koordinaten'),
             sim1, ('g5-4-lp-kontrolle-sinus-cosinus', 'Kontrollfragen zu Sinus und Cosinus'),
             fest1, [uebung('vorzeichen', 'Quadrant und Vorzeichen'), uebung('koordinaten', 'Koordinaten von P')],
             auf1, f'<a href="{TS}#definition">Themenseite 5.4, Definition am Einheitskreis</a> und <a href="{TS}#quadranten">Vorzeichen in den vier Quadranten</a>',
             'K1 · K2', 'Taschenrechner erlaubt')

# ------------------------------------------------------------------ Kapitel 2
sim2 = sim(2, 'Einheitskreis mit dem Punkt P zum eingestellten Winkel in Schritten von 15 Grad und seinem Spiegelbild im ersten Quadranten',
           '<div class="sl-row">\n          ' + regler('s2', 'phi', 'Winkel φ', 0, 360, 15, 45) + '\n        </div>',
           '<label class="hilfs-schalter"><input type="checkbox" checked> Spiegelbild im ersten Quadranten (gestrichelt)</label>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die besonderen Winkel</div>
          <p>\[ \begin{array}{c|ccccc} \varphi & 0^\circ & 30^\circ & 45^\circ & 60^\circ & 90^\circ \\ \hline \sin\varphi & 0 & \tfrac12 & \tfrac{\sqrt2}{2} & \tfrac{\sqrt3}{2} & 1 \\[2pt] \cos\varphi & 1 & \tfrac{\sqrt3}{2} & \tfrac{\sqrt2}{2} & \tfrac12 & 0 \end{array} \]</p>
          <p><b>Merkhilfe:</b> Die Sinuszeile ist \(\tfrac{\sqrt0}{2}, \tfrac{\sqrt1}{2}, \tfrac{\sqrt2}{2}, \tfrac{\sqrt3}{2}, \tfrac{\sqrt4}{2}\); der Cosinus hat dieselben Zahlen rückwärts.</p>
          <p><b>Herkunft:</b> \(45^\circ\) aus dem halben Quadrat (\(x = y\), \(x^2 + x^2 = 1\)), \(30^\circ\) und \(60^\circ\) aus dem halbierten gleichseitigen Dreieck mit Seite \(1\) (halbe Grundseite \(\tfrac12\), Höhe \(\sqrt{1 - \tfrac14} = \tfrac{\sqrt3}{2}\)).</p>
          <p><b>In den anderen Quadranten</b>, ohne Taschenrechner:</p>
          <ol style="padding-left:1.4em;margin:6px 0 10px">
            <li>Quadrant von \(P\) bestimmen. Liegt der Winkel nicht zwischen \(0^\circ\) und \(360^\circ\), zuerst volle Runden dazuzählen oder abziehen: \(-45^\circ\) ist derselbe Punkt wie \(315^\circ\), \(510^\circ\) derselbe wie \(150^\circ\).</li>
            <li><b>Referenzwinkel</b> — der spitze Winkel zwischen \(OP\) und der \(x\)-Achse: im II. Quadranten \(180^\circ - \varphi\), im III. \(\varphi - 180^\circ\), im IV. \(360^\circ - \varphi\).</li>
            <li>Betrag aus der Tabelle, Vorzeichen aus dem Quadranten.</li>
          </ol>
          <p>Beispiel: \(150^\circ\) liegt im II. Quadranten, Referenzwinkel \(30^\circ\): \(\sin 150^\circ = \tfrac12\), \(\cos 150^\circ = -\tfrac{\sqrt3}{2}\).</p>
          <p>Im Bogenmass (GF 5.1): \(30^\circ = \tfrac{\pi}{6}\), \(45^\circ = \tfrac{\pi}{4}\), \(60^\circ = \tfrac{\pi}{3}\), \(90^\circ = \tfrac{\pi}{2}\), \(180^\circ = \pi\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Referenzwinkel zur \(y\)-Achse messen: Bei \(120^\circ\) ist er \(60^\circ\), nicht \(30^\circ\) — sonst sind Sinus und Cosinus vertauscht.</p>
          <p>Das Vorzeichen vergessen: \(\cos 150^\circ\) ist \(-\tfrac{\sqrt3}{2}\), nicht \(\tfrac{\sqrt3}{2}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Gib ohne Taschenrechner exakt an: (a) \(\cos 135^\circ\) (b) \(\sin(-60^\circ)\) (c) \(\cos 420^\circ\)',
     r'<p>(a) II. Quadrant, Referenzwinkel \(45^\circ\): \(-\tfrac{\sqrt2}{2}\). (b) \(-60^\circ\) liegt im IV. Quadranten, Referenzwinkel \(60^\circ\): \(-\tfrac{\sqrt3}{2}\). (c) \(420^\circ = 360^\circ + 60^\circ\), derselbe Punkt wie bei \(60^\circ\): \(\tfrac12\).</p>', ''),
    ('2b', 2, r'Die Winkel stehen im Bogenmass. Gib exakt an: \(\sin\tfrac{7\pi}{6}\) und \(\cos\tfrac{7\pi}{4}\).',
     r'<p>\(\tfrac{7\pi}{6} = 210^\circ\): III. Quadrant, Referenzwinkel \(30^\circ\), \(\sin\tfrac{7\pi}{6} = -\tfrac12\). \(\tfrac{7\pi}{4} = 315^\circ\): IV. Quadrant, Referenzwinkel \(45^\circ\), \(\cos\tfrac{7\pi}{4} = \tfrac{\sqrt2}{2}\).</p>', ''),
    ('2c', 3, r'Begründe mit einem gleichseitigen Dreieck der Seitenlänge \(1\), dass \(\sin 30^\circ = \tfrac12\) und \(\cos 30^\circ = \tfrac{\sqrt3}{2}\) ist.',
     r'<p>Im gleichseitigen Dreieck sind alle Winkel \(60^\circ\). Die Höhe halbiert die Grundseite und den Winkel an der Spitze: Es entsteht ein rechtwinkliges Dreieck mit Hypotenuse \(1\), Winkel \(30^\circ\) an der Spitze und der kurzen Kathete \(\tfrac12\) gegenüber. Also \(\sin 30^\circ = \tfrac{1/2}{1} = \tfrac12\). Die Höhe ist nach Pythagoras \(\sqrt{1 - \tfrac14} = \tfrac{\sqrt3}{2}\) — die Ankathete von \(30^\circ\): \(\cos 30^\circ = \tfrac{\sqrt3}{2}\).</p>', ''),
    ('2d', 2, r'Zeichne in einen Einheitskreis alle Punkte \(P\) mit \(\sin\varphi = \tfrac{\sqrt2}{2}\) und gib ihre Winkel zwischen \(0^\circ\) und \(360^\circ\) an.',
     r'<p>Die Waagrechte in der Höhe \(\tfrac{\sqrt2}{2} \approx 0.707\) trifft den Kreis zweimal: bei \(45^\circ\) und — an der \(y\)-Achse gespiegelt — bei \(135^\circ\).</p>'
     + ek({'p': [45, 135], 'h': 0.7071, 'namen': ['45°', '135°']}, 'Einheitskreis mit der Waagrechten in der Höhe Wurzel zwei halbe und den Punkten zu 45 und 135 Grad'), ''),
    ('2e', 2, r'Warum genügt es, die Werte für Winkel von \(0^\circ\) bis \(90^\circ\) zu kennen?',
     r'<p>Jeder Punkt des Kreises ist das Spiegelbild eines Punktes im ersten Quadranten — an der \(x\)-Achse, an der \(y\)-Achse oder an beiden. Beim Spiegeln bleiben die Beträge der Koordinaten gleich, nur die Vorzeichen können sich ändern. Den Betrag liefert der Referenzwinkel, das Vorzeichen der Quadrant.</p>', ''),
], zwei=False)
k2 = kapitel(2, 'besondere-winkel', 'Besondere Winkel', 40,
             r'Du gibst Sinus und Cosinus der Winkel \(0^\circ\), \(30^\circ\), \(45^\circ\), \(60^\circ\), \(90^\circ\) und ihrer Gegenstücke in den anderen Quadranten exakt an — ohne Taschenrechner, über den Referenzwinkel.',
             ('g5-4-lp-besondere-winkel', 'Besondere Winkel'),
             sim2, ('g5-4-lp-kontrolle-besondere-winkel', 'Kontrollfragen zu den besonderen Winkeln'),
             fest2, [uebung('exakter-wert', 'Exakte Werte'), uebung('referenzwinkel', 'Quadrant und Referenzwinkel')],
             auf2, f'<a href="{TS}#umkehr">Themenseite 5.4, Strategie «Werte ohne Taschenrechner ablesen»</a> und <a href="{TS}#aufgaben">Aufgaben A1 und A3</a>',
             'K2', 'ohne Hilfsmittel')

# ------------------------------------------------------------------ Kapitel 3
sim3 = sim(3, 'Einheitskreis mit der Tangente x = 1, dem Punkt P, der Geraden durch O und P und dem Punkt S auf der Tangente',
           '<div class="sl-row">\n          ' + regler('s3', 'phi', 'Winkel φ', 0, 360, 5, 40) + '\n        </div>',
           '<label class="hilfs-schalter"><input type="checkbox" checked> ähnliche Dreiecke OQP und ORS</label>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Tangens am Einheitskreis</div>
          <p>Rechts am Kreis steht die senkrechte <b>Tangente</b> \(x = 1\); sie berührt den Kreis in \(R(1 \mid 0)\). Die Gerade durch \(O\) und \(P\) schneidet sie im Punkt \(S\). Seine \(y\)-Koordinate ist der Tangenswert:</p>
          <p>\[ S(1 \mid \tan\varphi) \]</p>
          <p>Im II. und III. Quadranten trifft erst die Verlängerung der Geraden über \(O\) hinaus die Tangente.</p>
          <p>Die Dreiecke \(OQP\) (\(Q\) ist der Fusspunkt von \(P\) auf der \(x\)-Achse) und \(ORS\) sind ähnlich: Beide haben bei \(O\) denselben spitzen Winkel und einen rechten Winkel. Im I. Quadranten ist dieser Winkel \(\varphi\), in den anderen Quadranten der Referenzwinkel. Das Seitenverhältnis gibt den Betrag, die Vorzeichen der Koordinaten geben das Vorzeichen — in jedem Quadranten gilt</p>
          <p>\[ \tan\varphi = \frac{\sin\varphi}{\cos\varphi} \qquad (\cos\varphi \neq 0) \]</p>
          <p>Bei \(90^\circ\) und \(270^\circ\) ist \(\cos\varphi = 0\): Die Gerade ist parallel zur Tangente, \(\tan\varphi\) ist <b>nicht definiert</b>. Positiv ist der Tangens im I. und III. Quadranten, negativ im II. und IV. Besondere Werte: \(\tan 0^\circ = 0\), \(\tan 30^\circ = \tfrac{\sqrt3}{3}\), \(\tan 45^\circ = 1\), \(\tan 60^\circ = \sqrt3\).</p>
          <p><b>Trigonometrischer Pythagoras.</b> Im rechtwinkligen Dreieck \(OQP\) sind die Katheten so lang wie \(|\cos\varphi|\) und \(|\sin\varphi|\), die Hypotenuse ist der Radius \(1\):</p>
          <p>\[ \sin^2\varphi + \cos^2\varphi = 1 \]</p>
          <p>Das gilt für jeden Winkel (\(\sin^2\varphi\) heisst \((\sin\varphi)^2\)). Aus einem Wert und dem Quadranten folgt der andere: \(\cos\varphi = \pm\sqrt{1 - \sin^2\varphi}\), das Vorzeichen gibt der Quadrant. Beispiel: \(\sin\varphi = 0.6\) im II. Quadranten: \(\cos^2\varphi = 0.64\), \(\cos\varphi = -0.8\), \(\tan\varphi = \tfrac{0.6}{-0.8} = -0.75\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nach dem Wurzelziehen das Vorzeichen vergessen: Die Wurzel ist positiv, im II. Quadranten ist der Cosinus aber negativ.</p>
          <p>\(\tan 90^\circ = 0\) schreiben: Bei \(90^\circ\) ist der <em>Cosinus</em> \(0\), der Nenner — es gibt keinen Wert. Null ist der Tangens, wo der Sinus null ist.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 2, r'Gib ohne Taschenrechner exakt an: \(\tan 150^\circ\) und \(\tan 300^\circ\).',
     r'<p>\(\tan 150^\circ = \tfrac{1/2}{-\sqrt3/2} = -\tfrac{1}{\sqrt3} = -\tfrac{\sqrt3}{3}\); \(\tan 300^\circ = \tfrac{-\sqrt3/2}{1/2} = -\sqrt3\).</p>', ''),
    ('3b', 3, r'Es gilt \(\cos\varphi = -\tfrac{5}{13}\), und \(\varphi\) liegt im III. Quadranten. Berechne ohne Taschenrechner \(\sin\varphi\) und \(\tan\varphi\).',
     r'<p>\(\sin^2\varphi = 1 - \tfrac{25}{169} = \tfrac{144}{169}\), also \(\sin\varphi = \pm\tfrac{12}{13}\); im III. Quadranten negativ: \(\sin\varphi = -\tfrac{12}{13}\). \(\tan\varphi = \tfrac{-12/13}{-5/13} = \tfrac{12}{5}\) (im III. Quadranten positiv ✓).</p>', ''),
    ('3c', 2, r'Bestimme \(\tan 100^\circ\) mit dem Taschenrechner auf drei Dezimalen. Erkläre am Einheitskreis das Vorzeichen.',
     r'<p>\(\tan 100^\circ \approx -5.671\). \(P\) liegt im II. Quadranten: Die Verlängerung der Geraden durch \(P\) und \(O\) trifft die Tangente weit <em>unter</em> der \(x\)-Achse. Rechnerisch: Sinus positiv, Cosinus negativ — der Quotient ist negativ.</p>', ''),
    ('3d', 2, r'Zeichne in einen Einheitskreis zu \(\varphi = 160^\circ\) den Punkt \(P\), die Tangente \(x = 1\) und den Punkt \(S\). Lies \(\tan 160^\circ\) ungefähr ab.',
     r'<p>Die Gerade durch \(P\) und \(O\) trifft die Tangente unter der \(x\)-Achse: \(S \approx (1 \mid -0.36)\), also \(\tan 160^\circ \approx -0.36\) (genau \(-0.364\)).</p>'
     + ek({'p': [160], 'tan': [160], 'fenster': [-1.4, 1.6, -1.4, 1.4], 'namen': ['P']}, 'Einheitskreis mit P zu 160 Grad und dem Punkt S auf der Tangente'), ''),
    ('3e', 2, r'Warum gibt es \(\tan 90^\circ\) nicht? Gib zwei Gründe an: einen am Kreis und einen mit der Formel.',
     r'<p>Am Kreis: Bei \(90^\circ\) liegt \(P\) auf der \(y\)-Achse, die Gerade durch \(O\) und \(P\) ist parallel zur Tangente \(x = 1\) — es gibt keinen Schnittpunkt \(S\). Mit der Formel: \(\tan 90^\circ = \tfrac{\sin 90^\circ}{\cos 90^\circ} = \tfrac{1}{0}\), und durch null kann man nicht teilen.</p>', ''),
], zwei=False)
k3 = kapitel(3, 'tangens-pythagoras', 'Tangens und trigonometrischer Pythagoras', 40,
             r'Du deutest \(\tan\varphi\) als Höhe des Punktes \(S\) auf der Tangente \(x = 1\), rechnest \(\tan\varphi = \tfrac{\sin\varphi}{\cos\varphi}\), erklärst, warum es bei \(90^\circ\) keinen Wert gibt, und bestimmst mit \(\sin^2\varphi + \cos^2\varphi = 1\) aus einem Wert und dem Quadranten den anderen.',
             ('g5-4-lp-tangens-pythagoras', 'Tangens und Pythagoras'),
             sim3, ('g5-4-lp-kontrolle-tangens-pythagoras', 'Kontrollfragen zu Tangens und Pythagoras'),
             fest3, [uebung('tan-wert', 'Tangenswerte'), uebung('pythagoras', 'Aus einem Wert die anderen')],
             auf3, f'<a href="{TS}#tangens">Themenseite 5.4, Tangens am Einheitskreis</a> und <a href="{TS}#beziehungen">Beziehungen zwischen den Winkelfunktionen</a>',
             'K1 · K2 · K3', 'ohne Hilfsmittel, 3c mit Taschenrechner')

# ------------------------------------------------------------------ Kapitel 4
sim4 = sim(4, 'Einheitskreis mit dem Punkt A zum Winkel alpha und seinem Spiegelpunkt B, gestrichelt die Spiegelachse',
           wahl('s4-modus', 'Spiegelung', [('180-a', '180° − α'), ('neg', '−α'), ('180+a', '180° + α'), ('90-a', '90° − α')])
           + '\n        <div class="sl-row">\n          ' + regler('s4', 'a', 'Winkel α', 0, 90, 5, 25) + '\n        </div>')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Symmetrien am Einheitskreis</div>
          <p>Jede Regel ist eine Spiegelung des Punktes zu \(\alpha\). Man muss sie nicht auswendig lernen: Punkt zeichnen, spiegeln, Koordinaten vergleichen.</p>
          <p>Die Spiegelungen: \(180^\circ - \alpha\) an der \(y\)-Achse, \(-\alpha\) an der \(x\)-Achse (derselbe Punkt wie \(360^\circ - \alpha\)), \(90^\circ - \alpha\) an der Geraden \(y = x\) — und \(180^\circ + \alpha\) am Ursprung \(O\) (Punktspiegelung).</p>
          <p>\[ \begin{array}{l|c|c|c} & \sin & \cos & \tan \\ \hline 180^\circ - \alpha & \sin\alpha & -\cos\alpha & -\tan\alpha \\ 180^\circ + \alpha & -\sin\alpha & -\cos\alpha & \tan\alpha \\ -\alpha & -\sin\alpha & \cos\alpha & -\tan\alpha \\ 90^\circ - \alpha & \cos\alpha & \sin\alpha & \tfrac{1}{\tan\alpha} \end{array} \]</p>
          <p>In der Tangensspalte muss \(\cos\alpha \neq 0\) sein, in der letzten Zeile auch \(\sin\alpha \neq 0\).</p>
          <p>Die erste Zeile ist das <b>Supplement</b>: \(\alpha\) und \(180^\circ - \alpha\) ergänzen sich zu \(180^\circ\). Die letzte Zeile ist das <b>Komplement</b>: \(x\) und \(y\) tauschen die Plätze. Im Bogenmass, wie im Lehrplan: \(\sin\left(\tfrac{\pi}{2} - \varphi\right) = \cos\varphi\) und \(\cos\left(\tfrac{\pi}{2} - \varphi\right) = \sin\varphi\). Im rechtwinkligen Dreieck ist \(90^\circ - \alpha\) der andere spitze Winkel: Seine Gegenkathete ist die Ankathete von \(\alpha\).</p>
          <p>Beispiel: \(\cos 205^\circ = \cos(180^\circ + 25^\circ)\) \(= -\cos 25^\circ \approx -0.906\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bei \(180^\circ - \alpha\) auch den Sinus umdrehen: Die Spiegelung an der \(y\)-Achse ändert nur die \(x\)-Koordinate.</p>
          <p>Komplement und Supplement verwechseln: \(\sin(90^\circ - \alpha) = \cos\alpha\), aber \(\sin(180^\circ - \alpha) = \sin\alpha\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Es gilt \(\sin 15^\circ \approx 0.259\) und \(\cos 15^\circ \approx 0.966\). Gib ohne Taschenrechner an: (a) \(\sin 165^\circ\) (b) \(\cos 195^\circ\) (c) \(\cos(-15^\circ)\)',
     r'<p>(a) \(\sin(180^\circ - 15^\circ) = \sin 15^\circ \approx 0.259\). (b) \(\cos(180^\circ + 15^\circ) = -\cos 15^\circ \approx -0.966\). (c) \(\cos(-15^\circ) = \cos 15^\circ \approx 0.966\).</p>', ''),
    ('4b', 2, r'Drücke \(\sin 70^\circ\) durch einen Cosinus und \(\cos 10^\circ\) durch einen Sinus aus.',
     r'<p>\(\sin 70^\circ = \cos(90^\circ - 70^\circ) = \cos 20^\circ\); \(\cos 10^\circ = \sin(90^\circ - 10^\circ) = \sin 80^\circ\).</p>', ''),
    ('4c', 3, r'Vereinfache: (a) \(\cos(180^\circ - \varphi) + \cos(-\varphi)\) (b) \(\sin(90^\circ - \varphi) \cdot \tan\varphi\) für \(\cos\varphi \neq 0\)',
     r'<p>(a) \(-\cos\varphi + \cos\varphi = 0\). (b) \(\cos\varphi \cdot \tfrac{\sin\varphi}{\cos\varphi} = \sin\varphi\).</p>', ''),
    ('4d', 2, r'Zeichne in einen Einheitskreis die Punkte zu \(40^\circ\) und \(140^\circ\). Begründe am Bild: \(\sin 140^\circ = \sin 40^\circ\) und \(\cos 140^\circ = -\cos 40^\circ\).',
     r'<p>\(140^\circ = 180^\circ - 40^\circ\): Der zweite Punkt ist das Spiegelbild des ersten an der \(y\)-Achse. Er liegt gleich hoch (gleicher Sinus), aber gleich weit links statt rechts (Cosinus mit umgekehrtem Vorzeichen).</p>'
     + ek({'p': [40, 140], 'sc': True, 'namen': ['40°', '140°']}, 'Einheitskreis mit den Punkten zu 40 und 140 Grad, gespiegelt an der y-Achse'), ''),
    ('4e', 2, r'Warum gilt \(\sin(90^\circ - \alpha) = \cos\alpha\)? Begründe am rechtwinkligen Dreieck.',
     r'<p>Im rechtwinkligen Dreieck mit dem spitzen Winkel \(\alpha\) ist der andere spitze Winkel \(90^\circ - \alpha\) (Winkelsumme \(180^\circ\)). Die Kathete, die \(\alpha\) anliegt, liegt \(90^\circ - \alpha\) gegenüber. Also ist \(\sin(90^\circ - \alpha) = \tfrac{\text{Ankathete von } \alpha}{\text{Hypotenuse}} = \cos\alpha\).</p>', ''),
], zwei=False)
k4 = kapitel(4, 'symmetrien', 'Symmetrien', 40,
             r'Du begründest die Beziehungen für \(180^\circ - \alpha\), \(180^\circ + \alpha\), \(-\alpha\) und \(90^\circ - \alpha\) als Spiegelungen am Einheitskreis und führst damit Werte ohne Taschenrechner auf bekannte zurück.',
             ('g5-4-lp-symmetrien', 'Symmetrien am Einheitskreis'),
             sim4, ('g5-4-lp-kontrolle-symmetrien', 'Kontrollfragen zu den Symmetrien'),
             fest4, [uebung('symmetrie-wert', 'Werte über Symmetrie'), uebung('symmetrie-regel', 'Welche Regel?')],
             auf4, f'<a href="{TS}#symmetrie">Themenseite 5.4, Symmetrieeigenschaften</a>',
             'K3', 'ohne Hilfsmittel')

# ------------------------------------------------------------------ Kapitel 5
sim5 = sim(5, 'Einheitskreis mit einem Wert w: Waagrechte, Senkrechte oder Gerade durch O, die Kreispunkte mit diesem Wert und der Hauptwertbereich des Rechners',
           wahl('s5-fn', 'Umkehroperation', [('sin', 'Sinus'), ('cos', 'Cosinus'), ('tan', 'Tangens')])
           + '\n        <div class="sl-row">\n          ' + regler('s5', 'w', 'Wert w', -2, 2, 0.05, 0.4, 'grau', '') + '\n        </div>')
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Periode und Umkehroperationen</div>
          <p><b>Periodizität.</b> Nach einer vollen Runde liegt \(P\) wieder am selben Ort:</p>
          <p>\[ \sin(\varphi + k \cdot 360^\circ) = \sin\varphi \]
             \[ \cos(\varphi + k \cdot 360^\circ) = \cos\varphi \qquad (k \in \mathbb{Z}) \]</p>
          <p>Der Tangens wiederholt sich schon nach einer halben Runde, weil der gegenüberliegende Punkt auf derselben Geraden durch \(O\) liegt: \(\tan(\varphi + k \cdot 180^\circ) = \tan\varphi\). Im Bogenmass sind die Perioden \(2\pi\) und \(\pi\).</p>
          <p><b>Umkehroperationen</b> gehen vom Wert zurück zum Winkel:</p>
          <p>Zu einem Wert gehören am Kreis meist zwei Punkte und wegen der Periode unendlich viele Winkel. Die Umkehroperation wählt davon einen, den <b>Hauptwert</b>:</p>
          <p>\(\arcsin w\) ist der Winkel aus \([-90^\circ;\, 90^\circ]\) mit \(\sin\varphi = w\) (rechte Kreishälfte; \(-1 \le w \le 1\)).<br>
             \(\arccos w\) ist der Winkel aus \([0^\circ;\, 180^\circ]\) mit \(\cos\varphi = w\) (obere Kreishälfte; \(-1 \le w \le 1\)).<br>
             \(\arctan w\) ist der Winkel aus \(]{-90^\circ};\, 90^\circ[\) mit \(\tan\varphi = w\) (rechte Kreishälfte ohne Endpunkte; jedes \(w\)).</p>
          <p>Auf dem Taschenrechner heissen sie \(\sin^{-1}\), \(\cos^{-1}\), \(\tan^{-1}\) — das ist <em>nicht</em> \(\tfrac{1}{\sin w}\). Beispiel: \(\sin^{-1}(0.4) \approx 23.6^\circ\) — den zweiten Punkt mit derselben Höhe liefert er nicht.</p>
          <p><b>Welchen Winkel liefert der Rechner?</b> Gegeben ist ein Winkel \(\beta\) ausserhalb des Hauptwertbereichs, zum Beispiel \(\beta = 210^\circ\) mit \(\sin 210^\circ = -\tfrac12\).</p>
          <ol style="padding-left:1.4em;margin:6px 0 10px">
            <li>Den zweiten Kreispunkt mit demselben Wert suchen, mit einer Spiegelung aus Kapitel 4: gleicher Sinus — an der \(y\)-Achse gespiegelt; gleicher Cosinus — an der \(x\)-Achse; gleicher Tangens — der Punkt gegenüber.</li>
            <li>Er liegt im Hauptwertbereich: Seinen Winkel <em>in diesem Bereich</em> angeben, unter der \(x\)-Achse also negativ.</li>
          </ol>
          <p>Hier: \(210^\circ\) liegt links unten. Das Spiegelbild an der \(y\)-Achse liegt gleich hoch, rechts unten, \(30^\circ\) unter der positiven \(x\)-Achse: \(\sin^{-1}(-0.5) = -30^\circ\).</p>
          <p>Wie man alle Winkel zu einem Wert findet und als Lösungsmenge aufschreibt, zeigt das Leitprogramm <a href="trigonometrische-gleichungen.html">Trigonometrische Gleichungen</a> (GF 5.5).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Winkel des Rechners für «den» Winkel halten: Er ist einer von vielen mit demselben Wert.</p>
          <p>Der Rechner steht im Bogenmass (RAD): \(\sin^{-1}(0.5)\) gibt dann \(0.524\) statt \(30^\circ\).</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 10, [
    ('5a', 3, r'Führe mit der Periode zurück und gib ohne Taschenrechner exakt an: (a) \(\sin 495^\circ\) (b) \(\cos(-240^\circ)\) (c) \(\tan 585^\circ\)',
     r'<p>(a) \(495^\circ - 360^\circ = 135^\circ\): \(\sin 135^\circ = \tfrac{\sqrt2}{2}\). (b) \(-240^\circ + 360^\circ = 120^\circ\): \(\cos 120^\circ = -\tfrac12\). (c) \(585^\circ - 3 \cdot 180^\circ = 45^\circ\): \(\tan 45^\circ = 1\).</p>', ''),
    ('5b', 3, r'Berechne mit dem Taschenrechner auf \(0.1^\circ\): \(\sin^{-1}(-0.8)\) und \(\cos^{-1}(-0.8)\). In welchem Quadranten liegt der Punkt \(P\) jeweils?',
     r'<p>\(\sin^{-1}(-0.8) \approx -53.1^\circ\): im Uhrzeigersinn, IV. Quadrant (rechte Kreishälfte, Hauptwert des Arkussinus). \(\cos^{-1}(-0.8) \approx 143.1^\circ\): II. Quadrant (obere Kreishälfte, Hauptwert des Arkuscosinus).</p>', ''),
    ('5c', 2, r'Der Rechner liefert \(\sin^{-1}(0.9) \approx 64.2^\circ\). Zeichne alle Punkte des Einheitskreises mit \(\sin\varphi = 0.9\). Welcher gehört zum Winkel des Rechners — und warum liefert er den anderen nicht?',
     r'<p>Die Waagrechte \(y = 0.9\) trifft den Kreis zweimal, rechts und links der \(y\)-Achse. Der rechte Punkt gehört zu \(64.2^\circ\). Der linke liegt im II. Quadranten, ausserhalb des Hauptwertbereichs \([-90^\circ;\, 90^\circ]\) des Arkussinus — darum liefert ihn der Rechner nicht.</p>'
     + ek({'p': [64.158, 115.842], 'h': 0.9, 'hohl': True, 'namen': ['64.2°', '']}, 'Einheitskreis mit der Waagrechten y = 0.9 und den zwei Punkten in dieser Höhe'), ''),
    ('5d', 2, r'Mia tippt \(\cos^{-1}(-0.5)\) und erhält \(2.094\). Was ist passiert, und welchen Winkel sucht sie?',
     r'<p>Der Rechner steht im Bogenmass (RAD). \(2.094 \approx \tfrac{2\pi}{3}\) ist im Bogenmass der Winkel \(120^\circ\). Im Gradmodus (DEG) zeigt er \(120\).</p>', ''),
], zwei=False)
k5 = kapitel(5, 'periode-umkehr', 'Periode und Umkehroperationen', 35,
             r'Du führst Winkel über \(360^\circ\) und negative Winkel mit der Periode zurück, erläuterst \(\arcsin\), \(\arccos\) und \(\arctan\) als Umkehroperationen und erklärst, warum der Taschenrechner zu einem Wert nur einen Winkel liefert — und welchen.',
             ('g5-4-lp-periode-umkehr', 'Periode und Umkehroperationen'),
             sim5, ('g5-4-lp-kontrolle-periode-umkehr', 'Kontrollfragen zu Periode und Umkehrung'),
             fest5, [uebung('periode', 'Mit der Periode zurückführen'), uebung('hauptwert', 'Welchen Winkel liefert der Rechner?')],
             auf5, f'<a href="{TS}#umkehr">Themenseite 5.4, Umkehroperationen</a> und <a href="{TS}#def-werte">Definitions- und Wertemenge</a>',
             'K3 · K1', 'Periode ohne, Umkehrung mit Taschenrechner')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 5.1 · GF 5.3</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Sinus, Cosinus und Tangens im rechtwinkligen Dreieck, der Winkel zurück mit dem Rechner, Bogenmass und der Satz des Pythagoras. Wenn das wackelt: Leitprogramm <a href="trigonometrische-berechnungen.html">Trigonometrische Berechnungen</a> (GF 5.3) und <a href="../grundlagen/g5-1-grundlagen.html">Themenseite 5.1, Grad und Radiant</a>.</p>
      ''' + clipkarte('g5-3-sin-cos-tan', 'Trigonometrie: Sinus, Cosinus und Tangens am Dreieck', '0:57') + '''
      ''' + clipkarte('g5-4-gradmass-bogenmass', 'Einheitskreis: Gradmass und Bogenmass', '0:56') + '''
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Ein rechtwinkliges Dreieck hat die Katheten \(3\,\text{cm}\) und \(4\,\text{cm}\) und die Hypotenuse \(5\,\text{cm}\). Der Winkel \(\alpha\) liegt der Kathete \(3\,\text{cm}\) gegenüber. Gib \(\sin\alpha\), \(\cos\alpha\) und \(\tan\alpha\) als Bruch an.',
     r'<p>\(\sin\alpha = \tfrac35\), \(\cos\alpha = \tfrac45\), \(\tan\alpha = \tfrac34\).</p><p class="komm">Gegenkathete, Ankathete, Hypotenuse — der erste Clip oben.</p>', ''),
    ('0b', 2, r'In einem rechtwinkligen Dreieck ist \(\sin\alpha = 0.75\). Wie gross ist \(\alpha\)? (Taschenrechner, auf \(0.1^\circ\))',
     r'<p>\(\alpha = \sin^{-1}(0.75) \approx 48.6^\circ\).</p><p class="komm">Den Winkel liefert die Taste \(\sin^{-1}\) — im Modus DEG. Kapitel 5 zeigt, was dieser Wert am Einheitskreis bedeutet.</p>', ''),
    ('0c', 2, r'Rechne ins Bogenmass um: \(90^\circ\); \(180^\circ\); \(60^\circ\).',
     r'<p>\(\tfrac{\pi}{2}\); \(\pi\); \(\tfrac{\pi}{3}\).</p><p class="komm">\(180^\circ = \pi\) — der zweite Clip oben.</p>', ''),
    ('0d', 2, r'Ein rechtwinkliges Dreieck hat die Hypotenuse \(1\) und eine Kathete \(0.6\). Wie lang ist die andere Kathete?',
     r'<p>\(\sqrt{1 - 0.36} = \sqrt{0.64} = 0.8\).</p><p class="komm">Genau diese Rechnung steckt im trigonometrischen Pythagoras (Kapitel 3).</p>', ''),
    ('0e', 2, r'In welchem Quadranten liegt der Punkt \((-2 \mid 3)\)? Und \((1 \mid -4)\)?',
     r'<p>\((-2 \mid 3)\): II. Quadrant; \((1 \mid -4)\): IV. Quadrant.</p><p class="komm">Die Quadranten zählen gegen den Uhrzeigersinn: I rechts oben, II links oben, III links unten, IV rechts unten.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/einheitskreis/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 5.4 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Skizze und Rechenweg. Teil A ohne Taschenrechner: Die Beziehungen am Einheitskreis (K3) tragen im Lehrplan den Vermerk «auch ohne Hilfsmittel». Dass auch die Werte der besonderen Winkel (K2) ohne Rechner verlangt sind, ist eine Auslegung dieses Leitprogramms, wie auf der Themenseite (Aufgaben A1–A3). Teil B mit Taschenrechner.<br>
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
          <p>Aufgabe → Kapitel: G1 → 1, 3; G2 → 2, 3, 5; G3 → 1, 3; G4 → 4; G5 → 3, 4, 5; G6 → 1; G7 → 5; G8 → 4, 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Einheitskreis, Version 1.0 (07.10.2026). Gebaut aus scripts/lp/einheitskreis/seite.py —
     Änderungen dort, nicht in dieser Datei. Verfahren: HOWTO-leitprogramme.md (Kapitelmuster).

     RLP-BM 2030, Grundlagenfach, Lerngebiet 5 Geometrie, Teilgebiet 5.4 Einheitskreis, wörtlich wie in der
     RLP-Box der Themenseite g5-4 (der Lehrplan schreibt «Kosinus», die Site «Cosinus»):
       K1  die Definition von Sinus, Cosinus und Tangens am Einheitskreis sowie deren Umkehroperationen erläutern
       K2  für ausgewählte Winkel entsprechende Funktionswerte am Einheitskreis bestimmen und visualisieren
       K3  elementare trigonometrische Beziehungen erläutern (trigonometrischer Pythagoras, Periodizität,
           Symmetrien, sin(π/2 − φ) = cos(φ) usw.) — auch ohne Hilfsmittel
     Hilfsmittel: K3 ohne Taschenrechner (Vermerk). Bei K2 gehören die besonderen Winkel (0°, 30°, 45°, 60°,
     90° und ihre Gegenstücke) ebenfalls ohne Rechner dazu (Themenseite A1–A3 «auch ohne Hilfsmittel»);
     beliebige Winkel und die Umkehroperationen (K1) mit Rechner.

     Kompetenzmatrix (Kompetenz | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 Definition sin, cos, tan; Umkehroperationen | mit TR | 1, 3, 5 | 1a–1e, 3c–3e, 5b–5d | G1, G6, G7, G8
       K2 Werte ausgewählter Winkel, visualisieren    | besondere Werte ohne | 1, 2, 3 | 1a, 1b, 2a–2d, 3a, 3d | G1, G2, G6
       K3 Pythagoras, Periodizität, Symmetrien         | ohne     | 3, 4, 5 | 3b, 4a–4e, 5a   | G2b (Periode), G3, G4, G5, G7, G8
     Kein Kapitelziel ohne Kompetenz. Gesamttest: Teil A (G1–G5, 16 P) ohne, Teil B (G6–G8, 9 P) mit Rechner.
     Nach der Prüfung vom 08.10.2026 neu: G2–G5 (keine Wiederholung von 1d, 2b, 4a, 4e), G5 prüft «kein Tangens bei 90°».

     Planung (Kapitel | Lernziel | Kompetenz | Clips | Tüfteln | Beispiel | Häufiger Fehler | min):
       0 Vorwissen       | Dreieck, Umkehrtaste, Bogenmass, Pythagoras | GF 5.1, 5.3 | g5-3-sin-cos-tan, g5-4-gradmass-bogenmass | — | 3-4-5-Dreieck | — | 10
       1 Sinus/Cosinus   | P(cos φ | sin φ), Quadranten, negativ und über 360° | K1 K2 | lp-sinus-cosinus + Kontrolle | sim1 −360°…720° | 50°, 140°, 230°, 320°, −60° | sin/cos vertauscht; Vorzeichen | 40
       2 Besondere Winkel| exakte Werte über Referenzwinkel, ohne TR | K2 | lp-besondere-winkel + Kontrolle | sim2 15°-Schritte mit Spiegelbild | 45°, 60°, 30°, 150°, 225°, 300° | Referenzwinkel zur y-Achse | 40
       3 Tangens, Pythagoras | S(1 | tan φ), tan = sin/cos, nicht definiert, sin² + cos² = 1 | K1 K2 K3 | lp-tangens-pythagoras + Kontrolle | sim3 mit Tangente und ähnlichen Dreiecken | 40°, 130°, sin φ = 0.6 im II. Q. | Vorzeichen nach der Wurzel; tan 90° = 0 | 40
       4 Symmetrien      | 180° − α, 180° + α, −α, 90° − α als Spiegelungen | K3 | lp-symmetrien + Kontrolle | sim4 Spiegelpunkt | α = 25° | Supplement/Komplement verwechselt | 40
       5 Periode, Umkehr | k · 360°, k · 180°; arcsin/arccos/arctan, Hauptwert | K3 K1 | lp-periode-umkehr + Kontrolle | sim5 Wert → Kreispunkte | 390°, sin⁻¹(0.4), cos⁻¹(−0.3) | nur den Rechnerwinkel; RAD | 35
       Gesamttest 30 — Summe 235 min ≈ fünf Lektionen plus Gesamttest.

     Kern: alles oben. Bewusst weggelassen (→ Themenseite 5.4): die Umrechnungstabelle sin ↔ cos ↔ tan mit
     Wurzeltermen (hier nur der Weg über sin² + cos² = 1), die Merkregel «All Students Take Calculus»,
     Definitions- und Wertemenge als Mengen (hier nur «zwischen −1 und 1» und «nicht definiert bei 90°, 270°»),
     die Tagestemperatur als Sinuskurve (A7, Vertiefung, gehört zu den Funktionen SP 3.5). Nicht in diesem
     Leitprogramm, sondern in GF 5.5 (Leitprogramm trigonometrische-gleichungen): alle Lösungen von sin x = c,
     die zweite Lösung als Verfahren, Lösungsmengen. Kapitel 5 zeigt den zweiten Kreispunkt nur, um zu
     erklären, warum der Rechner einen einzigen Winkel liefert.

     Konventionen wie auf der Themenseite: Winkel φ in Grad, ab der positiven x-Achse gegen den Uhrzeigersinn;
     P(cos φ | sin φ); Tangente x = 1 mit R(1 | 0) und S(1 | tan φ); Dreiecke OQP und ORS; Quadranten I–IV;
     Referenzwinkel zur x-Achse; arcsin, arccos, arctan, am Rechner sin⁻¹ usw.; Bogenmass aus GF 5.1.
     Farben: Sinus blau, Cosinus grün, Tangens orange, rot = Gegenbeispiel, Tinte = neutral.

     Widersprüche in der Themenseite (gemeldet, nicht übernommen):
       – Koordinaten mit Komma «P = (cos φ, sin φ)» (Anim 1) und «S = (1, tan φ)» (Anim 2) neben P(cos φ | sin φ)
         im Text; hier durchgehend mit senkrechtem Strich.
       – Tangens-Definition: «die y-Koordinate des Schnittpunkts S des Strahls OP» und «entspricht der Länge des
         Tangentenabschnitts RS» — im II./III. Quadranten trifft der Strahl die Tangente nicht (der Kasten daneben
         sagt es richtig), und eine Länge ist nie negativ. Hier: die Gerade durch O und P, y-Koordinate von S.
       – Farben: Sinus rot und Cosinus grün in Anim 1, Sinus grün und Cosinus orange im Abwickler.
       – Bogenmass: «in ↩ 5.1 erklärt», die Themenseite 5.4 hat aber einen eigenen Clip dazu; das Leitprogramm
         Planimetrie verweist für das Bogenmass auf 5.4. Hier: Vorwissen aus GF 5.1.
       – «Fundament für die Behandlung als Funktionen in Kapitel 5.5» (Einstieg, Abwickler) — 5.5 sind die
         trigonometrischen Gleichungen, die Funktionen stehen im Schwerpunktfach 3.5. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Einheitskreis</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 5.4</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Sinus und Cosinus</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Besondere Winkel</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Tangens, Pythagoras</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Symmetrien</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Periode, Umkehrung</span></a></li>
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
          <li><b>② Tüfteln:</b> Aufgaben in der Simulation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Skizze am Einheitskreis, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 5.4 Einheitskreis:</p>
        <ul>
          <li><b>K1</b> die Definition von Sinus, Cosinus und Tangens am Einheitskreis sowie deren Umkehroperationen erläutern — Kapitel 1, 3, 5, mit Taschenrechner</li>
          <li><b>K2</b> für ausgewählte Winkel entsprechende Funktionswerte am Einheitskreis bestimmen und visualisieren — Kapitel 1–3; die besonderen Winkel (Kapitel 2) ohne Taschenrechner — das ist eine Auslegung wie auf der Themenseite, der Lehrplan vermerkt «ohne Hilfsmittel» nur bei K3</li>
          <li><b>K3</b> elementare trigonometrische Beziehungen erläutern (trigonometrischer Pythagoras, Periodizität, Symmetrien, \\(\\sin(\\frac{\\pi}{2}-\\varphi) = \\cos(\\varphi)\\) usw.) <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 3–5</li>
        </ul>
        <p class="rlp-quelle">Nicht hier, sondern im Leitprogramm <a href="trigonometrische-gleichungen.html">Trigonometrische Gleichungen</a> (GF 5.5): alle Lösungen einer Gleichung wie \\(\\sin\\varphi = 0.4\\) und ihre Lösungsmenge. Auf der <a href="''' + TS + '''">Themenseite 5.4</a>: die Umrechnungstabelle zwischen den drei Funktionen und die Tagestemperatur als Sinuskurve.</p>
      </details>
    </div>
'''
unten = '''
    <div class="weiter">
      <div>
        <h3 id="weiter">Weiter</h3>
        <p>Nächstes Leitprogramm: <a href="trigonometrische-gleichungen.html">Trigonometrische Gleichungen</a> (GF 5.5) — Gleichungen wie \\(\\sin\\varphi = 0.4\\) am Einheitskreis lösen. Zum Nachschlagen: <a href="''' + TS + '''">Themenseite 5.4 Einheitskreis</a>.</p>
      </div>
    </div>

    <div class="fuss">
      <span>Leitprogramm Einheitskreis · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (07.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 40 · K4 40 · K5 35 · Gesamttest 30 = 235 min
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
