from models.users import User
from pages.base import BaseHandler
from glob import HOME_URL

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
        self.err[None] = User.authenticate(self, self.email, self.request.get('pwd'))

        # TODO: make the user immediately log in, not have to refresh
        self.redirect(HOME_URL)
