# Umzug auf `begreifbar.ch`

Vorgehen für den Wechsel von `go4exercises.github.io/TALS-Mathe/` auf eine eigene
Domain, die beide Lehrmittel trägt und für die geplanten Erweiterungen
(Passerelle, eidgenössische Maturitätsprüfung, Ausrichtung GS) offen bleibt.

**Stand: 10. August 2026.** Diese Datei ist die Arbeitsanleitung — abgehakt wird hier.
Phasen 0–2 sind erledigt und nachgemessen; Phase 3 läuft. Der Ist-Zustand steht
jeweils unter der Phase.

---

## Rollen

| Zeichen | Bedeutung |
|---|---|
| 🔑 | **Nur du.** Braucht Konto, Zahlung oder Zugriff, den ich nicht habe. |
| 🤖 | **Ich.** Reine Repo-Arbeit, läuft lokal, endet mit einem Commit. |
| 🤝 | **Zusammen.** Ich bereite vor, du bestätigst oder klickst. |

Ich pushe grundsätzlich nicht — jeder Push bleibt bei dir (`CLAUDE.md`).

---

## Zielbild

```
begreifbar.ch              →  Startseite, zeigt auf beide Fächer   (neues Mini-Repo)
mathe.begreifbar.ch        →  Repo TALS-Mathe
physik.begreifbar.ch       →  Repo TALS-Physik
```

**Warum Subdomains und nicht Unterordner:** GitHub Pages bindet eine Domain an
*genau ein* Repository (offizielle Doku, geprüft am 3.8.2026). Zwei Repos unter
einer Domain gehen deshalb nur über Subdomains. Der Fach-Schnitt oben ist auch
inhaltlich richtig: Der Abschluss (BM-Grundlagen, BM-Schwerpunkt, Passerelle,
eidg. Matur) gehört *innerhalb* eines Fachs, sonst müsstest du denselben Stoff
mehrfach führen — Kombinatorik für GS und für die Passerelle ist grösstenteils
derselbe Inhalt in anderer Tiefe.

**Der Name liest sich als Satz:** `mathe.begreifbar.ch` = «Mathe begreifbar».

---

## Phase 0 · Domain kaufen

- [x] 🔑 `begreifbar.ch` registrieren (Anbieter siehe unten). Am 3.8.2026 frei —
      per RDAP geprüft, aber **vor dem Kauf nochmals prüfen**, Domains gehen schnell weg.
- [ ] 🔑 Optional als Weiterleitung dazu: `matura-lernen.ch` (ebenfalls frei).
      Ein Markenname bringt keine Suchtreffer mit; eine beschreibende Domain,
      die nur umleitet, fängt das auf.
      **Offen** — bewusst zurückgestellt, nicht Teil des Umzugs.
- [x] 🔑 Beim Kauf **Auto-Renew einschalten.** Eine abgelaufene Domain ist der
      teuerste Fehler in dieser ganzen Liste.

> **Ist-Zustand (10. August 2026):** `begreifbar.ch` ist bei **Infomaniak**
> registriert, **Auto-Renew aktiv**.

---

## Phase 1 · DNS setzen

Beim Registrar in der DNS-Verwaltung. Die Werte stammen aus der GitHub-Doku
(geprüft am 3.8.2026) — vor dem Eintragen einmal gegenlesen, GitHub ändert sie
selten, aber nicht nie.

- [x] 🔑 **Apex `begreifbar.ch`** — vier A-Records:
      `185.199.108.153` · `185.199.109.153` · `185.199.110.153` · `185.199.111.153`
- [x] 🔑 **Apex, IPv6** — vier AAAA-Records:
      `2606:50c0:8000::153` · `2606:50c0:8001::153` · `2606:50c0:8002::153` · `2606:50c0:8003::153`
- [x] 🔑 **`mathe`** — CNAME auf `go4exercises.github.io.` (mit Punkt am Ende,
      **ohne** Repo-Namen)
- [x] 🔑 **`physik`** — CNAME auf `go4exercises.github.io.`
- [x] 🔑 **`www`** — CNAME auf `go4exercises.github.io.` (fängt Leute ab, die
      `www.` davor tippen)

