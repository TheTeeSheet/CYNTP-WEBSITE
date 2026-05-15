#!/usr/bin/env python3
"""Add greenFee tier field to every course, update tile + popup rendering."""

import re, sys

HTML_PATH = 'cyntp-courses.html'
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# ── Tier assignments (id → tier string) ───────────────────────────────
TIERS = {
    # ALABAMA
    1:  '$',   # Craft Farms $55-95
    2:  '$$',  # FarmLinks $80-140
    3:  '$',   # Hampton Cove $55-95
    4:  '$',   # Kiva Dunes $60-100
    5:  '$',   # Peninsula $60-110
    6:  '$$',  # Ross Bridge $75-130
    7:  '$',   # The Lakewood Club $65-110
    8:  '$',   # The Shoals Fighting Joe $65-110
    9:  '$',   # The Shoals Schoolmaster $65-110
    # ARIZONA
    10: '$$',  # Ak-Chin Southern Dunes $90-160
    11: '$',   # Arizona National $70-96
    12: '$$',  # Eagle Mountain $70-130
    13: '$$',  # Grayhawk Raptor $150-250
    14: '$',   # Paradise Valley CC $45-75
    15: '$$',  # Quintero $120-200
    16: '$$',  # Rancho Manana $70-130
    17: '$',   # SaddleBrooke Mountain View $45-80
    18: '$',   # SaddleBrooke Preserve $45-80
    19: '$$',  # Sewailo $70-160
    20: '$$',  # Sunridge Canyon $80-150
    21: '$',   # Talking Stick O'odham $65-120
    22: '$$',  # The Club at Starr Pass $80-160
    23: '$',   # Tubac $60-110
    24: '$$',  # Verrado Founder's $80-140
    25: '$$',  # We-Ko-Pa Cholla $110-180
    26: '$$',  # We-Ko-Pa Saguaro $130-200
    # CALIFORNIA
    27: '$$$',   # Aviara $175-300
    28: '$$',    # Classic Club $80-150
    29: '$$',    # Desert Willow Firecliff $95-165
    30: '$$',    # Desert Willow Mountain View $85-150
    31: '$',     # Escena $60-110
    32: '$$',    # Indian Wells Celebrity $70-130
    33: '$$$',   # Monarch Beach $185-370
    34: '$$',    # PGA West Pete Dye Mountain $150-260
    35: '$$$',   # PGA West Pete Dye Stadium $200-350
    36: '$$',    # Westin Rancho Mirage $70-130
    124: '$$$$', # Pelican Hill Ocean North $250-450
    125: '$$$$', # Pelican Hill Ocean South $250-450
    # DOMINICAN REPUBLIC
    37: '$$',    # Casa de Campo Dye Fore $150-250
    38: '$$$',   # Casa de Campo Teeth of the Dog $250-400
    39: '$$',    # La Cana $120-200
    40: '$$$',   # Puntacana Corales $200-350
    # FLORIDA
    41: '$',    # Forest Lake $40-70
    42: '$$',   # Grand Cypress Cypress $110-180
    43: '$$',   # Grand Cypress Links $120-200
    44: '$$',   # Hammock Beach Ocean $150-250
    45: '$$',   # Hammock Beach Conservatory $120-200
    46: '$',    # Miami Lakes $50-90
    47: '$$',   # Mission Resort El Campeon $80-140
    48: '$',    # Shingle Creek $60-100
    49: '$$',   # Trump Doral Silver Fox $80-140
    114: '$$$', # Trump Doral Blue Monster $200-350
    122: '$$',  # Turnberry Miller $120-200
    123: '$$',  # Turnberry Soffer $150-250
    126: '$',   # Eagle Creek $40-80
    # GEORGIA
    50: '$$',   # McLemore Highlands $120-200
    51: '$',    # McLemore The Keep $60-100
    # IDAHO
    52: '$$$',  # Coeur d'Alene $200-350
    # IRELAND
    53: '$$',   # Dooks $80-140
    54: '$$',   # Lahinch $150-250
    55: '$$$$', # Old Head $250-450
    56: '$$',   # Tralee $130-220
    57: '$$$',  # Trump Doonbeg $200-350
    58: '$$$',  # Waterville $150-280
    # KENTUCKY
    59: '$$',   # Olde Stone $80-140
    # MICHIGAN
    60: '$',    # Grand Traverse Spruce Run $50-90
    61: '$$',   # Grand Traverse The Bear $120-200
    62: '$$',   # Grand Traverse Wolverine $90-160
    # MISSISSIPPI
    63: '$',    # Mossy Oak $70-120
    64: '$$',   # Old Waverly $80-140
    65: '$',    # Tunica National $45-75
    # MISSOURI
    66: '$$',   # Big Cedar Mountain Top $75-125
    67: '$$',   # Big Cedar Top of Rock $100-175
    68: '$$',   # Buffalo Ridge Springs $120-200
    69: '$$',   # Ozarks National $150-250
    70: '$$$',  # Payne's Valley $195-295
    # SOUTH CAROLINA
    71: '$$',   # Caledonia $130-200
    72: '$',    # Golden Bear SC $45-80
    73: '$',    # Hilton Head National $60-100
    74: '$',    # Myrtle Beach National King's North $60-110
    75: '$',    # Old South $55-90
    76: '$$',   # Palmetto Dunes Jones $80-140
    77: '$',    # Pawleys Plantation $70-120
    78: '$',    # Sequoyah National $65-100
    79: '$$',   # True Blue $80-140
    115: '$',   # Barefoot Fazio $70-120
    117: '$$',  # TPC Myrtle Beach $80-140
    # TENNESSEE
    80: '$',    # Franklin Bridge $45-70
    81: '$',    # Harpeth Hills $30-50
    82: '$',    # Hermitage General's Retreat $45-75
    83: '$',    # Hermitage President's Reserve $55-85
    84: '$',    # Nashboro $35-60
    85: '$',    # Nashville National $50-80
    86: '$',    # Old Natchez CC $50-80
    87: '$$',   # Sweetens Cove $100-175
    88: '$',    # Course at Sewanee $40-70
    89: '$',    # TN Golf Trail Montgomery Bell $40-65
    90: '$',    # Two Rivers $25-45
    91: '$',    # Vanderbilt Legends North $60-95
    # TEXAS
    92: '$$',   # Lost Pines $80-140
    # UTAH
    93: '$$',   # Black Desert Resort $150-250
    94: '$',    # Mountain Dell Lake $35-60
    95: '$',    # Old Mill $25-45
    96: '$',    # Sky Mountain $45-80
    97: '$',    # Sleepy Ridge $40-70
    98: '$',    # Soldier Hollow Gold $55-90
    127: '$',   # Copper Rock $50-95
    128: '$',   # Coral Canyon $45-85
    129: '$$',  # Sand Hollow Championship $80-160
    # VIRGINIA
    99:  '$',   # Colonial Heritage $70-120
    100: '$$',  # Ford's Colony Blackheath $80-140
    101: '$$',  # Golden Horseshoe Gold $100-170
    102: '$$',  # Kingsmill Plantation $70-130
    103: '$$',  # Kingsmill River $100-180
    104: '$',   # Royal New Kent $60-100
    105: '$',   # Stonehouse $65-110
    106: '$',   # Club at Viniterra $70-120
    107: '$',   # Williamsburg National Jamestown $55-90
    # WASHINGTON
    108: '$$',  # Gamble Sands $120-200
    109: '$',   # Gamble Sands Scarecrow $40-60
    # WISCONSIN
    110: '$$',  # Erin Hills $95-145
    111: '$$',  # SentryWorld $85-140
    112: '$',   # Stevens Point CC $50-80
    113: '$',   # Club at Lac La Belle $60-100
    # NEVADA
    116: '$$',  # Bali Hai $100-175
    118: '$$',  # TPC Las Vegas $80-150
    119: '$$',  # Angel Park Mountain $75-130
    120: '$',   # Serket $40-80
    121: '$$',  # Reflection Bay $90-160
    130: '$$',  # Wolf Creek $80-175
    131: '$',   # Conestoga $50-100
    # ILLINOIS
    132: '$$',  # Cog Hill Dubsdread $85-165
    133: '$',   # Bolingbrook $55-100
    134: '$',   # Harborside Starboard $50-95
}

