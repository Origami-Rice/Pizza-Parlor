import json
class Drinks:
    def __init__(self, type, quantity):
        self.type = type
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.price = menu["drinks"][type]
        self.quantity = quantity

    def jsonif(self):
        jdata = json.dumps(self.__dict__)
        return jdata

    def changeQuantity(self, quantity):
        self.quantity = quantity
