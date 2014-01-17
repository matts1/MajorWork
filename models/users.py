import time
from models.tests import TestCase
from google.appengine.ext import db
import os
import hashlib
from glob import *
from models.validators import is_email


def encrypt(pwd, salt):
    return hashlib.sha512(salt + pwd).hexdigest().encode('hex')

class User(db.Model):
    email = db.StringProperty(required=True)
    pwd = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)
    session = db.StringProperty(required=False, default=None)
        
    @classmethod
    def authenticate(cls, handler, email, pwd):
        print email
        user = cls.all().filter("email =", email).get()
        if user is not None:
            hashed = hashlib.sha512(user.salt + pwd).hexdigest().encode('hex')
            if hashed != user.pwd:
                return "Incorrect Password"
        else:
            return email + " does not exist in our database"
        user.login(handler)

    @classmethod
    def register(cls, handler, email, pwd, confpwd):
        if not all((pwd, confpwd, is_email(email))):
            return '' # client side error messages
        if pwd != confpwd:
            return 'Your passwords were different'
        if cls.all().filter('email =', email).get():
            return email + ' is already in our database'
        salt = os.urandom(50).encode('hex')
        pwd = encrypt(pwd, salt)
        user = cls(email=email, pwd=pwd, salt=salt)
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
            User.register(None, "matt@gmail.com", "pwd", "diffpwd"),
            "Attempt to register with different passwords"
        )
        self.assertIsNotNone(
            User.register(None, "matt@gmail.com", "", ""),
            "Attempt to register with empty passwords"
        )
        self.assertIsNotNone(
            User.register(None, "", "pwd", "pwd"),
            "Attempt to register with empty email"
        )
        self.assertIsNotNone(
            User.register(None, "blah", "pwd", "diffpwd"),
            "Attempt to register with invalid email"
        )
        self.assertIsNotNone(
            User.register(None, "blah@@g.com", "pwd", "diffpwd"),
            "Attempt to register with another invalid email"
        )
        # don't test more invalid emails - validator is already tested

    def test_register_login(self):
        self.assertIsNotNone(
            User.authenticate(None, "matt@gmail.com", "correcthorsebatterystaple"),
            "Try to login with an email that doesn't exist"
        )
        self.assertIsNone(
            User.register(None, "matt@gmail.com", "correcthorsebatterystaple", "correcthorsebatterystaple"),
            "Register an account"
        )
        self.assertIsNotNone(
            User.register(None, "matt@gmail.com", "pwd", "pwd"),
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
