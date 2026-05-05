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
    { id:'g2-2', nr:'2.2', titel:'Lineare und quadratische Gleichungen', url:'grundlagen/g2-2-lineare-quadratische-gleichungen.html' },
    { id:'g2-3', nr:'2.3', titel:'Lineare Gleichungssysteme', url:'grundlagen/g2-3-lineare-gleichungssysteme.html' },
    { id:'g3-1', nr:'3.1', titel:'Grundlagen', url:'grundlagen/g3-1-grundlagen.html' },
    { id:'g3-2', nr:'3.2', titel:'Lineare Funktionen', url:'grundlagen/g3-2-lineare-funktionen.html' },
    { id:'g3-3', nr:'3.3', titel:'Quadratische Funktionen', url:'grundlagen/g3-3-quadratische-funktionen.html' },
    { id:'g4-1', nr:'4.1', titel:'Grundlagen', url:'grundlagen/g4-1-grundlagen.html' },
    { id:'g4-2', nr:'4.2', titel:'Diagramme', url:'grundlagen/g4-2-diagramme.html' },
    { id:'g4-3', nr:'4.3', titel:'Masszahlen', url:'grundlagen/g4-3-masszahlen.html' },
    { id:'g5-1', nr:'5.1', titel:'Grundlagen', url:'grundlagen/g5-1-grundlagen.html' },
    { id:'g5-2', nr:'5.2', titel:'Planimetrie', url:'grundlagen/g5-2-planimetrie.html' },
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
    { id:'s3-2', nr:'3.2', titel:'Potenz- und Wurzelfunktionen', url:'schwerpunkt/s3-2-potenz-wurzelfunktionen.html' },
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
    { nr:'2', titel:'Gleichungen, Ungleichungen und Gleichungssysteme', ids:['g2-1', 'g2-2', 'g2-3'] },
    { nr:'3', titel:'Funktionen', ids:['g3-1', 'g3-2', 'g3-3'] },
    { nr:'4', titel:'Datenanalyse', ids:['g4-1', 'g4-2', 'g4-3'] },
    { nr:'5', titel:'Geometrie', ids:['g5-1', 'g5-2', 'g5-3', 'g5-4', 'g5-5'] }
  ],
  schwerpunkt: [
    { nr:'1', titel:'Arithmetik/Algebra', ids:['s1-1', 's1-2', 's1-3'] },
    { nr:'2', titel:'Gleichungen', ids:['s2-1', 's2-2'] },
    { nr:'3', titel:'Funktionen', ids:['s3-1', 's3-2', 's3-3', 's3-4', 's3-5'] },
    { nr:'4', titel:'Geometrie', ids:['s4-1', 's4-2', 's4-3'] }
  ]
};

function buildNav(cfg) {
  // cfg = { bereich, id, kapitelNr, kapitelTitel, prev, next, homepage }
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

  // ── HEADER ──────────────────────────────────────────────────
  const headerHTML = `
<header class="site-hdr">
  <a href="${indexHref}" class="logo">
    <span class="logo-pill">TALS</span>Mathematik
  </a>
  <nav class="site-nav">
    <a href="${indexHref}">Übersicht</a>
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
    <a href="https://www.sbfi.admin.ch/dam/de/sd-web/xCh9wCCwVgrh/formulaire_final_d.pdf" target="_blank" rel="noopener">Formelsammlung</a>
  </nav>
  <button class="burger" onclick="toggleMobileNav()" aria-label="Navigation">☰</button>
</header>
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}">← Übersicht</a>
  <div class="mn-gruppe">Grundlagenfach</div>
  ${renderMobileGroup('grundlagen')}
  <div class="mn-gruppe">Schwerpunktfach</div>
  ${renderMobileGroup('schwerpunkt')}
</div>`;

  // ── BREADCRUMB + PREV/NEXT ───────────────────────────────────
  const fachLabel  = cfg.bereich === 'grundlagen' ? 'Grundlagenfach' : 'Schwerpunktfach';
  const fachHash   = cfg.bereich === 'grundlagen' ? '#gl' : '#sp';

  const prevBtn = cfg.prev
    ? `<a href="${cfg.prev.url}" class="pn-btn pn-prev" title="${cfg.prev.titel}">
         ← <span class="pn-nr">${cfg.prev.nr}</span>
         <span class="pn-tit">${cfg.prev.titel}</span>
       </a>`
    : `<span class="pn-btn pn-prev pn-dis">← Erstes Kapitel</span>`;

  const nextBtn = cfg.next
    ? `<a href="${cfg.next.url}" class="pn-btn pn-next" title="${cfg.next.titel}">
         <span class="pn-nr">${cfg.next.nr}</span>
         <span class="pn-tit">${cfg.next.titel}</span> →
       </a>`
    : `<span class="pn-btn pn-next pn-dis">Letztes Kapitel →</span>`;

  const bcHTML = `
<div class="breadcrumb-bar">
  <div class="breadcrumb">
    <a href="${indexHref}">Übersicht</a>
    <span class="bc-sep">›</span>
    <a href="${indexHref}${fachHash}">${fachLabel}</a>
    <span class="bc-sep">›</span>
    <span class="bc-cur">${cfg.kapitelNr} · ${cfg.kapitelTitel}</span>
  </div>
  <div class="prev-next">
    ${prevBtn}
    ${nextBtn}
  </div>
</div>`;

  // ── INJECT ───────────────────────────────────────────────────
  document.getElementById('nav-root').innerHTML = cfg.homepage ? headerHTML : (headerHTML + bcHTML);

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

function toggleMobileNav() {
  document.getElementById('mobile-nav').classList.toggle('open');
}

// ── Sticky ToC ────────────────────────────────────────────────
function buildToC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const headings = document.querySelectorAll('.content h2[id], .content h3[id]');
  if (headings.length < 2) { toc.closest('.toc-wrap')?.remove(); return; }

  toc.innerHTML = '<div class="toc-title">Auf dieser Seite</div>' +
    [...headings].map(h => `
      <a href="#${h.id}" class="toc-link toc-${h.tagName.toLowerCase()}">
        ${h.textContent}
      </a>`).join('');

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
}

document.addEventListener('DOMContentLoaded', buildToC);
