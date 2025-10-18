-- KPI：都道府縣 × 月份 的營收排名
-- 以 yyyymm 聚合，觀察各都道府縣月度表現
WITH f AS (
  SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')
),
d AS (
  SELECT date_key, CAST(date_key/100 AS INT) AS yyyymm
  FROM read_csv_auto('data/gold/dims/dim_date.csv')
),
g AS (
  SELECT city_key, pref_code, pref_name
  FROM read_csv_auto('data/gold/dims/dim_geo.csv')
)
SELECT
  g.pref_code,
  g.pref_name,
  d.yyyymm,
  ROUND(SUM(gross_amount)/1e8, 2) AS rev_億日圓
FROM f
JOIN d USING (date_key)
JOIN g USING (city_key)
GROUP BY 1,2,3
ORDER BY d.yyyymm, rev_億日圓 DESC;
