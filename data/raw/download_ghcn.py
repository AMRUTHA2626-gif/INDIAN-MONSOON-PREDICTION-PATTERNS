import os
import urllib.request

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Station ID
station_id = "USW00094728"
url = f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/all/{station_id}.dly"
output_path = f"data/{station_id}.dly"

print(f"Downloading real GHCN data for station {station_id}...")
try:
    urllib.request.urlretrieve(url, output_path)
    print(f"Success! Raw GHCN file saved to {output_path}")

    input_file = output_path
    output_file = "data/USW00094728_2000_2025.dly"

    with open(input_file, "r") as fin, open(output_file, "w") as fout:
        for line in fin:
            year = int(line[11:15])  # Year is in columns 12–15

            if 2000 <= year <= 2025:
                fout.write(line)

    print("Filtered data saved to", output_file)

except Exception as e:
    print(f"Error downloading data: {e}")