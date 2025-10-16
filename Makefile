PYTHON ?= python

	.PHONY: silver validate gold validate_gold all everything ci clean demo

	silver:
	$(PYTHON) scripts/to_silver.py

	validate:
	$(PYTHON) scripts/validate_silver.py

	gold:
	$(PYTHON) scripts/to_gold.py

	validate_gold:
	$(PYTHON) scripts/validate_gold.py

# 一鍵跑完全流程（本地／CI 都用這個）
	everything: silver validate gold validate_gold

# 舊習慣別名
	all: silver validate

# CI 入口（等同 everything）
	ci: everything

# Demo（可選）：輸出三個 KPI 範例
	demo:
	$(PYTHON) scripts/run_demo.py

	clean:
	rm -rf data/silver data/gold
