import unittest
from PizzaParlour import app
import json
from Pizza import Pizza
from Drinks import Drinks
from Order import Order


def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


def test_create():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        new_no = int(last_no) + 1
        order_no = str(new_no)
        f.close()
    with app.test_client() as client:
        # send data as POST form to endpoint
        sent = {"order_number": "1",
                "items": [{"type": "pepperoni", "size": 12, "topping": [
                    "olives", "tomatoes", "olives", "tomatoes"], "price": 14}]}
        result = client.post(
            '/create',
            data=sent
        )
        # check result from server with expected data
        print(result.data.decode('utf-8'))
        assert result.data.decode('utf-8') == str(new_no)


def test_retrieve():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        f.close()
    response = app.test_client().get('/retrieve/' + last_no)
    print("order_no: " + last_no)
    assert response.status_code == 200


def test_update():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        f.close()
    with app.test_client() as client:
        # send data as POST form to endpoint
        sent = {"order_number": "1",
                "items": [{"type": "pepperoni", "size": 12, "topping": [
                    "olives", "tomatoes", "olives", "tomatoes"], "price": 14}]}
        response = client.post(
            '/update/' + last_no,
            data=sent
        )
    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == last_no


def test_delete():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        f.close()
    response = app.test_client().get('/delete/' + last_no)
    assert response.status_code == 200


def test_delete_not_found():
    response = app.test_client().get('/delete/1000')
    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == "1000"


def test_retrieve_not_found():
    response = app.test_client().get('/retrieve/1000')

    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == "ERROR: order - 1000 not found!"


def test_update_not_found():
    with app.test_client() as client:
        # send data as POST form to endpoint
        sent = {"order_number": "1",
                "items": [{"type": "pepperoni", "size": 12, "topping": [
                    "olives", "tomatoes", "olives", "tomatoes"], "price": 14}]}
        response = client.post(
            '/update/1000',
            data=sent
        )
    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == "ERROR: order - 1000 not found!"


