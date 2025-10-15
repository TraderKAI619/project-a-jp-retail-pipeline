.PHONY: silver validate all
silver:
	python scripts/to_silver.py
validate:
	python scripts/validate_silver.py
all: silver validate
