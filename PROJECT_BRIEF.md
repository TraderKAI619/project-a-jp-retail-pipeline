# PROJECT_BRIEF – Project A (JP Retail/EC Batch Pipeline)

## Purpose
Build a reproducible **batch data pipeline** for **Japan retail/EC** that supports:
- **Seasonality / long-holiday analysis** (national holidays, GW/Obon/New Year)
- **Consumption tax SCD2** (store tax-exclusive & tax-inclusive side by side, with rate history incl. 8% reduced rate)
- **Region keys** (JIS X0401/0402 prefecture/city + store key)
- **Customer record linkage (名寄せ)**: full/half width, Kana/kanji, voiced/semi-voiced, whitespace normalization
- **Product identifier**: JAN field + checksum
- **Security & privacy**: Row-Level Security (prefecture/department), Column Masking (phone/email)

## Scope
**In**  
`dim_calendar`, `dim_tax_rate (SCD2)`, `dim_region (JIS)`, `dim_product (with JAN)`, `dim_customer (name matching)`, `fct_sales`, data quality/monitoring, Runbook, README_ja.

**Out**  
Any real PII or confidential business data. This repo uses **official reference tables + synthetic transactions/master data** only.

## Tech Stack
- **AWS**: S3 / Lake Formation / Athena / Glue / Step Functions (or Redshift variant)
- **Modeling/Orchestration**: dbt (stg/int/dim/fct, tests, seeds)
- **CI**: sqlfluff, dbt test (later)
- **Docs**: README (EN) / README_ja, Runbook

## Definition of Done (DoD)
1. `README_ja` complete and **all official sources traceable** (holidays/tax/JIS/GS1).
2. Both **Historic (one-off full load)** and **Daily (incremental)** paths are reproducible.
3. Tests exist for **tax-rate switch**, **holiday/連休 logic**, **name normalization**, **JAN checksum** (incl. edge cases).
4. **RLS (prefecture/department)** + **Column Mask** minimal runnable example.
5. **Canary queries** all pass; include basic **cost/perf notes** (e.g., scan size).

## Risks & Assumptions
- Official reference tables are publicly accessible; synthetic data will be crafted to hit boundary cases.
- Cost estimates focus on Athena scan sizes; org-internal DWH costs are out of scope.

## Placeholders
- **Sources**: will be added in `SOURCES.md` at Step 4/8.
- **Diagrams**: will live under `/docs` at Step 6/10.
