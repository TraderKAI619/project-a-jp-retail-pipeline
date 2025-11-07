.PHONY: venv install analysis dashboard dashboard-bg hello-bg stop kill port logs ps

PY=python
PORT ?= 8501
VENV_ACT = . .venv/bin/activate
PIDFILE = .streamlit.pid
LOGFILE = .streamlit.log

venv:
	python3 -m venv .venv

install: venv
	$(VENV_ACT) && pip install -U pip && pip install -r requirements.txt

analysis:
	$(VENV_ACT) && $(PY) scripts/run_gw_sql.py

# 前景啟動（用於本機測試）
dashboard:
	$(VENV_ACT) && streamlit run analytics/dashboards/app.py \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true --server.enableCORS false --server.enableXsrfProtection false

# 背景啟動（寫 PID 與 LOG）
dashboard-bg:
	$(VENV_ACT) && nohup streamlit run analytics/dashboards/app.py \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true --server.enableCORS false --server.enableXsrfProtection false \
	  > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

# 健檢：用官方 hello 起在指定埠，排除 app 程式碼問題
hello-bg:
	$(VENV_ACT) && nohup streamlit hello \
	  --server.address 0.0.0.0 --server.port $(PORT) \
	  --server.headless true > $(LOGFILE) 2>&1 & echo $$! > $(PIDFILE); sleep 2

# 停止背景服務（先用 PID，再保險殺字串）
stop:
	-@[ -f $(PIDFILE) ] && kill -TERM $$(cat $(PIDFILE)) 2>/dev/null || true
	-@rm -f $(PIDFILE)
	-@pkill -f "streamlit .*analytics/dashboards/app.py" 2>/dev/null || true
kill: stop  # 兼容舊習慣

# 檢查埠口
port:
	ss -lptn 'sport = :$(PORT)' || true

# 看啟動日誌
logs:
	@echo "=== $(LOGFILE) (last 120 lines) ==="
	@[ -f $(LOGFILE) ] && tail -n 120 $(LOGFILE) || echo "No log yet"

# 看行程
ps:
	ps aux | grep -i "[s]treamlit"
.PHONY: everything
everything: install analysis
