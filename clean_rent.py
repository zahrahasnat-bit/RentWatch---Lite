import pandas as pd
from pathlib import Path

data_folder = Path("data")

datasets = {}

for file in data_folder.glob("*.csv"):
    datasets[file.stem] = pd.read_csv(file)

for name, df in datasets.items():
    print(name)
    print(df.shape)
    print()

for name, df in datasets.items():
    print("\nDATASET:", name)
    print("\nROW LABELS:")
    print("\nCOLUMNS:")
    print(df.columns.tolist())
        
for name, df in datasets.items():

    print("\nDATASET:", name)

    if "B25064" in name:
        selected = df[
            df["Label (Grouping)"] == "Median gross rent"
        ]

    elif "B25119" in name:
        selected = df[
            df["Label (Grouping)"].str.strip() == "Renter occupied (dollars)"
        ]

    elif "B25070" in name:
        selected = df[
            df["Label (Grouping)"].str.strip().isin([
                "Total:",
                "50.0 percent or more",
                "Not computed"
            ])
        ]

    print(selected)

    county_columns = []

    for col in df.columns:
        if "County" in col:
            county_columns.append(col)

    print(county_columns)