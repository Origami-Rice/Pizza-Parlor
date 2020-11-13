import requests
import json
from Pizza import Pizza
from Order import Order
from Drinks import Drinks
import pandas as pd


def submitOrder(order):
    if order.items != []:
        rsp = requests.post('https://uoftcsc301a2.herokuapp.com/create',
                            json=order.jsonify(), headers=headers)
        if rsp.status_code == 200:
            print(
                "Order submitted successfully order_number is " + rsp.text)
            print("the total cost will be $" + str(order.getTotalPrice()))
            order.order_number = rsp.text
            rsp = requests.post(
                'https://uoftcsc301a2.herokuapp.com/update/' + order.order_number,
                json=order.jsonify(), headers=headers)
            print(
                "Status of updating order " + order.order_number + ": " + str(
                    rsp.status_code))
        else:
            print("submit failed, please try again")
    else:
        print("can't submit empty order")


""" def find_last_order_no():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        new_no = int(last_no) + 1
        f.close()

    with open('order/last_order_no', 'w') as f:
        f.write(str(new_no))
    return str(new_no) """


def print_pizzas(menu):
    print("Pizzas:")
    for pizza in menu["pizza"]["Type"].items():
        print(pizza[0] + " Small: $" + str(pizza[1][1]) + " Medium: $" + str(
            pizza[1][2]) + " Large: $" + str(pizza[1][3]))


def print_drinks(menu):
    print("Drinks:")
    for drink in menu["drinks"].items():
        print(drink[0] + ": $" + str(drink[1]))


def print_toppings(menu):
    print("Toppings:")
    for topping in menu["pizza"]["Toppings"].items():
        print(topping[0] + ": $" + str(topping[1]))


def printItemInfo(item_name, menu):
    for pizza in menu["pizza"]["Type"].items():
        if (pizza[0] == item_name):
            print(item_name + " pizza prices are $" + str(
                pizza[1][1]) + "(small), $" + str(pizza[1][2]) + "(medium), $" +
                  str(pizza[1][3]) + "(large)")
            return
    for drink in menu["drinks"].items():
        if (drink[0] == item_name):
            print(item_name + " price is $" + str(drink[1]))
            return


def printMenu(menu):
    selection = input('''Select an action:
    1. Print the full menu  
    2. Find the prices of an item on the menu
    Make your selection:  ''')
    if (selection == "1"):
        print_pizzas(menu)
        print_drinks(menu)
    elif (selection == "2"):
        item = input('''Enter the name of the item you want to find:''')
        printItemInfo(item, menu)
    # print_toppings(menu)
    return


def setUpType(type):
    if type == "Pizza":
        return setUpPizza()
    else:
        return setUpDrinkType()


def setUpPizzaType():
    pizza = input("Enter pizza name: ")
    while not pizza in menu["pizza"]["Type"].keys():
        print("we don't provide this type of pizza")
        pizza = input("Enter pizza name: ")
    return pizza


def setUpPizzaSize():
    size = input("Enter size (12, 15, 18): ")
    while size not in ["12", "15", "18"]:
        print("please choose the available size")
        size = input("Enter size (12, 15, 18): ")
    return size


def setUpPizza():
    pizza = input(
        "Enter pizza name(enter custom if you want to make your own pizza): ")
    while not pizza in menu["pizza"]["Type"].keys():
        print("we don't provide this type of pizza")
        pizza = input("Enter pizza name: ")
    size = input("Enter size (12, 15, 18): ")
    while size not in ["12", "15", "18"]:
        print("please choose the available size")
        size = input("Enter size (12, 15, 18): ")
    orderPizza = Pizza(pizza, int(size), 1)
    return orderPizza


def userInput(question):
    userinput = input(question)
    return userinput


def setUpDrinkType():
    drink = input("Enter drink's name: ")
    while drink not in menu["drinks"].keys():
        print("we don't have this Drinks, please choose again")
        drink = input("Enter drink's name: ")
    return drink


def setUpTopping():
    additionalToppings = []
    stillAdding = True
    print("Enter 'q' to finish adding toppings")
    while (stillAdding):
        newTopping = input("topping: ")
        while newTopping not in menu["pizza"][
            "Toppings"].keys() and newTopping != "q":
            print("we don't have this topping")
            newTopping = input("topping: ")
        if (newTopping == "q"):
            stillAdding = False
        else:
            additionalToppings.append(newTopping)
    return additionalToppings


def setUpQuantity():
    pizzaQuantity = input("how many would you like: ")
    while float(pizzaQuantity) <= 0 or float(
            pizzaQuantity) % 1 != 0.0:
        print("invalid quantity, please choose again")
        pizzaQuantity = input("how many would you like: ")
    return pizzaQuantity


def processOrderSubmission():
    still_ordering = True
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    # order = Order(find_last_order_no())
    # order number will be generated by https://uoftcsc301a2.herokuapp.com/create
    # and return to client by a respose. Overhere, we just give a fake number
    order = Order("1")
    while (still_ordering):
        selection = input('''Select from the following:
        1. Add an item.
        2. Submit order.  
        Make your selection:''')
        if selection == "1":
            print('''which item do you want: 
                1. Pizza.
                2. Drinks.  ''')
            itemChoice = input("Make your Choice: ")
            if itemChoice == "1":
                orderPizza = setUpPizza()
                additionalToppings = input(
                    "Do you want additional toppings (y/n)?")
                if (additionalToppings == "y"):
                    additionalToppings = setUpTopping()
                    orderPizza.addToppings(additionalToppings)
                    pizzaQuantity = setUpQuantity()
                    orderPizza.changeQuantity(int(pizzaQuantity))
                elif additionalToppings == "n":
                    pizzaQuantity = setUpQuantity()
                    orderPizza.changeQuantity(int(pizzaQuantity))
                print("item added")
                order.addItem(orderPizza)
            elif itemChoice == "2":
                drink = input("Enter drink's name: ")
                while drink not in menu["drinks"].keys():
                    print("we don't have this Drinks, please choose again")
                    drink = input("Enter drink's name: ")
                drinkQuantity = setUpQuantity()
                orderDrink = Drinks(drink, int(drinkQuantity))
                order.addItem(orderDrink)
        elif selection == "2":
            submitOrder(order)
            still_ordering = False
        else:
            print("invalid selection")


