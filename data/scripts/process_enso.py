import pandas as pd

# Read text file
df = pd.read_csv(
    "data/nina34.data",
    sep=r"\s+",
    skiprows=1,
    header=None,
    engine="python"
)

# Show dimensions
print("Shape:", df.shape)

# Show first rows
print(df.head())
print(df.shape)