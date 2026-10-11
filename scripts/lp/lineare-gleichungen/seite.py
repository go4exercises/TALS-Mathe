"""Baut leitprogramme/lineare-gleichungen.html aus einer Kapitelbeschreibung (11.10.2026).

  python3 scripts/lp/lineare-gleichungen/seite.py

Leitprogramm zur Themenseite GF 2.2a (grundlagen/g2-2a-lineare-gleichungen.html). Liest Kopf (inkl. <style>)
und Grundskript aus der bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js) und schreibt die Seite neu.
Beim ersten Lauf kommt das Gerüst aus leitprogramme/lineare-quadratische-gleichungen.html, mit eigenem Titel und
eigenen localStorage-Schlüsseln (lp-lineare-gleichungen-thema, lp-lineare-gleichungen-stand).
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und python3 scripts/build-seo.py
(Footer und SEO-Kopf). Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/lineare-gleichungen.html'
NAME = 'Lineare Gleichungen'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/lineare-quadratische-gleichungen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Lineare und quadratische Gleichungen</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-gleichungen-', 'lp-lineare-gleichungen-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Gleichungen (06.10.2026)', '\n/* ════════ Lineare Gleichungen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Lineare und quadratische Gleichungen —'),
                    alt.find('<script>\n/* Leitprogramm Lineare Gleichungen —')) if k > 0)
basis = alt[i:j]
# Footer erzeugt scripts/build-seo.py (seit 10.10.2026): hier nur leere FUSS-Marken.
fuss = alt[alt.index('<!-- FUSS:ANFANG'):]
fuss = re.sub(r'<!-- FUSS:ANFANG.*?<!-- FUSS:ENDE -->',
              lambda _: '<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n<!-- FUSS:ENDE -->',
              fuss, count=1, flags=re.S)

CSS = '''
/* ════════ Lineare Gleichungen (11.10.2026) — Kapitelmuster wie die Funktionen-Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg, Umformer) wie im Leitprogramm Lineare und
   quadratische Gleichungen. Farben: Gleichung und linke Seite blau, Umformung und rechte Seite orange,
   Lösungen grün, Fehler rot, Differenz links − rechts Tinte. */
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
.sim .kurve.diff{stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:2 3}
.sim .senk{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:3 3}
.p-loes{fill:var(--gruen)} .p-links{fill:var(--blau)} .p-rechts{fill:var(--orange)} .p-diff{fill:var(--tinte-2)}
svg.mini .kurve.k1{stroke:var(--orange);stroke-dasharray:6 3}   /* rechte Seite gestrichelt wie in den Simulationen — deckungsgleiche Geraden bleiben sichtbar */ svg.mini .kurve.k2{stroke:var(--gruen)}
.nb{white-space:nowrap}
/* Umformer: Verlauf wie im Heft — Gleichung links, Umformung rechts daneben. */
.umformer{max-width:720px;margin:10px auto 6px}
.uf-verlauf{display:grid;grid-template-columns:minmax(0,auto) auto;justify-content:start;gap:2px 22px;padding:10px 14px;
  border:1px solid var(--linie);border-radius:9px;background:var(--karte);min-height:2.6em;overflow-x:auto}
.uf-zeile{display:contents}
.uf-gl{color:var(--blau)}
.uf-op{color:var(--orange);font-size:.95em}
.uf-frage{font-family:var(--sans);font-size:.88rem;color:var(--tinte-2);margin:10px 2px 6px}
.uf-wahl{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.uf-knopf{font-family:var(--sans);font-size:.88rem;cursor:pointer;border-radius:8px;padding:6px 12px;border:1.5px solid var(--orange-rand);
  background:var(--orange-hell);color:var(--tinte);text-align:left;max-width:100%}
.uf-knopf:hover,.uf-knopf:focus-visible{border-color:var(--orange);outline:none}
.uf-feld{font-family:var(--mono);font-size:.95rem;display:inline-flex;flex-wrap:wrap;align-items:center;gap:4px}
.uf-feld input{width:4.2em;font-family:var(--mono);font-size:.95rem;padding:4px 6px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.uf-feld input.uf-menge{width:9em}
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
.sim-wahl{font-family:var(--sans);font-size:.88rem;padding:4px 8px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.wertetab{border-collapse:collapse;font-family:var(--sans);font-size:.9rem;margin:6px 0}
.wertetab td,.wertetab th{border:1px solid var(--linie);padding:3px 10px;text-align:center}
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


def umformer(nr, label):
    """Der Umformer trägt seine Aufgaben selbst (Aufgabenleiste); die Knoten stehen in seite.js."""
    return f'''      <figure class="sim umformer" id="sim{nr}" aria-label="{label}">
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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp, phase2='Tüfteln'):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 2.2a · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> {phase2}</p>
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


def mini(k, fenster, xm, ym, titel=None, gross=True, **extra):
    att = ''.join(f' data-{a}="{v}"' for a, v in extra.items())
    t = f' data-titel="{titel}"' if titel else ''
    return f'<svg class="mini{" gross" if gross else ""}" data-k="{k}" data-fenster="{fenster}" data-xm="{xm}" data-ym="{ym}"{t}{att}></svg>'


def minireihe(*svgs):
    return '\n            <div class="mini-reihe">' + ''.join(svgs) + '</div>'


TA = '../grundlagen/g2-2a-lineare-gleichungen.html'
L = r'\mathbb{L}'

# ------------------------------------------------------------------ Kapitel 1
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Äquivalenzumformungen</div>
          <p>Eine <b>Äquivalenzumformung</b> ändert die Lösungsmenge nicht: auf beiden Seiten dieselbe Zahl oder denselben Term addieren oder subtrahieren, beide Seiten mit derselben Zahl \(\neq 0\) multiplizieren oder durch sie dividieren. Jede lässt sich rückgängig machen.</p>
          <p>Eine <b>lineare Gleichung</b> in einer Variablen lässt sich durch Äquivalenzumformungen auf die Form \(a \cdot x + b = 0\) mit \(a \neq 0\) bringen; \(x\) kommt nur in der ersten Potenz vor — kein \(x^2\), kein \(x\) im Nenner (Themenseite, Definition).</p>
          <p><b>Strategie</b> (Themenseite, Lösungsverfahren):</p>
          <ol>
            <li>Alle \(x\)-Glieder auf eine Seite, alle Zahlen auf die andere.</li>
            <li>Zusammenfassen.</li>
            <li>Durch den Faktor vor \(x\) dividieren, samt Vorzeichen: Aus \(-x = -6\) wird \(x = 6\).</li>
            <li><b>Probe</b> in der ursprünglichen Gleichung: Beide Seiten müssen denselben Wert ergeben.</li>
          </ol>
          <p>\[ 5x - 7 = 2x + 8 \;\;\Longleftrightarrow\;\; 3x = 15 \;\;\Longleftrightarrow\;\; x = 5, \qquad ''' + L + r''' = \{5\} \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Vorzeichen beim Hinüberbringen: Aus \(2x + 5 = 11\) wird \(2x = 11 - 5\), nicht \(2x = 11 + 5\). Wer die Umformung hinschreibt (\(\mid -5\)), läuft selten in diese Falle.</p>
          <p>Mit \(0\) multiplizieren ist keine Äquivalenzumformung: Aus jeder Gleichung wird \(0 = 0\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 2, r'Löse \(4x + 11 = 9x - 4\) und mach die Probe.',
     r'<p>\(\mid -9x\): \(-5x + 11 = -4\); \(\mid -11\): \(-5x = -15\); \(\mid :(-5)\): \(x = 3\). Probe: \(4 \cdot 3 + 11 = 23\) und \(9 \cdot 3 - 4 = 23\) ✓. \(' + L + r' = \{3\}\).</p>', ''),
    ('1b', 2, r'Löse \(8 - 3x = x - 12\) und mach die Probe.',
     r'<p>\(\mid +3x\): \(8 = 4x - 12\); \(\mid +12\): \(20 = 4x\); \(\mid :4\): \(x = 5\). Probe: \(8 - 15 = -7\) und \(5 - 12 = -7\) ✓. \(' + L + r' = \{5\}\).</p>', ''),
    ('1c', 3, r'Jemand rechnet: «\(2x + 5 = 11 \Rightarrow 2x = 16 \Rightarrow x = 8\)». Mach die Probe, finde den Fehler und löse richtig.',
     r'<p>Probe: \(2 \cdot 8 + 5 = 21 \neq 11\), also ist \(8\) keine Lösung. Fehler: Die \(5\) wurde addiert statt subtrahiert. Richtig: \(\mid -5\): \(2x = 6\), \(x = 3\). Probe: \(6 + 5 = 11\) ✓. \(' + L + r' = \{3\}\).</p><p class="komm">Die Probe in der Ausgangsgleichung deckt jeden Rechenfehler auf.</p>', ''),
    ('1d', 2, r'Löse \(1.2x + 0.4 = 0.2x - 2.6\).',
     r'<p>\(\mid -0.2x\): \(x + 0.4 = -2.6\); \(\mid -0.4\): \(x = -3\). Probe: \(-3.6 + 0.4 = -3.2\) und \(-0.6 - 2.6 = -3.2\) ✓. \(' + L + r' = \{-3\}\).</p>', ''),
    ('1e', 2, r'Warum darf man beide Seiten durch \(4\) teilen, aber nicht mit \(0\) multiplizieren?',
     r'<p>Teilen durch \(4\) lässt sich mit «mal \(4\)» rückgängig machen; die Lösungsmenge bleibt gleich. Mal \(0\) macht aus jeder Gleichung \(0 = 0\), wahr für jedes \(x\): Die Lösungsmenge kann sich ändern (aus \(\{3\}\) würde \(\mathbb{R}\)), und zurück geht es nicht, weil man durch \(0\) nicht teilen kann.</p>', ''),
    ('1f', 2, r'Abgebildet sind die beiden Seiten von \(3x - 2 = x + 2\) als Geraden \(y = 3x - 2\) (blau) und \(y = x + 2\) (orange). Lies die Lösung ab. Was wird nach «beidseitig \(-x\)» aus den beiden Geraden, und wo schneiden sie sich dann?',
     r'<p>Schnittpunkt \((2 \mid 4)\): \(x = 2\). Nach \(\mid -x\) steht \(2x - 2 = 2\): die Geraden \(y = 2x - 2\) und \(y = 2\). Sie schneiden sich in \((2 \mid 2)\), also wieder bei \(x = 2\). Die Umformung ändert die Höhe, aber nicht die Lösung.</p>',
     minireihe(mini('g,3,-2;g,1,2', '-1,4,-3,7', '1,2,3', '2,4,6'))),
])
k1 = kapitel(1, 'umformen', 'Äquivalenzumformungen und Probe', 40,
             r'Du löst lineare Gleichungen mit Äquivalenzumformungen — \(x\)-Glieder auf eine Seite, Zahlen auf die andere, durch den Faktor vor \(x\) teilen — und machst die Probe in der Ausgangsgleichung.',
             ('g2-2a-lp-umformen', 'Umformen wie an der Waage'),
             umformer(1, 'Umformer: lineare Gleichungen Schritt für Schritt lösen'),
             ('g2-2a-lp-kontrolle-umformen', 'Kontrollfragen zum Umformen'),
             fest1, [uebung('zweischritt', 'Zwei Schritte bis x'), uebung('linear-loesen', 'x auf beiden Seiten')],
             auf1, f'<a href="{TA}#verfahren">Themenseite 2.2a, Lösungsverfahren</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 2
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zuerst aufräumen: Klammern und Brüche</div>
          <ol>
            <li><b>Klammern auflösen:</b> Der Faktor vor der Klammer multipliziert jedes Glied, \(4(x - 2) = 4x - 8\). Ein Minus vor der Klammer dreht jedes Vorzeichen in der Klammer: \(5 - 2(x + 1) = 5 - 2x - 2\).</li>
            <li><b>Brüche wegschaffen:</b> beide Seiten mit dem Hauptnenner (dem kleinsten gemeinsamen Vielfachen der Nenner) multiplizieren — <b>jedes</b> Glied, auch die Zahlen ohne Bruch. Ein Bruchstrich wirkt wie eine Klammer: \(6 \cdot \tfrac{x + 1}{3} = 2(x + 1)\).</li>
            <li>Dann sortieren, teilen und die Probe machen wie in Kapitel 1.</li>
          </ol>
          <p>\[ \frac{x}{3} + 2 = \frac{x}{2} - 1 \;\;\Big|\, \cdot 6 \qquad 2x + 12 = 3x - 6 \;\;\Longleftrightarrow\;\; x = 18 \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur das erste Glied multiplizieren: \(2(x - 3)\) ist \(2x - 6\), nicht \(2x - 3\). Und beim Minus vor der Klammer: \(-(x - 3) = -x + 3\).</p>
          <p>Beim Hauptnenner nur die Brüche multiplizieren: Aus \(\tfrac{x}{3} + 2\) wird mal \(6\) die Summe \(2x + 12\), nicht \(2x + 2\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'Löse \(3(x - 2) = 2x + 1\) und mach die Probe.',
     r'<p>\(3x - 6 = 2x + 1\), \(\mid -2x\), \(\mid +6\): \(x = 7\). Probe: \(3 \cdot 5 = 15\) und \(2 \cdot 7 + 1 = 15\) ✓. \(' + L + r' = \{7\}\).</p>', ''),
    ('2b', 3, r'Löse \(4 - 2(3 - x) = 3(x - 1)\).',
     r'<p>\(4 - 6 + 2x = 3x - 3\), also \(-2 + 2x = 3x - 3\); \(\mid -2x\), \(\mid +3\): \(1 = x\). Probe: \(4 - 2 \cdot 2 = 0\) und \(3 \cdot 0 = 0\) ✓. \(' + L + r' = \{1\}\).</p><p class="komm">Das Minus vor \(2(3 - x)\) gilt für beide Glieder: \(-6 + 2x\).</p>', ''),
    ('2c', 3, r'Löse \(\dfrac{x}{2} - \dfrac{x - 3}{4} = 1\).',
     r'<p>Mal \(4\): \(2x - (x - 3) = 4\), also \(2x - x + 3 = 4\), \(x + 3 = 4\), \(x = 1\). Probe: \(\tfrac{1}{2} - \tfrac{-2}{4} = \tfrac{1}{2} + \tfrac{1}{2} = 1\) ✓. \(' + L + r' = \{1\}\).</p><p class="komm">Der Bruchstrich klammert: Das Minus gilt für den ganzen Zähler \(x - 3\).</p>', ''),
    ('2d', 2, r'Jemand rechnet: «\(\tfrac{x}{3} + 2 = \tfrac{x}{4}\), mal \(12\): \(4x + 2 = 3x\), also \(x = -2\)». Was ist falsch? Löse richtig.',
     r'<p>Die \(2\) wurde nicht mit \(12\) multipliziert. Richtig: \(4x + 24 = 3x\), \(x = -24\). Probe: \(-8 + 2 = -6\) und \(\tfrac{-24}{4} = -6\) ✓. \(' + L + r' = \{-24\}\).</p>', ''),
    ('2e', 2, r'Warum muss man bei «beidseitig mal \(6\)» auch die Zahlen ohne Bruch mit \(6\) multiplizieren?',
     r'<p>Multipliziert wird die ganze Seite, also jedes Glied (Distributivgesetz). Nimmt man nur die Brüche mal \(6\), ist die linke Seite nicht mehr das Sechsfache der alten — das ist keine Äquivalenzumformung, und die Lösung ändert sich.</p>', ''),
    ('2f', 2, r'Abgebildet sind \(y = 2(x - 1)\) (blau) und \(y = -(x - 4)\) (orange). Lies die Lösung von \(2(x - 1) = -(x - 4)\) ab und bestätige sie rechnerisch.',
     r'<p>Die Geraden schneiden sich in \((2 \mid 2)\): \(x = 2\). Rechnung: \(2x - 2 = -x + 4\), \(3x = 6\), \(x = 2\). Beide Seiten ergeben \(2\).</p>',
     minireihe(mini('g,2,-2;g,-1,4', '-1,5,-3,5', '1,2,3,4', '2,4'))),
])
k2 = kapitel(2, 'klammern', 'Klammern und Brüche', 40,
             r'Du löst Gleichungen mit Klammern und Brüchen: Klammern auflösen — auch mit einem Minus davor —, mit dem Hauptnenner multiplizieren und erst dann sortieren.',
             ('g2-2a-lp-klammern', 'Klammern und Brüche'),
             umformer(2, 'Umformer: Klammern auflösen, Brüche wegschaffen, lösen'),
             ('g2-2a-lp-kontrolle-klammern', 'Kontrollfragen zu Klammern und Brüchen'),
             fest2, [uebung('klammer', 'Klammer auflösen und lösen'), uebung('nenner', 'Mit dem Hauptnenner lösen')],
             auf2, f'<a href="{TA}#verfahren">Themenseite 2.2a, Lösungsverfahren (Beispiel mit Brüchen)</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Drei Lösungsfälle</div>
          <p>Sortiert man alle \(x\)-Glieder nach links und alle Zahlen nach rechts, entsteht \(a \cdot x = c\). Dann entscheidet \(a\):</p>
          <ul>
            <li>\(a \neq 0\): genau eine Lösung, \(''' + L + r''' = \{\tfrac{c}{a}\}\). Die Geraden der beiden Seiten schneiden sich.</li>
            <li>\(a = 0\), \(c \neq 0\): Es bleibt eine falsche Aussage wie \(6 = 9\), \(''' + L + r''' = \{\,\}\). Die Geraden sind parallel.</li>
            <li>\(a = 0\), \(c = 0\): Es bleibt eine wahre Aussage wie \(8 = 8\), \(''' + L + r''' = \mathbb{R}\). Die Geraden liegen aufeinander.</li>
          </ul>
          <p>Nur der erste Fall ist eine lineare Gleichung im Sinne der Definition aus Kapitel 1 (\(a \neq 0\)); in den anderen hebt sich \(x\) weg.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(\{0\}\) statt \(\{\,\}\): \(\{0\}\) ist eine Menge mit einem Element, der Null. \(5x = 0\) hat die Lösung \(0\), \(0 \cdot x = 5\) hat keine.</p>
          <p>Aus «\(8 = 8\)» \(x = 8\) machen: In der Aussage kommt \(x\) nicht mehr vor, sie gilt für jedes \(x\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 13, [
    ('3a', 3, r'Welcher Lösungsfall liegt vor? Gib jeweils \(\mathbb{L}\) an: (a) \(3(x - 2) = 3x - 6\) (b) \(2x + 7 = 2(x + 3)\) (c) \(4x - 1 = 2(x + 1)\)',
     r'<p>(a) \(3x - 6 = 3x - 6\), nach \(\mid -3x\): \(-6 = -6\) wahr, \(' + L + r' = \mathbb{R}\). (b) \(2x + 7 = 2x + 6\), nach \(\mid -2x\): \(7 = 6\) falsch, \(' + L + r' = \{\,\}\). (c) \(4x - 1 = 2x + 2\), \(2x = 3\), \(x = 1.5\): \(' + L + r' = \{1.5\}\).</p>', ''),
    ('3b', 2, r'Löse \(5(x + 1) - 2x = 3(x + 2)\).',
     r'<p>\(5x + 5 - 2x = 3x + 6\), also \(3x + 5 = 3x + 6\); nach \(\mid -3x\): \(5 = 6\), falsch. \(' + L + r' = \{\,\}\).</p>', ''),
    ('3c', 2, r'Jemand schreibt nach dem Umformen: «\(0 = 4\), also \(\mathbb{L} = \{0\}\)». Was ist falsch?',
     r'<p>\(0 = 4\) ist für jedes \(x\) falsch, auch für \(x = 0\). Keine Zahl ist Lösung: \(' + L + r' = \{\,\}\). \(\{0\}\) wäre die Menge mit der Zahl \(0\).</p>', ''),
    ('3d', 2, r'Ergänze die rechte Seite \(3(x + 4) = 3x + \square\) so, dass die Gleichung (a) unendlich viele Lösungen, (b) keine Lösung hat.',
     r'<p>Links steht \(3x + 12\). (a) \(\square = 12\): \(12 = 12\) wahr, \(' + L + r' = \mathbb{R}\). (b) jede andere Zahl, z.&nbsp;B. \(\square = 10\): \(12 = 10\) falsch, \(' + L + r' = \{\,\}\).</p>', ''),
    ('3e', 2, r'Warum heisst die Aussage «\(8 = 8\)» nach dem Umformen nicht «\(x = 8\)»?',
     r'<p>In \(8 = 8\) kommt \(x\) nicht mehr vor. Die Aussage ist wahr, egal welches \(x\) man einsetzt: Jede Zahl ist Lösung, \(' + L + r' = \mathbb{R}\). Bei \(x = 8\) wäre nur die \(8\) eine Lösung.</p>', ''),
    ('3f', 2, r'Die Bilder zeigen je die beiden Seiten einer Gleichung als Geraden (blau links, orange rechts). Ordne zu und gib \(\mathbb{L}\) an: (1) \(2x + 1 = 2x - 2\) (2) \(2x + 1 = -x + 4\) (3) \(2(x + 0.5) = 2x + 1\)',
     r'<p>(1) ↔ B: parallele Geraden, \(1 = -2\) falsch, \(' + L + r' = \{\,\}\). (2) ↔ A: Schnitt bei \(x = 1\), \(3x = 3\), \(' + L + r' = \{1\}\). (3) ↔ C: beide Geraden liegen aufeinander, \(2x + 1 = 2x + 1\), \(' + L + r' = \mathbb{R}\).</p>',
     minireihe(mini('g,2,1;g,-1,4', '-3,3,-3,5', '-2,-1,1,2', '2,4', 'A', False),
               mini('g,2,1;g,2,-2', '-3,3,-3,5', '-2,-1,1,2', '2,4', 'B', False),
               mini('g,2,1;g,2,1', '-3,3,-3,5', '-2,-1,1,2', '2,4', 'C', False))),
])
k3 = kapitel(3, 'faelle', 'Drei Lösungsfälle', 35,
             r'Du sortierst eine Gleichung auf \(a \cdot x = c\) und entscheidest: genau eine Lösung, keine Lösung oder jede Zahl ist Lösung — und gibst die Lösungsmenge an.',
             ('g2-2a-lp-faelle', 'Drei Lösungsfälle'),
             umformer(3, 'Umformer: lösen und den Lösungsfall erkennen'),
             ('g2-2a-lp-kontrolle-faelle', 'Kontrollfragen zu den Lösungsfällen'),
             fest3, [uebung('loesungsfall', 'Welcher Lösungsfall?'), uebung('fall-zahl', 'Die Zahl, die den Fall macht')],
             auf3, f'<a href="{TA}#spezialfaelle">Themenseite 2.2a, Drei Lösungsfälle</a>', komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = '''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 280" role="img" aria-label="Linke Seite (blau) und rechte Seite (orange) als Geraden, senkrechte Linie bei x"></svg>
        <div class="sl-row">
          <div class="sl-grp akz-blau"><label for="s4-x"><span class="var">x</span></label><input type="range" id="s4-x" data-p="x" min="-2" max="6" step="0.5" value="0"><span class="sl-val"></span></div>
        </div>
        <label class="sim-schalter"><input type="checkbox"> Normalform zeigen: links − rechts</label>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Normalform und drei Sichten</div>
          <p>Die Form aus der Definition (Kapitel 1) heisst <b>Normalform</b>:</p>
          <p>\[ a \cdot x + b = 0 \quad \text{mit } a \neq 0, \qquad x = -\frac{b}{a} \]</p>
          <p>Beispiel: \(12x + 45 = 117 \;\;\big|\, -117\) gibt \(12x - 72 = 0\), also \(a = 12\), \(b = -72\), \(x = -\tfrac{-72}{12} = 6\).</p>
          <ul>
            <li><b>Tabelle:</b> beide Seiten für einige \(x\) ausrechnen — die Lösung liegt dort, wo das Vergleichszeichen kippt (von \(\lt\) zu \(\gt\) oder umgekehrt); dazwischen steht \(=\).</li>
            <li><b>Graph:</b> beide Seiten als Geraden — die Lösung ist der \(x\)-Wert des Schnittpunkts. In der Normalform ist sie die Nullstelle von \(y = a \cdot x + b\).</li>
            <li><b>Rechnung:</b> Äquivalenzumformungen liefern die Lösung genau.</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Tabelle oder Graph für genau halten: Bei \(3x - 1 = 1\) kippt das Zeichen zwischen \(0\) und \(1\); die Lösung \(\tfrac{2}{3}\) findet nur die Rechnung.</p>
          <p>Das Minus in \(x = -\tfrac{b}{a}\) vergessen: Bei \(4x - 10 = 0\) ist \(b = -10\) und \(x = 2.5\), nicht \(-2.5\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Bring auf die Normalform \(a \cdot x + b = 0\) und gib \(a\), \(b\) und die Lösung an: (a) \(7x - 4 = 3x + 12\) (b) \(\tfrac{x}{4} + 3 = \tfrac{x}{2} - 1\)',
     r'<p>(a) \(\mid -3x - 12\): \(4x - 16 = 0\), \(a = 4\), \(b = -16\), \(x = 4\). (b) Mal \(4\): \(x + 12 = 2x - 4\); \(\mid -2x + 4\): \(-x + 16 = 0\), \(a = -1\), \(b = 16\), \(x = 16\). Gleichwertig: \(x - 16 = 0\).</p>', ''),
    ('4b', 3, r'Rechne für \(4x - 3 = 2x + 4\) beide Seiten für \(x = 2\), \(3\) und \(4\) aus und setz das Vergleichszeichen. Zwischen welchen Zahlen liegt die Lösung? Berechne sie dann genau.',
     r'<table class="wertetab"><tr><th>\(x\)</th><th>links \(4x - 3\)</th><th>rechts \(2x + 4\)</th><th></th></tr><tr><td>2</td><td>5</td><td>8</td><td>\(\lt\)</td></tr><tr><td>3</td><td>9</td><td>10</td><td>\(\lt\)</td></tr><tr><td>4</td><td>13</td><td>12</td><td>\(\gt\)</td></tr></table><p>Das Zeichen kippt zwischen \(3\) und \(4\). Rechnung: \(2x = 7\), \(x = 3.5\). \(' + L + r' = \{3.5\}\).</p>', ''),
    ('4c', 2, r'Zwei Telefon-Angebote: \(K_A(t) = 0.2t + 30\) (blau) und \(K_B(t) = 0.35t\) (orange), \(t\) in Minuten, \(K\) in CHF. Lies ab, bei welcher Gesprächsdauer beide gleich viel kosten, und bestätige es rechnerisch.',
     r'<p>Die Geraden schneiden sich bei \(t = 200\), \(K = 70\). Rechnung: \(0.2t + 30 = 0.35t\), \(30 = 0.15t\), \(t = 200\). Probe: \(40 + 30 = 70\) und \(0.35 \cdot 200 = 70\) ✓. Bei 200 Minuten kosten beide 70 CHF.</p>',
     minireihe(mini('g,0.2,30;g,0.35,0', '-80,320,-12,120', '100,200', '30,70,100', sx=50, sy=10, xname='t [min]', yname='K [CHF]'))),
    ('4d', 2, r'Warum gilt die Lösungsformel \(x = -\tfrac{b}{a}\) nur für \(a \neq 0\)?',
     r'<p>Für die Formel teilt man durch \(a\), und durch \(0\) kann man nicht teilen. Ist \(a = 0\), kommt \(x\) gar nicht mehr vor: Je nach \(b\) gibt es keine Lösung oder jede Zahl ist Lösung (Kapitel 3).</p>', ''),
    ('4e', 2, r'Eine Taxifahrt kostet \(K(s) = 3.2 \cdot s + 6.5\) (\(s\) in km, \(K\) in CHF). Wie lang war eine Fahrt, die 38.50 CHF kostet?',
     r'<p>\(3.2s + 6.5 = 38.5\), \(\mid -6.5\): \(3.2s = 32\), \(\mid :3.2\): \(s = 10\). Die Fahrt war 10 km lang. Probe: \(32 + 6.5 = 38.5\) ✓.</p>', ''),
])
k4 = kapitel(4, 'sichten', 'Normalform: Tabelle, Graph und Rechnung', 40,
             r'Du bringst eine lineare Gleichung auf die Normalform \(a \cdot x + b = 0\), gibst die Lösung \(x = -\tfrac{b}{a}\) an und erklärst, wie Tabelle und Graph dieselbe Lösung zeigen — und warum nur die Rechnung sie immer genau liefert.',
             ('g2-2a-lp-sichten', 'Tabelle, Graph und Normalform'),
             sim4, ('g2-2a-lp-kontrolle-sichten', 'Kontrollfragen zu Tabelle, Graph und Normalform'),
             fest4, [uebung('normalform', 'Auf Normalform bringen'), uebung('gleichstand', 'Wann gleich teuer?')],
             auf4, f'<a href="{TA}#definition">Themenseite 2.2a, Definition und Normalform</a> und <a href="{TA}#darstellungen">Drei Sichten</a>', komp='K4')

# ------------------------------------------------------------------ Kapitel 5
sim5 = '''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Familie <select class="sim-wahl" aria-label="Gleichungsfamilie">
          <option value="A" selected>A: k · x + 6 = 2x + 3k</option>
          <option value="B">B: k · x + 1 = 2x + 3</option>
          <option value="C">C: (k² − 4) · x = k − 2</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 280" role="img" aria-label="Gerade y = a(k) · x − c(k): links minus rechts; ihre Nullstelle ist die Lösung"></svg>
        <div class="sl-row">
          <div class="sl-grp akz-orange"><label for="s5-k"><span class="var">Parameter k</span></label><input type="range" id="s5-k" data-p="k" min="-3" max="6" step="0.5" value="4"><span class="sl-val"></span></div>
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Parameterdiskussion</div>
          <ol>
            <li>Gleichung auf die Form \(a(k) \cdot x = c(k)\) sortieren.</li>
            <li>Den kritischen Parameterwert finden, bei dem \(a(k) = 0\) wird.</li>
            <li>Fälle unterscheiden:
              <ul>
                <li>\(a(k) \neq 0\): eindeutig lösbar, \(x = \tfrac{c(k)}{a(k)}\).</li>
                <li>\(a(k) = 0\) und \(c(k) \neq 0\): keine Lösung, \(''' + L + r''' = \{\,\}\).</li>
                <li>\(a(k) = 0\) und \(c(k) = 0\): \(''' + L + r''' = \mathbb{R}\).</li>
              </ul></li>
            <li>Die Lösungsmenge in Abhängigkeit von \(k\) angeben.</li>
          </ol>
          <p>\(k \cdot x + 6 = 2x + 3k \;\big|\, -2x - 6\) gibt \(kx - 2x = 3k - 6\); links \(x\), rechts \(3\) ausklammern: \((k - 2) \cdot x = 3 \cdot (k - 2)\). Für \(k \neq 2\) ist \(''' + L + r''' = \{3\}\), für \(k = 2\) ist \(''' + L + r''' = \mathbb{R}\).</p>
          <p>Lässt sich \(c(k)\) faktorisieren, kürzt man nach dem Teilen: \((k + 1) \cdot x = k^2 + k = k(k + 1)\) gibt für \(k \neq -1\) die Lösung \(x = k\), für \(k = -1\) ist \(''' + L + r''' = \mathbb{R}\).</p>
          <p>Ist \(a(k)\) selbst ein Produkt, etwa \(k^2 - 4 = (k - 2)(k + 2)\), gibt es zwei kritische Werte — jeden einzeln einsetzen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Durch \(a(k)\) teilen, ohne den Fall \(a(k) = 0\) zu prüfen.</p>
          <p>Am kritischen Wert immer «keine Lösung» schreiben: Was dort gilt, entscheidet \(c(k)\). Verschwindet es mit, ist jede Zahl Lösung.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 15, [
    ('5a', 3, r'Löse \(m \cdot x - 4 = 2x + 2m\) in Abhängigkeit von \(m\).',
     r'<p>\((m - 2) \cdot x = 2m + 4 = 2(m + 2)\). Für \(m = 2\): \(0 = 8\), falsch, \(' + L + r' = \{\,\}\). Für \(m \neq 2\): \(x = \dfrac{2(m + 2)}{m - 2}\). Dass jede Zahl Lösung ist, kommt nie vor: Dafür müssten \(m - 2\) und \(m + 2\) zugleich null sein.</p>', ''),
    ('5b', 3, r'Löse \((k - 3) \cdot x = k^2 - 9\) in Abhängigkeit von \(k\). Vereinfache die Lösung so weit wie möglich.',
     r'<p>\(k = 3\): \(0 \cdot x = 0\), wahr, \(' + L + r' = \mathbb{R}\). \(k \neq 3\): \(x = \dfrac{k^2 - 9}{k - 3} = \dfrac{(k - 3)(k + 3)}{k - 3} = k + 3\), \(' + L + r' = \{k + 3\}\).</p><p class="komm">\(k^2 - 9\) mit der dritten binomischen Formel zerlegen, dann kürzen — erlaubt, weil \(k \neq 3\).</p>', ''),
    ('5c', 2, r'\((2k + 1) \cdot x = 12\): Für welches \(k\) gibt es keine Lösung? Für welches \(k\) ist \(x = 4\) die Lösung?',
     r'<p>\(2k + 1 = 0\) bei \(k = -0.5\): \(0 = 12\), falsch, \(' + L + r' = \{\,\}\). \(x = 4\): \((2k + 1) \cdot 4 = 12\), \(2k + 1 = 3\), \(k = 1\). Probe: \(3 \cdot 4 = 12\) ✓.</p>', ''),
    ('5d', 3, r'<i>Vertiefung</i> — zwei kritische Werte: Löse \((k^2 - 1) \cdot x = k + 1\) in Abhängigkeit von \(k\).',
     r'<p>\(k^2 - 1 = (k - 1)(k + 1)\) wird null für \(k = 1\) und \(k = -1\). \(k = 1\): \(0 = 2\), \(' + L + r' = \{\,\}\). \(k = -1\): \(0 = 0\), \(' + L + r' = \mathbb{R}\). Sonst: \(x = \dfrac{k + 1}{(k - 1)(k + 1)} = \dfrac{1}{k - 1}\).</p>', ''),
    ('5e', 2, r'Warum prüft man bei \(a(k) \cdot x = c(k)\) zuerst den Fall \(a(k) = 0\)?',
     r'<p>Für \(x = \tfrac{c(k)}{a(k)}\) teilt man durch \(a(k)\) — das geht nur für \(a(k) \neq 0\). Im Fall \(a(k) = 0\) verschwindet \(x\): Dann gibt es keine oder unendlich viele Lösungen, je nach \(c(k)\).</p>', ''),
    ('5f', 2, r'Die Bilder zeigen links minus rechts von \((k - 1) \cdot x = 2\), also \(y = (k - 1) \cdot x - 2\), für \(k = 3\), \(k = 1\) und \(k = 0\) — in anderer Reihenfolge. Ordne zu und lies jeweils die Lösung ab.',
     r'<p>A ↔ \(k = 0\): \(y = -x - 2\), Nullstelle \(x = -2\). B ↔ \(k = 3\): \(y = 2x - 2\), Nullstelle \(x = 1\). C ↔ \(k = 1\): \(y = -2\) ist waagrecht und trifft die \(x\)-Achse nie — \(0 \cdot x = 2\), keine Lösung.</p>',
     minireihe(mini('g,-1,-2', '-4,3,-5,3', '-2,-1,1,2', '-2,2', 'A', False),
               mini('g,2,-2', '-4,3,-5,3', '-2,-1,1,2', '-2,2', 'B', False),
               mini('g,0,-2', '-4,3,-5,3', '-2,-1,1,2', '-2,2', 'C', False))),
])
k5 = kapitel(5, 'parameter', 'Parameterdiskussion', 45,
             r'Du sortierst eine Gleichung mit Parameter auf \(a(k) \cdot x = c(k)\), findest den kritischen Wert, bei dem \(a(k) = 0\) wird, und gibst die Lösungsmenge für alle \(k\) an.',
             ('g2-2a-lp-parameter', 'Parameterdiskussion'),
             sim5, ('g2-2a-lp-kontrolle-parameter', 'Kontrollfragen zur Parameterdiskussion'),
             fest5, [uebung('param-krit', 'Kritischer Wert'), uebung('param-wert', 'Das k zur Lösung')],
             auf5, f'<a href="{TA}#parameter">Themenseite 2.2a, Parameterdiskussion</a>', komp='K5')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 1.3 · 2.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Klammern auflösen, das kleinste gemeinsame Vielfache, ausklammern, einsetzen und die Äquivalenzumformungen. Wenn das wackelt: <a href="../grundlagen/g1-3-algebraische-terme.html">Teilgebiet 1.3, Algebraische Terme</a> und <a href="../grundlagen/g2-1-grundlagen.html">Teilgebiet 2.1, Grundlagen der Gleichungen</a>.</p>
      ''' + clipkarte('g2-1-aequivalenzumformungen', 'Gleichungen: was die Lösungsmenge erhält', '1:08') + '''
''' + test('t0', 'Vortest', 12, [
    ('0a', 3, r'Löse die Klammern auf und vereinfache: \(2(x + 4) - (3x - 1)\); \(5 - 2(x - 3)\).',
     r'<p>\(2x + 8 - 3x + 1 = -x + 9\); \(5 - 2x + 6 = 11 - 2x\).</p><p class="komm">Faktor und Minus vor der Klammer braucht Kapitel 2.</p>', ''),
    ('0b', 2, r'Wie heisst das kleinste gemeinsame Vielfache von \(4\) und \(6\)? Und von \(2\), \(3\) und \(4\)?',
     r'<p>\(12\); \(12\).</p><p class="komm">Das ist der Hauptnenner in Kapitel 2.</p>', ''),
    ('0c', 2, r'Schreib als Produkt: \(4k - 8\); \(k^2 - 9\).',
     r'<p>\(4(k - 2)\); \((k - 3)(k + 3)\) (dritte binomische Formel).</p><p class="komm">Ausklammern braucht Kapitel 5.</p>', ''),
    ('0d', 2, r'Ist \(x = -2\) eine Lösung von \(3x + 4 = x\)? Begründe mit Einsetzen.',
     r'<p>Ja: links \(3 \cdot (-2) + 4 = -2\), rechts \(-2\). Beide Seiten gleich.</p>', ''),
    ('0e', 3, r'Welche Umformungen ändern die Lösungsmenge einer Gleichung nicht? (A) beidseitig \(+5\) (B) beidseitig \(\cdot (-3)\) (C) beidseitig \(\cdot 0\) (D) beidseitig \(:4\)',
     r'<p>A, B und D — sie lassen sich rückgängig machen. C nicht: Mal \(0\) gibt \(0 = 0\).</p><p class="komm">Das ist die Grundlage von Kapitel 1.</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 8 von 12 Punkten: zuerst die verlinkten Teilgebiete, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/lineare-gleichungen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 2.2a · Kapitel 1–5</span><span class="zeit">≈ 25 min · 23 Punkte</span></div>
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
            <tr><td>20 – 23 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>15 – 19 P</td><td>Den schwächsten Teil nochmals: Tüfteln und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>10 – 14 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 9 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1 und 2; G2 → 2; G3 → 3; G4 → 4; G5 → 4; G6, G7 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Lineare Gleichungen, Version 1.0 (11.10.2026). Gebaut aus scripts/lp/lineare-gleichungen/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlage: HOWTO-leitprogramme.md; Ausgangsmaterial das gemeinsame
     Leitprogramm «Lineare und quadratische Gleichungen» (GF 2.2), das von den Leitprogrammen zu 2.2a und 2.2b abgelöst wird.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2, Teil «lineare Gleichungen» — Kompetenz wörtlich wie in der RLP-Box
     der Themenseite grundlagen/g2-2a-lineare-gleichungen.html:
       «lineare Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden, inkl. Parameterdiskussion
        (auch ohne Hilfsmittel)»
     Für die Kompetenzmatrix in fünf Teile gegliedert:
       K1  lineare Gleichungen mit Äquivalenzumformungen lösen und Lösungen überprüfen (Probe; dazu aus 2.1:
           «algebraische Äquivalenz erklären und anwenden», «Lösungen überprüfen»)
       K2  lineare Gleichungen mit Klammern und Brüchen lösen (Lösungsmethode: zuerst aufräumen)
       K3  die drei Lösungsfälle erkennen und die Lösungsmenge angeben (dazu aus 2.1: «den Typ einer Gleichung
           bestimmen und beim Lösen entsprechend beachten»)
       K4  verschiedene Lösungsmethoden erklären und anwenden: Normalform a·x + b = 0 mit x = −b/a, Tabelle, Graph
       K5  Parameterdiskussion

     Kompetenzmatrix (Kompetenz | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | ja | 1 | 1a–1f | G1
       K2 | ja | 2 | 2a–2f | G1, G2
       K3 | ja | 3 | 3a–3f | G3
       K4 | ja | 4 | 4a–4e | G4, G5
       K5 | ja | 5 | 5a–5f | G6, G7
     Alles ohne Taschenrechner (RLP-Vermerk «auch ohne Hilfsmittel»); auch 1d (Dezimalzahlen) und 4c/4e sind ohne Rechner lösbar.
     Die grafische Sicht (Kapitel 4, Minigrafen) unterstützt nur; «Gleichungen mithilfe von Funktionen visualisieren»
     gehört zu GF 3.1. Der Sachzusammenhang (Mietkosten, Taxi, Tarife) gibt das Modell vor — Modellieren ist GF 2.1/2.M.

     Planung (Kapitel | Lernziel | Kompetenz | Clips | Tüfteln | Beispiel (Quelle) | Häufiger Fehler | min):
       0 | Vorwissen prüfen | 1.3, 2.1 | g2-1-aequivalenzumformungen (Themenseite 2.1) | — | — | — | 10
       1 | umformen und Probe | K1 | g2-2a-lp-umformen, -kontrolle-umformen | Umformer 6 Aufgaben | 5x − 7 = 2x + 8 (Themenseite «Schrittweise»), 2x = 3x − 6 (Häufige Fehler) | Vorzeichen beim Hinüberbringen, −x = −6 | 40
       2 | Klammern und Brüche | K2 | g2-2a-lp-klammern, -kontrolle-klammern | Umformer 6 Aufgaben | 4(x − 2) = 2x + 6 (Mini-Check), 5 − 2(x + 1) = x (A2), x/3 + 2 = x/2 − 1 (Beispiel mit Brüchen) | nur erstes Glied, nur Brüche mal Hauptnenner | 40
       3 | drei Lösungsfälle | K3 | g2-2a-lp-faelle, -kontrolle-faelle | Umformer 6 Aufgaben | 3x + 2 = 11, 2(x + 3) = 2x + 9, 4x + 8 = 4(x + 2) (Themenseite) | {0} statt { } | 35
       4 | Normalform, Tabelle, Graph | K4 | g2-2a-lp-sichten, -kontrolle-sichten | Simulation «Drei Sichten», 6 Aufgaben | 12x + 45 = 117 (Einstieg), 2x − 3 = 5 (Drei Darstellungen) | Tabelle für genau halten, Minus in −b/a | 40
       5 | Parameterdiskussion | K5 | g2-2a-lp-parameter, -kontrolle-parameter | Simulation «Parameter», 7 Aufgaben | k·x + 6 = 2x + 3k, k·x + 1 = 2x + 3 (Themenseite) | durch a(k) teilen ohne Fall a(k) = 0 | 45
       Gesamttest | 25
     Zeiten: 10 + 40 + 40 + 35 + 40 + 45 + 25 = 235 min (≈ 5¼ Lektionen à 45 min). Clips: 10 eigene + 1 der Themenseite 2.1.
     Punkte: Vortest 12, Kapitel 13 · 14 · 13 · 12 · 15, Gesamttest 23 (A 6, B 3, C 7, D 7).

     Kern: K1–K5. Vertiefung: zwei kritische Werte (5d, Simulation Familie C), nicht im Gesamttest.
     Bewusst weggelassen (→ Themenseite 2.2a): lineare Ungleichungen und Vorzeichenkipp (Abschnitt «Lineare
     Ungleichungen», nicht Teil der RLP-Kompetenz 2.2); quadratische Gleichungen (→ 2.2b); Textaufgaben selbst
     modellieren (→ 2.M); Gleichungssysteme (→ 2.3).

     Konventionen wie auf der Themenseite: 𝕃 mit Strichpunkt, leere Menge {}, 𝕃 = ℝ, Normalform a·x + b = 0 mit
     a ≠ 0, Zwischenform a·x = c, Parameter k (bzw. m in A5), a(k)·x = c(k), «kritischer Parameterwert».
     Umformung rechts neben der Zeile wie im Heft («| −2x»).
     Bewusst anders als auf der Themenseite: Die Parameter-Simulation zeigt die Gerade y = a(k)·x − c(k) (links minus
     rechts, die Normalform aus Kapitel 4) statt nur Text — ihre Nullstelle ist die Lösung, und die drei Fälle werden
     sichtbar (Nullstelle, waagrecht neben der Achse, auf der Achse).
     Farben: Gleichung und linke Seite blau, Umformung, rechte Seite und Parameter orange, Lösungen grün, Fehler rot.

     Muster je Kapitel: ① Einführungsclip → ② Umformer (Kapitel 1–3) bzw. Simulation (Kapitel 4–5) mit Aufgabenleiste
     → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF aus LaTeX (downloads/leitprogramme/lineare-gleichungen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Lineare Gleichungen</h1>
      <p class="unter">Zuschauen, umformen, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest — zusammen rund 235 Minuten.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 2.2a</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Umformen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Klammern und Brüche</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Lösungsfälle</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Normalform</span></a></li>
      <li><a href="#k5"><span class="nr">5</span><span>Parameter</span></a></li>
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
          <li><b>② Tüfteln:</b> In Kapitel 1–3 wählst du im Umformer jeden Schritt selbst und gibst am Schluss die Lösungsmenge ein — er zeigt ✓, wenn sie stimmt. In Kapitel 4 und 5 ziehst du am Regler und löst die Aufgaben der Leiste.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2 (Teil lineare Gleichungen):</p>
        <p>lineare Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden, inkl. Parameterdiskussion <span class="ohm">auch ohne Hilfsmittel</span></p>
        <p class="rlp-quelle">Hier in fünf Teile gegliedert:</p>
        <ul>
          <li><b>K1</b> lineare Gleichungen mit Äquivalenzumformungen lösen und die Probe machen (dazu aus 2.1) — Kapitel 1</li>
          <li><b>K2</b> Gleichungen mit Klammern und Brüchen lösen — Kapitel 2</li>
          <li><b>K3</b> die drei Lösungsfälle erkennen und die Lösungsmenge angeben — Kapitel 3</li>
          <li><b>K4</b> Lösungsmethoden erklären und anwenden: Normalform, Tabelle, Graph — Kapitel 4</li>
          <li><b>K5</b> Parameterdiskussion — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Die Geraden im Bild zeigen die Lösung nur als Schnittpunkt — «Gleichungen mithilfe von Funktionen visualisieren» gehört zu GF 3.1.</p>
        <p class="rlp-quelle">Nicht hier, sondern auf der <a href="''' + TA + '''#ungleichungen">Themenseite 2.2a</a>: lineare Ungleichungen. Quadratische Gleichungen: Teilgebiet 2.2b. Gleichungssysteme: Teilgebiet 2.3.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Lineare Gleichungen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (11.10.2026): Vorwissen 10 · K1 40 · K2 40 · K3 35 · K4 40 · K5 45 · Gesamttest 25 = 235 min
assert 10 + 40 + 40 + 35 + 40 + 45 + 25 == 235
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
