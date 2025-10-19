# Postmortem: fact_sales Rowcount Mismatch

**Date:** 2025-10-18  
**Impact:** CI test failed in `test_gold_basic.py`; artifacts skipped.  
**Root cause:** Demo sales date range changed; test expectation not updated.  
**Detection:** Pytest red in Actions; reproduced locally.  
**Fix:** Updated expectation and added source comment; switched to query-based rowcount.  
**Prevention:** README note that demo data varies; tests explain expectation sources.  
**Refs:** Commit `f464e6b` (adjust test expectation).
