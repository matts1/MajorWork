from django.db import models
import os
from globals import COURSE_TABLE
from users.models import User
from search.models import Search
from oldmodels.validators import is_title, make_title


class Course(models.Model):
    name = models.TextField(unique=True)
    code = models.TextField(unique=True)

    teacher = models.ForeignKey(User, blank=False)

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
    user = models.ForeignKey(User, blank=False)
    course = models.ForeignKey(Course, blank=False)
