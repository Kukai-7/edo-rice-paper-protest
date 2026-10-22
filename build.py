"""Build the Edo Rice, Paper and Protest dataset.
Sources: GPIH (Iwahashi rice prices, compiled by O. Saito), NOAA WDS Paleo (Mikami historical weather diaries),
Japanese Wikipedia (notable uprisings, hansatsu by domain). See README for citations."""
import re, json, os, xlrd, numpy as np, pandas as pd
from uprisings_curated import EVENTS

RAW, OUT = 'raw', 'out/data'
os.makedirs(OUT, exist_ok=True)

ERAS = [(1615, 'Genna'), (1624, 'Kan\'ei'), (1644, 'Shoho'), (1648, 'Keian'), (1652, 'Joo'), (1655, 'Meireki'),
        (1658, 'Manji'), (1661, 'Kanbun'), (1673, 'Enpo'), (1681, 'Tenna'), (1684, 'Jokyo'), (1688, 'Genroku'),
        (1704, 'Hoei'), (1711, 'Shotoku'), (1716, 'Kyoho'), (1736, 'Genbun'), (1741, 'Kanpo'), (1744, 'Enkyo'),
        (1748, 'Kan\'en'), (1751, 'Horeki'), (1764, 'Meiwa'), (1772, 'An\'ei'), (1781, 'Tenmei'), (1789, 'Kansei'),
        (1801, 'Kyowa'), (1804, 'Bunka'), (1818, 'Bunsei'), (1830, 'Tenpo'), (1844, 'Koka'), (1848, 'Kaei'),
        (1854, 'Ansei'), (1860, 'Man\'en'), (1861, 'Bunkyu'), (1864, 'Genji'), (1865, 'Keio')]
def era(y):
    e = None
    for a, n in ERAS:
        if y >= a: e = n
    return e if y >= 1615 else 'Keicho'

# ------------------------------------------------------------------ rice prices (Iwahashi via GPIH)
wb = xlrd.open_workbook(f'{RAW}/gpih/Japan_rice_P_1620-1867.xls')
sh = wb.sheet_by_name('koku of rice')
hdr = [str(sh.cell_value(7, c)).strip() for c in range(sh.ncols)]
cur = [str(sh.cell_value(5, c)) for c in range(sh.ncols)]
cols = {}
unit = 'silver monme'
for c in range(1, sh.ncols):
    if 'Ryo' in cur[c]: unit = 'gold ryo'
    name = hdr[c]
    key = {'Osaka': 'osaka', 'Otsu town, Omi prov.': 'otsu', 'Rural Banshu prov.': 'banshu', 'Fukuchiyama': 'fukuchiyama',
           'Hiroshima': 'hiroshima', 'Bocho': 'bocho', 'Saga': 'saga', 'Kumamoto': 'kumamoto', 'Edo': 'edo', 'Nagoya': 'nagoya',
           'Shinshu': 'shinshu', 'Aizu': 'aizu', 'Dewa': 'dewa'}[name]
    if unit == 'gold ryo': key += '_ryo'
    else: key += '_monme'
    cols[c] = 'rice_' + key
rows = []
for r in range(8, sh.nrows):
    y = sh.cell_value(r, 0)
    if not isinstance(y, float): continue
    d = {'year': int(y)}
    for c, k in cols.items():
        v = sh.cell_value(r, c)
        d[k] = float(v) if isinstance(v, float) else np.nan
    rows.append(d)
rice = pd.DataFrame(rows)
rice = rice.loc[:, rice.notna().any()]
print('rice cols', list(rice.columns), rice.year.min(), rice.year.max())

