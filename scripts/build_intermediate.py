from pathlib import Path
import pandas as pd

BASE = Path("data/raw_official")
OUT  = Path("data/intermediate")
(OUT / "holidays").mkdir(parents=True, exist_ok=True)
(OUT / "jis").mkdir(parents=True, exist_ok=True)
(OUT / "tax").mkdir(parents=True, exist_ok=True)

def _pick_first(staging: Path, exts=(".xlsx", ".csv")) -> Path:
    cands = []
    for ext in exts:
        cands += sorted(staging.glob(f"*{ext}"))
    if not cands:
        raise FileNotFoundError(f"No XLSX/CSV found in {staging}")
    return cands[0]

def _read_any(p: Path) -> pd.DataFrame:
    if p.suffix.lower() == ".xlsx":
        return pd.read_excel(p, dtype=str)
    for enc in ("utf-8","cp932","shift_jis"):
        try:
            return pd.read_csv(p, dtype=str, encoding=enc)
        except Exception:
            pass
    return pd.read_csv(p, dtype=str, encoding="utf-8", errors="ignore")

# ---- holidays（沿用先前邏輯，略）----
def clean_holidays():
    src = BASE / "holidays/_staging"
    dst = OUT / "holidays/jp_holidays_clean.csv"
    try:
        df = _read_any(_pick_first(src))
    except Exception:
        df = pd.DataFrame(columns=["date","holiday_name","category"])
    cols = [c.strip().replace("\u3000","") for c in df.columns]
    df.columns = cols
    date_col = next((c for c in cols if ("月日" in c or "日付" in c or "年月日" in c)), None)
    name_col = next((c for c in cols if ("名" in c and ("祝" in c or "休日" in c))), None)
    if date_col and name_col:
        out = pd.DataFrame({
            "date": df[date_col],
            "holiday_name": df[name_col],
            "category": "国民の祝日"
        })
    else:
        out = pd.DataFrame(columns=["date","holiday_name","category"])
    out.to_csv(dst, index=False)
    print(f"✅ holidays → {dst} ({len(out)} rows)")

# ---- JIS：針對『団体コード／都道府県名（漢字）／市区町村名（漢字）』版型 ----
def clean_jis():
    src = BASE / "jis/_staging"
    raw = _read_any(_pick_first(src))

    # 正規化欄名：去全形空白、換行
    def norm(x): return str(x).replace("\u3000","").replace("\n","").strip()
    raw.columns = [norm(c) for c in raw.columns]

    # 可能的列名集合
    dantai_col = next((c for c in ("団体コード","全国地方公共団体コード","団体コード（JIS）") if c in raw.columns), None)
    pref_name_col = next((c for c in ("都道府県名（漢字）","都道府県名","都道府県") if c in raw.columns), None)
    city_name_col = next((c for c in ("市区町村名（漢字）","市区町村名","団体名","名称") if c in raw.columns), None)

    if not dantai_col:
        raise RuntimeError(f"JIS columns not found. Got: {list(raw.columns)}")

    codes = raw[dantai_col].astype(str).str.replace(r"\D","",regex=True)
    # 團體碼常見長度 6；前2=都道府縣，前5=市区町村
    pref_code = codes.str[:2].str.zfill(2)
    city_code = codes.str[:5].str.zfill(5)

    out = pd.DataFrame({"pref_code":pref_code, "city_code":city_code})

    # 名稱
    pref_map = {
        "01":"北海道","02":"青森県","03":"岩手県","04":"宮城県","05":"秋田県","06":"山形県","07":"福島県",
        "08":"茨城県","09":"栃木県","10":"群馬県","11":"埼玉県","12":"千葉県","13":"東京都","14":"神奈川県",
        "15":"新潟県","16":"富山県","17":"石川県","18":"福井県","19":"山梨県","20":"長野県","21":"岐阜県",
        "22":"静岡県","23":"愛知県","24":"三重県","25":"滋賀県","26":"京都府","27":"大阪府","28":"兵庫県",
        "29":"奈良県","30":"和歌山県","31":"鳥取県","32":"島根県","33":"岡山県","34":"広島県","35":"山口県",
        "36":"徳島県","37":"香川県","38":"愛媛県","39":"高知県","40":"福岡県","41":"佐賀県","42":"長崎県",
        "43":"熊本県","44":"大分県","45":"宮崎県","46":"鹿児島県","47":"沖縄県"
    }
    if pref_name_col and pref_name_col in raw.columns:
        out["pref_name"] = raw[pref_name_col]
    else:
        out["pref_name"] = out["pref_code"].map(pref_map)

    out["city_name"] = raw[city_name_col] if city_name_col and city_name_col in raw.columns else ""

    dst = OUT / "jis/jis_prefecture_city.csv"
    out = out[["pref_code","pref_name","city_code","city_name"]]
    # 去重（少數版本會有複本）
    out = out.drop_duplicates(subset=["city_code"], keep="first")
    out.to_csv(dst, index=False)
    print(f"✅ JIS → {dst} ({len(out)} rows)")

# ---- tax（沿用簡版）----
def clean_tax():
    src = BASE / "tax/_staging"
    dst = OUT / "tax/tax_rate_clean.csv"
    df = _read_any(_pick_first(src))
    df.columns = [c.strip() for c in df.columns]
    out = pd.DataFrame({
        "start_date": df.iloc[:,0],
        "end_date": df.iloc[:,1],
        "tax_rate": pd.to_numeric(df.iloc[:,2], errors="coerce")
    })
    out.to_csv(dst, index=False)
    print(f"✅ tax → {dst} ({len(out)} rows)")

if __name__ == "__main__":
    clean_holidays()
    clean_jis()
    clean_tax()
