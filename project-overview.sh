#!/bin/bash
echo "=== PROJECT STRUCTURE ==="
tree -L 3 -I '.venv|__pycache__|.git|node_modules'

echo -e "\n=== KEY FILES ==="
ls -la | grep -E '\.(yml|yaml|json|txt|md)$|Makefile'

echo -e "\n=== PYTHON SCRIPTS ==="
find . -name "*.py" -not -path "./.venv/*" | head -20

echo -e "\n=== DEPENDENCIES ==="
cat requirements.txt

echo -e "\n=== RECENT COMMITS ==="
git log --oneline -5

echo -e "\n=== GIT STATUS ==="
git status -s
