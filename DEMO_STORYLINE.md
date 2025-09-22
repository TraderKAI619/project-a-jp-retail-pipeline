# DEMO_STORYLINE – 3–5 min

## Business Question
How much uplift do **long-holiday weeks** deliver vs normal weeks by prefecture/department?  
Do **tax-rate changes** (incl. 8% reduced rate) affect average basket size?

## Data Journey
- **Historic**: one-off full load → Bronze/Silver/Gold.
- **Daily**: incremental loads every day; **on the 15th/28th** sync selected dims (`dim_calendar`, `dim_tax_rate`, etc.).

## Highlights to show
- **Tax SCD2**: keep both tax-exclusive & tax-inclusive; query-time derives correct rate by date.
- **JIS region keys + store key**: enables cuts by prefecture/department.
- **Name normalization (名寄せ)**: full/half width, Kana/kanji, voiced/semi-voiced, whitespace; tested with tough cases.
- **RLS/Masking**: row-level by prefecture/department; column masking for phone/email with audit fields.

## Validation
- **Canary queries**:
  - Crossing a **tax boundary day** returns correct inclusive amount.
  - **連休 week** detection at weekly grain works for GW/Obon/New Year.
  - **JAN checksum** rejects malformed IDs (length, leading zeros, non-digits).
  - **Name normalization** passes ≥10 edge cases.

## What the interviewer sees
- Clear folder layout, diagrams, and **how to reproduce**.
- Sources linked to **official JP standards** (e-Gov/国税庁/J-LIS/GS1).
- Tests and a short **Runbook** for reruns/compensation.
