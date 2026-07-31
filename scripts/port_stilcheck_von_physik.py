#!/usr/bin/env python3
"""Überträgt das Stilcheck-Regelwerk von TALS Physik nach TALS Mathe.

Vom Mathe-Repo-Root aufrufen. Standard ist ein Trockenlauf — es wird nichts
geschrieben, bis --apply gesetzt ist. Alle Schritte sind idempotent: ein
bereits eingefügter Block wird erkannt und übersprungen.

    python3 scripts/port_stilcheck_von_physik.py docs          # Trockenlauf
    python3 scripts/port_stilcheck_von_physik.py docs --apply
    python3 scripts/port_stilcheck_von_physik.py css --apply
    python3 scripts/port_stilcheck_von_physik.py check         # nur Bericht
    python3 scripts/port_stilcheck_von_physik.py inline        # nur Bericht

Schritte
  docs   STYLEGUIDE.md (§2.1-Ergänzung, §2.5 Preis/Kosten, neues §2.8)
         und CLAUDE.md (Stichwort «Stilcheck» mit Regeltabelle).
  css    style.css: die zwei zentralen Regeln, die Regel 4 überhaupt erst
         möglich machen (overflow-x und der Abstand zwischen Formelzeilen).
         Reine Ergänzung — kein Inline-Stil wird angefasst.
  check  Meldet Verstösse gegen die Regeln 1, 2 und 5. Ändert nichts —
         das Beheben ist redaktionelle Arbeit, kein Suchen-und-Ersetzen.
  inline Inventar der seitenweise definierten .formel-live-Stile. Ändert
         nichts. Grundlage für eine allfällige spätere Zentralisierung —
         siehe die Warnung unten.

Warum die Inline-Stile NICHT automatisch zentralisiert werden:
  Ein Zentralisieren der Mehrheitsvariante ist nicht darstellungsneutral.
  Fünf Seiten setzen .fl-eq bewusst ohne font-style; eine zentrale Regel mit
  font-style:italic würde sie kursivieren, weil CSS eigenschaftsweise mischt
  und die Inline-Regel diese Eigenschaft gar nicht setzt. Getestet und
  verworfen am 28.07.2026. Wer zentralisieren will, entscheidet vorher
  redaktionell, welche Variante gelten soll — das ist keine Skriptarbeit.

NICHT übertragen (bewusst):
  - Live-Box-Spaltenabstand: Mathe hat keine .live-box (siehe
    TODO-port-to-tals-mathe.md §2, dort seit 24.06.2026 korrekt vermerkt).
  - CHANGELOG-Ablösung: gilt nur für Physik. Mathes CHANGELOG.md wird
    weiter gepflegt (ZIP-Snapshot-Rhythmus).
"""
import argparse
import glob
import re
import sys
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════
#  Textbausteine
# ══════════════════════════════════════════════════════════════════════

# --- STYLEGUIDE §2.1: der Multiplikationspunkt ist nie ein Trennzeichen ---
MARKE_21 = 'Der Multiplikationspunkt ist nie ein Trennzeichen'
ANKER_21 = '### 2.2 Funktionsschreibweise'
BLOCK_21 = """**Der Multiplikationspunkt ist nie ein Trennzeichen** (verbindlich, Stichwort
«Stilcheck»). In Rechen- und Wertanzeigen — `.fl-eq`, Canvas-Beschriftungen,
Live-Ausgaben — bedeutet `·` ausschliesslich «mal». Wo zwei Angaben nebeneinander
stehen, trennt Leerraum, ein Gedankenstrich «—» oder eine zweite Zeile:

- `12:30   4.5 °C` ✓, `12:30 · 4.5 °C` ✗
- Zwei Gleichungen sind **zwei** `.fl-eq`-Zeilen, nicht eine Zeile mit «|» oder «·».

**Ausgenommen** sind Titel und Breadcrumbs («Animation 3 · Parabeln»), wo der Punkt
seit jeher als Gliederungszeichen dient.

"""

# --- STYLEGUIDE §2.5: Preis vs. Kosten ---
MARKE_25 = '«Preis» erscheint nie mit der Einheit CHF'
ANKER_25 = '| CHF (Währung) | Fr. |'
BLOCK_25 = """| Preis \\(p\\) — Kosten **pro Einheit** (CHF/kg, CHF/km) | «Preis» für einen Gesamtbetrag |
| Kosten \\(K\\) — der **Gesamtbetrag** (CHF) | «Kosten» für einen Stückpreis |"""
BLOCK_25_TEXT = """
**«Preis» erscheint nie mit der Einheit CHF** (verbindlich, Stichwort «Stilcheck»).
Wo ein Franken-Betrag steht, heisst die Grösse **Kosten**; der Preis ist die
Steigung, also der Betrag *pro Einheit*. Es gilt \\(K = m \\cdot p\\) und
\\(p = K/m\\). Achsenlabel darum `Kosten K [CHF]`, nie `Preis [CHF]`.
Betrifft alle Anwendungsaufgaben — Sachrechnen, Proportionalität, lineare
Funktionen, Steigungsdeutung.
"""

