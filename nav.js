// ─────────────────────────────────────────────────────────────
//  TALS Mathematik — Shared Navigation (nav.js)
//  Version 2.0 · RLP-2030-Struktur 1:1 (31 Teilgebiete)
//
//  Einbindung: <script src="../nav.js"></script> (von Themenseiten)
//              <script src="nav.js"></script>    (von index.html)
//  Aufruf:     buildNav({ bereich, id, kapitelNr, kapitelTitel, prev, next, homepage })
// ─────────────────────────────────────────────────────────────

const SITE = {
  grundlagen: [
    { id:'g1-1', nr:'1.1', titel:'Grundlagen', url:'grundlagen/g1-1-grundlagen.html' },
    { id:'g1-2', nr:'1.2', titel:'Zahlen und zugehörige Grundoperationen', url:'grundlagen/g1-2-zahlen-grundoperationen.html' },
    { id:'g1-3', nr:'1.3', titel:'Grundoperationen mit algebraischen Termen', url:'grundlagen/g1-3-algebraische-terme.html' },
    { id:'g1-4', nr:'1.4', titel:'Zehnerpotenzen und Quadratwurzeln', url:'grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html' },
    { id:'g2-1', nr:'2.1', titel:'Grundlagen', url:'grundlagen/g2-1-grundlagen.html' },
    { id:'g2-2a', nr:'2.2a', titel:'Lineare Gleichungen', url:'grundlagen/g2-2a-lineare-gleichungen.html' },
    { id:'g2-2b', nr:'2.2b', titel:'Quadratische Gleichungen', url:'grundlagen/g2-2b-quadratische-gleichungen.html' },
    { id:'g2-3', nr:'2.3', titel:'Lineare Gleichungssysteme', url:'grundlagen/g2-3-lineare-gleichungssysteme.html' },
    { id:'g3-1', nr:'3.1', titel:'Grundlagen', url:'grundlagen/g3-1-grundlagen.html' },
    { id:'g3-2', nr:'3.2', titel:'Lineare Funktionen', url:'grundlagen/g3-2-lineare-funktionen.html' },
    { id:'g3-3', nr:'3.3', titel:'Quadratische Funktionen', url:'grundlagen/g3-3-quadratische-funktionen.html' },
    { id:'g4-0', nr:'4.0', titel:'Praxisbeispiel BM2-Klasse', url:'grundlagen/g4-0-praxisbeispiel-bm2-klasse.html' },
    { id:'g4-1', nr:'4.1', titel:'Grundlagen', url:'grundlagen/g4-1-grundlagen.html' },
    { id:'g4-2', nr:'4.2', titel:'Diagramme', url:'grundlagen/g4-2-diagramme.html' },
    { id:'g4-3', nr:'4.3', titel:'Masszahlen', url:'grundlagen/g4-3-masszahlen.html' },
    { id:'g5-1', nr:'5.1', titel:'Grundlagen', url:'grundlagen/g5-1-grundlagen.html' },
    { id:'g5-2a', nr:'5.2a', titel:'Dreiecke', url:'grundlagen/g5-2a-dreiecke.html' },
    { id:'g5-2b', nr:'5.2b', titel:'Vierecke', url:'grundlagen/g5-2b-vierecke.html' },
    { id:'g5-2c', nr:'5.2c', titel:'Kreis und Kreisteile', url:'grundlagen/g5-2c-kreis-und-kreisteile.html' },
    { id:'g5-2d', nr:'5.2d', titel:'Zentrische Streckung und Ähnlichkeit', url:'grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html' },
    { id:'g5-3', nr:'5.3', titel:'Trigonometrische Berechnungen', url:'grundlagen/g5-3-trigonometrische-berechnungen.html' },
    { id:'g5-4', nr:'5.4', titel:'Einheitskreis', url:'grundlagen/g5-4-einheitskreis.html' },
    { id:'g5-5', nr:'5.5', titel:'Trigonometrische Gleichungen', url:'grundlagen/g5-5-trigonometrische-gleichungen.html' },
  ],
  schwerpunkt: [
    { id:'s1-1', nr:'1.1', titel:'Grundlagen', url:'schwerpunkt/s1-1-grundlagen.html' },
    { id:'s1-2', nr:'1.2', titel:'Potenzen', url:'schwerpunkt/s1-2-potenzen.html' },
    { id:'s1-3', nr:'1.3', titel:'Logarithmen', url:'schwerpunkt/s1-3-logarithmen.html' },
    { id:'s2-1', nr:'2.1', titel:'Grundlagen', url:'schwerpunkt/s2-1-grundlagen.html' },
    { id:'s2-2', nr:'2.2', titel:'Gleichungstypen', url:'schwerpunkt/s2-2-gleichungstypen.html' },
    { id:'s3-1', nr:'3.1', titel:'Grundlagen', url:'schwerpunkt/s3-1-grundlagen.html' },
    { id:'s3-2a', nr:'3.2a', titel:'Potenzfunktionen', url:'schwerpunkt/s3-2a-potenzfunktionen.html' },
    { id:'s3-2b', nr:'3.2b', titel:'Wurzelfunktionen', url:'schwerpunkt/s3-2b-wurzelfunktionen.html' },
    { id:'s3-3', nr:'3.3', titel:'Polynomfunktionen', url:'schwerpunkt/s3-3-polynomfunktionen.html' },
    { id:'s3-4', nr:'3.4', titel:'Exponential- und Logarithmusfunktionen', url:'schwerpunkt/s3-4-exponential-logarithmusfunktionen.html' },
    { id:'s3-5', nr:'3.5', titel:'Trigonometrische Funktionen', url:'schwerpunkt/s3-5-trigonometrische-funktionen.html' },
    { id:'s4-1', nr:'4.1', titel:'Grundlagen', url:'schwerpunkt/s4-1-grundlagen.html' },
    { id:'s4-2', nr:'4.2', titel:'Stereometrie', url:'schwerpunkt/s4-2-stereometrie.html' },
    { id:'s4-3', nr:'4.3', titel:'Zwei- und dreidimensionale Vektorgeometrie', url:'schwerpunkt/s4-3-vektorgeometrie.html' },
  ]
};

