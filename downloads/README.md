# Downloads

Hier liegen die Materialien zum Herunterladen oder Drucken, sortiert nach Bereich und Thema.

## Standard-Dateien pro Thema

Jeder Themen-Unterordner enthält fünf Dateien. Vier davon sind **HTML-Druckseiten** mit eingebautem Druck-Stylesheet (`print.css`); sie öffnen sich im Browser, lassen sich direkt ausdrucken oder als PDF speichern. Das Anki-Deck ist ein Download.

| Datei | Format | Inhalt |
|---|---|---|
| `handout.html` | HTML-Druckseite | Theorie-Zusammenfassung zum Mitnehmen |
| `formelauszug.html` | HTML-Druckseite | Kompakte Formelübersicht (nicht zu verwechseln mit Promath/SBFI) |
| `teste-dich-selbst.html` | HTML-Druckseite | Selbsttest mit Grundlagenaufgaben und Lösungen |
| `aufgabenserie.html` | HTML-Druckseite | Anwendungsaufgaben mit Diagrammen und Musterlösungen |
| `ankideck.apkg` | Anki | Karteikarten für Spaced Repetition |

## Struktur

```
downloads/
├── print.css                                ← gemeinsames Druck-Stylesheet (A4)
├── diagram.js                               ← SVG-Helper für Achsenkreuze
├── grundlagen/
│   ├── g3-2-lineare-funktionen/
│   │   ├── handout.html
│   │   ├── formelauszug.html
│   │   ├── teste-dich-selbst.html
│   │   ├── aufgabenserie.html
│   │   ├── ankideck.apkg
│   │   └── README.md
│   └── …
└── schwerpunkt/
    └── …
```

## Hinweis

Solange ein Thema noch nicht „verfügbar" ist, gibt es im entsprechenden Themen-Ordner keine Materialien. Die Themenseite zeigt in diesem Fall nur den Hinweis „Wird ergänzt." statt einer Download-Kachel-Galerie — es entstehen also keine 404-Links.
