#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────────────────────
#  neue-subdomain.py — eine gezippte Website als eigenes Repo auf GitHub Pages
#  veroeffentlichen und als Kachel in begreifbar.ch einhaengen.
#
#  Aufruf vom Repo-Wurzelverzeichnis:
#      python3 scripts/neue-subdomain.py <subdomain> <website.zip|seite.html> [Optionen]
#
#  Beispiel:
#      python3 scripts/neue-subdomain.py chemie ~/Downloads/chemie.zip \
#          --titel Chemie --farbe gruen \
#          --text "Stoffe, Reaktionen und Stoechiometrie — mit Rechenwegen." \
#          --marke Grundlagenfach
#
#  Was passiert, in dieser Reihenfolge:
#    1. Vorpruefungen (gh angemeldet, Repo-Name frei, ZIP lesbar, Kachel neu)
#    2. ZIP auspacken (oder die einzelne Seite als index.html hinlegen),
#       Wurzel normalisieren, CNAME und .nojekyll schreiben
#    3. WARTEN auf den DNS-Eintrag — den muss der Mensch beim Registrar setzen
#    4. Repo anlegen und pushen (gh repo create --public --source=. --push)
#    5. Pages einschalten, auf «built» warten, HTTPS erzwingen
#    6. Kachel in apex-startseite/index.html einfuegen und lokal committen
#       (entfaellt mit --ohne-kachel — fuer Einzelseiten, die nicht ins
#       Faecher-Verzeichnis gehoeren)
#    7. Apex-Repo klonen, Inhalt uebernehmen, pushen — die Kachel geht live
#    8. Abschlussmessung ueber HTTPS
#
#  Was das Skript NICHT kann: den DNS-Eintrag setzen. Dafuer braeuchte es
#  Registrar-Zugang. Es sagt genau, was einzutragen ist, und wartet darauf.
#
#  Abbruch mit Strg-C ist an jeder Stelle gefahrlos; angelegte Repos bleiben
#  dann stehen und muessen von Hand entfernt werden (das meldet das Skript).
# ─────────────────────────────────────────────────────────────────────────────

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = 'begreifbar.ch'
KONTO = 'go4exercises'
APEX_REPO = f'{KONTO}/begreifbar'
APEX_QUELLE = ROOT / 'apex-startseite'
PAGES_ZIEL = f'{KONTO}.github.io.'          # Ziel des CNAME-Eintrags beim Registrar
DOH = 'https://cloudflare-dns.com/dns-query?name={}&type=CNAME'

# Farbnamen aus dem Farbsystem der Lehrmittel (style.css). Wer etwas anderes
# will, uebergibt einen Hex-Wert; die hellen und mittleren Toene werden dann
# daraus gemischt.
PALETTE = {
    'blau':      ('#1a4f8a', '#ddeaf8', '#5b8fc9'),
    'bernstein': ('#8a4a0e', '#fbecd2', '#c98028'),
    'gruen':     ('#1f6b3a', '#d8f0e2', '#52a872'),
    'lila':      ('#5b2d8e', '#ede6f8', '#9b6bd4'),
    'rot':       ('#9b1c1c', '#fde8e8', '#d05050'),
    'orange':    ('#b85c00', '#fdefd8', '#e08030'),
}


# ── Ausgabe ──────────────────────────────────────────────────────────────────

class Abbruch(Exception):
    pass


def schritt(n, text):
    print(f'\n\033[1m[{n}]\033[0m {text}')


def ok(text):
    print(f'   ✓ {text}')


def info(text):
    print(f'     {text}')


def warn(text):
    print(f'   ! {text}')


# ── Hilfen ───────────────────────────────────────────────────────────────────

def lauf(befehl, cwd=None, pruefen=True, still=False):
    """Fuehrt einen Befehl aus und gibt (rc, stdout) zurueck."""
    e = subprocess.run(befehl, cwd=cwd, capture_output=True, text=True)
    if not still and e.stdout.strip():
        for z in e.stdout.strip().splitlines():
            info(z)
    if pruefen and e.returncode != 0:
        raise Abbruch(f'«{" ".join(befehl)}» scheiterte:\n{e.stderr.strip() or e.stdout.strip()}')
    return e.returncode, e.stdout.strip()