# --- STYLEGUIDE: neues §2.8 vor Kapitel 3 ---
MARKE_28 = '### 2.8 Live-Anzeigen in Widgets'
ANKER_28 = '## 3. Achsenskalierung (verbindlich)'
BLOCK_28 = """### 2.8 Live-Anzeigen in Widgets (verbindlich, Stichwort «Stilcheck»)

Übernommen aus TALS Physik (dort §2.1, §2.7, §2.8), an die Mathe-Konventionen
angepasst. Diese Regeln entstanden als Einzelbefunde an konkreten Animationen —
sie werden gebrochen, sobald jemand eine Anzeige *ergänzt*, ohne die ganze
Anzeige noch einmal anzusehen. Darum das Stichwort.

**(a) Ansatz vor Werten.** Jede `.formel-live` nennt zuerst die Formel symbolisch,
dann erst die Zahlen — entweder als zwei `.fl-eq`-Zeilen oder in einer Zeile
(`A = a · b = 3 · 4 = 12`). Beim Stichwort «Stilcheck» wird das auf der **ganzen
Seite** geprüft, nicht nur an der berührten Animation.

**(b) Einheiten beim Einsetzen.** Nur in Anwendungsaufgaben — reine Algebra hat
keine Einheiten:

- `K = 2.5 kg · 3.20 CHF/kg = 8.00 CHF` ✓
- `K = 2.5 · 3.20 = 8.00 CHF` ✗

Das Mitführen der Einheit ist die einzige Selbstkontrolle beim Einsetzen.

**Sonderfall Skalen- und Einheitenumrechnung,** wo die Einheit nicht mitgeführt
werden *kann*, weil die Gleichung Zahlenwerte zweier Skalen verknüpft: Einheit in
eckigen Klammern an die **Grösse**, nicht an die Zahl.

- `v [m/s] = v [km/h] / 3.6 = 108 / 3.6 = 30.0` ✓
- `v = 108 km/h / 3.6 = 30.0 m/s` ✗ (die 3.6 trägt versteckt eine Einheit)

Echte **Differenzen** sind davon nicht betroffen — dort wird normal mit Einheit
eingesetzt.

**(c) Brüche als Brüche.** Wo die Anzeige LaTeX verwendet, gehören Brüche als
`\\frac{…}{…}` gesetzt, nicht als `a/b` — und zwar in **beiden** Zeilen, Formel
*und* Zahlengleichung. Mehrstufige Umformungen kommen auf getrennte Zeilen, nie
als Inline-`⇒`-Kette.

Wird die Formel bei jedem Reglerschritt neu gerendert, muss der MathJax-Aufruf
**gedrosselt und serialisiert** werden (ein `requestAnimationFrame`-Fenster plus
eine Promise-Kette), sonst überholen sich die Aufrufe und die Anzeige flackert
oder bleibt leer. Dabei auf **doppelte Backslashes** in JS-Strings achten:

    const kg = v => v.toFixed(1) + '\\\\;\\\\text{kg}';   // richtig
    const kg = v => v.toFixed(1) + '\\;\\text{kg}';     // falsch — JS schluckt den Backslash

Der zweite Fall erzeugt `;text{kg}` und fällt erst im Browser auf.

**(d) Mehrzeilige Anzeigen.** `.formel-live` scrollt bei Überlänge horizontal
(`overflow-x:auto`), Folgezeilen haben 6 px Abstand. Beides liegt **zentral in
`style.css`** — nicht pro Seite nachbauen. Bricht eine Zeile auf 360 px mitten im
Term um, wird die Rechnung auf zwei `.fl-eq`-Zeilen aufgeteilt (Ansatz, dann
Werte), nicht die Schrift verkleinert.

---

"""

