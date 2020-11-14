import requests
import json
from Pizza import Pizza
from Order import Order
from Drinks import Drinks
#import pandas as pd

# Retrieves the menu from the Menu.json file and returns it as a dictionary
def retrieve_menu():
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    return menu

# Takes in an Order object and makes an api call to add it to the back end
def submit_order(order):
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
    menu = retrieve_menu()
    print("Pizzas:")
    for pizza in menu["pizza"]["Type"].items():
        print(pizza[0] + " Small: $" + str(pizza[1][1]) + " Medium: $" + str(
            pizza[1][2]) + " Large: $" + str(pizza[1][3]))

# Prints all the drink types and their associated prices
def print_drinks():
    menu = retrieve_menu()
    print("Drinks:")
    for drink in menu["drinks"].items():
        print(drink[0] + ": $" + str(drink[1]))

# Prints all the toppings and their associated prices
def print_toppings():
    menu = retrieve_menu()
    print("Toppings:")
    for topping in menu["pizza"]["Toppings"].items():
        print(topping[0] + ": $" + str(topping[1]))

# Prints the price of the item with the type "item_name"
def print_item_info(item_name):
    menu = retrieve_menu()
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
def print_menu_helper(selection):
    if (selection == "1"):
        print("--------------------------Menu--------------------------")
        print_pizzas()
        print_drinks()
    elif (selection == "2"):
        item = input('''Enter the name of the item you want to find:''')
        print_item_info(item)

# Prompts for the menu functionality the user wants, and passes that choice to printMenuHelper()
# which handles the logic.
def print_menu():
    selection = input('''Select an action:
    1. Print the full menu  
    2. Find the prices of an item on the menu
    Make your selection: ''')
    print_menu_helper(selection)

# Returns a Pizza object or Drink object depending on the requested type
def setup_type(type):
    if type == "Pizza":
        return setup_pizza()
    else:
        return setup_drink_type()

# Prompts user for a pizza type until they add one which is in the menu
def setup_pizza_type():
    menu = retrieve_menu()
    pizza = input("Enter pizza name (enter custom if you want to make your own pizza): ")
    while not pizza in menu["pizza"]["Type"].keys():
        print("we don't provide this type of pizza")
        pizza = input("Enter pizza name: ")
    return pizza

# Prompts user for a pizza size until they add one which is valid
def setup_pizza_size():
    size = input("Enter size (12, 15, 18): ")
    while size not in ["12", "15", "18"]:
        print("Please choose an available size.")
        size = input("Enter size (12, 15, 18): ")
    return size

# Creates a pizza based on user input
def setup_pizza():
    pizza = setup_pizza_type()
    size = setup_pizza_size()
    newItem = Pizza(pizza, int(size), 1)
    return newItem

# Prompts user for a drink type until they enter one which is valid
def setup_drink_type():
    drink = input("Enter drink's name: ")
    menu = retrieve_menu()
    while drink not in menu["drinks"].keys():
        print("We don't have this drink. Please choose again")
        drink = input("Enter drink's name: ")
    return drink

# Prompts user for the toppings they wish to add to the pizza until they enter "q" to exit.
# Returns the list of additional toppings
def setup_topping():
    menu = retrieve_menu()
    additional_toppings = []
    still_adding = True
    print("Enter 'q' to finish adding toppings.")
    while (still_adding):
        new_topping = input("Topping: ")
        while new_topping not in menu["pizza"][
                "Toppings"].keys() and new_topping != "q":
            print("We don't have this topping.")
            new_topping = input("Topping: ")
        if (new_topping == "q"):
            still_adding = False
        else:
            additional_toppings.append(new_topping)
    return additional_toppings

# Prompts user for a positive integer
def setup_quantity():
    quantity = input("Enter how many you would like: ")
    while float(quantity) <= 0 or float(
            quantity) % 1 != 0.0:
        print("invalid quantity, please choose again")
        quantity = input("Enter how many would you like: ")
    return quantity

# Sets up a pizza based on user input and adds it to the passed in order.
def add_pizza_to_order(order):
    new_item = setup_pizza()
    additionalToppings = input(
        "Do you want additional toppings (y/n)? ")
    if (additionalToppings == "y"):
        additionalToppings = setup_topping()
        new_item.addToppings(additionalToppings)
    quantity = setup_quantity()
    new_item.changeQuantity(int(quantity))
    print("Item added.")
    order.addItem(new_item)

# Creates a drink based on user input and adds it to the passed in order.
def add_drink_to_order(order):
    menu = retrieve_menu()
    drink = input("Enter drink's name: ")
    while drink not in menu["drinks"].keys():
        print("we don't have this Drinks. Please choose again.")
        drink = input("Enter drink's name: ")
    drink_quantity = setup_quantity()
    newItem = Drinks(drink, int(drink_quantity))
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
def process_order_submission():
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
            submit_order(order)
            still_ordering = False
        else:
            print("invalid selection")

# Removes the order with the order number sepcified by the user from the back end
def process_order_cancellation():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input('''Enter the number of the order you wish to cancel: ''')
    r = requests.get(base_url + "delete/" + order_no)
    print("The order has been deleted.")

# Creates and returns a copy of the passed in item
def init_item_to_be_updated(item):
    if item["category"] == "Pizza":
        new_item = Pizza(item["type"], item["size"],
                        item["quantity"])
    else:
        new_item = Drinks(item["type"], item["quantity"])
    return new_item

# Prompts user for whether they wish to change an item's type (within the same category.
# Drink -> Drink and Pizza -> Pizza)
def handle_item_type_update(item, new_item):
    typeCheck = input('''Do you want to change the Type?
                        yes or no: ''')
    if typeCheck == "yes":
        new_type = setup_type(item["category"])
        new_item.changeType(new_type)