def gh_api(pfad, methode='GET', felder=None, roh_felder=None, pruefen=True):
    befehl = ['gh', 'api', '-X', methode, pfad]
    for k, v in (felder or {}).items():
        befehl += ['-f', f'{k}={v}']
    for k, v in (roh_felder or {}).items():
        befehl += ['-F', f'{k}={v}']
    rc, aus = lauf(befehl, pruefen=pruefen, still=True)
    if rc != 0:
        return rc, {}
    try:
        return rc, json.loads(aus or '{}')
    except json.JSONDecodeError:
        return rc, {}


def hex_zu_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def misch(farbe, ziel, anteil):
    """anteil=0 -> farbe, anteil=1 -> ziel."""
    a, b = hex_zu_rgb(farbe), hex_zu_rgb(ziel)
    return '#%02x%02x%02x' % tuple(round(x + (y - x) * anteil) for x, y in zip(a, b))


def farbsatz(wert):
    """Liefert (grund, hell, rand) — aus der Palette oder aus einem Hex-Wert."""
    if wert in PALETTE:
        return PALETTE[wert]
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', wert):
        raise Abbruch(f'--farbe: «{wert}» ist weder ein Palettenname '
                      f'({", ".join(PALETTE)}) noch ein Hex-Wert wie #1f6b3a.')
    return wert.lower(), misch(wert, '#ffffff', 0.86), misch(wert, '#ffffff', 0.45)


