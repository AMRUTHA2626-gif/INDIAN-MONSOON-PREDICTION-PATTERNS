import pandas as pd
import os

# -----------------------------------------
# Read NOAA Nino3.4 data
# -----------------------------------------
df = pd.read_csv(
    "data/nina34.data",
    sep=r"\s+",
    skiprows=1,
    header=None,
    engine="python"
)

# -----------------------------------------
# Assign column names
# -----------------------------------------
df.columns = [
    "Year",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# -----------------------------------------
# CLEAN: convert Year to numeric FIRST
# -----------------------------------------
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# drop bad rows (if any header garbage exists)
df = df.dropna(subset=["Year"])

df["Year"] = df["Year"].astype(int)

# -----------------------------------------
# NOW filter safely
# -----------------------------------------
df = df[(df["Year"] >= 2000) & (df["Year"] <= 2025)]

# -----------------------------------------
# Convert wide → long (monthly format)
# -----------------------------------------
monthly_df = df.melt(
    id_vars="Year",
    var_name="Month",
    value_name="Nino34"
)

# -----------------------------------------
# Month mapping
# -----------------------------------------
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

monthly_df["Month"] = monthly_df["Month"].map(month_map)

# -----------------------------------------
# Convert Nino34 to numeric
# -----------------------------------------
monthly_df["Nino34"] = pd.to_numeric(monthly_df["Nino34"], errors="coerce")

# -----------------------------------------
# Sort properly
# -----------------------------------------
monthly_df = monthly_df.sort_values(["Year", "Month"]).reset_index(drop=True)

# -----------------------------------------
# Save output
# -----------------------------------------
os.makedirs("outputs", exist_ok=True)

monthly_df.to_csv(
    "outputs/enso_monthly_2000_2025.csv",
    index=False
)

# -----------------------------------------
# Verify
# -----------------------------------------
print("Shape:", monthly_df.shape)
print(monthly_df.head(12))
print(monthly_df.tail(12))