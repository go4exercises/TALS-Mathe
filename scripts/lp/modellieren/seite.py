"""Baut leitprogramme/modellieren.html aus einer Kapitelbeschreibung (08.10.2026).

  python3 scripts/lp/modellieren/seite.py

Leitprogramm zur Themenseite 2.M Textaufgaben modellieren (grundlagen/g2-modellieren.html, RLP GF 2.1 und 2.3).
Liest Kopf (inkl. <style>) und Grundskript aus der bestehenden Seite, ersetzt Inhalt und Seitenskript (seite.js)
und schreibt die Seite neu. Beim ersten Lauf kommt das Gerüst aus leitprogramme/trigonometrische-gleichungen.html
(Grundlagenfach, Kapitelmuster), mit eigenem Titel und eigenen localStorage-Schlüsseln. Wiederholbar: zweimal
laufen lassen ergibt dieselbe Datei. Clipzeiten aus den Drehbüchern. Siehe README.md.
"""
import html
import json
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'          # hier liegt seite.js
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
NAME = 'Textaufgaben modellieren'
DATEI = 'modellieren'
ZIEL = R + 'leitprogramme/' + DATEI + '.html'
BESCHREIBUNG = ('Leitprogramm zum Modellieren von Textaufgaben nach RLP GF 2.1 und 2.3: Zahlenrätsel, Mischen, '
                'Verteilen und Zins Schritt für Schritt vom Text über die Deklaration zum Ansatz, in die Grundform und '
                'mit dem TI-30X Pro gelöst — mit Clips, Simulationen, Übungen mit Rückmeldung und Gesamttest.')

if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
else:                                                          # erster Lauf: Gerüst vom Vorbild
    alt = open(R + 'leitprogramme/trigonometrische-gleichungen.html').read()
    alt = alt.replace('<title>Leitprogramm Trigonometrische Gleichungen</title>', '<title>Leitprogramm ' + NAME + '</title>')
    alt = alt.replace('lp-trigonometrische-gleichungen-', 'lp-' + DATEI + '-')

# Kopfblock für Suchmaschinen: noch unverlinkt (HOWTO-leitprogramme §13, §15). build-seo.py ersetzt ihn,
# sobald die Seite in SEITEN steht — mit noindex=True, bis sie freigeschaltet ist. Ein vorhandener Block,
# den build-seo.py schon geschrieben hat (mit JSON-LD), bleibt unangetastet.
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
for marke in ('\n/* ════════ Trigonometrische Gleichungen', '\n/* ════════ Modellieren'):
    if marke in kopf:
        kopf = kopf[:kopf.index(marke)]
i = alt.index('<script>\n  window.MathJax')
j = min(k for k in (alt.find('<script>\n/* Leitprogramm Trigonometrische Gleichungen —'),
                    alt.find('<script>\n/* Leitprogramm Modellieren —')) if k > 0)
basis = alt[i:j]
fuss = alt[alt.index('<footer class="site-footer">'):]
fuss = re.sub(r'Version [0-9.]+( \(Probe\))?', 'Version 1.0 (Probe)', fuss)
fuss = re.sub(r'Leitprogramm · [^<]+</p>', 'Leitprogramm · ' + NAME + '</p>', fuss, count=1)
fuss = re.sub(r'Stand [0-9]+\. [A-Za-zäöü]+ 2026', 'Stand 8. Oktober 2026', fuss)

