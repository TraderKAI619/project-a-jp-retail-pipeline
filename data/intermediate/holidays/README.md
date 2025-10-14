# holidays_clean.csv（日本祝日・中間資料層）

## 📘 用途（Purpose）
此資料為清理後的日本祝日表，  
由 `data/raw_official/holidays/_staging/` 中的原始資料整理而成。  
主要用於下游分析、日曆維度表、及零售時間序列建模。

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
| `date` | date | 節日日期（含振替休日） |
| `name_ja` | string | 節日名稱（日文） |
| `name_en` | string | 節日名稱（英文） |
| `is_substitute` | bool | 是否為振替休日（True/False） |
| `source` | string | 資料來源（內閣府官報） |
| `source_version` | string | 版本或下載日期 |

---

## 📎 備註（Notes）
- 節日日期以官方公告為準，包含振替休日。
- 此為整潔化（tidy）版本，可直接進行分析。
- 來源對應：`data/raw_official/holidays/_staging/`
