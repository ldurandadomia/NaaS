__author__ = 'Laurent DURAND'

class Dao(object):
    """Parent class for Data Access Model"""
    def __init__(self, database):
        """ Dao constructor
        parameters : database = database to be used by Dao
        attributes : db = database used by Dao
        """
        self.db = database

    def create(self, data):
        """ Create a new object into the database
        parameters : data = attributes dictionary"""
        pass

    def list(self, Filters=None):
        """ List All Elements in Database
        parameters : Filters = optional attributes values used as a filter for the database query"""
        pass

    def read(self, uuid):
        """Retreive a given object using its UUID
        parameters : uuid = Object UUID to be retreived into the database"""
        pass

    def update(self, uuid, data):
        """Update an existing object into the database using data attributes provided
        parameters :  uuid = identifier of object to be updated
                      data = attributes to be updated dictionary"""
        pass

    def delete(self, uuid):
        """Delete an object from the database
        parameters :  uuid = identifier of object to be deleted"""
        pass

