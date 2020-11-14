import requests
import json
from Pizza import Pizza
from Order import Order
from Drinks import Drinks
#import pandas as pd

# Retrieves the menu from the Menu.json file and returns it as a dictionary 
def retrieveMenu():
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    return menu

# Takes in an Order object and makes an api call to add it to the back end 
def submitOrder(order):
    if order.items != []:
        headers = {'Content-Type': 'application/json'}
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
            return 200
        else:
            print("submit failed, please try again")
            return 404
    else:
        print("can't submit empty order")
        return "can't submit empty order"

# Prints all the pizza types and their price for each size
def print_pizzas():
    menu = retrieveMenu()
    print("Pizzas:")
    for pizza in menu["pizza"]["Type"].items():
        print(pizza[0] + " Small: $" + str(pizza[1][1]) + " Medium: $" + str(
            pizza[1][2]) + " Large: $" + str(pizza[1][3]))

# Prints all the drink types and their associated prices 
def print_drinks():
    menu = retrieveMenu()
    print("Drinks:")
    for drink in menu["drinks"].items():
        print(drink[0] + ": $" + str(drink[1]))

# Prints all the toppings and their associated prices 
def print_toppings():
    menu = retrieveMenu()
    print("Toppings:")
    for topping in menu["pizza"]["Toppings"].items():
        print(topping[0] + ": $" + str(topping[1]))

# Prints the price of the item with the type "item_name"
def printItemInfo(item_name):
    menu = retrieveMenu()
    for pizza in menu["pizza"]["Type"].items():
        if (pizza[0] == item_name):
            print(item_name + " pizza prices are $" + str(
                pizza[1][1]) + " (small), $" + str(pizza[1][2]) + " (medium), $" +
                str(pizza[1][3]) + " (large)")
            return
    for drink in menu["drinks"].items():
        if (drink[0] == item_name):
            print(item_name + " price is $" + str(drink[1]))
            return

# Prints the full menu or prompts for the item name of a specific item whose price(s) is to be printed 
def printMenuHelper(selection):
    if (selection == "1"):
        print("--------------------------Menu--------------------------")
        print_pizzas()
        print_drinks()
    elif (selection == "2"):
        item = input('''Enter the name of the item you want to find:''')
        printItemInfo(item)

# Prompts for the menu functionality the user wants, and passes that choice to printMenuHelper()
# which handles the logic. 
def printMenu():
    selection = input('''Select an action:
    1. Print the full menu  
    2. Find the prices of an item on the menu
    Make your selection: ''')
    printMenuHelper(selection)

# Returns a Pizza object or Drink object depending on the requested type 
def setUpType(type):
    if type == "Pizza":
        return setUpPizza()
    else:
        return setUpDrinkType()

# Prompts user for a pizza type until they add one which is in the menu 
def setUpPizzaType():
    menu = retrieveMenu()
    pizza = input("Enter pizza name (enter custom if you want to make your own pizza): ")
    while not pizza in menu["pizza"]["Type"].keys():
        print("we don't provide this type of pizza")
        pizza = input("Enter pizza name: ")
    return pizza

# Prompts user for a pizza size until they add one which is valid 
def setUpPizzaSize():
    size = input("Enter size (12, 15, 18): ")
    while size not in ["12", "15", "18"]:
        print("Please choose an available size.")
        size = input("Enter size (12, 15, 18): ")
    return size

# Creates a pizza based on user input
def setUpPizza():
    pizza = setUpPizzaType()
    size = setUpPizzaSize()
    newItem = Pizza(pizza, int(size), 1)
    return newItem

# Prompts user for a drink type until they enter one which is valid 
def setUpDrinkType():
    drink = input("Enter drink's name: ")
    menu = retrieveMenu()
    while drink not in menu["drinks"].keys():
        print("We don't have this drink. Please choose again")
        drink = input("Enter drink's name: ")
    return drink

# Prompts user for the toppings they wish to add to the pizza until they enter "q" to exit. 
# Returns the list of additional toppings 
def setUpTopping():
    additionalToppings = []
    stillAdding = True
    print("Enter 'q' to finish adding toppings.")
    while (stillAdding):
        newTopping = input("Topping: ")
        while newTopping not in menu["pizza"][
                "Toppings"].keys() and newTopping != "q":
            print("We don't have this topping.")
            newTopping = input("Topping: ")
        if (newTopping == "q"):
            stillAdding = False
        else:
            additionalToppings.append(newTopping)
    return additionalToppings

