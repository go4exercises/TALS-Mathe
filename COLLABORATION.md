# Arbeitsweise mit Claude — TALS-Mathematik-Projekt

**Version 1.6 · Stand: 17. Mai 2026**

> **Adressat:** Claude (in jedem Chat dieses Projekts) — und der Auftraggeber (zum Nachlesen, was Claude kennt).
> **Diese Datei gehört ins Project-Knowledge, NICHT ins GitHub-Repo.** Sie ist Meta-Information über die Zusammenarbeit, nicht Teil des Lehrmittels.

---

## 1. Verhältnis zu anderen Konventions-Dokumenten

Es gibt zwei Konventions-Dokumente. Sie haben verschiedene Adressaten und werden nicht vermischt:

| Datei | Liegt in | Adressat | Inhalt |
|---|---|---|---|
| `STYLEGUIDE.md` | Repo + (Kopie im) Project-Knowledge | Wer Themenseiten baut (Mensch oder Claude) | Inhaltlich-redaktionelle Konventionen: Notation, Aufbau, Design |
| `COLLABORATION.md` | Nur Project-Knowledge | Claude und Auftraggeber | Wie wir effizient zusammenarbeiten |

**Wahrheits-Quelle:** Bei `STYLEGUIDE.md` ist das Repo die Wahrheit. Die Project-Knowledge-Kopie ist eine Arbeitskopie, die nach Updates im Repo manuell synchron gehalten wird.

---

## 2. Iterationsmodus (Standard-Workflow)

Eine typische Arbeitseinheit läuft so ab:

```
[Auftraggeber]                          [Claude]
─────────────                           ────────
1. ZIP des aktuellen Stands hochladen
   + alle gewünschten Änderungen
   in EINER Nachricht                →
                                      2. Klärungsfragen falls nötig
                                         (max. 1–3 Stück, gebündelt)
3. Antworten auf Fragen             →
                                      4. Plan kurz skizzieren
                                         (was, wo, wie viele Stellen)
                                      5. Umsetzung in einem Rutsch
                                      6. Sanity-Check (grep statt view)
                                      7. ZIP packen + present_files
                                      8. Kurze Zusammenfassung der Patches
9. Testen, ggf. Folge-Iteration     ↻
```

**Was vermieden wird:** „mach X" → Output → „passt, jetzt Y" → Output → „und noch Z" → Output. Jeder Hin-und-Her-Zyklus kostet Inspektions-Tool-Aufrufe für State-Wiederherstellung. Lieber alle Änderungen vorne sammeln.

---

## 3. Effizienz-Regeln für Claude

Diese Regeln helfen, im Tool-Budget eines Chats zu bleiben.

### 3.1 Mehrere ähnliche Edits → ein Skript, nicht N str_replace

Wenn mehr als 3 Stellen nach demselben Muster geändert werden (z.B. „alle `2x` → `2·x`"), nutze ich `sed`, `python -c …` oder ein kleines Skript via `bash_tool`. Ein Tool-Aufruf statt zehn.

**Beispiel:**
```bash
# Statt 6× str_replace für A3a–f Display-Strings:
sed -i "s/'\\([0-9.-]*\\)x\\([+-][0-9.]*\\)'/'\\1·x\\2'/g" datei.html
```

**Wann doch str_replace:** wenn die Stelle wirklich einzigartig ist und das Ersatz-Pattern komplex (Block-Edits mit mehreren Zeilen).

### 3.2 grep vor view

Wenn ich gezielt eine bekannte Stelle suche, ist `grep -n "muster" datei` einem `view` mit grossem Bereich vorzuziehen. View nur, wenn ich einen Kontext-Block brauche, dessen Position ich nicht kenne.

### 3.3 Inspektion nur, wenn nötig

Bei Folge-Iterationen muss ich nicht alle Dateien neu lesen. Wenn der Auftraggeber sagt „ändere nur g3-2-lineare-funktionen.html", schaue ich nicht in index.html, nav.js etc. rein.

### 3.4 ZIP-Packen ist nie der Risiko-Schritt

Sobald die Substanz drin ist, ist das ZIP zippbar. Wenn die Tool-Quote knapp wird, lieber ZIP mit Substanzstand jetzt als Feinschliff, der im Sand verläuft.

### 3.5 Tool-Quoten-Frühwarnung

Wenn Claude merkt, dass die Tool-Quote knapp wird (geschätzt > 70 % verbraucht), sagt er aktiv Bescheid und bietet Optionen:

> „Ich habe noch ungefähr Budget für 5 weitere Tool-Aufrufe. Möglichkeiten:
> a) ZIP jetzt mit aktuellem Stand (Punkt X und Y fertig, Z offen)
> b) Z noch fertig machen und dann ZIP — aber kein Spielraum mehr für Korrekturen
> Was bevorzugst du?"