> **Ist-Zustand (10. August 2026), gegen beide autoritativen Nameserver geprüft:**
>
> | Name | Typ | Wert | TTL |
> |---|---|---|---|
> | `begreifbar.ch` | A | `185.199.108.153` · `185.199.109.153` · `185.199.110.153` · `185.199.111.153` | 300 |
> | `begreifbar.ch` | AAAA | `2606:50c0:8000::153` · `2606:50c0:8001::153` · `2606:50c0:8002::153` · `2606:50c0:8003::153` | 300 |
> | `mathe` | CNAME | `go4exercises.github.io.` | 300 |
> | `physik` | CNAME | `go4exercises.github.io.` | 300 |
> | `www` | CNAME | `go4exercises.github.io.` | 300 |
>
> **Mail-Records unverändert erhalten:** SPF (`v=spf1 -all`) und DMARC (`p=reject`)
> stehen weiterhin. **Kein Wildcard-Record** — ein `*`-Eintrag würde unbekannte
> Subdomains auf GitHub Pages leiten und die Domain-Verifikation aushebeln.

DNS-Änderungen brauchen bis zu ein paar Stunden. Prüfen kannst du mit
`dig mathe.begreifbar.ch` bzw. `dig begreifbar.ch` — oder sag mir Bescheid,
🤖 ich messe nach und melde, was schon steht.

---

## Phase 2 · GitHub Pages verbinden

- [x] 🤖 `CNAME`-Datei mit dem Inhalt `mathe.begreifbar.ch` im Repo-Root anlegen.
- [x] 🔑 Pushen.
- [x] 🔑 Repo *TALS-Mathe* → **Settings → Pages → Custom domain** prüfen: dort
      sollte `mathe.begreifbar.ch` bereits stehen (aus der `CNAME`-Datei). Der
      grüne Haken «DNS check successful» kommt, sobald Phase 1 durchgelaufen ist.
