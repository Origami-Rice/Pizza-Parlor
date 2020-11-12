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

    def addToppings(self, topping):
        menu = self.getMenu()
        self.topping.extend(topping)
        toppings = menu["pizza"]["Toppings"]
        for i in topping:
            self.price += toppings[i] * self.quantity

    def changeSize(self, size):
        menu = self.getMenu()
        self.size = size
        pizzas = menu["pizza"]["Type"]
        if size == 12:
            self.price = pizzas[self.type][1]
        elif size == 15:
            self.price = pizzas[self.type][2]
        else:
            self.price = pizzas[self.type][3]
        self.price = self.price * self.quantity

    def changeTopping(self, topping):
        menu = self.getMenu()
        self.topping = topping
        orginPrice = 0
        toppings = menu["pizza"]["Toppings"]
        for i in self.topping:
            orginPrice += toppings[i]
        newPrice = 0
        for i in topping:
            newPrice += toppings[i]
        self.price -= (newPrice - orginPrice) * self.quantity

    def changeType(self, type):
        menu = self.getMenu()
        self.type = type
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if self.size == 12:
            self.price = pizzas[type][1]
        elif self.size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.getPrice() * self.getQuantity()

    def getTopping(self):
        return self.topping

    def getSize(self):
        return self.size
