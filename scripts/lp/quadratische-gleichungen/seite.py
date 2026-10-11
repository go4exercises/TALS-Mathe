"""Baut leitprogramme/quadratische-gleichungen.html aus einer Kapitelbeschreibung (11.10.2026).

  python3 scripts/lp/quadratische-gleichungen/seite.py

Leitprogramm zur Themenseite GF 2.2b Quadratische Gleichungen (grundlagen/g2-2b-quadratische-gleichungen.html).
Löst zusammen mit dem Leitprogramm «Lineare Gleichungen» (2.2a) das gemeinsame Leitprogramm «Lineare und
quadratische Gleichungen» ab und ersetzt das ältere, ausgeblendete Leitprogramm unter derselben Adresse.

Gerüst: Beim ersten Lauf kommen Kopf (bis </style>) und Grundskript aus leitprogramme/lineare-quadratische-gleichungen.html,
SEO-Block und Footer aus der bestehenden Zieldatei (beide schreibt scripts/build-seo.py; sie bleiben unangetastet).
Danach liest das Skript alles aus der eigenen Seite. Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei.
Danach Pre-Flight. Siehe README.md.
"""
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/quadratische-gleichungen.html'
NAME = 'Quadratische Gleichungen'
SCHLUESSEL = 'lp-quadratische-gleichungen-'
MARKE_CSS = '\n/* ════════ Quadratische Gleichungen'
MARKE_JS = '<script>\n/* Leitprogramm Quadratische Gleichungen —'

ziel_alt = open(ZIEL).read()
if MARKE_JS in ziel_alt:
    alt = ziel_alt
else:                                          # erster Lauf: Gerüst vom Vorgänger, SEO und Footer vom alten Ziel
    alt = open(R + 'leitprogramme/lineare-quadratische-gleichungen.html').read()
    a, b = alt.index('<!-- SEO:ANFANG'), alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    za, zb = ziel_alt.index('<!-- SEO:ANFANG'), ziel_alt.index('<!-- SEO:ENDE -->') + len('<!-- SEO:ENDE -->')
    alt = alt[:a] + ziel_alt[za:zb] + alt[b:]
    a, b = alt.index('<!-- FUSS:ANFANG'), alt.index('<!-- FUSS:ENDE -->') + len('<!-- FUSS:ENDE -->')
    za, zb = ziel_alt.index('<!-- FUSS:ANFANG'), ziel_alt.index('<!-- FUSS:ENDE -->') + len('<!-- FUSS:ENDE -->')
    alt = alt[:a] + ziel_alt[za:zb] + alt[b:]
    alt = re.sub(r'<title>.*?</title>', '<title>Leitprogramm ' + NAME + '</title>', alt, count=1)
    alt = alt.replace('lp-gleichungen-', SCHLUESSEL)

kopf = alt[:alt.index('</style>')]
for marke in ('\n/* ════════ Gleichungen', MARKE_CSS):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
kopf = kopf.rstrip('\n') + '\n'
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Lineare und quadratische Gleichungen —'), alt.find(MARKE_JS)) if k > 0)
basis = alt[i:j]
assert SCHLUESSEL + 'thema' in basis and SCHLUESSEL + 'stand' in basis, 'localStorage-Schlüssel fehlen'
# Footer: der Block zwischen den FUSS-Marken bleibt, wie build-seo.py ihn geschrieben hat.
fuss = alt[alt.index('<!-- FUSS:ANFANG'):]

