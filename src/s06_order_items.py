import pandas as pd
from common import *

T = "order_items"
df = read_bronze("olist_order_items_dataset")
print(f"[{T}] loaded {len(df):,} rows")
df = to_num(df, ['order_item_id', 'price', 'freight_value'])

df = drop_nulls(df, ["order_id", "order_item_id", "product_id", "seller_id"], T)
df = drop_dups(df, ["order_id", "order_item_id"], T)  # composite primary key

df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

n = len(df)
df = df[(df["price"] > 0) & (df["freight_value"] >= 0)]
step(T, "price > 0 and freight >= 0", n, len(df))

orders = read_silver("orders")
products = read_silver("products")
sellers = read_silver("sellers")
df = hard_fk(df, "order_id", orders["order_id"], T, "orders")
df = hard_fk(df, "product_id", products["product_id"], T, "products")
df = hard_fk(df, "seller_id", sellers["seller_id"], T, "sellers")

null_report(df, T)
write_silver(df, T)
