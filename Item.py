import json


class Item:
    def change_quantity(self, quantity):
        self.quantity = quantity
        self.price = self.price * quantity

    def get_price(self):
        return self.price

    def get_menu(self):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        return menu

    def get_quantity(self):
        return self.quantity

    def change_type(self, type):
        raise NotImplementedError

    def get_type(self):
        return self.type
