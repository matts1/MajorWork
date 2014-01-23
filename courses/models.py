from django.db import models
import os
from globals import COURSE_TABLE
from auth.models import User
from search.models import Search
from models.validators import is_title, make_title


class Course(models.Model):
    name = models.TextField(required=True)
    code = models.TextField()

    teacher = models.ForeignKey(User, required=True)

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
        course.save()
        Search.add_words(course.name, course.pk, COURSE_TABLE)
        return course

    def students(self):
        return [uc.user for uc in UserCourse.objects.filter(course=self)]

    def __repr__(self):
        return '%s (taught by %s)' % (self.name, self.teacher)

class UserCourse(models.Model):
    user = models.ForeignKey(User, required=True)
    course = models.ForeignKey(Course, required=True)
