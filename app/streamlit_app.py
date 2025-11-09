import matplotlib
matplotlib.use('Agg')  # 先設定 backend

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# === 強制重新載入字體快取 ===
import os
import shutil

# 清除 matplotlib 字體快取
cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "matplotlib")
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)

# 重新建立字體管理器
fm._load_fontmanager(try_read_cache=False)

# 設定日文字體
plt.rcParams['font.family'] = ['IPAGothic', 'IPAMincho', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# === Page setup ===
st.set_page_config(page_title="Golden Week Retail Demand Dashboard", layout="wide")

st.title("🇯🇵 Golden Week 分析結果（GW Analysis Dashboard）")
st.caption("Data: Synthetic JP Retail Data | Last Updated: 2025-11-08")

st.markdown("本 Dashboard 以都道府縣別、區域別及品類別展示 Golden Week 期間的上振れ率與貢獻度。")

# === 💡 商業價値セクション ===
st.markdown("""
### 💡 このダッシュボードが支援する意思決定

**マーケティング戦略**  
首都圏 vs 地方の上振れ率差異を可視化し、地域別プロモーション予算配分を最適化

**在庫計画**  
Golden Week 期間中の商品カテゴリ別貢献度から、連休前の発注量を精緻化

**売上予測**  
祝日・税率変更の影響を定量化し、予算策定の精度を向上

---

📊 **データ品質**: 95% validation pass rate  
🏗️ **アーキテクチャ**: Medallion (Bronze → Silver → Gold)  
🔒 **コンプライアンス**: 合成データ使用 (MIT License)
""")

st.markdown("---")

# === ① 都道府県別 GW uplift ===
st.header("🗾 1️⃣ 地域別上振れ率（都道府縣別）")

df_pref = pd.read_csv("data/analytics/top_prefecture_uplift.csv")

# 動態偵測欄位名稱（防止 KeyError）
if "pref_name" in df_pref.columns:
    name_col = "pref_name"
elif "pref_name_ja" in df_pref.columns:
    name_col = "pref_name_ja"
elif "prefecture" in df_pref.columns:
    name_col = "prefecture"
else:
    name_col = df_pref.columns[0]

uplift_col = "uplift_rate" if "uplift_rate" in df_pref.columns else "uplift_pct"

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(df_pref[name_col], df_pref[uplift_col], color="skyblue")
ax1.set_xlabel("上振れ率 (%)", fontsize=12)
ax1.set_ylabel("都道府縣名", fontsize=12)
plt.subplots_adjust(left=0.2)
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# === ② 首都圏 vs 地方 ===
st.header("📈 2️⃣ 首都圏 vs 地方（地域別比較）")

region_option = st.selectbox("地域を選択してください:", ("首都圏", "地方"))

if "pref_code" in df_pref.columns:
    if region_option == "首都圏":
        df_region = df_pref[df_pref["pref_code"].isin([13, 14, 11, 12])]
    else:
        df_region = df_pref[~df_pref["pref_code"].isin([13, 14, 11, 12])]
else:
    df_region = df_pref

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(df_region[name_col], df_region[uplift_col], color="lightcoral")
ax2.set_xlabel("上振れ率 (%)", fontsize=12)
plt.subplots_adjust(left=0.2)
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# === ③ 商品カテゴリ別貢献度 ===
st.header("🛍️ 3️⃣ 商品カテゴリ別貢献度")

df_cat = pd.read_csv("data/analytics/category_contrib.csv")

cat_name_col = "category" if "category" in df_cat.columns else "category_name"
contrib_col = "contribution_pct" if "contribution_pct" in df_cat.columns else "uplift_contrib"

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(df_cat[cat_name_col], df_cat[contrib_col], color="lightgreen")
ax3.set_ylabel("貢献度 (%)", fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

st.markdown("---")
st.caption("© 2025 Project A — Japan Retail Data Pipeline (Synthetic Data, Reproducible, MIT License)")
st.success("✅ Dashboard loaded successfully!")
