__author__ = "Laurent DURAND"

from flask_restplus import fields
from restapp.app import api

class SwitchesSerializers:
    """This Class is an Interface used to Serialize all input and output for Switches endpoint."""

    # Switches POST Serializer
    Post = api.model('SwitchesPost', {
        'Name': fields.String(description='Node Name', default="no name", location='json'),
        'ManagementIP': fields.String(description='Management IP address', required=True,
                                      help='No Management IP provided', location='json')
    })

    # Switches GET Serializer
    Get = api.model('SwitchesGet', {
        'Name': fields.String(description='Node Name'),
        'ManagementIP': fields.String(description='Management IP address'),
        'uri': fields.Url('Switch', absolute=True, scheme='http'),
#        'Ports': fields.List(fields.Nested(port_fields))
    })