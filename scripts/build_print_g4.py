#!/usr/bin/env python3
"""
Generator für die HTML-Druckseiten der g4-Themen (Datenanalyse).
Erzeugt 12 Dateien: g4-1, g4-2, g4-3 × {handout, formelauszug, teste-dich-selbst, aufgabenserie}.

Pattern-Vorlage: downloads/grundlagen/g5-1-grundlagen/*.html (schlanker Stil).
"""
import os

# ─── Header-Skelett (gleich für alle 4 Druckseiten-Typen) ─────────
HEAD_FULL = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{druck_titel} · {thema_titel} — Mathe begreifbar</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../print.css">
{extra_style}<script>
MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'global', scale: {mj_scale} }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea'] }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>

<div class="druck-bar no-print">
  <a class="db-back" href="../../../grundlagen/{themenseite}#downloads">← zurück zur Themenseite</a>
  <span class="db-info">{druck_titel} · A4 · Bereit zum Drucken</span>
  <button class="db-print" onclick="window.print()">Seite drucken</button>
</div>

<div class="druck-wrapper">

  <header class="doc-kopf">
    <div class="dk-bereich">Mathe begreifbar · Grundlagenfach · {nr} {thema_titel}</div>
    <h1>{druck_titel_h1}</h1>{subtitle}
  </header>

{body}

</div>

</body>
</html>
'''

FORMELAUSZUG_EXTRA_STYLE = '''<style>
  body { font-size: 10pt; }
  .druck-wrapper h2 { font-size: 12pt; margin-top: 4mm; }
  .druck-wrapper p { margin: 0 0 1.5mm; font-size: 9.5pt; }
  .druck-wrapper table.ftb-tabelle { font-size: 9.2pt; margin: 2mm 0; }
  .druck-wrapper table.ftb-tabelle th,
  .druck-wrapper table.ftb-tabelle td { padding: 1.2mm 2mm; }
</style>
'''


def render(druck_titel, druck_titel_h1, themenseite, nr, thema_titel,
           body, subtitle='', extra_style='', mj_scale=1.0):
    sub = ('\n    <p style="margin-top:2mm;font-size:9.5pt;color:var(--tinte-2)">' +
           subtitle + '</p>') if subtitle else ''
    return HEAD_FULL.format(
        druck_titel=druck_titel, druck_titel_h1=druck_titel_h1,
        themenseite=themenseite, nr=nr, thema_titel=thema_titel,
        body=body, subtitle=sub, extra_style=extra_style, mj_scale=mj_scale
    )


# ════════════════════════════════════════════════════════════════════
# G4-1 — Grundlagen Datenanalyse
# ════════════════════════════════════════════════════════════════════
G4_1 = dict(themenseite='g4-1-grundlagen.html', nr='4.1', thema_titel='Grundlagen Datenanalyse')

G4_1_HANDOUT = '''  <h2>1. Grundbegriffe</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definition</div>
    <p>Die <strong>Grundgesamtheit</strong> ist die Menge <em>aller</em> Objekte, über die eine Aussage getroffen werden soll. Eine <strong>Stichprobe</strong> ist eine Teilmenge der Grundgesamtheit, die tatsächlich untersucht wird. Der <strong>Stichprobenumfang</strong> \\(n\\) ist die Anzahl ihrer Elemente.</p>
  </div>

  <h3>Urliste, sortierte Liste, Rang</h3>
  <p>Die <strong>Urliste</strong> enthält alle erhobenen Werte in der Reihenfolge der Erhebung. Wird sie aufsteigend sortiert, entsteht die <strong>sortierte Liste</strong>. Der <strong>Rang</strong> eines Wertes ist seine Position in der sortierten Liste.</p>

  <table class="ftb-tabelle">
    <thead><tr><th>Begriff</th><th>Bedeutung</th></tr></thead>
    <tbody>
      <tr><td class="li">Grundgesamtheit</td><td>alle Objekte, über die eine Aussage gemacht werden soll</td></tr>
      <tr><td class="li">Stichprobe</td><td>tatsächlich untersuchte Teilmenge</td></tr>
      <tr><td class="li">Stichprobenumfang \\(n\\)</td><td>Anzahl Elemente der Stichprobe</td></tr>
      <tr><td class="li">Urliste</td><td>Werte in Erhebungsreihenfolge</td></tr>
      <tr><td class="li">Sortierte Liste</td><td>aufsteigend sortierte Urliste</td></tr>
      <tr><td class="li">Rang</td><td>Position in der sortierten Liste</td></tr>
    </tbody>
  </table>


  <h2>2. Merkmalstypen</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definition</div>
    <p>Jedes erhobene Merkmal ist von einem dieser drei Typen — die Wahl des Diagramms hängt davon ab.</p>
  </div>

  <table class="ftb-tabelle">
    <thead><tr><th>Typ</th><th>Bedeutung</th><th>Beispiele</th></tr></thead>
    <tbody>
      <tr><td class="li"><strong>kategorial</strong></td><td>Werte sind Namen / Kategorien, keine Reihenfolge</td><td class="li">Lieblingsfach, Augenfarbe, Wohnort</td></tr>
      <tr><td class="li"><strong>diskret</strong></td><td>Zahlen, nur abzählbar viele Werte möglich</td><td class="li">Kinderzahl, Würfelaugen, Anzahl Fehler</td></tr>
      <tr><td class="li"><strong>stetig</strong></td><td>Zahlen, beliebig fein abstufbar</td><td class="li">Körpergrösse, Wartezeit, Temperatur</td></tr>
    </tbody>
  </table>

  <div class="block block-tipp">
    <div class="block-titel">💡 Faustregel</div>
    <p>Bei diskreten Daten passt das <em>Balkendiagramm</em>, bei stetigen das <em>Histogramm</em>, bei kategorialen das <em>Kuchen- oder Balkendiagramm</em> ohne Achsen-Reihenfolge.</p>
  </div>


  <h2>3. Tabellenkalkulation als Werkzeug</h2>

  <p>Bei mehr als ca. 20 Werten ist Handrechnung ineffizient. Standard-Werkzeuge: <strong>Microsoft Excel</strong>, <strong>LibreOffice Calc</strong>, <strong>Google Sheets</strong>. Die Funktionsnamen unterscheiden sich (deutsch / englisch), die Logik ist identisch.</p>

  <table class="ftb-tabelle">
    <thead><tr><th>Aufgabe</th><th>Excel/Calc (deutsch)</th><th>Google Sheets / Excel (englisch)</th></tr></thead>
    <tbody>
      <tr><td class="li">Anzahl Werte</td><td>=ANZAHL(A1:A100)</td><td>=COUNT(A1:A100)</td></tr>
      <tr><td class="li">Sortieren (Hilfsspalte)</td><td>=KKLEINSTE(A:A;ZEILE())</td><td>=SMALL(A:A;ROW())</td></tr>
      <tr><td class="li">Häufigkeiten</td><td>=ZÄHLENWENN(A:A;"Wert")</td><td>=COUNTIF(A:A;"Wert")</td></tr>
      <tr><td class="li">Maximum / Minimum</td><td>=MAX(A:A) / =MIN(A:A)</td><td>=MAX(A:A) / =MIN(A:A)</td></tr>
    </tbody>
  </table>


  <h2>4. Datengewinnung und Datenqualität</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Drei Qualitätsmerkmale</div>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Repräsentativität</strong> — bildet die Stichprobe die Grundgesamtheit treu ab? (Beispiel: Online-Umfrage erreicht keine Senioren ohne Internet.)</li>
      <li><strong>Objektivität</strong> — würde eine andere Person dieselben Werte messen?</li>
      <li><strong>Genauigkeit</strong> — passt die Messpräzision zum Zweck? (Körpergrösse auf cm, nicht auf 0.001 mm.)</li>
    </ul>
  </div>

  <div class="block block-fehler">
    <div class="block-titel">⚠ Häufige Fehlerquellen</div>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Selbstselektions-Bias</strong> — wer freiwillig antwortet, ist nicht zufällig.</li>
      <li><strong>Suggestive Frageformulierung</strong> — „Bist du auch gegen Tierquälerei?" liefert kein neutrales Bild.</li>
      <li><strong>Zu kleine Stichproben</strong> — \\(n = 5\\) liefert für eine Schule mit 800 Lernenden keine belastbare Aussage.</li>
      <li><strong>Falsche Erhebungszeit</strong> — Wartezeit am Bankschalter um 11:00 ≠ Wartezeit um 16:30.</li>
    </ul>
  </div>
