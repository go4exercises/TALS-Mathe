# HOWTO — Werkzeuge

**Gilt seit 10.10.2026.** Wann ein Trainer oder Rechner eine eigene Seite unter `werkzeuge/`
bekommt, wie diese Seite aussieht und wie sie mit den Themenseiten verbunden wird. Das
Gegenstück für Simulationen ist `HOWTO-simulationen.md`; beide sind absichtlich gleich
gegliedert. Bei Widerspruch gilt `STYLEGUIDE.md`.

Dieselbe Anleitung steht in `tals-physik` — dort mit `physiklib.js` und `themen/` statt
`mathlib.js` und `grundlagen/`/`schwerpunkt/`, und mit dem Einheitentrainer als Vorbild. Wer
hier etwas am Verfahren ändert, trägt es über die Warteschlange `OFFEN` in
`scripts/abgleich.py` drüben ein (CLAUDE.md, «Schwesterprojekt»).

**Vorbild:** `werkzeuge/notationstrainer.html` (Lernkartei mit gespeichertem Stand).

---

## 1 · Wozu und Abgrenzung

Drei Arten interaktiver Inhalte, drei Orte:

| | was man tut | wo sie liegt | Beispiel |
|---|---|---|---|
| **Animation** | eine Idee an einer Stelle zeigen, ein bis drei Regler | eingebettet in die Themenseite (`.widget`) | Werkstatt-Waage in g2.1 |
| **Simulation** | ein Modell beobachten und seine Grössen verändern, mit eigener Abfolge | eigene Seite `simulationen/<name>.html` | Bungee-Sprung |
| **Werkzeug** | eigene Aufgaben oder Daten eingeben, üben, Rückmeldung bekommen | eigene Seite `werkzeuge/<name>.html` | Notationstrainer, Standardabweichung mit eigenen Messwerten |

**Simulation oder Werkzeug?** Eine Frage entscheidet: *Gibt man eigene Daten oder Aufgaben ein,
oder übt man an einem Vorrat von Aufgaben?* Ja → Werkzeug. Verändert man nur die Grössen eines
vorgegebenen Modells → Simulation (`HOWTO-simulationen.md`).

**Eigene Seite statt Aufgabe auf der Themenseite**, wenn das Werkzeug

- auch ohne die Themenseite benutzt wird (vor der Prüfung, im Unterricht direkt geöffnet),
- mehrere Themenseiten bedient, oder
- einen Stand führt, mehrere Modi hat oder mehr als einen Bildschirm braucht.

Ein einzelner Rechner zu einer einzigen Aufgabe bleibt in der Themenseite.

## 2 · Ablage und Name

- Datei: `werkzeuge/<name>.html`, Name in Kleinbuchstaben mit Bindestrich, **ohne Nummer**
  (`standardabweichung.html`, nicht `g4-3-rechner.html`).
- Hilfsdateien nur, wenn nötig, dann in `werkzeuge/<name>/`.
- Keine Seite im Repo-Root und keine unter `grundlagen/`/`schwerpunkt/`: Die Ordner der
  Themenseiten werden von den Prüfskripten als Themenseiten gelesen.

## 3 · Seitenaufbau

Vorlage ist `werkzeuge/notationstrainer.html`.

- **Einbindungen**, alle relativ eine Ebene hinauf und **kein fremder Host**:
  `../schriften.css`, `../style.css`, `../vendor/mathjax/tex-svg.js`, `../nav.js`; dazu
  `../mathlib.js`, sobald die Seite Canvas-Helfer oder `toggleL` nutzt, `../minicheck.js` bei
  `.minicheck`-Markup.
- **Navigation:** `buildNav({ id: 'werkzeuge' })` — ohne `homepage`, damit die Links mit
  `../` beginnen; ohne `kapitelNr`, `prev`, `next`.
- **Kopf:** `.page-titel` mit `<div class="pt-bereich">WZ · Werkzeuge</div>`, Titel als
  `h1.pt-h1`, ein Satz in `.pt-untertitel`, was man hier übt oder rechnet.
- **Rücklink** als letzter Satz im `.pt-untertitel`, auf den **Abschnitt** der Themenseite
  (Anker), bei mehreren Themenseiten auf jede:
  `Die Begriffe stehen in <a href="../grundlagen/g2-1-grundlagen.html#definition">2.1 Grundlagen</a>.`
