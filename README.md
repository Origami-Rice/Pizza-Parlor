# PizzaParlour

a command-line interface then support various features for PizzaParlour

## Installation - PizzaParlour web server (backend)

PizzaParlour web application has already been installed on Heroku clound platform:
https://uoftcsc301a2.herokuapp.com/pizza
No further installation is required
before running the cli-based client application: Main.py, please enter following URL in a browser
https://uoftcsc301a2.herokuapp.com/pizza
You will see a response: "Welcome to Pizza Planet!"
It means the web server is ready for client application to call

## Usage (cli client application)

Prerequisite: pandas package

```bash
    pip install pandas
```

then run the app by

```bash
python3 Main.py
```

## Test

Prerequisite: pytest, pytest-cov, mock packages

```bash
pip install pytest pytest-cov mock
```

Run the unit tests by

```bash
pytest --cov-report term --cov=. tests/unit_tests.py
```

## Pair Programming 
The two features that we pair programmed are the update order feature and the pickup/delivery feature. 

We broke update down into 3 checkpoints. Retrieving the order that was to be updated from the backend, modifying its information, and updating the backend with that modified information. William was the driver for the first and third feature, and Xinyuan was the driver for the second, as well as for the tests. 

We initially broke down the delivery feature into two checkpoints. Retrieving the given order that is to be delivered, and displaying the correct output depending on the delivery option that was chosen. Xinyuan was the driver for the first checkpoint and William was the driver for the second. After realizing that the first checkpoint reused a lot of code from the update order feature (which also requires retrieving the order information so that it can be interacted with), we split the second checkpoint to create a third checkpoint for dealing with the Foodora option (csv), in which Xinyuan became the driver and William acted as the navigator. Xinyuan also acted as the driver for the tests. 

Overall, although the pair programming process was filled with complications due to our drastically different time zones, it was ultimately a positive and beneficial experience. Even though the update and delievery feature were stretched out across several days, the overall time we spent discussing and actually working on the features is likely less than it would have been if we had done each feature separately. By exchanging feedback and discussing implementations, pair programming allowed us to not only write cleaner code, but create solutions that covered all the necessary requirements. 


## Program Design 
Our assignment has a parent class name Item of which Pizza and Drinks are children of. This is because all items share common features like quantity and type which end up needing to be modified at will. Methods like Item's changeType() method demonstrate the strategy design pattern, because how the associated information of the new type is retrieved depends on what kind of item it is. 

A variety of our features, such as update, use the chain of responsibility design pattern. The user's request to update an order is passed to a variety of handlers, beginning with processOrderUpdate(). Requests to add items are handled by updateAnItem(), which passes the request on to a sequence of other handlers which take care of updating individual attributes of the item to be updated.  