'''

G4_1_FORMELAUSZUG = '''  <h2>Grundbegriffe</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Begriff</th><th>Bedeutung</th></tr></thead>
    <tbody>
      <tr><td class="li">Grundgesamtheit</td><td>alle Objekte, über die eine Aussage gemacht werden soll</td></tr>
      <tr><td class="li">Stichprobe</td><td>tatsächlich untersuchte Teilmenge der Grundgesamtheit</td></tr>
      <tr><td class="li">Stichprobenumfang \\(n\\)</td><td>Anzahl Elemente der Stichprobe</td></tr>
      <tr><td class="li">Urliste</td><td>Werte in Erhebungsreihenfolge</td></tr>
      <tr><td class="li">Sortierte Liste</td><td>aufsteigend sortierte Urliste</td></tr>
      <tr><td class="li">Rang</td><td>Position eines Wertes in der sortierten Liste</td></tr>
    </tbody>
  </table>

  <h2>Merkmalstypen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Typ</th><th>Beschreibung</th><th>Beispiele</th></tr></thead>
    <tbody>
      <tr><td class="li">kategorial</td><td>Namen / Kategorien, keine Reihenfolge</td><td class="li">Lieblingsfach, Augenfarbe</td></tr>
      <tr><td class="li">diskret</td><td>Zahlen, abzählbar viele Werte</td><td class="li">Kinderzahl, Würfelaugen</td></tr>
      <tr><td class="li">stetig</td><td>Zahlen, beliebig fein abstufbar</td><td class="li">Körpergrösse, Wartezeit</td></tr>
    </tbody>
  </table>

  <h2>Tabellenkalkulation — Funktionsnamen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Aufgabe</th><th>deutsch</th><th>englisch</th></tr></thead>
    <tbody>
      <tr><td class="li">Anzahl</td><td>=ANZAHL(A1:A100)</td><td>=COUNT(A1:A100)</td></tr>
      <tr><td class="li">Häufigkeit</td><td>=ZÄHLENWENN(A:A;"x")</td><td>=COUNTIF(A:A;"x")</td></tr>
      <tr><td class="li">Maximum</td><td>=MAX(A:A)</td><td>=MAX(A:A)</td></tr>
      <tr><td class="li">Minimum</td><td>=MIN(A:A)</td><td>=MIN(A:A)</td></tr>
      <tr><td class="li">k-kleinster Wert</td><td>=KKLEINSTE(A:A;k)</td><td>=SMALL(A:A;k)</td></tr>
    </tbody>
  </table>

  <h2>Drei Qualitätsmerkmale einer Datenerhebung</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Merkmal</th><th>Frage</th></tr></thead>
    <tbody>
      <tr><td class="li">Repräsentativität</td><td>Bildet die Stichprobe die Grundgesamtheit treu ab?</td></tr>
      <tr><td class="li">Objektivität</td><td>Würde eine andere Person dieselben Werte messen?</td></tr>
      <tr><td class="li">Genauigkeit</td><td>Passt die Messpräzision zum Zweck?</td></tr>
    </tbody>
  </table>

  <p style="font-size:8.5pt;color:var(--tinte-2);font-style:italic;margin-top:5mm">Quelle: Anlehnung an „Formeln, Tabellen, Begriffe", Orell Füssli Lehrmittel.</p>
'''

G4_1_TESTE = '''  <h2>Aufgaben</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li>Erkläre den Unterschied zwischen <em>Grundgesamtheit</em> und <em>Stichprobe</em> in eigenen Worten.</li>
    <li>Eine Lehrperson erhebt die Schuhgrössen aller 22 Lernenden ihrer Klasse. Welcher Stichprobenumfang? Was ist die Grundgesamtheit, wenn eine Aussage über die ganze Schule (n = 800) gemacht werden soll?</li>
    <li>Wandle die Urliste 14, 9, 12, 14, 17, 9, 11 in eine sortierte Liste um. Welchen Rang hat der Wert <em>14</em>? (Es gibt zwei Vorkommen — nenne beide Ränge.)</li>
    <li>Klassiere als kategorial / diskret / stetig: a) Anzahl Geschwister, b) Lieblingssportart, c) Schuhgrösse, d) Körpergrösse in cm, e) Postleitzahl.</li>
    <li>Welcher Diagrammtyp passt zu Lieblingssportart in einer Klasse? Begründe.</li>
    <li>Welcher Diagrammtyp passt zu Körpergrösse in einer Klasse? Begründe.</li>
    <li>Schreibe die Excel-/Calc-Formel, die in Spalte A die Anzahl Vorkommen des Wertes „blau" zählt.</li>
    <li>Schreibe die Formel für den drittkleinsten Wert in A1 bis A50.</li>
    <li>Eine Online-Umfrage zur Lebenszufriedenheit von Senioren wird per Mail-Newsletter verschickt. Welches Qualitätsproblem entsteht?</li>
    <li>Beim Erheben der Wartezeit am Bahnschalter werden alle Kunden zwischen 11:00 und 12:00 erfasst. Welches Problem hat das?</li>
    <li>Eine Lehrperson misst die Körpergrösse der Klasse mit einem 1-cm-Massstab. Eine andere mit Lasermessung auf 0.1 mm. Welches Qualitätsmerkmal wird hier verglichen?</li>
    <li>Die Frage „Bist du auch dafür, dass die Pause länger sein sollte?" — was ist daran problematisch?</li>
    <li>Eine Stichprobe von n = 4 soll für eine Schule mit 800 Lernenden eine Aussage liefern. Beurteile.</li>
    <li>Postleitzahl: ist das Merkmal kategorial oder diskret? Begründe.</li>
    <li>Plausibilität: in einer Stichprobe vom Umfang n = 100 hat ein Wert den Rang 0. Kann das stimmen?</li>
  </ol>

  <h2 style="margin-top:6mm">Lösungen</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li>Grundgesamtheit = <em>alle</em> Objekte (z.B. alle Lernenden einer Schule). Stichprobe = die <em>tatsächlich untersuchte</em> Teilmenge (z.B. eine Klasse von 22).</li>
    <li>Stichprobenumfang n = 22. Grundgesamtheit = 800 Lernende der Schule. Die Stichprobe ist eine Klasse — möglicherweise nicht repräsentativ für die ganze Schule.</li>
    <li>Sortiert: 9, 9, 11, 12, 14, 14, 17. Die beiden 14er haben Rang 5 und Rang 6.</li>
    <li>a) diskret  b) kategorial  c) diskret (Schuhgrössen sind in halben Schritten abzählbar)  d) stetig  e) kategorial (PLZ ist ein Code, kein Zahlenwert für Rechnungen)</li>
    <li>Kuchen- oder Balkendiagramm — kategoriale Daten ohne natürliche Reihenfolge.</li>
    <li>Histogramm — stetige Daten in Klassen einteilen und als zusammenhängende Säulen darstellen.</li>
    <li><code>=ZÄHLENWENN(A:A;"blau")</code> bzw. englisch <code>=COUNTIF(A:A;"blau")</code>.</li>
    <li><code>=KKLEINSTE(A1:A50;3)</code> bzw. englisch <code>=SMALL(A1:A50;3)</code>.</li>
    <li><strong>Repräsentativität</strong> — Senioren ohne Internet werden nicht erreicht; die Stichprobe bildet die Grundgesamtheit nicht treu ab (Selbstselektions-Bias).</li>
    <li>Falsche <strong>Erhebungszeit</strong>. Die Wartezeit zur Mittagsspitze ist nicht repräsentativ für den ganzen Tag.</li>
    <li><strong>Genauigkeit</strong> (bzw. Messpräzision). Für Körpergrössen genügt 1 cm; 0.1 mm ist unverhältnismässig genau.</li>
    <li>Suggestive Frageformulierung — das Wort „auch" und die positive Folge („länger") drängen zur Zustimmung. Neutral wäre: „Wie sollte die Pause angelegt sein?"</li>
    <li>Zu kleine Stichprobe — n = 4 von 800 ist 0.5 % der Grundgesamtheit, viel zu wenig für belastbare Aussagen.</li>
    <li>Kategorial. Die Zahl 8000 (Zürich) ist nicht „grösser" oder „besser" als 1200 (Genf) — sie steht für ein Gebiet, nicht für eine Anzahl.</li>
    <li>Nein. Ränge in der sortierten Liste beginnen bei 1 und gehen bis n. Rang 0 ist nicht definiert.</li>
  </ol>