// Lerngebiet-Gruppen für die Dropdown-Anzeige
const GROUPS = {
  grundlagen: [
    { nr:'1', titel:'Arithmetik/Algebra', ids:['g1-1', 'g1-2', 'g1-3', 'g1-4'] },
    { nr:'2', titel:'Gleichungen, Ungleichungen und Gleichungssysteme', ids:['g2-1', 'g2-2a', 'g2-2b', 'g2-3'] },
    { nr:'3', titel:'Funktionen', ids:['g3-1', 'g3-2', 'g3-3'] },
    { nr:'4', titel:'Datenanalyse', ids:['g4-0', 'g4-1', 'g4-2', 'g4-3'] },
    { nr:'5', titel:'Geometrie', ids:['g5-1', 'g5-2a', 'g5-2b', 'g5-2c', 'g5-2d', 'g5-3', 'g5-4', 'g5-5'] }
  ],
  schwerpunkt: [
    { nr:'1', titel:'Arithmetik/Algebra', ids:['s1-1', 's1-2', 's1-3'] },
    { nr:'2', titel:'Gleichungen', ids:['s2-1', 's2-2'] },
    { nr:'3', titel:'Funktionen', ids:['s3-1', 's3-2a', 's3-2b', 's3-3', 's3-4', 's3-5'] },
    { nr:'4', titel:'Geometrie', ids:['s4-1', 's4-2', 's4-3'] }
  ]
};

