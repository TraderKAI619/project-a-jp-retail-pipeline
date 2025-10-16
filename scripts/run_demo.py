import duckdb, pathlib, re
def run_sql_file(path):
    print(f"\n==> RUN {path}")
    sql = pathlib.Path(path).read_text(encoding='utf-8')
    stmts = [s.strip() for s in re.split(r';\s*(?:\n|$)', sql) if s.strip()]
    k = 1
    for s in stmts:
        try:
            res = duckdb.sql(s)
            try:
                df = res.df()
            except Exception:
                continue
            if not df.empty:
                print(f"\n— 結果 #{k} —"); print(df.head(20)); k += 1
        except Exception as e:
            print(f"[ERROR] {e}\n{s}\n")
run_sql_file('sql/generate_fake_sales.sql')
run_sql_file('sql/demo_sales.sql')
