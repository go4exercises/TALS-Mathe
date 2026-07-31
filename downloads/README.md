# Downloads

Hier liegen die Materialien zum Herunterladen oder Drucken, sortiert nach Bereich und Thema.

## Standard-Dateien pro Thema

Jeder Themen-Unterordner enthält vier Dateien. Drei davon sind **HTML-Druckseiten** mit eingebautem Druck-Stylesheet (`print.css`); sie öffnen sich im Browser, lassen sich direkt ausdrucken oder als PDF speichern. Das Anki-Deck ist ein Download.

| Datei | Format | Inhalt |
|---|---|---|
| `handout.html` | HTML-Druckseite | Theorie-Zusammenfassung zum Mitnehmen |
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
│   │   ├── teste-dich-selbst.html
│   │   ├── aufgabenserie.html
│   │   ├── ankideck.apkg
│   │   └── README.md
│   └── …
└── schwerpunkt/
    └── …
```

## Hinweis

Seit Juli 2026 sind alle Themenseiten beider Bereiche verfügbar — jeder Themen-Ordner enthält den vollen Materialsatz. Die Regel für künftige neue Seiten bleibt: Solange ein Thema noch nicht „verfügbar" ist, gibt es im entsprechenden Themen-Ordner keine Materialien; die Themenseite zeigt dann nur den Hinweis „Wird ergänzt." statt einer Download-Kachel-Galerie — es entstehen also keine 404-Links.
