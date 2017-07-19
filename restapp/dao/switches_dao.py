__author__ = 'Laurent DURAND'

from dao import Dao
from database import models
from restapp.exceptions.exceptions import IntegrityConstraintViolation, MissingAttribute, BadAttribute, NotFound


class SwitchesDao(Dao):
    """Data Access Model for Switches"""
    def __init__(self, database):
        """ SwitchesDao constructor
        parameters : database = database to be used by Dao
        attributes : db = database used by Dao"""
        super(SwitchesDao, self).__init__(database)


    def create(self, data):
        """Create a switch into database using data attributes provided
        parameters : data = switch attributes"""
        try:
            sw_name = data["Name"]
            sw_mgnt_ip = data["ManagementIP"]
        except KeyError as missing_attribute:
            Message = "Attribute {} has not been provided for Switch creation into inventory".format(missing_attribute.message)
            raise MissingAttribute(Message)

        un_switch = models.Switches(Name=sw_name, ManagementIP=sw_mgnt_ip)
        try:
            self.db.session.add(un_switch)
            self.db.session.commit()
        except Exception as e:
            Message = 'Switch Name: {} with Management IP address: {} is already defined into inventory.'.format(sw_name, sw_mgnt_ip)
            raise IntegrityConstraintViolation(Message)
        return un_switch


    def list(self, Filters=None):
        """ List All Switches Elements in Database
        parameters : Filters = optional attributes values used as a filter for the query"""
        if (Filters == None) or (len(Filters) == 0):
            allSwitches = models.Switches.query.all()
        else:
            # Enforce query filter
            dbQuery = models.Switches.query
            try:
                for ParamName, ParamValue in Filters.items():
                    dbQuery = dbQuery.filter(getattr(models.Switches, ParamName) == ParamValue)
                allSwitches = dbQuery.all()

            except AttributeError as UnknownAttribute:
                Message = UnknownAttribute.message
                Position = Message.index('has no attribute') + len('has no attribute')
                AttributeName = Message[Position:]
                NewMessage = "A Switch has no such attribute: {}.".format(AttributeName)
                raise NotFound(description=NewMessage, response=404)

        if (allSwitches == None) or (len(allSwitches) == 0 ):
            raise NotFound(description="No Switch found", response=404)

        return allSwitches


    def read(self, uuid):
        """Retreive a given switch using its UUID"""
        un_switch = models.Switches.query.get_or_404(uuid)
        return un_switch


    def update(self, uuid, data):
        """Update a switch into database using data attributes provided"""
        un_switch = models.Switches.query.get_or_404(uuid)

        updatable_fields = ["Name", "ManagementIP"]
        for attribut in data.keys():
            try:
                updatable = updatable_fields.index(attribut)
            except ValueError as NotAllowed:
                Message = NotAllowed.message
                Position = Message.index('is not in list')
                AttributeName = Message[:Position]
                NewMessage = "A Switch has no such attribute: {} or is readonly.".format(AttributeName)
                raise BadAttribute(Message)

            setattr(un_switch, attribut, data[ attribut ])
        self.db.session.commit()
        return un_switch


    def delete(self, uuid):
        """Delete a given switch using its UUID"""
        # we are deleting all ports records
        dbQuery = models.Ports.query
        dbQuery = dbQuery.filter(getattr(models.Ports, "Switch_Id") == uuid)
        AllPorts = dbQuery.all()
        for Element in AllPorts:
            self.db.session.delete(Element)

        un_switch = models.Switches.query.get_or_404(uuid)
        self.db.session.delete(un_switch)
        self.db.session.commit()
        return uuid