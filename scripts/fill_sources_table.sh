#!/usr/bin/env bash
set -euo pipefail

SOURCES_FILE="SOURCES.md"

echo "🔄 Updating SOURCES.md with file sizes and SHA256..."

# 提取數據
for file in syukuijitsu-2.csv 000925835.xlsx; do
  size=$(grep -F "$file" reports/raw_sizes.txt | awk -F'\t' '{print $2}' || echo "N/A")
  sha=$(grep -F "$file" reports/raw_sha256.txt | awk '{print $1}' || echo "N/A")
  
  # 替換對應行
  if [[ "$file" == "syukuijitsu-2.csv" ]]; then
    # 替換 holidays 行
    perl -i -pe "s|(holidays\s*\|\s*syukuijitsu-2.csv\s*\|.*?\|\s*2025-10-13 11:00 JST\s*\|)\s*\*\(to fill\)\*\s*\|\s*\*\(to fill\)\*|\1 $size | $sha|" "$SOURCES_FILE"
  elif [[ "$file" == "000925835.xlsx" ]]; then
    # 替換 jis 行
    perl -i -pe "s|(jis\s*\|\s*000925835.xlsx\s*\|.*?\|\s*2025-10-13 11:05 JST\s*\|)\s*\*\(to fill\)\*\s*\|\s*\*\(to fill\)\*|\1 $size | $sha|" "$SOURCES_FILE"
  fi
  
  echo "  ✓ Updated $file: $size, SHA256: ${sha:0:16}...${sha: -16}"
done

echo "✅ SOURCES.md updated!"
