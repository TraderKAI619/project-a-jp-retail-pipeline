from pathlib import Path
import pandas as pd
import numpy as np

SILVER = Path("data/silver")
GOLD_D = Path("data/gold/dims")
GOLD_F = Path("data/gold/facts")
GOLD_D.mkdir(parents=True, exist_ok=True)
GOLD_F.mkdir(parents=True, exist_ok=True)

def build_dim_date():
    # 以 holidays 範圍為主，外加安全邊界（先用字串讀，再手動轉 datetime）
    hol = pd.read_csv(SILVER / "holidays/jp_holidays_silver.csv", dtype=str)
    hol["date"] = pd.to_datetime(hol["date"], errors="coerce")
    # 保險：去掉 NaT
    hol = hol.dropna(subset=["date"])

    dmin = hol["date"].min()
    dmax = hol["date"].max()
    if pd.isna(dmin) or pd.isna(dmax):
        raise RuntimeError("Holidays date range is empty after parsing. Please check silver/holidays CSV.")

    # 從 dmin 所在年的年初，到 dmax 之後延伸 2 年
    start = dmin.normalize().replace(month=1, day=1)
    end   = (dmax + pd.DateOffset(years=2)).normalize()

    dates = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"date": dates})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dow"] = df["date"].dt.weekday + 1   # 1=Mon ... 7=Sun
    df["is_weekend"] = df["dow"].isin([6,7])

    # 對應節日（flag + 名稱/類別）
    h = hol[["date","holiday_name","category"]].copy()
    df = df.merge(h, on="date", how="left")
    df["is_holiday"] = df["holiday_name"].notna()

    # 稅率（依日期區間）
    tax = pd.read_csv(SILVER / "tax/tax_rate_silver.csv", dtype=str)
    tax["start_date"] = pd.to_datetime(tax["start_date"], errors="coerce")
    tax["end_date"]   = pd.to_datetime(tax["end_date"], errors="coerce")
    df["tax_rate"] = np.nan
    for _, r in tax.iterrows():
        if pd.isna(r["start_date"]):
            continue
        mask = (df["date"] >= r["start_date"]) & (pd.isna(r["end_date"]) | (df["date"] <= r["end_date"]))
        # 轉 float（CSV 裡是字串）
        try:
            rate = float(r["tax_rate"]) if pd.notna(r["tax_rate"]) else np.nan
        except Exception:
            rate = np.nan
        df.loc[mask, "tax_rate"] = rate

    out = df[[
        "date_key","date","year","quarter","month","day","dow","is_weekend",
        "is_holiday","holiday_name","category","tax_rate"
    ]].copy()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    out.rename(columns={"category":"holiday_category"}, inplace=True)
    out.to_csv(GOLD_D / "dim_date.csv", index=False)
    print(f"✅ Saved: {GOLD_D/'dim_date.csv'} ({len(out)} rows)")

def build_dim_geo():
    jis = pd.read_csv(SILVER / "jis/jis_prefecture_city_silver.csv", dtype=str)
    # 清理 + 主鍵
    jis["pref_code"] = jis["pref_code"].astype(str).str.zfill(2)
    jis["city_code"] = jis["city_code"].astype(str).str.zfill(5)
    jis["city_key"] = jis["pref_code"] + "-" + jis["city_code"]
    out = jis[["city_key","pref_code","pref_name","city_code","city_name"]].drop_duplicates().copy()
    out.to_csv(GOLD_D / "dim_geo.csv", index=False)
    print(f"✅ Saved: {GOLD_D/'dim_geo.csv'} ({len(out)} rows)")

def build_fact_calendar():
    dim_date = pd.read_csv(GOLD_D / "dim_date.csv", dtype={"date_key":int})
    fact = dim_date[[
        "date_key","date","is_holiday","holiday_name","holiday_category","tax_rate"
    ]].copy()
    fact.to_csv(GOLD_F / "fact_calendar.csv", index=False)
    print(f"✅ Saved: {GOLD_F/'fact_calendar.csv'} ({len(fact)} rows)")

if __name__ == "__main__":
    build_dim_date()
    build_dim_geo()
    build_fact_calendar()
    print("🎉 Gold build done.")
