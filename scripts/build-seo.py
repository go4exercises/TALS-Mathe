#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  TALS Mathe — Auffindbarkeit: Seiten-Metadaten, sitemap.xml, robots.txt
#
#  Schreibt in jede Seite einen generierten Kopfblock zwischen den Marken
#      <!-- SEO:ANFANG … -->  …  <!-- SEO:ENDE -->
#  (Beschreibung, canonical, Favicons, Open Graph, JSON-LD nach schema.org).
#  Der Block wird bei jedem Lauf ersetzt — von Hand aendert man ihn nie,
#  sondern die Tabelle SEITEN weiter unten.
#
#  Die JSON-LD-Daten folgen schema.org/LearningResource (LRMI). Die
#  RLP-Kompetenzen werden direkt aus der Seite gelesen (.rlp-kompetenzen li),
#  damit Metadaten und sichtbarer Inhalt nicht auseinanderlaufen.
#
#  Schwesterprojekt: TALS Physik hat dieselbe Mechanik (Commit fc4ed40).
#  Aenderungen an Aufbau oder Feldern gehoeren dort ebenfalls hin —
#  Eintrag in TODO-schwesterprojekt.md.
#
#  Aufruf vom Repo-Root:
#      python3 scripts/build-seo.py            # schreiben
#      python3 scripts/build-seo.py --check    # nur pruefen (Exit 1 = veraltet)
#
#  Achtung, zwei Laeufe: dateModified und lastmod kommen aus dem Git-Datum der
#  jeweiligen Datei. Ein Commit, der eine Seite anfasst, macht damit deren
#  eigenen Block um eine Generation veraltet. Nach dem Commit also noch einmal
#  laufen lassen und die Datumsaenderung mitcommitten — danach ist es stabil.
# ─────────────────────────────────────────────────────────────

import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://mathe.begreifbar.ch/'
SEITENNAME = 'Mathe begreifbar'
AUTOR = 'Raphael Arnold Kohler'
LIZENZ = 'https://creativecommons.org/licenses/by-nc/4.0/deed.de'
RLP = ('Rahmenlehrplan für die Berufsmaturität RLP-BM 2030, '
       'Gruppe Technik, Architektur, Life Sciences')
STAND = '2026-08-02'

# Lerngebiete je Fachbereich — Quelle: index.html
GF = 'Grundlagenfach Mathematik'
SF = 'Schwerpunktfach Mathematik'
LG_G = {'1': 'Lerngebiet 1 Arithmetik/Algebra',
        '2': 'Lerngebiet 2 Gleichungen, Ungleichungen und Gleichungssysteme',
        '3': 'Lerngebiet 3 Funktionen',
        '4': 'Lerngebiet 4 Datenanalyse',
        '5': 'Lerngebiet 5 Geometrie'}
LG_S = {'1': 'Lerngebiet 1 Arithmetik/Algebra',
        '2': 'Lerngebiet 2 Gleichungen',
        '3': 'Lerngebiet 3 Funktionen',
        '4': 'Lerngebiet 4 Geometrie'}