# ------------------------------------------------------------------ weather diaries (Mikami, NOAA)
ST = {'hirosk': ('Hirosaki', 40.6, 140.5, 'official'), 'moriok': ('Morioka', 39.7, 141.2, 'official'),
      'kawans': ('Kawanishi', 38.0, 140.0, 'private'), 'nikkou': ('Nikko', 36.7, 139.6, 'official'),
      'hatioj': ('Hachioji', 35.7, 139.3, 'farmhouse'), 'yokham': ('Yokohama', 35.5, 139.6, 'private'),
      'saba': ('Sabae', 36.0, 136.1, 'official'), 'ise': ('Ise', 34.5, 136.7, 'official'),
      'ikeda': ('Ikeda', 34.8, 135.5, 'official'), 'tanabe': ('Tanabe', 33.7, 135.4, 'private'),
      'hagi': ('Hagi', 34.4, 131.4, 'official'), 'usuki': ('Usuki', 33.2, 131.8, 'official'),
      'nagaski': ('Nagasaki', 32.7, 130.0, 'official')}
W = []
for f, (name, lat, lon, kind) in ST.items():
    for line in open(f'{RAW}/noaa/{f}.txt'):
        p = line.split()
        if not p or not p[0].isdigit(): continue
        nums = list(map(int, p[3:]))
        if len(nums) < 15: continue
        t = dict(zip(['fine', 'partly_cloudy', 'cloudy', 'shower', 'thunderstorm', 'heavy_thunderstorm', 'little_rain', 'rain',
                      'heavy_rain', 'hail', 'snow_shower', 'little_snow', 'snow', 'no_record', 'days_in_month'], nums[:15]))
        t.update(station=name, year=int(p[0]), month=int(p[1]))
        if 1600 <= t['year'] <= 1900 and 1 <= t['month'] <= 12:
            W.append(t)
wm = pd.DataFrame(W)
wm['days_recorded'] = wm.days_in_month - wm.no_record
wm['rain_days'] = wm[['shower', 'thunderstorm', 'heavy_thunderstorm', 'little_rain', 'rain', 'heavy_rain']].sum(axis=1)
wm['snow_days'] = wm[['snow_shower', 'little_snow', 'snow']].sum(axis=1)
wm = wm[['station', 'year', 'month', 'days_in_month', 'days_recorded', 'fine', 'partly_cloudy', 'cloudy', 'shower', 'thunderstorm',
         'heavy_thunderstorm', 'little_rain', 'rain', 'heavy_rain', 'hail', 'snow_shower', 'little_snow', 'snow', 'rain_days', 'snow_days']]
wm = wm.sort_values(['station', 'year', 'month']).reset_index(drop=True)
wm.to_parquet(f'{OUT}/weather_monthly.parquet', index=False)
stations = pd.DataFrame([dict(station=n, latitude=la, longitude=lo, diary_type=k,
                              first_year=int(wm[wm.station == n].year.min()), last_year=int(wm[wm.station == n].year.max()))
                         for n, la, lo, k in ST.values()])
stations.to_parquet(f'{OUT}/stations.parquet', index=False)

# summer (Jun-Aug) wetness per station-year: rainy days / recorded days, then standardised by station and averaged
s = wm[wm.month.isin([6, 7, 8])].groupby(['station', 'year'])[['rain_days', 'days_recorded']].sum()
s = s[s.days_recorded >= 60]
s['wet'] = s.rain_days / s.days_recorded
s['z'] = s.groupby(level=0).wet.transform(lambda x: (x - x.mean()) / x.std())
summer = s.groupby(level=1).agg(summer_wet_share=('wet', 'mean'), summer_wet_z=('z', 'mean'), n_stations=('z', 'size'))

# ------------------------------------------------------------------ uprisings
up = pd.DataFrame(EVENTS, columns=['year', 'title_ja', 'name_en', 'province_ja', 'province_en', 'domain', 'latitude', 'longitude',
                                   'cause', 'summary_en'])