- **Trainer-Rahmen** (seit 11.10.2026, für jeden Trainer verbindlich): `werkzeuge/trainer.css` und `werkzeuge/trainer.js`
  einbinden, Vorbild ist `werkzeuge/systemtrainer.html`. Alle Trainer sehen gleich aus und passen samt Bedienelementen
  auf einen Bildschirm (1280×800 und 360×740):
  - `.page-wrap.tr-wrap`; der `.pt-untertitel` ist **ein** Satz mit Rücklink, alles Weitere steht im Erklärblock
    unter der Karte.
  - `.tr-karte` reicht bis an den unteren Bildschirmrand (Höhe setzt `trainer.js`). Darin `.tr-aufgabe` mit drei
    Teilen:
    - `.tr-kopf`: links `.tr-tags` («Aufgabe n / 10», Thema), **rechts immer `.tr-naechster`** «Nächster Schritt»
      mit Zähler `.tr-zaehler`;
    - `.tr-flaeche`: `.tr-auftrag`, `.tr-ausdruck` und darunter `.tr-weg` — die Lösung **entwickelt sich unter der
      Aufgabe**, Schritt für Schritt (`.tr-schritt` mit `.tr-schritt-kopf` «Schritt n · Bezeichnung», Zeilen
      `.tr-zeile`/`.tr-text`, Ergebnis `.tr-ergebnis`, Skizze `.tr-bild`). Nur diese Fläche scrollt; nach jedem
      Schritt `trNachUnten(fläche)`;
    - `.tr-leiste`: Eingabe (`.tr-reihe`, `.tr-hinweis`), Auswahl (`.tr-wahlen` mit `.tr-wahl`), Knöpfe (`.tr-btn`),
      Rückmeldung `.tr-rueck` (`richtig`/`falsch`/`fast`) und `.tr-weiter-box` mit «Nächste Aufgabe».
  - Rundenende: `.tr-bilanz` statt `.tr-aufgabe`. Seitenspalte `aside.tr-seite` (`.tr-gruppen`, `.tr-gruppe`,
    `.tr-g-titel`, `.tr-zahl`, `.tr-opt`, `.tr-neu`), schmal eingeklappt über der Karte.
  - Seiteneigenes `<style>` (Präfix der Seite) nur für das, was der Rahmen nicht hat.
- **Daten an einer Stelle.** Aufgaben, Faktoren, Lösungen stehen in **einer** Datenstruktur im
  Seitenskript (Notationstrainer: `KARTEN`), aus der Aufgabe, Rückmeldung und jede Tabelle
  zugleich entstehen. Nie einen Wert an zweiter Stelle notieren.
- **Jede Lösung vorab mit `python3` nachrechnen**, bevor sie in die Datenstruktur kommt; bei
  Rechnern die Rechenvorschrift an Referenzwerten (CLAUDE.md, «Verifikations-Standard»).
- **Gespeicherter Stand** (`localStorage`) nur, wenn er dem Lernen dient, und dann so:
  - eigener Schlüssel `tals-mathe-<name>-v1`, versioniert; bei einem neuen Format `-v2`,
    nicht stillschweigend umdeuten,
  - jeder Zugriff in `try { … } catch (e) {}` — im privaten Fenster fehlt der Speicher,
  - ein sichtbarer Knopf zum Zurücksetzen (Muster `#nt-reset`),
  - ein Absatz in **`rechtliches.html`** unter «Werkzeuge mit Lernstand»: Name, Schlüssel,
    was gespeichert wird. Ohne diesen Absatz stimmt die Datenschutzerklärung nicht.
- **Klassen** aus `style.css` kopieren, nicht erfinden; Seiteneigenes im `<style>` mit
  eigenem Präfix (`nt-`).
- Den SEO-Kopf und den Footer **nicht** von Hand schreiben: Beide entstehen aus `scripts/build-seo.py` (§4);
  für den Footer nur die leeren FUSS-Marken nach `.page-wrap` setzen (STYLEGUIDE §7). Die Marken wörtlich aus
  der Vorbildseite kopieren, samt «— generiert von scripts/build-seo.py, nicht von Hand ändern»: Ein nacktes
  `<!-- SEO:ANFANG -->` erkennt das Skript nicht und setzt einen zweiten Kopf davor.