Statt am Ende stillschweigend abzubrechen.

### 3.6 Themenseiten-Skelett: kopieren, nicht erfinden

Bevor Claude eine neue Themenseite anlegt, kopiert er das Body-Skelett aus einer fertigen Referenz-Seite (z.B. `g1-1-grundlagen.html` oder `g3-2-lineare-funktionen.html`) und passt nur Inhalt an. Die verbindliche Skelett-Spezifikation steht in **`STYLEGUIDE.md` § 6.1**.

**Vor dem ZIP-Packen läuft der Pre-Flight-Check** aus § 6.1 über alle neu erstellten oder modifizierten Themenseiten:

```bash
for f in <neue_oder_geänderte_seiten>; do
  pw=$(grep -c "page-wrap" "$f")
  mc=$(grep -c 'main class="content"' "$f")
  navjs=$(grep -c 'src="../nav.js">' "$f")
  navdef=$(grep -c 'src="../nav.js" defer' "$f")
  ml=$(grep -c 'src="../mathlib.js"' "$f")
  bn=$(grep -cE 'buildNav\(\{[[:space:]]*$|buildNav\(\{ bereich' "$f")
  sec=$(grep -cE '<section\b' "$f")
  bad=$(grep -cE 'class="(inhalt|brot|seiten-kopf|rlp|rlp-list|rlp-label|seiten-fuss|dl-box|ressourcen-grid|ress|ress-titel|ress-beschr|ress-quelle)"' "$f")
  togL=$(grep -c 'class="loesung-toggle"' "$f")
  if [ "$togL" != "0" ] && [ "$ml" = "0" ]; then mlw="MATHLIB-FEHLT!"; else mlw="ok"; fi
  printf "%-50s pw=%s mc=%s nav=%s def=%s ml=%s bn=%s sec=%s bad=%s tog=%s/%s\n" "$f" "$pw" "$mc" "$navjs" "$navdef" "$ml" "$bn" "$sec" "$bad" "$togL" "$mlw"
done
```

Erwartet: `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=N/ok`. Jede Abweichung wird vor dem ZIP behoben — sie zeigt Layout-Bruch oder eine Stelle, wo Lösungen sich nicht öffnen lassen.

**Hintergrund:** In zwei Iterationen hat Claude für 1.3/1.4 eigene Klassen erfunden — zuerst beim Body-Skelett (`<main class="inhalt">`, `<aside>` vor `<main>`, `defer` an nav.js, falsche `buildNav`-Signatur), dann bei den Inhalts-Containern (`<div class="ressourcen-grid">` mit `<a class="ress">` statt `<div class="links-grid">` mit `<a class="lk">`; in 2.3 zusätzlich `<div class="dl-box">` statt `<div class="dl-grid">`). Die Seiten wirkten strukturell „plausibel", aber die selbst erfundenen CSS-Klassen existieren nicht — Layout fiel auf Block-Default zurück, Karten wurden zu Listen, Sidebar überlappte. Solche Schäden sind durch grep-basierten Pre-Flight in einem Tool-Aufruf restlos sichtbar, **bevor** das ZIP gepackt wird.

