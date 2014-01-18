import datetime
from google.appengine.ext import db
import os
import hashlib
import urllib
from globals import *
from models.validators import is_email, is_name


def encrypt(pwd, salt=None):
    if salt is None:
        salt = os.urandom(50).encode('hex')
        return (hashlib.sha512(salt + pwd).hexdigest().encode('hex'), salt)
    else:
        return hashlib.sha512(salt + pwd).hexdigest().encode('hex')

class User(db.Model):
    email = db.StringProperty(required=True)
    pwd = db.StringProperty(required=True)
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)

    session = db.StringProperty(required=False, default=None)
    session_expiry = db.DateTimeProperty(required=False, default=None)
        
    @classmethod
    def authenticate(cls, handler, email, pwd):
        user = cls.all().filter('email =', email).get()
        if user is not None:
            hashed = encrypt(pwd, user.salt)
            if hashed != user.pwd:
                return 'Incorrect Password'
        else:
            return '%s does not exist in our database. If you need an account, click <a href=\'%s\'>here</a>' % (email, REGISTER_URL)
        user.login(handler)

    @classmethod
    def register(cls, handler, email, pwd, confpwd, fname, lname):
        errs = {}
        if not is_name(fname):
            errs['fname'] = 'The first name must be a valid name (hyphens and letters only, must start and end with a letter)'
        if not is_name(lname):
            errs['lname'] = 'The surname must be a valid name (hyphens and letters only, must start and end with a letter)'
        if not is_email(email):
            errs['email'] = 'Your email is invalid'
        if not all((pwd, confpwd)):
            errs[None] = '' # client side validation
        if pwd != confpwd:
            errs[None] = 'Your passwords were different'
        if cls.all().filter('email =', email).get():
            errs['email'] = email + ' is already in our database'
        if errs:
            return errs
        pwd, salt = encrypt(pwd)
        user = cls(email=email, pwd=pwd, fname=fname.title(), lname=lname.title(), salt=salt)
        user.login(handler)
        user.put()
    
    def login(self, handler):
        self.session = os.urandom(100).encode('hex')
        self.session_expiry = datetime.datetime.now() + datetime.timedelta(days=SESSION_NUM_DAYS)
        self.put()
        if hasattr(handler, 'set_cookie'): # so it doesn't fail in tests
            handler.set_cookie('session', self.session)
    
    def logout(self):
        self.session = None
        self.put()

    def chgpwd(self, oldpwd, newpwd, newpwdconf):
        if encrypt(oldpwd, self.salt) != self.pwd:
            return 'Old password was incorrect'
        if newpwd != newpwdconf:
            return 'Your new passwords were different'
        if not newpwd:
            return '' # client side validation
        self.pwd, self.salt = encrypt(newpwd)
        self.put()

    def gravatar(self, size):
        # http://en.gravatar.com/site/implement/images/python/
        default = "http://www.example.com/default.jpg"
        return '<img src="http://www.gravatar.com/avatar/%s?d=identicon&s=%d" alt="gravatar">' % \
               (hashlib.md5(self.email.lower()).hexdigest(), size)
