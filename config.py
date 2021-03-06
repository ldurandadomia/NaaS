author__ = "Laurent DURAND"

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Global application parameters
VERSION="1.0"

# Flask settings
FLASK_SERVER_NAME = '0.0.0.0:5000'
FLASK_DEBUG = True  # Do not use debug mode in production


# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False


# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Unitary tests settings
TEST_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_tests.db')