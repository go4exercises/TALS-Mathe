"""Baut leitprogramme/lineare-quadratische-gleichungen.html aus einer Kapitelbeschreibung (06.10.2026).

  python3 scripts/lp/lineare-quadratische-gleichungen/seite.py

Leitprogramm zum Teilgebiet GF 2.2 (Themenseiten g2-2a-lineare-gleichungen.html und
g2-2b-quadratische-gleichungen.html), nach dem Leitfaden des Auftraggebers ~/HOWTO-GleichungLP.md.
Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden Seite, ersetzt Inhalt und
Seitenskript (seite.js) und schreibt die Seite neu. Beim ersten Lauf kommt das Gerüst aus
leitprogramme/betragsfunktionen.html, mit eigenem Titel und eigenen localStorage-Schlüsseln.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und
python3 scripts/build-seo.py. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/lineare-quadratische-gleichungen.html'
NAME = 'Lineare und quadratische Gleichungen'

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/betragsfunktionen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = (alt[:a] + '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n'
           '<!-- SEO:ENDE -->' + alt[b:])
    alt = alt.replace('<title>Leitprogramm Betragsfunktionen</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-betrag-', 'lp-gleichungen-')

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Betragsfunktionen', '\n/* ════════ Gleichungen'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Betragsfunktionen — Simulationen'),
                    alt.find('<script>\n/* Leitprogramm Lineare und quadratische Gleichungen —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = fuss.replace('Leitprogramm · Betragsfunktionen', 'Leitprogramm · ' + NAME)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 6. Oktober 2026', fuss)

CSS = '''
/* ════════ Gleichungen (06.10.2026) — Kapitelmuster wie die Funktionen-Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg) wie dort. Neu ist der Umformer:
   Statt Regler wählen die Lernenden Umformungsschritte, füllen Lücken und geben die Lösungsmenge
   ein. Farben: Gleichung blau, Umformung orange, Lösungen grün, Fehler rot. */
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 2.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


TA = '../grundlagen/g2-2a-lineare-gleichungen.html'
TB = '../grundlagen/g2-2b-quadratische-gleichungen.html'
L = r'\mathbb{L}'

# ------------------------------------------------------------------ Kapitel 1
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Äquivalenzumformungen und die drei Lösungsfälle</div>
          <p>Eine <b>Äquivalenzumformung</b> ändert die Lösungsmenge nicht: auf beiden Seiten dieselbe Zahl oder denselben Term addieren oder subtrahieren, beide Seiten mit derselben Zahl \(\neq 0\) multiplizieren oder durch sie dividieren. Klammern auflösen und zusammenfassen sind Termumformungen — sie ändern nichts.</p>
          <ol>
            <li>Klammern auflösen, Brüche mit dem Hauptnenner beseitigen.</li>
            <li>Alle \(x\)-Glieder auf eine Seite, alle Zahlen auf die andere.</li>
            <li>Zusammenfassen und durch den Faktor vor \(x\) dividieren.</li>
            <li><b>Probe</b> in der ursprünglichen Gleichung.</li>
          </ol>
          <p>Sortiert steht \(a \cdot x = c\) da. Dann entscheidet \(a\):</p>
          <ul>
            <li>\(a \neq 0\): genau eine Lösung, \(''' + L + r''' = \{\tfrac{c}{a}\}\).</li>
            <li>\(a = 0\), \(c \neq 0\): Es bleibt eine falsche Aussage wie \(6 = 9\) — \(''' + L + r''' = \{\,\}\).</li>
            <li>\(a = 0\), \(c = 0\): Es bleibt eine wahre Aussage wie \(8 = 8\) — \(''' + L + r''' = \mathbb{R}\).</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Das Minus vor einer Klammer dreht <b>jedes</b> Vorzeichen in der Klammer: \(3 - (x - 1) = 3 - x + 1\).</p>
          <p>Mit \(0\) multiplizieren oder durch einen Term mit \(x\) dividieren ist keine Äquivalenzumformung — es ändert die Lösungsmenge: Mal \(0\) macht jede Zahl zur Lösung (\(0 = 0\)), durch \(x\) teilen kann Lösungen verlieren.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 15, [
    ('1a', 2, r'Löse \(7x - 4 = 3x + 12\) und mach die Probe.',
     r'<p>\(4x - 4 = 12\), \(4x = 16\), \(x = 4\). Probe: \(28 - 4 = 24\) und \(12 + 12 = 24\) ✓. \(' + L + r' = \{4\}\).</p>', ''),
    ('1b', 3, r'Löse \(3(2x - 1) - 2(x + 4) = 1\).',
     r'<p>\(6x - 3 - 2x - 8 = 1\), also \(4x - 11 = 1\), \(4x = 12\), \(x = 3\). \(' + L + r' = \{3\}\).</p><p class="komm">Das Minus vor \(2(x + 4)\) gilt für beide Glieder: \(-2x - 8\).</p>', ''),
    ('1c', 3, r'Löse \(\dfrac{x + 1}{4} = \dfrac{x - 2}{2}\).',
     r'<p>Mal \(4\): \(x + 1 = 2(x - 2) = 2x - 4\). Dann \(5 = x\). Probe: \(\tfrac{6}{4} = 1.5 = \tfrac{3}{2}\) ✓. \(' + L + r' = \{5\}\).</p>', ''),
    ('1d', 3, r'Welcher Lösungsfall liegt vor? (a) \(4(x - 1) = 4x - 4\) (b) \(2x + 5 = 2(x + 3)\)',
     r'<p>(a) \(4x - 4 = 4x - 4\), nach \(-4x\): \(-4 = -4\) wahr — \(' + L + r' = \mathbb{R}\). (b) \(2x + 5 = 2x + 6\), nach \(-2x\): \(5 = 6\) falsch — \(' + L + r' = \{\,\}\).</p>', ''),
    ('1e', 2, r'Warum ist «beidseitig mal \(0\)» keine Äquivalenzumformung?',
     r'<p>Danach steht \(0 = 0\) da — wahr für jedes \(x\). Aus einer Gleichung mit einer Lösung würde eine mit unendlich vielen: Die Lösungsmenge ändert sich. Umkehren lässt sich das nicht, denn durch \(0\) kann man nicht dividieren.</p>', ''),
    ('1f', 2, r'Die Geraden \(y = 0.5x + 1\) und \(y = -x + 4\) sind abgebildet. Welche Gleichung löst ihr Schnittpunkt? Lies die Lösung ab und bestätige sie rechnerisch.',
     r'<p>\(0.5x + 1 = -x + 4\). Der Schnittpunkt liegt bei \(x = 2\). Rechnung: \(1.5x = 3\), \(x = 2\). Beide Seiten geben \(2\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="g,0.5,1;g,-1,4" data-fenster="-2,6,-1,5" data-xm="-1,1,2,3,4,5" data-ym="1,2,3,4"></svg></div>'),
], zwei=False)
k1 = kapitel(1, 'lineare', 'Lineare Gleichungen umformen', 40,
             r'Du löst lineare Gleichungen mit Äquivalenzumformungen, machst die Probe und erkennst an \(a \cdot x = c\), ob es eine, keine oder unendlich viele Lösungen gibt.',
             ('g2-2-lp-umformen', 'Umformen und die drei Lösungsfälle'),
             umformer(1, 'Umformer: lineare Gleichungen Schritt für Schritt lösen'),
             ('g2-2-lp-kontrolle-umformen', 'Kontrollfragen zum Umformen'),
             fest1, [uebung('linear-loesen', 'Lineare Gleichung lösen'), uebung('loesungsfall', 'Welcher Lösungsfall?')],
             auf1, f'<a href="{TA}#verfahren">Themenseite 2.2a, Lösungsverfahren</a> und <a href="{TA}#spezialfaelle">drei Lösungsfälle</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 2
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ausklammern und Nullprodukt</div>
          <p><b>Satz vom Nullprodukt:</b> Ein Produkt ist genau dann null, wenn mindestens ein Faktor null ist: \(A \cdot B = 0 \iff A = 0 \;\text{oder}\; B = 0\).</p>
          <ol>
            <li>Auf null bringen — rechts muss \(0\) stehen.</li>
            <li>Ausklammern: aus der Summe ein Produkt machen.</li>
            <li>Jeden Faktor null setzen und lösen.</li>
            <li>Probe in der Ausgangsgleichung.</li>
          </ol>
          <p>\[ x^2 = 5x \iff x^2 - 5x = 0 \iff x\,(x - 5) = 0 \iff x = 0 \;\text{oder}\; x = 5 \]</p>
          <p>Fehlt die Zahl ohne \(x\) (\(ax^2 + bx = 0\)), ist \(x = 0\) immer eine Lösung. Eine getrennte Fallunterscheidung — erst \(x = 0\) prüfen, dann für \(x \neq 0\) teilen — ist ebenfalls richtig.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Durch \(x\) teilen: Aus \(x^2 = 4x\) wird \(x = 4\) — und \(x = 0\) fehlt. Teilen durch \(x\) setzt \(x \neq 0\) voraus.</p>
          <p>Das Nullprodukt nur bei «\(= 0\)»: \(x(x - 5) = 6\) heisst <b>nicht</b> \(x = 6\) oder \(x - 5 = 6\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Löse \(3x^2 + 12x = 0\). Schreib die Faktorform auf und mach die Probe.',
     r'<p>\(3x\,(x + 4) = 0\), also \(x = 0\) oder \(x = -4\). \(' + L + r' = \{-4;\ 0\}\). Probe: \(0 + 0 = 0\); \(3 \cdot 16 - 48 = 0\) ✓.</p>', ''),
    ('2b', 2, r'Löse \((x - 2)(x + 1) = 0\).',
     r'<p>\(x - 2 = 0\) oder \(x + 1 = 0\): \(' + L + r' = \{-1;\ 2\}\).</p><p class="komm">Bei Faktoren der Form \((x - x_1)\) steht die Lösung \(x_1\) direkt in der Klammer — mit umgekehrtem Vorzeichen geschrieben.</p>', ''),
    ('2c', 2, r'Jemand rechnet: «\((x - 3)(x + 1) = 5 \Rightarrow x - 3 = 5\) oder \(x + 1 = 5\), also \(x = 8\) oder \(x = 4\)». Was ist falsch? Mach die Probe und löse richtig.',
     r'<p>Das Nullprodukt gilt nur, wenn rechts \(0\) steht. Probe: \(5 \cdot 9 = 45 \neq 5\). Richtig: \(x^2 - 2x - 3 = 5\), \(x^2 - 2x - 8 = 0\), \((x - 4)(x + 2) = 0\), \(' + L + r' = \{-2;\ 4\}\).</p>', ''),
    ('2d', 3, r'Löse \((x - 1)^2 = 3(x - 1)\). Erkenne den gemeinsamen Faktor.',
     r'<p>\((x - 1)^2 - 3(x - 1) = 0\), \((x - 1)\,[(x - 1) - 3] = (x - 1)(x - 4) = 0\). \(' + L + r' = \{1;\ 4\}\).</p><p class="komm">Wer durch \((x - 1)\) teilt, verliert \(x = 1\).</p>', ''),
    ('2e', 2, r'Abgebildet ist \(y = x^2 + 2x\). Lies die Lösungen von \(x^2 + 2x = 0\) ab und bestätige sie mit dem Nullprodukt.',
     r'<p>Die Parabel schneidet die \(x\)-Achse bei \(-2\) und \(0\). Rechnung: \(x(x + 2) = 0\), \(' + L + r' = \{-2;\ 0\}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="q,1,2,0" data-fenster="-4,2,-2,4" data-xm="-3,-2,-1,1" data-ym="-1,1,2,3"></svg></div>'),
], zwei=False)
k2 = kapitel(2, 'nullprodukt', 'Ausklammern und Nullprodukt', 40,
             r'Du löst Gleichungen mit gemeinsamem Faktor durch Ausklammern und den Satz vom Nullprodukt und erklärst, warum die Division durch eine Variable, die null werden kann, Lösungen verliert.',
             ('g2-2-lp-nullprodukt', 'Ausklammern und Nullprodukt'),
             umformer(2, 'Umformer: ausklammern und mit dem Nullprodukt lösen'),
             ('g2-2-lp-kontrolle-nullprodukt', 'Kontrollfragen zum Nullprodukt'),
             fest2, [uebung('ausklammern', 'Ausklammern und lösen'), uebung('nullprodukt', 'Nullprodukt')],
             auf2, f'<a href="{TB}#faktorisieren">Themenseite 2.2b, Faktorisieren</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wurzelziehen, Ergänzen, Mitternachtsformel</div>
          <p><b>Wurzelziehen:</b> \(x^2 = r\) hat für \(r \gt 0\) die Lösungen \(x = \pm\sqrt{r}\), für \(r = 0\) nur \(x = 0\), für \(r \lt 0\) keine. Ebenso \((x - u)^2 = r \Rightarrow x - u = \pm\sqrt{r}\) für \(r \ge 0\).</p>
          <p><b>Quadratische Ergänzung</b> (Faktor \(1\) vor \(x^2\), sonst zuerst teilen): Bei \(x^2 + bx\) beidseitig \(\left(\tfrac{b}{2}\right)^2\) addieren — links entsteht ein Binom: \(x^2 - 4x + 4 = (x - 2)^2\).</p>
          <p><b>Mitternachtsformel</b> (Lösungsformel), für \(ax^2 + bx + c = 0\) mit \(a \neq 0\):</p>
          <p>\[ x_{1,2} = \frac{-b \pm \sqrt{D}}{2a}, \qquad D = b^2 - 4ac \]</p>
          <ul>
            <li>\(D \gt 0\): zwei Lösungen — die Parabel schneidet die \(x\)-Achse zweimal.</li>
            <li>\(D = 0\): eine (doppelte) Lösung \(x = -\tfrac{b}{2a}\) — die Parabel berührt die \(x\)-Achse.</li>
            <li>\(D \lt 0\): keine Lösung, \(''' + L + r''' = \{\,\}\).</li>
          </ul>
          <p>Die Lösungen von \(ax^2 + bx + c = 0\) sind die Nullstellen der Parabel \(y = ax^2 + bx + c\) (Funktionssicht aus GF 3.1/3.3). Die Themenseite zeigt dazu auch die pq-Formel für \(x^2 + px + q = 0\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur die positive Wurzel: Aus \(x^2 = 9\) folgt \(x = \pm 3\), denn auch \((-3)^2 = 9\).</p>
          <p>Vorzeichen in \(D\): Bei \(c \lt 0\) wird \(-4ac\) positiv — \(3x^2 - 5x - 2\) hat \(D = 25 + 24\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 16, [
    ('3a', 1, r'Löse \(x^2 = 0.49\).',
     r'<p>\(x = \pm 0.7\): \(' + L + r' = \{-0.7;\ 0.7\}\).</p>', ''),
    ('3b', 3, r'Löse \(x^2 + 4x - 21 = 0\) mit quadratischer Ergänzung.',
     r'<p>\(x^2 + 4x = 21\), plus \(4\): \((x + 2)^2 = 25\), \(x + 2 = \pm 5\). \(' + L + r' = \{-7;\ 3\}\).</p>', ''),
    ('3c', 3, r'Löse \(2x^2 - 7x + 3 = 0\) mit der Mitternachtsformel.',
     r'<p>\(D = 49 - 24 = 25\), \(x = \dfrac{7 \pm 5}{4}\): \(' + L + r' = \{0.5;\ 3\}\).</p>', ''),
    ('3d', 3, r'Wie viele Lösungen? Entscheide mit \(D\), ohne zu lösen: (a) \(x^2 - 6x + 10 = 0\) (b) \(9x^2 + 6x + 1 = 0\) (c) \(x^2 + x - 1 = 0\)',
     r'<p>(a) \(D = 36 - 40 = -4\): keine. (b) \(D = 36 - 36 = 0\): eine. (c) \(D = 1 + 4 = 5\): zwei.</p>', ''),
    ('3g', 2, r'Löse \(x^2 - 4x + 1 = 0\) exakt (ohne Taschenrechner).',
     r'<p>\(D = 16 - 4 = 12\), \(x = \dfrac{4 \pm \sqrt{12}}{2} = 2 \pm \sqrt{3}\). \(' + L + r' = \{2 - \sqrt{3};\ 2 + \sqrt{3}\}\) (\(\approx 0.27\) und \(3.73\)).</p><p class="komm">Nicht jede Lösung ist eine schöne Zahl: Die Wurzel bleibt stehen, wenn \(D\) keine Quadratzahl ist.</p>', ''),
    ('3e', 2, r'Warum gehören zu \(x^2 = 16\) zwei Lösungen, zu \(x^2 = 0\) nur eine?',
     r'<p>\(4^2 = 16\) und \((-4)^2 = 16\): Zwei Zahlen haben das Quadrat \(16\). Das Quadrat \(0\) hat nur die Zahl \(0\), denn \(+0\) und \(-0\) sind dieselbe Zahl.</p>', ''),
    ('3f', 2, r'Abgebildet ist \(y = x^2 - 4x + 3\). Berechne \(D\) und erkläre am Bild, warum das Vorzeichen passt.',
     r'<p>\(D = 16 - 12 = 4 \gt 0\): zwei Lösungen. Im Bild schneidet die Parabel die \(x\)-Achse zweimal, bei \(1\) und \(3\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="q,1,-4,3" data-fenster="-1,5,-2,4" data-xm="1,2,3,4" data-ym="-1,1,2,3"></svg></div>'),
], zwei=False)
k3 = kapitel(3, 'formel', 'Wurzelziehen, Ergänzen, Mitternachtsformel', 45,
             r'Du löst \(x^2 = r\) und \((x - p)^2 = r\) mit Wurzelziehen, ergänzt quadratisch, wendest die Mitternachtsformel an und liest an der Diskriminante ab, wie viele Lösungen es gibt.',
             ('g2-2-lp-ergaenzen', 'Wurzelziehen, Ergänzen, Mitternachtsformel'),
             umformer(3, 'Umformer: Wurzel ziehen, quadratisch ergänzen, Mitternachtsformel'),
             ('g2-2-lp-kontrolle-ergaenzen', 'Kontrollfragen zur Mitternachtsformel'),
             fest3, [uebung('wurzel', 'Wurzel ziehen'), uebung('mitternacht', 'Mitternachtsformel')],
             auf3, f'<a href="{TB}#verfahren">Themenseite 2.2b, Lösungsverfahren</a> und <a href="{TB}#diskriminante">Diskriminante</a>', komp='K3')

# ------------------------------------------------------------------ Kapitel 4
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Das passende Verfahren</div>
          <p><b>Zuerst umformen:</b> Klammern auflösen und alles auf eine Seite. Erst jetzt zeigt sich der <b>Typ</b> — heben sich die \(x^2\) weg, ist die Gleichung linear.</p>
          <ul>
            <li>Kein lineares Glied (\(b = 0\), \(ax^2 + c = 0\)): <b>Wurzelziehen</b>.</li>
            <li>Keine Zahl ohne \(x\) (\(ax^2 + bx = 0\)): <b>Ausklammern</b> und Nullprodukt.</li>
            <li>Zerlegung sichtbar: <b>Faktorisieren</b> — Binom \(x^2 - 6x + 9 = (x - 3)^2\) oder Zweiklammersatz \(x^2 + px + q = (x - x_1)(x - x_2)\) mit \(x_1 + x_2 = -p\) und \(x_1 \cdot x_2 = q\) (Satz von Vieta).</li>
            <li>Sonst: <b>Mitternachtsformel</b> — sie geht immer, ist aber am aufwendigsten.</li>
          </ul>
          <p>Zum Schluss die <b>Probe</b> in der Ausgangsgleichung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Ein Verfahren anwenden, bevor rechts \(0\) steht: \(x(x + 3) = 10\) ist kein Nullprodukt.</p>
          <p>Vorzeichen im Zweiklammersatz: Gesucht sind die <b>Lösungen</b> mit Summe \(-p\) und Produkt \(q\). \(x^2 + 3x - 10 = (x + 5)(x - 2)\): Lösungen \(-5\) und \(2\), Summe \(-3 = -p\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 13, [
    ('4a', 4, r'Wähle jeweils das schnellste Verfahren und löse: (a) \(4x^2 - 1 = 0\) (b) \(3x^2 - 6x = 0\) (c) \(x^2 - x - 12 = 0\)',
     r'<p>(a) Wurzelziehen: \(x^2 = \tfrac{1}{4}\), \(' + L + r' = \{-0.5;\ 0.5\}\). (b) Ausklammern: \(3x(x - 2) = 0\), \(' + L + r' = \{0;\ 2\}\). (c) Zweiklammersatz: \((x - 4)(x + 3) = 0\), \(' + L + r' = \{-3;\ 4\}\).</p>', ''),
    ('4b', 2, r'Bestimme den Typ und löse: \((2x - 1)^2 = 4x^2 + 3\).',
     r'<p>\(4x^2 - 4x + 1 = 4x^2 + 3\). Die \(4x^2\) heben sich weg: linear. \(-4x = 2\), \(x = -0.5\). \(' + L + r' = \{-0.5\}\).</p>', ''),
    ('4c', 2, r'Warum funktioniert die Mitternachtsformel immer, der Zweiklammersatz aber nicht?',
     r'<p>Die Formel ist die quadratische Ergänzung, allgemein ausgeführt — sie braucht nur \(a \neq 0\). Der Zweiklammersatz braucht zwei Zahlen mit passender Summe und passendem Produkt, die man erraten kann; bei Lösungen wie \(\tfrac{-1 \pm \sqrt{33}}{4}\) gibt es keine solchen ganzen Zahlen.</p>', ''),
    ('4d', 3, r'Löse \((x + 4)(x - 1) = 2x + 2\) und mach die Probe.',
     r'<p>\(x^2 + 3x - 4 = 2x + 2\), also \(x^2 + x - 6 = 0\), \((x + 3)(x - 2) = 0\). \(' + L + r' = \{-3;\ 2\}\). Probe: \(1 \cdot (-4) = -4 = -6 + 2\) ✓; \(6 \cdot 1 = 6 = 4 + 2\) ✓.</p><p class="komm">Das Nullprodukt darf man erst anwenden, wenn rechts \(0\) steht.</p>', ''),
    ('4e', 2, r'Abgebildet ist \(y = x^2 - x - 2\). Lies die Nullstellen ab und schreib die Gleichung \(x^2 - x - 2 = 0\) in Faktorform.',
     r'<p>Nullstellen \(-1\) und \(2\): \((x + 1)(x - 2) = 0\). Kontrolle: Summe \(-1 + 2 = 1 = -p\), Produkt \(-2 = q\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini gross" data-k="q,1,-1,-2" data-fenster="-3,4,-3,4" data-xm="-2,-1,1,2,3" data-ym="-2,-1,1,2,3"></svg></div>'),
], zwei=False)
k4 = kapitel(4, 'verfahren', 'Das passende Verfahren', 40,
             r'Du bringst eine Gleichung auf null, bestimmst ihren Typ, wählst das passende Verfahren — Wurzelziehen, Ausklammern, Faktorisieren oder Mitternachtsformel —, begründest die Wahl und prüfst die Lösungen.',
             ('g2-2-lp-verfahren', 'Das passende Verfahren wählen'),
             umformer(4, 'Umformer: Verfahren wählen und lösen'),
             ('g2-2-lp-kontrolle-verfahren', 'Kontrollfragen zur Verfahrenswahl'),
             fest4, [uebung('verfahren', 'Verfahren wählen'), uebung('zweiklammer', 'Zweiklammersatz')],
             auf4, f'<a href="{TB}#verfahren">Themenseite 2.2b, wann welches Verfahren</a> und <a href="{TB}#faktorisieren">Faktorisieren</a>', komp='K4')

# ------------------------------------------------------------------ Kapitel 5
sim5 = '''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Familie <select class="sim-wahl" aria-label="Gleichungsfamilie">
          <option value="A" selected>A: x² − 4x + k = 0</option>
          <option value="B">B: (k − 1) · x = k² − 1</option>
          <option value="C">C: k · x² + 2x + 1 = 0</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 280" role="img" aria-label="Graph zur gewählten Gleichungsfamilie mit den Lösungen"></svg>
        <div class="sl-row">
          <div class="sl-grp akz-orange"><label for="s5-k"><span class="var">Parameter k</span></label><input type="range" id="s5-k" data-p="k" min="-3" max="6" step="0.5" value="2"><span class="sl-val"></span></div>
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Parameterdiskussion</div>
          <p><b>Linear:</b> auf die Form \(a(k) \cdot x = c(k)\) sortieren und den kritischen Wert suchen, bei dem \(a(k) = 0\) wird.</p>
          <ul>
            <li>\(a(k) \neq 0\): genau eine Lösung \(x = \tfrac{c(k)}{a(k)}\).</li>
            <li>\(a(k) = 0\) und \(c(k) \neq 0\): keine Lösung. \(a(k) = 0\) und \(c(k) = 0\): \(''' + L + r''' = \mathbb{R}\).</li>
          </ul>
          <p>\(k \cdot x + 6 = 2x + 3k \iff (k - 2)\,x = 3(k - 2)\): für \(k \neq 2\) ist \(x = 3\), für \(k = 2\) ist \(''' + L + r''' = \mathbb{R}\).</p>
          <p><b>Quadratisch:</b> Die Diskriminante wird eine Funktion von \(k\). \(x^2 - 6x + k = 0\): \(D(k) = 36 - 4k\) — zwei Lösungen für \(k \lt 9\), eine (\(x = 3\)) für \(k = 9\), keine für \(k \gt 9\).</p>
          <p><b>Parameter vor \(x^2\):</b> zuerst den Fall untersuchen, in dem er null wird — dann ist die Gleichung linear (sofern der Faktor vor \(x\) nicht auch null ist), und \(D\) gilt nicht.</p><p><b>Mehrere kritische Werte:</b> Ist \(a(k)\) selbst quadratisch, etwa \((k^2 - 9)\,x = k - 3\), wird es an zwei Stellen null (\(k = \pm 3\)) — jede einzeln einsetzen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Durch \(a(k)\) teilen, ohne den Fall \(a(k) = 0\) zu prüfen.</p>
          <p>Bei \(m x^2 - 4x - 3 = 0\) nur \(D(m) = 16 + 12m\) untersuchen: Für \(m = 0\) gibt es genau eine Lösung \(x = -\tfrac{3}{4}\), obwohl \(D \gt 0\) wäre.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 15, [
    ('5a', 3, r'Löse \(k x - 4 = 2x + k\) in Abhängigkeit von \(k\).',
     r'<p>\((k - 2)\,x = k + 4\). Für \(k \neq 2\): \(x = \dfrac{k + 4}{k - 2}\). Für \(k = 2\): \(0 = 6\), \(' + L + r' = \{\,\}\).</p>', ''),
    ('5b', 3, r'Löse \((k^2 - 9)\,x = k - 3\) in Abhängigkeit von \(k\). Achtung: Es gibt zwei kritische Werte.',
     r'<p>\(k^2 - 9 = (k - 3)(k + 3) = 0\) bei \(k = 3\) und \(k = -3\). \(k = 3\): \(0 = 0\), \(' + L + r' = \mathbb{R}\). \(k = -3\): \(0 = -6\), \(' + L + r' = \{\,\}\). Sonst: \(x = \dfrac{k - 3}{(k - 3)(k + 3)} = \dfrac{1}{k + 3}\).</p>', ''),
    ('5c', 3, r'Für welche \(k\) hat \(x^2 + 8x + k = 0\) zwei, eine oder keine Lösung? Die drei Parabeln \(y = x^2 + 8x + k\) gehören zu \(k = 12\), \(16\) und \(20\) — ordne zu.',
     r'<p>\(D = 64 - 4k\): zwei für \(k \lt 16\), eine (\(x = -4\)) für \(k = 16\), keine für \(k \gt 16\). A: zwei Nullstellen, \(k = 12\); B: berührt, \(k = 16\); C: keine, \(k = 20\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-k="q,1,8,12" data-fenster="-8,1,-5,6" data-titel="A" data-xm="-6,-4,-2" data-ym="-4,4"></svg><svg class="mini" data-k="q,1,8,16" data-fenster="-8,1,-5,6" data-titel="B" data-xm="-6,-4,-2" data-ym="-4,4"></svg><svg class="mini" data-k="q,1,8,20" data-fenster="-8,1,-5,6" data-titel="C" data-xm="-6,-4,-2" data-ym="-4,4"></svg></div>'),
    ('5d', 4, r'Diskutiere \(m x^2 + 6x + 3 = 0\) vollständig — auch den Fall \(m = 0\).',
     r'<p>\(m = 0\): linear, \(6x + 3 = 0\), \(x = -0.5\). \(m \neq 0\): \(D = 36 - 12m\). \(m = 3\): eine Lösung \(x = -\tfrac{6}{6} = -1\). \(m \lt 3\), \(m \neq 0\): zwei. \(m \gt 3\): keine.</p>', ''),
    ('5e', 2, r'Warum prüft man bei \(a(k) \cdot x = c(k)\) zuerst den Fall \(a(k) = 0\)?',
     r'<p>Für die Lösung \(x = \tfrac{c(k)}{a(k)}\) wird durch \(a(k)\) geteilt — das geht nur, wenn \(a(k) \neq 0\). Den Fall \(a(k) = 0\) muss man getrennt ansehen: Dort verschwindet \(x\), und es gibt keine oder unendlich viele Lösungen.</p>', ''),
], zwei=False)
k5 = kapitel(5, 'parameter', 'Parameterdiskussion', 40,
             r'Du bringst eine Gleichung mit Parameter auf die Form \(a(k) \cdot x = c(k)\) oder untersuchst \(D(k)\), bestimmst die kritischen Werte und gibst die Lösungsmenge für alle Fälle an — auch, wenn der Faktor vor \(x^2\) null wird.',
             ('g2-2-lp-parameter', 'Parameterdiskussion'),
             sim5, ('g2-2-lp-kontrolle-parameter', 'Kontrollfragen zur Parameterdiskussion'),
             fest5, [uebung('param-linear', 'Kritischer Wert (linear)'), uebung('param-quadr', 'Genau eine Lösung')],
             auf5, f'<a href="{TA}#parameter">Themenseite 2.2a, Parameterdiskussion</a> und <a href="{TB}#parameter">2.2b, Parameterdiskussion</a>', komp='K5')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 1.3 · 1.4 · 2.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Terme umformen, ausklammern, die binomischen Formeln, Quadratwurzeln und die Probe. Wenn das wackelt: <a href="../grundlagen/g1-3-algebraische-terme.html">Teilgebiet 1.3, Algebraische Terme</a>, <a href="../grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html">1.4, Quadratwurzeln</a> und <a href="../grundlagen/g2-1-grundlagen.html">Teilgebiet 2.1, Grundlagen der Gleichungen</a>.</p>
      ''' + clipkarte('g2-1-aequivalenzumformungen', 'Gleichungen: was die Lösungsmenge erhält') + '''
''' + test('t0', 'Vortest', 12, [
    ('0a', 3, r'Vereinfache \(3(x - 2) - (2x - 5)\) und multipliziere \((x + 3)^2\) aus.',
     r'<p>\(3x - 6 - 2x + 5 = x - 1\); \(x^2 + 6x + 9\).</p><p class="komm">Minus vor der Klammer und das mittlere Glied des Binoms braucht jedes Kapitel.</p>', ''),
    ('0b', 2, r'Klammere so viel wie möglich aus: \(6x^2 - 9x\); \(x^2 + 4x\).',
     r'<p>\(3x\,(2x - 3)\); \(x\,(x + 4)\).</p><p class="komm">Falsch? Genau das braucht Kapitel 2.</p>', ''),
    ('0c', 3, r'Schreib als Produkt: \(x^2 - 10x + 25\); \(x^2 - 49\).',
     r'<p>\((x - 5)^2\); \((x - 7)(x + 7)\).</p><p class="komm">Binomische Formeln rückwärts brauchen Kapitel 3 und 4.</p>', ''),
    ('0d', 2, r'Berechne \(\sqrt{49}\) und \(\sqrt{\tfrac{9}{4}}\). Welche Zahlen haben das Quadrat \(16\)?',
     r'<p>\(7\); \(\tfrac{3}{2} = 1.5\); \(4\) und \(-4\).</p>', ''),
    ('0e', 2, r'Ist \(x = 2\) eine Lösung von \(3x - 4 = x\)? Begründe mit der Probe.',
     r'<p>Ja: links \(6 - 4 = 2\), rechts \(2\).</p><p class="komm">Die Probe gehört zu jeder Gleichung, die du löst.</p>', ''),
]) + '''
      <p class="komm">Weniger als 8 von 12 Punkten: zuerst die verlinkten Teilgebiete, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/lineare-quadratische-gleichungen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 2.2 · Kapitel 1–5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel: G1, G2 → 1; G3 → 2; G4, G5 → 3; G6 → 4; G7, G8 → 5</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Lineare und quadratische Gleichungen, Version 1.0 (06.10.2026). Gebaut aus
     scripts/lp/lineare-quadratische-gleichungen/seite.py — Änderungen dort, nicht in dieser Datei.
     Grundlage: Leitfaden des Auftraggebers (HOWTO-GleichungLP.md, 06.10.2026) und HOWTO-leitprogramme.md.

     RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2 «Lineare und quadratische Gleichungen» (gedruckte
     Seite 42), eine Kompetenz:
       «lineare und quadratische Gleichungen lösen, verschiedene Lösungsmethoden erklären und
        anwenden, inkl. Parameterdiskussion (auch ohne Hilfsmittel)»
     Für die Kompetenzmatrix in fünf Teile gegliedert:
       K1  lineare Gleichungen lösen (mit Äquivalenz, Typ und Probe aus 2.1)
       K2  quadratische Gleichungen mit Ausklammern und Nullprodukt lösen und das Verfahren erklären
       K3  quadratische Gleichungen mit Wurzelziehen, quadratischer Ergänzung und Mitternachtsformel lösen
       K4  verschiedene Lösungsmethoden vergleichen und begründet wählen (Typ bestimmen, Faktorisieren, Probe)
       K5  Parameterdiskussion, linear und quadratisch, inkl. verschwindendem Leitkoeffizienten
     Unterstützend aus 2.1: «algebraische Äquivalenz erklären und anwenden», «den Typ einer Gleichung
     bestimmen und beim Lösen entsprechend beachten, Lösungs- und Umformungsmethoden zielführend
     einsetzen sowie Lösungen überprüfen».

     Kompetenzmatrix (Kompetenz | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | 1 | 1a–1f | G1, G2
       K2 | 2 | 2a–2e | G3
       K3 | 3 | 3a–3g | G4, G5
       K4 | 4 | 4a–4e | G6
       K5 | 5 | 5a–5e | G7, G8
     Kein Kapitelziel ohne Kompetenz. Alles ohne Taschenrechner (RLP-Vermerk).

     Bewusst weggelassen (→ Themenseiten 2.2a/2.2b): lineare und quadratische Ungleichungen,
     Bruchgleichungen mit Definitionsmenge, Substitution (biquadratisch), Satz von Vieta als eigenes
     Verfahren (hier nur im Zweiklammersatz), die pq-Formel (nur erwähnt), Gleichungssysteme (2.3).

     Konventionen wie auf den Themenseiten: 𝕃 mit Strichpunkt, leere Menge {}, 𝕃 = ℝ,
     Mitternachtsformel mit D = b² − 4ac, «Satz vom Nullprodukt», Normalform a·x + b = 0,
     Zwischenform a·x = c, Parameter k (bzw. m vor x²). Umformung rechts neben der Zeile wie im Heft.
     Farben: Gleichung und Graph blau, Umformung und Parameter orange, Lösungen grün, Fehler rot.

     Muster je Kapitel: ① Einführungsclip → ② Umformer (Kapitel 1–4) bzw. Simulation (Kapitel 5) mit
     Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben
     mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/lineare-quadratische-gleichungen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Lineare und quadratische Gleichungen</h1>
      <p class="unter">Zuschauen, umformen, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 2.2</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Lineare Gleichungen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Nullprodukt</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Mitternachtsformel</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Verfahren wählen</span></a></li>
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
          <li><b>② Tüfteln:</b> Im Umformer wählst du jeden Schritt selbst und gibst am Schluss die Lösungsmenge ein — er zeigt ✓, wenn sie stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2 — eine Kompetenz:</p>
        <p>lineare und quadratische Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden, inkl. Parameterdiskussion <span class="ohm">auch ohne Hilfsmittel</span></p>
        <p class="rlp-quelle">Hier in fünf Teile gegliedert:</p>
        <ul>
          <li><b>K1</b> lineare Gleichungen lösen, mit Äquivalenzumformungen und Probe (dazu aus 2.1) — Kapitel 1</li>
          <li><b>K2</b> quadratische Gleichungen mit Ausklammern und Nullprodukt lösen und das Verfahren erklären — Kapitel 2</li>
          <li><b>K3</b> mit Wurzelziehen, quadratischer Ergänzung und Mitternachtsformel lösen — Kapitel 3</li>
          <li><b>K4</b> Lösungsmethoden vergleichen und begründet wählen, den Typ bestimmen — Kapitel 4</li>
          <li><b>K5</b> Parameterdiskussion — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Parabeln dienen als Bild der Lösungen (Nullstellen) — die Funktionssicht «Gleichungen mithilfe von Funktionen visualisieren» gehört zu GF 3.1.</p>
        <p class="rlp-quelle">Nicht hier, sondern auf den Themenseiten <a href="''' + TA + '''">2.2a</a> und <a href="''' + TB + '''">2.2b</a>: Ungleichungen, Bruchgleichungen, Substitution. Gleichungssysteme: Teilgebiet 2.3.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Lineare und quadratische Gleichungen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (06.10.2026): Vorwissen 10 (vorab) · K1 40 · K2 40 · K3 45 · K4 40 · K5 40 · Gesamttest 30 = 245 min
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
