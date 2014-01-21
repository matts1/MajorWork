from unittest import TestCase
from google.appengine.ext import testbed
from models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        self.assertIsNone(User.register(None, 'teacher@gmail.com', 'pwd', 'pwd', 'teacher', 't'))
        self.assertIsNone(User.all().get().make_teacher())

        User.register(None, 'student@gmail.com', 'pwd', 'pwd', 'student', 's')

    def tearDown(self):
        self.testbed.deactivate()
