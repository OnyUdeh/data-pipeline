import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from file_utils import write_csv, write_json
from tfl_api import fetch_all_raw, parse_all

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"
DATASET = "tfl_line_status"
MODES = ["tube", "dlr", "overground", "elizabeth-line"]

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Send log messages to the terminal and to pipeline.log."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(PROJECT_DIR / "pipeline.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def build_paths(run_time: datetime) -> tuple[Path, Path]:
    """Return the raw and clean file paths for this run."""
    day = run_time.strftime("%Y-%m-%d")
    stamp = run_time.strftime("%Y-%m-%dT%H%M%SZ")
    raw_path = OUTPUT_DIR / "raw" / DATASET / f"date={day}" / f"line_status_{stamp}.json"
    clean_path = OUTPUT_DIR / "clean" / DATASET / f"date={day}" / f"line_status_{stamp}.csv"
    return raw_path, clean_path


def main() -> None:
    setup_logging()
    load_dotenv(PROJECT_DIR / ".env")
    app_key = os.getenv("TFL_APP_KEY") or None

    run_time = datetime.now(timezone.utc)
    fetched_at = run_time.isoformat(timespec="seconds")
    raw_path, clean_path = build_paths(run_time)
    logger.info("Starting run at %s", fetched_at)

    raw = fetch_all_raw(MODES, app_key)
    if not raw:
        logger.error("No data fetched, so nothing was saved")
        raise SystemExit(1)

    write_json({"fetched_at": fetched_at, "data": raw}, raw_path)
    logger.info("Saved raw data to %s", raw_path.relative_to(PROJECT_DIR))

    records = parse_all(raw, fetched_at)
    write_csv(records, clean_path)
    logger.info("Saved %d clean records to %s", len(records), clean_path.relative_to(PROJECT_DIR))


if __name__ == "__main__":
    main()