- [x] 🔑 **Enforce HTTPS** anhaken. Das Zertifikat (Let's Encrypt) stellt GitHub
      selbst aus; es kann bis zu 24 h dauern, bis der Haken anklickbar ist.
- [x] 🔑 **Domain verifizieren** — GitHub-Konto → Settings → Pages →
      *Verify a domain*. GitHub gibt dir einen TXT-Record
      (`_github-pages-challenge-go4exercises`), den du beim Registrar einträgst.
      Das verhindert, dass jemand anders deine Domain auf sein Repo legt.

> **Ist-Zustand (10. August 2026):**
>
> - `CNAME` liegt im Repo-Root, Inhalt `mathe.begreifbar.ch` — eine Zeile, LF,
>   kein BOM — und ist gepusht.
> - `https://mathe.begreifbar.ch/` liefert aus, **Enforce HTTPS** ist gesetzt.
> - Die Domain ist auf GitHub **verifiziert**; der TXT-Record
>   `_github-pages-challenge-go4exercises` deckt die Subdomains mit ab.
>
> ⚠️ **Der TXT-Record darf nie gelöscht werden.** Ohne ihn fällt die Verifikation
> weg, und eine fremde Person könnte eine deiner Subdomains auf ihr Repo legen.

**Was dabei *nicht* passiert:** Die alten Adressen brechen nicht. GitHub leitet
`go4exercises.github.io/TALS-Mathe/…` auf die neue Domain um. Bestehende Links,
Lesezeichen und Suchtreffer laufen weiter.

---

## Phase 3 · Repo umstellen

**Erst starten, wenn Phase 2 grün ist.** Sonst zeigen die `canonical`-Angaben
für ein paar Stunden auf eine Domain, die noch nicht antwortet.

Die Bestandsaufnahme (gemessen, nicht geschätzt): 567 Vorkommen von
`go4exercises.github.io` im Repo, davon **501 in den generierten SEO-Blöcken**
plus 51 in `sitemap.xml` und 1 in `robots.txt`. Die entstehen alle neu, sobald
eine einzige Zeile stimmt. Von Hand bleiben 13 Stellen.

- [x] 🤖 `scripts/build-seo.py`, Zeile 37: `BASIS` auf `https://mathe.begreifbar.ch/`.
- [x] 🤖 `python3 scripts/build-seo.py` — schreibt 51 Seiten-Kopfblöcke,
      `sitemap.xml` und `robots.txt` neu.
- [x] 🤖 `nav.js`: die drei Querlinks auf `https://physik.begreifbar.ch/` und den
      Lizenz-Hinweis auf die neue Adresse.
- [x] 🤖 Fliesstext-Erwähnungen in `glossar.html` und `formelsammlung.html`.
- [x] 🤖 `README.md` (3×), `TODO-port-to-tals-mathe.md`. **Abweichung:** Die zwei
      Nennungen in `CHANGELOG.md` stehen im Eintrag `[66]` vom 13.06.2026 und
      halten fest, worauf die Querlinks *damals* gesetzt wurden — sie bleiben
      stehen, stattdessen gibt es einen neuen Changelog-Eintrag zum Umzug.
- [x] 🤖 Eintrag in `TODO-schwesterprojekt.md`: Physik braucht dieselbe Umstellung.
- [x] 🤖 Pre-Flight über alle 46 Themenseiten, dazu ein Link-Check: keine
      `github.io`-Reste ausserhalb der Doku-Historie.
- [x] 🔑 Pushen.
- [x] 🤝 Nach dem Deploy messe ich nach: HTTPS greift, `canonical` zeigt auf die
      neue Domain, `sitemap.xml` erreichbar, keine gemischten Inhalte.

> **Nachmessung am 11. August 2026** (Deploy vom 10.8., 20:01 UTC):
>
> - `http://mathe.begreifbar.ch/` antwortet **301** auf `https://` — Enforce HTTPS greift.
> - `go4exercises.github.io/TALS-Mathe/` antwortet **301** auf `https://mathe.begreifbar.ch/` —
>   alte Links, Lesezeichen und Suchtreffer laufen weiter.
> - `canonical`, `og:url` und `og:image` über **alle 233 HTML-Dateien** geprüft: 51 Seiten
>   tragen die Felder, keine einzige zeigt auf eine andere Domain. Live gegengeprüft an
>   Startseite, Glossar, Formelsammlung, Rechtliches, Feedback, 5.2c und 4.3d.
> - `og-bild.png` liefert **200 / image/png / 57 kB**, `sitemap.xml` erreichbar mit 51 Einträgen.
> - **Keine gemischten Inhalte:** in HTML, JS und CSS gibt es keine einzige `http://`-Einbindung.
>
> Ein Audit-Bericht vom 11.8. meldete die alte Adresse im `canonical` der Startseite. Das
> war ein Abzug von **vor** dem Deploy: `last-modified` ist für Startseite und Unterseiten
> derselbe Zeitstempel, die Fastly-Cache-Zeit beträgt 600 s. Wer die Startseite vor 20:01
> und die Unterseiten danach erfasst, sieht genau dieses gemischte Bild.

---

## Phase 4 · Startseite auf `begreifbar.ch`

Der Apex braucht ein eigenes Repository — er kann nicht auf dasselbe Repo zeigen
wie `mathe.`.

- [x] 🔑 Neues Repo anlegen, z. B. `go4exercises/begreifbar`. **Erledigt.**
- [x] 🤖 Ich schreibe die Startseite (eine einzige HTML-Datei im Stil der beiden
      Lehrmittel: Titel, ein Satz zum Angebot, zwei grosse Kacheln Mathe/Physik,
      Footer mit Lizenz) und lege sie hier unter `apex-startseite/` ab.
      **Erledigt am 11.8.2026.**
- [x] 🔑 Ordnerinhalt ins neue Repo kopieren, `CNAME` mit `begreifbar.ch`,
      Pages aktivieren, Enforce HTTPS. **Erledigt.**

> ✅ **Phase 4 läuft. Gemessen am 31.8.2026:** `go4exercises.github.io/begreifbar/`
> leitet mit **301** auf `https://begreifbar.ch/` um, die Seite antwortet, Pages baut
> aus `main` / Wurzel, `CNAME` = `begreifbar.ch`, **Enforce HTTPS aktiv**. Die
> Zertifikatswarnung von früher gibt es nicht mehr. Das Repo enthält vier Dateien
> (`.nojekyll`, `CNAME`, `favicon.svg`, `index.html`) aus einem einzigen Commit vom
> 11.8.2026.

### ⚠️ Der ausgelieferte Stand hinkt dem Ordner hinterher

`apex-startseite/index.html` ist seither **zweimal geändert** worden, live ist noch die
Fassung vom 11.8.:

1. **Schriften lokal** (30.8.2026). Live hängt die Seite weiterhin an
   `fonts.googleapis.com` — als einzige Seite der ganzen Domain. Mathe liefert seit
   dem 30.8. alles vom eigenen Server, `mathe.begreifbar.ch/rechtliches.html` sagt das
   ausdrücklich zu, und die Apex-Seite verlinkt genau dorthin. Solange sie nicht
   nachgezogen ist, widerspricht die Eingangsseite der Zusage, auf die sie selbst zeigt.
2. **Kachel-Layout** (`grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))`
   statt fester zwei Spalten, plus `border-left-color` und `:focus-visible`).

Der Ordner ist also **vorne**, nicht hinten — beim Kopieren geht nichts verloren.
**Wichtig:** Neu gehören `schriften.css` und der Ordner `schriften/` mit dazu; ohne sie
fällt die Seite still auf Georgia zurück, ohne Fehlermeldung.

### Wie dieser Bereich gepusht wird — nämlich gar nicht automatisch

Es gibt **keinen lokalen Klon** von `go4exercises/begreifbar` auf dem Arbeitsrechner
(gesucht am 31.8.2026), und **kein Automatismus verbindet** `apex-startseite/` mit dem
Apex-Repo. Der eine Commit vom 11.8. wurde offenbar von Hand eingespielt, vermutlich über
die GitHub-Weboberfläche. `apex-startseite/` ist die gepflegte Quelle, das Apex-Repo die
Auslieferung — die Brücke dazwischen muss jedes Mal von Hand geschlagen werden.

Einmalig einen Klon anlegen, danach ist es ein Dreizeiler:

```sh
gh repo clone go4exercises/begreifbar ~/begreifbar        # einmalig
cd ~/begreifbar
rsync -a --delete --exclude '.git' --exclude 'README.md' ~/tals-mathe/apex-startseite/ .
git add -A && git commit -m "Schriften lokal, Kachel-Layout" && git push
```

`--delete` räumt auch weg, was im Ordner nicht mehr steht; `--exclude 'README.md'` lässt
die Aufsetz-Anleitung im Mathe-Repo. **`--exclude '.git'` ist Pflicht** — ohne den
Ausschluss löscht `--delete` das `.git`-Verzeichnis des Klons, weil es in der Quelle nicht
vorkommt. Ohne `rsync`: `cp -r` und die Reste von Hand entfernen.

**Alternative, falls dir das dritte Repo je zu viel wird:** Apex und `www` per
Weiterleitung des Registrars auf `mathe.begreifbar.ch` schicken. Du verlierst dann die
gemeinsame Eingangsseite, und wer `begreifbar.ch` eintippt, landet in Mathe statt vor der
Wahl.

---

## Phase 5 · Physik nachziehen

> **Teilweise erledigt (gemessen am 11.8.2026):** `https://physik.begreifbar.ch/`
> antwortet mit **200**, und `go4exercises.github.io/TALS-Physik/` leitet mit **301**
> dorthin um — `CNAME`, Pages-Einstellung und die Basis-URL im dortigen SEO-Skript
> sind also gemacht (`canonical` und `og:url` zeigen auf die neue Domain, im Quelltext
> steht kein `go4exercises.github.io` mehr). **Offen ist dort nur noch der Markenname:**
> Titel und `og:site_name` lauten weiterhin «TALS Physik», während Mathe seit dem
> 10.8. «Mathe begreifbar» heisst und in Mathes Menü bereits «Physik begreifbar»
> steht. Details im Eintrag in `TODO-schwesterprojekt.md`.
>
> **Nachgemessen am 31.8.2026:** Der Markenname ist weiterhin offen — `<title>` lautet
> «TALS Physik — RLP-BM 2030», `og:site_name` «TALS Physik». Alles andere an Phase 5 ist
> erledigt, auch die Drittanbieter-Freiheit: `physik.begreifbar.ch` liefert `schriften.css`
> aus, kein `googleapis`, kein `jsdelivr`. Damit ist der Markenname der **einzige** offene
> Punkt des ganzen Umzugs.

🔑 **Komplett bei dir** — ich fasse das Physik-Repo grundsätzlich nicht an
(`CLAUDE.md`). Dort dieselben Schritte: `CNAME` mit `physik.begreifbar.ch`,
Pages-Einstellung, Enforce HTTPS, Basis-URL im dortigen SEO-Skript, Querlinks
zurück auf `mathe.begreifbar.ch`. Ich lege den Eintrag dafür in
`TODO-schwesterprojekt.md`, damit er in der nächsten Physik-Sitzung bereitsteht.

---

## Phase 6 · Auffindbarkeit

- [ ] 🔑 **Google Search Console**: neue Property `mathe.begreifbar.ch` anlegen
      (Verifikation läuft über denselben DNS-Zugang) und `sitemap.xml` einreichen.
- [ ] 🔑 Falls die alte Property schon eingerichtet ist: dort die Funktion
      **Adressänderung** verwenden. Sie überträgt die Bewertung schneller als
      die Weiterleitung allein.
- [ ] 🔑 Neue Adresse dort nachführen, wo du sie gestreut hast — Schul-Intranet,
      Klassen-Handout, QR-Codes auf Unterlagen.
- [x] 🤖 `og-bild.png` und die Metadaten trugen den Namen «TALS Mathematik».
      **Erledigt am 10.8.2026:** Die Marke heisst jetzt **«Mathe begreifbar»** —
      891 Stellen umbenannt, `og-bild.png` mit neuem Namen und neuer Adresse
      gebaut. «TALS» bleibt, wo es die Zielgruppe benennt. Offen bleibt nur
      `scripts/build_apkg.py` samt den 45 Anki-Decks, siehe unten.

---

## Offener Rest: Anki-Decks

Die 45 Decks unter `downloads/*/*/ankideck.apkg` tragen den Decknamen
`TALS Mathematik::Grundlagen::…`. Er wurde **absichtlich nicht** umbenannt:
`scripts/build_apkg.py` erzeugt die Notiz-GUIDs mit `random.seed(hash(deck_name))`,
die GUIDs hängen also am Decknamen. Ein Neubau unter neuem Namen erzeugt neue
GUIDs — wer das Deck schon benutzt, bekommt beim Import **Dubletten statt einer
Umbenennung** und verliert die Zuordnung seines Lernfortschritts.

Dazu kommt: `hash()` auf Zeichenketten ist in Python pro Prozess zufällig
gesalzen (`PYTHONHASHSEED`), der Seed ist also ohnehin nicht reproduzierbar —
schon ein Neubau *ohne* Umbenennung erzeugte neue GUIDs.

**Sauberer Weg, wenn du es willst:** erst die GUID-Erzeugung auf einen stabilen
Wert umstellen (z. B. `hashlib.sha1` über Deckname und Kartenvorderseite), dann
umbenennen und alle 45 Decks neu bauen. Solange das offen ist, bleiben Skript
und ausgelieferte Decks konsistent beim alten Namen.

---

## Notbremse

Falls etwas schiefgeht, ist der Rückweg kurz — nichts davon ist endgültig:

1. In **Settings → Pages** die Custom domain leeren (bzw. `CNAME`-Datei löschen).
   Die Seite ist sofort wieder unter `go4exercises.github.io/TALS-Mathe/` da.
2. `BASIS` in `scripts/build-seo.py` zurücksetzen, Skript laufen lassen, pushen.
3. Die DNS-Records können stehen bleiben; sie schaden nicht.

Jeder Schritt in Phase 3 ist ein eigener Commit — `git revert` genügt.

---

## Registrar — Empfehlung

Für eine `.ch`-Domain, die dauerhaft auf GitHub Pages zeigt, zählen drei Dinge:
**freie DNS-Verwaltung** (A, AAAA, CNAME und TXT musst du selbst setzen können —
manche Billiganbieter erlauben nur Web-Weiterleitung, damit funktioniert der
Apex nicht), **Beständigkeit** des Anbieters, und erst dann der Preis.

**Empfehlung: [Infomaniak](https://www.infomaniak.com/de/domains)** (Genf).
Schweizer Unternehmen seit 1994 mit eigenen Rechenzentren, vollständige
DNS-Verwaltung inbegriffen, DNSSEC vorhanden, kein aggressives Nachverkaufen
beim Bestellen. Für ein Projekt, das Jahre laufen soll, ist die Beständigkeit
mehr wert als ein paar Franken.

Alternativen, falls du vergleichen willst:

| Anbieter | Profil |
|---|---|
| [Hostpoint](https://www.hostpoint.ch) (Rapperswil) | Schweizer Anbieter mit dem besten Ruf beim Support; tendenziell etwas teurer |
| [cyon](https://www.cyon.ch) (Basel) | ebenfalls Schweiz, sehr solide Verwaltungsoberfläche |
| [INWX](https://www.inwx.de) (Berlin) | meist am günstigsten, technisch exzellent, volle DNS-Kontrolle — aber nicht Schweiz |

> **Preise absichtlich nicht genannt.** Ich konnte sie nicht aus erster Hand
> abrufen (die Preisseiten laden ihre Zahlen per JavaScript nach), und geratene
> Beträge sind schlechter als keine. Die Grössenordnung für `.ch` liegt im
> unteren zweistelligen Frankenbereich pro Jahr — schau vor dem Kauf auf die
> verlinkten Seiten und **achte besonders auf den Verlängerungspreis**, nicht
> nur auf das erste Jahr.

Ein Punkt zum Datenschutz: Wie sichtbar deine Halterdaten bei `.ch` sind, regelt
die Registerstelle, nicht der Registrar. Wenn dir das wichtig ist, kläre es vor
dem Kauf beim Anbieter ab — ich habe es nicht verifiziert und will es nicht raten.

---

## Reihenfolge in einem Satz

Domain kaufen → DNS setzen → GitHub verbinden und HTTPS erzwingen → **erst dann**
die URLs im Repo umstellen → Startseite und Physik nachziehen → Search Console.