'''

G4_1_AUFGABEN = '''  <h2>Aufgaben</h2>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 1 — Klassenumfrage planen</div>
    <p>Du sollst die Lieblings-Streamingplattform deiner Klasse erheben.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Was ist die Grundgesamtheit, was die Stichprobe?</li>
      <li>Welcher Merkmalstyp liegt vor?</li>
      <li>Welches Diagramm würdest du wählen?</li>
      <li>Welche zwei Qualitätsprobleme könnten auftreten?</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 2 — Wartezeiten in der Praxis</div>
    <p>Eine Hausärztin will die Wartezeit ihrer Patientinnen verbessern. Sie misst über einen Monat alle Wartezeiten zwischen Termin-Beginn und Aufruf — insgesamt 312 Werte.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Was ist Stichprobe, was Grundgesamtheit?</li>
      <li>Welcher Merkmalstyp?</li>
      <li>Welche zwei Excel-Formeln sind sofort nützlich?</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 3 — Sortieren mit Excel</div>
    <p>In Spalte A (A2 bis A21) stehen 20 Prüfungspunkte. Schreibe Formeln in Spalte B, sodass B2 den kleinsten, B3 den zweitkleinsten Wert usw. liefert. (Tipp: Funktion KKLEINSTE und ZEILE.)</p>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 4 — Bias erkennen</div>
    <p>Eine Tageszeitung schreibt: „76 % unserer Online-Leserinnen finden den neuen Tarif gut!" Diskutiere zwei Gründe, warum dieser Befund nicht repräsentativ für die ganze Bevölkerung ist.</p>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 5 — Frageformulierung</div>
    <p>Formuliere für die folgende Erhebungsabsicht zwei Versionen einer Frage: eine <em>suggestive</em> und eine <em>neutrale</em>. Absicht: Erhebung der Meinung zur Verlängerung der Schulpausen um 5 Minuten.</p>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 6 — Stichprobenumfang abschätzen</div>
    <p>Eine Studie soll Aussagen über die durchschnittliche tägliche Bildschirmzeit von Schweizer Jugendlichen (Grundgesamtheit ca. 800 000) machen. Welcher Stichprobenumfang ist plausibel: 50, 500, 5 000 oder 50 000? Begründe — auch ohne exakte Statistik-Theorie kannst du eine sinnvolle Grössenordnung nennen.</p>
  </div>


  <h2 style="margin-top:6mm">Lösungen</h2>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 1 — Klassenumfrage planen</div>
    <ol type="a">
      <li>Grundgesamtheit = alle Lernenden deiner Klasse. Stichprobe = die anwesenden, die antworten — meist eine echte Teilmenge der Klasse.</li>
      <li><strong>Kategorial</strong> (Plattform-Namen, keine natürliche Reihenfolge).</li>
      <li><strong>Kuchendiagramm</strong> oder <strong>Balkendiagramm</strong>. Kuchen funktioniert gut, wenn es 3–6 Kategorien sind.</li>
      <li>Mögliche Probleme: (1) Mehrfachnutzung — viele haben zwei Plattformen, dann muss die Frage genau formuliert werden („Hauptplattform"). (2) Selbstselektions-Bias, wenn nicht alle antworten.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 2 — Wartezeiten</div>
    <ol type="a">
      <li>Stichprobe: die 312 Wartezeiten dieses Monats. Grundgesamtheit: alle Wartezeiten in der Praxis (theoretisch unendlich, praktisch alle Wartezeiten über die Lebensdauer der Praxis hinweg).</li>
      <li><strong>Stetig</strong> — Wartezeit kann auf beliebige Sekunde fallen.</li>
      <li><code>=MITTELWERT(A1:A312)</code> für den Durchschnitt, <code>=MAX(A1:A312)</code> für die längste Wartezeit. Auch nützlich: <code>=MEDIAN(...)</code> als robusteres Lagemass.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 3 — Sortieren mit Excel</div>
    <p>In Zelle B2: <code>=KKLEINSTE($A$2:$A$21; ZEILE()-1)</code></p>
    <p>Erklärung: <code>ZEILE()</code> gibt die aktuelle Zeilennummer (in B2 also 2). <code>ZEILE()-1</code> wird so zu 1 in B2, zu 2 in B3 usw. Beim Kopieren der Formel bis B21 entsteht automatisch die sortierte Liste. Die <code>$</code>-Zeichen halten den Bezugsbereich fest.</p>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 4 — Bias erkennen</div>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Coverage-Bias:</strong> Nur Online-Leserinnen werden erreicht. Wer die Zeitung in Papier liest oder gar nicht — wird nicht erfasst.</li>
      <li><strong>Selbstselektions-Bias:</strong> Wer auf eine Online-Umfrage klickt, ist meist motivierter (positiv oder negativ) als der Durchschnitt — nicht zufällig ausgewählt.</li>
    </ul>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 5 — Frageformulierung</div>
    <p><strong>Suggestiv:</strong> „Wärst du auch dafür, dass die Pausen verlängert werden, damit man sich besser erholen kann?"</p>
    <p><strong>Neutral:</strong> „Sollten die Pausen um 5 Minuten verlängert werden? Antwort: Ja / Nein / Unentschieden."</p>
    <p>Die suggestive Version enthält das Wort „auch" (impliziert Konsens) und nennt einen positiven Grund — beides drängt zur Zustimmung.</p>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 6 — Stichprobenumfang</div>
    <p>Sinnvolle Grössenordnung: <strong>500 bis 5 000</strong>. Mit n = 50 wäre der Stichprobenumfang viel zu klein für eine 800 000-Grundgesamtheit. Mit n = 50 000 wäre der Aufwand unverhältnismässig hoch — die Genauigkeit nimmt ab n ≈ 1000 nur noch wenig zu (das ist ein Resultat aus der Stichprobentheorie). Repräsentative Studien zur Schweizer Jugend arbeiten typischerweise mit n ≈ 1000 bis 2000.</p>
  </div>
'''


# ════════════════════════════════════════════════════════════════════
# G4-2 — Diagramme
# ════════════════════════════════════════════════════════════════════
G4_2 = dict(themenseite='g4-2-diagramme.html', nr='4.2', thema_titel='Diagramme')

G4_2_HANDOUT = '''  <h2>1. Klassieren — der Schritt vor dem Diagramm</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definition</div>
    <p><strong>Klassieren</strong> bedeutet, einen Wertebereich in Intervalle (Klassen) gleicher Breite zu unterteilen und für jede Klasse die Anzahl der hineinfallenden Werte (<em>Klassenhäufigkeit</em>) zu zählen. Notwendig vor allem bei <strong>stetigen</strong> Daten.</p>
  </div>

  <h3>Faustregel zur Klassenanzahl</h3>
  <p>Anzahl Klassen \\(k \\approx \\sqrt{n}\\), gerundet auf eine sinnvolle Zahl. Klassenbreite \\(= (\\text{max} - \\text{min}) / k\\), aufgerundet auf einen einfachen Wert (1, 2, 5, 10).</p>

  <table class="ftb-tabelle">
    <thead><tr><th>n</th><th>k (Faustregel)</th><th>typisch verwendet</th></tr></thead>
    <tbody>
      <tr><td>10–25</td><td>3–5</td><td class="li">5 Klassen</td></tr>
      <tr><td>25–100</td><td>5–10</td><td class="li">5–8 Klassen</td></tr>
      <tr><td>100–500</td><td>10–22</td><td class="li">10–15 Klassen</td></tr>
      <tr><td>>500</td><td>>22</td><td class="li">je nach Auflösung</td></tr>
    </tbody>
  </table>


  <h2>2. Die vier Standarddiagramme</h2>

  <table class="ftb-tabelle">
    <thead><tr><th>Diagramm</th><th>für welchen Datentyp</th><th>was zeigt es</th></tr></thead>
    <tbody>
      <tr><td class="li"><strong>Balkendiagramm</strong></td><td>kategorial oder diskret</td><td class="li">Höhen vergleichen</td></tr>
      <tr><td class="li"><strong>Kuchendiagramm</strong></td><td>kategorial (max. ~6 Kategorien)</td><td class="li">Anteile am Ganzen</td></tr>
      <tr><td class="li"><strong>Histogramm</strong></td><td>stetig (klassiert)</td><td class="li">Verteilungsform</td></tr>
      <tr><td class="li"><strong>Boxplot</strong></td><td>stetig oder diskret</td><td class="li">Lage, Streuung, Schiefe</td></tr>
    </tbody>
  </table>

  <div class="block block-fehler">
    <div class="block-titel">⚠ Häufiger Fehler — Histogramm vs. Balkendiagramm</div>
    <p>Im <strong>Histogramm</strong> berühren sich die Säulen (stetiger Wertebereich, in Klassen unterteilt). Im <strong>Balkendiagramm</strong> stehen die Balken mit Lücken (kategoriale oder diskrete Werte). Wer einem stetigen Merkmal Lücken gibt, behauptet implizit, dass „nichts dazwischen" möglich ist — das ist falsch.</p>
  </div>


  <h2>3. Verteilungen charakterisieren</h2>

  <table class="ftb-tabelle">
    <thead><tr><th>Eigenschaft</th><th>Bedeutung</th></tr></thead>
    <tbody>
      <tr><td class="li"><strong>symmetrisch</strong></td><td>links und rechts vom Maximum gleich auslaufend</td></tr>
      <tr><td class="li"><strong>linksschief</strong></td><td>langer Schwanz nach links — Mittelwert &lt; Median</td></tr>
      <tr><td class="li"><strong>rechtsschief</strong></td><td>langer Schwanz nach rechts — Mittelwert &gt; Median</td></tr>
      <tr><td class="li"><strong>unimodal</strong></td><td>ein einziger Gipfel</td></tr>
      <tr><td class="li"><strong>bimodal / multimodal</strong></td><td>zwei oder mehr Gipfel</td></tr>
    </tbody>
  </table>


  <h2>4. Bivariate Daten — Streudiagramm</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definition</div>
    <p>Bei <strong>bivariaten</strong> Daten wird zu jedem Objekt ein Wertepaar \\((x, y)\\) erhoben. Das <strong>Streudiagramm</strong> trägt jedes Paar als Punkt in einem Koordinatensystem ein. Es zeigt, ob ein <em>Zusammenhang</em> zwischen den beiden Merkmalen besteht.</p>
  </div>

  <h3>Zusammenhangs-Typen</h3>
  <ul style="margin:2mm 0 0 6mm">
    <li><strong>positiver Zusammenhang</strong>: x↑ → y↑ (z. B. Körpergrösse / Schuhgrösse)</li>
    <li><strong>negativer Zusammenhang</strong>: x↑ → y↓ (z. B. Lernzeit / Fehlerzahl)</li>
    <li><strong>kein Zusammenhang</strong>: Punkte chaotisch verteilt</li>
    <li><strong>nicht-linearer Zusammenhang</strong>: Bogen oder Kurve sichtbar</li>
  </ul>

  <div class="block block-tipp">
    <div class="block-titel">💡 Korrelation ≠ Kausalität</div>
    <p>Ein erkennbarer Zusammenhang im Streudiagramm beweist nicht, dass das eine das andere <em>verursacht</em>. Beispiel: Eisverkauf und Sonnenbrand korrelieren — beide hängen aber an der Sonne, nicht aneinander.</p>
  </div>
'''

G4_2_FORMELAUSZUG = '''  <h2>Klassieren bei stetigen Daten</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Grösse</th><th>Formel / Faustregel</th></tr></thead>
    <tbody>
      <tr><td class="li">Anzahl Klassen \\(k\\)</td><td>\\(\\approx \\sqrt{n}\\), gerundet</td></tr>
      <tr><td class="li">Klassenbreite \\(b\\)</td><td>\\(b = (\\text{max} - \\text{min}) / k\\)</td></tr>
      <tr><td class="li">Klassenmitte</td><td>\\(\\text{Untergrenze} + b/2\\)</td></tr>
    </tbody>
  </table>

  <h2>Diagrammwahl nach Datentyp</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Datentyp</th><th>Standarddiagramm</th><th>auch möglich</th></tr></thead>
    <tbody>
      <tr><td class="li">kategorial</td><td>Balken- oder Kuchendiagramm</td><td>Tabelle</td></tr>
      <tr><td class="li">diskret</td><td>Balkendiagramm (mit Lücken)</td><td>Boxplot</td></tr>
      <tr><td class="li">stetig</td><td>Histogramm (ohne Lücken)</td><td>Boxplot</td></tr>
      <tr><td class="li">bivariat</td><td>Streudiagramm</td><td>—</td></tr>
    </tbody>
  </table>

  <h2>Verteilungsformen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Form</th><th>Erkennen</th><th>typisch bei</th></tr></thead>
    <tbody>
      <tr><td class="li">symmetrisch</td><td>spiegelbildlich um den Gipfel</td><td>Körpergrössen, Messfehler</td></tr>
      <tr><td class="li">rechtsschief</td><td>langer Schwanz rechts</td><td>Einkommen, Wartezeiten</td></tr>
      <tr><td class="li">linksschief</td><td>langer Schwanz links</td><td>Lebensalter (theoretisch)</td></tr>
      <tr><td class="li">bimodal</td><td>zwei Gipfel</td><td>Körpergrössen gemischt nach Geschlecht</td></tr>
    </tbody>
  </table>

  <h2>Boxplot — die fünf Zahlen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Element</th><th>Bedeutung</th></tr></thead>
    <tbody>
      <tr><td class="li">Whisker links</td><td>Minimum (oder Q1 − 1.5·IQR)</td></tr>
      <tr><td class="li">Box-links</td><td>Q1 (unteres Quartil)</td></tr>
      <tr><td class="li">Mittellinie</td><td>Median</td></tr>
      <tr><td class="li">Box-rechts</td><td>Q3 (oberes Quartil)</td></tr>
      <tr><td class="li">Whisker rechts</td><td>Maximum (oder Q3 + 1.5·IQR)</td></tr>
    </tbody>
  </table>

  <h2>Streudiagramm — Zusammenhangs-Typen</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Typ</th><th>Punktwolke</th></tr></thead>
    <tbody>
      <tr><td class="li">positiv</td><td>steigend von links unten nach rechts oben</td></tr>
      <tr><td class="li">negativ</td><td>fallend von links oben nach rechts unten</td></tr>
      <tr><td class="li">kein Zusammenhang</td><td>chaotisch verteilt</td></tr>
      <tr><td class="li">nicht-linear</td><td>klar erkennbarer Bogen oder Kurve</td></tr>
    </tbody>
  </table>

  <p style="font-size:8.5pt;color:var(--tinte-2);font-style:italic;margin-top:5mm">Quelle: Anlehnung an „Formeln, Tabellen, Begriffe", Orell Füssli Lehrmittel.</p>
'''

G4_2_TESTE = '''  <h2>Aufgaben</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li>Welches Diagramm passt am besten zu einem Datensatz von n = 12 Lieblingsfächern? Begründe.</li>
    <li>Welches Diagramm passt zu n = 200 Körpergrössen?</li>
    <li>Welches Diagramm passt, wenn du gleichzeitig Lernzeit (Stunden) und Prüfungsnote (Punkte) für n = 30 Lernende vergleichen willst?</li>
    <li>Bei einem Histogramm berühren sich die Säulen. Warum?</li>
    <li>Eine Stichprobe hat n = 64 Werte. Wie viele Klassen empfiehlt die Faustregel?</li>
    <li>Werte zwischen 12.0 und 27.0; Anzahl Klassen 5. Wie gross ist die Klassenbreite?</li>
    <li>Ein Histogramm hat einen langen Schwanz nach rechts. Welche Form? Was bedeutet das für Mittelwert vs. Median?</li>
    <li>Ein Boxplot zeigt: Median näher am Q3 als am Q1. Welche Form?</li>
    <li>Im Boxplot ist die Box deutlich kleiner als die Whisker. Was bedeutet das?</li>
    <li>Ein Streudiagramm zeigt Punkte, die wie eine fallende Gerade liegen. Welcher Zusammenhang?</li>
    <li>„Eisverkauf und Sonnenbrandfälle korrelieren stark — also verursacht Eis essen Sonnenbrand." Was ist der Denkfehler?</li>
    <li>Klassiere als Diagrammtyp: a) Anzahl Geschwister bei n = 25 Schülerinnen, b) Geburtsmonat bei n = 25 Schülerinnen, c) Wartezeit am Bankschalter bei n = 200 Kunden.</li>
    <li>Bei einer kategorialen Erhebung mit 12 Kategorien — Kuchendiagramm gut oder schlecht? Begründe.</li>
    <li>Was ist der Unterschied zwischen <em>univariat</em> und <em>bivariat</em>?</li>
    <li>Ein Histogramm hat zwei deutliche Gipfel. Wie heisst das? Was kann das bedeuten?</li>
  </ol>

  <h2 style="margin-top:6mm">Lösungen</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li><strong>Kuchen- oder Balkendiagramm</strong> — kategoriales Merkmal, kleine Anzahl Werte.</li>
    <li><strong>Histogramm</strong> — stetiges Merkmal, viele Werte → klassieren und als Säulen darstellen.</li>
    <li><strong>Streudiagramm</strong> — bivariate Daten (zwei Werte pro Objekt). Lernzeit auf x-Achse, Note auf y-Achse.</li>
    <li>Weil die Daten <em>stetig</em> sind und der Wertebereich lückenlos ist. Lücken zwischen den Säulen würden suggerieren, dass es Werte „dazwischen" nicht gibt — falsch.</li>
    <li>\\(\\sqrt{64} = 8\\) Klassen.</li>
    <li>Klassenbreite = (27.0 − 12.0) / 5 = 15.0 / 5 = <strong>3.0</strong>.</li>
    <li><strong>Rechtsschief</strong>. Der Mittelwert wird vom langen Schwanz nach rechts gezogen → Mittelwert &gt; Median.</li>
    <li><strong>Linksschief</strong>. Wenn der Median näher am Q3 (oberes Quartil) liegt, ist der untere Bereich der Verteilung weiter gestreut — Schwanz nach links.</li>
    <li>Die mittleren 50 % der Werte (= Boxbreite, Quartilsdifferenz) liegen eng beieinander, aber Minimum und Maximum sind weit entfernt — die Verteilung hat einige Ausreisser oder lange Ränder.</li>
    <li><strong>Negativer Zusammenhang</strong>: x↑ → y↓.</li>
    <li>Korrelation beweist keine Kausalität. Beide Grössen werden durch eine <strong>dritte Variable</strong> gesteuert: hohe Sonneneinstrahlung führt sowohl zu mehr Eisverkauf als auch zu mehr Sonnenbränden. Die Sonne ist der gemeinsame Verursacher.</li>
    <li>a) <strong>Balkendiagramm</strong> (diskret, mit Lücken)  b) <strong>Balken- oder Kuchendiagramm</strong> (kategorial, 12 Kategorien — Balken besser)  c) <strong>Histogramm</strong> (stetig, n gross genug zum Klassieren).</li>
    <li><strong>Schlecht</strong>. 12 Kategorien sind zu viele für ein Kuchendiagramm — die Sektoren werden zu klein und die Beschriftung unleserlich. Ein <strong>Balkendiagramm</strong> ist besser.</li>
    <li><strong>univariat</strong>: ein Wert pro Objekt (z.B. nur Körpergrösse). <strong>bivariat</strong>: zwei Werte pro Objekt (z.B. Körpergrösse <em>und</em> Schuhgrösse).</li>
    <li><strong>Bimodal</strong>. Häufig ein Hinweis auf zwei <em>Untergruppen</em> in den Daten — z.B. Körpergrössen einer Mischung aus Männern und Frauen, oder Reaktionszeiten von Geübten und Anfängerinnen.</li>
  </ol>
