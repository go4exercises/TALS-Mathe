"""
TODO-S4: Punkt-Koordinaten (x, y) → (x | y) in den 11 identifizierten Stellen.

Gemäss STYLEGUIDE §2.4 wird die Punkt-Notation `P(x \\mid y)` mit senkrechtem
Strich verwendet — FTB-Standard der Schweizer BM.

Vorgehen: Statt globaler Regex werden gezielte string-Ersetzungen pro
identifizierter Stelle durchgeführt. Das vermeidet Falsch-Positiva in
Datenwert-Aufzählungen (z.B. Statistik-Klassenhäufigkeiten "2 Werte
(158, 162)" in g4-2 aufgabenserie — diese bleiben unangetastet).

Identifizierte echte Punkt-Koordinaten (alle in g5-2d):
- grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html (1 Stelle, 9 Paare)
- downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/teste-dich-selbst.html (1 Stelle, 2 Paare)
"""

import os
import sys

# Repo-Root: Elternverzeichnis von scripts/, überschreibbar via Umgebungsvariable TALS_ROOT
ROOT = os.environ.get("TALS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Liste von (Datei, alt, neu)-Tripeln.
# Jede Stelle wird einzeln verifiziert und ersetzt.
REPLACEMENTS = [
    # --- grundlagen/g5-2d (Themenseite, Lösung zentrische Streckung mit k=2) ---
    (
        'grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html',
        "\\(A' = 2(0,0) - (1,1) = (-1, -1)\\), \\(B' = 2(6,0) - (1,1) = (11, -1)\\), \\(C' = 2(2,4) - (1,1) = (3, 7)\\)",
        "\\(A' = 2(0|0) - (1|1) = (-1|-1)\\), \\(B' = 2(6|0) - (1|1) = (11|-1)\\), \\(C' = 2(2|4) - (1|1) = (3|7)\\)"
    ),
    # --- downloads g5-2d teste-dich-selbst (Lösung Bildpunkt P' = -2·P) ---
    (
        'downloads/grundlagen/g5-2d-zentrische-streckung-aehnlichkeit/teste-dich-selbst.html',
        "\\(P' = k \\cdot P = -2 \\cdot (3, 4) = (-6, -8)\\)",
        "\\(P' = k \\cdot P = -2 \\cdot (3|4) = (-6|-8)\\)"
    ),
]


def main():
    apply_changes = '--apply' in sys.argv
    print(f"Modus: {'APPLY' if apply_changes else 'DRY-RUN'}\n")

    n_ok = 0
    n_fail = 0
    for fp, old, new in REPLACEMENTS:
        path = os.path.join(ROOT, fp)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        cnt = content.count(old)
        print(f"=== {fp} ===")
        print(f"  alt: {old}")
        print(f"  neu: {new}")
        if cnt == 0:
            print(f"  ⚠ ALT-String nicht gefunden!")
            n_fail += 1
        elif cnt > 1:
            print(f"  ⚠ ALT-String {cnt}× gefunden (Mehrdeutigkeit)")
            n_fail += 1
        else:
            print(f"  ✓ ALT-String genau 1× gefunden")
            n_ok += 1
            if apply_changes:
                new_content = content.replace(old, new)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  → geschrieben")
        print()

    print(f"=== {n_ok} Ersetzungen vorbereitet, {n_fail} Probleme ===")
    if not apply_changes:
        print("(Dry-Run — keine Dateien verändert. Mit --apply ausführen.)")

    # Verifikation
    if apply_changes and n_fail == 0:
        print()
        print("=== Verifikation ===")
        for fp, _, _ in REPLACEMENTS:
            path = os.path.join(ROOT, fp)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Sicherstellen, dass keine Stray-Steuerzeichen
            assert '\x00' not in content, f"STRAY in {fp}"
            assert '\x01' not in content, f"STRAY in {fp}"
        print("Keine Stray-Steuerzeichen ✓")


if __name__ == '__main__':
    main()
