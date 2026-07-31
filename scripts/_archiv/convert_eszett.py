"""
TODO-S1: ß → ss in den HTML-Dateien (Variante A — auch Eigennamen wie Gauß → Gauss).

Geltungsbereich (gemäss S1-Befund):
- alle HTML-Lehrmittel-Dateien (grundlagen/, downloads/, schwerpunkt/, index, TEMPLATE)
- KEINE Markdown-Dateien (CHANGELOG.md, STYLEGUIDE.md etc.) — das sind redaktionelle
  Texte ausserhalb des Lehrmittels selbst.

Schutz: ß-Vorkommen in <script>, <style>, <svg>, SVG-Attributen werden NICHT angefasst.
(Sehr unwahrscheinlich, dass dort ß steht, aber sicher ist sicher.)
"""

import os
import re
import glob
import sys
import difflib

# Repo-Root: Elternverzeichnis von scripts/, überschreibbar via Umgebungsvariable TALS_ROOT
ROOT = os.environ.get("TALS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def protect_regions(text):
    """Maskiert <style>, <svg>, SVG-Attribute aus.

    <script> wird hier NICHT maskiert: Die ß-Vorkommen in <script>-Blöcken
    stehen in JS-Strings, die zur Laufzeit als Text angezeigt werden (z.B.
    Canvas-Erklärungstexte in g5-2a wie 'Das blaue Dreieck ist halb so groß
    wie ...'). ß kommt in JS-Code selbst (Variablennamen, Properties,
    Schlüsselwörtern) nicht vor, deshalb ist die Ersetzung dort sicher.
    """
    protected = []

    def stash(match):
        protected.append(match.group(0))
        return f"\x00P{len(protected)-1}\x00"

    text = re.sub(r'<style\b[^>]*>.*?</style>', stash, text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<svg\b[^>]*>.*?</svg>', stash, text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\sd="[^"]*"', stash, text)
    text = re.sub(r'\spoints="[^"]*"', stash, text)
    text = re.sub(r'\sviewBox="[^"]*"', stash, text)
    text = re.sub(r'\stransform="[^"]*"', stash, text)
    return text, protected


def restore_regions(text, protected):
    def fn(m):
        return protected[int(m.group(1))]
    return re.sub(r'\x00P(\d+)\x00', fn, text)


def process_text(text):
    masked, protected = protect_regions(text)
    new, n = re.subn(r'ß', 'ss', masked)
    new = restore_regions(new, protected)
    return new, n


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


def show_diff(orig, new, fp, max_lines=10):
    """Zeigt unified diff zwischen orig und new."""
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
            print(f"  {line[:140]}")
            shown += 1
        elif line.startswith('+'):
            print(f"  {line[:140]}")


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
        show_diff(orig, new, fp, max_lines=12)
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
    print("=== Verifikation: Restliche ß-Vorkommen in HTML-Dateien ===")
    rest = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            t = f.read()
        n = t.count('ß')
        if n:
            print(f"  {fp}: noch {n} ß-Vorkommen")
            rest += n
    if rest == 0:
        print("  Keine ß-Reste in HTML-Dateien. ✓")


if __name__ == '__main__':
    main()