up['era'] = up.year.map(era)
CG = {'tax burden': 'taxes and levies', 'new tax': 'taxes and levies', 'new tax on silk markets': 'taxes and levies',
      'monetary levies': 'taxes and levies', 'forced levy (goyokin)': 'taxes and levies', 'land survey and tax': 'taxes and levies',
      'land survey': 'taxes and levies', 'new measuring rules': 'taxes and levies', 'corvee (post-horse duty)': 'labour duty',
      'land and debt': 'land and debt', 'domain monopolies': 'domain monopolies', 'paper monopoly': 'domain monopolies',
      'sugar monopoly': 'domain monopolies', 'famine': 'famine and rice prices', 'famine and rice prices': 'famine and rice prices',
      'rice prices': 'famine and rice prices', 'tax burden and famine': 'famine and rice prices', 'drought and irrigation': 'famine and rice prices',
      'resistance to new lord': 'resistance to a new lord', 'world-renewal (yonaoshi)': 'world renewal (yonaoshi)',
      'discriminatory edict': 'status and discrimination'}
up['cause_group'] = up.cause.map(CG)
assert up.cause_group.notna().all(), up[up.cause_group.isna()]
up['source_url'] = 'https://ja.wikipedia.org/wiki/' + up.title_ja.str.replace(' ', '_')
up.to_parquet(f'{OUT}/uprisings.parquet', index=False)

# ------------------------------------------------------------------ hansatsu issuers (Wikipedia, 各藩の状況)
w = open(f'{RAW}/wiki/hansatsu.txt', encoding='utf-8').read()
sec = w[w.index('==各藩の状況=='):w.index('== 脚注 ==')]
blocks = []
for blk in re.split(r'\n(?=; |=+)', sec):
    if blk.startswith('='):
        m = re.search(r'(\S+藩)の事例', blk)
        if m: blocks.append((m.group(1), blk))
        continue
    m = re.match(r'; (.+)', blk)
    if m: blocks.append((m.group(1).strip(), blk))
merged = {}
for n, b in blocks:
    n = re.sub(r'（.*?）', '', n)
    merged[n] = merged.get(n, '') + '\n' + b
geo = json.load(open(f'{RAW}/geo.json'))
wc = {}
for x in geo['wc']:
    wc.setdefault(x['q'], x)
qid = {d['req']: d['qid'] for d in geo['dm']}
HAND = {'麻田藩': (34.79, 135.46), '小野藩': (34.85, 134.93), '安志藩': (34.95, 134.60), '狭山藩': (34.50, 135.55),
        '丹南藩': (34.56, 135.55), '伯太藩': (34.48, 135.44), '岡部藩': (36.20, 139.22), '備後福山藩': (34.49, 133.36),
        '三日月藩': (34.96, 134.37), '林田藩': (34.90, 134.57), '三草藩': (34.92, 135.02), '福本藩': (35.03, 134.73)}
EN = {'弘前藩': 'Hirosaki', '仙台藩': 'Sendai', '会津藩': 'Aizu', '久保田藩': 'Kubota (Akita)', '米沢藩': 'Yonezawa',
      '岡部藩': 'Okabe', '岩村藩': 'Iwamura', '苗木藩': 'Naegi', '浜松藩': 'Hamamatsu', '狭山藩': 'Sayama', '丹南藩': 'Tannan',
      '岸和田藩': 'Kishiwada', '伯太藩': 'Hakata (Izumi)', '麻田藩': 'Asada', '尼崎藩': 'Amagasaki', '三田藩': 'Sanda',
      '高槻藩': 'Takatsuki', '明石藩': 'Akashi', '安志藩': 'Anshi', '小野藩': 'Ono', '龍野藩': 'Tatsuno', '林田藩': 'Hayashida',
      '姫路藩': 'Himeji', '福本藩': 'Fukumoto', '三日月藩': 'Mikazuki', '三草藩': 'Mikusa', '山崎藩': 'Yamasaki', '赤穂藩': 'Ako',
      '広島藩': 'Hiroshima', '備後福山藩': 'Fukuyama', '備中松山藩': 'Bitchu-Matsuyama', '徳島藩': 'Tokushima', '秋月藩': 'Akizuki'}
