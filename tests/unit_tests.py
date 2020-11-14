import unittest
from PizzaParlour import app
from Main import *
import io
import sys
import mock


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

    def test_initMidPizza(self):
        pizza = Pizza("pepperoni", 15, 1)
        self.assertEqual(pizza.getPrice(), 15)
        self.assertEqual(pizza.getSize(), 15)
        self.assertEqual(pizza.getType(), "pepperoni")
        self.assertEqual(pizza.getQuantity(), 1)

    def test_initLargePizza(self):
        pizza = Pizza("pepperoni", 18, 1)
        self.assertEqual(pizza.getPrice(), 20)
        self.assertEqual(pizza.getSize(), 18)
        self.assertEqual(pizza.getType(), "pepperoni")
        self.assertEqual(pizza.getQuantity(), 1)

    def test_initMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        self.assertEqual(pizza.getPrice(), 20)
        self.assertEqual(pizza.getSize(), 12)
        self.assertEqual(pizza.getType(), "pepperoni")
        self.assertEqual(pizza.getQuantity(), 2)

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

    def test_pizzachangeSizeToMid(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeSize(15)
        self.assertEqual(pizza.getSize(), 15)
        self.assertEqual(pizza.getPrice(), 15)

    def test_pizzachangeSizeToSmall(self):
        pizza = Pizza("pepperoni", 15, 1)
        pizza.changeSize(12)
        self.assertEqual(pizza.getSize(), 12)
        self.assertEqual(pizza.getPrice(), 10)

    def test_pizzachangeSizeToLarge(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeSize(18)
        self.assertEqual(pizza.getSize(), 18)
        self.assertEqual(pizza.getPrice(), 20)

    def test_pizzachangeSizeMultipleQuantity(self):
        pizza = Pizza("pepperoni", 12, 2)
        pizza.changeSize(15)
        self.assertEqual(pizza.getSize(), 15)
        self.assertEqual(pizza.getPrice(), 30)

    def test_SmallpizzaChangeType(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeType("margherita")
        self.assertEqual(pizza.getType(), "margherita")
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 11)

    def test_MidpizzaChangeType(self):
        pizza = Pizza("pepperoni", 15, 1)
        pizza.changeType("margherita")
        self.assertEqual(pizza.getType(), "margherita")
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 15)

    def test_LargepizzaChangeType(self):
        pizza = Pizza("pepperoni", 18, 1)
        pizza.changeType("margherita")
        self.assertEqual(pizza.getType(), "margherita")
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes"])
        self.assertEqual(pizza.getPrice(), 20)

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

    def test_pizzaChangeToLessTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeTopping(["olives"])
        self.assertEqual(pizza.getTopping(), ["olives"])
        self.assertEqual(pizza.getPrice(), 8)

    def test_pizzaChangeToMoreTopping(self):
        pizza = Pizza("pepperoni", 12, 1)
        pizza.changeTopping(["olives", "tomatoes", "chicken"])
        self.assertEqual(pizza.getTopping(), ["olives", "tomatoes", "chicken"])
        self.assertEqual(pizza.getPrice(), 15)

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
                    ],
                    "custom": [
                        [],
                        5,
                        10,
                        15
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

    def test_drinkGetType(self):
        drink = Drinks("Coke", 1)
        self.assertEqual(drink.getType(), "Coke")


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
        self.assertEqual(order.jsonify(),
                         '{"order_number": 1, "items": "[{\\"type\\": \\"Coke\\", \\"price\\": 2.5, \\"quantity\\": 1, \\"category\\": \\"Drink\\"}]"}')


class test_main_file(unittest.TestCase):

    def test_submit_emptyorder(self):
        order = Order(1)
        self.assertEqual(submitOrder(order), "can't submit empty order")

    def test_submit_order(self):
        drink = Drinks("Coke", 1)
        pizza = Pizza("pepperoni", 12, 2)
        order = Order(1)
        order.addItem(drink)
        order.addItem(pizza)
        self.assertEqual(submitOrder(order), 200)

    def test_print_pizza(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_pizzas()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), '''Pizzas:
pepperoni Small: $10 Medium: $15 Large: $20
margherita Small: $11 Medium: $15 Large: $20
vegetarian Small: $10 Medium: $15 Large: $20
Neapolitan Small: $10 Medium: $15 Large: $20
custom Small: $5 Medium: $10 Large: $15
''')

    def test_print_drinks(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_drinks()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), '''Drinks:
Coke: $2.5
Diet Coke: $3
Coke Zero: $3
Pepsi: $2.5
Diet Pepsi: $3
Dr. Pepper: $4
Water: $1
Juice: $2
''')

    def test_print_topping(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_toppings()
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''Toppings:
olives: $2
tomatoes: $2
mushrooms: $1.5
jalapenos: $2
chicken: $5
beef: $6
pepperoni: $6
''')

    def test_print_iteminfo_drink(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        printItemInfo("Coke")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''Coke price is $2.5
''')

    def test_print_iteminfo_pizza(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        printItemInfo("pepperoni")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''pepperoni pizza prices are $10 (small), $15 (medium), $20 (large)
''')

    def test_print_menuhelper1(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        printMenuHelper("1")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''--------------------------Menu--------------------------
Pizzas:
pepperoni Small: $10 Medium: $15 Large: $20
margherita Small: $11 Medium: $15 Large: $20
vegetarian Small: $10 Medium: $15 Large: $20
Neapolitan Small: $10 Medium: $15 Large: $20
custom Small: $5 Medium: $10 Large: $15
Drinks:
Coke: $2.5
Diet Coke: $3
Coke Zero: $3
Pepsi: $2.5
Diet Pepsi: $3
Dr. Pepper: $4
Water: $1
Juice: $2
''')

    def test_print_menuhelper2(self):
        with mock.patch('builtins.input', return_value="Coke"):
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            printMenuHelper("2")
            sys.stdout = sys.__stdout__
            a = capturedOutput.getvalue()
            self.assertEqual(capturedOutput.getvalue(), '''Coke price is $2.5
''')

    def test_print_menu(self):
        with mock.patch('builtins.input', return_value="1"):
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            printMenu()
            sys.stdout = sys.__stdout__
            a = capturedOutput.getvalue()
            self.assertEqual(capturedOutput.getvalue(), '''--------------------------Menu--------------------------
Pizzas:
pepperoni Small: $10 Medium: $15 Large: $20
margherita Small: $11 Medium: $15 Large: $20
vegetarian Small: $10 Medium: $15 Large: $20
Neapolitan Small: $10 Medium: $15 Large: $20
custom Small: $5 Medium: $10 Large: $15
Drinks:
Coke: $2.5
Diet Coke: $3
Coke Zero: $3
Pepsi: $2.5
Diet Pepsi: $3
Dr. Pepper: $4
Water: $1
Juice: $2
''')

    def test_setup_drink(self):
        with mock.patch('builtins.input', return_value="Coke"):
            a = setUpDrinkType()
            self.assertEqual(setUpDrinkType(), 'Coke')

    def test_order_cancel(self):
        with mock.patch('builtins.input', return_value="1026"):
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            processOrderCancellation()
            sys.stdout = sys.__stdout__
            a = capturedOutput.getvalue()
            self.assertEqual(capturedOutput.getvalue(), '''The order has been deleted.
''')

    def test_print_mainmenu_option(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        printMainMenuOptions()
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''Select a number for the action you would like to do: 
        1. Access the menu  
        2. Submit an order
        3. Update an existing order 
        4. Cancel an order
        5. Call for delivery/pickup. 
        6. Quit 
        
''')

    def test_process_ordersubmit(self):
        with mock.patch('builtins.input', return_value="2"):
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            processOrderSubmission()
            sys.stdout = sys.__stdout__
            self.assertEqual(capturedOutput.getvalue(), '''can't submit empty order\n''')

    def test_setup_topping(self):
        with mock.patch('builtins.input', return_value="q"):
            self.assertEqual(setUpTopping(), [])

    def test_setup_quantity(self):
        with mock.patch('builtins.input', return_value="3"):
            self.assertEqual(setUpQuantity(), "3")

    def test_normal_delivery(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        normalDelivery([{'type': 'custom', 'size': 12, 'category': 'Pizza', 'quantity': 1, 'topping': [], 'price': 5}],
                       "1", "test address")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''A delivery person has arrived at address "test address" to delivery your order.
Order number: 1
Order details: [{\'type\': \'custom\', \'size\': 12, \'category\': \'Pizza\', \'quantity\': 1, \'topping\': [], \'price\': 5}]
''')

    def test_get_delivery_asjson(self):
        a = getDeliveryAsJson({'order_number': '1020',
                               'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                              "3", "test address")
        self.assertEqual(getDeliveryAsJson({'order_number': '1020',
                                            'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                                           "3", "test address"),
                         '{"address": "test address", "order number": "3", "order details": [{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]}')

    def test_uberdelivery(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        uberDelivery({'order_number': '1020',
                      'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                     "1", "test address")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''Uber Eats has delivered the following order: 
{"address": "test address", "order number": "1", "order details": [{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]}
''')

    def test_foodoraDelivery(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        foodoraDelivery({'order_number': '1020',
                         'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                        "1", "test address")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), 'Foodora has delivered the following order: \n,0\naddress,test address\norder number,1\norder details,"[{\'type\': \'custom\', \'size\': 12, \'category\': \'Pizza\', \'quantity\': 1, \'topping\': [], \'price\': 5}]"\n\n')



    def test_sendD1(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        sendDelivery("1", {'order_number': '1020',
                         'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'}, "1", "qwe")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''A delivery person has arrived at address "qwe" to delivery your order.
Order number: 1
Order details: [{\'type\': \'custom\', \'size\': 12, \'category\': \'Pizza\', \'quantity\': 1, \'topping\': [], \'price\': 5}]
''')


    def test_sendD2(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        sendDelivery("2", {'order_number': '1020',
                           'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                     "1", "qwe")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''Uber Eats has delivered the following order: 
{"address": "qwe", "order number": "1", "order details": [{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]}
''')

    def test_sendD3(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        sendDelivery("3", {'order_number': '1020',
                           'items': '[{"type": "custom", "size": 12, "category": "Pizza", "quantity": 1, "topping": [], "price": 5}]'},
                     "1", "qwe")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), 'Foodora has delivered the following order: \n,0\naddress,qwe\norder number,1\norder details,"[{\'type\': \'custom\', \'size\': 12, \'category\': \'Pizza\', \'quantity\': 1, \'topping\': [], \'price\': 5}]"\n\n')

    def test_setup_pizzatype(self):
        with mock.patch('builtins.input', return_value="pepperoni"):
            self.assertEqual(setUpPizzaType(), "pepperoni")


    def test_setup_pizzasize(self):
        with mock.patch('builtins.input', return_value="12"):
            self.assertEqual(setUpPizzaSize(), "12")

    def test_updateorder_backend(self):
        self.assertEqual(updateOrderInBackend("1020", []), 200)


    def test_retrieve_orderaslist(self):
        self.assertEqual(retrieveOrderAsList("1051"), [{'type': 'Coke', 'price': 7.5, 'quantity': 3, 'category': 'Drink'}])


    def test_initItemTobeUpdateDrink(self):
        newitem = initItemToBeUpdated({'type': 'Coke', 'price': 7.5, 'quantity': 3, 'category': 'Drink'})
        self.assertEqual(newitem.type, "Coke")
        self.assertEqual(newitem.quantity, 3)
        self.assertEqual(newitem.price, 7.5)

    def test_initItemTobeUpdatePizza(self):
        newitem = initItemToBeUpdated({'type': 'pepperoni', 'price': 30, 'quantity': 3, 'category': 'Pizza', 'size': 12})
        self.assertEqual(newitem.type, "pepperoni")
        self.assertEqual(newitem.quantity, 3)
        self.assertEqual(newitem.price, 30)

    def test_processMainMenuSelection(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        processMainMenuSelection("6")
        sys.stdout = sys.__stdout__
        a = capturedOutput.getvalue()
        self.assertEqual(capturedOutput.getvalue(), '''invalid selection
''')


