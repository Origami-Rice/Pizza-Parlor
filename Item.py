import json


class Item:
    def __init__(self, type, quantity):
        self.type = type
        self.price = None
        self.quantity = quantity

    def change_quantity(self, quantity):
        self.price = (self.price / self.quantity) * quantity
        self.quantity = quantity

    def get_price(self):
        return self.price

    def get_menu(self):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close()
        return menu

    def get_quantity(self):
        return self.quantity

    def change_type(self, type):
        raise NotImplementedError

    def get_type(self):
        return self.type
