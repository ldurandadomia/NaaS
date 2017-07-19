__author__ = "Laurent DURAND"

from switches_serializers import SwitchesSerializers
from flask_restplus import Resource
from restapp.app import db, ns_switches
from restapp.dao.switches_dao import SwitchesDao
from flask import jsonify, make_response


SwDao = SwitchesDao(db)

@ns_switches.param('Id', 'Switch Unique Identifier')
@ns_switches.route('/<int:Id>', endpoint='Switch')
@ns_switches.response(404, 'No switch found into inventory')
class OneSwitch(Resource):

    @ns_switches.response(200, 'Success')
    @ns_switches.marshal_with(SwitchesSerializers.Get, envelope='Switch')
    def get(self, Id):
        """Display a given switch in the NaaS inventory"""
        return SwDao.read(Id), 200


    @ns_switches.response(204, 'Successfully Deleted')
    def delete(self, Id):
        """Delete a given switch in the NaaS inventory"""
        SwId = SwDao.delete(Id)
        TextMessage = "Switch UUID {} has been successfully deleted.".format(SwId)
        return make_response(jsonify({"Message":TextMessage}), 204)
