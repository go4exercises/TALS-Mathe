#!/usr/bin/env python3
"""
Schreibt den Clip-Block in die Lektionsseiten.

Verfahren wie bei scripts/build-seo.py: Du setzt einmal pro Seite die beiden
Kommentarzeilen

    <!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
    <!-- CLIPS:ENDE -->

danach pflegt sich der Block selbst. Welche Clips auf welche Seite gehoeren,
steht ausschliesslich im Drehbuch unter `lektion` (eine Liste von Codes aus
nav.js) — nicht in der Seite. Ein Clip kann so auf mehreren Seiten stehen,
ohne dass er dupliziert wird.

Der Block enthaelt eine Startkarte je Clip und darunter das Transkript aus
clips/sprechertext-*.txt. Das Transkript ist nicht Beiwerk: Von einem
animierten Clip sieht eine Suchmaschine sonst gar nichts, und die
Volltextsuche der Site ebenfalls nicht.

Der Clip selbst wird erst beim Klick geladen (clipStart in mathlib.js).

    python3 scripts/build-clips-einbau.py            # Probelauf
    python3 scripts/build-clips-einbau.py --schreiben

Vorher `python3 scripts/build-clips.py` laufen lassen — dieses Skript liest
clips/clips.json und baut selbst keine Clips.
"""

import argparse
import html
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")

MARKE_AUF = ('<!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, '
             'nicht von Hand ändern -->')
MARKE_ZU = '<!-- CLIPS:ENDE -->'
BLOCK = re.compile(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), re.DOTALL)


def lektionsseiten():
    """Code -> Seitenpfad, gelesen aus nav.js. Das ist die einzige Liste,
    die weiss, welche Lektion auf welcher Datei liegt."""
    quelle = open(os.path.join(WURZEL, "nav.js"), encoding="utf-8").read()
    paare = re.findall(r"id:\s*'([^']+)'.*?url:\s*'([^']+)'", quelle)
    return dict(paare)


def mmss(sekunden):
    return f"{int(sekunden) // 60}:{int(sekunden) % 60:02d}"


def transkript(datei):
    """clips/sprechertext-<name>.txt -> Liste (Zeit, Text). Fehlt die Datei,
    gibt es kein Transkript — das meldet das Skript, es ist kein Abbruch."""
    pfad = os.path.join(CLIPS, "sprechertext-" + datei.replace(".html", "") + ".txt")
    if not os.path.exists(pfad):
        return None
    zeilen = []
    for z in open(pfad, encoding="utf-8"):
        if "\t" not in z:
            continue
        t, txt = z.split("\t", 1)
        try:
            zeilen.append((mmss(float(t)), txt.strip()))
        except ValueError:
            continue
    return zeilen or None


def block_bauen(clips, tiefe):
    """tiefe = Ebenen unter der Wurzel, daraus wird der ../-Praefix."""
    vor = "../" * tiefe
    aus = [MARKE_AUF, '<h2 id="clips">Clips</h2>', '<div class="clip-grid">']
    for c in clips:
        titel = html.escape(c["titel"])
        aus += [
            f'<div class="clip" data-clip="{vor}clips/{c["datei"]}" data-titel="{titel}">',
            '  <button class="clip-start" type="button" onclick="clipStart(this)">',
            '    <span class="clip-play" aria-hidden="true">▶</span>',
            '    <span>',
            f'      <span class="clip-titel">{titel} abspielen</span>',
            f'      <span class="clip-text">{html.escape(c.get("kurzbeschrieb", ""))}</span>',
            f'      <span class="clip-meta">{mmss(c.get("dauer_s", 0))} · CLIP</span>',
            '    </span>',
            '  </button>',
            '</div>',
        ]
        tk = transkript(c["datei"])
        if tk:
            aus.append('<details class="clip-transkript">')
            aus.append(f'<summary>Transkript · {titel}</summary>')
            aus.append('<ol>')
            for zeit, txt in tk:
                aus.append(f'<li><span class="tk-zeit">{zeit}</span>'
                           f'<span>{html.escape(txt)}</span></li>')
            aus.append('</ol>')
            aus.append('</details>')
        else:
            print(f"  [WARN] kein Sprechertext zu {c['datei']}")
    aus += ['</div>', MARKE_ZU]
    return "\n".join(aus)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schreiben", action="store_true", help="Änderungen speichern")
    a = ap.parse_args()

    index = os.path.join(CLIPS, "clips.json")
    if not os.path.exists(index):
        sys.exit("clips/clips.json fehlt — erst `python3 scripts/build-clips.py` laufen lassen.")
    alle = json.load(open(index, encoding="utf-8"))["clips"]

    seiten = lektionsseiten()
    nach_lektion = {}
    for c in alle:
        codes = c.get("lektion") or []
        if isinstance(codes, str):
            codes = [codes]
        for code in codes:
            if code not in seiten:
                print(f"  [FEHLER] {c['datei']}: Lektion '{code}' steht nicht in nav.js")
                continue
            nach_lektion.setdefault(code, []).append(c)

    geaendert, gleich, ohne_marker = [], 0, []
    for code, clips in sorted(nach_lektion.items()):
        pfad = os.path.join(WURZEL, seiten[code])
        if not os.path.exists(pfad):
            print(f"  [FEHLER] {code}: {seiten[code]} existiert nicht")
            continue
        text = open(pfad, encoding="utf-8").read()
        if not BLOCK.search(text):
            ohne_marker.append((code, seiten[code], len(clips)))
            continue
        tiefe = seiten[code].count("/")
        neu = BLOCK.sub(lambda _m: block_bauen(clips, tiefe), text, count=1)
        if neu == text:
            gleich += 1
        else:
            geaendert.append((pfad, neu))

    print(f"{len(geaendert)} Seiten zu aktualisieren, {gleich} bereits aktuell")
    for code, url, n in ohne_marker:
        print(f"  [WARN] {code} hat {n} Clip(s), aber keine CLIPS-Marker in {url}")
    for pfad, _ in geaendert:
        print("   ", os.path.relpath(pfad, WURZEL))

    if not geaendert:
        return
    if not a.schreiben:
        print("\nProbelauf. Mit --schreiben werden die Änderungen gespeichert.")
        return
    for pfad, neu in geaendert:
        open(pfad, "w", encoding="utf-8").write(neu)
    print(f"\n{len(geaendert)} Seiten geschrieben.")


if __name__ == "__main__":
    main()