# ── Seiten-Tabelle: hier wird gepflegt ───────────────────────────────
# beschreibung: 140–165 Zeichen, eigenstaendig lesbar, mit den Suchbegriffen,
#               die jemand tatsaechlich eingibt.
# themen:       Stichworte fuer schema.org/about
# titel:        nur setzen, wo der <title> der Seite mehrdeutig ist — «1.1
#               Grundlagen» gibt es im Grundlagen- UND im Schwerpunktfach.
# tg:           Teilgebiet fuer educationalAlignment; lg/fach werden aus dem
#               Dateinamen abgeleitet.
SEITEN = {
 'index.html': dict(
   typ='website',
   titel='Mathe begreifbar — interaktives Lehrmittel für die Berufsmaturität',
   beschreibung='Kostenloses interaktives Mathematik-Lehrmittel für die Berufsmaturität TALS nach RLP-BM 2030: Algebra, Gleichungen, Funktionen, Geometrie und Datenanalyse.',
   themen=['Mathematik', 'Berufsmaturität', 'RLP-BM 2030', 'Lehrmittel', 'Algebra', 'Funktionen', 'Geometrie']),
 'glossar.html': dict(
   typ='article', lrt='Glossar',
   titel='Glossar — mathematische Begriffe von A bis Z',
   beschreibung='Mathematik-Glossar der Berufsmaturität: die zentralen Begriffe von A bis Z kurz erklärt, jeweils mit Formel und Verweis auf die passende Themenseite.',
   themen=['Mathematik', 'Glossar', 'Fachbegriffe', 'Berufsmaturität']),
 'clips.html': dict(
   typ='article', lrt='Erklärclip',
   titel='Clips — kurze Animationen zu den Rechenwegen',
   beschreibung='Kurze Animationen der BM-Mathematik: Ein Clip baut einen Rechenweg Zeile für Zeile auf, mit Farbführung und Text zum Mitlesen. Nach Lerngebieten geordnet.',
   themen=['Mathematik', 'Erklärclip', 'Animation', 'Berufsmaturität', 'Rechenweg']),
 'leitprogramme.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramme — selbstständig durch ein Thema',
   beschreibung='Leitprogramme der BM-Mathematik: Ein Thema in Kapiteln zum selbstständigen Durcharbeiten, mit Vorwissenstest, Beispielen, Aufgaben und Gesamttest.',
   themen=['Mathematik', 'Leitprogramm', 'Selbststudium', 'Berufsmaturität']),
 'leitprogramme/potenzen.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Potenzen — von ℕ über ℤ zu ℚ',
   beschreibung='Leitprogramm Potenzen: die Potenzregeln erst mit natürlichen, dann mit ganzen, dann mit rationalen Exponenten — und Wurzeln ganz ohne Wurzelgesetze.',
   themen=['Mathematik', 'Potenzen', 'Potenzgesetze', 'Wurzeln', 'Leitprogramm']),
 'leitprogramme/uebungspruefung-1.html': dict(
   typ='article', lrt='Leitprogramm', noindex=True,
   titel='Übungsprüfung 1 — Arithmetik, Algebra, Gleichungen',
   beschreibung='Eine vollständige BM2-Übungsprüfung zu Arithmetik, Algebra und linearen Gleichungen: Prüfungsbogen, Musterlösung mit Punkteschlüssel und zu jeder der 26 Teilaufgaben ein vertonter Clip.',
   themen=['Mathematik', 'Übungsprüfung', 'Arithmetik', 'Algebra', 'Lineare Gleichungen', 'Leitprogramm']),
 'formelsammlung.html': dict(
   typ='article', lrt='Formelsammlung',
   titel='Formelsammlung Mathematik — alle Formeln nach Lerngebieten',
   beschreibung='Alle Formeln der BM-Mathematik auf einer Seite: Arithmetik, Gleichungen, Funktionen, Datenanalyse und Geometrie, geordnet nach den Lerngebieten des RLP-BM 2030.',
   themen=['Mathematik', 'Formelsammlung', 'Formeln', 'Berufsmaturität']),
 'rechtliches.html': dict(
   typ='website',
   titel='Rechtliches & Datenschutz',
   beschreibung='Verantwortlichkeit, Haftung, Lizenz und Datenschutz von Mathe begreifbar — ohne Cookies, ohne Tracking, alle Inhalte unter CC BY-NC 4.0.',
   themen=['Impressum', 'Datenschutz', 'Lizenz']),
 'feedback.html': dict(
   typ='website',
   titel='Kontakt & Feedback',
   beschreibung='Fehler melden, Verbesserungen vorschlagen oder Rückmeldung geben zu Mathe begreifbar — ohne Anmeldung, Name und E-Mail freiwillig.',
   themen=['Kontakt', 'Feedback']),

 # ── Grundlagenfach ────────────────────────────────────────────────
 'grundlagen/g1-1-grundlagen.html': dict(
   titel='1.1 Grundlagen der Termstruktur — Grundlagenfach — Mathe begreifbar',
   beschreibung='Struktur algebraischer Terme: Hauptoperation erkennen, Strukturbaum lesen, Hierarchie der Operationen und die Rechengesetze für sicheres Umformen.',
   themen=['Term', 'Variable', 'Hauptoperation', 'Hierarchie der Operationen', 'Rechengesetze'],
   tg='1.1 Grundlagen'),
 'grundlagen/g1-2-zahlen-grundoperationen.html': dict(
   beschreibung='Die Zahlenmengen ℕ, ℤ, ℚ und ℝ, Bruch-, Dezimal- und Prozentdarstellung, Vorzeichenregeln, Betrag, Runden und Intervalle auf der Zahlengeraden.',
   themen=['Zahlenmengen', 'Bruchrechnen', 'Vorzeichenregeln', 'Betrag', 'Intervalle', 'Runden'],
   tg='1.2 Zahlen und zugehörige Grundoperationen'),
 'grundlagen/g1-3-algebraische-terme.html': dict(
   beschreibung='Rechnen mit algebraischen Termen: gleichartige Glieder zusammenfassen, Klammern auflösen, die binomischen Formeln und das Faktorisieren in Produkte.',
   themen=['Algebraische Terme', 'Binomische Formeln', 'Ausklammern', 'Faktorisieren', 'Klammerregeln'],
   tg='1.3 Grundoperationen mit algebraischen Termen'),
 'grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html': dict(
   beschreibung='Zehnerpotenzen und wissenschaftliche Notation, Potenz- und Wurzelgesetze, Quadratwurzeln — und die Hierarchie, wenn Potenzen und Wurzeln zusammentreffen.',
   themen=['Zehnerpotenzen', 'Wissenschaftliche Notation', 'Potenzgesetze', 'Quadratwurzel', 'Wurzelgesetze'],
   tg='1.4 Zehnerpotenzen und Quadratwurzeln'),
 'grundlagen/g2-1-grundlagen.html': dict(
   titel='2.1 Grundlagen der Gleichungslehre — Grundlagenfach — Mathe begreifbar',
   beschreibung='Die Waage als Modell: Sachverhalte als Gleichung oder Ungleichung formulieren, algebraische Äquivalenz, Gleichungstypen erkennen, lösen und Probe machen.',
   themen=['Gleichung', 'Ungleichung', 'Äquivalenzumformung', 'Lösungsmenge', 'Probe'],
   tg='2.1 Grundlagen'),
 'grundlagen/g2-2a-lineare-gleichungen.html': dict(
   beschreibung='Lineare Gleichungen und Ungleichungen: Normalform, Äquivalenzumformungen, die drei Lösungsfälle, Parameterdiskussion und die grafische Deutung als Gerade.',
   themen=['Lineare Gleichung', 'Äquivalenzumformung', 'Lösungsfälle', 'Parameterdiskussion', 'Lineare Ungleichung'],
   tg='2.2 Lineare und quadratische Gleichungen'),
 'grundlagen/g2-2b-quadratische-gleichungen.html': dict(
   beschreibung='Quadratische Gleichungen lösen: Lösungsformel, Faktorisieren, quadratisches Ergänzen, Diskriminante und Anzahl Lösungen sowie der Satz von Vieta.',
   themen=['Quadratische Gleichung', 'Lösungsformel', 'Diskriminante', 'Satz von Vieta', 'Quadratisches Ergänzen'],
   tg='2.2 Lineare und quadratische Gleichungen'),
 'grundlagen/g2-3-lineare-gleichungssysteme.html': dict(
   beschreibung='Lineare Gleichungssysteme mit zwei und drei Variablen: Einsetzen, Gleichsetzen, Addition und Gauss, die drei Lösungsfälle und ihre grafische Deutung.',
   themen=['Lineares Gleichungssystem', 'Einsetzungsverfahren', 'Additionsverfahren', 'Gauss-Verfahren', 'Lösungsfälle'],
   tg='2.3 Lineare Gleichungssysteme'),
 'grundlagen/g3-1-grundlagen.html': dict(
   titel='3.1 Grundlagen der Funktionenlehre — Grundlagenfach — Mathe begreifbar',
   beschreibung='Was eine Funktion ist: vier Darstellungsformen, Schreibweisen, Definitions- und Wertemenge, Vertikaltest sowie Schnittpunkte mit den Achsen und untereinander.',
   themen=['Funktion', 'Definitionsmenge', 'Wertemenge', 'Funktionsgraph', 'Nullstelle', 'Schnittpunkt'],
   tg='3.1 Grundlagen'),
 'grundlagen/g3-2-lineare-funktionen.html': dict(
   beschreibung='Lineare Funktionen: Steigung und Achsenabschnitt geometrisch deuten, Nullstelle berechnen, Typen unterscheiden und die Funktionsgleichung einer Geraden aufstellen.',
   themen=['Lineare Funktion', 'Steigung', 'y-Achsenabschnitt', 'Gerade', 'Steigungsdreieck'],
   tg='3.2 Lineare Funktionen'),
 'grundlagen/g3-3-quadratische-funktionen.html': dict(
   beschreibung='Quadratische Funktionen: Grund-, Scheitel- und Produktform, Öffnung, Scheitelpunkt und Nullstellen, Diskriminante sowie Extremwertaufgaben lösen.',
   themen=['Quadratische Funktion', 'Parabel', 'Scheitelform', 'Produktform', 'Diskriminante', 'Extremwertaufgabe'],
   tg='3.3 Quadratische Funktionen'),
 'grundlagen/g4-0-praxisbeispiel-bm2-klasse.html': dict(
   beschreibung='Datenanalyse an einem durchgehenden Beispiel: Erhebung in einer BM2-Klasse, Urliste, Kennzahlen, alle vier Diagrammtypen, Stichprobe und Datenqualität.',
   themen=['Datenanalyse', 'Urliste', 'Stichprobe', 'Kennzahlen', 'Diagramme', 'Datenqualität']),
   # kein tg: die Seite ist eine TALS-Ergaenzung und traegt keine RLP-Kompetenzbox
 'grundlagen/g4-1-grundlagen.html': dict(
   titel='4.1 Grundlagen der Datenanalyse — Grundlagenfach — Mathe begreifbar',
   beschreibung='Grundbegriffe der Datenanalyse: Grundgesamtheit, Urliste, Stichprobe und Rang, Merkmalstypen, Tabellenkalkulation als Werkzeug und die Frage der Datenqualität.',
   themen=['Datenanalyse', 'Grundgesamtheit', 'Stichprobe', 'Merkmalstypen', 'Tabellenkalkulation'],
   tg='4.1 Grundlagen'),
 'grundlagen/g4-2-diagramme.html': dict(
   beschreibung='Diagramme der Datenanalyse: Klassieren, die vier Standarddiagramme, symmetrisch oder schief charakterisieren und bivariate Daten im Streudiagramm.',
   themen=['Diagramm', 'Histogramm', 'Boxplot', 'Streudiagramm', 'Klassieren', 'Bivariate Daten'],
   tg='4.2 Diagramme'),
 'grundlagen/g4-3-masszahlen.html': dict(
   beschreibung='Lage- und Streumasse: Mittelwert, Median und Modus, Standardabweichung und Quartilsdifferenz — und wann der Median die ehrlichere Auskunft gibt.',
   themen=['Mittelwert', 'Median', 'Modus', 'Standardabweichung', 'Quartilsdifferenz', 'Robustheit'],
   tg='4.3 Masszahlen'),
 'grundlagen/g5-1-grundlagen.html': dict(
   titel='5.1 Grundlagen der Geometrie — Grundlagenfach — Mathe begreifbar',
   beschreibung='Geometrische Grundlagen: Winkeltypen und Winkelpaare, Grad und Radiant ineinander umrechnen sowie Skizzieren als Workflow zur Plausibilitätsprüfung.',
   themen=['Winkel', 'Radiant', 'Gradmass', 'Skizze', 'Plausibilität'],
   tg='5.1 Grundlagen'),
 'grundlagen/g5-2a-dreiecke.html': dict(
   beschreibung='Dreiecke: Eckpunkte, Seiten und Winkel, Innenwinkelsumme mit Beweis, spezielle Dreiecke und Transversalen, Umfang, Fläche, Kongruenz und Pythagoras.',
   themen=['Dreieck', 'Innenwinkelsumme', 'Satz des Pythagoras', 'Kongruenz', 'Höhe', 'Mittelsenkrechte'],
   tg='5.2 Ebene Figuren'),
 'grundlagen/g5-2b-vierecke.html': dict(
   beschreibung='Vierecke und ihre Hierarchie: Quadrat, Rechteck, Raute, Parallelogramm, Trapez und Drachen — Zerlegung in Dreiecke, Umfang und Flächeninhalt.',
   themen=['Viereck', 'Parallelogramm', 'Trapez', 'Raute', 'Drachenviereck', 'Flächeninhalt'],
   tg='5.2 Ebene Figuren'),
 'grundlagen/g5-2c-kreis-und-kreisteile.html': dict(
   beschreibung='Kreis und Kreisteile: Radius, Durchmesser, Sehne, Sekante und Tangente, die Kreiszahl π, Umfang und Fläche sowie Kreissektor und Kreisbogen berechnen.',
   themen=['Kreis', 'Kreiszahl Pi', 'Kreissektor', 'Kreisbogen', 'Tangente', 'Sehne'],
   tg='5.2 Ebene Figuren'),
 'grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html': dict(
   beschreibung='Zentrische Streckung und Ähnlichkeit: Streckzentrum und Streckfaktor, die Strahlensätze, ähnliche Figuren und die Ähnlichkeitssätze für Dreiecke.',
   themen=['Zentrische Streckung', 'Strahlensatz', 'Ähnlichkeit', 'Streckfaktor', 'Ähnlichkeitssätze'],
   tg='5.2 Ebene Figuren'),
 'grundlagen/g5-3-trigonometrische-berechnungen.html': dict(
   beschreibung='Trigonometrie am Dreieck: Sinus, Cosinus und Tangens am rechtwinkligen Dreieck, dazu Sinussatz und Cosinussatz für beliebige schiefwinklige Dreiecke.',
   themen=['Trigonometrie', 'Sinus', 'Cosinus', 'Tangens', 'Sinussatz', 'Cosinussatz'],
   tg='5.3 Trigonometrische Berechnungen'),
 'grundlagen/g5-4-einheitskreis.html': dict(
   beschreibung='Der Einheitskreis: Sinus, Cosinus und Tangens für beliebige Winkel definieren, Funktionswerte ablesen, trigonometrischer Pythagoras und Symmetrien.',
   themen=['Einheitskreis', 'Sinus', 'Cosinus', 'Tangens', 'Trigonometrischer Pythagoras', 'Periodizität'],
   tg='5.4 Einheitskreis'),
 'grundlagen/g5-5-trigonometrische-gleichungen.html': dict(
   beschreibung='Trigonometrische Gleichungen lösen: die drei Grundtypen, Visualisierung am Einheitskreis und an der Sinuskurve, Arcusfunktionen und die volle Lösungsmenge.',
   themen=['Trigonometrische Gleichung', 'Arcusfunktion', 'Einheitskreis', 'Periodizität', 'Lösungsmenge'],
   tg='5.5 Trigonometrische Gleichungen'),

 # ── Schwerpunktfach ───────────────────────────────────────────────
 'schwerpunkt/s1-1-grundlagen.html': dict(
   titel='1.1 Struktur algebraischer Ausdrücke — Schwerpunktfach — Mathe begreifbar',
   beschreibung='Struktur statt Rezept: warum (a+b)² nicht a²+b² ist, welche Umform-Werkzeuge in welche Richtung wirken und welche Struktur-Regeln wann erlaubt sind.',
   themen=['Termstruktur', 'Umformen', 'Binomische Formeln', 'Rechengesetze', 'Gegenbeispiel'],
   tg='1.1 Grundlagen'),
 'schwerpunkt/s1-2-potenzen.html': dict(
   beschreibung='Potenzen mit ganzzahligen und rationalen Exponenten: die fünf Potenzgesetze, Wurzeln als Potenzen schreiben und die Hierarchie mit Zehnerpotenzen.',
   themen=['Potenzen', 'Potenzgesetze', 'Rationale Exponenten', 'Wurzeln als Potenzen', 'Zehnerpotenzen'],
   tg='1.2 Potenzen'),
 'schwerpunkt/s1-3-logarithmen.html': dict(
   beschreibung='Logarithmen: Definition und die Spezialbasen lg, ln und ld, die drei Logarithmengesetze, der Basiswechsel und das Lösen von Exponentialgleichungen.',
   themen=['Logarithmus', 'Logarithmengesetze', 'Basiswechsel', 'Natürlicher Logarithmus', 'Exponentialgleichung'],
   tg='1.3 Logarithmen'),
 'schwerpunkt/s2-1-grundlagen.html': dict(
   titel='2.1 Gleichungstypen bestimmen — Schwerpunktfach — Mathe begreifbar',
   beschreibung='Den Typ einer Gleichung am Ort der Unbekannten erkennen — Landkarte aller Typen, passende Lösungsmethode wählen und das Ergebnis mit der Probe absichern.',
   themen=['Gleichungstypen', 'Unbekannte', 'Lösungsmethode', 'Probe', 'Scheinlösung'],
   tg='2.1 Grundlagen'),
 'schwerpunkt/s2-2a-potenz-wurzel-rationale-gleichungen.html': dict(
   beschreibung='Potenz-, Wurzel- und rationale Gleichungen lösen: Paritätsregel, Quadrieren mit Probe, Definitionsmenge bei Brüchen und Substitution bei mehrfacher Wurzel.',
   themen=['Potenzgleichung', 'Wurzelgleichung', 'Rationale Gleichung', 'Scheinlösung', 'Substitution'],
   tg='2.2 Gleichungen und Ungleichungen'),
 'schwerpunkt/s2-2b-exponential-logarithmische-gleichungen.html': dict(
   beschreibung='Exponential- und Logarithmusgleichungen: Exponentenvergleich, Logarithmieren, Ausklammern und Substitution — dazu Definitionsmenge und Probe.',
   themen=['Exponentialgleichung', 'Logarithmusgleichung', 'Exponentenvergleich', 'Substitution', 'Definitionsmenge'],
   tg='2.2 Gleichungen und Ungleichungen'),
 'schwerpunkt/s2-2c-betrag-polynom-ungleichungen.html': dict(
   beschreibung='Betrags- und Polynomgleichungen sowie Ungleichungen: Fallunterscheidung, Nullprodukt, Vorzeichentabelle und der Betrag als Abstand auf der Zahlengeraden.',
   themen=['Betragsgleichung', 'Polynomgleichung', 'Ungleichung', 'Vorzeichentabelle', 'Nullprodukt'],
   tg='2.2 Gleichungen und Ungleichungen'),
 'schwerpunkt/s3-1-grundlagen.html': dict(
   titel='3.1 Elementare Funktionen und Transformationen — Schwerpunktfach — Mathe begreifbar',
   beschreibung='Die Grundgraphen im Steckbrief und ein Transformationsschema für alle Funktionen — dazu Schnittpunkte, Ungleichungen grafisch und Extremwertaufgaben.',
   themen=['Elementare Funktionen', 'Funktionstransformation', 'Verschiebung', 'Streckung', 'Extremwertaufgabe'],
   tg='3.1 Grundlagen'),
 'schwerpunkt/s3-2a-potenzfunktionen.html': dict(
   beschreibung='Potenzfunktionen y = a·xⁿ: Parabeln und Hyperbeln n-ter Ordnung, Symmetrie über die Parität des Exponenten, Asymptoten und Transformationen.',
   themen=['Potenzfunktion', 'Hyperbel', 'Parabel n-ter Ordnung', 'Asymptote', 'Symmetrie'],
   tg='3.2 Potenz- und Wurzelfunktionen'),
 'schwerpunkt/s3-2b-wurzelfunktionen.html': dict(
   beschreibung='Wurzelfunktionen als Umkehrung der Potenzfunktion: Spiegelung an y = x, Definitionsmenge, Eigenschaften, Transformationen und Wurzelgleichungen.',
   themen=['Wurzelfunktion', 'Umkehrfunktion', 'Spiegelung an y = x', 'Definitionsmenge', 'Wurzelgleichung'],
   tg='3.2 Potenz- und Wurzelfunktionen'),
 'schwerpunkt/s3-3-polynomfunktionen.html': dict(
   beschreibung='Polynomfunktionen: Linearfaktoren und Nullstellen, Vielfachheit am Graphen ablesen, Verlauf aus Grad und Leitkoeffizient sowie Extremalstellen.',
   themen=['Polynomfunktion', 'Linearfaktor', 'Nullstelle', 'Vielfachheit', 'Leitkoeffizient', 'Globalverlauf'],
   tg='3.3 Polynomfunktionen'),
 'schwerpunkt/s3-4a-exponentialfunktionen.html': dict(
   beschreibung='Exponentialfunktionen y = aˣ: die Basis bestimmt Wachstum oder Zerfall, Asymptote und der Punkt (0|1), Transformationen und die natürliche e-Funktion.',
   themen=['Exponentialfunktion', 'Wachstum', 'Zerfall', 'e-Funktion', 'Asymptote', 'Halbwertszeit'],
   tg='3.4 Exponential- und Logarithmusfunktionen'),
 'schwerpunkt/s3-4b-logarithmusfunktionen.html': dict(
   beschreibung='Logarithmusfunktionen als Umkehrung der Exponentialfunktion: Spiegelung an y = x, Nullstelle (1|0), senkrechte Asymptote und die ln-Funktion.',
   themen=['Logarithmusfunktion', 'Umkehrfunktion', 'ln-Funktion', 'Asymptote', 'Basiswechsel'],
   tg='3.4 Exponential- und Logarithmusfunktionen'),
 'schwerpunkt/s3-5-trigonometrische-funktionen.html': dict(
   beschreibung='Sinus, Cosinus und Tangens als Funktionen: vom Einheitskreis zur Kurve, Periodizität und Symmetrie, allgemeine Sinusfunktion und harmonische Schwingungen.',
   themen=['Sinusfunktion', 'Cosinusfunktion', 'Tangensfunktion', 'Periode', 'Amplitude', 'Schwingung'],
   tg='3.5 Trigonometrische Funktionen'),
 'schwerpunkt/s3-6-betragsfunktionen.html': dict(
   beschreibung='Betragsfunktionen: das V verschieben und strecken, das Umklapp-Prinzip für y = |f(x)|, abschnittsweises Schreiben und das grafische Lösen von Gleichungen.',
   themen=['Betragsfunktion', 'Umklapp-Prinzip', 'Knickpunkt', 'Abschnittsweise Definition', 'Betragsungleichung'],
   tg='3.6 Betragsfunktionen (Ergänzung TALS)'),
 'schwerpunkt/s4-1-grundlagen.html': dict(
   titel='4.1 Grundlagen der Raumgeometrie — Schwerpunktfach — Mathe begreifbar',
   beschreibung='Raumgeometrie in zwei Dimensionen darstellen: Schrägbild und Netz, Lage von Punkt, Gerade und Ebene, Winkel im Raum und die Plausibilitäts-Strategie.',
   themen=['Raumgeometrie', 'Schrägbild', 'Körpernetz', 'Windschief', 'Raumwinkel'],
   tg='4.1 Grundlagen'),
 'schwerpunkt/s4-2a-prismen-zylinder.html': dict(
   beschreibung='Prismen und Kreiszylinder: das Prinzip von Cavalieri, Quader und Würfel, Raumdiagonale, Volumen und Oberfläche sowie das Umstellen der Formeln.',
   themen=['Prisma', 'Zylinder', 'Quader', 'Cavalieri', 'Raumdiagonale', 'Volumen'],
   tg='4.2 Körper'),
 'schwerpunkt/s4-2b-pyramiden-kegel-stuempfe.html': dict(
   beschreibung='Pyramide, Kegel und Stümpfe: warum der Faktor ein Drittel gilt, Mantellinie und Seitenhöhe, Öffnungswinkel, Volumen, Oberfläche und Rückwärtsrechnen.',
   themen=['Pyramide', 'Kegel', 'Pyramidenstumpf', 'Mantellinie', 'Öffnungswinkel', 'Volumen'],
   tg='4.2 Körper'),
 'schwerpunkt/s4-2c-kugel.html': dict(
   beschreibung='Kugel und zusammengesetzte Körper: Archimedes und der Zylinder, Volumen und Oberfläche, Kugelkappe, -segment und -sektor sowie Ähnlichkeit und Dichte.',
   themen=['Kugel', 'Kugelkappe', 'Kugelsektor', 'Archimedes', 'Zusammengesetzte Körper', 'Dichte'],
   tg='4.2 Körper'),
 'schwerpunkt/s4-3a-vektorbegriff-komponenten.html': dict(
   beschreibung='Vektoren: Betrag, Gegenvektor und Komponenten, Addition und Skalierung, Polarform mit Betrag und Winkel, Einheitsvektoren und Linearkombinationen.',
   themen=['Vektor', 'Komponenten', 'Betrag', 'Polarform', 'Einheitsvektor', 'Linearkombination'],
   tg='4.3 Vektorgeometrie'),
 'schwerpunkt/s4-3b-skalarprodukt.html': dict(
   beschreibung='Das Skalarprodukt zweier Vektoren: beide Formeln, das Vorzeichen als Winkelaussage, der Nulltest auf Rechtwinkligkeit, Projektion und Winkel in Figuren.',
   themen=['Skalarprodukt', 'Winkel zwischen Vektoren', 'Orthogonalität', 'Projektion', 'Rechtwinkligkeit'],
   tg='4.3 Vektorgeometrie'),
 'schwerpunkt/s4-3c-geraden.html': dict(
   beschreibung='Geraden in Parameterform: Punktprobe, gegenseitige Lage von zwei Geraden inklusive windschief, Schnittwinkel und der Abstand Punkt–Gerade über das Lot.',
   themen=['Parametergleichung', 'Gerade', 'Windschief', 'Schnittwinkel', 'Lotfusspunkt', 'Abstand'],
   tg='4.3 Vektorgeometrie'),
 'schwerpunkt/s4-3d-ebenen.html': dict(
   beschreibung='Ebenen in Parameterform: aus Punkt und zwei Richtungen oder aus drei Punkten, Punktprobe, Durchstosspunkt einer Geraden und Lagen im Überblick.',
   themen=['Ebene', 'Parametergleichung', 'Durchstosspunkt', 'Punktprobe', 'Lagebeziehung'],
   tg='4.3 Vektorgeometrie (Ergänzung TALS)'),
}

