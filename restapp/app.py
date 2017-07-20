__author__ = "Laurent DURAND"

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
import logging.config, logging
from config import VERSION


# Manage Logger configuration
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("NaaS")


def create_app(config_name):
    app = Flask(__name__)

    # Provide configuration parameters
    app.config.from_object(config_name)

    # Add the before request handler
    # app.before_request(create_before_request(app))
    return app


# Flask application creation
app = create_app('config')
db = SQLAlchemy(app)
db.init_app(app)

# Register our 3 blueprints (config, running and operation)
config_blueprint = Blueprint('config_apis', __name__, url_prefix='/naas/config/v{}'.format(VERSION))
running_blueprint = Blueprint('running_apis', __name__, url_prefix='/naas/running/v{}'.format(VERSION))
operation_blueprint = Blueprint('operation_apis', __name__, url_prefix='/naas/operation/v{}'.format(VERSION))


# Restplus API creation
api = Api(app=config_blueprint, doc='/api/',version=VERSION, title='NaaS - Network as a Service - Configuration',
          description='This is the {} version of Network Automation "configuration" application.'.format(VERSION))

op_api = Api(app=operation_blueprint, doc='/api/',version=VERSION, title='NaaS - Network as a Service - Operation',
          description='This is the {} version of Network Automation "operation" application.'.format(VERSION))

ex_api = Api(app=running_blueprint, doc='/api/',version=VERSION, title='NaaS - Network as a Service - Running',
          description='This is the {} version of Network Automation "running" application.'.format(VERSION))


# api.init must occur before app.register - not needed here as api has been initialized with config_blueprint
# api.init_app(config_blueprint)
app.register_blueprint(config_blueprint)
app.register_blueprint(operation_blueprint)
app.register_blueprint(running_blueprint)


# Register all API NameSpaces
ns_switches = api.namespace('Switches', description='Switch nodes configuration APIs')
api.add_namespace(ns_switches)

nsop_ansible = op_api.namespace('Ansible', description='Manage ansible playbooks execution')
op_api.add_namespace(nsop_ansible)

nsop_ansibledyn = op_api.namespace('AnsibleDynamic', description='Manage ansible playbooks dynamic creation and execution')
op_api.add_namespace(nsop_ansibledyn)

# Import all exceptions
from restapp.exceptions import errorhandlers

# Import all views
from restapp.endpoints import switches_view
from restapp.endpoints import switch_view
from restapp.endpoints import ports_view
from restapp.endpoints import port_view
from restapp.endpoints import ansible_opview
from restapp.endpoints import ansibledyn_opview