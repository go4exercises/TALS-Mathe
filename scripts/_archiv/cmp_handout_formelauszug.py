"""Vergleicht Handout vs. Formelauszug für alle Themen.
Berechnet zwei Metriken:
1. Token-Jaccard (auf normalisierten Wörtern + LaTeX-Formeln) — wie viel inhaltliche Substanz teilen sich die beiden
2. Anteil "Handout in Formelauszug enthalten" (Asymmetrie: was im Handout steht, taucht auch im Formelauszug auf?) — und vice versa
"""
import re
from pathlib import Path

import os

# Repo-Root: Elternverzeichnis von scripts/, überschreibbar via Umgebungsvariable TALS_ROOT
ROOT = Path(os.environ.get("TALS_ROOT") or Path(__file__).resolve().parent.parent) / "downloads" / "grundlagen"

def extract_content(html_path: Path) -> str:
    """Extrahiere den Inhalts-Bereich (zwischen druck-wrapper / druck-bar) als plain text."""
    txt = html_path.read_text(encoding="utf-8")
    # Body herauslösen
    m = re.search(r'<div class="druck-wrapper">(.*?)</div>\s*</body>', txt, re.S)
    body = m.group(1) if m else txt
    # MathJax-Skripte/Style entfernen
    body = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S)
    # HTML-Tags raus, aber LaTeX-Inhalte erhalten (\( ... \), \[ ... \])
    # Erst LaTeX-Blöcke markieren
    body = re.sub(r'\\\((.*?)\\\)', lambda m: ' MATH_' + m.group(1).strip() + '_MATH ', body, flags=re.S)
    body = re.sub(r'\\\[(.*?)\\\]', lambda m: ' MATH_' + m.group(1).strip() + '_MATH ', body, flags=re.S)
    # HTML-Tags raus
    body = re.sub(r'<[^>]+>', ' ', body)
    # HTML-Entities
    body = body.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    # Normalisieren
    body = body.lower()
    return body

def tokenize(text: str) -> set[str]:
    """Tokens als Set: Wörter und Mathe-Formeln."""
    tokens = set()
    # Mathe-Tokens — kompakte Formel-Strings
    for m in re.finditer(r'MATH_(.*?)_MATH', text):
        formel = m.group(1)
        # Whitespace und Klammern normalisieren
        formel = re.sub(r'\s+', '', formel)
        formel = formel.replace('{', '').replace('}', '').replace('\\,', '').replace('\\;', '')
        if len(formel) >= 2:
            tokens.add('MATH:' + formel)
    # Text ohne MATH_-Marker für Wörter
    text_no_math = re.sub(r'MATH_.*?_MATH', ' ', text)
    for w in re.findall(r'[a-zäöüß]+', text_no_math):
        if len(w) >= 3:  # Stoppwörter unter 3 Zeichen weg
            tokens.add(w)
    return tokens

# Themen ermitteln
themen = []
for p in sorted(ROOT.glob("g*-*/handout.html")):
    fa = p.parent / "formelauszug.html"
    if fa.exists():
        themen.append((p.parent.name, p, fa))

print(f"{'Thema':<48} {'|H|':>5} {'|F|':>5} {'∩':>5} {'Jac%':>6} {'H⊂F%':>6} {'F⊂H%':>6}")
print("-" * 90)

result = []
for name, h_path, f_path in themen:
    h_text = extract_content(h_path)
    f_text = extract_content(f_path)
    h_tok = tokenize(h_text)
    f_tok = tokenize(f_text)
    common = h_tok & f_tok
    union = h_tok | f_tok
    jac = len(common) / len(union) * 100 if union else 0
    hSubF = len(common) / len(h_tok) * 100 if h_tok else 0
    fSubH = len(common) / len(f_tok) * 100 if f_tok else 0
    print(f"{name:<48} {len(h_tok):>5} {len(f_tok):>5} {len(common):>5} {jac:>6.1f} {hSubF:>6.1f} {fSubH:>6.1f}")
    result.append((name, len(h_tok), len(f_tok), len(common), jac, hSubF, fSubH))

# Mittelwerte
if result:
    n = len(result)
    print("-" * 90)
    avg_jac = sum(r[4] for r in result) / n
    avg_hSubF = sum(r[5] for r in result) / n
    avg_fSubH = sum(r[6] for r in result) / n
    print(f"{'⌀ Durchschnitt':<48} {'':>5} {'':>5} {'':>5} {avg_jac:>6.1f} {avg_hSubF:>6.1f} {avg_fSubH:>6.1f}")

# Klassifikation
print()
print("Legende:")
print("  |H|/|F|  Anzahl Tokens (Wörter ≥3 Zeichen + Mathe-Formeln) im Handout / Formelauszug")
print("  ∩        gemeinsame Tokens")
print("  Jac%     Jaccard-Index: ∩/(H∪F) — symmetrische Überlappung")
print("  H⊂F%     Anteil der Handout-Tokens, die auch im Formelauszug stehen")
print("  F⊂H%     Anteil der Formelauszug-Tokens, die auch im Handout stehen")
