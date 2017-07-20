__author__ = "Laurent DURAND"

from flask import jsonify
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from collections import namedtuple
from ansible_common import ResultCallback


class AnsibleDynamic:
    """This Class is used to manage Ansible creating a Dynamic Playbook."""
    def __init__(self, playbook_dict):
        """AnsiblePlaybook constructor
        playbook_dict : playbook = dynamic playbook to be run
        """
        self.playbook = playbook_dict

    def run(self):
        """ run a dynamic Ansible Playbook"""

        # Playbook execution variables setup
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'remote_user', 'private_key_file',
                              'ssh_common_args',
                              'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method',
                              'become_user', 'verbosity', 'check'])
        options = Options(connection='local', module_path='/path/to/mymodules', forks=100, remote_user=None,
                          private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                          scp_extra_args=None, become=None, become_method=None, become_user=None, verbosity=None,
                          check=False)
        variable_manager = VariableManager()
        loader = DataLoader()
        passwords = dict(vault_pass='secret')

        # stdout message processing
        results_callback = ResultCallback()

        # Inventory Dynamic creation
        # inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='filename')
        inventory = Inventory(loader=loader, variable_manager=variable_manager)
        variable_manager.set_inventory(inventory)

        play = Play().load(self.playbook, variable_manager=variable_manager, loader=loader)

        # Excecution
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                # passwords=passwords,
                passwords=None,
                # stdout_callback='default', # display data on default STDOUT
                stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

        return results_callback


