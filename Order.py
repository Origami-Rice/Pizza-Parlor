from Pizza import Pizza
from Drinks import Drinks
import json


class Order:
    def __init__(self, order_number):
        self.order_number = order_number
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def addDrinks(self, type):
        drink = Drinks(type)
        self.addItem(drink)

    def addPizza(self, size, topping, type):
        pizza = Pizza(size, topping, type)
        self.addItem(pizza)

    def jsonify(self):
        jdata = {
            "order_number": self.order_number,
            "items": []
        }
        jsonItems = json.dumps([item.__dict__ for item in self.items])
        jdata["items"] = jsonItems
        jsondata = json.dumps(jdata)
        return jsondata