### 3.7 Strukturelle Integritäts-Checks nach Block-Patches

Der Standard-Pre-Flight aus § 6.1 der `STYLEGUIDE.md` zählt nur **Marker-Anwesenheit**: existiert `<main class="content">`, existiert `<aside class="toc-wrap">`, gibt es eine `buildNav`-Signatur, kommen keine Phantom-Klassen vor. Das genügt für Skelett-Vergleiche, erkennt aber **keine kaputte Verschachtelung**, die durch einen unsauberen Block-Ersatz entsteht (typisch: zu früh stoppendes Regex-Pattern hinterlässt einen Müll-Schwanz aus dem alten Block; verwaiste `</a>`-Tags zerschiessen die CSS-Grid-Beziehung zwischen `<main>` und `<aside>`).

**Verbindlich vor jedem ZIP-Packen, wenn ein Block ersetzt wurde** (Ressourcen-Sektion, Zusatzmaterial-Sektion, RLP-Kompetenzen-Box, h2-Abschnitt):

```bash
for f in <gepatchte_dateien>; do
  # 1. Eindeutigkeits-Check: kritische Marker exakt 1× pro Datei
  for marker in '<h2 id="ressourcen"'                 'ressourcen-subtitel">🎬'                 '<div class="dl-grid"'                 '<aside class="toc-wrap"'                 '<footer class="site-footer"'; do
    n=$(grep -cE "$marker" "$f")
    [ "$n" = "1" ] || echo "DUPLICATE-MARKER $f: '$marker' kommt ${n}× vor (erwartet 1)"
  done

  # 2. Tag-Bilanz innerhalb der Ressourcen-Sektion
  block=$(sed -n '/<h2 id="ressourcen"/,/<\/main>/p' "$f")
  a_open=$(echo "$block" | grep -oE '<a [^>]*class="lk' | wc -l)
  a_close=$(echo "$block" | grep -oE '</a>' | wc -l)
  [ "$a_open" = "$a_close" ] || echo "TAG-IMBALANCE $f: $a_open <a>, $a_close </a>"

  # 3. Slot-Limits in den kuratierten Sektionen (max 4)
  vid_n=$(echo "$block" | awk '/🎬/,/📝/' | grep -cE '<a href=')
  auf_n=$(echo "$block" | awk '/📝/,EOF' | grep -cE '<a href=')
  [ "$vid_n" -le 4 ] && [ "$auf_n" -le 4 ] || echo "SLOT-LIMIT $f: vid=$vid_n auf=$auf_n"
done
```

Erwartete Ausgabe: **leer**. Jede Zeile zeigt einen Schaden, der dem User sonst erst im Browser auffallen würde. Speziell `DUPLICATE-MARKER` und `TAG-IMBALANCE` decken den Fail-Modus auf, bei dem das Standard-Pre-Flight grün zeigt, weil die Marker zwar existieren, aber die Verschachtelung kaputt ist.

**Hintergrund:** In der Cluster-g3-Iteration hat Claude für g3-1 und g3-3 ein Replacement-Pattern `<h2 id="ressourcen".*?</div>\s*</div>` benutzt, das non-greedy beim ersten `</div></div>` mitten in der Sub-Sektion stoppte. Der Rest der alten Sektion blieb stehen → doppelte Subtitel, doppelte Karten, verwaistes `</a>`, kaputte `<main>`/`<aside>`-Geschwister-Beziehung. Standard-Pre-Flight meldete grün (alle Marker da, keine Phantom-Klassen), Schaden fiel erst im Browser-Test auf. Strukturelle Checks aus diesem Abschnitt hätten den Bruch in einem Tool-Aufruf sichtbar gemacht.

### 3.8 Skript-Abhängigkeiten: globale Funktionen brauchen ihr Modul