'''

G4_2_AUFGABEN = '''  <h2>Aufgaben</h2>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 1 — Histogramm konstruieren</div>
    <p>Eine Klasse misst die Körpergrössen (in cm) von 25 Schülerinnen:</p>
    <p style="font-family:var(--mono);font-size:0.92rem">158, 162, 165, 167, 168, 169, 170, 170, 171, 171, 172, 173, 173, 174, 175, 176, 177, 178, 179, 180, 182, 183, 185, 187, 189</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Wie viele Klassen empfiehlt die Faustregel?</li>
      <li>Bestimme Klassenbreite und Klassengrenzen.</li>
      <li>Berechne die Klassenhäufigkeiten.</li>
      <li>Charakterisiere die Verteilung (symmetrisch, schief, unimodal, bimodal).</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 2 — Diagrammwahl rechtfertigen</div>
    <p>Für jeden der folgenden Datensätze: nenne den passenden Diagrammtyp und begründe.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Lieblingsmusikrichtung von n = 30 Personen (5 Kategorien).</li>
      <li>Wartezeiten in Minuten an einer Kasse, n = 80.</li>
      <li>Anzahl Geschwister bei n = 22 Schülerinnen.</li>
      <li>Lernzeit (Stunden) und Punkte in der Prüfung von n = 40 Lernenden.</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 3 — Boxplot lesen</div>
    <p>Ein Boxplot von Prüfungsergebnissen zeigt: min = 2.5, Q1 = 4.0, Median = 4.8, Q3 = 5.2, max = 5.7.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Welche Form hat die Verteilung? Begründe.</li>
      <li>Wie gross ist die Quartilsdifferenz?</li>
      <li>Wo liegen die mittleren 50 % der Werte?</li>
      <li>Schätze: Mittelwert grösser oder kleiner als Median? Warum?</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 4 — Streudiagramm interpretieren</div>
    <p>Ein Streudiagramm zeigt für 50 Lernende: x = Lernzeit (Stunden), y = Prüfungspunkte. Die Punkte liegen näherungsweise auf einer steigenden Geraden, mit einigen Ausnahmen.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Welcher Zusammenhang liegt vor?</li>
      <li>Bedeutet das, dass „mehr Lernen" automatisch zu „mehr Punkten" führt? Diskutiere.</li>
      <li>Warum sind „Ausnahmen" (Punkte abseits der Geraden) zu erwarten?</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 5 — Diagramm-Kritik</div>
    <p>Eine Zeitung zeigt ein Kuchendiagramm der Wahlergebnisse mit 11 Parteien. Der grösste Sektor hat 28 %, der kleinste 0.3 %. Diskutiere zwei konkrete Probleme dieser Darstellung und schlage eine bessere Alternative vor.</p>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 6 — Verteilungsform aus Kontext erraten</div>
    <p>Welche Verteilungsform erwartest du für die folgenden Erhebungen? Begründe in einem Satz.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Vermögen aller Bewohner einer Stadt.</li>
      <li>Körpergrösse einer Schulklasse mit gemischten Geschlechtern.</li>
      <li>Zeit, die Studierende für die gleiche Klausur brauchen.</li>
      <li>Augenfarbe in einer Klasse.</li>
    </ol>
  </div>


  <h2 style="margin-top:6mm">Lösungen</h2>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 1 — Histogramm konstruieren</div>
    <ol type="a">
      <li>\\(\\sqrt{25} = 5\\) Klassen.</li>
      <li>min = 158, max = 189, Spanne = 31. Klassenbreite \\(b = 31/5 = 6.2\\) — aufgerundet auf <strong>7 cm</strong>. Klassen: [158, 165), [165, 172), [172, 179), [179, 186), [186, 193).</li>
      <li>Klassenhäufigkeiten:
        <ul style="margin:1mm 0 0 5mm">
          <li>[158, 165): 2 Werte (158, 162)</li>
          <li>[165, 172): 8 Werte (165, 167, 168, 169, 170, 170, 171, 171)</li>
          <li>[172, 179): 9 Werte (172, 173, 173, 174, 175, 176, 177, 178)</li>
          <li>[179, 186): 4 Werte (179, 180, 182, 183, 185)</li>
          <li>[186, 193): 2 Werte (187, 189)</li>
        </ul>
      </li>
      <li><strong>Annähernd symmetrisch und unimodal</strong> mit Gipfel im Bereich 165–179 cm. Plausibel für ein Mischmaterial aus Frauen und Männern in einer Klasse.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 2 — Diagrammwahl rechtfertigen</div>
    <ol type="a">
      <li><strong>Kuchen- oder Balkendiagramm</strong> — kategoriales Merkmal, 5 Kategorien (Kuchen funktioniert noch gut).</li>
      <li><strong>Histogramm</strong> — stetiges Merkmal, Wartezeiten in Klassen einteilen.</li>
      <li><strong>Balkendiagramm</strong> mit Lücken — diskretes Merkmal, kleine Anzahl Werte.</li>
      <li><strong>Streudiagramm</strong> — bivariate Daten, sucht Zusammenhang zwischen den beiden Grössen.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 3 — Boxplot lesen</div>
    <ol type="a">
      <li><strong>Linksschief</strong>. Der Median (4.8) liegt näher am Q3 (5.2) als am Q1 (4.0), und der untere Whisker reicht weit hinunter (bis 2.5). Der „Schwanz" der Verteilung zieht nach links.</li>
      <li>QD = Q3 − Q1 = 5.2 − 4.0 = <strong>1.2</strong>.</li>
      <li>Die mittleren 50 % liegen zwischen <strong>4.0 und 5.2</strong> (= Box).</li>
      <li><strong>Mittelwert kleiner als Median</strong>. Bei linksschiefen Verteilungen zieht der lange linke Schwanz den Mittelwert nach unten.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 4 — Streudiagramm</div>
    <ol type="a">
      <li><strong>Positiver linearer Zusammenhang</strong> — mehr Lernzeit korreliert mit mehr Punkten.</li>
      <li><strong>Nein, nicht automatisch.</strong> Korrelation beweist keine Kausalität, und auch wenn ein Kausalzusammenhang plausibel ist, gibt es individuelle Unterschiede in Lernmethoden, Vorwissen, Konzentration usw.</li>
      <li>Reale Daten enthalten immer Streuung — Tagesform, Aufgabenglück, individuelle Effizienz. Eine perfekte Gerade wäre verdächtig (zu sauber, oft auf Manipulation oder kleinen n hinweisend).</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 5 — Diagramm-Kritik</div>
    <p><strong>Probleme:</strong></p>
    <ul style="margin:2mm 0 0 6mm">
      <li>11 Sektoren sind zu viele — kleine Anteile (0.3 %) sind im Kuchen praktisch unsichtbar.</li>
      <li>Beschriftung wird unlesbar oder muss ins Legende ausgelagert, was den schnellen Vergleich erschwert.</li>
      <li>Vergleiche zwischen ähnlich grossen Sektoren sind im Kuchen schwerer als im Balkendiagramm (Augen sind besser im Höhenvergleich als im Winkelvergleich).</li>
    </ul>
    <p><strong>Alternative:</strong> Horizontales Balkendiagramm, Parteien nach Grösse sortiert. So sind alle Werte direkt vergleichbar und auch kleine Anteile bleiben sichtbar.</p>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 6 — Verteilungsform</div>
    <ol type="a">
      <li><strong>Stark rechtsschief</strong> — wenige sehr Vermögende erzeugen einen langen Schwanz nach rechts.</li>
      <li><strong>Bimodal</strong> — zwei Gipfel, je einer für Frauen und Männer (durchschnittlich unterschiedliche Körpergrösse).</li>
      <li><strong>Symmetrisch und unimodal</strong> (näherungsweise normalverteilt) — die meisten brauchen mittellange Zeit, wenige sehr kurz oder sehr lang.</li>
      <li>Keine kontinuierliche Form — kategorial. Daher Balken- oder Kuchendiagramm, nicht Histogramm.</li>
    </ol>
  </div>