def processOrderCancellation():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input('''Enter the number of the order you wish to cancel: ''')
    r = requests.get(base_url + "delete/" + order_no)
    print("The order has been deleted.")


def processOrderUpdate():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input(
        '''Enter the order number of the order you want to update  ''')
    r = requests.get(base_url + 'retrieve/' + order_no)
    json_order_data = json.loads(r.text)
    order = json.loads(json_order_data)
    print(order["order_number"])  # for debugging
    items = json.loads(order["items"])
    print(order["items"])  # for debugging
    counter = 0
    for item in items:
        print("Item #" + str(counter + 1) + ": " + str(item))
        counter = counter + 1
    running = True
    while running:
        item_no = input('''Which item would you like to update? 
        enter quit to exit''')
        if item_no == "quit":
            running = False
            break
        itemUpdated = items[int(item_no) - 1]
        if itemUpdated["category"] == "Pizza":
            newitem = Pizza(itemUpdated["type"], itemUpdated["size"],
                            itemUpdated["quantity"])
        else:
            newitem = Drinks(itemUpdated["type"], itemUpdated["quantity"])
        typeCheck = input('''do you want to change the Type?
                            yes or no''')
        if typeCheck == "yes":
            newType = setUpType(itemUpdated["category"])
            newitem.changeType(newType)
        quantityCheck = input('''do you want to change the Quantity?
                                    yes or no''')
        if quantityCheck == "yes":
            newQuantity = setUpQuantity()
            newitem.changeQuantity(int(newQuantity))
        if itemUpdated["category"] == "Pizza":
            sizeCheck = input('''do you want to change the size?
                yes or no''')
            if sizeCheck == "yes":
                newSize = setUpPizzaSize()
                newitem.changeSize(newSize)
            toppinCheck = input('''do you want to change the Topping?
                                        yes or no''')
            if toppinCheck == "yes":
                newTopping = setUpTopping()
                newitem.changeTopping(newTopping)
        items[int(item_no) - 1] = newitem.__dict__

        jdata = {
            "order_number": order_no,
            "items": []
        }
        jsonItems = json.dumps(items)
        jdata["items"] = jsonItems
        jsondata = json.dumps(jdata)
        jsondata = json.dumps(jsondata)
        r = requests.post(base_url + 'update/' + order_no,
                          data=jsondata, headers=headers)


def normalDelivery(order, order_number, address):
    print('A delivery person has arrived at address "' + address + '" to delivery your order.')
    print('Order number: ' + order_number)
    print('Order details: ' + str(order))


def getDeliveryAsJson(order, order_number, address):
    jdata = {
        "address": address,
        "order number": order_number,
        "order details": []
    }
    order_details = json.loads(order["items"])
    jdata["order details"] = order_details
    return json.dumps(jdata)


def uberDelivery(order, order_number, address):
    print('Uber Eats has delivered the following order: ')
    jsonDelivery = getDeliveryAsJson(order, order_number, address)
    print(str(jsonDelivery))


def foodoraDelivery(order, order_number, address):
    print('Foodora has delivered the following order: ')
    delivery = getDeliveryAsJson(order, order_number, address)
    pandashah = pd.read_json(delivery, typ='series')
    print(pandashah.to_csv())


def sendDelivery(deliverMethod, order, order_number, address):
    order_details = json.loads(order["items"])
    if deliverMethod == "1":
        normalDelivery(order_details, order_number, address)
    elif deliverMethod == "2":
        uberDelivery(order, order_number, address)
    elif deliverMethod == "3":
        foodoraDelivery(order, order_number, address)


def orderDelivery():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input(
        '''Enter the order number of the order you want to call delivery  ''')
    r = requests.get(base_url + 'retrieve/' + order_no)
    json_order_data = json.loads(r.text)
    order = json.loads(json_order_data)
    address = input(
        '''Enter the address you wish to deliver the order to: ''')
    deliveryMethod = input('''Would you like 
    1. Pickup (normal output) 
    2. Uber Eats (json)
    3. Foodora (csv)
    Enter a number: ''')
    sendDelivery(deliveryMethod, order, order_no, address)


if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    # base_url = 'http://127.0.0.1:5000/'
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    '''r = requests.post(base_url + 'create_menu', data=json.dumps(menu),
                       headers=headers)
    r = requests.get(base_url + 'retrieve/' + 'Menu')
    print("Response body: " + r.text) '''

    running = True
    while running:
        print('''Select a number for the action you would like to do: 
        1. Access the menu  
        2. Submit an order
        3. Update an existing order 
        4. Cancel an order
        5. Call for delivery/pickup. 
        6. Quit 
        ''')
        selection = input("Make your selection: ")

        if selection == "1":
            printMenu(menu)
        elif selection == "2":
            processOrderSubmission()
        elif selection == "3":
            processOrderUpdate()
        elif selection == "4":
            processOrderCancellation()
        elif selection == "5":
            orderDelivery()
        elif selection == "6":
            running = False
        else:
            print("invalid selection")
