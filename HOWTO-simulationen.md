# HOWTO — Simulationen

**Gilt seit 10.10.2026.** Wann eine Animation eine eigene Seite unter `simulationen/` bekommt,
wie diese Seite aussieht und wie sie mit den Themenseiten verbunden wird. Das Gegenstück für
Trainer und Rechner ist `HOWTO-werkzeuge.md`; beide sind absichtlich gleich gegliedert. Bei
Widerspruch gilt `STYLEGUIDE.md`.

Dieselbe Anleitung steht in `tals-physik` — dort mit `physiklib.js` und `themen/` statt
`mathlib.js` und `grundlagen/`/`schwerpunkt/`. Wer hier etwas am Verfahren ändert, trägt es
über die Warteschlange `OFFEN` in `scripts/abgleich.py` drüben ein (CLAUDE.md,
«Schwesterprojekt»).

---

## 1 · Wozu und Abgrenzung

Drei Arten interaktiver Inhalte, drei Orte:

| | was man tut | wo sie liegt | Beispiel |
|---|---|---|---|
| **Animation** | eine Idee an einer Stelle zeigen, ein bis drei Regler | eingebettet in die Themenseite (`.widget`) | Werkstatt-Waage in g2.1 |
| **Simulation** | ein Modell beobachten und seine Grössen verändern, mit eigener Abfolge | eigene Seite `simulationen/<name>.html` | Bungee-Sprung, Würfelexperiment zum Gesetz der grossen Zahlen |
| **Werkzeug** | eigene Aufgaben oder Daten eingeben, üben, Rückmeldung bekommen | eigene Seite `werkzeuge/<name>.html` | Notationstrainer, Standardabweichung mit eigenen Messwerten |

**Eigene Seite statt Animation** nur, wenn mindestens eines zutrifft:

- sie braucht mehr als einen Bildschirm (mehrere Ansichten, Diagramme nebeneinander, Tabelle der Durchläufe),
- sie hat eine eigene Abfolge (Szenen, Schritte, «Weiter»),
- sie wird auch ohne die Themenseite benutzt (im Unterricht direkt geöffnet).

Sonst bleibt sie eine Animation in der Themenseite (`STYLEGUIDE.md`, Animationen).

**Simulation oder Werkzeug?** Eine Frage entscheidet: *Gibt man eigene Daten oder Aufgaben ein?*
Ja → Werkzeug. Nein, man verändert nur die Grössen eines vorgegebenen Modells → Simulation.
Die Standardabweichung, in die man eigene Messwerte tippt, ist ein Werkzeug; dieselbe
Rechnung als Schieberegler-Modell, das zeigt, wie Ausreisser die Streuung treiben, wäre eine
Simulation.

**Wortgebrauch:** In den Leitprogrammen (`HOWTO-leitprogramme.md` §8) heissen die *eingebetteten*
Erkundungen ebenfalls «Simulationen». Das bleibt so. Ist von der Rubrik die Rede, heisst es
«Seite unter `simulationen/`» oder «Simulationsseite».

## 2 · Ablage und Name

- Datei: `simulationen/<name>.html`, Name in Kleinbuchstaben mit Bindestrich, **ohne Nummer**
  (`bungee-sprung.html`, nicht `g4-3-bungee.html`). Eine Simulation gehört oft zu mehreren
  Themenseiten; die Nummer stünde immer für nur eine.
- Bilder, Daten oder Hilfsdateien nur, wenn nötig, dann in `simulationen/<name>/`.
- Keine Seite im Repo-Root und keine unter `grundlagen/`/`schwerpunkt/`: Die Ordner der
  Themenseiten werden von den Prüfskripten als Themenseiten gelesen.

## 3 · Seitenaufbau

Es gibt noch keine Simulationsseite in Mathe. Vorlage ist darum der Kopf von
`werkzeuge/notationstrainer.html` (gleiche Tiefe, gleiche Einbindungen) und für die Animation
selbst eine Animation aus der passenden Themenseite.

