from models.tests.basetest import TestCase
from models.users import User

class UserTest(TestCase):
    def test_bad_register(self):
        self.assertIsNotNone(
            User.register(None, 'matt@gmail.com', 'pwd', 'diffpwd', 'first', 'last'),
            'Attempt to register with different passwords'
        )
        self.assertIsNotNone(
            User.register(None, 'matt@gmail.com', '', '', 'first', 'last'),
            'Attempt to register with empty passwords'
        )
        self.assertIsNotNone(
            User.register(None, '', 'pwd', 'pwd', 'first', 'last'),
            'Attempt to register with empty email'
        )
        self.assertIsNotNone(
            User.register(None, 'm@gmail.com', 'pwd', 'pwd', '', 'last'),
            'Attempt to register with empty first name'
        )
        self.assertIsNotNone(
            User.register(None, 'm@gmail.com', 'pwd', 'pwd', '', 'last'),
            'Attempt to register with invalid first name'
        )
        self.assertIsNotNone(
            User.register(None, 'm@gmail.com', 'pwd', 'pwd', 'first', ''),
            'Attempt to register with empty surname'
        )
        self.assertIsNotNone(
            User.register(None, 'm@gmail.com', 'pwd', 'pwd', 'blah-blah-', 'last'),
            'Attempt to register with invalid surname'
        )
        self.assertIsNotNone(
            User.register(None, 'blah', 'pwd', 'diffpwd', 'first', 'last'),
            'Attempt to register with invalid email'
        )
        self.assertIsNotNone(
            User.register(None, 'blah@@g.com', 'pwd', 'diffpwd', 'first', 'last'),
            'Attempt to register with another invalid email'
        )
        # don't test more invalid emails - validator is already tested

    def test_register_login(self):
        self.assertIsNotNone(
            User.authenticate(None, 'matt@gmail.com', 'correcthorsebatterystaple'),
            'Try to login with an email that doesn\'t exist'
        )
        self.assertIsNone(
            User.register(None, 'matt@gmail.com', 'correcthorsebatterystaple', 'correcthorsebatterystaple', 'matt', 'stark'),
            'Register an account'
        )
        self.assertIsNotNone(
            User.register(None, 'matt@gmail.com', 'pwd', 'pwd', 'first', 'last'),
            'Attempt to register an account when the name is already taken'
        )
        self.assertIsNone(
            User.authenticate(None, 'matt@gmail.com', 'correcthorsebatterystaple'),
            'Login with valid username and password'
        )
        self.assertIsNotNone(
            User.authenticate(None, 'matt@gmail.com', 'valid'),
            'Attempt to login with wrong password'
        )

    def test_formatting(self):
        self.assertIsNone(
            User.register(None, 'm@gmail.com', 'abc', 'abc', 'first', 'last'),
            'About to test automatic capitalisation'
        )
        user = User.all().filter('email =', 'm@gmail.com').get()
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, 'First')
        self.assertEqual(user.lname, 'Last')

    def test_chg_pwd(self):
        self.assertIsNone(
            User.register(None, 'pwd@gmail.com', 'abc', 'abc', 'first', 'last'),
            'About to test changing of passwords'
        )
        user = User.all().filter('email =', 'pwd@gmail.com').get()
        self.assertIsNotNone(user)
        self.assertIsNotNone(
            user.chgpwd('wrong', 'good', 'good'),
            'Wrong original password'
        )
        self.assertIsNotNone(
            user.chgpwd('abc', 'blah', 'different'),
            'Passwords differ'
        )
        self.assertIsNone(
            User.authenticate(None, 'pwd@gmail.com', 'abc'),
            'Password should not have changed'
        )
        self.assertIsNone(
            user.chgpwd('abc', 'newpwd', 'newpwd'),
            'Valid change of password'
        )
        self.assertIsNone(
            User.authenticate(None, 'pwd@gmail.com', 'newpwd'),
            'Password should have changed'
        )

