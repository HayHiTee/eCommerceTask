# Ecommerce Task Api

This project is the solution to a simple ecommerce task api

## Getting Started

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. See deployment for notes
on how to deploy the project on a live system

## Prerequisites
* Python 3.*



## Installation
1. Clone a copy of this app
2. Setup your python environment (Preferably set up a virtual environment)
3. Run `pip install -r requirements.txt`
4. A copy of the django and other packages would be install
5. Then run database migration `python manage.py migrate`
6. To start the application run `python manage.py runserver`
7. Below are the endpoints that are associated with this applications API


## Endpoints
1. for category => '/categories' and Allowed methods are GET and POST
2. for products => '/products' and allowed methods are GET and POST with option to filter by category in the query params e.g '/products?category=<category_name>'
3. for product detail => '/products/<pk>' and allowed methods are GET, PUT, PATCH and DELETE
4. for discount => '/discounts' and allowed methods are GET and POST. Also discount_unit field only takes either 'percent' or 'fixed'