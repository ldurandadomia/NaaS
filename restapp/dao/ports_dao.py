__author__ = 'Laurent DURAND'

from dao import Dao
from database import models
from restapp.exceptions.exceptions import IntegrityConstraintViolation, MissingAttribute, BadAttribute, NotFound


class PortsDao(Dao):
    """Data Access Model for Ports"""
    def __init__(self, database):
        """ PortDao constructor
        parameters : database = database to be used by Dao
        attributes : db = database used by Dao"""
        super(PortsDao, self).__init__(database)


    def create(self, Switch_Id, data):
        """Create a port into database using data attributes provided
        parameters : data = port attributes"""
        # We are checking that the switch is existing
        un_switch = models.Switches.query.get_or_404(Switch_Id)

        try:
            port_SwId = Switch_Id
            port_name = data["Name"]
            port_speed = data["Speed"]
            port_duplex = data["Duplex"]
            port_status = data["Status"]

        except KeyError as missing_attribute:
            Message = "Attribute {} has not been provided for Port creation into inventory".format(missing_attribute.message)
            raise MissingAttribute(Message)

        un_port = models.Ports(Switch_Id=port_SwId, Name=port_name, Speed=port_speed, Duplex=port_duplex, Status=port_status)
        try:
            self.db.session.add(un_port)
            self.db.session.commit()
        except Exception as e:
            Message = 'Port name: {} is already defined into inventory for given switch (UUID: {}).'.format(port_name, port_SwId)
            raise IntegrityConstraintViolation(Message)
        return un_port


    def list(self, Switch_Id, Filters=None):
        """ List All Ports Elements in Database for a given Switch
        parameters : Filters = optional attributes values used as a filter for the query"""

        dbQuery = models.Ports.query
        dbQuery = dbQuery.filter(getattr(models.Ports, "Switch_Id") == Switch_Id)

        if not ((Filters == None) or (len(Filters) == 0)):
            # Enforce query filter
            try:
                for ParamName, ParamValue in Filters.items():
                    dbQuery = dbQuery.filter(getattr(models.Ports, ParamName) == ParamValue)

            except AttributeError as UnknownAttribute:
                Message = UnknownAttribute.message
                Position = Message.index('has no attribute') + len('has no attribute')
                AttributeName = Message[Position:]
                NewMessage = "A Port has no such attribute: {}.".format(AttributeName)
                raise NotFound(description=NewMessage, response=404)

        allPorts = dbQuery.all()

        if (allPorts == None) or (len(allPorts) == 0 ):
            raise NotFound(description="No port found", response=404)

        return allPorts


    def read(self, uuid, Switch_Id):
        """Retreive a given port using its UUID"""
        un_port = models.Ports.query.get_or_404(uuid)
        if (un_port.Switch_Id != Switch_Id ):
            raise NotFound(description="Port not found on given switch", response=404)
        return un_port


    def update(self, uuid, data):
        """Update a port into database using data attributes provided"""
        un_port = models.Ports.query.get_or_404(uuid)

        updatable_fields = ["Name", "Speed", "Duplex", "Status"]

        for attribut in data.keys():
            try:
                updatable = updatable_fields.index(attribut)
            except ValueError as NotAllowed:
                Message = NotAllowed.message
                Position = Message.index('is not in list')
                AttributeName = Message[:Position]
                NewMessage = "A Port has no such attribute: {} or is readonly.".format(AttributeName)
                raise BadAttribute(Message)

            setattr(un_port, attribut, data[ attribut ])
        self.db.session.commit()
        return un_port


    def delete(self, uuid, Switch_Id):
        """Delete a given port using its UUID"""
        un_port = models.Ports.query.get_or_404(uuid)
        self.db.session.delete(un_port)
        self.db.session.commit()
        return uuid
