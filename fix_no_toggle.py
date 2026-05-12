#!/usr/bin/env python3
"""
Remove MAP/LIST toggle; make map+leaderboard and course list always visible.
Filter row moves to always-on between hero and map.
"ALL COURSES" editorial section wraps the course grid.
"""

HTML_PATH = 'cyntp-courses.html'
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

def replace_once(old, new, label):
    global html
    if old not in html:
        errors.append(f'NOT FOUND: {label}')
        return
    html = html.replace(old, new, 1)
    print(f'  OK: {label}')

# ══════════════════════════════════════════════════════════════════════
# CSS-1: Remove VIEW TOGGLE block entirely
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''/* ── VIEW TOGGLE ─────────────────────────────────────────────────────── */
.vtog-wrap {
  display: flex; border: 1px solid #d4a055; border-radius: 8px; overflow: hidden;
}
.vtog-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 10px 22px; border: none; border-radius: 0;
  font-family: var(--font-body); font-size: 11px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: #d4a055; background: transparent;
  cursor: pointer; transition: all 0.2s; min-height: 44px;
}
.vtog-btn + .vtog-btn { border-left: 1px solid #d4a055; }
.vtog-btn:hover { background: rgba(212,160,85,0.15); }
.vtog-btn.active { background: #d4a055; color: #0d0d0d; }
.vtog-btn svg { width: 14px; height: 14px; flex-shrink: 0; }
.ph-stats .vtog-wrap { margin-left: auto; }''',
    '',
    'VIEW TOGGLE CSS block removed'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-2: Remove body.view-map filter hide rule
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''/* ── Hide list-only controls in MAP view ────────────────────────────── */
body.view-map .filter-bar { display: none !important; }''',
    '',
    'body.view-map .filter-bar rule removed'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-3: course-grid-wrap — remove padding (section handles it)
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '.course-grid-wrap { padding: 48px 80px 80px; }',
    '.course-grid-wrap { padding: 0; }',
    'course-grid-wrap padding stripped (section handles it)'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-4: Add ALL COURSES section CSS before map pin block
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '/* ── MAP PIN & CLUSTER ───────────────────────────────────────────────── */',
    '''/* ── ALL COURSES SECTION ────────────────────────────────────────────── */
.all-courses-section { background: var(--ink); padding: 64px 80px 80px; }
.ac-eyebrow {
  display: flex; align-items: center; gap: 10px;
  font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
  color: #d4a055; font-weight: 600; margin-bottom: 20px;
}
.ac-eyebrow::before {
  content: ''; width: 20px; height: 2px;
  background: #d4a055; border-radius: 2px; flex-shrink: 0;
}
.ac-divider { height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 40px; }

/* ── MAP PIN & CLUSTER ───────────────────────────────────────────────── */''',
    'ALL COURSES section CSS added'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-5: Update 960px breakpoint — swap course-grid-wrap padding for
#        all-courses-section padding; keep other rules intact
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '  .course-grid-wrap { padding: 32px 20px 60px; }',
    '  .all-courses-section { padding: 48px 20px 60px; }',
    '960px course-grid-wrap → all-courses-section padding'
)

# ══════════════════════════════════════════════════════════════════════
# HTML-1: Remove vtog-wrap from hero stats row
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''    <div class="vtog-wrap" role="group" aria-label="View mode">
      <button class="vtog-btn active" id="vtogMap" aria-pressed="true" onclick="setView('map')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M10 2l4 2v10l-4-2-4 2-4-2V2l4 2 4-2z"/><path d="M6 4v10M10 2v10"/></svg>
        Map
      </button>
      <button class="vtog-btn" id="vtogList" aria-pressed="false" onclick="setView('list')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><line x1="4" y1="4" x2="14" y2="4"/><line x1="4" y1="8" x2="14" y2="8"/><line x1="4" y1="12" x2="14" y2="12"/><circle cx="1.5" cy="4" r="1" fill="currentColor" stroke="none"/><circle cx="1.5" cy="8" r="1" fill="currentColor" stroke="none"/><circle cx="1.5" cy="12" r="1" fill="currentColor" stroke="none"/></svg>
        List
      </button>
    </div>''',
    '',
    'HTML – vtog-wrap removed from hero'
)

# ══════════════════════════════════════════════════════════════════════
# HTML-2: Remove id="mapView" from map section (no longer toggled)
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '<div id="mapView" class="map-section">',
    '<div class="map-section">',
    'HTML – id="mapView" removed from map section'
)

# ══════════════════════════════════════════════════════════════════════
# HTML-3: Wrap course grid in ALL COURSES section with eyebrow header
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''<!-- ── COURSE GRID ── -->
<div class="course-grid-wrap" id="courseGridWrap"></div>''',
    '''<!-- ── ALL COURSES ── -->
<section class="all-courses-section">
  <div class="ac-eyebrow">All Courses</div>
  <div class="ac-divider"></div>
  <div class="course-grid-wrap" id="courseGridWrap"></div>
</section>''',
    'HTML – ALL COURSES section wraps course grid'
)

