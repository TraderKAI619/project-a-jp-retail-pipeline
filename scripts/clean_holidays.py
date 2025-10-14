import pandas as pd
from pathlib import Path
import sys
import re

STAGING_DIR = Path("data/raw_official/holidays/_staging")
OUTPUT_PATH = Path("data/intermediate/holidays/jp_holidays_clean.csv")

print(f"📥 Looking for source in: {STAGING_DIR}")

# 找檔案
candidates = list(STAGING_DIR.glob("*.csv")) + list(STAGING_DIR.glob("*.xlsx"))
if not candidates:
    print("❌ No CSV/XLSX found in _staging. Please put jp_holidays.csv or .xlsx there.")
    sys.exit(1)

RAW_PATH = candidates[0]
print(f"📄 Using file: {RAW_PATH.name}")

# 讀檔（支援多種常見日文編碼）
def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path, dtype=str)
    tried = []
    for enc in ["utf-8-sig", "utf-8", "cp932", "shift_jis", "ms932", "latin1"]:
        try:
            print(f"🔎 Trying encoding: {enc}")
            return pd.read_csv(path, dtype=str, encoding=enc)
        except UnicodeDecodeError:
            tried.append(enc)
            continue
    print(f"⚠️ All encodings failed, falling back with ignore: {tried}")
    return pd.read_csv(path, dtype=str, encoding="cp932", encoding_errors="ignore")

df = read_table(RAW_PATH)

print("🧹 Normalizing columns...")

# 去除全形空白與前後空格
df = df.applymap(lambda x: x.strip().replace('\u3000', ' ') if isinstance(x, str) else x)

# 欄名正規化（去空白 → 底線 → 小寫）
df.columns = [re.sub(r'\s+', '_', c.strip()).lower() for c in df.columns]

# 常見日文欄名對應
rename_map = {
    "日付": "date",
    "年月日": "date",
    "国民の祝日": "holiday_name",
    "祝日名": "holiday_name",
    "名称": "holiday_name",
}
df = df.rename(columns=rename_map)

# 檢查欄位
if "date" not in df.columns:
    print("❌ 'date' column not found in source file after renaming.")
    print(f"Columns seen: {list(df.columns)}")
    sys.exit(1)

# 篩選必要欄位（若 holiday_name 不在就先建立為空字串）
expected_cols = ["date", "holiday_name"]
for col in expected_cols:
    if col not in df.columns:
        df[col] = ""
df = df[expected_cols]

# 日期格式標準化 → YYYY-MM-DD
df["date"] = pd.to_datetime(df["date"], errors="coerce")
bad_date = df["date"].isna().sum()
if bad_date > 0:
    print(f"⚠️ Found {bad_date} invalid dates after coercion. They will be dropped.")
df = df.dropna(subset=["date"])
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# 去重（同日同名只留一列）
df = df.drop_duplicates(subset=["date", "holiday_name"])

# 排序輸出
df = df.sort_values("date").reset_index(drop=True)

# 輕量驗證
print(f"🧪 Rows: {len(df)}, unique dates: {df['date'].nunique()}")

# 寫檔
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"✅ Clean holidays saved to: {OUTPUT_PATH}")
