from pathlib import Path
import pandas as pd

BASE = Path("data/gold")

def ok(msg): print(f"✅ {msg}")
def die(msg): raise AssertionError(msg)

def validate_dim_date():
    p = BASE / "dims/dim_date.csv"
    df = pd.read_csv(p, dtype={"date_key":int})
    if not p.exists() or df.empty:
        die(f"{p} is missing or empty")
    if df["date_key"].duplicated().any():
        dup = df[df["date_key"].duplicated()]["date_key"].unique()[:5]
        die(f"{p}: duplicated date_key examples: {dup}")
    pd.to_datetime(df["date"], errors="raise")
    ok(f"{p}: OK ({len(df)} rows)")

def validate_dim_geo():
    p = BASE / "dims/dim_geo.csv"
    df = pd.read_csv(p, dtype=str)
    if not p.exists() or df.empty:
        die(f"{p} is missing or empty")
    if df["city_key"].duplicated().any():
        dup = df[df["city_key"].duplicated()]["city_key"].unique()[:5]
        die(f"{p}: duplicated city_key examples: {dup}")
    assert df["city_code"].notna().all(), f"{p}: city_code has nulls"
    ok(f"{p}: OK ({len(df)} rows)")

def validate_fact_calendar():
    p = BASE / "facts/fact_calendar.csv"
    df = pd.read_csv(p, dtype={"date_key":int})
    if not p.exists() or df.empty:
        die(f"{p} is missing or empty")
    if df["date_key"].duplicated().any():
        dup = df[df["date_key"].duplicated()]["date_key"].unique()[:5]
        die(f"{p}: duplicated date_key examples: {dup}")
    dim_date = pd.read_csv(BASE / "dims/dim_date.csv", dtype={"date_key":int})
    missing = set(df["date_key"]) - set(dim_date["date_key"])
    assert len(missing) == 0, f"{p}: FK to dim_date missing keys, examples: {list(missing)[:5]}"
    ok(f"{p}: OK ({len(df)} rows)")

if __name__ == "__main__":
    validate_dim_date()
    validate_dim_geo()
    validate_fact_calendar()
    print("🎯 All Gold datasets validated successfully!")
