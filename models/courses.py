import os
from google.appengine.ext import db
from models import User


class Course(db.Model):
    name = db.StringProperty(required=True)
    code = db.StringProperty(required=True)

    teacher = db.ReferenceProperty(User, required=True)
    # many to many, store on BOTH sides and ensure they're both updated
    students = db.ListProperty(db.Key)

    @classmethod
    def create(cls, user, name, private):
        if not name:
            return ''  # client side error

        course = cls(name=name.title(), teacher=user)
        if private:
            course.code = os.urandom(8).encode('hex')
        else:
            course.code = None
        course.put()
