import duckdb, pandas as pd, pathlib
sql_path = pathlib.Path('analytics/sql/gw_analysis.sql')
con = duckdb.connect()
query = sql_path.read_text(encoding='utf-8')
df = con.execute(query).fetchdf()
pathlib.Path('data/analytics').mkdir(parents=True, exist_ok=True)
df.to_csv('data/analytics/top_prefecture_uplift.csv', index=False)
print(f"✅ Wrote data/analytics/top_prefecture_uplift.csv ({len(df)} rows)")
