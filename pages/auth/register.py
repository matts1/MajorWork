from globals import VIEW_COURSES_URL
from models import User
from pages import BaseHandler


class RegisterHandler(BaseHandler):
    require_login = False
    template = 'other/index.html'
    formid = 'register'

    def mypost(self):
        if not self.adderr(User.register(
                self,
                self.request.get('email'),
                self.request.get('pwd'),
                self.request.get('confpwd'),
                self.request.get('fname'),
                self.request.get('lname')
        )):
            # all good, try and login for them
            self.redirect(VIEW_COURSES_URL)
