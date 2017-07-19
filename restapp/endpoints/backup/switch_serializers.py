__author__ = "Laurent DURAND"

from flask_restplus import fields
from restapp.app import ns_switches as api
from port_serializers import PortSerializers

class SwitchSerializers:
    """This Class is an Interface used to Serialize all input and output for Switch endpoint."""

    # Switch GET Serializer
    Get = api.model('SwitchGet', {
        "Id": fields.Integer(readOnly=True, description='Switch unique identifier'),
        'Name': fields.String(description='Node Name'),
        'ManagementIP': fields.String(description='Management IP address'),
        'uri': fields.Url('config_apis.Switch', absolute=True, scheme='http'),
        # When using blueprint, endpoint must be prefixed by blueprint name
        'Ports': fields.List(fields.Nested(PortSerializers.Get))

    })