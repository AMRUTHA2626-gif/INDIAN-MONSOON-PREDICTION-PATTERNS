import os
import imdlib as imd

start_year = 2000
end_year = 2025
variable = 'rain'
download_dir = './imd_data'

os.makedirs(download_dir, exist_ok=True)

try:
    print("Downloading IMD data...")
    imd.get_data(variable, start_year, end_year,
                 fn_format='yearwise',
                 file_dir=download_dir)

    print("Download complete. Loading data...")

    data = imd.open_data(variable, start_year, end_year,
                         fn_format='yearwise',
                         file_dir=download_dir)

    grid_dataset = data.get_xarray()

    print("Success: Data loaded")

except Exception as e:
    print("ERROR occurred:")
    print(e)