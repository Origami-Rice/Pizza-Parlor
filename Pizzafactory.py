from Pizza import Pizza


class PizzaFactory:

    @staticmethod
    def create_item(type, size, quantity):
        return Pizza(type, size, quantity)
