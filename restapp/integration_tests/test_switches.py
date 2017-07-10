import unittest2
import requests
import json

api_version = "1.0"
naas_url = "http://localhost:5000/todo/api/v" + api_version


class TestSwitches(unittest2.TestCase):

    def setUp(self):
        # set up header
        self.headers = {'content-type': 'application/json'}
        # set up Endpoint uri
        self.url_endpoint = naas_url + "/Switches"
        #set up payload
        self.payload = json.dumps({"ManagementIP":"10.10.10.1"})


    def test_switch_creation(self):
        '''Test if switch can be created in the Database'''
        response = requests.post(self.url_endpoint, data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
#        self.assertEqual(response.content.rstrip(), 'null')


    def test_switches_retrieval(self):
        '''Test if switch can be read in the Database'''
        response = requests.get(self.url_endpoint)
        content = response.json()
        self.assertEqual(response.status_code, 200)
        # Check if FirstSwitch name and IP are OK
        self.assertEqual(content["Switches"][0].get("Name"), "no name")
        self.assertEqual(content["Switches"][0].get("ManagementIP"), "10.10.10.1")


if __name__ == '__main__':
    unittest.main()