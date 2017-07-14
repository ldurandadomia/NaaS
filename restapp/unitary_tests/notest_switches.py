__author__ = "Laurent DURAND"

from __future__ import absolute_import
from flask_testing import LiveServerTestCase
import unittest2 as unittest
import urllib2
import requests
import json
from restapp import app as rest_app
from config import TEST_DATABASE_URI

api_version = "3.0"
naas_url = "http://localhost:9999/todo/api/v" + api_version



class TestSwitches(LiveServerTestCase):
    def create_app(self):
        app = rest_app
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 9999
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app


    def setUp(self):
        # set up header
        self.headers = {'content-type': 'application/json'}
        # set up Endpoint uri
        self.url_endpoint = naas_url + "/Switches"
        #set up payload
        self.payload = json.dumps({"ManagementIP":"10.10.10.1"})


    def test_server_is_up_and_running(self):
        '''Test if flask application is up and running'''
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


    def test_switches_retrieval(self):
        '''Test if a given switch can be read in the Database'''
        response = requests.get(self.url_endpoint)
        content = response.json()
        self.assertEqual(response.status_code, 200)
        # Check if FirstSwitch name and IP are OK
        self.assertEqual(content["Switches"][0].get("Name"), "no name")
        self.assertEqual(content["Switches"][0].get("ManagementIP"), "10.10.10.1")


    def test_switch_creation(self):
        '''Test if a new switch can be created in the Database'''
        response = requests.post(self.url_endpoint, data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
#        self.assertEqual(response.content.rstrip(), 'null')



if __name__ == '__main__':
    unittest.main()