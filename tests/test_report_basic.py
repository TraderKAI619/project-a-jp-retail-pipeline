from pathlib import Path
import subprocess
import sys
import pytest

@pytest.mark.skipif(
    not (Path("data/gold/facts/fact_sales.csv").exists()
         and Path("data/gold/dims/dim_date.csv").exists()),
    reason="gold not built",
)
def test_report_generated():
    r = subprocess.run([sys.executable, "scripts/generate_report.py"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert Path("reports/report.md").exists()
    assert Path("reports/uplift.csv").exists()
