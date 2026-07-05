#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Mathematik aus einer Liste von (Front, Back)-Paaren."""
import sqlite3, zipfile, json, hashlib, random, string, os, sys

# Schema-Konstanten (aus existierender g3-2-Datei extrahiert)
SCHEMA = """
CREATE TABLE col (id integer PRIMARY KEY, crt integer NOT NULL, mod integer NOT NULL, scm integer NOT NULL, ver integer NOT NULL, dty integer NOT NULL, usn integer NOT NULL, ls integer NOT NULL, conf text NOT NULL, models text NOT NULL, decks text NOT NULL, dconf text NOT NULL, tags text NOT NULL);
CREATE TABLE notes (id integer PRIMARY KEY, guid text NOT NULL, mid integer NOT NULL, mod integer NOT NULL, usn integer NOT NULL, tags text NOT NULL, flds text NOT NULL, sfld text NOT NULL, csum integer NOT NULL, flags integer NOT NULL, data text NOT NULL);
CREATE TABLE cards (id integer PRIMARY KEY, nid integer NOT NULL, did integer NOT NULL, ord integer NOT NULL, mod integer NOT NULL, usn integer NOT NULL, type integer NOT NULL, queue integer NOT NULL, due integer NOT NULL, ivl integer NOT NULL, factor integer NOT NULL, reps integer NOT NULL, lapses integer NOT NULL, left integer NOT NULL, odue integer NOT NULL, odid integer NOT NULL, flags integer NOT NULL, data text NOT NULL);
CREATE TABLE revlog (id integer PRIMARY KEY, cid integer NOT NULL, usn integer NOT NULL, ease integer NOT NULL, ivl integer NOT NULL, lastIvl integer NOT NULL, factor integer NOT NULL, time integer NOT NULL, type integer NOT NULL);
CREATE TABLE graves (usn integer NOT NULL, oid integer NOT NULL, type integer NOT NULL);
CREATE INDEX ix_notes_usn ON notes (usn);
CREATE INDEX ix_cards_usn ON cards (usn);
CREATE INDEX ix_revlog_usn ON revlog (usn);
CREATE INDEX ix_cards_nid ON cards (nid);
CREATE INDEX ix_cards_sched ON cards (did, queue, due);
CREATE INDEX ix_revlog_cid ON revlog (cid);
CREATE INDEX ix_notes_csum ON notes (csum);
"""

CSS = ".card { font-family: 'Source Sans 3','Helvetica Neue',sans-serif; font-size: 18px; color: #1a1a1a; background: #f8f5ee; padding: 18px; line-height: 1.5; }i { color: #1a4f8a; font-style: italic; }b { color: #1a1a1a; }hr#answer { border: 0; border-top: 1px solid #c8c2b0; margin: 14px 0; }"

def guid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def fnv32(s):
    """FNV-1a 32-bit hash, similar to what Anki uses for sfld checksum."""
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b
        h = (h * 0x01000193) & 0xffffffff
    return h

def build_apkg(out_path, deck_name, deck_desc, cards):
    """Erstellt eine .apkg-Datei. cards: Liste von (front_html, back_html)-Paaren."""
    random.seed(hash(deck_name))  # deterministisch
    # IDs (deterministisch aus deck_name, damit reproduzierbar)
    base = abs(hash(deck_name))
    deck_id = (base & 0xffffffffffff) | 0x100000000000
    model_id = ((base >> 16) & 0xffffffffffff) | 0x100000000000
    crt = 1778025600  # Tagesgrenze (UTC midnight) — reproduzierbar
    mod = 1778050418  # Modifikationszeit

    conf = {"nextPos": 1, "estTimes": True, "activeDecks": [deck_id], "sortType": "noteFld",
            "timeLim": 0, "sortBackwards": False, "addToCur": True, "curDeck": deck_id,
            "newBury": True, "newSpread": 0, "dueCounts": True, "curModel": str(model_id),
            "collapseTime": 1200}

    models = {str(model_id): {
        "id": model_id, "name": "TALS Basic", "type": 0, "mod": mod, "usn": -1,
        "sortf": 0, "did": deck_id,
        "tmpls": [{"name": "Karte 1", "ord": 0, "qfmt": "{{Front}}",
                   "afmt": "{{Front}}<hr id=\"answer\">{{Back}}",
                   "did": None, "bqfmt": "", "bafmt": ""}],
        "flds": [{"name": "Front", "ord": 0, "sticky": False, "rtl": False,
                  "font": "Source Sans 3", "size": 16, "media": []},
                 {"name": "Back", "ord": 1, "sticky": False, "rtl": False,
                  "font": "Source Sans 3", "size": 16, "media": []}],
        "css": CSS,
        "latexPre": "\\documentclass[12pt]{article}\\usepackage{amssymb,amsmath}\\begin{document}",
        "latexPost": "\\end{document}",
        "req": [[0, "any", [0]]], "tags": [], "vers": []
    }}

    decks = {str(deck_id): {
        "id": deck_id, "name": deck_name, "extendRev": 50, "usn": -1, "collapsed": False,
        "newToday": [0, 0], "revToday": [0, 0], "lrnToday": [0, 0], "timeToday": [0, 0],
        "dyn": 0, "extendNew": 10, "conf": 1, "desc": deck_desc, "mod": mod,
        "browserCollapsed": False
    }}

    dconf = {"1": {"id": 1, "name": "Default", "replayq": True,
                   "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0},
                   "rev": {"perDay": 200, "ivlFct": 1.0, "maxIvl": 36500, "minSpace": 1, "ease4": 1.3,
                           "bury": False, "fuzz": 0.05, "hardFactor": 1.2},
                   "timer": 0, "maxTaken": 60, "usn": -1,
                   "new": {"perDay": 20, "delays": [1, 10], "separate": True, "ints": [1, 4, 7],
                           "initialFactor": 2500, "bury": False, "order": 1},
                   "mod": 0, "autoplay": True, "dyn": False}}

    # Build SQLite DB
    tmp_db = out_path + '.tmp.sqlite'
    if os.path.exists(tmp_db):
        os.remove(tmp_db)
    con = sqlite3.connect(tmp_db)
    cur = con.cursor()
    cur.executescript(SCHEMA)
    cur.execute("INSERT INTO col VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (1, crt, mod, mod*1000, 11, 0, 0, 0,
                 json.dumps(conf), json.dumps(models), json.dumps(decks), json.dumps(dconf), "{}"))

    note_base = mod * 1000
    for i, (front, back) in enumerate(cards):
        nid = note_base + i
        cid = nid + 1000000
        flds = front + "\x1f" + back
        sfld = front
        csum = fnv32(sfld) >> 0
        cur.execute("INSERT INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (nid, guid(), model_id, mod, -1, "", flds, sfld, csum, 0, ""))
        cur.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (cid, nid, deck_id, 0, mod, -1, 0, 0, i+1, 0, 0, 0, 0, 0, 0, 0, 0, ""))
    con.commit()
    con.close()

    # Build .apkg ZIP
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(tmp_db, 'collection.anki2')
        z.writestr('media', '{}')
    os.remove(tmp_db)
    return len(cards)


# ─── Cards für g5-1 Grundlagen ────────────────────────────────────────────
g51_cards = [
    ("Was ist eine geometrische Skizze?",
     "Eine vereinfachte zeichnerische Darstellung einer Aufgabe, die alle relevanten Eigenschaften (Längen, Winkel, Beziehungen) sichtbar macht. <b>Nicht massstabsgetreu</b>, aber topologisch korrekt."),
    ("Welche zwei Massen für Winkel werden verwendet?",
     "<b>Grad</b> (°) — voller Kreis = 360°<br><b>Radiant</b> (rad) — voller Kreis = 2π rad"),
    ("Umrechnungsformel Grad ↔ Radiant",
     "Aus 180° = π rad folgt:<br>φ<sub>rad</sub> = φ<sub>Grad</sub> · π / 180°<br>φ<sub>Grad</sub> = φ<sub>rad</sub> · 180° / π"),
    ("Wie viele Grad sind π/2 rad?",
     "π/2 · 180°/π = <b>90°</b> (rechter Winkel)"),
    ("Wie viele Grad sind π/6 rad?",
     "π/6 · 180°/π = <b>30°</b>"),
    ("Wie viele Grad sind π/4 rad?",
     "π/4 · 180°/π = <b>45°</b>"),
    ("Wie viele Grad sind π/3 rad?",
     "π/3 · 180°/π = <b>60°</b>"),
    ("Wie viele Grad sind 2π/3 rad?",
     "2π/3 · 180°/π = <b>120°</b>"),
    ("Was ist ein <i>spitzer</i> Winkel?",
     "Ein Winkel mit <b>0° &lt; α &lt; 90°</b>."),
    ("Was ist ein <i>rechter</i> Winkel?",
     "Ein Winkel mit <b>α = 90°</b> (= π/2 rad). Markiert mit kleinem Quadrat-Symbol."),
    ("Was ist ein <i>stumpfer</i> Winkel?",
     "Ein Winkel mit <b>90° &lt; α &lt; 180°</b>."),
    ("Was ist ein <i>gestreckter</i> Winkel?",
     "Ein Winkel mit <b>α = 180°</b> (= π rad). Beide Schenkel liegen in einer Geraden."),
    ("Was ist ein <i>überstumpfer</i> Winkel?",
     "Ein Winkel mit <b>180° &lt; α &lt; 360°</b>."),
    ("Was ist ein <i>Vollwinkel</i>?",
     "Ein Winkel mit <b>α = 360°</b> (= 2π rad). Eine ganze Drehung."),
    ("Was sind <i>Komplementärwinkel</i>?",
     "Zwei Winkel, die sich zu <b>90°</b> ergänzen: α + β = 90°. Beispiel: 35° und 55°."),
    ("Was sind <i>Supplementärwinkel</i>?",
     "Zwei Winkel, die sich zu <b>180°</b> ergänzen: α + β = 180°. Beispiel: 110° und 70°."),
    ("Was sind <i>Scheitelwinkel</i>?",
     "Beim Schnitt zweier Geraden die <b>gegenüberliegenden</b> Winkel — sie sind <b>gleich gross</b>."),
    ("Was sind <i>Nebenwinkel</i>?",
     "Beim Schnitt zweier Geraden die <b>benachbarten</b> Winkel — sie sind <b>supplementär</b> (α + β = 180°)."),
    ("Workflow zum Skizzieren — die vier Schritte",
     "<b>1. Lesen</b> — Aufgabe zweimal lesen, Zahlen markieren<br><b>2. Skizzieren</b> — grobe Form aufs Papier<br><b>3. Beschriften</b> — Gegebenes mit Werten, Gesuchtes mit Variablen<br><b>4. Prüfen</b> — Resultat plausibel?"),
    ("Was bedeutet DEG/RAD am Taschenrechner?",
     "<b>DEG</b>: Winkel im <b>Grad</b>. <b>RAD</b>: Winkel im <b>Radiant</b>. Falscher Modus → falsches Resultat trotz richtiger Eingabe."),
    ("Drei Strategien zur Plausibilitätsprüfung",
     "<b>1. Grössenordnung</b> — vergleiche mit bekannten Längen<br><b>2. Schranken</b> — Hypotenuse länger als jede Kathete, kürzer als Summe<br><b>3. Spezialfall</b> — Sonderwerte einsetzen"),
    ("Was ist die Bogenlänge auf dem Einheitskreis bei Winkel φ?",
     "Genau <b>φ</b> — wenn φ im <b>Radiant</b> gegeben ist. Das ist die Definition von Radiant."),
    ("Wie gross ist das Komplement von 27°?",
     "90° − 27° = <b>63°</b>"),
    ("Wie gross ist das Supplement von 142°?",
     "180° − 142° = <b>38°</b>"),
    ("Welcher Winkel ist π rad?",
     "<b>180°</b> — der gestreckte Winkel."),
]

