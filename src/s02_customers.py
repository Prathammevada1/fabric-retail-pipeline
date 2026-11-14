from common import *

T = "customers"
df = read_bronze("olist_customers_dataset")
print(f"[{T}] loaded {len(df):,} rows")

df = drop_nulls(df, ["customer_id", "customer_unique_id"], T)
df = drop_dups(df, ["customer_id"], T)  # customer_id is the primary key

df["customer_zip_code_prefix"] = clean_zip(df["customer_zip_code_prefix"])
df["customer_city"] = clean_text(df["customer_city"])
df["customer_state"] = df["customer_state"].astype("string").str.strip().str.upper()

geo = read_silver("geolocation")
df = soft_fk(df, "customer_zip_code_prefix", geo["geolocation_zip_code_prefix"], T, "geolocation")

null_report(df, T)
write_silver(df, T)
