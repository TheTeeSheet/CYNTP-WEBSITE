#!/usr/bin/env python3
"""
Injects the interactive course map into cyntp-courses.html.
Run once; idempotent checks prevent double-injection.
"""
import re, sys

HTML_PATH = 'cyntp-courses.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ── Guard: abort if already injected ──────────────────────────────────
if 'COORDS =' in html:
    print('Already injected — aborting.'); sys.exit(0)

# ══════════════════════════════════════════════════════════════════════
# 1. CDN LINKS  (before </head>)
# ══════════════════════════════════════════════════════════════════════
CDN = """\
  <!-- Leaflet -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
"""
html = html.replace('</head>', CDN + '</head>', 1)

# ══════════════════════════════════════════════════════════════════════
# 2. CSS  (before </style>)
# ══════════════════════════════════════════════════════════════════════
MAP_CSS = """

/* ── VIEW TOGGLE ─────────────────────────────────────────────────────── */
.view-toggle-bar {
  background: var(--paper); border-bottom: 1px solid var(--paper3);
  padding: 14px 80px; display: flex; align-items: center;
}
.vtog-wrap {
  display: flex; background: var(--paper2); border-radius: 8px; padding: 3px; gap: 2px;
}
.vtog-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 20px; border: none; border-radius: 5px;
  font-family: var(--font-body); font-size: 11px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--muted); background: transparent;
  cursor: pointer; transition: all 0.2s; min-height: 44px;
}
.vtog-btn.active { background: var(--ink); color: #fff; }
.vtog-btn svg { width: 14px; height: 14px; flex-shrink: 0; }

/* ── MAP SECTION ─────────────────────────────────────────────────────── */
.map-section { position: relative; }
#courseMap {
  height: 520px; width: 100%;
  background: #0d0d0d;
  border-top: 1px solid rgba(212,160,85,0.18);
  border-bottom: 1px solid rgba(212,160,85,0.18);
}
.map-reset-btn {
  position: absolute; top: 16px; right: 16px; z-index: 1000;
  background: rgba(13,13,13,0.88); border: 1px solid var(--sun);
  color: var(--sun); border-radius: 6px; padding: 8px 14px;
  font-family: var(--font-body); font-size: 10px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  display: flex; align-items: center; gap: 6px; cursor: pointer;
  transition: all 0.2s; backdrop-filter: blur(8px);
}
.map-reset-btn:hover:not(:disabled) { background: rgba(212,160,85,0.14); }
.map-reset-btn:disabled { opacity: 0.35; pointer-events: none; }

/* ── MAP PIN & CLUSTER ───────────────────────────────────────────────── */
.map-pin {
  width: 14px; height: 14px; border-radius: 50%;
  background: #d4a055; border: 2px solid #0d0d0d;
  box-shadow: 0 2px 8px rgba(0,0,0,0.45);
  transition: transform 0.15s;
  cursor: pointer;
}
.leaflet-marker-icon:hover .map-pin { transform: scale(1.4); }
.map-cluster {
  border-radius: 50%; background: #d4a055;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-body); font-weight: 800; color: #0d0d0d;
  box-shadow: 0 3px 14px rgba(0,0,0,0.45);
  border: 2px solid #0d0d0d; cursor: pointer;
}

/* Override Leaflet's default cluster styles */
.marker-cluster-small, .marker-cluster-medium, .marker-cluster-large { background: transparent !important; }
.marker-cluster-small div, .marker-cluster-medium div, .marker-cluster-large div { background: transparent !important; }

/* ── MAP PREVIEW FLOATING CARD ───────────────────────────────────────── */
.map-preview-float {
  position: fixed; z-index: 9001; pointer-events: auto;
  display: none;
  transform: translate(-50%, calc(-100% - 18px));
}
.mpc-inner {
  background: #1c1c1c; border: 1px solid rgba(212,160,85,0.3);
  border-radius: 10px; padding: 16px 18px; min-width: 220px; max-width: 270px;
  box-shadow: 0 14px 48px rgba(0,0,0,0.65);
}
.mpc-name {
  font-family: var(--font-head); font-size: 15px; letter-spacing: 0.5px;
  color: #fff; line-height: 1.15; margin-bottom: 5px;
}
.mpc-location {
  font-size: 10px; color: rgba(255,255,255,0.4);
  letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px;
}
.mpc-rating { font-size: 13px; color: #d4a055; font-weight: 700; margin-bottom: 12px; }
.mpc-view-btn, .mpc-zoom-btn {
  display: block; width: 100%; padding: 9px; text-align: center;
  border: 1px solid rgba(212,160,85,0.45); border-radius: 6px;
  color: #d4a055; font-family: var(--font-body);
  font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
  background: transparent; cursor: pointer; transition: all 0.2s;
}
.mpc-view-btn:hover, .mpc-zoom-btn:hover { background: rgba(212,160,85,0.12); }
.mpc-cluster-header {
  font-size: 10px; color: #d4a055; letter-spacing: 2px;
  text-transform: uppercase; font-weight: 700; margin-bottom: 10px;
}
.mpc-dest-list { display: flex; flex-direction: column; gap: 6px; margin-bottom: 8px; }
.mpc-dest-item {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 13px; color: rgba(255,255,255,0.8);
}
.mpc-dest-count { color: #d4a055; font-weight: 700; font-size: 12px; }
.mpc-cluster-more { font-size: 11px; color: rgba(255,255,255,0.3); margin-bottom: 12px; font-style: italic; }

/* ── MAP STATS FOOTER ────────────────────────────────────────────────── */
.map-stats-footer {
  background: var(--ink); padding: 14px 80px;
  display: flex; align-items: center; gap: 14px;
  font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
  color: rgba(255,255,255,0.3);
}
.map-stats-footer strong {
  color: #d4a055; font-family: var(--font-head); font-size: 15px; letter-spacing: 1px;
}
.msd-dot { color: rgba(255,255,255,0.15); }

/* ── LEAFLET CONTROL OVERRIDES ───────────────────────────────────────── */
.leaflet-control-zoom {
  border: 1px solid rgba(212,160,85,0.3) !important;
  border-radius: 8px !important; overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.4) !important;
}
.leaflet-control-zoom a {
  background: rgba(13,13,13,0.92) !important;
  color: #d4a055 !important;
  border-color: rgba(212,160,85,0.2) !important;
  width: 32px !important; height: 32px !important; line-height: 32px !important;
  font-size: 18px !important;
}
.leaflet-control-zoom a:hover { background: rgba(212,160,85,0.14) !important; }
.leaflet-control-attribution { display: none !important; }
.leaflet-tile-pane { filter: brightness(0.92); }

/* ── RESPONSIVE ──────────────────────────────────────────────────────── */
@media (max-width: 960px) {
  .view-toggle-bar { padding: 12px 20px; }
  .map-stats-footer { padding: 12px 20px; }
}
@media (max-width: 768px) {
  #courseMap { height: 400px; }
}
"""
# Insert before the last </style> in the <head> (the main style block)
html = html.replace('</style>', MAP_CSS + '</style>', 1)