'''


# ════════════════════════════════════════════════════════════════════
# G4-3 — Masszahlen
# ════════════════════════════════════════════════════════════════════
G4_3 = dict(themenseite='g4-3-masszahlen.html', nr='4.3', thema_titel='Masszahlen')

G4_3_HANDOUT = '''  <h2>1. Lagemasse — wo liegt die Mitte?</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definitionen</div>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Mittelwert</strong> \\(\\bar{x}\\) = Summe aller Werte geteilt durch ihre Anzahl: \\[\\bar{x} = \\dfrac{1}{n}\\sum_{i=1}^{n} x_i\\]</li>
      <li><strong>Median</strong> \\(\\tilde{x}\\) = mittlerer Wert der <em>sortierten</em> Liste. Bei geradem n: Mittelwert der beiden mittleren Werte.</li>
      <li><strong>Modus</strong> \\(\\hat{x}\\) = häufigster Wert. Funktioniert auch für kategoriale Daten.</li>
    </ul>
  </div>

  <h3>Wann welches Lagemass?</h3>
  <table class="ftb-tabelle">
    <thead><tr><th>Situation</th><th>besser geeignet</th></tr></thead>
    <tbody>
      <tr><td class="li">Symmetrische Verteilung, keine Ausreisser</td><td>Mittelwert</td></tr>
      <tr><td class="li">Schiefe Verteilung oder Ausreisser</td><td>Median</td></tr>
      <tr><td class="li">Kategoriale Daten</td><td>Modus</td></tr>
      <tr><td class="li">Vergleich zweier Stichproben</td><td>Median (robust)</td></tr>
    </tbody>
  </table>


  <h2>2. Streumasse — wie breit verteilt?</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Definitionen</div>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Standardabweichung</strong> \\(s\\) = mittlere Abweichung vom Mittelwert: \\[s = \\sqrt{\\dfrac{1}{n-1}\\sum_{i=1}^{n}(x_i - \\bar{x})^2}\\] (Quadratwurzel der <em>Varianz</em> \\(s^2\\)).</li>
      <li><strong>Quartile</strong> \\(Q_1\\), \\(Q_2 = \\tilde{x}\\), \\(Q_3\\) teilen die sortierte Liste in vier gleich grosse Teile.</li>
      <li><strong>Quartilsdifferenz</strong> \\(\\text{QD} = Q_3 - Q_1\\) — Breite der mittleren 50 % der Daten (= Boxbreite im Boxplot).</li>
    </ul>
  </div>

  <div class="block block-tipp">
    <div class="block-titel">💡 Warum n − 1 (statt n) bei der Standardabweichung?</div>
    <p>Bei einer <em>Stichprobe</em> liefert die Division durch \\(n-1\\) eine bessere Schätzung der wahren Streuung in der Grundgesamtheit. Das ist die in Tabellenkalkulationen übliche Konvention (Funktion <code>STABW.S</code> bzw. <code>STDEV.S</code>).</p>
  </div>


  <h2>3. Tabellenkalkulation</h2>

  <table class="ftb-tabelle">
    <thead><tr><th>Masszahl</th><th>Excel/Calc deutsch</th><th>Englisch</th></tr></thead>
    <tbody>
      <tr><td class="li">Mittelwert</td><td>=MITTELWERT(A1:A100)</td><td>=AVERAGE(...)</td></tr>
      <tr><td class="li">Median</td><td>=MEDIAN(A1:A100)</td><td>=MEDIAN(...)</td></tr>
      <tr><td class="li">Modus</td><td>=MODUS.EINF(A1:A100)</td><td>=MODE(...)</td></tr>
      <tr><td class="li">Standardabweichung</td><td>=STABW.S(A1:A100)</td><td>=STDEV.S(...)</td></tr>
      <tr><td class="li">Q1</td><td>=QUARTILE.INKL(...;1)</td><td>=QUARTILE.INC(...;1)</td></tr>
      <tr><td class="li">Q3</td><td>=QUARTILE.INKL(...;3)</td><td>=QUARTILE.INC(...;3)</td></tr>
    </tbody>
  </table>


  <h2>4. Robustheit — Mittelwert oder Median?</h2>

  <div class="block block-def">
    <div class="block-titel">📘 Robustheit</div>
    <p>Eine Kennzahl heisst <strong>robust</strong>, wenn sie durch einzelne Extremwerte (Ausreisser) <em>kaum verändert</em> wird.</p>
    <ul style="margin:2mm 0 0 6mm">
      <li><strong>Median</strong> — robust. Verschieben einzelner Werte ändert die Mitte der sortierten Liste kaum.</li>
      <li><strong>Mittelwert</strong> — nicht robust. Jeder Wert geht mit voller Stärke in die Summe ein.</li>
    </ul>
  </div>

  <div class="block block-tipp">
    <div class="block-titel">💡 Faustregel zur Lagemass-Wahl</div>
    <p>Mittelwert und Median <em>nahe beieinander</em> → Verteilung ist annähernd symmetrisch, beide funktionieren. <em>Weit auseinander</em> → schief oder mit Ausreissern, Median bevorzugen.</p>
  </div>


  <h2>5. Zusammenhang mit dem Boxplot (Kapitel 4.2)</h2>

  <p>Die fünf Zahlen jedes Boxplots sind genau die Masszahlen aus diesem Kapitel:</p>
  <table class="ftb-tabelle">
    <thead><tr><th>Element</th><th>Wert</th></tr></thead>
    <tbody>
      <tr><td class="li">linker Whisker</td><td>Minimum</td></tr>
      <tr><td class="li">Box-links</td><td>\\(Q_1\\)</td></tr>
      <tr><td class="li">Mittellinie</td><td>Median \\(\\tilde{x}\\)</td></tr>
      <tr><td class="li">Box-rechts</td><td>\\(Q_3\\)</td></tr>
      <tr><td class="li">rechter Whisker</td><td>Maximum</td></tr>
      <tr><td class="li">Boxbreite</td><td>QD = \\(Q_3 - Q_1\\)</td></tr>
    </tbody>
  </table>

  <div class="merksatz">
    <strong>🎯 Merksatz:</strong> Eine Stichprobe ist erst dann beschrieben, wenn man <em>beide</em> Aspekte angibt: <strong>Lage</strong> (Mitte) und <strong>Streuung</strong> (Breite). Mittelwert und Standardabweichung gehen zusammen — Median und Quartilsdifferenz gehen zusammen. Die Paare nicht mischen.
  </div>
