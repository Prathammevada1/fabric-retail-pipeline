from common import *

T = "payments"
df = read_bronze("olist_order_payments_dataset")
print(f"[{T}] loaded {len(df):,} rows")
df = to_num(df, ['payment_sequential', 'payment_installments', 'payment_value'])

df = drop_nulls(df, ["order_id", "payment_sequential", "payment_type", "payment_value"], T)
df = drop_dups(df, ["order_id", "payment_sequential"], T)  # composite primary key

df["payment_type"] = clean_text(df["payment_type"])
n = len(df)
df = df[df["payment_type"] != "not_defined"]
step(T, "remove payment_type not_defined", n, len(df))

n = len(df)
df = df[df["payment_value"] >= 0]
step(T, "payment_value >= 0", n, len(df))

df["payment_installments"] = df["payment_installments"].clip(lower=1)  # 0 installments makes no sense

orders = read_silver("orders")
df = hard_fk(df, "order_id", orders["order_id"], T, "orders")

null_report(df, T)
write_silver(df, T)
