from pathlib import Path
import pandas as pd

BASE = Path("data/silver")

checks = [
    {
        "path": BASE / "holidays/jp_holidays_silver.csv",
        "required_cols": ["date","holiday_name","category"],
        "date_cols": ["date"],
        "unique_keys": [["date","holiday_name"]],
    },
    {
        "path": BASE / "jis/jis_prefecture_city_silver.csv",
        "required_cols": ["pref_code","pref_name","city_code","city_name"],
        "date_cols": [],
        "unique_keys": [["city_code"], ["pref_code","city_name"]],
    },
    {
        "path": BASE / "tax/tax_rate_silver.csv",
        "required_cols": ["start_date","end_date","tax_rate"],
        "date_cols": ["start_date","end_date"],
        "unique_keys": [["start_date","end_date"]],
    },
]

def validate_file(spec):
    p = spec["path"]
    df = pd.read_csv(p, dtype=str)
    # 欄位存在
    for c in spec["required_cols"]:
        assert c in df.columns, f"{p}: missing column {c}"
    # 日期轉型（允許 end_date 空）
    for c in spec["date_cols"]:
        if c in df.columns:
            ok = pd.to_datetime(df[c], errors="coerce")
            # 允許空值，但不允許非空卻轉不成日期
            bad = df[c].notna() & (ok.isna())
            assert not bad.any(), f"{p}: bad date values in column {c}"
    # 空值比例（允許 end_date 空；其餘欄位不可全空）
    for c in spec["required_cols"]:
        if c == "end_date":
            continue
        assert df[c].notna().any(), f"{p}: column {c} all null"
    # 重複鍵
    for key in spec["unique_keys"]:
        dup = df.duplicated(subset=key).sum()
        assert dup == 0, f"{p}: duplicated keys on {key}"
    print(f"✅ {p}: OK ({len(df)} rows)")

def main():
    for spec in checks:
        validate_file(spec)
    print("🎯 All Silver datasets validated successfully!")

if __name__ == "__main__":
    main()
