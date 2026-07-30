#!/usr/bin/env python3
"""Ordnet jedem Befund die fillText-Quellzeile zu, die ihn erzeugt."""
import json
import re
import sys
from collections import defaultdict

SC = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad'
bef = json.load(open(SC + '/audit-kandidaten.json'))

nur = sys.argv[1] if len(sys.argv) > 1 else None

pro = defaultdict(list)
for b in bef:
    pro[b['seite']].append(b)

for seite in sorted(pro):
    if nur and nur not in seite:
        continue
    zeilen = open(seite, encoding='utf-8').read().split('\n')
    # alle fillText/beschriftung-Aufrufe der Datei mit Zeilennummer
    aufrufe = []
    for i, z in enumerate(zeilen, 1):
        for m in re.finditer(r'(fillText|beschriftung)\s*\(', z):
            aufrufe.append((i, z.strip()))
    print(f'\n╔═ {seite}  ({len(aufrufe)} Textaufrufe)')
    for b in sorted(pro[seite], key=lambda x: (x['canvas'], x['art'])):
        txt = str(b['txt'])
        teile = [t.strip() for t in txt.split('⇄')] if '⇄' in txt else [txt]
        print(f"║ {b['canvas']:16s} {b['art']:14s} {txt[:38]!r:42s} {b['wert']}")
        for t in teile:
            # Literal-Treffer suchen; sonst nach markanten Teilstücken
            kern = re.sub(r'[-+0-9.\s|()]+', ' ', t).strip()
            kand = [(i, z) for i, z in aufrufe
                    if t and (f"'{t}'" in z or f'"{t}"' in z or (len(kern) > 2 and kern.split()[0] in z))]
            if not kand and len(t) <= 3:
                kand = [(i, z) for i, z in aufrufe if f"'{t}'" in z]
            for i, z in kand[:2]:
                print(f'║      → {seite}:{i}  {z[:104]}')
            if not kand:
                print(f'║      → (kein Literal gefunden — Variable oder Schleife)')
