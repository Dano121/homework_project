import json
from pathlib import Path
from src.config import DEFAULT_ADDRESS
from src.errors import ConfigError


def read_customers(path: Path) -> dict[str, dict]:
    if not path.is_file():
        raise ConfigError(f"File {path} does not exist.")
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        lookup = {customer["id"]: customer for customer in data}
        return lookup

def flatten_customer(customer: dict) -> dict[str, str | None]:
    name = customer["name"]

    if customer["address"] is None:
        city = DEFAULT_ADDRESS
    else:
        city = customer["address"]["city"]
    if not customer["contacts"]:
        email = None
    else:
        email = customer["contacts"][0]["value"]
    return {"name": name, "city": city, "email": email}

