import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# 0. ENSURE OUTPUT DIRECTORY
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 1. LOAD ENSO DATA
# -----------------------------
enso = pd.read_csv("outputs/enso_monthly_2000_2025.csv")

enso["Year"] = pd.to_numeric(enso["Year"], errors="coerce")

# Handle Month safely (numeric OR string)
if enso["Month"].dtype == "object":
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    enso["Month"] = enso["Month"].map(month_map)

enso["Month"] = pd.to_numeric(enso["Month"], errors="coerce")

# -----------------------------
# 2. LOAD GHCN DATA
# -----------------------------
ghcn = pd.read_csv("outputs/ghcn_monthly_2000_2025.csv")

ghcn["Year"] = pd.to_numeric(ghcn["Year"], errors="coerce")
ghcn["Month"] = pd.to_numeric(ghcn["Month"], errors="coerce")

# -----------------------------
# 3. CLEAN DATA BEFORE MERGE
# -----------------------------
enso = enso.dropna(subset=["Year", "Month", "Nino34"])
ghcn = ghcn.dropna(subset=["Year", "Month"])

enso["Year"] = enso["Year"].astype(int)
enso["Month"] = enso["Month"].astype(int)

ghcn["Year"] = ghcn["Year"].astype(int)
ghcn["Month"] = ghcn["Month"].astype(int)

# -----------------------------
# 4. MERGE DATASETS
# -----------------------------
df = pd.merge(enso, ghcn, on=["Year", "Month"], how="inner")

print("Merged shape:", df.shape)

if df.empty:
    raise ValueError("Merged dataframe is empty. Check Year/Month alignment.")

# Drop remaining NaNs
df = df.dropna()

print(df.head())

# -----------------------------
# 5. CORRELATION ANALYSIS
# -----------------------------
corr_rain = df["Nino34"].corr(df["Rainfall_Monthly"])
print(f"\nENSO vs Rainfall Correlation: {corr_rain:.3f}")

# -----------------------------
# 6. CREATE TIME INDEX
# -----------------------------
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))
df = df.sort_values("Date")

# -----------------------------
# 7. TIME SERIES PLOT
# -----------------------------
plt.figure(figsize=(14, 6))

plt.plot(df["Date"], df["Nino34"], label="Niño 3.4", color="red")
plt.plot(df["Date"], df["Rainfall_Monthly"], label="Rainfall", color="blue")

plt.title("Monthly ENSO vs Rainfall (2000–2025)")
plt.legend()
plt.tight_layout()

plt.savefig("outputs/enso_rainfall_monthly_timeseries.png", dpi=300)
plt.show()

# -----------------------------
# 8. SCATTER PLOT
# -----------------------------
plt.figure(figsize=(6, 5))

sns.scatterplot(data=df, x="Nino34", y="Rainfall_Monthly")

plt.title("ENSO vs Rainfall Relationship")
plt.tight_layout()

plt.savefig("outputs/enso_rainfall_scatter.png", dpi=300)
plt.show()

# -----------------------------
# 9. ROLLING CORRELATION
# -----------------------------
window = 12

df["Rolling_Corr"] = (
    df["Nino34"].rolling(window).corr(df["Rainfall_Monthly"])
)

plt.figure(figsize=(14, 6))

plt.plot(df["Date"], df["Rolling_Corr"], color="purple")
plt.axhline(0, color="black", linestyle="--")

plt.title(f"{window}-Month Rolling Correlation (ENSO vs Rainfall)")
plt.xlabel("Date")
plt.ylabel("Correlation")

plt.tight_layout()
plt.savefig("outputs/enso_rainfall_rolling_correlation.png", dpi=300)
plt.show()