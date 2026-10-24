import json, os, glob, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import shape, box

for f in glob.glob('fonts/*.otf') + ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc']:
    if os.path.exists(f): fm.fontManager.addfont(f)
_n = {f.name for f in fm.fontManager.ttflist}
FONT = next((n for n in ('Noto Sans CJK SC', 'Noto Sans CJK JP') if n in _n), 'DejaVu Sans')
plt.rcParams.update({'font.family': FONT, 'font.size': 10, 'axes.edgecolor': '#BBBBBB', 'axes.linewidth': .6,
                     'xtick.color': '#666666', 'ytick.color': '#666666', 'axes.labelcolor': '#444444', 'text.color': '#1F1F1F',
                     'savefig.dpi': 200})
INK, MID, LIGHT, LAND, PAPER = '#1F1F1F', '#8A8A8A', '#C9C6BF', '#ECE9E3', '#FFFFFF'
RED, RED_SOFT, BLUE, BLUE_SOFT = '#B33A2B', '#E3B5AE', '#2F4B7C', '#B9C4D6'
os.makedirs('out/assets', exist_ok=True)

an = pd.read_parquet('out/data/annual.parquet')
up = pd.read_parquet('out/data/uprisings.parquet')
hs = pd.read_parquet('out/data/hansatsu_domains.parquet')
st = pd.read_parquet('out/data/stations.parquet')
wm = pd.read_parquet('out/data/weather_monthly.parquet')

def title(fig, t, s, y=.95):
    fig.text(.05, y, t, fontsize=15, weight='bold')
    fig.text(.05, y - .045, s, fontsize=9, color='#555555')

# ------------------------------------------------------------------ 1. map
EXT = (129.3, 142.6, 30.9, 41.9)
clip = box(EXT[0] - 1, EXT[2] - 1, EXT[1] + 1, EXT[3] + 1)
def polys(g):
    g = g.intersection(clip)
    if g.is_empty: return []
    return [np.array(p.exterior.coords) for p in getattr(g, 'geoms', [g]) if p.geom_type == 'Polygon']
land = [shape(f['geometry']) for f in json.load(open('raw/ne_10m_land.geojson'))['features']]
lakes = [shape(f['geometry']) for f in json.load(open('raw/ne_10m_lakes.geojson'))['features']]
fig, ax = plt.subplots(figsize=(8.6, 8.6))
for g in land:
    if g.intersects(clip):
        for a in polys(g): ax.add_patch(MPoly(a, closed=True, fc=LAND, ec=LIGHT, lw=.4))
for g in lakes:
    if g.intersects(clip):
        for a in polys(g): ax.add_patch(MPoly(a, closed=True, fc=PAPER, ec=LIGHT, lw=.3))
u = up.dropna(subset=['latitude'])
ax.scatter(u.longitude, u.latitude, s=46, c=RED, alpha=.85, lw=.6, edgecolors=PAPER, zorder=4, label=f'Notable uprising ({len(u)})')
ax.scatter(hs.longitude, hs.latitude, s=26, marker='s', c=BLUE, alpha=.85, lw=.5, edgecolors=PAPER, zorder=3,
           label=f'Domain issuing paper notes, hansatsu ({len(hs)})')
ax.scatter(st.longitude, st.latitude, s=40, marker='^', c=PAPER, edgecolors=INK, lw=.8, zorder=5, label='Weather diary (13)')
for r in st.itertuples():
    ax.annotate(r.station, (r.longitude, r.latitude), xytext=(5, -3), textcoords='offset points', fontsize=7, color=MID)
for t, lab in [('島原の乱', 'Shimabara 1637'), ('郡上一揆', 'Gujo 1754 '), ('天保騒動', 'Kai 1836'), ('三閉伊一揆', 'Sanhei 1847'),
               ('長州藩天保一揆', 'Choshu 1831')]:
    r = up[up.title_ja == t].iloc[0]
    off, ha = ((8, -12), 'left') if t == '郡上一揆' else ((-8, 8), 'right')
    ax.annotate(lab, (r.longitude, r.latitude), xytext=off, textcoords='offset points', ha=ha, fontsize=8, color=RED)
ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3]); ax.set_aspect(1 / np.cos(np.radians(36)))
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.legend(loc='lower right', frameon=False, fontsize=8.5, markerscale=1.1)
title(fig, 'Rice, paper and protest in Edo Japan', 'Where the notable uprisings, the paper-note domains and the weather diaries are.', y=.955)
fig.text(.05, .03, 'Uprisings and hansatsu: Japanese Wikipedia, positions approximate. Diaries: Mikami (NOAA WDS Paleo). Coastline: Natural Earth.',
         fontsize=7, color=MID)
