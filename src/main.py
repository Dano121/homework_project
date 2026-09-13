from src.config import RAW_DIR, ORDERS_PATTERN
from src.clients.orders_files_source import read_all_csv
from src.transforms.cleaning import clean_order

def main() -> None:
    orders = read_all_csv(RAW_DIR, ORDERS_PATTERN)
    print(orders[0])
    print(clean_order(orders[0]))



if __name__ == "__main__":
    main()