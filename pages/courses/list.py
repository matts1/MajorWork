import time
from globals import OPEN_COURSE_URL
from pages import BaseHandler


class ListCoursesHandler(BaseHandler):
    template = "courses/list.html"

    def myget(self):
        return dict(
            my_courses=self.user.courses(),
            taught_courses=self.user.courses_taught()
        )

    def mypost(self):
        success = False
        if self.formid == 'joincourse':
            code = self.request.get('code')
            if code:
                success = True
                course = self.adderr(self.user.join_course(None, code.lower()))
                if not self.err:
                    time.sleep(0.1)  # let it update
                    self.redirect(OPEN_COURSE_URL + str(course.key().id()))

        elif self.formid is not None and len(self.formid) > 4:
            course = self.formid[4:]
            if course.isdigit():
                course = int(course)
                success = True
                self.adderr(self.user.join_course(course))
        if not success:
            self.err[None] = 'Invalid code'
