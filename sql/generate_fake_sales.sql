-- 先產生中繼表（不在同一層用別名引用）
CREATE OR REPLACE TABLE tmp_fact_sales_stage AS
WITH d AS (SELECT * FROM read_csv_auto('data/gold/dims/dim_date.csv')),
     g AS (SELECT * FROM read_csv_auto('data/gold/dims/dim_geo.csv')),
     cities AS (
       SELECT city_key, row_number() OVER (ORDER BY city_key) AS r
       FROM g
       LIMIT 120
     ),
     dc AS (
       SELECT d.date_key, d.year, d.month, d.dow, d.is_holiday, d.tax_rate, c.city_key, c.r
       FROM d CROSS JOIN cities c
     ),
     enriched AS (
       SELECT *,
         CASE WHEN month IN (7,8,12) THEN 1.15
              WHEN month IN (1,2)   THEN 0.92
              ELSE 1.0 END AS seasonality,
         CASE WHEN dow IN (6,7) THEN 1.08 ELSE 1.0 END AS weekend_boost,   -- 1~7 = Mon~Sun
         CASE WHEN is_holiday IS TRUE THEN 1.30 ELSE 1.0 END AS holiday_boost,
         CASE WHEN tax_rate >= 0.10 THEN 0.97 ELSE 1.0 END AS tax_penalty,
         12 + (r % 18) AS base_orders
       FROM dc
     )
SELECT
  date_key,
  city_key,
  CAST(ROUND(base_orders * seasonality * weekend_boost * holiday_boost * tax_penalty + random()*2) AS INTEGER) AS orders,
  CAST(ROUND(3000 + random()*4000, 0) AS INTEGER) AS avg_basket_jpy
FROM enriched
;

-- 再產出最終表，補上 revenue 欄位
CREATE OR REPLACE TABLE tmp_fact_sales AS
SELECT
  date_key,
  city_key,
  orders,
  avg_basket_jpy,
  CAST(orders * avg_basket_jpy AS BIGINT) AS revenue_jpy
FROM tmp_fact_sales_stage
;

-- 匯出 CSV
COPY tmp_fact_sales TO 'data/gold/facts/fact_sales.csv' (HEADER, DELIMITER ',');
