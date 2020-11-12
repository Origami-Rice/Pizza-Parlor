import json
from Item import Item


class Drinks(Item):
    def __init__(self, type, quantity):
        self.type = type
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.price = menu["drinks"][type] * quantity
        self.quantity = quantity
        self.category = "Drink"

    def changeType(self, type):
        menu = self.getMenu()
        self.type = type
        self.price = menu["drinks"][type] * self.quantity
