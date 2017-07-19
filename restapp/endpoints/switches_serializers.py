__author__ = "Laurent DURAND"

from flask_restplus import fields
from restapp.app import ns_switches as api
from port_serializers import PortSerializers

class SwitchesSerializers:
    """This Class is an Interface used to Serialize all input and output for Switches endpoint."""

    # Switches POST Serializer
    Post = api.model('SwitchesPost', {
        'Name': fields.String(description='Node Name', default="no name"),
        'ManagementIP': fields.String(description='Management IP address', required=True,
                                      help='No Management IP provided', example="192.168.1.1")
    })

    # Switches GET Serializer
    Get = api.model('SwitchesGet', {
        "Id": fields.Integer(readOnly=True, description='Switch unique identifier'),
        'Name': fields.String(description='Node Name'),
        'ManagementIP': fields.String(description='Management IP address'),
        'uri': fields.Url('config_apis.Switch', absolute=True, scheme='http'),
        # When using blueprint, endpoint must be prefixed by blueprint name
        'Ports': fields.List(fields.Nested(PortSerializers.Get))
    })

    # Switches PUT Serializer
    Put = api.model('SwitchesPut', {
        'Name': fields.String(description='Node Name'),
        'ManagementIP': fields.String(description='Management IP address'),
    })