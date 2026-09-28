# TODO — Übertrag ins Schwesterprojekt (TALS Physik)

Hier sammeln sich Änderungen aus TALS-Mathe, die auch in TALS-Physik gehören
(gemeinsame CSS-Muster, didaktische Module, Nav-Logik, geteilte JS-Helfer).
Claude Code editiert NIE über Repos hinweg — Einträge werden hier vermerkt und
später in einer Physik-Session von Hand portiert.

Format pro Eintrag: Datum · was · wo (Datei/Selektor) · warum.

**Bereinigt am 28.09.2026:** Alle Einträge wurden gegen das Physik-Repo geprüft
(Stand `f115899`, nur gelesen). Erledigte und gegenstandslose sind entfernt —
ihr Wortlaut steht in der Git-Geschichte dieser Datei. Übrig waren danach drei; neue kommen unten dazu.
Ein erledigter Eintrag wird künftig gelöscht, nicht als «erledigt» markiert.
Übertrage an geteiltem Werkzeug laufen zusätzlich über die Warteschlange `OFFEN`
in `scripts/abgleich.py`.

## Offen

- **2026-09-07 · Clip-Generator: Bedingungsleiste `voraussetzung` · `scripts/build-clips.py` · warum:** (Zählungen vom 07.09.2026; die zwei übrigen Bausteine `boxplot` und `beschriftung_bei` entfallen für Physik.)

  Gezählt im Physik-Repo am 07.09.2026, nicht geschätzt. Physiks
  `scripts/build-clips.py` kennt die Elementtypen `aussage`, `box`, `formel`, `graf`,
  `karte`, `liste`, `notiz`, `strich`, `text`, `titel`, `untertitel` — und **79
  Drehbücher** stehen dort (heute rund 200). Die Bedingungsleiste fehlt ihm weiterhin.


  **Was.** Ein Drehbuch bekommt neben `titel` ein Feld `voraussetzung`. Der Generator
  legt daraus eine schmale Leiste unter den Kopf, die **den ganzen Clip über stehen
  bleibt** — dort steht die Bedingung, auf der alles Folgende ruht (`a \neq 0`,
  `x \gt 0`, „nur im rechtwinkligen Dreieck"). Sie ist keine Szene, sie verschwindet nie.

  **Warum das didaktisch zählt.** Der Anlass war eine Beobachtung des Autors: Im Verlauf
  eines Clips wird oft auf eine Voraussetzung aufgebaut, die längst aus dem Bild gescrollt
  ist. Wer bei Minute zwei einsteigt, sieht die Rechnung, aber nicht, wofür sie gilt.

  **Abgrenzung, damit sie nicht verwässert.** Die Leiste trägt nur, was **von Anfang an
  gilt**. Was der Clip erst *herleitet*, gehört nicht hinein — sonst steht die Antwort
  schon in der Kopfzeile, bevor die Frage gestellt ist.

  **Wo in Physik.** `voraussetzung` kommt in `scripts/build-clips.py` **0-mal** vor.
  Dafür benutzen dort **77 von 79 Drehbüchern** `halten`, und das HOWTO warnt: „Eine
  gehaltene Zeile belegt das Band oben." `halten` und `voraussetzung` lösen **verwandte,
  aber verschiedene** Probleme — `halten` trägt eine Zeile *aus einer Szene* weiter,
  `voraussetzung` steht über dem *ganzen* Clip. Dass 77 von 79 Clips zum Halten greifen,
  ist der beste Beleg dafür, dass der Bedarf in Physik gross ist.

  **Was zu übertragen ist.** Die Emission nach dem Fussbereich in `build-clips.py`, das
  CSS `#vorleiste` / `.vor`, und die Schutzregel — Mathe bricht den Bau ab, wenn eine
  Szene mit `oben < 170` in die Leiste liefe:

  ```python
  if dreh.get("voraussetzung") and sz.get("oben", oben) < 170:
      raise SystemExit("Szene %r beginnt bei oben=%d und liefe in die Bedingungsleiste …")
  ```

  Physik braucht dort eine **eigene Zahl**, weil das Band von `halten` bereits Platz
  belegt: dort beginnen Folgeszenen laut HOWTO bei `oben: 430`. Wer beides kombiniert,
  prüft die Schwelle im Browser nach, statt 170 zu übernehmen.
