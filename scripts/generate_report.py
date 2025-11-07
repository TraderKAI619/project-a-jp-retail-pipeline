import os, shutil, pandas as pd

os.makedirs("reports", exist_ok=True)
lines = ["# JP Retail Analytics — Daily Report", ""]

def add_table(path, title):
    lines.append(f"## {title}")
    if os.path.exists(path):
        df = pd.read_csv(path)
        lines.append(f"- rows: {len(df)}")
        lines.append("")
        try:
            lines.append(df.head(5).to_markdown(index=False))
            lines.append("")
        except Exception:
            pass
    else:
        lines.append(f"- file missing: {path}")
        lines.append("")

# 來源（analytics）→ 目的地（reports）
src_uplift = "data/analytics/top_prefecture_uplift.csv"
dst_uplift = "reports/uplift.csv"
if os.path.exists(src_uplift):
    shutil.copyfile(src_uplift, dst_uplift)
    print(f"Copied {src_uplift} -> {dst_uplift}")
else:
    print(f"[WARN] missing {src_uplift}; skip copy")

# 可選：一併同步另一份，之後寫報告也好用
src_cc = "data/analytics/category_contrib.csv"
dst_cc = "reports/category_contrib.csv"
if os.path.exists(src_cc):
    shutil.copyfile(src_cc, dst_cc)
    print(f"Copied {src_cc} -> {dst_cc}")

# 報告本體
add_table(src_cc, "Category contribution")
add_table(src_uplift, "Top prefecture uplift")

with open("reports/report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Wrote reports/report.md")