def add_green_fee(course_id, tier):
    global html
    anchor = f'id:{course_id},dest:'
    idx = html.find(anchor)
    if idx == -1:
        errors.append(f'NOT FOUND id:{course_id}')
        return
    chunk = html[idx: idx + 2000]
    # Find price:"..." and insert greenFee after it
    m = re.search(r'price:"[^"]*"', chunk)
    if not m:
        errors.append(f'price field NOT FOUND for id:{course_id}')
        return
    abs_end = idx + m.end()
    # Check greenFee not already added
    if html[abs_end:abs_end+10].startswith(',greenFee'):
        print(f'  SKIP id:{course_id} (greenFee already present)')
        return
    html = html[:abs_end] + f',greenFee:"{tier}"' + html[abs_end:]
    print(f'  id:{course_id:<4} → {tier}')

for cid, tier in sorted(TIERS.items()):
    add_green_fee(cid, tier)

# ── Update grid tile rendering: replace c.price with c.greenFee ────────
old_card_meta = '''          <div class="card-meta">
            <div class="card-price">${c.price}</div>
          </div>'''
new_card_meta = '''          <div class="card-meta">
            ${c.greenFee ? `<div class="card-price">${c.greenFee}</div>` : ''}
          </div>'''
if old_card_meta in html:
    html = html.replace(old_card_meta, new_card_meta, 1)
    print('  OK: grid tile card-price → greenFee')
