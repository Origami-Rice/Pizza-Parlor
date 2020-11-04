class Menu:
    def __init__(self):
        self.Pizza = {"size": ["s", "m", "l"],
                      "type": ["pepperoni", "margherita", "vegetarian", "Neapolitan"],
                      "Topping":["olives","tomatoes","mushrooms","jalapenos","chicken","beef","pepperoni"]}
        self.Drinkstype = ["Coke", "Diet Coke", "Coke Zero", "Pepsi", "Diet Pepsi", "Dr. Pepper", "Water", "Juice"]

    def addPizzaType(self,type):
        self.Pizza["size"].append(type)