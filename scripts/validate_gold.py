import json
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "gold"
SCHEMAS = ROOT / "schemas"

def check_with_schema(df: pd.DataFrame, schema_file: str):
    """验证 DataFrame 符合 JSON schema"""
    s = json.loads((SCHEMAS / schema_file).read_text(encoding="utf-8"))
    cols = s["columns"]
    
    # 必填字段
    for c in s.get("notNull", []):
        assert c in df.columns and df[c].notna().all(), f"{c} has NULL"
    
    # 字段存在性
    for c in cols:
        assert c in df.columns, f"missing column: {c}"
    
    # 唯一性约束
    for uniq in s.get("uniques", []):
        assert df.duplicated(subset=uniq).sum() == 0, f"duplicate keys in {uniq}"

def validate_csv(path: pathlib.Path) -> tuple[bool, int]:
    """验证单个 CSV 文件"""
    try:
        df = pd.read_csv(path)
        return True, len(df)
    except Exception as e:
        print(f"❌ {path}: FAILED - {e}")
        return False, 0

def main():
    files = [
        GOLD / "dims" / "dim_date.csv",
        GOLD / "dims" / "dim_geo.csv",
        GOLD / "facts" / "fact_calendar.csv",
        GOLD / "dims" / "dim_product.csv",
        GOLD / "facts" / "fact_sales.csv",
    ]
    
    all_ok = True
    for f in files:
        ok, rows = validate_csv(f)
        if ok:
            print(f"✅ {f}: OK ({rows} rows)")
        else:
            all_ok = False
    
    # Schema 验证
    if all_ok and (SCHEMAS / "gold_fact_sales.json").exists():
        df_sales = pd.read_csv(GOLD / "facts" / "fact_sales.csv")
        try:
            check_with_schema(df_sales, "gold_fact_sales.json")
            print("✅ gold_fact_sales schema validation: PASSED")
        except AssertionError as e:
            print(f"❌ gold_fact_sales schema validation: FAILED - {e}")
            all_ok = False
    
    if all_ok:
        print("🎯 All Gold datasets validated successfully!")
    else:
        raise SystemExit("Gold validation failed")

if __name__ == "__main__":
    main()