# Prompts user for a positive integer
def setUpQuantity():
    quantity = input("Enter how many you would like: ")
    while float(quantity) <= 0 or float(
            quantity) % 1 != 0.0:
        print("invalid quantity, please choose again")
        quantity = input("Enter how many would you like: ")
    return quantity

# Sets up a pizza based on user input and adds it to the passed in order. 
def add_pizza_to_order(order):
    newItem = setUpPizza()
    additionalToppings = input(
        "Do you want additional toppings (y/n)? ")
    if (additionalToppings == "y"):
        additionalToppings = setUpTopping()
        newItem.addToppings(additionalToppings)
    quantity = setUpQuantity()
    newItem.changeQuantity(int(quantity))
    print("Item added.")
    order.addItem(newItem)

# Creates a drink based on user input and adds it to the passed in order. 
def add_drink_to_order(order):
    menu = retrieveMenu()
    drink = input("Enter drink's name: ")
    while drink not in menu["drinks"].keys():
        print("we don't have this Drinks. Please choose again.")
        drink = input("Enter drink's name: ")
    drinkQuantity = setUpQuantity()
    newItem = Drinks(drink, int(drinkQuantity))
    order.addItem(newItem)

# Prompts the user for the type of item they wish to add and adds it to the passed in order. 
def handle_add_item_request(order):
    print('''which item do you want: 
                1. Pizza.
                2. Drinks.  ''')
    itemChoice = input("Make your Choice: ")
    if itemChoice == "1":
        add_pizza_to_order(order)
    elif itemChoice == "2":
        add_drink_to_order(order)

# Handles user input for the creation of the order, allowing the user to continuously add items,
# or, when they decide to submit their order, submits it to the back end. 
def processOrderSubmission():
    still_ordering = True
    # order = Order(find_last_order_no())
    # order number will be generated by https://uoftcsc301a2.herokuapp.com/create
    # and return to client by a respose. Overhere, we just give a fake number
    order = Order("1")
    while (still_ordering):
        selection = input('''Select from the following:
        1. Add an item.
        2. Submit order.  
        Make your selection: ''')
        if selection == "1":
            handle_add_item_request(order)
        elif selection == "2":
            submitOrder(order)
            still_ordering = False
        else:
            print("invalid selection")

# Removes the order with the order number sepcified by the user from the back end 
def processOrderCancellation():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input('''Enter the number of the order you wish to cancel: ''')
    r = requests.get(base_url + "delete/" + order_no)
    print("The order has been deleted.")

# Creates and returns a copy of the passed in item 
def initItemToBeUpdated(item):
    if item["category"] == "Pizza":
        newitem = Pizza(item["type"], item["size"],
                        item["quantity"])
    else:
        newitem = Drinks(item["type"], item["quantity"])
    return newitem

# Prompts user for whether they wish to change an item's type (within the same category.
# Drink -> Drink and Pizza -> Pizza)
def handleItemTypeUpdate(item, newitem):
    typeCheck = input('''Do you want to change the Type?
                        yes or no: ''')
    if typeCheck == "yes":
        newType = setUpType(item["category"])
        newitem.changeType(newType)

# Prompts user for whether they wish to update an item's quantity. 
def handleQuantityUpdate(newitem):
    quantityCheck = input('''Do you want to change the Quantity?
                                yes or no: ''')
    if quantityCheck == "yes":
        newQuantity = setUpQuantity()
        newitem.changeQuantity(int(newQuantity))

# Prompts use for whether they wish to update a pizza item's size.
def handleSizeUpdate(newitem):
    sizeCheck = input('''Do you want to change the size?
            yes or no: ''')
    if sizeCheck == "yes":
        newSize = setUpPizzaSize()
        newitem.changeSize(newSize)

# Prompts user for whether they wish to add toppings to a pizza item
def handleToppingCheck(newitem):
    toppinCheck = input('''Do you want to change the Topping?
                                    yes or no: ''')
    if toppinCheck == "yes":
        newTopping = setUpTopping()
        newitem.changeTopping(newTopping)

