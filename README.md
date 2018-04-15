# Mini-Swiggy App

The App has bare minimum features to create, update, delete a restaurant. Create driver, save the location of driver and update it on real time basis. Creating customer account, ordering menu and placing order of amount x to a restaurant.
Once an order comes to a restaurant, it also gives you a list of 10 drivers within 4 km of the particular restaurant.

## Getting Started

You need to have PostgreSQL and ElasticSearch installed in your machine. The instructions can be found on their respective websites. Once these are installed follow the below steps to setup the project:

```
$ virtualenv -p python3 newenv
$ source newenv/bin/activate
$ pip3 install -r requirements.txt
```
run migrations
```
python manage.py migrate
```

And start the server with follwoing command

```
$ python manage.py runserver 8000
```
