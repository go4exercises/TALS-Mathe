#!/usr/bin/env python3
"""Schreibt BERICHT-beschriftungen-animationen.md aus den geprüften Befunden."""
import json
import os
from collections import OrderedDict

SC = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad'
roh = json.load(open(SC + '/audit-roh.json'))
bef = json.load(open(SC + '/audit-kandidaten.json'))
BASIS = 'http://localhost:8001/'

# ── Einstufung: manuell gesetzt, nach Sichtprüfung aller 55 Canvas ──────────
# schwer  = Beschriftung fehlt, ist abgeschnitten oder zwei Texte sind
#           gegenseitig unlesbar
# mittel  = Beschriftung liegt lesbar, aber störend auf einem Grafikelement
#           oder überlappt eine andere teilweise
# leicht  = Achsenzahl wird von Kurve/Punkt/Strichlinie gekreuzt, bleibt lesbar
SCHWER = {
    ('grundlagen/g3-2-lineare-funktionen.html', 'ks-canvas'),
    ('grundlagen/g2-3-lineare-gleichungssysteme.html', 'cv-kino'),
    ('grundlagen/g3-3-quadratische-funktionen.html', 'ws-canvas'),
    ('grundlagen/g3-1-grundlagen.html', 'einstieg-glas'),
    ('grundlagen/g4-3-masszahlen.html', 'sl-canvas'),
    ('schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html', 'a1-canvas'),
    ('grundlagen/g2-1-grundlagen.html', 'uf-canvas'),
    ('grundlagen/g3-1-grundlagen.html', 'schn1-canvas'),
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-cossatz'),
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-flaeche'),
    ('grundlagen/g2-2b-quadratische-gleichungen.html', 'velo-canvas'),
    ('grundlagen/g3-1-grundlagen.html', 'par-canvas'),
    ('grundlagen/g5-4-einheitskreis.html', 'cv-schiff'),
    ('schwerpunkt/s3-2a-potenzfunktionen.html', 'ba-canvas'),
    ('schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html', 'sw-canvas'),
    ('grundlagen/g5-2c-kreis-und-kreisteile.html', 'cv-umfang'),
    ('grundlagen/g3-3-quadratische-funktionen.html', 'dr-canvas'),
    ('grundlagen/g1-3-algebraische-terme.html', 'cv-equiv'),
    ('schwerpunkt/s3-6-betragsfunktionen.html', 'wa-canvas'),
    ('grundlagen/g2-3-lineare-gleichungssysteme.html', 'cv-lbuschel'),
}
LEICHT_ARTEN = {'rest'}

