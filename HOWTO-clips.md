# HOWTO — Erklärclip bauen und einbauen

Ein Clip ist eine kurze, stumme Animation, die einen einzelnen Gedankengang Zeile für
Zeile aufbaut — kein Video, sondern eine HTML-Seite von rund 17 kB. Kein MP4, kein
Drittanbieter, scharf auf jedem Bildschirm.

Verwandte Dokumente: `STYLEGUIDE.md` (§5.3.1 keine Drittanbieter), `HOWTO-neue-themenseite.md`,
`CLAUDE.md` (Pre-Flight und Commit-Regel).

---

## Überblick

```
clips/
  <lektion>-<kurzname>.json          ← das Drehbuch. Die einzige Quelle.
  <lektion>-<kurzname>.html          ← generiert
  sprechertext-<lektion>-<kurzname>.txt   ← generiert, wird zum Transkript
  clips.json                         ← generierter Index
  themes/  begreifbar | heft | tafel | papier
  vorlage.json                       ← kommentierte Drehbuch-Vorlage
scripts/build-clips.py               ← Drehbuch  → Clip
scripts/build-clips-einbau.py        ← Clip      → Lektionsseite
```

Von Hand geschrieben wird **nur das Drehbuch**. Alles andere ist erzeugt und wird
mitversioniert, weil GitHub Pages nichts baut.

---

## Schritt 1 — Drehbuch schreiben

`clips/vorlage.json` kopieren nach `clips/<lektion>-<kurzname>.json` und ausfüllen. Alle
Felder, die mit `_` beginnen, sind Kommentare und werden ignoriert — sie dokumentieren
die Formelschreibweise, die Elementtypen und die Farbführung direkt in der Vorlage.

Drei Felder entscheiden über den Einbau:

| Feld | Bedeutung |
|---|---|
| `dateiname` | ohne Endung, ohne Umlaute — daraus werden `.html` und Sprechertext |
| `lektion` | **Liste** von Codes aus `nav.js`, z.B. `["g2-2b", "s2-2a"]` |
| `theme` | `begreifbar` ist Standard und übernimmt die Farben aus `style.css` |

**`lektion` ist eine Liste, auch bei nur einem Eintrag.** Ein Clip gehört oft auf mehrere
Seiten: die Bruchgleichung steht im Grundlagenfach unter `g2-2b` und im Schwerpunktfach
unter `s2-2a`. Ohne Liste müsste man ihn duplizieren, und zwei Kopien laufen auseinander.
Jeder Code muss zu einer `id` in `nav.js` passen — `build-clips-einbau.py` meldet einen
Tippfehler als `[FEHLER]`.

### Formelschreibweise

Kein LaTeX, kein MathJax — der Generator setzt selbst. `[a|b]` ist der Bruch, `x^2` und
`x_1` hoch- und tiefgestellt, `*` wird zum Malpunkt, `-` zum echten Minus, `\R` zu ℝ,
`!=` `<=` `>=` zu ≠ ≤ ≥, `->` `=>` zu ⟶ ⟹. Zwei Leerzeichen bleiben als Abstand stehen.

### Farbführung

`{1:x-2}` färbt einen Term ein — Text und weiche Fläche. Zweck ist ausschliesslich,
denselben Term über mehrere Zeilen hinweg wiedererkennbar zu machen: man sieht, was von
wo nach wo wandert.

**1 und 2 (Blau/Orange) sind das sichere Paar**, auch bei Rotgrünschwäche. Dass Orange
auf den Seiten „Aufgabe" markiert, ist hier kein Widerspruch: im Clip markiert Farbe
einen Term, nicht einen Blocktyp. Sparsam bleiben — ein Bild mit sechs Farben erklärt
nichts mehr.

---

## Schritt 2 — Clip bauen

```sh
python3 scripts/build-clips.py                      # alle
python3 scripts/build-clips.py g2-2b-bruchgleichungen
python3 scripts/build-clips.py g2-2b-bruchgleichungen --eigenstaendig
```

Braucht nur Python 3. Der Lauf gibt die Szenenzeiten aus — daran sieht man sofort, ob
eine Szene zu hetzt oder steht.

`clips.json` wird **fortgeschrieben**, nicht überschrieben: Ein Lauf für einen einzelnen
Clip lässt die übrigen Einträge stehen und entfernt nur solche, deren HTML-Datei nicht
mehr existiert.

Die eigenständige Fassung (rund 480 kB) bettet die Schriften ein und läuft ohne die
Site — für Moodle, zum Verschicken, fürs Archiv. Nicht routinemässig bauen und **nicht
committen**; die Web-Fassung ist die gepflegte.

---

## Schritt 3 — In die Lektionsseite einbauen

