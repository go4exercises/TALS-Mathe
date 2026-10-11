// Trainer-Rahmen — gemeinsam für alle Trainer in werkzeuge/ (Gegenstück zu trainer.css).
// Die Karte .tr-karte reicht von ihrer Oberkante bis an den unteren Bildschirmrand, damit Aufgabe,
// Lösung und Bedienelemente auf einen Bildschirm passen; scrollen muss nur die Arbeitsfläche .tr-flaeche.
//   trHoehe()          Höhe neu setzen (nach Änderungen oberhalb der Karte, z.B. Seitenspalte aufgeklappt)
//   trNachUnten(el)    eine Arbeitsfläche ans Ende scrollen, damit der neueste Schritt sichtbar ist
(function () {
  const MIN = 420, RAND = 12;
  function trHoehe() {
    document.querySelectorAll('.tr-karte').forEach(k => {
      const oben = k.getBoundingClientRect().top + window.scrollY;
      k.style.height = Math.max(MIN, Math.floor(window.innerHeight - oben - RAND)) + 'px';
    });
  }
  function trNachUnten(el) { if (el) el.scrollTop = el.scrollHeight; }
  window.trHoehe = trHoehe;
  window.trNachUnten = trNachUnten;
  window.addEventListener('resize', trHoehe);
  window.addEventListener('load', trHoehe);
  document.addEventListener('DOMContentLoaded', trHoehe);
  document.addEventListener('toggle', trHoehe, true);          // Seitenspalte auf- oder zugeklappt
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(trHoehe);
  // Was über der Karte steht, kann seine Höhe ändern (Titel bricht um, Zusammenfassung der Seitenspalte wächst):
  // dann wandert die Karte, und ihre Höhe wird nachgeführt.
  if (window.ResizeObserver) document.addEventListener('DOMContentLoaded', () => {
    const ro = new ResizeObserver(() => trHoehe());
    document.querySelectorAll('.tr-wrap .page-titel, .tr-seite').forEach(el => ro.observe(el));
  });
})();
