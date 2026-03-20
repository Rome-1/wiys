# Chicago Residential Property Composition Analysis

This analysis was completed after the paper but explores a dimension that is
both interesting and relevant to the work: the physical composition of
Chicago's residential housing stock by community area.

Using the Cook County Assessor's archived residential property characteristics
dataset (~2M records, 2018-2019 tax years), we visualize how wall material,
roof material, repair condition, and property age vary across Chicago's 77
community areas.

## Data Source

**Cook County Assessor — Archived Residential Property Characteristics (05-11-2022)**
https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z/about_data

The raw CSV (~158MB, ~2M rows) is not checked into the repo. To download it,
run the included fetch script which pulls data from the Socrata Open Data API:

```bash
cd analysis
python3 fetch_data.py
```

This requires only the Python standard library and takes a few minutes (40
paginated API calls at 50k rows each). No authentication is needed — the
dataset is public.

A community area boundary GeoJSON (~2MB) is also fetched at visualization
time from the City of Chicago data portal.

## Reproducing the Figures

After downloading the data:

```bash
pip install pandas geopandas matplotlib seaborn shapely
python3 visualize.py
```

Outputs go to `figures/`.

## Key Findings

- **Wall material**: Masonry dominates Chicago (60%), but with strong geographic
  variation — near-downtown and south side neighborhoods are heavily masonry,
  while far-south and northwest areas are predominantly wood.
- **Roof material**: Shingle/asphalt covers 82% of properties. Tar & gravel
  (16%) concentrates in denser, older neighborhoods near downtown.
- **Repair condition**: 98.6% rated "Average," but below-average repair clusters
  on the south and west sides (Washington Park 7.1%, Grand Boulevard 5.2%).
- **Age**: Median property age is 93 years. The inner ring (Lower West Side,
  Bridgeport, West Town) has the oldest stock (120-130 yr medians), while
  post-WWII far-south/southwest areas are youngest (~65 yrs).