'''

G4_3_FORMELAUSZUG = '''  <h2>Lagemasse</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Mass</th><th>Symbol</th><th>Berechnung</th></tr></thead>
    <tbody>
      <tr><td class="li">Mittelwert</td><td>\\(\\bar{x}\\)</td><td>\\(\\bar{x} = \\dfrac{1}{n}\\sum x_i\\)</td></tr>
      <tr><td class="li">Median (n ungerade)</td><td>\\(\\tilde{x}\\)</td><td>Wert an Position \\(\\frac{n+1}{2}\\) der sortierten Liste</td></tr>
      <tr><td class="li">Median (n gerade)</td><td>\\(\\tilde{x}\\)</td><td>Mittelwert der Werte an Positionen \\(\\frac{n}{2}\\) und \\(\\frac{n}{2}+1\\)</td></tr>
      <tr><td class="li">Modus</td><td>\\(\\hat{x}\\)</td><td>häufigster Wert</td></tr>
    </tbody>
  </table>

  <h2>Streumasse</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Mass</th><th>Symbol</th><th>Formel</th></tr></thead>
    <tbody>
      <tr><td class="li">Varianz</td><td>\\(s^2\\)</td><td>\\(s^2 = \\dfrac{1}{n-1}\\sum (x_i - \\bar{x})^2\\)</td></tr>
      <tr><td class="li">Standardabweichung</td><td>\\(s\\)</td><td>\\(s = \\sqrt{s^2}\\)</td></tr>
      <tr><td class="li">Quartilsdifferenz (IQR)</td><td>QD</td><td>\\(\\text{QD} = Q_3 - Q_1\\)</td></tr>
    </tbody>
  </table>

  <h2>Tabellenkalkulation</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Mass</th><th>deutsch</th><th>englisch</th></tr></thead>
    <tbody>
      <tr><td class="li">Mittelwert</td><td>=MITTELWERT(A:A)</td><td>=AVERAGE(A:A)</td></tr>
      <tr><td class="li">Median</td><td>=MEDIAN(A:A)</td><td>=MEDIAN(A:A)</td></tr>
      <tr><td class="li">Modus</td><td>=MODUS.EINF(A:A)</td><td>=MODE(A:A)</td></tr>
      <tr><td class="li">Standardabw. (Stichprobe)</td><td>=STABW.S(A:A)</td><td>=STDEV.S(A:A)</td></tr>
      <tr><td class="li">1. Quartil</td><td>=QUARTILE.INKL(A:A;1)</td><td>=QUARTILE.INC(A:A;1)</td></tr>
      <tr><td class="li">3. Quartil</td><td>=QUARTILE.INKL(A:A;3)</td><td>=QUARTILE.INC(A:A;3)</td></tr>
    </tbody>
  </table>

  <h2>Faustregel zur Lagemass-Wahl</h2>
  <table class="ftb-tabelle">
    <thead><tr><th>Verteilung</th><th>Lagemass</th><th>passendes Streumass</th></tr></thead>
    <tbody>
      <tr><td class="li">symmetrisch, ohne Ausreisser</td><td>Mittelwert \\(\\bar{x}\\)</td><td>Standardabweichung \\(s\\)</td></tr>
      <tr><td class="li">schief oder mit Ausreissern</td><td>Median \\(\\tilde{x}\\)</td><td>Quartilsdifferenz QD</td></tr>
      <tr><td class="li">kategorial</td><td>Modus \\(\\hat{x}\\)</td><td>—</td></tr>
    </tbody>
  </table>

  <h2>Boxplot — die fünf Zahlen</h2>
  <p>min · \\(Q_1\\) · \\(\\tilde{x}\\) · \\(Q_3\\) · max</p>

  <p style="font-size:8.5pt;color:var(--tinte-2);font-style:italic;margin-top:5mm">Quelle: Anlehnung an „Formeln, Tabellen, Begriffe", Orell Füssli Lehrmittel.</p>
