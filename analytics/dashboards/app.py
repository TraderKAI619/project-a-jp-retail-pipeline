import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="GW需要分析", layout="wide")

@st.cache_data
def load_pref():
    return pd.read_csv("data/analytics/top_prefecture_uplift.csv")

@st.cache_data
def load_cat():
    return pd.read_csv("data/analytics/category_contrib.csv")

pref = load_pref()
cat  = load_cat()

st.title("🏪 ゴールデンウィーク需要分析（デモ）")
st.caption("デモ用プレースホルダー。実データに差し替え可能。")

c1, c2, c3 = st.columns(3)
c1.metric("GW押し上げ率（例）", "+42.3%")
c2.metric("最高成長地域", "東京都")
c3.metric("対象都道府県", f"{pref.shape[0]}")

st.subheader("🗾 都道府県別 Uplift")
fig1 = px.bar(
    pref, x="pref_name_ja", y="uplift_rate",
    labels={"pref_name_ja":"都道府県","uplift_rate":"Uplift"},
    title="都道府県別 GW 押し上げ率（デモ）"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🛍️ カテゴリー別 貢献度")
fig2 = px.bar(
    cat, x="category_name", y="uplift_contrib",
    labels={"category_name":"カテゴリー","uplift_contrib":"貢献度"},
    title="カテゴリー別 貢献度（デモ）"
)
st.plotly_chart(fig2, use_container_width=True)
