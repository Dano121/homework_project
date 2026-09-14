from datetime import datetime,timezone
from src.config import SOURCE_NAME,DEFAULT_ADDRESS,DEFAULT_CONTACTS,UNKNOWN_CATEGORY
from src.clients.customers_file_source import flatten_customer



def normalize_order(order: dict, customers: dict, item_count: int) -> dict:
    order_id = order["order_id"]
    order_date = order["order_date"]
    customer_id = order["customer_id"]
    amount = order["amount"]
    currency = order["currency"]
    status = order["status"]
    if customer_id in customers:
        flat = flatten_customer(customers[customer_id])
        customer_name = flat["name"]
        customer_city = flat["city"]
        customer_email = flat["email"] if flat["email"] is not None else DEFAULT_CONTACTS
    else:
        customer_name = UNKNOWN_CATEGORY
        customer_city = DEFAULT_ADDRESS
        customer_email = DEFAULT_CONTACTS
    ingested_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "order_id": order_id,
        "order_date": order_date,
        "customer_id": customer_id,
        "amount": amount,
        "currency": currency,
        "status": status,
        "customer_name": customer_name,
        "customer_city": customer_city,
        "customer_email": customer_email,
        "item_count": item_count,
        "source": SOURCE_NAME,
        "ingested_at": ingested_at,
        }
def normalize_order_items(order_id: str, items: list[dict]) -> list[dict]:
    result = []
    for position, item in enumerate(items, start=1):
        line_total = item["quantity"] * item["unit_price"]
        result.append({
            "order_id": order_id,
            "position": position,
            "sku": item["sku"],
            "product_name": item["product_name"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "line_total": line_total,
        })
    return result

def normalize_all(orders: list[dict], items: list[dict], customers: dict[str,dict]) -> tuple[list[dict], list[dict]]:
    grouped_items = {}
    for item in items:
        if item["order_id"] not in grouped_items:
            grouped_items[item["order_id"]] = []
        grouped_items[item["order_id"]].append(item)
    all_orders = []
    all_items = []
    for order in orders:
        order_items = grouped_items.get(order["order_id"], [])
        item_count = len(order_items)
        normalized_order = normalize_order(order, customers, item_count)
        all_orders.append(normalized_order)
        normalized_items = normalize_order_items(order["order_id"], order_items)
        all_items.extend(normalized_items)
    return all_orders, all_items
