from unittest import TestCase
from google.appengine.ext import testbed
from models import User, Course


class BaseTestCase(TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        # should all return None, because this is simply creating data and is all meant to be correct
        self.assertIsNone(User.register(None, 'teacher@gmail.com', 'pwd', 'pwd', 'teacher', 't'))
        self.assertIsNone(User.register(None, 'teacher2@gmail.com', 'pwd', 'pwd', 'teachertwo', 'ttwo'))
        self.assertIsNone(User.register(None, 'student@gmail.com', 'pwd', 'pwd', 'student', 's'))

        self.teacher = User.all().filter('email =', 'teacher@gmail.com').get()
        self.teacher2 = User.all().filter('email =', 'teacher2@gmail.com').get()
        self.student = User.all().filter('email =', 'student@gmail.com' ).get()

        self.assertIsNotNone(self.teacher)
        self.assertIsNone(self.teacher.make_teacher())
        self.assertIsNotNone(self.teacher2)
        self.assertIsNone(self.teacher2.make_teacher())

        self.assertIsNone(Course.create(self.teacher, 'public', ''))
        self.public = Course.all().filter('name =', 'Public').get()
        self.assertIsNotNone(self.public)
        self.assertIsNone(Course.create(self.teacher, 'private', 'on'))
        self.private = Course.all().filter('name =', 'Private').get()
        self.assertIsNotNone(self.private)


    def tearDown(self):
        self.testbed.deactivate()
