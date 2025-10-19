import duckdb

def q(sql: str):
    return duckdb.connect().execute(sql)

def test_dim_date_has_keys_and_unique():
    q("SELECT date_key, is_holiday, tax_rate FROM read_csv_auto('data/gold/dims/dim_date.csv') LIMIT 1")
    dup = q("SELECT date_key, COUNT(*) AS c FROM read_csv_auto('data/gold/dims/dim_date.csv') GROUP BY date_key HAVING c>1").fetchall()
    assert len(dup) == 0, f"duplicate date_key: {dup}"

def test_fact_sales_rowcount_sane():
    n = q("SELECT COUNT(*) FROM read_csv_auto('data/gold/facts/fact_sales.csv')").fetchone()[0]
    # 调整为合理的范围：400 行是演示数据
    assert 100 <= n <= 500_000, f"rowcount out of expected range: {n}"

def test_fact_sales_non_negative_amounts():
    bad = q("""
        SELECT COUNT(*) FROM read_csv_auto('data/gold/facts/fact_sales.csv')
        WHERE COALESCE(net_amount,0) < 0
           OR COALESCE(tax_amount,0) < 0
           OR COALESCE(gross_amount,0) < 0
    """).fetchone()[0]
    assert bad == 0, f"found {bad} rows with negative amounts"

def test_sales_foreign_keys_cover_date_and_geo():
    miss_date = q("""
        WITH f AS (SELECT date_key FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
             d AS (SELECT date_key FROM read_csv_auto('data/gold/dims/dim_date.csv'))
        SELECT COUNT(*) FROM f
        LEFT JOIN d ON f.date_key = d.date_key
        WHERE d.date_key IS NULL
    """).fetchone()[0]
    assert miss_date == 0, f"{miss_date} sales rows have invalid date_key"

    miss_geo = q("""
        WITH f AS (SELECT city_key FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
             g AS (SELECT city_key FROM read_csv_auto('data/gold/dims/dim_geo.csv'))
        SELECT COUNT(*) FROM f
        LEFT JOIN g ON f.city_key = g.city_key
        WHERE g.city_key IS NULL
    """).fetchone()[0]
    assert miss_geo == 0, f"{miss_geo} sales rows have invalid city_key"