# ─── Cards für g5-2 Planimetrie ────────────────────────────────────────────
g52_cards = [
    ("Umfang und Fläche eines Quadrats mit Seite a",
     "U = <b>4·a</b><br>A = <b>a²</b>"),
    ("Umfang und Fläche eines Rechtecks mit Seiten a und b",
     "U = <b>2·(a + b)</b><br>A = <b>a · b</b>"),
    ("Umfang und Fläche eines Parallelogramms",
     "U = <b>2·(a + b)</b> mit b = Schenkel<br>A = <b>a · h</b> mit h = Höhe (nicht b!)"),
    ("Fläche eines Rhombus mit Diagonalen e und f",
     "A = <b>(e · f) / 2</b><br>Seitenlänge: a = √((e/2)² + (f/2)²)"),
    ("Fläche eines Trapezes mit Parallelseiten a, c und Höhe h",
     "A = <b>((a + c) / 2) · h</b> = <b>m · h</b><br>m = Mittellinie = (a + c) / 2"),
    ("Was ist die Mittellinie im Trapez?",
     "Die Strecke, die die <b>Mittelpunkte der nicht-parallelen Schenkel</b> verbindet. Sie ist parallel zu a und c und hat die Länge <b>m = (a + c) / 2</b>."),
    ("Vierecks-Hierarchie — von allgemein zu speziell",
     "<b>Trapez</b> → Parallelogramm → Rechteck / Rhombus → Quadrat. Jede speziellere Figur erbt alle Eigenschaften der allgemeineren."),
    ("Welche Eigenschaft macht aus einem Parallelogramm ein Rechteck?",
     "Mindestens ein <b>rechter Winkel</b> (dann sind alle vier rechtwinklig)."),
    ("Welche Eigenschaft macht aus einem Parallelogramm einen Rhombus?",
     "Alle vier <b>Seiten gleich lang</b>."),
    ("Welche Eigenschaft macht aus einem Rechteck ein Quadrat?",
     "Alle vier <b>Seiten gleich lang</b>."),
    ("Fläche eines allgemeinen Dreiecks",
     "A = <b>(g · h) / 2</b><br>g = Grundseite, h = zugehörige Höhe"),
    ("Fläche eines gleichseitigen Dreiecks mit Seite a",
     "A = <b>a² · √3 / 4</b><br>Höhe: h = a · √3 / 2"),
    ("Was ist eine Höhe im Dreieck?",
     "Die Strecke von einer Ecke <b>senkrecht</b> zur gegenüberliegenden Seite (oder deren Verlängerung). Schnittpunkt der drei Höhen: <b>Höhenschnittpunkt H</b>."),
    ("Was ist eine Seitenhalbierende?",
     "Die Strecke von einer Ecke zum <b>Mittelpunkt</b> der gegenüberliegenden Seite. Schnittpunkt: <b>Schwerpunkt S</b> — teilt jede Seitenhalbierende im Verhältnis <b>2 : 1</b>."),
    ("Was ist eine Winkelhalbierende?",
     "Strahl, der einen Innenwinkel in <b>zwei gleiche Teile</b> teilt. Schnittpunkt der drei Winkelhalbierenden: <b>Inkreismittelpunkt I</b>."),
    ("Was ist eine Mittelsenkrechte?",
     "Gerade, die <b>senkrecht durch den Mittelpunkt</b> einer Seite verläuft. Schnittpunkt der drei Mittelsenkrechten: <b>Umkreismittelpunkt U</b>."),
    ("Vier Linien, vier Schnittpunkte im Dreieck — Übersicht",
     "<b>Höhen</b> → Höhenschnittpunkt H<br><b>Seitenhalbierende</b> → Schwerpunkt S<br><b>Winkelhalbierende</b> → Inkreismittelpunkt I<br><b>Mittelsenkrechten</b> → Umkreismittelpunkt U"),
    ("Was ist eine <i>Sehne</i> im Kreis?",
     "Eine <b>Strecke</b>, deren beide Endpunkte auf der Kreislinie liegen."),
    ("Was ist eine <i>Sekante</i>?",
     "Eine <b>Gerade</b>, die den Kreis in <b>zwei Punkten</b> schneidet (eine Sehne, beidseitig verlängert)."),
    ("Was ist eine <i>Tangente</i>?",
     "Eine Gerade, die den Kreis in <b>genau einem Punkt</b> berührt. Sie steht <b>senkrecht</b> auf dem Radius zum Berührpunkt."),
    ("Was ist ein <i>Sektor</i>?",
     'Das „Tortenstück" — die Fläche, die von <b>zwei Radien und einem Bogen</b> begrenzt wird.'),
    ("Was ist ein <i>Segment</i>?",
     'Die „Linsenform" — die Fläche, die von einer <b>Sehne und einem Bogen</b> begrenzt wird.'),
    ("Umfang und Fläche eines Kreises mit Radius r",
     "U = <b>2π · r</b><br>A = <b>π · r²</b>"),
    ("Bogenlänge im Kreis",
     "Mit Winkel im <b>Radiant</b>: b = <b>r · φ</b><br>Mit Winkel im <b>Grad</b>: b = π · r · α / 180°"),
    ("Sektorfläche im Kreis",
     "Mit Winkel im <b>Radiant</b>: A = <b>r² · φ / 2</b><br>Mit Winkel im <b>Grad</b>: A = π · r² · α / 360°"),
    ("Wann sind zwei Figuren <i>ähnlich</i>?",
     "Wenn <b>entsprechende Winkel gleich</b> sind und <b>entsprechende Seiten im selben Verhältnis</b> stehen (Ähnlichkeitsfaktor k)."),
    ("Wie skalieren Längen, Flächen, Volumen bei Ähnlichkeit?",
     "Längen wachsen mit <b>k</b><br>Flächen wachsen mit <b>k²</b><br>Volumen wachsen mit <b>k³</b><br>Beispiel k=2: Länge ×2, Fläche ×4, Volumen ×8"),
    ("Wann gilt der Strahlensatz?",
     "Wenn zwei sich schneidende Strahlen von <b>zwei parallelen Geraden</b> geschnitten werden. Es gilt: a<sub>1</sub> / a<sub>2</sub> = b<sub>1</sub> / b<sub>2</sub>."),
    ("Pythagoras im rechtwinkligen Dreieck",
     "Hypotenuse c, Katheten a und b: <b>c² = a² + b²</b>"),
    ("Plausibilitätsschranken für die Diagonale eines Rechtecks",
     "Diagonale d ist <b>länger</b> als jede Seite und <b>kürzer</b> als die Summe der Seiten. Beispiel 8×6: 8 &lt; d &lt; 14 (echtes d = 10)."),
]

# ─── Cards für g5-2a Dreiecke ─────────────────────────────────────────
g52a_cards = [
    # Bezeichnungen
    ("Bezeichnung der Seiten im Dreieck",
     "Eine Seite heisst stets nach dem <b>gegenüberliegenden Eckpunkt</b>: a = BC (gegenüber A), b = CA (gegenüber B), c = AB (gegenüber C)."),
    ("Innenwinkelsumme im Dreieck",
     "α + β + γ = <b>180°</b>. Folgt aus dem Wechselwinkelsatz an einer Parallelen durch C zur Seite c."),
    ("Was ist ein <i>Aussenwinkel</i>?",
     "Der Nebenwinkel eines Innenwinkels: α' = <b>180° − α</b>. Jeder Eckpunkt hat einen Aussenwinkel."),
    ("Aussenwinkelsumme",
     "α' + β' + γ' = <b>360°</b>."),
    ("Aussenwinkelsatz",
     "Jeder Aussenwinkel ist gleich der Summe der beiden <b>nicht anliegenden</b> Innenwinkel: α' = <b>β + γ</b>."),

    # Spezielle Dreiecke
    ("Was ist ein <i>gleichschenkliges</i> Dreieck?",
     "Ein Dreieck mit <b>zwei gleich langen Seiten</b> (Schenkeln). Die beiden Basiswinkel sind gleich gross."),
    ("Was ist ein <i>gleichseitiges</i> Dreieck?",
     "Ein Dreieck mit <b>drei gleich langen Seiten</b>. Alle Innenwinkel betragen <b>60°</b>."),
    ("Was ist ein <i>rechtwinkliges</i> Dreieck?",
     "Ein Dreieck mit einem Innenwinkel von <b>90°</b>. Die Seite gegenüber dem rechten Winkel heisst <b>Hypotenuse</b> und ist die längste Seite."),
    ("Höhe im gleichseitigen Dreieck mit Seite s",
     "h = <b>s · √3 / 2</b>. (Folgt aus dem halben gleichseitigen Dreieck mit Seitenverhältnis 1 : √3 : 2.)"),

    # Dreieckselemente
    ("Was ist eine <i>Höhe</i> im Dreieck?",
     "Strecke von einer Ecke <b>senkrecht</b> zur gegenüberliegenden Seite (oder deren Verlängerung). Schnittpunkt der drei Höhen: <b>Höhenschnittpunkt H</b>."),
    ("Wo liegt der Höhenschnittpunkt?",
     "Bei <b>spitzwinkligen</b> Dreiecken im Innern, bei <b>rechtwinkligen</b> auf der Ecke C, bei <b>stumpfwinkligen</b> ausserhalb."),
    ("Was ist eine <i>Seitenhalbierende</i>?",
     "Strecke von einer Ecke zum <b>Mittelpunkt</b> der gegenüberliegenden Seite. Schnittpunkt: <b>Schwerpunkt S</b>, teilt jede im Verhältnis <b>2 : 1</b> vom Eckpunkt."),
    ("Was ist eine <i>Mittelsenkrechte</i>?",
     "Gerade, die <b>senkrecht</b> durch den <b>Mittelpunkt einer Seite</b> verläuft. Schnittpunkt: <b>Umkreismittelpunkt M<sub>U</sub></b> — gleich weit von allen Eckpunkten."),
    ("Was ist eine <i>Winkelhalbierende</i>?",
     "Strahl, der einen Innenwinkel in <b>zwei gleiche Teile</b> teilt. Schnittpunkt: <b>Inkreismittelpunkt M<sub>I</sub></b> — gleich weit von allen Seiten."),
    ("Vier merkwürdige Punkte — Übersicht",
     "<b>Höhen</b> → H<br><b>Seitenhalbierende</b> → S (2:1)<br><b>Mittelsenkrechte</b> → M<sub>U</sub> (Umkreis)<br><b>Winkelhalbierende</b> → M<sub>I</sub> (Inkreis)"),

    # Konstruktion und Kongruenz
    ("Was bedeutet <i>kongruent</i>?",
     "<b>Deckungsgleich</b> — durch Drehung, Spiegelung oder Verschiebung exakt zur Deckung zu bringen."),
    ("Kongruenzsatz <b>SSS</b>",
     "Drei Seiten gegeben. Eindeutig, wenn die <b>Dreiecksungleichung</b> erfüllt ist."),
    ("Kongruenzsatz <b>SWS</b>",
     "Zwei Seiten und der <b>eingeschlossene</b> Winkel. Immer eindeutig."),
    ("Kongruenzsatz <b>WSW</b>",
     "Eine Seite und die beiden <b>anliegenden</b> Winkel. Eindeutig, solange α + β &lt; 180°."),
    ("Kongruenzsatz <b>SsW</b>",
     "Zwei Seiten und der Winkel <b>gegenüber der grösseren</b> Seite (Grossbuchstabe S — kleines s). Eindeutig."),
    ("Achtung: <b>sSW</b> — Winkel gegenüber kleinerer Seite",
     "Im Allgemeinen <b>nicht eindeutig</b>. Es gibt 0, 1 oder 2 Lösungen je nach Verhältnis von b·sin(α) zu a."),
    ("Was ist die <i>Dreiecksungleichung</i>?",
     "Jede Seite ist <b>kürzer als die Summe</b> und <b>länger als die Differenz</b> der beiden anderen. Reicht zu prüfen: längste Seite &lt; Summe der anderen zwei."),

    # Fläche
    ("Fläche eines allgemeinen Dreiecks",
     "A = <b>(g · h) / 2</b><br>g = beliebige Grundseite, h = zugehörige Höhe."),
    ("Fläche eines gleichseitigen Dreiecks mit Seite s",
     "A = <b>s² · √3 / 4</b>."),
    ("Fläche eines rechtwinkligen Dreiecks (Katheten a, b)",
     "A = <b>(a · b) / 2</b>."),

    # Pythagoras
    ("Satz des Pythagoras",
     "Im rechtwinkligen Dreieck mit Hypotenuse c und Katheten a, b: <b>a² + b² = c²</b>."),
    ("Kathetensatz des Euklid",
     "Im rechtwinkligen Dreieck mit Hypotenusenabschnitten p (unter a) und q (unter b):<br>a² = <b>p · c</b><br>b² = <b>q · c</b>."),
    ("Höhensatz des Euklid",
     "Höhe h auf der Hypotenuse, Hypotenusenabschnitte p und q: <b>h² = p · q</b>."),
    ("Kehrsatz des Pythagoras",
     "Wenn in einem Dreieck a² + b² = c² gilt (mit c als längster Seite), dann ist es <b>rechtwinklig</b> mit rechtem Winkel gegenüber c."),

    # Spezialdreiecke
    ("Seitenverhältnis 30°-60°-90°-Dreieck",
     "<b>1 : √3 : 2</b>. Entsteht beim Halbieren eines gleichseitigen Dreiecks."),
    ("Seitenverhältnis 45°-45°-90°-Dreieck",
     "<b>1 : 1 : √2</b>. Entsteht beim Halbieren eines Quadrats entlang der Diagonale."),
    ("Drei bekannte pythagoreische Tripel",
     "<b>(3, 4, 5)</b>, <b>(5, 12, 13)</b>, <b>(8, 15, 17)</b>. Vielfache (z.B. 6, 8, 10) sind ebenfalls Tripel."),
]


