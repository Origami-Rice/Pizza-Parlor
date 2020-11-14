from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
app = Flask(__name__)
CORS(app)

#
# This function to retrieve last order number
# and return a new order number


def find_last_order_no():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        new_no = int(last_no) + 1
        f.close()

    with open('order/last_order_no', 'w') as f:
        f.write(str(new_no))
    return str(new_no)

# part of starter code


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


""" @app.route('/create_menu', methods=['POST', 'GET'])
def create_menu():
    jsonData = request.get_json()
    order_file_name = 'order/' + 'Menu.json'
    with open(order_file_name, 'w') as outfile:
        json.dump(jsonData, outfile)
    return jsonData  """

# Persist a new order on backend data storage
# in this project, it's just stored under /order
# directory as a system file


@app.route('/create', methods=['POST', 'GET'])
def create_order():
    new_order_no = find_last_order_no()
    jsonData = request.get_json()
    order_file_name = 'order/' + new_order_no+'.json'
    with open(order_file_name, 'w') as outfile:
        json.dump(jsonData, outfile)
    return new_order_no

# Retrieve an order from backend data storage by an order number


@app.route('/retrieve/<string:order_no>', methods=['GET'])
def retrieve_order(order_no):
    order_file_name = 'order/' + order_no + '.json'
    if os.path.exists(order_file_name):
        with open(order_file_name) as f:
            order = json.load(f)
            f.close()
        return jsonify(order)
    else:
        return "ERROR: order - " + order_no + " not found!"

# Delete an order from backend data storage by an order number


@app.route('/delete/<string:order_no>', methods=['GET'])
def delete_order(order_no):
    order_file_name = 'order/' + order_no + '.json'
    if os.path.exists(order_file_name):
        os.remove(order_file_name)
        return order_no
    else:
        # although order file is not found, it's still treated as
        # delete successfully
        return order_no


@app.route('/update/<string:order_no>', methods=['POST', 'GET'])
def update_order(order_no):
    order_file_name = 'order/' + order_no + '.json'
    if os.path.exists(order_file_name):
        jsonData = request.get_json()
        with open(order_file_name, 'w') as outfile:
            json.dump(jsonData, outfile)
            outfile.close
        return order_no
    else:
        return "ERROR: order - " + order_no + " not found!"


if __name__ == "__main__":
    app.run()
