# Technical Decisions (ADR-lite)

## 1) DuckDB over Spark
**Decision:** Use DuckDB for local analytics.
**Reasoning:** Demo scale (<100K rows), zero infra, fast startup, easy CI.
**Trade-off:** Not ideal for >1M rows unpartitioned.
**Path:** Later migrate compute to Glue/Athena if scale grows.

## 2) Star Schema over Flat Tables
**Decision:** Dimensional model (dims + facts) in gold.
**Reasoning:** Query performance, conformed dimensions, BI-friendly.
**Trade-off:** ETL complexity vs. denormalized simplicity.

## 3) CSV Artifacts over Parquet (for portfolio)
**Decision:** Keep CSV for gold/report artifacts.
**Reasoning:** Human-readable, GitHub previewable, easy diff.
**Trade-off:** Larger size, slower I/O; production → Parquet + partitioning.

## 4) Python + JSON Schema first; dbt later
**Decision:** Start with Python validators + JSON schemas.
**Reasoning:** Fast MVP iteration, language-agnostic validation, simple CI.
**Next:** Add dbt-duckdb tests for declarative checks.

## 5) Natural Key for Idempotency
**Decision:** Use `[order_date, geo_id, product_id]` as composite NK.
**Reasoning:** Business-meaningful, simplifies upsert logic.
**Trade-off:** Larger composite index vs. surrogate key.