# ─── Cards für g5-2b Vierecke ─────────────────────────────────────────
g52b_cards = [
    # Innenwinkelsumme
    ("Innenwinkelsumme im Viereck",
     "α + β + γ + δ = <b>360°</b>. Beweis: Eine Diagonale teilt das Viereck in zwei Dreiecke à 180°."),
    ("Innenwinkelsumme im n-Eck",
     "σ_n = <b>(n − 2) · 180°</b>. Folgt aus der Zerlegung in n−2 Dreiecke, ausgehend von einem Eckpunkt."),
    ("Anzahl Diagonalen im n-Eck",
     "<b>n · (n − 3) / 2</b>. Im Achteck: 8·5/2 = 20 Diagonalen."),

    # Hierarchie
    ("Vierecks-Hierarchie",
     "Viereck → <b>Trapez</b> → Parallelogramm → Rechteck / Rhombus → Quadrat. Jede speziellere Form erbt alle Eigenschaften der allgemeineren."),
    ("Was ist ein <i>Trapez</i>?",
     "Ein Viereck mit <b>mindestens einem Paar paralleler Seiten</b>. Die parallelen Seiten heissen a und c, die Schenkel b und d."),
    ("Was ist ein <i>Parallelogramm</i>?",
     "Ein Viereck, in dem <b>beide Seitenpaare parallel</b> sind. Folgerung: Gegenseiten gleich lang, Diagonalen halbieren sich."),
    ("Was ist ein <i>Rechteck</i>?",
     "Ein Parallelogramm mit <b>einem rechten Winkel</b> (dann sind alle vier 90°). Folgerung: Diagonalen sind gleich lang."),
    ("Was ist ein <i>Rhombus</i> (Raute)?",
     "Ein Parallelogramm mit <b>allen vier Seiten gleich lang</b>. Folgerung: Diagonalen stehen senkrecht aufeinander und halbieren die Innenwinkel."),
    ("Was ist ein <i>Quadrat</i>?",
     "<b>Rechteck und Rhombus zugleich</b>: alle Seiten gleich, alle Winkel 90°."),
    ("Was ist ein <i>Drachenviereck</i>?",
     "Viereck mit <b>zwei Paaren gleich langer benachbarter Seiten</b>. Eine Symmetrieachse, Diagonalen senkrecht."),
    ("Unterschied Rhombus und Drachen",
     "Rhombus: <b>alle vier Seiten gleich</b>. Drachen: <b>zwei Paare</b> benachbarter gleicher Seiten, beide Paare nicht zwingend gleich lang. Jeder Rhombus ist Drachen, nicht umgekehrt."),

    # Mittellinie
    ("Mittellinie im Trapez",
     "Strecke, die die <b>Mittelpunkte der Schenkel</b> verbindet. Länge: m = <b>(a + c) / 2</b>. Parallel zu a und c. Daraus: A = m · h."),

    # Umfang und Fläche
    ("Fläche Quadrat (Seite a)",
     "A = <b>a²</b>; Umfang U = 4a."),
    ("Fläche Rechteck (Seiten a, b)",
     "A = <b>a · b</b>; Umfang U = 2(a + b)."),
    ("Fläche Parallelogramm",
     "A = <b>g · h</b> mit g = Grundseite, h = Höhe (nicht der Schenkel!). Umfang U = 2(a + b)."),
    ("Fläche Trapez",
     "A = <b>½ · (a + c) · h</b> = m · h. Höhe h ist der senkrechte Abstand der parallelen Seiten."),
    ("Fläche Rhombus oder Drachen (Diagonalen e, f)",
     "A = <b>½ · e · f</b>. Gilt für alle Vierecke mit senkrecht aufeinander stehenden Diagonalen."),

    # Diagonalen
    ("Eigenschaften der Diagonalen im Parallelogramm",
     "Sie <b>halbieren sich gegenseitig</b> im Schnittpunkt."),
    ("Eigenschaften der Diagonalen im Rechteck",
     "Sie halbieren sich UND sind <b>gleich lang</b>."),
    ("Eigenschaften der Diagonalen im Rhombus",
     "Sie halbieren sich, stehen <b>senkrecht aufeinander</b> und halbieren die Innenwinkel."),

    # Sehnen- und Tangentenviereck
    ("Was ist ein <i>Sehnenviereck</i>?",
     "Ein Viereck, dessen vier Eckpunkte <b>auf einem gemeinsamen Kreis</b> (Umkreis) liegen."),
    ("Charakterisierung Sehnenviereck",
     "<b>α + γ = 180°</b> und <b>β + δ = 180°</b> — gegenüberliegende Innenwinkel ergänzen sich auf 180°."),
    ("Was ist ein <i>Tangentenviereck</i>?",
     "Ein Viereck, in das ein <b>Inkreis</b> passt (berührt alle vier Seiten von innen)."),
    ("Charakterisierung Tangentenviereck",
     "<b>a + c = b + d</b> — Summen gegenüberliegender Seiten sind gleich."),
    ("Welche Vierecke sind immer Sehnenvierecke?",
     "<b>Rechteck</b> und <b>Quadrat</b>. Auch <b>gleichschenkliges Trapez</b>."),
    ("Welche Vierecke sind immer Tangentenvierecke?",
     "<b>Quadrat, Rhombus, Drachen</b>."),

    # Regelmässige Vielecke
    ("Was ist ein <i>regelmässiges</i> n-Eck?",
     "Ein n-Eck mit <b>allen Seiten gleich lang</b> UND <b>allen Innenwinkeln gleich gross</b>. Hat einen Umkreis (R) und einen Inkreis (Apothem r)."),
    ("Zentriwinkel im regelmässigen n-Eck",
     "ζ_n = <b>360° / n</b>. Beispiele: ζ_3 = 120°, ζ_4 = 90°, ζ_6 = 60°."),
    ("Innenwinkel im regelmässigen n-Eck",
     "α_n = <b>180° − ζ_n</b> = (n−2)·180°/n. Beispiele: α_6 = 120°, α_8 = 135°."),
    ("Seitenlänge im regelmässigen n-Eck",
     "s = <b>2R · sin(ζ_n / 2)</b>. Im Sechseck: s = R (ohne Trigonometrie, weil das Sechseck aus sechs gleichseitigen Dreiecken besteht)."),
    ("Inkreisradius (Apothem) im regelmässigen n-Eck",
     "r = <b>R · cos(ζ_n / 2)</b>. Die Höhe eines Bestimmungsdreiecks vom Mittelpunkt zur Seitenmitte."),
    ("Regelmässiges Sechseck — exakte Werte",
     "Mit Umkreisradius R: <b>s = R</b>, <b>r = R√3/2</b>. Zentriwinkel 60°, Innenwinkel 120°. Zerlegt in 6 gleichseitige Dreiecke."),
    ("Regelmässiges Dreieck (gleichseitig) — exakte Werte",
     "Mit Umkreisradius R: <b>s = R√3</b>, <b>r = R/2</b>. Zentriwinkel 120°, Innenwinkel 60°."),
    ("Regelmässiges Quadrat — exakte Werte",
     "Mit Umkreisradius R: <b>s = R√2</b>, <b>r = R√2/2</b>. Zentriwinkel 90°, Innenwinkel 90°."),
    ("Fläche regelmässiges n-Eck",
     "A = <b>½ · n · s · r</b> = ½ · U · r. Halber Umfang mal Apothem."),
]


g52c_cards = [
    # Grundlagen
    ('Definition: Kreis (Mittelpunkt M, Radius r)',
     'Menge aller Punkte in der Ebene mit Abstand <b>r</b> zum Mittelpunkt <b>M</b>.'),
    ('Was ist der <i>Durchmesser</i> d eines Kreises?',
     'Strecke durch M, die beide Kreislinien-Punkte verbindet. Es gilt <b>d = 2r</b>.'),
    ('Was ist eine <i>Sehne</i>?',
     'Eine <b>Strecke</b>, die zwei Punkte der Kreislinie verbindet (ohne durch M zu gehen).'),
    ('Was ist eine <i>Sekante</i>?',
     'Eine <b>Gerade</b>, die die Kreislinie in zwei Punkten schneidet.'),
    ('Was ist eine <i>Tangente</i>?',
     'Eine <b>Gerade</b>, die die Kreislinie in genau einem Punkt berührt. Sie steht dort <b>senkrecht</b> auf dem Radius.'),
    ('Was ist eine <i>Passante</i>?',
     'Eine <b>Gerade</b>, die die Kreislinie <b>nicht</b> schneidet (verläuft komplett ausserhalb).'),
    ('Welche Symbole sind Strecken, welche Geraden?',
     'Strecken: <b>r</b> (Radius), <b>d</b> (Durchmesser), <b>s</b> (Sehne).<br>Geraden: <b>g</b> (Sekante), <b>t</b> (Tangente), <b>p</b> (Passante).'),
    ('Tangenten-Eigenschaft',
     'Die Tangente steht im <b>Berührungspunkt senkrecht</b> auf dem Radius: t ⊥ r.'),

    # Pi
    ('Definition der Kreiszahl π',
     'π = <b>U / d</b> = Umfang geteilt durch Durchmesser. Bei jedem Kreis gleich.'),
    ('Ungefährer Wert von π (5 Stellen)',
     '<b>π ≈ 3,14159</b>.'),
    ('Eigenschaften von π',
     'π ist <b>irrational</b> (kein Bruch) und sogar <b>transzendent</b> (nicht Lösung einer Polynomgleichung mit rationalen Koeffizienten).'),
    ('Pi-Schranken: einbeschriebenes n-Eck im Einheitskreis',
     'u_n / d = <b>n · sin(180°/n)</b>. Bei n = 6: u_6/d = 3 (untere Schranke).'),
    ('Pi-Schranken: umschriebenes n-Eck im Einheitskreis',
     'U_n / d = <b>n · tan(180°/n)</b>. Bei n = 6: U_6/d = 2√3 ≈ 3,4641 (obere Schranke).'),
    ('Was leistete Archimedes mit n = 96?',
     'Er klemmte π ein: 3,1408 &lt; π &lt; 3,1429 — drei Nachkommastellen gesichert.'),

    # Kreis: Umfang und Fläche
    ('Kreis-Umfang (Formeln)',
     'U = <b>2πr = πd</b>.'),
    ('Kreis-Fläche (Formeln)',
     'A = <b>πr² = πd² / 4</b>.'),
    ('Herleitung der Flächenformel (Idee)',
     'Kreis in viele Sektoren schneiden, abwechselnd auflegen → Quasi-Rechteck mit Höhe r und Breite πr. Fläche = πr · r = <b>πr²</b>.'),

    # Kreisring
    ('Definition: Kreisring',
     'Bereich zwischen zwei konzentrischen Kreisen mit Aussenradius <b>R</b> und Innenradius <b>r</b>.'),
    ('Kreisring: Breite und mittlerer Radius',
     'Breite: <b>b = R − r</b>. Mittlerer Radius: <b>r_m = (R + r) / 2</b>.'),
    ('Kreisring: Flächenformeln (drei Varianten)',
     'A = R²π − r²π = <b>(R − r)(R + r)π</b> = <b>2π · r_m · b</b>.'),
    ('Anschauliche Bedeutung von A = 2π r_m · b',
     '„Mittlerer Umfang mal Breite" — aufgeschnittener Ring ≈ Rechteck mit Länge U_Mitte und Breite b.'),

    # Kreissektor
    ('Definition: Kreissektor (Kreisausschnitt)',
     'Bereich zwischen zwei Radien und dem dazugehörigen Bogen. Gekennzeichnet durch Radius r und Zentriwinkel φ.'),
    ('Bogenlänge eines Sektors (Grad)',
     '<b>b = r · π · φ / 180°</b> = (φ / 360°) · 2πr.'),
    ('Sektorfläche (zwei Formen)',
     'A_SK = <b>r² · π · φ / 360°</b> = <b>½ · b · r</b>.'),
    ('Spezialfall Sektor: Halbkreis (φ = 180°)',
     'A_SK = ½ πr², b = πr.'),
    ('Spezialfall Sektor: Viertelkreis (φ = 90°)',
     'A_SK = ¼ πr², b = ½ πr. Anteil am Vollkreis: 25 %.'),

    # Kreissegment
    ('Definition: Kreissegment (Kreisabschnitt)',
     'Bereich zwischen einer Sehne und dem zugehörigen Kreisbogen.'),
    ('Sehne s im Kreissegment (in Abhängigkeit von r und φ)',
     '<b>s = 2r · sin(φ/2)</b>.'),
    ('Segmenthöhe h im Kreissegment',
     '<b>h = r · (1 − cos(φ/2))</b>.'),
    ('Pythagoras-Beziehung im Segment',
     '(s/2)² + (r − h)² = <b>r²</b>. (Verbindet s, h und r.)'),
    ('Segmentfläche (Hauptformel)',
     'A_SG = A_Sektor − A_Dreieck = <b>r² π φ / 360° − s(r − h) / 2</b>.'),
    ('Beziehung Bogen ↔ Sektorfläche',
     'A_SK = <b>½ · b · r</b> — wie Dreiecksformel: halbe „Grundseite" mal Höhe.'),
]


g11_cards = [
    ("Was ist ein <i>Term</i>?",
     "Ein mathematischer Ausdruck, der aus <b>Zahlen</b>, <b>Variablen</b> und <b>Operationen</b> aufgebaut ist. Beispiel: 3·(x + 2)² − 5."),
    ("Was ist eine <i>Variable</i>?",
     "Ein Buchstabe, der für eine (zunächst unbestimmte) Zahl steht. Beispiele: x, y, t, n."),
    ("Was ist die <i>Hauptoperation</i> eines Terms?",
     "Die Operation, die <b>als letzte</b> ausgeführt würde, wenn man konkrete Werte einsetzt. Sie steht im Strukturbaum ganz oben."),
    ("Hauptoperation von 3·(x + 2)² − 5?",
     "<b>Subtraktion</b> (das − 5 wird als letztes ausgeführt)."),
    ("Hauptoperation von (a + b)·(c + d)?",
     "<b>Multiplikation</b> der zwei Klammern."),
    ("Hauptoperation von 2x² + 3x?",
     "<b>Addition</b> der zwei Summanden 2x² und 3x."),
    ("Hierarchie der Operationen — Reihenfolge",
     "<b>1. Klammern</b><br><b>2. Potenzen und Wurzeln</b><br><b>3. Punkt vor Strich</b> (·, : vor +, −)<br><b>4. Von links nach rechts</b> bei gleicher Stufe"),
    ("Was sagt das <i>Kommutativgesetz</i>?",
     "Reihenfolge ist egal:<br>a + b = b + a<br>a · b = b · a<br><b>Gilt nicht</b> für Subtraktion und Division."),
    ("Was sagt das <i>Assoziativgesetz</i>?",
     "Klammern sind egal:<br>(a + b) + c = a + (b + c)<br>(a · b) · c = a · (b · c)<br><b>Gilt nicht</b> für Subtraktion und Division."),
    ("Was sagt das <i>Distributivgesetz</i>?",
     "Multiplikation verteilt sich auf Addition:<br>a · (b + c) = a · b + a · c"),
    ("Was ist ein <i>Strukturbaum</i>?",
     "Eine Baumdarstellung eines Terms. Die <b>Wurzel</b> ist die Hauptoperation, die <b>Blätter</b> sind Zahlen oder Variablen."),
    ("Welche Strategie hilft beim Erkennen der Struktur?",
     "Den Term <b>von aussen nach innen</b> lesen. Was würde man zuletzt ausrechnen? Diese Operation ist die Hauptoperation."),
    ("Warum ist 2 + 3 · 4 = 14 und nicht 20?",
     "Punkt vor Strich: <b>3 · 4 = 12</b> wird zuerst gerechnet, dann <b>2 + 12 = 14</b>."),
    ("Wie behandelt man verschachtelte Klammern?",
     "Von <b>innen nach aussen</b>: erst die innersten Klammern, dann die äusseren."),
    ("Was bedeutet \u201ealgebraisch denken\u201c?",
     "Die <b>Struktur</b> eines Terms erkennen, ohne konkrete Zahlen einzusetzen. Beispiel: (a + b)² folgt der binomischen Formel — egal welche Werte a und b haben."),
]