# ══════════════════════════════════════════════════════════════════════
# JS-1: Remove activeView + setView() from state block
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''// ── MAP VIEW STATE (early – so toggle works before CDN finishes loading) ──
let activeView = 'map';
let mapInitialized = false;
let mapInstance = null;
let clusterGroup = null;
let courseMarkers = {};
let initialBounds = null;

function setView(view) {
  activeView = view;
  document.body.classList.toggle('view-map',  view === 'map');
  document.body.classList.toggle('view-list', view === 'list');
  const vMap  = document.getElementById('vtogMap');
  const vList = document.getElementById('vtogList');
  if (vMap)  { vMap.classList.toggle('active',  view === 'map');  vMap.setAttribute('aria-pressed',  String(view === 'map')); }
  if (vList) { vList.classList.toggle('active', view === 'list'); vList.setAttribute('aria-pressed', String(view === 'list')); }
  const mapView  = document.getElementById('mapView');
  const gridWrap = document.getElementById('courseGridWrap');
  if (mapView)  mapView.style.display  = view === 'map'  ? 'block' : 'none';
  if (gridWrap) gridWrap.style.display = view === 'list' ? 'block' : 'none';
  if (view === 'map') {
    if (typeof initMap === 'function' && !mapInitialized) initMap();
    else if (typeof filterMap === 'function' && mapInitialized) filterMap(activeDest);
  }
}''',
    '''// ── MAP STATE ──────────────────────────────────────────────────────────
let mapInitialized = false;
let mapInstance = null;
let clusterGroup = null;
let courseMarkers = {};
let initialBounds = null;''',
    'JS – activeView + setView() removed'
)

# ══════════════════════════════════════════════════════════════════════
# JS-2: Update filter tab click handler — always update map + LB + grid
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''document.querySelectorAll('.ftab').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.ftab').forEach(b => b.classList.remove('on'));
    this.classList.add('on');
    activeDest = this.dataset.dest;
    if (activeView === 'map') filterMap(activeDest);
    else renderGrid();
  });
});''',
    '''document.querySelectorAll('.ftab').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.ftab').forEach(b => b.classList.remove('on'));
    this.classList.add('on');
    activeDest = this.dataset.dest;
    filterMap(activeDest);
    buildLeaderboard(activeDest);
    renderGrid();
  });
});''',
    'JS – filter tab handler updated to always sync map + LB + grid'
)

# ══════════════════════════════════════════════════════════════════════
# JS-3: buildLeaderboard — accept optional dest to filter leaderboard
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''function buildLeaderboard() {
  const top10 = COURSES
    .filter(function(c) { return c.cyntp_rating != null; })
    .sort(function(a, b) {
      return b.cyntp_rating - a.cyntp_rating || a.name.localeCompare(b.name);
    })
    .slice(0, 10);''',
    '''function buildLeaderboard(dest) {
  const pool = (!dest || dest === 'all')
    ? COURSES
    : COURSES.filter(function(c) { return c.dest === dest; });
  const top10 = pool
    .filter(function(c) { return c.cyntp_rating != null; })
    .sort(function(a, b) {
      return b.cyntp_rating - a.cyntp_rating || a.name.localeCompare(b.name);
    })
    .slice(0, 10);''',
    'JS – buildLeaderboard accepts optional dest param'
)

# ══════════════════════════════════════════════════════════════════════
# JS-4: INIT block — remove setView('map') call
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''loadData();
updateHeroStats();
buildLeaderboard();
renderGrid();
setView('map');''',
    '''loadData();
updateHeroStats();
buildLeaderboard();
renderGrid();''',
    'JS – setView(\'map\') removed from INIT block'
)

# ══════════════════════════════════════════════════════════════════════
# JS-5: Bottom of map script — replace setView('map') with initMap()
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''// kick off default MAP view
setView('map');''',
    '''// initialise map on page load
initMap();''',
    'JS – setView(\'map\') → initMap() at bottom of map script'
)

# ── Report ─────────────────────────────────────────────────────────────
if errors:
    print('\nFAILED:')
    for e in errors:
        print(' ', e)
    import sys; sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone – all replacements applied.')
