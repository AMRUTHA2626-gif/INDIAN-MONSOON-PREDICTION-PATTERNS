import pandas as pd
import numpy as np
import os

# 1. Load data
df = pd.read_csv(
    "data/nina34.data",
    sep=r"\s+",
    skiprows=1,
    header=None,
    engine="python"
)

# 2. Handle missing values
df = df.replace(-99.99, np.nan)

# 3. Extract Year
years = pd.to_numeric(df.iloc[:, 0], errors="coerce")

# 4. Extract monthly values (Jan–Dec)
monthly = df.iloc[:, 1:13]
monthly = monthly.apply(pd.to_numeric, errors="coerce")

# 5. Name columns as months
monthly.columns = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# 6. Combine Year + monthly values
monthly.insert(0, "Year", years)

# 7. Convert wide → long format (MONTHLY DATA)
out = monthly.melt(
    id_vars="Year",
    var_name="Month",
    value_name="Nino34"
)

# 8. Ensure Year is numeric (CRITICAL FIX)
out["Year"] = pd.to_numeric(out["Year"], errors="coerce")

# 9. Filter 2000–2025
out = out[(out["Year"] >= 2000) & (out["Year"] <= 2025)]

# 10. Remove missing values
out = out.dropna(subset=["Nino34"])

# 11. Save output
os.makedirs("outputs", exist_ok=True)
out.to_csv("outputs/enso_monthly_2000_2025.csv", index=False)

# 12. Preview
print(out.head(12))
print(out.tail(12))
print("Done ✔ Monthly Niño 3.4 dataset created")