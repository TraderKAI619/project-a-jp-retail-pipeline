.PHONY: venv install analysis dashboard kill

PY=python
PORT?=8501

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

analysis:
	. .venv/bin/activate && $(PY) scripts/run_gw_sql.py

dashboard:
	. .venv/bin/activate && streamlit run analytics/dashboards/app.py \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true --server.enableCORS false --server.enableXsrfProtection false

kill:
	pkill -f "streamlit" || true