MARKE_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
MARKE_ZU = '<!-- SEO:ENDE -->'

MAKROS = {'cdot': '·', 'Delta': 'Δ', 'delta': 'δ', 'lambda': 'λ', 'alpha': 'α',
          'beta': 'β', 'gamma': 'γ', 'rho': 'ρ', 'omega': 'ω', 'pi': 'π', 'mu': 'µ',
          'circ': '°', 'approx': '≈', 'cdots': '…', 'times': '×', 'frac': '/',
          'mathbb': '', 'mathbf': '', 'longmapsto': '↦', 'longrightarrow': '→',
          'Longleftrightarrow': '⇔', 'Rightarrow': '⇒', 'leq': '≤', 'geq': '≥',
          'neq': '≠', 'in': '∈', 'sqrt': '√', 'varphi': 'φ', 'setminus': '\\',
          'log': 'log', 'ln': 'ln', 'lg': 'lg', 'sin': 'sin', 'cos': 'cos', 'tan': 'tan',
          'vec': '', 'text': '', 'mathrm': '', 'left': '', 'right': '', 'quad': ' '}


def tex_weg(t):
    """LaTeX aus Fliesstext in lesbaren Klartext ueberfuehren."""
    def innen(m):
        x = m.group(1)
        x = re.sub(r'\\([a-zA-Z]+)', lambda k: MAKROS.get(k.group(1), ' '), x)
        # ^ und _ bleiben stehen: ohne sie wird aus a^x ein «ax» und aus
        # log_a(b) ein «a(b)» — in Metadaten waere das schlicht falsch.
        return re.sub(r'[{}$]', '', x).replace('\\', '')
    t = re.sub(r'\\\((.*?)\\\)', innen, t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def kompetenzen(seite_html):
    # bis zum Ende der Liste lesen — das erste </div> schliesst nur .rlp-titel
    m = re.search(r'<div class="rlp-kompetenzen">(.*?)</ul>', seite_html, re.S)
    if not m:
        return []
    return [tex_weg(li) for li in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)]


