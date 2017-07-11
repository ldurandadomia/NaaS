from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api


def create_app(config_name):
    app = Flask(__name__)

    # Provide configuration parameters
    app.config.from_object(config_name)

    # Register the blueprints

    # Add the before request handler
    # app.before_request(create_before_request(app))
    return app


# Declaration de l'application Flask

app = create_app('config')
db = SQLAlchemy(app)

from restapp import models

# API version 1 : sans extension RestFul
from restapp import view_ports_v1
from restapp import view_single_port_v1
from restapp import view_switches_v1
from restapp import view_single_switch_v1
from restapp import view_errorhandler_v1
from restapp.view_errorhandler_v3 import MyApi

# Declaration des APIs
api = MyApi(app)  # API RestFul
api_restplus = Api(app, version='1.0')

# API version 2 : avec extension RestFul
from restapp import view_ports_v2
from restapp import view_single_port_v2
from restapp import view_switches_v2
from restapp import view_single_switch_v2

# API version 3 : RestFul et Marshal_With
from restapp import view_switches_v3
from restapp import view_single_switch_v3


# API version 7 : Generiques v4
from restapp import view_PortSwitches_v7

# API version 8 : RestPlus
from restapp import view_switches_v8
