__author__ = "Laurent DURAND"

from restapp.app import api
from switches_serializers import SwitchesSerializers
from flask_restplus import Resource
from restapp.app import db, ns_switches
from restapp.dao.switches_dao import SwitchesDao

SwDao = SwitchesDao(db)

#    def __init__(self):
#        """Constructor: define the post parser"""
#        self.post_parser = SwitchesParser()
#        super(SetOfSwitches, self).__init__()



@ns_switches.route('/')
@ns_switches.response(404, 'No switch found')
class SetOfSwitches(Resource):

    @api.marshal_with(SwitchesSerializers.Get, envelope='Switches')
    def get(self):
        """Display all switches"""

        # arguments a parser pour le filtrage

        return SwDao.list()

"""
    @marshal_with(switch_fields, envelope='Switch')
    def post(self):
        ""ajoute un switch a l'infrastructure""
        args = self.post_parser.parse_args()
        try:
            un_switch = models.Switches(Name=args.Name, ManagementIP=args.ManagementIP)
            db.session.add(un_switch)
            db.session.commit()
        except:
            abort(400)
        return un_switch, 201
"""

#api_restplus.add_resource(SetOfSwitches, '/todo/api/v8.0/Switches', endpoint='Switches')