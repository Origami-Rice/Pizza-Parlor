import json
class Pizza:
    def __init__(self, type, size, quantity):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.menu = menu
        self.type = type
        self.size = size
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
        self.topping.extend(topping)
        toppings = self.menu["pizza"]["Toppings"]
        for i in topping:
            self.price += toppings[i] * self.quantity

    def changeQuantity(self, quantity):
        self.quantity = quantity

    def changeSize(self, size):
        pizzas = self.menu["pizza"]["Type"]
        if size == 12:
            self.price = pizzas[type][1]
        elif size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.price * self.quantity

    def changeTopping(self, topping):
        self.topping = topping
        orginPrice = 0
        toppings = self.menu["pizza"]["Toppings"]
        for i in self.topping:
            orginPrice += toppings[i]
        newPrice = 0
        for i in topping:
            newPrice += toppings[i]
        self.price -= (newPrice - orginPrice) * self.quantity

    def getTopping(self):
        return self.topping

    def getPrice(self):
        return self.price









