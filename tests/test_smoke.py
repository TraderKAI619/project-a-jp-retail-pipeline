import os, csv

def test_report_exists():
    assert os.path.exists("reports/report.md")

def test_category_contrib_csv_has_rows():
    path = "data/analytics/category_contrib.csv"
    assert os.path.exists(path)
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 2  # 含表頭＋至少一行資料

def test_top_prefecture_uplift_csv_has_rows():
    path = "data/analytics/top_prefecture_uplift.csv"
    assert os.path.exists(path)
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 2
