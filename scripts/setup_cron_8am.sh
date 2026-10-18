#!/usr/bin/env bash
# ==============================================================================
# Installs a daily 8:00 AM Cron Job on macOS / Linux for ExtrovertNerd Automation
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_SCRIPT="${PROJECT_ROOT}/scripts/daily_automation_8am.sh"

chmod +x "${TARGET_SCRIPT}"

# Cron expression for 8:00 AM daily
CRON_JOB="0 8 * * * ${TARGET_SCRIPT} >/dev/null 2>&1"

echo "Checking existing crontab..."
CURRENT_CRON="$(crontab -l 2>/dev/null || true)"

if echo "${CURRENT_CRON}" | grep -Fq "${TARGET_SCRIPT}"; then
    echo "✅ ExtrovertNerd 8:00 AM cron job is already installed:"
    echo "${CURRENT_CRON}" | grep -F "${TARGET_SCRIPT}"
else
    (echo "${CURRENT_CRON}"; echo "# ExtrovertNerd 8:00 AM Daily Acquisition Funnel"; echo "${CRON_JOB}") | crontab -
    echo "🎉 Successfully installed ExtrovertNerd 8:00 AM daily cron job!"
    echo "Schedule: Every day at 08:00 AM local time"
    echo "Command:  ${TARGET_SCRIPT}"
fi

echo ""
echo "Current crontab entries:"
crontab -l
