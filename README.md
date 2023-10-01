# Digital Bank

ApiRest built with Django Rest Framework 3.14.0 and Django 4.2.5
# ERD
<p align="center">
           <img src="https://lucid.app/publicSegments/view/f56589fc-8908-4c80-9de7-cb3e682dfdb9/image.png"/>
</p>

# Getting Started
1) Create a new directory.
2) Open your favourite IDE and then open your directory. 
3) Open the terminal in working directory:
4) Clone this repository:
```
           git clone https://github.com/jewelazo/digital_bank.git
```
5) Create a virtual environmnent:
```
            python -m venv .venv
```
6) Activate the virtual environment:
```
            .\.venv\Scripts\activate
```
7) Create your postgresql database and add its values in your .env file, please follow .env.example as template:

8) Go to project folder and install libraries:
```
            (env) pip install -r requirements.txt
```
9) Run Migrations:
```
            (env) python manage.py migrate
```
10) Start running the server with this command:
```
            (env) python manage.py runserver
```
11) Explore API Documentation to review endpoints and remember add your token in this format "Bearer {{your_token}}:
```
            http://127.0.0.1:8000/apidocs/
```
12) Also is available django admin panel, so make sure to create a superuser and then go to /admin:

```
           python manage.py createsuperuser
           http://127.0.0.1:8000/admin
```
  