def titel_von(seite_html):
    m = re.search(r'<title>(.*?)</title>', seite_html, re.S)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''


def git_datum(pfad):
    try:
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', pfad],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or STAND
    except Exception:
        return STAND


def fach_lg(datei):
    """Fachbereich und Lerngebiet aus dem Dateinamen ableiten."""
    name = os.path.basename(datei)
    if datei.startswith('grundlagen/'):
        return GF, LG_G.get(name[1], '')
    if datei.startswith('schwerpunkt/'):
        return SF, LG_S.get(name[1], '')
    return '', ''


def jsonld(url, cfg, titel, komp, ist_thema):
    person = {'@type': 'Person', 'name': AUTOR}
    knoten = {
        '@type': ['LearningResource', 'WebPage'] if ist_thema else 'WebPage',
        '@id': url + '#inhalt',
        'url': url,
        'name': titel,
        'description': cfg['beschreibung'],
        'inLanguage': 'de-CH',
        'isAccessibleForFree': True,
        'license': LIZENZ,
        'creator': person,
        'publisher': person,
        'dateModified': cfg['datum'],
        'isPartOf': {'@id': BASIS + '#website'},
    }
    if cfg.get('themen'):
        knoten['about'] = [{'@type': 'DefinedTerm', 'name': t} for t in cfg['themen']]
        knoten['keywords'] = ', '.join(cfg['themen'])
    if ist_thema or cfg.get('lrt'):
        knoten['learningResourceType'] = cfg.get('lrt', ['Lerneinheit', 'interaktive Simulation', 'Aufgabensammlung'])
        knoten['educationalLevel'] = 'Sekundarstufe II — Berufsmaturität (Schweiz)'
        knoten['typicalAgeRange'] = '16-20'
        knoten['audience'] = {'@type': 'EducationalAudience',
                              'educationalRole': ['student', 'teacher']}
        knoten['interactivityType'] = 'active'
    if komp:
        knoten['teaches'] = komp
    if cfg.get('tg'):
        knoten['educationalAlignment'] = [{
            '@type': 'AlignmentObject',
            'alignmentType': 'teaches',
            'educationalFramework': RLP,
            'targetName': f"{cfg['fach']} · {cfg['lg']} · {cfg['tg']}",
        }]
    graph = [knoten]

    if cfg['datei'] == 'index.html':
        graph.append({
            '@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS,
            'name': SEITENNAME, 'inLanguage': 'de-CH', 'license': LIZENZ,
            'publisher': person,
            'potentialAction': {
                '@type': 'SearchAction',
                'target': {'@type': 'EntryPoint', 'urlTemplate': BASIS + '?q={search_term_string}'},
                'query-input': 'required name=search_term_string',
            },
        })
    else:
        graph.append({'@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS, 'name': SEITENNAME})

    if ist_thema:
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': SEITENNAME, 'item': BASIS},
                {'@type': 'ListItem', 'position': 2, 'name': cfg['fach']},
                {'@type': 'ListItem', 'position': 3, 'name': cfg['lg']},
                {'@type': 'ListItem', 'position': 4, 'name': cfg.get('tg', titel), 'item': url},
            ],
        })
    return {'@context': 'https://schema.org', '@graph': graph}


