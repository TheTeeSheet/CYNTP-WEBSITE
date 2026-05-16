#!/usr/bin/env python3
"""Remove Course Overview: strip review: data fields and panel section."""

import re, sys

HTML_PATH = 'cyntp-courses.html'
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# ── 1. Remove all review:"..." lines from course data ─────────────────
before = html.count('\n    review:')
html = re.sub(r'\n    review:"[^"]*",?', '', html)
after = html.count('\n    review:')
removed = before - after
print(f'  Removed {removed} review: data fields')
if after > 0:
    errors.append(f'{after} review: fields still present after removal')

# ── 2. Remove Course Overview section from panel rendering ─────────────
old_panel = (
    '\n\n      <div class="section-label">Course Overview</div>\n'
    '      <div class="review-text">${course.review}</div>'
)
if old_panel in html:
    html = html.replace(old_panel, '', 1)
    print('  Removed Course Overview panel section')
else:
    errors.append('NOT FOUND: Course Overview panel section')

# ── 3. Remove now-unused CSS (.section-label, .review-text) ───────────
old_css = (
    '.section-label { font-size: 11px; letter-spacing: 3px; text-transform: uppercase;'
    ' font-weight: 600; color: var(--grass); margin-bottom: 12px; display: flex;'
    ' align-items: center; gap: 8px; }\n'
    '.section-label::before { content: \'\'; width: 16px; height: 2px;'
    ' background: var(--grass); border-radius: 2px; }\n'
    '.review-text { font-size: 15px; color: var(--muted); line-height: 1.85; margin-bottom: 28px; }'
)
if old_css in html:
    html = html.replace(old_css, '', 1)
    print('  Removed unused .section-label / .review-text CSS')
else:
    errors.append('NOT FOUND: .section-label/.review-text CSS block')

# ── Report ─────────────────────────────────────────────────────────────
if errors:
    print('\nFAILED:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone.')
