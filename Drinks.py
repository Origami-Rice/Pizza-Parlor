import json
class Drinks:
    def __init__(self, type):
        self.type = type

    def jsonif(self):
        jdata = json.dumps(self.__dict__)
        return jdata
