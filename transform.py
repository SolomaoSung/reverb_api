# %%
import pandas as pd
pd.set_option("display.max_columns", None)
import json

# %%
df = pd.read_parquet("data/raw/listings_00.parquet")
# %%
df.head()
to_dict = ["shop", "condition", "price", "buyer_price","categories","state",
           "shipping","_links","photos"]

normalized = []
for column in to_dict:
    df[column] = df[column].apply(lambda x: json.loads(x))
    normalized.append(pd.json_normalize(df[column]))
    df = df.drop(columns=column)

df_normalized = pd.concat([df] + normalized, axis=1)
# %%
list_columns = ["categories", "photos"]
# %%
for col in list_columns:
    df_split[col] = pd.Series(df[col], index=df.index)
    df_split = df_split.add_prefix("val_")
    df_split
# %%
mask = df["categories"].apply(lambda x : len(x) > 1)
df.loc[mask, "categories"][0]
# %%
