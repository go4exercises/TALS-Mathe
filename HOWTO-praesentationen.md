# HOWTO — Präsentationen

**Gilt seit 23.11.2026.** Wann ein Foliensatz eine Präsentation unter `praesentationen/` wird, wie er
eingebaut und mit den Themenseiten verbunden wird. Die Gegenstücke sind `HOWTO-simulationen.md` und
`HOWTO-werkzeuge.md`; alle drei sind gleich gegliedert. Bei Widerspruch gilt `STYLEGUIDE.md` (§6.6).

Präsentationen werden **extern gebaut** und hier mit wenig Eingriff übernommen, nach dem Grundsatz von
`HOWTO-werkzeuge.md` §9: eigenes Aussehen, sonst die Regeln der Site.

**Vorbilder:** `praesentationen/sinussatz-cosinussatz.html` (mit Rechenkern und Selbsttest),
`praesentationen/rechtwinkliges-dreieck.html` (feste Aufgaben, Farbmakros in MathJax).

---

## 1 · Wozu und Abgrenzung

| | wer führt | wo | Beispiel |
|---|---|---|---|
| **Simulation** | die Lernenden beobachten und verändern ein Modell | `simulationen/` | Standardabweichung |
| **Werkzeug** | die Lernenden üben oder rechnen mit eigenen Daten | `werkzeuge/` | Systemtrainer |
| **Präsentation** | die Lehrperson führt Folie für Folie durch ein Thema | `praesentationen/` | Sinussatz und Cosinussatz |

Kennzeichen einer Präsentation: feste Folien im Format 16:9, Schritte mit Pfeiltaste oder Leertaste,
Vollbild, gedacht für den Beamer. Interaktive Teile (Punkt ziehen, Regler) dürfen vorkommen. Sie
ersetzen aber nicht die Animation auf der Themenseite.

**Nicht fürs Handy.** Die Folie ist eine feste Bühne von 1600 × 900 px, die auf den Bildschirm skaliert
wird. Bei 360 px Breite wird die Schrift unlesbar. Das ist so gewollt und wird nicht «repariert». Die
Übersicht sagt es den Lernenden.

## 2 · Ablage und Name

- `praesentationen/<name>.html`, Kleinbuchstaben mit Bindestrich, **ohne Nummer**
  (`sinussatz-cosinussatz.html`).
- Die externe Originaldatei kommt **nicht** ins Repo. Für den Vergleich liegt sie im Scratchpad;
  die Commit-Nachricht zählt auf, was angepasst wurde.

## 3 · Seitenaufbau

Der ganze Foliensatz bleibt, wie er ist: eigenes `<style>`, eigene Navigationsleiste, eigene Folien.
Angepasst werden nur die Punkte hier.

- **Kopf:** `<html lang="de-CH">`. Die leeren SEO-Marken wörtlich aus einem Vorbild kopieren, Google
  Fonts durch `<link rel="stylesheet" href="../schriften.css">` ersetzen (Source Sans 3, Source Serif 4,
  JetBrains Mono und Caveat sind vorhanden). **Kein fremder Host.**
- **Footer:** die leeren FUSS-Marken nach der Navigationsleiste (`</nav>`). Weil `style.css` fehlt,
  kommen diese Zeilen ins eigene `<style>`. Sie halten den Footer einzeilig, und im Vollbild verschwindet er:
  ```css
  .site-footer{flex:none;color:#9aa3b8;font-size:11px;line-height:1.5;text-align:center;padding:0 16px 6px}
  .site-footer p{display:inline;margin:0 .45em}.site-footer a{color:inherit}
  html:fullscreen .site-footer{display:none}
  ```
- **Rücklink** auf der Titelfolie, als Satz unter dem Tastenhinweis, mit Anker auf den Abschnitt:
  `Der Stoff dazu steht in <a href="../grundlagen/…html#abschnitt">5.3 …</a>.` Dazu
  `.stage a{color:inherit}`. In der Tastensteuerung `e.target.matches('button,a')`, damit Enter
  auf dem Link dem Link folgt und nicht weiterblättert.
- **MathJax** statt Formeln aus HTML (`a²`, `sin α`, Bruch-Spans). Einstellung vor
  `../vendor/mathjax/tex-svg.js`:
  ```js
  window.MathJax={loader:{load:['[tex]/boldsymbol','[tex]/color']},
    tex:{packages:{'[+]':['boldsymbol','color']},inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']],
         macros:{B:['\\boldsymbol{#1}',1], ca:['{\\color{##1c6fb8}{#1}}',1]}},
    svg:{fontCache:'local'},options:{enableMenu:false},startup:{typeset:false}};
  ```
  - `startup:{typeset:false}`: Die Folien entstehen erst im Skript. Gesetzt wird danach, in einem Zug.
  - **Erweiterungen vorladen** (`loader.load`). `MathJax.tex2svg` arbeitet synchron und kann eine
    Erweiterung nicht nachladen. Fehlt sie, bleibt die Formel roh stehen.
  - **Farben in Makros mit `##`**: `{\\color{##1c6fb8}{#1}}`. Ein einfaches `#1c6fb8` liest
    MathJax als Parameter `#1` («Illegal macro parameter reference»). Das Modell `[HTML]` kennt MathJax 3
    nicht.
  - `fontCache:'local'`: Jede Formel trägt ihre Glyphen selbst. Das ist nötig, weil `mjHTML` die SVG als
    Text einsetzt.
