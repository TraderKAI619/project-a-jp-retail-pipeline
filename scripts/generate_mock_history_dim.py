import pandas as pd, numpy as np
from datetime import datetime, timedelta
from pathlib import Path

Path("artifacts").mkdir(exist_ok=True)

N = 30
dates = pd.date_range(end=datetime.now(), periods=N, freq='D')

np.random.seed(42)
df = pd.DataFrame({
    "date": dates.date,
    "data_freshness_hours": np.random.uniform(1.0, 6.0, N).round(2),
    "prefecture_coverage_pct": 100.0,  # 47/47
    "municipality_join_consistency_pct": np.random.uniform(99.2, 99.9, N).round(2),
    "duplicate_pref_code_rate": np.random.uniform(0.0, 0.2, N).round(2),
    "duplicate_muni_code_rate": np.random.uniform(0.0, 0.4, N).round(2),
    "critical_null_rate": np.random.uniform(0.0, 0.3, N).round(2),
    "holidays_next30_count": np.random.randint(0, 4, N),
    "active_tax_rate_bands": np.random.randint(1, 3, N),
})

df.to_csv("artifacts/kpi_history.csv", index=False)
print("✅ artifacts/kpi_history.csv generated (reference-data mock)")
