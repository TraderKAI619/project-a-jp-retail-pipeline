import pandas as pd
from pathlib import Path

# --- 路徑設定 ---
RAW_PATH = Path("data/raw_official/tax/_staging/tax_rate_history.csv")
OUTPUT_PATH = Path("data/intermediate/tax/tax_rate_clean.csv")

# --- 讀取原始資料 ---
df = pd.read_csv(RAW_PATH)

# --- 清理與格式統一 ---
# 1. 移除空白、轉小寫欄位名
df.columns = df.columns.str.strip().str.lower()

# 2. 確保日期格式一致
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce").dt.strftime("%Y-%m-%d")
df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce").dt.strftime("%Y-%m-%d")

# 3. 填補缺失值（若 reduced_tax_rate 為空則填 0）
df["reduced_tax_rate"] = df["reduced_tax_rate"].fillna(0).astype(int)

# 4. 稅率轉為 int
df["tax_rate"] = df["tax_rate"].astype(int)

# 5. 排序（由舊到新）
df = df.sort_values("start_date").reset_index(drop=True)

# --- 輸出 ---
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8", line_terminator="\n")

print(f"✅ tax_rate_clean.csv 已輸出到：{OUTPUT_PATH}")
print(df.head())
