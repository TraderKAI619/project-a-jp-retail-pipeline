# tax（消費税率）

必備欄位：
- start_date
- end_date
- tax_rate
- reduced_tax_rate
- source
- source_version

主鍵：
- start_date + tax_rate

備註：
- 來源：国税庁「消費税率等の改正について」
- 含軽減税率（8%）與標準税率（10%）
- 税率適用期間以施行日ベース記錄
- 原始資料：tax_rate_history.csv
- 更新頻率：税制改正時（不定期）
