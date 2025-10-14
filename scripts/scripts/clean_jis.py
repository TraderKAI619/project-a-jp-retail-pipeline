import pandas as pd
from pathlib import Path
import sys

STAGING_DIR = Path("data/raw_official/jis/_staging")
OUTPUT_PATH = Path("data/intermediate/jis/jis_prefecture_city.csv")

print(f"📥 Looking for source in: {STAGING_DIR}")

# 找檔案（先找 csv，沒有就找 xlsx）
candidates = list(STAGING_DIR.glob("*.csv")) + list(STAGING_DIR.glob("*.xlsx"))
if not candidates:
    print("❌ No CSV/XLSX found in _staging. Please put jis_prefecture_city.csv or .xlsx there.")
    sys.exit(1)

RAW_PATH = candidates[0]
print(f"📄 Using file: {RAW_PATH.name}")

# 讀檔（保留前導 0）
if RAW_PATH.suffix.lower() == ".xlsx":
    df = pd.read_excel(RAW_PATH, dtype=str)
else:
    df = pd.read_csv(RAW_PATH, dtype=str)

print("🧹 Normalizing columns...")

# 對應表（日文與英文皆可）
rename_map = {
    "prefecture_code": "pref_code",
    "prefecture_name": "pref_name",
    "city_code": "city_code",
    "city_name": "city_name",
    "都道府県コード": "pref_code",
    "都道府県名": "pref_name",
    "市区町村コード": "city_code",
    "市区町村名": "city_name",
}

# 轉換欄名（保留原樣不轉小寫）
df.columns = [c.strip() for c in df.columns]
df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})

required = ["pref_code", "pref_name", "city_code", "city_name"]
missing = [c for c in required if c not in df.columns]
if missing:
    print(f"❌ Missing required columns after rename: {missing}")
    print(f"Columns in file: {list(df.columns)}")
    sys.exit(1)

# 整理欄位
df = df[required].copy()
df["pref_code"] = df["pref_code"].astype(str).str.strip().str.zfill(2)
df["city_code"] = df["city_code"].astype(str).str.strip().str.zfill(5)
df["pref_name"] = df["pref_name"].astype(str).str.strip()
df["city_name"] = df["city_name"].astype(str).str.strip()

# 去重、排序
df = df.drop_duplicates().dropna(subset=["pref_name", "city_name"])
df = df.sort_values(["pref_code", "city_code"]).reset_index(drop=True)

# 輸出
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8", lineterminator="\n")

print(f"✅ jis_prefecture_city.csv 已輸出到：{OUTPUT_PATH}")
print(df.head())

