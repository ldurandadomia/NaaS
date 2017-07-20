__author__ = "Laurent DURAND"

from flask import jsonify
from flask import abort
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible_common import ResultCallback
from collections import namedtuple
from restapp.exceptions.exceptions import NotFound
import os


class AnsiblePlaybook:
    """This Class is used to manage Ansible."""
    def __init__(self, playbook_name):
        """AnsiblePlaybook constructor
        playbook_name : playbook = playbook to be run
        """
        self.playbook = playbook_name

    def run(self):
        """run an Ansible Playbook"""

        # Playbook execution variables setup
        Options = namedtuple('Options',
                             ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                              'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                              'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='local',
                          module_path=None, forks=100, remote_user='slotlocker', private_key_file=None,
                          ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
                          become=None,
                          become_method=None, become_user=None, verbosity=None, check=False)

        variable_manager = VariableManager()
        variable_manager.extra_vars = {'ansible_user': 'ansible', 'ansible_port': '5986', 'ansible_connection': 'local',
                                       'ansible_password': 'pass'}  # Here are the variables used in the playbook
        loader = DataLoader()
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='fullpath/to/hosts')

        passwords = {}

        # stdout message processing
        results_callback = ResultCallback()

        playbook_path = './playbook/{}'.format(self.playbook)
        if not os.path.exists(playbook_path):
            Message = "Playbook {} has not been found".format(playbook_path)
            raise NotFound(Message)

        pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                                loader=loader, options=options, passwords=passwords)
        pbex._tqm._stdout_callback = results_callback
        results = pbex.run()
        return results_callback