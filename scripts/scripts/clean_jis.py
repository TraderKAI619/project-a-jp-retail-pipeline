import pandas as pd
from pathlib import Path
import sys
import re

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

# ---- 欄名正規化：移除換行、全形/半形空白、括號內容 ----
def norm_col(s: str) -> str:
    s = str(s)
    s = s.replace("\n", "").replace("\r", "")
    s = s.replace("　", "").replace(" ", "")        # 全形/半形空白
    s = re.sub("（.*?）", "", s)                     # 全形括號內容
    s = re.sub(r"\(.*?\)", "", s)                   # 半形括號內容
    return s

df.columns = [norm_col(c) for c in df.columns]

# ---- 欄位對應（日英都支援）----
rename_map = {
    # 英文
    "prefecture_code": "pref_code",
    "prefecture_name": "pref_name",
    "city_code": "city_code",
    "city_name": "city_name",
    # 日文（正規化後）
    "団体コード": "lg_code",
    "全国地方公共団体コード": "lg_code",
    "都道府県名": "pref_name",
    "市区町村名": "city_name",
}
df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})

# 若 rename 後出現重複欄名，保留第一個
df = df.loc[:, ~df.columns.duplicated(keep="first")]

# 從 lg_code 拆出 pref_code / city_code（lg_code=2位都道府県+3位市区町村+1位校驗）
if "pref_code" not in df.columns and "lg_code" in df.columns:
    df["lg_code"] = df["lg_code"].astype(str).str.strip()
    df["pref_code"] = df["lg_code"].str.slice(0, 2)
    df["city_code"] = df["lg_code"].str.slice(0, 5)

required = ["pref_code", "pref_name", "city_code", "city_name"]
missing = [c for c in required if c not in df.columns]
if missing:
    print(f"❌ Missing required columns after normalization: {missing}")
    print(f"Columns (normalized): {list(df.columns)}")
    sys.exit(1)

# 整理與格式化
df = df[required].copy()
df["pref_code"] = df["pref_code"].astype(str).str.strip().str.zfill(2)
df["city_code"] = df["city_code"].astype(str).str.strip().str.zfill(5)
df["pref_name"] = df["pref_name"].astype(str).str.strip()
df["city_name"] = df["city_name"].astype(str).str.strip()

# 去重、排序
df = df.dropna(subset=["pref_name", "city_name"]).drop_duplicates()
df = df.sort_values(["pref_code", "city_code"]).reset_index(drop=True)

# 輸出
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8", lineterminator="\n")

print(f"✅ jis_prefecture_city.csv 已輸出到：{OUTPUT_PATH}")
print(df.head())
