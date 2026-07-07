import requests

url = "https://psl.noaa.gov/data/correlation/nina34.data"

response = requests.get(url)

filtered_lines = []

with open("data/nina34.data", "r") as f:
    for line in f:
        parts = line.split()

        # Keep only yearly data rows
        if len(parts) == 13 and parts[0].isdigit():
            year = int(parts[0])
            if 2000 <= year <= 2025:
                filtered_lines.append(line)

print("Years found:")
for line in filtered_lines[:3]:
    print(line.strip())