plt.subplots_adjust(left=.02, right=.98, top=.88, bottom=.05)
fig.savefig('out/assets/map_edo.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 2. timeline
fig, ax = plt.subplots(figsize=(12, 4.8))
ax.axvspan(1707, 1730, color=BLUE_SOFT, alpha=.45, lw=0, zorder=0)
ax.text(1718.5, 255, 'Hansatsu\nbanned', ha='center', fontsize=7.6, color=BLUE)
for a, b, n in [(1640, 1643, "Kan'ei"), (1732, 1733, 'Kyoho'), (1755, 1757, 'Horeki'), (1782, 1788, 'Tenmei'), (1833, 1839, 'Tenpo')]:
    ax.axvspan(a - .5, b + .5, color=RED_SOFT, alpha=.55, lw=0, zorder=0)
    ax.text((a + b) / 2, 255 if n != 'Tenpo' else 255, n, ha='center', fontsize=7.6, color=RED)
for c, lab, col, lw in [('rice_hiroshima_monme', 'Hiroshima (merchant accounts)', MID, .9), ('rice_osaka_monme', 'Osaka (Dojima market)', INK, 1.2)]:
    ax.plot(an.year, an[c], color=col, lw=lw, label=lab, zorder=3)
ax.set_yscale('log'); ax.set_ylim(15, 420)
from matplotlib.ticker import FixedLocator, NullFormatter, FixedFormatter
ax.yaxis.set_major_locator(FixedLocator([20, 50, 100, 200, 400])); ax.yaxis.set_major_formatter(FixedFormatter(['20', '50', '100', '200', '400']))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_ylabel('Silver monme per koku of rice (log scale)')
yrs = up.year.values
ax.scatter(yrs, np.full(len(yrs), 17.5), marker='|', s=90, c=RED, lw=1.2, zorder=4, label='Notable uprising')
ax.set_xlim(1618, 1869); ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.0), frameon=False, fontsize=8.2, ncol=3)
title(fig, 'Two and a half centuries of rice prices', 'Price spikes line up with the great famines; the notable uprisings are spread far more evenly.', y=.96)
plt.subplots_adjust(left=.07, right=.985, top=.8, bottom=.1)
fig.savefig('out/assets/timeline_edo.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 3. scatter-plot matrix: made by correlations.py, with r, confidence intervals and p-values

# ------------------------------------------------------------------ 4. causes of the notable uprisings
cg = up.cause_group.value_counts().sort_values()
fig, ax = plt.subplots(figsize=(8.5, 4.2))
cols = [RED if c == 'famine and rice prices' else (BLUE if c == 'taxes and levies' else LIGHT) for c in cg.index]
ax.barh(cg.index, cg.values, color=cols, height=.62)
for y, v in enumerate(cg.values): ax.text(v + .3, y, str(v), va='center', fontsize=8.5, color=INK)
ax.spines[['top', 'right', 'bottom']].set_visible(False); ax.set_xticks([]); ax.tick_params(length=0, labelsize=9)
title(fig, 'What the uprisings were about', f'Main grievance of the {len(up)} notable uprisings, from each Wikipedia article.', y=.93)
plt.subplots_adjust(left=.3, right=.95, top=.78, bottom=.05)
fig.savefig('out/assets/causes.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 5. diaries heatmap: summer wetness by station and decade
s = wm[wm.month.isin([6, 7, 8])].copy(); s['decade'] = (s.year // 10) * 10
g = s.groupby(['station', 'decade'])[['rain_days', 'days_recorded']].sum()
g = g[g.days_recorded >= 180]
share = (g.rain_days / g.days_recorded).unstack()
order = st.sort_values('latitude', ascending=False).station
share = share.reindex(order)
share = share[[c for c in share.columns if 1660 <= c <= 1880]]
fig, ax = plt.subplots(figsize=(12, 4.6))
cmap = LinearSegmentedColormap.from_list('wet', ['#F4F2EE', BLUE_SOFT, BLUE, '#14243F']); cmap.set_bad(PAPER)
im = ax.imshow(share.values, aspect='auto', cmap=cmap, vmin=.2, vmax=.65, interpolation='nearest')
ax.set_yticks(range(len(share))); ax.set_yticklabels(share.index, fontsize=8.5)
ax.set_xticks(range(len(share.columns))[::2]); ax.set_xticklabels([f'{c}s' for c in share.columns][::2], fontsize=8)
for s_ in ax.spines.values(): s_.set_visible(False)
ax.tick_params(length=0)
cb = fig.colorbar(im, ax=ax, fraction=.018, pad=.01); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7.5, length=0)
cb.set_label('Share of summer days with rain', fontsize=8, labelpad=6)
title(fig, 'Two centuries of summer weather, from diaries', 'June to August, stations ordered north to south. Blank: too few recorded days.')
plt.subplots_adjust(left=.09, right=.93, top=.83, bottom=.08)
fig.savefig('out/assets/diaries_heatmap.png', facecolor=PAPER); plt.close(fig)
print('ok')
