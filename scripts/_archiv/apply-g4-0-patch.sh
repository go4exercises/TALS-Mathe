#!/usr/bin/env bash
# Portiert die g4-0-Praxisbeispiel-Erweiterung in einen Repo-Stand,
# der die anderen Themenseiten weiterentwickelt hat.
#
# Erwartet:
#   - Ausführung im Repo-Root (wo nav.js, index.html, grundlagen/ liegen)
#   - $1 = Pfad zum entpackten g4-0-ZIP (oder weglassen für "./_g4-0-patch")
#
# Verwendung:
#   ./apply-g4-0-patch.sh /pfad/zum/entpackten/zip
#
# Das Skript:
#   1. kopiert die neue Datei grundlagen/g4-0-praxisbeispiel-bm2-klasse.html
#   2. patcht nav.js (2 Stellen)
#   3. patcht index.html (Karte + Teilgebiete-Text)
#   4. patcht g3-3.next und g4-1.prev
# Idempotent: mehrfaches Ausführen schadet nicht.

set -euo pipefail

PATCH_SRC="${1:-./_g4-0-patch}"

# === Sanity-Checks ===
[ -d "$PATCH_SRC" ] || { echo "FEHLER: Quellverzeichnis $PATCH_SRC existiert nicht." >&2; exit 1; }
[ -f "nav.js" ] || { echo "FEHLER: Bitte im Repo-Root ausführen (nav.js nicht gefunden)." >&2; exit 1; }
[ -f "$PATCH_SRC/grundlagen/g4-0-praxisbeispiel-bm2-klasse.html" ] || \
  { echo "FEHLER: g4-0-Datei nicht in $PATCH_SRC/grundlagen/ gefunden." >&2; exit 1; }

# === 1. g4-0 kopieren ===
echo "1. Kopiere g4-0-praxisbeispiel-bm2-klasse.html …"
cp "$PATCH_SRC/grundlagen/g4-0-praxisbeispiel-bm2-klasse.html" grundlagen/

# === 2. nav.js patchen ===
echo "2. Patche nav.js …"
# 2a) g4-0 in SITE eintragen (idempotent)
if ! grep -q "id:'g4-0'" nav.js; then
  python3 - <<'PY'
import re
with open('nav.js') as f: s = f.read()
needle = "{ id:'g4-1', nr:'4.1', titel:'Grundlagen', url:'grundlagen/g4-1-grundlagen.html' },"
add    = "{ id:'g4-0', nr:'4.0', titel:'Praxisbeispiel BM2-Klasse', url:'grundlagen/g4-0-praxisbeispiel-bm2-klasse.html' },\n    "
assert needle in s, "nav.js: g4-1-Eintrag nicht gefunden (Stand hat sich geändert?)"
s = s.replace(needle, add + needle, 1)
with open('nav.js','w') as f: f.write(s)
PY
fi
# 2b) GROUPS-Eintrag erweitern (idempotent)
if ! grep -q "ids:\['g4-0'" nav.js; then
  python3 - <<'PY'
import re
with open('nav.js') as f: s = f.read()
old = "{ nr:'4', titel:'Datenanalyse', ids:['g4-1', 'g4-2', 'g4-3'] }"
new = "{ nr:'4', titel:'Datenanalyse', ids:['g4-0', 'g4-1', 'g4-2', 'g4-3'] }"
assert old in s, "nav.js: GROUPS-Eintrag für Datenanalyse nicht im erwarteten Format"
s = s.replace(old, new, 1)
with open('nav.js','w') as f: f.write(s)
PY
fi

# === 3. index.html patchen ===
echo "3. Patche index.html …"
if ! grep -q "g4-0-praxisbeispiel-bm2-klasse" index.html; then
  python3 - <<'PY'