Die Standard-Toggle-Funktion `toggleL` für aufklappbare Lösungen lebt in `mathlib.js`. Andere globale Helfer (`fmt`, `parseL`, …) ebenfalls. Eine Themenseite, die solche Funktionen via `onclick="toggleL('…')"` aufruft, muss `mathlib.js` einbinden — sonst gibt es einen stillen `ReferenceError` beim Klick, der nicht visuell auffällt (Lösung klappt einfach nicht auf, keine Konsole-Meldung sichtbar für den User).

**Verbindlich vor jedem ZIP-Packen, wenn Themenseiten erstellt oder migriert wurden:**

```bash
for f in <neue_oder_geänderte_seiten>; do
  uses_toggle=$(grep -c 'class="loesung-toggle"' "$f")
  has_mathlib=$(grep -c 'src="../mathlib.js"' "$f")
  if [ "$uses_toggle" != "0" ] && [ "$has_mathlib" = "0" ]; then
    echo "MATHLIB-FEHLT $f: $uses_toggle Toggle-Buttons, aber mathlib.js nicht eingebunden"
  fi
done
```

Erwartete Ausgabe: **leer**. Jede `MATHLIB-FEHLT`-Zeile zeigt eine Datei, deren Lösungen zwar visuell korrekt aussehen, aber beim Klick nichts tun.

