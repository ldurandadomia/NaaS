__author__ = "Laurent DURAND"

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
import logging.config
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
config_blueprint = Blueprint('Network node configuration API', __name__, url_prefix='/naas/config/v{}'.format(VERSION))
running_blueprint = Blueprint('running_apis', __name__, url_prefix='/naas/running/v{}'.format(VERSION))
operation_blueprint = Blueprint('operation_apis', __name__, url_prefix='/naas/operation/v{}'.format(VERSION))

# Restplus API creation
api = Api(app=config_blueprint, doc='/api/',version=VERSION, title='NaaS - Network as a Service',
          description='This is the {} version of Network Automation application.'.format(VERSION))

# api.init must occur before app.register - not needed here as api has been initialized with config_blueprint
# api.init_app(config_blueprint)
app.register_blueprint(config_blueprint)


# Register all API NameSpaces
ns_switches = api.namespace('Switches', description='Switch nodes configuration APIs')
api.add_namespace(ns_switches)

# Import all exceptions
from restapp.exceptions import errorhandlers

# Import all view
from restapp.endpoints import switches_view