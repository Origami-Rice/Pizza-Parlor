import json
from Item import Item


class Drinks(Item):
    """
        create a drink object
        attributes:
            type: what type of drink
            price: the total price of this drink object
            quantity: the quantity of this drink object
        """

    def __init__(self, type, quantity):
        super().__init__(type, quantity)
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close()
        self.price = menu["drinks"][type] * quantity
        self.category = "Drink"

    # change the type of this drink object, change price accordingly
    def change_type(self, type):
        menu = self.get_menu()
        self.type = type
        self.price = menu["drinks"][type] * self.quantity
