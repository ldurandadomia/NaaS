__author__ = "Laurent DURAND"

from ports_serializers import PortsSerializers
from flask_restplus import Resource
from restapp.app import db, ns_switches
from restapp.dao.ports_dao import PortsDao
from flask import jsonify, make_response
from flask import request

MyPortsDao = PortsDao(db)

@ns_switches.param('Id', 'Port Unique Identifier')
@ns_switches.param('Switch_Id', 'Switch Unique Identifier')
@ns_switches.route('/<int:Switch_Id>/Ports/<int:Id>', endpoint='Port')
@ns_switches.response(404, 'No port found into inventory')
class OnePort(Resource):

    @ns_switches.response(200, 'Success')
    @ns_switches.marshal_with(PortsSerializers.Get, envelope='Port')
    def get(self, Id, Switch_Id):
        """Display a given port on a switch in the NaaS inventory"""
        return MyPortsDao.read(Id, Switch_Id), 200

    @ns_switches.response(204, 'Successfully Deleted')
    def delete(self, Id, Switch_Id):
        """Delete a given port on a switch in the NaaS inventory"""
        PortId = MyPortsDao.delete(Id, Switch_Id)
        TextMessage = "Port UUID {} has been successfully deleted onto switch UUID {}.".format(PortId, Switch_Id)
        Response = make_response(jsonify({"Message":TextMessage}), 204)
        return Response

    @ns_switches.expect(PortsSerializers.Put, envelope='Port', code=200, validate=True)
    @ns_switches.marshal_with(PortsSerializers.Get, envelope='Port')
    @ns_switches.response(200, 'Successfully Updated')
    def put(self, Id, Switch_Id):
        """Update a given port on a switch in the NaaS inventory"""
        data = request.json
        return MyPortsDao.update(Id, Switch_Id, data), 200