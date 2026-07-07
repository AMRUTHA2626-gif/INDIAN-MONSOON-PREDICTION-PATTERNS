import os
import pandas as pd

# =====================================================
# File Paths
# =====================================================
ENSO_FILE = "outputs/enso_monthly_2000_2025.csv"
GHCN_FILE = "outputs/ghcn_monthly_2000_2025.csv"
OUTPUT_FILE = "outputs/enso_ghcn_monthly_2000_2025.csv"

# =====================================================
# Check files exist
# =====================================================
if not os.path.exists(ENSO_FILE):
    raise FileNotFoundError(f"ENSO file not found:\n{ENSO_FILE}")

if not os.path.exists(GHCN_FILE):
    raise FileNotFoundError(f"GHCN file not found:\n{GHCN_FILE}")

# =====================================================
# Read files
# =====================================================
enso_df = pd.read_csv(ENSO_FILE)
ghcn_df = pd.read_csv(GHCN_FILE)

print("=" * 60)
print("ENSO Columns")
print(enso_df.columns.tolist())

print("=" * 60)
print("GHCN Columns")
print(ghcn_df.columns.tolist())

# =====================================================
# Standardize column names
# =====================================================
enso_df.columns = enso_df.columns.str.strip()
ghcn_df.columns = ghcn_df.columns.str.strip()

rename_map = {
    "YEAR": "Year",
    "year": "Year",
    "MONTH": "Month",
    "month": "Month"
}

enso_df.rename(columns=rename_map, inplace=True)
ghcn_df.rename(columns=rename_map, inplace=True)

# =====================================================
# Check required columns
# =====================================================
required = ["Year", "Month"]

for col in required:
    if col not in enso_df.columns:
        raise ValueError(f"'{col}' missing in ENSO file.")

    if col not in ghcn_df.columns:
        raise ValueError(f"'{col}' missing in GHCN file.")

# =====================================================
# Clean Year & Month
# =====================================================
for df in [enso_df, ghcn_df]:

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Month"] = pd.to_numeric(df["Month"], errors="coerce")

    df.dropna(subset=["Year", "Month"], inplace=True)

    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)

# =====================================================
# Keep only 2000-2025
# =====================================================
enso_df = enso_df[
    (enso_df["Year"] >= 2000) &
    (enso_df["Year"] <= 2025)
]

ghcn_df = ghcn_df[
    (ghcn_df["Year"] >= 2000) &
    (ghcn_df["Year"] <= 2025)
]

# =====================================================
# Sort
# =====================================================
enso_df = enso_df.sort_values(["Year", "Month"])
ghcn_df = ghcn_df.sort_values(["Year", "Month"])

# =====================================================
# Diagnostics BEFORE merge
# =====================================================
print("\n")
print("=" * 60)
print("ENSO Dataset")

print(enso_df.head())
print(enso_df.tail())

print("\nRows:", len(enso_df))

print("\nUnique Years:")
print(enso_df["Year"].min(), "to", enso_df["Year"].max())

print("\nMonths:")
print(sorted(enso_df["Month"].unique()))

print("\n")
print("=" * 60)
print("GHCN Dataset")

print(ghcn_df.head())
print(ghcn_df.tail())

print("\nRows:", len(ghcn_df))

print("\nUnique Years:")
print(ghcn_df["Year"].min(), "to", ghcn_df["Year"].max())

print("\nMonths:")
print(sorted(ghcn_df["Month"].unique()))

# =====================================================
# Merge
# =====================================================
merged_df = pd.merge(
    enso_df,
    ghcn_df,
    on=["Year", "Month"],
    how="inner"
)

# =====================================================
# If merge failed, diagnose
# =====================================================
if merged_df.empty:

    print("\n")
    print("=" * 60)
    print("NO MATCH FOUND")

    debug = pd.merge(
        enso_df,
        ghcn_df,
        on=["Year", "Month"],
        how="outer",
        indicator=True
    )

    print(debug["_merge"].value_counts())

    print("\nSample unmatched rows:")
    print(debug[debug["_merge"] != "both"].head(20))

    raise ValueError(
        "\nMerge produced ZERO rows.\n"
        "Inspect the diagnostics above."
    )

# =====================================================
# Replace missing codes
# =====================================================
merged_df.replace(
    [-99.99, -9999, -999.9],
    pd.NA,
    inplace=True
)

# =====================================================
# Save
# =====================================================
os.makedirs("outputs", exist_ok=True)

merged_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n")
print("=" * 60)
print("SUCCESS")
print(f"Rows : {len(merged_df)}")
print(f"Columns : {len(merged_df.columns)}")
print(f"Saved : {OUTPUT_FILE}")

print("\nPreview")
print(merged_df.head())

print("\nLast Rows")
print(merged_df.tail())