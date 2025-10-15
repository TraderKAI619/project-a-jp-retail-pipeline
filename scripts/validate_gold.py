from pathlib import Path
import pandas as pd

BASE = Path("data/gold")

def ok(msg): print(f"✅ {msg}")
def skip(msg): print(f"⏭️ {msg}")
def die(msg): raise AssertionError(msg)

def _must_exist_csv(p: Path) -> pd.DataFrame:
    if not p.exists():
        die(f"{p} is missing")
    df = pd.read_csv(p)
    if df.empty:
        die(f"{p} is empty")
    return df

def validate_dim_date():
    p = BASE / "dims/dim_date.csv"
    df = _must_exist_csv(p)
    if df["date_key"].duplicated().any():
        dup = df[df["date_key"].duplicated()]["date_key"].unique()[:5]
        die(f"{p}: duplicated date_key examples: {dup}")
    pd.to_datetime(df["date"], errors="raise")
    ok(f"{p}: OK ({len(df)} rows)")

def validate_dim_geo():
    p = BASE / "dims/dim_geo.csv"
    df = _must_exist_csv(p)
    if df["city_key"].duplicated().any():
        dup = df[df["city_key"].duplicated()]["city_key"].unique()[:5]
        die(f"{p}: duplicated city_key examples: {dup}")
    ok(f"{p}: OK ({len(df)} rows)")

def validate_fact_calendar():
    p = BASE / "facts/fact_calendar.csv"
    df = _must_exist_csv(p)
    ok(f"{p}: OK ({len(df)} rows)")

def validate_dim_product():
    p = BASE / "dims/dim_product.csv"
    if not p.exists():
        skip(f"{p}: skipped (not found)")
        return
    df = _must_exist_csv(p)
    if df["product_key"].duplicated().any():
        dup = df[df["product_key"].duplicated()]["product_key"].unique()[:5]
        die(f"{p}: duplicated product_key: {dup}")
    ok(f"{p}: OK ({len(df)} rows)")

def validate_fact_sales():
    p = BASE / "facts/fact_sales.csv"
    if not p.exists():
        skip(f"{p}: skipped (not found)")
        return
    df = _must_exist_csv(p)
    # 基本合理性檢查
    for c in ["units","unit_price","net_amount","tax_amount","gross_amount"]:
        if (df[c] < 0).any():
            die(f"{p}: negative values in {c}")
    ok(f"{p}: OK ({len(df)} rows)")

if __name__ == "__main__":
    validate_dim_date()
    validate_dim_geo()
    validate_fact_calendar()
    validate_dim_product()
    validate_fact_sales()
    print("🎯 All Gold datasets validated successfully!")