# ─── Cards für g1-2 Zahlen und Grundoperationen ─────────────────────────
g12_cards = [
    ("Was ist ℕ?",
     "<b>Natürliche Zahlen</b>: 0, 1, 2, 3, … (zählende Zahlen).<br><i>Beispiele</i>: 0, 7, 42 sind in ℕ — die Anzahl Schüler einer Klasse, Hausnummern."),
    ("Was ist ℤ?",
     "<b>Ganze Zahlen</b>: …, −2, −1, 0, 1, 2, … (positive und negative ganze Zahlen plus Null).<br><i>Beispiele</i>: −5°C (Temperatur unter null), Bilanzveränderung −1200 Fr., Höhenmeter +345."),
    ("Was ist ℚ?",
     "<b>Rationale Zahlen</b>: alle Zahlen, die als Bruch p/q (mit p ∈ ℤ, q ∈ ℕ*) geschrieben werden können. Dezimaldarstellung: endlich oder periodisch.<br><i>Beispiele</i>: 3/4 = 0.75, −7/2 = −3.5, 1/3 = 0.333…"),
    ("Was ist ℝ?",
     "<b>Reelle Zahlen</b>: alle rationalen Zahlen <b>plus</b> die irrationalen (z. B. √2, π, e). Dezimaldarstellung: endlich, periodisch oder unendlich nicht-periodisch.<br><i>Beispiele</i>: 5, −1/2, √2 = 1.414…, π = 3.14159… — alle in ℝ."),
    ("Hierarchie der Zahlenmengen",
     "<b>ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ</b><br>Jede natürliche Zahl ist auch ganz, jede ganze auch rational, jede rationale auch reell.<br><i>Beispiel</i>: 5 ist in <em>allen vier</em> Mengen; −3 nur in ℤ, ℚ, ℝ; 1/2 nur in ℚ und ℝ; √2 nur in ℝ."),
    ("Beispiele für irrationale Zahlen",
     "<b>√2, √3, π, e</b>. Sie sind reell, aber nicht rational — keine Bruchdarstellung möglich.<br><i>Konkrete Werte</i>: √2 ≈ 1.41421…, π ≈ 3.14159…, e ≈ 2.71828… — alle mit unendlich vielen nicht-periodischen Nachkommastellen."),
    ("Wandle 0.75 in einen Bruch um",
     "0.75 = <b>75/100 = 3/4</b>. (Kürzen mit 25.)"),
    ("Wandle 3/8 in eine Dezimalzahl um",
     "3 ÷ 8 = <b>0.375</b> (endliche Dezimalzahl)."),
    ("Wandle 1/3 in eine Dezimalzahl um",
     "1 ÷ 3 = <b>0.333…</b> = 0.<span style='text-decoration:overline'>3</span> (periodisch)."),
    ("Was ist ein <i>Intervall</i>?",
     "Eine zusammenhängende Teilmenge von ℝ. Schreibweise:<br>[a; b]: a und b enthalten<br>]a; b[: a und b ausgeschlossen<br>[a; b[: a enthalten, b ausgeschlossen"),
    ("Was bedeutet [3; 7]?",
     "Alle reellen Zahlen <b>von 3 bis 7</b>, beide Grenzen <b>inklusive</b>."),
    ("Was bedeutet ]−∞; 5[?",
     "Alle reellen Zahlen <b>kleiner als 5</b> (5 nicht enthalten). −∞ ist nie eingeschlossen."),
    ("Vorzeichenregel: (−3) · (−4) = ?",
     "<b>+12</b>. Minus mal Minus = Plus."),
    ("Vorzeichenregel: (−3) · (+4) = ?",
     "<b>−12</b>. Minus mal Plus = Minus."),
    ("Was ist der <i>Betrag</i> einer Zahl?",
     "Der Abstand zur Null: |3| = 3, |−3| = 3, |0| = 0. Immer ≥ 0."),
    ("Wie rundet man 3.567 auf 1 Nachkommastelle?",
     "Nachkomma-2 ist 6 (≥ 5) → aufrunden: <b>3.6</b>."),
    ("Wie rundet man 3.547 auf 1 Nachkommastelle?",
     "Nachkomma-2 ist 4 (&lt; 5) → abrunden: <b>3.5</b>. <i>Grenzfall &bdquo;bei genau 5&ldquo;</i>: kaufmännische Rundung (Schule, Banken) rundet 3.55 → 3.6 (immer auf). Wissenschaftliche Rundung (Physik, Statistik) rundet 3.55 → 3.6 und 3.45 → 3.4 (auf gerade Stelle, &bdquo;banker rounding&ldquo;) — gleicht Rundungsfehler über viele Werte aus."),
    ("Was ist die <i>Hierarchie der Operationen</i>?",
     "<b>Klammern → Potenzen/Wurzeln → Punktrechnung → Strichrechnung</b>"),
    ("Berechne ohne Hilfsmittel: −2 + 3 · (−4)",
     "Punkt vor Strich: 3 · (−4) = −12. Dann: −2 + (−12) = <b>−14</b>."),
    ("Berechne ohne Hilfsmittel: (−6) : (−2) − 4",
     "(−6) : (−2) = +3. Dann 3 − 4 = <b>−1</b>."),
    ("Was ist die <i>Ordnungsrelation</i>?",
     "Vergleich zwischen Zahlen: a &lt; b, a &gt; b, a = b, a ≤ b, a ≥ b. Auf der Zahlengeraden: <b>links = kleiner</b>."),
    ("Welche Zahlenmenge enthält die Lösung von x² = 2?",
     "<b>ℝ</b>. x = ±√2 — also <b>zwei Lösungen</b>: x₁ = +√2 ≈ +1.414 und x₂ = −√2 ≈ −1.414. Beide sind irrational, also nicht in ℚ. Wichtig: eine quadratische Gleichung hat in ℝ üblicherweise <em>zwei</em> Lösungen (Symmetrie des Quadrierens)."),
    ("Wie schreibt man \u201ealle reellen Zahlen ohne Null\u201c?",
     "<b>ℝ \\ {0}</b> oder <b>ℝ*</b>"),
    ("Was bedeutet ℕ*?",
     "<b>Natürliche Zahlen ohne Null</b>: 1, 2, 3, …"),
]


# ─── Cards für g1-3 Algebraische Terme ──────────────────────────────────
g13_cards = [
    ("Was sind <i>gleichartige Glieder</i>?",
     "Glieder mit <b>denselben Variablen in denselben Potenzen</b>. Beispiele: 3x und −5x, 4x²y und 7x²y. Gegenbeispiel: 3x und 3x² (verschiedene Potenzen)."),
    ("Wie fasst man 3x + 5x − 2x zusammen?",
     "Addition der Koeffizienten bei gleicher Variable: (3 + 5 − 2)·x = <b>6x</b>."),
    ("Wie fasst man 2x² + 3x − x² + 4 zusammen?",
     "Gleichartige Glieder addieren:<br>x²: 2x² − x² = x²<br>x: 3x bleibt<br>Konstante: 4 bleibt<br>Resultat: <b>x² + 3x + 4</b>"),
    ("Klammer auflösen: 3·(x + 4)",
     "Distributivgesetz: <b>3x + 12</b>"),
    ("Klammer auflösen: −2·(x − 5)",
     "Vorzeichen mitnehmen: <b>−2x + 10</b>"),
    ("Klammer auflösen: −(a − b + c)",
     "Minuszeichen kehrt alle Vorzeichen um: <b>−a + b − c</b>"),
    ("1. Binomische Formel",
     "<b>(a + b)² = a² + 2ab + b²</b>"),
    ("2. Binomische Formel",
     "<b>(a − b)² = a² − 2ab + b²</b>"),
    ("3. Binomische Formel (Plus-Minus)",
     "<b>(a + b)(a − b) = a² − b²</b>"),
    ("Berechne (x + 3)² mit binomischer Formel",
     "1. Bin: a = x, b = 3<br><b>x² + 6x + 9</b>"),
    ("Berechne (2x − 5)² mit binomischer Formel",
     "2. Bin: a = 2x, b = 5. <i>Vorzeichen-Vorsicht</i>: das Quadrat eines Minus-Terms hat einen <em>negativen Mittelterm</em>, aber beide Endterme sind <em>positiv</em>. (2x)² − 2·2x·5 + 5² = <b>4x² − 20x + 25</b>"),
    ("Berechne (x + 4)(x − 4) mit binomischer Formel",
     "3. Bin: a = x, b = 4<br><b>x² − 16</b>"),
    ("Was bedeutet <i>faktorisieren</i>?",
     "Einen Term in ein <b>Produkt</b> umformen. Umkehrung des Klammer-Auflösens."),
    ("Faktorisiere 6x + 9",
     "Gemeinsamer Faktor (<i>ggT der Koeffizienten</i>): ggT(6, 9) = 3. <b>3·(2x + 3)</b>"),
    ("Faktorisiere 4x² − 12x",
     "Gemeinsamer Faktor 4x: <b>4x·(x − 3)</b>"),
    ("Faktorisiere x² − 9",
     "3. binomische Formel rückwärts: <b>(x + 3)(x − 3)</b>"),
    ("Faktorisiere x² + 6x + 9",
     "1. binomische Formel rückwärts: <b>(x + 3)²</b>"),
    ("Faktorisiere x² − 10x + 25",
     "2. binomische Formel rückwärts: <b>(x − 5)²</b>"),
    ("Faktorisiere 2x² − 8",
     "Erst ausklammern, dann 3. Bin: 2·(x² − 4) = <b>2·(x + 2)(x − 2)</b>. <i>Probe</i> mit x = 3: original 2·9 − 8 = 10; faktorisiert 2·5·1 = 10 ✓"),
    ("Faktorisiere 3x² − 12x + 12",
     "Erst 3 ausklammern, dann 2. Bin: 3·(x² − 4x + 4) = <b>3·(x − 2)²</b>"),
    ("Reihenfolge beim Faktorisieren",
     "<b>1. Gemeinsamer Faktor</b> (zahl- oder variablenseitig)<br><b>2. Binomische Formeln rückwärts</b><br><b>3. Spezielle Tricks</b> (z. B. quadratische Ergänzung)"),
    ("Was ist eine Polynomdivision (im Grundlagenfach)?",
     "Im Grundlagenfach <b>nicht erforderlich</b>. Faktorisieren beschränkt sich auf Ausklammern und binomische Formeln."),
    ("Häufiger Fehler bei (a + b)²",
     "Falsch: a² + b². Richtig: <b>a² + 2ab + b²</b> (mittlerer Term nicht vergessen!). <i>Schnelle Probe</i> mit a = 3, b = 4: (3+4)² = 49 ≠ 9 + 16 = 25 — der Mittelterm 2·3·4 = 24 fehlt."),
    ("Wie prüft man eine Faktorisierung?",
     "Klammern <b>wieder ausmultiplizieren</b>. Stimmt das Ergebnis mit dem Original überein, ist die Faktorisierung korrekt."),
    ("Was ist der <i>Grad</i> eines Polynoms?",
     "Der <b>höchste Exponent</b>, der in einem Glied vorkommt. Beispiel: 5x³ − 2x² + 7x − 4 hat Grad <b>3</b>. Konstante Polynome (z. B. 5) haben Grad 0."),
    ("Was ist das <i>konstante Glied</i> eines Polynoms?",
     "Das Glied <b>ohne Variable</b> (höchster Exponent 0). Beispiel: in 5x³ − 2x² + 7x − 4 ist das konstante Glied <b>−4</b>. Es ist der Wert des Polynoms an der Stelle x = 0."),
    ("Welche Koeffizienten hat 5x³ − 2x² + 7x − 4?",
     "<b>5, −2, 7, −4</b> — die Vorzahlen jedes Glieds in fallender Potenzordnung. Wichtig: Vorzeichen mitnehmen."),
]


# ─── Cards für g1-4 Zehnerpotenzen und Quadratwurzeln ───────────────────
g14_cards = [
    ("Was ist eine <i>Zehnerpotenz</i>?",
     "Eine Zahl der Form 10ⁿ mit n ∈ ℤ. Beispiele: 10² = 100, 10⁻³ = 0.001, 10⁰ = 1."),
    ("Wert von 10⁰?",
     "<b>1</b>. (Jede Zahl hoch null ist 1, ausser 0⁰ — undefiniert.)"),
    ("Wert von 10⁻²?",
     "<b>0.01 = 1/100</b>. Negativer Exponent → Kehrwert."),
    ("Was ist die <i>wissenschaftliche Notation</i>?",
     "Schreibweise <b>a · 10ⁿ</b> mit 1 ≤ |a| &lt; 10 und n ∈ ℤ. Beispiel: 3.14·10⁸."),
    ("Wandle 4500 in wissenschaftliche Notation",
     "<b>4.5 · 10³</b>"),
    ("Wandle 0.0027 in wissenschaftliche Notation",
     "<b>2.7 · 10⁻³</b>"),
    ("Wandle 6.02 · 10²³ in normale Schreibweise",
     "Komma 23 Stellen nach rechts: <b>602 000 000 000 000 000 000 000</b>. Diese Zahl ist die <i>Avogadro-Zahl</i> — die Anzahl Teilchen in einem Mol (z.B. einem Mol Wassermoleküle, etwa 18 g Wasser). Das ist <i>der</i> Grund, warum die wissenschaftliche Notation existiert."),
    ("Potenzgesetz: aᵐ · aⁿ = ?",
     "<b>aᵐ⁺ⁿ</b> (gleiche Basis: Exponenten addieren)"),
    ("Potenzgesetz: aᵐ : aⁿ = ?",
     "<b>aᵐ⁻ⁿ</b> (gleiche Basis: Exponenten subtrahieren)"),
    ("Potenzgesetz: (aᵐ)ⁿ = ?",
     "<b>aᵐ·ⁿ</b> (Potenz hoch Potenz: Exponenten multiplizieren)"),
    ("Potenzgesetz: (a · b)ⁿ = ?",
     "<b>aⁿ · bⁿ</b>"),
    ("Potenzgesetz: a⁻ⁿ = ?",
     "<b>1/aⁿ</b> (negativer Exponent = Kehrwert)"),
    ("Berechne 10³ · 10⁴",
     "Exponenten addieren: <b>10⁷ = 10 000 000</b>"),
    ("Berechne (10²)³",
     "Exponenten multiplizieren: <b>10⁶ = 1 000 000</b>"),
    ("Was ist eine <i>Quadratwurzel</i>?",
     "<b>√a = b</b> bedeutet b² = a (mit b ≥ 0). Definiert für a ≥ 0."),
    ("Was ist √16?",
     "<b>4</b> (denn 4² = 16)."),
    ("Was ist √0.25?",
     "<b>0.5</b> (denn 0.5² = 0.25). <i>Dezimal-Wurzel-Falle</i>: \"√(klein) wird grösser\" — die Wurzel einer Dezimalzahl zwischen 0 und 1 ist <em>grösser</em> als die ursprüngliche Zahl (0.5 &gt; 0.25). Gilt analog für √0.04 = 0.2, √0.01 = 0.1."),
    ("Wurzelgesetz: √(a·b) = ?",
     "<b>√a · √b</b> (für a, b ≥ 0)"),
    ("Wurzelgesetz: √(a/b) = ?",
     "<b>√a / √b</b> (für a ≥ 0, b &gt; 0)"),
    ("Achtung: ist √(a + b) = √a + √b?",
     "<b>NEIN!</b> Ein häufiger Fehler. √(9 + 16) = √25 = 5, aber √9 + √16 = 3 + 4 = 7. Die Wurzel verteilt sich nur auf <b>Produkte</b>, nicht auf Summen."),
    ("Vereinfache √50 (teilweises Wurzelziehen)",
     "√50 = √(25·2) = √25 · √2 = <b>5√2</b>"),
    ("Vereinfache √72",
     "√72 = √(36·2) = <b>6√2</b>"),
    ("Mache den Nenner rational: 3/√2",
     "Mit √2 erweitern: 3/√2 · √2/√2 = <b>3√2 / 2</b>. <i>Warum erweitern</i>: √2·√2 = √4 = 2, der Nenner wird rational. Erweitern mit √2/√2 ändert den Wert nicht (es ist gleich 1), aber die Form."),
    ("Mache den Nenner rational: 1/√5",
     "Mit √5 erweitern: <b>√5 / 5</b>"),
    ("Berechne √2 · √8 ohne Hilfsmittel",
     "√(2·8) = √16 = <b>4</b>"),
    ("Hierarchie: 2 + 3·√16",
     "Wurzel zuerst: √16 = 4. Dann Punkt: 3·4 = 12. Dann Strich: 2 + 12 = <b>14</b>."),
    ("Was ist (−3)²?",
     "<b>9</b>. Klammer schliesst das Minus mit ein: (−3)·(−3) = 9."),
    ("Was ist −3²?",
     "<b>−9</b>. Ohne Klammer wirkt das Minus nur auf das Resultat: −(3²) = −9."),
    ("SI-Vorsatz: G entspricht welcher Zehnerpotenz?",
     "<b>G = Giga = 10⁹</b>. Beispiel: 1 GHz = 10⁹ Hz."),
    ("SI-Vorsatz: M entspricht welcher Zehnerpotenz?",
     "<b>M = Mega = 10⁶</b>. Beispiel: 1 MB = 10⁶ Byte."),
    ("SI-Vorsatz: µ (Mikro) entspricht welcher Zehnerpotenz?",
     "<b>µ = Mikro = 10⁻⁶</b>. Beispiel: 1 µs = 10⁻⁶ s = eine Millionstelsekunde."),
    ("SI-Vorsatz: c (Centi) entspricht welcher Zehnerpotenz?",
     "<b>c = Centi = 10⁻²</b>. Beispiel: 1 cm = 10⁻² m = 0.01 m."),
    ("Wandle 1 cm in m um",
     "<b>1 cm = 10⁻² m = 0.01 m</b>. Centi (c) = 10⁻²."),
    ("Wandle 1 hPa in Pa um",
     "<b>1 hPa = 100 Pa</b>. Hekto (h) = 10². hPa ist die Standard-Einheit für Luftdruck (Wetterbericht)."),
    ("Wandle 5 dl in Liter um",
     "<b>5 dl = 0.5 l</b>. Deci (d) = 10⁻¹. Ein Standardglas Wein in der Schweiz ist 1 dl."),
    ("SI-Vorsatz: n entspricht welcher Zehnerpotenz?",
     "<b>n = Nano = 10⁻⁹</b>. Beispiel: 1 nm = 10⁻⁹ m (Wellenlängenbereich von sichtbarem Licht)."),
]


