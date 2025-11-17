import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from pathlib import Path

Path("images").mkdir(exist_ok=True)
hist = pd.read_csv("artifacts/kpi_history.csv", parse_dates=["date"]).sort_values("date")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0,0].plot(hist["date"], hist["data_freshness_hours"])
axes[0,0].set_title("Freshness (hours)")
axes[0,0].axhline(24, ls="--", color='red', alpha=0.5)

axes[0,1].plot(hist["date"], hist["municipality_join_consistency_pct"])
axes[0,1].set_title("Municipality Join Consistency (%)")
axes[0,1].axhline(99.0, ls="--", color='red', alpha=0.5)

axes[1,0].plot(hist["date"], hist["duplicate_muni_code_rate"])
axes[1,0].set_title("Duplicate Municipality Code Rate (%)")
axes[1,0].axhline(0.5, ls="--", color='red', alpha=0.5)

axes[1,1].bar(hist["date"], hist["holidays_next30_count"])
axes[1,1].set_title("Holidays in Next 30 Days (count)")

for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))

plt.tight_layout()
plt.savefig("images/refdata_metrics.png", dpi=150)
print("📊 Saved images/refdata_metrics.png")
