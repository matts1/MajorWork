from globals import HOME_URL
from models import User
from pages import BaseHandler


class RegisterHandler(BaseHandler):
    formid = 'register'
    require_login = False
    template = 'index.html'

    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.err[None] = ''

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
            self.redirect(HOME_URL)