# ─── Cards für g4-1 Grundlagen Datenanalyse ─────────────────────────────
g41_cards = [
    ("Was ist die <i>Grundgesamtheit</i>?",
     "Die Menge <b>aller Objekte</b>, über die eine Aussage getroffen werden soll. Beispiel: alle Lernenden einer Schule."),
    ("Was ist eine <i>Stichprobe</i>?",
     "Eine <b>Teilmenge</b> der Grundgesamtheit, die tatsächlich untersucht wird. Beispiel: eine Klasse von 22 Lernenden."),
    ("Was ist der <i>Stichprobenumfang</i>?",
     "Die Anzahl <b>n</b> der Elemente in der Stichprobe."),
    ("Was ist eine <i>Urliste</i>?",
     "Die Liste der Werte in der <b>Reihenfolge der Erhebung</b> — unverändert, ungeordnet."),
    ("Was ist die <i>sortierte Liste</i>?",
     "Die Urliste, <b>aufsteigend sortiert</b>. Grundlage für Median, Quartile, Rang."),
    ("Was ist der <i>Rang</i> eines Wertes?",
     "Die <b>Position</b> des Wertes in der sortierten Liste. Bei Mehrfachvorkommen erhält jedes seinen eigenen Rang."),
    ("Was ist ein <i>kategoriales</i> Merkmal?",
     "Werte sind <b>Namen oder Kategorien</b>, ohne natürliche Reihenfolge. Beispiele: Lieblingsfach, Augenfarbe, Postleitzahl."),
    ("Was ist ein <i>diskretes</i> Merkmal?",
     "Zahlen, aber nur <b>abzählbar viele Werte</b> möglich. Beispiele: Kinderzahl, Würfelaugen, Anzahl Geschwister."),
    ("Was ist ein <i>stetiges</i> Merkmal?",
     "Zahlen, <b>beliebig fein abstufbar</b>. Beispiele: Körpergrösse, Wartezeit, Temperatur."),
    ("Welcher Diagrammtyp passt zu kategorialen Daten?",
     "<b>Balken-</b> oder <b>Kuchendiagramm</b>."),
    ("Welcher Diagrammtyp passt zu diskreten Daten?",
     "<b>Balkendiagramm</b> (mit Lücken zwischen den Balken)."),
    ("Welcher Diagrammtyp passt zu stetigen Daten?",
     "<b>Histogramm</b> — Säulen ohne Lücken, weil der Wertebereich lückenlos ist."),
    ("Excel-Funktion: Anzahl Werte zählen",
     "<b>=ANZAHL(A:A)</b> (deutsch) bzw. <b>=COUNT(A:A)</b> (englisch)."),
    ("Excel-Funktion: Häufigkeit eines Wertes",
     "<b>=ZÄHLENWENN(A:A; \"Wert\")</b> bzw. <b>=COUNTIF(A:A; \"Wert\")</b>"),
    ("Excel-Funktion: k-kleinster Wert",
     "<b>=KKLEINSTE(A:A; k)</b> bzw. <b>=SMALL(A:A; k)</b>"),
    ("Was ist <i>Repräsentativität</i>?",
     "Bildet die Stichprobe die Grundgesamtheit <b>treu ab</b>? Eine Online-Umfrage erreicht z. B. keine Senioren ohne Internet — nicht repräsentativ."),
    ("Was ist <i>Objektivität</i> einer Datenerhebung?",
     "Würden <b>verschiedene Personen</b> dieselben Werte messen? Hängt von Messgerät und Methode ab."),
    ("Was ist <i>Genauigkeit</i> einer Datenerhebung?",
     "Passt die <b>Messpräzision</b> zum Zweck? Körpergrösse auf cm reicht — auf 0.001 mm wäre überflüssig."),
    ("Was ist <i>Selbstselektions-Bias</i>?",
     "Wer freiwillig an einer Umfrage teilnimmt, ist meist <b>nicht zufällig</b> ausgewählt — oft motivierter (positiv oder negativ) als der Durchschnitt."),
    ("Was ist <i>Coverage-Bias</i>?",
     "Wenn die <b>Erhebungsmethode</b> bestimmte Gruppen ausschliesst. Beispiel: Online-Umfrage erreicht keine Internet-fernen Personen."),
    ("Häufiger Fehler bei Frageformulierung",
     "<b>Suggestive Fragen</b>. \u201eBist du auch dafür, dass \u2026\u201c drängt zur Zustimmung. Neutral: \u201eSollte \u2026 oder nicht?\u201c."),
    ("Wie gross sollte n für repräsentative Aussagen sein?",
     "Faustregel: <b>500–2000</b> für Aussagen über grosse Bevölkerungsgruppen. Mit n &lt; 50 sind Aussagen über grosse Grundgesamtheiten nicht belastbar."),
    ("Plausibilität: kann ein Rang 0 vorkommen?",
     "<b>Nein</b>. Ränge in der sortierten Liste beginnen bei 1 und gehen bis n."),
    ("Tabellen-Tipp: wie sortiert man eine Spalte fortlaufend?",
     "In B2 schreiben: <b>=KKLEINSTE($A$2:$A$100; ZEILE()-1)</b>. Beim Kopieren bis B100 entsteht die sortierte Liste."),
]


# ─── Cards für g4-2 Diagramme ───────────────────────────────────────────
g42_cards = [
    ("Was bedeutet <i>klassieren</i>?",
     "Wertebereich in <b>Klassen gleicher Breite</b> einteilen und für jede Klasse die Anzahl der Werte zählen. Notwendig bei stetigen Daten."),
    ("Faustregel für Klassenanzahl",
     "<b>k ≈ √n</b>, gerundet auf eine sinnvolle Zahl."),
    ("Klassenbreite berechnen",
     "<b>b = (max − min) / k</b>, aufgerundet auf einen einfachen Wert."),
    ("Standarddiagramm für kategoriale Daten",
     "<b>Balken-</b> oder <b>Kuchendiagramm</b>."),
    ("Standarddiagramm für diskrete Daten",
     "<b>Balkendiagramm</b> (mit Lücken)."),
    ("Standarddiagramm für stetige Daten",
     "<b>Histogramm</b> (ohne Lücken)."),
    ("Standarddiagramm für bivariate Daten",
     "<b>Streudiagramm</b>: jedes Wertepaar (x, y) als Punkt im Koordinatensystem."),
    ("Unterschied Histogramm vs. Balkendiagramm",
     "<b>Histogramm</b>: Säulen <b>berühren sich</b> (stetiger Wertebereich).<br><b>Balkendiagramm</b>: Balken <b>mit Lücken</b> (kategorial oder diskret)."),
    ("Eigenschaft: <i>symmetrische</i> Verteilung",
     "Links und rechts vom Gipfel <b>spiegelbildlich gleich</b>. Mittelwert ≈ Median."),
    ("Eigenschaft: <i>rechtsschiefe</i> Verteilung",
     "Langer Schwanz nach <b>rechts</b>. Mittelwert &gt; Median. Beispiele: Einkommen, Wartezeiten."),
    ("Eigenschaft: <i>linksschiefe</i> Verteilung",
     "Langer Schwanz nach <b>links</b>. Mittelwert &lt; Median."),
    ("Eigenschaft: <i>unimodal</i>",
     "Verteilung hat <b>einen Gipfel</b> (eine Häufung)."),
    ("Eigenschaft: <i>bimodal / multimodal</i>",
     "Verteilung hat <b>zwei oder mehr Gipfel</b>. Oft Hinweis auf Mischung verschiedener Untergruppen."),
    ("Was zeigt der <i>Boxplot</i>?",
     "Fünf Zahlen: <b>min · Q₁ · Median · Q₃ · max</b>. Box von Q₁ bis Q₃, Whisker zu min/max, Strich am Median."),
    ("Was sind <i>bivariate</i> Daten?",
     "Zu jedem Objekt ein <b>Wertepaar (x, y)</b>. Beispiel: Lernzeit und Note pro Person."),
    ("Welche Zusammenhangs-Typen im Streudiagramm?",
     "<b>Positiv</b> (steigend), <b>negativ</b> (fallend), <b>kein</b> (chaotisch), <b>nicht-linear</b> (Bogen)."),
    ("Korrelation = Kausalität?",
     "<b>Nein!</b> Beide können durch eine dritte Grösse verursacht sein. Beispiel: Eisverkauf und Sonnenbrand korrelieren — beide hängen an der Sonne."),
    ("Wie viele Klassen für n = 36?",
     "√36 = <b>6 Klassen</b>"),
    ("Wann Kuchendiagramm vermeiden?",
     "Bei <b>vielen Kategorien</b> (über 6–7) oder bei <b>ähnlich grossen Anteilen</b>. Augen vergleichen Höhen besser als Winkel — Balkendiagramm ist meist überlegen."),
    ("Wie liest man Schiefe aus dem Boxplot?",
     "Lage der Mittellinie (Median) in der Box: näher am Q₁ → <b>rechtsschief</b>; näher am Q₃ → <b>linksschief</b>; in der Mitte → <b>symmetrisch</b>."),
    ("Was zeigt eine bimodale Körpergrössen-Verteilung in einer Klasse?",
     "Mögliche Mischung aus <b>Frauen und Männern</b> mit unterschiedlichen Mittelwerten — zwei Gipfel sind dann typisch."),
    ("Wann ein Streudiagramm wählen?",
     "Wenn man den <b>Zusammenhang zweier Merkmale</b> untersuchen will (bivariate Daten)."),
    ("Erste Frage vor jeder Diagrammwahl",
     "<b>\u201eWelcher Datentyp?\u201c</b> Kategorial / diskret / stetig / bivariat \u2014 daraus folgt der Diagrammtyp."),
]


