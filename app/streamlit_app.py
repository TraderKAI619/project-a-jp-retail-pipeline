import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

<<<<<<< Updated upstream
st.set_page_config(page_title="Golden Week Analysis Dashboard 🇯🇵", layout="wide")

st.title("📊 Golden Week 分析結果（GW Analysis Dashboard）")
st.markdown("本 Dashboard 以都道府縣別、區域別及品類別展示 Golden Week 期間的上振れ率與貢獻度。")

# --- Load data ---
pref_df = pd.read_csv("data/analytics/top_prefecture_uplift.csv")
cat_df = pd.read_csv("data/analytics/category_contrib.csv")

# --- Prefecture uplift chart ---
st.header("🗾 1️⃣ 地域別上振れ率（都道府縣別）")
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.barh(pref_df["pref_name"], pref_df["uplift_pct"], color="skyblue")
ax1.set_xlabel("上振れ率 (%)")
ax1.set_ylabel("都道府縣名")
st.pyplot(fig1)

# --- Region comparison chart (optional) ---
try:
    region_df = pd.read_csv("data/analytics/region_comparison.csv")
    st.header("📈 2️⃣ 首都圏 vs 地方（比較）")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(region_df["region"], region_df["uplift_pct"], color=["#0066cc", "#99ccff"])
    ax2.set_ylabel("上振れ率 (%)")
    st.pyplot(fig2)
except FileNotFoundError:
    st.info("地域別比較データがまだ生成されていません。")

# --- Category contribution chart ---
st.header("🛍️ 3️⃣ 商品カテゴリ別貢献度")
fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.barh(cat_df["category"], cat_df["contribution_pct"], color="lightgreen")
ax3.set_xlabel("貢献度 (%)")
ax3.set_ylabel("カテゴリ")
st.pyplot(fig3)

st.markdown("---")
st.caption("© 2025 Project A — Japan Retail Data Pipeline (Synthetic Data, Reproducible, MIT License)")
=======
# 🔥 就这一行！自动处理日文字体
import japanize_matplotlib

st.set_page_config(page_title="Golden Week Retail Demand Dashboard", layout="wide")

st.title("🇯🇵 Golden Week Retail Demand Dashboard")
st.caption("Data: Synthetic JP Retail Data | Last Updated: 2025-11-08")

# === ① 都道府県別 GW uplift ===
st.header("都道府県別:GW期間の売上上振れ率")

df_pref = pd.read_csv("data/analytics/top_prefecture_uplift.csv")

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(df_pref["pref_name_ja"], df_pref["uplift_rate"], color="skyblue")
ax1.set_xlabel("上振れ率 (%)", fontsize=12)
ax1.set_ylabel("都道府県名", fontsize=12)
ax1.set_xlim(0, df_pref["uplift_rate"].max() * 1.1)

for i, v in enumerate(df_pref["uplift_rate"]):
    ax1.text(v + 0.01, i, f"{v*100:.1f}%", va="center", fontsize=10)

plt.subplots_adjust(left=0.2)
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# === ② 首都圏 vs 地方 ===
st.header("首都圏 vs 地方:地域別比較")

region_option = st.selectbox(
    "地域を選択してください:",
    ("首都圏", "地方")
)

if region_option == "首都圏":
    df_region = df_pref[df_pref["pref_code"].isin([13, 14, 11, 12])]
else:
    df_region = df_pref[~df_pref["pref_code"].isin([13, 14, 11, 12])]

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(df_region["pref_name_ja"], df_region["uplift_rate"], color="lightcoral")
ax2.set_xlabel("上振れ率 (%)", fontsize=12)

for i, v in enumerate(df_region["uplift_rate"]):
    ax2.text(v + 0.01, i, f"{v*100:.1f}%", va="center", fontsize=10)

plt.subplots_adjust(left=0.2)
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# === ③ 品類別寄与度 ===
st.header("品類別寄与度")

df_cat = pd.read_csv("data/analytics/category_contrib.csv")

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(df_cat["category_name"], df_cat["uplift_contrib"], color="lightgreen")
ax3.set_ylabel("売上寄与度 (%)", fontsize=12)
plt.xticks(rotation=30, ha='right')

for i, v in enumerate(df_cat["uplift_contrib"]):
    ax3.text(i, v + 0.01, f"{v*100:.1f}%", ha="center", fontsize=10)

plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

st.success("✅ Dashboard loaded successfully!")
>>>>>>> Stashed changes
