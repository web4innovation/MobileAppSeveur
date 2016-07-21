# backend 
This repo will contain all the code to implement a RESTful web server.
It will also contain all the necessary instructions to setup and run the web server on a new machine.
the server can run on linux, mac or windows. The only requirement is to have python3.4 installed.

The web server is developed using python3.4 and the flask library. 
This work was inspired by http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

# Installation
- clone the git repo ```git clone https://github.com/lwiss/web4innovation_mobile.git```.
- go to backend directory ```cd web4innovation_mobile/backend```
- ceate a virtual environment in the same directory and name it flask: ```ython3 -m venv flask```
- install the following dependencies to the freshly prepared venv (execute the following commands one by one):
```
    flask/bin/pip install flask
    flask/bin/pip install flask-login
    flask/bin/pip install flask-openid
    flask/bin/pip install flask-mail
    flask/bin/pip install flask-sqlalchemy
    flask/bin/pip install sqlalchemy-migrate
    flask/bin/pip install flask-whooshalchemy
    flask/bin/pip install flask-wtf
    flask/bin/pip install flask-babel
    flask/bin/pip install guess_language
    flask/bin/pip install flipflop
    flask/bin/pip install coverage
```
- Run ```./run.py```  to sart the server (on Windows use ``flask\Scripts\python rest.py`` insead)
- Open http://localhost:5000/index.html on your web browser to run the client. This should show the REST api implemented
so far.

