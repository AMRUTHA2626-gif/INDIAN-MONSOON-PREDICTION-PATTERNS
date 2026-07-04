import pandas as pd

# NOAA GHCN Daily station ID
STATION_ID = "USW00094728"   # Replace with your station ID

# NOAA GHCN Daily URL
url = f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/all/{STATION_ID}.csv"

# Column names from NOAA documentation
columns = [
    "ID", "DATE", "ELEMENT", "VALUE",
    "MFLAG", "QFLAG", "SFLAG", "OBS_TIME"
]

# Read data
df = pd.read_csv(url, names=columns)

# Convert DATE to datetime
df["DATE"] = pd.to_datetime(df["DATE"], format="%Y%m%d")

# Keep only years 2000–2025
df = df[(df["DATE"].dt.year >= 2000) &
        (df["DATE"].dt.year <= 2025)]

# Keep rainfall and temperature observations
df = df[df["ELEMENT"].isin(["PRCP", "TMAX", "TMIN"])]

# Convert units
# PRCP: tenths of mm -> mm
# TMAX/TMIN: tenths of °C -> °C
df.loc[df["ELEMENT"] == "PRCP", "VALUE"] /= 10
df.loc[df["ELEMENT"].isin(["TMAX", "TMIN"]), "VALUE"] /= 10

# Convert to wide format
ghcn = (
    df.pivot_table(
        index="DATE",
        columns="ELEMENT",
        values="VALUE",
        aggfunc="first"
    )
    .reset_index()
)

print(ghcn.head())

# Save
ghcn.to_csv("ghcn_2000_2025.csv", index=False)

print("Saved as 'ghcn_2000_2025.csv'")