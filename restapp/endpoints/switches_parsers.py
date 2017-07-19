author__ = "Laurent DURAND"

from flask_restplus import Resource
from flask_restplus import reqparse

class SwitchesParsers(Resource):

    def __init__(self):
        """Constructor: define the parsers"""

        # Look only in the POST body : location='form'
        # Look only in the querystring : location='args'
        # From the request headers : location='headers'
        # From http cookies : location='cookies'
        # From file uploads : location='files'
        # Look into the body : location='json'

        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('ManagementIP', type=str, location='args')
        self.get_parser.add_argument('Name', type=str, location='args')


        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('ManagementIP', type=str, required=True,
                                   help='No Management provided',
                                   location='json')
        self.post_parser.add_argument('Name', type=str, default="no name",
                                   location='json')

        super(SwitchesParsers, self).__init__()