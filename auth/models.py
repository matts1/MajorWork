from django.db import models

import datetime

from os import urandom
import hashlib

from globals import *
from models.validators import is_email, is_name


def encrypt(pwd, salt=None):
    if salt is None:
        salt = urandom(50).encode('hex')
        return hashlib.sha512(salt + pwd).hexdigest().encode('hex'), salt
    else:
        return hashlib.sha512(salt + pwd).hexdigest().encode('hex')


class User(models.Model):
    email = models.TextField(required=True)
    pwd = models.TextField(required=True)
    fname = models.TextField(required=True)
    lname = models.TextField(required=True)
    salt = models.TextField(required=True)

    session = models.TextField(required=False, default=None)
    session_expiry = models.DateTimeField(required=False, default=None)

    reset_code = models.TextField(required=False, default=None)

    teacher = models.BooleanField(required=True, default=False)

    @classmethod
    def authenticate(cls, handler, email, pwd):
        user = cls.objects.filter(email=email).first()
        if user is not None:
            hashed = encrypt(pwd, user.salt)
            if hashed != user.pwd:
                return 'Incorrect Password'
        else:
            return ('%s does not exist in our database. If you need an account, '
                    'click <a href=\'%s\'>here</a>' % (email, REGISTER_URL))
        user.login(handler)

    @classmethod
    def register(cls, handler, email, pwd, confpwd, fname, lname):
        errs = {}
        if not is_name(fname):
            errs['fname'] = ('The first name must be a valid name (hyphens and letters only, '
                             'must start and end with a letter)')
        if not is_name(lname):
            errs['lname'] = ('The surname must be a valid name (hyphens and letters only, '
                             'must start and end with a letter)')
        if not is_email(email):
            errs['email'] = 'Your email is invalid'
        if not all((pwd, confpwd)):
            errs[None] = ''  # client side validation
        if pwd != confpwd:
            errs[None] = 'Your passwords were different'
        if cls.objects.filter(email=email).first():
            errs['email'] = email + ' is already in our database'
        if errs:
            return errs
        pwd, salt = encrypt(pwd)
        user = cls(email=email, pwd=pwd, fname=fname.title(), lname=lname.title(), salt=salt)
        user.login(handler)
        user.save()

    @classmethod
    def setup_reset(cls, email, send_email=False):
        if email is None:
            return ''  # client side validation
        user = cls.objects.filter(email=email).first()
        if user is None:
            return 'There is no user with the email ' + email
        user.reset_code = urandom(50).encode('hex')
        user.put()
        if send_email:
            user.send_mail(
                'Password Reset',
                'A password reset has been requested for %s %s on %s.\n'
                'If you did not request the reset, don\'t worry, your account is still secure.\n\n'
                'To reset your password go to the following URL.\n'
                'http://%s/doreset?code=%s' %
                (user.fname, user.lname, WEBSITE_URL, WEBSITE_URL, user.reset_code)
            )

    @classmethod
    def do_reset(cls, code, newpwd, confpwd):
        if not all((code, newpwd, confpwd)):
            return ''  # client side validation
        user = cls.objects.filter(reset_code=code).first()
        if user is None:
            return 'The code you provided was wrong. Please check that you copied the url correctly'
        if newpwd != confpwd:
            return 'The passwords were different'
        user.reset_code = None
        user.pwd, user.salt = encrypt(newpwd)
        user.put()

    def login(self, handler):
        self.session = urandom(100).encode('hex')
        self.session_expiry = datetime.datetime.now() + datetime.timedelta(days=SESSION_NUM_DAYS)
        self.save()
        if hasattr(handler, 'set_cookie'):  # so it doesn't fail in tests
            handler.set_cookie('session', self.session)

    def logout(self):
        self.session = None
        self.save()

    def chgpwd(self, oldpwd, newpwd, newpwdconf):
        if not all((oldpwd, newpwd, newpwdconf)):
            return ''  # client side validation
        if encrypt(oldpwd, self.salt) != self.pwd:
            return 'Old password was incorrect'
        if newpwd != newpwdconf:
            return 'Your new passwords were different'
        if not newpwd:
            return ''  # client side validation
        self.pwd, self.salt = encrypt(newpwd)
        self.save()

    def make_teacher(self):
        self.teacher = True
        self.save()

    def join_course(self, course_id, code=None):
        from courses.models import Course, UserCourse  # do this because users.py & courses.py import each other
        if code is not None:
            course = Course.objects.filter(code=code).first()
        elif course_id is not None:
            course = Course.filter(pk=course_id).first()
        else:
            return ''
        if course is None:
            return 'Invalid code'
        if UserCourse.objects.filter(user=self, course=course).first():
            return 'You are already in the course'
        if course.teacher.pk == self.pk:
            return 'You teach that course'
        UserCourse(user=self, course=course).save()
        return course

    def courses(self):
        from courses.models import UserCourse  # do this because users.py & courses.py import each other
        return [uc.course for uc in UserCourse.objects.filter(user=self)]

    def courses_taught(self):
        from courses.models import Course  # do this because users.py & courses.py import each other
        return Course.objects.filter(teacher=self)

    def has_permission(self, course):
        from courses.models import UserCourse  # cross referencing imports
        inside = UserCourse.objects.filter(user=self, course=course).first() \
                is not None or course.teacher.pk == self.pk
        if course.code is None or inside:  # public or we're in it
            course.inside = inside
            return True
        return False

    def gravatar(self, size):
        # http://en.gravatar.com/site/implement/images/python/
        return '<img src="http://www.gravatar.com/avatar/%s?d=identicon&s=%d" alt="gravatar">' % \
               (hashlib.md5(self.email.lower()).hexdigest(), size)

    def __repr__(self):
        return '%s %s' % (self.fname, self.lname)

    def send_mail(self, subject, body):
        # TODO: get mail working
        mail.send_mail(
            sender='Kno Support <support@%s>' % WEBSITE_EMAIL,
            to='%s %s <%s>' % (self.fname, self.lname, self.email),
            subject='Kno: ' + subject,
            body=('Dear %s\n\n%s\n\n'
                  'Please contact us if you have any questions\n\n'
                  'The Kno Team'
                   % (self.fname, body))
        )
