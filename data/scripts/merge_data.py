import os
import pandas as pd

# Load your annual outputs
enso_df = pd.read_csv("outputs/enso_annual.csv")
ghcn_df = pd.read_csv("outputs/ghcn_annual.csv")

# Ensure column names match for merging (Case-sensitive check)
enso_df.rename(columns={"YEAR": "Year"}, errors="ignore", inplace=True)
ghcn_df.rename(columns={"YEAR": "Year"}, errors="ignore", inplace=True)

# CRITICAL FIX: Convert 'Year' in both dataframes to integers to resolve type mismatch
enso_df["Year"] = pd.to_numeric(enso_df["Year"], errors="coerce")
ghcn_df["Year"] = pd.to_numeric(ghcn_df["Year"], errors="coerce")

# Drop any rows where 'Year' couldn't be converted properly (if any header text snuck in)
enso_df = enso_df.dropna(subset=["Year"])
ghcn_df = ghcn_df.dropna(subset=["Year"])

# Now explicitly cast them to integer type
enso_df["Year"] = enso_df["Year"].astype(int)
ghcn_df["Year"] = ghcn_df["Year"].astype(int)

# Merge on Year (Inner join keeps years where both datasets have values)
merged_df = pd.merge(enso_df, ghcn_df, on="Year", how="inner")

# Save to the final analytics folder
os.makedirs("outputs", exist_ok=True)
merged_df.to_csv("outputs/enso_ghcn_merged.csv", index=False)

print("Master dataset created successfully at 'outputs/enso_ghcn_merged.csv'!")
print(merged_df.head())