function buildNav(cfg) {
  // cfg = { bereich, id, kapitelNr, kapitelTitel, prev, next, homepage }
  window.__navCfg = cfg;   // Damit buildToC kapitelNr/prev/next nutzen kann.
  const prefix    = cfg.homepage ? '' : '../';
  const indexHref = cfg.homepage ? 'index.html' : '../index.html';

  // Lookup: id → page-Objekt (für Dropdown-Highlight)
  const pageById = {};
  [...SITE.grundlagen, ...SITE.schwerpunkt].forEach(p => pageById[p.id] = p);

  // Dropdown-HTML mit Lerngebiet-Gruppierung
  function renderDropdown(bereich, ddId) {
    const groups = GROUPS[bereich];
    return groups.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'dd-aktiv':''}">
          <span class="dd-nr">${p.nr}</span>
          <span class="dd-tit">${p.titel}</span>
        </a>`;
      }).join('');
      return `<div class="dd-gruppe">
        <div class="dd-gruppe-titel">${g.nr} · ${g.titel}</div>
        ${items}
      </div>`;
    }).join('');
  }

  // Mobile-Nav: gruppiert mit Lerngebiet-Headern
  function renderMobileGroup(bereich) {
    const groups = GROUPS[bereich];
    return groups.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'mn-aktiv':''}">${p.nr} · ${p.titel}</a>`;
      }).join('');
      return `<div class="mn-untergruppe">${g.nr} · ${g.titel}</div>${items}`;
    }).join('');
  }

  // ── META-DROPDOWN-INHALTE (Autor, Ausblick, Feedback, Lizenz) ──
  // Vier kleine Info-Panels rechts im Header, auf jeder Seite identisch.
  const metaAutorHTML = `
    <div class="meta-titel">Autor &amp; Intention</div>
    <p>Erstellt von einem Elektroingenieur mit über 30 Jahren Unterrichtserfahrung,
       der gerne Mathematik und Physik erklärt — seinen Schülerinnen und Schülern
       genauso wie seinen Kindern. Begeistert von dem, was sich mit KI im
       Bildungsbereich machen lässt.</p>
    <p>Dieses Lehrmittel <strong>ersetzt weder Lehrperson noch klassisches Lehrbuch</strong>.
       Es will eine niederschwellige, animierte und animierende Ergänzung sein, die der
       Lehrperson didaktischen Freiraum schafft — zum Beispiel für Methoden wie
       <em>Flipped Classroom</em>.</p>`;

  const metaAusblickHTML = `
    <div class="meta-titel">Ausblick</div>
    <div class="meta-sub">Erstellt</div>
    <ul>
      <li>Inhalte für das Grundlagenfach (23 Themenseiten)</li>
    </ul>
    <div class="meta-sub">Geplant</div>
    <ul>
      <li>Grundlagenfach verfeinern</li>
      <li>Schwerpunktfach erstellen</li>
    </ul>
    <div class="meta-sub">Ideen</div>
    <ul>
      <li>Englische Übersetzung für Immersionsunterricht</li>
      <li>Physik analog aufbereiten</li>
      <li>Mathematik für Passerelle und Gymnasium ergänzen</li>
    </ul>`;

  const metaFeedbackHTML = `
    <div class="meta-titel">Feedback</div>
    <p>Fehler gefunden? Verbesserungsvorschlag? Fehlendes Thema?
       Bitte über den GitHub-Issue-Tracker melden — so geht keine Rückmeldung verloren
       und alle anderen profitieren von der Diskussion.</p>
    <p><a href="https://github.com/go4exercises/TALS-Mathe/issues/new" target="_blank" rel="noopener" class="meta-link">
       → Issue auf GitHub erstellen</a></p>
    <p><em>Feedbackformular folgt.</em></p>`;

  const metaLizenzHTML = `
    <div class="meta-titel">Lizenz</div>
    <p>Inhalte erstellt mit Unterstützung von <strong>Claude Opus 4.7</strong> (Anthropic).</p>
    <p>Veröffentlicht unter <strong>Creative Commons BY-NC 4.0</strong>:
       Inhalte sind frei nutzbar für nicht-kommerzielle Zwecke, dürfen verändert
       und weitergegeben werden — bei Kopien und Weiterverarbeitung bitte auf die
       Herkunft verweisen. Die Inhalte sind frei und sollen frei bleiben.</p>
    <p><a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener" class="meta-link">
       → Lizenztext (CC BY-NC 4.0)</a></p>`;

  // ── HEADER ──────────────────────────────────────────────────
  const headerHTML = `
<header class="site-hdr">
  <a href="${indexHref}" class="logo">
    Mathematik
  </a>
  <nav class="site-nav">
    <div class="dropdown">
      <button class="nav-btn${cfg.bereich==='grundlagen' ? ' aktiv':''}" onclick="toggleDD('dd-gl')">
        Grundlagenfach ▾
      </button>
      <div class="dd-menu dd-menu-gross" id="dd-gl">
        ${renderDropdown('grundlagen','dd-gl')}
      </div>
    </div>
    <div class="dropdown">
      <button class="nav-btn${cfg.bereich==='schwerpunkt' ? ' aktiv':''}" onclick="toggleDD('dd-sp')">
        Schwerpunktfach ▾
      </button>
      <div class="dd-menu dd-menu-gross" id="dd-sp">
        ${renderDropdown('schwerpunkt','dd-sp')}
      </div>
    </div>
    <div class="dropdown">
      <button class="nav-btn${(cfg.id==='glossar'||cfg.id==='formeln') ? ' aktiv':''}" onclick="toggleDD('dd-ref')">
        Nachschlagen ▾
      </button>
      <div class="dd-menu" id="dd-ref">
        <div class="dd-gruppe">
          <div class="dd-gruppe-titel">In diesem Lehrmittel</div>
          <a href="${prefix}glossar.html" class="${cfg.id==='glossar'?'dd-aktiv':''}">
            <span class="dd-nr">A–Z</span><span class="dd-tit">Glossar</span>
          </a>
          <a href="${prefix}formelsammlung.html" class="${cfg.id==='formeln'?'dd-aktiv':''}">
            <span class="dd-nr">∑</span><span class="dd-tit">Formelsammlung</span>
          </a>
        </div>
        <div class="dd-gruppe">
          <div class="dd-gruppe-titel">Extern</div>
          <a href="https://www.sbfi.admin.ch/dam/de/sd-web/xCh9wCCwVgrh/formulaire_final_d.pdf" target="_blank" rel="noopener">
            <span class="dd-nr">PDF</span><span class="dd-tit">SBFI-Formelsammlung (Prüfung)</span>
          </a>
        </div>
      </div>
    </div>
    <a href="https://go4exercises.github.io/TALS-Physik/" target="_blank" rel="noopener">Physik ↗</a>

    <span class="nav-sep" aria-hidden="true"></span>

    <div class="dropdown">
      <button class="nav-btn nav-meta" onclick="toggleDD('dd-ueber')">
        <span class="ueber-icon" aria-hidden="true">ⓘ</span> Über ▾
      </button>
      <div class="dd-menu dd-menu-ueber" id="dd-ueber">
        <div class="ueber-tabs" role="tablist">
          <button class="ueber-tab aktiv" role="tab" data-target="ueber-autor">Autor &amp; Intention</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-ausblick">Ausblick</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-feedback">Feedback</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-lizenz">Lizenz</button>
        </div>
        <div class="ueber-panels">
          <div class="ueber-panel aktiv" id="ueber-autor"   role="tabpanel">${metaAutorHTML}</div>
          <div class="ueber-panel"        id="ueber-ausblick" role="tabpanel">${metaAusblickHTML}</div>
          <div class="ueber-panel"        id="ueber-feedback" role="tabpanel">${metaFeedbackHTML}</div>
          <div class="ueber-panel"        id="ueber-lizenz"   role="tabpanel">${metaLizenzHTML}</div>
        </div>
      </div>
    </div>
  </nav>
  <button class="burger" onclick="toggleMobileNav()" aria-label="Navigation">☰</button>
</header>
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}">← Übersicht</a>
  <div class="mn-gruppe">Grundlagenfach</div>
  ${renderMobileGroup('grundlagen')}
  <div class="mn-gruppe">Schwerpunktfach</div>
  ${renderMobileGroup('schwerpunkt')}
  <a href="https://go4exercises.github.io/TALS-Physik/" target="_blank" rel="noopener">Physik ↗</a>
  <div class="mn-gruppe">Nachschlagen</div>
  <a href="${prefix}glossar.html" class="${cfg.id==='glossar'?'mn-aktiv':''}">A–Z · Glossar</a>
  <a href="${prefix}formelsammlung.html" class="${cfg.id==='formeln'?'mn-aktiv':''}">∑ · Formelsammlung</a>
  <a href="https://www.sbfi.admin.ch/dam/de/sd-web/xCh9wCCwVgrh/formulaire_final_d.pdf" target="_blank" rel="noopener">PDF · SBFI-Formelsammlung</a>
  <div class="mn-gruppe">Über dieses Lehrmittel</div>
  <details class="mn-meta"><summary>Autor &amp; Intention</summary><div class="mn-meta-body">${metaAutorHTML}</div></details>
  <details class="mn-meta"><summary>Ausblick</summary><div class="mn-meta-body">${metaAusblickHTML}</div></details>
  <details class="mn-meta"><summary>Feedback</summary><div class="mn-meta-body">${metaFeedbackHTML}</div></details>
  <details class="mn-meta"><summary>Lizenz</summary><div class="mn-meta-body">${metaLizenzHTML}</div></details>
</div>`;

  // ── INJECT ───────────────────────────────────────────────────
  document.getElementById('nav-root').innerHTML = headerHTML;

  // Close dropdowns on outside click
  document.addEventListener('click', e => {
    if (!e.target.closest('.dropdown') && !e.target.closest('.nav-btn')) {
      document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
    }
  });
}

