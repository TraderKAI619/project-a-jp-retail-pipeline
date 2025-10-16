import pandas as pd
from pathlib import Path

INTERMEDIATE = Path("data/intermediate/jis/jis_prefecture_city.csv")
SILVER       = Path("data/silver/jis/jis_prefecture_city_silver.csv")

pref_map = {
 "01":"北海道","02":"青森県","03":"岩手県","04":"宮城県","05":"秋田県","06":"山形県","07":"福島県",
 "08":"茨城県","09":"栃木県","10":"群馬県","11":"埼玉県","12":"千葉県","13":"東京都","14":"神奈川県",
 "15":"新潟県","16":"富山県","17":"石川県","18":"福井県","19":"山梨県","20":"長野県","21":"岐阜県",
 "22":"静岡県","23":"愛知県","24":"三重県","25":"滋賀県","26":"京都府","27":"大阪府","28":"兵庫県",
 "29":"奈良県","30":"和歌山県","31":"鳥取県","32":"島根県","33":"岡山県","34":"広島県","35":"山口県",
 "36":"徳島県","37":"香川県","38":"愛媛県","39":"高知県","40":"福岡県","41":"佐賀県","42":"長崎県",
 "43":"熊本県","44":"大分県","45":"宮崎県","46":"鹿児島県","47":"沖縄県"
}

df = pd.read_csv(INTERMEDIATE, dtype=str)
for c in ["pref_code","pref_name","city_code","city_name"]:
    if c not in df.columns: df[c] = None

# 保留前導零
df["pref_code"] = df["pref_code"].astype(str).str.replace(r"\D","",regex=True).str.zfill(2)
df["city_code"] = df["city_code"].astype(str).str.replace(r"\D","",regex=True).str.zfill(5)

# 回填都道府縣名稱
need_fill = df["pref_name"].isna() | (df["pref_name"].astype(str).str.strip()=="")
df.loc[need_fill, "pref_name"] = df.loc[need_fill, "pref_code"].map(pref_map)

# city_name 若完全缺，先填空字串避免「全是 NaN」的驗證失敗（之後可再精修）
if df["city_name"].isna().all():
    df["city_name"] = ""

df = df[["pref_code","pref_name","city_code","city_name"]]
df.to_csv(SILVER, index=False)
print(f"✅ Fixed JIS silver written: {SILVER} ({len(df)} rows)")
