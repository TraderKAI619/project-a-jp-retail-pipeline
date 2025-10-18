-- KPI: 稅率境界（2019/10）前後的銷售額
WITH f AS (
  SELECT date_key, gross_amount
  FROM read_csv_auto('data/gold/facts/fact_sales.csv')
),
d AS (
  SELECT date_key, tax_rate
  FROM read_csv_auto('data/gold/dims/dim_date.csv')
)
SELECT
  d.tax_rate,
  ROUND(SUM(f.gross_amount) / 1e8, 2) AS rev_億日圓
FROM f
JOIN d USING (date_key)
WHERE d.date_key BETWEEN (SELECT MIN(date_key) FROM f)
                     AND (SELECT MAX(date_key) FROM f)
GROUP BY d.tax_rate
ORDER BY d.tax_rate;
