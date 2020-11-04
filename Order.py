from Pizza import Pizza
from Drinks import Drinks
import json
from types import SimpleNamespace


class Order:
    def __init__(self):
        self.order_number = 1
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


d1 = Drinks("coe")
p1 = Pizza("large","olive","vege")
o1 = Order()
o1.addItem(d1)
o1.addItem(p1)
jsonOrder = o1.jsonify()
print(jsonOrder)
con = json.loads(jsonOrder)
print(con["items"])