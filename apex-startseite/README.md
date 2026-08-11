# Startseite für `begreifbar.ch`

Der Ordnerinhalt ist die **komplette** Website für den Apex — eine einzelne
HTML-Datei ohne Abhängigkeiten ins Mathe-Repo. Er gehört in ein **eigenes**
Repository, weil GitHub Pages eine Domain an genau ein Repo bindet und
`mathe.begreifbar.ch` bereits an *TALS-Mathe* hängt.

Hier liegt er nur zur Aufbewahrung und Versionierung; ausgeliefert wird er aus
dem neuen Repo. Siehe `DOMAIN-UMZUG.md`, Phase 4.

## Inhalt

| Datei | Zweck |
|---|---|
| `index.html` | die Startseite, CSS inline, keine externen Dateien ausser Google Fonts |
| `CNAME` | `begreifbar.ch` — eine Zeile, LF, kein BOM |
| `favicon.svg` | Platzhalter-Zeichen: zwei Balken in Mathe-Blau und Physik-Bernstein |
| `.nojekyll` | schaltet die Jekyll-Verarbeitung ab, wie im Mathe-Repo |

## Aufsetzen

1. Repository anlegen, z. B. `go4exercises/begreifbar`, öffentlich.
2. Den **Inhalt** dieses Ordners ins Repo-Wurzelverzeichnis kopieren — nicht den
   Ordner selbst, sonst liegt `index.html` eine Ebene zu tief und Pages liefert 404.
   Diese `README.md` braucht es dort nicht.
3. Pushen.
4. **Settings → Pages**: Source auf `Deploy from a branch`, Branch `main`, Ordner `/ (root)`.
   Unter *Custom domain* sollte `begreifbar.ch` bereits aus der `CNAME`-Datei stehen.
5. Warten, bis GitHub das Zertifikat ausgestellt hat (bis zu 24 h), dann
   **Enforce HTTPS** anhaken.

Die DNS-Einträge stehen schon (Phase 1): vier A- und vier AAAA-Records am Apex,
`www` als CNAME. Es fehlt ausschliesslich das Repo, das die Domain beansprucht.

**Solange das nicht gemacht ist, zeigen `begreifbar.ch` und `www.begreifbar.ch`
eine Zertifikatswarnung** — die Namen lösen bereits auf GitHub Pages auf, aber
kein Repo beansprucht sie, also liefert GitHub das Platzhalter-Zertifikat
`CN=*.github.io` aus und dahinter eine 404.

### `www` mitnehmen

Ein Pages-Repo bedient entweder `begreifbar.ch` **oder** `www.begreifbar.ch`.
Trägt man den Apex als Custom domain ein, leitet GitHub `www` automatisch
dorthin um, sofern der CNAME-Eintrag steht — das ist hier der Fall. Nach dem
Aufsetzen einmal `curl -I https://www.begreifbar.ch/` prüfen.

## Was bewusst nicht drin ist

- **Kein `og:image`.** Ein Vorschaubild müsste diese Seite zeigen, nicht eines
  der beiden Fächer; `og-bild.png` aus dem Mathe-Repo trägt «Mathe begreifbar»
  und wäre hier falsch. Link-Vorschauen zeigen vorerst nur Titel und Text. Wenn
  du eines willst: `.claude/tools/build-bilder.mjs` im Mathe-Repo ist die
  Vorlage, dort ist der Aufbau in ~40 Zeilen HTML beschrieben.
- **Kein eigenes Impressum.** Fusszeile und Rechtliches verweisen auf
  `mathe.begreifbar.ch`, damit der Text nur an einer Stelle gepflegt wird und
  nicht auseinanderläuft. Wenn der Apex später eigenständig wirken soll, gehört
  eine eigene `rechtliches.html` dazu.
- **Das Favicon ist ein Platzhalter** — zwei Balken in den Fachfarben, kein
  gestaltetes Zeichen. Es funktioniert bei 16 px und passt ins Farbsystem, mehr
  nicht.

## Pflege

Die Seite nennt beide Fächer, aber keine Kapitel — sie muss also nicht
mitwachsen, wenn in Mathe oder Physik Teilgebiete dazukommen. Zu ändern ist sie
nur, wenn ein Fach dazukommt, eine Adresse wechselt oder die Fachbeschreibung
nicht mehr stimmt.
