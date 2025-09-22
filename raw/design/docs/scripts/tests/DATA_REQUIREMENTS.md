# DATA_REQUIREMENTS – Project A (JP Retail/EC)

## 1) Scope & Principles
- Use **official JP reference tables** where applicable; all **business data is synthetic**.
- Clearly declare **grain**, **required fields**, **freshness**, **source type (official/synthetic)**, and **privacy**.

---

## 2) Datasets Summary

| Dataset | Grain | Purpose | Source Type | Freshness |
|---|---|---|---|---|
| `dim_calendar` | day | holidays & **long‐holiday (連休) rule** | **Official** (JP govt) | annual + ad-hoc updates |
| `dim_tax_rate` (SCD2) | interval (`valid_from`→`valid_to`) | consumption tax rates incl. 8% reduced | **Official** (国税庁/e-Gov) | event-driven (law changes) |
| `dim_region` (JIS) | prefecture / city | region keys for slicing | **Official** (JIS X0401/0402) | per release |
| `dim_product` | product id | holds **JAN** & attributes (minimal) | **Synthetic** (+ GS1 rules) | static for demo |
| `dim_customer` | customer id | **name normalization (名寄せ)** fields | **Synthetic** | static + cases |
| `fct_sales` | transaction line | joins all dims; pre-tax amount & tax code | **Synthetic** | daily incremental |

---

## 3) Detailed Requirements

### 3.1 `dim_calendar` (Official)
- **Fields**: `date`, `is_holiday`, `holiday_name`, `is_substitute`(振替), `is_citizen_holiday`(国民の休日), `week_number`, `dow`, `is_long_holiday_week` (derived rule at weekly grain).
- **Rules**: document how **連休** is determined (≥3 days within Mon–Sun incl. weekend+holidays).
- **Quality**: dates unique; coverage for the demo year(s).

### 3.2 `dim_tax_rate` (Official, SCD2)
- **Fields**: `tax_code`, `rate`, `reduced_flag`, `valid_from`, `valid_to`, `is_current`.
- **Notes**: include historical changes; list **sources** later in `SOURCES.md`.
- **Quality**: non-overlapping intervals per `tax_code`; boundary day tests.

### 3.3 `dim_region` (Official JIS)
- **Fields**: `pref_code`, `pref_name_ja`, `city_code` (optional for demo), `city_name_ja`.
- **Join**: store key will reference `pref_code` (city optional).
- **Quality**: codes match JIS; names in JP.

### 3.4 `dim_product` (Synthetic, GS1 rules)
- **Fields**: `product_id`, `jan_code` (13-digit), `category`, `brand`, `unit_price_pre_tax`.
- **Rules**: **JAN checksum** must pass (GS1); include some failing test cases in `/tests`.
- **Privacy**: no real brand dependencies required.

### 3.5 `dim_customer` (Synthetic)
- **Fields**: `customer_id`, `name_raw`, `name_norm` (full/half width, Kana/kanji normalized), `kana_raw`, `kana_norm`, `phone_masked`, `email_masked`, `pref_code`.
- **Normalization**: full↔half width, voiced/semi-voiced, whitespace, long vowel mark; keep a **test list ≥10 edge cases**.
- **Privacy**: only masked examples; no real PII.

### 3.6 `fct_sales` (Synthetic)
- **Grain**: 1 row per **transaction line**.
- **Fields**: `txn_id`, `txn_ts`, `store_id`, `pref_code`, `customer_id`, `product_id`, `qty`, `price_pre_tax`, `tax_code`.
- **Derived (view)**: `price_incl_tax` via `dim_tax_rate` SCD2 on `txn_ts`.
- **Quality**: FK coverage to all dims; amounts ≥0; timestamps within demo period.

---

## 4) Volumes (for demo)
- `dim_*`: 100–5,000 rows each; `fct_sales`: ~10–50k rows for one demo year.
- Keep small enough for CI yet large enough to show partitions/filters.

---

## 5) Freshness & Updates
- Official tables (`calendar`, `tax_rate`, `region`) checked **at Step 4/8** and referenced in `SOURCES.md`.
- Synthetic data: fixed snapshot for reproducibility.

---

## 6) Acceptance (Step-3 DoD)
- Each dataset above has **grain, fields, quality rules** described here.
- `SOURCES.md` placeholder created (to be filled at Step 4/8).
- Folder `raw/` exists for official CSV; `tests/` has a **case list placeholder**.