function toggleDD(id) {
  const el = document.getElementById(id);
  const wasOpen = el.classList.contains('open');
  document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
  if (!wasOpen) el.classList.add('open');
}

// Tabs innerhalb des "Über"-Dropdowns (Autor / Ausblick / Feedback / Lizenz)
document.addEventListener('click', e => {
  const tab = e.target.closest('.ueber-tab');
  if (!tab) return;
  const wrap = tab.closest('.dd-menu-ueber');
  if (!wrap) return;
  wrap.querySelectorAll('.ueber-tab').forEach(t => t.classList.remove('aktiv'));
  wrap.querySelectorAll('.ueber-panel').forEach(p => p.classList.remove('aktiv'));
  tab.classList.add('aktiv');
  const target = wrap.querySelector('#' + tab.dataset.target);
  if (target) target.classList.add('aktiv');
});

function toggleMobileNav() {
  document.getElementById('mobile-nav').classList.toggle('open');
}

// ── Sticky ToC ────────────────────────────────────────────────
// Kurz-Labels für die wiederkehrenden Standard-Slots. Bei nicht
// gelisteten IDs bleibt der originale h2/h3-Text der Seite stehen.
const TOC_KURZ = {
  einstieg:       'Einstieg',
  definition:     'Definition',
  darstellungen:  'Darstellungen',
  typen:          'Typen',
  theorie:        'Theorie',
  aufgaben:       'Aufgaben',
  zusammenfassung:'Zusammenfassung',
  downloads:      'Zusatzmaterial',
  ressourcen:     'Externe V&AS'
};

