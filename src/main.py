import sys

from config import CURATED_DIR, REJECTED_DIR
from src.config import RAW_DIR, ORDERS_PATTERN, ORDER_ITEMS_PATTERN
from src.clients.orders_files_source import read_all_csv
from src.clients.customers_file_source import read_customers
from src.transforms.cleaning import clean_order, clean_order_item
from src.transforms.validation import validate_order
from src.transforms.orders import normalize_all
from src.errors import ValidationError, PipelineError
from src.storage.csv_writer import write_rows

def main() -> None:
    raw_orders = read_all_csv(RAW_DIR, ORDERS_PATTERN)
    raw_items = read_all_csv(RAW_DIR, ORDER_ITEMS_PATTERN)
    customers = read_customers(RAW_DIR / "customers.json")

    seen_ids: set[str] = set()
    rejected_orders = []
    cleaned_orders = []
    for o in raw_orders:
        try:
            cleaned = clean_order(o)
            validate_order(cleaned, seen_ids)
            cleaned_orders.append(cleaned)
        except ValidationError as e:
            rejected_orders.append({"order_id": o["order_id"], "reason": str(e)})
            print(f"Pominięto: {e}")

    cleaned_items = []
    for i in raw_items:
        try:
            cleaned_items.append(clean_order_item(i))
        except ValidationError as e:
            print(f"Pominięto: {e}")

    all_orders, all_items = normalize_all(cleaned_orders, cleaned_items, customers)


    print(f"Liczba wczytanych zamówień: {len(raw_orders)}",
          f"Liczba odrzuconych zamówień: {len(rejected_orders)}",
          f"Liczba zamówień: {len(all_orders)}",
          f"Liczba pozycji: {len(all_items)}",
          )

    write_rows(all_orders, CURATED_DIR / "orders.csv")
    write_rows(all_items, CURATED_DIR / "order_items.csv")
    write_rows(rejected_orders, REJECTED_DIR / "orders_rejected.csv")



if __name__ == "__main__":
    try:
        main()
    except PipelineError as e:
        print(f"Przerwano: {e}")
        sys.exit(1)

# tutaj zawsze :
# if __name__ == "__main__":
#     main()


# zrob cos na wzor:
# def main() -> None:
#     try:
#         summary = run()
#     except PipelineError as error:
#         print(f"run aborted -- {type(error).__name__}: {error}")
#         raise SystemExit(1) from error
#
#     print(
#         f"read: {summary['read']} orders | "
#         f"rejected: {summary['rejected']} | "
#         f"orders: {summary['orders']} rows | "
#         f"order_items: {summary['items']} rows | "
#         f"output: {summary['output_dir']}"
#     )
#
#
# if __name__ == "__main__":
#     main()


# to co wiekszosc masz w main dopisz metode run nad main w tym pliku
