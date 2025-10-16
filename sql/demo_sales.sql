-- ① 假日 vs 非假日 營收差異
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, is_holiday FROM read_csv_auto('data/gold/dims/dim_date.csv'))
SELECT is_holiday, SUM(revenue_jpy) AS rev_jpy
FROM f JOIN d USING(date_key)
GROUP BY is_holiday
ORDER BY is_holiday;

-- ② 2019/10 調稅前後（稅率效果）
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, tax_rate FROM read_csv_auto('data/gold/dims/dim_date.csv'))
SELECT tax_rate, ROUND(SUM(revenue_jpy)/1e8, 2) AS rev_億日圓
FROM f JOIN d USING(date_key)
WHERE date_key BETWEEN 20180801 AND 20201231
GROUP BY tax_rate
ORDER BY tax_rate;

-- ③ 各都道府縣（月）營收排名（地理×時間）
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, CAST(date_key/100 AS INT) AS yyyymm FROM read_csv_auto('data/gold/dims/dim_date.csv')),
     g AS (SELECT city_key, pref_code, pref_name FROM read_csv_auto('data/gold/dims/dim_geo.csv'))
SELECT g.pref_code, g.pref_name, d.yyyymm,
       ROUND(SUM(f.revenue_jpy)/1e8, 2) AS rev_億日圓
FROM f JOIN d USING(date_key) JOIN g USING(city_key)
GROUP BY 1,2,3
ORDER BY d.yyyymm, rev_億日圓 DESC;
