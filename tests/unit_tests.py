from PizzaParlour import app
import json


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
        sent = {"order_number": "1", "items": [{"type": "pepperoni", "size": 12, "topping": [
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
    response = app.test_client().get('/retrieve/'+last_no)
    print("order_no: " + last_no)
    assert response.status_code == 200


def test_update():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        f.close()
    with app.test_client() as client:
        # send data as POST form to endpoint
        sent = {"order_number": "1", "items": [{"type": "pepperoni", "size": 12, "topping": [
            "olives", "tomatoes", "olives", "tomatoes"], "price": 14}]}
        response = client.post(
            '/update/'+last_no,
            data=sent
        )
    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == last_no


def test_delete():
    with open('order/last_order_no', 'r') as f:
        last_no = f.readline()
        f.close()
    response = app.test_client().get('/delete/'+last_no)
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
        sent = {"order_number": "1", "items": [{"type": "pepperoni", "size": 12, "topping": [
            "olives", "tomatoes", "olives", "tomatoes"], "price": 14}]}
        response = client.post(
            '/update/1000',
            data=sent
        )
    assert response.status_code == 200
    print(response.data.decode('utf-8'))
    assert response.data.decode('utf-8') == "ERROR: order - 1000 not found!"
