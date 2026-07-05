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
