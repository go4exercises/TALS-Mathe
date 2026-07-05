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
