#!/usr/bin/env bash
set -euo pipefail

SOURCES_FILE="SOURCES.md"

echo "🔄 Updating SOURCES.md with file sizes and SHA256..."

# 首先，顯示所有找到的文件
echo ""
echo "📂 Files found:"
cat reports/raw_sizes.txt

echo ""
echo "🔍 Processing files..."

# 處理每個文件
while IFS=$'\t' read -r filepath size; do
    # 提取文件名
    filename=$(basename "$filepath")
    
    # 獲取 SHA256
    sha=$(grep -F "$filepath" reports/raw_sha256.txt | awk '{print $1}' || echo "")
    
    if [[ -z "$sha" ]] || [[ -z "$size" ]]; then
        echo "  ⚠️  Skipping $filename (missing data)"
        continue
    fi
    
    # 根據文件名更新對應行
    case "$filename" in
        *syuku*.csv|*holiday*.csv)
            echo "  📅 Updating holidays: $filename ($size)"
            # 使用 sed 更新（更簡單可靠）
            sed -i "s|\(holidays.*\)|(to fill)\*\s*|\s*\*(to fill)\*|\1$size | $sha|" "$SOURCES_FILE" || true
            ;;
        *.xlsx)
            echo "  🗺️  Updating JIS: $filename ($size)"
            sed -i "s|\(jis.*000925835.xlsx.*\)|(to fill)\*\s*|\s*\*(to fill)\*|\1$size | $sha|" "$SOURCES_FILE" || true
            ;;
        *tax*.csv)
            echo "  💴 Tax file already filled: $filename"
            ;;
        *)
            echo "  ℹ️  Unknown file type: $filename"
            ;;
    esac
    
done < reports/raw_sizes.txt

echo ""
echo "✅ Update complete!"
echo ""
echo "📝 Please verify SOURCES.md manually"

