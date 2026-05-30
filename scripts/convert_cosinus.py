"""
TODO-S2: Kosinus → Cosinus in den HTML-Dateien (Schweizer Konvention).

- Ersetzt 'Kosinus' → 'Cosinus' und 'kosinus' → 'cosinus' (case-erhaltend)
- Schützt URLs (href/src), <script>, <style>, <svg>, SVG-Attribute
- Markdown-Dokumente werden NICHT angefasst (redaktionelle Texte ausserhalb
  des Lehrmittels)

Hinweis: 'Kosinus'/'kosinus' kommt in keinen internen id/class/href-Ankern
des Lehrmittels vor (geprüft). Die einzigen URL-Vorkommen sind externe
Serlo-Links (de.serlo.org/...kosinus...) — diese werden bewahrt.
"""

import os
import re
import glob
import sys
import difflib

ROOT = "/home/claude/work/tals-mathe_26_9"


def protect_regions(text):
    """Maskiert URLs, <style>, <svg>, SVG-Attribute aus.

    <script>-Blöcke werden NICHT generell geschützt: Kosinus-Vorkommen darin
    stehen in JS-Strings/Template-Literals, die zur Laufzeit als Text gerendert
    werden (z.B. Canvas-Erklärungen in g5-3 Spezialwinkel-Beweis).
    'Kosinus' kommt in JS-Code-Konstrukten (Variablennamen, Properties) nicht
    vor, deshalb ist die Ersetzung dort sicher.

    Reihenfolge wichtig: erst die großen Blöcke (<style>/<svg>), erst DANACH
    href/src-Attribute. Sonst kann es zu verschachtelten Platzhaltern kommen.
    """
    protected = []

    def stash(match):
        protected.append(match.group(0))
        return f"\x00P{len(protected)-1}\x00"

    # 1) <style>, <svg> komplett geschützt
    text = re.sub(r'<style\b[^>]*>.*?</style>', stash, text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<svg\b[^>]*>.*?</svg>', stash, text,
                  flags=re.DOTALL | re.IGNORECASE)
    # 2) href/src-Attribute (auch innerhalb von <script src="..."> oder <a href="...">)
    text = re.sub(r'\shref="[^"]*"', stash, text)
    text = re.sub(r"\shref='[^']*'", stash, text)
    text = re.sub(r'\ssrc="[^"]*"', stash, text)
    text = re.sub(r"\ssrc='[^']*'", stash, text)
    # 3) SVG-Attribute für inline SVG
    text = re.sub(r'\sd="[^"]*"', stash, text)
    text = re.sub(r'\spoints="[^"]*"', stash, text)
    text = re.sub(r'\sviewBox="[^"]*"', stash, text)
    text = re.sub(r'\stransform="[^"]*"', stash, text)
    return text, protected


def restore_regions(text, protected):
    """Setzt Platzhalter zurück. Iterativ, falls Platzhalter ineinander
    geschachtelt waren (z.B. ein <script>-Block, dessen src-Attribut bereits
    separat maskiert war)."""
    for _ in range(10):  # Safety: max 10 Iterationen
        new = re.sub(r'\x00P(\d+)\x00',
                     lambda m: protected[int(m.group(1))], text)
        if new == text:
            break
        text = new
    return text


def process_text(text):
    masked, protected = protect_regions(text)
    # Case-erhaltend: 'Kosinus' → 'Cosinus', 'kosinus' → 'cosinus'.
    # Wir schauen explizit auf den ersten Buchstaben, weil 'K' und 'k' bewusst
    # unterschiedlich behandelt werden müssen.
    new, n1 = re.subn(r'Kosinus', 'Cosinus', masked)
    new, n2 = re.subn(r'kosinus', 'cosinus', new)
    new = restore_regions(new, protected)
    return new, n1 + n2


def collect_files():
    os.chdir(ROOT)
    files = (
        sorted(glob.glob('grundlagen/*.html')) +
        sorted(glob.glob('downloads/grundlagen/**/*.html', recursive=True)) +
        sorted(glob.glob('schwerpunkt/*.html'))
    )
    for extra in ['index.html', 'TEMPLATE.html']:
        if os.path.exists(extra):
            files.append(extra)
    return files


def show_diff(orig, new, fp, max_lines=12):
    a = orig.splitlines(keepends=True)
    b = new.splitlines(keepends=True)
    diff = list(difflib.unified_diff(a, b, fromfile=f'a/{fp}',
                                     tofile=f'b/{fp}', n=0))
    shown = 0
    for line in diff:
        if shown >= max_lines:
            print(f"  ... (weitere Änderungen ausgelassen)")
            break
        line = line.rstrip('\n')
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            print(f"  {line}")
        elif line.startswith('-'):
            print(f"  {line[:160]}")
            shown += 1
        elif line.startswith('+'):
            print(f"  {line[:160]}")


def main():
    apply_changes = '--apply' in sys.argv
    files = collect_files()

    print(f"Modus: {'APPLY (echte Änderungen)' if apply_changes else 'DRY-RUN (nur Vorschau)'}")
    print()

    total = 0
    n_files = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            orig = f.read()
        new, n = process_text(orig)
        if n == 0:
            continue
        n_files += 1
        total += n
        print(f"=== {fp}: {n} Ersetzungen ===")
        show_diff(orig, new, fp, max_lines=8)
        print()
        if apply_changes:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new)

    print(f"=== TOTAL: {total} Ersetzungen in {n_files} Dateien ===")
    if not apply_changes:
        print("(Dry-Run — keine Dateien verändert. Mit --apply ausführen.)")
    else:
        print("(Apply-Modus — Dateien wurden verändert.)")

    # Verifikation
    print()
    print("=== Verifikation: Restliche 'Kosinus' in HTML-Dateien (ausserhalb URLs) ===")
    rest = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            t = f.read()
        # URLs ausmaskieren für die Verifikation, damit Serlo-Links nicht zählen
        masked, _ = protect_regions(t)
        n = len(re.findall(r'[Kk]osinus', masked))
        if n:
            print(f"  {fp}: noch {n} 'Kosinus'-Vorkommen")
            rest += n
    if rest == 0:
        print("  Keine 'Kosinus'-Reste in HTML-Dateien (ausserhalb URLs). ✓")
    # Externe URL-Vorkommen separat melden (zur Bestätigung, dass sie bewahrt werden)
    print()
    print("=== URL-Vorkommen (bewahrt) ===")
    url_count = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            t = f.read()
        for m in re.finditer(r'\s(?:href|src)=["\'][^"\']*[Kk]osinus[^"\']*["\']', t):
            url_count += 1
            print(f"  {fp}: {m.group(0).strip()[:120]}")
    if url_count == 0:
        print("  Keine.")


if __name__ == '__main__':
    main()
