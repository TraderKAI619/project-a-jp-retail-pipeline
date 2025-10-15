# Gold Layer — 星型模型（MVP）

## 維度
- `dims/dim_date.csv`  
  - `date_key (int, YYYYMMDD)` 主鍵  
  - `is_holiday`, `holiday_name`, `holiday_category`, `tax_rate` 等時間屬性
- `dims/dim_geo.csv`  
  - `city_key (PP-CCCCC)` 主鍵  
  - `pref_code`, `pref_name`, `city_code`, `city_name`

## 事實表
- `facts/fact_calendar.csv`（一日一列，供報表/模型掛時間與稅制）
  - `date_key` 外鍵 → `dim_date.date_key`
  - 欄位：`is_holiday`, `holiday_name`, `holiday_category`, `tax_rate`

> 後續可以新增 `fact_sales` 並以 `date_key` 與 `city_key` 連到上述兩個維度。
