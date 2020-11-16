import json
from Item import Item


class Pizza(Item):
    """
    create a pizza object
    attributes:
        size: the size of pizza, in 12, 15 or 18
        category: what is the item
        type: what type of pizza
        price: the total price of this pizza object
        quantity: the quantity of this pizza object
    """

    def __init__(self, type, size, quantity):
        super().__init__(type, quantity)
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close()
        self.size = size
        self.category = "Pizza"
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if size == 12:
            self.price = pizzas[type][1]
        elif size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.price * quantity

    """ add topping to the pizza and modify the price according to
     the change in topping"""

    def add_toppings(self, topping):
        menu = self.get_menu()
        self.topping.extend(topping)
        toppings = menu["pizza"]["Toppings"]
        for i in topping:
            self.price += toppings[i] * self.quantity

    # change the size of pizza, also change price according
    def change_size(self, size):
        menu = self.get_menu()
        self.size = size
        pizzas = menu["pizza"]["Type"]
        if size == 12:
            self.price = pizzas[self.type][1]
        elif size == 15:
            self.price = pizzas[self.type][2]
        else:
            self.price = pizzas[self.type][3]
        self.price = self.price * self.quantity

    # change the topping of pizza, also change price according
    def change_topping(self, topping):
        menu = self.get_menu()
        orginPrice = 0
        toppings = menu["pizza"]["Toppings"]
        for i in self.topping:
            orginPrice += toppings[i]
        newPrice = 0
        for i in topping:
            newPrice += toppings[i]
        self.price -= (orginPrice - newPrice) * self.quantity
        self.topping = topping

    # change the type of pizza, also change price according
    def change_type(self, type):
        menu = self.get_menu()
        self.type = type
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if self.size == 12:
            self.price = pizzas[type][1]
        elif self.size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.get_price() * self.get_quantity()

    # get the topping of pizza
    def get_topping(self):
        return self.topping

    # get the topping of pizza
    def get_size(self):
        return self.size
