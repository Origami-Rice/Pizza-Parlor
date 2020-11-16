from Drinks import Drinks


class DrinkFactory:

    @staticmethod
    # factory method for create drink
    def creat_item(type, quantity):
        return Drinks(type, quantity)
