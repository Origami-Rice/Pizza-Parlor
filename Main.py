import requests 
import json

def processOrderSubmission():
    still_ordering = True 
    print('''Select a number for the action you would like to do: 
    1. Add an item.
    2. Submit order.  ''') 
    while(still_ordering):
        selection = input("Make your selection: ")
        if selection == "1":
            pizza = input("Enter pizza name: ")
            size = input("Enter size (Small, Medium, Large): ")
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
        elif selection == "2":
            still_ordering = False 
        else:
            print("invalid selection")

if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://uoftcsc301a2.herokuapp.com/'
    #base_url = 'http://127.0.0.1:5000/' 
    with open('order/Menu.json') as f:
        menu = json.load(f)
        f.close
    r = requests.post(base_url + 'create_menu', data=json.dumps(menu), headers=headers)
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



