# order_service.py
from inventory import Inventory
from payment import PaymentProcessor
from order import Order

class OrderService:
    def __init__(self):
        """Initialize the order service with an inventory and payment processor."""
        self.inventory = Inventory()
        self.payment_processor = PaymentProcessor()

    def create_order(self, item, quantity, price):
        """Create and process an order."""
        order = Order(item, quantity, price)
        if order.place_order(self.inventory, self.payment_processor):
            print(f"Order successful: {quantity} x {item}")
            return True
        print(f"Order failed: Not enough stock or payment issue for {item}")
        return False
