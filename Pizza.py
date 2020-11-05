import json
class Pizza:
    def __init__(self, type, size):
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        self.type = type
        self.size = size
        pizzas = menu["pizza"]["Type"]
        self.topping = pizzas[type][0]
        if size == 12:
            self.price = pizzas[type][1]
        elif size == 15:
            self.price = pizzas[type][2]
        else:
            self.price = pizzas[type][3]


    def addToppings(self, topping):
        self.topping.extend(topping)
        with open('order/Menu.json') as f:
            menu = json.load(f)
            f.close
        toppings = menu["pizza"]["Toppings"]
        for i in topping:
            self.price += toppings[i]


