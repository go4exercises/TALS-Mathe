#!/usr/bin/env python3
"""Erzeugt index-test-zweispaltig.html aus index.html.

Drei Änderungen gegenüber der Produktivseite:
  1. Bereichskopf nur noch „Grundlagenfach" / „Schwerpunktfach" (Badge + langer
     Titel raus), dadurch flacher.
  2. Die beiden Bereiche stehen nebeneinander statt untereinander.
  3. In der Kapitelzeile wandert die Lektionsangabe von rechts nach links unter
     den Titel; die Zeilenhöhe bleibt über kleinere Polsterung fast gleich.

Der Kapitelinhalt (Karten, Sub-Splits) wird unverändert übernommen — er wird
nur umgehängt, nicht neu geschrieben.
"""
import re
import sys

QUELLE = 'index.html'
ZIEL = 'index-test-zweispaltig.html'

s = open(QUELLE, encoding='utf-8').read()


def ersetze(alt, neu, wie_oft=1):
    global s
    n = s.count(alt)
    if n != wie_oft:
        sys.exit('[FEHLER] %d × statt %d gefunden: %s' % (n, wie_oft, alt[:90]))
    s = s.replace(alt, neu)


# ── 1. Kennzeichnung als Testversion ─────────────────────────────
ersetze('<title>TALS Mathematik — RLP 2030</title>',
        '<title>TESTVERSION zweispaltig — TALS Mathematik</title>')

# ── 2. Bereichskopf: nur ein Wort, flacher ───────────────────────
ersetze('.bereich { margin-top: 40px; padding: 17px 20px 15px;',
        '.bereich { margin-top: 40px; padding: 11px 18px 10px;')
ersetze('.b-titel { font-family: var(--serif); font-size: 1.18rem; font-weight: 700; }',
        '.b-titel { font-family: var(--serif); font-size: 1.06rem; font-weight: 700; }')

for bereich, wort in [('b-gl', 'Grundlagenfach'), ('b-sp', 'Schwerpunktfach')]:
    alt = re.search(r'<div class="bereich %s" id="\w+">\s*<div class="bh">.*?</div>\s*</div>'
                    % bereich, s, re.S)
    if not alt:
        sys.exit('[FEHLER] Bereichskopf %s nicht gefunden' % bereich)
    kopf = alt.group(0)
    neu = re.sub(r'<div class="bh">.*?</div>\s*(?=</div>)',
                 '<div class="bh">\n      <span class="b-titel">%s</span>\n    </div>\n  ' % wort,
                 kopf, flags=re.S)
    s = s.replace(kopf, neu, 1)

# ── 3. Kapitelzeile: Lektionsangabe unter den Titel ──────────────
# Markup: .k-name + .k-lek in einen .k-txt-Block einpacken.
vorher = len(re.findall(r'<span class="k-name">', s))
s = re.sub(
    r'(\s*)<span class="k-name">(.*?)</span>\s*<span class="k-lek">(.*?)</span>',
    lambda m: ('%s<span class="k-txt">'
               '%s  <span class="k-name">%s</span>'
               '%s  <span class="k-lek">%s</span>'
               '%s</span>') % (m.group(1), m.group(1), m.group(2),
                               m.group(1), m.group(3), m.group(1)),
    s, flags=re.S)
nachher = len(re.findall(r'<span class="k-txt">', s))
if vorher != nachher or vorher != 9:
    sys.exit('[FEHLER] k-txt: %d Kapitelzeilen umgebaut, erwartet 9' % nachher)

# ── 4. Die beiden Bereiche nebeneinander ─────────────────────────
i_gl = s.index('  <div class="bereich b-gl" id="gl">')
i_sp = s.index('  <!-- ═')
i_sp = s.index('  <!-- ═', s.index('id="sp"') - 400)   # Kommentarblock vor #sp
i_ds = s.index('  <div class="ds">')

spalte_gl = s[i_gl:i_sp].rstrip()
spalte_sp = s[i_sp:i_ds].rstrip()

neu_block = (
    '  <div class="spalten">\n'
    '    <div class="spalte">\n'
    + spalte_gl + '\n'
    '    </div>\n'
    '    <div class="spalte">\n'
    + spalte_sp + '\n'
    '    </div>\n'
    '  </div>\n\n'
)
s = s[:i_gl] + neu_block + s[i_ds:]

# ── 5. CSS für das Zweispalten-Layout ────────────────────────────
CSS = """
  /* ══════════════════════════════════════════════════════════════
     TESTVERSION — Bereiche nebeneinander
     Nur diese Datei. Produktive index.html ist unberührt.
     ══════════════════════════════════════════════════════════════ */
  .spalten { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }
  /* Kein Trenner-Abstand über dem Bereichskopf: er ist erstes Element seiner Spalte.
     Ersetzt die Regel `.page > .bereich:first-child` der Produktivseite. */
  .spalte > .bereich { margin-top: 0; }

  /* Kapitelzeile: Lektionsangabe links unter dem Titel statt rechts aussen.
     Polsterung 12 -> 9px und knappe line-heights halten die Zeilenhöhe fast
     auf dem alten Wert, obwohl jetzt zwei Textzeilen darin stehen. */
  .kap-hdr { padding: 9px 16px; align-items: center; gap: 10px; }
  .k-txt   { display: flex; flex-direction: column; gap: 1px; min-width: 0; flex: 1; }
  .k-name  { line-height: 1.2; }
  .k-lek   { margin-left: 0; font-size: 0.6rem; line-height: 1.25; white-space: normal; }

  /* Die §9-Regel richtet .k-lek unter 600px rechts aus — richtig, solange die Angabe
     am rechten Zeilenende sitzt. Hier steht sie unter dem Titel und muss mit ihm
     linksbündig sein. Dasselbe gilt für das dortige align-items/padding-Gefummel. */
  @media (max-width: 600px) {
    .kap-hdr { align-items: center; }
    .k-lek   { text-align: left; }
    .k-nr, .k-name { padding-top: 0; }
  }

  /* Halbe Breite: Karten in 2 Spalten, Sub-Split-Container nie breiter als 2.
     Ohne das würde `span-3`/`span-4` im schmalen Spaltengrid gestaucht. */
  .spalte .tc { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); padding: 12px; }
  .spalte .ksub.span-3, .spalte .ksub.span-4 { grid-column: span 2; }
  .spalte .ksub.span-3 .ksub-grid,
  .spalte .ksub.span-4 .ksub-grid { grid-template-columns: repeat(2, 1fr); }

  /* Unter 900px lohnt das Nebeneinander nicht mehr — zurück auf untereinander,
     mit dem Trenner-Abstand über dem zweiten Bereich. */
  @media (max-width: 900px) {
    .spalten { grid-template-columns: 1fr; gap: 0; }
    .spalte + .spalte > .bereich { margin-top: 40px; }
  }
"""
ersetze('\n</style>', CSS + '</style>')

open(ZIEL, 'w', encoding='utf-8').write(s)
print('%s geschrieben (%d Zeichen)' % (ZIEL, len(s)))
print('  div-Bilanz:', s.count('<div') == s.count('</div>'),
      '| span-Bilanz:', s.count('<span') == s.count('</span>'),
      '| kein ß:', 'ß' not in s)
