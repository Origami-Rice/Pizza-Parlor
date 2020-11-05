import json
class Drinks:
    def __init__(self, type):
        self.type = type
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.price = menu["drinks"][type]

    def jsonif(self):
        jdata = json.dumps(self.__dict__)
        return jdata
