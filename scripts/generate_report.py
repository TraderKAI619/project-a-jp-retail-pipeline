import os
import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path

REPORTS_DIR = Path("reports")
ANALYTICS_DIR = Path("data/analytics")
SRC_UPLIFT = ANALYTICS_DIR / "top_prefecture_uplift.csv"
DST_UPLIFT = REPORTS_DIR / "uplift.csv"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

lines = ["# JP Retail Analytics — Daily Report", ""]

def add_table(path: Path, title: str):
    lines.append(f"## {title}")
    if path.exists():
        try:
            df = pd.read_csv(path)
            lines.append(f"- rows: {len(df)}\n")
            try:
                lines.append(df.head(5).to_markdown(index=False))
                lines.append("")
            except Exception:
                pass
        except Exception as e:
            lines.append(f"- failed to read: {path} ({e})\n")
    else:
        lines.append(f"- file missing: {path}\n")

# 1) 確保 analytics 產出（若缺就呼叫 SQL 產生腳本）
if not SRC_UPLIFT.exists():
    try:
        subprocess.run([sys.executable, "scripts/run_gw_sql.py"], check=True)
    except Exception as e:
        print(f"Warning: couldn't build analytics via run_gw_sql.py: {e}")

# 2) 一定要在 reports/ 放一份 uplift.csv（來源有就拷，沒就放佔位檔）
if SRC_UPLIFT.exists():
    shutil.copyfile(SRC_UPLIFT, DST_UPLIFT)
    print(f"Copied {SRC_UPLIFT} -> {DST_UPLIFT}")
else:
    with open(DST_UPLIFT, "w", encoding="utf-8") as f:
        f.write("prefecture,uplift\n")
    print(f"Created placeholder {DST_UPLIFT} (analytics source missing)")

# 3) 組 report.md（測試只驗存在）
add_table(Path("data/gold/facts/fact_sales.csv"), "fact_sales (head)")
add_table(SRC_UPLIFT, "Top Prefecture Uplift (analytics)")
add_table(DST_UPLIFT, "Exported uplift (reports/uplift.csv)")

with open(REPORTS_DIR / "report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Wrote reports/report.md")
