#!/usr/bin/env python3
"""Add CYNTP ratings to 24 courses and rename Barefoot Love → Fazio."""

HTML_PATH = 'cyntp-courses.html'
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

results = []
errors  = []

def set_rating(course_id, rating, label):
    """Find course by id, replace cyntp_rating:null with the given value."""
    global html
    anchor = f'id:{course_id},dest:'
    idx = html.find(anchor)
    if idx == -1:
        errors.append(f'NOT FOUND id:{course_id} ({label})')
        return
    chunk = html[idx: idx + 2000]
    old_tok = 'cyntp_rating:null,'
    pos = chunk.find(old_tok)
    if pos == -1:
        errors.append(f'cyntp_rating:null NOT FOUND for id:{course_id} ({label})')
        return
    abs_pos = idx + pos
    html = html[:abs_pos] + f'cyntp_rating:{rating},' + html[abs_pos + len(old_tok):]
    results.append(f'  id:{course_id:<4}  null → {rating}   ({label})')

def rename_course(old_name, new_name, label):
    global html
    if old_name not in html:
        errors.append(f'NOT FOUND name: {label}')
        return
    html = html.replace(old_name, new_name, 1)
    results.append(f'  RENAMED: {label}')

# ── ARIZONA ───────────────────────────────────────────────────────────
set_rating(17,  7.4, 'SaddleBrooke — Mountain View')
set_rating(18,  7.5, 'SaddleBrooke — The Preserve')

# ── CALIFORNIA ────────────────────────────────────────────────────────
set_rating(33,  8.1, 'Monarch Beach Golf Links')
set_rating(124, 8.6, 'Pelican Hill — Ocean North')
set_rating(125, 8.5, 'Pelican Hill — Ocean South')

# ── FLORIDA ───────────────────────────────────────────────────────────
set_rating(126, 6.4, 'Eagle Creek Golf Club')
set_rating(45,  6.9, 'Hammock Beach — Conservatory Course')
set_rating(114, 8.3, 'Trump National Doral — Blue Monster')
set_rating(122, 7.7, 'Turnberry Isle — Miller Course')
set_rating(123, 7.8, 'Turnberry Isle — Soffer Course')

# ── ILLINOIS ──────────────────────────────────────────────────────────
set_rating(132, 8.7, 'Cog Hill — Dubsdread')
set_rating(133, 8.2, 'Bolingbrook Golf Club')
set_rating(134, 7.4, 'Harborside International — Starboard')

# ── MISSOURI ──────────────────────────────────────────────────────────
set_rating(66,  8.3, 'Big Cedar Lodge — Mountain Top')
set_rating(67,  8.5, 'Big Cedar Lodge — Top of the Rock')

# ── SOUTH CAROLINA ────────────────────────────────────────────────────
rename_course(
    'name:"Barefoot Resort &mdash; Love Course"',
    'name:"Barefoot Resort &mdash; Fazio Course"',
    'Barefoot Love → Fazio'
)
set_rating(115, 7.4, 'Barefoot Resort — Fazio Course')
set_rating(117, 7.4, 'TPC Myrtle Beach')

# ── TENNESSEE ─────────────────────────────────────────────────────────
set_rating(87,  8.2, 'Sweetens Cove Golf Club')

# ── UTAH ──────────────────────────────────────────────────────────────
set_rating(127, 8.2, 'Copper Rock Golf Course')
set_rating(128, 8.0, 'Coral Canyon Golf Course')
set_rating(129, 9.0, 'Sand Hollow — Championship Course')

# ── NEVADA ────────────────────────────────────────────────────────────
set_rating(119, 7.6, 'Angel Park — Mountain Course')
set_rating(116, 6.3, 'Bali Hai Golf Club')
# Conestoga (131) — left as-is per instructions
set_rating(121, 8.3, 'Reflection Bay Golf Club')
set_rating(120, 7.5, 'Serket Golf Club')
set_rating(118, 7.6, 'TPC Las Vegas')
# Wolf Creek (130) — left as-is per instructions

# ── Report ────────────────────────────────────────────────────────────
print('Applied:')
for r in results:
    print(r)

if errors:
    print('\nFAILED:')
    for e in errors:
        print(' ', e)
    import sys; sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone — {len(results)} changes applied.')
