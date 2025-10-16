.PHONY: intermediate silver validate gold validate_gold all everything

intermediate:
	python scripts/build_intermediate.py

silver: intermediate
	python scripts/to_silver.py

validate:
	python scripts/validate_silver.py

gold: silver validate
	python scripts/to_gold.py

validate_gold:
	python scripts/validate_gold.py

all: silver validate
everything: intermediate silver validate gold validate_gold
