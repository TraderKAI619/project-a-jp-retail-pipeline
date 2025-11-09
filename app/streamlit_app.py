import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
