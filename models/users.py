from google.appengine.ext import db
import os
import hashlib
from glob import *


def encrypt(pwd, salt):
    return hashlib.sha512(salt + pwd).hexdigest().encode('hex')

class User(db.Model):
    email = db.StringProperty(required=True)
    pwd = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)
    session = db.StringProperty(required=False, default=None)
        
    @classmethod
    def authenticate(cls, handler, email, pwd):
        user = User.all().filter("email =", email).get()
        if user is not None:
            hashed = hashlib.sha512(user.salt + pwd).hexdigest().encode('hex')
            if hashed != user.pwd:
                return "Incorrect Password"
        else:
            return "The email does not exist in our database"
        user.login(handler)

    @classmethod
    def register(cls, email, pwd, confpwd):
        if not all((email, pwd, confpwd)):
            return '' # client side error messages
        if pwd != confpwd:
            return 'Your passwords were different'
        if cls.all().filter('email =', email).get():
            return email + ' is already in our database'
        salt = os.urandom(50).encode('hex')
        pwd = encrypt(pwd, salt)
        cls(email=email, pwd=pwd, salt=salt).put()
    
    def login(self, handler):
        self.session = os.urandom(100).encode('hex')
        self.put()
        handler.set_cookie('session', self.session)
    
    def logout(self):
        self.session = None
        self.put()