CSS = '''
/* ════════ Modellieren (08.10.2026) — Kapitelmuster wie die anderen Leitprogramme ════════
   Grundgerüst (Leiste, Übungen, Festhalten, PDF-Weg) wie dort. Eigen: die vier Bilder der Grundgleichungen
   (Zehnerstangen, Gefässe, Rechteckmodell, Kapital- und Zinssäulen) und Übungen mit sechs Koeffizienten.
   Farben: erste Unbekannte blau, zweite orange, Ergebnis und Mischung grün, Fehler rot. */
.sim-gross{max-width:640px;margin:10px auto 6px}
.sim-gross > svg{max-width:560px}
.sl-grp[hidden]{display:none}
/* Regler mit vielen Stufen über die ganze Breite, auf dem Handy Beschriftung darüber (wie LP Trigonometrische Gleichungen):
   30 Stufen für x (Schritt 1000 CHF) brauchen genug Pixel, auch mit dem Finger */
.sl-row:has(.sl-weit){flex-wrap:wrap}
.sl-grp.sl-weit{flex:1 1 100%;display:flex;align-items:center;gap:10px}
.sl-grp.sl-weit input[type=range]{flex:1;min-width:0;width:auto}
.sl-grp.sl-weit[hidden]{display:none}
@media(max-width:620px){.sl-grp.sl-weit{flex-wrap:wrap;gap:2px 10px}.sl-grp.sl-weit label{flex:1 1 100%}}
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
.clip-paar{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;max-width:640px}
.kompetenzen ul{margin:10px 0 0;padding-left:1.25em;font-family:var(--sans);font-size:.92rem}
.kompetenzen li{margin:5px 0}
.kompetenzen .rlp-quelle{font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);margin:8px 0 0}
.kompetenzen .ohm{font-size:.72rem;padding:1px 7px;border-radius:999px;background:var(--orange-hell);border:1px solid var(--orange-rand);white-space:nowrap}
.sim .pfeil,svg.mo-bild .pfeil{fill:var(--tinte-2)}
.sim .achse,svg.mo-bild .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .gitter{stroke:var(--linie);stroke-width:.8;stroke-dasharray:3 3}
.sim .skala,svg.mo-bild .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:13px}
.achsname{fill:var(--tinte);font-family:var(--serif);font-style:italic;font-size:12px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.sim-wahl{display:flex;flex-wrap:wrap;gap:6px 14px;justify-content:center;font-family:var(--sans);font-size:.86rem;margin:4px 0 10px}
.sim-wahl label{display:inline-flex;gap:5px;align-items:center;cursor:pointer;white-space:nowrap}
.sim-formel{line-height:1.6;font-family:var(--sans);font-size:.9rem;text-align:center}
/* Bilder der Grundgleichungen: Rahmen und Flächen in der Farbe ihrer Unbekannten */
.st{stroke-width:1.4} .st.blau{fill:var(--blau-hell);stroke:var(--blau)} .st.orange{fill:var(--orange-hell);stroke:var(--orange)}
.st-teil{stroke-width:.8} .st-teil.blau{stroke:var(--blau)} .st-teil.orange{stroke:var(--orange)}
.becher{fill:none;stroke:var(--tinte-2);stroke-width:1.6}
.fuell{stroke-width:1.2;opacity:.9} .fuell.blau{fill:var(--blau-hell);stroke:var(--blau)} .fuell.orange{fill:var(--orange-hell);stroke:var(--orange)} .fuell.gruen{fill:var(--gruen-hell);stroke:var(--gruen)}
.stoff{stroke:none} .stoff.blau{fill:var(--blau)} .stoff.orange{fill:var(--orange)} .stoff.gruen{fill:var(--gruen)}
.fl{stroke-width:1.4} .fl.blau{fill:var(--blau-hell);stroke:var(--blau)} .fl.orange{fill:var(--orange-hell);stroke:var(--orange)} .fl.gruen{fill:var(--gruen-hell);stroke:var(--gruen)}
.fl.dunkel.blau{fill:var(--blau)} .fl.dunkel.orange{fill:var(--orange)} .fl.dunkel.gruen{fill:var(--gruen)}
.klammer{stroke:var(--gruen);stroke-width:2.4} .trenn{stroke:var(--linie);stroke-width:1.2;stroke-dasharray:4 4}
.bt{fill:var(--tinte);font-family:var(--sans);font-size:15px}
.bt-kopf{fill:var(--tinte-2);font-family:var(--sans);font-size:14px;font-weight:700;letter-spacing:.06em}
.bt-zahl{fill:var(--tinte);font-family:var(--serif);font-size:22px}
.bt-klein{fill:var(--tinte);font-family:var(--sans);font-size:13.5px;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.bt-klein.hell{fill:#fff;stroke:none} .gruen.bt,.bt-klein.gruen{fill:var(--gruen);font-weight:700}
svg.mo-bild{display:block;width:100%;max-width:300px;margin:6px 0;background:var(--karte);border:1px solid var(--linie);border-radius:8px}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.festhalten .merk ul{padding-left:1.3em;margin:6px 0 10px}
.festhalten .merk li{margin:3px 0}
.festhalten table.arten{border-collapse:collapse;font-family:var(--sans);font-size:.86rem;margin:6px 0 10px;width:100%}
.festhalten table.arten td,.festhalten table.arten th{border:1px solid var(--blau-rand);padding:4px 8px;text-align:left;vertical-align:top}
.tab-rahmen{overflow-x:auto}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--blau-hell);border:1px solid var(--blau-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte);max-width:100%}
.ue-eingabe select:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe{line-height:2.4}
.ue-eingabe input{width:4.6em}
.sl-grp.akz-grau{--akz:var(--tinte-2)}
/* Simulation Zins: viel Text im Bild — grösser, damit es bei 360 px noch lesbar ist (Prüfung 08.10.2026) */
#sim4 > svg{max-width:440px} #sim4 .bt-klein{font-size:19px} #sim4 .bt-kopf{font-size:17px} #sim4 .bt{font-size:21px}
.nb{white-space:nowrap}
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


def regler(sim, p, label, mn, mx, st, val, akz='grau', einheit='', weit=False):
    return (f'<div class="sl-grp akz-{akz}{" sl-weit" if weit else ""}"><label for="{sim}-{p}"><span class="var">{label}</span></label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="sl-val"></span></div>')


def wahl(name, label, optionen):
    """Auswahlknöpfe in der Simulation; der erste ist der Startzustand (die Leiste setzt zurück)."""
    knoepfe = ''.join(f'<label><input type="radio" name="{name}" value="{w}"{" checked" if k == 0 else ""}> {t}</label>'
                      for k, (w, t) in enumerate(optionen))
    return f'<div class="sim-wahl" role="radiogroup" aria-label="{label}">{knoepfe}</div>'


def sim(nr, label, unten):
    return f'''      <figure class="sim sim-gross" id="sim{nr}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="{label}"></svg>
        {unten}
      </figure>'''


def bild(d, label):
    return (f'\n            <svg class="mo-bild" aria-label="{label}" '
            f'data-bild="{html.escape(json.dumps(d, ensure_ascii=False), quote=True)}"></svg>')


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


def kapitel(n, kid, titel, zeit, ziel, clip1, sim_, clips2, festhalten, uebungen, aufgaben, mehr, hm):
    ue = '\n        '.join(uebungen)
    paar = '\n        '.join(clipkarte(*c) for c in clips2)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-gf">GF 2.1 · 2.3 · K1 · K2 · K3 · {hm}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim_}

      <p class="phase"><span>③</span> Kontrollfragen</p>
      <div class="clip-paar">
        {paar}
      </div>

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


TS = '../grundlagen/g2-modellieren.html'
OHNE = '<span class="nb">(ohne Taschenrechner)</span>'

# ------------------------------------------------------------------ Kapitel 1 · Zahlen- und Ziffernrätsel
sim1 = sim(1, 'Zweistellige Zahl als Zehnerstangen und Einerwürfel neben der Zahl mit vertauschten Ziffern',
           '<div class="sl-row">\n          ' + regler('s1', 'z', 'z (Zehnerziffer)', 1, 9, 1, 4, 'blau')
           + '\n          ' + regler('s1', 'e', 'e (Einerziffer)', 0, 9, 1, 7, 'orange') + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zahlen- und Ziffernrätsel</div>
          <p>Bei Zahlen- und Ziffernrätseln gilt: <b>je eine Gleichung pro Aussage</b> des Textes.</p>
          <ul>
            <li><b>Zweistellige Zahl:</b> \(z\): Zehnerziffer, \(e\): Einerziffer, mit \(z \in \{1;\ 2;\ \ldots;\ 9\}\) und \(e \in \{0;\ 1;\ \ldots;\ 9\}\). Die Zahl ist \(10 \cdot z + e\), vertauscht \(10 \cdot e + z\), die Quersumme \(z + e\).</li>
            <li><b>Aufeinanderfolgende natürliche Zahlen:</b> \(n\), \(n + 1\), \(n + 2\) — eine Unbekannte genügt.</li>
            <li><b>Übersetzen:</b> «um 3 grösser als \(a\)» ist \(a + 3\), «3-mal so gross wie \(a\)» ist \(3 \cdot a\).</li>
          </ul>
          <p><b>Gleichungsart erkennen:</b> Stehen die Unbekannten nur in Summen und Vielfachen, ist es linear — eine Gleichung löst du von Hand (oder mit num-solv), ein System mit sys-solv oder von Hand. Bleibt nach dem Ausmultiplizieren ein Quadrat oder ein <b>Produkt der Unbekannten</b> (\(z \cdot e\)) stehen, ist es quadratisch: einsetzen, in die Grundform \(a \cdot x^2 + b \cdot x + c = 0\) bringen, poly-solv. (In \((n + 1)^2 - n^2 = 15\) fällt das Quadrat weg: linear.)</p>
          <p><b>Probe am Text</b>, und Lösungen verwerfen, die keine Ziffer oder keine natürliche Zahl sind. Beispiel aus dem Clip: Quersumme 9, Produkt der Ziffern 14 gibt \(z^2 - 9 \cdot z + 14 = 0\) — zwei Zahlen, 72 und 27.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«um 3 grösser» und «3-mal so gross» verwechseln — und die Richtung: Die 3 kommt zur <em>kleineren</em> Grösse. Kontrolle mit einer Zahl.</p>
          <p>Die Zahl als \(z \cdot e\) schreiben: Das ist das Produkt der Ziffern. Die Zahl ist \(10 \cdot z + e\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 10, [
    ('1a', 3, r'Die Einerziffer einer zweistelligen Zahl ist um 1 grösser als das Doppelte der Zehnerziffer. Vertauscht man die Ziffern, wird die Zahl um 45 grösser. Deklariere, stelle das System auf und löse es von Hand ' + OHNE + '.',
     r'<p>\(z\): Zehnerziffer, \(e\): Einerziffer. \(e = 2 \cdot z + 1\) und \(10 \cdot e + z = 10 \cdot z + e + 45\), also \(9 \cdot e - 9 \cdot z = 45\) und \(e - z = 5\). Einsetzen: \(2 \cdot z + 1 - z = 5\), \(z = 4\), \(e = 9\). Die Zahl heisst <b>49</b>. Probe am Text: \(9 = 2 \cdot 4 + 1\) ✓; \(94 - 49 = 45\) ✓.</p>', ''),
    ('1b', 2, r'Schreib mit \(z\) (Zehnerziffer) und \(e\) (Einerziffer) als Gleichung: (a) Die Zahl ist um 18 grösser als die Zahl mit vertauschten Ziffern. (b) Das Produkt der Ziffern ist um 2 kleiner als die Zahl selbst. (c) Die Einerziffer ist halb so gross wie die Zehnerziffer. Welche der drei Gleichungen macht ein System quadratisch?',
     r'<p>(a) \(10 \cdot z + e = 10 \cdot e + z + 18\). (b) \(z \cdot e = 10 \cdot z + e - 2\). (c) \(e = \tfrac{z}{2}\), gleichwertig \(z = 2 \cdot e\). Quadratisch macht (b): Dort werden die Unbekannten multipliziert.</p><p class="komm">Kontrolle mit einer Zahl: Bei 31 ist (a) erfüllt, \(31 - 13 = 18\).</p>', ''),
    ('1c', 3, r'Das Produkt zweier aufeinanderfolgender gerader Zahlen ist 168. Welche Zahlen können es sein? Bring die Gleichung in die Grundform und löse sie mit dem Taschenrechner.',
     r'<p>\(n\): kleinere der beiden Zahlen, die grössere ist \(n + 2\). \(n \cdot (n + 2) = 168\), Grundform \(n^2 + 2 \cdot n - 168 = 0\); poly-solv: \(x_1 = 12\), \(x_2 = -14\). Beide sind gerade Zahlen: <b>12 und 14</b> oder <b>−14 und −12</b>. Probe: \(12 \cdot 14 = 168\) ✓, \((-14) \cdot (-12) = 168\) ✓.</p><p class="komm">Hiesse es «natürliche Zahlen», fiele \(-14\) weg. Was verworfen wird, entscheidet der Text.</p>', ''),
    ('1d', 2, r'(a) Welche Zahl zeigt das Bild? Gib die Zahl mit vertauschten Ziffern und die Differenz der beiden an. (b) Warum ist diese Differenz bei jeder zweistelligen Zahl ein Vielfaches von 9?',
     r'<p>(a) 3 Zehnerstangen und 6 Einer: 36. Vertauscht 63, Differenz \(63 - 36 = 27\). (b) \((10 \cdot e + z) - (10 \cdot z + e) = 9 \cdot e - 9 \cdot z = 9 \cdot (e - z)\) — immer 9 mal eine ganze Zahl.</p>',
     bild({'art': 'zahl', 'z': 3, 'e': 6}, 'Drei Zehnerstangen und sechs Einerwürfel')),
])
k1 = kapitel(1, 'zahlenraetsel', 'Zahlen- und Ziffernrätsel', 60,
             r'Du übersetzt die Aussagen eines Zahlenrätsels in Gleichungen — mit dem Stellenwert \(10 \cdot z + e\) —, erkennst, ob eine lineare oder quadratische Gleichung oder ein System entsteht, bringst sie in die Grundform für den Rechner und prüfst jede Lösung am Text.',
             ('g2-M-lp-zahlenraetsel', 'Zahlen- und Ziffernrätsel'),
             sim1, [('g2-M-lp-kontrolle-zahlen-1', 'Kontrollfragen: eine Unbekannte'), ('g2-M-lp-kontrolle-zahlen-2', 'Kontrollfragen: zwei Unbekannte')],
             fest1, [uebung('ziffern', 'Ziffernrätsel für sys-solv'), uebung('folge', 'Mit Quadrat: Grundform und Lösung'), uebung('art', 'Gleichungsart und Löser')],
             auf1, f'<a href="{TS}#zahlen">Themenseite 2.M, Typ 1 — Zahlen- und Ziffernrätsel</a> (dort auch Bruchrätsel)',
             'Taschenrechner erlaubt, 1a ohne')

# ------------------------------------------------------------------ Kapitel 2 · Mischen
sim2 = sim(2, 'Drei Gefässe: Sorte 1 und Sorte 2 mit ihrer Menge und dem Stoff darin, und die Mischung',
           '<div class="sl-row">\n          ' + regler('s2', 'x', 'x (Sorte 1)', 0, 30, 1, 20, 'blau', ' kg')
           + '\n          ' + regler('s2', 'y', 'y (Sorte 2)', 0, 30, 1, 10, 'orange', ' kg') + '\n        </div>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Mischen: Mengenbilanz und Stoffbilanz</div>
          <p>\(x\): Menge der Sorte 1, \(y\): Menge der Sorte 2 — in kg oder l, je nach Text.</p>
          <p>\[ \begin{cases} x + y = M & \text{(Mengenbilanz)} \\ p_1 \cdot x + p_2 \cdot y = p \cdot M & \text{(Stoffbilanz)} \end{cases} \]</p>
          <ul>
            <li>\(p_1\), \(p_2\) sind die Anteile der Sorten, \(p\) der Anteil der Mischung, \(M\) die Gesamtmenge. Anteile als <b>Dezimalzahl</b>: 3.8 % wird zu \(0.038\). Stoff = Anteil mal Menge.</li>
            <li>Beim Mischen von Preisen ist \(p\) der Preis pro kg, die zweite Gleichung eine Wertbilanz in CHF.</li>
            <li><b>Verdünnen:</b> Wasser ist eine Sorte mit dem Anteil \(0\). Mit einer Unbekannten entsteht eine lineare Gleichung. <b>Eindampfen:</b> Verdunstet Wasser, bleibt der Stoff, die Masse wird kleiner: \(p_1 \cdot V = p_2 \cdot (V - w)\).</li>
            <li><b>Prozentpunkte:</b> Sinkt ein Anteil von 30 % um 10 Prozentpunkte, sind es 20 % — als Dezimalzahl \(p - 0.1\). (Um 10 Prozent gesunken wären es 27 %.)</li>
            <li>Für sys-solv darf die Stoffbilanz mit 100 multipliziert werden: ganze Zahlen tippen sich sicherer.</li>
            <li><b>Quadratisch</b> wird es, wenn Menge und Anteil beide unbekannt sind (\(m \cdot p\)) oder wenn zweimal Gemisch entnommen und ersetzt wird.</li>
          </ul>
          <p>Beispiel aus dem Clip: 20 % und 50 % Zucker zu 30 kg mit 30 %: \(x + y = 30\), \(0.2 \cdot x + 0.5 \cdot y = 9\); \(x = 20\), \(y = 10\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Prozent und Menge in derselben Gleichung: In \(0.2 \cdot x + 0.5 \cdot y = 0.3\) steht links eine Masse, rechts ein Anteil. Die Anteile der Sorten addieren sich nicht zum Anteil der Mischung — addiert werden die Stoffmengen.</p>
          <p>Kontrollfrage für jede Gleichung: Welche Einheit steht links, welche rechts? Es muss dieselbe sein.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 10, [
    ('2a', 3, r'Ein Teeladen mischt Tee zu 40 CHF pro kg mit Tee zu 64 CHF pro kg zu 6 kg einer Mischung zu 48 CHF pro kg. Deklariere, stelle das System auf und löse es von Hand ' + OHNE + '.',
     r'<p>\(x\): Masse Tee zu 40 CHF in kg, \(y\): Masse Tee zu 64 CHF in kg. \(x + y = 6\) und \(40 \cdot x + 64 \cdot y = 48 \cdot 6 = 288\). Mit \(x = 6 - y\): \(240 + 24 \cdot y = 288\), \(y = 2\), \(x = 4\). <b>4 kg zu 40 CHF und 2 kg zu 64 CHF.</b> Probe am Text: \(160 + 128 = 288\) CHF, und \(288 : 6 = 48\) CHF pro kg ✓.</p>', ''),
    ('2b', 2, r'Für «Milch mit 3.5 % Fett und Rahm mit 35 % Fett ergeben 70 kg mit 8 % Fett» schreibt jemand \(x + y = 70\) und \(0.035 \cdot x + 0.35 \cdot y = 8\). Was ist falsch? Korrigiere und löse mit dem Taschenrechner.',
     r'<p>Rechts steht ein Prozentwert, links eine Fettmasse in kg. Richtig ist die Fettmasse der Mischung: \(0.08 \cdot 70 = 5.6\). sys-solv mit \(x + y = 70\) und \(0.035 \cdot x + 0.35 \cdot y = 5.6\): <b>\(x = 60\) kg Milch, \(y = 10\) kg Rahm.</b> Probe: \(2.1 + 3.5 = 5.6\) kg Fett ✓.</p>', ''),
    ('2c', 3, r'Ein Behälter enthält 50 l reines Frostschutzmittel. Man lässt eine Menge ab, füllt mit Wasser auf und mischt gut. Dann lässt man <em>doppelt so viel</em> ab wie beim ersten Mal und füllt wieder mit Wasser auf. Jetzt enthält er noch 24 l Frostschutzmittel. Wie viel wurde beim ersten Mal abgelassen? (Taschenrechner)',
     r'<p>\(x\): beim ersten Mal abgelassene Menge in l, beim zweiten Mal \(2 \cdot x\); \(0 \lt 2 \cdot x \lt 50\). Nach dem ersten Mal \(50 - x\) l Mittel, Anteil \(\tfrac{50 - x}{50}\). Beim zweiten Mal gehen \(2 \cdot x \cdot \tfrac{50 - x}{50}\) l Mittel weg; übrig bleibt \((50 - x) \cdot \tfrac{50 - 2 \cdot x}{50} = 24\). Mal 50: \((50 - x) \cdot (50 - 2 \cdot x) = 1200\), Grundform \(2 \cdot x^2 - 150 \cdot x + 1300 = 0\) (oder durch 2: \(x^2 - 75 \cdot x + 650 = 0\)); poly-solv: \(x_1 = 65\), \(x_2 = 10\). 65 l sind mehr, als im Behälter ist: <b>beim ersten Mal 10 l, beim zweiten Mal 20 l</b>. Probe am Text: 40 l Mittel in 50 l, also 80 %; mit 20 l Gemisch gehen 16 l Mittel weg, es bleiben 24 l ✓.</p>', ''),
    ('2d', 2, r'(a) Lies im Bild die Stoffmengen ab und berechne den Anteil der Mischung. (b) Warum ist der Anteil nicht der Mittelwert \((20\,\% + 60\,\%) : 2 = 40\,\%\)?',
     r'<p>(a) \(0.2 \cdot 30 = 6\) kg und \(0.6 \cdot 10 = 6\) kg, zusammen 12 kg Stoff in 40 kg: \(12 : 40 = 0.3\), also 30 %. (b) Es ist dreimal so viel von der 20-%-Sorte dabei. Der Anteil der Mischung liegt darum näher bei 20 %: Gemittelt wird mit den Mengen, nicht mit den Prozenten allein.</p>',
     bild({'art': 'misch', 'x': 30, 'p1': 0.2, 'y': 10, 'p2': 0.6}, 'Gefäss mit 30 kg zu 20 Prozent, Gefäss mit 10 kg zu 60 Prozent und die Mischung')),
])
k2 = kapitel(2, 'mischen', 'Mischen', 65,
             r'Du deklarierst bei Mischaufgaben die Mengen, stellst Mengenbilanz und Stoffbilanz auf — Anteil mal Menge, Anteile als Dezimalzahl —, verdünnst mit Wasser als Sorte mit Anteil 0, dampfst ein, indem Wasser verdunstet, und erkennst, wann ein Produkt zweier Unbekannter die Aufgabe quadratisch macht.',
             ('g2-M-lp-mischen', 'Mischen'),
             sim2, [('g2-M-lp-kontrolle-mischen-1', 'Kontrollfragen: eine Unbekannte'), ('g2-M-lp-kontrolle-mischen-2', 'Kontrollfragen: zwei Unbekannte')],
             fest2, [uebung('stoff', 'Mengen- und Stoffbilanz für sys-solv'), uebung('verduennen', 'Verdünnen mit Wasser'), uebung('verdunsten', 'Eindampfen: Wasser verdunstet')],
             auf2, f'<a href="{TS}#mischen">Themenseite 2.M, Typ 2 — Mischen</a>',
             'Taschenrechner erlaubt, 2a ohne')

# ------------------------------------------------------------------ Kapitel 3 · Verteilen
sim3 = sim(3, 'Rechteckmodell: Breite gleich Anzahl, Höhe gleich Wert pro Stück, Fläche gleich Wert',
           '<div class="sl-row">\n          ' + regler('s3', 'x', 'x (Sorte 1)', 0, 20, 1, 6, 'blau')
           + '\n          ' + regler('s3', 'y', 'y (Sorte 2)', 0, 20, 1, 6, 'orange') + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Verteilen: Stückbilanz und Wertbilanz</div>
          <p>\(x\), \(y\): Stückzahlen der Sorten bzw. Anzahl Fahrten — ganze Zahlen, nicht negativ.</p>
          <p>\[ \begin{cases} x + y = N & \text{(Stückbilanz)} \\ a \cdot x + b \cdot y = W & \text{(Wertbilanz)} \end{cases} \]</p>
          <ul>
            <li>\(a\), \(b\) sind die Werte pro Stück (CHF, t, Sitzplätze), \(W\) ist der Gesamtwert: Anzahl mal Wert pro Stück. Im Rechteckmodell ist die Stückbilanz die Breite, die Wertbilanz die Fläche.</li>
            <li>Gibt es mehrere Artikel, deren Gesamtzahl bekannt ist, entsteht <b>pro Artikel eine eigene Stückbilanz</b>; ein Set zählt in jeder.</li>
            <li>Mit einer Unbekannten steht der Rest als Term: \(N - x\).</li>
            <li><b>Quadratisch</b> wird es, wenn Anzahl und Wert pro Stück beide unbekannt sind: \(r \cdot (r + 6)\) Stühle, \(x \cdot y\) Franken.</li>
          </ul>
          <p>Beispiel aus dem Clip: 12 Fahrten zu 18 t und 14 t, zusammen 188 t: \(x + y = 12\), \(18 \cdot x + 14 \cdot y = 188\); \(x = 5\), \(y = 7\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Ein Set nur einmal zählen: Ein Set «Stöcke + Brille» gehört in die Stückbilanz der Stöcke <em>und</em> in die der Brillen.</p>
          <p>Ein Ergebnis wie \(x = 5.5\) Fahrten übernehmen: Stückzahlen sind ganz. Die Probe am Text entscheidet, ob es überhaupt geht.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 10, [
    ('3a', 3, r'Ein Kino verkauft an einem Abend 150 Billette, für Erwachsene zu 17 CHF und für Kinder zu 11 CHF. Die Einnahmen betragen 2190 CHF. Deklariere, stelle das System auf und löse es von Hand ' + OHNE + '.',
     r'<p>\(x\): Anzahl Erwachsenenbillette, \(y\): Anzahl Kinderbillette. \(x + y = 150\) und \(17 \cdot x + 11 \cdot y = 2190\). Mit \(y = 150 - x\): \(6 \cdot x + 1650 = 2190\), \(x = 90\), \(y = 60\). <b>90 Erwachsenen- und 60 Kinderbillette.</b> Probe am Text: \(1530 + 660 = 2190\) CHF ✓.</p>', ''),
    ('3b', 2, r'Ein Laden verkauft Kappen zu 25 CHF, Schals zu 30 CHF und das Set «Kappe + Schal» zu 45 CHF. An einem Tag gehen 20 Kappen und 14 Schals weg — einzeln oder im Set — für zusammen 820 CHF. Deklariere und stelle das System auf. Nicht lösen.',
     r'<p>\(x\): einzeln verkaufte Kappen, \(y\): einzeln verkaufte Schals, \(z\): verkaufte Sets. \(x + z = 20\) (Kappen), \(y + z = 14\) (Schals), \(25 \cdot x + 30 \cdot y + 45 \cdot z = 820\) (CHF).</p><p class="komm">Zur Kontrolle, wenn du es lösen willst: Aus den Stückbilanzen \(x = 20 - z\) und \(y = 14 - z\) — eingesetzt bleibt eine Gleichung mit \(z\): \(25 \cdot (20 - z) + 30 \cdot (14 - z) + 45 \cdot z = 820\), zusammengefasst \(920 - 10 \cdot z = 820\). Also \(z = 10\), \(x = 10\) und \(y = 4\). Mehr zu Systemen mit drei Unbekannten: Themenseite 2.3.</p>', ''),
    ('3c', 3, r'In einem Saal stehen 120 Stühle in gleich langen Reihen. Für eine Feier räumt man 3 Reihen weg und nimmt aus jeder übrigen Reihe 2 Stühle heraus. Jetzt stehen noch 70 Stühle. Wie viele Reihen waren es, und wie viele Stühle standen in jeder? (Taschenrechner)',
     r'<p>\(r\): Anzahl Reihen, \(s\): Stühle pro Reihe — ganze Zahlen, nicht negativ. \(r \cdot s = 120\) und \((r - 3) \cdot (s - 2) = 70\). Ausmultipliziert und \(r \cdot s = 120\) benutzt: \(120 - 2 \cdot r - 3 \cdot s + 6 = 70\), also \(s = \tfrac{56 - 2 \cdot r}{3}\). Eingesetzt und mit 3 multipliziert: \(2 \cdot r^2 - 56 \cdot r + 360 = 0\); poly-solv: \(r_1 = 18\), \(r_2 = 10\) (der Rechner nennt sie \(x_1\), \(x_2\)). Bei 18 Reihen wären es \(\tfrac{120}{18} = 6.\overline{6}\) Stühle pro Reihe — keine ganze Zahl, fällt weg. <b>10 Reihen zu 12 Stühlen.</b> Probe am Text: \(10 \cdot 12 = 120\) ✓, \(7 \cdot 10 = 70\) ✓.</p><p class="komm">Hier sind beide Lösungen positiv. Erst die zweite Unbekannte zeigt, welche Lösung zum Text passt.</p>', ''),
    ('3d', 2, r'(a) Lies im Rechteckmodell ab: Wie viele Stück sind es, und wie gross ist der Gesamtwert? (b) Warum ist mit 12 Stück zu 18 CHF und 7 CHF ein Gesamtwert von genau 100 CHF unmöglich?',
     r'<p>(a) \(4 + 8 = 12\) Stück; Wert \(18 \cdot 4 + 7 \cdot 8 = 72 + 56 = 128\) CHF. (b) \(18 \cdot x + 7 \cdot (12 - x) = 100\) gibt \(11 \cdot x = 16\), also \(x = \tfrac{16}{11}\) — keine ganze Zahl. Bruchteile von Stücken gibt es nicht.</p>',
     bild({'art': 'rechteck', 'x': 4, 'a': 18, 'y': 8, 'b': 7}, 'Rechteckmodell: 4 Stück zu 18 CHF und 8 Stück zu 7 CHF')),
])
k3 = kapitel(3, 'verteilen', 'Verteilen', 60,
             r'Du stellst bei Verteilaufgaben Stückbilanz und Wertbilanz auf — Anzahl mal Wert pro Stück —, zählst Sets in jeder Stückbilanz ihrer Artikel, prüfst, ob Stückzahlen ganz und nicht negativ sind, und erkennst, wann Anzahl und Wert pro Stück beide unbekannt sind: Dann wird es quadratisch.',
             ('g2-M-lp-verteilen', 'Verteilen'),
             sim3, [('g2-M-lp-kontrolle-verteilen-1', 'Kontrollfragen: eine Unbekannte'), ('g2-M-lp-kontrolle-verteilen-2', 'Kontrollfragen: zwei Unbekannte')],
             fest3, [uebung('wertbilanz', 'Stück- und Wertbilanz für sys-solv'), uebung('reihen', 'Anzahl mal Wert pro Stück, quadratisch')],
             auf3, f'<a href="{TS}#verteilen">Themenseite 2.M, Typ 3 — Verteilen</a>',
             'Taschenrechner erlaubt, 3a ohne')

# ------------------------------------------------------------------ Kapitel 4 · Zins
sim4 = sim(4, 'Zwei Anlagen: Kapital und Zins als Balken; oder Zinseszins: 5000 CHF über zwei Jahre',
           wahl('s4-art', 'Bild', [('a', 'zwei Anlagen'), ('b', 'Zinseszins')])
           + '\n        <div class="sl-row">\n          ' + regler('s4', 'x', 'x (Sparkonto)', 0, 30000, 1000, 15000, 'blau', ' CHF', True)
           + '\n          ' + regler('s4', 'p', 'p in %', 0, 5, 0.5, 3, 'gruen', ' %', True) + '\n        </div>')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zins: Kapitalgleichung und Zinsgleichung</div>
          <p>\(x\): Kapital auf Anlage 1 in CHF, \(y\): Kapital auf Anlage 2 in CHF.</p>
          <p>\[ \begin{cases} x + y = K & \text{(Kapitalgleichung)} \\ p_1 \cdot t_1 \cdot x + p_2 \cdot t_2 \cdot y = Z & \text{(Zinsgleichung)} \end{cases} \]</p>
          <ul>
            <li>Zinssätze als <b>Dezimalzahl</b>: 2 % wird zu \(0.02\). Zeitanteil \(t\) in Jahren: Halbjahr \(t = \tfrac{1}{2}\), vier Monate \(t = \tfrac{1}{3}\). Einfacher Zins: Zins \(= p \cdot t \cdot\) Kapital.</li>
            <li><b>Zinseszins</b> (Themenseite, A7): Wird der Zins gutgeschrieben und mitverzinst, wächst ein Kapital pro Jahr mit dem Faktor \(1 + p\): nach zwei Jahren \(K \cdot (1 + p)^2\).</li>
            <li><b>Einfacher Zins</b> über zwei Jahre (Zins nicht mitverzinst): \(K \cdot (1 + 2 \cdot p)\). <b>Zinseszins:</b> \(K \cdot (1 + p)^2\).</li>
            <li><b>Quadratisch</b> wird es, wenn bei Zinseszins \(p\) gesucht ist oder wenn Kapital und Zinssatz beide unbekannt sind (\(K \cdot p\)). Bei ganzzahligen Koeffizienten zeigt poly-solv eine Lösung wie \(\tfrac{1}{50}\) als Bruch; die Umschalttaste ↔ zeigt die Dezimalzahl. Steht in der Grundform eine Dezimalzahl, multiplizierst du die Gleichung vorher, bis alle Koeffizienten ganz sind.</li>
          </ul>
          <p>Beispiel aus dem Clip: 30 000 CHF zu 0.75 % und 2 %, 425 CHF Zins: \(x + y = 30\,000\), \(0.0075 \cdot x + 0.02 \cdot y = 425\); \(x = 14\,000\), \(y = 16\,000\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Zinssatz in Prozent stehen lassen: \(0.75 \cdot x + 2 \cdot y = 425\) rechnet mit 75 % und 200 %.</p>
          <p>Den Zeitanteil vergessen: Ein Halbjahr zum vollen Jahressatz gibt den doppelten Zins.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 10, [
    ('4a', 3, r'Frau Rossi legt 16 000 CHF an: einen Teil zu 1.5 %, den Rest zu 2.5 %. Nach einem Jahr erhält sie 300 CHF Zins. Deklariere, stelle das System auf und löse es von Hand ' + OHNE + '.',
     r'<p>\(x\): Kapital zu 1.5 % in CHF, \(y\): Kapital zu 2.5 % in CHF. \(x + y = 16\,000\) und \(0.015 \cdot x + 0.025 \cdot y = 300\). Mit \(x = 16\,000 - y\): \(240 + 0.01 \cdot y = 300\), \(y = 6000\), \(x = 10\,000\). <b>10 000 CHF zu 1.5 %, 6000 CHF zu 2.5 %.</b> Probe: \(150 + 150 = 300\) CHF ✓.</p>', ''),
    ('4b', 2, r'Welcher Faktor steht in der Zinsgleichung vor dem Kapital? (a) 1.8 %, 8 Monate (b) 0.9 %, ein Vierteljahr (c) 2.4 %, 5 Monate',
     r'<p>(a) \(0.018 \cdot \tfrac{8}{12} = 0.012\). (b) \(0.009 \cdot \tfrac{1}{4} = 0.00225\). (c) \(0.024 \cdot \tfrac{5}{12} = 0.01\).</p>', ''),
    ('4c', 3, r'10 000 CHF liegen zwei Jahre auf einem Konto; der Zins wird mitverzinst. Im zweiten Jahr ist der Zinssatz um 0.5 Prozentpunkte höher als im ersten. Nach zwei Jahren sind es 10 353 CHF. Bestimme den Zinssatz des ersten Jahres: Gleichung, Grundform, poly-solv, Antwort.',
     r'<p>\(p\): Zinssatz im ersten Jahr als Dezimalzahl, im zweiten Jahr \(p + 0.005\). \(10\,000 \cdot (1 + p) \cdot (1.005 + p) = 10\,353\). Ausmultipliziert: \(10\,000 \cdot p^2 + 20\,050 \cdot p + 10\,050 = 10\,353\), Grundform \(10\,000 \cdot p^2 + 20\,050 \cdot p - 303 = 0\); poly-solv: \(x_1 = \tfrac{3}{200} = 0.015\), \(x_2 = -\tfrac{101}{50} = -2.02\) (unter −100 %, verworfen). <b>1.5 % im ersten, 2 % im zweiten Jahr.</b> Probe am Text: \(10\,000 \cdot 1.015 = 10\,150\) und \(10\,150 \cdot 1.02 = 10\,353\) ✓.</p><p class="komm">Hier hilft Wurzelziehen nicht: Die zwei Jahre haben verschiedene Faktoren.</p>', ''),
    ('4d', 2, r'(a) Lies im Bild die beiden Kapitalien und ihre Zinssätze ab und berechne den Zins nach einem Jahr. (b) Warum ist der Zins nicht \(20\,000 \cdot 1.75\,\% = 350\) CHF, obwohl 1.75 % der Mittelwert der Zinssätze ist?',
     r'<p>(a) 12 000 CHF zu 1 % und 8000 CHF zu 2.5 %: \(120 + 200 = 320\) CHF. (b) Mehr Geld liegt zum tieferen Zinssatz. Der mittlere Zinssatz gälte nur, wenn beide Kapitalien gleich gross wären.</p>',
     bild({'art': 'zins', 'x': 12000, 'p1': 0.01, 'y': 8000, 'p2': 0.025}, 'Kapital 20 000 CHF, geteilt in 12 000 CHF zu 1 Prozent und 8000 CHF zu 2.5 Prozent, darunter die Zinsen')),
])
k4 = kapitel(4, 'zins', 'Zins', 65,
             r'Du stellst Kapitalgleichung und Zinsgleichung auf — Zinssatz als Dezimalzahl, Zeit in Jahren —, rechnest mit Zinseszins über zwei Jahre (Faktor \(1 + p\) pro Jahr) und löst die entstehenden linearen und quadratischen Gleichungen und Systeme, wo nötig mit dem Rechner.',
             ('g2-M-lp-zins', 'Zins'),
             sim4, [('g2-M-lp-kontrolle-zins-1', 'Kontrollfragen: eine Unbekannte'), ('g2-M-lp-kontrolle-zins-2', 'Kontrollfragen: zwei Unbekannte')],
             fest4, [uebung('faktor', 'Zinssatz mal Zeit'), uebung('zinseszins', 'Zinseszins: Grundform und Zinssatz')],
             auf4, f'<a href="{TS}#zins">Themenseite 2.M, Typ 4 — Zins</a> und Aufgabe A7 (Zinseszins)',
             'Taschenrechner erlaubt, 4a ohne')

# ------------------------------------------------------------------ Vorwissen
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-gf">Vorwissen · GF 2.2 · 2.3</span><span class="zeit">≈ 20 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Das Bilanzprinzip in vier Schritten, die vier Arten von Gleichungen mit ihrer Grundform und die zwei Löser des TI-30X Pro (MathPrint bzw. MultiView). Wenn das wackelt: Leitprogramm <a href="lineare-quadratische-gleichungen.html">Lineare und quadratische Gleichungen</a> (GF 2.2) und <a href="../grundlagen/g2-3-lineare-gleichungssysteme.html">Themenseite 2.3 Lineare Gleichungssysteme</a>.</p>
      ''' + clipkarte('g2-M-deklarieren-bilanzieren', 'Textaufgaben: zuerst deklarieren, dann bilanzieren', '1:14') + '''
      ''' + clipkarte('g2-2b-ti30x-poly-solv', 'Quadratische Gleichungen: mit poly-solv lösen', '1:11') + '''
      ''' + clipkarte('g2-3-ti30x-sys-solv', 'Gleichungssysteme: 2×2 mit sys-solv lösen', '1:12') + r'''
      <div class="festhalten">
        <div class="merk">
          <div class="titel">Vom Text zur Lösung</div>
          <p>Das Bilanzprinzip der Themenseite in vier Schritten: <b>① Unbekannte deklarieren</b> — mit Bedeutung und Einheit; <b>② Gleichungen aufstellen</b> — so viele unabhängige wie Unbekannte, jede eine Bilanz; <b>③ Lösen</b>; <b>④ Probe am Text</b>. In den Kontrollclips ist ③ geteilt: zuerst die <b>Grundform</b>, dann <b>Lösen</b>.</p>
          <div class="tab-rahmen"><table class="arten">
            <tr><th>Art</th><th>Grundform</th><th>Lösen</th></tr>
            <tr><td>lineare Gleichung</td><td>\(a \cdot x = c\) mit \(a \neq 0\)</td><td>von Hand: \(x = c : a\) (oder num-solv)</td></tr>
            <tr><td>quadratische Gleichung</td><td>\(a \cdot x^2 + b \cdot x + c = 0\)</td><td>poly-solv: \(a\), \(b\), \(c\) mit Vorzeichen</td></tr>
            <tr><td>lineares Gleichungssystem</td><td>\(a_1 \cdot x + b_1 \cdot y = c_1\)<br>\(a_2 \cdot x + b_2 \cdot y = c_2\)</td><td>sys-solv 2×2 — oder von Hand (Einsetzen, Addition)</td></tr>
            <tr><td>quadratisches Gleichungssystem</td><td>eine Gleichung nach einer Unbekannten auflösen, einsetzen: quadratische Gleichung</td><td>poly-solv, dann die zweite Unbekannte</td></tr>
          </table></div>
          <p>«Grundform» heisst hier die geordnete Form, die der Rechner verlangt. Die Themenseite 2.2b nennt \(a \cdot x^2 + b \cdot x + c = 0\) die allgemeine Form, das Leitprogramm <a href="lineare-quadratische-gleichungen.html">Lineare und quadratische Gleichungen</a> \(a \cdot x = c\) die Zwischenform. Jede Art geht auch ganz von Hand.</p>
        </div>
        <div class="warn">
          <div class="titel">Rechner richtig lesen</div>
          <p>poly-solv zeigt immer beide Lösungen der Gleichung — welche zum Text passen, entscheidest du. Es nennt sie \(x_1\) und \(x_2\), auch wenn die Unbekannte bei dir \(n\), \(r\) oder \(p\) heisst; sys-solv nennt die Unbekannten \(x\) und \(y\), auch wenn sie bei dir \(z\) und \(e\) heissen.</p>
          <p>Das Minus einer negativen Zahl kommt mit der Vorzeichentaste (−). Brüche wie \(\tfrac{1}{50}\) schaltet die Umschalttaste in die Dezimalzahl um.</p>
        </div>
      </div>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Für 18 CHF erhält man Äpfel zu 3.60 CHF pro kg. Deklariere die Unbekannte vollständig, stelle die Gleichung auf und löse sie.',
     r'<p>\(x\): Masse der Äpfel in kg. \(3.60 \cdot x = 18\), also \(x = 5\) kg.</p><p class="komm">Deklaration mit Grösse, Bezug und Einheit — Themenseite 2.M, Bilanzprinzip.</p>', ''),
    ('0b', 2, r'Welche Art ist es — lineare oder quadratische Gleichung, lineares oder quadratisches System? (a) \(3 \cdot (x - 2) = x + 4\) (b) \(x \cdot (x + 3) = 10\) (c) \(x + y = 5\) und \(2 \cdot x - y = 1\) (d) \(x + y = 5\) und \(x \cdot y = 6\)',
     r'<p>(a) linear. (b) quadratisch: ausmultipliziert \(x^2 + 3 \cdot x\). (c) lineares System. (d) quadratisches System: \(x \cdot y\) ist ein Produkt der Unbekannten.</p>', ''),
    ('0c', 2, r'Bring \((x - 3)^2 = 2 \cdot x + 1\) in die Grundform und gib \(a\), \(b\) und \(c\) an, wie du sie in poly-solv eintippst.',
     r'<p>\(x^2 - 6 \cdot x + 9 = 2 \cdot x + 1\), also \(x^2 - 8 \cdot x + 8 = 0\): \(a = 1\), \(b = -8\), \(c = 8\).</p><p class="komm">Binom, auf null bringen, Vorzeichen — Leitprogramm <a href="lineare-quadratische-gleichungen.html#verfahren">Lineare und quadratische Gleichungen, Kapitel 4</a>.</p>', ''),
    ('0d', 2, r'Ordne das System für sys-solv: \(y = 2 \cdot x - 3\) und \(3 \cdot x = 12 - 2 \cdot y\). Welche sechs Zahlen tippst du ein?',
     r'<p>\(2 \cdot x - y = 3\) und \(3 \cdot x + 2 \cdot y = 12\): Zeile 1: 2, −1, 3; Zeile 2: 3, 2, 12. Gleichwertig \(-2 \cdot x + y = -3\).</p><p class="komm">Jede Zeile: erst \(x\), dann \(y\), dann die Zahl — Clip «2×2 mit sys-solv lösen».</p>', ''),
    ('0e', 2, r'Löse von Hand ' + OHNE + r': \(x + y = 9\) und \(3 \cdot x + y = 21\).',
     r'<p>Subtrahieren: \(2 \cdot x = 12\), \(x = 6\), \(y = 3\). \(\mathbb{L} = \{(6 \mid 3)\}\).</p><p class="komm">Themenseite 2.3, Verfahren — RLP 2.3 verlangt das auch ohne Hilfsmittel.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/' + DATEI + '/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-gf">GF 2.1 · 2.3 · Kapitel 1–4</span><span class="zeit">≈ 35 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Deklaration, Ansatz und Rechenweg. Teil A ohne Taschenrechner, Teil B mit Taschenrechner.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben. Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Aufgabenarten sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Tüfteln, Kontrollclips und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast — zuerst die Kontrollclips.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 0 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 3; G3 → 3; G4 → 2; G5 → 2; G6 → 4; G7 → 4</p>
        </div>
      </div>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Textaufgaben modellieren, Version 1.0 (08.10.2026). Gebaut aus
     scripts/lp/modellieren/seite.py — Änderungen dort, nicht in dieser Datei. Verfahren: HOWTO-leitprogramme.md
     (Kapitelmuster). Auftrag: scripts/lp/modellieren/AUFTRAG.md. Alle Zahlen: scripts/lp/modellieren/zahlen.py.

     RLP-BM 2030, Grundlagenfach, Lerngebiet 2 Gleichungen, Ungleichungen und Gleichungssysteme, Teilgebiete 2.1
     und 2.3 — wörtlich wie in der RLP-Box der Themenseite 2.M (geprüft gegen Math-GL.pdf):
       K1  gegebene Sachverhalte im technischen Kontext als Gleichung, Ungleichung oder Gleichungssystem formulieren (2.1)
       K2  den Typ einer Gleichung bestimmen und beim Lösen entsprechend beachten, Lösungs- und Umformungsmethoden
           zielführend einsetzen sowie Lösungen überprüfen (2.1)
       K3  ein lineares Gleichungssystem mit maximal drei Variablen lösen (auch ohne Hilfsmittel) (2.3)
     K1, K2 ohne Vermerk: Taschenrechner erlaubt (TI-30X Pro, Löser poly-solv und sys-solv). K3 «auch ohne
     Hilfsmittel»: je Kapitel eine Aufgabe (1a, 2a, 3a, 4a) und der Gesamttest-Teil A ohne Rechner (G1–G3).

     Kompetenzmatrix (Kompetenz | ohne HM? | Kapitel | Kapitelaufgaben | Gesamttest):
       K1 als Gleichung oder Gleichungssystem formulieren | —        | 1–4 (Clips, Sim.) | 1a, 1b, 2a, 2b, 2c, 3a, 3b, 3c, 4a, 4c | G1–G7
       K1 «Ungleichung»                                   | —        | nicht hier → LP/Themenseite 2.2a (Ungleichungen); die Themenseite 2.M hat keine
       K2 Typ bestimmen, Methoden zielführend, prüfen     | —        | 0–4               | 0b, 0c, 1b, 1c, 1d, 2c, 2d, 3c, 3d, 4c, 4d; Übung «art» | G2, G3, G5, G6, G7
       K3 lineares System lösen, auch ohne HM             | ja       | 0–4               | 0d, 0e, 1a, 2a, 3a, 4a              | G1, G2, G3 (ohne TR); G4, G7 (sys-solv)
       K3 drei Variablen                                  | ja       | 3 (Set: aufstellen, Lösungsweg im Kommentar) | 3b     | G3 (Set, über Terme mit einer Unbekannten)
     Kein Kapitelziel ohne Kompetenz.

     Planung (Kapitel | Lernziel | Clips | Tüfteln | Kontrollclip-Aufgaben: Gleichungsart → Löser | Häufiger Fehler | min):
       0 Vorwissen  | Bilanzprinzip, Arten, Grundform, Löser | g2-M-deklarieren-bilanzieren, g2-2b-ti30x-poly-solv, g2-3-ti30x-sys-solv | — | — | — | 20
       1 Zahlen     | 10·z + e, je Aussage eine Gleichung | lp-zahlenraetsel + 2 Kontrollclips | sim1 Zehnerstangen | aufeinanderfolgende Zahlen, Summe 132 (linear → von Hand);
                      Quadratsumme 113 (quadratisch → poly-solv); Quersumme 12, vertauscht +36 (LGS → sys-solv); z = e + 2, Zahl mal Quersumme 640 (QGS → poly-solv) | um/mal, Richtung, z · e | 60
       2 Mischen    | Mengen- und Stoffbilanz, Wasser 0 | lp-mischen + 2 | sim2 Gefässe | 12 l Sirup verdünnen (linear); Fass 40 l zweimal abzapfen (quadratisch);
                      60 % und 85 % zu 50 kg (LGS); Salzlösung m · p = 3, 5 Prozentpunkte weniger (QGS) | Prozent statt Menge | 65
       3 Verteilen  | Stück- und Wertbilanz, Sets, ganze Zahlen | lp-verteilen + 2 | sim3 Rechteckmodell | 24 Billette (linear); 216 Stühle in Reihen (quadratisch);
                      Fähre 70 Fahrzeuge (LGS); Bus 360 CHF (QGS) | Set einmal gezählt | 60
       4 Zins       | Kapital- und Zinsgleichung, Zeitanteil, Zinseszins | lp-zins + 2 | sim4 Balken/Zinseszins | 12 000 CHF mit Halbjahr (linear);
                      Zinseszins mit Einzahlung 7242 CHF (quadratisch); vertauschte Zinssätze (LGS); K · p = 480 (QGS) | Prozent stehen lassen, Zeitanteil | 65
       Gesamttest 35 — Summe 305 min (rund 7 Lektionen): Vorwissen 20, Kapitel 60 + 65 + 60 + 65, Gesamttest 35.
       Zeiten neu geschätzt nach der Prüfung (08.10.2026, M12) aus den Teilen: Einführungsclip 3, Tüfteln 8, zwei Kontrollclips mit
       je 10 Fragen und Rechner 2 × 10, Festhalten 3, Übungen 10–15 (Kapitel 2: drei), Aufgaben auf Papier 15. Das ist mehr als die
       Zielgrösse des Kapitelmusters (HOWTO §3: 35–45 min je Kapitel, bis 5 Lektionen) — offen, ob geteilt wird.
       Clips: 12 eigene (dazu 3 der Themenseiten).

     Gesamttest (Neufassung 08.10.2026 nach Prüfung H1, M3, M4): Teil A ohne Taschenrechner — G1 Ziffernrätsel (LGS), G2 Ansätze
     vergleichen (LGS, eine Unbekannte), G3 Set mit drei Unbekannten über Terme (linear); Teil B mit Taschenrechner — G4 zwei Lösungen
     und Wasser (LGS, sys-solv), G5 Eindampfen mit Masse und Anteil unbekannt (QGS, poly-solv), G6 Zinseszins mit Abhebung
     (quadratisch, poly-solv), G7 gleich viel Zins mit Zeitanteil (LGS, sys-solv). Jede Aufgabe kombiniert Geübtes neu: Wasser als
     dritte Sorte (Clip Verdünnen + LGS), Eindampfen (Übung) mit m · p (Kontrollclip), Abhebung (Übung Zinseszins), Set (Clip, 3b) mit
     Rest als Term (Kontrollclips), «gleich viel Zins» statt Gesamtzins.

     Kern: alles oben. Vertiefung: Zinseszins ist auf der Themenseite Vertiefung (A7); hier Kern von Kapitel 4, weil der Auftrag in jeder
     Aufgabenart eine quadratische Gleichung verlangt und der Zinseszins die natürliche ist (eingeführt im Einführungsclip).
     Bewusst weggelassen (→ Themenseite 2.M): Bruchrätsel (Bruchgleichungen), Systeme mit drei Unbekannten allgemein lösen (das Set nur über Terme mit einer Unbekannten),
     die technische Zusatzserie A8–A11 (Widerstände, Träger, Linse, Mischtemperatur), der Ansatz-Trainer; Ungleichungen (2.2a).

     Konventionen wie auf der Themenseite: Deklaration mit Bedeutung und Einheit; z Zehnerziffer, e Einerziffer, Zahl 10 · z + e;
     Mengenbilanz x + y = M, Stoffbilanz p₁ · x + p₂ · y = p · M; Stückbilanz x + y = N, Wertbilanz a · x + b · y = W; Kapitalgleichung
     x + y = K, Zinsgleichung p₁ · t₁ · x + p₂ · t₂ · y = Z; Anteile und Zinssätze als Dezimalzahl, t in Jahren; Zinseszins K · (1 + p)²;
     Multiplikationspunkt in Gleichungen wie auf der Themenseite; Mengen mit Strichpunkt; Probe am Text.
     Farben: erste Unbekannte blau, zweite orange, Ergebnis/Mischung grün, Fehler rot — in Clips und Seite gleich.

     Bewusst anders als die Themenseite:
       – Schritt ③ Lösen ist geteilt in «Grundform» und «Lösen» mit dem TI-30X Pro (poly-solv, sys-solv), wie im Auftrag; die Themenseite
         löst von Hand. Das Verfahren von Hand bleibt in den a-Aufgaben und im Gesamttest (RLP 2.3, auch ohne Hilfsmittel).
       – «Grundform» für die geordnete Form, die der Rechner verlangt; die Themenseite 2.2b sagt «allgemeine Form» (einmal vermerkt).
       – Zinseszins im Kern (siehe oben).

     Widersprüche und Lücken in der Themenseite (gemeldet, nicht übernommen):
       – Merksatz «Jede Misch-, Verteil- und Zinsaufgabe ist eine Mengenbilanz plus eine Wertbilanz» — mit Sets braucht es zwei
         Stückbilanzen (eigenes Beispiel der Seite: drei Gleichungen), und zwei Zinsgleichungen ohne Kapitalgleichung (vertauschte
         Zinssätze) passen nicht ins Schema. Im Leitprogramm darum «so viele Bilanzen wie Unbekannte».
       – RLP-Box «Teilgebiete 2.1 und 2.3» mit der 2.3-Kompetenz; Breadcrumb und JSON-LD (build-seo.py) nennen nur «2.1 Grundlagen».
       – K1 nennt «Ungleichung»; die Themenseite 2.M behandelt keine. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">begreifbar.ch · Leitprogramm</p>
      <h1>Textaufgaben modellieren</h1>
      <p class="unter">Vom Text zur Deklaration, zum Ansatz und mit dem Rechner zur Lösung — für Zahlenrätsel, Mischen, Verteilen und Zins. Vier Kapitel zu je rund anderthalb Lektionen, dazu Vorwissen und Gesamttest — zusammen rund sieben Lektionen.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Grundlagenfach 2.1 · 2.3</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Zahlenrätsel</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Mischen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Verteilen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Zins</span></a></li>
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
          <li><b>① Clip</b> anschauen: die Grundgleichung der Aufgabenart.</li>
          <li><b>② Tüfteln:</b> Aufgaben in der Simulation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Zwei Clips führen je zwei Aufgaben vom Text bis zur Antwort. Der Clip hält an jedem Schritt an — erst antworten. Den Taschenrechner bereitlegen.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, mit Deklaration und Ansatz, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Grundlagenfach, Teilgebiete 2.1 Grundlagen und 2.3 Lineare Gleichungssysteme:</p>
        <ul>
          <li><b>K1</b> gegebene Sachverhalte im technischen Kontext als Gleichung, Ungleichung oder Gleichungssystem formulieren — Kapitel 1–4 (ohne Ungleichungen)</li>
          <li><b>K2</b> den Typ einer Gleichung bestimmen und beim Lösen entsprechend beachten, Lösungs- und Umformungsmethoden zielführend einsetzen sowie Lösungen überprüfen — Kapitel 0–4</li>
          <li><b>K3</b> ein lineares Gleichungssystem mit maximal drei Variablen lösen <span class="ohm">auch ohne Hilfsmittel</span> — Kapitel 1–4, je die erste Aufgabe ohne Taschenrechner</li>
        </ul>
        <p class="rlp-quelle">Auf der <a href="''' + TS + '''">Themenseite 2.M</a>, nicht hier: Bruchrätsel, Systeme mit drei Unbekannten allgemein lösen, die technischen Sachverhalte A8–A11 und der Ansatz-Trainer. Ungleichungen: <a href="../grundlagen/g2-2a-lineare-gleichungen.html">Themenseite 2.2a</a>.</p>
      </details>
    </div>
'''
unten = '''
    <div class="duo">
      <div>
        <h3 id="weiter">Weiter</h3>
        <p>Zum Nachschlagen: <a href="''' + TS + '''">Themenseite 2.M Textaufgaben modellieren</a> — mit dem Ansatz-Trainer, Bruchrätseln, einem System mit drei Unbekannten und technischen Sachverhalten (Widerstände, Träger, Linse, Mischtemperatur). Im Grundlagenfach geht es weiter mit den Funktionen; das Leitprogramm <a href="lineare-funktionen.html">Lineare Funktionen</a> (GF 3.2) beginnt dort.</p>
      </div>
    </div>

    <div class="fuss">
      <span>Leitprogramm Textaufgaben modellieren · Clips von mathe.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''
# Zeiten (neu geschätzt 08.10.2026, Prüfung M12): Vorwissen 20 · K1 60 · K2 65 · K3 60 · K4 65 · Gesamttest 35 = 305 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + unten
seite = kopf + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + basis + open(SP + 'seite.js').read().replace(
    '<script>\n/* Leitprogramm Modellieren —', '<script>\n/* Leitprogramm Modellieren —') + '\n' + fuss
open(ZIEL, 'w').write(seite)
print('geschrieben', len(seite.splitlines()), 'Zeilen')
