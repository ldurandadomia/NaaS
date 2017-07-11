# Manage RESTAPP application
import unittest2 as unittest
import coverage
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from restapp import app, db
from restapp.models import Switches

COV = coverage.coverage(
    branch=True,
    include='restapp/*',
    omit=[
        'restapp/tests/*',
        'restapp/*/__init__.py'
    ]
)
COV.start()



migrate = Migrate(app, db)
manager = Manager(app)

# Manage creation of all needed migration commands
manager.add_command('db', MigrateCommand)


@manager.command
def unitary_tests():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('restapp/unitary_tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def integration_tests():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('restapp/integration_tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('restapp/unitary_tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_test_data():
    """Create a switch"""
    db.session.add(Switches(Name='Test-Switch', ManagementIP="1.1.1.1"))
    db.session.commit()


if __name__ == '__main__':
    manager.run()