'''

G4_3_TESTE = '''  <h2>Aufgaben</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li>Berechne den Mittelwert von 4, 7, 2, 9, 8.</li>
    <li>Berechne den Median von 4, 7, 2, 9, 8.</li>
    <li>Berechne den Median von 3, 5, 8, 10.</li>
    <li>Bestimme den Modus von 2, 3, 3, 5, 7, 3, 9, 5, 5, 5.</li>
    <li>Welches Lagemass passt zu Lieblingsfarben in einer Klasse?</li>
    <li>Eine Stichprobe hat \\(\\bar{x} = 50\\), Median = 30. Welche Form hat die Verteilung wahrscheinlich?</li>
    <li>Berechne die Standardabweichung von 4, 4, 4, 4, 4. Was bedeutet das Ergebnis?</li>
    <li>Berechne die Standardabweichung von 2, 4, 6 (n = 3, also durch n − 1 = 2 teilen).</li>
    <li>Welche Excel-Formel berechnet die Standardabweichung der Stichprobe in den Zellen B2:B100?</li>
    <li>Sortierte Liste: 1, 2, 3, 4, 5, 6, 7, 8. Bestimme \\(Q_1\\), \\(Q_3\\) und QD.</li>
    <li>Sortierte Liste: 10, 12, 14, 18, 22, 27, 30. Bestimme \\(Q_1\\) und \\(Q_3\\). (Hinweis: ungerades n.)</li>
    <li>Eine Stichprobe hat \\(s = 0\\). Was bedeutet das?</li>
    <li>In einem Betrieb verdienen alle 4500 Fr. ausser der Inhaberin (50 000 Fr.). Welches Lagemass beschreibt das „typische" Einkommen besser?</li>
    <li>Klasse X: \\(\\bar{x} = 4.5\\), \\(s = 0.4\\). Klasse Y: \\(\\bar{x} = 4.5\\), \\(s = 1.3\\). Welche Klasse ist homogener?</li>
    <li>Boxplot: min = 5, \\(Q_1\\) = 12, Median = 14, \\(Q_3\\) = 16, max = 22. Wie gross ist die Box, wie gross die QD?</li>
  </ol>

  <h2 style="margin-top:6mm">Lösungen</h2>

  <ol style="margin:2mm 0 0 6mm;line-height:1.7">
    <li>\\(\\bar{x} = (4+7+2+9+8)/5 = 30/5 = \\mathbf{6}\\).</li>
    <li>Sortiert: 2, 4, 7, 8, 9. Mittlere Position (Position 3): \\(\\tilde{x} = \\mathbf{7}\\).</li>
    <li>Sortiert: 3, 5, 8, 10. n gerade → Mittel der Werte an Position 2 und 3: \\(\\tilde{x} = (5+8)/2 = \\mathbf{6.5}\\).</li>
    <li>Modus = <strong>5</strong> (kommt viermal vor, häufiger als alle anderen Werte).</li>
    <li><strong>Modus</strong> — kategoriale Daten haben keinen Mittelwert oder Median.</li>
    <li><strong>Rechtsschief</strong>. Mittelwert deutlich grösser als Median → langer Schwanz nach rechts (z.B. einige sehr grosse Werte ziehen den Mittelwert nach oben).</li>
    <li>\\(s = 0\\) — alle Werte gleich, keine Streuung.</li>
    <li>\\(\\bar{x} = (2+4+6)/3 = 4\\). Abweichungen: −2, 0, 2. Quadrate: 4, 0, 4. Summe = 8. \\(s = \\sqrt{8/(3-1)} = \\sqrt{4} = \\mathbf{2}\\).</li>
    <li><code>=STABW.S(B2:B100)</code> bzw. englisch <code>=STDEV.S(B2:B100)</code>.</li>
    <li>Untere Hälfte: 1, 2, 3, 4 → \\(Q_1 = (2+3)/2 = 2.5\\). Obere Hälfte: 5, 6, 7, 8 → \\(Q_3 = (6+7)/2 = 6.5\\). QD = 6.5 − 2.5 = <strong>4</strong>.</li>
    <li>n = 7 ungerade. Median = Position 4 = 18. Untere Hälfte (ohne Median): 10, 12, 14 → \\(Q_1 = 12\\). Obere Hälfte: 22, 27, 30 → \\(Q_3 = 27\\).</li>
    <li>Alle Werte in der Stichprobe sind gleich — die Verteilung hat keine Streuung.</li>
    <li><strong>Median</strong> = 4 500 Fr. — der Mittelwert wäre durch die Inhaberin stark verzerrt.</li>
    <li><strong>Klasse X</strong> ist homogener: kleinere Standardabweichung (0.4 vs. 1.3) bedeutet, die Werte liegen enger um den Mittelwert.</li>
    <li>Box: von 12 bis 16. Boxbreite = QD = 16 − 12 = <strong>4</strong>.</li>
  </ol>
