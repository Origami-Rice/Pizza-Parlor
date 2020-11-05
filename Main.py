import requests
import json
from Pizza import Pizza
from Order import Order
from Drinks import Drinks


def submitOrder(order):
    request = requests.post('https://uoftcsc301a2.herokuapp.com/create',
                            json=order.jsonify(), headers=headers)
    if request.status_code == 200:
        print(
            "Order submitted successfully order_number is " + order.order_number)

    else:
        print("submit failed, please try again")


def find_last_order_no():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        new_no = int(last_no) + 1
        f.close()

    with open('order/last_order_no', 'w') as f:
        f.write(str(new_no))
    return str(new_no)


def processOrderSubmission():
    still_ordering = True
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    print('''Select a number for the action you would like to do: 
    1. Add an item.
    2. Submit order.  ''')
    order = Order(find_last_order_no())
    while (still_ordering):
        selection = input("Make your selection: ")
        if selection == "1":
            pizza = input("Enter pizza name: ")
            while not pizza in menu["pizza"]["Type"].keys():
                print("we don't provide this type of pizza")
                pizza = input("Enter pizza name: ")
            size = input("Enter size (12, 15, 18): ")
            while size not in ["12", "15", "18"]:
                print("please choose the available size")
                size = input("Enter size (12, 15, 18): ")
            orderPizza = Pizza(pizza, int(size))
            additionalToppings = input("Do you want additional toppings (y/n)?")
            if (additionalToppings == "y"):
                additionalToppings = []
                stillAdding = True
                print("Enter 'q' to finish adding toppings")
                while (stillAdding):
                    newTopping = input("topping: ")
                    if (newTopping == "q"):
                        stillAdding = False
                    else:
                        additionalToppings.append(newTopping)
                orderPizza.addToppings(additionalToppings)
            order.addItem(orderPizza)
        elif selection == "2":
            submitOrder(order)
            still_ordering = False
        else:
            print("invalid selection")


if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    # base_url = 'http://127.0.0.1:5000/'
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    r = requests.post(base_url + 'create_menu', data=json.dumps(menu),
                      headers=headers)
    r = requests.get(base_url + 'retrieve/' + 'Menu')
    print("Response body: " + r.text)

    while True:
        print('''Select a number for the action you would like to do: 
        1. Submit an order
        2. 
        3. 
        ''')
        selection = input("Make your selection: ")

        if selection == "1":
            processOrderSubmission()
        else:
            print("invalid selection")
