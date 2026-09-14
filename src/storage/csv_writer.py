import csv
from pathlib import Path

def write_rows(rows: list[dict], path: Path) -> int:
    if not rows:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(path, 'w', newline='',encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
