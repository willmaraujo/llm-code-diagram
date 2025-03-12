# order.py

from inventory import Inventory
from payment import PaymentProcessor

class Order:
    def __init__(self, item, quantity, price):
        """Initialize an order with an item, quantity, and price."""
        self.item = item
        self.quantity = quantity
        self.price = price

    def total_amount(self):
        """Calculate the total amount of the order."""
        return self.quantity * self.price

    def place_order(self, inventory: Inventory, payment_processor: PaymentProcessor):
        """Place an order if inventory and payment conditions are met."""
        if inventory.update_stock(self.item, self.quantity):
            return payment_processor.process_payment(self.total_amount())
        return False