# Prompts for and handles all possible modification to a given item in a list of items. 
def updateAnItem(items, item_no):
    item = items[int(item_no) - 1]
    newitem = initItemToBeUpdated(item)

    handleItemTypeUpdate(item, newitem)
    handleQuantityUpdate(newitem)
    if item["category"] == "Pizza":
        handleSizeUpdate(newitem)
        handleToppingCheck(newitem)
    items[int(item_no) - 1] = newitem.__dict__

# Creates a new order with the passed in order_no and list of items and makes an api call to
# have it replace the original order with this order number in the back end. 
def updateOrderInBackend(order_no, items):
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
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

# Retrieves the order with the given order number from the back end and returns its items
# as a python list 
def retrieveOrderAsList(order_no):
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    r = requests.get(base_url + 'retrieve/' + order_no)
    json_order_data = json.loads(r.text)
    order = json.loads(json_order_data)
    items = json.loads(order["items"])
    return items

# Prompts the user for the order number of the order they wish to update as 
# well as the items they wish to update.
def processOrderUpdate():
    order_no = input(
        '''Enter the order number of the order you want to update  ''')
    items = retrieveOrderAsList(order_no)

    counter = 0
    for item in items:
        print("Item #" + str(counter + 1) + ": " + str(item))
        counter = counter + 1
    running = True
    while running:
        item_no = input('''Which item would you like to update? 
        Enter an item number, or enter "quit" to exit: ''')
        if item_no == "quit":
            running = False
        else:
            updateAnItem(items, item_no)
            updateOrderInBackend(order_no, items)

# Delivers an order "normally", wherein the order information is displayed in plain english, 
# with the order details as a python list.  
def normalDelivery(order, order_number, address):
    print('A delivery person has arrived at address "' +
          address + '" to delivery your order.')
    print('Order number: ' + order_number)
    print('Order details: ' + str(order))

# Takes in the order to be delievered, its order number, and address, and returns
# a JSON object with all the delivery information 
def getDeliveryAsJson(order, order_number, address):
    jdata = {
        "address": address,
        "order number": order_number,
        "order details": []
    }
    order_details = json.loads(order["items"])
    jdata["order details"] = order_details
    return json.dumps(jdata)

# The Uber Eats delivery which prints the order formatted as JSON data. 
def uberDelivery(order, order_number, address):
    print('Uber Eats has delivered the following order: ')
    jsonDelivery = getDeliveryAsJson(order, order_number, address)
    print(str(jsonDelivery))

# The Foodora delivery, which prints the order formatted as csv 
def foodoraDelivery(order, order_number, address):
    print('Foodora has delivered the following order: ')
    delivery = getDeliveryAsJson(order, order_number, address)
    pandashah = pd.read_json(delivery, typ='series')
    print(pandashah.to_csv())

# Performs a normal delivery, an Uber Eats delivery, or a Foodora delivery depending on 
# the passed in deliverMethod selection and using the passed in details of the order. 
def sendDelivery(deliverMethod, order, order_number, address):
    order_details = json.loads(order["items"])
    if deliverMethod == "1":
        normalDelivery(order_details, order_number, address)
    elif deliverMethod == "2":
        uberDelivery(order, order_number, address)
    elif deliverMethod == "3":
        foodoraDelivery(order, order_number, address)

# Retrieves an order from the back end and delivers it according to the chosen delivery method. 
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

# Prints out all the available functionalities a user can perform
def printMainMenuOptions():
    print('''Select a number for the action you would like to do: 
        1. Access the menu  
        2. Submit an order
        3. Update an existing order 
        4. Cancel an order
        5. Call for delivery/pickup. 
        6. Quit 
        ''')

# Executes the according functionality depending on the user's selection 
def processMainMenuSelection(selection):
    if selection == "1":
        printMenu()
    elif selection == "2":
        processOrderSubmission()
    elif selection == "3":
        processOrderUpdate()
    elif selection == "4":
        processOrderCancellation()
    elif selection == "5":
        orderDelivery()
    else:
        print("invalid selection")


if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    menu = retrieveMenu()

    running = True
    while running:
        printMainMenuOptions()
        selection = input("Make your selection: ")
        if selection == "6":
            running = False
        else:
            processMainMenuSelection(selection)
