from pathlib import Path
import pandas as pd

BASE = Path("data/silver")

SPECS = [
    {
        "path": BASE / "holidays/jp_holidays_silver.csv",
        "required_cols": ["date","holiday_name","category"],
        "date_cols": ["date"],
        # 同一天同名不可重複
        "unique_keys": [["date","holiday_name"]],
    },
    {
        "path": BASE / "jis/jis_prefecture_city_silver.csv",
        "required_cols": ["pref_code","pref_name","city_code","city_name"],
        "date_cols": [],
        # ✔ JIS 唯一鍵：city_code（官方碼，天然唯一）
        "unique_keys": [["city_code"]],
    },
    {
        "path": BASE / "tax/tax_rate_silver.csv",
        "required_cols": ["start_date","end_date","tax_rate"],
        "date_cols": ["start_date","end_date"],
        # 稅率期間可重疊，但單純檢查起日+稅率不重複（鬆檢）
        "unique_keys": [["start_date","tax_rate"]],
    },
]

def validate_file(spec):
    p = spec["path"]
    df = pd.read_csv(p, dtype=str)

    # 必要欄
    for c in spec["required_cols"]:
        assert c in df.columns, f"{p}: missing column {c}"

    # 日期欄可解析且非全空
    for c in spec["date_cols"]:
        parsed = pd.to_datetime(df[c], errors="coerce")
        assert parsed.notna().any(), f"{p}: column {c} all null after parse"

    # 唯一鍵
    for key in spec["unique_keys"]:
        dup = df.duplicated(subset=key).sum()
        assert dup == 0, f"{p}: duplicated keys on {key}"

    print(f"✅ {p}: OK ({len(df)} rows)")

def main():
    for s in SPECS:
        validate_file(s)
    print("🎯 All Silver datasets validated successfully!")

if __name__ == "__main__":
    main()
