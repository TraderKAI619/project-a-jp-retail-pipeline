# project-a-jp-retail-pipeline

[![CI](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/ci.yml)
[![Nightly ETL](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/schedule.yml/badge.svg)](https://github.com/TraderKAI619/project-a-jp-retail-pipeline/actions/workflows/schedule.yml)

日本零售批次管線：官方來源清洗 **Bronze → Silver**，匯入 **星型模型 Gold（dim_date、dim_geo、fact_calendar）**。  
內建驗證與 Makefile，一鍵完成建置與驗證；提供 DuckDB 範例查詢可直接跑在 CSV 上。

---