# Prompts user for whether they wish to update an item's quantity.
def handle_quantity_update(new_item):
    quantity_check = input('''Do you want to change the Quantity?
                                yes or no: ''')
    if quantity_check == "yes":
        new_quantity = setup_quantity()
        new_item.changeQuantity(int(new_quantity))

# Prompts use for whether they wish to update a pizza item's size.
def handle_size_update(new_item):
    size_check = input('''Do you want to change the size?
            yes or no: ''')
    if size_check == "yes":
        new_size = setup_pizza_size()
        new_item.changeSize(new_size)

# Prompts user for whether they wish to add toppings to a pizza item
def handle_topping_check(new_item):
    topping_check = input('''Do you want to change the Topping?
                                    yes or no: ''')
    if topping_check == "yes":
        new_topping = setup_topping()
        new_item.changeTopping(new_topping)

# Prompts for and handles all possible modification to a given item in a list of items.
def update_an_item(items, item_no):
    item = items[int(item_no) - 1]
    new_item = init_item_to_be_updated(item)

    handle_item_type_update(item, new_item)
    handle_quantity_update(new_item)
    if item["category"] == "Pizza":
        handle_size_update(new_item)
        handle_topping_check(new_item)
    items[int(item_no) - 1] = new_item.__dict__

# Creates a new order with the passed in order_no and list of items and makes an api call to
# have it replace the original order with this order number in the back end.
def update_order_in_backend(order_no, items):
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    jdata = {
        "order_number": order_no,
        "items": []
    }
    json_items = json.dumps(items)
    jdata["items"] = json_items
    json_data = json.dumps(jdata)
    json_data = json.dumps(json_data)
    r = requests.post(base_url + 'update/' + order_no,
                      data=json_data, headers=headers)

# Retrieves the order with the given order number from the back end and returns its items
# as a python list
def retrieve_order_as_list(order_no):
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    r = requests.get(base_url + 'retrieve/' + order_no)
    json_order_data = json.loads(r.text)
    order = json.loads(json_order_data)
    items = json.loads(order["items"])
    return items

# Prompts the user for the order number of the order they wish to update as
# well as the items they wish to update.
def process_order_update():
    order_no = input(
        '''Enter the order number of the order you want to update  ''')
    items = retrieve_order_as_list(order_no)

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
            update_an_item(items, item_no)
            update_order_in_backend(order_no, items)

# Delivers an order "normally", wherein the order information is displayed in plain english,
# with the order details as a python list.
def normal_delivery(order, order_number, address):
    print('A delivery person has arrived at address "' +
          address + '" to delivery your order.')
    print('Order number: ' + order_number)
    print('Order details: ' + str(order))

# Takes in the order to be delievered, its order number, and address, and returns
# a JSON object with all the delivery information
def get_delivery_as_json(order, order_number, address):
    jdata = {
        "address": address,
        "order number": order_number,
        "order details": []
    }
    order_details = json.loads(order["items"])
    jdata["order details"] = order_details
    return json.dumps(jdata)

# The Uber Eats delivery which prints the order formatted as JSON data.
def uber_delivery(order, order_number, address):
    print('Uber Eats has delivered the following order: ')
    jsonDelivery = get_delivery_as_json(order, order_number, address)
    print(str(jsonDelivery))

# The Foodora delivery, which prints the order formatted as csv
def foodora_delivery(order, order_number, address):
    print('Foodora has delivered the following order: ')
    delivery = get_delivery_as_json(order, order_number, address)
    pandashah = pd.read_json(delivery, typ='series')
    print(pandashah.to_csv())

# Performs a normal delivery, an Uber Eats delivery, or a Foodora delivery depending on
# the passed in deliverMethod selection and using the passed in details of the order.
def send_delivery(deliver_method, order, order_number, address):
    order_details = json.loads(order["items"])
    if deliver_method == "1":
        normal_delivery(order_details, order_number, address)
    elif deliver_method == "2":
        uber_delivery(order, order_number, address)
    elif deliver_method == "3":
        foodora_delivery(order, order_number, address)

# Retrieves an order from the back end and delivers it according to the chosen delivery method.
def order_delivery():
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    order_no = input(
        '''Enter the order number of the order you want to call delivery  ''')
    r = requests.get(base_url + 'retrieve/' + order_no)
    json_order_data = json.loads(r.text)
    order = json.loads(json_order_data)
    address = input(
        '''Enter the address you wish to deliver the order to: ''')
    delivery_method = input('''Would you like 
    1. Pickup (normal output) 
    2. Uber Eats (json)
    3. Foodora (csv)
    Enter a number: ''')
    send_delivery(delivery_method, order, order_no, address)

# Prints out all the available functionalities a user can perform
def print_main_menu_options():
    print('''Select a number for the action you would like to do: 
        1. Access the menu  
        2. Submit an order
        3. Update an existing order 
        4. Cancel an order
        5. Call for delivery/pickup. 
        6. Quit 
        ''')

# Executes the according functionality depending on the user's selection
def process_main_menu_selection(selection):
    if selection == "1":
        print_menu()
    elif selection == "2":
        process_order_submission()
    elif selection == "3":
        process_order_update()
    elif selection == "4":
        process_order_cancellation()
    elif selection == "5":
        order_delivery()
    else:
        print("invalid selection")


if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    menu = retrieve_menu()

    running = True
    while running:
        print_main_menu_options()
        selection = input("Make your selection: ")
        if selection == "6":
            running = False
        else:
            process_main_menu_selection(selection)