class TestPizzaClass(unittest.TestCase):

    def test_init(self):
        pizza = Pizza("pepperoni", 12, 1)
        self.assertEqual(pizza.getPrice(), 10)
        self.assertEqual(pizza.getSize(), 12)
        self.assertEqual(pizza.getType(), "pepperoni")
        self.assertEqual(pizza.getQuantity(), 1)

    def test_addEmptyTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.addToppings([])
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 10)

    def test_addOneTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.addToppings(["olives"])
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes", "olives"])
        self.assertEqual(pizza.getPrice(), 12.0)

    def test_addMultipleTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.addToppings(["olives", "mushrooms"])
        self.assertEqual(pizza.getTopping(),
                         ["olives", "tomatoes", "olives", "mushrooms"])
        self.assertEqual(pizza.getPrice(), 13.5)

    def test_addEmptyToppingAndMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.addToppings([])
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 20)

    def test_addOneToppingAndMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.addToppings(["olives"])
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes", "olives"])
        self.assertEqual(pizza.getPrice(), 24.0)

    def test_addMultipleToppingAndMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.addToppings(["olives", "mushrooms"])
        self.assertEqual(pizza.getTopping(),
                         ["olives", "tomatoes", "olives", "mushrooms"])
        self.assertEqual(pizza.getPrice(), 27.0)

    def test_pizzachangeSize(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeSize(15)
        self.assertEqual(pizza.getSize(), 15)
        self.assertEqual(pizza.getPrice(), 15)

    def test_pizzachangeSizeMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.changeSize(15)
        self.assertEqual(pizza.getSize(), 15)
        self.assertEqual(pizza.getPrice(), 30)

    def test_pizzaChangeType(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeType("margherita")
        self.assertEqual(pizza.getType(), "margherita")
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 11)

    def test_pizzaChangeTypeMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.changeType("margherita")
        self.assertEqual(pizza.getType(), "margherita")
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 22)

    def test_pizzaGetTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])

    def test_pizzaGetQuantity(self):
        pizza = Pizza("pepperoni", 12, 1)
        self.assertEqual(pizza.getQuantity(), 1)

    def test_pizzaGetSiza(self):
        pizza = Pizza("pepperoni", 12, 1)
        self.assertEqual(pizza.getSize(), 12)

    def test_pizzaChangeTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeTopping(["olives"])
        self.assertEqual(pizza.getTopping(), ["olives"])
        self.assertEqual(pizza.getPrice(), 8)

    def test_pizzaChangeQuantity(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeQuantity(3)
        self.assertEqual((pizza.getPrice()), 30)

    def test_pizzaChangeToppingMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.changeTopping(["olives"])
        self.assertEqual(pizza.getTopping(), ["olives"])
        self.assertEqual(pizza.getPrice(), 16)

    def test_getMenu(self):
        pizza = Pizza("pepperoni", 12, 1)
        menu = pizza.getMenu()
        self.assertEqual(menu, {
            "drinks": {
                "Coke": 2.5,
                "Diet Coke": 3,
                "Coke Zero": 3,
                "Pepsi": 2.5,
                "Diet Pepsi": 3,
                "Dr. Pepper": 4,
                "Water": 1,
                "Juice": 2
            },
            "pizza": {
                "Type": {
                    "pepperoni": [
                        [
                            "olives",
                            "tomatoes"
                        ],
                        10,
                        15,
                        20
                    ],
                    "margherita": [
                        [
                            "olives",
                            "tomatoes"
                        ],
                        11,
                        15,
                        20
                    ],
                    "vegetarian": [
                        [
                            "olives",
                            "tomatoes"
                        ],
                        10,
                        15,
                        20
                    ],
                    "Neapolitan": [
                        [
                            "olives",
                            "tomatoes"
                        ],
                        10,
                        15,
                        20
                    ]
                },
                "Toppings": {
                    "olives": 2,
                    "tomatoes": 2,
                    "mushrooms": 1.5,
                    "jalapenos": 2,
                    "chicken": 5,
                    "beef": 6,
                    "pepperoni": 6
                }
            }
        })


class TestDrinksClass(unittest.TestCase):

    def test_init(self):
        drink = Drinks("Coke", 2)
        self.assertEqual(drink.getPrice(), 5.0)

    def test_priceWithMultipleQuantity(self):
        drink = Drinks("Diet Coke", 2)
        self.assertEqual(drink.getPrice(), 6)

    def test_drinkChangeType(self):
        drink = Drinks("Coke", 1)
        drink.changeType("Diet Coke")
        self.assertEqual(drink.getType(), "Diet Coke")
        self.assertEqual(drink.getPrice(), 3)

    def test_drinkChangeTypeMultipleQuantity(self):
        drink = Drinks("Coke", 2)
        drink.changeType("Diet Coke")
        self.assertEqual(drink.getType(), "Diet Coke", 6)

    def test_drinkChangeQuantity(self):
        drink = Drinks("Coke", 1)
        drink.changeQuantity(2)
        self.assertEqual(drink.getPrice(), 5)


class TestOrderClass(unittest.TestCase):

    def test_init(self):
        order = Order(1)
        self.assertEqual(order.getItems(), [])
        self.assertEqual(order.getOrderNumber(), 1)

    def test_orderTotalcost(self):
        drink = Drinks("Coke", 1)
        pizza = Pizza("pepperoni", 12, 2)
        order = Order(1)
        order.addItem(drink)
        order.addItem(pizza)
        self.assertEqual(order.getTotalPrice(), 22.5)

    def test_emptyorderTotalCost(self):
        order = Order(1)
        self.assertEqual(order.getTotalPrice(), 0)

    def test_getOrderNumber(self):
        order = Order(1)
        self.assertEqual(order.getOrderNumber(), 1)

    def test_addItem(self):
        drink = Drinks("Coke", 1)
        pizza = Pizza("pepperoni", 12, 2)
        order = Order(1)
        order.addItem(drink)
        order.addItem(pizza)
        self.assertEqual(order.getItems()[0].__dict__,
                         {"type": "Coke", "price": 2.5, "quantity": 1, "category": "Drink"})
        self.assertEqual(order.getItems()[1].__dict__,
                         {"type": "pepperoni", "price": 20, "quantity": 2, "category": "Pizza", "size": 12,
                          "topping": ['olives', 'tomatoes'], })

    def test_jsonify(self):
        drink = Drinks("Coke", 1)
        order = Order(1)
        order.addItem(drink)
        self.assertEqual(order.jsonify(), '{"order_number": 1, "items": "[{\\"type\\": \\"Coke\\", \\"price\\": 2.5, \\"quantity\\": 1, \\"category\\": \\"Drink\\"}]"}')