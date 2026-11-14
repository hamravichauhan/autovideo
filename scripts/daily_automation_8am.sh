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

# Execute isolated multi-track daily acquisition pipeline:
# Track 1: Dev Content (Top 100 System Architecture + Performance Blueprints + 60s Reel) -> LinkedIn & Instagram
# Track 2: Breaking Tech News (Architecture Radar Poster + X/Twitter breaking news post) -> X (Twitter)
# Track 3: Local B2B Funnel (pSEO Blog + 4-slide Local Carousel + 30s Reel + Prospecting) -> Website Blog & Local IG/FB
"${PYTHON_BIN}" -m src.main --mode daily --platform all 2>&1 | tee -a output/logs/daily_8am.log

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] Daily 8:00 AM Run Finished!"
