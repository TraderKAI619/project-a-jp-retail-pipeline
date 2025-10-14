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

# 讀檔
if RAW_PATH.suffix.lower() == ".xlsx":
    df = pd.read_excel(RAW_PATH, dtype=str)
else:
    df = pd.read_csv(RAW_PATH, dtype=str)

print("🧹 Normalizing columns...")

# 去除全形空白與前後空格
df = df.applymap(lambda x: x.strip().replace('\u3000', ' ') if isinstance(x, str) else x)

# 欄名正規化
df.columns = [re.sub(r'\s+', '_', c.strip()) for c in df.columns]

# 檢查欄位
if "date" not in df.columns:
    print("❌ 'date' column not found in source file.")
    sys.exit(1)

# 篩選必要欄位
expected_cols = ["date", "holiday_name"]
df = df[[c for c in df.columns if c in expected_cols]]

# 日期格式標準化
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

# 移除空白行
df = df.dropna(subset=["date"])

# 排序輸出
df = df.sort_values("date")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"✅ Clean holidays saved to: {OUTPUT_PATH}")
