from Pizza import Pizza


class PizzaFactory:

    # factory method for create pizza
    @staticmethod
    def create_item(type, size, quantity):
        return Pizza(type, size, quantity)
