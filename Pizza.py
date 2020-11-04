import json
class Pizza:
    def __init__(self, size, topping, type):
        self.size = size
        self.topping = topping
        self.type = type

    def jsonif(self):
        jdata = json.dumps(self.__dict__)
        return jdata

