Project A — Japan Retail Data Pipeline (MVP)

A production-ready batch ETL pipeline for Japanese retail analytics using the Medallion architecture.
Integrates official government data (holidays, consumption tax history, JIS region codes) with synthetic sales for KPI demos.

Perfect for portfolios, learning DE patterns, or as a template for JP-specific analytics.

Features

✅ Real Japanese complexity

振替休日 (substitute holiday) & 国民の休日 covered

Consumption tax SCD-2: 3% → 5% → 8% → 10% + 8% reduced rate

✅ Production patterns

Medallion layers with validations at each step

GitHub Actions CI (push + nightly)

Full provenance in SOURCES.md

✅ Demo-ready analytics

~140K synthetic sales rows with seasonality/holiday/tax effects

Pre-built KPI queries: holiday lift, tax impact, geo trends

## Architecture

The pipeline follows a **3-layer Medallion pattern**:

- **Raw**: official files as-is (holidays, JIS codes, tax history)
- **Intermediate**: encoding fixes, header normalization, de-duplication
- **Silver**: stable CSV schemas (data contracts) with basic constraints
- **Gold**: star schema (dims + facts) ready for BI tools
```mermaid
flowchart LR
    subgraph Raw["Raw (official sources)"]
      H[holidays/_staging]
      J[jis/_staging]
      T[tax/_staging]
    end

    subgraph INT["Intermediate"]
      ih[holidays_clean.csv]
      ij[jis_prefecture_city.csv]
      it[tax_rate_clean.csv]
    end

    subgraph SIL["Silver (stable)"]
      sh[jp_holidays_silver.csv]
      sj[jis_prefecture_city_silver.csv]
      st[tax_rate_silver.csv]
    end

    subgraph GOLD["Gold (analytics)"]
      dd[dim_date.csv]
      dg[dim_geo.csv]
      fc[fact_calendar.csv]
      dp[dim_product.csv]
      fs[fact_sales.csv]
    end

    H-->ih
    J-->ij
    T-->it
    ih-->sh
    ij-->sj
    it-->st
    sh-->dd
    st-->dd
    sj-->dg
    dd-->fc
    dd-->fs
    dg-->fs
    dp-->fs
```

Prerequisites

Python: 3.10–3.12 (tested on macOS/Linux/Windows)

pip for dependency management

(Optional for SQL demos) DuckDB CLI ≥ 0.9 or pip install duckdb

Disk space: < 50 MB (all layers + synthetic data)

Quick Start
1) Create & activate venv

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate


Windows (PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate

2) Install deps
pip install -r requirements.txt
# optional demos:
pip install duckdb

3) Build end-to-end + validations （⏱️ ~25–40s）
make everything
# runs: to_silver -> validate_silver -> to_gold -> validate_gold


Outputs

data/silver/{holidays,jis,tax}/...
data/gold/dims/{dim_date,dim_geo,dim_product}.csv
data/gold/facts/{fact_calendar,fact_sales}.csv

Demo Queries (DuckDB) 📊

Use DuckDB CLI or Python duckdb.
If your generator exports revenue_jpy (e.g., from generate_fake_sales.sql), replace gross_amount below with revenue_jpy.

① Holiday vs Non-holiday revenue uplift
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, is_holiday FROM read_csv_auto('data/gold/dims/dim_date.csv'))
SELECT is_holiday, SUM(gross_amount) AS revenue_jpy
FROM f JOIN d USING(date_key)
GROUP BY is_holiday
ORDER BY is_holiday;


Example output

is_holiday	revenue_jpy
FALSE	8,523,441
TRUE	9,871,223

Note: Pattern only; your numbers vary with seed — expect holiday > non-holiday.

② Tax boundary (2019/10 change)
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, tax_rate FROM read_csv_auto('data/gold/dims/dim_date.csv'))
SELECT tax_rate, ROUND(SUM(gross_amount)/1e8, 2) AS rev_億日圓
FROM f JOIN d USING(date_key)
WHERE date_key BETWEEN 20180801 AND 20201231
GROUP BY tax_rate
ORDER BY tax_rate;


