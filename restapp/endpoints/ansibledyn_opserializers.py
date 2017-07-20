__author__ = "Laurent DURAND"

from flask_restplus import fields
from restapp.app import nsop_ansible as api

class AnsibleDynamicOpSerializers:
    """This Class is an Interface used to Serialize all input and output for Ansible endpoint."""

    # Ansible POST Serializer
    Post = api.model('AnsibleOperation', {
        'Name': fields.String(description='Ansible Playbook Name', required=True,
                                      help='No Playbook name provided', example="test.yml")
    })