# ══════════════════════════════════════════════════════════════════════
# 3. HTML  (view toggle + map section, before the course grid div)
# ══════════════════════════════════════════════════════════════════════
MAP_HTML = """\

<!-- ── VIEW TOGGLE ── -->
<div class="view-toggle-bar">
  <div class="vtog-wrap" role="group" aria-label="View mode">
    <button class="vtog-btn active" id="vtogMap" aria-pressed="true" onclick="setView('map')">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M10 2l4 2v10l-4-2-4 2-4-2V2l4 2 4-2z"/><path d="M6 4v10M10 2v10"/></svg>
      Map
    </button>
    <button class="vtog-btn" id="vtogList" aria-pressed="false" onclick="setView('list')">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><line x1="4" y1="4" x2="14" y2="4"/><line x1="4" y1="8" x2="14" y2="8"/><line x1="4" y1="12" x2="14" y2="12"/><circle cx="1.5" cy="4" r="1" fill="currentColor" stroke="none"/><circle cx="1.5" cy="8" r="1" fill="currentColor" stroke="none"/><circle cx="1.5" cy="12" r="1" fill="currentColor" stroke="none"/></svg>
      List
    </button>
  </div>
</div>

<!-- ── MAP VIEW ── -->
<div id="mapView" class="map-section">
  <div id="courseMap" role="application" aria-label="Interactive map of all the courses we've played"></div>
  <button class="map-reset-btn" id="mapResetBtn" aria-label="Reset map view to show all courses" onclick="resetMapView()" disabled>
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><polyline points="1,5 5,1 5,3.5 11,3.5 11,6.5 5,6.5 5,9"/></svg>
    Reset View
  </button>
  <div class="map-stats-footer" id="mapStatsFooter"></div>
</div>

"""

