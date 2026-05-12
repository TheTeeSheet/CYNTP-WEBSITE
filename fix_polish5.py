#!/usr/bin/env python3
"""Five polish fixes for cyntp-courses.html."""

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
# FIX 1: Filter bar — dark theme
# ══════════════════════════════════════════════════════════════════════

# Filter bar container
replace_once(
    '''.filter-bar {
  background: var(--paper2);
  border-bottom: 1px solid var(--paper3);
  border-top: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center;
  height: 60px; position: sticky; top: 64px; z-index: 150;
  padding: 0;
  box-shadow: none;
}''',
    '''.filter-bar {
  background: #0d0d0d;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  border-top: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center;
  height: 60px; position: sticky; top: 64px; z-index: 150;
  padding: 0;
  box-shadow: none;
}''',
    'filter-bar background → dark'
)

# ftab default state
replace_once(
    '''  color: var(--muted); border-bottom: 2px solid transparent;
  transition: all 0.2s; white-space: nowrap;
}
.ftab.on { color: var(--ink); border-bottom-color: var(--grass); }
.ftab:hover { color: var(--ink); }''',
    '''  color: rgba(255,255,255,0.4); border-bottom: 2px solid transparent;
  transition: all 0.2s; white-space: nowrap;
}
.ftab.on { color: #d4a055; border-bottom-color: #d4a055; }
.ftab:hover { color: rgba(255,255,255,0.8); }''',
    'ftab colors → dark theme (gold active)'
)

# filter-right panel
replace_once(
    '.filter-right { display: flex; align-items: center; gap: 12px; padding: 0 24px 0 16px; border-left: 1px solid var(--paper3); background: var(--paper2); flex-shrink: 0; height: 100%; }',
    '.filter-right { display: flex; align-items: center; gap: 12px; padding: 0 24px 0 16px; border-left: 1px solid rgba(255,255,255,0.08); background: #0d0d0d; flex-shrink: 0; height: 100%; }',
    'filter-right background/border → dark'
)

# sort-label
replace_once(
    '.sort-label { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }',
    '.sort-label { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.35); }',
    'sort-label color → dark'
)

# sort-select
replace_once(
    '  background: transparent; border: 1px solid rgba(15,15,15,0.15);\n  border-radius: 8px; padding: 6px 12px; font-family: var(--font-body);\n  font-size: 12px; color: var(--ink); cursor: pointer; outline: none;\n}',
    '  background: transparent; border: 1px solid rgba(255,255,255,0.12);\n  border-radius: 8px; padding: 6px 12px; font-family: var(--font-body);\n  font-size: 12px; color: rgba(255,255,255,0.6); cursor: pointer; outline: none;\n}',
    'sort-select color/border → dark'
)

# course-count
replace_once(
    '.course-count { font-size: 12px; color: var(--muted); padding-left: 12px; border-left: 1px solid var(--paper3); }',
    '.course-count { font-size: 12px; color: rgba(255,255,255,0.35); padding-left: 12px; border-left: 1px solid rgba(255,255,255,0.08); }',
    'course-count color/border → dark'
)

# ══════════════════════════════════════════════════════════════════════
# FIX 2: Contain Leaflet stacking context so filter bar sits above map
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '.map-section { position: relative; background: var(--ink); padding: 16px 0; }',
    '.map-section { position: relative; background: var(--ink); padding: 16px 0; isolation: isolate; }',
    'map-section isolation: isolate (contains Leaflet z-indices)'
)

# ══════════════════════════════════════════════════════════════════════
# FIX 3a: Leaderboard HTML — new title and subtitle
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '      <div class="lb-title">CYNTP Top 10</div>\n      <p class="lb-subtitle">The 10 highest-rated courses we&#39;ve played, by us. Click any course to see it on the map.</p>',
    '      <div class="lb-title">Highest Rated</div>\n      <p class="lb-subtitle">Sorted by our rating. Click any course to see it on the map.</p>',
    'leaderboard title + subtitle updated'
)

# ══════════════════════════════════════════════════════════════════════
# FIX 3b: Remove .slice(0, 10) — show all filtered courses
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''  const top10 = pool
    .filter(function(c) { return c.cyntp_rating != null; })
    .sort(function(a, b) {
      return b.cyntp_rating - a.cyntp_rating || a.name.localeCompare(b.name);
    })
    .slice(0, 10);
  const list = document.getElementById('lbList');
  if (!list) return;
  list.innerHTML = top10.map(function(c, i) {''',
    '''  const sorted = pool
    .filter(function(c) { return c.cyntp_rating != null; })
    .sort(function(a, b) {
      return b.cyntp_rating - a.cyntp_rating || a.name.localeCompare(b.name);
    });
  const list = document.getElementById('lbList');
  if (!list) return;
  list.innerHTML = sorted.map(function(c, i) {''',
    'buildLeaderboard: remove .slice(0,10), rename top10→sorted'
)

# ══════════════════════════════════════════════════════════════════════
# FIX 4: Destination heading text — light on dark background
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '.dest-name { font-family: var(--font-head); font-size: 28px; letter-spacing: 2px; color: var(--ink); }',
    '.dest-name { font-family: var(--font-head); font-size: 28px; letter-spacing: 2px; color: #a8a39d; }',
    'dest-name color var(--ink) → #a8a39d'
)

replace_once(
    '.dest-count { font-size: 12px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; padding: 4px 12px; background: var(--paper3); border-radius: 4px; }',
    '.dest-count { font-size: 12px; color: rgba(255,255,255,0.35); letter-spacing: 2px; text-transform: uppercase; padding: 4px 12px; background: rgba(255,255,255,0.06); border-radius: 4px; }',
    'dest-count → dark theme'
)

replace_once(
    '.dest-line { flex: 1; height: 1px; background: var(--paper3); }',
    '.dest-line { flex: 1; height: 1px; background: rgba(255,255,255,0.08); }',
    'dest-line → dark theme'
)

# ══════════════════════════════════════════════════════════════════════
# FIX 5: Reduce map→ALL COURSES gap 64px → 32px
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '.all-courses-section { background: var(--ink); padding: 64px 80px 80px; }',
    '.all-courses-section { background: var(--ink); padding: 32px 80px 80px; }',
    'all-courses-section top padding 64px → 32px'
)

replace_once(
    '  .all-courses-section { padding: 48px 20px 60px; }',
    '  .all-courses-section { padding: 32px 20px 60px; }',
    'all-courses-section 960px top padding 48px → 32px'
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
