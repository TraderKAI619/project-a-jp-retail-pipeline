# tax_rate_clean.csv（日本消費稅率・中間資料層）

## 📘 用途（Purpose）
此資料為清理後的日本消費稅率歷史表，  
由 `data/raw_official/tax/_staging/` 的原始資料（國稅廳「消費税率等の改正について」）整理而成。  
主要用途為：
- 模擬不同稅率下的零售銷售影響；
- 建立時間維度表（含稅制變動）；
- 於報表與 BI 模型中動態對應稅率期間。

---

## 🧩 格式規範（Data Format Rules）

| 項目 | 規範 |
|------|------|
| 編碼 | UTF-8 |
| 換行符號 | LF (`\n`) |
| 分隔符 | `,`（逗號）|
| 日期格式 | `YYYY-MM-DD` |
| 小數點 | `.`（英文句點）|

---

## 📋 欄位定義（Field Definitions）

| 欄位名稱 | 型態 | 說明 |
|-----------|------|------|
| `start_date` | date | 稅率開始生效日期 |
| `end_date` | date | 稅率結束日期（若為當前生效中則可為空） |
| `tax_rate` | float | 一般稅率（百分比） |
| `reduced_tax_rate` | float | 輕減稅率（百分比，若無則為空） |
| `source` | string | 資料來源（國稅廳） |
| `source_version` | string | 原始資料版本或更新日期 |

---

## 📎 備註（Notes）
- 稅率資料依官方公告順序排列，涵蓋自 1989 年以來的歷史紀錄。  
- 輕減稅率（8%）自 2019 年 10 月導入，僅適用特定食品與報紙。  
- 建議於 ETL 階段進行日期範圍 join，以避免錯誤稅期對應。  
- 來源對應：`data/raw_official/tax/_staging/tax_rate_history.csv`