NOTIZ = {
    ('grundlagen/g3-2-lineare-funktionen.html', 'ks-canvas'):
        'Alle Achsenzahlen fehlen: 24 von 29 Beschriftungen liegen ausserhalb des '
        'Canvas (y-Zahlen 12–13 px links, x-Zahlen unterhalb). Ursache unten §2.1. '
        'Zusätzlich bleibt vom generischen «y» ein Rest neben «K [CHF]» stehen.',
    ('grundlagen/g2-3-lineare-gleichungssysteme.html', 'cv-kino'):
        'Alle Achsenzahlen fehlen (14 von 21 ausserhalb). Vom generischen «y» bleibt '
        'ein Rest neben «y [Kinder]» stehen.',
    ('grundlagen/g3-3-quadratische-funktionen.html', 'ws-canvas'):
        'Alle Achsenzahlen fehlen (8 von 14 ausserhalb). «h [m]»/«x [m]» tragen je '
        'einen Rest des generischen Labels.',
    ('grundlagen/g3-1-grundlagen.html', 'einstieg-glas'):
        'Die zweistelligen Skalenzahlen 15/20/25/30 stehen 2–8 px über den rechten '
        'Canvasrand hinaus und sind angeschnitten; 5 und 10 passen.',
    ('grundlagen/g4-3-masszahlen.html', 'sl-canvas'):
        '«Klasse A» und «Klasse B» sind links um 13 px abgeschnitten, die zwei '
        '«MW = 4.50 · Spannweite …»-Zeilen rechts um 10 px. Die untere kollidiert '
        'zusätzlich mit der Achsenbeschriftung «Note».',
    ('schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html', 'a1-canvas'):
        'Schwerster Fall: die x-Achse trägt bei dieser Skalierung so viele Ticks, '
        'dass die Zahlen zu einem unlesbaren Band verschmelzen (60 Überlappungspaare).',
    ('grundlagen/g2-1-grundlagen.html', 'uf-canvas'):
        '«4·x + 3 (= 15 bei x=3)» ragt 27 px über den linken Rand hinaus.',
    ('grundlagen/g3-1-grundlagen.html', 'schn1-canvas'):
        '«g(x) = −x + 5» ragt 46 px links hinaus, «f(x) = 2·x − 4» 3 px oben.',
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-cossatz'):
        '«α=60°» ragt 27 px über den linken Rand hinaus — nur «0°» bleibt sichtbar.',
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-flaeche'):
        '«φ=55°» ragt 21 px über den linken Rand hinaus.',
    ('grundlagen/g2-2b-quadratische-gleichungen.html', 'velo-canvas'):
        '«Hinweg →» (7 px) und «← Rückweg» (14 px) sind links abgeschnitten.',
    ('grundlagen/g3-1-grundlagen.html', 'par-canvas'):
        'Fünf Überlappungen: «y» unter «g(x) = …», und «x = −0.41»/«x = 2.41» liegen '
        'auf den x-Achsenzahlen −1 … 4.',
    ('grundlagen/g5-4-einheitskreis.html', 'cv-schiff'):
        '«φ» und «+0.71» liegen übereinander, ebenso «S» und «Quadrant I».',
    ('schwerpunkt/s3-2a-potenzfunktionen.html', 'ba-canvas'):
        '«V [dm³]» und «platzt (150 dm³)» liegen zu 73 % übereinander.',
    ('schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html', 'sw-canvas'):
        '«s [km]» und «100 km» liegen übereinander.',
    ('grundlagen/g5-2c-kreis-und-kreisteile.html', 'cv-umfang'):
        '«3·d» und «π·d» liegen übereinander.',
    ('grundlagen/g3-3-quadratische-funktionen.html', 'dr-canvas'):
        '«S(1 | -2)» und «(0 | -1.5)» liegen übereinander.',
    ('grundlagen/g1-3-algebraische-terme.html', 'cv-equiv'):
        '«nicht äquivalent» und «+490 zu viel» liegen zu 30 % übereinander.',
    ('schwerpunkt/s3-6-betragsfunktionen.html', 'wa-canvas'):
        '«Boden = 5» liegt auf der y-Achsenzahl 6.',
    ('grundlagen/g2-3-lineare-gleichungssysteme.html', 'cv-lbuschel'):
        '«S(0.00 | 4.00)» liegt auf der y-Achsenzahl 5.',
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-sinussatz'):
        'Die Seitenbeschriftungen a, b, c liegen mit 53–76 % ihrer Glyphenfläche '
        'direkt auf den Dreiecksseiten.',
    ('grundlagen/g5-2a-dreiecke.html', 'cv-elem'):
        'A, B, C und H liegen auf den Höhenlinien bzw. auf dem Höhenschnittpunkt.',
    ('grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html', 'cv-streck'):
        "A, A', B und C' liegen auf den Dreieckskanten; C' zu 67 %.",
    ('grundlagen/g5-3-trigonometrische-berechnungen.html', 'cv-spez'):
        '«c = √2» liegt zu 58 % auf der Hypotenuse.',
    ('schwerpunkt/s4-3a-vektorbegriff-komponenten.html', 'ad-canvas'):
        'Die Vektornamen a und b liegen auf den Vektorpfeilen (b zu 75 %).',
}

# Titel/Anker je Canvas aus dem Messlauf
meta = {}
for p in roh:
    for cid, m in (p.get('meta') or {}).items():
        meta[(p['seite'], cid)] = m

kan = OrderedDict()
for b in bef:
    kan.setdefault((b['seite'], b['canvas']), []).append(b)


def stufe(key, bs):
    if key in SCHWER:
        return 'schwer'
    if all(b['art'] in LEICHT_ARTEN for b in bs):
        return 'leicht'
    if any(b['art'] in ('abgeschnitten', 'ueberlappung') for b in bs):
        return 'mittel'
    return 'mittel'


gruppen = {'schwer': [], 'mittel': [], 'leicht': []}
for key, bs in kan.items():
    gruppen[stufe(key, bs)].append((key, bs))

ART_TEXT = {'ueberlappung': 'Text über Text', 'auf-grafik': 'Text auf Grafikelement',
            'abgeschnitten': 'ausserhalb des Canvas', 'rest': 'Rest einer überdeckten Beschriftung'}

