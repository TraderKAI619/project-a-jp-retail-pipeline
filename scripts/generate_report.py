# scripts/generate_report.py
import pathlib
import datetime as dt
import duckdb
import pandas as pd  # for to_csv / to_markdown

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "gold"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

def _gold(p):
    return (GOLD / p).as_posix()

def main():
    # 前置檢查：gold 檔案一定要在
    need = [GOLD / "facts" / "fact_sales.csv", GOLD / "dims" / "dim_date.csv"]
    missing = [str(p) for p in need if not p.exists()]
    if missing:
        raise SystemExit(
            "Gold 層尚未就緒，請先 `make gold` 或 `make everything`。\n缺少：\n- " + "\n- ".join(missing)
        )

    con = duckdb.connect()

    # KPI：假日 vs 非假日營收
    sql_uplift = f"""
    WITH f AS (SELECT * FROM read_csv_auto('{_gold('facts/fact_sales.csv')}')),
         d AS (SELECT date_key, is_holiday FROM read_csv_auto('{_gold('dims/dim_date.csv')}'))
    SELECT is_holiday, ROUND(SUM(gross_amount), 0) AS revenue_jpy
    FROM f JOIN d USING (date_key)
    GROUP BY 1
    ORDER BY 1;
    """
    uplift = con.execute(sql_uplift).fetch_df()

    # 寫 CSV
    uplift.to_csv(OUT / "uplift.csv", index=False, encoding="utf-8")

    # 寫 Markdown（需要 tabulate）
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [
        "# Daily Report",
        f"_generated: {now}_",
        "## Holiday uplift",
        uplift.to_markdown(index=False),
    ]
    (OUT / "report.md").write_text("\n\n".join(md), encoding="utf-8")
    print("Wrote", OUT / "report.md")
    print("Wrote", OUT / "uplift.csv")

if __name__ == "__main__":
    main()