- **Einbindungen**, alle relativ eine Ebene hinauf und **kein fremder Host**:
  `../schriften.css`, `../style.css`, `../vendor/mathjax/tex-svg.js`, `../mathlib.js`
  (Canvas-Helfer, `toggleL`), `../anim-hinweise.js` (👁/💡 sind Pflicht, wie in den
  Themenseiten), `../nav.js`.
- **Navigation:** `buildNav({ id: 'simulationen' })` — ohne `homepage`, damit die Links mit
  `../` beginnen; ohne `kapitelNr`, `prev`, `next`. Im Menü ist dann «Nachschlagen»
  hervorgehoben.
- **Kopf:** `.page-titel` mit `<div class="pt-bereich">SIM · Simulationen</div>`, Titel als
  `h1.pt-h1`, ein Satz in `.pt-untertitel`, was man hier beobachtet.
- **Rücklink** als letzter Satz im `.pt-untertitel`, auf den **Abschnitt** der Themenseite
  (Anker), nicht nur auf die Seite:
  `Der Stoff dazu steht in <a href="../grundlagen/g4-3-masszahlen.html#theorie">4.3 Masszahlen</a>.`
  Gehört sie zu keinem Themenbereich, entfällt der Satz.
- **Klassen** aus `style.css` und den Themenseiten kopieren, nicht erfinden (CLAUDE.md,
  «Skelett & Klassen»). Seiteneigenes CSS im `<style>` der Seite mit eigenem Präfix
  (Muster: `nt-` im Notationstrainer).
- Den SEO-Kopf **nicht** von Hand schreiben: Er entsteht aus `scripts/build-seo.py` (§4).

## 4 · Eintragen

Eine Simulation hängt an vier Stellen; fehlt eine, meldet es der Pre-Flight (§6) oder sie ist
nicht auffindbar.

1. **Übersicht** `simulationen.html`, zwischen `<!-- SIMULATIONEN:ANFANG -->` und
   `<!-- SIMULATIONEN:ENDE -->`: eine Kachel unter Fach und Themenbereich, aufgebaut wie
   in `werkzeuge.html` — `a.karte` über der ganzen Kachel, `.lp-kopf` Titel, `.lp-satz` ein
   Satz, je verweisende Themenseite eine `.lp-zeile` mit Pille auf den Abschnitt. Gehört sie
   zu mehreren Fächern, steht die Kachel in jedem Fach einmal. Ohne Themenbereich unter
   `<h2 id="ausserhalb">Ausserhalb der Lerngebiete</h2>`. Den Satz `.ue-leer` löschen,
   sobald die erste Kachel steht.
2. **`scripts/build-seo.py`**, Tabelle `SEITEN`: Schlüssel `'simulationen/<name>.html'`,
   `typ='article'`, `lrt='Simulation'`, Titel, Beschreibung 140–165 Zeichen, `themen`.
   Dann `python3 scripts/build-seo.py` — nach dem Commit ein zweites Mal (Kopfkommentar
   des Skripts) und die Datumsänderung mitcommitten.
3. **`scripts/build-suchindex.py`**, Liste `ZUSATZSEITEN`: `('simulationen/<name>.html', 'SIM',
   '<Titel>', 'thema')` unter dem Kommentar «Simulationen und Werkzeuge selbst». Dann
   `python3 scripts/build-suchindex.py`.
4. **Themenseite**, siehe §5.

`nav.js` und `index.html` bleiben unberührt: Die Rubrik steht dort schon, einzelne Seiten nicht.

## 5 · Verlinken in der Themenseite

**Im Abschnitt, zu dem die Simulation inhaltlich gehört** — nicht am Seitenanfang (dort steht
nur das Leitprogramm), nicht im Zusatzmaterial, und **keine Abzeichen auf den Kacheln von
`index.html`**. Baustein, Wortlaut fest:

