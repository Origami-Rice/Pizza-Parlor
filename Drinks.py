import json
class Drinks:
    def __init__(self, type, quantity):
        self.type = type
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.menu = menu
        self.price = menu["drinks"][type] * quantity
        self.quantity = quantity
        self.category = "Drink"

    def jsonif(self):
        jdata = json.dumps(self.__dict__)
        return jdata

    def changeQuantity(self, quantity):
        self.quantity = quantity

    def getPrice(self):
        return self.price

    def changeType(self, type):
        self.type = type
        self.price = self.menu["drinks"][type] * self.quantity
