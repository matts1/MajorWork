from pages.base import BaseHandler


class CourseHandler(BaseHandler):
    require_login = True
    template = "courses/all.html"
