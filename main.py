from pathlib import Path

from file_utils import read_csv, write_csv, write_json
from transforms import apply_discount, calculate_total, clean_product_name

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"


def transform(row: dict) -> dict:
    """Clean one order and add calculated totals."""
    price = float(row["price"])
    quantity = int(row["quantity"])
    total = calculate_total(price, quantity)
    return {
        "order_id": int(row["order_id"]),
        "product": clean_product_name(row["product"]),
        "price": price,
        "quantity": quantity,
        "total": round(total, 2),
        "discounted_total": round(apply_discount(total, 10), 2),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    rows = read_csv(DATA_DIR / "orders.csv")
    clean_rows = [transform(row) for row in rows]
    write_csv(clean_rows, OUTPUT_DIR / "orders_clean.csv")
    write_json(clean_rows, OUTPUT_DIR / "orders_clean.json")
    print(f"Read {len(rows)} rows, wrote {len(clean_rows)} rows to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()