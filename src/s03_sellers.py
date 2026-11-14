from common import *

T = "sellers"
df = read_bronze("olist_sellers_dataset")
print(f"[{T}] loaded {len(df):,} rows")

df = drop_nulls(df, ["seller_id"], T)
df = drop_dups(df, ["seller_id"], T)

df["seller_zip_code_prefix"] = clean_zip(df["seller_zip_code_prefix"])
df["seller_city"] = clean_text(df["seller_city"])
df["seller_state"] = df["seller_state"].astype("string").str.strip().str.upper()

geo = read_silver("geolocation")
df = soft_fk(df, "seller_zip_code_prefix", geo["geolocation_zip_code_prefix"], T, "geolocation")

null_report(df, T)
write_silver(df, T)
