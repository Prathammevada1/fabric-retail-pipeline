import pandas as pd
from common import *

T = "orders"
df = read_bronze("olist_orders_dataset")
print(f"[{T}] loaded {len(df):,} rows")

df = drop_nulls(df, ["order_id", "customer_id", "order_purchase_timestamp"], T)
df = drop_dups(df, ["order_id"], T)

df["order_status"] = clean_text(df["order_status"])
VALID = {"delivered", "shipped", "canceled", "unavailable", "invoiced",
         "processing", "created", "approved"}
n = len(df)
df = df[df["order_status"].isin(VALID)]
step(T, "valid order_status", n, len(df))

date_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
             "order_delivered_customer_date", "order_estimated_delivery_date"]
for c in date_cols:
    df[c] = pd.to_datetime(df[c], errors="coerce")
df = drop_nulls(df, ["order_purchase_timestamp"], T)

# a delivery before the purchase is impossible, so the wrong date becomes null
bad = df["order_delivered_customer_date"] < df["order_purchase_timestamp"]
df.loc[bad, "order_delivered_customer_date"] = pd.NaT
print(f"[{T}] delivered before purchase -> set to null: {bad.sum():,}")

customers = read_silver("customers")
df = hard_fk(df, "customer_id", customers["customer_id"], T, "customers")

# nulls in the delivery dates are normal for orders that are not delivered yet
null_report(df, T)
write_silver(df, T)
