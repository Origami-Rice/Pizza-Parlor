import json
from Item import Item


class Pizza(Item):
    def __init__(self, type, size, quantity):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.type = type
        self.size = size
        self.category = "Pizza"
        self.quantity = quantity
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if size == 12:
            self.price = pizzas[type][1]
        elif size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.price * quantity

    def add_toppings(self, topping):
        menu = self.get_menu()
        self.topping.extend(topping)
        toppings = menu["pizza"]["Toppings"]
        for i in topping:
            self.price += toppings[i] * self.quantity

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

    def get_topping(self):
        return self.topping

    def get_size(self):
        return self.size
