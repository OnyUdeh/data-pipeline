import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from tfl_api import fetch_all_statuses

PROJECT_DIR = Path(__file__).parent
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


def main() -> None:
    setup_logging()
    load_dotenv(PROJECT_DIR / ".env")
    app_key = os.getenv("TFL_APP_KEY") or None

    logger.info("Starting run for modes: %s", ", ".join(MODES))
    records = fetch_all_statuses(MODES, app_key)
    for record in records:
        print(f"{record['mode']:<15} {record['line_name']:<22} {record['status']}")

    problems = [r for r in records if r["status"] != "Good Service"]
    logger.info("Finished: %d lines checked, %d with problems", len(records), len(problems))


if __name__ == "__main__":
    main()