## 4 · Eintragen

Ein Werkzeug hängt an vier Stellen; fehlt eine, meldet es der Pre-Flight (§6) oder es ist
nicht auffindbar.

1. **Übersicht** `werkzeuge.html`, zwischen `<!-- WERKZEUGE:ANFANG -->` und
   `<!-- WERKZEUGE:ENDE -->`: eine Kachel unter Fach und Themenbereich — `a.karte` über der
   ganzen Kachel, `.lp-kopf` Titel, `.lp-satz` ein kurzer Satz (eine Zeile), darunter
   in `.lp-pillen` je verweisende Themenseite eine Pille ohne Text davor, die auf den Abschnitt zeigt. Bedient es mehrere Fächer, steht die Kachel in
   jedem Fach einmal. Ohne Themenbereich unter
   `<h2 id="ausserhalb">Ausserhalb der Lerngebiete</h2>`.
2. **`scripts/build-seo.py`**, Tabelle `SEITEN`: Schlüssel `'werkzeuge/<name>.html'`,
   `typ='article'`, `lrt=['Werkzeug', …]`, Titel, Beschreibung 140–165 Zeichen, `themen`, `ort`
   (Footer-Ortszeile, z.B. `ort='Werkzeuge · Notationstrainer'`).
   Dann `python3 scripts/build-seo.py` — nach dem Commit ein zweites Mal und die
   Datumsänderung mitcommitten.
3. **`scripts/build-suchindex.py`**, Liste `ZUSATZSEITEN`: `('werkzeuge/<name>.html', 'WZ',
   '<Titel>', 'thema')` unter dem Kommentar «Simulationen und Werkzeuge selbst». Dann
   `python3 scripts/build-suchindex.py`.
4. **Themenseite**, siehe §5.

`nav.js` und `index.html` bleiben unberührt: Die Rubrik steht dort schon, einzelne Seiten nicht.

Dazu ein Absatz in **`werkzeuge/CLAUDE.md`**: wozu die Seite dient, Themen und Vorwahl, Selbsttest und was nicht aus
dem Code hervorgeht. Claude Code lädt diese Datei nur, wenn es in `werkzeuge/` arbeitet; die Haupt-`CLAUDE.md` nennt
seit 11.10.2026 nur noch die Regeln für alle Seiten.

## 5 · Verlinken in der Themenseite

**Im Abschnitt, zu dem das Werkzeug inhaltlich gehört** — nicht am Seitenanfang (dort steht nur
das Leitprogramm), nicht im Zusatzmaterial, und **keine Abzeichen auf den Kacheln von
`index.html`**. Baustein, Wortlaut fest:

```html
<div class="block block-tipp" style="margin-top:10px">
  <div class="block-titel">🛠 Werkzeug: Notationstrainer</div>
  <p>Ein Satz, was man dort übt oder rechnet. <a href="../werkzeuge/notationstrainer.html">Zum Werkzeug →</a></p>
</div>
```

Platz: nach dem Definitions- oder Beispielblock, den das Werkzeug übt, vor Mini-Check und
Verständnisfragen des Abschnitts. Beispiel: g2.1 und s2.1, je im Abschnitt `#definition` nach
dem Block mit Grund-, Definitions- und Lösungsmenge. Verweisen mehrere Themenseiten darauf,
bekommt jede ihren eigenen Baustein.

Ein Leitprogramm darf im passenden Schritt auf das Werkzeug zeigen — mit einem gewöhnlichen
Link, nicht mit dem Baustein.

## 6 · Prüfen

- **Pre-Flight** über die neue Seite und jede geänderte Themenseite:
  `python3 .claude/skills/preflight/preflight.py werkzeuge/<name>.html grundlagen/<seite>.html`.
  `check_sim_wz` meldet als `[FEHLER]`, wenn die Seite in `werkzeuge.html` fehlt oder ein
  Rücklink-Anker nicht existiert, als `[WARN]`, wenn keine Themenseite auf sie verweist und
  sie nicht unter `#ausserhalb` steht.
