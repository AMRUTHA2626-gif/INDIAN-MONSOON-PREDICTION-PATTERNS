import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD ENSO MONTHLY DATA

enso = pd.read_csv("outputs/enso_monthly_2000_2025.csv")

enso["Year"] = pd.to_numeric(enso["Year"], errors="coerce")

# Convert month names → numbers
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
enso["Month"] = enso["Month"].map(month_map)


# 2. LOAD GHCN MONTHLY DATA

ghcn = pd.read_csv("outputs/ghcn_monthly_2000_2025.csv")

# Ensure numeric
ghcn["Year"] = pd.to_numeric(ghcn["Year"], errors="coerce")
ghcn["Month"] = pd.to_numeric(ghcn["Month"], errors="coerce")


# 3. MERGE ON YEAR + MONTH

df = pd.merge(
    enso,
    ghcn,
    on=["Year", "Month"],
    how="inner"
)

# Drop missing values
df = df.dropna()

print("Merged shape:", df.shape)
print(df.head())


# 4. CORRELATION (MONTHLY)

corr_rain = df["Nino34"].corr(df["Rainfall_Monthly"])
print(f"\nMonthly ENSO vs Rainfall Correlation: {corr_rain:.3f}")


# 5. TIME SERIES PLOT

df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

plt.figure(figsize=(14,6))

plt.plot(df["Date"], df["Nino34"], label="Niño 3.4", color="red")
plt.plot(df["Date"], df["Rainfall_Monthly"], label="Rainfall (mm)", color="blue")

plt.title("Monthly ENSO vs Rainfall (2000–2025)")
plt.legend()
plt.tight_layout()

plt.savefig("outputs/enso_rainfall_monthly_timeseries.png")
plt.show()


# 6. SCATTER PLOT (RELATIONSHIP)

plt.figure(figsize=(6,5))
sns.scatterplot(data=df, x="Nino34", y="Rainfall_Monthly")
plt.title("ENSO vs Rainfall (Monthly)")
plt.tight_layout()

plt.savefig("outputs/enso_rainfall_scatter.png")
plt.show()

# 7. ROLLING CORRELATION (12-MONTH WINDOW)

# Set window size (you can adjust: 6, 12, 24 months)
window = 12

df = df.sort_values("Date")

df["Rolling_Corr"] = (
    df["Nino34"]
    .rolling(window)
    .corr(df["Rainfall_Monthly"])
)

plt.figure(figsize=(14,6))

plt.plot(df["Date"], df["Rolling_Corr"], color="purple", linewidth=2)

plt.axhline(0, color="black", linestyle="--", linewidth=1)

plt.title(f"{window}-Month Rolling Correlation: ENSO vs Rainfall")
plt.ylabel("Correlation")
plt.xlabel("Date")

plt.tight_layout()
plt.savefig("outputs/enso_rainfall_rolling_correlation.png")
plt.show()