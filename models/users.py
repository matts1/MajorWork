import time
from models.tests import TestCase
from google.appengine.ext import db
import os
import hashlib
from glob import *
from models.validators import is_email, is_alphabetic, is_name


def encrypt(pwd, salt):
    return hashlib.sha512(salt + pwd).hexdigest().encode('hex')

class User(db.Model):
    email = db.StringProperty(required=True)
    pwd = db.StringProperty(required=True)
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)

    session = db.StringProperty(required=False, default=None)
        
    @classmethod
    def authenticate(cls, handler, email, pwd):
        user = cls.all().filter("email =", email).get()
        if user is not None:
            hashed = hashlib.sha512(user.salt + pwd).hexdigest().encode('hex')
            if hashed != user.pwd:
                return "Incorrect Password"
        else:
            return email + " does not exist in our database"
        user.login(handler)

    @classmethod
    def register(cls, handler, email, pwd, confpwd, fname, lname):
        if not is_name(fname):
            return ('fname', 'The first name must be a valid name (hyphens and letters only, must start and end with a letter)')
        if not is_name(lname):
            return ('lname', 'The surname must be a valid name (hyphens and letters only, must start and end with a letter)')
        if not all((pwd, confpwd, is_email(email))):
            return '' # client side error messages
        if pwd != confpwd:
            return 'Your passwords were different'
        if cls.all().filter('email =', email).get():
            return ('email', email + ' is already in our database')
        salt = os.urandom(50).encode('hex')
        pwd = encrypt(pwd, salt)
        user = cls(email=email, pwd=pwd, fname=fname.title(), lname=lname.title(), salt=salt)
        user.login(handler)
        user.put()
    
    def login(self, handler):
        self.session = os.urandom(100).encode('hex')
        self.put()
        if hasattr(handler, 'set_cookie'): # so it doesn't fail in tests
            handler.set_cookie('session', self.session)
    
    def logout(self):
        self.session = None
        self.put()


class UserTest(TestCase):
    def test_bad_register(self):
        self.assertIsNotNone(
            User.register(None, "matt@gmail.com", "pwd", "diffpwd", "first", "last"),
            "Attempt to register with different passwords"
        )
        self.assertIsNotNone(
            User.register(None, "matt@gmail.com", "", "", "first", "last"),
            "Attempt to register with empty passwords"
        )
        self.assertIsNotNone(
            User.register(None, "", "pwd", "pwd", "first", "last"),
            "Attempt to register with empty email"
        )
        self.assertIsNotNone(
            User.register(None, "m@gmail.com", "pwd", "pwd", "", "last"),
            "Attempt to register with empty first name"
        )
        self.assertIsNotNone(
            User.register(None, "m@gmail.com", "pwd", "pwd", "", "last"),
            "Attempt to register with invalid first name"
        )
        self.assertIsNotNone(
            User.register(None, "m@gmail.com", "pwd", "pwd", "first", ""),
            "Attempt to register with empty surname"
        )
        self.assertIsNotNone(
            User.register(None, "m@gmail.com", "pwd", "pwd", "blah-blah-", "last"),
            "Attempt to register with invalid surname"
        )
        self.assertIsNotNone(
            User.register(None, "blah", "pwd", "diffpwd", "first", "last"),
            "Attempt to register with invalid email"
        )
        self.assertIsNotNone(
            User.register(None, "blah@@g.com", "pwd", "diffpwd", "first", "last"),
            "Attempt to register with another invalid email"
        )
        # don't test more invalid emails - validator is already tested

    def test_register_login(self):
        self.assertIsNotNone(
            User.authenticate(None, "matt@gmail.com", "correcthorsebatterystaple"),
            "Try to login with an email that doesn't exist"
        )
        self.assertIsNone(
            User.register(None, "matt@gmail.com", "correcthorsebatterystaple", "correcthorsebatterystaple", "matt", "stark"),
            "Register an account"
        )
        self.assertIsNotNone(
            User.register(None, "matt@gmail.com", "pwd", "pwd", "first", "last"),
            "Attempt to register an account when the name is already taken"
        )
        self.assertIsNone(
            User.authenticate(None, "matt@gmail.com", "correcthorsebatterystaple"),
            "Login with valid username and password"
        )
        self.assertIsNotNone(
            User.authenticate(None, "matt@gmail.com", "valid"),
            "Attempt to login with wrong password"
        )

    def test_formatting(self):
        self.assertIsNone(
            User.register(None, "m@gmail.com", "abc", "abc", "first", "last"),
            "About to test automatic capitalisation"
        )
        user = User.all().filter("email =", "m@gmail.com").get()
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, "First")
        self.assertEqual(user.lname, "Last")
