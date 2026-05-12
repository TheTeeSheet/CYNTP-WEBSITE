#!/usr/bin/env python3
"""Add footer band to cyntp-courses.html."""

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
# CSS-1: Add footer-band CSS before map pin cluster block
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '/* ── MAP PIN & CLUSTER ───────────────────────────────────────────────── */',
    '''/* ── FOOTER BAND ─────────────────────────────────────────────────────── */
.footer-band {
  background: var(--grass); padding: 60px 80px;
  display: flex; align-items: center; justify-content: space-between;
}
.fb-left h3 { font-family: var(--font-head); font-size: 36px; letter-spacing: 2px; color: #fff; }
.fb-left h3 em { font-family: var(--font-serif); font-style: italic; color: rgba(255,255,255,0.8); }
.fb-left p { margin-top: 8px; font-size: 14px; color: rgba(255,255,255,0.7); }
.fb-cta { background: #fff; color: var(--grass); font-size: 12px; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; padding: 16px 32px; border-radius: 8px; transition: opacity 0.2s; text-decoration: none; display: inline-block; }
.fb-cta:hover { opacity: 0.85; }

/* ── MAP PIN & CLUSTER ───────────────────────────────────────────────── */''',
    'footer-band CSS added'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-2: Add footer responsive rules inside 640px breakpoint
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '  .sort-label { display: none; }\n}',
    '''  .sort-label { display: none; }
  .footer-band { flex-direction: column; align-items: flex-start; gap: 28px; padding: 48px 20px; }
  .fb-left h3 { font-size: 26px; }
  .fb-cta { width: 100%; text-align: center; display: block; box-sizing: border-box; }
}''',
    'footer responsive rules inside 640px breakpoint'
)

# ══════════════════════════════════════════════════════════════════════
# HTML: Insert footer before the main <script> block
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '</div>\n\n<script>\n// ── DATA ──────────────────────────────────────────────────────────────',
    '''</div>

<!-- ── FOOTER ── -->
<div class="footer-band">
  <div class="fb-left">
    <h3>READY TO PLAN YOUR <em>Next Round?</em></h3>
    <p>Tell us where you want to play. We&#39;ll help you build the perfect trip.</p>
  </div>
  <a href="https://www.coursesyouneedtoplay.com/contact" rel="noopener noreferrer" class="fb-cta">Get In Touch &rarr;</a>
</div>

<script>
// ── DATA ──────────────────────────────────────────────────────────────''',
    'footer HTML inserted before main script'
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
