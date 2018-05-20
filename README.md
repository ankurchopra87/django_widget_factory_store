
Widget Factory Store
=====

Widget Factory Store is a Django project that implements a web store. The
Front-End is written in ReactJS and the backend-end REST API and administration
is written in Django/Python.

The source for the Front-End is located at [here](https://github.com/ankurchopra87/react_widget_factory_store).  

Installation
-----------

This is a Django application which uses Python 3. You will need to install
Python3 before proceeding further.

Python 3 - https://www.python.org/download/releases/3.0/

In the project dir run the following commands. 

pip3 install --user virtualenv

python3 -m virtualenv .env

source .env/bin/activate

pip3 install -r requirements.txt

Start the App
-----------

After installation, use the following command to start the app

python manage.py runserver 

This will start ths development server at http://127.0.0.1:8000/

Administration
-----------

The administration console is located at http://127.0.0.1:8000/admin/

user: admin

pass: facetwealth

Testing 
-----------

Use the following command to test the app

python manage.py test

Known Issues & Opportunities for Improvement
-----------

1) Front End doesn't cache cart items. The cart data is lost on refresh.
2) Cart doesn't add to quantity when a new sku is added. It adds it as a new item. 
3) The Front-end and back-end interfaces are de-coupled.
4) Search hits the backend on every change.
5) Admin pages can be refined a lot more. 
6) Order confirmation page is not styled.
7) The UI needs some CSS work.