GRID_ANCHOR = '<!-- ── COURSE GRID ── -->'
if GRID_ANCHOR not in html:
    GRID_ANCHOR = '<div class="course-grid-wrap" id="courseGridWrap">'
    html = html.replace(GRID_ANCHOR, MAP_HTML + GRID_ANCHOR, 1)
else:
    html = html.replace(GRID_ANCHOR, MAP_HTML + GRID_ANCHOR, 1)

# ══════════════════════════════════════════════════════════════════════
# 4. JS  (before closing </script> of the main script block)
# ══════════════════════════════════════════════════════════════════════
MAP_JS = """

// ── MAP COORDS (id → [lat, lng]) ──────────────────────────────────────
const COORDS = {
  1:  [30.256, -87.713],   2:  [33.174, -86.252],   3:  [34.669, -86.430],
  4:  [30.259, -87.740],   5:  [30.274, -87.808],   6:  [33.406, -86.918],
  7:  [30.476, -87.913],   8:  [34.744, -87.719],   9:  [34.745, -87.720],
  10: [33.059, -112.048],  11: [32.214, -110.812],  12: [33.601, -111.746],
  13: [33.683, -111.907],  14: [33.537, -111.942],  15: [33.874, -112.538],
  16: [33.834, -111.953],  17: [32.553, -110.878],  18: [32.554, -110.880],
  19: [32.277, -110.908],  20: [33.599, -111.722],  21: [33.576, -111.898],
  22: [32.220, -111.023],  23: [31.688, -111.047],  24: [33.499, -112.566],
  25: [33.673, -111.655],  26: [33.675, -111.657],  27: [33.124, -117.301],
  28: [33.765, -116.399],  29: [33.762, -116.377],  30: [33.760, -116.375],
  31: [33.860, -116.504],  32: [33.723, -116.350],  33: [33.477, -117.698],
  34: [33.643, -116.317],  35: [33.640, -116.319],  36: [33.740, -116.454],
  37: [18.420, -68.965],   38: [18.419, -68.970],   39: [18.577, -68.365],
  40: [18.560, -68.401],   41: [28.568, -81.541],   42: [28.393, -81.559],
  43: [28.395, -81.560],   44: [29.566, -81.209],   45: [29.565, -81.210],
  46: [25.905, -80.302],   47: [28.709, -81.773],   48: [28.439, -81.462],
  49: [25.830, -80.329],   50: [34.783, -85.423],   51: [34.784, -85.425],
  52: [47.671, -116.782],  53: [52.000, -9.822],    54: [52.930, -9.350],
  55: [51.594, -8.521],    56: [52.288, -9.898],    57: [52.735, -9.520],
  58: [51.830, -10.154],   59: [36.988, -86.454],   60: [44.763, -85.376],
  61: [44.787, -85.351],   62: [44.789, -85.353],   63: [33.609, -88.654],
  64: [33.581, -88.671],   65: [34.718, -90.301],   66: [36.543, -93.330],
  67: [36.537, -93.316],   68: [36.538, -93.322],   69: [36.562, -93.343],
  70: [36.551, -93.335],   71: [33.529, -79.110],   72: [32.191, -80.742],
  73: [32.231, -80.848],   74: [33.717, -78.898],   75: [32.257, -80.850],
  76: [32.183, -80.754],   77: [33.477, -79.099],   78: [35.438, -83.143],
  79: [33.482, -79.077],   80: [35.923, -86.864],   81: [36.077, -86.930],
  82: [36.287, -86.651],   83: [36.288, -86.652],   84: [36.024, -86.641],
  85: [36.110, -86.876],   86: [35.941, -86.880],   87: [35.019, -85.704],
  88: [35.204, -85.920],   89: [36.078, -87.321],   90: [36.162, -86.814],
  91: [35.908, -86.892],   92: [30.135, -97.365],   93: [37.163, -113.708],
  94: [40.750, -111.702],  95: [40.657, -111.910],  96: [37.165, -113.312],
  97: [40.330, -111.723],  98: [40.519, -111.499],  99: [37.299, -76.877],
  100:[37.320, -76.765],   101:[37.286, -76.702],   102:[37.254, -76.699],
  103:[37.255, -76.700],   104:[37.439, -77.043],   105:[37.387, -76.754],
  106:[37.499, -76.921],   107:[37.277, -76.823],   108:[48.110, -119.764],
  109:[48.111, -119.765],  110:[43.399, -88.324],   111:[44.527, -89.572],
  112:[44.543, -89.554],   113:[43.119, -88.465],   114:[25.832, -80.327],
  115:[33.823, -78.765],   116:[36.101, -115.173],  117:[33.554, -79.065],
  118:[36.154, -115.199],  119:[36.177, -115.250],  120:[36.087, -115.165],
  121:[36.030, -114.983],  122:[25.957, -80.143],   123:[25.958, -80.144],
  124:[33.578, -117.830],  125:[33.577, -117.831],  126:[28.401, -81.239],
  127:[37.172, -113.389],  128:[37.139, -113.530],  129:[37.199, -113.380],
  130:[36.809, -114.110],  131:[36.818, -114.077],
};

// ── VIEW STATE ────────────────────────────────────────────────────────
let activeView = 'map';
let mapInitialized = false;
let mapInstance = null;
let clusterGroup = null;
let courseMarkers = {};
let initialBounds = null;

function setView(view) {
  activeView = view;
  document.getElementById('vtogMap').classList.toggle('active', view === 'map');
  document.getElementById('vtogList').classList.toggle('active', view === 'list');
  document.getElementById('vtogMap').setAttribute('aria-pressed', String(view === 'map'));
  document.getElementById('vtogList').setAttribute('aria-pressed', String(view === 'list'));
  document.getElementById('mapView').style.display = view === 'map' ? 'block' : 'none';
  document.getElementById('courseGridWrap').style.display = view === 'list' ? 'block' : 'none';
  if (view === 'map' && !mapInitialized) initMap();
  else if (view === 'map') filterMap(activeDest);
}

// ── MAP INIT ──────────────────────────────────────────────────────────
function initMap() {
  if (mapInitialized) return;
  mapInitialized = true;

  mapInstance = L.map('courseMap', {
    scrollWheelZoom: false,
    zoomControl: true,
    attributionControl: false,
    maxZoom: 18
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd', maxZoom: 19
  }).addTo(mapInstance);

  const pinIcon = () => L.divIcon({
    className: '',
    html: '<div class="map-pin"></div>',
    iconSize: [14, 14], iconAnchor: [7, 7]
  });

  clusterGroup = L.markerClusterGroup({
    maxClusterRadius: 50,
    showCoverageOnHover: false,
    spiderfyOnMaxZoom: true,
    iconCreateFunction(cluster) {
      const n = cluster.getChildCount();
      const sz = n >= 20 ? 44 : n >= 10 ? 38 : n >= 5 ? 32 : 28;
      const fs = sz <= 28 ? 11 : sz <= 32 ? 12 : 13;
      return L.divIcon({
        html: '<div class="map-cluster" style="width:' + sz + 'px;height:' + sz + 'px;font-size:' + fs + 'px">' + n + '</div>',
        className: '', iconSize: [sz, sz], iconAnchor: [sz/2, sz/2]
      });
    }
  });

  // ── Floating preview card ──────────────────────────────────────────
  const previewEl = document.createElement('div');
  previewEl.className = 'map-preview-float';
  document.body.appendChild(previewEl);

  let hideTimer = null;
  const cancelHide = () => clearTimeout(hideTimer);
  const startHide  = () => { hideTimer = setTimeout(() => { previewEl.style.display = 'none'; }, 200); };

  previewEl.addEventListener('mouseenter', cancelHide);
  previewEl.addEventListener('mouseleave', startHide);

  function positionPreview(latlng) {
    const pt  = mapInstance.latLngToContainerPoint(latlng);
    const rect = document.getElementById('courseMap').getBoundingClientRect();
    previewEl.style.left = (rect.left + pt.x) + 'px';
    previewEl.style.top  = (rect.top  + pt.y) + 'px';
  }

  function showCoursePreview(course, latlng) {
    cancelHide();
    positionPreview(latlng);
    const stars = course.cyntp_rating != null ? '&#9733; ' + course.cyntp_rating.toFixed(1) : '';
    previewEl.innerHTML =
      '<div class="mpc-inner">' +
        '<div class="mpc-name">' + course.name.replace(/&mdash;/g,'—').replace(/&amp;/g,'&') + '</div>' +
        '<div class="mpc-location">' + (course.city || course.destLabel) + '</div>' +
        (stars ? '<div class="mpc-rating">' + stars + '</div>' : '') +
        '<button class="mpc-view-btn" onclick="openCourse(' + course.id + ')">VIEW COURSE &#8594;</button>' +
      '</div>';
    previewEl.style.display = 'block';
  }

  function showClusterPreview(cluster, latlng) {
    cancelHide();
    positionPreview(latlng);
    const markers  = cluster.getAllChildMarkers();
    const courses  = markers.map(m => COURSES.find(c => c.id === m.courseId)).filter(Boolean);
    const destMap  = {};
    courses.forEach(c => { destMap[c.destLabel] = (destMap[c.destLabel] || 0) + 1; });
    const dests    = Object.entries(destMap).sort((a,b) => b[1]-a[1]);
    const show5    = dests.slice(0, 5);
    const remaining = dests.length - 5;
    const listHtml = show5.map(([lbl,cnt]) =>
      '<div class="mpc-dest-item"><span>' + lbl + '</span><span class="mpc-dest-count">' + cnt + '</span></div>'
    ).join('');
    previewEl._cluster = cluster;
    previewEl.innerHTML =
      '<div class="mpc-inner">' +
        '<div class="mpc-cluster-header">' + courses.length + ' course' + (courses.length !== 1 ? 's' : '') +
          ' &middot; ' + dests.length + ' destination' + (dests.length !== 1 ? 's' : '') + '</div>' +
        '<div class="mpc-dest-list">' + listHtml + '</div>' +
        (remaining > 0 ? '<div class="mpc-cluster-more">+ ' + remaining + ' more</div>' : '') +
        '<button class="mpc-zoom-btn" onclick="_zoomCluster()">ZOOM IN &#8594;</button>' +
      '</div>';
    previewEl.style.display = 'block';
  }

  window._zoomCluster = function() {
    if (previewEl._cluster) {
      previewEl.style.display = 'none';
      previewEl._cluster.zoomToBounds({ padding: [40, 40] });
    }
  };

  // ── Build markers ──────────────────────────────────────────────────
  COURSES.forEach(function(c) {
    const coords = COORDS[c.id];
    if (!coords) return;
    const marker = L.marker(coords, { icon: pinIcon() });
    marker.courseId = c.id;
    courseMarkers[c.id] = marker;

    marker.on('mouseover', function(e) { showCoursePreview(c, e.latlng); });
    marker.on('mouseout',  startHide);
    marker.on('click',     function(e) {
      cancelHide();
      showCoursePreview(c, e.latlng);
      L.DomEvent.stopPropagation(e);
    });
    clusterGroup.addLayer(marker);
  });

  clusterGroup.on('clustermouseover', function(e) { showClusterPreview(e.layer, e.latlng); });
  clusterGroup.on('clustermouseout',  startHide);
  clusterGroup.on('clusterclick',     function(e) {
    cancelHide();
    showClusterPreview(e.layer, e.latlng);
  });

  mapInstance.addLayer(clusterGroup);

  // Hide preview on map move / page scroll / map click
  mapInstance.on('movestart', function() { previewEl.style.display = 'none'; });
  mapInstance.on('click',     startHide);
  window.addEventListener('scroll', function() { previewEl.style.display = 'none'; }, { passive: true });

  // Initial view
  const allCoords = COURSES.filter(c => COORDS[c.id]).map(c => COORDS[c.id]);
  initialBounds = L.latLngBounds(allCoords);
  mapInstance.fitBounds(initialBounds, { padding: [40, 40] });

  // Reset button
  mapInstance.on('moveend zoomend', checkResetBtn);
  renderStatsFooter();
}

function checkResetBtn() {
  if (!mapInstance || !initialBounds) return;
  const btn = document.getElementById('mapResetBtn');
  if (!btn) return;
  const c0 = initialBounds.getCenter();
  const c1 = mapInstance.getCenter();
  const z0 = mapInstance.getBoundsZoom(initialBounds, false, [40, 40]);
  const z1 = mapInstance.getZoom();
  const moved = Math.abs(c1.lat - c0.lat) > 0.8 ||
                Math.abs(c1.lng - c0.lng) > 0.8 ||
                Math.abs(z1 - z0) > 0.5;
  btn.disabled = !moved;
}

function resetMapView() {
  if (!mapInstance || !initialBounds) return;
  mapInstance.flyToBounds(initialBounds, { padding: [40, 40], duration: 0.8 });
}

function filterMap(dest) {
  if (!mapInitialized || !mapInstance) return;
  clusterGroup.clearLayers();
  const filtered = dest === 'all' ? COURSES : COURSES.filter(c => c.dest === dest);
  filtered.forEach(function(c) {
    if (courseMarkers[c.id]) clusterGroup.addLayer(courseMarkers[c.id]);
  });
  if (clusterGroup.getLayers().length > 0) {
    const b = clusterGroup.getBounds();
    if (b.isValid()) mapInstance.flyToBounds(b, { padding: [40, 40], duration: 0.6 });
  }
  renderStatsFooter(filtered.length);
}

function renderStatsFooter(count) {
  const el = document.getElementById('mapStatsFooter');
  if (!el) return;
  const total  = (count !== undefined) ? count : COURSES.length;
  const dests  = new Set(
    (count !== undefined && activeDest !== 'all'
      ? COURSES.filter(c => c.dest === activeDest)
      : COURSES
    ).map(c => c.dest)
  ).size;
  const countries = new Set(COURSES.map(function(c) {
    if (c.dest === 'ireland') return 'IE';
    if (c.dest === 'dominican-republic') return 'DR';
    return 'US';
  })).size;
  el.innerHTML =
    '<strong>' + total + '</strong>&nbsp;Courses Played' +
    ' <span class="msd-dot">&middot;</span> ' +
    '<strong>' + dests + '</strong>&nbsp;Destination' + (dests !== 1 ? 's' : '') +
    ' <span class="msd-dot">&middot;</span> ' +
    '<strong>' + countries + '</strong>&nbsp;Countries';
}
"""

