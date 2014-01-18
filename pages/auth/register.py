from glob import HOME_URL
from models.users import User
from pages.base import BaseHandler


class RegisterHandler(BaseHandler):
    formid = 'register'
    require_login = False
    template = 'index.html'
    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.get_data()
        self.err[None] = ''

    def mypost(self):
        self.get_data('email', 'fname', 'lname')

        if not self.adderr(User.register(
                self,
                self.email,
                self.request.get('pwd'),
                self.request.get('confpwd'),
                self.fname,
                self.lname
            )):
            # all good, try and login for them
            self.redirect(HOME_URL)