Einmal pro Seite die beiden Kommentarzeilen setzen, sinnvollerweise direkt vor
`<h2 id="ressourcen">` — erst die eigenen Clips, dann die fremden Links:

```html
<!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS:ENDE -->
```

Danach:

```sh
python3 scripts/build-clips-einbau.py               # Probelauf
python3 scripts/build-clips-einbau.py --schreiben
```

Das Skript liest `clips/clips.json`, holt die Zuordnung Lektion → Datei aus `nav.js` und
schreibt zwischen die Marker: eine `<h2 id="clips">`-Überschrift (die Seiten-Navigation
nimmt sie automatisch auf) und dann je Clip

```html
<h3 id="clip-<dateiname>" class="clip-h">Titel</h3>
<p class="clip-text">Kurzbeschrieb</p>
<div class="clip" data-clip="…" data-titel="…">
  <button class="clip-start" …>▶ 1:21</button>
</div>
<details class="clip-transkript">…</details>
```

**Die eigene `h3` je Clip ist nicht Schmuck.** `scripts/build-suchindex.py` schneidet an
`h3.clip-h[id]` einen eigenen Abschnitt. Ohne sie heisst in den Suchergebnissen jeder
Clip einer Seite „Clips" und alle führen auf dasselbe Sprungziel. Weil der Titel damit in
der Überschrift steht, trägt der Knopf nur noch das Dreieck und die Dauer — er ist rund
67 × 29 px gross statt einer Karte über die volle Breite. Im Inhaltsverzeichnis der Seite
taucht er nicht auf: `buildToC` nimmt nur `h2`.

**Der Clip wird nicht beim Seitenaufruf geladen.** Sichtbar ist zuerst nur der Knopf;
erst der Klick setzt das `<iframe>` ein (`clipStart` in `mathlib.js`). So läuft bei
mehreren Clips auf einer Seite keiner von selbst los, und die Seite lädt nicht N
zusätzliche Dokumente mit. Der Clip startet dann von selbst — er ist frisch eingesetzt,
sein Autostart ist genau richtig.

**Und er lässt sich wieder einklappen.** Über dem Rahmen steht „✕ Clip schliessen"
(`clipStop`); das entfernt das `<iframe>`, der Clip hält an, gibt den Platz frei, und der
Knopf kommt zurück. Ein zweiter Klick startet ihn von vorn.

Jede Seite mit einem Clip-Block **muss `mathlib.js` einbinden.** Themenseiten tun das
ohnehin.

---

## Schritt 4 — Verifikation

1. **Pre-Flight** über die geänderten Lektionsseiten, wie immer vor dem Commit.
2. **Im Browser bei 1280 und 360 px**: Karte sichtbar, Klick lädt den Clip, Rahmen im
   richtigen Verhältnis, Bedienleiste ohne Überlauf. Auf schmalen Schirmen blendet der
   Clip die Tastaturhinweise aus — dort gibt es weder Leertaste noch Pfeiltasten.
3. **Netzwerk-Tab**: keine Anfrage an einen fremden Host. Der Clip zieht die Schriften
   per `@import url("../schriften.css")` aus dem Repo.
4. **Transkript vorhanden und lesbar.** Fehlt der Sprechertext, meldet das
   Einbau-Skript `[WARN]` und lässt den Block weg.

---

## Häufige Stolpersteine

**Der Clip liegt eine Ebene unter der Wurzel — und das ist nicht frei wählbar.** Er zieht
die Schriften per `@import url("../schriften.css")`. Verschiebt man `clips/` tiefer, sind
die Schriften weg, ohne dass etwas bricht: die Seite fällt still auf Georgia zurück.

**Das Transkript ist nicht Beiwerk.** Von einem animierten Clip sieht eine Suchmaschine
gar nichts, und die Volltextsuche der Site ebenso wenig. Der Transkriptblock trägt darum
die Klasse `clip-transkript`, und die darf **nicht** in `SKIP_CLASSES` von
`scripts/build-suchindex.py` landen — sonst ist der Clip inhaltlich unsichtbar.

**Nach jedem Drehbuch-Edit beide Skripte laufen lassen**, erst `build-clips.py`, dann
`build-clips-einbau.py`. Das zweite liest nur `clips.json` und baut selbst nichts; ohne
den ersten Lauf steht in der Seite die alte Dauer und der alte Kurzbeschrieb.

**`build-seo.py` danach**, damit `dateModified` und die Sitemap stimmen. Der Pre-Flight
warnt, wenn es fehlt.

