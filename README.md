# Project A — Japan Retail Data Pipeline (MVP)
[![CI](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English** | [**日本語**](README_ja.md)

A production-ready batch ETL pipeline for Japanese retail analytics using the Medallion architecture.
Integrates official government data (holidays, consumption tax history, JIS region codes) with synthetic sales for KPI demos.

Perfect for portfolios, learning DE patterns, or as a template for JP-specific analytics. 

## ⚡ 3-Minute Quick Start (Total ~3 min)

### Outputs (after build)
- `data/silver/{holidays,jis,tax}/...`
- `data/gold/dims/{dim_date,dim_geo,dim_product}.csv`
- `data/gold/facts/{fact_calendar,fact_sales}.csv`
