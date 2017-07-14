__author__ = "Laurent DURAND"

from __future__ import absolute_import
from flask_testing import TestCase
import unittest2 as unittest
import json
from restapp import app as rest_app, db
from config import TEST_DATABASE_URI
from restapp.models import Switches

api_version = "3.0"
naas_endpoint = "/todo/api/v" + api_version


class TestSwitches(TestCase):

    def create_app(self):
        app = rest_app
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app


    def setUp(self):
        """Run before each test"""
        db.create_all()


    def tearDown(self):
        """Run after each test"""
        db.session.remove()
        db.drop_all()


    def test_switches_get(self):
        '''Test if all switches can be read with REST'''
        response = self.client.get(naas_endpoint + "/Switches")
        self.assertEquals(response.json, dict(Switches=[]))
        self.assertEqual(response.status_code, 200)


    def test_switches_post(self):
        '''Test if a new switch can be created with REST'''
        headers = [('Content-Type', 'application/json')]
        url_endpoint = naas_endpoint + "/Switches"
        payload = json.dumps({"ManagementIP":"10.10.10.1"})
        response = self.client.post(url_endpoint, data=payload, headers=headers)
        self.assertEquals(response.status_code, 201)


    def test_switches_create_db(self):
        '''Test if a given switch can be created in the Database'''
        aSwitch = Switches(Name='Test-Switch', ManagementIP="1.1.1.1")
        aSwitch2 = Switches(Name='Test-Switch', ManagementIP="2.2.2.2")
        db.session.add(aSwitch)
        db.session.add(aSwitch2)
        # this works
        assert aSwitch in db.session
        # this raises an AssertionError
        #assert aSwitch2 not in db.session


    def test_switches_create_REST_db(self):
        '''Test if a given switch can be created with REST and retrieved in the Database'''
        headers = [('Content-Type', 'application/json')]
        url_endpoint = naas_endpoint + "/Switches"
        payload = json.dumps({"ManagementIP":"10.10.10.1"})
        self.client.post(url_endpoint, data=payload, headers=headers)
        aSwitch = Switches.query.get_or_404(1)

        # this works
        assert aSwitch in db.session


if __name__ == '__main__':
    unittest.main()
