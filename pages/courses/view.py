from models import Course
from pages import BaseHandler


class ViewCourseHandler(BaseHandler):
    template = "courses/view.html"

    def myget(self):
        return dict(
            my_courses=self.user.courses(),
            taught_courses=self.user.courses_taught()
        )
