"""Functions for fetching line status data from the TfL Unified API."""

import time
from datetime import datetime, timezone

import requests

BASE_URL = "https://api.tfl.gov.uk"


"""Functions for fetching line status data from the TfL Unified API."""

import logging
import time
from datetime import datetime, timezone

import requests

BASE_URL = "https://api.tfl.gov.uk"

logger = logging.getLogger(__name__)


class TflApiError(Exception):
    """Raised when the TfL API can't be reached or returns an error."""


def fetch_line_statuses(mode: str, app_key: str | None = None, retries: int = 3) -> list[dict]:
    """Fetch the current status of every line for one mode, retrying temporary failures."""
    url = f"{BASE_URL}/Line/Mode/{mode}/Status"
    params = {"app_key": app_key} if app_key else {}

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            status = error.response.status_code
            if status < 500 and status != 429:
                raise TflApiError(f"TfL returned status {status} for {mode}") from error
            logger.warning("Attempt %d of %d for %s got status %d", attempt, retries, mode, status)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            logger.warning("Attempt %d of %d for %s failed: %s", attempt, retries, mode, type(error).__name__)

        if attempt < retries:
            time.sleep(2 ** attempt)

    raise TflApiError(f"Gave up on {mode} after {retries} attempts")

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
    """Fetch and clean line statuses for several modes, skipping any that fail."""
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = []
    for mode in modes:
        try:
            lines = fetch_line_statuses(mode, app_key)
        except TflApiError as error:
            logger.error("Skipping %s: %s", mode, error)
            continue
        records.extend(parse_line(line, fetched_at) for line in lines)
        logger.info("Fetched %d lines for %s", len(lines), mode)
        time.sleep(1)
    return records