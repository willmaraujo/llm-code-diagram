# inventory.py

class Inventory:
    def __init__(self):
        self.stock = {
            "apple": 50,
            "banana": 30,
            "orange": 20
        }

    def check_stock(self, item, quantity):
        return self.stock.get(item, 0) >= quantity

    def update_stock(self, item, quantity):
        if self.check_stock(item, quantity):
            self.stock[item] -= quantity
            return True
        return False
