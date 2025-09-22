# MODULES_AND_DOD – list & acceptance

> Repo uses **official reference tables + synthetic data** to cover realistic JP scenarios and edge cases.

## Modules
- `dim_calendar` – national holidays / 振替休日 / 国民の休日 + **long-holiday (連休) rule**
- `dim_tax_rate` – **SCD2** (`valid_from`, `valid_to`, `is_current`), incl. **8% reduced rate**
- `dim_region` – **JIS X0401/0402** prefecture/city + store key
- `dim_product` – **JAN** field and checksum
- `dim_customer` – **name normalization (名寄せ)**: full/half width, Kana/kanji, voiced/semi-voiced, whitespace
- `fct_sales` – store **tax-exclusive** and **tax code**; derive tax-inclusive via view
- **RLS/Column Mask** – row-level by department/prefecture; mask phone/email; audit columns
- **Monitoring & Runbook** – data quality tests, canary queries, rerun/compensation steps

## DoD by module

### 1) `dim_calendar`
- `SOURCES.md` lists ≥2 **official** links with dates & update cadence.
- Definitions for **holiday/振替/国民の休日** documented.
- **連休 rule** (weekly grain) documented.
- Seed/reference CSV reproducible.

### 2) `dim_tax_rate (SCD2)`
- Columns: `tax_code`, `rate`, `valid_from`, `valid_to`, `is_current`.
- **Tax-change timeline** + **reduced-rate scope** have ≥2 official sources in `SOURCES.md`.
- **Boundary tests** provided (switch day, cross-month/year).

### 3) `dim_region (JIS)`
- Official JIS code source + **update frequency** in `SOURCES.md`.
- Clear mapping rules for `pref_code` / `city_code` with store key.

### 4) `dim_product (JAN)`
- **JAN checksum** documented from GS1; include failing cases (wrong length, leading zeros, non-digits).
- External master **hook** documented (even if not implemented).

### 5) `dim_customer (名寄せ)`
- Normalization steps documented: full/half width, Kana/kanji, voiced/semi-voiced, whitespace/symbols.
- **≥10 edge-case tests** (long vowel mark, Katakana variants, internal spaces, email case, etc.).

### 6) `fct_sales`
- Persist **pre-tax amount** and **tax code**; **view** returns tax-inclusive using SCD2 rate by date.
- Keys to `dim_*` documented (store, region, customer, product, date).

### 7) RLS / Column Mask
- **Row-Level** demo for department/prefecture (at least one implemented end-to-end).
- **Column Mask** for phone/email; include **audit** fields (by/at).

### 8) Monitoring & Runbook
- **DQ matrix**: PK uniqueness, FK relationships, SCD2 boundaries, tax interval coverage, 名寄せ/JAN cases.
- **Canary queries** list complete; **rerun/compensation** steps documented.

## Placeholders
- Diagrams to `/docs` (ERD, flow, RLS view).
- Link `SOURCES.md` once Step 4/8 are done.