PROV_FIX = {'丹南藩': '河内国', '伯太藩': '和泉国', '尼崎藩': '摂津国', '高槻藩': '摂津国', '会津藩': '陸奥国', '浜松藩': '遠江国',
            '岡部藩': '武蔵国', **{k: '播磨国' for k in ['安志藩', '小野藩', '龍野藩', '林田藩', '姫路藩', '福本藩', '三日月藩', '三草藩', '山崎藩', '赤穂藩', '明石藩']}}
H = []
for n, b in merged.items():
    yrs = sorted(int(y) for y in re.findall(r'(1[6-8]\d\d)年', b) if 1600 <= int(y) <= 1871)
    q = qid.get(n) or qid.get(n.replace('備後', ''))
    pt = None
    if q and q in wc:
        pt = wc[q].get('c') or wc[q].get('hq')
    if pt:
        lo, la = map(float, re.findall(r'[-\d.]+', pt))
        how = 'Wikidata'
    elif n in HAND:
        la, lo = HAND[n]; how = 'approximate, set by hand'
    else:
        la = lo = None; how = None
    prov = re.findall(r'\[\[(\S{1,4}国)\]\]', b)
    prov = [PROV_FIX[n]] if n in PROV_FIX else prov
    H.append(dict(domain_ja=n, domain_en=EN.get(n, n), province_ja=prov[0] if prov else None,
                  earliest_year_mentioned=yrs[0] if yrs else None, latitude=la, longitude=lo, coordinates_from=how,
                  source_url='https://ja.wikipedia.org/wiki/%E8%97%A9%E6%9C%AD'))
hans = pd.DataFrame(H)
hans['earliest_year_mentioned'] = hans.earliest_year_mentioned.astype('Int64')
hans.to_parquet(f'{OUT}/hansatsu_domains.parquet', index=False)

# ------------------------------------------------------------------ annual panel 1620-1867
FAMINES = [(1640, 1643, "Kan'ei famine"), (1732, 1733, 'Kyoho famine'), (1755, 1757, 'Horeki famine'),
           (1782, 1788, 'Tenmei famine'), (1833, 1839, 'Tenpo famine')]
def famine(y):
    for a, b, n in FAMINES:
        if a <= y <= b: return n
    return None
def hansatsu_regime(y):
    if y < 1661: return 'before first domain notes'
    if y < 1707: return 'domain notes allowed'
    if y < 1730: return 'banned (1707 edict)'
    if y < 1759: return 'allowed again (1730)'
    return 'existing notes only, new issues restricted (1759)'
an = pd.DataFrame({'year': range(1620, 1868)})
an['era'] = an.year.map(era)
an = an.merge(rice, on='year', how='left')
o = an.set_index('year').rice_osaka_monme
an['osaka_price_vs_trend'] = (np.log(o) - np.log(o).rolling(11, center=True, min_periods=6).median()).round(4).values
monme = [c for c in an.columns if c.endswith('_monme')]
dev = pd.DataFrame({c: np.log(an[c]) - np.log(an[c]).rolling(11, center=True, min_periods=6).median() for c in monme})
an['rice_shock'] = dev.mean(axis=1).round(4)
an['rice_shock_n_series'] = dev.notna().sum(axis=1)
an = an.merge(summer.reset_index(), on='year', how='left')
an['famine'] = an.year.map(famine)
an['hansatsu_regime'] = an.year.map(hansatsu_regime)
an['hansatsu_domains_first_mentioned'] = an.year.map(hans.earliest_year_mentioned.value_counts()).fillna(0).astype(int)
an['notable_uprisings'] = an.year.map(up.year.value_counts()).fillna(0).astype(int)
an.to_parquet(f'{OUT}/annual.parquet', index=False)

stats = dict(years=len(an), rice_series=[c for c in rice.columns if c != 'year'], weather_rows=len(wm), stations=len(stations),
             uprisings=len(up), hansatsu_domains=len(hans), hansatsu_with_coords=int(hans.latitude.notna().sum()))
json.dump(stats, open('out/stats.json', 'w'), indent=1)
print(stats)
