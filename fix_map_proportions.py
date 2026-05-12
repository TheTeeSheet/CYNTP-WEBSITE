#!/usr/bin/env python3
"""Resize map/leaderboard proportions and increase lb-row breathing room."""

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

# ── 1. Map column: flex: 1 → flex: 3 (60%) ────────────────────────────
replace_once(
    '.map-col {\n  flex: 1; position: relative; border-radius: 14px; overflow: hidden;\n}',
    '.map-col {\n  flex: 3; position: relative; border-radius: 14px; overflow: hidden;\n}',
    'map-col flex: 1 → flex: 3'
)

# ── 2. Leaderboard panel: fixed 360px → flex: 2 (40%) ─────────────────
replace_once(
    '  width: 360px; max-width: 360px; flex-shrink: 0;',
    '  flex: 2; min-width: 0;',
    'lb-panel fixed width → flex: 2'
)

# ── 3. Row padding: 10px → 16px ───────────────────────────────────────
replace_once(
    '  padding: 10px 0;\n  border-bottom: 1px solid rgba(244,240,232,0.05);',
    '  padding: 16px 0;\n  border-bottom: 1px solid rgba(244,240,232,0.05);',
    'lb-row padding 10px → 16px'
)

# ── 4. Dest label gap: margin-bottom 2px → 4px ────────────────────────
replace_once(
    '.lb-dest { font-size: 11px; color: #a8a39d; margin-bottom: 2px; }',
    '.lb-dest { font-size: 11px; color: #a8a39d; margin-bottom: 4px; }',
    'lb-dest margin-bottom 2px → 4px'
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
