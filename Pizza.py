import json
class Pizza:
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

    def changeQuantity(self, quantity):
        self.quantity = quantity

    def changeSize(self, size):
        menu = self.getMenu()
        pizzas = menu["pizza"]["Type"]
        if size == 12:
            self.price = pizzas[type][1]
        elif size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
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
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if self.size == 12:
            self.price = pizzas[type][1]
        elif self.size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]
        self.price = self.price * self.quantity


    def getTopping(self):
        return self.topping

    def getPrice(self):
        return self.price

    def getMenu(self):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        return menu










