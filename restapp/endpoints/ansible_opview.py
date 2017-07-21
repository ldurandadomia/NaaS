__author__ = "Laurent DURAND"

from devices.ansible_playbook import AnsiblePlaybook
from restapp.app import nsop_ansible
from flask_restplus import Resource
from ansible_opserializers import AnsiblePlaybookOpSerializers
from flask import request
from flask import jsonify, make_response
from restapp.exceptions.exceptions import MissingAttribute


@nsop_ansible.route('', '/', endpoint="AnsiblePlaybooks")
class AnsiblePlay(Resource):

    @nsop_ansible.expect(AnsiblePlaybookOpSerializers.Post, envelope='AnsiblePlay', code=200, validate=True)
    @nsop_ansible.response(200, 'Playbook successfully run')
    @nsop_ansible.response(404, 'Playbook has not been found')
    def post(self):
        """Run the playbook given into "Name" argument"""
        data = request.json

        try:
            playbook_name = data["Name"]
            playbook_name = './playbook/{}'.format(playbook_name)

        except KeyError as missing_attribute:
            Message = "Attribute {} has not been provided for ansible playbook execution".format(missing_attribute.message)
            raise MissingAttribute(Message)

        if "Inventory" in data.keys():
            inventory = data["Inventory"]
            inventory = './playbook/{}'.format(inventory)
        else:
            inventory=None

        MyPlayBook = AnsiblePlaybook(playbook_name,inventory_filename=inventory)
        Result = MyPlayBook.run()
        return make_response(jsonify({'Playbook Results': [Task for Task in Result.results]}), 200)
