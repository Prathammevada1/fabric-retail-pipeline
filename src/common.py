"""Shared helpers for every silver script."""
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"


def read_bronze(name: str) -> pd.DataFrame:
    return pd.read_parquet(BRONZE / f"{name}.parquet")


def read_silver(name: str) -> pd.DataFrame:
    return pd.read_parquet(SILVER / f"{name}.parquet")


def write_silver(df: pd.DataFrame, name: str) -> None:
    SILVER.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER / f"{name}.parquet", index=False)
    print(f"[{name}] saved {len(df):,} rows -> {SILVER / (name + '.parquet')}\n")


def step(table: str, what: str, before: int, after: int) -> None:
    print(f"[{table}] {what}: {before:,} -> {after:,} (removed {before - after:,})")


def _strip_accents(x):
    if not isinstance(x, str):
        return x
    return "".join(c for c in unicodedata.normalize("NFKD", x) if not unicodedata.combining(c))


def clean_text(s: pd.Series) -> pd.Series:
    """trim, lowercase, remove accents, collapse spaces. Empty text becomes NA."""
    out = (
        s.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
        .map(_strip_accents)
        .astype("string")
    )
    return out.replace("", pd.NA)


def clean_zip(s: pd.Series) -> pd.Series:
    """zip prefix as a 5-character string, e.g. 1046 -> '01046'."""
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype("string").str.zfill(5)


def drop_nulls(df, cols, table):
    n = len(df)
    df = df.dropna(subset=cols)
    step(table, f"drop null in {cols}", n, len(df))
    return df


def drop_dups(df, subset, table):
    n = len(df)
    df = df.drop_duplicates(subset=subset, keep="first")
    step(table, f"drop duplicates on {subset}", n, len(df))
    return df


def hard_fk(df, col, parent_ids, table, parent):
    """Drop rows whose foreign key does not exist in the parent table."""
    n = len(df)
    df = df[df[col].isin(parent_ids)]
    step(table, f"FK {col} must exist in {parent}", n, len(df))
    return df


def soft_fk(df, col, parent_ids, table, parent):
    """Only report orphans, keep the rows."""
    missing = (~df[col].isin(parent_ids)).sum()
    print(f"[{table}] soft FK {col} not found in {parent}: {missing:,} rows (kept)")
    return df


def null_report(df, table):
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    print(f"[{table}] remaining nulls:", nulls.to_dict() if len(nulls) else "none")


def to_num(df, cols):
    """bronze stores everything as text, so convert number columns first."""
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
