__author__ = "Laurent DURAND"

from switches_serializers import SwitchesSerializers
from switches_parsers import SwitchesParsers
from flask_restplus import Resource
from restapp.app import db, ns_switches
from restapp.dao.switches_dao import SwitchesDao
from flask import request

SwDao = SwitchesDao(db)

@ns_switches.route('', '/', endpoint="Switches")
@ns_switches.response(404, 'No switch found into inventory')
class SetOfSwitches(Resource):

    @ns_switches.response(200, 'Success')
    @ns_switches.marshal_list_with(SwitchesSerializers.Get, envelope='Switches')
    def get(self):
        """Display all switches in the NaaS inventory"""
        Filter_Attributes = request.args
#        Filter_Attributes = SwitchesParsers().get_parser.parse_args()
        return SwDao.list(Filter_Attributes), 200


    @ns_switches.marshal_with(SwitchesSerializers.Get, envelope='Switch')
    @ns_switches.expect(SwitchesSerializers.Post, envelope='Switch', code=201, validate=True)
    @ns_switches.response(201, 'New switch created into inventory')
    @ns_switches.response(409, 'A switch with the same management IP and name is already defined into inventory')
    @ns_switches.response(422, 'A mandatory attribute has not been provided in the creation request')
    def post(self):
        """Add a switch into the NaaS inventory"""
        data = request.json
        return SwDao.create(data), 201