# ─── Cards für g4-3 Masszahlen ──────────────────────────────────────────
g43_cards = [
    ("Was ist der <i>Mittelwert</i>?",
     "<b>Summe aller Werte geteilt durch n</b>. Symbol: x̄ (\"x quer\"). Formel: x̄ = (1/n)·Σxᵢ"),
    ("Was ist der <i>Median</i>?",
     "Der <b>mittlere Wert der sortierten Liste</b>. Bei geradem n: Mittelwert der zwei mittleren Werte. Symbol: x̃ (\"x Schlange\")."),
    ("Was ist der <i>Modus</i>?",
     "Der <b>häufigste Wert</b>. Funktioniert auch für kategoriale Daten. Symbol: x̂ (\"x Dach\")."),
    ("Berechne den Mittelwert von 4, 7, 2, 9, 8",
     "(4+7+2+9+8)/5 = 30/5 = <b>6</b>"),
    ("Berechne den Median von 4, 7, 2, 9, 8",
     "Sortiert: 2, 4, 7, 8, 9. Mittlere Position (3): <b>7</b>"),
    ("Berechne den Median von 3, 5, 8, 10",
     "n gerade. Mittel der Positionen 2 und 3: (5+8)/2 = <b>6.5</b>"),
    ("Was ist die <i>Standardabweichung</i>?",
     "<b>Mittlere Abweichung vom Mittelwert</b>. Formel: s = √((1/(n−1))·Σ(xᵢ−x̄)²)"),
    ("Was ist die <i>Varianz</i>?",
     "Das <b>Quadrat der Standardabweichung</b>. s² = (1/(n−1))·Σ(xᵢ−x̄)²"),
    ("Warum dividieren wir bei s durch (n−1) und nicht durch n?",
     "Bei einer <b>Stichprobe</b> liefert n−1 eine bessere Schätzung der Streuung in der Grundgesamtheit. Tabellenkalkulation: <b>STABW.S</b> bzw. <b>STDEV.S</b>."),
    ("Was sind <i>Quartile</i>?",
     "Q₁, Q₂, Q₃ teilen die sortierte Liste in <b>vier gleich grosse Teile</b>. Q₂ = Median."),
    ("Was ist Q₁?",
     "Das <b>untere Quartil</b> — 25 % der Werte sind kleiner. Median der unteren Hälfte."),
    ("Was ist Q₃?",
     "Das <b>obere Quartil</b> — 75 % der Werte sind kleiner. Median der oberen Hälfte."),
    ("Was ist die <i>Quartilsdifferenz</i> (IQR)?",
     "<b>QD = Q₃ − Q₁</b>. Breite der mittleren 50 % der Daten. Im Boxplot: Boxbreite."),
    ("Was bedeutet <i>robust</i>?",
     "Eine Kennzahl ist robust, wenn sie durch <b>einzelne Extremwerte (Ausreisser) kaum verändert</b> wird."),
    ("Median oder Mittelwert — welches ist robust?",
     "<b>Median ist robust</b>. Mittelwert reagiert stark auf Ausreisser."),
    ("Wann Mittelwert verwenden?",
     "Bei <b>symmetrischer Verteilung ohne Ausreisser</b>."),
    ("Wann Median verwenden?",
     "Bei <b>schiefer Verteilung oder mit Ausreissern</b>. Beispiel: Einkommen, Wartezeiten."),
    ("Faustregel: x̄ und x̃ weit auseinander → ?",
     "Verteilung ist <b>schief</b>, oft mit Ausreissern. Median bevorzugen."),
    ("Faustregel: x̄ und x̃ nahe beieinander → ?",
     "Verteilung ist <b>annähernd symmetrisch</b>. Beide Lagemasse funktionieren."),
    ("Excel: Mittelwert in A1:A100",
     "<b>=MITTELWERT(A1:A100)</b> bzw. englisch <b>=AVERAGE(A1:A100)</b>"),
    ("Excel: Standardabweichung der Stichprobe",
     "<b>=STABW.S(A1:A100)</b> bzw. englisch <b>=STDEV.S(A1:A100)</b>"),
    ("Excel: Quartilsdifferenz in einer Formel",
     "<b>=QUARTILE.INKL(A:A;3) − QUARTILE.INKL(A:A;1)</b>"),
    ("Wenn s = 0, was bedeutet das?",
     "Alle Werte der Stichprobe sind <b>gleich</b>. Keine Streuung."),
    ("Welche fünf Zahlen bilden den Boxplot?",
     "<b>min, Q₁, Median, Q₃, max</b>. Box von Q₁ bis Q₃, Mittellinie am Median, Whisker zu min und max."),
    ("Welche Masszahl ist nur für kategoriale Daten sinnvoll?",
     "<b>Modus</b>. Mittelwert und Median brauchen Zahlen mit Reihenfolge."),
    ("Welches Streumass passt zum Median?",
     "<b>Quartilsdifferenz</b> (QD). Beide sind robust und passen zum Boxplot."),
    ("Welches Streumass passt zum Mittelwert?",
     "<b>Standardabweichung</b>. Beide nutzen alle Werte mit voller Stärke."),
    ("Merksatz: Lage und Streuung",
     "Eine Stichprobe ist erst beschrieben, wenn beide angegeben sind: <b>Lage</b> (wo liegt die Mitte?) und <b>Streuung</b> (wie breit verteilt?). Mittelwert + s gehen zusammen, Median + QD gehen zusammen."),
]


# ─── Cards für g5-2d Zentrische Streckung und Ähnlichkeit ─────────
g52d_cards = [
    # Zentrische Streckung — Grundlagen
    ("Definition: zentrische Streckung",
     "Zentrum <b>Z</b> und Streckfaktor <b>k ≠ 0</b>. Jeder Punkt P wird abgebildet auf P′ mit <b>ZP′ = k · ZP</b> (Vektoren)."),
    ("Bedeutung k = 1",
     "<b>Identität</b>: Bild = Original."),
    ("Bedeutung k = −1",
     "<b>Punktspiegelung</b> am Zentrum Z. Längen bleiben gleich, Orientierung kehrt sich um."),
    ("Bedeutung |k| &gt; 1",
     "<b>Vergrösserung</b>: Bildstrecken sind länger als Originalstrecken."),
    ("Bedeutung 0 &lt; |k| &lt; 1",
     "<b>Verkleinerung</b>: Bildstrecken sind kürzer als Originalstrecken."),
    ("Bedeutung k &lt; 0",
     "Bildpunkt liegt auf der <b>anderen Seite</b> von Z; Figur wird zusätzlich am Zentrum gespiegelt (gegensinnig)."),

    # Eigenschaften
    ("Vier Eigenschaften der zentrischen Streckung",
     "<b>Gleichsinnig</b> (bei k &gt; 0), <b>parallelentreu</b>, <b>winkeltreu</b>, <b>verhältnistreu</b>."),
    ("Was bedeutet «verhältnistreu»?",
     "Der Quotient aus Bildstrecke und Originalstrecke ist <b>konstant</b> und gleich dem Streckfaktor k."),
    ("Streckfaktor und Längen",
     "Strecken werden mit <b>|k|</b> skaliert: a′ = |k| · a."),
    ("Streckfaktor und Flächen",
     "Flächen werden mit <b>k²</b> skaliert: A′ = k² · A."),
    ("Streckfaktor und Volumina (im Raum)",
     "Volumina werden mit <b>|k|³</b> skaliert: V′ = |k|³ · V."),

    # Strahlensätze
    ("1. Strahlensatz (Aussage)",
     "Schneiden zwei Strahlen mit Anfangspunkt S zwei Parallelen AB und A′B′ (AB ∥ A′B′), so gilt:<br><b>SA : SA′ = SB : SB′</b><br>und gleichwertig <b>SA : AA′ = SB : BB′</b>."),
    ("2. Strahlensatz (Aussage)",
     "Unter denselben Voraussetzungen stehen die <b>Parallelenabschnitte</b> im gleichen Verhältnis wie die Strahlenabschnitte: <b>SA : SA′ = AB : A′B′</b> und <b>SB : SB′ = AB : A′B′</b>."),
    ("Umkehrung des 1. Strahlensatzes",
     "Gilt SA : SA′ = SB : SB′, dann sind die Geraden <b>AB und A′B′ parallel</b>. (Standardkonstruktion für Parallele durch einen Punkt.)"),
    ("Strahlensätze — Voraussetzung",
     "Zwei <b>Strahlen mit gemeinsamem Anfangspunkt</b> S, geschnitten von zwei <b>zueinander parallelen Geraden</b>."),
    ("Strahlensatz — typische Anwendung",
     "Drei Strecken bekannt, eine vierte berechnen. Setze die Verhältnisse gleich und löse die entstehende Proportionsgleichung."),

    # Ähnlichkeit
    ("Definition: ähnliche Figuren",
     "Zwei Figuren F₁ und F₂ sind <b>ähnlich</b> (F₁ ~ F₂), wenn sie durch eine <b>Ähnlichkeitsabbildung</b> ineinander überführt werden können."),
    ("Was ist eine Ähnlichkeitsabbildung?",
     "Eine <b>zentrische Streckung</b>, evtl. kombiniert mit Verschiebung, Drehung oder Spiegelung."),
    ("Drei Eigenschaften ähnlicher Figuren",
     "1. Sich entsprechende Winkel sind <b>gleich gross</b>.<br>2. Sich entsprechende Streckenverhältnisse sind <b>konstant</b> (= k).<br>3. Flächen verhalten sich wie <b>k²</b>."),

    # Ähnlichkeitssätze für Dreiecke
    ("Hauptähnlichkeitssatz am Dreieck",
     "Zwei Dreiecke sind ähnlich, wenn sie in <b>zwei Winkeln</b> übereinstimmen. (Kürzel: <b>WW</b>.)"),
    ("Warum reichen zwei Winkel?",
     "Weil die Innenwinkelsumme im Dreieck immer <b>180°</b> beträgt — der dritte Winkel folgt automatisch."),
    ("Ähnlichkeitssatz SSS",
     "Zwei Dreiecke sind ähnlich, wenn sie im <b>Verhältnis aller drei entsprechender Seiten</b> übereinstimmen: a′/a = b′/b = c′/c."),
    ("Ähnlichkeitssatz sWs",
     "Zwei Dreiecke sind ähnlich, wenn sie im <b>Verhältnis zweier entsprechender Seiten und im eingeschlossenen Winkel</b> übereinstimmen."),
    ("Ähnlichkeitssatz SsW",
     "Zwei Dreiecke sind ähnlich, wenn sie im <b>Verhältnis zweier entsprechender Seiten und im Gegenwinkel der grösseren Seite</b> übereinstimmen."),

    # Höhe im rechtwinkligen Dreieck
    ("Hauptähnlichkeitssatz im rechtwinkligen Dreieck",
     "Im rechtwinkligen Dreieck ABC mit ∠C = 90° und Höhe h auf der Hypotenuse c (Fusspunkt H) sind die drei Dreiecke <b>ABC ~ AHC ~ CHB</b> ähnlich."),
    ("Kathetensatz (Euklid)",
     "Im rechtwinkligen Dreieck: <b>a² = p · c</b> und <b>b² = q · c</b>. (Kathetenquadrat = Hypotenusenabschnitt × Hypotenuse.)"),
    ("Höhensatz (Euklid)",
     "Im rechtwinkligen Dreieck mit Höhe h auf der Hypotenuse: <b>h² = p · q</b>. (Höhenquadrat = Produkt der Hypotenusenabschnitte.)"),
    ("Pythagoras als Folge des Kathetensatzes",
     "a² + b² = pc + qc = (p + q) · c = c · c = <b>c²</b>. (Mit p + q = c.)"),
    ("Höhe aus den Katheten",
     "h = <b>a · b / c</b>. (Flächengleichheit: ½ ab = ½ ch.)"),

    # Anwendungen
    ("Massstab 1:N — Flächenfaktor",
     "Längenfaktor 1/N, also Flächenfaktor <b>(1/N)² = 1/N²</b>. Beispiel: Karte 1:25 000 → 1 cm² Karte = 625 000 000 cm² = 6,25 ha real."),
    ("Schattenwurf-Methode (Höhenmessung)",
     "Höhe und Schatten verhalten sich für alle Objekte zur selben Sonnenzeit gleich: <b>h_Objekt / h_Stab = Schatten_Objekt / Schatten_Stab</b>."),
    ("Wann sind die Kongruenzsätze und die Ähnlichkeitssätze verwandt?",
     "Die Ähnlichkeitssätze sind die <b>Verallgemeinerung</b> der Kongruenzsätze: statt <i>gleicher Seitenlängen</i> verlangt man <i>gleiche Seitenverhältnisse</i>. Bei Streckfaktor k = 1 fallen sie zusammen."),
]


# ─── s3-2a Potenzfunktionen (Schwerpunkt) ───────────────────
s32a_cards = [
    # Definitionen
    ('Was ist eine <i>Potenzfunktion</i>?',
     'Eine Funktion mit <b>f(x) = a · xⁿ</b>, n ∈ ℤ\\{0}, a ∈ ℝ\\{0}. (n = 0 zählt nicht dazu, n = 1 schon.)'),
    ('Was ist eine <i>Parabel n-ter Ordnung</i>?',
     'Der Graph einer Potenzfunktion mit <b>natürlichem Exponenten</b> n ∈ ℕ*.'),
    ('Was ist eine <i>Hyperbel n-ter Ordnung</i>?',
     'Der Graph einer Potenzfunktion mit <b>negativem ganzzahligem Exponenten</b>; Schreibweise x⁻ⁿ = 1/xⁿ.'),
    ('Wann heisst eine Funktion <i>gerade</i>?',
     '<b>f(−x) = f(x)</b> — der Graph ist achsensymmetrisch zur y-Achse. Bei Potenzfunktionen: gerader Exponent.'),
    ('Wann heisst eine Funktion <i>ungerade</i>?',
     '<b>f(−x) = −f(x)</b> — der Graph ist punktsymmetrisch zum Ursprung. Bei Potenzfunktionen: ungerader Exponent.'),
    ('Was ist eine <i>horizontale Asymptote</i>?',
     'Eine Gerade, an die sich der Graph <b>in x-Richtung</b> immer mehr annähert, ohne sie zu schneiden.'),
    ('Was ist eine <i>Polstelle</i> (Pol)?',
     'Die <b>Definitionslücke</b> x₀ einer Hyperbel; dort wächst |f(x)| über alle Grenzen. Die senkrechte Gerade x = x₀ heisst Polgerade.'),
    # Eigenschaften
    ('D und W von y = x²ⁿ (gerader Exponent)?',
     '<b>D = ℝ, W = ℝ₀⁺</b>. Gemeinsame Punkte: (0|0), (1|1), (−1|1).'),
    ('D und W von y = 1/x²ⁿ (gerade Hyperbel)?',
     '<b>D = ℝ\\{0}, W = ℝ⁺</b>. Asymptoten x = 0 und y = 0, keine Nullstellen.'),
    ('Gemeinsame Punkte aller ungeraden Parabeln y = x²ⁿ⁻¹?',
     '<b>(0|0), (1|1), (−1|−1)</b>.'),
    ('Asymptoten von y = 1/xⁿ?',
     'Vertikal <b>x = 0</b> (y-Achse), horizontal <b>y = 0</b> (x-Achse).'),
    ('Terrassenpunkt vs. Flachpunkt bei S(0|0)?',
     '<b>Terrassenpunkt</b> bei ungeraden Exponenten (n ≥ 3), <b>Flachpunkt</b> bei geraden Exponenten.'),
    # Transformationen
    ('Wirkung von u und v in y = a·(x−u)ⁿ + v?',
     'u verschiebt <b>horizontal</b> (rechts für u &gt; 0), v <b>vertikal</b>. Hyperbel-Asymptoten wandern mit: x = u, y = v.'),
    ('Wirkung von a in y = a·(x−u)ⁿ + v?',
     '|a| &gt; 1 <b>Streckung</b>, |a| &lt; 1 Stauchung in y-Richtung; a &lt; 0 zusätzlich <b>Spiegelung an der x-Achse</b>.'),
    # Beispiele
    ('Nullstellen von (x−3)⁴ − 16 = 0',
     '(x−3)⁴ = 16 → x − 3 = ±2 → <b>x₁ = 5, x₂ = 1</b>. (Gerader Exponent: ±-Fall!)'),
    ('Nullstelle von (x−2)³ + 8 = 0',
     '(x−2)³ = −8 → x − 2 = −2 → <b>x₀ = 0</b>. (Ungerader Exponent: genau eine Lösung.)'),
    ('y = xⁿ geht durch P(2|32). Bestimme n.',
     '2ⁿ = 32 = 2⁵ → <b>n = 5</b>.'),
    # Faustregeln
    ('Anzahl Lösungen von (x−u)ⁿ = r bei geradem n?',
     '<b>Zwei</b> für r &gt; 0 (±ⁿ√r), <b>keine</b> für r &lt; 0, eine für r = 0.'),
    ('y = x³: Was passiert mit y, wenn x verdoppelt wird?',
     'Faktor <b>2³ = 8</b> — Verdopplung des Arguments verachtfacht den Funktionswert.'),
]

