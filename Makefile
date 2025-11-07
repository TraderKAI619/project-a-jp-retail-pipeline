.PHONY: venv install analysis dashboard dashboard-bg hello-bg stop kill port logs ps everything

PORT ?= 8501
PIDFILE = .streamlit.pid
LOGFILE = .streamlit.log

ifdef CI
PY=python
PIP=pip
VENV_ACT=
else
PY=.venv/bin/python
PIP=.venv/bin/pip
VENV_ACT=. .venv/bin/activate
endif

venv:
	python3 -m venv .venv

install:
ifdef CI
	$(PIP) install -U pip && $(PIP) install -r requirements.txt
else
	$(VENV_ACT) && $(PIP) install -U pip && $(PIP) install -r requirements.txt
endif

analysis:
ifdef CI
	$(PY) scripts/run_gw_sql.py
else
	$(VENV_ACT) && $(PY) scripts/run_gw_sql.py
endif

dashboard:
	$(VENV_ACT) && streamlit run analytics/dashboards/app.py \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true --server.enableCORS false --server.enableXsrfProtection false

dashboard-bg:
	$(VENV_ACT) && nohup streamlit run analytics/dashboards/app.py \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true --server.enableCORS false --server.enableXsrfProtection false \
	  > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

hello-bg:
	$(VENV_ACT) && nohup streamlit hello \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

stop:
	-@[ -f $(PIDFILE) ] && kill -TERM $$(cat $(PIDFILE)) 2>/dev/null || true
	-@rm -f $(PIDFILE)
	-@pkill -f "streamlit .*analytics/dashboards/app.py" 2>/dev/null || true

kill: stop

port:
	ss -lptn 'sport = :$(PORT)' || true

logs:
	@echo "=== $(LOGFILE) (last 120 lines) ==="
	@[ -f $(LOGFILE) ] && tail -n 120 $(LOGFILE) || echo "No log yet"

ps:
	ps aux | grep -i "[s]treamlit"

everything: install analysis
