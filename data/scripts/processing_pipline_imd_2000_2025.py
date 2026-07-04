import imdlib as imd
import pandas as pd

# 1. LOAD IMD DATA (2000–2025)

start_year = 2000
end_year = 2025
variable = 'rain'
download_dir = './imd_data'

data = imd.open_data(variable, start_year, end_year,
                     fn_format='yearwise',
                     file_dir=download_dir)

grid_dataset = data.get_xarray()

# 2. EXTRACT RAINFALL VARIABLE
rain = grid_dataset['rain']

grid_dataset = data.get_xarray()
rain = grid_dataset['rain']

# Clean out IMD missing value flags before taking the mean
rain = rain.where(rain != -999.0)

# 3. CONVERT GRID → INDIA AVERAGE
#    (removes lat/lon complexity)

india_rain = rain.mean(dim=['lat', 'lon'])

# 4. CONVERT TO DATAFRAME

df = india_rain.to_dataframe().reset_index()

# 5. CLEAN TIME COLUMN

df['time'] = pd.to_datetime(df['time'])

# 6. FILTER 2000–2025

df = df[(df['time'].dt.year >= 2000) &
        (df['time'].dt.year <= 2025)]

# 7. EXTRACT MONSOON (JJAS)

df_monsoon = df[df['time'].dt.month.isin([6, 7, 8, 9])]

# 8. YEARLY MONSOON TOTAL

monsoon_yearly = df_monsoon.groupby(
    df_monsoon['time'].dt.year
)['rain'].sum().reset_index()

monsoon_yearly.columns = ['Year', 'Monsoon_Rainfall']

# 9. CALCULATE ANOMALY

baseline = monsoon_yearly['Monsoon_Rainfall'].mean()
monsoon_yearly['Anomaly'] = monsoon_yearly['Monsoon_Rainfall'] - baseline


# 10. SAVE FINAL DATASET

output_file = "imd_monsoon_2000_2025.csv"
monsoon_yearly.to_csv(output_file, index=False)

print("DONE ✔")
print("Saved:", output_file)
print(monsoon_yearly.head())