def esc(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


# ── 1. Vorpruefungen ─────────────────────────────────────────────────────────

def pruefe_subdomain(name):
    if not re.fullmatch(r'[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?', name):
        raise Abbruch(f'«{name}» ist kein gueltiger Subdomain-Name. Erlaubt sind '
                      'Kleinbuchstaben, Ziffern und Bindestriche (nicht am Rand), '
                      'hoechstens 63 Zeichen.')
    if name in ('www', 'mathe', 'physik'):
        raise Abbruch(f'«{name}» ist bereits vergeben.')


def pruefe_alleinstehend(html_pfad):
    """Eine einzelne Seite muss ohne Nachbardateien auskommen — sonst fehlen sie
    im Repo. Relative Bezuege sind darum ein Grund zur Warnung, kein Abbruch:
    vielleicht sind sie Absicht."""
    t = html_pfad.read_text(encoding='utf-8', errors='replace')
    bezuege = sorted(set(re.findall(
        r'(?:src|href)="(?!https?://|data:|mailto:|tel:|#|/)([^"]+)"', t)))
    if bezuege:
        warn(f'Die Seite verweist auf {len(bezuege)} Datei(en) daneben — die kommen '
             'nicht mit, weil nur diese eine Datei hochgeladen wird:')
        for b in bezuege[:8]:
            info(f'  {b}')
        if len(bezuege) > 8:
            info(f'  … und {len(bezuege) - 8} weitere')
        info('Entweder alles in die HTML einbetten oder ein ZIP mit allen Dateien übergeben.')


def vorpruefungen(args, repo):
    schritt(1, 'Vorprüfungen')
    for werkzeug in ('git', 'gh'):
        if not shutil.which(werkzeug):
            raise Abbruch(f'{werkzeug} ist nicht installiert.')
    rc, _ = lauf(['gh', 'auth', 'status'], pruefen=False, still=True)
    if rc != 0:
        raise Abbruch('gh ist nicht angemeldet — «gh auth login» ausführen.')
    ok('git und gh vorhanden, gh angemeldet')

    if not args.quelle.is_file():
        raise Abbruch(f'Datei nicht gefunden: {args.quelle}')
    if args.quelle.suffix.lower() in ('.html', '.htm'):
        ok(f'Einzelne Seite: {args.quelle.name}')
        pruefe_alleinstehend(args.quelle)
    elif zipfile.is_zipfile(args.quelle):
        ok(f'ZIP lesbar: {args.quelle.name}')
    else:
        raise Abbruch(f'{args.quelle.name} ist weder eine .html-Datei noch ein ZIP.')

    rc, _ = gh_api(f'repos/{repo}', pruefen=False)
    if rc == 0:
        raise Abbruch(f'Repository {repo} existiert bereits. Anderen Namen mit '
                      '--repo wählen oder das bestehende Repo aufräumen.')
    ok(f'Repository-Name frei: {repo}')

    if args.ohne_kachel:
        ok('ohne Kachel — begreifbar.ch wird nicht angefasst')
        return

    if not (APEX_QUELLE / 'index.html').is_file():
        raise Abbruch(f'{APEX_QUELLE}/index.html fehlt — läuft das Skript im Repo-Wurzelverzeichnis?')
    apex = (APEX_QUELLE / 'index.html').read_text(encoding='utf-8')
    if not args.ohne_kachel and f'https://{args.subdomain}.{DOMAIN}/' in apex:
        raise Abbruch(f'In apex-startseite/index.html gibt es bereits eine Kachel für '
                      f'{args.subdomain}.{DOMAIN}.')
    for marke in ('FAECHER:ANFANG', 'FAECHER:ENDE', 'FACHFARBEN:ANFANG', 'FACHFARBEN:ENDE'):
        if marke not in apex:
            raise Abbruch(f'Marke «{marke}» fehlt in apex-startseite/index.html.')
    ok('Apex-Startseite bereit, Kachel noch nicht vorhanden')

    grund, hell, rand = farbsatz(args.farbe)   # wirft bei unbekanntem Wert
    ok(f'Farbe {args.farbe} → {grund} / {hell} / {rand}')

    rc, _ = lauf(['git', 'diff', '--quiet', '--', str(APEX_QUELLE)], cwd=ROOT, pruefen=False, still=True)
    if rc != 0:
        warn('apex-startseite/ hat uncommittete Änderungen — die kämen mit in den Commit.')


# ── 2. ZIP auspacken ─────────────────────────────────────────────────────────

def bereitstellen(quelle, ziel):
    """Legt den auszuliefernden Ordner an — aus einem ZIP oder aus einer Seite."""
    if quelle.suffix.lower() in ('.html', '.htm'):
        schritt(2, 'Einzelne Seite bereitstellen')
        ziel.mkdir(parents=True, exist_ok=True)
        shutil.copy2(quelle, ziel / 'index.html')
        if quelle.name != 'index.html':
            ok(f'{quelle.name} → index.html (nur dieser Name wird als Startseite ausgeliefert)')
        else:
            ok('index.html übernommen')
        return ziel

    schritt(2, 'ZIP auspacken und Wurzel bestimmen')
    with zipfile.ZipFile(quelle) as z:
        for eintrag in z.namelist():
            p = Path(eintrag)
            # Zip-Slip: absolute Pfade und »..« wuerden ausserhalb von ziel schreiben.
            if p.is_absolute() or '..' in p.parts:
                raise Abbruch(f'ZIP enthält einen unsicheren Pfad: {eintrag}')
        z.extractall(ziel)
    ok(f'{len(list(ziel.rglob("*")))} Einträge ausgepackt')

    # Haeufigster Fall: alles steckt in genau einem Oberordner — den ziehen wir hoch.
    inhalt = [p for p in ziel.iterdir() if p.name not in ('__MACOSX',)]
    if len(inhalt) == 1 and inhalt[0].is_dir():
        unter = inhalt[0]
        info(f'Ein einzelner Oberordner «{unter.name}» — Inhalt wird hochgezogen.')
        for p in list(unter.iterdir()):
            shutil.move(str(p), str(ziel / p.name))
        unter.rmdir()
    shutil.rmtree(ziel / '__MACOSX', ignore_errors=True)

    if not (ziel / 'index.html').is_file():
        gefunden = sorted(p.relative_to(ziel).as_posix() for p in ziel.rglob('index.html'))
        hinweis = f' Gefunden wurde index.html unter: {", ".join(gefunden)}' if gefunden else ''
        raise Abbruch('Im ZIP liegt keine index.html im Wurzelverzeichnis.' + hinweis)
    ok('index.html liegt im Wurzelverzeichnis')
    return ziel


def beigaben(ordner, host):
    (ordner / 'CNAME').write_text(host + '\n', encoding='utf-8', newline='\n')
    (ordner / '.nojekyll').touch()
    ok(f'CNAME geschrieben ({host}) und .nojekyll angelegt')


# ── 3. DNS ───────────────────────────────────────────────────────────────────

def dns_cname(host):
    try:
        anfrage = urllib.request.Request(DOH.format(host),
                                         headers={'accept': 'application/dns-json'})
        with urllib.request.urlopen(anfrage, timeout=15) as a:
            daten = json.load(a)
        return [e['data'] for e in daten.get('Answer', []) if e.get('type') == 5]
    except Exception:
        return []


def warte_auf_dns(host, warten, takt=20):
    schritt(3, 'DNS-Eintrag')
    print(f"""
   ┌─ Beim Registrar (Infomaniak) eintragen ────────────────────────
   │  Typ    CNAME
   │  Name   {host.split('.')[0]}
   │  Ziel   {PAGES_ZIEL}          (mit Punkt am Ende)
   │  TTL    300
   └────────────────────────────────────────────────────────────────
""")
    if not warten:
        warn('--ohne-dns-warten gesetzt: weiter ohne Prüfung. Der Pages-DNS-Check '
             'schlägt fehl, solange der Eintrag nicht steht.')
        return
    print(f'   Warte auf den Eintrag (Abbruch mit Strg-C) …')
    while True:
        ziele = dns_cname(host)
        if any(z.rstrip('.') == PAGES_ZIEL.rstrip('.') for z in ziele):
            ok(f'{host} → {ziele[0]}')
            return
        if ziele:
            warn(f'{host} zeigt auf {ziele[0]} statt auf {PAGES_ZIEL} — bitte korrigieren.')
        time.sleep(takt)
        print('     … noch nicht sichtbar, prüfe erneut', flush=True)


# ── 4./5. Repo und Pages ─────────────────────────────────────────────────────

def repo_anlegen(ordner, repo, host):
    schritt(4, f'Repository {repo} anlegen und pushen')
    lauf(['git', 'init', '-b', 'main'], cwd=ordner, still=True)
    lauf(['git', 'add', '-A'], cwd=ordner, still=True)
    lauf(['git', 'commit', '-m', f'Website für {host}'], cwd=ordner, still=True)
    lauf(['gh', 'repo', 'create', repo, '--public', '--source=.', '--push'], cwd=ordner)
    ok(f'https://github.com/{repo} angelegt und gepusht')


def pages_einschalten(repo, host):
    schritt(5, 'GitHub Pages einschalten')
    rc, _ = gh_api(f'repos/{repo}/pages', 'POST',
                   felder={'source[branch]': 'main', 'source[path]': '/', 'cname': host},
                   pruefen=False)
    if rc != 0:
        raise Abbruch('Pages liess sich nicht einschalten. Häufigste Ursache: der '
                      'DNS-Eintrag steht noch nicht. Nach dem Setzen genügt:\n'
                      f'  gh api -X POST repos/{repo}/pages '
                      f'-f "source[branch]=main" -f "source[path]=/" -f cname={host}')
    ok(f'Pages eingeschaltet, Custom domain {host}')

    print('   Warte auf den ersten Build …')
    for _ in range(40):                       # bis ~10 Minuten
        _, daten = gh_api(f'repos/{repo}/pages', pruefen=False)
        if daten.get('status') == 'built':
            ok('Build fertig')
            break
        time.sleep(15)
    else:
        warn('Build dauert länger als erwartet — später mit '
             f'«gh api repos/{repo}/pages» nachsehen.')

    print('   Warte auf das Zertifikat, dann HTTPS erzwingen …')
    for _ in range(40):
        rc, _ = gh_api(f'repos/{repo}/pages', 'PUT',
                       roh_felder={'https_enforced': 'true'}, pruefen=False)
        if rc == 0:
            ok('Enforce HTTPS gesetzt')
            return
        time.sleep(15)
    warn('Zertifikat noch nicht bereit. Später nachholen mit:\n'
         f'       gh api -X PUT repos/{repo}/pages -F https_enforced=true')


# ── 6. Kachel in die Apex-Startseite ─────────────────────────────────────────

def kachel_text(s, slug, host, titel, marke, text, farbe):
    """Reine Textumformung — ohne Datei- oder Git-Zugriff, damit pruefbar."""
    grund, hell, rand = farbsatz(farbe)

    regel = (f'.f-{slug} {{ --fach: {grund}; --fach-hell: {hell}; --fach-rand: {rand}; }}\n')
    s = s.replace('/* FACHFARBEN:ENDE */', regel + '/* FACHFARBEN:ENDE */', 1)

    kachel = f"""
    <a class="fach f-{slug}" href="https://{host}/">
      <span class="f-marke">{esc(marke)}</span>
      <div class="f-titel">{esc(titel)}</div>
      <p class="f-text">{esc(text)}</p>
      <div class="f-adresse">{host} <span class="f-pfeil" aria-hidden="true">→</span></div>
    </a>

    <!-- FAECHER:ENDE -->"""
    return s.replace('\n    <!-- FAECHER:ENDE -->', kachel, 1), grund


def kachel_einfuegen(args, host):
    schritt(6, 'Kachel in apex-startseite/index.html einfügen')
    datei = APEX_QUELLE / 'index.html'
    neu, grund = kachel_text(datei.read_text(encoding='utf-8'), args.subdomain, host,
                             args.titel, args.marke, args.text, args.farbe)
    datei.write_text(neu, encoding='utf-8')
    ok(f'Kachel «{args.titel}» ergänzt, Farbe {grund}')

    # Überschrift und Beschreibung nennen die Fächer namentlich. Sie automatisch
    # umzuschreiben hiesse Prosa raten — darum nur ein Hinweis mit den Fundstellen.
    anzahl = neu.count('class="fach f-')
    if anzahl > 2:
        stellen = [f'{i}: {z.strip()[:96]}' for i, z in enumerate(neu.splitlines(), 1)
                   if ('Zwei kostenlose' in z or '<h1>' in z
                       or ('name="description"' in z) or ('og:description' in z)
                       or '<title>' in z or 'og:title' in z)]
        warn(f'Die Seite trägt jetzt {anzahl} Fächer, spricht aber weiter von zweien.')
        info('Von Hand nachziehen in apex-startseite/index.html:')
        for st in stellen:
            info(f'  Zeile {st}')

    lauf(['git', 'add', str(datei)], cwd=ROOT, still=True)
    lauf(['git', 'commit', '-m',
          f'Apex-Startseite: Kachel für {host}\n\n'
          f'Fach «{args.titel}», Farbe {grund}. Repository {KONTO}/{args.repo or args.subdomain}.'],
         cwd=ROOT, still=True)
    ok('lokal committet (Push dieses Repos bleibt bei dir)')


# ── 7. Apex-Repo aktualisieren ───────────────────────────────────────────────

def apex_veroeffentlichen(arbeitsordner):
    schritt(7, f'Apex-Repo {APEX_REPO} aktualisieren')
    klon = arbeitsordner / 'apex'
    lauf(['gh', 'repo', 'clone', APEX_REPO, str(klon), '--', '--depth', '1'], still=True)
    for p in APEX_QUELLE.iterdir():
        if p.name in ('README.md', '.git'):
            continue                       # die Anleitung gehoert nicht auf die Website
        ziel = klon / p.name
        if p.is_dir():
            shutil.copytree(p, ziel, dirs_exist_ok=True)
        else:
            shutil.copy2(p, ziel)
    rc, aus = lauf(['git', 'status', '--porcelain'], cwd=klon, still=True)
    if not aus:
        warn('Apex-Repo ist bereits auf diesem Stand — nichts zu pushen.')
        return
    lauf(['git', 'add', '-A'], cwd=klon, still=True)
    lauf(['git', 'commit', '-m', 'Startseite: neue Fach-Kachel'], cwd=klon, still=True)
    lauf(['git', 'push'], cwd=klon, still=True)
    ok(f'https://{DOMAIN}/ aktualisiert')


# ── 8. Messung ───────────────────────────────────────────────────────────────

def messen(host, mit_apex=True):
    schritt(8, 'Abschlussmessung')
    ziele = (f'https://{host}/', f'https://{DOMAIN}/') if mit_apex else (f'https://{host}/',)
    for url in ziele:
        for versuch in range(6):
            try:
                with urllib.request.urlopen(url, timeout=20) as a:
                    inhalt = a.read().decode('utf-8', 'replace')
                ok(f'{url} → {a.status}')
                if url == f'https://{DOMAIN}/' and host in inhalt:
                    ok(f'Kachel für {host} ist auf der Startseite sichtbar')
                break
            except Exception as e:
                if versuch == 5:
                    warn(f'{url} antwortet noch nicht ({e}) — Pages braucht manchmal '
                         'ein paar Minuten.')
                else:
                    time.sleep(20)


# ── Hauptlauf ────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description='Gezippte Website als eigenes Repo auf GitHub Pages veröffentlichen '
                    'und als Kachel in begreifbar.ch einhängen.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('subdomain', help='z. B. chemie  →  chemie.begreifbar.ch')
    p.add_argument('quelle', type=Path,
                   help='ZIP mit der Website (index.html im Wurzelverzeichnis) '
                        'ODER eine einzelne .html-Datei')
    p.add_argument('--titel', help='Titel auf der Kachel (Vorgabe: Subdomain gross geschrieben)')
    p.add_argument('--marke', default='Grundlagenfach', help='Pille über dem Titel')
    p.add_argument('--text', default='', help='Ein Satz zum Inhalt, erscheint auf der Kachel')
    p.add_argument('--farbe', default='gruen',
                   help='Palettenname (' + ', '.join(PALETTE) + ') oder Hex-Wert wie #1f6b3a')
    p.add_argument('--repo', help='Repository-Name (Vorgabe: die Subdomain)')
    p.add_argument('--ohne-dns-warten', action='store_true',
                   help='nicht auf den DNS-Eintrag warten (nur sinnvoll, wenn er schon steht)')
    p.add_argument('--ohne-kachel', action='store_true',
                   help='keine Kachel auf begreifbar.ch — für einzelne Seiten, die '
                        'nicht ins Fächer-Verzeichnis gehören')
    p.add_argument('--nur-pruefen', action='store_true',
                   help='nur Schritte 1 und 2 — nichts anlegen, nichts pushen')
    args = p.parse_args()

    args.titel = args.titel or args.subdomain.capitalize()
    args.text = args.text or f'{args.titel} für die Berufsmaturität.'
    repo = f'{KONTO}/{args.repo or args.subdomain}'
    host = f'{args.subdomain}.{DOMAIN}'
    args.quelle = args.quelle.expanduser().resolve()

    arbeit = Path(tempfile.mkdtemp(prefix='neue-subdomain-'))
    repo_angelegt = False
    try:
        pruefe_subdomain(args.subdomain)     # vor der Kopfzeile, damit kein
        print(f'\n\033[1m{host}\033[0m  ←  {args.quelle.name}  ·  Repository {repo}')
        if args.nur_pruefen:                 # unsinniger Name gedruckt wird
            print('   \033[1mProbelauf\033[0m — es wird nichts angelegt und nichts gepusht.')
        vorpruefungen(args, repo)
        seite = bereitstellen(args.quelle, arbeit / 'seite')
        if args.nur_pruefen:
            beigaben(seite, host)
            print(f'\n   Probelauf in Ordnung. Bereitgestellt unter: {seite}')
            print('   Für den echten Lauf dieselbe Zeile ohne --nur-pruefen.')
            return 0
        beigaben(seite, host)
        warte_auf_dns(host, warten=not args.ohne_dns_warten)
        repo_anlegen(seite, repo, host)
        repo_angelegt = True
        pages_einschalten(repo, host)
        if args.ohne_kachel:
            schritt(6, 'Kachel übersprungen (--ohne-kachel)')
            info(f'https://{DOMAIN}/ bleibt unverändert.')
        else:
            kachel_einfuegen(args, host)
            apex_veroeffentlichen(arbeit)
        messen(host, mit_apex=not args.ohne_kachel)
        print(f'\n\033[1mFertig.\033[0m  https://{host}/'
              + ('' if args.ohne_kachel else f'  ·  Kachel auf https://{DOMAIN}/'))
        if not args.ohne_kachel:
            print(f'   Offen: «git push» in {ROOT} — der Kachel-Commit liegt lokal.')
        return 0
    except Abbruch as e:
        print(f'\n\033[1mAbbruch:\033[0m {e}', file=sys.stderr)
        if repo_angelegt:
            print(f'   Das Repository {repo} wurde bereits angelegt. Entfernen mit:\n'
                  f'     gh repo delete {repo} --yes', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('\nAbgebrochen.', file=sys.stderr)
        if repo_angelegt:
            print(f'   {repo} steht bereits — ggf. «gh repo delete {repo} --yes».', file=sys.stderr)
        return 130
    finally:
        if args.nur_pruefen:
            print(f'   (Arbeitsordner bleibt zum Nachsehen: {arbeit})')
        else:
            shutil.rmtree(arbeit, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
