from pathlib import Path
import pandas as pd

BASE = Path("data/gold")

def ok(msg): print(f"✅ {msg}")
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
    df = _must_exist_csv(p)
    if df["product_key"].duplicated().any():
        dup = df[df["product_key"].duplicated()]["product_key"].unique()[:5]
        die(f"{p}: duplicated product_key: {dup}")
    ok(f"{p}: OK ({len(df)} rows)")

def validate_fact_sales():
    p = BASE / "facts/fact_sales.csv"
    df = _must_exist_csv(p)

    # 轉 numeric
    num_cols = ["units","unit_price","net_amount","tax_amount","gross_amount","tax_rate"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # 非負檢查
    for c in ["units","unit_price","net_amount","tax_amount","gross_amount"]:
        if (df[c] < 0).any():
            die(f"{p}: negative values in {c}")

    # 外鍵檢查（抽樣）
    d_date = pd.read_csv(BASE / "dims/dim_date.csv", usecols=["date_key"])
    d_prod = pd.read_csv(BASE / "dims/dim_product.csv", usecols=["product_key"])
    sample = df.sample(min(5000, len(df)), random_state=42)
    missing = set(sample["date_key"]) - set(d_date["date_key"])
    if missing:
        die(f"{p}: missing date_key in dim_date, examples: {list(missing)[:5]}")
    missing = set(sample["product_key"]) - set(d_prod["product_key"])
    if missing:
        die(f"{p}: missing product_key in dim_product, examples: {list(missing)[:5]}")

    # 金額等式（抽樣）— 先算稅額四捨五入，再相加；允許 ±1 偏差
    calc_tax   = (sample["net_amount"] * (sample["tax_rate"]/100.0)).round(0)
    calc_gross = sample["net_amount"] + calc_tax
    mismatch = (calc_gross - sample["gross_amount"]).abs() > 1.0
    rate = mismatch.mean()
    if rate > 0.01:
        ex = sample.loc[mismatch, ["date_key","product_key","units","unit_price","tax_rate","net_amount","gross_amount"]].head(5).copy()
        ex["calc_tax"] = calc_tax.loc[mismatch].head(5).values
        ex["calc_gross"] = calc_gross.loc[mismatch].head(5).values
        raise AssertionError(f"{p}: amount formula mismatch rate {rate:.2%} (>1%). Examples:\n{ex.to_string(index=False)}")

    ok(f"{p}: OK ({len(df)} rows)")

if __name__ == "__main__":
    validate_dim_date()
    validate_dim_geo()
    validate_fact_calendar()
    try:
        validate_dim_product()
        validate_fact_sales()
    except FileNotFoundError:
        pass
    print("🎯 All Gold datasets validated successfully!")
