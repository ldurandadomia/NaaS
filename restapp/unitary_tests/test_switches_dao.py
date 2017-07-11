from __future__ import absolute_import
from flask_testing import TestCase
import unittest2 as unittest
from config import TEST_DATABASE_URI
from restapp.dao import SwitchesDao
from restapp.exceptions import IntegrityConstraintViolation, MissingAttribute, BadAttribute, NotFound
from restapp import app as rest_app, db


SwDao = SwitchesDao(db)


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


    def test_switch_create(self):
        """Check Switch Creation and Unicity Constraint"""
        # A first switch
        MySwitch = {"Name": "First_Switch", "ManagementIP": "2.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "2.1.1.1")

        # A duplication issue is expected
        with self.assertRaises(IntegrityConstraintViolation):
            Result = SwDao.create(MySwitch)

        # Switch IPAddress is missing
        MySwitch = {"Name": "First_Switch"}
        with self.assertRaises(MissingAttribute):
            Result = SwDao.create(MySwitch)

        # Switch Name is missing
        MySwitch = {"ManagementIP": "2.1.1.1"}
        with self.assertRaises(MissingAttribute):
            Result = SwDao.create(MySwitch)


    def test_switch_read(self):
        """Check if we can retreive a switch using its UUID"""
        # A first switch is created
        MySwitch = {"Name": "First_Switch", "ManagementIP": "2.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "2.1.1.1")

        # This switch is existing
        ReadSwitch = SwDao.read(1)
        self.assertEqual(ReadSwitch.Id, 1)

        # But this one should not exist
        with self.assertRaises(NotFound):
            ReadSwitch = SwDao.read(2)


    def test_switch_list(self):
        """Check if we can retreive a switch list"""
        # No Switch is existing
        with self.assertRaises(NotFound):
            ReadSwitches = SwDao.list()

        # A first switch is created
        MySwitch = {"Name": "First_Switch", "ManagementIP": "1.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "1.1.1.1")

        # A Second switch is created
        MySwitch = {"Name": "Second_Switch", "ManagementIP": "2.2.2.2"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "Second_Switch")
        self.assertEqual(Result.ManagementIP, "2.2.2.2")

        # Two switches are existing
        ReadSwitches = SwDao.list()
        self.assertEqual(len(ReadSwitches), 2)


    def test_switch_list_with_filter(self):
        """Check if we can retreive a switch list with a given filter"""
        # No Switch is existing
        with self.assertRaises(NotFound):
            ReadSwitches = SwDao.list({"Name": "Second_Switch", "ManagementIP": "2.2.2.2"})

        # A first switch is created
        MySwitch = {"Name": "First_Switch", "ManagementIP": "1.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "1.1.1.1")

        # A Second switch is created
        MySwitch = {"Name": "Second_Switch", "ManagementIP": "2.2.2.2"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "Second_Switch")
        self.assertEqual(Result.ManagementIP, "2.2.2.2")

        # We are looking for the first switch using its name
        ReadSwitches = SwDao.list({"Name": "First_Switch"})
        self.assertEqual(len(ReadSwitches), 1)

        # We are looking for the first switch using its IP address
        ReadSwitches = SwDao.list({"ManagementIP": "1.1.1.1"})
        self.assertEqual(len(ReadSwitches), 1)

        # We are looking for the second switch with all its attributes
        ReadSwitches = SwDao.list({"Name": "Second_Switch", "ManagementIP": "2.2.2.2"})
        self.assertEqual(len(ReadSwitches), 1)

        # We are looking a switch that is not into our database
        with self.assertRaises(NotFound):
            ReadSwitches = SwDao.list({"Name": "First_Switch", "ManagementIP": "2.2.2.2"})

        # We are looking a switch using a not existing attribute
        with self.assertRaises(NotFound):
            ReadSwitches = SwDao.list({"SwName": "First_Switch"})


    def test_switch_delete(self):
        """Check if we can delete a switch using its UUID"""
        # No Switch is existing
        with self.assertRaises(NotFound):
            uuid = SwDao.delete(1)

        # A first switch is created
        MySwitch = {"Name": "First_Switch", "ManagementIP": "1.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "1.1.1.1")

        # Now we can delete the created switch
        uuid = SwDao.delete(1)
        self.assertEqual(uuid, 1)


    def test_switch_update(self):
        """Check if we can update a switch using its UUID"""
        # No Switch is existing
        with self.assertRaises(NotFound):
            UpdatedSwitch = SwDao.update(1, {"Name": "First_Switch", "ManagementIP": "1.1.1.1"})

        # A first switch is created
        MySwitch = {"Name": "First_Switch", "ManagementIP": "1.1.1.1"}
        Result = SwDao.create(MySwitch)
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "1.1.1.1")

        # Nothing Change
        Result = SwDao.update(1, {"Name": "First_Switch", "ManagementIP": "1.1.1.1"})
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "1.1.1.1")

        # Only its IP has been changed
        Result = SwDao.update(1, {"Name": "First_Switch", "ManagementIP": "3.3.3.3"})
        self.assertEqual(Result.Name, "First_Switch")
        self.assertEqual(Result.ManagementIP, "3.3.3.3")

        # Only its Name has been changed
        Result = SwDao.update(1, {"Name": "New_Switch", "ManagementIP": "3.3.3.3"})
        self.assertEqual(Result.Name, "New_Switch")
        self.assertEqual(Result.ManagementIP, "3.3.3.3")

        # Only its Name has been changed
        Result = SwDao.update(1, {"Name": "New_Switch2"})
        self.assertEqual(Result.Name, "New_Switch2")
        self.assertEqual(Result.ManagementIP, "3.3.3.3")

        # Not possible to update its UUID
        with self.assertRaises(BadAttribute):
            Result = SwDao.update(1, {"Id": 200})

        # Not possible to update an unknown attribute
        with self.assertRaises(BadAttribute):
            Result = SwDao.update(1, {"SwName": "MyNewName"})


if __name__ == '__main__':
    unittest.main()