function buildToC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const headings = document.querySelectorAll('.content h2[id]');
  if (headings.length < 2) { toc.closest('.toc-wrap')?.remove(); return; }

  // Aus buildNav-Aufruf: Kapitelnummer + Prev/Next
  const cfg = window.__navCfg || {};
  const kapitel = cfg.kapitelNr
    ? `Kapitel <span class="toc-kapnr">${cfg.kapitelNr}</span>`
    : 'Auf dieser Seite';
  const prevLink = cfg.prev
    ? `<a href="${cfg.prev.url}" class="toc-prev" title="${cfg.prev.titel}">← ${cfg.prev.nr}</a>`
    : '';
  const nextLink = cfg.next
    ? `<a href="${cfg.next.url}" class="toc-next" title="${cfg.next.titel}">${cfg.next.nr} →</a>`
    : '';

  toc.innerHTML =
    (prevLink ? `<div class="toc-nav toc-nav-oben">${prevLink}</div>` : '') +
    `<button type="button" class="toc-title" title="Zum Seitenanfang">${kapitel}<span class="toc-title-pfeil" aria-hidden="true">↑</span></button>` +
    [...headings].map(h => {
      const label = TOC_KURZ[h.id] || h.textContent;
      return `
      <a href="#${h.id}" class="toc-link toc-${h.tagName.toLowerCase()}" title="${h.textContent.trim()}">
        ${label}
      </a>`;
    }).join('') +
    (nextLink ? `<div class="toc-nav toc-nav-unten">${nextLink}</div>` : '');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
        const link = toc.querySelector(`[href="#${e.target.id}"]`);
        if (link) link.classList.add('toc-aktiv');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  headings.forEach(h => observer.observe(h));

  // Sofortige, konsistente Markierung beim Klick (ohne auf den Observer zu warten);
  // Sprünge sind instant (kein Smooth-Scroll), wie bei der Titelwahl.
  toc.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
      link.classList.add('toc-aktiv');
    });
  });
  // Kapiteltitel = Sprung an den Seitenanfang (instant), Markierung zurücksetzen.
  const titelEl = toc.querySelector('.toc-title');
  if (titelEl) titelEl.addEventListener('click', () => {
    window.scrollTo(0, 0);
    history.replaceState(null, '', location.pathname + location.search);
    document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
  });
}

document.addEventListener('DOMContentLoaded', buildToC);
