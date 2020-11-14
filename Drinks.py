import json
from Item import Item


class Drinks(Item):
    def __init__(self, type, quantity):
        super().__init__(type, quantity)
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close()
        self.price = menu["drinks"][type] * quantity
        self.category = "Drink"

    def change_type(self, type):
        menu = self.get_menu()
        self.type = type
        self.price = menu["drinks"][type] * self.quantity