```html
<div class="block block-tipp" style="margin-top:10px">
  <div class="block-titel">🧪 Simulation: Bungee-Sprung</div>
  <p>Ein Satz, was man dort beobachtet und verändert. <a href="../simulationen/bungee-sprung.html">Zur Simulation →</a></p>
</div>
```

Platz: nach dem Definitions- oder Beispielblock, den die Simulation vertieft, vor Mini-Check
und Verständnisfragen des Abschnitts. Ein Abschnitt trägt höchstens einen solchen Baustein je
Simulation; verweisen mehrere Themenseiten darauf, bekommt jede ihren eigenen.

Ein Leitprogramm darf im passenden Schritt auf die Simulation zeigen, statt sie nachzubauen —
mit einem gewöhnlichen Link, nicht mit dem Baustein.

## 6 · Prüfen

- **Pre-Flight** über die neue Seite und jede geänderte Themenseite:
  `python3 .claude/skills/preflight/preflight.py simulationen/<name>.html grundlagen/<seite>.html`.
  `check_sim_wz` meldet als `[FEHLER]`, wenn die Seite in `simulationen.html` fehlt oder ein
  Rücklink-Anker nicht existiert, als `[WARN]`, wenn keine Themenseite auf sie verweist und
  sie nicht unter `#ausserhalb` steht.
- **Zahlen und Geometrie vorab in `python3`** durchrechnen: Stützpunkte, Schnittpunkte,
  Endwerte, Label-Positionen (CLAUDE.md, «Verifikations-Standard»). Eine Simulation zeigt
  mehr Zustände als eine Animation, also mehr Stellen, an denen ein falscher Wert sichtbar wird.
- **Render-Check** bei 1280 px und 360 px: `node .claude/tools/render-check.mjs
  simulationen/<name>.html`, Screenshots der Canvases ansehen. Kein seitliches Scrollen,
  Regler bei 360 px bedienbar.
- **Clips** sind freiwillig; wenn, dann nach `HOWTO-clips.md`.

## 7 · Verschieben oder umbenennen

Eine veröffentlichte Adresse steht in Lesezeichen und Unterrichtsunterlagen. Wird eine Seite
verschoben oder umbenannt:

1. `git mv`, damit die Geschichte mitwandert; relative Pfade in der Datei anpassen.
2. Alte Adresse in **`404.html`**, Tabelle `WEITERLEITUNGEN`, eintragen
   (`'/alt.html': '/simulationen/neu.html'`). GitHub Pages liefert `404.html` für jede
   fehlende Adresse aus; das Skript leitet weiter und behält den Anker. **Keine Hilfsseite
   an der alten Stelle** — sie läge in den Globs der Prüfskripte.
3. Alle Verweise umstellen: `grep -rn '<alter name>' --exclude-dir=node_modules .` —
   Themenseiten, Leitprogramme, deren Bauskripte unter `scripts/lp/`, `build-seo.py`,
   `build-suchindex.py`, Doku.
4. Gespeicherte Stände (`localStorage`-Schlüssel) **nicht** umbenennen, sonst verlieren die
   Lernenden ihren Stand.

## 8 · Checkliste

- [ ] Eigene Seite gerechtfertigt (§1), Simulation und nicht Werkzeug
- [ ] `simulationen/<name>.html`, ohne Nummer, Einbindungen mit `../`, kein fremder Host
- [ ] `buildNav({ id: 'simulationen' })`, `pt-bereich` «SIM · Simulationen», Rücklink mit Anker
- [ ] 👁/💡-Hinweise, Werte in `python3` nachgerechnet
- [ ] Kachel in `simulationen.html` (je Fach), `.ue-leer` entfernt
- [ ] `build-seo.py` `SEITEN` + zweimal laufen lassen
- [ ] `build-suchindex.py` `ZUSATZSEITEN` + laufen lassen
- [ ] Baustein «🧪 Simulation:» im passenden Abschnitt jeder verweisenden Themenseite
- [ ] Pre-Flight `ALLE CHECKS BESTANDEN`, Render-Check 1280/360 angesehen
