# main.py

from order_service import OrderService

def main():
    """Main function to simulate order processing."""
    order_service = OrderService()

    order_details = [
        ("apple", 2, 3),
        ("banana", 5, 1),
        ("orange", 10, 2)
    ]

    for item, quantity, price in order_details:
        order_service.create_order(item, quantity, price)

if __name__ == "__main__":
    main()