# --- CLAUDE.md: Stichwort «Stilcheck» ---
MARKE_CLAUDE = 'Stichwort «Stilcheck»'
ANKER_CLAUDE = '## Verifikations-Standard'
BLOCK_CLAUDE = """## Stichwort «Stilcheck»

Nennt der Auftraggeber im Prompt **„Stilcheck"**, dann gilt zusätzlich zum
eigentlichen Auftrag: **alle gesammelten Darstellungsregeln an den berührten
Stellen prüfen und korrigieren** — nicht nur die neu geschriebenen Zeilen,
sondern die ganze Animation / den ganzen Abschnitt, an dem gearbeitet wird.

Die Liste steht in `STYLEGUIDE.md` und wächst; aktuell:

| # | Regel | STYLEGUIDE |
|---|---|---|
| 1 | In Rechen-/Wertanzeigen (`.fl-eq`, Canvas-Zahlen) heisst `·` nur Multiplikation, nie Trennzeichen. Zwei Gleichungen = zwei `.fl-eq`-Zeilen. Titel/Breadcrumbs sind ausgenommen. | §2.1 |
| 2 | **Jede** `.fl-eq` nennt zuerst die Formel symbolisch, dann die Werte — auf der ganzen Seite prüfen, nicht nur an der geänderten Animation. | §2.8 (a) |
| 3 | Werte werden **mit Einheit** eingesetzt (Anwendungsaufgaben). Wo die Einheit nicht mitgeführt werden kann, steht sie in eckigen Klammern an der Grösse. | §2.8 (b) |
| 4 | Formelzeilen **komplett** in LaTeX — Formel *und* Zahlengleichung, Brüche als `\\frac{…}{…}`. Dynamisches Neu-Rendern gedrosselt und serialisiert; auf doppelte Backslashes in JS-Strings achten. | §2.8 (c) |
| 5 | **Preis** = Kosten pro Einheit (CHF/kg, CHF/km); **Kosten** = Gesamtbetrag (CHF). «Preis» nie mit der Einheit CHF — weder im Text noch an Achsen oder in Live-Boxen. | §2.5 |

Neue Regeln, die der Auftraggeber ansagt, werden in STYLEGUIDE.md aufgenommen
**und** hier in der Tabelle nachgeführt.

> Herkunft: TALS Physik, Sessions vom 26./27.07.2026. Physik führt dort eine
> sechste Regel zum Spaltenabstand der `.live-box` — die entfällt hier, weil
> Mathe keine `.live-box`-Struktur hat (siehe `TODO-port-to-tals-mathe.md` §2).

"""

# --- style.css: die zwei zentralen Regeln (Regel 4 / §2.8 d) ---
MARKE_CSS = 'Stilcheck §2.8 (d)'
BLOCK_CSS = """
/* ── Live-Formelanzeigen: mehrzeilig und überlaufsicher ──────────────────
   Stilcheck §2.8 (d). Greift auch dort, wo eine Seite .formel-live inline
   überschreibt — die Inline-Blöcke setzen keine dieser beiden Eigenschaften. */
.formel-live { overflow-x:auto; }
.formel-live .fl-eq + .fl-eq { margin-top:6px; }
"""

SEITEN = sorted(glob.glob('grundlagen/*.html')) + sorted(glob.glob('schwerpunkt/*.html'))


# ══════════════════════════════════════════════════════════════════════
#  Hilfen
# ══════════════════════════════════════════════════════════════════════

class Aenderung:
    def __init__(self):
        self.puffer = {}
        self.notizen = []

    def lies(self, pfad):
        if pfad in self.puffer:
            return self.puffer[pfad]
        return Path(pfad).read_text(encoding='utf-8')

    def setze(self, pfad, text, notiz):
        self.puffer[pfad] = text
        self.notizen.append(notiz)

    def schreibe(self, apply):
        for pfad, text in self.puffer.items():
            if apply:
                Path(pfad).write_text(text, encoding='utf-8')
        return len(self.puffer)


def pruefe_repo():
    fehlt = [f for f in ('STYLEGUIDE.md', 'CLAUDE.md', 'style.css') if not Path(f).exists()]
    if fehlt:
        sys.exit('FEHLER: %s nicht gefunden — vom Mathe-Repo-Root aufrufen.' % ', '.join(fehlt))
    if Path('physiklib.js').exists():
        sys.exit('FEHLER: das sieht nach dem Physik-Repo aus. Dieses Skript gehört ins Mathe-Repo.')


def einfuegen_vor(text, anker, block, was):
    """Fügt block unmittelbar vor der ersten Zeile ein, die anker enthält."""
    i = text.find(anker)
    if i < 0:
        raise LookupError('Anker nicht gefunden für %s: %r' % (was, anker))
    return text[:i] + block + text[i:]


# ══════════════════════════════════════════════════════════════════════
#  Schritt: docs
# ══════════════════════════════════════════════════════════════════════

