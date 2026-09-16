import json
from pathlib import Path
from typing import Any

from src.config import UNKNOWN_CATEGORY, DEFAULT_ADDRESS
from src.errors import ConfigError


def read_customers(path: Path) -> dict[str, dict]:
    if not path.is_file():
        raise ConfigError(f"File {path} does not exist.")
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        lookup = {customer["id"]: customer for customer in data}
        return lookup

def flatten_customer(customer: dict[str, Any]) -> dict[str, str | None]:
    name = customer.get("name",UNKNOWN_CATEGORY)

    address = customer.get("address") or {}
    city = address.get("city",DEFAULT_ADDRESS)


    email = next(
        (contact["value"] for contact in customer.get("contacts",[]) if contact["type"] == "email"),
        None,
    )

    return {"name": name, "city": city, "email": email}

