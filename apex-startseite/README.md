# Startseite für `begreifbar.ch`

Der Ordnerinhalt ist die **komplette** Website für den Apex — ohne
Abhängigkeiten ins Mathe-Repo und ohne Drittanbieter. Er gehört in ein **eigenes**
Repository, weil GitHub Pages eine Domain an genau ein Repo bindet und
`mathe.begreifbar.ch` bereits an *TALS-Mathe* hängt.

Hier liegt er nur zur Aufbewahrung und Versionierung; ausgeliefert wird er aus
**`go4exercises/begreifbar`**. Das Repo steht, Pages baut aus `main` / Wurzel,
`CNAME` = `begreifbar.ch`, Enforce HTTPS ist an. Siehe `DOMAIN-UMZUG.md`, Phase 4.

> ⚠️ **Dieser Ordner ist die Quelle, nicht die Auslieferung — und die beiden laufen
> auseinander.** Es gibt keinen Automatismus und keinen lokalen Klon des Apex-Repos.
> Wer hier etwas ändert, muss es von Hand hinüberbringen, sonst bleibt live der alte
> Stand. Stand 31.8.2026 hinkt die Live-Seite zwei Änderungen hinterher: lokale
> Schriften und das neue Kachel-Layout.

## Inhalt

| Datei | Zweck |
|---|---|
| `index.html` | die Startseite, CSS inline |
| `schriften.css` + `schriften/` | die drei Schriften, lokal ausgeliefert — eigene Kopie, weil dieser Ordner nicht auf die Wurzel des Mathe-Repos zugreifen kann |
| `CNAME` | `begreifbar.ch` — eine Zeile, LF, kein BOM |
| `favicon.svg` | Platzhalter-Zeichen: zwei Balken in Mathe-Blau und Physik-Bernstein |
| `.nojekyll` | schaltet die Jekyll-Verarbeitung ab, wie im Mathe-Repo |

## Aktualisieren (der Normalfall)

Einmalig einen Klon anlegen, danach je Änderung drei Zeilen:

```sh
gh repo clone go4exercises/begreifbar ~/begreifbar        # einmalig
cd ~/begreifbar
rsync -a --delete --exclude '.git' --exclude 'README.md' ~/tals-mathe/apex-startseite/ .
git add -A && git commit -m "…" && git push
```

`--delete` räumt weg, was hier nicht mehr steht; `--exclude 'README.md'` lässt diese
Anleitung im Mathe-Repo, sie gehört nicht auf die Website.

**`--exclude '.git'` ist nicht optional.** Ohne den Ausschluss löscht `--delete` das
Verzeichnis `.git` im Klon — es kommt in der Quelle ja nicht vor. Der Klon wäre damit
kein Repository mehr, und der Commit ginge verloren.

**Danach prüfen:** `curl -s https://begreifbar.ch/ | grep -c googleapis` muss `0`
ergeben, und im Netzwerk-Tab darf keine Anfrage an einen fremden Host stehen.

## Aufsetzen (erledigt, zur Dokumentation)

1. Repository anlegen, z. B. `go4exercises/begreifbar`, öffentlich.
2. Den **Inhalt** dieses Ordners ins Repo-Wurzelverzeichnis kopieren, `schriften/`
   eingeschlossen — nicht den Ordner selbst, sonst liegt `index.html` eine Ebene zu tief und Pages liefert 404.
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

## Ein Fach dazunehmen

`scripts/neue-subdomain.py` im Mathe-Repo macht den ganzen Weg von der ZIP-Datei
bis zur fertigen Kachel:

```bash
python3 scripts/neue-subdomain.py chemie ~/Downloads/chemie.zip \
    --titel Chemie --marke Grundlagenfach --farbe gruen \
    --text "Stoffe, Reaktionen und Stöchiometrie — mit Rechenweg."
```

Es packt das ZIP aus, legt `CNAME` und `.nojekyll` an, wartet auf den
DNS-Eintrag, erstellt das Repository, schaltet Pages ein, erzwingt HTTPS, hängt
die Kachel hier ein und pusht das Apex-Repo. Mit `--nur-pruefen` läuft alles bis
zum Auspacken, ohne etwas anzulegen.

Eine **einzelne Seite** geht genauso — dann ohne Kachel, weil sie nicht ins
Fächer-Verzeichnis gehört:

```bash
python3 scripts/neue-subdomain.py sonnenfinsternis ~/sonnenfinsternis.html --ohne-kachel
```

Die Datei wird zu `index.html`; verweist sie auf Bilder oder CSS daneben, meldet
das Skript die Fundstellen — dann entweder alles einbetten oder ein ZIP übergeben.

Die Kacheln stehen zwischen `<!-- FAECHER:ANFANG -->` und `<!-- FAECHER:ENDE -->`,
die Fachfarben zwischen `<!-- FACHFARBEN:ANFANG -->` und `<!-- FACHFARBEN:ENDE -->` —
das Skript schreibt genau dorthin. Von Hand geht es genauso: eine Kachel kopieren,
Klasse `f-<fach>` vergeben und eine Farbzeile ergänzen.

Das Raster ist auf `repeat(auto-fit, minmax(320px, 1fr))` gestellt und trägt zwei
Fächer so gut wie fünf. **Was nicht mitwächst, ist die Prosa:** Überschrift,
Seitentitel und Beschreibung nennen Mathematik und Physik namentlich und sprechen
von «zwei Lehrmitteln». Ab dem dritten Fach gehört das nachgezogen — das Skript
listet beim Einfügen die betroffenen Zeilen auf.

## Pflege

Die Seite nennt beide Fächer, aber keine Kapitel — sie muss also nicht
mitwachsen, wenn in Mathe oder Physik Teilgebiete dazukommen. Zu ändern ist sie
nur, wenn ein Fach dazukommt, eine Adresse wechselt oder die Fachbeschreibung
nicht mehr stimmt.

Genau darum ist der Auslieferungs-Schritt die eigentliche Fehlerquelle: Weil hier
selten etwas passiert, ist beim nächsten Mal vergessen, dass es ihn überhaupt gibt.
Wer diesen Ordner anfasst, hat erst die Hälfte getan — der Abschnitt
**Aktualisieren** oben ist die andere.