- **Selbsttest**, sobald das Werkzeug rechnet oder Aufgaben erzeugt: eine Funktion im
  Seitenskript, die jede Aufgabe der Datenstruktur gegen ihre Lösung prüft, und ein Skript
  `scripts/verify_<name>.js`, das die Seite in jsdom lädt und sie aufruft. Muster ist
  `scripts/verify_einheitentrainer.js` in `tals-physik` (dort im Pre-Flight eingehängt). In
  Mathe: `scripts/verify_strategietrainer.js` — es lädt nur den Block zwischen `KERN:ANFANG` und
  `KERN:ENDE` in `node:vm` (ohne DOM) und spielt Tausende Zufallsaufgaben durch. Neue Selbsttests
  in die Liste der Werkzeug-Selbsttests in `preflight.py` aufnehmen.
  Dass die Musterlösung angenommen und jeder Denkfehler-Wert erkannt wird, genügt nicht (Prüfung
  aller Trainer am 11.10.2026, `TODO-trainer-korrekturen.md`). Der Selbsttest prüft auch:
  - ob ein Denkfehler-Wert zufällig der Lösung oder der Gegenzahl der Lösung entspricht. Solche
    Aufgaben verwerfen, oder dem Wert einen eigenen Code geben.
  - ob die Erklärung zum Denkfehler zur gestellten Aufgabe passt. Etwa «addiert» bei einem Minus
    oder «Klammer übersehen» bei \((-a)^3\): Hier ändert die Klammer nichts.
  - ob gleichwertige Eingaben angenommen werden, etwa eine gemischte Zahl oder `*` an jeder Stelle.
  - ob halbfertige Formen nicht als richtig gelten, etwa ein Doppelbruch oder eine unvereinfachte
    Klammer.
- **Render-Check** bei 1280 px und 360 px: `node .claude/tools/render-check.mjs
  werkzeuge/<name>.html`. Eingabefelder und Knöpfe bei 360 px bedienbar, kein seitliches
  Scrollen.
- **Gespeicherten Stand** einmal im privaten Fenster prüfen: Die Seite muss ohne Speicher
  funktionieren.

## 7 · Verschieben und Umbenennen

Eine veröffentlichte Adresse steht in Lesezeichen und Unterrichtsunterlagen. Wird eine Seite
verschoben oder umbenannt:

1. `git mv`, damit die Geschichte mitwandert; relative Pfade in der Datei anpassen (auch
   Pfade in Daten des Seitenskripts — im Notationstrainer `S_G22A` usw.).
2. Alte Adresse in **`404.html`**, Tabelle `WEITERLEITUNGEN`, eintragen
   (`'/notationstrainer.html': '/werkzeuge/notationstrainer.html'`). GitHub Pages liefert
   `404.html` für jede fehlende Adresse aus; das Skript leitet weiter und behält den Anker.
   **Keine Hilfsseite an der alten Stelle** — sie läge in den Globs der Prüfskripte.
3. Alle Verweise umstellen: `grep -rn '<alter name>' --exclude-dir=node_modules .` —
   Themenseiten, Leitprogramme, deren Bauskripte unter `scripts/lp/`, `build-seo.py`,
   `build-suchindex.py`, `rechtliches.html`, Doku.
4. Den `localStorage`-Schlüssel **nicht** umbenennen, sonst verlieren die Lernenden ihren
   Stand. Der Notationstrainer behielt beim Umzug `tals-mathe-notationstrainer-v1`.

## 8 · Checkliste

- [ ] Eigene Seite gerechtfertigt (§1), Werkzeug und nicht Simulation
- [ ] `werkzeuge/<name>.html`, ohne Nummer, Einbindungen mit `../`, kein fremder Host
- [ ] `buildNav({ id: 'werkzeuge' })`, `pt-bereich` «WZ · Werkzeuge», Rücklink mit Anker
- [ ] Daten in einer Struktur, jede Lösung in `python3` nachgerechnet
- [ ] Bei gespeichertem Stand: eigener Schlüssel, `try/catch`, Zurücksetzen, Absatz in `rechtliches.html`
- [ ] Kachel in `werkzeuge.html` (je Fach)
- [ ] `build-seo.py` `SEITEN` + zweimal laufen lassen
- [ ] `build-suchindex.py` `ZUSATZSEITEN` + laufen lassen
- [ ] Baustein «🛠 Werkzeug:» im passenden Abschnitt jeder verweisenden Themenseite
- [ ] Selbsttest, sobald gerechnet wird; Pre-Flight `ALLE CHECKS BESTANDEN`; Render-Check 1280/360
