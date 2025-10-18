import duckdb

def q(sql: str):
    return duckdb.connect().execute(sql)

def test_dim_date_has_keys_and_unique():
    # 關鍵欄位存在 + PK 無重複
    q("SELECT date_key, is_holiday, tax_rate FROM read_csv_auto('data/gold/dims/dim_date.csv') LIMIT 1")
    dup = q("""
        SELECT COUNT(*) - COUNT(DISTINCT date_key) AS dups
        FROM read_csv_auto('data/gold/dims/dim_date.csv')
    """).fetchone()[0]
    assert dup == 0, f"date_key duplicate rows: {dup}"

def test_fact_sales_rowcount_sane():
    n = q("SELECT COUNT(*) FROM read_csv_auto('data/gold/facts/fact_sales.csv')").fetchone()[0]
    assert 100_000 <= n <= 2_000_000, f"rowcount out of expected range: {n}"

def test_fact_sales_non_negative_amounts():
    bad = q("""
        SELECT COUNT(*) FROM read_csv_auto('data/gold/facts/fact_sales.csv')
        WHERE COALESCE(net_amount,0) < 0
           OR COALESCE(tax_amount,0) < 0
           OR COALESCE(gross_amount,0) < 0
    """).fetchone()[0]
    assert bad == 0, f"found negative amounts: {bad}"

def test_sales_foreign_keys_cover_date_and_geo():
    # 用 LEFT JOIN + IS NULL 檢查遺失的外鍵，比 ANTI JOIN 更通用
    miss_date = q("""
        WITH f AS (SELECT date_key FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
             d AS (SELECT date_key FROM read_csv_auto('data/gold/dims/dim_date.csv'))
        SELECT COUNT(*) FROM f
        LEFT JOIN d ON f.date_key = d.date_key
        WHERE d.date_key IS NULL
    """).fetchone()[0]

    miss_geo = q("""
        WITH f AS (SELECT city_key FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
             g AS (SELECT city_key FROM read_csv_auto('data/gold/dims/dim_geo.csv'))
        SELECT COUNT(*) FROM f
        LEFT JOIN g ON f.city_key = g.city_key
        WHERE g.city_key IS NULL
    """).fetchone()[0]

    assert miss_date == 0, f"sales rows missing date_key in dim_date: {miss_date}"
    assert miss_geo == 0, f"sales rows missing city_key in dim_geo: {miss_geo}"
