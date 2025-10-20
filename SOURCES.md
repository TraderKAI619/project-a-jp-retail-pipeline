# SOURCES – Official Data References

## Primary Datasets

| Dataset  | File name            | Source (org/page)                                                                                                                                   | Retrieved at (JST)   | File size | SHA256 |
|----------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|-----------|--------|
| holidays | syukujitsu-2.csv    | 内閣府: [国民の祝日について](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)                                 | 2025-10-13 11:00 JST | 20K | 1abbdac0fd72f7b754220e42844e9db7f5272cbae77919c559d85a8457d65cbb |
| jis      | 000925835.xlsx       | 総務省: [全国地方公共団体コード](https://www.soumu.go.jp/denshijiti/code.html)                                                | 2025-10-13 11:05 JST | 104K | cb0f09f52cd29dd48ae1a2d75c7e1c2639e5920444ead22c89f4a9532ae922d0 |
| tax      | tax_rate_history.csv | 財務省: [消費税の概要](https://www.mof.go.jp/tax_policy/summary/consumption/consumption_tax/index.html) | 2025-10-13 11:35 JST | 609 Bytes | a4fdcedf920ee2aa61e66c4417a9c7e53fdf427d35cc9a06d7bd80d07c2a4164 |

> **Note:** Full checksums & sizes live in `reports/raw_sha256.txt` / `reports/raw_sizes.txt`.  
> Use the commands below to (re)generate and verify.

---

## Verification & Reproducibility

**Evidence files** (generated locally, not in version control)

> 💡 **Note:** These files are `.gitignore`d and generated locally. Run the commands below to create them.
- [`reports/raw_sha256.txt`](./reports/raw_sha256.txt) – Complete SHA256 checksums  
- [`reports/raw_sizes.txt`](./reports/raw_sizes.txt) – File sizes

**Generate / refresh evidence**
```bash
# Create / refresh full checksums & sizes
find data/raw_official -type f \( -name "*.csv" -o -name "*.xlsx" \) -print0 \
  | xargs -0 sha256sum | sort > reports/raw_sha256.txt

find data/raw_official -type f \( -name "*.csv" -o -name "*.xlsx" \) -exec ls -lh {} \; \
  | awk '{print $9"\t"$5}' | sort > reports/raw_sizes.txt

## Verify integrity
sha256sum -c reports/raw_sha256.txt
# Expected:
# data/raw_official/holidays/syukuijitsu-2.csv: OK
# data/raw_official/jis/000925835.xlsx: OK
# data/raw_official/tax/tax_rate_history.csv: OK

Data Provenance
Holidays (National Holidays)

Authority: 内閣府 (Cabinet Office) / 公式ページ: 国民の祝日について

Update cadence: 年次＋告示時

Format: CSV（UTF-8）

JIS Codes (Administrative Divisions)

Authority: 総務省 / 規格: JIS X 0401/0402 / 公式ページ: 全国地方公共団体コード

Update cadence: 市区町村の統廃合等の告示時

Format: Excel（.xlsx）

Consumption Tax (Rates & History)

Authority: 財務省 / 公式ページ: 消費税の概要

Update cadence: 法改正時

Format: CSV（告示に基づく整理）

Future Expansion

 GS1 / JAN codes（GS1 Japan / Global）— 検証ルール・チェックサム

 統計境界ポリゴン（e-Stat）— 県・市区町村ポリゴン / 年次

 為替レート（日本銀行）— 国際比較用 / 日次（必要時）

Update Strategy

Quarterly: JIS 更新有無・翌年祝日・税制改正の監視

Annual: 最新データ再取得 → SHA256 再生成 → ドキュメント更新 → バリデーション実行

License & Usage

政府オープンデータの利用規約（各サイト）に準拠。教育・ポートフォリオ用途を想定。

商用利用時は各公式サイトの最新ライセンスを確認。

引用時は出典（内閣府・総務省・財務省）、取得日時、変更点を明記。

Last updated: 2025-10-20 JST

補齊 holidays / jis 的大小與 **完整 SHA256** 時，可用這一段快速取值（貼回主表）：
```bash
for f in syukuijitsu-2.csv 000925835.xlsx; do
  size=$(grep -F "$f" reports/raw_sizes.txt | awk -F'\t' '{print $2}')
  sha=$(grep -F "$f" reports/raw_sha256.txt | awk '{print $1}')
  printf "%-18s  size=%-8s  sha256=%s\n" "$f" "$size" "$sha"
done