def block(datei, cfg, seite_html):
    tief = datei.count('/')
    auf = '../' * tief
    url = BASIS + datei
    titel = cfg.get('titel') or titel_von(seite_html)
    ist_thema = datei.startswith(('grundlagen/', 'schwerpunkt/'))
    komp = kompetenzen(seite_html) if ist_thema else []
    fach, lg = fach_lg(datei)
    cfg = dict(cfg, datei=datei, datum=git_datum(datei), fach=fach, lg=lg)
    b = cfg['beschreibung']
    z = [MARKE_AUF,
         f'<meta name="description" content="{html.escape(b, quote=True)}">',
         f'<meta name="author" content="{AUTOR}">']
    # Unverlinkte Seite: nur ueber den Direktlink erreichbar. Das Weglassen aus
    # der Sitemap allein genuegt dafuer nicht — eine Suchmaschine, die die URL
    # anderswoher kennt (geteilter Link, Referrer, Browserleiste), indexiert sie
    # trotzdem. Erst das robots-Meta haelt sie draussen. "nofollow" dazu, damit
    # von hier aus auch die eingebetteten Clipdateien nicht aufgenommen werden;
    # die stehen aus demselben Grund nicht in der Sitemap.
    if cfg.get('noindex'):
        z.append('<meta name="robots" content="noindex, nofollow">')
    z += [
         f'<link rel="canonical" href="{url}">',
         f'<link rel="icon" href="{auf}favicon.svg" type="image/svg+xml">',
         f'<link rel="icon" href="{auf}favicon-32.png" sizes="32x32" type="image/png">',
         f'<link rel="apple-touch-icon" href="{auf}apple-touch-icon.png">',
         f'<meta property="og:type" content="{cfg.get("typ", "article")}">',
         f'<meta property="og:site_name" content="{SEITENNAME}">',
         '<meta property="og:locale" content="de_CH">',
         f'<meta property="og:title" content="{html.escape(titel, quote=True)}">',
         f'<meta property="og:description" content="{html.escape(b, quote=True)}">',
         f'<meta property="og:url" content="{url}">',
         f'<meta property="og:image" content="{BASIS}og-bild.png">',
         '<meta name="twitter:card" content="summary_large_image">',
         '<script type="application/ld+json">',
         json.dumps(jsonld(url, cfg, titel, komp, ist_thema), ensure_ascii=False, indent=1),
         '</script>',
         MARKE_ZU]
    return '\n'.join(z)


