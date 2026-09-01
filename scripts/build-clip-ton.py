#!/usr/bin/env python3
"""
Erzeugt die Tonspur zu einem Clip — lokal, offline, aus dem Sprechertext
des Drehbuchs.

Warum ueberhaupt: Die Szenendauer wird sonst aus der Wortzahl geschaetzt
(`Woerter / sprechtempo`). Mit echtem Ton ist das falsch. Dieses Skript
misst die tatsaechliche Laenge jeder Szene und schreibt sie als Feld
`dauer` ins Drehbuch zurueck — danach stimmt Bild zu Sprache exakt.

Ergebnis: **eine** MP3 je Clip, nicht eine je Szene. Der Clip synchronisiert
sie gegen seine eigene Uhr; mit einer einzigen Spur gibt es nichts zu
verketten und kein Stolpern an den Szenengrenzen. Die Sprache jeder Szene
sitzt an `Szenenstart + vorlauf`, dazwischen ist Stille.

    export PIPER_MODELL=/pfad/de_DE-thorsten-high.onnx
    python3 scripts/build-clip-ton.py g2-2a-parametergleichung-drei-faelle
    python3 scripts/build-clips.py    g2-2a-parametergleichung-drei-faelle

Der zweite Aufruf ist noetig: Dieses Skript aendert nur das Drehbuch und
legt die Tonspur ab, gebaut wird der Clip weiterhin von build-clips.py.

Voraussetzungen (nicht im Repo, bewusst):
  pip install piper-tts soundfile
  Stimme: rhasspy/piper-voices, de/de_DE/thorsten/high  (Datensatz CC0)
Lizenzlage in HOWTO-clips.md, Abschnitt «Ton».
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import OrderedDict

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")
TON = os.path.join(CLIPS, "ton")

sys.path.insert(0, os.path.join(WURZEL, "scripts"))


def lade_generator():
    """szenen_planen aus build-clips.py wiederverwenden statt nachbauen —
    sonst laufen die beiden Zeitrechnungen frueher oder spaeter auseinander."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "buildclips", os.path.join(WURZEL, "scripts", "build-clips.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sprich(piper, modell, text, ziel, tempo=None):
    """tempo = Phonemlaenge. Kleiner heisst schneller gesprochen; ohne
    Angabe gilt die Voreinstellung des Modells."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write(text)
        quelle = f.name
    befehl = piper + ["-m", modell, "-i", quelle, "-f", ziel]
    if tempo is not None:
        befehl += ["--length-scale", "%.4f" % tempo]
    try:
        r = subprocess.run(befehl, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"piper ist gescheitert:\n{r.stderr[-800:]}")
    finally:
        os.unlink(quelle)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", help="Drehbuch ohne .json")
    ap.add_argument("--modell", default=os.environ.get("PIPER_MODELL", ""),
                    help="Pfad zur .onnx-Stimme (oder Umgebung PIPER_MODELL)")
    ap.add_argument("--piper", default=os.environ.get("PIPER_CMD", "piper"),
                    help="Aufruf von piper (oder Umgebung PIPER_CMD)")
    ap.add_argument("--qualitaet", type=float, default=0.5,
                    help="MP3-Kompression 0.0 (gross) bis 1.0 (klein)")
    ap.add_argument("--zweitstimme", metavar="NAME",
                    help="zweite Spur <dateiname>-NAME.mp3 bauen, angepasst an "
                         "die erste: gleiche Satzdauern, gleiche Lautheit. "
                         "Das Drehbuch bleibt dabei unveraendert.")
    ap.add_argument("--modell2", default=os.environ.get("PIPER_MODELL2", ""),
                    help="Stimme fuer --zweitstimme (oder Umgebung PIPER_MODELL2)")
    a = ap.parse_args()

    if not a.modell or not os.path.exists(a.modell):
        sys.exit("Stimmmodell fehlt — --modell setzen oder PIPER_MODELL exportieren.")
    try:
        import numpy as np
        import soundfile as sf
    except ImportError as e:
        sys.exit(f"{e} — `pip install soundfile` fehlt.")

    pfad = os.path.join(CLIPS, a.clip.removesuffix(".json") + ".json")
    if not os.path.exists(pfad):
        sys.exit(f"Drehbuch nicht gefunden: {pfad}")
    dreh = json.load(open(pfad, encoding="utf-8"), object_pairs_hook=OrderedDict)
    bc = lade_generator()
    piper = a.piper.split()

    # ---- Schritt 1: sprechen und messen ------------------------------
    stuecke = {}
    with tempfile.TemporaryDirectory() as tmp:
        for i, sz in enumerate(dreh["szenen"]):
            text = (sz.get("sprecher") or "").strip()
            if not text:
                continue
            w = os.path.join(tmp, f"{i}.wav")
            sprich(piper, a.modell, text, w)
            daten, sr = sf.read(w, dtype="float32")

            if a.zweitstimme:
                # Die zweite Stimme muss in dieselbe Zeitspur passen: Das
                # Drehbuch und die Animation stehen schon. Also erst mit
                # Normaltempo messen, dann mit dem Faktor neu sprechen, der
                # den Satz genau so lang macht wie den der ersten Stimme.
                w2 = os.path.join(tmp, f"{i}-2.wav")
                sprich(piper, a.modell2, text, w2)
                probe, sr2 = sf.read(w2, dtype="float32")
                ziel_s = len(daten) / sr
                tempo = ziel_s / (len(probe) / sr2)
                # Zwei Durchgaenge: --length-scale streckt die Phoneme, nicht
                # die feste Satzpause davor und dahinter. Der erste Schuss
                # liegt darum um fuenf bis zehn Prozent daneben; der zweite
                # rechnet den Rest heraus.
                for _ in range(2):
                    sprich(piper, a.modell2, text, w2, tempo=tempo)
                    zweit, sr2 = sf.read(w2, dtype="float32")
                    ist = len(zweit) / sr2
                    if abs(ist - ziel_s) < 0.05:
                        break
                    tempo *= ziel_s / ist
                print(f"  Szene {i+1}: {ziel_s:6.2f} s   Tempo {tempo:.3f}"
                      f"  →  {len(zweit)/sr2:5.2f} s  ({len(zweit)/sr2-ziel_s:+.2f})"
                      f"   {text[:32]}")
                stuecke[i] = (zweit, sr2)
                continue

            stuecke[i] = (daten, sr)
            print(f"  Szene {i+1}: {len(daten)/sr:6.2f} s   {text[:52]}")

        if not stuecke:
            sys.exit("Keine sprecher-Texte im Drehbuch.")
        rate = stuecke[next(iter(stuecke))][1]

        # ---- Schritt 2: gemessene Dauer ins Drehbuch ------------------
        vorlauf = bc.STD["vorlauf"]
        takt = dreh.get("takt", bc.STD["takt"])
        nachlauf = dreh.get("nachlauf", bc.STD["nachlauf"])
        for i, sz in enumerate(dreh["szenen"]):
            if a.zweitstimme:
                break            # die Zeitspur gehoert der ersten Stimme
            letzte = max([el.get("ein", vorlauf + k * takt)
                          for k, el in enumerate(sz.get("elemente", []))] or [0.0])
            noetig = letzte + nachlauf
            if i in stuecke:
                daten, sr = stuecke[i]
                noetig = max(noetig, vorlauf + len(daten) / sr + 0.8)
            sz["dauer"] = round(max(noetig, 3.0), 2)
        if not a.zweitstimme:
            json.dump(dreh, open(pfad, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)

        # ---- Schritt 3: eine Spur, Sprache an die Szenenstarts --------
        plan, gesamt = bc.szenen_planen(dreh)
        spur = np.zeros(int(round(gesamt * rate)) + rate, dtype="float32")
        for i, p in enumerate(plan):
            if i not in stuecke:
                continue
            daten, _ = stuecke[i]
            ab = int(round((p["start"] + vorlauf) * rate))
            spur[ab:ab + len(daten)] += daten

        # Lautheit: Zwei Stimmen mit gleicher Spitze klingen nicht gleich
        # laut — dafuer zaehlt der Effektivwert. Die zweite Spur wird auf
        # den der ersten gezogen, damit das Umschalten nicht auffaellt.
        if a.zweitstimme:
            erste = os.path.join(TON, dreh["dateiname"] + ".mp3")
            if os.path.exists(erste):
                ref, _ = sf.read(erste, dtype="float32", always_2d=False)
                if ref.ndim > 1:
                    ref = ref.mean(axis=1)
                laut = lambda y: float(np.sqrt(np.mean(y[np.abs(y) > 0.01] ** 2))) if (np.abs(y) > 0.01).any() else 0.0
                z, r = laut(spur), laut(ref)
                if z > 0 and r > 0:
                    print(f"  Lautheit {20*np.log10(z/r):+.1f} dB gegenueber der ersten "
                          f"Spur — angeglichen.")
                    spur *= r / z
            else:
                print("  [WARN] erste Spur fehlt — keine Lautheitsangleichung.")

        # Kopfraum: Piper steuert einzelne Saetze bis an die Grenze aus,
        # und der MP3-Encoder ueberschwingt leicht. Ohne das zerrt es.
        spitze = float(np.abs(spur).max())
        if spitze > 0.95:
            spur *= 0.95 / spitze

        os.makedirs(TON, exist_ok=True)
        ziel = os.path.join(TON, dreh["dateiname"]
                            + (("-" + a.zweitstimme) if a.zweitstimme else "") + ".mp3")
        sf.write(ziel, spur[:int(round(gesamt * rate))], rate,
                 format="MP3", compression_level=a.qualitaet)

    kb = os.path.getsize(ziel) / 1024
    print(f"\n  {os.path.relpath(ziel, WURZEL)}  —  {gesamt:.1f} s, {kb:.0f} kB")
    if a.zweitstimme:
        print(f"  Zweite Spur — Drehbuch unveraendert. Jetzt: "
              f"python3 scripts/build-clips.py {dreh['dateiname']}")
    else:
        print(f"  Dauern im Drehbuch aktualisiert. Jetzt: "
              f"python3 scripts/build-clips.py {dreh['dateiname']}")


if __name__ == "__main__":
    main()
