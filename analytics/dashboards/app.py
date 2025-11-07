import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="GW需要分析", layout="wide")

@st.cache_data
def load():
    return pd.read_csv("data/analytics/top_prefecture_uplift.csv")

df = load()

st.title("🏪 ゴールデンウィーク需要分析（デモ）")
st.caption("デモ用プレースホルダー。実データに差し替え可能。")

c1,c2,c3 = st.columns(3)
c1.metric("GW押し上げ率（例）", "+42.3%")
c2.metric("最高成長地域", "東京都")
c3.metric("対象都道府県", f"{df.shape[0]}")

fig = px.bar(df, x="pref_name_ja", y="uplift_rate", labels={"pref_name_ja":"都道府県","uplift_rate":"Uplift"})
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)
