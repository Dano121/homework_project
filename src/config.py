from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
CURATED_DIR = PROJECT_DIR / "data" / "curated"
REJECTED_DIR = PROJECT_DIR / "data" / "rejected"

ORDERS_PATTERN = "orders_*.csv"
ORDER_ITEMS_PATTERN = "order_items_*.csv"

ALLOWED_STATUSES = {"paid","pending","shipped","cancelled"}
REQUIRED_ORDER_FIELDS = ["order_id","customer_id","amount","status"]

DEFAULT_CURRENCY = "PLN"
DEFAULT_ADDRESS = "Brak adresu"
DEFAULT_CONTACTS = "Brak email lub nr telefonu"


SOURCE_NAME = "homework-store"
UNKNOWN_CATEGORY = "UNKNOWN"