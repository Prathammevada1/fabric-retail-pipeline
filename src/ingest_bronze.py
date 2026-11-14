from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
BRONZE = Path("data/bronze")
BRONZE.mkdir(parents=True, exist_ok=True)

ingested_at = datetime.now(timezone.utc).isoformat()

for f in sorted(RAW.glob("*.csv")):
    df = pd.read_csv(f, dtype=str, keep_default_na=False)
    df["_source_file"] = f.name
    df["_ingested_at"] = ingested_at
    out = BRONZE / f"{f.stem}.parquet"
    df.to_parquet(out, index=False)
    print(f"{f.name} -> {out.name}: {len(df):,} rows")