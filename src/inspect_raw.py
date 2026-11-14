from pathlib import Path
import pandas as pd

RAW = Path("data/raw")

for f in sorted(RAW.glob("*.csv")):
    df = pd.read_csv(f)
    print(f"{f.name}: {len(df):,} rows, {len(df.columns)} columns")