from src.transforms.cleaning import clean_amount
from decimal import Decimal

def test_clean_amount():
    result = clean_amount("129,00")
    assert result == Decimal("129.00")

