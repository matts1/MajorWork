from globals import LIST_COURSES_URL
from models import Course
from pages import BaseHandler


class ViewCourseHandler(BaseHandler):
    template = 'courses/view.html'

    def myget(self, course_id):
        course = Course.get_by_id(int(course_id))
        if course is None:
            return self.error(404)
        if not self.user.has_permission(course):
            self.redirect(LIST_COURSES_URL)
        return {'course': course}
