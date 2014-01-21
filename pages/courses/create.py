from globals import TEACHER
from models import Course
from pages import BaseHandler


class CreateCourseHandler(BaseHandler):
    require_login = TEACHER
    formid = 'createcourse'
    template = 'index.html'

    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.err[None] = ''

    def mypost(self):
        self.adderr(Course.create(
            self.user,
            self.request.get('name'),
            self.request.get('mode'),
        ))
        # if not self.err:
            # self.redirect() REDIRECT TO THE COURSE PAGE
