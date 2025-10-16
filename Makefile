PYTHON ?= python

.PHONY: silver validate gold validate_gold all everything ci clean

silver:
	$(PYTHON) scripts/to_silver.py

validate:
	$(PYTHON) scripts/validate_silver.py

gold:
	$(PYTHON) scripts/to_gold.py

validate_gold:
	$(PYTHON) scripts/validate_gold.py

all: silver validate
everything: silver validate gold validate_gold
ci: everything

clean:
	rm -rf data/silver data/gold
