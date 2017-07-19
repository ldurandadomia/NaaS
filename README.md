## Synopsis
This project is an example of Flask Resplus application. This Flask application allows to configure a network Switch using REST commands.
This application is written in python using Netmiko package. In This application we are using a **configuration database** for inventory and configuration data persistency. This application is considered as **always in sync with the network node**.
SQL Alchemy ORM is used to manage Database access.


## Code Examples

1. No example for the moment:
```python
todo  
```

## Installation
1. First clone this repository.
```bash
$ git clone https://github.com/ldurandadomia/NaaS.git
$ cd NaaS
```

2. Create a virtualenv, and activate it.
```bash
$ virtualenv env.
$ source env/bin/activate
```

3. After install all required packages to run the app.
```bash
$ pip install -r requirements.txt
```

4. Then, run the app.
```bash
$ python manage.py runserver
```

## Run Unitary tests
```bash
$ python manage.py unitary_tests
```

## API Reference
This api give us the ability to manage a network infrastructure.

The swagger documentation is dynamically generated  thanks to the Python Flask Restplus framework.
To see the documentation, access this url in your browser:


```bash
http://localhost:5000/naas/config/v1.0/api/
```

## Tests
All available tests are under the test repository.
Test have been implemented using the python unittest library.

## Contributors
Author | Email | Website
--- | --- | ---
*Laurent DURAND* | `FR Paris` | **https://www.nowhere.com**


## License
Free to use.
