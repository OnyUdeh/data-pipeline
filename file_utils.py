"""Functions for reading and writing data files."""

import csv
import json
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    """Read a CSV file and return its rows as a list of dictionaries."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(rows: list[dict], path: Path) -> None:
    """Write a list of dictionaries to a CSV file, creating folders if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def write_json(data, path: Path) -> None:
    """Write data to a JSON file with readable indentation, creating folders if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def read_json(path: Path):
    """Read a JSON file and return its contents."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)