import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from pathlib import Path

outdir = Path("reports/figures")
outdir.mkdir(parents=True, exist_ok=True)

# === ① 都道府県別 GW uplift ===
df_pref = pd.read_csv("data/analytics/top_prefecture_uplift.csv")

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(df_pref["pref_name_ja"], df_pref["uplift_rate"], color="skyblue")
ax1.set_xlabel("上振れ率 (%)", fontsize=12)
ax1.set_ylabel("都道府県名", fontsize=12)
ax1.set_xlim(0, df_pref["uplift_rate"].max() * 1.1)

for i, v in enumerate(df_pref["uplift_rate"]):
    ax1.text(v + 0.01, i, f"{v*100:.1f}%", va="center", fontsize=10)

plt.tight_layout()
plt.savefig(outdir / "top_prefecture_uplift.png", bbox_inches="tight")
plt.close(fig1)

# === ② 首都圏 vs 地方 ===
tokyo_area = [13, 14, 11, 12]
df_region = df_pref[df_pref["pref_code"].isin(tokyo_area)]
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(df_region["pref_name_ja"], df_region["uplift_rate"], color="lightcoral")
ax2.set_xlabel("上振れ率 (%)", fontsize=12)
for i, v in enumerate(df_region["uplift_rate"]):
    ax2.text(v + 0.01, i, f"{v*100:.1f}%", va="center", fontsize=10)

plt.tight_layout()
plt.savefig(outdir / "region_comparison.png", bbox_inches="tight")
plt.close(fig2)

# === ③ 品類別寄与度 ===
df_cat = pd.read_csv("data/analytics/category_contrib.csv")
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(df_cat["category_name"], df_cat["uplift_contrib"], color="lightgreen")
ax3.set_ylabel("売上寄与度 (%)", fontsize=12)
plt.xticks(rotation=30, ha='right')
for i, v in enumerate(df_cat["uplift_contrib"]):
    ax3.text(i, v + 0.01, f"{v*100:.1f}%", ha="center", fontsize=10)

plt.tight_layout()
plt.savefig(outdir / "category_contrib.png", bbox_inches="tight")
plt.close(fig3)

print("✅ Saved all charts to reports/figures/")
