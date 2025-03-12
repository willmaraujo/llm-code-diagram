# order.py

from inventory import Inventory
from payment import PaymentProcessor
from order import Order

class OrderService:
    def __init__(self):
        self.inventory = Inventory()
        self.payment_processor = PaymentProcessor()

    def create_order(self, item, quantity, price):
        order = Order(item, quantity, price)
        if order.place_order(self.inventory, self.payment_processor):
            print("Order successful.")
        else:
            print("Order failed.")