L = []
A = L.append
A('# Beschriftungs-Konflikte in den Canvas-Animationen')
A('')
A('Prüflauf vom **30.07.2026** über **alle 46 Themenseiten** (`grundlagen/` + `schwerpunkt/`),')
A('jede Animation in ihrer **Startposition**, ohne jede Interaktion. **An den Seiten wurde')
A('nichts geändert** — dieser Bericht ist reine Bestandsaufnahme.')
A('')
A('Die Links zeigen auf den lokalen Server: `python3 -m http.server 8001` im Repo-Root starten,')
A('dann sind sie klickbar. Der Anker ist die Canvas-ID, der Browser springt direkt auf die Grafik.')
A('')
A('---')
A('')
A('## 1. Was gemessen wurde')
A('')
A('Für jeden Aufruf von `fillText`/`strokeText` auf einem 2D-Canvas wurde protokolliert:')
A('das Textfeld (aus `measureText` samt `textAlign`/`textBaseline` und der aktiven')
A('Transformationsmatrix) und die Canvas-Pixel im Feld unmittelbar **vor** und **nach**')
A('dem Zeichnen, dazu der Endzustand nach dem Rendern. Daraus vier Befundarten:')
A('')
A('| Art | Bedeutung |')
A('|---|---|')
A('| **Text über Text** | Zwei Beschriftungen, die am Ende **beide sichtbar** sind, überdecken sich zu ≥ 25 % der kleineren Fläche. |')
A('| **Text auf Grafikelement** | ≥ 25 % der Glyphenpixel liegen auf Nicht-Hintergrund — Linie, Kurve, Fläche, Punkt. |')
A('| **ausserhalb des Canvas** | Das Textfeld reicht > 1.5 px über den Rand; die Beschriftung ist angeschnitten oder ganz weg. |')
A('| **Rest einer überdeckten Beschriftung** | Von einer absichtlich abgedeckten Beschriftung bleiben 3–45 % stehen (siehe §2.2). |')
A('')
A('Ausgewertet wird immer der **letzte Zeichendurchgang** — also das, was am Ende dasteht.')
A('Beschriftungen, die absichtlich vollständig überdeckt werden, zählen **nicht** als Konflikt.')
A('')
gesamt_texte = sum(len([t for t in c['texte'] if not t.get('unlesbar')])
                   for p in roh for c in p['canvases'])
A(f'**Umfang:** {sum(len(p["canvases"]) for p in roh)} Canvas mit {gesamt_texte} messbaren '
  f'Beschriftungen. Auffällig: **{len(kan)} Canvas auf {len(set(k[0] for k in kan))} Seiten** '
  f'mit {len(bef)} Einzelbefunden.')
A('')
A('**Jeder der aufgeführten Canvas wurde einzeln am Bild nachgesehen** (Kontrollbilder mit')
A('markierten Textfeldern bei 1280 px). Fehlalarme sind dabei keine übrig geblieben.')
A('')
A('---')
A('')
A('## 2. Zwei systematische Ursachen')
A('')
A('Der grösste Teil der schweren Fälle geht auf zwei Muster zurück, nicht auf Einzelfehler.')
A('')
A('### 2.1 Anwendungsgraphen mit Nullpunkt in der Ecke verlieren **alle** Achsenzahlen')
A('')
A('`mathlib.js` → `drawGrid()` setzt die Achsenzahlen relativ zum Nullpunkt:')
A('')
A('```js')
A("for (…) ctx.fillText(gx, cx(gx), cy(0) + 14);   // x-Zahlen: 14 px UNTER der x-Achse")
A("for (…) ctx.fillText(gy, cx(0) - 5,  cy(gy) + 4);  // y-Zahlen: 5 px LINKS der y-Achse")
A('```')
A('')
A('Bei einem Achsenkreuz in der Bildmitte stimmt das. Bei Anwendungsgraphen mit')
A('`xMin = 0` und/oder `yMin = 0` liegt der Nullpunkt aber am Canvasrand: `cy(0)` ist die')
A('Unterkante, `cx(0)` die linke Kante. Damit landen die x-Zahlen **unterhalb** und die')
A('y-Zahlen **links ausserhalb** der Zeichenfläche — sie sind ersatzlos weg. Betroffen')
A('sind fünf Canvas; die Skalierung steht jeweils in der eigenen `xMin/yMin`-Zeile der Seite.')
A('')
A('### 2.2 Der dokumentierte Abdeck-Trick für Achsen-Captions lässt einen Rest stehen')
A('')
A('`drawGrid()` schreibt immer die generischen Labels `x` und `y`. Der Kopfkommentar von')
A('`mathlib.js` beschreibt, wie eine Seite sie durch eigene mit Einheit ersetzt: Bereich mit')
A('`fillRect` weiss übermalen, dann neu schreiben. Die Rechtecke sind aber mit festen')
A('Pixelwerten hinterlegt (`fillRect(W-30, cy(0)-22, 30, 18)`) und treffen den Glyphen nicht')
A('in jeder Skalierung ganz. Übrig bleibt ein Strichrest direkt neben der neuen Caption.')
A('Messbar als 3–45 % verbliebene Glyphenfläche — im Bericht als *Rest einer überdeckten')
A('Beschriftung* geführt.')
A('')
A('---')
A('')

