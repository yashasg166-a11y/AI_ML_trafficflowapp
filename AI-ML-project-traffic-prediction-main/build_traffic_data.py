"""
build_traffic_data.py
=====================
Reads the Metro_Interstate_Traffic_Volume CSV, computes REAL average
traffic volumes per hour × day_type (Weekday / Weekend), normalises
them to a 0–100 intensity scale, and saves the result as
traffic_data.json which app.py uses at runtime.

Run once:  python build_traffic_data.py
"""

import os
import json
import csv
from datetime import datetime

# ── Locate the CSV ────────────────────────────────────────────────────────────
CANDIDATES = [
    os.path.join("archive (1)", "Metro_Interstate_Traffic_Volume_modified.csv"),
    os.path.join("archive (2)", "Metro_Interstate_Traffic_Volume.csv"),
]

csv_path = None
for c in CANDIDATES:
    if os.path.exists(c):
        csv_path = c
        break

if csv_path is None:
    raise FileNotFoundError("Could not find the traffic CSV. Make sure the archive folders exist.")

print(f"Using CSV: {csv_path}")

# ── Parse & accumulate volumes ────────────────────────────────────────────────
# Structure: sums[day_type_str][hour] = [list of traffic volumes]
sums = {
    "Weekday": {h: [] for h in range(24)},
    "Weekend": {h: [] for h in range(24)},
}

modified_csv = "modified" in csv_path.lower()

with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse traffic volume (skip blanks)
        vol_raw = row.get("traffic_volume", "").strip()
        if not vol_raw:
            continue
        try:
            volume = float(vol_raw)
        except ValueError:
            continue

        # Determine day_type and hour
        if modified_csv:
            # date_time format: "10/2/12 9:00"  day_type column: "Weekday"/"Weekend"
            dt_str = row.get("date_time", "").strip()
            day_type = row.get("day_type", "").strip()
            if day_type not in ("Weekday", "Weekend"):
                continue
            try:
                dt = datetime.strptime(dt_str, "%m/%d/%y %H:%M")
                hour = dt.hour
            except ValueError:
                continue
        else:
            # date_time format: "2012-10-02 09:00:00"  no day_type column – derive from weekday
            dt_str = row.get("date_time", "").strip()
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                hour = dt.hour
                day_type = "Weekend" if dt.weekday() >= 5 else "Weekday"
            except ValueError:
                continue

        sums[day_type][hour].append(volume)

# ── Compute averages ──────────────────────────────────────────────────────────
avg = {}
for dt_key in ("Weekday", "Weekend"):
    avg[dt_key] = {}
    for h in range(24):
        vals = sums[dt_key][h]
        avg[dt_key][h] = sum(vals) / len(vals) if vals else 0.0

# ── Normalise to 0–100 ────────────────────────────────────────────────────────
all_avgs = [v for dt_key in avg for v in avg[dt_key].values()]
min_v = min(all_avgs)
max_v = max(all_avgs)

def norm(v):
    """Scale raw average to 2–98 range."""
    if max_v == min_v:
        return 50
    return round(2 + (v - min_v) / (max_v - min_v) * 96, 2)

normalised = {}
for dt_key in ("Weekday", "Weekend"):
    normalised[dt_key] = {str(h): norm(avg[dt_key][h]) for h in range(24)}

# ── Save ──────────────────────────────────────────────────────────────────────
out = {
    "source": csv_path,
    "rows_processed": int(sum(len(sums[d][h]) for d in sums for h in range(24))),
    "intensities": normalised,
}

with open("traffic_data.json", "w") as f:
    json.dump(out, f, indent=2)

print("\n✅  traffic_data.json written successfully.\n")
print("Sample — Weekday intensities by hour:")
for h in range(24):
    bar = "█" * int(normalised["Weekday"][str(h)] / 5)
    print(f"  {h:02d}:00  {normalised['Weekday'][str(h)]:5.1f}  {bar}")
print()
print("Sample — Weekend intensities by hour:")
for h in range(24):
    bar = "█" * int(normalised["Weekend"][str(h)] / 5)
    print(f"  {h:02d}:00  {normalised['Weekend'][str(h)]:5.1f}  {bar}")
