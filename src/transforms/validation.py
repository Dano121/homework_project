from src.errors import ValidationError
from src.config import ALLOWED_STATUSES, REQUIRED_ORDER_FIELDS

def validate_order(order: dict, seen_ids: set[str]) -> dict:
    for field in REQUIRED_ORDER_FIELDS:
        if field not in order:
            raise ValidationError(f"Order {order['order_id']}: missing field {field}")
    if order["status"] not in ALLOWED_STATUSES:
            raise ValidationError(f"Order {order['order_id']}: {order['status']} is not allowed")

    if order["amount"] <= 0:
        raise ValidationError(f"Order {order['order_id']}: negative amount {order['amount']}")
    if order["order_id"] in seen_ids:
        raise ValidationError(f"Order {order['order_id']}: duplicate id")
    seen_ids.add(order["order_id"])
    return order