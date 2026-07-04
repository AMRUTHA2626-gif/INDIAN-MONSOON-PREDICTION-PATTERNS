import pandas as pd

# 1. Direct URL to NOAA's official raw ONI data text file
url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

# 2. Read the space-separated text file (UPDATED FIX)
df = pd.read_csv(url, sep=r'\s+')

# Clean up column names just in case of hidden leading/trailing spaces
df.columns = df.columns.str.strip()

# 3. Filter the data to include only years from 2000 to 2025
filtered_df = df[(df['YR'] >= 2000) & (df['YR'] <= 2025)]

# 4. Preview the filtered data to check your work
print(f"Successfully filtered data! Total rows: {len(filtered_df)}")
print("\nFirst 5 rows (Year 2000):")
print(filtered_df.head())
print("\nLast 5 rows (Year 2025):")
print(filtered_df.tail())

# 5. Export to a clean CSV file in your local directory
filtered_df.to_csv("noaa_enso_2000_2025.csv", index=False)
print("\nSaved as 'noaa_enso_2000_2025.csv'")