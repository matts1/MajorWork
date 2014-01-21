import os
from google.appengine.ext import db
from models import User
from models.validators import is_title, make_title


class Course(db.Model):
    name = db.StringProperty(required=True)
    code = db.StringProperty()

    teacher = db.ReferenceProperty(User, required=True)

    @classmethod
    def create(cls, user, name, private):
        # PRECONDITION: user is a teacher
        if not is_title(name):
            return 'name', 'Empty Course Name'  # client side error
        name = make_title(name)
        if cls.all().filter('name =', name).get() is not None:
            return 'name', 'Course name is already taken'
        if private:
            code = os.urandom(8).encode('hex')
        else:
            code = None
        course = cls(name=name, teacher=user, code=code)
        course.put()

    def students(self):
        return [uc.user for uc in UserCourse.all().filter('course =', self)]

class UserCourse(db.Model):
    user = db.ReferenceProperty(User, required=True)
    course = db.ReferenceProperty(Course, required=True)
