__author__ = "Laurent DURAND"

from ports_serializers import PortsSerializers
from flask_restplus import Resource
from restapp.app import db, ns_switches
from restapp.dao.ports_dao import PortsDao
from flask import request

MyPortsDao = PortsDao(db)

@ns_switches.route('/<int:Switch_Id>/Ports', endpoint="Ports")
@ns_switches.response(404, 'No port found into inventory')
class SetOfPorts(Resource):

    @ns_switches.response(200, 'Success')
    @ns_switches.marshal_list_with(PortsSerializers.Get, envelope='Ports')
    def get(self, Switch_Id):
        """Display all ports in the NaaS inventory"""
        Filter_Attributes = request.args
        return MyPortsDao.list(Switch_Id, Filter_Attributes), 200


    @ns_switches.marshal_with(PortsSerializers.Get, envelope='Port')
    @ns_switches.expect(PortsSerializers.Post, envelope='Port', code=201, validate=True)
    @ns_switches.response(201, 'New port created into inventory')
    @ns_switches.response(409, 'A port with the same name name is already defined into inventory for the given switch')
    @ns_switches.response(422, 'A mandatory attribute has not been provided in the creation request')
    def post(self, Switch_Id):
        """Add a port into the NaaS inventory"""
        data = request.json
        return MyPortsDao.create(Switch_Id, data), 201