-- KPI：稅率變更（2019/10）前後的營收
-- 篩選 2018-08-01～2020-12-31，觀察 8%→10%（含 8% 輕減）期間差異
WITH f AS (
  SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')
),
d AS (
  SELECT date_key, tax_rate
  FROM read_csv_auto('data/gold/dims/dim_date.csv')
)
SELECT
  tax_rate,
  ROUND(SUM(gross_amount)/1e8, 2) AS rev_億日圓
FROM f
JOIN d USING (date_key)
WHERE date_key BETWEEN 20180801 AND 20201231
GROUP BY tax_rate
ORDER BY tax_rate;
