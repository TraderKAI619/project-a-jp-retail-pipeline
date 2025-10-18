-- KPI: 稅率境界（2019/10）前後的銷售額（以日期維度的 tax_rate 為準）
WITH f AS (
<<<<<<< HEAD
=======
  -- 只保留用得到的欄位，避免與 d.tax_rate 重名
>>>>>>> 13d2be691e86ddaf3399c1de950308650515ec3f
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
<<<<<<< HEAD
-- 這裡自動用目前 sales 的最小/最大日期
WHERE d.date_key BETWEEN (SELECT MIN(date_key) FROM f)
                     AND (SELECT MAX(date_key) FROM f)
=======
WHERE d.date_key BETWEEN 20180801 AND 20201231
>>>>>>> 13d2be691e86ddaf3399c1de950308650515ec3f
GROUP BY d.tax_rate
ORDER BY d.tax_rate;
