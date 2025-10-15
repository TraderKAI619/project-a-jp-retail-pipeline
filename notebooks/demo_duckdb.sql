-- 每年國定假日天數
SELECT strftime(date, '%Y') AS year, count(*) AS holiday_days
FROM read_csv_auto('data/gold/facts/fact_calendar.csv', header=true)
WHERE is_holiday = true
GROUP BY 1 ORDER BY 1;

-- 稅率變更點前後的假日天數（示範 join 維度）
WITH d AS (
  SELECT date_key, year
  FROM read_csv_auto('data/gold/dims/dim_date.csv', header=true)
)
SELECT d.year, count(*) AS holiday_days, any_value(f.tax_rate) AS sample_tax
FROM read_csv_auto('data/gold/facts/fact_calendar.csv', header=true) f
JOIN d USING (date_key)
WHERE f.is_holiday = true
GROUP BY d.year ORDER BY d.year;
