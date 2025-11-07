import os, pandas as pd

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

add_table("data/analytics/category_contrib.csv", "Category contribution")
add_table("data/analytics/top_prefecture_uplift.csv", "Top prefecture uplift")

with open("reports/report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Wrote reports/report.md")