- **Formeln, die das Skript erst setzt** (Live-Anzeigen, Werte der Regler, Rechenwege), gehen durch
  `mjHTML(el, html)`. Die Funktion ersetzt jedes `\(…\)` im Text durch die SVG von `MathJax.tex2svg`.
  Vor dem Start von MathJax schreibt sie den Text roh und merkt sich das Element; beim Start wird alles
  nachgesetzt. Vorlage aus `rechtwinkliges-dreieck.html` kopieren (mit Abbruch, wenn sich nichts
  geändert hat: Das spart bei Tweens 60 Neusetzungen je Sekunde). Am Ende des Skripts:
  ```js
  {const zeigen=()=>document.body.classList.add('mj');
    if(window.MathJax&&MathJax.startup&&MathJax.startup.promise){
      MathJax.startup.promise.then(()=>{MJ=true;MJ_EL.forEach(el=>mjHTML(el,el._mj));return MathJax.typesetPromise([deck])})
        .catch(e=>console.error(e)).finally(zeigen)}
    else zeigen();
    setTimeout(zeigen,4000)}
  ```
  Dazu `body:not(.mj) #deck{visibility:hidden}`, damit beim Laden kein rohes TeX aufblitzt.
- **TeX in JS-Strings mit doppeltem Backslash**: `'\\(\\alpha\\)'`. Ein einfacher Backslash vor `;`, `,`,
  `!` oder `:` verschwindet still: Aus `\;` wird `;`, und das ist gültiges TeX. Der Selbsttest (§6) sucht
  danach.
- **Fallen im CSS des Originals:**
  - Regeln wie `.karte svg{height:280px}` oder `.fig svg{width:860px;height:640px}` gelten auch für die SVGs von
    MathJax. Auf das gemeinte Element einschränken (`.karte>svg`, `.fig>svg`).
  - Text in `<option>` kann MathJax nicht setzen: In Auswahllisten bleibt Klartext (`sin φ`), auf der Folie
    steht dieselbe Angabe in TeX (Muster `t`/`tt` in `einheitskreis.html`).
  - Ist ein Container `display:flex` mit `gap` (Bedienleiste `.ctl`), wird jede Formel ein eigenes
    Flex-Element mit Abstand. Den Text in ein `<span>` fassen.
- **Beschriftungen in Figuren** (SVG-`<text>`, Canvas) bleiben Text mit `α`, `²`, `·`, wie in den
  Animationen der Themenseiten. Eine Meldung, die in der Figur *und* im Text steht, wird einmal mit
  `\(…\)` geschrieben und für die Figur umgewandelt (Muster `klartext()` in `sinussatz-cosinussatz.html`).
- **Notation** wie sie der Auftraggeber geliefert hat. Weicht sie von der Themenseite ab, wird das in
  `praesentationen/CLAUDE.md` vermerkt, nicht angeglichen (Entscheid vom 23.11.2026 zu SsW/sSw/SWW).
- **Kein Karoraster** auf den Folien (Entscheid vom 23.11.2026): Die `background-image`-Zeilen mit dem
  Raster in `.stage` entfernen, die Papierfarbe bleibt.
- **Farben** behalten ihre Bedeutung (STYLEGUIDE §5). Getauscht wird nur eine umgedeutete Farbe, etwa
  Rot für einen der beiden Sätze im Überblick.
- **Rechnung** zwischen `// ── KERN:ANFANG` und `// ── KERN:ENDE`, ohne DOM, sobald die Präsentation
  aus Eingaben rechnet (Fallauswahl, Regler mit Rechenweg). Feste Aufgaben brauchen keinen Kern, aber
  jede Lösung wird vor dem Einbau mit `python3` nachgerechnet.

## 4 · Eintragen

Eine Präsentation hängt an vier Stellen:

1. **Übersicht** `praesentationen.html`, zwischen `<!-- PRAESENTATIONEN:ANFANG -->` und
   `<!-- PRAESENTATIONEN:ENDE -->`: eine Kachel nach Fach und Themenbereich, wie in `simulationen.html`,
   der Link mit `target="_blank" rel="noopener"` und `aria-label="Präsentation … (öffnet in neuem Fenster)"`.
