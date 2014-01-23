from pages import BaseHandler


class ListCoursesHandler(BaseHandler):
    template = "courses/list.html"

    def myget(self):
        return dict(
            my_courses=self.user.courses(),
            taught_courses=self.user.courses_taught()
        )

    def mypost(self):
        if self.formid is not None and len(self.formid) > 4:
            course = self.formid[4:]
            if course.isdigit():
                course = int(course)
                success = True
                self.adderr(self.user.join_course(course))
        if not success:
            self.err[None] = ''