else:
    errors.append('NOT FOUND: grid tile card-price block')

# ── Add .mpc-fee CSS after .mpc-rating ────────────────────────────────
old_mpc_css = '.mpc-rating { font-size: 13px; color: #d4a055; font-weight: 700; margin-bottom: 12px; }'
new_mpc_css = '''.mpc-rating { font-size: 13px; color: #d4a055; font-weight: 700; margin-bottom: 4px; }
.mpc-fee { font-size: 12px; color: #2d6a3f; font-weight: 700; margin-bottom: 10px; }'''
if old_mpc_css in html:
    html = html.replace(old_mpc_css, new_mpc_css, 1)
    print('  OK: .mpc-fee CSS added')
else:
    errors.append('NOT FOUND: .mpc-rating CSS')

# ── Update map popup to show greenFee ─────────────────────────────────
old_popup = ("        (stars ? '<div class=\"mpc-rating\">' + stars + '</div>' : '') +\n"
             "        '<button class=\"mpc-view-btn\" onclick=\"openCourse(' + course.id + ')\">VIEW COURSE &#8594;</button>' +")
new_popup = ("        (stars ? '<div class=\"mpc-rating\">' + stars + '</div>' : '') +\n"
             "        (course.greenFee ? '<div class=\"mpc-fee\">' + course.greenFee + '</div>' : '') +\n"
             "        '<button class=\"mpc-view-btn\" onclick=\"openCourse(' + course.id + ')\">VIEW COURSE &#8594;</button>' +")
if old_popup in html:
    html = html.replace(old_popup, new_popup, 1)
    print('  OK: map popup greenFee line added')
else:
    errors.append('NOT FOUND: map popup stars block')

# ── Report ─────────────────────────────────────────────────────────────
if errors:
    print('\nFAILED:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone — {len(TIERS)} greenFee fields added, rendering updated.')
