from globals import TEACHER
from models import Course
from pages import BaseHandler


class CreateCourseHandler(BaseHandler):
    require_login = TEACHER
    template = 'index.html'

    def mypost(self):
        self.adderr(Course.create(
            self.user,
            self.request.get('name'),
            self.request.get('mode'),
        ))
        # if not self.err:
            # self.redirect() REDIRECT TO THE COURSE PAGE
