import pandas as pd
from pathlib import Path

INTERMEDIATE_DIR = Path("data/intermediate")
SILVER_DIR = Path("data/silver")
(SILVER_DIR / "holidays").mkdir(parents=True, exist_ok=True)
(SILVER_DIR / "jis").mkdir(parents=True, exist_ok=True)
(SILVER_DIR / "tax").mkdir(parents=True, exist_ok=True)

def clean_holidays():
    src = INTERMEDIATE_DIR / "holidays/jp_holidays_clean.csv"
    dst = SILVER_DIR / "holidays/jp_holidays_silver.csv"
    df = pd.read_csv(src, dtype=str)
    # 統一欄名
    # 你的中間層文件寫的是 name_ja/name_en/is_substitute... 這裡我們先用最小可行欄位
    # 若未來補上更多欄位，只要在這裡擴充 mapping 即可
    if set(df.columns) >= {"date","holiday_name","category"}:
        df = df[["date","holiday_name","category"]]
    else:
        df.columns = ["date","holiday_name","category"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date")
    df.to_csv(dst, index=False)
    print(f"✅ Saved: {dst}")

def clean_jis():
    src = INTERMEDIATE_DIR / "jis/jis_prefecture_city.csv"
    dst = SILVER_DIR / "jis/jis_prefecture_city_silver.csv"
    df = pd.read_csv(src, dtype=str)
    # 統一欄名
    # 若未來改成 pref_name_ja/city_name_ja 也可以在此處 mapping
    if set(df.columns) >= {"pref_code","pref_name","city_code","city_name"}:
        df = df[["pref_code","pref_name","city_code","city_name"]]
    else:
        df.columns = ["pref_code","pref_name","city_code","city_name"]
    df.to_csv(dst, index=False)
    print(f"✅ Saved: {dst}")

def clean_tax():
    src = INTERMEDIATE_DIR / "tax/tax_rate_clean.csv"
    dst = SILVER_DIR / "tax/tax_rate_silver.csv"
    df = pd.read_csv(src, dtype=str)
    # 支援將來加入 reduced_tax_rate 的擴充
    base_cols = ["start_date","end_date","tax_rate"]
    if set(df.columns) >= set(base_cols):
        df = df[base_cols]
    else:
        df.columns = base_cols[:len(df.columns)]
    df["tax_rate"] = pd.to_numeric(df["tax_rate"], errors="coerce")
    df.to_csv(dst, index=False)
    print(f"✅ Saved: {dst}")

if __name__ == "__main__":
    print("🚀 Intermediate → Silver ...")
    clean_holidays()
    clean_jis()
    clean_tax()
    print("🎉 All Silver datasets ready!")
