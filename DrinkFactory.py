from Drinks import Drinks


class DrinkFactory:

    @staticmethod
    def creat_item(type, quantity):
        return Drinks(type, quantity)