# Insert before the last </script> that contains the main JS
# We identify it by looking for the email-capture script tag
SCRIPT_ANCHOR = '<script src="/email-capture.js"></script>'
html = html.replace(SCRIPT_ANCHOR, MAP_JS + '\n' + SCRIPT_ANCHOR, 1)

# ══════════════════════════════════════════════════════════════════════
# 5. Add Leaflet CDN JS before email-capture.js
# ══════════════════════════════════════════════════════════════════════
LEAFLET_JS = """\
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
"""
html = html.replace(SCRIPT_ANCHOR, LEAFLET_JS + SCRIPT_ANCHOR, 1)

# ══════════════════════════════════════════════════════════════════════
# 6. Patch filter tab click handler to respect activeView
# ══════════════════════════════════════════════════════════════════════
OLD_FILTER = """    activeDest = this.dataset.dest;
    renderGrid();"""
NEW_FILTER = """    activeDest = this.dataset.dest;
    if (activeView === 'map') filterMap(activeDest);
    else renderGrid();"""
html = html.replace(OLD_FILTER, NEW_FILTER, 1)

# ══════════════════════════════════════════════════════════════════════
# 7. Set default view to MAP on init (after renderGrid() call)
# ══════════════════════════════════════════════════════════════════════
OLD_INIT = 'loadData();\nrenderGrid();\nwindow.addEventListener'
NEW_INIT = 'loadData();\nrenderGrid();\nsetView(\'map\');\nwindow.addEventListener'
html = html.replace(OLD_INIT, NEW_INIT, 1)

# ══════════════════════════════════════════════════════════════════════
# 8. Write output
# ══════════════════════════════════════════════════════════════════════
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done. Injected map into', HTML_PATH)
