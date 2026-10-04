"""One-off: remove duplicate rows from the raw dataset (ignoring Id)."""

import pandas as pd

PATH = "data/raw/WineQT.csv"

df = pd.read_csv(PATH)
before = len(df)
df = df.drop_duplicates(subset=[c for c in df.columns if c != "Id"], keep="first")
df.to_csv(PATH, index=False)
print(f"rows: {before} -> {len(df)} ({before - len(df)} duplicates removed)")
