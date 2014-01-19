from models.users import User
from pages.base import BaseHandler
from globals import HOME_URL
import time


class LoginHandler(BaseHandler):
    formid = 'login'
    template = 'index.html'
    require_login = False

    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.get_data()
        self.err[None] = ''

    def mypost(self):
        self.get_data('email')
        self.err[None] = User.authenticate(
            self,
            self.attrs['email'],
            self.request.get('pwd')
        )
        if self.err[None] is None:
            # The time.sleep is necessary because otherwise the database
            # hasn't updated so there is no-one to log in as
            time.sleep(0.1)
            self.redirect(HOME_URL)
