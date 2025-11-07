.RECIPEPREFIX := >
.PHONY: venv install silver gold validate analytics report dashboard dashboard-bg hello-bg stop kill port logs ps everything test

PORT ?= 8501
PIDFILE := .streamlit.pid
LOGFILE := .streamlit.log

# CI 環境不啟動 venv；本機啟動 .venv
ifdef CI
PY := python
PIP := pip
ACT :=
else
PY := .venv/bin/python
PIP := .venv/bin/pip
ACT := . .venv/bin/activate &&
endif

venv:
> python3 -m venv .venv

install:
ifdef CI
> $(PIP) install -U pip && $(PIP) install -r requirements.txt
else
> $(ACT) $(PIP) install -U pip && $(PIP) install -r requirements.txt
endif

silver:
> $(ACT) $(PY) scripts/to_silver.py

gold:
> $(ACT) $(PY) scripts/to_gold.py

validate:
> $(ACT) $(PY) scripts/validate_gold.py

analytics:
> $(ACT) $(PY) scripts/run_gw_sql.py

report:
> $(ACT) $(PY) scripts/generate_report.py

test:
> pytest -v --cov=scripts --cov-report=term-missing

dashboard:
> $(ACT) streamlit run analytics/dashboards/app.py \
>   --server.address 0.0.0.0 --server.port $(PORT) \
>   --server.headless true --server.enableCORS false --server.enableXsrfProtection false

dashboard-bg:
> $(ACT) nohup streamlit run analytics/dashboards/app.py \
>   --server.address 0.0.0.0 --server.port $(PORT) \
>   --server.headless true --server.enableCORS false --server.enableXsrfProtection false \
>   > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

hello-bg:
> $(ACT) nohup streamlit hello \
>   --server.address 0.0.0.0 --server.port $(PORT) \
>   --server.headless true > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

stop:
> -@[ -f $(PIDFILE) ] && kill -TERM $$(cat $(PIDFILE)) 2>/dev/null || true
> -@rm -f $(PIDFILE)
> -@pkill -f "streamlit .*analytics/dashboards/app.py" 2>/dev/null || true

kill: stop

port:
> ss -lptn 'sport = :$(PORT)' || true

logs:
> @echo "=== $(LOGFILE) (last 120 lines) ==="
> @[ -f $(LOGFILE) ] && tail -n 120 $(LOGFILE) || echo "No log yet"

ps:
> ps aux | grep -i "[s]treamlit"

everything: install silver gold validate analytics report
