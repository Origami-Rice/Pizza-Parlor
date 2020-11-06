from Pizza import Pizza
from Drinks import Drinks
import json


class Order:
    def __init__(self, order_number):
        self.order_number = order_number
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def jsonify(self):
        jdata = {
            "order_number": self.order_number,
            "items": []
        }
        jsonItems = json.dumps([item.__dict__ for item in self.items])
        jdata["items"] = jsonItems
        jsondata = json.dumps(jdata)
        return jsondata

    def getTotalPrice(self):
        totalPrice = 0.0
        for i in self.items:
            totalPrice += i.price * i.quantity
        return totalPrice
