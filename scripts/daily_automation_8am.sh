#!/usr/bin/env bash
# ==============================================================================
# ExtrovertNerd 8:00 AM Daily Automated Acquisition & Multi-Platform Dispatch
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================================="
echo "⚡ [${TIMESTAMP}] Running ExtrovertNerd 8:00 AM Daily Funnel Automation"
echo "=================================================================="

# Detect Python in virtualenv or system
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
else
    echo "❌ Error: Python not found!"
    exit 1
fi

mkdir -p output/logs

# Execute full daily acquisition pipeline:
# 1. Generates daily pSEO blog article for local city/niche
# 2. Renders 4-slide local case study carousel
# 3. Renders 2-slide Top 100 Website Teardowns (Instagram, LinkedIn, X)
# 4. Assembles ready-to-post captions and X Twitter thread
# 5. Automatically dispatches labeled posters + platform captions + live blog link to Telegram
"${PYTHON_BIN}" -m src.main --mode daily --platform all 2>&1 | tee -a output/logs/daily_8am.log

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] Daily 8:00 AM Run Finished!"
