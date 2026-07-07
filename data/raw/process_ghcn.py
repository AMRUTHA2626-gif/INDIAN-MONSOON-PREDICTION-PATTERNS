import glob
import os
import numpy as np
import pandas as pd

# 1. LOAD DATA (FIXED WIDTH SLICING)

dly_files = glob.glob("data/*.dly")
if not dly_files:
    raise FileNotFoundError(
        "No .dly file found in 'data/' directory. Run download_ghcn.py first."
    )

file_path = dly_files[0]
print(f"Processing raw GHCN file: {file_path}")

# GHCN .dly structure: Station (11), Year (4), Month (2), Element (4), then 31 days of (Value(5)+Flags(3))
col_specs = [
    (0, 11),  # Station ID
    (11, 15),  # Year
    (15, 17),  # Month
    (17, 21),  # Element (PRCP, TMAX, TMIN, etc.)
]
for i in range(31):
    start = 21 + i * 8
    col_specs.append((start, start + 5))

col_names = ["STATION", "YEAR", "MONTH", "ELEMENT"] + [
    f"DAY_{i+1}" for i in range(31)
]

# Read fixed width file
df_raw = pd.read_fwf(
    file_path, widths=[w[1] - w[0] for w in col_specs], names=col_names
)

# Filter down to target parameters
required_elements = ["PRCP", "TMAX", "TMIN"]
df_filtered = df_raw[df_raw["ELEMENT"].isin(required_elements)].copy()

# 2. MELT & RESHAPE TO LONG FORMAT

df_long = df_filtered.melt(
    id_vars=["STATION", "YEAR", "MONTH", "ELEMENT"],
    value_vars=[f"DAY_{i+1}" for i in range(31)],
    var_name="DAY",
    value_name="VALUE",
)

df_long["DAY"] = df_long["DAY"].str.replace("DAY_", "").astype(int)

# Create accurate date rows
df_long["DATE"] = pd.to_datetime(
    df_long[["YEAR", "MONTH", "DAY"]], errors="coerce"
)
df_long = df_long.dropna(subset=["DATE"])

# Pivot back so PRCP, TMAX, TMIN become distinct columns
df_pivot = df_long.pivot_table(
    index=["DATE", "YEAR"], columns="ELEMENT", values="VALUE", aggfunc="first"
).reset_index()

df_pivot.columns.name = None

# Ensure all columns exist
for col in required_elements:
    if col not in df_pivot.columns:
        df_pivot[col] = np.nan

# 3. CLEAN MISSING VALUES & ENFORCE NUMERIC TYPES (THE FIX)
# Replace GHCN string or numeric missing flags with NaN
df_pivot.replace([-9999, "-9999", " -999"], np.nan, inplace=True)

# CRITICAL FIX: Explicitly convert columns to numeric, turning any rogue string data into NaN
for col in required_elements:
    df_pivot[col] = pd.to_numeric(df_pivot[col], errors="coerce")

# Convert tenths of mm/degrees to standard mm and Celsius
df_pivot["PRCP"] = df_pivot["PRCP"] / 10.0
df_pivot["TMAX"] = df_pivot["TMAX"] / 10.0
df_pivot["TMIN"] = df_pivot["TMIN"] / 10.0

# 4. FILTER DATA FROM 2000 TO 2025

df_pivot = df_pivot[
    (df_pivot["YEAR"] >= 2000) &
    (df_pivot["YEAR"] <= 2025)
].copy()

# Extract month from DATE
df_pivot["MONTH"] = df_pivot["DATE"].dt.month

# 5. MONTHLY AGGREGATION

monthly = (
    df_pivot.groupby(["YEAR", "MONTH"])
    .agg({
        "PRCP": "sum",      # Total monthly rainfall (mm)
        "TMAX": "mean",     # Average monthly maximum temperature (°C)
        "TMIN": "mean"      # Average monthly minimum temperature (°C)
    })
    .reset_index()
)

monthly.rename(
    columns={
        "YEAR": "Year",
        "MONTH": "Month",
        "PRCP": "Rainfall_Monthly",
        "TMAX": "TMAX_Monthly",
        "TMIN": "TMIN_Monthly",
    },
    inplace=True,
)

# 6. SAVE OUTPUT

os.makedirs("outputs", exist_ok=True)

monthly.to_csv("outputs/ghcn_monthly_2000_2025.csv", index=False)

print("\nFinal Monthly Dataset Preview:")
print(monthly.head())
print(monthly.tail())

print(f"\nNumber of monthly records: {len(monthly)}")
print("\nDone: GHCN monthly dataset (2000-2025) created successfully.")