CSS = '''
/* ════════ Quadratische Gleichungen (11.10.2026) — Kapitelmuster mit Umformer ════════
   Grundgerüst (Leiste, Übungen, Minigrafen, Festhalten, PDF-Weg, Umformer) aus dem Leitprogramm «Lineare und
   quadratische Gleichungen». Farben: Gleichung blau, Umformung und Parameter orange, Lösungen grün, Fehler rot. */
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


PUNKTE = {}


def test(tid, titel, punkte, aufgaben, zwei=False):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte, sum(a[1] for a in aufgaben))
    PUNKTE[tid] = punkte
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''


MINUTEN = {}


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp):
    MINUTEN[n] = zeit
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


TB = '../grundlagen/g2-2b-quadratische-gleichungen.html'
L = r'\mathbb{L}'


def mini(k, fenster, xm, ym, punkte=None, titel=None, gross=True):
    a = f' data-punkte="{punkte}"' if punkte else ''
    t = f' data-titel="{titel}"' if titel else ''
    return f'<svg class="mini{" gross" if gross else ""}" data-k="{k}" data-fenster="{fenster}" data-xm="{xm}" data-ym="{ym}"{a}{t}></svg>'


# ------------------------------------------------------------------ Kapitel 1
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Quadratische Gleichung, Normalform, Wurzelziehen</div>
          <p>Eine Gleichung der Form \(a x^2 + b x + c = 0\) mit \(a \neq 0\) (\(a, b, c \in \mathbb{R}\)) heisst <b>quadratische Gleichung</b>. \(a x^2\) ist das quadratische, \(b x\) das lineare, \(c\) das konstante Glied. Ob eine Gleichung quadratisch ist, zeigt sich erst nach dem <b>Ordnen</b>: Klammern auflösen, alles auf eine Seite. Heben sich die \(x^2\) weg, ist sie linear.</p>
          <p><b>Normalform:</b> Durch \(a\) geteilt steht \(x^2 + p x + q = 0\) da. Die Lösungsmenge bleibt gleich: \(2x^2 + 8x - 10 = 0 \;\mid :2\;\) gibt \(x^2 + 4x - 5 = 0\).</p>
          <p><b>Wurzelziehen</b>, wenn das lineare Glied fehlt (\(b = 0\)): erst \(x^2\) allein auf eine Seite, dann</p>
          <ul>
            <li>\(x^2 = r\) mit \(r \gt 0\): zwei Lösungen \(x = \pm\sqrt{r}\);</li>
            <li>\(x^2 = 0\): eine Lösung \(x = 0\);</li>
            <li>\(x^2 = r\) mit \(r \lt 0\): keine Lösung, \(''' + L + r''' = \{\,\}\) — ein Quadrat ist nie negativ.</li>
          </ul>
          <p>Ebenso mit Klammer: \((x - 2)^2 = 9 \Rightarrow x - 2 = \pm 3 \Rightarrow x = 5\) oder \(x = -1\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Nur die positive Wurzel: Aus \(x^2 = 9\) folgt \(x = \pm 3\), denn auch \((-3)^2 = 9\).</p>
          <p>Gliedweise Wurzel ziehen: Aus einer Summe oder Differenz zieht man nicht Glied für Glied die Wurzel. Erst das Quadrat allein auf eine Seite bringen.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 2, r'Welche Gleichungen sind quadratisch? Ordne zuerst. (a) \(x^2 - 3x = x^2 + 5\) (b) \(x\,(x - 4) = 7\) (c) \(5x - 2 = 0\) (d) \(3 - x^2 = 0\)',
     r'<p>(b) und (d). (b) ausmultipliziert: \(x^2 - 4x - 7 = 0\). (d): \(-x^2 + 3 = 0\). (a): Die \(x^2\) heben sich weg, es bleibt \(-3x = 5\) — linear. (c) ist linear.</p>', ''),
    ('1b', 2, r'Bring \(-2x^2 + 10x - 8 = 0\) auf die Normalform und gib \(p\) und \(q\) an.',
     r'<p>Durch \(-2\) teilen (jedes Vorzeichen dreht): \(x^2 - 5x + 4 = 0\), also \(p = -5\), \(q = 4\).</p>', ''),
    ('1c', 2, r'Löse (a) \(2x^2 = 162\) und (b) \(x^2 + 9 = 0\).',
     r'<p>(a) \(x^2 = 81\), \(' + L + r' = \{-9;\ 9\}\). (b) \(x^2 = -9\): Ein Quadrat ist nie negativ, \(' + L + r' = \{\,\}\).</p>', ''),
    ('1d', 3, r'Löse \((x - 5)^2 = 36\) und mach die Probe.',
     r'<p>\(x - 5 = \pm 6\), also \(x = 11\) oder \(x = -1\): \(' + L + r' = \{-1;\ 11\}\). Probe: \((11 - 5)^2 = 36\) ✓; \((-1 - 5)^2 = (-6)^2 = 36\) ✓.</p>', ''),
    ('1e', 2, r'Jemand löst \(x^2 + 25 = 169\) so: «gliedweise Wurzel ziehen: \(x + 5 = 13\), also \(x = 8\)». Warum ist das falsch? Löse richtig.',
     r'<p>\(\sqrt{x^2 + 25}\) ist nicht \(x + 5\) — die Wurzel einer Summe ist nicht die Summe der Wurzeln. Probe: \(8^2 + 25 = 89 \neq 169\). Richtig: \(x^2 = 144\), \(' + L + r' = \{-12;\ 12\}\).</p>', ''),
    ('1f', 2, r'Abgebildet sind \(y = (x - 1)^2\) und \(y = 4\). Lies die Lösungen von \((x - 1)^2 = 4\) ab und bestätige sie mit Wurzelziehen.',
     r'<p>Die Waagrechte schneidet die Parabel bei \(x = -1\) und \(x = 3\). Rechnung: \(x - 1 = \pm 2\), \(' + L + r' = \{-1;\ 3\}\).</p>',
     '\n            <div class="mini-reihe">' + mini('q,1,-2,1;g,0,4', '-3,5,-1,7', '-1,1,2,3', '2,4') + '</div>'),
])
k1 = kapitel(1, 'wurzelziehen', 'Erkennen und Wurzel ziehen', 40,
             r'Du erkennst quadratische Gleichungen, bringst sie auf die Normalform und löst Gleichungen wie \(a x^2 + c = 0\) oder \((x - 2)^2 = 9\) mit Wurzelziehen — zwei, eine oder keine Lösung.',
             ('g2-2b-lp-wurzel', 'Erkennen und Wurzel ziehen'),
             umformer(1, 'Umformer: quadratische Gleichungen mit Wurzelziehen lösen'),
             ('g2-2b-lp-kontrolle-wurzel', 'Kontrollfragen zum Wurzelziehen'),
             fest1, [uebung('normalform', 'Normalform'), uebung('wurzel', 'Wurzel ziehen')],
             auf1, f'<a href="{TB}#definition">Themenseite 2.2b, Definition und Normalformen</a>', komp='K1')

# ------------------------------------------------------------------ Kapitel 2
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Faktorisieren und Nullprodukt</div>
          <p><b>Satz vom Nullprodukt:</b> Ein Produkt ist genau dann null, wenn mindestens ein Faktor null ist: \(A \cdot B = 0 \iff A = 0 \;\text{oder}\; B = 0\). Darum zuerst <b>auf null bringen</b>, dann als Produkt schreiben, dann jeden Faktor null setzen.</p>
          <ul>
            <li><b>Ausklammern</b>, wenn die Zahl ohne \(x\) fehlt (\(c = 0\)): \(x^2 = 5x \iff x\,(x - 5) = 0\), also \(x = 0\) oder \(x = 5\). Eine Lösung ist dann immer \(0\).</li>
            <li><b>Binom erkennen:</b> \(x^2 - 6x + 9 = (x - 3)^2\) — nur eine Lösung, \(x = 3\). Und \(a^2 - b^2 = (a - b)(a + b)\): \(x^2 - 36 = (x - 6)(x + 6)\).</li>
            <li><b>Zweiklammersatz</b> für die Normalform, wenn sie zwei ganzzahlige Lösungen hat: \(x^2 + px + q = (x - x_1)(x - x_2)\). Gesucht sind die Lösungen \(x_1\), \(x_2\) mit Summe \(-p\) und Produkt \(q\): \(x^2 - 7x + 12 = (x - 3)(x - 4)\), denn \(3 + 4 = 7\) und \(3 \cdot 4 = 12\). In Teilgebiet 1.3 suchst du die Zahlen in den Klammern, \((x + r)(x + s)\) mit \(r + s = p\): dort \(-3\) und \(-4\). Es sind dieselben Zahlen mit umgekehrtem Vorzeichen — die Lösungen.</li>
          </ul>
          <p><b>Satz von Vieta:</b> Für die Lösungen von \(x^2 + px + q = 0\) gilt \(x_1 + x_2 = -p\) und \(x_1 \cdot x_2 = q\). Damit faktorisiert man — und kontrolliert gefundene Lösungen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Durch \(x\) teilen: Aus \(x^2 = 5x\) wird \(x = 5\) — und \(x = 0\) fehlt. Teilen durch \(x\) setzt \(x \neq 0\) voraus.</p>
          <p>Das Nullprodukt nur bei «\(= 0\)»: \(x\,(x - 5) = 6\) heisst <b>nicht</b> \(x = 6\) oder \(x - 5 = 6\).</p>
          <p>Vorzeichen: Aus dem Faktor \((x + 5)\) folgt die Lösung \(x = -5\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 2, r'Löse \(4x^2 + 20x = 0\) und mach die Probe.',
     r'<p>\(4x\,(x + 5) = 0\), also \(x = 0\) oder \(x = -5\): \(' + L + r' = \{-5;\ 0\}\). Probe: \(0 + 0 = 0\) ✓; \(4 \cdot 25 - 100 = 0\) ✓.</p>', ''),
    ('2b', 2, r'Löse \(x^2 - 14x + 49 = 0\).',
     r'<p>Binom: \((x - 7)^2 = 0\), also \(x - 7 = 0\): \(' + L + r' = \{7\}\).</p><p class="komm">Prüfe das mittlere Glied: \(2 \cdot x \cdot 7 = 14x\) ✓.</p>', ''),
    ('2c', 3, r'Löse \(x^2 + 3x - 28 = 0\) mit dem Zweiklammersatz und kontrolliere mit Vieta.',
     r'<p>Gesucht: Summe \(-3\), Produkt \(-28\): \(-7\) und \(4\). \((x + 7)(x - 4) = 0\), \(' + L + r' = \{-7;\ 4\}\). Vieta: \(-7 + 4 = -3 = -p\) ✓; \(-7 \cdot 4 = -28 = q\) ✓.</p>', ''),
    ('2d', 2, r'Jemand rechnet: «\((x - 1)(x - 4) = 10 \Rightarrow x - 1 = 10\) oder \(x - 4 = 10\), also \(x = 11\) oder \(x = 14\)». Was ist falsch? Mach die Probe und löse richtig.',
     r'<p>Das Nullprodukt gilt nur, wenn rechts \(0\) steht. Probe: \(10 \cdot 7 = 70 \neq 10\); \(13 \cdot 10 = 130 \neq 10\). Richtig: \(x^2 - 5x + 4 = 10\), also \(x^2 - 5x - 6 = 0\), \((x - 6)(x + 1) = 0\): \(' + L + r' = \{-1;\ 6\}\). Probe: \(5 \cdot 2 = 10\) ✓; \((-2)(-5) = 10\) ✓.</p>', ''),
    ('2e', 2, r'Abgebildet ist \(y = x^2 + 2x - 3\). Lies die Nullstellen ab und schreib \(x^2 + 2x - 3 = 0\) in Faktorform. Kontrolliere mit Vieta.',
     r'<p>Nullstellen \(-3\) und \(1\): \((x + 3)(x - 1) = 0\). Vieta: \(-3 + 1 = -2 = -p\) ✓; \(-3 \cdot 1 = -3 = q\) ✓.</p>',
     '\n            <div class="mini-reihe">' + mini('q,1,2,-3', '-5,3,-5,4', '-3,-2,-1,1,2', '-4,-2,2') + '</div>'),
    ('2f', 2, r'Gib eine quadratische Gleichung in Normalform an, die die Lösungen \(1\) und \(-6\) hat. Warum funktioniert dein Vorgehen?',
     r'<p>\((x - 1)(x + 6) = 0\), ausmultipliziert \(x^2 + 5x - 6 = 0\). Ein Produkt ist genau dann null, wenn ein Faktor null ist — das passiert genau bei \(1\) und \(-6\). Kontrolle mit Vieta: Summe \(-5 = -p\), Produkt \(-6 = q\).</p>', ''),
])
k2 = kapitel(2, 'faktorisieren', 'Ausklammern und faktorisieren', 45,
             r'Du löst quadratische Gleichungen mit dem Satz vom Nullprodukt — durch Ausklammern, mit einer binomischen Formel oder mit dem Zweiklammersatz (Satz von Vieta) — und erklärst, warum man nicht durch \(x\) teilt.',
             ('g2-2b-lp-faktorisieren', 'Ausklammern und faktorisieren'),
             umformer(2, 'Umformer: ausklammern und faktorisieren'),
             ('g2-2b-lp-kontrolle-faktorisieren', 'Kontrollfragen zum Faktorisieren'),
             fest2, [uebung('ausklammern', 'Ausklammern und lösen'), uebung('binom', 'Binom erkennen'), uebung('zweiklammer', 'Zweiklammersatz')],
             auf2, f'<a href="{TB}#faktorisieren">Themenseite 2.2b, Faktorisieren</a> und <a href="{TB}#vieta">Satz von Vieta</a>', komp='K2')

# ------------------------------------------------------------------ Kapitel 3
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Quadratische Ergänzung, Mitternachtsformel, Diskriminante</div>
          <p><b>Quadratische Ergänzung</b> (Faktor \(1\) vor \(x^2\), sonst zuerst durch \(a\) teilen): die Zahl ohne \(x\) nach rechts, dann bei \(x^2 + px\) beidseitig \(\left(\tfrac{p}{2}\right)^2\) addieren — links entsteht ein Binom. \(x^2 + 6x - 16 = 0 \Rightarrow x^2 + 6x = 16 \Rightarrow (x + 3)^2 = 25 \Rightarrow x = 2\) oder \(x = -8\).</p>
          <p><b>Mitternachtsformel</b> für \(a x^2 + b x + c = 0\) mit \(a \neq 0\):</p>
          <p>\[ x_{1,2} = \frac{-b \pm \sqrt{D}}{2a}, \qquad D = b^2 - 4ac \]</p>
          <p>Sie liefert Lösungen, wenn \(D \ge 0\) ist; bei \(D \lt 0\) zeigt sie, dass es keine gibt. Woher sie kommt: die Ergänzung allgemein. Durch \(a\) teilen, \(\tfrac{c}{a}\) hinüberbringen, \(\left(\tfrac{b}{2a}\right)^2\) ergänzen: \(\left(x + \tfrac{b}{2a}\right)^2 = \tfrac{b^2 - 4ac}{4a^2}\). Wurzel ziehen und \(\tfrac{b}{2a}\) hinüberbringen.</p>
          <p>Die <b>Diskriminante</b> \(D\) entscheidet über die Anzahl der Lösungen:</p>
          <ul>
            <li>\(D \gt 0\): zwei Lösungen — die Parabel \(y = a x^2 + b x + c\) schneidet die \(x\)-Achse zweimal;</li>
            <li>\(D = 0\): eine (doppelte) Lösung \(x = -\tfrac{b}{2a}\) — die Parabel berührt die \(x\)-Achse;</li>
            <li>\(D \lt 0\): keine Lösung, \(''' + L + r''' = \{\,\}\) — rechts stünde nach dem Ergänzen eine negative Zahl.</li>
          </ul>
          <p><b>Exakt rechnen:</b> Ist \(D\) keine Quadratzahl, bleibt die Wurzel stehen. Teilweise Wurzel ziehen und kürzen: \(\sqrt{20} = \sqrt{4 \cdot 5} = 2\sqrt{5}\), also \(\tfrac{2 \pm 2\sqrt{5}}{2} = 1 \pm \sqrt{5}\).</p>
          <p>Für die Normalform vereinfacht sich die Formel zur pq-Formel; mehr dazu auf der Themenseite.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Vorzeichen in \(D\): Bei \(c \lt 0\) wird \(-4ac\) positiv: \(2x^2 - 5x - 3\) hat \(D = 25 + 24\).</p>
          <p>Vorne steht \(-b\): Bei \(b = -5\) ist \(-b = 5\). Und unten steht \(2a\), unter dem ganzen Zähler.</p>
          <p>Ergänzt wird das Quadrat der <b>halben</b> Zahl vor \(x\): zu \(x^2 + 8x\) gehört \(16\), nicht \(64\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 16, [
    ('3a', 3, r'Löse \(x^2 - 8x + 13 = 0\) mit quadratischer Ergänzung. Gib die Lösungen exakt an.',
     r'<p>\(x^2 - 8x = -13\), plus \(\left(\tfrac{8}{2}\right)^2 = 16\): \((x - 4)^2 = 3\), \(x - 4 = \pm\sqrt{3}\). \(' + L + r' = \{4 - \sqrt{3};\ 4 + \sqrt{3}\}\) (\(\approx 2.27\) und \(5.73\)).</p><p class="komm">Steht rechts keine Quadratzahl, bleibt die Wurzel stehen.</p>', ''),
    ('3b', 3, r'Löse \(2x^2 + x - 6 = 0\) mit der Mitternachtsformel.',
     r'<p>\(a = 2\), \(b = 1\), \(c = -6\): \(D = 1 + 48 = 49\), \(x = \dfrac{-1 \pm 7}{4}\). \(' + L + r' = \{-2;\ 1.5\}\).</p>', ''),
    ('3c', 2, r'Löse \(x^2 - 2x - 4 = 0\) exakt (ohne Taschenrechner).',
     r'<p>\(D = 4 + 16 = 20\), \(\sqrt{20} = \sqrt{4 \cdot 5} = 2\sqrt{5}\), also \(x = \dfrac{2 \pm 2\sqrt{5}}{2} = 1 \pm \sqrt{5}\). \(' + L + r' = \{1 - \sqrt{5};\ 1 + \sqrt{5}\}\).</p><p class="komm">Die Wurzel bleibt stehen, wenn \(D\) keine Quadratzahl ist.</p>', ''),
    ('3d', 3, r'Wie viele Lösungen? Entscheide mit \(D\), ohne zu lösen: (a) \(x^2 + 5x + 7 = 0\) (b) \(4x^2 - 20x + 25 = 0\) (c) \(3x^2 - x - 1 = 0\)',
     r'<p>(a) \(D = 25 - 28 = -3\): keine. (b) \(D = 400 - 400 = 0\): eine. (c) \(D = 1 + 12 = 13\): zwei.</p>', ''),
    ('3e', 3, r'Ergänze \(x^2 + px + q = 0\) allgemein quadratisch, bis \(\left(x + \tfrac{p}{2}\right)^2 = \ldots\) dasteht. Erkläre daran, woher die Lösungsformel kommt und warum es keine Lösung gibt, wenn die rechte Seite negativ ist.',
     r'<p>\(x^2 + px = -q\), plus \(\left(\tfrac{p}{2}\right)^2\): \(\left(x + \tfrac{p}{2}\right)^2 = \left(\tfrac{p}{2}\right)^2 - q\). Ist die rechte Seite negativ, gibt es keine Lösung — ein Quadrat ist nie negativ. Sonst Wurzel ziehen: \(x = -\tfrac{p}{2} \pm \sqrt{\left(\tfrac{p}{2}\right)^2 - q}\). Das ist die Lösungsformel für die Normalform; mit \(a \neq 1\) teilt man zuerst durch \(a\) und erhält genauso die Mitternachtsformel.</p>', ''),
    ('3f', 2, r'Die Parabeln A, B, C gehören zu \(y = x^2 - 4x + c\) mit \(c = 3\), \(4\) und \(6\). Ordne zu und gib jeweils \(D\) an.',
     r'<p>\(D = 16 - 4c\). \(c = 3\): \(D = 4\), zwei Nullstellen — B. \(c = 4\): \(D = 0\), berührt — C. \(c = 6\): \(D = -8\), keine — A.</p>',
     '\n            <div class="mini-reihe">' + mini('q,1,-4,6', '-1,5,-2,6', '1,2,3,4', '2,4', titel='A', gross=False)
     + mini('q,1,-4,3', '-1,5,-2,6', '1,2,3,4', '2,4', titel='B', gross=False)
     + mini('q,1,-4,4', '-1,5,-2,6', '1,2,3,4', '2,4', titel='C', gross=False) + '</div>'),
])
k3 = kapitel(3, 'formel', 'Quadratisch ergänzen und Mitternachtsformel', 45,
             r'Du ergänzt quadratisch, erklärst damit, woher die Mitternachtsformel kommt, löst jede quadratische Gleichung mit der Formel und bestimmst mit der Diskriminante, wie viele Lösungen es gibt.',
             ('g2-2b-lp-formel', 'Quadratisch ergänzen und Mitternachtsformel'),
             umformer(3, 'Umformer: quadratisch ergänzen und Mitternachtsformel'),
             ('g2-2b-lp-kontrolle-formel', 'Kontrollfragen zu Ergänzung und Formel'),
             fest3, [uebung('ergaenzen', 'Quadratisch ergänzen'), uebung('mitternacht', 'Mitternachtsformel'), uebung('exakt', 'Exakt mit Wurzel'), uebung('anzahl', 'Anzahl Lösungen')],
             auf3, f'<a href="{TB}#verfahren">Themenseite 2.2b, Lösungsverfahren</a> und <a href="{TB}#diskriminante">Diskriminante</a>', komp='K3')

# ------------------------------------------------------------------ Kapitel 4
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Das passende Verfahren</div>
          <p><b>Zuerst ordnen:</b> Klammern auflösen und alles auf eine Seite. Erst jetzt zeigt sich der <b>Typ</b> — heben sich die \(x^2\) weg, ist die Gleichung linear: \((x - 1)^2 = x^2 + 7 \Rightarrow -2x + 1 = 7 \Rightarrow x = -3\).</p>
          <ul>
            <li>Kein lineares Glied (\(b = 0\)): <b>Wurzelziehen</b>.</li>
            <li>Keine Zahl ohne \(x\) (\(c = 0\)): <b>Ausklammern</b> und Nullprodukt.</li>
            <li>Zerlegung sichtbar: <b>Faktorisieren</b> — Binom oder Zweiklammersatz mit Summe \(-p\) und Produkt \(q\).</li>
            <li>Sonst: <b>Mitternachtsformel</b> — sie geht immer (bei \(D \lt 0\) zeigt sie, dass es keine Lösung gibt), ist aber am aufwendigsten.</li>
          </ul>
          <p><b>Kontrolle:</b> die Probe in der Ausgangsgleichung oder, bei der Normalform, der Satz von Vieta: \(x^2 - 8x + 15 = 0\) mit \(3\) und \(5\): \(3 + 5 = 8 = -p\), \(3 \cdot 5 = 15 = q\) ✓.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Ein Verfahren anwenden, bevor rechts \(0\) steht: \(x\,(x + 4) = 12\) ist kein Nullprodukt. Erst \(x^2 + 4x - 12 = 0\), dann \((x + 6)(x - 2) = 0\).</p>
          <p>Den Zweiklammersatz bei einem Faktor vor \(x^2\): Er braucht die Normalform. Bei \(5x^2 - 3x - 2 = 0\) ist die Formel sicherer.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 13, [
    ('4a', 4, r'Wähle jeweils das schnellste Verfahren, begründe kurz und löse: (a) \(9x^2 - 4 = 0\) (b) \(x^2 - 13x = 0\) (c) \(x^2 + 2x - 24 = 0\) (d) \(2x^2 - 3x - 1 = 0\)',
     r'<p>(a) Wurzelziehen, kein lineares Glied: \(x^2 = \tfrac{4}{9}\), \(' + L + r' = \{-\tfrac{2}{3};\ \tfrac{2}{3}\}\) (oder Binom \((3x - 2)(3x + 2) = 0\)). (b) Ausklammern, keine Zahl ohne \(x\): \(x\,(x - 13) = 0\), \(' + L + r' = \{0;\ 13\}\). (c) Zweiklammersatz, Summe \(-2\), Produkt \(-24\): \((x + 6)(x - 4) = 0\), \(' + L + r' = \{-6;\ 4\}\). (d) Formel, Faktor \(2\) vor \(x^2\) und keine ganzzahlige Zerlegung: \(D = 9 + 8 = 17\), \(' + L + r' = \left\{\tfrac{3 - \sqrt{17}}{4};\ \tfrac{3 + \sqrt{17}}{4}\right\}\).</p>', ''),
    ('4b', 2, r'Bestimme den Typ und löse: \((3x - 1)^2 = 9x^2 + 7\).',
     r'<p>\(9x^2 - 6x + 1 = 9x^2 + 7\). Die \(9x^2\) heben sich weg: linear. \(-6x = 6\), \(x = -1\). \(' + L + r' = \{-1\}\).</p>', ''),
    ('4c', 3, r'Löse \((x - 2)(x + 3) = 2x\) und mach die Probe.',
     r'<p>\(x^2 + x - 6 = 2x\), also \(x^2 - x - 6 = 0\), \((x - 3)(x + 2) = 0\). \(' + L + r' = \{-2;\ 3\}\). Probe: \(1 \cdot 6 = 6 = 2 \cdot 3\) ✓; \((-4) \cdot 1 = -4 = 2 \cdot (-2)\) ✓.</p><p class="komm">Das Nullprodukt darf man erst anwenden, wenn rechts \(0\) steht.</p>', ''),
    ('4d', 2, r'Für \(x^2 + x - 20 = 0\) gibt jemand die Lösungen \(4\) und \(-5\) an, jemand anderes \(-4\) und \(5\). Wer hat recht? Begründe mit Vieta, ohne die Gleichung zu lösen.',
     r'<p>Nach Vieta muss die Summe \(-p = -1\) und das Produkt \(q = -20\) sein. \(4 + (-5) = -1\) und \(4 \cdot (-5) = -20\) ✓. Bei \(-4\) und \(5\) ist die Summe \(1\) — falsch. Die erste Person hat recht.</p>', ''),
    ('4e', 2, r'Abgebildet sind \(y = x^2 - 4x\) und \(y = 12\). Welche Gleichung lösen die Stellen der Schnittpunkte? Lies sie ab und bestätige rechnerisch.',
     r'<p>\(x^2 - 4x = 12\). Abgelesen: \(x = -2\) und \(x = 6\). Rechnung: \(x^2 - 4x - 12 = 0\), \((x - 6)(x + 2) = 0\), \(' + L + r' = \{-2;\ 6\}\).</p>',
     '\n            <div class="mini-reihe">' + mini('q,1,-4,0;g,0,12', '-4,8,-6,16', '-2,2,4,6', '-4,4,8,12', gross=True).replace('data-k=', 'data-sy="2" data-k=') + '</div>'),
])
k4 = kapitel(4, 'verfahren', 'Das passende Verfahren', 40,
             r'Du ordnest eine Gleichung, bestimmst ihren Typ, wählst das schnellste passende Verfahren, begründest die Wahl und kontrollierst die Lösungen mit der Probe oder dem Satz von Vieta.',
             ('g2-2b-lp-verfahren', 'Das passende Verfahren'),
             umformer(4, 'Umformer: Verfahren wählen und lösen'),
             ('g2-2b-lp-kontrolle-verfahren', 'Kontrollfragen zur Verfahrenswahl'),
             fest4, [uebung('verfahren', 'Verfahren wählen'), uebung('ordnen', 'Erst auf null bringen'), uebung('vieta', 'Kontrolle mit Vieta')],
             auf4, f'<a href="{TB}#verfahren">Themenseite 2.2b, Lösungsverfahren — wann welches?</a> und <a href="{TB}#aufgaben">Aufgabe A1</a>', komp='K4')

# ------------------------------------------------------------------ Kapitel 5
sim5 = '''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Familie <select class="sim-wahl" aria-label="Gleichungsfamilie">
          <option value="A" selected>A: x² − 2x + k = 0</option>
          <option value="B">B: x² + k · x − 3 = 0</option>
          <option value="C">C: k · x² + 2x + 1 = 0</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 280" role="img" aria-label="Parabel der gewählten Gleichungsfamilie mit den Lösungen auf der x-Achse"></svg>
        <div class="sl-row">
          <div class="sl-grp akz-orange"><label for="s5-k"><span class="var">Parameter k</span></label><input type="range" id="s5-k" data-p="k" min="-3" max="6" step="0.5" value="-2"><span class="sl-val"></span></div>
        </div>
      </figure>'''
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Parameterdiskussion</div>
          <p>Steht in der Gleichung ein zweiter Buchstabe, der <b>Parameter</b>, wird die Diskriminante eine Funktion von ihm. Man bestimmt die <b>kritischen Werte</b>, bei denen \(D = 0\) ist, und gibt für alle Bereiche die Anzahl der Lösungen an.</p>
          <ul>
            <li>\(x^2 - 6x + k = 0\): \(D(k) = 36 - 4k\) — zwei Lösungen für \(k \lt 9\), eine (\(x = 3\)) für \(k = 9\), keine für \(k \gt 9\).</li>
            <li>\(x^2 + kx + 4 = 0\): \(D(k) = k^2 - 16\) — null bei \(k = 4\) und \(k = -4\); keine Lösung für \(-4 \lt k \lt 4\), zwei für \(k \lt -4\) oder \(k \gt 4\).</li>
          </ul>
          <p><b>Parameter vor \(x^2\):</b> zuerst den Fall untersuchen, in dem der Faktor null wird — dann ist die Gleichung linear (genau eine Lösung, sofern der Faktor vor \(x\) nicht auch null ist), und \(D\) gilt nicht. \(m x^2 - 4x - 3 = 0\): \(m = 0\) gibt \(x = -\tfrac{3}{4}\); für \(m \neq 0\) ist \(D(m) = 16 + 12m\), eine Lösung bei \(m = -\tfrac{4}{3}\), zwei für \(m \gt -\tfrac{4}{3}\) (\(m \neq 0\)), keine für \(m \lt -\tfrac{4}{3}\).</p>
          <p><b>Nach \(x\) auflösen:</b> Der Parameter wird mitgeführt. \(x^2 - 2t\,x + t^2 - 9 = 0\): \(D = 4t^2 - 4(t^2 - 9) = 36\), \(x = \tfrac{2t \pm 6}{2} = t \pm 3\), also \(''' + L + r''' = \{t - 3;\ t + 3\}\) für jedes \(t\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bei \(m x^2 - 4x - 3 = 0\) nur \(D(m) = 16 + 12m\) untersuchen: Für \(m = 0\) gibt es genau eine Lösung \(x = -\tfrac{3}{4}\), obwohl \(D(0) = 16 \gt 0\) wäre.</p>
          <p>Aus \(k^2 = 16\) nur \(k = 4\) folgern: Auch \(k = -4\) ist ein kritischer Wert.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 16, [
    ('5a', 3, r'Für welche \(k\) hat \(x^2 + 10x + k = 0\) zwei, eine oder keine Lösung? Gib die Lösung an, wo es genau eine gibt.',
     r'<p>\(D = 100 - 4k\). Zwei für \(k \lt 25\), eine für \(k = 25\) (\(x = -5\)), keine für \(k \gt 25\).</p>', ''),
    ('5b', 3, r'Für welche \(k\) hat \(x^2 + kx + 9 = 0\) genau eine Lösung? Wie heisst sie jeweils? Für welche \(k\) gibt es keine?',
     r'<p>\(D = k^2 - 36 = 0\) bei \(k = 6\) (Lösung \(x = -3\)) und \(k = -6\) (Lösung \(x = 3\)). Keine Lösung für \(-6 \lt k \lt 6\).</p>', ''),
    ('5c', 2, r'Abgebildet ist \(y = x^2 - 4x + 1\). Für welches \(k\) hat \(x^2 - 4x + 1 = k\) genau eine Lösung? Lies es am Scheitel ab und bestätige mit \(D\).',
     r'<p>Die Waagrechte \(y = k\) berührt die Parabel nur im Scheitel \((2 \mid -3)\): \(k = -3\). Rechnung: \(x^2 - 4x + 1 - k = 0\), \(D = 16 - 4(1 - k) = 12 + 4k = 0\) bei \(k = -3\).</p>',
     '\n            <div class="mini-reihe">' + mini('q,1,-4,1', '-2,6,-4,6', '1,2,3,4', '-3,-2,2,4', punkte='2,-3') + '</div>'),
    ('5d', 4, r'Diskutiere \((m - 1)\,x^2 + 8x + 4 = 0\) vollständig — auch den Fall, in dem der Faktor vor \(x^2\) null wird.',
     r'<p>\(m = 1\): linear, \(8x + 4 = 0\), \(x = -0.5\). \(m \neq 1\): \(D = 64 - 4 \cdot (m - 1) \cdot 4 = 80 - 16m\). \(m = 5\): eine Lösung \(x = -\tfrac{8}{2 \cdot 4} = -1\). \(m \lt 5\), \(m \neq 1\): zwei. \(m \gt 5\): keine.</p><p class="komm">Der kritische Wert für den linearen Fall ist der, bei dem \(m - 1 = 0\) wird — nicht \(m = 0\).</p>', ''),
    ('5e', 2, r'Warum muss man bei \(k x^2 + 3x - 1 = 0\) den Fall \(k = 0\) getrennt untersuchen?',
     r'<p>Die Diskriminante und die Formel gehören zu quadratischen Gleichungen; in der Formel wird durch \(2a = 2k\) geteilt. Bei \(k = 0\) ist die Gleichung linear: \(3x - 1 = 0\), genau eine Lösung \(x = \tfrac{1}{3}\) — obwohl \(D(0) = 9 \gt 0\) zwei behaupten würde.</p>', ''),
    ('5f', 2, r'Löse \(x^2 - 4t\,x + 4t^2 - 1 = 0\) nach \(x\) auf (\(t\) ist ein Parameter).',
     r'<p>\(D = 16t^2 - 4(4t^2 - 1) = 4\), \(x = \dfrac{4t \pm 2}{2} = 2t \pm 1\). \(' + L + r' = \{2t - 1;\ 2t + 1\}\) für jedes \(t\). Probe mit \(t = 1\): \(x^2 - 4x + 3 = 0\) hat \(1\) und \(3\) ✓.</p>', ''),
])
k5 = kapitel(5, 'parameter', 'Parameterdiskussion', 45,
             r'Du untersuchst quadratische Gleichungen mit einem Parameter: \(D\) in Abhängigkeit des Parameters, die kritischen Werte, die Anzahl der Lösungen in allen Fällen — und zuerst den Fall, in dem der Faktor vor \(x^2\) null wird.',
             ('g2-2b-lp-parameter', 'Parameterdiskussion'),
             sim5, ('g2-2b-lp-kontrolle-parameter', 'Kontrollfragen zur Parameterdiskussion'),
             fest5, [uebung('param-quadr', 'Parameter im konstanten Glied'), uebung('param-lin', 'Parameter vor x'), uebung('param-vorne', 'Parameter vor x²')],
             auf5, f'<a href="{TB}#parameter">Themenseite 2.2b, Parameterdiskussion</a>', komp='K5')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 1.3 · 1.4 · 2.2a</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Ausmultiplizieren, ausklammern, die binomischen Formeln und den Zweiklammersatz, Quadratwurzeln und lineare Gleichungen mit Probe. Beim Zweiklammersatz suchst du in 1.3 die Zahlen in den Klammern; hier suchen wir meist die Lösungen — dieselben Zahlen mit umgekehrtem Vorzeichen (Kapitel 2). Wenn das wackelt: <a href="../grundlagen/g1-3-algebraische-terme.html">Teilgebiet 1.3, Algebraische Terme</a>, <a href="../grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html">1.4, Quadratwurzeln</a> und das <a href="lineare-gleichungen.html">Leitprogramm Lineare Gleichungen</a> (2.2a).</p>
      <div class="duo">
        ''' + clipkarte('g1-3-binome-erkennen', 'Binome: geschickt ausmultiplizieren — und zurück', '0:44') + '''
        ''' + clipkarte('g1-3-zweiklammersatz', 'Faktorisieren: der Zweiklammersatz', '0:46') + '''
      </div>
''' + test('t0', 'Vortest', 11, [
    ('0a', 2, r'Multipliziere aus: \((x - 4)^2\) und \((x + 3)(x - 4)\).',
     r'<p>\(x^2 - 8x + 16\); \(x^2 - x - 12\).</p><p class="komm">Das mittlere Glied des Binoms brauchen Kapitel 2 und 3.</p>', ''),
    ('0b', 2, r'Klammere so viel wie möglich aus: \(6x^2 - 9x\) und \(x^2 + 7x\).',
     r'<p>\(3x\,(2x - 3)\); \(x\,(x + 7)\).</p><p class="komm">Falsch? Genau das braucht Kapitel 2.</p>', ''),
    ('0c', 3, r'Schreib als Produkt: \(x^2 + 12x + 36\), \(x^2 - 100\) und \(x^2 + x - 6\).',
     r'<p>\((x + 6)^2\); \((x - 10)(x + 10)\); \((x + 3)(x - 2)\).</p><p class="komm">Binomische Formeln und Zweiklammersatz rückwärts: Kapitel 2.</p>', ''),
    ('0d', 2, r'Berechne \(\sqrt{81}\) und \(\sqrt{0.36}\), vereinfache \(\sqrt{12}\). Welche Zahlen haben das Quadrat \(49\)?',
     r'<p>\(9\); \(0.6\); \(\sqrt{12} = \sqrt{4 \cdot 3} = 2\sqrt{3}\); \(7\) und \(-7\).</p><p class="komm">Teilweise Wurzel ziehen braucht Kapitel 3 (exakte Lösungen).</p>', ''),
    ('0e', 2, r'Löse \(5x - 3 = 2x + 9\) und mach die Probe.',
     r'<p>\(3x = 12\), \(x = 4\). Probe: \(20 - 3 = 17\) und \(8 + 9 = 17\) ✓.</p><p class="komm">Die Probe gehört zu jeder Gleichung, die du löst.</p>', ''),
], zwei=True) + '''
      <p class="komm">Weniger als 8 von 11 Punkten: zuerst die verlinkten Teilgebiete, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/quadratische-gleichungen/'
GT_MIN, GT_P = 30, 25
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 2.2 · Kapitel 1–5</span><span class="zeit">≈ {GT_MIN} min · {GT_P} Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg, ohne Taschenrechner.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben oder selbst bewerten. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Das Kapitel, in dem du die meisten Punkte verloren hast, nochmals: Tüfteln und Übungen.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1 und 2; G2 → 2 und 4; G3 → 3 und 4; G4 → 3 und 4; G5 → 4, 1 und 3; G6, G7 → 5</p>
        </div>
        <p class="ausf">Weiter: <a href="gleichungssysteme.html">Leitprogramm Gleichungssysteme</a> (GF 2.3). Nicht in diesem Leitprogramm: Bruchgleichungen, Gleichungen wie \\(x^4 - 10x^2 + 9 = 0\\) (Substitution) und quadratische Ungleichungen — auf der <a href="{TB}#bruchgleichungen">Themenseite 2.2b</a>.</p>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Quadratische Gleichungen, Version 2.0 (11.10.2026). Gebaut aus
     scripts/lp/quadratische-gleichungen/seite.py — Änderungen dort, nicht in dieser Datei.
     Ersetzt unter derselben Adresse das ältere Leitprogramm «Quadratische Gleichungen» (07.09.2026, Git-Geschichte)
     und löst mit «Lineare Gleichungen» (2.2a) das gemeinsame Leitprogramm «Lineare und quadratische Gleichungen» ab.
     Grundlage: HOWTO-leitprogramme.md (Kapitelmuster, §8d Umformer).

     RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2 «Lineare und quadratische Gleichungen», eine Kompetenz:
       «lineare und quadratische Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden,
        inkl. Parameterdiskussion (auch ohne Hilfsmittel)»
     Kompetenzbox der Themenseite 2.2b (wörtlich):
       «quadratische Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden, inkl.
        Parameterdiskussion (auch ohne Hilfsmittel)»
     Für die Kompetenzmatrix in fünf Teile gegliedert:
       K1  quadratische Gleichungen erkennen, auf die Normalform bringen, mit Wurzelziehen lösen
       K2  mit Ausklammern und Faktorisieren lösen (Nullprodukt, Binom, Zweiklammersatz/Vieta), das Verfahren erklären
       K3  mit quadratischer Ergänzung und Mitternachtsformel lösen, die Formel herleiten, die Diskriminante deuten
       K4  Lösungsmethoden vergleichen und begründet wählen, den Typ bestimmen, Lösungen prüfen (Probe, Vieta)
       K5  Parameterdiskussion, inkl. verschwindendem Leitkoeffizienten
     Unterstützend aus 2.1: «den Typ einer Gleichung bestimmen … sowie Lösungen überprüfen» (K1, K4).

     Kompetenzmatrix (Kompetenz | ohne HM | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 | ja | 1 | 1a–1f | G1, G5(a)(ii) (Typ)
       K2 | ja | 2 | 2a–2f | G1, G2
       K3 | ja | 3 | 3a–3f (3e: Formel herleiten) | G3, G4, G5(b)
       K4 | ja | 4 | 4a–4e | G2(b), G3, G4, G5(a)
       K5 | ja | 5 | 5a–5f | G6, G7
     Funktionssicht (Parabel als Bild der Lösungen) nur unterstützend aus GF 3.1 «Gleichungen mithilfe von Funktionen
     visualisieren»: 1f, 2e, 3f, 4e, 5c, Sim 5; kein eigenes Kapitelziel, nicht im Gesamttest.
     Alles ohne Taschenrechner (RLP-Vermerk «auch ohne Hilfsmittel»).

     Planung (Kapitel | Lernziel | Kompetenz | Clips | Tüfteln | Beispiel (Quelle) | häufiger Fehler | min):
       0 | Vorwissen | — | g1-3-binome-erkennen, g1-3-zweiklammersatz | Vortest | — | — | 10
       1 | erkennen, Normalform, Wurzelziehen | K1 | wurzel, kontrolle-wurzel | Umformer 1 | 2x² + 8x − 10, x² = 9, (x − 2)² = 9 (Themenseite: x² = 9) | nur +√ | 40
       2 | Nullprodukt, ausklammern, Binom, Zweiklammersatz, Vieta | K2 | faktorisieren, kontrolle-faktorisieren | Umformer 2 | x² = 5x, x² − 6x + 9, x² − 7x + 12 (Themenseite) | durch x teilen | 45
       3 | Ergänzung, Herleitung, Formel, D | K3 | formel, kontrolle-formel | Umformer 3 | Flächenmodell p = 6, x² − 6x + c mit c = 5, 9, 10 (Themenseite), 2x² − 5x − 3 | −4ac, −b, 2a | 45
       4 | ordnen, Typ, Verfahren, Kontrolle | K4 | verfahren, kontrolle-verfahren | Umformer 4 | (x − 1)² = x² + 7, x(x + 4) = 12 | Verfahren vor «= 0» | 40
       5 | Parameter | K5 | parameter, kontrolle-parameter | Simulation mit drei Familien | x² − 6x + k, x² + kx + 4, m x² − 4x − 3 (Themenseite) | Fall a = 0 | 45
       Gesamttest 30 min · Summe 255 min ≈ 5.7 Lektionen (fünf Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest).

     Bewusst weggelassen (→ Themenseite 2.2b, nicht RLP 2.2): Bruchgleichungen mit Definitionsmenge und
     Scheinlösung, Substitution (biquadratisch), quadratische Ungleichungen; die pq-Formel nur erwähnt (die
     Mitternachtsformel deckt die Normalform mit ab, die Themenseite zeigt beide); TI-30X (RLP: ohne Hilfsmittel).

     Konventionen wie auf der Themenseite: 𝕃 mit Strichpunkt, leere Menge {}, Normalform x² + px + q = 0,
     Mitternachtsformel mit D = b² − 4ac, «Satz vom Nullprodukt», «Zweiklammersatz», «Satz von Vieta»
     (x₁ + x₂ = −p, x₁ · x₂ = q), quadratische Ergänzung mit (p/2)², Parameter k (m vor x²).
     Widersprüche in der Themenseite: keine, die ein Kapitel betreffen. Zweiklammersatz: Die Themenseite 2.2b sucht die Lösungen
     (Summe −p), Teilgebiet 1.3 die Klammerzahlen (r + s = p) — im Vorwissen und im Festhalten 2 ausdrücklich überbrückt.
     Farben: Gleichung und Parabel blau, Umformung und Parameter orange, Lösungen grün, Fehler rot.

     Muster je Kapitel: ① Einführungsclip → ② Umformer (Kapitel 1–4) bzw. Simulation (Kapitel 5) mit
     Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben
     mit Lösungen. Gesamttest und Bewertungspaket nur als PDF aus LaTeX
     (downloads/leitprogramme/quadratische-gleichungen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Quadratische Gleichungen</h1>
      <p class="unter">Zuschauen, umformen, kontrollieren, üben. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 2.2b</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Wurzel ziehen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Faktorisieren</span></a></li>
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
          <li><b>② Tüfteln:</b> In Kapitel 1–4 wählst du im Umformer jeden Schritt selbst und gibst am Schluss die Lösungsmenge ein — er zeigt ✓, wenn sie stimmt. In Kapitel 5 ziehst du am Regler für den Parameter und löst die Aufgaben der Leiste.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiet 2.2 — hier der quadratische Teil (Themenseite 2.2b):</p>
        <p>quadratische Gleichungen lösen, verschiedene Lösungsmethoden erklären und anwenden, inkl. Parameterdiskussion <span class="ohm">auch ohne Hilfsmittel</span></p>
        <p class="rlp-quelle">Hier in fünf Teile gegliedert:</p>
        <ul>
          <li><b>K1</b> quadratische Gleichungen erkennen, auf die Normalform bringen und mit Wurzelziehen lösen — Kapitel 1</li>
          <li><b>K2</b> mit Ausklammern und Faktorisieren lösen (Nullprodukt, Binom, Zweiklammersatz, Vieta) und das Verfahren erklären — Kapitel 2</li>
          <li><b>K3</b> mit quadratischer Ergänzung und Mitternachtsformel lösen, die Formel erklären, die Diskriminante deuten — Kapitel 3</li>
          <li><b>K4</b> Lösungsmethoden vergleichen und begründet wählen, den Typ bestimmen, Lösungen prüfen — Kapitel 4</li>
          <li><b>K5</b> Parameterdiskussion — Kapitel 5</li>
        </ul>
        <p class="rlp-quelle">Parabeln dienen als Bild der Lösungen (Nullstellen) — die Funktionssicht «Gleichungen mithilfe von Funktionen visualisieren» gehört zu GF 3.1.</p>
        <p class="rlp-quelle">Nicht hier, sondern auf der <a href="''' + TB + '''">Themenseite 2.2b</a>: Bruchgleichungen, Substitution, quadratische Ungleichungen. Lineare Gleichungen: Leitprogramm 2.2a. Gleichungssysteme: Teilgebiet 2.3.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Quadratische Gleichungen · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (11.10.2026): Vorwissen 10 · K1 40 · K2 45 · K3 45 · K4 40 · K5 45 · Gesamttest 30 = 255 min
summe = 10 + sum(MINUTEN.values()) + GT_MIN
assert summe == 255, summe
assert sum(PUNKTE[t] for t in ('t1', 't2', 't3', 't4', 't5')) == 71 and PUNKTE['t0'] == 11
body = oben + k0 + k1 + k2 + k3 + k4 + k5 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read() + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen;', summe, 'min')
