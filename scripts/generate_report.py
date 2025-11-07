import os
import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path

REPORTS_DIR = Path("reports")
ANALYTICS_DIR = Path("data/analytics")

# analytics 來源
SRC_UPLIFT = ANALYTICS_DIR / "top_prefecture_uplift.csv"
SRC_CONTRIB = ANALYTICS_DIR / "category_contrib.csv"

# reports 輸出
DST_UPLIFT = REPORTS_DIR / "uplift.csv"
DST_CONTRIB = REPORTS_DIR / "category_contrib.csv"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

lines = ["# JP Retail Analytics — Daily Report", ""]

def add_table(path: Path, title: str):
    lines.append(f"## {title}")
    if path.exists():
        try:
            df = pd.read_csv(path)
            lines.append(f"- rows: {len(df)}")
            lines.append("")
            try:
                lines.append(df.head(5).to_markdown(index=False))
                lines.append("")
            except Exception:
                # markdown 需要可選依賴（tabulate）；缺少就略過表格
                pass
        except Exception as e:
            lines.append(f"- failed to read: {path} ({e})")
            lines.append("")
    else:
        lines.append(f"- file missing: {path}")
        lines.append("")

# 1) 確保 analytics 產出（任一缺就呼叫 SQL 產生腳本）
if not (SRC_UPLIFT.exists() and SRC_CONTRIB.exists()):
    try:
        subprocess.run([sys.executable, "scripts/run_gw_sql.py"], check=True)
    except Exception as e:
        print(f"Warning: couldn't build analytics via run_gw_sql.py: {e}")

# 2) 一定要在 reports/ 放出檔案
# 2a) uplift
if SRC_UPLIFT.exists():
    shutil.copyfile(SRC_UPLIFT, DST_UPLIFT)
    print(f"Copied {SRC_UPLIFT} -> {DST_UPLIFT}")
else:
    DST_UPLIFT.write_text("prefecture,uplift\n", encoding="utf-8")
    print(f"Created placeholder {DST_UPLIFT} (analytics source missing)")

# 2b) category_contrib
if SRC_CONTRIB.exists():
    shutil.copyfile(SRC_CONTRIB, DST_CONTRIB)
    print(f"Copied {SRC_CONTRIB} -> {DST_CONTRIB}")
else:
    DST_CONTRIB.write_text("category,share\n", encoding="utf-8")
    print(f"Created placeholder {DST_CONTRIB} (analytics source missing)")

# 3) 組出 report.md
add_table(Path("data/gold/facts/fact_sales.csv"), "fact_sales (head)")
add_table(SRC_UPLIFT, "Top Prefecture Uplift (analytics)")
add_table(DST_UPLIFT, "Exported uplift (reports/uplift.csv)")
add_table(SRC_CONTRIB, "Category Contribution (analytics)")
add_table(DST_CONTRIB, "Exported category contrib (reports/category_contrib.csv)")

(REPORTS_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")
print("Wrote reports/report.md")