'''

G4_3_AUFGABEN = '''  <h2>Aufgaben</h2>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 1 — Klassenarbeit auswerten</div>
    <p>20 Lernende erreichen folgende Punkte: 12, 18, 15, 14, 17, 16, 20, 14, 13, 15, 16, 18, 11, 17, 19, 14, 16, 15, 12, 18.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Berechne Mittelwert, Median und Modus.</li>
      <li>Bestimme \\(Q_1\\), \\(Q_3\\) und die Quartilsdifferenz.</li>
      <li>Berechne die Standardabweichung. (Tipp: zur Erleichterung Hilfsspalten anlegen.)</li>
      <li>Charakterisiere die Verteilung kurz.</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 2 — Robustheit bei Ausreisser</div>
    <p>Eine Stichprobe von n = 7 Werten ergibt: 4, 4, 5, 5, 6, 6, 7. Plötzlich wird ein 8. Wert hinzugefügt: <strong>50</strong> (Tippfehler oder Ausreisser).</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Berechne Mittelwert <em>vor</em> und <em>nach</em> dem Hinzufügen.</li>
      <li>Berechne Median <em>vor</em> und <em>nach</em>.</li>
      <li>Welches Lagemass ist robuster gegen den Ausreisser? Quantifiziere den Unterschied.</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 3 — Schwimmtraining</div>
    <p>Eine Schwimmerin notiert ihre Zeiten über 50 m (in Sekunden) an fünf Tagen: 28.4, 28.6, 28.5, 28.9, 28.6.</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Berechne Mittelwert und Standardabweichung.</li>
      <li>Interpretiere das Ergebnis: ist die Schwimmerin konstant?</li>
      <li>Schätze ohne Rechnung, wie sich die Standardabweichung ändert, wenn ein Tag mit 30.0 s hinzugefügt wird.</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 4 — Tabellenkalkulation</div>
    <p>In Spalte A (Zellen A2 bis A201) stehen 200 Verkaufszahlen einer Bäckerei. Schreibe Excel-/Calc-Formeln für:</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Mittelwert</li>
      <li>Median</li>
      <li>Standardabweichung der Stichprobe</li>
      <li>Quartilsdifferenz (in einer einzigen Formel)</li>
      <li>Anzahl Tage, an denen der Verkauf grösser war als der Median</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 5 — Zwei Filialen</div>
    <p>Bäckerei A und B notieren über 30 Tage ihre Verkaufszahlen.</p>
    <p style="margin-top:2mm"><strong>Filiale A:</strong> \\(\\bar{x} = 320\\), Median = 318, \\(s = 22\\), QD = 30</p>
    <p><strong>Filiale B:</strong> \\(\\bar{x} = 320\\), Median = 280, \\(s = 65\\), QD = 50</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Welche Filiale hat ein konstanteres Geschäft? Begründe.</li>
      <li>Welche Filiale hat möglicherweise einzelne Spitzentage? Begründe aus den Zahlen.</li>
      <li>Welches Lagemass ist für Filiale B aussagekräftiger? Warum?</li>
    </ol>
  </div>

  <div class="block block-aufg">
    <div class="block-titel">🟠 Aufgabe 6 — Eigene Erhebung</div>
    <p>Erhebe eine kleine Stichprobe (n ≥ 15) zu einem Merkmal deiner Wahl — z. B. tägliche Bildschirmzeit, Anzahl Schritte, Pulsfrequenz nach 1 Min Hampelmänner. Erstelle:</p>
    <ol type="a" style="margin:2mm 0 0 6mm">
      <li>Urliste und sortierte Liste.</li>
      <li>Mittelwert, Median, Modus, Standardabweichung, \\(Q_1\\), \\(Q_3\\), Quartilsdifferenz.</li>
      <li>Einen Boxplot von Hand oder mit Tabellenkalkulation.</li>
      <li>3–5 Sätze Interpretation: Was sagen die Masszahlen? Gibt es Ausreisser? Welches Lagemass passt besser?</li>
    </ol>
  </div>


  <h2 style="margin-top:6mm">Lösungen</h2>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 1 — Klassenarbeit</div>
    <p>Sortiert: 11, 12, 12, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 18, 18, 18, 19, 20.</p>
    <ol type="a">
      <li>\\(\\bar{x} = 310/20 = \\mathbf{15.5}\\). Median = (15 + 16)/2 = <strong>15.5</strong>. Modus: 14, 15, 16, 18 kommen je 3-mal vor (mehrere Modi).</li>
      <li>Untere Hälfte (Positionen 1–10): 11, 12, 12, 13, 14, 14, 14, 15, 15, 15. \\(Q_1 = (14+14)/2 = \\mathbf{14}\\). Obere Hälfte (Positionen 11–20): 16, 16, 16, 17, 17, 18, 18, 18, 19, 20. \\(Q_3 = (17+18)/2 = \\mathbf{17.5}\\). QD = 17.5 − 14 = <strong>3.5</strong>.</li>
      <li>Abweichungen \\((x_i - 15.5)\\) quadriert summieren: ergibt 102. \\(s = \\sqrt{102/19} \\approx \\mathbf{2.32}\\).</li>
      <li>Mittelwert = Median, mehrere Modi → annähernd <strong>symmetrische, leicht multimodale</strong> Verteilung. Mittlere 50 % zwischen 14 und 17.5.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 2 — Robustheit</div>
    <ol type="a">
      <li><strong>Vor:</strong> \\(\\bar{x} = 37/7 \\approx 5.29\\). <strong>Nach:</strong> \\(\\bar{x} = 87/8 \\approx 10.88\\). Sprung: +5.59.</li>
      <li><strong>Vor:</strong> Median = 5. <strong>Nach:</strong> sortiert 4, 4, 5, 5, 6, 6, 7, 50; Median = (5+6)/2 = 5.5. Sprung: +0.5.</li>
      <li>Der <strong>Median</strong> ist deutlich robuster: Verschiebung um 0.5 vs. 5.59 beim Mittelwert. Der Ausreisser hat den Mittelwert mehr als verdoppelt — den Median kaum bewegt.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 3 — Schwimmtraining</div>
    <ol type="a">
      <li>\\(\\bar{x} = (28.4+28.6+28.5+28.9+28.6)/5 = 143.0/5 = \\mathbf{28.60}\\) s. Abweichungen: −0.20, 0.00, −0.10, 0.30, 0.00. Quadrate: 0.04, 0, 0.01, 0.09, 0. Summe = 0.14. \\(s = \\sqrt{0.14/4} = \\sqrt{0.035} \\approx \\mathbf{0.19}\\) s.</li>
      <li>Streuung von ca. 2 Zehntelsekunden um den Mittelwert — die Schwimmerin ist <strong>sehr konstant</strong>.</li>
      <li>Der neue Wert 30.0 s liegt 1.4 s über dem bisherigen Mittelwert — das ist 7 mal die bisherige Standardabweichung. Mittelwert und vor allem Standardabweichung würden <strong>deutlich grösser</strong>. (Tatsächlich: \\(\\bar{x} \\approx 28.83\\), \\(s \\approx 0.59\\) — Standardabweichung verdreifacht.)</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 4 — Tabellenkalkulation</div>
    <ol type="a">
      <li><code>=MITTELWERT(A2:A201)</code></li>
      <li><code>=MEDIAN(A2:A201)</code></li>
      <li><code>=STABW.S(A2:A201)</code></li>
      <li><code>=QUARTILE.INKL(A2:A201;3) − QUARTILE.INKL(A2:A201;1)</code></li>
      <li><code>=ZÄHLENWENN(A2:A201;">"&amp;MEDIAN(A2:A201))</code></li>
    </ol>
    <p>Hinweis zu e): Das <code>&amp;</code>-Zeichen verkettet den Operator <code>"&gt;"</code> mit dem Wert des Medians zu einer Zeichenkette, die ZÄHLENWENN als Kriterium akzeptiert.</p>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 5 — Zwei Filialen</div>
    <ol type="a">
      <li><strong>Filiale A</strong> ist konstanter: kleinere Standardabweichung (22 vs. 65) und kleinere Quartilsdifferenz (30 vs. 50).</li>
      <li><strong>Filiale B</strong> hat möglicherweise Spitzentage: Mittelwert (320) deutlich grösser als Median (280), grosse Standardabweichung (65). Beides spricht für rechtsschiefe Verteilung mit einigen sehr grossen Werten.</li>
      <li>Für Filiale B ist der <strong>Median</strong> aussagekräftiger — er beschreibt den „typischen" Verkaufstag (280 Stück), während der Mittelwert (320) durch die Spitzentage nach oben gezogen wird und kein realistisches Alltagsbild liefert.</li>
    </ol>
  </div>

  <div class="block block-bsp">
    <div class="block-titel">🟢 Lösung 6 — Eigene Erhebung</div>
    <p>Individuelle Aufgabe — hier Kontroll-Schema:</p>
    <ul style="margin:2mm 0 0 6mm">
      <li>Anzahl Werte korrekt gezählt? n stimmt?</li>
      <li>\\(Q_1 \\le \\) Median \\(\\le Q_3\\)? (Sonst Fehler.)</li>
      <li>Standardabweichung positiv und in plausibler Grössenordnung relativ zum Mittelwert?</li>
      <li>Mittelwert und Median weit auseinander → suche im Boxplot oder Histogramm nach Ausreissern. Ist Median dann besseres Lagemass?</li>
      <li>Tipp: Nimm eine Tabellenkalkulation und prüfe deine Handrechnung gegen <code>MITTELWERT</code>, <code>MEDIAN</code>, <code>STABW.S</code>.</li>
    </ul>
  </div>
'''


# ════════════════════════════════════════════════════════════════════
# Generation
# ════════════════════════════════════════════════════════════════════
SPECS = [
    # G4-1
    (G4_1, 'handout',           'Handout',           'Handout — Theorie',           '',                                                                              G4_1_HANDOUT, ''),
    (G4_1, 'formelauszug',      'Formelauszug',      'Formelauszug',                '',                                                                              G4_1_FORMELAUSZUG, FORMELAUSZUG_EXTRA_STYLE),
    (G4_1, 'teste-dich-selbst', 'Teste dich selbst', 'Teste dich selbst',           '15 Grundlagenaufgaben mit Lösungen. Erst rechnen, dann nachschauen.',           G4_1_TESTE, ''),
    (G4_1, 'aufgabenserie',     'Aufgabenserie',     'Aufgabenserie — Anwendungen', 'Sechs Anwendungsaufgaben aus Statistik-Praxis und Empirie. Mit Lösungen.',     G4_1_AUFGABEN, ''),

    # G4-2
    (G4_2, 'handout',           'Handout',           'Handout — Theorie',           '',                                                                              G4_2_HANDOUT, ''),
    (G4_2, 'formelauszug',      'Formelauszug',      'Formelauszug',                '',                                                                              G4_2_FORMELAUSZUG, FORMELAUSZUG_EXTRA_STYLE),
    (G4_2, 'teste-dich-selbst', 'Teste dich selbst', 'Teste dich selbst',           '15 Grundlagenaufgaben mit Lösungen. Erst rechnen, dann nachschauen.',           G4_2_TESTE, ''),
    (G4_2, 'aufgabenserie',     'Aufgabenserie',     'Aufgabenserie — Anwendungen', 'Sechs Anwendungsaufgaben aus Datenanalyse und Diagrammwahl. Mit Lösungen.',    G4_2_AUFGABEN, ''),

    # G4-3
    (G4_3, 'handout',           'Handout',           'Handout — Theorie',           '',                                                                              G4_3_HANDOUT, ''),
    (G4_3, 'formelauszug',      'Formelauszug',      'Formelauszug',                '',                                                                              G4_3_FORMELAUSZUG, FORMELAUSZUG_EXTRA_STYLE),
    (G4_3, 'teste-dich-selbst', 'Teste dich selbst', 'Teste dich selbst',           '15 Grundlagenaufgaben mit Lösungen. Erst rechnen, dann nachschauen.',           G4_3_TESTE, ''),
    (G4_3, 'aufgabenserie',     'Aufgabenserie',     'Aufgabenserie — Anwendungen', 'Sechs Anwendungsaufgaben aus Praxis und Tabellenkalkulation. Mit Lösungen.',   G4_3_AUFGABEN, ''),
]


THEMA_DIR = {
    'g4-1-grundlagen.html':  'g4-1-grundlagen',
    'g4-2-diagramme.html':   'g4-2-diagramme',
    'g4-3-masszahlen.html':  'g4-3-masszahlen',
}

if __name__ == '__main__':
    base = 'downloads/grundlagen'
    written = 0
    for thema, slug, druck_titel, druck_titel_h1, subtitle, body, extra_style in SPECS:
        out_dir = os.path.join(base, THEMA_DIR[thema['themenseite']])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f'{slug}.html')
        # Formelauszug nutzt scale 0.95 wie in g5-1, sonst 1.0
        mj_scale = 0.95 if slug == 'formelauszug' else 1.0
        html = render(
            druck_titel=druck_titel,
            druck_titel_h1=druck_titel_h1,
            themenseite=thema['themenseite'],
            nr=thema['nr'],
            thema_titel=thema['thema_titel'],
            body=body,
            subtitle=subtitle,
            extra_style=extra_style,
            mj_scale=mj_scale,
        )
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        written += 1
        print(f'  {out_path}')
    print(f'\n{written} Druckseiten geschrieben.')