**Hintergrund:** In der Aufgaben/Lösungs-Migration vom 17. Mai 2026 wurden die Themenseiten g1-3 und g1-4 vom alten `aw`-Schema (mit eigenem Inline-`classList.toggle('offen')`-Mechanismus) auf das Standard-`toggleL('id')`-Schema umgestellt. Da beide Seiten ihren eigenen Toggle hatten, war `mathlib.js` dort historisch nie eingebunden — nach der Migration fehlte das Skript also weiterhin, obwohl der neue Code es aufrief. Erst der Browsertest („Lösung lässt sich nicht öffnen") zeigte den Bruch. Der Pre-Flight-Check oben hätte den Fehler in einem einzigen Tool-Aufruf direkt nach der Migration sichtbar gemacht, ohne Browsertest.

**Analoger Check für andere globale Helfer**, falls eine Themenseite sie nutzt:

```bash
# Generischer Check: jede onclick="funcName(…)"-Verwendung muss zu einer src=-Einbindung passen,
# wenn funcName nicht im selben <script>-Block der Datei definiert ist.
# Reservierte Namen aus mathlib.js (siehe STYLEGUIDE §6.2): fmt, fmtS, fmtMx, fmtAffine,
# parseL, toggleL, initCanvas, drawGrid, drawLine, drawDot.
```

---

## 4. Was der Auftraggeber liefert

**Bei jeder Folge-Iteration:**
- Aktuellstes ZIP des Projektstands hochladen (sofern Änderungen lokal gemacht wurden, die Claude nicht kennt)
- Alle gewünschten Änderungen in einer Nachricht bündeln
- Bei Bezug auf vorherige Chats: kurzer Hinweis, was relevant ist (Claude kann ältere Chats durchsuchen, aber gezielter Hinweis spart Tool-Aufrufe)

**Bei Erst-Auftrag eines neuen Themas:**
- Lerngebiet-Bezeichnung (z.B. „Grundlagenfach 3.3 Quadratische Funktionen")
- RLP-Kompetenzen (oder Hinweis, dass Claude sie aus dem Rahmenlehrplan-Dokument im Project-Knowledge ziehen soll)
- Spezielle Wünsche, die vom Standard-Schema abweichen

---

## 5. Default-Verhalten von Claude

Diese Defaults gelten ohne weitere Nachfrage:

- **Bei klaren Aufträgen nicht rückfragen.** Wenn der Auftrag eindeutig ist, direkt umsetzen — auch wenn ich an einer Detailstelle eine Annahme treffen muss. Dann die Annahme inline kurz erwähnen, nicht eine Frage stellen.
- **Bei Mehrdeutigkeit: max. 3 gebündelte Fragen, dann starten.** Keine Endlos-Klärungsschleifen.
- **Tabellen, Code-Blöcke und Formate** wo angebracht (Listen-Output, Strukturvergleiche), Fliesstext sonst.
- **Mathematische Formeln immer in LaTeX**, Symbole gemäss FTB (siehe `STYLEGUIDE.md`).
- **Diagramme:** reine Mathematik 1:1 skaliert, Anwendungen aufgabenbezogen mit Einheiten an den Achsen.
- **Sprache:** Deutsch (Schweizer Hochdeutsch, ohne ß — also „Funktionsgleichung aufstellen", aber „dass" statt „daß").
- **Dezimaltrennzeichen:** Punkt, nicht Komma (Schweizer Schul-Konvention).

---

## 6. Was Claude NICHT tut

- Keine ungebetene „Verbesserungs-Initiative" am Code, der nicht Gegenstand der Aufgabe ist. Wenn Claude bei einem Patch unterwegs etwas anderes auffällt, kurz im Output erwähnen, aber nicht ungefragt mit-patchen.
- Kein Refactoring „weil's eleganter wäre". Funktionierende Strukturen bleiben, ausser explizit Refactoring-Auftrag.
- **Keine eigenen Klassen-Namen, Container-Hierarchien oder API-Signaturen erfinden.** Wenn der Styleguide ein Skelett vorgibt (siehe §6.1), wird es 1:1 kopiert. „Klingt vernünftig" reicht nicht — CSS und nav.js sind auf die *exakten* Klassen ausgerichtet.
- Keine Annahmen über Tools, die nicht da sind. Wenn ein Tool fehlt, das Claude bräuchte (z.B. Internet-Zugriff in einer bestimmten Form), explizit melden statt zu raten.
- Keine erfundenen Quellen, Zitate oder Lehrplan-Stellen. Im Zweifel sagen „das müsste verifiziert werden".

---

## 7. Was beim Tool-Limit-Stop passiert

Falls trotz aller Massnahmen der Tool-Budget-Stop erreicht wird:

1. **Claude packt sofort ein ZIP** mit dem aktuellen Stand, auch wenn unvollständig.
2. **Claude listet explizit auf**, was fehlt — als Punkt-Liste, präzise genug, dass ein neuer Chat sie umsetzen kann.
3. **Claude formuliert den Folge-Prompt**, den der Auftraggeber im neuen Chat verwenden kann.
4. **Keine Schuldzuweisung**, keine Selbst-Geisselung. Sachlich melden.

---

## 8. Pflege dieses Dokuments

Diese Datei wird erweitert, wenn Erfahrungen zeigen, dass eine Konvention fehlt oder verfeinert werden sollte. Bei Änderungen:
- Versionsnummer hochzählen
- Datum aktualisieren
- Neue Konvention ist ab dem nächsten Chat gültig (Claude liest die Datei am Anfang jedes Chats neu)

---

## 9. Externe Videos und Aufgabensammlungen kuratieren

Die Sektion „Externe Videos &amp; Aufgabensammlungen" jeder Themenseite folgt einer festen Anbieter-Reihenfolge und einer verbindlichen Verifikations-Methode. **Detaillierte Anleitung in `HOWTO-externe-ressourcen.md` (im Repo).** Diese Kurzfassung hier reicht für die operative Arbeit zwischen Auftraggeber und Claude.

### 9.1 Anbieter-Reihenfolge (verbindlich)

- **Videos** (max. 4 Links, max. 1 Playlist pro Anbieter):
  1. MathemaTrick
  2. Lehrerschmidt
  3. Mathe SMI
  4. Mathehoch13
  5. Magda liebt Mathe
  6. Mathe by Daniel Jung

- **Aufgabensammlungen** (max. 4 Links, mehrere pro Plattform erlaubt):
  1. sos-mathe.ch
  2. serlo.org
  3. SwissEduc Munterbunt

### 9.2 Regeln in Kürze

- **Videos**: Playlists strikt bevorzugt. Hat ein Anbieter zum Thema keine Playlist → Anbieter überspringen. Wenn nach allen 6 Anbietern weniger als 4 Playlists vorhanden sind → mit Einzelvideos in derselben Reihenfolge auffüllen. Wenn gar nichts gefunden wird → Platzhalter-Karte (Form siehe HOWTO §6).
- **Aufgaben**: Eine Plattform darf mehrere Aufgabenseiten zum gleichen Thema beisteuern (z.B. serlo.org hat häufig 2–4 passende Seiten pro Thema, alle dürfen in die 4-Slot-Grenze).
- **Lösungen**: Bei Aufgabensammlungen müssen Lösungen vorhanden sein. Reine Aufgabenlisten ohne Musterlösung sind raus.
- **Negativ-Liste**: kein Mathebibel, kein Mathepower, kein klassenarbeiten.de, keine YouTube-Suchergebnis-URLs, keine youtu.be-Kurz-URLs.

### 9.3 Verifikations-Methode — wichtigste Regel

**Playlist-ID-Präfixe sind keine zuverlässigen Kanal-Indikatoren.** Ein und derselbe YouTube-Kanal kann verschiedene Präfix-Familien nutzen. Heuristik aus dem Präfix → falscher Anbieter → falsche Karte auf der Themenseite.

**Die einzige zuverlässige Methode**: `web_fetch` auf die Playlist-URL aufrufen. Die Antwort enthält den **Owner-Namen** und die **Videoanzahl**.

```
web_fetch("https://www.youtube.com/playlist?list=<PLAYLIST_ID>")
→ liefert z.B. "Owner: Mathe SMI · Count: 8 videos"
```

Diese Verifikation kostet einen einzigen Tool-Aufruf pro Kandidat — billiger als jede Heuristik, die später Fehler korrigieren muss.

### 9.4 Cluster-weiser Recherche-Lauf

Eine komplette Themenseite (Videos + Aufgaben) braucht ca. 4–8 Tool-Aufrufe. Für 19 Grundlagen-Themen oder 13 Schwerpunkt-Themen sind das insgesamt 75–150 Aufrufe. Empfehlung: pro Chat-Sitzung **einen Lerngebiet-Cluster** abarbeiten (z.B. g4-1 bis g4-3 in einem Chat, g5-1 bis g5-5 im nächsten).

### 9.5 Pflege der Anbieter-Map

In `HOWTO-externe-ressourcen.md` §8 wird eine Tabelle der bereits verifizierten Playlist-IDs pro Thema gepflegt. **Bei jedem abgeschlossenen Recherche-Lauf wird diese Tabelle erweitert.** So muss eine bereits verifizierte Playlist nicht erneut recherchiert werden.

### 9.6 Übertragung Grundlagen → Schwerpunkt

Identisches Verfahren, identische Anbieter-Reihenfolge. Erwartete Verteilung:
- Sek-I-affine Schwerpunkt-Themen (Arithmetik, einfache Gleichungen) → MathemaTrick und Lehrerschmidt dominieren.
- Schwerpunkt-Funktionen (Logarithmen, Polynome, Trigonometrische Funktionen) → Mathe SMI und Mathehoch13 oft Treffer.
- Schwerpunkt-Vektorgeometrie → Magda liebt Mathe wird relevanter.

---

## 10. Animations-Refactorings (Canvas-Animationen)

Eine separate Workflow-Kategorie ist die **Anpassung interaktiver Canvas-Animationen** in einer bestehenden Themenseite. Charakteristisch: viele kleine Auftragspakete für *eine* Datei, sichtprüfungsbasiert, geometrische und visuelle Korrektheit über reine Code-Korrektheit hinaus.

### 10.1 Auftragsformat

Der Auftraggeber liefert ein **PDF mit ein paar nummerierten Aufträgen** (typisch 3–7 Stück), die je eine Animation der Datei betreffen. Beispiele aus der Sitzung 2026-05-16 zur Datei `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html`:

1. „Anim 1 — Z, A, B, C verschiebbar"
2. „Anim 2 — Strahlensätze komplett neu gestalten"
3. „Anim 3 — bei k=±2 zeigen, dass Fläche 4-fach"
4. „Anim 4 — Beschriftung verbessern + sss-Konvention"
5. „Anim 5 — α/β-Position korrigieren + Drehkopie"

### 10.2 Pro-Auftrag-Workflow

```
1. Vorschlag erläutern   (kurz, was geometrisch und visuell gemacht wird)
2. User bestätigt        (oder verfeinert die Spec)
3. Umsetzung             (im Code)
4. Verifikation          (Python-Geometrie-Simulation + Node-Syntax-Check)
5. CHANGELOG-Eintrag     (ausführlich, weil später Doku-Wert)
6. Zwischensicherung     (ZIP mit aussagekräftigem Suffix: _g5-2d-anim3.zip,
                          _g5-2d-anim5-2.zip, _g5-2d-anim2-v3.zip etc.)
7. User testet im Browser
8. Bei Nachjustierung: zurück zu 1.
```

Die Zwischen-ZIPs sind essenziell — bei sichtprüfungs-basierten Aufgaben spart das einen kompletten Iterations-Zyklus, weil der Auftraggeber sofort am Snapshot probieren kann.

### 10.3 Verifikationswerkzeuge

- **Python-Geometrie-Simulation:** bei jedem Auftrag, der Koordinaten betrifft, wird `python3 -c "import math; ..."` aufgerufen, um die Zielpositionen (Eckpunkte, Label-Stellen, Versatz-Vektoren) **vor** der Code-Änderung durchzurechnen. So fängt Claude Bugs in der Geometrie-Mathematik ab, bevor sie im Browser landen. Beispiel: der Bisektrix-Bug in `drawAngleArc` (gespiegelte Label-Position bei `atan2`-Branch-Cut) wurde durch direkte Simulation der Label-Koordinaten gefunden.
- **Node-Syntax-Check** auf jedem Script-Block: `node --check sc.js` (mit Mini-DOM-Mocks). Fängt Tippfehler im JS, bevor sie zu Browser-Konsolen-Errors werden.
- **Canvas-Bounds-Check:** sind alle berechneten Endpunkte / Labels im Canvas-Bereich? Margin-Prüfung mit `0 < pt[0] < W and 0 < pt[1] < H`.

### 10.4 Bilder als Iterations-Input

Der Auftraggeber lädt häufig **Screenshots** der aktuellen Animation hoch, um Probleme zu zeigen (z.B. „diese Beschriftung liegt auf der Linie", „Farben hier konfliktig"). Claude analysiert das Bild, identifiziert die Code-Stelle und schlägt eine Korrektur vor. Das ist erheblich effizienter als textuelle Beschreibung.

### 10.5 Refactoring quer durch andere Dateien

Manche Erkenntnisse aus der Arbeit an einer Datei lassen sich global anwenden — Beispiel HiDPI-Rendering: in der g5-2d-Sitzung wurde der Fix auch auf g5-3 und g5-4 ausgerollt, weil die gleiches Pattern hatten. Bei solchen Cross-File-Patches **kurz beim Auftraggeber rückfragen**, ob das ok ist, und die Konvention dann im STYLEGUIDE festhalten (so geschehen in STYLEGUIDE §5.5.1).

---

*Wenn du als Auftraggeber etwas in dieser Datei änderst, das Claude in der laufenden Konversation noch nicht kennt: kurz darauf hinweisen, damit Claude die neue Konvention sofort anwendet.*
