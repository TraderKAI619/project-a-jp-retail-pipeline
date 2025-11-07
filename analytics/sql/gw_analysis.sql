-- OUTPUT: top_prefecture_uplift (pref_code, pref_name_ja, uplift_rate)
-- デモ用のプレースホルダー（実データ接続前）
SELECT * FROM (VALUES
  (13, '東京都',   0.587),
  (14, '神奈川県', 0.523),
  (27, '大阪府',   0.489),
  (11, '埼玉県',   0.471),
  (12, '千葉県',   0.462)
) AS t(pref_code, pref_name_ja, uplift_rate);
