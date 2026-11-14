import numpy as np
from common import *

T = "products"
df = read_bronze("olist_products_dataset")
print(f"[{T}] loaded {len(df):,} rows")

df = drop_nulls(df, ["product_id"], T)
df = drop_dups(df, ["product_id"], T)

# fix the typos in the original column names
df = df.rename(columns={
    "product_name_lenght": "product_name_length",
    "product_description_lenght": "product_description_length",
})

df = to_num(df, ["product_name_length", "product_description_length", "product_photos_qty",
                 "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"])

df["product_category_name"] = clean_text(df["product_category_name"]).fillna("unknown")

# add the english category name, keep the portuguese one if there is no translation
tr = read_bronze("product_category_name_translation")
tr["product_category_name"] = clean_text(tr["product_category_name"])
tr = tr.drop_duplicates("product_category_name")
df = df.merge(tr, on="product_category_name", how="left")
df["product_category_name_english"] = df["product_category_name_english"].fillna(df["product_category_name"])

# impossible sizes become null (the product itself is kept)
for c in ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]:
    bad = (df[c] <= 0).sum()
    df.loc[df[c] <= 0, c] = np.nan
    print(f"[{T}] {c} <= 0 set to null: {bad:,}")

null_report(df, T)
write_silver(df, T)