2. **`scripts/build-seo.py`**, Tabelle `SEITEN`: `'praesentationen/<name>.html'`, `typ='article'`,
   `lrt='Präsentation'`, Beschreibung 140–165 Zeichen, `ort='Präsentationen · <Titel>'`. Dann
   `python3 scripts/build-seo.py`, nach dem Commit ein zweites Mal.
3. **`scripts/build-suchindex.py`**, Liste `ZUSATZSEITEN`: `('praesentationen/<name>.html', 'PRÄ',
   '<Titel>', 'thema')`. Dann `python3 scripts/build-suchindex.py`.
4. **Themenseite**, siehe §5.

Dazu ein Absatz in **`praesentationen/CLAUDE.md`**: Inhalt, Folien, Besonderheiten, Abweichungen.

## 5 · Verlinken in der Themenseite

Im Abschnitt, zu dem die Präsentation gehört, mit dem Baustein (Wortlaut fest):

```html
<div class="block block-tipp" style="margin-top:10px">
  <div class="block-titel">📽 Präsentation: Sinussatz und Cosinussatz</div>
  <p>Ein Satz, was der Foliensatz zeigt. <a href="../praesentationen/sinussatz-cosinussatz.html" target="_blank" rel="noopener">Zur Präsentation (neues Fenster) →</a></p>
</div>
```

Nicht am Seitenanfang, nicht auf den Kacheln von `index.html`. Deckt der Foliensatz mehrere
Themenseiten ab, bekommt jede ihren Baustein.

## 6 · Prüfen

- **Pre-Flight** über die Präsentation und jede geänderte Themenseite. `praesentationen/` ist vom
  Skelett-Check ausgenommen, alle anderen Checks laufen (ß, Dezimalkomma, fremde Hosts …).
  `check_sim_wz` prüft Kachel, Verweise und Rücklink-Anker.
- **`scripts/verify_praesentationen.js`** (im Pre-Flight, für alle Präsentationen): lädt jede Seite in
  jsdom, drückt jeden Knopf, stellt jeden Regler auf Minimum, Mitte und Maximum, blättert alle Schritte
  durch und setzt jedes `\(…\)`, das dabei entsteht, mit `mathjax-full`, mit den Makros der Seite.
  Meldet Laufzeitfehler, MathJax-Fehler, `undefined`/`NaN`, Dezimalkomma und einfache Backslashes im
  Skript. Nötig, weil `verify_mathjax.js` `<script>` überspringt und eine Präsentation fast alle Formeln
  im Skript hat.
- **Eigener Selbsttest** `scripts/verify_<name>.js`, sobald ein Kern rechnet, mit Gegenrechnung in
  `python3` auf einem *anderen* Weg (Muster `verify_sinussatz-cosinussatz.js`: Dreieck aus Koordinaten
  konstruieren statt Sinus- und Cosinussatz). In die Liste der Selbsttests in `preflight.py` aufnehmen.
  Einmal absichtlich einen Fehler einbauen und sehen, dass der Test anschlägt.
- **Im Browser** bei 1280 × 800 jede Folie im letzten Schritt ansehen: Lädt MathJax ohne 404, bleibt kein
  rohes `\(` stehen, passt jede Formel in ihren Kasten? Die Bilder ansehen; ein Prüfer sieht
  Überlappung, aber nicht, ob eine Formel riesig geraten ist.

## 7 · Verschieben und Umbenennen

Wie `HOWTO-werkzeuge.md` §7: `git mv`, alte Adresse in `404.html` (`WEITERLEITUNGEN`), alle Verweise
umstellen.

## 8 · Checkliste

- [ ] Präsentation, nicht Simulation oder Werkzeug (§1)
- [ ] `praesentationen/<name>.html`, `lang="de-CH"`, SEO- und FUSS-Marken, Footer-CSS, `../schriften.css`, kein fremder Host
- [ ] MathJax-Einstellung mit vorgeladenen Erweiterungen, `mjHTML` für Skript-Texte, Start am Skriptende, keine Formel mehr als HTML
- [ ] CSS-Fallen: `svg`-Regeln eingeschränkt, Formeln in Flex-Leisten in `<span>`; Karoraster entfernt
- [ ] Rücklink mit Anker auf der Titelfolie, Enter auf Links
- [ ] Lösungen in `python3` nachgerechnet; bei Rechenkern: `KERN`-Marken und eigener Selbsttest im Pre-Flight
- [ ] Kachel in `praesentationen.html`, `build-seo.py` (zweimal laufen lassen), `build-suchindex.py`
- [ ] Baustein «📽 Präsentation:» im Abschnitt jeder Themenseite, mit `target="_blank"`
- [ ] Absatz in `praesentationen/CLAUDE.md`
- [ ] Pre-Flight `ALLE CHECKS BESTANDEN`, jede Folie im Browser angesehen
