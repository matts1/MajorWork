from globals import TEACHER, OPEN_COURSE_URL
from models import Course
from pages import BaseHandler


class CreateCourseHandler(BaseHandler):
    require_login = TEACHER
    template = 'other/index.html'
    formid = 'createcourse'

    def mypost(self):
        course = self.adderr(Course.create(
            self.user,
            self.request.get('name'),
            self.request.get('mode'),
        ))
        if not self.err:
            self.redirect(OPEN_COURSE_URL + str(course.key().id()))
