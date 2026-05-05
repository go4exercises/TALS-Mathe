# Arbeitsweise mit Claude — TALS-Mathematik-Projekt

**Version 1.0 · Stand: Mai 2026**

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

*Wenn du als Auftraggeber etwas in dieser Datei änderst, das Claude in der laufenden Konversation noch nicht kennt: kurz darauf hinweisen, damit Claude die neue Konvention sofort anwendet.*
