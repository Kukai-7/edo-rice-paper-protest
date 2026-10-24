# Edo Rice, Paper and Protest

[Dataset on Hugging Face](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest) · code in this repository

**Did paper money and rice prices drive peasant revolts in Edo Japan?** This dataset brings together three kinds of evidence for 1620 to 1867: **rice prices** from fourteen markets, merchants and domains, **weather** written down day after day in thirteen diaries, and the **notable uprisings** and **paper-note domains** (*hansatsu* 藩札) documented in Japanese sources, each placed on the map.

*Le riz, le papier-monnaie et les révoltes paysannes du Japon d'Edo.*

![Rice, paper and protest in Edo Japan](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest/resolve/main/assets/map_edo.png)

*Reading the map: red dots are the 50 notable uprisings (named ones labelled with their year), blue squares the 33 domains whose paper notes are described, triangles the 13 weather diaries. Uprisings spread across the country; paper money clusters around Osaka.*

## At a glance

| | |
|---|---|
| Period | 1620 to 1867, annual; weather diaries 1661 to 1890, monthly |
| Rice prices | 14 series: Osaka, Otsu, Banshu, Fukuchiyama, Hiroshima, Bocho, Saga, Kumamoto in silver; Edo, Osaka, Nagoya, Shinshu, Aizu, Dewa in gold |
| Weather | 23,748 station-months from 13 diaries, about 640,000 recorded days, from Hirosaki to Nagasaki |
| Uprisings | 50 notable uprisings with year, province, domain, grievance and source link |
| Paper money | 33 domains whose notes are described in the sources, with the policy regime for every year |
| Format | Parquet, five configurations: `annual`, `uprisings`, `hansatsu_domains`, `weather_monthly`, `stations` |

## What it shows

![Two and a half centuries of rice prices](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest/resolve/main/assets/timeline_edo.png)

*Reading the chart: rice prices on a log scale, so equal heights mean equal percentage moves. Red bands are the five great famines, the blue band the 1707 to 1730 ban on domain notes, red ticks at the bottom the notable uprisings. Price spikes sit inside the famine bands; the ticks do not cluster there.*

- **Rice prices follow the weather, not the other way round.** In the 23 years of the five great famines, prices sit about 17% above their local trend on average, against about 1% in other years, and the diaries record wetter summers (z-score +0.26). Cool, rainy summers ruin the harvest, then prices jump.
- **The notable uprisings do not follow prices.** Years with an uprising show a slightly higher price shock (+5% against +2%), but the difference is not significant (Mann-Whitney p = 0.90) and the yearly correlation is 0.06. Only 4 of the 50 uprisings fall in famine years, about what chance alone would give.
- **People rose against the lord's demands.** Thirty of the 50 uprisings were about taxes and levies; only five were about famine or the price of rice. The usual reading of the period, that protest targeted the fiscal squeeze of domains rather than the market, holds in this small sample.
- **Paper money was a western affair.** Of the 33 domains whose notes are described, 19 sit in Harima and the provinces around Osaka, close to the money changers who backed the notes.

![What moves with what, year by year](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest/resolve/main/assets/scatter_matrix.png)

*Reading the chart: see "Reading the correlations" below. The only links that hold are between prices and weather; the uprising row is flat.*

![What the uprisings were about](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest/resolve/main/assets/causes.png)

*Reading the chart: the main grievance of each uprising, as given in its article. Taxes and levies dominate; famine and prices come a distant second.*

