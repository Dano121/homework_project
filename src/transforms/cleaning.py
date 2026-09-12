import decimal

from src.errors import ValidationError
from datetime import datetime

def clean_text(value: str) -> str | None:

    clean_value = value.strip()
    if clean_value == "":
        return None
    else:
        return clean_value

def clean_amount(value:str) -> decimal.Decimal:
    new_value = value.strip()
    new_value = new_value.replace(",", ".")
    if new_value == "":
        raise ValidationError("Please enter a valid amount")
    try:
        return decimal.Decimal(new_value)
    except decimal.InvalidOperation:
        raise ValidationError("Please enter a valid amount")

def clean_int(value:str) -> int:
    clean_int_value = value.strip()
    if clean_int_value == "":
        raise ValidationError("Please enter a valid integer")
    try:
        return int(clean_int_value)
    except ValueError:
        raise ValidationError("Please enter a valid integer")

def clean_date(value:str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        try:
            parsed = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValidationError("Please enter a valid date")
    return parsed.strftime("%Y-%m-%d")


def clean_order(raw:dict) -> dict:
    order_id = raw["order_id"]
    try:
        customer_id = clean_text(raw["customer_id"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        order_date = clean_date(raw["order_date"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        amount = clean_amount(raw["amount"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        currency = clean_text(raw["currency"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        status = clean_text(raw["status"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date,
        "amount": amount,
        "currency": currency,
        "status": status,
    }

def clean_order_item(raw:dict) -> dict:
    order_id = raw["order_id"]
    try:
        sku = clean_text(raw["sku"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        product_name = clean_text(raw["product_name"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        quantity = clean_int(raw["quantity"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    try:
        unit_price = clean_amount(raw["unit_price"])
    except ValidationError as error:
        raise ValidationError(f"Order {order_id}: {error}") from error
    return {
        "order_id": order_id,
        "sku": sku,
        "product_name": product_name,
        "quantity": quantity,
        "unit_price": unit_price,
    }