import pandas as pd

geo = pd.read_parquet(
    "data/bronze/olist_geolocation_dataset.parquet"
)

geo["geolocation_lat"] = pd.to_numeric(
    geo["geolocation_lat"], errors="coerce"
)

geo["geolocation_lng"] = pd.to_numeric(
    geo["geolocation_lng"], errors="coerce"
)

invalid_city = geo[
    ~geo["geolocation_city"].str.match(
        r"^[^\W\d_]+(?:\s+[^\W\d_]+)*$",
        na=False
    )
]

# 1. Check null values
print(geo.isnull().sum())

# 2. Check exact duplicate rows
print("Duplicate rows:", geo.duplicated().sum())
print(geo.dtypes)


# # 3. Check invalid latitude
# invalid_lat = geo[
#     (geo["geolocation_lat"] < -90) |
#     (geo["geolocation_lat"] > 90)
# ]

# # 4. Check invalid longitude
# invalid_lng = geo[
#     (geo["geolocation_lng"] < -180) |
#     (geo["geolocation_lng"] > 180)
# ]

# # 5. Check ZIP prefix duplicates
# print(
#     geo["geolocation_zip_code_prefix"].duplicated().sum()
# )