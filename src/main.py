from src.config import RAW_DIR, ORDERS_PATTERN, ORDER_ITEMS_PATTERN
from src.clients.orders_files_source import read_all_csv
from src.clients.customers_file_source import read_customers
from src.transforms.cleaning import clean_order, clean_order_item
from src.transforms.validation import validate_order
from src.transforms.orders import normalize_all
from src.errors import ValidationError

def main() -> None:
    raw_orders = read_all_csv(RAW_DIR, ORDERS_PATTERN)
    raw_items = read_all_csv(RAW_DIR, ORDER_ITEMS_PATTERN)
    customers = read_customers(RAW_DIR / "customers.json")

    seen_ids: set[str] = set()
    cleaned_orders = []
    for o in raw_orders:
        try:
            cleaned = clean_order(o)
            validate_order(cleaned, seen_ids)
            cleaned_orders.append(cleaned)
        except ValidationError as e:
            print(f"Pominięto: {e}")

    cleaned_items = []
    for i in raw_items:
        try:
            cleaned_items.append(clean_order_item(i))
        except ValidationError as e:
            print(f"Pominięto: {e}")

    all_orders, all_items = normalize_all(cleaned_orders, cleaned_items, customers)

    print(f"Liczba zamówień: {len(all_orders)}")
    print(f"Liczba pozycji: {len(all_items)}")
    print("---")
    print("Przykładowe zamówienie:", all_orders[0])
    print("---")
    print("Przykładowa pozycja:", all_items[0])



if __name__ == "__main__":
    main()