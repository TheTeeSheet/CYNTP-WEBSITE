#!/usr/bin/env python3
"""Replace green footer-band with home page multi-column footer on cyntp-courses.html."""

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
# CSS-1: Replace footer-band block with home-page footer CSS
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''/* ── FOOTER BAND ─────────────────────────────────────────────────────── */
.footer-band {
  background: var(--grass); padding: 60px 80px;
  display: flex; align-items: center; justify-content: space-between;
}
.fb-left h3 { font-family: var(--font-head); font-size: 36px; letter-spacing: 2px; color: #fff; }
.fb-left h3 em { font-family: var(--font-serif); font-style: italic; color: rgba(255,255,255,0.8); }
.fb-left p { margin-top: 8px; font-size: 14px; color: rgba(255,255,255,0.7); }
.fb-cta { background: #fff; color: var(--grass); font-size: 12px; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; padding: 16px 32px; border-radius: 8px; transition: opacity 0.2s; text-decoration: none; display: inline-block; }
.fb-cta:hover { opacity: 0.85; }''',
    '''/* ── FOOTER ─────────────────────────────────────────────────────────── */
footer { background: #111; }
.footer-main { padding: 72px 80px 60px; display: grid; grid-template-columns: 1.6fr 1fr 1fr 1fr; gap: 48px; }
.footer-brand-name { font-family: var(--font-head); font-size: 28px; letter-spacing: 4px; color: #fff; margin-bottom: 20px; }
.footer-brand-desc { font-size: 13px; color: rgba(255,255,255,0.35); line-height: 1.8; max-width: 260px; }
.footer-col-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--sun); font-weight: 700; margin-bottom: 20px; }
.footer-links { display: flex; flex-direction: column; gap: 12px; }
.footer-links a { font-size: 14px; color: rgba(255,255,255,0.55); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: #fff; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.06); padding: 20px 80px; display: flex; align-items: center; justify-content: space-between; }
.footer-bottom span { font-size: 12px; color: rgba(255,255,255,0.2); }
.footer-bottom strong { color: rgba(255,255,255,0.55); font-weight: 700; }''',
    'footer-band CSS → home-page footer CSS'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-2: Add footer responsive rules to 960px breakpoint
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '  .map-inner { margin: 0 20px; }\n}',
    '  .map-inner { margin: 0 20px; }\n  .footer-main { padding: 60px 40px 48px; }\n  .footer-bottom { padding: 20px 40px; }\n}',
    '960px – footer responsive rules added'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-3: Replace footer-band responsive rules in 640px breakpoint
#        with home-page footer responsive rules
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '  .footer-band { flex-direction: column; align-items: flex-start; gap: 28px; padding: 48px 20px; }\n  .fb-left h3 { font-size: 26px; }\n  .fb-cta { width: 100%; text-align: center; display: block; box-sizing: border-box; }',
    '  .footer-main { grid-template-columns: 1fr 1fr; gap: 40px; padding: 40px 24px 32px; }\n  .footer-bottom { padding: 18px 24px; flex-direction: column; gap: 8px; text-align: center; }',
    '640px – footer-band rules → home-page footer rules'
)

# ══════════════════════════════════════════════════════════════════════
# CSS-4: Add 480px breakpoint for single-column footer
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '\n\n\nnav .active { color: var(--sun) !important; }',
    '\n\n@media (max-width: 480px) {\n  .footer-main { grid-template-columns: 1fr; }\n}\n\nnav .active { color: var(--sun) !important; }',
    '480px breakpoint for single-column footer'
)

# ══════════════════════════════════════════════════════════════════════
# HTML: Replace footer-band div with home-page <footer> element
# ══════════════════════════════════════════════════════════════════════
replace_once(
    '''<!-- ── FOOTER ── -->
<div class="footer-band">
  <div class="fb-left">
    <h3>READY TO PLAN YOUR <em>Next Round?</em></h3>
    <p>Tell us where you want to play. We&#39;ll help you build the perfect trip.</p>
  </div>
  <a href="https://www.coursesyouneedtoplay.com/contact" rel="noopener noreferrer" class="fb-cta">Get In Touch &rarr;</a>
</div>''',
    '''<!-- ── FOOTER ── -->
<footer>
  <div class="footer-main">
    <div>
      <div class="footer-brand-name">CYNTP</div>
      <p class="footer-brand-desc">Honest golf course reviews and trip guides for everyday golfers. We play it, we rate it, we tell you the truth.</p>
    </div>
    <div>
      <div class="footer-col-label">Explore</div>
      <div class="footer-links">
        <a href="cyntp-trips.html">Golf Trips</a>
        <a href="cyntp-turn.html">Insider Guide</a>
        <a href="cyntp-about.html">About Us</a>
        <a href="cyntp-partner.html">Partner</a>
      </div>
    </div>
    <div>
      <div class="footer-col-label">Destinations</div>
      <div class="footer-links">
        <a href="cyntp-trips.html">Scottsdale</a>
        <a href="cyntp-trips.html">Hilton Head</a>
        <a href="cyntp-trips.html">Myrtle Beach</a>
        <a href="cyntp-trips.html">Las Vegas</a>
        <a href="cyntp-trips.html">Palm Springs</a>
      </div>
    </div>
    <div>
      <div class="footer-col-label">Connect</div>
      <div class="footer-links">
        <a href="https://www.instagram.com/coursesyouneedtoplay" rel="noopener noreferrer" target="_blank">Instagram</a>
        <a href="https://www.tiktok.com/@coursesyouneedtoplay" rel="noopener noreferrer" target="_blank">TikTok</a>
        <a href="https://www.youtube.com/@coursesyouneedtoplay" rel="noopener noreferrer" target="_blank">YouTube</a>
        <a href="/cdn-cgi/l/email-protection#c9b9a8bbbda7acbbba89aaa6bcbbbaacbab0a6bca7acacadbda6b9a5a8b0e7aaa6a4">Email Us</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 Sharp Golf LLC. All Rights Reserved.</span>
    <span>Built for golfers who play hard and <strong>plan smarter.</strong></span>
  </div>
</footer>''',
    'footer HTML → home-page footer element'
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
