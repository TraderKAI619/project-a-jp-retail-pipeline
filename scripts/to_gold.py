from pathlib import Path
import pandas as pd
import numpy as np

SILVER = Path("data/silver")
GOLD_D = Path("data/gold/dims")
GOLD_F = Path("data/gold/facts")
GOLD_D.mkdir(parents=True, exist_ok=True)
GOLD_F.mkdir(parents=True, exist_ok=True)

# ---------- Dim Date ----------
def build_dim_date():
    hol = pd.read_csv(SILVER / "holidays/jp_holidays_silver.csv", dtype=str)
    hol["date"] = pd.to_datetime(hol["date"], errors="coerce")
    hol = hol.dropna(subset=["date"])

    dmin = hol["date"].min()
    dmax = hol["date"].max()
    if pd.isna(dmin) or pd.isna(dmax):
        raise RuntimeError("Holidays date range is empty.")

    start = dmin.normalize().replace(month=1, day=1)
    end   = (dmax + pd.DateOffset(years=2)).normalize()

    dates = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"date": dates})
    df["date_key"]   = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"]       = df["date"].dt.year
    df["quarter"]    = df["date"].dt.quarter
    df["month"]      = df["date"].dt.month
    df["day"]        = df["date"].dt.day
    df["dow"]        = df["date"].dt.weekday + 1
    df["is_weekend"] = df["dow"].isin([6,7])

    # join holidays
    h = hol[["date","holiday_name","category"]].copy()
    h.rename(columns={"category":"holiday_category"}, inplace=True)
    df = df.merge(h, on="date", how="left")
    df["is_holiday"] = df["holiday_name"].notna()

    # attach tax_rate by effective range (merge_asof trick)
    tax = pd.read_csv(SILVER / "tax/tax_rate_silver.csv", dtype=str)
    tax["start_date"] = pd.to_datetime(tax["start_date"])
    tax["end_date"]   = pd.to_datetime(tax["end_date"], errors="coerce")
    tax = tax.sort_values("start_date").reset_index(drop=True)
    tax["next_start"] = tax["start_date"].shift(-1)
    tax["tax_rate"]   = pd.to_numeric(tax["tax_rate"], errors="coerce")
    # asof on start_date
    tmp = df[["date"]].sort_values("date")
    m   = pd.merge_asof(tmp, tax[["start_date","next_start","tax_rate"]].sort_values("start_date"),
                        left_on="date", right_on="start_date", direction="backward")
    mask = (m["next_start"].isna()) | (m["date"] < m["next_start"])
    df["tax_rate"] = np.where(mask, m["tax_rate"], np.nan)

    cols = ["date_key","date","year","quarter","month","day","dow",
            "is_weekend","is_holiday","holiday_name","holiday_category","tax_rate"]
    df[cols].to_csv(GOLD_D / "dim_date.csv", index=False)
    print(f"✅ Saved: {GOLD_D/'dim_date.csv'} ({len(df)})")

# ---------- Dim Geo ----------
def build_dim_geo():
    jis = pd.read_csv(SILVER / "jis/jis_prefecture_city_silver.csv", dtype=str)
    jis["city_key"] = jis["pref_code"].str.zfill(2) + "-" + jis["city_code"].str.zfill(5)
    out = jis[["city_key","pref_code","pref_name","city_code","city_name"]].drop_duplicates()
    out.to_csv(GOLD_D / "dim_geo.csv", index=False)
    print(f"✅ Saved: {GOLD_D/'dim_geo.csv'} ({len(out)})")

# ---------- Fact Calendar ----------
def build_fact_calendar():
    dd = pd.read_csv(GOLD_D / "dim_date.csv", parse_dates=["date"])
    fact = dd[["date_key","date","is_holiday","holiday_name","holiday_category","tax_rate"]].copy()
    fact.to_csv(GOLD_F / "fact_calendar.csv", index=False)
    print(f"✅ Saved: {GOLD_F/'fact_calendar.csv'} ({len(fact)})")

# ---------- Dim Product (NEW) ----------
def build_dim_product():
    products = [
        ("P001","飲料"), ("P002","零食"), ("P003","家居"),
        ("P004","美妝"), ("P005","文具"), ("P006","嬰幼"),
        ("P007","寵物"), ("P008","保健"),
    ]
    df = pd.DataFrame(products, columns=["product_key","category"])
    df.to_csv(GOLD_D / "dim_product.csv", index=False)
    print(f"✅ Saved: {GOLD_D/'dim_product.csv'} ({len(df)})")

# ---------- Fact Sales (NEW, synthetic) ----------
def build_fact_sales(seed=42, years=(2024,)):
    rng = np.random.default_rng(seed)

    dd  = pd.read_csv(GOLD_D / "dim_date.csv", dtype={"date_key":int}, parse_dates=["date"])
    geo = pd.read_csv(GOLD_D / "dim_geo.csv", dtype=str)
    prod= pd.read_csv(GOLD_D / "dim_product.csv", dtype=str)

    # 一年、50 個城市、8 產品 → 大約 146k rows
    dd = dd[dd["date"].dt.year.isin(years)]
    cities = geo.sample(n=min(50, len(geo)), random_state=seed)["city_key"].tolist()

    # 笛卡兒積（日期 × 城市 × 產品）
    base = (dd.assign(key=1)[["date_key","date","key"]]
              .merge(pd.DataFrame({"city_key":cities, "key":[1]*len(cities)}), on="key")
              .merge(prod.assign(key=1)[["product_key","key"]], on="key")
              .drop(columns="key"))

    # 隨機生成銷售
    base["units"]      = rng.integers(0, 40, size=len(base))          # 0~39
    base["unit_price"] = rng.choice([120,150,180,199,220,250,299], size=len(base)).astype(float)

    # 稅率：取該日 dim_date 稅率
    rate = dd[["date_key","tax_rate"]].copy()
    base = base.merge(rate, on="date_key", how="left")
    base["tax_rate"]   = pd.to_numeric(base["tax_rate"], errors="coerce").fillna(10.0)

    # 金額
    base["net_amount"]   = (base["units"] * base["unit_price"]).round(0)
    base["tax_amount"]   = (base["net_amount"] * (base["tax_rate"]/100.0)).round(0)
    base["gross_amount"] = base["net_amount"] + base["tax_amount"]

    cols = ["date_key","city_key","product_key","units","unit_price",
            "net_amount","tax_rate","tax_amount","gross_amount","revenue_jpy"]
    base[cols].to_csv(GOLD_F / "fact_sales.csv", index=False)
    print(f"✅ Saved: {GOLD_F/'fact_sales.csv'} ({len(base)})")

if __name__ == "__main__":
    GOLD_D.mkdir(parents=True, exist_ok=True)
    GOLD_F.mkdir(parents=True, exist_ok=True)
    build_dim_date()
    build_dim_geo()
    build_fact_calendar()
    build_dim_product()
    build_fact_sales()
    print("🎉 Gold build done.")
