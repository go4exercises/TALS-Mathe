#!/usr/bin/env python3
"""
Schreibt die Clips dorthin, wo sie erscheinen sollen: in die Lektionsseiten
und in die Bibliotheksseite clips.html.

Verfahren wie bei scripts/build-seo.py — der Inhalt zwischen zwei
Kommentarzeilen ist generiert, alles andere bleibt von Hand gepflegt.

    Lektionsseite:  <!-- CLIPS:ANFANG … -->  …  <!-- CLIPS:ENDE -->
    clips.html:     <!-- CLIPS-BIBLIOTHEK:ANFANG … -->  …  <!-- CLIPS-BIBLIOTHEK:ENDE -->

Welche Clips auf welche Seite gehoeren, steht ausschliesslich im Drehbuch
unter `lektion` (Liste von Codes aus nav.js) — nicht in der Seite. Ein Clip
kann so auf mehreren Seiten stehen, ohne dass er dupliziert wird.

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

BIB_AUF = ('<!-- CLIPS-BIBLIOTHEK:ANFANG — generiert von scripts/build-clips-einbau.py, '
           'nicht von Hand ändern -->')
BIB_ZU = '<!-- CLIPS-BIBLIOTHEK:ENDE -->'
BIB = re.compile(re.escape(BIB_AUF) + r'.*?' + re.escape(BIB_ZU), re.DOTALL)

BIBLIOTHEK = "clips.html"
FAECHER = ["Grundlagenfach", "Schwerpunktfach"]


def lektionsseiten():
    """Code -> {nr, titel, url}, gelesen aus nav.js. Das ist die einzige
    Liste, die weiss, welche Lektion auf welcher Datei liegt."""
    quelle = open(os.path.join(WURZEL, "nav.js"), encoding="utf-8").read()
    treffer = re.findall(
        r"id:\s*'([^']+)'\s*,\s*nr:\s*'([^']*)'\s*,\s*titel:\s*'([^']*)'\s*,\s*url:\s*'([^']+)'",
        quelle)
    return {i: dict(nr=nr, titel=ti, url=u) for i, nr, ti, u in treffer}


def mmss(sekunden):
    return f"{int(sekunden) // 60}:{int(sekunden) % 60:02d}"


def codes(clip):
    v = clip.get("lektion") or []
    return [v] if isinstance(v, str) else list(v)


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


def karte(clip, vor):
    titel = html.escape(clip["titel"])
    return [
        f'<div class="clip" data-clip="{vor}clips/{clip["datei"]}" data-titel="{titel}">',
        '  <button class="clip-start" type="button" onclick="clipStart(this)">',
        '    <span class="clip-play" aria-hidden="true">▶</span>',
        '    <span>',
        f'      <span class="clip-titel">{titel} abspielen</span>',
        f'      <span class="clip-text">{html.escape(clip.get("kurzbeschrieb", ""))}</span>',
        f'      <span class="clip-meta">{mmss(clip.get("dauer_s", 0))} · CLIP</span>',
        '    </span>',
        '  </button>',
        '</div>',
    ]


def transkript_block(clip):
    tk = transkript(clip["datei"])
    if not tk:
        print(f"  [WARN] kein Sprechertext zu {clip['datei']}")
        return []
    aus = ['<details class="clip-transkript">',
           f'<summary>Transkript · {html.escape(clip["titel"])}</summary>', '<ol>']
    for zeit, txt in tk:
        aus.append(f'<li><span class="tk-zeit">{zeit}</span>'
                   f'<span>{html.escape(txt)}</span></li>')
    aus += ['</ol>', '</details>']
    return aus


def block_lektion(clips, tiefe):
    """Der Block auf einer Lektionsseite. tiefe = Ebenen unter der Wurzel."""
    vor = "../" * tiefe
    aus = [MARKE_AUF, '<h2 id="clips">Clips</h2>', '<div class="clip-grid">']
    for c in clips:
        aus += karte(c, vor) + transkript_block(c)
    aus += ['</div>', MARKE_ZU]
    return "\n".join(aus)


def block_bibliothek(alle, seiten):
    """clips.html — nach Fach, darin nach Lerngebiet, in der Reihenfolge
    der Startseite."""
    aus = [BIB_AUF]
    faecher = FAECHER + sorted({c.get("fach", "") for c in alle} - set(FAECHER) - {""})
    for fach in faecher:
        drin = [c for c in alle if c.get("fach") == fach]
        if not drin:
            continue
        anker = fach.lower().replace("ü", "ue")
        aus.append(f'<h2 id="{anker}">{html.escape(fach)}</h2>')
        for lg in sorted({c.get("lerngebiet", "") for c in drin}):
            aus.append(f'<h3 class="clip-lg">{html.escape(lg)}</h3>')
            aus.append('<div class="clip-grid">')
            for c in sorted((x for x in drin if x.get("lerngebiet") == lg),
                            key=lambda x: x["titel"]):
                aus += karte(c, "")
                verweise = []
                for code in codes(c):
                    s = seiten.get(code)
                    if s:
                        verweise.append(f'<a href="{s["url"]}">{s["nr"]} {html.escape(s["titel"])}</a>')
                if verweise:
                    aus.append('<p class="clip-lektionen">Im Zusammenhang: '
                               + ' · '.join(verweise) + '</p>')
                aus += transkript_block(c)
            aus.append('</div>')
    aus.append(BIB_ZU)
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
        for code in codes(c):
            if code not in seiten:
                print(f"  [FEHLER] {c['datei']}: Lektion '{code}' steht nicht in nav.js")
                continue
            nach_lektion.setdefault(code, []).append(c)

    aufgaben = []          # (pfad, neuer Text)
    gleich, ohne_marker = 0, []

    for code, clips in sorted(nach_lektion.items()):
        pfad = os.path.join(WURZEL, seiten[code]["url"])
        if not os.path.exists(pfad):
            print(f"  [FEHLER] {code}: {seiten[code]['url']} existiert nicht")
            continue
        text = open(pfad, encoding="utf-8").read()
        if not BLOCK.search(text):
            ohne_marker.append((code, seiten[code]["url"], len(clips)))
            continue
        tiefe = seiten[code]["url"].count("/")
        neu = BLOCK.sub(lambda _m: block_lektion(clips, tiefe), text, count=1)
        if neu == text:
            gleich += 1
        else:
            aufgaben.append((pfad, neu))

    bib = os.path.join(WURZEL, BIBLIOTHEK)
    if not os.path.exists(bib):
        print(f"  [WARN] {BIBLIOTHEK} fehlt — Bibliothek wird nicht geschrieben")
    else:
        text = open(bib, encoding="utf-8").read()
        if not BIB.search(text):
            print(f"  [WARN] {BIBLIOTHEK} hat keine CLIPS-BIBLIOTHEK-Marker")
        else:
            neu = BIB.sub(lambda _m: block_bibliothek(alle, seiten), text, count=1)
            if neu == text:
                gleich += 1
            else:
                aufgaben.append((bib, neu))

    print(f"{len(aufgaben)} Seiten zu aktualisieren, {gleich} bereits aktuell")
    for code, url, n in ohne_marker:
        print(f"  [WARN] {code} hat {n} Clip(s), aber keine CLIPS-Marker in {url}")
    for pfad, _ in aufgaben:
        print("   ", os.path.relpath(pfad, WURZEL))

    if not aufgaben:
        return
    if not a.schreiben:
        print("\nProbelauf. Mit --schreiben werden die Änderungen gespeichert.")
        return
    for pfad, neu in aufgaben:
        open(pfad, "w", encoding="utf-8").write(neu)
    print(f"\n{len(aufgaben)} Seiten geschrieben.")


if __name__ == "__main__":
    main()