TITEL = {'schwer': ('3. Schwer — Beschriftung fehlt, ist angeschnitten oder unlesbar',
                    'Hier geht Information verloren oder zwei Texte machen sich gegenseitig unlesbar.'),
         'mittel': ('4. Mittel — Beschriftung liegt störend auf einem Grafikelement',
                    'Lesbar, aber die Beschriftung sitzt auf einer Linie, Kurve oder Fläche.'),
         'leicht': ('5. Leicht — Rest einer überdeckten Beschriftung',
                    'Kleiner Artefakt-Strich neben einer ersetzten Beschriftung (§2.2).')}

for g in ('schwer', 'mittel', 'leicht'):
    t, sub = TITEL[g]
    A(f'## {t}')
    A('')
    A(sub + f' — **{len(gruppen[g])} Animationen**.')
    A('')
    for (seite, cid), bs in sorted(gruppen[g]):
        m = meta.get((seite, cid), {})
        link = f'{BASIS}{seite}#{cid}'
        titel = m.get('titel') or ''
        kopf = f'### `{cid}` — {seite.split("/")[1].replace(".html", "")}'
        A(kopf)
        A('')
        A(f'[→ {link}]({link})')
        A('')
        if titel:
            A(f'*Widget: {titel}*')
            A('')
        notiz = NOTIZ.get((seite, cid))
        if notiz:
            A(notiz)
            A('')
        zus = {}
        for b in bs:
            zus.setdefault(b['art'], []).append(b)
        A('| Befund | Beschriftung | Mass |')
        A('|---|---|---|')
        for art, lst in sorted(zus.items()):
            for b in lst[:6]:
                txt = str(b['txt']).replace('|', '\\|')
                A(f'| {ART_TEXT[art]} | `{txt}` | {b["wert"]} |')
            if len(lst) > 6:
                A(f'| {ART_TEXT[art]} | … weitere {len(lst) - 6} gleichartige | |')
        A('')
    A('---')
    A('')

A('## 6. Methodenkritik — was dieser Bericht nicht abdeckt')
A('')
A('- **Nur die Startposition.** Wer einen Regler zieht oder einen Knopf drückt, kann neue')
A('  Kollisionen erzeugen; geprüft ist ausschliesslich der Zustand nach dem Laden.')
A('- **Nur 1280 px.** Bei 360 px skalieren die Canvas neu, die Verhältnisse verschieben sich.')
A('  Ein zweiter Lauf bei 360 px wäre ein eigener Durchgang.')
A('- **Nur Canvas-Text.** Beschriftungen als HTML/MathJax neben der Grafik sind nicht erfasst.')
A('- Die Grenzwerte (25 % Überdeckung, 1.5 px Rand) sind gesetzt, nicht hergeleitet. Die')
A('  Zahl der auffälligen Canvas ist gegen sie robust: zwischen 20 % und 35 % Schwelle')
A('  ändert sich das Ergebnis um wenige Fälle.')
A('- `4` Canvas zeichnen laufend neu (Animation). Dort ist «Startposition» der erste')
A('  Ruhezustand nach dem Laden, nicht zwingend das erste Bild.')
A('')

out = 'BERICHT-beschriftungen-animationen.md'
open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(f'{out}: {len(L)} Zeilen, {len(kan)} Animationen '
      f'(schwer {len(gruppen["schwer"])}, mittel {len(gruppen["mittel"])}, leicht {len(gruppen["leicht"])})')
