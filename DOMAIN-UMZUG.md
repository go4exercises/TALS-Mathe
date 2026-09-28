# Domain `begreifbar.ch` — Stand und offene Punkte

Der Umzug von `go4exercises.github.io/TALS-Mathe/` auf `begreifbar.ch` ist
abgeschlossen (Phasen 0–5, zuletzt der Physik-Markenname, Commit `2c72192`, auf
`origin/main` seit September 2026). Die ausführliche Arbeitsanleitung samt
Nachmessungen steht in der Git-Geschichte dieser Datei (bis 28.09.2026).

Rollen: 🔑 nur du (Konto, Zahlung, Zugriff) · 🤖 Repo-Arbeit.

---

## Was steht

```
begreifbar.ch         →  Startseite, zeigt auf beide Fächer  (Repo go4exercises/begreifbar)
mathe.begreifbar.ch   →  Repo TALS-Mathe
physik.begreifbar.ch  →  Repo TALS-Physik
```

- **Registrar:** Infomaniak, **Auto-Renew aktiv**. Eine abgelaufene Domain wäre
  der teuerste Fehler von allen.
- **DNS** (TTL 300): Apex mit vier A-Records `185.199.108–111.153` und vier
  AAAA-Records `2606:50c0:8000–8003::153`; `mathe`, `physik`, `www` als CNAME auf
  `go4exercises.github.io.`. SPF (`v=spf1 -all`) und DMARC (`p=reject`) bleiben.
  **Kein Wildcard-Record** — er würde unbekannte Subdomains auf GitHub Pages
  leiten.
- **GitHub Pages:** `CNAME` im Repo-Root, Enforce HTTPS, Domain verifiziert.
  Alte `go4exercises.github.io/…`-Adressen leiten mit 301 um.

> ⚠️ **Der TXT-Record `_github-pages-challenge-go4exercises` darf nie gelöscht
> werden.** Ohne ihn fällt die Verifikation weg, und eine fremde Person könnte eine
> deiner Subdomains auf ihr Repo legen.

---

## Startseite `begreifbar.ch` pflegen

`apex-startseite/` in diesem Repo ist die gepflegte Quelle, das Repo
`go4exercises/begreifbar` die Auslieferung. **Kein Automatismus** verbindet die
beiden — die Brücke wird jedes Mal von Hand geschlagen:

```sh
gh repo clone go4exercises/begreifbar ~/begreifbar        # einmalig
cd ~/begreifbar
rsync -a --delete --exclude '.git' --exclude 'README.md' ~/tals-mathe/apex-startseite/ .
git add -A && git commit -m "…" && git push
```

`--exclude '.git'` ist Pflicht, sonst löscht `--delete` das `.git` des Klons.
`schriften.css` und `schriften/` gehören mit dazu, sonst fällt die Seite still auf
Georgia zurück.

> ⚠️ **Live ist die Seite weiter als der Ordner** (gemessen 14.09.2026): Dort steht
> zusätzlich ein Link «Projektwoche IDM 2027» auf `projektwoche/` samt CSS-Block
> `.anlass`, der in `apex-startseite/index.html` fehlt. Vor dem nächsten `rsync
> --delete` erst den Ordner aus dem Apex-Repo aktualisieren, sonst geht der Link
> verloren.

---

## Offen

- [ ] 🔑 **Google Search Console:** Property `mathe.begreifbar.ch` anlegen
      (Verifikation über DNS) und `sitemap.xml` einreichen. Von aussen war am
      14.09.2026 keine Verifikation zu sehen.
- [ ] 🔑 Falls die alte Property existiert: dort **Adressänderung** verwenden — sie
      überträgt die Bewertung schneller als die Weiterleitung allein.
- [ ] 🔑 Neue Adresse dort nachführen, wo sie gestreut wurde: Schul-Intranet,
      Handouts, QR-Codes.
- [ ] 🔑 Optional, bewusst zurückgestellt: `matura-lernen.ch` als beschreibende
      Weiterleitungs-Domain (war am 03.08.2026 frei).
- [ ] 🤖 **Anki-Decks** tragen noch den Namen `TALS Mathematik::Grundlagen::…` —
      absichtlich: `scripts/build_apkg.py` erzeugt die Notiz-GUIDs mit
      `random.seed(hash(deck_name))`. Eine Umbenennung gäbe beim Import Dubletten
      statt eines Updates, und `hash()` ist pro Prozess gesalzen, also ohnehin
      nicht reproduzierbar. Sauberer Weg: erst GUIDs stabil machen (z. B.
      `hashlib.sha1` über Deckname und Vorderseite), dann umbenennen und alle 45
      Decks neu bauen.

---

## Notbremse

1. In **Settings → Pages** die Custom domain leeren (bzw. `CNAME` löschen) — die
   Seite ist sofort wieder unter `go4exercises.github.io/TALS-Mathe/` da.
2. `BASIS` in `scripts/build-seo.py` zurücksetzen, Skript laufen lassen, pushen.
3. Die DNS-Records können stehen bleiben.