import re
with open('index.html') as f: s = f.read()
# Teilgebiete-Text
s = s.replace(
  '<span class="k-lek">20 Lektionen · 3 Teilgebiete</span>',
  '<span class="k-lek">20 Lektionen · 3 Teilgebiete + Praxisbeispiel</span>',
  1
)
# 4.0-Karte vor der 4.1-Karte einfügen
needle = '      <a href="grundlagen/g4-1-grundlagen.html" class="karte fertig">\n        <span class="k-id">4.1</span>'
karte_4_0 = '''      <a href="grundlagen/g4-0-praxisbeispiel-bm2-klasse.html" class="karte fertig">
        <span class="k-id">4.0</span>
        <span class="k-tit">Praxisbeispiel BM2-Klasse</span>
      </a>

      <a href="grundlagen/g4-1-grundlagen.html" class="karte fertig">
        <span class="k-id">4.1</span>'''
if needle in s:
    s = s.replace(needle, karte_4_0, 1)
else:
    print("WARNUNG: index.html — 4.1-Karten-Anker nicht im erwarteten Format. Bitte manuell prüfen.")
with open('index.html','w') as f: f.write(s)
PY
fi

# === 4. g3-3 next: patchen ===
echo "4. Patche g3-3 (next:) …"
G33="grundlagen/g3-3-quadratische-funktionen.html"
if [ -f "$G33" ] && ! grep -q "next:{nr:'4.0'" "$G33"; then
  python3 - <<PY
with open("$G33") as f: s = f.read()
old = "next:{nr:'4.1',titel:'Grundlagen',url:'g4-1-grundlagen.html'}"
new = "next:{nr:'4.0',titel:'Praxisbeispiel BM2-Klasse',url:'g4-0-praxisbeispiel-bm2-klasse.html'}"
if old in s:
    s = s.replace(old, new, 1)
    with open("$G33",'w') as f: f.write(s)
else:
    print("WARNUNG: g3-3 — next:-Eintrag nicht im erwarteten Format. Bitte manuell prüfen.")
PY
fi

# === 5. g4-1 prev: patchen ===
echo "5. Patche g4-1 (prev:) …"
G41="grundlagen/g4-1-grundlagen.html"
if [ -f "$G41" ] && ! grep -q "prev:{nr:'4.0'" "$G41"; then
  python3 - <<PY
with open("$G41") as f: s = f.read()
old = "prev:{nr:'3.3',titel:'Quadratische Funktionen',url:'g3-3-quadratische-funktionen.html'},"
new = "prev:{nr:'4.0',titel:'Praxisbeispiel BM2-Klasse',url:'g4-0-praxisbeispiel-bm2-klasse.html'},"
if old in s:
    s = s.replace(old, new, 1)
    with open("$G41",'w') as f: f.write(s)
else:
    print("WARNUNG: g4-1 — prev:-Eintrag nicht im erwarteten Format. Bitte manuell prüfen.")
PY
fi

# === 6. Pre-Flight ===
echo ""
echo "6. Pre-Flight auf alle drei betroffenen Themenseiten:"
for f in grundlagen/g4-0-praxisbeispiel-bm2-klasse.html grundlagen/g3-3-quadratische-funktionen.html grundlagen/g4-1-grundlagen.html; do
  [ -f "$f" ] || continue
  pw=$(grep -c "page-wrap" "$f")
  mc=$(grep -c 'main class="content"' "$f")
  nav=$(grep -c 'src="../nav.js">' "$f")
  ml=$(grep -c 'src="../mathlib.js"' "$f")
  bn=$(grep -cE 'buildNav\(\{[[:space:]]*$|buildNav\(\{ bereich' "$f")
  printf "   %-60s pw=%s mc=%s nav=%s ml=%s bn=%s\n" "$(basename $f)" "$pw" "$mc" "$nav" "$ml" "$bn"
done

echo ""
echo "Fertig. Bitte im Browser testen: index.html und grundlagen/g4-0-praxisbeispiel-bm2-klasse.html."
