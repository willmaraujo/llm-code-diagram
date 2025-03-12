# inventory.py

class Inventory:
    def __init__(self):
        self.stock = {
            "apple": 50,
            "banana": 30,
            "orange": 20
        }

    def check_stock(self, item, quantity):
        """Check if the requested quantity of an item is available."""
        return self.stock.get(item, 0) >= quantity

    def update_stock(self, item, quantity):
        """Reduce the stock of an item if enough quantity is available."""
        if self.check_stock(item, quantity):
            self.stock[item] -= quantity
            return True
        return False
