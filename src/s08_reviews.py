import pandas as pd
from common import *

T = "reviews"
df = read_bronze("olist_order_reviews_dataset")
print(f"[{T}] loaded {len(df):,} rows")
df = to_num(df, ['review_score'])

df = drop_nulls(df, ["review_id", "order_id", "review_score"], T)
# the same review_id can appear for different orders, so the key is the pair
df = drop_dups(df, ["review_id", "order_id"], T)

n = len(df)
df = df[df["review_score"].between(1, 5)]
step(T, "review_score between 1 and 5", n, len(df))

for c in ["review_creation_date", "review_answer_timestamp"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")

for c in ["review_comment_title", "review_comment_message"]:
    df[c] = df[c].astype("string").str.strip().replace("", pd.NA)

orders = read_silver("orders")
df = hard_fk(df, "order_id", orders["order_id"], T, "orders")

# empty comments are normal (most people only give a score)
null_report(df, T)
write_silver(df, T)
