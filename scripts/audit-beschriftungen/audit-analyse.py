#!/usr/bin/env python3
"""Wertet audit-roh.json aus.

Entscheidend ist, was im ENDBILD steht. Darum:
  sichtbar = 1 - ueberzeichnet   (Anteil Glyphenpixel, der am Ende noch da ist)

Gemeldet wird nur, was am Ende auch zu sehen ist:
  A  ueberlappung  — zwei am Ende sichtbare Beschriftungen liegen übereinander
  B  auf-grafik    — eine sichtbare Beschriftung liegt auf einem Grafikelement
  C  rest          — eine Beschriftung ist fast, aber nicht ganz überdeckt;
                     der Rest bleibt als Artefakt stehen (typisch: der
                     mathlib-Trick „generisches x/y mit fillRect abdecken",
                     dessen Rechteck den Glyphen nicht ganz erwischt)
  D  abgeschnitten — das Textfeld reicht über den Canvasrand hinaus
"""
import json
import os

ROH = '/tmp/claude-1000/-home-paps-tals-mathe/cd6adf82-99f0-45f1-be4d-37f8d51362a9/scratchpad/audit-roh.json'
d = json.load(open(ROH))

SICHTBAR_MIN = 0.55    # darunter gilt die Beschriftung als (gewollt) überdeckt
REST_VON, REST_BIS = 0.03, 0.45   # sichtbarer Restanteil einer überdeckten Beschriftung
S_AUF_GRAFIK = 0.25
S_RAUS = 1.5
S_UEBERLAPP = 0.25


def flaeche(b):
    return max(0.0, b['x1'] - b['x0']) * max(0.0, b['y1'] - b['y0'])


def schnitt(a, b):
    w = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
    h = min(a['y1'], b['y1']) - max(a['y0'], b['y0'])
    return max(0.0, w) * max(0.0, h)


befunde = []
for p in d:
    seite = p['seite']
    for c in p.get('canvases', []):
        meta = p.get('meta', {}).get(c['id'], {})
        texte = [t for t in c['texte'] if not t.get('unlesbar')]
        for t in texte:
            t['sichtbar'] = 1.0 - t['ueberzeichnet']

        eintraege = []

        # ── A  Überlappung zweier am Ende sichtbarer Beschriftungen ──
        for i in range(len(texte)):
            for j in range(i + 1, len(texte)):
                a, b = texte[i], texte[j]
                if a['sichtbar'] < SICHTBAR_MIN or b['sichtbar'] < SICHTBAR_MIN:
                    continue      # eine der beiden ist am Ende weg -> gewollt überschrieben
                s = schnitt(a['b'], b['b'])
                if s <= 0:
                    continue
                kl = min(flaeche(a['b']), flaeche(b['b']))
                if kl > 0 and s / kl >= S_UEBERLAPP:
                    eintraege.append({'art': 'ueberlappung', 'wert': round(s / kl, 2),
                                      'txt': f"{a['txt']}  ⇄  {b['txt']}", 'b': None})

        for t in texte:
            # ── C  Rest einer fast vollständig überdeckten Beschriftung ──
            if REST_VON <= t['sichtbar'] <= REST_BIS:
                eintraege.append({'art': 'rest', 'wert': round(t['sichtbar'], 2),
                                  'txt': t['txt'], 'b': t['b']})
                continue
            if t['sichtbar'] < SICHTBAR_MIN:
                continue           # gewollt abgedeckt, im Endbild nicht zu sehen
            # ── B  sichtbare Beschriftung auf einem Grafikelement ──
            if t['aufGrafik'] >= S_AUF_GRAFIK:
                eintraege.append({'art': 'auf-grafik', 'wert': round(t['aufGrafik'], 2),
                                  'txt': t['txt'], 'b': t['b']})
            # ── D  über den Canvasrand hinaus ──
            r = t['raus']
            if any(r[k] > S_RAUS for k in ('links', 'oben', 'rechts', 'unten')):
                wo = ', '.join(f'{k} {r[k]:.0f}px' for k in ('links', 'oben', 'rechts', 'unten')
                               if r[k] > S_RAUS)
                eintraege.append({'art': 'abgeschnitten', 'wert': wo,
                                  'txt': t['txt'], 'b': t['b']})

        for e in eintraege:
            befunde.append({'seite': seite, 'canvas': c['id'], 'meta': meta,
                            'cv': [c['w'], c['h']], **e})

kanaele = {}
for b in befunde:
    kanaele.setdefault((b['seite'], b['canvas']), []).append(b)

print(f'{len(befunde)} Befunde auf {len(kanaele)} Canvas '
      f'({len(set(k[0] for k in kanaele))} Seiten)\n')
arten = {}
for b in befunde:
    arten[b['art']] = arten.get(b['art'], 0) + 1
print('nach Art:', arten, '\n')
for (seite, cv), bs in sorted(kanaele.items()):
    z = {}
    for b in bs:
        z[b['art']] = z.get(b['art'], 0) + 1
    print(f"{seite.split('/')[1][:46]:46s} {cv:18s} " + ', '.join(f'{k}×{v}' for k, v in sorted(z.items())))

json.dump(befunde, open(os.path.join(os.path.dirname(ROH), 'audit-kandidaten.json'), 'w'))