def schritt_docs(ae):
    sg = ae.lies('STYLEGUIDE.md')

    if MARKE_21 in sg:
        ae.notizen.append('STYLEGUIDE §2.1  übersprungen (schon vorhanden)')
    else:
        sg = einfuegen_vor(sg, ANKER_21, BLOCK_21, '§2.1-Ergänzung')
        ae.notizen.append('STYLEGUIDE §2.1  Multiplikationspunkt ist kein Trennzeichen (+%d Zeilen)'
                          % BLOCK_21.count('\n'))

    if MARKE_25 in sg:
        ae.notizen.append('STYLEGUIDE §2.5  übersprungen (schon vorhanden)')
    else:
        if ANKER_25 not in sg:
            raise LookupError('Anker nicht gefunden für §2.5: %r' % ANKER_25)
        # Tabellenzeilen direkt nach der CHF-Zeile, Fliesstext ans Ende der Tabelle
        sg = sg.replace(ANKER_25, ANKER_25 + '\n' + BLOCK_25, 1)
        i = sg.index(BLOCK_25) + len(BLOCK_25)
        j = sg.index('\n\n', i)
        sg = sg[:j] + '\n' + BLOCK_25_TEXT + sg[j:]
        ae.notizen.append('STYLEGUIDE §2.5  Preis/Kosten (2 Tabellenzeilen + Erläuterung)')

    if MARKE_28 in sg:
        ae.notizen.append('STYLEGUIDE §2.8  übersprungen (schon vorhanden)')
    else:
        sg = einfuegen_vor(sg, ANKER_28, BLOCK_28, '§2.8')
        ae.notizen.append('STYLEGUIDE §2.8  Live-Anzeigen in Widgets, neu (+%d Zeilen)'
                          % BLOCK_28.count('\n'))

    if sg != ae.lies('STYLEGUIDE.md'):
        ae.setze('STYLEGUIDE.md', sg, None)

    cl = ae.lies('CLAUDE.md')
    if MARKE_CLAUDE in cl:
        ae.notizen.append('CLAUDE.md        übersprungen (Stilcheck schon vorhanden)')
    else:
        cl = einfuegen_vor(cl, ANKER_CLAUDE, BLOCK_CLAUDE, 'Stilcheck-Abschnitt')
        ae.setze('CLAUDE.md', cl, 'CLAUDE.md        Stichwort «Stilcheck» + Regeltabelle (5 Regeln)')

    ae.notizen = [n for n in ae.notizen if n]


# ══════════════════════════════════════════════════════════════════════
#  Schritt: css
# ══════════════════════════════════════════════════════════════════════

def schritt_css(ae):
    css = ae.lies('style.css')
    if MARKE_CSS in css:
        ae.notizen.append('style.css        übersprungen (§2.8-d-Regeln schon vorhanden)')
        return
    ae.setze('style.css', css.rstrip('\n') + '\n' + BLOCK_CSS,
             'style.css        overflow-x:auto + 6 px zwischen Formelzeilen')
    n_bl = sum(len(re.findall(r'</div>\s*<div class="fl-eq"', Path(f).read_text(encoding='utf-8')))
               for f in SEITEN)
    ae.notizen.append('                 betrifft sichtbar %d mehrzeilige Anzeigen — '
                      'danach Render-Check!' % n_bl)


# ══════════════════════════════════════════════════════════════════════
#  Schritt: check  (nur Bericht)
# ══════════════════════════════════════════════════════════════════════

