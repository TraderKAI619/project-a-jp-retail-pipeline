-- KPI：假日 vs 平日營收
WITH f AS (
  SELECT date_key, COALESCE(revenue_jpy, gross_amount) AS revenue
  FROM read_csv_auto('data/gold/facts/fact_sales.csv')
),
d AS (
  SELECT date_key, is_holiday
  FROM read_csv_auto('data/gold/dims/dim_date.csv')
)
SELECT
  is_holiday,
  SUM(revenue) AS revenue_jpy
FROM f
JOIN d USING (date_key)
GROUP BY is_holiday
ORDER BY is_holiday;
