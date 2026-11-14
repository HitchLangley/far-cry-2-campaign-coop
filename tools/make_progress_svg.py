# Draws docs/progress.svg for the README: overall progress, a bar per area and the time spent.
# The percentages are the maintainer's estimates; edit AREAS / STATS and run: python -I tools/make_progress_svg.py
# One SVG for both GitHub themes: colours switch with prefers-color-scheme inside the file.
import os

TITLE = 'Far Cry 2 Campaign Coop'
DATE = '14 November 2026'
# (area, percent, weight in the overall figure): the campaign itself (missions, world) weighs more
AREAS = [
    ('Joining and menu', 85, 1),
    ('Partner avatar', 75, 1),
    ('Player hits', 80, 1),
    ('Vehicles', 60, 1),
    ('NPCs on the joiner', 55, 2),
    ('Enemies attack the joiner', 30, 2),
    ('World state', 10, 2),
    ('Missions and story', 0, 3),
]
STATS = [
    ('51 h', 'AI-assisted development'),
    ('610', 'game test runs (63 h)'),
    ('87', 'commits'),
    ('17', 'days of work sessions'),
]

W, PAD = 840, 32
overall = round(sum(p * w for _, p, w in AREAS) / sum(w for _, _, w in AREAS))


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


out = []
y = PAD
out.append('<text class="title" x="%d" y="%d">%s</text>' % (PAD, y + 22, esc(TITLE)))
out.append('<text class="muted" x="%d" y="%d">Progress estimate, %s</text>' % (PAD, y + 46, DATE))
# overall
y += 76
bw = W - 2 * PAD - 110
out.append('<text class="label" x="%d" y="%d">Campaign co-op overall</text>' % (PAD, y))
out.append('<text class="big" x="%d" y="%d" text-anchor="end">%d%%</text>' % (W - PAD, y + 30, overall))
out.append('<rect class="track" x="%d" y="%d" width="%d" height="14" rx="7"/>' % (PAD, y + 14, bw))
out.append('<rect class="fill" x="%d" y="%d" width="%d" height="14" rx="7"/>' % (PAD, y + 14, max(14, bw * overall // 100)))
# areas, two columns
y += 62
colw = (W - 2 * PAD - 32) // 2
for i, (name, p, _) in enumerate(AREAS):
    cx = PAD + (i % 2) * (colw + 32)
    cy = y + (i // 2) * 46
    out.append('<text class="label" x="%d" y="%d">%s</text>' % (cx, cy, esc(name)))
    out.append('<text class="pct" x="%d" y="%d" text-anchor="end">%d%%</text>' % (cx + colw, cy, p))
    out.append('<rect class="track" x="%d" y="%d" width="%d" height="8" rx="4"/>' % (cx, cy + 9, colw))
    if p:
        out.append('<rect class="%s" x="%d" y="%d" width="%d" height="8" rx="4"/>' % ('fill' if p >= 50 else 'part', cx, cy + 9, max(8, colw * p // 100)))
y += (len(AREAS) + 1) // 2 * 46 + 6
# stats tiles
out.append('<line class="rule" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (PAD, y, W - PAD, y))
y += 20
tw = (W - 2 * PAD - 3 * 16) // 4
for i, (v, label) in enumerate(STATS):
    tx = PAD + i * (tw + 16)
    out.append('<rect class="tile" x="%d" y="%d" width="%d" height="70" rx="10"/>' % (tx, y, tw))
    out.append('<text class="stat" x="%d" y="%d">%s</text>' % (tx + 14, y + 34, esc(v)))
    out.append('<text class="muted small" x="%d" y="%d">%s</text>' % (tx + 14, y + 55, esc(label)))
y += 70 + PAD
H = y

style = '''
  .bg { fill: #ffffff; } .title { font: 700 22px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #1f2328; }
  .label { font: 500 14px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #1f2328; }
  .pct { font: 600 13px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #59636e; }
  .big { font: 700 30px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #c2410c; }
  .stat { font: 700 24px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #1f2328; }
  .muted { font: 400 13px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #59636e; } .small { font-size: 12px; }
  .track { fill: #eaeef2; } .fill { fill: #ea580c; } .part { fill: #f5a46b; } .tile { fill: #f6f8fa; } .rule { stroke: #d1d9e0; }
  .frame { fill: none; stroke: #d1d9e0; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #0d1117; } .title, .label, .stat { fill: #f0f6fc; } .pct, .muted { fill: #9198a1; } .big { fill: #fb923c; }
    .track { fill: #21262d; } .fill { fill: #f97316; } .part { fill: #9a4a1c; } .tile { fill: #161b22; } .rule, .frame { stroke: #30363d; }
  }
'''
svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s: %d%% overall">\n'
       '<style>%s</style>\n<rect class="bg" x="0.5" y="0.5" width="%d" height="%d" rx="14"/>\n'
       '<rect class="frame" x="0.5" y="0.5" width="%d" height="%d" rx="14"/>\n%s\n</svg>\n') % (
    W, H, W, H, esc(TITLE), overall, style, W - 1, H - 1, W - 1, H - 1, '\n'.join(out))
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'progress.svg')
with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(svg)
print('overall %d%%, %dx%d -> %s' % (overall, W, H, os.path.normpath(path)))