Expected: 10% period slightly lower due to generator’s tax_penalty.

③ Prefecture × month ranking
WITH f AS (SELECT * FROM read_csv_auto('data/gold/facts/fact_sales.csv')),
     d AS (SELECT date_key, CAST(date_key/100 AS INT) AS yyyymm FROM read_csv_auto('data/gold/dims/dim_date.csv')),
     g AS (SELECT city_key, pref_code, pref_name FROM read_csv_auto('data/gold/dims/dim_geo.csv'))
SELECT g.pref_code, g.pref_name, d.yyyymm,
       ROUND(SUM(gross_amount)/1e8, 2) AS rev_億日圓
FROM f JOIN d USING(date_key) JOIN g USING(city_key)
GROUP BY 1,2,3
ORDER BY d.yyyymm, rev_億日圓 DESC;

Data Model

Classic star schema with 3 dimensions and 2 fact tables (calendar + sales).
```mermaid
erDiagram
    dim_date ||--o{ fact_calendar : "date_key"
    dim_date ||--o{ fact_sales    : "date_key"
    dim_geo  ||--o{ fact_sales    : "city_key"
    dim_product ||--o{ fact_sales : "product_key"

    dim_date {
      int    date_key PK
      date   date
      int    year
      int    quarter
      int    month
      int    day
      int    dow
      bool   is_weekend
      bool   is_holiday
      string holiday_name
      string holiday_category
      float  tax_rate
    }

    dim_geo {
      string city_key PK
      string pref_code
      string pref_name
      string city_code
      string city_name
    }

    fact_calendar {
      int    date_key FK
      date   date
      bool   is_holiday
      string holiday_name
      string holiday_category
      float  tax_rate
    }

    fact_sales {
      int    date_key FK
      string city_key  FK
      string product_key FK
      int    units
      float  unit_price
      float  net_amount
      float  tax_rate
      float  tax_amount
      float  gross_amount
    }
```

Project Structure (excerpt)
data/
  raw_official/{holidays,jis,tax}/_staging/
  intermediate/{holidays,jis,tax}/...
  silver/{holidays,jis,tax}/...
  gold/
    dims/{dim_date,dim_geo,dim_product}.csv
    facts/{fact_calendar,fact_sales}.csv
notebooks/{demo_duckdb.sql, demo_sales.sql, generate_fake_sales.sql}
scripts/*.py

Make Targets
make silver          # intermediate -> silver
make validate        # validate silver (schema, dates, unique keys)
make gold            # silver -> gold (adds synthetic product/sales)
make validate_gold   # gold checks (PK dup, negative amounts, row-count sanity)
make everything      # all of the above

Validations & CI/CD

Silver: required columns, date parseability, uniqueness（e.g., city_code）

Gold: PK duplicates, negative amounts guard, row-count sanity

GitHub Actions

CI on push/PR → make everything

Nightly ETL (cron) → refresh & keep green

Data Provenance

SOURCES.md records URLs, retrieval time (JST), file size & SHA256.

Update SHA quickly:

shasum -a 256 data/raw_official/tax/_staging/tax_rate_history.csv

Troubleshooting
Symptom	Likely cause	Fix
FileNotFoundError	Running outside repo root or _staging missing	Run from repo root; place official source files under data/raw_official/.../_staging/
UnicodeDecodeError	JP encoding variance in raw files	Built-in readers try multiple encodings; if it persists, re-save as UTF-8 first
Gold tables empty	Silver not built yet	Run make everything, confirm silver CSVs exist
Duplicate keys	Upstream duplicates or mixed versions	clean_* de-dups; if still present, verify upstream file version & refresh
Roadmap

Next (MVP+) — why it matters

 dbt port → industry-standard modeling/tests & easier CI

 dim_store + mapping to JIS → city/store cuts & store-level KPIs

 Export diagrams to /docs → easier onboarding (rendered PNGs)

Future

 Incremental loads → production-scale efficiency & cost control

 RLS / Column Mask demo → multi-tenant security patterns

 JAN checksum & name-normalization tests → realistic data-quality edge cases

License

MIT — see LICENSE
.
