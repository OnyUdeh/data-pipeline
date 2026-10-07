"""Functions for fetching line status data from the TfL Unified API."""

import time
from datetime import datetime, timezone

import requests

BASE_URL = "https://api.tfl.gov.uk"


def fetch_line_statuses(mode: str, app_key: str | None = None) -> list[dict]:
    """Fetch the current status of every line for one mode, such as 'tube'."""
    url = f"{BASE_URL}/Line/Mode/{mode}/Status"
    params = {"app_key": app_key} if app_key else {}
    response = requests.get(url, params=params, timeout=10)
    return response.json()

def parse_line(line: dict, fetched_at: str) -> dict:
    """Keep only the fields we need from one raw line record."""
    status = line["lineStatuses"][0]
    return {
        "line_id": line["id"],
        "line_name": line["name"],
        "mode": line["modeName"],
        "status": status["statusSeverityDescription"],
        "reason": status.get("reason"),
        "fetched_at": fetched_at,
    }

def fetch_all_statuses(modes: list[str], app_key: str | None = None) -> list[dict]:
    """Fetch and clean line statuses for several modes."""
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = []
    for mode in modes:
        lines = fetch_line_statuses(mode, app_key)
        records.extend(parse_line(line, fetched_at) for line in lines)
        time.sleep(1)
    return records