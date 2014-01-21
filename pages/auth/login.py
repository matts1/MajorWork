from models import User
from pages import BaseHandler
from globals import VIEW_COURSES_URL
import time


class LoginHandler(BaseHandler):
    template = 'other/index.html'
    require_login = False
    formid = 'login'

    def mypost(self):
        self.err[None] = User.authenticate(
            self,
            self.request.get('email'),
            self.request.get('pwd')
        )
        if self.err[None] is None:
            # The time.sleep is necessary because otherwise the database
            # hasn't updated so there is no-one to log in as
            time.sleep(0.1)
            self.redirect(VIEW_COURSES_URL)
