PYTHON ?= python
# 讓配方行用 '>' 當前綴，不再依賴 Tab
.RECIPEPREFIX := >

.PHONY: intermediate silver validate gold validate_gold report all everything ci clean demo

# 先把 raw_official/*/_staging → data/intermediate/*
intermediate:
> $(PYTHON) scripts/build_intermediate.py

silver:
> $(PYTHON) scripts/to_silver.py

validate:
> $(PYTHON) scripts/validate_silver.py

gold:
> $(PYTHON) scripts/to_gold.py

validate_gold:
> $(PYTHON) scripts/validate_gold.py

# 報表輸出（Markdown + CSV）  
report:
> $(PYTHON) scripts/generate_report.py

# 一鍵跑完全流程 
everything: intermediate silver validate gold validate_gold report

# 習慣別名
all: silver validate

# CI 入口
ci: everything

# Demo（可選）
demo:
> $(PYTHON) scripts/run_demo.py

clean:
> rm -rf data/silver data/gold data/intermediate   
