-- OUTPUT: top_prefecture_uplift (pref_code, pref_name_ja, uplift_rate)
-- デモ用のプレースホルダー（実データ接続前）
SELECT * FROM (VALUES
  (13, '東京都',   0.587),
  (14, '神奈川県', 0.523),
  (27, '大阪府',   0.489),
  (11, '埼玉県',   0.471),
  (12, '千葉県',   0.462)
) AS t(pref_code, pref_name_ja, uplift_rate);
-- 追加：category_contrib (category_name, uplift_contrib)
-- デモ用
SELECT * FROM (VALUES
  ('旅行用品', 0.32),
  ('日用品ミニ', 0.18),
  ('食品', -0.05)
) AS c(category_name, uplift_contrib);
