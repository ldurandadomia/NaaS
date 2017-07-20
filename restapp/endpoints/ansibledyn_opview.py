__author__ = "Laurent DURAND"

from devices.ansible_dynamic import AnsibleDynamic
from restapp.app import nsop_ansibledyn
from flask_restplus import Resource
from flask import request
from flask import jsonify, make_response
from restapp.exceptions.exceptions import MissingAttribute
from ansibledyn_opserializers import AnsibleDynamicOpSerializers


@nsop_ansibledyn.route('', '/', endpoint="AnsibleDynamic")
class AnsiblePlay(Resource):

    #@nsop_ansibledyn.expect(AnsibleDynamicOpSerializers.Post, envelope='AnsiblePlay', code=200, validate=True)
    @nsop_ansibledyn.response(200, 'Playbook successfully run')
    @nsop_ansibledyn.response(404, 'Playbook has not been found')
    def post(self):
        """Run an dynamic playbook"""

        # Here is an example on how to run a dynamically built playbook

        #data = request.json
        try:
            pass
        except KeyError as missing_attribute:
            Message = "Attribute {} has not been provided for ansible playbook execution".format(missing_attribute.message)
            raise MissingAttribute(Message)

        # Playbook dynamic creation (3 tasks : ls and 2 debug messages)
        DynamicPlaybook = dict(
            name="Ansible Play",
            hosts='localhost',
            gather_facts='no',
            tasks=[
                dict(action=dict(module='shell', args='ls'), register='shell_out'),
                dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
                dict(action=dict(module='debug', args=dict(msg='Hello Galaxy!')))
                ])

        MyPlayBook = AnsibleDynamic(DynamicPlaybook)
        Result = MyPlayBook.run()
        return make_response(jsonify({'Playbook Results': [Task for Task in Result.results]}), 200)
