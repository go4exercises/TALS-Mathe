#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Druckseiten-Generator für Lerngebiet s3 (Schwerpunkt Funktionen).
Analog zu build_print_g4.py: HTML-Skelett als Template, Inhalte als
Triple-Quoted-Strings, Generation in einer Schleife.

Erzeugt je Themenseite vier Druckseiten unter
downloads/schwerpunkt/<slug>/{handout,formelauszug,teste-dich-selbst,aufgabenserie}.html

Aufruf vom Repo-Root:  python3 scripts/build_print_s3.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = r'''<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{rolle} · {thema} — TALS Mathematik</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../print.css">
{extra_style}<script>
MathJax = {{
  tex: {{ inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']] }},
  svg: {{ fontCache: 'global', scale: {scale} }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea'] }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>

<div class="druck-bar no-print">
  <a class="db-back" href="../../../schwerpunkt/{slug}.html#downloads">← zurück zur Themenseite</a>
  <span class="db-info">{rolle} · A4 · Bereit zum Drucken</span>
  <button class="db-print" onclick="window.print()">Seite drucken</button>
</div>

<div class="druck-wrapper">

  <header class="doc-kopf">
    <div class="dk-bereich">TALS Mathematik · Schwerpunktfach · {thema}</div>
    <h1>{h1}</h1>
{quelle}  </header>

'''

FOOT = r'''
  <footer class="doc-fuss">
    <span>TALS Mathematik · Schwerpunkt {thema}</span>
    <span>{rolle}</span>
  </footer>

</div>
</body>
</html>
'''

STYLE_FORMELAUSZUG = r'''<style>
  body { font-size: 10pt; }
  .druck-wrapper h2 { font-size: 12pt; margin-top: 4mm; }
  .druck-wrapper p { margin: 0 0 1.5mm; font-size: 9.5pt; }
  .druck-wrapper table.ftb-tabelle { font-size: 9.2pt; margin: 2mm 0; }
  .druck-wrapper table.ftb-tabelle th,
  .druck-wrapper table.ftb-tabelle td { padding: 1.2mm 2mm; }
  .quelle { font-size: 8.8pt; color: var(--tinte-2); font-style: italic; margin-top: 1mm; }
</style>
'''

STYLE_TDS = r'''<style>
  .aufg-rahmen { border: 1pt solid var(--linie); border-radius: 4px; padding: 4mm; margin: 3mm 0;
                 page-break-inside: avoid; break-inside: avoid; }
  .aufg-rahmen .aufg-kopf { margin-bottom: 2mm; }
  .schwierig { font-family: var(--mono); font-size: 8pt; color: var(--tinte-2); margin-left: auto; letter-spacing: 0.5px; }
  .schwierig .punkt { color: var(--blau); font-size: 9pt; }
  .schwierig .punkt-leer { color: var(--linie); font-size: 9pt; }
  .lueckentext { font-family: var(--mono); font-size: 10pt; line-height: 1.9; background: var(--papier-2);
                 padding: 3mm 4mm; border-radius: 3px; border: 1px dashed var(--linie); }
  .lueckentext .lueck { display: inline-block; border-bottom: 0.8pt solid var(--tinte); min-width: 35mm; height: 1.2em; }
  .gruppe-titel { font-family: var(--serif); font-size: 11pt; font-weight: 700; color: var(--tinte);
                  margin: 5mm 0 2mm; padding-bottom: 1mm; border-bottom: 0.6pt solid var(--linie);
                  page-break-after: avoid; break-after: avoid; }
  .lin-mehr { margin-bottom: 2mm; }
  .lin-mehr .lin { height: 7mm; }
</style>
'''

STYLE_SERIE = r'''<style>
  .aufg-rahmen { border: 1pt solid var(--linie); border-radius: 4px; padding: 4mm; margin: 3mm 0;
                 page-break-inside: avoid; break-inside: avoid; }
  .aufg-rahmen .aufg-kopf { margin-bottom: 2mm; align-items: baseline; }
  .schwierig { font-family: var(--mono); font-size: 8pt; color: var(--tinte-2); margin-left: auto; letter-spacing: 0.5px; }
  .schwierig .punkt { color: var(--blau); font-size: 9pt; }
  .schwierig .punkt-leer { color: var(--linie); font-size: 9pt; }
  .bereich-tag { font-family: var(--mono); font-size: 7.5pt; color: var(--blau); background: var(--blau-hell);
                 padding: 0.5mm 2mm; border-radius: 3px; text-transform: uppercase; letter-spacing: 1px; margin-left: 3mm; }
  .lin-mehr { margin-bottom: 2mm; }
  .lin-mehr .lin { height: 7mm; }
  .uebersicht { width: 100%; border-collapse: collapse; font-size: 9.2pt; margin: 3mm 0 5mm; }
  .uebersicht th, .uebersicht td { border: 1px solid var(--linie); padding: 1.4mm 2.5mm; text-align: left; }
  .uebersicht th { background: var(--papier-2); font-family: var(--sans); font-weight: 700; font-size: 9pt; }
  .uebersicht td.nr { text-align: center; font-family: var(--mono); width: 10mm; }
  .uebersicht td.s  { text-align: center; font-family: var(--mono); width: 18mm; color: var(--orange); letter-spacing: 1px; }
</style>
'''

LINS = '<div class="lin-mehr">' + '<div class="lin"></div>' * 3 + '</div>'
LINS4 = '<div class="lin-mehr">' + '<div class="lin"></div>' * 4 + '</div>'


def aufg(nr, titel, dots, body, tag=None):
    """Aufgaben-Rahmen für teste-dich-selbst (tag=None) und aufgabenserie."""
    punkte = ''.join(f'<span class="punkt{"" if i < dots else "-leer"}">●</span>' for i in range(3))
    tag_html = f'<span class="bereich-tag">{tag}</span>' if tag else ''
    pre = '△ ' if tag is None else ''
    return f'''  <div class="aufg-rahmen">
    <div class="aufg-kopf">
      <span class="aufg-nr">{pre}{nr}</span>
      <span class="aufg-titel">{titel}</span>{tag_html}
      <span class="schwierig">{punkte}</span>
    </div>
{body}
  </div>
'''


def loes(nr, body):
    return f'''  <div class="loes">
    <div class="loes-titel">✓ Lösung {nr}</div>
{body}
  </div>
'''


# ═══════════════════════════════════════════════════════════════════
#  s3-2a  POTENZFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

A_HANDOUT = r'''
  <h2>1. Definition</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Potenzfunktion</div>
    <p>Eine Funktion \( f : \mathbb{R} \longrightarrow \mathbb{R} \) mit einer Gleichung der Form</p>
    \[ y = f(x) = a \cdot x^n, \qquad n \in \mathbb{Z} \setminus \{0\},\quad a \in \mathbb{R} \setminus \{0\} \]
    <p>heisst <strong>Potenzfunktion</strong>.</p>
  </div>

  <p><strong>Spezialfälle des Exponenten:</strong> \(n = 0\) ergäbe die konstante Funktion \(y = 1\) —
  sie zählt <strong>nicht</strong> zu den Potenzfunktionen. \(n = 1\) ergibt die lineare Funktion
  \(y = x\) — sie zählt dazu.</p>

  <h2>2. Gerade und ungerade Funktionen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Begriff</th><th>Bedingung</th><th>Symmetrie des Graphen</th></tr></thead>
    <tbody>
      <tr><td class="li">gerade Funktion</td><td>\( f(-x) = f(x) \)</td><td class="li">Achsensymmetrie zur \(y\)-Achse</td></tr>
      <tr><td class="li">ungerade Funktion</td><td>\( f(-x) = -f(x) \)</td><td class="li">Punktsymmetrie zum Ursprung</td></tr>
    </tbody>
  </table>
  <p>Bei Potenzfunktionen entscheidet die <strong>Parität des Exponenten</strong>: gerades \(n\) →
  gerade Funktion, ungerades \(n\) → ungerade Funktion.</p>

  <h2>3. Parabeln n-ter Ordnung (\(n \in \mathbb{N}^*\))</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaften</th><th>\( y = x^{2n-1} \) (ungerade)</th><th>\( y = x^{2n} \) (gerade)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td>\( D = \mathbb{R} \)</td><td>\( D = \mathbb{R} \)</td></tr>
      <tr><td class="li">Wertemenge</td><td>\( W = \mathbb{R} \)</td><td>\( W = \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Gemeinsame Punkte</td><td>\( (0 \mid 0),\, (1 \mid 1),\, (-1 \mid -1) \)</td><td>\( (0 \mid 0),\, (1 \mid 1),\, (-1 \mid 1) \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>\( x_0 = 0 \)</td><td>\( x_0 = 0 \)</td></tr>
      <tr><td class="li">Symmetrie</td><td class="li">punktsymmetrisch (ungerade)</td><td class="li">achsensymmetrisch (gerade)</td></tr>
    </tbody>
  </table>
  <p>Der Punkt \( S = (0 \mid 0) \) heisst bei ungeraden Exponenten (\(n \geq 3\)) <strong>Terrassenpunkt</strong>,
  bei geraden Exponenten <strong>Flachpunkt</strong>.</p>

  <h2>4. Hyperbeln n-ter Ordnung (\(n \in \mathbb{Z}^-\))</h2>
  <p>Schreibweise als Bruch: \( y = x^{-n} = \dfrac{1}{x^n} \) mit \( n \in \mathbb{N}^* \).</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaften</th><th>\( y = \dfrac{1}{x^{2n-1}} \) (ungerade)</th><th>\( y = \dfrac{1}{x^{2n}} \) (gerade)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td>\( D = \mathbb{R} \setminus \{0\} \)</td><td>\( D = \mathbb{R} \setminus \{0\} \)</td></tr>
      <tr><td class="li">Wertemenge</td><td>\( W = \mathbb{R} \setminus \{0\} \)</td><td>\( W = \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">Gemeinsame Punkte</td><td>\( (1 \mid 1),\, (-1 \mid -1) \)</td><td>\( (1 \mid 1),\, (-1 \mid 1) \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>—</td><td>—</td></tr>
      <tr><td class="li">Asymptoten</td><td>\( x = 0;\; y = 0 \)</td><td>\( x = 0;\; y = 0 \)</td></tr>
    </tbody>
  </table>

  <h2>5. Asymptoten</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Horizontale Asymptote</div>
    <p>Eine Gerade, an die sich der Graph mit wachsender Entfernung vom Ursprung <strong>in
    \(x\)-Richtung</strong> immer mehr annähert, ohne sie zu schneiden.</p>
  </div>
  <div class="block block-def">
    <div class="block-titel">📘 Vertikale Asymptote</div>
    <p>Eine Gerade, an die sich der Graph mit wachsender Entfernung vom Ursprung <strong>in
    \(y\)-Richtung</strong> immer mehr annähert, ohne sie zu schneiden. Die Definitionslücke \(x_0\)
    heisst <strong>Polstelle</strong> (Pol), die Gerade \( x = x_0 \) <strong>Polgerade</strong>.</p>
  </div>

  <h2>6. Transformationen</h2>
  <p>Ausgangsfunktion \( y = x^n \), Bildfunktion \( y = a \cdot (x-u)^n + v \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung (nach rechts für \(u > 0\))</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung (nach oben für \(v > 0\))</td></tr>
      <tr><td>\(|a|\)</td><td class="li">Streckung (\(|a| > 1\)) bzw. Stauchung (\(|a| < 1\)) in \(y\)-Richtung</td></tr>
      <tr><td>\(a < 0\)</td><td class="li">zusätzlich Spiegelung an der \(x\)-Achse</td></tr>
    </tbody>
  </table>
  <p>Bei verschobenen Hyperbeln wandern die Asymptoten mit: Polgerade \( x = u \), horizontale
  Asymptote \( y = v \).</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Der Exponent \(n\) bestimmt die <strong>Grundform</strong> (Parabel für \(n > 0\), Hyperbel für
    \(n < 0\)), seine <strong>Parität</strong> die Symmetrie. Die Parameter \(a\), \(u\), \(v\)
    strecken, spiegeln und verschieben die Grundform.</p>
  </div>
'''

A_FORMELAUSZUG = r'''
  <h2>1. Definition</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Potenzfunktion</td>
          <td>\( y = f(x) = a \cdot x^n, \quad n \in \mathbb{Z} \setminus \{0\},\; a \in \mathbb{R} \setminus \{0\} \)</td></tr>
      <tr><td class="li">Bruch-Schreibweise</td>
          <td>\( x^{-n} = \dfrac{1}{x^n} \quad (n \in \mathbb{N}^*) \)</td></tr>
    </tbody>
  </table>

  <h2>2. Die vier Grundtypen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( x^{2n} \)</th><th>\( x^{2n-1} \)</th><th>\( x^{-2n} \)</th><th>\( x^{-(2n-1)} \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Graph</td><td class="li">Parabel</td><td class="li">Parabel</td><td class="li">Hyperbel</td><td class="li">Hyperbel</td></tr>
      <tr><td class="li">\(D\)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td></tr>
      <tr><td class="li">\(W\)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td></tr>
      <tr><td class="li">Symmetrie</td><td class="li">Achse</td><td class="li">Punkt</td><td class="li">Achse</td><td class="li">Punkt</td></tr>
      <tr><td class="li">Nullstelle</td><td>\( x_0 = 0 \)</td><td>\( x_0 = 0 \)</td><td>—</td><td>—</td></tr>
      <tr><td class="li">Asymptoten</td><td>—</td><td>—</td><td>\( x = 0,\; y = 0 \)</td><td>\( x = 0,\; y = 0 \)</td></tr>
    </tbody>
  </table>

  <h2>3. Symmetrie</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">gerade Funktion</td><td>\( f(-x) = f(x) \) — Achsensymmetrie zur \(y\)-Achse</td></tr>
      <tr><td class="li">ungerade Funktion</td><td>\( f(-x) = -f(x) \) — Punktsymmetrie zum Ursprung</td></tr>
    </tbody>
  </table>

  <h2>4. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = a \cdot (x-u)^n + v \)</td></tr>
      <tr><td class="li">Verschiebung</td><td>\(u\) in \(x\)-, \(v\) in \(y\)-Richtung</td></tr>
      <tr><td class="li">Streckung / Spiegelung</td><td>\(|a|\) in \(y\)-Richtung; \(a < 0\): Spiegelung an \(x\)-Achse</td></tr>
      <tr><td class="li">Asymptoten (Hyperbel)</td><td>Polgerade \( x = u \), horizontale Asymptote \( y = v \)</td></tr>
    </tbody>
  </table>

  <h2>5. Nullstellen von \( a(x-u)^n + v = 0 \)</h2>
  \[ (x-u)^n = -\frac{v}{a} \]
  <table class="ftb-tabelle">
    <thead><tr><th>Exponent</th><th>rechte Seite</th><th>Lösungen</th></tr></thead>
    <tbody>
      <tr><td class="li">\(n\) gerade</td><td>\( > 0 \)</td><td>\( x = u \pm \sqrt[n]{-v/a} \) (zwei)</td></tr>
      <tr><td class="li">\(n\) gerade</td><td>\( < 0 \)</td><td class="li">keine Lösung</td></tr>
      <tr><td class="li">\(n\) ungerade</td><td class="li">beliebig</td><td>\( x = u + \sqrt[n]{-v/a} \) (genau eine)</td></tr>
    </tbody>
  </table>

  <h2>6. Parameter aus Punkten bestimmen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Gegeben</th><th>Vorgehen</th></tr></thead>
    <tbody>
      <tr><td class="li">\( y = x^n \) durch \( P(x_1 \mid y_1) \)</td>
          <td class="li">\(n\) aus \( x_1^n = y_1 \) ablesen (Vorzeichen beachtet die Parität)</td></tr>
      <tr><td class="li">\( y = a \cdot x^n \) durch \(P\) und \(Q\)</td>
          <td class="li">beide Punkte einsetzen, Gleichungen dividieren → \(n\), dann \(a\)</td></tr>
    </tbody>
  </table>
'''

A_TDS_INTRO = r'''  <div class="block block-def" style="margin-bottom:5mm">
    <div class="block-titel">📘 Anleitung</div>
    <p>12 Aufgaben mit ansteigendem Schwierigkeitsgrad. Bearbeite alle Aufgaben in einem Zug, ohne in
    die Lösungen zu schauen — diese stehen am Ende. <strong>Hilfsmittel:</strong> nur Formelsammlung
    Promath. <strong>Zeitvorgabe:</strong> ca. 45 Minuten.</p>
  </div>
'''

A_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Eine Potenzfunktion hat die Form \( f(x) = \) <span class="lueck"></span>
      &nbsp;mit&nbsp; \( n \in \) <span class="lueck"></span> &nbsp;und&nbsp; \( a \in \mathbb{R} \setminus \{0\} \).<br>
      Für \( n > 0 \) heisst der Graph <span class="lueck"></span> n-ter Ordnung,<br>
      für \( n < 0 \) <span class="lueck"></span> n-ter Ordnung.
    </div>''')
    + aufg(2, 'Potenzfunktionen erkennen', 1, r'''    <p>Welche der folgenden Funktionen sind Potenzfunktionen? Kreuze an und begründe kurz:</p>
    <p>(a) \( f(x) = 3 \cdot x^4 \) &nbsp;&nbsp; (b) \( g(x) = 2^x \) &nbsp;&nbsp;
       (c) \( h(x) = \dfrac{5}{x^2} \) &nbsp;&nbsp; (d) \( k(x) = x^2 + x \)</p>
''' + LINS)
    + aufg(3, 'Symmetrie bestimmen', 1, r'''    <p>Gerade oder ungerade? Gib jeweils die Symmetrie des Graphen an:</p>
    <p>(a) \( y = x^6 \) &nbsp;&nbsp; (b) \( y = x^7 \) &nbsp;&nbsp;
       (c) \( y = \dfrac{2}{x^3} \) &nbsp;&nbsp; (d) \( y = \dfrac{1}{2 x^4} \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Eigenschaften</div>\n'
    + aufg(4, 'Definitions- und Wertemenge', 2, r'''    <p>Gib \(D\) und \(W\) an:</p>
    <p>(a) \( y = x^4 \) &nbsp;&nbsp;&nbsp; (b) \( y = \dfrac{1}{x^2} \)</p>
''' + LINS)
    + aufg(5, 'Gemeinsame Punkte', 1, r'''    <p>Durch welche drei Punkte verlaufen <em>alle</em> Parabeln mit geradem Exponenten
    \( y = x^{2n} \)?</p>
''' + LINS)
    + aufg(6, 'Funktionswerte', 1, r'''    <p>Berechne ohne Taschenrechner:</p>
    <p>(a) \( f(x) = 2 x^3 \): \( f(-2) = \,? \) &nbsp;&nbsp;&nbsp;
       (b) \( g(x) = x^{-2} \): \( g(0.5) = \,? \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(7, 'Verschiebung', 2, r'''    <p>Der Graph von \( y = x^3 \) wird um \(2\) Einheiten nach links und \(5\) Einheiten nach oben
    verschoben. Gib die Gleichung der Bildfunktion an.</p>
''' + LINS)
    + aufg(8, 'Asymptoten', 2, r'''    <p>Bestimme Polgerade und horizontale Asymptote von \( y = \dfrac{2}{x-3} + 1 \).</p>
''' + LINS)
    + aufg(9, 'Nullstelle', 2, r'''    <p>Bestimme die Nullstelle von \( f(x) = (x-2)^3 + 8 \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Parameter bestimmen</div>\n'
    + aufg(10, 'Exponent aus Punkt', 2, r'''    <p>Die Potenzfunktion \( y = x^n \) geht durch \( P(2 \mid 32) \). Bestimme \(n\).</p>
''' + LINS)
    + aufg(11, 'Koeffizient und Exponent', 3, r'''    <p>Die Potenzfunktion \( y = a \cdot x^n \) geht durch \( P(1 \mid 3) \) und \( Q(2 \mid 48) \).
    Bestimme \(a\) und \(n\).</p>
''' + LINS)
    + aufg(12, 'Symmetrienachweis', 3, r'''    <p>Zeige rechnerisch, dass \( f(x) = \tfrac{1}{4} x^6 - 2 \) eine gerade Funktion ist.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\( f(x) = a \cdot x^n \) mit \( n \in \mathbb{Z} \setminus \{0\} \). Für \( n > 0 \):
    <strong>Parabel</strong> n-ter Ordnung, für \( n < 0 \): <strong>Hyperbel</strong> n-ter Ordnung.</p>''')
    + loes(2, r'''    <p>(a) ja (\( a = 3 \), \( n = 4 \)) · (b) nein — \(x\) steht im Exponenten (Exponentialfunktion) ·
    (c) ja — \( h(x) = 5 \cdot x^{-2} \) · (d) nein — Summe zweier Potenzen, keine reine Potenzfunktion.</p>''')
    + loes(3, r'''    <p>(a) gerade → achsensymmetrisch zur \(y\)-Achse · (b) ungerade → punktsymmetrisch zum Ursprung ·
    (c) ungerade (Exponent \(-3\)) → punktsymmetrisch · (d) gerade (Exponent \(-4\)) → achsensymmetrisch.</p>''')
    + loes(4, r'''    <p>(a) \( D = \mathbb{R} \), \( W = \mathbb{R}_0^+ \) ·
    (b) \( D = \mathbb{R} \setminus \{0\} \), \( W = \mathbb{R}^+ \).</p>''')
    + loes(5, r'''    <p>\( (0 \mid 0) \), \( (1 \mid 1) \) und \( (-1 \mid 1) \) — denn \( 0^{2n} = 0 \),
    \( (\pm 1)^{2n} = 1 \).</p>''')
    + loes(6, r'''    <p>(a) \( f(-2) = 2 \cdot (-2)^3 = 2 \cdot (-8) = -16 \) ·
    (b) \( g(0.5) = 0.5^{-2} = \dfrac{1}{0.25} = 4 \).</p>''')
    + loes(7, r'''    \[ y = (x+2)^3 + 5 \]''')
    + loes(8, r'''    <p>Definitionslücke bei \( x = 3 \) → Polgerade \( x = 3 \); Verschiebung um \(+1\) in
    \(y\)-Richtung → horizontale Asymptote \( y = 1 \).</p>''')
    + loes(9, r'''    <p>\( (x-2)^3 = -8 \;\Longrightarrow\; x - 2 = \sqrt[3]{-8} = -2 \;\Longrightarrow\; x_0 = 0 \).
    Probe: \( (0-2)^3 + 8 = -8 + 8 = 0 \) ✓</p>''')
    + loes(10, r'''    <p>\( 2^n = 32 = 2^5 \;\Longrightarrow\; n = 5 \).</p>''')
    + loes(11, r'''    <p>Aus \(P\): \( a \cdot 1^n = 3 \Rightarrow a = 3 \). Aus \(Q\): \( 3 \cdot 2^n = 48
    \Rightarrow 2^n = 16 \Rightarrow n = 4 \). Also \( y = 3 x^4 \).</p>''')
    + loes(12, r'''    <p>\( f(-x) = \tfrac{1}{4} (-x)^6 - 2 = \tfrac{1}{4} x^6 - 2 = f(x) \) — die Bedingung
    \( f(-x) = f(x) \) ist erfüllt, \(f\) ist gerade. ✓</p>''')
)

A_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Alle Graphen mit beschrifteten Achsen
    (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Pneumatik</td><td>Boyle-Mariotte an der Velopumpe</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Ballonfahrt</td><td>Volumen eines Heissluftballons</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Lichttechnik</td><td>Beleuchtungsstärke und Abstand</td><td class="s">●●●</td></tr>
      <tr><td class="nr">4</td><td>Statik</td><td>Durchbiegung eines Balkens</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Elektrotechnik</td><td>Parallelschaltung</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Energietechnik</td><td>Windleistung</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Boyle-Mariotte an der Velopumpe', 2, r'''    <p>In einer verschlossenen Velopumpe gilt bei konstanter Temperatur \( p \cdot V = 240 \)
    (Druck \(p\) in kPa, Volumen \(V\) in dm³).</p>
    <p>(a) Gib die Funktionsgleichung \( p(V) \) an und benenne den Funktionstyp.</p>
    <p>(b) Berechne den Druck bei \( V = 2\ \text{dm}^3 \).</p>
    <p>(c) Auf welches Volumen muss komprimiert werden, damit \( p = 300 \) kPa erreicht wird?</p>
    <p>(d) Skizziere den Graphen für \( 0.5 \leq V \leq 4 \) und deute das asymptotische Verhalten.</p>
''' + LINS4, tag='Pneumatik')
    + aufg(2, 'Volumen eines Heissluftballons', 2, r'''    <p>Ein Heissluftballon sei näherungsweise kugelförmig: \( V(r) = \tfrac{4}{3} \pi r^3 \).</p>
    <p>(a) Berechne das Volumen für \( r = 8.5 \) m.</p>
    <p>(b) Welchen Radius braucht ein Ballon mit \( V = 3000\ \text{m}^3 \)?</p>
    <p>(c) Der Radius wird um 10 % vergrössert. Um wie viel Prozent wächst das Volumen?</p>
''' + LINS4, tag='Ballonfahrt')
    + aufg(3, 'Beleuchtungsstärke und Abstand', 3, r'''    <p>Für eine punktförmige Lichtquelle gilt das Abstandsgesetz \( E(r) = \dfrac{k}{r^2} \)
    mit \( k = 800\ \text{lx} \cdot \text{m}^2 \) (Beleuchtungsstärke \(E\) in Lux, Abstand \(r\) in m).</p>
    <p>(a) Welcher Potenzfunktions-Typ liegt vor? Gib den Exponenten an.</p>
    <p>(b) Berechne \( E \) im Abstand \( r = 2 \) m.</p>
    <p>(c) In welchem Abstand beträgt die Beleuchtungsstärke noch \( 50 \) lx?</p>
    <p>(d) Der Abstand wird verdoppelt — auf welchen Bruchteil sinkt \(E\)?</p>
''' + LINS4, tag='Lichttechnik')
    + aufg(4, 'Durchbiegung eines Balkens', 3, r'''    <p>Die Durchbiegung eines einseitig eingespannten Balkens unter fester Last wächst mit der
    dritten Potenz der freien Länge: \( f(L) = 0.2 \cdot L^3 \) (\(f\) in mm, \(L\) in m).</p>
    <p>(a) Berechne die Durchbiegung bei \( L = 3 \) m.</p>
    <p>(b) Bei welcher Länge erreicht die Durchbiegung \( 10 \) mm?</p>
    <p>(c) Die Länge wird verdoppelt. Um welchen Faktor wächst die Durchbiegung?</p>
''' + LINS4, tag='Statik')
    + aufg(5, 'Parallelschaltung', 3, r'''    <p>Zu einem festen Widerstand \( R_2 = 1000\ \Omega \) wird \(R_1\) parallel geschaltet:
    \( R(R_1) = \dfrac{1000 \cdot R_1}{R_1 + 1000} \).</p>
    <p>(a) Berechne \( R(1000) \).</p>
    <p>(b) Wie gross muss \( R_1 \) sein, damit \( R = 800\ \Omega \) beträgt?</p>
    <p>(c) Welchem Wert nähert sich \(R\) für sehr grosse \(R_1\)? Deute die Asymptote physikalisch.</p>
''' + LINS4, tag='Elektrotechnik')
    + aufg(6, 'Windleistung', 3, r'''    <p>Die Leistung einer kleinen Windturbine wächst mit der dritten Potenz der Windgeschwindigkeit:
    \( P(v) = 0.6 \cdot v^3 \) (\(P\) in kW, \(v\) in m/s).</p>
    <p>(a) Berechne die Leistung bei \( v = 5 \) m/s.</p>
    <p>(b) Ab welcher Windgeschwindigkeit liefert die Anlage \( 300 \) kW?</p>
    <p>(c) Die Windgeschwindigkeit verdoppelt sich. Um welchen Faktor steigt die Leistung?
    Was bedeutet das für die Standortwahl?</p>
''' + LINS4, tag='Energietechnik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( p(V) = \dfrac{240}{V} = 240 \cdot V^{-1} \) — Potenzfunktion mit \( n = -1 \),
    Graph ist eine Hyperbel (physikalisch sinnvoll nur der Ast mit \( V > 0 \)).</p>
    <p>(b) \( p(2) = 120 \) kPa.</p>
    <p>(c) \( V = \dfrac{240}{300} = 0.8\ \text{dm}^3 \).</p>
    <p>(d) Für \( V \to 0 \) wächst \(p\) über alle Grenzen (Polgerade \( V = 0 \));
    für \( V \to \infty \) geht \( p \to 0 \) (horizontale Asymptote).</p>''')
    + loes(2, r'''    <p>(a) \( V(8.5) = \tfrac{4}{3} \pi \cdot 8.5^3 \approx 2572\ \text{m}^3 \).</p>
    <p>(b) \( r = \sqrt[3]{\dfrac{3V}{4\pi}} = \sqrt[3]{\dfrac{3 \cdot 3000}{4\pi}} \approx 8.95 \) m.</p>
    <p>(c) Faktor \( 1.1^3 = 1.331 \) — das Volumen wächst um gut 33 %.</p>''')
    + loes(3, r'''    <p>(a) Hyperbel 2. Ordnung: \( E = 800 \cdot r^{-2} \), Exponent \( n = -2 \).</p>
    <p>(b) \( E(2) = \dfrac{800}{4} = 200 \) lx.</p>
    <p>(c) \( r^2 = \dfrac{800}{50} = 16 \Rightarrow r = 4 \) m.</p>
    <p>(d) \( E(2r) = \dfrac{k}{4r^2} \) — auf einen Viertel.</p>''')
    + loes(4, r'''    <p>(a) \( f(3) = 0.2 \cdot 27 = 5.4 \) mm.</p>
    <p>(b) \( L^3 = \dfrac{10}{0.2} = 50 \Rightarrow L = \sqrt[3]{50} \approx 3.68 \) m.</p>
    <p>(c) Faktor \( 2^3 = 8 \) — doppelte Länge, achtfache Durchbiegung.</p>''')
    + loes(5, r'''    <p>(a) \( R(1000) = \dfrac{10^6}{2000} = 500\ \Omega \) — zwei gleiche Widerstände parallel halbieren.</p>
    <p>(b) \( \dfrac{1}{R_1} = \dfrac{1}{800} - \dfrac{1}{1000} = \dfrac{200}{800\,000}
    \Rightarrow R_1 = 4000\ \Omega \).</p>
    <p>(c) \( R \to 1000\ \Omega \) (horizontale Asymptote \( R = R_2 \)): Ein riesiger
    Parallelwiderstand trägt fast nichts bei — der Gesamtwiderstand bleibt stets unter dem
    kleinsten Einzelwiderstand.</p>''')
    + loes(6, r'''    <p>(a) \( P(5) = 0.6 \cdot 125 = 75 \) kW.</p>
    <p>(b) \( v^3 = \dfrac{300}{0.6} = 500 \Rightarrow v = \sqrt[3]{500} \approx 7.94 \) m/s.</p>
    <p>(c) Faktor \( 2^3 = 8 \). Schon geringfügig windigere Standorte liefern massiv mehr
    Energie — darum lohnt sich die sorgfältige Standortwahl (und Nabenhöhe) überproportional.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-2b  WURZELFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

B_HANDOUT = r'''
  <h2>1. Definition</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Wurzelfunktion</div>
    <p>Eine Funktion \( f : \mathbb{R}_0^+ \longrightarrow \mathbb{R}_0^+ \) mit einer Gleichung der Form</p>
    \[ y = f(x) = \sqrt[n]{x} = x^{\frac{1}{n}}, \qquad n \in \mathbb{N}^* \]
    <p>heisst <strong>Wurzelfunktion</strong> mit Wurzelexponent \(n\).</p>
  </div>

  <p>Wegen \( a^{1/n} = \sqrt[n]{a} \) sind Wurzelfunktionen Potenzfunktionen mit rationalen
  Exponenten der Form \( \tfrac{1}{n} \).</p>

  <h2>2. Wurzelfunktion als Umkehrfunktion</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Umkehrbeziehung</div>
    \[ f:\; y = x^n \;\Longrightarrow\; x = \sqrt[n]{y} \;\Longrightarrow\; f^{-1}:\; y = \sqrt[n]{x} \]
    <p>Der Graph von \( f^{-1} \) entsteht durch <strong>Spiegelung an der Winkelhalbierenden</strong>
    \( y = x \): Jeder Punkt \( (a \mid b) \) wird zu \( (b \mid a) \).</p>
  </div>

  <h3>Umkehrbarkeit der Potenzfunktionen</h3>
  <table class="ftb-tabelle">
    <thead><tr><th>Exponent</th><th>Umkehrbarkeit</th><th>Umkehrfunktion</th></tr></thead>
    <tbody>
      <tr><td class="li">gerade (z.B. \( x^2 \))</td>
          <td class="li">nur nach Einschränkung auf \( \mathbb{R}_0^+ \) (rechter Ast)</td>
          <td>\( y = \sqrt{x} \); linker Ast: \( y = -\sqrt{x} \)</td></tr>
      <tr><td class="li">ungerade (z.B. \( x^3 \))</td>
          <td class="li">auf ganz \( \mathbb{R} \) umkehrbar</td>
          <td>\( y = \sqrt[3]{x} \)</td></tr>
    </tbody>
  </table>
  <p>Es ist sinnvoll, die Umkehrbarkeit aller Potenzfunktionen einheitlich auf
  \( D = \mathbb{R}_0^+ \) zu beschränken.</p>

  <h2>3. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaften</th><th>\( y = \sqrt[n]{x} = x^{1/n} \), \( n \in \mathbb{N}^* \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td>\( D = \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Wertemenge</td><td>\( W = \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Gemeinsame Punkte</td><td>\( (0 \mid 0) \) und \( (1 \mid 1) \)</td></tr>
      <tr><td class="li">Ordinatenabschnitt</td><td>\( y_0 = 0 \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>\( x_0 = 0 \)</td></tr>
      <tr><td class="li">Symmetrie</td><td>—</td></tr>
    </tbody>
  </table>
  <p>Zwischen \(0\) und \(1\) liegt die höhere Wurzel über der niedrigeren; rechts von \(1\) ist es
  umgekehrt. Alle Kurven steigen — je grösser \(x\), desto flacher.</p>

  <h2>4. Transformationen</h2>
  <p>Ausgangsfunktion \( y = \sqrt[n]{x} \), Bildfunktion \( y = a \cdot \sqrt[n]{x-u} + v \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung; neuer Definitionsbereich \( D = [u;\, +\infty[ \)</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung</td></tr>
      <tr><td>\(|a|\)</td><td class="li">Streckung/Stauchung in \(y\)-Richtung</td></tr>
      <tr><td>\(a < 0\)</td><td class="li">Spiegelung an der \(x\)-Achse (Kurve fällt)</td></tr>
    </tbody>
  </table>
  <p>Der <strong>Startpunkt</strong> der Kurve liegt bei \( (u \mid v) \).</p>

  <h2>5. Wurzelgleichungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Grafische Lösung</div>
    <p>Beide Seiten der Gleichung als Funktionsterme auffassen und die Graphen zeichnen. Die
    \(x\)-Koordinate des Schnittpunkts liefert die Lösung (näherungsweise ablesen, algebraisch
    kontrollieren).</p>
  </div>
  <div class="block block-fehler">
    <div class="block-titel">⚠ Zwei Stolpersteine</div>
    <p><strong>1.</strong> Wurzelwerte sind nie negativ: \( \sqrt{\dots} = c \) mit \( c < 0 \) hat
    keine Lösung. <strong>2.</strong> Quadrieren ist keine Äquivalenzumformung — Scheinlösungen sind
    möglich. Nach dem Lösen immer die <strong>Probe</strong> in der Ausgangsgleichung machen.</p>
  </div>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Die Wurzelfunktion \( y = \sqrt[n]{x} \) ist die <strong>Umkehrfunktion</strong> der
    Potenzfunktion \( y = x^n \) auf \( \mathbb{R}_0^+ \) — ihr Graph ist deren Spiegelbild an der
    Winkelhalbierenden \( y = x \).</p>
  </div>
'''

B_FORMELAUSZUG = r'''
  <h2>1. Definition</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Wurzelfunktion</td>
          <td>\( y = f(x) = \sqrt[n]{x} = x^{1/n}, \quad n \in \mathbb{N}^* \)</td></tr>
      <tr><td class="li">Funktion</td>
          <td>\( f : \mathbb{R}_0^+ \longrightarrow \mathbb{R}_0^+ \)</td></tr>
    </tbody>
  </table>

  <h2>2. Umkehrbeziehung</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Umkehrfunktion</td>
          <td>\( f: y = x^n \;\Longleftrightarrow\; f^{-1}: y = \sqrt[n]{x} \) (auf \( \mathbb{R}_0^+ \))</td></tr>
      <tr><td class="li">grafisch</td>
          <td class="li">Spiegelung an der Winkelhalbierenden \( y = x \): \( (a \mid b) \to (b \mid a) \)</td></tr>
      <tr><td class="li">gerader Exponent</td>
          <td class="li">nur umkehrbar nach Einschränkung auf \( \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">ungerader Exponent</td>
          <td class="li">auf ganz \( \mathbb{R} \) umkehrbar</td></tr>
    </tbody>
  </table>

  <h2>3. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definitions-/Wertemenge</td><td>\( D = W = \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Gemeinsame Punkte</td><td>\( (0 \mid 0) \), \( (1 \mid 1) \)</td></tr>
      <tr><td class="li">Nullstelle / Ordinatenabschnitt</td><td>\( x_0 = 0 \), \( y_0 = 0 \)</td></tr>
      <tr><td class="li">Symmetrie</td><td>— (D nicht symmetrisch zum Ursprung)</td></tr>
    </tbody>
  </table>

  <h2>4. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = a \cdot \sqrt[n]{x-u} + v \)</td></tr>
      <tr><td class="li">Definitionsbereich</td><td>\( x - u \geq 0 \;\Longrightarrow\; D = [u;\, +\infty[ \)</td></tr>
      <tr><td class="li">Startpunkt</td><td>\( (u \mid v) \)</td></tr>
      <tr><td class="li">\( a < 0 \)</td><td class="li">Spiegelung an der \(x\)-Achse — Kurve fällt</td></tr>
    </tbody>
  </table>

  <h2>5. Wurzelgleichungen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Schritt</th><th>Vorgehen</th></tr></thead>
    <tbody>
      <tr><td class="li">1. Definitionsbereich</td><td class="li">Radikand \( \geq 0 \) setzen und auflösen</td></tr>
      <tr><td class="li">2. Isolieren</td><td class="li">Wurzel allein auf eine Seite bringen</td></tr>
      <tr><td class="li">3. Potenzieren</td><td>beide Seiten hoch \(n\) — Achtung: keine Äquivalenzumformung!</td></tr>
      <tr><td class="li">4. Probe</td><td class="li">Lösung in Ausgangsgleichung einsetzen (Scheinlösungen entlarven)</td></tr>
    </tbody>
  </table>
  <p>Grafisch: linke und rechte Seite als Funktionen zeichnen; \(x\)-Koordinate des Schnittpunkts =
  Lösung. Ist die rechte Seite negativ (\( \sqrt{\dots} = c \), \( c < 0 \)): keine Lösung.</p>

  <h2>6. Wichtige Umkehr-Paare</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Funktion</th><th>Umkehrfunktion</th></tr></thead>
    <tbody>
      <tr><td>\( y = x^2 \) (\( x \geq 0 \))</td><td>\( y = \sqrt{x} \)</td></tr>
      <tr><td>\( y = x^3 \)</td><td>\( y = \sqrt[3]{x} \)</td></tr>
      <tr><td>\( y = x^n \) (\( x \geq 0 \))</td><td>\( y = \sqrt[n]{x} \)</td></tr>
    </tbody>
  </table>
'''

B_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Die Wurzelfunktion \( f(x) = \sqrt[n]{x} \) lässt sich als Potenz schreiben:
      \( f(x) = x^{\,?} \) mit Exponent <span class="lueck"></span>.<br>
      Definitionsmenge: \( D = \) <span class="lueck"></span>,&nbsp;
      Wertemenge: \( W = \) <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Wurzelwerte berechnen', 1, r'''    <p>Berechne ohne Taschenrechner:</p>
    <p>(a) \( \sqrt{49} \) &nbsp;&nbsp; (b) \( \sqrt[3]{64} \) &nbsp;&nbsp;
       (c) \( \sqrt[4]{81} \) &nbsp;&nbsp; (d) \( \sqrt[5]{32} \)</p>
''' + LINS)
    + aufg(3, 'Als Potenz schreiben', 1, r'''    <p>Schreibe mit rationalem Exponenten:</p>
    <p>(a) \( \sqrt{x} \) &nbsp;&nbsp; (b) \( \sqrt[3]{x^2} \) &nbsp;&nbsp; (c) \( \dfrac{1}{\sqrt{x}} \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Umkehrfunktion</div>\n'
    + aufg(4, 'Umkehrfunktionen angeben', 2, r'''    <p>Gib die Umkehrfunktion an (jeweils auf \( \mathbb{R}_0^+ \)):</p>
    <p>(a) \( y = x^4 \) &nbsp;&nbsp;&nbsp; (b) \( y = x^5 \)</p>
''' + LINS)
    + aufg(5, 'Umkehrbarkeit begründen', 2, r'''    <p>Begründe mit einem Zahlenbeispiel, warum \( y = x^2 \) auf ganz \( \mathbb{R} \)
    <em>nicht</em> umkehrbar ist.</p>
''' + LINS)
    + aufg(6, 'Spiegelpunkt', 1, r'''    <p>Der Punkt \( P(2 \mid 8) \) liegt auf dem Graphen von \( y = x^3 \). Welcher Punkt des
    Graphen von \( y = \sqrt[3]{x} \) entspricht ihm bei der Spiegelung an \( y = x \)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Eigenschaften &amp; Transformationen</div>\n'
    + aufg(7, 'Definitionsbereich', 2, r'''    <p>Bestimme den maximalen Definitionsbereich von \( y = \sqrt{2x - 6} \).</p>
''' + LINS)
    + aufg(8, 'Startpunkt und Bereiche', 2, r'''    <p>Gib für \( y = \sqrt{x+1} - 3 \) den Startpunkt, den Definitionsbereich und die
    Wertemenge an.</p>
''' + LINS)
    + aufg(9, 'Ordinatenabschnitt und Nullstelle', 3, r'''    <p>Bestimme Ordinatenabschnitt und Nullstelle von \( y = 3\sqrt{x+1} - 6 \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Wurzelgleichungen</div>\n'
    + aufg(10, 'Quadratwurzel-Gleichung', 2, r'''    <p>Löse \( \sqrt{3x + 1} = 4 \) und mache die Probe.</p>
''' + LINS)
    + aufg(11, 'Kubikwurzel-Gleichung', 2, r'''    <p>Löse \( \sqrt[3]{x - 5} = 3 \).</p>
''' + LINS)
    + aufg(12, 'Lösbarkeit beurteilen', 3, r'''    <p>Hat die Gleichung \( \sqrt{x + 7} = -2 \) eine Lösung? Begründe ohne zu quadrieren —
    und zeige, welche Scheinlösung das Quadrieren liefern würde.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>Exponent \( \tfrac{1}{n} \); \( D = \mathbb{R}_0^+ \); \( W = \mathbb{R}_0^+ \).</p>''')
    + loes(2, r'''    <p>(a) \(7\) · (b) \(4\) · (c) \(3\) · (d) \(2\).</p>''')
    + loes(3, r'''    <p>(a) \( x^{1/2} \) · (b) \( x^{2/3} \) · (c) \( x^{-1/2} \).</p>''')
    + loes(4, r'''    <p>(a) \( y = \sqrt[4]{x} \) · (b) \( y = \sqrt[5]{x} \).</p>''')
    + loes(5, r'''    <p>Zur Höhe \( y = 4 \) gehören zwei Urbilder: \( 2^2 = 4 \) und \( (-2)^2 = 4 \).
    Eine Umkehrfunktion müsste der \(4\) einen eindeutigen Wert zuordnen — unmöglich.
    Erst die Einschränkung auf \( x \geq 0 \) macht die Zuordnung eindeutig.</p>''')
    + loes(6, r'''    <p>Koordinaten vertauschen: \( P'(8 \mid 2) \). Kontrolle: \( \sqrt[3]{8} = 2 \) ✓</p>''')
    + loes(7, r'''    <p>\( 2x - 6 \geq 0 \Rightarrow x \geq 3 \Rightarrow D = [3;\, +\infty[ \).</p>''')
    + loes(8, r'''    <p>Startpunkt \( (-1 \mid -3) \); \( D = [-1;\, +\infty[ \); \( W = [-3;\, +\infty[ \).</p>''')
    + loes(9, r'''    <p>Ordinatenabschnitt: \( y_0 = 3\sqrt{1} - 6 = -3 \). Nullstelle: \( 3\sqrt{x+1} = 6
    \Rightarrow \sqrt{x+1} = 2 \Rightarrow x + 1 = 4 \Rightarrow x_0 = 3 \).
    Probe: \( 3\sqrt{4} - 6 = 0 \) ✓</p>''')
    + loes(10, r'''    <p>Quadrieren: \( 3x + 1 = 16 \Rightarrow x = 5 \). Probe: \( \sqrt{16} = 4 \) ✓</p>''')
    + loes(11, r'''    <p>Hoch 3: \( x - 5 = 27 \Rightarrow x = 32 \). Probe: \( \sqrt[3]{27} = 3 \) ✓</p>''')
    + loes(12, r'''    <p>Keine Lösung: Die linke Seite ist ein Wurzelwert (\( \geq 0 \)), die rechte \(-2 < 0\) —
    Gleichheit unmöglich, \( L = \{\,\} \). Quadrieren ergäbe \( x + 7 = 4 \Rightarrow x = -3 \);
    die Probe \( \sqrt{4} = 2 \neq -2 \) entlarvt die Scheinlösung.</p>''')
)

B_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Alle Graphen mit beschrifteten Achsen
    (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Verkehrsphysik</td><td>Geschwindigkeit aus der Bremsspur</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Uhrentechnik</td><td>Das Sekundenpendel</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Ozeanografie</td><td>Wellen im Flachmeer</td><td class="s">●●●</td></tr>
      <tr><td class="nr">4</td><td>Geometrie</td><td>Kreiskegel mit festem Volumen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Mechanik</td><td>Fallzeit vom Turm</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Verfahrenstechnik</td><td>Kugelradius aus dem Volumen</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Geschwindigkeit aus der Bremsspur', 2, r'''    <p>Aus einer Bremsspur der Länge \(s\) lässt sich die Ausgangsgeschwindigkeit rekonstruieren:
    \( v(s) = \sqrt{2 \cdot a \cdot s} \) mit der Bremsverzögerung \( a = 7.5\ \text{m/s}^2 \).</p>
    <p>(a) Welcher Funktionstyp liegt vor? Skizziere \( v(s) \) für \( 0 \leq s \leq 60 \) m.</p>
    <p>(b) Eine Bremsspur ist \( 40 \) m lang. Wie schnell fuhr das Fahrzeug (in m/s und km/h)?</p>
    <p>(c) Wie ändert sich die rekonstruierte Geschwindigkeit, wenn die Spur viermal so lang ist?</p>
''' + LINS4, tag='Verkehrsphysik')
    + aufg(2, 'Das Sekundenpendel', 2, r'''    <p>Ein Sekundenpendel braucht für eine volle Schwingung genau \( T = 2 \) s. Es gilt
    \( T = 2\pi\sqrt{l/g} \) mit \( g = 9.81\ \text{m/s}^2 \).</p>
    <p>(a) Löse die Formel nach \(l\) auf.</p>
    <p>(b) Wie lang muss das Sekundenpendel sein?</p>
    <p>(c) Warum nannte man das Resultat früher scherzhaft „das Urmeter der Uhrmacher"?</p>
''' + LINS4, tag='Uhrentechnik')
    + aufg(3, 'Wellen im Flachmeer', 3, r'''    <p>Für Oberflächenwellen gilt \( v = 1.25 \cdot \sqrt{x} \) (\(v\) in m/s, Wellenlänge \(x\) in m),
    solange \( x \leq 6h \) (Wassertiefe \(h\)).</p>
    <p>(a) In einem Flachmeer beträgt die Wassertiefe \( 60 \) m. Bis zu welcher Wellenlänge gilt
    die Formel?</p>
    <p>(b) Berechne die maximale Wellengeschwindigkeit in diesem Flachmeer.</p>
    <p>(c) Skizziere den Graphen \( v(x) \) für \( 0 \leq x \leq 360 \) m mit beschrifteten Achsen.</p>
''' + LINS4, tag='Ozeanografie')
    + aufg(4, 'Kreiskegel mit festem Volumen', 3, r'''    <p>Ein Kreiskegel soll das Volumen \( V = 380\ \text{m}^3 \) haben: \( V = \tfrac{1}{3}\pi r^2 h \).</p>
    <p>(a) Löse nach \(r\) auf: Gib die Funktionsgleichung \( r(h) \) an.</p>
    <p>(b) Berechne den Radius für die Höhe \( h = 10 \) m und mache die Probe.</p>
    <p>(c) Wie verhält sich \( r(h) \) für sehr grosse Höhen? Deute das Ergebnis geometrisch.</p>
''' + LINS4, tag='Geometrie')
    + aufg(5, 'Fallzeit vom Turm', 3, r'''    <p>Für den freien Fall gilt \( s = \tfrac{1}{2} g t^2 \) mit \( g = 9.81\ \text{m/s}^2 \).</p>
    <p>(a) Löse nach \(t\) auf: Gib die Fallzeit-Funktion \( t(s) \) an. Welcher Funktionstyp?</p>
    <p>(b) Ein Gegenstand fällt von einem \( 50 \) m hohen Turm. Berechne die Fallzeit.</p>
    <p>(c) Aus welcher „Verdopplung" folgt: Doppelte Höhe heisst <em>nicht</em> doppelte Fallzeit —
    um welchen Faktor verlängert sich die Fallzeit tatsächlich?</p>
''' + LINS4, tag='Mechanik')
    + aufg(6, 'Kugelradius aus dem Volumen', 3, r'''    <p>In der Verfahrenstechnik muss aus dem Volumen eines kugelförmigen Tropfens sein Radius
    bestimmt werden: \( V = \tfrac{4}{3}\pi r^3 \).</p>
    <p>(a) Löse nach \(r\) auf: Gib \( r(V) \) an. Welche Wurzel tritt auf?</p>
    <p>(b) Berechne den Radius einer Kugel mit \( V = 1000\ \text{cm}^3 \) (1 Liter).</p>
    <p>(c) Das Volumen wird verachtfacht. Um welchen Faktor wächst der Radius?</p>
''' + LINS4, tag='Verfahrenstechnik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) Wurzelfunktion \( v(s) = \sqrt{15} \cdot \sqrt{s} \approx 3.87\sqrt{s} \) — steil am
    Anfang, zunehmend flacher.</p>
    <p>(b) \( v = \sqrt{2 \cdot 7.5 \cdot 40} = \sqrt{600} \approx 24.5\ \text{m/s} \approx 88 \) km/h.</p>
    <p>(c) \( \sqrt{4} = 2 \) — nur doppelt so schnell, nicht viermal.</p>''')
    + loes(2, r'''    <p>(a) \( l = \dfrac{g \cdot T^2}{4\pi^2} \) — die Umkehrfunktion (quadratisch in \(T\)).</p>
    <p>(b) \( l = \dfrac{9.81 \cdot 4}{4\pi^2} \approx 0.994 \) m — knapp ein Meter.</p>
    <p>(c) Weil die Sekundenpendel-Länge fast exakt \(1\) m beträgt, diente das Pendel im 18.
    Jahrhundert als Kandidat für die Definition des Meters.</p>''')
    + loes(3, r'''    <p>(a) \( x_{\max} = 6 \cdot 60 = 360 \) m.</p>
    <p>(b) \( v(360) = 1.25 \cdot \sqrt{360} \approx 23.7 \) m/s (rund \(85\) km/h).</p>
    <p>(c) Wurzelkurve durch den Ursprung; Achsen \( x \) [m] und \( v \) [m/s], aufgabenbezogene
    Skalierung.</p>''')
    + loes(4, r'''    <p>(a) \( r^2 = \dfrac{3V}{\pi h} \Rightarrow r(h) = \sqrt{\dfrac{3 \cdot 380}{\pi h}}
    = \sqrt{\dfrac{1140}{\pi h}} \).</p>
    <p>(b) \( r(10) = \sqrt{1140 / (10\pi)} \approx 6.02 \) m. Probe:
    \( \tfrac{1}{3}\pi \cdot 6.02^2 \cdot 10 \approx 380\ \text{m}^3 \) ✓</p>
    <p>(c) \( r \to 0 \): Je höher der Kegel bei festem Volumen, desto schlanker wird er —
    die Funktion fällt asymptotisch gegen null.</p>''')
    + loes(5, r'''    <p>(a) \( t(s) = \sqrt{\dfrac{2s}{g}} \) — eine Wurzelfunktion (Umkehrung der quadratischen
    Fallfunktion).</p>
    <p>(b) \( t = \sqrt{100/9.81} \approx 3.19 \) s.</p>
    <p>(c) Faktor \( \sqrt{2} \approx 1.41 \): doppelte Höhe, aber nur \(41\,\%\) mehr Fallzeit.</p>''')
    + loes(6, r'''    <p>(a) \( r(V) = \sqrt[3]{\dfrac{3V}{4\pi}} \) — die dritte Wurzel (Kubikwurzel).</p>
    <p>(b) \( r = \sqrt[3]{3000/(4\pi)} \approx 6.20 \) cm.</p>
    <p>(c) \( \sqrt[3]{8} = 2 \) — achtfaches Volumen, doppelter Radius.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-3  POLYNOMFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

C_HANDOUT = r'''
  <h2>1. Definition</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Polynomfunktion n-ten Grades</div>
    <p>Eine Funktion \( f : \mathbb{R} \longrightarrow \mathbb{R} \) mit einer Gleichung der Form</p>
    \[ y = f(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0, \qquad n \in \mathbb{N} \]
    <p>heisst <strong>Polynomfunktion</strong> (ganzrationale Funktion), mit \( a_k \in \mathbb{R} \)
    und \( a_n \neq 0 \). \(n\) heisst <strong>Grad</strong>, \(a_n\) <strong>Leitkoeffizient</strong>.</p>
  </div>

  <p><strong>Spezialfälle:</strong> Grad 1 = lineare Funktion, Grad 2 = quadratische Funktion,
  Potenzfunktionen \( a_n x^n \) = Polynomfunktionen mit nur einem Term. Eine Polynomfunktion ist
  eine Linearkombination von Potenzfunktionen.</p>

  <h2>2. Linearfaktoren und Nullstellen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Linearfaktordarstellung</div>
    <p>Sind \( x_1, \dots, x_n \) die Nullstellen, so gilt</p>
    \[ f(x) = a_n \cdot (x - x_1)(x - x_2) \cdots (x - x_n) \]
    <p>Jeder Linearfaktor liefert genau eine Nullstelle (Satz vom Nullprodukt) — und umgekehrt.</p>
  </div>

  <h3>Vielfachheit einer Nullstelle</h3>
  <table class="ftb-tabelle">
    <thead><tr><th>Vielfachheit</th><th>Faktor</th><th>Graph an der Nullstelle</th></tr></thead>
    <tbody>
      <tr><td class="li">einfach</td><td>\( (x-x_1)^1 \)</td><td class="li"><strong>schneidet</strong> die x-Achse (Vorzeichenwechsel)</td></tr>
      <tr><td class="li">doppelt</td><td>\( (x-x_1)^2 \)</td><td class="li"><strong>berührt</strong> die x-Achse (Hoch-/Tiefpunkt auf der Achse)</td></tr>
      <tr><td class="li">dreifach</td><td>\( (x-x_1)^3 \)</td><td class="li"><strong>schneidet terrassenförmig</strong> abgeflacht</td></tr>
    </tbody>
  </table>

  <h2>3. Globalverlauf</h2>
  <p>Für grosse \( |x| \) dominiert der Leitterm \( a_n x^n \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Grad \(n\)</th><th>\( a_n > 0 \)</th><th>\( a_n < 0 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">ungerade</td><td class="li">links unten → rechts oben ↗</td><td class="li">links oben → rechts unten ↘</td></tr>
      <tr><td class="li">gerade</td><td class="li">beide Enden oben ∪</td><td class="li">beide Enden unten ∩</td></tr>
    </tbody>
  </table>
  <p>Eine Polynomfunktion n-ten Grades hat <strong>höchstens \(n\) Nullstellen</strong> und
  <strong>höchstens \(n-1\) lokale Extremstellen</strong>; bei ungeradem Grad mindestens eine Nullstelle.</p>

  <h2>4. Extremalstellen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Hochpunkt, Tiefpunkt, lokal und absolut</div>
    <p>Ein <strong>Hochpunkt</strong> \(H\) ist ein lokal höchster Punkt des Graphen (\(y\)-Koordinate:
    <strong>lokales/relatives Maximum</strong>), ein <strong>Tiefpunkt</strong> \(T\) ein lokal tiefster
    Punkt (lokales Minimum). Ein <strong>absolutes</strong> Maximum/Minimum ist der grösste bzw.
    kleinste Funktionswert überhaupt — Polynomfunktionen ungeraden Grades besitzen keines, da sie
    unbeschränkt wachsen und fallen.</p>
  </div>

  <h2>5. Symmetrie-Schnellcheck</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:45%">nur gerade Exponenten (inkl. \(a_0\))</td><td class="li"><strong>gerade</strong> Funktion — achsensymmetrisch zur \(y\)-Achse</td></tr>
      <tr><td class="li">nur ungerade Exponenten (also \(a_0 = 0\))</td><td class="li"><strong>ungerade</strong> Funktion — punktsymmetrisch zum Ursprung</td></tr>
      <tr><td class="li">gemischte Exponenten</td><td class="li">weder gerade noch ungerade</td></tr>
    </tbody>
  </table>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Grad und Leitkoeffizient bestimmen den <strong>Globalverlauf</strong>, die Linearfaktoren die
    <strong>Nullstellen</strong> samt Vielfachheit (schneiden — berühren — Terrassen-Schnitt).
    Hoch- und Tiefpunkte sind <strong>lokale</strong> Extremwerte.</p>
  </div>
'''

C_FORMELAUSZUG = r'''
  <h2>1. Definition</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Polynomfunktion</td>
          <td>\( f(x) = a_n x^n + \dots + a_1 x + a_0, \quad a_n \neq 0 \)</td></tr>
      <tr><td class="li">Grad / Leitkoeffizient</td>
          <td class="li">\(n\) bzw. \(a_n\)</td></tr>
    </tbody>
  </table>

  <h2>2. Linearfaktoren</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Produktform</td>
          <td>\( f(x) = a_n (x-x_1)(x-x_2)\cdots(x-x_n) \)</td></tr>
      <tr><td class="li">Nullstellen</td>
          <td class="li">stehen direkt in den Faktoren (Satz vom Nullprodukt)</td></tr>
      <tr><td class="li">aus Nullstellen + Punkt</td>
          <td class="li">Ansatz mit Faktoren, \(a\) aus dem \(y\)-Achsenabschnitt: \( f(0) = a \cdot (-x_1)(-x_2)\cdots \)</td></tr>
    </tbody>
  </table>

  <h2>3. Vielfachheit</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Faktor</th><th>Verhalten an der Nullstelle</th></tr></thead>
    <tbody>
      <tr><td>\( (x-x_1)^1 \)</td><td class="li">schneidet (Vorzeichenwechsel)</td></tr>
      <tr><td>\( (x-x_1)^2 \)</td><td class="li">berührt (kein Vorzeichenwechsel)</td></tr>
      <tr><td>\( (x-x_1)^3 \)</td><td class="li">schneidet terrassenförmig abgeflacht</td></tr>
    </tbody>
  </table>

  <h2>4. Globalverlauf</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Grad</th><th>\( a_n > 0 \)</th><th>\( a_n < 0 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">ungerade</td><td class="li">↗ (unten → oben)</td><td class="li">↘ (oben → unten)</td></tr>
      <tr><td class="li">gerade</td><td class="li">∪ (beide oben)</td><td class="li">∩ (beide unten)</td></tr>
    </tbody>
  </table>

  <h2>5. Anzahlen und Begriffe</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:45%">Nullstellen</td><td class="li">höchstens \(n\); ungerader Grad: mindestens 1</td></tr>
      <tr><td class="li">lokale Extremstellen</td><td class="li">höchstens \(n-1\)</td></tr>
      <tr><td class="li">Hochpunkt / Tiefpunkt</td><td class="li">lokal höchster / tiefster Punkt (lokales Max./Min.)</td></tr>
      <tr><td class="li">absolutes Max./Min.</td><td class="li">grösster/kleinster Funktionswert überhaupt — existiert nicht immer</td></tr>
    </tbody>
  </table>

  <h2>6. Symmetrie-Schnellcheck</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:45%">nur gerade Exponenten</td><td class="li">gerade Funktion (\( f(-x) = f(x) \))</td></tr>
      <tr><td class="li">nur ungerade Exponenten</td><td class="li">ungerade Funktion (\( f(-x) = -f(x) \))</td></tr>
    </tbody>
  </table>
'''

C_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Eine Polynomfunktion n-ten Grades hat die Form
      \( f(x) = \) <span class="lueck"></span>.<br>
      Der Koeffizient der höchsten Potenz heisst <span class="lueck"></span>
      und darf nicht <span class="lueck"></span> sein.
    </div>''')
    + aufg(2, 'Polynomfunktion erkennen', 1, r'''    <p>Polynomfunktion oder nicht? Begründe kurz:</p>
    <p>(a) \( f(x) = 3x^5 - x \) &nbsp;&nbsp; (b) \( g(x) = \sqrt{x} + 1 \) &nbsp;&nbsp;
       (c) \( h(x) = \dfrac{x^2}{4} \) &nbsp;&nbsp; (d) \( k(x) = 2^x \)</p>
''' + LINS)
    + aufg(3, 'Grad und Leitkoeffizient', 1, r'''    <p>Gib Grad und Leitkoeffizient von \( f(x) = \dfrac{-4x^3 + x^2 - x}{10} \) an.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Linearfaktoren und Nullstellen</div>\n'
    + aufg(4, 'Nullstellen ablesen', 1, r'''    <p>Gib die Nullstellen von \( f(x) = 3\,(x-1)(x+5) \) an.</p>
''' + LINS)
    + aufg(5, 'Ausklammern', 2, r'''    <p>Bestimme alle Nullstellen von \( f(x) = x^3 - 16x \) durch Ausklammern.</p>
''' + LINS)
    + aufg(6, 'Funktionsgleichung aus Nullstellen', 2, r'''    <p>Eine Polynomfunktion zweiten Grades hat die Nullstellen \(-1\) und \(3\) und den
    \(y\)-Achsenabschnitt \(6\). Bestimme die Funktionsgleichung.</p>
''' + LINS)
    + aufg(7, 'Vielfachheit deuten', 2, r'''    <p>Wie verhält sich der Graph von \( f(x) = (x-2)^2 (x+3) \) an den Stellen \( x = 2 \)
    und \( x = -3 \)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Verlauf und Symmetrie</div>\n'
    + aufg(8, 'Globalverlauf', 2, r'''    <p>Beschreibe den Globalverlauf von \( f(x) = -3x^4 + x \) (beide Enden des Graphen).</p>
''' + LINS)
    + aufg(9, 'Maximale Anzahlen', 1, r'''    <p>Wie viele Nullstellen und wie viele lokale Extremstellen kann eine Polynomfunktion
    fünften Grades höchstens haben?</p>
''' + LINS)
    + aufg(10, 'Symmetrie-Schnellcheck', 2, r'''    <p>Gerade, ungerade oder keines von beidem?</p>
    <p>(a) \( y = x^4 - 2x^2 \) &nbsp;&nbsp; (b) \( y = x^3 + x \) &nbsp;&nbsp; (c) \( y = x^3 + 1 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Extremwerte</div>\n'
    + aufg(11, 'Lokal oder absolut?', 3, r'''    <p>Der Graph von \( f(x) = x^3 - x^2 - 2x + 1 \) hat den Hochpunkt \( H(-0.55 \mid 1.63) \).
    Warum ist \( 1.63 \) nur ein <em>lokales</em>, kein absolutes Maximum?</p>
''' + LINS)
    + aufg(12, 'Begründung', 3, r'''    <p>Begründe, warum \( f(x) = x^3 + 2x \) weder ein absolutes Maximum noch ein absolutes
    Minimum besitzt.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\( f(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0 \); der Koeffizient \(a_n\)
    heisst <strong>Leitkoeffizient</strong> und darf nicht <strong>null</strong> sein.</p>''')
    + loes(2, r'''    <p>(a) ja, Grad 5 · (b) nein — \( \sqrt{x} = x^{1/2} \) hat keinen natürlichen Exponenten ·
    (c) ja, Grad 2 mit \( a_2 = \tfrac{1}{4} \) · (d) nein — \(x\) steht im Exponenten.</p>''')
    + loes(3, r'''    <p>\( f(x) = -0.4x^3 + 0.1x^2 - 0.1x \): Grad \(3\), Leitkoeffizient \(-0.4\).</p>''')
    + loes(4, r'''    <p>\( x_1 = 1 \) und \( x_2 = -5 \) — direkt aus den Linearfaktoren.</p>''')
    + loes(5, r'''    <p>\( x^3 - 16x = x(x^2 - 16) = x(x-4)(x+4) \Rightarrow x_1 = -4,\; x_2 = 0,\; x_3 = 4 \).</p>''')
    + loes(6, r'''    <p>Ansatz \( f(x) = a(x+1)(x-3) \); \( f(0) = a \cdot 1 \cdot (-3) = -3a = 6 \Rightarrow a = -2 \).</p>
    \[ f(x) = -2\,(x+1)(x-3) = -2x^2 + 4x + 6 \]''')
    + loes(7, r'''    <p>Bei \( x = 2 \) (doppelte Nullstelle): Der Graph <strong>berührt</strong> die x-Achse.
    Bei \( x = -3 \) (einfache Nullstelle): Er <strong>schneidet</strong> sie.</p>''')
    + loes(8, r'''    <p>Grad 4 (gerade), \( a_4 = -3 < 0 \): <strong>beide Enden nach unten</strong> (∩-Form).</p>''')
    + loes(9, r'''    <p>Höchstens \(5\) Nullstellen und höchstens \(4\) lokale Extremstellen.</p>''')
    + loes(10, r'''    <p>(a) gerade (nur Exponenten 4, 2) · (b) ungerade (nur 3, 1) ·
    (c) weder noch — das konstante Glied \(+1\) ist ein gerader Anteil neben ungeraden.</p>''')
    + loes(11, r'''    <p>Für grosse \(x\) wächst \( x^3 \) unbeschränkt — z.B. \( f(10) = 881 \gg 1.63 \).
    Der Wert \(1.63\) ist nur in einer <em>Umgebung</em> des Hochpunkts der grösste Funktionswert.</p>''')
    + loes(12, r'''    <p>Grad 3 (ungerade): Für \( x \to +\infty \) wächst \(f\) über alle Grenzen, für
    \( x \to -\infty \) fällt sie unter alle Grenzen — es gibt weder einen grössten noch einen
    kleinsten Funktionswert. (Diese Funktion hat nicht einmal lokale Extremstellen: Sie steigt überall.)</p>''')
)

C_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Extremwerte werden
    <strong>grafisch</strong> bestimmt (Graph zeichnen bzw. Grafikrechner) — Differentialrechnung wird
    nicht vorausgesetzt. Musterlösungen am Ende.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Verpackung</td><td>Die offene Schachtel</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Biologie</td><td>Truthahn-Population</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Meteorologie</td><td>Temperaturverlauf</td><td class="s">●●●</td></tr>
      <tr><td class="nr">4</td><td>Fahrzeugbau</td><td>Flüssigkeitstank</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Geometrie</td><td>Kegel in der Kugel</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Fertigung</td><td>Tisch aus der Marmorplatte</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Die offene Schachtel', 2, r'''    <p>Aus einem Karton von \( 20 \times 15 \) cm wird eine offene Schachtel gefaltet: In den vier
    Ecken wird je ein Quadrat der Seite \(x\) ausgeschnitten.</p>
    <p>(a) Zeige: \( V(x) = x(20-2x)(15-2x) = 4x^3 - 70x^2 + 300x \). Grad? Sinnvoller Bereich?</p>
    <p>(b) Bestimme grafisch das maximale Volumen und das zugehörige \(x\).</p>
    <p>(c) Für welche \(x\) fasst die Schachtel genau \( 300\ \text{cm}^3 \)? (grafisch, zwei Lösungen)</p>
''' + LINS4, tag='Verpackung')
    + aufg(2, 'Truthahn-Population', 2, r'''    <p>Auf einer Insel ohne natürliche Feinde entwickelt sich eine ausgesetzte Truthahn-Population
    näherungsweise gemäss \( h(t) = -0.00001\,t^3 + 0.002\,t^2 + 1.5\,t + 100 \) (\(t\) in Tagen).</p>
    <p>(a) Bestimme die Anfangspopulation und skizziere den Graphen für \( 0 \leq t \leq 550 \).</p>
    <p>(b) Wann ist die Population maximal, und wie gross ist sie dann?</p>
    <p>(c) Wann sagt das Modell das Verschwinden der Population voraus? Deute biologisch.</p>
''' + LINS4, tag='Biologie')
    + aufg(3, 'Temperaturverlauf', 3, r'''    <p>Die Temperatur einer Stadt über 24 Stunden: \( T(t) = 0.01\,t(t-24)(t-18) + 10 \) in °C,
    \( t = 0 \) um 8 Uhr morgens.</p>
    <p>(a) Bestimme \( T(0) \), \( T(18) \), \( T(24) \) — was fällt auf?</p>
    <p>(b) Bestimme grafisch Höchst- und Tiefsttemperatur samt Uhrzeit sowie die Wertemenge.</p>
    <p>(c) Wann beträgt die Temperatur \(20\) °C?</p>
''' + LINS4, tag='Meteorologie')
    + aufg(4, 'Flüssigkeitstank', 3, r'''    <p>Ein Tank besteht aus einem Zylinder mit zwei angesetzten Halbkugeln (alle Radius \(x\));
    Gesamtlänge \(4.2\) m. Es gilt \( V(x) = 4.2\,\pi x^2 - \tfrac{2}{3}\pi x^3 \).</p>
    <p>(a) Leite die Formel her (Zylinderlänge \( 4.2 - 2x \)) und begründe \( 0 < x \leq 2.1 \).</p>
    <p>(b) Für welchen Radius fasst der Tank \( 25\ \text{m}^3 \)? (grafisch, Probe)</p>
    <p>(c) Bei welchem \(x\) ist \(V\) maximal? Welche Form hat der Tank dann?</p>
''' + LINS4, tag='Fahrzeugbau')
    + aufg(5, 'Kegel in der Kugel', 3, r'''    <p>In eine Kugel mit Radius \( r_1 = 2 \) dm wird ein gerader Kreiskegel (Radius \(r_2\),
    Höhe \(h\)) einbeschrieben. Nach dem Höhensatz gilt \( r_2^2 = h\,(2r_1 - h) = h\,(4 - h) \).</p>
    <p>(a) Zeige: \( V(h) = \tfrac{\pi}{3}\,h^2\,(4 - h) \). Welchen Grad hat dieses Polynom in \(h\)?</p>
    <p>(b) Bestimme grafisch, für welche Höhe \(h\) das Kegelvolumen maximal wird.</p>
    <p>(c) Gib \( r_2 \) und \( V_{\max} \) an.</p>
''' + LINS4, tag='Geometrie')
    + aufg(6, 'Tisch aus der Marmorplatte', 3, r'''    <p>Die Bruchkante einer Marmorplatte folgt näherungsweise \( y = x^2 - 4.6x + 4.93 \)
    (für \( 0 \leq x \leq 1.7 \), Masse in m). Daraus soll ein rechteckiger Tisch mit Ecke
    \( P(a \mid y(a)) \) geschnitten werden: Fläche \( A(a) = a \cdot y(a) \).</p>
    <p>(a) Zeige: \( A(a) = a^3 - 4.6a^2 + 4.93a \) — eine Polynomfunktion dritten Grades.</p>
    <p>(b) Bestimme grafisch das optimale \(a\) und die maximale Fläche.</p>
    <p>(c) Gib die beiden Seitenlängen des optimalen Tischs an.</p>
''' + LINS4, tag='Fertigung')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) Ausmultiplizieren liefert \( 4x^3 - 70x^2 + 300x \) — Grad 3; sinnvoll: \( 0 < x < 7.5 \).</p>
    <p>(b) Hochpunkt bei \( x \approx 2.83 \) cm mit \( V_{\max} \approx 379\ \text{cm}^3 \).</p>
    <p>(c) Ablesen am Graphen: \( x \approx 1.5 \) cm und \( x \approx 4.6 \) cm
    (Kontrolle: \( V(1.5) \approx 306 \), genauer \( x_1 \approx 1.46 \); \( V(4.6) \approx 297 \),
    genauer \( x_2 \approx 4.65 \) — Ablesegenauigkeit genügt).</p>''')
    + loes(2, r'''    <p>(a) \( h(0) = 100 \) Tiere.</p>
    <p>(b) Hochpunkt bei \( t = 300 \) Tagen: \( h(300) = 460 \) Tiere.</p>
    <p>(c) Nullstelle bei \( t \approx 523 \) Tagen — das Modell sagt den Zusammenbruch voraus,
    plausibel durch Überweidung der begrenzten Insel-Ressourcen. Danach verliert das Polynom-Modell
    seine Gültigkeit (negative Bestände).</p>''')
    + loes(3, r'''    <p>(a) \( T(0) = T(18) = T(24) = 10 \) °C — an den Nullstellen des Produktterms bleibt nur
    die Verschiebung \(+10\).</p>
    <p>(b) Hochpunkt \( t \approx 6.8 \) (≈ 14:50 Uhr): \( T_{\max} \approx 23.1 \) °C; Tiefpunkt
    \( t \approx 21.2 \) (≈ 5:10 Uhr): \( T_{\min} \approx 8.1 \) °C. \( W \approx [8.1;\, 23.1] \).</p>
    <p>(c) \( t \approx 3.3 \) (≈ 11:15 Uhr) und \( t \approx 11.0 \) (≈ 19:00 Uhr); die dritte
    Lösung \( t \approx 27.7 \) liegt ausserhalb von \( D = [0;\, 24] \).</p>''')
    + loes(4, r'''    <p>(a) \( V = \pi x^2 (4.2 - 2x) + \tfrac{4}{3}\pi x^3 = 4.2\pi x^2 - \tfrac{2}{3}\pi x^3 \);
    die Halbkugeln brauchen zusammen die Länge \(2x \leq 4.2\).</p>
    <p>(b) \( x \approx 1.59 \) m (Probe: \( V(1.592) \approx 25.0\ \text{m}^3 \) ✓).</p>
    <p>(c) \(V\) wächst auf dem ganzen Bereich — Randmaximum bei \( x = 2.1 \) m mit
    \( V \approx 38.8\ \text{m}^3 \): Der Tank ist dann eine reine Kugel.</p>''')
    + loes(5, r'''    <p>(a) \( V = \tfrac{\pi}{3} r_2^2 h = \tfrac{\pi}{3} h(4-h) \cdot h = \tfrac{\pi}{3} h^2 (4-h) \)
    — Grad 3 in \(h\).</p>
    <p>(b) Hochpunkt bei \( h = \tfrac{8}{3} \approx 2.67 \) dm.</p>
    <p>(c) \( r_2 = \sqrt{h(4-h)} = \tfrac{\sqrt{32}}{3} \approx 1.89 \) dm;
    \( V_{\max} = \tfrac{256\pi}{81} \approx 9.93\ \text{dm}^3 \).</p>''')
    + loes(6, r'''    <p>(a) \( A(a) = a(a^2 - 4.6a + 4.93) = a^3 - 4.6a^2 + 4.93a \). ✓</p>
    <p>(b) Hochpunkt bei \( a \approx 0.69 \) m mit \( A_{\max} \approx 1.54\ \text{m}^2 \).</p>
    <p>(c) Seiten \( a \approx 0.69 \) m und \( y(0.69) \approx 2.23 \) m.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-4a  EXPONENTIALFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

D_HANDOUT = r'''
  <h2>1. Definition</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Exponentialfunktion</div>
    <p>Eine Funktion \( f : \mathbb{R} \longrightarrow \mathbb{R}^+ \) mit einer Gleichung der Form</p>
    \[ y = f(x) = a^x, \qquad a \in \mathbb{R}^+,\quad a \neq 1 \]
    <p>heisst <strong>Exponentialfunktion</strong> mit der Basis \(a\). Die Variable steht im
    <strong>Exponenten</strong>.</p>
  </div>

  <p><strong>Ausgeschlossene Basen:</strong> \(a = 1\) ergäbe die konstante Funktion \(y = 1\);
  Basen \(a \leq 0\) sind nicht für alle reellen Exponenten definiert.</p>

  <h2>2. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaften</th><th colspan="2">\( y = a^x \), \( a > 0 \), \( a \neq 1 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td colspan="2">\( D = \mathbb{R} \)</td></tr>
      <tr><td class="li">Wertemenge</td><td colspan="2">\( W = \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">Gemeinsamer Punkt</td><td colspan="2">\( (0 \mid 1) \), denn \( a^0 = 1 \)</td></tr>
      <tr><td class="li">Nullstellen</td><td colspan="2">—</td></tr>
      <tr><td class="li">Verlauf</td><td class="li">\( a > 1 \): steigend (Wachstum)</td><td class="li">\( a < 1 \): fallend (Zerfall)</td></tr>
      <tr><td class="li">Asymptote</td><td colspan="2">\(x\)-Achse (\( y = 0 \))</td></tr>
    </tbody>
  </table>
  <p>Spiegelung an der \(y\)-Achse wechselt zwischen Wachstum und Zerfall:
  \( a^{-x} = \left(\tfrac{1}{a}\right)^{x} \).</p>

  <h2>3. Transformationen</h2>
  <p>Ausgangsfunktion \( y = a^x \), Bildfunktion \( y = k \cdot a^{x-u} + v \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung (nach rechts für \(u > 0\))</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung — die Asymptote wandert mit zu \( y = v \)</td></tr>
      <tr><td>\(|k|\)</td><td class="li">Streckung (\(|k| > 1\)) bzw. Stauchung (\(|k| < 1\)) in \(y\)-Richtung</td></tr>
      <tr><td>\(k < 0\)</td><td class="li">zusätzlich Spiegelung an der \(x\)-Achse</td></tr>
    </tbody>
  </table>

  <h2>4. Zwei Besonderheiten</h2>
  <p><strong>Streckung in \(x\) = Basiswechsel:</strong>
  \( a^{b \cdot x} = \left(a^b\right)^x = c^x \) mit \( c = a^b \).</p>
  <p><strong>Streckung in \(y\) = Verschiebung in \(x\):</strong>
  \( a^{x-u} = a^{-u} \cdot a^x = k \cdot a^x \). Die Graphen von \( k \cdot a^x \) und
  \( a^{x-u} \) sind identisch, wenn \( k \cdot a^u = 1 \), d.h. \( u = -\log_a k \).</p>

  <h2>5. Die natürliche Exponentialfunktion</h2>
  <div class="block block-def">
    <div class="block-titel">📘 e-Funktion</div>
    <p>Exponentialfunktion mit der irrationalen Basis \( e \approx 2.71828 \) (Eulersche Zahl):
    \( y = e^x \). Jede Exponentialfunktion lässt sich mit Basis \(e\) schreiben:</p>
    \[ a^x = e^{b \cdot x} \qquad \text{mit } b = \ln a \]
  </div>

  <h2>6. Modellieren von Wachstum und Zerfall</h2>
  <p>Startwert \(N_0\), pro Schritt Faktor \(a\): \( N(t) = N_0 \cdot a^t \). Prozentuale Änderung
  um \(p\,\%\) pro Schritt: \( a = 1 \pm \tfrac{p}{100} \). Verdopplung alle \(T\) Schritte:
  \( N(t) = N_0 \cdot 2^{t/T} \); Halbierung alle \(T\) Schritte: \( N(t) = N_0 \cdot 0.5^{\,t/T} \).</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Exponentialfunktionen wachsen mit konstantem <strong>Faktor</strong> pro Schritt — nicht mit
    konstantem Summand. Alle Kurven laufen durch \( (0 \mid 1) \), bleiben positiv und haben die
    \(x\)-Achse als Asymptote. Die Basis entscheidet: \( a > 1 \) Wachstum, \( a < 1 \) Zerfall.</p>
  </div>
'''

D_FORMELAUSZUG = r'''
  <h2>1. Definition</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Exponentialfunktion</td>
          <td>\( y = f(x) = a^x, \quad a \in \mathbb{R}^+,\; a \neq 1 \)</td></tr>
      <tr><td class="li">Spiegelung an \(y\)-Achse</td>
          <td>\( a^{-x} = \dfrac{1}{a^x} = \left(\dfrac{1}{a}\right)^{x} \)</td></tr>
      <tr><td class="li">e-Funktion</td>
          <td>\( y = e^x, \quad e \approx 2.71828 \)</td></tr>
      <tr><td class="li">Basiswechsel zu \(e\)</td>
          <td>\( a^x = e^{b \cdot x} \quad \text{mit } b = \ln a \)</td></tr>
    </tbody>
  </table>

  <h2>2. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( a > 1 \)</th><th>\( 0 < a < 1 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Prozesstyp</td><td class="li">Wachstum</td><td class="li">Zerfall</td></tr>
      <tr><td class="li">\(D\)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td></tr>
      <tr><td class="li">\(W\)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">Gemeinsamer Punkt</td><td>\( (0 \mid 1) \)</td><td>\( (0 \mid 1) \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>—</td><td>—</td></tr>
      <tr><td class="li">Asymptote</td><td>\( y = 0 \) (links)</td><td>\( y = 0 \) (rechts)</td></tr>
    </tbody>
  </table>

  <h2>3. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = k \cdot a^{x-u} + v \)</td></tr>
      <tr><td class="li">Asymptote</td><td>\( y = v \)</td></tr>
      <tr><td class="li">Ordinatenabschnitt</td><td>\( y_0 = k \cdot a^{-u} + v \)</td></tr>
      <tr><td class="li">Streckung in \(x\) = Basiswechsel</td><td>\( a^{b x} = (a^b)^x = c^x \)</td></tr>
      <tr><td class="li">Streckung in \(y\) = Verschiebung in \(x\)</td><td>\( a^{x-u} = a^{-u} \cdot a^x = k \cdot a^x, \quad k \cdot a^u = 1 \)</td></tr>
    </tbody>
  </table>

  <h2>4. Nullstellen von \( k \cdot a^x + v = 0 \)</h2>
  \[ a^x = -\frac{v}{k} \]
  <table class="ftb-tabelle">
    <thead><tr><th>rechte Seite</th><th>Lösungen</th></tr></thead>
    <tbody>
      <tr><td>\( > 0 \)</td><td>genau eine: \( x_0 = \log_a\left(-\tfrac{v}{k}\right) \)</td></tr>
      <tr><td>\( \leq 0 \)</td><td class="li">keine — denn \( a^x > 0 \) für alle \(x\)</td></tr>
    </tbody>
  </table>

  <h2>5. Wachstums- und Zerfallsprozesse</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Grundform</td><td>\( N(t) = N_0 \cdot a^t \) (Startwert \(N_0\), Faktor \(a\) pro Schritt)</td></tr>
      <tr><td class="li">Änderung um \(p\,\%\) pro Schritt</td><td>\( a = 1 \pm \dfrac{p}{100} \)</td></tr>
      <tr><td class="li">Verdopplung alle \(T\) Schritte</td><td>\( N(t) = N_0 \cdot 2^{t/T} \)</td></tr>
      <tr><td class="li">Halbierung alle \(T\) Schritte</td><td>\( N(t) = N_0 \cdot 0.5^{\,t/T} \)</td></tr>
    </tbody>
  </table>

  <h2>6. Parameter aus Punkten bestimmen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Gegeben</th><th>Vorgehen</th></tr></thead>
    <tbody>
      <tr><td class="li">\( y = a^x \) durch \( P(x_1 \mid y_1) \)</td>
          <td>\( a = y_1^{\,1/x_1} \)</td></tr>
      <tr><td class="li">\( y = k \cdot a^x \) durch \(P\) und \(Q\)</td>
          <td class="li">beide Punkte einsetzen, Gleichungen dividieren → \(a\), dann \(k\)</td></tr>
    </tbody>
  </table>
'''

D_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Eine Exponentialfunktion hat die Form \( f(x) = \) <span class="lueck"></span>
      &nbsp;mit&nbsp; \( a \in \) <span class="lueck"></span>.<br>
      Für \( a > 1 \) beschreibt sie einen <span class="lueck"></span>sprozess,<br>
      für \( 0 < a < 1 \) einen <span class="lueck"></span>sprozess.
    </div>''')
    + aufg(2, 'Exponentialfunktionen erkennen', 1, r'''    <p>Welche der folgenden Funktionen sind Exponentialfunktionen? Kreuze an und begründe kurz:</p>
    <p>(a) \( f(x) = 3 \cdot x^4 \) &nbsp;&nbsp; (b) \( g(x) = 2^x \) &nbsp;&nbsp;
       (c) \( h(x) = 5^{1-x} \) &nbsp;&nbsp; (d) \( k(x) = x^2 + 2^x \)</p>
''' + LINS)
    + aufg(3, 'Steigend oder fallend?', 1, r'''    <p>Entscheide ohne zu zeichnen, ob die Kurve steigt oder fällt:</p>
    <p>(a) \( y = 3^x \) &nbsp;&nbsp; (b) \( y = \left(\tfrac{1}{4}\right)^{x} \) &nbsp;&nbsp;
       (c) \( y = 0.9^x \) &nbsp;&nbsp; (d) \( y = \left(\tfrac{5}{2}\right)^{x} \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Eigenschaften</div>\n'
    + aufg(4, 'Definitions- und Wertemenge', 2, r'''    <p>Gib \(D\) und \(W\) an:</p>
    <p>(a) \( y = 2^x \) &nbsp;&nbsp;&nbsp; (b) \( y = 2^x - 4 \)</p>
''' + LINS)
    + aufg(5, 'Gemeinsamer Punkt', 1, r'''    <p>Durch welchen Punkt verlaufen <em>alle</em> Exponentialkurven \( y = a^x \)? Begründe.</p>
''' + LINS)
    + aufg(6, 'Funktionswerte', 1, r'''    <p>Berechne ohne Taschenrechner:</p>
    <p>(a) \( f(x) = 3 \cdot 2^x \): \( f(4) = \,? \) &nbsp;&nbsp;&nbsp;
       (b) \( g(x) = \left(\tfrac{1}{3}\right)^{x} \): \( g(-2) = \,? \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(7, 'Verschiebung', 2, r'''    <p>Der Graph von \( y = 2^x \) wird um \(3\) Einheiten nach links und \(1\) Einheit nach unten
    verschoben. Gib die Gleichung der Bildfunktion an.</p>
''' + LINS)
    + aufg(8, 'Asymptote und Nullstelle', 2, r'''    <p>Bestimme die horizontale Asymptote und die Nullstelle von \( y = 2^x - 8 \).</p>
''' + LINS)
    + aufg(9, 'In die Form \\( a^x \\) bringen', 2, r'''    <p>Schreibe \( f(x) = 5^{2x} \) in der Form \( f(x) = a^x \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Parameter bestimmen</div>\n'
    + aufg(10, 'Basis aus Punkt', 2, r'''    <p>Die Exponentialkurve \( y = a^x \) geht durch \( P(3 \mid 125) \). Bestimme \(a\).</p>
''' + LINS)
    + aufg(11, 'Faktor und Basis', 3, r'''    <p>Die Kurve \( y = k \cdot a^x \) geht durch \( P(0 \mid 4) \) und \( Q(3 \mid 32) \).
    Bestimme \(k\) und \(a\).</p>
''' + LINS)
    + aufg(12, 'Streckung durch Verschiebung ersetzen', 3, r'''    <p>Zeige, dass \( g(x) = \tfrac{1}{9} \cdot 3^x \) eine verschobene Kopie von \( f(x) = 3^x \)
    ist. Um wie viele Einheiten und in welche Richtung?</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\( f(x) = a^x \) mit \( a \in \mathbb{R}^+ \setminus \{1\} \). Für \( a > 1 \):
    <strong>Wachstums</strong>prozess, für \( 0 < a < 1 \): <strong>Zerfalls</strong>prozess.</p>''')
    + loes(2, r'''    <p>(a) nein — \(x\) steht in der Basis (Potenzfunktion) · (b) ja ·
    (c) ja — \( 5^{1-x} = 5 \cdot \left(\tfrac{1}{5}\right)^{x} \) · (d) nein — Summe aus Potenz-
    und Exponentialterm.</p>''')
    + loes(3, r'''    <p>(a) steigend (\( a = 3 > 1 \)) · (b) fallend (\( a = \tfrac{1}{4} < 1 \)) ·
    (c) fallend (\( a = 0.9 < 1 \)) · (d) steigend (\( a = \tfrac{5}{2} > 1 \)).</p>''')
    + loes(4, r'''    <p>(a) \( D = \mathbb{R} \), \( W = \mathbb{R}^+ \) ·
    (b) \( D = \mathbb{R} \), \( W = \{ y \mid y > -4 \} \) — die Verschiebung nimmt die
    Wertemenge mit.</p>''')
    + loes(5, r'''    <p>\( (0 \mid 1) \) — denn \( a^0 = 1 \) für jede zulässige Basis \(a\).</p>''')
    + loes(6, r'''    <p>(a) \( f(4) = 3 \cdot 2^4 = 3 \cdot 16 = 48 \) ·
    (b) \( g(-2) = \left(\tfrac{1}{3}\right)^{-2} = 3^2 = 9 \).</p>''')
    + loes(7, r'''    \[ y = 2^{x+3} - 1 \]''')
    + loes(8, r'''    <p>Asymptote \( y = -8 \) (Verschiebung um \(-8\)); Nullstelle: \( 2^x = 8 \Rightarrow x_0 = 3 \).</p>''')
    + loes(9, r'''    <p>\( 5^{2x} = \left(5^2\right)^x = 25^x \) — also \( a = 25 \).</p>''')
    + loes(10, r'''    <p>\( a^3 = 125 = 5^3 \;\Longrightarrow\; a = 5 \).</p>''')
    + loes(11, r'''    <p>Aus \(P\): \( k \cdot a^0 = k = 4 \). Aus \(Q\): \( 4 \cdot a^3 = 32 \Rightarrow a^3 = 8
    \Rightarrow a = 2 \). Also \( y = 4 \cdot 2^x \).</p>''')
    + loes(12, r'''    <p>\( \tfrac{1}{9} = 3^{-2} \), also \( g(x) = 3^{-2} \cdot 3^x = 3^{x-2} \) —
    Verschiebung um \(2\) Einheiten <strong>nach rechts</strong>.</p>''')
)

D_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Alle Graphen mit beschrifteten Achsen
    (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Biologie</td><td>Zellkultur</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Finanzmathematik</td><td>Degressive Abschreibung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Physik</td><td>Luftdruck und Höhe</td><td class="s">●●●</td></tr>
      <tr><td class="nr">4</td><td>Elektrotechnik</td><td>Kondensator-Entladung</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Finanzmathematik</td><td>Zinseszins und Verdopplung</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Life Sciences</td><td>Medikamentenabbau</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Zellkultur', 2, r'''    <p>Eine Zellkultur startet mit \( N_0 = 500 \) Zellen; die Zellzahl verdoppelt sich alle
    \(2\) Stunden.</p>
    <p>(a) Gib die Funktionsgleichung \( N(t) \) an (\(t\) in Stunden).</p>
    <p>(b) Berechne die Zellzahl nach \(6\) Stunden.</p>
    <p>(c) Nach wie vielen Stunden sind \( 64\,000 \) Zellen erreicht? (Ohne Logarithmus lösbar!)</p>
''' + LINS4, tag='Biologie')
    + aufg(2, 'Degressive Abschreibung', 2, r'''    <p>Eine Maschine kostet neu \( 24\,000 \) CHF und verliert pro Jahr \(20\) % ihres
    Buchwerts.</p>
    <p>(a) Gib die Funktionsgleichung \( W(n) \) für den Buchwert nach \(n\) Jahren an.</p>
    <p>(b) Berechne den Buchwert nach \(3\) Jahren.</p>
    <p>(c) Ab welchem Jahr liegt der Buchwert erstmals unter einem Drittel des Neuwerts?</p>
''' + LINS4, tag='Finanzmathematik')
    + aufg(3, 'Luftdruck und Höhe', 3, r'''    <p>Näherungsweise nimmt der Luftdruck pro Kilometer Höhe um \(12\) % ab; auf Meereshöhe
    beträgt er \( 1013 \) hPa: \( p(h) = 1013 \cdot 0.88^h \) (\(h\) in km).</p>
    <p>(a) Berechne den Luftdruck auf \( 3000 \) m Höhe.</p>
    <p>(b) In welcher Höhe hat sich der Druck halbiert?</p>
    <p>(c) Warum ist ein exponentielles Modell hier plausibler als ein lineares?</p>
''' + LINS4, tag='Physik')
    + aufg(4, 'Kondensator-Entladung', 3, r'''    <p>Ein Kondensator entlädt sich über einen Widerstand nach \( U(t) = 12 \cdot e^{-t/2} \)
    (\(U\) in Volt, \(t\) in Sekunden).</p>
    <p>(a) Gib Startspannung und Asymptote an.</p>
    <p>(b) Berechne die Spannung nach \(1\) Sekunde.</p>
    <p>(c) Nach welcher Zeit ist die Spannung auf \(1\) V gesunken?</p>
''' + LINS4, tag='Elektrotechnik')
    + aufg(5, 'Zinseszins und Verdopplung', 3, r'''    <p>Ein Kapital von \( 2000 \) CHF wird zu \(3\) % Jahreszins mit Zinseszins angelegt.</p>
    <p>(a) Gib die Funktionsgleichung \( K(n) \) an.</p>
    <p>(b) Berechne das Kapital nach \(10\) Jahren.</p>
    <p>(c) Nach wie vielen Jahren hat sich das Kapital verdoppelt? Zeige, dass die Antwort
    nicht vom Startkapital abhängt.</p>
''' + LINS4, tag='Finanzmathematik')
    + aufg(6, 'Medikamentenabbau', 3, r'''    <p>Nach der Einnahme baut der Körper ein Medikament exponentiell ab: pro Stunde um \(15\) %.
    Die Anfangsdosis beträgt \( 100 \) mg.</p>
    <p>(a) Gib die Funktionsgleichung \( C(t) \) an (\(t\) in Stunden, \(C\) in mg).</p>
    <p>(b) Welche Menge ist nach \(6\) Stunden noch im Körper?</p>
    <p>(c) Bestimme die Halbwertszeit des Medikaments.</p>
''' + LINS4, tag='Life Sciences')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) Verdopplung alle \(2\) h: \( N(t) = 500 \cdot 2^{t/2} \).</p>
    <p>(b) \( N(6) = 500 \cdot 2^3 = 4000 \) Zellen.</p>
    <p>(c) \( 2^{t/2} = \dfrac{64\,000}{500} = 128 = 2^7 \Rightarrow \dfrac{t}{2} = 7
    \Rightarrow t = 14 \) h.</p>''')
    + loes(2, r'''    <p>(a) Pro Jahr bleiben \(80\) %: \( W(n) = 24\,000 \cdot 0.8^n \).</p>
    <p>(b) \( W(3) = 24\,000 \cdot 0.512 = 12\,288 \) CHF.</p>
    <p>(c) Ansatz \( 0.8^n < \tfrac{1}{3} \): \( n = \log_{0.8} \tfrac{1}{3} \approx 4.92 \) —
    ab dem \(5\). Jahr (\( W(5) \approx 7864 \) CHF \( < 8000 \) CHF).</p>''')
    + loes(3, r'''    <p>(a) \( p(3) = 1013 \cdot 0.88^3 \approx 690 \) hPa.</p>
    <p>(b) \( 0.88^h = 0.5 \Rightarrow h = \log_{0.88} 0.5 = \dfrac{\ln 0.5}{\ln 0.88}
    \approx 5.4 \) km.</p>
    <p>(c) Die Abnahme ist proportional zum aktuellen Druck (gleiche Höhendifferenz → gleicher
    Faktor). Ein lineares Modell würde ab ca. \(8.4\) km negativen Druck liefern — physikalisch
    unmöglich; die Exponentialkurve bleibt positiv.</p>''')
    + loes(4, r'''    <p>(a) Startspannung \( U(0) = 12 \) V; Asymptote \( U = 0 \) (vollständige Entladung).</p>
    <p>(b) \( U(1) = 12 \cdot e^{-0.5} \approx 7.28 \) V.</p>
    <p>(c) \( 12 \cdot e^{-t/2} = 1 \Rightarrow e^{-t/2} = \tfrac{1}{12} \Rightarrow
    t = 2 \ln 12 \approx 4.97 \) s.</p>''')
    + loes(5, r'''    <p>(a) \( K(n) = 2000 \cdot 1.03^n \).</p>
    <p>(b) \( K(10) = 2000 \cdot 1.03^{10} \approx 2687.83 \) CHF.</p>
    <p>(c) \( K_0 \cdot 1.03^n = 2 K_0 \Rightarrow 1.03^n = 2 \Rightarrow n = \log_{1.03} 2
    \approx 23.4 \) Jahre — \(K_0\) kürzt sich weg, die Verdopplungszeit hängt nur vom Zinssatz ab.</p>''')
    + loes(6, r'''    <p>(a) Pro Stunde bleiben \(85\) %: \( C(t) = 100 \cdot 0.85^t \).</p>
    <p>(b) \( C(6) = 100 \cdot 0.85^6 \approx 37.7 \) mg.</p>
    <p>(c) \( 0.85^t = 0.5 \Rightarrow t = \dfrac{\ln 0.5}{\ln 0.85} \approx 4.3 \) h.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-4b  LOGARITHMUSFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

E_HANDOUT = r'''
  <h2>1. Definition</h2>

  <p>Die Umkehrfunktion der Exponentialfunktion \( y = a^x \) entsteht durch Auflösen nach \(x\)
  (Logarithmieren) und Variablentausch:</p>
  \[ y = a^x \;\Longrightarrow\; x = \log_a y \qquad \Longrightarrow \qquad f^{-1}:\ y = \log_a x \]

  <div class="block block-def">
    <div class="block-titel">📘 Logarithmusfunktion</div>
    <p>Eine Funktion \( f : \mathbb{R}^+ \longrightarrow \mathbb{R} \) mit einer Gleichung der Form</p>
    \[ y = f(x) = \log_a x, \qquad a \in \mathbb{R}^+,\quad a \neq 1 \]
    <p>heisst <strong>Logarithmusfunktion</strong> mit der Basis \(a\).</p>
  </div>

  <p>Der Graph ist die an der <strong>Winkelhalbierenden</strong> \( y = x \) gespiegelte
  Exponentialkurve — alle Eigenschaften folgen aus dieser Spiegelung.</p>

  <h2>2. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaften</th><th colspan="2">\( y = \log_a x \), \( a > 0 \), \( a \neq 1 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td colspan="2">\( D = \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">Wertemenge</td><td colspan="2">\( W = \mathbb{R} \)</td></tr>
      <tr><td class="li">Gemeinsamer Punkt</td><td colspan="2">\( (1 \mid 0) \), denn \( \log_a 1 = 0 \)</td></tr>
      <tr><td class="li">Nullstelle</td><td colspan="2">\( x_0 = 1 \)</td></tr>
      <tr><td class="li">Verlauf</td><td class="li">\( a > 1 \): steigend, immer flacher</td><td class="li">\( a < 1 \): fallend</td></tr>
      <tr><td class="li">Asymptote</td><td colspan="2">\(y\)-Achse (\( x = 0 \))</td></tr>
    </tbody>
  </table>

  <h2>3. Transformationen</h2>
  <p>Ausgangsfunktion \( y = \log_a x \), Bildfunktion \( y = k \cdot \log_a(x-u) + v \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung — die vertikale Asymptote wandert mit zu \( x = u \)</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung</td></tr>
      <tr><td>\(|k|\)</td><td class="li">Streckung (\(|k| > 1\)) bzw. Stauchung (\(|k| < 1\)) in \(y\)-Richtung</td></tr>
      <tr><td>\(k < 0\)</td><td class="li">zusätzlich Spiegelung an der \(x\)-Achse</td></tr>
    </tbody>
  </table>

  <h2>4. Zwei Besonderheiten</h2>
  <p><strong>Streckung in \(y\) = Basiswechsel:</strong>
  \( k \cdot \log_a x = \log_c x \), wenn \( k \cdot \log_a c = 1 \). Alle Logarithmuskurven
  sind vertikal gestreckte Kopien voneinander.</p>
  <p><strong>Streckung in \(x\) = Verschiebung in \(y\):</strong>
  \( \log_a(b \cdot x) = \log_a x + \log_a b = \log_a x + v \) mit \( v = \log_a b \).</p>

  <h2>5. Die natürliche Logarithmusfunktion</h2>
  <div class="block block-def">
    <div class="block-titel">📘 ln-Funktion</div>
    <p>Logarithmusfunktion mit der irrationalen Basis \( e \approx 2.71828 \):
    \( y = \log_e x = \ln x \). Basiswechsel:</p>
    \[ \log_a x = \frac{\ln x}{\ln a} = k \cdot \ln x \qquad \text{mit } k = \frac{1}{\ln a} \]
  </div>

  <h2>6. Umkehrfunktionen bestimmen</h2>
  <p>Vorgehen: (1) Funktionsgleichung nach \(x\) auflösen — bei \(x\) im Exponenten durch
  <strong>Logarithmieren</strong>, bei \(x\) im Logarithmus durch <strong>Exponenzieren</strong>.
  (2) Variablen vertauschen. Kontrolle: \(D\) und \(W\) tauschen die Rollen.</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Die Logarithmusfunktion ist die <strong>Umkehrfunktion</strong> der Exponentialfunktion:
    Spiegelung an \( y = x \) vertauscht \( (0 \mid 1) \leftrightarrow (1 \mid 0) \), horizontale
    und vertikale Asymptote sowie \(D\) und \(W\). Der Logarithmus macht aus Faktoren
    Summanden — darum eignet er sich für Skalen über viele Grössenordnungen (Phon, pH, Magnitude).</p>
  </div>
'''

E_FORMELAUSZUG = r'''
  <h2>1. Definition</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Logarithmusfunktion</td>
          <td>\( y = f(x) = \log_a x, \quad a \in \mathbb{R}^+,\; a \neq 1 \)</td></tr>
      <tr><td class="li">Umkehrfunktion von</td>
          <td>\( y = a^x \) — Spiegelung an \( y = x \)</td></tr>
      <tr><td class="li">ln-Funktion</td>
          <td>\( y = \ln x = \log_e x, \quad e \approx 2.71828 \)</td></tr>
      <tr><td class="li">Basiswechsel</td>
          <td>\( \log_a x = \dfrac{\ln x}{\ln a} = \dfrac{\lg x}{\lg a} \)</td></tr>
    </tbody>
  </table>

  <h2>2. Exponential- und Logarithmusfunktion im Vergleich</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( y = a^x \)</th><th>\( y = \log_a x \)</th></tr></thead>
    <tbody>
      <tr><td class="li">\(D\)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">\(W\)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R} \)</td></tr>
      <tr><td class="li">Gemeinsamer Punkt</td><td>\( (0 \mid 1) \)</td><td>\( (1 \mid 0) \)</td></tr>
      <tr><td class="li">Nullstelle</td><td>—</td><td>\( x_0 = 1 \)</td></tr>
      <tr><td class="li">Asymptote</td><td>\( y = 0 \)</td><td>\( x = 0 \)</td></tr>
      <tr><td class="li">Spezialfall Basis \(e\)</td><td>\( e^x \)</td><td>\( \ln x \)</td></tr>
    </tbody>
  </table>

  <h2>3. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = k \cdot \log_a(x-u) + v \)</td></tr>
      <tr><td class="li">Vertikale Asymptote</td><td>\( x = u \)</td></tr>
      <tr><td class="li">Definitionsmenge</td><td>\( D = \{ x \mid x > u \} \)</td></tr>
      <tr><td class="li">Nullstelle</td><td>\( x_0 = u + a^{-v/k} \)</td></tr>
      <tr><td class="li">Streckung in \(y\) = Basiswechsel</td><td>\( k \cdot \log_a x = \log_c x, \quad k \cdot \log_a c = 1 \)</td></tr>
      <tr><td class="li">Streckung in \(x\) = Verschiebung in \(y\)</td><td>\( \log_a(b x) = \log_a x + \log_a b \)</td></tr>
    </tbody>
  </table>

  <h2>4. Umkehrfunktionen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Funktion</th><th>Umkehrfunktion</th></tr></thead>
    <tbody>
      <tr><td>\( y = a^x \)</td><td>\( y = \log_a x \)</td></tr>
      <tr><td>\( y = e^x \)</td><td>\( y = \ln x \)</td></tr>
      <tr><td>\( y = k \cdot a^x \)</td><td>\( y = \log_a \dfrac{x}{k} \)</td></tr>
      <tr><td>\( y = a^x + v \)</td><td>\( y = \log_a(x - v) \)</td></tr>
    </tbody>
  </table>
  <p class="li">Vorgehen: nach \(x\) auflösen (logarithmieren bzw. exponenzieren), dann Variablen tauschen.</p>

  <h2>5. Logarithmische Skalen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Lautstärke (Weber-Fechner)</td><td>\( L = 10 \cdot \lg\dfrac{J}{J_0} \) [Phon]</td></tr>
      <tr><td class="li">pH-Wert</td><td>\( \text{pH} = -\lg c \)</td></tr>
      <tr><td class="li">Zerfallsdauer aus Restanteil</td><td>\( \dfrac{N}{N_0} = 0.5^{\,t/T} \;\Rightarrow\; t = T \cdot \dfrac{\ln(N/N_0)}{\ln 0.5} \)</td></tr>
    </tbody>
  </table>
'''

E_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Die Logarithmusfunktion \( f(x) = \) <span class="lueck"></span> ist die
      <span class="lueck"></span> der Exponentialfunktion \( y = a^x \).<br>
      Ihre Definitionsmenge ist \( D = \) <span class="lueck"></span>,
      ihre Nullstelle liegt bei \( x_0 = \) <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Logarithmen ohne Taschenrechner', 1, r'''    <p>Berechne:</p>
    <p>(a) \( \log_2 32 \) &nbsp;&nbsp; (b) \( \log_3 \dfrac{1}{9} \) &nbsp;&nbsp;
       (c) \( \lg 10\,000 \) &nbsp;&nbsp; (d) \( \ln e \)</p>
''' + LINS)
    + aufg(3, 'Umkehrfunktionen angeben', 1, r'''    <p>Gib die Umkehrfunktion an:</p>
    <p>(a) \( y = 4^x \) &nbsp;&nbsp;&nbsp; (b) \( y = \lg x \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Eigenschaften</div>\n'
    + aufg(4, 'Definitions- und Wertemenge', 2, r'''    <p>Gib \(D\) und \(W\) an:</p>
    <p>(a) \( y = \log_5 x \) &nbsp;&nbsp;&nbsp; (b) \( y = \ln(x - 2) \)</p>
''' + LINS)
    + aufg(5, 'Gemeinsamer Punkt', 1, r'''    <p>Durch welchen Punkt verlaufen <em>alle</em> Logarithmuskurven \( y = \log_a x \)? Begründe.</p>
''' + LINS)
    + aufg(6, 'Steigend oder fallend?', 1, r'''    <p>Entscheide ohne zu zeichnen, ob die Kurve steigt oder fällt:</p>
    <p>(a) \( y = \log_3 x \) &nbsp;&nbsp; (b) \( y = \log_{1/3} x \) &nbsp;&nbsp;
       (c) \( y = -\ln x \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(7, 'Verschiebung', 2, r'''    <p>Der Graph von \( y = \ln x \) wird um \(2\) Einheiten nach rechts und \(1\) Einheit nach
    oben verschoben. Gib die Gleichung der Bildfunktion und ihre vertikale Asymptote an.</p>
''' + LINS)
    + aufg(8, 'Nullstelle', 2, r'''    <p>Bestimme die Nullstelle von \( f(x) = \log_2 x - 3 \).</p>
''' + LINS)
    + aufg(9, 'Basiswechsel', 2, r'''    <p>Schreibe \( y = \log_4 x \) in der Form \( y = k \cdot \ln x \). Bestimme \(k\) auf drei
    Dezimalen.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Parameter bestimmen</div>\n'
    + aufg(10, 'Streckfaktor aus Punkt', 2, r'''    <p>Die Kurve \( y = k \cdot \log_2 x \) geht durch \( P(8 \mid 6) \). Bestimme \(k\).</p>
''' + LINS)
    + aufg(11, 'Punkte spiegeln', 3, r'''    <p>Der Punkt \( P(3 \mid 8) \) liegt auf dem Graphen von \( y = 2^x \). Gib ohne Rechnung
    einen Punkt des Graphen von \( y = \log_2 x \) an und begründe.</p>
''' + LINS)
    + aufg(12, 'Identische Funktionen', 3, r'''    <p>Zeige durch Basiswechsel, dass \( f(x) = 2 \cdot \log_9 x \) und \( g(x) = \log_3 x \)
    identisch sind.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\( f(x) = \log_a x \) ist die <strong>Umkehrfunktion</strong> von \( y = a^x \);
    \( D = \mathbb{R}^+ \), Nullstelle \( x_0 = 1 \).</p>''')
    + loes(2, r'''    <p>(a) \( 2^5 = 32 \Rightarrow 5 \) · (b) \( 3^{-2} = \tfrac{1}{9} \Rightarrow -2 \) ·
    (c) \( 10^4 \Rightarrow 4 \) · (d) \( e^1 = e \Rightarrow 1 \).</p>''')
    + loes(3, r'''    <p>(a) \( y = \log_4 x \) · (b) \( y = 10^x \) — die Umkehrfunktion der Logarithmusfunktion
    ist eine Exponentialfunktion.</p>''')
    + loes(4, r'''    <p>(a) \( D = \mathbb{R}^+ \), \( W = \mathbb{R} \) ·
    (b) \( x - 2 > 0 \Rightarrow D = \{ x \mid x > 2 \} \), \( W = \mathbb{R} \).</p>''')
    + loes(5, r'''    <p>\( (1 \mid 0) \) — denn \( \log_a 1 = 0 \) für jede zulässige Basis (\( a^0 = 1 \)).</p>''')
    + loes(6, r'''    <p>(a) steigend (\( a = 3 > 1 \)) · (b) fallend (\( a < 1 \)) ·
    (c) fallend — \( \ln x \) an der \(x\)-Achse gespiegelt.</p>''')
    + loes(7, r'''    <p>\( y = \ln(x-2) + 1 \); vertikale Asymptote \( x = 2 \).</p>''')
    + loes(8, r'''    <p>\( \log_2 x = 3 \Rightarrow x_0 = 2^3 = 8 \).</p>''')
    + loes(9, r'''    <p>\( \log_4 x = \dfrac{\ln x}{\ln 4} \approx 0.721 \cdot \ln x \) — also \( k = \dfrac{1}{\ln 4} \approx 0.721 \).</p>''')
    + loes(10, r'''    <p>\( \log_2 8 = 3 \), also \( 6 = k \cdot 3 \Rightarrow k = 2 \).</p>''')
    + loes(11, r'''    <p>\( P'(8 \mid 3) \) — die Spiegelung an \( y = x \) vertauscht die Koordinaten.
    Kontrolle: \( \log_2 8 = 3 \) ✓</p>''')
    + loes(12, r'''    <p>\( f(x) = 2 \cdot \log_9 x = 2 \cdot \dfrac{\log_3 x}{\log_3 9} = 2 \cdot
    \dfrac{\log_3 x}{2} = \log_3 x = g(x) \) ✓</p>''')
)

E_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Alle Graphen mit beschrifteten Achsen
    (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Akustik</td><td>Schallpegel</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Chemie</td><td>pH-Wert</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Geologie</td><td>Erdbeben-Magnitude</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Archäologie</td><td>C-14-Datierung</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Finanzmathematik</td><td>Verdopplungszeit</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Elektrotechnik</td><td>Entladezeit eines Kondensators</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Schallpegel', 2, r'''    <p>Das Lautstärkeempfinden folgt dem Weber-Fechner-Gesetz \( L = 10 \cdot \lg\dfrac{J}{J_0} \)
    (\(L\) in Phon, \(J_0\): Hörschwelle).</p>
    <p>(a) Ein Düsentriebwerk erreicht \( J = 10^{12} \cdot J_0 \). Berechne \(L\).</p>
    <p>(b) Zwei gleich laute Schallquellen verdoppeln die Intensität. Um wie viele Phon steigt
    der Pegel?</p>
    <p>(c) Warum ist eine logarithmische Skala hier sinnvoll?</p>
''' + LINS4, tag='Akustik')
    + aufg(2, 'pH-Wert', 2, r'''    <p>Der pH-Wert ist definiert als \( \text{pH} = -\lg c \) (\(c\): Wasserstoffionen-Konzentration
    in mol/l).</p>
    <p>(a) Berechne den pH-Wert einer Lösung mit \( c = 2 \cdot 10^{-5} \) mol/l.</p>
    <p>(b) Um wie viel ändert sich der pH-Wert, wenn die Konzentration verzehnfacht wird?</p>
    <p>(c) Welche Konzentration hat eine Lösung mit pH \(9\)?</p>
''' + LINS4, tag='Chemie')
    + aufg(3, 'Erdbeben-Magnitude', 2, r'''    <p>Die Magnitude eines Erdbebens ist näherungsweise \( M = \lg\dfrac{A}{A_0} \)
    (\(A\): Amplitude im Seismogramm, \(A_0\): Referenzamplitude).</p>
    <p>(a) Ein Beben hat die tausendfache Referenzamplitude. Berechne \(M\).</p>
    <p>(b) Beben B hat Magnitude \(6\), Beben C Magnitude \(4\). Um welchen Faktor unterscheiden
    sich die Amplituden?</p>
    <p>(c) Was bedeutet ein Magnitudenschritt von \(+1\) für die Amplitude?</p>
''' + LINS4, tag='Geologie')
    + aufg(4, 'C-14-Datierung', 3, r'''    <p>C-14 zerfällt mit Halbwertszeit \( T = 5730 \) Jahren:
    \( \dfrac{N(t)}{N_0} = 0.5^{\,t/T} \).</p>
    <p>(a) Löse die Gleichung allgemein nach \(t\) auf.</p>
    <p>(b) In einem Fund werden noch \(60\) % des ursprünglichen C-14 gemessen. Wie alt ist er?</p>
    <p>(c) Warum ist die Methode für sehr junge Funde (unter 100 Jahren) ungenau? Argumentiere
    mit der Flachheit der Kurve.</p>
''' + LINS4, tag='Archäologie')
    + aufg(5, 'Verdopplungszeit', 3, r'''    <p>Ein Kapital wird zu \(2.5\) % Jahreszins mit Zinseszins angelegt: \( K(n) = K_0 \cdot 1.025^n \).</p>
    <p>(a) Leite mit dem Logarithmus eine Formel für die Verdopplungszeit her.</p>
    <p>(b) Berechne die Verdopplungszeit.</p>
    <p>(c) Faustregel: „Verdopplungszeit \( \approx 70 / p \)" (\(p\) in %). Prüfe die Regel an
    diesem Beispiel.</p>
''' + LINS4, tag='Finanzmathematik')
    + aufg(6, 'Entladezeit eines Kondensators', 3, r'''    <p>Ein Kondensator entlädt sich nach \( U(t) = 9 \cdot e^{-t/3} \) (\(U\) in Volt,
    \(t\) in Sekunden).</p>
    <p>(a) Löse die Gleichung allgemein nach \(t\) auf (Umkehrfunktion).</p>
    <p>(b) Nach welcher Zeit ist die Spannung auf \( 0.5 \) V gesunken?</p>
    <p>(c) Skizziere \(U(t)\) und die Umkehrfunktion \(t(U)\) — welche Kurventypen entstehen?</p>
''' + LINS4, tag='Elektrotechnik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( L = 10 \cdot \lg 10^{12} = 120 \) Phon.</p>
    <p>(b) \( \Delta L = 10 \cdot \lg 2 \approx 3 \) Phon — Verdopplung der Intensität gibt immer
    \(+3\) Phon.</p>
    <p>(c) Das Ohr verarbeitet Intensitäten über \(12\) Grössenordnungen; der Logarithmus bildet
    diese auf eine handliche Skala von \(0\) bis \(120\) ab (Faktoren werden Summanden).</p>''')
    + loes(2, r'''    <p>(a) \( \text{pH} = -\lg(2 \cdot 10^{-5}) \approx 4.7 \).</p>
    <p>(b) \( -\lg(10 c) = -\lg c - 1 \) — der pH-Wert sinkt um \(1\).</p>
    <p>(c) \( c = 10^{-9} \) mol/l (Exponenzieren als Umkehrung).</p>''')
    + loes(3, r'''    <p>(a) \( M = \lg 1000 = 3 \).</p>
    <p>(b) \( \Delta M = 2 \Rightarrow \) Faktor \( 10^2 = 100 \).</p>
    <p>(c) Ein Schritt \(+1\) bedeutet <strong>zehnfache</strong> Amplitude — die Skala ist
    logarithmisch.</p>''')
    + loes(4, r'''    <p>(a) Logarithmieren: \( t = T \cdot \dfrac{\ln(N/N_0)}{\ln 0.5} \).</p>
    <p>(b) \( t = 5730 \cdot \dfrac{\ln 0.6}{\ln 0.5} \approx 4223 \) Jahre.</p>
    <p>(c) Nach \(100\) Jahren sind noch \( 0.5^{100/5730} \approx 98.8 \) % vorhanden — die
    Kurve ist dort fast flach. Kleine Messfehler im Anteil ergeben grosse Fehler in \(t\).</p>''')
    + loes(5, r'''    <p>(a) \( 1.025^n = 2 \Rightarrow n = \dfrac{\ln 2}{\ln 1.025} \).</p>
    <p>(b) \( n \approx 28.1 \) Jahre.</p>
    <p>(c) Faustregel: \( 70 / 2.5 = 28 \) — sehr nahe am exakten Wert \(28.1\); die Regel
    nutzt \( \ln 2 \approx 0.7 \) und \( \ln(1+p/100) \approx p/100 \) für kleine \(p\).</p>''')
    + loes(6, r'''    <p>(a) \( \dfrac{U}{9} = e^{-t/3} \Rightarrow t = -3 \ln\dfrac{U}{9} = 3 \ln\dfrac{9}{U} \).</p>
    <p>(b) \( t = 3 \ln\dfrac{9}{0.5} = 3 \ln 18 \approx 8.67 \) s.</p>
    <p>(c) \( U(t) \) ist eine fallende Exponentialkurve mit Asymptote \( U = 0 \); die
    Umkehrfunktion \( t(U) \) ist eine Logarithmuskurve mit vertikaler Asymptote \( U = 0 \) —
    gespiegelt an der Winkelhalbierenden.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-5  TRIGONOMETRISCHE FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════

F_HANDOUT = r'''
  <h2>1. Definition</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Trigonometrische Funktionen</div>
    <p>Am Einheitskreis gehört zu jedem Winkel \(x\) (Bogenmass) ein Punkt \(P\): seine
    \(y\)-Koordinate ist \(\sin x\), seine \(x\)-Koordinate \(\cos x\), der Tangentenabschnitt
    bei \(x = 1\) ist \(\tan x\). Als Funktionen von \(x\) heissen</p>
    \[ f(x) = \sin x, \qquad f(x) = \cos x, \qquad f(x) = \tan x \]
    <p><strong>Sinus-, Cosinus- und Tangensfunktion</strong> (Winkelfunktionen).</p>
  </div>

  <h2>2. Eigenschaften</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( \sin x \)</th><th>\( \cos x \)</th><th>\( \tan x \)</th></tr></thead>
    <tbody>
      <tr><td class="li">Definitionsmenge</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \setminus \{\tfrac{\pi}{2} + k\pi\} \)</td></tr>
      <tr><td class="li">Wertemenge</td><td>\( [-1;\,1] \)</td><td>\( [-1;\,1] \)</td><td>\( \mathbb{R} \)</td></tr>
      <tr><td class="li">Periodenlänge</td><td>\( 2\pi \)</td><td>\( 2\pi \)</td><td>\( \pi \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>\( k\pi \)</td><td>\( \tfrac{\pi}{2} + k\pi \)</td><td>\( k\pi \)</td></tr>
      <tr><td class="li">Symmetrieachsen</td><td>\( x = \tfrac{\pi}{2} + k\pi \)</td><td>\( x = k\pi \)</td><td>—</td></tr>
      <tr><td class="li">Symmetriezentren</td><td>\( (k\pi \mid 0) \)</td><td>\( (\tfrac{\pi}{2} + k\pi \mid 0) \)</td><td>\( (\tfrac{k\pi}{2} \mid 0) \)</td></tr>
      <tr><td class="li">Pole</td><td>—</td><td>—</td><td>\( x = \tfrac{\pi}{2} + k\pi \)</td></tr>
    </tbody>
  </table>
  <p>(jeweils \( k \in \mathbb{Z} \)) Die Tangensfunktion springt an jedem Pol von \(+\infty\)
  nach \(-\infty\); ihre Periode ist nur halb so lang.</p>

  <h2>3. Kongruenz und Beziehungen</h2>
  <p>Sinus- und Cosinuskurve sind <strong>kongruent</strong> — horizontale Verschiebung um \(\tfrac{\pi}{2}\):</p>
  \[ \cos x = \sin\left(x + \tfrac{\pi}{2}\right), \qquad \sin x = \cos\left(x - \tfrac{\pi}{2}\right) \]
  <table class="ftb-tabelle">
    <thead><tr><th>Sinus</th><th>Cosinus</th><th>Tangens</th></tr></thead>
    <tbody>
      <tr><td>\( \sin(\pi - x) = \sin x \)</td><td>\( \cos(\pi - x) = -\cos x \)</td><td>\( \tan(\pi - x) = -\tan x \)</td></tr>
      <tr><td>\( \sin(\pi + x) = -\sin x \)</td><td>\( \cos(\pi + x) = -\cos x \)</td><td>\( \tan(\pi + x) = \tan x \)</td></tr>
      <tr><td>\( \sin(2\pi - x) = -\sin x \)</td><td>\( \cos(2\pi - x) = \cos x \)</td><td>\( \tan(2\pi - x) = -\tan x \)</td></tr>
    </tbody>
  </table>

  <h2>4. Transformationen</h2>
  <p>Ausgangsfunktion \( y = \sin x \), Bildfunktion \( y = a \cdot \sin\bigl(b(x-u)\bigr) + v \)
  (analog für Cosinus und Tangens):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(a\)</td><td class="li">Streckung/Stauchung in \(y\)-Richtung — die <strong>Amplitude</strong></td></tr>
      <tr><td>\(b\)</td><td class="li">Streckung/Stauchung mit Faktor \(\tfrac{1}{b}\) in \(x\)-Richtung — neue Periode \( p = \tfrac{2\pi}{b} \)</td></tr>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung (nach rechts für \(u > 0\))</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung — Mittellinie \( y = v \)</td></tr>
    </tbody>
  </table>
  <p>Negative \(a\), \(b\) sind entbehrlich: \( \sin(-x) = -\sin x = \sin(x - \pi) \).</p>

  <h2>5. Allgemeine Sinusfunktion</h2>
  <div class="block block-def">
    <div class="block-titel">📘 \( y = a \sin(bx + c) \), \( a, b \in \mathbb{R}^+ \), \( c \in \mathbb{R} \)</div>
    <p>Amplitude \(a\), Periodenlänge \( p = \tfrac{2\pi}{b} \), Wertebereich \( -a \leq y \leq a \),
    Verschiebung («Startpunkt») \( x_0 = -\tfrac{c}{b} \). Ausklammern verbindet beide Formen:
    \( a\sin(bx + c) = a\sin\bigl(b(x + \tfrac{c}{b})\bigr) \).</p>
  </div>

  <h2>6. Harmonische Schwingungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 \( y = f(t) = A \sin(\omega t + \varphi) \)</div>
    <p>Amplitude \(A\), Kreisfrequenz \(\omega\) [rad/s], Phasenwinkel \(\varphi\) (Bogenmass).
    Periodendauer \( T = \tfrac{2\pi}{\omega} \), Frequenz \( f = \tfrac{1}{T} = \tfrac{\omega}{2\pi} \)
    [Hz], Phasenverschiebung \( t_0 = -\tfrac{\varphi}{\omega} \). Es gilt \( \omega = 2\pi f \).</p>
  </div>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Sinus und Cosinus pendeln mit Periode \(2\pi\) zwischen \(-1\) und \(1\) und sind kongruent;
    der Tangens hat Periode \(\pi\) und Pole. In \( a\sin\bigl(b(x-u)\bigr) + v \) bestimmt \(a\) die
    Amplitude und \(b\) die Periode \( \tfrac{2\pi}{b} \) — zeitabhängig beschreibt dieselbe Form
    als \( A\sin(\omega t + \varphi) \) jede harmonische Schwingung.</p>
  </div>
'''

F_FORMELAUSZUG = r'''
  <h2>1. Die drei Winkelfunktionen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( \sin x \)</th><th>\( \cos x \)</th><th>\( \tan x \)</th></tr></thead>
    <tbody>
      <tr><td class="li">am Einheitskreis</td><td class="li">\(y\)-Koordinate von \(P\)</td><td class="li">\(x\)-Koordinate von \(P\)</td><td class="li">Tangentenabschnitt</td></tr>
      <tr><td class="li">\(D\)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \setminus \{\tfrac{\pi}{2} + k\pi\} \)</td></tr>
      <tr><td class="li">\(W\)</td><td>\( [-1;\,1] \)</td><td>\( [-1;\,1] \)</td><td>\( \mathbb{R} \)</td></tr>
      <tr><td class="li">Periode</td><td>\( 2\pi \)</td><td>\( 2\pi \)</td><td>\( \pi \)</td></tr>
      <tr><td class="li">Nullstellen</td><td>\( k\pi \)</td><td>\( \tfrac{\pi}{2} + k\pi \)</td><td>\( k\pi \)</td></tr>
      <tr><td class="li">Symmetrie</td><td class="li">ungerade (Punkt)</td><td class="li">gerade (Achse)</td><td class="li">ungerade (Punkt)</td></tr>
    </tbody>
  </table>

  <h2>2. Kongruenz und Beziehungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Kongruenz</td><td>\( \cos x = \sin(x + \tfrac{\pi}{2}), \quad \sin x = \cos(x - \tfrac{\pi}{2}) \)</td></tr>
      <tr><td class="li">Ergänzung auf \(\pi\)</td><td>\( \sin(\pi - x) = \sin x, \quad \cos(\pi - x) = -\cos x \)</td></tr>
      <tr><td class="li">Verschiebung um \(\pi\)</td><td>\( \sin(\pi + x) = -\sin x, \quad \tan(\pi + x) = \tan x \)</td></tr>
      <tr><td class="li">negatives Argument</td><td>\( \sin(-x) = -\sin x, \quad \cos(-x) = \cos x \)</td></tr>
    </tbody>
  </table>

  <h2>3. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = a \cdot \sin\bigl(b(x-u)\bigr) + v \)</td></tr>
      <tr><td class="li">Amplitude</td><td>\( a \)</td></tr>
      <tr><td class="li">Periodenlänge</td><td>\( p = \dfrac{2\pi}{b} \)</td></tr>
      <tr><td class="li">Mittellinie</td><td>\( y = v \)</td></tr>
      <tr><td class="li">Wertebereich</td><td>\( v - a \leq y \leq v + a \)</td></tr>
    </tbody>
  </table>

  <h2>4. Allgemeine Sinusfunktion</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Form</td><td>\( y = a \sin(bx + c), \quad a, b \in \mathbb{R}^+ \)</td></tr>
      <tr><td class="li">Verschiebung («Startpunkt»)</td><td>\( x_0 = -\dfrac{c}{b} \)</td></tr>
      <tr><td class="li">Umrechnung</td><td>\( a\sin(bx + c) = a\sin\bigl(b(x + \tfrac{c}{b})\bigr) \)</td></tr>
    </tbody>
  </table>

  <h2>5. Harmonische Schwingungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Form</td><td>\( y = A \sin(\omega t + \varphi) \)</td></tr>
      <tr><td class="li">Periodendauer</td><td>\( T = \dfrac{2\pi}{\omega} \)</td></tr>
      <tr><td class="li">Frequenz</td><td>\( f = \dfrac{1}{T} = \dfrac{\omega}{2\pi} \) [Hz], \( 1\ \text{Hz} = 1\ \text{s}^{-1} \)</td></tr>
      <tr><td class="li">Kreisfrequenz</td><td>\( \omega = 2\pi f = \dfrac{2\pi}{T} \) [rad/s]</td></tr>
      <tr><td class="li">Phasenverschiebung</td><td>\( t_0 = -\dfrac{\varphi}{\omega} \)</td></tr>
    </tbody>
  </table>

  <h2>6. Hoch- und Tiefpunkte finden</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Funktion</th><th>Hochpunkt: Argument =</th><th>Tiefpunkt: Argument =</th></tr></thead>
    <tbody>
      <tr><td class="li">Sinus</td><td>\( \tfrac{\pi}{2} + 2k\pi \)</td><td>\( \tfrac{3\pi}{2} + 2k\pi \)</td></tr>
      <tr><td class="li">Cosinus</td><td>\( 2k\pi \)</td><td>\( \pi + 2k\pi \)</td></tr>
    </tbody>
  </table>
'''

F_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Am Einheitskreis ist \( \sin x \) die <span class="lueck"></span>-Koordinate des Punktes \(P\).<br>
      Sinus und Cosinus haben die Periodenlänge <span class="lueck"></span>,<br>
      die Tangensfunktion hat die Periodenlänge <span class="lueck"></span>
      und Pole bei \( x = \) <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Werte ohne Taschenrechner', 1, r'''    <p>Gib exakt an:</p>
    <p>(a) \( \sin\tfrac{\pi}{2} \) &nbsp;&nbsp; (b) \( \cos \pi \) &nbsp;&nbsp;
       (c) \( \tan 0 \) &nbsp;&nbsp; (d) \( \sin\tfrac{\pi}{6} \)</p>
''' + LINS)
    + aufg(3, 'Steckbrief ausfüllen', 1, r'''    <p>Gib Definitionsmenge, Wertemenge und Periodenlänge an:</p>
    <p>(a) \( y = \sin x \) &nbsp;&nbsp;&nbsp; (b) \( y = \tan x \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Eigenschaften</div>\n'
    + aufg(4, 'Nullstellen', 2, r'''    <p>Gib alle Nullstellen der Cosinusfunktion an (mit \( k \in \mathbb{Z} \)).</p>
''' + LINS)
    + aufg(5, 'Symmetrie', 2, r'''    <p>Zeige mit der Bedingung \( f(-x) = \pm f(x) \): Die Sinusfunktion ist ungerade,
    die Cosinusfunktion gerade.</p>
''' + LINS)
    + aufg(6, 'Terme vereinfachen', 2, r'''    <p>Vereinfache mithilfe der Symmetrie-Beziehungen:</p>
    <p>(a) \( \sin(\pi - x) \) &nbsp;&nbsp;&nbsp; (b) \( \cos(\pi + x) + \cos x \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(7, 'Kenngrössen ablesen', 2, r'''    <p>Gib Amplitude, Periodenlänge und Mittellinie von \( y = 4\sin(2x) - 1 \) an.</p>
''' + LINS)
    + aufg(8, 'Periode berechnen', 1, r'''    <p>Welche Periodenlänge hat \( y = \cos\left(\tfrac{1}{2}x\right) \)?</p>
''' + LINS)
    + aufg(9, 'Verschiebung erkennen', 2, r'''    <p>Wie geht der Graph von \( y = \sin\left(x - \tfrac{\pi}{3}\right) \) aus dem Graphen
    von \( y = \sin x \) hervor? Wo liegt seine erste positive Nullstelle?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Parameter bestimmen</div>\n'
    + aufg(10, 'Allgemeine Sinusfunktion', 2, r'''    <p>Gegeben ist \( y = 2\sin\left(\tfrac{\pi}{4}x - \tfrac{\pi}{2}\right) \). Bestimme die
    Periodenlänge \(p\) und die Verschiebung \(x_0\).</p>
''' + LINS)
    + aufg(11, 'Gleichung aus Kenngrössen', 3, r'''    <p>Eine Sinuskurve durch den Ursprung (steigend) hat die Amplitude \(3\) und die
    Periodenlänge \(\pi\). Gib die Funktionsgleichung an.</p>
''' + LINS)
    + aufg(12, 'Kongruenz anwenden', 3, r'''    <p>Schreibe \( y = \cos x \) als verschobene Sinusfunktion und begründe mit dem
    Einheitskreis oder den Graphen.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\( \sin x \) ist die <strong>\(y\)</strong>-Koordinate von \(P\). Periode von Sinus und
    Cosinus: <strong>\(2\pi\)</strong>; Tangens: <strong>\(\pi\)</strong>, Pole bei
    \( x = \tfrac{\pi}{2} + k\pi \).</p>''')
    + loes(2, r'''    <p>(a) \(1\) · (b) \(-1\) · (c) \(0\) · (d) \(\tfrac{1}{2}\).</p>''')
    + loes(3, r'''    <p>(a) \( D = \mathbb{R} \), \( W = [-1;\,1] \), \( p = 2\pi \) ·
    (b) \( D = \mathbb{R} \setminus \{\tfrac{\pi}{2} + k\pi\} \), \( W = \mathbb{R} \), \( p = \pi \).</p>''')
    + loes(4, r'''    <p>\( x_0 = \tfrac{\pi}{2} + k\pi \), \( k \in \mathbb{Z} \) — versetzt zu den
    Sinus-Nullstellen \( k\pi \).</p>''')
    + loes(5, r'''    <p>\( \sin(-x) = -\sin x \) (Punktsymmetrie zum Ursprung → ungerade);
    \( \cos(-x) = \cos x \) (Achsensymmetrie zur \(y\)-Achse → gerade) — am Einheitskreis:
    Spiegeln von \(P\) an der \(x\)-Achse wechselt das Vorzeichen der \(y\)-Koordinate,
    nicht aber das der \(x\)-Koordinate.</p>''')
    + loes(6, r'''    <p>(a) \( \sin(\pi - x) = \sin x \) ·
    (b) \( \cos(\pi + x) + \cos x = -\cos x + \cos x = 0 \).</p>''')
    + loes(7, r'''    <p>Amplitude \(4\); Periode \( p = \tfrac{2\pi}{2} = \pi \); Mittellinie \( y = -1 \)
    (Kurve pendelt zwischen \(-5\) und \(3\)).</p>''')
    + loes(8, r'''    <p>\( p = \dfrac{2\pi}{1/2} = 4\pi \) — kleines \(b\) heisst lange Periode.</p>''')
    + loes(9, r'''    <p>Verschiebung um \( \tfrac{\pi}{3} \) <strong>nach rechts</strong>; die Nullstelle wandert
    von \(0\) zu \( x = \tfrac{\pi}{3} \).</p>''')
    + loes(10, r'''    <p>\( b = \tfrac{\pi}{4} \Rightarrow p = \tfrac{2\pi}{\pi/4} = 8 \);
    \( x_0 = -\tfrac{c}{b} = \tfrac{\pi/2}{\pi/4} = 2 \) (nach rechts).</p>''')
    + loes(11, r'''    <p>Amplitude \( a = 3 \); \( p = \pi \Rightarrow b = \tfrac{2\pi}{p} = 2 \):
    \( y = 3\sin(2x) \).</p>''')
    + loes(12, r'''    <p>\( \cos x = \sin\left(x + \tfrac{\pi}{2}\right) \) — die Cosinuskurve ist die um
    \( \tfrac{\pi}{2} \) nach links verschobene Sinuskurve. Am Einheitskreis: Die \(x\)-Koordinate
    von \(P(x)\) ist gleich der \(y\)-Koordinate des um \( \tfrac{\pi}{2} \) weitergedrehten
    Punktes.</p>''')
)

F_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Taschenrechner im RAD-Modus!
    Alle Graphen mit beschrifteten Achsen (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Elektrotechnik</td><td>Netzspannung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Geografie</td><td>Gezeiten</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Mechanik</td><td>Federpendel</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Akustik</td><td>Kammerton a</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Astronomie</td><td>Tageslänge im Jahresverlauf</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Mechanik</td><td>Sekundenpendel</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Netzspannung', 2, r'''    <p>Die Spannung im Stromnetz verläuft sinusförmig: \( U(t) = 325 \cdot \sin(100\pi\, t) \)
    (\(U\) in Volt, \(t\) in Sekunden).</p>
    <p>(a) Gib Amplitude, Periodendauer und Frequenz an.</p>
    <p>(b) Berechne die Spannung zum Zeitpunkt \( t = 0.002 \) s.</p>
    <p>(c) Die Netzspannung wird mit «230 V» angegeben, die Amplitude beträgt aber 325 V.
    Woran könnte das liegen? (Stichwort: Effektivwert — keine Rechnung verlangt.)</p>
''' + LINS4, tag='Elektrotechnik')
    + aufg(2, 'Gezeiten', 2, r'''    <p>In einem Hafen schwankt der Wasserstand näherungsweise sinusförmig:
    \( h(t) = 5 + 3 \cdot \sin\left(\tfrac{2\pi}{12.4}\, t\right) \) (\(h\) in m, \(t\) in Stunden
    seit Mittelwasser bei steigender Flut).</p>
    <p>(a) Gib mittleren Wasserstand, Tidenhub (Differenz Hoch-/Niedrigwasser) und Periode an.</p>
    <p>(b) Berechne den Wasserstand nach \( 3.1 \) Stunden.</p>
    <p>(c) Wie viele Stunden nach \( t = 0 \) tritt das erste Niedrigwasser ein?</p>
''' + LINS4, tag='Geografie')
    + aufg(3, 'Federpendel', 2, r'''    <p>Eine Masse an einer Feder schwingt harmonisch: \( y(t) = 8 \cdot \sin(4\pi\, t) \)
    (\(y\) in cm, \(t\) in s).</p>
    <p>(a) Gib Amplitude, Kreisfrequenz, Periodendauer und Frequenz an.</p>
    <p>(b) Berechne die Auslenkung nach \( 0.1 \) s.</p>
    <p>(c) Zu welchen Zeitpunkten ist die Auslenkung maximal?</p>
''' + LINS4, tag='Mechanik')
    + aufg(4, 'Kammerton a', 3, r'''    <p>Der Kammerton a ist eine Schallschwingung mit der Frequenz \( f = 440 \) Hz.</p>
    <p>(a) Berechne Periodendauer und Kreisfrequenz.</p>
    <p>(b) Gib die Funktionsgleichung \( p(t) = A \sin(\omega t) \) für die Amplitude
    \( A = 0.2 \) Pa an.</p>
    <p>(c) Die Oktave darüber hat die doppelte Frequenz. Wie ändern sich \(T\) und \(\omega\)?</p>
''' + LINS4, tag='Akustik')
    + aufg(5, 'Tageslänge im Jahresverlauf', 3, r'''    <p>Die Tageslänge (Sonnenaufgang bis -untergang) lässt sich näherungsweise beschreiben durch
    \( L(d) = 12.2 + 4.3 \cdot \sin\left(\tfrac{2\pi}{365}(d - 80)\right) \)
    (\(L\) in Stunden, \(d\): Tag des Jahres).</p>
    <p>(a) Gib den kürzesten und den längsten Tag (Stundenzahl) sowie die Periode an.</p>
    <p>(b) An welchem Tag \(d\) ist der Tag am längsten?</p>
    <p>(c) Berechne die Tageslänge am Tag \( d = 355 \) (21. Dezember).</p>
''' + LINS4, tag='Astronomie')
    + aufg(6, 'Sekundenpendel', 3, r'''    <p>Ein Uhrenpendel schwingt mit Periodendauer \( T = 2 \) s und maximaler Auslenkung
    \( 3 \) cm. Beim Start (\( t = 0 \)) ist die Auslenkung maximal.</p>
    <p>(a) Bestimme \(\omega\) und den Phasenwinkel \(\varphi\) in \( x(t) = A\sin(\omega t + \varphi) \).</p>
    <p>(b) Zeige, dass sich die Schwingung auch als \( x(t) = 3\cos(\pi t) \) schreiben lässt.</p>
    <p>(c) Wo befindet sich das Pendel bei \( t = 0.5 \) s und bei \( t = 1 \) s?</p>
''' + LINS4, tag='Mechanik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) Amplitude \( 325 \) V; \( \omega = 100\pi \Rightarrow T = \tfrac{2\pi}{100\pi} = 0.02 \) s;
    \( f = \tfrac{1}{T} = 50 \) Hz.</p>
    <p>(b) \( U(0.002) = 325\sin(0.2\pi) \approx 191 \) V.</p>
    <p>(c) 230 V ist der <em>Effektivwert</em> — ein zeitlicher Mittelwert der Leistung; die
    Spitzenspannung (Amplitude) ist um den Faktor \( \sqrt{2} \) grösser: \( 230 \cdot \sqrt{2} \approx 325 \) V.</p>''')
    + loes(2, r'''    <p>(a) Mittelwasser \( 5 \) m; Tidenhub \( 2 \cdot 3 = 6 \) m; Periode \( 12.4 \) h.</p>
    <p>(b) \( t = 3.1 = \tfrac{12.4}{4} \): Argument \( = \tfrac{\pi}{2} \), also
    \( h = 5 + 3 = 8 \) m — Hochwasser.</p>
    <p>(c) Niedrigwasser beim Argument \( \tfrac{3\pi}{2} \): \( t = \tfrac{3}{4} \cdot 12.4 = 9.3 \) h.</p>''')
    + loes(3, r'''    <p>(a) \( A = 8 \) cm; \( \omega = 4\pi \approx 12.57\ \text{s}^{-1} \);
    \( T = \tfrac{2\pi}{4\pi} = 0.5 \) s; \( f = 2 \) Hz.</p>
    <p>(b) \( y(0.1) = 8\sin(0.4\pi) \approx 7.61 \) cm.</p>
    <p>(c) Beim Argument \( \tfrac{\pi}{2} + 2k\pi \): \( t = 0.125 + 0.5k \) s (\( k \in \mathbb{N}_0 \)).</p>''')
    + loes(4, r'''    <p>(a) \( T = \tfrac{1}{440} \approx 0.00227 \) s; \( \omega = 2\pi \cdot 440 \approx 2765\ \text{rad/s} \).</p>
    <p>(b) \( p(t) = 0.2 \cdot \sin(2765\, t) \) [Pa].</p>
    <p>(c) Doppelte Frequenz (880 Hz): \(T\) halbiert sich, \(\omega\) verdoppelt sich
    (\( \omega \approx 5529\ \text{rad/s} \)).</p>''')
    + loes(5, r'''    <p>(a) Kürzester Tag \( 12.2 - 4.3 = 7.9 \) h, längster \( 12.2 + 4.3 = 16.5 \) h;
    Periode \( 365 \) Tage.</p>
    <p>(b) Maximum beim Argument \( \tfrac{\pi}{2} \): \( d = 80 + \tfrac{365}{4} \approx 171 \)
    (etwa 20. Juni — Sommersonnenwende).</p>
    <p>(c) \( L(355) = 12.2 + 4.3\sin\left(\tfrac{2\pi \cdot 275}{365}\right) \approx 7.9 \) h —
    der kürzeste Tag.</p>''')
    + loes(6, r'''    <p>(a) \( \omega = \tfrac{2\pi}{T} = \pi\ \text{s}^{-1} \); Start am Maximum:
    \( \sin\varphi = 1 \Rightarrow \varphi = \tfrac{\pi}{2} \); also
    \( x(t) = 3\sin\left(\pi t + \tfrac{\pi}{2}\right) \).</p>
    <p>(b) Kongruenz: \( \sin\left(x + \tfrac{\pi}{2}\right) = \cos x \), also
    \( x(t) = 3\cos(\pi t) \).</p>
    <p>(c) \( x(0.5) = 3\cos\tfrac{\pi}{2} = 0 \) (Nulldurchgang);
    \( x(1) = 3\cos\pi = -3 \) cm (Gegenseite, maximal ausgelenkt).</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-1  GRUNDLAGEN (WERKZEUGKASTEN FUNKTIONEN)
# ═══════════════════════════════════════════════════════════════════

G_HANDOUT = r'''
  <h2>1. Elementare Funktionen — die Grundgraphen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Funktion</th><th>\(D\)</th><th>\(W\)</th><th>markante Punkte</th><th>Besonderes</th></tr></thead>
    <tbody>
      <tr><td>\( x \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td><td>\( (0 \mid 0) \)</td><td class="li">Gerade, ungerade Funktion</td></tr>
      <tr><td>\( x^2 \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( (0 \mid 0),\ (\pm 1 \mid 1) \)</td><td class="li">Normalparabel, gerade Funktion</td></tr>
      <tr><td>\( x^3 \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R} \)</td><td>\( (0 \mid 0),\ (\pm 1 \mid \pm 1) \)</td><td class="li">ungerade, Terrassenpunkt</td></tr>
      <tr><td>\( \sqrt{x} \)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( (0 \mid 0),\ (1 \mid 1) \)</td><td class="li">Umkehrfunktion von \(x^2\)</td></tr>
      <tr><td>\( \tfrac{1}{x} \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td><td>\( (\pm 1 \mid \pm 1) \)</td><td class="li">Hyperbel, Asymptoten \(x = 0\), \(y = 0\)</td></tr>
      <tr><td>\( a^x \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}^+ \)</td><td>\( (0 \mid 1),\ (1 \mid a) \)</td><td class="li">Asymptote \(y = 0\)</td></tr>
      <tr><td>\( \log_a x \)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R} \)</td><td>\( (1 \mid 0) \)</td><td class="li">Asymptote \(x = 0\)</td></tr>
      <tr><td>\( \sin x \)</td><td>\( \mathbb{R} \)</td><td>\( [-1;\,1] \)</td><td>\( (0 \mid 0),\ (\tfrac{\pi}{2} \mid 1) \)</td><td class="li">periodisch (\(2\pi\)), ungerade</td></tr>
    </tbody>
  </table>

  <h2>2. Transformationen</h2>
  <p>Aus jeder Grundfunktion \(f\) entsteht die Familie \( y = a \cdot f(x-u) + v \):</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Parameter</th><th>Wirkung</th></tr></thead>
    <tbody>
      <tr><td>\(u\)</td><td class="li">Verschiebung in \(x\)-Richtung (nach rechts für \(u > 0\))</td></tr>
      <tr><td>\(v\)</td><td class="li">Verschiebung in \(y\)-Richtung (nach oben für \(v > 0\))</td></tr>
      <tr><td>\(|a|\)</td><td class="li">Streckung (\(|a| > 1\)) bzw. Stauchung (\(|a| < 1\)) in \(y\)-Richtung</td></tr>
      <tr><td>\(a < 0\)</td><td class="li">zusätzlich Spiegelung an der \(x\)-Achse</td></tr>
    </tbody>
  </table>
  <p>Die Ersetzung \( x \to -x \) spiegelt an der \(y\)-Achse. Markante Punkte und Asymptoten
  wandern mit; \((x-3)\) verschiebt nach <strong>rechts</strong>, nicht nach links!</p>

  <h2>3. Schnittpunkte zweier Graphen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Verfahren</div>
    <p><strong>Gleichsetzen → lösen → einsetzen:</strong> \( f(x) = g(x) \) liefert die
    Schnittstellen \(x_i\); Einsetzen in \(f\) oder \(g\) die Schnittpunkte
    \( S_i = (x_i \mid f(x_i)) \). Grafisch: die Kreuzungspunkte der Kurven.</p>
  </div>

  <h2>4. Gleichungen und Ungleichungen am Graphen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Algebra</th><th>Bild am Graphen</th><th>Lösungsmenge</th></tr></thead>
    <tbody>
      <tr><td>\( f(x) = g(x) \)</td><td class="li">Kurven kreuzen sich</td><td class="li">einzelne Schnittstellen</td></tr>
      <tr><td>\( f(x) > g(x) \)</td><td class="li">Kurve von \(f\) liegt oberhalb</td><td class="li">Intervalle</td></tr>
      <tr><td>\( f(x) = 0 \)</td><td class="li">Kurve schneidet die \(x\)-Achse</td><td class="li">Nullstellen</td></tr>
    </tbody>
  </table>
  <p>Die Schnittstellen zerlegen die \(x\)-Achse in Abschnitte — ein <strong>Testwert pro
  Abschnitt</strong> entscheidet, wo die Ungleichung gilt. Randpunkte gehören nur bei
  \(\geq\)/\(\leq\) dazu.</p>

  <h2>5. Extremwertaufgaben</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Strategie</div>
    <p>(1) <strong>Zielgrösse</strong> festlegen · (2) <strong>Nebenbedingung</strong> aufschreiben ·
    (3) einsetzen → Zielfunktion mit einer Variablen (Definitionsbereich!) ·
    (4) Extremum über die <strong>Scheitelform</strong> \( a(x-u)^2 + v \) (Scheitel \((u \mid v)\))
    oder grafisch bestimmen.</p>
  </div>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Grundgraphen kennen, mit \( a \cdot f(x-u) + v \) transformieren, Schnittpunkte durch
    Gleichsetzen, Ungleichungen als «oberhalb/unterhalb»-Frage, Extremwerte über Zielfunktion +
    Nebenbedingung. Die Skizze zuerst — sie verrät Anzahl und Lage der Lösungen.</p>
  </div>
'''

G_FORMELAUSZUG = r'''
  <h2>1. Transformationen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bildfunktion</td><td>\( y = a \cdot f(x-u) + v \)</td></tr>
      <tr><td class="li">Verschiebung</td><td>\(u\) in \(x\)-Richtung (rechts für \(u > 0\)), \(v\) in \(y\)-Richtung</td></tr>
      <tr><td class="li">Streckung / Spiegelung</td><td>\(|a|\) in \(y\)-Richtung; \(a < 0\): Spiegelung an der \(x\)-Achse</td></tr>
      <tr><td class="li">Spiegelung an der \(y\)-Achse</td><td>\( y = f(-x) \)</td></tr>
    </tbody>
  </table>

  <h2>2. Grundgraphen-Kenndaten</h2>
  <table class="ftb-tabelle">
    <thead><tr><th></th><th>\( x^2 \)</th><th>\( \sqrt{x} \)</th><th>\( \tfrac{1}{x} \)</th><th>\( a^x \)</th><th>\( \log_a x \)</th><th>\( \sin x \)</th></tr></thead>
    <tbody>
      <tr><td class="li">\(D\)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td><td>\( \mathbb{R} \)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R} \)</td></tr>
      <tr><td class="li">\(W\)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( \mathbb{R}_0^+ \)</td><td>\( \mathbb{R} \setminus \{0\} \)</td><td>\( \mathbb{R}^+ \)</td><td>\( \mathbb{R} \)</td><td>\( [-1;\,1] \)</td></tr>
      <tr><td class="li">Punkt</td><td>\( (0 \mid 0) \)</td><td>\( (0 \mid 0) \)</td><td>\( (1 \mid 1) \)</td><td>\( (0 \mid 1) \)</td><td>\( (1 \mid 0) \)</td><td>\( (0 \mid 0) \)</td></tr>
      <tr><td class="li">Asymptoten</td><td>—</td><td>—</td><td>\( x = 0,\ y = 0 \)</td><td>\( y = 0 \)</td><td>\( x = 0 \)</td><td>—</td></tr>
    </tbody>
  </table>

  <h2>3. Schnittpunkte</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Verfahren</td><td class="li">gleichsetzen → lösen → einsetzen</td></tr>
      <tr><td class="li">Schnittstellen</td><td>Lösungen von \( f(x) = g(x) \)</td></tr>
      <tr><td class="li">Schnittpunkte</td><td>\( S_i = \bigl(x_i \mid f(x_i)\bigr) \)</td></tr>
    </tbody>
  </table>

  <h2>4. Un-/Gleichungen grafisch</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( f(x) = g(x) \)</td><td class="li">Schnittstellen der Kurven</td></tr>
      <tr><td class="li">\( f(x) > g(x) \)</td><td class="li">Kurve von \(f\) oberhalb — Lösungsmenge sind Intervalle</td></tr>
      <tr><td class="li">Testwert-Methode</td><td class="li">Schnittstellen zerlegen die Achse; ein Testwert pro Abschnitt</td></tr>
      <tr><td class="li">Monotonie-Argument</td><td class="li">streng steigend gegen streng fallend → höchstens ein Schnitt</td></tr>
    </tbody>
  </table>

  <h2>5. Extremwertaufgaben</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Schritte</td><td class="li">Zielgrösse → Nebenbedingung → einsetzen → Extremum</td></tr>
      <tr><td class="li">Scheitelform</td><td>\( y = a(x-u)^2 + v \) — Scheitel \( S = (u \mid v) \)</td></tr>
      <tr><td class="li">Maximum / Minimum</td><td>\( a < 0 \): Maximum \(v\) · \( a > 0 \): Minimum \(v\)</td></tr>
    </tbody>
  </table>
'''

G_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Transformationsschema vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      In \( y = a \cdot f(x-u) + v \) verschiebt \(u\) den Graphen in <span class="lueck"></span>-Richtung,<br>
      \(v\) in <span class="lueck"></span>-Richtung, \(|a|\) <span class="lueck"></span> in \(y\)-Richtung,<br>
      und \( a < 0 \) spiegelt an der <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Definitionsmengen der Grundfunktionen', 1, r'''    <p>Gib die Definitionsmenge an:</p>
    <p>(a) \( y = \sqrt{x} \) &nbsp;&nbsp; (b) \( y = \dfrac{1}{x} \) &nbsp;&nbsp; (c) \( y = \ln x \)</p>
''' + LINS)
    + aufg(3, 'Markante Punkte', 1, r'''    <p>Durch welchen Punkt laufen <em>alle</em> Kurven der Familie?</p>
    <p>(a) \( y = a^x \) &nbsp;&nbsp; (b) \( y = \log_a x \) &nbsp;&nbsp; (c) \( y = x^n \) (\(n\) ungerade)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(4, 'Scheitel ablesen', 1, r'''    <p>Gib den Scheitelpunkt von \( y = 3(x+2)^2 - 7 \) an.</p>
''' + LINS)
    + aufg(5, 'Gleichung aus Beschreibung', 2, r'''    <p>Die Normalparabel wird um \(1\) nach rechts und \(4\) nach unten verschoben.
    Gib die Funktionsgleichung an und berechne die Nullstellen.</p>
''' + LINS)
    + aufg(6, 'Spiegelungen unterscheiden', 2, r'''    <p>Was bewirkt jeweils die Umformung am Graphen von \( y = f(x) \)?</p>
    <p>(a) \( y = -f(x) \) &nbsp;&nbsp;&nbsp; (b) \( y = f(-x) \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Schnittpunkte und Ungleichungen</div>\n'
    + aufg(7, 'Schnittpunkt zweier Geraden', 2, r'''    <p>Berechne den Schnittpunkt von \( y = x + 2 \) und \( y = 3x - 4 \).</p>
''' + LINS)
    + aufg(8, 'Gerade schneidet Parabel', 2, r'''    <p>Berechne die Schnittstellen von \( f(x) = x^2 \) und \( g(x) = 2x + 3 \).</p>
''' + LINS)
    + aufg(9, 'Ungleichung grafisch', 2, r'''    <p>Für welche \(x\) gilt \( x^2 < 4 \)? Argumentiere am Graphen der Normalparabel
    und der Geraden \( y = 4 \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Nullstellen und Extremwerte</div>\n'
    + aufg(10, 'Nullstellen einer verschobenen Parabel', 2, r'''    <p>Berechne die Nullstellen von \( y = (x+2)^2 - 9 \).</p>
''' + LINS)
    + aufg(11, 'Extremwertaufgabe', 3, r'''    <p>Ein Rechteck hat den Umfang \(40\) cm. Welche Seitenlängen maximieren den
    Flächeninhalt? Stelle die Zielfunktion auf und nutze die Scheitelform.</p>
''' + LINS)
    + aufg(12, 'Monotonie-Argument', 3, r'''    <p>Begründe ohne Rechnung, dass die Gleichung \( 3^x = -1 \) keine Lösung hat —
    und dass \( 3^x = 5 - x \) genau eine hat.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p>\(u\): <strong>\(x\)</strong>-Richtung · \(v\): <strong>\(y\)</strong>-Richtung ·
    \(|a|\): <strong>streckt/staucht</strong> · \(a < 0\): Spiegelung an der <strong>\(x\)-Achse</strong>.</p>''')
    + loes(2, r'''    <p>(a) \( D = \mathbb{R}_0^+ \) · (b) \( D = \mathbb{R} \setminus \{0\} \) ·
    (c) \( D = \mathbb{R}^+ \).</p>''')
    + loes(3, r'''    <p>(a) \( (0 \mid 1) \), denn \( a^0 = 1 \) · (b) \( (1 \mid 0) \), denn \( \log_a 1 = 0 \) ·
    (c) \( (0 \mid 0) \), \( (1 \mid 1) \) und \( (-1 \mid -1) \).</p>''')
    + loes(4, r'''    <p>\( x + 2 = x - (-2) \), also \( S = (-2 \mid -7) \).</p>''')
    + loes(5, r'''    <p>\( y = (x-1)^2 - 4 \). Nullstellen: \( (x-1)^2 = 4 \Rightarrow x - 1 = \pm 2
    \Rightarrow x_1 = -1,\ x_2 = 3 \).</p>''')
    + loes(6, r'''    <p>(a) Spiegelung an der <strong>\(x\)-Achse</strong> (alle Funktionswerte wechseln das
    Vorzeichen) · (b) Spiegelung an der <strong>\(y\)-Achse</strong> (der Graph wird seitenverkehrt).</p>''')
    + loes(7, r'''    <p>\( x + 2 = 3x - 4 \Rightarrow 2x = 6 \Rightarrow x = 3 \); \( y = 5 \):
    \( S = (3 \mid 5) \).</p>''')
    + loes(8, r'''    <p>\( x^2 = 2x + 3 \Rightarrow x^2 - 2x - 3 = 0 \Rightarrow (x+1)(x-3) = 0
    \Rightarrow x_1 = -1,\ x_2 = 3 \).</p>''')
    + loes(9, r'''    <p>Die Parabel liegt zwischen den Schnittstellen \( \pm 2 \) unterhalb der Geraden:
    \( L = \{x \mid -2 < x < 2\} \) — Randpunkte ausgeschlossen (striktes «kleiner»).</p>''')
    + loes(10, r'''    <p>\( (x+2)^2 = 9 \Rightarrow x + 2 = \pm 3 \Rightarrow x_1 = -5,\ x_2 = 1 \).</p>''')
    + loes(11, r'''    <p>Nebenbedingung \( 2x + 2y = 40 \Rightarrow y = 20 - x \). Zielfunktion
    \( A(x) = x(20-x) = -(x-10)^2 + 100 \) — Maximum bei \( x = y = 10 \) cm, \( A = 100\ \text{cm}^2 \):
    Das Quadrat ist das flächengrösste Rechteck bei festem Umfang.</p>''')
    + loes(12, r'''    <p>\( 3^x > 0 \) für alle \(x\) — die Kurve erreicht \(-1\) nie. Bei \( 3^x = 5 - x \)
    ist die linke Seite streng steigend, die rechte streng fallend: höchstens ein Schnitt; da
    für \( x = 0 \) die Gerade oben liegt (\(1 < 5\)) und für \( x = 2 \) die Exponentialkurve
    (\(9 > 3\)), gibt es genau eine Lösung dazwischen.</p>''')
)

G_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Alle Graphen mit beschrifteten Achsen
    (Grösse und Einheit) skizzieren.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Architektur</td><td>Brückenbogen</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Sport / Physik</td><td>Ballwurf</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Betriebswirtschaft</td><td>Break-even-Analyse</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Bauplanung</td><td>Fensterrahmen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Energie</td><td>Stromtarife vergleichen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Mathematik</td><td>Parabel trifft Exponentialkurve</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Brückenbogen', 2, r'''    <p>Ein parabelförmiger Brückenbogen wird beschrieben durch \( y = 4 - 0.1\,x^2 \)
    (\(x\), \(y\) in m; \(x = 0\) in der Bogenmitte).</p>
    <p>(a) Wie hoch ist der Bogen in der Mitte, und wie breit ist er am Boden (\(y = 0\))?</p>
    <p>(b) Ein Lastwagen ist \(3\) m hoch. Wie breit ist die Durchfahrt auf dieser Höhe?</p>
    <p>(c) Formuliere Teilaufgabe (b) als Gleichung und als Ungleichung.</p>
''' + LINS4, tag='Architektur')
    + aufg(2, 'Ballwurf', 2, r'''    <p>Die Flugbahn eines Balls: \( h(x) = -0.05\,x^2 + x + 2 \) (\(h\): Höhe in m,
    \(x\): horizontale Entfernung in m).</p>
    <p>(a) Aus welcher Höhe wird der Ball abgeworfen?</p>
    <p>(b) Bestimme den höchsten Punkt der Flugbahn (Scheitelform!).</p>
    <p>(c) In welcher Entfernung landet der Ball (\(h = 0\))?</p>
''' + LINS4, tag='Sport / Physik')
    + aufg(3, 'Break-even-Analyse', 2, r'''    <p>Ein Kleinbetrieb produziert Werkstücke: Fixkosten \(2000\) CHF, variable Kosten
    \(15\) CHF/Stück, Verkaufspreis \(40\) CHF/Stück. Also \( K(x) = 2000 + 15x \) und
    \( E(x) = 40x \).</p>
    <p>(a) Zeichne beide Graphen in ein Koordinatensystem (bis \(x = 150\)).</p>
    <p>(b) Berechne den Break-even-Punkt (\(E = K\)).</p>
    <p>(c) Interpretiere die Bereiche links und rechts davon als Ungleichung.</p>
''' + LINS4, tag='Betriebswirtschaft')
    + aufg(4, 'Fensterrahmen', 3, r'''    <p>Für ein rechteckiges Fenster stehen \(6\) m Rahmenprofil zur Verfügung (alle vier
    Seiten).</p>
    <p>(a) Stelle die Zielfunktion \( A(x) \) für die Glasfläche auf (\(x\): Breite).</p>
    <p>(b) Bestimme die Masse mit maximaler Fläche über die Scheitelform.</p>
    <p>(c) Welche geometrische Form ergibt sich — und wäre das Ergebnis anders, wenn eine
    Seite (z.B. an einer Mauer) kein Profil bräuchte?</p>
''' + LINS4, tag='Bauplanung')
    + aufg(5, 'Stromtarife vergleichen', 3, r'''    <p>Zwei Stromtarife: Grundtarif \( G(x) = 120 + 0.18x \) (Grundgebühr plus
    18 Rp./kWh) und Pauschaltarif \( P(x) = 0.30x \) (30 Rp./kWh, keine Grundgebühr);
    \(x\) in kWh pro Jahr, Kosten in CHF.</p>
    <p>(a) Bei welchem Jahresverbrauch kosten beide gleich viel?</p>
    <p>(b) Formuliere als Ungleichung: Für wen lohnt sich der Pauschaltarif?</p>
    <p>(c) Ein Haushalt verbraucht \(3500\) kWh. Welcher Tarif ist günstiger, und um wie viel?</p>
''' + LINS4, tag='Energie')
    + aufg(6, 'Parabel trifft Exponentialkurve', 3, r'''    <p>Betrachte die Gleichung \( x^2 = 2^x \).</p>
    <p>(a) Skizziere beide Graphen im Intervall \( -2 \leq x \leq 5 \).</p>
    <p>(b) Finde durch Probieren zwei ganzzahlige Lösungen.</p>
    <p>(c) Der Skizze nach gibt es noch eine dritte Lösung. Wo ungefähr liegt sie, und
    warum kann sie nicht ganzzahlig sein?</p>
''' + LINS4, tag='Mathematik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) Mitte: \( y(0) = 4 \) m. Boden: \( 4 - 0.1x^2 = 0 \Rightarrow x = \pm\sqrt{40}
    \approx \pm 6.32 \) — Breite \( \approx 12.6 \) m.</p>
    <p>(b) \( 4 - 0.1x^2 = 3 \Rightarrow x^2 = 10 \Rightarrow x = \pm\sqrt{10} \approx \pm 3.16 \) —
    Durchfahrtsbreite \( \approx 6.3 \) m.</p>
    <p>(c) Gleichung: \( 4 - 0.1x^2 = 3 \) (Grenzfall). Ungleichung: \( 4 - 0.1x^2 > 3 \) —
    dort ist der Bogen höher als der Lastwagen: \( -\sqrt{10} < x < \sqrt{10} \).</p>''')
    + loes(2, r'''    <p>(a) \( h(0) = 2 \) m.</p>
    <p>(b) \( h(x) = -0.05(x^2 - 20x) + 2 = -0.05(x-10)^2 + 7 \) — Hochpunkt \( (10 \mid 7) \):
    nach \(10\) m Distanz, \(7\) m Höhe.</p>
    <p>(c) \( -0.05x^2 + x + 2 = 0 \Rightarrow x^2 - 20x - 40 = 0 \Rightarrow
    x = 10 + \sqrt{140} \approx 21.8 \) m (negative Lösung entfällt).</p>''')
    + loes(3, r'''    <p>(b) \( 40x = 2000 + 15x \Rightarrow 25x = 2000 \Rightarrow x = 80 \) Stück
    (Kosten = Erlös = \(3200\) CHF).</p>
    <p>(c) Für \( x < 80 \) gilt \( E(x) < K(x) \) — Verlustzone (Erlösgerade unterhalb);
    für \( x > 80 \) gilt \( E(x) > K(x) \) — Gewinnzone.</p>''')
    + loes(4, r'''    <p>(a) Nebenbedingung \( 2x + 2y = 6 \Rightarrow y = 3 - x \);
    \( A(x) = x(3-x) \) mit \( 0 < x < 3 \).</p>
    <p>(b) \( A(x) = -(x-1.5)^2 + 2.25 \) — Maximum bei \( x = y = 1.5 \) m,
    \( A = 2.25\ \text{m}^2 \).</p>
    <p>(c) Ein <strong>Quadrat</strong>. Mit einer profillosen Seite (Nebenbedingung
    \( 2x + y = 6 \)) wäre das Optimum ein Rechteck mit \( y = 2x \) — wie beim Weide-Beispiel
    auf der Themenseite.</p>''')
    + loes(5, r'''    <p>(a) \( 120 + 0.18x = 0.30x \Rightarrow 0.12x = 120 \Rightarrow x = 1000 \) kWh
    (beide \(300\) CHF).</p>
    <p>(b) \( P(x) < G(x) \Leftrightarrow x < 1000 \) — der Pauschaltarif lohnt sich für
    <em>Wenigverbraucher</em>.</p>
    <p>(c) \( G(3500) = 120 + 630 = 750 \) CHF, \( P(3500) = 1050 \) CHF — der Grundtarif ist
    \(300\) CHF günstiger.</p>''')
    + loes(6, r'''    <p>(b) \( x = 2 \): \( 4 = 4 \) ✓ und \( x = 4 \): \( 16 = 16 \) ✓.</p>
    <p>(c) Links der \(y\)-Achse: Die Parabel steigt (nach links), die Exponentialkurve fällt
    gegen \(0\) — ein Schnitt bei \( x \approx -0.77 \). Für ganzzahlige negative \(x\) ist
    \( x^2 \geq 1 \), aber \( 2^x \leq \tfrac{1}{2} \) — Gleichheit unmöglich, die Lösung liegt
    zwischen \(-1\) und \(0\).</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s2-2a  POTENZ-, WURZEL- UND RATIONALE GLEICHUNGEN
# ═══════════════════════════════════════════════════════════════════

H_HANDOUT = r'''
  <h2>1. Potenzgleichungen \( x^n = c \)</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Exponent</th><th>\( c > 0 \)</th><th>\( c = 0 \)</th><th>\( c < 0 \)</th></tr></thead>
    <tbody>
      <tr><td class="li">\(n\) gerade</td><td>\( x = \pm\sqrt[n]{c} \) (zwei)</td><td>\( x = 0 \)</td><td class="li">keine Lösung</td></tr>
      <tr><td class="li">\(n\) ungerade</td><td>\( x = \sqrt[n]{c} \) (eine)</td><td>\( x = 0 \)</td><td>\( x = -\sqrt[n]{|c|} \) (eine)</td></tr>
    </tbody>
  </table>

  <h2>2. Wurzelgleichungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Definition und Lösungsmethode</div>
    <p>Die Lösungsvariable steht <strong>unter einer Wurzel</strong>. Verfahren:
    (1) Wurzel <strong>separieren</strong> (bei mehreren Wurzeln: auf beide Seiten verteilen) ·
    (2) <strong>quadrieren</strong> · (3) nötigenfalls wiederholen · (4) wurzelfreie Gleichung lösen ·
    (5) <strong>Kontrolle</strong> in der Ausgangsgleichung.</p>
  </div>
  <p><strong>Quadrieren ist keine Äquivalenzumformung</strong> — es können Scheinlösungen entstehen:
  \( \sqrt{x-3} = -2 \) hat keine Lösung (Wurzelwerte sind nie negativ), quadriert liefert sie aber
  \( x = 7 \). Definitionsmenge: Radikand \( \geq 0 \).</p>

  <h2>3. Substitution</h2>
  <p>Tritt derselbe Wurzelterm mehrfach auf: \( u = \sqrt{T(x)} \) setzen, Gleichung in \(u\) lösen
  (nur \( u \geq 0 \) brauchbar), dann <strong>Rücksubstitution</strong> \( T(x) = u^2 \).</p>

  <h2>4. Rationale Gleichungen (Bruchgleichungen)</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Verfahren</div>
    <p>Die Lösungsvariable steht <strong>im Nenner</strong>. (1) Definitionsmenge: Nenner-Nullstellen
    ausschliessen · (2) mit dem <strong>Hauptnenner</strong> multiplizieren · (3) entstehende lineare
    oder quadratische Gleichung lösen · (4) Lösungen gegen \(D\) prüfen.</p>
  </div>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Die passende <strong>Umkehroperation</strong> löst den Gleichungstyp — aber Quadrieren und
    Hauptnenner-Multiplikation können Scheinlösungen erzeugen: <strong>Definitionsmenge notieren,
    am Schluss kontrollieren.</strong> Gerade Exponenten: an den \(\pm\)-Fall denken.</p>
  </div>
'''

H_FORMELAUSZUG = r'''
  <h2>1. Potenzgleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( x^n = c \), \(n\) ungerade</td><td>genau eine Lösung \( x = \sqrt[n]{c} \) (Vorzeichen bleibt)</td></tr>
      <tr><td class="li">\( x^n = c \), \(n\) gerade, \( c > 0 \)</td><td>\( x = \pm\sqrt[n]{c} \)</td></tr>
      <tr><td class="li">\( x^n = c \), \(n\) gerade, \( c < 0 \)</td><td class="li">keine Lösung</td></tr>
    </tbody>
  </table>

  <h2>2. Wurzelgleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definitionsmenge</td><td>Radikand \( \geq 0 \)</td></tr>
      <tr><td class="li">Verfahren</td><td class="li">separieren → quadrieren → (wiederholen) → lösen → Kontrolle</td></tr>
      <tr><td class="li">Scheinlösung</td><td class="li">erfüllt die quadrierte, nicht aber die ursprüngliche Gleichung</td></tr>
      <tr><td class="li">Substitution</td><td>\( u = \sqrt{T(x)} \) bei mehrfachem Wurzelterm; nur \( u \geq 0 \)</td></tr>
      <tr><td class="li">unlösbar</td><td>\( \sqrt{T(x)} = c \) mit \( c < 0 \)</td></tr>
    </tbody>
  </table>

  <h2>3. Rationale Gleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definitionsmenge</td><td>Nenner \( \neq 0 \)</td></tr>
      <tr><td class="li">Verfahren</td><td class="li">\(D\) → mit Hauptnenner multiplizieren → lösen → gegen \(D\) prüfen</td></tr>
    </tbody>
  </table>

  <h2>4. Anwendungsformeln (Beispiele)</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Sichtweite</td><td>\( s = 3.57\sqrt{h} \) [km; \(h\) in m]</td></tr>
      <tr><td class="li">Fadenpendel</td><td>\( T = 2\pi\sqrt{l/g} \;\Rightarrow\; l = g\,(T/2\pi)^2 \)</td></tr>
      <tr><td class="li">Freier Fall</td><td>\( t = \sqrt{2h/g} \;\Rightarrow\; h = g\,t^2/2 \)</td></tr>
    </tbody>
  </table>
'''

H_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Bei einer Wurzelgleichung steht die Lösungsvariable unter einer <span class="lueck"></span>.<br>
      Quadrieren ist keine <span class="lueck"></span>umformung — es können<br>
      <span class="lueck"></span> entstehen, darum ist die <span class="lueck"></span> Pflicht.
    </div>''')
    + aufg(2, 'Potenzgleichungen', 1, r'''    <p>Gib die Lösungsmenge an:</p>
    <p>(a) \( x^3 = -27 \) &nbsp;&nbsp; (b) \( x^4 = 81 \) &nbsp;&nbsp; (c) \( x^2 = -9 \)</p>
''' + LINS)
    + aufg(3, 'Lösbar oder nicht?', 1, r'''    <p>Entscheide ohne grosse Rechnung, ob die Gleichung lösbar ist:</p>
    <p>(a) \( \sqrt{x} = 11 \) &nbsp;&nbsp; (b) \( \sqrt{x} = -11 \) &nbsp;&nbsp;
       (c) \( \sqrt{-x} = 11 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Wurzelgleichungen</div>\n'
    + aufg(4, 'Definitionsmenge', 2, r'''    <p>Bestimme die Definitionsmenge von \( \sqrt{5x+1} = 4 \) und von \( \sqrt{4-2x} = 7 \).</p>
''' + LINS)
    + aufg(5, 'Separieren und Quadrieren', 2, r'''    <p>Löse \( \sqrt{6x+7} - 5 = 0 \) inklusive Kontrolle.</p>
''' + LINS)
    + aufg(6, 'Scheinlösung entlarven', 2, r'''    <p>Löse \( \sqrt{6x+7} + 5 = 0 \). Was liefert das Quadrieren, und wie lautet die
    Lösungsmenge wirklich?</p>
''' + LINS)
    + aufg(7, 'Wurzeln zusammenfassen', 2, r'''    <p>Löse \( 9\sqrt{5x+1} = 20 + 4\sqrt{5x+1} \).</p>
''' + LINS)
    + aufg(8, 'Zweimal quadrieren', 3, r'''    <p>Löse \( \sqrt{a-4} = 1 - \sqrt{a+3} \) inklusive Kontrolle.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Rationale Gleichungen</div>\n'
    + aufg(9, 'Bruchgleichung', 2, r'''    <p>Löse \( \dfrac{6}{x-2} = x + 3 \). Notiere zuerst die Definitionsmenge.</p>
''' + LINS)
    + aufg(10, 'Bruchgleichung mit zwei Lösungen', 3, r'''    <p>Löse \( \dfrac{2}{x-1} + 1 = x \) (exakte Werte).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Vertiefung</div>\n'
    + aufg(11, 'Substitution', 3, r'''    <p>Löse \( \sqrt{x^2+9} = 5 \). Welche Rolle spielt der \(\pm\)-Fall?</p>
''' + LINS)
    + aufg(12, 'Äquivalenz beurteilen', 3, r'''    <p>Die Gleichung \( (x+2)(x-2) = 0 \) wird durch \( (x+2) \) dividiert. Bestimme die
    Lösungsmengen vor und nach der Umformung — was ist passiert?</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Wurzel</strong> · <strong>Äquivalenz</strong>umformung · <strong>Scheinlösungen</strong> ·
    <strong>Kontrolle</strong> (Einsetzen in die Ausgangsgleichung).</p>''')
    + loes(2, r'''    <p>(a) \( L = \{-3\} \) (ungerader Exponent) · (b) \( L = \{-3;\ 3\} \) ·
    (c) \( L = \{\,\} \) (gerade Potenz nie negativ).</p>''')
    + loes(3, r'''    <p>(a) lösbar: \( x = 121 \) · (b) unlösbar (Wurzelwert nie negativ) ·
    (c) lösbar: \( -x = 121 \Rightarrow x = -121 \).</p>''')
    + loes(4, r'''    <p>\( 5x+1 \geq 0 \Rightarrow D = \{x \mid x \geq -\tfrac{1}{5}\} \);
    \( 4-2x \geq 0 \Rightarrow D = \{x \mid x \leq 2\} \).</p>''')
    + loes(5, r'''    <p>\( \sqrt{6x+7} = 5 \Rightarrow 6x+7 = 25 \Rightarrow x = 3 \).
    Kontrolle: \( \sqrt{25} - 5 = 0 \) ✓ — \( L = \{3\} \).</p>''')
    + loes(6, r'''    <p>Quadrieren liefert ebenfalls \( x = 3 \) — aber die Kontrolle scheitert:
    \( \sqrt{25} + 5 = 10 \neq 0 \). Die linke Seite ist stets \( \geq 5 \):
    \( L = \{\,\} \).</p>''')
    + loes(7, r'''    <p>\( 5\sqrt{5x+1} = 20 \Rightarrow \sqrt{5x+1} = 4 \Rightarrow 5x+1 = 16
    \Rightarrow x = 3 \). Kontrolle: \( 36 = 36 \) ✓</p>''')
    + loes(8, r'''    <p>Quadrieren: \( a-4 = 1 + a + 3 - 2\sqrt{a+3} \Rightarrow \sqrt{a+3} = 4
    \Rightarrow a = 13 \). Kontrolle: \( 3 \neq 1 - 4 = -3 \) — Scheinlösung,
    \( L = \{\,\} \).</p>''')
    + loes(9, r'''    <p>\( D: x \neq 2 \). \( 6 = (x+3)(x-2) \Rightarrow x^2 + x - 12 = 0
    \Rightarrow (x+4)(x-3) = 0 \Rightarrow L = \{-4;\ 3\} \) (beide in \(D\)).</p>''')
    + loes(10, r'''    <p>\( D: x \neq 1 \). \( 2 + x - 1 = x^2 - x \Rightarrow x^2 - 2x - 1 = 0
    \Rightarrow x = 1 \pm \sqrt{2} \) — beide in \(D\).</p>''')
    + loes(11, r'''    <p>\( x^2 + 9 = 25 \Rightarrow x^2 = 16 \Rightarrow x = \pm 4 \) — die
    Potenzgleichung im zweiten Schritt hat den \(\pm\)-Fall: \( L = \{-4;\ 4\} \).</p>''')
    + loes(12, r'''    <p>Vorher \( L = \{-2;\ 2\} \), nachher \( x - 2 = 0 \Rightarrow L = \{2\} \) —
    die Division durch \( (x+2) \) ist für \( x = -2 \) eine Division durch null und
    <strong>vernichtet</strong> diese Lösung.</p>''')
)

H_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Definitionsmenge und Kontrolle gehören
    zu jeder Wurzel- und Bruchgleichung dazu!</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Navigation</td><td>Sichtweite zum Horizont</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Mechanik</td><td>Fadenpendel</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Physik</td><td>Freier Fall</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Konstruktion</td><td>Zylinder-Radius</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Fahrzeugtechnik</td><td>Kurvengeschwindigkeit</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Optik</td><td>Linsengleichung</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Sichtweite zum Horizont', 2, r'''    <p>Für die Sichtweite gilt \( s = 3.57\sqrt{h} \) (\(s\) in km, \(h\) in m).</p>
    <p>(a) Wie weit sieht man von einem \(30\) m hohen Leuchtturm?</p>
    <p>(b) Welche Höhe braucht es für \(50\) km Sichtweite?</p>
    <p>(c) Warum verdoppelt die vierfache Höhe die Sichtweite nur?</p>
''' + LINS4, tag='Navigation')
    + aufg(2, 'Fadenpendel', 2, r'''    <p>Für ein Fadenpendel gilt \( T = 2\pi\sqrt{l/g} \) mit \( g = 9.81\ \text{m/s}^2 \).</p>
    <p>(a) Löse die Formel nach \(l\) auf.</p>
    <p>(b) Wie lang ist ein Sekundenpendel (\( T = 2 \) s)?</p>
    <p>(c) Berechne die Schwingungsdauer eines \(4\) m langen Pendels.</p>
''' + LINS4, tag='Mechanik')
    + aufg(3, 'Freier Fall', 2, r'''    <p>Für die Fallzeit gilt \( t = \sqrt{2h/g} \).</p>
    <p>(a) Wie lange fällt ein Stein von einer \(80\) m hohen Brücke?</p>
    <p>(b) Aus welcher Höhe fällt ein Körper \(3\) Sekunden lang?</p>
    <p>(c) Ein Echo-Test misst die doppelte Zeit. Ändert sich die Formel?</p>
''' + LINS4, tag='Physik')
    + aufg(4, 'Zylinder-Radius', 3, r'''    <p>Ein zylindrischer Tank soll \( V = 1000\ \text{cm}^3 \) fassen bei Höhe
    \( h = 10 \) cm; es gilt \( V = \pi r^2 h \).</p>
    <p>(a) Löse die Formel nach \(r\) auf.</p>
    <p>(b) Berechne den nötigen Radius.</p>
    <p>(c) Warum ist die negative Wurzel hier keine Lösung?</p>
''' + LINS4, tag='Konstruktion')
    + aufg(5, 'Kurvengeschwindigkeit', 3, r'''    <p>Die maximale Kurvengeschwindigkeit (trockene Strasse) beträgt näherungsweise
    \( v = \sqrt{\mu \cdot g \cdot r} \) mit Haftreibungszahl \( \mu = 0.8 \),
    \( g = 9.81\ \text{m/s}^2 \) und Kurvenradius \(r\).</p>
    <p>(a) Berechne \(v\) für \( r = 50 \) m (in m/s und km/h).</p>
    <p>(b) Welcher Radius erlaubt \(30\) m/s? (Nach \(r\) auflösen.)</p>
    <p>(c) Der Radius wird vervierfacht. Um welchen Faktor steigt \(v\)?</p>
''' + LINS4, tag='Fahrzeugtechnik')
    + aufg(6, 'Linsengleichung', 3, r'''    <p>Für dünne Linsen gilt \( \dfrac{1}{f} = \dfrac{1}{g} + \dfrac{1}{b} \)
    (Brennweite \(f\), Gegenstandsweite \(g\), Bildweite \(b\)).</p>
    <p>(a) Eine Linse hat \( f = 5 \) cm; der Gegenstand steht bei \( g = 8 \) cm.
    Berechne die Bildweite \(b\) (rationale Gleichung!).</p>
    <p>(b) Für welche Gegenstandsweite wäre die Gleichung unlösbar? Deute das optisch.</p>
''' + LINS4, tag='Optik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( s = 3.57\sqrt{30} \approx 19.6 \) km.</p>
    <p>(b) \( \sqrt{h} = \tfrac{50}{3.57} \Rightarrow h \approx 196 \) m.</p>
    <p>(c) \( \sqrt{4h} = 2\sqrt{h} \) — die Wurzel halbiert den Faktor im Exponentensinn.</p>''')
    + loes(2, r'''    <p>(a) \( l = g \cdot (T/2\pi)^2 \).</p>
    <p>(b) \( l = 9.81 \cdot (2/2\pi)^2 \approx 0.99 \) m.</p>
    <p>(c) \( T = 2\pi\sqrt{4/9.81} \approx 4.01 \) s.</p>''')
    + loes(3, r'''    <p>(a) \( t = \sqrt{160/9.81} \approx 4.04 \) s.</p>
    <p>(b) Quadrieren: \( h = g t^2/2 = 9.81 \cdot 9/2 \approx 44.1 \) m.</p>
    <p>(c) Nein — nur die gemessene Zeit muss vorher halbiert werden (Hin- und Rückweg des Schalls).</p>''')
    + loes(4, r'''    <p>(a) \( r^2 = \dfrac{V}{\pi h} \Rightarrow r = \sqrt{\dfrac{V}{\pi h}} \).</p>
    <p>(b) \( r = \sqrt{1000/(10\pi)} \approx 5.64 \) cm.</p>
    <p>(c) Ein Radius ist eine Länge — nur die positive Lösung der Potenzgleichung ist
    physikalisch sinnvoll.</p>''')
    + loes(5, r'''    <p>(a) \( v = \sqrt{0.8 \cdot 9.81 \cdot 50} \approx 19.8\ \text{m/s} \approx 71\ \text{km/h} \).</p>
    <p>(b) Quadrieren: \( r = \dfrac{v^2}{\mu g} = \dfrac{900}{0.8 \cdot 9.81} \approx 115 \) m.</p>
    <p>(c) Faktor \( \sqrt{4} = 2 \).</p>''')
    + loes(6, r'''    <p>(a) \( \tfrac{1}{b} = \tfrac{1}{5} - \tfrac{1}{8} = \tfrac{3}{40} \Rightarrow
    b = \tfrac{40}{3} \approx 13.3 \) cm.</p>
    <p>(b) Für \( g = f = 5 \) cm: \( \tfrac{1}{b} = 0 \) hat keine Lösung — der Gegenstand
    steht im Brennpunkt, es entsteht kein reelles Bild (Strahlen parallel).</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s2-2b  EXPONENTIAL- UND LOGARITHMISCHE GLEICHUNGEN
# ═══════════════════════════════════════════════════════════════════

I_HANDOUT = r'''
  <h2>1. Exponentialgleichungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Definition und Verfahren</div>
    <p>Die Lösungsvariable steht <strong>im Exponenten</strong>. Werkzeuge:
    (1) gleiche Basis → <strong>Exponentenvergleich</strong> \( a^m = a^n \Rightarrow m = n \) ·
    (2) sonst <strong>logarithmieren</strong>: \( \log_a u^x = x \log_a u \) holt die Variable herunter ·
    (3) Summen gleicher Basen erst <strong>ausklammern</strong> ·
    (4) \( a^{2x} \) und \( a^x \) gemischt: <strong>Substitution</strong> \( u = a^x \).</p>
  </div>
  <p><strong>Nie logarithmieren, wenn eine Summe dasteht:</strong> \( \log_a(u^x + v) \) lässt sich
  nicht zerlegen. Und \( a^x = c \) mit \( c \leq 0 \) ist unlösbar (\( a^x > 0 \)).</p>

  <h2>2. Logarithmische Gleichungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Definition und Verfahren</div>
    <p>Die Lösungsvariable steht <strong>im Argument von Logarithmen</strong>. Verfahren:
    (1) <strong>Definitionsmenge</strong>: alle Argumente positiv ·
    (2) mit den Logarithmengesetzen zu je einem Term <strong>zusammenfassen</strong> ·
    (3) <strong>entlogarithmieren</strong> (potenzieren mit der Basis) ·
    (4) lösen und <strong>kontrollieren</strong> — Scheinlösungen möglich.</p>
  </div>
  <p>Vorsicht in beide Richtungen: Entlogarithmieren kann Scheinlösungen erzeugen; die Umformung
  \( \lg x^2 = 2\lg x \) (statt \( 2\lg|x| \)) kann Lösungen <strong>verlieren</strong>.</p>

  <h2>3. Typische Anwendungen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Prozess</th><th>Modell</th><th>«Wann?»-Gleichung</th></tr></thead>
    <tbody>
      <tr><td class="li">Zinseszins</td><td>\( K_0 \cdot q^n \)</td><td>\( q^n = c \Rightarrow n = \ln c / \ln q \)</td></tr>
      <tr><td class="li">Verdopplung alle \(T\)</td><td>\( N_0 \cdot 2^{t/T} \)</td><td>\( 2^{t/T} = c \Rightarrow t = T \log_2 c \)</td></tr>
      <tr><td class="li">Zerfall um \(p\,\%\)</td><td>\( W_0 \cdot (1 - \tfrac{p}{100})^n \)</td><td class="li">logarithmieren</td></tr>
    </tbody>
  </table>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Variable im Exponenten → <strong>logarithmieren</strong> (nach Basen-Check und Ausklammern);
    Variable im Logarithmus → <strong>entlogarithmieren</strong> (nach \(D\)-Check und Zusammenfassen).
    Beide Wege verlangen die <strong>Kontrolle</strong> — und die Substitution \( u = a^x \) macht aus
    gemischten Termen eine quadratische Gleichung.</p>
  </div>
'''

I_FORMELAUSZUG = r'''
  <h2>1. Exponentialgleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Exponentenvergleich</td><td>\( a^m = a^n \Rightarrow m = n \)</td></tr>
      <tr><td class="li">Logarithmieren</td><td>\( a^x = c \Rightarrow x = \dfrac{\ln c}{\ln a} = \log_a c \) (für \( c > 0 \))</td></tr>
      <tr><td class="li">Summe gleicher Basen</td><td>\( a^{x+1} + a^x = a^x (a + 1) \) — erst ausklammern</td></tr>
      <tr><td class="li">Substitution</td><td>\( a^{2x} = (a^x)^2 \Rightarrow u = a^x \), nur \( u > 0 \) brauchbar</td></tr>
      <tr><td class="li">unlösbar</td><td>\( a^x = c \) mit \( c \leq 0 \)</td></tr>
    </tbody>
  </table>

  <h2>2. Logarithmische Gleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definitionsmenge</td><td class="li">alle Logarithmus-Argumente positiv</td></tr>
      <tr><td class="li">Entlogarithmieren</td><td>\( \log_a T(x) = c \Rightarrow T(x) = a^c \)</td></tr>
      <tr><td class="li">Zusammenfassen</td><td>\( \log u + \log v = \log(uv), \quad \log u - \log v = \log\tfrac{u}{v} \)</td></tr>
      <tr><td class="li">Betrags-Falle</td><td>\( \lg x^2 = 2\lg|x| \) — sonst geht eine Lösung verloren</td></tr>
    </tbody>
  </table>

  <h2>3. Wachstums- und Zerfallsgleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Verdopplungszeit</td><td>\( q^n = 2 \Rightarrow n = \dfrac{\ln 2}{\ln q} \)</td></tr>
      <tr><td class="li">Halbwertszeit-Modell</td><td>\( N(t) = N_0 \cdot 0.5^{\,t/T} \Rightarrow t = T \cdot \dfrac{\ln(N/N_0)}{\ln 0.5} \)</td></tr>
      <tr><td class="li">Zielwert erreichen</td><td>\( N_0 \cdot q^t = Z \Rightarrow t = \dfrac{\ln(Z/N_0)}{\ln q} \)</td></tr>
    </tbody>
  </table>
'''

I_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Steht die Variable im Exponenten, hilft das <span class="lueck"></span>;<br>
      steht sie im Logarithmus, das <span class="lueck"></span>.<br>
      Bei Summen zuerst <span class="lueck"></span>; bei \( a^{2x} \) und \( a^x \)
      die <span class="lueck"></span> \( u = a^x \).
    </div>''')
    + aufg(2, 'Exponentenvergleich', 1, r'''    <p>Löse durch Exponentenvergleich:</p>
    <p>(a) \( 2^x = 16 \) &nbsp;&nbsp; (b) \( 3^x = \tfrac{1}{27} \) &nbsp;&nbsp;
       (c) \( 10^x = 0.0001 \)</p>
''' + LINS)
    + aufg(3, 'Lösbar oder nicht?', 1, r'''    <p>Wie viele Lösungen haben die Gleichungen?</p>
    <p>(a) \( 5^x = 30 \) &nbsp;&nbsp; (b) \( 5^x = -30 \) &nbsp;&nbsp; (c) \( 5^x = 0 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Exponentialgleichungen</div>\n'
    + aufg(4, 'Logarithmieren', 2, r'''    <p>Löse \( 3^x = 8 \) und \( 4^{y-5} = 100 \) (zwei Dezimalen).</p>
''' + LINS)
    + aufg(5, 'Ausklammern', 2, r'''    <p>Löse \( 3^{x+1} + 3^x = 20 \).</p>
''' + LINS)
    + aufg(6, 'Substitution', 3, r'''    <p>Löse \( 4^x - 7 \cdot 2^x = 8 \).</p>
''' + LINS)
    + aufg(7, 'Substitution mit zwei Lösungen', 3, r'''    <p>Löse \( 3^{2x} + 9 = 10 \cdot 3^x \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Logarithmische Gleichungen</div>\n'
    + aufg(8, 'Entlogarithmieren', 1, r'''    <p>Bestimme \(x\): (a) \( \lg x = 4 \) &nbsp;&nbsp; (b) \( \ln x = -1 \) &nbsp;&nbsp;
    (c) \( \lg(x+3) = 2 \)</p>
''' + LINS)
    + aufg(9, 'Zusammenfassen', 2, r'''    <p>Löse \( \ln z + \ln 2 = 3 \).</p>
''' + LINS)
    + aufg(10, 'Mit Scheinlösung', 3, r'''    <p>Löse \( \log_2 u + \log_2(u-2) = 3 \) inklusive Definitionsmenge und Kontrolle.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Vertiefung</div>\n'
    + aufg(11, 'Scheinlösung bei lg', 3, r'''    <p>Löse \( \lg(x-3) = 1 - \lg x \). Warum ist einer der Kandidaten keine Lösung?</p>
''' + LINS)
    + aufg(12, 'Verlorene Lösung', 3, r'''    <p>Löse \( 3\lg x^2 + 7 = 13 \). Warum liefert der Weg über \( 6\lg x = 6 \) nur die
    halbe Lösungsmenge?</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Logarithmieren</strong> · <strong>Entlogarithmieren</strong> ·
    <strong>ausklammern</strong> · <strong>Substitution</strong>.</p>''')
    + loes(2, r'''    <p>(a) \( x = 4 \) · (b) \( 3^x = 3^{-3} \Rightarrow x = -3 \) ·
    (c) \( x = -4 \).</p>''')
    + loes(3, r'''    <p>(a) genau eine (\( x = \log_5 30 \)) · (b) keine · (c) keine —
    \( 5^x > 0 \) für alle \(x\).</p>''')
    + loes(4, r'''    <p>\( x = \tfrac{\ln 8}{\ln 3} \approx 1.89 \);
    \( (y-5)\ln 4 = \ln 100 \Rightarrow y = 5 + \tfrac{\ln 100}{\ln 4} \approx 8.32 \).</p>''')
    + loes(5, r'''    <p>\( 3^x (3+1) = 20 \Rightarrow 3^x = 5 \Rightarrow x = \log_3 5 \approx 1.46 \).</p>''')
    + loes(6, r'''    <p>\( u = 2^x \): \( u^2 - 7u - 8 = 0 \Rightarrow u = 8 \) (\( u = -1 \) entfällt)
    \( \Rightarrow x = 3 \).</p>''')
    + loes(7, r'''    <p>\( u = 3^x \): \( u^2 - 10u + 9 = 0 \Rightarrow u = 1, 9 \Rightarrow
    L = \{0;\ 2\} \).</p>''')
    + loes(8, r'''    <p>(a) \( x = 10^4 \) · (b) \( x = e^{-1} \approx 0.37 \) ·
    (c) \( x = 100 - 3 = 97 \).</p>''')
    + loes(9, r'''    <p>\( \ln 2z = 3 \Rightarrow 2z = e^3 \Rightarrow z = \tfrac{e^3}{2} \approx 10.04 \).</p>''')
    + loes(10, r'''    <p>\( D: u > 2 \). \( u(u-2) = 8 \Rightarrow (u-4)(u+2) = 0 \) —
    \( u = -2 \notin D \) (Scheinlösung), \( u = 4 \): Kontrolle \( 2 + 1 = 3 \) ✓.
    \( L = \{4\} \).</p>''')
    + loes(11, r'''    <p>\( D: x > 3 \). \( x(x-3) = 10 \Rightarrow (x-5)(x+2) = 0 \). \( x = -2 \)
    verletzt \(D\) (\( \lg(-2) \) existiert nicht) — Scheinlösung. \( L = \{5\} \).</p>''')
    + loes(12, r'''    <p>\( \lg x^2 = 2 \Rightarrow x^2 = 100 \Rightarrow L = \{-10;\ 10\} \).
    Der Weg \( 6\lg x = 6 \) setzt stillschweigend \( x > 0 \) voraus (korrekt wäre
    \( 2\lg|x| \)) und verliert \( x = -10 \).</p>''')
)

I_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Naturwissenschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Exakt lösen (Logarithmus), dann runden.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Finanzmathematik</td><td>Zinseszins</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Biologie</td><td>Algen im See</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Wirtschaft</td><td>Wertverlust eines Autos</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Physik</td><td>Radioaktiver Zerfall</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Meteorologie</td><td>Barometrische Höhenformel</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Alltag / Physik</td><td>Kaffee-Abkühlung</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Zinseszins', 2, r'''    <p>Ein Kapital von \( 22\,000 \) CHF wird zu \(4.5\) % angelegt: \( K(n) = 22\,000 \cdot 1.045^n \).</p>
    <p>(a) Auf welchen Betrag wächst es in \(6\) Jahren?</p>
    <p>(b) Nach wie vielen Jahren erreicht es \( 30\,000 \) CHF?</p>
    <p>(c) Nach wie vielen Jahren hat es sich verdoppelt?</p>
''' + LINS4, tag='Finanzmathematik')
    + aufg(2, 'Algen im See', 2, r'''    <p>Ein See ist zu \(2.5\) % mit Algen bedeckt; die Fläche verdoppelt sich alle \(4\) Tage:
    \( A(t) = 2.5 \cdot 2^{t/4} \) (in %).</p>
    <p>(a) Welcher Anteil ist nach \(20\) Tagen bedeckt?</p>
    <p>(b) Wann ist der See zur Hälfte bedeckt?</p>
    <p>(c) Wann vollständig?</p>
''' + LINS4, tag='Biologie')
    + aufg(3, 'Wertverlust eines Autos', 2, r'''    <p>Neupreis \( 32\,000 \) CHF, Wertverlust \(22\) % pro Jahr: \( W(n) = 32\,000 \cdot 0.78^n \).</p>
    <p>(a) Wie viel ist das Auto nach \(6\) Jahren wert?</p>
    <p>(b) Nach wie vielen Jahren ist es noch die Hälfte wert?</p>
    <p>(c) Skizziere den Verlauf über \(10\) Jahre.</p>
''' + LINS4, tag='Wirtschaft')
    + aufg(4, 'Radioaktiver Zerfall', 3, r'''    <p>Ein radioaktiver Stoff hat die Halbwertszeit \(5\) Tage: \( N(t) = N_0 \cdot 0.5^{t/5} \).</p>
    <p>(a) Welcher Anteil ist nach \(10\) Tagen noch vorhanden?</p>
    <p>(b) Nach wie vielen Tagen ist noch ein Zehntel vorhanden?</p>
    <p>(c) Warum genügt «zweimal die Halbwertszeit» nicht für ein Viertel → ein Zehntel?</p>
''' + LINS4, tag='Physik')
    + aufg(5, 'Barometrische Höhenformel', 3, r'''    <p>Näherungsweise gilt \( p(h) = 1013 \cdot 0.5^{\,h/5500} \) (Druck in hPa, Höhe in m).</p>
    <p>(a) Berechne den Luftdruck in Bern (\(542\) m) und auf dem Jungfraujoch (\(3471\) m).</p>
    <p>(b) In welcher Höhe beträgt der Druck noch \(500\) hPa? (Logarithmieren!)</p>
''' + LINS4, tag='Meteorologie')
    + aufg(6, 'Kaffee-Abkühlung', 3, r'''    <p>Ein Kaffee kühlt gegen die Raumtemperatur ab: \( T(t) = 20 + 70 \cdot 0.9^t \)
    (\(T\) in °C, \(t\) in min).</p>
    <p>(a) Wie heiss ist der Kaffee zu Beginn und nach \(5\) Minuten?</p>
    <p>(b) Wann erreicht er trinkbare \(40\) °C? (Erst \(0.9^t\) isolieren!)</p>
    <p>(c) Warum darf man hier nicht sofort logarithmieren?</p>
''' + LINS4, tag='Alltag / Physik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( 22\,000 \cdot 1.045^6 \approx 28\,650 \) CHF.</p>
    <p>(b) \( 1.045^n = \tfrac{30}{22} \Rightarrow n = \tfrac{\ln(30/22)}{\ln 1.045} \approx 7.0 \) Jahre.</p>
    <p>(c) \( n = \tfrac{\ln 2}{\ln 1.045} \approx 15.7 \) Jahre.</p>''')
    + loes(2, r'''    <p>(a) \( 2.5 \cdot 2^5 = 80 \) %.</p>
    <p>(b) \( 2^{t/4} = 20 \Rightarrow t = 4\log_2 20 \approx 17.3 \) Tage.</p>
    <p>(c) \( 2^{t/4} = 40 \Rightarrow t = 4\log_2 40 \approx 21.3 \) Tage.</p>''')
    + loes(3, r'''    <p>(a) \( 32\,000 \cdot 0.78^6 \approx 7206 \) CHF.</p>
    <p>(b) \( 0.78^n = 0.5 \Rightarrow n = \tfrac{\ln 0.5}{\ln 0.78} \approx 2.8 \) Jahre.</p>
    <p>(c) Fallende Exponentialkurve mit Asymptote \( W = 0 \).</p>''')
    + loes(4, r'''    <p>(a) \( 0.5^2 = 0.25 \) — ein Viertel.</p>
    <p>(b) \( 0.5^{t/5} = 0.1 \Rightarrow t = 5 \cdot \tfrac{\ln 0.1}{\ln 0.5} \approx 16.6 \) Tage.</p>
    <p>(c) Zwei Halbwertszeiten geben den Faktor \( \tfrac{1}{4} \), nicht \( \tfrac{1}{10} \) —
    exponentieller Zerfall rechnet multiplikativ.</p>''')
    + loes(5, r'''    <p>(a) Bern: \( 1013 \cdot 0.5^{542/5500} \approx 946 \) hPa; Jungfraujoch:
    \( \approx 654 \) hPa.</p>
    <p>(b) \( 0.5^{h/5500} = \tfrac{500}{1013} \Rightarrow h = 5500 \cdot
    \tfrac{\ln(500/1013)}{\ln 0.5} \approx 5600 \) m.</p>''')
    + loes(6, r'''    <p>(a) \( T(0) = 90 \) °C; \( T(5) = 20 + 70 \cdot 0.9^5 \approx 61.3 \) °C.</p>
    <p>(b) \( 70 \cdot 0.9^t = 20 \Rightarrow 0.9^t = \tfrac{2}{7} \Rightarrow
    t = \tfrac{\ln(2/7)}{\ln 0.9} \approx 11.9 \) min.</p>
    <p>(c) Links steht die Summe \( 20 + 70 \cdot 0.9^t \) — Logarithmieren einer Summe
    ist nicht zerlegbar. Erst die Potenz isolieren.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s2-2c  BETRAGS- UND POLYNOMGLEICHUNGEN, UNGLEICHUNGEN
# ═══════════════════════════════════════════════════════════════════

J_HANDOUT = r'''
  <h2>1. Betrag und Betragsgleichungen</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Betrag</div>
    <p>\( |x| = x \) für \( x \geq 0 \), \( |x| = -x \) für \( x < 0 \) — geometrisch der
    <strong>Abstand</strong> zum Nullpunkt; \( |x - m| \) ist der Abstand zu \(m\).</p>
  </div>
  <table class="ftb-tabelle">
    <thead><tr><th>\( |T(x)| = c \)</th><th>Vorgehen</th></tr></thead>
    <tbody>
      <tr><td>\( c > 0 \)</td><td class="li">zwei Fälle: \( T(x) = c \) oder \( T(x) = -c \)</td></tr>
      <tr><td>\( c = 0 \)</td><td>\( T(x) = 0 \)</td></tr>
      <tr><td>\( c < 0 \)</td><td class="li">keine Lösung (Beträge nie negativ)</td></tr>
    </tbody>
  </table>

  <h2>2. Polynomgleichungen in Produktform</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Satz vom Nullprodukt</div>
    <p>\( A \cdot B = 0 \Leftrightarrow A = 0 \vee B = 0 \) — jeden Faktor einzeln null setzen.
    Gemeinsame Faktoren zuerst <strong>ausklammern</strong> (\( x^3 = 9x \Rightarrow x(x-3)(x+3) = 0 \));
    <strong>nie durch \(x\) dividieren</strong> — das vernichtet die Lösung \( x = 0 \).</p>
  </div>

  <h2>3. Ungleichungen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Umformung</th><th>Relationszeichen</th></tr></thead>
    <tbody>
      <tr><td class="li">addieren / subtrahieren</td><td class="li">bleibt</td></tr>
      <tr><td class="li">mal / durch positive Zahl</td><td class="li">bleibt</td></tr>
      <tr><td class="li">mal / durch <strong>negative</strong> Zahl</td><td class="li"><strong>dreht</strong> (\(<\) wird \(>\))</td></tr>
    </tbody>
  </table>
  <p><strong>Vorzeichentabelle</strong> für Produkte: Nullstellen aller Faktoren zerlegen die
  Zahlengerade in Abschnitte; je Abschnitt das Vorzeichen jedes Faktors notieren, Produktvorzeichen
  ablesen. Randpunkte gehören nur bei \( \geq/\leq \) zur Lösungsmenge. Alternative: grafisch
  (Kurve oberhalb/unterhalb).</p>

  <h2>4. Betragsungleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( |x - m| \leq r \)</td><td>Intervall \( [m-r;\ m+r] \) — «Toleranzband» um \(m\)</td></tr>
      <tr><td class="li">\( |x - m| > r \)</td><td>\( x < m-r \ \vee\ x > m+r \) — Aussenbereiche</td></tr>
    </tbody>
  </table>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Betrag = Abstand: Gleichungen brauchen <strong>zwei Fälle</strong>, Ungleichungen liefern
    <strong>Intervalle</strong>. Produkte gleich null löst der <strong>Satz vom Nullprodukt</strong>,
    Produkte grösser/kleiner null die <strong>Vorzeichentabelle</strong>. Und beim Multiplizieren mit
    Negativem: Relationszeichen <strong>drehen</strong>.</p>
  </div>
'''

J_FORMELAUSZUG = r'''
  <h2>1. Betrag</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definition</td><td>\( |x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases} \)</td></tr>
      <tr><td class="li">geometrisch</td><td class="li">Abstand zum Nullpunkt; \( |x-m| \): Abstand zu \(m\)</td></tr>
      <tr><td class="li">\( |T(x)| = c > 0 \)</td><td>\( T(x) = c \ \vee\ T(x) = -c \)</td></tr>
      <tr><td class="li">\( |T(x)| = c < 0 \)</td><td>\( L = \{\,\} \)</td></tr>
      <tr><td class="li">\( |A| = |B| \)</td><td>\( A = B \ \vee\ A = -B \)</td></tr>
    </tbody>
  </table>

  <h2>2. Betragsungleichungen (\( r > 0 \))</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( |x-m| \leq r \)</td><td>\( [m-r;\ m+r] \)</td></tr>
      <tr><td class="li">\( |x-m| < r \)</td><td>\( ]m-r;\ m+r[ \)</td></tr>
      <tr><td class="li">\( |x-m| > r \)</td><td>\( x < m-r \ \vee\ x > m+r \)</td></tr>
    </tbody>
  </table>

  <h2>3. Nullprodukt</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Satz</td><td>\( A \cdot B = 0 \Leftrightarrow A = 0 \ \vee\ B = 0 \)</td></tr>
      <tr><td class="li">Vorbereitung</td><td class="li">alles auf eine Seite, gemeinsame Faktoren ausklammern</td></tr>
      <tr><td class="li">Verboten</td><td class="li">Division durch \(x\) (vernichtet \( x = 0 \))</td></tr>
    </tbody>
  </table>

  <h2>4. Ungleichungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Zeichen dreht bei</td><td class="li">Multiplikation/Division mit negativer Zahl</td></tr>
      <tr><td class="li">Vorzeichentabelle</td><td class="li">Nullstellen → Abschnitte → Faktor-Vorzeichen → Produkt</td></tr>
      <tr><td class="li">Randpunkte</td><td class="li">nur bei \( \geq \) / \( \leq \) in der Lösungsmenge</td></tr>
      <tr><td class="li">Kontrolle</td><td class="li">ein Testwert pro Abschnitt</td></tr>
    </tbody>
  </table>
'''

J_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Der Betrag \( |x - m| \) misst den <span class="lueck"></span> von \(x\) zu \(m\).<br>
      Ein Produkt ist null, wenn mindestens ein <span class="lueck"></span> null ist.<br>
      Multiplizieren mit einer negativen Zahl <span class="lueck"></span> das Relationszeichen.
    </div>''')
    + aufg(2, 'Beträge berechnen', 1, r'''    <p>Berechne: (a) \( |{-7}| \) &nbsp;&nbsp; (b) \( |4 - 9| \) &nbsp;&nbsp;
    (c) \( |3 - \pi| \)</p>
''' + LINS)
    + aufg(3, 'Lösbar oder nicht?', 1, r'''    <p>Wie viele Lösungen haben die Gleichungen?</p>
    <p>(a) \( |x| = 6 \) &nbsp;&nbsp; (b) \( |x| = 0 \) &nbsp;&nbsp; (c) \( |x| = -6 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Betragsgleichungen</div>\n'
    + aufg(4, 'Zwei Fälle', 2, r'''    <p>Löse \( |x - 3| = 5 \) und deute die Lösungen als Abstände.</p>
''' + LINS)
    + aufg(5, 'Linearer Term im Betrag', 2, r'''    <p>Löse \( |2x + 1| = 7 \).</p>
''' + LINS)
    + aufg(6, 'Betragsungleichung', 2, r'''    <p>Löse \( |x - 2| \leq 3 \) und gib die Lösungsmenge als Intervall an.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Polynomgleichungen</div>\n'
    + aufg(7, 'Nullprodukt ablesen', 1, r'''    <p>Löse \( (x+1)(x-2)(x-5) = 0 \).</p>
''' + LINS)
    + aufg(8, 'Erst ausklammern', 2, r'''    <p>Löse \( x^3 = 9x \). Warum darf nicht durch \(x\) dividiert werden?</p>
''' + LINS)
    + aufg(9, 'Quadratischer Faktor', 2, r'''    <p>Löse \( (x-4)(x^2+1) = 0 \). Wie viele reelle Lösungen gibt es?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Ungleichungen</div>\n'
    + aufg(10, 'Zeichen drehen', 2, r'''    <p>Löse \( 5 - 2x < 11 \) und prüfe mit einem Testwert.</p>
''' + LINS)
    + aufg(11, 'Vorzeichentabelle', 3, r'''    <p>Löse \( (x-1)(x+3) < 0 \) mit der Vorzeichentabelle.</p>
''' + LINS)
    + aufg(12, 'Drei Faktoren', 3, r'''    <p>Löse \( (x+2)(x-1)(x-4) > 0 \).</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Abstand</strong> · <strong>Faktor</strong> · <strong>dreht</strong>.</p>''')
    + loes(2, r'''    <p>(a) \(7\) · (b) \( |-5| = 5 \) · (c) \( \pi > 3 \), also \( \pi - 3 \approx 0.14 \).</p>''')
    + loes(3, r'''    <p>(a) zwei (\( \pm 6 \)) · (b) eine (\( x = 0 \)) · (c) keine.</p>''')
    + loes(4, r'''    <p>\( x - 3 = \pm 5 \Rightarrow L = \{-2;\ 8\} \) — die beiden Zahlen mit Abstand \(5\)
    von der \(3\).</p>''')
    + loes(5, r'''    <p>\( 2x+1 = 7 \Rightarrow x = 3 \); \( 2x+1 = -7 \Rightarrow x = -4 \):
    \( L = \{-4;\ 3\} \).</p>''')
    + loes(6, r'''    <p>Abstand von \(2\) höchstens \(3\): \( L = [-1;\ 5] \).</p>''')
    + loes(7, r'''    <p>\( L = \{-1;\ 2;\ 5\} \).</p>''')
    + loes(8, r'''    <p>\( x(x-3)(x+3) = 0 \Rightarrow L = \{-3;\ 0;\ 3\} \). Division durch \(x\) ist für
    \( x = 0 \) verboten und würde genau diese Lösung vernichten.</p>''')
    + loes(9, r'''    <p>Nur \( x = 4 \) — der Faktor \( x^2 + 1 \geq 1 \) wird nie null: eine reelle Lösung.</p>''')
    + loes(10, r'''    <p>\( -2x < 6 \Rightarrow x > -3 \) (Zeichen gedreht). Testwert \( x = 0 \):
    \( 5 < 11 \) ✓</p>''')
    + loes(11, r'''    <p>Nullstellen \( -3, 1 \); dazwischen ist genau ein Faktor negativ → Produkt negativ:
    \( L = \{x \mid -3 < x < 1\} \).</p>''')
    + loes(12, r'''    <p>Nullstellen \( -2, 1, 4 \); Tabelle gibt \(+\) in \( ]-2;\,1[ \) und \( ]4;\,\infty[ \):
    \( L = \{x \mid -2 < x < 1 \ \vee\ x > 4\} \).</p>''')
)

J_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Wirtschaft, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Lösungsmengen als Intervalle angeben.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Fertigung</td><td>Toleranzprüfung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Elektrotechnik</td><td>Widerstands-Toleranz</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Medizin</td><td>Fieber-Grenzen</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Betriebswirtschaft</td><td>Gewinnzone</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Wirtschaft</td><td>Break-even als Ungleichung</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Verkehr</td><td>Bremsweg-Limite</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Toleranzprüfung', 2, r'''    <p>Eine Welle hat das Sollmass \(25\) mm mit Toleranz \( \pm 0.02 \) mm:
    brauchbar, wenn \( |d - 25| \leq 0.02 \).</p>
    <p>(a) Gib das Toleranzband als Intervall an.</p>
    <p>(b) Beurteile drei Werkstücke: \( 25.01 \), \( 24.97 \) und \( 25.02 \) mm.</p>
''' + LINS4, tag='Fertigung')
    + aufg(2, 'Widerstands-Toleranz', 2, r'''    <p>Ein Widerstand hat den Nennwert \( 470\ \Omega \) mit \(5\) % Toleranz.</p>
    <p>(a) Schreibe den zulässigen Bereich als Betragsungleichung.</p>
    <p>(b) Gib das Intervall an.</p>
    <p>(c) Ist ein gemessener Wert von \( 495\ \Omega \) innerhalb der Toleranz?</p>
''' + LINS4, tag='Elektrotechnik')
    + aufg(3, 'Fieber-Grenzen', 2, r'''    <p>Als auffällig gilt eine Körpertemperatur, die um mehr als \(1.2\) °C von \(36.8\) °C
    abweicht: \( |T - 36.8| > 1.2 \).</p>
    <p>(a) Gib die auffälligen Temperaturbereiche an.</p>
    <p>(b) Formuliere den unauffälligen Bereich als Intervall.</p>
''' + LINS4, tag='Medizin')
    + aufg(4, 'Gewinnzone', 3, r'''    <p>Der Tagesgewinn beträgt \( G(x) = -(x-30)^2 + 400 \) (CHF, Stückzahl \(x\)).</p>
    <p>(a) Forme \( G(x) > 0 \) in eine Betragsungleichung um.</p>
    <p>(b) Bestimme die Gewinnzone.</p>
    <p>(c) Bei welcher Stückzahl ist der Gewinn maximal?</p>
''' + LINS4, tag='Betriebswirtschaft')
    + aufg(5, 'Break-even als Ungleichung', 3, r'''    <p>Kosten \( K(x) = 2000 + 15x \), Erlös \( E(x) = 40x \).</p>
    <p>(a) Formuliere «Gewinn» als Ungleichung.</p>
    <p>(b) Löse sie und interpretiere die Grenze.</p>
    <p>(c) Was ändert sich, wenn die Fixkosten auf \(2500\) steigen?</p>
''' + LINS4, tag='Wirtschaft')
    + aufg(6, 'Bremsweg-Limite', 3, r'''    <p>Faustregel für den Bremsweg: \( s = \dfrac{v^2}{100} \) (\(s\) in m, \(v\) in km/h).</p>
    <p>(a) Vor einem Hindernis stehen höchstens \(40\) m zur Verfügung. Formuliere die
    Bedingung als Ungleichung.</p>
    <p>(b) Löse sie nach \(v\) auf — welche Höchstgeschwindigkeit ist zulässig?</p>
    <p>(c) Warum ist die negative Lösung der Potenzgleichung hier bedeutungslos?</p>
''' + LINS4, tag='Verkehr')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( [24.98;\ 25.02] \) mm.</p>
    <p>(b) \( |25.01-25| = 0.01 \) ✓ brauchbar; \( |24.97-25| = 0.03 \) ✗ Ausschuss;
    \( |25.02-25| = 0.02 \) ✓ gerade noch brauchbar (Randpunkt, \( \leq \)).</p>''')
    + loes(2, r'''    <p>(a) \(5\) % von \(470\) sind \(23.5\): \( |R - 470| \leq 23.5 \).</p>
    <p>(b) \( [446.5;\ 493.5]\ \Omega \).</p>
    <p>(c) \( |495 - 470| = 25 > 23.5 \) — ausserhalb der Toleranz.</p>''')
    + loes(3, r'''    <p>(a) \( T < 35.6 \) °C oder \( T > 38 \) °C.</p>
    <p>(b) \( [35.6;\ 38] \) °C (mit \( \leq \): Randwerte gelten als unauffällig).</p>''')
    + loes(4, r'''    <p>(a) \( (x-30)^2 < 400 \Leftrightarrow |x - 30| < 20 \).</p>
    <p>(b) \( 10 < x < 50 \) Stück.</p>
    <p>(c) Scheitel der Parabel: \( x = 30 \), Maximalgewinn \(400\) CHF.</p>''')
    + loes(5, r'''    <p>(a) \( E(x) > K(x) \): \( 40x > 2000 + 15x \).</p>
    <p>(b) \( 25x > 2000 \Rightarrow x > 80 \) — ab dem \(81\). Stück Gewinn.</p>
    <p>(c) \( 25x > 2500 \Rightarrow x > 100 \) — die Gewinnzone beginnt später.</p>''')
    + loes(6, r'''    <p>(a) \( \dfrac{v^2}{100} \leq 40 \).</p>
    <p>(b) \( v^2 \leq 4000 \Rightarrow v \leq \sqrt{4000} \approx 63 \) km/h
    (für \( v \geq 0 \)).</p>
    <p>(c) Geschwindigkeiten sind hier nicht negativ — nur der Ast \( v \geq 0 \)
    der Potenzgleichung ist physikalisch sinnvoll.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s2-1  GRUNDLAGEN (GLEICHUNGS-WERKZEUGKASTEN)
# ═══════════════════════════════════════════════════════════════════

K_HANDOUT = r'''
  <h2>1. Vokabular</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Gleichung</td><td class="li">Aussage \( T_1(x) = T_2(x) \) — zwei Terme haben denselben Wert</td></tr>
      <tr><td class="li">Grundmenge \(G\)</td><td class="li">erlaubte Zahlenmenge (meist \( \mathbb{R} \))</td></tr>
      <tr><td class="li">Definitionsmenge \(D\)</td><td class="li">alle \(x\), für die beide Terme definiert sind (Nenner \( \neq 0 \), Radikand \( \geq 0 \), Log-Argument \( > 0 \))</td></tr>
      <tr><td class="li">Lösungsmenge \(L\)</td><td class="li">alle \( x \in D \), welche die Gleichung erfüllen — kann leer, endlich oder unendlich sein</td></tr>
    </tbody>
  </table>

  <h2>2. Äquivalenzumformungen — und ihre gefährlichen Verwandten</h2>
  <p><strong>Sicher</strong> (Lösungsmenge bleibt): beidseitig addieren/subtrahieren; beidseitig
  mit fester Zahl \( \neq 0 \) multiplizieren/dividieren — das Waage-Prinzip.</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Gefährliche Umformung</th><th>Risiko</th><th>Gegenmittel</th></tr></thead>
    <tbody>
      <tr><td class="li">quadrieren / potenzieren</td><td class="li">Scheinlösungen</td><td class="li">Probe in der Ausgangsgleichung</td></tr>
      <tr><td class="li">mit Term multiplizieren</td><td class="li">Scheinlösung bei Term = 0</td><td class="li">\(D\) notieren, Lösungen prüfen</td></tr>
      <tr><td class="li">durch Term dividieren</td><td class="li">Lösungen gehen verloren</td><td class="li">ausklammern + Nullprodukt</td></tr>
    </tbody>
  </table>

  <h2>3. Der Typen-Blick: Wo steht die Unbekannte?</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Typ</th><th>Wo steht \(x\)?</th><th>Beispiel</th><th>Methode</th></tr></thead>
    <tbody>
      <tr><td class="li">linear</td><td class="li">nur 1. Potenz</td><td>\( 3x + 2 = 11 \)</td><td class="li">Äquivalenzumformungen</td></tr>
      <tr><td class="li">quadratisch</td><td class="li">2. Potenz</td><td>\( x^2 + 3x - 10 = 0 \)</td><td class="li">Faktorisieren · Lösungsformel</td></tr>
      <tr><td class="li">Potenzgleichung</td><td class="li">Basis</td><td>\( x^4 = 81 \)</td><td class="li">\(n\)-te Wurzel (Parität!)</td></tr>
      <tr><td class="li">Wurzelgleichung</td><td class="li">Radikand</td><td>\( \sqrt{2x+1} = 7 \)</td><td class="li">separieren · quadrieren · Probe</td></tr>
      <tr><td class="li">rational</td><td class="li">Nenner</td><td>\( \tfrac{6}{x+1} = 2 \)</td><td class="li">\(D\) · Hauptnenner</td></tr>
      <tr><td class="li">exponentiell</td><td class="li">Exponent</td><td>\( 5 \cdot 2^x = 80 \)</td><td class="li">Exponentenvergleich · logarithmieren</td></tr>
      <tr><td class="li">logarithmisch</td><td class="li">Log-Argument</td><td>\( \lg(x+3) = 2 \)</td><td class="li">\(D\) · entlogarithmieren · Probe</td></tr>
      <tr><td class="li">Betrag</td><td class="li">im Betrag</td><td>\( |x-4| = 9 \)</td><td class="li">zwei Fälle \( \pm \)</td></tr>
      <tr><td class="li">Produktform</td><td class="li">Faktoren</td><td>\( x(x-3)(x+2) = 0 \)</td><td class="li">Nullprodukt</td></tr>
    </tbody>
  </table>

  <h2>4. Der Vier-Schritte-Fahrplan</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Typ → D → Methode → Kontrolle</div>
    <p>(1) Typ bestimmen («Wo steht \(x\)?») · (2) Definitionsmenge notieren ·
    (3) passende Methode anwenden · (4) überprüfen: <strong>Probe</strong> (Ausgangsgleichung),
    <strong>Skizze</strong> (Anzahl Schnittpunkte = erwartete Lösungsanzahl),
    <strong>Plausibilität</strong> (Vorzeichen, Grössenordnung, Einheit).</p>
  </div>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Die wichtigste Entscheidung fällt <strong>vor</strong> dem Rechnen: den Typ am Ort der
    Unbekannten erkennen. Sichere Umformungen erhalten die Waage; Quadrieren, Terme-Multiplikation
    und -Division verlangen \(D\) und Probe. Ohne Kontrolle ist keine Lösungsmenge bestimmt.</p>
  </div>
'''

K_FORMELAUSZUG = r'''
  <h2>1. Mengen-Begriffe</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definitionsmenge \(D\)</td><td class="li">Nenner \( \neq 0 \) · Radikand \( \geq 0 \) · Log-Argument \( > 0 \)</td></tr>
      <tr><td class="li">Lösungsmenge \(L\)</td><td class="li">leer \( \{\,\} \) · endlich \( \{x_1; \dots\} \) · allgemeingültig \( G \)</td></tr>
    </tbody>
  </table>

  <h2>2. Umformungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">äquivalent</td><td class="li">\( \pm \) Term · \( \cdot/: \) Zahl \( \neq 0 \)</td></tr>
      <tr><td class="li">Scheinlösungs-Gefahr</td><td class="li">quadrieren · mit Term multiplizieren · entlogarithmieren</td></tr>
      <tr><td class="li">Verlust-Gefahr</td><td class="li">durch Term dividieren · \( \lg x^2 = 2\lg x \) statt \( 2\lg|x| \)</td></tr>
    </tbody>
  </table>

  <h2>3. Typ-Erkennung und Methode</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>\(x\) steht …</th><th>Typ</th><th>Methode</th></tr></thead>
    <tbody>
      <tr><td class="li">in 1. Potenz</td><td class="li">linear</td><td class="li">umformen</td></tr>
      <tr><td class="li">in 2. Potenz</td><td class="li">quadratisch</td><td class="li">faktorisieren · Formel</td></tr>
      <tr><td class="li">in der Basis (\(x^n = c\))</td><td class="li">Potenzgleichung</td><td class="li">\(n\)-te Wurzel, Parität</td></tr>
      <tr><td class="li">im Radikanden</td><td class="li">Wurzelgleichung</td><td class="li">separieren + quadrieren</td></tr>
      <tr><td class="li">im Nenner</td><td class="li">rational</td><td class="li">Hauptnenner</td></tr>
      <tr><td class="li">im Exponenten</td><td class="li">exponentiell</td><td class="li">logarithmieren</td></tr>
      <tr><td class="li">im Log-Argument</td><td class="li">logarithmisch</td><td class="li">entlogarithmieren</td></tr>
      <tr><td class="li">im Betrag</td><td class="li">Betragsgleichung</td><td class="li">zwei Fälle</td></tr>
      <tr><td class="li">in Faktoren (\( \cdot = 0 \))</td><td class="li">Produktform</td><td class="li">Nullprodukt</td></tr>
    </tbody>
  </table>

  <h2>4. Kontrolle</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Probe</td><td class="li">in die <strong>Ausgangs</strong>gleichung einsetzen</td></tr>
      <tr><td class="li">Skizze</td><td class="li">Schnittpunkte beider Seiten = erwartete Lösungsanzahl</td></tr>
      <tr><td class="li">Plausibilität</td><td class="li">Vorzeichen, Grössenordnung, Einheit zur Anwendung passend?</td></tr>
    </tbody>
  </table>
'''

K_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Vokabular vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Umformungen, welche die Lösungsmenge nicht ändern, heissen <span class="lueck"></span>.<br>
      Die <span class="lueck"></span>menge enthält alle \(x\), für die beide Seiten definiert sind.<br>
      Die Probe macht man in der <span class="lueck"></span>gleichung.
    </div>''')
    + aufg(2, 'Äquivalent oder nicht?', 2, r'''    <p>Beurteile die Umformung (äquivalent / Scheinlösungs-Gefahr / Verlust-Gefahr):</p>
    <p>(a) beidseitig \( +9 \) &nbsp;&nbsp; (b) beidseitig quadrieren &nbsp;&nbsp;
       (c) beidseitig durch \(x\) dividieren</p>
''' + LINS)
    + aufg(3, 'Lösungsmengen-Spezialfälle', 2, r'''    <p>Bestimme die Lösungsmenge:</p>
    <p>(a) \( 2(x+1) = 2x + 2 \) &nbsp;&nbsp;&nbsp; (b) \( x = x + 1 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Typ bestimmen</div>\n'
    + aufg(4, 'Wo steht die Unbekannte?', 1, r'''    <p>Bestimme den Typ (ohne zu lösen):</p>
    <p>(a) \( \sqrt{x-5} = 4 \) &nbsp;&nbsp; (b) \( 3^x = 125 \) &nbsp;&nbsp;
       (c) \( x^3 = 125 \) &nbsp;&nbsp; (d) \( \tfrac{8}{x-3} = 5 \)</p>
''' + LINS)
    + aufg(5, 'Verwechslungsgefahr', 2, r'''    <p>Worin unterscheiden sich \( x^4 = 81 \) und \( 4^x = 81 \)? Gib zu beiden Typ und
    Lösungsmenge an.</p>
''' + LINS)
    + aufg(6, 'Definitionsmenge zuerst', 2, r'''    <p>Bestimme die Definitionsmenge:</p>
    <p>(a) \( \tfrac{5}{x-3} = x \) &nbsp;&nbsp; (b) \( \sqrt{2x-8} = 3 \) &nbsp;&nbsp;
       (c) \( \lg(x+2) = 1 \)</p>
''' + LINS)
    + '  <div class="gruppe-titel">Quer durch die Typen</div>\n'
    + aufg(7, 'Linear', 1, r'''    <p>Löse \( 5x - 4 = 3x + 5 \) mit Probe.</p>
''' + LINS)
    + aufg(8, 'Quadratisch', 2, r'''    <p>Löse \( x^2 - 5x + 6 = 0 \) durch Faktorisieren; Kontrolle mit Vieta.</p>
''' + LINS)
    + aufg(9, 'Rational', 2, r'''    <p>Löse \( \tfrac{12}{x} = 3 \) (mit \(D\)).</p>
''' + LINS)
    + aufg(10, 'Wurzel', 2, r'''    <p>Löse \( \sqrt{x} + 1 = 5 \) mit Probe.</p>
''' + LINS)
    + aufg(11, 'Exponentiell', 2, r'''    <p>Löse \( 2^x = 32 \) durch Exponentenvergleich.</p>
''' + LINS)
    + aufg(12, 'Fehlersuche', 3, r'''    <p>Finde den Fehler: \( x^2 = 4x \ \mid : x \ \Rightarrow\ x = 4 \Rightarrow L = \{4\} \).</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Äquivalenzumformungen</strong> · <strong>Definitions</strong>menge ·
    <strong>Ausgangs</strong>gleichung.</p>''')
    + loes(2, r'''    <p>(a) äquivalent · (b) Scheinlösungs-Gefahr (Vorzeichen geht verloren) ·
    (c) Verlust-Gefahr (\( x = 0 \) wird getilgt).</p>''')
    + loes(3, r'''    <p>(a) allgemeingültig: \( L = \mathbb{R} \) (Identität) · (b) unlösbar: \( L = \{\,\} \).</p>''')
    + loes(4, r'''    <p>(a) Wurzelgleichung · (b) Exponentialgleichung (\(x\) im Exponenten) ·
    (c) Potenzgleichung (\(x\) in der Basis) · (d) rationale Gleichung.</p>''')
    + loes(5, r'''    <p>\( x^4 = 81 \): Potenzgleichung, \( L = \{-3;\ 3\} \) (gerader Exponent!) ·
    \( 4^x = 81 \): Exponentialgleichung, \( L = \{\log_4 81\} \approx \{3.17\} \) — genau eine Lösung.</p>''')
    + loes(6, r'''    <p>(a) \( D = \mathbb{R} \setminus \{3\} \) · (b) \( 2x - 8 \geq 0 \Rightarrow x \geq 4 \) ·
    (c) \( x + 2 > 0 \Rightarrow x > -2 \).</p>''')
    + loes(7, r'''    <p>\( 2x = 9 \Rightarrow x = 4.5 \). Probe: \( 18.5 = 18.5 \) ✓</p>''')
    + loes(8, r'''    <p>\( (x-2)(x-3) = 0 \Rightarrow L = \{2;\ 3\} \). Vieta: Produkt \(6\) ✓, Summe \(5\) ✓</p>''')
    + loes(9, r'''    <p>\( D: x \neq 0 \); \( 12 = 3x \Rightarrow x = 4 \in D \): \( L = \{4\} \).</p>''')
    + loes(10, r'''    <p>\( \sqrt{x} = 4 \Rightarrow x = 16 \). Probe: \( 4 + 1 = 5 \) ✓</p>''')
    + loes(11, r'''    <p>\( 2^x = 2^5 \Rightarrow x = 5 \).</p>''')
    + loes(12, r'''    <p>Die Division durch \(x\) hat die Lösung \( x = 0 \) vernichtet. Korrekt:
    \( x(x-4) = 0 \Rightarrow L = \{0;\ 4\} \).</p>''')
)

K_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Bei jeder Aufgabe
    gehört dazu: Gleichung aufstellen, <strong>Typ benennen</strong>, lösen und die Lösung auf
    <strong>Plausibilität</strong> prüfen. Die Musterlösungen folgen am Ende des Dokuments.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Alltag</td><td>Zwei Handy-Abos</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Geometrie</td><td>Rechteck gesucht</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Konstruktion</td><td>Kegel umgekehrt</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Physik</td><td>Fallhöhe</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Finanzen</td><td>Sparziel</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Werkstatt</td><td>Toleranz-Check</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Zwei Handy-Abos', 2, r'''    <p>Abo A: \(25\) CHF plus \(0.40\) CHF pro Einheit; Abo B: \(40\) CHF plus \(0.25\) CHF
    pro Einheit.</p>
    <p>(a) Stelle die Gleichung für «gleich teuer» auf und benenne den Typ.</p>
    <p>(b) Löse sie und gib die gemeinsamen Kosten an.</p>
    <p>(c) Ab wann lohnt sich B? (Blick voraus: Ungleichung.)</p>
''' + LINS4, tag='Alltag')
    + aufg(2, 'Rechteck gesucht', 2, r'''    <p>Ein Rechteck hat Umfang \(28\) cm und Flächeninhalt \(48\ \text{cm}^2\).</p>
    <p>(a) Stelle mit der Breite \(x\) eine Gleichung auf. Welcher Typ?</p>
    <p>(b) Löse sie und deute beide Lösungen.</p>
''' + LINS4, tag='Geometrie')
    + aufg(3, 'Kegel umgekehrt', 2, r'''    <p>Für einen Kegel gilt \( V = \tfrac{1}{3}\pi r^2 h \); gegeben \( V = 100\ \text{cm}^3 \),
    \( h = 12 \) cm.</p>
    <p>(a) Stelle die Gleichung für \(r\) auf und benenne den Typ.</p>
    <p>(b) Löse sie — welche Lösung ist plausibel?</p>
''' + LINS4, tag='Konstruktion')
    + aufg(4, 'Fallhöhe', 3, r'''    <p>Ein Stein fällt \( t = \sqrt{2h/g} \) Sekunden aus der Höhe \(h\) (\( g = 9.81\ \text{m/s}^2 \)).
    Gemessen werden \( 2.5 \) s.</p>
    <p>(a) Stelle die Gleichung für \(h\) auf und benenne den Typ.</p>
    <p>(b) Löse sie (Wurzel separieren, quadrieren) und prüfe die Grössenordnung.</p>
''' + LINS4, tag='Physik')
    + aufg(5, 'Sparziel', 3, r'''    <p>Ein Konto mit \( 8000 \) CHF wird zu \(2\) % verzinst: \( K(n) = 8000 \cdot 1.02^n \).
    Ziel sind \( 10\,000 \) CHF.</p>
    <p>(a) Stelle die Gleichung auf und benenne den Typ.</p>
    <p>(b) Löse sie exakt und runde sinnvoll.</p>
''' + LINS4, tag='Finanzen')
    + aufg(6, 'Toleranz-Check', 3, r'''    <p>Ein Bolzen hat Sollmass \(12\) mm; zulässig ist eine Abweichung von höchstens
    \( 0.05 \) mm.</p>
    <p>(a) Für welche Durchmesser \(d\) gilt exakt Grenzmass? Stelle die Gleichung auf
    (Typ?) und löse sie.</p>
    <p>(b) Formuliere den brauchbaren Bereich als Ungleichung und als Intervall.</p>
''' + LINS4, tag='Werkstatt')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( 25 + 0.4x = 40 + 0.25x \) — <strong>linear</strong>.</p>
    <p>(b) \( 0.15x = 15 \Rightarrow x = 100 \) Einheiten; Kosten \(65\) CHF (Probe mit B ✓).</p>
    <p>(c) \( 40 + 0.25x < 25 + 0.4x \Rightarrow x > 100 \).</p>''')
    + loes(2, r'''    <p>(a) Länge \( 14 - x \): \( x(14-x) = 48 \) — <strong>quadratisch</strong>.</p>
    <p>(b) \( x^2 - 14x + 48 = 0 \Rightarrow (x-6)(x-8) = 0 \) — beide Lösungen beschreiben
    dasselbe Rechteck mit Seiten \(6\) und \(8\) cm (Probe: \(48\ \text{cm}^2\), \(28\) cm ✓).</p>''')
    + loes(3, r'''    <p>(a) \( r^2 = \tfrac{3V}{\pi h} = \tfrac{300}{12\pi} \) — <strong>Potenzgleichung</strong>
    (gerader Exponent).</p>
    <p>(b) \( r = \pm 2.82 \) cm; plausibel ist nur der positive Radius.</p>''')
    + loes(4, r'''    <p>(a) \( \sqrt{2h/9.81} = 2.5 \) — <strong>Wurzelgleichung</strong>.</p>
    <p>(b) Quadrieren: \( \tfrac{2h}{9.81} = 6.25 \Rightarrow h = \tfrac{9.81 \cdot 6.25}{2}
    \approx 30.7 \) m — etwa ein zehnstöckiges Haus, plausibel.</p>''')
    + loes(5, r'''    <p>(a) \( 8000 \cdot 1.02^n = 10\,000 \) — <strong>Exponentialgleichung</strong>.</p>
    <p>(b) \( 1.02^n = 1.25 \Rightarrow n = \tfrac{\ln 1.25}{\ln 1.02} \approx 11.3 \) —
    nach \(12\) vollen Jahren ist das Ziel erreicht.</p>''')
    + loes(6, r'''    <p>(a) \( |d - 12| = 0.05 \) — <strong>Betragsgleichung</strong>, zwei Fälle:
    \( d = 11.95 \) oder \( d = 12.05 \) mm.</p>
    <p>(b) \( |d - 12| \leq 0.05 \), also \( d \in [11.95;\ 12.05] \) mm.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s3-6  BETRAGSFUNKTIONEN (ERGÄNZUNG TALS)
# ═══════════════════════════════════════════════════════════════════

L_HANDOUT = r'''
  <h2>1. Definition</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Betragsfunktion</div>
    <p>\( f : \mathbb{R} \to \mathbb{R}_0^+ \) mit
    \( f(x) = |x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases} \) —
    <strong>abschnittsweise linear</strong>, Graph ist ein V.</p>
  </div>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\(D\) / \(W\)</td><td>\( \mathbb{R} \) / \( \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Nullstelle</td><td>\( x_0 = 0 \)</td></tr>
      <tr><td class="li">Symmetrie</td><td class="li">gerade Funktion (\( |-x| = |x| \)), achsensymmetrisch zur \(y\)-Achse</td></tr>
      <tr><td class="li">Knickpunkt</td><td>\( (0 \mid 0) \) — Steigungswechsel von \(-1\) auf \(+1\)</td></tr>
    </tbody>
  </table>
  <p><em>Hinweis: Teilgebiet 3.6 ist eine Ergänzung des TALS-Lehrmittels und kein
  RLP-2030-Teilgebiet.</em></p>

  <h2>2. Transformationen \( y = a \cdot |x-u| + v \)</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Knickpunkt</td><td>\( (u \mid v) \) — Rolle des Parabel-Scheitels; Symmetrieachse \( x = u \)</td></tr>
      <tr><td class="li">Ast-Steigungen</td><td>\( \pm a \) — grosses \(|a|\): spitzes V; \( a < 0 \): Dach (Öffnung unten)</td></tr>
      <tr><td class="li">Nullstellen</td><td>\( x = u \pm |v/a| \), falls Knick auf der «falschen» Seite der Achse liegt</td></tr>
    </tbody>
  </table>

  <h2>3. Das Umklapp-Prinzip: \( y = |f(x)| \)</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Von \(f\) zu \(|f|\)</div>
    <p>Alle Kurventeile <strong>unterhalb</strong> der \(x\)-Achse an der \(x\)-Achse nach oben
    spiegeln; Teile oberhalb bleiben. An den <strong>Nullstellen von \(f\)</strong> entstehen Knicke.
    Beispiele: Gerade → V; Parabel \( x^2 - 4 \) → <strong>W</strong> (Scheitel \( (0 \mid -4) \)
    wird Buckel \( (0 \mid 4) \)); \( x^2 + 1 \) bleibt unverändert (nie negativ).</p>
  </div>

  <h2>4. Abschnittsweise schreiben</h2>
  <p>Fallunterscheidung an der Nullstelle des <strong>Arguments</strong>:</p>
  \[ |2x - 6| = \begin{cases} 2x - 6 & x \geq 3 \\ -2x + 6 & x < 3 \end{cases} \]
  <p>Der Knick liegt bei \( x = 3 \) (Argument-Nullstelle), nicht bei \(6\)! Es gilt
  \( |2x-6| = 2\,|x-3| \).</p>

  <h2>5. Gleichungen und Ungleichungen grafisch</h2>
  <p>\( |T(x)| = c \): Schnittstellen der Betragskurve mit der Horizontalen \( y = c \) — die
  <strong>Skizze verrät die Lösungsanzahl</strong> (z.B. hat \( |x^2-4| = 3 \) <em>vier</em>
  Lösungen: \( \pm 1, \pm\sqrt{7} \)). Ungleichungen: oberhalb/unterhalb ablesen
  (\( |x+1| > 2 \Rightarrow x < -3 \vee x > 1 \)).</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Das V von \( a|x-u|+v \) hat seinen <strong>Knick bei \( (u \mid v) \)</strong> und
    Ast-Steigungen \( \pm a \). Für beliebige \(f\) gilt das <strong>Umklapp-Prinzip</strong>
    mit Knicken an den Nullstellen. Betragsstriche verschwinden per Fallunterscheidung —
    und die Skizze zählt die Lösungen, bevor gerechnet wird.</p>
  </div>
'''

L_FORMELAUSZUG = r'''
  <h2>1. Betragsfunktion</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Definition</td><td>\( |x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases} \)</td></tr>
      <tr><td class="li">\(D\) / \(W\)</td><td>\( \mathbb{R} \) / \( \mathbb{R}_0^+ \)</td></tr>
      <tr><td class="li">Symmetrie</td><td class="li">gerade Funktion — achsensymmetrisch zur \(y\)-Achse</td></tr>
      <tr><td class="li">Knick</td><td>\( (0 \mid 0) \), Steigungen \( \pm 1 \)</td></tr>
    </tbody>
  </table>

  <h2>2. Transformierte Form</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Gleichung</td><td>\( y = a \cdot |x - u| + v \)</td></tr>
      <tr><td class="li">Knickpunkt</td><td>\( (u \mid v) \), Symmetrieachse \( x = u \)</td></tr>
      <tr><td class="li">Ast-Steigungen</td><td>\( \pm a \); \( a < 0 \): Öffnung nach unten</td></tr>
      <tr><td class="li">Nullstellen (falls vorhanden)</td><td>\( a|x-u| + v = 0 \Rightarrow x = u \pm \left|\tfrac{v}{a}\right| \)</td></tr>
      <tr><td class="li">Betrag einer Geraden</td><td>\( |mx + b| \): Knick bei \( x = -\tfrac{b}{m} \), Steigungen \( \pm|m| \)</td></tr>
    </tbody>
  </table>

  <h2>3. Umklapp-Prinzip</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( y = |f(x)| \)</td><td class="li">negative Teile von \(f\) an der \(x\)-Achse hochspiegeln</td></tr>
      <tr><td class="li">Knicke</td><td class="li">an den Nullstellen von \(f\)</td></tr>
      <tr><td class="li">Parabel mit 2 Nullstellen</td><td class="li">W-Form; geklappter Scheitel wird lokaler Hochpunkt</td></tr>
      <tr><td class="li">\( f > 0 \) überall</td><td>\( |f| = f \) — nichts zu klappen</td></tr>
    </tbody>
  </table>

  <h2>4. Abschnittsweise Form</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Grenze</td><td class="li">Nullstelle des Arguments</td></tr>
      <tr><td class="li">Beispiel</td><td>\( |2x-6| = \begin{cases} 2x-6 & x \geq 3 \\ -2x+6 & x < 3 \end{cases} \)</td></tr>
      <tr><td class="li">Faktor herausziehen</td><td>\( |2x - 6| = 2\,|x - 3| \)</td></tr>
    </tbody>
  </table>

  <h2>5. Gleichungen / Ungleichungen (vgl. 2.2c)</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">\( |T(x)| = c > 0 \)</td><td>\( T(x) = \pm c \); grafisch: Schnitt mit \( y = c \)</td></tr>
      <tr><td class="li">\( |x - m| \leq r \)</td><td>\( [m - r;\ m + r] \)</td></tr>
      <tr><td class="li">\( |x - m| > r \)</td><td>\( x < m-r \ \vee\ x > m+r \)</td></tr>
    </tbody>
  </table>
'''

L_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Die Betragsfunktion ist abschnittsweise <span class="lueck"></span>;<br>
      ihr Graph ist ein V mit <span class="lueck"></span>punkt bei \( (0 \mid 0) \)<br>
      und den Ast-Steigungen <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Werte berechnen', 1, r'''    <p>Berechne: (a) \( f(-4) \) für \( f(x) = |x| \) &nbsp;&nbsp;
    (b) \( g(1) \) für \( g(x) = |2x - 6| \) &nbsp;&nbsp; (c) \( h(0) \) für \( h(x) = |x - 3| + 2 \)</p>
''' + LINS)
    + aufg(3, 'Eigenschaften', 1, r'''    <p>Gib für \( y = |x| \) an: Definitionsmenge, Wertemenge, Symmetrie.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Transformationen</div>\n'
    + aufg(4, 'Knickpunkt ablesen', 1, r'''    <p>Wo liegt der Knickpunkt? (a) \( y = |x - 5| \) &nbsp;&nbsp;
    (b) \( y = |x + 2| - 3 \) &nbsp;&nbsp; (c) \( y = 2|x| + 1 \)</p>
''' + LINS)
    + aufg(5, 'Gleichung aufstellen', 2, r'''    <p>Gib die Gleichung der V-Kurve mit Knick \( (3 \mid -2) \) und Ast-Steigungen \( \pm 1 \) an
    und berechne ihre Nullstellen.</p>
''' + LINS)
    + aufg(6, 'Knick an der richtigen Stelle', 2, r'''    <p>Wo knickt der Graph von \( y = |3x + 9| \)? Schreibe die Funktion in der Form
    \( a|x - u| \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Umklapp-Prinzip</div>\n'
    + aufg(7, 'Gerade umklappen', 2, r'''    <p>Skizziere \( y = |x - 2| \), ausgehend von der Geraden \( y = x - 2 \). Wo entsteht
    der Knick?</p>
''' + LINS)
    + aufg(8, 'Parabel umklappen', 2, r'''    <p>Skizziere \( y = |x^2 - 4| \). Welche Form entsteht, und wohin klappt der Scheitel?</p>
''' + LINS)
    + aufg(9, 'Nichts zu klappen?', 2, r'''    <p>Warum gilt \( |x^2 + 1| = x^2 + 1 \) für alle \(x\)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Abschnittsweise und Gleichungen</div>\n'
    + aufg(10, 'Abschnittsweise schreiben', 3, r'''    <p>Schreibe \( y = |2x - 6| \) ohne Betragsstriche (zwei Abschnitte mit Bedingung).</p>
''' + LINS)
    + aufg(11, 'Gleichung grafisch', 3, r'''    <p>Wie viele Lösungen hat \( |x^2 - 4| = 3 \)? Skizziere und berechne alle.</p>
''' + LINS)
    + aufg(12, 'Ungleichung', 3, r'''    <p>Löse \( |x + 1| > 2 \) grafisch und algebraisch.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>linear</strong> · <strong>Knick</strong>punkt · <strong>\( \pm 1 \)</strong>.</p>''')
    + loes(2, r'''    <p>(a) \( 4 \) · (b) \( |{-4}| = 4 \) · (c) \( |-3| + 2 = 5 \).</p>''')
    + loes(3, r'''    <p>\( D = \mathbb{R} \), \( W = \mathbb{R}_0^+ \); gerade Funktion —
    achsensymmetrisch zur \(y\)-Achse.</p>''')
    + loes(4, r'''    <p>(a) \( (5 \mid 0) \) · (b) \( (-2 \mid -3) \) · (c) \( (0 \mid 1) \).</p>''')
    + loes(5, r'''    <p>\( y = |x - 3| - 2 \); Nullstellen: \( |x-3| = 2 \Rightarrow x = 1 \) und \( x = 5 \).</p>''')
    + loes(6, r'''    <p>Argument null: \( 3x + 9 = 0 \Rightarrow x = -3 \) — Knick bei \( (-3 \mid 0) \);
    \( |3x + 9| = 3\,|x + 3| \).</p>''')
    + loes(7, r'''    <p>Der Teil der Geraden links von \( x = 2 \) (dort negativ) wird hochgeklappt —
    Knick an der Nullstelle \( (2 \mid 0) \), V mit Steigungen \( \pm 1 \).</p>''')
    + loes(8, r'''    <p>Ein <strong>W</strong>: Der Parabelbogen zwischen den Nullstellen \( \pm 2 \) klappt
    nach oben; der Scheitel \( (0 \mid -4) \) wird zum Buckel \( (0 \mid 4) \).</p>''')
    + loes(9, r'''    <p>\( x^2 + 1 \geq 1 > 0 \) — die Funktion hat keine negativen Werte, der Betrag
    ändert nichts.</p>''')
    + loes(10, r'''    <p>\( |2x-6| = \begin{cases} 2x-6 & x \geq 3 \\ -2x+6 & x < 3 \end{cases} \) —
    Grenze an der Argument-Nullstelle \( x = 3 \).</p>''')
    + loes(11, r'''    <p>Vier (Skizze: Horizontale \( y = 3 \) schneidet das W viermal):
    \( x^2 - 4 = 3 \Rightarrow x = \pm\sqrt{7} \) und \( x^2 - 4 = -3 \Rightarrow x = \pm 1 \).</p>''')
    + loes(12, r'''    <p>Schnittstellen \( x + 1 = \pm 2 \Rightarrow x = -3, 1 \); das V liegt aussen
    oberhalb: \( L = \{x \mid x < -3 \ \vee\ x > 1\} \).</p>''')
)

L_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben aus Technik und Alltag, nach zunehmendem Schwierigkeitsgrad
    geordnet. Die Musterlösungen folgen am Ende des Dokuments. Immer zuerst skizzieren —
    das V bzw. W zeigt Lösungsanzahl und Lage.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Verkehr</td><td>Abstand zum Bahnhof</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Fertigung</td><td>Kosten der Abweichung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Elektrotechnik</td><td>Spannungstoleranz</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Logistik</td><td>Der beste Standort</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Maschinenbau</td><td>Materialabtrag</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Mathematik</td><td>Lösungsanzahl am W</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Abstand zum Bahnhof', 2, r'''    <p>Auf einer geraden Strasse liegt der Bahnhof bei km \(6\); der Abstand einer Position
    \(x\) ist \( a(x) = |x - 6| \).</p>
    <p>(a) Skizziere \(a(x)\) für \( 0 \leq x \leq 12 \) und beschrifte den Knick.</p>
    <p>(b) Berechne \( a(2) \) und \( a(9) \).</p>
    <p>(c) Welche Positionen haben Abstand \(4\) km? (Gleichung und Skizze.)</p>
''' + LINS4, tag='Verkehr')
    + aufg(2, 'Kosten der Abweichung', 2, r'''    <p>Eine Abfüllanlage (Soll \(500\) ml) verursacht Abweichungskosten
    \( K(x) = 0.5 \cdot |x - 500| \) (Rappen pro Flasche).</p>
    <p>(a) Deute den Knickpunkt der Kostenfunktion.</p>
    <p>(b) Berechne \( K(508) \).</p>
    <p>(c) Für welche Füllmengen bleiben die Kosten unter \(3\) Rappen?</p>
''' + LINS4, tag='Fertigung')
    + aufg(3, 'Spannungstoleranz', 2, r'''    <p>Ein Netzteil soll \(12\) V liefern; zulässig ist \( |U - 12| \leq 0.5 \) V.</p>
    <p>(a) Skizziere die Abweichungsfunktion \( f(U) = |U - 12| \) samt Toleranzgrenze.</p>
    <p>(b) Gib den zulässigen Bereich als Intervall an.</p>
    <p>(c) Ist \( U = 12.6 \) V zulässig?</p>
''' + LINS4, tag='Elektrotechnik')
    + aufg(4, 'Der beste Standort', 3, r'''    <p>Ari wohnt bei km \(2\), Bea bei km \(8\); der Gesamtweg zu einem Treffpunkt \(x\) ist
    \( d(x) = |x - 2| + |x - 8| \).</p>
    <p>(a) Berechne \( d(0) \), \( d(5) \), \( d(10) \).</p>
    <p>(b) Schreibe \( d(x) \) abschnittsweise (drei Abschnitte).</p>
    <p>(c) Wo ist der Gesamtweg minimal? Begründe mit der abschnittsweisen Form.</p>
''' + LINS4, tag='Logistik')
    + aufg(5, 'Materialabtrag', 3, r'''    <p>Ein Werkstückprofil weicht um \( f(x) = x^2 - 4 \) (mm) vom Soll ab; die Fräse trägt
    \( A(x) = |x^2 - 4| \) ab (\( -3 \leq x \leq 3 \), \(x\) in cm).</p>
    <p>(a) Skizziere \( A(x) \) — welche Form entsteht?</p>
    <p>(b) Berechne den Abtrag bei \( x = 1 \) und \( x = 3 \).</p>
    <p>(c) Wo ist nichts abzutragen, und wo ist der Abtrag im Innenbereich maximal?</p>
''' + LINS4, tag='Maschinenbau')
    + aufg(6, 'Lösungsanzahl am W', 3, r'''    <p>Betrachte die Gleichung \( |x^2 - 4| = c \) mit dem Parameter \( c \geq 0 \).</p>
    <p>(a) Skizziere \( y = |x^2 - 4| \) und verschiedene Horizontalen \( y = c \).</p>
    <p>(b) Für welche \(c\) gibt es vier, drei bzw. zwei Lösungen?</p>
    <p>(c) Berechne alle Lösungen für \( c = 3 \).</p>
''' + LINS4, tag='Mathematik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) V mit Knick \( (6 \mid 0) \), Steigungen \( \pm 1 \).</p>
    <p>(b) \( a(2) = 4 \) km, \( a(9) = 3 \) km.</p>
    <p>(c) \( |x - 6| = 4 \Rightarrow x = 2 \) oder \( x = 10 \) — symmetrisch um den Bahnhof.</p>''')
    + loes(2, r'''    <p>(a) Knick \( (500 \mid 0) \): exakte Füllmenge kostet nichts, jede Abweichung
    symmetrisch mehr.</p>
    <p>(b) \( K(508) = 0.5 \cdot 8 = 4 \) Rappen.</p>
    <p>(c) \( 0.5|x-500| < 3 \Rightarrow |x-500| < 6 \Rightarrow 494 < x < 506 \) ml.</p>''')
    + loes(3, r'''    <p>(a) V mit Knick \( (12 \mid 0) \), Toleranzgrenze als Horizontale \( y = 0.5 \).</p>
    <p>(b) \( [11.5;\ 12.5] \) V.</p>
    <p>(c) \( |12.6 - 12| = 0.6 > 0.5 \) — nicht zulässig.</p>''')
    + loes(4, r'''    <p>(a) \( d(0) = 10 \), \( d(5) = 6 \), \( d(10) = 10 \) km.</p>
    <p>(b) \( x < 2 \): \( -2x + 10 \); \( 2 \leq x \leq 8 \): \( 6 \); \( x > 8 \): \( 2x - 10 \).</p>
    <p>(c) Im mittleren Abschnitt ist \(d\) konstant \(6\) — <strong>jeder</strong> Punkt
    zwischen den Wohnorten ist optimal («Wanne mit flachem Boden»).</p>''')
    + loes(5, r'''    <p>(a) Ein <strong>W</strong> — die Parabel zwischen \( \pm 2 \) hochgeklappt.</p>
    <p>(b) \( A(1) = 3 \) mm, \( A(3) = 5 \) mm.</p>
    <p>(c) Nichts bei \( x = \pm 2 \) (Nullstellen); im Innenbereich maximal beim geklappten
    Scheitel: \( A(0) = 4 \) mm.</p>''')
    + loes(6, r'''    <p>(b) Vier Lösungen für \( 0 < c < 4 \), drei für \( c = 4 \) (Berührung am Buckel),
    zwei für \( c > 4 \) oder \( c = 0 \).</p>
    <p>(c) \( x^2 - 4 = \pm 3 \Rightarrow x = \pm\sqrt{7} \approx \pm 2.65 \) und
    \( x = \pm 1 \).</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s4-3a  VEKTORBEGRIFF UND KOMPONENTEN
# ═══════════════════════════════════════════════════════════════════

M_HANDOUT = r'''
  <h2>1. Vektorbegriff</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Vektor</div>
    <p>Ein <strong>Vektor</strong> \( \vec{a} \) ist die Klasse aller Pfeile gleicher Länge und
    Richtung — eine <strong>Verschiebung</strong> ohne festen Ort. Skalare Grössen (Masse, Zeit)
    brauchen nur eine Zahl; vektorielle (Kraft, Geschwindigkeit) zusätzlich eine Richtung.</p>
  </div>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Betrag (Norm)</td><td>\( |\vec{a}| \geq 0 \) — die Pfeillänge</td></tr>
      <tr><td class="li">Nullvektor / Gegenvektor</td><td>\( \vec{0} \) (Länge 0) · \( -\vec{a} \) (umgedreht); \( \vec{a} + (-\vec{a}) = \vec{0} \)</td></tr>
      <tr><td class="li">kollinear</td><td>\( \vec{b} = s\,\vec{a} \) — parallele Pfeile (gleicher Faktor in allen Komponenten)</td></tr>
    </tbody>
  </table>

  <h2>2. Operationen</h2>
  <p><strong>Addition:</strong> Pfeile aneinanderhängen (oder Parallelogramm) ·
  <strong>Subtraktion:</strong> Gegenvektor addieren · <strong>skalare Multiplikation:</strong>
  strecken (\( s < 0 \): umdrehen). Komponentenweise:</p>
  \[ \binom{a_1}{a_2} \pm \binom{b_1}{b_2} = \binom{a_1 \pm b_1}{a_2 \pm b_2}, \qquad
     s\binom{a_1}{a_2} = \binom{s a_1}{s a_2} \]

  <h2>3. Komponenten, Ortsvektor, Betrag</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Ortsvektor</td><td>\( \vec{r}_A = \vec{OA} \) — Komponenten = Koordinaten von \(A\)</td></tr>
      <tr><td class="li">Verbindungsvektor</td><td>\( \vec{AB} = \vec{r}_B - \vec{r}_A \) — «Spitze minus Fuss»</td></tr>
      <tr><td class="li">Betrag (Ebene / Raum)</td><td>\( |\vec{a}| = \sqrt{a_1^2 + a_2^2} \) bzw. \( \sqrt{a_1^2 + a_2^2 + a_3^2} \)</td></tr>
      <tr><td class="li">Mittelpunkt / Schwerpunkt</td><td>\( \vec{r}_M = \tfrac{1}{2}(\vec{r}_A + \vec{r}_B) \) · \( \vec{r}_S = \tfrac{1}{3}(\vec{r}_A + \vec{r}_B + \vec{r}_C) \)</td></tr>
    </tbody>
  </table>

  <h2>4. Polarform (nur Ebene)</h2>
  <p>polar → kartesisch: \( a_1 = r\cos\varphi \), \( a_2 = r\sin\varphi \) ·
  kartesisch → polar: \( r = \sqrt{a_1^2 + a_2^2} \), \( \tan\varphi = a_2/a_1 \) —
  <strong>Quadrant an den Vorzeichen prüfen</strong> (2./3. Quadrant: \( 180° \) addieren).</p>

  <h2>5. Einheitsvektor und Linearkombination</h2>
  <p><strong>Normieren:</strong> \( \vec{e}_a = \vec{a}/|\vec{a}| \) (Betrag 1, gleiche Richtung).
  <strong>Linearkombination:</strong> \( \vec{c} = s\,\vec{a} + t\,\vec{b} \) — bei nicht
  kollinearen \( \vec{a}, \vec{b} \) ist jeder ebene Vektor eindeutig zerlegbar
  (Gleichungssystem in \(s\), \(t\)).</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Komponentenweise rechnen, Betrag mit Pythagoras, Verbindungsvektor «Spitze minus Fuss»,
    Normieren durch die Länge teilen — und bei der Polarform immer den Quadranten kontrollieren.</p>
  </div>
'''

M_FORMELAUSZUG = r'''
  <h2>1. Grundformeln</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Verbindungsvektor</td><td>\( \vec{AB} = \vec{r}_B - \vec{r}_A \)</td></tr>
      <tr><td class="li">Betrag</td><td>\( |\vec{a}| = \sqrt{a_1^2 + a_2^2\ (+\,a_3^2)} \)</td></tr>
      <tr><td class="li">Einheitsvektor</td><td>\( \vec{e}_a = \dfrac{\vec{a}}{|\vec{a}|} \)</td></tr>
      <tr><td class="li">Kollinearität</td><td>\( \vec{b} = s\,\vec{a} \)</td></tr>
    </tbody>
  </table>

  <h2>2. Operationen (komponentenweise)</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Addition / Subtraktion</td><td>\( (a_i \pm b_i) \) je Komponente</td></tr>
      <tr><td class="li">skalare Multiplikation</td><td>\( (s\,a_i) \) je Komponente; \( s < 0 \) dreht die Richtung</td></tr>
      <tr><td class="li">Linearkombination</td><td>\( \vec{c} = s\,\vec{a} + t\,\vec{b} \) — LGS für \(s\), \(t\)</td></tr>
    </tbody>
  </table>

  <h2>3. Polarform (Ebene)</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">polar → kartesisch</td><td>\( a_1 = r\cos\varphi, \quad a_2 = r\sin\varphi \)</td></tr>
      <tr><td class="li">kartesisch → polar</td><td>\( r = \sqrt{a_1^2+a_2^2}, \quad \tan\varphi = a_2/a_1 \) (Quadrant!)</td></tr>
    </tbody>
  </table>

  <h2>4. Punkte aus Vektoren</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Mittelpunkt \(AB\)</td><td>\( \vec{r}_M = \tfrac{1}{2}(\vec{r}_A + \vec{r}_B) \)</td></tr>
      <tr><td class="li">Schwerpunkt \(ABC\)</td><td>\( \vec{r}_S = \tfrac{1}{3}(\vec{r}_A + \vec{r}_B + \vec{r}_C) \)</td></tr>
    </tbody>
  </table>
'''

M_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Ein Vektor hat <span class="lueck"></span> und <span class="lueck"></span>,<br>
      aber keinen festen Ort. Der Gegenvektor \( -\vec{a} \) ist gleich lang,<br>
      aber <span class="lueck"></span> gerichtet.
    </div>''')
    + aufg(2, 'Skalar oder Vektor?', 1, r'''    <p>Entscheide: (a) Temperatur &nbsp; (b) Windgeschwindigkeit &nbsp; (c) Masse &nbsp;
    (d) Kraft</p>
''' + LINS)
    + aufg(3, 'Komponenten ablesen', 1, r'''    <p>Ein Pfeil führt von \( A(1 \mid 3) \) nach \( B(4 \mid 1) \). Gib den Vektor
    \( \vec{AB} \) an.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Operationen</div>\n'
    + aufg(4, 'Komponentenweise rechnen', 1, r'''    <p>\( \vec{a} = \binom{3}{1} \), \( \vec{b} = \binom{1}{2} \). Berechne
    \( \vec{a} + \vec{b} \), \( \vec{a} - \vec{b} \) und \( 2\vec{a} \).</p>
''' + LINS)
    + aufg(5, 'Beträge', 2, r'''    <p>Berechne \( \left|\binom{3}{4}\right| \) und
    \( \left|\begin{pmatrix} 2 \\ -1 \\ 2 \end{pmatrix}\right| \).</p>
''' + LINS)
    + aufg(6, 'Kollinear?', 2, r'''    <p>Sind \( \binom{2}{3} \) und \( \binom{6}{9} \) kollinear? Und \( \binom{2}{3} \)
    und \( \binom{6}{8} \)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Polarform und Einheitsvektor</div>\n'
    + aufg(7, 'Polar → kartesisch', 2, r'''    <p>\( r = 6 \), \( \varphi = 30° \). Berechne die Komponenten.</p>
''' + LINS)
    + aufg(8, 'Kartesisch → polar', 2, r'''    <p>Gib \( \binom{3}{4} \) in Polarform an.</p>
''' + LINS)
    + aufg(9, 'Quadranten-Falle', 3, r'''    <p>Bestimme die Polarform von \( \binom{-2}{2} \) — Vorsicht beim Winkel!</p>
''' + LINS)
    + '  <div class="gruppe-titel">Zerlegung und Punkte</div>\n'
    + aufg(10, 'Normieren', 2, r'''    <p>Bestimme den Einheitsvektor zu \( \binom{3}{4} \).</p>
''' + LINS)
    + aufg(11, 'Linearkombination', 3, r'''    <p>Zerlege \( \vec{c} = \binom{5}{1} \) in die Richtungen \( \binom{2}{1} \) und
    \( \binom{1}{-1} \).</p>
''' + LINS)
    + aufg(12, 'Mittelpunkt im Raum', 3, r'''    <p>Berechne den Mittelpunkt der Strecke von \( A(1 \mid 2 \mid 3) \) nach
    \( B(5 \mid 0 \mid 1) \).</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Länge</strong> (Betrag) und <strong>Richtung</strong>;
    <strong>entgegengesetzt</strong>.</p>''')
    + loes(2, r'''    <p>(a) Skalar · (b) Vektor · (c) Skalar · (d) Vektor.</p>''')
    + loes(3, r'''    <p>\( \vec{AB} = \binom{4-1}{1-3} = \binom{3}{-2} \).</p>''')
    + loes(4, r'''    <p>\( \binom{4}{3} \), \( \binom{2}{-1} \), \( \binom{6}{2} \).</p>''')
    + loes(5, r'''    <p>\( \sqrt{9+16} = 5 \) und \( \sqrt{4+1+4} = 3 \).</p>''')
    + loes(6, r'''    <p>\( \binom{6}{9} = 3\binom{2}{3} \) — kollinear. \( \binom{6}{8} \): Faktor wäre 3
    bzw. \( \tfrac{8}{3} \) — nicht kollinear.</p>''')
    + loes(7, r'''    <p>\( a_1 = 6\cos 30° \approx 5.20 \), \( a_2 = 6\sin 30° = 3 \).</p>''')
    + loes(8, r'''    <p>\( r = 5 \), \( \varphi = \arctan\tfrac{4}{3} \approx 53.1° \).</p>''')
    + loes(9, r'''    <p>\( r = 2\sqrt{2} \approx 2.83 \); Rechner: \( \arctan(-1) = -45° \), aber
    2. Quadrant: \( \varphi = 135° \).</p>''')
    + loes(10, r'''    <p>\( |\vec{a}| = 5 \Rightarrow \vec{e}_a = \binom{0.6}{0.8} \).</p>''')
    + loes(11, r'''    <p>\( 2s + t = 5 \), \( s - t = 1 \Rightarrow s = 2 \), \( t = 1 \).</p>''')
    + loes(12, r'''    <p>\( M(3 \mid 1 \mid 2) \) — Mittelwert der Ortsvektoren.</p>''')
)

M_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Die Musterlösungen
    folgen am Ende des Dokuments. Skizze mit Pfeilen gehört zu jeder Vektoraufgabe!</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Nautik</td><td>Flussüberquerung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Mechanik</td><td>Zwei Kräfte am Haken</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Vermessung</td><td>Mittelpunkt und Schwerpunkt</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Aviatik</td><td>Wind und Kurs</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Statik</td><td>Kraft in zwei Stäbe zerlegen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Robotik</td><td>Greifarm in Schritten</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Flussüberquerung', 2, r'''    <p>Ein Boot hält mit \( 4\ \text{m/s} \) quer auf das Ufer zu; die Strömung schiebt mit
    \( 3\ \text{m/s} \) flussabwärts. Der Fluss ist \(60\) m breit.</p>
    <p>(a) Berechne Betrag und Richtung der resultierenden Geschwindigkeit.</p>
    <p>(b) Wie lange dauert die Überquerung, wie gross ist die Abdrift?</p>
    <p>(c) Wie lang ist der tatsächlich gefahrene Weg?</p>
''' + LINS4, tag='Nautik')
    + aufg(2, 'Zwei Kräfte am Haken', 2, r'''    <p>An einem Haken ziehen \( F_1 = 60 \) N horizontal und \( F_2 = 25 \) N vertikal.</p>
    <p>(a) Berechne den Betrag der resultierenden Kraft.</p>
    <p>(b) Unter welchem Winkel zur Horizontalen wirkt sie?</p>
    <p>(c) Welche dritte Kraft würde den Haken im Gleichgewicht halten?</p>
''' + LINS4, tag='Mechanik')
    + aufg(3, 'Mittelpunkt und Schwerpunkt', 2, r'''    <p>Drei Vermessungspunkte: \( A(1 \mid 2 \mid 3) \), \( B(5 \mid 0 \mid 1) \),
    \( C(0 \mid 4 \mid 2) \) (Koordinaten in km).</p>
    <p>(a) Berechne den Mittelpunkt der Strecke \(AB\).</p>
    <p>(b) Berechne den Schwerpunkt des Dreiecks \(ABC\).</p>
    <p>(c) Wie weit sind \(A\) und \(B\) voneinander entfernt?</p>
''' + LINS4, tag='Vermessung')
    + aufg(4, 'Wind und Kurs', 3, r'''    <p>Ein Flugzeug fliegt mit Eigengeschwindigkeit \( \binom{0}{200} \) km/h (nach Norden);
    der Wind weht mit \( \binom{50}{0} \) km/h (nach Osten).</p>
    <p>(a) Berechne den Geschwindigkeitsvektor über Grund und seinen Betrag.</p>
    <p>(b) Um welchen Winkel weicht der Kurs von Norden ab?</p>
    <p>(c) Wie weit kommt das Flugzeug in 1.5 Stunden?</p>
''' + LINS4, tag='Aviatik')
    + aufg(5, 'Kraft in zwei Stäbe zerlegen', 3, r'''    <p>Eine Kraft \( \vec{F} = \binom{5}{1} \) kN soll von zwei Stäben mit den Richtungen
    \( \vec{a} = \binom{2}{1} \) und \( \vec{b} = \binom{1}{-1} \) aufgenommen werden:
    \( \vec{F} = s\,\vec{a} + t\,\vec{b} \).</p>
    <p>(a) Stelle das Gleichungssystem auf.</p>
    <p>(b) Berechne \(s\) und \(t\).</p>
    <p>(c) Welche Kraftbeträge tragen die Stäbe (\( |s\vec{a}| \), \( |t\vec{b}| \))?</p>
''' + LINS4, tag='Statik')
    + aufg(6, 'Greifarm in Schritten', 3, r'''    <p>Ein Greifarm fährt vom Ursprung nacheinander die Verschiebungen
    \( \binom{3}{1} \), \( \binom{-1}{2} \) und \( \binom{2}{2} \) ab (in dm).</p>
    <p>(a) Wo steht der Greifer am Schluss?</p>
    <p>(b) Wie weit ist er (Luftlinie) vom Start entfernt?</p>
    <p>(c) Welcher einzelne Verschiebungsvektor hätte denselben Effekt — und was sagt das
    über die Vektoraddition?</p>
''' + LINS4, tag='Robotik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( |\vec{v}| = \sqrt{3^2+4^2} = 5\ \text{m/s} \), \( \approx 36.9° \) zur Querrichtung.</p>
    <p>(b) \( t = 60/4 = 15 \) s; Abdrift \( 3 \cdot 15 = 45 \) m.</p>
    <p>(c) \( 5 \cdot 15 = 75 \) m (oder \( \sqrt{60^2 + 45^2} = 75 \) ✓).</p>''')
    + loes(2, r'''    <p>(a) \( \sqrt{60^2 + 25^2} = 65 \) N.</p>
    <p>(b) \( \arctan(25/60) \approx 22.6° \).</p>
    <p>(c) Der Gegenvektor der Resultierenden: \(65\) N unter \( 22.6° \) in die
    Gegenrichtung.</p>''')
    + loes(3, r'''    <p>(a) \( M(3 \mid 1 \mid 2) \).</p>
    <p>(b) \( S(2 \mid 2 \mid 2) \).</p>
    <p>(c) \( |\vec{AB}| = |(4, -2, -2)| = \sqrt{24} \approx 4.9 \) km.</p>''')
    + loes(4, r'''    <p>(a) \( \binom{50}{200} \), Betrag \( \sqrt{2500 + 40000} \approx 206.2 \) km/h.</p>
    <p>(b) \( \arctan(50/200) \approx 14.0° \) nach Osten.</p>
    <p>(c) \( 206.2 \cdot 1.5 \approx 309 \) km.</p>''')
    + loes(5, r'''    <p>(a) \( 2s + t = 5 \), \( s - t = 1 \).</p>
    <p>(b) \( s = 2 \), \( t = 1 \).</p>
    <p>(c) \( |2\vec{a}| = 2\sqrt{5} \approx 4.47 \) kN, \( |1\,\vec{b}| = \sqrt{2} \approx 1.41 \) kN.</p>''')
    + loes(6, r'''    <p>(a) Summe \( \binom{4}{5} \) — Punkt \( (4 \mid 5) \).</p>
    <p>(b) \( \sqrt{16+25} = \sqrt{41} \approx 6.4 \) dm.</p>
    <p>(c) Genau \( \binom{4}{5} \) — die Reihenfolge der Teilschritte ist egal:
    Vektoraddition ist kommutativ und assoziativ.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s4-3b  SKALARPRODUKT
# ═══════════════════════════════════════════════════════════════════

N_HANDOUT = r'''
  <h2>1. Definition</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Skalarprodukt</div>
    <p>Geometrisch: \( \vec{a} \cdot \vec{b} = |\vec{a}|\,|\vec{b}|\cos\varphi \) (Zwischenwinkel
    \(\varphi\)) — komponentenweise: \( a_1b_1 + a_2b_2\ (+\,a_3b_3) \). Das Ergebnis ist eine
    <strong>Zahl</strong>: «Vektor · Vektor = Skalar». Spezialfall
    \( \vec{a} \cdot \vec{a} = |\vec{a}|^2 \).</p>
  </div>

  <h2>2. Winkel und Orthogonalität</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Winkelformel</td><td>\( \cos\varphi = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{a}|\,|\vec{b}|} \)</td></tr>
      <tr><td class="li">Vorzeichen</td><td class="li">\( > 0 \): spitz · \( = 0 \): <strong>orthogonal</strong> · \( < 0 \): stumpf</td></tr>
      <tr><td class="li">Grenzfälle</td><td>\( \varphi = 0°/180° \): kollinear, \( \pm|\vec{a}||\vec{b}| \)</td></tr>
    </tbody>
  </table>

  <h2>3. Rechenregeln</h2>
  <p>Kommutativ (\( \vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a} \)), distributiv,
  Skalare herausziehbar. <strong>Kein</strong> Assoziativgesetz — \( (\vec{a} \cdot \vec{b})\vec{c} \)
  ist ein Vektor; Division durch Vektoren ist sinnlos.</p>

  <h2>4. Normalprojektion</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Projektion («Schattenwurf»)</div>
    <p>\( \vec{a}_b = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2}\,\vec{b} \), Betrag
    \( |\vec{a}_b| = \dfrac{|\vec{a} \cdot \vec{b}|}{|\vec{b}|} \) — der wirksame Anteil von
    \( \vec{a} \) in Richtung \( \vec{b} \). Physik: Arbeit \( W = \vec{F} \cdot \vec{s} \).</p>
  </div>

  <h2>5. Winkel in Figuren</h2>
  <p>Innenwinkel bei Ecke \(A\): Vektoren <strong>von \(A\) weg</strong> (\( \vec{AB} \),
  \( \vec{AC} \)) in die Winkelformel. Falsche Pfeilrichtung liefert den Nebenwinkel
  \( 180° - \varphi \). Rechtwinkligkeit: Skalarprodukt der anliegenden Seitenvektoren gleich null.</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Produkte der Komponenten <strong>summieren</strong> — die Zahl verrät den Winkel:
    positiv/null/negativ = spitz/senkrecht/stumpf. Projektion = wirksamer Anteil.
    Bei Figuren: Pfeile von der Ecke weg.</p>
  </div>
'''

N_FORMELAUSZUG = r'''
  <h2>1. Skalarprodukt</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">geometrisch</td><td>\( \vec{a} \cdot \vec{b} = |\vec{a}|\,|\vec{b}|\cos\varphi \)</td></tr>
      <tr><td class="li">komponentenweise</td><td>\( a_1b_1 + a_2b_2\ (+\,a_3b_3) \)</td></tr>
      <tr><td class="li">mit sich selbst</td><td>\( \vec{a} \cdot \vec{a} = |\vec{a}|^2 \)</td></tr>
    </tbody>
  </table>

  <h2>2. Winkel</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Winkelformel</td><td>\( \cos\varphi = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{a}|\,|\vec{b}|} \)</td></tr>
      <tr><td class="li">Orthogonalität</td><td>\( \vec{a} \perp \vec{b} \Leftrightarrow \vec{a} \cdot \vec{b} = 0 \)</td></tr>
      <tr><td class="li">Vorzeichen-Klassierung</td><td class="li">\( > 0 \) spitz · \( = 0 \) recht · \( < 0 \) stumpf</td></tr>
      <tr><td class="li">2D-Normalen-Trick</td><td>\( \binom{a_1}{a_2} \perp \binom{-a_2}{a_1} \)</td></tr>
    </tbody>
  </table>

  <h2>3. Projektion und Arbeit</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Projektionsvektor</td><td>\( \vec{a}_b = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2}\,\vec{b} \)</td></tr>
      <tr><td class="li">Projektionsbetrag</td><td>\( |\vec{a}_b| = \dfrac{|\vec{a} \cdot \vec{b}|}{|\vec{b}|} \)</td></tr>
      <tr><td class="li">Arbeit (Physik)</td><td>\( W = \vec{F} \cdot \vec{s} = |\vec{F}|\,|\vec{s}|\cos\varphi \)</td></tr>
    </tbody>
  </table>

  <h2>4. Rechenregeln</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">kommutativ / distributiv</td><td>\( \vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a} \); \( \vec{a} \cdot (\vec{b}+\vec{c}) = \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c} \)</td></tr>
      <tr><td class="li">Skalar herausziehen</td><td>\( (s\vec{a}) \cdot \vec{b} = s(\vec{a} \cdot \vec{b}) \)</td></tr>
      <tr><td class="li">kein Assoziativgesetz</td><td class="li">\( (\vec{a} \cdot \vec{b})\,\vec{c} \) ist ein Vektor!</td></tr>
    </tbody>
  </table>
'''

N_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Definition vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Das Skalarprodukt zweier Vektoren ist eine <span class="lueck"></span>, kein Vektor.<br>
      Es ist null genau dann, wenn die Vektoren <span class="lueck"></span> stehen.<br>
      Komponentenweise: Produkte bilden und <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Skalarprodukte berechnen', 1, r'''    <p>(a) \( \binom{2}{5} \cdot \binom{4}{-1} \) &nbsp;&nbsp;
    (b) \( \binom{3}{0} \cdot \binom{0}{7} \) &nbsp;&nbsp;
    (c) \( \begin{pmatrix} 1 \\ 2 \\ 2 \end{pmatrix} \cdot \begin{pmatrix} 2 \\ -2 \\ 1 \end{pmatrix} \)</p>
''' + LINS)
    + aufg(3, 'Vorzeichen deuten', 1, r'''    <p>Was sagt das Vorzeichen von \( \vec{a} \cdot \vec{b} \) über den Zwischenwinkel?
    Gib alle drei Fälle an.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Winkel</div>\n'
    + aufg(4, 'Winkelformel', 2, r'''    <p>Berechne den Zwischenwinkel von \( \binom{4}{3} \) und \( \binom{5}{0} \).</p>
''' + LINS)
    + aufg(5, 'Exakter Winkel', 2, r'''    <p>Zeige, dass \( \binom{1}{2} \) und \( \binom{3}{1} \) den Winkel \( 45° \)
    einschliessen.</p>
''' + LINS)
    + aufg(6, 'Orthogonalität erzwingen', 2, r'''    <p>Für welches \(k\) steht \( \binom{3}{k} \) senkrecht auf \( \binom{2}{4} \)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Projektion</div>\n'
    + aufg(7, 'Projektion berechnen', 2, r'''    <p>Projiziere \( \binom{4}{2} \) auf \( \binom{3}{0} \): Projektionsvektor und Betrag.</p>
''' + LINS)
    + aufg(8, 'Arbeit', 2, r'''    <p>\( F = 50 \) N, \( s = 8 \) m, Winkel \( 60° \). Berechne die Arbeit.</p>
''' + LINS)
    + aufg(9, 'Projektion senkrecht', 2, r'''    <p>Was ist die Projektion von \( \vec{a} \) auf \( \vec{b} \), wenn
    \( \vec{a} \perp \vec{b} \)?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Figuren</div>\n'
    + aufg(10, 'Innenwinkel', 3, r'''    <p>Berechne den Innenwinkel bei \( A(1 \mid 1) \) im Dreieck mit \( B(5 \mid 2) \),
    \( C(2 \mid 4) \).</p>
''' + LINS)
    + aufg(11, 'Rechtwinklig?', 3, r'''    <p>Zeige: Das Dreieck \( A(0 \mid 0) \), \( B(4 \mid 2) \), \( C(3 \mid 4) \) ist
    rechtwinklig. Wo liegt der rechte Winkel?</p>
''' + LINS)
    + aufg(12, 'Würfeldiagonale', 3, r'''    <p>Berechne den Winkel zwischen der Raumdiagonale \( (1 \mid 1 \mid 1) \) eines
    Einheitswürfels und einer Kante.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Zahl</strong> (Skalar) · <strong>senkrecht</strong> (orthogonal) ·
    <strong>summieren</strong>.</p>''')
    + loes(2, r'''    <p>(a) \( 8 - 5 = 3 \) · (b) \( 0 \) (Achsen stehen senkrecht) · (c) \( 2 - 4 + 2 = 0 \).</p>''')
    + loes(3, r'''    <p>\( > 0 \): spitzer Winkel · \( = 0 \): rechter Winkel · \( < 0 \): stumpfer Winkel.</p>''')
    + loes(4, r'''    <p>\( \cos\varphi = \tfrac{20}{5 \cdot 5} = 0.8 \Rightarrow \varphi \approx 36.9° \).</p>''')
    + loes(5, r'''    <p>\( \cos\varphi = \tfrac{5}{\sqrt{5}\sqrt{10}} = \tfrac{1}{\sqrt{2}} \Rightarrow 45° \).</p>''')
    + loes(6, r'''    <p>\( 6 + 4k = 0 \Rightarrow k = -1.5 \).</p>''')
    + loes(7, r'''    <p>\( \vec{a}_b = \tfrac{12}{9}\binom{3}{0} = \binom{4}{0} \), Betrag \( 4 \).</p>''')
    + loes(8, r'''    <p>\( W = 50 \cdot 8 \cdot 0.5 = 200 \) J.</p>''')
    + loes(9, r'''    <p>\( \vec{a} \cdot \vec{b} = 0 \Rightarrow \vec{a}_b = \vec{0} \) — kein «Schatten».</p>''')
    + loes(10, r'''    <p>\( \vec{AB} = \binom{4}{1} \), \( \vec{AC} = \binom{1}{3} \):
    \( \cos\alpha = \tfrac{7}{\sqrt{170}} \Rightarrow \alpha \approx 57.5° \).</p>''')
    + loes(11, r'''    <p>\( \vec{BA} \cdot \vec{BC} = \binom{-4}{-2} \cdot \binom{-1}{2} = 4 - 4 = 0 \) —
    rechter Winkel bei \( B \).</p>''')
    + loes(12, r'''    <p>\( \cos\varphi = \tfrac{1}{\sqrt{3}} \Rightarrow \varphi \approx 54.7° \) — für alle
    drei Kanten gleich (Symmetrie).</p>''')
)

N_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Die Musterlösungen
    folgen am Ende des Dokuments. Taschenrechner für Winkel auf DEG stellen.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Physik</td><td>Arbeit am Schlitten</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Konstruktion</td><td>Rechtwinklig-Kontrolle</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Vermessung</td><td>Winkel im Gelände-Dreieck</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Mechanik</td><td>Hangabtriebskraft als Projektion</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Bauwesen</td><td>Winkel im Dachstuhl (3D)</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Solartechnik</td><td>Einstrahlung auf ein Panel</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Arbeit am Schlitten', 2, r'''    <p>Ein Schlitten wird mit \( F = 80 \) N über \( s = 12 \) m gezogen; das Seil bildet
    \( 35° \) mit dem Boden.</p>
    <p>(a) Berechne die Arbeit \( W = |\vec{F}||\vec{s}|\cos\varphi \).</p>
    <p>(b) Wie viel Arbeit ginge bei waagrechtem Seil?</p>
    <p>(c) Warum leistet die Vertikalkomponente der Kraft keine Arbeit?</p>
''' + LINS4, tag='Physik')
    + aufg(2, 'Rechtwinklig-Kontrolle', 2, r'''    <p>Ein Metallwinkel hat die Schenkel \( \vec{a} = \binom{4}{2} \) und
    \( \vec{b} = \binom{-1}{2} \) (in cm).</p>
    <p>(a) Prüfe mit dem Skalarprodukt, ob der Winkel exakt \( 90° \) beträgt.</p>
    <p>(b) Die Fertigung liefert stattdessen \( \vec{b}\,' = \binom{-1}{2.1} \).
    Welcher Winkel entsteht?</p>
''' + LINS4, tag='Konstruktion')
    + aufg(3, 'Winkel im Gelände-Dreieck', 2, r'''    <p>Drei Messpunkte: \( A(1 \mid 1) \), \( B(5 \mid 2) \), \( C(2 \mid 4) \) (in hm).</p>
    <p>(a) Berechne den Winkel bei \( A \).</p>
    <p>(b) Berechne die Winkel bei \( B \) und \( C \) und prüfe die Winkelsumme.</p>
''' + LINS4, tag='Vermessung')
    + aufg(4, 'Hangabtriebskraft als Projektion', 3, r'''    <p>Auf einen Wagen wirkt die Gewichtskraft \( \vec{F}_G = \binom{0}{-800} \) N. Die
    Rampe hat die Richtung \( \vec{u} = \binom{4}{-1} \).</p>
    <p>(a) Berechne den Betrag der Projektion von \( \vec{F}_G \) auf \( \vec{u} \)
    (Hangabtriebskraft).</p>
    <p>(b) Wie ändert sich diese Kraft bei doppelt so steiler Rampe \( \binom{4}{-2} \)?</p>
''' + LINS4, tag='Mechanik')
    + aufg(5, 'Winkel im Dachstuhl (3D)', 3, r'''    <p>Zwei Sparren treffen sich im First: \( \vec{a} = \begin{pmatrix} 4 \\ 0 \\ -3 \end{pmatrix} \)
    und \( \vec{b} = \begin{pmatrix} -4 \\ 0 \\ -3 \end{pmatrix} \) (in m, \(z\) nach oben).</p>
    <p>(a) Berechne den Winkel zwischen den Sparren.</p>
    <p>(b) Wie lang ist jeder Sparren?</p>
''' + LINS4, tag='Bauwesen')
    + aufg(6, 'Einstrahlung auf ein Panel', 3, r'''    <p>Sonnenstrahlen fallen in Richtung \( \vec{s} = \begin{pmatrix} 0 \\ 2 \\ -3 \end{pmatrix} \)
    ein; die Panel-Normale (senkrecht zur Fläche) zeigt nach
    \( \vec{n} = \begin{pmatrix} 0 \\ -1 \\ 2 \end{pmatrix} \).</p>
    <p>(a) Berechne den Winkel zwischen \( -\vec{s} \) (Richtung <em>zur</em> Sonne) und
    \( \vec{n} \).</p>
    <p>(b) Ideal wäre \( 0° \). Wie gut ist die Ausrichtung (Anteil \( \cos\varphi \))?</p>
''' + LINS4, tag='Solartechnik')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( W = 80 \cdot 12 \cdot \cos 35° \approx 786 \) J.</p>
    <p>(b) \( 960 \) J — rund 18 % mehr.</p>
    <p>(c) Sie steht senkrecht zur Bewegung: \( \cos 90° = 0 \).</p>''')
    + loes(2, r'''    <p>(a) \( -4 + 4 = 0 \) — exakt \( 90° \) ✓.</p>
    <p>(b) \( \vec{a} \cdot \vec{b}\,' = -4 + 4.2 = 0.2 \);
    \( \cos\varphi = \tfrac{0.2}{\sqrt{20}\sqrt{5.41}} \approx 0.0192 \Rightarrow
    \varphi \approx 88.9° \) — knapp daneben.</p>''')
    + loes(3, r'''    <p>(a) \( \alpha \approx 57.5° \) (siehe Theorie).</p>
    <p>(b) \( \vec{BA} = \binom{-4}{-1} \), \( \vec{BC} = \binom{-3}{2} \):
    \( \cos\beta = \tfrac{10}{\sqrt{17}\sqrt{13}} \Rightarrow \beta \approx 47.7° \);
    \( \gamma \approx 180° - 57.5° - 47.7° = 74.8° \) — Summe \( 180° \) ✓.</p>''')
    + loes(4, r'''    <p>(a) \( |\vec{F}_{G,u}| = \tfrac{|\vec{F}_G \cdot \vec{u}|}{|\vec{u}|}
    = \tfrac{800}{\sqrt{17}} \approx 194 \) N.</p>
    <p>(b) \( \tfrac{1600}{\sqrt{20}} \approx 358 \) N — fast doppelt.</p>''')
    + loes(5, r'''    <p>(a) \( \vec{a} \cdot \vec{b} = -16 + 9 = -7 \); \( |\vec{a}| = |\vec{b}| = 5 \):
    \( \cos\varphi = -\tfrac{7}{25} \Rightarrow \varphi \approx 106.3° \).</p>
    <p>(b) je \( 5 \) m.</p>''')
    + loes(6, r'''    <p>(a) \( -\vec{s} = \begin{pmatrix} 0 \\ -2 \\ 3 \end{pmatrix} \):
    \( (-\vec{s}) \cdot \vec{n} = 2 + 6 = 8 \); Beträge \( \sqrt{13} \), \( \sqrt{5} \):
    \( \cos\varphi = \tfrac{8}{\sqrt{65}} \approx 0.992 \Rightarrow \varphi \approx 7.1° \).</p>
    <p>(b) Anteil \( \approx 99.2\ \% \) — sehr gut ausgerichtet.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s4-3c  GERADEN
# ═══════════════════════════════════════════════════════════════════

O_HANDOUT = r'''
  <h2>1. Parametergleichung</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Gerade</div>
    <p>\( g:\ \vec{r} = \vec{r}_A + t\,\vec{u} \), \( t \in \mathbb{R} \) — Stützpunkt \(A\),
    Richtungsvektor \( \vec{u} \neq \vec{0} \); gilt in Ebene und Raum. Aus zwei Punkten:
    \( \vec{u} = \vec{AB} \). Stützpunkt und Richtung sind nicht eindeutig.</p>
  </div>
  <p><strong>Punktprobe:</strong> komponentenweise nach \(t\) auflösen — alle Komponenten müssen
  <strong>dasselbe</strong> \(t\) liefern.</p>

  <h2>2. Gegenseitige Lage</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Richtungen kollinear?</th><th>Zusatztest</th><th>Lage</th></tr></thead>
    <tbody>
      <tr><td class="li">ja</td><td class="li">Stützpunkt auf der anderen Geraden</td><td class="li"><strong>identisch</strong></td></tr>
      <tr><td class="li">ja</td><td class="li">Stützpunkt nicht darauf</td><td class="li"><strong>echt parallel</strong></td></tr>
      <tr><td class="li">nein</td><td class="li">Gleichsetzen lösbar</td><td class="li"><strong>schneidend</strong></td></tr>
      <tr><td class="li">nein</td><td class="li">Gleichsetzen unlösbar (nur Raum)</td><td class="li"><strong>windschief</strong></td></tr>
    </tbody>
  </table>
  <p>Beim Gleichsetzen <strong>verschiedene Parameternamen</strong> (\(t\), \(s\)) verwenden!
  Im Raum: Zwei Komponenten bestimmen \(t\), \(s\) — die dritte testet.</p>

  <h2>3. Schnittwinkel</h2>
  \[ \cos\varphi = \frac{|\vec{u} \cdot \vec{v}|}{|\vec{u}|\,|\vec{v}|}, \qquad 0° \leq \varphi \leq 90° \]
  <p>Der Betrag erzwingt den spitzen Winkel. Senkrecht: \( \vec{u} \cdot \vec{v} = 0 \).</p>

  <h2>4. Abstand Punkt–Gerade (Lot)</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Lot-Rezept</div>
    <p>(1) Laufender Punkt \( F = A + t\,\vec{u} \) · (2) Lotbedingung
    \( \vec{PF} \cdot \vec{u} = 0 \) → \(t\) · (3) Abstand \( d = |\vec{PF}| \).</p>
  </div>

  <h2>5. Bewegungen</h2>
  <p>\( \vec{r}(t) = \vec{r}_0 + t\,\vec{v} \) mit \(t\) = Zeit; Tempo \( = |\vec{v}| \).
  <strong>Kollision</strong> braucht gleichen Ort bei <strong>gleichem</strong> \(t\) —
  Bahnschnitt erlaubt \( t \neq s \).</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Stützpunkt plus \(t\)-mal Richtung. Lage: erst Richtungen, dann Punkte. Winkel über
    die Richtungsvektoren, Abstand über das Lot — und windschief gibt es nur im Raum.</p>
  </div>
'''

O_FORMELAUSZUG = r'''
  <h2>1. Parametergleichung</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Gerade</td><td>\( \vec{r} = \vec{r}_A + t\,\vec{u} \)</td></tr>
      <tr><td class="li">aus zwei Punkten</td><td>\( \vec{u} = \vec{AB} = \vec{r}_B - \vec{r}_A \)</td></tr>
      <tr><td class="li">Punktprobe</td><td class="li">alle Komponenten → dasselbe \(t\)</td></tr>
      <tr><td class="li">Ebene: Umrechnung</td><td>\( m = u_2/u_1 \) → \( y = mx + b \) (im Raum unmöglich)</td></tr>
    </tbody>
  </table>

  <h2>2. Lage zweier Geraden</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">identisch / parallel</td><td class="li">Richtungen kollinear; Punktprobe entscheidet</td></tr>
      <tr><td class="li">schneidend</td><td class="li">gleichsetzen (\(t\), \(s\)!) — System lösbar</td></tr>
      <tr><td class="li">windschief (nur Raum)</td><td class="li">nicht kollinear + System unlösbar</td></tr>
    </tbody>
  </table>

  <h2>3. Winkel und Abstand</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Schnittwinkel</td><td>\( \cos\varphi = \dfrac{|\vec{u} \cdot \vec{v}|}{|\vec{u}|\,|\vec{v}|} \) (spitz)</td></tr>
      <tr><td class="li">senkrecht</td><td>\( \vec{u} \cdot \vec{v} = 0 \)</td></tr>
      <tr><td class="li">Abstand Punkt–Gerade</td><td>\( \vec{PF} \cdot \vec{u} = 0 \) → \(t\) → \( d = |\vec{PF}| \)</td></tr>
    </tbody>
  </table>

  <h2>4. Bewegung</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Bahn</td><td>\( \vec{r}(t) = \vec{r}_0 + t\,\vec{v} \), \(t\) = Zeit</td></tr>
      <tr><td class="li">Tempo</td><td>\( |\vec{v}| \)</td></tr>
      <tr><td class="li">Kollision</td><td class="li">gleicher Ort bei gleichem \(t\) (Bahnschnitt: \(t\), \(s\) frei)</td></tr>
    </tbody>
  </table>
'''

O_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Die Parametergleichung braucht einen <span class="lueck"></span>punkt und einen<br>
      <span class="lueck"></span>vektor. Windschiefe Geraden gibt es nur im <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Punkte erzeugen', 1, r'''    <p>\( g:\ \vec{r} = \binom{1}{2} + t\binom{3}{1} \). Berechne die Geradenpunkte für
    \( t = 0, 1, 2 \) und \( t = -1 \).</p>
''' + LINS)
    + aufg(3, 'Gerade durch zwei Punkte', 1, r'''    <p>Stelle die Parametergleichung durch \( A(1 \mid 2) \) und \( B(4 \mid 3) \) auf.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Punktprobe und Lage</div>\n'
    + aufg(4, 'Punktprobe', 2, r'''    <p>Liegt \( P(7 \mid 4) \) auf \(g\) aus Aufgabe 2? Und \( Q(4 \mid 4) \)?</p>
''' + LINS)
    + aufg(5, 'Parallel oder identisch?', 2, r'''    <p>\( g:\ \vec{r} = \binom{0}{1} + t\binom{2}{1} \) und
    \( h:\ \vec{r} = \binom{4}{3} + s\binom{-2}{-1} \). Bestimme die Lage.</p>
''' + LINS)
    + aufg(6, 'Schnittpunkt', 2, r'''    <p>Berechne den Schnittpunkt von \( g:\ \vec{r} = \binom{1}{2} + t\binom{3}{1} \) und
    \( h:\ \vec{r} = \binom{0}{5} + s\binom{1}{-1} \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Winkel und Abstand</div>\n'
    + aufg(7, 'Schnittwinkel', 2, r'''    <p>Berechne den Schnittwinkel der Geraden aus Aufgabe 6.</p>
''' + LINS)
    + aufg(8, 'Senkrecht?', 2, r'''    <p>Stehen die Geraden mit \( \vec{u} = \binom{2}{1} \) und \( \vec{v} = \binom{-1}{2} \)
    senkrecht?</p>
''' + LINS)
    + aufg(9, 'Abstand Punkt–Gerade', 3, r'''    <p>Berechne den Abstand von \( P(4 \mid 0) \) zu
    \( g:\ \vec{r} = \binom{0}{1} + t\binom{2}{1} \).</p>
''' + LINS)
    + '  <div class="gruppe-titel">Raum und Bewegung</div>\n'
    + aufg(10, 'Windschief', 3, r'''    <p>Zeige: Die \(x\)-Achse und
    \( h:\ \vec{r} = \begin{pmatrix} 0 \\ 1 \\ 3 \end{pmatrix} + s\begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix} \)
    sind windschief.</p>
''' + LINS)
    + aufg(11, 'Bewegung', 2, r'''    <p>\( \vec{r}(t) = \begin{pmatrix} 2 \\ 1 \\ 10 \end{pmatrix} + t\begin{pmatrix} 4 \\ 3 \\ 0 \end{pmatrix} \)
    (m, min). Bestimme Position nach 4 min und das Tempo.</p>
''' + LINS)
    + aufg(12, 'Einholen', 3, r'''    <p>Zwei Objekte auf einer Linie: \( x_1(t) = 10t \) und \( x_2(t) = 50 + 5t \).
    Wann und wo trifft das erste das zweite?</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>Stütz</strong>punkt · <strong>Richtungs</strong>vektor · <strong>Raum</strong>.</p>''')
    + loes(2, r'''    <p>\( (1 \mid 2) \), \( (4 \mid 3) \), \( (7 \mid 4) \), \( (-2 \mid 1) \).</p>''')
    + loes(3, r'''    <p>\( \vec{r} = \binom{1}{2} + t\binom{3}{1} \) (Richtung \( \vec{AB} \)).</p>''')
    + loes(4, r'''    <p>\(P\): \( t = 2 \) in beiden Komponenten ✓. \(Q\): \( t = 1 \) vs. \( t = 2 \) —
    nicht auf \(g\).</p>''')
    + loes(5, r'''    <p>Richtungen kollinear (Faktor \(-1\)); Punktprobe \( (4 \mid 3) \): \( t = 2 \) in
    beiden Komponenten — <strong>identisch</strong>.</p>''')
    + loes(6, r'''    <p>\( 1 + 3t = s \), \( 2 + t = 5 - s \Rightarrow t = 0.5 \), \( s = 2.5 \):
    Schnittpunkt \( (2.5 \mid 2.5) \).</p>''')
    + loes(7, r'''    <p>\( \cos\varphi = \tfrac{2}{\sqrt{20}} \Rightarrow \varphi \approx 63.4° \).</p>''')
    + loes(8, r'''    <p>\( -2 + 2 = 0 \) — ja.</p>''')
    + loes(9, r'''    <p>\( 5t - 7 = 0 \Rightarrow t = 1.4 \); \( F(2.8 \mid 2.4) \);
    \( d = \sqrt{7.2} \approx 2.68 \).</p>''')
    + loes(10, r'''    <p>Richtungen nicht kollinear; Gleichsetzen: \( z \)-Komponente verlangt \( 0 = 3 \) —
    Widerspruch: windschief.</p>''')
    + loes(11, r'''    <p>\( (18 \mid 13 \mid 10) \); Tempo \( \sqrt{16+9} = 5 \) m/min.</p>''')
    + loes(12, r'''    <p>\( 10t = 50 + 5t \Rightarrow t = 10 \); Ort \( x = 100 \).</p>''')
)

O_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Die Musterlösungen
    folgen am Ende des Dokuments. Bei Bewegungen: Kollision heisst gleicher Ort bei gleichem \(t\)!</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Aviatik</td><td>Drohnenbahn</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Verkehr</td><td>Überholmanöver</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Vermessung</td><td>Leitungstrasse und Brunnen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">4</td><td>Städtebau</td><td>Zwei Strassenachsen</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Nautik</td><td>Kollisionskurs?</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Bergbau</td><td>Zwei Stollen (windschief)</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Drohnenbahn', 2, r'''    <p>Eine Drohne fliegt auf
    \( \vec{r}(t) = \begin{pmatrix} 2 \\ 1 \\ 10 \end{pmatrix} + t\begin{pmatrix} 4 \\ 3 \\ 0 \end{pmatrix} \)
    (m, min).</p>
    <p>(a) Bestimme Position nach 4 Minuten und das Tempo.</p>
    <p>(b) Passiert die Drohne den Punkt \( (10 \mid 7 \mid 10) \)? Wann?</p>
    <p>(c) Warum bleibt die Flughöhe konstant?</p>
''' + LINS4, tag='Aviatik')
    + aufg(2, 'Überholmanöver', 2, r'''    <p>Auf einer geraden Strasse: Velo A bei Position \( x_A(t) = 10t \), Velo B bei
    \( x_B(t) = 50 + 5t \) (Einheiten und Stunden).</p>
    <p>(a) Wann holt A das Velo B ein, und wo?</p>
    <p>(b) Wie gross ist der Vorsprung von B nach einer halben Stunde?</p>
''' + LINS4, tag='Verkehr')
    + aufg(3, 'Leitungstrasse und Brunnen', 3, r'''    <p>Eine geplante Leitung folgt \( g:\ \vec{r} = \binom{0}{1} + t\binom{2}{1} \)
    (Koordinaten in hm). Ein Brunnen steht bei \( P(4 \mid 0) \).</p>
    <p>(a) Berechne den Lotfusspunkt der kürzesten Verbindung.</p>
    <p>(b) Wie weit liegt der Brunnen von der Trasse entfernt?</p>
''' + LINS4, tag='Vermessung')
    + aufg(4, 'Zwei Strassenachsen', 3, r'''    <p>\( g:\ \vec{r} = \binom{1}{2} + t\binom{3}{1} \) und
    \( h:\ \vec{r} = \binom{0}{5} + s\binom{1}{-1} \) beschreiben zwei Strassenachsen.</p>
    <p>(a) Berechne den Kreuzungspunkt.</p>
    <p>(b) Unter welchem Winkel kreuzen sich die Strassen?</p>
''' + LINS4, tag='Städtebau')
    + aufg(5, 'Kollisionskurs?', 3, r'''    <p>Zwei Boote (Meter, Sekunden, gleiches \(t\)):
    \( \vec{r}_1(t) = t\binom{2}{1} \) und \( \vec{r}_2(t) = \binom{6}{-2} + t\binom{-1}{2} \).</p>
    <p>(a) Schneiden sich die Bahnen? Wo?</p>
    <p>(b) Kollidieren die Boote?</p>
''' + LINS4, tag='Nautik')
    + aufg(6, 'Zwei Stollen (windschief)', 3, r'''    <p>Stollen 1 folgt der \(x\)-Achse; Stollen 2 folgt
    \( \vec{r} = \begin{pmatrix} 0 \\ 1 \\ 3 \end{pmatrix} + s\begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix} \)
    (Koordinaten in hm).</p>
    <p>(a) Zeige, dass sich die Stollen nicht kreuzen.</p>
    <p>(b) In welcher Tiefe unter Stollen 2 verläuft Stollen 1 (z-Differenz)?</p>
''' + LINS4, tag='Bergbau')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( (18 \mid 13 \mid 10) \); Tempo \( 5 \) m/min.</p>
    <p>(b) \( 2 + 4t = 10 \Rightarrow t = 2 \); Kontrolle: \( 1 + 3 \cdot 2 = 7 \) ✓,
    \( z = 10 \) ✓ — ja, nach 2 Minuten.</p>
    <p>(c) Die \(z\)-Komponente des Geschwindigkeitsvektors ist null.</p>''')
    + loes(2, r'''    <p>(a) \( 10t = 50 + 5t \Rightarrow t = 10 \) h, Position \(100\).</p>
    <p>(b) \( x_B(0.5) - x_A(0.5) = 52.5 - 5 = 47.5 \) Einheiten.</p>''')
    + loes(3, r'''    <p>(a) \( 5t - 7 = 0 \Rightarrow t = 1.4 \): \( F(2.8 \mid 2.4) \).</p>
    <p>(b) \( d = \sqrt{1.2^2 + 2.4^2} = \sqrt{7.2} \approx 2.68 \) hm.</p>''')
    + loes(4, r'''    <p>(a) \( t = 0.5 \), \( s = 2.5 \): Kreuzung \( (2.5 \mid 2.5) \).</p>
    <p>(b) \( \cos\varphi = \tfrac{2}{\sqrt{20}} \Rightarrow \varphi \approx 63.4° \).</p>''')
    + loes(5, r'''    <p>(a) Mit Parametern \(t\), \(s\): \( s = 2 \), \( t = 2 \) — Schnitt in \( (4 \mid 2) \).</p>
    <p>(b) Da sogar \( t = s = 2 \): gleicher Ort zur gleichen Zeit — <strong>Kollision</strong>
    nach 2 s.</p>''')
    + loes(6, r'''    <p>(a) Richtungen nicht kollinear; \(z\): \( 0 = 3 \) — Widerspruch: windschief.</p>
    <p>(b) Stollen 1 liegt bei \( z = 0 \), Stollen 2 bei \( z = 3 \) — Differenz \(3\) hm.</p>''')
)

# ═══════════════════════════════════════════════════════════════════
#  s4-3d  EBENEN (ERGÄNZUNG TALS)
# ═══════════════════════════════════════════════════════════════════

P_HANDOUT = r'''
  <h2>1. Parametergleichung der Ebene</h2>
  <div class="block block-def">
    <div class="block-titel">📘 Ebene</div>
    <p>\( E:\ \vec{r} = \vec{r}_A + s\,\vec{u} + t\,\vec{v} \), \( s, t \in \mathbb{R} \) —
    Stützpunkt \(A\), zwei <strong>nicht kollineare</strong> Spannvektoren. Aus drei Punkten
    (echtes Dreieck): \( \vec{u} = \vec{AB} \), \( \vec{v} = \vec{AC} \).</p>
  </div>
  <p><em>Hinweis: Teilgebiet 4.3d ist eine Ergänzung des TALS-Lehrmittels und kein
  RLP-2030-Teilgebiet.</em></p>

  <h2>2. Punktprobe</h2>
  <p>Ansatz \( \vec{r}_P = \vec{r}_A + s\,\vec{u} + t\,\vec{v} \): <strong>drei</strong>
  Gleichungen, <strong>zwei</strong> Unbekannte — zwei bestimmen \(s\), \(t\), die dritte
  <strong>testet</strong>.</p>

  <h2>3. Gerade und Ebene</h2>
  <p>Gleichsetzen gibt ein \( 3 \times 3 \)-System in \(r\) (Geraden-Parameter), \(s\), \(t\):</p>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">genau eine Lösung</td><td class="li"><strong>Durchstosspunkt</strong></td></tr>
      <tr><td class="li">keine Lösung</td><td class="li">Gerade <strong>echt parallel</strong></td></tr>
      <tr><td class="li">unendlich viele</td><td class="li">Gerade <strong>liegt in</strong> der Ebene</td></tr>
    </tbody>
  </table>

  <h2>4. Zwei Ebenen</h2>
  <p><strong>Identisch</strong>, <strong>echt parallel</strong> oder Schnitt in einer
  <strong>Geraden</strong> — nie in nur einem Punkt. Test: Spannvektoren vergleichen, dann
  Punktprobe.</p>

  <h2>5. Flächen modellieren</h2>
  <p>Dächer und Rampen sind Ebenen: Die Grundriss-Koordinaten legen \(s\), \(t\) fest; die
  \(z\)-Gleichung liefert die Höhe. Beispiel Pultdach
  \( \vec{r} = (0, 0, 4) + s\,(6, 0, 0) + t\,(0, 5, 2) \): Höhe \( z = 4 + 2t \) — die Neigung
  steckt im Verhältnis der \(v\)-Komponenten.</p>

  <div class="block block-merksatz">
    <div class="block-titel">⭐ Merksatz</div>
    <p>Ebene = Gerade mit zweitem Parameter. Punktprobe: zwei bestimmen, eine testet.
    Durchstosspunkt: \( 3 \times 3 \)-System — 1/0/∞ Lösungen entscheiden die Lage.
    Zwei Ebenen schneiden sich, wenn überhaupt, in einer Geraden.</p>
  </div>
'''

P_FORMELAUSZUG = r'''
  <h2>1. Parametergleichung</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Ebene</td><td>\( \vec{r} = \vec{r}_A + s\,\vec{u} + t\,\vec{v} \) (\( \vec{u}, \vec{v} \) nicht kollinear)</td></tr>
      <tr><td class="li">aus drei Punkten</td><td>\( \vec{u} = \vec{AB}, \quad \vec{v} = \vec{AC} \)</td></tr>
      <tr><td class="li">Freiheitsgrade</td><td class="li">zwei Parameter — eine Fläche</td></tr>
    </tbody>
  </table>

  <h2>2. Punktprobe</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Ansatz</td><td>\( \vec{r}_P = \vec{r}_A + s\,\vec{u} + t\,\vec{v} \) — 3 Gleichungen, 2 Unbekannte</td></tr>
      <tr><td class="li">Verfahren</td><td class="li">zwei Gleichungen bestimmen \(s\), \(t\) — die dritte testet</td></tr>
    </tbody>
  </table>

  <h2>3. Lagebeziehungen</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Gerade–Ebene</td><td class="li">gleichsetzen (\(r\), \(s\), \(t\)): 1 Lösung = Durchstosspunkt · 0 = parallel · ∞ = enthalten</td></tr>
      <tr><td class="li">Ebene–Ebene</td><td class="li">Schnittgerade · echt parallel · identisch</td></tr>
      <tr><td class="li">Punkt–Ebene</td><td class="li">Punktprobe</td></tr>
    </tbody>
  </table>

  <h2>4. Höhen über dem Grundriss</h2>
  <table class="ftb-tabelle">
    <tbody>
      <tr><td class="li" style="width:35%">Vorgehen</td><td class="li">\(x\)-, \(y\)-Gleichung → \(s\), \(t\) → in \(z\)-Gleichung einsetzen</td></tr>
      <tr><td class="li">Neigung</td><td class="li">Verhältnis der Spannvektor-Komponenten (z.B. \( 2 : 5 \))</td></tr>
    </tbody>
  </table>
'''

P_TDS = (
    A_TDS_INTRO
    + '  <div class="gruppe-titel">Grundlagen &amp; Verständnis</div>\n'
    + aufg(1, 'Begriffe vervollständigen', 1, r'''    <p>Vervollständige die Aussage und schreibe in die Lücken:</p>
    <div class="lueckentext">
      Eine Ebene braucht <span class="lueck"></span> Parameter und zwei nicht<br>
      <span class="lueck"></span> Spannvektoren. Zwei Ebenen schneiden sich —<br>
      wenn überhaupt — in einer <span class="lueck"></span>.
    </div>''')
    + aufg(2, 'Ebenenpunkte erzeugen', 1, r'''    <p>\( E:\ \vec{r} = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} + s\begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix} + t\begin{pmatrix} 0 \\ 1 \\ 3 \end{pmatrix} \).
    Berechne die Punkte für \( (s, t) = (0, 0) \), \( (1, 0) \) und \( (2, 1) \).</p>
''' + LINS)
    + aufg(3, 'Ebene aus drei Punkten', 2, r'''    <p>Stelle die Ebene durch \( A(0 \mid 0 \mid 1) \), \( B(2 \mid 0 \mid 1) \),
    \( C(0 \mid 3 \mid 4) \) auf.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Punktprobe</div>\n'
    + aufg(4, 'Punktprobe positiv', 2, r'''    <p>Liegt \( P(2 \mid 3 \mid 3) \) in \(E\) aus Aufgabe 2?</p>
''' + LINS)
    + aufg(5, 'Punktprobe negativ', 2, r'''    <p>Liegt \( Q(2 \mid 3 \mid 4) \) in \(E\) aus Aufgabe 2?</p>
''' + LINS)
    + aufg(6, 'Koordinatenebenen', 1, r'''    <p>Gib Parametergleichungen der \(x\)-\(y\)-Ebene und der \(x\)-\(z\)-Ebene an.</p>
''' + LINS)
    + '  <div class="gruppe-titel">Gerade und Ebene</div>\n'
    + aufg(7, 'Durchstosspunkt', 3, r'''    <p>\( g:\ \vec{r} = \begin{pmatrix} 0 \\ 5 \\ 3 \end{pmatrix} + r\begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} \).
    Berechne den Durchstosspunkt durch \(E\) aus Aufgabe 2.</p>
''' + LINS)
    + aufg(8, 'Lage deuten', 2, r'''    <p>Das System Gerade–Ebene hat keine Lösung. Was bedeutet das — und was bei unendlich
    vielen Lösungen?</p>
''' + LINS)
    + aufg(9, 'Anzahl Unbekannte', 1, r'''    <p>Wie viele Gleichungen und Unbekannte hat das System beim Schnitt Gerade–Ebene?</p>
''' + LINS)
    + '  <div class="gruppe-titel">Anwendung</div>\n'
    + aufg(10, 'Dachhöhe', 2, r'''    <p>Pultdach \( \vec{r} = \begin{pmatrix} 0 \\ 0 \\ 4 \end{pmatrix} + s\begin{pmatrix} 6 \\ 0 \\ 0 \end{pmatrix} + t\begin{pmatrix} 0 \\ 5 \\ 2 \end{pmatrix} \).
    Wie hoch liegt das Dach über dem Grundriss-Punkt \( (3 \mid 2.5) \)?</p>
''' + LINS)
    + aufg(11, 'Kamin', 3, r'''    <p>Ein senkrechtes Rohr steht über \( (2 \mid 3) \). In welcher Höhe durchstösst es
    das Pultdach?</p>
''' + LINS)
    + aufg(12, 'Parallel oder enthalten?', 3, r'''    <p>\( h:\ \vec{r} = \begin{pmatrix} 0 \\ 0 \\ 9 \end{pmatrix} + r\begin{pmatrix} 6 \\ 0 \\ 0 \end{pmatrix} \)
    und das Pultdach: Bestimme die Lage.</p>
''' + LINS)
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Lösungen</h2>\n\n'
    + loes(1, r'''    <p><strong>zwei</strong> · <strong>kollineare(n)</strong> · <strong>Geraden</strong>.</p>''')
    + loes(2, r'''    <p>\( (1 \mid 0 \mid 0) \), \( (2 \mid 2 \mid 0) \), \( (3 \mid 5 \mid 3) \).</p>''')
    + loes(3, r'''    <p>\( \vec{r} = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix} + s\begin{pmatrix} 2 \\ 0 \\ 0 \end{pmatrix} + t\begin{pmatrix} 0 \\ 3 \\ 3 \end{pmatrix} \).</p>''')
    + loes(4, r'''    <p>\( s = 1 \) (x), \( t = 1 \) (z); Test y: \( 2 + 1 = 3 \) ✓ — ja.</p>''')
    + loes(5, r'''    <p>\( s = 1 \), \( z \): \( 3t = 4 \Rightarrow t = \tfrac{4}{3} \); Test y:
    \( 2 + \tfrac{4}{3} = \tfrac{10}{3} \neq 3 \) — nein.</p>''')
    + loes(6, r'''    <p>\( \vec{r} = s\,\vec{e}_1 + t\,\vec{e}_2 \) bzw. \( \vec{r} = s\,\vec{e}_1 + t\,\vec{e}_3 \).</p>''')
    + loes(7, r'''    <p>\( 3t = 3 \Rightarrow t = 1 \); \( 2s + t = 5 \Rightarrow s = 2 \);
    \( r = 1 + s = 3 \): Durchstosspunkt \( (3 \mid 5 \mid 3) \).</p>''')
    + loes(8, r'''    <p>Keine Lösung: Gerade <strong>echt parallel</strong> zur Ebene. Unendlich viele:
    Gerade <strong>liegt in</strong> der Ebene.</p>''')
    + loes(9, r'''    <p>Drei Gleichungen (je Komponente), drei Unbekannte (\(r\), \(s\), \(t\)).</p>''')
    + loes(10, r'''    <p>\( s = 0.5 \), \( t = 0.5 \): \( z = 4 + 1 = 5 \) m.</p>''')
    + loes(11, r'''    <p>\( s = \tfrac{1}{3} \), \( t = 0.6 \): Höhe \( 4 + 1.2 = 5.2 \) m.</p>''')
    + loes(12, r'''    <p>Richtung von \(h\) ist Spannvektor von \(E\); über \( (0 \mid 0) \) liegt \(E\) auf
    \(4\) m, \(h\) auf \(9\) m — <strong>echt parallel</strong>.</p>''')
)

P_SERIE = (
    r'''  <div class="block block-def" style="margin-bottom:4mm">
    <div class="block-titel">📘 Hinweise</div>
    <p>Sechs Anwendungsaufgaben, nach zunehmendem Schwierigkeitsgrad geordnet. Die Musterlösungen
    folgen am Ende des Dokuments. Alle Aufgaben nutzen das Pultdach
    \( E:\ \vec{r} = (0, 0, 4) + s\,(6, 0, 0) + t\,(0, 5, 2) \), \( 0 \leq s, t \leq 1 \)
    (Koordinaten in m), sofern nichts anderes steht.</p>
  </div>

  <h3 style="margin-top:4mm">Übersicht</h3>
  <table class="uebersicht">
    <thead><tr><th>Nr.</th><th>Bereich</th><th>Titel</th><th style="text-align:center">Schwierigkeit</th></tr></thead>
    <tbody>
      <tr><td class="nr">1</td><td>Architektur</td><td>Dachhöhen und Neigung</td><td class="s">●●○</td></tr>
      <tr><td class="nr">2</td><td>Haustechnik</td><td>Kaminrohr</td><td class="s">●●○</td></tr>
      <tr><td class="nr">3</td><td>Solartechnik</td><td>Panelfläche als Ebene</td><td class="s">●●○</td></tr>
      <tr><td class="nr">4</td><td>Elektroinstallation</td><td>Leitung parallel zum Dach</td><td class="s">●●●</td></tr>
      <tr><td class="nr">5</td><td>Aviatik</td><td>Drohne über dem Dach</td><td class="s">●●●</td></tr>
      <tr><td class="nr">6</td><td>Geometrie</td><td>Rampe durch drei Punkte</td><td class="s">●●●</td></tr>
    </tbody>
  </table>

'''
    + aufg(1, 'Dachhöhen und Neigung', 2, r'''    <p>(a) Berechne die Dachhöhe über den Grundriss-Punkten \( (3 \mid 2.5) \) und
    \( (1 \mid 5) \).</p>
    <p>(b) Welche Neigung hat das Dach (Steigung in \(y\)-Richtung)?</p>
    <p>(c) Warum ist die Höhe unabhängig von \(x\)?</p>
''' + LINS4, tag='Architektur')
    + aufg(2, 'Kaminrohr', 2, r'''    <p>Ein senkrechtes Kaminrohr steht über dem Grundriss-Punkt \( (2 \mid 3) \):
    \( k:\ \vec{r} = (2, 3, 0) + r\,(0, 0, 1) \).</p>
    <p>(a) Stelle das Gleichungssystem für den Durchstosspunkt auf.</p>
    <p>(b) In welcher Höhe tritt das Rohr durch die Dachfläche?</p>
''' + LINS4, tag='Haustechnik')
    + aufg(3, 'Panelfläche als Ebene', 2, r'''    <p>Ein Solarpanel liegt auf dem Dach: Es belegt den Bereich \( 0.2 \leq s \leq 0.8 \),
    \( 0.4 \leq t \leq 0.9 \).</p>
    <p>(a) Berechne die vier Eckpunkte des Panels (nur \(x\), \(y\)).</p>
    <p>(b) Zwischen welchen Höhen liegt das Panel?</p>
''' + LINS4, tag='Solartechnik')
    + aufg(4, 'Leitung parallel zum Dach', 3, r'''    <p>Eine Leitung folgt \( h:\ \vec{r} = (0, 0, 9) + r\,(6, 0, 0) \).</p>
    <p>(a) Zeige, dass die Leitung parallel zur Dachebene verläuft.</p>
    <p>(b) Wie gross ist der Höhenunterschied zur Vorderkante des Dachs?</p>
''' + LINS4, tag='Elektroinstallation')
    + aufg(5, 'Drohne über dem Dach', 3, r'''    <p>Eine Drohne sinkt auf \( g:\ \vec{r} = (0, 0, 7) + r\,(2, 2, -1) \) (m; \(r\) in s).</p>
    <p>(a) Stelle das Gleichungssystem für den Durchstosspunkt durch die Dachebene auf
    und löse es.</p>
    <p>(b) Liegt der Treffpunkt auf dem realen Dach (\( 0 \leq s, t \leq 1 \))?</p>
''' + LINS4, tag='Aviatik')
    + aufg(6, 'Rampe durch drei Punkte', 3, r'''    <p>Eine Rollstuhlrampe geht durch \( A(0 \mid 0 \mid 0) \), \( B(4 \mid 0 \mid 0) \)
    und \( C(0 \mid 6 \mid 0.5) \) (Meter).</p>
    <p>(a) Stelle die Parametergleichung der Rampenebene auf.</p>
    <p>(b) Wie hoch liegt die Rampe nach \(3\) m in \(y\)-Richtung?</p>
    <p>(c) Erfüllt die Rampe die Norm von höchstens \(6\) % Steigung?</p>
''' + LINS4, tag='Geometrie')
    + '\n  <h2 style="border-bottom:2px solid var(--gruen);color:var(--gruen)">Musterlösungen</h2>\n\n'
    + loes(1, r'''    <p>(a) \( 5 \) m bzw. \( 6 \) m.</p>
    <p>(b) \( 2 \) m auf \( 5 \) m — Steigung \( 40\ \% \).</p>
    <p>(c) Der Spannvektor in \(x\)-Richtung hat \(z\)-Komponente null.</p>''')
    + loes(2, r'''    <p>(a) \( 6s = 2 \), \( 5t = 3 \), \( r = 4 + 2t \).</p>
    <p>(b) \( s = \tfrac{1}{3} \), \( t = 0.6 \): Höhe \( 5.2 \) m.</p>''')
    + loes(3, r'''    <p>(a) \( x = 6s \in \{1.2, 4.8\} \), \( y = 5t \in \{2, 4.5\} \) — Ecken
    \( (1.2 \mid 2) \), \( (4.8 \mid 2) \), \( (1.2 \mid 4.5) \), \( (4.8 \mid 4.5) \).</p>
    <p>(b) \( z = 4 + 2t \): zwischen \( 4.8 \) m und \( 5.8 \) m.</p>''')
    + loes(4, r'''    <p>(a) Die Richtung \( (6, 0, 0) \) ist Spannvektor der Dachebene — parallel;
    Stützpunkt \( (0, 0, 9) \) liegt nicht in der Ebene (dort \( z = 4 \)).</p>
    <p>(b) \( 9 - 4 = 5 \) m über der Vorderkante.</p>''')
    + loes(5, r'''    <p>(a) \( 6s = 2r \), \( 5t = 2r \), \( 4 + 2t = 7 - r \Rightarrow r = \tfrac{5}{3} \approx 1.67 \) s.</p>
    <p>(b) \( s = \tfrac{5}{9} \approx 0.56 \), \( t = \tfrac{2}{3} \approx 0.67 \) —
    beide in \([0; 1]\): Treffer auf dem realen Dach.</p>''')
    + loes(6, r'''    <p>(a) \( \vec{r} = s\,(4, 0, 0) + t\,(0, 6, 0.5) \).</p>
    <p>(b) \( t = 0.5 \): \( z = 0.25 \) m.</p>
    <p>(c) Steigung \( \tfrac{0.5}{6} \approx 8.3\ \% > 6\ \% \) — Norm nicht erfüllt,
    die Rampe müsste länger werden.</p>''')
)

# ═══════════════════════════════════════════════════════════════════

QUELLE_FA = ('    <div class="quelle">Ergänzung zur Formelsammlung Promath (SBFI). '
             'Notation gemäss <em>Formeln, Tabellen, Begriffe</em> (FTB).</div>\n')

SEITEN = [
    # (slug, thema, rolle, dateiname, h1, extra_style, scale, quelle, body)
    ('s3-2a-potenzfunktionen', 'Potenzfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', A_HANDOUT),
    ('s3-2a-potenzfunktionen', 'Potenzfunktionen', 'Formelauszug', 'formelauszug.html',
     'Potenzfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, A_FORMELAUSZUG),
    ('s3-2a-potenzfunktionen', 'Potenzfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', A_TDS),
    ('s3-2a-potenzfunktionen', 'Potenzfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Potenzfunktionen', STYLE_SERIE, '1.0', '', A_SERIE),
    ('s3-2b-wurzelfunktionen', 'Wurzelfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', B_HANDOUT),
    ('s3-2b-wurzelfunktionen', 'Wurzelfunktionen', 'Formelauszug', 'formelauszug.html',
     'Wurzelfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, B_FORMELAUSZUG),
    ('s3-2b-wurzelfunktionen', 'Wurzelfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', B_TDS),
    ('s3-2b-wurzelfunktionen', 'Wurzelfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Wurzelfunktionen', STYLE_SERIE, '1.0', '', B_SERIE),
    ('s3-3-polynomfunktionen', 'Polynomfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', C_HANDOUT),
    ('s3-3-polynomfunktionen', 'Polynomfunktionen', 'Formelauszug', 'formelauszug.html',
     'Polynomfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, C_FORMELAUSZUG),
    ('s3-3-polynomfunktionen', 'Polynomfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', C_TDS),
    ('s3-3-polynomfunktionen', 'Polynomfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Polynomfunktionen', STYLE_SERIE, '1.0', '', C_SERIE),
    ('s3-4a-exponentialfunktionen', 'Exponentialfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', D_HANDOUT),
    ('s3-4a-exponentialfunktionen', 'Exponentialfunktionen', 'Formelauszug', 'formelauszug.html',
     'Exponentialfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, D_FORMELAUSZUG),
    ('s3-4a-exponentialfunktionen', 'Exponentialfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', D_TDS),
    ('s3-4a-exponentialfunktionen', 'Exponentialfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Exponentialfunktionen', STYLE_SERIE, '1.0', '', D_SERIE),
    ('s3-4b-logarithmusfunktionen', 'Logarithmusfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', E_HANDOUT),
    ('s3-4b-logarithmusfunktionen', 'Logarithmusfunktionen', 'Formelauszug', 'formelauszug.html',
     'Logarithmusfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, E_FORMELAUSZUG),
    ('s3-4b-logarithmusfunktionen', 'Logarithmusfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', E_TDS),
    ('s3-4b-logarithmusfunktionen', 'Logarithmusfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Logarithmusfunktionen', STYLE_SERIE, '1.0', '', E_SERIE),
    ('s3-5-trigonometrische-funktionen', 'Trigonometrische Funktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', F_HANDOUT),
    ('s3-5-trigonometrische-funktionen', 'Trigonometrische Funktionen', 'Formelauszug', 'formelauszug.html',
     'Trigonometrische Funktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, F_FORMELAUSZUG),
    ('s3-5-trigonometrische-funktionen', 'Trigonometrische Funktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', F_TDS),
    ('s3-5-trigonometrische-funktionen', 'Trigonometrische Funktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Trigonometrische Funktionen', STYLE_SERIE, '1.0', '', F_SERIE),
    ('s3-1-grundlagen', 'Grundlagen Funktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', G_HANDOUT),
    ('s3-1-grundlagen', 'Grundlagen Funktionen', 'Formelauszug', 'formelauszug.html',
     'Grundlagen Funktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, G_FORMELAUSZUG),
    ('s3-1-grundlagen', 'Grundlagen Funktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', G_TDS),
    ('s3-1-grundlagen', 'Grundlagen Funktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Grundlagen Funktionen', STYLE_SERIE, '1.0', '', G_SERIE),
    ('s2-2a-potenz-wurzel-rationale-gleichungen', 'Potenz-, Wurzel- und rationale Gleichungen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', H_HANDOUT),
    ('s2-2a-potenz-wurzel-rationale-gleichungen', 'Potenz-, Wurzel- und rationale Gleichungen', 'Formelauszug', 'formelauszug.html',
     'Potenz-, Wurzel- und rationale Gleichungen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, H_FORMELAUSZUG),
    ('s2-2a-potenz-wurzel-rationale-gleichungen', 'Potenz-, Wurzel- und rationale Gleichungen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', H_TDS),
    ('s2-2a-potenz-wurzel-rationale-gleichungen', 'Potenz-, Wurzel- und rationale Gleichungen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Potenz-, Wurzel- und rationale Gleichungen', STYLE_SERIE, '1.0', '', H_SERIE),
    ('s2-2b-exponential-logarithmische-gleichungen', 'Exponential- und logarithmische Gleichungen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', I_HANDOUT),
    ('s2-2b-exponential-logarithmische-gleichungen', 'Exponential- und logarithmische Gleichungen', 'Formelauszug', 'formelauszug.html',
     'Exponential- und logarithmische Gleichungen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, I_FORMELAUSZUG),
    ('s2-2b-exponential-logarithmische-gleichungen', 'Exponential- und logarithmische Gleichungen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', I_TDS),
    ('s2-2b-exponential-logarithmische-gleichungen', 'Exponential- und logarithmische Gleichungen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Exponential- und logarithmische Gleichungen', STYLE_SERIE, '1.0', '', I_SERIE),
    ('s2-2c-betrag-polynom-ungleichungen', 'Betrags- und Polynomgleichungen, Ungleichungen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', J_HANDOUT),
    ('s2-2c-betrag-polynom-ungleichungen', 'Betrags- und Polynomgleichungen, Ungleichungen', 'Formelauszug', 'formelauszug.html',
     'Betrag, Nullprodukt, Ungleichungen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, J_FORMELAUSZUG),
    ('s2-2c-betrag-polynom-ungleichungen', 'Betrags- und Polynomgleichungen, Ungleichungen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', J_TDS),
    ('s2-2c-betrag-polynom-ungleichungen', 'Betrags- und Polynomgleichungen, Ungleichungen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Betrag, Nullprodukt, Ungleichungen', STYLE_SERIE, '1.0', '', J_SERIE),
    ('s2-1-grundlagen', 'Grundlagen Gleichungen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', K_HANDOUT),
    ('s2-1-grundlagen', 'Grundlagen Gleichungen', 'Formelauszug', 'formelauszug.html',
     'Grundlagen Gleichungen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, K_FORMELAUSZUG),
    ('s2-1-grundlagen', 'Grundlagen Gleichungen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', K_TDS),
    ('s2-1-grundlagen', 'Grundlagen Gleichungen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Grundlagen Gleichungen', STYLE_SERIE, '1.0', '', K_SERIE),
    ('s3-6-betragsfunktionen', 'Betragsfunktionen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', L_HANDOUT),
    ('s3-6-betragsfunktionen', 'Betragsfunktionen', 'Formelauszug', 'formelauszug.html',
     'Betragsfunktionen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, L_FORMELAUSZUG),
    ('s3-6-betragsfunktionen', 'Betragsfunktionen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', L_TDS),
    ('s3-6-betragsfunktionen', 'Betragsfunktionen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Betragsfunktionen', STYLE_SERIE, '1.0', '', L_SERIE),
    ('s4-3a-vektorbegriff-komponenten', 'Vektorbegriff und Komponenten', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', M_HANDOUT),
    ('s4-3a-vektorbegriff-komponenten', 'Vektorbegriff und Komponenten', 'Formelauszug', 'formelauszug.html',
     'Vektorbegriff und Komponenten — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, M_FORMELAUSZUG),
    ('s4-3a-vektorbegriff-komponenten', 'Vektorbegriff und Komponenten', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', M_TDS),
    ('s4-3a-vektorbegriff-komponenten', 'Vektorbegriff und Komponenten', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Vektorbegriff und Komponenten', STYLE_SERIE, '1.0', '', M_SERIE),
    ('s4-3b-skalarprodukt', 'Skalarprodukt', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', N_HANDOUT),
    ('s4-3b-skalarprodukt', 'Skalarprodukt', 'Formelauszug', 'formelauszug.html',
     'Skalarprodukt — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, N_FORMELAUSZUG),
    ('s4-3b-skalarprodukt', 'Skalarprodukt', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', N_TDS),
    ('s4-3b-skalarprodukt', 'Skalarprodukt', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Skalarprodukt', STYLE_SERIE, '1.0', '', N_SERIE),
    ('s4-3c-geraden', 'Geraden', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', O_HANDOUT),
    ('s4-3c-geraden', 'Geraden', 'Formelauszug', 'formelauszug.html',
     'Geraden — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, O_FORMELAUSZUG),
    ('s4-3c-geraden', 'Geraden', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', O_TDS),
    ('s4-3c-geraden', 'Geraden', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Geraden', STYLE_SERIE, '1.0', '', O_SERIE),
    ('s4-3d-ebenen', 'Ebenen', 'Handout', 'handout.html',
     'Handout — Theorie', '', '1.0', '', P_HANDOUT),
    ('s4-3d-ebenen', 'Ebenen', 'Formelauszug', 'formelauszug.html',
     'Ebenen — Formelauszug', STYLE_FORMELAUSZUG, '0.95', QUELLE_FA, P_FORMELAUSZUG),
    ('s4-3d-ebenen', 'Ebenen', 'Teste dich selbst', 'teste-dich-selbst.html',
     'Teste dich selbst', STYLE_TDS, '1.0', '', P_TDS),
    ('s4-3d-ebenen', 'Ebenen', 'Aufgabenserie', 'aufgabenserie.html',
     'Anwendungsaufgaben — Ebenen', STYLE_SERIE, '1.0', '', P_SERIE),
]


def main():
    for slug, thema, rolle, fname, h1, style, scale, quelle, body in SEITEN:
        out_dir = os.path.join(ROOT, 'downloads', 'schwerpunkt', slug)
        os.makedirs(out_dir, exist_ok=True)
        html = (HEAD.format(rolle=rolle, thema=thema, slug=slug, h1=h1,
                            extra_style=style, scale=scale, quelle=quelle)
                + body
                + FOOT.format(thema=thema, rolle=rolle))
        path = os.path.join(out_dir, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {os.path.relpath(path, ROOT)}  ({html.count(chr(10))} Zeilen)')
    # Selbsttest: kein ß, kein Dezimalkomma-Muster in Zahlen, Tag-Balance grob
    fails = 0
    for slug, _, _, fname, *_ in SEITEN:
        p = os.path.join(ROOT, 'downloads', 'schwerpunkt', slug, fname)
        t = open(p, encoding='utf-8').read()
        if 'ß' in t:
            print(f'  ✗ ß gefunden in {p}'); fails += 1
        if t.count('<div') != t.count('</div>'):
            print(f'  ✗ div-Bilanz in {p}: {t.count("<div")} vs {t.count("</div>")}'); fails += 1
    print('Selbsttest:', 'FEHLER' if fails else 'ok')


if __name__ == '__main__':
    main()