![Two centuries of summer weather, from diaries](https://huggingface.co/datasets/Kukai-7/edo-rice-paper-protest/resolve/main/assets/diaries_heatmap.png)

*Reading the chart: each row is a diary, north at the top; darker cells are decades with a larger share of rainy summer days. Some writers simply noted rain more often (Nikko, Hachioji), which is why the annual index is standardised station by station.*

## Reading the correlations

**How to read r.** Pearson's r measures how closely two variables move along a straight line: +1 is a perfect positive line, 0 no linear link, -1 a perfect negative line. r² is the share of the variance of one variable that a straight line on the other accounts for (r = 0.7 means about half). The labels used here: under 0.1 negligible, 0.1 to 0.3 weak, 0.3 to 0.5 moderate, 0.5 to 0.7 strong, 0.7 and above very strong.

**How sure is it?** The 95% confidence interval gives the range of r compatible with the data; when it excludes zero, p is below 0.05 and the link is distinguishable from chance. Strength and certainty are different things: a weak r can be certain with many observations, and a strong r can be uncertain with few. Spearman's ρ repeats the exercise on ranks, so a large gap between r and ρ points to outliers or a curved relationship.

**Yearly changes.** Two series that both trend upward will correlate even if they are unrelated. The last column correlates the year-on-year changes instead, which removes shared trends: a link that survives in changes is more convincing than one that exists only in levels.

In the scatter-plot matrix (`scatter_matrix.png`), the panels below the diagonal show the points with a least-squares line, the diagonal shows each distribution, and the panels above the diagonal give r, its 95% confidence interval, p and n for the pair in that row and column. A figure is in colour only when p < 0.05.

**What stands out**

- **Prices and weather move together, and the link survives in yearly changes.** The price shock correlates at +0.24 with wet summers (95% CI +0.10 to +0.36, 207 years), and at +0.34 when both are taken as year-on-year changes. Weak but clearly real: rain explains a small part of price swings, and famines the large ones.
- **Uprisings are unrelated to prices and weather.** All three correlations with the yearly count of notable uprisings are below 0.07 in absolute value, with intervals that straddle zero. This is the central finding of the dataset, and it is a negative one.
- **The +0.75 between the shock and the Osaka price level is partly built in**: the shock is computed from prices that include Osaka. Read it as a check of the series, not as a finding.

**All pairs**, sorted by the size of r. The same figures are in the `correlations` configuration.

| Pair | r | 95% CI | p | n | Spearman ρ | r of yearly changes | Reading |
|---|---|---|---|---|---|---|---|
| Rice price shock (log vs 11-year median) × Osaka price level (log monme) | **+0.75** | +0.67 to +0.81 | < 0.001 | 167 | +0.64 | +0.87 (p < 0.001) | very strong, positive; distinguishable from zero |
| Rice price shock (log vs 11-year median) × Wet summer (diary z-score) | **+0.24** | +0.10 to +0.36 | < 0.001 | 207 | +0.21 | +0.34 (p < 0.001) | weak, positive; distinguishable from zero |
| Wet summer (diary z-score) × Osaka price level (log monme) | **+0.10** | -0.06 to +0.24 | 0.22 | 167 | +0.14 | +0.28 (p < 0.001) | negligible; not distinguishable from zero |
| Wet summer (diary z-score) × Notable uprisings (per year) | **-0.07** | -0.20 to +0.07 | 0.35 | 207 | -0.07 | -0.01 (p = 0.86) | negligible; not distinguishable from zero |
| Rice price shock (log vs 11-year median) × Notable uprisings (per year) | **+0.05** | -0.08 to +0.19 | 0.44 | 207 | -0.01 | +0.08 (p = 0.27) | negligible; not distinguishable from zero |
| Osaka price level (log monme) × Notable uprisings (per year) | **+0.02** | -0.13 to +0.17 | 0.79 | 167 | -0.02 | +0.05 (p = 0.49) | negligible; not distinguishable from zero |

**What it does not say**

- Fifty uprisings are a small, non-random sample; a full chronology could show a price link that this one cannot.
- Annual correlations miss lags: a bad harvest may lead to protest one or two years later.
- No correlation here identifies a cause.

## Load it

```python
from datasets import load_dataset

annual = load_dataset("Kukai-7/edo-rice-paper-protest", "annual", split="train").to_pandas()
uprisings = load_dataset("Kukai-7/edo-rice-paper-protest", "uprisings", split="train").to_pandas()

# Price shock in famine years against the rest
annual.groupby(annual.famine.notna()).rice_shock.mean()
```

## Configurations

### `annual` (default), 248 rows

| column | description |
|---|---|
| `year`, `era` | Calendar year and Japanese era name (first era of the year) |
| `rice_<place>_monme` | Price of one koku of rice in silver monme: Osaka (Dojima market, from 1701), Otsu and Banshu (market), Fukuchiyama, Bocho, Saga, Kumamoto (domain records), Hiroshima (merchant account books, from 1620) |
| `rice_<place>_ryo` | Price of one koku in gold ryo: Edo (shogunate records), Osaka (market), Nagoya, Shinshu (Ina), Aizu, Dewa (Shonai) (domain records) |
| `osaka_price_vs_trend` | Log Osaka price minus its centred 11-year median |
| `rice_shock`, `rice_shock_n_series` | Same deviation averaged over all silver series available that year, and how many there were |
| `summer_wet_share`, `summer_wet_z`, `n_stations` | June to August share of rainy days in the diaries; the z-score is computed station by station, then averaged, so diaries that note rain more often do not dominate |
| `famine` | Kan'ei (1640 to 1643), Kyoho (1732 to 1733), Horeki (1755 to 1757), Tenmei (1782 to 1788) or Tenpo (1833 to 1839) |
| `hansatsu_regime` | Shogunate policy on domain notes that year: first notes 1661, ban 1707, reauthorised 1730, new issues restricted 1759 |
| `hansatsu_domains_first_mentioned` | Domains whose earliest note in the sources dates from that year |
| `notable_uprisings` | Number of uprisings in the `uprisings` table that year |

### `uprisings`, 50 rows

`year`, `title_ja`, `name_en`, `province_ja`, `province_en`, `domain`, `latitude`, `longitude`, `cause`, `cause_group`, `summary_en`, `era`, `source_url`. One row per uprising, with the Japanese article it comes from.

### `hansatsu_domains`, 33 rows

`domain_ja`, `domain_en`, `province_ja`, `earliest_year_mentioned` (earliest year cited in the domain's paragraph, often the first issue), `latitude`, `longitude`, `coordinates_from` (Wikidata or set by hand), `source_url`.

### `weather_monthly`, 23,748 rows, and `stations`, 13 rows

For each station and month: days in the month, days recorded, and the number of days of each kind of weather noted in the diary (fine, partly cloudy, cloudy, shower, thunderstorm, heavy thunderstorm, little rain, rain, heavy rain, hail, snow shower, little snow, snow), plus `rain_days` and `snow_days`. `stations` gives position, diary type (official, private, farmhouse) and years covered.

### `correlations`, 6 rows

One row per pair of variables in the scatter-plot matrix: `x`, `y` and their labels, `n`, `pearson_r`, `r_squared`, `ci95_low`, `ci95_high` (Fisher z interval), `p_value` (two-sided t test), `spearman_rho`, `strength`, `direction`, and for annual series `n_changes`, `pearson_r_changes` and `p_value_changes`, the same correlation on year-on-year differences. Made by `correlations.py`.

## How it was built

1. **Rice prices.** Iwahashi Masaru's annual series (*Kinsei Nihon bukka-shi no kenkyū*, Ōhara Shinseisha, 1981, appendix table 1), compiled by Osamu Saito for the [Global Price and Income History Group](https://gpih.ucdavis.edu/Datafilelist.htm). Most are domain or account-book prices rather than market quotes; Osaka, Otsu and Banshu are market series.
2. **Weather.** Takehiko Mikami's *Historical Weather DataBase in Japan* (1993), distributed by NOAA's World Data Service for Paleoclimatology: daily weather written in domain, temple and household diaries, counted by month.
3. **Uprisings.** The list of notable uprisings in the Japanese Wikipedia article *一揆* and the pages of *Category:一揆*, 1603 to 1867, with duplicates merged. Province, domain, grievance and an English summary were written for this dataset from each article's lead; positions are the domain seat or district named there.
4. **Paper money.** The section *各藩の状況* of the Japanese Wikipedia article *藩札*, one row per domain; castle positions from Wikidata, or set by hand for twelve small domains.
5. **Annual panel.** Deviations from an 11-year centred median isolate short shocks from long inflation, including the currency debasements of the 1690s and the 1860s.
6. **Charts.** Python and Matplotlib; coastline from Natural Earth. The full pipeline is in [`code/`](./). The correlation figures come from `correlations.py`, which reads only the published Parquet files.

## Limitations

- **Fifty uprisings is a small sample.** Aoki Kōji's chronology counts about 3,200 peasant uprisings between 1590 and 1867, plus urban riots and village disputes. That chronology is not openly licensed, so this dataset keeps only the cases with their own Japanese Wikipedia article: the large, the famous and the well written-up. Read the uprising results as a sketch.
- **Notable is not random.** Famous uprisings are often the ones that ended with a martyr or a dispossessed lord, which favours tax disputes over hunger riots.
- **Hansatsu coverage is thin.** A Meiji survey of 1871 found notes in about 244 domains; the sources used here describe 33. The geographic pattern may partly reflect who wrote the articles.
- **Prices are nominal.** Silver and gold prices include the effect of recoinages; the trend deviation removes most of it, not all.
- **Diaries differ.** Each writer had their own threshold for "rain" (Nikko and Hachioji record far more rainy days than their neighbours), which is why the annual index is standardised by station.
- **Correlation only.** Nothing here identifies a causal effect.

## Credits and licences

- Rice prices: Iwahashi Masaru (1981), compiled by Osamu Saito, Global Price and Income History Group, UC Davis.
- Weather: Mikami, T. (1993), *Historical Weather Observations, Japan*, IGBP PAGES/World Data Center-A for Paleoclimatology Data Contribution Series 93-028, NOAA.
- Uprisings and hansatsu: Japanese Wikipedia, CC BY-SA 4.0 (the English summaries are derived from it and shared under the same terms); coordinates partly from Wikidata (CC0).
- Coastline: Natural Earth (public domain).
- This compilation, derived columns and charts: CC BY 4.0, except the Wikipedia-derived text fields (CC BY-SA 4.0).

## Related

- [Ming Crisis Atlas](https://huggingface.co/datasets/Kukai-7/ming-crisis-atlas), the companion dataset on Ming China, 1368 to 1644.
- [Tōkaidō 53 Stations](https://huggingface.co/datasets/Kukai-7/tokaido-53-stations), the great road of the same period.
- [GitHub: Kukai-7](https://github.com/Kukai-7)
