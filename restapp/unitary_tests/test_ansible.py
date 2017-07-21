from __future__ import absolute_import
import unittest2 as unittest
from devices.ansible_playbook import AnsiblePlaybook
import os

__author__ = "Laurent DURAND"


class TestAnsible(unittest.TestCase):

    def setUp(self):
        """Run before each test"""
        pass


    def tearDown(self):
        """Run after each test"""
        pass


    def test_ansible(self):
        '''Test all playbooks having a test inventory defined'''
        path = "/home/ldurand/todo-api/playbook/"
        dirs = os.listdir(path)
        for file in dirs:
            if os.path.isfile(path+file):
                pass
                if file[-4:] == '.inv':
                    filename = file[:-4]
                    Inventory = path + filename + ".inv"
                    Playbook = path + filename + ".yml"

                    MyPlayBook = AnsiblePlaybook(Playbook, inventory_filename=Inventory)
                    Results = MyPlayBook.run()

                    for result in Results.results:
                        status = result["status"]
                        assert status=='changed' or status=='ok'

if __name__ == '__main__':
    unittest.main()
