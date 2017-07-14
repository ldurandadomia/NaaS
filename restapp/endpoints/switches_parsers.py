author__ = "Laurent DURAND"


class SwitchesParser(Resource):

    def __init__(self):
        """Constructor: define the post parser"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('ManagementIP', type=str, required=True,
                                   help='No Management provided',
                                   location='json')
        self.post_parser.add_argument('Name', type=str, default="no name",
                                   location='json')

        super(SwitchesParser, self).__init__()


