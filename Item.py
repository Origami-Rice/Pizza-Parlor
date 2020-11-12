import json


class Item:
    def changeQuantity(self, quantity):
        self.quantity = quantity
        self.price = self.price * quantity

    def getPrice(self):
        return self.price

    def getMenu(self):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        return menu

    def getQuantity(self):
        return self.quantity

    def changeType(self, type):
        raise NotImplementedError

    def getType(self):
        return self.type
