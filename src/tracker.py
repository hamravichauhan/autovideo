"""Persistent Tracker for ExtrovertNerd Automation Series.

Manages sequential progression for the Top 100 Website Architecture series,
ensuring content is dispatched strictly day-by-day (e.g. Day 11, Day 12, Day 13...)
without duplicates or skipped days.
"""

from __future__ import annotations

import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict

from src.config import config

logger = logging.getLogger("tracker")

TRACKER_FILE = config.content_dir / "tracker.json"


def _load_tracker() -> Dict[str, Any]:
    """Loads tracker data from JSON file."""
    if TRACKER_FILE.exists():
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Could not read tracker file: %s. Using default.", e)
    return {"current_top100_rank": 0, "dispatched_ranks": []}


def _save_tracker(data: Dict[str, Any]) -> None:
    """Saves tracker data to JSON file."""
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_current_top100_rank() -> int:
    """Returns the most recently dispatched rank (1-100)."""
    data = _load_tracker()
    return int(data.get("current_top100_rank", 0))


def set_current_top100_rank(rank: int) -> None:
    """Sets the most recently dispatched rank."""
    data = _load_tracker()
    data["current_top100_rank"] = rank
    data["updated_at"] = datetime.datetime.now().isoformat()
    dispatched = data.setdefault("dispatched_ranks", [])
    if rank not in dispatched:
        dispatched.append(rank)
    _save_tracker(data)
    logger.info("Updated Top 100 tracker: rank #%d", rank)


def get_next_top100_rank(advance: bool = False) -> int:
    """Computes the next rank to be dispatched (1-100).

    If advance=True, updates the tracker immediately.
    """
    cur = get_current_top100_rank()
    next_rank = 1 if cur >= 100 or cur < 1 else cur + 1
    if advance:
        set_current_top100_rank(next_rank)
    return next_rank
