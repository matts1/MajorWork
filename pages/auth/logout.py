from globals import LOGOUT_URL
from pages.base import BaseHandler


class LogoutHandler(BaseHandler):
    require_login = True

    def myget(self):
        self.user.logout()

        # We redirect to ourselves so that we get into an infinite loop until
        # the cookies update, at which time we go back to the home page
        self.redirect(LOGOUT_URL)
