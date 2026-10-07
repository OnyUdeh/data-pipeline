import os
from pathlib import Path

from dotenv import load_dotenv

from tfl_api import fetch_all_statuses

PROJECT_DIR = Path(__file__).parent
MODES = ["tube", "dlr", "overground", "elizabeth-line"]


def main() -> None:
    load_dotenv(PROJECT_DIR / ".env")
    app_key = os.getenv("TFL_APP_KEY") or None

    records = fetch_all_statuses(MODES, app_key)
    for record in records:
        print(f"{record['mode']:<15} {record['line_name']:<22} {record['status']}")

    problems = [r for r in records if r["status"] != "Good Service"]
    print(f"\n{len(records)} lines checked, {len(problems)} with problems")


if __name__ == "__main__":
    main()