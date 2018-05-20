=====
Widget Factory Store
=====

Widget Factory Store is a Django project that implements a web store. The
Front-End is written in ReactJS and the backend-end REST API and administration
is written in Django/Python.

Installation
-----------

This is a Django application which uses Python 3. You will need to install
Python3 before proceeding furthon

Python 3 - https://www.python.org/download/releases/3.0/

in the project dir run the following commands. 

pip install --user virtualenv
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt

Start the App
-----------

After installation, use the following command to start the app

python manage.py runserver 

This will start ths development server at http://127.0.0.1:8000/

Testing 
-----------

Use the following command to test the app

python manage.py test

Administration
-----------

The administration console is located at http://127.0.0.1:8000/admin/

user: admin
pass: facetwealth

Known Issues & Oppotunities for Improvement
-----------

1) Front end doesnt cache cart items. The cart data is lost on refresh
2) UI needs some CSS work.
3) Cart doesn't add to quantity when a new sku is added. It adds it as a new item. 
4) Order confirmation page is not styled.
5) The Front-end and back-end interfaces are de-coupled.
6) Search hits the backend on every change.
7) Admin pages can be refined a lot more. 
many more ...