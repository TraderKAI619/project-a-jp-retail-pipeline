import duckdb, pathlib
out = pathlib.Path('data/analytics'); out.mkdir(parents=True, exist_ok=True)
con = duckdb.connect()
q = pathlib.Path('analytics/sql/gw_analysis.sql').read_text(encoding='utf-8')
# 第1個結果（prefecture）
pref = con.execute(q.split(';')[0]).fetchdf()
pref.to_csv(out/'top_prefecture_uplift.csv', index=False)
# 第2個結果（category）
cat = con.execute(q.split(';')[1]).fetchdf()
cat.to_csv(out/'category_contrib.csv', index=False)
print("✅ wrote:", *(str(p) for p in out.glob('*.csv')), sep="\n")
