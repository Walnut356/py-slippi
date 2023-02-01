import polars as pl

wd_df = pl.read_parquet(r"wavedashdata.parquet")

print(wd_df)