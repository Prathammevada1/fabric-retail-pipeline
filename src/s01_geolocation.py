import pandas as pd
from common import *

T = "geolocation"
df = read_bronze("olist_geolocation_dataset")
print(f"[{T}] loaded {len(df):,} rows")
df = to_num(df, ['geolocation_lat', 'geolocation_lng'])

df = drop_dups(df, None, T)  # exact duplicate rows
df = drop_nulls(df, ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"], T)

df["geolocation_zip_code_prefix"] = clean_zip(df["geolocation_zip_code_prefix"])
df["geolocation_city"] = clean_text(df["geolocation_city"])
df["geolocation_state"] = df["geolocation_state"].astype("string").str.strip().str.upper()

# coordinates must be inside Brazil
n = len(df)
df = df[df["geolocation_lat"].between(-34, 6) & df["geolocation_lng"].between(-74, -34)]
step(T, "coordinates inside Brazil", n, len(df))

# valid state codes only
STATES = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
          "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}
n = len(df)
df = df[df["geolocation_state"].isin(STATES)]
step(T, "valid state code", n, len(df))


def mode(s):
    m = s.dropna().mode()
    return m.iat[0] if len(m) else pd.NA


# one row per zip prefix, so it can be used as a clean lookup table
n = len(df)
df = (
    df.groupby("geolocation_zip_code_prefix")
    .agg(
        geolocation_lat=("geolocation_lat", "median"),
        geolocation_lng=("geolocation_lng", "median"),
        geolocation_city=("geolocation_city", mode),
        geolocation_state=("geolocation_state", mode),
    )
    .reset_index()
)
step(T, "one row per zip prefix", n, len(df))

assert df["geolocation_zip_code_prefix"].is_unique
null_report(df, T)
write_silver(df, T)
