# main.py

from order import OrderService

def main():
    order_service = OrderService()
    order_details = [
        ("Laptop", 2, 1200),
        ("Headphones", 5, 200),
        ("Mouse", 10, 50)
    ]

    for item, quantity, price in order_details:
        success = order_service.create_order(item, quantity, price)
        if success:
            print(f"Order placed for {quantity} {item}(s)")
        else:
            print(f"Order failed for {item}")
