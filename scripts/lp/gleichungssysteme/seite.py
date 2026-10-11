"""Baut leitprogramme/gleichungssysteme.html aus einer Kapitelbeschreibung (11.10.2026).

  python3 scripts/lp/gleichungssysteme/seite.py

Leitprogramm zum Teilgebiet GF 2.3 (Themenseite grundlagen/g2-3-lineare-gleichungssysteme.html) im
Kapitelmuster (HOWTO-leitprogramme §4). Ersetzt das ältere, klassische Leitprogramm unter derselben Adresse.
Beim ersten Lauf kommt das Gerüst (Kopf, <style>, Grundskript) aus leitprogramme/lineare-quadratische-gleichungen.html;
SEO-Block und Footer bleiben die der bisherigen Datei (beide schreibt scripts/build-seo.py). Danach liest das
Skript die eigene Seite. Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Siehe README.md.
"""
import json
import os
import re
import sys

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, SP)
import umformer   # noqa: E402
import zahlen     # noqa: E402

R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/gleichungssysteme.html'
NAME = 'Lineare Gleichungssysteme'
MARKE = '\n/* ════════ Gleichungssysteme (11.10.2026)'

alt = open(ZIEL).read()
if MARKE not in alt:                                   # erster Lauf: Gerüst vom Vorbild, SEO und Fuss von der alten Seite
    vorbild = open(R + 'leitprogramme/lineare-quadratische-gleichungen.html').read()
    seo = alt[alt.index('<!-- SEO:ANFANG'):alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')]
    fuss_alt = alt[alt.index('<!-- FUSS:ANFANG'):alt.index('<!-- FUSS:ENDE -->') + len('<!-- FUSS:ENDE -->')]
    a, b = vorbild.index('<!-- SEO:ANFANG'), vorbild.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    vorbild = vorbild[:a] + seo + vorbild[b:]
    a, b = vorbild.index('<!-- FUSS:ANFANG'), vorbild.index('<!-- FUSS:ENDE -->') + len('<!-- FUSS:ENDE -->')
    vorbild = vorbild[:a] + fuss_alt + vorbild[b:]
    vorbild = re.sub(r'<title>[^<]*</title>', '<title>Leitprogramm ' + NAME + '</title>', vorbild, count=1)
    vorbild = vorbild.replace('lp-gleichungen-', 'lp-lgs-')
    alt = vorbild

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Gleichungen (06.10.2026)', MARKE):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Lineare und quadratische Gleichungen —'),
                    alt.find('<script>\n/* Leitprogramm Lineare Gleichungssysteme —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<!-- FUSS:ANFANG'):]

