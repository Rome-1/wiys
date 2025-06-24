# What's In Your Soil? Data Analysis

This repository contains the code for the paper "What's In Your Soil? A Citywide Investigation of the Importance of Soil Lead for Elevated Blood Lead Levels in Chicago".

## Setup Instructions

Download R and RStudio from [CRAN (R Project)](https://cran.r-project.org/) and [Posit (RStudio Downloads)](https://posit.co/downloads/), respectively, if not already on your device.

Next, download the data sources listed below. 

Third, go into the R file:
- Update the root path to the location of this repository
- Run the commented-out `install.packages` line if you don't have any of the required packages
- Click 'Run all chunks'

## Data sources

### Provided

- Soil lead data with building ages. The sampling and analysis was conducted by us. Building ages were ported over from the Cook County Assessor's Office; the data necessary to replicate this step is not included because it requires precise latitude and longitude data which has been de-identified. 
- Chicago Community area boundaries geojson. Source: [Chicago Community Area Boundaries GeoJSON](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-Map/cauq-8yn6)
- Chicago Census tract boundaries geojson. Source: [Chicago Census Tract Boundaries GeoJSON](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik)
- Industrial Corridors data. Source: [Industrial Corridors Data](https://data.cityofchicago.org/Community-Economic-Development/Boundaries-Industrial-Corridors-current-/e6xh-nr8w) (download as a CSV, change the name to remove the timestamp at the end (IndustrialCorridor_Jan2013.csv) and place the file in the data/landuse folder)
- Parks data. Source: [Parks Data](https://data.cityofchicago.org/Parks-Recreation/CPD_Parks/ejsh-fztr/about_data) (download as a CSV, change the name to remove the timestamp at the end (CPD_Parks.csv) and place the file in the data/landuse folder)

### Not Provided (Available Upon Request)

To access the Chicago Department of Public Health annual elevated blood Lead level rates by census tract from 1995-2015, submit a request here: [CDPH Data Request Form](https://www.chicago.gov/city/en/depts/cdph/provdrs/health_data_and_reports/svcs/data-request-form.html) 

A less complete dataset for 1999 to 2013 (which will require some small configurations to the code) can be found publicly on the Chicago Data Portal here: [Public Health Statistics (1999-2013)](https://data.cityofchicago.org/Health-Human-Services/Public-Health-Statistics-Screening-for-elevated-bl/v2z5-jyrq/about_data).

### Not provided (Publicly Available)

Link: [Census Data (DP3 2000)](https://data.census.gov/chart?q=U.S.+Census+Bureau,+Census+2000+Summary+File+4+household+income+DP3_C112&g=040XX00US17$0500000_050XX00US17031,17031$1400000_160XX00US1714000_860XX00US740HH)

Download the "DP3 | Profile of Selected Economic Characteristics: 2000" > "DEC Summary File 4 Demographic Profile", unzip the file, and move the data file (DECENNIALDPSF42000.DP3-Data.csv) to `data/socioecon`.

- Search Term if link breaks: U.S. Census Bureau, Census 2000 Summary File 4 household income DP3_C112
- Region: Census Tracts > Illinois > All Census Tracts within Cook County

---

Link: [Census Data (S1903 2015)](https://data.census.gov/chart/ACSST5Y2015.S1903?q=ACSST5Y2015.S1903&g=050XX00US17031$1400000_160XX00US1714000_860XX00US740HH)

Download the "S1903 | MEDIAN INCOME IN THE PAST 12 MONTHS (IN 2015 INFLATION-ADJUSTED DOLLARS)" > "ACS 5-Year Estimates Subject Tables", unzip the file, and move the data file (ACSST5Y2015.S1903-Data.csv) to `data/socioecon`.

- Search Term if link breaks: ACSST5Y2015.S1903
- Region: Census Tracts > Illinois > All Census Tracts within Cook County

---

Link: [Census Data (DP1 2000)](https://data.census.gov/chart/DECENNIALDPSF42000.DP1?q=DECENNIALDPSF42000.DP1&g=050XX00US17031$1400000_160XX00US1714000_860XX00US740HH)

Download the "DP1 DP1Profile of General Demographic Characteristics: 2000" > "DEC Summary File 4 Demographic Profile", unzip the file, and move the data file (DECENNIALDPSF42000.DP1-Data.csv) to `data/socioecon`.

- Search Term if link breaks: DECENNIALDPSF42000.DP1
- Region: Census Tracts > Illinois > All Census Tracts within Cook County

---


Link: [Census Data (S2502 2015)](https://data.census.gov/chart?q=ACSST5Y2015.S2502&g=050XX00US17031$1400000_160XX00US1714000_860XX00US740HH)

Download the "S2502DEMOGRAPHIC CHARACTERISTICS FOR OCCUPIED HOUSING UNITS" > "ACS 5-Year Estimates Subject Tables", unzip the file, and move the data file (ACSST5Y2015.S2502-Data.csv) to `data/socioecon`.

- Search Term if link breaks: ACSST5Y2015.S2502
- Region: Census Tracts > Illinois > All Census Tracts within Cook County

---

The Enviroaltas data has been updated since the analysis was performed. The data used in this study (CIL_metrics_Apr2020_FGDB) is available for download (approx. 1 GB): [EnviroAtlas Data (CIL_metrics_Apr2020_FGDB.zip)](https://gaftp.epa.gov/epadatacommons/ORD/EnviroAtlas/CIL_metrics_Apr2020_FGDB.zip) with details [EnviroAtlas Details (Archived)](https://web.archive.org/web/20250215235237/https://catalog.data.gov/dataset/enviroatlas-chicago-il-tree-cover-configuration-and-connectivity2). The more recent dataset (not used) is available: [EnviroAtlas (Newer Dataset)](https://catalog.data.gov/dataset/enviroatlas-chicago-il-tree-cover-configuration-and-connectivity3)
Download the file, extract the zip, and place the resulting folder in the data folder (e.g. `data/CIL_metrics_Apr2020_FGDB/Community_CIL.gdb/...`).

### Citations

- CDP. (2024a). *Boundaries - industrial corridors (current)*. Retrieved from [City of Chicago Data Portal](https://data.cityofchicago.org/Community-Economic-Development/Boundaries-Industrial-Corridors-current-/e6xh-nr8w) (Accessed: 2025-01-21).
- CDP. (2024b). *Parks - chicago park district park boundaries (current)*. Retrieved from [City of Chicago Data Portal](https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr) (Accessed: 2025-01-21).
- CDP. (2025). *Boundaries - neighborhoods*. Retrieved from [City of Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9) (Accessed: 2025-01-21).
- Chicago Department of Public Health. (2025). *Data request and data feedback form*. Retrieved from [CDPH](https://www.chicago.gov/city/en/depts/cdph/provdrs/health_data_and_reports/svcs/data-request-form.html) (Accessed: 2025-04-21).
- CDP. (2010). *Census tracts - 2010*. Retrieved from [City of Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik) (Accessed: 2025-01-21).
- EPA (U.S. Environmental Protection Agency). (2019). *EnviroAtlas - Chicago, IL - tree cover, configuration, and connectivity*. Retrieved from [Data.gov](https://catalog.data.gov/dataset/enviroatlas-chicago-il-tree-cover-configuration-and-connectivity2).
- U.S. Census Bureau. (2000a). *Census 2000 summary file 4 (SF4) - DP1 (demographic profile 1)*. Retrieved from [census.gov](https://www.census.gov/data/datasets/2000/dec/summary-file-4.html) (Source: U.S. Census Bureau, Census 2000 Summary File 4, Matrices PCT1, PCT3, PCT4, PCT8, PCT9, PCT10, PCT11, PCT12, PCT14, PCT15, PCT23, PCT26, HCT2, and HCT7.).
- U.S. Census Bureau. (2000b). *Census 2000 summary file 4 (SF4) - DP3 (economic profile)*. Retrieved from [census.gov](https://www.census.gov/data/datasets/2000/dec/summary-file-4.html) (Source: U.S. Census Bureau, Census 2000 Summary File 4, DP3 Data.).
- U.S. Census Bureau. (2015a). *American Community Survey (ACS) 5-year estimates (2015) - table S1903: Median household income*. Retrieved from [census.gov](https://www.census.gov/programs-surveys/acs) (Source: U.S. Census Bureau, ACS 5-Year Estimates (2015), Table S1903.).
- U.S. Census Bureau. (2015b). *American Community Survey (ACS) 5-year estimates (2015) - table S2502: Demographic characteristics for occupied housing units*. Retrieved from [census.gov](https://www.census.gov/programs-surveys/acs) (Source: U.S. Census Bureau, ACS 5-Year Estimates (2015), Table S2502.).
- U.S. Census Bureau. (2025). *Geocoding services API*. Retrieved from [census.gov](https://geocoding.geo.census.gov/geocoder/geographies/coordinates).