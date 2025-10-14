import pandas as pd
from pathlib import Path

# --- 路徑設定 ---
RAW_PATH = Path("data/raw_official/jis/_staging/jis_prefecture_city.csv")
OUTPUT_PATH = Path("data/intermediate/jis/jis_prefecture_city.csv")

# --- 讀取原始資料 ---
print(f"📥 Loading raw data from: {RAW_PATH}")
df = pd.read_csv(RAW_PATH)

# --- 清理欄位 ---
print("🧹 Cleaning column names and formatting...")
df.columns = df.columns.str.strip().str.lower()

# --- 基本欄位統一 ---
rename_map = {
    "prefecture_code": "pref_code",
    "prefecture_name": "pref_name",
    "city_code": "city_code",
    "city_name": "city_name"
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# --- 移除重複與缺失 ---
df = df.drop_duplicates().dropna(subset=["pref_name", "city_name"])

# --- 排序 ---
if "pref_code" in df.columns and "city_code" in df.columns:
    df = df.sort_values(["pref_code", "city_code"]).reset_index(drop=True)

# --- 輸出 ---
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8", lineterminator="\n")

print(f"✅ jis_prefecture_city.csv 已輸出到：{OUTPUT_PATH}")
print(df.head())