# ─── s3-2b Wurzelfunktionen (Schwerpunkt) ───────────────────
s32b_cards = [
    # Definitionen
    ('Was ist eine <i>Wurzelfunktion</i>?',
     'Eine Funktion <b>f(x) = ⁿ√x = x^(1/n)</b> mit n ∈ ℕ*; f : ℝ₀⁺ → ℝ₀⁺.'),
    ('Wurzelfunktion und Potenzfunktion — Zusammenhang?',
     'Die Wurzelfunktion ist die <b>Umkehrfunktion</b> der Potenzfunktion y = xⁿ (auf ℝ₀⁺) — und umgekehrt.'),
    ('Wie entsteht der Graph der Umkehrfunktion grafisch?',
     'Durch <b>Spiegelung an der Winkelhalbierenden y = x</b>: Jeder Punkt (a|b) wird zu (b|a).'),
    ('Warum ist y = x² auf ganz ℝ nicht umkehrbar?',
     'Zu jeder Höhe y &gt; 0 gehören <b>zwei Urbilder ±x</b>. Erst die Einschränkung auf ℝ₀⁺ macht die Zuordnung eindeutig.'),
    ('Umkehrfunktion von y = x³?',
     '<b>y = ∛x</b> — bei ungeradem Exponenten wäre die Umkehrung sogar auf ganz ℝ möglich.'),
    # Eigenschaften
    ('D und W der Wurzelfunktion y = ⁿ√x?',
     '<b>D = W = ℝ₀⁺</b> — Radikand und Wurzelwert sind nie negativ.'),
    ('Gemeinsame Punkte aller Wurzelkurven?',
     '<b>(0|0) und (1|1)</b> — denn ⁿ√1 = 1 für jedes n.'),
    ('Warum hat die Wurzelfunktion keine Symmetrie?',
     'D = ℝ₀⁺ ist <b>nicht symmetrisch zum Ursprung</b> — mit x liegt −x nie im Definitionsbereich.'),
    ('Maximaler Definitionsbereich von y = √(x−u)?',
     'Radikand ≥ 0: x − u ≥ 0 → <b>D = [u; +∞[</b>.'),
    ('Startpunkt von y = a·√(x−u) + v?',
     '<b>(u | v)</b> — dort ist die Wurzel null.'),
    # Schreibweise / Werte
    ('√x und ∛(x²) als Potenzen geschrieben?',
     '√x = <b>x^(1/2)</b>, ∛(x²) = <b>x^(2/3)</b>.'),
    ('⁵√32 und ⁴√81 im Kopf?',
     '⁵√32 = <b>2</b> (2⁵ = 32), ⁴√81 = <b>3</b> (3⁴ = 81).'),
    # Wurzelgleichungen
    ('Strategie zum Lösen einer Wurzelgleichung?',
     '1. <b>Definitionsbereich</b> (Radikand ≥ 0), 2. Wurzel isolieren, 3. hoch n, 4. <b>Probe</b> in der Ausgangsgleichung.'),
    ('Warum ist nach dem Quadrieren eine Probe nötig?',
     'Quadrieren ist <b>keine Äquivalenzumformung</b> — es können Scheinlösungen entstehen.'),
    ('√(…) = c mit c &lt; 0 — Lösungsmenge?',
     '<b>L = { }</b> — Wurzelwerte sind nie negativ, die Gleichung ist unlösbar.'),
    ('Löse √(3x+1) = 4.',
     'Quadrieren: 3x + 1 = 16 → <b>x = 5</b>. Probe: √16 = 4 ✓'),
    ('Löse ∛(x−5) = 3.',
     'Hoch 3: x − 5 = 27 → <b>x = 32</b>. Probe: ∛27 = 3 ✓'),
    ('Ordinatenabschnitt von y = 3√(x+1) − 6?',
     'x = 0 einsetzen: y₀ = 3·√1 − 6 = <b>−3</b>.'),
    # Anwendung
    ('Fadenpendel T = 2π·√(l/g): Umkehrfunktion l(T)?',
     '<b>l = g·T²/(4π²) ≈ 0.248·T²</b> — die Umkehrung der Wurzelfunktion ist quadratisch.'),
    ('√x oder ⁵√x — welcher Wert ist zwischen 0 und 1 grösser?',
     'Die <b>höhere Wurzel</b>: ⁵√x &gt; √x für 0 &lt; x &lt; 1 (rechts von 1 ist es umgekehrt).'),
]


# ─── s3-3 Polynomfunktionen (Schwerpunkt) ───────────────────
s33_cards = [
    # Definitionen
    ('Was ist eine <i>Polynomfunktion</i> (ganzrationale Funktion)?',
     '<b>f(x) = aₙxⁿ + … + a₁x + a₀</b> mit n ∈ ℕ, aₖ ∈ ℝ, aₙ ≠ 0 — eine Linearkombination von Potenzfunktionen.'),
    ('Was heisst <i>Grad</i> und <i>Leitkoeffizient</i>?',
     'Der <b>Grad n</b> ist der höchste Exponent, der <b>Leitkoeffizient aₙ</b> der Koeffizient davor (aₙ ≠ 0).'),
    ('Bekannte Spezialfälle der Polynomfunktion?',
     'Grad 1: <b>lineare Funktion</b>; Grad 2: <b>quadratische Funktion</b>; nur ein Term aₙxⁿ: <b>Potenzfunktion</b>.'),
    ('Ist f(x) = 2x⁴ − 1/x² eine Polynomfunktion?',
     '<b>Nein</b> — 1/x² = x⁻² hat einen negativen Exponenten. Polynome brauchen natürliche Exponenten.'),
    # Linearfaktoren
    ('Was ist die <i>Linearfaktordarstellung</i>?',
     '<b>f(x) = aₙ·(x−x₁)(x−x₂)···(x−xₙ)</b> — die Nullstellen stehen direkt in den Faktoren.'),
    ('Wie verhält sich der Graph an einer <i>einfachen</i> Nullstelle?',
     'Er <b>schneidet</b> die x-Achse (Vorzeichenwechsel).'),
    ('Wie verhält sich der Graph an einer <i>doppelten</i> Nullstelle?',
     'Er <b>berührt</b> die x-Achse — Hoch- oder Tiefpunkt auf der Achse, kein Vorzeichenwechsel.'),
    ('Wie verhält sich der Graph an einer <i>dreifachen</i> Nullstelle?',
     'Er <b>schneidet terrassenförmig abgeflacht</b> (Vorzeichenwechsel mit Sattel).'),
    ('Grad 2, Nullstellen 3 und −4, y-Achsenabschnitt −24: Funktionsgleichung?',
     'Ansatz f(x) = a(x−3)(x+4); f(0) = −12a = −24 → a = 2: <b>f(x) = 2(x−3)(x+4)</b>.'),
    ('Nullstellen von f(x) = x³ − 9x?',
     'Ausklammern: x(x−3)(x+3) → <b>x = −3, 0, 3</b> (Satz vom Nullprodukt).'),
    # Verlauf
    ('Globalverlauf bei ungeradem Grad?',
     'Enden <b>entgegengesetzt</b>: aₙ &gt; 0 von links unten nach rechts oben ↗; aₙ &lt; 0 umgekehrt ↘.'),
    ('Globalverlauf bei geradem Grad?',
     'Enden <b>gleich</b>: aₙ &gt; 0 beide oben ∪; aₙ &lt; 0 beide unten ∩.'),
    ('Wie viele Nullstellen hat eine Polynomfunktion n-ten Grades höchstens?',
     '<b>Höchstens n</b> — bei ungeradem Grad mindestens eine (durchgehende Kurve kreuzt die Achse).'),
    ('Wie viele lokale Extremstellen höchstens?',
     '<b>Höchstens n − 1</b> (Hochpunkte und Tiefpunkte zusammen).'),
    ('Stimmt «Grad = Anzahl Nullstellen»?',
     '<b>Nein</b> — der Grad ist nur die Obergrenze: x² + 1 hat Grad 2 und keine Nullstelle.'),
    # Extremwerte
    ('Was ist ein <i>Hochpunkt</i>?',
     'Ein <b>lokal höchster Punkt</b> des Graphen; seine y-Koordinate ist ein lokales (relatives) Maximum.'),
    ('Lokales vs. absolutes Maximum?',
     '<b>Lokal</b>: grösster Wert in einer Umgebung. <b>Absolut</b>: grösster Funktionswert überhaupt — bei ungeradem Grad existiert er nie.'),
    # Symmetrie
    ('Symmetrie-Schnellcheck über die Exponenten?',
     'Nur <b>gerade</b> Exponenten (inkl. a₀): gerade Funktion, achsensymmetrisch. Nur <b>ungerade</b> (a₀ = 0!): ungerade, punktsymmetrisch.'),
    ('Ist f(x) = x⁵ − 3x³ + x + 1 gerade oder ungerade?',
     '<b>Weder noch</b> — das konstante Glied +1 ist ein gerader Anteil neben den ungeraden Exponenten.'),
    ('Gerade Funktion mit Nullstelle bei x = 2: Welche weitere Nullstelle ist sicher?',
     '<b>x = −2</b> — Achsensymmetrie: f(−2) = f(2) = 0.'),
]

# ─── s3-4a Exponentialfunktionen (Schwerpunkt) ──────────────
s34a_cards = [
    # Definitionen
    ('Was ist eine <i>Exponentialfunktion</i>?',
     'Eine Funktion <b>f(x) = aˣ</b> mit a ∈ ℝ⁺, a ≠ 1 — die Variable steht im <b>Exponenten</b>.'),
    ('Warum sind a = 1 und a ≤ 0 als Basis ausgeschlossen?',
     'a = 1 ergäbe die <b>konstante Funktion</b> y = 1; für a ≤ 0 sind Potenzen wie a^(1/2) nicht für alle reellen Exponenten definiert.'),
    ('Unterschied 2ˣ und x²?',
     '<b>2ˣ</b>: Exponentialfunktion (Variable im Exponenten), <b>x²</b>: Potenzfunktion. Für grosse x gewinnt 2ˣ haushoch: 2¹⁰ = 1024, aber 10² = 100.'),
    ('Was ist die <i>e-Funktion</i>?',
     'Die Exponentialfunktion <b>y = eˣ</b> mit der irrationalen Basis e ≈ 2.71828 (Eulersche Zahl).'),
    ('Wie ist die Eulersche Zahl e definiert?',
     'Als Grenzwert <b>(1 + 1/x)ˣ für x → ∞</b> — z.B. Zinseszins bei immer feinerer Gutschrift.'),
    # Eigenschaften
    ('D und W von y = aˣ?',
     '<b>D = ℝ, W = ℝ⁺</b> — die Funktionswerte sind immer positiv, nie null.'),
    ('Gemeinsamer Punkt aller Exponentialkurven?',
     '<b>(0|1)</b> — denn a⁰ = 1 für jede zulässige Basis.'),
    ('Asymptote von y = aˣ?',
     'Die <b>x-Achse</b> (y = 0). Sie wird nie erreicht: aˣ = 0 hat keine Lösung.'),
    ('Verlauf bei a &gt; 1 bzw. a &lt; 1?',
     'a &gt; 1: <b>steigend</b> (Wachstum) · 0 &lt; a &lt; 1: <b>fallend</b> (Zerfall).'),
    ('Spiegelung von y = aˣ an der y-Achse?',
     '<b>a⁻ˣ = (1/a)ˣ</b> — aus Wachstum wird Zerfall und umgekehrt.'),
    ('Wann hat k·aˣ + v eine Nullstelle?',
     'Nur wenn aˣ = −v/k eine <b>positive</b> rechte Seite hat — sonst keine (aˣ &gt; 0).'),
    # Transformationen
    ('Wirkung von v in y = aˣ + v?',
     'Vertikale Verschiebung — die <b>Asymptote wandert mit</b> zu y = v.'),
    ('Besonderheit: Streckung in y vs. Verschiebung in x?',
     'Bei Exponentialfunktionen <b>dasselbe</b>: a^(x−u) = a⁻ᵘ·aˣ = k·aˣ. Identisch, wenn k·aᵘ = 1, d.h. u = −log_a k.'),
    ('Basiswechsel bei Streckung in x-Richtung?',
     '<b>a^(b·x) = (aᵇ)ˣ = cˣ</b> mit c = aᵇ — z.B. 2²ˣ = 4ˣ.'),
    ('Wie schreibt man aˣ mit der Basis e?',
     '<b>aˣ = e^(ln a · x)</b> — z.B. 2ˣ = e^(0.693·x).'),
    # Beispiele
    ('y = aˣ geht durch P(3|125). Bestimme a.',
     'a³ = 125 = 5³ → <b>a = 5</b>.'),
    ('Ordinatenabschnitt und Nullstelle von y = 3ˣ − 6?',
     'y₀ = 3⁰ − 6 = <b>−5</b>; Nullstelle 3ˣ = 6 → <b>x₀ = log₃ 6 ≈ 1.63</b>.'),
    ('Modell «Verdopplung alle T Schritte»?',
     '<b>N(t) = N₀ · 2^(t/T)</b> — analog Halbierung: N₀ · 0.5^(t/T).'),
    ('Abnahme um 30 % pro Minute — Funktionsgleichung?',
     'Pro Minute bleiben 70 %: <b>h(t) = h₀ · 0.7ᵗ</b>.'),
    ('Zinseszins mit 2 % Jahreszins?',
     '<b>K(n) = K₀ · 1.02ⁿ</b> — Wachstumsfaktor 1 + p/100.'),
]

