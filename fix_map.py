#!/usr/bin/env python3
"""
Fix 1: Move the raw map JS (currently outside <script>) into a proper
        <script> block placed AFTER the Leaflet CDN loads.
Fix 2: Hide filter bar / sort / count in MAP view via body class + CSS.
"""
import re, sys

HTML_PATH = 'cyntp-courses.html'
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ── Guard ──────────────────────────────────────────────────────────────
if 'fix_map_applied' in html:
    print('Already applied.'); sys.exit(0)

# ══════════════════════════════════════════════════════════════════════
# 1. Remove setView('map'); from the main (early) script block
# ══════════════════════════════════════════════════════════════════════
# This call happens before Leaflet loads — must be removed from here.
html = html.replace("setView('map');\n", '', 1)

# ══════════════════════════════════════════════════════════════════════
# 2. Extract the raw map JS (currently floating outside <script> tags)
#    It starts right after the main </script> and ends before Leaflet CDN.
# ══════════════════════════════════════════════════════════════════════
MAIN_SCRIPT_END  = '</script>\n\n\n// ── MAP COORDS'
CDN_LEAFLET      = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

start_marker = MAIN_SCRIPT_END.replace('\n\n\n// ── MAP COORDS', '')  # == '</script>'
# Find the boundary: after the main </script> we have raw JS up to CDN
# The raw block starts with newlines + '// ── MAP COORDS'
raw_js_start = html.find(CDN_LEAFLET)
# Everything between first occurrence of '</script>\n\n' and CDN_LEAFLET
# that is NOT inside a script tag is our raw JS.

# More precise: find the raw JS block
raw_start_token = '</script>\n\n\n// ── MAP COORDS'
if raw_start_token not in html:
    raw_start_token = '</script>\n\n// ── MAP COORDS'
if raw_start_token not in html:
    # Try to find it with any newlines between </script> and // ── MAP
    m = re.search(r'</script>\s*(// ── MAP COORDS)', html)
    if m:
        raw_start_token = html[m.start():m.start()+len('</script>')]
        raw_js_start_idx = m.start(1)
    else:
        print('ERROR: could not find raw JS start. Aborting.'); sys.exit(1)
else:
    raw_js_start_idx = html.index(raw_start_token) + len('</script>') + html[html.index(raw_start_token)+len('</script>'):].index('// ── MAP COORDS')

cdn_idx = html.index(CDN_LEAFLET)
raw_map_js = html[raw_js_start_idx:cdn_idx].strip()

# Remove the raw JS from between </script> and the CDN scripts
# Replace from after the main </script> up to (not including) the CDN line
main_script_close_idx = html.rindex('</script>', 0, cdn_idx)
# Everything between that </script> and CDN_LEAFLET is the raw JS + whitespace
between = html[main_script_close_idx + len('</script>'):cdn_idx]
html = html[:main_script_close_idx + len('</script>')] + '\n\n' + html[cdn_idx:]

# ══════════════════════════════════════════════════════════════════════
# 3. Patch setView() in raw_map_js to also toggle body classes (Issue 2)
# ══════════════════════════════════════════════════════════════════════
OLD_SETVIEW_BODY = """\
  document.getElementById('vtogMap').classList.toggle('active', view === 'map');
  document.getElementById('vtogList').classList.toggle('active', view === 'list');
  document.getElementById('vtogMap').setAttribute('aria-pressed', String(view === 'map'));
  document.getElementById('vtogList').setAttribute('aria-pressed', String(view === 'list'));"""

NEW_SETVIEW_BODY = """\
  document.body.classList.toggle('view-map',  view === 'map');
  document.body.classList.toggle('view-list', view === 'list');
  document.getElementById('vtogMap').classList.toggle('active', view === 'map');
  document.getElementById('vtogList').classList.toggle('active', view === 'list');
  document.getElementById('vtogMap').setAttribute('aria-pressed', String(view === 'map'));
  document.getElementById('vtogList').setAttribute('aria-pressed', String(view === 'list'));"""

raw_map_js = raw_map_js.replace(OLD_SETVIEW_BODY, NEW_SETVIEW_BODY, 1)

# ══════════════════════════════════════════════════════════════════════
# 4. Insert the map JS as a proper <script> block AFTER the CDN scripts,
#    with setView('map') at the end to kick off the default view.
# ══════════════════════════════════════════════════════════════════════
EMAIL_SCRIPT = '<script src="/email-capture.js"></script>'
NEW_BLOCK = (
    CDN_LEAFLET + '\n' +
    '<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>\n' +
    '<script>\n' +
    raw_map_js + "\n\n// kick off default MAP view\nsetView('map');\n" +
    '</script>\n' +
    EMAIL_SCRIPT
)

# The CDN line is now in html, followed by the markercluster line + email-capture
# Find the pattern we need to replace
OLD_CDN_BLOCK = (
    CDN_LEAFLET + '\n' +
    '<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>\n' +
    EMAIL_SCRIPT
)
if OLD_CDN_BLOCK in html:
    html = html.replace(OLD_CDN_BLOCK, NEW_BLOCK, 1)
else:
    # Try alternate order
    OLD_CDN_BLOCK2 = CDN_LEAFLET + '\n<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>'
    if OLD_CDN_BLOCK2 in html:
        html = html.replace(OLD_CDN_BLOCK2,
            CDN_LEAFLET + '\n<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>\n<script>\n' + raw_map_js + "\n\nsetView('map');\n</script>",
            1)
    else:
        print('ERROR: CDN block not found. Dumping nearby context:')
        idx = html.index(CDN_LEAFLET)
        print(repr(html[idx:idx+200]))
        sys.exit(1)

# ══════════════════════════════════════════════════════════════════════
# 5. Add CSS for Issue 2 — hide filter bar in map view
# ══════════════════════════════════════════════════════════════════════
FILTER_HIDE_CSS = """
/* ── Hide list-only controls in MAP view ────────────────────────────── */
body.view-map .filter-bar { display: none !important; }
"""
# Insert before the last </style>
html = html.replace('</style>', FILTER_HIDE_CSS + '</style>', 1)

# ══════════════════════════════════════════════════════════════════════
# 6. Guard marker
# ══════════════════════════════════════════════════════════════════════
html = html.replace('<body>', '<body><!-- fix_map_applied -->', 1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done.')