**Brüche funktionieren nur in Formel-Elementen, nicht in Prosa.** `formel`, `karte` und
`box` schicken ihren ganzen Text durch `formel()` — dort wird `[a|b]` zum Bruch. Die
Prosa-Typen `text`, `notiz`, `titel`, `untertitel`, `aussage` und `liste` gehen dagegen
durch `text_html`, und das ersetzt `|` **zuerst** durch einen Zeilenumbruch, bevor es die
`@…@`-Abschnitte auswertet. Aus `@x = [b|a]@` wird darum kein Bruch, sondern eine
umgebrochene eckige Klammer — ohne Fehlermeldung, es sieht nur falsch aus. Wer in einer
Merkzeile einen Bruch braucht, macht daraus ein eigenes `formel`-Element.

**`liste` wird nicht zentriert.** Der Typ bekommt die Klassen `l sans`, aber kein `mitte`
— der Block läuft über die volle Bühnenbreite und beginnt am linken Rand, auch im Layout
`zentriert`. In einer sonst mittigen Szene wirkt das wie ein Versehen. Für aufgezählte
Merkpunkte in der Mitte drei `formel`-Zeilen nehmen; die tragen `row` und sitzen zentriert.

**Eine gehaltene Ankerzeile belegt die oberste Zeile — Folgeszenen müssen tiefer
beginnen.** Steht auf einem Element `halten`, bleibt es über die folgenden Szenen stehen.
Deren `oben` muss dann unter der Ankerzeile liegen, sonst rendern beide übereinander und
die Formeln stehen ineinander. Bewährt: die einführende Szene auf `oben: 178`, alle
Folgeszenen auf `oben: 348`. Beide bestehenden Clips machen es so.

---

## Bibliotheksseite `clips.html`

Die Übersicht über alle Clips, gruppiert nach Fach und darin nach Lerngebiet. Sie ist
**nicht** von Hand gepflegt: `build-clips-einbau.py` füllt auch dort einen Block,

```html
<!-- CLIPS-BIBLIOTHEK:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS-BIBLIOTHEK:ENDE -->
```

und schreibt je Clip dieselbe Startkarte wie auf der Lektionsseite, dazu die Verweise
„Im Zusammenhang" auf alle Seiten aus `lektion` (Nummer und Titel kommen aus `nav.js`)
und das Transkript. Ein neuer Clip erscheint dort also automatisch, sobald sein Drehbuch
gebaut ist.

Angebunden ist die Seite an drei Stellen — die sind schon gesetzt und müssen für neue
Clips nicht angefasst werden:

| Datei | was |
|---|---|
| `nav.js` | Eintrag `▶ Clips` im Menü *Nachschlagen*, in der Kopfzeile und im Mobilmenü |
| `scripts/build-seo.py` | Zeile in der `SEITEN`-Tabelle — Beschreibung, canonical, Sitemap |
| `scripts/build-suchindex.py` | `clips.html` in der Liste der Nachschlagewerke |

Die Clip-Dateien selbst stehen bewusst **nicht** in der Sitemap: ohne Seitengerüst,
Navigation und Fussbereich wären sie als Landeseite aus einer Suche eine Sackgasse.
Indexiert werden `clips.html` und die Lektionsseite — beide tragen das Transkript.

---

## Pre-Flight

Clips werden mitgeprüft, wenn man sie übergibt:

```sh
python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html clips/*.html clips.html
```

Auf den Clip-Bühnen laufen nur die allgemeinen Checks (Tag-Bilanz, doppelte IDs, kein ß,
Dezimalpunkt, keine Fremdhosts) — Skelett-, nav- und Ressourcen-Checks gelten für sie
nicht, sie haben kein Seitengerüst.

Dazu kommt eine Konsistenzprüfung der Ablage, die immer läuft:

- jeder `clips.json`-Eintrag hat eine Datei → sonst `[FEHLER]` (toter Knopf in der Bibliothek)
- jede Datei steht in `clips.json` → sonst `[FEHLER]` (fehlt lautlos in der Bibliothek)
- jedes `lektion`-Kürzel existiert in `nav.js` → sonst `[FEHLER]` (landet auf keiner Seite)
- Sprechertext vorhanden → sonst `[WARN]` (die Seite bekommt kein Transkript)

---

## Noch offen

Die Mechanik steht. Was noch fehlt, ist Inhalt und der Übertrag:

- **Mehr Clips.** Bisher gibt es drei, alle im Lerngebiet 2. Sie sind zugleich die
  Referenz dafür, wie ein Drehbuch aussieht: `g2-2b-bruchgleichungen` für eine
  Schritt-für-Schritt-Herleitung, `g2-2a-parametergleichung` für eine mit Bedingung,
  `g2-2a-parametergleichung-drei-faelle` für eine Fallunterscheidung.
- **Übertrag nach TALS Physik** — vermerkt in `TODO-schwesterprojekt.md`.
