"""Vertont nur einzelne Szenen oder Fragetöne eines Clips neu (Prüfung 08.10.2026).

  python3 scripts/lp/einheitskreis/teilton.py szenen <clip> "<Szene>" …   # Szenen der Haupttonspur
  python3 scripts/lp/einheitskreis/teilton.py fragen <clip> <i>[:<schl>] …  # Fragetöne (i ab 0, schl wie r1, fall2)

Warum: build-clip-ton.py spricht jeden Clip ganz neu, und Piper klingt bei jedem Lauf ein wenig anders. Nach einer
Korrektur an einer Szene sollen die übrigen genau so bleiben, wie der Auftraggeber sie gehört hat. Dieses Skript

  * schneidet die unveränderten Szenen aus der bisherigen Tonspur clips/ton/<clip>.mp3 (Lage aus dem Drehbuch im
    letzten Commit, git show HEAD:…, mit szenen_planen() aus build-clips.py),
  * spricht nur die genannten Szenen mit sprich() und aussprache() aus build-clip-ton.py neu,
  * rechnet `dauer` wie build-clip-ton.py und legt alles in eine neue Spur.

Fragetöne: Nur die genannten Dateien clips/ton/<clip>-f<i>-<schl>.mp3; ohne :schl alle Töne der Frage i (alte
Dateien dieser Frage werden vorher entfernt). Danach wie immer: wortzeiten.py, clips.py, build-clips.py.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
TON = R + 'clips/ton/'


def lade(datei, name):
    spec = importlib.util.spec_from_file_location(name, R + 'scripts/' + datei)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bc = lade('build-clips.py', 'buildclips')
ton = lade('build-clip-ton.py', 'clipton')
MODELL = os.environ.get('PIPER_MODELL', '')
PIPER = os.environ.get('PIPER_CMD', 'piper').split()
if not MODELL or not os.path.exists(MODELL):
    sys.exit('Stimmmodell fehlt — PIPER_MODELL exportieren.')


def sprechen(text):
    with tempfile.TemporaryDirectory() as tmp:
        w = os.path.join(tmp, 's.wav')
        ton.sprich(PIPER, MODELL, ton.aussprache(text), w)
        return sf.read(w, dtype='float32')


def szenen(clip, namen):
    pfad = R + 'clips/' + clip + '.json'
    dreh = json.load(open(pfad, encoding='utf-8'))
    alt = json.loads(subprocess.run(['git', 'show', 'HEAD:clips/' + clip + '.json'], cwd=R, capture_output=True,
                                    text=True, check=True).stdout)
    spur_alt, rate = sf.read(TON + clip + '.mp3', dtype='float32')
    if spur_alt.ndim > 1:
        spur_alt = spur_alt.mean(1)
    plan_alt, _ = bc.szenen_planen(alt)
    vorlauf = bc.STD['vorlauf']
    alt_je = {(p['sz']['name'], p['sz'].get('sprecher', '')): p for p in plan_alt}
    stuecke = {}
    for i, sz in enumerate(dreh['szenen']):
        text = (sz.get('sprecher') or '').strip()
        if not text:
            continue
        if sz['name'] in namen:
            daten, sr = sprechen(text)
            assert sr == rate, (sr, rate)
            print('  neu   %-22s %6.2f s  %s' % (sz['name'], len(daten) / sr, text[:50]))
        else:
            p = alt_je.get((sz['name'], text))
            if p is None:
                sys.exit('Szene «%s» hat neuen Text, steht aber nicht in der Liste.' % sz['name'])
            a, e = int(round((p['start'] + vorlauf) * rate)), int(round((p['start'] + p['dauer']) * rate))
            daten = spur_alt[a:e].copy()
            # Stille am Ende abschneiden (wie ein frisch gesprochenes Stück)
            laut = np.nonzero(np.abs(daten) > 1e-3)[0]
            daten = daten[:laut[-1] + int(0.05 * rate)] if len(laut) else daten[:0]
            print('  alt   %-22s %6.2f s' % (sz['name'], len(daten) / rate))
        stuecke[i] = daten
    takt = dreh.get('takt', bc.STD['takt'])
    nachlauf = dreh.get('nachlauf', bc.STD['nachlauf'])
    for i, sz in enumerate(dreh['szenen']):
        letzte = max([el.get('ein', vorlauf + k * takt) for k, el in enumerate(sz.get('elemente', []))] or [0.0])
        noetig = letzte + nachlauf
        if sz['name'] in namen and i in stuecke:
            noetig = max(noetig, vorlauf + len(stuecke[i]) / rate + 0.8)
            sz['dauer'] = round(max(noetig, 3.0), 2)
        elif 'dauer' not in sz:
            sys.exit('Szene «%s» ohne dauer.' % sz['name'])
    json.dump(dreh, open(pfad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    plan, gesamt = bc.szenen_planen(dreh)
    spur = np.zeros(int(round(gesamt * rate)) + rate, dtype='float32')
    for i, p in enumerate(plan):
        if i in stuecke:
            ab = int(round((p['start'] + vorlauf) * rate))
            spur[ab:ab + len(stuecke[i])] += stuecke[i]
    spitze = float(np.abs(spur).max())
    if spitze > 0.95:
        spur *= 0.95 / spitze
    sf.write(TON + clip + '.mp3', spur[:int(round(gesamt * rate))], rate, format='MP3', compression_level=0.5)
    print('  %s.mp3 — %.1f s' % (clip, gesamt))


def fragen(clip, angaben):
    dreh = json.load(open(R + 'clips/' + clip + '.json', encoding='utf-8'))
    for ang in angaben:
        i, _, schl = ang.partition(':')
        i = int(i)
        F = dreh['fragen'][i]
        if not schl:
            for f in os.listdir(TON):
                if f.startswith('%s-f%d-' % (clip, i)) and f.endswith('.mp3'):
                    os.remove(TON + f)
        for k, _, gesprochen in bc.fragen_texte(F):
            if schl and k != schl:
                continue
            daten, rate = sprechen(gesprochen)
            spitze = float(np.abs(daten).max()) if len(daten) else 0
            if spitze > 0.95:
                daten *= 0.95 / spitze
            sf.write(TON + bc.fragen_tondatei(dreh['dateiname'], i, k), daten, rate, format='MP3', compression_level=0.5)
            print('  Frage %d %-7s %5.1f s  %s' % (i + 1, k, len(daten) / rate, gesprochen[:60]))


if __name__ == '__main__':
    art, clip, *rest = sys.argv[1:]
    {'szenen': szenen, 'fragen': fragen}[art](clip, rest)
