"""Functions for cleaning and calculating order data."""


def calculate_total(price: float, quantity: int) -> float:
    """Return the total cost for a quantity of items at a given price."""
    return price * quantity


def apply_discount(total: float, percent: float) -> float:
    """Return the total after taking off a percentage discount."""
    return total * (1 - percent / 100)


def clean_product_name(name: str) -> str:
    """Return a product name with extra spaces removed, in lowercase."""
    return name.strip().lower()