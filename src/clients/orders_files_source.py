import csv
from pathlib import Path

from src.errors import ConfigError


def read_csv_file(path: Path) -> list[dict]:
    with open(path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def read_all_csv(raw_dir: Path, pattern: str) -> list[dict]:
    if not raw_dir.exists():
        raise ConfigError(f"Directory {raw_dir} does not exist")
    matching_files = raw_dir.glob(pattern)
    sorted_files = sorted(matching_files)

    all_rows = []
    for file in sorted_files:
        all_rows.extend(read_csv_file(file))
    return all_rows


