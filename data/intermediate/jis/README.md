# jis_prefecture_city.csv（日本地域コード・中間資料層）

## 📘 用途（Purpose）
此資料為清理後的日本行政區劃代碼表，  
由 `data/raw_official/jis/_staging/` 的原始資料（總務省「全国地方公共団体コード」）整理而成。  
主要用途為地理層級分析、區域統計聚合、以及地區別銷售模型的維度資料。

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
| `pref_code` | string | 都道府縣代碼（2位數） |
| `city_code` | string | 市區町村代碼（5位數） |
| `pref_name_ja` | string | 都道府縣名稱（日文） |
| `city_name_ja` | string | 市區町村名稱（日文） |
| `source` | string | 資料來源（總務省） |
| `source_version` | string | 原始 Excel 檔案版本或下載日期 |

---

## 📎 備註（Notes）
- 資料原始來源：總務省「全国地方公共団体コード」。
- 已刪除不必要的註解行與空白列。
- 本表可用於地理層 join、統計聚合及市町村層級模型分析。
