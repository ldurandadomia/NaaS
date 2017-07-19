__author__ = "Laurent DURAND"

from flask_restplus import fields
from restapp.app import ns_switches as api

class PortSerializers:
    """This Class is an Interface used to Serialize all input and output for Port endpoint."""

    # Ports GET Serializer
    Get = api.model('PortGet', {
        'Id': fields.Integer(readOnly=True, description='Port unique identifier'),
        'Name': fields.String(description='Port Name'),
        'Speed': fields.String(description='Port Speed (auto/10/100/1G/10G/100G)'),
        'Duplex': fields.String(description='Port Duplex (auto/half/full)'),
        'Status': fields.String(description='Port administrative status (enable/disable)'),
        'Switch_Id': fields.String(description='Switch unique identifier'),
        'uri': fields.Url('config_apis.Port', absolute=True, scheme='http'),
    })
