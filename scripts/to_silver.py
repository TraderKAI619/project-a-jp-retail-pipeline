#!/usr/bin/env python3
import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
INT = ROOT / "data" / "intermediate"
SILVER = ROOT / "data" / "silver"

def to_silver():
    print("🚀 Intermediate → Silver ...")
    
    # === Holidays ===
    df_h = pd.read_csv(INT / "holidays" / "jp_holidays_clean.csv")
    # 添加 date_key (YYYYMMDD 格式)
    df_h['date'] = pd.to_datetime(df_h['date'])
    df_h['date_key'] = df_h['date'].dt.strftime('%Y%m%d').astype(int)
    # 添加 is_holiday (都是 True)
    df_h['is_holiday'] = True
    # 重命名列
    df_h = df_h.rename(columns={'category': 'holiday_category'})
    # 重新排序列
    df_h = df_h[['date_key', 'date', 'is_holiday', 'holiday_name', 'holiday_category']]
    
    out_h = SILVER / "holidays" / "jp_holidays_silver.csv"
    out_h.parent.mkdir(parents=True, exist_ok=True)
    df_h.to_csv(out_h, index=False, encoding="utf-8")
    print(f"✅ Saved: {out_h}")
    
    # === JIS ===
    df_j = pd.read_csv(INT / "jis" / "jis_prefecture_city.csv")
    out_j = SILVER / "jis" / "jis_prefecture_city_silver.csv"
    out_j.parent.mkdir(parents=True, exist_ok=True)
    df_j.to_csv(out_j, index=False, encoding="utf-8")
    print(f"✅ Saved: {out_j}")
    
    # === Tax ===
    df_t = pd.read_csv(INT / "tax" / "tax_rate_clean.csv")
    out_t = SILVER / "tax" / "tax_rate_silver.csv"
    out_t.parent.mkdir(parents=True, exist_ok=True)
    df_t.to_csv(out_t, index=False, encoding="utf-8")
    print(f"✅ Saved: {out_t}")
    
    print("🎉 All Silver datasets ready!")

if __name__ == "__main__":
    to_silver()
