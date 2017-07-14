__author__ = "Laurent DURAND"
from exceptions import IntegrityConstraintViolation, MissingAttribute, BadAttribute, NotFound
from restapp.app import logger
from restapp.app import api

@api.errorhandler
def handle_error(self, e):
    """" Overrides the handle_error() method of the api and adds custom error handling
    :param e: error object
    """
    message = 'An unhandled exception occurred.'
    logger.exception(e.message)

    code = getattr(e, 'code', 500)  # Gets code or defaults to 500 - Internal Server Error
    if code == 404:
        return self.make_response({
            'message': 'not-found',
            'code': 404 # Not Found
        }, 404)
    return super(MyApi, self).handle_error(e)  # handle others the default way


@api.errorhandler(NotFound)
def database_not_found_errorhandler(error):
    """Define the error pocessing when an object is not found into database"""
    logger.warning(error.description)
    return {'message': error.description}, 404 # Not Found


@api.errorhandler(IntegrityConstraintViolation)
def database_integrity_constraint_errorhandler(error):
    logger.warning(error.message)
    return {'message': error.message}, 409 # Conflict


@api.errorhandler(MissingAttribute)
def MissingAttribute_errorhandler(error):
    logger.warning(error.message)
    return {'message': error.message}, 422 # Unprocessable entity


@api.errorhandler(BadAttribute)
def BadAttribute_errorhandler(error):
    logger.warning(error.message)
    return {'message': error.message}, 417 # Expectation failed