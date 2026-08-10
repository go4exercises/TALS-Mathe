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
- [ ] 🔑 Pushen.
- [ ] 🤝 Nach dem Deploy messe ich nach: HTTPS greift, `canonical` zeigt auf die
      neue Domain, `sitemap.xml` erreichbar, keine gemischten Inhalte.

---

## Phase 4 · Startseite auf `begreifbar.ch`

Der Apex braucht ein eigenes Repository — er kann nicht auf dasselbe Repo zeigen
wie `mathe.`.

- [ ] 🔑 Neues Repo anlegen, z. B. `go4exercises/begreifbar`.
- [ ] 🤖 Ich schreibe die Startseite (eine einzige HTML-Datei im Stil der beiden
      Lehrmittel: Titel, ein Satz zum Angebot, zwei grosse Kacheln Mathe/Physik,
      Footer mit Lizenz) und lege sie hier unter `apex-startseite/` ab.
- [ ] 🔑 Ordnerinhalt ins neue Repo kopieren, `CNAME` mit `begreifbar.ch`,
      Pages aktivieren, Enforce HTTPS.

**Alternative, falls dir das dritte Repo zu viel ist:** Apex und `www` per
Weiterleitung des Registrars auf `mathe.begreifbar.ch` schicken. Kostet nichts
und geht sofort — du verlierst nur die gemeinsame Eingangsseite, und wer
`begreifbar.ch` eintippt, landet in Mathe statt vor der Wahl.

---

## Phase 5 · Physik nachziehen

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