def schritt_check():
    # Regel 1: «·» als Trenner in JS-Strings — Multiplikation hat rechts eine
    # Zahl/Variable/Klammer, ein Trenner hat rechts ein Leerzeichen + Grossbuchstabe
    # oder eine Einheit. Heuristik, darum als Verdacht ausgewiesen.
    trenner = re.compile(r"'[^'\n]*\S\s+·\s+[A-ZÄÖÜ][^'\n]*'")
    # Regel 5: «Preis» in unmittelbarer Nähe von CHF ohne Nenner
    preis_chf = re.compile(r'Preis[^.<\n]{0,40}\bCHF\b(?!\s*/)')
    # Regel 2: fl-eq mit Zahlengleichung, ohne dass eine Formelzeile davor steht
    fl_eq = re.compile(r'<div class="fl-eq"[^>]*>([^<]{1,90})</div>')

    treffer = {'trenner': [], 'preis': [], 'ansatz': []}
    for f in SEITEN:
        s = Path(f).read_text(encoding='utf-8')
        for m in trenner.finditer(s):
            treffer['trenner'].append((f, m.group(0)[:78]))
        for m in preis_chf.finditer(s):
            treffer['preis'].append((f, m.group(0)[:78]))
        # Ansatz-Prinzip: Blöcke mit genau einer fl-eq, die ein «=» und eine Ziffer trägt
        for blk in re.finditer(r'<div class="formel-live">(.*?)</div>\s*</div>', s, re.S):
            eqs = fl_eq.findall(blk.group(1))
            if len(eqs) == 1 and '=' in eqs[0] and re.search(r'\d', eqs[0]):
                links = eqs[0].split('=')[0]
                # Formel benannt, wenn links vom ersten «=» keine Ziffer steht und
                # rechts davon mindestens zwei «=» folgen (Formel = Werte = Ergebnis)
                if eqs[0].count('=') < 2 and not re.search(r'[a-zA-Zα-ω]\s*\(', links):
                    treffer['ansatz'].append((f, eqs[0][:78]))

    def zeig(titel, regel, eintraege):
        print('\n── %s  (Regel %s) ──' % (titel, regel))
        if not eintraege:
            print('   keine Befunde')
            return
        for f, t in eintraege[:40]:
            print('   %-46s %s' % (f, t))
        if len(eintraege) > 40:
            print('   … und %d weitere' % (len(eintraege) - 40))

    zeig('«·» vermutlich als Trennzeichen', 1, treffer['trenner'])
    zeig('«Preis» mit der Einheit CHF', 5, treffer['preis'])
    zeig('Zahlengleichung ohne benannte Formel', 2, treffer['ansatz'])
    print('\nAlle drei Listen sind Heuristiken — jeder Treffer will von Hand angesehen')
    print('werden. Das Beheben ist redaktionelle Arbeit, kein Suchen-und-Ersetzen.')


# ══════════════════════════════════════════════════════════════════════
#  Schritt: inline  (nur Bericht)
# ══════════════════════════════════════════════════════════════════════

def schritt_inline():
    import collections
    sel = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in SEITEN:
        s = Path(f).read_text(encoding='utf-8')
        for m in re.finditer(r'^(\.formel-live[^\{\n]*)\{([^}]*)\}\s*$', s, re.M):
            sel[m.group(1).strip()][re.sub(r'\s+', ' ', m.group(2)).strip()].append(f)
    for k in sorted(sel):
        varianten = sorted(sel[k].items(), key=lambda kv: -len(kv[1]))
        print('\n## %s   — %d Variante(n)' % (k, len(varianten)))
        for i, (decl, files) in enumerate(varianten):
            kopf = 'Mehrheit' if i == 0 else 'abweichend'
            print('   [%s, %dx] %s' % (kopf, len(files), decl[:96]))
            if i:
                for f in files:
                    print('        %s' % f)
    print('\nZentralisieren ist NICHT darstellungsneutral, solange Varianten sich in')
    print('gesetzten *und* fehlenden Eigenschaften unterscheiden (z.B. font-style).')
    print('Erst redaktionell entscheiden, welche Variante gelten soll.')


# ══════════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('schritt', choices=['docs', 'css', 'check', 'inline', 'all'])
    p.add_argument('--apply', action='store_true', help='wirklich schreiben (sonst Trockenlauf)')
    a = p.parse_args()

    pruefe_repo()

    if a.schritt == 'check':
        schritt_check()
        return
    if a.schritt == 'inline':
        schritt_inline()
        return

    ae = Aenderung()
    try:
        if a.schritt in ('docs', 'all'):
            schritt_docs(ae)
        if a.schritt in ('css', 'all'):
            schritt_css(ae)
    except LookupError as e:
        sys.exit('FEHLER: %s\nDie Datei wurde seit dem 28.07.2026 geändert — Anker im '
                 'Skript nachziehen, nichts geschrieben.' % e)

    print('\n'.join('  ' + n for n in ae.notizen) or '  nichts zu tun')
    n = ae.schreibe(a.apply)
    print('\n%s: %d Datei(en)%s' % ('GESCHRIEBEN' if a.apply else 'TROCKENLAUF', n,
                                    '' if a.apply else ' — mit --apply wirklich schreiben'))
    if a.apply and n:
        print('\nNächste Schritte:')
        print('  1. git diff ansehen')
        print('  2. python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html')
        print('  3. node .claude/tools/screenshot-widgets.mjs   (Render-Check 1280 + 360 px)')
        print('  4. python3 scripts/port_stilcheck_von_physik.py check   (Befundliste)')


if __name__ == '__main__':
    main()