CSS = MARKE + r''' — Kapitelmuster wie die Funktionen-Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Neu: der System-Umformer (Umformer
   der Gleichungen, erweitert auf Systeme) und zwei Geraden-Simulationen. Farben: Gleichung (I) blau, Gleichung (II)
   orange, Lösung grün, Fehler rot; Umformungsschritte und Parameter neutral. */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:420px}
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
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.festhalten table{border-collapse:collapse;width:100%;font-size:.92rem;margin:6px 0 10px}
.festhalten td,.festhalten th{border-bottom:1px solid var(--blau-rand);padding:5px 6px;text-align:left;vertical-align:top}
.festhalten th{font-family:var(--sans);font-size:.78rem;color:var(--tinte-2);font-weight:700}
.tabelle-scroll{overflow-x:auto}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-aufgabe mjx-container{max-width:100%;overflow-x:auto;overflow-y:hidden}
.sim-formel{line-height:1.6;font-size:.92rem}
.nb{white-space:nowrap}
/* Geraden: (I) blau, (II) orange, Hilfslinien grün gestrichelt; identische Geraden breit + gestrichelt darüber. */
.gerade{fill:none;stroke-width:2.6;stroke-linecap:round}
.gerade.g1{stroke:var(--blau)} .gerade.g2{stroke:var(--orange)} .gerade.g3{stroke:var(--gruen)} .gerade.g5{stroke:var(--tinte-2)}
.gerade.breit{stroke-width:7;opacity:.55}
.gerade.gestrichelt{stroke-dasharray:7 5}
svg.mini .gerade{stroke-width:2.2} svg.mini .gerade.breit{stroke-width:5.5}
.p-loes{fill:var(--gruen)} .p-g{fill:var(--blau)} .p-n{fill:var(--orange)} .p-p{fill:var(--tinte)}
.sim-legende{font-family:var(--sans);font-size:.84rem;color:var(--tinte-2);text-align:center;margin:8px auto 0;max-width:60ch}
.sim .sl-row{flex-wrap:wrap;justify-content:center;gap:6px 14px}
.sim .sl-grp{display:flex;align-items:center;gap:8px;flex:1 1 220px;min-width:0}
.sim .sl-grp input[type=range]{flex:1;min-width:0}
.sim-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px}
.sim-wahl{font-family:var(--sans);font-size:.88rem;padding:4px 8px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
/* System-Umformer: Verlauf wie im Heft — System bzw. Gleichung links, Umformung rechts daneben (neutral). */
.lgs-umformer{max-width:760px;margin:10px auto 6px}
.uf-verlauf{display:grid;grid-template-columns:minmax(0,auto) auto;justify-content:start;align-items:center;gap:4px 22px;padding:10px 14px;
  border:1px solid var(--linie);border-radius:9px;background:var(--karte);min-height:2.6em;overflow-x:auto}
.uf-zeile{display:contents}
.uf-gl{color:var(--blau)}
.uf-op{color:var(--tinte-2);font-size:.95em}
.uf-frage{font-family:var(--sans);font-size:.88rem;color:var(--tinte-2);margin:10px 2px 6px}
.uf-wahl{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.uf-knopf{font-family:var(--sans);font-size:.88rem;cursor:pointer;border-radius:8px;padding:6px 12px;border:1.5px solid var(--orange-rand);
  background:var(--orange-hell);color:var(--tinte);text-align:left;max-width:100%}
.uf-knopf:hover,.uf-knopf:focus-visible{border-color:var(--orange);outline:none}
.uf-feld{font-family:var(--mono);font-size:.95rem;display:inline-flex;flex-wrap:wrap;align-items:center;gap:4px}
.uf-feld input{width:4.2em;font-family:var(--mono);font-size:.95rem;padding:4px 6px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.uf-feld input.uf-menge{width:11em}
.uf-feld input:focus{outline:none;border-color:var(--orange-rand)}
.uf-pruefen,.uf-werkzeug button{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;border:1px solid var(--orange-rand);background:var(--karte);color:var(--tinte)}
.uf-werkzeug{display:flex;gap:8px;justify-content:flex-end;margin-top:8px}
.uf-werkzeug button{border-color:var(--linie);color:var(--tinte-2)}
.uf-werkzeug button:disabled{opacity:.4;cursor:default}
.uf-rueck{font-family:var(--sans);font-size:.9rem;margin-top:10px;border-radius:7px}
.uf-rueck:empty{display:none}
.uf-rueck.richtig{background:var(--gruen-hell);border-left:4px solid var(--gruen-rand);padding:8px 12px}
.uf-rueck.falsch{background:var(--rot-hell);border-left:4px solid var(--rot-rand);padding:8px 12px}
.uf-rueck.hinweis{background:var(--papier-2);padding:8px 12px}
.uf-loesung{color:var(--gruen);font-size:1.05rem;padding:4px 2px}
.uf-probe{font-family:var(--sans);font-size:.88rem;color:var(--tinte-2);margin:4px 2px}
.weiter ul{font-family:var(--sans);font-size:.92rem;max-width:68ch}
.weiter li{margin:5px 0}
'''


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf — so rechnet die Bibliothek),
    abgerundet auf Sekunden (HOWTO-leitprogramme §7)."""
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


def umformer_fig(nr, label):
    """Der System-Umformer trägt seine Aufgaben selbst (Aufgabenleiste); die Knoten stehen in umformer.py."""
    return f'''      <figure class="sim lgs-umformer" id="sim{nr}" aria-label="{label}">
        <div class="leiste" aria-live="polite"></div>
        <div class="uf-verlauf" aria-live="polite"></div>
        <p class="uf-frage"></p>
        <div class="uf-wahl"></div>
        <div class="uf-rueck" aria-live="polite"></div>
        <div class="uf-werkzeug"><button type="button" class="uf-zurueck">↶ Schritt zurück</button></div>
      </figure>'''


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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 2.3 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


T = '../grundlagen/g2-3-lineare-gleichungssysteme.html'
L = r'\mathbb{L}'


def mini(k, fenster, xm, ym, titel=None, punkte=None, gross=True, label=None):
    t = f' data-titel="{titel}"' if titel else ''
    p = f' data-punkte="{punkte}"' if punkte else ''
    a = f' aria-label="{label}"' if label else ''
    return f'<svg class="mini{" gross" if gross else ""}" data-k="{k}" data-fenster="{fenster}" data-xm="{xm}" data-ym="{ym}"{t}{p}{a}></svg>'


def sysx(*z):
    """System als LaTeX mit Beschriftungen (I), (II), (III)."""
    lab = ['I', 'II', 'III']
    return r'\begin{cases} ' + r' \\ '.join(g + r' & \text{(' + lab[i] + ')}' for i, g in enumerate(z)) + r' \end{cases}'


# ------------------------------------------------------------------ Kapitel 1
sim1 = '''      <figure class="sim sim-gross" id="sim1" aria-label="Punkt-Sucher: Punkte suchen, die eine Gleichung erfüllen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Koordinatensystem mit dem Punkt P, den gefundenen Punkten und den Geraden"></svg>
        <div class="sl-row">
          <div class="sl-grp"><label for="s1-x"><span class="var">x</span></label><input type="range" id="s1-x" data-p="x" min="-2" max="6" step="0.5" value="0"><span class="sl-val"></span></div>
          <div class="sl-grp"><label for="s1-y"><span class="var">y</span></label><input type="range" id="s1-y" data-p="y" min="-2" max="6" step="0.5" value="0"><span class="sl-val"></span></div>
        </div>
        <p class="sim-legende">Jede Gleichung für sich hat unendlich viele Lösungen — eine ganze Gerade. Die Lösung des Systems ist der Schnittpunkt: das einzige Zahlenpaar, das auf beiden Geraden liegt.</p>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Lineares Gleichungssystem und seine Lösung</div>
          <p>Ein <b>lineares Gleichungssystem</b> besteht aus zwei oder mehr linearen Gleichungen, die <b>gleichzeitig</b> erfüllt werden müssen. Das allgemeine 2×2-System lautet</p>
          <p>\[ \begin{cases} a \cdot x + b \cdot y = c \\ d \cdot x + e \cdot y = f \end{cases} \qquad a, b, c, d, e, f \in \mathbb{R} \]</p>
          <p>Dabei sind \(a\) und \(b\) nicht beide null, ebenso \(d\) und \(e\) — sonst wäre es keine Gleichung mit \(x\) oder \(y\).</p>
          <p>Eine <b>Lösung</b> ist ein Zahlenpaar \((x \mid y)\), das beide Gleichungen erfüllt. Die Lösungsmenge enthält alle solchen Paare, zum Beispiel \(''' + L + r''' = \{(2 \mid 3)\}\).</p>
          <p>Eine einzelne Gleichung wie \(2x + y = 7\) hat unendlich viele Lösungen; im Koordinatensystem bilden sie eine <b>Gerade</b>. Kommt \(y\) vor, löst man nach \(y\) auf: \(y = -2x + 7\). Dann sagt die Zahl vor \(x\), wie steil die Gerade ist (ihre <b>Steigung</b>), die Zahl ohne \(x\), wo sie die \(y\)-Achse schneidet. Fehlt \(y\), etwa bei \(2x = 6\), ist die Gerade die Senkrechte \(x = 3\).</p>
          <p><b>Grafisch lösen:</b></p>
          <ol>
            <li>Jede Gleichung nach \(y\) auflösen (fehlt \(y\): Senkrechte \(x = \ldots\)).</li>
            <li>Je zwei Punkte berechnen und die Gerade zeichnen.</li>
            <li>Den Schnittpunkt ablesen.</li>
            <li><b>Probe</b> in beiden Gleichungen — abgelesene Werte sind Schätzungen.</li>
          </ol>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Probe nur in einer Gleichung: \((5 \mid 1)\) erfüllt \(x - y = 4\), aber nicht \(x + y = 4\) — also keine Lösung des Systems.</p>
          <p>Ablesen ohne Probe: Liegt der Schnittpunkt zwischen den Gitterlinien, ist ein abgelesener Wert nur ungefähr. Erst die Probe zeigt, ob er stimmt.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 2, r'Prüfe, ob \((3 \mid -1)\) eine Lösung von \(' + sysx('2x + 3y = 3', 'x - y = 4') + r'\) ist.',
     r'<p>(I): \(2 \cdot 3 + 3 \cdot (-1) = 6 - 3 = 3\) ✓. (II): \(3 - (-1) = 4\) ✓. Beide stimmen: \((3 \mid -1)\) ist eine Lösung. Die Geraden haben verschiedene Steigungen (\(-\tfrac{2}{3}\) und \(1\)) und schneiden sich nur einmal, also \(' + L + r' = \{(3 \mid -1)\}\).</p>', ''),
    ('1b', 3, r'Löse grafisch und mach die Probe: \(' + sysx('x + y = 7', 'x - 2y = 1') + r'\)',
     r'<p>Nach \(y\) aufgelöst: (I) \(y = -x + 7\), (II) \(y = 0.5x - 0.5\). Punkte zum Zeichnen: (I) \((0 \mid 7)\), \((7 \mid 0)\); (II) \((1 \mid 0)\), \((5 \mid 2)\). Schnittpunkt \((5 \mid 2)\). Probe: \(5 + 2 = 7\) ✓, \(5 - 4 = 1\) ✓. \(' + L + r' = \{(5 \mid 2)\}\).</p>'
     '<div class="mini-reihe">' + mini('g,-1,7,1;g,0.5,-0.5,2', '-1,8,-1,8', '1,2,3,4,5,6,7', '1,2,3,4,5,6,7', punkte='5,2', label='Geraden y = −x + 7 und y = 0.5x − 0.5 mit dem Schnittpunkt (5 | 2)') + '</div>', ''),
    ('1c', 2, r'Abgebildet sind die Geraden zu (I) \(2x - y = 5\) (blau) und (II) \(x + y = 4\) (orange). Lies die Lösung ab und mach die Probe.',
     r'<p>Schnittpunkt \((3 \mid 1)\). Probe: \(6 - 1 = 5\) ✓, \(3 + 1 = 4\) ✓. \(' + L + r' = \{(3 \mid 1)\}\).</p>',
     '\n            <div class="mini-reihe">' + mini('g,2,-5,1;g,-1,4,2', '-1,5,-3,5', '1,2,3,4', '-2,-1,1,2,3,4', label='Geraden zu 2x − y = 5 und x + y = 4') + '</div>'),
    ('1d', 2, r'Warum hat die Gleichung \(x + y = 6\) allein unendlich viele Lösungen, das System aus \(x + y = 6\) und \(x - y = 2\) aber nur eine?',
     r'<p>Zu jedem \(x\) gibt es ein \(y = 6 - x\): unendlich viele Paare, im Bild eine ganze Gerade. Die zweite Gleichung ist eine zweite Gerade; beide Bedingungen zugleich erfüllt nur der Schnittpunkt \((4 \mid 2)\) (\(4 + 2 = 6\), \(4 - 2 = 2\)).</p>', ''),
    ('1e', 3, r'Abgebildet sind die Geraden zu (I) \(2x + y = 5\) (blau) und (II) \(x - y = -1\) (orange). Jemand liest die Lösung \((1 \mid 2)\) ab. Mach die Probe. Was schliesst du daraus?',
     r'<p>(I): \(2 + 2 = 4 \neq 5\) ✗, (II): \(1 - 2 = -1\) ✓. \((1 \mid 2)\) liegt nur auf (II) — keine Lösung des Systems. Der Schnittpunkt liegt zwischen den Gitterlinien, etwa bei \((1.3 \mid 2.3)\); abgelesen ist er nur ungefähr. Genau rechnest du ihn in Kapitel 2: \(\left(\tfrac{4}{3} \mid \tfrac{7}{3}\right)\).</p>',
     '\n            <div class="mini-reihe">' + mini('g,-2,5,1;g,1,1,2', '-1,4,-1,5', '1,2,3', '1,2,3,4', label='Geraden zu 2x + y = 5 und x − y = −1') + '</div>'),
])
k1 = kapitel(1, 'schnittpunkt', 'Lösung und Schnittpunkt', 40,
             r'Du prüfst, ob ein Zahlenpaar ein Gleichungssystem löst, zeichnest jede Gleichung als Gerade und liest die Lösung als Schnittpunkt ab — bestätigt mit der Probe.',
             ('g2-3-lp-schnittpunkt', 'Lösung und Schnittpunkt'), sim1,
             ('g2-3-lp-kontrolle-schnittpunkt', 'Kontrollfragen zu Lösung und Schnittpunkt'),
             fest1, [uebung('paar-pruefen', 'Ist das Paar eine Lösung?'), uebung('nach-y', 'Nach y auflösen')],
             auf1, f'<a href="{T}#definition">Themenseite 2.3, Definition</a> und <a href="{T}#darstellungen">drei Darstellungen</a>', komp='K1 · K2')

# ------------------------------------------------------------------ Kapitel 2
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Einsetzen und Gleichsetzen</div>
          <p><b>Einsetzverfahren</b> — wenn eine Variable allein steht (oder sich leicht freistellen lässt):</p>
          <ol>
            <li>Eine Gleichung nach einer Variablen auflösen.</li>
            <li>Den Term <b>in Klammern</b> in die <b>andere</b> Gleichung einsetzen.</li>
            <li>Die Gleichung mit einer Variablen lösen.</li>
            <li>Den Wert in eine der Gleichungen einsetzen (am einfachsten in die aufgelöste) und den zweiten Wert berechnen.</li>
            <li><b>Probe</b> in beiden Gleichungen.</li>
          </ol>
          <p>\(x - y = -1 \Rightarrow x = y - 1\); in \(2x + y = 7\): \(2(y - 1) + y = 7\), also \(3y = 9\), \(y = 3\) und \(x = 2\).</p>
          <p><b>Gleichsetzverfahren</b> — wenn beide Gleichungen nach derselben Variablen aufgelöst sind: die rechten Seiten gleichsetzen. \(y = 7 - 2x\) und \(y = x + 1\): \(7 - 2x = x + 1\), also \(x = 2\) und \(y = 3\).</p>
          <p>Beide Verfahren <b>eliminieren</b> eine Variable: Es bleibt eine lineare Gleichung mit einer Variablen (GF 2.2a).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Klammer vergessen: \(x = 3y + 2\) in \(2x - y = 9\) gibt \(2(3y + 2) - y = 9\), nicht \(2 \cdot 3y + 2 - y = 9\).</p>
          <p>Den aufgelösten Term in <b>dieselbe</b> Gleichung zurücksetzen: Aus \(2x + y = 7\) und \(y = 7 - 2x\) wird \(2x + 7 - 2x = 7\), also \(7 = 7\) — wahr, aber nutzlos. Der Term gehört in die andere Gleichung.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 15, [
    ('2a', 3, r'Löse mit dem Einsetzverfahren: \(' + sysx('y = 2x - 5', '4x - 3y = 9') + r'\)',
     r'<p>\(4x - 3(2x - 5) = 9\), also \(4x - 6x + 15 = 9\), \(-2x = -6\), \(x = 3\). Dann \(y = 2 \cdot 3 - 5 = 1\). Probe: (I) \(2 \cdot 3 - 5 = 1\) ✓, (II) \(12 - 3 = 9\) ✓. \(' + L + r' = \{(3 \mid 1)\}\).</p><p class="komm">\(-3 \cdot (-5) = +15\): Die Klammer gehört mit dem Minus zusammen.</p>', ''),
    ('2b', 3, r'Löse mit dem Gleichsetzverfahren: \(' + sysx('x = 3y + 4', 'x = -y + 8') + r'\)',
     r'<p>\(3y + 4 = -y + 8\), also \(4y = 4\), \(y = 1\). Dann \(x = 3 + 4 = 7\). Probe: (I) \(3 + 4 = 7\) ✓, (II) \(-1 + 8 = 7\) ✓. \(' + L + r' = \{(7 \mid 1)\}\).</p>', ''),
    ('2c', 2, r'Jemand löst \(y = 5 - x\), \(3x + 2y = 13\) so: «\(3x + 2 \cdot 5 - x = 13\), also \(2x = 3\) und \(x = 1.5\)». Was ist falsch? Löse richtig.',
     r'<p>Die Klammer fehlt: \(2 \cdot (5 - x) = 10 - 2x\). Richtig: \(3x + 10 - 2x = 13\), also \(x = 3\) und \(y = 5 - 3 = 2\). Probe: (I) \(5 - 3 = 2\) ✓, (II) \(9 + 4 = 13\) ✓. \(' + L + r' = \{(3 \mid 2)\}\).</p><p class="komm">Mit \(x = 1.5\), \(y = 3.5\) gibt (II) \(4.5 + 7 = 11.5 \neq 13\) — die Probe hätte den Fehler gezeigt.</p>', ''),
    ('2d', 3, r'Löse: \(' + sysx('3x + y = 5', '5x - 2y = 12') + r'\). Welche Variable stellst du zuerst frei, und warum?',
     r'<p>\(y\) aus (I), denn vor \(y\) steht keine Zahl: \(y = 5 - 3x\). In (II): \(5x - 2(5 - 3x) = 12\), also \(5x - 10 + 6x = 12\), \(11x = 22\), \(x = 2\), \(y = 5 - 6 = -1\). Probe: (I) \(6 - 1 = 5\) ✓, (II) \(10 + 2 = 12\) ✓. \(' + L + r' = \{(2 \mid -1)\}\).</p>', ''),
    ('2e', 2, r'Abgebildet sind die Geraden \(y = 2x - 1\) (blau) und \(y = -x + 4\) (orange). Lies den Schnittpunkt ungefähr ab und berechne ihn exakt mit dem Gleichsetzverfahren.',
     r'<p>Abgelesen etwa \((1.7 \mid 2.3)\). Exakt: \(2x - 1 = -x + 4\), also \(3x = 5\), \(x = \tfrac{5}{3}\), \(y = \tfrac{10}{3} - 1 = \tfrac{7}{3}\). \(' + L + r' = \left\{\left(\tfrac{5}{3} \mid \tfrac{7}{3}\right)\right\}\).</p>',
     '\n            <div class="mini-reihe">' + mini('g,2,-1,1;g,-1,4,2', '-1,4,-2,5', '1,2,3', '-1,1,2,3,4', label='Geraden y = 2x − 1 und y = −x + 4') + '</div>'),
    ('2f', 2, r'Warum liefern Einsetz- und Gleichsetzverfahren für dasselbe System immer dieselbe Lösung?',
     r'<p>Beide Verfahren formen nur äquivalent um und eliminieren dabei eine Variable. Gesucht ist in beiden Fällen dasselbe: das Paar, das beide Gleichungen erfüllt — im Bild der Schnittpunkt der beiden Geraden. Davon gibt es hier genau einen.</p>', ''),
])
k2 = kapitel(2, 'einsetzen', 'Einsetzen und Gleichsetzen', 45,
             r'Du löst Systeme mit dem Einsetz- und dem Gleichsetzverfahren: eine Variable eliminieren, die übrige Gleichung lösen, zurück einsetzen und die Probe machen.',
             ('g2-3-lp-einsetzen', 'Einsetzen und Gleichsetzen'),
             umformer_fig(2, 'System-Umformer: einsetzen und gleichsetzen'),
             ('g2-3-lp-kontrolle-einsetzen', 'Kontrollfragen zum Einsetzen und Gleichsetzen'),
             fest2, [uebung('einsetzen', 'Einsetzverfahren'), uebung('gleichsetzen', 'Gleichsetzverfahren')],
             auf2, f'<a href="{T}#verfahren">Themenseite 2.3, vier Lösungsverfahren</a>; mehr Übung: <a href="../werkzeuge/systemtrainer.html#thema=zwei">Systemtrainer</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 3
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Additionsverfahren und die Wahl des Verfahrens</div>
          <ol>
            <li>Beide Gleichungen <b>ordnen</b>: \(x\) und \(y\) links untereinander, die Zahl rechts.</li>
            <li><b>Vervielfachen</b>, bis vor einer Variablen entgegengesetzt gleiche Zahlen stehen — beide Seiten der Gleichung. Bei gleichen Zahlen subtrahierst du statt zu addieren.</li>
            <li><b>Addieren</b>: Die Variable fällt weg.</li>
            <li>Lösen, zurück einsetzen, <b>Probe</b>.</li>
          </ol>
          <p>\(2x + 3y = 12\) und \(5x - 2y = 11\): \(2 \cdot \text{(I)} + 3 \cdot \text{(II)}\) gibt \(4x + 15x + 6y - 6y = 24 + 33\), also \(19x = 57\), \(x = 3\) und \(y = 2\).</p>
          <p><b>Warum das erlaubt ist:</b> Erfüllt ein Paar beide Gleichungen, dann erfüllt es auch jedes Vielfache mit einer Zahl \(\neq 0\) und die Summe — links und rechts kommt je gleich viel dazu. Beide Schritte lassen sich rückgängig machen (durch die Zahl teilen, die andere Gleichung wieder abziehen); darum kommt auch keine falsche Lösung dazu. Die Lösung ändert sich nicht. Mal \(0\) wäre nicht erlaubt: Aus jeder Gleichung würde \(0 = 0\).</p>
          <div class="tabelle-scroll"><table>
            <tr><th>Form des Systems</th><th>kürzestes Verfahren</th></tr>
            <tr><td>eine Variable steht allein, z. B. \(y = 2x + 3\)</td><td>Einsetzen</td></tr>
            <tr><td>beide nach derselben Variablen aufgelöst</td><td>Gleichsetzen</td></tr>
            <tr><td>geordnet, vor \(x\) oder \(y\) gleiche oder entgegengesetzte Zahlen</td><td>Addition</td></tr>
          </table></div>
          <p>Grafisch lösen gibt einen Überblick, aber nur eine Schätzung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beim Vervielfachen die rechte Seite vergessen: \(2 \cdot (3x - y = 1)\) ergibt \(6x - 2y = 2\), nicht \(6x - 2y = 1\).</p>
          <p>Vorzeichen beim Subtrahieren: \((5x + 2y) - (5x - 3y) = 5y\), denn \(2y - (-3y) = 5y\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 16, [
    ('3a', 3, r'Löse mit dem Additionsverfahren: \(' + sysx('5x + 2y = 1', '3x - 2y = 7') + r'\)',
     r'<p>(I) + (II): \(8x = 8\), \(x = 1\). In (I): \(5 + 2y = 1\), \(y = -2\). Probe: (I) \(5 - 4 = 1\) ✓, (II) \(3 + 4 = 7\) ✓. \(' + L + r' = \{(1 \mid -2)\}\).</p>', ''),
    ('3b', 3, r'Löse: \(' + sysx('2x + 5y = 1', '4x + 3y = 9') + r'\)',
     r'<p>\(2 \cdot \text{(I)} - \text{(II)}\): \(10y - 3y = 2 - 9\), also \(7y = -7\), \(y = -1\). In (I): \(2x - 5 = 1\), \(x = 3\). Probe: (I) \(6 - 5 = 1\) ✓, (II) \(12 - 3 = 9\) ✓. \(' + L + r' = \{(3 \mid -1)\}\).</p>', ''),
    ('3c', 3, r'Löse: \(' + sysx('4x + 3y = 5', '3x - 2y = -9') + r'\). Hier musst du beide Gleichungen vervielfachen.',
     r'<p>\(2 \cdot \text{(I)} + 3 \cdot \text{(II)}\): \(8x + 6y + 9x - 6y = 10 - 27\), also \(17x = -17\), \(x = -1\). In (I): \(-4 + 3y = 5\), \(y = 3\). Probe: (I) \(-4 + 9 = 5\) ✓, (II) \(-3 - 6 = -9\) ✓. \(' + L + r' = \{(-1 \mid 3)\}\).</p>', ''),
    ('3d', 3, r'Welches Verfahren ist am kürzesten? Begründe in einem Satz, ohne zu lösen. (a) \(x = 4 - 2y\), \(3x + 5y = 13\) (b) \(y = 3x + 1\), \(y = -x + 9\) (c) \(6x - 5y = 7\), \(4x + 5y = 13\)',
     r'<p>(a) Einsetzen: In der ersten Gleichung steht \(x\) schon allein. (b) Gleichsetzen: Beide sind nach \(y\) aufgelöst. (c) Addition: Vor \(y\) stehen \(-5\) und \(+5\), beim Addieren fällt \(y\) weg.</p>', ''),
    ('3e', 2, r'Abgebildet sind die Geraden zu (I) \(x + y = 5\) (blau), (II) \(x - y = 1\) (orange) und gestrichelt die Gerade zu \(\text{(I)} + \text{(II)}\). Welche Gleichung hat sie? Warum geht sie durch den Schnittpunkt?',
     r'<p>\(\text{(I)} + \text{(II)}\): \(2x = 6\), also \(x = 3\) — eine Senkrechte. Der Schnittpunkt \((3 \mid 2)\) erfüllt (I) und (II), also auch ihre Summe; darum liegt er auf der neuen Geraden.</p>',
     '\n            <div class="mini-reihe">' + mini('g,-1,5,1;g,1,-1,2;s,3,3,d', '-1,5,-2,5', '1,2,3,4', '-1,1,2,3,4', label='Geraden zu x + y = 5, x − y = 1 und gestrichelt x = 3') + '</div>'),
    ('3f', 2, r'Warum darf man eine Gleichung mit einer Zahl multiplizieren und zur anderen addieren, ohne dass sich die Lösung ändert?',
     r'<p>Erfüllt ein Paar die Gleichung, sind ihre beiden Seiten gleich; mal dieselbe Zahl \(\neq 0\) bleiben sie gleich (mal \(0\) machte aus jeder Gleichung \(0 = 0\) und liesse sich nicht rückgängig machen). Addiert man zwei wahre Gleichungen, kommt links und rechts je gleich viel dazu — die Summe ist für dasselbe Paar wieder wahr. Und weil man beide Schritte rückgängig machen kann (durch die Zahl teilen, wieder abziehen), kommt keine falsche Lösung dazu.</p>', ''),
])
k3 = kapitel(3, 'addition', 'Additionsverfahren und Verfahrenswahl', 45,
             r'Du löst Systeme mit dem Additionsverfahren, auch wenn du zuerst eine oder beide Gleichungen vervielfachen musst, und wählst begründet das kürzeste Verfahren.',
             ('g2-3-lp-addition', 'Additionsverfahren und Verfahrenswahl'),
             umformer_fig(3, 'System-Umformer: Additionsverfahren und Verfahren wählen'),
             ('g2-3-lp-kontrolle-addition', 'Kontrollfragen zum Additionsverfahren'),
             fest3, [uebung('addition', 'Additionsverfahren'), uebung('verfahren-wahl', 'Verfahren wählen')],
             auf3, f'<a href="{T}#verfahren">Themenseite 2.3, vier Lösungsverfahren</a>; Kontrolle mit dem Rechner: <a href="{T}#clip-g2-3-ti30x-sys-solv">Clip «2×2 mit sys-solv lösen»</a>; Strategie üben: <a href="../werkzeuge/strategietrainer.html#bereich=lgs">Strategietrainer</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 4
sim4 = '''      <figure class="sim sim-gross" id="sim4" aria-label="Lösungsfall-Labor: Geraden mit Parameter k">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Familie <select class="sim-wahl" aria-label="Gleichungssystem mit Parameter k">
          <option value="A" selected>A: k in der Konstanten</option>
          <option value="B">B: k vor x in (I)</option>
          <option value="C">C: k in beiden Gleichungen</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Die beiden Geraden des Systems und ihr Schnittpunkt"></svg>
        <div class="sl-row">
          <div class="sl-grp"><label for="s4-k"><span class="var">Parameter k</span></label><input type="range" id="s4-k" data-p="k" min="-8" max="8" step="1" value="1"><span class="sl-val"></span></div>
        </div>
        <p class="sim-legende">Die drei Lösungsfälle sind die drei Lagen zweier Geraden: schneidend (genau eine Lösung), parallel (keine), identisch (unendlich viele).</p>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Drei Lösungsfälle</div>
          <p>Was beim Eliminieren übrig bleibt, entscheidet:</p>
          <ul>
            <li>eine Gleichung wie \(x = 2\): Die Geraden <b>schneiden sich</b> — genau eine Lösung, ein Paar wie \(''' + L + r''' = \{(2 \mid 3)\}\).</li>
            <li>ein Widerspruch wie \(0 = 5\): Die Geraden sind <b>parallel</b> — keine Lösung, \(''' + L + r''' = \{\,\}\).</li>
            <li>die wahre Aussage \(0 = 0\): Die Geraden sind <b>identisch</b> — unendlich viele Lösungen, alle Punkte der Geraden: \(''' + L + r''' = \{(x \mid 2x - 4) : x \in \mathbb{R}\}\).</li>
          </ul>
          <p><b>Ohne das System zu lösen:</b> beide Gleichungen nach \(y\) auflösen (fehlt \(y\) in beiden, sind beide Geraden senkrecht — parallel oder identisch). Verschiedene Steigungen: genau eine Lösung. Gleiche Steigung: parallel oder identisch — das entscheidet die Zahl ohne \(x\). Gleichwertig und immer anwendbar: Ist (II) links ein Vielfaches von (I), haben die Geraden dieselbe Richtung; dann entscheidet die rechte Seite.</p>
          <p><b>Mit Parameter \(k\):</b> \(3x - 6y = 9\) und \(-x + 2y = k\). \(\text{(I)} + 3 \cdot \text{(II)}\) gibt \(0 = 9 + 3k\). Für \(k = -3\) ist das \(0 = 0\): identische Geraden. Für jedes andere \(k\) ein Widerspruch: parallele Geraden. Genau eine Lösung gibt es für kein \(k\), weil beide Geraden die Steigung \(\tfrac{1}{2}\) haben.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bei \(0 = 0\) «\(''' + L + r''' = \mathbb{R}\)» schreiben: Die Lösungen sind Zahlen<b>paare</b>, und nur die Paare auf der gemeinsamen Geraden — nicht jedes Paar.</p>
          <p>Bei \(0 = 5\) «keine Lösung gefunden» schreiben und aufhören: Die Lösungsmenge ist leer, \(''' + L + r''' = \{\,\}\), und das hat eine Bedeutung — die Geraden sind parallel.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 2, r'Löse und deute das Ergebnis geometrisch: \(' + sysx('3x - 2y = 4', '-6x + 4y = 5') + r'\)',
     r'<p>\(2 \cdot \text{(I)} + \text{(II)}\): \(0 = 8 + 5 = 13\), ein Widerspruch. \(' + L + r' = \{\,\}\). Die Geraden \(y = 1.5x - 2\) und \(y = 1.5x + 1.25\) sind parallel.</p>', ''),
    ('4b', 3, r'Löse und gib die Lösungsmenge an: \(' + sysx('3x - y = 2', '-6x + 2y = -4') + r'\)',
     r'<p>\(2 \cdot \text{(I)} + \text{(II)}\): \(0 = 0\), immer wahr. (II) ist das \((-2)\)-Fache von (I): dieselbe Gerade \(y = 3x - 2\). \(' + L + r' = \{(x \mid 3x - 2) : x \in \mathbb{R}\}\).</p><p class="komm">Nicht \(\mathbb{R}\): Lösungen sind nur die Paare auf der Geraden, etwa \((0 \mid -2)\) oder \((1 \mid 1)\).</p>', ''),
    ('4c', 2, r'Ordne zu: Welches Bild gehört zu welchem System? Wie viele Lösungen hat es? (a) \(y = 3x - 1\), \(y = 3x + 2\) (b) \(2x + 4y = 6\), \(x + 2y = 3\) (c) \(x + y = 2\), \(x - y = 4\)',
     r'<p>A gehört zu (b): (I) ist das Doppelte von (II), identische Geraden, unendlich viele Lösungen. B gehört zu (c): verschiedene Steigungen, genau eine Lösung, \((3 \mid -1)\). C gehört zu (a): gleiche Steigung \(3\), verschiedene Achsenabschnitte, parallel, keine Lösung.</p>',
     '\n            <div class="mini-reihe">' + mini('g,-0.5,1.5,1,b;g,-0.5,1.5,2,d', '-3,5,-5,5', '-2,2,4', '-4,-2,2,4', titel='A', gross=False, label='Bild A')
     + mini('g,-1,2,1;g,1,-4,2', '-3,5,-5,5', '-2,2,4', '-4,-2,2,4', titel='B', gross=False, label='Bild B')
     + mini('g,3,-1,1;g,3,2,2', '-3,5,-5,5', '-2,2,4', '-4,-2,2,4', titel='C', gross=False, label='Bild C') + '</div>'),
    ('4d', 3, r'Für welches \(k\) hat \(' + sysx('6x - 3y = k', '-4x + 2y = 2') + r'\) unendlich viele Lösungen, für welche keine? Begründe geometrisch, warum es für kein \(k\) genau eine Lösung gibt.',
     r'<p>\(2 \cdot \text{(I)} + 3 \cdot \text{(II)}\): \(0 = 2k + 6\). \(k = -3\): \(0 = 0\), identische Geraden, unendlich viele Lösungen. \(k \neq -3\): Widerspruch, parallel, keine Lösung. Nach \(y\) aufgelöst: \(y = 2x - \tfrac{k}{3}\) und \(y = 2x + 1\) — beide Steigung \(2\), für jedes \(k\). Geraden mit gleicher Steigung schneiden sich nie in genau einem Punkt.</p>', ''),
    ('4e', 3, r'Für welches \(k\) hat \(' + sysx('kx + 2y = 6', '3x + y = 4') + r'\) keine Lösung? Gibt es ein \(k\) mit unendlich vielen Lösungen?',
     r'<p>(I) ist links ein Vielfaches von (II), wenn \(\tfrac{k}{3} = \tfrac{2}{1}\), also \(k = 6\). Dann ist (I) links das Doppelte von (II), rechts aber \(6 \neq 2 \cdot 4 = 8\): parallel, keine Lösung. Rechnerisch: \(\text{(I)} - 2 \cdot \text{(II)}\) gibt \((k - 6)x = -2\); bei \(k = 6\) steht \(0 = -2\). Unendlich viele Lösungen gibt es für kein \(k\), denn \(0 = -2\) wird nie wahr. Für jedes \(k \neq 6\) genau eine Lösung.</p>', ''),
    ('4f', 3, r'Hier steht \(k\) in beiden Gleichungen: \(' + sysx('kx + y = 2', '4x + ky = 4') + r'\). Für welche \(k\) gibt es keine, für welche unendlich viele Lösungen?',
     r'<p>(II) ist links ein Vielfaches von (I), wenn \(\tfrac{4}{k} = \tfrac{k}{1}\), also \(k^2 = 4\): \(k = 2\) oder \(k = -2\). Rechnerisch: \(k \cdot \text{(I)} - \text{(II)}\) gibt \((k^2 - 4)\,x = 2k - 4\). \(k = 2\): \(0 = 0\); (II) ist das Doppelte von (I), auch rechts (\(4 = 2 \cdot 2\)) — identische Geraden, unendlich viele Lösungen. \(k = -2\): \(0 = -8\); links ist (II) das \((-2)\)-Fache, rechts müsste \(-4\) stehen — parallel, keine Lösung. Jedes andere \(k\): genau eine Lösung (bei \(k = 0\) etwa \((1 \mid 2)\)).</p><p class="komm">Beide kritischen Werte prüfen: Sie geben verschiedene Fälle.</p>', ''),
])
k4 = kapitel(4, 'faelle', 'Keine oder unendlich viele Lösungen', 45,
             r'Du erkennst beim Rechnen und am Bild, ob ein System genau eine, keine oder unendlich viele Lösungen hat, schreibst die Lösungsmenge auf und bestimmst bei einem Parameter \(k\), für welche Werte welcher Fall eintritt.',
             ('g2-3-lp-faelle', 'Keine oder unendlich viele Lösungen'), sim4,
             ('g2-3-lp-kontrolle-faelle', 'Kontrollfragen zu den Lösungsfällen'),
             fest4, [uebung('fall', 'Welcher Lösungsfall?'), uebung('param-k', 'Parameter k')],
             auf4, f'<a href="{T}#loesungsfaelle">Themenseite 2.3, drei Lösungsfälle</a> und <a href="{T}#parameter-k">Für welches k …?</a>', komp='K1 · K2')

# ------------------------------------------------------------------ Kapitel 5
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Systeme mit drei Variablen</div>
          <ol>
            <li>Eine Variable wählen, die sich leicht eliminieren lässt (vor ihr stehen \(1\) oder \(-1\)).</li>
            <li><b>Zweimal</b> dieselbe Variable eliminieren, mit verschiedenen Paaren von Gleichungen. Es bleibt ein 2×2-System.</li>
            <li>Das 2×2-System lösen (Kapitel 2 und 3).</li>
            <li>Zurück einsetzen, um die dritte Variable zu berechnen.</li>
            <li><b>Probe</b> in allen drei Gleichungen.</li>
          </ol>
          <p>\(\text{(I)}\ x + y + z = 6\), \(\text{(II)}\ 2x - y + z = 3\), \(\text{(III)}\ x + 2y - z = 2\): \(\text{(I)} + \text{(III)}\) gibt \(2x + 3y = 8\), \(\text{(II)} + \text{(III)}\) gibt \(3x + y = 5\). Daraus \(x = 1\), \(y = 2\), und aus (I) \(z = 3\): \(''' + L + r''' = \{(1 \mid 2 \mid 3)\}\).</p>
          <p><b>Stufenform:</b> Steht unten nur noch eine Variable, setzt man von unten nach oben ein.</p>
          <p><b>Endaussage:</b> \(0 = 5\) — Widerspruch, keine Lösung, \(''' + L + r''' = \{\,\}\). \(0 = 0\) — diese Gleichung sagt nichts mehr aus. Entsteht nirgends ein Widerspruch, gibt es unendlich viele Lösungen (mindestens eine Variable bleibt frei; die Lösungsmenge dazu steht auf der Themenseite). Ein Widerspruch an anderer Stelle bedeutet trotzdem: keine Lösung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beim zweiten Eliminieren eine andere Variable wegschaffen: Dann bleiben zwei Gleichungen mit verschiedenen Unbekannten — kein 2×2-System.</p>
          <p>Zweimal dasselbe Paar kombinieren, etwa \(\text{(I)} + \text{(II)}\) und \(\text{(I)} - \text{(II)}\): Die dritte Gleichung geht nie in die Rechnung ein. Jede Gleichung muss vorkommen.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 5, r'Löse: \(' + sysx('x + y + z = 2', '2x + y - z = -2', 'x - 2y + z = 11') + r'\)',
     r'<p>\(z\) eliminieren: \(\text{(I)} + \text{(II)}\) gibt \(3x + 2y = 0\) (IV), \(\text{(II)} + \text{(III)}\) gibt \(3x - y = 9\) (V). \(\text{(IV)} - \text{(V)}\): \(3y = -9\), \(y = -3\). In (V): \(3x + 3 = 9\), \(x = 2\). In (I): \(2 - 3 + z = 2\), \(z = 3\). Probe: (I) \(2 - 3 + 3 = 2\) ✓, (II) \(4 - 3 - 3 = -2\) ✓, (III) \(2 + 6 + 3 = 11\) ✓. \(' + L + r' = \{(2 \mid -3 \mid 3)\}\).</p>', ''),
    ('5b', 3, r'Löse: \(' + sysx('x + 2y = 7', 'y - z = 1', 'x + z = 4') + r'\). In jeder Gleichung fehlt eine Variable.',
     r'<p>Aus (II): \(y = z + 1\); aus (III): \(x = 4 - z\). In (I): \(4 - z + 2(z + 1) = 7\), also \(z + 6 = 7\), \(z = 1\). Dann \(y = 2\), \(x = 3\). Probe: (I) \(3 + 4 = 7\) ✓, (II) \(2 - 1 = 1\) ✓, (III) \(3 + 1 = 4\) ✓. \(' + L + r' = \{(3 \mid 2 \mid 1)\}\).</p>', ''),
    ('5c', 2, r'Löse das System in Stufenform: \(' + sysx('2x - y + z = 5', '3y - z = 4', '2z = 4') + r'\)',
     r'<p>(III): \(z = 2\). (II): \(3y - 2 = 4\), \(y = 2\). (I): \(2x - 2 + 2 = 5\), \(x = 2.5\). \(' + L + r' = \{(2.5 \mid 2 \mid 2)\}\).</p>', ''),
    ('5d', 2, r'Zeige, dass \(' + sysx('x + y - z = 1', '2x + y + z = 4', '3x + 2y = 7') + r'\) keine Lösung hat.',
     r'<p>\(\text{(I)} + \text{(II)}\): \(3x + 2y = 5\). Mit (III): \(3x + 2y = 7\). Subtrahieren: \(0 = 2\), ein Widerspruch. \(' + L + r' = \{\,\}\).</p>', ''),
    ('5e', 2, r'Warum muss man beim zweiten Eliminieren dieselbe Variable wegschaffen wie beim ersten?',
     r'<p>Nur dann stehen in beiden neuen Gleichungen dieselben zwei Variablen — ein 2×2-System, das man lösen kann. Fällt einmal \(z\) und einmal \(y\) weg, hat man zwei Gleichungen mit drei verschiedenen Unbekannten und ist nicht weiter.</p>', ''),
])
k5 = kapitel(5, 'drei', 'Drei Variablen', 40,
             r'Du löst ein lineares Gleichungssystem mit drei Variablen, indem du schrittweise eliminierst, bis ein 2×2-System bleibt, und erkennst an einem Widerspruch, dass es keine Lösung gibt.',
             ('g2-3-lp-drei', 'Drei Variablen: zurück auf zwei'),
             umformer_fig(5, 'System-Umformer: drei Variablen'),
             ('g2-3-lp-kontrolle-drei', 'Kontrollfragen zu drei Variablen'),
             fest5, [uebung('stufe', 'Stufenform'), uebung('eliminieren', 'Eine Variable eliminieren')],
             auf5, f'<a href="{T}#dreidim">Themenseite 2.3, 3×3-Systeme</a>; mehr Übung: <a href="../werkzeuge/systemtrainer.html#thema=drei">Systemtrainer</a>', komp='K1')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 2.1 · 2.2a</span><span class="zeit">≈ 15 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Lineare Gleichungen lösen, eine Gleichung nach einer Variablen auflösen, Zahlen einsetzen. Wenn das wackelt: <a href="lineare-gleichungen.html">Leitprogramm Lineare Gleichungen</a> und <a href="../grundlagen/g2-2a-lineare-gleichungen.html">Themenseite 2.2a</a>.</p>
      ''' + clipkarte('g2-2a-minus-vor-klammer', 'Lineare Gleichungen: Minus vor der Klammer') + '''
''' + test('t0', 'Vortest', 12, [
    ('0a', 3, r'Löse \(5x - 2(x + 3) = 9\) und mach die Probe.',
     r'<p>\(5x - 2x - 6 = 9\), \(3x = 15\), \(x = 5\). Probe: \(25 - 2 \cdot 8 = 9\) ✓. \(' + L + r' = \{5\}\).</p><p class="komm">Das Minus vor der Klammer und die Probe brauchst du in jedem Kapitel.</p>', ''),
    ('0b', 3, r'Löse nach \(y\) auf: (a) \(3x + y = 8\) (b) \(2x - 4y = 6\)',
     r'<p>(a) \(y = -3x + 8\). (b) \(-4y = 6 - 2x\), also \(y = 0.5x - 1.5\).</p><p class="komm">Falsch? Genau das braucht Kapitel 1 zum Zeichnen und Kapitel 2 zum Einsetzen.</p>', ''),
    ('0c', 2, r'Berechne für \(y = -2x + 3\) die Punkte mit \(x = 0\), \(1\), \(2\), zeichne sie in ein Koordinatensystem und verbinde sie. Liegt \((3 \mid -3)\) auf dieser Geraden?',
     r'<p>\((0 \mid 3)\), \((1 \mid 1)\), \((2 \mid -1)\) — sie liegen auf einer Geraden. \(-2 \cdot 3 + 3 = -3\): ja, \((3 \mid -3)\) liegt darauf.</p>'
     '<div class="mini-reihe">' + mini('g,-2,3,1', '-2,4,-4,4', '-1,1,2,3', '-3,-2,-1,1,2,3', punkte='0,3;1,1;2,-1;3,-3', label='Gerade y = −2x + 3 mit den Punkten (0 | 3), (1 | 1), (2 | −1), (3 | −3)') + '</div><p class="komm">Punkte berechnen und eine Gerade zeichnen braucht Kapitel 1.</p>', ''),
    ('0d', 2, r'Multipliziere beide Seiten der Gleichung \(2x - 3y = 5\) mit \(-3\).',
     r'<p>\(-6x + 9y = -15\).</p><p class="komm">Jedes Glied und die rechte Seite — das braucht Kapitel 3.</p>', ''),
    ('0e', 2, r'Fasse zusammen: \((3x + 2y) + (x - 2y)\) und \((5x + y) - (5x - 3y)\).',
     r'<p>\(4x\); \(4y\).</p><p class="komm">Das Minus vor der zweiten Klammer dreht beide Vorzeichen.</p>', ''),
]) + '''
      <p class="komm">Weniger als 8 von 12 Punkten: zuerst das Leitprogramm Lineare Gleichungen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/gleichungssysteme/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 2.3 · Kapitel 1–5</span><span class="zeit">≈ 25 min · 25 Punkte</span></div>
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Tüfteln und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1 (Bestätigung 2 oder 3); G2 → 4; G3 → 1 und 4; G4 → 2 und 3; G5, G6 → 3; G7 → 4; G8 → 5 (b auch 4)</p>
        </div>
      </div>
    </section>

    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Wie weiter?</h2>
      <ul>
        <li><b>Textaufgaben mit Gleichungssystemen</b> — Ansatz finden, Mischungen, Verteilungen: <a href="modellieren.html">Leitprogramm Textaufgaben modellieren</a> (GF 2.M).</li>
        <li><b>Geraden als Funktionen</b> — Steigung, Achsenabschnitt, Schnittpunkte: <a href="lineare-funktionen.html">Leitprogramm Lineare Funktionen</a> (GF 3.2).</li>
        <li><b>Nicht in diesem Leitprogramm</b>, auf der <a href="{T}">Themenseite 2.3</a>: Systeme, die erst durch Substitution linear werden (\\(x\\) im Nenner, <a href="{T}#substitution">Abschnitt</a>), Auflösen nach \\(x\\) und \\(y\\) mit Parameter samt Fallunterscheidung (<a href="{T}#parameter-aufloesen">Abschnitt</a>), die Lösungsmenge eines 3×3-Systems mit freier Variablen (<a href="{T}#dreidim">Abschnitt</a>).</li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Lineare Gleichungssysteme, Version 1.0 (11.10.2026). Gebaut aus
     scripts/lp/gleichungssysteme/seite.py — Änderungen dort, nicht in dieser Datei. Ersetzt das ältere,
     klassische Leitprogramm «Gleichungssysteme» unter derselben Adresse (es bleibt in der Git-Geschichte).
     Grundlage: HOWTO-leitprogramme.md (Kapitelmuster §4, Umformer §8d), Themenseite g2-3.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 2.3 «Lineare Gleichungssysteme», wörtlich wie in der RLP-Box
     der Themenseite:
       K1  «ein lineares Gleichungssystem mit maximal drei Variablen lösen» (auch ohne Hilfsmittel)
       K2  «die Lösungsmenge eines linearen Gleichungssystems mit zwei Variablen grafisch veranschaulichen
            und interpretieren» (auch ohne Hilfsmittel)
     Beide «auch ohne Hilfsmittel»: Gesamttest ganz ohne Taschenrechner. Der Rechner (sys-solv) nur als
     Hinweis «Kontrolle mit dem Rechner» in Kapitel 3 (HOWTO §7).

     Kompetenzmatrix (Kompetenz | ohne HM | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | ja | 1 (Lösung prüfen), 2, 3, 4 (Rechnung), 5 | 1a, 2a–2f, 3a–3f, 4a, 4b, 4d–4f, 5a–5e | G1 (Bestätigung), G2, G4, G5, G6, G7, G8
       K2 | ja | 1, 4                                     | 1b–1e, 2e, 3e, 4a–4f                 | G1, G2, G3, G7
     Gesamttest: Teil A (Kapitel 1, 4) G1–G3 8 P · Teil B (Kapitel 2, 3) G4–G6 8 P · Teil C (Kapitel 4, 5) G7, G8 9 P = 25 P,
     alles ohne Taschenrechner. Jede Aufgabe kombiniert Geübtes neu: zeichnen und bestätigen (G1), Lösungsmenge mit
     Dezimalzahl (G2), Lösungsfall am Bild und Begründung (G3), Gleichsetzen bei nach x aufgelösten Gleichungen mit Wahl
     (G4), erst ordnen, dann beide vervielfachen (G5), Fehler finden (G6), k in beiden Gleichungen plus Lösung für k = 0
     (G7, geübt in 4f und Labor C), 3×3 mit Gleichung ohne z plus Widerspruch mit Zahl c (G8). Nach der Prüfung vom 12.10.2026.

     Planung (Kapitel | Lernziel | Kompetenz | Clips | Tüfteln | Beispiel (Quelle) | häufiger Fehler | min):
       0 Vorwissen  | Gleichung lösen, auflösen, einsetzen | 2.1/2.2a | g2-2a-minus-vor-klammer | — | Vortest | Minus vor Klammer | 15
       1 Lösung und Schnittpunkt | Paar prüfen, Gerade, Schnittpunkt, Probe | K1 K2 | g2-3-lp-schnittpunkt, -kontrolle-schnittpunkt
         | Punkt-Sucher (§8b) | 2x + y = 7, x − y = −1 (Themenseite «Drei Darstellungen») | Probe nur in einer Gleichung | 40
       2 Einsetzen und Gleichsetzen | eliminieren, zurück einsetzen | K1 | g2-3-lp-einsetzen, -kontrolle-einsetzen
         | System-Umformer (§8d) | dasselbe System (Themenseite «Drei analytische Verfahren») | Klammer vergessen; dieselbe Gleichung | 45
       3 Additionsverfahren und Verfahrenswahl | vervielfachen, addieren, Verfahren begründen | K1 | g2-3-lp-addition, -kontrolle-addition
         | System-Umformer | 2x + 3y = 12, 5x − 2y = 11 | rechte Seite nicht vervielfacht; Vorzeichen beim Subtrahieren | 45
       4 Keine oder unendlich viele Lösungen | 0 = 5 / 0 = 0 deuten, Steigung vergleichen, Parameter k | K1 K2 | g2-3-lp-faelle, -kontrolle-faelle
         | Lösungsfall-Labor (§8b) | x + y = 3/x + y = 5 (Mini-Check), 2x − y = 4/−4x + 2y = −8 (A5), 3x − 6y = 9/−x + 2y = k (Beispiel 1)
         | 𝕃 = ℝ statt Paarmenge | 45
       5 Drei Variablen | zweimal dieselbe Variable eliminieren, Stufenform, 0 = 5 | K1 | g2-3-lp-drei, -kontrolle-drei
         | System-Umformer | x + y + z = 6, 2x − y + z = 3, x + 2y − z = 2 (Themenseite «3×3 schrittweise») | andere Variable beim zweiten Mal | 40
       Gesamttest 25 · Summe 255 min ≈ 5.7 Lektionen (fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest).

     Kern / weggelassen (→ Themenseite): nicht lineare Systeme mit Substitution (#substitution, gehen über «lineares
     Gleichungssystem» hinaus), Auflösen mit Parameter und Fallunterscheidung (#parameter-aufloesen), Lösungsmenge
     eines 3×3-Systems mit freier Variablen und Ebenen im Raum (#dreidim), Textaufgaben (LP Modellieren, GF 2.M).
     Parameter k nur, um die Lösungsfälle zu deuten (K2: «interpretieren»).

     Konventionen der Themenseite: 𝕃 = {(2 | 3)}, leer {}, unendlich viele {(x | 2x − 4) : x ∈ ℝ}, Tripel (1 | 2 | 3);
     Einsetz-, Gleichsetz-, Additionsverfahren; Lösungsfälle eindeutig / keine / unendlich viele; Steigung von
     a·x + b·y = c nach y aufgelöst; Gleichungen (I), (II), (III). Im LaTeX ohne Malpunkt (2x statt 2 · x, STYLEGUIDE §2.1).
     Abweichung, bewusst: Die Themenseite schreibt im 3×3-Teil G1, G2, G3 und {(t | t | 6 − 2t) | t ∈ ℝ}; hier
     durchgehend (I), (II), (III) und, wo nötig, der Doppelpunkt wie im 2×2-Teil der Themenseite.
     Farben: Gleichung (I) blau, Gleichung (II) orange, Lösung grün, Fehler rot, Umformungsschritte und k neutral.

     Muster je Kapitel: ① Einführungsclip → ② Simulation bzw. System-Umformer mit Aufgabenleiste → ③ Kontrollclip
     mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF aus LaTeX (downloads/leitprogramme/gleichungssysteme/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Lineare Gleichungssysteme</h1>
      <p class="unter">Zuschauen, Schritte wählen, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 2.3</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Schnittpunkt</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Einsetzen, Gleichsetzen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Addition</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Lösungsfälle</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Drei Variablen</span></a></li>
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
          <li><b>② Tüfteln:</b> In Kapitel 1 und 4 ziehst du an Reglern, in Kapitel 2, 3 und 5 wählst du im System-Umformer jeden Schritt selbst und gibst am Schluss die Lösungsmenge ein. Die Aufgabenleiste zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 2.3:</p>
        <ul>
          <li><b>K1</b> ein lineares Gleichungssystem mit maximal drei Variablen lösen <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1 bis 5</li>
          <li><b>K2</b> die Lösungsmenge eines linearen Gleichungssystems mit zwei Variablen grafisch veranschaulichen und interpretieren <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1 und 4</li>
        </ul>
        <p class="rlp-quelle">Der Parameter \\(k\\) in Kapitel 4 dient dazu, die Lösungsfälle zu deuten (K2). Nicht hier, sondern auf der <a href="''' + T + '''">Themenseite 2.3</a>: Systeme, die erst durch Substitution linear werden, und das Auflösen mit Parameter. Textaufgaben: <a href="modellieren.html">Leitprogramm Modellieren</a>.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Lineare Gleichungssysteme · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (12.10.2026, nach der Prüfung): Vorwissen 15 · K1 40 · K2 45 · K3 45 · K4 45 · K5 40 · Gesamttest 25 = 255 min
ZEITEN = [15, 40, 45, 45, 45, 40, 25]
assert sum(ZEITEN) == 255

js = open(SP + 'seite.js').read()
js = js.replace('/*@UMFORMER@*/null', umformer.als_json())
js = js.replace('/*@SPERRE@*/{ sys: [], gl: [], pk: [] }', json.dumps(zahlen.sperre(), ensure_ascii=False))
assert '/*@' not in js
b = umformer.pruefen()
assert not b, b

body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + js + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
