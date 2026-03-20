#!/usr/bin/env python3
"""Download Cook County residential property data via SODA API."""
import urllib.request
import json
import csv
import os

DATASET_ID = "bcnq-qi2z"
BASE_URL = f"https://datacatalog.cookcountyil.gov/resource/{DATASET_ID}.json"

# Fields we need
FIELDS = [
    "pin", "ext_wall", "roof_cnst", "gar2_cnst", "repair_cnd", "age",
    "neigborhood_code_mapping_", "town_code", "nbhd",
    "centroid_x", "centroid_y", "bldg_sf", "class", "tax_year"
]

SELECT = ",".join(FIELDS)
LIMIT = 50000
OUTPUT = "/home/rome/gt/wiys/crew/alice/analysis/properties.csv"

def fetch_all():
    offset = 0
    all_rows = []
    while True:
        url = f"{BASE_URL}?$select={SELECT}&$limit={LIMIT}&$offset={offset}&$order=pin"
        print(f"Fetching offset={offset}...")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
        if not data:
            break
        all_rows.extend(data)
        print(f"  Got {len(data)} rows (total: {len(all_rows)})")
        if len(data) < LIMIT:
            break
        offset += LIMIT

    # Write CSV
    if all_rows:
        keys = FIELDS
        with open(OUTPUT, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            w.writerows(all_rows)
        print(f"Wrote {len(all_rows)} rows to {OUTPUT}")

if __name__ == "__main__":
    fetch_all()
