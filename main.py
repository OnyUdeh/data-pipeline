from transforms import apply_discount, calculate_total, clean_product_name

ORDERS = [
    {"product": "  Widget ", "price": 2.50, "quantity": 4},
    {"product": "GADGET", "price": 10.00, "quantity": 1},
    {"product": "gizmo  ", "price": 4.75, "quantity": 2},
]


def main() -> None:
    for order in ORDERS:
        name = clean_product_name(order["product"])
        total = calculate_total(order["price"], order["quantity"])
        discounted = apply_discount(total, 10)
        print(f"{name}: {total:.2f} -> {discounted:.2f} after 10% off")


if __name__ == "__main__":
    main()
    