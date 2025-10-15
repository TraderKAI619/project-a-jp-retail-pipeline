# Silver Layer — 日本官方資料清理層（中間資料的整潔版本）

本層為 Project A 的第二層資料處理成果。  
所有資料皆由 Intermediate 層進一步清理、統一欄位名稱與格式後產生。  
此層可直接被分析層（Gold Layer / dbt 模型）使用。

---

## 🗂️ 檔案清單

| 類別 | 檔案路徑 | 說明 |
|------|-----------|------|
| 日本祝日 | `data/silver/holidays/jp_holidays_silver.csv` | 整潔化的日本祝日資料 |
| 行政區劃 | `data/silver/jis/jis_prefecture_city_silver.csv` | 都道府縣與市區町村代碼表 |
| 消費稅率 | `data/silver/tax/tax_rate_silver.csv` | 日本消費稅率歷史表 |

---

## 🇯🇵 1. 日本祝日資料（jp_holidays_silver.csv）

### 用途
供時間維度表與零售銷售分析使用，包含國定假日與振替休日。

### 欄位定義
| 欄位 | 型態 | 說明 |
|------|------|------|
| `date` | date | 節日日期（YYYY-MM-DD） |
| `holiday_name` | string | 節日名稱（日文） |
| `category` | string | 節日類別（如：国民の祝日、振替休日） |

---

## 🗾 2. 日本行政區劃代碼（jis_prefecture_city_silver.csv）

### 用途
提供地理維度表基礎，用於區域銷售統計與地理 Join。

### 欄位定義
| 欄位 | 型態 | 說明 |
|------|------|------|
| `pref_code` | string | 都道府縣代碼（2 位數） |
| `pref_name` | string | 都道府縣名稱（日文） |
| `city_code` | string | 市區町村代碼（5 位數） |
| `city_name` | string | 市區町村名稱（日文） |

---

## 💰 3. 日本消費稅率歷史表（tax_rate_silver.csv）

### 用途
用於時間序列分析與稅制變動模擬（ETL Join 可依日期範圍對應）。

### 欄位定義
| 欄位 | 型態 | 說明 |
|------|------|------|
| `start_date` | date | 稅率生效起日 |
| `end_date` | date | 稅率生效迄日（若為現行則留空） |
| `tax_rate` | float | 一般消費稅率（%） |

---

## ⚙️ 資料標準化規則（通用）

| 項目 | 規範 |
|------|------|
| 編碼 | UTF-8 |
| 換行符 | LF (`\n`) |
| 分隔符 | 逗號（`,`） |
| 日期格式 | `YYYY-MM-DD` |
| 小數點 | `.`（英文句點） |
| 缺失值 | 空白（不以 NULL 表示） |

---

## 🔗 來源與版本對應

| 類別 | 原始來源 | 版本／備註 |
|------|-----------|-------------|
| 祝日 | 內閣府官報公開資料 | 最新下載版 |
| 行政區劃 | 總務省「全国地方公共団体コード」 | R6 年度版 |
| 消費稅率 | 國稅廳公告「消費税率等の改正」 | 自 1989 年起歷史資料 |

---

## 🧩 未來擴充項目（Next Steps）
- 增加 `source`、`source_version` 欄位追蹤更新批次。  
- 於 Silver 階段加入唯一鍵驗證與 NA 比例統計。  
- 建立自動化檢查腳本（validate_silver.py）。

