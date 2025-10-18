-- KPI：假日 vs 平日營收
-- 輸入：data/gold/facts/fact_sales.csv、data/gold/dims/dim_date.csv
-- 提示：若你的欄位是 revenue_jpy，請把下方的 gross_amount 換成 revenue_jpy
WITH f AS (
  SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')
),
d AS (
  SELECT date_key, is_holiday
  FROM read_csv_auto('data/gold/dims/dim_date.csv')
)
SELECT
  is_holiday,
  SUM(gross_amount) AS revenue_jpy
FROM f
JOIN d USING (date_key)
GROUP BY is_holiday
ORDER BY is_holiday;
