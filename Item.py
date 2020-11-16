import json


class Item:
    """
        create a Item object
        attributes:
            type: what type of Item
            price: the total price of this Item object
            quantity: the quantity of this Item object
        """

    def __init__(self, type, quantity):
        self.type = type
        self.price = None
        self.quantity = quantity

    # change quantity of this Item, change price accordingly
    def change_quantity(self, quantity):
        self.price = (self.price / self.quantity) * quantity
        self.quantity = quantity

    # return the price of the Item
    def get_price(self):
        return self.price

    # return the menu of the Item
    def get_menu(self):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close()
        return menu

    # return the quantity of the Item
    def get_quantity(self):
        return self.quantity

    # change quantity of this Item, change price accordingly
    def change_type(self, type):
        raise NotImplementedError

    # return the type of the Item
    def get_type(self):
        return self.type
