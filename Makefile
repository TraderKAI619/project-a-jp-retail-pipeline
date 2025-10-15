.PHONY: silver validate gold validate_gold all everything
silver:
	python scripts/to_silver.py
validate:
	python scripts/validate_silver.py
gold:
	python scripts/to_gold.py
validate_gold:
	python scripts/validate_gold.py
all: silver validate
everything: silver validate gold validate_gold