def einsetzen(datei, cfg):
    pfad = os.path.join(ROOT, datei)
    s = open(pfad, encoding='utf-8').read()
    neu = block(datei, cfg, s)
    if MARKE_AUF in s:
        s2 = re.sub(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), lambda _: neu, s, flags=re.S)
    else:
        m = re.search(r'</title>\n?', s)
        assert m, f'{datei}: kein <title>'
        s2 = s[:m.end()] + neu + '\n' + s[m.end():]
    geaendert = s2 != s
    return s2, geaendert


def sitemap():
    eintraege = []
    for datei in SEITEN:
        if SEITEN[datei].get('noindex'):
            continue
        eintraege.append((BASIS + datei, git_datum(datei),
                          '1.0' if datei == 'index.html' else
                          '0.8' if datei.startswith(('grundlagen/', 'schwerpunkt/')) else '0.5'))
    z = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, datum, prio in eintraege:
        z += ['  <url>', f'    <loc>{url}</loc>', f'    <lastmod>{datum}</lastmod>',
              f'    <priority>{prio}</priority>', '  </url>']
    z.append('</urlset>')
    return '\n'.join(z) + '\n'


ROBOTS = f"""# {SEITENNAME} — alles darf indexiert werden.
User-agent: *
Allow: /

Sitemap: {BASIS}sitemap.xml
"""


def main(argv):
    pruefen = '--check' in argv
    offen = []
    for datei, cfg in SEITEN.items():
        s2, geaendert = einsetzen(datei, cfg)
        if geaendert:
            offen.append(datei)
            if not pruefen:
                open(os.path.join(ROOT, datei), 'w', encoding='utf-8').write(s2)
    for name, inhalt in (('sitemap.xml', sitemap()), ('robots.txt', ROBOTS)):
        p = os.path.join(ROOT, name)
        alt = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        if alt != inhalt:
            offen.append(name)
            if not pruefen:
                open(p, 'w', encoding='utf-8').write(inhalt)
    if pruefen:
        if offen:
            print('SEO-Metadaten VERALTET:', ', '.join(offen))
            return 1
        print(f'SEO-Metadaten aktuell ({len(SEITEN)} Seiten).')
        return 0
    print(f'{len(SEITEN)} Seiten mit Metadaten versehen, sitemap.xml und robots.txt geschrieben.')
    if offen:
        print('  geändert:', ', '.join(offen))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