# ─── s3-4b Logarithmusfunktionen (Schwerpunkt) ──────────────
s34b_cards = [
    # Definitionen
    ('Was ist eine <i>Logarithmusfunktion</i>?',
     'Eine Funktion <b>f(x) = log_a x</b> mit a ∈ ℝ⁺, a ≠ 1; f : ℝ⁺ → ℝ — die <b>Umkehrfunktion</b> der Exponentialfunktion y = aˣ.'),
    ('Wie entsteht der Graph von log_a x grafisch?',
     'Durch <b>Spiegelung der Exponentialkurve an der Winkelhalbierenden y = x</b>: Jeder Punkt (a|b) wird zu (b|a).'),
    ('D und W von y = log_a x?',
     '<b>D = ℝ⁺, W = ℝ</b> — gegenüber der Exponentialfunktion tauschen D und W die Rollen.'),
    ('Gemeinsamer Punkt aller Logarithmuskurven?',
     '<b>(1|0)</b> — denn log_a 1 = 0 für jede Basis (a⁰ = 1).'),
    ('Nullstelle von y = log_a x?',
     '<b>x₀ = 1</b> — das gespiegelte Gegenstück zum Punkt (0|1) der Exponentialkurve.'),
    ('Asymptote von y = log_a x?',
     'Die <b>y-Achse</b> (x = 0) — eine <b>vertikale</b> Asymptote.'),
    ('Warum ist log_a von 0 oder negativen Zahlen nicht definiert?',
     'Gesucht wäre ein Exponent t mit aᵗ ≤ 0 — unmöglich, denn <b>aᵗ &gt; 0</b> für alle t.'),
    ('Hat die Logarithmuskurve eine horizontale Asymptote?',
     '<b>Nein</b> — W = ℝ: Sie wächst über alle Grenzen, nur immer langsamer. Flach ≠ beschränkt!'),
    # ln und lg
    ('Was ist die <i>ln-Funktion</i>?',
     'Die Logarithmusfunktion mit Basis e: <b>ln x = log_e x</b> (natürlicher Logarithmus).'),
    ('Was bedeutet lg x?',
     'Der <b>Zehnerlogarithmus</b> log₁₀ x — Standard bei logarithmischen Skalen (pH, Phon).'),
    ('Basiswechsel-Formel?',
     '<b>log_a x = ln x / ln a = lg x / lg a</b> — darum genügen dem Taschenrechner ln und log.'),
    ('Streckung in y-Richtung bei Logarithmusfunktionen?',
     'Entspricht einem <b>Basiswechsel</b>: k·log_a x = log_c x, wenn k·log_a c = 1. Alle Log-Kurven sind gestreckte Kopien voneinander.'),
    ('Was ergibt log_a(b·x)?',
     '<b>log_a x + log_a b</b> — Streckung in x-Richtung ist dasselbe wie Verschiebung in y-Richtung.'),
    # Transformationen / Beispiele
    ('Vertikale Asymptote und D von y = log₂(x − 3)?',
     'Asymptote <b>x = 3</b>; Argument positiv: <b>D = {x | x &gt; 3}</b>.'),
    ('Nullstelle von f(x) = log₂ x − 3?',
     'log₂ x = 3 → <b>x₀ = 2³ = 8</b>.'),
    ('Umkehrfunktion bestimmen — Vorgehen?',
     '1. Nach x auflösen (<b>logarithmieren</b> bzw. <b>exponenzieren</b>), 2. Variablen tauschen. Kontrolle: D und W tauschen die Rollen.'),
    ('Umkehrfunktion von y = 5ˣ − 4?',
     'y + 4 = 5ˣ → x = log₅(y + 4) → <b>f⁻¹: y = log₅(x + 4)</b>.'),
    ('P(3|8) liegt auf y = 2ˣ. Welcher Punkt liegt auf y = log₂ x?',
     '<b>(8|3)</b> — Spiegelung an y = x vertauscht die Koordinaten.'),
    ('Weber-Fechner: Wirkung einer Verdopplung der Schallintensität?',
     'L = 10·lg(J/J₀) steigt um <b>10·lg 2 ≈ 3 Phon</b> — Faktoren werden Summanden.'),
    ('pH-Wert: Definition und Umkehrung?',
     '<b>pH = −lg c</b>; Umkehrung durch Exponenzieren: <b>c = 10^(−pH)</b>.'),
]

# ─── s3-5 Trigonometrische Funktionen (Schwerpunkt) ─────────
s35_cards = [
    # Definitionen am Einheitskreis
    ('Was ist sin x am <i>Einheitskreis</i>?',
     'Die <b>y-Koordinate</b> des Punktes P zum Winkel x (Bogenmass).'),
    ('Was ist cos x am <i>Einheitskreis</i>?',
     'Die <b>x-Koordinate</b> des Punktes P — und tan x der <b>Tangentenabschnitt</b> bei x = 1.'),
    ('Warum ist die Sinusfunktion für alle reellen x definiert?',
     'Der Punkt P kann <b>beliebig viele Umdrehungen</b> in beide Richtungen machen: sin(x + 2kπ) = sin x.'),
    ('Definitionsmenge der Tangensfunktion?',
     '<b>D = ℝ \\ {π/2 + kπ}</b> — an diesen Stellen hat tan x <b>Pole</b> (Definitionslücken).'),
    # Eigenschaften
    ('D und W von sin x und cos x?',
     '<b>D = ℝ, W = [−1; 1]</b> — die Koordinaten am Einheitskreis liegen nie ausserhalb.'),
    ('Wertemenge der Tangensfunktion?',
     '<b>W = ℝ</b> — im Gegensatz zu Sinus und Cosinus unbeschränkt.'),
    ('Periodenlängen von sin, cos und tan?',
     'sin und cos: <b>2π</b> · tan: <b>π</b> (halb so lang!).'),
    ('Nullstellen von sin x und cos x?',
     'sin: <b>x₀ = kπ</b> · cos: <b>x₀ = π/2 + kπ</b> — genau versetzt.'),
    ('Symmetrie von Sinus- und Cosinusfunktion?',
     'sin ist <b>ungerade</b> (punktsymmetrisch, sin(−x) = −sin x), cos ist <b>gerade</b> (achsensymmetrisch, cos(−x) = cos x).'),
    ('Kongruenz von Sinus- und Cosinuskurve?',
     'Horizontale Verschiebung um π/2: <b>cos x = sin(x + π/2)</b> und sin x = cos(x − π/2).'),
    ('Was ergibt sin(π − x)?',
     '<b>sin x</b> — Ergänzungsbeziehung; dagegen cos(π − x) = −cos x.'),
    # Transformationen
    ('Wirkung von a in y = a·sin(b(x−u)) + v?',
     'Streckung in y-Richtung — a ist die <b>Amplitude</b> (maximale Auslenkung von der Mittellinie).'),
    ('Wirkung von b in y = a·sin(b(x−u)) + v?',
     'Streckung mit Faktor 1/b in x-Richtung — neue <b>Periode p = 2π/b</b>: grosses b, kurze Periode!'),
    ('Wirkung von u und v in y = a·sin(b(x−u)) + v?',
     'u verschiebt <b>horizontal</b> (rechts für u &gt; 0), v <b>vertikal</b> — die Mittellinie liegt bei y = v.'),
    ('Periodenlänge von y = sin(2x)?',
     '<b>p = 2π/2 = π</b> — die Kurve schwingt doppelt so schnell.'),
    ('Verschiebung x₀ der allgemeinen Sinusfunktion y = a·sin(bx + c)?',
     '<b>x₀ = −c/b</b> — Ausklammern zeigt es: a·sin(b(x + c/b)).'),
    # Harmonische Schwingungen
    ('Form und Grössen einer <i>harmonischen Schwingung</i>?',
     '<b>y = A·sin(ωt + φ)</b>: Amplitude A, Kreisfrequenz ω, Phasenwinkel φ (Bogenmass).'),
    ('Zusammenhang von T, f und ω?',
     '<b>T = 2π/ω</b>, <b>f = 1/T = ω/(2π)</b>, <b>ω = 2πf</b>. Einheit von f: Hertz (1 Hz = 1 s⁻¹).'),
    ('Wie findet man den ersten Hochpunkt von y = a·sin(bx + c)?',
     'Das <b>Argument gleich π/2 setzen</b>: bx + c = π/2 und nach x auflösen. (Cosinus: Argument = 0.)'),
    ('Häufige Taschenrechner-Falle bei Winkelfunktionen?',
     'Falscher Winkelmodus: Für Graphen und Schwingungen immer <b>RAD</b> (Bogenmass) verwenden — sin 30 ist im DEG-Modus 0.5, im RAD-Modus −0.988.'),
]

# ─── Generation ────────────────────────────────────────────
out_dir_51 = 'downloads/grundlagen/g5-1-grundlagen'
# Hinweis: g5-2 Planimetrie wurde in 5.2a/5.2b/5.2c gesplittet. Das alte Deck
# wird ins Archivverzeichnis geschrieben — als Referenz, nicht als aktive Quelle.
out_dir_52 = 'downloads/grundlagen/_archiv_g5-2-planimetrie'
os.makedirs(out_dir_51, exist_ok=True)
os.makedirs(out_dir_52, exist_ok=True)

n51 = build_apkg(os.path.join(out_dir_51, 'ankideck.apkg'),
                 'TALS Mathematik::Grundlagen::5.1 Grundlagen Geometrie',
                 'TALS Mathematik · Grundlagen Geometrie — Skizzen, Grad und Radiant.',
                 g51_cards)
print(f"g5-1: {n51} Karten erzeugt")

n52 = build_apkg(os.path.join(out_dir_52, 'ankideck.apkg'),
                 'TALS Mathematik::Grundlagen::5.2 Planimetrie',
                 'TALS Mathematik · Planimetrie — Vierecke, Dreiecke, Kreis, Ähnlichkeit.',
                 g52_cards)
print(f"g5-2: {n52} Karten erzeugt")

# ─── Neue Decks für g1-1 bis g1-4 und g4-1 bis g4-3 ─────────
NEW_DECKS = [
    ('g1-1-grundlagen',                  '1.1 Grundlagen Algebra',
     'Algebraische Strukturen, Hauptoperation, Hierarchie der Operationen, Rechengesetze.', g11_cards),
    ('g1-2-zahlen-grundoperationen',     '1.2 Zahlen und Grundoperationen',
     'Zahlenmengen ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ, Bruch-Dezimal-Prozent, Intervalle, Vorzeichenregeln.',  g12_cards),
    ('g1-3-algebraische-terme',          '1.3 Algebraische Terme',
     'Gleichartige Glieder, Klammern, binomische Formeln, Faktorisieren.',                  g13_cards),
    ('g1-4-zehnerpotenzen-quadratwurzeln', '1.4 Zehnerpotenzen und Quadratwurzeln',
     'Wissenschaftliche Notation, Potenzgesetze, Quadratwurzeln, Wurzelgesetze.',           g14_cards),
    ('g4-1-grundlagen',                  '4.1 Grundlagen Datenanalyse',
     'Grundgesamtheit, Stichprobe, Merkmalstypen, Datenqualität.',                          g41_cards),
    ('g4-2-diagramme',                   '4.2 Diagramme',
     'Klassieren, vier Standarddiagramme, Verteilungsformen, Streudiagramm.',               g42_cards),
    ('g4-3-masszahlen',                  '4.3 Masszahlen',
     'Mittelwert, Median, Modus, Standardabweichung, Quartile, Robustheit.',                g43_cards),
    ('g5-2a-dreiecke',                   '5.2a Dreiecke',
     'Innenwinkel, spezielle Dreiecke, Dreieckselemente, Kongruenz, Pythagoras-Satzgruppe.', g52a_cards),
    ('g5-2b-vierecke',                    '5.2b Vierecke',
     'Vierecks-Hierarchie, Flächenformeln, Mittellinie, Sehnen- und Tangentenviereck, regelmässige Vielecke.', g52b_cards),
    ('g5-2c-kreis-und-kreisteile',        '5.2c Kreis und Kreisteile',
     'Geraden und Strecken am Kreis, Pi, Umfang und Fläche, Kreisring, Kreissektor und Kreissegment.', g52c_cards),
    ('g5-2d-zentrische-streckung-aehnlichkeit', '5.2d Zentrische Streckung und Ähnlichkeit',
     'Zentrische Streckung, Strahlensätze, Ähnliche Figuren, Ähnlichkeitssätze, Höhe im rechtwinkligen Dreieck (Höhensatz, Kathetensatz).', g52d_cards),
]

new_dirs = []
for slug, deck_short, deck_desc, cards in NEW_DECKS:
    out_dir = f'downloads/grundlagen/{slug}'
    os.makedirs(out_dir, exist_ok=True)
    n = build_apkg(os.path.join(out_dir, 'ankideck.apkg'),
                   f'TALS Mathematik::Grundlagen::{deck_short}',
                   f'TALS Mathematik · {deck_desc}',
                   cards)
    print(f"{slug}: {n} Karten erzeugt")
    new_dirs.append(out_dir)

# ─── Schwerpunkt-Decks (downloads/schwerpunkt/) ─────────────
SP_DECKS = [
    ('s3-2a-potenzfunktionen', '3.2a Potenzfunktionen',
     'Parabeln und Hyperbeln n-ter Ordnung, Symmetrie, Asymptoten, Transformationen.', s32a_cards),
    ('s3-2b-wurzelfunktionen', '3.2b Wurzelfunktionen',
     'Wurzelfunktion als Umkehrfunktion, Spiegelung an y = x, Definitionsbereiche, Wurzelgleichungen.', s32b_cards),
    ('s3-3-polynomfunktionen', '3.3 Polynomfunktionen',
     'Grad und Leitkoeffizient, Linearfaktoren und Vielfachheit, Globalverlauf, Extremstellen.', s33_cards),
    ('s3-4a-exponentialfunktionen', '3.4a Exponentialfunktionen',
     'Basis und Verlauf, Punkt (0|1), Asymptote, Transformationen, e-Funktion und Basiswechsel.', s34a_cards),
    ('s3-4b-logarithmusfunktionen', '3.4b Logarithmusfunktionen',
     'Umkehrfunktion, Spiegelung an y = x, Nullstelle x = 1, Basiswechsel, logarithmische Skalen.', s34b_cards),
    ('s3-5-trigonometrische-funktionen', '3.5 Trigonometrische Funktionen',
     'Einheitskreis, Periodizität und Symmetrien, Transformationen, allgemeine Sinusfunktion, harmonische Schwingungen.', s35_cards),
]

for slug, deck_short, deck_desc, cards in SP_DECKS:
    out_dir = f'downloads/schwerpunkt/{slug}'
    os.makedirs(out_dir, exist_ok=True)
    n = build_apkg(os.path.join(out_dir, 'ankideck.apkg'),
                   f'TALS Mathematik::Schwerpunkt::{deck_short}',
                   f'TALS Mathematik · {deck_desc}',
                   cards)
    print(f"{slug}: {n} Karten erzeugt")
    new_dirs.append(out_dir)


# Test: kann man die wieder lesen?
import sqlite3, zipfile, tempfile
for d in [out_dir_51, out_dir_52] + new_dirs:
    apkg = os.path.join(d, 'ankideck.apkg')
    sz = os.path.getsize(apkg)
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(apkg) as z:
            z.extractall(td)
        con = sqlite3.connect(os.path.join(td, 'collection.anki2'))
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM notes")
        n_notes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM cards")
        n_cards = cur.fetchone()[0]
        con.close()
    print(f"  {apkg}: {sz} bytes, {n_notes} notes, {n_cards} cards")
